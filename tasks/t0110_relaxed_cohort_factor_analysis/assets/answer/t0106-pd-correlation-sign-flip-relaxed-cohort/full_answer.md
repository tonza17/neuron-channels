---
spec_version: "2"
answer_id: "t0106-pd-correlation-sign-flip-relaxed-cohort"
answered_by_task: "t0110_relaxed_cohort_factor_analysis"
date_answered: "2026-05-18"
confidence: "high"
---

# All-negative PD column is a truncated-cohort artifact

## Question

Does t0108's all-negative PD-rate factor-correlation column persist if we re-run the same
varimax factor analysis on a less-truncated cohort, or is it a cohort-selection artifact?

## Short Answer

It is a truncated-cohort artifact. Re-running the same varimax FA pipeline on 247 t0106 cells
at DSI > 0.2 AND PD > 3 Hz produces 2 of 10 factors with positive r(PD) (F2 +0.136 at p=0.033,
F4 +0.048 n.s.). DSI sign distribution flips from 4 / 6 to 6 / 4. F1 — the dominant axis in
both cohorts — is reinterpreted: t0108 reported it as a PD-only dropper because the DSI
ceiling masked the DSI effect, but at the relaxed threshold it is the joint failure axis
(r_DSI = −0.37, r_PD = −0.75). F2 identifies "more persistent sodium → more firing" as a real
PD-positive direction the strict cohort hid.

## Research Process

The hypothesis: t0108's all-negative PD column (0 of 10 PD correlations above zero) is an
effect of selecting cells in the top corner of the DSI/PD space (DSI > 0.5 AND PD > 10).
Within that already-good cohort, every structured residual variation tends to push cells away
from the ceiling, so factors mostly align with "decreasing" directions.

The test: re-run the same FA pipeline on a less-truncated cohort. If the hypothesis holds,
some PD correlations should flip positive. If the hypothesis fails (all PD correlations remain
negative even at the looser threshold), the pattern reflects a real structural property of the
optimisation space rather than cohort selection.

Cohort design: t0106 cells passing DSI > 0.2 AND PD > 3 — chosen because (a) it is the
threshold the operator suggested, (b) it gives 247 unique cells (65 % more than t0108), and
(c) it is a known threshold from t0105's design space, allowing cross-task interpretation.

Pipeline: identical to t0108 — sklearn FactorAnalysis with no built-in rotation, plus the
manual Kaiser varimax routine in t0108's `code/factor_analysis.py` (imported by absolute
path). Factor count by Kaiser eigenvalues > 1 capped at 10. Factor scores via the regression
method `Z * Λ * (Λᵀ Λ)⁻¹`. Pearson correlations via `scipy.stats.pearsonr`.

## Evidence from Papers

No paper-based evidence was used. This question is answered by direct re-analysis of t0106
optimisation output under a different cohort filter.

## Evidence from Internet Sources

No external internet sources were used.

## Evidence from Code or Experiments

Source data: `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`.

Cohort construction:

| Filter | N raw | N passing | N unique |
| --- | --- | --- | --- |
| DSI > 0.5 AND PD > 10 (t0108) | 3,744 | 784 | 150 |
| DSI > 0.2 AND PD > 3 (this task) | 3,744 | 1,209 | **247** |

t0110 factor-correlation table (10 factors):

| Factor | r(DSI) | p(DSI) | r(PD) | p(PD) |
| --- | --- | --- | --- | --- |
| F1 | −0.370 | 2.1e-09 | **−0.754** | 1.5e-46 |
| F2 | +0.042 | 0.51 | **+0.136** | 0.033 |
| F3 | +0.006 | 0.93 | −0.148 | 0.020 |
| F4 | +0.018 | 0.78 | **+0.048** | 0.45 |
| F5 | +0.292 | 2.9e-06 | −0.101 | 0.11 |
| F6 | −0.117 | 0.067 | −0.184 | 3.8e-03 |
| F7 | −0.173 | 6.4e-03 | −0.009 | 0.89 |
| F8 | +0.168 | 8.2e-03 | −0.088 | 0.17 |
| F9 | +0.036 | 0.57 | −0.110 | 0.086 |
| F10 | −0.122 | 0.055 | −0.235 | 1.9e-04 |

Sign counts:
* **DSI**: 6 positive, 4 negative (t0108: 4 positive, 6 negative).
* **PD**: **2 positive** (F2 +0.136 significant at p=0.033, F4 +0.048 not significant),
  **8 negative** (t0108: 0 positive, 10 negative).

Joint factors (|r_DSI| > 0.3 AND |r_PD| > 0.3): **F1** in t0110 — the joint failure axis,
r_DSI = −0.37, r_PD = −0.75. Both signs negative, in contrast to t0108's F10 which had
opposite signs (r_DSI = +0.31, r_PD = −0.45, the trade-off axis).

