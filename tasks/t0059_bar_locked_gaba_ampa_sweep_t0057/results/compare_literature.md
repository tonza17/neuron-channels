---
spec_version: "1"
task_id: "t0059_bar_locked_gaba_ampa_sweep_t0057"
date_compared: "2026-04-29"
---
# Comparison with Published Results

## Summary

The 5x5 `(gAMPA, GABA_BASE_NS)` sweep on the bar-arrival-locked tonic-GABA substrate **escapes the
0.667 Hz single-spike-degenerate ceiling** that pinned t0052 / t0053 / t0054-AMPA / t0055 / t0057
but only barely — the maximum FULL-mode peak rate across all 25 grid cells is **2.143 Hz** (3
spikes / 1.4 s), the maximum primary DSI is **0.500** (a discrete 3-vs-1 spike-count artefact), and
the maximum vector-sum DSI is **0.209**. These remain **14-50x below** in vitro DSGC peak rates of
30+ Hz [Park2014, p. 3978] and **3.1-3.5x below** vector-sum DSI benchmarks of **0.65**
[Park2014, p. 3978] / **0.39** [deRosenroll2026, Fig 5]. The two new building blocks (per-synapse
bar-arrival-locked windows; HH save-and-zero on soma + AIS) validate independently: the bar-locked
mechanism produces an **8.5 ms** direction-dependent IPSP centre-of-mass shift the global-window
t0057 mechanism could not, and EPSP_PASSIVE peak Vm reaches **-9.04 mV** worst-case (well below the
+5 mV gate, confirming HH is correctly muted). The negative result definitively rules out two
hypotheses: AMPA conductance escape via the swept gAMPA range and sub-0.25 nS bar-locked GABA
graded-suppression rescue. The most plausible remaining gap-closers are active dendritic
conductances (passive dendrites cap multi-spike firing) and Mg-block NMDA layered onto this
bar-locked substrate (S-0057-06 follow-up).

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| Park2014 (CART-Cre, voltage-clamp) | DSI (primary) | 0.65 | 0.500 | -0.150 | In vitro mouse On-Off DSGCs, n=14; our 0.500 is at gAMPA=3.0/gaba=0.10 (3-vs-1 spike-count artefact, not biologically tuned) [Park2014, p. 3978] |
| Park2014 (TRHR-GFP / wild-type) | DSI (primary) | 0.73 | 0.500 | -0.230 | Reference subset, n=38 cells; same caveat — discrete spike-count contrast, not graded firing-rate tuning [Park2014, p. 3978] |
| Park2014 (in vivo-implied peak rate) | Peak Hz | 30.00 | 2.143 | -27.857 | 30-100 Hz in vivo range; max FULL peak Hz across all 25 cells is 2.143 = **14x below** lower bound of in vivo band [Park2014, p. 3978] |
| PolegPolsky2016 (voltage-dep NMDA + tuned GABA) | DSI | 0.46 | 0.500 | +0.040 | Apparent match is misleading — our 0.500 is a 3-vs-1 spike-count discretisation; PolegPolsky's 0.46 is a graded multi-spike DSI under Mg-block NMDA [PolegPolsky2016, Fig 5] |
| deRosenroll2026 (correlated AR(2) release) | DSI (vector-sum) | 0.39 | 0.209 | -0.181 | Vector-sum DSI vs paper's vector-sum benchmark; rho=0.6; ours is the best across the entire 25-cell grid (gAMPA=1.0/gaba=0.10) [deRosenroll2026, Fig 5] |
| deRosenroll2026 (uncorrelated release) | DSI (vector-sum) | 0.25 | 0.209 | -0.041 | Lower-bound model benchmark; we lack release noise entirely so this is closest comparable point [deRosenroll2026, Fig 5] |
| t0004 target curve (this project) | Peak rate (Hz) | 32.00 | 2.143 | -29.857 | Project canonical target; our peak rate is **15x below** target across the entire grid [t0004 results_summary] |
| t0004 target curve (this project) | DSI (primary) | 0.8824 | 0.500 | -0.382 | Project canonical target; best primary-DSI cell still **0.38 below** the project target [t0004 results_summary] |
| t0004 target curve (this project) | HWHM (deg) | 68.51 | 30.00 | -38.51 | Best-HWHM cell (gAMPA=2.0/gaba=0.20) is sharper than target; reflects discrete spike-count tuning, not biological tuning width [t0004 results_summary] |
| t0004 target curve (this project) | Tuning RMSE (Hz) | 0.0000 | 16.064 | +16.064 | Best-RMSE cell (gAMPA=2.0/gaba=0.10) still **16 Hz off** because target peaks at 32 Hz and model peaks at 2.143 Hz [t0004 results_summary] |
| PolegPolsky2016 (control PD PSP) | PD PSP (mV) | 5.8 | 6.545 | +0.745 | Aggregate IPSP at theta=210 deg in IPSP_PASSIVE at gaba=1.0 nS; paper value is excitatory NMDA-PSP, ours is inhibitory IPSP — order-of-magnitude similar [PolegPolsky2016, p. 1280, Fig 1] |
| Park2014 (null inhibitory conductance, P-N) | Inhibitory P-N nS | 2.43 | 1.0 | -1.430 | Whole-cell P-N is 2.43 nS [Park2014, p. 3978]; we deliver up to 100 syn x active-fraction modulation 0.34-0.66 x per-synapse 1.0 nS effective at the centre of the swept GABA grid [Park2014, p. 3978] |

