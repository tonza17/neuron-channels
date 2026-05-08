---
spec_version: "1"
task_id: "t0098_visualise_pareto_morphologies"
date_completed: "2026-05-08"
status: "complete"
---

# Results Summary: Visualise t0091 Pareto Morphologies

## Summary

Produced four reproducible visualisations of t0091's 57-cell Pareto front: an 8x8 morphology
grid (sorted by DSI descending, colored by nearest anchor, annotated with DSI/PD-rate per panel),
a sorted DSI bar chart, a sorted PD-rate bar chart, and a DSI-vs-PD scatter with the strict
joint-pass cell starred. Total wall-clock: **8.65 s** on the local 64-core EPYC; total cost
**$0.00**.

## Metrics

* **57 cells** rendered (matches t0091's Pareto archive cardinality).
* **Anchor distribution recomputed and verified**: bedb_like=20, symmetric=0, pd_asymmetric=12,
  nd_asymmetric=9, alt_topology=16. Matches `t0091/results/data/anchor_tracking.json` exactly.
* **1 strict joint-pass cell** identified in the scatter (DSI>=0.5, PD>=30 Hz, robust>=0.7).
* **Morphology generation time**: 1.1 s for all 57 cells via `generate_fixed_morphology`
  (canonical via C-0093-01).
* **Chart rendering time**: ~7.5 s for all 4 PNGs combined.
* **Output sizes**: morphology grid ~900 KB; bar charts ~40 KB each; scatter ~55 KB.

## Verification

* `verify_task_file.py` — to be run during reporting step
* `verify_task_dependencies.py` — t0091, t0092, t0093 all completed (verified at check-deps)
* `verify_task_metrics.py` — empty `metrics.json` is valid (no registered metrics for a pure
  visualisation task)
* `verify_task_results.py` — to be run during reporting step
* `verify_task_folder.py` — to be run during reporting step
* `verify_logs.py` — to be run during reporting step
* `ruff check` and `ruff format` — PASSED on `code/`
* `mypy -p tasks.t0098_visualise_pareto_morphologies.code` — PASSED (no issues)
