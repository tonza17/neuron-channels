---
spec_version: "2"
answer_id: "t0106-electrophys-clusters-morphology-signature"
answered_by_task: "t0108_t0106_cluster_factor_dsi05_pd10"
date_answered: "2026-05-18"
confidence: "medium"
---

# Electrophys clusters carry only a weak morphology signature

## Question

When t0106 cells with DSI > 0.5 AND PD > 10 Hz are clustered by their 54-d electrophys parameters,
do the clusters carry a distinguishable morphological signature?

## Short Answer

Only weakly. K-means on the z-scored 54-d electrophys submatrix of the 150-cell strict cohort
produces an unbalanced k=2 split (10 vs 140; silhouette 0.496) that essentially separates a small
low-firing high-DSI outlier group from the bulk. Only 3 of 14 morphology parameters survive
Bonferroni correction at p < 0.05: mean_branching_angle_deg, branch_length_cv, ais_length_um.
Higher-k partitions degrade silhouette to ~0.13, so no further morphology-relevant structure
exists. The electrophys regime that produces high DSI and high PD is therefore largely
morphology-agnostic within this cohort.

## Research Process

The answer was produced by re-clustering an existing optimised cell population (t0106) under a
stricter filter than the prior t0105 analysis used. The pipeline was:

* Read 3,744 raw evaluations from
  `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`.
* Apply `DSI > 0.5 AND PD-rate > 10 Hz`; 784 raw rows passed.
* Dedupe by the 68-d parameter vector at 6-decimal precision; 150 unique cells remained.
* Split the 68-d vector into 54 electrophys + 14 morphology dimensions following the canonical
  layout from `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants_morphology.py`.
* z-score each electrophys column; run `sklearn.cluster.KMeans` for `k ∈ {2, 3, 4}` with
  `random_state=42`, `n_init=10`; pick the headline k by maximum silhouette.
* For each of 14 morphology parameters, run a Kruskal-Wallis H test across clusters and
  Bonferroni-correct over 14 simultaneous tests.

No conflicting evidence was encountered because this is the first analysis at this filter; the
result is contrasted with the looser-filter t0105 analysis in the Synthesis section.

## Evidence from Papers

No paper-based evidence was used. This question is answered purely by re-analysis of project
optimisation output.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

The full quantitative evidence is in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/electrophys_clusters.json`. Headline
numbers:

| k | inertia | silhouette |
| --- | --- | --- |
| 2 | 6617.86 | 0.496 |
| 3 | 6076.78 | 0.129 |
| 4 | 5557.24 | 0.126 |

Cluster sizes at headline k=2: cluster 0 = 10 cells (DSI mean 0.920, PD-rate 18.74 Hz),
cluster 1 = 140 cells (DSI mean 0.864, PD-rate 84.01 Hz).

Morphology Kruskal-Wallis across the two clusters (Bonferroni-corrected over 14 tests):

| parameter | H | p_bonferroni | cluster 0 mean | cluster 1 mean |
| --- | --- | --- | --- | --- |
| mean_branching_angle_deg | 11.63 | 0.009 | 52.57° | 37.55° |
| branch_length_cv | 10.31 | 0.019 | 0.194 | 0.301 |
| ais_length_um | 9.03 | 0.037 | 35.56 µm | 27.10 µm |
| max_strahler_depth | 6.42 | 0.16 | 3.91 | 5.23 |
| field_elongation_pd | 4.11 | 0.60 | 1.73 | 1.23 |
| (rest of 14) | < 4 | ≥ 0.59 | — | — |

PCA on the same 54-d submatrix explains modest variance: PC1 = 19.9 %, PC2 = 9.1 %, PC3 = 7.1 %.
Top PC1 loadings: SK_MID (+0.29), CAT (+0.27), SK_SOMA (+0.25), SK_TERMINAL (+0.25), RA_OHM_CM
(+0.23) — a "terminal/somatic K-Ca-Ca" axis. Top PC2 loadings: KV3_AIS (+0.33), CAL (+0.30),
NAV16_MID (+0.29), NAP_PRIMARY (−0.24), W_ACH (−0.23) — an "axonal-Kv3 / Ca-L vs persistent-Na"
contrast.

## Synthesis

The k=2 split that K-means finds is essentially a "fast-firing main cohort (140 cells)" vs
"slow-firing outlier subgroup (10 cells)" boundary, with PD-rate ~84 Hz vs ~19 Hz separating them.
The morphology parameters that survive Bonferroni correction reflect this split rather than a
biological morphology classification — the slower-firing cluster is more variable in branch
geometry and has a slightly longer AIS. The contrast with the inverse analysis on the same cohort
(see `t0106-morphology-clusters-electrophys-signature`, which finds 30 of 54 electrophys
parameters Bonferroni-significant across morphology clusters) supports the conclusion that
**morphology is the dominant categorical axis** within the high-DSI/high-PD population. The
electrophys regime adapts continuously across morphology types rather than partitioning into
discrete electrophys "types".

## Limitations

* 150 samples × 54 features is borderline for K-means in high dimensions; alternative clusterers
  (Gaussian mixture, hierarchical, DBSCAN) might yield different splits.
* The strict filter removes weak-DSI / low-firing cells that t0105 retained; this answer holds
  only within the "already empirically successful DSGCs" population.
* PC1 explains only 19.9 % of variance, so PCA-projected scatter visualisations may understate
  separation that exists in the full 54-d space.
* Bonferroni correction over 14 tests is conservative; a Benjamini-Hochberg FDR analysis might
  identify additional morphology parameters with weaker effects.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — source cells.
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — analysis task.
* Result data:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/electrophys_clusters.json`.
* Visualisations:
  `results/images/pca_electrophys_by_cluster.png`,
  `results/images/pca_electrophys_by_dsi_pd.png`,
  `results/images/morph_overlay_by_electrophys_cluster.png`.
