---
spec_version: "1"
task_id: "t0125_t0123_cluster_factor_mi_atp"
research_stage: "code"
tasks_reviewed: 12
tasks_cited: 10
libraries_found: 19
libraries_relevant: 2
date_completed: "2026-05-25"
status: "complete"
---
# Research Code — t0125 Cluster + Factor Analysis of t0123 MI / ATP-per-Spike Cells

## Task Objective

Adapt the canonical PCA + KMeans + varimax factor analysis pipeline used by t0108, t0116, and t0117
to the t0123 single-seed (seed 441) NSGA-II run that optimised spike-count MI vs ATP-per-spike on
the 68-d Bed B + 14-d morphology substrate. The task analyses all 5 760 evaluated cells across two
cohorts (full unfiltered cohort, and a spiking cohort defined by
`pd_rate_hz > 1.0 Hz AND NOT silence_failed_bool`), produces a 2 x 2 MI x ATP corner decomposition,
runs Cliff's-delta and Mann-Whitney group comparisons, and answers four questions as
`assets/answer/` assets: (1) does the 68-d substrate have a joint MI x ATP latent or decoupled
factors? (2) which electrophys parameters distinguish high-MI from low-MI cells? (3) which
morphology parameters distinguish low-ATP from high-ATP cells? (4) which combination of parameters
distinguishes the Pareto-favoured corner from the dominated corner?

## Library Landscape

The library aggregator script `arf.scripts.aggregators.aggregate_libraries` referenced by the
research-code skill is not implemented in this fork (only `aggregate_tasks`,
`aggregate_metric_results`, `aggregate_suggestions`, `aggregate_categories`, `aggregate_costs`,
`aggregate_machines`, `aggregate_task_types`, and `aggregate_metrics` exist under
`arf/scripts/aggregators/`). Library and answer discovery was therefore done by direct filesystem
inspection of `tasks/*/assets/library/` and `tasks/*/assets/answer/`. A total of **19 library
assets** with valid `details.json` files were enumerated.

**Domain-irrelevant libraries (17 of 19)** — these are NEURON / DSGC compartmental-model
simulation libraries (channel packs, baseline channel sets, ModelDB ports, minimal cells, scalar /
spatial GABA variants, AIS extensions) that do not bear on a CPU-only pandas / scikit-learn /
matplotlib clustering and factor analysis: `modeldb_189347_dsgc` (t0008), `tuning_curve_viz`
(t0011), `tuning_curve_loss` (t0012), `modeldb_189347_dsgc_gabamod` (t0020),
`modeldb_189347_dsgc_dendritic` (t0022), `de_rosenroll_2026_dsgc` (t0024),
`modeldb_189347_dsgc_exact` (t0046), `minimal_dsgc_scalar_gaba` (t0052), `minimal_dsgc_spatial_gaba`
(t0053), `minimal_dsgc_ampa_nmda_scalar_gaba` (t0054), `minimal_dsgc_mg_block_nmda` (t0055),
`minimal_dsgc_tonic_gaba_sweep` (t0057), `minimal_dsgc_bar_locked_gaba_ampa_sweep` (t0059),
`dsgc_active_channel_pack` (t0074), `de_rosenroll_2026_dsgc_ais` (t0078), and
`de_rosenroll_2026_dsgc_ais_dendritic_spike` (t0080).

**Relevant libraries (2 of 19)** — both required for Step 5's per-cluster morphology galleries
(NEURON pt3d rendering of full dendrite trees), exactly as already used by t0117 and t0109.

* `procedural_dsgc_morphology_generator` (t0090) — registered at
  `tasks/t0090_morphology_generator_diversity_test/assets/library/`. Key entry points:
  `MorphologyParams` (frozen dataclass with the 14 morphology fields needed to reconstruct cells
  from the 68-d vector slice `vec[54:68]`), `MorphologyResult` (with `h`, `soma`, `all_dends`,
  `section_endpoints_xy`, `origin_xy`), `BEDB_BASE_POINT`, and `PARAM_BOUNDS`. Import path:
  `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams`.
* `procedural_dsgc_morphology_generator_fix` (t0092) — registered at
  `tasks/t0092_diagnose_morphology_generator_silence/assets/library/`. Single entry point
  `generate_fixed_morphology(*, params, morph_seed=None)` is the canonical drop-in replacement for
  t0090's `generate_morphology` and is the project-standard build call used by t0109's gallery,
  t0117's render module, and `scratch_t0112_top15_morphologies.py`. Import path:
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.

These two libraries cover all morphology-rendering needs. No pandas / scikit-learn / matplotlib code
is registered as a library — the closest precedents (t0117 [t0117], t0116 [t0116], t0108 [t0108])
are bundled task code that must be copied per the cross-task-import rule (CLAUDE.md rule 3).

## Prior Answer Assets

The answer aggregator is also not implemented; the assets directory was walked directly. Of the 49
existing answer assets, the relevant subset for this task is:

* `[t0117] pooled-all-cells-truncated-cohort-artefact-test` — confirmed F1 in the unfiltered
  cross-seed pool is a joint DSI x PD factor (r_DSI = +0.421, r_PD = +0.352) when no cohort filter
  is applied. **Directly informs answer 1 here**: the MI x ATP analogue must be evaluated on the
  full t0123 pool exactly the same way.
* `[t0117] pooled-all-cells-latent-drivers` and
  `[t0117] pooled-all-cells-basin-connectivity-without-filter` — companion findings about the
  full-pool varimax structure and cluster-vs-seed purity.
