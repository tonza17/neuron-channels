---
spec_version: "2"
answer_id: "pooled-all-cells-truncated-cohort-artefact-test"
answered_by_task: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
date_answered: "2026-05-22"
---
# One joint DSI-PD factor reappears in the unfiltered pool, confirming truncated-cohort artefact

## Question

Does at least one varimax factor recover a joint DSI-PD axis (|r_DSI| > 0.3 AND |r_PD| > 0.3)
when the cohort filter is removed and the full DSI / PD quality range is in the pool, confirming
the truncated-cohort artefact first observed at t0110 and t0116?

## Answer

Yes — F1 of the unfiltered-pool varimax solution is a joint DSI-PD factor (r_DSI = +0.421, r_PD
= +0.352, both p < 1e-100, n = 4431), satisfying |r| > 0.3 on both axes. At the strict cohort
(t0116) zero of ten factors satisfied this criterion. The reappearance of a joint factor once
the filter is lifted confirms the truncated-cohort-artefact hypothesis: the strict cohort
genuinely erases the shared latent that couples DSI and PD; the decoupling is not an intrinsic
substrate property.

## Sources

* Task: `t0110_relaxed_cohort_factor_analysis`
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
* Task: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
