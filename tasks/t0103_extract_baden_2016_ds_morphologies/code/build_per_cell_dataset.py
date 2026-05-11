"""Build the Baden 2016 DS-cell per-cell dataset asset.

Loads the Dryad .mat container with `load_baden_mat`, filters to the 8
paper-authoritative DS groups (`DS_GROUP_IDS`), assembles one record per cell
with every per-cell field present in the source, and writes:

* `assets/dataset/baden-2016-ds-cells/files/baden-2016-ds-cells.parquet` — the
  per-cell records (Parquet with nested `list<float32>` columns for the
  variable-length functional traces; scalar feature columns retain their
  native precision).
* `assets/dataset/baden-2016-ds-cells/details.json` (dataset asset spec v2).
* `assets/dataset/baden-2016-ds-cells/description.md` (v2 spec, 7 mandatory
  sections plus YAML frontmatter).

Per-cell shape choice: Parquet with `list<float32>` columns is supported by
pyarrow and preserves the time series natively without forcing a column per
sample.  Time axes (`chirp_time`, `bar_time`, ...) are constant across all
cells and are written once into the file-level metadata, not duplicated per
row.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from tasks.t0103_extract_baden_2016_ds_morphologies.code.constants import (
    DATASET_ID,
    DRYAD_DATASET_URL,
    DRYAD_DOI_URL,
    DS_GROUP_IDS,
    DS_GROUP_LABELS,
    FIELD_BAR_BYREPEAT_BYDIR_MEAN,
    FIELD_BAR_QI,
    FIELD_BAR_TC,
    FIELD_CELL_INDEX,
    FIELD_CELL_NUM,
    FIELD_CHIRP_AVG,
    FIELD_CHIRP_QI,
    FIELD_CHIRP_SCALING,
    FIELD_CLUSTER_ID,
    FIELD_COLOR_AVG,
    FIELD_COLOR_QI,
    FIELD_DATE,
    FIELD_DSI,
    FIELD_DSI_PVALUE,
    FIELD_EYE_ID,
    FIELD_FF_INDEX,
    FIELD_GENETICS_PCP,
    FIELD_GENETICS_PV,
    FIELD_GROUP_ID,
    FIELD_GROUP_LABEL,
    FIELD_IMMUNO_CHAT,
    FIELD_IMMUNO_GAD,
    FIELD_IMMUNO_MELANOPSIN,
    FIELD_IMMUNO_SMI,
    FIELD_MOUSE_ID,
    FIELD_ON_OFF_INDEX,
    FIELD_OSI,
    FIELD_OSI_PVALUE,
    FIELD_RF_GAUSS_MEAN_X,
    FIELD_RF_GAUSS_MEAN_Y,
    FIELD_RF_GAUSS_STD_X,
    FIELD_RF_GAUSS_STD_Y,
    FIELD_RF_QI,
    FIELD_RF_SIZE,
    FIELD_RF_TC,
    FIELD_SCAN_NUM,
    FIELD_SELECTED,
    FIELD_SOMA_AREA,
    FIELD_SOMA_VOLUME,
    FIELD_STIM_NUM,
    PAPER_DOI,
    PAPER_ID,
    PAPER_PUB_DATE,
    PAPER_URL,
    PAPER_YEAR,
)
from tasks.t0103_extract_baden_2016_ds_morphologies.code.load_baden_mat import (
    BadenMatData,
    load_baden_mat,
)
from tasks.t0103_extract_baden_2016_ds_morphologies.code.paths import (
    BADEN_MAT_PATH,
    DATASET_DESCRIPTION_PATH,
    DATASET_DETAILS_PATH,
    DATASET_FILES_DIR,
    DATASET_OUT_PARQUET_PATH,
)


@dataclass(frozen=True, slots=True)
class DatasetBuildResult:
    """Outcome of building the DS-cell dataset asset."""

    n_cells: int
    per_group_counts: dict[int, int]
    parquet_path_relative: str
    parquet_bytes: int


@dataclass(frozen=True, slots=True)
class _PerCellArrays:
    """Per-cell columnar views after filtering to DS cells."""

    cell_index: np.ndarray
    group_id: np.ndarray
    cluster_id: np.ndarray
    selected: np.ndarray
    soma_area: np.ndarray
    soma_volume: np.ndarray
    dsi: np.ndarray
    osi: np.ndarray
    dsi_pvalue: np.ndarray
    osi_pvalue: np.ndarray
    ff_index: np.ndarray
    on_off_index: np.ndarray
    chirp_qi: np.ndarray
    bar_qi: np.ndarray
    color_qi: np.ndarray
    rf_qi: np.ndarray
    chirp_scaling: np.ndarray
    rf_diameter: np.ndarray
    rf_gauss_mean_x: np.ndarray
    rf_gauss_mean_y: np.ndarray
    rf_gauss_std_x: np.ndarray
    rf_gauss_std_y: np.ndarray
    immuno_chat: np.ndarray
    immuno_gad: np.ndarray
    immuno_melanopsin: np.ndarray
    immuno_smi: np.ndarray
    genetics_pv: np.ndarray
    genetics_pcp: np.ndarray
    recording_date: list[str]
    mouse_id: np.ndarray
    eye_id: np.ndarray
    scan_num: np.ndarray
    stim_num: np.ndarray
    cell_num: np.ndarray
    chirp_avg_per_cell: list[list[float]]
    bar_tc_per_cell: list[list[float]]
    bar_byrepeat_bydir_mean_per_cell: list[list[float]]
    color_avg_per_cell: list[list[float]]
    rf_tc_per_cell: list[list[float]]


def _filter_ds_indices(*, baden: BadenMatData) -> np.ndarray:
    """Return the cell indices belonging to any DS group, in source order."""
    mask: np.ndarray = np.isin(baden.group_idx, np.asarray(DS_GROUP_IDS, dtype=np.int16))
    return np.where(mask)[0].astype(np.int64)


def _trace_columns_to_lists(
    *,
    matrix: np.ndarray,
    cell_indices: np.ndarray,
) -> list[list[float]]:
    """Slice `matrix[:, cell_indices]` into a list of per-cell float lists."""
    out: list[list[float]] = []
    for idx in cell_indices:
        out.append(matrix[:, idx].astype(np.float64).tolist())
    return out


def _bar_byrepeat_mean_per_cell(
    *,
    bar_byrepeat: np.ndarray,
    cell_indices: np.ndarray,
) -> list[list[float]]:
    """Average `bar_byrepeat` across the 3 repeats for each direction & cell.

    Input shape `(T=32, D=8, R=3, N=11210)` → returns per cell a flat list of
    length `T*D = 256` ordered as `[d0_t0, d0_t1, ..., d7_t31]`.
    """
    repeat_mean: np.ndarray = bar_byrepeat.mean(axis=2)  # (T, D, N)
    out: list[list[float]] = []
    for idx in cell_indices:
        per_cell: np.ndarray = repeat_mean[:, :, idx]  # (T, D)
        # Transpose to (D, T) before flatten so each direction is contiguous.
        out.append(per_cell.T.reshape(-1).astype(np.float64).tolist())
    return out


def _gather_per_cell_arrays(
    *,
    baden: BadenMatData,
    cell_indices: np.ndarray,
) -> _PerCellArrays:
    """Build per-cell columnar arrays for the filtered cell index list."""
    group_ids: np.ndarray = baden.group_idx[cell_indices].astype(np.int64)
    return _PerCellArrays(
        cell_index=cell_indices,
        group_id=group_ids,
        cluster_id=baden.cluster_idx[cell_indices].astype(np.int64),
        selected=baden.selected[cell_indices].astype(np.bool_),
        soma_area=baden.soma_area[cell_indices],
        soma_volume=baden.soma_volume[cell_indices],
        dsi=baden.dsi[cell_indices],
        osi=baden.osi[cell_indices],
        dsi_pvalue=baden.dsi_pvalue[cell_indices],
        osi_pvalue=baden.osi_pvalue[cell_indices],
        ff_index=baden.ff_index[cell_indices],
        on_off_index=baden.on_off_index[cell_indices],
        chirp_qi=baden.chirp_qi[cell_indices],
        bar_qi=baden.bar_qi[cell_indices],
        color_qi=baden.color_qi[cell_indices],
        rf_qi=baden.rf_qi[cell_indices],
        chirp_scaling=baden.chirp_scaling[cell_indices],
        rf_diameter=baden.rf_diameter[cell_indices],
        rf_gauss_mean_x=baden.rf_gauss_mean[cell_indices, 0],
        rf_gauss_mean_y=baden.rf_gauss_mean[cell_indices, 1],
        rf_gauss_std_x=baden.rf_gauss_std[cell_indices, 0],
        rf_gauss_std_y=baden.rf_gauss_std[cell_indices, 1],
        immuno_chat=baden.immuno_chat[cell_indices],
        immuno_gad=baden.immuno_gad[cell_indices],
        immuno_melanopsin=baden.immuno_melanopsin[cell_indices],
        immuno_smi=baden.immuno_smi[cell_indices],
        genetics_pv=baden.genetics_pv[cell_indices],
        genetics_pcp=baden.genetics_pcp[cell_indices],
        recording_date=[baden.recording_date[i] for i in cell_indices.tolist()],
        mouse_id=baden.mouse_id[cell_indices],
        eye_id=baden.eye_id[cell_indices],
        scan_num=baden.scan_num[cell_indices],
        stim_num=baden.stim_num[cell_indices],
        cell_num=baden.cell_num[cell_indices],
        chirp_avg_per_cell=_trace_columns_to_lists(
            matrix=baden.chirp_avg,
            cell_indices=cell_indices,
        ),
        bar_tc_per_cell=_trace_columns_to_lists(
            matrix=baden.bar_tc,
            cell_indices=cell_indices,
        ),
        bar_byrepeat_bydir_mean_per_cell=_bar_byrepeat_mean_per_cell(
            bar_byrepeat=baden.bar_byrepeat,
            cell_indices=cell_indices,
        ),
        color_avg_per_cell=_trace_columns_to_lists(
            matrix=baden.color_avg,
            cell_indices=cell_indices,
        ),
        rf_tc_per_cell=_trace_columns_to_lists(
            matrix=baden.rf_tc,
            cell_indices=cell_indices,
        ),
    )


@dataclass(frozen=True, slots=True)
class _TableMetadata:
    """File-level metadata persisted in Parquet key/value metadata."""

    dataset_id: str
    paper_id: str
    paper_doi: str
    n_cells: int
    ds_group_ids: list[int]
    ds_group_labels: dict[str, str]
    chirp_time_s: list[float]
    bar_time_s: list[float]
    color_time_s: list[float]
    rf_time_s: list[float]
    bar_byrepeat_layout: str
    notes: list[str] = field(default_factory=list)


def _build_arrow_table(
    *,
    arrays: _PerCellArrays,
    baden: BadenMatData,
) -> pa.Table:
    """Build a pyarrow.Table with one row per cell and nested list columns."""
    group_labels: list[str] = [DS_GROUP_LABELS[int(g)] for g in arrays.group_id.tolist()]
    columns: dict[str, pa.Array] = {
        FIELD_CELL_INDEX: pa.array(arrays.cell_index, type=pa.int64()),
        FIELD_GROUP_ID: pa.array(arrays.group_id, type=pa.int32()),
        FIELD_GROUP_LABEL: pa.array(group_labels, type=pa.string()),
        FIELD_CLUSTER_ID: pa.array(arrays.cluster_id, type=pa.int32()),
        FIELD_SELECTED: pa.array(arrays.selected, type=pa.bool_()),
        FIELD_SOMA_AREA: pa.array(arrays.soma_area, type=pa.float64()),
        FIELD_SOMA_VOLUME: pa.array(arrays.soma_volume, type=pa.float64()),
        FIELD_DSI: pa.array(arrays.dsi, type=pa.float64()),
        FIELD_OSI: pa.array(arrays.osi, type=pa.float64()),
        FIELD_DSI_PVALUE: pa.array(arrays.dsi_pvalue, type=pa.float64()),
        FIELD_OSI_PVALUE: pa.array(arrays.osi_pvalue, type=pa.float64()),
        FIELD_FF_INDEX: pa.array(arrays.ff_index, type=pa.float64()),
        FIELD_ON_OFF_INDEX: pa.array(arrays.on_off_index, type=pa.float64()),
        FIELD_CHIRP_QI: pa.array(arrays.chirp_qi, type=pa.float64()),
        FIELD_BAR_QI: pa.array(arrays.bar_qi, type=pa.float64()),
        FIELD_COLOR_QI: pa.array(arrays.color_qi, type=pa.float64()),
        FIELD_RF_QI: pa.array(arrays.rf_qi, type=pa.float64()),
        FIELD_CHIRP_SCALING: pa.array(arrays.chirp_scaling, type=pa.float64()),
        FIELD_RF_SIZE: pa.array(arrays.rf_diameter, type=pa.float64()),
        FIELD_RF_GAUSS_MEAN_X: pa.array(arrays.rf_gauss_mean_x, type=pa.float64()),
        FIELD_RF_GAUSS_MEAN_Y: pa.array(arrays.rf_gauss_mean_y, type=pa.float64()),
        FIELD_RF_GAUSS_STD_X: pa.array(arrays.rf_gauss_std_x, type=pa.float64()),
        FIELD_RF_GAUSS_STD_Y: pa.array(arrays.rf_gauss_std_y, type=pa.float64()),
        FIELD_IMMUNO_CHAT: pa.array(arrays.immuno_chat, type=pa.float64()),
        FIELD_IMMUNO_GAD: pa.array(arrays.immuno_gad, type=pa.float64()),
        FIELD_IMMUNO_MELANOPSIN: pa.array(arrays.immuno_melanopsin, type=pa.float64()),
        FIELD_IMMUNO_SMI: pa.array(arrays.immuno_smi, type=pa.float64()),
        FIELD_GENETICS_PV: pa.array(arrays.genetics_pv, type=pa.float64()),
        FIELD_GENETICS_PCP: pa.array(arrays.genetics_pcp, type=pa.float64()),
        FIELD_DATE: pa.array(arrays.recording_date, type=pa.string()),
        FIELD_MOUSE_ID: pa.array(arrays.mouse_id, type=pa.int32()),
        FIELD_EYE_ID: pa.array(arrays.eye_id, type=pa.int32()),
        FIELD_SCAN_NUM: pa.array(arrays.scan_num, type=pa.int32()),
        FIELD_STIM_NUM: pa.array(arrays.stim_num, type=pa.int32()),
        FIELD_CELL_NUM: pa.array(arrays.cell_num, type=pa.int32()),
        # Functional trace columns are stored as `list<float32>` rather than
        # `list<float64>` to keep the on-disk Parquet under the 5 MB per-file
        # limit enforced by the pre-merge verificator. Float32 (~6-7 sig digits)
        # is well within scientific tolerance for Baden 2016 traces, which are
        # normalised cluster-mean responses in roughly the [-1, 1] range.
        FIELD_CHIRP_AVG: pa.array(arrays.chirp_avg_per_cell, type=pa.list_(pa.float32())),
        FIELD_BAR_TC: pa.array(arrays.bar_tc_per_cell, type=pa.list_(pa.float32())),
        FIELD_BAR_BYREPEAT_BYDIR_MEAN: pa.array(
            arrays.bar_byrepeat_bydir_mean_per_cell,
            type=pa.list_(pa.float32()),
        ),
        FIELD_COLOR_AVG: pa.array(arrays.color_avg_per_cell, type=pa.list_(pa.float32())),
        FIELD_RF_TC: pa.array(arrays.rf_tc_per_cell, type=pa.list_(pa.float32())),
    }

    metadata: _TableMetadata = _TableMetadata(
        dataset_id=DATASET_ID,
        paper_id=PAPER_ID,
        paper_doi=PAPER_DOI,
        n_cells=int(arrays.cell_index.shape[0]),
        ds_group_ids=DS_GROUP_IDS,
        ds_group_labels={str(k): v for k, v in DS_GROUP_LABELS.items()},
        chirp_time_s=baden.chirp_time.tolist(),
        bar_time_s=baden.bar_time.tolist(),
        color_time_s=baden.color_time.tolist(),
        rf_time_s=baden.rf_time.tolist(),
        bar_byrepeat_layout=(
            "Per cell a flat 256-element list ordered as direction-major "
            "(D=8 directions, T=32 time bins): [d0_t0, d0_t1, ..., d0_t31, "
            "d1_t0, ..., d7_t31]. Values are the mean across the 3 stimulus "
            "repeats reported in the Dryad container."
        ),
        notes=[
            (
                "Per-cell IPL stratification depth profile is NOT available in the "
                "Dryad release; the source .mat exposes scan-level structural volumes "
                "(`structural` and `rois`) rather than per-cell IPL profiles."
            ),
            (
                "Per-cell soma retinal location (x, y / eccentricity) is NOT exposed "
                "in the Dryad release. `rf_gauss_mean_*` is the receptive field centre "
                "in stimulus-screen coordinates and is a downstream proxy, not the soma "
                "position on the retinal surface."
            ),
            (
                "Per-cell morphological reconstruction is NOT in the Dryad release. "
                "Baden 2016 is a primarily functional dataset; DS-cell morphologies "
                "should be sourced from a complementary paper (Bae 2018, Ran 2020) in "
                "a separate task."
            ),
        ],
    )
    metadata_bytes: bytes = json.dumps(
        {
            "dataset_id": metadata.dataset_id,
            "paper_id": metadata.paper_id,
            "paper_doi": metadata.paper_doi,
            "n_cells": metadata.n_cells,
            "ds_group_ids": metadata.ds_group_ids,
            "ds_group_labels": metadata.ds_group_labels,
            "chirp_time_s": metadata.chirp_time_s,
            "bar_time_s": metadata.bar_time_s,
            "color_time_s": metadata.color_time_s,
            "rf_time_s": metadata.rf_time_s,
            "bar_byrepeat_layout": metadata.bar_byrepeat_layout,
            "notes": metadata.notes,
        },
        indent=2,
    ).encode("utf-8")
    schema: pa.Schema = pa.schema(
        [(name, arr.type) for name, arr in columns.items()],
        metadata={b"baden_2016_ds_cells_metadata": metadata_bytes},
    )
    return pa.table(columns, schema=schema)


def build_dataset_parquet(*, baden: BadenMatData) -> DatasetBuildResult:
    """Filter to DS cells and write the per-cell Parquet file."""
    DATASET_FILES_DIR.mkdir(parents=True, exist_ok=True)
    cell_indices: np.ndarray = _filter_ds_indices(baden=baden)
    arrays: _PerCellArrays = _gather_per_cell_arrays(
        baden=baden,
        cell_indices=cell_indices,
    )
    table: pa.Table = _build_arrow_table(arrays=arrays, baden=baden)
    # zstd at maximum level (22) is used so the file stays comfortably below the
    # 5 MiB pre-merge limit. Compression is a one-time cost at build time and a
    # no-op at read time (decompression speed is independent of zstd level).
    pq.write_table(
        table=table,
        where=str(DATASET_OUT_PARQUET_PATH),
        compression="zstd",
        compression_level=22,
    )
    per_group_counts: dict[int, int] = {
        int(g): int((arrays.group_id == g).sum()) for g in DS_GROUP_IDS
    }
    parquet_bytes: int = DATASET_OUT_PARQUET_PATH.stat().st_size
    return DatasetBuildResult(
        n_cells=int(cell_indices.shape[0]),
        per_group_counts=per_group_counts,
        parquet_path_relative="files/baden-2016-ds-cells.parquet",
        parquet_bytes=parquet_bytes,
    )


# ---------------------------------------------------------------------------
# details.json
# ---------------------------------------------------------------------------


_AUTHORS: list[dict[str, str | None]] = [
    {
        "name": "Tom Baden",
        "country": "DE",
        "institution": "University of Tübingen",
        "orcid": "0000-0002-7758-6536",
    },
    {
        "name": "Philipp Berens",
        "country": "DE",
        "institution": "University of Tübingen",
        "orcid": "0000-0002-0199-4727",
    },
    {
        "name": "Katrin Franke",
        "country": "DE",
        "institution": "University of Tübingen",
        "orcid": None,
    },
    {
        "name": "Miroslav Román Rosón",
        "country": "DE",
        "institution": "University of Tübingen",
        "orcid": None,
    },
    {
        "name": "Matthias Bethge",
        "country": "DE",
        "institution": "University of Tübingen",
        "orcid": None,
    },
    {
        "name": "Thomas Euler",
        "country": "DE",
        "institution": "University of Tübingen",
        "orcid": "0000-0002-4567-6966",
    },
]
_INSTITUTIONS: list[dict[str, str]] = [
    {
        "name": "University of Tübingen",
        "country": "DE",
    },
]


def write_dataset_details(*, build: DatasetBuildResult) -> None:
    """Write `assets/dataset/baden-2016-ds-cells/details.json` (spec v2)."""
    size_desc: str = (
        f"{build.n_cells} retinal ganglion / displaced amacrine cells from the 8 "
        f"paper-authoritative DS-containing groups (G2/G6/G12/G13/G16/G25/G26/G29) "
        f"of Baden 2016, one row per cell with functional traces (chirp 249 samples, "
        f"moving-bar 32 samples, moving-bar by 8 directions 256 samples, colour 96 "
        f"samples, RF temporal kernel 80 samples) and per-cell selectivity indices, "
        f"soma area/volume, RF Gaussian fit, immuno (ChAT, GAD, melanopsin, SMI-32) "
        f"and genetics (PV, PCP2) flags. NO per-cell IPL stratification depth and "
        f"NO morphology in the Dryad release."
    )
    details: dict[str, object] = {
        "spec_version": "2",
        "dataset_id": DATASET_ID,
        "name": "Baden 2016 RGC direction-selective subset",
        "version": "v1",
        "short_description": (
            "Per-cell functional fingerprints (chirp, moving-bar, colour, RF) and "
            "metadata for 1,238 cells from the 8 paper-authoritative direction-"
            "selective groups of Baden et al. 2016. No morphologies — Baden 2016 is "
            "a functional dataset."
        ),
        "description_path": "description.md",
        "source_paper_id": PAPER_ID,
        "url": DRYAD_DATASET_URL,
        "download_url": DRYAD_DOI_URL,
        "year": PAPER_YEAR,
        "date_published": PAPER_PUB_DATE,
        "authors": _AUTHORS,
        "institutions": _INSTITUTIONS,
        "license": "CC0-1.0",
        "access_kind": "public",
        "size_description": size_desc,
        "files": [
            {
                "path": build.parquet_path_relative,
                "description": (
                    "Per-cell Parquet table for the 8 DS groups. One row per cell; "
                    "functional traces stored as nested list<float32> columns "
                    "(scalar feature columns retain native precision). "
                    "Stimulus time axes and the moving-bar direction-major layout are "
                    "recorded in the Parquet file-level key/value metadata under "
                    "key `baden_2016_ds_cells_metadata`."
                ),
                "format": "parquet",
            },
        ],
        "categories": [
            "direction-selectivity",
            "retinal-ganglion-cell",
        ],
    }
    DATASET_DETAILS_PATH.write_text(
        json.dumps(details, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# description.md
# ---------------------------------------------------------------------------


def _build_description_markdown(*, build: DatasetBuildResult) -> str:
    """Render `description.md` content for the DS-cell asset (spec v2)."""
    group_counts_rows: list[str] = []
    for g in DS_GROUP_IDS:
        label: str = DS_GROUP_LABELS[g]
        n: int = build.per_group_counts[g]
        group_counts_rows.append(f"| G{g} | {label} | {n} |")
    counts_table: str = "\n".join(group_counts_rows)
    return f"""---
