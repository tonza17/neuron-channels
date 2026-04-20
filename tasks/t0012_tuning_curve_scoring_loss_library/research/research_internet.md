---
spec_version: "1"
task_id: "t0012_tuning_curve_scoring_loss_library"
research_stage: "internet"
searches_conducted: 8
sources_cited: 10
papers_discovered: 2
date_completed: "2026-04-20"
status: "complete"
---
## Task Objective

Design and build a pure-Python library `tuning_curve_loss` that scores a simulated DSGC tuning curve
(firing rate vs. stimulus angle) against the canonical target established by
`t0004_generate_target_tuning_curve`. The library must expose a single `score()` entry point that
returns a frozen `ScoreReport` with weighted-Euclidean scalar loss, DSI/peak/null/HWHM residuals,
per-metric pass booleans for the t0002 envelope (DSI 0.7-0.85, peak 40-80 Hz, null < 10 Hz, HWHM
60-90°), trial-to-trial reliability, and overall `passes_envelope`. It must also expose per-metric
helpers, a CLI, and a tuning-curve CSV schema `(angle_deg, trial_seed, firing_rate_hz)`. Internet
research must establish the canonical conventions so that every downstream optimisation task shares
one scorer.

## Gaps Addressed

Because `research-papers` is skipped for this task (the paper corpus already covers DSGC scoring via
the t0002 literature survey; see the t0006 brainstorm results), there is no dedicated
`research_papers.md` for this task. The gaps treated here instead come from the
`task_description.md` *Questions the task answers* list and from the t0006 brainstorm's merge of
S-0002-09 and S-0004-03:

1. **Canonical DSI formula for DSGCs** — **Resolved**. The dominant convention is the
   ratio-of-differences DSI = (R_pref - R_null) / (R_pref + R_null) with R_null taken at pref +
   180° [Elstrott2008] [Taylor2012]. The vector-sum DSI is used in some earlier cortical DS work
   but is not the DSGC standard; we adopt the ratio form to stay aligned with the Poleg-Polsky 2016
   envelope [PolegPolsky2016].
2. **Canonical HWHM for a sampled tuning curve** — **Resolved**. Standard practice is to fit or
   linearly interpolate between sample points on each side of the peak, find the first crossing of
   the half-max level, and report the mean of the two angular distances to those crossings
   [PolegPolsky2016] [scipy-interp-docs]. Non-monotonic shoulders are handled by selecting the first
   crossing from the peak outward.
3. **"Reliability" for trial-resolved tuning curves** — **Partially resolved**. The closest
   community-converged metric is the split-half or leave-one-trial-out coefficient of determination
   of trial means vs. individual trials, clamped to [0, 1] [DavidGallant2005]. Fano factor and SNR
   are also used but are sensitive to low firing rates; the R² formulation is preferred for DSGC
   scoring because it is bounded.
4. **Public DSGC scoring libraries** — **Partially resolved**. ModelDB 189347 ships a MATLAB/HOC
   stack that computes DSI inline but does not expose a Python scoring API [ModelDB-189347].
   `ratcave`, `pynapple`, and `elephant` provide tuning-curve utilities but none implement the t0002
   four-target envelope [elephant-GH]. No off-the-shelf library meets our spec, confirming the need
   for this task.
5. **Angle convention** — **Resolved**. DSGC literature uses 0° = preferred direction (or the
   stimulus azimuth at which response is maximal) with counter-clockwise positive. The target CSV
   from t0004 follows this convention, so our scorer must not re-rotate angles [Taylor2012].
6. **Normalisation for the weighted scalar loss** — **Resolved**. Min-max over the envelope
   half-widths is the standard choice in calibration-loss libraries (each residual is divided by the
   envelope width before squaring), which makes the four residuals commensurable [Nevergrad-docs]
   [BayesianOpt-GH].

## Search Strategy

**Sources searched**: Google Scholar, Semantic Scholar, ModelDB, GitHub code search, PyPI, SciPy
documentation, Nature Reviews Neuroscience archive, the Poleg-Polsky & Diamond (2016) supplement.

**Queries executed (8 total)**:

1. `direction selectivity index formula retinal ganglion cell DSI pref null`
2. `HWHM half width half maximum tuning curve sampled interpolation retinal`
3. `tuning curve reliability coefficient of determination trial R2 direction`
4. `"ModelDB 189347" Poleg-Polsky DSGC scoring implementation`
5. `GitHub "tuning_curve" DSI direction selectivity python library`
6. `scipy.interpolate HWHM half max crossing tuning curve`
7. `weighted euclidean loss envelope calibration residual normalization`
8. `python elephant tuning curve direction selectivity utilities`

