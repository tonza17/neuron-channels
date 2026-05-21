---
spec_version: "2"
task_id: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
date_completed: "2026-05-21"
status: "complete"
---
# t0116 — Pooled PCA + Cluster + Factor Analysis (DSI > 0.7 ∧ PD > 10) Plan

## Objective

Pool every NSGA-II survivor cell with `dsi_vector_sum > 0.7` AND `pd_rate_hz > 10.0` across four
seeds (t0106 seed 44, t0112 seed 77, t0114 seed 7755, t0115 seed 9354) into a single labelled cohort
keyed by `(source_task, seed, generation, individual_idx)`, then run PCA + KMeans on the 54-d
electrophys subspace, PCA + KMeans on the 14-d morphology subspace, varimax factor analysis on the
full 68-d feature vector, and a gen-0-random-init overlay to quantify how far NSGA-II travelled from
its random initialisation. Produce six charts, several CSV tables, and three answer assets covering
(Q1) cross-seed basin connectivity, (Q2) displacement from random init, and (Q3) latent factor
drivers of joint DSI / PD-rate quality. Done = all charts on disk, three answer assets passing
`verify_answer_asset`, and the pooled cohort persisted as Parquet for reproducibility.

## Task Requirement Checklist

Operative task text from `task.json` (`short_description`) and `task_description.md`:

> **Name**: Pooled PCA + cluster + factor analysis of DSI>0.7 / PD>10 cells across 4 seeds
>
> **Short description**: Pool DSI>0.7 ∧ PD>10 Hz cells from t0106 (s44), t0112 (s77), t0114
> (s7755), t0115 (s9354); PCA + KMeans on electrophys (54-d) and morphology (14-d) subspaces +
> factor analysis on the full 68-d vector.
>
> Filter: `dsi_vector_sum > 0.7` AND `pd_rate_hz > 10.0`, both strict. Record per-seed counts before
> and after the filter and report them in `results_detailed.md`.
>
> Analyses to run: (1) Combined 68-d PCA + side panels (one figure, three subplots — combined,
> electrophys-only, morphology-only); (2) Gen-0 random-init overlay on the same PCA axes plus
> per-seed mean Euclidean displacement in PC1+PC2 space; (3) KMeans on 54-d electrophys subspace,
> auto-pick `k ∈ [3, 7]` by silhouette, with 5×3 grids of full-dendrite morphologies per cluster;
> (4) KMeans on 14-d morphology subspace, auto-pick `k ∈ [3, 7]` by silhouette, with a 15-row
> representative table per cluster including
> `(source_task, seed, generation, dsi_vector_sum, pd_rate_hz, ePhys PC1, ePhys PC2, ePhys PC3)`;
> (5) Factor analysis on the full 68-d feature matrix with Kaiser criterion (correlation-matrix
> eigenvalues, not FA noise variances) and varimax rotation, loadings heatmap on `RdBu_r` with
> symmetric vmin/vmax.
>
> Three answer assets: Q1 cross-seed basin connectivity (evidence: PCA overlap, KMeans purity by
> seed via chi-square or NMI); Q2 displacement from random init (evidence: per-seed mean and
> 95th-percentile Euclidean displacement in 68-d standardised space and PC1+PC2 space, compared
> against gen-0 within-seed spread); Q3 latent drivers of joint-pass quality (evidence: factor
> loadings heatmap + per-factor Pearson r with DSI and PD).
>
> Verification: `pooled_survivors.parquet` row count equals the sum of per-seed survivor counts;
> standardiser is fitted on the union pool (not per-seed); every chart referenced in
> `results_detailed.md` exists on disk; every claim in the three answer assets is grounded in a
> specific table or chart.

* **REQ-1**: Load every evaluation record from the four source predictions paths listed in
  `task_description.md` (`tasks/t0106_long_pdnd_nsga2_300gen/.../all_evaluations_seed44.json.gz`,
  `tasks/t0112_t0106_seed77_replicate/.../all_evaluations_seed77.json.gz`,
  `tasks/t0114_seed7755_no_autostop/.../predictions.jsonl.gz`,
  `tasks/t0115_seed9354_no_autostop/.../predictions.jsonl.gz`). Handle both container shapes: t0106
  / t0112 use a gzipped JSON wrapper `{"evaluations": [...]}`, while t0114 / t0115 use gzipped JSONL
  (one record per line). Branch on `path.suffixes` to pick the right decoder. Ignore the optional
  `joint_pass` / `legit` booleans on t0114 / t0115 records. *Satisfied by Step 2.*

* **REQ-2**: Apply the cohort filter `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` (both strict
  inequalities) and dedupe by the 68-d vector rounded to 6 decimals (project convention from t0108).
  Record per-seed `n_raw`, `n_passing_filter`, and `n_unique` and emit them as a CSV plus Markdown
  table. *Satisfied by Step 2 and Step 3.*

