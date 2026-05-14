---
spec_version: "2"
task_id: "t0105_cluster_factor_analysis_dsi_pd"
date_completed: "2026-05-14"
status: "complete"
---
# Plan: Cluster + Factor Analysis of High-DSI / High-PD Cells across All Four 68-d Optimisations

## Objective

Pool every per-cell evaluation from the four 68-d NSGA-II lineages — t0091 (warm-start 3-obj),
t0099 (random-init 3-obj N=20), t0102 (random-init 3-obj N=4), and t0104 (random-init 2-obj N=4 with
the S-0102-01 DSI-silence guard) — apply the primary filter `DSI > 0.1 AND PD > 2 Hz`, dedupe by
the 68-d parameter vector (rounded to 6 decimals), and run three analyses on the resulting ~86
unique cells: (1) build a stratified morphology gallery showing the dendritic trees of
representative cells annotated with DSI, PD, asymmetry score, and source task; (2) run PCA on the
54-d electrophys submatrix, classify each cell as symmetric vs asymmetric by a normalised asymmetry
score, plot PC1-vs-PC2 coloured by class, DSI, PD, and source task, and report a Mann-Whitney U test
on PC1 / PC2 scores between symmetric and asymmetric cells; (3) run factor analysis with varimax
rotation on the full 68-d matrix, choose factor count by Kaiser criterion capped at 10, compute
Pearson correlations between factor scores and DSI / PD, and flag any joint-DSI-PD factor where
`|r_DSI| > 0.3 AND |r_PD| > 0.3`. Re-run every headline analysis on the strict cohort
`DSI > 0.2 AND PD > 3 Hz` (~31 cells) as a sensitivity check. Produce two answer assets — one for
"do symmetric and asymmetric cells share the same electrophys regime?" and one for "which factors
explain DSI / PD diversity?". Success criteria: both answer assets exist and validate, all charts
are saved at 150-180 DPI and embedded in `results_detailed.md`, the primary-cohort PCA and factor
results in `results_detailed.md` match values in `results/metrics.json`, the verificator
`verify_plan` passes with 0 errors, and total spend is **$0** (pure local analysis on existing
predictions data; no remote compute, no paid APIs).

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0105_cluster_factor_analysis_dsi_pd/task.json` and the resolved
long description at `tasks/t0105_cluster_factor_analysis_dsi_pd/task_description.md`:

```text
Name: Cluster + factor analysis of high-DSI/high-PD cells
      (t0102 + t0104, symmetric vs asymmetric)

Short description: Pool all cells from t0102 and t0104 with DSI > 0.2 AND PD > 3 Hz, classify
by morphological asymmetry, run PCA cluster analysis on intrinsic params, and factor analysis
(incl. morphology) on what explains DSI / PD diversity.

Long description (excerpts — see task_description.md for full text):
* Pool ALL 4 68-d optimisation lineages (t0091 + t0099 + t0102 + t0104), 7,003 cells total.
* Primary filter DSI > 0.1 AND PD > 2 Hz (~86 unique cells expected); strict filter DSI > 0.2
  AND PD > 3 Hz (~31 cells) as sensitivity check.
* Dedupe by 68-d vector rounded to 6 decimals; record per-lineage cell counts.
* Apply silenced-cell artifact filter (exclude DSI > 0.95 AND PD < 5) from
  t0091/t0099/t0102 (t0104 already has the guard).
* Compute normalised asymmetry score; classify symmetric (<0.5) vs asymmetric (>=0.5).
* Build morphology gallery (stratified subsample <=30 by class x source_task; deterministic
  selection top-by-DSI*PD within each stratum).
* PCA on 54-d electrophys submatrix; PC1 vs PC2 scatter coloured by class, DSI, PD, and
  source task; report variance explained and top-5 loadings per PC.
* Mann-Whitney U test on PC1 (and PC2) scores between symmetric and asymmetric cells.
* Factor analysis on full 68-d with varimax rotation; Kaiser criterion (eigenvalues > 1)
  capped at 10 factors; report loadings.
* Pearson r between each factor and DSI / PD; identify top-3 factors per outcome; flag any
  joint factor (|r_DSI| > 0.3 AND |r_PD| > 0.3).
* Bootstrap factor loadings (200 resamples); report 95% CIs; only highlight stable factors
  (consistent signs, median |lambda| > 0.4).
* Repeat all headline analyses on the strict cohort (DSI > 0.2 AND PD > 3).
* Two answer assets: symmetric-vs-asymmetric-electrophys-cluster and
  dsi-pd-diversity-factor-decomposition.
* All charts saved to results/images/ at 150-180 DPI; embedded in results_detailed.md.

Expected assets: 2 answer assets.
Out of scope: re-running optimisation, in silico patch-clamp, external dataset comparison.
```

Concrete requirements decomposed (each item names the step(s) that satisfy it and the evidence that
proves completion):

* **REQ-1** — Pool every per-cell evaluation row from the four 68-d optimisation lineages by
  reading `tasks/t0091_morphology_extended_nsga2_v1/results/data/all_evaluations.json`,
  `tasks/t0099_random_init_pareto_robustness/results/data/all_evaluations_seed{11,22,33}.json`,
  `tasks/t0102_seedscale_n4_gen20/results/data/all_evaluations_seed{44,55}.json`, and
  `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/all_evaluations_seed{44,55}.json`. Apply
  the primary filter `dsi_vector_sum > 0.1 AND pd_rate_hz > 2.0` and the strict filter
  `dsi_vector_sum > 0.2 AND pd_rate_hz > 3.0`. Dedupe by the 68-d parameter vector rounded to 6
  decimals. Tag each retained row with `source_task` (one of `t0091`, `t0099`, `t0102`, `t0104`) and
  `seed` (where applicable). Record `N_raw`, `N_passing`, `N_unique` per lineage and per filter
  threshold. Satisfied by step 4. Evidence: `tasks/t0105_*/results/data/selected_cells_primary.json`
  and `selected_cells_strict.json` exist and the per-lineage counts are mirrored in
  `results/data/selection_counts.json`.

* **REQ-2** — Add `factor_analyzer>=0.5.1` to `[project].dependencies` in the top-level
  `pyproject.toml` and refresh `uv.lock`. This is a top-level tooling change explicitly allowed by
  the framework's exception list (`pyproject.toml`, `uv.lock`, `ruff.toml`, `.gitignore`,
  `mypy.ini`). Satisfied by step 2. Evidence: `grep -n 'factor_analyzer' pyproject.toml` returns one
  line in the dependencies block; `grep -n 'factor_analyzer' uv.lock` returns at least one block
  describing the locked version;
  `uv run python -c "import factor_analyzer; print(factor_analyzer.__version__)"` prints a version
  `>=0.5.1`.

* **REQ-3** — Apply the silenced-cell artifact filter to t0091, t0099, and t0102 rows by excluding
  cells where `dsi_vector_sum > 0.95 AND pd_rate_hz < 5.0` before the primary / strict filter is
  applied. t0104 already has the S-0102-01 guard in-evaluator so no post-hoc re-filtering is needed
  for t0104 rows. Log the per-lineage exclusion counts. Satisfied by step 4. Evidence:
  `results/data/selection_counts.json` contains a `silence_artifact_exclusions` block with
  per-lineage counts; the unit test `code/test_load_filter_cells.py::test_silence_filter` passes.

* **REQ-4** — Compute the normalised asymmetry score for each selected cell using the formula:

  ```text
  asym_score = abs(soma_offset_pd_um) / 150
             + abs(field_elongation_pd - 1.0) / 2.0
             + abs(branch_density_gradient_pd) / 1.0
             + abs(primary_branch_pd_concentration) / 5.0
  ```

  Classify each cell as `symmetric` when `asym_score < 0.5` and `asymmetric` when
  `asym_score >= 0.5`. Report class counts and the histogram of `asym_score` in
  `results/data/asym_score_distribution.json` and as an `results/images/asym_score_histogram.png`
  chart. Also report a 0.3 / 0.5 / 1.0 threshold sweep in `results_detailed.md` to confirm class
  balance is not pathological at the headline 0.5 threshold. Satisfied by step 5. Evidence:
  `results/data/asym_score_distribution.json` lists `symmetric_count`, `asymmetric_count`, and
  per-threshold sweep counts; the histogram chart exists.

* **REQ-5** — Build a morphology gallery as a stratified subsample of up to 30 cells, stratified
  by `(asymmetry_class, source_task)`. Within each stratum select the top cells by `DSI * PD`
  deterministically (no random seed needed because the ordering is data-driven). Render each cell by
  building its 14-d morphology with
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`,
  extracting `soma + all_dends` pt3d coordinates, plotting the top-down (x, y) projection with the
  soma marked, and annotating DSI, PD, `asym_score`, and `source_task`. Output:
  `results/images/morphology_gallery.png`. If the primary cohort has fewer than 30 cells after
  filtering, plot all cells. Record the (class, source_task) quota table in `results_detailed.md`.
  Satisfied by step 6. Evidence: `results/images/morphology_gallery.png` exists and the per-stratum
  quota table is referenced in `results_detailed.md`.

