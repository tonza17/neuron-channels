---
spec_version: "2"
answer_id: "t0106-morphology-clusters-electrophys-signature"
answered_by_task: "t0108_t0106_cluster_factor_dsi05_pd10"
date_answered: "2026-05-18"
---

# Morphology clusters carry a strong electrophys signature

## Question

When t0106 cells with DSI > 0.5 AND PD > 10 Hz are clustered by their 14-d morphology parameters,
do the clusters carry a distinguishable electrophys signature?

## Answer

Yes, strongly. K-means on the z-scored 14-d morphology submatrix of the 150-cell strict cohort
gives a balanced k=4 split (silhouette 0.233, sizes 21/55/67/7), and 30 of 54 electrophys
parameters separate the clusters at Bonferroni p < 0.05. The strongest discriminators are
NAV16_AIS_GBAR, NAV16_MID_GBAR, CAL_GBAR, CAT_GBAR, IH_GBAR, and AIS_DIAMETER_UM (all
p_bonf < 1e-6). Cluster 3 (n=7, low PD ~29 Hz) carries a distinctive high-K low-axonal-Na regime
with very different NAV16_AIS, CAT, SK_TERMINAL, and KV3_PRIMARY values from clusters 0–2. Each
morphology type therefore imposes a distinct channel regime in this cohort.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0108_t0106_cluster_factor_dsi05_pd10`
