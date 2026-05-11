"""Load the Baden 2016 Dryad MATLAB container into typed Python structures.

The Dryad release `BadenEtAl_RGCs_2016_v1.mat` is a MATLAB 5.0 MAT-file with
~46 top-level arrays.  Each array is either:

* a per-cell column (`(11210, 1)` or `(11210, K)`) — one row per RGC/AC,
* a stimulus time axis (`(1, T)`) — shared across all cells,
* a per-cell trace matrix (`(T, 11210)`) — one column per cell,
* a scan-level array (`(64, 64, 171)`, `(20, 15, 1750, 171)`) — one slice per
  scan field, NOT per cell.

This module exposes only the per-cell-relevant arrays — scan-level structural
imaging volumes (`structural`, `rois`, `noise_stim`) are deliberately omitted
since the task scope is per-cell extraction.

The `BadenMatData` dataclass below is a frozen view over the loaded arrays.
All NumPy arrays returned use float64 / int16 etc. as in the source file.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import scipy.io

from tasks.t0103_extract_baden_2016_ds_morphologies.code.constants import (
    TOTAL_BADEN_CELLS_EXPECTED,
)


@dataclass(frozen=True, slots=True)
class BadenMatData:
    """Typed view over the Baden 2016 Dryad .mat container.

    All `(N,)` arrays are flat per-cell columns (N = 11210). All `(T, N)`
    arrays carry one column per cell. Time axes are 1-D.
    """

    n_cells: int

    # Cluster / group assignments.
    group_idx: np.ndarray  # (N,) int16; -1 = unassigned, 1..46 valid
    cluster_idx: np.ndarray  # (N,) int16; finer-grained subdivision
    selected: np.ndarray  # (N,) bool; quality-selected for clustering

    # Cluster -> group lookup (1..75 cluster IDs -> 1..46 group IDs).
    cluster_to_group: np.ndarray  # (75,) int

    # Selectivity scores.
    dsi: np.ndarray  # (N,) float64
    osi: np.ndarray  # (N,) float64
    dsi_pvalue: np.ndarray  # (N,) float64; cell_dp
    osi_pvalue: np.ndarray  # (N,) float64; cell_op

    # Functional indices.
    ff_index: np.ndarray  # (N,) float64; full-field index
    on_off_index: np.ndarray  # (N,) float64; ON-OFF index

    # Quality indices per stimulus.
    chirp_qi: np.ndarray  # (N,) float64
    bar_qi: np.ndarray  # (N,) float64
    color_qi: np.ndarray  # (N,) float64
    rf_qi: np.ndarray  # (N,) float64
    chirp_scaling: np.ndarray  # (N,) float64

    # Soma morphology (limited).
    soma_area: np.ndarray  # (N,) float64; um^2
    soma_volume: np.ndarray  # (N,) float64; um^3

    # Receptive field.
    rf_diameter: np.ndarray  # (N,) float64; um
    rf_gauss_mean: np.ndarray  # (N, 2) float64; RF Gaussian fit centre x, y
    rf_gauss_std: np.ndarray  # (N, 2) float64; RF Gaussian fit std x, y

    # Immuno / genetics flags.
    immuno_chat: np.ndarray  # (N,) float64; ChAT label (DS amacrine marker)
    immuno_gad: np.ndarray  # (N,) float64; GAD67 (GABAergic / dAC marker)
    immuno_melanopsin: np.ndarray  # (N,) float64; melanopsin (ipRGC marker)
    immuno_smi: np.ndarray  # (N,) float64; SMI-32 (alpha-RGC marker)
    genetics_pv: np.ndarray  # (N,) float64; Parvalbumin Cre line
    genetics_pcp: np.ndarray  # (N,) float64; PCP2 Cre line

    # Cell-of-origin metadata.
    recording_date: list[str]  # length N
    mouse_id: np.ndarray  # (N,) int
    eye_id: np.ndarray  # (N,) int
    scan_num: np.ndarray  # (N,) int
    stim_num: np.ndarray  # (N,) int
    cell_num: np.ndarray  # (N,) int

    # Functional traces (time axes are shared across all cells).
    chirp_time: np.ndarray  # (T_chirp,) float64
    chirp_avg: np.ndarray  # (T_chirp, N) float64 — cluster-mean chirp
    bar_time: np.ndarray  # (T_bar,) float64
    bar_tc: np.ndarray  # (T_bar, N) float64 — moving-bar cluster mean
    bar_byrepeat: np.ndarray  # (T_bar, 8, 3, N) float64 — by direction & repeat
    color_time: np.ndarray  # (T_color,) float64
    color_avg: np.ndarray  # (T_color, N) float64
    rf_time: np.ndarray  # (T_rf,) float64
    rf_tc: np.ndarray  # (T_rf, N) float64 — temporal RF kernel


def _to_1d_float(arr: np.ndarray) -> np.ndarray:
    """Flatten a `(N, 1)` column to `(N,)` keeping float64."""
    return arr.astype(np.float64).reshape(-1)


def _to_1d_int(arr: np.ndarray) -> np.ndarray:
    """Flatten a `(N, 1)` integer column to `(N,)` int64."""
    return arr.astype(np.int64).reshape(-1)


def _to_1d_bool(arr: np.ndarray) -> np.ndarray:
    """Cast a `(N, 1)` uint8 selection mask to a flat boolean array."""
    return arr.astype(np.uint8).reshape(-1).astype(np.bool_)


def _extract_struct_column(
    *,
    struct_array: np.ndarray,
    field: str,
) -> list[Any]:
    """Pull one per-cell field from a struct-of-arrays-style MATLAB struct.

    The Dryad release stores cell-of-origin metadata in the (misnamed)
    `noise_time` array, which is a numpy struct with object-typed fields. Each
    object is a `(1,)`/`(1,1)` ndarray; we squeeze it to a Python scalar.
    """
    out: list[Any] = []
    for i in range(struct_array.shape[0]):
        cell = struct_array[i][0][field]
        flat = np.asarray(cell).reshape(-1)
        out.append(flat[0])
    return out


def load_baden_mat(*, mat_path: Path) -> BadenMatData:
    """Load `BadenEtAl_RGCs_2016_v1.mat` into a `BadenMatData` view.

    Reads the MATLAB 5.0 container with `scipy.io.loadmat` (the Dryad file is
    NOT HDF5 v7.3, contrary to the plan's risk note). All per-cell columns are
    flattened to 1-D for ergonomic indexing.
    """
    assert mat_path.exists(), f"mat_path must exist: {mat_path}"
    raw: dict[str, Any] = scipy.io.loadmat(
        str(mat_path),
        squeeze_me=False,
        struct_as_record=True,
    )

    group_idx: np.ndarray = raw["group_idx"].astype(np.int16).reshape(-1)
    n_cells: int = int(group_idx.shape[0])
    assert n_cells == TOTAL_BADEN_CELLS_EXPECTED, (
        f"unexpected cell count: got {n_cells}, expected {TOTAL_BADEN_CELLS_EXPECTED}"
    )

    cluster_idx: np.ndarray = raw["cluster_idx"].astype(np.int16).reshape(-1)
    selected: np.ndarray = _to_1d_bool(arr=raw["sel_idx"])
    cluster_to_group: np.ndarray = raw["c2g"].astype(np.int64).reshape(-1)

    rf_gauss_mean: np.ndarray = raw["rf_gauss_mean"].astype(np.float64)
    rf_gauss_std: np.ndarray = raw["rf_gauss_std"].astype(np.float64)
    assert rf_gauss_mean.shape == (n_cells, 2)
    assert rf_gauss_std.shape == (n_cells, 2)

    # Cell-of-origin: stored in the `noise_time` struct (misnamed in the .mat).
    noise_time: np.ndarray = raw["noise_time"]
    assert noise_time.shape == (n_cells, 1), f"noise_time shape mismatch: {noise_time.shape}"
    recording_date: list[str] = [
        str(x) for x in _extract_struct_column(struct_array=noise_time, field="date")
    ]
    mouse_id: np.ndarray = np.asarray(
        [int(x) for x in _extract_struct_column(struct_array=noise_time, field="mouse_id")],
        dtype=np.int64,
    )
    eye_id: np.ndarray = np.asarray(
        [int(x) for x in _extract_struct_column(struct_array=noise_time, field="eye_id")],
        dtype=np.int64,
    )
    scan_num: np.ndarray = np.asarray(
        [int(x) for x in _extract_struct_column(struct_array=noise_time, field="scan_num")],
        dtype=np.int64,
    )
    stim_num: np.ndarray = np.asarray(
        [int(x) for x in _extract_struct_column(struct_array=noise_time, field="stim_num")],
        dtype=np.int64,
    )
    cell_num: np.ndarray = np.asarray(
        [int(x) for x in _extract_struct_column(struct_array=noise_time, field="cell_num")],
        dtype=np.int64,
    )

    chirp_time: np.ndarray = raw["chirp_time"].astype(np.float64).reshape(-1)
    bar_time: np.ndarray = raw["bar_time"].astype(np.float64).reshape(-1)
    color_time: np.ndarray = raw["color_time"].astype(np.float64).reshape(-1)
    rf_time: np.ndarray = raw["rf_time"].astype(np.float64).reshape(-1)

    chirp_avg: np.ndarray = raw["chirp_avg"].astype(np.float64)
    bar_tc: np.ndarray = raw["bar_tc"].astype(np.float64)
    color_avg: np.ndarray = raw["color_avg"].astype(np.float64)
    rf_tc: np.ndarray = raw["rf_tc"].astype(np.float64)
    bar_byrepeat: np.ndarray = raw["bar_byrepeat"].astype(np.float64)

    assert chirp_avg.shape[1] == n_cells, f"chirp_avg shape: {chirp_avg.shape}"
    assert bar_tc.shape[1] == n_cells, f"bar_tc shape: {bar_tc.shape}"
    assert color_avg.shape[1] == n_cells, f"color_avg shape: {color_avg.shape}"
    assert rf_tc.shape[1] == n_cells, f"rf_tc shape: {rf_tc.shape}"
    assert bar_byrepeat.shape[3] == n_cells, f"bar_byrepeat shape: {bar_byrepeat.shape}"

    return BadenMatData(
        n_cells=n_cells,
        group_idx=group_idx,
        cluster_idx=cluster_idx,
        selected=selected,
        cluster_to_group=cluster_to_group,
        dsi=_to_1d_float(arr=raw["cell_dsi"]),
        osi=_to_1d_float(arr=raw["cell_osi"]),
        dsi_pvalue=_to_1d_float(arr=raw["cell_dp"]),
        osi_pvalue=_to_1d_float(arr=raw["cell_op"]),
        ff_index=_to_1d_float(arr=raw["cell_ff_idx"]),
        on_off_index=_to_1d_float(arr=raw["cell_oo_idx"]),
        chirp_qi=_to_1d_float(arr=raw["chirp_qi"]),
        bar_qi=_to_1d_float(arr=raw["bar_qi"]),
        color_qi=_to_1d_float(arr=raw["color_qi"]),
        rf_qi=_to_1d_float(arr=raw["rf_qi"]),
        chirp_scaling=_to_1d_float(arr=raw["chirp_scaling"]),
        soma_area=_to_1d_float(arr=raw["cell_area"]),
        soma_volume=_to_1d_float(arr=raw["cell_volume"]),
        rf_diameter=_to_1d_float(arr=raw["rf_size"]),
        rf_gauss_mean=rf_gauss_mean,
        rf_gauss_std=rf_gauss_std,
        immuno_chat=_to_1d_float(arr=raw["immuno_chat"]),
        immuno_gad=_to_1d_float(arr=raw["immuno_gad"]),
        immuno_melanopsin=_to_1d_float(arr=raw["immuno_melanopsin"]),
        immuno_smi=_to_1d_float(arr=raw["immuno_smi"]),
        genetics_pv=_to_1d_float(arr=raw["genetics_pv"]),
        genetics_pcp=_to_1d_float(arr=raw["genetics_pcp"]),
        recording_date=recording_date,
        mouse_id=mouse_id,
        eye_id=eye_id,
        scan_num=scan_num,
        stim_num=stim_num,
        cell_num=cell_num,
        chirp_time=chirp_time,
        chirp_avg=chirp_avg,
        bar_time=bar_time,
        bar_tc=bar_tc,
        bar_byrepeat=bar_byrepeat,
        color_time=color_time,
        color_avg=color_avg,
        rf_time=rf_time,
        rf_tc=rf_tc,
    )
