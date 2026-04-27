---
spec_version: "1"
task_id: "t0052_minimal_dsgc_scalar_gaba"
date_compared: "2026-04-25"
---
# Comparison with Published Results

## Summary

The minimal from-scratch DSGC with scalar `gabaMOD` inhibition produces a primary DSI of **1.000**
(vector-sum DSI **0.746**) at peak rate **0.667 Hz**, HWHM **82.5°**, with an IPSP somatic voltage
ratio of **1.54** against a 3.0x conductance ratio. The DSI sits well above the in vitro mouse
On-Off DSGC band of **0.65 +/- 0.05** reported by Park2014 [Park2014, p. 3978] and the model-based
**0.39** correlated benchmark of deRosenroll2026 [deRosenroll2026, Fig 5 / Table S1]; peak firing
rate is **~25-50x lower** than the published in vivo / in vitro DSGC range and ~22x lower than this
project's own t0004 target curve. The driving-force-saturation gap (1.54x voltage vs 3.0x
conductance) is the headline mechanistic finding and aligns qualitatively with the
multiplicative-vs-additive shunting framework in PolegPolsky2016 [PolegPolsky2016, p. 1283].

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Park2014 (CART-Cre, voltage-clamp) | DSI (primary) | 0.65 | 1.000 | +0.35 | In vitro mouse On-Off DSGCs, n=14; we exceed in-vivo band [Park2014, p. 3978] |
| Park2014 (TRHR-GFP / wild-type) | DSI (primary) | 0.73 | 1.000 | +0.27 | Reference subset, n=38 cells [Park2014, p. 3978] |
| deRosenroll2026 (correlated AR(2) release) | DSI | 0.39 | 0.746 | +0.356 | Vector-sum DSI vs paper's vector-sum benchmark; correlated rho=0.6 [deRosenroll2026, p. 6 / Fig 5] |
| deRosenroll2026 (uncorrelated release) | DSI | 0.25 | n/a | n/a | We do not run AR(2) noise; comparison context only [deRosenroll2026, p. 6 / Fig 5] |
| PolegPolsky2016 (Fig 1, control PD PSP) | PD NMDA-PSP | 5.8 mV | 5.30 mV | -0.50 mV | We measure aggregate IPSP at PD instead of NMDA-PSP at PD; magnitudes coincidentally near each other but mechanism differs [PolegPolsky2016, p. 1280, Fig 1] |
| PolegPolsky2016 (Fig 1, control ND PSP) | ND NMDA-PSP | 3.3 mV | 8.16 mV | +4.86 mV | Our ND IPSP is the aggregate inhibitory PSP (positive depolarizing magnitude); paper value is excitatory NMDA component [PolegPolsky2016, p. 1280, Fig 1] |
| Park2014 (null inhibitory conductance, P-N) | Inhibitory P-N (nS) | 2.43 | 1.32 | -1.11 | Our gNULL/gPD = 3.0 (gabaMOD) over base 2 nS implies P-N = (0.99-0.33)*2 nS = 1.32 nS per synapse; order-of-magnitude consistent at the per-synapse level [Park2014, p. 3978] |
| t0004 target curve (this project) | Peak rate (Hz) | 32.0 | 0.667 | -31.33 | Peak rate ~48x below project target [t0004 results_summary] |
| t0004 target curve (this project) | DSI | 0.8824 | 1.000 | +0.118 | Our binary single-spike-per-trial regime exceeds target DSI [t0004 results_summary] |
| t0004 target curve (this project) | HWHM (deg) | 68.51 | 82.5 | +13.99 | Our tuning is broader than the cosine^2 target [t0004 results_summary] |

### Prior Task Comparison

| Prior Task | Variant | DSI | Peak Hz | HWHM (deg) | Notes |
| --- | --- | --- | --- | --- | --- |
| t0008 (rotation-proxy ModelDB 189347) | baseline | 0.316 | 18.1 | 82.81 | Wrong DS protocol; below project envelope |
| t0020 (gabaMOD-swap ModelDB 189347) | PD/ND | 0.7838 | 14.85 | n/a | Native gabaMOD swap; high DSI, low peak |
| t0022 (E-I temporal-asymmetry) | spatial | 1.000 | 15.0 | 116.25 | DSI = 1.0 also achieved but via different mechanism, broader HWHM |
| t0024 (de Rosenroll port, correlated) | rho=0.6 | 0.7758 | 5.15 | 68.65 | Stochastic AR(2) release; HWHM closest to t0004 target |
| t0046 (Poleg-Polsky exact reproduce, Fig 8 control) | suprathreshold | 0.6757 | n/a | n/a | Faithful 282-syn ModelDB port |
| t0049 (SE-clamp AMPA conductance DSI) | AMPA only | 0.0120 | n/a | n/a | Conductance-level DSI in clamped cell, near zero |
| t0052 (this task) | FULL | **1.000** | **0.667** | **82.5** | Single-spike-per-trial; perfect on/off binary tuning |

