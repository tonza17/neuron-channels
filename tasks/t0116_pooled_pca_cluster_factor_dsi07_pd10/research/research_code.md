---
spec_version: "1"
task_id: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 8
libraries_found: 19
libraries_relevant: 2
date_completed: "2026-05-21"
status: "complete"
---
# Research Code — t0116 Pooled PCA + Cluster + Factor Analysis (DSI > 0.7 ∧ PD > 10)

## Task Objective

Pool the DSI > 0.7 ∧ pd_rate_hz > 10 Hz survivor cells from four NSGA-II runs (t0106 seed 44, t0112
seed 77, t0114 seed 7755, t0115 seed 9354) and run the same PCA + KMeans + varimax factor analysis
pipeline used by t0108, but in a multi-seed pool keyed by
`(source_task, seed, generation, individual_idx)`. Three questions are answered as separate
`assets/answer/` assets: (1) does the joint-pass cohort form one connected basin or seed-specific
sub-basins? (2) how far did NSGA-II travel from the gen-0 random initialisation, per seed? (3) which
varimax-rotated factors drive joint DSI / pd_rate_hz quality, and are they morphology-,
electrophys-, or mixed-loaded?

## Library Landscape

The library aggregator script `arf.scripts.aggregators.aggregate_libraries` referenced by the
research-code skill is not implemented in this fork of the ARF framework (only `aggregate_tasks`,
`aggregate_metric_results`, `aggregate_suggestions`, `aggregate_categories`, `aggregate_costs`,
`aggregate_machines`, `aggregate_task_types`, and `aggregate_metrics` exist under
`arf/scripts/aggregators/`). Library and answer discovery was therefore done by direct filesystem
inspection of `tasks/*/assets/library/` and `tasks/*/assets/answer/`. A total of **19 library
assets** were enumerated, summarised below.

**Domain-irrelevant libraries (16 of 19)** — these are NEURON / DSGC compartmental-model libraries
that do not bear on a CPU-only pandas/scikit-learn/matplotlib analysis: `modeldb_189347_dsgc` (from
t0008), `tuning_curve_viz` (t0011), `tuning_curve_loss` (t0012), `modeldb_189347_dsgc_gabamod`
(t0020), `modeldb_189347_dsgc_dendritic` (t0022), `de_rosenroll_2026_dsgc` (t0024),
`modeldb_189347_dsgc_exact` (t0046), `minimal_dsgc_scalar_gaba` (t0052), `minimal_dsgc_spatial_gaba`
(t0053), `minimal_dsgc_ampa_nmda_scalar_gaba` (t0054), `minimal_dsgc_mg_block_nmda` (t0055),
`minimal_dsgc_tonic_gaba_sweep` (t0057), `minimal_dsgc_bar_locked_gaba_ampa_sweep` (t0059),
`dsgc_active_channel_pack` (t0074), `de_rosenroll_2026_dsgc_ais` (t0078), and
`de_rosenroll_2026_dsgc_ais_dendritic_spike` (t0080).

**Relevant libraries (2 of 19)** — both registered under `meta/asset_types/library/`. Note that the
library at `tasks/t0010_*/assets/library/` exists as a folder but is empty (no `details.json`); it
is not counted.

* `procedural_dsgc_morphology_generator` (t0090) — registered at
  `tasks/t0090_morphology_generator_diversity_test/assets/library/`. Entry points include
  `MorphologyParams` (frozen dataclass with the 14 morphology fields t0116 needs to reconstruct
  cells from the 68-d vector), `MorphologyResult` (with `h`, `soma`, `all_dends`,
  `section_endpoints_xy`, `origin_xy`), `BEDB_BASE_POINT`, and `PARAM_BOUNDS`. Import path:
  `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult`.
* `procedural_dsgc_morphology_generator_fix` (t0092) — registered at
  `tasks/t0092_diagnose_morphology_generator_silence/assets/library/`. Single entry point
  `generate_fixed_morphology(*, params, morph_seed=None)` is the canonical drop-in replacement for
  t0090's `generate_morphology` and is the project-standard build call used by t0109's gallery and
  the `scratch_t0112_top15_morphologies.py` precedent. Import path:
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.

These two libraries cover all morphology rendering needs (steps 3 representative-morph grids and
step 4 cluster representative rendering, both per the task description). No pandas / scikit-learn /
matplotlib code is registered as a library — the closest precedent is t0108's `code/` directory,
which must be copied per the cross-task-import rule.

