---
spec_version: "2"
task_id: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
date_completed: "2026-05-22"
status: "complete"
---
# t0117 — Pooled PCA + Cluster + Factor Analysis of ALL Cells Across 4 Seeds Plan

## Objective

Pool every NSGA-II evaluation record from four seeds (t0106 seed 44, t0112 seed 77, t0114 seed 7755,
t0115 seed 9354) into a single labelled cohort keyed by
`(source_task, seed, generation, individual_idx)` **without applying any DSI / PD-rate cohort
filter**, then run PCA + KMeans on the 54-d electrophys subspace, PCA + KMeans on the 14-d
morphology subspace, varimax factor analysis on the full 68-d feature vector, and a gen-0
random-init overlay to quantify how far NSGA-II travelled from its random initialisation. Produce
six charts, several CSV tables, three answer assets, and a head-to-head comparison subsection vs
t0116 (the strict-cohort version of the same pipeline). Done = all charts on disk, three answer
assets passing `verify_answer_asset`, the pooled cohort persisted as Parquet for reproducibility,
and the t0116 head-to-head comparison table present in `results_detailed.md` covering pool sizes,
KMeans k, NMI, silhouette, varimax factor count, total variance explained, joint-factor count, and
per-seed displacement.

## Task Requirement Checklist

Operative task text from `task.json` (`short_description`) and `task_description.md`:

