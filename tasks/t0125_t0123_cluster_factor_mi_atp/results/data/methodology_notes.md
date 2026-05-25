# Methodology Notes: t0125 vs t0117

This document records the deltas between t0125 and the t0117 / t0108 / t0116 cluster-and-factor
template that t0125 inherits.

## Source data

* **t0117**: pooled four NSGA-II seeds (44, 77, 7755, 9354) optimising direction selectivity +
  preferred-direction firing rate. Two source formats (JSONL.gz and JSON.gz `{evaluations: [...]}`).
* **t0125**: single t0123 NSGA-II run (seed 441) optimising `mi_count_bits` against
  `atp_per_spike_molecules`. Only the `predictions.jsonl.gz` branch is needed.

## Two-cohort design

* `data/t0125_cells.parquet` (full cohort, 5760 cells, post-dedup) is the **primary pool** for
  fitting the standardiser, PCA, KMeans, and factor analysis. Refitting on the spiking cohort would
  absorb cohort-specific scale into the standardiser and erase the signal the analysis is designed
  to detect.
* `data/t0125_spiking_cells.parquet` (3125 cells, `pd_rate_hz > 1.0 AND not silence_failed`) is used
  for group comparisons (REQ-14 / REQ-15), corner heatmap (REQ-16 / REQ-22), ATP compartment shares
  (REQ-17), and cluster purity (REQ-18). The denominator of `atp_per_spike_molecules` is unstable
  for near-silent cells; the spiking-cohort filter is essential for that family of analyses.

## Generation derivation

t0123 predictions records lack an explicit `generation` field. t0125 derives
`generation = cell_index // 96 + 1` (1-indexed) to match the t0117 convention that gen 1 is the
random init. The t0123 NSGA-II pop_size is 96 and the run is 60 generations, giving
`5760 == 96 * 60` cells total. Gen-0 (generation == 1) contains exactly 96 records, as expected.

## Field-name compatibility

The t0123 predictions asset description (`details.json` `prediction_schema`) documents
`silence_failed_bool` but actual records carry the field as `silence_failed`. The loader accepts
either, preferring `silence_failed` (the value observed in the file).

## Ranking-metric changes

t0117's `render_electrophys_cluster_morphs` ranked representatives by `dsi_vector_sum * pd_rate_hz`
(the t0117 problem statement). t0125 ranks by `mi_count_bits / atp_per_spike_molecules`
(bits-per-ATP), restricted to the spiking cohort. The same metric is used to populate the
`morphology_cluster_<k>_representatives.csv` tables.

## Correlation table extension

t0117's factor-analysis correlation table reported Pearson r and p vs two metrics (`dsi_vector_sum`,
`pd_rate_hz`). t0125 extends this to four metrics (`mi_count_bits`, `atp_per_spike_molecules`,
`dsi_vector_sum`, `pd_rate_hz`) and adds two classification columns:

* `joint_mi_atp_flag = (|r_mi| > 0.30 AND |r_atp| > 0.30)`
* `factor_classification`: one of `joint_mi_atp_dsi`, `joint_mi_atp_pd`, `joint_mi_atp`,
  `joint_dsi_pd`, `mi_only`, `atp_only`, `dsi_only`, `pd_only`, `none`.

## Cluster-purity reference change

t0117's `cluster_seed_purity` measured NMI of KMeans cluster labels against the seed (cells' source
NSGA-II seed). t0125 replaces this with `cluster_group_purity`, which measures NMI of cluster labels
against MI-quartile and ATP-quartile group labels (high / mid / low, 3125 spiking-cohort cells).
Four (partition, reference) pairs are reported:

* `(electrophys_cluster, MI_quartile_group)`
* `(electrophys_cluster, ATP_quartile_group)`
* `(morphology_cluster, MI_quartile_group)`
* `(morphology_cluster, ATP_quartile_group)`

## Inherited verbatim

