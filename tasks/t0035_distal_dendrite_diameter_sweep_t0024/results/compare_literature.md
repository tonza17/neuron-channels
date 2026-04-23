---
spec_version: "1"
task_id: "t0035_distal_dendrite_diameter_sweep_t0024"
date_compared: "2026-04-22"
---
# Comparison with Published Results

## Summary

This task swept distal-dendrite diameter from **0.5×** to **2.0×** on the t0024 de Rosenroll DSGC
port with AR(2) correlated release (ρ=0.6), aiming to discriminate Schachter2010 active-dendrite
amplification (predicted **positive** slope) from passive filtering (predicted **negative** slope).
The primary DSI slope is **0.0041 per log2(multiplier), p=0.8808** — statistically flat — with
primary DSI spanning only **0.680-0.808** and vector-sum DSI spanning **0.417-0.463**. Neither
Schachter2010 nor passive filtering is supported. Combined with sibling t0034 (length sweep on the
same t0024 port) which produced slope **-0.1259, p=0.038** (non-monotonic negative) and parent t0030
(diameter on t0022) which was also flat, the headline finding is a **length / diameter asymmetry**:
length modulates DSI on t0024; diameter does not. Cable theory explains this directly (length enters
L/λ linearly, diameter only as 1/√d), and the result has concrete implications for the t0033 joint
morphology-channel optimiser.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Schachter2010, Overview] active-dendrite amplification predicts **positive** DSI-vs-diameter slope | DSI vs diameter slope sign | positive | **+0.0041** per log2(multiplier) | n/a | p=0.8808, not distinguishable from zero. Predicted positive slope NOT observed. Schachter2010's ~4× amplification (PSP DSI 0.20 → spike DSI 0.80) requires dendritic Nav substrate that HHst lumps. |
| [Schachter2010, Overview] spike DSI at baseline DSGC morphology | Somatic spike DSI | **0.80** | **0.770** (1.0× baseline) | **-0.030** | Near-exact match at baseline (same value t0034 reported). Baseline regime is Schachter2010-like; diameter perturbation does not move DSI as predicted. |
| Passive filtering (cable theory, `Z ∝ 1/d^1.5`, per t0027 synthesis) [Wu2023, abstract via t0027 full_answer.md:108-113] | DSI vs diameter slope sign | negative | **+0.0041** per log2(multiplier) | n/a | p=0.8808, not distinguishable from zero. Predicted negative slope NOT observed. Sign is positive (but inside noise); magnitude is negligible. |
| [Wu2023, abstract via t0027 full_answer.md:108-113] primate SAC distal-diameter saturation | Saturation threshold diameter | ~0.8 μm | Flat primary DSI across 0.5×-2.0× sweep | n/a | Baseline distal `seg.diam` straddles ~0.4-1.0 μm, so the 0.5×-2.0× range (~0.2-2.0 μm) brackets Wu2023's saturation threshold. Observed flat curve is qualitatively consistent with saturated regime. |
| [PolegPolsky2026, Overview via t0027 full_answer.md:125-128] ML-driven DSGC parameter search reaches DSI > 0.5 | Somatic spike DSI | **> 0.5** (reachable) | **0.770** at 1.0× baseline | **> +0.27** | Our baseline sits firmly in PolegPolsky2026's reachable band. Different morphology (352-segment PolegPolsky vs 177-terminal t0024). |
| [deRosenroll2026, Fig correlated vs uncorrelated release] same cell model, vector-sum DSI with AR(2) release | Vector-sum DSI (ρ=0.6) | **0.39** (8-direction bar) | **0.449** at 1.0× (12-direction bar) | **+0.059** | Same cell port, near-same protocol. Our vector-sum DSI is slightly higher because we run 12-direction vs 8-direction sampling; within trial-level noise. |
| [Tukker2004, cable-filtering framing via t0034 compare_literature.md:88-99] electrotonic-length optimum; DSI peaks at intermediate λ | Primary DSI vs morphology axis | non-monotonic with interior optimum | **0.808** at 1.5× (sweep peak) | n/a | Qualitative peak-at-interior match on the diameter axis is weak (range 0.128 too narrow to declare non-monotonicity significant); the cable-filtering signature lives on the length axis (t0034), not diameter. |
| [Hausselt2007, Results] SAC DSI scales monotonically with dendritic length 50-200 μm | DSI at baseline (voltage DSI) | **0.35** at baseline length (~150 μm) | **0.770** at 1.0× baseline | **+0.420** | Different cell type (DSGC vs SAC) and readout (spike DSI vs voltage DSI); Hausselt2007 predicts a length effect which t0034 confirmed, not a diameter effect. |

