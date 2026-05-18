# t0108 — Cluster + Factor Analysis of t0106 Cells at DSI>0.5 AND PD>10

## Context

Direct researcher commission at 2026-05-18 after the t0106 / t0107 results landed.
`t0106_long_pdnd_nsga2_300gen` is the most recent 68-d NSGA-II lineage (54-d electrophys + 14-d
morphology) on the Bed B + morphology substrate. It evaluated **3,744 cells** across 300+
generations from a single GA seed (44).

This task re-asks the questions from `t0105_cluster_factor_analysis_dsi_pd` on a single,
high-quality cohort and at a much stricter filter:

* **t0105 primary**: `DSI > 0.1 AND PD > 2 Hz` across 4 lineages (~86 unique cells).
* **t0108 (this task)**: `DSI > 0.5 AND PD > 10 Hz` on t0106 alone (**150 unique cells** confirmed
  by pre-scoping count).

The stricter filter focuses the analysis on cells that already exhibit strong direction selectivity
*and* substantial firing — the cohort of empirically successful DSGCs from the optimiser.
Restricting to the single t0106 lineage removes cross-lineage seed and-generation confounds that
t0105 carried.

This task also extends the t0105 design in two important ways:

1. **Bidirectional cluster analysis**: instead of pre-classifying cells by an asymmetry rule and
   running PCA only on electrophys, this task runs *two* unsupervised pipelines:
   * PCA + K-means on the 54-d electrophys submatrix, with the 14-d morphology parameter
     distributions overlaid per cluster (electrophys clusters → which morphology shapes?).
   * PCA + K-means on the 14-d morphology submatrix, with the 54-d electrophys parameter
     distributions overlaid per cluster (morphology clusters → which channel regimes?).
2. **Factor analysis on the joint 68-d vector** with varimax rotation, exactly as t0105 did, but on
   the new cohort.

## Goal

For the **150 unique cells** from `t0106_long_pdnd_nsga2_300gen` with `DSI > 0.5 AND PD > 10 Hz`
(deduped by 68-d vector), answer three questions:

1. **Do electrophys clusters carry a morphological signature?** Run PCA + K-means on the 54-d
   electrophys vectors, then for each cluster summarise the morphology parameter distributions
   (mean, median, IQR, boxplots). Report which morphology parameters separate the clusters.

2. **Do morphology clusters carry an electrophys signature?** Run PCA + K-means on the 14-d
   morphology vectors, then for each cluster summarise the electrophys parameter distributions.
   Report which electrophys parameters separate the clusters.

3. **Which combinations of the 68 input parameters drive DSI and PD diversity in this strict
   cohort?** Run factor analysis (varimax) on the full 68-d matrix, project DSI and PD onto factors
   via Pearson r, and identify joint-DSI/PD factors (if any).

## Key Questions

1. Are the K-means clusters on the electrophys submatrix separable on morphology — i.e. do channel
   regimes carry a morphology signature?
2. Are the K-means clusters on the morphology submatrix separable on electrophys — i.e. do
   morphology shapes carry a channel regime signature?
3. Which top-3 varimax factors load most strongly on DSI? On PD-rate? Is there a single joint factor
   with `|r_DSI| > 0.3 AND |r_PD| > 0.3`?
4. Compared to t0105's looser-cohort findings, do the dominant axes change when restricted to
   genuinely high-performing cells (DSI > 0.5 AND PD > 10)?

## Approach

### Cell selection

Pool all evaluations from the single t0106 lineage:

* `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`

**Filter**: `dsi_vector_sum > 0.5 AND pd_rate_hz > 10.0`.

**Dedupe**: by full 68-d parameter vector rounded to 6 decimals. Pareto carry-over across
generations creates many duplicate rows. Pre-scoping count: **784 raw passing rows → 150 unique**.

Record `N_raw`, `N_passing`, `N_unique` in `metrics.json` and `results_summary.md`.

### PCA + K-means on electrophys (54-d) with morphology overlays

1. Stack the 54-d electrophys submatrix `X_e` shape `(150, 54)`.
2. z-score each column.
3. PCA: keep PC1, PC2, PC3. Report variance explained and top-5 loading dimensions per PC.
4. K-means with `k ∈ {2, 3, 4}` on the full z-scored 54-d matrix (not on the PCA projection —
   using the full feature space gives a more honest clustering). Pick the headline `k` using the
   elbow on inertia and silhouette score; report all three.
5. Plot:
   * PC1-PC2 scatter coloured by cluster label.
   * For each morphology parameter, a boxplot grouped by cluster (one row of 14 panels).
6. For each morphology parameter, run a Kruskal-Wallis test across clusters; report H statistic and
   p-value. Bonferroni-correct across 14 tests; flag parameters that remain significant after
   correction.

### PCA + K-means on morphology (14-d) with electrophys overlays

1. Stack the 14-d morphology submatrix `X_m` shape `(150, 14)`.
2. z-score each column.
3. PCA: keep PC1, PC2, PC3. Report variance explained and top-5 loading dimensions per PC.
4. K-means with `k ∈ {2, 3, 4}` on the full z-scored 14-d matrix. Pick headline `k` from
   silhouette
   + elbow.
5. Plot:
   * PC1-PC2 scatter coloured by cluster label.
   * For each electrophys parameter, a strip plot or violin grouped by cluster. With 54 panels this
     becomes large; render as a compact grid sized for legibility.
6. For each electrophys parameter, run Kruskal-Wallis across clusters; report H and p with
   Bonferroni correction across 54 tests; flag survivors.

### Factor analysis on the full 68-d matrix

1. Stack the 68-d full vectors into `X_full` shape `(150, 68)`.
2. z-score each column.
3. Run `sklearn.decomposition.FactorAnalysis` followed by varimax rotation (use `factor_analyzer`
   package if installed, else manual varimax routine).
4. Choose factor count by Kaiser criterion (eigenvalues > 1 on the correlation matrix) OR 80% of
   total variance, whichever gives fewer factors, capped at 10.
5. For each factor, list the top-5 loading parameters with signed loadings.
6. Compute factor scores per cell. Compute Pearson r between each factor and `dsi_vector_sum` and
   between each factor and `pd_rate_hz`.
7. Flag any factor with `|r_DSI| > 0.3 AND |r_PD| > 0.3` as a joint factor.

Outputs:
* `results/images/factor_loadings_heatmap.png`
* `results/images/factor_correlations_dsi_pd.png`

### Answer assets

1. `assets/answer/t0106-electrophys-clusters-morphology-signature/`
   * Q: "When t0106 cells with DSI > 0.5 AND PD > 10 are clustered by their 54-d electrophys
     parameters, do the clusters carry a distinguishable morphological signature?"
2. `assets/answer/t0106-morphology-clusters-electrophys-signature/`
   * Q: "When the same cells are clustered by their 14-d morphology parameters, do the clusters
     carry a distinguishable electrophys signature?"
3. `assets/answer/t0106-dsi-pd-factor-decomposition-strict-cohort/`
   * Q: "Which factors (combinations of the 68 input parameters) explain DSI and PD diversity in the
     strict cohort (DSI > 0.5 AND PD > 10), and is there a joint factor?"

## Out of Scope

* Re-running NSGA-II or any optimisation.
* Pooling across lineages other than t0106.
* Morphology gallery (separately covered in t0105_preliminary_figures_report and earlier).
* In-silico patch / IV-curve analysis on cluster representatives.
* Comparison to external datasets (Bae 2018, Ran 2020).
