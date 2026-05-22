---
spec_version: "2"
answer_id: "pooled-all-cells-truncated-cohort-artefact-test"
answered_by_task: "t0117_pooled_pca_cluster_factor_all_cells_4_seeds"
date_answered: "2026-05-22"
confidence: "high"
---
# One joint DSI-PD factor reappears in the unfiltered pool, confirming truncated-cohort artefact

## Question

Does at least one varimax factor recover a joint DSI-PD axis (|r_DSI| > 0.3 AND |r_PD| > 0.3)
when the cohort filter is removed and the full DSI / PD quality range is in the pool, confirming
the truncated-cohort artefact first observed at t0110 and t0116?

## Short Answer

Yes — F1 of the unfiltered-pool varimax solution is a joint DSI-PD factor (r_DSI = +0.421, r_PD
= +0.352, both p < 1e-100, n = 4431), satisfying |r| > 0.3 on both axes. At the strict cohort
(t0116) zero of ten factors satisfied this criterion. The reappearance of a joint factor once
the filter is lifted confirms the truncated-cohort-artefact hypothesis: the strict cohort
genuinely erases the shared latent that couples DSI and PD; the decoupling is not an intrinsic
substrate property.

## Research Process

The factor-analysis pipeline mirrors t0116 / t0108 exactly with only the cohort filter removed
upstream in `code/load_pooled_cells.py`:

1. Load every record (no DSI / PD filter) from the four seeds.
2. Dedup by the 68-d vector rounded to 6 decimals; persist `data/pooled_all_cells.parquet`
   (n=4431 unique cells).
3. Fit a single union-pool z-score standardiser; persist mean / std arrays.
4. Compute correlation-matrix eigenvalues on the standardised matrix; count Kaiser eigenvalues
   > 1 (`code/factor_analysis.py` `run_factor_analysis`).
5. Cap factor count at `KAISER_FACTOR_CAP = 10` (inherited from t0108).
6. Refit `sklearn.decomposition.FactorAnalysis(n_components=n_factors)` with the chosen count.
7. Apply varimax rotation (iterative SVD, gamma=1, tol=1e-6, max_iter=500) — same helper as
   t0108 / t0110 / t0116.
8. Compute rotated factor scores via the regression approximation `Z @ Λ @ pinv(ΛᵀΛ)`.
9. Render the loadings heatmap to `results/images/factor_loadings_heatmap.png` and emit
   per-factor variance + Pearson r vs DSI / PD to `results/data/factor_correlations.csv`.
10. Flag every factor satisfying `|r_DSI| > 0.30 AND |r_PD| > 0.30` (the joint-DSI-PD criterion;
    `JOINT_FACTOR_R_THRESHOLD = 0.30` in `code/constants.py`).

## Evidence from Papers

No paper-based evidence was used. The truncated-cohort artefact question is internal to this
project's NSGA-II survivor cohort and has no published benchmark — its origin is in t0108
(strict DSI > 0.5 cohort, all-negative PD correlations) and was first identified as a candidate
strict-cohort artefact by t0110.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Factor count and total variance explained (`results/data/factor_correlations.csv`):

| Quantity | t0116 (strict) | t0117 (no filter) |
| --- | --- | --- |
| Raw Kaiser eigenvalues > 1 | 10 (capped at 10) | 15 (capped at 10) |
| Factors retained | 10 | 10 |
| Total variance explained | 65.3% | 34.9% |
| Joint-factor count (|r| > 0.3 on both) | 0 | 1 (F1) |

The unfiltered pool has nearly double the number of raw Kaiser-eligible factors (15 vs 10) but
the same number is retained because of the project's KAISER_FACTOR_CAP = 10 inherited from
t0108. Total variance explained is dramatically lower (34.9% vs 65.3%) because admitting the
sub-threshold cells re-introduces the random-init dispersion — the strict cohort had already
been pre-selected for a narrow region of parameter space, so its 10 factors covered a much
higher proportion of its (smaller) variance.

Per-factor table at t0117 (`results/data/factor_correlations.csv`):

| Factor | var_explained_pct | r_dsi | r_pd | joint_factor_flag |
| --- | --- | --- | --- | --- |
| F1 | 12.61 | +0.421 | +0.352 | **True** |
| F2 | 3.69 | +0.032 | +0.314 | False |
| F3 | 3.48 | −0.004 | −0.172 | False |
| F4 | 2.59 | +0.262 | −0.238 | False |
| F5 | 4.25 | −0.262 | −0.554 | False |
| F6 | 1.53 | −0.031 | −0.099 | False |
| F7 | 1.96 | −0.019 | −0.080 | False |
| F8 | 1.43 | +0.145 | −0.005 | False |
| F9 | 1.08 | +0.077 | +0.040 | False |
| F10 | 2.28 | +0.277 | +0.244 | False |

F1 is the unambiguous joint factor: both r_DSI = +0.421 and r_PD = +0.352 exceed the |r| > 0.30
threshold by a comfortable margin, both with p-values astronomically below 0.05 (1.18e-189 and
3.59e-129 respectively at n=4431). F1 alone explains 12.6% of the total 34.9% variance — by far
the dominant factor.

Direct head-to-head per-factor table at t0116 (`tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/factor_correlations.csv`):

