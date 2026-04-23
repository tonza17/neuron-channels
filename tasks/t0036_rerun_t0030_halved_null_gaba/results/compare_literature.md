---
spec_version: "1"
task_id: "t0036_rerun_t0030_halved_null_gaba"
date_compared: "2026-04-22"
---
# Comparison with Published Results

## Summary

This task halved the null-direction GABA conductance from **12 nS** to **6 nS** — matching the
compound null inhibition reported by Schachter2010 [Schachter2010, Architecture/Methods p. 3] —
with the explicit goal of unpinning null-direction firing on the t0022 testbed and restoring a
measurable primary-DSI dynamic range across the 0.5×-2.0× distal-diameter sweep. **The
Schachter2010-derived rescue hypothesis is falsified**: mean null-direction firing stayed at exactly
**0.00 Hz** at every diameter multiplier, primary DSI remained pinned at **1.000**, and the
classifier emitted the `flat_partial` label with a pre-condition-failure flag. The fallback
vector-sum DSI moved by only **0.011** absolute (range 0.579-0.590, slope **+0.0049**, p=**0.019**)
— statistically distinguishable from zero but three orders of magnitude below the ~**0.6** DSI
movement Schachter2010 reports between PSP and spike regimes.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Schachter2010 compound null inhibition [Schachter2010, Architecture/Methods p. 3] | null_GABA (nS) | 6.0 | 6.0 | +0.0 | GABA level matched exactly by t0036 override |
| Schachter2010 rescue hypothesis (S-0030-01) [Schachter2010, Architecture/Methods p. 3; t0030 compare_literature.md Analysis] | mean null firing at 1.0× (Hz) | >= 0.1 | 0.00 | **-0.1** | Pre-condition failed; halving did not unpin null firing on deterministic t0022 |
| Schachter2010 spike-DSI ceiling [Schachter2010, Abstract; Overview p. 1] | spike DSI | 0.80 | 1.000 | **+0.200** | Our testbed remains saturated above Schachter2010's spike-DSI value even after GABA halving |
| Schachter2010 PSP-to-spike amplification [Schachter2010, Overview p. 1] | DSI change (PSP -> spike) | ~0.60 | 0.011 | **-0.589** | Vector-sum range across 4x diameter is three orders of magnitude below the dendritic-Nav amplification step |
| Schachter2010 active-amplification prediction [Schachter2010, Overview p. 1] | DSI vs diameter slope sign | positive | +0.0049 | n/a | Sign matches Schachter2010 but magnitude negligible; primary DSI discriminator saturated at 1.000 |
| Passive filtering (cable theory via t0027 synthesis) [Wu2023, abstract via t0027 full_answer.md:108-113] | DSI vs diameter slope sign | negative | +0.0049 | n/a | Sign is opposite Wu2023's Z~1/d^1.5 prediction; passive filtering also not supported |
| Sivyer2013 rabbit DSGC control DSI [Sivyer2013, Fig. 2-3 text via t0002 summary] | spike DSI | ~1.0 | 1.000 | **+0.000** | Qualitative match but uninformative because ceiling is schedule-driven, not biophysical |

### Prior Task Comparison

The t0036 task plan cites two prior tasks as direct comparators: **t0030** (same diameter sweep on
t0022 at 12 nS GABA — the "before schedule fix" baseline) and **t0035** (same diameter sweep on
the t0024 AR(2) testbed). The t0034 length sweep on t0024 provides a second cross-testbed reference.
All four rows below compare t0036's halved-GABA result against those prior measurements.

| Prior Task / Source | Metric | Prior Value | t0036 Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0030 (same sweep, GABA=12 nS) | mean null firing (Hz) | 0.00 | 0.00 | **+0.00** | Halving GABA produced zero change — the core negative finding |
| t0030 (same sweep, GABA=12 nS) | primary DSI range across extremes | 0.000 | 0.000 | **+0.000** | Pinned at 1.000 in both cases; GABA halving did not unpin |
| t0030 (same sweep, GABA=12 nS) | vector-sum DSI range across extremes | 0.012 | 0.011 | **-0.001** | Marginal contraction of the fallback range despite halved GABA |
| t0030 (same sweep, GABA=12 nS) | vector-sum DSI slope (per log2 mult) | +0.0083 | +0.0049 | **-0.0034** | Slope halved and now statistically significant (p=0.019 vs t0030 p=0.177) but absolute range below practical threshold |
| t0035 (diameter sweep on t0024 AR(2)) | mean null firing (Hz) | 0.50-0.80 | 0.00 | **-0.50 to -0.80** | AR(2) stochasticity keeps null firing non-zero; halved-GABA on deterministic t0022 does not |
| t0035 (diameter sweep on t0024 AR(2)) | primary DSI range | 0.680-0.808 | 1.000 (pinned) | n/a | t0024 preserves a measurable primary DSI dynamic range that t0022 cannot produce, even with halved GABA |
| t0035 (diameter sweep on t0024 AR(2)) | primary DSI slope (per log2 mult) | 0.0041 (p=0.88) | 0.000 (pinned) | n/a | Both testbeds produce flat diameter-axis slopes; only t0035 produces a measurable primary signal |
| t0034 (length sweep on t0024 AR(2)) | primary DSI slope | -0.1259 (p=0.038) | n/a | n/a | Length modulates primary DSI on t0024; diameter does not; t0022 cannot even produce the measurement |