* **REQ-3**: Persist the pooled survivor cohort to
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/data/pooled_survivors.parquet` keyed by
  `(source_task, seed, generation, individual_idx)` with `dsi_vector_sum`, `pd_rate_hz`, and the 68
  named vector columns from `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py`
  `ALL_PARAM_NAMES`. The Parquet row count must equal the sum of per-seed survivor counts.
  *Satisfied by Step 2.*

* **REQ-4**: Load the gen-0 random-init pool by filtering `generation == 1` (1-indexed in all four
  files; gen 1 contains exactly 96 records per seed = pop slot count). Persist to
  `data/pooled_gen0.parquet` with the same column schema as `pooled_survivors.parquet`. *Satisfied
  by Step 3.*

* **REQ-5**: Standardise the 68-d feature matrix on the **union pool** (not per-seed). The same
  standardiser must be fitted once and reused for every downstream PCA, KMeans, FA, and gen-0
  projection. Encode the fit as `fit_pooled_standardiser(matrix)` and reference the returned
  `mean`/`std` everywhere. *Satisfied by Step 4 and propagated through Steps 5-9.*

* **REQ-6**: Fit three PCAs on the standardised union pool — full 68-d, 54-d electrophys-only
  (vector columns 0-53 of `ALL_PARAM_NAMES`), and 14-d morphology-only (columns 54-67). For each
  PCA, retain PC1 and PC2 with `% variance explained`. Render `results/images/pca_combined.png` as a
  1×3 figure: main panel (combined 68-d PC1 vs PC2), side panel A (electrophys-only PC1 vs PC2),
  side panel B (morphology-only PC1 vs PC2). Colour every point by `seed` using a fixed 4-colour
  palette (the first four of `matplotlib.cm.tab10`); use filled circles for all points (every
  retained cell is joint-pass by construction). Each subplot's axis labels must contain the
  `% variance explained` for PC1 and PC2. *Satisfied by Step 5.*

* **REQ-7**: Project the gen-0 individuals onto the **same three PCAs fitted in Step 5** (no refit;
  reuse the standardiser too). Render `results/images/pca_with_gen0_overlay.png` as the same 1×3
  figure with faint grey crosses (`x` marker, `alpha=0.3`) for gen-0 cells underneath the survivor
  scatter. Compute per-seed mean Euclidean displacement in (a) PC1+PC2 space of the combined 68-d
  PCA, and (b) the full 68-d standardised space (survivors vs gen-0 mean for the same seed) plus
  per-seed 95th-percentile displacements. Emit as `results/data/gen0_displacement.csv` for
  downstream reporting consumption. *Satisfied by Step 6.*

* **REQ-8**: KMeans on the standardised 54-d electrophys subspace. Sweep `k ∈ {3, 4, 5, 6, 7}` and
  pick the headline `k` by maximum mean silhouette score (`sklearn.metrics.silhouette_score`). Emit
  `results/images/electrophys_silhouette.png` (k on x-axis, mean silhouette on y-axis with every
  candidate k marked). Emit per-cluster CSV `results/data/electrophys_clusters.csv` containing
  `cluster_id, source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, pc1_combined, pc2_combined`.
  *Satisfied by Step 7.*

* **REQ-9**: For each electrophys cluster, render a 5×3 grid of full dendrite trees for 15
  representative cells. Representatives ranked descending by `dsi * pd_rate_hz` within cluster
  (canonical rule from `tasks/t0109_t0108_morph_cluster_gallery/code/build_cluster_gallery.py`
  `_select_top_per_cluster`, lines 112-122). Use the NEURON pt3d extraction path (`h.x3d(i)`,
  `h.y3d(i)`, `h.diam3d(i)` over `result.all_dends`), not the endpoint shortcut — full dendrite
  trees per the project preference established by t0114's morphology-grid backport. Each panel must
  annotate `source_task`, `seed`, `gen`, `DSI`, `PD` so cross-seed identity is visible. Emit one PNG
  per cluster as `results/images/electrophys_cluster_<k>_morphs.png`. *Satisfied by Step 8.*

* **REQ-10**: KMeans on the standardised 14-d morphology subspace. Same `k ∈ {3, 4, 5, 6, 7}`
  silhouette auto-pick. Emit `results/images/morphology_silhouette.png` and
  `results/data/morphology_clusters.csv` with the same column layout as Step 7. *Satisfied by Step
  9.*

* **REQ-11**: For each morphology cluster, write a 15-row representative listing — descending
  ranking by `dsi * pd_rate_hz` — with columns
  `source_task, seed, generation, dsi_vector_sum, pd_rate_hz, ephys_pc1, ephys_pc2, ephys_pc3`. The
  `ephys_pc1/2/3` values come from the 54-d electrophys PCA fitted in Step 5 (project the cell's
  electrophys row onto the first three PCs). Emit
  `results/data/morphology_cluster_<k>_representatives.csv` for downstream reporting consumption.
  *Satisfied by Step 9.*

* **REQ-12**: Factor analysis on the full standardised 68-d matrix. Procedure: (a) Fit
  `sklearn.decomposition.FactorAnalysis(n_components=68)`; (b) Compute correlation-matrix
  eigenvalues via `np.linalg.eigvalsh(np.cov(z_matrix, rowvar=False, ddof=0))`; count
  `n_eig_above_one` factors that satisfy Kaiser; cap at the project constant
  `KAISER_FACTOR_CAP = 10` (inherited from t0108); (c) Refit FA with
  `n_components = min(n_eig_above_one, KAISER_FACTOR_CAP)`; (d) Apply varimax rotation via the
  iterative-SVD `varimax_rotation` helper from
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/factor_analysis.py` lines 48-78; (e) Compute
  rotated factor scores via the regression approximation `Z @ Λ @ pinv(Λ.T @ Λ)`; (f) Render
  `results/images/factor_loadings_heatmap.png` as factors × 68 features, `RdBu_r` colourmap,
  `vmin = -vmax` where `vmax = max(|loadings|)`, feature names on y-axis from `ALL_PARAM_NAMES`.
  *Satisfied by Step 10.*

* **REQ-13**: Report per-factor variance explained, total variance explained, and Pearson r between
  each rotated factor score and `dsi_vector_sum` / `pd_rate_hz`. Emit as
  `results/data/factor_correlations.csv` for downstream reporting consumption. *Satisfied by Step
  10.*

* **REQ-14**: Compute KMeans cluster-vs-seed purity for both partitions (electrophys-k and
  morphology-k). Report both normalised mutual information
  (`sklearn.metrics.normalized_mutual_info_score(labels_true=seeds, labels_pred=clusters)`) and a
  chi-square contingency test (`scipy.stats.chi2_contingency`) on the cluster × seed crosstab. Emit
  as `results/data/cluster_seed_purity.csv`. *Satisfied by Step 11.*

* **REQ-15**: Produce three answer assets under `assets/answer/<answer_id>/` following
  `meta/asset_types/answer/specification.md`. The three answer IDs and questions are:
  * `pooled-survivors-basin-connectivity-dsi07-pd10` — Q1 cross-seed basin connectivity;
  * `pooled-survivors-displacement-from-init-dsi07-pd10` — Q2 displacement from random init;
  * `pooled-survivors-latent-drivers-dsi07-pd10` — Q3 latent factor drivers. Each canonical short
    answer must be 2-5 sentences, citation-free in the `## Answer` / `## Short Answer` sections,
    with all citations in `## Sources`. Each full answer asset must cite the specific chart and CSV
    files produced by Steps 5-11. *Satisfied by Step 12.*

* **REQ-16**: Every chart in `results/images/` must be embedded by the downstream reporting stage
  via `![desc](images/file.png)` syntax. This embedding is performed by the orchestrator-managed
  reporting stage and is not part of the implementation Step by Step below; the implementation must,
  however, produce every PNG on disk before reporting can succeed. *Satisfied via the orchestrator
  reporting step which consumes the artefacts produced by Steps 5-11.*

