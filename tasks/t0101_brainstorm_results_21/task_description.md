# t0101 — Brainstorm Session 21: Poleg-Polsky 2026 Deep-Dive

## Context

Researcher asked seven concrete questions about Poleg-Polsky 2026 (Nature Communications,
`10.1038/s41467-026-70288-4`): parameter count, morphology optimisation, seed count, generation
count, novel mechanisms, DSI values, and biological realism. Answers were read directly from the
downloaded PDF
(`tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/files/polegpolsky_2026_ml-motion-primitives.pdf`)
rather than from the existing `summary.md`, which we discovered contains several fabricated claims
(wrong title, "NMDA multiplicative gating", "velocity-dependent coincidence detection",
"distance-graded delay lines", "A-type K density" — none of which appear in the published paper).

A side-by-side comparison with our NSGA-II / MOBO history (t0076 -> t0078 -> t0080 -> t0081 -> t0083
-> t0091 -> t0099) revealed three orders of magnitude in candidate budget per "configuration":
Poleg-Polsky runs ~50-100 independent GA restarts of a pop=10, 300-1000-generation (1+9)-ES per
study configuration (~300k candidates per configuration, deterministic), whereas our largest lineage
(t0081 + t0083) totals 1 728 candidates from a single warm-started seed at pop=96, gens 0-17 with
N_SEEDS=20 noise replicates per direction (160 sims per candidate).

The researcher decided to spawn one follow-up NSGA-II task that re-balances the budget in PP-2026's
favour: 2 GA seeds instead of 1, N_SEEDS reduced from 20 to 4 (factor of 5), generations extended
from 8-17 to 20, on the same 68-d joint electrophys+morphology substrate as t0091 / t0099 with
random initialisation (no anchor warm-start). Expected cost ~$4-6.

The session also surfaced a budget overrun: the project had spent $23.91 against a $20 ceiling
(119.5%). Researcher approved a budget bump to $35 total / $8 per-task, committed directly to main
prior to this brainstorm task per the framework's "infrastructure changes outside task folders"
rule.

## Decisions

1. **Create t0102_seedscale_n4_gen20** — follow-up NSGA-II on 68-d substrate, GA seeds=2 (random
   init, seeds 44 and 55 to avoid overlap with t0099's 11/22/33), N_SEEDS=4, gens=20, pop=96. Cost
   cap $8.

2. **Record three new suggestions**:
   - **HIGH**: correct the fabricated content in
     `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md` using
     the corrections mechanism.
   - **MEDIUM**: if t0102 succeeds at N_SEEDS=4 with DSI/PD scatter comparable to t0099, lock 4 as
     the new default noise-replicate count and update `tasks/t0080_*/code/constants.py:43`.
   - **MEDIUM**: PP-style ablation — run a budget-matched comparison between (a) our current 1-2
     GA seeds at gens 17-20 and (b) a PP-style 10-20 GA seeds at gens 8 each on the same 68-d
     substrate; test whether more restarts at fewer generations yields more diverse Pareto cells.

3. **No suggestion rejections, no task cancellations, no reprioritisations** — the brainstorm is
   forward-creating only.

## Scope

This is a pure decision-recording task. No experiments, no code, no asset production. The follow-up
optimisation work happens in `t0102_seedscale_n4_gen20`; correction of the Poleg-Polsky 2026
`summary.md` is left as a high-priority suggestion to be picked up by a future task.

## Out of Scope

* Actually running the NSGA-II (t0102's job).
* Correcting the Poleg-Polsky 2026 `summary.md` (deferred suggestion).
* Re-baselining N_SEEDS or population size as a framework-wide default (deferred suggestion).
