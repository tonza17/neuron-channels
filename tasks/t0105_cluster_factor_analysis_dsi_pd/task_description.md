# t0105 — Cluster + Factor Analysis of High-DSI / High-PD Cells across t0102 and t0104

## Context

Direct researcher commission at 2026-05-14 after the t0104 result landed. t0102 (3-objective NSGA-II
with robustness) and t0104 (2-objective NSGA-II without robustness, with the DSI-silence guard)
together produced 4,800 evaluations across 4 GA seeds. The two best cells in t0104 are strongly
asymmetric DSGCs (soma offset toward PD, dendritic field 2× elongated, primary branches
PD-concentrated). The follow-up question: across all cells that produced *some* direction
selectivity AND *some* firing — not just the Pareto extremes — does the asymmetric morphology
motif hold, and which of the 68 input parameters drive DSI and PD diversity?

A scratch comparison plot (`scratch_t0102_t0104_morph_compare.png` on main) showed top-5 cells per
optimisation but was limited to extreme cells. This task extends to the full population of
non-trivial cells.

## Goal

For all cells from t0102 + t0104 with **DSI > 0.2 AND PD-rate > 3 Hz** (the "non-trivial both-axes"
population), answer three questions:

1. **What does a morphology gallery of these cells look like?** Plot each cell's morphology (or a
   representative subsample if the count > 30) with its DSI and PD values annotated, separated by
   source optimisation.

2. **Do the intrinsic (electrophys) parameters cluster by morphological asymmetry?** Run PCA on the
   54-d electrophys parameter vectors (excluding morphology) of the selected cells, classify each
   cell as "symmetric" or "asymmetric" using a normalised asymmetry score across the four PD
   asymmetry axes, and plot a PC1-vs-PC2 scatter coloured by class. If the two classes separate in
   PC space, the electrophys regime differs between the two morphology classes; if they do not, the
   asymmetry is independent of the electrophys regime.

3. **Which of the 68 parameters drive DSI and PD diversity?** Run factor analysis on the full 68-d
   parameter matrix of the selected cells, project DSI and PD onto the factors via Pearson
   correlation between factor scores and the two outcomes, and report the top-loading factors for
   each outcome. Both electrophys and morphology parameters must be included.

## Key Questions

1. Does the asymmetric-morphology motif (the four PD-asymmetry axes elevated) hold across the
   broader DSI > 0.2 ∧ PD > 3 population, or only at the Pareto extremes?
2. In PCA of the 54-d electrophys vectors, do symmetric and asymmetric cells separate? Or do they
   share the same electrophys-parameter cluster, suggesting that the morphology is the dominant
   discriminator?
3. Which top-3 factors (out of N factors retained by Kaiser criterion or 80% variance) load most
   strongly on DSI? On PD? Do these factor loadings include both electrophys and morphology
   parameters?