* `[t0116] pooled-survivors-latent-drivers-dsi07-pd10` — strict-cohort counterpart finding (F1
  drives DSI mixed, F3 drives PD purely electrophys, no joint factor). t0116 / t0117 contrast
  defines the truncated-cohort artefact this task replicates for MI x ATP.
* `[t0108] t0106-dsi-pd-factor-decomposition-strict-cohort` and
  `[t0108] t0106-electrophys-clusters-morphology-signature` — original strict-cohort pipeline on
  t0106 seed 44 cells. F10 emerged as a single joint trade-off factor under the strict cohort.
* `[t0086] cluster-biological-plausibility-attribution` and
  `[t0088] are-cluster-motifs-mechanistically-distinct` — earlier (pre-procedural-morphology) work
  on biological-plausibility clustering of joint-pass cells under the t0080 v3 channel set. The
  methodological lesson reused here is that cluster purity needs an external categorical reference
  (biological / parameter group) to be meaningful; for t0125 that reference is the MI and ATP
  quartile group.
* `[t0123] dsgc-bits-per-atp-vs-niven-2007` — the only answer asset produced by t0123 itself,
  reporting the bits-per-ATP Pareto front against the Niven 2007 fly-photoreceptor curve. Does not
  speak to substrate structure but documents that the top-10 Pareto cells all had
  `bits_per_sec = 0.0` under Strong-Bialek because of the low PD-rate (`~3` spikes per 1 400 ms
  trial), an important caveat for any MI-based interpretation here.

These prior answers establish the trade-off-axis question pattern (high vs low quartile group,
`abs(r) > 0.30` joint-factor threshold, NMI for cluster purity) that t0125 must mechanically
transpose from DSI x PD to MI x ATP.

## Key Findings

### t0123 predictions schema — sufficient for the full pipeline, single-file load

t0123 [t0123] writes one predictions asset
`tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`
with **5 760 rows** and the per-record schema (`details.json` line 11; full doc at
`assets/predictions/.../description.md`):

```text
{generation, cell_index, vector_68d, mi_count_bits, atp_per_spike_molecules,
 atp_per_ap_molecules, atp_per_ap_compartment_breakdown,
 firing_hz_per_dir, dsi_vector_sum, pd_rate_hz, objective_F_minimised,
 silence_failed_bool, legit_bool}
```

Top-N (10) Pareto cells additionally carry `mi_strong_bialek_bits_per_sec`, `std_err_bits_per_sec`,
and `r_squared`. The format is **gzipped JSONL** (one record per line, no wrapper) — same as t0114
/ t0115 in t0117. The 68-d vector layout is identical to t0108 / t0117 (54-d electrophys + 14-d
morphology) because t0123 forked the t0122 substrate which forked the t0080 / t0090 substrate
without re-ordering parameters [t0123].

Concrete loader implications for this task (vs t0117's loader):

* Only **one source file**, not four; drop the `SOURCES` tuple and the per-seed `n_raw` / `n_unique`
  aggregation.
* The format is `.jsonl.gz` — reuse the JSONL branch of t0117's `_iter_records` (decoded line by
  line) and drop the `.json.gz` branch.
* The dedup-by-rounded-68d-vector convention (`DEDUP_DECIMALS = 6`) is preserved verbatim — t0117
  collapsed seed 44 from 3 744 raw to 1 065 unique (28 %); a similar collapse is expected here.
* The cohort-filter logic must be **replaced** entirely. t0116 filtered on
  `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0`; t0117 applied no filter. t0125 keeps **two cohorts
  in parallel**: full unfiltered (PCA / KMeans / FA, like t0117) and spiking
  (`pd_rate_hz > 1.0 AND NOT silence_failed_bool`, used for ATP-per-spike comparisons because the
  denominator approaches zero for near-silent cells).
* Three new diagnostic columns must be promoted to top-level DataFrame columns by the loader:
  `mi_count_bits`, `atp_per_spike_molecules`, and the **dict** field
  `atp_per_ap_compartment_breakdown` (keys: `soma`, `ais`, `dendrites_total`). The breakdown is most
  cleanly stored as three separate columns (`atp_soma`, `atp_ais`, `atp_dendrites_total`) plus three
  derived **share** columns (`atp_share_soma`, `atp_share_ais`, `atp_share_dendrites_total`).

### Pipeline architecture from t0108 / t0116 / t0117

t0117 [t0117] (15 source files, 2 374 lines) is the most direct structural template because it runs
the no-filter variant of the analysis and uses the union-pool standardiser invariant. Its module
layout — `paths.py` (63 lines), `constants.py` (158 lines), `cluster_helpers.py` (170 lines),
`load_pooled_cells.py` (254 lines), `load_pooled_gen0.py` (126 lines), `fit_standardiser.py` (57
lines), `pooled_pca_with_overlay.py` (379 lines), `factor_analysis.py` (262 lines),
`cluster_electrophys.py` (159 lines), `cluster_morphology.py` (195 lines),
`render_electrophys_cluster_morphs.py` (220 lines), `morphology_rendering.py` (178 lines),
`cluster_seed_purity.py` (85 lines), `methodology_and_comparison.py` (267 lines) — maps almost
1-to-1 onto the t0125 step list.

