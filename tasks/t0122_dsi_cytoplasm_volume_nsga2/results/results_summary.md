---
spec_version: "1"
task_id: "t0122_dsi_cytoplasm_volume_nsga2"
date_completed: "2026-05-24"
status: "complete"
---
# Results Summary: DSI vs Cytoplasm-Volume NSGA-II

## Summary

68-d Bed B + 14-d morphology NSGA-II with cytoplasm volume replacing PD-rate as the second
objective. 60 generations on Vast.ai EPYC 7K62 48-core (instance 37546422), GA seed 1524, 5760 cells
evaluated. **Cuntz 2010 falsifiable prediction is CONFIRMED: 10/10 top-DSI cells fall in the
predicted balancing-factor `[0.2, 0.7]` band**, all clustering at `bf = 0.500`. Best LEGIT DSI
0.9753 at cytoplasm volume 250.2 um^3 (two orders of magnitude smaller than t0091's ~30000 um^3
cells). Total cost $0.50 of $6 cap (8.3%).

## Metrics

* **GA seed**: **1524** (drawn via `secrets.randbelow(10000)`, non-round).
* **Final generation**: **60 / 60** (clean max_gen ceiling exit; no watchdog, no operator-stop, no
  plateau).
* **Cells evaluated**: **5760**.
* **Best LEGIT DSI** (DSI < 0.9999 AND PD-rate >= 30 Hz AND volume <= 50000 um^3): **0.9753** at
  cytoplasm volume = 250.2 um^3.
* **n_legit (strict)**: **10**; **n_silence_corner (DSI = 1.0)**: **1116**.
* **Cuntz 2010 in-band count (top-10 by DSI)**: **10 / 10** at `bf = 0.500` (midpoint of [0.2, 0.7]
  band).
* **Final hypervolume**: **49763.35** (ref point (0, 50000 um^3)).
* **Total cost**: **$0.50** of $6 cap (8.3%); Vast.ai balance after: $6.50.
* **Wall-clock**: ~66 min implementation + ~19 min setup + ~7 min teardown.

## Verification

* `verify_research_code` -- PASSED (0/0).
* `verify_plan` -- PASSED (0/0).
* `verify_predictions_asset` -- PASSED (0 errors, 2 expected warnings: null model_id, empty
  dataset_ids -- procedural-cell pattern).
* Local-fallback answer-asset verifier (`meta.asset_types.answer.verificator`) -- PASSED (0/0).
* `verify_machines_destroyed` -- PASSED (1 expected warning RM-W001 -- destroyed-instance API
  returns NoneType, treated as benign).
* `ruff check`, `ruff format`, `mypy -p tasks.t0122_dsi_cytoplasm_volume_nsga2.code` -- all PASSED
  on 33 code files.
* Smoke gate (8 checks) -- 8/8 PASS locally + remotely.
* Unit tests (7 checks on evaluator silence-guard) -- 7/7 PASS.
* All 6 hard constraints verified by grep + smoke-gate checks C1-C6 (`_POOL_RESTART_EVERY=10`,
  `HV_PLATEAU_AUTO_STOP=False`, `POP_SIZE=96`, `N_EVAL_SEEDS=3`, `N_GEN_MAX=60`,
  `COST_CAP_USD=6.0`).