> **Name**: Pooled PCA + cluster + factor analysis of ALL cells across 4 seeds
>
> **Short description**: Repeat t0116 PCA + KMeans + varimax FA across seeds 44/77/7755/9354 with NO
> DSI/PD filter; tests whether t0116's seed-specific basin pattern is a strict-cohort artefact.
>
> **Pool**: every record from every source loaded (no DSI / PD filter); deduplicated by the 68-d
> vector rounded to 6 decimals (same convention as t0116); expected pool size after dedup ~14k cells
> (vs t0116's 869); per-seed counts recorded before and after dedup and reported in
> `results_detailed.md`.
>
> **Feature vector**: identical to t0116, 68-d `vector_68d` with indices 0-53 the 54-d Bed-B
> electrophys vector and 54-67 the 14-d morphology vector. Authoritative names in
> `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` `ALL_PARAM_NAMES`.
>
> **Analyses to run (mirror t0116 exactly, sans cohort filter)**: (1) Combined 68-d PCA + side
> panels — one figure, three subplots; combined / electrophys-only / morphology-only PC1 vs PC2,
> coloured by source seed; `% variance explained` in axis labels; saved to
> `results/images/pca_combined.png`. (2) Gen-0 (`generation == 1`) random-init overlay on the same
> axes; per-seed mean and 95th-percentile Euclidean displacement in PC1+PC2 space and in 68-d
> standardised space; saved to `results/images/pca_with_gen0_overlay.png` and
> `results/data/gen0_displacement.csv`. (3) KMeans on 54-d electrophys subspace, auto-pick
> `k ∈ [3, 7]` by silhouette; per-cluster 5×3 grid of 15 representative cells using full dendrite
> trees (NEURON pt3d, not somas); representatives ranked by `dsi_vector_sum * pd_rate_hz` within
> cluster (canonical t0109 / t0116 rule); saved to `results/images/electrophys_silhouette.png`,
> `results/data/electrophys_clusters.csv`, and one
> `results/images/electrophys_cluster_<k>_morphs.png` per cluster. (4) KMeans on 14-d morphology
> subspace, auto-pick `k ∈ [3, 7]` by silhouette; per-cluster 15-row representative table with
> `(source_task, seed, generation, dsi_vector_sum, pd_rate_hz, ephys_PC1, ephys_PC2, ephys_PC3)`;
> saved to `results/images/morphology_silhouette.png`, `results/data/morphology_clusters.csv`, and
> one `results/data/morphology_cluster_<k>_representatives.csv` per morph cluster. (5) Factor
> analysis on the full 68-d feature matrix; standardise → fit
> `sklearn.decomposition.FactorAnalysis(n_components=68)`; count Kaiser eigenvalues > 1 from the
> correlation matrix; cap at `KAISER_FACTOR_CAP = 10` (inherited from t0108); refit FA with the
> chosen count; apply varimax rotation via the iterative-SVD helper from t0108; render loadings
> heatmap with `RdBu_r` and symmetric vmin/vmax to `results/images/factor_loadings_heatmap.png`;
> per-factor variance and Pearson r vs DSI / PD in `results/data/factor_correlations.csv`.
>
> **Three answer assets** (each one question): Q1 cross-seed basin connectivity without the cohort
> filter — NMI, chi-square contingency, visual PCA overlap, direct head-to-head vs t0116; Q2
> truncated-cohort artefact test — does at least one varimax factor satisfy
> `|r_DSI| > 0.3 AND |r_PD| > 0.3` once the full quality range is admitted; Q3 displacement from
> random init in the full pool — compare to t0116's per-seed displacement.
>
> **Comparison vs t0116** in `results_detailed.md`: side-by-side table of pool sizes, KMeans k
> chosen, per-partition NMI, per-partition silhouette, varimax factor count, total variance
> explained, joint-factor count (|r| > 0.3 on both), plus per-seed displacement (mean PC1+PC2 and
> mean 68-d); plain-English verdict per question.
>
> **Verification**: `data/pooled_all_cells.parquet` row count equals the sum of per-seed
> dedup-unique counts logged at load time; every PCA / KMeans / FA fit uses the standardiser fitted
> on the union pool (not per-seed); every chart referenced in `results_detailed.md` exists on disk;
> every claim in the three answer assets is grounded in a specific table or chart in
> `results_detailed.md`; headline NMI and joint-factor counts must be reported even if they confirm
> the t0116 finding.

* **REQ-1**: Load every evaluation record from the four source predictions paths listed in
  `task_description.md` (`tasks/t0106_long_pdnd_nsga2_300gen/.../all_evaluations_seed44.json.gz`,
  `tasks/t0112_t0106_seed77_replicate/.../all_evaluations_seed77.json.gz`,
  `tasks/t0114_seed7755_no_autostop/.../predictions.jsonl.gz`,
  `tasks/t0115_seed9354_no_autostop/.../predictions.jsonl.gz`). **No DSI / PD-rate filter is
  applied** — every record from every source is admitted. Handle both container shapes: t0106 /
  t0112 use a gzipped JSON wrapper `{"evaluations": [...]}`, while t0114 / t0115 use gzipped JSONL
  (one record per line). Branch on `path.suffixes` to pick the right decoder. Ignore the optional
  `joint_pass` / `legit` booleans on t0114 / t0115 records (they are deliberately not used as a
  filter). The single one-line edit vs t0116 lives inside `code/load_pooled_cells.py`: the cohort
  filter `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` is removed; every other line of the loader is
  identical. *Satisfied by Step 2.*

* **REQ-2**: Dedupe by the 68-d vector rounded to 6 decimals (project convention from t0108) and
  record per-seed counts `n_raw` (every record loaded) and `n_unique` (post-dedup). The strict
  filter is no longer applied, so there is no separate `n_passing_filter` column — the per-seed
  CSV has only the raw and dedup-unique counts. Emit the per-seed counts as a CSV
  (`results/data/per_seed_pool_counts.csv`) plus a Markdown summary for the downstream reporting
  stage. *Satisfied by Step 2 and Step 3.*

* **REQ-3**: Persist the pooled cohort to
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet` keyed by
  `(source_task, seed, generation, individual_idx)` with `dsi_vector_sum`, `pd_rate_hz`, and the 68
  named vector columns from `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py`
  `ALL_PARAM_NAMES`. The Parquet row count must equal the sum of per-seed `n_unique` counts.
  Expected total ~14k rows (vs t0116's 869). *Satisfied by Step 2.*

* **REQ-4**: Load the gen-0 random-init pool by filtering `generation == 1` (1-indexed in all four
  files; gen 1 contains exactly 96 records per seed = pop slot count, regardless of the DSI / PD
  values of those gen-0 individuals). Persist to `data/pooled_gen0.parquet` with the same column
  schema as `pooled_all_cells.parquet`. Expected total = `96 × 4 = 384` rows (same as t0116; gen-0
  was never filtered there either). *Satisfied by Step 3.*

* **REQ-5**: Standardise the 68-d feature matrix on the **union pool** (not per-seed). The same
  standardiser must be fitted once on the ~14k unfiltered cohort and reused for every downstream
  PCA, KMeans, FA, and gen-0 projection. Encode the fit as `fit_pooled_standardiser(matrix)` and
  reference the returned `mean`/`std` everywhere. *Satisfied by Step 4 and propagated through Steps
  5-9.*

* **REQ-6**: Fit three PCAs on the standardised union pool — full 68-d, 54-d electrophys-only
  (vector columns 0-53 of `ALL_PARAM_NAMES`), and 14-d morphology-only (columns 54-67). For each
  PCA, retain PC1 and PC2 with `% variance explained`. Render `results/images/pca_combined.png` as a
  1×3 figure: main panel (combined 68-d PC1 vs PC2), side panel A (electrophys-only PC1 vs PC2),
  side panel B (morphology-only PC1 vs PC2). Colour every point by `seed` using a fixed 4-colour
  palette (the first four of `matplotlib.cm.tab10`); use filled circles for all points. Each
  subplot's axis labels must contain the `% variance explained` for PC1 and PC2. *Satisfied by Step
  5.*

* **REQ-7**: Project the gen-0 individuals onto the **same three PCAs fitted in Step 5** (no refit;
  reuse the standardiser too). Render `results/images/pca_with_gen0_overlay.png` as the same 1×3
  figure with faint grey crosses (`x` marker, `alpha=0.3`) for gen-0 cells underneath the cohort
  scatter. Compute per-seed mean and 95th-percentile Euclidean displacement in (a) PC1+PC2 space of
  the combined 68-d PCA, and (b) the full 68-d standardised space (cohort cells vs gen-0 mean for
  the same seed). Emit as `results/data/gen0_displacement.csv` for downstream reporting consumption.
  *Satisfied by Step 6.*

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
  electrophys row onto the first three PCs; a separate `pca_ephys_3d` instance with `n_components=3`
  is fitted on the same standardised electrophys submatrix and persisted alongside the 2-component
  PCAs). Emit `results/data/morphology_cluster_<k>_representatives.csv` for downstream reporting
  consumption. *Satisfied by Step 9.*

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
  each rotated factor score and `dsi_vector_sum` / `pd_rate_hz`. Flag joint factors that satisfy
  `|r_DSI| > 0.30 AND |r_PD| > 0.30` (the "truncated-cohort artefact test" — t0116 found zero such
  factors at the strict cohort; t0117 must report how many are present once the full quality range
  is admitted). Emit as `results/data/factor_correlations.csv` for downstream reporting consumption.
  *Satisfied by Step 10.*

* **REQ-14**: Compute KMeans cluster-vs-seed purity for both partitions (electrophys-k and
  morphology-k). Report both normalised mutual information
  (`sklearn.metrics.normalized_mutual_info_score(labels_true=seeds, labels_pred=clusters)`) and a
  chi-square contingency test (`scipy.stats.chi2_contingency`) on the cluster × seed crosstab. Emit
  as `results/data/cluster_seed_purity.csv`. The same NMI numbers must appear in the t0116
  head-to-head comparison subsection of `results_detailed.md`. *Satisfied by Step 11.*

* **REQ-15**: Produce three answer assets under `assets/answer/<answer_id>/` following
  `meta/asset_types/answer/specification.md`. The three answer IDs and questions, per
  `task_description.md` Expected Outputs section, are:
  * `pooled-all-cells-basin-connectivity-without-filter` — Q1 cross-seed basin connectivity
    without the cohort filter, with explicit head-to-head NMI vs t0116;
  * `pooled-all-cells-truncated-cohort-artefact-test` — Q2 truncated-cohort artefact test: does at
    least one varimax factor satisfy `|r_DSI| > 0.3 AND |r_PD| > 0.3` once the full pool is
    admitted;
  * `pooled-all-cells-displacement-from-init-full-pool` — Q3 displacement from random init in the
    full pool, with explicit head-to-head per-seed displacement vs t0116. Each canonical short
    answer must be 2-5 sentences, citation-free in the `## Answer` / `## Short Answer` sections,
    with all citations in `## Sources`. Each full answer asset must cite the specific chart and CSV
    files produced by Steps 5-11. *Satisfied by Step 12.*

* **REQ-16**: Every chart in `results/images/` must be embedded by the downstream reporting stage
  via `![desc](images/file.png)` syntax. This embedding is performed by the orchestrator-managed
  reporting stage and is not part of the implementation Step by Step below; the implementation must,
  however, produce every PNG on disk before reporting can succeed. *Satisfied via the orchestrator
  reporting step which consumes the artefacts produced by Steps 5-11.*

* **REQ-17**: Document up-front the schema variance across the four sources (t0106 / t0112
  JSON-wrapped vs t0114 / t0115 JSONL; gen 1 = random init in all four; `joint_pass` / `legit`
  booleans ignored; **no cohort filter applied**, in deliberate contrast to t0116). The
  implementation must emit a Methodology block as `results/data/methodology_notes.md` for the
  reporting stage to consume when assembling the downstream report. *Satisfied by Step 13.*

## Approach

This task is a near-clone of t0116 with a single methodological change: the cohort filter
`dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` is **removed** from `code/load_pooled_cells.py`. Every
other module from `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/` is copied verbatim into
this task's `code/` directory (loader format-branching, gen-0 = `generation == 1` convention,
union-pool standardiser, NEURON pt3d morphology rendering, varimax + Kaiser cap = 10, cluster
representative selection rule). The 68-d feature layout is identical across all four seeds because
all four are forks of t0106 that did not touch the parameter ordering — indices 0-53 are the 54-d
Bed-B electrophys vector (`ELECTROPHYS_PARAM_NAMES`) and 54-67 are the 14-d morphology vector
(`MORPHOLOGY_PARAM_NAMES`), both authoritatively defined in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py`.

**Module layout adopted from t0116**: `paths.py` (path constants, with paths updated to point at
`data/pooled_all_cells.parquet` instead of `data/pooled_survivors.parquet`), `constants.py` (the 68
feature names, k-sweep range `(3, 4, 5, 6, 7)`, `KAISER_FACTOR_CAP = 10`, `DEDUP_DECIMALS = 6`,
`SOURCES` four-tuple — `DSI_THRESHOLD` may be left in the file but is no longer referenced),
`cluster_helpers.py` (`zscore_matrix`, `run_pca`, `run_kmeans_sweep`, `top_k_loadings`),
`factor_analysis.py` (`varimax_rotation`, `run_factor_analysis`), `cluster_electrophys.py` and
`cluster_morphology.py` (the two subspace clustering drivers), `morphology_rendering.py`
(full-dendrite NEURON pt3d helpers — copied verbatim from t0116, which itself copied from t0109),
`pooled_pca_with_overlay.py` (the three-panel PCA + gen-0 overlay driver), `load_pooled_cells.py`
(multi-seed, multi-format loader — **the one line that diverges from t0116 is the deletion of the
`dsi > 0.7 AND pd > 10` filter clause**), `load_pooled_gen0.py` (gen-0 random-init loader, identical
to t0116), and `cluster_seed_purity.py` (NMI + chi-square purity calculator, identical to t0116).
Per the cross-task import rule, all code is copied into this task's `code/` directory rather than
imported.

**Key research findings (inherited verbatim from
`tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/research/research_code.md` — no new research was
required for t0117 because the only methodological change is dropping the cohort filter):**

* **Container format drift**: t0106 and t0112 use gzipped JSON with a top-level
  `{"evaluations": [...]}` wrapper; t0114 and t0115 use gzipped JSONL (one record per line). All
  four share the same per-record schema. The loader must branch on `path.suffixes`
  (`['.jsonl', '.gz']` vs `['.json', '.gz']`) and cannot assume a single decode path.

* **Gen-0 ≡ generation == 1**: all four files are 1-indexed; gen 1 contains exactly 96 records
  (one per pop slot) and is the random init. There is no `generation == 0` row; any code that
  assumes one will silently produce no records.

* **Standardisation on union pool, not per-seed**: per-seed z-scoring would absorb cross-seed scale
  differences into the standardiser and erase the very signal the analysis is designed to detect.
  Encode the fit once and propagate the returned mean / std everywhere. Especially important for
  t0117 because the pool is now ~14k cells with much wider variance in DSI / PD than t0116's
  869-cell strict cohort.

* **NEURON memory creep**: t0109's `_build_and_extract` explicitly calls `h.delete_section(sec=s)`
  on each `result.all_dends` section after extraction. Skipping this causes monotonic RSS growth as
  more morphologies are rendered. t0117 will build at minimum `K_max × 15 = 7 × 15 = 105`
  morphologies in one process (more across both partitions), so this hygiene step is mandatory.

* **`morph_seed` overflow**: the morphology vector carries `morph_seed` as a float. Cast as
  `int(round(x)) % (2**31 - 1)` before constructing `MorphologyParams` to avoid out-of-range
  integers if the GA mutated the seed beyond INT32_MAX.

* **Truncated-cohort artefact (the central reason t0117 exists)**: t0108's strict cohort (DSI > 0.5)
  produced all-negative PD correlations in every factor. t0110 showed this was a strict-cohort
  artefact rather than a fundamental substrate property — at the relaxed DSI > 0.2 cohort, 2 of 10
  factors had positive r(PD). t0116's even stricter cohort (DSI > 0.7 ∧ PD > 10) reported zero
  joint factors (no factor with |r| > 0.3 on both DSI and PD simultaneously). t0117 lifts the filter
  entirely; its central question is whether a joint factor reappears once the full quality range is
  in the pool.

* **Silhouette scaling**: `sklearn.metrics.silhouette_score` is O(n²) in memory and runtime when
  computed exactly. At ~14k cells × `K_SWEEP` of 5 values × 2 partitions, this is the dominant
  wall-clock cost (estimated ~30-60 min). t0116's strict cohort (~869 cells) made silhouette
  trivially fast; t0117 must budget for it.

**Alternatives considered (rejected)**:

* *Per-seed PCAs with Procrustes alignment instead of union-pool PCA.* Rejected for the same reason
  as t0116: the task explicitly requires a pool-level standardiser; aligning four separate PCAs adds
  methodological complexity without answering the "is this one basin or several?" question more
  cleanly than union PCA already does. Especially important here because the question is whether the
  basin pattern from t0116 persists or dissolves when the cohort filter is lifted — per-seed PCAs
  would prevent direct comparison to t0116's union-pool numbers.

* *Including t0113 (seed 2247) for a five-seed pool.* Rejected as out-of-scope per the task
  description ("t0113 remains intentionally excluded so the only methodological change vs t0116 is
  the cohort filter"). Adding a fifth seed would conflate the cohort-filter effect with a
  seed-coverage effect.

* *Subsampling the unfiltered pool to ~869 cells (matching t0116's pool size) before clustering.*
  Rejected because the whole point of t0117 is to ask what happens when the full quality range is
  admitted. Subsampling would either reintroduce the cohort selection or impose a different (and
  ad-hoc) selection rule.

* *Endpoint-only morphology rendering via `scratch_t0112_top15_morphologies.py`.* Rejected because
  the project preference (memory note `feedback_top50_morphologies_full_dendrites.md`) explicitly
  requires full dendrite trees, not just somas / endpoint segments. t0116 followed this rule; t0117
  inherits it.

**Task types (`task.json` declares `data-analysis`, `comparative-analysis`, `answer-question`)**.
All three apply: the load + PCA + KMeans + FA pipeline is a data-analysis workflow; the cross-seed
comparison (basin connectivity, displacement, factor drivers) and the head-to-head vs t0116 together
make this a comparative analysis along two axes; and the three deliverables are answer assets. Per
the data-analysis Planning Guidelines, every chart type is named up-front; per the
comparative-analysis guidelines, the comparison axes (seed AND cohort filter vs t0116) and
significance test (chi-square on cluster × seed contingency, plus NMI) are decided here; per the
answer-question guidelines, three explicit `answer_id` slugs are listed above and each cites
concrete chart / CSV evidence.

**Registered metrics applicability**. The four registered metrics (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) all describe per-cell DSI
/ tuning measurements taken during a NEURON simulation. t0117 does no new simulations — it pools
and analyses pre-computed `dsi_vector_sum` and `pd_rate_hz` values from frozen predictions assets
(identical to t0116). None of the registered metrics correspond to the unsupervised summaries this
task produces (silhouette scores, % variance explained, NMI, Euclidean displacement). The
implementation will therefore not write any registered metric keys into `results/metrics.json`. This
omission is deliberate, not accidental, and is documented in `results/data/methodology_notes.md` for
the reporting stage to mirror.

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Local CPU compute (load + standardise + 3 PCAs + 2 KMeans sweeps with O(n²) silhouette on ~14k cells + FA + 100+ NEURON cell builds + matplotlib rendering on a single laptop CPU) | ~60-90 minutes wall clock |
| Paid API calls (OpenAI, Anthropic, etc.) | $0 — no LLM calls in the pipeline |
| Remote GPU compute (Vast.ai, RunPod) | $0 — no remote machine provisioned |
| Storage / egress | $0 — local Parquet + PNG only |
| **Predicted spend** | **$0** |
| **Hard cap** | **$0** (well under the per-task default limit of $8 from `project/budget.json`) |

All four source predictions files are already present locally in the dependency task folders (t0106,
t0112, t0114, t0115). No external downloads are required; no paid services are touched. Runtime is
somewhat longer than t0116 (~14k vs ~870 cells) because the silhouette score is O(n²); the KMeans
sweep dominates wall-clock.

## Step by Step

Implementation work only — load → pool → PCA → KMeans → morph grids → factor analysis
→ answer assets. The reporting / suggestions / compare-literature stages are managed by the
orchestrator after this implementation finishes.

1. **Set up the module skeleton.** Create `code/paths.py`, `code/constants.py`,
   `code/cluster_helpers.py`, and `code/factor_analysis.py` by copying the same-named files from
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/` into
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/`. Update `paths.py` to point at
   this task's `data/pooled_all_cells.parquet` (instead of `data/pooled_survivors.parquet`); leave
   every other constant in `constants.py` unchanged (`K_SWEEP = (3, 4, 5, 6, 7)`,
   `KAISER_FACTOR_CAP = 10`, `DEDUP_DECIMALS = 6`, the `SOURCES` four-tuple, the 68 feature names).
   `DSI_THRESHOLD = 0.7` and `PD_THRESHOLD = 10.0` may stay in `constants.py` as dead constants (no
   caller will reference them after Step 2 drops the filter), or may be deleted — either is
   acceptable; do not, however, change their values silently. Inputs: every file under
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/`. Outputs: four Python modules under
   `code/`. Expected observable: module imports succeed via
   `uv run python -c "from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code import constants, paths, cluster_helpers, factor_analysis"`
   returning exit code 0. Satisfies REQ prerequisites for steps below (no specific REQ — pure
   scaffolding).

