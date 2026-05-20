---
spec_version: "3"
task_id: "t0113_t0106_seed2247_replicate"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-05-20T02:34:32Z"
completed_at: "2026-05-20T02:39:00Z"
---
# Step 13: compare-literature

## Summary

Spawned the compare-literature subagent to compare t0113's seed-2247 outcome against published DSGC
and NSGA-II references plus the t0106 / t0112 prior-task baselines. The subagent wrote
`results/compare_literature.md` (286 lines, Flowmark-normalised) covering four comparison families:
prior-task replication delta, 3-seed substrate-rate vs Hay 2011 / Druckmann 2007, HV-plateau gen vs
Mohacsi 2024 NSGA-II convergence range, and best legit DSI vs DSGC biological references (Trenholm
2013, Oesch 2005, Poleg-Polsky 2026). Verificator passes with zero errors and zero warnings.

## Actions Taken

1. Spawned a `/compare-literature` subagent following `arf/skills/compare-literature/SKILL.md`.
2. The subagent loaded t0106 / t0112 / t0113 predictions assets, enumerated relevant corpus papers
   via `aggregate_papers.py`, cross-referenced t0107's 8-direction polar overstatement finding, and
   computed quantitative deltas vs each literature baseline with specific paper / page / table
   citations.
3. The subagent wrote `tasks/t0113_t0106_seed2247_replicate/results/compare_literature.md` and ran
   the verificator which passed cleanly.

## Outputs

* `tasks/t0113_t0106_seed2247_replicate/results/compare_literature.md` — 286 lines covering 4
  comparison families with cited references.

## Headline Comparisons

* Prior-task non-replication: best legit DSI 0.365 vs t0106's 0.99 (delta -0.63) and t0112's 0.95
  (delta -0.59); best PD 71.7 Hz vs t0106's 122.6 Hz and t0112's 114.8 Hz. 0 legit joint-pass cells
  vs 122 and 7.
* 3-seed substrate-rate: 1.26% ± 1.01% (CI -0.73 to 3.25%) brackets Hay 2011 (0.40%) and Druckmann
  2007 (0.10%) — cannot reject either; the random seed widened the variance envelope as S-0112-01
  predicted.
* HV plateau gen 14 is 6 gens BELOW Mohacsi 2024's published NSGA-II convergence range (20-60); the
  gen 13->14 +26% HV jump is strong prima facie evidence of premature stop.
* Best legit DSI 0.365 sits ~50% below all three DSGC biological references (Trenholm 2013 0.76,
  Oesch 2005 0.74, Poleg-Polsky 2026 0.73). Carrying t0107's ~0.42 absolute polar overstatement
  forward implies effective 8-direction DSI of zero for the best legit cell.

## Issues

No issues encountered. The verificator passed cleanly. All cited values resolved against existing
paper summaries linked from t0078, t0097, t0002, t0010, and t0102 task folders.