* **REQ-6** — Run PCA on the 54-d electrophys submatrix `X_electrophys` of the primary-cohort
  selected cells using `sklearn.decomposition.PCA`. Standardise each column by z-score before
  fitting. Keep PC1, PC2, PC3. Produce a single multi-panel chart
  `results/images/pca_electrophys_panels.png` with four panels: (a) PC1 vs PC2 coloured by asymmetry
  class (symmetric=blue, asymmetric=red); (b) PC1 vs PC2 coloured by DSI (continuous viridis
  colormap); (c) PC1 vs PC2 coloured by PD (continuous plasma colormap); (d) PC1 vs PC2 coloured by
  `source_task` (categorical). Report variance explained by PC1, PC2, PC3 and the top-5 loading
  dimensions on each of PC1, PC2, PC3 with parameter name and signed loading magnitude. Satisfied by
  step 7. Evidence: `results/data/pca_results.json` contains the variance-explained list and top-5
  loadings per PC; `results/images/pca_electrophys_panels.png` exists.

* **REQ-7** — Compute a Mann-Whitney U test on PC1 scores between symmetric and asymmetric cells,
  and on PC2 scores. Use `scipy.stats.mannwhitneyu` with two-sided alternative. Report the U
  statistic, p-value, and a brief interpretation for each. Satisfied by step 7. Evidence:
  `results/data/pca_mannwhitney.json` contains the keys `pc1_u`, `pc1_p`, `pc2_u`, `pc2_p`, and
  `interpretation` strings.

* **REQ-8** — Run factor analysis on the full 68-d standardised matrix `X_full` using
  `factor_analyzer.FactorAnalyzer(rotation="varimax")`. Choose the factor count by the Kaiser
  criterion (count of eigenvalues > 1 on the correlation matrix) capped at 10. Compute factor
  loadings as a `(68, n_factors)` matrix and factor scores as a `(N_selected, n_factors)` matrix.
  Render the loadings as a heatmap at `results/images/factor_loadings.png`. List the top-5 loading
  parameters per factor (parameter name and signed loading) in `results/data/factor_loadings.json`.
  Satisfied by step 8. Evidence: `results/data/factor_loadings.json` exists with `n_factors`,
  `eigenvalues_above_1_count`, and a `per_factor_top_loadings` block;
  `results/images/factor_loadings.png` exists.

* **REQ-9** — Compute Pearson r between each factor score column and DSI, and between each factor
  score column and PD, using `scipy.stats.pearsonr`. Identify the top-3 factors per outcome by
  `|r|`. Flag any factor where `|r_DSI| > 0.3 AND |r_PD| > 0.3` as a joint-DSI-PD factor. Render
  `results/images/factor_correlations.png` as a grouped bar chart of `|r|` vs DSI and `|r|` vs PD
  across factors. Satisfied by step 9. Evidence: `results/data/factor_correlations.json` contains
  per-factor `r_dsi`, `p_dsi`, `r_pd`, `p_pd`, a `top3_dsi` list, a `top3_pd` list, and a
  `joint_factors` list (may be empty).

* **REQ-10** — Bootstrap the factor loadings with 200 resamples (resample cells with replacement;
  refit the factor analyser on each resample; record loadings). Report 95% CIs per loading entry
  using percentile bootstrap. Highlight stable factors as those whose top-5 loading parameters
  retain consistent signs across resamples and whose median absolute loading exceeds 0.4. Render
  `results/images/factor_loadings_bootstrap.png` overlaying the CI bars on the headline loadings
  heatmap row(s) for the top loadings. Satisfied by step 10. Evidence:
  `results/data/factor_bootstrap.json` contains `n_bootstrap_resamples`, per-loading CIs, and a
  `stable_factors` list.

* **REQ-11** — Repeat steps 6, 7, 8, 9 on the strict cohort (`DSI > 0.2 AND PD > 3.0`). Document
  any qualitative change in `results_detailed.md` (e.g., a factor disappearing, sign flipping, or
  correlation strength changing). Save strict-cohort outputs in parallel files:
  `results/data/pca_results_strict.json`, `results/data/factor_loadings_strict.json`,
  `results/data/factor_correlations_strict.json`,
  `results/images/pca_electrophys_panels_strict.png`, `results/images/factor_loadings_strict.png`,
  `results/images/factor_correlations_strict.png`. Satisfied by step 11. Evidence: all six strict
  files exist.

