---
spec_version: "3"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
step_number: 7
step_name: "planning"
status: "completed"
started_at: "2026-05-03T14:21:12Z"
completed_at: "2026-05-03T14:35:00Z"
---
# Step 7 — Planning

## Summary

Spawned a `/planning` subagent to synthesise the three research files (papers, internet, code) into
`plan/plan.md`. The subagent produced a 6,760-word plan with 22 REQ items, 14 numbered
implementation steps grouped into 3 milestones, 14 verification criteria, a 47-d parameter-space
breakdown, and a $2.10 - $2.86 (rounded $3.50 ceiling) cost estimate that fits comfortably under the
researcher-authorised $2.50 - $4.00 envelope. Verificator passes 0 errors / 0 warnings. The plan
adopts a **two-tier pass criterion** in response to the research-internet finding: **primary** DSI
>= 0.4 AND PD rate >= 10 Hz (anchored to Rivlin-Etzion 2012 mouse DSGC paired measurements),
**stretch** DSI >= 0.4 AND PD rate >= 30 Hz (the original brainstorm target, retained for backward
comparability). The plan resolves the qLogNEHVI / Normalize / NEURON re-init bug fixes, the
t78-namespace SUFFIX rename, the cadecay collision avoidance, and the TSTOP_MS update from 1000 to
1400 ms.

## Actions Taken

1. Ran `prestep planning`.
2. Spawned a `/planning` subagent with explicit context: researcher-authorised $2.50 - $4.00
   compute, 47-d parameter space, fresh Sobol restart, qLogNEHVI mandatory, and the critical "30 Hz
   vs 10 Hz" pass-criterion contradiction surfaced by research-internet. The subagent read all three
   research files plus the task description and produced `plan/plan.md` with all 11 mandatory
   sections.
3. Verified `plan/plan.md` exists with all required sections.
4. Ran `verify_plan.py` via `run_with_logs.py`: PASSED with 0 errors, 0 warnings.

## Outputs

* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/plan/plan.md` — 6,760-word implementation plan with 22
  REQ items, 14 steps, 14 verification criteria, 47-d parameter breakdown, $2.10 - $2.86 cost
  estimate, two-tier pass criterion (DSI >= 0.4 AND PD rate >= 10 Hz primary; >= 30 Hz stretch), AIS
  construction strategy, SK_E2 vendoring with `tau_ca_multiplier` parameter, qLogNEHVI migration
  with `Normalize` input transform, and 12 documented risks with mitigations.
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/007_planning/step_log.md` — this step log.

## Issues

The plan flags four unresolved scoping questions that the researcher should be aware of before
implementation:

1. **AIS proximal-subsegment Nav modelling**: the plan uses HHst basal Na+K plus a single Nav1.6
   instance at proximal-specific (lower) density as a stand-in for biologically distinct Nav1.1 /
   Nav1.2. A more faithful implementation would vendor a separate Nav1.2 MOD; if adopted, parameter
   space grows from 47 d to 48 d.
2. **AIS length and diameter as free MOBO parameters or fixed**: plan currently fixes them at
   default values (30 um length, 0.8 um diameter) to keep the count at 47. Free-parameter variant is
   49 d.
3. **`tau_ca_multiplier` upper bound**: plan extends to `[1, 200x]` based on Larsson 2013 sAHP
   timescale (1 - 3 s) versus the researcher-stated `[1, 20x]` (5 - 100 ms). The 200x extension is
   the more defensible choice but the researcher should confirm.
4. **`results/costs.json` and `results/remote_machines_used.json` ownership**: plan treats these as
   orchestrator-owned (written by the orchestrator's `setup-machines` / `teardown` / `results`
   steps), with the implementation step only emitting raw telemetry to its log.

These four are minor scoping refinements; none of them blocks the implementation step. They are
documented so the researcher can adjust at the pause-point checkpoint between this step and the
setup-machines step.
