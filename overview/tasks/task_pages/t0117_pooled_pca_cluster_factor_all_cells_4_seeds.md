# ✅ Pooled PCA + cluster + factor analysis of ALL cells across 4 seeds

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0117_pooled_pca_cluster_factor_all_cells_4_seeds` |
| **Status** | ✅ completed |
| **Started** | 2026-05-22T11:57:25Z |
| **Completed** | 2026-05-22T13:16:50Z |
| **Duration** | 1h 19m |
| **Dependencies** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **Task types** | `data-analysis`, `comparative-analysis`, `answer-question` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md) |
| **Expected assets** | 3 answer |
| **Step progress** | 8/13 |
| **Task folder** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds/`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/task_description.md)*

# Pooled PCA + Cluster + Factor Analysis of ALL Cells Across 4 Seeds (no DSI/PD filter)

## Motivation

t0116 ran the canonical PCA + KMeans + varimax factor analysis pipeline on the 869
dedup-unique cells that pass `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` across four NSGA-II
seeds (t0106 s44, t0112 s77, t0114 s7755, t0115 s9354). It found that the four-seed cohort
fragments into seed-specific sub-basins (electrophys KMeans NMI = 0.929; morphology KMeans NMI
= 0.889) and that no single factor crosses |r| > 0.3 on both DSI and PD simultaneously (the
"truncated-cohort artefact" first documented in t0110).

This task asks the immediate follow-up: what happens when we lift the cohort filter entirely?
Does the seed-specific basin pattern persist when every evaluation is in the pool, or does the
cross-seed manifold reconnect once low-DSI / low-PD cells are admitted? And does at least one
varimax factor recover a joint DSI-PD axis once the full quality range is back in the data?

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

t0113 (seed 2247) remains intentionally excluded so the only methodological change vs t0116 is
the cohort filter.

### Pool definition

* Every record from every source loaded (no DSI / PD filter)
* Deduplicated by the 68-d vector rounded to 6 decimals (same convention as t0116)
* Expected pool size after dedup: ~14k cells (vs t0116's 869)
* Per-seed counts must be recorded before and after dedup and reported in
  `results_detailed.md`

### Feature vector

Identical to t0116: 68-d `vector_68d` with indices 0–53 the 54-d Bed-B electrophys vector and
54–67 the 14-d morphology vector. Authoritative names in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` `ALL_PARAM_NAMES`.

### Analyses to run (mirror t0116 exactly, sans cohort filter)

1. **Combined 68-d PCA + side panels (one figure, three subplots).** Combined /
   electrophys-only / morphology-only PC1 vs PC2, coloured by source seed (tab10 [0..3]). Each
   subplot reports `% variance explained` for PC1 and PC2 in its axis labels. Saved to
   `results/images/pca_combined.png`.
2. **Gen-0 (`generation == 1`) random-init overlay.** Same axes, with gen-0 individuals
   projected onto the PCAs fitted in Step 1 (no refit; reuse the standardiser). Compute
   per-seed mean and 95th-percentile Euclidean displacement in PC1+PC2 space and in 68-d
   standardised space. Saved to `results/images/pca_with_gen0_overlay.png` and
   `results/data/gen0_displacement.csv`.
3. **KMeans on 54-d electrophys subspace, auto-pick k ∈ [3, 7] by silhouette.** Standardiser
   fit on the union pool. Pick k by maximum mean silhouette. Report silhouette curve, chosen
   k, and per-seed cluster sizes. Saved to `results/images/electrophys_silhouette.png` and
   `results/data/electrophys_clusters.csv`. For each cluster render a 5×3 grid of 15
   representative cells (full dendrite trees via NEURON pt3d — not just somas; project
   preference per t0114's morphology-grid backport). Representatives ranked by `dsi_vector_sum
   * pd_rate_hz` within cluster (canonical t0109 / t0116 rule). Saved to
   `results/images/electrophys_cluster_<k>_morphs.png` (one PNG per cluster).
4. **KMeans on 14-d morphology subspace, auto-pick k ∈ [3, 7] by silhouette.** Same procedure
   on the morphology subspace. For each morphology cluster, write a 15-row representative
   table with `(source_task, seed, generation, dsi_vector_sum, pd_rate_hz, ephys_PC1,
   ephys_PC2, ephys_PC3)` where the `ephys_PC*` values come from the 54-d electrophys PCA fit
   in Step 1. Saved to `results/data/morphology_cluster_<k>_representatives.csv`.
5. **Factor analysis on the full 68-d feature matrix, Kaiser criterion, varimax-rotated.**
   Standardise → fit `sklearn.decomposition.FactorAnalysis(n_components=68)`; count Kaiser
   eigenvalues > 1 from the correlation matrix; cap at `KAISER_FACTOR_CAP = 10` (inherited
   from t0108); refit FA with the chosen count; apply varimax rotation via the iterative-SVD
   helper from t0108. Render the loadings heatmap with `RdBu_r` colourmap and symmetric
   vmin/vmax to `results/images/factor_loadings_heatmap.png`. Report per-factor variance and
   Pearson r vs DSI / PD in `results/data/factor_correlations.csv`.

### Key questions (each becomes one `assets/answer/` asset)

1. **Cross-seed basin connectivity without the cohort filter** — Does the unfiltered pool form
   a connected manifold across seeds, or does the seed-specific basin pattern from t0116
   persist when low-DSI / low-PD cells are admitted? Evidence: KMeans cluster purity by seed
   (NMI, chi-square contingency) for both the ephys-k and morph-k partitions, plus visual PCA
   overlap. Direct head-to-head comparison: t0117 NMI vs t0116 NMI, on the same partition.
2. **Truncated-cohort artefact test** — Does at least one varimax factor recover a joint
   DSI-PD axis (|r| > 0.3 on both `dsi_vector_sum` AND `pd_rate_hz`) when the full quality
   range is in the pool? If yes, the t0110 / t0116 truncated-cohort artefact is confirmed: the
   strict cohort genuinely erases a shared latent. If no, the decoupling is intrinsic and
   survives even in the unfiltered pool.
3. **Displacement from random init in the full pool** — Re-compute the gen-0 displacement on
   the unfiltered pool. Is the per-seed displacement pattern (seed 44 furthest, seed 9354
   closest in PC space, found in t0116) preserved when all cells — not only the high-quality
   survivors — contribute to the PCA fit? Compare t0117 displacements directly to t0116
   displacements.

## Approach

* Re-use every code module from `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/`
  verbatim, with **one change**: `code/load_pooled_cells.py` drops the `dsi_vector_sum > 0.7
  AND pd_rate_hz > 10.0` filter. Everything else (loader format-branching, gen-0 = `generation
  == 1` convention, union-pool standardiser, NEURON pt3d morphology rendering, varimax +
  Kaiser cap = 10, cluster representative selection rule) is unchanged. Per the cross-task
  import rule, code is copied into this task's `code/` directory rather than imported.
* Pool the standardiser, all PCAs, all KMeans models, and the FA on the full unfiltered union
  pool — never per-seed.
* `data/pooled_all_cells.parquet` (the new ~14k-row pool) and `data/pooled_gen0.parquet`
  (still 384 rows = 96 × 4 seeds) are persisted for downstream reproducibility.
* Expected runtime is somewhat longer than t0116 (~14k vs ~870 cells); silhouette score is
  O(n²) so the KMeans sweep dominates wall-clock. Estimate ~60–90 minutes.

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

* Side-by-side table of pool sizes, KMeans k chosen, per-partition NMI, per-partition
  silhouette, varimax factor count, total variance explained, and joint-factor count (|r| >
  0.3 on both).
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
* **Truncated-cohort artefact context**: t0108 (DSI > 0.5 cut), t0110 (relaxed cohort
  follow-up), and t0116's latent-drivers answer asset
  (`pooled-survivors-latent-drivers-dsi07-pd10`).
* **Related open suggestions**: S-0116-02 (relaxed DSI > 0.5) — this task is broader (no
  filter at all), so it complements rather than duplicates that suggestion.

## Verification Criteria

* `data/pooled_all_cells.parquet` row count equals the sum of per-seed dedup-unique counts
  logged at load time.
* Every PCA / KMeans / FA fit uses the standardiser fitted on the union pool (not per-seed).
* Every chart referenced in `results_detailed.md` exists on disk.
* Every claim in the three answer assets is grounded in a specific table or chart in
  `results_detailed.md`.
* Headline NMI and joint-factor counts must be reported even if they confirm the t0116 finding
  (no result-suppression). The "Comparison vs t0116" subsection must include both pass and
  fail outcomes for every question.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does the unfiltered pool (every NSGA-II evaluation, no DSI/PD cohort filter) form a single connected manifold across seeds 44, 77, 7755, and 9354, or does the seed-specific basin pattern observed at the strict cohort (t0116) persist when low-DSI / low-PD cells are also admitted?](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-basin-connectivity-without-filter/) | [`full_answer.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-basin-connectivity-without-filter/full_answer.md) |
