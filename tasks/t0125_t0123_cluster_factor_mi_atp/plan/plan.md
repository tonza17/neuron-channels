---
spec_version: "2"
task_id: "t0125_t0123_cluster_factor_mi_atp"
date_completed: "2026-05-25"
status: "complete"
---
# Plan -- Cluster + Factor Analysis of t0123 Cells (MI vs ATP-per-Spike)

## Objective

Apply the canonical t0108 / t0116 / t0117 cluster-and-factor pipeline (PCA + KMeans on 54-d
electrophys and 14-d morphology subspaces + Kaiser-cap varimax factor analysis on the full 68-d
vector) to the t0123 single-seed (seed 441) NSGA-II output of 5760 evaluated cells optimising
spike-count mutual information `mi_count_bits` against ATP-per-spike `atp_per_spike_molecules`,
producing four answer assets that dissect the substrate structure around these two new objectives:

* `mi-atp-joint-structure-in-t0123-substrate` -- does the 68-d substrate have a joint MI x ATP
  latent factor or are the two objectives driven by decoupled factors?
* `high-vs-low-mi-electrophys-signature` -- which electrophys parameters distinguish high-MI from
  low-MI cells?
* `low-vs-high-atp-morphology-signature` -- which morphology parameters distinguish low-ATP from
  high-ATP cells?
* `pareto-favoured-corner-signature` -- which combination of electrophys + morphology parameters
  distinguishes the high-MI / low-ATP corner from the low-MI / high-ATP corner?

**Definition of "done"**: all four answer assets exist under `assets/answer/`, every chart and table
listed in `## Expected Assets` is produced, `verify_answer_asset` passes on each answer,
`verify_plan` passes with zero errors, and every claim in each answer cites a specific row/column of
`results/data/group_comparison.csv` or `results/data/factor_correlations.csv` or a specific PNG.

* * *

## Task Requirement Checklist

The operative task text from `tasks/t0125_t0123_cluster_factor_mi_atp/task_description.md` (verbatim
quote of the binding sections):

```text
Pool definition
* Load every record from the predictions asset.
* Deduplicate by the 68-d vector rounded to 6 decimals (DEDUP_DECIMALS = 6).
* Record raw count, dedup-unique count, and post-filter counts before any analysis.

Cohort filter
1. Full cohort -- every dedup-unique cell. Primary pool for PCA, KMeans, and factor analysis.
2. Spiking cohort -- cells with pd_rate_hz > 1.0 Hz AND silence_failed_bool == False.

Group definitions (spiking cohort):
* MI groups: top quartile by mi_count_bits = "high MI"; bottom quartile = "low MI".
* ATP groups: top quartile by atp_per_spike_molecules = "high ATP"; bottom quartile = "low ATP".
* MI x ATP corners: four 2x2 quadrants formed by the median split on each axis.

Analyses to run:
1. Combined 68-d PCA + side panels (one figure, three subplots), coloured by mi_count_bits.
2. Same three-panel figure coloured by atp_per_spike_molecules (log10).
3. Same three-panel figure coloured by MI x ATP corner.
4. Gen-0 (generation == 1) random-init overlay; mean and 95th-percentile Euclidean displacement.
5. KMeans on 54-d electrophys subspace, auto-pick k in [3, 7] by silhouette. 5x3 morphology grid
   of 15 representatives per cluster, ranked by mi_count_bits / atp_per_spike_molecules.
6. KMeans on 14-d morphology subspace, auto-pick k in [3, 7] by silhouette. 15-row representative
   table with (generation, cell_index, mi, atp, dsi, pd, ephys_PC1/2/3, soma_share_atp).
7. Factor analysis on the full 68-d feature matrix, Kaiser criterion, varimax-rotated. Cap at 10.
   Report Pearson r vs mi_count_bits AND atp_per_spike_molecules AND dsi_vector_sum AND pd_rate_hz.
   Identify joint factors (|r| > 0.3 on both MI AND ATP) and decoupled factors.
8. High vs low group comparison (electrophys + morphology): mean/std, Mann-Whitney U p-value,
   Cliff's delta. Ranked bar charts (top-20 by |delta|) for MI and ATP.
9. 2x2 corner heatmap: 68 parameters z-scored on the full cohort, mean per MI x ATP corner.
10. ATP compartment breakdown (soma/AIS/dendrites_total shares): ternary plot + violin panel.

Key questions (each becomes one assets/answer/ asset):
1. MI-ATP joint structure
2. Electrophys signature of high-MI vs low-MI cells
3. Morphology signature of low-ATP vs high-ATP cells
4. Pareto-favoured corner signature
```

Concrete requirements extracted from the task text. Each `REQ-*` lists the step(s) in
`## Step by Step` that satisfy it and the evidence that proves completion.

