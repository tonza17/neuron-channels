---
spec_version: "2"
task_id: "t0083_bedb_v3_extend_nsga2_gen8plus"
date_completed: "2026-05-06"
---
# Results Summary -- t0083_bedb_v3_extend_nsga2_gen8plus

## Summary

The NSGA-II warm-start continuation extended t0081's run from gen 7 through gen 17 on the same v3
Bed B substrate, producing **14 new joint-pass cells** (DSI >= 0.4 AND PD >= 10 Hz) on top of
t0081's single inherited cell 767, for a project total of **15 joint-pass cells** at completion.
Hypervolume grew from **16.330 at gen 7** to **35.576 at gen 17** (+118%) over 960 additional
evaluations; the run terminated under the gen-17 hard cap rather than the HV-plateau watchdog.

## Metrics

* **15 joint-pass cells** across 1728 total evaluations: 1 inherited from t0081 (cell 767, gen 7,
  DSI 0.494 / PD 11.39 Hz) and 14 new ones produced in t0083 generations 13-17.
* **3 of those 15 joint-pass cells lie on the final Pareto front**: cell 1304 (gen 13, DSI 0.7652 /
  PD 13.96 Hz), cell 1559 (gen 16, DSI 0.7061 / PD 39.18 Hz), and cell 1677 (gen 17, DSI 0.6570 / PD
  40.71 Hz). Cell 1304 is the project's headline highest-DSI joint-pass cell to date.
* **Hypervolume grew from 16.330 at gen 7 to 35.576 at gen 17 (+118%)**, with the largest single-gen
  jump from gen 15 (23.142) to gen 16 (34.503), corresponding to NSGA-II discovering the high-PD
  joint-pass region (cells 1559 / 1624).
* **18 non-dominated feasible cells** on the final Pareto front (vs t0081's 16 cells at gen 7).
* **Total cost $5.828** across **18.16 hours** of Vast.ai EPYC 7B13 instance lifetime; in-loop
  watchdog reported $4.115 due to a hard-coded $0.2382/hr rate that did not match the actual
  $0.3209/hr offer rate (documented in `costs.json` `note`).

## Verification

* `verify_task_metrics t0083_bedb_v3_extend_nsga2_gen8plus`: PASSED (no errors, no warnings).
* `verify_machines_destroyed t0083_bedb_v3_extend_nsga2_gen8plus`: PASSED with 3 informational
  warnings (RM-W001 API unreachable, RM-W003 runtime > 12 h, RM-W006 no checkpoint_path).
* `verify_research_code t0083_bedb_v3_extend_nsga2_gen8plus`: PASSED (run during research-code).
* `verify_plan t0083_bedb_v3_extend_nsga2_gen8plus`: PASSED (run during planning).
* All 16 plan-defined REQ items resolved (REQ-1 through REQ-16); see `results/results_detailed.md`
  `## Task Requirement Coverage`.
