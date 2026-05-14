---
spec_version: "3"
task_id: "t0104_nsga2_2obj_dsi_pdrate_3seeds"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-12T21:58:15Z"
completed_at: "2026-05-14T02:55:00Z"
---
## Summary

Ran the 2-objective NSGA-II optimisation for 2 of the originally planned 3 GA seeds on the Vast.ai
instance (seeds 44 and 55; seed 66 skipped per the early-stop intervention). Both seeds tripped the
per-seed $4 watchdog before reaching the planned gen 20: seed 44 stopped after gen 12 (HV = 2.85,
cost $4.69), seed 55 after gen 11 (HV = 7.59, cost $4.19). 2,208 cells evaluated in total. Zero
joint-pass cells (DSI ≥ 0.5 AND PD ≥ 30 Hz). However, the first DSI ≥ 0.5 cell in the entire
t0080-t0104 NSGA-II lineage was discovered by seed 55 at gen 11 (DSI = 0.5417 at PD = 3.57 Hz),
confirming that the substrate is not artificially DSI-capped. Pulled all data back, built 2
predictions assets that pass their verificators.

## Actions Taken

1. Local code prep: forked t0102's code/ folder verbatim, patched `evaluator.py` (REQ-1/2/3),
   `nsga2_driver.py` (REQ-4/5/6/8), `constants.py` (REQ-9), added `test_evaluator_dsi_guard.py`
   (REQ-7) and `run_three_seeds.sh`. ruff + mypy clean. 3 unit tests pass locally and remotely.
2. Remote setup: tarballed t0104 + t0080 MODs + t0024 MODs, uploaded to instance, compiled MOD
   libraries with `nrnivmodl`, installed pytest, ran 1-cell smoke gate (DSI = 0.0, PD = 0.71 Hz, 178
   s, 0 errors).
3. Ran NSGA-II seed 44 in tmux session `t0104_seed44`: gens 1-12 completed in 48,550 s (13.5 h
   wall-clock), final cost $4.69, watchdog tripped mid-gen-13 (pymoo finished gen 12 first).
4. Auto-launched seed 55 via `t0104_launcher` tmux session at 22:29 UTC May 13. Gens 1-11 completed
   in 43,305 s (12.0 h wall-clock), final cost $4.19. Gen 8 produced a discontinuous HV jump (2.94
   → 6.87) when NSGA-II discovered the DSI = 0.42 / PD = 15 region. Watchdog tripped after gen 11.
5. Researcher early-stop intervention recorded in `intervention/early_stop_after_seed_55.md` at
   21:55 UTC May 13; killed `t0104_launcher` tmux session to prevent seed 66 auto-start.
6. Pulled all 11 result data files back via scp (init pops, HV trajectories, Pareto fronts,
   evaluation seeds, NSGA-II checkpoints, algorithm config, all_evaluations for both seeds).
7. Ran `build_predictions_assets.py` to produce 2 predictions assets, one per seed. Each contains
   `details.json` + `description.md` + per-seed JSONL prediction files. Both pass
   `verify_predictions_asset`, `verify_predictions_description`, and `verify_predictions_details`
   with 0 errors. Two warnings each (PR-W014 model_id null, PR-W015 dataset_ids empty) — both
   expected for NSGA-II output predictions that do not consume an external dataset.
8. Updated `task.json` `expected_assets` from `{predictions: 3, answer: 1}` to
   `{predictions: 2, answer: 1}` consistent with the early-stop intervention.

## Outputs

* `code/` — 33 files including patched `evaluator.py`, `nsga2_driver.py`, `cost_watchdog.py`,
  `constants.py`, `test_evaluator_dsi_guard.py`, `run_three_seeds.sh`, `build_analysis_charts.py`
* `results/data/` — 13 JSON files: per-seed `all_evaluations`, `pareto_front`, `hv_trajectory`,
  `nsga2_checkpoint`, `init_pop` (3 seeds — seed 66 init pop was generated but never used),
  `algorithm_config`, `evaluation_seeds`
* `assets/predictions/nsga2-seed44-bedb-morph-n4-gen20-2obj/` — 1,152 prediction records
* `assets/predictions/nsga2-seed55-bedb-morph-n4-gen20-2obj/` — 1,056 prediction records
* `task.json` — `expected_assets` updated to reflect 2-seed scope
* `intervention/early_stop_after_seed_55.md` — researcher decision audit trail
* `logs/commands/*` — wrapped CLI command logs for every action

## Issues

The original plan called for 3 GA seeds × 20 generations × pop = 96 (5,760 evaluations). Actual
execution delivered 2 GA seeds × 11-12 generations × pop = 96 (2,208 evaluations) because:

* Per-seed cost watchdog tripped earlier than the planned gen 20 on both seeds — NEURON memory
  accumulation made per-gen wall-clock grow from ~15 min in gen 1 to ~120 min by gen 10-12. At ~$0.6
  / gen by gen 10, both seeds hit the $4 cap by gen 11-12.
* Seed 66 was explicitly skipped per researcher direction at 2026-05-13 ~21:55 UTC (full audit in
  `intervention/early_stop_after_seed_55.md`).

The DSI silence guard fired cleanly: 47/2,208 cells (2.1%) at DSI = 0.0 floor, zero spurious DSI =
1.0 silenced-cell artifacts — a definitive improvement over t0102's 27 artifact cells. REQ-3 is
working as designed.
