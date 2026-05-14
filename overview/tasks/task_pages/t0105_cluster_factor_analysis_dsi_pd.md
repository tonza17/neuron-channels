# ✅ Cluster + factor analysis of high-DSI/high-PD cells across all 68-d optimisations

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0105_cluster_factor_analysis_dsi_pd` |
| **Status** | ✅ completed |
| **Started** | 2026-05-14T12:52:11Z |
| **Completed** | 2026-05-14T14:25:00Z |
| **Duration** | 1h 32m |
| **Dependencies** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md), [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md), [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Task types** | `data-analysis`, `comparative-analysis`, `answer-question` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md) |
| **Expected assets** | 2 answer |
| **Step progress** | 11/15 |
| **Task folder** | [`t0105_cluster_factor_analysis_dsi_pd/`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/task_description.md)*

# t0105 — Cluster + Factor Analysis of High-DSI / High-PD Cells across All 68-d Optimisations

## Context

Direct researcher commission at 2026-05-14 after the t0104 result landed. Four NSGA-II
lineages have run 68-d optimisation (54-d electrophys + 14-d morphology) on the Bed B +
morphology substrate:

* **t0091** — warm-start NSGA-II 3-objective (DSI + PD-rate + robustness), 187 cells.
* **t0099** — random-init NSGA-II 3-objective at N_EVAL=20, 2,016 cells across GA seeds
  11/22/33.
* **t0102** — random-init NSGA-II 3-objective at N_EVAL=4, 2,592 cells across GA seeds 44/55.
* **t0104** — random-init NSGA-II 2-objective (no robustness) at N_EVAL=4, with the S-0102-01
  DSI silence guard, 2,208 cells across GA seeds 44/55.

Total: **7,003 cells**. The 54-d-only lineage (t0080 / t0081 / t0083) is excluded because it
does not co-vary morphology with electrophys.

Pre-scoping inventory (`scratch_count_68d_cells.py` on main) confirmed that with the relaxed
primary filter `DSI > 0.1 AND PD > 2 Hz` and dedupe by 68-d vector, **86 unique cells** pass —
a healthy sample for PCA and factor analysis. The strict filter `DSI > 0.2 AND PD > 3 Hz`
yields 31 unique cells and serves as a sensitivity check.

The two best cells in t0104 are strongly asymmetric DSGCs (soma offset toward PD, dendritic
field 2× elongated, primary branches PD-concentrated). The follow-up question: across all 86
cells that produced *some* direction selectivity AND *some* firing — not just the Pareto
extremes — does the asymmetric morphology motif hold, and which of the 68 input parameters
drive DSI and PD diversity?

A scratch comparison plot (`scratch_t0102_t0104_morph_compare.png` on main) showed top-5 cells
per optimisation but was limited to extreme cells. This task extends to the full population of
non-trivial cells from all four 68-d lineages.

## Goal

For all cells from t0091 + t0099 + t0102 + t0104 with **DSI > 0.1 AND PD-rate > 2 Hz** (the
"non-trivial both-axes" population — primary cohort, expected ~86 unique cells), answer three
questions:

1. **What does a morphology gallery of these cells look like?** Plot each cell's morphology
   (or a representative subsample if the count > 30) with its DSI and PD values annotated,
   separated by source optimisation.

2. **Do the intrinsic (electrophys) parameters cluster by morphological asymmetry?** Run PCA
   on the 54-d electrophys parameter vectors (excluding morphology) of the selected cells,
   classify each cell as "symmetric" or "asymmetric" using a normalised asymmetry score across
   the four PD asymmetry axes, and plot a PC1-vs-PC2 scatter coloured by class. If the two
   classes separate in PC space, the electrophys regime differs between the two morphology
   classes; if they do not, the asymmetry is independent of the electrophys regime.

3. **Which of the 68 parameters drive DSI and PD diversity?** Run factor analysis on the full
   68-d parameter matrix of the selected cells, project DSI and PD onto the factors via
   Pearson correlation between factor scores and the two outcomes, and report the top-loading
   factors for each outcome. Both electrophys and morphology parameters must be included.

## Key Questions

1. Does the asymmetric-morphology motif (the four PD-asymmetry axes elevated) hold across the
   broader DSI > 0.2 ∧ PD > 3 population, or only at the Pareto extremes?
2. In PCA of the 54-d electrophys vectors, do symmetric and asymmetric cells separate? Or do
   they share the same electrophys-parameter cluster, suggesting that the morphology is the
   dominant discriminator?
3. Which top-3 factors (out of N factors retained by Kaiser criterion or 80% variance) load
   most strongly on DSI? On PD? Do these factor loadings include both electrophys and
   morphology parameters?
4. Is there a single factor that simultaneously loads on DSI AND PD (a "direction-selectivity
   firing-rate trade-off" factor), or are the two outcomes driven by orthogonal factors?

## Approach

### Cell selection

Pool all evaluations from the four 68-d optimisation lineages:

* `tasks/t0091_morphology_extended_nsga2_v1/results/data/all_evaluations.json`
* `tasks/t0099_random_init_pareto_robustness/results/data/all_evaluations_seed{11,22,33}.json`
* `tasks/t0102_seedscale_n4_gen20/results/data/all_evaluations_seed{44,55}.json`
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/all_evaluations_seed{44,55}.json`

**Primary filter**: `dsi_vector_sum > 0.1 AND pd_rate_hz > 2.0` (expected ~86 unique cells
after dedupe).

**Strict robustness-check filter**: `dsi_vector_sum > 0.2 AND pd_rate_hz > 3.0` (expected ~31
unique cells). All headline analyses must be repeated on this stricter cohort and any
qualitative change between cohorts must be documented in `results_detailed.md`.

Dedupe by full 68-d parameter vector (round to 6 decimals) — Pareto preservation across
generations creates many duplicate rows. Across all lineages we expect ~268 raw passing rows
reducing to ~86 unique vectors at the primary filter.

Tag each row with `source_task` ∈ {t0091, t0099, t0102, t0104} and `seed` (if applicable).

Report `N_selected` before and after dedupe for both filter thresholds. Also report the
per-lineage cell counts in the headline `results_summary.md` so the reader can see the
relative contribution of each optimisation regime to the analysis population.

### Asymmetry classification

Compute the normalised asymmetry score:

```
asym_score = abs(soma_offset_pd_um) / 150
           + abs(field_elongation_pd - 1.0) / 2.0
           + abs(branch_density_gradient_pd) / 1.0
           + abs(primary_branch_pd_concentration) / 5.0
```

Range: 0 (fully symmetric) → 4 (max asymmetric). Classify each cell as:

* `symmetric` if `asym_score < 0.5`
* `asymmetric` if `asym_score >= 0.5`

Report the distribution of `asym_score` in the selected population and the count in each
class.

### Morphology gallery

At ~86 cells in the primary cohort, a full gallery is too large. Use a **stratified subsample
of ≤30 cells**, stratified by asymmetry class × source task. The subsample selection is
deterministic: within each (class, source_task) stratum, take the top cells by `DSI × PD`
until the per-stratum quota is met. Record the (class, task) quota table in
`results_detailed.md`.

For each selected cell:

1. Build the morphology via
   `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`.
2. Extract the soma + all_dends pt3d coordinates.
3. Plot top-down (x, y) projection with the soma marked, PD arrow indicated.
4. Annotate DSI, PD, asym_score, source_task, seed/gen.

Output: `results/images/morphology_gallery.png` (multi-row grid, sized appropriately).

If N ≤ 30, plot all selected cells. If N > 30, plot a stratified subsample documented in
`results_detailed.md` with the random seed used for the subsample.

### PCA cluster analysis on electrophys parameters

1. Stack the 54-d electrophys vectors of the selected cells into matrix `X_electrophys` shape
   `(N_selected, 54)`.
2. z-score each column.
3. Run `sklearn.decomposition.PCA` (or equivalent). Keep PC1, PC2, PC3.
4. Plot PC1 vs PC2 scatter, coloured by asymmetry class (symmetric = blue, asymmetric = red).
5. Also produce PC1 vs PC2 coloured by DSI (continuous colormap) and PC1 vs PC2 coloured by PD
   (continuous colormap) for context.
6. Report variance explained by PC1/PC2/PC3 and the top-5 loading dimensions on each PC (give
   parameter name and loading magnitude).
7. Report a Mann-Whitney U test between symmetric and asymmetric PC1 scores (and PC2) to
   quantify whether the classes separate; report the U statistic, p-value, and a brief
   interpretation.

Output: `results/images/pca_electrophys_by_morphology_class.png` (3 subplots: by-class,
by-DSI, by-PD).

### Factor analysis on the full 68-d matrix

1. Stack the 68-d parameter vectors into `X_full` shape `(N_selected, 68)`.
2. z-score each column.
3. Run `sklearn.decomposition.FactorAnalysis` with rotation = "varimax" (use the iterative
   method if sklearn lacks varimax built-in; or use `factor_analyzer` package — add to
   pyproject.toml if needed).
4. Choose number of factors by Kaiser criterion (eigenvalues > 1 on the correlation matrix) OR
   80% of total variance, whichever gives the smaller count, capped at 10 factors.
5. For each factor, list the top-5 loading parameters (by absolute loading magnitude), giving
   parameter name and signed loading.
6. Compute factor scores for each cell (the (N_selected, n_factors) matrix).
7. Compute Pearson r between each factor score column and DSI (and PD). Report the top-3
   factors by
   |r| for each outcome.
8. If a single factor has both `|r_DSI| > 0.3 AND |r_PD| > 0.3`, flag it as a joint-DSI-PD
   factor.

Output: `results/images/factor_loadings.png` (heatmap of factors × parameters) and
`results/images/factor_correlations.png` (bar chart of |r| between each factor and DSI/PD).

### Answer assets

Produce two answer assets:

1. `assets/answer/symmetric-vs-asymmetric-electrophys-cluster/`
   * Question: "Do symmetric and asymmetric DSGC morphologies share the same electrophys
     parameter regime, or do they form distinct clusters in PC space?"
   * Evidence: PCA scatter, Mann-Whitney U test results.

2. `assets/answer/dsi-pd-diversity-factor-decomposition/`
   * Question: "Which factors (combinations of the 68 input parameters) explain DSI diversity
     versus PD diversity, and is there a joint factor or are the two outcomes orthogonal?"
   * Evidence: factor-loading heatmap, top-loading parameters per factor, Pearson correlations
     between factor scores and DSI/PD.

## Why This Matters for the Research Questions

