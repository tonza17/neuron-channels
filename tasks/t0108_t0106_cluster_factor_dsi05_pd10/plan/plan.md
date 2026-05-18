# t0108 — Plan

## Objective

For 150 unique t0106 cells passing `DSI > 0.5 AND PD-rate > 10 Hz`: run PCA + K-means on the 54-d
electrophys submatrix (with 14-d morphology overlays), PCA + K-means on the 14-d morphology
submatrix (with 54-d electrophys overlays), and varimax factor analysis on the full 68-d vector with
Pearson r against DSI and PD.

## Approach

Single-lineage analysis on `t0106_long_pdnd_nsga2_300gen` only — no cross-lineage pooling. Strict
filter `DSI > 0.5 AND PD > 10 Hz`. Dedupe by full 68-d vector at 6 decimal precision.

PCA via `sklearn.decomposition.PCA`. K-means via `sklearn.cluster.KMeans` (random_state=42, n_init
"auto"). Sweep `k ∈ {2, 3, 4}` on the z-scored full feature space; pick headline `k` from
silhouette maximum.

Factor analysis via `sklearn.decomposition.FactorAnalysis`; varimax rotation via the closed-form
iterative routine implemented in `code/factor_analysis.py` (same as t0105).

Significance tests: Kruskal-Wallis (`scipy.stats.kruskal`) across cluster labels per parameter,
Bonferroni-corrected over the parameter count.

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Local compute (PCA + K-means + factor analysis on 150 cells) | < 10 minutes |
| API costs | $0 |
| Vast.ai | $0 |
| **Predicted spend** | **$0** |
| **Hard cap** | **$0** |

## Step by Step

1. Filter t0106 evaluations: `code/load_filter_cells.py` → `results/data/filtered_cells.json`.
2. PCA + K-means on electrophys (54-d) with morphology overlays: `code/cluster_electrophys.py` →
   `results/data/electrophys_clusters.json`, `results/images/pca_electrophys_*.png`,
   `results/images/morph_overlay_by_electrophys_cluster.png`.
3. PCA + K-means on morphology (14-d) with electrophys overlays: `code/cluster_morphology.py` →
   `results/data/morphology_clusters.json`, `results/images/pca_morphology_*.png`,
   `results/images/electrophys_overlay_by_morphology_cluster.png`.
4. Factor analysis on full 68-d: `code/factor_analysis.py` → `results/data/factor_analysis.json`,
   `results/images/factor_loadings_heatmap.png`, `results/images/factor_correlations_dsi_pd.png`.
5. Build `metrics.json` and 3 answer assets.
6. Write `results_summary.md`, `results_detailed.md`, run verificators.

## Remote Machines

None. Local compute only.

## Assets Needed

* `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz` (3,744 rows).

## Expected Assets

* 3 answer assets:
  * `t0106-electrophys-clusters-morphology-signature`
  * `t0106-morphology-clusters-electrophys-signature`
  * `t0106-dsi-pd-factor-decomposition-strict-cohort`

## Time Estimation

* Implementation: 60-90 min.
* Reporting + answer assets: 30-45 min.
* **Total**: 1.5-2.5 hours wall clock.

## Risks & Fallbacks

* **Risk**: K-means cluster count is unclear; silhouette and elbow disagree. **Fallback**: report
  `k=2` headline; also report `k=3` and `k=4` in the appendix.
* **Risk**: factor analysis with 150 samples and 68 features is borderline. **Fallback**: report
  scree and stability via 100-bootstrap loading recovery; constrain interpretation to top-3 factors.
* **Risk**: Bonferroni at 54 tests is harsh; some real effects may be missed. **Fallback**: also
  report Benjamini-Hochberg FDR-corrected p-values.
* **Risk**: variant_id collision with t0105 metric variants. **Fallback**: prefix all variants with
  `t0108_`.

## Verification Criteria

* `verify_task_metrics t0108_t0106_cluster_factor_dsi05_pd10` passes with 0 errors.
* `verify_task_results t0108_t0106_cluster_factor_dsi05_pd10` passes with 0 errors.
* All 3 answer assets validate against `verify_answer_asset`.
* All charts in `results/images/` are PNG and embedded in `results_detailed.md` via
  `![desc](images/file.png)`.
* `metrics.json` numbers match `results_detailed.md` exactly.

## Task Requirement Checklist (REQ)

* **REQ-1**: Filter `t0106_long_pdnd_nsga2_300gen` evaluations with
  `dsi_vector_sum > 0.5 AND pd_rate_hz > 10`. Dedupe by 68-d vector at 6 decimals. Record `N_raw`,
  `N_passing`, `N_unique`.
* **REQ-2**: PCA on z-scored 54-d electrophys submatrix; keep PC1-3; report variance explained and
  top-5 loadings per PC.
* **REQ-3**: K-means on z-scored 54-d electrophys submatrix at `k ∈ {2, 3, 4}`; report inertia and
  silhouette; pick headline `k`.
* **REQ-4**: For each electrophys cluster, summarise the 14 morphology parameters (mean, median,
  std). Kruskal-Wallis across clusters per morphology parameter, Bonferroni-corrected.
* **REQ-5**: PCA on z-scored 14-d morphology submatrix; keep PC1-3; report variance explained and
  top-5 loadings per PC.
* **REQ-6**: K-means on z-scored 14-d morphology submatrix at `k ∈ {2, 3, 4}`; report inertia and
  silhouette; pick headline `k`.
* **REQ-7**: For each morphology cluster, summarise the 54 electrophys parameters. Kruskal-Wallis
  across clusters per electrophys parameter, Bonferroni-corrected.
* **REQ-8**: Factor analysis (varimax) on z-scored full 68-d matrix. Factor count by Kaiser OR 80%
  variance, capped at 10.
* **REQ-9**: Pearson r between each factor score and `dsi_vector_sum`; same for `pd_rate_hz`. Top-3
  factors by `|r|` per outcome. Flag joint factors with `|r_DSI| > 0.3 AND |r_PD| > 0.3`.
* **REQ-10**: Three answer assets validated by `verify_answer_asset`.
* **REQ-11**: All charts embedded in `results_detailed.md` via `![desc](images/file.png)`.
