---
spec_version: "3"
task_id: "t0122_dsi_cytoplasm_volume_nsga2"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-24T02:47:48Z"
completed_at: "2026-05-24T03:02:00Z"
---
# Step 6: Research Code

## Summary

Spawned a `/research-code` subagent that reviewed 14 prior tasks (12 cited) and wrote
`research/research_code.md` (~540 lines). Key findings: t0115 is the single canonical fork point for
the NSGA-II driver; cytoplasm volume is `sum(pi * (sec.diam/2)^2 * sec.L)` over soma
+ dendrites + AIS; evaluator-level objective swap is a one-place change in
  `BedBV3MorphProblem._evaluate`; silence guard tightens from `total_mean_spikes < 10` to
  `pd_spikes_sum < 3` (one-line change). Verificator passes 0/0.

## Actions Taken

1. Spawned a subagent to execute the `/research-code` skill against task t0122.
2. The subagent identified the t0115 source files to fork verbatim (`nsga2_driver.py`,
   `evaluator.py`, `build_top50_morphologies.py`, ~17 other modules), the two new modules to add
   (`cytoplasm_volume.py`, `cuntz_balancing_factor.py`), and the one-place objective swap.
3. The subagent ran `verify_research_code` -- PASSED with 0 errors / 0 warnings.

## Outputs

* `tasks/t0122_dsi_cytoplasm_volume_nsga2/research/research_code.md` (~540 lines)
* `tasks/t0122_dsi_cytoplasm_volume_nsga2/logs/steps/006_research-code/step_log.md`

## Key Findings (carried into planning)

1. Fork t0115 driver verbatim; minimal patches for the objective swap.
2. Cytoplasm volume computed inside `evaluate_68d_vector` from already-built MorphologyResult.
3. Cuntz balancing factor computed only in post-processing (not in optimisation loop).
4. Silence-guard tightening to `>= 3 PD spikes` is a one-line change.
5. t0120 gating verdict (rendering-only artefact) confirmed; no `_apply_asymmetry` patch needed.
6. Vast.ai setup inherits t0115's setup-remote-machine conventions; $5 per-instance watchdog under
   the $6 task cap leaves $1 buffer under the $7 Vast.ai balance.

## Issues

No issues encountered.
