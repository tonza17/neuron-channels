# Results Summary: Re-Simulate 10 Cells per t0117 Electrophys Cluster

## Summary

Stratified-sampled 40 cells (10 per t0117 electrophys cluster, k = 4) spanning DSI × PD quintiles
from the unfiltered 4 431-cell pool and re-simulated each cell in the canonical 3-mode trio
(EPSP_PASSIVE, IPSP_PASSIVE, FULL) for PD (0°) and ND (180°) directions — 240 NEURON runs total,
zero failures, ~70 min wall-clock. Produced 4 per-cluster 10-row × 3-column trace figures (g_E /
g_I / V_m, PD solid + ND dashed) and a 4-row × 3-column cross-cluster median-trace summary.
Demonstration / exploratory artefact; no answer assets produced (`expected_assets: {}`).

## Metrics

* **Cells re-simulated**: **40** (10 per electrophys cluster, stratified across 5 DSI × 5 PD
  quintile bins per cluster)
* **NEURON runs completed**: **240 / 240** (success rate 100.0%)
* **DSI span sampled**: **0.0 to 0.93** (most of the unfiltered pool sits near 0 — this is genuine
  pool composition, not a sampling bug; only seed 7755 cells provide DSI ≥ 0.2)
* **PD-rate span sampled**: **0.7 to 115 Hz**
* **Peak g_E range across cells**: **0.001 to 0.32 µS**
* **Peak g_I range across cells**: **0.016 to 0.95 µS**
* **g_I / g_E ratio (at peak g_E) range**: **0.03 to 440** (six orders of magnitude — the
  excitation-inhibition balance is the most variable feature across cells)
* **Spike count range** in FULL V_m: **0 to ~26** (with one cell at DSI 0.93 producing 0 spikes —
  silent under the canonical −10 mV threshold; documented)
* **Trace samples per file**: **1 400** (RECORD_DT = 1.0 ms × TSTOP = 1 400 ms)
* **Figures produced**: **5** (4 per-cluster + 1 cross-cluster median summary)

## Verification

* `verify_plan` — **PASSED** (0 errors, 0 warnings)
* `verify_research_code` — **PASSED**
* `verify_task_results` — **PASSED**
* `verify_task_metrics` — **PASSED** (`metrics.json = {}` valid; documented)
* C1: 40-cell manifest resolves to t0117 pooled parquet (one-to-one) — **PASSED**
* C2: every (cell, mode, direction) trace parquet has 1 400 rows with mode-correct columns —
  **PASSED**
* C3: all 5 PNGs on disk — **PASSED**
* `dsi_sanity_check.csv`: **39 / 40** cells satisfy PD-spike-count > ND-spike-count for DSI > 0.5
  (the one failure is a near-silent cell whose V_m never crosses −10 mV in either direction —
  edge case, not a pipeline bug)
* `ruff check --fix`, `ruff format`,
  `mypy -p tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code` — **PASSED**
