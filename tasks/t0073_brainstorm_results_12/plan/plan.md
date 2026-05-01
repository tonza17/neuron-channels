# Plan: Brainstorm Results Session 12

## Objective

Run an interactive strategic brainstorming session on 2026-05-01 after t0070 / t0071 / t0072 all
completed; act on two convergent gaps in the t0067-t0069 voltage-gated-channel arc on Bed A — the
unmeasured tuning-width effect of channel addition (t0067 only measured DSI at PD and ND), and the
absence of any DSGC + AIS configuration that simultaneously contains all biologically-present AIS
channels and produces DSI in [0.3, 0.95] with peak rate in [5, 50] Hz; commission two new tasks that
together close those gaps; reject nine covered or duplicate suggestions; reprioritise three
high-priority suggestions to medium.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, read every results summary
for tasks completed since brainstorm 11 (t0059-t0072), present an independent priority reassessment
of the 20 high-priority active uncovered suggestions, conduct the three-round discussion (two new
tasks; suggestion cleanup; confirmation), scaffold the brainstorm-results folder, write twelve
correction files, and create two new not-started task folders via the `/create-task` skill.

## Cost Estimation

No paid services. No remote compute. Local CPU only. Zero dollar cost.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read `results_summary.md` for
   t0059 through t0072; rebuild `overview/`.
2. Form an independent reassessment of the 20 high-priority active uncovered suggestions, focusing
   on those covered by the t0065 / t0066 shunting-inhibition discovery, the t0067 / t0068 / t0069
   channel arc, and direct duplicates between S-0065-01 and S-0066-02.
3. Present project state and reassessed priorities to the researcher.
4. Three-round discussion: agree on the t0074 channel-tuning-width-on-Bed-A scope (8 channels at 3
   densities plus baseline; BK / SK / Kv7 vendored); agree on the t0075 biologically-realistic AIS
   one-axis sweep design ({HHst, Nav1.6, Kv3, Kv7} channel set; 8 sweep axes; Stage 1 baseline
   calibration plus Stage 2 sweep); agree on nine rejections plus three reprioritisations; explicit
   go-ahead.
5. Scaffold `tasks/t0073_brainstorm_results_12/` with full folder structure.
6. Write twelve suggestion-correction files under `corrections/`: nine `update` actions setting
   `status: "rejected"`, three `update` actions setting `priority: "medium"`.
7. Create t0074 (`channel_tuning_width_bed_a`) folder via `/create-task`.
8. Create t0075 (`bio_realistic_ais_param_sweep`) folder via `/create-task` with t0074 listed as a
   dependency for the Kv7 vendoring.
9. Write step logs, session log, and results files.
10. Capture session transcripts via `capture_task_sessions`.
11. Run all relevant verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
    `verify_suggestions`).
12. Commit, push branch, open PR, run pre-merge verificator, merge.

## Remote Machines

None.

## Assets Needed

None. The brainstorm task itself produces no assets.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 55 min of interactive discussion plus 35 min of scaffolding, correction authoring, and
child-task creation plus 25 min of verification, PR, and merge.

## Risks & Fallbacks

* **Task index drift mid-session**: a parallel session merged t0072 to main while this brainstorm
  was running. Mitigation: re-run the task aggregator before reserving the brainstorm task index;
  rename branch and folder if a collision is detected.
* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **Vendoring overhead drift on t0074**: the BK / SK / Kv7 MOD vendoring is the largest single cost
  in t0074. If vendoring proves more disruptive than estimated (e.g., un-zeroing CaL / CaT in Bed
  A's `init_active` breaks t0067 baseline regression beyond the 1e-3 tolerance), t0074 can be split
  at planning time without affecting the brainstorm task itself.

## Verification Criteria

* `verify_task_file.py t0073_brainstorm_results_12` passes with 0 errors.
* `verify_logs.py t0073_brainstorm_results_12` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance).
* `verify_corrections.py t0073_brainstorm_results_12` passes with 0 errors for all 12 correction
  files.
* `verify_suggestions.py t0073_brainstorm_results_12` passes with 0 errors (empty array).
* The two new child tasks (t0074, t0075) exist on disk with valid `task.json`.
* `verify_task_file.py` passes for both t0074 and t0075.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