* **REQ-12** — Build two answer assets:

  1. `tasks/t0105_*/assets/answer/symmetric-vs-asymmetric-electrophys-cluster/` answering "Do
     symmetric and asymmetric DSGC morphologies share the same electrophys parameter regime, or do
     they form distinct clusters in PC space?" Evidence: the PCA panels chart, the Mann-Whitney U
     test, top-5 loadings per PC. Cite t0091, t0099, t0102, t0104 source-task predictions and the
     t0086 cluster-analysis precedent.

  2. `tasks/t0105_*/assets/answer/dsi-pd-diversity-factor-decomposition/` answering "Which factors
     (combinations of the 68 input parameters) explain DSI diversity versus PD diversity, and is
     there a joint factor or are the two outcomes orthogonal?" Evidence: factor loadings heatmap,
     per-factor Pearson r vs DSI / PD, bootstrap CIs, joint-factor flag. Cite the same four
     predictions sources and reference Mohacsi 2024, Sivyer 2013, Vaney 2012 where literature
     alignment is needed.

  Each answer asset must follow `meta/asset_types/answer/specification.md` (details.json,
  short_answer.md, full_answer.md). Satisfied by step 12. Evidence:
  `uv run python -m arf.scripts.verificators.verify_answer_asset tasks/t0105_*/assets/answer/symmetric-vs-asymmetric-electrophys-cluster`
  exits 0, and the same for `dsi-pd-diversity-factor-decomposition`.

* **REQ-13** — Save every chart to `results/images/` at 150-180 DPI and embed each one in
  `results_detailed.md` with the `![description](images/filename.png)` syntax. Charts to produce:
  `morphology_gallery.png`, `asym_score_histogram.png`, `pca_electrophys_panels.png`,
  `pca_electrophys_panels_strict.png`, `factor_loadings.png`, `factor_loadings_strict.png`,
  `factor_correlations.png`, `factor_correlations_strict.png`, `factor_loadings_bootstrap.png`,
  `eigenvalue_scree.png`. Every chart must have a title, labelled axes, and a legend where
  applicable. Satisfied by all chart-producing steps (5, 6, 7, 8, 9, 10, 11) and the orchestrator
  results-writing step. Evidence: `ls tasks/t0105_*/results/images/*.png | wc -l` returns at least
  10\.

* **REQ-14** — Write `results/metrics.json` in the explicit multi-variant format with two
  variants: `primary_cohort` and `strict_cohort`. Each variant records the four registered metric
  keys aggregated across the cohort's selected cells: `direction_selectivity_index` (median DSI in
  cohort), `tuning_curve_hwhm_deg` (set to `null` because tuning-curve HWHM is not available from
  the pooled predictions data), `tuning_curve_reliability` (set to `null` for the same reason —
  t0091/t0099/t0102/t0104 did not store per-trial Pearson reliability in `all_evaluations*.json`),
  `tuning_curve_rmse` (set to `null` — RMSE against a target tuning curve is not stored in the
  pooled predictions data). The `null` values are explicit, per the styleguide rule "use `None` for
  missing data, never zero or empty string"; the explicit reasoning is documented in
  `results_detailed.md`. Satisfied by step 13. Evidence:
  `jq '.variants | keys' tasks/t0105_*/results/metrics.json` prints
  `["primary_cohort", "strict_cohort"]` and each variant contains all four registered metric keys
  (with explicit nulls where data is unavailable).

* **REQ-15** — Do not modify any prior task folder (immutability). Only files under
  `tasks/t0105_cluster_factor_analysis_dsi_pd/` plus the allowlisted top-level tooling files
  (`pyproject.toml`, `uv.lock`, `ruff.toml`, `.gitignore`, `mypy.ini`) may change. Satisfied
  implicitly across every step. Evidence: post-task `git diff main -- tasks/ | head` shows changes
  only under `tasks/t0105_cluster_factor_analysis_dsi_pd/`.

* * *

## Approach

### Technical approach

t0105 is a pure local-analysis task with no remote compute, no paid APIs, and no new optimisation.
Every input already exists on disk in the four predecessor task folders. The implementation pulls
per-cell evaluation rows from
`tasks/t0091_morphology_extended_nsga2_v1/results/data/all_evaluations.json` (a single file covering
187 cells across one warm-start lineage) and from the per-seed files `all_evaluations_seed*.json` in
t0099 (seeds 11, 22, 33; ~2,016 cells total), t0102 (seeds 44, 55; ~2,592 cells), and t0104 (seeds
44, 55; ~2,208 cells), for 7,003 raw rows in total. Every row shares the schema
`{generation, vector_68d, objective_F_minimised, dsi_vector_sum, pd_rate_hz, robustness}` except
t0104's, which lacks the `robustness` field by design (it ran 2-objective NSGA-II). The pooling code
tolerates the missing key and fills with `None`.

The 68-d vector splits `[54 electrophys | 14 morphology]`. The 14 morphology dimensions are
documented in `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants_morphology.py` (lines 18-33)
and three of them are integer dimensions (`num_primary_branches`, `max_strahler_depth`,
`morph_seed`) that must be rounded before being passed to `MorphologyParams.from_dict`. The four
PD-asymmetry dimensions used by the asymmetry-score formula are `soma_offset_pd_um` (dim 5),
`field_elongation_pd` (dim 6), `branch_density_gradient_pd` (dim 7),
`primary_branch_pd_concentration` (dim 8).

The silenced-cell artifact (DSI ~= 1.0 when total spikes < 10) is the dominant pre-guard pollution
in t0091, t0099, and t0102. t0104 fixed this in-evaluator with the S-0102-01 guard; for the older
three lineages we apply a conservative post-hoc filter `DSI > 0.95 AND PD < 5 Hz` that captures the
same artifact pattern without requiring re-evaluation. The exclusion counts are logged per-lineage
in `results/data/selection_counts.json`.

PCA on the 54-d electrophys submatrix uses standard `sklearn.decomposition.PCA` after z-scoring
columns. The 86 unique cells in the primary cohort give a passable N/p ratio of 86/54 ~= 1.6, which
is enough for PC1-PC2-PC3 interpretation but not for PC4+ (consistent with t0086's prior finding
that PC1-PC2 captured ~45% of variance on a similar-scale problem). The Mann-Whitney U test between
symmetric and asymmetric PC1 / PC2 scores avoids the normality assumption that would be unsupported
at N=86 split across two classes.

Factor analysis on the full 68-d matrix uses `factor_analyzer.FactorAnalyzer(rotation="varimax")`
because sklearn's `FactorAnalysis` lacks a built-in varimax rotation in 1.8.0 and a hand-rolled
varimax would add risk for no benefit. The package is added to `pyproject.toml` as part of REQ-2.
Factor count comes from the Kaiser criterion (eigenvalues > 1 on the correlation matrix) capped at
10 because more factors at N=86 would overfit. Bootstrap CIs on loadings (200 resamples) provide a
stability check; stable factors are those whose top-5 loading signs are consistent across resamples
and whose median absolute loading exceeds 0.4.

The morphology gallery reuses the working prototype from `scratch_t0102_t0104_morph_compare.py` on
main (commit `e600e3f0`) which builds 10 cells in ~30 s. Adapted to t0105's stratified subsampling
logic: within each (asymmetry_class, source_task) stratum, take the top cells by `DSI * PD` until
the per-stratum quota is met. At eight strata (2 classes x 4 sources) and a 30 cell budget, the
per-stratum quota is `min(stratum_size, ceil(30 / nonempty_strata))`. The build path is
`generate_fixed_morphology(params=MorphologyParams.from_dict(...))` from t0092 / t0090 (importable
directly since these are part of the `de_rosenroll_2026_dsgc` library per t0093 / t0090 correction
patches).

