# ✅ Cluster + factor analysis of t0123 cells: high vs low MI and ATP

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0125_t0123_cluster_factor_mi_atp` |
| **Status** | ✅ completed |
| **Started** | 2026-05-24T23:02:37Z |
| **Completed** | 2026-05-25T01:12:00Z |
| **Duration** | 2h 9m |
| **Dependencies** | [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md), [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md), [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md), [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md) |
| **Task types** | `data-analysis`, `comparative-analysis`, `answer-question` |
| **Categories** | [`cable-theory`](../../by-category/cable-theory.md), [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 4 answer |
| **Step progress** | 11/15 |
| **Task folder** | [`t0125_t0123_cluster_factor_mi_atp/`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/task_description.md)*

# Cluster + Factor Analysis of t0123 Cells: High vs Low MI and ATP

## Motivation

t0123 ran a single-seed (seed 441) 60-generation NSGA-II maximising spike-count mutual
information (`mi_count_bits`) and minimising metabolic cost (`atp_per_spike_molecules`) on the
68-d Bed B + 14-d morphology substrate. The run produced 5760 evaluated cells, 10 Pareto
cells, and reported a best `mi_count_bits = 1.459` (73% of the `log2(4) = 2.0` ceiling) and a
minimum `atp_per_spike_molecules = 6.76e5`.

The single-cell Pareto front answers "where does the DSGC bits-per-ATP front sit relative to
Niven 2007" but says nothing about **how** the 68-d parameter space organises around the two
objectives. Before launching the 3-objective MI + DSI + ATP follow-up (S-0123-02), we need to
know:

* Are high-MI cells and low-ATP cells found in the same regions of the 68-d substrate, or do
  they occupy disjoint clusters?
* Which electrophys parameters (channel densities, synapse densities, axial resistance, etc.)
  systematically differ between high-MI and low-MI cells? Between low-ATP and high-ATP cells?
* Which morphology parameters (segment count, branch order, segment diameter, segment length,
  soma share, etc.) differ across the four corner groups (high-MI / low-ATP, high-MI /
  high-ATP, low-MI / low-ATP, low-MI / high-ATP)?
* Does at least one varimax factor on the 68-d vector load jointly on MI and ATP — implying a
  shared latent driver — or do separate factors drive each objective?
* How does the per-compartment ATP cost share (soma / AIS / dendrites; from
  `atp_per_ap_compartment_breakdown`) covary with the MI and ATP groupings?

This task applies the canonical t0108 / t0116 / t0117 cluster-and-factor pipeline (PCA +
KMeans on electrophys-only and morphology-only subspaces + Kaiser-cap varimax factor analysis
on the full 68-d vector) to the t0123 cell pool, replacing the prior DSI / PD axes with MI and
ATP-per-spike.

## Scope

### Data source (one NSGA-II run, single GA seed)

* `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`
  — seed 441, all 5760 cells evaluated by the t0123 NSGA-II run.

Use the predictions asset as the authoritative data source, not
`results/data/all_evaluations_seed441.json.gz` (same content, different format).

### Pool definition

* Load every record from the predictions asset.
* Deduplicate by the 68-d vector rounded to 6 decimals (`DEDUP_DECIMALS = 6`, same convention
  as t0108 / t0116 / t0117).
* Record raw count, dedup-unique count, and post-filter counts (see below) before any
  analysis.

### Cohort filter

Two cohorts are analysed in parallel:

1. **Full cohort** — every dedup-unique cell, including near-silent cells. This is the primary
   pool for PCA, KMeans, and factor analysis (mirrors t0117's full-cohort design).
2. **Spiking cohort** — cells with `pd_rate_hz > 1.0 Hz` AND `silence_failed_bool == False`.
   This is required for the ATP-per-spike comparison because near-silent cells have a
   denominator approaching zero and produce unstable `atp_per_spike_molecules` values. Used
   for the group-comparison and Pareto-corner analyses.

Per-cohort counts must be reported in `results_detailed.md`.

### Feature vector

Identical to t0108 / t0117: 68-d `vector_68d` with indices 0-53 the 54-d Bed-B electrophys
vector and 54-67 the 14-d morphology vector. Authoritative names in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` `ALL_PARAM_NAMES`.

### Group definitions

For the spiking cohort:

* **MI groups**: top quartile by `mi_count_bits` = "high MI"; bottom quartile = "low MI".
* **ATP groups**: top quartile by `atp_per_spike_molecules` = "high ATP"; bottom quartile =
  "low ATP".
* **MI x ATP corners**: four 2 x 2 quadrants formed by the median split on each axis. Cells in
  the top-left quadrant (high MI, low ATP) are the "Pareto-favoured" corner; bottom-right (low
  MI, high ATP) is the "dominated" corner.

Quartile and median thresholds must be recorded in `results/data/group_thresholds.json`.

### Analyses to run

1. **Combined 68-d PCA + side panels (one figure, three subplots).** Combined PCA /
   electrophys-only PCA / morphology-only PCA, each panel showing PC1 vs PC2 of the full
   cohort, coloured by `mi_count_bits` (viridis). Per-panel report of `% variance explained`
   for PC1 and PC2. Saved to `results/images/pca_combined_color_mi.png`.

2. **Same three-panel figure coloured by `atp_per_spike_molecules`** (log10, viridis). Saved
   to `results/images/pca_combined_color_atp.png`.

3. **Same three-panel figure coloured by MI x ATP corner** (4 categorical colours from tab10).
   Saved to `results/images/pca_combined_color_corner.png`.

4. **Gen-0 (`generation == 1`) random-init overlay.** Same axes as Step 1, with the 96 gen-0
   individuals projected onto the PCAs fitted in Step 1 (no refit; reuse the standardiser).
   Compute mean and 95th-percentile Euclidean displacement in PC1+PC2 space and in 68-d
   standardised space, both overall and per MI x ATP corner. Saved to
   `results/images/pca_with_gen0_overlay.png` and `results/data/gen0_displacement.csv`.

5. **KMeans on 54-d electrophys subspace, auto-pick k in [3, 7] by silhouette.** Standardiser
   fit on the full-cohort union pool. Pick k by maximum mean silhouette. Report silhouette
   curve, chosen k, per-cluster cell counts, and per-cluster mean MI / ATP / DSI / PD /
   firing-rate. Saved to `results/images/electrophys_silhouette.png` and
   `results/data/electrophys_clusters.csv`. For each cluster render a 5 x 3 grid of 15
   representative cells (full dendrite trees via NEURON pt3d — not somas; per memory
   `feedback_top50_morphologies_full_dendrites.md`). Representatives ranked by `mi_count_bits
   / atp_per_spike_molecules` (bits-per-ATP) within cluster, restricted to the spiking cohort.
   Saved to `results/images/electrophys_cluster_<k>_morphs.png` (one PNG per cluster).

6. **KMeans on 14-d morphology subspace, auto-pick k in [3, 7] by silhouette.** Same procedure
   on the morphology subspace. For each morphology cluster, write a 15-row representative
   table with `(generation, cell_index, mi_count_bits, atp_per_spike_molecules,
   dsi_vector_sum, pd_rate_hz, ephys_PC1, ephys_PC2, ephys_PC3, soma_share_atp)` where
   `soma_share_atp` is the soma fraction of `atp_per_ap_compartment_breakdown`. Saved to
   `results/data/morphology_cluster_<k>_representatives.csv`.

7. **Factor analysis on the full 68-d feature matrix, Kaiser criterion, varimax-rotated.**
   Standardise the full cohort -> fit `sklearn.decomposition.FactorAnalysis(n_components=68)`;
   count Kaiser eigenvalues > 1 from the correlation matrix; cap at `KAISER_FACTOR_CAP = 10`
   (inherited from t0108); refit FA with the chosen count; apply varimax rotation via the
   iterative-SVD helper from t0108. Render the loadings heatmap with `RdBu_r` colourmap and
   symmetric vmin/vmax to `results/images/factor_loadings_heatmap.png`. Report per-factor
   variance and Pearson r vs `mi_count_bits` AND `atp_per_spike_molecules` AND
   `dsi_vector_sum` AND `pd_rate_hz` in `results/data/factor_correlations.csv`. Identify any
   factor with |r| > 0.3 on both MI AND ATP (joint factor) and any factor with |r| > 0.3 on MI
   only or ATP only (decoupled factors).

8. **High vs low group comparison (electrophys + morphology).** For each of the 68 parameters,
   compute on the spiking cohort:

   * Mean and standard deviation in the high-MI group, low-MI group, high-ATP group, low-ATP
     group.
   * Mann-Whitney U two-sided p-value: high-MI vs low-MI, high-ATP vs low-ATP.
   * Cliff's delta effect size (non-parametric): high-MI vs low-MI, high-ATP vs low-ATP.

   Save the full table to `results/data/group_comparison.csv`. Render two ranked bar charts of
   Cliff's delta:

   * `results/images/cliffs_delta_high_vs_low_mi.png` -- top-20 parameters by |delta| for MI.
   * `results/images/cliffs_delta_high_vs_low_atp.png` -- top-20 parameters by |delta| for
     ATP.

9. **2 x 2 corner heatmap.** For the 68 parameters, compute the mean (z-scored on the full
   cohort) in each of the four MI x ATP corners. Render as a 68 x 4 heatmap (RdBu_r, symmetric
   vmin/vmax) to `results/images/corner_param_heatmap.png` and save the underlying matrix to
   `results/data/corner_param_means.csv`. This is the central visualisation answering "what
   distinguishes the Pareto-favoured corner from the dominated corner".

10. **ATP compartment breakdown.** Using `atp_per_ap_compartment_breakdown` (keys: `soma`,
    `ais`, `dendrites_total`), compute the per-cell soma / AIS / dendrite **shares** of total
    per-AP ATP cost on the spiking cohort. Compare share distributions across MI groups (high
    vs low) and ATP groups (high vs low) with a ternary plot
    (`results/images/atp_share_ternary.png`) and a violin-plot panel
    (`results/images/atp_share_violins.png`). Save shares per cell to
    `results/data/atp_compartment_shares.csv`.

### Key questions (each becomes one `assets/answer/` asset)

1. **MI-ATP joint structure** — Does the 68-d substrate have a joint latent driving both MI
   and ATP-per-spike, or are MI and ATP driven by decoupled factors? Evidence: varimax factor
   correlations (joint factor with |r| > 0.3 on both MI AND ATP vs decoupled factors with |r|
   > 0.3 on one only) plus the PCA colourings from Steps 1-2. State whether the MI / ATP
   Pareto trade-off observed in t0123 is the result of a single trade-off axis or multiple
   competing axes.

2. **Electrophys signature of high-MI vs low-MI cells** — Which channel densities, axial
   resistance, synapse densities, or other electrophys parameters most distinguish high-MI
   from low-MI cells? Evidence: Cliff's delta ranked bar chart, per-cluster mean MI table, and
   electrophys-KMeans cluster purity by MI-quartile group. State the top-5 parameters by
   |Cliff's delta| with effect sizes and directions.

