---
spec_version: "1"
task_id: "t0088_recluster_marginals_and_vm_motifs"
research_stage: "code"
tasks_reviewed: 7
tasks_cited: 7
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-05-06"
status: "complete"
---
# Research Code: Re-cluster t0086 13 Cells and Per-cluster Vm-trace Deep-dive

## Task Objective

Identify and characterise existing project code that this task should re-use, and confirm the data
sources for the 13-cell parameter pool. The task extends t0086's clustering to include Marginal
cells (13 cells: 6 Genuine + 7 Marginal) and re-uses t0084's Vm-trace deep-dive recording pattern at
higher angular resolution (16 directions instead of 8). Phase A produces re-cluster centroids and
biological-plausibility scorecard; Phase B runs per-cluster Vm-trace deep-dive on representative
cells; Phase C produces a mechanism-distinctness answer asset. Source suggestion: S-0086-03
(extension scope).

## Library Landscape

A single library is relevant: **`de_rosenroll_2026_dsgc_ais_dendritic_spike`** (registered under
[t0080]). Provides the 54-d v3 substrate, the canonical per-cell evaluator
(`apply_parameter_vector`), the parameter-vector dataclass `ParameterVector`, the `ParamIndex` enum,
the synapse setup helpers (`setup_synapses_parametric`, `_bar_arrival_times`,
`_rates_with_ar2_noise`, `_rates_to_events`, `_gaba_prob_for_direction`), the cell builder
(`build_dsgc_cell_with_ais`, `DSGCCellWithAIS`), and the v3 substrate constants (`ANGLES_8DIR_DEG`,
`AP_THRESHOLD_MV`, `CELSIUS_DEG_C`, `DT_MS`, `STEPS_PER_MS`, `TSTOP_MS`, `V_INIT_MV`, `SEED_BASE`,
`LOWER_BOUNDS`, `UPPER_BOUNDS`, `N_PARAMS=54`). All re-uses are unchanged.

## Architecture Overview

The task is structured as three sequential phases sharing the same Python code package
(`tasks.t0088_recluster_marginals_and_vm_motifs.code`). Phase A is pure data analysis (clustering +
biological scoring); Phase B drives NEURON simulations on local CPU for representative cells; Phase
C synthesises the deep-dive output into a single mechanism-distinctness verdict and writes the
answer asset. The Phase A artefact (`representative_cells.json`) is the bridge between Phase A and
Phase B; the Phase B artefacts (per-(cell, direction) `.npz` traces and per-cell attribution JSONs)
feed Phase C.

t0086 (`robustness_cluster_bio_comparison`) produced six pieces of re-usable infrastructure:

* `code/cluster_analysis.py` (359 LOC) -- KMeans k=2..6 + hierarchical (cosine + euclidean) +
  bootstrap ARI + per-cluster centroids; reads from a SELECTED_CELLS_JSON + cell_classification
  schema and outputs `clustering_results.json` and `cluster_centroids.json`.
* `code/biological_priors.py` (179 LOC) -- 9 published biological priors database with
  `BiologicalPrior` dataclass schema (parameter_name, param_index, published_mean, published_sigma,
  paper_id, citation, units, description); writes `biological_priors.json`.
* `code/biological_scorecard.py` (201 LOC) -- per-cluster, per-prior deviation scoring with
  plausible/stretched/exotic verdicts and worst-case aggregate; writes `biological_scorecard.json`
  and `biological_plausibility_heatmap.png`.
* `code/paths.py` (59 LOC) -- task-local path constants.
* `code/plot_phase_b.py` (204 LOC) -- per-cluster scatter + UMAP / PCA + dendrogram + silhouette
  plots.
* `code/classify_cells.py` (145 LOC) -- Genuine/Marginal/Stochastic classifier (already applied to
  produce `cell_classification.json` -- this task starts from that output).

t0084 (`t0081_cell_767_vm_trace_deepdive`) produced three pieces of re-usable infrastructure:

* `code/run_deepdive.py` (439 LOC) -- per-direction NEURON simulation with attached recording
  vectors for: per-segment Vm at proximal soma, mid-dendrite, distal-dendrite, AIS; per-synapse NMDA
  conductance trajectories; per-segment Nav1.6 (`nav16t80._ref_i`) and NaP (`napt80._ref_i`)
  currents at distal dendrite; section-area scaling for unit conversion. Saves one .npz per (cell,
  direction). Designed for 3 cells x 8 directions; this task extends to N representative cells x 16
  directions.
