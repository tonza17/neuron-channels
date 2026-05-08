---
spec_version: "2"
answer_id: "morphology-extension-biological-plausibility"
answered_by_task: "t0091_morphology_extended_nsga2_v1"
date_answered: "2026-05-08"
---

## Question

Did enabling the 14-d procedural morphology variation as an optimisation axis open biologically-plausible joint-pass regions of parameter space that the fixed-Bed-B substrate of t0080-t0088 could not reach?

## Answer

No. None of the 57 Pareto cells reach the joint plausible region across all 13 priors (9 electrophys + 4 morphology). Worst-case aggregation flags every cell as exotic or stretched, driven primarily by NMDA / NaP / GABA prior deviations carried over from the v3 electrophys substrate. PD-asymmetric anchor 3 captured 12 cells vs ND-asymmetric anchor 4 with 9 (one-sided permutation p=0.331).

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus`
* Task: `t0086_robustness_cluster_bio_comparison`
* Task: `t0090_morphology_generator_diversity_test`
* Task: `t0092_diagnose_morphology_generator_silence`
* Task: `t0093_resweep_and_t0090_correction`
