---
spec_version: "2"
task_id: "t0109_t0108_morph_cluster_gallery"
date_completed: "2026-05-18"
---

# t0109 — Morphology Gallery for the 4 t0108 Clusters: Results Summary

## Summary

Rendered up to 10 example morphologies per t0108 morphology K-means cluster. Cluster 3 has only 7
cells in t0108 (total cells per cluster: 21 / 55 / 67 / 7), so its row is 7 panels wide. Top
cells per cluster were picked deterministically by descending `DSI x PD_rate` and rebuilt via
the t0090/t0092 morphology generator. The 4-row × 10-column gallery is at
`results/images/morphology_gallery_by_cluster.png`.

## Metrics

* Cluster sizes (from t0108 morphology K-means, k=4): **21 / 55 / 67 / 7**.
* Examples shown per cluster: **10 / 10 / 10 / 7** (max 10 cap).
* Total morphologies built and rendered: **37**.
* Morphology build failures: **0**.

## Verification

* All 37 cell panels render without "build failed" placeholders.
* Per-panel annotations match `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/
  filtered_cells.json` rows (DSI, PD-rate, generation) for the corresponding `cluster_labels`
  entries in `morphology_clusters.json`.
* `results/data/gallery_picks.json` lists the exact pick per cluster for reproducibility.
* `metrics.json` empty (no registered metric variant); `costs.json` = 0 USD;
  `remote_machines_used.json` = `[]`; `suggestions.json` empty.

## Figures

* `results/images/morphology_gallery_by_cluster.png` — 4-row × 10-col morphology gallery.

## Headline interpretation

Cluster 0 (n=21, fast-firing, PD ~103 Hz) and cluster 2 (n=67, middle PD ~84 Hz) show similar
broad dendritic fields. Cluster 1 (n=55, highest DSI ~0.90, PD ~71 Hz) shows tighter, more
PD-asymmetric morphologies. Cluster 3 (n=7, slow-firing PD ~29 Hz) is visually distinct — its
cells have a different branching pattern consistent with the low-axonal-Na, high-K channel
regime identified in t0108 (NAV16_AIS = 0.78 vs ~3.1 in the other clusters).
