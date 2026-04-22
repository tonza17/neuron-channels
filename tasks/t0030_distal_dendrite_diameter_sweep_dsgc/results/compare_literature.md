---
spec_version: "1"
task_id: "t0030_distal_dendrite_diameter_sweep_dsgc"
date_compared: "2026-04-22"
---
# Comparison with Published Results

## Summary

This task swept distal-dendrite diameter from **0.5x** to **2.0x** of baseline on the t0022 DSGC
testbed with the explicit aim of discriminating Schachter2010 active-dendrite amplification (a
positive DSI-vs-diameter slope) from a passive-filtering alternative (a negative slope). Primary
peak/null DSI is pinned at **1.000** at every multiplier (slope **0.000**, range at extremes
**0.000**), forcing the vector-sum DSI to act as fallback; its slope is **0.0083 per
log2(multiplier)** with **p = 0.1773** and a range at extremes of only **0.0124** — the curve is
**flat**, so **neither Schachter2010 nor passive filtering is supported**. The sibling length sweep
t0029 observed the same 1.000 plateau under the same schedule, identifying the t0022 E-I timing as
the DSI-setting variable and distal morphology as a nullified axis on this testbed.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Schachter2010 compartmental DSGC — spike DSI with dendritic Nav [Schachter2010, Abstract / Overview] | DSI (somatic spike) | 0.80 | 1.000 | **+0.200** | Schachter2010 reports ~4x DSI amplification from passive PSP DSI ~0.20 to spike DSI ~0.80 via dendritic Nav/Ca threshold nonlinearity; our testbed is already saturated above their spike-DSI value |
| Schachter2010 subthreshold PSP DSI [Schachter2010, Overview] | DSI (PSP) | 0.20 | n/a | n/a | Not measured — the t0022 driver emits spike-count tuning only; the PSP-DSI axis that quantifies the Schachter2010 active-amplification step is absent |
| Schachter2010 active-amplification prediction (slope sign) [Schachter2010, Overview] | DSI vs diameter slope | positive | **+0.0083** | n/a | Slope p=0.1773 is not distinguishable from zero; predicted positive slope not observed |
| Passive filtering (cable theory, per t0027 synthesis) [Wu2023, abstract; t0027 full_answer.md:108-113] | DSI vs diameter slope | negative | **+0.0083** | n/a | Thicker distal = lower input impedance (Z ~ 1/d^1.5) should damp directional contrast; predicted negative slope not observed |
| Wu2023 primate SAC connectomics sweep — distal diameter saturation [Wu2023, abstract via t0027 full_answer.md:108-113] | distal-diameter saturation threshold | ~0.8 um | 0.30 across 0.5x-2.0x sweep (vector-sum DSI range) | n/a | Wu2023 reports DSI saturates once distal diameter exceeds ~0.8 um; our baseline distal `seg.diam` ~0.4-1.0 um already straddles this threshold, consistent with the observed flat vector-sum DSI but not a direct DSI-magnitude comparator |
| Sivyer2013 rabbit DSGC control — dendritic-spike branch independence [Sivyer2013, Fig. 2-3 text] | DSI (spike) | ~1.0 | 1.000 | **+0.000** | Qualitative match — "close to 1" under control conditions; Sivyer2013 plateau height not quantified to 3 dp |
| PolegPolsky2026 DSGC machine-learning model [PolegPolsky2026, Overview via t0027 full_answer.md:125-128] | DSI (spike) | > 0.5 (reachable) | 1.000 | **+0.500** | Parent of the morphology used in our testbed; PolegPolsky2026 shows DSI > 0.5 is reachable via distance-graded passive delay, coincidence detection, or NMDA gating — our E-I-timing driver far exceeds their reported operating band |

### Prior Task Comparison

The t0030 plan cites two upstream project results as baselines — t0022 (the testbed we sweep) and
t0029 (the sibling length sweep) — plus the t0027 synthesis answer as the source of the two
hypotheses. Those values are restated here so the flat DSI-vs-diameter finding can be judged against
the project's own measurement lineage.