## Key Findings

### Predictions schema differences across the four source seeds

All four `predictions/.../files/*.json(l).gz` payloads share the **same per-record schema** —
`generation` (int, 1-indexed), `vector_68d` (list[float], length 68), `objective_F_minimised`
(list[float]), `dsi_vector_sum` (float, stores ratio DSI on this lineage), `pd_rate_hz` (float). The
68-d vector layout is identical across all four seeds because all four runs are forks of t0106 that
did not touch the parameter ordering: indices 0..53 are the 54-d Bed B electrophys vector
(`ELECTROPHYS_PARAM_NAMES` in `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py`) and
indices 54..67 are the 14-d morphology vector (`MORPHOLOGY_PARAM_NAMES` in the same file).

The container format **differs in two ways**, both of which the loader must handle:

* **Wrapper**: t0106 [t0106] and t0112 [t0112] use gzipped JSON with a top-level
  `{"evaluations": [...]}` dict; t0114 [t0114] and t0115 [t0115] use gzipped JSONL (one record per
  line, no wrapper).
* **Per-record extras**: t0114 and t0115 carry two additional booleans `joint_pass` and `legit` that
  t0106 and t0112 do not. These can be safely ignored by t0116 because the filter
  `dsi_vector_sum > 0.7 ∧ pd_rate_hz > 10.0` is applied at the loader level on the raw fields, not
  on the post-hoc flags.

**Gen-0 caveat**: in all four files the lowest generation index is `1`, not `0`, and gen 1 contains
exactly 96 records (one per pop slot). The task description's "gen-0" overlay corresponds to
`generation == 1` records in these files — there is no `generation == 0` row. (t0106 separately
provides `results/data/init_pop_seed44.json` containing the raw 96×68 LHS-sampled matrix in pymoo
normalised space; the predictions-side `generation == 1` rows are the evaluated equivalents in real
parameter space.)

### Pipeline architecture inherited from t0108

t0108 [t0108] decomposes the analysis into five small modules under `code/`:

* `paths.py` (42 lines) — centralises every input / output `Path` constant.
* `constants.py` (111 lines) — owns the 54-d / 14-d parameter-name tuples, the k-sweep range
  (currently `K_SWEEP = (2, 3, 4)`), the Kaiser cap (`KAISER_FACTOR_CAP = 10`), the joint-factor
  threshold (`JOINT_FACTOR_R_THRESHOLD = 0.30`), and seeds. Both `ELECTROPHYS_PARAM_NAMES` (length
  54\) and `MORPHOLOGY_PARAM_NAMES` (length 14) are sealed with `assert len(...) == N_*_DIMS`
  guards. **This module is the authoritative source of the 68-d feature-name layout for the whole
  project.**
* `load_filter_cells.py` (138 lines) — single-source loader. The `FilteredCell` dataclass
  (`cell_index`, `source_task`, `source_seed`, `generation`, `dsi`, `pd_rate_hz`, `vector_68d`) is
  designed to extend naturally to a multi-seed pool by reusing the same record shape and varying
  `source_task` and `source_seed`.
* `cluster_helpers.py` (126 lines) — `zscore_matrix`, `run_pca`, `run_kmeans_sweep`,
  `top_k_loadings`, and `write_json` are the reusable analysis primitives. `run_kmeans_sweep`
  iterates `K_SWEEP` and picks the headline k by mean silhouette score (exactly the auto-pick rule
  t0116 needs in steps 3 and 4).
* `cluster_electrophys.py` (352 lines) and `cluster_morphology.py` (320 lines) — the two PCA +
  KMeans + Kruskal-Wallis subspaces with Bonferroni correction across {14, 54} features
  respectively.
* `factor_analysis.py` (362 lines) — Kaiser criterion + varimax rotation + factor-score / DSI / PD
  correlation. The `varimax_rotation` helper (lines 48-78) is a stand-alone iterative-SVD
  implementation that t0110 [t0110] also re-uses by direct import.

For t0116 the structural pattern carries over almost verbatim, but with three modifications listed
in **Recommendations for This Task** below.

### t0108 results that anchor methodology choices for t0116

t0108 [t0108] reports key headline numbers that t0116 should mirror in its own reporting cadence so
the analyses are directly comparable:

* Electrophys K-means picked **k = 2**, silhouette **0.496**, cluster sizes **10 / 140** — a small
  outlier vs bulk-cohort partition. Only 3 of 14 morphology parameters separated those clusters at
  Bonferroni p < 0.05.
