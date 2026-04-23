---
spec_version: "3"
task_id: "t0036_rerun_t0030_halved_null_gaba"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-23T21:01:42Z"
completed_at: "2026-04-23T21:09:00Z"
---
## Summary

Spawned a research-code subagent that located the `GABA_CONDUCTANCE_NULL_NS = 12.0` constant at
t0022/code/constants.py:84 and identified the exact call sites in t0022/code/run_tuning_curve.py
(lines 77, 327, 447, 585, 593). Subagent specified a pre-import monkey-patch override strategy: set
`_t0022_constants.GABA_CONDUCTANCE_NULL_NS = 6.0` before importing run_tuning_curve, AND rebind the
local value to avoid the `null_weight_us` assertion inside schedule_ei_onsets. Null-Hz pre-condition
gate documented (mean null-Hz at 1.0× must be ≥ 0.1 Hz).

## Actions Taken

1. Spawned general-purpose subagent with /research-code skill instructions and a focused prompt
   covering t0022 driver / GABA constant location / t0030 workflow copy / override strategy.
2. Subagent traced the GABA constant through t0022's codebase (5 call sites), documented the
   monkey-patch override semantics, confirmed the ratio-dependent assertion that must also be
   rebound, and wrote `research/research_code.md` covering all required sections.
3. Subagent ran flowmark and verify_research_code.py wrapped in run_with_logs.py; 0 errors, 0
   warnings.

## Outputs

* `tasks/t0036_rerun_t0030_halved_null_gaba/research/research_code.md`
* `tasks/t0036_rerun_t0030_halved_null_gaba/logs/commands/...` (run_with_logs entries)
* `tasks/t0036_rerun_t0030_halved_null_gaba/logs/steps/006_research-code/step_log.md` (this file)

## Issues

No issues encountered. Critical finding: the monkey-patch must happen BEFORE
`from tasks.t0022...run_tuning_curve import ...` and must rebind BOTH the module attribute and any
local import, because `schedule_ei_onsets` asserts
`null_weight_us == GABA_CONDUCTANCE_NULL_NS * 1e-3`. This is the single riskiest step in the task.