t0116 [t0116] (16 source files, 2 282 lines) is structurally identical to t0117 except for the
loader (`load_pooled_cells.py` applies the strict DSI / PD filter) and the methodology / comparison
module (compares t0116 strict cohort against the t0108 strict cohort). It also includes a local
re-implementation of `verify_answer_asset` called `verify_answers_local.py` (150 lines) that is
**NOT** needed for t0125 because the project's `verify_answer_asset` verificator now exists.

t0108 [t0108] (8 source files, 1 738 lines) is the original strict-cohort version. Its
`factor_analysis.py` (362 lines) is the **authoritative source of the `varimax_rotation` helper**
(lines 48-78, iterative-SVD; gamma=1, tol=1e-6, max_iter=500) — t0116, t0117, and t0125 all reuse
this helper verbatim. Its `code/constants.py` (111 lines) is the **authoritative source of
`ALL_PARAM_NAMES`** (54-d `ELECTROPHYS_PARAM_NAMES` + 14-d `MORPHOLOGY_PARAM_NAMES`, sealed with
length asserts).

Common architecture across all three:

* `paths.py` centralises every input / output `Path` constant; tests by file presence are easy.
* `constants.py` owns parameter names, k-sweep range, Kaiser cap, joint-factor threshold, dedup
  decimals, KMeans random state. t0117 uses `K_SWEEP = (3, 4, 5, 6, 7)` and
  `KAISER_FACTOR_CAP = 10`; t0125 inherits both because the task description says "auto-pick k in
  [3, 7]".
* `cluster_helpers.py` defines the `PooledStandardiser` frozen dataclass (mean / std arrays as
  `NDArray[np.float64]`, `transform` method, `save_standardiser` / `load_standardiser` to / from
  `.npz`), plus `fit_pooled_standardiser`, `zscore_matrix`, `run_pca`, `run_kmeans_sweep`,
  `top_k_loadings`, and `write_json`. Zero-std columns are clipped to 1.0 to avoid division-by-zero
  — this matters because `morph_seed` and a few electrophys parameters can be near-constant in
  narrow cohorts.
* The standardiser is fitted **once** on the full-cohort union pool and serialised to
  `data/pooled_standardiser.npz`. Every downstream PCA, KMeans, FA, and gen-0 projection reuses the
  same fit. Per-seed (or per-cohort) re-fitting is forbidden. The t0117 module docstring explicitly
  warns: "Per-seed re-fitting would absorb cross-seed scale differences into the standardiser and
  erase the very signal the analysis is designed to detect." For t0125 the same rule applies between
  the full and spiking cohorts — the spiking-cohort analysis must reuse the full-cohort
  standardiser, not refit on the spiking subset.

### Factor analysis details that must be preserved

The factor-analysis flow in `code/factor_analysis.py` (both t0108 and t0117 versions) goes:

1. `_drop_constant_columns` removes columns whose `std < 1e-8` from the standardised matrix to avoid
   degenerate FA; record the kept indices and names. For t0123 cells this should drop few or no
   columns because the full pool spans 60 generations of NSGA-II offspring across the bounds.
2. `np.linalg.eigvalsh(np.cov(z, rowvar=False, ddof=0))[::-1]` produces correlation-matrix
   eigenvalues sorted descending. `n_eig_above_one = sum(eig > 1.0)` is the Kaiser criterion;
   `n_factors = max(1, min(n_eig_above_one, KAISER_FACTOR_CAP))` (cap = 10).
3. `FactorAnalysis(n_components=n_factors, rotation=None, random_state=42)` fits the unrotated
   loadings; `varimax_rotation` (the iterative-SVD helper, copied from t0108) rotates them to
   gamma=1 varimax. The rotation method is **stand-alone**; do not use scikit-learn's
   `rotation="varimax"` — t0108 deliberately used the in-house iterative-SVD code.
4. Rotated factor scores via the **regression approximation**:
   `scores = Z @ Lambda @ pinv(Lambda.T @ Lambda)` — closed-form, deterministic given the rotated
   loadings.
5. Variance explained per factor = `sum(Lambda**2, axis=0) / n_kept_dims`. Total variance explained
   is the sum.
6. Pearson r and p between each rotated factor score and **each outcome metric**. For t0117 the
   outcomes were `dsi_vector_sum` and `pd_rate_hz`. For t0125 the outcomes are `mi_count_bits`,
   `atp_per_spike_molecules`, `dsi_vector_sum`, and `pd_rate_hz` — same code, four columns instead
   of two.
7. Joint-factor flag: `abs(r_metric_a) > 0.30 AND abs(r_metric_b) > 0.30`. For t0125 the "joint MI x
   ATP factor" check uses metrics_a = MI and metrics_b = ATP; the additional |r| > 0.30 vs DSI and
   PD give classifications "MI-only", "ATP-only", "MI+ATP joint", "MI+DSI joint", "ATP+PD joint"
   etc.

The loadings heatmap is rendered with `RdBu_r` colourmap and symmetric
`vmin / vmax = +/- max(|loadings|)`, matching t0108 / t0117 verbatim. Figure height scales as
`0.18 * 68 + 1` inches.

### KMeans + silhouette auto-pick

`run_kmeans_sweep` in `cluster_helpers.py` iterates `K_SWEEP = (3, 4, 5, 6, 7)`, runs
`KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(...)`, computes
`silhouette_score(matrix_zscored, labels)`, and picks the headline `k` by `max(silhouette)`. The
sweep runs separately on the 54-d electrophys submatrix and on the 14-d morphology submatrix, both
pre-standardised by the full-cohort `PooledStandardiser` [t0117]. For 5 760 cells the sweep is
comfortably CPU-bound and finishes in 1-2 minutes — t0117 ran on 4 431 cells in similar time per
the task description's ~30-60 min total wall estimate.

