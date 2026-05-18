# t0108 — Detailed Results

## Summary

For 150 unique t0106 cells passing DSI > 0.5 AND PD-rate > 10 Hz: k-means on the 54-d electrophys
submatrix is dominated by a 10-cell low-PD outlier cluster (silhouette 0.50 at k=2); k-means on the
14-d morphology submatrix gives a richer 4-cluster split (sizes 21/55/67/7) with 30 of 54
electrophys parameters Bonferroni-significant across clusters. Varimax factor analysis on the full
68-d vector identifies a single joint DSI–PD trade-off factor F10 (|r_DSI|=0.31, |r_PD|=0.45).

## Methodology

* **Machine**: local Windows 11 / PowerShell session, no remote machines.
* **Runtime**: ~3 min wall clock for all three pipelines.
* **Timestamps**: started 2026-05-18 13:00 UTC; finished 2026-05-18 ~16:00 UTC.
* **Software**: Python 3.13, scikit-learn 1.8.0 (PCA, FactorAnalysis, KMeans), scipy.stats (kruskal,
  pearsonr), numpy, matplotlib.
* **Random seeds**: KMeans random_state=42, n_init=10. FactorAnalysis random_state=42.
* **Determinism**: dedup tolerance = 6 decimals on the 68-d vector. Identical reruns reproduce all
  numbers reported here.

## Cell selection

| Filter | N raw evaluations | N passing | N unique (deduped) |
| --- | --- | --- | --- |
| `dsi > 0.5 AND pd_rate_hz > 10` | 3,744 | 784 | **150** |

Source: `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`.

Cohort statistics:
* DSI mean = 0.868, range [0.503, 1.000].
* PD rate mean = 79.66 Hz, range [10.71, 122.62 Hz].

## Q1 — PCA + K-means on electrophys (54-d) with morphology overlays

### K-means sweep on z-scored 54-d electrophys

| k | inertia | silhouette |
| --- | --- | --- |
| 2 | 6617.86 | **0.496** |
| 3 | 6076.78 | 0.129 |
| 4 | 5557.24 | 0.126 |

Headline `k = 2` (silhouette maximum).

### Cluster sizes and DSI/PD distributions

| cluster | n | DSI mean | PD-rate mean (Hz) |
| --- | --- | --- | --- |
| 0 | 10 | 0.920 | **18.74** |
| 1 | 140 | 0.864 | 84.01 |

The k=2 split picks out a small (~7%) low-firing high-DSI subgroup against the bulk of cells.

### PCA variance explained (54-d electrophys)

* PC1 = 19.9 %, PC2 = 9.1 %, PC3 = 7.1 % (cumulative PC1–3 = 36.1 %).

### Top-5 loadings per PC (54-d electrophys)

PC1 (terminal/somatic Ca2+ and K-Ca cluster):
* SK_MID_GBAR +0.290, CAT_GBAR +0.274, SK_SOMA_GBAR +0.254, SK_TERMINAL_GBAR +0.252, RA_OHM_CM
  +0.227.

PC2 (axonal Kv3 / Ca-L vs persistent-Na contrast):
* KV3_AIS_GBAR +0.326, CAL_GBAR +0.304, NAV16_MID_GBAR +0.294, NAP_PRIMARY_GBAR −0.237, W_ACH_US
  −0.234.

PC3 (BK localisation contrast):
* BK_PRIMARY_GBAR +0.423, W_GABA_US +0.278, BK_MID_GBAR −0.261, AIS_DIAMETER_UM −0.236,
  NAV16_AIS_GBAR −0.236.

### Morphology overlays — Kruskal-Wallis across electrophys clusters

Significant at Bonferroni p < 0.05 (3 of 14 morphology parameters):

| parameter | H | p_bonferroni | cluster 0 mean | cluster 1 mean |
| --- | --- | --- | --- | --- |
| `mean_branching_angle_deg` | 11.63 | **0.009** | 52.57° | 37.55° |
| `branch_length_cv` | 10.31 | **0.019** | 0.194 | 0.301 |
| `ais_length_um` | 9.03 | **0.037** | 35.56 µm | 27.10 µm |

Non-significant (max_strahler_depth p_bonf=0.16, field_elongation_pd p_bonf=0.60, soma_offset_pd_um
p_bonf=1.0, etc.). The morphology signature of the electrophys clustering is weak — only branching
geometry and AIS length differ between the small low-firing group and the bulk.