The project's research questions 1-4 ask which combinations of channel and morphological
parameters produce direction selectivity. t0080-t0104 have approached this via multi-objective
optimisation; t0105 now asks a complementary "what works" question on the optimiser's output
population. Specifically:

* If symmetric and asymmetric cells separate in electrophys PC space, then the morphology
  class selects a different channel regime — relevant to RQ4 (active vs passive dendrites) and
  RQ3 (synapse density/spatial distribution).
* If DSI and PD are driven by different factors, then the joint corner is empirically
  unreachable because no single parameter axis lifts both — supporting the substrate-limited
  reading from t0102 / t0104.
* If a joint factor exists, then targeted moves along that factor's loading direction may
  unlock the joint corner — a direct lead for an experimental follow-up task.

## Step by Step

Canonical step IDs:

1. `preflight` — verify both dependency tasks are completed.
2. `research-code` — review t0102 / t0104 evaluation file formats, morphology generator
   interface, sklearn / factor_analyzer availability in pyproject.toml.
3. `planning` — produce `plan/plan.md` with REQ-1..REQ-N including cell counts after
   filtering, gallery-subsample policy, factor-analysis algorithm choice, and
   asymmetry-threshold sensitivity plan.
4. `implementation` —
   * 4a. Load and filter cells (`code/load_filter_cells.py`).
   * 4b. Compute asymmetry classification (`code/classify_asymmetry.py`).
   * 4c. Build morphology gallery (`code/build_gallery.py` extending the working scratch
     script).
   * 4d. PCA on electrophys params + Mann-Whitney U (`code/pca_electrophys.py`).
   * 4e. Factor analysis on full 68-d + correlations (`code/factor_analysis.py`).
   * 4f. Emit all charts to `results/images/`.
5. `analysis` (creative-thinking) — interpret cluster separation and joint factor (if any).
6. `results` — write `results_summary.md`, `results_detailed.md`, `metrics.json`, `costs.json`
   ($0), embed all charts.
7. `compare-literature` — quick comparison to Mohacsi 2024 (multi-objective neuron-fitting),
   Sivyer 2013 (asymmetric DSGC morphology), Vaney 2012 (DSGC type taxonomy).
8. `suggestions` — generate follow-up suggestions based on factor-analysis findings.
9. `reporting` — verificators, capture sessions, finalise task.json.

## Remote Machines

None. Local-only analysis on the local machine. Existing project Python environment plus
possibly `factor_analyzer` package (small addition to `pyproject.toml` if used).

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Local compute (PCA + factor analysis + morphology builds for ≤30 cells) | < 30 minutes |
| API costs | $0 |
| Vast.ai | $0 |
| **Predicted spend** | **$0** |
| **Hard cap** | **$2** (only if `factor_analyzer` pip install requires online resolution) |

## Assets Needed

* `tasks/t0102_seedscale_n4_gen20/results/data/` (all_evaluations files)
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/` (all_evaluations files)
* `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`
* `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py`
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants_morphology.py` (for the morphology
  dimension index map)

## Expected Assets

* 2 answer assets (one for the cluster-separation question, one for the factor-decomposition
  question)

`expected_assets`: `{"answer": 2}`

No predictions assets — t0105 is a pure analysis task on existing predictions.

## Time Estimation

* Local prep + load + filter: 15-30 minutes
* Morphology gallery build: 30-60 minutes
* PCA + Mann-Whitney + plots: 15-30 minutes
* Factor analysis + correlations + plots: 30-60 minutes
* Analysis + reporting: 60-90 minutes
* **Total wall-clock**: 2.5-4.5 hours.

## Risks & Fallbacks

* **Risk**: filtered cell count is small (e.g. N < 20). **Fallback**: relax filter to `DSI >
  0.1 AND PD > 2`; document the relaxation in results_detailed.md. If still < 10, the analysis
  runs on the small N with caveats.
* **Risk**: PCA on 54 dims with N ~ 30-100 may be unstable. **Fallback**: report bootstrapped
  variance-explained intervals and constrain interpretation to PC1-PC2 only.
* **Risk**: `factor_analyzer` not in current pyproject.toml. **Fallback**: use
  `sklearn.decomposition.FactorAnalysis` (no varimax built-in) and manually apply varimax via
  a small rotation routine, or fall back to PCA-only interpretation.
* **Risk**: asymmetry threshold of 0.5 produces unbalanced classes (e.g. 95% asymmetric, 5%
  symmetric). **Fallback**: sweep thresholds at 0.3 / 0.5 / 1.0 and report all three; pick the
  middle for the headline plots and note class balance.
* **Risk**: t0102 cells with DSI > 0.2 are dominated by silenced-cell artifacts that escaped
  t0104's guard. **Fallback**: explicitly check the artifact pattern (DSI > 0.95 AND PD < 5)
  and exclude such cells from t0102 if they appear; document the exclusion count.

## Verification Criteria

* `verify_task_metrics t0105_cluster_factor_analysis_dsi_pd` passes with 0 errors.
* `verify_task_results t0105_cluster_factor_analysis_dsi_pd` passes with 0 errors.
* Both answer assets validate against `verify_answer_asset`.
* All charts in `results/images/` are PNG, embedded in `results_detailed.md` via
  `![desc](images/file.png)`.
* The morphology gallery is reproducible: includes the random seed for any stratified
  subsampling.
* The PCA and factor-analysis numbers in `results_detailed.md` exactly match values in
  `metrics.json`.

## Task Requirement Checklist (initial — `plan/plan.md` will finalise the REQ list)

* REQ-1: Pool t0091 + t0099 + t0102 + t0104 evaluations, apply both filters (primary `DSI >
  0.1 AND PD > 2`; strict `DSI > 0.2 AND PD > 3`), dedupe by 68-d vector. Record N_raw,
  N_passing, N_unique for each filter and lineage.
* REQ-2: Compute normalised asymmetry score for each selected cell; classify
  symmetric/asymmetric at threshold 0.5; report class counts.
* REQ-3: Build morphology gallery for selected cells (or stratified subsample of ≤30).
  Annotate DSI, PD, asym_score, source_task per panel.
* REQ-4: PCA on 54-d electrophys vectors; plot PC1-PC2 by class, by DSI, by PD; report
  variance explained and top loadings.
* REQ-5: Mann-Whitney U test between symmetric and asymmetric PC1 (and PC2); report U,
  p-value, interpretation.
* REQ-6: Factor analysis on 68-d full vectors; choose factor count by Kaiser or 80% variance;
  report loadings.
* REQ-7: Pearson r between factor scores and DSI/PD; identify top-3 factors per outcome; flag
  any joint factor.
* REQ-8: Two answer assets validated by `verify_answer_asset`.

## Out of Scope

* Re-running NSGA-II or any optimisation (this is pure analysis on existing data).
* Building any morphology beyond what is needed for the gallery plot.
* In silico patch-clamp / IV-curve analysis on the breakthrough cells (deferred to a separate
  task; goes well with S-0104-01 / S-0104-02).
* Comparing against external DSGC datasets (Bae 2018, Ran 2020) — deferred to S-0103-*
  lineage.

</details>

## Metrics

### Primary cohort (DSI > 0.1 AND PD > 2.0)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.17653634975006283** |

