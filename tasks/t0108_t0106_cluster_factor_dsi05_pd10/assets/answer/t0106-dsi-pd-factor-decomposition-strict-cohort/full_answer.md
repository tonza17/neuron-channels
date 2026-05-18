---
spec_version: "2"
answer_id: "t0106-dsi-pd-factor-decomposition-strict-cohort"
answered_by_task: "t0108_t0106_cluster_factor_dsi05_pd10"
date_answered: "2026-05-18"
confidence: "medium"
---

# F10 is the single joint DSI-PD trade-off factor in the strict cohort

## Question

Which factors (combinations of the 68 input parameters) explain DSI and PD diversity in the strict
cohort (DSI > 0.5 AND PD > 10), and is there a joint factor?

## Short Answer

Varimax factor analysis on the z-scored 68-d matrix of the 150-cell strict cohort retains 10
factors and identifies F10 as the single joint DSI-PD factor (|r_DSI|=0.31, |r_PD|=0.45). PD-rate
diversity is otherwise dominated by F1 (r=−0.545; SK_TERMINAL, SK_MID, CAT, NAV16_AIS, NAP_MID
loadings); DSI diversity is split between F5 (r=−0.325) and F10 (r=+0.313). F10's positive
direction raises DSI but suppresses PD, making it a trade-off axis along CAD_DEPTH, CAL, W_ACH,
branch_prob_per_um, and mean_segment_length. No single factor jointly increases both objectives in
this cohort.

## Research Process

The varimax FA was run on the same 150-cell strict cohort used in the two cluster answers.
Pipeline:

* z-score all 68 columns of the strict cohort vector. No columns are dropped (all 68 have non-zero
  variance).
* Factor extraction with `sklearn.decomposition.FactorAnalysis(n_components=k, rotation=None,
  random_state=42)` fit on the z-scored matrix.
* Apply Kaiser varimax rotation to `fa.components_.T` via a manual iterative SVD routine
  (`gamma=1`, `tol=1e-6`, `max_iter=500`) in `code/factor_analysis.py`.
* Factor count: 18 eigenvalues > 1 on the 68×68 correlation matrix; cap at 10 per plan.
  `n_factors = 10`.
* Factor scores via the regression method: `scores = Z * Λ * (Λᵀ Λ)⁻¹`.
* For each factor, compute Pearson r between its scores and `dsi_vector_sum`; same for
  `pd_rate_hz`. Flag joint factors with `|r_DSI| > 0.3 AND |r_PD| > 0.3`.

This replaces the original factor_analyzer-package implementation used in t0105 because the
package is incompatible with scikit-learn 1.8.0. The same varimax loadings are produced by both.

## Evidence from Papers