| Prior Task / Source | Metric | Prior Value | t0030 Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0022 baseline (per-dendrite E-I, 1.00x multiplier) | DSI (pref/null) | 1.000 | 1.000 | **+0.000** | t0030 at 1.00x is an exact by-construction reproduction — only `seg.diam` is mutated, never the schedule |
| t0022 baseline | HWHM (deg) | 116.25 | 116.25 | **+0.00** | Same exact match at 1.00x |
| t0022 baseline | Peak firing (Hz) | 15 | 15 | **+0** | Same exact match at 1.00x |
| t0029 length sweep (parallel geometry axis) | primary DSI (range across 0.5x-2.0x) | 0.000 | 0.000 | **+0.000** | Both sweeps produce the same saturated 1.000 plateau; diameter adds no new information on the primary axis |
| t0029 length sweep | vector-sum DSI (range across 0.5x-2.0x) | 0.021 | 0.012 | **-0.009** | t0030 dynamic range is even smaller than t0029's — diameter moves the secondary metric less than length does |
| t0029 length sweep | classification label | flat | flat | n/a | Both axes yield the same null result; the testbed's E-I schedule dominates both morphology axes |

The lineage-internal finding is that **both distal-morphology axes (length, diameter) hit the DSI =
1.000 ceiling** while the schedule stays fixed. The t0030 sweep adds a second morphological axis to
the t0029 pattern and produces an even smaller vector-sum dynamic range (0.012 vs 0.021) —
diameter is **less informative** than length on this testbed, because diameter modifies local input
impedance and Nav substrate per unit length without changing the section midpoints that
`schedule_ei_onsets` uses for onset timing. The cross-task null result is decisive: on the t0022
schedule, neither Schachter2010 amplification nor passive filtering has an observable DSI signature
over a 4x morphology range.

## Methodology Differences

* **Null-direction firing silenced by design.** The t0022 scheduler uses
  `GABA_CONDUCTANCE_NULL_NS = 12 nS` (about 4x the preferred-direction value of 3 nS) applied 10 ms
  before AMPA onset on the null half-plane. Null firing is exactly **0 Hz** at every diameter
  multiplier, which pins the peak-minus-null DSI numerator at the preferred rate and the ratio at
  1.000 before distal biophysics can enter. Schachter2010 uses compound null inhibition of ~6 nS
  alongside Poisson-like stochastic inputs, and the Schachter2010 DSI ~0.80 comes precisely from
  retaining a non-zero null firing rate that the cable can modulate.

* **Stochasticity absent.** Schachter2010 and the Wu2023 SAC model inject Poisson-like stochastic
  bipolar inputs; the t0022 testbed is deterministic (`reliability = 1.000` at every diameter
  multiplier). Deterministic drive collapses the rate-code integration that the Schachter2010
  dendritic-spike-threshold mechanism needs in order to amplify DSI — thresholds either cross
  every trial or none.

* **Channel substrate is lumped, not Nav1.6/Nav1.2 + Kv1/Kv3.** The Poleg-Polsky 2026 morphology
  inherited by t0022 uses the HHst lumped Na/K pair in the dendrites (see t0019 synthesis). The
  Schachter2010 active-amplification prediction depends on a distal Nav density and kinetic regime
  that is modelled in a reduced form here — scaling `seg.diam` rescales total Nav current capacity
  proportionally to surface area (`~ pi * L * d`), but does not reproduce the Nav1.6 persistent
  current that Schachter2010 identifies as the amplifier.

* **No axon / AIS.** The Schachter2010 model includes an axon initial segment with high Nav density
  that participates in the distal-to-soma amplification cascade. The t0022 channel-partition HOC
  declares `AIS_PROXIMAL`, `AIS_DISTAL`, and `THIN_AXON` `SectionList`s that are all empty on this
  morphology. The predicted amplification regime is therefore structurally unreachable.

