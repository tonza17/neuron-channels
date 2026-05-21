# Results Summary: Pooled PCA + Cluster + Factor Analysis of DSI > 0.7 / PD > 10 Cells (4 Seeds)

## Summary

Pooled **869** unique joint-pass survivor cells (`dsi_vector_sum > 0.7 ∧ pd_rate_hz > 10.0`) from
four NSGA-II runs (t0106 seed 44, t0112 seed 77, t0114 seed 7755, t0115 seed 9354), ran a unified
PCA + KMeans + varimax factor analysis on the standardised 68-d feature pool, and produced three
answer assets covering basin connectivity, displacement from random init, and latent drivers of
joint-pass quality. Headline finding: the four-seed cohort fragments into **seed-specific
sub-basins** (electrophys KMeans NMI = **0.929**; morphology KMeans NMI = **0.889**), not a single
connected manifold; F1 drives DSI as a mixed ephys + morph factor (`r = -0.589`), F3 drives PD-rate
as a purely electrophys factor (`r = +0.746`), and no factor crosses |r| > 0.3 on both DSI and PD
— the strict-cohort decoupling reproduces t0110's truncated-cohort artefact.

## Metrics

* **Pooled cohort size**: **869** unique cells from **16 992** raw evaluations (121 + 10 + 675 + 63
  across seeds 44 / 77 / 7755 / 9354)
* **Electrophys KMeans**: k = **3**, mean silhouette = **0.472**, NMI(cluster, seed) = **0.929**,
  chi-square p < 1e-300
* **Morphology KMeans**: k = **3**, mean silhouette = **0.529**, NMI(cluster, seed) = **0.889**,
  chi-square p < 1e-300
* **Varimax factor analysis**: **11** eigenvalues > 1, capped at **10** factors, **65.3 %** total
  variance explained
* **Top factor / DSI correlation**: F1 with `r = -0.589` (mixed ephys + morph)
* **Top factor / PD correlation**: F3 with `r = +0.746` (purely electrophys)
* **Gen-0 displacement** (per-seed mean in PC1 + PC2): seed 44 = **15.0**, seed 77 = **8.5**, seed
  7755 = **13.3**, seed 9354 = **2.4** (PC units)
* **Gen-0 displacement** (per-seed mean in 68-d standardised space): all four seeds in the narrow
  band **59.7 – 61.3** standardised units
* **Charts produced**: **8** PNGs under `results/images/`
* **Answer assets produced**: **3** under `assets/answer/`

## Verification

* `verify_plan` — **PASSED** (0 errors, 0 warnings)
* C1 (parquet row count == per-seed sum): **PASSED** — 869 == 121 + 10 + 675 + 63
* C2 (union-pool standardiser shape (68,) / (68,), all std > 0): **PASSED**
* C3 (all required PNGs present on disk): **PASSED** — 8 / 8
* C5 (schema sanity: DSI > 0.7, PD > 10, no NaN in vector cols): **PASSED**
* `verify_answers_local` (local re-implementation of missing `verify_answer_asset`): **PASSED** for
  all 3 answer assets
* `ruff check --fix`, `ruff format`,
  `mypy -p tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code`: **PASSED** (clean)
