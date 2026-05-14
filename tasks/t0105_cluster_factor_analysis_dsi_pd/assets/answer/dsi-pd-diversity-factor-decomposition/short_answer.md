---
spec_version: "2"
answer_id: "dsi-pd-diversity-factor-decomposition"
answered_by_task: "t0105_cluster_factor_analysis_dsi_pd"
date_answered: "2026-05-14"
---
# Factor decomposition of DSI vs PD diversity

## Question

Which factors (combinations of the 68 input parameters) explain DSI diversity versus PD diversity,
and is there a joint factor or are the two outcomes orthogonal?

## Answer

The two outcomes are mostly orthogonal but partially coupled through one near-joint factor: a
varimax factor analysis on the standardised 68-d matrix (N=85, 10 factors by Kaiser criterion capped
at 10) finds F1 the only factor exceeding |r| = 0.25 on either outcome, with r_DSI = -0.322
(p=0.003) and r_PD = -0.265 (p=0.014). No factor crosses the joint-factor threshold |r| > 0.3 on
both, so the joint high-DSI / high-PD corner is not unlocked by a single low-d axis. F1's top
loadings (NAP_PRIMARY, SK_MID, MG_CONC_MM, RA_OHM_CM) are bootstrap-stable across 200 resamples, but
F3 through F10 are not. The substrate-limited reading from t0102 and t0104 is reinforced: DSI and PD
share a weak common axis but remain substantially orthogonal.

## Sources

* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0099_random_init_pareto_robustness`
* Task: `t0102_seedscale_n4_gen20`
* Task: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_loadings.png`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_correlations.png`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_loadings_bootstrap.png`