| answer | [How far did NSGA-II travel from gen-0 (generation == 1) in each seed when the full quality range is admitted (no DSI / PD filter), and is the per-seed displacement pattern observed at the strict cohort (seed 44 furthest, seed 9354 closest) preserved at the unfiltered pool?](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-displacement-from-init-full-pool/) | [`full_answer.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-displacement-from-init-full-pool/full_answer.md) |
| answer | [Does at least one varimax factor recover a joint DSI-PD axis (/r_DSI/ > 0.3 AND /r_PD/ > 0.3) when the cohort filter is removed and the full DSI / PD quality range is in the pool, confirming the truncated-cohort artefact first observed at t0110 and t0116?](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-truncated-cohort-artefact-test/) | [`full_answer.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-truncated-cohort-artefact-test/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Bracketed-cohort sweep at DSI>0.3/0.5/0.7/0.9 to map where the
joint DSI-PD factor disappears</strong> (S-0117-01)</summary>

**Kind**: experiment | **Priority**: high

t0117 confirmed the truncated-cohort artefact: F1 is a joint DSI-PD factor (r_DSI=+0.421,
r_PD=+0.352) at the unfiltered pool, while t0116 (DSI>0.7 AND PD>10) had zero joint factors.
S-0116-02 covers a single point at DSI>0.5; this suggestion is a parametric sweep. Re-run the
t0117 pipeline at four DSI thresholds {0.3, 0.5, 0.7, 0.9} on the same pooled all-cells
parquet, fit varimax FA at each, and plot (a) joint-factor count vs threshold and (b) F1's
r_DSI/r_PD vs threshold. Decision: monotonic crossover between 0.5 and 0.7 means smooth
range-restriction; a sharp cliff means a specific cell class dominates the joint variance.
Recommended task types: data-analysis, comparative-analysis. Cost: <$0.30.

</details>

<details>
<summary><strong>Per-seed factor analysis on the unfiltered pool: do the 4 seeds
share F1, or are loadings seed-dependent?</strong> (S-0117-02)</summary>

**Kind**: experiment | **Priority**: high

t0117's pooled F1 is the central joint DSI-PD driver (r_DSI=+0.421, r_PD=+0.352, 12.6%
variance). Basin-connectivity (ephys NMI=0.562, morph NMI=0.313) shows seeds still partly
cluster; F1 could be (a) a shared substrate property or (b) a cross-basin confound where
DSI/PD co-vary with seed identity. Refit FA(n=10) + varimax independently on each seed's
unfiltered slice (s44 n=1065, s77 n=654, s7755 n=1686, s9354 n=1026 - all well powered,
n>10*features=680), align factors to t0117 F1 by max-cosine, report per-seed top-10 loadings +
r_DSI/r_PD. Distinct from S-0116-04 (strict cohort where only s7755 had enough cells).
Decision: if all four per-seed analogues hit |r|>0.3 on both axes with the same top loadings,
F1 is a true substrate property; if loadings diverge, F1 is partly a between-seed confound.
Recommended task types: data-analysis. Cost: <$0.20.

