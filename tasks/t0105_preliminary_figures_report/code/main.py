"""Run the full t0105 figure pack: 7 figures (10 PNGs) + deck + metrics.json.

Steps (matching plan/plan.md Milestone B+C):
1. fig 1: HH equations
2. fig 2: conductance tables (Bed A + Bed B)
3. fig 3: morphology PNGs (copy from t0070)
4. fig 4: two-point polar synaptic (Bed A + Bed B)
5. fig 5: three-mode overlays (2x2 bed x direction)
6. fig 6: channel-effect-on-DSI panel
7. fig 7: top-5 Pareto cells (3-obj NSGA-II)
8. build slide deck
9. write metrics.json (5 variants, one per selected Pareto cell)
10. sanity check all PNGs exist and are at least MIN_PNG_BYTES.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tasks.t0105_preliminary_figures_report.code import (
    build_slides,
    render_channel_effect,
    render_conductance_table,
    render_hh_equations,
    render_morphology,
    render_pareto_top5,
    render_polar_synaptic,
    render_three_mode_overlays,
)
from tasks.t0105_preliminary_figures_report.code import constants as cst
from tasks.t0105_preliminary_figures_report.code import paths as pth
from tasks.t0105_preliminary_figures_report.code.render_pareto_top5 import CellRecord


def _all_output_pngs() -> list[Path]:
    return [
        pth.FIG01_HH_EQUATIONS_PNG,
        pth.FIG02_TABLE_BED_A_PNG,
        pth.FIG02_TABLE_BED_B_PNG,
        pth.FIG03_BED_A_MORPH_PNG,
        pth.FIG03_BED_B_MORPH_PNG,
        pth.FIG04_BED_A_POLAR_PNG,
        pth.FIG04_BED_B_POLAR_PNG,
        pth.FIG05_THREE_MODE_PNG,
        pth.FIG06_CHANNEL_EFFECT_PNG,
        pth.FIG07_TOP5_PARETO_PNG,
    ]


def _sanity_check_pngs() -> None:
    failures: list[str] = []
    for png in _all_output_pngs():
        if not png.exists():
            failures.append(f"MISSING: {png}")
            continue
        size: int = png.stat().st_size
        if size < cst.MIN_PNG_BYTES:
            failures.append(f"TOO_SMALL ({size} bytes): {png}")
    if len(failures) > 0:
        raise RuntimeError("PNG sanity check failed:\n" + "\n".join(failures))
    print(f"[t0105] sanity check OK -- {len(_all_output_pngs())} PNGs >= {cst.MIN_PNG_BYTES} bytes")


def _write_metrics_json(*, top_cells: list[CellRecord]) -> None:
    assert len(top_cells) == cst.TOP_K_PARETO_CELLS, (
        f"expected {cst.TOP_K_PARETO_CELLS} top cells, got {len(top_cells)}"
    )
    variants: list[dict[str, Any]] = []
    for cell in top_cells:
        variants.append(
            {
                "variant_id": f"pareto-cell-{cell.cell_id}-seed{cell.seed}",
                "label": (
                    f"t0102 Pareto cell {cell.cell_id} (seed {cell.seed}) -- "
                    f"DSI={cell.dsi:.3f}, PD={cell.pd_rate_hz:.2f}Hz"
                ),
                "dimensions": {
                    "source_task": "t0102_seedscale_n4_gen20",
                    "pareto_seed": cell.seed,
                    "cell_id": cell.cell_id,
                    "pd_rate_hz": cell.pd_rate_hz,
                    "robustness": cell.robustness,
                },
                "metrics": {
                    cst.METRIC_DSI: cell.dsi,
                },
            }
        )
    pth.METRICS_JSON.write_text(
        data=json.dumps(obj={"variants": variants}, indent=2),
        encoding="utf-8",
    )
    print(f"[t0105] wrote {pth.METRICS_JSON} ({len(variants)} variants)")


def main() -> None:
    print("[t0105] ==== rendering figure 1: HH equations ====")
    render_hh_equations.main()
    print("[t0105] ==== rendering figure 2: conductance tables ====")
    render_conductance_table.main()
    print("[t0105] ==== rendering figure 3: morphology PNGs (copy) ====")
    render_morphology.main()
    print("[t0105] ==== rendering figure 4: two-point polar synaptic ====")
    render_polar_synaptic.main()
    print("[t0105] ==== rendering figure 5: three-mode overlays ====")
    render_three_mode_overlays.main()
    print("[t0105] ==== rendering figure 6: channel-effect-on-DSI ====")
    render_channel_effect.main()
    print("[t0105] ==== rendering figure 7: top-5 Pareto cells ====")
    top_cells: list[CellRecord] = render_pareto_top5.main()
    print("[t0105] ==== sanity check ====")
    _sanity_check_pngs()
    print("[t0105] ==== writing metrics.json ====")
    _write_metrics_json(top_cells=top_cells)
    print("[t0105] ==== building slide deck ====")
    build_slides.main()
    print("[t0105] ==== DONE ====")


if __name__ == "__main__":
    main()