2. **[CRITICAL] Write the pooled cohort loader with the cohort filter removed.** Copy
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/load_pooled_cells.py` into
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/load_pooled_cells.py` and apply
   **one and only one** change: delete the filter clause
   `if record["dsi_vector_sum"] > 0.7 and record["pd_rate_hz"] > 10.0:` (or the equivalent
   `if filtered` mask depending on the t0116 implementation) — every record from every source must
   be admitted. Replace the output parquet path with `data/pooled_all_cells.parquet`. Replace the
   per-seed-count CSV path with `results/data/per_seed_pool_counts.csv` and emit only two count
   columns (`n_raw`, `n_unique`) — no `n_passing_filter` column, because no filter is applied. The
   loader: iterates `SOURCES`; opens each `*.json.gz` or `*.jsonl.gz` and branches on
   `path.suffixes` (`['.jsonl', '.gz']` → line-by-line JSONL, `['.json', '.gz']` → single JSON
   load and read the `"evaluations"` list); attaches the iteration variables `source_task` and
   `seed` plus an enumerated `individual_idx`; dedupes by the 68-d vector rounded to
   `DEDUP_DECIMALS = 6`; assembles a pandas DataFrame with columns
   `[source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, *ALL_PARAM_NAMES]`
   using explicit dtypes (`StringDtype` for `source_task`, `UInt32Dtype` for seed / generation /
   individual_idx, `float64` for the metric and 68 vector columns). Persist to
   `data/pooled_all_cells.parquet`. Run as
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0117_pooled_pca_cluster_factor_all_cells_4_seeds -- uv run python -u -m tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.load_pooled_cells`.
   Inputs: 4 predictions `*.gz` files. Outputs: `data/pooled_all_cells.parquet`,
   `results/data/per_seed_pool_counts.csv`. Expected observable: stdout reports the per-seed counts
   and a total pool count; `pooled_all_cells.parquet` exists with `n_unique` rows. Validation gate
   (~14k cells is well past the 100-item threshold and the load + dedup is non-trivial): after
   loading t0106 alone, print `n_raw` and `n_unique` and verify `n_raw == 3744` (per
   `research_code.md`'s per-seed totals); the trivial baseline / failure condition is
   **`n_raw == 0`** for any seed, which means the loader's format branching is broken or the source
   path is wrong — STOP and debug by reading 5 individual records from the offending file directly
   before continuing. Also assert `dedup_unique_total ≤ raw_total` and
   `dedup_unique_total > 0.5 × raw_total` (i.e., dedup should not collapse the pool to a tiny
   fraction — if it does, the rounding decimals are wrong). Inspect 5 individual rows of
   `pooled_all_cells.parquet` and verify every record has all 68 vector columns populated, no NaNs,
   and `source_task` / `seed` / `generation` / `individual_idx` are all consistent. Satisfies REQ-1,
   REQ-2, REQ-3.

3. **Write the gen-0 random-init loader.** Copy
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/load_pooled_gen0.py` into
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/load_pooled_gen0.py` verbatim and
   update the output path to `data/pooled_gen0.parquet`. The filter inside this loader
   (`generation == 1`) stays exactly as in t0116 — gen-0 was never DSI / PD-filtered there either,
   so no edit is required to the body of the loader. Inputs: same 4 predictions files. Outputs:
   `data/pooled_gen0.parquet`. Expected observable: stdout reports exactly 96 records per seed (pop
   slot count) and a total of `96 × 4 = 384` gen-0 rows. Validation gate: if any seed returns
   `n_gen0 != 96`, STOP and inspect — the file's generation indexing is broken or the filter is
   wrong (this is the same gate t0116 used and passed). Satisfies REQ-4.

4. **Fit the union-pool standardiser.** Add or reuse the `fit_pooled_standardiser(matrix)` function
   inside `code/cluster_helpers.py` (or a new `code/pooled_standardiser.py`, identical to the t0116
   file) returning a frozen dataclass with `mean: np.ndarray`, `std: np.ndarray` (with zero-std
   columns clipped to 1.0 to avoid division-by-zero), and a `transform(matrix)` method. Fit it once
   on the 68-d submatrix of `pooled_all_cells.parquet` (the full ~14k-cell pool) and serialise the
   resulting `mean` / `std` arrays to `data/pooled_standardiser.npz` so downstream steps and the
   gen-0 overlay reuse the **same** fit. Inputs: `data/pooled_all_cells.parquet`. Outputs:
   `data/pooled_standardiser.npz`. Expected observable: stdout prints `mean.shape == (68,)` and
   `std.shape == (68,)`; no zero or NaN values in `std`. Satisfies REQ-5.

5. **Run three PCAs and render `pca_combined.png`.** Copy
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/pooled_pca_with_overlay.py` into
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/pooled_pca_with_overlay.py` and
   update only the input parquet path (from `pooled_survivors.parquet` to
   `pooled_all_cells.parquet`). Load `data/pooled_all_cells.parquet` and
   `data/pooled_standardiser.npz`. Standardise the 68-d matrix using the pre-fitted standardiser.
   Slice into electrophys (columns 0-53) and morphology (columns 54-67) submatrices. Fit three
   `sklearn.decomposition.PCA(n_components=2)` instances: `pca_combined` on the full 68-d matrix,
   `pca_ephys` on the 54-d submatrix, `pca_morph` on the 14-d submatrix. Also fit
   `pca_ephys_3d = PCA(n_components=3)` on the 54-d submatrix for use in Step 9's representative
   table. Persist `pca_combined`, `pca_ephys`, `pca_morph`, `pca_ephys_3d` to `data/pca_models.pkl`
   (joblib-pickled dict). Render the 1×3 figure `results/images/pca_combined.png` using
   `matplotlib.pyplot.subplots(1, 3, figsize=(15, 5))`: main panel = combined 68-d, side panel A =
   electrophys, side panel B = morphology. Colour points by seed using `tab10[0..3]`; marker `o`
   filled; one legend entry per seed. Axis labels must read `PC1 ({pct:.1f}%)` and
   `PC2 ({pct:.1f}%)`. Inputs: `data/pooled_all_cells.parquet`, `data/pooled_standardiser.npz`.
   Outputs: `data/pca_models.pkl`, `results/images/pca_combined.png`. Expected observable: PNG file
   exists and is non-empty; stdout prints the variance-explained percentages for all three PCAs.
   Satisfies REQ-6.

6. **Project gen-0 and render `pca_with_gen0_overlay.png`.** Extend
   `code/pooled_pca_with_overlay.py` (or add a `render_gen0_overlay` function in the same file) to
   load `data/pooled_gen0.parquet`. Standardise its 68-d matrix using the **same**
   `data/pooled_standardiser.npz` from Step 4 (no refit). Project it onto each of the three PCAs
   from Step 5 via `pca.transform(...)` (no refit). Re-render the same 1×3 figure with gen-0 points
   drawn first as faint grey crosses (`marker='x'`, `color='#888888'`, `alpha=0.3`, `zorder=1`), and
   cohort points on top as in Step 5 (`zorder=2`). Save to
   `results/images/pca_with_gen0_overlay.png`. Compute per-seed mean and 95th-percentile Euclidean
   displacement in (a) PC1+PC2 space of `pca_combined` (cohort cells vs gen-0 mean for the same
   seed, taken as point-to-mean distance), and (b) the full 68-d standardised space. Emit
   `results/data/gen0_displacement.csv` with columns
   `seed, mean_disp_pc12, mean_disp_68d, p95_disp_pc12, p95_disp_68d, n_cohort, n_gen0`. Expected
   observable: PNG exists and is non-empty; CSV has exactly 4 rows (one per seed) plus a header.
   Satisfies REQ-7.

7. **KMeans on the 54-d electrophys subspace.** Copy
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/cluster_electrophys.py` into
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/cluster_electrophys.py` and update
   only the input parquet path (from `pooled_survivors.parquet` to `pooled_all_cells.parquet`). Load
   the cohort, apply the standardiser from `data/pooled_standardiser.npz` on the 54-d submatrix (do
   not refit). Call `run_kmeans_sweep(...)` from `cluster_helpers.py` with
   `K_SWEEP = (3, 4, 5, 6, 7)`; it returns `inertias`, `silhouettes`, and the best k by mean
   silhouette. Save the silhouette curve to `results/images/electrophys_silhouette.png` (k on
   x-axis, mean silhouette on y-axis, every k marked, best k highlighted). Save the per-cell cluster
   assignments and PCA-combined coordinates as `results/data/electrophys_clusters.csv` with columns
   `cluster_id, source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, pc1_combined, pc2_combined`.
   Print chosen k, per-cluster size, and per-seed × cluster contingency table to stdout. Inputs:
   `data/pooled_all_cells.parquet`, `data/pooled_standardiser.npz`, `data/pca_models.pkl`. Outputs:
   `results/images/electrophys_silhouette.png`, `results/data/electrophys_clusters.csv`. Expected
   observable: PNG and CSV both exist; chosen k is in `[3, 7]`; total cluster-assigned rows = total
   cohort rows. **Validation gate**: the silhouette computation is O(n²) at n ≈ 14000 and is the
   wall-clock bottleneck for the whole task (~30 min on a single laptop CPU). Run with
   `--limit 1000` first (a random subsample of 1000 cells) and verify the silhouette function
   returns a non-trivial value in (0, 1), the chosen k is finite, and the per-cluster contingency
   table is not degenerate (no cluster absorbing 90%+ of cells); if the small run returns
   `silhouette_score ≤ 0` for the best k, or if one cluster captures more than 90% of cells, STOP
   and inspect: read 5 cells' standardised feature vectors and the cluster centres directly — most
   likely the standardiser was misfit (one feature column dominating) or the data was not
   standardised at all. Do not proceed to the full ~14k run until the 1000-cell smoke test passes.
   Satisfies REQ-8.

8. **Render electrophys-cluster morphology grids.** Copy
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/morphology_rendering.py` and
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/render_electrophys_cluster_morphs.py` into
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/` verbatim; update only the input
   paths (cluster CSV and cohort parquet) to point at the t0117 file names. The renderer loads
   `results/data/electrophys_clusters.csv` and `data/pooled_all_cells.parquet`, joins the cluster
   labels onto the cohort rows, then for each cluster id in the headline-k partition: ranks rows
   descending by `dsi * pd_rate_hz`, takes the top 15, and renders a 5×3 grid using
   `_plot_cell(...)` per panel. Each panel must annotate
   `source_task[-5:] / seed / gen=N / DSI=0.XX / PD=YY.Y` in the upper-left corner so cross-seed
   identity is visible. Save each cluster's grid as
   `results/images/electrophys_cluster_<cluster_id>_morphs.png`. Use the `generate_fixed_morphology`
   library entry point
   (`from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`)
   and `MorphologyParams` from
   `tasks.t0090_morphology_generator_diversity_test.code.morphology_params`. The
   `morph_seed = int(round(x)) % (2**31 - 1)` coercion and the `h.delete_section(sec=s)` cleanup are
   already present in the copied `morphology_rendering.py` and must remain. Inputs:
   `results/data/electrophys_clusters.csv`, `data/pooled_all_cells.parquet`. Outputs: one PNG per
   electrophys cluster id (e.g., if headline k = 4, four PNGs). Expected observable: one PNG per
   cluster; stdout prints `Built <N> morphologies` and process RSS does not grow unboundedly thanks
   to the `h.delete_section` cleanup. **Validation gate**: render cluster 1 alone first; verify the
   PNG contains 15 visible dendrite trees with annotations; if any panel is blank or only shows a
   soma circle (no dendrites), STOP and debug — the pt3d extraction or `_plot_cell` adapter has a
   bug. Inspect the first cell's `result.all_dends` length and `len(result.h.x3d(...))` per section
   directly before continuing to the remaining clusters. Satisfies REQ-9.

