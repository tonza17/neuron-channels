# Pooled PCA + Cluster + Factor Analysis of DSI>0.7 / PD>10 Cells Across 4 Seeds

## Motivation

The S-0112-01 substrate-rate batch is now complete (t0106, t0112, t0113, t0114, t0115 — five
independent NSGA-II seeds replicating the 68-d Bed-B + morphology DSGC substrate). t0108 ran a PCA +
K-means + varimax factor analysis on the t0106-only joint-pass cohort and identified a 4-cluster
morphology partition (followed up by t0109's gallery and t0110's relaxed-cohort sensitivity check).
All of t0108's structure is single-seed by construction; the present task extends the same machinery
to four seeds simultaneously to test whether the joint-pass corner is one connected basin or several
disjoint sub-basins, and to quantify how far the survivors moved from their random gen-0
initialisations.

This task is the analytical complement to S-0113-08 ("Cross-seed 68-d signature of silence-guard
cells: same parameter basin or seed-specific artefacts?") and S-0115-07 ("Investigate the seed-44 /
seed-7755 / seed-9354 rich-yield parameter signature") — it operates on the survivor pool from
those seeds and uses unsupervised methods rather than ANOVA-style contrasts.

## Scope

### Data sources (4 NSGA-II runs, frozen predictions assets)

* `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/`
  — seed 44, the original t0106 long run
* `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz`
  — seed 77
* `tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/files/` —
  seed 7755
* `tasks/t0115_seed9354_no_autostop/assets/predictions/t0115-bedb-morph-nsga2-seed9354/files/` —
  seed 9354

t0113 (seed 2247) is intentionally excluded for this first cut — the four selected seeds use the
identical no-autostop / pool-restart-every-10 configuration introduced in t0114 (and t0106 / t0112
are the canonical reference points). If the analysis flags four-seed coverage as too narrow during
implementation, t0113 can be added as a correction.

### Cohort filter

For every loaded evaluation:

* `dsi_vector_sum > 0.7` AND
* `pd_rate_hz > 10.0`

Both inequalities are strict. The implementation must record per-seed counts before and after the
filter and report them in `results_detailed.md`.

### Feature vector

Each survivor cell is represented by its `vector_68d`:

* Indices 0..53 — 54-d electrophys subspace (channel densities, kinetics, synaptic conductances,
  passive params; same layout as t0106 / t0108)
* Indices 54..67 — 14-d morphology subspace (`MorphologyParams` fields as in
  `scratch_t0112_top15_morphologies.py`)

Feature names must be carried alongside the matrix from load time onward — no hard-coded magic
index lists outside the load module.

### Analyses to run

1. **Combined 68-d PCA + side panels (one figure, three subplots).**
   * Main panel: PC1 vs PC2 of the standardised 68-d filtered pool. Points coloured by source seed
     (4 colours). Marker shape encodes joint-pass (DSI>0.7 ∧ PD>10) — all retained cells are
     joint-pass by construction, so all use the filled circle.
   * Side panel A: PC1 vs PC2 of the 54-d electrophys-only PCA, same colouring.
   * Side panel B: PC1 vs PC2 of the 14-d morphology-only PCA, same colouring.
   * Each subplot reports `% variance explained` for PC1 and PC2 in axis labels.
   * Saved to `results/images/pca_combined.png`.

2. **Gen-0 random-init overlay on the same PCA axes.**
   * For each seed, load the generation-0 individuals from the same `all_evaluations.json(.gz)` and
     project them onto the PCA fitted in step 1 (no refit). Render as faint grey crosses beneath the
     survivor scatter.
   * Saved to `results/images/pca_with_gen0_overlay.png`.
   * Also compute per-seed mean Euclidean displacement in PC1+PC2 space (survivors vs gen-0 mean)
     and tabulate in `results_detailed.md`.

3. **KMeans on 54-d electrophys subspace, auto-pick k ∈ [3, 7] by silhouette.**
   * Standardise the 54-d subspace before clustering.
   * Pick the k that maximises mean silhouette score across the candidate range.
   * Report silhouette curve, chosen k, and cluster sizes by seed.
   * Saved to `results/images/electrophys_silhouette.png` and
     `results/data/electrophys_clusters.csv`.
   * For each cluster, render dendritic morphologies of 15 representative cells in a 5×3 grid (full
     dendrite trees — not just somas — per the project preference established by t0114's
     morphology-grid backport). Representatives are sampled by top DSI × pd_rate_hz product within
     cluster (same selection rule as t0109).
   * Saved to `results/images/electrophys_cluster_<k>_morphs.png` (one PNG per cluster).

4. **KMeans on 14-d morphology subspace, auto-pick k ∈ [3, 7] by silhouette.**
   * Same procedure as step 3 on the morphology subspace.
   * Report silhouette curve, chosen k, and per-seed cluster sizes.
   * For each morphology cluster, write a 15-row table listing the representative cells with:
     `source_task`, `seed`, `generation`, `dsi_vector_sum`, `pd_rate_hz`, and a compact 6-number
     summary of the electrophys vector (PC1/PC2/PC3 loadings on the 54-d electrophys PCA fitted in
     step 1).
   * Saved to `results/data/morphology_cluster_<k>_representatives.csv`, and rendered as a markdown
     table in `results_detailed.md`.

5. **Factor analysis on the full 68-d feature matrix, Kaiser criterion.**
   * Standardise → fit `sklearn.decomposition.FactorAnalysis` with `n_components=68`, then retain
     factors with eigenvalue > 1 (use the eigenvalues of the correlation matrix, not the FA's
     internal noise variances, for the Kaiser cut).
   * Refit FA with the chosen number of factors and apply varimax rotation (consistent with t0108).
   * Render the loadings as a heatmap (factors × 68 features) with feature names on the y-axis,
     `RdBu_r` colourmap, symmetric vmin/vmax.
   * Saved to `results/images/factor_loadings_heatmap.png`.
   * Report variance explained per factor and total variance explained in `results_detailed.md`.

### Key questions (each becomes one `assets/answer/` asset)

1. **Cross-seed basin connectivity** — Does the joint-pass cohort form a single connected manifold
   in 68-d, or do the four seeds occupy seed-specific sub-basins? Evidence: PCA cluster overlap by
   seed, KMeans cluster purity by seed (chi-square or normalised mutual information between cluster
   label and seed label).
2. **Displacement from random init** — How far did NSGA-II travel from gen-0 in each seed?
   Evidence: per-seed mean and 95th-percentile Euclidean displacement in the 68-d standardised space
   and in PC1+PC2 space. Compare to gen-0 within-seed spread.
3. **Latent drivers of joint-pass quality** — Which factors (after varimax rotation) load most
   strongly on DSI and pd_rate_hz, and are they morphology-dominated, electrophys-dominated, or
   mixed? Evidence: factor loadings heatmap and per-factor correlation with DSI / pd_rate_hz.

## Approach

* Re-use `scratch_t0112_top15_morphologies.py` machinery for morphology rendering (full dendrite
  trees via `arf.tasks.t0090_*` and `t0092_*` generators). No new morphology code.
* Re-use the t0108 PCA / KMeans / FA pipeline as the starting template; the diff is "load from 4
  sources instead of 1" and "track seed label as a categorical column throughout".
* All loaded data is concatenated into a single pandas DataFrame keyed by
  `(source_task, seed, generation, individual_idx)` and saved to
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/data/pooled_survivors.parquet` for downstream
  reproducibility. Gen-0 individuals are stored separately in `data/pooled_gen0.parquet`.

## Expected Outputs

### Assets

* `assets/answer/<answer_id_1>/` — basin-connectivity question
* `assets/answer/<answer_id_2>/` — displacement-from-init question
* `assets/answer/<answer_id_3>/` — latent-drivers question

### Charts (all under `results/images/`, all embedded in `results_detailed.md`)

| File | Axes / Content | Answers |
| --- | --- | --- |
| `pca_combined.png` | 3-panel: combined PC1/PC2, electrophys PC1/PC2, morphology PC1/PC2; coloured by seed | Q1 |
| `pca_with_gen0_overlay.png` | Same combined PCA with gen-0 crosses underneath | Q2 |
| `electrophys_silhouette.png` | k (x) vs mean silhouette (y) for k∈[3,7] | Q1 |
| `electrophys_cluster_1_morphs.png` … `electrophys_cluster_K_morphs.png` | 5×3 grid of full dendrite trees | Q1, Q3 |
| `morphology_silhouette.png` | k (x) vs mean silhouette (y) for k∈[3,7] | Q1 |
| `factor_loadings_heatmap.png` | factors (x) × 68 features (y), RdBu_r diverging | Q3 |

### Tables (rendered in `results_detailed.md`, raw under `results/data/`)

* Per-seed cohort counts (before / after filter)
* Electrophys cluster sizes by seed
* Morphology cluster sizes by seed
* Per-cluster representative listings (15 rows × {source_task, seed, gen, DSI, PD, e-phys PC1/2/3})
  for both partitions
* Variance explained per retained factor

## Compute and Budget

CPU-only analysis. Pandas + scikit-learn + matplotlib only. No remote machines. Wall-clock estimate
~30 minutes for load + all analyses + plotting; budget for paid services: $0.

## Cross-References

* **Methodology precedent**: t0108 (single-seed version of the same pipeline), t0109 (morphology
  gallery sampling rule), t0110 (relaxed-cohort sensitivity).
* **Source data**: t0106, t0112, t0114, t0115. t0113 (seed 2247) is excluded from this first cut but
  eligible for inclusion via correction if the four-seed view is judged insufficient.
* **Related open suggestions**: S-0113-08, S-0115-07.

## Verification Criteria

* `pooled_survivors.parquet` row count equals the sum of per-seed survivor counts logged at load
  time.
* Every PCA / KMeans / FA fit uses the standardiser fitted on the union pool (not per-seed) so
  cross-seed comparisons are well-defined.
* Every chart referenced in `results_detailed.md` exists on disk.
* Every claim in the three answer assets is grounded in a specific table or chart in
  `results_detailed.md`.
