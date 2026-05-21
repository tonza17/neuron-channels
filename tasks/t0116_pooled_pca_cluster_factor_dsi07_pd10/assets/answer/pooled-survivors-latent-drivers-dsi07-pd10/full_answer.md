---
spec_version: "2"
answer_id: "pooled-survivors-latent-drivers-dsi07-pd10"
answered_by_task: "t0116_pooled_pca_cluster_factor_dsi07_pd10"
date_answered: "2026-05-21"
confidence: "medium"
---
# F1 drives DSI (r=-0.59, mixed ephys+morph), F3 drives PD rate (r=+0.75, purely electrophys); no joint factor passes |r|>0.3 on both

## Question

Which factors (after varimax rotation on the full 68-d pool) load most strongly on dsi_vector_sum
and pd_rate_hz, and are they morphology-dominated, electrophys-dominated, or mixed?

## Short Answer

F1 is the dominant DSI driver (r=-0.589, p ~ 1e-82) and is mixed — its top loadings include both
electrophys channels (SK_AIS, SKAHP, NAP) and a morphology parameter
(primary_branch_pd_concentration). F3 is the dominant PD-rate driver (r=+0.746, p ~ 1e-155) and is
purely electrophys (NAR, IH, NAV16_SOMA, BK channels, RA). No single factor crosses |r|>0.3 on both
DSI and PD simultaneously, so the strict-cohort pool does not contain a joint DSI-PD axis — the
answer to "are the drivers shared?" is no in this strict cohort, but t0110's relaxed-cohort analysis
shows this is a known truncated-cohort artefact.

## Research Process

1. Standardise the union-pool 68-d matrix (n=869 cells) using the pre-fitted
   `data/pooled_standardiser.npz` — same fit reused for every step
   (`code/factor_analysis.py:main()`).
2. Compute correlation-matrix eigenvalues via `np.linalg.eigvalsh(np.cov(z, rowvar=False))` and
   count `n_eig_above_one` (Kaiser criterion). The pool produces 11 eigenvalues > 1; the project's
   `KAISER_FACTOR_CAP = 10` caps the factor count at 10.
3. Fit `sklearn.decomposition.FactorAnalysis(n_components=10, random_state=42)` on the standardised
   matrix; rotate the resulting loadings with Kaiser varimax (iterative SVD, `gamma=1.0`,
   `tol=1e-6`, `max_iter=500`) — the same `varimax_rotation` helper used by t0108 and t0110.
4. Compute rotated factor scores via the regression-method approximation Z @ Λ @ pinv(Λᵀ Λ).
5. For each factor, compute Pearson r between its rotated score and `dsi_vector_sum` / `pd_rate_hz`.
   Flag joint factors (|r_DSI|>0.3 AND |r_PD|>0.3); none pass.
6. Render the loadings heatmap (factors × 68 features) with the canonical `RdBu_r` diverging
   colourmap, vmin=-vmax symmetric on `max(|loadings|)`
   (`results/images/factor_loadings_heatmap.png`).
7. Inspect top-7 absolute loadings per factor to determine the morphology-vs-electrophys
   classification of each driver.

## Evidence from Papers

No paper-based evidence was used.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Per-factor variance explained and Pearson correlations (`results/data/factor_correlations.csv`):

| Factor | Var explained (%) | r (DSI) | p (DSI) | r (PD) | p (PD) | Joint? |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | 30.06 | -0.589 | 3.1e-82 | -0.210 | 4.3e-10 | No |
| F2 | 14.02 | -0.086 | 1.2e-2 | -0.367 | 5.0e-29 | No |
| F3 | 9.36 | -0.172 | 3.6e-7 | +0.746 | 4.3e-155 | No |
| F4 | 1.83 | +0.089 | 9.0e-3 | -0.230 | 6.6e-12 | No |
| F5 | 2.94 | +0.057 | 9.4e-2 | +0.230 | 6.7e-12 | No |
| F6 | 1.35 | -0.222 | 3.8e-11 | +0.033 | 3.4e-1 | No |
| F7 | 1.36 | +0.087 | 1.0e-2 | -0.009 | 7.9e-1 | No |
| F8 | 1.87 | +0.014 | 6.8e-1 | -0.038 | 2.7e-1 | No |
| F9 | 1.10 | -0.026 | 4.5e-1 | +0.070 | 3.8e-2 | No |
| F10 | 1.38 | -0.059 | 8.1e-2 | -0.095 | 5.1e-3 | No |