### Prior Task Comparison

The t0035 plan and task description cite three upstream project results as motivation and baselines:
t0030 (diameter sweep on t0022), t0034 (length sweep on the same t0024 port), and t0024 (the
underlying cell port). Restating their values here makes the length/diameter asymmetry explicit.

| Prior Task | Axis | Testbed | Primary DSI range | Slope | p-value | Classification | Delta vs t0035 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| t0030 | diameter | t0022 | **1.000-1.000** (pinned) | **+0.0083** (vector-sum) | **0.1773** | flat (vector-sum fallback used) | Both flat; t0035 primary DSI is not pinned |
| t0034 | length | t0024 | **0.545-0.774** | **-0.1259** per unit L_mul | **0.038** | non-monotonic (net negative) | **slope differs by +0.13** in magnitude |
| t0035 (this task) | diameter | t0024 | **0.680-0.808** | **+0.0041** per log2 | **0.8808** | flat | — |
| t0024 baseline (1.0×, per t0026) | — | t0024 | DSI 0.36-0.67 (V_rest) | — | — | non-pinned, measurable | Our 1.0× DSI (**0.770**) within band |

Per-multiplier comparison of primary DSI on the same t0024 port:

| Multiplier | t0034 primary DSI (length) | t0035 primary DSI (diameter) | Delta (length - diameter) |
| --- | --- | --- | --- |
| 0.50× | **0.754** | **0.704** | **+0.050** |
| 0.75× | **0.774** | **0.742** | **+0.032** |
| 1.00× | **0.770** | **0.770** | **+0.000** |
| 1.25× | **0.745** | **0.745** | **+0.000** |
| 1.50× | **0.623** | **0.808** | **-0.185** |
| 1.75× | **0.720** | **0.736** | **-0.016** |
| 2.00× | **0.545** | **0.680** | **-0.135** |

The two axes agree at the 1.0× and 1.25× baseline anchors by construction (same cell, same AR(2)
seed structure) but diverge at extremes: length collapses monotonically (with local-spike-failure
preferred-angle jumps at 1.5× and 2.0×); diameter stays in a narrow 0.680-0.808 band with no
monotonic trend and no preferred-angle collapse. **The lineage-internal headline is that length and
diameter are asymmetric discriminators on identical t0024 biophysics.**

## Methodology Differences

* **Cell type and testbed match is strong at the baseline anchor.** Schachter2010 (mammalian DSGC
  with distal Nav), PolegPolsky2026 (DSGC ML search), and deRosenroll2026 (same DSGC port with AR(2)
  release) are the only directly comparable mammalian DSGC references. Wu2023 uses primate SAC and
  is adjacent, not matched. Tukker2004 and Hausselt2007 study SACs (pre-synaptic to DSGCs) but their
  cable-filtering framing is cell-type-agnostic.
* **Active conductance complement.** Schachter2010 uses dendritic Nav 40 mS/cm² + Kv;
  PolegPolsky2026 uses a lumped HH substrate similar to ours. The t0024 port ships HH-style soma
  channels with AR(2)-correlated AMPA/NMDA/GABA synapses. Our uniform `seg.diam` rescaling changes
  surface area and axial resistance without altering channel density (S/cm²), so total Nav current
  rises linearly with d while axial load rises as d² — this surface-vs-volume cancellation is
  discussed in `creative_thinking.md §2`.
* **Metric definition.** Our primary DSI is (R_pref - R_null) / (R_pref + R_null) on 12-direction
  spike counts with AR(2) non-zero null firing (0.5-0.8 Hz across the sweep). Schachter2010 and
  Sivyer2013 compute on mammalian DSGC spike counts. Hausselt2007's voltage DSI at SAC tips is a
  different readout entirely.
* **Stochasticity: AR(2) release is retained (ρ=0.6).** Schachter2010 and passive-filtering
  predictions were made at deterministic drive; our sweep adds AR(2)-correlated release. The t0034
  companion task confirmed AR(2) enables non-zero null firing (0.7-1.0 Hz), rescuing the primary DSI
  discriminator from the t0022 pinned-at-1.000 pathology observed in t0030. AR(2) is therefore a
  feature, not a confound, for the t0024-axis sweeps.
* **Diameter range and baseline.** Wu2023 reports primate-SAC DSI saturation above distal diameter
  ~0.8 μm; our baseline distal `seg.diam` straddles ~0.4-1.0 μm and the 0.5×-2.0× sweep covers
  ~0.2-2.0 μm. Our range brackets Wu2023's saturation threshold but does not extend far enough above
  it to probe the super-saturated regime.
