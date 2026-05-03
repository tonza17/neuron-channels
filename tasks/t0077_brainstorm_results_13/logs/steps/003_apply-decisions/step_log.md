---
spec_version: "3"
task_id: "t0077_brainstorm_results_13"
step_number: 3
step_name: "apply-decisions"
status: "completed"
started_at: "2026-05-03T12:10:00Z"
completed_at: "2026-05-03T12:35:00Z"
---
# Step 3 — Apply Decisions

## Summary

Wrote sixteen correction files under `corrections/`, all `update` actions setting
`status: "rejected"`. Four reject the t0076-derived high-priority suggestions covered by the new
t0078 task (S-0076-01, S-0076-02, S-0076-03, S-0076-05). One rejects S-0024-03 (medium priority, Bed
B AIS library asset, also covered by t0078). Eleven reject the stale from-scratch-family
high-priority suggestions (t0052 - t0059 lineage) which the project has pivoted away from. Cancelled
t0045 (CoreNEURON-on-GPU benchmark) by editing its `task.json` to set `status: "cancelled"`. Created
the new not-started t0078 task folder via `/create-task` with source_suggestion `S-0076-02`,
dependencies on t0024 / t0069 / t0076, and a detailed `task_description.md` describing the bundled
MOBO scope (AIS + tier-stratification + slow Kv-AHP + implementation fixes).

## Actions Taken

1. Wrote four correction files rejecting t0076-derived suggestions covered by t0078:
   `suggestion_S-0076-01.json` (tier-stratified channel densities), `suggestion_S-0076-02.json`
   (AIS-augmented Bed B MOBO; primary scope), `suggestion_S-0076-03.json` (qLogNEHVI / GP
   normalisation / NEURON re-init fixes), `suggestion_S-0076-05.json` (slow Kv-AHP via SK_E2 with
   extended Ca-binding). Each uses `correcting_task: "t0077_brainstorm_results_13"`,
   `target_kind: "suggestion"`, `action: "update"`, `changes: {"status": "rejected"}`, with
   rationale identifying t0078 as the covering task.
2. Wrote one correction file rejecting the medium-priority `suggestion_S-0024-03.json` (Van Wart +
   Werginz AIS overlay on the deRosenroll morphology); rationale identifies t0078 as the covering
   task because the Bed B AIS section is built as part of the bundled MOBO scope and registered as a
   new library asset.
3. Wrote eleven correction files rejecting the stale from-scratch-family high-priority suggestions:
   `suggestion_S-0052-01.json`, `suggestion_S-0052-02.json`, `suggestion_S-0054-02.json`,
   `suggestion_S-0055-02.json`, `suggestion_S-0055-03.json`, `suggestion_S-0057-06.json`,
   `suggestion_S-0059-01.json`, `suggestion_S-0059-02.json`, `suggestion_S-0059-03.json`,
   `suggestion_S-0065-02.json`, `suggestion_S-0066-02.json`. Each rationale identifies the project
   pivot away from the from-scratch family (t0052 - t0059) toward the deposited Bed A (t0008) and
   Bed B (t0024) substrates, and notes that the from-scratch family is stuck in a binary regime that
   none of these eleven follow-ups would unblock at this point in the project.
4. Cancelled t0045 by editing `tasks/t0045_coreneuron_vastai_speedup_benchmark/task.json` to set
   `"status": "cancelled"`. Verified that the task was previously `not_started` (no files outside
   the cancellation-edit; no in-flight branch).
5. Created `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/` via `/create-task` with valid `task.json`
   (status `not_started`, source_suggestion `S-0076-02`, dependencies on t0024 / t0069 / t0076,
   expected_assets `{"library": 1}`, task_types `["build-model", "experiment-run"]`) and a detailed
   `task_description.md` describing the bundled MOBO scope, parameter dimensionality, slow-AHP
   implementation choice, fresh-Sobol restart, qLogNEHVI / GP-normalise / NEURON re-init fixes,
   compute estimate, and pass criteria.

## Outputs

* `corrections/suggestion_S-0024-03.json` — reject (covered by t0078; Bed B AIS library asset)
* `corrections/suggestion_S-0052-01.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0052-02.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0054-02.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0055-02.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0055-03.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0057-06.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0059-01.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0059-02.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0059-03.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0065-02.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0066-02.json` — reject (stale from-scratch family)
* `corrections/suggestion_S-0076-01.json` — reject (covered by t0078; tier-stratification)
* `corrections/suggestion_S-0076-02.json` — reject (covered by t0078; AIS-augmented MOBO primary)
* `corrections/suggestion_S-0076-03.json` — reject (covered by t0078; implementation fixes folded
  in)
* `corrections/suggestion_S-0076-05.json` — reject (covered by t0078; slow Kv-AHP folded in as
  MOBO parameter)
* `tasks/t0045_coreneuron_vastai_speedup_benchmark/task.json` — `status` updated to `"cancelled"`
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/` — full not-started task folder with `task.json` and
  `task_description.md`

## Issues

No issues encountered.