The lineage-internal finding is decisive: **the rescue hypothesis is falsified at 6 nS on the t0022
deterministic schedule**, and the only testbed in the project where primary DSI remains measurable
on any morphology axis is **t0024 with AR(2)** (t0034 length sweep, t0035 diameter sweep). Halving
the conductance alone does not substitute for stochastic release.

## Methodology Differences

* **Deterministic t0022 schedule vs Schachter2010 stochastic drive.** The t0022 testbed delivers one
  AMPA and one GABA event per dendrite per trial at seeded, fixed onset times, with GABA leading
  AMPA by 10 ms on null trials. Schachter2010 uses a full drifting-bar simulation with SAC-derived
  presynaptic DS templates and Poisson-like stochastic release
  [Schachter2010, Architecture/Methods p. 3]; their non-zero null spike rate emerges from the
  stochastic release tail, not from the peak GABA conductance alone. Halving the peak conductance
  without adding stochasticity does not reproduce the near-threshold spike escape Schachter2010's
  regime requires.

* **Timing lead preserved at 10 ms.** The t0022 driver keeps GABA leading AMPA by 10 ms at the null
  direction. Schachter2010 reports per-input spatially offset inhibition within ~20 um of each
  excitatory input [Schachter2010, Architecture/Methods p. 3]; the integrated kinetic profile, not
  the peak, is the operative variable. The t0036 intervention scaled peak only; the timing lead
  remained at the t0022 default.

* **Channel substrate is HHst-lumped, not Nav1.6 + Kv1/Kv3 + Ca.** Schachter2010 uses a fast
  Nav1.6-like sodium channel plus delayed rectifier Kv, A-type Kv4, Ca, and Ca-activated K currents
  [Schachter2010, Architecture/Methods p. 3]. The t0022 morphology inherits the Poleg-Polsky 2026
  HHst Na/K lumped pair; scaling `seg.diam` rescales total Nav current with surface area but does
  not reproduce the persistent Nav1.6 current Schachter2010 identifies as the amplifier.

* **No AIS.** The t0022 channel partition declares AIS_PROXIMAL, AIS_DISTAL, and THIN_AXON section
  lists that are empty on this morphology. Schachter2010's model includes a high-Nav AIS that
  participates in the distal-to-soma amplification cascade.

* **Uniform diameter multiplier, no tapering.** Our 0.5×-2.0× sweep applies one multiplier to all
  177 identified distal leaves. Schachter2010's 150-200 MOhm proximal -> >1 GOhm distal impedance
  gradient arises from tapered, non-uniform diameters along the arbor
  [Schachter2010, Architecture/Methods p. 3]; a uniform-multiplier sweep cannot probe that regime.

* **DSI definition is identical but input distribution is not.** Both studies compute
  `DSI = (R_pref - R_null) / (R_pref + R_null)` on 12-direction spike counts. On the t0022 testbed
  `R_null = 0` at every trial (deterministic + 6 nS GABA still sufficient to clamp), collapsing the
  ratio to 1.000 before biophysics can modulate it. Vector-sum DSI (Mazurek/Kagan 2020 formulation)
  retains weak sensitivity and is what the slope classifier used in fallback mode.

## Analysis

