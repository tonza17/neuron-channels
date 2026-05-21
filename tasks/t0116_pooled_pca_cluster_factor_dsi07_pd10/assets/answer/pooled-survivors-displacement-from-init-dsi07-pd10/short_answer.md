---
spec_version: "2"
answer_id: "pooled-survivors-displacement-from-init-dsi07-pd10"
answered_by_task: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
date_answered: "2026-05-21"
---
# Per-seed mean displacement from gen-0 ranges 2.4 to 15.0 in PC1+PC2; ~60 in 68-d standardised space

## Question

How far did NSGA-II travel from its gen-0 random initialisation in each seed (44, 77, 7755, 9354),
measured in the 68-d standardised parameter space and in PC1+PC2 space of the combined 68-d PCA?

## Answer

The four seeds travel comparably in the full 68-d standardised space (mean displacement 59.7-61.3
standardised units, p95 60.8-61.7) but diverge sharply in the combined PC1+PC2 plane: seed 44
traveled 15.0 PCA units, seed 7755 traveled 13.3, seed 77 traveled 8.5, and seed 9354 traveled only
2.4. The 68-d uniformity is consistent with each seed's gen-0 distribution covering similar shells
of the LHS-sampled parameter space, while the PC1+PC2 divergence reflects the seed-specific
direction of NSGA-II descent — the leading components are exactly the cross-seed axis along which
the basins separate. All four seeds traveled substantially further than their own gen-0 within-seed
spread, confirming optimisation moved the survivors out of the random-init region.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