* `code/attribution_metric.py` (155 LOC) -- fractional channel contribution computation: PD-minus-ND
  integrated current difference over response window [200, 1200] ms, fraction NMDA / Nav1.6 / NaP,
  dominant mechanism string. Reads PD direction (0 deg) and ND direction (180 deg) from .npz files;
  writes one `cell{id}_attribution.json` per cell.
* `code/plot_figures.py` (230 LOC) -- four standard figures per cell: per-direction Vm traces grid
  (proximal soma / mid dendrite / distal dendrite per direction), NMDA conductance trajectories,
  Nav1.6 / NaP current decomposition, AIS spike onsets.

## Reusable Code and Assets

* **t0086 cluster_analysis.py** -- KMeans + hierarchical + bootstrap ARI core; copy with input
  loader replaced.
* **t0086 biological_priors.py** -- 9-prior database; copy unchanged.
* **t0086 biological_scorecard.py** -- per-cluster scoring; copy unchanged.
* **t0086 cell_classification.json** -- the source of the 6 Genuine + 7 Marginal labels.
* **t0083 all_evaluations.json** -- the source of all 13 cells' 54-d parameter vectors.
* **t0084 run_deepdive.py** -- per-direction NEURON sim with attached recording vectors; copy with
  angle list and cell-list source modified.
* **t0084 attribution_metric.py** -- PD-minus-ND fractional attribution; copy unchanged.
* **t0084 plot_figures.py** -- 4 standard figures per cell; copy with column / bin counts updated.
* **t0080 de_rosenroll_2026_dsgc_ais_dendritic_spike library** -- the v3 substrate (cell builder,
  parameter-vector helpers, synapse setup, constants).

## Methodology Review

### Cell parameter loading

Verified empirically that all 13 target cells (767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634,
1639, 1663, 1677, 1721) have their 54-d natural-unit parameter vectors in
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json`. None require
fall-back loading from t0081's `all_evaluations.json`. The schema per record is the same as t0081:
each record has `cell_index`, `generation`, `dsi`, `pd_rate_hz`, and `params` (54-d list).

### Re-clustering

t0086's `cluster_analysis.py` operates on a SELECTED_CELLS_JSON + cell_classification schema that
filters to Genuine cells only at the start. For this task the input differs:

* Input is the 13 cells (6 Genuine + 7 Marginal) already enumerated from t0086's
  `cell_classification.json`.
* Parameter vectors come from t0083's `all_evaluations.json`.
* All other steps (KMeans 2..6, hierarchical with cosine + euclidean, bootstrap ARI, centroids in
  normalised + unnormalised space) are unchanged.

So this task copies `cluster_analysis.py` into its own `code/` directory and replaces the input
loading with a 13-cell loader from t0083's `all_evaluations.json`. The clustering core logic (k
selection, bootstrap ARI, centroid math) is preserved verbatim.

### Biological scoring

`biological_priors.py` and `biological_scorecard.py` are re-used unchanged; they operate on the
unnormalised cluster centroids in the t0080 54-d parameter space, which is the same parameter space
in this task. Copy both files into `code/` with import path updates from
`tasks.t0086_robustness_cluster_bio_comparison.code.paths` to
`tasks.t0088_recluster_marginals_and_vm_motifs.code.paths`.

### Per-cluster deep-dive

`run_deepdive.py` records per-direction Vm + NMDA + Nav1.6 + NaP traces. The original is hard-coded
to 8 directions (`ANGLES_8DIR_DEG` from t0080 constants) and 3 specific cells (767, 637, 762). For
this task:

* Replace `ANGLES_8DIR_DEG` (0, 45, 90, 135, 180, 225, 270, 315 deg) with a 16-direction list at
  22.5 deg spacing (0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5,
  315, 337.5 deg).
* Replace the hard-coded cell list with a representative-per-cluster list determined at runtime
  after Phase A (the cell minimising 54-d Euclidean distance to its cluster centroid).
* Replace the load source from t0081's `all_evaluations.json` to t0083's.
* Save one .npz per (representative_cell, direction).
* Phase A representative selection runs separately from Phase B simulations; the simulation script
  reads the representative list from a Phase A artefact.

The PD/ND attribution still uses 0 deg and 180 deg; `RESPONSE_WINDOW_START_MS` and
`RESPONSE_WINDOW_END_MS` (200 / 1200 ms) are unchanged. Per-direction current integrals are computed
for all 16 directions to enable a polar attribution sweep figure.

### Plotting

t0084's `plot_figures.py` produces 4 standard figures at 8 directions:

1. Per-direction Vm traces (3-row x 8-column grid).
2. NMDA conductance trajectories (8-line plot).
3. Nav1.6 / NaP current decomposition (8-direction subplots).
4. AIS spike onset histogram (8-bin polar or bar).

The same 4 figures will be produced at 16 directions per representative cell. Modify column counts
from 8 to 16 in subplot grids; modify polar bin counts from 8 to 16.

## Key Findings

### Data sources are clean and complete

All 13 target cell parameter vectors live in
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json`. None of the 13 cells
require fallback loading from t0081's `all_evaluations.json`, even though cell 767 was originally
warm-started from t0081 -- its parameter vector was re-recorded by t0083 with the same `cell_index`.
The cell_classification.json from t0086 cleanly labels each of the 20 originally-evaluated cells as
Genuine, Marginal, or Stochastic; the 13-cell pool is
`[767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1721]` and includes only
the Genuine + Marginal subset (drops the 7 Stochastic). This simplifies the implementation: a single
13-cell loader from t0083 covers all parameter vectors, and a single classification filter from
t0086 covers the 13-cell selection.

