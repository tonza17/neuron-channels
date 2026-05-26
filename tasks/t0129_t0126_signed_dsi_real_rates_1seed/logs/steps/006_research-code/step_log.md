---
spec_version: "3"
task_id: "t0129_t0126_signed_dsi_real_rates_1seed"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-26T12:41:50Z"
completed_at: "2026-05-26T12:57:30Z"
---
# Step 6: research-code

## Summary

Surveyed t0126's evaluator, NSGA-II driver, run-script wrapper, smoke gate, metrics builder, and all
downstream consumers (build_predictions_assets, build_results, post_run_analysis,
t0124_vs_t0126_comparator) to map exactly what the t0129 fork must change. Confirmed that the DSI
swap is surgical (one helper, two call sites), that `pd_rate_hz` is already computed correctly in
the t0126 evaluator (the `=40` placeholder came from a post-run synthesis pass, not the live run),
and that the `T0126_CELL_TRACE_JSONL` env-var dropout is the root cause of the diagnostic gap. The
research file enumerates every site touched by the field rename `dsi_vector_sum -> dsi_signed`
(across 8 files) and lists the non-negotiable invariants (`_POOL_RESTART_EVERY = 10`, HV-plateau
auto-stop disabled, launch via `run_seed3517.sh` wrapper).

## Actions Taken

1. Ran `prestep research-code` to mark the step in_progress.
2. Spawned a subagent to execute the `/research-code` skill end-to-end (read SKILL.md, read t0126
   evaluator + driver + downstream code, survey libraries and prior memories, write
   `research/research_code.md`, run the verificator).
3. Subagent wrote `research/research_code.md` with line-anchored references to every modification
   site in the t0126 codebase plus explicit "do-not-touch" boundaries for `tasks/t0127_*` and
   `tasks/t0128_*`.
4. Subagent ran `verify_research_code` (wrapped in `run_with_logs`); verificator returned 0 errors,
   0 warnings.

## Outputs

* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/research/research_code.md`
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/steps/006_research-code/step_log.md`
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/logs/commands/00X_*.{json,stdout.txt,stderr.txt}`
  (command transcripts from the subagent)

## Issues

No issues encountered. Key research finding the planner must internalise: `dsi_vector_sum` and
signed antipodal DSI are numerically identical for the positive-PD-dominant case on the antipodal
pair (because `|PD - ND| = PD - ND` when `PD >= ND`), so the smoke gate's value assertions on the
fixed reference cell carry over unchanged; only cells with `PD < ND` see a behaviour change (now
report negative DSI instead of positive magnitude).