**Date range**: no date restriction for foundational DS papers; 2015-2026 for code and tools.

**Inclusion criteria**: sources must provide either (a) an explicit DSI/HWHM/reliability formula
applied to a DSGC or DS ganglion-cell preparation, (b) open-source Python or MATLAB code computing
one of these quantities, or (c) design guidance for weighted scalar losses over bounded envelopes.
Non-DS cortical DSI work was excluded unless it was cited by DSGC sources.

**Search iterations**: queries 4-6 were follow-ups: query 4 was triggered by locating the
Poleg-Polsky & Diamond 2016 ModelDB entry, query 5 probed whether any community library already
exposes a score function, and query 6 validated the HWHM interpolation method against the SciPy API
we plan to depend on.

## Key Findings

### DSI formula convention for DSGCs

The standard DSGC DSI is the ratio-of-differences
`DSI = (R_preferred - R_null) / (R_preferred + R_null)`, where `R_preferred` is the firing rate at
the angle that maximises the trial-mean firing rate and `R_null` is the rate at `pref + 180°`
(modulo the angular grid) [Elstrott2008] [Taylor2012] [PolegPolsky2016]. This form gives DSI in
[0, 1] for non-negative rates and matches the envelope bounds stated in t0002 (DSI 0.7-0.85). The
vector-sum DSI used in some cortical papers produces a slightly different distribution and is not
used by the DSGC community.

**Best practice**: compute DSI on the trial-mean curve, not per-trial, to avoid division-by-zero
when a single trial happens to fire zero spikes at the null.

### HWHM computation on sampled tuning curves

HWHM (half width at half maximum) is computed by interpolating the tuning curve on each side of the
peak to find the angular distance at which the response crosses half of the peak value, then
averaging the two half-widths [PolegPolsky2016] [scipy-interp-docs]. For a 12-point curve at 30°
spacing, linear interpolation is enough — the community does not converge on cubic or spline fits
because those can introduce overshoots on noisy shoulders.

The half-max threshold is `(R_pref + R_baseline) / 2` or `R_pref / 2` depending on whether baseline
is subtracted. The Poleg-Polsky envelope uses the unsubtracted form `R_pref / 2` because baseline at
null is already small; we adopt the same form.

**Edge cases**: if no crossing is found on one side (monotonic shoulder), use the full angular span
on that side and document the clamp. If the curve has multiple local maxima, take the global max as
the peak and the *first* half-max crossing moving outward.

### Reliability as a bounded metric

The `tuning_curve_reliability` metric registered in `meta/metrics/` maps onto the
coefficient-of-determination variant used in [DavidGallant2005]: `1 - SS_residual / SS_total` across
trials, where the "model" is the trial-mean curve and residuals are trial-level rates. Without a
model, this reduces to `max(0, 1 - var_across_trials / var_across_angles)`. The value is explicitly
clamped to [0, 1] because small samples with low variance can produce negative values that have no
natural interpretation.

Alternative metrics (Fano factor, raw SNR) fail for zero-rate bins and introduce scale-dependence,
so they were rejected.

### Open-source landscape

ModelDB 189347 [ModelDB-189347] bundles inline MATLAB scoring functions but no stand-alone Python
API; porting those functions is the correct pattern. `elephant` [elephant-GH] provides
`elephant.statistics.fanofactor` and a `directional_tuning` helper but does not implement an
envelope loss. No public library was found that implements the exact DSI + peak + null + HWHM
four-target envelope — this confirms t0012's scope is genuinely missing.

**Hypothesis**: because DSI and HWHM are computed from the trial-mean curve but `reliability` is
computed across trials, the four-target loss and reliability will be roughly uncorrelated, and a
model can pass all four envelope targets while still having low reliability. The envelope pass
condition therefore must *not* be gated on reliability.

### Weighted scalar loss normalisation

[Nevergrad-docs] and [BayesianOpt-GH] both recommend normalising each residual by the width of its
admissible envelope before squaring and weighting, which gives a dimensionless loss of order 1 when
a residual is at the envelope boundary. We adopt this convention:
`residual_norm = (value - envelope_midpoint) / envelope_half_width`, so the scalar loss is
`sqrt(sum(weight_i * residual_norm_i^2))` with default weights 0.25 each.

## Methodology Insights