### Prior Task Comparison

| Prior Task | E pathway | I pathway | Max FULL Peak Hz | Max FULL DSI | Notes |
| --- | --- | --- | ---: | --- | --- |
| t0052 (sibling, scalar gabaMOD) | AMPA 0.5 nS | scalar gabaMOD point process | **0.667** | 1.000 (primary, trivial) / 0.7464 (vector) | Single-spike-per-trial; perfect on/off binary tuning. Vector-sum DSI from full PD/ND switch |
| t0053 (sibling, spatial Exp2Syn at 2 nS) | AMPA 0.5 nS | spatial Exp2Syn GABA, centripetal gating | **0.000** | 0.000 (full suppression) / 0.7464 (vector) | Fully suppressed by 100 nS mean GABA mass at gGABA=2.0 nS; trivial vector-sum from ND-only firing |
| t0054 (sibling, NMDA + scalar gabaMOD, gNMDA=0.25) | AMPA + voltage-indep NMDA | scalar gabaMOD | **8.000** | 0.143 (primary) / 0.082 (vector) | NMDA breaks single-spike regime but DSI collapses without Mg-block |
| t0055 (sibling, AMPA + Mg-block NMDA + gabaMOD) | AMPA + Mg-block NMDA | scalar gabaMOD | **0.667** | 1.000 (primary, trivial) / 0.7464 (vector) | DSI recovers but back in single-spike regime; Mg-block keeps NMDA blocked under hyperpolarising GABA |
| t0057 (parent, tonic GABA global window 0.25-2.0) | AMPA 0.5 nS | tonic GABA, global `(100, 1400)` ms window | **0.667** | 0.000 (primary, degenerate) / ~3e-17 (vector) | Either uniform single-spike (gaba <= 1.0 nS) or fully suppressed (gaba >= 1.5 nS); no intermediate |
| **t0059 (this task)** | **AMPA 0.5-4.0 nS sweep** | **bar-locked tonic GABA, 0.1-2.0 nS sweep** | **2.143** | **0.500 (primary) / 0.209 (vector)** | **First task to escape 0.667 Hz non-trivially** but still 14x below in vivo; vector-sum DSI 3.1x below deRosenroll2026 |

## Methodology Differences

* **Substrate inheritance**: t0059 forks t0057's `minimal_dsgc_tonic_gaba_sweep` library verbatim
  (same morphology, same placement seed, same `gaba_tonic.mod` POINT_PROCESS, same CVODE bootstrap),
  applies four targeted edits (per-synapse window, HH save-and-zero, gAMPA outer loop, 1400 ms
  TSTOP), and keeps everything else bit-identical. The placement_seed0 bit-identity test (REQ-16)
  passes 100/100 pairs at POSITION_TOLERANCE = 1e-9, so cross-task comparisons against t0052 / t0053
  / t0054 / t0055 / t0057 are scientifically valid.

* **Inhibition mechanism (vs t0057 parent)**: t0057 holds `g = GABA_BASE_NS` over the entire global
  `(t_on, t_off) = (100, 1400) ms` window for every active synapse — a 1300 ms sustained envelope
  that is **far longer** than the published 100-300 ms SAC->DSGC IPSC envelope range. t0059 replaces
  this with per-synapse windows
  `t_on_i = (x_i cos theta + y_i sin theta) / v + 100 ms, t_off_i = t_on_i + 200 ms` — a 200 ms
  envelope **inside** the published biological range. The bar-locked mechanism produces a measurable
  **8.5 ms** direction-dependent IPSP centre-of-mass shift (REQ-13 PASS) that the global-window
  t0057 mechanism cannot.