* **REQ-17**: Document up-front the schema variance across the four sources (t0106/t0112
  JSON-wrapped vs t0114/t0115 JSONL; gen 1 = random init in all four; `joint_pass` / `legit`
  booleans ignored). The implementation must emit a Methodology block as
  `results/data/methodology_notes.md` for the reporting stage to consume when assembling the
  downstream report. *Satisfied by Step 13.*

## Approach

This task is a multi-seed extension of t0108's single-seed clustering / factor-analysis pipeline.
The diff is small and well-isolated: load from four sources instead of one, carry seed labels
through every downstream artefact, and widen the KMeans silhouette sweep from `k ∈ {2, 3, 4}` to
`k ∈ {3, 4, 5, 6, 7}` per the task description. The 68-d feature layout is identical across all
four seeds because all four are forks of t0106 that did not touch the parameter ordering — indices
0-53 are the 54-d Bed-B electrophys vector (`ELECTROPHYS_PARAM_NAMES`) and 54-67 are the 14-d
morphology vector (`MORPHOLOGY_PARAM_NAMES`), both authoritatively defined in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py`.

**Module layout adopted from t0108**: `paths.py` (path constants), `constants.py` (the 68 feature
names, k-sweep range, `KAISER_FACTOR_CAP = 10`, `DSI_THRESHOLD = 0.7`, `DEDUP_DECIMALS = 6`,
`SOURCES` four-tuple), `cluster_helpers.py` (`zscore_matrix`, `run_pca`, `run_kmeans_sweep`,
`top_k_loadings`), `factor_analysis.py` (`varimax_rotation`, `run_factor_analysis`),
`cluster_electrophys.py` and `cluster_morphology.py` (the two subspace clustering drivers). **New
for t0116**: `load_pooled_cells.py` (multi-seed, multi-format loader handling both JSON wrapper and
JSONL containers), `load_pooled_gen0.py` (gen-0 random-init loader), `morphology_rendering.py`
(copied verbatim from t0109's `_build_and_extract`, `_extract_section_pts`, `_global_extents`,
`_plot_cell` helpers — full dendrite trees via NEURON pt3d, with `h.delete_section(sec=s)` cleanup
mandatory to prevent NEURON RSS creep when building ~100+ cells in one process), and
`pooled_pca_with_overlay.py` (the new three-panel PCA + gen-0 overlay driver).

**Key research findings driving the approach**:

* **Container format drift** (`research_code.md`): t0106 and t0112 use gzipped JSON with a top-level
  `{"evaluations": [...]}` wrapper; t0114 and t0115 use gzipped JSONL (one record per line). All
  four share the same per-record schema. The loader must branch on `path.suffixes`
  (`['.jsonl', '.gz']` vs `['.json', '.gz']`) and cannot assume a single decode path.

* **Gen-0 ≡ generation == 1** (`research_code.md`): all four files are 1-indexed; gen 1 contains
  exactly 96 records (one per pop slot) and is the random init. There is no `generation == 0` row;
  any code that assumes one will silently produce no records.

* **Standardisation on union pool, not per-seed** (`research_code.md` and task verification
  criteria): per-seed z-scoring would absorb cross-seed scale differences into the standardiser and
  erase the very signal the analysis is designed to detect. Encode the fit once and propagate the
  returned mean / std everywhere.

* **NEURON memory creep** (`research_code.md`, t0109 lines 152-154): t0109 explicitly calls
  `h.delete_section(sec=s)` on each `result.all_dends` section after extraction. Skipping this
  causes monotonic RSS growth as more morphologies are rendered. t0116 will build at minimum
  `K_max × 15 = 7 × 15 = 105` morphologies in one process (more across both partitions), so this
  hygiene step is mandatory.

* **`morph_seed` overflow** (`research_code.md`, t0109 line 130): the morphology vector carries
  `morph_seed` as a float. Cast as `int(round(x)) % (2**31 - 1)` before constructing
  `MorphologyParams` to avoid out-of-range integers if the GA mutated the seed beyond INT32_MAX.

* **Truncated-cohort artefact** (`research_code.md` re: t0110): t0108's strict cohort (DSI > 0.5)
  produced all-negative PD correlations in every factor — a strict-cohort artefact, not a
  fundamental property. t0116's even stricter filter (DSI > 0.7) may exhibit further saturation; the
  answer asset for Q3 must condition its claims on the cohort.

**Alternatives considered (rejected)**:

* *Per-seed PCAs with Procrustes alignment instead of union-pool PCA.* Rejected because the task
  explicitly requires a pool-level standardiser; aligning four separate PCAs adds methodological
  complexity without answering the "is this one basin or several?" question more cleanly than union
  PCA already does.
* *Including t0113 (seed 2247) for a five-seed pool.* Rejected as out-of-scope for this first cut
  per the task description; t0113 uses an earlier autostop / pool-restart configuration. Can be
  added via a downstream correction task if four-seed coverage proves insufficient.
* *Endpoint-only morphology rendering via `scratch_t0112_top15_morphologies.py`.* Rejected because
  the project preference (memory note `feedback_top50_morphologies_full_dendrites.md`) explicitly
  requires full dendrite trees, not just somas / endpoint segments.

**Task types (`task.json` declares `data-analysis`, `comparative-analysis`, `answer-question`)**.
All three apply: the load + PCA + KMeans + FA pipeline is a data-analysis workflow; the cross-seed
comparison (basin connectivity, displacement, factor drivers) is a comparative analysis; and the
three deliverables are answer assets. Per the data-analysis Planning Guidelines, every chart type is
named up-front; per the comparative-analysis guidelines, the comparison axis (seed) and significance
test (chi-square on cluster × seed contingency, plus NMI) are decided here; per the answer-question
guidelines, three explicit `answer_id` slugs are listed above and each cites concrete chart / CSV
evidence.

**Registered metrics applicability**. The four registered metrics (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) all describe per-cell DSI
/ tuning measurements taken during a NEURON simulation. t0116 does no new simulations — it pools
and analyses pre-computed `dsi_vector_sum` and `pd_rate_hz` values from frozen predictions assets.
None of the registered metrics correspond to the unsupervised summaries this task produces
(silhouette scores, % variance explained, NMI, Euclidean displacement). The implementation will
therefore not write any registered metric keys into `results/metrics.json`. This omission is
deliberate, not accidental, and is documented in `results/data/methodology_notes.md` for the
reporting stage to mirror.

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Local CPU compute (load + standardise + 3 PCAs + 2 KMeans sweeps + FA + 100+ NEURON cell builds + matplotlib rendering on a single laptop CPU) | ~30 minutes wall clock |
| Paid API calls (OpenAI, Anthropic, etc.) | $0 — no LLM calls in the pipeline |
| Remote GPU compute (Vast.ai, RunPod) | $0 — no remote machine provisioned |
| Storage / egress | $0 — local Parquet + PNG only |
| **Predicted spend** | **$0** |
| **Hard cap** | **$0** (well under the per-task default limit of $8 from `project/budget.json`) |

All four source predictions files are already present locally in the dependency task folders (t0106,
t0112, t0114, t0115). No external downloads are required; no paid services are touched.

## Step by Step

Implementation work only — load → pool → PCA → KMeans → morph grids → factor analysis
→ answer assets. The reporting / suggestions / compare-literature stages are managed by the
orchestrator after this implementation finishes.

1. **Set up the module skeleton.** Create `code/paths.py`, `code/constants.py`,
   `code/cluster_helpers.py`, and `code/factor_analysis.py` by copying the same-named files from
   `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/` into
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/`. Then apply these constant patches
   inside the new `constants.py`: `DSI_THRESHOLD = 0.5 → 0.7`;
   `K_SWEEP = (2, 3, 4) → (3, 4, 5, 6, 7)`; remove scalar `SOURCE_TASK` / `SOURCE_SEED` and add
   `SOURCES: tuple[tuple[str, int, Path], ...] = ( ("t0106_long_pdnd_nsga2_300gen", 44, Path("tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz")), ("t0112_t0106_seed77_replicate", 77, Path("tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz")), ("t0114_seed7755_no_autostop", 7755, Path("tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/files/predictions.jsonl.gz")), ("t0115_seed9354_no_autostop", 9354, Path("tasks/t0115_seed9354_no_autostop/assets/predictions/t0115-bedb-morph-nsga2-seed9354/files/predictions.jsonl.gz")), )`.
   Update `paths.py` with the new figure paths (`pca_combined.png`, `pca_with_gen0_overlay.png`,
   `electrophys_silhouette.png`, `electrophys_cluster_<k>_morphs.png`, `morphology_silhouette.png`,
   `factor_loadings_heatmap.png`) and the new Parquet paths under `data/`. Inputs: the four files
   from t0108. Outputs: four Python modules under `code/`. Expected observable: module imports
   succeed via
   `uv run python -c "from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code import constants, paths, cluster_helpers, factor_analysis"`
   returning exit code 0. Satisfies REQ prerequisites for steps below (no specific REQ — pure
   scaffolding).