9. **KMeans on the 14-d morphology subspace + representative table.** Copy
   `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/cluster_morphology.py` into
   `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/cluster_morphology.py` and update
   only the input parquet path (from `pooled_survivors.parquet` to `pooled_all_cells.parquet`). Same
   procedure as Step 7 but on the 14-d morphology submatrix. Replace any t0116-specific
   electrophys-overlay boxplots with a 15-row representative table per cluster: rank descending by
   `dsi * pd_rate_hz` within cluster, take top 15, and project each row's 54-d electrophys slice
   onto the **3-component** `pca_ephys_3d` from `data/pca_models.pkl` (fitted in Step 5). Emit
   `results/data/morphology_clusters.csv` (same column layout as Step 7's CSV) and
   `results/data/morphology_cluster_<cluster_id>_representatives.csv` per cluster with columns
   `source_task, seed, generation, dsi_vector_sum, pd_rate_hz, ephys_pc1, ephys_pc2, ephys_pc3`.
   Also save `results/images/morphology_silhouette.png` as the silhouette curve. The same O(n²)
   silhouette validation gate from Step 7 applies — if Step 7 passed the gate, Step 9 should pass
   too, but rerun the `--limit 1000` smoke test if Step 7's silhouette behaviour surprised the agent
   in any way. Inputs: `data/pooled_all_cells.parquet`, `data/pooled_standardiser.npz`,
   `data/pca_models.pkl`. Outputs: `results/images/morphology_silhouette.png`,
   `results/data/morphology_clusters.csv`, `results/data/morphology_cluster_<k>_representatives.csv`
   (one per cluster). Expected observable: silhouette PNG exists; per-cluster representative CSVs
   have 15 rows each; chosen k in `[3, 7]`. Satisfies REQ-10, REQ-11.

10. **Factor analysis on the full 68-d matrix.** Copy
    `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/factor_analysis.py` into
    `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/factor_analysis.py` (verbatim;
    update only the input parquet path). Replace `pooled_survivors.parquet` with
    `pooled_all_cells.parquet`. `run_factor_analysis` computes correlation-matrix eigenvalues via
    `np.linalg.eigvalsh(np.cov(z_matrix, rowvar=False, ddof=0))`, counts eigenvalues > 1.0
    (`n_eig_above_one`), caps factor count at `KAISER_FACTOR_CAP = 10`, refits FA with that count,
    applies `varimax_rotation`, and computes rotated factor scores via `Z @ Λ @ pinv(Λ.T @ Λ)`.
    Render the loadings heatmap at `results/images/factor_loadings_heatmap.png` with `RdBu_r`
    colourmap, `vmax = max(abs(loadings))`, `vmin = -vmax`, feature names from `ALL_PARAM_NAMES` on
    the y-axis, factor indices on the x-axis. Compute Pearson r between each rotated factor score
    and `dsi_vector_sum` / `pd_rate_hz`. Emit `results/data/factor_correlations.csv` with columns
    `factor_id, var_explained_pct, r_dsi, r_pd, joint_factor_flag` where
    `joint_factor_flag = (|r_dsi| > 0.30 AND |r_pd| > 0.30)`. Also emit
    `results/data/factor_loadings.csv` (raw loadings matrix, factors × 68 features). Print total
    variance explained and the per-factor table to stdout. Inputs: `data/pooled_all_cells.parquet`,
    `data/pooled_standardiser.npz`. Outputs: `results/images/factor_loadings_heatmap.png`,
    `results/data/factor_correlations.csv`, `results/data/factor_loadings.csv`. Expected observable:
    heatmap PNG exists; factor count is in `[1, 10]`; total variance explained percentage is
    printed; `factor_correlations.csv` has exactly `factor_count` data rows; the `joint_factor_flag`
    column has at least one True / False value (deliberately not predicting which, because the
    central question of the task is exactly whether any factor satisfies the joint threshold once
    the filter is dropped — but the column must be present and populated for every factor).
    Satisfies REQ-12, REQ-13.

11. **Compute cluster-vs-seed purity.** Copy
    `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/cluster_seed_purity.py` into
    `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/cluster_seed_purity.py` verbatim;
    update only the input CSV paths. Load `results/data/electrophys_clusters.csv` and
    `results/data/morphology_clusters.csv`. For each partition, compute (a)
    `sklearn.metrics.normalized_mutual_info_score(labels_true=seeds, labels_pred=clusters)` and (b)
    `scipy.stats.chi2_contingency(crosstab)` returning `(chi2, p_value, dof, expected)` on a pandas
    crosstab. Emit `results/data/cluster_seed_purity.csv` with columns
    `partition, nmi, chi2, p_value, dof` (two rows: `electrophys_k=<n>` and `morphology_k=<m>`).
    Print both rows to stdout. Inputs: the two cluster CSVs from Steps 7 and 9. Outputs:
    `results/data/cluster_seed_purity.csv`. Expected observable: CSV has 2 rows + header; NMI in
    `[0, 1]`; chi-square p-value reported. Satisfies REQ-14.

12. **Produce three answer assets.** Create the three answer asset folders
    `assets/answer/pooled-all-cells-basin-connectivity-without-filter/`,
    `assets/answer/pooled-all-cells-truncated-cohort-artefact-test/`, and
    `assets/answer/pooled-all-cells-displacement-from-init-full-pool/`. Each folder contains
    `details.json` (per `meta/asset_types/answer/specification.md`), a canonical short answer
    document `answer.md`, and a canonical full answer document `full.md`. Each `details.json` must
    set `answer_id` to the folder slug, `question` to the verbatim Q from `task_description.md`,
    `short_answer_path: "answer.md"`, `full_answer_path: "full.md"`,
    `added_by_task: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"`, and `answer_methods`
    listing `["asset-cross-reference", "code-experiment"]`. Short answers must be 2-5 sentences
    each, direct, citation-free in the `## Answer` block. Full answers must include
    `## Short Answer`, `## Evidence from Code or Experiments` (citing the CSVs and PNGs from Steps
    5-11 by exact relative path), `## Limitations` (note the still-present possibility of
    sub-threshold pollution / non-NSGA-II-relevant gen-0 noise dominating the FA), and `## Sources`
    containing markdown reference link definitions for all cited tasks (t0106, t0112, t0114, t0115,
    t0108, t0109, t0110, t0116 — t0116 is the direct head-to-head reference). Each full answer
    must include a "vs t0116" subsection citing the equivalent t0116 number it compares against
    (NMI, joint-factor count, per-seed displacement). Inputs: every artefact from Steps 5-11.
    Outputs: three asset folders. Expected observable: each `details.json` is valid JSON; each
    canonical short answer has 2-5 sentences; each canonical full answer has all four required
    sections plus the "vs t0116" subsection. Satisfies REQ-15.

13. **Emit methodology notes for the downstream reporting stage.** Create
    `results/data/methodology_notes.md` (a small ~30-line file consumed downstream by the
    orchestrator). Document: (a) the schema variance across the four sources (t0106 / t0112
    JSON-wrapped vs t0114 / t0115 JSONL); (b) `generation == 1` is the random init in all four
    files; (c) `joint_pass` / `legit` booleans on t0114 / t0115 records are ignored — and, in
    contrast to t0116, **no DSI / PD cohort filter is applied either**; (d) the union-pool
    standardiser is fit once on the ~14k unfiltered pool and reused (not refit per seed); (e) no
    registered metric from `meta/metrics/` applies because this task performs no new simulations —
    DSI and PD are backfilled from frozen predictions assets; (f) the head-to-head comparison vs
    t0116 is computed by reading t0116's published numbers (electrophys NMI = 0.929, morphology NMI
    = 0.889, joint-factor count = 0, per-seed displacements) and pasting them into the downstream
    reporting stage's comparison table — t0117 does not recompute any t0116 number from scratch.
    Also emit a parallel `results/data/t0116_comparison.csv` table with one row per quantity
    compared (pool size, KMeans k, electrophys NMI, morphology NMI, electrophys silhouette,
    morphology silhouette, varimax factor count, total variance explained, joint-factor count, plus
    one row per seed for the displacement metrics) — `t0116_value`, `t0117_value`, `delta` — so
    the orchestrator-managed reporting stage can consume the comparison data without re-deriving any
    numbers. Inputs: prior knowledge from t0116's `research/research_code.md`, t0116's published
    numbers from `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/`, and this task's
    implementation log. Outputs: `results/data/methodology_notes.md`,
    `results/data/t0116_comparison.csv`. Expected observable: methodology notes file exists and
    contains the six bullet points above; the comparison CSV has at least one row per quantity
    listed. Satisfies REQ-17.

