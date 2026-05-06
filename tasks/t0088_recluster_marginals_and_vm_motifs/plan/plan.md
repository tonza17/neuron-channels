---
spec_version: "2"
task_id: "t0088_recluster_marginals_and_vm_motifs"
date_completed: "2026-05-06"
status: "complete"
---
# Plan: Re-cluster t0086 13 Cells and Per-cluster Vm-trace Deep-dive

## Objective

Run three sequential phases on top of t0086's robustness-classified 20-cell set: Phase A re-clusters
the 13-cell pool of 6 Genuine + 7 Marginal cells in the t0080 54-d v3 parameter space using KMeans
k=2..6 (silhouette + BIC) + hierarchical (cosine + euclidean) + UMAP / PCA visualisation, computes
per-cluster centroids, and scores against the t0086 biological priors database (Kole 2008, Werginz
2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005, Goldfinger 2000, Stuart 1999, de Rosenroll
2026); Phase B picks one representative cell per cluster (closest to centroid in 54-d Euclidean
distance) and runs a t0084-style Vm-trace deep-dive at **16 directions** (every 22.5 deg), recording
per-segment Vm at proximal soma / mid dendrite / distal dendrite / AIS, per-synapse NMDA
conductance, per-segment Nav1.6 / NaP currents at the distal dendrite, and AIS spike onsets; Phase C
computes fractional channel attribution per representative cell and synthesises a
mechanism-distinctness verdict comparing the per-cluster attributions, producing one answer asset.

**Done** when: the re-cluster assignments + centroids + biological scorecard exist; per-cluster
representative Vm-trace deep-dive data + attribution + 4 figures per representative exist; the
mechanism-distinctness JSON exists; one answer asset exists; all REQ-1..REQ-13 are resolved;
verificators pass with 0 errors; PR merged to main.

## Task Requirement Checklist

> **Task name**: Re-cluster t0086 13 cells and per-cluster Vm-trace deep-dive.
>
> **Short description**: Re-cluster 6 Genuine + 7 Marginal cells from t0086 (13 total); per-cluster
> Vm-trace deep-dive at 16 dirs to attribute mechanism; produce mechanism-distinctness answer asset.
>
> **Long description (excerpts from `task_description.md`)**: Phase A re-cluster 13 cells in 54-d
> natural-unit parameter space; KMeans k=2..6 + hierarchical (ward + cosine + euclidean) + UMAP /
> PCA; pick best k via silhouette + BIC; compute centroids; score against published biological
> priors via t0086's scorecard. Phase B per-cluster Vm-trace deep-dive at 16 directions on a
> representative cell per cluster (closest to centroid); record per-segment Vm + NMDA conductance +
> Nav1.6 / NaP currents + AIS spike onsets; produce 4 figures per representative; compute fractional
> channel contributions. Phase C compare attributions across clusters; mechanism distinctness
> verdict. Output: one answer asset `assets/answer/are-cluster-motifs-mechanistically-distinct/`.
> Local-CPU only; $0 cost.

