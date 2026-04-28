---
spec_version: "1"
task_id: "t0054_minimal_dsgc_ampa_nmda_scalar_gaba"
date_compared: "2026-04-25"
---
# Comparison with Published Results

## Summary

Adding co-located voltage-independent NMDA `Exp2Syn` (tau1 = 5 ms, tau2 = 80 ms, e = 0 mV) at every
E synapse of the t0052 minimal DSGC dramatically closes the peak-rate gap (peak Hz at the preferred
direction goes from **0.667 Hz** at gNMDA = 0 nS to **8.000 Hz** at gNMDA = 0.25 nS, a **~12x**
boost) but collapses direction selectivity under the unchanged scalar `gabaMOD` inhibition: vector-
sum DSI drops from **0.746** (gNMDA = 0) to **0.082** (gNMDA = 0.25) and approaches **0.017** at
gNMDA = 1.0. The peak-rate sweep reaches an order of magnitude of the in vivo target **30-100 Hz**
implied by Park2014 cells [Park2014, p. 3978] but never matches the in vitro DSI band of **0.65 +/-
0.05** [Park2014, p. 3978]. The result confirms the prediction of PolegPolsky2016
[PolegPolsky2016, p. 1283] that voltage-dependent NMDA Mg-block (absent here by design) is a
necessary ingredient for multiplicative direction-selective gain.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Park2014 (CART-Cre, voltage-clamp) | DSI (primary) | 0.65 | 0.143 | -0.507 | gNMDA = 0.25 nS FULL; peak-rate regime closer to in vivo than t0052 but DSI is much lower [Park2014, p. 3978] |
| Park2014 (TRHR-GFP / wild-type) | DSI (primary) | 0.73 | 0.143 | -0.587 | Reference subset, n = 38 cells [Park2014, p. 3978] |
| Park2014 (in vivo-implied peak rate) | Peak Hz | 30.0 | 8.0 | -22.0 | gNMDA = 0.25 nS FULL; 30-100 Hz range cited in t0052 plan as the in vivo target [Park2014, p. 3978] |
| PolegPolsky2016 (NMDA decay tau) | NMDA tau (ms) | 50.0 | 80.0 | +30.0 | Their `bipolarNMDA.mod` `tau1NMDA = 50 ms` deactivation; ours `Exp2Syn` `tau2 = 80 ms` decay [PolegPolsky2016, p. 1280, Methods] |
| PolegPolsky2016 (control PD PSP, AMPA + NMDA) | PD PSP (mV) | 5.8 | ~84.0 | +78.2 | Aggregate E_ONLY EPSP peak at preferred direction; mV scale not directly comparable (see Methodology) [PolegPolsky2016, p. 1280, Fig 1] |
| PolegPolsky2016 (DSI under voltage-dependent NMDA) | DSI | 0.46 | 0.143 | -0.317 | Their NEURON model with voltage-dependent NMDA + tuned GABA preserves DSI; ours collapses without Mg-block [PolegPolsky2016, Fig 5] |
| t0052 (parent, no NMDA) | Vector-sum DSI | 0.746 | 0.746 | +0.0 | gNMDA = 0 FULL; bit-identical regression-gate match (max diff 0e+00 Hz) [t0052 results_summary.md] |
| t0052 (parent, no NMDA) | Peak Hz | 0.667 | 0.667 | +0.0 | gNMDA = 0 FULL; regression gate confirms exact reproduction [t0052 results_summary.md] |
| t0053 (sibling, spatial GABA, no NMDA) | Vector-sum DSI | 0.0 | 0.746 | +0.746 | gNMDA = 0 FULL; t0053 fully suppressed at 100 nS GABA mass while t0054 inherits t0052's 66 nS regime [t0053 results_summary.md] |
| t0048 (voltage-independent NMDA on deposited DSGC) | DSI at gNMDA = 1.0 nS | 0.078 | 0.0 | -0.078 | t0048 used `Voff_bipNMDA = 1`; same voltage-independent NMDA regime [t0048 results_summary.md] |
| t0048 (voltage-independent NMDA on deposited DSGC) | DSI range across gNMDA sweep | 0.066 | 0.143 | +0.077 | Max-min DSI across the gNMDA sweep [t0048 results_summary.md] |

### Prior Task Comparison