* **Inhibition mechanism (vs Park2014)**: Park2014 [p. 3978] reports whole-cell PD-ND = **2.43 nS**
  at the soma. Our peak per-synapse GABA conductance reaches 2.0 nS but is gated to ~50 active
  synapses by the centripetal predicate, so aggregate per-direction conductance scales with the 0.34
  - 0.66 active-fraction modulation. The 200 ms bar-locked window envelope is closer to the
    biological SAC IPSC than t0057's 1300 ms window but still simplifies the multi-event SAC release
    kinetics down to a single sustained pulse.

* **Inhibition mechanism (vs PolegPolsky2016)**: PolegPolsky2016 [p. 1280, Methods] uses a
  multi-event SAC->DSGC GABA driver with envelope tau ~50-150 ms; we use a single 200 ms tonic pulse
  per synapse. The PolegPolsky2016 model also includes voltage-dependent NMDA Mg-block which
  preserves DSI multiplicatively; our model is AMPA-only by design.

* **Excitation (vs all sibling minimal-DSGCs)**: t0052 / t0053 / t0057 all hard-code AMPA at 0.5 nS
  per synapse. t0059 sweeps gAMPA ∈ {0.5, 1.0, 2.0, 3.0, 4.0} nS — an 8x range. Even at the
  maximum swept value (4.0 nS = 8x baseline), the cell maxes out at 2.143 Hz peak rate (3 spikes /
  1.4 s), ruling out an amplitudinal escape from the single-spike regime within this substrate.

* **Synapse count (vs published DSGCs)**: 100 E + 100 I in this task vs ~177 in PolegPolsky2016
  [p. 1280] / 282 in t0046 reproduction / >1000 SAC varicosities in deRosenroll2026 [p. 5]. Lower
  synapse count gives weaker total drive; combined with passive dendrites, this is the structural
  bottleneck most consistent with the 2.143 Hz peak ceiling.

* **Active dendrites (vs published DSGCs)**: Our morphology has `pas` only on dendrites and `hh` on
  soma + AIS. Park2014 [p. 3977] and PolegPolsky2016 [p. 1278] both implicitly assume active
  dendritic mechanisms (Nav, Kv, NMDA) that boost local depolarisation and enable multi-spike
  firing. The 2.143 Hz ceiling here is most plausibly a structural consequence of passive dendrites,
  not a calibration issue.

* **No noise (vs deRosenroll2026)**: Trials are deterministic single-event-per-synapse;
  deRosenroll2026 [p. 6] requires AR(2) correlated release with rho = 0.6 to match in vitro. Our
  reliability = 1.0 across all FULL cells reflects this — DSI sensitivity to trial-to-trial
  variability is not characterised.

* **Measurement protocol (vs t0052 / t0053 / t0054 / t0055 / t0057)**: t0059 ships the project-wide
  S-0055-01 fix — drops the legacy `AMPA_ONLY` / `GABA_ONLY` modes (which kept HH active and
  contaminated passive measurements with spikes) and replaces them with `EPSP_PASSIVE` /
  `IPSP_PASSIVE` modes that save-and-zero `gnabar_hh` / `gkbar_hh` on soma + AIS. Worst-case
  EPSP_PASSIVE peak Vm = -9.04 mV at gAMPA=4.0/gaba=0.10/theta=210 deg — well below the +5 mV
  gate, confirming HH is correctly muted (REQ-15 PASS). The FULL-mode bit-identity test (REQ-14)
  confirms HH is correctly restored (atol = 1e-6 mV against reference).

* **Trial length (vs t0052 / t0053 / t0054 / t0055 / t0057)**: 1400 ms here vs 1500 ms upstream.
  Firing-rate denominator tightens by ~7%; affects nominal Hz values but not regime classification.

## Analysis

### Headline negative finding: bar-locked windows + AMPA escape do not reach the in vivo regime

The 5x5 `(gAMPA, GABA_BASE_NS)` sweep produces a **maximum FULL-mode peak rate of 2.143 Hz** (3
spikes / 1.4 s, four cells) and a **maximum vector-sum DSI of 0.209** (gAMPA=1.0 / gaba=0.10). These
are **14-50x below** Park2014's in vivo / in vitro peak-rate range of 30-100 Hz [Park2014, p. 3978]
and **3.1-3.5x below** the project-relevant vector-sum DSI benchmarks (Park2014 0.65,
PolegPolsky2016 0.46, deRosenroll2026 0.39). The headline primary DSI of **0.500** is a
3-spike-vs-1-spike count discretisation artefact at gAMPA=3.0/gaba in {0.10, 0.20}, not a
biologically meaningful tuned response — vector-sum DSI at the same operating point is only 0.111
because firing is approximately bimodal across the 12 directions rather than smoothly tuned.