* **Match t0004's DSI/HWHM closed-form formulas exactly** so that `score(target, target)` returns
  `loss_scalar == 0.0`. The t0004 dataset stores angles and rates, not the peak or DSI, so the
  scorer must recompute both from the points; any subtle rounding or interpolation difference will
  break the identity test.
* **Clamp reliability to [0, 1]** at the top of the function, never at the bottom — this prevents
  spurious negative values from propagating into the residuals or the scalar loss.
* **Angle grid may be arbitrary**: do not hardcode 12 angles × 30°. Discover the grid from the
  input CSV and require only that it spans ≥180° so that a null counterpart exists for every
  angle.
* **Separate pure-math from CSV plumbing**: put `compute_dsi`, `compute_hwhm_deg`,
  `compute_reliability`, and `compute_weighted_loss` in `metrics.py`; keep CSV loading,
  group-by-trial, and target matching in `io.py`. Each test file then targets one module.
* **Return a frozen dataclass, not a dict**: `ScoreReport` is a `dataclass(frozen=True, slots=True)`
  so that downstream callers (tuning-curve optimisation tasks) get type hints and cannot mutate a
  result mid-pipeline.
* **CLI should print JSON**: emit the `ScoreReport` as JSON on stdout so the CLI is callable from a
  bash optimiser or W&B sweep without further parsing.
* **Testable hypothesis**: two synthetic curves with identical trial-means but different trial-level
  variance will produce identical DSI/peak/null/HWHM values but different `reliability` values. This
  is the exact reliability discrimination test required by the task description and must pass.

## Discovered Papers

### [Elstrott2008]

* **Title**: Direction Selectivity in the Retina Is Established Independent of Visual Experience and
  Cholinergic Retinal Waves
* **Authors**: Elstrott, J., Anishchenko, A., Greschner, M., Sher, A., Litke, A. M., Chichilnisky,
  E. J., Feller, M. B.
* **Year**: 2008
* **DOI**: `10.1016/j.neuron.2008.10.029`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(08)00898-X
* **Suggested categories**: `retinal-direction-selectivity`, `dsgc-reviews`
* **Why download**: Uses the exact DSI = (pref - null) / (pref + null) formulation on DSGC
  recordings and reports the bounded-[0,1] distributions we target. Useful as a canonical citation
  for the DSI formula and as a dataset reference for wild-type DSI distributions.

### [DavidGallant2005]

* **Title**: Predicting Neuronal Responses During Natural Vision
* **Authors**: David, S. V., Gallant, J. L.
* **Year**: 2005
* **DOI**: `10.1088/0954-898X_16_2_003`
* **URL**: https://iopscience.iop.org/article/10.1088/0954-898X_16_2_003
* **Suggested categories**: `receptive-field-modeling`
* **Why download**: Source for the bounded [0, 1] coefficient-of-determination reliability metric
  that we adopt. Establishes the split-half and leave-one-out computation variants.

## Recommendations for This Task

1. **Adopt the ratio DSI** `(pref - null) / (pref + null)` for `compute_dsi`. This is the DSGC
   standard and matches the t0002 envelope bounds [Elstrott2008] [Taylor2012].
2. **Use linear interpolation for HWHM** via `numpy.interp` or `scipy.interpolate.interp1d` with
   `kind="linear"` [scipy-interp-docs]. Cubic fits are contraindicated on 12-point curves.
3. **Clamp reliability to [0, 1]** using the `max(0, min(1, r))` idiom and document the clamp in the
   library `description.md` so downstream optimisers do not interpret unclamped negative R² values
   [DavidGallant2005].
4. **Normalise residuals by envelope half-widths** before computing the scalar loss, with default
   weights 0.25 each [Nevergrad-docs].
5. **Expose a `cli.py` entry point** that prints the full `ScoreReport` as JSON, so W&B sweeps and
   bash-driven parameter scans can consume the scorer directly.
6. **Write the envelope-boundary tests before writing the scoring code** — each of DSI, peak,
   null, HWHM needs one test just inside and one just outside its boundary. These tests protect the
   meaning of `passes_envelope` across refactors.
7. **Do NOT add a second `vector_sum_dsi` field to ScoreReport** even though it is tempting — it
   is not the DSGC convention and would bloat the report without adding information [Taylor2012].

## Source Index

### [Elstrott2008]

* **Type**: paper
* **Title**: Direction Selectivity in the Retina Is Established Independent of Visual Experience and
  Cholinergic Retinal Waves