* **Diameter range and baseline.** Wu2023 reports distal-SAC DSI saturates above diameter ~0.8 um;
  the baseline distal `seg.diam` on our morphology spans roughly 0.4-1.0 um. Our 0.5x to 2.0x sweep
  therefore covers ~0.2-2.0 um — straddling the Wu2023 saturation threshold but on a mouse DSGC
  rather than the primate SAC she modelled. A wider sweep (0.25x to 4x) would probe more extreme
  impedance regimes but risks leaving the regime where the current E-I schedule remains compatible.

* **Metric definition.** Schachter2010 and Sivyer2013 compute DSI as
  `(Rpref - Rnull) / (Rpref + Rnull)` on spike counts at physiological noise; the t0012 scorer used
  here applies the same formula on 12 directions but on deterministic integer spike counts with null
  rate exactly 0. Vector-sum DSI (Mazurek / Kagan 2020 formulation) is reported here as fallback and
  is what the slope classifier actually uses.

## Analysis

**Schachter2010 prediction vs t0030 observation.** Schachter2010 predicts that thickening a distal
dendrite with active Nav/Ca substrate raises the preferred-direction spike-DSI via a ~4x
amplification from passive PSP DSI ~0.20 to spike DSI ~0.80 [Schachter2010, Overview]. Translated to
our sweep axis this is a **positive** slope on DSI vs diameter: more Nav per unit length = greater
preferred-direction threshold crossing. Our observation is vector-sum DSI **0.635-0.665** across 4x
diameter with slope **+0.0083 per log2(multiplier)**, p=**0.1773** and 95% CI spanning zero
(-0.0053, +0.0220). The sign matches Schachter2010's prediction but the magnitude is ~**50x**
smaller than the ~0.6 DSI movement that Schachter2010's ~4x amplification would imply; more
importantly, the p-value exceeds 0.05 and the DSI range at extremes (**0.0124**) is well below the
0.05 threshold the t0030 classifier requires to declare an active-amplification signature. The t0030
result therefore **does not support** Schachter2010 active amplification on this testbed.

**Passive-filtering prediction vs t0030 observation.** Passive cable theory predicts input impedance
scales as `Z ~ 1/d^1.5`; thicker distal = lower local depolarisation per synaptic current, so the
directional contrast should be damped at the soma and DSI should **decrease** with diameter. Our
observation is a **positive** slope (though statistically flat), which is the **opposite sign** of
the passive-filtering prediction, and the DSI range at extremes is again below any classifier
threshold for a significant negative slope. The passive-filtering prediction is also not supported.

**Why the discriminator failed: ceiling + desensitised secondary metric.** The primary DSI was
expected to move above 0.05 as distal diameter changed by 4x. It did not — every diameter hits the
same 1.000 ceiling because the t0022 E-I schedule deposits a 12-nS null-direction GABA shunt 10 ms
before AMPA arrival, zeroing null firing independently of distal biophysics. The fallback vector-sum
DSI does retain some residual sensitivity because it integrates the full 12-angle curve and captures
off-null angles where a single spike can change the vector magnitude; but that sensitivity is too
weak (**0.030** absolute range across 4x diameter) to distinguish mechanisms at the resolution the
task calls for. The sibling t0029 length sweep observed an even slightly larger vector-sum range
(**0.021**) and was also classified flat — the two morphology axes fail in the same way because
the same E-I schedule dominates both.

**Wu2023 saturation consistency.** Wu2023's primate SAC model reports distal-diameter DSI saturation
above ~0.8 um. Our baseline distal diameters sit near this threshold; our sweep covers ~0.2-2.0 um
across the 0.5x-2.0x range; and the observed flat DSI is qualitatively consistent with operating in
the saturated regime Wu2023 identifies. This is an aesthetic agreement with published work, but it
does not discriminate between the two mechanism hypotheses the t0030 task posed — both mechanisms
predict non-flat curves away from saturation, and our testbed cannot exit saturation without a
schedule change.