The strict cohort (`DSI > 0.2 AND PD > 3 Hz`) at ~31 unique cells is too small for stable factor
analysis (N/p ~= 31/68 ~= 0.46) but supports a sensitivity comparison: rerun every headline analysis
and document any qualitative change (factor disappearance, sign flip, correlation-strength shift).
The strict-cohort PCA at N=31 on 54 dims is also unstable, so we constrain interpretation to PC1-PC2
and report variance-explained without claiming significance on PC3.

### Alternatives considered

* **k-means clustering instead of PCA + classification by asymmetry**. Rejected: the task question
  is whether the morphology-based asymmetry classes correspond to electrophys clusters, which
  requires the classification to be defined a priori from morphology. k-means would produce
  data-driven clusters whose alignment with morphology classes is then a derived question; this
  changes the analysis from "do morphology classes cluster in electrophys space?" to "do
  unsupervised clusters align with morphology labels?". The latter is less direct and more sensitive
  to k. t0086's k-means precedent on a 54-d Pareto library still informs the methodology (silhouette
  and ARI ideas may be cited in `results_detailed.md`), but the headline analysis stays PCA +
  Mann-Whitney U.

* **Use sklearn's `FactorAnalysis` and apply varimax manually via numpy.linalg.svd**. Rejected: a
  hand-rolled varimax routine adds ~30 lines of code with non-trivial correctness risk (rotation
  convergence threshold, scaling of communalities). `factor_analyzer>=0.5.1` is a small pure-Python
  package (~2 MB) with the rotation built in. The single-line `pyproject.toml` addition is the
  lowest-risk path.

* **UMAP instead of PCA for the cluster visualisation**. Rejected: UMAP is excellent for preserving
  local neighbourhoods but distorts global distances and the morphology gallery / asymmetry-class
  question is fundamentally about global parameter regimes. PCA is variance-preserving and the
  loadings have a direct linear interpretation back onto the 54 electrophys parameters, which is
  essential for the "which dimensions separate the classes?" question.

* **Pool only t0102 and t0104 (as the task name suggests) instead of all four 68-d lineages**.
  Rejected: the researcher's commission and the task description explicitly extend to all four
  lineages because t0091 and t0099 add 46 unique cells to the primary cohort, pushing N from 40 to
  86 and substantially improving PCA / factor stability. The task name's "(t0102 + t0104, ...)"
  wording is a vestigial reference from the brainstorm session and is superseded by the full long
  description.

* **Re-run NSGA-II at the strict cohort to grow N for tighter factor analysis**. Rejected: this task
  is explicitly scoped as pure analysis on existing predictions. Re-running optimisation is out of
  scope per the task description's "Out of Scope" section.

### Task types

`task.json` lists `task_types: ["data-analysis", "comparative-analysis", "answer-question"]`, which
matches the work this task does:

* **data-analysis** Planning Guidelines: define questions upfront (done in REQ-12), list all metrics
  and charts upfront (done in REQ-13), name statistical tests (Mann-Whitney U for the cluster
  question, Pearson r for the factor-DSI / factor-PD relationships, percentile bootstrap for loading
  CIs). Save intermediate data (selected-cell tables, PCA components, factor scores) as JSON, not
  just final charts.

* **comparative-analysis** Planning Guidelines: comparison dimensions are symmetric-vs-asymmetric
  (PC1, PC2, source-task colouring) and primary-vs-strict cohort (variant-level comparison). Use the
  explicit multi-variant `metrics.json` format with `primary_cohort` and `strict_cohort` variants.
  Statistical significance test is Mann-Whitney U on PC1 / PC2 between classes within the primary
  cohort.

* **answer-question** Planning Guidelines: define the two questions upfront (REQ-12). One answer
  asset per question. Evidence sources are the predictions assets from t0091, t0099, t0102, t0104
  plus the new PCA / factor-analysis outputs. Stopping criterion: when the four predictions sources
  have been pooled, filtered, deduped, and analysed at both cohorts. If evidence is insufficient
  (e.g., primary cohort drops below 20 cells), the short answer must state the uncertainty rather
  than overclaim.

* * *

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Local compute (pooling, PCA, factor analysis, bootstrap, morphology builds for <=30 cells) | < 60 minutes of local CPU time |
| LLM API costs | **$0** (no external API calls in implementation) |
| Vast.ai compute | **$0** (no remote machines provisioned) |
| Paid services | **$0** (no datasets or libraries behind paywall) |
| Network egress | **$0** (no large downloads — `factor_analyzer` install is ~2 MB) |
| **Predicted total spend** | **$0.00** |
| **Hard cap** | **$0.00** (pure local analysis; if local resources fail the implementation must create an intervention file rather than spending money) |

This sits comfortably under the project's `per_task_default_limit` of $8.00 (`project/budget.json`)
and the project total budget of $50.00. The only conceivable cost exposure is if `factor_analyzer`
install fails locally and the implementation has to fall back to a paid alternative — this is
explicitly listed in Risks & Fallbacks below with an intervention-file escalation path, not a paid
workaround.

* * *

## Step by Step

### Milestone A: Project tooling and data pooling

1. **Preflight: confirm dependency tasks completed.** Run

   ```bash
   uv run python -u -m arf.scripts.aggregators.aggregate_tasks \
     --format json --detail short \
     --ids t0091_morphology_extended_nsga2_v1 \
           t0099_random_init_pareto_robustness \
           t0102_seedscale_n4_gen20 \
           t0104_nsga2_2obj_dsi_pdrate_3seeds
   ```

   Expected output: all four tasks have `status: "completed"`. Halt if any task is
   `permanently_failed` or still `in_progress` — t0105 cannot proceed without these inputs.
   Satisfies the preflight check that gates REQ-1.

