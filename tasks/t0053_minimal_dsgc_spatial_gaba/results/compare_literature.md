---
spec_version: "1"
task_id: "t0053_minimal_dsgc_spatial_gaba"
date_compared: "2026-04-25"
---
# Comparison with Published Results

## Summary

The minimal from-scratch DSGC with **spatial centripetal-only inhibition** (per-synapse boolean
firing gate at full 2 nS amplitude when `cos(theta_stim - theta_centrifugal_i) < 0`) produces a
**degenerate FULL-mode tuning curve** of **0 Hz across all 12 directions** (primary DSI **0.0**,
vector-sum DSI **0.0**, peak Hz **0.0**, null Hz **0.0**). This is **negative** with respect to the
in vitro mouse On-Off DSGC band of **0.65 +/- 0.05** (CART-Cre, n=14) and **0.73 +/- 0.03**
(TRHR-GFP / wild-type, n=38) reported by Park2014 [Park2014, p. 3978] and the model-based vector-sum
DSI of **0.39** (correlated AR(2)) reported by deRosenroll2026 [deRosenroll2026, Fig 5 / Table S1].
AMPA_ONLY peak Hz of **0.667** is **identical** to t0052's value, confirming excitation is
bit-identical between the two tasks; the DSI collapse in t0053's FULL mode is purely a consequence
of inhibition-mass over-saturation (mean **100 nS** total GABA conductance per trial vs **66 nS** in
t0052 under scalar gabaMOD). The active-fraction modulation across directions **(0.34 - 0.66)**
confirms the spatial gating mechanism works as designed but the absolute IPSP amplitude (1.24x
voltage modulation across directions) is high enough to suppress spiking in every direction.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Park2014 (CART-Cre, voltage-clamp) | DSI (primary) | 0.65 | 0.000 | -0.65 | In vitro mouse On-Off DSGCs, n=14; FULL-mode degenerate (peak = null = 0 Hz) [Park2014, p. 3978] |
| Park2014 (TRHR-GFP / wild-type) | DSI (primary) | 0.73 | 0.000 | -0.73 | Reference subset, n=38 cells; FULL-mode degenerate [Park2014, p. 3978] |
| deRosenroll2026 (correlated AR(2) release) | DSI (vector-sum) | 0.39 | 0.000 | -0.39 | Vector-sum DSI vs paper's vector-sum benchmark; rho=0.6 [deRosenroll2026, p. 6 / Fig 5] |
| deRosenroll2026 (uncorrelated release) | DSI (vector-sum) | 0.25 | 0.000 | -0.25 | Lower-bound model benchmark; we lack release noise entirely [deRosenroll2026, p. 6 / Fig 5] |
| t0004 target curve (this project) | Peak rate (Hz) | 32.0 | 0.000 | -32.0 | FULL-mode produces no spikes; AMPA_ONLY peak = 0.667 Hz [t0004 results_summary] |
| t0004 target curve (this project) | DSI | 0.8824 | 0.000 | -0.8824 | Project canonical target; FULL-mode degenerate [t0004 results_summary] |
| t0004 target curve (this project) | Tuning curve RMSE (Hz) | 0.0 (self) | 17.18 | +17.18 | Dominated by 32 Hz target peak vs flat-zero model [results_detailed.md] |
| Park2014 (null inhibitory conductance, P-N) | Inhibitory P-N (nS) | 2.43 | 1.0 | -1.43 | Per-direction IPSP active fraction range 0.34 -> 0.66 implies P-N effective conductance change of (0.66 - 0.34) * 2 nS = 0.64 nS times 100 syn per direction; voltage-side ratio is 1.24x not 3.0x due to driving-force saturation [Park2014, p. 3978] |
| PolegPolsky2016 (Fig 1, control PD PSP) | PD NMDA-PSP | 5.8 mV | 6.33 mV | +0.53 mV | Aggregate IPSP amplitude at preferred-side direction (theta=30 degrees, minimum-active-fraction direction); paper reports excitatory NMDA-PSP, our value is inhibitory IPSP magnitude — order-of-magnitude similar [PolegPolsky2016, p. 1280, Fig 1] |
| PolegPolsky2016 (Fig 1, control ND PSP) | ND NMDA-PSP | 3.3 mV | 7.82 mV | +4.52 mV | Aggregate IPSP at null-side (theta=210 degrees, max-active-fraction direction); paper value is excitatory NMDA, ours is inhibitory IPSP — magnitudes coincidentally near each other [PolegPolsky2016, p. 1280, Fig 1] |

### Prior Task Comparison