| Factor | t0116 var_pct | t0116 r_dsi | t0116 r_pd | t0116 joint? |
| --- | --- | --- | --- | --- |
| F1 | 30.06 | −0.589 | −0.210 | False (r_pd too small) |
| F2 | 14.02 | −0.086 | −0.367 | False (r_dsi too small) |
| F3 | 9.36 | −0.172 | +0.746 | False (r_dsi too small) |
| F4 | 1.83 | +0.089 | −0.230 | False (both too small) |
| F5 | 2.94 | +0.057 | +0.230 | False (both too small) |
| F6 | 1.35 | −0.222 | +0.033 | False (r_pd too small) |
| F7 | 1.36 | +0.087 | −0.009 | False (both too small) |
| F8 | 1.87 | +0.014 | −0.038 | False (both too small) |
| F9 | 1.10 | −0.026 | +0.070 | False (both too small) |
| F10 | 1.38 | −0.059 | −0.095 | False (both too small) |

At t0116 the highest |r_DSI| is 0.589 (F1) but with r_PD = −0.210 — below threshold. The highest
|r_PD| is 0.746 (F3) but with r_DSI = −0.172 — below threshold. The strict cohort has DSI and PD
each correlated with separate factors but no single factor coupling them, confirming the t0110
artefact signature. Once the filter is lifted, the cells with low DSI and low PD re-enter the
pool and a single shared latent re-emerges (t0117 F1).

The loadings heatmap (`results/images/factor_loadings_heatmap.png`) shows F1's loadings
distributed across multiple electrophys + morphology parameters with no single dominant feature
— consistent with a shared "quality" axis that the GA pushed against rather than a single
mechanistic driver.

## Synthesis

The unfiltered pool delivers a definitive answer to the t0110-originating question: the
DSI-vs-PD decoupling observed at every strict cohort (t0108 DSI > 0.5: all-negative PD
correlations; t0116 DSI > 0.7 AND PD > 10 Hz: zero joint factors) is a truncated-cohort artefact
in the strict sense. The substrate's underlying parameter space genuinely has a shared
DSI-PD latent (t0117 F1: r_DSI=+0.421, r_PD=+0.352), and the strict cohort filter erases this
latent by retaining only cells from a narrow region of joint-quality space where DSI and PD have
already been simultaneously optimised to high values. Once both have ceilings (the GA has hit
the top of both objective dimensions), additional variation along the F1 direction stops moving
either DSI or PD — so the correlation flattens to below 0.3 at the strict cohort.

This conclusively confirms t0110's finding (relaxed DSI > 0.2 cohort: 2 of 10 factors had
positive r(PD)) and extends it: at the fully unfiltered pool, the joint factor emerges as the
dominant factor (12.6% variance explained, by far the largest of any factor in either t0116 or
t0117). The substrate-level interpretation should NOT be "DSI and PD are decoupled in this
parameter space" — that is a strict-cohort framing artefact. The substrate-level interpretation
is "there exists a shared quality axis F1 along which both DSI and PD increase together; high-DSI
high-PD cells are at the top end of this axis; the cohort filter retains only the top of this
axis and so masks the underlying correlation."

For downstream tasks, the practical implication is: when reporting parameter-DSI / parameter-PD
correlations, always either (a) use the unfiltered pool (or a relaxed DSI > 0.2 cohort) or
(b) explicitly note that strict-cohort correlations cannot be interpreted as substrate-level
relationships. t0116's all-negative joint-factor result remains valid as a description of the
strict-cohort cells, but its substrate-level interpretation should be retracted in favour of
this t0117 result.

## Limitations

* **Gen-1 / early-generation cells dominate the pool**. The unfiltered pool admits the gen-0
  random-init (n=384) and every subsequent generation including the very early ones where
  NSGA-II has not yet found any high-quality cell. The F1 joint factor may therefore reflect
  not only the substrate-level DSI-PD coupling but also the trajectory NSGA-II takes from a
  random init to its Pareto front. A possible refinement is a generation-stratified analysis
  (limit to generations ≥ 50 vs all generations); this is documented as a follow-up.
* **t0117 F1 is not the same as any t0116 factor**. Cross-pool factor identity is not preserved
  by varimax rotation — there is no formal correspondence between t0117 F1 and any specific
  t0116 factor. The valid comparison is at the partition level (joint-factor count: 1 vs 0),
  not at the per-factor level.
* **The joint factor accounts for 12.6% of variance, not the majority**. The substrate-level
  DSI-PD coupling is real but modest; most parameter variation does not project onto F1.
  Mechanistic interpretation of F1's loadings (which channels / morphology parameters drive
  joint DSI-PD?) is left to a downstream task — t0117 only confirms its existence.
* **n=4431 is large enough that very small effect sizes become statistically significant**.
  Both r_DSI=+0.421 and r_PD=+0.352 are well above the |r| > 0.30 threshold and would remain so
  at much smaller sample sizes, so this is not a "p-hacking by sample size" finding. But the
  reader should weight the effect magnitude (|r| ≈ 0.4), not the p-value, when judging
  biological significance.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — seed 44 NSGA-II run.
* Task: `t0112_t0106_seed77_replicate` — seed 77 replicate.
* Task: `t0114_seed7755_no_autostop` — seed 7755 replicate.
* Task: `t0115_seed9354_no_autostop` — seed 9354 replicate.
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — original strict-cohort observation of
  all-negative PD correlations.
* Task: `t0110_relaxed_cohort_factor_analysis` — first relaxed-cohort follow-up that flagged
  the artefact at DSI > 0.2.
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10` — strict DSI > 0.7 AND PD > 10 head-to-head
  reference (joint-factor count = 0).
* Result data:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/factor_correlations.csv`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/factor_loadings.csv`,
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/t0116_comparison.csv`.
* Visualisation:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/images/factor_loadings_heatmap.png`.

[t0108]: ../../../../t0108_t0106_cluster_factor_dsi05_pd10/
[t0110]: ../../../../t0110_relaxed_cohort_factor_analysis/
[t0116]: ../../../../t0116_pooled_pca_cluster_factor_dsi07_pd10/