Top-5 loadings for the two newly PD-positive factors:

* **F2** (r_PD = +0.136, p = 0.033): BK_PRIMARY −0.74, MG_CONC −0.73, NAP_PRIMARY +0.69,
  NAP_SOMA +0.63, AIS_DIAMETER +0.61.
* **F4** (r_PD = +0.048, p = 0.45): NAV16_MID −0.76, mean_branching_angle +0.69, KV3_AIS −0.65,
  soma_diameter +0.59, KV3_PRIMARY +0.48.

F1's top loadings (the dominant axis in both cohorts) in t0110: NAP_MID +0.94, CAT +0.89,
SK_MID +0.86, CAD_TAUR +0.85, RA_OHM_CM +0.78. Same loading family as t0108's F1
(SK_TERMINAL +0.94, SK_MID +0.88, CAT +0.87, NAV16_AIS −0.84, NAP_MID +0.80) — the "K-Ca /
persistent-Na / low-axonal-Na / high RA / high Ca buffer" combination. What changes between
cohorts is the sign on r(DSI), not the loading structure.

The comparison chart `results/images/factor_correlations_comparison.png` shows both panels
side-by-side at the same y-axis scale: in the left panel (t0108 strict) all 10 orange bars
fall below zero; in the right panel (t0110 relaxed) the F2 and F4 orange bars sit above zero.

## Synthesis

The truncated-cohort hypothesis is confirmed. Three substantive findings:

1. **The all-negative PD column is a cohort selection artifact.** Within a population already
   filtered to the top of the PD distribution, no factor can align with "go higher in PD"
   because there is no headroom. Relaxing the filter restores at least one significant
   PD-positive direction (F2 at p=0.033).

2. **F1 is the joint failure axis, not a PD-only dropper.** t0108 reported F1 (high
   SK_TERMINAL / SK_MID / CAT / NAP_MID, low NAV16_AIS) as a PD-only dropper because
   r_DSI(F1) ≈ 0 in the strict cohort. The same loading structure in t0110 gives
   r_DSI = −0.37 and r_PD = −0.75: moving along F1 collapses both objectives. The DSI ceiling
   in the strict cohort hid the DSI cost.

3. **F2 identifies "persistent-Na excitability → more firing" as a real positive PD axis.**
   The loadings — high NAP_PRIMARY / NAP_SOMA / AIS_DIAMETER, low MG_CONC / low BK_PRIMARY —
   describe a coherent biological direction: more persistent sodium, reduced NMDA Mg-block,
   reduced primary-dendrite BK braking. F2's appearance only at the relaxed threshold suggests
   this is the path the optimiser used to push cells from low-PD into the strict-cohort regime
   in the first place; once cells are already in the high-PD corner, F2 saturates and reads as
   neutral.

The t0108 trade-off axis F10 (DSI +0.31 / PD −0.45) has no direct analogue in t0110 at the
|r| > 0.3 cut. The closest neighbour is t0110 F5 (DSI +0.29 / PD −0.10) with similar but not
identical loadings. This is consistent with t0108's F10 being a *corner-specific* trade-off
direction that emerges only in the truncated population.

The practical lesson for the project: any factor analysis on optimiser output must declare
its filter explicitly, because factor sign patterns reflect cohort selection as much as
parameter structure. t0108's headline interpretation of F1 as "the PD-dropping axis" should
be amended to "the joint failure axis"; t0108's F10 trade-off direction stands but is
cohort-specific.

## Limitations

* N=247 with 68 features is comfortable but bootstrap stability of loadings was not run.
* Varimax enforces orthogonality; oblique rotations may yield more interpretable factors.
* The Kaiser cap leaves 6 Kaiser-eligible factors (eigenvalues 11-16) unmodelled.
* Factor identities across cohorts are rotation-dependent; "F1 in t0108 matches F1 in t0110"
  is judged by loading overlap, not factor index.
* The cohort still excludes silenced cells; a full-population FA (DSI > 0.0 AND PD > 0.0, 930
  unique cells) would test the limit case and is recommended as a follow-up.
* F4's PD-positive correlation (+0.048) is not significant (p = 0.45); only F2 (+0.136 at
  p = 0.033) is a confident sign-flip.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — source cells.
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — strict-cohort comparison baseline.
* Task: `t0110_relaxed_cohort_factor_analysis` — this task.
* Result data: `tasks/t0110_relaxed_cohort_factor_analysis/results/data/
  factor_analysis_relaxed.json`.
* Visualisations: `results/images/factor_correlations_comparison.png` (side-by-side bar chart
  vs t0108), `results/images/factor_loadings_heatmap_relaxed.png`.
