# t0109 — Morphology Gallery for the Four t0108 Morphology Clusters

## Context

t0108 identified 4 K-means clusters on the 14-d morphology submatrix of the 150 strict-cohort
t0106 cells (DSI > 0.5 AND PD > 10). Sizes: 21 / 55 / 67 / 7. Cluster 3 (n=7) is the
high-K low-axonal-Na outlier morphology. The numerical Kruskal-Wallis results identify *which*
electrophys parameters separate the morphology clusters, but they do not show what the actual
dendritic shapes look like.

## Goal

Render up to **10 example morphologies per cluster** (all 7 for cluster 3), with DSI / PD / source
seed/gen annotated per panel, arranged as one row per cluster.

## Approach

* Load `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/filtered_cells.json` and
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/morphology_clusters.json`.
* Re-attach the cluster label to each cell using the order in `morphology_clusters.json`
  `cluster_labels`.
* Within each cluster, rank cells by descending `DSI × PD-rate` and take the top 10 (deterministic
  selection). Cluster 3 has only 7 cells; take all of them.
* Build each morphology via
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`,
  exactly as t0105's build_gallery did.
* Plot top-down (x, y) projection per cell, soma marked, PD-arrow indicated. Annotate
  `DSI`, `PD-rate`, `generation`, `cluster id`.
* Layout: 4 rows × 10 cols. Row label gives cluster id and cluster size from t0108.
* Output: `results/images/morphology_gallery_by_cluster.png`.

## Out of Scope

* New optimisation / re-evaluation.
* Re-clustering or re-doing t0108's analysis.
* 3D rendering or any per-cell electrophysiology plotting.