### Plots — Q1

PCA scatter coloured by k-means cluster:

![PCA scatter on 54-d electrophys, coloured by K-means cluster](images/pca_electrophys_by_cluster.png)

PCA scatter coloured by DSI / PD-rate:

![PCA scatter on 54-d electrophys, coloured by DSI and PD rate](images/pca_electrophys_by_dsi_pd.png)

Morphology distributions per electrophys cluster (boxplots, 14 panels):

![Morphology distributions by electrophys K-means cluster](images/morph_overlay_by_electrophys_cluster.png)

## Q2 — PCA + K-means on morphology (14-d) with electrophys overlays

### K-means sweep on z-scored 14-d morphology

| k | inertia | silhouette |
| --- | --- | --- |
| 2 | 1751.65 | 0.176 |
| 3 | 1535.35 | 0.208 |
| 4 | 1313.34 | **0.233** |

Headline `k = 4` (silhouette maximum).

### Cluster sizes and DSI/PD distributions

| cluster | n | DSI mean | PD-rate mean (Hz) |
| --- | --- | --- | --- |
| 0 | 21 | 0.879 | 102.85 |
| 1 | 55 | 0.900 | 71.43 |
| 2 | 67 | 0.839 | 84.40 |
| 3 | 7 | 0.864 | **29.39** |

Cluster 3 is a low-PD-rate morphology mode; clusters 0–2 are high-PD with similar DSI.

### PCA variance explained (14-d morphology)

* PC1 = 20.9 %, PC2 = 15.8 %, PC3 = 13.8 % (cumulative PC1–3 = 50.5 %).

### Top-5 loadings per PC (14-d morphology)

PC1 (branch-shape variability vs Rall taper):
* branch_length_cv +0.458, rall_exponent −0.429, branch_density_gradient_pd +0.409,
  primary_branch_pd_concentration +0.348, morph_seed −0.273.

PC2 (branching rate, soma/AIS size axis):
* branch_prob_per_um +0.459, soma_diameter_um +0.411, ais_length_um −0.357, morph_seed −0.336,
  mean_segment_length_um +0.321.

PC3 (branching geometry / field shape):
* mean_branching_angle_deg +0.585, num_primary_branches −0.429, soma_diameter_um +0.426,
  field_elongation_pd +0.422, soma_offset_pd_um −0.255.

Note: `morph_seed` is the morphology-generator RNG seed, not a biological parameter — it appears in
PC1/PC2 because the generator's stochastic choices do create real geometric variation correlated
with that seed. Treat as a "generator nuisance variable" when interpreting biologically.

### Electrophys overlays — Kruskal-Wallis across morphology clusters

**30 of 54 electrophys parameters** are Bonferroni-significant (p < 0.05). Top 15:

| parameter | H | p_bonferroni | mean per cluster (0,1,2,3) |
| --- | --- | --- | --- |
| NAV16_AIS_GBAR | 58.67 | **6.1e-11** | 3.10, 3.05, 3.15, **0.78** |
| NAV16_MID_GBAR | 45.53 | **3.9e-8** | 0.42, 0.62, 0.60, 0.44 |
| CAL_GBAR | 44.17 | **7.5e-8** | 0.14, 0.40, 0.29, 0.24 |
| CAT_GBAR | 43.16 | **1.2e-7** | 0.031, 0.038, 0.030, **0.21** |
| IH_GBAR | 42.67 | **1.6e-7** | 0.29, 0.29, 0.29, 0.21 |
| AIS_DIAMETER_UM | 40.65 | **4.2e-7** | 0.62, 0.62, 0.62, 0.60 |
| SK_TERMINAL_GBAR | 37.60 | **1.9e-6** | 0.15, 0.21, 0.20, **0.73** |
| N_ACH | 36.31 | **3.5e-6** | 197, 221, 197, 265 |
| NAP_MID_GBAR | 35.95 | **4.1e-6** | 0.070, 0.085, 0.080, 0.155 |
| BK_AIS_GBAR | 35.90 | **4.3e-6** | 0.65, 0.81, 0.72, 0.91 |
| CM_UF_CM2 | 35.20 | **6.0e-6** | 0.87, 0.96, 0.85, 0.84 |
| KV3_PRIMARY_GBAR | 31.83 | **3.1e-5** | 0.61, 0.32, 0.35, 0.85 |
| NAP_TERMINAL_GBAR | 30.44 | **6.0e-5** | 0.42, 0.44, 0.37, 0.10 |
| SK_PRIMARY_GBAR | 28.99 | **1.2e-4** | 0.99, 0.97, 0.96, 0.83 |
| KV3_AIS_GBAR | 28.48 | **1.6e-4** | 0.28, 0.69, 0.60, 0.71 |

