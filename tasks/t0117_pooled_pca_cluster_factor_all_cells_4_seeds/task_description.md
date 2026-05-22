# Pooled PCA + Cluster + Factor Analysis of ALL Cells Across 4 Seeds (no DSI/PD filter)

## Motivation

t0116 ran the canonical PCA + KMeans + varimax factor analysis pipeline on the 869 dedup-unique
cells that pass `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` across four NSGA-II seeds (t0106 s44,
t0112 s77, t0114 s7755, t0115 s9354). It found that the four-seed cohort fragments into
seed-specific sub-basins (electrophys KMeans NMI = 0.929; morphology KMeans NMI = 0.889) and that no
single factor crosses |r| > 0.3 on both DSI and PD simultaneously (the "truncated-cohort artefact"
first documented in t0110).

This task asks the immediate follow-up: what happens when we lift the cohort filter entirely? Does
the seed-specific basin pattern persist when every evaluation is in the pool, or does the cross-seed
manifold reconnect once low-DSI / low-PD cells are admitted? And does at least one varimax factor
recover a joint DSI-PD axis once the full quality range is back in the data?

## Scope

### Data sources (4 NSGA-II runs, same as t0116)

* `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`
  — seed 44
* `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz`
  — seed 77
* `tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/files/predictions.jsonl.gz`
  — seed 7755
* `tasks/t0115_seed9354_no_autostop/assets/predictions/t0115-bedb-morph-nsga2-seed9354/files/predictions.jsonl.gz`
  — seed 9354

t0113 (seed 2247) remains intentionally excluded so the only methodological change vs t0116 is the
cohort filter.

### Pool definition

