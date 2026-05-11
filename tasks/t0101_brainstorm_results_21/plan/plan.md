# Plan: Brainstorm Session 21

## Objective

Record the strategic decisions reached during the Poleg-Polsky 2026 deep-dive session: commission
the t0102 NSGA-II follow-up, log three new suggestions, and document the project budget bump already
committed to main.

## Approach

Pure decision-recording task. Follow `arf/skills/human-brainstorm/SKILL.md` Phases 4-6: scaffold
brainstorm-results task folder, record decisions in `results/`, run verificators, push and merge.

## Cost Estimation

$0.00. No remote machines, no API calls, no compute beyond the local verificators and Vast.ai
metadata commands.

## Step by Step

1. Scaffold task folder with mandatory subdirectories and placeholder files.
2. Write `task.json`, `task_description.md`, `step_tracker.json`.
3. Populate research placeholders (no research performed).
4. Write `results/results_summary.md`, `results/results_detailed.md`, `results/suggestions.json`,
   `results/metrics.json`, `results/costs.json`, `results/remote_machines_used.json`.
5. Write per-step `logs/steps/NNN_*/step_log.md` files.
6. Write `logs/session_log.md` with the full Poleg-Polsky discussion transcript.
7. Run `verify_task_file`, `verify_corrections`, `verify_suggestions`, `verify_logs`.
8. Rebuild overview via `materialize.py`.
9. Commit, push, open PR, run pre-merge verificator, merge.

## Remote Machines

None.

## Assets Needed

None. The Poleg-Polsky 2026 PDF
(`tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/files/polegpolsky_2026_ml-motion-primitives.pdf`)
was the primary source for the discussion; it is already in the project.

## Expected Assets

None. Brainstorm tasks produce decisions, not assets.

## Time Estimation

15-20 minutes (decision-recording only; no compute).

## Risks & Fallbacks

* Risk: `verify_logs` rejects custom step names with `TS-W001`. Mitigation: this warning is
  documented as expected for brainstorm tasks in the skill spec.
* Risk: `verify_task_file` flags empty `expected_assets`. Mitigation: this warning is documented as
  expected for brainstorm-results tasks.

## Verification Criteria

* All four verificators (`verify_task_file`, `verify_corrections`, `verify_suggestions`,
  `verify_logs`) pass with zero errors.
* `results/suggestions.json` validates against the suggestions specification and lists exactly three
  new suggestions (1 high, 2 medium).
* `logs/session_log.md` contains a full record of the Poleg-Polsky discussion sufficient for a
  future reader to reconstruct what was decided and why.