2. **Add `factor_analyzer` to project dependencies.** Edit the top-level `pyproject.toml` to add
   `"factor_analyzer>=0.5.1",` to the `[project].dependencies` list, alphabetically near the other
   scientific Python deps. Then refresh the lockfile:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0105_cluster_factor_analysis_dsi_pd \
     -- uv lock
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0105_cluster_factor_analysis_dsi_pd \
     -- uv sync
   ```

   Smoke-test the install:

   ```bash
   uv run python -c "import factor_analyzer; print(factor_analyzer.__version__)"
   ```

   Expected output: a version string `>=0.5.1`. Satisfies **REQ-2**.

3. **Set up task scaffolding.** Create `code/paths.py` (centralised `pathlib.Path` constants for
   every input and output file path), `code/constants.py` (column names, dimension index map for the
   68-d vector, asymmetry-score weights, threshold constants `PRIMARY_DSI_THRESHOLD = 0.1`,
   `PRIMARY_PD_THRESHOLD = 2.0`, `STRICT_DSI_THRESHOLD = 0.2`, `STRICT_PD_THRESHOLD = 3.0`,
   `SILENCE_DSI_THRESHOLD = 0.95`, `SILENCE_PD_THRESHOLD = 5.0`, `ASYM_CLASS_THRESHOLD = 0.5`,
   `GALLERY_MAX_CELLS = 30`, `BOOTSTRAP_RESAMPLES = 200`, `KAISER_FACTOR_CAP = 10`,
   `CHART_DPI = 150`, deterministic `RANDOM_SEED = 105`), and `code/schemas.py` (dataclasses for the
   per-cell record and the analysis outputs). `code/__init__.py` must be empty (declares the
   package). No expected console output for this step. Satisfies the scaffolding required by REQ-1,
   REQ-4, REQ-6, REQ-8.

4. **Load and filter cells.** Implement `code/load_filter_cells.py` with a `main()` that:

   * reads `tasks/t0091_morphology_extended_nsga2_v1/results/data/all_evaluations.json` (single
     file), and the three / two / two seed-split files for t0099, t0102, t0104 from the paths
     defined in `code/paths.py`;
   * tags each row with `source_task` and `seed` (where applicable);
   * applies the silence-artifact filter `DSI > 0.95 AND PD < 5.0` to t0091/t0099/t0102 rows
     (skipping t0104 because the in-evaluator guard already applied) and counts exclusions per
     lineage;
   * applies the primary filter `DSI > 0.1 AND PD > 2.0` and writes the deduped table to
     `results/data/selected_cells_primary.json`;
   * applies the strict filter `DSI > 0.2 AND PD > 3.0` and writes the deduped table to
     `results/data/selected_cells_strict.json`;
   * dedupes by the 68-d vector rounded to 6 decimals (use a tuple-of-rounded-floats hash);
   * writes the per-lineage counts (`N_raw`, `N_passing_primary`, `N_unique_primary`,
     `N_passing_strict`, `N_unique_strict`, `silence_artifact_exclusions`) to
     `results/data/selection_counts.json`.

   Run:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0105_cluster_factor_analysis_dsi_pd \
     -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/load_filter_cells.py
   ```

   Expected output (stdout): the per-lineage and per-cohort counts printed as a table. Expect
   N_unique_primary in the 70-100 range (pre-scope estimate was 86) and N_unique_strict in the 20-40
   range (estimate 31). If N_unique_primary < 20, halt and create an intervention file recording the
   unexpectedly small cohort. Satisfies **REQ-1** and **REQ-3**.

### Milestone B: Asymmetry classification and morphology gallery

5. **Compute asymmetry score and class.** Implement `code/classify_asymmetry.py` that:

   * reads `results/data/selected_cells_primary.json`;
   * computes the normalised asymmetry score per cell using the four PD-asymmetry dims at positions
     54, 55, 56, 57 of the 68-d vector (per the morphology dim map in
     `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants_morphology.py`); names and normalising
     denominators are `soma_offset_pd_um` (150), `field_elongation_pd` (offset 1.0, /2.0),
     `branch_density_gradient_pd` (1.0), `primary_branch_pd_concentration` (5.0);
   * classifies cells at the `0.5` threshold (symmetric vs asymmetric);
   * also computes the 0.3 / 0.5 / 1.0 threshold sweep and writes class counts at each;
   * renders `results/images/asym_score_histogram.png` (DPI 150) with a vertical line at 0.5;
   * writes `results/data/asym_score_distribution.json` with `symmetric_count`, `asymmetric_count`,
     the histogram bin edges and counts, and the threshold sweep table.

   Run:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0105_cluster_factor_analysis_dsi_pd \
     -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/classify_asymmetry.py
   ```

   Expected output: class counts printed; histogram saved. If one class has zero cells at the 0.5
   threshold, halt and report the threshold sweep so the researcher can decide whether to continue
   with a different threshold (this is the unbalanced-class risk from Risks & Fallbacks). Satisfies
   **REQ-4**.

6. **Build the morphology gallery.** Adapt `scratch_t0102_t0104_morph_compare.py` on main into
   `code/build_gallery.py` with the following changes:

   * read `results/data/selected_cells_primary.json` and the asymmetry-class column joined from step
     5;
   * partition cells into 8 strata
     `(class in {symmetric, asymmetric}, source in {t0091, t0099, t0102, t0104})` and compute
     per-stratum quotas as `min(stratum_size, ceil(30 / nonempty_strata))`;
   * within each stratum, sort by `DSI * PD` descending and take the top quota cells (deterministic,
     no random seed);
   * for each selected cell, build the morphology via
     `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`
     with `params=MorphologyParams.from_dict(data=<14-d slice as dict>)` from
     `tasks.t0090_morphology_generator_diversity_test.code.morphology_params`; round the three
     integer morphology dims before constructing the dict;
   * iterate `result.soma + result.all_dends` and call NEURON's `h.x3d`, `h.y3d`, `h.diam3d` to
     extract pt3d coordinates; plot the top-down (x, y) projection per cell;
   * annotate each panel with DSI, PD, `asym_score`, and `source_task` as a small text block;
   * compose a multi-row grid sized to fit up to 30 panels (e.g., 5 cols x 6 rows) and save to
     `results/images/morphology_gallery.png` at DPI 150;
   * write the (class, source_task) quota table to `results/data/gallery_quota_table.json` for later
     embedding in the task results document.

   Run:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0105_cluster_factor_analysis_dsi_pd \
     -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/build_gallery.py
   ```

   Expected output: progress bar over 30 cells (~30 s on local CPU); gallery PNG saved. Verify by
   opening the PNG and confirming the asymmetric panels show visible soma offset and field
   elongation toward PD. Satisfies **REQ-5**.

### Milestone C: PCA cluster analysis