Cluster 3 (the n=7 low-PD-rate morphology) sits at the extreme of several channel axes — low
NAV16_AIS, high CAT_GBAR, high SK_TERMINAL, high N_ACH, high KV3_PRIMARY. The low NAV16_AIS in
particular is a striking violation of the rest of the cohort's high-axonal-Na regime.

### Plots — Q2

PCA scatter coloured by k-means cluster:

![PCA scatter on 14-d morphology, coloured by K-means cluster](images/pca_morphology_by_cluster.png)

PCA scatter coloured by DSI / PD-rate:

![PCA scatter on 14-d morphology, coloured by DSI and PD rate](images/pca_morphology_by_dsi_pd.png)

Electrophys distributions per morphology cluster (boxplots, 54 panels):

![Electrophys distributions by morphology K-means cluster](images/electrophys_overlay_by_morphology_cluster.png)

## Q3 — Varimax factor analysis on the full 68-d vector

* Eigenvalues > 1 (Kaiser criterion): 18.
* Factor count retained (capped at 10): **10**.
* Constant-column drop: 0 / 68 (all dimensions kept).

### Top-5 loadings per factor

| Factor | Top loadings (param → loading) |
| --- | --- |
| F1 | SK_TERMINAL +0.94, SK_MID +0.88, CAT +0.87, NAV16_AIS −0.84, NAP_MID +0.80 |
| F2 | BK_PRIMARY −0.89, BK_MID +0.86, W_GABA −0.74, AIS_DIAMETER +0.69, NAV16_SOMA −0.56 |
| F3 | CAD_TAUR +0.94, field_elongation_pd +0.42, SKAHP_GBAR_SOMA_AIS +0.39, BK_MID +0.38, NAV16_AIS −0.26 |
| F4 | KV3_TERMINAL +0.87, RA_OHM_CM +0.64, CAT +0.28, branch_density_gradient_pd +0.26, N_GABA −0.22 |
| F5 | NAV16_MID +0.77, KV3_AIS +0.72, mean_branching_angle −0.70, SK_AIS −0.69, LAMBDA_ACH +0.56 |
| F6 | NAP_SOMA −0.76, VOFF_NMDA −0.62, ais_length_um −0.59, RHO0_ACH −0.55, IM_GBAR −0.51 |
| F7 | branch_length_cv +0.70, branch_density_gradient_pd +0.64, rall_exponent −0.64, morph_seed −0.54, primary_branch_pd_concentration +0.53 |
| F8 | NAP_MID +0.51, CAT +0.32, AIS_DIAMETER +0.32, BK_TERMINAL −0.31, RHO0_GABA −0.27 |
| F9 | num_primary_branches +0.57, NAP_PRIMARY −0.53, MG_CONC_MM +0.49, N_ACH −0.46, NAV16_TERMINAL +0.42 |
| F10 | CAD_DEPTH −0.73, branch_prob_per_um −0.67, W_ACH −0.58, CAL +0.57, mean_segment_length −0.56 |

### Pearson correlations between factor scores and outcomes

| Factor | r (DSI) | p (DSI) | r (PD) | p (PD) |
| --- | --- | --- | --- | --- |
| F1 | +0.062 | 0.45 | **−0.545** | 5.4e-13 |
| F2 | +0.075 | 0.36 | −0.262 | 1.2e-3 |
| F3 | −0.136 | 0.097 | −0.204 | 0.012 |
| F4 | −0.081 | 0.33 | −0.042 | 0.61 |
| F5 | **−0.325** | 5.1e-5 | −0.140 | 0.088 |
| F6 | −0.278 | 5.8e-4 | −0.129 | 0.12 |
| F7 | +0.147 | 0.074 | −0.096 | 0.24 |
| F8 | −0.067 | 0.41 | −0.008 | 0.92 |
| F9 | −0.021 | 0.80 | −0.031 | 0.71 |
| F10 | **+0.313** | 9.6e-5 | **−0.446** | 1.0e-8 |

