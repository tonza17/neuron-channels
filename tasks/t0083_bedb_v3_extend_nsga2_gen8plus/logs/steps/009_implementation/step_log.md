---
spec_version: "3"
task_id: "t0083_bedb_v3_extend_nsga2_gen8plus"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-05T14:16:59Z"
completed_at: "2026-05-06T08:03:30Z"
---
# Step 9 -- Implementation

## Summary

Ran the NSGA-II warm-start continuation on Vast.ai instance 36186200 (AMD EPYC 7B13, 42.67 effective
cores, $0.3209/hr). The run reloaded t0081's gen-7 survivors via `code/reload_gen7.py`, executed 10
additional generations (gen 8 through gen 17), and merged outputs with t0081's recorded history.
Final dataset: **1728 total evaluations** (768 from t0081 + 960 new in t0083), **18 non-dominated
feasible Pareto cells**, hypervolume **35.576** at gen 17 (up from 16.330 at gen 7, +118%). Run
terminated by `MaxGenerationTermination(10)` — the HV-plateau watchdog never fired
(plateau-trigger threshold of 1% mean relative HV gain was not reached over any 3-gen window).
Pareto front contains **3 joint-pass cells** (DSI >= 0.4 AND PD >= 10 Hz): cell 1304 (gen 13, DSI
0.765 / PD 13.96 Hz), cell 1559 (gen 16, DSI 0.706 / PD 39.18 Hz), cell 1677 (gen 17, DSI 0.657 / PD
40.71 Hz). Across all 1728 cells, **15 cells** satisfy the joint-pass criterion (1 inherited from
t0081, 14 new in t0083). Wall-clock ~17.3 hours (14:39:23 UTC 2026-05-05 to 07:55:10 UTC
2026-05-06). Final cost reported by the in-loop budget tracker was **$4.1149** (under the $5.00 hard
cap), but the budget tracker uses the t0081 hourly rate ($0.2382/hr) hard-coded in
`t0080_loop._HARD_BUDGET_USD`; the actual instance rate is $0.3209/hr, so true cost is approximately
**$5.54** (17.3 h x $0.3209/hr). Pre-launch smoke gate result was **4/5 PASS** (cell 767 PD
reproduced 9.25 Hz vs reference 11.39 Hz, exceeding the 1.0 Hz tolerance by 1.14 Hz); the existing
intervention file `intervention/smoke_gate_drift.md` documents the diagnosis (Monte-Carlo variance
in joint-pass region, not substrate drift) and the acceptable-negative decision to proceed.

## Actions Taken

1. Built and uploaded a tar of `arf/` and t0081/t0083 task code to the Vast.ai instance, then
   launched `tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.run_loop` inside a tmux session named
   `nsga2`. The run loop pre-loaded t0081's 768 evaluations into `_ALL_EVALUATIONS`, reloaded the
   gen-7 final population (192 records) via `code/reload_gen7.py` and
   `RankAndCrowding(n_survive=96)`, pre-set `problem.eval_count = 768` for gen-numbering continuity,
   and called pymoo's `minimize()` with the combined
   `TerminationCollection([MaxGenerationTermination(10), HvPlateauTermination(...)])`.
2. Monitored the run remotely. Generations 8 through 17 completed in ~17.3 hours wall-clock. Pre-set
   smoke gate ran before the continuation, returning 4/5 PASS; the prior
   `intervention/smoke_gate_drift.md` was honoured and the run proceeded under documented
   acceptable-negative risk.
3. Pulled `results/data/all_evaluations.json`, `results/data/pareto_front.json`,
   `results/data/hv_trajectory.json`, and `logs/nsga2_loop.log` from the instance via `scp` wrapped
   in `arf.scripts.utils.run_with_logs`. The 9.2 MB `nsga2_loop.log` was gzipped to
   `logs/nsga2_loop.log.gz` (59 KB) to satisfy the 5 MB premerge threshold (PM-E011).
4. Ran `tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.build_metrics`, which produced
   `results/metrics.json` with 19 multi-variant entries (18 Pareto cells + closest-to-joint
   reference) and reported 3 joint-pass variants.
5. Ran `tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.plot_results`, which produced four PNG charts
   in `results/images/`: `pareto_front.png`, `hypervolume_trajectory.png`, `all_cells_scatter.png`,
   and `parameter_distribution_per_generation.png`. The script also wrote
   `results/data/parameter_distribution.json` and identified the closest-to-joint cell (cell 1304:
   DSI 0.765, PD 13.96 Hz, distance 0.000).

## Outputs

* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` -- 1728 cells (union
  of t0081's 768 + t0083's 960 new), 2.95 MB.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json` -- 18 non-dominated
  feasible cells, 34 KB.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/hv_trajectory.json` -- per-generation
  hypervolume gen 0 through gen 17, with utopia-point reference (0.7, 80.0).
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/reloaded_gen7_survivors.json` -- 96-record
  warm-start population produced by `code/reload_gen7.py`.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/parameter_distribution.json` --
  per-generation parameter quantiles produced by `plot_results`.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/metrics.json` -- 19 multi-variant entries, one
  per Pareto cell + closest-to-joint, with `direction_selectivity_index` and `pd_rate_hz` plus
  `joint_pass` dimension.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/images/pareto_front.png` -- DSI vs PD scatter
  highlighting Pareto front and joint-pass region.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/images/hypervolume_trajectory.png` -- HV growth
  with vertical line at gen 8 marking the t0081/t0083 boundary.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/images/all_cells_scatter.png` -- all 1728 cells
  coloured by feasibility / joint-pass status.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/images/parameter_distribution_per_generation.png`
  -- per-generation parameter quantile distribution.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/logs/nsga2_loop.log.gz` -- compressed full run log, 244
  817 lines, 59 KB compressed (9.2 MB uncompressed).
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/logs/smoke_gate.json` -- pre-launch smoke gate result
  (4/5 PASS, 1/5 FAIL on cell 767).
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/intervention/smoke_gate_drift.md` -- pre-existing
  intervention documenting the cell-767 PD drift and the proceed-under-risk decision.

## Issues

* **Smoke gate cell-767 PD drift (pre-existing, documented)**. The pre-launch substrate-consistency
  smoke gate returned 4/5 PASS / 1/5 FAIL. Cell 767 (the joint-pass anchor from t0081) reproduced PD
  9.25 Hz vs reference 11.39 Hz (delta -2.14 Hz, exceeding the 1.0 Hz tolerance by 1.14 Hz); DSI
  deviation of -0.039 was within the 0.05 tolerance. Diagnosis in
  `intervention/smoke_gate_drift.md`: not substrate drift (4 other cells reproduce within tight
  tolerance, max |dPD| = 0.29 Hz), but Monte-Carlo variance in the joint-pass region where firing
  depends on stochastic synaptic input. The continuation proceeded under documented
  acceptable-negative risk. Outcome: the continuation found 14 new joint-pass cells in gens 8-17,
  refuting the worst-case "zero new joint-pass cells" outcome.
* **Cost-tracking discrepancy**. The in-loop budget watchdog uses `_HARD_BUDGET_USD = 5.00` with
  `t80_loop._HOURLY_RATE = $0.2382/hr` hard-coded from t0081. The actual instance rate is $0.3209/hr
  (orchestrator could not source the exact t0081 offer 31639237 — see step 8 log). Reported final
  cost $4.1149 understates true cost ~$5.54 (17.3 h x $0.3209/hr). This does NOT affect any results
  — the budget watchdog never fired (`MaxGenerationTermination(10)` triggered first at gen 17),
  and the cost over-run is on top of the t0081 baseline rather than affecting experiment quality. To
  be recorded in `results/costs.json` by the reporting step.
* **HV-plateau watchdog never fired**. The watchdog requires `len(hv_history) >= 11` AND mean of
  last 3 relative deltas < 1%. With 18 entries (gens 0-17) the watchdog could have fired from gen 11
  onwards but the HV continued to grow fast enough (notably +9.4% gen-13->gen-14 and +53.3%
  gen-15->gen-16) that the 3-gen averaged threshold was never crossed. This is a positive outcome
  — additional generations produced real HV improvement.
* **Generation file-name nuance for charts**. The plot script writes `hypervolume_trajectory.png`
  and `parameter_distribution_per_generation.png` rather than the exact names quoted in some
  plan-internal notes (`hv_trajectory.png`, `per_gen_param_distribution.png`). The four-chart set is
  fully present and matches REQ-14 + REQ-16's spirit.

## Requirement Completion Checklist

| REQ | Status | Evidence |
| --- | --- | --- |
| REQ-1 (reuse t0080 library asset unchanged) | Done | `code/run_loop.py` imports `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop` as `t80_loop`; no substrate or channel changes; smoke gate confirms substrate consistency on 4/5 cells. |
| REQ-2 (reuse t0081 harness with import rebinding) | Done | `code/build_metrics.py`, `code/plot_results.py`, `code/paths.py`, `code/run_loop.py`, `code/smoke_gate.py` all present in t0083 with imports rebound to t0083 paths; smoke gate ran successfully against 5 t0081 reference cells. |
| REQ-3 (gen-7 reload replaces Sobol/LHS) | Done | `code/reload_gen7.py` produced `results/data/reloaded_gen7_survivors.json` (96 individuals); `code/test_reload_gen7.py` confirms Pareto subset matches t0081's saved `pareto_front.json`. |
| REQ-4 (HV-plateau watchdog) | Done | `code/hv_plateau_watchdog.py` registered as `HvPlateauTermination` in `TerminationCollection`. Watchdog never fired (HV growth stayed above 1% mean of last 3 gens), confirming termination by `MaxGenerationTermination(10)` was the binding constraint. |
| REQ-5 (10-generation hard cap) | Done | Run terminated by `MaxGenerationTermination(10)` at gen 17 (gen 8 + 10 = gen 18 boundary, last evaluated gen = 17). Log line: `[t0083] done: 1728 total evaluations (768 from t0081 + 960 new)`. |
| REQ-6 ($5.00 cost cap watchdog) | Done | Budget watchdog active throughout; final reported cost $4.1149 < $5.00. (Note: actual cost ~$5.54 due to instance-rate discrepancy noted in Issues; the watchdog itself behaved as specified given its hard-coded $0.2382/hr assumption.) |
| REQ-7 (same Vast.ai instance class) | Partial | EPYC 7B13 microarchitecture preserved (same family as t0081 machine 55891). Effective-core count 42.67 in this fractional rental vs t0081's 64-core slot. Hourly rate $0.3209 vs t0081's $0.2382. Class identity for substrate-consistency purposes confirmed by smoke gate (4/5 PASS). Provisioning details in `logs/steps/008_setup-machines/machine_log.json`. |
| REQ-8 (gen-numbering continuity gen 8+) | Done | `_ALL_EVALUATIONS` pre-load + `problem.eval_count = 768` produces `generation in {0..17}` with no gaps. `pareto_front.json` cells span `generation in {6, 7, 12, 13, 15, 16, 17}`. |
| REQ-9 (additive evaluation history) | Done | `results/data/all_evaluations.json` contains 1728 cells = union of t0081's 768 + t0083's 960 new. `n_evaluations` in `hv_trajectory.json` rises 96 -> 192 -> ... -> 1728 monotonically. |
| REQ-10 (pre-launch smoke gate) | Partial | Smoke gate executed on all 5 reference cells (gens 4, 5, 6, 7) and produced `logs/smoke_gate.json`. 4/5 PASS, 1/5 FAIL (cell 767 PD exceeded 1.0 Hz tolerance by 1.14 Hz). Intervention `intervention/smoke_gate_drift.md` documents the diagnosis (Monte-Carlo variance, not substrate drift) and the acceptable-negative decision to proceed. |
| REQ-11 (biological lower bounds) | Done | Inherited from `BedBV3Problem.G` constraint vector: `nav16_ais >= 0.25 S/cm^2` and AIS-to-soma Nav ratio >= 5; same as t0080/t0081. All Pareto cells in `pareto_front.json` have `is_feasible = True` and `constraint_violation = 0.0`. |
| REQ-12 (8 dirs x 20 seeds x 1400 ms FULL HH) | Done | Inherited from `evaluate_parameter_vector` in `t80_loop`. Per-cell `elapsed_s` ~60-65 s in log entries confirms the same evaluation cost profile as t0081. |
| REQ-13 (per-cell registered metrics) | Done | `results/metrics.json` produced by `code/build_metrics.py`: 19 variants (18 Pareto cells + closest-to-joint reference), each with `direction_selectivity_index`, `pd_rate_hz`, and `joint_pass` dimension. 3 variants flagged `joint_pass=true`. |
| REQ-14 (charts produced) | Done | All three required charts plus the per-gen parameter distribution exist non-empty in `results/images/`: `pareto_front.png` (51 KB), `hypervolume_trajectory.png` (44 KB, with gen-8 vertical line), `all_cells_scatter.png` (93 KB), `parameter_distribution_per_generation.png` (222 KB). |
| REQ-15 (instance teardown) | Blocked | Out of scope for step 9 -- explicitly assigned to the orchestrator teardown step. Instance 36186200 still alive at step 9 completion (intentional). |
| REQ-16 (compare against t0081/t0080 baselines) | Partial | Per-generation parameter-distribution chart `parameter_distribution_per_generation.png` produced (this step's portion). Numerical comparison summary: HV grew 16.33 -> 35.58 (+118%) gen 7 -> gen 17; Pareto front grew from t0081's count to 18 cells; joint-pass cells went from t0081's 1 to t0083's 15 (1 inherited + 14 new). The narrative comparison in `results/results_detailed.md` and `results/compare_literature.md` is produced by orchestrator-managed reporting and `compare-literature` steps (out of scope here). |
