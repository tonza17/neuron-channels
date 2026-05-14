---
spec_version: "1"
task_id: "t0105_cluster_factor_analysis_dsi_pd"
research_stage: "code"
tasks_reviewed: 7
tasks_cited: 6
libraries_found: 2
libraries_relevant: 1
date_completed: "2026-05-14"
status: "complete"
---
# Research Code: Cluster + Factor Analysis Across 68-d Optimisations

## Task Objective

Pool cells from t0091, t0099, t0102, t0104 (all four 68-d electrophys+morphology NSGA-II lineages)
with `DSI > 0.1 AND PD > 2 Hz`, dedupe by 68-d vector, classify by morphological asymmetry, then run
PCA on the 54-d electrophys submatrix and factor analysis on the full 68-d matrix to identify which
factors explain DSI and PD diversity. Produces 2 answer assets, a morphology gallery, and a PCA
scatter + factor-loading heatmap.

## Library Landscape

Project libraries aggregator surfaces two relevant libraries:

* `de_rosenroll_2026_dsgc` (from t0024 with corrections from later tasks) — the Bed B DSGC
  compartmental model. **Not directly relevant** to t0105 because t0105 does no compartmental
  simulation; the existing predictions data fully encodes the simulation output. Only the
  morphology-parameter bound definitions are reused indirectly via t0090's `MorphologyParams` schema
  (no simulation calls).

* No `factor_analyzer` or `scikit-learn` library is registered as a project library (these are
  upstream pip deps configured in `pyproject.toml`). Confirmed present at runtime:
  `scikit-learn>=1.8.0` and `scipy>=1.17.1`. **`factor_analyzer` is NOT installed** — adding it to
  `pyproject.toml` is part of REQ-2 in the plan.

## Key Findings

### Evaluation file structure across all four 68-d lineages

All four tasks store per-cell evaluations under `tasks/{task_id}/results/data/all_evaluations*.json`
with the same row schema:

* `generation` (int)
* `vector_68d` (list[float], length 68 — 54 electrophys followed by 14 morphology dims)
* `objective_F_minimised` (list[float], length 2 or 3)
* `dsi_vector_sum` (float)
* `pd_rate_hz` (float)
* `robustness` (float — present in t0091, t0099, t0102; **absent in t0104** because the 2-obj run
  dropped the field)

t0091's file is a single `all_evaluations.json` (no per-seed split). t0099 / t0102 / t0104 split by
GA seed (`all_evaluations_seed{11,22,33,44,55}.json`). All files wrap rows in
`{"evaluations": [...]}`. Citations: [t0091], [t0099], [t0102], [t0104].

Pre-scope inventory (`scratch_count_68d_cells.py`):
* Total 68-d cells: **7,003** across all 4 lineages (187 + 2,016 + 2,592 + 2,208).
* At primary filter `DSI > 0.1 AND PD > 2`: 268 passing rows → **86 unique 68-d vectors**.
* At strict filter `DSI > 0.2 AND PD > 3`: 95 passing rows → 31 unique vectors.

The 54-d-only lineage (`t0080`, `t0081`, `t0083`) is excluded because those runs fixed morphology
and varied only electrophys (54-d vector). Citations: [t0080], [t0083].

### Morphology generator interface

Procedurally building a NEURON dendritic tree from a 14-d morphology parameter vector uses
`tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`:

```python
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)

result = generate_fixed_morphology(params=MorphologyParams.from_dict(data=morph_dict))
# result has fields: h (neuron h object), soma, all_dends, primary_dends, terminal_dends,
# terminal_locs_xy, ...
```

The 14 morphology dim names are documented at
`tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants_morphology.py:18-33` — the same schema is
used by all four lineages. Three of the 14 dims are integers (`num_primary_branches`,
`max_strahler_depth`, `morph_seed`) and must be rounded before constructing
`MorphologyParams.from_dict`. Citations: [t0090], [t0092].

To plot the morphology, iterate `result.soma + result.all_dends` and call NEURON's `h.x3d(i)`,
`h.y3d(i)`, `h.diam3d(i)` while the section is pushed on the access stack. The working prototype is
`scratch_t0102_t0104_morph_compare.py` on main (commit `e600e3f0`); it builds 10 cells and renders a
2×5 grid in ~30 s.

### Asymmetry-classification convention

The four PD-asymmetry dims (5: soma_offset_pd_um, 6: field_elongation_pd, 7:
branch_density_gradient_pd, 8: primary_branch_pd_concentration) drive whether the dendritic tree is
polarised toward the preferred direction. The normalised asymmetry score formula in t0104's
intervention file `early_stop_after_seed_55.md` (and used in the scratch decoder) sums normalised
magnitudes:

```
asym_score = abs(soma_offset_pd_um) / 150
           + abs(field_elongation_pd - 1.0) / 2.0
           + abs(branch_density_gradient_pd) / 1.0
           + abs(primary_branch_pd_concentration) / 5.0
```

Range 0..4. Threshold ≥ 0.5 = asymmetric. Citations: [t0104].

### Silenced-cell artifact handling

t0102's pre-guard data contains 27 cells with `DSI ~= 1.0 AND PD < 5 Hz` that are vector-sum
divide-by-near-zero artifacts. t0104 fixed this with the S-0102-01 silence guard. **t0091, t0099,
t0102 evaluations may contain the same artifact pattern.** For t0105 the conservative move is to
exclude cells matching `DSI > 0.95 AND PD < 5 Hz` from t0091/t0099/t0102. Citation: [t0102].

### Existing PCA / factor analysis precedent in the project