2. **Write the pooled survivor loader.** Create `code/load_pooled_cells.py` (~150 lines) which:
   iterates `SOURCES`; opens each `*.json.gz` or `*.jsonl.gz` and branches on `path.suffixes`
   (`['.jsonl', '.gz']` → line-by-line JSONL, `['.json', '.gz']` → single JSON load and read the
   `"evaluations"` list); for each record applies the cohort filter
   `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0`; attaches the iteration variables `source_task` and
   `seed` plus an enumerated `individual_idx`; dedupes by the 68-d vector rounded to
   `DEDUP_DECIMALS = 6`; assembles a pandas DataFrame with columns
   `[source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, *ALL_PARAM_NAMES]`
   using explicit dtypes (`StringDtype` for `source_task`, `UInt32Dtype` for seed / generation /
   individual_idx, `float64` for the metric and 68 vector columns). Persist to
   `data/pooled_survivors.parquet`. Emit per-seed counts (`n_raw`, `n_passing_filter`, `n_unique`)
   to `results/data/per_seed_cohort_counts.csv`. Run as
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0116_pooled_pca_cluster_factor_dsi07_pd10 -- uv run python -u -m tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.load_pooled_cells`.
   Inputs: 4 predictions `*.gz` files. Outputs: `data/pooled_survivors.parquet`,
   `results/data/per_seed_cohort_counts.csv`. Expected observable: stdout reports the per-seed
   counts and a total survivor count; `pooled_survivors.parquet` exists with `n_unique` rows. This
   is the first non-trivial expensive operation (loads 4 multi-MB files and writes to disk), so
   include a **validation gate**: after loading t0106 alone (~3744 raw records, expected post-filter
   count in the hundreds), print the first 3 surviving rows including all 68 vector values and
   verify `dsi_vector_sum > 0.7` and `pd_rate_hz > 10.0` hold for each. If the t0106 post-filter
   count is **zero** (the trivial baseline — meaning the filter mis-matched the schema or both
   thresholds were inverted), **STOP and debug**: read 5 individual t0106 records, inspect the field
   names exactly, and fix the filter logic before continuing. Do not proceed to the other three
   seeds until t0106 yields a non-empty post-filter cohort. Satisfies REQ-1, REQ-2, REQ-3.

3. **Write the gen-0 random-init loader.** Create `code/load_pooled_gen0.py` (~80 lines) reusing the
   format-branching logic from Step 2 but with the filter `generation == 1` and no DSI / PD filter.
   (`generation == 1` is the random init in all four files; the task description's "gen-0"
   terminology corresponds to this 1-indexed gen 1 row per `research_code.md`'s gen-0 caveat.)
   Persist to `data/pooled_gen0.parquet` with the same column schema as `pooled_survivors.parquet`.
   Inputs: same 4 predictions files. Outputs: `data/pooled_gen0.parquet`. Expected observable:
   stdout reports exactly 96 records per seed (pop slot count) and a total of `96 × 4 = 384` gen-0
   rows. Validation gate: if any seed returns `n_gen0 != 96`, STOP and inspect — the file's
   generation indexing is broken or the filter is wrong. Satisfies REQ-4.

4. **Fit the union-pool standardiser.** Add a
   `fit_pooled_standardiser(matrix: np.ndarray) -> PooledStandardiser` function inside
   `code/cluster_helpers.py` (or a new `code/pooled_standardiser.py`) returning a frozen dataclass
   with `mean: np.ndarray`, `std: np.ndarray` (with zero-std columns clipped to 1.0 to avoid
   division-by-zero), and a `transform(matrix) -> np.ndarray` method. Fit it once on the 68-d
   submatrix of `pooled_survivors.parquet` and serialise the resulting `mean` / `std` arrays to
   `data/pooled_standardiser.npz` so downstream steps and the gen-0 overlay reuse the **same** fit.
   Inputs: `data/pooled_survivors.parquet`. Outputs: `data/pooled_standardiser.npz`. Expected
   observable: stdout prints `mean.shape == (68,)` and `std.shape == (68,)`; no zero or NaN values
   in `std`. Satisfies REQ-5.

5. **Run three PCAs and render `pca_combined.png`.** Create `code/pooled_pca_with_overlay.py` (~250
   lines). Load `data/pooled_survivors.parquet` and `data/pooled_standardiser.npz`. Standardise the
   68-d matrix using the pre-fitted standardiser. Slice into electrophys (columns 0-53) and
   morphology (columns 54-67) submatrices. Fit three `sklearn.decomposition.PCA(n_components=2)`
   instances: `pca_combined` on the full 68-d matrix, `pca_ephys` on the 54-d submatrix, `pca_morph`
   on the 14-d submatrix. Persist `pca_combined`, `pca_ephys`, `pca_morph` to `data/pca_models.pkl`
   (joblib-pickled dict) so Steps 6 and 11 reuse them. Render the 1×3 figure
   `results/images/pca_combined.png` using `matplotlib.pyplot.subplots(1, 3, figsize=(15, 5))`: main
   panel = combined 68-d, side panel A = electrophys, side panel B = morphology. Colour points by
   seed using `tab10[0..3]`; marker `o` filled; one legend entry per seed. Axis labels must read
   `PC1 ({pct:.1f}%)` and `PC2 ({pct:.1f}%)`. Also fit and persist a third PCA
   `pca_ephys_3d = PCA(n_components=3)` on the 54-d submatrix for use in Step 9's representative
   table. Inputs: `data/pooled_survivors.parquet`, `data/pooled_standardiser.npz`. Outputs:
   `data/pca_models.pkl`, `results/images/pca_combined.png`. Expected observable: PNG file exists
   and is non-empty; stdout prints the variance-explained percentages for all three PCAs. Satisfies
   REQ-6.

6. **Project gen-0 and render `pca_with_gen0_overlay.png`.** Extend
   `code/pooled_pca_with_overlay.py` (or add a `render_gen0_overlay` function in the same file).
   Load `data/pooled_gen0.parquet`. Standardise its 68-d matrix using the **same**
   `data/pooled_standardiser.npz` from Step 4 (no refit). Project it onto each of the three PCAs
   from Step 5 via `pca.transform(...)` (no refit). Re-render the same 1×3 figure with gen-0 points
   drawn first as faint grey crosses (`marker='x'`, `color='#888888'`, `alpha=0.3`, `zorder=1`), and
   survivor points on top as in Step 5 (`zorder=2`). Save to
   `results/images/pca_with_gen0_overlay.png`. Compute per-seed mean and 95th-percentile Euclidean
   displacement in (a) PC1+PC2 space of `pca_combined` (survivor mean minus gen-0 mean for the same
   seed, taken as point-to-mean distance), and (b) the full 68-d standardised space. Emit
   `results/data/gen0_displacement.csv` with columns
   `seed, mean_disp_pc12, mean_disp_68d, p95_disp_pc12, p95_disp_68d, n_survivors, n_gen0`. Expected
   observable: PNG exists and is non-empty; CSV has exactly 4 rows (one per seed) plus a header.
   Satisfies REQ-7.

7. **KMeans on the 54-d electrophys subspace.** Adapt
   `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/cluster_electrophys.py` into
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/cluster_electrophys.py` (~400 lines).
   Replace the t0108-specific loader with `pd.read_parquet(...)` against
   `data/pooled_survivors.parquet`. Use the standardiser from `data/pooled_standardiser.npz` on the
   54-d submatrix (do not refit). Call `run_kmeans_sweep(...)` from `cluster_helpers.py` with
   `K_SWEEP = (3, 4, 5, 6, 7)`; it returns `inertias`, `silhouettes`, and the best k by mean
   silhouette. Save the silhouette curve to `results/images/electrophys_silhouette.png` (k on
   x-axis, mean silhouette on y-axis, every k marked, best k highlighted). Save the per-cell cluster
   assignments and PCA-combined coordinates as `results/data/electrophys_clusters.csv` with columns
   `cluster_id, source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, pc1_combined, pc2_combined`.
   Print chosen k, per-cluster size, and per-seed × cluster contingency table to stdout. Inputs:
   `data/pooled_survivors.parquet`, `data/pooled_standardiser.npz`, `data/pca_models.pkl`. Outputs:
   `results/images/electrophys_silhouette.png`, `results/data/electrophys_clusters.csv`. Expected
   observable: PNG and CSV both exist; chosen k is in `[3, 7]`; total cluster-assigned rows = total
   survivor rows. Satisfies REQ-8.

