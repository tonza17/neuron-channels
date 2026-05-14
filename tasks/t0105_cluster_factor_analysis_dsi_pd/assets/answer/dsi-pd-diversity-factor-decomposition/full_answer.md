---
spec_version: "2"
answer_id: "dsi-pd-diversity-factor-decomposition"
answered_by_task: "t0105_cluster_factor_analysis_dsi_pd"
date_answered: "2026-05-14"
confidence: "medium"
---
# Factor decomposition of DSI vs PD diversity

## Question

Which factors (combinations of the 68 input parameters) explain DSI diversity versus PD diversity,
and is there a joint factor or are the two outcomes orthogonal?

## Short Answer

The two outcomes are mostly orthogonal but partially coupled through one near-joint factor: a
varimax factor analysis on the standardised 68-d matrix (N=85, 10 factors by Kaiser criterion capped
at 10) finds F1 the only factor exceeding |r| = 0.25 on either outcome, with r_DSI = -0.322
(p=0.003) and r_PD = -0.265 (p=0.014). No factor crosses the joint-factor threshold |r| > 0.3 on
both, so the joint high-DSI / high-PD corner is not unlocked by a single low-d axis. F1's top
loadings (NAP_PRIMARY, SK_MID, MG_CONC_MM, RA_OHM_CM) are bootstrap-stable across 200 resamples, but
F3 through F10 are not. The substrate-limited reading from t0102 and t0104 is reinforced: DSI and PD
share a weak common axis but remain substantially orthogonal.

## Research Process

The 85-cell primary cohort (DSI > 0.1 AND PD > 2 Hz, deduped across t0091/t0099/t0102/t0104,
post-silence-filter) was z-scored column-wise across the full 68-d parameter vector. The factor
count was chosen by the Kaiser criterion (eigenvalues > 1 on the correlation matrix), capped at 10
per `constants.KAISER_FACTOR_CAP`; 18 eigenvalues passed Kaiser, so the cap applied. Varimax
rotation was applied via
`factor_analyzer.FactorAnalyzer(rotation="varimax", n_factors=10, method="minres")`. A compatibility
shim re-aliases `force_all_finite` (removed in scikit-learn 1.6) to `ensure_all_finite` so
factor_analyzer 0.5.1 runs on sklearn 1.8.

Per-cell factor scores were derived via `FactorAnalyzer.transform`. Pearson r and p-values between
each factor score column and the two outcomes (`dsi_vector_sum`, `pd_rate_hz`) were computed with
`scipy.stats.pearsonr`. The joint-factor flag is triggered when |r_DSI| > 0.3 AND |r_PD| > 0.3; no
factor reached that bar in the primary cohort.

Stability was tested by bootstrap (200 resamples; `numpy.random.default_rng(seed=42)`). For each
resample we draw N=85 cells with replacement, refit the 10-factor varimax solution, align the
resampled loadings to the headline via the greedy max-|dot| matching with sign flips
(`code/factor_bootstrap.py:_align_loadings`), and record the aligned loading matrix. Per-cell 95 %
CIs are percentile (2.5 % / 97.5 %). A factor is flagged `stable` when its top-5 loadings retain
consistent signs in >= 90 % of resamples AND each median absolute loading exceeds 0.4. F1 and F2
cleared both thresholds; F3-F10 did not.

The strict cohort (DSI > 0.2 AND PD > 3 Hz, N=30) re-ran the same pipeline with separate outputs at
`results/data/factor_loadings_strict.json` and `results/data/factor_correlations_strict.json`. At
that sample size F1 still emerges as a correlate but the top-3 factors per outcome reshuffle (F6
takes the top correlation slot with PD at r = +0.36), reflecting the much smaller N / p ratio.

## Evidence from Papers

This method does not use the `papers` answer method; no specific paper assets were re-read for this
question. Selection of varimax over an oblique rotation followed standard practice documented in
psychometric factor-analysis literature (see `research/research_code.md`).

## Evidence from Internet Sources

This method does not use the `internet` answer method; no external URLs were consulted during
synthesis. The factor_analyzer/scikit-learn compatibility shim was developed locally and is
documented in `code/factor_analysis.py`.

## Evidence from Code or Experiments

Headline factor-vs-outcome correlations (primary cohort, N=85, 10 factors):

| Factor | r_DSI | p_DSI | r_PD | p_PD | Stable? |
| --- | --- | --- | --- | --- | --- |
| F1 | -0.322 | 0.003 | -0.265 | 0.014 | yes |
| F2 | -0.128 | 0.243 | -0.135 | 0.219 | yes |
| F3 | -0.167 | 0.128 | -0.161 | 0.140 | no |
| F4 | -0.109 | 0.322 | -0.061 | 0.579 | no |
| F5 | -0.136 | 0.215 | -0.098 | 0.370 | no |
| F6 | -0.026 | 0.815 | -0.073 | 0.509 | no |
| F7 | +0.107 | 0.330 | -0.107 | 0.330 | no |
| F8 | -0.058 | 0.596 | +0.052 | 0.639 | no |
| F9 | -0.111 | 0.312 | -0.044 | 0.687 | no |
| F10 | -0.114 | 0.298 | -0.142 | 0.196 | no |

