"""Step 20: compute project metrics + diversity summary chart.

Reads:
* ``data/verification_summary.json`` (60 morphologies)
* ``data/bedb_reproducibility.json`` (5 cells)

Writes:
* ``results/metrics.json`` (multi-variant: different_set, similar_set, bedb_repro_5)
* ``results/images/diversity_summary.png`` (DSI + PD-rate histograms)
"""

from __future__ import annotations

import json
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    StabilityKind,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_BEDB_REPRO_JSON,
    DATA_VERIFICATION_JSON,
    RESULTS_IMAGES_DIR,
    RESULTS_METRICS_JSON,
    ensure_directories,
)


def _safe_floats(*, xs: list[Any]) -> list[float]:
    return [float(x) for x in xs if x is not None and isinstance(x, int | float) and np.isfinite(x)]


def _summarise_population(
    *,
    records: list[dict[str, Any]],
    population: str,
) -> dict[str, Any]:
    pop_records = [r for r in records if r.get("population") == population]
    stable = [r for r in pop_records if r.get("stability_flag") == StabilityKind.STABLE.value]
    dsis = _safe_floats(xs=[r.get("dsi") for r in stable])
    pd_rates = _safe_floats(xs=[r.get("pd_rate_hz") for r in stable])
    return {
        "n_total": len(pop_records),
        "n_stable": len(stable),
        "n_unstable": len(pop_records) - len(stable),
        "dsi_mean": float(np.mean(dsis)) if len(dsis) > 0 else None,
        "dsi_median": float(np.median(dsis)) if len(dsis) > 0 else None,
        "dsi_min": float(np.min(dsis)) if len(dsis) > 0 else None,
        "dsi_max": float(np.max(dsis)) if len(dsis) > 0 else None,
        "pd_rate_mean": float(np.mean(pd_rates)) if len(pd_rates) > 0 else None,
        "pd_rate_median": float(np.median(pd_rates)) if len(pd_rates) > 0 else None,
        "dsis": dsis,
        "pd_rates": pd_rates,
    }


def _build_metrics_variant(
    *,
    variant_id: str,
    label: str,
    population_summary: dict[str, Any],
    extra_metrics: dict[str, float | None] | None = None,
) -> dict[str, Any]:
    metrics: dict[str, float | int | None] = {}
    metrics["direction_selectivity_index"] = population_summary.get("dsi_median")
    metrics["n_stable_morphologies"] = population_summary["n_stable"]
    metrics["n_total_morphologies"] = population_summary["n_total"]
    if extra_metrics is not None:
        for k, v in extra_metrics.items():
            metrics[k] = v
    return {
        "variant_id": variant_id,
        "label": label,
        "dimensions": {
            "morphology_population": variant_id,
        },
        "metrics": metrics,
    }


def _bedb_metrics(*, repro_records: list[dict[str, Any]]) -> dict[str, Any]:
    proc_dsis = [r["procedural_dsi"] for r in repro_records if r.get("procedural_dsi") is not None]
    pd_deltas = _safe_floats(xs=[r.get("pd_rate_delta_pct") for r in repro_records])
    dsi_deltas = _safe_floats(xs=[r.get("dsi_delta_pct") for r in repro_records])
    n_pass = sum(1 for r in repro_records if r.get("pass_10pct"))
    summary: dict[str, Any] = {
        "n_total": len(repro_records),
        "n_pass_10pct": n_pass,
        "dsi_delta_mean_pct": float(np.mean(dsi_deltas)) if len(dsi_deltas) > 0 else None,
        "dsi_delta_max_abs_pct": float(np.max(np.abs(dsi_deltas))) if len(dsi_deltas) > 0 else None,
        "pd_rate_delta_mean_pct": float(np.mean(pd_deltas)) if len(pd_deltas) > 0 else None,
        "pd_rate_delta_max_abs_pct": (
            float(np.max(np.abs(pd_deltas))) if len(pd_deltas) > 0 else None
        ),
        "procedural_dsi_median": float(np.median(proc_dsis)) if len(proc_dsis) > 0 else None,
    }
    return summary