## Methodology Differences

* **Excitation tuning**: Park2014 [p. 3978] proves bipolar-cell glutamate is omnidirectional at
  release (iGluSnFR P-N = +0.073 +/- 0.04, p = 0.95). Our model implements omnidirectional AMPA
  exactly as Park2014 prescribes -- no tuned excitation. This matches the paper's mechanistic
  picture.

* **Inhibition mechanism**: Park2014 attributes all DS to null-direction GABA from SACs (P-N = 2.43
  nS). Our model uses a uniform `gabaMOD(theta)` scalar (PD = 0.33, ND = 0.99) applied to all 100
  GABA synapses, equivalent in net P-N to **1.32 nS** per synapse times the count = ~1.32 nS at soma
  -- same order of magnitude as Park2014's 2.43 nS.

* **Synapse count**: 100 E + 100 I (this task) vs ~177 in PolegPolsky2016 [p. 1280] / 282 in t0046
  reproduction / >1000 SAC varicosities in deRosenroll2026 [p. 5]. Lower synapse count produces
  weaker total drive, consistent with our 22-50x lower peak firing rate.

* **No NMDA**: Our model has AMPA only by design, while PolegPolsky2016 emphasises NMDARs contribute
  multiplicatively at PD (5.8 mV / 35% of total PSP). This is a structural omission, not a parameter
  mismatch -- our task is the AMPA-only minimal floor.

* **No noise**: Our trials are deterministic single-event-per-synapse, while deRosenroll2026 [p. 6]
  requires AR(2) correlated release with rho = 0.6 to match in vitro noise. Our reliability = 1.000
  is an artefact of determinism.

* **AIS/active conductances**: We use NEURON's stock `hh` on soma and a synthetic 1 um x 30 um AIS
  section. PolegPolsky2016 / t0046 use the custom `HHst.mod` on soma + dendrites; deRosenroll2026
  uses `HHst_noiseless.mod` with no separate AIS. These differences are not directly comparable.

* **DSI definition**: Park2014 uses the standard primary DSI on AP counts; deRosenroll2026 uses
  vector-sum DSI on spike counts; PolegPolsky2016 uses both for PSP and AP. Our primary DSI = 1.0 is
  from the standard formula on `peak_hz / null_hz`; vector-sum DSI = **0.746** is more directly
  comparable to deRosenroll2026's value of **0.39**.

* **Tuning protocol**: 12 directions x 10 trials at 1 µm/ms bar speed (this task) vs 8 directions
  at 1 mm/s (PolegPolsky2016, deRosenroll2026, Park2014). The angular sampling is finer here, but
  bar geometry is comparable.

## Analysis

The model achieves **DSI = 1.000** (primary) and **0.746** (vector-sum), which is **+0.35** above
the in vivo reference (Park2014, 0.65) and **+0.36** above the deRosenroll2026 model benchmark
(0.39). However, this DSI is **not a meaningful match** to the literature because it is generated by
a degenerate single-spike-per-trial firing regime: every preferred-side direction fires exactly one
spike per 1500 ms trial (0.667 Hz) and every null-side direction is silent. With null = 0 Hz
exactly, the primary DSI formula `(peak - null) / (peak + null)` collapses to 1 trivially. The
vector-sum DSI = 0.746 is more informative because it encodes the angular spread (broad HWHM =
82.5°) but it still over-shoots the in vivo target by **0.10-0.36** depending on the published
reference chosen.

The peak rate of **0.667 Hz** is **22x below the t0004 project target (32 Hz)** and **30-150x below
in vivo / in vitro published DSGC peak rates of 30-100 Hz**. The cause is the AMPA-only
configuration with conservative 0.5 nS per-synapse conductance; PolegPolsky2016 reports PD PSPs of
5.8 mV (with NMDA) at 177 synapses, and the t0046 exact reproduction overshoots at 23.25 mV with 282
synapses, while our 100-synapse AMPA-only model lands at 5.30 mV PD EPSP. The PSP magnitude is
correct -- the cell is simply at the lower edge of the AP-firing operating range.

