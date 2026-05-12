---
spec_version: "2"
answer_id: "does-n4-gens20-2seeds-recover-joint-pass-corner"
answered_by_task: "t0102_seedscale_n4_gen20"
date_answered: "2026-05-12"
---
# Random-init NSGA-II joint-pass recovery test

## Question

Does running 68-d NSGA-II at N_EVAL_SEEDS=4 noise replicates, gens=20, pop=96, 2 random-init GA
seeds (44, 55), no warm-start, recover the strict joint-pass corner (DSI>=0.5 AND PD-rate>=30 Hz AND
robustness>=0.7) of the Bed B + morphology compartmental DSGC substrate?

## Answer

No. Across 2,592 evaluations from two random-init NSGA-II seeds, zero cells cleared the strict
joint-pass corner, and zero cells cleared even the loosest 2-axis test (DSI>=0.5 AND PD>=5 Hz),
because DSI and PD-rate are strongly bimodally anti-correlated on this substrate. The headline
max-DSI of 1.0 in both seeds turned out to be a floating-point artifact of the vector-sum DSI
formula on silenced cells with PD=0 Hz; the real DSI ceiling under N=4 noise replicates is roughly
0.35. The earlier t0091 single joint-pass cell, previously framed as an NSGA-II discovery, is
reframed here as a one-mutation polynomial-mutation descendant of an alt_topology warm-start anchor,
so removing the warm-start removes the entire joint-pass signal.

## Sources

* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0099_random_init_pareto_robustness`
* Task: `t0101_brainstorm_results_21`
* Paper: `10.1371_journal.pcbi.1012039`
* Paper: `10.48550_arXiv.2306.04525`
* Paper: `10.48550_arXiv.2401.14014`