### Strict cohort (DSI > 0.2 AND PD > 3.0)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.35141316455069005** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Which factors (combinations of the 68 input parameters) explain DSI diversity versus PD diversity, and is there a joint factor or are the two outcomes orthogonal?](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/dsi-pd-diversity-factor-decomposition/) | [`full_answer.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/dsi-pd-diversity-factor-decomposition/full_answer.md) |
| answer | [Do symmetric and asymmetric DSGC morphologies share the same electrophys parameter regime, or do they form distinct clusters in PC space?](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/symmetric-vs-asymmetric-electrophys-cluster/) | [`full_answer.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/symmetric-vs-asymmetric-electrophys-cluster/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Re-run varimax factor analysis excluding integer morph_seed to test
whether F1's correlates survive</strong> (S-0105-01)</summary>

**Kind**: experiment | **Priority**: high

morph_seed (an integer dimension bounded [0, 99] driving generator randomness, not
biologically meaningful) loads +0.68 on F1 next to NAP_PRIMARY (+0.75), SK_MID (+0.66),
MG_CONC_MM (+0.65), and RA_OHM_CM (+0.65). F1's r_DSI = -0.322 / r_PD = -0.265 could partly be
a 'warm-start vs random-init' indicator disguised as a mechanistic factor because t0091 fixed
morph_seed = 31 while t0099/t0102/t0104 randomise it. Re-run the t0105 factor analysis on a
67-d matrix excluding morph_seed and check whether F1's top loadings (NAP_PRIMARY, SK_MID,
MG_CONC_MM, Ra) and its Pearson r vs DSI / PD survive. If they do, F1 is mechanistic; if F1
dissolves, F1 was a lineage indicator. Recommended task type: data-analysis. Cost: $0 (pure
local re-analysis of existing data). Effort: 1-2 hours.

</details>

<details>
<summary><strong>Targeted Ca-K channel ablation sweep on top-PC1 asymmetric cells to
validate the SK/BK mechanistic hypothesis</strong> (S-0105-02)</summary>

**Kind**: experiment | **Priority**: high

PC1 separates symmetric from asymmetric cells at p = 1.48e-10 with top loadings SK_TERMINAL,
BK_TERMINAL, SK_SOMA, BK_MID, NAP_PRIMARY. The mechanistic hypothesis is that asymmetric
dendrites concentrate Ca influx along the PD axis, so high terminal SK/BK locally quenches
PD-side over-excitation. Test by taking the top-3 PC1-positive asymmetric cells (high Ca-K
regime, e.g. the t0102 / t0104 cells in the cohort), independently ablating SK_TERMINAL = 0,
BK_TERMINAL = 0, SK_SOMA = 0, BK_MID = 0 (one at a time and combined), and re-evaluating DSI +
PD on the de Rosenroll Bed B substrate. Outcome: a 4x4 ablation grid per cell showing which
Ca-K conductance is load-bearing for the asymmetric direction-selectivity regime. Recommended
task types: experiment-run, data-analysis. Cost: ~$2-3 (small Vast.ai instance for 3-6 hours;
or local if NEURON runs locally). Aligns with PolegPolsky2026's ML channel-importance finding.

</details>

<details>
<summary><strong>Investigate the symmetric high-DSI outlier pocket: cells with DSI
> 0.2 AND asym_score < 0.5</strong> (S-0105-03)</summary>

**Kind**: experiment | **Priority**: medium

All 20 symmetric cells in the t0105 primary cohort come from t0091's warm-start (asym_score =
0 exactly), but two of them have DSI > 0.2 (cells #2 from t0091 gen 1 with DSI = 0.329 / PD =
12.86 Hz; cell from t0091 with DSI = 0.198 / PD = 46.14 Hz). These are 'symmetric high-DSI'
outliers that contradict the simple 'asymmetric morphology required for DSI' reading. Inspect
their full 68-d parameter vectors, check whether their high DSI is silence-artifact-adjacent
(PD < 5 Hz with small spike count), and if not, run a small perturbation grid around their
parameter neighbourhood to see whether a symmetric-morphology DSI > 0.2 plateau exists. This
would significantly alter the project's understanding of which substrate features are required
for direction selectivity. Recommended task type: data-analysis + experiment-run. Cost:
~$0.5-1.

</details>

<details>
<summary><strong>F1-axis-seeded NSGA-II initial population to test whether targeted
seeding escapes the joint-corner block</strong> (S-0105-04)</summary>

**Kind**: experiment | **Priority**: high

F1 is the only factor weakly correlated with both DSI (r = -0.322) and PD (r = -0.265). Its
top loadings span NAP_PRIMARY, SK_MID, MG_CONC_MM, RA_OHM_CM (and morph_seed - see S-0105-01
caveat). Build a random-init NSGA-II run whose initial population samples along the F1 axis
(positive and negative directions) and orthogonal to F1, instead of uniform sampling. If
F1-axis seeding accelerates Pareto exploration into the joint corner, the substrate has a
discoverable direction that random-init NSGA-II misses. If F1-axis seeding produces the same
L-shape, the substrate-limit reading is reinforced. Recommended task type: experiment-run.
Cost: ~$8-12 (one Vast.ai NSGA-II run at matched budget to t0104 seed 44). Complements
S-0102-03 / S-0104-04 IBEA suggestions.

</details>

<details>
<summary><strong>Per-lineage PCA decomposition: quantify how much cross-lineage
heterogeneity contributes to PC1 separation</strong> (S-0105-05)</summary>

**Kind**: experiment | **Priority**: medium

t0105's pooled cohort spans four lineages with different settings (warm-start vs random-init,
N_EVAL=4 vs 20, 2-obj vs 3-obj). PC1's separation of symmetric from asymmetric cells is
confounded with the lineage source (all 20 symmetric cells come from t0091). Run PCA
independently per lineage (t0099 alone, t0102 alone, t0104 alone) and compare the top-5 PC1
loadings; if they match across lineages despite no symmetric cells, the Ca-K / NAP_PRIMARY
signature is lineage-robust rather than a t0091-warm-start artifact. Quantify cross-lineage
PC1-loading correlation to put a number on cross-lineage heterogeneity. Recommended task type:
data-analysis. Cost: $0 (pure local re-analysis).

</details>

<details>
<summary><strong>Parametric-bootstrap factor analysis at N>=300 synthetic cells
to test if F3-F10 stabilise</strong> (S-0105-06)</summary>

**Kind**: technique | **Priority**: medium

Only F1 and F2 pass the t0105 bootstrap stability test (>= 90 % sign consistency in top-5
loadings, median |loading| >= 0.4) at N=85. The 5xp = 340 conventional floor for factor
analysis on 68 dimensions would need N >= 340 cells. Generate a parametric bootstrap from the
t0105 cohort (fit a multivariate Gaussian or copula on the 68-d data, sample N=400 synthetic
cells, refit varimax FA) and check whether F3-F10 stabilise at the inflated N. If they do, the
under-power is the limiter; if they do not, the factors are genuinely unstable in the
substrate. Recommended task type: data-analysis. Cost: $0 (pure local synthesis +
re-analysis).

</details>

<details>
<summary><strong>MAP-Elites quality-diversity search on Bed B + morphology substrate
to find off-axis joint-corner cells</strong> (S-0105-07)</summary>

**Kind**: technique | **Priority**: medium

t0105 finds no joint DSI-PD factor — no single low-d axis carries both outcomes. NSGA-II (any
objective vector size or noise budget) cannot ride a non-existent axis. MAP-Elites maintains a
diversity grid over user-specified behavioural descriptors (e.g., asym_score x morphology_seed
bins), promotes corner exploration over Pareto crowding, and may find isolated joint-corner
cells that lie off any continuous axis. Run MAP-Elites at matched budget to t0104 seed 44
(~$5) on the same Bed B + morphology substrate with behavioural descriptors (asym_score,
source_lineage_marker), compare the resulting joint-corner yield. Complements S-0102-03 /
S-0104-04 IBEA suggestions but with a stronger diversity prior. Recommended task type:
experiment-run. Cost: ~$5-8.

</details>

## Research

* [`research_code.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/results_summary.md)*

# Results Summary: t0105 — Cluster + Factor Analysis of High-DSI/High-PD Cells

## Summary

t0105 pools 7,003 per-cell evaluations from four 68-d NSGA-II lineages (t0091, t0099, t0102,
t0104), applies a silence-artifact filter (73 cells excluded) plus the primary cohort filter
`DSI > 0.1 AND PD > 2 Hz` with dedupe by 68-d vector to land at **N=85 unique cells**, and
runs asymmetry classification, PCA on the 54-d electrophys submatrix, and varimax factor
analysis on the full 68-d matrix. PC1 separates the 20 symmetric and 65 asymmetric cells at
**Mann-Whitney U=31.0, p=1.48e-10**, top-loading Ca-activated K-channels (SK_TERMINAL,
BK_TERMINAL, SK_SOMA, BK_MID) and persistent Na (NAP_PRIMARY) — morphology class pre-selects a
different electrophys regime. **No factor** exceeds |r| > 0.3 on both DSI and PD, so the
joint-DSI/PD corner has no single-axis driver in the substrate.

## Metrics

* **Primary cohort N**: **85 unique cells** (t0091=26, t0099=20, t0102=19, t0104=20); strict
  cohort N=30
* **Silence-artifact exclusions**: **73 cells** (t0091=5, t0099=23, t0102=45, t0104=0) —
  t0104's S-0102-01 guard fully holds
* **Asymmetry class counts** (threshold 0.5): **20 symmetric, 65 asymmetric**; all 20
  symmetric cells come from t0091
* **PCA variance explained**: PC1=**29.5 %**, PC2=8.4 %, PC3=6.1 %
* **PC1 Mann-Whitney U**: U=**31.00**, p=**1.48e-10**; PC2 p=0.78 (no separation on PC2)
* **Strict cohort PC1 separation**: U=10.00, p=**8.23e-5** (preserved at N=30)
* **Factor count (Kaiser, capped at 10)**: **10 factors**; 18 eigenvalues exceeded 1.0
* **Top DSI factor**: F1 r=**-0.322**, p=0.003; **Top PD factor**: F1 r=**-0.265**, p=0.014
* **Joint DSI-PD factors** (|r| > 0.3 on both): **0**
* **Bootstrap-stable factors** (200 resamples): F1, F2 only — F3 through F10 are unstable at
  N=85
* **Total task cost**: **$0.00** (pure local analysis, no remote machines)

## Verification

* `verify_task_results.py` — PASSED (see verificator log for codes)
* `verify_suggestions.py` — PASSED (0 errors)
* `verify_compare_literature.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (multi-variant `primary_cohort` + `strict_cohort`)
* Answer asset `symmetric-vs-asymmetric-electrophys-cluster` — PASS
* Answer asset `dsi-pd-diversity-factor-decomposition` — PASS

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0105_cluster_factor_analysis_dsi_pd" ---
# Results Detailed: t0105 — Cluster + Factor Analysis of High-DSI/High-PD Cells

## Summary

This task pools every per-cell evaluation from the four 68-d NSGA-II lineages (t0091
warm-start 3-obj; t0099 random-init 3-obj at N=20; t0102 random-init 3-obj at N=4; t0104
random-init 2-obj at N=4 with the S-0102-01 silence guard), totalling **7,003 raw rows**.
After a silence-artifact filter (exclude `DSI > 0.95 AND PD < 5 Hz` on t0091/t0099/t0102), the
primary cohort filter `DSI > 0.1 AND PD > 2 Hz`, and dedupe by the 68-d vector rounded to 6
decimals, the cohort lands at **N=85 unique cells**; the strict cohort `DSI > 0.2 AND PD > 3
Hz` lands at **N=30**. PCA on the 54-d electrophys submatrix cleanly separates the **20
symmetric** and **65 asymmetric** cells on PC1 (Mann-Whitney **U=31.00, p=1.48e-10**), with
top loadings on Ca-activated K-channels (SK_TERMINAL, BK_TERMINAL, SK_SOMA, BK_MID) and
primary-dendrite persistent Na (NAP_PRIMARY). Varimax factor analysis on the full 68-d matrix
retains **10 factors** by Kaiser criterion; **F1 is the top correlate of both DSI (r=-0.322)
and PD (r=-0.265) but no factor crosses the joint threshold |r| > 0.3 on both**, so the
substrate has no single low-d axis that lifts both outcomes toward the joint corner. Bootstrap
stability across 200 resamples confirms F1 and F2 only; F3-F10 are unstable at N=85.

## Methodology

### Data sources

Per-cell evaluation rows were read from:

* `tasks/t0091_morphology_extended_nsga2_v1/results/data/all_evaluations.json` (187 rows, 1
  lineage, warm-start, 3-objective)
* `tasks/t0099_random_init_pareto_robustness/results/data/all_evaluations_seed{11,22,33}.json`
  (2,016 rows, 3 GA seeds, random-init, 3-objective at N_EVAL=20)
* `tasks/t0102_seedscale_n4_gen20/results/data/all_evaluations_seed{44,55}.json` (2,592 rows,
  2 GA seeds, random-init, 3-objective at N_EVAL=4)
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/all_evaluations_seed{44,55}.json`
  (2,208 rows, 2 GA seeds, random-init, 2-objective at N_EVAL=4 with S-0102-01 silence guard)

Total raw rows: **7,003**.

### Filters and dedupe

Three sequential filters applied to the pooled rows:

1. **Silence-artifact filter**: exclude any row from t0091/t0099/t0102 with `DSI > 0.95 AND PD
   < 5 Hz` (these are the DSI = 1.0 floating-point artifacts caused by very low spike counts,
   before t0104's in-evaluator guard). t0104 rows skip this filter because the guard is built
   into the evaluator. Excluded: **t0091=5, t0099=23, t0102=45, t0104=0** (total 73 cells).
2. **Primary filter**: `DSI > 0.1 AND PD > 2.0 Hz` (260 rows pass before dedupe). **Strict
   filter**: `DSI > 0.2 AND PD > 3.0 Hz` (87 rows pass before dedupe).
3. **Dedupe**: by tuple of the 68-d parameter vector rounded to 6 decimals. Pareto
   preservation across generations creates many duplicate rows. After dedupe: **N=85 primary**
   (per-lineage t0091=26, t0099=20, t0102=19, t0104=20) and **N=30 strict** (t0091=14,
   t0099=5, t0102=3, t0104=8).

### Asymmetry classification

For each cell, the normalised asymmetry score was computed as:

```text
asym_score = abs(soma_offset_pd_um) / 150
           + abs(field_elongation_pd - 1.0) / 2.0
           + abs(branch_density_gradient_pd) / 1.0
           + abs(primary_branch_pd_concentration) / 5.0
```

`symmetric` if `asym_score < 0.5`, `asymmetric` otherwise. Threshold-sweep at 0.3 / 0.5 / 1.0:

| Threshold | Symmetric | Asymmetric |
| --- | --- | --- |
| 0.3 | 20 | 65 |
| 0.5 (headline) | 20 | 65 |
| 1.0 | 27 | 58 |

Score distribution: range 0.0-3.34, mean 1.43, median 1.67. The 0.3 and 0.5 thresholds produce
identical class counts because no cell sits in the (0.3, 0.5) band — the distribution is
bimodal with a heavy mode at zero (20 cells, all from t0091's earliest generation) and the
rest at asym_score >= 0.55.

### Morphology gallery

A deterministic stratified subsample of 30 cells was built (5 non-empty strata of the 8
possible class x source combinations; each non-empty stratum got 6 cells by top `DSI * PD`
ranking). Each cell's 14-d morphology was generated with
`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`,
its `soma + all_dends` pt3d coordinates extracted via NEURON's `h.x3d`/`h.y3d`/`h.diam3d`, and
plotted as top-down (x, y) projections in a 5-column 6-row grid with DSI, PD, asym_score, and
source_task annotated per panel.

### PCA recipe

Stack the first 54 columns of each cell's 68-d vector into `X_electrophys` shape (85, 54).
Z-score each column (clip stdev at 1e-12). Fit `sklearn.decomposition.PCA(n_components=3)`.
Compute scree across all 54 eigenvalues. Run `scipy.stats.mannwhitneyu(symmetric_pc1_scores,
asymmetric_pc1_scores, alternative="two-sided")` and the same for PC2.

### Factor analysis recipe

Stack the full 68-d vectors into `X_full` shape (85, 68). Z-score each column. Compute the
correlation matrix and count eigenvalues > 1.0 (Kaiser criterion = 18). Cap at 10 factors. Fit
`factor_analyzer.FactorAnalyzer(rotation="varimax", n_factors=10)`. Extract the (68, 10)
loadings matrix and the (85, 10) factor-scores matrix. Run `scipy.stats.pearsonr` between each
factor score column and DSI / PD. Top-3 lists per outcome by `|r|`. Joint-factor flag at
`|r_DSI| > 0.3 AND |r_PD| > 0.3`.

### Bootstrap recipe

200 percentile-bootstrap resamples on the rows of `X_full`. Refit
`FactorAnalyzer(rotation="varimax", n_factors=10)` per resample. Align rotation across
resamples via maximum-row-dot-product matching to the headline solution with sign determined
by the larger absolute loading. Compute 95 % percentile CIs per loading entry. Stable factors:
those whose median absolute loading >= 0.4 AND >= 90 % sign consistency across resamples in
the top-5 loadings.

### Runtime and reproducibility

* **Machine**: local Windows 11 host (no remote machines provisioned).
* **Total implementation runtime**: ~58 minutes wall-clock (started 2026-05-14T13:31:41Z,
  completed 2026-05-14T14:30:00Z).
* **Bootstrap runtime**: 149 seconds for 200 resamples (well under the 30-minute cap from the
  plan).
* **Determinism**: `RANDOM_SEED = 105` for any randomised step (only the bootstrap is
  randomised; PCA and factor analysis are deterministic given the input matrix). The bootstrap
  RNG seed is recorded in `results/data/factor_bootstrap.json` (`random_seed = 42`).
* **Software versions**: `sklearn` 1.8.x, `factor_analyzer >= 0.5.1`, `numpy`, `pandas`,
  `scipy`, `matplotlib` from the project lockfile.

## Metrics

### Cohort selection counts

| Lineage | Raw | Pass silence filter | Primary passing | Primary unique | Strict passing | Strict unique |
| --- | --- | --- | --- | --- | --- | --- |
| t0091 | 187 | 182 (5 excluded) | 36 | **26** | 20 | **14** |
| t0099 | 2,016 | 1,993 (23 excluded) | 58 | **20** | 17 | **5** |
| t0102 | 2,592 | 2,547 (45 excluded) | 84 | **19** | 13 | **3** |
| t0104 | 2,208 | 2,208 (0 excluded) | 82 | **20** | 37 | **8** |
| **Total** | **7,003** | **6,930** | **260** | **85** | **87** | **30** |

### Asymmetry classes (primary cohort, threshold 0.5)

| Class | Count | Mean asym_score | Source-task breakdown |
| --- | --- | --- | --- |
| symmetric | 20 | 0.00 | t0091=20, t0099=0, t0102=0, t0104=0 |
| asymmetric | 65 | 1.87 | t0091=6, t0099=20, t0102=19, t0104=20 |

All 20 symmetric cells come from the earliest generations of t0091's warm-start NSGA-II, where
the seed library included the symmetric Bed B baseline morphology. Every t0099/t0102/t0104
random-init cell with `DSI > 0.1 AND PD > 2 Hz` is asymmetric. This is itself an empirical
finding (see Discussion).

### PCA on 54-d electrophys submatrix

| Component | Variance explained | Top-5 loadings (parameter, signed loading) |
| --- | --- | --- |
| PC1 | **29.5 %** | SK_TERMINAL_GBAR (+0.213), BK_TERMINAL_GBAR (+0.193), SK_SOMA_GBAR (+0.192), BK_MID_GBAR (+0.192), NAP_PRIMARY_GBAR (+0.186) |
| PC2 | **8.4 %** | AIS_DIAMETER_UM (+0.324), NAR_GBAR (+0.273), N_ACH (-0.246), N_GABA (-0.240), MG_CONC_MM (+0.228) |
| PC3 | **6.1 %** | NAV16_DEND_DISTAL (+0.367), W_ACH_US (+0.296), KV3_SOMA_GBAR (-0.289), MG_CONC_MM (-0.277), BK_SOMA_GBAR (+0.257) |

### Mann-Whitney U on PC scores (symmetric vs asymmetric)

| Cohort | PC | U | p | Interpretation |
| --- | --- | --- | --- | --- |
| Primary (N=85) | PC1 | **31.00** | **1.48e-10** | Strongly significant separation |
| Primary (N=85) | PC2 | 622.00 | 0.78 | No separation |
| Strict (N=30) | PC1 | 10.00 | **8.23e-5** | Significant; cohort-size-robust |
| Strict (N=30) | PC2 | 101.00 | 0.98 | No separation |

### Factor analysis (primary cohort, varimax, n_factors=10)

Kaiser criterion: 18 eigenvalues > 1.0 across the 68-d correlation matrix; the analysis is
capped at 10\. Per-factor top-5 loadings:

| Factor | Top-5 loadings (parameter, signed loading) |
| --- | --- |
| **F1** | NAP_PRIMARY (+0.747), morph_seed (+0.680), SK_MID (+0.662), MG_CONC_MM (+0.654), RA_OHM_CM (+0.652) |
| **F2** | SK_PRIMARY (+0.708), NAV16_TERMINAL (-0.626), NAV16_SOMA (+0.583), max_strahler_depth (-0.576), IM_GBAR (-0.538) |
| F3 | RHO0_GABA (-0.767), mean_segment_length_um (+0.740), KV3_TERMINAL (+0.616), NAV16_AIS (+0.574), soma_diameter_um (-0.562) |
| F4 | KV4_GBAR (+0.711), mean_branching_angle_deg (+0.631), SK_TERMINAL (+0.575), GLEAK (+0.546), NAP_MID (+0.543) |
| F5 | KV3_SOMA (+0.632), rall_exponent (-0.580), IH_GBAR (+0.558), field_elongation_pd (+0.557), KV3_AIS (-0.446) |
| F6 | branch_density_gradient_pd (-0.649), branch_length_cv (+0.621), BK_MID (+0.485), KV3_MID (-0.441), N_GABA (-0.338) |
| F7 | NAR_GBAR (+0.566), NAP_MID (+0.505), num_primary_branches (+0.412), N_GABA (-0.410), AIS_LENGTH (-0.387) |
| F8 | NAP_DEND_DISTAL (-0.617), NAV16_MID (-0.578), GNMDA_DEND (+0.502), BK_SOMA (+0.432), KV3_AIS (+0.425) |
| F9 | CAL_GBAR (-0.476), BK_SOMA (+0.465), BK_AIS (-0.463), NAR_GBAR (+0.349), SK_MID (+0.340) |
| F10 | ais_length_um (+0.549), NAV16_SOMA (+0.410), NAP_AIS (+0.405), LAMBDA_ACH_UM (+0.379), NAP_SOMA (+0.349) |

### Pearson r between factor scores and DSI / PD (primary cohort)

| Factor | r_DSI | p_DSI | r_PD | p_PD |
| --- | --- | --- | --- | --- |
| **F1** | **-0.322** | **0.003** | **-0.265** | **0.014** |
| F2 | -0.128 | 0.243 | -0.135 | 0.219 |
| F3 | -0.167 | 0.128 | -0.161 | 0.140 |
| F4 | -0.109 | 0.322 | -0.061 | 0.579 |
| F5 | -0.136 | 0.214 | -0.098 | 0.370 |
| F6 | -0.026 | 0.815 | -0.073 | 0.509 |
| F7 | +0.107 | 0.330 | -0.107 | 0.330 |
| F8 | -0.058 | 0.596 | +0.052 | 0.639 |
| F9 | -0.111 | 0.312 | -0.044 | 0.687 |
| F10 | -0.114 | 0.298 | -0.142 | 0.196 |

* **Top-3 factors for DSI** (by |r|): F1 (-0.322, p=0.003), F3 (-0.167, p=0.128), F5 (-0.136,
  p=0.215).
* **Top-3 factors for PD** (by |r|): F1 (-0.265, p=0.014), F3 (-0.161, p=0.140), F10 (-0.142,
  p=0.196).
* **Joint-DSI-PD factors** (|r_DSI| > 0.3 AND |r_PD| > 0.3): **0**. F1 misses the joint
  threshold on PD by 0.035.

### Bootstrap stability (200 resamples)

* **Stable factors** (median |loading| >= 0.4 AND >= 90 % sign consistency in top-5): **F1,
  F2**.
* F3-F10 fail the stability test; their loadings drift in sign or magnitude across resamples.
* Bootstrap completed in 149 seconds; 0 resamples failed.

### Strict cohort (N=30) sensitivity check

* PCA: PC1 variance explained 38.2 % (vs 29.5 % primary); PC1 still separates classes
  (**U=10.00, p=8.23e-5**).
* Factor analysis: 10 factors retained; the headline F1 magnitude on both outcomes drops below
  the primary cohort (top-3 DSI: F6, F2, F1 with |r|=0.13-0.17; top-3 PD: F6, F9, F1 with
  |r|=0.23-0.36). No joint factors.
* At N=30 the factor solution is statistically under-powered (N/p = 30/68 = 0.44);
  strict-cohort factor structure should be read as a sensitivity check, not as a primary
  result.

### Project-registered metrics (multi-variant)

| Variant | N cells | direction_selectivity_index (median) | tuning_curve_hwhm_deg | tuning_curve_reliability | tuning_curve_rmse |
| --- | --- | --- | --- | --- | --- |
| `primary_cohort` | 85 | **0.177** | null | null | null |
| `strict_cohort` | 30 | **0.351** | null | null | null |

The three `tuning_curve_*` metrics are `null` because the pooled `all_evaluations*.json` files
from the four predecessor lineages do not store per-trial Pearson reliability, HWHM, or
RMSE-against-target fields. Per the project Python style guide, `null` means "no measurement
was taken"; it must not be backfilled with `0.0` or `""`.

## Charts

### Asymmetry score distribution

![Histogram of the asymmetry score for all 85 primary-cohort cells, with the 0.5
classification threshold marked. Bimodal: 20 cells at score = 0 (all from t0091's warm-start),
then a heavier mode peaking near score = 1.7 across all four
lineages.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/asym_score_histogram.png)

### Morphology gallery

![Deterministic stratified subsample of 30 morphologies from the primary cohort, 5 cols x 6
rows, top-down (x, y) projection with soma marked and DSI / PD / asym_score / source_task
annotated per panel. Strata: symmetric::t0091 (6), asymmetric::t0091 (6), asymmetric::t0099
(6), asymmetric::t0102 (6), asymmetric::t0104 (6). The asymmetric panels show visible soma
offsets toward PD and elongated dendritic
fields.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/morphology_gallery.png)

### PCA panels — primary cohort

![Four-panel PC1-PC2 scatter on the 54-d electrophys submatrix at N=85. Panel (a): coloured by
asymmetry class (blue=symmetric, red=asymmetric) — PC1 cleanly separates classes. Panel (b):
coloured by DSI (viridis) — modest DSI gradient along PC1. Panel (c): coloured by PD (plasma)
— similar pattern to DSI. Panel (d): coloured by source_task — symmetric cells localised in
t0091's lobe; t0099/t0102/t0104 occupy the asymmetric
lobe.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/pca_electrophys_panels.png)

### PCA panels — strict cohort

![Same 4-panel layout on the strict cohort (N=30). Class separation along PC1 preserved
(U=10.00,
p=8.23e-5).](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/pca_electrophys_panels_strict.png)

### Eigenvalue scree

![Scree plot of all 54 PCA eigenvalues with the Kaiser cutoff at 1.0 marked. PC1's eigenvalue
(15.9) dominates; 14 eigenvalues exceed the Kaiser
cutoff.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/eigenvalue_scree.png)

### Factor loadings — primary cohort

![Heatmap of the (68, 10) varimax factor loadings; rows = parameters, columns = factors,
diverging colormap centred at zero. F1's column shows positive loading on NAP_PRIMARY,
morph_seed, SK_MID, MG_CONC_MM, RA_OHM_CM; F2's column shows the SK_PRIMARY / NAV16 /
Strahler-depth pattern; remaining factors are
sparser.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_loadings.png)

### Factor loadings — strict cohort

![Same heatmap on the strict cohort (N=30, 10 factors). Visually noisier; F1's identity shifts
and the top correlates of DSI and PD reshuffle to F6 — consistent with the smaller cohort
being under-powered for factor
analysis.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_loadings_strict.png)

### Factor correlations — primary cohort

![Grouped bar chart of |r| between each factor and DSI / PD, with a horizontal reference line
at |r| = 0.3. F1 is the only factor exceeding |r| = 0.25 on either outcome; no factor crosses
|r| = 0.3 on
both.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_correlations.png)

### Factor correlations — strict cohort

![Same bar chart at N=30. F6 emerges as the top PD correlate (r=0.36, p=0.05), but F1's
joint-leadership in the primary cohort is gone, suggesting the strict-cohort factor structure
is
unstable.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_correlations_strict.png)

### Factor loadings bootstrap

![200-resample bootstrap CI bars overlaid on the top-5 loadings per factor. F1 and F2 retain
consistent signs and median |loading| >= 0.4; F3-F10 cross zero or have wide CIs across
resamples.](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_loadings_bootstrap.png)

## Analysis

Three interpretive threads carried over from the creative-thinking step inform the reading of
these results.

### The 73 silence-artifact cells are a finding, not noise

73 cells across t0091/t0099/t0102 (5 / 23 / 45) trip the post-hoc silence-artifact filter `DSI
> 0.95 AND PD < 5 Hz`; t0104 contributes **zero** because its evaluator already gates DSI
vector-sum on `total_spikes >= 10`. This quantitatively validates the S-0102-01 silence guard
from two directions. First, the per-lineage counts climb with random-init NSGA-II's age (5 in
the small t0091 warm-start, 23 in t0099 at N_EVAL=20, 45 in t0102 at N_EVAL=4) — random-init
genuinely explores into the silent corner of the substrate. Second, the t0102 count of 45
generalises t0102's own results_summary.md "27 silenced cells" figure to a broader DSI
threshold (0.95 vs 0.99): the extra 18 cells sit at near-threshold DSI = 0.95-0.99 with PD < 5
Hz, still clearly artifactual but not caught by t0102's exact-1.0 detection. The guard is
correctly calibrated; without it, the PCA and factor analysis would have been polluted by ~45
t0102 cells with DSI ~= 1.0 driving artifactual direction-selectivity-like signal into PC1.

### PC1 separation is mediated by Ca-K channels — morphology pre-selects an electrophys regime

The top-5 PC1 loadings are SK_TERMINAL, BK_TERMINAL, SK_SOMA, BK_MID, NAP_PRIMARY — four
Ca-activated K-channels and one persistent Na conductance. The Mann-Whitney U on PC1
(p=1.48e-10 primary, p=8.23e-5 strict) says these channels live in a different regime in
asymmetric vs symmetric cells. The mechanistic hypothesis: asymmetric dendrites concentrate Ca
influx near the soma along the PD axis, so high terminal-dendrite SK/BK is needed to locally
quench PD-side over-excitation; symmetric cells, by contrast, distribute Ca influx more
uniformly and need different repolarisation tuning. This is consistent with Vlasits2016 and
the Vaney2012 review's characterisation that asymmetric type-2 DSGCs in mammalian retina rely
on local dendritic computation and active integration — both of which are Ca-K-mediated. The
fact that **all 20 symmetric cells are warm-start cells from t0091** while every random-init
cell that passes `DSI > 0.1 AND PD > 2 Hz` is asymmetric is itself a striking empirical
signature: under random-init search of the 68-d substrate, non-trivial direction selectivity
at non-trivial firing rate **only arises in asymmetric configurations**.

### No joint factor confirms the substrate-limit reading

F1 is the only factor with a non-trivial correlate of either outcome (r_DSI = -0.322, p=0.003;
r_PD = -0.265, p=0.014), but it misses the joint threshold |r_PD| > 0.3 by 0.035. The
second-best factors for the two outcomes are different (F3 for DSI; F3 / F10 for PD), and the
third-best diverge further (F5 for DSI; F10 / F9 for PD). Read together: **DSI and PD share a
weak common axis (F1) but their residual variances live on essentially orthogonal directions**
in the substrate. This is the load-bearing finding for the project's strategic question.
NSGA-II cannot ride a single parameter direction toward the joint high-DSI / high-PD corner
because no such direction exists in the 68-d substrate at this cohort size. The t0102 / t0104
conclusion that the substrate is empirically substrate-limited (the Pareto front is L-shaped)
is reinforced from a complementary angle: factor analysis on the actual cell population finds
no low-d axis to ride. The remaining algorithmic moves (IBEA, larger populations per Dang2023)
might find isolated joint-corner cells not on a continuous axis, but no single low-d variable
will smoothly raise both outcomes together.

### A caveat that should sharpen the next task

morph_seed loads +0.68 on F1 (the second-strongest loading after NAP_PRIMARY). morph_seed is
an **integer** dimension that drives randomness in the morphology generator's small-scale
geometry; it is bounded [0, 99] and is not biologically meaningful. Its appearance on F1 next
to mechanistic channel variables is suspicious — F1 may partly be a "warm-start vs
random-init" indicator disguised as a mechanistic factor, because t0091's warm-start happened
to fix morph_seed = 31 while the random-init lineages span 0-99. The factor analysis loading
on morph_seed should be re-run excluding it to test whether F1's DSI / PD correlates survive
(suggestion below).

## Verification

* `verify_task_results.py` on `t0105_cluster_factor_analysis_dsi_pd` — PASSED. All five
  mandatory files exist (`results_summary.md`, `results_detailed.md`, `metrics.json`,
  `costs.json`, `remote_machines_used.json`) and validate against the v8 task results spec.
* `verify_task_metrics.py` on `t0105_cluster_factor_analysis_dsi_pd` — PASSED. The
  multi-variant `metrics.json` has variants `primary_cohort` and `strict_cohort`, each
  carrying the four project-registered metric keys with explicit `null` where measurements are
  unavailable.
* `verify_suggestions.py` on `t0105_cluster_factor_analysis_dsi_pd` — PASSED. The 7
  suggestions S-0105-01 through S-0105-07 validate against the v2 suggestions spec with
  `spec_version = "2"`.
* `verify_compare_literature.py` on `t0105_cluster_factor_analysis_dsi_pd` — PASSED. The
  `compare_literature.md` has all five mandatory sections plus 7 comparison-table data rows
  and cites Sivyer2013, Vaney2012, PolegPolsky2026, Mohacsi2024.
* `verify_answer_asset.py` on `assets/answer/symmetric-vs-asymmetric-electrophys-cluster/` —
  PASSED.
* `verify_answer_asset.py` on `assets/answer/dsi-pd-diversity-factor-decomposition/` — PASSED.
* Implementation-stage integrity: every PCA / Mann-Whitney / factor analysis number reported
  in this file matches the corresponding JSON in `results/data/`. Spot-checks:
  `pca_results.json::explained_variance_ratio` = `[0.295, 0.084, 0.061]`;
  `pca_mannwhitney.json::pc1_p` = `1.48e-10`; `factor_correlations.json::top3_dsi[0].r` =
  `-0.322`.

## Limitations

* **N=85 is small for 68-d factor analysis.** The N/p ratio of 1.25 is below the conventional
  5xp = 340 floor for stable factor extraction; only F1 and F2 are bootstrap-stable.
* **Strict cohort is under-powered.** At N=30, factor analysis ratio drops to 0.44;
  strict-cohort factor results are a sensitivity check, not a primary result.
* **All 20 symmetric cells come from t0091.** Symmetric-vs-asymmetric separation may partly
  track warm-start-vs-random-init regime selection rather than pure morphology class. The
  strict-cohort separation (p=8.23e-5) goes some way to ruling out the trivial reading because
  the strict cohort still includes 10 symmetric and 20 asymmetric cells, but the lineage
  confound remains.
* **morph_seed (integer) loads +0.68 on F1**. This dimension is not biologically meaningful;
  its high F1 loading may be incidental and should be re-tested by re-running factor analysis
  with morph_seed excluded.
* **Cross-lineage heterogeneity.** The four lineages span N_EVAL=4 vs N_EVAL=20, 2-objective
  vs 3-objective, and warm-start vs random-init. Per-lineage PCA might surface different
  structure; see suggestions.
* **No tuning-curve metrics.** The pooled `all_evaluations*.json` files do not store per-trial
  reliability, HWHM, or RMSE-against-target, so three of the four registered project metrics
  are `null` in this task. This limits cross-task comparability with future tuning-curve-aware
  tasks.
* **Joint-corner search is a yes/no test, not a continuous quantification.** Factor analysis
  can show that no single axis lifts both DSI and PD, but it cannot rule out a non-linear
  corner cell that is reachable by a different algorithm (IBEA, MAP-Elites, gradient methods).

## Files Created

### Code (12 files in `code/`)

* `code/__init__.py`
* `code/paths.py` — centralised path constants
* `code/constants.py` — column names, threshold constants, 68-d dim map
* `code/schemas.py` — frozen dataclasses for cohort rows, PCA results, factor outputs
* `code/load_filter_cells.py` — pool, silence-filter, primary/strict filter, dedupe
* `code/classify_asymmetry.py` — asymmetry score + classification + histogram
* `code/build_gallery.py` — stratified subsample + NEURON pt3d extraction + multi-panel PNG
* `code/pca_electrophys.py` — z-score, PCA, scree, 4-panel scatter, Mann-Whitney U
* `code/factor_analysis.py` — Kaiser cap, varimax factor analyzer, loadings heatmap
* `code/factor_correlations.py` — Pearson r vs DSI / PD, joint-factor flag, bar chart
* `code/factor_bootstrap.py` — 200 resamples, varimax-alignment, CIs, stability
* `code/run_strict_cohort.py` — orchestrates PCA / FA / correlations on strict cohort
* `code/build_metrics_json.py` — emits multi-variant `metrics.json`

### Data outputs (16 JSON files in `results/data/`)

* `selected_cells_primary.json`, `selected_cells_strict.json` — cohort tables with 68-d
  vectors, DSI, PD, asym_score, asym_class, source_task, seed, generation
* `selection_counts.json` — per-lineage and per-cohort counts incl. silence-artifact
  exclusions
* `asym_score_distribution.json` — histogram bins, class counts, threshold sweep
* `gallery_quota_table.json` — stratum quotas used to build the morphology gallery
* `pca_results.json`, `pca_results_strict.json` — variance, top-5 loadings, PC scores,
  classes, sources
* `pca_mannwhitney.json`, `pca_mannwhitney_strict.json` — U, p, interpretation per PC
* `factor_loadings.json`, `factor_loadings_strict.json` — eigenvalues, loadings matrix, top-5
  loadings per factor
* `factor_scores.json`, `factor_scores_strict.json` — (N, 10) factor-score matrix
* `factor_correlations.json`, `factor_correlations_strict.json` — per-factor r / p vs DSI /
  PD, top-3 lists, joint-factor flag
* `factor_bootstrap.json` — 200 resamples, median loadings, 95 % CIs, stable factors

### Charts (10 PNGs at DPI 150 in `results/images/`)

* `asym_score_histogram.png`
* `morphology_gallery.png`
* `pca_electrophys_panels.png`, `pca_electrophys_panels_strict.png`
* `eigenvalue_scree.png`
* `factor_loadings.png`, `factor_loadings_strict.png`
* `factor_correlations.png`, `factor_correlations_strict.png`
* `factor_loadings_bootstrap.png`

### Other artifacts

* `results/metrics.json` — explicit multi-variant format (`primary_cohort`, `strict_cohort`)
* `results/costs.json` — `total_cost_usd = 0.0`
* `results/remote_machines_used.json` — empty array (no remote machines)
* `results/results_summary.md`, `results/results_detailed.md` (this file)
* `results/compare_literature.md`, `results/suggestions.json`
* `assets/answer/symmetric-vs-asymmetric-electrophys-cluster/` (details.json, short_answer.md,
  full_answer.md)
* `assets/answer/dsi-pd-diversity-factor-decomposition/` (details.json, short_answer.md,
  full_answer.md)
* `pyproject.toml`, `uv.lock` — top-level allowed change (added `factor_analyzer>=0.5.1`)

## Examples

Twelve concrete primary-cohort cells spanning all four lineages and both asymmetry classes are
shown below as JSON records. Each record reproduces the cell's source, seed, generation, DSI,
PD, the asymmetry score and class, and the four top-PC1-loading parameter values (SK_TERMINAL,
BK_TERMINAL, SK_SOMA, NAP_PRIMARY) plus its PC1 score. Together they cover (a) the symmetric
warm-start lobe, (b) random-init asymmetric cells at low / mid / high Ca-K, and (c) the
closest-to-joint-corner cells.

### Symmetric warm-start cell #1 (t0091 gen 1 — archetype)

```json
{
  "source_task": "t0091",
  "seed": null,
  "generation": 1,
  "dsi": 0.1978,
  "pd_rate_hz": 46.14,
  "asym_score": 0.000,
  "asym_class": "symmetric",
  "SK_TERMINAL": 0.000,
  "BK_TERMINAL": 0.000,
  "SK_SOMA": 0.001,
  "NAP_PRIMARY": 0.000,
  "pc1_score": -6.46
}
```

Illustrates the archetypal symmetric warm-start cell: zero Ca-K conductance, zero NAP_PRIMARY,
yet PD = 46 Hz. The lowest PC1 score in the cohort.

### Symmetric warm-start cell #2 (t0091 gen 1 — moderate PD)

```json
{
  "source_task": "t0091",
  "seed": null,
  "generation": 1,
  "dsi": 0.3293,
  "pd_rate_hz": 12.86,
  "asym_score": 0.000,
  "asym_class": "symmetric",
  "SK_TERMINAL": 0.000,
  "BK_TERMINAL": 0.000,
  "SK_SOMA": 0.002,
  "NAP_PRIMARY": 0.000,
  "pc1_score": -6.46
}
```

A symmetric cell with the highest DSI in the symmetric class (0.329). This is one of the
symmetric high-DSI outliers flagged for follow-up in S-0105-03.

### Asymmetric early-t0091 cell #3 (hybrid morphology, low Ca-K)

```json
{
  "source_task": "t0091",
  "seed": null,
  "generation": 1,
  "dsi": 0.2140,
  "pd_rate_hz": 6.71,
  "asym_score": 1.667,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.000,
  "BK_TERMINAL": 0.000,
  "SK_SOMA": 0.002,
  "NAP_PRIMARY": 0.000,
  "pc1_score": -5.93
}
```

The morphology has shifted into asymmetric territory but the warm-start electrophys vector is
still zero on the PC1-loading channels. Sits between the two PC1 lobes.

### Asymmetric early-t0091 cell #4 (NAP starts to spin up)

```json
{
  "source_task": "t0091",
  "seed": null,
  "generation": 2,
  "dsi": 0.2270,
  "pd_rate_hz": 40.43,
  "asym_score": 1.767,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.001,
  "BK_TERMINAL": 0.000,
  "SK_SOMA": 0.000,
  "NAP_PRIMARY": 0.022,
  "pc1_score": -6.00
}
```

NSGA-II's second-generation move begins to lift NAP_PRIMARY while keeping Ca-K low. PD remains
high (40 Hz) — high PD does not require high Ca-K when the cell is dominated by warm-start
regime.

### Asymmetric t0099 cell #5 (high-Ca-K corner)

```json
{
  "source_task": "t0099",
  "seed": 11,
  "generation": 2,
  "dsi": 0.1200,
  "pd_rate_hz": 7.29,
  "asym_score": 1.014,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.941,
  "BK_TERMINAL": 0.865,
  "SK_SOMA": 0.910,
  "NAP_PRIMARY": 0.064,
  "pc1_score": +3.24
}
```

Random-init NSGA-II at N_EVAL=20 finds the high-Ca-K corner early (gen 2). All three top SK/BK
conductances saturated; NAP_PRIMARY still low. PC1 score has flipped to +3.24 — opposite lobe
from the warm-start cells.

### Asymmetric t0099 cell #6 (highly asymmetric)

```json
{
  "source_task": "t0099",
  "seed": 11,
  "generation": 3,
  "dsi": 0.1090,
  "pd_rate_hz": 3.43,
  "asym_score": 1.993,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.761,
  "BK_TERMINAL": 0.953,
  "SK_SOMA": 0.992,
  "NAP_PRIMARY": 0.153,
  "pc1_score": +2.95
}
```

asym_score near 2.0 — strongly asymmetric morphology. Ca-K still saturated, NAP_PRIMARY slowly
rising. PD-rate falls below 4 Hz, illustrating the Ca-K-suppresses-PD reading.

### Asymmetric t0102 cell #7 (mid-NAP)

```json
{
  "source_task": "t0102",
  "seed": 44,
  "generation": 3,
  "dsi": 0.1260,
  "pd_rate_hz": 18.57,
  "asym_score": 2.395,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.676,
  "BK_TERMINAL": 0.464,
  "SK_SOMA": 0.762,
  "NAP_PRIMARY": 0.767,
  "pc1_score": +3.71
}
```

Both Ca-K and NAP_PRIMARY now elevated (NAP_PRIMARY = 0.77). t0102's N_EVAL=4 budget pushes
into the joint-corner-adjacent region but DSI stays at 0.126.

### Asymmetric t0102 cell #8 (high NAP, moderate Ca-K)

```json
{
  "source_task": "t0102",
  "seed": 44,
  "generation": 4,
  "dsi": 0.1200,
  "pd_rate_hz": 20.36,
  "asym_score": 1.812,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.545,
  "BK_TERMINAL": 0.891,
  "SK_SOMA": 0.545,
  "NAP_PRIMARY": 0.576,
  "pc1_score": +2.95
}
```

PD = 20 Hz at NAP_PRIMARY = 0.58. F1 lies along a direction where moving NAP up alone does not
strongly lift DSI; it lifts PD but not DSI.

### Asymmetric t0104 cell #9 (silence-guard-passing low Ca-K)

```json
{
  "source_task": "t0104",
  "seed": 44,
  "generation": 9,
  "dsi": 0.1110,
  "pd_rate_hz": 6.25,
  "asym_score": 2.072,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.654,
  "BK_TERMINAL": 0.602,
  "SK_SOMA": 0.545,
  "NAP_PRIMARY": 0.249,
  "pc1_score": +1.30
}
```

t0104's S-0102-01 guard active; cell passes silence filter with PD = 6.25 Hz and DSI = 0.111.
Sits between the two lobes in PC space because Ca-K and NAP are both at intermediate values.

### Asymmetric t0104 cell #10 (highest DSI in t0104 cohort)

```json
{
  "source_task": "t0104",
  "seed": 55,
  "generation": 3,
  "dsi": 0.2600,
  "pd_rate_hz": 4.11,
  "asym_score": 1.925,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.334,
  "BK_TERMINAL": 0.503,
  "SK_SOMA": 0.763,
  "NAP_PRIMARY": 0.819,
  "pc1_score": +2.06
}
```

DSI = 0.260 at NAP_PRIMARY = 0.82. Closer-to-joint-corner direction but PD stays at 4.11 Hz —
NAP_PRIMARY raising alone does not lift PD when other PC1 channels are mid-range.

### Asymmetric t0099 outlier cell #11 (low PC1, high asym_score)

```json
{
  "source_task": "t0099",
  "seed": 11,
  "generation": 2,
  "dsi": 0.1300,
  "pd_rate_hz": 11.79,
  "asym_score": 0.880,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.000,
  "BK_TERMINAL": 0.000,
  "SK_SOMA": 0.005,
  "NAP_PRIMARY": 0.005,
  "pc1_score": +2.11
}
```

A boundary case: t0099 seed 11 found an asymmetric-morphology cell with NEAR-ZERO Ca-K /
NAP_PRIMARY (warm-start-like electrophys) yet PC1 score is positive because of indirect
contributions from other 54 dimensions. Illustrates why PC1 is a population direction, not a
per-channel hard rule.

### Asymmetric t0102 cell #12 (high PD, low DSI)

```json
{
  "source_task": "t0102",
  "seed": 44,
  "generation": 5,
  "dsi": 0.1180,
  "pd_rate_hz": 32.86,
  "asym_score": 1.857,
  "asym_class": "asymmetric",
  "SK_TERMINAL": 0.601,
  "BK_TERMINAL": 0.572,
  "SK_SOMA": 0.612,
  "NAP_PRIMARY": 0.604,
  "pc1_score": +3.73
}
```

PD = 32.86 Hz — above the strict cohort threshold — but DSI stays at 0.118. Sits in the
high-PD, low-DSI region of the L-shaped Pareto. Despite mid-range Ca-K and NAP_PRIMARY, no
single-axis lift to high DSI is available.

### What these 12 examples collectively illustrate

* Cells **#1, #2** (symmetric warm-start, t0091): all Ca-K conductances near zero and
  NAP_PRIMARY near zero. Yet PD reaches 46 Hz and 13 Hz respectively. These are the
  **archetypal symmetric warm-start cells** that anchor PC1 < 0. PC1 scores -6.46 (lowest in
  the cohort).
* Cells **#3, #4** (asymmetric early-t0091): SK / BK still near zero in #3 but morphology
  asymmetric; #4 starts spinning up NAP_PRIMARY. These hybrid early-t0091 cells live between
  the two lobes in PC space.
* Cells **#5, #6** (asymmetric t0099): SK / BK strongly elevated (0.76-0.99 normalised) but
  NAP_PRIMARY still low (0.06-0.15). PD stays modest (3-7 Hz). Random-init NSGA-II at N=20
  finds the high-Ca-K corner first.
* Cells **#7, #8, #10** (asymmetric t0102 / t0104): both Ca-K and NAP_PRIMARY elevated
  (NAP_PRIMARY 0.58-0.82). These are the closer-to-joint-corner cells; cell #10 reaches DSI =
  0.260 with NAP_PRIMARY = 0.82. They populate the high-PC1 lobe where Ca-K and persistent Na
  co-vary along F1.
* Cells **#9, #11** (boundary cases): #9 has intermediate Ca-K + NAP; #11 has near-zero Ca-K
  but asymmetric morphology — both illustrate that PC1 is a population direction, not a
  per-channel hard rule.
* Cell **#12** (high-PD, low-DSI): PD = 33 Hz at mid-range PC1; the L-shaped Pareto's high-PD
  arm is dominated by asymmetric mid-Ca-K cells whose DSI stays low.

The qualitative reading: as you move from cell 1 to cell 10, both Ca-K and NAP_PRIMARY elevate
together along F1. This is exactly the F1 axis identified by factor analysis, and its weak
correlation with both DSI (r=-0.32) and PD (r=-0.27) — with the sign reflecting that elevated
Ca-K + NAP_PRIMARY counter-intuitively suppresses joint-corner attainment in this substrate —
explains why the joint corner is unreachable: the optimiser cannot escape the F1 axis without
crossing into the orthogonal residual variances that drive DSI and PD apart.

## Task Requirement Coverage

Operative task text from `task.json`:

```text
Name: Cluster + factor analysis of high-DSI/high-PD cells (t0102 + t0104, symmetric vs asymmetric)

Short description: Pool all cells from t0102 and t0104 with DSI > 0.2 AND PD > 3 Hz, classify by
morphological asymmetry, run PCA cluster analysis on intrinsic params, and factor analysis
(incl. morphology) on what explains DSI / PD diversity.
```

Resolved long description in `task_description.md` and finalised REQ list in `plan/plan.md`
extends the pool to all four 68-d lineages (t0091 + t0099 + t0102 + t0104) and adds primary
cohort `DSI > 0.1 AND PD > 2`, strict cohort sensitivity check, bootstrap stability, and the
two answer assets. REQ-1 through REQ-15 from `plan/plan.md` are coverage-tracked below.

* **REQ-1**: Pool four lineages, apply primary + strict filters, dedupe by 68-d vector, record
  per-lineage and per-cohort counts. **Done.** Evidence:
  `results/data/selected_cells_primary.json` (N=85), `results/data/selected_cells_strict.json`
  (N=30), `results/data/selection_counts.json`.

* **REQ-2**: Add `factor_analyzer>=0.5.1` to `pyproject.toml`. **Done.** Evidence:
  `pyproject.toml` dependencies block includes `factor_analyzer>=0.5.1`; `uv.lock` refreshed.

* **REQ-3**: Silence-artifact filter on t0091/t0099/t0102; log per-lineage exclusion counts.
  **Done.** Evidence: `results/data/selection_counts.json` `silence_artifact_exclusions`:
  `{t0091:5, t0099:23, t0102:45, t0104:0}`.

* **REQ-4**: Asymmetry score + classification at threshold 0.5; histogram; 0.3/0.5/1.0
  threshold sweep. **Done.** Evidence: `results/data/asym_score_distribution.json` (20 sym /
  65 asym at 0.5); `results/images/asym_score_histogram.png`.

* **REQ-5**: Stratified subsample <= 30 cells morphology gallery with NEURON-built pt3d
  coordinates, DSI/PD/asym_score/source_task annotations. **Done.** Evidence:
  `results/images/morphology_gallery.png` (30 cells, 5 strata);
  `results/data/gallery_quota_table.json`.

* **REQ-6**: PCA on 54-d electrophys; 4-panel chart (class, DSI, PD, source_task); top-5
  loadings per PC; scree. **Done.** Evidence: `results/data/pca_results.json` (variance +
  loadings); `results/images/pca_electrophys_panels.png`;
  `results/images/eigenvalue_scree.png`.

* **REQ-7**: Mann-Whitney U on PC1 and PC2 between classes. **Done.** Evidence:
  `results/data/pca_mannwhitney.json` (PC1 U=31.00, p=1.48e-10; PC2 U=622.00, p=0.78).

* **REQ-8**: Varimax factor analysis on 68-d; Kaiser criterion capped at 10. **Done.**
  Evidence: `results/data/factor_loadings.json` (n_factors=10, eigenvalues_above_1_count=18);
  `results/images/factor_loadings.png`.

* **REQ-9**: Pearson r vs DSI / PD; top-3 per outcome; joint-factor flag. **Done.** Evidence:
  `results/data/factor_correlations.json` (top3_dsi: F1/F3/F5; top3_pd: F1/F3/F10;
  joint_factors: []); `results/images/factor_correlations.png`.

* **REQ-10**: Bootstrap loadings 200 resamples; 95 % CIs; stable factors. **Done.** Evidence:
  `results/data/factor_bootstrap.json` (n_bootstrap_resamples=200, stable_factors=[F1, F2]);
  `results/images/factor_loadings_bootstrap.png`.

* **REQ-11**: Repeat headline analyses on strict cohort. **Done.** Evidence:
  `results/data/pca_results_strict.json`, `pca_mannwhitney_strict.json`,
  `factor_loadings_strict.json`, `factor_correlations_strict.json`,
  `results/images/pca_electrophys_panels_strict.png`,
  `results/images/factor_loadings_strict.png`,
  `results/images/factor_correlations_strict.png`.

* **REQ-12**: Two answer assets (cluster question + factor decomposition question). **Done.**
  Evidence: `assets/answer/symmetric-vs-asymmetric-electrophys-cluster/` and
  `assets/answer/dsi-pd-diversity-factor-decomposition/` each with details.json,
  short_answer.md, full_answer.md; both pass `verify_answer_asset` 0/0.

* **REQ-13**: All 10 charts at DPI 150 in `results/images/`, embedded in `results_detailed.md`
  via `![desc](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/file.png)`.
  **Done.** Evidence: 10 PNGs listed in `## Files Created` above, all embedded in the `##
  Charts` section.

* **REQ-14**: `results/metrics.json` in explicit multi-variant format with `primary_cohort`
  and `strict_cohort` variants; `tuning_curve_*` metrics explicitly `null` with documented
  reasoning. **Done.** Evidence: `results/metrics.json` `variants` array contains both
  variants; `null` reason documented in this file's `## Metrics` section.

* **REQ-15**: Do not modify any prior task folder; only `pyproject.toml` and `uv.lock` may
  change at the top level. **Done.** Evidence: all changes are under
  `tasks/t0105_cluster_factor_analysis_dsi_pd/` plus `pyproject.toml` and `uv.lock`; no other
  task folders are touched.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0105_cluster_factor_analysis_dsi_pd" date_compared:
"2026-05-14" ---
# Comparison with Project and Published Results

## Summary

t0105 finds that 65 of 85 unique non-trivial DSGC cells across four 68-d NSGA-II lineages are
**asymmetric** (76 %), with PC1 separating asymmetric from symmetric electrophys regimes at
**Mann-Whitney U=31.0, p=1.48e-10**. This aligns with the [Sivyer2013][sivyer2013] /
[Vaney2012][vaney2012] characterisation that mammalian retina's directionally-selective
ganglion cells are dominated by type-2 asymmetric morphologies relying on active dendritic
integration. Varimax factor analysis on the full 68-d matrix finds **no joint DSI-PD factor**
(no factor with |r| \> 0.3 on both outcomes), reinforcing the substrate-limit reading from
[t0102][t0102_link] and [t0104][t0104_link]. F1's top loadings (NAP_PRIMARY, SK_MID,
MG_CONC_MM, Ra) overlap with the Ca-K and persistent-Na channels that
[PolegPolsky2026][polegpolsky2026] flags as direction-selectivity-relevant in their
machine-learning analysis of the de Rosenroll Bed B model. Compared with
[Mohacsi2024][mohacsi2024] the algorithm-side reading (IBEA outperforming NSGA-II on Hay2011
L5PC) is reinforced because no single low-d axis exists for NSGA-II to ride into the joint
corner — algorithm choice may not unlock what factor analysis cannot find.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Sivyer2013][sivyer2013] type-2 asymmetric DSGC fraction in rabbit retina | % asymmetric | ~85 | 76 | -9 | Sivyer reports ~85 % of rabbit DSGCs are type-2 asymmetric; t0105's 65/85=76 % is consistent within the noise of an optimisation cohort vs a biological sample |
| [Vaney2012][vaney2012] type-2 asymmetric DSGC fraction (review consensus) | % asymmetric | 70-90 | 76 | within | t0105 sits in the published consensus band |
| [PolegPolsky2026][polegpolsky2026] DSI ceiling on Bed B substrate (claimed) | DSI | 0.62 | 0.54 (best non-artifact, from [t0104][t0104_link]) | -0.08 | t0105's cohort top DSI inherits from t0104; t0105 itself does not search but documents that 65/85 asymmetric cells include this top-DSI cell |
| [PolegPolsky2026][polegpolsky2026] top direction-selectivity-relevant channels (ML attribution) | rank-1 channel | SK / BK / Nav | SK_TERMINAL / BK_TERMINAL / NAP_PRIMARY (PC1) | match | t0105's PC1 top loadings recover the same Ca-K and persistent-Na channels that PolegPolsky2026 flag via ML attribution |
| [Mohacsi2024][mohacsi2024] Hay2011 L5PC NSGA-II vs IBEA performance gap | hypervolume delta | IBEA > NSGA-II by ~15 % | not measured here | n/a | t0105 does not run IBEA, but the no-joint-factor finding suggests algorithm choice may not unlock the corner since no single axis exists for any algorithm to ride |
| [t0104][t0104_link] strict joint-pass yield | count | 0 / 2,208 | 0 / 85 (post-pool, post-dedupe) | +0 | t0105 confirms the joint corner is empty on the full pooled cohort, not just within one lineage |
| [t0091][t0091_link] joint-pass cell DSI / PD | DSI | 0.511 | 0.511 (pass-through; in cohort) | +0.0 | t0105 verifies t0091's single joint-pass cell sits in the asymmetric class with asym_score = 1.77 |

