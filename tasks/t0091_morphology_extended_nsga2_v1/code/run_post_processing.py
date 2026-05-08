"""Run all t0091 post-processing in order.

After the NSGA-II finishes (success or watchdog trip), this script:
1. Extracts the Pareto front + length-vs-DSI test (REQ-10, REQ-15).
2. Generates the biological priors JSON (REQ-11, REQ-22).
3. Scores every Pareto cell against priors (REQ-11, REQ-12).
4. Runs the anchor-tracking analysis with bootstrap (REQ-13, REQ-14).
5. Builds predictions + answer assets and metrics.json (REQ-16, REQ-17).
"""

from __future__ import annotations


def main() -> None:
    print("[post_processing] step 1/5: Pareto extraction + length vs DSI")
    from tasks.t0091_morphology_extended_nsga2_v1.code import pareto_analysis

    pareto_analysis.main()

    print("[post_processing] step 2/5: biological priors")
    from tasks.t0091_morphology_extended_nsga2_v1.code import biological_priors

    biological_priors.main()

    print("[post_processing] step 3/5: biological scorecard")
    from tasks.t0091_morphology_extended_nsga2_v1.code import biological_scorecard

    biological_scorecard.main()

    print("[post_processing] step 4/5: anchor tracking")
    from tasks.t0091_morphology_extended_nsga2_v1.code import anchor_tracking

    anchor_tracking.main()

    print("[post_processing] step 5/5: build assets + metrics")
    from tasks.t0091_morphology_extended_nsga2_v1.code import build_assets

    build_assets.main()

    print("[post_processing] DONE")


if __name__ == "__main__":
    main()
