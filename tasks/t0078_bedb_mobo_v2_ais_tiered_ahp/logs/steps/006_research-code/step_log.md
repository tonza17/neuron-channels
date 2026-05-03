---
spec_version: "3"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-03T14:07:55Z"
completed_at: "2026-05-03T14:25:00Z"
---
# Step 6 — Research Code

## Summary

Spawned a `/research-code` subagent to audit the prior-task code that t0078 will fork or extend. The
subagent identified ~2,500 LOC of reusable code from t0076 (BoTorch loop, ProcessPoolExecutor trial
driver, Vast.ai launcher, plot_pareto, recorder, trial_helpers), the t0069 AIS attachment
architecture (one extend script + constants), the t0074 SK_E2 MOD as the slow-AHP source, the three
runtime libraries to declare (`de_rosenroll_2026_dsgc`, `tuning_curve_loss`, `tuning_curve_viz`),
the exact line numbers for the qLogNEHVI / Normalize / NEURON re-init fixes, and six code-level
surprises the planning step must address (including the `cadecay.mod` collision avoidance rule, the
`Exp2NMDA name already exists` non-idempotent loader trap, a TSTOP_MS update from 1000 to 1400 ms to
match the project standard mode trio, and an `os.chdir` quirk in t0024's HOC template loading).
Verificator passed 0 errors / 0 warnings.

## Actions Taken

1. Ran `prestep research-code`.
2. Spawned a `/research-code` subagent. The subagent enumerated t0076 / t0024 / t0069 / t0074 /
   t0011 / t0012 code, identified import vs copy strategy per the cross-task rule (libraries
   imported, non-library code copied), located the three implementation fix sites at specific line
   numbers, and surfaced project-level limitations (no library or answer aggregator exists).
3. Verified `research/research_code.md` exists with all six required sections.
4. Ran `verify_research_code.py` via `run_with_logs.py`: PASSED with 0 errors, 0 warnings.

## Outputs

* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/research/research_code.md` — code-grounded research
  audit identifying every prior-task module the t0078 implementation will reuse, the exact fix sites
  for the three t0076 implementation defects, the SK_E2 → SK_E2-with-extended-Ca-binding vendoring
  strategy, and six implementation traps to avoid (cadecay collision, Exp2NMDA re-init, TSTOP_MS
  update, os.chdir cwd quirk, tier mapping, Vast.ai compile pattern).
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/006_research-code/step_log.md` — this step
  log.

## Issues

No blocking issues. The library and answer aggregators referenced by the skill do not exist in this
project (only 8 aggregators are present); the subagent fell back to direct filesystem scan of
`tasks/*/assets/library/*/details.json`. This is a project-level limitation flagged for a potential
future framework PR; out of scope for t0078 itself.