spec_version: "2"
dataset_id: "{DATASET_ID}"
summarized_by_task: "t0103_extract_baden_2016_ds_morphologies"
date_summarized: "2026-05-11"
---

# Baden 2016 RGC Direction-Selective Subset

## Metadata

* **Name**: Baden 2016 RGC direction-selective subset
* **Year**: 2016
* **Authors**: Tom Baden, Philipp Berens, Katrin Franke, Miroslav Román Rosón,
  Matthias Bethge, Thomas Euler — University of Tübingen
* **Source paper**: Baden et al., *Nature* 529:345–350 ([10.1038/nature16468]({PAPER_URL}))
* **Source data**: Dryad [10.5061/dryad.d9v38]({DRYAD_DATASET_URL})
* **License**: CC0-1.0 (Dryad-default)
* **Access**: public
* **Size**: {build.n_cells} cells across 8 DS-containing groups (out of the 11,210 cell
  Dryad release)
* **Container**: Parquet with nested `list<float32>` columns for traces (scalar
  feature columns retain native precision)

## Overview

This dataset is the direction-selective (DS) subset of the Baden et al. 2016 *Nature*
release of functional fingerprints for ~11,000 mouse retinal ganglion cells (RGCs) and
displaced amacrine cells (dACs) measured with two-photon Ca2+ imaging. Each row is one
cell, and the cells are drawn from the **8 paper-authoritative DS groups** that the
Baden 2016 main text enumerates ("Most DS cells (70%) were sorted into 8 groups (G 2, 6,
12, 13, 16, 25, 26, 29).").

