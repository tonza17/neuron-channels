# t0109 — Plan

## Objective

Render up to 10 example morphologies per t0108 morphology cluster (4 clusters, sizes
21/55/67/7 — cluster 3 gets all 7), arranged as a 4-row x 10-col grid PNG with DSI/PD/source
annotations per panel.

## Approach

Pure visualisation task on existing t0108 result data. Reuse the t0105 build_gallery code patterns
for morphology building via
`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`.

Selection is deterministic: sort cells within each cluster by descending `DSI * PD_rate` and take
the top 10 (or all if fewer).

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Local compute (morphology builds for up to 37 cells) | < 5 minutes |
| API costs | $0 |
| **Predicted spend** | **$0** |
| **Hard cap** | **$0** |

## Step by Step

1. Load t0108 filtered_cells.json + morphology_clusters.json.
2. Attach cluster label to each cell using `cluster_labels` index order.
3. Per cluster, sort by DSI*PD desc; take top min(10, n_cluster).
4. Build each morphology; extract soma + dend pt3d coords.
5. Render 4-row x 10-col grid PNG.

## Remote Machines

None.

## Assets Needed

* `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/filtered_cells.json`
* `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/morphology_clusters.json`
* `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`
* `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py`

## Expected Assets

None (pure visualisation; no answer / model / dataset / paper assets).

## Time Estimation

* Implementation: 30-60 min.
* Reporting: 15 min.
* **Total**: ~1 hour wall clock.

## Risks & Fallbacks

* **Risk**: some morphology builds fail (NEURON section errors, etc.).
  **Fallback**: mark panel with "build failed" and continue.
* **Risk**: cluster 3 has only 7 cells.
  **Fallback**: render row 3 with 7 panels + 3 blanks.

## Verification Criteria

* `verify_task_results t0109_t0108_morph_cluster_gallery` passes with 0 errors.
* `verify_task_complete` passes with 0 errors.
* `results/images/morphology_gallery_by_cluster.png` exists and is embedded in
  `results_detailed.md`.

## REQ Checklist

* **REQ-1**: Load t0108 cluster labels and cell vectors.
* **REQ-2**: Per cluster, select top 10 (or all) cells by DSI*PD descending.
* **REQ-3**: Build each morphology using the project morphology generator.
* **REQ-4**: Render a 4-row x 10-col grid PNG with per-panel annotations.
* **REQ-5**: Embed the chart in results_detailed.md and reference in results_summary.md.
