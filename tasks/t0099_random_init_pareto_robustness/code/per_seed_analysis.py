"""Phase C: per-seed post-processing.

For each task seed:

1. Load the per-seed Pareto front (assumed already extracted by NSGA-II).
2. Classify each cell to its nearest t0091 anchor.
3. Score each cell against the 13 biological priors (worst-case aggregation).
4. Compute strict joint-pass count (DSI >= 0.5, PD-rate >= 30 Hz, robust >= 0.7).
"""

from __future__ import annotations

import json

from tasks.t0099_random_init_pareto_robustness.code.anchor_classifier import (
    main_for_seed as classify_anchors,
)
from tasks.t0099_random_init_pareto_robustness.code.biological_priors import (
    main as build_priors_file,
)
from tasks.t0099_random_init_pareto_robustness.code.biological_scorecard import (
    main_for_seed as score_priors,
)
from tasks.t0099_random_init_pareto_robustness.code.constants import T0099_SEEDS
from tasks.t0099_random_init_pareto_robustness.code.paths import (
    biological_priors_json,
    ensure_directories,
    pareto_front_json,
)

STRICT_DSI_THRESHOLD: float = 0.5
STRICT_PD_RATE_HZ_THRESHOLD: float = 30.0
STRICT_ROBUSTNESS_THRESHOLD: float = 0.7


def strict_joint_pass_count_for_seed(*, seed: int) -> dict[str, object]:
    pareto_path = pareto_front_json(seed=seed)
    if not pareto_path.exists():
        return {
            "seed": seed,
            "pareto_path": str(pareto_path),
            "exists": False,
            "n_cells_total": 0,
            "n_strict_joint_pass": 0,
        }
    pareto = json.loads(pareto_path.read_text(encoding="utf-8"))
    cells = pareto["cells"]
    n_pass = 0
    pass_cell_ids: list[int] = []
    for cell in cells:
        dsi = float(cell.get("dsi_vector_sum", 0.0))
        pd = float(cell.get("pd_rate_hz", 0.0))
        rob = float(cell.get("robustness", 0.0))
        if (
            dsi >= STRICT_DSI_THRESHOLD
            and pd >= STRICT_PD_RATE_HZ_THRESHOLD
            and rob >= STRICT_ROBUSTNESS_THRESHOLD
        ):
            n_pass += 1
            pass_cell_ids.append(int(cell.get("cell_id", -1)))
    return {
        "seed": seed,
        "pareto_path": str(pareto_path),
        "exists": True,
        "n_cells_total": len(cells),
        "n_strict_joint_pass": n_pass,
        "strict_pass_cell_ids": pass_cell_ids,
        "thresholds": {
            "dsi_min": STRICT_DSI_THRESHOLD,
            "pd_rate_hz_min": STRICT_PD_RATE_HZ_THRESHOLD,
            "robustness_min": STRICT_ROBUSTNESS_THRESHOLD,
        },
    }


def run_for_seed(*, seed: int) -> dict[str, object]:
    """Run anchor classification + biological scoring for one seed."""
    pareto_path = pareto_front_json(seed=seed)
    if not pareto_path.exists():
        print(f"[per_seed_analysis] seed={seed} pareto file missing; skipping")
        return {"seed": seed, "skipped": True, "reason": "pareto_front_missing"}
    if not biological_priors_json().exists():
        build_priors_file()
    classify_anchors(seed=seed)
    score_priors(seed=seed)
    strict = strict_joint_pass_count_for_seed(seed=seed)
    print(f"[per_seed_analysis] seed={seed} strict_joint_pass={strict['n_strict_joint_pass']}")
    return {"seed": seed, "skipped": False, "strict": strict}


def main() -> None:
    ensure_directories()
    if not biological_priors_json().exists():
        build_priors_file()
    for seed in T0099_SEEDS:
        run_for_seed(seed=int(seed))


if __name__ == "__main__":
    main()