* **REQ-1: Load all 5760 records from the t0123 predictions asset.** Source path:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`.
  Satisfied by Step 2 (loader). Evidence: `results/data/pool_counts.csv` row `raw_count == 5760`.

* **REQ-2: Deduplicate by the 68-d vector rounded to 6 decimals.** `DEDUP_DECIMALS = 6` constant.
  Satisfied by Step 2. Evidence: `results/data/pool_counts.csv` row
  `dedup_unique_count >= 0.10 * raw_count`.

* **REQ-3: Build full cohort and spiking cohort and persist both.** Full = dedup-unique; Spiking =
  `pd_rate_hz > 1.0 AND silence_failed_bool == False`. Satisfied by Step 2. Evidence:
  `data/t0123_cells.parquet`, `data/t0123_spiking_cells.parquet`, both row counts logged in
  `results/data/pool_counts.csv`.

* **REQ-4: Compute MI and ATP quartile thresholds and median splits.** Satisfied by Step 3.
  Evidence: `results/data/group_thresholds.json` contains numeric values for `mi_q1`, `mi_q3`,
  `mi_median`, `atp_q1`, `atp_q3`, `atp_median`.

* **REQ-5: Fit standardiser once on the full cohort union pool.** Satisfied by Step 4. Evidence:
  `data/t0123_standardiser.npz` exists.

* **REQ-6: Three-panel PCA figure coloured by MI.** Satisfied by Step 5. Evidence:
  `results/images/pca_combined_color_mi.png`.

* **REQ-7: Three-panel PCA figure coloured by ATP (log10).** Satisfied by Step 5. Evidence:
  `results/images/pca_combined_color_atp.png`.

* **REQ-8: Three-panel PCA figure coloured by MI x ATP corner.** Satisfied by Step 5. Evidence:
  `results/images/pca_combined_color_corner.png`.

* **REQ-9: Gen-0 overlay PCA plot.** Project the 96 `generation == 1` individuals onto the fitted
  full-cohort PCA. Satisfied by Step 6. Evidence: `results/images/pca_with_gen0_overlay.png` and
  `results/data/gen0_displacement.csv` (mean + p95 displacement overall and per corner).

* **REQ-10: KMeans on the 54-d electrophys subspace with silhouette auto-pick over k in [3, 7].**
  Satisfied by Step 7. Evidence: `results/images/electrophys_silhouette.png`,
  `results/data/electrophys_clusters.csv` with per-cluster mean MI / ATP / DSI / PD / firing_hz.

* **REQ-11: 5x3 morphology gallery per electrophys cluster (full dendrite trees), representatives
  ranked by bits-per-ATP within cluster (spiking cohort).** Satisfied by Step 8. Evidence: one PNG
  per cluster `results/images/electrophys_cluster_<k>_morphs.png`.

* **REQ-12: KMeans on the 14-d morphology subspace with silhouette auto-pick over k in [3, 7].**
  Satisfied by Step 9. Evidence: `results/images/morphology_silhouette.png`,
  `results/data/morphology_clusters.csv`, plus one per-cluster representatives table
  `results/data/morphology_cluster_<k>_representatives.csv`.

* **REQ-13: Factor analysis (Kaiser criterion, varimax-rotated, cap 10) with Pearson r vs MI, ATP,
  DSI, PD.** Satisfied by Step 10. Evidence: `results/images/factor_loadings_heatmap.png`,
  `results/data/factor_loadings.csv`, `results/data/factor_correlations.csv` with one row per factor
  and a `joint_mi_atp_flag` column.

* **REQ-14: High vs low group comparison for all 68 parameters with mean / std / Mann-Whitney U
  p-value / Cliff's delta.** Satisfied by Step 11. Evidence: `results/data/group_comparison.csv`.

* **REQ-15: Cliff's-delta ranked bar charts (top-20) for MI and ATP groups.** Satisfied by Step 11.
  Evidence: `results/images/cliffs_delta_high_vs_low_mi.png`,
  `results/images/cliffs_delta_high_vs_low_atp.png`.

* **REQ-16: 68 x 4 corner heatmap of z-scored parameter means by MI x ATP corner.** Satisfied by
  Step 12. Evidence: `results/images/corner_param_heatmap.png`,
  `results/data/corner_param_means.csv`.

* **REQ-17: ATP compartment shares (soma / AIS / dendrites) per cell + ternary + violins.**
  Satisfied by Step 13. Evidence: `results/data/atp_compartment_shares.csv`,
  `results/images/atp_share_ternary.png`, `results/images/atp_share_violins.png`.

* **REQ-18: Cluster purity tables vs MI quartile groups and ATP quartile groups (NMI +
  chi-square).** Satisfied by Step 14. Evidence: `results/data/cluster_group_purity.csv` with one
  row per (partition, reference) pair, NMI and chi-square p-value columns.

* **REQ-19: Methodology notes document recording choices, deviations from t0117, and threshold
  rationale.** Satisfied by Step 15. Evidence: `results/data/methodology_notes.md`.

* **REQ-20: Four answer assets, one per question, each citing the specific table / chart that
  underpins its verdict.** Satisfied by Step 16. Evidence: four folders under `assets/answer/`, each
  passing `verify_answer_asset`.

* **REQ-21: Top-5 parameters per question with effect size and direction.** Specifically asked in
  the long description for answers 2, 3, and 4. Satisfied by Step 16 (the answer-writing step
  consumes `group_comparison.csv` and `corner_param_means.csv` directly). Evidence: each answer's
  full document includes a top-5 table.

* **REQ-22: Per-corner cell counts and per-corner mean (MI, ATP, DSI, PD-rate) for answer 4.**
  Satisfied by Step 12 (corner aggregation) and Step 16 (answer writing). Evidence:
  `results/data/corner_param_means.csv` `cell_count` row + answer 4 full document.

* * *

## Approach

### Task Type Classification

`task.json` declares `task_types: ["data-analysis", "comparative-analysis", "answer-question"]`. All
three types apply and contribute concrete planning guidance:

* `data-analysis` (instruction.md): produce structured `results/metrics.json`, save intermediate
  data as CSV / JSON not just charts, use matplotlib + seaborn, explicit dtypes on pandas reads,
  every chart titled + axis-labelled. Influence: every analysis step has explicit table output and
  every chart has an explicit title and axis labels.
* `comparative-analysis` (instruction.md): define comparison dimensions upfront (here: MI quartile,
  ATP quartile, MI x ATP corner); statistical significance tests planned upfront (here: Mann-
  Whitney U + Cliff's delta + chi-square); pareto / multi-dim visualisations (here: corner heatmap
  + ternary plot). Influence: REQ-14, REQ-15, REQ-16, REQ-18 explicitly call out the comparison
    dimensions and statistical tests.
* `answer-question` (instruction.md): one answer asset per question with stable `answer_id`, short
  answer 2-5 sentences, full answer as mini-paper, no inline citations in short answers. Influence:
  REQ-20 lists the four `answer_id` slugs explicitly so each answer asset is reserved before Step
  16\.

### Substrate Geometry Prior (from research/research_papers.md)

The 68-d substrate is expected to form a "collection of loosely connected hyperplanes" rather than a
single blob or set of isolated points -- the canonical [Achard2006] finding from 20 acceptable
Purkinje cell models. The varimax factor analysis is the right tool for this geometry because it
reads off which combinations of channels co-vary along the manifold. The empirical backup at network
scale comes from [Prinz2004]: 20.25 M brute-force STG networks, 2.2% match all 15 criteria, every
channel combination represented in the matching set. [Marder2006] gives the canonical review framing
of parameter degeneracy: channel densities can vary two- to fourfold across cells of the same type
while activity profiles remain conserved because compensating channels co-vary. Expectation: the
68-d t0123 substrate admits a small number (3-10) of varimax factors capturing substantial variance;
per-factor variance of 10-15% is normal for MOO output ensembles.

### Joint vs Decoupled Factor Hypothesis

The central question of answer 1 mirrors the t0117 truncated-cohort artefact finding: t0117 found
one joint DSI x PD factor F1 (r_DSI = +0.421, r_PD = +0.352, 12.6% variance) in the unfiltered
4-seed pool but zero joint factors in the strict-cohort version (t0116, DSI > 0.7 AND PD > 10). The
t0125 question is whether the analogous joint factor exists for MI x ATP in the t0123 unfiltered
full cohort. The threshold for "joint" is the t0117-inherited `|r| > 0.30` on both metrics
simultaneously.

### ATP-per-Spike Mechanism Prior (from research/research_papers.md)

The ATP-per-spike axis is driven by Na+/K+ overlap during the AP, not by AP shape (Sengupta2010, R^2
= 0.99 between total Na+ load and overlap load; 1.76-fold ATP differences at identical waveform).
Mammalian neurons cluster at alpha = total/capacitive-min Na+ load in `[1.0, 1.5]` vs squid at
`[4, 11]`. The expected "energy levers" in the Cliff's delta top-5 for ATP (REQ-15) are Nav
densities (`g_nav16_*`), Kv densities (`g_kv3_*`, `g_kv4_*`), and Na+ inactivation kinetics. The
Attwell-Laughlin canonical compartment breakdown (axon 82%, dendrites 14%, soma 4%) supplies the
cortical reference against which the t0125 ATP-share ternary will be compared in the answer-3
document.

### MI Ceiling Prior (from research/research_papers.md)

t0123 hit `best mi_count_bits = 1.459`, i.e. 73% of the `log2(4) = 2 bits/stimulus` ceiling.
[Strong1998] and [Dhingra2004] establish that any reported information rate must specify the
resolution, window, number of trials, bias-correction method, and units. The t0125 cluster analysis
consumes `mi_count_bits` as the bits/stimulus surrogate; absolute MI claims defer to the post-hoc
8-direction x 20-trial Strong-Bialek validation in the t0123 predictions asset (top-10 Pareto cells
only). All MI charts in this task must annotate the `log2(4) = 2 bits` ceiling in their captions,
and the answer-1 document must note that the 10 t0123 top-Pareto cells reported `bits_per_sec = 0.0`
under Strong-Bialek because PD-rate was too low (~3 spikes per 1400-ms trial).

### Code Reuse Strategy (from research/research_code.md)

The cross-task import rule (CLAUDE.md rule 3) forbids importing from another task's `code/`
directory. The t0117 module set (15 source files, ~2374 lines) is the most direct structural
template; modules are **copied** verbatim or with minor adaptation into `code/`:

* `paths.py` (63 lines) -- copy + path renames (`pooled_*` -> `t0123_*`); add t0125-new output paths
  (`pca_combined_color_mi.png`, `corner_param_heatmap.png`, `atp_share_ternary.png`, etc.).
* `constants.py` (110 lines, from t0108) -- copy `ALL_PARAM_NAMES`, `ELECTROPHYS_PARAM_NAMES` (54),
  `MORPHOLOGY_PARAM_NAMES` (14), `N_*_DIMS`; strip `DSI_THRESHOLD` / `PD_THRESHOLD_HZ` /
  `SOURCE_TASK` / `SOURCE_SEED`; add `SPIKING_PD_RATE_HZ_THRESHOLD = 1.0`,
  `MI_QUARTILE_TOP_QUANTILE = 0.75`, `MI_QUARTILE_BOTTOM_QUANTILE = 0.25`,
  `CLIFFS_DELTA_TOP_N = 20`, `JOINT_FACTOR_R_THRESHOLD = 0.30`, `DEDUP_DECIMALS = 6`,
  `KAISER_FACTOR_CAP = 10`, `K_SWEEP = (3, 4, 5, 6, 7)`, `KMEANS_RANDOM_STATE = 42`,
  `N_INIT_KMEANS = 10`, `T0123_PREDICTIONS_REL_PATH = Path(...)`.
* `cluster_helpers.py` (170 lines) -- copy verbatim (only namespace update). Provides
  `PooledStandardiser`, `fit_pooled_standardiser`, `save_standardiser`, `load_standardiser`,
  `zscore_matrix`, `run_pca`, `run_kmeans_sweep`, `top_k_loadings`, `write_json`,
  `PCAResult / KMeansResult / KMeansSweepResult` dataclasses. Zero-std columns clipped to 1.0.
* `load_pooled_cells.py` -> `load_t0123_cells.py` (254 lines, **major adaptation**) -- drop
  `SOURCES` tuple and per-seed loop; read only the single `.jsonl.gz` source; keep only the JSONL
  branch of `_iter_records`; promote `mi_count_bits`, `atp_per_spike_molecules`,
  `silence_failed_bool`, plus the three breakdown sub-keys (`atp_soma`, `atp_ais`,
  `atp_dendrites_total`) to top-level DataFrame columns; persist two parquets
  (`data/t0123_cells.parquet`, `data/t0123_spiking_cells.parquet`); write
  `results/data/pool_counts.csv` and `results/data/group_thresholds.json`.
* `load_pooled_gen0.py` -> `load_t0123_gen0.py` (126 lines, minor adaptation) -- read t0123
  predictions, keep `generation == 1` (96 expected), persist `data/t0123_gen0.parquet`.
* `fit_standardiser.py` (57 lines) -- copy + rename. Fit standardiser on `data/t0123_cells.parquet`
  (full cohort), save to `data/t0123_standardiser.npz`.
* `pooled_pca_with_overlay.py` -> `pca_with_overlay.py` (379 lines, **major adaptation**) --
  restructure into three figures: MI / ATP-log10 / corner-categorical. Replace
  `_scatter_cells_by_seed` with `_scatter_cells_by_value` (continuous viridis) and
  `_scatter_cells_by_corner` (categorical tab10, 4 colours). Gen-0 overlay
  (`pca_with_gen0_overlay.png`) and `gen0_displacement.csv` segmented per MI x ATP corner instead of
  per seed.
* `factor_analysis.py` (262 lines, minor adaptation) -- copy verbatim including the in-house
  `varimax_rotation` iterative-SVD helper (gamma = 1.0, tol = 1e-6, max_iter = 500), `FactorResult`,
  `_drop_constant_columns`, `_plot_loadings_heatmap` with `RdBu_r` symmetric colourmap. Extend the
  correlation table to four outcome metrics (MI, ATP, DSI, PD) instead of two. Add
  `joint_mi_atp_flag` and `factor_classification` columns.
* `cluster_electrophys.py` (159 lines, minor adaptation) -- KMeans on 54-d submatrix, silhouette
  auto-pick over `K_SWEEP`. Add per-cluster mean MI / ATP / DSI / PD / firing_hz to output CSV.
* `cluster_morphology.py` (195 lines, minor adaptation) -- KMeans on 14-d submatrix. 15-row
  representative table now needs
  `(generation, cell_index, mi_count_bits, atp_per_spike_molecules, dsi_vector_sum, pd_rate_hz, ephys_PC1, ephys_PC2, ephys_PC3, soma_share_atp)`.
  Compute `soma_share_atp = atp_soma / (atp_soma + atp_ais + atp_dendrites_total)`.
* `morphology_rendering.py` (178 lines) -- copy verbatim (only namespace update). NEURON pt3d
  helpers; full dendrite trees per `feedback_top50_morphologies_full_dendrites.md` memory;
  `MAX_MORPH_SEED = 2**31 - 1` modulo and `h.delete_section` cleanup mandatory.
* `render_electrophys_cluster_morphs.py` (220 lines, minor adaptation) -- 5 x 3 grid preserved.
  Within-cluster ranking metric changes from `DSI * PD` (t0117) to
  `mi_count_bits / atp_per_spike_molecules` (bits-per-ATP) restricted to the spiking cohort.
* `cluster_seed_purity.py` -> `cluster_group_purity.py` (85 lines, heavy adaptation) -- replace
  `(cluster, seed)` with `(cluster, MI_quartile_group)` and `(cluster, ATP_quartile_group)`. NMI +
  chi-square reporting structure preserved.
* `methodology_and_comparison.py` (267 lines) -- structural template only; this task does not itself
  write `compare_literature.md` (that is an orchestrator step), but the module is the reference
  layout for the `methodology_notes.md` data file (REQ-19).

The two morphology libraries are project-registered and **imported directly** via library:

* `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams`
* `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`

Four new modules with no precedent:

* `code/effect_sizes.py` (~30 lines) -- `cliffs_delta(x, y) -> float` using ties-aware rank formula
  `delta = (#x>y - #x<y) / (n_x * n_y)`.
* `code/group_comparison.py` (~150 lines) -- 68 parameters x 4 group definitions (high MI, low MI,
  high ATP, low ATP). Per-parameter mean / std / Mann-Whitney U p-value / Cliff's delta. Top-20
  ranked bar charts.
* `code/corner_heatmap.py` (~100 lines) -- 68 x 4 z-scored corner-mean matrix.
  `results/images/corner_param_heatmap.png` with `RdBu_r` symmetric colourmap.
* `code/atp_compartment_shares.py` (~200 lines) -- per-cell soma / AIS / dendrite shares; ternary
  plot via `mpltern` if available, hand-rolled barycentric scatter as fallback; 6-panel violin plot.

### Two-Cohort Discipline

The standardiser, PCA, KMeans, and FA are all fit on the **full** cohort. Group comparisons (REQ-14,
REQ-15) and the corner aggregations (REQ-16) and the ATP compartment shares (REQ-17) use the
**spiking** cohort but project onto the full-cohort PCA / standardiser. Refitting on the spiking
cohort would absorb cohort-specific scale into the standardiser and erase the very signal the
analysis is designed to detect (the t0117 module docstring documents this risk explicitly).

### Alternatives Considered

* **Alternative 1 -- single combined cohort with no filter.** Rejected because ATP-per-spike has a
  denominator approaching zero for near-silent cells (low `pd_rate_hz`), producing extreme
  `atp_per_spike_molecules` values that would dominate the quartile thresholds and contaminate the
  group comparisons. The dual-cohort design isolates the substrate-structure analyses (full cohort,
  where every cell informs the standardiser and PCA) from the ATP-per-spike comparisons (spiking
  cohort, where the denominator is stable).
* **Alternative 2 -- separate KMeans on the joint 68-d vector instead of separate electrophys-only
  and morphology-only KMeans.** Rejected per [Baden2016] best practice (precedent for unsupervised
  clustering of high-d cell-type fingerprints): clustering on function-relevant subspaces separately
  yields more interpretable cluster identities. The t0117 / t0108 / t0116 precedents all do separate
  KMeans for the same reason.
* **Alternative 3 -- BIC-based mixture model in place of KMeans + silhouette.** Rejected for
  consistency with the t0117 / t0108 / t0116 precedents (silhouette over
  `K_SWEEP = (3, 4, 5, 6, 7)`). BIC and silhouette can disagree on cluster count; switching now
  would prevent direct comparison against t0117's joint-DSI-PD-factor finding (the central
  comparison for the compare-literature step). [Baden2016]'s BIC parallel is documented in the
  methodology notes but not adopted as the primary criterion.
