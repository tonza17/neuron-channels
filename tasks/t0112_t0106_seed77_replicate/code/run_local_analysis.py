"""Run all local post-NSGA-II analysis steps in order.

1. Phase C: per-seed anchor classification + biological scorecard.
2. Phase D: cross-seed comparison + plots.
3. metrics.json builder.
4. Phase E + F: predictions assets (3) + answer asset (1).

Run after the per-seed Pareto JSONs have been synced back from the remote
machine.
"""

from __future__ import annotations

from tasks.t0112_t0106_seed77_replicate.code.build_assets import main as build_assets_main
from tasks.t0112_t0106_seed77_replicate.code.cross_seed_analysis import (
    main as cross_seed_main,
)
from tasks.t0112_t0106_seed77_replicate.code.metrics_builder import main as metrics_main
from tasks.t0112_t0106_seed77_replicate.code.per_seed_analysis import main as per_seed_main


def main() -> None:
    print("=== Phase C: per-seed analysis ===")
    per_seed_main()
    print("=== Phase D: cross-seed analysis ===")
    cross_seed_main()
    print("=== metrics.json ===")
    metrics_main()
    print("=== Phase E + F: build assets ===")
    build_assets_main()
    print("=== run_local_analysis done ===")


if __name__ == "__main__":
    main()