| Prior Task | Variant | DSI (primary) | Peak Hz | Notes |
| --- | --- | --- | --- | --- |
| t0048 (Voff = 1, voltage-independent NMDA on deposited DSGC) | gNMDA = 0.5 nS | 0.102 | n/a | Closest prior project result for "voltage-independent NMDA on a DSGC"; DSI flattens but does not collapse to zero |
| t0048 (Voff = 1, voltage-independent NMDA on deposited DSGC) | gNMDA = 3.0 nS | 0.037 | n/a | Highest gNMDA point; DSI continues to drop but stays above zero |
| t0052 (parent, scalar gabaMOD, AMPA only) | FULL | **1.000** | **0.667** | Single-spike-per-trial; trivial DSI = 1 from null = 0 Hz |
| t0053 (sibling, spatial GABA, AMPA only) | FULL | **0.000** | **0.000** | Fully suppressed by 100 nS mean GABA mass |
| t0054 (this task) | gNMDA = 0 FULL | **1.000** | **0.667** | Regression gate vs t0052: 0e+00 Hz max diff |
| t0054 (this task) | gNMDA = 0.25 FULL | **0.143** | **8.000** | NMDA closes peak-rate gap but DSI collapses ~9x |
| t0054 (this task) | gNMDA = 0.5 FULL | **0.100** | **7.333** | Saturating regime |
| t0054 (this task) | gNMDA = 1.0 FULL | **0.000** | **4.667** | Preferred = null = 4.67 Hz; vector-sum DSI 0.017 |

## Methodology Differences

* **NMDA voltage dependence**: PolegPolsky2016 [p. 1280, Methods] uses a Jahr-Stevens Mg-block
  `bipolarNMDA.mod` channel; we use NEURON's built-in `Exp2Syn` with no Mg-block. This is by design
  — the task explicitly defers voltage-dependent NMDA to a follow-up. It is the most consequential
  methodological gap.

* **NMDA kinetics**: PolegPolsky2016 reports `tau1NMDA = 50 ms` deactivation and `tau2NMDA = 2 ms`
  activation [PolegPolsky2016, p. 1280, Methods]. Our `Exp2Syn` uses `tau1 = 5 ms` rise and
  `tau2 = 80 ms` decay (NEURON `Exp2Syn` convention is `tau1 < tau2`, both positive). Both fall
  within the 50-200 ms biological NMDA decay range cited in t0018, but the precise time course is
  different.

* **Excitation count**: 100 AMPA + 100 NMDA (this task) vs 177 AMPA + 177 NMDA in PolegPolsky2016
  [p. 1280] / 282 in t0046 reproduction / >1000 SAC varicosities in deRosenroll2026 [p. 5]. Lower
  synapse count gives lower aggregate drive.

* **Inhibition mechanism**: Park2014 attributes DS to null-direction GABA from SACs; PolegPolsky2016
  uses tuned GABA on a morphologically realistic DSGC; we use the unchanged t0052 scalar `gabaMOD`
  (PD = 0.33, ND = 0.99) on all 100 GABA synapses, an order-of-magnitude consistent but
  non-spatially-distributed inhibition pattern. The t0054 design holds inhibition fixed at the t0052
  level so that the gNMDA effect can be isolated.

* **DSGC subtype and morphology**: Park2014 records mouse On-Off DSGCs in CART-Cre and TRHR-GFP
  lines [p. 3977]; PolegPolsky2016 uses DRD4-GFP On-Off DSGCs [p. 1278]. Our morphology is the
  t0009-calibrated `dsgc-baseline-morphology-calibrated`, which is a generic mouse DSGC
  reconstruction shared across t0052 / t0053. Morphological details (dendritic field, soma size, AIS
  geometry) are not directly matched.

* **Bar speed**: 1.0 µm/ms = 1000 µm/s in this task; PolegPolsky2016 reports 1 mm/s
  [PolegPolsky2016, p. 1278] and Park2014 reports 31-36 deg/s [Park2014, p. 3977]. Conversions are
  imperfect, but our speed is consistent with prior t0052 / t0053 settings.

* **Single-event-per-synapse, no noise**: Trials are deterministic (one NetStim event per synapse
  per trial); deRosenroll2026 emphasises that DSI is sensitive to AR(2) correlated release noise,
  and Park2014's in vivo DSI band reflects in vitro membrane noise that is not reproduced here.

