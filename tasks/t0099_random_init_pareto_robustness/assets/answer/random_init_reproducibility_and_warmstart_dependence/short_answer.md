---
spec_version: "2"
answer_id: "random_init_reproducibility_and_warmstart_dependence"
answered_by_task: "t0099_random_init_pareto_robustness"
date_answered: "2026-05-10"
---

## Question

Are the qualitative findings of t0091's joint 68-d NSGA-II run (anchor distribution, biological-plausibility verdict, strict joint-pass count) reproducible under different RNG seeds, and was t0091's 5-anchor warm-start load-bearing — would a purely random initial population have found the same Pareto front?

## Answer

Q1 reproducibility verdict: **Yes**. Yes, qualitatively: across 3 random-init seeds with Pareto sizes [19, 22, 14], every seed reaches the same headline verdict as t0091 — zero biologically-plausible joint-pass cells under the 13-prior worst-case aggregation. The bio-plausibility outcome is robust to RNG seed. Strict joint-pass count is 0 in every seed. Q2 warm-start dependence
verdict: **Yes**. The 5-anchor warm-start was load-bearing for the strict joint-pass region. t0091 found 1 strict joint-pass cell(s) from the warm-started Pareto (57 cells); none of the 3 random-init seeds (Pareto sizes [19, 22, 14], total 0 strict joint-pass) recover that region under a $1.00-per-seed budget.

## Sources

* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0092_diagnose_morphology_generator_silence`
* Task: `t0093_resweep_and_t0090_correction`
