---
spec_version: "2"
answer_id: "random-init-reproducibility-and-warmstart-dependence"
answered_by_task: "t0099_random_init_pareto_robustness"
date_answered: "2026-05-10"
---

## Question

Are the qualitative findings of t0091's joint 68-d NSGA-II run (anchor distribution, biological-plausibility verdict, strict joint-pass count) reproducible under different RNG seeds, and was t0091's 5-anchor warm-start load-bearing — would a purely random initial population have found the same Pareto front?

## Answer

**Q1 (reproducibility): Yes** — across 3 random-init seeds (Pareto sizes 19/22/14), every seed reaches the same headline verdict as t0091: zero biologically-plausible joint-pass cells, zero symmetric-anchor Pareto cells. **Q2 (warm-start dependence): Yes** — t0091 found 1 strict joint-pass cell from its 5-anchor warm-started Pareto (57 cells); none of the 3 random-init seeds (55 cells total) recover that region within 5–8 generations and $1–5 per-seed budget. The warm-start was load-bearing specifically for the high-PD-rate dimension: random-init reaches t0091's DSI threshold (best 0.49) but only half its PD-rate (best 18.7 Hz vs t0091's 35 Hz).

## Sources

* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0092_diagnose_morphology_generator_silence`
* Task: `t0093_resweep_and_t0090_correction`