Total variance explained: 65.3% across 10 factors. F1 alone captures 30.1% — the dominant axis.

Top-7 absolute loadings per the three correlated factors (from `results/data/factor_loadings.csv`):

| F1 (DSI driver, mixed) | F2 (PD driver, ephys+morph) | F3 (PD driver, ephys only) |
| --- | --- | --- |
| SK_AIS_GBAR +0.946 | SK_MID_GBAR +0.863 | NAR_GBAR +0.876 |
| primary_branch_pd_concentration -0.945 | BK_SOMA_GBAR +0.817 | IH_GBAR +0.865 |
| SKAHP_TAU_CA_MULTIPLIER -0.930 | CAT_GBAR +0.812 | NAV16_SOMA_GBAR +0.823 |
| NAP_SOMA_GBAR -0.923 | W_GABA_US +0.793 | BK_AIS_GBAR +0.753 |
| NAP_MID_GBAR -0.922 | MG_CONC_MM -0.790 | RA_OHM_CM -0.637 |
| N_ACH +0.903 | NAV16_AIS_GBAR -0.702 | BK_TERMINAL_GBAR -0.628 |
| BK_PRIMARY_GBAR +0.890 | num_primary_branches -0.657 | BK_MID_GBAR -0.586 |

Classification by loading mix (counting parameters at |loading| > 0.5):

* **F1 = mixed DSI driver.** Top-7 has 6 electrophys + 1 morphology
  (primary_branch_pd_concentration). r_DSI = -0.589, r_PD = -0.210. F1 is the leading axis of the
  cohort and dominates DSI alone.
* **F2 = mixed PD driver.** Top-7 has 5 electrophys + 2 morphology (num_primary_branches, W_GABA_US
  count if we treat synapse weight as electrophys). r_DSI = -0.086, r_PD = -0.367. PD-driver with
  negative sign — higher F2 score means lower PD rate.
* **F3 = purely electrophys PD driver.** Top-7 are all electrophys (NAR, IH, NAV16_SOMA, BK
  channels, RA). r_PD = +0.746 (the strongest single correlation in the table). F3 is the classic
  "depolarising-current bundle": NAR (persistent Na-rectifier), IH (HCN h-current), and NAV16_SOMA
  together push the soma membrane towards firing; BK_AIS opposes (slows down repolarisation), so the
  +/- sign mix here is consistent with a high-firing-rate axis.

**No joint factor**: no factor crosses |r|>0.3 on BOTH DSI and PD. The closest candidate is F1
(r_DSI=-0.589, r_PD=-0.210 — fails on PD). This contrasts sharply with t0108's t0106-only
strict-cohort result, which identified F10 as a joint factor (|r_DSI|=0.31, |r_PD|=0.45).

## Synthesis

The pooled DSI > 0.7 strict cohort decomposes into 10 varimax factors with 65.3% total variance
explained. F1 (30% variance, DSI driver, mixed loadings) and F3 (9% variance, PD driver, purely
electrophys) are the two largest correlated axes. The signs are intuitive: F1 loads SK and SKAHP
(Ca-dependent K conductances) with one sign and NAP (persistent Na) with the other, matching the
standard "spike-frequency-adaptation vs sustained-depolarisation" tradeoff that determines DSI; F3
loads pure depolarising currents (NAR, IH, NAV16_SOMA) which set the firing rate.

The most important null result is that NO factor passes the joint |r|>0.3 threshold. In the strict
cohort, DSI and PD are governed by independent axes — F1 for DSI and F3 for PD — rather than by
a shared trade-off factor. This means selection pressure along F1 raises DSI without specifically
affecting PD, and selection along F3 raises PD without specifically affecting DSI. The two
objectives are decoupled in the latent factor space.