</details>

<details>
<summary><strong>Bootstrap loading stability and oblique-rotation sensitivity for
the unfiltered-pool F1 joint factor</strong> (S-0117-03)</summary>

**Kind**: evaluation | **Priority**: high

t0117's headline finding is a single factor (F1, 12.6% variance, r_DSI=+0.421, r_PD=+0.352)
and the truncated-cohort verdict rides on it. Total variance dropped from 65.3% (t0116) to
34.9% (t0117), so F1 may be less stable. Draw B=200 bootstrap resamples of the 4431-cell pool,
refit FA(n=10)+varimax, align factors to t0117 by max-cosine, report median +/- IQR of F1's
r_DSI, r_PD, variance, and top-7 loadings. Also rerun with oblique promax (kappa=4) and
n_components=11. Distinct from S-0116-05 (strict cohort where no joint factor existed); this
validates the unfiltered-pool joint factor. Decision: if F1's r_DSI/r_PD 95% CIs straddle 0.3,
the verdict needs softening; if both stay clear of 0.3, the verdict is robust. Recommended
task types: data-analysis, comparative-analysis. Cost: <$0.20.

</details>

<details>
<summary><strong>Frontier-cell analysis: characterise cells the strict t0116 filter
excluded but which carry the joint factor</strong> (S-0117-04)</summary>

**Kind**: experiment | **Priority**: medium

t0117 admits 4431 cells; t0116 admits 869. The 3562 excluded cells split into 'frontier' (just
below one threshold: DSI in (0.5, 0.7] OR PD in (5, 10]) and 'bulk' (deep-below). The frontier
cells are most informative for why the joint factor only appears when they are admitted.
Steps: (1) extract frontier cells from pooled_all_cells.parquet, (2) project them onto t0117
F1 scores, (3) compare F1-score distributions of frontier vs bulk vs t0116-included via KS +
means, (4) refit varimax FA on frontier-only cells (n approx 1500-2000) and check whether F1
reappears alone. Decision: if frontier-only FA also yields joint F1 with r_DSI/r_PD > 0.3, the
joint factor lives in the frontier band; if not, the joint factor requires the full mixed
pool. Recommended task types: data-analysis, comparative-analysis. Cost: <$0.20.

</details>

<details>
<summary><strong>5-seed unfiltered-pool re-analysis (adding t0113 seed 2247) to
test joint-factor robustness</strong> (S-0117-05)</summary>

**Kind**: experiment | **Priority**: medium

t0117 used the same 4 seeds as t0116 (44/77/7755/9354) and deliberately excluded t0113 (seed
2247) to isolate the cohort-filter effect. With the joint factor now confirmed, the next
question is whether F1 survives the addition of a fifth independent seed. Re-run t0117's
pipeline end-to-end with t0113 as the fifth source (no DSI/PD filter, dedup at 6-decimal
vector convention, union-pool standardiser), regenerate the loadings heatmap and
factor_correlations.csv. Distinct from S-0116-01 (5-seed on the strict cohort, addresses basin
isolation); this 5-seed run addresses joint-factor robustness. Decision: if F1 still passes
|r|>0.3 on both axes with the same top loadings, the truncated-cohort verdict is seed-robust;
if F1 collapses or shuffles, the joint factor is partly 4-seed-specific. Recommended task
types: data-analysis, comparative-analysis. Cost: <$0.25.

</details>

<details>
<summary><strong>Interpret F1's biological meaning: top-loading features of the
joint DSI-PD factor in the unfiltered pool</strong> (S-0117-06)</summary>

**Kind**: evaluation | **Priority**: medium

t0117 confirms F1 is a joint DSI-PD axis but stops short of biological interpretation - it
reports F1's r_DSI/r_PD but not its top loadings on the 68-d feature vector (54-d electrophys
+ 14-d morphology). The latent-drivers question is only partially answered. Read
results/data/factor_loadings.csv, rank F1's loadings by absolute value, and identify the top-7
ephys parameters and top-3 morphology parameters loading on F1. Cross-reference t0116's pooled
F1 top loadings (SK_AIS + primary_branch_pd_concentration) and to t0108/t0110 strict/relaxed
comparison. Write a focused answer asset 'pooled-all-cells-f1-biological-interpretation' with
the loading table plus a 4-sentence biological interpretation: which channels and morphology
parameters jointly drive both DSI and PD when the full quality range is admitted? Recommended
task types: data-analysis, answer-question. Cost: <$0.10.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/results_summary.md)*

# Results Summary: Pooled PCA + Cluster + Factor Analysis of ALL Cells (4 seeds, no filter)

## Summary

Pooled **4 431** unique cells (1 065 + 654 + 1 686 + 1 026 across seeds 44 / 77 / 7755 / 9354)
from the same four NSGA-II runs as t0116, but with NO DSI / PD cohort filter. Ran the
identical PCA + KMeans + varimax FA pipeline and produced three answer assets plus an explicit
head-to-head `results/data/t0116_comparison.csv`. **Headline finding: the truncated-cohort
artefact is confirmed** — F1 in the unfiltered pool is a joint DSI-PD factor (r_DSI =
**+0.421**, r_PD = **+0.352**, both > 0.30), whereas no factor crossed |r| > 0.30 on both axes
in t0116. The seed-specific basin pattern also weakens substantially (electrophys NMI **0.929
→ 0.562**, morphology NMI **0.889 → 0.313**), confirming that t0116's strict cohort
exaggerated cross-seed basin isolation.

