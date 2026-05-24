"""End-to-end orchestrator for the canonical 5-seed substrate-rate report.

Runs the pipeline in dependency order: per-seed summaries (with raw-data
asserts), pooled LEGIT parquet, convention-drift CSV, per-seed convergence
CSV, 5-seed stats CSV (with mean / SE asserts), literature comparison CSV,
three charts, and the answer asset.
"""

from __future__ import annotations

from pathlib import Path

from tasks.t0121_5seed_substrate_rate_canonical_report.code.answer_asset import (
    write_answer_asset,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.charts import (
    chart_dsi_pd_scatter,
    chart_hv_trajectory_overlay,
    chart_per_seed_acceptance_bar,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.csv_writers import (
    build_pooled_legit_cells,
    write_convention_drift,
    write_literature_comparison,
    write_per_seed_convergence,
    write_per_seed_substrate_rate,
    write_pooled_legit_cells,
    write_substrate_stats,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.loaders import (
    load_hv,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.paths import (
    OUT_DATA_DIR,
    OUT_IMAGES_DIR,
    T0106_EVALS,
    T0106_HV,
    T0112_EVALS,
    T0112_HV,
    T0113_EVALS,
    T0113_HV,
    T0114_EVALS,
    T0114_HV,
    T0115_EVALS,
    T0115_HV,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.per_seed import (
    PerSeedSummary,
    summarize_seed,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.seed_metadata import (
    ALL_SEED_KEYS,
)
from tasks.t0121_5seed_substrate_rate_canonical_report.code.stats import (
    compute_substrate_stats,
)

EVAL_PATHS: dict[str, Path] = {
    "t0106_seed44": T0106_EVALS,
    "t0112_seed77": T0112_EVALS,
    "t0113_seed2247": T0113_EVALS,
    "t0114_seed7755": T0114_EVALS,
    "t0115_seed9354": T0115_EVALS,
}

HV_PATHS: dict[str, Path] = {
    "t0106_seed44": T0106_HV,
    "t0112_seed77": T0112_HV,
    "t0113_seed2247": T0113_HV,
    "t0114_seed7755": T0114_HV,
    "t0115_seed9354": T0115_HV,
}


def main() -> None:
    OUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # --- Step 5: per-seed acceptance summaries (with raw-anchor asserts) ---
    summaries: dict[str, PerSeedSummary] = {}
    for key in ALL_SEED_KEYS:
        print(f"[load] {key} from {EVAL_PATHS[key]}", flush=True)
        s = summarize_seed(
            seed_key=key,
            eval_path=EVAL_PATHS[key],
            hv_path=HV_PATHS[key],
        )
        summaries[key] = s
        print(
            f"{key} {s.task_id} {s.n_total_evals} evals "
            f"{s.n_legit_unique} LEGIT {s.acceptance_rate_pct:.4f}%",
            flush=True,
        )

    # --- Step 8: 5-seed statistics (with mean / SE asserts) ---
    stats = compute_substrate_stats(summaries=summaries)
    print(
        f"5-seed mean = {stats.mean_pct:.2f} +/- SE {stats.sample_se_pct:.2f}; "
        f"normal-approx 95% CI = "
        f"({stats.normal_approx_ci_lo_pct:.2f}, {stats.normal_approx_ci_hi_pct:.2f}); "
        f"bootstrap 95% CI = "
        f"({stats.bootstrap_ci_lo_pct:.2f}, {stats.bootstrap_ci_hi_pct:.2f}); "
        f"n_seeds > Hay = {stats.n_seeds_above_hay_envelope}",
        flush=True,
    )

    # --- Step 5 CSV: per-seed substrate rate ---
    p_per_seed = write_per_seed_substrate_rate(summaries=summaries)
    print(f"wrote {p_per_seed}", flush=True)

    # --- Step 6: pooled LEGIT joint-pass parquet (with row-count assert) ---
    pooled_df = build_pooled_legit_cells(eval_paths=EVAL_PATHS)
    p_parquet = write_pooled_legit_cells(df=pooled_df)
    print(f"wrote {p_parquet}: {len(pooled_df)} rows", flush=True)

    # --- Step 7: convention drift ---
    p_drift = write_convention_drift(summaries=summaries)
    print(f"wrote {p_drift}", flush=True)

    # --- Step 10: per-seed convergence ---
    p_conv = write_per_seed_convergence(summaries=summaries)
    print(f"wrote {p_conv}", flush=True)

    # --- Step 8 CSV: 5-seed stats ---
    p_stats = write_substrate_stats(stats=stats)
    print(f"wrote {p_stats}", flush=True)

    # --- Step 9: literature comparison ---
    p_lit = write_literature_comparison(stats=stats)
    print(f"wrote {p_lit}", flush=True)

    # --- Step 11: three charts ---
    p_bar = chart_per_seed_acceptance_bar(summaries=summaries, stats=stats)
    print(f"wrote {p_bar}", flush=True)
    hv_traces: dict[str, list[dict[str, object]]] = {
        key: load_hv(path=HV_PATHS[key]) for key in ALL_SEED_KEYS
    }
    p_hv = chart_hv_trajectory_overlay(hv_traces=hv_traces)
    print(f"wrote {p_hv}", flush=True)
    p_scatter = chart_dsi_pd_scatter(pooled_df=pooled_df)
    print(f"wrote {p_scatter}", flush=True)

    # --- Step 12: answer asset ---
    p_answer = write_answer_asset(summaries=summaries, stats=stats)
    print(f"wrote answer asset at {p_answer}", flush=True)

    print(
        "wrote 5 CSVs, 1 parquet, 3 charts, 1 answer asset to "
        "tasks/t0121_5seed_substrate_rate_canonical_report/",
        flush=True,
    )


if __name__ == "__main__":
    main()