### Morphology rendering for cluster galleries

t0117 [t0117] and t0109 [t0109] both render NEURON pt3d morphologies — full dendrite trees, not
just somas (`feedback_top50_morphologies_full_dendrites.md` memory). Helpers live in
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/morphology_rendering.py` (178 lines,
copied from t0116 which copied from t0109). The key steps:

* `to_morph_params(vec)` slices the 14-d morphology tail off the 68-d vector, coerces
  `num_primary_branches` and `max_strahler_depth` to `int(round(...))`, and applies
  `morph_seed % (2**31 - 1)` to avoid INT32 overflow. **The `% MAX_MORPH_SEED` coercion is
  mandatory** — t0109 line 130 explicitly documents this.
* `build_and_extract(params)` calls `generate_fixed_morphology(params=params)` from the t0092
  library, then extracts pt3d arrays via `h.x3d(i) / h.y3d(i) / h.diam3d(i)` over `result.soma` and
  every section in `result.all_dends`. The `h.delete_section(sec=s)` cleanup at the end is also
  mandatory to prevent NEURON RSS creep across many cells in one process.
* `plot_cell(ax, built, label)` renders dendrites as blue line segments scaled by mean diameter,
  soma as a red `mpatches.Circle` of radius `max(4 um, mean diameter / 2)`, plus a PD arrow.
* `global_extents(built_list)` returns a single square (xlo, xhi, ylo, yhi) covering every cell so
  all panels share the same axes — visual comparison across the cluster is then valid.
* `render_electrophys_cluster_morphs._select_top_per_cluster` ranks within cluster by `DSI * PD`
  descending. **For t0125 this ranking metric must change**: per task description Step 5, rank
  representatives by `mi_count_bits / atp_per_spike_molecules` (bits-per-ATP) within cluster,
  restricted to the spiking cohort. The grid is **5 rows x 3 cols = 15 panels**, same as t0117.

### Effect sizes and group comparisons

The t0125 task description adds two analyses that have no exact precedent in t0108 / t0116 / t0117
but are easily expressed:

* **Mann-Whitney U two-sided p-value** via `scipy.stats.mannwhitneyu(alternative="two-sided")` —
  already available in the project's deps. No previous task ran this at scale across 68 parameters,
  but t0108's `cluster_electrophys.py` uses Kruskal-Wallis (`scipy.stats.kruskal`) with Bonferroni
  correction across 54 features, which is structurally identical.
* **Cliff's delta effect size** — the rank-based statistic `delta = (#x>y - #x<y) / (n_x * n_y)`.
  No prior task implemented this. The standard formula is about 20 lines including ties handling;
  the task description says to put it in `code/effect_sizes.py`. Recommended reference
  implementation: pair `np.argsort` of the combined vector with `np.searchsorted` to count
  exceedances in O(n log n).

### Common patterns across analysis tasks

* Path constants live in `code/paths.py` and use `REPO_ROOT = Path(__file__).resolve().parents[3]`
  then derived paths. The chart helpers always call
  `out_path.parent.mkdir(parents=True, exist_ok=True)` before saving.
* Constants live in `code/constants.py`. The 54-d / 14-d / 68-d parameter-name tuples are sealed
  with `assert len(...) == N_*_DIMS`.
* Every chart is rendered with `matplotlib.use("Agg")` for headless CPU runs, `dpi=150`, and an
  explicit `fig.tight_layout()` + `fig.savefig(path, dpi=CHART_DPI)` + `plt.close(fig)` cleanup.
  This pattern is uniform across t0108, t0116, t0117, t0123, and t0109.
* Every numeric CSV emits explicit dtypes via the `_typed_dataframe` helper pattern; parquet files
  always go through `_typed_dataframe` then `to_parquet(path, index=False)`.
* Every module is callable both as `python -u -m tasks.<task>.code.<module>` and via `main()` guard
  at the bottom.

## Reusable Code and Assets

### Libraries — import directly via library

* `procedural_dsgc_morphology_generator` (t0090) — **import via library**.
  `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams`.
  Provides the 14-field `MorphologyParams` frozen dataclass (`num_primary_branches: int`,
  `branch_prob_per_um: float`, ..., `branch_length_cv: float`) with `from_dict` / `to_dict` /
  `from_bedb_base_point` constructors. Needed by Step 5 morphology rendering.
* `procedural_dsgc_morphology_generator_fix` (t0092) — **import via library**.
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
  Signature:
  `generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`.
  Returns object with `h`, `soma`, `all_dends`, `section_endpoints_xy`, `origin_xy`. Used in every
  per-cluster morphology gallery in this project.

### Task code — copy into t0125 `code/` directory

* `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` — **copy into task**. Source of
  `ALL_PARAM_NAMES`, `ELECTROPHYS_PARAM_NAMES` (54), `MORPHOLOGY_PARAM_NAMES` (14),
  `N_ELECTROPHYS_DIMS = 54`, `N_MORPHOLOGY_DIMS = 14`, `N_TOTAL_DIMS = 68`. About 110 lines. Strip
  the `DSI_THRESHOLD` / `PD_THRESHOLD_HZ` / `SOURCE_TASK` / `SOURCE_SEED` constants and add
  t0125-specific constants: `SPIKING_PD_RATE_HZ_THRESHOLD = 1.0`, `MI_QUARTILE_TOP_QUANTILE = 0.75`,
  `MI_QUARTILE_BOTTOM_QUANTILE = 0.25`, `CLIFFS_DELTA_TOP_N = 20`,
  `T0123_PREDICTIONS_REL_PATH = Path("tasks/t0123_.../predictions.jsonl.gz")`.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/cluster_helpers.py` — **copy into
  task**. 170 lines. `PooledStandardiser`, `fit_pooled_standardiser`, `save_standardiser`,
  `load_standardiser`, `zscore_matrix`, `run_pca`, `run_kmeans_sweep`, `top_k_loadings`,
  `write_json`, `PCAResult` / `KMeansResult` / `KMeansSweepResult` dataclasses. **Adaptation**:
  change the namespace in the import header to
  `tasks.t0125_t0123_cluster_factor_mi_atp.code.constants`. No behavioural changes needed.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/fit_standardiser.py` — **copy into
  task**. 57 lines. Reads `data/t0123_cells.parquet` (renamed from `pooled_all_cells.parquet`), fits
  the standardiser on the full cohort, saves to `data/t0123_standardiser.npz`. Only path and
  module-namespace changes needed.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/load_pooled_cells.py` — **copy +
  major adaptation**. 254 lines. **Critical changes**:
  * Drop the `SOURCES` tuple and per-source loop. Read only the single
    `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/.../files/predictions.jsonl.gz`
    file.
  * Keep only the `.jsonl.gz` branch of `_iter_records` (drop the `.json.gz` branch).
  * Promote new columns to top-level: `mi_count_bits`, `atp_per_spike_molecules`,
    `silence_failed_bool`, `atp_soma`, `atp_ais`, `atp_dendrites_total` (from
    `atp_per_ap_compartment_breakdown`).
  * Apply the dedup-by-rounded-68d-vector rule (`DEDUP_DECIMALS = 6`) unchanged.
  * Persist two parquets: `data/t0123_cells.parquet` (full cohort, dedup-unique) and
    `data/t0123_spiking_cells.parquet` (spiking cohort subset).
  * Write `results/data/pool_counts.csv` (raw / dedup-unique / spiking-cohort counts) and
    `results/data/group_thresholds.json` (MI Q1 / Q3 / median, ATP Q1 / Q3 / median).

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/load_pooled_gen0.py` — **copy +
  minor adaptation**. 126 lines. Drop the per-source loop. Read t0123 predictions, keep only
  `generation == 1` records (96 expected). Persist `data/t0123_gen0.parquet`. Same dtype and
  column-typing pattern.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/pooled_pca_with_overlay.py` —
  **copy + major adaptation**. 379 lines. Restructure the 1 x 3 PCA panel into **three separate
  figures**, each with the three PCAs (combined / electrophys / morphology) coloured by:
  * `pca_combined_color_mi.png` — viridis on `mi_count_bits`
  * `pca_combined_color_atp.png` — viridis on `log10(atp_per_spike_molecules)`
  * `pca_combined_color_corner.png` — categorical tab10 on the 4 MI x ATP quadrants. Replace
    `_scatter_cells_by_seed` with `_scatter_cells_by_value` (continuous colormap) and
    `_scatter_cells_by_corner` (categorical). Keep gen-0 overlay (`pca_with_gen0_overlay.png`) and
    the displacement table (`gen0_displacement.csv`), but segment displacement statistics **per MI x
    ATP corner** instead of per seed.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/factor_analysis.py` — **copy +
  minor adaptation**. 262 lines. Reuses `varimax_rotation` (lines 48-78 of t0108's version,
  identical iterative-SVD; gamma=1, tol=1e-6, max_iter=500), `FactorResult`,
  `_drop_constant_columns`, `run_factor_analysis`, `_plot_loadings_heatmap`. **Adaptation**: extend
  the correlation table to four metrics (`mi_count_bits`, `atp_per_spike_molecules`,
  `dsi_vector_sum`, `pd_rate_hz`) instead of two. Add a `joint_mi_atp_flag` column with the |r| >
  0.30 rule and a `factor_classification` column ("joint_MI_ATP", "MI_only", "ATP_only",
  "decoupled") for downstream answer 1.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/cluster_electrophys.py` — **copy +
  minor adaptation**. 159 lines. KMeans on the 54-d electrophys submatrix with silhouette auto-pick
  over `K_SWEEP = (3, 4, 5, 6, 7)`. The output CSV needs the MI / ATP / DSI / PD columns added per
  cell (Step 5's "per-cluster mean MI / ATP / DSI / PD / firing-rate" requirement); strip the
  `_seed`-specific reporting.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/cluster_morphology.py` — **copy
  + minor adaptation**. 195 lines. KMeans on the 14-d morphology submatrix. Output per-cluster
    representative table; **adaptation**: the 15-row representative table now needs
    `(generation, cell_index, mi_count_bits, atp_per_spike_molecules, dsi_vector_sum, pd_rate_hz, ephys_PC1, ephys_PC2, ephys_PC3, soma_share_atp)`
    (Step 6's requirement) — add
    `soma_share_atp = atp_soma / (atp_soma + atp_ais + atp_dendrites_total)`.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/render_electrophys_cluster_morphs.py`
  — **copy + minor adaptation**. 220 lines. The 5 x 3 grid is preserved. **Critical adaptation**:
  replace the within-cluster ranking metric from `DSI * PD` (t0117) to
  `mi_count_bits / atp_per_spike_molecules` (bits-per-ATP) restricted to the spiking cohort.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/morphology_rendering.py` — **copy
  unchanged** (after namespace update). 178 lines. NEURON pt3d helpers (`SectionPts`, `BuiltMorph`,
  `CellLabel`, `to_morph_params`, `extract_section_pts`, `build_and_extract`, `global_extents`,
  `plot_cell`). The `MAX_MORPH_SEED = 2**31 - 1` modulo and the `h.delete_section` cleanup are
  mandatory; do not strip them.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/cluster_seed_purity.py` — **copy +
  heavy adaptation**. 85 lines. Replace the `(cluster, seed)` purity calculation with a
  `(cluster, MI_quartile_group)` and `(cluster, ATP_quartile_group)` contingency table per
  partition. Output renamed `results/data/cluster_group_purity.csv`. NMI + chi-square reporting
  structure stays.

* `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/paths.py` — **copy + path
  renames**. 63 lines. All `pooled_*` names become `t0123_*` and the new outputs from the t0125 step
  list are added: `pca_combined_color_mi.png`, `pca_combined_color_atp.png`,
  `pca_combined_color_corner.png`, `cliffs_delta_high_vs_low_mi.png`,
  `cliffs_delta_high_vs_low_atp.png`, `corner_param_heatmap.png`, `atp_share_ternary.png`,
  `atp_share_violins.png`, `group_thresholds.json`, `pool_counts.csv`, `group_comparison.csv`,
  `corner_param_means.csv`, `atp_compartment_shares.csv`.

### New modules required (no precedent)

* `code/effect_sizes.py` — **new code**. Implement `cliffs_delta(x: NDArray, y: NDArray) -> float`
  via rank-based formula. Roughly 30 lines including ties handling. Test via
  `code/test_effect_sizes.py` against a known-result example.
* `code/group_comparison.py` — **new code, ~150 lines**. For each of 68 parameters, compute mean /
  std in high-MI / low-MI / high-ATP / low-ATP groups, Mann-Whitney U two-sided p, Cliff's delta, on
  the spiking cohort. Emit `results/data/group_comparison.csv` and the two ranked-bar
  `cliffs_delta_*.png` charts (top-20 by `|delta|`).
* `code/corner_heatmap.py` — **new code, ~100 lines**. 68 x 4 z-scored mean matrix in the four MI
  x ATP corners; render as `RdBu_r` heatmap with symmetric vmin / vmax; save the matrix to
  `results/data/corner_param_means.csv`.
* `code/atp_compartment_shares.py` — **new code, ~200 lines**. Per-cell soma / AIS / dendrite
  shares of total per-AP ATP cost on the spiking cohort. Render ternary plot
  (`results/images/atp_share_ternary.png`, coloured by corner) and 6-panel violin plot
  (`results/images/atp_share_violins.png`, by MI group and ATP group). Save per-cell shares to
  `results/data/atp_compartment_shares.csv`. The `mpltern` package is the standard ternary helper;
  check `pyproject.toml` — if absent, fall back to a hand-rolled barycentric scatter.

### Source data — pre-existing asset

* **Predictions asset**:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`
  [t0123]. 5 760 records, jsonl.gz format. Validated by t0123's `verify_predictions_asset`.
  Authoritative — do **not** read the alternative
  `tasks/t0123_*/results/data/all_evaluations_seed441.json.gz` per the task description.

## Lessons Learned

### Standardiser fit is a single point of correctness

t0108, t0116, and t0117 all converge on the same invariant: fit the standardiser **once** on the
union pool (or the full cohort), persist it, and reuse it across every PCA, KMeans, FA, and
projection. t0117's `fit_standardiser.py` and the `PooledStandardiser` dataclass embody this. The
risk if violated: per-cohort refitting absorbs cohort-specific scale into the standardiser and
erases the signal the analysis is designed to detect. t0125 has two cohorts (full + spiking) and
must use the full-cohort standardiser everywhere, including the spiking-cohort group comparisons.

### Truncated-cohort artefacts are real

t0116 [t0116] found zero joint DSI x PD factors under the strict cohort (DSI > 0.7 AND PD > 10);
t0117 [t0117] confirmed that removing the filter restored a joint factor F1 (r_DSI = +0.421, r_PD =
+0.352) on the same underlying NSGA-II output. The MI x ATP analogue is **the central question** of
t0125's answer 1. The full cohort (5 760 cells, including silent and near-silent cells) must be used
for the FA correlations; the spiking cohort is only for the ATP-per-spike group comparisons because
the denominator is unstable for near-silent cells.

### Cluster purity requires a meaningful external categorical reference

t0117's cluster-vs-seed NMI works because seed is the natural categorical reference for a multi-seed
pool. t0125 has only one seed, so cluster-vs-seed is meaningless. The replacement references are the
**MI quartile group** and the **ATP quartile group** (one categorical variable each, 2 or 4 levels
depending on the analysis). Per-cluster mean MI / ATP / DSI / PD provides the continuous companion
view.

### NEURON pt3d morphology rendering needs the `h.delete_section` cleanup

t0109 [t0109] and t0117 both call `h.delete_section(sec=s)` for every soma and dendrite section
after extracting pt3d arrays, wrapped in `contextlib.suppress(RuntimeError, AttributeError)`.
Without this cleanup NEURON's RSS grows linearly with the number of cells built per process and can
OOM on large galleries. Memory `feedback_top50_morphologies_full_dendrites.md` requires **full
dendrite trees** (not soma-only), so the cleanup matters even more — each cell typically has 100+
dendrite sections.

### Single-file source simplifies the loader but loses the dedup gate

t0117's loader has an explicit validation gate: t0106 must yield n_raw > 0 and n_unique > 0.1 *
n_raw (more than 10 % of records survive 6-decimal dedup). For t0125 with only one source, the same
gate applies (n_unique > 0.1 * 5 760 = 576). NSGA-II naturally collapses many converged offspring;
28 % survival in t0106 and similar elsewhere; expect 1 000-3 000 unique cells after dedup.

### MI count-bits has a low ceiling and a degenerate corner

t0123 [t0123] reported `best_mi_count_bits = 1.459` at the high-MI corner but
`Strong-Bialek bits_per_sec = 0.0` for all 10 top-Pareto cells because PD-rate was too low (~3
spikes / 1 400 ms trial) to populate non-trivial spike-time words. This is a methodological caveat
for any MI-based interpretation in t0125: cells in the "high-MI" quartile may include optimisation
artefacts where MI is high but the underlying spike train is degenerate. The spiking cohort filter
(`pd_rate_hz > 1.0 AND NOT silence_failed_bool`) partly mitigates this, but answer 1 must note that
the MI metric is count-MI on a 4-direction contingency, not a rate or bits/s code.

### Validate dependencies before relying on aggregator output

The library and answer aggregators (`aggregate_libraries.py`, `aggregate_answers.py`) referenced by
the research-code skill do **not exist** in this fork. Direct filesystem walking of
`tasks/*/assets/{library,answer}/` is the fallback. Future skill invocations should detect this
upfront rather than failing with `ModuleNotFoundError`.

## Recommendations for This Task

### Module structure (highest priority)

Set up `code/` mirroring t0117's layout, then add four new modules:

```text
tasks/t0125_t0123_cluster_factor_mi_atp/code/
  __init__.py
  paths.py                                  # copy + rename from t0117
  constants.py                              # copy from t0108, strip DSI/PD constants, add t0125 ones
  cluster_helpers.py                        # copy verbatim from t0117 (namespace change only)
  load_t0123_cells.py                       # copy + heavily adapt from t0117 load_pooled_cells.py
  load_t0123_gen0.py                        # copy + minor adapt from t0117 load_pooled_gen0.py
  fit_standardiser.py                       # copy + rename from t0117
  pca_with_overlay.py                       # copy + heavily adapt from t0117 pooled_pca_with_overlay.py
  factor_analysis.py                        # copy + minor adapt from t0117
  cluster_electrophys.py                    # copy + minor adapt from t0117
  cluster_morphology.py                     # copy + minor adapt from t0117
  cluster_group_purity.py                   # copy + heavily adapt from t0117 cluster_seed_purity.py
  morphology_rendering.py                   # copy verbatim from t0117 (namespace change only)
  render_electrophys_cluster_morphs.py      # copy + minor adapt from t0117 (rank by bits-per-ATP)
  effect_sizes.py                           # NEW
  group_comparison.py                       # NEW (Step 8: 68-param Cliff's delta + MWU)
  corner_heatmap.py                         # NEW (Step 9: 68 x 4 z-scored corner means)
  atp_compartment_shares.py                 # NEW (Step 10: soma/AIS/dendrite shares ternary + violins)
  methodology_notes.py                      # copy + adapt from t0117 (compare against t0117 not t0116)
  test_effect_sizes.py                      # NEW (unit tests for Cliff's delta)
```

Approximate total: ~3 000 lines (similar to t0117's 2 374 lines plus ~600 lines of new code for the
t0125-specific analyses).

### Use the existing library imports, do not re-vendor morphology helpers

The `procedural_dsgc_morphology_generator` and `procedural_dsgc_morphology_generator_fix` libraries
are project-registered. Direct import path is the only sanctioned cross-task code reuse. Do not copy
`morphology_generator_fix.py` or `morphology_params.py` into t0125's `code/` directory.

### Preserve every t0117 / t0108 hyperparameter

* `DEDUP_DECIMALS = 6` — keep verbatim.
* `K_SWEEP = (3, 4, 5, 6, 7)` — keep verbatim (matches task description Step 5/6).
* `KMEANS_RANDOM_STATE = 42`, `N_INIT_KMEANS = 10` — keep verbatim.
* `KAISER_FACTOR_CAP = 10` — keep verbatim.
* `JOINT_FACTOR_R_THRESHOLD = 0.30` — keep verbatim (task description uses |r| > 0.3).
* `RANDOM_SEED = 42` (FactorAnalysis), `CHART_DPI = 150` — keep verbatim.
* Varimax: `gamma = 1.0`, `tol = 1e-6`, `max_iter = 500`, in-house iterative-SVD — keep verbatim.

### Two-cohort architecture

The full cohort is the standardiser-fit cohort, the PCA-fit cohort, the KMeans-fit cohort, and the
FA-fit cohort. The spiking cohort is **only** used for: Cliff's delta + MWU group comparisons (Step
8), the cluster-representative ranking by bits-per-ATP (Step 5/6), the 2 x 2 corner z-scored heatmap
(Step 9), and the ATP compartment-share comparison (Step 10). Mixing these up — e.g. refitting the
standardiser on the spiking cohort — will silently corrupt the joint-factor finding.

### Preserve full dendrite trees in morphology grids

Per memory `feedback_top50_morphologies_full_dendrites.md`, render full dendrite trees, not
soma-only. The t0117 `morphology_rendering.py` already does this; do not change the rendering code.
The `5 x 3 = 15` cells per cluster panel layout is fixed by Step 5.

### Output one answer asset per question, citing source CSV rows / chart files

The task description defines four questions, each becoming one `assets/answer/<id>/` asset following
`meta/asset_types/answer/specification.md`. Each answer must cite the specific row / column of
`group_comparison.csv` or `factor_correlations.csv` underpinning its verdict, the specific chart
image, and the per-corner cell counts. Use `meta/asset_types/answer/` specification version 2
(`ANSWER_SPEC_VERSION = "2"`).

### Compare-literature pass against t0117

`results/compare_literature.md` must include one row comparing the t0125 MI x ATP joint-factor
finding against t0117's DSI x PD joint-factor finding (truncated-cohort artefact confirmation for
the DSI x PD axis; same hypothesis testable for MI x ATP here). The structure of
`tasks/t0117_*/code/methodology_and_comparison.py` (267 lines) is the template — copy and
re-target the comparison from "t0117 vs t0116" to "t0125 vs t0117" with the metric pairs
substituted.

