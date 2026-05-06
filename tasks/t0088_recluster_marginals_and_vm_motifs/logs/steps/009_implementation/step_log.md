---
spec_version: "3"
task_id: "t0088_recluster_marginals_and_vm_motifs"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-06T19:58:06Z"
completed_at: "2026-05-06T20:50:00Z"
---
# Step 9 -- Implementation

## Summary

Executed all three phases on local CPU. Phase A re-clustered the 13-cell pool (6 Genuine + 7
Marginal) and produced **best_k = 4 clusters** (silhouette = 0.164, bootstrap ARI = 0.583 +/-
0.226); all 4 clusters classified exotic by the biological scorecard. Phase B ran the per-cluster
Vm-trace deep-dive at 16 directions on the 4 representative cells (1604, 1634, 767, 1639) using the
cell builder + recording pattern from t0080 / t0084 libraries; **all 64 simulations stable**
(`stable_count == expected_total == 64`). Phase C produced the mechanism-distinctness verdict
**`shared_mechanism_different_scale`** because all 4 representative cells are NaP-dominant in
PD-minus-ND attribution (frac NaP 0.874-0.997, frac Nav1.6 0.003-0.126, frac NMDA = 0.000), and
wrote the single answer asset at `assets/answer/are-cluster-motifs-mechanistically-distinct/`.

## Actions Taken

1. Wrote `code/constants.py` with `TARGET_CELL_IDS` (13 cells), `ANGLES_16DIR_DEG` (every 22.5 deg),
   response-window + clustering hyperparameters.
2. Wrote `code/paths.py` with task-local input / output path constants.
3. Wrote `code/biological_priors.py` (copied from t0086 with import-path rebinding); ran
   biological_priors module to produce `biological_priors.json` (9 priors).
4. Wrote `code/select_representatives.py` (Phase A driver: cell loader + clustering core +
   representative selection adapted from t0086 cluster_analysis.py); ran it to produce
   `recluster_assignments.json` (best_k = 4), `recluster_centroids.json`, and
   `representative_cells.json` (representatives: cluster 0 -> 1604, cluster 1 -> 1634, cluster 2 ->
   767, cluster 3 -> 1639). Generated cluster PCA / silhouette / dendrogram PNGs (UMAP not
   available; PCA fallback used).
5. Wrote `code/biological_scorecard.py` (copied from t0086 with import-path rebinding); ran it to
   produce `recluster_biological_scorecard.json` and `biological_plausibility_heatmap.png`. All 4
   clusters classified exotic.
6. Compiled the t0080 NEURON MOD library at
   `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/nrnmech.dll` via
   `nrnivmodl.bat ../mods` (this is a build artefact; it lives outside the t0088 task folder but is
   required by `apply_parameter_vector` to load Nav1.6, NaP, KDr, etc. mechanisms; the build is not
   committed because t0080 is a completed task and we cannot modify its folder).
7. Wrote `code/run_deepdive.py` (copied from t0084 with `ANGLES_16DIR_DEG` substitution and cell
   list loaded from `representative_cells.json`); ran it to produce 64 `.npz` trace files (4 cells x
   16 directions) and 4 per-cell summary JSONs. All 64 simulations passed the `is_stable` check.
8. Wrote `code/attribution_metric.py` (copied from t0084 with task-local path rebinding); ran it to
   produce 4 per-representative `cell{id}_attribution.json` files. All 4 representatives are
   NaP-dominant.
9. Wrote `code/plot_figures.py` (copied from t0084 with subplot grid columns updated to 16); ran it
   to produce 16 PNGs (4 figures per representative cell: Vm traces grid, NMDA conductance, Nav1.6 /
   NaP currents, AIS spike onsets at 16 directions polar).
10. Wrote `code/mechanism_distinctness.py` (Phase C driver); ran it to produce
    `mechanism_distinctness.json` with verdict `shared_mechanism_different_scale`.
11. Wrote `code/write_answer_asset.py` (Phase C answer asset writer); ran it to produce
    `assets/answer/are-cluster-motifs-mechanistically-distinct/{details.json, short_answer.md, full_answer.md}`.