4. Is there a single factor that simultaneously loads on DSI AND PD (a "direction-selectivity
   firing-rate trade-off" factor), or are the two outcomes driven by orthogonal factors?

## Approach

### Cell selection

Pool all evaluations from
`tasks/t0102_seedscale_n4_gen20/results/data/all_evaluations_seed{44,55}.json` and
`tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/all_evaluations_seed{44,55}.json`.

Apply the filter: `dsi_vector_sum > 0.2 AND pd_rate_hz > 3.0`.

Dedupe by full 68-d parameter vector (round to 6 decimals) — Pareto preservation across
generations creates many duplicate rows.

Tag each row with `source_task` ∈ {t0102, t0104} and `seed` ∈ {44, 55}.

Report N_selected before and after dedupe.

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

Report the distribution of `asym_score` in the selected population and the count in each class.

### Morphology gallery

For each selected cell (or a stratified subsample of ≤30 cells if N > 30, stratified by asymmetry
class and source task):

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
7. Report a Mann-Whitney U test between symmetric and asymmetric PC1 scores (and PC2) to quantify
   whether the classes separate; report the U statistic, p-value, and a brief interpretation.

Output: `results/images/pca_electrophys_by_morphology_class.png` (3 subplots: by-class, by-DSI,
by-PD).

### Factor analysis on the full 68-d matrix

1. Stack the 68-d parameter vectors into `X_full` shape `(N_selected, 68)`.
2. z-score each column.
3. Run `sklearn.decomposition.FactorAnalysis` with rotation = "varimax" (use the iterative method if
   sklearn lacks varimax built-in; or use `factor_analyzer` package — add to pyproject.toml if
   needed).
4. Choose number of factors by Kaiser criterion (eigenvalues > 1 on the correlation matrix) OR 80%
   of total variance, whichever gives the smaller count, capped at 10 factors.
5. For each factor, list the top-5 loading parameters (by absolute loading magnitude), giving
   parameter name and signed loading.
6. Compute factor scores for each cell (the (N_selected, n_factors) matrix).
7. Compute Pearson r between each factor score column and DSI (and PD). Report the top-3 factors by
   |r| for each outcome.
8. If a single factor has both `|r_DSI| > 0.3 AND |r_PD| > 0.3`, flag it as a joint-DSI-PD factor.

Output: `results/images/factor_loadings.png` (heatmap of factors × parameters) and
`results/images/factor_correlations.png` (bar chart of |r| between each factor and DSI/PD).

### Answer assets

Produce two answer assets:

1. `assets/answer/symmetric-vs-asymmetric-electrophys-cluster/`
   * Question: "Do symmetric and asymmetric DSGC morphologies share the same electrophys parameter
     regime, or do they form distinct clusters in PC space?"
   * Evidence: PCA scatter, Mann-Whitney U test results.

2. `assets/answer/dsi-pd-diversity-factor-decomposition/`
   * Question: "Which factors (combinations of the 68 input parameters) explain DSI diversity versus
     PD diversity, and is there a joint factor or are the two outcomes orthogonal?"
   * Evidence: factor-loading heatmap, top-loading parameters per factor, Pearson correlations
     between factor scores and DSI/PD.

## Why This Matters for the Research Questions

The project's research questions 1-4 ask which combinations of channel and morphological parameters
produce direction selectivity. t0080-t0104 have approached this via multi-objective optimisation;
t0105 now asks a complementary "what works" question on the optimiser's output population.
Specifically:

* If symmetric and asymmetric cells separate in electrophys PC space, then the morphology class
  selects a different channel regime — relevant to RQ4 (active vs passive dendrites) and RQ3
  (synapse density/spatial distribution).
* If DSI and PD are driven by different factors, then the joint corner is empirically unreachable
  because no single parameter axis lifts both — supporting the substrate-limited reading from
  t0102 / t0104.
* If a joint factor exists, then targeted moves along that factor's loading direction may unlock the
  joint corner — a direct lead for an experimental follow-up task.

## Step by Step

Canonical step IDs:

1. `preflight` — verify both dependency tasks are completed.
2. `research-code` — review t0102 / t0104 evaluation file formats, morphology generator interface,
   sklearn / factor_analyzer availability in pyproject.toml.
3. `planning` — produce `plan/plan.md` with REQ-1..REQ-N including cell counts after filtering,
   gallery-subsample policy, factor-analysis algorithm choice, and asymmetry-threshold sensitivity
   plan.
4. `implementation` —
   * 4a. Load and filter cells (`code/load_filter_cells.py`).
   * 4b. Compute asymmetry classification (`code/classify_asymmetry.py`).
   * 4c. Build morphology gallery (`code/build_gallery.py` extending the working scratch script).
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

None. Local-only analysis on the local machine. Existing project Python environment plus possibly
`factor_analyzer` package (small addition to `pyproject.toml` if used).

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

* **Risk**: filtered cell count is small (e.g. N < 20). **Fallback**: relax filter to
  `DSI > 0.1 AND PD > 2`; document the relaxation in results_detailed.md. If still < 10, the
  analysis runs on the small N with caveats.
* **Risk**: PCA on 54 dims with N ~ 30-100 may be unstable. **Fallback**: report bootstrapped
  variance-explained intervals and constrain interpretation to PC1-PC2 only.
* **Risk**: `factor_analyzer` not in current pyproject.toml. **Fallback**: use
  `sklearn.decomposition.FactorAnalysis` (no varimax built-in) and manually apply varimax via a
  small rotation routine, or fall back to PCA-only interpretation.
* **Risk**: asymmetry threshold of 0.5 produces unbalanced classes (e.g. 95% asymmetric, 5%
  symmetric). **Fallback**: sweep thresholds at 0.3 / 0.5 / 1.0 and report all three; pick the
  middle for the headline plots and note class balance.
* **Risk**: t0102 cells with DSI > 0.2 are dominated by silenced-cell artifacts that escaped t0104's
  guard. **Fallback**: explicitly check the artifact pattern (DSI > 0.95 AND PD < 5) and exclude
  such cells from t0102 if they appear; document the exclusion count.

## Verification Criteria

* `verify_task_metrics t0105_cluster_factor_analysis_dsi_pd` passes with 0 errors.
* `verify_task_results t0105_cluster_factor_analysis_dsi_pd` passes with 0 errors.
* Both answer assets validate against `verify_answer_asset`.
* All charts in `results/images/` are PNG, embedded in `results_detailed.md` via
  `![desc](images/file.png)`.
* The morphology gallery is reproducible: includes the random seed for any stratified subsampling.
* The PCA and factor-analysis numbers in `results_detailed.md` exactly match values in
  `metrics.json`.

## Task Requirement Checklist (initial — `plan/plan.md` will finalise the REQ list)

* REQ-1: Pool t0102 + t0104 evaluations, apply filter `DSI > 0.2 AND PD > 3 Hz`, dedupe by 68-d
  vector. Record N_before_filter, N_after_filter, N_after_dedupe.
* REQ-2: Compute normalised asymmetry score for each selected cell; classify symmetric/asymmetric at
  threshold 0.5; report class counts.
* REQ-3: Build morphology gallery for selected cells (or stratified subsample of ≤30). Annotate
  DSI, PD, asym_score, source_task per panel.
* REQ-4: PCA on 54-d electrophys vectors; plot PC1-PC2 by class, by DSI, by PD; report variance
  explained and top loadings.
* REQ-5: Mann-Whitney U test between symmetric and asymmetric PC1 (and PC2); report U, p-value,
  interpretation.
* REQ-6: Factor analysis on 68-d full vectors; choose factor count by Kaiser or 80% variance; report
  loadings.
* REQ-7: Pearson r between factor scores and DSI/PD; identify top-3 factors per outcome; flag any
  joint factor.
* REQ-8: Two answer assets validated by `verify_answer_asset`.

## Out of Scope

* Re-running NSGA-II or any optimisation (this is pure analysis on existing data).
* Building any morphology beyond what is needed for the gallery plot.
* In silico patch-clamp / IV-curve analysis on the breakthrough cells (deferred to a separate task;
  goes well with S-0104-01 / S-0104-02).
* Comparing against external DSGC datasets (Bae 2018, Ran 2020) — deferred to S-0103-* lineage.