| REQ | Description | Step(s) | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Load the 13-cell pool from t0086 cell_classification.json (6 Genuine + 7 Marginal); confirm cell IDs match `[767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1721]` | Step 9 | `code/select_representatives.py` + `results/data/recluster_assignments.json` |
| REQ-2 | Load 54-d natural-unit parameter vectors from t0083 `all_evaluations.json` for all 13 cells | Step 9 | Same artefact; `params` field per cell in `recluster_assignments.json` |
| REQ-3 | Run KMeans k=2..6 with silhouette + BIC selection on the 13-cell normalised parameter matrix | Step 9 | `results/data/recluster_assignments.json` `kmeans` array |
| REQ-4 | Run hierarchical clustering with ward linkage and cosine + euclidean metrics for cross-validation | Step 9 | `recluster_assignments.json` `hierarchical_cosine_labels` + `hierarchical_euclidean_labels` |
| REQ-5 | Run UMAP (or PCA fallback if UMAP fails) for 2D visualisation overlaid with cluster labels | Step 9 | `results/images/cluster_umap.png` |
| REQ-6 | Compute per-cluster centroids in normalised + unnormalised 54-d space; record within-cluster variance | Step 9 | `results/data/recluster_centroids.json` |
| REQ-7 | Score each cluster centroid against the 9 t0086 biological priors with plausible / stretched / exotic verdicts | Step 9 | `results/data/recluster_biological_scorecard.json` + `results/images/biological_plausibility_heatmap.png` |
| REQ-8 | Pick one representative cell per cluster as the cell minimising 54-d Euclidean distance to the cluster centroid | Step 9 | `results/data/representative_cells.json` |
| REQ-9 | Run a t0084-style Vm-trace deep-dive at 16 directions (every 22.5 deg) per representative cell with per-segment Vm + per-synapse NMDA + per-segment Nav1.6 / NaP recording | Step 9 | `results/data/cell{id}_dir{deg}_traces.npz` per representative cell x 16 directions |
| REQ-10 | Compute fractional channel attribution (NMDA / Nav1.6 / NaP) per representative cell using PD = 0 deg vs ND = 180 deg | Step 9 | `results/data/cell{id}_attribution.json` per representative cell |
| REQ-11 | Generate 4 standard figures per representative cell (Vm traces grid, NMDA conductance, Nav1.6 / NaP currents, AIS spike onsets) | Step 9 | `results/images/{vm_traces,nmda_conductance,nav_decomp,ais_spike_onset}_<cell_id>.png` |
| REQ-12 | Synthesise mechanism-distinctness verdict by comparing fractional contributions across clusters; record verdict + per-cluster narrative | Step 9 | `results/data/mechanism_distinctness.json` |
| REQ-13 | Write one answer asset at `assets/answer/are-cluster-motifs-mechanistically-distinct/` per the answer-asset specification | Step 9 | `assets/answer/are-cluster-motifs-mechanistically-distinct/{details.json, short_answer.md, full_answer.md}` |

## Approach

Three phases, all local-CPU. Phase A (clustering + biological scoring) is pure data analysis with
sklearn / scipy; estimated ~10 minutes. Phase B (per-cluster Vm-trace deep-dive) drives NEURON
simulations using the v3 substrate library; ~16 simulations per representative cell at ~60 s each =
~16 minutes per cell; 2-3 representative cells (depending on best_k from Phase A) = 32-48 minutes.
Phase C (mechanism-distinctness analysis + answer asset) is data analysis + markdown generation; ~10
minutes. Total wall-clock estimate: 1-2 hours.

The task copies code from t0086 (clustering core, biological priors, biological scorecard) and t0084
(deep-dive recording pattern, attribution metric, plotting helpers) into the local `code/`
directory, rebinding imports per the cross-task import rule. The library asset
`de_rosenroll_2026_dsgc_ais_dendritic_spike` from t0080 is the only external import. Per-task
constants (`ANGLES_16DIR_DEG`, `TARGET_CELL_IDS`) live in `code/constants.py`; per-task paths live
in `code/paths.py`.

## Cost Estimation

* **Phase A (clustering + biological scoring)**: $0. Pure local CPU; sklearn KMeans + scipy
  hierarchical + numpy/matplotlib. Estimated 10 min wall-clock.
* **Phase B (Vm-trace deep-dive)**: $0. Local CPU NEURON simulations. 2-3 representative cells x 16
  directions = 32-48 NEURON sims at ~60 s each = ~32-48 min wall-clock.
* **Phase C (mechanism distinctness + answer asset)**: $0. Pure data analysis + markdown generation.
  Estimated 10 min wall-clock.
* **Total**: $0.00. Local-CPU only.

Project budget after t0086: $15.56 spent / $20.00 cap; $4.44 remaining. t0088 estimated $0 preserves
the buffer for subsequent S-0086-* follow-ups.

## Step by Step

The implementation runs as a single integrated `main.py` orchestrator that drives all three phases
sequentially. The orchestrator imports task-local helpers and calls them in order.