### t0086's clustering core is directly portable

The `cluster_analysis.py` module's KMeans (k=2..6 with random_state=42, n_init="auto"), hierarchical
clustering (cosine + euclidean, average linkage), bootstrap ARI (50 samples, 80 percent subsample
rate), and centroid math all operate on a normalised parameter matrix that is morphology- and
classification-agnostic. Only the input schema changes for this task. The output schema
(clustering_results.json + cluster_centroids.json) is identical so downstream consumers
(biological_scorecard, plotting) work unchanged.

### t0086's biological scoring is fully re-usable

Both `biological_priors.py` and `biological_scorecard.py` operate on the unnormalised cluster
centroids in the t0080 54-d parameter space. Since this task's clustering produces centroids in the
same space, the priors database and scoring math run unmodified. The only change required is the
import path: `tasks.t0086_robustness_cluster_bio_comparison.code.paths` becomes
`tasks.t0088_recluster_marginals_and_vm_motifs.code.paths`. The 9 priors (Kole 2008, Werginz 2024,
Sivyer 2013, Branco-Hausser 2010, Oesch 2005, Stuart 1999 / Goldfinger 2000, de Rosenroll 2026
rho0_gaba and lambda_gaba_um, plus the derived AIS-to-soma Nav ratio from Werginz) are unchanged.

### t0084's deep-dive recording pattern needs two surface modifications

`run_deepdive.py` records per-direction Vm + NMDA + Nav1.6 + NaP traces via NEURON Vector.record()
handles attached before h.run(). The original is hard-coded to 8 directions
(`ANGLES_8DIR_DEG = (0, 45, 90, 135, 180, 225, 270, 315)`) and 3 specific cells (767, 637, 762). For
this task: (a) replace the angle list with a 16-direction list at 22.5 deg spacing, including 0 and
180 deg so the existing PD/ND attribution at those directions still works; (b) make the cell list
data-driven, reading from a Phase A artefact (`representative_cells.json`) so Phase B picks up the
post-clustering representatives. The recording infrastructure (per-segment Vm, per-synapse NMDA g,
per-segment Nav1.6 / NaP currents, AIS Vm, section-area scaling for nA conversion) is preserved.

### Attribution metric is unmodified

`attribution_metric.py` computes the PD-minus-ND integrated current difference over the response
window [200, 1200] ms. Since both PD (0 deg) and ND (180 deg) are present in the 16-direction list,
the attribution math runs unchanged. Per-direction integrals can additionally be computed for all 16
directions to enable a polar attribution sweep figure for richer mechanism-distinctness
visualisation.

## Recommended Approach

1. **Copy** the following files into `tasks/t0088_recluster_marginals_and_vm_motifs/code/` with
   import-path rebinding from `tasks.t0086_robustness_cluster_bio_comparison.code.paths` /
   `tasks.t0084_t0081_cell_767_vm_trace_deepdive.code.{paths,constants}` to
   `tasks.t0088_recluster_marginals_and_vm_motifs.code.{paths,constants}`:

   * `biological_priors.py` (from t0086)
   * `biological_scorecard.py` (from t0086)
   * `cluster_analysis.py` (from t0086, with a new loader for the 13-cell input)
   * `run_deepdive.py` (from t0084, with 16-direction angle list and runtime-determined cell list)
   * `attribution_metric.py` (from t0084, unchanged except path imports)
   * `plot_figures.py` (from t0084, with column / bin counts updated to 16)

