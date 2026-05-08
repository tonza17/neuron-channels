---
spec_version: "1"
task_id: "t0094_brainstorm_results_19"
date_completed: "2026-05-08"
status: "complete"
---
# Results Summary: Brainstorm Session 19

## Summary

Nineteenth strategic brainstorm, run on 2026-05-08 immediately after t0093
(`resweep_and_t0090_correction`) merged with 60/60 cells STABLE-firing under the t0092 patched
generator and `C-0093-01` correction overlay in place. The researcher's directive was direct: launch
the morphology-extended NSGA-II optimisation now. The session updated t0091
(`morphology_extended_nsga2_v1`) in place — added t0092 + t0093 to dependencies, swapped the
generator import path to `tasks.t0092_..code.morphology_generator_fix.generate_fixed_morphology`,
refreshed the Bed-B-anchor source to t0093's verified post-fix reproducibility point, and extended
cross-references — and rejected two suggestions falsified by the t0093 outcome (S-0092-03,
S-0090-04). Project budget $20.00; $15.55 spent; **$4.45 remaining** before t0091; estimated
**$0.95–1.45 buffer remaining** after t0091 with the existing $4.00 cost watchdog.

## Session Overview

Date: 2026-05-08. Triggered by the t0093 merge confirming the t0092 fix at scale: 60/60 STABLE,
56/60 with PD-rate>0, 21/60 with DSI>0.5, total spikes 16,107 vs 0 pre-fix, 0 regressions. The
researcher led with three substantive questions before the launch directive:

1. "Explain me in simple words what was the bug with new morphologies generation and how you fixed
   it? How do we know that everything is fine? Also, did all morphologies showed toughly the same
   DSI or did they differ?" — answered with the soma-pt3d collapse explanation, the
   `generate_fixed_morphology` z-axis re-emission fix, the three-layer evidence stack (unit tests
   + hand-coded gate + 60-cell re-sweep), and the per-cell DSI spread (mean 0.32–0.35, range from
     DSI=0 to DSI=1.0, with the DSI=1.0 cells flagged as low-firing-rate statistical artefacts).
2. "where can I find DSI for each individual cell from these 60 cells?" — answered with the path
   `tasks/t0093_resweep_and_t0090_correction/data/post_fix_verification_summary.json` and noted the
   embedded examples in `results_detailed.md` lines 171-308.
3. "well it's time to run an optimisation. Update the t0091 if you haven't yet done so and run it.
   How much budget do we need? Is there enough?" — the launch directive plus budget question.

The budget answer was: $4.45 remaining, t0091 plan estimate $3.00–3.50, watchdog hard cap $4.00,
post-t0091 buffer $0.95–1.45 (best/realistic) or $0.45 (worst case at watchdog cap). Yes, enough,
but no headroom for a second remote-compute task in this budget cycle.

Two clarifying multi-choice questions resolved the launch surface:

* **NMDA calibration**: keep S-0090-03 (G.2 NMDA units calibration) as a separate post-t0091 task,
  not folded into t0091 as Phase A.5. Researcher chose the recommended option; rationale: keep t0091
  launch simple, accept potential re-score after calibration.
* **Cost watchdog**: keep at $4.00 as planned. Researcher chose the recommended option; rationale:
  matches existing plan, gives NSGA-II room to hit 8 generations.

## Decisions