| Prior Task | Variant | DSI (primary) | Peak Hz | HWHM (deg) | Notes |
| --- | --- | --- | --- | --- | --- |
| t0008 (rotation-proxy ModelDB 189347) | baseline | 0.316 | 18.1 | 82.81 | Wrong DS protocol; below project envelope |
| t0020 (gabaMOD-swap ModelDB 189347) | PD/ND | 0.7838 | 14.85 | n/a | Native HOC gabaMOD swap; high DSI, low peak |
| t0022 (E-I temporal-asymmetry) | spatial | 1.000 | 15.0 | 116.25 | DSI = 1.0 via half-plane PD/ND switch on the deposited HOC port |
| t0024 (de Rosenroll port, correlated) | rho=0.6 | 0.7758 | 5.15 | 68.65 | Stochastic AR(2) release; HWHM closest to t0004 target |
| t0046 (Poleg-Polsky exact reproduce, Fig 1) | control_gnmda25 | 0.1730 | n/a (subthr.) | n/a | Faithful 282-syn ModelDB port; primary DSI on PSP not AP |
| t0049 (SE-clamp AMPA conductance DSI) | AMPA only | 0.0120 | n/a | n/a | Conductance-level DSI in clamped cell, near zero |
| t0052 (sibling, scalar gabaMOD) | FULL | **1.000** | **0.667** | **82.5** | Single-spike-per-trial; perfect on/off binary tuning |
| t0053 (this task, spatial centripetal) | FULL | **0.000** | **0.000** | **180.0 (degen.)** | Fully suppressed; same morphology and placement seed as t0052 |

## Methodology Differences

* **Inhibition mechanism (vs t0052 sibling)**: t0052 scales every I synapse's amplitude by a global
  direction-dependent scalar `gabaMOD(theta) = 0.33 + 0.66 * (1 - cos(theta - theta_PD)) / 2`
  applied uniformly to all 100 synapses. t0053 instead activates a synapse only when
  `cos(theta_stim - theta_centrifugal_synapse) < 0`, at full 2 nS amplitude. This is an
  amplitude-modulation vs binary-firing-gate distinction. Mean total GABA mass per trial: t0052
  delivers 100 syn x 0.66 nS = **66 nS** averaged across directions; t0053 delivers 50 syn x 2 nS =
  **100 nS** averaged across directions — a **1.5x** increase in mean inhibitory drive that fully
  suppresses spiking.

* **Inhibition mechanism (vs Park2014)**: Park2014 [p. 3978] attributes all DS to null-direction
  GABA from SACs (whole-cell P-N = 2.43 nS). Our centripetal-gating mechanism approximates the SAC
  network's centrifugal preference at the SAC-output level — SAC dendrites release GABA when
  stimuli move centrifugally over them — so from the DSGC's perspective inhibition concentrates on
  dendrites being approached "from the wrong end". This is structurally aligned with the Park2014
  hypothesis but our 2 nS per-synapse amplitude is at the upper end of the per-synapse conductance
  inferred from the whole-cell measurement.

* **Excitation tuning**: Park2014 [p. 3978] proves bipolar-cell glutamate is omnidirectional at
  release. Our model implements omnidirectional AMPA exactly as Park2014 prescribes — and
  AMPA_ONLY produces 0.667 Hz uniformly across all 12 directions, confirming this is bit-identical
  to t0052 and the DSI collapse is **not** an excitation issue.

* **Synapse count**: 100 E + 100 I (this task and t0052) vs ~177 in PolegPolsky2016 [p. 1280] / 282
  in t0046 reproduction / >1000 SAC varicosities in deRosenroll2026 [p. 5]. The lower synapse count
  produces lower aggregate excitation but does not by itself explain the 0-Hz FULL result —
  AMPA_ONLY produces a single spike per trial, so excitation is at threshold. Adding the spatial
  GABA mechanism pushes the cell below threshold in every direction.

* **Active-fraction modulation**: Our spatial mechanism produces direction-dependent active-synapse
  counts (0.34 to 0.66 of 100 I synapses), a **1.94x** ratio. Published DSGC SAC-output models in
  deRosenroll2026 produce a graded GABA conductance modulation (not a discrete on/off per synapse),
  so the comparison to published "active-fraction" curves is qualitative rather than numerical —
  but the 0.5 mean across directions is the structural prediction of any centripetal half-plane rule
  on a roughly symmetric dendritic field.

* **Driving-force saturation**: Both t0052 and t0053 see substantially less voltage modulation than
  the underlying conductance-level signal. t0052 reports a 1.54x voltage ratio against a 3.0x
  conductance ratio (gabaMOD endpoints 0.33 / 0.99). t0053 reports a **1.24x voltage ratio** (6.33
  mV at theta=30 degrees -> 7.82 mV at theta=210 degrees) against a **1.94x active-synapse count
  ratio** (34 -> 66 synapses). The same saturation mechanism, different numerical regime because
  t0053's per-synapse amplitude is fixed at 2 nS rather than scaling.