Top-3 factors per outcome (primary):

* DSI: F1 (-0.322), F3 (-0.167), F5 (-0.136)
* PD: F1 (-0.265), F3 (-0.161), F10 (-0.142)

F1 is the strongest correlate for both outcomes, but the magnitudes (|r_DSI| = 0.32, |r_PD| = 0.27)
sit on opposite sides of the joint-factor threshold (0.3). Joint-factor count is 0.

F1 top-5 loadings (headline solution; bootstrap-stable):

| Param index | Param | Headline loading | Bootstrap median |
| --- | --- | --- | --- |
| 11 | NAP_PRIMARY_GBAR | +0.747 | (see results/data/factor_bootstrap.json) |
| 66 | morph_seed | +0.680 |  |
| 22 | SK_MID_GBAR | +0.662 |  |
| 50 | MG_CONC_MM | +0.654 |  |
| 34 | RA_OHM_CM | +0.652 |  |

F2 top-5 loadings:

| Param | Headline loading |
| --- | --- |
| SK_PRIMARY_GBAR | +0.708 |
| NAV16_TERMINAL_GBAR | -0.626 |
| NAV16_SOMA_GBAR | +0.583 |
| max_strahler_depth | -0.576 |
| IM_GBAR | -0.538 |

Strict-cohort comparison (N=30):

| Factor | r_DSI | r_PD |
| --- | --- | --- |
| F1 (strict) | +0.135 | -0.234 |
| F6 (strict) | -0.170 | +0.364 |

The strict-cohort reordering is consistent with low statistical power (N=30, 68 dims) and should be
read as a sensitivity check rather than an independent estimate.

## Synthesis

The factor decomposition produces a clear primary axis (F1) that aligns with both DSI and PD in the
same sign direction (negative correlation; cells higher in this axis tend to be lower in both DSI
and PD). F1 loads heavily on primary-dendrite persistent Na (NAP_PRIMARY) plus mid-dendrite SK and
synaptic / passive parameters (MG_CONC_MM, RA_OHM_CM). The morph_seed loading is a procedural
artefact: it is an integer-coded seed used to seed morphology generation and not a physically
meaningful parameter, so its inclusion in F1's top-5 should be discounted when interpreting biology.

Crucially, no factor crosses |r| > 0.3 on *both* outcomes. This means the 68-d substrate as
empirically explored by NSGA-II does not contain a single linear axis that simultaneously maximises
DSI and PD-rate. The substrate-limited reading from t0102 / t0104 — that the joint high-DSI /
high-PD corner is hard to reach because DSI demands distal-dendrite shunting and PD demands strong
somatic / AIS spike generation — is reinforced: the factor structure is near-orthogonal between
the two outcomes.

The bootstrap stability check tightens the interpretation: only F1 and F2 are reproducible across
resamples. The remaining 8 factors capture residual variance whose sign and magnitude flip between
resamples, so they should not be interpreted as biological mechanisms.

Confidence is `medium` because (a) N=85 vs p=68 gives a ratio of 1.25, well below the psychometric
rule of thumb (5-10:1); (b) the strict-cohort sensitivity at N=30 reshuffles the factor ordering,
which would be expected with low power but also flags that the 10-factor solution is at the edge of
stability; (c) factor_analyzer 0.5.1 lacks built-in fit statistics (BIC, RMSEA) so we cannot
quantitatively rank rotations.

## Limitations

* N=85 / 68 dimensions is below the standard 5:1 ratio for factor analysis; F3-F10 should not be
  relied on for biological interpretation.
* Two of the 14 morphology dims (`num_primary_branches`, `max_strahler_depth`, `morph_seed`) are
  integer-coded. `morph_seed` in particular is purely indexical and its appearance in F1's top
  loadings should be discounted.
* The strict cohort (N=30) is too small for a stable factor decomposition; its rerun is documented
  but should be read as exploratory.
* No mediation analysis between PCA (54-d electrophys) and FA (68-d full): we report the two
  decompositions side by side without quantifying overlap. A targeted follow-up could fit a
  hierarchical model where electrophys PCs are nested within asymmetry class.
* Pearson r is sensitive to linear relationships only; a non-monotonic factor would be missed by
  this design.

## Sources

* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0099_random_init_pareto_robustness`
* Task: `t0102_seedscale_n4_gen20`
* Task: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_loadings.png`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_correlations.png`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/factor_loadings_bootstrap.png`
* Data: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/factor_loadings.json`
* Data: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/factor_correlations.json`
* Data: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/factor_bootstrap.json`

[t0091]: ../../../../t0091_morphology_extended_nsga2_v1/
[t0099]: ../../../../t0099_random_init_pareto_robustness/
[t0102]: ../../../../t0102_seedscale_n4_gen20/
[t0104]: ../../../../t0104_nsga2_2obj_dsi_pdrate_3seeds/
