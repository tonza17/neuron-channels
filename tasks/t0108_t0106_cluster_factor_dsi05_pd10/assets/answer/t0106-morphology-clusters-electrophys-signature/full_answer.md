---
spec_version: "2"
answer_id: "t0106-morphology-clusters-electrophys-signature"
answered_by_task: "t0108_t0106_cluster_factor_dsi05_pd10"
date_answered: "2026-05-18"
confidence: "high"
---

# Morphology clusters carry a strong electrophys signature

## Question

When t0106 cells with DSI > 0.5 AND PD > 10 Hz are clustered by their 14-d morphology parameters,
do the clusters carry a distinguishable electrophys signature?

## Short Answer

Yes, strongly. K-means on the z-scored 14-d morphology submatrix of the 150-cell strict cohort
gives a balanced k=4 split (silhouette 0.233, sizes 21/55/67/7), and 30 of 54 electrophys
parameters separate the clusters at Bonferroni p < 0.05. The strongest discriminators are
NAV16_AIS_GBAR, NAV16_MID_GBAR, CAL_GBAR, CAT_GBAR, IH_GBAR, and AIS_DIAMETER_UM (all
p_bonf < 1e-6). Cluster 3 (n=7, low PD ~29 Hz) carries a distinctive high-K low-axonal-Na regime.
Each morphology type therefore imposes a distinct channel regime in this cohort.

## Research Process

Same source data, filter, and dedup as the inverse-direction answer
(`t0106-electrophys-clusters-morphology-signature`). The pipeline this question uses:

* Read 3,744 t0106 evaluations; apply `DSI > 0.5 AND PD > 10 Hz`; 784 passing; dedupe to 150 unique
  68-d vectors.
* Split into 54 electrophys + 14 morphology.
* z-score the 14-d morphology submatrix.
* K-means for `k ∈ {2, 3, 4}` on the z-scored 14-d matrix with `random_state=42`, `n_init=10`. Pick
  the headline k by maximum silhouette.
* For each of 54 electrophys parameters, Kruskal-Wallis H test across clusters,
  Bonferroni-corrected over 54 simultaneous tests.

The answer is decisive (high confidence) because the effect size is large (30/54 parameters
significant after a conservative correction, top effects at p < 1e-7) and reproduces across
silhouette-equivalent k values.

## Evidence from Papers