The filter from the source 11,210-cell release to the {build.n_cells}-cell DS subset is
exact: a single boolean test on the `group_idx` array of the source `.mat` against the
list `{{2, 6, 12, 13, 16, 25, 26, 29}}`. No re-clustering, re-classification, or trace
refitting is performed — the cells, indices, and trace values are passed through
exactly as released.

The dataset's purpose is to ground downstream DSGC compartmental-modelling tasks
(parameter-envelope tuning, joint-pass validation, biologically grounded null
distributions) in a population of real DS cells from one well-characterised source,
rather than only the single canonical morphology used in t0024 and its descendants.

### Important scope note — paper-authoritative DS set vs. original task brief

The task brief (`task_description.md`) originally enumerated DS groups as
`{{2, 17, 18, 19, 22, 35, 36, 40}}`. That list does not match the paper's own DS
enumeration: only G2 overlaps. The other seven IDs in the original list either refer to
non-DS RGC groups in the Baden 2016 taxonomy (G17 = "ON local trans.", G18 = "ON
trans.", G19 = "ON trans., large", G22 = "ON sust.") or to displaced amacrine
subgroups beyond G32 whose DS status is not asserted by the visualisation scripts. The
user resolved the ambiguity by explicitly choosing the paper-authoritative set, and
this dataset therefore reflects the paper's own DS set `{{2, 6, 12, 13, 16, 25, 26,
29}}`. The original brief list is preserved verbatim in `task_description.md` for
audit; the discrepancy and its resolution are recorded in
`code/visualization_code_notes.md` (see "Cluster ID reconciliation" and "Resolution: DS
group set").

## Content & Annotation

Each Parquet row carries the following per-cell fields (see Statistics for value ranges
and Usage Notes for loading):

* **Cluster / group assignment** — `group_id` (one of `{{2, 6, 12, 13, 16, 25, 26,
  29}}`), `group_label` (human-readable name from `plotStamp.m`), `cluster_id` (the
  finer Baden 2016 cluster index from the .mat `cluster_idx` array), and `selected`
  (the boolean response-quality mask `sel_idx`).
* **Selectivity indices** — `dsi`, `osi` (both 0..1), with their permutation-test
  p-values `dsi_pvalue`, `osi_pvalue` (DS cells have `dsi_pvalue < 0.05`).
* **Functional indices** — `ff_index` (full-field, -1..1), `on_off_index` (-1..1).
* **Per-stimulus quality indices** — `chirp_qi`, `bar_qi`, `color_qi`, `rf_qi` and the
  amplitude-scaling factor `chirp_scaling`.
* **Soma morphology (limited)** — `soma_area_um2`, `soma_volume_um3`. Per-cell IPL
  stratification depth and full dendritic morphology are **NOT** in the Dryad release.
* **Receptive field** — `rf_diameter_um`, plus the 2-D Gaussian-fit centre
  (`rf_gauss_mean_x`, `rf_gauss_mean_y`) and standard deviation
  (`rf_gauss_std_x`, `rf_gauss_std_y`) in stimulus-screen coordinates.
* **Immunohistochemistry / genetics flags** — `immuno_chat`, `immuno_gad`,
  `immuno_melanopsin`, `immuno_smi32`, `genetics_pv`, `genetics_pcp`. NaN means "not
  stained / not genetically labelled for this animal"; 0 vs >0 distinguishes
  negative from positive.
* **Cell-of-origin metadata** — `recording_date`, `mouse_id`, `eye_id`, `scan_num`,
  `stim_num`, `cell_num` (the per-mouse cell index used in the original Baden lab
  acquisition pipeline).
* **Functional traces** (nested `list<float32>` Parquet columns; see Usage
  Notes for the rationale):
  * `chirp_avg` — cluster-mean chirp response per cell, 249 samples on `chirp_time`.
  * `bar_tc` — cluster-mean moving-bar time course per cell, 32 samples on `bar_time`.
  * `bar_byrepeat_bydir_mean` — moving-bar response averaged across the 3 stimulus
    repeats, flattened as 8 directions × 32 time bins = 256 floats per cell ordered as
    `[d0_t0, ..., d0_t31, d1_t0, ..., d7_t31]`. The 8 directions span 360° in 45°
    steps per the Baden 2016 moving-bar protocol.
  * `color_avg` — coloured-stimulus cluster mean, 96 samples on `color_time`.
  * `rf_tc` — spike-triggered temporal RF kernel, 80 samples on `rf_time`.

Stimulus time axes (`chirp_time`, `bar_time`, `color_time`, `rf_time`) are constant
across cells and are stored once in the Parquet file-level metadata under the key
`baden_2016_ds_cells_metadata`. The same metadata block also documents the
`bar_byrepeat_bydir_mean` layout and three explicit "what's missing" notes.

### What is NOT in this dataset (gaps inherited from the Dryad release)

* **No per-cell IPL stratification depth profile.** The Dryad `.mat` exposes a
  scan-level `structural` volume and per-scan `rois`; the paper reports IPL profiles
  per group derived from these scans, but the per-cell IPL profile field is not in the
  release.
* **No per-cell retinal soma coordinates.** The `noise_time` struct (despite its
  misleading name — it is the cell-of-origin metadata struct) does not carry retinal
  (x, y) or eccentricity. The `rf_gauss_mean_*` fields are stimulus-screen receptive-
  field centres, which are a downstream readout of the cell's position relative to the
  stimulus monitor, not the soma's position on the retina.
* **No dendritic morphology.** Baden 2016 is a primarily functional dataset. The
  dye-fill morphologies for the DS-RGC types described in the paper are scattered
  across complementary references. A follow-up task should source the DS-cell
  morphologies from a complementary paper such as Bae et al. 2018 (which provides
  dense reconstructions for several Baden cluster IDs) or Ran et al. 2020 (which
  catalogues morphologies for ON-OFF DS cells in particular). Sourcing those is **out
  of scope for t0103** by design and is left as a separate task.

## Statistics

| Group | Label | Cells |
|---|---|---|
{counts_table}

**Total cells**: {build.n_cells} (matches the sum of the eight per-group counts
exactly).

The per-group counts cross-check exactly against the source `group_idx` array
(`code/group_count_check.json` records the comparison; all eight deltas are zero
because the produced count and the reference count are both computed directly from
`group_idx`).

Selectivity-index distribution within DS groups (from the source `.mat`):

* `dsi`: 0..1, with the DS-defining permutation test in `dsi_pvalue`. Cells with
  `dsi_pvalue < 0.05` are the "significantly direction-selective" subset within each
  group.
* `osi`: 0..1, with `osi_pvalue` analogous for orientation selectivity. Some groups
  (e.g. G29 "ON local sust. OS") are dominated by OS rather than DS cells but are still
  included in the paper's 8-group DS set.

Trace lengths are constant across all cells: chirp 249 samples, moving-bar 32 samples
(per direction & repeat dimension; aggregate moving-bar `bar_tc` is also 32), colour 96
samples, RF kernel 80 samples.

## Usage Notes

### Trace column precision (float32)

The five functional-trace list columns (`chirp_avg`, `bar_tc`,
`bar_byrepeat_bydir_mean`, `color_avg`, `rf_tc`) are stored as
`list<float32>` to keep the single on-disk Parquet file under the project's
5 MB per-file pre-merge limit (PM-E011). Float32 retains ~6-7 significant
decimal digits, which is comfortably below the noise floor of Baden 2016's
normalised cluster-mean traces (roughly in `[-1, 1]` range). Scalar feature
columns (DSI, OSI, soma area/volume, RF Gaussian-fit parameters, etc.)
retain their native `float64` precision, since they are cheap on disk and
some downstream consumers may prefer them at full precision. Cast a trace
back to `float64` at load time if a particular analysis requires it:

```python
import numpy as np

