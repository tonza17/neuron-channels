---
spec_version: "3"
task_id: "t0129_t0126_signed_dsi_real_rates_1seed"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-26T19:35:00Z"
completed_at: "2026-05-26T19:55:00Z"
---
# Step 10: teardown

## Summary

Pulled all NSGA-II artefacts from Vast.ai instance `37924958` (ssh4.vast.ai:14958) after the
seed-3517 run completed cleanly (NSGA2_EXIT=0, gen 60/60, 5760 cells evaluated, 9-cell Pareto
front, final HV=19995904075.7871 at gen 60, driver-reported active-window cost $0.6469), then
destroyed the instance via `vastai destroy instance 37924958 --yes`. Final full-lifetime cost
$0.9650 (ready_at 2026-05-26T14:46:55Z to destroyed_at 2026-05-26T19:49:52Z, 5.0492 h at
$0.1911/hr) -- 32.2% of the caller's $3.00 hard cap. `machine_log.json`,
`remote_machines_used.json`, and `costs.json` updated. Verificator
`verify_machines_destroyed.py` PASSED with 2 benign warnings (RM-W001 API-unreachable for
destroyed instances and RM-W006 no external checkpoint -- both expected for the NSGA-II
workflow per t0126's precedent).

## Actions Taken

1. Verified remote run completion via SSH: `tail -3 /root/t0129_workdir/nsga2_seed3517.log`
   showed the final `[run_seed3517] cell_params.jsonl line count: 5760` line and confirmed the
   wrapper's housekeeping ran after the seed-3517 driver exited cleanly with NSGA2_EXIT=0 at
   2026-05-26T18:45:33Z. `wc -l` on the remote cell_params.jsonl confirmed 5760 lines. Listed
   results/data/ to confirm all 7 expected JSON files were present and listed
   logs/steps/009_implementation/checkpoints/ to confirm 60 .pkl files
   (`checkpoint_seed3517_gen0001.pkl` .. `checkpoint_seed3517_gen0060.pkl`).
2. Pulled `cell_params.jsonl` (9.2 MB, 5760 lines) via `scp -r` (wrapped with run_with_logs.py)
   to `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/cell_params.jsonl`. The local
   `results/local_killed_run/cell_params_local_killed.jsonl` (10-line preserved evidence from
   the killed 4-worker local attempt) was NOT touched -- separate subdirectory, no overlap.
3. Pulled `results/data/` (7 files, 24.5 MB uncompressed) via `scp -r` to
   `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/data/`.
4. Pulled `nsga2_seed3517.log` (24 KB, 240 lines) to
   `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/nsga2_seed3517.log`.
5. Pulled `logs/steps/009_implementation/hv_trace.jsonl` (60 lines) and
   `logs/steps/009_implementation/checkpoints/` (60 .pkl files, 227 MB total) via `scp -r`.
6. Identified two JSON files in `results/data/` over the 5 MB PM-E011 threshold:
   `all_evaluations_seed3517.json` (12.5 MB) and `nsga2_checkpoint_seed3517.json` (12.4 MB).
   Compressed both in place to `.json.gz` via `gzip -9` (wrapped). Compression ratios ~3.9x:
   12.5 MB -> 3.2 MB and 12.4 MB -> 3.1 MB. Both now under the 5 MB threshold.
7. Committed Phase 1 pull: commit `8526852d` with message
   `t0129_t0126_signed_dsi_real_rates_1seed [implementation]: Pull NSGA-II results from
   Vast.ai (5760 cells, 9-cell Pareto front, gen 60/60 complete)`. 120 files added,
   14,873 insertions. Pre-commit hooks normalised trailing newlines and trimmed trailing
   whitespace on six text files (the JSONs and one ssh stdout); re-staged and the commit
   succeeded on the second attempt.
8. Captured the destroyed_at timestamp by running `date -u` immediately after the destroy
   command returned: 2026-05-26T19:49:52Z.
9. Ran `vastai destroy instance 37924958 --yes` (wrapped). The CLI returned
   `destroying instance 37924958.` with exit code 0.
10. Confirmed destruction by two independent checks:
    * `vastai show instances --raw` returned `[]` -- the account has zero remaining
      instances.
    * `vastai show instance 37924958 --raw` raised TypeError on `row['start_date']` (the
      SDK's manifestation of "instance not found": the API returns null for destroyed
      instances and the CLI handler crashes trying to subscript None when computing
      `duration`). This matches t0126's verificator-precedent for confirmed destruction.
11. Updated `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/steps/008_setup-machines/machine_log.json`:
    set `destroyed_at=2026-05-26T19:49:52Z`, `total_duration_hours=5.049167` (computed from
    `ready_at=2026-05-26T14:46:55Z` per the caller's teardown instruction -- the SKILL
    default uses `created_at` but the caller explicitly specified `ready_at`),
    `total_cost_usd=0.965008` (= `total_duration_hours * dph_total = 5.049167 * 0.19111`).
12. Wrote `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/remote_machines_used.json`
    with the t0129 machine summary; populated `duration_hours=5.049167`,
    `cost_usd=0.965008`, `destroyed_at=2026-05-26T19:49:52Z`, and a workload/note narrative
    reconciling the driver's $0.6469 (active-run only) with the $0.9650 full-lifetime
    figure.
13. Wrote `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/costs.json`: set
    `total_cost_usd=0.965008` matching the actual Vast.ai spend; itemised vast-ai instance
    cost vs. zero entries for api_calls and local_compute; added a note explaining the
    $0.318 setup+teardown idle delta vs the driver's in-flight watchdog reading; computed
    utilisation percentages (12.1% of the $8 project per-task default, 32.2% of the caller's
    $3.00 hard cap).
14. Ran
    `uv run python -m arf.scripts.verificators.verify_machines_destroyed t0129_t0126_signed_dsi_real_rates_1seed`
    via run_with_logs.py: PASSED with 0 errors and 2 warnings (RM-W001 "Cannot verify
    destruction of 37924958 -- API unreachable" -- benign per the t0126 precedent above;
    RM-W006 "Machine 37924958 ran 5.0h but no checkpoint_path is set" -- expected because
    the NSGA-II driver persists its own state via 60 .pkl checkpoints in
    `logs/steps/009_implementation/checkpoints/` and does not need an external checkpoint
    file).
15. Wrote this `step_log.md` per `arf/specifications/logs_specification.md` v3.

## Outputs

* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/cell_params.jsonl` -- 5760-line
  per-cell parameter snapshot (60 gen x 96 pop). 9.2 MB.
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/data/` -- 7 files: 5 small JSONs
  (algorithm_config, evaluation_seeds, init_pop, hv_trajectory, pareto_front) and 2
  gzip-compressed JSONs (all_evaluations, nsga2_checkpoint). 6.4 MB total.
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/nsga2_seed3517.log` -- 240-line
  wrapper log including the final
  `[seed 3517 gen 60] HV=19995904075.7871 pop_size=96 cost_so_far=$0.6468 elapsed=12184s`
  line and the seed-3517 driver's exit summary.
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/steps/009_implementation/hv_trace.jsonl`
  -- 60 entries, one per generation.
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/steps/009_implementation/checkpoints/`
  -- 60 .pkl files (checkpoint_seed3517_gen0001.pkl .. checkpoint_seed3517_gen0060.pkl).
  227 MB total. NOTE: many of these exceed the PM-E011 5 MB threshold (the last ~30
  generations); they match the t0126 precedent (t0126 has the same .pkl-per-generation
  pattern uncompressed) and will be flagged as warnings rather than errors at PR pre-merge.
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/steps/008_setup-machines/machine_log.json`
  -- populated `destroyed_at`, `total_duration_hours`, `total_cost_usd`.
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/remote_machines_used.json` --
  finalised machine summary.
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/costs.json` -- final cost
  breakdown.
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/steps/010_teardown/step_log.md` --
  this log.

## Issues

The verificator emitted two warnings, both benign and matching the t0126 precedent:
RM-W001 "Cannot verify destruction of 37924958 -- API unreachable" is a quirk of the
verificator's strategy because Vast.ai returns null for destroyed instances, which the
underlying CLI handler crashes on with a TypeError when computing duration. The
authoritative check is the empty `vastai show instances --raw` output (`[]`) which
confirms instance 37924958 is no longer in the account. RM-W006 "Machine 37924958 ran
5.0h but no checkpoint_path is set" is also benign -- NSGA-II uses 60 per-generation
.pkl checkpoints in `logs/steps/009_implementation/checkpoints/` for resume, not an
external heartbeat file. Zero errors.

PM-E011 deferred concerns: the `.pkl` checkpoints in
`logs/steps/009_implementation/checkpoints/` (up to 7.6 MB for `gen0060`) and the
9.2 MB `results/cell_params.jsonl` will be flagged as warnings by `verify_pr_premerge`
at PR time. Per the caller's teardown instruction, only the JSON files in
`results/data/` were compressed in place. The .pkl checkpoints follow the t0126
precedent (uncompressed, accepted at merge) and `cell_params.jsonl` is the
deliverable-of-record for the per-cell signed-DSI / real-rate evidence. The reporting
stage can decide whether to compress these or document the warnings.

Total cost $0.9650 is 56% of the $1.72 plan estimate -- substantially under because the
NSGA-II run completed in 3.385 h vs t0126's 5.22 h (the t0129 evaluator changes did not
add measurable compute; per-cell jsonl writes were negligible I/O) plus a shorter
post-run idle window (1.07 h vs t0126's 1.4 h).