8. **Render electrophys-cluster morphology grids.** Create `code/morphology_rendering.py` (~250
   lines) by copying the helpers `_to_morph_params`, `_extract_section_pts`, `_build_and_extract`,
   `_global_extents`, `_plot_cell`, `_select_top_per_cluster` from
   `tasks/t0109_t0108_morph_cluster_gallery/code/build_cluster_gallery.py` lines 112-222. Add the
   `morph_seed = int(round(x)) % (2**31 - 1)` coercion (t0109 line 130) and the
   `h.delete_section(sec=s)` cleanup (t0109 lines 152-154) — both mandatory. Then create
   `code/render_electrophys_cluster_morphs.py` (~200 lines) which loads
   `results/data/electrophys_clusters.csv` and `data/pooled_survivors.parquet`, joins the cluster
   labels onto the cohort rows, then for each cluster id in the headline-k partition: ranks rows
   descending by `dsi * pd_rate_hz`, takes the top 15, and renders a 5×3 grid using
   `_plot_cell(...)` per panel. Each panel must annotate
   `source_task[-5:] / seed / gen=N / DSI=0.XX / PD=YY.Y` in the upper-left corner so cross-seed
   identity is visible. Save each cluster's grid as
   `results/images/electrophys_cluster_<cluster_id>_morphs.png`. Use the `generate_fixed_morphology`
   library entry point
   (`from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`)
   and `MorphologyParams` from
   `tasks.t0090_morphology_generator_diversity_test.code.morphology_params`. Inputs:
   `results/data/electrophys_clusters.csv`, `data/pooled_survivors.parquet`. Outputs: one PNG per
   electrophys cluster id (e.g., if headline k = 4, four PNGs). Expected observable: one PNG per
   cluster; stdout prints `Built <N> morphologies` and process RSS does not grow unboundedly thanks
   to the `h.delete_section` cleanup. This step builds 15 × k_headline ≤ 105 NEURON cells —
   moderately expensive. **Validation gate**: render cluster 1 alone first; verify the PNG contains
   15 visible dendrite trees with annotations; if any panel is blank or only shows a soma circle (no
   dendrites), **STOP and debug** — the pt3d extraction or `_plot_cell` adapter has a bug. Inspect
   the first cell's `result.all_dends` length and `len(result.h.x3d(...))` per section directly
   before continuing to the remaining clusters. Satisfies REQ-9.

