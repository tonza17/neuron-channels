"""Phase B + C orchestrator: classify -> cluster -> plot -> score -> answer asset.

Run after Phase A completes and replication_results.json is finalized.

CLI: uv run python -m tasks.t0086_robustness_cluster_bio_comparison.code.run_phase_b
"""

from __future__ import annotations

from tasks.t0086_robustness_cluster_bio_comparison.code import (
    biological_priors,
    biological_scorecard,
    build_metrics,
    classify_cells,
    cluster_analysis,
    plot_phase_b,
    write_answer_asset,
)


def main() -> None:
    print("[run_phase_b] step 1: classify cells")
    classify_cells.main()
    print("[run_phase_b] step 2: cluster analysis")
    cluster_analysis.main()
    print("[run_phase_b] step 3: phase B plots")
    plot_phase_b.main()
    print("[run_phase_b] step 4: biological priors")
    biological_priors.main()
    print("[run_phase_b] step 5: biological scorecard + heatmap")
    biological_scorecard.main()
    print("[run_phase_b] step 6: write answer asset")
    write_answer_asset.main()
    print("[run_phase_b] step 7: build metrics.json")
    build_metrics.main()
    print("[run_phase_b] all done")


if __name__ == "__main__":
    main()