## Task Index

### [t0086]

* **Task ID**: `t0086_robustness_cluster_bio_comparison`
* **Name**: Robustness cluster biological-plausibility attribution
* **Status**: completed
* **Relevance**: Established the cluster-vs-categorical-reference NMI methodology
  (biological-plausibility groups as the reference) that t0125 transposes to MI / ATP quartile
  groups for cluster purity.

### [t0088]

* **Task ID**: `t0088_recluster_marginals_and_vm_motifs`
* **Name**: Re-cluster t0086 13-cell pool in t0080 54-d v3 parameter space
* **Status**: completed
* **Relevance**: Companion analysis to t0086 confirming that mechanism distinctness across clusters
  requires per-cluster mechanism inspection (not just centroid distance) — informs Step 5/6
  representative-cell selection rule.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator + diversity test
* **Status**: completed
* **Relevance**: Source of the `procedural_dsgc_morphology_generator` library and the
  `MorphologyParams` dataclass needed by Step 5/6's morphology galleries.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose t0090 procedural-cell silence; ship the soma-area fix
* **Status**: completed
* **Relevance**: Source of the `procedural_dsgc_morphology_generator_fix` library and the
  `generate_fixed_morphology` function — the project-standard cell-build entry point used in every
  morphology gallery from t0109 onwards, including t0125.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long PD-ND NSGA-II 300 generations
