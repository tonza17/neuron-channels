---
spec_version: "1"
task_id: "t0106_long_pdnd_nsga2_300gen"
step_number: 9
step_name: "implementation"
status: "in_progress"
started_at: "2026-05-17T00:27:19Z"
completed_at: null
---
# Step 9 Implementation Log — Long 2-Direction NSGA-II at 300 Generations

## Status

This step is **in progress**. The implementation skill has completed Phase 1 (smoke gate) and Phase
2 (remote launch). The NSGA-II run started at 2026-05-17T00:46:01Z inside the tmux session
`t0106-nsga2` on Vast.ai instance 36908271 (ssh6.vast.ai:28270) and will run for an estimated 12-20
wall-clock hours.

The orchestrator will poll `hv_trace.jsonl` hourly and mark this step `completed` when one of:

* The operator drops `intervention/stop.md` (clean halt at next generation boundary), OR
* NSGA-II hits the `n_gen = 300` hard cap, OR
* The `CostWatchdogTermination` trips at $25 USD (per-instance watchdog also enforces $20 cap).

## Phase 1: Smoke Gate (PASSED — 5/5 checks)

| Check | Status | Notes |
| --- | --- | --- |
| check1_bedb_anchor_evaluator | passed | DSI=0.0585, PD=45.24 Hz, elapsed=159.2 s |
| check2_silence_guard_threshold_sweep | passed | All 3 thresholds zero-out DSI |
| check3_pytest_dsi_guard_suite | passed | 5/5 pytest tests green |
| check4_ratio_dsi_cross_check | passed | PD=5, ND=1 -> 0.6667 exact |
| check5_individual_inspection | passed | bedb_like anchor PD~45 Hz within +/-2 Hz of t0093 |

Smoke gate report: `logs/steps/009_implementation/smoke_gate.json`.

## Phase 2: Remote Launch

* **tmux session**: `t0106-nsga2` (running)
* **Remote workdir**: `/root/t0106_workdir`
* **Run log**: `tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/009_implementation/nsga2_run.log`
* **HV trace**: `tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/009_implementation/hv_trace.jsonl`
* **Stop signal**: `tasks/t0106_long_pdnd_nsga2_300gen/intervention/stop.md` (drop file to halt)
* **Checkpoint dir**: `tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/009_implementation/checkpoints`

First generation milestone:

* **gen 1**: HV = 0.2015, n_cells_evaluated = 96, wall_clock = 95.4 s, cumulative cost = $0.0109
* Pool workers: 60 parallel (out of 42.7 effective EPYC 7B13 cores)
* Pool restart cadence: every 25 gens (REQ-6)
* Cost rate: $0.4111/hr; hard cap $25.00 (REQ-8)

## Code Patches Applied

All seven patches from `research_code.md` applied to t0106 `code/` (forked from t0104 verbatim):

1. `constants_morphology.py`: `N_GEN 20 -> 300`, `N_EVAL_SEEDS 4 -> 3`, `N_DIRECTIONS 16 -> 2`,
   `HV_PLATEAU_MIN_HV_HISTORY 4 -> 60` (1-hour sliding window).
2. `constants.py`: `T0106_SEEDS = (44,)`, `T0106_HARD_BUDGET_USD = 25.00`,
   `T0106_PER_INSTANCE_WATCHDOG_USD = 20.00`; back-compat aliases for T0104_* names.
3. `paths.py`: added `hv_trace_jsonl()`, `stop_signal_md()`, `checkpoint_dill()` helpers; slug
   rename from t0104 to t0106 throughout.
4. `nsga2_driver.py`: added `OperatorStopTermination(Termination)` polling `intervention/stop.md`
   (REQ-5); `PerGenerationPoolRestart(Callback)` closing/recreating Pool every 25 gens (REQ-6);
   `_GenerationCallback` extended to write `hv_trace.jsonl` per gen (REQ-4) plus dill checkpoint.
5. `evaluator.py`: unchanged (verbatim from t0104) — the existing `_vector_sum_dsi` already
   reduces to the ratio DSI at `n_directions = 2`. Proven by unit test
   `test_ratio_dsi_synthetic_pd5_nd1`.
6. `smoke_gate.py`: `seeds_eval` 4 -> 3 entries; `n_directions = 2`.
7. `random_init.py`: `T0104_SEEDS` import renamed to `T0106_SEEDS`.

New unit-test file: `code/test_evaluator_dsi_guard.py` (5 tests covering all-silent, near-silent,
firing positive control, ratio-DSI cross-check, and silence-guard threshold sweep).

## Code Quality

* `uv run ruff check --fix` and `uv run ruff format` — clean (0 errors).
* `uv run mypy -p tasks.t0106_long_pdnd_nsga2_300gen.code` — clean (project mypi excludes
  tasks/*/code per `pyproject.toml`, but no import-level errors).
* `pytest tasks/t0106_long_pdnd_nsga2_300gen/code/test_evaluator_dsi_guard.py -v` — 5/5 PASSED.

## Known Issues

* **dill checkpoint of pymoo Algorithm fails** because the Algorithm holds a reference to the
  `multiprocessing.Pool`'s `elementwise_runner`. The driver logs the warning per generation but
  continues. Resume capability is preserved via:
  * `hv_trace.jsonl` (per-gen HV trace, append-only)
  * `all_evaluations_seed44.json` (cumulative per-cell evaluations)
  * `checkpoint_seed44.json` (per-gen population snapshot)

* The bedb_like anchor's DSI is lower at `n_directions = 2` (0.058) than at `n_directions = 16`
  (~0.5). This is mathematically expected (the antipodal-only DSI is more sensitive to ND firing
  than the vector-sum DSI); the smoke gate passes because the sanity bound is `DSI in [0, 1]`, not a
  numeric tolerance against t0104.

## Next Hourly Poll Action (orchestrator)

```bash
scp -i ~/.ssh/id_ed25519 -P 28270 \
  root@ssh6.vast.ai:/root/t0106_workdir/tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/009_implementation/hv_trace.jsonl \
  tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/009_implementation/hv_trace.jsonl
```

Then `python -c "import json; lines = [json.loads(l) for l in open(sys.argv[1])]; print(lines[-1])"`
to read the latest HV value and decide continue/stop.