7. **PCA on the 54-d electrophys submatrix + Mann-Whitney U.** Implement `code/pca_electrophys.py`
   that:

   * reads `results/data/selected_cells_primary.json`, slices the first 54 columns of each cell's
     68-d vector as `X_electrophys` (shape `(N, 54)`);
   * z-scores each column with `(x - mean) / std` (clip std at `1e-12` to avoid divide-by-zero on
     any constant column);
   * fits `sklearn.decomposition.PCA(n_components=3)`;
   * computes a 4-panel matplotlib figure `results/images/pca_electrophys_panels.png` at DPI 150
     with panels: (a) PC1 vs PC2 coloured by asymmetry class (legend: blue=symmetric,
     red=asymmetric); (b) PC1 vs PC2 coloured by DSI (viridis colorbar); (c) PC1 vs PC2 coloured by
     PD (plasma colorbar); (d) PC1 vs PC2 coloured by `source_task` (categorical with a legend);
   * also renders `results/images/eigenvalue_scree.png` showing the scree plot of all 54 eigenvalues
     with a Kaiser-threshold line at 1.0;
   * runs `scipy.stats.mannwhitneyu(symmetric_pc1, asymmetric_pc1, alternative="two-sided")` and the
     same for PC2;
   * writes `results/data/pca_results.json` with `variance_explained` (length-3 list),
     `pc_loadings_top5` (mapping PC -> list of `(param_index, param_name, signed_loading)`),
     `pc_scores` (the `(N, 3)` matrix), and the class-labels column;
   * writes `results/data/pca_mannwhitney.json` with keys `pc1_u`, `pc1_p`, `pc2_u`, `pc2_p`,
     `n_symmetric`, `n_asymmetric`, and a short `interpretation` string keyed per PC ("PC1 separates
     classes at p={pc1_p:.3g}; cohort is/is not consistent with a single electrophys regime").

   Run:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0105_cluster_factor_analysis_dsi_pd \
     -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/pca_electrophys.py
   ```

   Expected output (stdout): variance-explained list (e.g., `[0.28, 0.17, 0.10]`), top-5 loadings
   printed per PC, and the Mann-Whitney U + p-value per PC. If PC1 variance < 0.10 (suggesting
   near-zero signal), halt and report — this signals a degenerate dataset. Satisfies **REQ-6** and
   **REQ-7**.

### Milestone D: Factor analysis

8. **Factor analysis on the full 68-d matrix.** Implement `code/factor_analysis.py` that:

   * reads `results/data/selected_cells_primary.json` and stacks the 68-d vectors into `X_full`
     shape `(N, 68)`;
   * z-scores each column;
   * computes the correlation matrix and counts eigenvalues > 1 (Kaiser criterion);
   * sets `n_factors = min(eigenvalues_above_1_count, 10)`;
   * fits `factor_analyzer.FactorAnalyzer(rotation="varimax", n_factors=n_factors)`;
   * extracts loadings as a `(68, n_factors)` matrix and computes factor scores via
     `analyser.transform(X_full_scaled)`;
   * writes `results/data/factor_loadings.json` with `n_factors`, `eigenvalues_above_1_count`,
     `eigenvalues` (full length-68 list for the scree), the `(68, n_factors)` loadings matrix, and
     the per-factor top-5 loadings list (factor -> `[(param_name, signed_loading)] * 5`);
   * writes `results/data/factor_scores.json` with the `(N, n_factors)` matrix (cell-major);
   * renders `results/images/factor_loadings.png` as a seaborn heatmap (factors on x, parameters on
     y, signed loadings as colour, divergent colormap centred at 0) at DPI 150.

   Run:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0105_cluster_factor_analysis_dsi_pd \
     -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/factor_analysis.py
   ```

   Expected output: `n_factors` printed (likely 5-9), per-factor top-5 loadings printed. If the
   factor solution fails to converge (factor_analyzer raises), halt and create an intervention file
   describing the convergence failure; the fallback is to sweep the `rotation` to `"varimax_kaiser"`
   or to fall back to unrotated factors. Satisfies **REQ-8**.

9. **Pearson r between factor scores and DSI / PD; flag joint factor.** Implement
   `code/factor_correlations.py` that:

   * reads `results/data/factor_scores.json` and the DSI / PD columns from
     `results/data/selected_cells_primary.json`;
   * runs `scipy.stats.pearsonr` between each factor score column and DSI, and between each factor
     score column and PD;
   * builds top-3 lists per outcome by `|r|`;
   * flags any factor where `|r_DSI| > 0.3 AND |r_PD| > 0.3` as a joint-DSI-PD factor;
   * writes `results/data/factor_correlations.json` with per-factor `r_dsi`, `p_dsi`, `r_pd`,
     `p_pd`, `top3_dsi` list, `top3_pd` list, and `joint_factors` list;
   * renders `results/images/factor_correlations.png` as a grouped bar chart at DPI 150 with two
     bars per factor (`|r|` vs DSI in one colour, `|r|` vs PD in another) and a horizontal reference
     line at `|r| = 0.3`.

   Run:

   ```bash
   uv run python -m arf.scripts.utils.run_with_logs \
     --task-id t0105_cluster_factor_analysis_dsi_pd \
     -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/factor_correlations.py
   ```

   Expected output (stdout): the per-factor `r_dsi`, `r_pd` table and the joint-factor list
   (possibly empty). Satisfies **REQ-9**.

10. **Bootstrap factor loadings.** Implement `code/factor_bootstrap.py` that:

    * reads `X_full` from `results/data/selected_cells_primary.json`;
    * runs 200 bootstrap resamples (resample N rows with replacement; refit
      `factor_analyzer.FactorAnalyzer(rotation="varimax", n_factors=n_factors)` per resample; record
      the loadings matrix per resample);
    * computes percentile 95% CIs per loading cell across resamples;
    * applies factor alignment (sign-flip and column permutation) per resample against the headline
      solution to guard against varimax's rotational ambiguity — use the simple heuristic of
      maximising row-wise dot product with the headline loadings, with sign determined by the larger
      absolute loading;
    * flags stable factors as those whose top-5 loadings retain consistent signs in at least 90% of
      resamples AND whose median absolute loading exceeds 0.4;
    * writes `results/data/factor_bootstrap.json` with `n_bootstrap_resamples`, the per-loading 95%
      CI matrix, and the `stable_factors` list;
    * renders `results/images/factor_loadings_bootstrap.png` overlaying CI error bars on the top-5
      loadings per factor at DPI 150.

    Run:

    ```bash
    uv run python -m arf.scripts.utils.run_with_logs \
      --task-id t0105_cluster_factor_analysis_dsi_pd \
      -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/factor_bootstrap.py
    ```

    Expected output (stdout): the stable-factor list printed, runtime in seconds (expect 1-5 minutes
    on local CPU for 200 resamples at N=86). If bootstrap runtime exceeds 30 minutes, halt and
    reduce resamples to 100; record the reduction in `results/data/factor_bootstrap.json` as a
    `reduced_to_100_reason` field. Satisfies **REQ-10**.

### Milestone E: Strict cohort and aggregation

11. **Repeat headline analyses on the strict cohort.** Implement `code/run_strict_cohort.py` that
    orchestrates steps 7, 8, 9 against `results/data/selected_cells_strict.json` and writes the
    parallel output files listed in REQ-11 (`pca_results_strict.json`,
    `factor_loadings_strict.json`, `factor_correlations_strict.json`, and the three `*_strict.png`
    charts). The strict-cohort code paths import the same analysis functions from steps 7, 8, 9
    (refactor them to take an input-path argument so they are re-usable). Run:

    ```bash
    uv run python -m arf.scripts.utils.run_with_logs \
      --task-id t0105_cluster_factor_analysis_dsi_pd \
      -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/run_strict_cohort.py
    ```

    Expected output: same set of stdout summaries as steps 7, 8, 9 but on the strict cohort. If
    strict-cohort N < 10, halt and skip the strict-cohort factor analysis (the PCA can still run);
    record the skip as a `strict_cohort_factor_analysis_skipped` flag in
    `results/data/factor_loadings_strict.json` with an explanatory reason string. Satisfies
    **REQ-11**.

### Milestone F: Answer assets and metrics aggregation

12. **Build the two answer assets.** Author the two assets at
    `tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/symmetric-vs-asymmetric-electrophys-cluster/`
    and
    `tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/dsi-pd-diversity-factor-decomposition/`,
    each with `details.json`, `short_answer.md`, and `full_answer.md` per
    `meta/asset_types/answer/specification.md`.

    * `details.json` fields: `spec_version: "2"`, `answer_id`, the question text verbatim,
      `short_answer_path: "short_answer.md"`, `full_answer_path: "full_answer.md"`,
      `answer_methods: ["existing_papers", "prior_project_findings", "code_experiments"]`,
      `categories`, `confidence`, `created_by_task: "t0105_cluster_factor_analysis_dsi_pd"`,
      `date_created`.
    * `short_answer.md`: 2-5 sentence direct answer, no inline citations, starting with "Yes", "No",
      or a concrete claim. Plus a `## Sources` section listing the four predictions task IDs and the
      headline chart filenames.
    * `full_answer.md`: mini-paper format. Sections: `## Short Answer` (mirrors the short answer
      doc), `## Research Process`, `## Evidence from Prior Project Tasks` (cite t0091, t0099, t0102,
      t0104), `## Evidence from Code or Experiments` (point at the PCA panels, the Mann-Whitney U
      output, the factor-loadings heatmap, and the bootstrap CIs as appropriate per asset),
      `## Synthesis`, `## Limitations` (N=86 at primary cohort, no per-trial reliability data,
      etc.), `## Sources` with markdown reference link definitions.

    Run the verificator:

    ```bash
    uv run python -m arf.scripts.utils.run_with_logs \
      --task-id t0105_cluster_factor_analysis_dsi_pd \
      -- uv run python -m arf.scripts.verificators.verify_answer_asset \
         tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/symmetric-vs-asymmetric-electrophys-cluster
    uv run python -m arf.scripts.utils.run_with_logs \
      --task-id t0105_cluster_factor_analysis_dsi_pd \
      -- uv run python -m arf.scripts.verificators.verify_answer_asset \
         tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/dsi-pd-diversity-factor-decomposition
    ```

    Expected output: 0 errors per asset. Satisfies **REQ-12**.

13. **Write `results/metrics.json` in the explicit multi-variant format.** Implement
    `code/build_metrics_json.py` that:

    * reads the primary and strict selected-cell tables;
    * computes the median DSI per cohort and writes it to the `direction_selectivity_index.value`;
    * sets `tuning_curve_hwhm_deg.value = null`, `tuning_curve_reliability.value = null`,
      `tuning_curve_rmse.value = null` for both variants, with `null_reason` strings explaining that
      these metrics are not stored in the pooled `all_evaluations*.json` data;
    * writes the file in the explicit multi-variant format per
      `arf/specifications/metrics_specification.md` (two variants: `primary_cohort`,
      `strict_cohort`).

    Run:

    ```bash
    uv run python -m arf.scripts.utils.run_with_logs \
      --task-id t0105_cluster_factor_analysis_dsi_pd \
      -- uv run python -u tasks/t0105_cluster_factor_analysis_dsi_pd/code/build_metrics_json.py
    ```

    Expected output: the JSON file written; `jq '.variants | keys' results/metrics.json` prints
    `["primary_cohort", "strict_cohort"]`. Satisfies **REQ-14**.

14. **Final implementation-stage verification.** Run the per-asset and metric verificators:

    ```bash
    uv run python -m arf.scripts.utils.run_with_logs \
      --task-id t0105_cluster_factor_analysis_dsi_pd \
      -- uv run python -m arf.scripts.verificators.verify_task_metrics \
         t0105_cluster_factor_analysis_dsi_pd
    ```

    Expected output: 0 errors. Confirm every required output file exists under
    `tasks/t0105_*/results/data/` and `tasks/t0105_*/results/images/`. Satisfies the
    requirement-coverage check spanning **REQ-1..REQ-14** and the immutability check for **REQ-15**.

The Step by Step ends here. Downstream orchestrator stages (results, compare-literature,
suggestions, reporting) are out of scope for this section and consume the JSON and PNG artifacts
produced above.

* * *

## Remote Machines

None required. This task is pure local analysis on existing per-cell evaluation files already on
disk in the predecessor task folders. No NEURON simulation, no NSGA-II re-run, no LLM API calls. The
morphology gallery does call NEURON's `h` object to extract pt3d coordinates for plotting, but the
call happens inside the local Python process and does not require a remote machine.

* * *

## Assets Needed

* `tasks/t0091_morphology_extended_nsga2_v1/results/data/all_evaluations.json` (input data)
* `tasks/t0099_random_init_pareto_robustness/results/data/all_evaluations_seed{11,22,33}.json`
  (input data)
* `tasks/t0102_seedscale_n4_gen20/results/data/all_evaluations_seed{44,55}.json` (input data)
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/all_evaluations_seed{44,55}.json` (input
  data)
* `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py` (imported via
  the `de_rosenroll_2026_dsgc` library for `generate_fixed_morphology`)
* `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` (imported for
  `MorphologyParams`)
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants_morphology.py` (referenced for the 14-d
  morphology dim index map; copied into `code/constants.py` rather than imported across tasks
  because it is not part of the registered library)
* `pyproject.toml` (modified to add `factor_analyzer>=0.5.1`)
* `uv.lock` (refreshed after the dependency add)

* * *

## Expected Assets

Two answer assets, matching `expected_assets: {"answer": 2}` in `task.json`:

1. **`assets/answer/symmetric-vs-asymmetric-electrophys-cluster/`** — answers "Do symmetric and
   asymmetric DSGC morphologies share the same electrophys parameter regime, or do they form
   distinct clusters in PC space?". Evidence: PCA panels chart, Mann-Whitney U on PC1 / PC2, top-5
   PC loadings, source-task colouring panel.

2. **`assets/answer/dsi-pd-diversity-factor-decomposition/`** — answers "Which factors
   (combinations of the 68 input parameters) explain DSI diversity versus PD diversity, and is there
   a joint factor or are the two outcomes orthogonal?". Evidence: factor-loadings heatmap,
   per-factor Pearson r vs DSI and PD, bootstrap 95% CIs, joint-factor flag.

No predictions, dataset, library, model, or paper assets are produced. The task only re-analyses
existing predictions.

* * *

## Time Estimation

* Local prep + data pooling + dedupe (steps 1-4): 15-30 minutes wall clock
* Asymmetry classification (step 5): 5-10 minutes
* Morphology gallery build (step 6): 30-60 minutes (limited by NEURON build of ~30 cells)
* PCA + Mann-Whitney U (step 7): 10-20 minutes
* Factor analysis + correlations (steps 8, 9): 15-30 minutes
* Bootstrap loadings (step 10): 5-30 minutes (200 resamples at N=86)
* Strict-cohort re-run (step 11): 15-30 minutes
* Answer-asset writing + metric aggregation (steps 12, 13, 14): 60-120 minutes
* **Total wall-clock**: 2.5-5 hours

This excludes orchestrator-managed downstream stages (results writing, compare-literature,
suggestions, reporting) which add their own time but are out of the Step by Step scope.

* * *

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Primary-cohort N < 20 after dedupe (much smaller than the ~86 estimate) | Low | Blocking | The primary filter is already the relaxed threshold. If N < 20, halt at step 4 and create an intervention file. Fallback: relax the filter further to `DSI > 0.05 AND PD > 1.0`, document the relaxation in `results_detailed.md`, and note the reduced statistical power. |
| `factor_analyzer` install fails (uv resolution issue, Windows wheel missing, version conflict) | Low | Blocking | Halt at step 2; create an intervention file. Fallback: implement a manual varimax rotation on top of `sklearn.decomposition.FactorAnalysis` (~30 lines via `numpy.linalg.svd`) and document the deviation in `results_detailed.md`. No paid alternative is used. |
| Class imbalance at threshold 0.5 (95% asymmetric, 5% symmetric or vice versa) | Medium | Reduces interpretability | Step 5 emits the 0.3 / 0.5 / 1.0 threshold sweep. If the 0.5 split is more extreme than 90/10, switch the headline threshold to whichever of 0.3 or 1.0 gives the closest-to-50/50 split and document the change. |
| PCA on 54 dims with N ~= 86 is unstable beyond PC1-PC2 | Medium | Limits interpretation | Restrict PC interpretation to PC1-PC2; report PC3 variance but do not draw conclusions from PC3 loadings. Also note in `results_detailed.md` that PC4+ are noise. |
| Factor analysis fails to converge on the 68-d matrix | Low | Blocking | Step 8 catches the exception, halts, and creates an intervention file. Fallback: drop varimax rotation (use unrotated factors) and document the limitation; alternative is to bin morphology dims to reduce to 64-d. |
| Bootstrap loadings reveal that no factor is stable (all factors fail the 90% sign-consistency check) | Medium | Limits factor-interpretation strength | Report the instability honestly in `results_detailed.md` and the second answer asset; the answer becomes "the 68-d parameter space does not support a stable low-d factor decomposition at N=86", which is a publishable null result. |
| t0091/t0099/t0102 silenced-cell artifacts escape the `DSI > 0.95 AND PD < 5` filter (some cells at DSI 0.94 are still artifacts) | Low | Pollutes the cohort | Inspect the cells nearest to the silence boundary (top-5 highest DSI in the cohort, sort by ascending PD, inspect spike counts in the source `all_evaluations*.json` where stored). If suspicious, tighten the filter to `DSI > 0.85 AND PD < 5` and document the change. |
| Strict-cohort N < 10 makes factor analysis numerically degenerate | Medium | Skips strict-cohort factor analysis | Step 11 detects this and skips the strict-cohort factor analysis (PCA still runs). The strict cohort remains a primary-cohort sanity check via PCA only; document the skip in `results_detailed.md`. |
| Morphology gallery PNG too large to render reliably on GitHub (>5 MB) | Low | Render glitches | Cap DPI at 150 and the figure size at 5 cols x 6 rows; if the PNG exceeds 5 MB, downscale to DPI 120 and re-render. |
| Implementation accidentally modifies a non-allowlisted top-level file | Low | Verifier failure | Run `git diff main -- tasks/` and `git diff main -- pyproject.toml uv.lock` periodically; never `git add .` — always stage specific files. |

* * *

## Verification Criteria

* **REQ-1 / REQ-3 coverage.** Run:

  ```bash
  jq '.silence_artifact_exclusions' \
    tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/selection_counts.json
  ```

  Expected output: a non-null object with per-lineage exclusion counts (t0091, t0099, t0102 keys
  present; t0104 key may be 0 or absent because the in-evaluator guard already applied).

* **REQ-2 coverage.** Run:

  ```bash
  uv run python -c "import factor_analyzer; print(factor_analyzer.__version__)"
  ```

  Expected output: a version string `>=0.5.1`. Also run `grep -n 'factor_analyzer' pyproject.toml`
  and expect one matching line in the dependencies block.

* **REQ-4 coverage.** Run:

  ```bash
  jq '.symmetric_count, .asymmetric_count' \
    tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/asym_score_distribution.json
  ```

  Expected output: two non-negative integers summing to the primary-cohort `N_unique`.

* **REQ-5 coverage.** Run:

  ```bash
  ls tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/morphology_gallery.png
  ```

  Expected output: the file exists. Verify panel count by opening the image (should match the quota
  table written to `results/data/gallery_quota_table.json`).

* **REQ-6 / REQ-7 coverage.** Run:

  ```bash
  jq '.variance_explained, .pc_loadings_top5 | keys' \
    tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/pca_results.json
  jq '.pc1_u, .pc1_p, .pc2_u, .pc2_p' \
    tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/pca_mannwhitney.json
  ```

  Expected output: a length-3 variance-explained list, top-5 loading keys for PC1/PC2/PC3, and
  numeric U statistics and p-values for both PC1 and PC2.

* **REQ-8 / REQ-9 / REQ-10 coverage.** Run:

  ```bash
  jq '.n_factors, .eigenvalues_above_1_count' \
    tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/factor_loadings.json
  jq '.top3_dsi, .top3_pd, .joint_factors' \
    tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/factor_correlations.json
  jq '.n_bootstrap_resamples, .stable_factors' \
    tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/factor_bootstrap.json
  ```

  Expected output: `n_factors` between 1 and 10; the top-3 lists are non-empty;
  `n_bootstrap_resamples` is 200 (or 100 with a documented reduction).

* **REQ-11 coverage.** Run:

  ```bash
  ls tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/*_strict.json \
     tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/*_strict.png
  ```

  Expected output: all six strict-cohort files listed (or with documented skips for the
  factor-analysis files if strict-cohort N < 10).

* **REQ-12 coverage.** Run:

  ```bash
  uv run python -m arf.scripts.verificators.verify_answer_asset \
    tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/symmetric-vs-asymmetric-electrophys-cluster
  uv run python -m arf.scripts.verificators.verify_answer_asset \
    tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/dsi-pd-diversity-factor-decomposition
  ```

  Expected output: 0 errors per asset.

* **REQ-13 coverage.** Run:

  ```bash
  ls tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/*.png | wc -l
  ```

  Expected output: at least 10. After the orchestrator results stage, every PNG must be referenced
  in `results_detailed.md` with `![desc](images/file.png)` syntax (verified by the results
  verificator).

* **REQ-14 coverage.** Run:

  ```bash
  jq '.variants | keys' \
    tasks/t0105_cluster_factor_analysis_dsi_pd/results/metrics.json
  ```

  Expected output: `["primary_cohort", "strict_cohort"]`. Then:

  ```bash
  uv run python -m arf.scripts.verificators.verify_task_metrics \
    t0105_cluster_factor_analysis_dsi_pd
  ```

  Expected output: 0 errors.

* **REQ-15 coverage (immutability).** Run:

  ```bash
  git diff main -- tasks/ | head -1
  git diff main -- pyproject.toml uv.lock
  ```

  Expected output: every changed file under `tasks/` lives under
  `tasks/t0105_cluster_factor_analysis_dsi_pd/`; the only top-level files touched are
  `pyproject.toml` and `uv.lock`.

* **Plan structure verification.** Run:

  ```bash
  uv run python -m arf.scripts.verificators.verify_plan \
    t0105_cluster_factor_analysis_dsi_pd
  ```

  Expected output: 0 errors.