1. **Setup**: import library asset `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants`
   (LOWER_BOUNDS, UPPER_BOUNDS, N_PARAMS, ParamIndex). Import task-local `paths`, `constants`.
   Ensure all output directories exist.

2. **Phase A.1 -- Load 13-cell parameter pool**: read t0086 `cell_classification.json`; filter to
   Genuine + Marginal cells (13 total); read t0083 `all_evaluations.json`; for each cell, look up
   `params` field; build a (13, 54) parameter matrix. Assert all 13 cells are found.

3. **Phase A.2 -- Cluster the 13 cells**: normalise the parameter matrix using LOWER / UPPER bounds;
   run KMeans k=2..6 with silhouette + BIC; pick best k; run hierarchical clustering with cosine +
   euclidean metrics at best_k; compute 50-sample bootstrap stability ARI; compute per-cluster
   centroids in normalised + unnormalised space + within-cluster variance. Write
   `recluster_assignments.json` and `recluster_centroids.json`.

4. **Phase A.3 -- UMAP / PCA visualisation**: try UMAP fit on the 13-cell normalised matrix; if fit
   succeeds use UMAP, else fall back to PCA(n=2). Overlay cluster labels with cell IDs as markers.
   Write `cluster_umap.png` (or `cluster_pca.png` if fallback).

5. **Phase A.4 -- Biological priors + scoring**: write the 9-prior database via
   `biological_priors.py` (`biological_priors.json`); score each cluster centroid via
   `biological_scorecard.py` (`recluster_biological_scorecard.json` +
   `biological_plausibility_heatmap.png`).

6. **Phase A.5 -- Pick representative cells**: per cluster, find the cell minimising 54-d Euclidean
   distance to the cluster centroid (in normalised space). Write `representative_cells.json` with
   one entry per cluster.

7. **Phase B.1 -- Build cell + apply parameter vector**: build the DSGCCellWithAIS once via
   `build_dsgc_cell_with_ais()`. For each representative cell, apply its 54-d parameter vector via
   `apply_parameter_vector(cell, ParameterVector(values=...))`.

8. **Phase B.2 -- Setup synapses parametrically**: per representative cell, call
   `setup_synapses_parametric(cell, ...)` with the cell's `n_ach`, `n_gaba`, `rho_0_ach`,
   `lambda_ach_um`, `rho_0_gaba`, `lambda_gaba_um`, `w_ach_us`, `w_gaba_us`, `placer_seed`,
   `gnmda_dend`, `mg_conc_mm`, `voff_nmda`. Use a deterministic placer_seed derived from a hash of
   the parameter vector (matching t0084).

9. **Phase B.3 -- Run 16-direction simulations**: for each representative cell, for each of the 16
   directions in `ANGLES_16DIR_DEG`, call `_run_one_direction_with_recording` with attached
   recording vectors for: t, v_soma, v_mid, v_distal, v_ais, g_nmda (per synapse), i_nav16 (per
   distal segment), i_nap (per distal segment). Save one `.npz` per (cell, direction) under
   `results/data/`.

10. **Phase B.4 -- Per-cell summary**: per representative cell, compute spike count + peak Vm per
    direction; compute DSI from PD (0 deg) vs ND (180 deg); write
    `results/data/cell{id}_summary.json`.

11. **Phase B.5 -- Compute fractional attribution**: per representative cell, run
    `compute_attribution(cell_id=...)` using the PD and ND .npz files; write
    `results/data/cell{id}_attribution.json` with `frac_nmda`, `frac_nav16`, `frac_nap`,
    `dominant_mechanism`.

12. **Phase B.6 -- Generate 4 figures per representative cell**: `vm_traces_<cell>.png` (3-row x
    16-column grid: proximal soma / mid dendrite / distal dendrite per direction);
    `nmda_conductance_<cell>.png` (16-line plot of summed NMDA conductance per direction);
    `nav_decomp_<cell>.png` (16-direction subplots of Nav1.6 vs NaP at distal dendrite);
    `ais_spike_onset_<cell>.png` (16-bin polar histogram of AIS spike onsets).

