---
spec_version: "2"
answer_id: "pooled-survivors-latent-drivers-dsi07-pd10"
answered_by_task: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
date_answered: "2026-05-21"
---
# F1 drives DSI (r=-0.59, mixed ephys+morph), F3 drives PD rate (r=+0.75, purely electrophys); no joint factor passes |r|>0.3 on both

## Question

Which factors (after varimax rotation on the full 68-d pool) load most strongly on dsi_vector_sum
and pd_rate_hz, and are they morphology-dominated, electrophys-dominated, or mixed?

## Answer

F1 is the dominant DSI driver (r=-0.589, p ~ 1e-82) and is mixed — its top loadings include both
electrophys channels (SK_AIS, SKAHP, NAP) and a morphology parameter
(primary_branch_pd_concentration). F3 is the dominant PD-rate driver (r=+0.746, p ~ 1e-155) and is
purely electrophys (NAR, IH, NAV16_SOMA, BK channels, RA). No single factor crosses |r|>0.3 on both
DSI and PD simultaneously, so the strict-cohort pool does not contain a joint DSI-PD axis — the
answer to "are the drivers shared?" is no in this strict cohort, but t0110's relaxed-cohort analysis
shows this is a known truncated-cohort artefact.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0108_t0106_cluster_factor_dsi05_pd10`
* Task: `t0110_relaxed_cohort_factor_analysis`
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
