---
spec_version: "3"
task_id: "t0129_t0126_signed_dsi_real_rates_1seed"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-26T13:21:56Z"
completed_at: "2026-05-26T19:30:00Z"
---
# Step 9: implementation

## Summary

Forked t0126's NSGA-II code into `tasks/t0129_*/code/`, applied the two evaluator corrections
(signed antipodal DSI replacing vector-sum DSI; `pd_rate_hz`/`nd_rate_hz` as real per-cell scalar
fields from actual NEURON spike counts) plus the per-cell parameter dump
(`results/cell_params.jsonl`, path captured at `BedBV3MorphProblem.__init__` so it pickles into
workers). Unit-tested the DSI helper (10/10 pass), passed the 9-check smoke gate locally and again
on the remote, then ran 60 generations of NSGA-II on Vast.ai (32-vCPU EPYC 7C13, same physical
machine as t0126). Final outputs: 5760 cells evaluated (0 errors, 4.6% silenced), 9-cell Pareto
front spanning DSI 0→1.0 at ATP 0.78→6.66 M molec/spike, plus 95 negative-DSI cells (the
signed/vector-sum distinction the task was built to expose).

Step had two recoveries from initial planning errors: (1) the planner assumed local CPU but t0126
actually used Vast.ai, so the first launch on local 4 workers extrapolated to 5-7 days and was
killed; (2) the local smoke gate's check 1 (t0080 MOD-dependent anchor) had to be deferred locally
but ran clean on the remote.

## Actions Taken

1. Forked t0126 code (~30 files: evaluator, nsga2_driver, smoke_gate, tests, metrics_builder,
   build_*, post_run_analysis, comparators, constants, generator_wrapper, apply_params,
   atp_per_spike, biological_priors, biological_scorecard, mi_estimator, trial_helpers, bootstrap,
   mods/, anchor_definitions, anchor_classifier, build_cell_ais, extend_with_ais, cytoplasm_volume,
   cost_watchdog, hv_plateau_watchdog) into `tasks/t0129_*/code/`. Renamed all `tasks.t0126_*`
   imports to `tasks.t0129_t0126_signed_dsi_real_rates_1seed`.
2. evaluator.py edits:
   - Added `_signed_antipodal_dsi(*, spike_counts_per_dir) -> float` returning
     `(R_PD - R_ND)/(R_PD + R_ND)` in `[-1, 1]`, with `WORST_CASE_DSI = -1.0` silence sentinel.
   - Renamed `CellEvalResult.dsi_vector_sum` -> `dsi_signed`. Updated all call sites to use the
     signed helper. F = `[-cell_result.dsi_signed, +atp_per_spike_molecules]`.
   - Added `pd_rate_hz` and `nd_rate_hz` as named scalar fields on `CellEvalResult`, both
     `mean(spikes) / (TSTOP_MS / 1000.0)` from the actual per-direction spike counts.
   - Added `cell_params.jsonl` writer with path captured in `BedBV3MorphProblem.__init__` (not env
     var) so it survives pickling into worker processes.
3. Renamed `run_seed8929.sh` -> `run_seed3517.sh`. Updated all paths, removed the
   `T0126_CELL_TRACE_JSONL` env-var sink (replaced by constructor-time path), fixed PYTHONPATH
   construction for cross-platform (Windows used `cygpath -w` + `;`, Linux uses `:`).
4. Wrote `code/test_evaluator_dsi_signed.py` (10 unit tests covering PD>ND, PD<ND, PD=ND>0, PD=ND=0
   silence, silence guard pd_spikes_sum<3, synthetic and positive-control cases). All PASS.
5. Updated all downstream consumers (metrics_builder, build_predictions_assets, build_results,
   t0124_vs_t0126_comparator, post_run_analysis) for the field rename.
6. Local smoke gate: 9/9 PASS (check 1 deferred — needs t0080 MODs not compiled locally).
7. Attempted local NSGA-II launch on 4 workers; observed throughput ~7 min/cell projecting to 5-7
   days for 60 gens. KILLED at gen 5 because the planner had wrongly assumed local CPU sufficiency.
   Preserved 10-cell partial cell_params as
   `results/local_killed_run/cell_params_local_killed.jsonl`. Dropped 120 MB of throwaway
   checkpoints/data/log from the killed run.
8. Pivoted to Vast.ai (un-skipped setup-machines and teardown steps). Provisioned instance 37924958
   on the same physical machine as t0126 (machine_id 34698) — see step 8 log.