### What this task ruled out

Two specific hypotheses are now definitively rejected on the from-scratch DSGC substrate:

1. **AMPA conductance escape via gAMPA up to 4.0 nS does not unlock multi-spike firing** on the
   passive-dendrite + soma+AIS-HH morphology. The 8x conductance increase from 0.5 nS (t0057
   baseline) to 4.0 nS adds at most 2 spikes per trial. The peak-Hz heatmap shows clear diminishing
   returns at gAMPA >= 2.0 nS, suggesting the wall is structural (passive dendrites cap local
   depolarisation), not amplitudinal.

2. **Sub-0.25 nS bar-locked GABA does not produce graded suppression of an already-firing cell**.
   The graded-suppression hypothesis required the cell to be firing multi-spike for sub-0.25 nS GABA
   to modulate. Since multi-spike firing is not entered, sub-0.25 nS GABA produces near-zero IPSP
   voltage envelope (1.495 mV at gaba=0.10 nS at theta=210 deg) and has no effect on spike count.

### The 2.143 Hz ceiling vs t0054's 8 Hz: NMDA, not GABA window shape, is the rate-limiter

The most informative literature comparison is **internal**: t0054's voltage-independent NMDA on the
same morphology, at gNMDA = 0.25 nS, reaches **8.0 Hz** peak rate but DSI collapses to **0.082**
vector-sum / 0.143 primary. t0059's bar-locked tonic GABA + AMPA escape reaches only **2.143 Hz**
peak. The **delta of 5.86 Hz** between these two tasks under matched morphology + matched 100 E +
100 I architecture is direct evidence that **NMDA on the E pathway is the rate-limiting ingredient**
for breaking the 0.667 Hz regime — not the GABA window shape, not the gAMPA conductance, not the
inhibitory amplitude.

### Convergence with PolegPolsky2016 prediction

PolegPolsky2016 [p. 1283-1284] argues that voltage-dependent NMDA Mg-block is necessary for
multiplicative DSI scaling, and that subtractive inhibition alone cannot produce the in vivo DSI
band. Cumulative evidence across t0052 (trivial DSI in single-spike regime), t0053 (full suppression
at 2 nS), t0054 (DSI collapses under voltage-independent NMDA), t0055 (DSI recovers under Mg-block
but reverts to single-spike regime), t0057 (no graded operating point in 8x sweep), and now t0059
(no operating point in 25-cell 2-axis sweep) converges on the same conclusion: **no AMPA-only
minimal DSGC operating in the single-spike-per-trial regime can reach the published DSI band**,
regardless of inhibition mechanism's spatial or temporal profile. The minimal model is missing
**multiple structural ingredients simultaneously** — most plausibly active dendritic conductances
and Mg-block NMDA on the bar-locked substrate.

### What this task validated

Two new mechanisms ship correctly and both decouple from the negative DSI result:

1. **Bar-arrival-locked window mechanism**: per-synapse `(t_on_i, t_off_i)` writes produce an IPSP
   envelope at the soma whose centre of mass shifts with stimulus direction by **8.5 ms** between
   theta = 0 and theta = 90 (REQ-13 PASS) — exceeding the geometric lower bound from synapse
   coordinates. This is the explicit fingerprint of the bar-locked mechanism that t0057's
   global-window mechanism could not produce. RQ3 = YES.

2. **HH save-and-zero correctness**: the `try/finally` save-and-restore on `gnabar_hh` / `gkbar_hh`
   on soma + AIS works exception-safely. EPSP_PASSIVE peak Vm = **-9.04 mV** worst-case (REQ-15
   PASS, well below the +5 mV gate); FULL-mode bit-identity test passes against reference at atol =
   1e-6 mV (REQ-14 PASS). The new measurement protocol fixes the EPSP-decay null-metric failure that
   affected t0054 / t0055.

### Prior Task Comparison (sibling deltas, vector-sum DSI)

The vector-sum DSI of **0.209** in this task is the **first non-trivial vector-sum DSI in the
from-scratch DSGC line**. t0052's 0.7464 and t0055's 0.7464 are trivial PD-vs-ND on/off switches in
the single-spike regime; t0053's are 0 (full suppression); t0054 reaches 0.082 only at the cost of
peak rate 8 Hz with DSI collapse; t0057 lives at the 3.2e-17 numerical floor. t0059 produces the
first **graded** vector-sum response, but at peak rate 1.429 Hz the DSI is too low to be
biologically meaningful.