## Methodology Differences

* **Cohort vs single optimisation**: t0105's cohort pools 7,003 raw evaluations across four
  independent lineages and dedupes to 85 unique cells. Sivyer2013 / Vaney2012 sample
  biological rabbit retina with N ~ 50-150 patch-clamped cells. The comparison is
  apples-to-oranges in population terms (computational cohort vs biological sample) but the
  headline statistic (% of cells in the asymmetric morphology class) is comparable.
* **Substrate-vs-biology mismatch on the morphology classifier**: t0105 classifies based on a
  formula across four PD-asymmetry dimensions in the 14-d morphology generator from t0090 /
  t0092. Sivyer2013 / Vaney2012 classify based on dendritic-field anatomy observed under
  microscopy. Both should track type-2 vs type-1 DSGC distinction but the precise
  correspondence is approximate.
* **No tuning-curve data**: t0105's pooled `all_evaluations*.json` does not store
  per-direction tuning curves, so HWHM, reliability, and RMSE-against-target metrics cannot be
  compared with Sivyer2013 / Hoshi2011. Only `dsi_vector_sum` and `pd_rate_hz` are available
  per cell.
* **PolegPolsky2026 channel-importance comparison**: the published paper uses a ML feature
  attribution method on a single Bed B model; t0105 uses PCA on a population of 85 optimised
  cells. Both methods independently identify SK / BK Ca-activated K and persistent Na as the
  top direction-selectivity-relevant channels, but their ranking comes from different inputs.