* **Alternative 4 -- third-party Cliff's delta package.** Rejected because the formula is ~30 lines
  including ties handling; adding a dependency for a one-line wrapper is not worth the
  pyproject.toml + lockfile churn.

### Metrics Format

`results/metrics.json` will be the empty object `{}` per `metrics_specification.md` guidance and per
the t0117 precedent. None of the four registered project metrics (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) applies: this task neither
runs a tuning-curve simulation nor produces a new DSI estimate. The headline numbers (joint-factor
count, per-question top-5 parameters with Cliff's delta, per-corner cell counts and means) live in
`results/data/*.csv` and are summarised in `results_detailed.md` and the answer assets, not as
registered metrics. This omission is deliberate and documented here so it is recognised as planned
rather than accidental.

* * *

## Cost Estimation

| Item | Estimated cost (USD) |
| --- | --- |
| API calls (LLM inference, paid services) | $0.00 |
| Remote compute (GPU rental, cloud instances) | $0.00 |
| Local CPU compute (no external billing) | $0.00 |
| Data downloads (no paid datasets) | $0.00 |
| **Total** | **$0.00** |

**Reasoning**: this is a pure CPU data-analysis task. All input data is one pre-existing predictions
asset (`tasks/t0123_.../assets/predictions/.../files/predictions.jsonl.gz`, 5760 records) already on
disk. All compute is local: pandas / numpy / scikit-learn / matplotlib / NEURON pt3d rendering. No
paid third-party service is invoked. Expected wall-clock ~30-60 minutes on the local workstation,
dominated by the KMeans silhouette sweep on ~5760 cells.

**Project budget context**: total project budget = $100.00 (USD); $35.41 remaining of $100.00
available at task start; per-task default cap = $8.00. This task's $0.00 estimate is well within
both the per-task cap and the remaining project budget.

* * *

## Step by Step

### Milestone A: Set up code/ skeleton and load data

1. **[CRITICAL] Set up the `code/` directory skeleton.** Create `code/__init__.py` (empty) and copy
   the following t0117 / t0108 modules into `code/` with namespace updates from
   `tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.*` to
   `tasks.t0125_t0123_cluster_factor_mi_atp.code.*`:
   * `code/paths.py` from `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/paths.py`,
     rename `pooled_*` to `t0123_*`, add t0125-new output paths.
   * `code/constants.py` from `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py`, strip
     `DSI_THRESHOLD` / `PD_THRESHOLD_HZ` / `SOURCE_TASK` / `SOURCE_SEED`; add t0125-specific
     constants listed in `## Approach > Code Reuse Strategy`.
   * `code/cluster_helpers.py` from t0117 (verbatim, only namespace).
   * `code/fit_standardiser.py` from t0117 (rename input/output paths).
   * `code/factor_analysis.py` from t0117 (extend correlation table to 4 metrics).
   * `code/cluster_electrophys.py`, `code/cluster_morphology.py` from t0117.
   * `code/morphology_rendering.py` from t0117 (verbatim, only namespace).
   * `code/render_electrophys_cluster_morphs.py` from t0117 (ranking metric change).
   * `code/cluster_group_purity.py` from t0117's `cluster_seed_purity.py`. Expected: `ls code/`
     shows 14+ Python files including the three new modules created in later steps. Satisfies
     infrastructure for REQ-1 through REQ-22.

2. **[CRITICAL] Implement and run `code/load_t0123_cells.py`.** Copy
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/load_pooled_cells.py` as starting
   point. Drop `SOURCES` tuple and per-seed loop. Read the single
   `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`
   file. Keep only the `.jsonl.gz` branch of `_iter_records`. Promote new columns to top-level:
   `mi_count_bits`, `atp_per_spike_molecules`, `silence_failed_bool`, `atp_soma`, `atp_ais`,
   `atp_dendrites_total` (from `atp_per_ap_compartment_breakdown` dict). Apply `DEDUP_DECIMALS = 6`
   rule. Persist `data/t0123_cells.parquet` (full cohort) and `data/t0123_spiking_cells.parquet`
   (spiking subset: `pd_rate_hz > 1.0 AND silence_failed_bool == False`). Write
   `results/data/pool_counts.csv` (columns: `raw_count`, `dedup_unique_count`,
   `spiking_cohort_count`). Run via
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0125_t0123_cluster_factor_mi_atp -- uv run python -u -m tasks.t0125_t0123_cluster_factor_mi_atp.code.load_t0123_cells`.
   Expected: `raw_count == 5760`, `dedup_unique_count >= 576` (10% of raw), parquets exist.
   Satisfies REQ-1, REQ-2, REQ-3.

3. **Compute MI / ATP quartile and median thresholds.** Add a small helper (either at the bottom of
   `code/load_t0123_cells.py` or as a `code/group_thresholds.py` module) that loads
   `data/t0123_spiking_cells.parquet`, computes `mi_q1 = np.quantile(mi, 0.25)`,
   `mi_q3 = np.quantile(mi, 0.75)`, `mi_median = np.quantile(mi, 0.5)`, same for ATP, and writes
   `results/data/group_thresholds.json` as
   `{"mi_q1": ..., "mi_q3": ..., "mi_median": ..., "atp_q1": ..., "atp_q3": ..., "atp_median": ..., "spiking_cohort_count": ..., "high_mi_count": ..., "low_mi_count": ..., "high_atp_count": ..., "low_atp_count": ..., "corner_counts": {"high_mi_low_atp": ..., "high_mi_high_atp": ..., "low_mi_low_atp": ..., "low_mi_high_atp": ...}}`.
   Expected: all 6 quartile thresholds are positive floats; the four corner counts sum to the
   spiking cohort count. Satisfies REQ-4.

4. **[CRITICAL] Fit the full-cohort standardiser.** Run `code/fit_standardiser.py` -- loads
   `data/t0123_cells.parquet`, fits `PooledStandardiser` (mean and std arrays from
   `cluster_helpers.fit_pooled_standardiser`), saves to `data/t0123_standardiser.npz`. Run via
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0125_t0123_cluster_factor_mi_atp -- uv run python -u -m tasks.t0125_t0123_cluster_factor_mi_atp.code.fit_standardiser`.
   Expected: `data/t0123_standardiser.npz` exists; `mean.shape == (68,)` and `std.shape == (68,)`.
   Satisfies REQ-5.

### Milestone B: PCA + gen-0 overlay

5. **Implement and run `code/pca_with_overlay.py` -- three PCA-coloured figures.** Copy
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/pooled_pca_with_overlay.py`.
   Restructure the single-figure design into three separate output figures, each a 1 x 3 panel
   (combined / electrophys-only / morphology-only). Replace `_scatter_cells_by_seed` with two new
   helpers: `_scatter_cells_by_value(ax, x, y, value, cmap)` (continuous viridis; used for MI and
   `log10(ATP)`) and `_scatter_cells_by_corner(ax, x, y, corner_label)` (categorical tab10 over four
   corners). Compute PC1+PC2 variance explained per panel. Save:
   * `results/images/pca_combined_color_mi.png` (viridis on `mi_count_bits`).
   * `results/images/pca_combined_color_atp.png` (viridis on `log10(atp_per_spike_molecules)`).
   * `results/images/pca_combined_color_corner.png` (tab10 on corner label). Expected: three PNGs
     exist, each ~6 x 18 inches at dpi=150. Satisfies REQ-6, REQ-7, REQ-8.

6. **Run gen-0 overlay.** Add a helper in `pca_with_overlay.py` (or in `code/load_t0123_gen0.py`)
   that:
   * Loads `data/t0123_gen0.parquet` (created by `code/load_t0123_gen0.py` -- run this loader first;
     copy from t0117 `load_pooled_gen0.py`, filter to `generation == 1`, ~96 cells).
   * Projects gen-0 cells onto the full-cohort PCAs (reuse the fitted standardiser; do **not**
     refit).
   * Computes mean and 95th-percentile Euclidean displacement in PC1+PC2 space and in 68-d
     standardised space, both overall and per MI x ATP corner.
   * Renders `results/images/pca_with_gen0_overlay.png` (same three-panel layout, gen-0 cells
     overlaid in red x markers, evolved cells in light blue).
   * Writes `results/data/gen0_displacement.csv` with columns `partition` (`overall` or corner
     label), `mean_pc12_displacement`, `p95_pc12_displacement`, `mean_68d_displacement`,
     `p95_68d_displacement`. Expected: 5 rows in `gen0_displacement.csv` (overall + 4 corners), PNG
     exists. Satisfies REQ-9.

### Milestone C: KMeans cluster analyses

7. **Run `code/cluster_electrophys.py`.** Copy from t0117. Standardise the 54-d electrophys
   submatrix on the full cohort (using the saved standardiser, no refit). Run
   `run_kmeans_sweep(matrix_zscored, k_sweep=K_SWEEP)`. Pick `k` by `argmax(mean_silhouette)`. Save
   silhouette curve `results/images/electrophys_silhouette.png` (x = k, y = silhouette). Write
   `results/data/electrophys_clusters.csv` with columns
   `(generation, cell_index, cluster, mi_count_bits, atp_per_spike_molecules, dsi_vector_sum, pd_rate_hz, firing_hz_mean)`
   and a summary block of per-cluster means at the top of the file (or as a sibling
   `electrophys_cluster_summary.csv`). Expected: chosen `k in [3, 7]`, per-cluster counts > 50.
   Satisfies REQ-10.

8. **Run `code/render_electrophys_cluster_morphs.py`.** Copy from t0117. For each electrophys
   cluster, select the 15 representatives ranked by `mi_count_bits / atp_per_spike_molecules`
   (bits-per-ATP) within cluster, restricted to the spiking cohort. Render as 5 rows x 3 columns,
   one PNG per cluster: `results/images/electrophys_cluster_<k>_morphs.png`. Use full dendrite trees
   (NEURON pt3d), not just somas (per `feedback_top50_morphologies_full_dendrites.md` memory). Use
   the `procedural_dsgc_morphology_generator_fix` library (`generate_fixed_morphology` from t0092)
   and `procedural_dsgc_morphology_generator` library (`MorphologyParams` from t0090). Apply
   `morph_seed % (2**31 - 1)` and `h.delete_section` cleanup on every section. Expected: one PNG per
   electrophys cluster, each with 15 panels of full dendrite trees, axes scaled by `global_extents`
   so panels share the same scale. Satisfies REQ-11.

9. **Run `code/cluster_morphology.py`.** Copy from t0117. KMeans on the 14-d morphology submatrix
   with silhouette auto-pick over `K_SWEEP = (3, 4, 5, 6, 7)`. Save
   `results/images/morphology_silhouette.png`, `results/data/morphology_clusters.csv`. For each
   morphology cluster, write a 15-row representative table to
   `results/data/morphology_cluster_<k>_representatives.csv` with columns
   `(generation, cell_index, mi_count_bits, atp_per_spike_molecules, dsi_vector_sum, pd_rate_hz, ephys_PC1, ephys_PC2, ephys_PC3, soma_share_atp)`.
   Compute `soma_share_atp = atp_soma / (atp_soma + atp_ais + atp_dendrites_total)`. Expected:
   chosen `k in [3, 7]`, one CSV per cluster. Satisfies REQ-12.

### Milestone D: Factor analysis

10. **[CRITICAL] Run `code/factor_analysis.py`.** Copy from t0117 (which reuses t0108's in-house
    `varimax_rotation`, gamma = 1.0, tol = 1e-6, max_iter = 500, iterative-SVD). Pipeline:
    `_drop_constant_columns` removes std < 1e-8 columns; `np.linalg.eigvalsh` produces the
    correlation-matrix eigenvalues sorted descending; `n_eig_above_one = sum(eig > 1.0)`;
    `n_factors = max(1, min(n_eig_above_one, KAISER_FACTOR_CAP=10))`; fit
    `FactorAnalysis(n_components=n_factors, rotation=None, random_state=42)`; apply
    `varimax_rotation`; compute regression scores `Z @ Lambda @ pinv(Lambda.T @ Lambda)`. Compute
    Pearson r and p between each rotated factor score and each of the four outcome metrics:
    `mi_count_bits`, `atp_per_spike_molecules`, `dsi_vector_sum`, `pd_rate_hz`. Write:
    * `results/images/factor_loadings_heatmap.png` (RdBu_r symmetric vmin/vmax, height
      `0.18 * 68 + 1` inches).
    * `results/data/factor_loadings.csv` (68 rows x `n_factors` columns + parameter-name column).
    * `results/data/factor_correlations.csv` with columns
      `factor_id, variance_explained, r_mi, p_mi, r_atp, p_atp, r_dsi, p_dsi, r_pd, p_pd, joint_mi_atp_flag, factor_classification`.
      `joint_mi_atp_flag = (abs(r_mi) > 0.30 AND abs(r_atp) > 0.30)`. `factor_classification` is one
      of `joint_mi_atp`, `mi_only`, `atp_only`, `joint_mi_atp_dsi`, `joint_mi_atp_pd`,
      `joint_dsi_pd`, `dsi_only`, `pd_only`, `none`. Expected: `n_factors in [1, 10]`, all four r
      columns populated for every factor. Satisfies REQ-13.

### Milestone E: Group comparisons + corner heatmap

11. **Implement and run `code/effect_sizes.py` and `code/group_comparison.py`.**
    * `code/effect_sizes.py` (~30 lines): `cliffs_delta(x, y) -> float` using the rank-based formula
      with ties handling. Recommended: combine `x` and `y`, sort via `np.argsort`, use
      `np.searchsorted` to count exceedances in O(n log n). Add `code/test_effect_sizes.py` checking
      against a known-result example (e.g., `cliffs_delta([1, 2, 3], [4, 5, 6]) == -1.0` and
      `cliffs_delta([1, 2, 3], [1, 2, 3]) == 0.0`). Validation: run
      `uv run pytest tasks/t0125_t0123_cluster_factor_mi_atp/code/test_effect_sizes.py -v` and
      confirm 0 failures.
    * `code/group_comparison.py` (~150 lines): for each of the 68 parameters, compute mean and std
      on the spiking cohort for the high-MI, low-MI, high-ATP, low-ATP groups; compute
      `scipy.stats.mannwhitneyu(alternative="two-sided")` p-values for high-MI vs low-MI and
      high-ATP vs low-ATP; compute `cliffs_delta` for the same two pairs. Save to
      `results/data/group_comparison.csv` with columns
      `parameter, mean_high_mi, std_high_mi, mean_low_mi, std_low_mi, mwu_p_mi, cliffs_delta_mi, mean_high_atp, std_high_atp, mean_low_atp, std_low_atp, mwu_p_atp, cliffs_delta_atp`.
      Render two top-20 ranked bar charts of `|cliffs_delta|`:
      `results/images/cliffs_delta_high_vs_low_mi.png` and
      `results/images/cliffs_delta_high_vs_low_atp.png`. Bars annotated with the parameter name on
      the y-axis and the signed delta value on the bar. Expected: CSV has 68 rows, two PNGs exist
      with 20 bars each. Satisfies REQ-14, REQ-15.

12. **Implement and run `code/corner_heatmap.py`.** For the 68 parameters, on the spiking cohort,
    z-score using the full-cohort standardiser, then compute the mean z-score in each of the four MI
    x ATP corners (defined by the median split on each axis). Render the 68 x 4 matrix as a `RdBu_r`
    symmetric-vmin/vmax heatmap: `results/images/corner_param_heatmap.png` with parameter names on
    the y-axis and corner labels on the x-axis. Save the underlying matrix to
    `results/data/corner_param_means.csv` with columns
    `(parameter, high_mi_low_atp, high_mi_high_atp, low_mi_low_atp, low_mi_high_atp)`. Add a summary
    footer block with per-corner cell counts and per-corner mean of MI, ATP, `dsi_vector_sum`,
    `pd_rate_hz`. Expected: 68 rows in CSV + 1 footer row (or sibling file), PNG exists. Satisfies
    REQ-16, REQ-22.

### Milestone F: ATP compartment shares + cluster purity + methodology notes

13. **Implement and run `code/atp_compartment_shares.py`.** For each cell in the spiking cohort,
    compute `total_ap_atp = atp_soma + atp_ais + atp_dendrites_total`,
    `share_soma = atp_soma / total_ap_atp`, `share_ais = atp_ais / total_ap_atp`,
    `share_dend = atp_dendrites_total / total_ap_atp`. Save per-cell shares to
    `results/data/atp_compartment_shares.csv` with columns
    `(generation, cell_index, mi_count_bits, atp_per_spike_molecules, corner_label, share_soma, share_ais, share_dend)`.
    Render two charts:
    * `results/images/atp_share_ternary.png` -- ternary scatter with soma / AIS / dendrite shares on
      the three axes, coloured by MI x ATP corner (tab10). Use `mpltern` if present in
      `pyproject.toml`; otherwise fall back to hand-rolled barycentric coordinates
      `x = 0.5 * (2 * share_ais + share_dend) / (share_soma + share_ais + share_dend)`,
      `y = (sqrt(3) / 2) * share_dend / (share_soma + share_ais + share_dend)` and plot as a regular
      scatter with a triangle outline.
    * `results/images/atp_share_violins.png` -- 2 x 3 violin grid: three rows of compartments (soma
      / AIS / dendrites) x two columns of group axes (MI group: high vs low; ATP group: high vs
      low). Compute Mann-Whitney U p-value for each violin pair and annotate it in the panel title.
      Expected: CSV row count == spiking cohort count, two PNGs exist. Satisfies REQ-17.

14. **Run `code/cluster_group_purity.py`.** Copy from t0117's `cluster_seed_purity.py`. Replace the
    `(cluster, seed)` purity calculation with two partition x reference pairs:
    `(electrophys_cluster, MI_quartile_group)`, `(electrophys_cluster, ATP_quartile_group)`,
    `(morphology_cluster, MI_quartile_group)`, `(morphology_cluster, ATP_quartile_group)`. Each
    reference assigns every spiking-cohort cell to one of three categories (high / mid / low) based
    on the quartile thresholds. For each (partition, reference) pair, compute the contingency table,
    normalised mutual information `sklearn.metrics.normalized_mutual_info_score`, and chi-square
    `scipy.stats.chi2_contingency` p-value. Write `results/data/cluster_group_purity.csv` with
    columns `(partition, reference, nmi, chi2_p, n_cells)`. Expected: 4 rows in CSV. Satisfies
    REQ-18.

15. **Write `results/data/methodology_notes.md`.** Document the t0117 -> t0125 deltas: single source
    (t0123) instead of four (t0114 / t0115 / t0116-source / t0117-source); spiking-cohort filter
    (`pd_rate_hz > 1.0 AND silence_failed_bool == False`) introduced for ATP-per-spike stability;
    ranking metric in `render_electrophys_cluster_morphs` changed from `DSI * PD` to
    `mi_count_bits / atp_per_spike_molecules`; correlation table extended from 2 to 4 outcome
    metrics; cluster-purity reference changed from `seed` to `MI_quartile_group` /
    `ATP_quartile_group`. State that all `K_SWEEP`, `KAISER_FACTOR_CAP`, `DEDUP_DECIMALS`,
    `JOINT_FACTOR_R_THRESHOLD`, varimax settings (`gamma = 1.0`, `tol = 1e-6`, `max_iter = 500`),
    and random states (`KMEANS_RANDOM_STATE = 42`, FA `random_state = 42`) are inherited verbatim
    from t0117. Note the empty `metrics.json` rationale. Expected: ~150 line markdown file.
    Satisfies REQ-19.

### Milestone G: Answer assets

16. **[CRITICAL] Create the four answer assets under `assets/answer/<answer_id>/`.** For each asset,
    create the folder, write `details.json` (spec_version "2", `answer_id` matching folder name,
    `short_answer_path: "short_answer.md"`, `full_answer_path: "full_answer.md"`,
    `categories: ["compartmental-modeling", "voltage-gated-channels"]` plus per-question relevant
    categories, `answer_methods: ["code-experiment", "papers"]`, `source_paper_ids: [...]` --
    populated from `research/research_papers.md` citation keys,
    `source_task_ids: ["t0117_*", "t0123_bedb_mi_atp_per_spike_nsga2", "t0108_*", "t0116_*"]`,
    `confidence: "medium"`, `created_by_task: "t0125_t0123_cluster_factor_mi_atp"`, `date_created` =
    today), `short_answer.md` (Question + Answer 2-5 sentences with no inline citations + Sources),
    and `full_answer.md` (Question + Short Answer + Research Process + Evidence from Papers +
    Evidence from Internet Sources [state "not used"] + Evidence from Code or Experiments +
    Synthesis + Limitations + Sources with markdown reference link definitions). Per-asset detail:

    * `assets/answer/mi-atp-joint-structure-in-t0123-substrate/` -- cites
      `results/data/factor_correlations.csv` (row of any factor with `joint_mi_atp_flag = True`,
      else statement of zero joint factors), and PCAs `pca_combined_color_mi.png` /
      `pca_combined_color_atp.png` / `pca_combined_color_corner.png`. State whether the MI x ATP
      Pareto trade-off observed in t0123 results from a single trade-off axis (joint factor) or from
      multiple competing axes (decoupled factors). Compare against the t0117 DSI x PD finding (joint
      F1 r_DSI = +0.421, r_PD = +0.352, 12.6% variance, unfiltered 4-seed pool). Cite [Achard2006],
      [Prinz2004], [Marder2006] for the parameter-degeneracy framing. Note the t0123
      `bits_per_sec = 0.0` caveat for the top-10 Pareto cells. Satisfies REQ-20 (answer 1).

    * `assets/answer/high-vs-low-mi-electrophys-signature/` -- cites the top-20 rows of
      `results/data/group_comparison.csv` ranked by `|cliffs_delta_mi|`, and
      `results/images/cliffs_delta_high_vs_low_mi.png`. State the top-5 electrophys parameters by
      `|Cliff's delta|` with effect size and direction (which group has the higher value). Cite
      [Sengupta2010] for Nav-related interpretation, [Dhingra2004] for the spike-generator MI bound,
      [Strong1998] for the bits-per-stimulus framing. Satisfies REQ-20 (answer 2), REQ-21 (top-5 for
      MI).

    * `assets/answer/low-vs-high-atp-morphology-signature/` -- cites the top-20 rows of
      `results/data/group_comparison.csv` ranked by `|cliffs_delta_atp|` restricted to the 14
      morphology parameters, plus `results/images/cliffs_delta_high_vs_low_atp.png` and
      `results/data/atp_compartment_shares.csv`. State the top-5 morphology parameters by
      `|Cliff's delta|` with effect size and direction. Address whether the low-ATP group spends
      relatively more ATP at the AIS and less in the dendrites (consult `atp_share_violins.png`).
      Cite [Mainen1996], [FohlmeisterMiller1997], [Cuntz2010] for the morphology-as-functional- axis
      framing; [Attwell2001] for the cortical 82/14/4 axon/dendrite/soma reference; [Sengupta2010]
      for the Na+/K+ overlap mechanism. Satisfies REQ-20 (answer 3), REQ-21 (top-5 for ATP
      morphology).

    * `assets/answer/pareto-favoured-corner-signature/` -- cites
      `results/data/corner_param_means.csv` (top-5 parameters by absolute z-score difference between
      `high_mi_low_atp` and `low_mi_high_atp` columns), plus
      `results/images/corner_param_heatmap.png` and the per-corner morphology galleries
      `results/images/electrophys_cluster_<k>_morphs.png` for the clusters whose `MI_quartile_group`
      purity is dominated by the high-MI / low-ATP corner. State the 5 parameters with the largest
      absolute z-score difference, the per-corner cell counts (from `group_thresholds.json`
      `corner_counts`), and the per-corner mean (MI, ATP, DSI, PD-rate) from the footer of
      `corner_param_means.csv`. Cite [Hay2011] (Pareto-acceptable-ensemble reporting convention),
      [Druckmann2007] (per-feature SD normalisation), [Baden2016] (functional-fingerprint clustering
      precedent). Satisfies REQ-20 (answer 4), REQ-21 (top-5 for corner), REQ-22 (per-corner counts
      \+ means).

    Run the answer verificator after writing each asset:
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0125_t0123_cluster_factor_mi_atp -- uv run python -u -m arf.scripts.verificators.verify_answer_asset --task-id t0125_t0123_cluster_factor_mi_atp --answer-id <answer_id>`.
    Expected: each verifier returns zero errors; four answer folders exist with valid
    `details.json`, `short_answer.md`, `full_answer.md`. Satisfies REQ-20, REQ-21, REQ-22.

* * *

## Remote Machines

None required. This is a pure local CPU task: pandas / numpy / scikit-learn / matplotlib / NEURON
pt3d rendering on 5760 cells. No GPU, no remote provisioning, no cloud egress. Expected wall-clock
~30-60 minutes on the local workstation (KMeans silhouette sweep dominates). No `setup-machines`
step is invoked.

* * *

## Assets Needed

* **Predictions asset (input, pre-existing)**:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`
  -- 5760 records, gzipped JSONL, validated by t0123's `verify_predictions_asset`. Schema:
  `{generation, cell_index, vector_68d, mi_count_bits, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, dsi_vector_sum, pd_rate_hz, objective_F_minimised, silence_failed_bool, legit_bool}`.
  Top-10 Pareto cells additionally carry `mi_strong_bialek_bits_per_sec`, `std_err_bits_per_sec`,
  `r_squared`.

* **Library (imported via library)**: `procedural_dsgc_morphology_generator` (t0090);
  `procedural_dsgc_morphology_generator_fix` (t0092). Import paths in
  `## Approach > Code Reuse Strategy`.

* **Code (copied into `code/`)**: t0117 modules (loader, standardiser, PCA, KMeans, FA, render,
  purity, helpers, paths); t0108 `constants.py`. Full module map in
  `## Approach > Code Reuse Strategy`.

* **Papers (cited, already in project corpus)**: 17 citations enumerated in
  `tasks/t0125_t0123_cluster_factor_mi_atp/research/research_papers.md`; key references for
  answer-asset citations: [Achard2006], [Prinz2004], [Marder2006], [Hay2011], [Druckmann2007],
  [VanGeit2016], [Attwell2001], [Sengupta2010], [Strong1998], [Dhingra2004], [Mainen1996],
  [FohlmeisterMiller1997], [KochPoggio1982], [LondonHausser2005], [Cuntz2010], [Hines1997],
  [Baden2016].

* * *

## Expected Assets

Match `task.json` `expected_assets: {"answer": 4}`. The four `assets/answer/<answer_id>/` folders
(each containing `details.json`, `short_answer.md`, `full_answer.md`):

| Asset | Type | answer_id | Description |
| --- | --- | --- | --- |
| 1 | answer | `mi-atp-joint-structure-in-t0123-substrate` | Does the 68-d substrate have a joint MI x ATP latent factor or decoupled factors? |
| 2 | answer | `high-vs-low-mi-electrophys-signature` | Which electrophys parameters most distinguish high-MI from low-MI cells? |
| 3 | answer | `low-vs-high-atp-morphology-signature` | Which morphology parameters most distinguish low-ATP from high-ATP cells? |
| 4 | answer | `pareto-favoured-corner-signature` | Which combination of parameters distinguishes the Pareto-favoured corner from the dominated corner? |

In addition (not asset-typed, but enumerated in REQ-coverage as evidence the answers cite):

* 12 charts under `results/images/`: `pca_combined_color_mi.png`, `pca_combined_color_atp.png`,
  `pca_combined_color_corner.png`, `pca_with_gen0_overlay.png`, `electrophys_silhouette.png`,
  `morphology_silhouette.png`, `electrophys_cluster_<k>_morphs.png` (one per electrophys cluster =
  `K_chosen`), `factor_loadings_heatmap.png`, `cliffs_delta_high_vs_low_mi.png`,
  `cliffs_delta_high_vs_low_atp.png`, `corner_param_heatmap.png`, `atp_share_ternary.png`,
  `atp_share_violins.png`.
* ~13 data tables under `results/data/`: `pool_counts.csv`, `group_thresholds.json`,
  `gen0_displacement.csv`, `electrophys_clusters.csv`, `morphology_clusters.csv`,
  `morphology_cluster_<k>_representatives.csv` (one per morphology cluster),
  `cluster_group_purity.csv`, `factor_correlations.csv`, `factor_loadings.csv`,
  `group_comparison.csv`, `corner_param_means.csv`, `atp_compartment_shares.csv`,
  `methodology_notes.md`.
* Three persisted parquets under `data/`: `t0123_cells.parquet`, `t0123_spiking_cells.parquet`,
  `t0123_gen0.parquet`, plus standardiser `t0123_standardiser.npz`.

* * *

## Time Estimation

| Phase | Estimated wall-clock |
| --- | --- |
| Research (already done) | 0 minutes (done in research stage) |
| Module skeleton + loader + standardiser (Steps 1-4) | 5-10 minutes |
| PCA + gen-0 overlay (Steps 5-6) | 3-5 minutes |
| KMeans electrophys + morphology + silhouette sweeps (Steps 7, 9) | 10-15 minutes |
| Morphology galleries (Step 8) | 5-10 minutes (NEURON pt3d build dominates) |
| Factor analysis (Step 10) | 2-3 minutes |
| Group comparison + Cliff's delta + bar charts (Step 11) | 3-5 minutes |
| Corner heatmap (Step 12) | 1-2 minutes |
| ATP compartment shares + ternary + violins (Step 13) | 2-3 minutes |
| Cluster purity + methodology notes (Steps 14-15) | 1-2 minutes |
| Answer asset writing + verification (Step 16) | 5-10 minutes |
| **Total implementation** | **~30-60 minutes** |

* * *

## Risks & Fallbacks

Pre-mortem: imagine the task has already failed. Work backwards from each failure mode.

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Predictions asset path or schema differs from research-code findings | Low | Blocking | Verify with `python -c "import gzip, json; print(json.loads(next(gzip.open('tasks/t0123_.../predictions.jsonl.gz'))))"` before running Step 2; if schema differs, update column-promotion logic and document the delta in `methodology_notes.md`. |
| Dedup-unique count < 10% of raw (poor NSGA-II diversity) | Low | Degraded analysis | Loader applies the same `n_unique > 0.10 * n_raw` gate as t0117; if it fails, fall back to the 9-decimal dedup convention used by t0086 and log the change. |
| Silhouette curve is flat (no clear k preferred) | Medium | Weak cluster identity | Per [Baden2016] best practice + t0117 convention, report the full silhouette curve in `electrophys_silhouette.png`; if peak difference < 0.05, note in `methodology_notes.md` as "k not strongly preferred" and run sensitivity check at `k_chosen +/- 1` per the research-papers recommendation #7. |
| No joint MI x ATP factor found (`joint_mi_atp_flag = False` for every factor) | Medium | Negative result for answer 1 | Report the negative finding directly per task description's "no result-suppression" requirement; state in answer 1 that decoupled factors are observed and contrast against t0117's joint DSI x PD finding. |
| Spiking cohort too small for ATP-per-spike comparisons (< 50 cells per group) | Low | Degraded statistical power | If `low_mi_count` or `low_atp_count` < 50, relax quartile thresholds to terciles (Q1/3 and Q2/3) and document the change in `methodology_notes.md`. Do not relax beyond terciles. |
| NEURON pt3d rendering OOMs on the morphology gallery | Low | Blocking gallery | The `h.delete_section` cleanup after every section is mandatory per t0109 / t0117 precedent; if RSS still grows, render galleries one cluster per subprocess (fork via `subprocess.run` per cluster) to reset NEURON state. |
| `mpltern` not installed (ternary plot fallback) | Medium | Ternary cosmetic | Hand-rolled barycentric scatter as documented in Step 13 produces a functionally equivalent triangle; cosmetic only; no impact on answers. |
| Cross-task import accidentally imports from `tasks.t0117*.code.*` instead of copying | Medium | CLAUDE.md rule 3 violation | Enforce by grep on `code/` after Step 1: `grep -r "from tasks\\.t0117\\|from tasks\\.t0116\\|from tasks\\.t0108" code/` must return zero matches. The two library imports (t0090, t0092) are explicitly permitted as libraries, not task code. |
| `metrics.json` defaults to nonempty placeholder, failing verifier | Low | Verifier error | Write empty `{}` per `metrics_specification.md` guidance + t0117 precedent; this is the orchestrator's job, not this task's, but document the rationale in `methodology_notes.md`. |
| Cliff's delta implementation has a sign bug | Low | Wrong direction in answers | Mandatory unit tests in `code/test_effect_sizes.py`: `cliffs_delta([1, 2, 3], [4, 5, 6]) == -1.0`, `cliffs_delta([4, 5, 6], [1, 2, 3]) == +1.0`, `cliffs_delta([1, 2, 3], [1, 2, 3]) == 0.0`. Step 11 gates on these passing. |

* * *

## Verification Criteria

Each criterion is a concrete check with an exact command (where applicable) and the expected output.
Includes at least one direct REQ-coverage check (the final bullet).

* **Loader correctness (REQ-1, REQ-2, REQ-3).** Run
  `uv run python -c "import pandas as pd; df = pd.read_parquet('tasks/t0125_t0123_cluster_factor_mi_atp/data/t0123_cells.parquet'); print(len(df), df.columns.tolist())"`
  and confirm row count >= 576 (10% of 5760) and columns include `mi_count_bits`,
  `atp_per_spike_molecules`, `silence_failed_bool`, `atp_soma`, `atp_ais`, `atp_dendrites_total`,
  `dsi_vector_sum`, `pd_rate_hz`, `generation`, `cell_index`. The same for
  `data/t0123_spiking_cells.parquet` with the additional check that every row satisfies
  `pd_rate_hz > 1.0 AND silence_failed_bool == False`.

* **Pool counts (REQ-1, REQ-3).** Run
  `uv run python -c "import pandas as pd; print(pd.read_csv('tasks/t0125_t0123_cluster_factor_mi_atp/results/data/pool_counts.csv').to_dict())"`
  and confirm `raw_count == 5760`, `dedup_unique_count >= 576`, `spiking_cohort_count > 0`.

* **Quartile thresholds (REQ-4).** Run
  `uv run python -c "import json; d=json.load(open('tasks/t0125_t0123_cluster_factor_mi_atp/results/data/group_thresholds.json')); assert d['mi_q1'] < d['mi_median'] < d['mi_q3']; assert d['atp_q1'] < d['atp_median'] < d['atp_q3']; print(d)"`
  and confirm no `AssertionError`.

* **Standardiser fitted on full cohort (REQ-5).** Run
  `uv run python -c "import numpy as np; d = np.load('tasks/t0125_t0123_cluster_factor_mi_atp/data/t0123_standardiser.npz'); assert d['mean'].shape == (68,) and d['std'].shape == (68,) and (d['std'] > 0).all(); print('OK')"`
  and confirm output `OK`.

* **All required charts exist (REQ-6 through REQ-11, REQ-13, REQ-15, REQ-16, REQ-17).** Run
  `ls tasks/t0125_t0123_cluster_factor_mi_atp/results/images/` and confirm presence of
  `pca_combined_color_mi.png`, `pca_combined_color_atp.png`, `pca_combined_color_corner.png`,
  `pca_with_gen0_overlay.png`, `electrophys_silhouette.png`, `morphology_silhouette.png`,
  `factor_loadings_heatmap.png`, `cliffs_delta_high_vs_low_mi.png`,
  `cliffs_delta_high_vs_low_atp.png`, `corner_param_heatmap.png`, `atp_share_ternary.png`,
  `atp_share_violins.png`, plus at least three `electrophys_cluster_<k>_morphs.png` files.

* **Factor correlations table is well-formed (REQ-13).** Run
  `uv run python -c "import pandas as pd; df = pd.read_csv('tasks/t0125_t0123_cluster_factor_mi_atp/results/data/factor_correlations.csv'); assert {'r_mi','p_mi','r_atp','p_atp','r_dsi','p_dsi','r_pd','p_pd','joint_mi_atp_flag','factor_classification'}.issubset(df.columns); print(len(df))"`
  and confirm 1 to 10 factor rows.

* **Group comparison table has 68 rows with both p-value and delta columns (REQ-14, REQ-15).** Run
  `uv run python -c "import pandas as pd; df = pd.read_csv('tasks/t0125_t0123_cluster_factor_mi_atp/results/data/group_comparison.csv'); assert len(df) == 68; assert {'mwu_p_mi','cliffs_delta_mi','mwu_p_atp','cliffs_delta_atp'}.issubset(df.columns); print('OK')"`.

* **Corner heatmap matrix is 68 x 4 (REQ-16, REQ-22).** Run
  `uv run python -c "import pandas as pd; df = pd.read_csv('tasks/t0125_t0123_cluster_factor_mi_atp/results/data/corner_param_means.csv'); assert {'parameter','high_mi_low_atp','high_mi_high_atp','low_mi_low_atp','low_mi_high_atp'}.issubset(df.columns); print(len(df))"`
  and confirm >= 68 rows.

* **Cliff's delta unit tests pass (REQ-15).** Run
  `uv run pytest tasks/t0125_t0123_cluster_factor_mi_atp/code/test_effect_sizes.py -v` and confirm 0
  failures.

* **Cross-task import rule (CLAUDE.md rule 3).** Run
  `uv run python -c "import subprocess, sys; r = subprocess.run(['grep','-rn','from tasks.t0108\\|from tasks.t0116\\|from tasks.t0117','tasks/t0125_t0123_cluster_factor_mi_atp/code/'], capture_output=True, text=True); assert r.returncode != 0 or len(r.stdout.strip()) == 0, r.stdout"`
  and confirm no matches (only library imports from t0090 / t0092 are allowed).

* **Answer-asset verification (REQ-20, REQ-21, REQ-22).** Run
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset --task-id t0125_t0123_cluster_factor_mi_atp --answer-id mi-atp-joint-structure-in-t0123-substrate`,
  same for `high-vs-low-mi-electrophys-signature`, `low-vs-high-atp-morphology-signature`,
  `pareto-favoured-corner-signature`. Confirm zero errors on each.

* **Plan verifier passes (this plan).** Run
  `uv run python -u -m arf.scripts.verificators.verify_plan t0125_t0123_cluster_factor_mi_atp` and
  confirm zero errors.

* **Requirement coverage check (REQ-1 through REQ-22).** Run
  `grep -c "REQ-" tasks/t0125_t0123_cluster_factor_mi_atp/plan/plan.md` and confirm the count is
  consistent with 22 distinct `REQ-N` items each referenced by at least one step in
  `## Step by Step` (each REQ-N appears in both the checklist and at least one step's "Satisfies"
  annotation).