def _plot_diversity_summary(
    *,
    different_summary: dict[str, Any],
    similar_summary: dict[str, Any],
    output_png: str,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.5))

    # Panel 1: DSI histogram per set.
    bins = np.linspace(-1.0, 1.0, 21)
    diff_dsis = different_summary["dsis"]
    sim_dsis = similar_summary["dsis"]
    if len(diff_dsis) > 0:
        axes[0].hist(diff_dsis, bins=bins, alpha=0.55, label="different", color="#0072B2")
    if len(sim_dsis) > 0:
        axes[0].hist(sim_dsis, bins=bins, alpha=0.55, label="similar", color="#D55E00")
    axes[0].set_xlabel("DSI")
    axes[0].set_ylabel("count")
    axes[0].set_title("DSI distribution per population")
    axes[0].legend(loc="best")
    axes[0].grid(True, alpha=0.3)

    # Panel 2: PD-rate histogram per set.
    diff_rates = different_summary["pd_rates"]
    sim_rates = similar_summary["pd_rates"]
    if len(diff_rates) > 0 or len(sim_rates) > 0:
        max_rate = max(
            max(diff_rates, default=0.0),
            max(sim_rates, default=0.0),
        )
        bins2 = np.linspace(0.0, max(max_rate, 1.0) + 1.0, 21)
        if len(diff_rates) > 0:
            axes[1].hist(diff_rates, bins=bins2, alpha=0.55, label="different", color="#0072B2")
        if len(sim_rates) > 0:
            axes[1].hist(sim_rates, bins=bins2, alpha=0.55, label="similar", color="#D55E00")
    axes[1].set_xlabel("PD firing rate (Hz)")
    axes[1].set_ylabel("count")
    axes[1].set_title("PD firing-rate distribution per population")
    axes[1].legend(loc="best")
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ensure_directories()

    if not DATA_VERIFICATION_JSON.exists():
        raise FileNotFoundError(f"verification summary not found at {DATA_VERIFICATION_JSON}")
    records = json.loads(DATA_VERIFICATION_JSON.read_text())
    different = _summarise_population(records=records, population="different")
    similar = _summarise_population(records=records, population="similar")
    print(
        f"different: {different['n_stable']}/{different['n_total']} stable, "
        f"DSI median={different['dsi_median']}, mean={different['dsi_mean']}"
    )
    print(
        f"similar:   {similar['n_stable']}/{similar['n_total']} stable, "
        f"DSI median={similar['dsi_median']}, mean={similar['dsi_mean']}"
    )

    repro: list[dict[str, Any]] = []
    bedb_summary: dict[str, Any] = {}
    if DATA_BEDB_REPRO_JSON.exists():
        repro = json.loads(DATA_BEDB_REPRO_JSON.read_text())
        bedb_summary = _bedb_metrics(repro_records=repro)
        print(
            f"bedb_repro: {bedb_summary['n_pass_10pct']}/{bedb_summary['n_total']} pass within 10% "
            f"on both DSI and PD-rate"
        )
    else:
        print("WARNING: bedb_reproducibility.json not found; skipping bedb metrics")

    variants: list[dict[str, Any]] = [
        _build_metrics_variant(
            variant_id="different_set",
            label="30 LHS-sampled very-different morphologies (Phase B)",
            population_summary=different,
        ),
        _build_metrics_variant(
            variant_id="similar_set",
            label="30 +/-5 percent perturbed very-similar morphologies (Phase C)",
            population_summary=similar,
        ),
    ]
    if len(repro) > 0:
        variants.append(
            {
                "variant_id": "bedb_repro_5",
                "label": "5 t0083 Pareto cells re-evaluated at the BedB-equivalent procedural cell",
                "dimensions": {"morphology_population": "bedb_repro_5"},
                "metrics": {
                    "direction_selectivity_index": bedb_summary.get("procedural_dsi_median"),
                    "n_pass_10pct": bedb_summary.get("n_pass_10pct"),
                    "n_total": bedb_summary.get("n_total"),
                    "dsi_delta_max_abs_pct": bedb_summary.get("dsi_delta_max_abs_pct"),
                    "pd_rate_delta_max_abs_pct": bedb_summary.get("pd_rate_delta_max_abs_pct"),
                },
            }
        )

    metrics_doc = {
        "spec_version": "1",
        "task_id": "t0090_morphology_generator_diversity_test",
        "format": "explicit_variant",
        "variants": variants,
    }
    RESULTS_METRICS_JSON.write_text(json.dumps(metrics_doc, indent=2))
    print(f"wrote {RESULTS_METRICS_JSON}")

    out_png = RESULTS_IMAGES_DIR / "diversity_summary.png"
    _plot_diversity_summary(
        different_summary=different,
        similar_summary=similar,
        output_png=str(out_png),
    )
    print(f"wrote {out_png}")


if __name__ == "__main__":
    main()
