---
spec_version: "2"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_completed: "2026-05-04"
status: "complete"
---
# Results Summary: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Summary

Ran a 49-d BoTorch qLogNEHVI multi-objective Bayesian optimisation on the AIS-augmented de Rosenroll
2026 Bed B DSGC compartmental model in NEURON, jointly maximising direction selectivity index (DSI)
and preferred-direction (PD) firing rate over 75 Sobol DoE + 416 acquisition iterations (491 total
cell evaluations × 8 directions × 20 seeds = **78,560** NEURON simulations) on a Vast.ai 64-core
CPU instance for **$3.93** (24.86 h total). The loop was stopped early via SIGTERM at acq 416 (vs
the planned 700) per researcher decision after the hypervolume curve plateaued and per-cell
wall-clock grew super-linearly under O(N³) GP-fit scaling. **The 49-d substrate produces a Pareto
front with 17 non-dominated cells and final hypervolume 11.41**, exceeding the t0076 final HV (8.41)
by **+36%**. The pass criterion (`DSI ≥ 0.4 AND PD ≥ 10 Hz`) was **narrowly missed**: the
closest Pareto cell (iter 81) has **DSI 0.316, PD 9.68 Hz** — short by 0.084 on DSI and 0.32 Hz on
PD rate. The augmented substrate genuinely improves Pareto coverage over t0076 but the joint
operating point sits just outside the achievable Pareto front.

## Metrics

* **Headline registered metric** (`direction_selectivity_index` per
  `meta/metrics/direction_selectivity_index/`): the Pareto front spans DSI **0.007 → 1.000**
  across 17 cells.
* **Best Pareto cell on DSI axis**: iter 290 with **DSI = 1.000, PD = 0.36 Hz** (sub-threshold
  high-DSI extreme).
* **Best Pareto cell on PD-rate axis**: iter 475 with **DSI = 0.007, PD = 197.14 Hz** (saturated
  high-rate corner; no directional information).
* **Closest Pareto cell to joint pass criterion**: iter 81 with **DSI = 0.316, PD = 9.68 Hz**
  (misses pass criterion by 0.084 on DSI and 0.32 Hz on PD rate).
* **Final hypervolume**: **11.41** (vs t0076 final 8.41 = **+36%**, vs the 1.5× rule-out threshold
  of 12.62 = 90% of the way there).
* **Total cell evaluations**: 491 (75 Sobol + 416 qLogNEHVI acquisitions); BO stopped early at acq
  416 / 700 per cost-of-progress decision.
* **Compute**: Vast.ai instance 36068067 (AMD EPYC 7B13, **64** effective CPU cores, **503 GB** RAM,
  Norway) at **$0.1582/hr** for **24.8578 h** = **$3.9335** (under the $5.00 per-task limit but
  slightly over the researcher-authorised $4.00 envelope).

## Verification

* `verify_machines_destroyed.py` — PASSED (0 errors, 2 expected warnings: API-unreachable for live
  confirmation; >12 h runtime).
* `verify_library_asset.py` (de_rosenroll_2026_dsgc_ais) — PASSED (0 errors, 1 LA-W014 warning: no
  test_paths, accepted; the BO loop is the end-to-end test).
* `verify_research_papers.py` — PASSED (0 errors, 0 warnings).
* `verify_research_internet.py` — PASSED (0 errors, 0 warnings).
* `verify_research_code.py` — PASSED (0 errors, 0 warnings).
* `verify_plan.py` — PASSED (0 errors, 0 warnings).
* `verify_task_metrics.py` — to be run at reporting step.
* `verify_task_results.py` — to be run at reporting step.
* `verify_task_file.py` — to be run at reporting step.
* `verify_logs.py` — to be run at reporting step.