2. **Add new files**:

   * `paths.py` with the t0088 task-local path constants (data, images, answer asset folder).
   * `constants.py` with `ANGLES_16DIR_DEG` and the 13 target cell IDs.
   * `select_representatives.py` for Phase A: load cell_classification.json, load t0083
     all_evaluations.json, build the 54-d parameter matrix for the 13 cells, run clustering, pick
     representative per cluster, write `representative_cells.json`.
   * `mechanism_distinctness.py` for Phase C: load all attributions, compute pairwise comparison and
     dominant-mechanism table, write `mechanism_distinctness.json`.
   * `write_answer_asset.py` for Phase C: produce the
     `assets/answer/are-cluster-motifs-mechanistically-distinct/` answer asset.

3. **Run order**:

   1. `biological_priors.py` -> writes `biological_priors.json`.
   2. `select_representatives.py` -> reads cell_classification.json + t0083 all_evaluations.json,
      runs clustering, writes `recluster_assignments.json`, `recluster_centroids.json`,
      `representative_cells.json`.
   3. `biological_scorecard.py` -> reads centroids + priors, writes
      `recluster_biological_scorecard.json` + heatmap PNG.
   4. `run_deepdive.py` -> reads representative_cells.json + t0083 all_evaluations.json, runs NEURON
      sims, writes per-(cell, direction) .npz files.
   5. `attribution_metric.py` -> reads .npz, writes per-cell attribution JSONs.
   6. `plot_figures.py` -> writes 4 PNGs per representative cell.
   7. `mechanism_distinctness.py` -> writes `mechanism_distinctness.json`.
   8. `write_answer_asset.py` -> writes the answer asset.

## Lessons Learned

* **Cross-task code re-use without library extraction is feasible** when the source task's code is
  modular (clear input/output JSONs, no implicit globals beyond t0080's `ParamIndex` /
  `LOWER_BOUNDS` / `UPPER_BOUNDS`). t0086's biological scoring meets this bar; copying with import
  rebinding is straightforward.
* **Hard-coded constants (angle lists, cell lists) trade simplicity for re-usability**. t0084's
  `ANGLES_8DIR_DEG` is imported from t0080's constants module; replacing it cleanly requires a new
  task-local constant (`ANGLES_16DIR_DEG`) rather than modifying the import.