* Morphology K-means picked **k = 4**, silhouette **0.233**, cluster sizes **21 / 55 / 67 / 7** —
  the richer of the two partitions. 30 of 54 electrophys parameters separated those clusters at
  Bonferroni p < 0.05; top discriminator was `NAV16_AIS_GBAR` (H = 58.7, p_bonf = 6.1×10⁻¹¹).
* Factor analysis retained **10 factors** (Kaiser cap of 10 was binding — 18 eigenvalues > 1). The
  joint DSI – PD trade-off factor was **F10** (|r_DSI| = 0.31, |r_PD| = 0.45).

t0116's expected k range is wider — `k ∈ [3, 7]` per the task description, vs t0108's
`K_SWEEP = (2, 3, 4)` — so the helper `K_SWEEP` constant must be widened.

### Truncated-cohort artefact diagnosed by t0110

t0110 [t0110] re-ran t0108's varimax pipeline on a relaxed cohort (DSI > 0.2 ∧ PD > 3 Hz, N = 247)
and showed that t0108's "all-negative PD column" was a **truncated-cohort artefact**: 2 of 10
factors had positive r(PD) at the relaxed threshold (vs 0/10 in the strict cohort), and the dominant
axis F1 was revealed as a joint suppressor (r_DSI = −0.37, r_PD = −0.75) rather than the PD-only
dropper t0108 reported.