chirp = np.asarray(df.loc[i, "chirp_avg"], dtype=np.float64)
```

### Loading

```python
import pyarrow.parquet as pq

table = pq.read_table("files/baden-2016-ds-cells.parquet")
df = table.to_pandas()  # one row per cell; trace columns are lists of float32
```

### Stimulus time axes

The Parquet file's key/value metadata holds the four stimulus time axes as JSON. Read
them with:

```python
import json, pyarrow.parquet as pq

meta = json.loads(
    pq.read_metadata("files/baden-2016-ds-cells.parquet")
    .metadata[b"baden_2016_ds_cells_metadata"]
)
chirp_time_s = meta["chirp_time_s"]      # length 249
bar_time_s   = meta["bar_time_s"]        # length 32
color_time_s = meta["color_time_s"]      # length 96
rf_time_s    = meta["rf_time_s"]         # length 80
```

### Direction-major moving-bar trace

`bar_byrepeat_bydir_mean` is the moving-bar response averaged across the 3 stimulus
repeats per direction, flattened as direction-major:

```text
[d0_t0, d0_t1, ..., d0_t31, d1_t0, ..., d7_t31]   # length 256
```

To reshape one cell's response back to `(D=8, T=32)`:

```python
import numpy as np

mat = np.asarray(df.loc[i, "bar_byrepeat_bydir_mean"]).reshape(8, 32)
```

### Quirks / pitfalls

* **NaN means "not labelled"** for the `immuno_*` and `genetics_*` columns. Use
  `pandas.isna` / `numpy.isnan` to filter, not `== 0` (0 means "stained but negative").
* **`group_id` and `cluster_id` are two different things.** `group_id` is the coarser
  Baden 2016 group taxonomy (1..46, with 33+ being displaced amacrine subgroups);
  `cluster_id` is the finer 75-way cluster index from the .mat `cluster_idx` array.
  Downstream consumers should filter on `group_id`.
* **No per-cell IPL depth / morphology**, as noted in Content & Annotation. If a
  downstream task needs those, source from Bae 2018 or Ran 2020 in a separate task.

## Main Ideas

* This dataset is the **filtered DS subset** of Baden 2016 — exact, no re-analysis. The
  filter is `group_idx ∈ {{2, 6, 12, 13, 16, 25, 26, 29}}`, taken verbatim from the
  paper's own DS-group enumeration.
* The dataset supplies **functional fingerprints, RF parameters, soma area/volume, and
  cell-of-origin metadata** but **not morphologies or per-cell IPL profiles**. A
  morphology source for DS-RGC dendritic trees is a separate task (Bae 2018 / Ran
  2020).
* The original task brief used a different 8-group list (`{{2, 17, 18, 19, 22, 35, 36,
  40}}`) that overlaps the paper's set only at G2. The user resolved the discrepancy in
  favour of the paper's set; the original list is preserved in `task_description.md`
  and the reconciliation is documented in `code/visualization_code_notes.md`.

## Summary

This dataset is the direction-selective subset of the Baden et al. 2016 *Nature*
release of functional fingerprints for ~11,000 mouse RGCs / dACs. Each of the
{build.n_cells} rows is one cell drawn from the 8 paper-authoritative DS groups (G2,
G6, G12, G13, G16, G25, G26, G29), with every per-cell field exposed by the Dryad .mat
container that is meaningful per-cell: cluster/group assignment, selectivity indices
and their permutation p-values, soma area/volume, RF Gaussian-fit parameters,
immuno/genetics labels, cell-of-origin metadata, and the four functional traces
(chirp, moving-bar mean, moving-bar by direction & repeat-mean, colour, RF temporal
kernel).

For this project the dataset's primary use is to ground downstream DSGC
compartmental-modelling tasks in a real DS-cell population. Functional traces and
selectivity indices feed parameter-envelope checks for synthetic DSGCs (t0090 lineage)
and provide null distributions for the t0102 joint-pass validation. The main
limitation is the absence of per-cell IPL stratification profiles and full dendritic
morphologies — those should be sourced from Bae 2018 or Ran 2020 in a separate
follow-up task, which this dataset's Main Ideas and the Resolution-decision note in
`code/visualization_code_notes.md` flag explicitly. Compared to manually digitising
DS-cell traces from publication figures, this asset gives downstream tasks direct,
authoritative cluster-mean and per-cell responses with no estimation error.
"""


def write_dataset_description(*, build: DatasetBuildResult) -> None:
    """Write `assets/dataset/baden-2016-ds-cells/description.md` (spec v2)."""
    content: str = _build_description_markdown(build=build)
    DATASET_DESCRIPTION_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    baden: BadenMatData = load_baden_mat(mat_path=BADEN_MAT_PATH)
    build: DatasetBuildResult = build_dataset_parquet(baden=baden)
    write_dataset_details(build=build)
    write_dataset_description(build=build)
    print(f"Wrote {DATASET_OUT_PARQUET_PATH} ({build.parquet_bytes:,} bytes)")
    print(f"Wrote {DATASET_DETAILS_PATH}")
    print(f"Wrote {DATASET_DESCRIPTION_PATH}")
    print(f"Total cells: {build.n_cells}")
    for g in DS_GROUP_IDS:
        n: int = build.per_group_counts[g]
        print(f"  G{g:>3d} ({DS_GROUP_LABELS[g]}): {n}")


if __name__ == "__main__":
    main()