3. **Morphology signature of low-ATP vs high-ATP cells** — Which morphology parameters most
   distinguish low-ATP-per-spike cells from high-ATP-per-spike cells? Evidence: Cliff's delta
   ranked bar chart restricted to the 14 morphology parameters, morphology-KMeans cluster
   purity by ATP-quartile group, and the ATP compartment breakdown (does the low-ATP group
   spend relatively more ATP at the AIS and less in the dendrites?). State the top-5
   morphology parameters by
   |Cliff's delta| with effect sizes and directions.

4. **Pareto-favoured corner signature** — Which combination of electrophys and morphology
   parameters distinguishes the high-MI / low-ATP corner (Pareto-favoured) from the low-MI /
   high-ATP corner (dominated)? Evidence: 2 x 2 corner heatmap (Step 9) and per-corner
   morphology gallery. State the 5 parameters with the largest absolute z-score difference
   between the two corners, the per-corner cell counts, and the per-corner mean (MI, ATP, DSI,
   PD-rate).

## Approach

* Re-use every code module from
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/` as the structural template
  (loader, PCA, KMeans + silhouette sweep, varimax FA + Kaiser cap, NEURON pt3d morphology
  rendering, cluster representative selection rule). Per the cross-task import rule (CLAUDE.md
  rule 3), code is **copied into this task's `code/` directory** rather than imported. Adapt
  the loader to read the single t0123 predictions asset rather than four per-seed prediction
  files, and replace the cohort filter with the dual full / spiking cohort definition above.
* Reuse `ALL_PARAM_NAMES` (68 entries) from t0108's `code/constants.py` by copying the
  constant into this task's `code/constants.py`.
* The standardiser, PCA, KMeans, and FA must all be fit on the full-cohort union pool. Group
  comparisons in Steps 8-10 use the spiking cohort but project onto the full-cohort PCA fits.
* `data/t0123_cells.parquet` (~5.7k rows, dedup-unique full cohort) and
  `data/t0123_spiking_cells.parquet` (spiking cohort subset) are persisted for downstream
  reproducibility. Gen-0 cells (`generation == 1`, n=96) saved to `data/t0123_gen0.parquet`.
* Mann-Whitney U via `scipy.stats.mannwhitneyu(alternative="two-sided")`. Cliff's delta via
  the standard rank-based formula (no third-party dependency needed; implement in
  `code/effect_sizes.py`).
* Expected runtime: similar to t0117 (CPU-only, KMeans + silhouette dominates). ~30-60 minutes
  wall-clock on 5760 cells.

## Expected Outputs

### Assets

* `assets/answer/<answer_id_1>/` — MI-ATP joint structure question
* `assets/answer/<answer_id_2>/` — high-MI vs low-MI electrophys signature question
* `assets/answer/<answer_id_3>/` — low-ATP vs high-ATP morphology signature question
* `assets/answer/<answer_id_4>/` — Pareto-favoured corner signature question

### Charts (under `results/images/`)

* `pca_combined_color_mi.png` -- three-panel PCA coloured by MI
* `pca_combined_color_atp.png` -- three-panel PCA coloured by ATP (log10)
* `pca_combined_color_corner.png` -- three-panel PCA coloured by MI x ATP corner
* `pca_with_gen0_overlay.png` -- gen-0 overlay
* `electrophys_silhouette.png`, `morphology_silhouette.png` -- silhouette sweeps
* `electrophys_cluster_<k>_morphs.png` (one per ephys cluster) -- 5x3 morphology gallery per
  ephys cluster, full dendrite trees, ranked by bits-per-ATP within cluster
* `factor_loadings_heatmap.png` -- varimax loadings heatmap
* `cliffs_delta_high_vs_low_mi.png` -- top-20 |Cliff's delta| for MI groups
* `cliffs_delta_high_vs_low_atp.png` -- top-20 |Cliff's delta| for ATP groups
* `corner_param_heatmap.png` -- 68 x 4 z-scored parameter means by MI x ATP corner
* `atp_share_ternary.png` -- soma/AIS/dendrite ATP share ternary, coloured by corner
* `atp_share_violins.png` -- per-compartment ATP share violins by MI group and ATP group

### Tables (under `results/data/`)

* `pool_counts.csv` -- raw / dedup-unique / spiking-cohort counts
* `group_thresholds.json` -- quartile and median cutoffs for MI and ATP
* `gen0_displacement.csv` -- per-corner gen-0 displacement
* `electrophys_clusters.csv`, `morphology_clusters.csv` -- per-cell cluster membership +
  summary stats
* `morphology_cluster_<k>_representatives.csv` (one per morph cluster)
* `cluster_group_purity.csv` -- contingency table + NMI of KMeans clusters vs MI / ATP
  quartile groups
* `factor_correlations.csv` -- Pearson r of each varimax factor vs MI / ATP / DSI / PD
* `factor_loadings.csv` -- 68-row varimax loadings matrix
* `group_comparison.csv` -- per-parameter mean / std / U-p / Cliff's delta for high vs low MI
  and high vs low ATP
* `corner_param_means.csv` -- 68 x 4 z-scored parameter means by MI x ATP corner
* `atp_compartment_shares.csv` -- per-cell soma / AIS / dendrite ATP shares
* `methodology_notes.md` -- choices, deviations from t0117, threshold rationale

### Results documents

* `results/results_summary.md` -- 2-3 sentence headline + key numbers
* `results/results_detailed.md` -- full results with all charts embedded via
  `![desc](images/filename.png)` syntax; per-section commentary; per-question verdict
* `results/compare_literature.md` -- one comparison row vs t0117's joint-factor finding
  (truncated-cohort artefact confirmed in t0117 for DSI x PD; does an equivalent finding hold
  for MI x ATP?)

## Compute and Budget

CPU-only. No remote machines. ~30-60 minutes wall-clock (KMeans + silhouette on ~5.7k cells
dominates). $0 paid services. No new dependencies beyond what t0117 already uses
(`scikit-learn`, `pandas`, `numpy`, `scipy`, `matplotlib`, `neuron` for pt3d morphology
rendering).

## Cross-References

* **Methodology precedent**: t0117 (no-filter cohort across 4 seeds, DSI x PD axes), t0116
  (strict cohort across 4 seeds, DSI x PD axes), t0108 (original strict-cohort version on
  t0106 seed 44). Every code module is reused as a structural template, with the loader and
  cohort-filter modules rewritten for the t0123 single-seed source.
* **Source data**: t0123 (NSGA-II MI vs ATP-per-spike, seed 441, 5760 cells, 10 Pareto).
* **Related open suggestions**: none of the t0123 suggestions cover this analysis directly;
  S-0123-02 (3-objective MI + DSI + ATP NSGA-II) and S-0123-03 (cell 2 deep-dive) are the
  closest downstream follow-ups and benefit from the cluster / factor structure produced here.
* **Truncated-cohort artefact context**: memory
  `project_truncated_cohort_artefact_confirmed.md` (t0117 confirmed F1 is a joint DSI-PD
  factor in the unfiltered pool). The MI-ATP equivalent is the central question of answer 1
  here.
* **Methodology preferences**: memory `feedback_top50_morphologies_full_dendrites.md` (render
  full dendrite trees in morphology grids, not just somas).

## Verification Criteria

* `data/t0123_cells.parquet` row count equals the dedup-unique count logged at load time, and
  `data/t0123_spiking_cells.parquet` row count equals the cohort-filtered subset.
* `group_thresholds.json` contains numeric values for MI Q1, MI Q3, ATP Q1, ATP Q3, MI median,
  ATP median.
* Every PCA / KMeans / FA fit uses the standardiser fitted on the full-cohort union pool (not
  the spiking subset).
* Every chart referenced in `results_detailed.md` exists on disk and is embedded with markdown
  image syntax (not just listed as text).
* Every claim in each of the four answer assets is grounded in a specific table or chart in
  `results_detailed.md`. Each answer asset cites the specific row/column of
  `group_comparison.csv` or `factor_correlations.csv` underpinning its verdict.
* Headline numbers (joint-factor count, per-question top-5 parameters with effect sizes,
  per-corner cell counts) must be reported even if they are negative (no result-suppression).
* `compare_literature.md` includes a one-row comparison of the MI-ATP joint factor result vs
  t0117's DSI-PD joint factor finding.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Which electrophys parameters most distinguish high-MI from low-MI cells in the t0123 spiking cohort, with effect size and direction?](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/high-vs-low-mi-electrophys-signature/) | [`full_answer.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/high-vs-low-mi-electrophys-signature/full_answer.md) |