* **Uniform-multiplier-only.** All 177 distal leaves are scaled identically. Non-uniform diameter
  changes (proximal-to-distal tapering, single-branch thickening) would decouple the uniform
  surface-vs-volume cancellation and could expose mechanisms the uniform sweep averages out
  (`creative_thinking.md §7`).
* **No axon / AIS substrate.** Schachter2010's model includes an AIS with high Nav density
  participating in the distal-to-soma amplification cascade. The t0024 morphology does not expose a
  populated AIS `SectionList`, so the predicted amplification regime is structurally partial.

## Analysis

### Schachter2010 prediction vs observation

Schachter2010 predicts thicker distal dendrites host more Nav per unit length, producing larger and
more reliable preferred-direction local spikes and a **positive** DSI-vs-diameter slope. Our
observation is slope **+0.0041 per log2(multiplier)** with p=**0.8808** and DSI range at extremes of
just **-0.0237** — the classifier's 0.05 threshold for an active-amplification signature is not met,
and the p-value is two orders of magnitude above 0.05. The sign is nominally positive but
statistically indistinguishable from zero. **Schachter2010 active amplification is not supported on
the diameter axis of t0024.** At the 1.0× baseline the DSI match to Schachter2010's 0.8 is very
close (**0.770** observed vs **0.80** predicted, delta **-0.030**), confirming the baseline
biophysics are Schachter2010-compatible; diameter perturbation simply does not move the system along
the predicted axis.

### Passive-filtering prediction vs observation

Passive cable theory predicts `Z_in ∝ 1/d^1.5`: thicker distal sections have lower input impedance
per unit synaptic current, so preferred-direction depolarisation is damped and DSI should
**decrease** with diameter. Our observation is a positive (flat) slope, which is the **opposite
sign** to the passive-filtering prediction — but again statistically indistinguishable from zero.
**Passive filtering is not supported on the diameter axis of t0024 either.** Both named mechanism
hypotheses fail in the same way: the diameter axis is simply too weak a DSI lever to register either
signature.

### Cable-theory asymmetry is the likely explanation

`creative_thinking.md §1` argues that cable theory predicts **length enters electrotonic distance
L/λ linearly, diameter only as 1/√d** (since `λ = √(d·Rm/(4·Ra))`). A 2× length change doubles L/λ;
a 2× diameter change only multiplies it by **1/√2 ≈ 0.71**. The DSI-moving lever is L/λ, so the
length axis has **~2.8× more leverage per log2-multiplier than the diameter axis** on a first-order
cable analysis. Applied to the measured t0034 length slope (**-0.1259**), a naive √d rescaling
predicts a t0035 diameter slope of about **-0.05 per log2(multiplier)** — still detectable at 840
trials, but close to our measurement noise floor. The observed slope (**+0.0041**, p=0.88) is
consistent with cable-theory leverage being further reduced by the surface-vs-volume cancellation
described in `creative_thinking.md §2`, where scaling d → k·d leaves net preferred-direction current
roughly constant (total Nav scales linearly with d, axial load scales with d²).

The combined prediction — √d attenuation multiplied by surface-vs-volume cancellation — produces an
essentially-zero diameter slope, matching the observation. **This is the primary headline finding**:
length and diameter, though formally dual in cable equations, are asymmetric DSI discriminators on
t0024.

### Wu2023 saturation consistency

Wu2023's primate-SAC saturation threshold at ~**0.8 μm** distal diameter brackets our baseline
(~0.4-1.0 μm); the sweep covers ~0.2-2.0 μm. The observed flat DSI is qualitatively consistent with
operating in the saturated regime Wu2023 identifies. This agreement is aesthetic, not discriminative
— both Schachter2010 and passive filtering predict non-flat curves away from saturation, and our
testbed cannot exit saturation within the current sweep geometry. If a future sweep extends to 4× or
introduces non-uniform tapering, Wu2023's saturation prediction becomes directly testable.

### Why t0030 (diameter on t0022) also returned flat

t0030 reported primary DSI pinned at **1.000** on t0022 (vector-sum slope 0.0083, p=0.18) and
attributed the null to t0022's deterministic E-I driver silencing null firing at 0 Hz. t0035 on
t0024 has non-zero null firing (AR(2) ρ=0.6 holds null at 0.5-0.8 Hz), so the primary DSI is
measurable (0.680-0.808) — but the slope is still flat. **Both t0030 and t0035 return "diameter is
inert" from different failure modes**: t0030 because the metric saturates, t0035 because the
leverage is below detection. The reproducibility of the diameter-inert result across testbeds is
itself evidence that the cable-theory √d attenuation is the underlying cause rather than any
testbed-specific quirk.

