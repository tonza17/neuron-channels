---
spec_version: "1"
task_id: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"
step_number: 9
step_name: "implementation"
status: "handoff_pending_nsga2_completion"
date_handoff: "2026-05-25"
---
# Implementation Step 9 Handoff

## Status

* **Phase**: NSGA-II running in background on Vast.ai; subagent session ending before completion to
  preserve budget.
* **Last observed**: gen 3 of 60 complete at 14:06 UTC, HV = 1.453e10, cost $0.0271.
* **Background process**: tmux session `nsga2` on Vast.ai instance 37767708, PID 2880 (driver main +
  60 workers), launched at 13:54 UTC.
* **Expected completion**: ~17:15 UTC (60 gens at observed ~176s/gen mean = ~2.9h wall clock).
* **Projected cost**: $0.55 (well under $6 cap).

## What Is Complete

* All Phase 1 code-fork steps (REQ-1 through REQ-13, REQ-28):
  * 36 Python modules forked from `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/`.
  * `build_t0124_outputs.py` dropped (replaced by `build_t0126_outputs.py`).
  * Global import-path rewrite
    `tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code -> tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code`
    applied.
  * Global constant rewrite `T0124_ -> T0126_` applied.
  * `T0126_SEEDS = (8929,)` set, asserted distinct from t0124's 6650 (REQ-9).
  * `OperatorStopTermination` REMOVED from live `TerminationCollection` in `nsga2_driver.py`
    (REQ-15, REQ-16). The class definition is preserved for smoke-gate introspection; the sentinel
    `STOP_FILE = pathlib.Path("/dev/null/never")` is in the source comment block.
  * NEW module `code/t0124_vs_t0126_comparator.py` (440 lines) implements the S-0124-01 decision
    rule and side-by-side Pareto chart (REQ-18, REQ-20).
  * NEW module `code/post_run_analysis.py` orchestrates Steps 10-11 chart generation.
  * NEW module `code/build_t0126_outputs.py` (forked from `build_t0124_outputs.py` with
    `t0124 -> t0126`,
    `nsga2-dsi-atp-per-spike-bedb-morph -> nsga2-dsi-atp-per-spike-bedb-morph-60gen`, and answer-id
    rewrites).
  * 7/7 DSI silence-guard regression tests pass.
  * All code passes `ruff check`, `ruff format`, and `mypy`.
  * Hard-constants verification command from `plan/plan.md` Verification Criteria runs cleanly.

* Phase 2 setup-machines + smoke-gate steps (REQ-14, REQ-13):
  * Vast.ai instance 37767708 (EPYC 7C13 32 effective vCPUs, 64 GB RAM, Virginia US, $0.1844/hr)
    provisioned and verified at 13:07 UTC (machine_log.json present).
  * Carter-Bean smoke-gate ALL 9 CHECKS PASS on remote:
    * Check 9 (Carter-Bean): `observed_atp_per_ap_per_cm = 6.138e8` inside the canonical
      `[1e8, 1e9]` band (verdict = PASS).
    * Check 7 (DSI/ATP sanity): OK.
    * Check 8 (F-axis sign): OK -- F[0] = -DSI, F[1] = +ATP.
    * Check 4 (`_POOL_RESTART_EVERY == 10`): OK.
    * Check 5 (cost-watchdog wiring at $6 task cap): OK.
    * Check 6 (no `HVPlateauTermination` in live collection): OK.
  * Local smoke-gate report at
    `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/logs/steps/009_implementation/smoke_gate.json`.

## What Is In Progress (Background, Autonomous)

* NSGA-II run with seed 8929, n_gen 60, pop 96, 2 directions (0/180 deg), 3 eval seeds, $6/$5
  watchdog. Launched in tmux session `nsga2` via `setsid bash /tmp/launch_nsga2.sh`.
* Per-gen `hv_trace.jsonl` writes are working. The `dill checkpoint` writes FAIL with
  `NotImplementedError: pool objects cannot be passed between processes or pickled` (the parallel
  multiprocessing.Pool is not picklable). This is a known caveat -- the per-gen JSON trace + final
  population dump are still written. Resume-from-checkpoint is therefore NOT available; if the
  instance crashes, the run must restart from scratch.
* Cost watchdog reading `$0.1844/hr` from `logs/steps/008_setup-machines/machine_log.json` and
  tracking actual spend.

## Next Subagent Pickup Steps (after NSGA-II completes)