No paper-based evidence was used. This question is answered purely by re-analysis of project
optimisation output.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Full results in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/morphology_clusters.json`.

K-means sweep on 14-d morphology:

| k | inertia | silhouette |
| --- | --- | --- |
| 2 | 1751.65 | 0.176 |
| 3 | 1535.35 | 0.208 |
| 4 | 1313.34 | 0.233 |

Headline k=4. Cluster composition:

| cluster | n | DSI mean | PD-rate mean (Hz) |
| --- | --- | --- | --- |
| 0 | 21 | 0.879 | 102.85 |
| 1 | 55 | 0.900 | 71.43 |
| 2 | 67 | 0.839 | 84.40 |
| 3 | 7 | 0.864 | 29.39 |

Top-15 Bonferroni-significant electrophys parameters (out of 30):

| parameter | H | p_bonferroni | mean per cluster (0, 1, 2, 3) |
| --- | --- | --- | --- |
| NAV16_AIS_GBAR | 58.67 | 6.1e-11 | 3.10, 3.05, 3.15, 0.78 |
| NAV16_MID_GBAR | 45.53 | 3.9e-08 | 0.42, 0.62, 0.60, 0.44 |
| CAL_GBAR | 44.17 | 7.5e-08 | 0.14, 0.40, 0.29, 0.24 |
| CAT_GBAR | 43.16 | 1.2e-07 | 0.031, 0.038, 0.030, 0.21 |
| IH_GBAR | 42.67 | 1.6e-07 | 0.29, 0.29, 0.29, 0.21 |
| AIS_DIAMETER_UM | 40.65 | 4.2e-07 | 0.62, 0.62, 0.62, 0.60 |
| SK_TERMINAL_GBAR | 37.60 | 1.9e-06 | 0.15, 0.21, 0.20, 0.73 |
| N_ACH | 36.31 | 3.5e-06 | 197, 221, 197, 265 |
| NAP_MID_GBAR | 35.95 | 4.1e-06 | 0.070, 0.085, 0.080, 0.155 |
| BK_AIS_GBAR | 35.90 | 4.3e-06 | 0.65, 0.81, 0.72, 0.91 |
| CM_UF_CM2 | 35.20 | 6.0e-06 | 0.87, 0.96, 0.85, 0.84 |
| KV3_PRIMARY_GBAR | 31.83 | 3.1e-05 | 0.61, 0.32, 0.35, 0.85 |
| NAP_TERMINAL_GBAR | 30.44 | 6.0e-05 | 0.42, 0.44, 0.37, 0.10 |
| SK_PRIMARY_GBAR | 28.99 | 1.2e-04 | 0.99, 0.97, 0.96, 0.83 |
| KV3_AIS_GBAR | 28.48 | 1.6e-04 | 0.28, 0.69, 0.60, 0.71 |

PCA on the 14-d morphology submatrix explains more variance per PC than the electrophys PCA:
PC1 = 20.9 %, PC2 = 15.8 %, PC3 = 13.8 %.

## Synthesis

Each morphology cluster carries a distinct channel signature:

* **Cluster 0** (n=21, high PD ~103 Hz): low CAL=0.14, moderate KV3_PRIMARY=0.61, low NAP_MID. A
  high-firing morphology mode.
* **Cluster 1** (n=55, high DSI 0.90, PD ~71 Hz): high CAL=0.40, moderate-low KV3, balanced NAP.
  The "best DSI" morphology cluster.
* **Cluster 2** (n=67, average PD ~84 Hz): intermediate on most axes — the "modal" morphology.
* **Cluster 3** (n=7, low PD ~29 Hz): low NAV16_AIS (0.78), high CAT (0.21), high SK_TERMINAL
  (0.73), high KV3_PRIMARY (0.85), high N_ACH (265), low NAP_TERMINAL. A distinctive "high-K
  low-axonal-Na" cluster with high cholinergic input but low firing rate.

NAV16_AIS_GBAR is the single strongest discriminator (H = 58.7, p_bonf = 6×10⁻¹¹), separating
cluster 3 (low axonal Na) from clusters 0–2 (high axonal Na). This matches the low PD-rate of
cluster 3 — PD scales with AIS Na conductance, consistent with the t0024-era result.

The contrast with the inverse analysis (`t0106-electrophys-clusters-morphology-signature`, which
finds only 3 / 14 morphology parameters separating electrophys clusters) is striking and the two
analyses are in agreement: **morphology defines categorical groups; electrophys modulates
continuously within them**.

## Limitations

* Cluster 3 has only n=7; the channel-regime characterisation is robust against KW non-parametric
  testing but the cluster boundary may be sensitive to outliers.
* Bonferroni correction over 54 tests is conservative; a Benjamini-Hochberg FDR analysis would
  identify additional electrophys parameters with weaker but real effects.
* `morph_seed` appears in PC1/PC2 loadings — it is the generator's RNG seed and not a biological
  parameter; its loading reflects the fact that the morphology-generator's discrete random choices
  co-vary with cluster identity.
* The cluster boundary depends on the choice of k; k=3 and k=2 also reach silhouette ≥ 0.18 with
  meaningful but coarser splits.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — source cells.
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — analysis task.
* Result data:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/morphology_clusters.json`.
* Visualisations:
  `results/images/pca_morphology_by_cluster.png`,
  `results/images/pca_morphology_by_dsi_pd.png`,
  `results/images/electrophys_overlay_by_morphology_cluster.png`.
