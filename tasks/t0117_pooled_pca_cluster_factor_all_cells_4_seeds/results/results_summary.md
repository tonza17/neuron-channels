# Results Summary: Pooled PCA + Cluster + Factor Analysis of ALL Cells (4 seeds, no filter)

## Summary

Pooled **4 431** unique cells (1 065 + 654 + 1 686 + 1 026 across seeds 44 / 77 / 7755 / 9354) from
the same four NSGA-II runs as t0116, but with NO DSI / PD cohort filter. Ran the identical PCA +
KMeans + varimax FA pipeline and produced three answer assets plus an explicit head-to-head
`results/data/t0116_comparison.csv`. **Headline finding: the truncated-cohort artefact is
confirmed** — F1 in the unfiltered pool is a joint DSI-PD factor (r_DSI = **+0.421**, r_PD =
**+0.352**, both > 0.30), whereas no factor crossed |r| > 0.30 on both axes in t0116. The
seed-specific basin pattern also weakens substantially (electrophys NMI **0.929 → 0.562**,
morphology NMI **0.889 → 0.313**), confirming that t0116's strict cohort exaggerated cross-seed
basin isolation.

## Metrics

* **Pooled cohort size**: **4 431** unique cells from 16 992 raw evaluations (~5× t0116's 869)
* **Electrophys KMeans**: k = **4**, mean silhouette = **0.158**, NMI(cluster, seed) = **0.562**,
  chi-square p < 1e-300
* **Morphology KMeans**: k = **5**, mean silhouette = **0.153**, NMI(cluster, seed) = **0.313**,
  chi-square p < 1e-300
* **Varimax factor analysis**: **15** Kaiser eigenvalues > 1, capped at **10** factors, **34.9 %**
  total variance explained (vs t0116's 65.3 %)
* **Joint-factor count**: **1** (F1: r_DSI = +0.421, p ~ 1e-189; r_PD = +0.352, p ~ 1e-129; 12.6 %
  variance explained). **t0116 had 0.**
* **F1 vs t0116 F1**: t0117 F1 is a joint driver; t0116 F1 was DSI-only — the strict cohort erased
  the joint axis.
* **Gen-0 displacement** (per-seed mean in PC1+PC2): seed 44 = **4.87**, seed 77 = **1.49**, seed
  7755 = **5.74**, seed 9354 = **1.59** — same rank order as t0116 but uniformly smaller because
  the pool now includes near-init cells.
* **Gen-0 displacement** (per-seed mean in 68-d standardised space): **8.83 – 9.34** across all
  four seeds (vs t0116's 59.7 – 61.3 — much smaller because the standardiser is now fitted on a
  broader distribution).
* **Charts produced**: **9** PNGs under `results/images/` (1 extra cluster grid vs t0116 because
  t0117 chose k = 4 instead of 3).
* **Answer assets produced**: **3** under `assets/answer/`.

## Verification

* `verify_plan` — **PASSED** (0 errors, 0 warnings)
* `verify_task_results` — **PASSED**
* `verify_task_metrics` — **PASSED** (metrics.json = `{}`, intentional)
* C1 (parquet row count == per-seed sum): **PASSED** — 4 431 == 1 065 + 654 + 1 686 + 1 026
* C2 (union-pool standardiser shape (68,) / (68,), all std > 0): **PASSED**
* C3 (all 9 required PNGs on disk): **PASSED**
* C4 (local answer-asset structural check on all 3 assets): **PASSED**
* C5 (schema sanity: no NaN in vector cols): **PASSED**
* `ruff check --fix`, `ruff format`,
  `mypy -p tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code`: **PASSED** (clean)
