# Creative Thinking: Length vs Diameter Asymmetry on t0024 DSGC

## Objective

On the t0024 DSGC testbed, a uniform multiplier on distal-dendrite **length** (sibling t0034)
produced a detectable, non-monotonic modulation of DSI (slope-based regression **p = 0.038**), while
the matched multiplier on distal-dendrite **diameter** (this task, t0035) produced a flat
DSI-versus-diameter relationship (slope **0.0041**, **p = 0.8808**; primary DSI spans a narrow
**0.680-0.808**, vector-sum **0.417-0.463**). Diameter also read flat on the parent t0022 testbed
(t0030), so the "diameter is inert" result is reproducible across morphologies, whereas length is
not. The core puzzle is mechanistic: in cable theory both parameters enter the same equations, so
why is only one of them read out by DSI on this cell? Below I enumerate explanations that could
generate this asymmetry and sketch a decisive follow-up for each.

## Alternatives Considered

1. **Cable-theory asymmetry (length enters linearly, diameter under a square-root).** (a)
   Electrotonic length `L/λ` scales linearly with physical length but only as `1/√d` with diameter
   (since `λ = √(d·Rm/(4·Ra))`). A 2× length change doubles `L/λ`; a 2× diameter change only
   multiplies it by `1/√2 ≈ 0.71`. DSI, which depends on how much distal depolarisation survives to
   the soma, therefore tracks length much more sensitively. (b) Consistent with both observations:
   length moved DSI on t0024 (t0034), diameter did not (t0035); diameter was also flat on t0022
   (t0030). The narrow 0.128 DSI range over a 4× diameter sweep is exactly what the √d attenuation
   predicts. (c) Compute `L/λ` for each variant from morphology + passive params and regress DSI on
   it; a unified linear fit against `L/λ` should collapse the length and diameter sweeps onto the
   same curve if this is the dominant explanation.

2. **Surface-to-volume compensation in active conductances.** (a) In HHst, `gbar` is a surface
   density (S/cm²). Scaling diameter d → k·d scales surface area by k (per unit length) but
   cross-sectional area by k². The *total* Nav/Kv current rises linearly with d while the *axial
   load* it has to charge rises as d². Net soma-directed current is therefore roughly constant or
   mildly decreasing in d — no monotonic DSI trend. (b) Fits the flat-with-mild-peak pattern seen at
   x1.50 and dip at x2.00; length rescaling does not create this surface/volume cancellation. (c)
   Switch the distal compartments to a *density* rescaling (scale `gnabar_HHst` by 1/d) so the
   per-section channel count is held fixed, and re-run a small x0.5/x1.0/x2.0 sweep. If DSI now
   tracks diameter, the confound is confirmed.

3. **NEURON `d_lambda` auto-resegmentation masks diameter effects.** (a) The code reapplies
   `d_lambda` after geometry edits. Because `λ ∝ √d`, thicker sections get *more* segments,
   effectively counter-balancing the biophysical change by improving spatial resolution in exactly
   the regions that changed. (b) Could explain why diameter is flat on both t0022 and t0024, but
   also why slopes at extreme multipliers are symmetric rather than monotonic. (c) Re-run a single
   multiplier (e.g. x2.00) with `nseg` frozen to the baseline value; any DSI shift that emerges is a
   segmentation artefact we are currently absorbing.

4. **Input impedance saturation at t0024's distal baseline.** (a) If the baseline distal terminals
   are already in an "impedance-saturated" regime where the local depolarisation is limited by
   channel availability rather than by load, further diameter changes barely shift the voltage
   waveform, whereas length changes still alter *where* the synapse sits electrotonically. (b) Fits
   the flat result but not the particular non-monotonic t0034 curve; also explains why the DSI band
   is so narrow (0.128 wide) across a large geometric sweep. (c) Measure distal input impedance
   `Zin` at each variant; if it is already near asymptote at baseline, diameter truly is the wrong
   lever on this cell.

5. **AR(2) release noise ceiling.** (a) Vector-sum DSI only varies 0.046 across the sweep, which may
   sit inside the per-trial AR(2) variance floor from stochastic release. Length happened to clear
   it; diameter did not. (b) Consistent with 120 trials per variant still giving p = 0.88. Does not,
   however, explain why t0030 is also flat — both testbeds would need the same ceiling
   coincidentally. (c) Fit the residual variance from the 840 trials and compute the minimum
   detectable slope at α = 0.05. If it exceeds 0.01 DSI / diameter step, the experiment was
   underpowered, not null.

6. **Morphology-specific structural simplicity of t0024.** (a) t0024's DSGC has a shallower,
   less-branched distal tree than t0022's Poleg-Polsky morphology; diameter-driven changes in
   branch-point impedance mismatch only matter when the arbor is complex enough to host many such
   mismatches. (b) Weakly supported: diameter is flat on *both* testbeds, so morphology complexity
   is not distinguishing. (c) Sweep diameter on a synthetic highly-branched morphology (Y-fork
   cascade); if DSI recovers a slope there, this hypothesis is promoted.

7. **Distal channel gradient non-uniformity.** (a) Nav/Kv densities in the PolegPolsky family are
   already graded along the dendrite. A uniform diameter multiplier over the distal mask rescales
   axial load homogeneously but the *local* channel gradient it must drive is inhomogeneous; the net
   effect averages out. Length scaling stretches the gradient itself, so its effect does not cancel.
   (b) Consistent with flat diameter and non-monotonic length. (c) Apply a graded
   (proximal-to-distal) diameter multiplier matched to the channel gradient; if DSI now moves, the
   cancellation hypothesis is confirmed.

## Recommendation

Hypothesis **1 (cable-theory √d vs linear-L)** is the most likely primary driver: it is
parameter-free, predicts the direction, magnitude, and cross-testbed reproducibility of the
asymmetry, and is a necessary consequence of the equations we already use. Hypothesis **2
(surface/volume compensation)** is a close partner that plausibly explains why the residual diameter
signal is not merely small but essentially zero — the √d shrinkage from (1) and the d-vs-d²
cancellation from (2) multiply rather than add. The single most informative follow-up is a re-plot
of DSI from all existing t0034 and t0035 trials against the computed `L/λ` of the distal tree; a
collapse onto a common curve would confirm (1) without any new simulation cost. If the residual
scatter is still structured by diameter, hypothesis (2) can be isolated by a small density- rescaled
sweep as described above.

## Limitations

* Only the seven-point diameter curve on t0024 is inspected; the parent t0030 data are summarised
  from the task description rather than re-examined in detail here.
* AR(2) variance ceiling cannot be ruled out without the residual distribution of the 840 trials.
* We did not download any new papers for this creative-thinking step; cable-theory reasoning is
  drawn from standard Rall-form relationships embedded in the existing codebase, not from a
  freshly-surveyed literature.
* "Non-monotonic length effect" is taken from the t0034 summary statistic (p = 0.038); the creative
  hypotheses do not attempt to explain the *shape* of the length curve, only the length-vs-diameter
  contrast.
* The `L/λ` collapse test assumes passive parameters `Rm` and `Ra` are unchanged across variants,
  which matches the current sweep protocol but would fail if a future sweep co-varies them.