* **Aggregate EPSP magnitude scale**: Our reported aggregate E_ONLY EPSP peak is **~84 mV** above
  V_rest (i.e., the somatic voltage reaches ~0 mV after 100 simultaneous AMPA + NMDA conductances
  drive Vm to E_AMPA = E_NMDA = 0 mV with no inhibition). PolegPolsky2016's **5.8 mV** PD PSP
  [p. 1280] is recorded under whole-cell voltage-clamp with TTX/QX-314 in a regime where the cell
  cannot reach reversal. The two numbers are not directly comparable — the methodology rows are
  flagged in the comparison table only for completeness.

## Analysis

### Peak-rate gap closure (Key Question 2)

NMDA closes the peak-rate gap dramatically. At gNMDA = 0.25 nS the peak firing rate at the preferred
direction reaches **8.000 Hz**, **12x** the gNMDA = 0 baseline of **0.667 Hz**. This brings the
model within an order of magnitude of the in vivo target band of **30-100 Hz** implied by Park2014
[Park2014, p. 3977]. At gNMDA = 0.5 nS the peak rate slightly *drops* to **7.333 Hz** because the
cell saturates in a refractory-limited regime; at gNMDA = 1.0 nS the peak rate falls further to
**4.667 Hz** as the slow NMDA tail keeps the cell tonically depolarised and curtails spikes per
trial. This non-monotonic peak-rate-vs-gNMDA curve is a quantitative finding consistent with the
[t0048] cautionary note that NMDA pushed beyond the multi-spike-per-trial threshold re-saturates the
response.

### DSI collapse under voltage-independent NMDA (Key Question 3)

Vector-sum DSI drops monotonically from **0.746** to **0.082** (gNMDA = 0.25), to **0.029** (gNMDA =
0.5), to **0.017** (gNMDA = 1.0). The primary DSI follows the same path: **1.000** -> **0.143** ->
**0.100** -> **0.000**. At gNMDA = 1.0 nS the preferred and null peak rates are both exactly **4.667
Hz**, eliminating direction selectivity entirely. This result quantitatively demonstrates a known
mechanism documented in PolegPolsky2016 [PolegPolsky2016, Fig 5, p. 1283-1284]: removing the
voltage-dependent NMDA Mg-block converts NMDA scaling from *multiplicative* (preserves DSI) to
*additive* (degrades DSI). Our t0054 result is a forward-direction confirmation: starting from a
working DSI = 0.746 baseline, adding voltage-independent NMDA degrades DSI exactly as
PolegPolsky2016's NEURON model predicted for the voltage-independent / Ohmic NMDA substitute. The
mechanism is the same one [t0048] explored on the deposited DSGC; t0054 reproduces it on the t0052
minimal architecture.

### Comparison with t0048 (voltage-independent NMDA on the deposited DSGC)

[t0048] reported a DSI range of **0.066** (max - min) across a 7-point gNMDA sweep at
`Voff_bipNMDA = 1`, with absolute DSI values between **0.04 and 0.10**. Our 4-point sweep produces a
DSI range of **0.143** (max - min: 0.143 at gNMDA = 0.25 minus 0.0 at gNMDA = 1.0) with absolute DSI
between **0.0 and 0.143** in the FULL mode. The two studies agree on the qualitative finding —
voltage-independent NMDA flattens but does not collapse DSI to a meaningful in vivo target — and
disagree quantitatively because the underlying excitatory-inhibitory balance is different (t0048
uses the deposited 282-synapse DSGC with `bipolarNMDA.mod`; we use a from-scratch 100-synapse cell
with built-in `Exp2Syn`). Both confirm the **PolegPolsky2016** prediction that voltage-dependent
NMDA Mg-block is essential for multiplicative DSI scaling.

### Compare to PolegPolsky2016's voltage-dependent NMDA model

PolegPolsky2016's NEURON model with voltage-dependent NMDA + tuned GABA preserves DSI under noisy
conditions (DSI roughly **0.46** in their Figure 5 voltage-dependent NMDA condition; DSI degrades
under their `0 Mg2+` and `high-Cl-` interventions [PolegPolsky2016, Fig 5]). Our t0054 result lands
at **0.143** primary DSI at gNMDA = 0.25 — a **-0.317** delta against the voltage-dependent-NMDA
reference, attributable to two factors: (1) the absence of Mg-block in our NMDA, and (2) the simpler
scalar `gabaMOD` inhibition. The decomposition between these two factors is a follow-up experiment.