### Joint DSI-PD factor

Threshold for joint-factor flag: `|r_DSI| > 0.3 AND |r_PD| > 0.3`.

* **F10 is the single joint factor** in this cohort.
* Loadings: CAD_DEPTH (−0.73), branch_prob_per_um (−0.67), W_ACH (−0.58), CAL (+0.57),
  mean_segment_length (−0.56).
* Sign pattern: pushing F10 in the *positive* direction raises DSI (r=+0.31) but reduces PD-rate
  (r=−0.45). The axis behaves as a DSI–PD **trade-off direction**.
* Biological reading: increasing CAL conductance and reducing CAD_DEPTH (Ca buffer thickness),
  branch_prob_per_um (denser branching), W_ACH (excitatory synaptic weight), and mean segment length
  together improves directional tuning *at the expense of firing throughput*.

### Plots — Q3

Loadings heatmap:

![Varimax factor loadings on 68 parameters](images/factor_loadings_heatmap.png)

Factor correlations with DSI and PD:

![Factor-score correlations with DSI and PD rate](images/factor_correlations_dsi_pd.png)

## Comparison vs t0105 (looser cohort, pooled lineages)

| Aspect | t0105 (N=85, DSI>0.1 & PD>2) | **t0108 (N=150, DSI>0.5 & PD>10)** |
| --- | --- | --- |
| Source lineages | t0091 + t0099 + t0102 + t0104 | t0106 only |
| Electrophys PCA PC1 % var | 29.5 % | 19.9 % |
| Morph clustering | not run | k=4, silhouette 0.233 |
| Electrophys clustering | not headline; binary asym split used instead | k=2, silhouette 0.496 (10 vs 140) |
| Dominant outcome driver | PD: terminal-dendrite K-Ca; DSI: not isolated | PD: F1 (SK/CAT/NAP/NAV16_AIS); DSI: F5/F10 |
| Joint DSI-PD factor | not identified | **F10** (joint trade-off) |

## Analysis / Discussion

1. **Morphology dominates as a categorical axis.** At strict filter, the morphology vector organises
   the cohort more cleanly (k=4 with balanced clusters) than the 54-d electrophys vector (k=2 with a
   10-vs-140 split). 30 of 54 electrophys parameters separate the morphology clusters significantly,
   but only 3 of 14 morphology parameters separate the electrophys clusters. This is consistent with
   the t0105 conclusion that morphology is the dominant discriminator, sharpened here by the
   stricter filter.

2. **Within the high-DSI/high-PD population, electrophys is largely homogeneous.** The 140-cell
   electrophys cluster covers the bulk of high-PD cells with no further internal substructure
   (silhouette 0.13 at k=3-4). The 10-cell minority is a low-PD outlier set that the optimiser
   reached but rarely. Strict filtering thus reveals a narrow channel-regime corridor at the joint
   DSI-PD corner.

3. **F10 is the cohort's trade-off direction.** A single varimax factor captures the joint DSI-PD
   axis with opposite signs. Higher CAL conductance and lower CAD_DEPTH push the cell towards higher
   DSI but reduced PD-rate. The biological interpretation: stronger somatic Ca-L current with a
   thinner Ca buffer enhances directional tuning (better PD–ND discrimination) but may activate
   Ca-dependent K (SK/BK) currents that suppress firing throughput. This is a direct lead for
   targeted moves along F10's loading direction in future optimisation runs.

4. **PD-rate-dominant factor F1 is biologically interpretable.** F1 loads strongly on SK
   (terminal/mid), CAT, NAP_MID — all currents that load capacitive return at the soma and
   accelerate the AHP. The negative loading on NAV16_AIS is the "AIS-Na driving firing rate" axis.
   F1 alone explains ~30 % of PD-rate variance (r² ≈ 0.30).

5. **Cluster 3 (morphology) is the cohort's outlier mode.** Only 7 cells, but they sit at the
   extreme of NAV16_AIS (low), CAT (high), SK_TERMINAL (high), KV3_PRIMARY (high), and N_ACH (high).
   DSI matches the cohort average but PD-rate is much lower (~29 Hz). These cells may represent a
   distinct "high-K, low-Na axon" sub-population that the optimiser found but did not explore in
   depth.

