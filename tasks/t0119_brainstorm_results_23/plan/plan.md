# Plan: Brainstorm Session 23

## Objective

Resolve the morphology-generator geometry concern surfaced by the researcher (soma appears
disconnected from dendrites in t0115 top-50 morphology grid), commission the next optimisation wave
gated on that diagnostic, write a canonical 5-seed substrate-rate report, and aggressively prune the
high-priority suggestion backlog.

## Approach

1. Aggregate project state (tasks, suggestions, costs) and read recent task results.
2. Trace the morphology generator code path end-to-end: `_apply_asymmetry` →
   `_materialise_neuron_sections` → synapse placement (`_section_midpoint_xy`) → arrival-time
   projection (`_bar_arrival_times` against `origin_xy`).
3. Present project state and trace findings to the researcher.
4. Discuss with the researcher in three structured rounds: gating diagnostic + new NSGA-II
   direction, suggestion cleanup, confirmation.
5. Apply decisions: create the brainstorm task folder, the 3 child tasks (geometry audit, 5-seed
   report, cytoplasm-volume NSGA-II), and 30 correction files.
6. Record the session in step logs and the session transcript.

## Cost Estimation

This task: $0. Commissions 3 child tasks:

* `t0120_morph_generator_geometry_audit` — <$0.10 (local analysis only).
* `t0121_5seed_substrate_rate_canonical_report` — <$0.20 (local write-up).
* `t0122_dsi_cytoplasm_volume_nsga2` — ~$4-8 (one Vast.ai EPYC NSGA-II run, $8 cap).

Total commissioned: ~$4-8 of $37 remaining budget.

## Step by Step

1. Run aggregators and read recent `results_summary.md` files for t0112-t0118.
2. Trace the morphology generator code path; identify which xy coordinates the simulation actually
   reads.
3. Materialise the overview so the latest state is browsable on GitHub.
4. Present project state plus an independent priority reassessment.
5. Round 1: propose gating geometry audit; researcher confirms with scope adjustment (15-20 cells,
   not 5).
6. Round 1 (continued): propose the cytoplasm-volume NSGA-II run + 5-seed canonical report.
7. Round 2: propose aggressive suggestion cleanup (8 rejects + 21 downgrades).
8. Round 3: confirm decision list.
9. Phase 4: create this brainstorm task folder.
10. Phase 5: create 3 child tasks via `/create-task`; write 30 correction files.
11. Phase 6: write results, step logs, session transcript, capture sessions, verificators, push, PR,
    pre-merge verify, merge.

## Remote Machines

None for the brainstorm task. `t0122_dsi_cytoplasm_volume_nsga2` will provision one Vast.ai EPYC
instance when it executes.

## Assets Needed

None.

## Expected Assets

None. Brainstorm-only task.

## Time Estimation

Brainstorm session: ~2 hours. Child task t0120 geometry audit: ~30 min local. Child task t0121
5-seed report: ~1 hour local. Child task t0122 cytoplasm-volume NSGA-II: ~6-12 hours wall-clock on
Vast.ai.

## Risks & Fallbacks

* If `/create-task` fails to claim the next index, retry once; if it still fails, manually create
  the folder following `arf/specifications/task_file_specification.md`.
* If the geometry audit (t0120) reveals a real geometry bug, t0122 will be cancelled and a
  framework-level decision on whether to patch `_apply_asymmetry` and re-run all 68-d NSGA-II
  lineage tasks (t0091, t0099, t0102, t0104, t0106, t0112-t0115) must be made in a follow-up
  brainstorm session.
* If verificators surface unexpected errors at the finalize step, fix and re-run; do not commit with
  errors.

## Verification Criteria

* `verify_task_file t0119_brainstorm_results_23` passes with 0 errors.
* `verify_corrections t0119_brainstorm_results_23` passes with 0 errors (30 corrections written).
* `verify_suggestions t0119_brainstorm_results_23` passes with 0 errors (no new suggestions).
* `verify_logs t0119_brainstorm_results_23` passes with 0 errors (warnings LG-W005, LG-W007, LG-W008
  may be present and are non-blocking for a pure-planning brainstorm).
* `verify_pr_premerge t0119_brainstorm_results_23 --pr-number <N>` passes with 0 errors before
  merge.