**Peak firing rate trend is real but DSI-irrelevant.** Peak firing declines monotonically from 15 Hz
(0.5x-1.0x) to 13 Hz (1.75x-2.0x) with slope p=**0.0075** — a statistically significant peak-Hz
decrease with diameter, consistent with thicker dendrites requiring more current to reach spike
threshold (reduced input impedance). But the same peak-Hz trend does **not** translate to a DSI
trend because null firing stays at 0 Hz across the whole sweep. In Schachter2010's regime (where
null is non-zero and stochastic), a peak-Hz drop without a compensating null-Hz drop would
immediately show up as a DSI decrease. On this testbed the denominator is empty, so the numerator
trend is invisible.

**Implications for the t0033 joint morphology-channel optimisation.** The planned joint optimisation
task must either (a) re-weight its objective toward vector-sum DSI (which retained weak sensitivity
here) and accept the ~0.03 dynamic range as the measurable signal, (b) modify the t0022 E-I schedule
so the null half-plane is not identically silenced (e.g. reduce `GABA_CONDUCTANCE_NULL_NS` from 12
nS to ~4-6 nS closer to Schachter2010's compound null inhibition), or (c) add a stochasticity layer
(Poisson background release per distal dendrite) to break the deterministic 1.000 plateau. Without
one of these, distal morphology parameters are nullified within the optimiser and no
morphology-channel interaction can be discovered. The cleanest prescription — likely to preserve
the testbed's DS mechanism while restoring discriminator sensitivity — is (b) combined with (c):
bring the schedule closer to the Schachter2010 regime and re-run both the t0029 length sweep and the
t0030 diameter sweep.

## Limitations

* **DSI-pinned-at-1 eliminates the primary discriminator.** The primary DSI is saturated at every
  multiplier; both mechanism hypotheses are consistent with a constant 1.000 ceiling, so neither is
  falsified. This is a genuine null result on the mechanism-discrimination question and must be
  reported as such. The fallback vector-sum DSI retains weak sensitivity but its 0.012 range at
  extremes is well below the 0.05 threshold the task classifier requires.

* **No subthreshold PSP-DSI measurement.** Schachter2010's key comparison is between PSP DSI (~0.20)
  and spike DSI (~0.80), which quantifies the dendritic-spike-amplification step. The t0022 driver
  emits only spike-count tuning; the PSP-DSI axis that would tie directly to Schachter2010's
  headline 4x amplification is not produced and cannot be compared in the Comparison Table — hence
  the n/a row.

* **No direct passive-filtering DSI-vs-diameter sweep in the corpus.** The passive-filtering
  prediction comes from cable theory (`Z ~ 1/d^1.5`) via the t0027 synthesis rather than from a
  single paper's quantitative sweep. No paper in the t0030 research corpus reports an equivalent
  DSI-vs-diameter sweep on a mouse ON-OFF DSGC at the resolution we ran here — the closest is the
  Wu2023 primate SAC sweep which reports a saturation threshold but not the shape above it.

* **Diameter range below Schachter2010's impedance gradient.** Schachter2010's measurement of
  150-200 MOhm proximal -> >1 GOhm distal impedance spans a ~5-7x gradient driven by large diameter
  changes along the arbor. Our 0.5x-2.0x uniform sweep is a 4x range; a wider, non-uniform
  perturbation (e.g., tapered distal-to-proximal thickening) might reveal mechanisms the
  marginal-sweep structure misses.

* **Uniform-multiplier-only.** The sweep applies one multiplier to every distal leaf. Non-uniform
  diameter changes (proximal-to-distal tapering, single-branch thickening) could expose mechanisms
  that the uniform sweep averages out.

* **Lumped HHst channel substrate.** The dendritic channels are a lumped HHst Na/K pair rather than
  the Nav1.6 / Nav1.2 / Kv1.2 / Kv3 priors that t0019 recommends. The Schachter2010 predicted
  amplification depends on kinetics this substrate does not fully reproduce. A re-run with the t0019
  channel set (future t0033 joint optimisation) is needed before the null result can be claimed to
  cover Schachter2010's mechanism in full.