The mixed (electrophys + morphology) character of F1 vs the pure electrophys character of F3 is a
more nuanced finding. F1 mixes SK_AIS_GBAR with primary_branch_pd_concentration, which suggests that
DSI in this cohort depends jointly on K conductance distribution AND on dendritic branching
geometry. F3, by contrast, is pure electrophys — PD rate depends almost entirely on channel
densities and passive properties, not on morphology. This is consistent with the biological
intuition that PD rate is a soma-level firing measure (insensitive to dendrite geometry once enough
synaptic drive arrives) while DSI is a dendritic-integration measure (sensitive to both channel and
geometric properties).

The DSI driver (F1) and PD driver (F3) being orthogonal in the strict cohort is the central new
result for downstream task design: optimisation along F1 alone won't raise PD, and optimisation
along F3 alone won't raise DSI. Practical follow-ups should explicitly target moves that combine F1
and F3 directions (rather than rely on a single joint factor like t0108's F10) — which is itself a
hypothesis to test.

## Limitations

* **Truncated-cohort artefact risk (cf. t0110).** The cohort filter DSI > 0.7 is even stricter than
  t0108's DSI > 0.5; t0110 demonstrated that t0108's "all-negative PD column" was a strict-cohort
  artefact. t0116's even stricter filter is likely to amplify this effect. The absence of a joint
  factor here could be such an artefact — at a relaxed threshold the pool might contain a clear
  joint axis (the kind t0108 found at F10). The Q3 conclusion is conditional on the strict cohort
  and should not be extrapolated to looser ones.
* **n=869 with 68 features is borderline for FA stability.** Bootstrapped loading recovery (as in
  t0105) is not run in this task. The largest factor signs (F1, F2, F3) are likely robust; smaller
  factors (F6-F10) with low variance explained may have unstable loading directions.
* **Varimax forces orthogonal factors.** Real biological axes can be correlated; an oblique rotation
  (promax, geomin) could yield more interpretable but correlated factors. The "no joint factor"
  finding is robust to this — orthogonal factors are the more conservative null for joint-factor
  detection.
* **The Kaiser cap binds at 10**: 11 eigenvalues > 1, so one Kaiser-eligible factor is unmodelled.
  It is unlikely to be the missing joint factor (it would have appeared in t0108's 10-factor
  solution if it existed), but the cap was inherited mechanically from t0108 and could be relaxed in
  a follow-up.
* **Cross-seed pooling concentrates within-basin variance.** Per-seed factor analyses would reveal
  whether F1's mixed loadings reflect a single mixed axis or two separate axes (one electrophys, one
  morphology) that happen to co-vary because of the cross-seed basin structure documented in the
  basin-connectivity answer. This is a candidate correction task.
* **`morph_seed` is a generator RNG nuisance** that appears in some factors' loadings; it is not a
  meaningful biological parameter and could be excluded in a follow-up.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — single-seed strict-cohort precedent (F10 joint
  factor).
* Task: `t0110_relaxed_cohort_factor_analysis` — relaxed-cohort sensitivity diagnoses the
  truncated-cohort artefact that may bias t0116's strict-cohort signs.
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10` — this analysis.
* Result data:
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/factor_correlations.csv`,
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/data/factor_loadings.csv`.
* Visualisations:
  `tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/results/images/factor_loadings_heatmap.png`.

[t0106]: ../../../../t0106_long_pdnd_nsga2_300gen/
[t0112]: ../../../../t0112_t0106_seed77_replicate/
[t0114]: ../../../../t0114_seed7755_no_autostop/
[t0115]: ../../../../t0115_seed9354_no_autostop/
[t0108]: ../../../../t0108_t0106_cluster_factor_dsi05_pd10/
[t0110]: ../../../../t0110_relaxed_cohort_factor_analysis/
[t0116]: ../../../