| answer | [Which morphology parameters most distinguish low-ATP from high-ATP cells in the t0123 spiking cohort, and does the low-ATP group spend relatively more ATP at the AIS than in the dendrites?](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/low-vs-high-atp-morphology-signature/) | [`full_answer.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/low-vs-high-atp-morphology-signature/full_answer.md) |
| answer | [Does the 68-d substrate of the t0123 single-seed MI vs ATP-per-spike NSGA-II run admit a joint MI x ATP latent factor (/r/ > 0.30 on both metrics simultaneously), or are MI and ATP driven by decoupled factors?](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/mi-atp-joint-structure-in-t0123-substrate/) | [`full_answer.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/mi-atp-joint-structure-in-t0123-substrate/full_answer.md) |
| answer | [Which combination of electrophys + morphology parameters most distinguishes the Pareto-favoured corner (high MI, low ATP) from the Pareto-dominated corner (low MI, high ATP) in the t0123 substrate, and what are the per-corner cell counts and means?](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/pareto-favoured-corner-signature/) | [`full_answer.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/pareto-favoured-corner-signature/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Multi-seed MI/ATP NSGA-II replicate to test seed dependence of
the zero-joint-factor verdict</strong> (S-0125-01)</summary>

**Kind**: experiment | **Priority**: high

t0125's zero-joint MI x ATP varimax verdict is derived from a SINGLE NSGA-II seed (441).
Precedent: t0116 (single seed) found no joint DSI x PD factor; t0117 (4 seeds) recovered one.
The verdict is known to be seed-sensitive on this substrate. Action: replicate t0123 on 2-3
additional non-round GA seeds (POP_SIZE=96, N_EVAL_SEEDS=3, N_GEN_MAX=60, COST_CAP_USD=6,
HV-plateau auto-stop DISABLED per memory feedback_disable_hv_plateau_autostop,
_POOL_RESTART_EVERY=10) and rerun the t0125 cluster + Kaiser-cap varimax pipeline on the
pooled 4-seed pool. Predicted outcome: either F1's ATP loading crosses 0.30 (joint factor
reappears) or stays decoupled (objective-pair-specific verdict confirmed). Budget ~$15-25
Vast.ai EPYC. Recommended task types: experiment-run, data-analysis, comparative-analysis.

</details>

<details>
<summary><strong>Patch t0080 with an explicit myelinated axon to fix the
soma-vs-axon ATP-share inversion vs Attwell 2001</strong> (S-0125-02)</summary>

**Kind**: experiment | **Priority**: high

t0125 finds 76.7% soma / 5.5% AIS / 17.8% dendrite ATP share -- inverted from Attwell &
Laughlin 2001's 4% soma / 82% axon / 14% dendrite rodent-cortical breakdown. methodology_notes
and compare_literature attribute this to t0080 lacking an explicit myelinated axon (only a
procedural AIS). Action: extend the t0080 cell builder with one or two nodes of Ranvier +
myelin segments at realistic R_m (~50 kOhm cm^2), C_m (~0.04 uF/cm^2), and Na/K channel
densities; re-run t0123's MI vs ATP-per-spike NSGA-II at matched compute; re-check
soma/AIS/axon/dendrite ATP shares against Attwell 2001 Table 4 and Sengupta 2010. Test whether
the Pareto front shifts and whether compartment-ATP diversity broadens to match the rodent
picture. Budget ~$10-15 Vast.ai EPYC. Recommended task types: build-model, experiment-run,
comparative-analysis.

</details>

<details>
<summary><strong>8-direction MI NSGA-II to lift the 2-bit ceiling and re-test the
joint factor at higher MI resolution</strong> (S-0125-03)</summary>

**Kind**: experiment | **Priority**: medium

t0125's top cells saturate at mi_count_bits = 1.459 (73% of log2(4) = 2.0). Three Pareto cells
converged on identical (MI, DSI, PD-rate) -- a deterministic optimum at the ceiling.
Compressed MI variance pulls all joint loadings toward zero. Distinct from S-0123-01 (extended
trial length + PD-rate floor for Strong-Bialek bits/s) and from polar 8-direction
re-evaluation suggestions on DSI lineages (those re-score existing cells; this is a fresh
NSGA-II). Action: fork t0123 with N_DIRECTIONS = 8 (ceiling = log2(8) = 3.0 bits), keep other
constants matched (POP_SIZE = 96, N_EVAL_SEEDS = 3, HV auto-stop OFF, pool restart every 10);
scale trial duration only if firing rate falls (per memory
feedback_dsgc_measurement_protocol); rerun cluster + factor analysis. Budget ~$10-15 Vast.ai
EPYC. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Partial-correlation analysis of MI vs electrophys (control
morphology) and ATP vs morphology (control electrophys)</strong>
(S-0125-04)</summary>

**Kind**: experiment | **Priority**: medium

t0125's PCA colourings make the separation visible: high-MI cells cluster in the electrophys
PCA but are absent from the morphology PCA; log10(ATP) shows a gradient in the morphology PCA,
flatter in electrophys. NMI table corroborates (electrophys-vs-MI 0.178, electrophys-vs-ATP
0.186, morphology-vs-MI 0.121, morphology-vs-ATP 0.176). These are pairwise correlations and
could share a common cause. Action: on the existing spiking-cohort parquet, compute Spearman
partial r for (a) MI vs each of 54 electrophys params partialling out 14 morphology params;
(b) ATP vs each of 14 morphology params partialling out 54 electrophys params; (c) MI vs ATP
partialling out morphology; (d) MI vs ATP partialling out electrophys. Report top-10 with
bootstrap CI; compare to t0125 group_comparison.csv. Single CPU-only follow-up. Recommended
task types: data-analysis, answer-question.

</details>

<details>
<summary><strong>Off-diagonal-corner-constrained NSGA-II to sample the undersampled
high-MI/high-ATP and low-MI/low-ATP corners</strong> (S-0125-05)</summary>

**Kind**: experiment | **Priority**: medium

t0125 finds a 3.6x diagonal-vs-off-diagonal corner imbalance: 1221 high_MI/low_ATP + 1220
low_MI/high_ATP vs only 343 high_MI/high_ATP + 341 low_MI/low_ATP cells. Off-diagonal corners
are real -- cell (19, 1816) hits MI=1.459 at ATP=4.97e7 (8.7x more expensive than equivalent
(30, 2828)) -- but undersampled because NSGA-II exploited the cheap-and-informative half.
Action: rerun the t0123 NSGA-II twice with constrained objectives (a) maximise BOTH MI and ATP
(forces high_MI/high_ATP corner); (b) minimise BOTH (forces low_MI/low_ATP corner). Sample 96
cells per corner; rerun the t0125 cluster + factor pipeline on the union plus the original
t0123 pool. Tests whether off-diagonal corners share or have private latent drivers. Budget
~$8-12 Vast.ai EPYC. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Vm-trace deep-dive of cell (19, 1816) -- high-MI / high-ATP /
extended-dendrite outlier</strong> (S-0125-06)</summary>

**Kind**: experiment | **Priority**: medium

Cell (19, 1816) hits the MI ceiling (1.459 bits) at ATP = 4.97e7 molecules/spike (cohort
99th-percentile) with 79% of ATP spent in dendrites (cohort mean 17.8%); cell (30, 2828)
matches the MI at 0.5% dendrite share. This is the cleanest case of 'high MI is consistent
with both compact-dendrite/low-ATP and extended-dendrite/high-ATP geometries'. Distinct from
S-0123-03 (cell 2, near-silent high-MI cell): this is the complementary deep-dive on the OTHER
end of the iso-MI ridge. Action: single-cell resimulate (19, 1816) from its 68-d vector under
the EPSP_PASSIVE / IPSP_PASSIVE / FULL trio (memory feedback_dsgc_measurement_protocol),
record somatic + dendritic Vm and per-compartment g_E / g_I / i_Na / i_K. Identify which
subset drives the across-direction count signal vs the dendritic ATP overhead. Local CPU < 2
h. Recommended task types: experiment-run, data-analysis, answer-question.

</details>

<details>
<summary><strong>Disjoint parameter-basin enumeration of high-MI cells to quantify
Achard 2006 degeneracy on the t0123 substrate</strong> (S-0125-07)</summary>

**Kind**: experiment | **Priority**: medium

t0125's electrophys silhouette = 0.083 (low) paired with chi-square p = 1e-236 (highly
significant) is the signature of Achard 2006's 'loosely connected hyperplane' geometry. t0125
confirmed the qualitative pattern (5 of 68 parameters with |Cliff's delta| > 0.6 for MI
groups, ~7%) but did NOT count DISJOINT parameter basins producing mi_count_bits > 1.0.
Action: on the spiking-cohort parquet, restrict to cells with MI > 1.0 (n ~ 600-800), apply
single-linkage hierarchical clustering in the standardised 54-d electrophys subspace tuned to
3-10 connected components, report per-component median pairwise distance, per-parameter range,
and cross-component nearest-neighbour distance. Replicate in morphology and full-68-d. Tests
Marder 2006 'many models, one behaviour' on t0123; motivates per-basin re-seeded NSGA-II.
CPU-only. Recommended task types: data-analysis, answer-question.

</details>

<details>
<summary><strong>Bootstrap loading stability for the single-seed MI factors to
bracket the 0.358 / 0.205 joint-threshold gap</strong> (S-0125-08)</summary>

**Kind**: evaluation | **Priority**: medium

t0125's zero-joint verdict rides on F1's r_MI = -0.358 (above threshold) paired with r_ATP =
+0.205 (below threshold) -- ATP only 0.095 below the 0.30 cutoff. Verdict could flip under
resampling. Distinct from S-0117-03 (bootstrap on t0117 4-seed DSI x PD F1): this is the MI x
ATP single-seed analogue. Action: on the existing t0125 standardiser and 5760-cell parquet,
draw B = 500 bootstrap resamples, refit FA(n=10) + varimax, report (a) per-factor 5/50/95
percentile loadings on every 68-d parameter; (b) per-factor 5/50/95 percentile r vs MI and
ATP; (c) probability that >=1 factor crosses |r| > 0.30 on both axes per resample; (d)
threshold sensitivity at 0.20, 0.25, 0.30, 0.35. Bounds the joint-factor verdict and produces
the threshold-sensitivity curve flagged in compare_literature. CPU-only. Recommended task
types: data-analysis, answer-question.

</details>

## Research

* [`research_code.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/research/research_code.md)
* [`research_papers.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/results_summary.md)*

# Results Summary: t0125 Cluster + Factor Analysis of t0123 MI vs ATP

## Summary

Applied the canonical PCA + KMeans + varimax factor-analysis pipeline (inherited from t0108 /
t0116 / t0117) to the **5,760** t0123 cells with a dual full / spiking-cohort design. The
headline finding is **negative for the joint-driver hypothesis**: **zero** varimax factors
satisfy `|r_MI| > 0.30 AND |r_ATP| > 0.30` simultaneously, in direct contrast to t0117 which
found one joint DSI x PD factor. Despite the decoupled latent structure, MI and ATP are
positively correlated at the cell level (**3.6x** diagonal-vs-off-diagonal corner-count
imbalance), and the high-MI / low-ATP "Pareto-favoured" corner has **1,221** of the 3,125
spiking cells.

## Metrics

* **Joint MI-ATP factors** (|r| > 0.30 on both): **0** (largest joint loading: F1 with `r_MI =
  -0.358`, `r_ATP = +0.205`).
* **Top |Cliff's delta| for MI**: IH_GBAR **-0.79**, CAD_TAUR_MS **-0.72**, KDR_GBAR
  **-0.67**, SK_AIS_GBAR **+0.63**, SKAHP_TAU_CA_MULTIPLIER **-0.63**.
* **Top |Cliff's delta| for ATP morphology**: mean_segment_length_um **-0.73**,
  branch_length_cv **+0.55**, branch_density_gradient_pd **+0.50**, field_elongation_pd
  **-0.47**, ais_length_um **+0.38**.
* **MI x ATP corner counts** (spiking cohort, median splits): high_MI_low_ATP=**1,221**,
  high_MI_high_ATP=**343**, low_MI_low_ATP=**341**, low_MI_high_ATP=**1,220**.
* **ATP compartment shares** (spiking cohort means): soma **76.7%**, dendrites **17.8%**, AIS
  **5.5%**; low-ATP cells skew to **93%** soma vs high-ATP cells skewing to **62%** dendrites.
* **KMeans headline k**: electrophys k=**4** (mean silhouette 0.083), morphology k=**5** (mean
  silhouette 0.158).
* **Cluster-purity NMI** (spiking cohort): electrophys-vs-MI-quartile **0.178**,
  electrophys-vs-ATP-quartile **0.186**, morphology-vs-MI-quartile **0.121**,
  morphology-vs-ATP-quartile **0.176**.

## Verification

* `verify_task_file.py` — to be run in reporting step.
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings) at check-deps step.
* `verify_research_papers.py` — PASSED (0 errors, 0 warnings).
* `verify_research_code.py` — PASSED (0 errors, 0 warnings).
* `verify_plan.py` — PASSED (0 errors, 0 warnings).
* Inline answer-asset checker (walks AA-E001..AA-E014 + AA-W001 from
  `meta/asset_types/answer/specification.md`) — PASSED for all 4 answer assets (0 errors, 0
  warnings). `verify_answer_asset.py` does not exist in this checkout.
* `ruff check`, `ruff format`, `mypy -p tasks.t0125_....code` — all clean. 6/6 pytest tests
  pass.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0125_t0123_cluster_factor_mi_atp" ---
# Results Detailed: t0125 Cluster + Factor Analysis of t0123 MI vs ATP

## Summary

Adapted the canonical PCA + KMeans + varimax FA pipeline (t0108 / t0116 / t0117 template) to
the t0123 single-seed NSGA-II run that optimised spike-count MI vs ATP-per-spike on the 68-d
Bed B + 14-d morphology substrate. Loaded **5,760** dedup-unique cells (full cohort) and the
**3,125**-cell spiking subset (`pd_rate_hz > 1.0 AND not silence_failed`), produced 12 unique
charts + 4 morphology galleries (60 dendrite trees total), 13 result tables, and **4** answer
assets. Headline finding: **MI and ATP are decoupled at the varimax-factor level** (no factor
crosses |r| > 0.30 on both) despite a strong positive correlation at the cell level (3.6x
diagonal-vs-off-diagonal corner-count imbalance). Soma dominates the per-AP ATP budget (76.7%
mean share) and low-ATP cells concentrate even further at the soma (93% mean), inverting the
canonical Attwell-Laughlin cortical breakdown.

## Methodology

* **Machine**: local Windows 11 workstation, CPU-only. No remote machines.
* **Runtime**: ~80 minutes wall-clock for the full pipeline (load -> standardise -> PCA ->
  KMeans silhouette sweep -> FA + Kaiser cap -> group comparison + Cliff's delta -> corner
  heatmap -> ATP share -> cluster purity -> morphology gallery via NEURON pt3d).
* **Timestamps**: implementation started 2026-05-24T23:55:46Z, completed 2026-05-25T01:15:00Z.
* **Methods**:
  * Standardiser: per-column z-score on the full cohort (mean / std; zero-std columns clipped
    to 1.0).
  * PCA: `sklearn.decomposition.PCA` on combined 68-d, electrophys-only 54-d, and
    morphology-only 14-d.
  * KMeans: `sklearn.cluster.KMeans(random_state=42, n_init=10)` swept over `k = (3, 4, 5, 6,
    7)`, headline `k` picked by maximum mean silhouette.
  * Factor analysis: `sklearn.decomposition.FactorAnalysis(n_components=68, random_state=42)`
    -> Kaiser eigenvalue cut (>1) capped to 10 -> refit -> in-house iterative-SVD varimax
    (`gamma=1.0`, `tol=1e-6`, `max_iter=500`).
  * Effect sizes: Mann-Whitney U two-sided (`scipy.stats.mannwhitneyu`) + in-house Cliff's
    delta (`code/effect_sizes.py`, 6 unit tests).
  * Cohort filter: `pd_rate_hz > 1.0 AND silence_failed == False`. Group thresholds and corner
    counts persisted to `results/data/group_thresholds.json`.
  * Morphology rendering: NEURON pt3d (`h.x3d / y3d / diam3d`) full dendrite trees per memory
    `feedback_top50_morphologies_full_dendrites`.
  * Cross-task imports: t0117 code modules copied verbatim into `code/` with namespace updates
    (per CLAUDE.md rule 3); t0090 and t0092 procedural morphology generators imported as
    libraries (the exception to the cross-task rule).

## Pool counts and group thresholds

| Cohort | Cells |
| --- | --- |
| Raw t0123 records | 5,760 |
| Dedup-unique (6-decimal vector hash) | 5,760 |
| Spiking (`pd_rate_hz > 1.0 AND not silence_failed`) | 3,125 |
| Gen-0 (generation == 1) | 96 |

Quartile thresholds (spiking cohort): MI Q1 = 0.000 bits, Q2 = 0.565, Q3 = 0.964.
ATP-per-spike Q1 = 5.30e6, Q2 = 6.55e6, Q3 = 1.24e7 molecules.

Corner counts (spiking cohort, median splits): **high_MI/low_ATP = 1221**, **high_MI/high_ATP
= 343**, **low_MI/low_ATP = 341**, **low_MI/high_ATP = 1220**. The diagonal sum (2441) exceeds
the off-diagonal sum (684) by **3.57x**, indicating MI and ATP are positively correlated at
the cell level (high-MI cells tend to be low-ATP cells and vice versa).

## Visualizations

### PCA, three-panel views

The three panels of each PCA figure are combined 68-d, electrophys-only 54-d, and
morphology-only 14-d. PC1+PC2 percent variance is annotated on each axis.

![PCA coloured by
MI](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/pca_combined_color_mi.png)

`pca_combined_color_mi.png` shows that high-MI cells (yellow) form a tight cluster in the
electrophys PC1 < 0 region and are largely absent from the morphology PCA, indicating
**electrophys drives MI more than morphology does**.

![PCA coloured by ATP
(log10)](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/pca_combined_color_atp.png)

`pca_combined_color_atp.png` shows the inverse trend: log10(ATP) gradient is visible in the
morphology PCA but flatter in the electrophys PCA, indicating **morphology drives ATP more
than electrophys does**. This complementarity is the structural explanation for the
zero-joint-factor result.

![PCA coloured by MI x ATP
corner](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/pca_combined_color_corner.png)

`pca_combined_color_corner.png` confirms the high_MI/low_ATP (Pareto-favoured) and
low_MI/high_ATP (dominated) corners occupy the densest, near-opposite tails of PC1, while the
off-diagonal corners are sparse and overlap the cohort centre.

![PCA with gen-0
overlay](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/pca_with_gen0_overlay.png)

The 96 gen-0 random-init individuals overlay the optimised pool's PC1+PC2 space, showing
NSGA-II moved cells substantially: overall mean PC1+PC2 displacement = 7.13 (95th-percentile
10.07), and the high_MI/low_ATP corner saw the largest displacement (mean 9.50, 95th 10.32) —
consistent with NSGA-II actively seeking the Pareto front.

### KMeans silhouette sweeps

![Electrophys
silhouette](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/electrophys_silhouette.png)

Electrophys silhouette peaks at **k=4** (0.083). The cluster representative table is
`results/data/electrophys_clusters.csv`.

![Morphology
silhouette](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/morphology_silhouette.png)

Morphology silhouette peaks at **k=5** (0.158), notably higher than the electrophys score,
suggesting the 14-d morphology subspace has cleaner cluster structure than the 54-d
electrophys subspace.

### Morphology cluster galleries (full NEURON pt3d dendrite trees)

Each gallery contains 5x3 = 15 representatives ranked by `mi_count_bits /
atp_per_spike_molecules` (bits-per-ATP) within the cluster, restricted to the spiking cohort.

![Electrophys cluster
0](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/electrophys_cluster_0_morphs.png)
![Electrophys cluster
1](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/electrophys_cluster_1_morphs.png)
![Electrophys cluster
2](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/electrophys_cluster_2_morphs.png)
![Electrophys cluster
3](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/electrophys_cluster_3_morphs.png)

### Varimax factor analysis

![Factor loadings
heatmap](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/factor_loadings_heatmap.png)

The heatmap of the 10 varimax-rotated factors x 68 parameters shows broad loading on
electrophys parameters (PC1-side) and a narrower, distinct loading on morphology
(`mean_segment_length_um`, `branch_length_cv`, etc.) but no single factor jointly loads on MI
and ATP. Full numeric correlations and the classification column are in
`results/data/factor_correlations.csv`:

| Factor | r_MI | r_ATP | r_DSI | r_PD | classification |
| --- | --- | --- | --- | --- | --- |
| F1 | -0.358 | +0.205 | -0.347 | +0.030 | mi_only |
| F2 | +0.463 | +0.063 | +0.413 | +0.201 | mi_only |
| F3 | +0.206 | -0.115 | +0.230 | -0.159 | none |
| F4 | +0.111 | +0.032 | +0.147 | +0.065 | none |
| F5 | +0.105 | +0.061 | +0.080 | +0.038 | none |
| F6 | +0.006 | +0.047 | +0.003 | +0.109 | none |
| F7 | -0.009 | +0.086 | -0.003 | +0.129 | none |
| F8 | +0.204 | +0.019 | +0.180 | +0.013 | none |
| F9 | +0.022 | -0.059 | +0.024 | -0.067 | none |
| F10 | +0.011 | +0.020 | +0.009 | -0.016 | none |

**No factor satisfies `joint_mi_atp_flag = True`** (|r| > 0.30 on both MI and ATP).

### Cliff's delta ranked bar charts

![Cliff's delta: high vs low
MI](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/cliffs_delta_high_vs_low_mi.png)

The top-20 |Cliff's delta| parameters for high-MI vs low-MI cells are dominated by intrinsic
electrophys parameters — IH_GBAR (-0.79), CAD_TAUR_MS (-0.72), KDR_GBAR (-0.67), SK_AIS_GBAR
(+0.63), SKAHP_TAU_CA_MULTIPLIER (-0.63) — confirming the PCA finding that electrophys drives
MI.

![Cliff's delta: high vs low
ATP](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/cliffs_delta_high_vs_low_atp.png)

The top-20 for high-ATP vs low-ATP are a mix of electrophys (BK_TERMINAL_GBAR +0.69,
NAV16_MID_GBAR +0.64) and morphology (mean_segment_length_um -0.73, branch_length_cv +0.55).
The strongest single ATP discriminator is morphological — **mean_segment_length_um**, with
short dendritic segments correlating with low ATP per spike.

### 2x2 MI x ATP corner heatmap

![Corner
heatmap](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/corner_param_heatmap.png)

The 68 x 4 z-scored corner means visualise which parameters separate the four MI x ATP
quadrants. The Pareto-favoured corner (high_MI/low_ATP) is characterised by strong positive
NAV16_AIS_GBAR (+0.57), SK_AIS_GBAR, and KV3 elevations and negative IH_GBAR / CAD_TAUR_MS;
the dominated corner (low_MI/high_ATP) is approximately the mirror.

### ATP compartment shares

![ATP share
ternary](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/atp_share_ternary.png)
![ATP share
violins](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/images/atp_share_violins.png)

The ternary plot shows the four MI x ATP corners stack vertically along the soma <-> dendrite
edge of the simplex with the AIS share staying low (mean 5.5%). The violin panel quantifies
the contrast: low-ATP cells concentrate **93%** of per-AP ATP at the soma vs **62%** in the
dendrites for high-ATP cells. This contradicts the canonical Attwell-Laughlin breakdown (axon
82%, dendrites 14%, soma 4%) — the t0125 model concentrates AP energy in the soma, not the
axon.

## Examples

The following 11 cells illustrate the joint MI / ATP / DSI / PD distribution. Each block shows
the exact record from `data/t0125_spiking_cells.parquet` (the loader output the rest of the
pipeline reads). Cells are identified by `(generation, cell_index)`.

### Best 1: cell (51, 4810) -- top bits-per-ATP, Pareto front

```json
{
  "generation": 51,
  "cell_index": 4810,
  "mi_count_bits": 1.4589893596666386,
  "atp_per_spike_molecules": 4756737.981196062,
  "dsi_vector_sum": 0.3162277660168379,
  "pd_rate_hz": 2.857142857142857,
  "atp_soma": 4494461.495327889,
  "atp_ais": 232253.3973627749,
  "atp_dendrites_total": 30023.088505398187
}
```

Reaches the spike-count MI ceiling (`log2(4) - bias` ~ 1.46 bits) at the lowest ATP-per-spike
in the cohort. 94.5% of ATP at the soma, 0.6% in the dendrites -- the prototype Pareto cell.

### Best 2: cell (59, 5643)

```json
{
  "generation": 59,
  "cell_index": 5643,
  "mi_count_bits": 1.4589893596666386,
  "atp_per_spike_molecules": 4780283.875595512,
  "dsi_vector_sum": 0.3162277660168379,
  "pd_rate_hz": 2.857142857142857,
  "atp_soma": 4517750.730902616,
  "atp_ais": 230749.17593879285,
  "atp_dendrites_total": 31783.9687541024
}
```

Same MI / DSI / PD-rate signature as cell (51, 4810); NSGA-II converged on the same operating
point in three independent cells, suggesting a near-deterministic optimum given the substrate.

### Best 3: cell (57, 5424)

```json
{
  "generation": 57,
  "cell_index": 5424,
  "mi_count_bits": 1.4589893596666386,
  "atp_per_spike_molecules": 4813833.841124552,
  "dsi_vector_sum": 0.3162277660168379,
  "pd_rate_hz": 2.857142857142857,
  "atp_soma": 4581585.598085737,
  "atp_ais": 207065.65964902387,
  "atp_dendrites_total": 25182.583389790798
}
```

Third Pareto-front cell. Together with cells (51, 4810) and (59, 5643), these are the actual
t0123 Pareto cells in (MI, ATP) space.

### Worst 1: cell (1, 4) -- zero MI despite firing

```json
{
  "generation": 1,
  "cell_index": 4,
  "mi_count_bits": 0.0,
  "atp_per_spike_molecules": 18244303.179105602,
  "dsi_vector_sum": 5.897955049882633e-17,
  "pd_rate_hz": 4.285714285714286,
  "atp_soma": 9281779.31464655,
  "atp_ais": 948380.9187748223,
  "atp_dendrites_total": 8014142.945684231
}
```

Gen-0 random-init cell fires at 4.3 Hz but encodes zero directional information at the
4-direction count-MI estimator. 44% of ATP in dendrites -- typical low-MI / high-ATP
"dominated" corner.

### Worst 2: cell (1, 8) -- high firing, zero MI

```json
{
  "generation": 1,
  "cell_index": 8,
  "mi_count_bits": 0.0,
  "atp_per_spike_molecules": 15075282.542278035,
  "dsi_vector_sum": 5.649027278170325e-17,
  "pd_rate_hz": 19.28571428571429,
  "atp_soma": 10395430.79856601,
  "atp_ais": 929313.698361163,
  "atp_dendrites_total": 3750538.04535086
}
```

Fires at 19.3 Hz but still has zero MI: the cell discharges equally across all four
directions. This is what an "unselective" DSGC looks like in the t0123 substrate.

### Worst 3: cell (1, 11) -- worst ATP-per-spike

```json
{
  "generation": 1,
  "cell_index": 11,
  "mi_count_bits": 0.0,
  "atp_per_spike_molecules": 48710631.904302634,
  "dsi_vector_sum": 5.52000058772841e-17,
  "pd_rate_hz": 20.714285714285715,
  "atp_soma": 8624127.857600173,
  "atp_ais": 2659394.6996856392,
  "atp_dendrites_total": 37427109.347016826
}
```

Most expensive cell in this sample at 4.87e7 ATP/spike. 77% of ATP is in the dendrites; zero
MI despite the highest firing rate (20.7 Hz). Uniformly bad on both objectives.

### Contrastive 1: cell (30, 2828) -- high MI / low ATP

```json
{
  "generation": 30,
  "cell_index": 2828,
  "mi_count_bits": 1.4589893596666386,
  "atp_per_spike_molecules": 5686299.128393824,
  "dsi_vector_sum": 0.3162277660168379,
  "pd_rate_hz": 2.857142857142857,
  "atp_soma": 5095245.274360853,
  "atp_ais": 564573.1746877071,
  "atp_dendrites_total": 26480.679345264147
}
```

MI at the ceiling (1.459 bits), low ATP (5.7e6). Pair with cell (19, 1816) below.

### Contrastive 2: cell (19, 1816) -- high MI / HIGH ATP

```json
{
  "generation": 19,
  "cell_index": 1816,
  "mi_count_bits": 1.4589893596666386,
  "atp_per_spike_molecules": 49704407.68098243,
  "dsi_vector_sum": 0.35630482034348054,
  "pd_rate_hz": 3.333333333333334,
  "atp_soma": 9787499.656632485,
  "atp_ais": 610310.2295128409,
  "atp_dendrites_total": 39306597.79483711
}
```

Same MI = 1.459 bits as cell (30, 2828) but **8.7x more expensive per spike** (4.97e7 vs
5.69e6). 79% of ATP is in the dendrites here vs 0.5% in (30, 2828). Direct proof that the (MI,
ATP) Pareto front is two-dimensional: achieving MI ceiling does not require the low-ATP
geometry; high MI is consistent with both compact-dendrite (low ATP) and extended-dendrite
(high ATP) configurations.

### Boundary 1: cell (27, 2555) -- near median on both axes

```json
{
  "generation": 27,
  "cell_index": 2555,
  "mi_count_bits": 0.5699579180264102,
  "atp_per_spike_molecules": 6492094.765434377,
  "dsi_vector_sum": 0.21209125149788163,
  "pd_rate_hz": 1.4285714285714286,
  "atp_soma": 5931323.1162902685,
  "atp_ais": 542239.6817579035,
  "atp_dendrites_total": 18531.96738620567
}
```

Median MI (0.57), median ATP (~6.5e6). Lands in the high_MI/low_ATP corner because both axes
are exactly at their median (the median split assigns ties to the "high" side).

### Boundary 2: cell (47, 4455) -- median MI/ATP but very different DSI

```json
{
  "generation": 47,
  "cell_index": 4455,
  "mi_count_bits": 0.5699579180264102,
  "atp_per_spike_molecules": 6477721.327219318,
  "dsi_vector_sum": 0.015342771384953142,
  "pd_rate_hz": 14.285714285714286,
  "atp_soma": 6282714.06300913,
  "atp_ais": 189946.1811030425,
  "atp_dendrites_total": 5061.0831071452585
}
```

Same MI = 0.57 as cell (27, 2555) but DSI is essentially zero (0.015) and PD-rate is 10x
higher (14.3 vs 1.4 Hz). Shows that the (MI, ATP) pair does not fully determine DSI: two cells
can match on both objectives and still have very different selectivity.

### Boundary 3: cell (22, 2023) -- near-median triple

```json
{
  "generation": 22,
  "cell_index": 2023,
  "mi_count_bits": 0.5699579180264102,
  "atp_per_spike_molecules": 6703904.499197614,
  "dsi_vector_sum": 0.18976585660336784,
  "pd_rate_hz": 1.4285714285714286,
  "atp_soma": 6208226.253892355,
  "atp_ais": 480506.91302141146,
  "atp_dendrites_total": 15171.3322838489
}
```

Median MI (0.57), median ATP (6.7e6), moderate DSI (0.19), PD-rate 1.4 Hz. The triple of
(median MI, median ATP, modest DSI) is the central cluster of the spiking cohort.

These 11 cells motivate S-0123-02 (three-objective NSGA-II with DSI added) and S-0123-03
(Vm-trace deep-dive of a near-silent high-MI cell). Cell (27, 2555) vs (47, 4455) in
particular shows that **MI and ATP alone do not capture selectivity** -- the project's
first-question DSGC mission still needs DSI as an explicit objective.

## Analysis

* The **decoupled MI x ATP varimax structure** is the cleanest finding. In t0117, F1 jointly
  loaded on DSI (+0.42) and PD (+0.35). Here, the largest joint MI loading (F1, -0.358) is
  paired with a much smaller ATP loading (+0.205). The factor structure says: there exists a
  latent that primarily controls MI (with weak ATP coupling) and a different latent set that
  controls ATP. This is consistent with the PCA colourings — MI structure visible in the
  electrophys PCA, ATP structure visible in the morphology PCA.
* Despite decoupled latent structure, **MI and ATP are positively correlated at the cell
  level** (3.6x corner imbalance). The interpretation: NSGA-II preferentially explored the
  cheap-and-informative half of the substrate, leaving the expensive-and-uninformative half
  populated by gen-0 random init. The off-diagonal corners (343 high_MI/high_ATP + 341
  low_MI/low_ATP) are real but undersampled by the optimiser.
* The **electrophys signature of high-MI cells** (IH_GBAR -0.79, CAD_TAUR_MS -0.72, KDR_GBAR
  -0.67) is biologically interpretable: low Ih makes the cell more excitable, low KDR slows AP
  repolarisation, and low CAD_TAUR keeps intracellular Ca2+ transients sharp — all of which
  sharpen spike timing and increase the per-spike directional discriminability. The positive
  SK_AIS_GBAR (+0.63) is a counter-effect (SK_AIS would suppress firing) and needs deeper
  Vm-trace analysis.
* The **morphology signature of low-ATP cells** (mean_segment_length_um -0.73) makes geometric
  sense: shorter segments accumulate less Na+ inward current per AP. The positive
  branch_length_cv (+0.55) and branch_density_gradient_pd (+0.50) suggest that low-ATP cells
  have less uniform, more PD-asymmetric dendritic trees.
* The **ATP-share inversion** (76.7% soma vs Attwell-Laughlin's 4% soma / 82% axon) is the
  largest unexpected finding. It almost certainly reflects the t0080 model's lack of axonal
  myelination geometry and the procedural-AIS construction, both of which would normally shift
  ATP cost into the axon. Documented in `methodology_notes.md` and flagged for the
  compare-literature step.

## Cluster-group purity

| Partition | Reference | NMI | chi-square p | n |
| --- | --- | --- | --- | --- |
| electrophys_cluster | MI_quartile | 0.178 | 1.0e-236 | 3125 |
| electrophys_cluster | ATP_quartile | 0.186 | 1.0e-235 | 3125 |
| morphology_cluster | MI_quartile | 0.121 | 7.2e-162 | 3125 |
| morphology_cluster | ATP_quartile | 0.176 | 1.3e-258 | 3125 |

All four contingencies are highly significant (chi-square p < 1e-160) but NMI is low (<0.20),
meaning **clusters carry MI / ATP information but are not pure MI / ATP partitions**. The
electrophys clusters carry slightly more ATP info (0.186) than MI info (0.178). The morphology
clusters carry more ATP info (0.176) than MI info (0.121), consistent with the PCA-level
interpretation that morphology drives ATP more than MI.

## Verification

* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings) at check-deps.
* `verify_research_papers.py` — PASSED.
* `verify_research_code.py` — PASSED.
* `verify_plan.py` — PASSED.
* `verify_task_file.py`, `verify_task_metrics.py`, `verify_task_results.py`,
  `verify_task_folder.py`, `verify_logs.py` — to be run in `reporting` step.
* Inline answer-asset checker — PASSED for all 4 answer assets (zero errors / warnings).
  `verify_answer_asset.py` does not exist in this checkout.
* `ruff check --fix .` — clean.
* `ruff format .` — clean (7 files reformatted at first pass).
* `mypy -p tasks.t0125_t0123_cluster_factor_mi_atp.code` — Success.
* `pytest tasks/t0125_..._mi_atp/code/test_effect_sizes.py` — 6 passed.

## Limitations

* **Single NSGA-II seed** (seed 441). The cluster structure could be seed-specific in the same
  way t0116 / t0117 found seed-specific basins. The closest comparison would be replicating
  t0123 with a second GA seed and re-running this analysis.
* **MI ceiling at 2 bits**. The 4-direction protocol caps `mi_count_bits` at `log2(4) = 2.0`.
  The cohort already saturates at 1.459 bits (73% of the ceiling), so finer MI discrimination
  among the very-best cells is lost. A direct-method 8-direction MI rerun on the top-10 cells
  (already done by t0123) shows zero bits/s because the direct-method estimator needs more
  trials.
* **ATP recipe sensitivity**. The t0123 ATP-per-spike denominator can become unstable for
  near-silent cells; we excluded them with `pd_rate_hz > 1.0`. The Attwell-Laughlin comparison
  (and the soma-vs-axon inversion) hinges on the t0080 model's lack of an explicit myelinated
  axon. A future correction should either patch the model or normalise to within-class
  fractions only.
* **3.6x corner imbalance** means the off-diagonal corners (343 and 341 cells) have ~1/3.6 the
  statistical power of the diagonal corners for the per-corner mean and per-corner morphology
  gallery. Effect sizes from the rare corners are noisier.
* **No direct biological anchor**. The DSGC bits-per-ATP curve is not measured in published
  literature (only the fly photoreceptor data from Niven 2007 is the closest proxy). The
  compare-literature step will quantify the gap.

## Files Created

### Code

* `code/__init__.py`, `code/paths.py`, `code/constants.py`
* `code/load_t0123_cells.py`, `code/load_t0123_gen0.py`, `code/fit_standardiser.py`
* `code/group_thresholds.py`, `code/cluster_helpers.py`
* `code/pca_with_overlay.py`, `code/cluster_electrophys.py`, `code/cluster_morphology.py`
* `code/factor_analysis.py`
* `code/effect_sizes.py` (with `test_effect_sizes.py`, 6 tests), `code/group_comparison.py`,
  `code/corner_heatmap.py`, `code/atp_compartment_shares.py`, `code/cluster_group_purity.py`
* `code/morphology_rendering.py`, `code/render_electrophys_cluster_morphs.py`

### Data (`data/`)

* `t0125_cells.parquet` (full cohort, 5760 rows, 2.5 MB)
* `t0125_spiking_cells.parquet` (3125 rows, 1.4 MB)
* `t0125_gen0.parquet` (96 rows, 110 KB)
* `t0125_standardiser.npz`, `pca_models.pkl`

### Results tables (`results/data/`)

* `pool_counts.csv`, `group_thresholds.json`, `gen0_displacement.csv`
* `electrophys_clusters.csv`, `morphology_clusters.csv`
* `morphology_cluster_0_representatives.csv` ... `morphology_cluster_4_representatives.csv`
* `factor_correlations.csv`, `factor_loadings.csv`
* `group_comparison.csv` (68 parameters x 12 stats columns)
* `corner_param_means.csv` (68 parameters x 4 corners, z-scored)
* `atp_compartment_shares.csv` (per-cell soma / AIS / dendrite shares)
* `cluster_group_purity.csv` (4 NMI rows)
* `methodology_notes.md` (deltas from t0117 template, headline findings preview, reading
  order)

### Charts (`results/images/`)

* `pca_combined_color_mi.png`, `pca_combined_color_atp.png`, `pca_combined_color_corner.png`
* `pca_with_gen0_overlay.png`
* `electrophys_silhouette.png`, `morphology_silhouette.png`
* `electrophys_cluster_0_morphs.png` ... `electrophys_cluster_3_morphs.png`
* `factor_loadings_heatmap.png`
* `cliffs_delta_high_vs_low_mi.png`, `cliffs_delta_high_vs_low_atp.png`
* `corner_param_heatmap.png`
* `atp_share_ternary.png`, `atp_share_violins.png`

### Answer assets (`assets/answer/`)

* `mi-atp-joint-structure-in-t0123-substrate/` (details.json + short_answer.md +
  full_answer.md)
* `high-vs-low-mi-electrophys-signature/`
* `low-vs-high-atp-morphology-signature/`
* `pareto-favoured-corner-signature/`

### Result documents

* `results_summary.md`, `results_detailed.md`, `metrics.json` (`{}`), `costs.json`
  (`{"total_cost_usd": 0, "breakdown": {}}`), `remote_machines_used.json` (`[]`)

## Task Requirement Coverage

Operative task text from `task.json`:

> Name: "Cluster + factor analysis of t0123 cells: high vs low MI and ATP". Short description: "PCA
> \+ KMeans on electrophys (54-d) and morphology (14-d) + varimax FA on 68-d for t0123 cells;
> quartile-group comparisons of high vs low MI and high vs low ATP-per-spike."

The long description in `task_description.md` enumerates the data source (t0123 predictions
asset, single seed 441), the dual full / spiking cohort definition, the MI x ATP quartile
group definitions, 10 analyses to run (PCA / KMeans / FA / Cliff's delta / corner heatmap /
ATP shares / cluster purity / morphology galleries), and four answer-asset questions (MI-ATP
joint structure, high-vs-low MI electrophys signature, low-vs-high ATP morphology signature,
Pareto-favoured corner signature).

The plan refines these into **REQ-1 through REQ-22**. Status:

| REQ | Status | Result | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Done | 5760 raw t0123 cells loaded from `predictions.jsonl.gz` | `results/data/pool_counts.csv` |
| REQ-2 | Done | Dedup at 6 decimals retained all 5760 cells | `pool_counts.csv` (`dedup_unique_count == 5760`) |
| REQ-3 | Done | Full + spiking cohorts persisted | `data/t0125_cells.parquet` (5760) and `data/t0125_spiking_cells.parquet` (3125) |
| REQ-4 | Done | Quartile + median thresholds + corner counts persisted | `results/data/group_thresholds.json` |
| REQ-5 | Done | Standardiser fitted ONCE on the full cohort | `data/t0125_standardiser.npz` |
| REQ-6 | Done | Three-panel PCA coloured by MI | `results/images/pca_combined_color_mi.png` |
| REQ-7 | Done | Three-panel PCA coloured by ATP (log10) | `results/images/pca_combined_color_atp.png` |
| REQ-8 | Done | Three-panel PCA coloured by MI x ATP corner | `results/images/pca_combined_color_corner.png` |
| REQ-9 | Done | Gen-0 overlay + per-corner displacement table | `results/images/pca_with_gen0_overlay.png`, `results/data/gen0_displacement.csv` |
| REQ-10 | Done | Electrophys KMeans, headline k=4 | `results/images/electrophys_silhouette.png`, `results/data/electrophys_clusters.csv` |
| REQ-11 | Done | 4 morphology grids (5x3=15 cells each), full dendrite trees, ranked by bits-per-ATP | `results/images/electrophys_cluster_{0..3}_morphs.png` |
| REQ-12 | Done | Morphology KMeans, k=5, silhouette + 5 representative tables | `results/images/morphology_silhouette.png`, `results/data/morphology_clusters.csv`, `morphology_cluster_{0..4}_representatives.csv` |
| REQ-13 | Done | FA with 10 varimax factors, joint_mi_atp_flag, classification, all 4 outcome r columns. Joint factor count = 0 | `results/data/factor_correlations.csv`, `factor_loadings.csv`, `results/images/factor_loadings_heatmap.png` |
| REQ-14 | Done | 68-row per-parameter group comparison (mean / std / MWU p / Cliff's delta) for MI and ATP | `results/data/group_comparison.csv` |
| REQ-15 | Done | Top-20 Cliff's delta bar charts for MI and ATP | `results/images/cliffs_delta_high_vs_low_{mi,atp}.png` |
| REQ-16 | Done | 68 x 4 z-scored corner means table + heatmap | `results/data/corner_param_means.csv`, `results/images/corner_param_heatmap.png` |
| REQ-17 | Done | Per-cell ATP compartment shares + ternary + violin panel | `results/data/atp_compartment_shares.csv`, `results/images/atp_share_{ternary,violins}.png` |
| REQ-18 | Done | 4 (partition, reference) NMI + chi-square rows | `results/data/cluster_group_purity.csv` |
| REQ-19 | Done | Methodology notes with t0117 -> t0125 deltas, headline preview, reading order | `results/data/methodology_notes.md` |
| REQ-20 | Done | 4 answer assets, all pass spec checks | `assets/answer/{mi-atp-joint-structure-in-t0123-substrate, high-vs-low-mi-electrophys-signature, low-vs-high-atp-morphology-signature, pareto-favoured-corner-signature}/` |
| REQ-21 | Done | Top-5 parameter tables present in answer documents 2, 3, 4 | full_answer.md in answers 2, 3, 4 |
| REQ-22 | Done | Per-corner counts + per-corner means | `results/data/corner_param_means.csv` + `group_thresholds.json` |

**All 22 plan requirements are Done. No requirements are Partial or Not done.**

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0125_t0123_cluster_factor_mi_atp" date_compared: "2026-05-25"
---
# Comparison with Project and Published Results

## Summary

The headline comparison is project-internal: t0117 confirmed F1 as a joint DSI x PD varimax
factor in the unfiltered 4-seed pool (**r_DSI = +0.421**, **r_PD = +0.352**, **12.6 %
variance**), generalising the truncated-cohort artefact to the DSI / PD pair. t0125 ran the
same pipeline (PCA + KMeans + Kaiser-cap varimax FA) on the t0123 MI / ATP-per-spike
single-seed pool of 5,760 cells and **does not** reproduce a joint factor: the largest joint
loading is F1 with **r_MI = -0.358** but only **r_ATP = +0.205**, below the **|r| > 0.30**
threshold on the ATP axis (**0 joint factors** total). The MI / ATP pair therefore behaves
opposite to DSI / PD: the truncated-cohort artefact does **not** generalise — MI and ATP are
decoupled at the latent level even in the unfiltered NSGA-II output. Against published
methodology, t0125's headline ephys k = **4** and morphology k = **5** are an order of
magnitude smaller than [Baden2016][baden2016]'s **32** mouse-RGC functional types from a real
~11,000-cell cohort, and the low ephys silhouette (**0.083**) is consistent with the parameter
degeneracy [Achard2006][achard2006] reports on Purkinje-cell ensembles (20 acceptable models
lying on "loosely connected hyperplanes"). [Niven2007][niven2007]-style bits-per-ATP scaling
is not re-tested here; it is fully covered by [t0123]'s `compare_literature.md` (Insufficient
evidence: post-hoc Strong-Bialek MI = 0 on top-10 Pareto cells).

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0117] (unfiltered 4-seed DSI x PD pool, varimax F1) | r on first objective (DSI) | +0.421 | -0.358 | -0.779 | t0125 F1 loads on MI with magnitude **0.358** vs t0117 F1 on DSI **0.421**. Sign differs; magnitude is similar. Variance fraction not directly comparable (different pool size and objective pair) |
| [t0117] (unfiltered 4-seed DSI x PD pool, varimax F1) | r on second objective (PD vs ATP) | +0.352 | +0.205 | -0.147 | t0125 F1's ATP loading is **+0.205** vs t0117 F1's PD loading **+0.352** — t0125 fails the joint-threshold on the second axis (needs &#124;r&#124; > 0.30) |
| [t0117] (unfiltered pool, joint factor count) | n_joint_factors (&#124;r&#124; > 0.30 on both) | 1 | 0 | -1 | t0117 found exactly one joint DSI-PD factor; t0125 finds **zero** joint MI-ATP factors across all 10 varimax components. **The truncated-cohort artefact does not generalise to MI x ATP** |
| [t0117] (unfiltered pool, electrophys KMeans) | k_headline (mean silhouette) | 4 (0.158) | 4 (0.083) | k +0, silhouette -0.075 | t0125 picks the same k = 4 on the electrophys subspace but at roughly half the silhouette quality. Smaller cohort (3,125 spiking vs 4,431) and lower-dimensional structure both plausible drivers |
| [t0117] (unfiltered pool, morphology KMeans) | k_headline (mean silhouette) | 5 (0.153) | 5 (0.158) | k +0, silhouette +0.005 | Same k = 5 on the morphology subspace and within rounding of t0117's silhouette — morphology subspace clusters more cleanly than the electrophys subspace in **both** tasks |
| [t0123] (NSGA-II MI vs ATP, single seed 441) | n_evaluated_cells | 5760 | 5760 | 0 | t0125 consumes the t0123 predictions asset verbatim; cohort identity is enforced |
| [t0123] (NSGA-II MI vs ATP, top-Pareto MI) | mi_count_bits | 1.459 | 1.459 | 0 | Top-MI cell `(51, 4810)` reproduced exactly; same predictions asset, same MI ceiling at 73 % of log2(4) = 2.0 |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Baden2016][baden2016] (mouse RGC functional fingerprints, Mixture-of-Gaussians + BIC) | n_clusters_total | 32 RGC functional types | 4 (ephys) + 5 (morphology) | -27 to -28 | [Baden2016, Methods, p. 348 + Results, Fig 2]: clustered ~11,000 mouse RGCs into **32 functional types** plus 17 displaced amacrine types. t0125 finds **4** ephys + **5** morphology KMeans clusters in 5,760 simulated cells — roughly an order of magnitude lower diversity than the biological cohort. Direction: simulated DSGCs from a single 68-d substrate are far less heterogeneous than the real mouse RGC population — expected, because the t0123 NSGA-II explores one cell-type-equivalent parameter cube |
| [Baden2016][baden2016] (cluster-count selection criterion) | criterion | BIC (full curve reported, peak at 32) | silhouette (full sweep k in [3, 7] reported, peak at 4 ephys / 5 morph) | n/a | Methodological difference flagged in [Baden2016, Methods, p. 348]: BIC penalises model complexity and is appropriate for the Mixture-of-Gaussians family; silhouette is geometric and appropriate for KMeans. The two criteria can disagree; t0125 reports the full silhouette curves on disk (`electrophys_silhouette.png`, `morphology_silhouette.png`) per Baden's reporting convention |
| [Achard2006][achard2006] (Purkinje 24-parameter ensemble, 20 acceptable models) | manifold shape | "loosely connected hyperplanes" (thin lower-d sub-manifolds; per-channel ranges narrow on 4 of 24 params, full-range on others; grid search would miss ~65 %) | low electrophys silhouette **0.083** + low NMI vs MI quartile **0.178** + low NMI vs ATP quartile **0.186** | n/a | [Achard2006, Discussion]: the high-d parameter landscape of an MOO-acceptable ensemble forms thin sub-manifolds, not blobs — KMeans on such structure produces poorly-separated clusters (low silhouette) yet still captures statistically significant structure (chi-square p < 1e-160 in t0125). t0125's low ephys silhouette is **consistent** with the Achard "hyperplane" picture: clusters carry MI / ATP information but are not pure MI / ATP partitions |
| [Achard2006][achard2006] (per-parameter variability across acceptable models) | n_params_with_full_range | 4 of 24 (full range); 4 of 24 (tightly bounded) | top-5 Cliff's delta for MI: IH_GBAR **-0.79**, CAD_TAUR_MS **-0.72**, KDR_GBAR **-0.67**, SK_AIS_GBAR **+0.63**, SKAHP_TAU_CA_MULTIPLIER **-0.63** | n/a | [Achard2006][achard2006] enumerates 4 / 24 channels varying across the entire allowed range. t0125 reports 5 / 68 parameters with &#124;Cliff's delta&#124; > 0.6 for MI groups (the top-5 listed). Direction: ratio of "strongly discriminating" parameters in t0125 (~7 %) is similar to Achard's "tightly bounded" ratio (~17 %) — both ensembles concentrate the functional axis on a minority of the parameter cube, consistent with [Marder2006][marder2006]'s parameter-degeneracy framing |
| [Attwell2001][attwell2001] (rodent cortical neuron, biophysical accounting) | ATP compartment share (axon, dendrites, soma) | 82 % axon, 14 % dendrites, 4 % soma | 5.5 % AIS, 17.8 % dendrites, 76.7 % soma (spiking cohort means) | -76.5 pp axon / +3.8 pp dendrites / +72.7 pp soma | [Attwell2001, Table 4, p. 1140]: rodent cortical neuron AP energy budget is axon-dominated (82 %). t0125 t0123 cells are **soma-dominated** (76.7 %). The inversion is documented in t0125 `methodology_notes.md` and originally attributed to the t0080 model's lack of explicit myelinated axon and the procedural-AIS construction; the AIS share (5.5 %) is **15x smaller** than Attwell's axon collateral share. This is a model-architecture artefact, not a biological finding |
| [Sengupta2010][sengupta2010] (cross-cell-type ATP per AP, soma vs axon split) | ATP per AP ratio across cell types | 17-fold range across 7 HH models; alpha (Na+/K+ overlap) **1.0-1.5** for mammals | per-cell ATP/spike range in spiking cohort: ATP Q1 / Q3 = **5.30e6** / **1.24e7** (2.3-fold IQR); per-corner mean ATP-share of soma rises to 93 % in low-ATP corner | n/a | [Sengupta2010, Table 1, p. 5]: 17-fold ATP range across seven HH models is the published prior; t0125's 2.3-fold IQR is **narrower**, reflecting that the t0123 NSGA-II explored a single parameter cube rather than seven distinct cell types. The low-ATP corner concentrating to 93 % soma share is **qualitatively** consistent with Sengupta's "Na+/K+ overlap concentrates where Nav density is highest" but quantitatively inverted from Attwell's axon-dominated picture (see row above) |
| [Niven2007][niven2007] (fly photoreceptors, bits-per-ATP Pareto) | bits_per_sec | 200-1000 (4 species) | not re-computed | n/a | Already analysed in `tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/compare_literature.md` (Niven 2007 verdict: **Insufficient evidence** — post-hoc Strong-Bialek MI = 0 bits/s on all 10 top-Pareto cells because PD-rate 1-3 Hz is too low). t0125 does not re-run the bits/s comparison; the cluster-and-factor analysis is on `mi_count_bits` (the inner-loop count-MI surrogate) rather than the bits/s axis |

## Methodology Differences

* **Pool composition (t0117 vs t0125)**: t0117 pooled **4** NSGA-II seeds (9,124 raw cells,
  4,431 dedup-unique) on a DSI x PD-cube objective pair; t0125 used **1** seed (441) on a MI x
  ATP-per-spike pair (5,760 raw, 5,760 dedup-unique). The single-seed design weakens
  generalisation of the joint-factor verdict — a 4-seed MI / ATP replicate is the natural
  follow-up.

* **Cohort filter (t0117 vs t0125)**: both pipelines fit standardiser / PCA / KMeans / FA on
  the full-cohort union (no filter). t0125 additionally analyses a **spiking** subcohort
  (`pd_rate_hz > 1.0 AND not silence_failed`, n = 3,125) for the ATP-per-spike comparison
  because near-silent cells drive the denominator toward zero. Group comparisons (Cliff's
  delta, corner heatmap, ATP compartment shares) use the spiking subcohort; PCA / FA fits use
  the full cohort.

* **Joint-factor threshold (t0117 vs t0125)**: both use **|r| > 0.30** on each of the two
  objectives as the joint-factor criterion. The threshold is held constant to make the
  verdicts directly comparable.

* **Cluster-count selection criterion (t0125 vs Baden 2016)**: t0125 uses silhouette on KMeans
  (k in [3, 7]); [Baden2016][baden2016] uses BIC on Mixture-of-Gaussians. Both report the full
  curve. BIC penalises complexity and produced 32 clusters on real cells; silhouette is
  geometric and produced 4-5 on simulated cells. The order-of-magnitude difference is partly a
  criterion mismatch and partly a cohort-diversity mismatch — disentangling the two would
  require re-running BIC on t0125's data.

* **Cell type and substrate (t0125 vs Baden 2016)**: [Baden2016][baden2016] clusters ~11,000
  mouse RGCs experimentally measured by two-photon Ca2+ imaging on functional features (SVD of
  moving-bar responses + chirp + colour + receptive field + soma area + ON/OFF index + DSi +
  OSi + IHC); t0125 clusters 5,760 simulated DSGCs on the 68-d Bed B + 14-d morphology
  parameter vector. The two feature spaces are fundamentally different (function vs
  parameter), so cluster counts cannot be directly compared — but the *order-of-magnitude* gap
  (32 vs 4-5) is informative about the diversity ceiling of the t0123 substrate.

* **Parameter-ensemble analysis tool (t0125 vs Achard 2006)**: [Achard2006][achard2006]
  reports per-channel ranges across 20 acceptable Purkinje models; t0125 reports varimax
  factor loadings, Cliff's delta, and KMeans cluster purity on 5,760 t0123 cells. The two
  analyses are complementary — Achard shows what *individual parameters* do; t0125 shows what
  *factor axes* do. The "loose hyperplane" geometry Achard infers from per-channel ranges
  manifests in t0125 as low silhouette (clusters are not blob-like) combined with high
  chi-square significance (clusters carry real information).

* **ATP recipe (t0125 vs Attwell-Laughlin)**: t0125 consumes the per-cell
  `atp_per_spike_molecules` and `atp_per_ap_compartment_breakdown` from t0123 verbatim. The
  t0080 model lacks an explicit myelinated axon, so Attwell's 82 % axon-collateral share has
  no analogue in the simulation; the t0080 AIS is a procedural construct that contributes only
  5.5 % of per-AP ATP. The soma-dominated share (76.7 %) is consequently a model-architecture
  artefact, not a contradicting biological finding.

* **No published MI / ATP NSGA-II ensemble exists**: [Hay2011][hay2011],
  [Druckmann2007][druckmann2007], [VanGeit2016][vangeit2016], [Achard2006][achard2006] all
  optimise to *electrophysiological-feature* targets, not to information / energy objectives.
  The closest analogue, [Remme2018][remme2018] (MSO coincidence-detector vs energy MOBO), is
  not present in the project paper corpus. t0125 has no direct published factor-analysis
  precedent for a function-vs-energy MOO ensemble; the project-internal t0117 / t0116 / t0108
  lineage is the only methodological precedent.

## Analysis

### Truncated-cohort artefact does NOT generalise from DSI x PD to MI x ATP

The headline finding is **negative for the joint-driver hypothesis**. t0117 confirmed F1 as a
joint DSI x PD factor in the unfiltered 4-seed pool with **r_DSI = +0.421** and **r_PD =
+0.352**, both crossing the **|r| > 0.30** threshold and together explaining **12.6 %** of the
variance, and explicitly framed this as confirmation of the truncated-cohort artefact (t0116's
strict cohort erased the joint axis). t0125 ran the equivalent pipeline on the t0123
unfiltered pool of 5,760 cells with the same threshold and the same Kaiser-cap = 10 factor
budget, and found **zero** joint MI x ATP factors. The closest candidate F1 loads on MI with
**r_MI = -0.358** (above threshold) but only **r_ATP = +0.205** (below threshold); F2 loads on
MI with **r_MI = +0.463** but has **r_ATP = +0.063**. The factor structure is **decoupled**:
one set of latents controls MI, another set controls ATP, and the diagonal-corner cell-level
correlation (**3.6x** imbalance) emerges from NSGA-II actively exploring the
cheap-and-informative half of the cube rather than from a shared latent driver. The two
truncated-cohort experiments together suggest the artefact is **objective-pair specific**: DSI
/ PD reveal a joint axis when the silence guard is removed; MI / ATP do not.

### Cluster diversity is an order of magnitude below the biological RGC cohort

t0125 finds **4** electrophys clusters + **5** morphology clusters (silhouette peaks) in 5,760
simulated cells. [Baden2016, Fig 2] reports **32** RGC functional types + 17 displaced
amacrine types in ~11,000 mouse RGCs measured by two-photon Ca2+ imaging. The
order-of-magnitude gap is consistent with the simulation exploring a single
cell-type-equivalent parameter cube (one 68-d Bed B + 14-d morphology substrate, one set of
channel gating kinetics), whereas the biological cohort spans the full mouse RGC diversity.
The morphology silhouette **0.158** (higher than the electrophys **0.083**) confirms Baden's
observation that morphological / functional dimensions separate cell types more cleanly than
purely electrophysiological dimensions. The cluster-count mismatch is a **cohort-diversity
limitation** of the t0123 substrate, not a methodological defect.

### Low silhouette is consistent with Achard's "loose hyperplane" geometry

[Achard2006][achard2006] characterises the 24-parameter Purkinje-cell parameter landscape as
"a collection of loosely connected hyperplanes" — thin lower-dimensional manifolds where 4 of
24 channels vary across the entire allowed range while others are tightly bounded, and a 6 /
10-point-per-dimension grid search misses ~65 % of the acceptable region. t0125's electrophys
silhouette **0.083** is low in absolute terms but the chi-square p-value for ephys-cluster vs
MI-quartile contingency is **1e-236** (highly significant). The combination — low silhouette +
high chi-square — is the signature of hyperplane-like rather than blob-like cluster geometry:
the clusters are real (carry information) but not well-separated (lie on thin sub-manifolds
rather than tight balls). The top-5 Cliff's delta parameters for MI (IH_GBAR **-0.79**,
CAD_TAUR_MS **-0.72**, KDR_GBAR **-0.67**, SK_AIS_GBAR **+0.63**, SKAHP_TAU_CA_MULTIPLIER
**-0.63**) act as the "Achard-style narrow-range" channels — 5 of 68 parameters (~7 %) drive
most of the MI variance, with the remainder distributed broadly. This pattern is what
[Marder2006][marder2006]'s parameter-degeneracy framing predicts: compensating channels
co-vary along factor axes, and only a small subset of channels are functionally constrained at
any one operating point.

### ATP compartment-share inversion is a model-architecture artefact

The soma-dominated ATP split (mean **76.7 %** soma, **17.8 %** dendrites, **5.5 %** AIS) is
inverted from [Attwell2001, Table 4]'s axon-dominated rodent cortical breakdown (**82 %** axon
collaterals, **14 %** dendrites, **4 %** soma). The inversion is documented in t0125's
`methodology_notes.md` and is attributed to the t0080 model's lack of an explicit myelinated
axon and the procedural construction of the AIS. [Sengupta2010, Eq 9]'s "Na+/K+ overlap
concentrates where Nav density is highest" predicts the soma will dominate in the t0080 /
t0123 substrate because the procedural cells place most Nav density at the soma. This is the
second cross-task finding (after the joint-factor result above) where t0125 does not reproduce
a published / prior pattern in the t0123 substrate, and in both cases the cause is traceable
to a single design choice (NSGA-II objective set in the first case; cell-architecture choice
in the second).

### Why t0123's Niven 2007 comparison is not re-analysed here

[t0123]'s `compare_literature.md` already addresses the [Niven2007][niven2007]-anchored
bits-per-ATP Pareto comparison and concluded **Insufficient evidence**: the post-hoc
Strong-Bialek direct-method MI collapsed to **0.0 bits/s** for all 10 top-Pareto cells because
PD firing rates of 1-3 Hz cannot populate non-trivial spike-time words at word lengths T <=
100 ms. t0125 does not re-run the comparison because the cluster-and-factor analysis operates
on `mi_count_bits` (the inner-loop count-MI surrogate, ceiling **log2(4) = 2.0 bits**, top
cell **1.459 bits**) rather than the bits/s axis. The Niven comparison remains a missing-paper
observation for downstream tasks; t0125's contribution is the latent-structure verdict (no
joint factor), not the Pareto-front placement.

## Limitations

* **Single NSGA-II seed** (seed 441). The joint-factor verdict (zero) could in principle be a
  single-seed accident, in the same way that t0116 (single-seed-equivalent strict cohort)
  showed zero joint DSI-PD factors before t0117 (4-seed unfiltered) found one. The natural
  follow-up is a multi-seed MI / ATP replicate (suggestion-asset candidate for the t0125
  reporting stage).

* **Joint-factor threshold sensitivity**. The **|r| > 0.30** threshold is inherited from t0108
  / t0116 / t0117 for direct comparability, but t0125's F1 has **r_MI = -0.358** + **r_ATP =
  +0.205** — only **0.095** below the ATP threshold. A threshold of **|r| > 0.20** would
  reclassify F1 as joint. The verdict is robust at the literature-comparable **|r| > 0.30**
  value but should not be interpreted as a sharp dichotomy.

* **MI ceiling at 2 bits**. The 4-direction protocol caps `mi_count_bits` at **log2(4) =
  2.0**; 73 % of the ceiling is reached. Cells near the ceiling have compressed MI variance,
  which weakens the Pearson r of factor scores vs MI and pulls all joint loadings toward zero.
  An 8-direction or 16-direction protocol with a higher MI ceiling would re-test the
  joint-factor verdict at higher resolution.

* **No published function-vs-energy MOO factor analysis exists in the corpus**. The closest
  published analogue is [Remme2018][remme2018] (MSO coincidence-detector vs energy MOBO, DOI
  `10.1371/journal.pcbi.1006612`), which is not present as a paper asset. The joint-factor
  verdict cannot be benchmarked against a directly comparable published number; the strongest
  published anchor is [Achard2006][achard2006]'s per-channel-range analysis on a 24-parameter
  Purkinje ensemble, which is a methodological cousin rather than a direct comparator.

* **Baden 2016 cluster count is not directly comparable**. [Baden2016][baden2016]'s 32 RGC
  functional types are derived from real-cell functional fingerprints (SVD of light-driven
  Ca2+ responses, chirp, colour, RF, morphology, IHC markers), not from a model-parameter
  vector. The order-of-magnitude gap (32 biological vs 4-5 simulated) is informative about the
  diversity ceiling of the t0123 substrate but should not be interpreted as a methodological
  deficiency of the t0125 pipeline.

* **ATP compartment-share inversion**. The 76.7 % soma share vs Attwell's 4 % soma share is a
  model-architecture artefact (t0080 lacks an explicit myelinated axon). The inversion is
  documented and flagged; it does not contradict [Attwell2001][attwell2001] biologically, only
  computationally. A model-correction follow-up adding an explicit axon would resolve this and
  is a candidate suggestion for downstream tasks.

* **Carter-Bean 2009 paper is not in the project corpus**. The strict ATP/AP/cm benchmark was
  flagged as a plan typo in [t0123]'s compare_literature; t0125 inherits the same limitation
  and cannot re-verify against the original paper (DOI `10.1016/j.neuron.2009.12.011`).

[achard2006]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md
[attwell2001]:
../../t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/summary.md
[baden2016]:
../../t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/summary.md
[druckmann2007]:
../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md [hay2011]:
../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[marder2006]: ../../t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/summary.md [niven2007]:
https://doi.org/10.1242/jeb.005249 [remme2018]: https://doi.org/10.1371/journal.pcbi.1006612
[sengupta2010]:
../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/summary.md
[vangeit2016]: ../../t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/summary.md
[t0117]: ../../t0117_pooled_pca_cluster_factor_all_cells_4_seeds/ [t0123]:
../../t0123_bedb_mi_atp_per_spike_nsga2/

</details>
