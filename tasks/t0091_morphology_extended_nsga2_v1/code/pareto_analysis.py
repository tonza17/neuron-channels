"""Pareto-front extraction + length-vs-DSI sanity check (REQ-10, REQ-15).

If the NSGA-II driver wrote `pareto_front.json` already, this module's main
function is a no-op for extraction and only runs the length-vs-DSI Spearman
correlation. If the file is missing, we extract from `all_evaluations.json`.
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from tasks.t0091_morphology_extended_nsga2_v1.code.anchor_tracking import (
    _effective_dendritic_length_um,
)
from tasks.t0091_morphology_extended_nsga2_v1.code.paths import (
    ALL_EVALUATIONS_JSON,
    DSI_VS_LENGTH_PNG,
    LENGTH_DSI_CORRELATION_JSON,
    PARETO_FRONT_JSON,
    ensure_directories,
)


def _spearman(*, x: NDArray[np.float64], y: NDArray[np.float64]) -> float:
    """Simple Spearman rank correlation."""
    if len(x) < 3 or len(y) < 3:
        return float("nan")
    rx = np.argsort(np.argsort(x))
    ry = np.argsort(np.argsort(y))
    rx_mean = float(np.mean(rx))
    ry_mean = float(np.mean(ry))
    num = float(np.sum((rx - rx_mean) * (ry - ry_mean)))
    den = float(np.sqrt(np.sum((rx - rx_mean) ** 2) * np.sum((ry - ry_mean) ** 2)))
    if den == 0.0:
        return 0.0
    return num / den


def _extract_pareto_from_all_evaluations() -> dict[str, object]:
    """Compute non-dominated front from `all_evaluations.json`."""
    payload = json.loads(ALL_EVALUATIONS_JSON.read_text(encoding="utf-8"))
    evaluations: list[dict[str, object]] = list(payload["evaluations"])
    if len(evaluations) == 0:
        return {"n_total": 0, "cells": []}
    F = np.array([e["objective_F_minimised"] for e in evaluations], dtype=np.float64)
    nds = NonDominatedSorting()
    fronts = nds.do(F, only_non_dominated_front=True)
    cells_out: list[dict[str, object]] = []
    for i, idx in enumerate(fronts):
        e = evaluations[int(idx)]
        cells_out.append(
            {
                "cell_id": i,
                "vector_68d": list(e["vector_68d"]),
                "params": list(e["vector_68d"][:54]),
                "morphology_vector_14d": list(e["vector_68d"][54:]),
                "objective_F_minimised": list(e["objective_F_minimised"]),
                "dsi_vector_sum": float(e["dsi_vector_sum"]),
                "pd_rate_hz": float(e["pd_rate_hz"]),
                "robustness": float(e["robustness"]),
                "source_generation": int(e["generation"]),
            }
        )
    return {"n_total": len(cells_out), "cells": cells_out}


def main() -> None:
    ensure_directories()
    if PARETO_FRONT_JSON.exists():
        pareto_payload = json.loads(PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    else:
        pareto_payload = _extract_pareto_from_all_evaluations()
        PARETO_FRONT_JSON.write_text(json.dumps(pareto_payload, indent=2), encoding="utf-8")
        print(
            f"[pareto_analysis] extracted {pareto_payload['n_total']} cells "
            f"from all_evaluations.json"
        )

    cells = pareto_payload["cells"]
    if len(cells) == 0:
        print("[pareto_analysis] no Pareto cells; skipping length-vs-DSI plot")
        return

    dsi: list[float] = []
    length: list[float] = []
    for c in cells:
        vec_68d = np.array(c.get("vector_68d") or c.get("params"), dtype=np.float64)
        if len(vec_68d) < 68:
            continue
        dsi.append(float(c.get("dsi_vector_sum", 0.0)))
        length.append(float(_effective_dendritic_length_um(vector_68d=vec_68d)))

    dsi_arr = np.asarray(dsi, dtype=np.float64)
    len_arr = np.asarray(length, dtype=np.float64)
    rho = _spearman(x=len_arr, y=dsi_arr)

    LENGTH_DSI_CORRELATION_JSON.write_text(
        json.dumps(
            {
                "n_cells": len(dsi),
                "spearman_rho": float(rho),
                "dsi": dsi,
                "effective_dendritic_length_um": length,
                "interpretation": (
                    "positive rho indicates Hausselt 2007 length-mechanism is operative; "
                    "near-zero or negative rho indicates DSI is driven by the v3 channel "
                    "mechanism rather than morphology length."
                ),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(len_arr, dsi_arr, alpha=0.7)
    ax.set_xlabel("Effective dendritic length (um)")
    ax.set_ylabel("DSI (vector sum)")
    ax.set_title(f"Hausselt length vs DSI (rho={rho:.3f}, n={len(dsi)})")
    fig.tight_layout()
    fig.savefig(DSI_VS_LENGTH_PNG, dpi=150)
    plt.close(fig)

    print(f"[pareto_analysis] spearman={rho:.4f}; n={len(cells)}; wrote {DSI_VS_LENGTH_PNG}")


if __name__ == "__main__":
    main()