* **Parameter-vector hashing for deterministic seed offsets** (t0084's `_hash_param_vector`) is
  important: re-running the same cell at the same direction must produce the same synapse placement
  and event times. This is preserved verbatim.
* **t0086's clustering input schema constraints to "Genuine cells only" via a hard-coded filter
  inside `cluster_analysis.py`** is brittle. For this task we accept the brittleness and replace the
  filter with a Genuine-or-Marginal filter, but a future refactor could move the filter to a
  caller-supplied predicate.

## Recommendations for This Task

### Code structure

* `paths.py` (new) -- task-local path constants for all input / output files.
* `constants.py` (new) -- `ANGLES_16DIR_DEG`, `TARGET_CELL_IDS` (the 13-cell list), response-window
  constants copied from t0084.
* `select_representatives.py` (new) -- Phase A driver: load cell_classification.json, load t0083
  all_evaluations.json, build the 54-d parameter matrix for the 13 cells, run clustering (re-using
  cluster_analysis core), pick the per-cluster representative cell minimising 54-d Euclidean
  distance to the centroid. Outputs: `recluster_assignments.json`, `recluster_centroids.json`,
  `representative_cells.json`.
* `cluster_analysis.py` (copied from t0086, with input loader replaced).
* `biological_priors.py` (copied from t0086, with import path rebinding).
* `biological_scorecard.py` (copied from t0086, with import path rebinding).
* `run_deepdive.py` (copied from t0084, with `ANGLES_8DIR_DEG` -> `ANGLES_16DIR_DEG`, hard-coded
  cell list -> read from `representative_cells.json`, t0081 -> t0083 path source).
* `attribution_metric.py` (copied from t0084, with task-local path imports).
* `plot_figures.py` (copied from t0084, with subplot grid columns 8 -> 16).
* `mechanism_distinctness.py` (new) -- Phase C driver: compare attributions across clusters, produce
  dominant-mechanism table, write `mechanism_distinctness.json`.
* `write_answer_asset.py` (new) -- Phase C: produce the
  `assets/answer/are-cluster-motifs-mechanistically-distinct/` answer asset (details.json,
  short_answer.md, full_answer.md per the answer-asset spec).

### Run order

1. `biological_priors.py` -> `biological_priors.json`.
2. `select_representatives.py` -> `recluster_assignments.json`, `recluster_centroids.json`,
   `representative_cells.json`.
3. `biological_scorecard.py` -> `recluster_biological_scorecard.json` + heatmap PNG.
4. `run_deepdive.py` -> per-(cell, direction) `.npz` files for representative cells x 16 dirs.
5. `attribution_metric.py` -> per-cell `cell{id}_attribution.json`.
6. `plot_figures.py` -> 4 PNGs per representative cell.
7. `mechanism_distinctness.py` -> `mechanism_distinctness.json`.
8. `write_answer_asset.py` -> answer asset.

### Library asset

The `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset (registered under t0080) is the only
external import needed. It provides `DSGCCellWithAIS`, `build_dsgc_cell_with_ais`,
`apply_parameter_vector`, `ParameterVector`, `ParamIndex`, the canonical synapse setup helpers
(`setup_synapses_parametric`, `_bar_arrival_times`, etc.), and the v3 substrate constants
(`ANGLES_8DIR_DEG`, `AP_THRESHOLD_MV`, `CELSIUS_DEG_C`, `DT_MS`, `STEPS_PER_MS`, `TSTOP_MS`,
`V_INIT_MV`, `SEED_BASE`, `LOWER_BOUNDS`, `UPPER_BOUNDS`, `N_PARAMS=54`). All re-uses are unchanged.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC compartmental model to NEURON
* **Status**: completed
* **Relevance**: Provides the de Rosenroll 2026 base substrate; informs the GABA / AMPA spatial
  distribution biological prior used in Phase A scoring.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B v2 MOBO with AIS tiered AHP (49-d substrate)
* **Status**: completed
* **Relevance**: Parent substrate of t0080 v3; informs the AIS-Nav biological prior used in Phase A
  scoring.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic spike (54-d substrate, NSGA-II)
* **Status**: completed
* **Relevance**: Provides the v3 substrate library (cell builder, parameter vector helpers, synapse
  setup, constants `LOWER_BOUNDS` / `UPPER_BOUNDS` / `N_PARAMS=54`, `ParamIndex` enum). All re-uses
  are unchanged.

### [t0081]

* **Task ID**: `t0081_bedb_v3_warmstart_nsga2`
* **Name**: Bed B v3 NSGA-II warm-start from t0078 Pareto cells
* **Status**: completed
* **Relevance**: Originally housed cell 767's parameter vector via warm-start; t0083 re-recorded the
  same `cell_index` so this task's loader uses t0083 exclusively. Listed for completeness.

### [t0083]

* **Task ID**: `t0083_bedb_v3_extend_nsga2_gen8plus`
* **Name**: Extend t0081 NSGA-II from gen-7 with adaptive HV-plateau stop
* **Status**: completed
* **Relevance**: `results/data/all_evaluations.json` is the source of all 13 cells' 54-d parameter
  vectors (verified empirically that all of
  `[767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1721]` are present).

### [t0084]

* **Task ID**: `t0084_t0081_cell_767_vm_trace_deepdive`
* **Name**: Vm-trace deep-dive of t0081 cell 767 to attribute the joint-pass DSI mechanism
* **Status**: completed
* **Relevance**: Provides `code/run_deepdive.py` (per-direction NEURON sim with per-segment Vm,
  per-synapse NMDA conductance, per-segment Nav1.6 / NaP currents, AIS Vm, section-area scaling),
  `code/attribution_metric.py` (PD-minus-ND fractional channel contribution), `code/plot_figures.py`
  (4 standard figures), and `code/constants.py` (RECORD_DT_MS, response window, NMDA Erev). Copy
  with surface modifications: angle list 8 -> 16, cell list runtime-driven.

### [t0086]

* **Task ID**: `t0086_robustness_cluster_bio_comparison`
* **Name**: Robustness + cluster + bio-comparison of t0081/t0083 joint-pass cells
* **Status**: completed
* **Relevance**: Provides `code/cluster_analysis.py` (KMeans + hierarchical + bootstrap ARI core),
  `code/biological_priors.py` (9 priors database), `code/biological_scorecard.py` (per-cluster
  scoring), and `results/data/cell_classification.json` (Genuine + Marginal + Stochastic
  classification). Copy clustering core with input loader replaced; copy scoring code unchanged.

## References

* `tasks/t0086_robustness_cluster_bio_comparison/code/cluster_analysis.py`
* `tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py`
* `tasks/t0086_robustness_cluster_bio_comparison/code/biological_scorecard.py`
* `tasks/t0086_robustness_cluster_bio_comparison/code/paths.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/run_deepdive.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/attribution_metric.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/plot_figures.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/constants.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/paths.py`
* `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py` (LOWER_BOUNDS, UPPER_BOUNDS,
  N_PARAMS=54, ParamIndex)
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` (data source for all
  13 cell parameter vectors)
* `tasks/t0086_robustness_cluster_bio_comparison/results/data/cell_classification.json` (data source
  for Genuine + Marginal classification)