9. **KMeans on the 14-d morphology subspace + representative table.** Adapt
   `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/cluster_morphology.py` into
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/cluster_morphology.py` (~300 lines). Same
   procedure as Step 7 but on the 14-d morphology submatrix. Replace the t0108-specific
   electrophys-overlay boxplots with a 15-row representative table per cluster: rank descending by
   `dsi * pd_rate_hz` within cluster, take top 15, and project each row's 54-d electrophys slice
   onto the **3-component** `pca_ephys_3d` from `data/pca_models.pkl` (fitted in Step 5). Emit
   `results/data/morphology_clusters.csv` (same column layout as Step 7's CSV) and
   `results/data/morphology_cluster_<cluster_id>_representatives.csv` per cluster with columns
   `source_task, seed, generation, dsi_vector_sum, pd_rate_hz, ephys_pc1, ephys_pc2, ephys_pc3`.
   Also save `results/images/morphology_silhouette.png` as the silhouette curve. Inputs:
   `data/pooled_survivors.parquet`, `data/pooled_standardiser.npz`, `data/pca_models.pkl`. Outputs:
   `results/images/morphology_silhouette.png`, `results/data/morphology_clusters.csv`,
   `results/data/morphology_cluster_<k>_representatives.csv` (one per cluster). Expected observable:
   silhouette PNG exists; per-cluster representative CSVs have 15 rows each; chosen k ∈ `[3, 7]`.
   Satisfies REQ-10, REQ-11.

10. **Factor analysis on the full 68-d matrix.** Adapt
    `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/factor_analysis.py` into
    `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/factor_analysis.py` (~360 lines, mostly
    unchanged). Replace the t0108-specific loader with `pd.read_parquet(...)` against
    `data/pooled_survivors.parquet`; use `data/pooled_standardiser.npz` on the 68-d matrix.
    `run_factor_analysis` computes correlation-matrix eigenvalues via
    `np.linalg.eigvalsh(np.cov(z_matrix, rowvar=False, ddof=0))`, counts eigenvalues > 1.0
    (`n_eig_above_one`), caps factor count at `KAISER_FACTOR_CAP = 10`, refits FA with that count,
    applies `varimax_rotation`, and computes rotated factor scores via `Z @ Λ @ pinv(Λ.T @ Λ)`.
    Render the loadings heatmap at `results/images/factor_loadings_heatmap.png` with `RdBu_r`
    colourmap, `vmax = max(abs(loadings))`, `vmin = -vmax`, feature names from `ALL_PARAM_NAMES` on
    the y-axis, factor indices on the x-axis. Compute Pearson r between each rotated factor score
    and `dsi_vector_sum` / `pd_rate_hz`. Emit `results/data/factor_correlations.csv` with columns
    `factor_id, var_explained_pct, r_dsi, r_pd, joint_factor_flag`
    (`joint_factor_flag = (|r_dsi| > 0.30 AND |r_pd| > 0.30)`). Print total variance explained and
    the per-factor table to stdout. Inputs: `data/pooled_survivors.parquet`,
    `data/pooled_standardiser.npz`. Outputs: `results/images/factor_loadings_heatmap.png`,
    `results/data/factor_correlations.csv`, `results/data/factor_loadings.csv` (raw loadings matrix,
    factors × 68 features). Expected observable: heatmap PNG exists; factor count is in `[1, 10]`;
    total variance explained percentage is printed; `factor_correlations.csv` has exactly
    `factor_count` data rows. Satisfies REQ-12, REQ-13.

11. **Compute cluster-vs-seed purity.** Create `code/cluster_seed_purity.py` (~50 lines). Load
    `results/data/electrophys_clusters.csv` and `results/data/morphology_clusters.csv`. For each
    partition, compute (a)
    `sklearn.metrics.normalized_mutual_info_score(labels_true=seeds, labels_pred=clusters)` and (b)
    `scipy.stats.chi2_contingency(crosstab)` returning `(chi2, p_value, dof, expected)` on a pandas
    crosstab. Emit `results/data/cluster_seed_purity.csv` with columns
    `partition, nmi, chi2, p_value, dof` (two rows: `electrophys_k=<n>` and `morphology_k=<m>`).
    Print both rows to stdout. Inputs: the two cluster CSVs from Steps 7 and 9. Outputs:
    `results/data/cluster_seed_purity.csv`. Expected observable: CSV has 2 rows + header; NMI in
    `[0, 1]`; chi-square p-value reported. Satisfies REQ-14.

12. **Produce three answer assets.** Create the three answer asset folders
    `assets/answer/pooled-survivors-basin-connectivity-dsi07-pd10/`,
    `assets/answer/pooled-survivors-displacement-from-init-dsi07-pd10/`, and
    `assets/answer/pooled-survivors-latent-drivers-dsi07-pd10/`. Each folder contains `details.json`
    (per `meta/asset_types/answer/specification.md`), a canonical short answer document `answer.md`,
    and a canonical full answer document `full.md`. Each `details.json` must set `paper_id`-style
    `answer_id` to the folder slug, `question` to the verbatim Q from `task_description.md`,
    `short_answer_path: "answer.md"`, `full_answer_path: "full.md"`,
    `added_by_task: "t0116_pooled_pca_cluster_factor_dsi07_pd10"`, and `answer_methods` listing
    `["asset-cross-reference", "code-experiment"]`. Short answers must be 2-5 sentences each,
    direct, citation-free in the `## Answer` block. Full answers must include `## Short Answer`,
    `## Evidence from Code or Experiments` (citing the CSVs and PNGs from Steps 5-11 by exact
    relative path), `## Limitations` (note the truncated-cohort artefact risk per t0110), and
    `## Sources` containing markdown reference link definitions for all cited tasks (t0106, t0112,
    t0114, t0115, t0108, t0109, t0110). Inputs: every artefact from Steps 5-11. Outputs: three asset
    folders. Expected observable: each `details.json` is valid JSON; each canonical short answer has
    2-5 sentences; each canonical full answer has all four required sections. Satisfies REQ-15.