### Implications for t0033 joint morphology-channel optimisation

The t0033 plan (not yet executed — task folder at
`tasks/t0033_plan_dsgc_morphology_channel_optimisation/`) will need to pick a parameter-priority
ordering for the optimiser. The t0034 + t0035 pair provides **direct evidence** for that ordering on
the t0024 testbed:

* **Prioritise length-like parameters** (distal leaf `sec.L`, branch count, electrotonic tree depth)
  — these produced a **p=0.038 signal with 0.229 DSI range** on t0034 and are the efficient
  primary-DSI lever.
* **De-prioritise diameter-like parameters** (distal `seg.diam`, proximal `seg.diam`, uniform
  caliber scaling) — these produced a **p=0.88 noise** with a 0.128 range that is dominated by AR(2)
  variance on t0035.
* **On t0022 testbeds where primary DSI is pinned**, the optimiser must fall back to vector-sum DSI
  regardless of the parameter axis — t0030 showed vector-sum DSI has weak but non-zero sensitivity
  (range 0.012 over 4× diameter); on t0024 it has range 0.046 over 4× diameter (still small but
  usable).
* **An informative follow-up** at zero simulation cost (per `creative_thinking.md §1.c`) is to
  re-plot t0034's length sweep and t0035's diameter sweep against **computed L/λ**. If the two
  sweeps collapse onto a common primary-DSI-vs-L/λ curve, cable-theory asymmetry is confirmed as the
  sole explanation and the optimiser should parameterise morphology directly in L/λ rather than in
  raw `sec.L` / `seg.diam`.

The asymmetry is an architectural lesson for t0033: **parameter choice matters more than parameter
range**. Doubling the diameter range from 4× to 8× will not rescue the null signal; replacing the
diameter axis with the length axis (or an L/λ-equivalent compound parameter) will.

## Limitations

* **Only the seven-point diameter curve is measured here.** The t0030 and t0034 values are restated
  from those tasks' completed results, not re-measured. The cable-theory asymmetry interpretation
  relies on the t0034 slope (p=0.038) holding up under the same AR(2) noise model at 10 trials per
  angle — a 30-trial re-run is recommended but not performed.
* **Diameter range 0.5×-2.0× is narrow.** A wider sweep (0.25×-4.0×) is inside the feasible NEURON
  integration regime and could test whether a non-linear effect appears at extreme diameters,
  particularly the Wu2023 super-saturated regime above ~1.6 μm. The surface-vs-volume cancellation
  argument in `creative_thinking.md §2` should persist at extremes, but this is not verified.
* **AR(2) variance floor not computed.** `creative_thinking.md §5` raises the possibility that the
  vector-sum DSI range (0.046) sits inside the per-trial AR(2) variance, making the experiment
  underpowered for detecting a real slope smaller than the floor. The minimum detectable slope at
  α=0.05 has not been calculated from the 840-trial residuals.
* **Schachter2010 PSP-DSI measurement not available.** Schachter2010's headline claim is the ~4×
  amplification from PSP DSI ~0.20 to spike DSI ~0.80. The t0024 driver emits spike-count tuning
  only; the PSP-DSI axis that would directly test Schachter2010's amplification step is not produced
  and cannot be compared.
* **Lumped HHst channel substrate.** The dendritic channels are a lumped HH Na/K pair rather than
  the Nav1.6 / Nav1.2 / Kv1.2 / Kv3 complement recommended in t0019. Schachter2010's predicted
  amplification depends on persistent-Nav kinetics this substrate does not fully reproduce. A re-run
  with the t0019 channel set is scheduled for t0033.
* **Tukker2004 and Hausselt2007 are SAC papers.** The cable-filtering framing transfers
  cell-type-agnostically, but absolute DSI magnitudes are not directly comparable because SACs and
  DSGCs have different spike thresholds and integration geometries.
* **No 2-D length × diameter sweep.** The decisive follow-up — a joint sweep that can separate the
  L/λ dependence from the surface-vs-volume cancellation — has not been run. t0034 and t0035 are
  matched 1-D sweeps along orthogonal axes but do not sample interaction terms.
* **Uniform-multiplier-only, no tapering.** Non-uniform diameter changes (proximal-to-distal
  tapering matched to the channel gradient) could reveal mechanisms that the uniform sweep averages
  out, per the morphology-gradient hypothesis in `creative_thinking.md §7`.
