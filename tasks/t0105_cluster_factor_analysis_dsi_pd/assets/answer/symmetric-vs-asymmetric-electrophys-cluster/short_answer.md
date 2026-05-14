---
spec_version: "2"
answer_id: "symmetric-vs-asymmetric-electrophys-cluster"
answered_by_task: "t0105_cluster_factor_analysis_dsi_pd"
date_answered: "2026-05-14"
---
# Symmetric vs asymmetric DSGCs in electrophys PC space

## Question

Do symmetric and asymmetric DSGC morphologies share the same electrophys parameter regime, or do
they form distinct clusters in PC space?

## Answer

No, they form distinct clusters. PCA on the 54-d electrophys submatrix of the 85-cell primary cohort
(DSI > 0.1 AND PD > 2 Hz, pooled across four 68-d NSGA-II lineages) shows PC1 separating the 20
symmetric and 65 asymmetric cells at Mann-Whitney U=31.0, p=1.5e-10. PC1 captures 29.5 % of variance
and loads on terminal-dendrite K-Ca conductances (SK_TERMINAL, BK_TERMINAL, BK_MID, SK_SOMA) plus
primary-dendrite persistent Na (NAP_PRIMARY). The strict cohort (DSI > 0.2 AND PD > 3 Hz, N=30)
preserves the separation (p=8.2e-5), so the result is not an artefact of the relaxed primary filter.
PC2 does not separate the classes (p=0.78), so the distinction lives on a single axis dominated by
terminal-dendrite KCa expression.

## Sources

* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0099_random_init_pareto_robustness`
* Task: `t0102_seedscale_n4_gen20`
* Task: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* Task: `t0086_robustness_cluster_bio_comparison` (cluster-analysis precedent)
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/pca_electrophys_panels.png`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/morphology_gallery.png`