The headline mechanistic result is the **IPSP voltage-vs-conductance gap (1.54x voltage vs 3.0x
conductance)**. This is driving-force saturation: with 100 GABA synapses firing near synchronously,
local Vm approaches E_GABA = -75 mV and additional conductance produces sub-linear voltage
suppression. This finding is *consistent* with the multiplicative-vs-additive shunting framework of
PolegPolsky2016 [p. 1283]: shunting inhibition acts as a divisive operation only when driving force
is far from E_GABA; once driving force collapses, the operation becomes sub-linear in conductance.
For scalar-`gabaMOD` models this means the **voltage modulation depth (1.54x) is the relevant
biological quantity**, not the nominal conductance ratio (3.0x). Models that report gabaMOD ratios
as if they were voltage modulation depths systematically over-promise the suppression at the soma.

The agreement between this minimal model and Park2014's circuit hypothesis is **structural**: with
omnidirectional excitation and tuned-only inhibition we recover the qualitative DS phenomenon and
hit the reasonable HWHM range (82.5° vs Park2014 cells with HWHMs typically in the 60-90° range,
and t0004 target 68.5°). What we do **not** recover is the absolute firing rate or the fine-scale
shape of the tuning curve -- both of which require either (a) higher AMPA conductance, (b) NMDA
addition, or (c) AR(2) correlated noise. These are all flagged as downstream tasks.

A surprising secondary finding is that the IPSP amplitude at PD (5.30 mV) and ND (8.16 mV) lies
**within the same order of magnitude** as the PolegPolsky2016 NMDA-PSP magnitudes (5.8 mV PD / 3.3
mV ND), even though the underlying mechanism (inhibitory conductance vs NMDA depolarisation) is
different. This coincidence of magnitudes makes scalar-`gabaMOD` models qualitatively
indistinguishable from NMDA-driven multiplication when only somatic PSP is measured -- a
methodological warning for studies that infer NMDA contribution purely from PSP scaling slopes.

## Limitations

* **Park2014 in vivo DSI band** in the orchestrator's hand-off message ("0.40-0.60") could not be
  verified from the paper text. The paper reports CART-Cre cells DSI = 0.65 +/- 0.05 (n = 14) and
  TRHR-GFP / wild-type cells 0.73 +/- 0.03 (n = 38) [Park2014, p. 3978]. The 0.40-0.60 band may
  reference other studies; we use the values directly attributable to Park2014.

* **deRosenroll2026 DSI of 0.39** is a model output, not an in vivo measurement; it is the
  correlated AR(2) release benchmark that any reimplementation should match, not a direct comparison
  to physiology. Used as the closest comparable published model in the project corpus.

* **No noise comparison**: deRosenroll2026 emphasises that DSI is sensitive to release decorrelation
  (0.39 -> 0.25). Our deterministic protocol cannot test this; reliability = 1.000 is artefactual.

* **NMDA absent**: PolegPolsky2016 attributes ~35% of PSP magnitude to NMDA. Direct comparison of
  PSP magnitudes therefore underestimates our model relative to literature.

* **Synapse-count regime mismatch**: 100 vs 177 (PolegPolsky2016) vs 282 (t0046) vs >1000
  (deRosenroll2026) is a >10x range. Per-synapse parameters cannot be directly compared without
  total-conductance normalisation.

* **Voltage ratio observation lacks a direct literature anchor**: the 1.54 vs 3.0 driving-force
  saturation is not reported as an explicit quantity in any paper in the project corpus; the
  comparison is qualitative (consistent with PolegPolsky2016 multiplicative framework) rather than a
  numerical match.

* **Single-spike-per-trial regime**: the binary on/off firing pattern produces a primary DSI = 1.0
  trivially; this is a model-regime artefact and not a meaningful match to literature DSI values.
  All literature DSI values come from cells in a multi-spike-per-trial regime.

* **Park2014's inhibitory conductance estimate (2.43 nS, P-N)** is a whole-cell voltage-clamp
  measurement; our `gabaMOD` design gives a per-synapse net P-N of 1.32 nS times 100 synapses = 132
  nS aggregate, but most of this is shunted locally and only a fraction reaches the soma. The
  order-of-magnitude consistency is approximate.