13. **Emit methodology notes for the downstream reporting stage.** Create
    `results/data/methodology_notes.md` (a small ~30-line file consumed downstream by the
    orchestrator). Document: (a) the schema variance across the four sources (t0106/t0112
    JSON-wrapped vs t0114/t0115 JSONL); (b) `generation == 1` is the random init in all four files;
    (c) `joint_pass` / `legit` booleans on t0114/t0115 records are ignored in favour of the
    canonical fields `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0`; (d) the union-pool standardiser
    is fit once and reused (not refit per seed); (e) no registered metric from `meta/metrics/`
    applies because this task performs no new simulations — DSI and PD are backfilled from frozen
    predictions assets. Inputs: prior knowledge from `research_code.md` and the implementation log.
    Outputs: `results/data/methodology_notes.md`. Expected observable: file exists and contains the
    five bullet points above. Satisfies REQ-17.

## Remote Machines

None required. This is a CPU-only pandas + scikit-learn + matplotlib + NEURON-build analysis
designed to run on a single laptop CPU in ~30 minutes wall clock. No GPU, no cluster, no Vast.ai, no
cloud egress.

## Assets Needed

* `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`
  (~3744 evaluation records, gzipped JSON wrapper format) — from dependency
  `t0106_long_pdnd_nsga2_300gen`.
* `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz`
  (~2016 evaluation records, gzipped JSON wrapper format) — from dependency
  `t0112_t0106_seed77_replicate`.
* `tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/files/predictions.jsonl.gz`
  (~5952 evaluation records, gzipped JSONL format) — from dependency `t0114_seed7755_no_autostop`.
* `tasks/t0115_seed9354_no_autostop/assets/predictions/t0115-bedb-morph-nsga2-seed9354/files/predictions.jsonl.gz`
  (~5280 evaluation records, gzipped JSONL format) — from dependency `t0115_seed9354_no_autostop`.
* Registered library `procedural_dsgc_morphology_generator` from
  `tasks/t0090_morphology_generator_diversity_test/` — provides `MorphologyParams` and
  `MorphologyResult` dataclasses.
* Registered library `procedural_dsgc_morphology_generator_fix` from
  `tasks/t0092_diagnose_morphology_generator_silence/` — provides `generate_fixed_morphology`, the
  canonical build entry point.
* Reference code (copied, not imported) from `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/` —
  `paths.py`, `constants.py`, `cluster_helpers.py`, `factor_analysis.py`, and adapted
  `cluster_electrophys.py` / `cluster_morphology.py`.
* Reference code (copied, not imported) from
  `tasks/t0109_t0108_morph_cluster_gallery/code/build_cluster_gallery.py` lines 112-222 —
  `_to_morph_params`, `_extract_section_pts`, `_build_and_extract`, `_global_extents`, `_plot_cell`,
  `_select_top_per_cluster`.

## Expected Assets

Per `task.json` `expected_assets`: 3 answer assets.

* `assets/answer/pooled-survivors-basin-connectivity-dsi07-pd10/` — answers Q1: "Does the
  joint-pass cohort form a single connected manifold in 68-d, or do the four seeds occupy
  seed-specific sub-basins?" Evidence: `pca_combined.png`, `pca_with_gen0_overlay.png`,
  `cluster_seed_purity.csv` (NMI + chi-square).
* `assets/answer/pooled-survivors-displacement-from-init-dsi07-pd10/` — answers Q2: "How far did
  NSGA-II travel from gen-0 in each seed?" Evidence: `pca_with_gen0_overlay.png`,
  `gen0_displacement.csv` (per-seed mean and 95th-percentile Euclidean displacement in PC1+PC2 and
  full 68-d standardised spaces).
* `assets/answer/pooled-survivors-latent-drivers-dsi07-pd10/` — answers Q3: "Which factors (after
  varimax rotation) load most strongly on DSI and pd_rate_hz, and are they morphology-dominated,
  electrophys-dominated, or mixed?" Evidence: `factor_loadings_heatmap.png`,
  `factor_correlations.csv` (per-factor Pearson r with DSI / PD, joint-factor flag),
  `factor_loadings.csv`.

## Time Estimation

* Module scaffolding (Step 1): ~5 minutes.
* Loaders + standardiser fit (Steps 2-4): ~5 minutes wall clock for the IO + Parquet writes.
* PCA + gen-0 overlay rendering (Steps 5-6): ~5 minutes.
* KMeans sweeps + silhouette PNGs (Steps 7 and 9): ~5 minutes per partition (the silhouette
  computation on `k ∈ {3, 4, 5, 6, 7}` is the dominant cost but still trivial at < 1000 cells).
* Morphology grid rendering (Step 8): ~10 minutes for ≤ 105 NEURON cell builds + matplotlib
  output.
* Factor analysis + heatmap (Step 10): ~2 minutes.
* Purity computation (Step 11): < 1 minute.
* Answer asset authoring (Step 12): ~30 minutes — three small markdown documents plus three
  `details.json` files.
* Methodology notes (Step 13): ~5 minutes.
* **Total implementation wall clock**: ~60-75 minutes (excluding the orchestrator-managed downstream
  stages that follow implementation).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Container-format branch mishandles t0114 / t0115 JSONL (loader returns empty cohort for either seed) | Medium | Blocking — Q1 / Q2 / Q3 all depend on a non-trivial pool | Step 2 includes a validation gate that prints per-seed `n_raw` / `n_passing_filter` / `n_unique`; STOP-and-debug if any seed reports `n_raw == 0`. Confirm by reading 5 individual records from the offending file directly. |