* **Authors**: Elstrott, J. et al.
* **Year**: 2008
* **DOI**: `10.1016/j.neuron.2008.10.029`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(08)00898-X
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Canonical source for DSI = (pref - null) / (pref + null) applied to DSGCs and for
  bounded-[0,1] DSI distributions in wild-type mouse retina.

### [Taylor2012]

* **Type**: paper
* **Title**: Direction selectivity in the retina: symmetry and asymmetry in structure and function
* **Authors**: Vaney, D. I., Sivyer, B., Taylor, W. R.
* **Year**: 2012
* **DOI**: `10.1038/nrn3165`
* **URL**: https://www.nature.com/articles/nrn3165
* **Peer-reviewed**: yes (Nature Reviews Neuroscience)
* **Relevance**: Standard DSGC review establishing the DSI convention, the preferred = 0° angle
  convention, and the HWHM reporting style for tuning curves.

### [PolegPolsky2016]

* **Type**: paper
* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(16)00173-3
* **Peer-reviewed**: yes (Neuron)
* **Relevance**: Provides the DSGC compartmental-model envelope (DSI 0.7-0.85, peak 40-80 Hz, null <
  10 Hz, HWHM 60-90°) that this scoring library enforces via `passes_envelope`.

### [DavidGallant2005]

* **Type**: paper
* **Title**: Predicting Neuronal Responses During Natural Vision
* **Authors**: David, S. V., Gallant, J. L.
* **Year**: 2005
* **DOI**: `10.1088/0954-898X_16_2_003`
* **URL**: https://iopscience.iop.org/article/10.1088/0954-898X_16_2_003
* **Peer-reviewed**: yes (Network: Computation in Neural Systems)
* **Relevance**: Bounded [0, 1] coefficient-of-determination reliability metric that we adopt.

### [ModelDB-189347]

* **Type**: repository
* **Title**: ModelDB 189347 — Poleg-Polsky & Diamond DSGC model with NMDA multiplicative gain
* **Author/Org**: Poleg-Polsky, A., Diamond, J. S.
* **URL**: https://modeldb.science/189347
* **Last updated**: 2016-02
* **Peer-reviewed**: no (companion code)
* **Relevance**: The reference DSGC implementation whose envelope we score against. Inline
  MATLAB/HOC scoring functions are the closest existing scorer but are not exposed as a Python API,
  motivating this task.

### [elephant-GH]

* **Type**: repository
* **Title**: Elephant — Electrophysiology Analysis Toolkit
* **Author/Org**: NeuralEnsemble
* **URL**: https://github.com/NeuralEnsemble/elephant
* **Last updated**: 2026-02
* **Peer-reviewed**: no (companion to published toolkit papers)
* **Relevance**: Offers a `fanofactor` and direction-tuning helpers but no envelope-loss scoring.
  Confirms the gap this task fills.

### [scipy-interp-docs]

* **Type**: documentation
* **Title**: scipy.interpolate — Interpolation
* **Author/Org**: SciPy Project
* **URL**: https://docs.scipy.org/doc/scipy/reference/interpolate.html
* **Peer-reviewed**: no
* **Relevance**: API reference for `numpy.interp` and `scipy.interpolate.interp1d` used by
  `compute_hwhm_deg` to find the half-max crossings.

### [Nevergrad-docs]

* **Type**: documentation
* **Title**: Nevergrad — A Gradient-Free Optimization Platform (Losses and Penalties)
* **Author/Org**: Facebook AI Research
* **URL**: https://facebookresearch.github.io/nevergrad/optimization.html
* **Peer-reviewed**: no
* **Relevance**: Documents the normalise-by-envelope-width pattern we use for the weighted scalar
  loss so that residuals are dimensionally comparable.

### [BayesianOpt-GH]

* **Type**: repository
* **Title**: bayesian-optimization — constrained Bayesian optimisation in Python
* **Author/Org**: fmfn
* **URL**: https://github.com/fmfn/BayesianOptimization
* **Last updated**: 2026-01
* **Peer-reviewed**: no
* **Relevance**: Provides the pattern of bounded-constraint penalisation that we mirror with
  envelope-width normalisation in the weighted scalar loss.

### [pandas-docs]

* **Type**: documentation
* **Title**: pandas GroupBy
* **Author/Org**: pandas Project
* **URL**: https://pandas.pydata.org/docs/user_guide/groupby.html
* **Peer-reviewed**: no
* **Relevance**: API reference for trial-aware groupby used by `io.py` to reduce the
  `(angle_deg, trial_seed, firing_rate_hz)` CSV into the trial-mean curve consumed by DSI, peak,
  null, and HWHM.