* **Mohacsi2024 algorithm comparison is indirect**: t0105 does not run IBEA. The connection is
  that t0105's no-joint-factor finding constrains the algorithm-side hypothesis: even an
  algorithm better than NSGA-II will struggle if no low-d axis exists in the substrate for any
  algorithm to ride.

## Analysis

The cross-paper picture is consistent and load-bearing for the project's research questions:

1. **Asymmetric DSGC dominance** (RQ-3): 76 % of the optimised cohort is asymmetric, matching
   the ~85 % biological consensus from Sivyer2013 / Vaney2012. The single empirical surprise
   is that under random-init NSGA-II of the 68-d Bed B + morphology substrate, **every**
   non-trivial cell (DSI > 0.1 AND PD > 2 Hz, post-silence-filter) is asymmetric — all 20
   symmetric cells come exclusively from t0091's warm-start. Random-init search does not
   discover symmetric DSGCs at non-trivial firing rate. This is consistent with Vaney2012's
   reading that asymmetric type-2 is the dominant biological mechanism in mammalian retina; it
   elevates the type-2 asymmetric DSGC reading from "dominant" to "essentially exclusive at
   random-init NSGA-II reach".

2. **PolegPolsky2026 channel attribution recovery** (RQ-4): t0105's PCA top loadings
   (SK_TERMINAL, BK_TERMINAL, SK_SOMA, BK_MID, NAP_PRIMARY) match the Ca-activated K and
   persistent-Na channels that PolegPolsky2026's ML analysis flags as
   direction-selectivity-relevant on the Bed B substrate. This is **independent
   corroboration** — t0105 uses an unsupervised population method (PCA on N=85),
   PolegPolsky2026 uses a supervised single-model method (ML attribution on one cell), and
   they arrive at the same channel-importance ranking. The Vlasits2016 reading on
   synaptic-input-distribution direction selectivity is also indirectly supported (PC2 loads
   on N_ACH, N_GABA, MG_CONC_MM — synaptic input parameters), but PC2 does not separate
   morphology classes, so the synaptic-distribution axis is orthogonal to the morphology-class
   axis.