* `K_SWEEP = (3, 4, 5, 6, 7)` for both KMeans sweeps.
* `KAISER_FACTOR_CAP = 10`.
* `DEDUP_DECIMALS = 6`.
* `JOINT_FACTOR_R_THRESHOLD = 0.30`.
* Varimax rotation: `gamma = 1.0`, `tol = 1e-6`, `max_iter = 500`, iterative-SVD helper.
* Random states: `KMEANS_RANDOM_STATE = 42`, `FactorAnalysis(random_state=42)`.
* Standardiser fitted ONCE on the full cohort; zero-std columns clipped to 1.0.
* Morphology rendering: full dendrite trees via NEURON pt3d (`h.x3d / y3d / diam3d`);
  `morph_seed % (2**31 - 1)` coercion; `h.delete_section(sec=s)` cleanup after every cell.

## `metrics.json` rationale

`results/metrics.json` is the empty object `{}`. None of the four registered project metrics
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) applies to this task: t0125 neither runs a tuning-curve simulation nor produces
a new DSI estimate. The headline numbers (joint-factor count, per-question top-5 parameters with
Cliff's delta, per-corner cell counts and means) live in `results/data/*.csv` files and are cited by
the four answer assets.

## Headline findings (preview)

* Loader gates pass: `raw_count == 5760`, `dedup_unique_count == 5760` (every t0123 cell is unique
  in the 68-d vector at 6-decimal rounding), `spiking_cohort_count == 3125`.
* Group thresholds (spiking cohort): `mi_q1 = 0.0` (a quarter of spiking cells fired but conveyed
  zero direction information), `mi_median = 0.565`, `mi_q3 = 0.964`. ATP per spike:
  `atp_q1 = 5.30e6`, `atp_median = 6.55e6`, `atp_q3 = 1.24e7`.
* Corner counts (median splits, spiking cohort): `high_mi_low_atp = 1221`, `high_mi_high_atp = 343`,
  `low_mi_low_atp = 341`, `low_mi_high_atp = 1220`. The diagonal imbalance
  (`high_mi_low_atp + low_mi_high_atp = 2441` vs the off-diagonal 684) is the joint Pareto
  signature.
* Factor analysis: 16 Kaiser eigenvalues > 1, capped to 10 factors; total variance explained =
  0.343. **No factor has |r_MI| > 0.30 AND |r_ATP| > 0.30** simultaneously
  (`joint_mi_atp_flag = False` for every factor). The largest joint loading is F1 with
  `r_MI = -0.358, r_ATP = +0.205` and F2 with `r_MI = +0.463, r_ATP = +0.063`. Compared to t0117
  (which found one joint DSI x PD factor F1: `r_DSI = +0.421, r_PD = +0.352, 12.6% variance`), the
  MI x ATP axes in t0123's substrate are **decoupled** at the chosen threshold.
* KMeans: electrophys headline `k = 4` (silhouette 0.0834, well-separated), morphology headline
  `k = 5` (silhouette 0.1576).
* ATP compartment shares (spiking cohort means): **soma 76.7%, dendrites 17.8%, AIS 5.5%**. This
  inverts the canonical Attwell-Laughlin cortical breakdown (axon 82%, dendrites 14%, soma 4%) —
  the t0125 model concentrates AP energy in the soma, not the axon.

## Reading order

1. `pool_counts.csv`, `group_thresholds.json`
2. `pca_combined_color_{mi,atp,corner}.png`, `pca_with_gen0_overlay.png`, `gen0_displacement.csv`
3. `electrophys_silhouette.png`, `morphology_silhouette.png`, `electrophys_clusters.csv`,
   `morphology_clusters.csv`, `electrophys_cluster_{0..3}_morphs.png`,
   `morphology_cluster_{0..4}_representatives.csv`
4. `factor_correlations.csv`, `factor_loadings.csv`, `factor_loadings_heatmap.png`
5. `group_comparison.csv`, `cliffs_delta_high_vs_low_{mi,atp}.png`
6. `corner_param_means.csv`, `corner_param_heatmap.png`
7. `atp_compartment_shares.csv`, `atp_share_{ternary,violins}.png`
8. `cluster_group_purity.csv`
9. The four answer assets under `assets/answer/`