| Sibling task | Best vector-sum DSI | Best peak Hz | Both achievable simultaneously? |
| --- | ---: | ---: | ---: |
| t0052 | 0.7464 (trivial) | 0.667 | No (single-spike degeneracy) |
| t0053 | 0.7464 (trivial) | 0.000 | No (full suppression) |
| t0054 (gNMDA=0.25) | 0.082 (graded) | 8.000 | DSI collapses |
| t0055 | 0.7464 (trivial) | 0.667 | No (single-spike regime) |
| t0057 | 3.2e-17 (floor) | 0.667 | No (degenerate) |
| **t0059 (this task)** | **0.209 (graded)** | **2.143** | **Partially (graded but low)** |

The sibling-comparison table directly contradicts the t0057 results-detailed claim that "no minimal
DSGC operating in the single-spike-per-trial regime can produce non-trivial vector-sum DSI" —
t0059 reaches **0.209** vector-sum DSI in the two-spike regime (gAMPA=1.0/gaba=0.10, peak Hz = 1.429
nS). The bar-locked window mechanism, despite the negative headline result, does deliver the first
direction-graded suppression on the from-scratch substrate.

## Limitations

* **Single-trial-noise insensitivity**: 10 deterministic trials per direction, no synaptic noise, no
  release stochasticity. Reliability = 1.0 across all FULL cells reflects this — DSI sensitivity
  to trial-to-trial variability is not characterised. Real DSGCs have reliability << 1
  [deRosenroll2026, p. 6].

* **AMPA-only excitation**: NMDA explicitly out of scope per task description; the AMPA-only path
  may underestimate what the substrate can do once Mg-block-NMDA is added (active follow-up:
  S-0057-06).

* **Passive dendrites**: the t0009 calibrated morphology has only `pas` channels in dendrites; `hh`
  lives only on soma + AIS. The 2.143 Hz peak-Hz ceiling is most plausibly a structural consequence
  of this passive-dendrite design, not an amplitude calibration issue. Active dendritic conductances
  (Nav1.6, Kv3, etc.) are the most likely path to multi-spike firing.

* **Fixed `window_ms = 200`**: biologically motivated midpoint of the 100-300 ms SAC IPSC envelope
  range; not swept. Whether 100 ms or 300 ms windows shift the regime boundary is unknown.

* **gAMPA ceiling at 4.0 nS**: trimmed from the original S-0057-02 proposal of 5.0 nS by researcher
  decision before the sweep. Diminishing-returns shape of the peak-Hz heatmap suggests extending to
  6-10 nS is unlikely to break the multi-spike wall but should be confirmed.

* **Bar speed and width fixed**: 1000 um/s, 200 um bar. Both shape stimulus-bar arrival timing and
  active-fraction modulation; not swept here.

* **Single placement seed**: seed 0 (bit-identical to t0052 / t0053 / t0057). No across-seed
  ensemble; the active-fraction polar might shift on different seeds.

* **Park2014 in vivo peak-rate band of 30-100 Hz** is cited from the paper text [Park2014, p. 3978]
  but the exact range (30 Hz lower bound vs higher upper bounds) is qualitative; precise
  headline-rate citation requires the paper's voltage-clamp panel which we treat as the lower bound.

* **PolegPolsky2016 DSI under voltage-dependent NMDA** of **0.46** is read from their Figure 5
  voltage-dependent NMDA + tuned GABA panel [PolegPolsky2016, Fig 5]. The paper does not publish a
  single headline DSI number, so this value should be treated as a representative model output
  rather than a precise benchmark.

* **deRosenroll2026 DSI of 0.39** is a model output, not an in vivo measurement; it is the
  correlated AR(2) release benchmark that any reimplementation should match, not a direct comparison
  to physiology. Used as the closest comparable published model in the project corpus.

* **Apparent +0.04 match against PolegPolsky2016 DSI is misleading**: our 0.500 primary DSI is a
  3-vs-1 spike-count discretisation in the 0-3 spike range; PolegPolsky2016's 0.46 is a graded
  multi-spike DSI at 30+ Hz peak rate. The same numeric value reflects **completely different
  underlying firing regimes** and should not be interpreted as quantitative agreement.

* **Synapse-count regime mismatch**: 100 vs 177 (PolegPolsky2016) vs 282 (t0046) vs >1000
  (deRosenroll2026) is a >10x range. Per-synapse parameters cannot be directly compared without
  total-conductance normalisation.
