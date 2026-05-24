# Cluster + Factor Analysis of t0123 Cells: High vs Low MI and ATP

## Motivation

t0123 ran a single-seed (seed 441) 60-generation NSGA-II maximising spike-count mutual information
(`mi_count_bits`) and minimising metabolic cost (`atp_per_spike_molecules`) on the 68-d Bed B + 14-d
morphology substrate. The run produced 5760 evaluated cells, 10 Pareto cells, and reported a best
`mi_count_bits = 1.459` (73% of the `log2(4) = 2.0` ceiling) and a minimum
`atp_per_spike_molecules = 6.76e5`.

The single-cell Pareto front answers "where does the DSGC bits-per-ATP front sit relative to Niven
2007" but says nothing about **how** the 68-d parameter space organises around the two objectives.
Before launching the 3-objective MI + DSI + ATP follow-up (S-0123-02), we need to know:

* Are high-MI cells and low-ATP cells found in the same regions of the 68-d substrate, or do they
  occupy disjoint clusters?
* Which electrophys parameters (channel densities, synapse densities, axial resistance, etc.)
  systematically differ between high-MI and low-MI cells? Between low-ATP and high-ATP cells?
* Which morphology parameters (segment count, branch order, segment diameter, segment length, soma
  share, etc.) differ across the four corner groups (high-MI / low-ATP, high-MI / high-ATP, low-MI /
  low-ATP, low-MI / high-ATP)?
* Does at least one varimax factor on the 68-d vector load jointly on MI and ATP — implying a
  shared latent driver — or do separate factors drive each objective?
* How does the per-compartment ATP cost share (soma / AIS / dendrites; from
  `atp_per_ap_compartment_breakdown`) covary with the MI and ATP groupings?

This task applies the canonical t0108 / t0116 / t0117 cluster-and-factor pipeline (PCA + KMeans on
electrophys-only and morphology-only subspaces + Kaiser-cap varimax factor analysis on the full 68-d
vector) to the t0123 cell pool, replacing the prior DSI / PD axes with MI and ATP-per-spike.

## Scope

### Data source (one NSGA-II run, single GA seed)

* `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`
  — seed 441, all 5760 cells evaluated by the t0123 NSGA-II run.

Use the predictions asset as the authoritative data source, not
`results/data/all_evaluations_seed441.json.gz` (same content, different format).

### Pool definition

* Load every record from the predictions asset.
* Deduplicate by the 68-d vector rounded to 6 decimals (`DEDUP_DECIMALS = 6`, same convention as
  t0108 / t0116 / t0117).
* Record raw count, dedup-unique count, and post-filter counts (see below) before any analysis.

### Cohort filter

Two cohorts are analysed in parallel:

1. **Full cohort** — every dedup-unique cell, including near-silent cells. This is the primary
   pool for PCA, KMeans, and factor analysis (mirrors t0117's full-cohort design).
2. **Spiking cohort** — cells with `pd_rate_hz > 1.0 Hz` AND `silence_failed_bool == False`. This
   is required for the ATP-per-spike comparison because near-silent cells have a denominator
   approaching zero and produce unstable `atp_per_spike_molecules` values. Used for the
   group-comparison and Pareto-corner analyses.

Per-cohort counts must be reported in `results_detailed.md`.

### Feature vector

Identical to t0108 / t0117: 68-d `vector_68d` with indices 0-53 the 54-d Bed-B electrophys vector
and 54-67 the 14-d morphology vector. Authoritative names in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` `ALL_PARAM_NAMES`.

### Group definitions

For the spiking cohort:

* **MI groups**: top quartile by `mi_count_bits` = "high MI"; bottom quartile = "low MI".
* **ATP groups**: top quartile by `atp_per_spike_molecules` = "high ATP"; bottom quartile = "low
  ATP".
* **MI x ATP corners**: four 2 x 2 quadrants formed by the median split on each axis. Cells in the
  top-left quadrant (high MI, low ATP) are the "Pareto-favoured" corner; bottom-right (low MI, high
  ATP) is the "dominated" corner.

Quartile and median thresholds must be recorded in `results/data/group_thresholds.json`.

### Analyses to run

1. **Combined 68-d PCA + side panels (one figure, three subplots).** Combined PCA / electrophys-only
   PCA / morphology-only PCA, each panel showing PC1 vs PC2 of the full cohort, coloured by
   `mi_count_bits` (viridis). Per-panel report of `% variance explained` for PC1 and PC2. Saved to
   `results/images/pca_combined_color_mi.png`.

2. **Same three-panel figure coloured by `atp_per_spike_molecules`** (log10, viridis). Saved to
   `results/images/pca_combined_color_atp.png`.

3. **Same three-panel figure coloured by MI x ATP corner** (4 categorical colours from tab10). Saved
   to `results/images/pca_combined_color_corner.png`.

4. **Gen-0 (`generation == 1`) random-init overlay.** Same axes as Step 1, with the 96 gen-0
   individuals projected onto the PCAs fitted in Step 1 (no refit; reuse the standardiser). Compute
   mean and 95th-percentile Euclidean displacement in PC1+PC2 space and in 68-d standardised space,
   both overall and per MI x ATP corner. Saved to `results/images/pca_with_gen0_overlay.png` and
   `results/data/gen0_displacement.csv`.

5. **KMeans on 54-d electrophys subspace, auto-pick k in [3, 7] by silhouette.** Standardiser fit on
   the full-cohort union pool. Pick k by maximum mean silhouette. Report silhouette curve, chosen k,
   per-cluster cell counts, and per-cluster mean MI / ATP / DSI / PD / firing-rate. Saved to
   `results/images/electrophys_silhouette.png` and `results/data/electrophys_clusters.csv`. For each
   cluster render a 5 x 3 grid of 15 representative cells (full dendrite trees via NEURON pt3d —
   not somas; per memory `feedback_top50_morphologies_full_dendrites.md`). Representatives ranked by
   `mi_count_bits / atp_per_spike_molecules` (bits-per-ATP) within cluster, restricted to the
   spiking cohort. Saved to `results/images/electrophys_cluster_<k>_morphs.png` (one PNG per
   cluster).

6. **KMeans on 14-d morphology subspace, auto-pick k in [3, 7] by silhouette.** Same procedure on
   the morphology subspace. For each morphology cluster, write a 15-row representative table with
   `(generation, cell_index, mi_count_bits, atp_per_spike_molecules, dsi_vector_sum, pd_rate_hz, ephys_PC1, ephys_PC2, ephys_PC3, soma_share_atp)`
   where `soma_share_atp` is the soma fraction of `atp_per_ap_compartment_breakdown`. Saved to
   `results/data/morphology_cluster_<k>_representatives.csv`.

7. **Factor analysis on the full 68-d feature matrix, Kaiser criterion, varimax-rotated.**
   Standardise the full cohort -> fit `sklearn.decomposition.FactorAnalysis(n_components=68)`; count
   Kaiser eigenvalues > 1 from the correlation matrix; cap at `KAISER_FACTOR_CAP = 10` (inherited
   from t0108); refit FA with the chosen count; apply varimax rotation via the iterative-SVD helper
   from t0108. Render the loadings heatmap with `RdBu_r` colourmap and symmetric vmin/vmax to
   `results/images/factor_loadings_heatmap.png`. Report per-factor variance and Pearson r vs
   `mi_count_bits` AND `atp_per_spike_molecules` AND `dsi_vector_sum` AND `pd_rate_hz` in
   `results/data/factor_correlations.csv`. Identify any factor with |r| > 0.3 on both MI AND ATP
   (joint factor) and any factor with |r| > 0.3 on MI only or ATP only (decoupled factors).

8. **High vs low group comparison (electrophys + morphology).** For each of the 68 parameters,
   compute on the spiking cohort:

   * Mean and standard deviation in the high-MI group, low-MI group, high-ATP group, low-ATP group.
   * Mann-Whitney U two-sided p-value: high-MI vs low-MI, high-ATP vs low-ATP.
   * Cliff's delta effect size (non-parametric): high-MI vs low-MI, high-ATP vs low-ATP.

   Save the full table to `results/data/group_comparison.csv`. Render two ranked bar charts of
   Cliff's delta:

   * `results/images/cliffs_delta_high_vs_low_mi.png` -- top-20 parameters by |delta| for MI.
   * `results/images/cliffs_delta_high_vs_low_atp.png` -- top-20 parameters by |delta| for ATP.

9. **2 x 2 corner heatmap.** For the 68 parameters, compute the mean (z-scored on the full cohort)
   in each of the four MI x ATP corners. Render as a 68 x 4 heatmap (RdBu_r, symmetric vmin/vmax) to
   `results/images/corner_param_heatmap.png` and save the underlying matrix to
   `results/data/corner_param_means.csv`. This is the central visualisation answering "what
   distinguishes the Pareto-favoured corner from the dominated corner".

10. **ATP compartment breakdown.** Using `atp_per_ap_compartment_breakdown` (keys: `soma`, `ais`,
    `dendrites_total`), compute the per-cell soma / AIS / dendrite **shares** of total per-AP ATP
    cost on the spiking cohort. Compare share distributions across MI groups (high vs low) and ATP
    groups (high vs low) with a ternary plot (`results/images/atp_share_ternary.png`) and a
    violin-plot panel (`results/images/atp_share_violins.png`). Save shares per cell to
    `results/data/atp_compartment_shares.csv`.

### Key questions (each becomes one `assets/answer/` asset)

1. **MI-ATP joint structure** — Does the 68-d substrate have a joint latent driving both MI and
   ATP-per-spike, or are MI and ATP driven by decoupled factors? Evidence: varimax factor
   correlations (joint factor with |r| > 0.3 on both MI AND ATP vs decoupled factors with |r| > 0.3
   on one only) plus the PCA colourings from Steps 1-2. State whether the MI / ATP Pareto trade-off
   observed in t0123 is the result of a single trade-off axis or multiple competing axes.

2. **Electrophys signature of high-MI vs low-MI cells** — Which channel densities, axial
   resistance, synapse densities, or other electrophys parameters most distinguish high-MI from
   low-MI cells? Evidence: Cliff's delta ranked bar chart, per-cluster mean MI table, and
   electrophys-KMeans cluster purity by MI-quartile group. State the top-5 parameters by |Cliff's
   delta| with effect sizes and directions.

3. **Morphology signature of low-ATP vs high-ATP cells** — Which morphology parameters most
   distinguish low-ATP-per-spike cells from high-ATP-per-spike cells? Evidence: Cliff's delta ranked
   bar chart restricted to the 14 morphology parameters, morphology-KMeans cluster purity by
   ATP-quartile group, and the ATP compartment breakdown (does the low-ATP group spend relatively
   more ATP at the AIS and less in the dendrites?). State the top-5 morphology parameters by
   |Cliff's delta| with effect sizes and directions.

4. **Pareto-favoured corner signature** — Which combination of electrophys and morphology
   parameters distinguishes the high-MI / low-ATP corner (Pareto-favoured) from the low-MI /
   high-ATP corner (dominated)? Evidence: 2 x 2 corner heatmap (Step 9) and per-corner morphology
   gallery. State the 5 parameters with the largest absolute z-score difference between the two
   corners, the per-corner cell counts, and the per-corner mean (MI, ATP, DSI, PD-rate).

## Approach

* Re-use every code module from `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/` as
  the structural template (loader, PCA, KMeans + silhouette sweep, varimax FA + Kaiser cap, NEURON
  pt3d morphology rendering, cluster representative selection rule). Per the cross-task import rule
  (CLAUDE.md rule 3), code is **copied into this task's `code/` directory** rather than imported.
  Adapt the loader to read the single t0123 predictions asset rather than four per-seed prediction
  files, and replace the cohort filter with the dual full / spiking cohort definition above.
* Reuse `ALL_PARAM_NAMES` (68 entries) from t0108's `code/constants.py` by copying the constant into
  this task's `code/constants.py`.
* The standardiser, PCA, KMeans, and FA must all be fit on the full-cohort union pool. Group
  comparisons in Steps 8-10 use the spiking cohort but project onto the full-cohort PCA fits.
* `data/t0123_cells.parquet` (~5.7k rows, dedup-unique full cohort) and
  `data/t0123_spiking_cells.parquet` (spiking cohort subset) are persisted for downstream
  reproducibility. Gen-0 cells (`generation == 1`, n=96) saved to `data/t0123_gen0.parquet`.
* Mann-Whitney U via `scipy.stats.mannwhitneyu(alternative="two-sided")`. Cliff's delta via the
  standard rank-based formula (no third-party dependency needed; implement in
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
* `electrophys_cluster_<k>_morphs.png` (one per ephys cluster) -- 5x3 morphology gallery per ephys
  cluster, full dendrite trees, ranked by bits-per-ATP within cluster
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
* `electrophys_clusters.csv`, `morphology_clusters.csv` -- per-cell cluster membership + summary
  stats
* `morphology_cluster_<k>_representatives.csv` (one per morph cluster)
* `cluster_group_purity.csv` -- contingency table + NMI of KMeans clusters vs MI / ATP quartile
  groups
* `factor_correlations.csv` -- Pearson r of each varimax factor vs MI / ATP / DSI / PD
* `factor_loadings.csv` -- 68-row varimax loadings matrix
* `group_comparison.csv` -- per-parameter mean / std / U-p / Cliff's delta for high vs low MI and
  high vs low ATP
* `corner_param_means.csv` -- 68 x 4 z-scored parameter means by MI x ATP corner
* `atp_compartment_shares.csv` -- per-cell soma / AIS / dendrite ATP shares
* `methodology_notes.md` -- choices, deviations from t0117, threshold rationale

### Results documents

* `results/results_summary.md` -- 2-3 sentence headline + key numbers
* `results/results_detailed.md` -- full results with all charts embedded via
  `![desc](images/filename.png)` syntax; per-section commentary; per-question verdict
* `results/compare_literature.md` -- one comparison row vs t0117's joint-factor finding
  (truncated-cohort artefact confirmed in t0117 for DSI x PD; does an equivalent finding hold for MI
  x ATP?)

## Compute and Budget

CPU-only. No remote machines. ~30-60 minutes wall-clock (KMeans + silhouette on ~5.7k cells
dominates). $0 paid services. No new dependencies beyond what t0117 already uses (`scikit-learn`,
`pandas`, `numpy`, `scipy`, `matplotlib`, `neuron` for pt3d morphology rendering).

## Cross-References

* **Methodology precedent**: t0117 (no-filter cohort across 4 seeds, DSI x PD axes), t0116 (strict
  cohort across 4 seeds, DSI x PD axes), t0108 (original strict-cohort version on t0106 seed 44).
  Every code module is reused as a structural template, with the loader and cohort-filter modules
  rewritten for the t0123 single-seed source.
* **Source data**: t0123 (NSGA-II MI vs ATP-per-spike, seed 441, 5760 cells, 10 Pareto).
* **Related open suggestions**: none of the t0123 suggestions cover this analysis directly;
  S-0123-02 (3-objective MI + DSI + ATP NSGA-II) and S-0123-03 (cell 2 deep-dive) are the closest
  downstream follow-ups and benefit from the cluster / factor structure produced here.
* **Truncated-cohort artefact context**: memory `project_truncated_cohort_artefact_confirmed.md`
  (t0117 confirmed F1 is a joint DSI-PD factor in the unfiltered pool). The MI-ATP equivalent is the
  central question of answer 1 here.
* **Methodology preferences**: memory `feedback_top50_morphologies_full_dendrites.md` (render full
  dendrite trees in morphology grids, not just somas).

## Verification Criteria

* `data/t0123_cells.parquet` row count equals the dedup-unique count logged at load time, and
  `data/t0123_spiking_cells.parquet` row count equals the cohort-filtered subset.
* `group_thresholds.json` contains numeric values for MI Q1, MI Q3, ATP Q1, ATP Q3, MI median, ATP
  median.
* Every PCA / KMeans / FA fit uses the standardiser fitted on the full-cohort union pool (not the
  spiking subset).
* Every chart referenced in `results_detailed.md` exists on disk and is embedded with markdown image
  syntax (not just listed as text).
* Every claim in each of the four answer assets is grounded in a specific table or chart in
  `results_detailed.md`. Each answer asset cites the specific row/column of `group_comparison.csv`
  or `factor_correlations.csv` underpinning its verdict.
* Headline numbers (joint-factor count, per-question top-5 parameters with effect sizes, per-corner
  cell counts) must be reported even if they are negative (no result-suppression).
* `compare_literature.md` includes a one-row comparison of the MI-ATP joint factor result vs t0117's
  DSI-PD joint factor finding.