9. Wrote `code/remote_bootstrap.sh` and `code/remote_sync_push.sh`. Bootstrap installed apt/pip deps
   on the remote (neuron 8.2.7, pymoo 0.6.1.6, numpy 2.4.6, etc.). Compiled t0080 + t0024 MOD trees
   with `nrnivmodl` (both PASS, 64KB libnrnmech.so each).
10. Remote smoke gate: **9/9 PASS** (this time including check 1).
11. Launched NSGA-II in tmux session `nsga2_seed3517` on the remote via `bash run_seed3517.sh`.
    Started 2026-05-26T15:22:25Z, completed 60 gens at 2026-05-26T18:45:33Z (12184s wall = 3h
    23min). Cost during active run: $0.6468.
12. Final result: 5760 cells evaluated, 9-cell Pareto front (DSI range 0→1.0, ATP range 0.78-6.66
    M molec/spike), 95 negative-DSI cells, 264 silenced (4.6%), 0 errors.
13. Pulled all results back via SCP. Compressed two oversized JSON files in `results/data/`
    (`all_evaluations_seed3517.json` 12.5 MB → 3.2 MB, `nsga2_checkpoint_seed3517.json` 12.4 MB
    → 3.1 MB) to satisfy PM-E011 5 MB threshold.

## Outputs

* `tasks/t0129_*/code/` (30+ files, signed-DSI evaluator + driver + downstream consumers)
* `tasks/t0129_*/code/test_evaluator_dsi_signed.py` (10 unit tests, all pass)
* `tasks/t0129_*/code/run_seed3517.sh`
* `tasks/t0129_*/code/remote_bootstrap.sh`
* `tasks/t0129_*/code/remote_sync_push.sh`
* `tasks/t0129_*/logs/steps/009_implementation/smoke_gate.json` (local 9/9 pass, check 1 deferred)
* `tasks/t0129_*/logs/steps/009_implementation/smoke_gate_remote.json` (remote 9/9 pass)
* `tasks/t0129_*/logs/steps/009_implementation/hv_trace.jsonl` (60 generations)
* `tasks/t0129_*/logs/steps/009_implementation/checkpoints/` (60 .pkl files, gen 1-60)
* `tasks/t0129_*/logs/steps/009_implementation/implementation_state.json`
* `tasks/t0129_*/logs/nsga2_seed3517.log` (run log, 240 lines)
* `tasks/t0129_*/results/cell_params.jsonl` (5760 lines, ~9.2 MB)
* `tasks/t0129_*/results/data/init_pop_seed3517.json` (Phase A random init, 96 cells × 68 dims)
* `tasks/t0129_*/results/data/pareto_front_seed3517.json` (final 9-cell Pareto)
* `tasks/t0129_*/results/data/hv_trajectory_seed3517.json` (60-gen HV trace)
* `tasks/t0129_*/results/data/all_evaluations_seed3517.json.gz` (compressed)
* `tasks/t0129_*/results/data/nsga2_checkpoint_seed3517.json.gz` (compressed)
* `tasks/t0129_*/results/data/algorithm_config.json`
* `tasks/t0129_*/results/data/evaluation_seeds.json`
* `tasks/t0129_*/results/local_killed_run/cell_params_local_killed.jsonl` (audit; 10 cells from the
  killed local-CPU attempt — preserved as evidence the writer functions correctly)

## Issues

Two recoveries from planning errors:

1. **Wrong compute target assumed in planning.** The planner was told "local CPU only" because the
   plan misread t0126's runtime (t0126 actually ran on Vast.ai 32 vCPU EPYC, not local CPU). Local
   4-worker run extrapolated to 5-7 days; killed at gen 5 and pivoted to Vast.ai. Cost of the dead
   end: ~0 wall-clock damage (caught at gen 5), 120 MB of throwaway disk, ~30 min of sub-agent time.

2. **Local smoke gate check 1 deferred.** Check 1 (single-eval anchor PD rate) requires the t0080
   MOD library compiled with `nrnivmodl`; local NEURON install didn't have it ready. Acceptable per
   the smoke-gate `--skip-check-1` flag. Remote run executed all 9 checks successfully.

REQ coverage summary against the plan's REQ-1..REQ-23 checklist: REQ-1 through REQ-13 all DONE.
REQ-14..REQ-23 (post-run chart construction, predictions/answer assets, metrics.json) are handled in
the results step.