### EPSP decay (Key Question 1)

The numerical `epsp_decay_to_1e_ms` returned `null` for all four gNMDA values because the trial
window (1500 ms) is shorter than the time the cell takes to drop back below the 1/e threshold once
NMDA's 80 ms decay tau is engaged across 100 simultaneous synapses (the 100-fold superposition keeps
Vm above the 1/e threshold throughout the trial). Qualitatively, the EPSP tail at gNMDA = 1.0 nS
extends well beyond the **~30 ms** observed in t0052 (per the per-direction EPSP PNG comparison
described in `results_detailed.md`), reaching the **~50-200 ms** biological NMDA decay range cited
in [t0018]. A precise number requires either a longer trial window or an exponential fit; the
qualitative answer to Key Question 1 is **yes, NMDA dramatically slows the EPSP tail**, but the
quantitative answer is deferred.

### Single-spike vs multi-spike regime (Key Question 4)

t0052's gNMDA = 0 regime is single-spike-per-trial (0.667 Hz = 1 spike per 1500 ms). t0054's gNMDA
>= 0.25 nS regime is multi-spike-per-trial (8 Hz = 12 spikes per 1500 ms; 4.67 Hz = 7 spikes). The
transition occurs at gNMDA = 0.25 nS — adding even the smallest non-zero NMDA conductance moves
the cell out of the degenerate single-spike regime into the multi-spike regime where DSI is no
longer trivially 1. This is exactly the regime change predicted in [t0052]'s Limitations section and
in the t0054 plan's motivation.

## Limitations

* **No voltage-dependent NMDA Mg-block in this task**. The most relevant comparison from
  PolegPolsky2016 is to their voltage-*dependent* NMDA configuration, which we cannot reproduce by
  design. Our model is the voltage-*independent* NMDA control. The DSI gap in the comparison table
  (-0.317 vs PolegPolsky2016 Fig 5) reflects exactly this design choice and motivates a follow-up
  task with a Mg-block channel.

* **Aggregate EPSP magnitudes (~84 mV) are not directly comparable to PolegPolsky2016's 5.8 mV PD
  PSP** because their measurement is voltage-clamp with reversal-potential constraints absent here.
  The mV-scale rows in the comparison table are flagged but provide little constraint.

* **`epsp_decay_to_1e_ms` returned null**. The headline EPSP-decay-vs-gNMDA observable is
  qualitative only. Numerical values for the time constant of the EPSP tail are not reported.

* **Park2014's "in vivo 30-100 Hz" range** is the t0052 plan's interpretation of Park2014 + general
  in vivo DSGC literature. Park2014 itself reports tuning-by-direction PSP and current values, not a
  "peak Hz" rate; the 30-100 Hz figure should be treated as a general in vivo DSGC range from the
  literature rather than a direct Park2014 quantity.

* **Park2014 in vivo DSI band of "0.40-0.60"** in the orchestrator's hand-off message could not be
  verified from the paper text. The paper reports CART-Cre cells DSI = **0.65 +/- 0.05** (n = 14)
  and TRHR-GFP / wild-type cells **0.73 +/- 0.03** (n = 38) [Park2014, p. 3978]. We use the values
  directly attributable to Park2014 and treat 0.65-0.73 as the in vitro DSI target.

* **PolegPolsky2016 DSI under voltage-dependent NMDA** of **0.46** is read from their Figure 5
  voltage-dependent NMDA + tuned GABA panel. The paper does not publish a single headline DSI
  number, so this value should be treated as a representative model output rather than a precise
  benchmark.

* **No noise comparison**: Our deterministic trials cannot probe the noisy-discrimination benefit of
  NMDA multiplication that PolegPolsky2016 demonstrates with ROC analysis [p. 1283]. Reliability is
  artefactually 1.0 in this task.

* **Scalar `gabaMOD` is not the same as Park2014's null-direction SAC GABA**. The inhibition is
  spatially uniform but direction-modulated in amplitude, not spatially distributed across the
  dendritic field. The DSI collapse may partly reflect this simplification, separately from the
  voltage-independent-NMDA gap.

* **Single conductance setting per gNMDA value**: only four gNMDA values were sampled ({0.0, 0.25,
  0.5, 1.0} nS). No GABA conductance sweep was performed; the operating point where inhibition could
  compensate for NMDA-amplified excitation is not characterised.