## Remote Machines

None required. This is a CPU-only pandas + scikit-learn + matplotlib + NEURON-build analysis
designed to run on a single laptop CPU in ~60-90 minutes wall clock (silhouette on ~14k cells
dominates). No GPU, no cluster, no Vast.ai, no cloud egress.

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
* Reference code (copied, not imported) from
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/code/` — every module (`paths.py`,
  `constants.py`, `cluster_helpers.py`, `factor_analysis.py`, `load_pooled_cells.py`,
  `load_pooled_gen0.py`, `morphology_rendering.py`, `pooled_pca_with_overlay.py`,
  `cluster_electrophys.py`, `cluster_morphology.py`, `render_electrophys_cluster_morphs.py`,
  `cluster_seed_purity.py`). All copied verbatim; only `load_pooled_cells.py` has its filter clause
  deleted.
* Reference numbers (read, not copied) from
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/` — pool size 869, electrophys NMI
  0.929, morphology NMI 0.889, joint-factor count 0, per-seed displacements. These are pasted into
  the head-to-head comparison table in `results_detailed.md` by the downstream reporting stage.

## Expected Assets

Per `task.json` `expected_assets`: 3 answer assets.

* `assets/answer/pooled-all-cells-basin-connectivity-without-filter/` — answers Q1: "Does the
  unfiltered pool form a connected manifold across seeds, or does the seed-specific basin pattern
  from t0116 persist when low-DSI / low-PD cells are admitted?" Evidence: `pca_combined.png`,
  `pca_with_gen0_overlay.png`, `cluster_seed_purity.csv` (NMI + chi-square), head-to-head NMI vs
  t0116 (0.929 / 0.889).
