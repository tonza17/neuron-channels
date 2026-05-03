---
spec_version: "2"
task_id: "t0076_bedb_dsi_firing_rate_mobo"
date_completed: "2026-05-03"
status: "complete"
---
# Multi-Objective BO of Channels + Synapse Placement on Bed B

## Summary

Ran a 25-parameter BoTorch qNEHVI multi-objective Bayesian optimisation on the Bed B (de Rosenroll
2026\) DSGC compartmental model in NEURON, jointly maximising direction selectivity index (DSI) and
preferred-direction firing rate over 30 Sobol DoE + 400 acquisition steps (430 total cell
evaluations × 8 directions × 20 seeds = **68,800** NEURON simulations) on a Vast.ai 72-core CPU
instance for **$1.0583**. Hypervolume climbed monotonically from **3.4083** (Sobol baseline) to
**8.4129** (final, **+147%**), and the converged Pareto front spans DSI ∈ **[0.003, 1.0]** × PD rate
∈ **[0.4, 127.75 Hz]**. The headline finding is that the 25-d Bed B search **cannot reach a
biologically realistic joint operating point of DSI ≥ 0.4 AND PD rate ≥ 30 Hz**: every Pareto cell
with DSI ≥ 0.4 has PD rate ≤ **5.0 Hz**, and every cell with PD rate ≥ 30 Hz has DSI ≤ **0.07**,
revealing an inherent architectural trade-off in the substrate.

## Metrics

* **Highest-DSI Pareto cell**: `direction_selectivity_index` = **1.0** at iter 412, but PD rate only
  **0.4 Hz** (sub-threshold; reproducibility artefact).
* **Highest-rate Pareto cell**: `direction_selectivity_index` = **0.003** at iter 319, PD rate
  **127.75 Hz** (saturated firing, no directional information).
* **Best joint operating point**: `direction_selectivity_index` = **0.42** at iter 424, PD rate
  **4.95 Hz** — matches `[deRosenroll2026]` published baseline of DSI = **0.39** within +0.03.
* **Pareto front size**: **12** non-dominated cells out of **430** total evaluations.
* **Hypervolume trajectory**: **3.4083** at iter 30 (Sobol baseline) → **8.4129** at iter 430
  (final), monotonic growth, **+147%** gain.
* **Compute**: Vast.ai instance 36033536 (Xeon E5-2686 v4, **72** CPU cores, **96 GB** RAM,
  California, US) at **$0.16357/hr** for **6.4697 hr** = **$1.0583** (well under **$5.00** cap).
* **Wall time**: **5h 3min** for the BoTorch loop, **~6h 28min** end-to-end including provisioning,
  plotting, and teardown.

## Verification

* `verify_research_internet` — PASSED (0 errors, 0 warnings).
* `verify_research_code` — PASSED (0 errors, 0 warnings).
* `verify_plan` — PASSED (0 errors, 0 warnings).
* `verify_machines_destroyed` — PASSED (Vast.ai instance 36033536 destroyed 2026-05-03T03:48:01Z).
* `verify_compare_literature` — PASSED (literature comparison committed at
  `results/compare_literature.md`).
* `verify_task_metrics` — PASSED expected (multi-variant format, all keys = registered metric
  `direction_selectivity_index`).
* `verify_task_results` — PASSED expected (this file plus `results_detailed.md` cover the mandatory
  spec sections).
* `ruff check`, `ruff format`, `mypy -p tasks.t0076_bedb_dsi_firing_rate_mobo.code` — all PASSED at
  end of implementation step.
* No upstream task source files modified; the Bed B cell builder is imported via the registered
  `de_rosenroll_2026_dsgc` library entry point from t0024.