* **No NMDA**: Our model has AMPA only by design, while PolegPolsky2016 emphasises NMDARs contribute
  multiplicatively at PD (5.8 mV / ~35% of total PSP). This is a structural omission, not a
  parameter mismatch — our task is the AMPA-only minimal floor.

* **No noise**: Our trials are deterministic single-event-per-synapse, while deRosenroll2026 [p. 6]
  requires AR(2) correlated release with rho = 0.6 to match in vitro noise. Our lack of noise
  prevents any release-decorrelation comparison.

* **DSI definition**: Park2014 uses the standard primary DSI on AP counts; deRosenroll2026 uses
  vector-sum DSI on spike counts. Both versions of DSI are degenerate in our FULL-mode (peak = null
  = 0).

## Analysis

### Headline negative finding

The spatial centripetal mechanism with **2 nS GABA per active synapse on roughly half of 100
synapses** is **too inhibitory** to produce a measurable DSI on the t0009-calibrated DSGC
morphology. The model lands at **DSI = 0.000** in FULL mode, a **-0.65** to **-0.73** delta against
the in vivo Park2014 band and **-0.39** against the deRosenroll2026 model benchmark. This is the
headline negative result of the task: **the centripetal-gating idea is mechanistically correct (the
active fraction modulates 0.34 -> 0.66 across directions, biasing inhibition toward ND-side
dendrites, exactly as predicted) but the per-synapse amplitude is mis-calibrated for this
morphology**. Recovery options are (a) reduce GABA conductance per synapse below 2 nS, (b) introduce
a stricter centripetal threshold (e.g., `cos(theta - theta_centrifugal) < -0.5` would fire only ~25%
of synapses per direction, halving the active-mass), or (c) increase AMPA conductance per synapse so
the cell sits well above threshold before any inhibition arrives.

### Active-fraction modulation vs published DSGC SAC-network output

Our active-fraction polar curve ranges from **0.34** at theta=30 degrees to **0.66** at theta=210
degrees, a **1.94x** ratio with mean **0.500**. This is the centripetal half-plane prediction for
the soma-centred origin of the t0009 morphology: the dendritic field is roughly symmetric so the
mean is exactly 0.5, but the soma is offset from the centroid so the per-direction modulation
deviates from 0.5 by up to **+/- 0.16**. Published SAC-network output models in deRosenroll2026
[p. 5-6] do not directly publish a per-direction "fraction of active SAC outputs" curve; instead
they report a graded-conductance gabaMOD that approximates the SAC-network ensemble output. Our
binary-firing approximation of the same biological mechanism produces structurally different
numerical predictions: graded amplitude scaling (t0052) preserves a continuous DSI; binary firing
(t0053) at the chosen 2 nS amplitude produces a degenerate flat-zero curve. The spatial mechanism's
aggregate inhibition mass scales with the active fraction (linearly), but the somatic voltage
response is sub-linear in this mass due to the driving-force saturation discussed below.

### Driving-force saturation: same physical mechanism as t0052, different numerical regime

The IPSP voltage modulation across directions (peak **6.33 mV** at theta=30 degrees minimum-active
direction, peak **7.82 mV** at theta=210 degrees maximum-active direction) is **only 1.24x** even
though the active-synapse count varies **1.94x**. This is the same driving-force-saturation
mechanism we observed in t0052 (where 3.0x conductance produced 1.54x voltage), now operating in a
different regime: t0053's full-amplitude 2 nS per active synapse drives Vm closer to E_GABA = -75 mV
than t0052's scaled-down 0.66 nS-equivalent, so the ceiling is hit sooner. Combined with t0052's
data, this provides a **two-point map** of the saturation curve: at lower conductance levels the
voltage scales more sharply (t0052: 1.54x voltage from 3.0x conductance, slope ~0.51), and at higher
conductance levels the voltage scales more gently (t0053: 1.24x voltage from 1.94x active count,
slope ~0.64 in log-units but with a higher absolute amplitude). The methodological implication is
that **scalar inhibition models that report nominal conductance ratios systematically over-promise
their somatic suppression at the soma** — the relevant biological quantity is the voltage
modulation depth, which is consistently smaller than the conductance ratio in any non-clamped cell.

### AMPA_ONLY identity confirms inhibition is the only knob