No prior task in this project has run PCA on optimisation outputs. t0090 (`morphometric_pca.py`)
computed PCA / UMAP on six morphometric summary features for diversity testing (not on the parameter
vectors). t0086 (`cluster_analysis.py`) ran k-means + silhouette
+ ARI on a 54-d Pareto library; that pattern is the closest precedent. The t0086 approach used
  `sklearn.cluster.KMeans` and `sklearn.metrics.silhouette_score` — both still available in
  sklearn 1.8.0. Citations: [t0090], [t0086].

## Reusable Code and Assets

### From t0092 — morphology generator (copy into task)

* **Source**: `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`
  (~80 lines including imports). Plus its dependency
  `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` (~150 lines).
* **What it does**: builds a NEURON Cell from a 14-d morphology vector and returns soma / dendrite
  Section objects.
* **Reuse method**: **import via library** — t0092's generator is exported as part of the
  `de_rosenroll_2026_dsgc` library (per t0093 / t0090 correction patches). Confirmed by import in
  `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/generator_wrapper.py:25-30`. t0105 can import
  directly:
  ```python
  from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
      generate_fixed_morphology,
  )
  from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
      MorphologyParams,
  )
  ```
* **Adaptation needed**: none — the prototype scratch script already exercises this import path
  successfully on main.

### From the t0104 scratch script — gallery layout (copy into task)

* **Source**: `scratch_t0102_t0104_morph_compare.py` on main (~210 lines).
* **What it does**: loads evaluations, top-N by `DSI × PD`, builds morphologies, plots a grid.
* **Reuse method**: **copy into task** as `code/build_gallery.py` and adapt for stratified
  subsampling (by class × source_task) instead of top-N-per-optimisation. Add asym_score annotation
  per panel.
* **Adaptation needed**: stratified subsampling logic (≤30 cells), per-panel asym_score
  annotation, support for all 4 lineages.

### From sklearn / scipy (pip-installed)

* `sklearn.decomposition.PCA` — fit on the standardised 54-d electrophys submatrix.
* `sklearn.decomposition.FactorAnalysis` — fit on the standardised 68-d matrix; lacks varimax
  built-in (rotation parameter not supported in sklearn 1.8.0 for `FactorAnalysis`).
* `scipy.stats.mannwhitneyu` — symmetric vs asymmetric PC1/PC2 separation.
* `scipy.stats.pearsonr` — factor scores vs DSI / PD.

### Varimax via factor_analyzer (add to pyproject.toml)

* **Add**: `factor_analyzer>=0.5.1` to `pyproject.toml` (small pure-Python package, ~2 MB).
* **Why**: provides `FactorAnalyzer(rotation="varimax")` out of the box; cleaner than manually
  implementing varimax rotation. Alternative is a manual ~30-line varimax routine using
  `numpy.linalg.svd`. Plan REQ-3 will choose between these based on whether the package can be
  installed cleanly.

## Lessons Learned

* t0086's cluster analysis used N=128 cells on 54 dims — comparable scale to t0105 (86 cells on 68
  dims). t0086 found that PC1-PC2 captured ~45% of variance; further PCs were noisy. Expect similar
  at t0105.
* t0104's silence guard (S-0102-01) is the most important guard against artifact pollution; the
  t0105 implementation must apply the same guard pattern when ingesting pre-guard data from
  t0091/t0099/t0102. Citation: [t0102].
* Cross-lineage heterogeneity (warm-start vs random-init; 2-obj vs 3-obj; N_EVAL 4 vs 20) means PCA
  loadings may reflect lineage origin as much as DSI/PD trade-off. The PCA scatter should
  additionally colour-code by source_task to inspect lineage clustering.

## Recommendations for This Task

1. Add `factor_analyzer` to `pyproject.toml` (single-line edit) before implementing.
2. Reuse the scratch gallery script's morphology-build path verbatim; adapt the cell-selection logic
   for stratified sampling.
3. Apply silence guard (`DSI = 0` when total spike count < 10 — or as fallback exclude
   `DSI > 0.95 AND PD < 5`) consistently across all four lineages.
4. Cap factor count at min(Kaiser eigenvalues > 1, 80% variance, 10) and report bootstrap CIs on
   loadings.
5. For each chart, save at 150-180 DPI; embed in `results_detailed.md` with descriptive caption.

## Task Index

* [t0080] — `t0080_bedb_mobo_v3_dendritic_spike_nsga2` — 54-d electrophys-only NSGA-II,
  excluded.
* [t0086] — `t0086_robustness_cluster_bio_comparison` — closest cluster-analysis precedent in
  the project (k-means + silhouette on 54-d Pareto library).
* [t0090] — `t0090_morphology_generator_diversity_test` — provides `MorphologyParams` schema and
  the morphology generator's reference test harness.
* [t0091] — `t0091_morphology_extended_nsga2_v1` — warm-start 68-d NSGA-II; one of t0105's
  pooled lineages.
* [t0092] — `t0092_diagnose_morphology_generator_silence` — fixes the soma-area bug;
  `generate_fixed_morphology` is t0105's morphology entry point.
* [t0099] — `t0099_random_init_pareto_robustness` — random-init 68-d at N_EVAL=20; pooled
  lineage.
* [t0102] — `t0102_seedscale_n4_gen20` — random-init 68-d at N_EVAL=4 with robustness; pooled
  lineage. Contains silenced-cell artifacts.
* [t0104] — `t0104_nsga2_2obj_dsi_pdrate_3seeds` — random-init 68-d without robustness, with
  silence guard; pooled lineage.
