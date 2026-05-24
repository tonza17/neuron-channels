"""Step 6: build each cell via generate_fixed_morphology and dump pt3d (REQ-2, REQ-3, REQ-11).

For every row in `results/data/sampled_cell_manifest.csv`:

1. Build `MorphologyParams` from the 14 morphology parameter columns.
2. Apply the NEURON DLL bypass (no electrical simulation -- pt3d only).
3. Call `generate_fixed_morphology(params=..., morph_seed=int(row.morph_seed))`.
4. Walk every section (soma, primaries, non-primaries, terminals, AIS) and dump:
   * NEURON pt3d (x, y, z, diam) for every point.
   * Python `section_endpoints_xy` start/end coordinates.
   * The midpoint xy via the strict `_section_midpoint_xy_strict` helper.
5. Compute soma-frame summary stats: `soma_pt3d_xy_min`, `soma_pt3d_xy_max`, and
   `soma_frame_offset_um = dist(origin_xy, soma_pt3d_center_xy)`.
6. Serialise the per-cell `CellDump` list to JSON via `dataclasses.asdict`.

Writes `results/data/section_endpoints_dump.json`.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict
from typing import Any

import pandas as pd

# DLL bypass must happen before importing generate_fixed_morphology.
# We do this via the helper module which keeps the imports local.
from tasks.t0120_morph_generator_geometry_audit.code.constants import (
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    MORPH_SEED_COL,
    MORPHOLOGY_PARAM_NAMES,
    SEED_COL,
    SOURCE_TASK_COL,
    STRATUM_TAG_COL,
)
from tasks.t0120_morph_generator_geometry_audit.code.dump_helpers import (
    CellDump,
    SectionDump,
    _dump_one_section,
    _params_from_14d,
    install_neuron_dll_bypass,
)
from tasks.t0120_morph_generator_geometry_audit.code.paths import (
    SAMPLED_CELL_MANIFEST_CSV,
    SECTION_ENDPOINTS_DUMP_JSON,
    ensure_directories,
)

install_neuron_dll_bypass()

# Imports that load NEURON / t0090 generator come AFTER the DLL bypass.
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (  # noqa: E402
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (  # noqa: E402
    generate_fixed_morphology,
)


def _build_cell_id(*, row: pd.Series) -> str:
    return f"{int(row[SEED_COL])}_{int(row[GENERATION_COL])}_{int(row[INDIVIDUAL_IDX_COL])}"


def _make_morphology_params(*, row: pd.Series) -> Any:
    vec: tuple[float, ...] = tuple(float(row[name]) for name in MORPHOLOGY_PARAM_NAMES)
    return _params_from_14d(vec=vec)


def _section_kind(
    *,
    sec: Any,
    primary_set: set[str],
    terminal_set: set[str],
    non_terminal_set: set[str],
    ais_proximal_name: str,
    ais_distal_name: str,
    soma_name: str,
) -> str:
    name: str = str(sec.name())
    if name == soma_name:
        return "soma"
    if name == ais_proximal_name:
        return "ais_proximal"
    if name == ais_distal_name:
        return "ais_distal"
    in_primary: bool = name in primary_set
    in_terminal: bool = name in terminal_set
    in_non_terminal: bool = name in non_terminal_set
    if in_primary and in_terminal:
        # Edge case: a primary that is also terminal (no children). Classify as primary.
        return "primary"
    if in_primary:
        return "primary"
    if in_terminal:
        return "terminal"
    if in_non_terminal:
        return "non_terminal"
    return "unknown"


def _dump_cell(
    *,
    row: pd.Series,
    cell_idx: int,
) -> CellDump:
    cell_id: str = _build_cell_id(row=row)
    params: Any = _make_morphology_params(row=row)
    morph_seed: int = int(row[MORPH_SEED_COL])

    print(
        f"[dump] cell {cell_idx + 1} id={cell_id} stratum={row[STRATUM_TAG_COL]} "
        f"morph_seed={morph_seed} "
        f"soma_offset={float(row['soma_offset_pd_um']):+.2f} "
        f"elong={float(row['field_elongation_pd']):.2f}",
        flush=True,
    )

    result: MorphologyResult = generate_fixed_morphology(params=params, morph_seed=morph_seed)
    h: Any = result.h

    # Sets of section names (with _t90 suffix) per kind.
    primary_set: set[str] = {str(s.name()) for s in result.primary_dends}
    terminal_set: set[str] = {str(s.name()) for s in result.terminal_dends}
    non_terminal_set: set[str] = {str(s.name()) for s in result.non_terminal_dends}
    soma_name: str = str(result.soma.name())
    ais_proximal_name: str = str(result.ais_proximal.name())
    ais_distal_name: str = str(result.ais_distal.name())

    # All sections to dump: soma + all_dends (primaries + non_terminals + terminals are subsets)
    # + AIS.
    all_secs: list[Any] = [result.soma, *result.all_dends, result.ais_proximal, result.ais_distal]

    section_dumps: list[SectionDump] = []
    for sec in all_secs:
        name: str = str(sec.name())
        endpoints: tuple[float, float, float, float] | None = result.section_endpoints_xy.get(
            name.replace("_t90", "")
        )
        python_start_xy: tuple[float, float] | None = None
        python_end_xy: tuple[float, float] | None = None
        if endpoints is not None:
            python_start_xy = (float(endpoints[0]), float(endpoints[1]))
            python_end_xy = (float(endpoints[2]), float(endpoints[3]))
        kind: str = _section_kind(
            sec=sec,
            primary_set=primary_set,
            terminal_set=terminal_set,
            non_terminal_set=non_terminal_set,
            ais_proximal_name=ais_proximal_name,
            ais_distal_name=ais_distal_name,
            soma_name=soma_name,
        )
        sec_dump: SectionDump = _dump_one_section(
            h=h,
            sec=sec,
            section_kind=kind,
            python_start_xy=python_start_xy,
            python_end_xy=python_end_xy,
        )
        section_dumps.append(sec_dump)

    # Soma-frame summary stats (REQ-7).
    soma_dump: SectionDump = next(s for s in section_dumps if s.section_kind == "soma")
    soma_xy_pts: list[tuple[float, float]] = [(p.x, p.y) for p in soma_dump.pt3d]
    if len(soma_xy_pts) == 0:
        soma_xy_min: tuple[float, float] = (math.nan, math.nan)
        soma_xy_max: tuple[float, float] = (math.nan, math.nan)
        soma_center_xy: tuple[float, float] = (math.nan, math.nan)
    else:
        xs: list[float] = [p[0] for p in soma_xy_pts]
        ys: list[float] = [p[1] for p in soma_xy_pts]
        soma_xy_min = (min(xs), min(ys))
        soma_xy_max = (max(xs), max(ys))
        soma_center_xy = (
            (soma_xy_min[0] + soma_xy_max[0]) / 2.0,
            (soma_xy_min[1] + soma_xy_max[1]) / 2.0,
        )
    origin_xy: tuple[float, float] = (
        float(result.origin_xy[0]),
        float(result.origin_xy[1]),
    )
    soma_frame_offset_um: float = float(
        math.sqrt((origin_xy[0] - soma_center_xy[0]) ** 2 + (origin_xy[1] - soma_center_xy[1]) ** 2)
    )

    asymmetry_params: dict[str, float] = {
        "soma_offset_pd_um": float(row["soma_offset_pd_um"]),
        "field_elongation_pd": float(row["field_elongation_pd"]),
        "branch_density_gradient_pd": float(row["branch_density_gradient_pd"]),
        "primary_branch_pd_concentration": float(row["primary_branch_pd_concentration"]),
        "soma_diameter_um": float(row["soma_diameter_um"]),
    }

    n_primary: int = len(result.primary_dends)
    n_non_primary: int = len(result.non_terminal_dends) + len(result.terminal_dends) - n_primary
    # Above subtracts primaries that may also appear in terminal/non_terminal sets;
    # but the cleaner count of non-primary dendrites is just total dends minus primaries.
    n_non_primary = len(result.all_dends) - n_primary

    dump: CellDump = CellDump(
        cell_id=cell_id,
        source_task=str(row[SOURCE_TASK_COL]),
        seed=int(row[SEED_COL]),
        generation=int(row[GENERATION_COL]),
        individual_idx=int(row[INDIVIDUAL_IDX_COL]),
        stratum_tag=str(row[STRATUM_TAG_COL]),
        asymmetry_params=asymmetry_params,
        origin_xy=origin_xy,
        soma_pt3d_xy_min=soma_xy_min,
        soma_pt3d_xy_max=soma_xy_max,
        soma_frame_offset_um=soma_frame_offset_um,
        n_sections=len(section_dumps),
        n_primary=n_primary,
        n_non_primary_dends=n_non_primary,
        n_dendrites=len(result.all_dends),
        sections=section_dumps,
        connectivity={
            child.replace("_t90", ""): parent.replace("_t90", "")
            for child, parent in result.connectivity.items()
        },
    )

    print(
        f"[dump]   n_sections={dump.n_sections} n_primary={n_primary} "
        f"n_dends={dump.n_dendrites} soma_n3d={len(soma_dump.pt3d)} "
        f"origin_xy=({origin_xy[0]:+.3f}, {origin_xy[1]:+.3f}) "
        f"soma_frame_offset_um={soma_frame_offset_um:.3f}",
        flush=True,
    )
    return dump


def _cell_dump_to_jsonable(*, dump: CellDump) -> dict[str, Any]:
    """Use dataclasses.asdict but coerce tuples to lists for JSON-friendliness."""
    raw: dict[str, Any] = asdict(dump)
    # asdict converts tuples to tuples (which json.dumps handles as lists already),
    # so no further conversion is strictly necessary. We do nothing here.
    return raw


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Dump per-section pt3d + Python endpoints for every sampled cell.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="If set, process only the first N cells (smoke-test mode).",
    )
    args = parser.parse_args()

    ensure_directories()
    manifest: pd.DataFrame = pd.read_csv(SAMPLED_CELL_MANIFEST_CSV)
    n_total: int = len(manifest)
    if args.limit is not None:
        manifest = manifest.head(args.limit)
        print(f"[dump] SMOKE TEST: limiting to {len(manifest)} of {n_total} cells", flush=True)
    else:
        print(f"[dump] processing all {n_total} cells", flush=True)

    dumps: list[CellDump] = []
    for cell_idx, (_, row) in enumerate(manifest.iterrows()):
        dump: CellDump = _dump_cell(row=row, cell_idx=cell_idx)
        dumps.append(dump)

    payload: list[dict[str, Any]] = [_cell_dump_to_jsonable(dump=d) for d in dumps]

    if args.limit is None:
        SECTION_ENDPOINTS_DUMP_JSON.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )
        print(f"[dump] wrote {SECTION_ENDPOINTS_DUMP_JSON}", flush=True)
        print(
            f"[dump] file size = {SECTION_ENDPOINTS_DUMP_JSON.stat().st_size / 1024:.1f} KB",
            flush=True,
        )
    else:
        print(
            f"[dump] SMOKE TEST: not writing JSON file. Processed {len(dumps)} cells.",
            flush=True,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