**The Schachter2010 conductance-matching hypothesis is falsified on the t0022 deterministic
schedule.** The plan's central prediction — that moving GABA from 12 nS (roughly 2×
Schachter2010) to 6 nS (matching Schachter2010's compound null inhibition) would restore non-zero
null firing — was tested cleanly and failed. Mean null-direction firing stayed at exactly **0.00
Hz** at every diameter, primary DSI stayed pinned at **1.000**, and the pre-condition gate built
into the classifier flagged the sweep as `flat_partial`. This is a stronger negative finding than
t0030 provided, because t0030 could be explained by "GABA is too strong"; t0036 rules out that
explanation at the Schachter2010 level. The failure therefore implicates either **timing dominance**
(the 10 ms pre-AMPA GABA lead matters more than the peak conductance) or **the absence of stochastic
release** (deterministic drive cannot produce the near-threshold spike tail Schachter2010's regime
depends on) as the true rate-limiter.

**Vector-sum DSI slope acquired statistical significance but lost magnitude.** Compared to t0030,
the halved-GABA sweep produced a vector-sum DSI slope of **+0.0049** per log2(multiplier) with
p=**0.019** — below the 0.05 threshold, unlike t0030's p=**0.177**. But the absolute DSI range
across the sweep contracted from **0.012** (t0030) to **0.011** (t0036), and the slope magnitude
halved. This combination (more significant slope, smaller range) is the statistical fingerprint of a
tighter null distribution rather than a genuine mechanism signal — halving GABA reduced
trial-to-trial noise-equivalent fluctuations in the vector sum without introducing any
null-direction firing. The sign still matches Schachter2010's positive prediction but the magnitude
is three orders of magnitude below Schachter2010's PSP-to-spike amplification of ~0.6 DSI units
[Schachter2010, Overview p. 1].

**Cross-testbed comparison strengthens the stochasticity attribution.** t0035 (the matched diameter
sweep on t0024 with AR(2) release) produced a flat DSI-vs-diameter slope (**+0.0041**, p=**0.88**)
but with a **measurable primary DSI dynamic range of 0.128** (0.680-0.808), while t0036's primary
DSI range remained **0.000**. Both testbeds agree that the **diameter axis is a weak discriminator**
for either mechanism; they disagree on whether a primary-DSI measurement is even recoverable. The
only testbed-axis combination in the project where primary DSI varies meaningfully is **t0024 +
length** (t0034, slope **-0.1259**, p=**0.038**) — and that signal is cable-filtering-shaped, not
Schachter-amplification-shaped. The pattern across t0030/t0034/t0035/t0036 is consistent:
Schachter2010's active-amplification prediction is not observable on any of these testbeds, and the
one testbed where the discriminator works at all (t0024 length) leans toward passive filtering.

**Implications for the t0033 joint morphology-channel optimiser.** Three options follow from this
result. (1) **Abandon t0022 for primary-DSI objectives.** The deterministic testbed cannot support
the peak-minus-null metric on any morphology axis, even at Schachter2010-matched GABA — the
optimiser should default to t0024 with AR(2) for any task whose objective is primary DSI. (2) **Use
vector-sum DSI if t0022 is required.** The fallback retains ~0.01 absolute sensitivity, enough to
register the peak-firing-rate trend already visible in t0030 and t0036 but not to discriminate
Schachter2010 from passive filtering. (3) **Adopt a stochasticity or timing intervention.** Poisson
background release (S-0030-02) or reducing the 10 ms GABA pre-AMPA lead would plausibly restore the
null tail, but neither has been tested and both constitute schedule mutations beyond the single-knob
parameter space the current optimiser is designed for. The clean recommendation is (1): **the t0033
optimiser should prefer t0024 + primary DSI, or t0022 + vector-sum DSI, and should not rely on the
t0022 + primary DSI combination.**

## Limitations

* **Single GABA value tested.** t0036 tested exactly one intermediate point (6 nS). It is possible
  — though not predicted by creative_thinking — that further reductions to 4, 2, or 1 nS would
  unpin null firing. Follow-up suggestion S-0036-01 is queued to sweep this axis.

* **Timing axis unexplored.** The 10 ms GABA-leads-AMPA interval was kept at its t0022 default.
  Creative_thinking hypothesis #2 identifies timing as a plausible dominant variable; this task did
  not vary it.

* **Schachter2010 spike-DSI ceiling comparison is confounded by schedule.** Our DSI=1.000 does not
  quantitatively exceed Schachter2010's DSI=0.80 because it comes from a schedule-clamped null
  denominator, not from a stronger active-amplification mechanism. The +0.200 delta in the
  comparison table is a methodological artefact, not a biological finding.

* **Schachter2010 PSP-DSI axis not measured.** The t0022 driver emits spike-count tuning only; the
  PSP-DSI axis (~0.20 in Schachter2010) that would isolate the dendritic-spike-amplification step is
  not produced and cannot be compared.

* **Distal voltage traces not captured.** The trial runner records `peak_mv` per trial but not the
  full voltage time course at null direction. Creative_thinking hypothesis #4 (distal Nav
  sub-threshold at null) cannot be confirmed without trace data.

* **Only one paper's quantitative null-GABA estimate exists in the corpus.** Wu2023's passive
  filtering prediction is derived from cable theory (`Z ~ 1/d^1.5`) via the t0027 synthesis rather
  than from a direct DSI-vs-diameter sweep. No paper in the t0036 research corpus reports a
  GABA-reduction rescue of primary DSI on a deterministic DSGC simulation, so the negative result
  cannot be cross-validated against a direct published precedent.