* `assets/answer/pooled-all-cells-truncated-cohort-artefact-test/` — answers Q2: "Does at least
  one varimax factor recover a joint DSI-PD axis (`|r_DSI| > 0.3` AND `|r_PD| > 0.3`) when the full
  quality range is in the pool?" Evidence: `factor_loadings_heatmap.png`, `factor_correlations.csv`
  (per-factor Pearson r with DSI / PD, `joint_factor_flag` column), `factor_loadings.csv`.
  Head-to-head vs t0116: t0116 found 0 joint factors at the strict cohort.
* `assets/answer/pooled-all-cells-displacement-from-init-full-pool/` — answers Q3: "How far did
  NSGA-II travel from gen-0 in each seed when the full quality range is in the pool, and is the
  per-seed displacement pattern from t0116 (seed 44 furthest, seed 9354 closest) preserved?"
  Evidence: `pca_with_gen0_overlay.png`, `gen0_displacement.csv` (per-seed mean and 95th-percentile
  Euclidean displacement in PC1+PC2 and full 68-d standardised spaces), head-to-head displacement
  table vs t0116.

## Time Estimation

* Module scaffolding (Step 1): ~5 minutes — copy 12 files from t0116, update path constants.
* Loaders + standardiser fit (Steps 2-4): ~10 minutes wall clock for the IO + Parquet writes (~14k
  records vs t0116's 869 — IO is still trivial; the dedupe is O(n) on rounded vectors).
* PCA + gen-0 overlay rendering (Steps 5-6): ~5 minutes — PCA on a 14k × 68 matrix is sub-second;
  the matplotlib render is the bulk of the time.
* KMeans sweeps + silhouette PNGs (Steps 7 and 9): ~30-45 minutes per partition — silhouette is
  O(n²) at n ≈ 14000; this is the wall-clock bottleneck.
* Morphology grid rendering (Step 8): ~10 minutes for ≤ 105 NEURON cell builds + matplotlib output
  (same cost as t0116; cluster count drives this, not pool size).
* Factor analysis + heatmap (Step 10): ~3 minutes — FA on a 14k × 68 matrix is dominated by the
  `n_components=68` initial fit.
* Purity computation (Step 11): < 1 minute.
* Answer asset authoring (Step 12): ~30 minutes — three small markdown documents plus three
  `details.json` files, each including a "vs t0116" subsection.
* Methodology notes (Step 13): ~5 minutes.
* **Total implementation wall clock**: ~75-115 minutes (excluding the orchestrator-managed
  downstream stages that follow implementation). The 60-90-minute estimate in `task_description.md`
  assumes the morphology grid and answer-asset authoring overlap with the KMeans wall-clock; that
  assumption is preserved here.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Container-format branch mishandles t0114 / t0115 JSONL (loader returns empty cohort for either seed) | Low (already de-risked by t0116) | Blocking — Q1 / Q2 / Q3 all depend on a non-trivial pool | Step 2 includes a validation gate that prints per-seed `n_raw` and `n_unique`; STOP-and-debug if any seed reports `n_raw == 0`. Confirm by reading 5 individual records from the offending file directly. |
| Silhouette score O(n²) blows up wall-clock or memory at n ≈ 14000 | High | Step 7 / Step 9 hangs or runs out of memory | Step 7 includes a `--limit 1000` validation gate; if the small run takes > 5 minutes, expect the full run to take 5 × (14²) = ~16 hours and either: (a) use `sklearn.metrics.silhouette_score(sample_size=2000)` to subsample, or (b) compute silhouette on a held-out 5000-cell subsample, but record this departure in `methodology_notes.md`. Default is to run the exact silhouette and budget for ~30-45 min per partition. |
| Dedup rounding collapses ~14k pool to a tiny fraction because the same 68-d vector is repeated across many records | Medium | The pool ends up much smaller than expected (e.g., a few hundred); cross-seed comparison degraded | Step 2's validation gate asserts `dedup_unique_total > 0.5 × raw_total`; if it fails, log per-seed dedup ratios and inspect: most likely a single seed has a degenerate sub-population repeating the same vector. Report the dedup-induced losses explicitly in `methodology_notes.md` and proceed with the dedup-unique pool (do not relax the rounding rule, because t0116 used the same convention and the analyses must remain directly comparable). |
| Joint-factor question (Q2) returns ambiguous result: one factor is exactly at ` | r | = 0.30` | Low |
| Truncated-cohort artefact (per t0110 / t0116) — fact that the unfiltered pool admits many DSI ≈ 0 / PD ≈ 0 cells from early NSGA-II generations may itself bias the factor structure toward a different "low-quality" axis | Medium | Q3 conclusions may reflect "early-generation noise" rather than substrate properties | Report `n_eig_above_one` (raw Kaiser count) alongside the capped factor count; note explicitly in the Q2 / Q3 answer assets' `## Limitations` section that the unfiltered pool includes many gen-1 / gen-2 random-init survivors that NSGA-II discarded by gen-50. The answer asset must acknowledge that t0117's "joint factor" may differ qualitatively from a hypothetical "all-NSGA-II-converged" joint factor — the relevant comparator is still t0116 (the strict-quality cohort), not a never-published "perfectly converged" cohort. |
| NEURON RSS creep when building > 100 morphologies in one process | Low (mitigated by t0109's `h.delete_section` cleanup, copied via t0116) | Process may crash or swap on a laptop with 8 GB RAM | The `h.delete_section(sec=s)` cleanup is already in the copied `morphology_rendering.py`. If RSS still grows, render each cluster's grid in a separate subprocess via `multiprocessing.Process`. |
| Headline `k` differs sharply between the electrophys and morphology partitions (e.g., 3 vs 7) | Medium | Cross-partition narrative becomes harder; risk of cherry-picking which partition to highlight | Step 7 and Step 9 both report the full silhouette curve over `k ∈ {3, 4, 5, 6, 7}`; the answer asset must report both headline k's side by side and refrain from declaring either as "the right one". |
| `morph_seed` cast to int overflows INT32 in a corner record | Low | NEURON `Random()` raises ValueError; cell build crashes | Apply the `int(round(x)) % (2**31 - 1)` coercion (t0109 line 130) before passing `morph_seed` to `MorphologyParams.from_dict`. Already present in the copied `morphology_rendering.py`. |
| Standardiser accidentally refit per seed inside one of the cluster scripts | Low (intent: guard by passing the `data/pooled_standardiser.npz` arrays explicitly) | Silently invalidates every cross-seed comparison — the very signal the task is designed to detect would be erased | Encode the fit as a single function returning a frozen dataclass and load it from `data/pooled_standardiser.npz` in every downstream script. Never instantiate `sklearn.preprocessing.StandardScaler` inside a per-seed loop. |

## Verification Criteria

Each criterion below names an exact command to run and the observable signal that confirms it.

* **C1 (REQ-3, REQ-4)**: `pooled_all_cells.parquet` exists, the row count equals the sum of per-seed
  dedup-unique counts logged at load time, and `pooled_gen0.parquet` has exactly 384 rows (96 per
  seed × 4 seeds). Run:
  `uv run python -c "import pandas as pd; from pathlib import Path; df_p = pd.read_parquet(Path('tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet')); df_g = pd.read_parquet(Path('tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_gen0.parquet')); print(len(df_p), len(df_g), df_p.groupby('seed').size().to_dict(), df_g.groupby('seed').size().to_dict())"`.
  Expected: `len(df_p) > 5000` (much larger than t0116's 869), `len(df_g) == 384`, every seed's
  `df_g` count is exactly 96.

* **C2 (REQ-5)**: The pooled standardiser was fitted once on the union pool and saved to
  `data/pooled_standardiser.npz`. Run:
  `uv run python -c "import numpy as np; s = np.load('tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_standardiser.npz'); print(s['mean'].shape, s['std'].shape, bool(np.all(s['std'] > 0)))"`.
  Expected: shapes are `(68,)`, `(68,)`, and `np.all(s['std'] > 0)` is `True`.

* **C3 (REQ-6, REQ-7, REQ-8, REQ-10, REQ-12)**: Every chart referenced in the plan exists on disk
  under `results/images/`. Run:
  `uv run python -c "from pathlib import Path; root = Path('tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images'); required = ['pca_combined.png', 'pca_with_gen0_overlay.png', 'electrophys_silhouette.png', 'morphology_silhouette.png', 'factor_loadings_heatmap.png']; missing = [n for n in required if not (root / n).exists()]; assert missing == [], missing; print('all required PNGs present')"`.
  Expected: prints `all required PNGs present`. Additionally, at least one
  `electrophys_cluster_*_morphs.png` exists in the same directory.

* **C4 (REQ-15)**: The three answer asset folders exist and each contains `details.json`,
  `answer.md`, and `full.md`. Run:
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
  and verify zero errors on all three asset slugs
  `pooled-all-cells-basin-connectivity-without-filter`,
  `pooled-all-cells-truncated-cohort-artefact-test`,
  `pooled-all-cells-displacement-from-init-full-pool`. Expected: exit code 0 and no error-level
  diagnostics.

* **C5 (REQ-1, REQ-2, REQ-3, REQ-17 — schema sanity)**: The pooled cohort file contains the 68
  named vector columns from `ALL_PARAM_NAMES`, no nulls in those columns, and the pool covers a wide
  DSI / PD range (not the t0116-strict cut). Run:
  `uv run python -c "import pandas as pd; from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.constants import ALL_PARAM_NAMES; df = pd.read_parquet('tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet'); assert set(ALL_PARAM_NAMES).issubset(df.columns); assert df[list(ALL_PARAM_NAMES)].isna().sum().sum() == 0; assert df['dsi_vector_sum'].min() < 0.7, 'pool should include low-DSI cells (no cohort filter)'; print('schema ok; dsi range', df['dsi_vector_sum'].min(), df['dsi_vector_sum'].max())"`.
  Expected: prints `schema ok` with `dsi range` showing a minimum well below 0.7.

* **C6 (plan structure)**: The plan verificator passes with zero errors. Run:
  `uv run python -u -m arf.scripts.verificators.verify_plan t0117_pooled_pca_cluster_factor_all_cells_4_seeds`.
  Expected: exit code 0 and no error-level diagnostics.

* **C7 (REQ coverage)**: Every `REQ-*` item from `## Task Requirement Checklist` is referenced by at
  least one step in `## Step by Step`. Spot-check by grepping the plan for `REQ-1` through `REQ-17`
  and confirming each appears at least once in the Step by Step section. This is a manual check the
  reviewer can run with a single grep over `plan.md`; the verificator's `PL-W007` check also
  validates that `REQ-*` markers appear in `## Step by Step`.