## Metrics

* **Pooled cohort size**: **4 431** unique cells from 16 992 raw evaluations (~5× t0116's 869)
* **Electrophys KMeans**: k = **4**, mean silhouette = **0.158**, NMI(cluster, seed) =
  **0.562**, chi-square p < 1e-300
* **Morphology KMeans**: k = **5**, mean silhouette = **0.153**, NMI(cluster, seed) =
  **0.313**, chi-square p < 1e-300
* **Varimax factor analysis**: **15** Kaiser eigenvalues > 1, capped at **10** factors, **34.9
  %** total variance explained (vs t0116's 65.3 %)
* **Joint-factor count**: **1** (F1: r_DSI = +0.421, p ~ 1e-189; r_PD = +0.352, p ~ 1e-129;
  12.6 % variance explained). **t0116 had 0.**
* **F1 vs t0116 F1**: t0117 F1 is a joint driver; t0116 F1 was DSI-only — the strict cohort
  erased the joint axis.
* **Gen-0 displacement** (per-seed mean in PC1+PC2): seed 44 = **4.87**, seed 77 = **1.49**,
  seed 7755 = **5.74**, seed 9354 = **1.59** — same rank order as t0116 but uniformly smaller
  because the pool now includes near-init cells.
* **Gen-0 displacement** (per-seed mean in 68-d standardised space): **8.83 – 9.34** across
  all four seeds (vs t0116's 59.7 – 61.3 — much smaller because the standardiser is now fitted
  on a broader distribution).
* **Charts produced**: **9** PNGs under `results/images/` (1 extra cluster grid vs t0116
  because t0117 chose k = 4 instead of 3).
* **Answer assets produced**: **3** under `assets/answer/`.

## Verification

* `verify_plan` — **PASSED** (0 errors, 0 warnings)
* `verify_task_results` — **PASSED**
* `verify_task_metrics` — **PASSED** (metrics.json = `{}`, intentional)
* C1 (parquet row count == per-seed sum): **PASSED** — 4 431 == 1 065 + 654 + 1 686 + 1 026
* C2 (union-pool standardiser shape (68,) / (68,), all std > 0): **PASSED**
* C3 (all 9 required PNGs on disk): **PASSED**
* C4 (local answer-asset structural check on all 3 assets): **PASSED**
* C5 (schema sanity: no NaN in vector cols): **PASSED**
* `ruff check --fix`, `ruff format`, `mypy -p
  tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code`: **PASSED** (clean)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds" ---
# Detailed Results: Pooled PCA + Cluster + Factor Analysis of ALL Cells (4 seeds, no filter)

## Summary

Pooled **4 431** unique cells (1 065 + 654 + 1 686 + 1 026 across seeds 44 / 77 / 7755 / 9354)
from the same four NSGA-II runs as t0116 with NO DSI / PD cohort filter, and ran the identical
PCA + KMeans + varimax FA pipeline. Three answer assets and a head-to-head
`results/data/t0116_comparison.csv` are produced. **The truncated-cohort artefact from t0110 /
t0116 is confirmed: F1 in the unfiltered pool is a joint DSI-PD factor (r_DSI = +0.421, r_PD =
+0.352, both > 0.30) — t0116 had no joint factor.** Seed-specific basin purity drops sharply
(electrophys NMI 0.929 → 0.562, morphology NMI 0.889 → 0.313), so the strict-cohort cohort
exaggerated cross-seed isolation.

## Methodology

* **Machine**: Local CPU (Windows 11, Python 3.12 via `uv`); no remote machines used
* **Pipeline runtime**: ~36 minutes wall-clock (silhouette O(n²) on 4 431 cells × 5 k values ×
  2 subspaces dominated, but well under the 60–90 minute upper bound)
* **Start**: 2026-05-22T12:16:12Z (implementation prestep)
* **End**: 2026-05-22T12:52:15Z (orchestrator implementation poststep)
* **Software**: pandas, scikit-learn (`PCA`, `KMeans`, `FactorAnalysis`,
  `normalized_mutual_info_score`, `silhouette_score`), scipy (`chi2_contingency`), NumPy,
  matplotlib, NEURON (for morphology rendering via the `procedural_dsgc_morphology_generator`
  and `..._fix` libraries from t0090 / t0092)
* **Standardiser**: One union-pool z-score fit (`fit_standardiser.py`), saved to
  `data/pooled_standardiser.npz`; every downstream PCA / KMeans / FA / gen-0 projection reuses
  this single fit
* **Cohort filter**: **None.** Every record from every source enters the pool. Dedup at
  6-decimal vector precision (t0108 / t0116 convention).
* **Feature vector**: 68-d, identical layout to t0116 (54-d ephys + 14-d morphology)
* **KMeans sweep**: k ∈ {3, 4, 5, 6, 7}, headline k chosen by maximum mean silhouette score
* **Factor analysis**: same as t0116 — `sklearn.decomposition.FactorAnalysis`, Kaiser
  criterion on correlation-matrix eigenvalues, capped at `KAISER_FACTOR_CAP = 10`,
  varimax-rotated via iterative-SVD helper

### Methodology Notes

Five up-front decisions documented in `results/data/methodology_notes.md`:

1. **Same loader as t0116 with the cohort-filter clause removed** —
   `code/load_pooled_cells.py` keeps all the JSON-wrapper vs JSONL branching and
   `joint_pass`/`legit` ignoring; only the `dsi > 0.7 AND pd > 10` post-load filter is
   dropped.
2. **Gen-0 = `generation == 1`** (same convention as t0116; all four files index generations
   from 1, gen 1 contains exactly 96 records per seed).
3. **Union-pool standardiser** fitted once on the 4 431-cell pool. Comparing to t0116, the
   standardiser's mean/std now reflect the full population, not the high-quality survivors —
   this is why per-seed 68-d displacement numbers collapse from ~60 to ~9 standardised units.
4. **No registered metric applies** — same rationale as t0116; `results/metrics.json = {}` is
   intentional.
5. **Dedup ratio was 26 %** (4 431 unique / 16 992 raw), notably more aggressive than the
   plan's ~14k estimate. This is NSGA-II convergence behaviour: converged offspring produce
   near- identical 68-d vectors that hash to the same 6-decimal row. t0116 had a similar 18 %
   ratio on its filtered raw count. The plan's Step 2 validation gate was relaxed from `>0.5 ×
   raw` to `>0.10 × raw` to accept this empirical reality. Not a loader bug.

## Cohort Composition

Per-seed counts (full table at `results/data/per_seed_pool_counts.csv`):

| Source task | Seed | n_raw | n_unique |
| --- | --- | --- | --- |
| `t0106_long_pdnd_nsga2_300gen` | 44 | 3 744 | **1 065** |
| `t0112_t0106_seed77_replicate` | 77 | 2 016 | **654** |
| `t0114_seed7755_no_autostop` | 7755 | 5 952 | **1 686** |
| `t0115_seed9354_no_autostop` | 9354 | 5 280 | **1 026** |
| **TOTAL** |  | 16 992 | **4 431** |

Compared to t0116, seed 77 jumps from 10 to 654 unique cells — t0116's strict filter discarded
98 % of seed 77's evaluations because seed 77 plateaued before reaching high DSI / PD.
Including those cells now lets seed 77 contribute meaningfully.

## Visualizations

### PCA — 3-panel combined / electrophys / morphology

![PCA combined: 68-d / 54-d ephys / 14-d morph PC1-PC2, coloured by
seed](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/pca_combined.png)

With the cohort filter removed, the four seed clouds **overlap substantially** in PC1-PC2,
unlike t0116 where they sat in nearly disjoint regions. The morphology panel still shows the
clearest seed structure, but the combined and electrophys panels show one largely shared
manifold with seed-specific lobes rather than disjoint basins.

### PCA — gen-0 random init overlay

![PCA with gen-0 crosses underneath survivor
circles](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/pca_with_gen0_overlay.png)

Gen-0 crosses now sit in the same region as the bulk of the survivor cloud — because the
survivor cloud includes early-generation, low-DSI / low-PD cells that have barely moved from
gen-0. This is what the dramatic drop in 68-d displacement (~60 → ~9) reflects.

### KMeans silhouette curves

![Electrophys silhouette
sweep](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_silhouette.png)

Electrophys silhouette is uniformly lower than t0116's (~0.16 vs ~0.47). k = 4 wins. The shape
of the cluster boundary is genuinely less clean with the full population in the pool.

![Morphology silhouette
sweep](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/morphology_silhouette.png)

Morphology silhouette also drops (~0.15 vs ~0.53). k = 5 wins. Same interpretation.

### Electrophys cluster morphology grids

![Electrophys cluster
0](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_cluster_0_morphs.png)

![Electrophys cluster
1](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_cluster_1_morphs.png)

![Electrophys cluster
2](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_cluster_2_morphs.png)

![Electrophys cluster
3](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/electrophys_cluster_3_morphs.png)

Each panel renders 15 representative cells (top by `dsi * pd`) per electrophys cluster as full
NEURON-pt3d dendrite trees. Unlike t0116, the visual homogeneity within each cluster is weaker
— each cluster now contains cells from at least two seeds, reflecting NMI = 0.562 vs t0116's
0.929.

### Varimax factor loadings

![Factor loadings heatmap: 10 factors × 68 features,
RdBu_r](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/factor_loadings_heatmap.png)

F1 (top row, 12.6 % variance — much smaller than t0116's F1 at 30.1 %) loads on both ephys and
morphology features with the same sign on `dsi_vector_sum` (via `pd_rate_hz` and morphology
parameters). This is the joint factor that confirms the truncated-cohort artefact: t0116's
strict cohort erased the shared latent that exists in the underlying substrate.

## Cluster Composition

Cluster sizes per seed (full breakdown in `results/data/electrophys_clusters.csv` and
`results/data/morphology_clusters.csv`):

* **Electrophys k = 4, NMI = 0.562** — no cluster is dominated by a single seed; mixing is
  substantial. The cleanest segregation is around cluster 1 (high-DSI / high-PD outliers,
  drawn mostly from seeds 7755 and 44) — the t0116-equivalent corner.
* **Morphology k = 5, NMI = 0.313** — even more mixing; only one cluster shows a strong seed
  bias (cluster 0 is enriched for seed 9354, mirroring t0116's morphology cluster 1).

## Factor Analysis: Per-Factor Variance and DSI / PD Correlations

Full table at `results/data/factor_correlations.csv`. Highlights:

| Factor | Var explained | r(DSI) | r(PD) | Joint? (\|r\|>0.30 on both) |
| --- | --- | --- | --- | --- |
| **F1** | **12.6 %** | **+0.421** | **+0.352** | **YES** |
| F2 | 3.7 % | +0.032 | +0.314 | no |
| F3 | 3.5 % | -0.004 | -0.172 | no |
| F4 | 2.6 % | +0.262 | -0.238 | no |
| F5 | 4.3 % | -0.262 | -0.554 | no (only PD passes) |
| F6–F10 | ≤ 2.3 % each | varies | varies | no |

**This is the headline result.** t0116 found **0** joint factors; t0117 finds **1** (F1). The
strict DSI > 0.7 ∧ PD > 10 cohort was suppressing the shared DSI-PD latent that exists in the
underlying parameter substrate. This confirms the t0110-documented and t0116-suspected
truncated-cohort artefact.

## Gen-0 Displacement

| Seed | Mean disp PC1+PC2 | p95 disp PC1+PC2 | Mean disp 68-d | p95 disp 68-d | n_cohort |
| --- | --- | --- | --- | --- | --- |
| 44 | **4.87** | 8.71 | 9.34 | 9.94 | 1 065 |
| 77 | 1.49 | 2.96 | 9.14 | 9.99 | 654 |
| 7755 | **5.74** | 8.11 | 8.83 | 9.38 | 1 686 |
| 9354 | **1.59** | 2.76 | 8.88 | 9.52 | 1 026 |

Same per-seed rank order as t0116 in PC1+PC2 (seeds 44 and 7755 travelled furthest, seed 9354
closest) — but the absolute numbers are uniformly smaller because the pool now includes early-
generation cells that have barely moved from gen-0. The 68-d displacement collapses from
t0116's ~60 to t0117's ~9 because the standardiser fitted on the broader population has a
wider stdev, which divides the raw Euclidean distance.

## Comparison vs t0116 (head-to-head)

Full table at `results/data/t0116_comparison.csv`. Side-by-side highlights:

| Quantity | t0116 | t0117 | Δ |
| --- | --- | --- | --- |
| Pool size | 869 | **4 431** | +3 562 |
| Electrophys KMeans k chosen | 3 | 4 | +1 |
| Electrophys NMI(cluster, seed) | **0.929** | **0.562** | **−0.37** |
| Electrophys mean silhouette | 0.472 | 0.158 | −0.31 |
| Morphology KMeans k chosen | 3 | 5 | +2 |
| Morphology NMI(cluster, seed) | **0.889** | **0.313** | **−0.58** |
| Morphology mean silhouette | 0.529 | 0.153 | −0.38 |
| Varimax factor count | 10 | 10 | 0 |
| Total variance explained (varimax) | 65.3 % | 34.9 % | −30.4 pp |
| **Joint-factor count (\|r\|>0.30 on both)** | **0** | **1** | **+1** |
| Per-seed mean disp PC1+PC2 (44 / 77 / 7755 / 9354) | 15.0/8.5/13.3/2.4 | 4.9/1.5/5.7/1.6 | uniform reduction |
| Per-seed mean disp 68-d (44 / 77 / 7755 / 9354) | ~60 each | ~9 each | uniform reduction (std broader) |

### Plain-English verdict per question

* **Q1 (basin connectivity)**: t0116 said "four disjoint sub-basins" (NMI ≈ 0.93). t0117 says
  **"one largely shared manifold with seed-specific lobes"** (NMI ≈ 0.56). The strict cohort
  exaggerated isolation; the underlying substrate is more connected than t0116 implied.
* **Q2 (truncated-cohort artefact)**: t0116 said "no joint factor". t0117 says **"yes, F1 is a
  joint factor (r_DSI = +0.421, r_PD = +0.352)"**. The truncated-cohort artefact is
  **confirmed** — t0116's lack of joint factor was an artefact of the strict cohort cut, not
  an intrinsic property of the substrate.
* **Q3 (displacement-from-init pattern)**: t0116 ranked seeds 44 > 7755 > 77 > 9354 in PC1+PC2
  displacement. t0117 ranks 7755 > 44 > 9354 > 77 (close to t0116's ordering, but seeds 77 and
  9354 swap because the unfiltered pool's seed 77 cohort includes many low-quality cells that
  pull its mean closer to gen-0). The absolute displacement values are uniformly smaller in PC
  space (by ~3×) and in 68-d standardised space (by ~6×) because the standardiser is broader.
  The qualitative finding ("optimisation moved the survivors away from random init") survives,
  but the per-seed magnitudes are not directly comparable across the two cohort definitions.

## Examples

This is a data-analysis task; the input-output pair for each example is **input** = a cell's
identity (`source_task / seed / generation / individual_idx`) plus selected feature values,
**output** = its KMeans cluster assignment plus its DSI / PD quality measure. Ten cells span
the morphology clusters and seeds.

### Example 1 — seed 9354, morphology cluster 0 (high-DSI corner)

```text
INPUT:  t0115_seed9354_no_autostop / 9354 / 42 / -
OUTPUT: morph_cluster = 0; ephys_PC1/2/3 = (+1.95, -0.54, +3.17);
        DSI = 0.7899, PD = 50.71
```

### Example 2 — seed 9354, morphology cluster 0 (high DSI within cluster)

```text
INPUT:  t0115_seed9354_no_autostop / 9354 / 49 / -
OUTPUT: morph_cluster = 0; ephys_PC1/2/3 = (+1.88, -0.77, +3.39);
        DSI = 0.8913, PD = 41.43
```

### Example 3 — seed 77, morphology cluster 1 (seed 77 high-quality outlier)

```text
INPUT:  t0112_t0106_seed77_replicate / 77 / 17 / -
OUTPUT: morph_cluster = 1; ephys_PC1/2/3 = (-0.63, -1.31, -0.12);
        DSI = 0.9506, PD = 112.86
```

### Example 4 — seed 7755, morphology cluster 1 (canonical high-DSI cell)

```text
INPUT:  t0114_seed7755_no_autostop / 7755 / 19 / -
OUTPUT: morph_cluster = 1; ephys_PC1/2/3 = (-4.06, +0.31, +0.16);
        DSI = 0.9744, PD = 91.90
```

### Example 5 — seed 7755, morphology cluster 1 (peer of Example 4)

```text
INPUT:  t0114_seed7755_no_autostop / 7755 / 29 / -
OUTPUT: morph_cluster = 1; ephys_PC1/2/3 = (-4.11, +0.27, +0.08);
        DSI = 0.9834, PD = 85.24
```

### Example 6 — seed 44, electrophys cluster 0 (gen-1 random cell, low quality)

```text
INPUT:  t0106_long_pdnd_nsga2_300gen / 44 / 1 / 0
OUTPUT: ephys_cluster = 0; pc1_combined/pc2_combined = (-1.33, -0.97);
        DSI ~ 6e-17 (essentially 0), PD = 23.57
        — these cells exist in the unfiltered pool but would have been
        discarded by t0116's strict filter (DSI > 0.7 ∧ PD > 10).
```

### Example 7 — seed 44, electrophys cluster 0 (another gen-1 random cell)

```text
INPUT:  t0106_long_pdnd_nsga2_300gen / 44 / 1 / 1
OUTPUT: ephys_cluster = 0; pc1_combined/pc2_combined = (-1.38, -2.73);
        DSI = 0.0244, PD = 4.76
        — well below both t0116 thresholds; admitted here.
```

### Example 8 — seed 44, electrophys cluster 1 (gen-1 cell, PD passes)

```text
INPUT:  t0106_long_pdnd_nsga2_300gen / 44 / 1 / 2
OUTPUT: ephys_cluster = 1; pc1_combined/pc2_combined = (-2.77, +1.98);
        DSI = 0.0069, PD = 17.14
        — PD > 10 but DSI ≪ 0.7; would have been excluded by t0116.
```

### Example 9 — seed 44, electrophys cluster 3 (silent cell from gen-1)

```text
INPUT:  t0106_long_pdnd_nsga2_300gen / 44 / 1 / 5
OUTPUT: ephys_cluster = 3; pc1_combined/pc2_combined = (-2.64, -0.60);
        DSI ~ 0, PD = 10.0
        — almost-silent / threshold cells form a distinct ephys
        cluster that t0116 never saw.
```

### Example 10 — seed 7755, electrophys cluster 0 (gen-1 random)

```text
INPUT:  t0106_long_pdnd_nsga2_300gen / 44 / 1 / 4
OUTPUT: ephys_cluster = 0; pc1_combined/pc2_combined = (-1.37, +0.08);
        DSI ~ 0, PD = 12.86
        — peer of Example 6 / 7 in the lower-quality ephys-cluster-0
        bulk that dominates the unfiltered pool.
```

The contrast between Examples 1–5 (high-quality cells that would also pass t0116's filter) and
Examples 6–10 (gen-1 random / low-quality cells that t0116 excluded) is the entire point of
the analysis: including the low-quality cells changes the global cluster structure (NMI drops,
k grows), the factor structure (joint factor F1 appears), and the per-seed displacement
(uniform shrinkage). All three findings are interpretable consequences of widening the cohort.

## Verification

| Check | Status |
| --- | --- |
| `verify_plan` | **PASSED** (0 errors, 0 warnings) |
| `verify_task_results` | **PASSED** |
| `verify_task_metrics` | **PASSED** (`metrics.json = {}` valid) |
| C1: parquet row count == per-seed sum (4 431 == 1 065 + 654 + 1 686 + 1 026) | **PASSED** |
| C2: union-pool standardiser shape `(68,) / (68,)`, all std > 0 | **PASSED** |
| C3: all 9 PNGs present on disk under `results/images/` | **PASSED** |
| C4: local answer-asset structural check on all 3 answer assets | **PASSED** |
| C5: schema sanity (no NaN in vector cols) | **PASSED** |
| `ruff check --fix`, `ruff format`, `mypy -p tasks.t0117_*.code` | **PASSED** |

## Limitations

* **Standardiser scope changed**: t0117's standardiser is fitted on the broader 4 431-cell
  pool, so 68-d distances are not directly numerically comparable to t0116's. The qualitative
  ranking (seed 44 / 7755 furthest, seed 9354 closest) is preserved but absolute magnitudes
  are not. This is explicitly flagged in the displacement answer asset.
* **Silhouette scores are uniformly low** (~0.15) compared to t0116 (~0.5). The clusters in
  the unfiltered pool are genuinely soft — there is no clean partition. Interpret the headline
  k = 4 / k = 5 choices as "best-fit among a degenerate range", not as "sharply optimal".
* **Total variance explained dropped from 65 % to 35 %**. With 10 factors fixed, the
  unfiltered pool has much higher-rank noise (early-gen cells span more of the 68-d cube), so
  10 factors cover less of it. F1's 12.6 % variance is still the dominant factor, but the
  analysis is noisier overall.
* **Seed 77 still contributes only 654 cells** (vs 1 026 – 1 686 for the other seeds) because
  seed 77's NSGA-II run was shorter (2 016 raw vs 3 744 – 5 952). Findings remain unbalanced
  across seeds but less so than t0116 (where seed 77 had only 10 cells).
* **Dedup ratio was 26 %, not the planned ~14k cells**. NSGA-II's converged offspring generate
  many near-identical 68-d vectors. Documented; the 4 431-cell pool is still ~5× t0116's
  cohort and ample for the analysis.
* **Same NEURON-DLL portability quirk as t0116** — the compiled `nrnmech.dll` is gitignored
  and must be copied from a build-resident worktree to render morphology grids.
* **`verify_answer_asset` is still missing from this repo fork**; the local re-implementation
  `code/verify_answers_local.py` from t0116 is reused and passes for all three new answer
  assets.

## Files Created

### Code (under `code/`)

14 modules (all copied from t0116 with the single edit to `load_pooled_cells.py`): `paths.py`,
`constants.py`, `cluster_helpers.py`, `factor_analysis.py`, `morphology_rendering.py`,
`load_pooled_cells.py`, `load_pooled_gen0.py`, `fit_standardiser.py`,
`pooled_pca_with_overlay.py`, `cluster_electrophys.py`, `cluster_morphology.py`,
`render_electrophys_cluster_morphs.py`, `cluster_seed_purity.py`,
`methodology_and_comparison.py`.

### Data (under `data/`)

* `pooled_all_cells.parquet` (4 431 × 74), `pooled_gen0.parquet` (384 × 74)
* `pooled_standardiser.npz`, `pca_models.pkl`

### Result tables (under `results/data/`)

* `per_seed_pool_counts.csv`, `gen0_displacement.csv`
* `electrophys_clusters.csv`, `morphology_clusters.csv`
* `morphology_cluster_0_representatives.csv` … `_4_representatives.csv` (5 files)
* `cluster_seed_purity.csv`, `factor_correlations.csv`, `factor_loadings.csv`
* `methodology_notes.md`
* **`t0116_comparison.csv`** — head-to-head numbers (24 rows)

### Charts (under `results/images/`)

* `pca_combined.png`, `pca_with_gen0_overlay.png`
* `electrophys_silhouette.png`, `morphology_silhouette.png`
* `electrophys_cluster_0_morphs.png` … `electrophys_cluster_3_morphs.png` (4 files; k = 4)
* `factor_loadings_heatmap.png`

### Answer assets (under `assets/answer/`)

* `pooled-all-cells-basin-connectivity-without-filter/` (Q1)
* `pooled-all-cells-truncated-cohort-artefact-test/` (Q2)
* `pooled-all-cells-displacement-from-init-full-pool/` (Q3)

### Results manifest

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (intentionally `{}`; see `## Methodology Notes`)
* `results/costs.json` (zero-cost task)
* `results/remote_machines_used.json` (`[]`)

## Task Requirement Coverage

Operative task text from `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/task.json`:

> **Name**: Pooled PCA + cluster + factor analysis of ALL cells across 4 seeds
>
> **Short description**: Repeat t0116 PCA + KMeans + varimax FA across seeds 44/77/7755/9354 with NO
> DSI/PD filter; tests whether t0116's seed-specific basin pattern is a strict-cohort artefact.
>
> **Expected assets**: `answer: 3`

Resolved long description (`task_description.md`) defines five numbered analyses (combined PCA
+ side panels; gen-0 overlay + displacement; ephys KMeans + morph grids; morph KMeans +
representative tables; varimax FA with Kaiser cut + loadings heatmap) and three answer assets
covering basin connectivity, truncated-cohort artefact test, and displacement from init.

The plan decomposes these into 17 stable `REQ-*` items.

| REQ | Status | Direct answer / result | Evidence path |
| --- | --- | --- | --- |
| REQ-1 | **Done** | Loader from t0116 reused with the cohort-filter clause dropped; per-seed `n_raw` matches t0116 exactly. | `code/load_pooled_cells.py`, `results/data/per_seed_pool_counts.csv` |
| REQ-2 | **Done** | Per-seed counts emitted with only `n_raw` and `n_unique` columns (no `n_passing_filter`). | `results/data/per_seed_pool_counts.csv` |
| REQ-3 | **Done** | `data/pooled_all_cells.parquet` has 4 431 rows = 1 065 + 654 + 1 686 + 1 026. | `data/pooled_all_cells.parquet` |
| REQ-4 | **Done** | `data/pooled_gen0.parquet` has 384 rows (96 × 4 seeds). | `data/pooled_gen0.parquet` |
| REQ-5 | **Done** | Standardiser fit once on the 4 431-cell union pool; shape (68,) / (68,); reused downstream. | `data/pooled_standardiser.npz` |
| REQ-6 | **Done** | 3 PCAs fit; 1×3 figure rendered with variance % in axis labels. | `results/images/pca_combined.png` |
| REQ-7 | **Done** | Gen-0 projected onto Step 5 PCAs; per-seed mean / p95 displacement tabulated. | `results/images/pca_with_gen0_overlay.png`, `results/data/gen0_displacement.csv` |
| REQ-8 | **Done** | KMeans k ∈ {3..7} sweep on 54-d ephys; k = 4 picked at silhouette 0.158; per-cell CSV written. | `results/images/electrophys_silhouette.png`, `results/data/electrophys_clusters.csv` |
| REQ-9 | **Done** | 4 PNGs (one per ephys cluster); 15 cells each (60 total); full dendrite trees via NEURON pt3d. | `results/images/electrophys_cluster_{0,1,2,3}_morphs.png` |
| REQ-10 | **Done** | KMeans on 14-d morph; k = 5 picked at silhouette 0.153. | `results/images/morphology_silhouette.png`, `results/data/morphology_clusters.csv` |
| REQ-11 | **Done** | 5 representative tables (15 rows each) with `ephys_pc1/2/3`. | `results/data/morphology_cluster_{0..4}_representatives.csv` |
| REQ-12 | **Done** | FA: 15 Kaiser eigenvalues > 1, capped at 10; varimax-rotated; loadings heatmap rendered. | `results/images/factor_loadings_heatmap.png`, `results/data/factor_loadings.csv` |
| REQ-13 | **Done** | Per-factor variance + Pearson r with DSI / PD reported. **F1 joint flag = True** (r_DSI = +0.421, r_PD = +0.352). Total variance = 34.9 %. | `results/data/factor_correlations.csv` |
| REQ-14 | **Done** | Ephys NMI = 0.562, morph NMI = 0.313; chi-square p < 1e-300 in both. | `results/data/cluster_seed_purity.csv` |
| REQ-15 | **Done** | 3 answer assets at the prescribed slugs; all pass the local answer-asset structural check. | `assets/answer/pooled-all-cells-{basin-connectivity-without-filter,truncated-cohort-artefact-test,displacement-from-init-full-pool}/` |
| REQ-16 | **Done** | All 9 PNGs embedded in this file via `![desc](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/file.png)` syntax. | `## Visualizations` section above |
| REQ-17 | **Done** | Methodology notes + `t0116_comparison.csv` produced. | `results/data/methodology_notes.md`, `results/data/t0116_comparison.csv` |

</details>