1. **Update t0091** (`morphology_extended_nsga2_v1`) in place. Direct edit allowed because t0091 is
   `not_started`. Changes:

   * `task.json`: add `t0092_diagnose_morphology_generator_silence` and
     `t0093_resweep_and_t0090_correction` to `dependencies`; refresh `short_description` to mention
     the t0092-patched generator instead of t0090.
   * `task_description.md` Motivation section: rewrite to acknowledge the t0090 bug, t0092
     diagnosis, t0093 fix-validation, and `C-0093-01` correction overlay.
   * `task_description.md` In Scope: replace "t0090 procedural generator" with "t0092 patched
     procedural generator (`generate_fixed_morphology`, canonicalised by C-0093-01)".
   * `task_description.md` Phase A anchor 1 source: replace "t0090 Phase F validated point" with
     "t0093 patched-generator Bed-B reproducibility (43.6 Hz PD-rate post-fix on the BedB-equivalent
     point)".
   * `task_description.md` Phase B per-cell evaluation: explicit import statement
     `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
   * `task_description.md` Risks and Fallbacks: refresh "Generator instability under NSGA-II
     mutation" to reference t0093's 60/60 STABLE evidence.
   * `task_description.md` Cross-References: extend with t0092, t0093, t0094 entries; mark t0090 as
     superseded.

2. **Reject S-0092-03**
   (`Issue a correction overlay against t0090 marking the procedural generator as superseded by the t0092 fix`)
   as covered. t0093's `C-0093-01` correction is in place and verified; suggestion is operationally
   fulfilled.

3. **Reject S-0090-04**
   (`Tighten t0091 LHS morphology bounds using the 9 STABLE cells from the t0090 diversity sweep`)
   as premise-falsified. t0093's patched-generator re-sweep made 60/60 cells STABLE-firing; the 9
   STABLE pool was a soma-pt3d-collapse artefact.

4. **Keep t0091 cost watchdog at $4.00** matching the existing plan.

5. **Keep S-0090-03** (G.2 NMDA units calibration) as a separate post-t0091 task, not folded into
   t0091.

6. **No new tasks created.** t0091 is launched as-is by execute-task in a separate worktree after
   this brainstorm merges.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 0 |
| Tasks updated | 1 (t0091_morphology_extended_nsga2_v1: deps + short_description + task_description.md) |
| Tasks cancelled | 0 |
| Suggestions rejected | 2 (S-0092-03, S-0090-04) |
| Suggestions reprioritised | 0 |
| Corrections written | 2 |
| New suggestions created | 0 |
| Answer assets created | 0 |
| Session duration | ~30 minutes interactive |
| Session cost | $0.00 |
| Estimated cost of commissioned tasks | $3.00–3.50 (t0091 only) |

## Verification

* `verify_task_file.py t0094_brainstorm_results_19` — target 0 errors.
* `verify_task_file.py t0091_morphology_extended_nsga2_v1` — target 0 errors after the update.
* `verify_corrections.py t0094_brainstorm_results_19` — target 0 errors for 2 correction files.
* `verify_suggestions.py t0094_brainstorm_results_19` — target 0 errors (empty array).
* `verify_logs.py t0094_brainstorm_results_19` — target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_pr_premerge.py t0094_brainstorm_results_19 --pr-number <N>` — target 0 errors.

## Next Steps

1. **t0091 execution** is the immediate follow-up: invoke
   `/execute-task t0091_morphology_extended_nsga2_v1` in a fresh worktree. Expected wall-clock
   ~14–16 hours Vast.ai EPYC 7B13; ~$3.00–3.50 cost. Output: 68-d Pareto-front predictions asset
   \+ biological-plausibility answer asset.

2. **Decision point after t0091 completes**:

   * If morphology extension opens biologically-plausible joint-pass cells, this confirms morphology
     as a functional DS mechanism on top of the channel mechanism. Opens cross-bed validation
     follow-ups (S-0070-01 PD/ND encoding harmonisation; Bed A morphology-extended NSGA-II).
   * If anchor 3 (PD-asymmetric) is preserved more than anchor 4 (ND-asymmetric), strong evidence
     for soma-displacement-toward-PD as a functional DS mechanism (Schachter 2010, Trenholm 2013).
   * If morphology pegs at near-Bed-B defaults across the entire Pareto, motivates Option G
     (NeuroMorpho real-cell library + categorical selector + parametric deformation) as a future
     task.

3. **Post-t0091 follow-ups** to consider in the next brainstorm:

   * **S-0086-01** (NSGA-II re-run with tightened NMDA bounds, ~$1.50) — high priority, fits the
     ~$0.95–1.45 buffer if t0091 negative result motivates revisiting 54-d search.
   * **S-0090-03** (G.2 NMDA units calibration) — post-t0091, local-only $0 incremental.
   * **S-0090-02** (NaP-knockout sweep at scale on local 64-core) — local-only $0 incremental.
   * **S-0070-01** (harmonise PD/ND encoding across Bed A and Bed B) — high priority, infra work,
     no compute.
