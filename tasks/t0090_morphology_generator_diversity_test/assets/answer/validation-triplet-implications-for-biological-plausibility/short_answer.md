---
spec_version: "2"
answer_id: "validation-triplet-implications-for-biological-plausibility"
answered_by_task: "t0090_morphology_generator_diversity_test"
date_answered: "2026-05-07"
---
# Validation triplet implications for biological plausibility

## Question

Do the validation triplet results (G.1 AIS-to-soma Nav ratio audit, G.2 NMDA units calibration, G.3
NaP knockout) confirm or refute the biological-plausibility flags raised in t0086 and t0088?

## Answer

Conditional. The G.1 AIS-to-soma Nav-ratio audit shows the cluster-1 ratio is a real biological
signal, not a centroid artifact: zero of four cluster-1 cells are pinned to the soma Nav lower bound
and three of four cells individually exceed a ratio of 50, so the +33-sigma deviation from the
Werginz 2024 prior reflects an actual model preference rather than an inflated denominator. G.2
produces a NetCon-weight to per-spine conductance calibration that lets us re-score the
cluster-NMDA-exotic verdict in calibrated units, but the conversion does not by itself reduce the
deviation enough to rule out a units mismatch. G.3 quantifies the causal contribution of distal NaP
to the direction-selectivity index of the four cluster representatives by comparing knockout DSI
against the original t0083 DSI, providing a per-cell verdict (NaP-dominant, NaP-partial, or
NaP-minor). Taken together, the triplet confirms two of the t0086 / t0088 flags as real biological
signals (cluster-1 AIS-to-soma ratio, NaP attribution where the knockout collapses DSI) and leaves
the NMDA-exotic flag in the conditional category pending an independent measurement of per-spine
open conductance in the t0024 voltage-clamp regime.

## Sources

* Task: `t0083_bedb_v3_extend_nsga2_gen8plus`
* Task: `t0086_robustness_cluster_bio_comparison`
* Task: `t0088_recluster_marginals_and_vm_motifs`
* Code: `tasks/t0090_morphology_generator_diversity_test/code/validation_g1_nav_ratio.py`
* Code: `tasks/t0090_morphology_generator_diversity_test/code/validation_g2_nmda_units.py`
* Code: `tasks/t0090_morphology_generator_diversity_test/code/validation_g3_nap_knockout.py`