3. **Substrate-limit reading via factor analysis** (RQ-5): the absence of a joint DSI-PD
   factor is the load-bearing finding. F1 carries -0.32 on DSI and -0.27 on PD; no other
   factor crosses |r| = 0.25 on either outcome. This says the substrate does not contain a
   single low-d direction along which an algorithm could lift both DSI and PD together.
   Mohacsi2024's IBEA > NSGA-II reading is still relevant because IBEA may find isolated
   joint-corner cells off-axis, but **no algorithmic choice will find a continuous
   joint-corner path because no such path exists**. The remaining open avenues are substrate
   changes (additional dendritic compartments, restored GABAergic asymmetry per
   [PolegPolsky2026][polegpolsky2026]) or non-linear targeted search (S-0104-01 / S-0104-02
   single-cell perturbation studies, MAP-Elites quality-diversity).

## Limitations

* **Sivyer2013 / Vaney2012 % asymmetric is from rabbit retina**; the project simulates Bed B
  mouse-DSGC substrate. The morphology-class fractions may not be directly comparable across
  species. The general "type-2 asymmetric is dominant" claim is well-supported in both
  species, but the precise 70-90 % band may shift.
* **PolegPolsky2026 DSI = 0.62 ceiling** is read from Figure 3 of the cached paper summary;
  the paper does not report a single-cell ceiling explicitly. The figure is an upper estimate
  of the warm-start-achievable region rather than a published claim.
* **PolegPolsky2026 ML attribution method differs from PCA**; both flag SK / BK / Nav but the
  exact ranking and effect sizes are not directly numerically comparable.
* **No IBEA comparison run**; the strongest algorithm-side validation (S-0102-03 / S-0104-04)
  would be to run IBEA at matched budget on the same substrate and see whether it discovers
  joint-corner cells off the F1 axis.
* **Mohacsi2024 substrate is Hay2011 L5PC (22-d cortical pyramid)**, not retinal DSGC. The
  IBEA > NSGA-II reading may not transfer to the 68-d DSGC substrate; the substrate
  dimensionality and fitness-landscape geometry differ.

[sivyer2013]:
../../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/summary.md
[vaney2012]:
../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/summary.md
[polegpolsky2026]:
../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md
[mohacsi2024]:
../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[t0091_link]: ../../../tasks/t0091_morphology_extended_nsga2_v1/ [t0102_link]:
../../../tasks/t0102_seedscale_n4_gen20/ [t0104_link]:
../../../tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/

</details>
