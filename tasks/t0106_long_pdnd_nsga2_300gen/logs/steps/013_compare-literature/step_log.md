---
spec_version: "3"
task_id: "t0106_long_pdnd_nsga2_300gen"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-05-18T01:37:15Z"
completed_at: "2026-05-18T01:43:00Z"
---
# Step 13: compare-literature

## Summary

Compared t0106's quantitative outputs against the t0078 -> t0104 NSGA-II lineage and 7 published
papers. 19 comparison rows total (9 prior-task + 10 published) written to
`results/compare_literature.md`. Headline: t0106's 3.28% joint-pass acceptance rate is 8.2x Hay
2011's 0.40% upper bound and 33x Druckmann 2007's 0.10%, despite running on a 68-d substrate
(2.8x-5.7x higher dim than any published NSGA-II benchmark) and a ~10x lower budget. Best DSI = 1.0
/ PD = 81 Hz exceeds Trenholm 2013 mouse Hb9 DSI = 0.76 and Poleg-Polsky 2026 unconstrained ML
ceiling = 0.731. `verify_compare_literature` PASSED with 0 errors and 0 warnings.

## Actions Taken

1. Read the compare-literature skill spec and the relevant lineage / literature inputs (task.json,
   results_summary.md, results_detailed.md, research_papers.md, research_internet.md).
2. Picked the 6 lineage tasks (t0078, t0080, t0091, t0099, t0102, t0104) and 7 published anchors
   (Druckmann2007, Hay2011, Achard2006, Mohacsi2024, Trenholm2013, Oesch2005, PolegPolsky2026).
3. Wrote `results/compare_literature.md` per spec v1: tables comparing joint-pass yield, best DSI,
   best PD-rate, NSGA-II convergence behaviour, and acceptance rates. Formatted with flowmark and
   verified with `verify_compare_literature` (0 errors, 0 warnings).

## Outputs

* `tasks/t0106_long_pdnd_nsga2_300gen/results/compare_literature.md`
* This step log

## Issues

Caveats flagged in the comparison document but not blocking: (1) single GA seed without multi-seed
confirmation, (2) DSI=1.0 cells have ND firing of exactly zero — suspicious vs Trenholm 2013's 27
± 12 Hz peak ND, (3) the 2-direction protocol has no equal-protocol published precedent in DSGC
modelling, (4) operator-stop at gen 40 is a visual-plateau call, not the pre-registered Blank-Deb
threshold, (5) acceptance-rate comparisons are against extrapolated dimensional baselines, not
matched-dim fits. All five carry over to the suggestions step.