## Limitations

1. **Single lineage**: only t0106 cells are pooled. Cross-lineage generalisation is not tested here;
   t0105 covers that comparison.
2. **N=150 with 68 features** is borderline for factor analysis. Eigenvalue-bootstrap stability is
   not run in this task; t0105's 100-bootstrap factor stability assessment did not transfer.
3. **K-means assumes spherical clusters in z-scored space**. The 10-vs-140 electrophys split may
   reflect this assumption rather than a true bimodal structure; alternative clusterers (Gaussian
   mixture, DBSCAN, hierarchical) might yield different splits.
4. **`morph_seed` appears in PC and factor loadings**. It is a generator nuisance variable, not a
   biological parameter. Where it loads, the interpretation is "the morphology-generator's discrete
   random choices co-vary with this axis", not "the seed value causes the variance".
5. **Varimax requires score regression.** Scores are computed as `Z Λ (Λᵀ Λ)⁻¹` (regression method)
   which is a standard but lossy approximation when communalities are low.
6. **Bonferroni correction is conservative.** A Benjamini-Hochberg FDR analysis would likely uncover
   more morphology parameters separating the electrophys clusters.

## Verification

* All numbers in this document match `results/metrics.json`,
  `results/data/electrophys_clusters.json`, `results/data/morphology_clusters.json`, and
  `results/data/factor_analysis.json` (exact-match check).
* Reproduction: rerun
  `uv run python -m tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.load_filter_cells`,
  `cluster_electrophys`, `cluster_morphology`, `factor_analysis` in that order; all outputs are
  deterministic under the seeds documented in `code/constants.py` and the script headers.
* Cell counts 3744 → 784 → 150 are reproduced verbatim from the gzipped t0106 evaluations.

## Files Created

* `code/paths.py`, `code/constants.py`, `code/cluster_helpers.py`, `code/load_filter_cells.py`,
  `code/cluster_electrophys.py`, `code/cluster_morphology.py`, `code/factor_analysis.py`.
* `results/data/filtered_cells.json`, `results/data/electrophys_clusters.json`,
  `results/data/morphology_clusters.json`, `results/data/factor_analysis.json`.
* `results/metrics.json`, `results/costs.json`, `results/suggestions.json`,
  `results/remote_machines_used.json`.
* `results/images/pca_electrophys_by_cluster.png`, `results/images/pca_electrophys_by_dsi_pd.png`,
  `results/images/morph_overlay_by_electrophys_cluster.png`,
  `results/images/pca_morphology_by_cluster.png`, `results/images/pca_morphology_by_dsi_pd.png`,
  `results/images/electrophys_overlay_by_morphology_cluster.png`,
  `results/images/factor_loadings_heatmap.png`, `results/images/factor_correlations_dsi_pd.png`.
* `assets/answer/t0106-electrophys-clusters-morphology-signature/`,
  `assets/answer/t0106-morphology-clusters-electrophys-signature/`,
  `assets/answer/t0106-dsi-pd-factor-decomposition-strict-cohort/`.

## Next Steps / Suggestions

* **Probe F10 trade-off direction directly**: perturb each F10-loading parameter independently in a
  sample of joint-corner cells (CAD_DEPTH ↓, CAL ↑, branch_prob_per_um ↓, W_ACH ↓,
  mean_segment_length ↓) and measure the DSI / PD response. If the trade-off holds, this gives a
  recipe for sliding along the Pareto front.
* **Probe morphology cluster 3 specifically**: the 7-cell outlier morphology has a distinctive
  high-K low-Na channel regime; in-silico patch / IV recordings on cluster-3 representatives would
  clarify whether the low PD rate reflects a true low-AIS-Na axon or a compensating mechanism
  elsewhere.
* **Repeat factor analysis with NMF or sparse PCA**. Varimax forces orthogonality; sparse
  decomposition might identify more interpretable biological axes.
* **Compare F1 to t0080-era models**. The PD-rate dominant factor (SK/CAT/NAP/NAV16_AIS) is a
  candidate "firing-rate machinery" sub-circuit that could be parameterised and ablated as a
  separate library.