13. **Phase C.1 -- Compute mechanism distinctness**: load all per-representative attribution JSONs;
    compare fractional NMDA / Nav1.6 / NaP across clusters; produce a verdict `distinct` (different
    dominant mechanisms across clusters) vs `shared_mechanism_different_scale` (same dominant
    mechanism across clusters with parameter -scale variation) vs `mixed` (some clusters share a
    mechanism, others differ). Compare to t0084 cell 767 attribution (NaP-dominant 93%, Nav1.6 7%,
    NMDA 0%). Write `mechanism_distinctness.json` with verdict + per-cluster narrative.

14. **Phase C.2 -- Write answer asset**: produce
    `assets/answer/are-cluster-motifs-mechanistically-distinct/details.json` (asset metadata),
    `short_answer.md` (2-5 sentence answer), `full_answer.md` (full answer with sections per the
    answer-asset specification including evidence from code / experiments, synthesis, limitations,
    sources). Use the mechanism-distinctness verdict and per-cluster narrative from Phase C.1.

15. **Compute metrics + produce charts**: this is the final step ending the implementation. Results
    writing, suggestions, compare-literature are orchestrator steps managed by execute-task.

## Remote Machines

None. Local CPU only.

## Assets Needed

* **Library asset** (read-only): `de_rosenroll_2026_dsgc_ais_dendritic_spike` (registered under
  t0080). Provides cell builder, parameter vector helpers, synapse setup, constants.

## Expected Assets

* **One answer asset**: `assets/answer/are-cluster-motifs-mechanistically-distinct/`. Per the
  answer-asset specification: `details.json`, `short_answer.md`, `full_answer.md`.

## Time Estimation

* **Phase A**: 10 minutes wall-clock.
* **Phase B**: 32-48 minutes wall-clock (2-3 representatives x 16 directions x 60 s).
* **Phase C**: 10 minutes wall-clock.
* **Total**: 1-2 hours wall-clock; $0 cost.

## Risks & Fallbacks

* **UMAP fit fails on 13-cell sample** (UMAP needs at least 3-5 neighbours; defaults to 15 which is
  > sample size): fall back to PCA(n=2). Both produce a 2D scatter for visualisation.
* **k = 1 winner from silhouette + BIC** (homogeneous 13-cell pool): force k = 2 minimum and
  document in the results that the 13-cell pool has weak intrinsic structure. The downstream
  per-cluster representative selection still works at k = 2.
* **Representative cell selection ties** (two cells equidistant from centroid): pick the one with
  the smaller cell_index (deterministic tiebreaker).
* **NEURON simulation instability** (NaN Vm at one direction): retry with the placer_seed offset by
  +1 (matches t0084's existing fallback). Document any retried direction in `cell{id}_summary.json`.
* **Local CPU runtime exceeds 2 hours** (e.g., 90 s per direction instead of 60 s): no cost impact;
  document in `costs.json` `note` field. Wall-clock impact is acceptable.
* **Phase B representative cell parameter vector triggers a different bundle structure** (e.g.,
  different n_ach / n_gaba) than t0084: the `setup_synapses_parametric` helper handles all parameter
  combinations within bounds; no fallback needed.

## Verification Criteria

* `verify_research_code` passes with 0 errors.
* `verify_plan` passes with 0 errors.
* `verify_logs` passes with 0 errors (warnings LG-W007 / LG-W008 acceptable, cleared by
  `capture_task_sessions` in reporting).
* `verify_task_file`, `verify_task_dependencies`, `verify_task_folder` pass.
* The single answer asset passes `verify_answer_asset` (or equivalent answer-asset verificator) and
  the answer schema.
* `verify_task_metrics` accepts `metrics.json = {}` (this task produces an answer not metrics).
* `verify_task_results` accepts the V2 `results_detailed.md` with mandatory sections including
  Examples (>=10 concrete instances pulled from the per-direction trace files) and Task Requirement
  Coverage as the final section.
* `verify_pr_premerge` passes with 0 errors.
