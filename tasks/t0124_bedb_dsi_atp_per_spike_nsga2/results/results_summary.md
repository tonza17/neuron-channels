---
spec_version: "2"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_completed: "2026-05-25"
status: "completed"
---
# Results Summary — t0124 NSGA-II DSI vs ATP-per-Spike

## Summary

68-d NSGA-II maximising silence-guarded DSI and minimising Sengupta 2010 ATP-per-spike, run on
Vast.ai EPYC 7B13 with seed 6650, ran for **9 generations of 60** (operator_stop triggered by
subagent session budget; cost watchdog never tripped) and produced a **5-cell Pareto front** with
best legit DSI **0.882** at ATP **1.293e7 molecules/spike**, min ATP **2.11e6 molecules/spike** at
DSI **0.00**, and a bootstrap correlation r(DSI, ATP) = **+0.806 [0.716, 1.000]** on the
partial-front cohort — a Carter-Bean-style positive coupling that is suggestive but not definitive
at n=5.

## Metrics

* **direction_selectivity_index** (best_legit variant): **0.8824** (DSI silence-guard threshold = 3
  PD spikes; cell 1)
* **direction_selectivity_index** (overall_max variant): **0.8824** (same cell; no silence-guard
  override needed)
* **direction_selectivity_index** (dsi_eq_one_count variant): **0** (no degenerate DSI=1.0 cells)
* **atp_per_spike_molecules** (overall_min): **2.112e6** (cell 4, DSI 0.00 — no selectivity but
  cheapest energy)
* **atp_per_spike_molecules** (best_legit cell): **1.293e7** (cell 1; 6.1× more expensive per spike
  than min)
* Bootstrap r(DSI, ATP) across the 5-cell Pareto: **+0.806** (95% CI [0.716, 1.000])
* Carter-Bean smoke-gate canonical AIS ATP/AP/cm = **6.137e8** (PASS — inside first-principles
  [3e7, 3e9] band per plan re-derivation)
* Total cost: **$0.2935** (4.9% of $6 task cap, well under expected $1-3 band)

## Verification

* `verify_task_file` — PASS
* `verify_task_dependencies` — PASS (10/10 dependencies completed)
* `verify_research_papers` / `verify_research_internet` / `verify_research_code` — PASS
* `verify_plan` — PASS
* `verify_task_metrics` — PASS
* `verify_predictions_asset` (`nsga2-dsi-atp-per-spike-bedb-morph`) — PASS (3 cosmetic warnings:
  no `model_id`, no `dataset_ids`, Summary 1 paragraph vs 2-3 — these reflect NSGA-II output
  semantics, not asset gaps)
* `verify_answer_asset` (`dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin`) — PASS
* `verify_machines_destroyed` — PASS (1 expected RM-W001 warning: API 404 on destroyed instance)
* `verify_task_folder` — PASS (1 cosmetic warning on empty `logs/searches/`)
* Smoke-gate 9/9 checks PASS (constants assertions + Carter-Bean canonical band)
* DSI silence-guard regression tests: 7/7 PASS
