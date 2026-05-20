"""Build `results/metrics.json` for the t0099 task.

Uses the explicit multi-variant format because we have 3 random-init seeds
(plus a t0091 reference variant). Reports the registered metric
``direction_selectivity_index`` (mean DSI vector-sum over each Pareto front)
because that is the only DSI-like metric registered in `meta/metrics/`.
"""

from __future__ import annotations

import json
from pathlib import Path

from tasks.t0113_t0106_seed2247_replicate.code.constants import T0104_SEEDS
from tasks.t0113_t0106_seed2247_replicate.code.paths import (
    RESULTS_DIR,
    T0091_PARETO_FRONT_JSON,
    ensure_directories,
    pareto_front_json,
)


def _mean_dsi(*, pareto_path: Path) -> tuple[float, int]:
    if not pareto_path.exists():
        return (0.0, 0)
    payload = json.loads(pareto_path.read_text(encoding="utf-8"))
    cells = payload.get("cells", [])
    if len(cells) == 0:
        return (0.0, 0)
    s = sum(float(c.get("dsi_vector_sum", 0.0)) for c in cells)
    return (s / len(cells), len(cells))


def build_metrics() -> dict[str, object]:
    variants: list[dict[str, object]] = []
    for seed in T0104_SEEDS:
        mean_dsi, n_cells = _mean_dsi(pareto_path=pareto_front_json(seed=seed))
        variants.append(
            {
                "variant_id": f"random-init-seed{seed}",
                "label": f"Random-init seed {seed}",
                "dimensions": {
                    "task_seed": int(seed),
                    "init_method": "lhs_random",
                    "n_cells": int(n_cells),
                },
                "metrics": {
                    "direction_selectivity_index": float(mean_dsi),
                },
            }
        )

    # t0091 reference variant for cross-task comparison.
    mean_dsi_91, n_cells_91 = _mean_dsi(pareto_path=T0091_PARETO_FRONT_JSON)
    variants.append(
        {
            "variant_id": "t0091-warmstart-reference",
            "label": "t0091 warm-start reference",
            "dimensions": {
                "task_seed": -1,
                "init_method": "5_anchor_warmstart",
                "n_cells": int(n_cells_91),
            },
            "metrics": {
                "direction_selectivity_index": float(mean_dsi_91),
            },
        }
    )
    return {"variants": variants}


def main() -> None:
    ensure_directories()
    payload = build_metrics()
    out = RESULTS_DIR / "metrics.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[metrics_builder] wrote {out} with {len(payload['variants'])} variants")


if __name__ == "__main__":
    main()