For t0116 this matters because the task's filter (DSI > 0.7 ∧ PD > 10) is **even stricter** than
t0108's (DSI > 0.5 ∧ PD > 10). The analysis must therefore be alert to two failure modes: (a) the
factor-correlation sign pattern may saturate further; (b) the Kaiser cap of 10 may bind even more
tightly given the smaller sample-to-feature ratio. t0110 retained 16 eigenvalues > 1 in the relaxed
cohort (vs 18 in t0108's strict) — t0116 should report the same eigenvalue count to make the
methodological comparison legible.

### Morphology rendering precedent: scratch_t0112 vs t0109

The task description points at two morphology-rendering scripts. They differ in how they extract
dendrite geometry from `MorphologyResult`:

* `scratch_t0112_top15_morphologies.py` (root, untracked in worktree) uses
  `result.section_endpoints_xy` — a dict mapping section name to a 4-tuple `(x0, y0, x1, y1)`. This
  draws **straight line segments between section endpoints only**, which is fast but loses any
  intermediate `pt3d` curvature. The task description's "full dendrite trees" rule rejects this
  shortcut.
* `tasks/t0109_t0108_morph_cluster_gallery/code/build_cluster_gallery.py` [t0109] uses
  `result.h.x3d(i) / y3d(i) / diam3d(i)` over all `result.all_dends` sections — i.e., the full
  NEURON pt3d list per section. This reproduces full dendrite trees including curvature and diameter
  taper. Each panel renders dends as `ax.plot(xs, ys, ...)` per section with linewidth proportional
  to mean section diameter, soma as a `mpatches.Circle`, and a PD-arrow annotation in axes-fraction
  coords. Each `result.all_dends` section is explicitly deleted via `h.delete_section(sec=s)` after
  extraction (lines 153-154) to prevent NEURON memory creep when many cells are built in one
  process.

**t0116 must follow the t0109 approach**, not the scratch_t0112 approach, per the project preference
established by t0114's [t0114] morphology-grid backport and the memory note in
`feedback_top50_morphologies_full_dendrites.md`.

### Cluster representative selection rule

t0109's `_select_top_per_cluster` (lines 112-122 of `build_cluster_gallery.py`) is the canonical
implementation of the "top DSI × pd_rate_hz product within cluster" sampling rule that the t0116
task description names. The function takes a list of `CellRecord`s and an `n_per_cluster` integer
and returns a `dict[int, list[CellRecord]]` keyed by cluster id, with each list ranked descending by
`r.dsi * r.pd_rate_hz`. For t0116's `5×3 = 15` representative grids this becomes `n_per_cluster=15`.
The same rule must drive the 15-row representative tables in step 4.

### Multi-seed bookkeeping: keying records

None of the prior tasks pool across seeds. t0108 [t0108], t0109 [t0109], and t0110 [t0110] all use a
single source seed (t0106's seed 44), so their `FilteredCell` dataclasses only carry a single
`source_task` / `source_seed` value identical across every record. t0116 inverts this: each filtered
record must carry a unique `(source_task, seed, generation, individual_idx)` tuple, and analyses
must propagate the seed label through to every plot and table. Concretely:

* Standardisation (z-score) must be computed on the **union pool** (the task description spells this
  out under Verification Criteria), not per seed — otherwise PCA on the combined pool would mix two
  different parameter scales.
* Per-seed counts must be logged at three checkpoints: raw evaluation count, post-filter count,
  unique count after de-dup. t0108 reports this in `results_summary.md` as one row; t0116 reports it
  as a per-seed table.

The natural canonical store is a single Parquet file (`data/pooled_survivors.parquet`) with one row
per surviving cell and columns
`source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz` plus the 68 named vector
columns. Gen-0 individuals are stored separately in `data/pooled_gen0.parquet` because they will not
pass the cohort filter (most have DSI ≈ 0). The 68 vector columns must use the names from
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py:ALL_PARAM_NAMES` — that is the
project-canonical ordering and any deviation will silently break downstream cross-task
comparability.

### Why Parquet, not JSON

t0108's `filtered_cells.json` (the t0108 loader output for 150 cells) is ~300 KB. The pooled t0116
cohort will be smaller after filtering at DSI > 0.7 (per task scope: ~150 cells from t0106 alone at
DSI > 0.5, fewer at DSI > 0.7, totalling at most a few hundred across all four seeds), so JSON would
work. Parquet is recommended in the task description for downstream reproducibility (the file
becomes a stable input to potential follow-up tasks without needing to re-run the load / filter /
dedupe pipeline), and the pandas `to_parquet` round-trip with named columns is the cleanest path to
preserve dtypes for both `int` (generation, individual_idx) and `float64` (the 68 vector columns).

### Factor analysis Kaiser cut: correlation vs internal eigenvalues

The t0116 task description says: "retain factors with eigenvalue > 1 (use the eigenvalues of the
correlation matrix, not the FA's internal noise variances, for the Kaiser cut)." This is exactly
what t0108's `factor_analysis.py:run_factor_analysis` (lines 121-159) already does — it computes
`np.linalg.eigvalsh(np.cov(z_matrix, rowvar=False, ddof=0))` on the z-scored matrix to get
correlation-matrix eigenvalues, counts how many exceed 1.0, and caps at `KAISER_FACTOR_CAP = 10`.
The varimax rotation is applied to the truncated unrotated FA loadings, and rotated factor scores
are computed via the regression approximation `Z @ Λ @ pinv(Λ.T @ Λ)` (lines 146-148). For t0116 the
only change is feeding the function the pooled 68-d matrix instead of the single-seed matrix. The
Kaiser cap stays at 10 (t0116 task spec does not relax it).

## Reusable Code and Assets

### Import via library

* **`generate_fixed_morphology`** — Source: `tasks/t0092_diagnose_morphology_generator_silence/` via
  the registered `procedural_dsgc_morphology_generator_fix` library. Signature:
  `generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`.
  Use to rebuild each representative cell's NEURON morphology for the cluster-rep grids (step 3) and
  the morphology-cluster representative listing (step 4). Adaptation needed: none — same usage as
  t0109 line 148.

* **`MorphologyParams` / `MorphologyResult`** — Source:
  `tasks/t0090_morphology_generator_diversity_test/` via the registered
  `procedural_dsgc_morphology_generator` library. `MorphologyParams.from_dict(data=...)` is the
  serialisation entry point used by t0109 (line 131). Adaptation needed: t0116 must convert each
  cell's `vector_68d[54:68]` slice into a `dict[str, float | int]` keyed by `MORPHOLOGY_PARAM_NAMES`
  and pass it to `MorphologyParams.from_dict`. The three int-typed fields (`num_primary_branches`,
  `max_strahler_depth`, `morph_seed`) need `int(round(...))` coercion and `morph_seed` must be
  `% (2**31 - 1)` (per t0109 line 130) before the cast.

### Copy into task

The cross-task-import rule says all of these must be **copied** into
`tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/`, not imported. Total approximate copy
budget: ~600 lines from t0108 plus a new ~150-line multi-seed loader, plus a ~200-line morphology
gallery driver adapted from t0109.

* **`paths.py`** [t0108] — Source: `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/paths.py` (42
  lines). Defines every input / output `Path` constant. Adapt: rename `T0106_EVALUATIONS_GZ` to the
  four-source layout (`T0106_EVALS`, `T0112_EVALS`, `T0114_EVALS`, `T0115_EVALS` — each pointing at
  the right `assets/predictions/.../files/*.json(l).gz`); add the new figure paths
  `pca_combined.png`, `pca_with_gen0_overlay.png`, `electrophys_silhouette.png`,
  `electrophys_cluster_<k>_morphs.png`, `morphology_silhouette.png`, `factor_loadings_heatmap.png`;
  add `pooled_survivors.parquet` and `pooled_gen0.parquet` under `data/`.

* **`constants.py`** [t0108] — Source:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` (111 lines). Carries the
  authoritative `ELECTROPHYS_PARAM_NAMES` (54) and `MORPHOLOGY_PARAM_NAMES` (14) tuples,
  `N_ELECTROPHYS_DIMS = 54`, `N_MORPHOLOGY_DIMS = 14`, `N_TOTAL_DIMS = 68`,
  `KAISER_FACTOR_CAP = 10`, `JOINT_FACTOR_R_THRESHOLD = 0.30`, `DEDUP_DECIMALS = 6`. Adapt: change
  `DSI_THRESHOLD = 0.5` → `0.7`; widen `K_SWEEP = (2, 3, 4)` → `(3, 4, 5, 6, 7)`; add four-seed
  sources tuple e.g.
  `SOURCES: tuple[tuple[str, int], ...] = (("t0106_long_pdnd_nsga2_300gen", 44), ("t0112_t0106_seed77_replicate", 77), ("t0114_seed7755_no_autostop", 7755), ("t0115_seed9354_no_autostop", 9354))`.
  The `SOURCE_TASK` / `SOURCE_SEED` scalar constants must be removed and replaced by per-record
  fields.

* **`cluster_helpers.py`** [t0108] — Source:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/cluster_helpers.py` (126 lines). Provides
  `PCAResult`, `KMeansResult`, `KMeansSweepResult` dataclasses and `zscore_matrix`, `run_pca`,
  `run_kmeans_sweep`, `top_k_loadings`, `write_json`. Adapt: none in the dataclasses or
  `run_kmeans_sweep` logic — the function already auto-picks by silhouette across `K_SWEEP`, so it
  will respect the widened tuple automatically.

* **`load_filter_cells.py`** [t0108] — Source:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/load_filter_cells.py` (138 lines). Carries the
  `FilteredCell` dataclass and the dedupe-by-rounded-vector logic. Adapt heavily: iterate four
  sources instead of one; handle both the t0106/t0112 JSON-wrapper format and the t0114/t0115 JSONL
  format (branch on `path.suffixes` or sniff the first decoded character); attach per-record
  `source_task` and `seed` from the iteration variable; serialise to Parquet not JSON; emit the
  per-seed before/after-filter / after-dedupe report into `results_detailed.md`. **Estimate ~150
  lines after adaptation.**

* **`factor_analysis.py`** [t0108] — Source:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/factor_analysis.py` (362 lines). The
  `varimax_rotation` helper (lines 48-78) and `run_factor_analysis` (lines 121-159) carry over
  verbatim. Adapt: keep `KAISER_FACTOR_CAP = 10`; replace the t0108-specific loader with the
  pooled-Parquet loader; the t0116 task spec uses **symmetric vmin/vmax** for the heatmap
  (`vmin=-vmax`) which t0108's `_plot_loadings_heatmap` already does at line 243.

* **`cluster_electrophys.py`** [t0108] — Source:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/cluster_electrophys.py` (352 lines). Adapt:
  replace per-cluster morphology-overlay boxplots (lines 201-252) with the t0116-specific 5×3
  representative-morphology grids per cluster (using the t0109 dendrite-extraction pattern).
  Standardisation is computed on the union electrophys submatrix (no per-seed split). Keep the
  silhouette curve and PCA-by-cluster scatter. The chosen k is now in [3, 7] not [2, 4]. **Estimate
  ~400 lines after adaptation.**

* **`cluster_morphology.py`** [t0108] — Source:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/cluster_morphology.py` (320 lines). Adapt:
  replace the per-cluster electrophys-overlay boxplots with the t0116-specific 15-row representative
  tables (`source_task, seed, generation, dsi_vector_sum, pd_rate_hz`, ePhys PC1/PC2/PC3 loadings on
  the 54-d electrophys PCA fitted in step 1). Same k ∈ [3, 7] silhouette sweep. **Estimate ~300
  lines after adaptation.**

* **`build_cluster_gallery.py`** [t0109] — Source:
  `tasks/t0109_t0108_morph_cluster_gallery/code/build_cluster_gallery.py` (336 lines). Provides the
  canonical `_select_top_per_cluster` (lines 112-122), `_to_morph_params` (lines 125-131),
  `_extract_section_pts` (lines 134-144), `_build_and_extract` (lines 147-155), `_global_extents`
  (lines 158-175), and `_plot_cell` (lines 178-222) helpers. Adapt: change the cluster-source from
  t0108's `morphology_clusters.json` to t0116's in-memory cluster-label arrays; change the per-panel
  annotation to include `source_task` and `seed` per the t0116 task spec; render a 5×3 grid (15
  cells) per cluster instead of one 4×10 grid for all clusters at once. **Estimate ~250 lines after
  adaptation across two separate scripts — one for electrophys clusters' morph grids (step 3) and
  one for the morphology-cluster representative tables (step 4, which does not need morphology
  rendering, only a Markdown / CSV table).**

### New code for t0116 (not copied)

* **Pooled-PCA-with-overlay driver** — ~150 lines new. Loads `pooled_survivors.parquet` and
  `pooled_gen0.parquet`, fits the standardiser on the union pool, fits combined 68-d / 54-d / 14-d
  PCAs, renders the three-panel `pca_combined.png` with seed-coloured filled circles, then refits
  the gen-0 cells against the **same** standardiser and PCA (no refit) for
  `pca_with_gen0_overlay. png`. Tabulates per-seed mean Euclidean displacement (PC1+PC2 space and
  68-d standardised space) into `results_detailed.md`.

* **Per-seed cohort-count table generator** — ~30 lines new. Writes one row per seed with
  `n_raw, n_passing_filter, n_unique` after the load + filter + dedupe pipeline; emits both a CSV
  under `results/data/` and a Markdown table in `results_detailed.md`.

## Lessons Learned

* **Strict cohorts produce truncated-correlation artefacts** [t0110]. t0108's all-negative PD column
  was a strict-cohort artefact, not a fundamental substrate property. t0116's even stricter filter
  (DSI > 0.7 vs t0108's > 0.5) is at risk of more severe saturation — every claim about factor signs
  in t0116 should be made conditional on the cohort, and the answer asset for Q3 should explicitly
  note this.

* **NEURON memory creep when building many cells in one process** [t0109]. t0109's
  `build_cluster_gallery.py:_build_and_extract` (lines 152-154) explicitly deletes each section via
  `h.delete_section(sec=s)` after extraction. Skipping this step causes the process RSS to climb
  monotonically as more cells are rendered. t0116 will build at minimum `K_max × 15 = 7 × 15 = 105`
  morphologies in one process (likely more across both cluster partitions), so this hygiene step is
  mandatory.

* **`morph_seed` needs the `% (2**31 - 1)` coercion** [t0109 line 130]. The 14-d morphology vector
  carries `morph_seed` as a float in `vector_68d[66]`. Casting straight to `int(...)` can produce
  out-of-range integers if the GA mutated the seed beyond `INT32_MAX`. t0109 modulos it down before
  constructing `MorphologyParams`.

* **All four predictions files are 1-indexed for `generation`** — confirmed empirically by counting
  records per generation across all four files. Gen 1 has exactly 96 records (= pop size) in every
  file, so it is the random-init pop. Any code that assumes a `generation == 0` row will silently
  get no records.

* **Boolean container schema differences are easy to miss** — t0114 and t0115 carry `joint_pass` and
  `legit` booleans that t0106 and t0112 do not. A loader that does `record["joint_pass"]`
  unconditionally will `KeyError` on t0106/t0112. Use `.get(...)` or filter on the canonical fields
  `dsi_vector_sum` and `pd_rate_hz` (which exist in all four).

* **t0108's K_SWEEP was narrow at (2, 3, 4)** [t0108]. Both partitions picked the smallest k
  (electrophys: 2; morphology: 4). This may have been a sweep-range artefact rather than a genuine
  preference. t0116's task spec explicitly broadens to k ∈ [3, 7], which will tell us whether the
  cohort actually wants more clusters.

* **Standardisation must be computed on the union pool, not per-seed**
  [task description's Verification Criteria]. This is the multi-seed analogue of t0108's "z-score
  before clustering" rule, but the failure mode here is silent: per-seed z-scoring would absorb the
  cross-seed scale differences into the standardiser and zero out the very signal the analysis aims
  to detect.

* **t0106 / t0112 use JSON-wrapped, t0114 / t0115 use JSONL**. The format drift happened between
  t0112 and t0114; the loader must branch on the file extension (`.jsonl.gz` vs `.json.gz`) and
  cannot assume a single decode path. This is the single biggest code-level adaptation the t0116
  loader must make vs t0108's load_filter_cells.py.

## Recommendations for This Task

1. **Adopt t0108's module layout verbatim** for `paths.py`, `constants.py`, `cluster_helpers.py`,
   and `factor_analysis.py`. Copy the files into `tasks/t0116_*/code/`, replace each
   `tasks. t0108_*` import with `tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10`, and apply three
   targeted constant patches: `DSI_THRESHOLD: 0.5 → 0.7`; `K_SWEEP: (2, 3, 4) → (3, 4, 5, 6, 7)`;
   replace `SOURCE_TASK` / `SOURCE_SEED` scalars with the `SOURCES` four-tuple of
   `(source_task, seed)` pairs.

2. **Write a new multi-format loader** (`code/load_pooled_cells.py`, ~150 lines) that handles both
   the t0106/t0112 JSON-wrapper format and the t0114/t0115 JSONL format by branching on
   `path.suffixes` (`['.jsonl', '.gz']` vs `['.json', '.gz']`). The loader iterates the four
   `(source_task, seed, predictions_path)` triples, applies the filter
   `dsi_vector_sum > 0.7 ∧ pd_rate_hz > 10.0`, dedupes by rounded 68-d vector at
   `DEDUP_DECIMALS = 6` (t0108 convention), writes `data/pooled_survivors.parquet`, and emits a
   per-seed before / after-filter / after-dedupe count table.

3. **Write a separate gen-0 loader** (`code/load_pooled_gen0.py`, ~80 lines) that re-uses the same
   format-branching logic but with the filter `generation == 1`. Writes `data/pooled_gen0.parquet`.
   The displacement-from-init analysis (step 2) uses the survivor pool and the gen-0 pool together.

4. **Fit the standardiser and PCAs on the union pool, never per-seed**. Per the task's Verification
   Criteria. This is the single hardest invariant to check by inspection; encode it as a function
   `fit_pooled_standardiser(matrix)` and reference the returned `mean`/`std` arrays throughout —
   never instantiate a new StandardScaler inside any per-seed loop.

5. **Use t0109's NEURON build path for morphology rendering**, not the
   `scratch_t0112_top15_morphologies.py` endpoint shortcut. Copy `_extract_section_pts`,
   `_build_and_extract`, `_global_extents`, and `_plot_cell` from
   `tasks/t0109_t0108_morph_cluster_gallery/code/build_cluster_gallery.py` lines 134-222 into a new
   `code/morphology_rendering.py` module, including the `h.delete_section(sec=s)` cleanup at lines
   153-154. Pass `morph_seed` through the `% (2**31 - 1)` modulo before the `int()` cast.

6. **Apply the t0109 cluster-representative rule** (`_select_top_per_cluster` lines 112-122): rank
   by descending `r.dsi * r.pd_rate_hz` within cluster and take the top 15. Per the task description
   this rule applies to both the electrophys clusters' morph-grid step (step 3) and the morphology
   clusters' representative-table step (step 4).

7. **Re-use the t0108 varimax + Kaiser FA pipeline verbatim** (`factor_analysis.py`
   `varimax_rotation` and `run_factor_analysis`). Confirm the Kaiser cut uses correlation-matrix
   eigenvalues (it already does — line 129 `np.linalg.eigvalsh(corr)`), not FA's internal noise
   variances. Keep `KAISER_FACTOR_CAP = 10`. Use the symmetric `vmin=-vmax` heatmap render (already
   in `_plot_loadings_heatmap` line 243).

8. **Embed seed labels in every plot and table** — every PCA scatter, every cluster gallery, every
   representative table, and every cohort-count summary must carry the `source_task` / `seed`
   columns. Use the same 4-colour palette across the entire task for the four seeds to make
   cross-figure comparison easier (e.g., `tab10[0..3]` with a small legend).

9. **Compute cluster purity by seed** via normalised mutual information (NMI) or chi-square between
   cluster label and seed label. The task description names both, and
   `sklearn.metrics. normalized_mutual_info_score(labels_true=seeds, labels_pred=clusters)` is the
   canonical one-liner. Report NMI per partition (electrophys k and morphology k) in
   `results_detailed.md`.

10. **Document the schema variance up-front** in `results_detailed.md` Methodology section: state
    that t0106/t0112 use JSON-wrapped predictions while t0114/t0115 use JSONL, that all four share
    the same per-record schema, that `generation == 1` is the random init in all four files, and
    that the `joint_pass` / `legit` booleans in t0114/t0115 are ignored in favour of the canonical
    `dsi_vector_sum > 0.7 ∧ pd_rate_hz > 10.0` filter applied on the raw fields.

## Task Index

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Morphology generator diversity test
* **Status**: completed
* **Relevance**: Producer of the registered `procedural_dsgc_morphology_generator` library that owns
  `MorphologyParams` and `MorphologyResult`. t0116 imports these classes to reconstruct cells from
  the 68-d vector's morphology slice.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology-generator silence
* **Status**: completed
* **Relevance**: Producer of the registered `procedural_dsgc_morphology_generator_fix` library that
  owns `generate_fixed_morphology` — the canonical drop-in replacement for t0090's
  `generate_morphology`. t0116 imports this entry point to build each representative cell.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long 2-direction NSGA-II at 300 gens, 1 seed, 3 trials (ratio DSI + PD-rate)
* **Status**: completed
* **Relevance**: First of the four source NSGA-II runs that t0116 pools. Source seed 44, predictions
  at `assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`
  (JSON wrapper format, 3744 evaluations).

### [t0108]

* **Task ID**: `t0108_t0106_cluster_factor_dsi05_pd10`
* **Name**: Cluster + factor analysis of t0106 cells at DSI>0.5 AND PD>10
* **Status**: completed
* **Relevance**: The single-seed methodology precedent. t0116 inherits its module layout
  (paths/constants/load_filter/cluster_helpers/cluster_electrophys/cluster_morphology/factor_
  analysis), the 68-d feature-name layout in `constants.py`, the varimax + Kaiser FA pipeline, and
  the silhouette-pick KMeans helper.

### [t0109]

* **Task ID**: `t0109_t0108_morph_cluster_gallery`
* **Name**: Morphology gallery (10 per cluster) for the four t0108 morphology clusters
* **Status**: completed
* **Relevance**: Provides the full-dendrite NEURON pt3d extraction path (`_build_and_extract`,
  `_extract_section_pts`), the cluster-representative ranking rule (`_select_top_per_cluster`,
  descending `dsi * pd_rate_hz` within cluster), and the morph-seed `% (2**31 - 1)` coercion. All of
  these carry into t0116.

### [t0110]

* **Task ID**: `t0110_relaxed_cohort_factor_analysis`
* **Name**: Factor analysis at relaxed cohort (DSI > 0.2 AND PD > 3)
* **Status**: completed
* **Relevance**: Diagnoses the truncated-cohort artefact in t0108's strict-cohort factor signs and
  re-uses t0108's `varimax_rotation` by direct import. Warns t0116 that its even stricter filter
  (DSI > 0.7) may exhibit further saturation in factor-sign patterns.

### [t0112]

* **Task ID**: `t0112_t0106_seed77_replicate`
* **Name**: Seed-77 minimum-change replicate of t0106 long 2-direction NSGA-II
* **Status**: completed
* **Relevance**: Second of the four source NSGA-II runs. Source seed 77, predictions at
  `assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz` (JSON
  wrapper format, 2016 evaluations). 7 LEGIT joint-pass cells — the sparsest seed in the four-source
  pool.

### [t0114]

* **Task ID**: `t0114_seed7755_no_autostop`
* **Name**: Seed-7755 NSGA-II replicate of t0106 with auto-stop disabled
* **Status**: completed
* **Relevance**: Third source run. Source seed 7755, predictions at
  `assets/predictions/t0114-bedb-morph-nsga2-seed7755/files/predictions.jsonl.gz` (JSONL format —
  first run to use this format, 5952 evaluations). 484 LEGIT joint-pass cells — the densest seed in
  the four-source pool. Established the project's full-dendrite morphology- grid backport
  convention.

### [t0115]

* **Task ID**: `t0115_seed9354_no_autostop`
* **Name**: Seed-9354 NSGA-II replicate of t0106 with auto-stop disabled
* **Status**: completed
* **Relevance**: Fourth source run. Source seed 9354, predictions at
  `assets/predictions/t0115-bedb-morph-nsga2-seed9354/files/predictions.jsonl.gz` (JSONL format,
  5280 evaluations). 63 LEGIT joint-pass cells — intermediate density between t0112 and t0114.
