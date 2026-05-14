---
spec_version: "2"
answer_id: "t0104-joint-pass-recovery-2obj"
answered_by_task: "t0104_nsga2_2obj_dsi_pdrate_3seeds"
date_answered: "2026-05-14"
---
# 2-objective NSGA-II joint-pass recovery test

## Question

Does 2-objective NSGA-II (DSI + PD-rate, with the DSI-silence guard applied) recover joint-pass
cells where t0102's 3-objective run found zero?

## Answer

No. Across 2,208 evaluations from two random-init NSGA-II seeds (44 and 55) running the 2-objective
DSI + PD formulation with the silence guard active, zero cells cleared the strict joint-pass corner
(DSI >= 0.5 AND PD >= 30 Hz). The DSI extreme broke past 0.5 for the first time in the t0080-t0104
NSGA-II lineage (seed 55 gen 11, DSI = 0.5417 at PD = 3.57 Hz), confirming the substrate is not
artificially capped by the silenced-cell DSI=1.0 floating-point artifact that contaminated t0102's
Pareto front. The L-shaped Pareto front replicates t0102's exactly — extremes reachable on each
axis but the joint corner empirically empty — ruling out objective-vector dimensionality as the
explanation for the substrate-limited reading.

## Sources

* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0099_random_init_pareto_robustness`
* Task: `t0102_seedscale_n4_gen20`
* Paper: `10.1371_journal.pcbi.1012039`
* Paper: `10.48550_arXiv.2306.04525`
* Paper: `10.48550_arXiv.2401.14014`
