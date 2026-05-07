# Results Summary: Procedural DSGC Morphology Generator + Diversity Test + Validation Bundle

## Summary

Delivered a deterministic 14-knob procedural DSGC morphology generator (library asset
`procedural_dsgc_morphology_generator`) plus a 60-morphology diversity sweep, a Phase G validation
triplet (G.1 done, G.2 / G.3 partial), and the
`validation-triplet-implications-for-biological-plausibility` answer asset. **13/16 REQs done, 3
partial** — partial REQs (REQ-9 Bed-B reproducibility, REQ-11 G.2 NMDA calibration, REQ-12 G.3 NaP
knockout) all share the same root cause: the procedural Bed-B-equivalent cell paired with the t0083
best-cell channel set is silent (DSI=0), so the downstream simulations cannot produce informative
deltas. Drivers and infrastructure are committed for all phases; a follow-up correction task should
retune `BEDB_BASE_POINT` so the procedural cell elicits spikes under the t0083 channel set before
re-running F / G.2 / G.3.

## Metrics

* **Generator unit tests**: **9 / 9** passing (`uv run pytest tasks/t0090_.../code/`).
* **Different-set verification stability**: **6 / 30** STABLE (24/30 NAN_VOLTAGE; consistent with
  Mainen 1996 morphology-determines-firing-pattern when applying a fixed channel set to morphologies
  it was not fitted on).
* **Similar-set verification stability**: **3 / 30** STABLE (27/30 NAN_VOLTAGE).
* **Direction selectivity index, different_set (STABLE cells)**: **0.000** (synaptic input does not
  drive spikes on the procedural topologies under the t0083 channel set).
* **Direction selectivity index, similar_set (STABLE cells)**: **0.000**.
* **Morphometric PCA variance explained (PC1+PC2)**: **82.9 percent** of variance over a 6-feature
  morphometric matrix; similar-set cluster radius (95th percentile) is **20.8 percent** of the PC1
  range — within the plan's "tight cluster" target.
* **G.1 cluster-1 AIS-to-soma Nav ratio audit**: cluster-1 centroid ratio = **116.0**; per-cell
  ratios **139.4 / 42.6 / 270.7 / 141.2** for cells 1304, 1504, 1624, 1634; **0 / 4** floor-pinned;
  verdict: **`real_signal`**.
* **G.2 NMDA calibration**: 7-point sweep ran but **0/7 valid recordings** because the procedural
  cell diverges during stimulus when paired with t0083 params; cluster re-score values null.
* **G.3 NaP knockout**: driver complete, **0 / 4 cells** with completed simulations
  (`infrastructure_only`).
* **Bed-B reproducibility**: **0 / 5** cells with completed deltas (`infrastructure_only`).
* **Library + answer assets**: 1 + 1 produced; both pass their schema requirements.

## Verification

* `uv run pytest tasks/t0090_morphology_generator_diversity_test/code/` — **9 / 9** PASS
* `verify_research_papers.py`, `verify_research_internet.py`, `verify_research_code.py`,
  `verify_plan.py` — PASSED in earlier steps
* `verify_task_metrics.py` — to be run during the reporting step (only registered metric keys
  retained in `metrics.json`)
* `verify_logs.py`, `verify_task_file.py`, `verify_task_folder.py`, `verify_task_results.py`,
  `verify_assets.py`, `verify_corrections.py`, `verify_pr_premerge.py` — to be run during the
  reporting step