The orchestrator should spawn a fresh subagent (or the same one if it has budget) to:

1. **Confirm NSGA-II completion**:

   ```bash
   ssh -i /c/Users/md1avn/.ssh/id_ed25519 -p 17708 root@ssh2.vast.ai \
     'grep NSGA2_EXIT /root/t0126_workdir/nsga2.log; tail -50 /root/t0126_workdir/nsga2.log'
   ```

   Expected: `NSGA2_EXIT=0` line + final summary printed.

2. **Pull results back**:

   ```bash
   ssh -i /c/Users/md1avn/.ssh/id_ed25519 -p 17708 root@ssh2.vast.ai \
     'cd /root/t0126_workdir/repo && tar czf - \
        tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data \
        tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/logs/steps/009_implementation' \
     | tar xzf - -C C:/Users/md1avn/Documents/GitHub/neuron-channels-worktrees/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/
   ```

   Files expected:
   * `results/data/pareto_front_seed8929.json` (final Pareto front, n>=20 expected)
   * `results/data/all_evaluations_seed8929.json`
   * `results/data/hv_trajectory_seed8929.json`
   * `logs/steps/009_implementation/hv_trace.jsonl` (60 lines)

3. **Run post-run analysis (Steps 10-11)**:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- \
     uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.post_run_analysis \
       --seed 8929
   ```

   Produces:
   * `results/images/pareto_front_t0124_vs_t0126.png` (REQ-20)
   * `results/images/pareto_front_dsi_vs_atp.png` (REQ-19)
   * `results/images/hv_trajectory_seed8929.png` (REQ-24)
   * `results/data/comparator_report.json` (S-0124-01 verdict)

4. **Run Step 11 remaining charts via `build_pareto_plots`**:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- \
     uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.build_pareto_plots \
       --seed 8929
   ```

   Produces:
   * `results/images/carter_bean_atp_per_ap_check.png` (REQ-21)
   * `results/images/attwell_laughlin_signalling_budget.png` (REQ-22)

5. **Run Step 12 top-50 morphologies (REQ-23)**:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- \
     uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.build_top50_morphologies \
       --seed 8929
   ```

6. **Run Step 13-15 metrics + predictions + answer asset (`build_t0126_outputs.py`)**:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- \
     uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.build_t0126_outputs
   ```

   Produces:
   * `results/metrics.json` (4 variants: best_legit, overall_max_dsi, overall_min_atp,
     dsi_eq_one_count)
   * `assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph-60gen/details.json + description.md + files/predictions.jsonl.gz`
   * `assets/answer/dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact/details.json + short_answer.md + full_answer.md`

7. **Run verificators**:

   ```bash
   uv run python -u -m arf.scripts.verificators.verify_predictions_asset \
     tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen
   uv run python -u -m arf.scripts.verificators.verify_answer_asset \
     tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen
   uv run python -u -m arf.scripts.verificators.verify_task_metrics \
     tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen
   ```

8. **Keep Vast.ai instance running** -- the orchestrator's step 010_teardown destroys it.

## Files Modified in This Session

* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/` -- 36 forked modules + 3 new modules
  (`build_t0126_outputs.py`, `t0124_vs_t0126_comparator.py`, `post_run_analysis.py`).
* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/logs/steps/009_implementation/` --
  `smoke_gate.json`, `hv_trace.jsonl` (partial; will grow on remote), `implementation_state.json`,
  this `HANDOFF.md`.
* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/` -- `init_pop_seed8929.json`,
  `algorithm_config.json`.
* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/images/` --
  `pareto_front_t0124_vs_t0126.png` (placeholder; gets overridden when t0126 front is ready).

## Notes

* The NSGA-II run is fully decoupled from the subagent session per S-0124-02 mitigation. It will
  continue running even after this subagent's SSH connection ends because the launch was via
  `setsid bash` from inside a `tmux new-session -d`.
* Cost-watchdog autorun: if cost reaches $5 per-instance / $6 task, the driver writes
  `intervention/budget_overrun_seed8929.md` and `vastai destroy` is NOT auto-called (we did not pass
  `--teardown-on-watchdog`); the orchestrator's step 010_teardown handles teardown.
* The `dill checkpoint` warning logged at every generation is benign -- the parallel pool cannot be
  pickled, so the `.pkl` files don't get written, but the JSON files (`hv_trace.jsonl`,
  `hv_trajectory_seed8929.json`, `all_evaluations_seed8929.json`) capture all needed data.
