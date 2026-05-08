---
spec_version: "1"
task_id: "t0091_morphology_extended_nsga2_v1"
date_completed: "2026-05-08"
status: "complete"
---

# Results Summary: First Joint 68-d NSGA-II with Morphology Generator In-Loop

## Summary

Joint 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) on Bed B with the t0092 patched
procedural generator inside the per-cell evaluation loop reached **gen 2 of 8** before user-
directed teardown, producing a **57-cell Pareto front**. **Zero cells pass the t0086/t0088
biological-plausibility scorecard** under worst-case prior aggregation; one cell is a strict
joint-pass on (DSI ≥ 0.5, PD ≥ 30 Hz, robustness ≥ 0.7) but fails the biological priors. **Total
spend $0.6454** (16% of the $4.00 watchdog cap) over 2.63 hours of Vast.ai uptime.

## Metrics

* **57 Pareto cells** (REQ-10 threshold ≥ 8 met by 7×).
* **HV trajectory**: gen 1 = 14.07 → gen 2 = 23.71 (+68% growth; not yet plateaued).
* **Anchor distribution in Pareto**: bedb_like 20, symmetric **0**, pd_asymmetric 12,
  nd_asymmetric 9, alt_topology 16, random 0.
* **PD vs ND asymmetric counts**: 12 vs 9, one-sided permutation **p = 0.331** (1000 bootstrap
  resamples). Below the 5:1 effect-size threshold from Briggman 2011 needed to claim functional
  asymmetry.
* **Mean DSI per anchor in Pareto** (registered metric): bedb_like 0.110, pd_asymmetric 0.176,
  nd_asymmetric 0.451, alt_topology 0.263, all-Pareto 0.221.
* **One strict joint-pass cell** (gen 2): DSI = 0.511, PD = 35.1 Hz, robustness = 0.79; fails
  biological plausibility on at least one channel-density prior.
* **Length-vs-DSI Spearman**: ρ = -0.07 (no monotonic dependency).
* **Total cost**: $0.6454 (well under $4.00 hard cap and $3.00–3.50 plan estimate).

## Verification

* `verify_predictions_asset.py` — PASSED (0 errors, 2 expected warnings)
* `verify_answer_asset.py` (via `meta/asset_types/answer/verificator.py`) — PASSED (0 errors,
  0 warnings)
* `verify_task_metrics.py` — PASSED (0 errors, 0 warnings)
* `verify_machines_destroyed.py` — PASSED (0 errors, 1 RM-W001 warning is verifier false
  negative for already-destroyed instances; instance 36344985 confirmed destroyed via empty
  `vastai show instances` output)
* `ruff check` on `code/` — PASSED
* `mypy -p tasks.t0091_morphology_extended_nsga2_v1.code` — PASSED (no issues)