* Every record from every source loaded (no DSI / PD filter)
* Deduplicated by the 68-d vector rounded to 6 decimals (same convention as t0116)
* Expected pool size after dedup: ~14k cells (vs t0116's 869)
* Per-seed counts must be recorded before and after dedup and reported in `results_detailed.md`

### Feature vector

Identical to t0116: 68-d `vector_68d` with indices 0–53 the 54-d Bed-B electrophys vector and
54–67 the 14-d morphology vector. Authoritative names in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` `ALL_PARAM_NAMES`.

### Analyses to run (mirror t0116 exactly, sans cohort filter)

1. **Combined 68-d PCA + side panels (one figure, three subplots).** Combined / electrophys-only /
   morphology-only PC1 vs PC2, coloured by source seed (tab10 [0..3]). Each subplot reports
   `% variance explained` for PC1 and PC2 in its axis labels. Saved to
   `results/images/pca_combined.png`.
2. **Gen-0 (`generation == 1`) random-init overlay.** Same axes, with gen-0 individuals projected
   onto the PCAs fitted in Step 1 (no refit; reuse the standardiser). Compute per-seed mean and
   95th-percentile Euclidean displacement in PC1+PC2 space and in 68-d standardised space. Saved to
   `results/images/pca_with_gen0_overlay.png` and `results/data/gen0_displacement.csv`.
3. **KMeans on 54-d electrophys subspace, auto-pick k ∈ [3, 7] by silhouette.** Standardiser fit
   on the union pool. Pick k by maximum mean silhouette. Report silhouette curve, chosen k, and
   per-seed cluster sizes. Saved to `results/images/electrophys_silhouette.png` and
   `results/data/electrophys_clusters.csv`. For each cluster render a 5×3 grid of 15 representative
   cells (full dendrite trees via NEURON pt3d — not just somas; project preference per t0114's
   morphology-grid backport). Representatives ranked by `dsi_vector_sum * pd_rate_hz` within cluster
   (canonical t0109 / t0116 rule). Saved to `results/images/electrophys_cluster_<k>_morphs.png` (one
   PNG per cluster).
4. **KMeans on 14-d morphology subspace, auto-pick k ∈ [3, 7] by silhouette.** Same procedure on
   the morphology subspace. For each morphology cluster, write a 15-row representative table with
   `(source_task, seed, generation, dsi_vector_sum, pd_rate_hz, ephys_PC1, ephys_PC2, ephys_PC3)`
   where the `ephys_PC*` values come from the 54-d electrophys PCA fit in Step 1. Saved to
   `results/data/morphology_cluster_<k>_representatives.csv`.
5. **Factor analysis on the full 68-d feature matrix, Kaiser criterion, varimax-rotated.**
   Standardise → fit `sklearn.decomposition.FactorAnalysis(n_components=68)`; count Kaiser
   eigenvalues > 1 from the correlation matrix; cap at `KAISER_FACTOR_CAP = 10` (inherited from
   t0108); refit FA with the chosen count; apply varimax rotation via the iterative-SVD helper from
   t0108. Render the loadings heatmap with `RdBu_r` colourmap and symmetric vmin/vmax to
   `results/images/factor_loadings_heatmap.png`. Report per-factor variance and Pearson r vs DSI /
   PD in `results/data/factor_correlations.csv`.

### Key questions (each becomes one `assets/answer/` asset)

1. **Cross-seed basin connectivity without the cohort filter** — Does the unfiltered pool form a
   connected manifold across seeds, or does the seed-specific basin pattern from t0116 persist when
   low-DSI / low-PD cells are admitted? Evidence: KMeans cluster purity by seed (NMI, chi-square
   contingency) for both the ephys-k and morph-k partitions, plus visual PCA overlap. Direct
   head-to-head comparison: t0117 NMI vs t0116 NMI, on the same partition.
2. **Truncated-cohort artefact test** — Does at least one varimax factor recover a joint DSI-PD
   axis (|r| > 0.3 on both `dsi_vector_sum` AND `pd_rate_hz`) when the full quality range is in the
   pool? If yes, the t0110 / t0116 truncated-cohort artefact is confirmed: the strict cohort
   genuinely erases a shared latent. If no, the decoupling is intrinsic and survives even in the
   unfiltered pool.
3. **Displacement from random init in the full pool** — Re-compute the gen-0 displacement on the
   unfiltered pool. Is the per-seed displacement pattern (seed 44 furthest, seed 9354 closest in PC
   space, found in t0116) preserved when all cells — not only the high-quality survivors —
   contribute to the PCA fit? Compare t0117 displacements directly to t0116 displacements.

## Approach

* Re-use every code module from `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/` verbatim,
  with **one change**: `code/load_pooled_cells.py` drops the
  `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` filter. Everything else (loader format-branching,
  gen-0 = `generation == 1` convention, union-pool standardiser, NEURON pt3d morphology rendering,
  varimax + Kaiser cap = 10, cluster representative selection rule) is unchanged. Per the cross-task
  import rule, code is copied into this task's `code/` directory rather than imported.
* Pool the standardiser, all PCAs, all KMeans models, and the FA on the full unfiltered union pool
  — never per-seed.
* `data/pooled_all_cells.parquet` (the new ~14k-row pool) and `data/pooled_gen0.parquet` (still 384
  rows = 96 × 4 seeds) are persisted for downstream reproducibility.
* Expected runtime is somewhat longer than t0116 (~14k vs ~870 cells); silhouette score is O(n²) so
  the KMeans sweep dominates wall-clock. Estimate ~60–90 minutes.

## Expected Outputs

### Assets

* `assets/answer/<answer_id_1>/` — basin-connectivity-without-filter question
* `assets/answer/<answer_id_2>/` — truncated-cohort-artefact-test question
* `assets/answer/<answer_id_3>/` — displacement-from-init-full-pool question

### Charts (under `results/images/`)

* `pca_combined.png`, `pca_with_gen0_overlay.png`
* `electrophys_silhouette.png`, `morphology_silhouette.png`
* `electrophys_cluster_<k>_morphs.png` (one per ephys cluster)
* `factor_loadings_heatmap.png`

### Tables (under `results/data/`)

* `per_seed_pool_counts.csv` (raw + dedup-unique per seed)
* `gen0_displacement.csv`
* `electrophys_clusters.csv`, `morphology_clusters.csv`
* `morphology_cluster_<k>_representatives.csv` (one per morph cluster)
* `cluster_seed_purity.csv`, `factor_correlations.csv`, `factor_loadings.csv`
* `methodology_notes.md`

### Direct comparison vs t0116

`results_detailed.md` must include a "Comparison vs t0116" subsection with at least:

* Side-by-side table of pool sizes, KMeans k chosen, per-partition NMI, per-partition silhouette,
  varimax factor count, total variance explained, and joint-factor count (|r| > 0.3 on both).
* Side-by-side per-seed displacement table (mean PC1+PC2, mean 68-d).
* Plain-English verdict for each of the 3 questions: "t0116 said X; t0117 says Y; the
  truncated-cohort artefact / basin pattern is confirmed / refuted because Z."

## Compute and Budget

CPU-only. No remote machines. ~60–90 minutes wall-clock (KMeans + silhouette on ~14k cells
dominates). $0 paid services. No new dependencies.

## Cross-References

* **Methodology precedent**: t0116 (strict-cohort version of the same pipeline) — every code
  module is reused verbatim except the cohort filter.
* **Source data**: t0106, t0112, t0114, t0115.
* **Truncated-cohort artefact context**: t0108 (DSI > 0.5 cut), t0110 (relaxed cohort follow-up),
  and t0116's latent-drivers answer asset (`pooled-survivors-latent-drivers-dsi07-pd10`).
* **Related open suggestions**: S-0116-02 (relaxed DSI > 0.5) — this task is broader (no filter at
  all), so it complements rather than duplicates that suggestion.

## Verification Criteria

* `data/pooled_all_cells.parquet` row count equals the sum of per-seed dedup-unique counts logged at
  load time.
* Every PCA / KMeans / FA fit uses the standardiser fitted on the union pool (not per-seed).
* Every chart referenced in `results_detailed.md` exists on disk.
* Every claim in the three answer assets is grounded in a specific table or chart in
  `results_detailed.md`.
* Headline NMI and joint-factor counts must be reported even if they confirm the t0116 finding (no
  result-suppression). The "Comparison vs t0116" subsection must include both pass and fail outcomes
  for every question.