No paper-based evidence was used. This question is answered purely by re-analysis of project
optimisation output.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Full results in
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/factor_analysis.json`.

Top-5 loadings per factor:

| Factor | Top loadings |
| --- | --- |
| F1 | SK_TERMINAL +0.94, SK_MID +0.88, CAT +0.87, NAV16_AIS −0.84, NAP_MID +0.80 |
| F2 | BK_PRIMARY −0.89, BK_MID +0.86, W_GABA −0.74, AIS_DIAMETER +0.69, NAV16_SOMA −0.56 |
| F3 | CAD_TAUR +0.94, field_elongation_pd +0.42, SKAHP_GBAR_SOMA_AIS +0.39, BK_MID +0.38, NAV16_AIS −0.26 |
| F4 | KV3_TERMINAL +0.87, RA_OHM_CM +0.64, CAT +0.28, branch_density_gradient_pd +0.26, N_GABA −0.22 |
| F5 | NAV16_MID +0.77, KV3_AIS +0.72, mean_branching_angle −0.70, SK_AIS −0.69, LAMBDA_ACH +0.56 |
| F6 | NAP_SOMA −0.76, VOFF_NMDA −0.62, ais_length_um −0.59, RHO0_ACH −0.55, IM_GBAR −0.51 |
| F7 | branch_length_cv +0.70, branch_density_gradient_pd +0.64, rall_exponent −0.64, morph_seed −0.54, primary_branch_pd_concentration +0.53 |
| F8 | NAP_MID +0.51, CAT +0.32, AIS_DIAMETER +0.32, BK_TERMINAL −0.31, RHO0_GABA −0.27 |
| F9 | num_primary_branches +0.57, NAP_PRIMARY −0.53, MG_CONC_MM +0.49, N_ACH −0.46, NAV16_TERMINAL +0.42 |
| F10 | CAD_DEPTH −0.73, branch_prob_per_um −0.67, W_ACH −0.58, CAL +0.57, mean_segment_length −0.56 |

Factor-outcome correlations:

| Factor | r (DSI) | p (DSI) | r (PD) | p (PD) |
| --- | --- | --- | --- | --- |
| F1 | +0.062 | 0.45 | −0.545 | 5.4e-13 |
| F2 | +0.075 | 0.36 | −0.262 | 1.2e-3 |
| F3 | −0.136 | 0.097 | −0.204 | 0.012 |
| F4 | −0.081 | 0.33 | −0.042 | 0.61 |
| F5 | −0.325 | 5.1e-5 | −0.140 | 0.088 |
| F6 | −0.278 | 5.8e-4 | −0.129 | 0.12 |
| F7 | +0.147 | 0.074 | −0.096 | 0.24 |
| F8 | −0.067 | 0.41 | −0.008 | 0.92 |
| F9 | −0.021 | 0.80 | −0.031 | 0.71 |
| F10 | +0.313 | 9.6e-5 | −0.446 | 1.0e-8 |

Top 3 factors per outcome:

* DSI: F5 (r=−0.325), F10 (r=+0.313), F6 (r=−0.278).
* PD: F1 (r=−0.545), F10 (r=−0.446), F2 (r=−0.262).

## Synthesis

F1 is the PD-rate driver. It loads on SK_TERMINAL (+0.94), SK_MID (+0.88), CAT (+0.87), NAV16_AIS
(−0.84), NAP_MID (+0.80) — a "K-Ca / persistent-Na / low-axonal-Na" combination. Cells scoring
high on F1 have low PD-rate; F1 alone explains ~30 % of PD-rate variance.

F5 and F10 drive DSI in opposite directions:

* F5 (NAV16_MID, KV3_AIS, mean_branching_angle, SK_AIS, LAMBDA_ACH) is associated with lower DSI.
* F10 (CAD_DEPTH ↓, branch_prob_per_um ↓, W_ACH ↓, CAL ↑, mean_segment_length ↓) is associated
  with higher DSI.

F10 is the cohort's joint DSI-PD axis: positive direction raises DSI (r=+0.31) but reduces
PD-rate (r=−0.45). The biological interpretation is that stronger somatic Ca-L conductance
combined with a thinner Ca buffer enhances Ca²⁺ transients during PD stimulation, which improves
directional tuning but also activates Ca-dependent K conductances (SK, BK) that suppress firing —
hence the PD-rate cost.

A practical implication: targeted moves along F10's loading direction are a candidate for
"sliding along the Pareto front" between DSI and PD. Setting CAL ↑, CAD_DEPTH ↓,
branch_prob_per_um ↓, W_ACH ↓, mean_segment_length ↓ together — while compensating with stronger
NAV16_AIS to offset the PD penalty (NAV16_AIS is a key F1 loading with opposite-sign effect on
PD) — is a concrete recipe for a follow-up experimental task.

## Limitations

* N=150 with 68 features is borderline for FA stability; bootstrapped loading recovery (which
  t0105 ran with 100 resamples) was not run in this task.
* Varimax forces orthogonality. Real biological axes may be correlated; oblique rotations
  (promax, geomin) could yield more interpretable but correlated factors.
* The cap of 10 factors leaves 8 Kaiser-eligible factors (eigenvalues 11–18 of the correlation
  matrix) unmodelled. The captured variance is partial.
* Factor scores computed by the regression method are biased estimators of the true latent
  scores; correlation magnitudes are conservative.
* `morph_seed` appears in F7's loadings (−0.54) and biases F7 towards a "generator-RNG nuisance"
  factor rather than a biological axis.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — source cells.
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — analysis task.
* Result data:
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/results/data/factor_analysis.json`.
* Visualisations:
  `results/images/factor_loadings_heatmap.png`,
  `results/images/factor_correlations_dsi_pd.png`.