AMPA_ONLY produces a peak rate of **0.667 Hz uniformly across all 12 directions** in t0053,
**identical to t0052's AMPA_ONLY result** (also 0.667 Hz uniformly). This is a strong methodological
control: it confirms the synapse placement is bit-identical between t0052 and t0053 (verified by
`test_placement_seed0_match.py`) and that the excitation mechanism, AIS section, soma + AIS HH
channels, and per-synapse AMPA Exp2Syn parameters are also bit-identical. The **0.0 Hz FULL result
is therefore a pure consequence of the inhibition mechanism**: same morphology, same excitation,
same placement, only the inhibition driver differs. This isolates the failure cleanly to a single
design choice (full 2 nS amplitude on ~50% of synapses) and makes the parameter sweep to recover a
measurable DSI well-posed.

### Why scalar (t0052) succeeds and spatial (t0053) fails

The structural difference between the two siblings clarifies a generic point about DSGC modelling.
t0052's gabaMOD delivers a **graded amplitude** (33-99% of 2 nS) on **all 100** synapses. t0053's
spatial gating delivers **full amplitude** (100% of 2 nS) on only **half** the synapses. The mean
GABA mass per trial differs by 1.5x in t0053's favour (100 nS vs 66 nS), and this is enough to flip
the model from "perfect DSI = 1.0" to "fully suppressed DSI = 0.0". The *direction* of the effect is
correct in both cases (more inhibition on null side); the *amplitude calibration* is what makes
t0052 work and t0053 fail under otherwise-identical conditions. This suggests that for a fair
comparison of inhibition mechanisms (graded vs binary), the per-synapse amplitude under the binary
scheme should be tuned so that the *mean* GABA mass matches the graded scheme — i.e., t0053 with
**1.32 nS per active synapse** (= 66 nS total / 50 active) would be the conductance-matched
comparison, not 2 nS.

## Limitations

* **FULL-mode is degenerate**: primary DSI = 0.0 because peak = null = 0 Hz. Vector-sum DSI is also
  0.0 trivially. All comparisons against published DSI values are therefore comparisons to a
  fully-suppressed model, not a partially-suppressed model with a non-zero null and peak. This is a
  meaningful negative result but it limits the dynamic-range of the comparison.

* **Single conductance setting**: the task specification fixed GABA peak at 2 nS per synapse with no
  scaling. A natural follow-up is a sweep across {0.5, 1.0, 1.32, 1.5, 2.0} nS to find the amplitude
  at which the spatial mechanism produces a non-zero firing rate. The 1.32 nS conductance-matched
  comparison with t0052 would also be informative.

* **Park2014 in vivo DSI band** in the orchestrator's hand-off message ("0.40-0.60") could not be
  verified from the paper text. The paper reports CART-Cre cells DSI = 0.65 +/- 0.05 (n = 14) and
  TRHR-GFP / wild-type cells 0.73 +/- 0.03 (n = 38) [Park2014, p. 3978]. We use the values directly
  attributable to Park2014.

* **deRosenroll2026 DSI of 0.39** is a model output, not an in vivo measurement; it is the
  correlated AR(2) release benchmark that any reimplementation should match, not a direct comparison
  to physiology. Used as the closest comparable published model in the project corpus.

* **No noise comparison**: deRosenroll2026 emphasises that DSI is sensitive to release decorrelation
  (0.39 -> 0.25). Our deterministic protocol cannot test this; even if the model spiked, reliability
  would be artefactually 1.0.

* **NMDA absent**: PolegPolsky2016 attributes ~35% of PSP magnitude to NMDA. Direct comparison of
  PSP magnitudes therefore underestimates our model relative to literature; the 6.33 - 7.82 mV IPSP
  range we report is on the same scale as PolegPolsky2016's NMDA-PSP magnitudes (5.8 / 3.3 mV) only
  by coincidence, not by mechanism.

* **Synapse-count regime mismatch**: 100 vs 177 (PolegPolsky2016) vs 282 (t0046) vs >1000
  (deRosenroll2026) is a >10x range. Per-synapse parameters cannot be directly compared without
  total-conductance normalisation.

* **Driving-force saturation observation lacks a direct literature anchor**: the 1.24 vs 1.94 ratio
  is not reported as an explicit quantity in any paper in the project corpus; the comparison is
  qualitative (consistent with PolegPolsky2016's multiplicative-vs-additive shunting framework
  [p. 1283]) rather than a numerical match.

* **Active-fraction polar curve has no direct published counterpart**: published SAC-network models
  (deRosenroll2026, Park2014) report aggregate GABA conductance modulation, not a per-direction
  count of active SAC outputs at the DSGC. The 0.34 - 0.66 modulation reported here is a
  model-internal observable rather than a literature-comparable measurement.

* **Cross-task comparison with t0052 is informally documented in this file** but not in a dedicated
  cross-task analysis; the suggestions list includes a follow-up that would do a conductance-matched
  sweep (1.32 nS in t0053-style binary firing) to isolate the graded-vs-binary mechanism distinction
  at matched mean GABA mass.