* **Status**: completed
* **Relevance**: Source of the original 68-d vector layout (54-d electrophys + 14-d morphology)
  inherited by t0108 / t0116 / t0117 / t0122 / t0123 / t0125. The `_dedupe_cells` and
  `_passes_filter` patterns originate in t0108 over this run's outputs.

### [t0108]

* **Task ID**: `t0108_t0106_cluster_factor_dsi05_pd10`
* **Name**: Cluster + factor analysis on t0106 (strict cohort DSI > 0.5, PD > 10)
* **Status**: completed
* **Relevance**: Original strict-cohort version of the pipeline. **Authoritative source of
  `ALL_PARAM_NAMES` constants** and the in-house `varimax_rotation` iterative-SVD helper that t0116
  / t0117 / t0125 all reuse verbatim.

### [t0109]

* **Task ID**: `t0109_t0108_morph_cluster_gallery`
* **Name**: Morphology gallery for t0108 clusters
* **Status**: completed
* **Relevance**: Original NEURON pt3d morphology rendering pipeline (`_to_morph_params`,
  `_build_and_extract`, `_plot_cell`, `_global_extents`, `_select_top_per_cluster`). t0117 copied
  these helpers; t0125 will inherit them through the same copy chain.

### [t0116]

* **Task ID**: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
* **Name**: Pooled PCA + cluster + factor analysis (DSI > 0.7, PD > 10) across 4 seeds
* **Status**: completed
* **Relevance**: Strict-cohort variant of the multi-seed pooled pipeline. Found **no joint DSI x PD
  factor** under the strict filter; t0117 reversed this finding. t0125 replicates the same test for
  MI x ATP and cites both t0116 and t0117 as the methodology precedents.

### [t0117]

* **Task ID**: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
* **Name**: Pooled PCA + cluster + factor analysis (no DSI / PD filter) across 4 seeds
* **Status**: completed
* **Relevance**: **Primary structural template for t0125.** Every module (loader, standardiser fit,
  PCA + gen-0 overlay, factor analysis, KMeans on both subspaces, cluster purity, morphology
  rendering, methodology-comparison) is the direct copy source. Confirmed the truncated-cohort
  artefact for DSI x PD (joint F1 with r_DSI = +0.421, r_PD = +0.352); t0125 tests whether the same
  artefact holds for MI x ATP.

### [t0123]

* **Task ID**: `t0123_bedb_mi_atp_per_spike_nsga2`
* **Name**: NSGA-II MI vs ATP-per-spike on Bed B + 14-d morph (seed 441, 60 gens)
* **Status**: completed
* **Relevance**: **Sole source of input data for this task**. Produced the 5 760-cell predictions
  asset that t0125 analyses, including the new `mi_count_bits`, `atp_per_spike_molecules`, and
  `atp_per_ap_compartment_breakdown` fields. The full per-record schema is documented in t0123's
  `build_predictions_assets.py` and the asset's `description.md`.