| t0112 seed-77 cohort has too few survivors (research_code.md flags 7 LEGIT joint-pass cells at the t0114-style strict threshold) | High | The chi-square test on cluster × seed contingency may have <5 expected counts in some cells, invalidating the chi-square asymptotic. NMI is unaffected. | Report both NMI (robust to sparse cells) and chi-square; if any expected count is < 5, fall back to Fisher's exact test (`scipy.stats.fisher_exact` on per-cluster 2×2 contingency) and report a warning in the answer asset. |
| Truncated-cohort artefact (per t0110) — strict DSI > 0.7 filter saturates factor sign patterns and Kaiser may bind at the cap of 10 | Medium | Q3 conclusions may be partially methodological artefacts rather than substrate properties | Report `n_eig_above_one` (raw Kaiser count) alongside the capped factor count; note explicitly in the Q3 answer asset's `## Limitations` section that the strict cohort may bias factor signs, citing t0110's relaxed-cohort finding. |
| NEURON RSS creep when building > 100 morphologies in one process | Low (mitigated by t0109's `h.delete_section` cleanup) | Process may crash or swap on a laptop with 8 GB RAM | Copy the t0109 cleanup (`h.delete_section(sec=s)` after `_extract_section_pts`, lines 152-154 of `build_cluster_gallery.py`) verbatim into `morphology_rendering.py`. If RSS still grows, render each cluster's grid in a separate subprocess via `multiprocessing.Process`. |
| Headline `k` differs sharply between the electrophys and morphology partitions (e.g., 3 vs 7) | Medium | Cross-partition narrative becomes harder; risk of cherry-picking which partition to highlight | Step 7 and Step 9 both report the full silhouette curve over `k ∈ {3, 4, 5, 6, 7}`; the answer asset must report both headline k's side by side and refrain from declaring either as "the right one". |
| `morph_seed` cast to int overflows INT32 in a corner record | Low | NEURON `Random()` raises ValueError; cell build crashes | Apply the `int(round(x)) % (2**31 - 1)` coercion (t0109 line 130) before passing `morph_seed` to `MorphologyParams.from_dict`. |
| Standardiser accidentally refit per seed inside one of the cluster scripts | Low (intent: guard by passing the `data/pooled_standardiser.npz` arrays explicitly) | Silently invalidates every cross-seed comparison — the very signal the task is designed to detect would be erased | Encode the fit as a single function returning a frozen dataclass and load it from `data/pooled_standardiser.npz` in every downstream script. Never instantiate `sklearn.preprocessing.StandardScaler` inside a per-seed loop. |

## Verification Criteria

Each criterion below names an exact command to run and the observable signal that confirms it.

* **C1 (REQ-3, REQ-4)**: `pooled_survivors.parquet` exists, the row count equals the sum of per-seed
  survivor counts logged at load time, and `pooled_gen0.parquet` has exactly 384 rows (96 per seed
  × 4 seeds). Run:
  `uv run python -c "import pandas as pd; from pathlib import Path; df_s = pd.read_parquet(Path('tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/data/pooled_survivors.parquet')); df_g = pd.read_parquet(Path('tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/data/pooled_gen0.parquet')); print(len(df_s), len(df_g), df_s.groupby('seed').size().to_dict(), df_g.groupby('seed').size().to_dict())"`.
  Expected: `len(df_s) > 0`, `len(df_g) == 384`, every seed's `df_g` count is exactly 96.

* **C2 (REQ-5)**: The pooled standardiser was fitted once on the union pool and saved to
  `data/pooled_standardiser.npz`. Run:
  `uv run python -c "import numpy as np; s = np.load('tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/data/pooled_standardiser.npz'); print(s['mean'].shape, s['std'].shape, np.all(s['std'] > 0))"`.
  Expected: shapes are `(68,)`, `(68,)`, and `np.all(s['std'] > 0)` is `True`.

* **C3 (REQ-6, REQ-7, REQ-8, REQ-10, REQ-12)**: Every chart referenced in the plan exists on disk
  under `results/images/`. Run:
  `uv run python -c "from pathlib import Path; root = Path('tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images'); required = ['pca_combined.png', 'pca_with_gen0_overlay.png', 'electrophys_silhouette.png', 'morphology_silhouette.png', 'factor_loadings_heatmap.png']; missing = [n for n in required if not (root / n).exists()]; assert missing == [], missing; print('all required PNGs present')"`.
  Expected: prints `all required PNGs present`. Additionally, at least one
  `electrophys_cluster_*_morphs.png` exists in the same directory.

* **C4 (REQ-15)**: The three answer asset folders exist and each contains `details.json`,
  `answer.md`, and `full.md`. Run:
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset t0116_pooled_pca_cluster_factor_dsi07_pd10`
  and verify zero errors on all three asset slugs `pooled-survivors-basin-connectivity-dsi07-pd10`,
  `pooled-survivors-displacement-from-init-dsi07-pd10`,
  `pooled-survivors-latent-drivers-dsi07-pd10`. Expected: exit code 0 and no error-level
  diagnostics.

* **C5 (REQ-1, REQ-2, REQ-3, REQ-17 — schema sanity)**: The pooled survivor file contains the 68
  named vector columns from `ALL_PARAM_NAMES`, no nulls in those columns, and every `dsi_vector_sum`
  value exceeds 0.7. Run:
  `uv run python -c "import pandas as pd; from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.constants import ALL_PARAM_NAMES; df = pd.read_parquet('tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/data/pooled_survivors.parquet'); assert set(ALL_PARAM_NAMES).issubset(df.columns); assert df[list(ALL_PARAM_NAMES)].isna().sum().sum() == 0; assert (df['dsi_vector_sum'] > 0.7).all(); assert (df['pd_rate_hz'] > 10.0).all(); print('schema ok')"`.
  Expected: prints `schema ok`.

* **C6 (plan structure)**: The plan verificator passes with zero errors. Run:
  `uv run python -u -m arf.scripts.verificators.verify_plan t0116_pooled_pca_cluster_factor_dsi07_pd10`.
  Expected: exit code 0 and no error-level diagnostics.

* **C7 (REQ coverage)**: Every `REQ-*` item from `## Task Requirement Checklist` is referenced by at
  least one step in `## Step by Step`. Spot-check by grepping the plan for `REQ-1` through `REQ-17`
  and confirming each appears at least once in the Step by Step section. This is a manual check the
  reviewer can run with a single grep over `plan.md`; the verificator's `PL-W007` check also
  validates that `REQ-*` markers appear in `## Step by Step`.