12. Ran `ruff check --fix` and `ruff format` on `code/`; all checks pass.
    `mypy -p tasks.t0088_recluster_marginals_and_vm_motifs.code` passes with 0 issues.
13. Ran `flowmark` on the answer asset markdown files.

## Outputs

* `tasks/t0088_recluster_marginals_and_vm_motifs/code/constants.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/paths.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/biological_priors.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/biological_scorecard.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/select_representatives.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/run_deepdive.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/attribution_metric.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/plot_figures.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/mechanism_distinctness.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/code/write_answer_asset.py`
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/biological_priors.json` (9 priors)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/recluster_assignments.json` (best_k =
  4, silhouette = 0.164, bootstrap ARI = 0.583 +/- 0.226)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/recluster_centroids.json` (4
  centroids, between-cluster distance matrix)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/recluster_biological_scorecard.json`
  (all 4 clusters exotic)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/representative_cells.json`
  (representatives 1604, 1634, 767, 1639)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/cell{id}_dir{int_tenths}_traces.npz`
  (64 trace files: 4 representatives x 16 directions)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/cell{id}_summary.json` (4 per-cell
  summaries)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/cell{id}_attribution.json` (4
  per-representative fractional attributions)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/mechanism_distinctness.json` (verdict
  `shared_mechanism_different_scale`)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/images/cluster_pca.png`,
  `cluster_silhouette.png`, `cluster_dendrogram.png`, `biological_plausibility_heatmap.png` (Phase A
  plots)
* `tasks/t0088_recluster_marginals_and_vm_motifs/results/images/{vm_traces,nmda_conductance, nav_decomp,ais_spike_onset}_{1604,1634,767,1639}.png`
  (16 PNGs, 4 figures per representative cell)
* `tasks/t0088_recluster_marginals_and_vm_motifs/assets/answer/ are-cluster-motifs-mechanistically-distinct/{details.json, short_answer.md, full_answer.md}`
  (answer asset)

## Issues

* The `init_task_folders.py` `--step-log-dir` flag rejected the absolute Windows path during Phase
  0; worked around by writing `folders_created.txt` directly. Documented in step 3 log.
* The t0080 NEURON MOD library was not pre-compiled in the worktree; built it via
  `nrnivmodl.bat ../mods` from the t0080 `code/build/` directory before running Phase B. This build
  artefact lives in t0080's folder (a completed task) but is not committed -- it is generated
  locally per worktree and is reproducible from the source `.mod` files.

## Requirement Completion Checklist

* REQ-1: Done -- 13 cells loaded from t0086 cell_classification.json; cell IDs match the expected
  list.
* REQ-2: Done -- 54-d parameter vectors for all 13 cells loaded from t0083 all_evaluations.json.
* REQ-3: Done -- KMeans k=2..6 with silhouette + BIC selection; best_k = 4.
* REQ-4: Done -- hierarchical clustering with cosine + euclidean metrics at best_k = 4; ARI vs
  KMeans = 0.799 (cosine and euclidean both).
* REQ-5: Done -- PCA fallback used (UMAP unavailable); cluster_pca.png written.
* REQ-6: Done -- 4 cluster centroids in normalised + unnormalised space + within-cluster variance
  + between-cluster distance matrix.
* REQ-7: Done -- per-cluster biological scorecard against 9 priors; all 4 clusters exotic.
* REQ-8: Done -- representatives picked as min-distance-to-centroid: cluster 0 -> 1604, cluster 1 ->
  1634, cluster 2 -> 767, cluster 3 -> 1639.
* REQ-9: Done -- 64 stable NEURON simulations at 16 directions x 4 representatives, with per-segment
  Vm + per-synapse NMDA + per-segment Nav1.6 / NaP recording.
* REQ-10: Done -- fractional channel attribution computed per representative; all NaP-dominant.
* REQ-11: Done -- 4 figures per representative cell (16 PNGs total).
* REQ-12: Done -- mechanism_distinctness.json with verdict `shared_mechanism_different_scale` and
  per-cluster narrative.
* REQ-13: Done -- answer asset at `assets/answer/are-cluster-motifs-mechanistically-distinct/`.
