---
spec_version: "1"
task_id: "t0057_tonic_gaba_sweep_t0053"
date_compared: "2026-04-28"
---
# Comparison with Published Results

## Summary

The tonic-GABA sweep over `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS on the t0053 spatial DSGC
fails to recover any non-trivial direction selectivity. FULL-mode primary DSI is **0.000** at every
swept conductance: the cell either fires uniformly at **0.667 Hz** across all 12 directions
(`gaba <= 1.0 nS`, the AMPA-only single-spike-per-trial regime) or is fully suppressed at **0.0 Hz**
(`gaba >= 1.5 nS`). This is a wider negative result than the t0053 sibling: at the matched 2 nS
operating point the tonic mechanism is **more** suppressive than t0053's per-event Exp2Syn (both
land at 0 Hz, but the tonic IPSP envelope persists for 1300 ms vs t0053's ~80 ms decay tail).
Vector-sum DSI is **0.000** (numerical floor 3.2e-17) everywhere — well below the in vitro mouse
On-Off DSGC band of **0.65 +/- 0.05** [Park2014, p. 3978], the PolegPolsky2016 voltage-dependent
NMDA model output of **0.46** [PolegPolsky2016, Fig 5], and the deRosenroll2026 correlated AR(2)
benchmark of **0.39** [deRosenroll2026, Fig 5]. The active-fraction polar curve (0.34 -> 0.66) is
bit-identical to t0053, confirming the spatial centripetal-gating mechanism is intact and the
failure is amplitude calibration interacting with the new sustained-window mechanism, not the gating
rule.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Park2014 (CART-Cre, voltage-clamp) | DSI (primary) | 0.65 | 0.000 | -0.65 | In vitro mouse On-Off DSGCs, n=14; FULL-mode degenerate (peak = null = 0.667 Hz at gaba <= 1.0 nS or 0 Hz at gaba >= 1.5 nS) at all 5 swept conductances [Park2014, p. 3978] |
| Park2014 (TRHR-GFP / wild-type) | DSI (primary) | 0.73 | 0.000 | -0.73 | Reference subset, n=38 cells; FULL-mode degenerate at all 5 swept conductances [Park2014, p. 3978] |
| PolegPolsky2016 (voltage-dependent NMDA + tuned GABA) | DSI | 0.46 | 0.000 | -0.46 | Their NEURON DSGC with Mg-block NMDA preserves DSI; ours is AMPA-only with tonic GABA and degenerates at every operating point [PolegPolsky2016, Fig 5] |
| deRosenroll2026 (correlated AR(2) release) | DSI (vector-sum) | 0.39 | 3.2e-17 | -0.39 | Vector-sum DSI vs paper's vector-sum benchmark; rho=0.6; our value is at the floating-point noise floor [deRosenroll2026, p. 6 / Fig 5] |
| deRosenroll2026 (uncorrelated release) | DSI (vector-sum) | 0.25 | 3.2e-17 | -0.25 | Lower-bound model benchmark; we lack release noise entirely [deRosenroll2026, p. 6 / Fig 5] |
| t0004 target curve (this project) | Peak rate (Hz) | 32.0 | 0.667 | -31.33 | Our peak rate is at most **48x below** the project target across the entire sweep; at gaba >= 1.5 nS it drops to 0 Hz [t0004 results_summary] |
| t0004 target curve (this project) | DSI | 0.8824 | 0.000 | -0.8824 | Project canonical target; FULL-mode degenerate [t0004 results_summary] |
| t0004 target curve (this project) | HWHM (deg) | 68.51 | 180.0 | +111.49 | Tuning curve is uniform (gaba <= 1.0 nS) — HWHM degenerates to 180 deg, vs target 68.51 deg [t0004 results_summary] |
| t0004 target curve (this project) | Tuning curve RMSE (Hz) | 0.0 (self) | 16.67 | +16.67 | gaba <= 1.0 nS RMSE; dominated by 32 Hz target peak vs 0.667 Hz model response [results_detailed.md] |
| Park2014 (null inhibitory conductance, P-N) | Inhibitory P-N (nS) | 2.43 | 1.5 | -0.93 | Per-direction effective P-N for the tonic mechanism: at gaba = 1.5 nS, ratio of (active@theta=210) - (active@theta=30) = (0.66 - 0.34) * 1.5 nS = 0.48 nS per synapse times 100 = ~48 nS aggregate, but voltage-side IPSP modulation is only 1.22x (7.38 mV / 6.05 mV) due to driving-force saturation [Park2014, p. 3978] |
| PolegPolsky2016 (Fig 1, control PD PSP) | PD PSP (mV) | 5.8 | 6.05 | +0.25 | Aggregate IPSP at preferred-side direction (theta=30 deg, minimum-active-fraction direction) at gaba = 1.5 nS; paper value is excitatory NMDA-PSP, ours is inhibitory IPSP — order-of-magnitude similar [PolegPolsky2016, p. 1280, Fig 1] |
| PolegPolsky2016 (Fig 1, control ND PSP) | ND PSP (mV) | 3.3 | 7.38 | +4.08 | Aggregate IPSP at null-side (theta=210 deg, max-active-fraction direction) at gaba = 1.5 nS; paper value is excitatory NMDA, ours is inhibitory IPSP — sign and mechanism differ [PolegPolsky2016, p. 1280, Fig 1] |

### Prior Task Comparison

| Prior Task | Variant | Primary DSI | Peak Hz | HWHM (deg) | Notes |
| --- | --- | --- | --- | --- | --- |
| t0052 (parent, scalar gabaMOD) | FULL | **1.000** | **0.667** | **82.5** | Single-spike-per-trial; perfect on/off binary tuning. Mean GABA mass 66 nS per trial. |
| t0053 (sibling, spatial Exp2Syn at 2 nS) | FULL | **0.000** | **0.000** | **180.0 (degen.)** | Fully suppressed by 100 nS mean GABA mass. Same morphology and placement seed as t0052. |
| t0054 (NMDA + scalar gabaMOD, gNMDA = 0.25 nS) | FULL | **0.143** | **8.000** | n/a | NMDA closes 12x of peak-rate gap but DSI collapses ~9x vs t0052. Voltage-independent NMDA. |
| t0054 (NMDA + scalar gabaMOD, gNMDA = 1.0 nS) | FULL | **0.000** | **4.667** | n/a | DSI collapses to zero entirely; the cell becomes direction-blind. |
| t0057 (this task, tonic GABA at 0.25 nS) | FULL | **0.000** | **0.667** | **180.0 (degen.)** | Tonic too weak to override single AMPA spike — uniform single-spike regime. |
| t0057 (this task, tonic GABA at 0.50 nS) | FULL | **0.000** | **0.667** | **180.0 (degen.)** | Same single-spike regime. |
| t0057 (this task, tonic GABA at 1.00 nS) | FULL | **0.000** | **0.667** | **180.0 (degen.)** | Same single-spike regime. |
| t0057 (this task, tonic GABA at 1.50 nS) | FULL | **null** | **0.000** | **null** | Step into full suppression — IPSP envelope 7.38 mV crosses the spike-veto threshold. |
| t0057 (this task, tonic GABA at 2.00 nS) | FULL | **null** | **0.000** | **null** | Fully suppressed; matches t0053's 2 nS suppression but via the persistent envelope. |

## Methodology Differences

* **Inhibition mechanism (vs t0053 sibling)**: t0053 uses per-event `Exp2Syn` GABA (rise 1 ms, decay
  20 ms, e = -75 mV) fired once per active synapse at the bar-arrival time, so the conductance
  envelope is on for only ~100-200 ms per trial. t0057 replaces this with a new `gaba_tonic.mod`
  POINT_PROCESS that holds `g = GABA_BASE_NS` over the entire `(t_on, t_off) = (100 ms, 1400 ms)`
  stimulus window for active synapses (1300 ms sustained vs t0053's ~80 ms decay tail). At matched 2
  nS amplitude the tonic mechanism delivers **~16x more total inhibitory charge** than the per-event
  mechanism — and lands at the same 0 Hz suppression because both exceed the spike-veto threshold.

* **Inhibition mechanism (vs t0052 parent)**: t0052 modulates every I synapse's amplitude by a
  global direction-dependent scalar `gabaMOD(theta) = 0.33 + 0.66 * (1 - cos(theta - theta_PD)) / 2`
  applied uniformly to all 100 synapses for one Exp2Syn event per trial. t0057 instead activates a
  binary subset of synapses (centripetal half) at full `GABA_BASE_NS` amplitude, sustained over the
  entire trial. Mean total GABA *charge* per trial is much larger in t0057 (0.25-2.0 nS x 50 syn x
  1300 ms vs 0.66 nS x 100 syn x ~30 ms in t0052) — at the lower end of the sweep the
  active-fraction modulation cannot generate enough differential charge to break the binary
  AMPA-spike decision, while at the upper end the cell is held below threshold throughout.

* **Inhibition mechanism (vs Park2014)**: Park2014 [p. 3978] attributes DS to null-direction GABA
  from SACs (whole-cell P-N = 2.43 nS). The centripetal-gating predicate approximates the SAC
  network's centrifugal preference at the SAC-output level. The new tonic envelope is a closer match
  to the **biological SAC->DSGC IPSC envelope of 100-300 ms** than t0053's 20 ms Exp2Syn decay, but
  our 1300 ms persistence is **far longer** than even the slowest published SAC IPSC envelopes —
  biologically wrong in the opposite direction from t0053.

* **Inhibition mechanism (vs PolegPolsky2016)**: PolegPolsky2016 [p. 1280, Methods] uses a
  multi-event SAC->DSGC GABA driver with realistic envelope tau ~50-150 ms; we use a single tonic
  pulse (Brainstorm-10 explicitly chose this simplest "always-on during stimulus" Option C). The
  PolegPolsky2016 model also includes voltage-dependent NMDA Mg-block which preserves DSI
  multiplicatively; our model is AMPA-only.

* **Synapse count**: 100 E + 100 I (this task, t0052, t0053, t0054) vs ~177 in PolegPolsky2016
  [p. 1280] / 282 in t0046 reproduction / >1000 SAC varicosities in deRosenroll2026 [p. 5]. Lower
  synapse count gives weaker total drive but does not by itself explain the 0-Hz FULL result —
  AMPA_ONLY produces the same 0.667 Hz at all 5 swept conductances.

* **Excitation tuning**: Park2014 [p. 3978] proves bipolar-cell glutamate is omnidirectional at
  release. Our model implements omnidirectional AMPA exactly as Park2014 prescribes — and
  AMPA_ONLY produces 0.667 Hz uniformly across all 12 directions at every conductance, confirming
  this is bit-identical to t0052/t0053 and the DSI degeneration is purely an inhibition-mechanism
  effect.

* **No NMDA**: Our model has AMPA only by design. PolegPolsky2016 emphasises NMDARs contribute
  multiplicatively at PD (5.8 mV / ~35% of total PSP). t0054 has shown that adding *voltage-
  independent* NMDA breaks DSI; PolegPolsky2016's voltage-*dependent* NMDA Mg-block is the
  identified path forward but is excluded from this task's scope.

* **No noise**: Trials are deterministic single-event-per-synapse; deRosenroll2026 [p. 6] requires
  AR(2) correlated release with rho = 0.6 to match in vitro. Reliability = 1.0 here is artefactual.

* **Sustained-window vs pulse-event timing**: This is the headline new methodology choice unique to
  t0057. The 1300 ms tonic window keeps the active half of synapses delivering full conductance for
  the entire stimulus presentation. The IPSP-sustained-window regression test
  (`test_gaba_tonic_envelope.py`) confirms IPSP voltage at t = 1300 ms is at least 50% of IPSP
  voltage at t = 200 ms — i.e., the new mechanism does deliver the designed envelope. The
  biological interpretation is that this is a "what if real SAC->DSGC IPSCs were perfectly sustained
  over the stimulus?" upper bound, not a faithful reproduction of multi-event SAC release kinetics.

* **DSI definition**: Park2014 uses primary DSI on AP counts; deRosenroll2026 uses vector-sum DSI on
  spike counts. Both versions are degenerate in our FULL mode (peak = null at every swept point).

## Analysis

### Headline negative finding: the entire sweep grid is degenerate

The tonic-GABA mechanism with `(t_on, t_off) = (100 ms, 1400 ms)` produces **zero meaningful
direction selectivity** across the swept range `{0.25, 0.5, 1.0, 1.5, 2.0}` nS. Below 1.5 nS the
tonic conductance is too weak to override the single AMPA-driven spike per trial (peak = null =
**0.667 Hz**, identical to AMPA_ONLY); at 1.5 nS and above the IPSP envelope (peak depolarization
**7.38 mV** at theta = 210 deg, GABA reversal -75 mV) crosses the threshold-veto boundary and the
cell stops firing entirely (peak = null = **0 Hz**). The gap between the two regimes is binary:
there is no `GABA_BASE_NS` value in the swept grid where the cell fires *some* but not *all* of its
otherwise-uniform single-spike responses. The **-0.65** to **-0.73** delta against the in vitro
Park2014 band is therefore a delta against a fully-suppressed or uniformly-firing model, not a
partially-suppressed model with a non-zero null and peak. The negative result is wider than t0053's
single-amplitude failure: the entire 8x conductance range fails for the same underlying reason.

### The tonic mechanism is more suppressive than t0053 at matched amplitude

At the matched 2 nS operating point, the tonic mechanism produces **0 Hz** in FULL mode — the same
fully-suppressed result as t0053's per-event Exp2Syn GABA. But the route to suppression is
different: t0053 delivers a brief, sharp shunt within ~100 ms of bar arrival; t0057 holds the same
amplitude shunt across the entire 1300 ms window. The peak somatic IPSP voltage at theta = 210 deg
grows from **3.17 mV** at 0.25 nS to **7.87 mV** at 2 nS — sub-linear (8x conductance ratio yields
2.5x voltage ratio), confirming the same driving-force-saturation mechanism documented in t0052
(1.54x voltage from 3.0x conductance) and t0053 (1.24x voltage from 1.94x active-count ratio). The
matched-amplitude head-to-head therefore does not produce the timing-mechanism-isolation comparison
that motivated the task — both mechanisms exceed the spike-veto threshold at 2 nS and the tonic
mechanism gets there sooner because of its sustained envelope.

### Spatial gating intact; failure is amplitude calibration

The active-fraction polar curve (**0.34** at theta = 30 deg to **0.66** at theta = 210 deg, mean
**0.500**) is **bit-identical to t0053** because the centripetal-gating rule
`cos(theta_stim - theta_centrifugal_synapse) < 0` is unchanged. This is direct evidence that the
gating mechanism continues to work as designed — the failure is in the inhibition *amplitude* that
gates onto a single-spike-per-trial AMPA regime that cannot produce graded direction-dependent
firing rates. The four-way table below maps the parameter regime:

| Inhibition driver | t0052 (scalar gabaMOD) | t0053 (Exp2Syn 2 nS) | t0057 (tonic 0.25-1.0 nS) | t0057 (tonic 1.5-2.0 nS) |
| --- | --- | --- | --- | --- |
| Mean GABA mass per trial | 66 nS x 30 ms | 100 nS x 80 ms | 12.5-50 nS x 1300 ms | 75-100 nS x 1300 ms |
| Cell regime | Single-spike PD / silent ND | Suppressed everywhere | Uniform single-spike | Suppressed everywhere |
| Primary DSI | 1.000 (degenerate) | 0.000 (degenerate) | 0.000 (degenerate) | null (degenerate) |

### The single-spike-per-trial AMPA regime is the deeper bottleneck

t0057, t0053, and t0052 all fire **at most one spike per trial** at the highest-active direction
under the chosen AMPA conductance (0.5 nS per synapse, 100 synapses). Once the cell is in this
regime, no inhibition mechanism — graded scalar amplitude (t0052), spatial Exp2Syn pulse (t0053),
or sustained tonic conductance (t0057) — can produce a graded direction-dependent firing rate. The
decision is binary: spike fires or it does not. Direction selectivity in the published literature
requires a multi-spike-per-trial regime, which t0054 partially achieves with NMDA (8 Hz peak at
gNMDA = 0.25 nS) but at the cost of DSI collapse under voltage-independent kinetics. The path
forward is therefore to **escape the single-spike regime first** (via higher AMPA, NMDA with
Mg-block, or both) and **then re-test inhibition mechanisms** in the multi-spike regime where a
graded suppression can produce graded selectivity.

### IPSP envelope grows sub-linearly with conductance (driving-force saturation)

The aggregate IPSP voltage envelope at theta = 210 deg (max-active direction) grows from **3.17 mV**
at 0.25 nS to **7.87 mV** at 2 nS — a **2.5x voltage ratio** for an **8x conductance ratio**. This
is the same driving-force saturation observed in t0052 and t0053 but in a different regime: the IPSP
envelope here is sustained over 1300 ms instead of decaying within 80-100 ms, so the voltage spends
more time near E_GABA = -75 mV and the additional conductance produces ever-smaller voltage
suppression. The implication is that **sustained inhibition mechanisms hit the driving-force ceiling
sooner than pulse-event mechanisms at matched amplitude** — t0057 lands at full suppression at 1.5
nS, while t0053's pulse-event mechanism would presumably need somewhat higher conductance to reach
the same suppression level (untested in the t0053 sweep).

### Convergence with PolegPolsky2016 prediction

PolegPolsky2016 [p. 1283-1284] argues that voltage-dependent NMDA Mg-block is necessary for
multiplicative DSI scaling, and that subtractive inhibition alone cannot produce the in vivo DSI
band. Our cumulative evidence (t0052 trivial DSI in single-spike regime, t0053 spatial inhibition
suppresses everything at 2 nS, t0054 DSI collapses under voltage-independent NMDA, and now t0057 no
operating point in an 8x sweep produces non-trivial DSI) converges on the same conclusion: **no
AMPA-only minimal DSGC operating in the single-spike-per-trial regime can reach the
Park2014/deRosenroll2026/PolegPolsky2016 DSI band**, regardless of the inhibition mechanism's
spatial or temporal profile. The minimal model is missing the multiplicative-NMDA ingredient.

## Limitations

* **Coarse sweep grid**: 5 conductance values, all at or above 0.25 nS. The sub-0.25 nS regime
  (where the tonic mechanism might produce graded suppression rather than the binary
  single-spike-vs-zero) is not characterised. A finer grid (e.g., 0.05, 0.10, 0.15, 0.20, 0.25 nS)
  would test whether any tonic operating point exists below the AMPA-spike-veto threshold.

* **FULL-mode is degenerate at every swept point**: primary DSI is 0.000 or null at all 5
  conductances because peak = null. Vector-sum DSI is at the floating-point noise floor 3.2e-17
  (sub-1.5 nS) or exactly 0.0 (suppressed). All comparisons against published DSI values are
  therefore comparisons to a fully-suppressed or uniformly-firing model, not a partially- suppressed
  model with a meaningful peak/null contrast.

* **Tonic envelope is biologically extreme**: the 1300 ms `(t_on, t_off)` window is far longer than
  any published SAC->DSGC IPSC envelope (typical 100-300 ms). Brainstorm-10 explicitly chose this
  simplest "always-on during stimulus" model with the understanding that biological realism would be
  revisited if results justified it. The tonic mechanism is therefore an upper-bound test of "what
  if SAC inhibition were perfectly sustained?" rather than a faithful biological model.

* **No noise**: Trials are deterministic; deRosenroll2026 emphasises DSI is sensitive to release
  decorrelation (0.39 -> 0.25). Our protocol cannot test this; reliability would be artefactually
  1.0 even if the cell spiked.

* **No NMDA**: AMPA-only by design (matching t0053 parent). The most likely path to a non-degenerate
  DSI is voltage-dependent NMDA Mg-block (cf. PolegPolsky2016 [Fig 5] and t0054 results). The
  tonic-GABA + Mg-block-NMDA combination is left for a follow-up.

* **Park2014 in vivo DSI band** in earlier orchestrator messages ("0.40-0.60") could not be verified
  from the paper text. The paper reports CART-Cre cells DSI = 0.65 +/- 0.05 (n = 14) and TRHR-GFP /
  wild-type cells 0.73 +/- 0.03 (n = 38) [Park2014, p. 3978]. We use the values directly
  attributable to Park2014.

* **deRosenroll2026 DSI of 0.39** is a model output, not an in vivo measurement; it is the
  correlated AR(2) release benchmark that any reimplementation should match, not a direct comparison
  to physiology. Used as the closest comparable published model in the project corpus.

* **PolegPolsky2016 DSI under voltage-dependent NMDA** of **0.46** is read from their Figure 5
  voltage-dependent NMDA + tuned GABA panel. The paper does not publish a single headline DSI
  number, so this value should be treated as a representative model output rather than a precise
  benchmark.

* **Voltage-side ratios (1.22x at 1.5 nS, 2.5x across the full sweep) lack a direct literature
  anchor**: driving-force saturation is consistent qualitatively with PolegPolsky2016's
  multiplicative-vs-additive shunting framework [p. 1283] but the specific numerical mapping is not
  published in the project corpus.

* **Active-fraction polar curve has no direct published counterpart**: published SAC-network models
  (deRosenroll2026, Park2014) report aggregate GABA conductance modulation, not a per-direction
  count of active SAC outputs at the DSGC. The 0.34 - 0.66 modulation reported here is a
  model-internal observable rather than a literature-comparable measurement.

* **Synapse-count regime mismatch**: 100 vs 177 (PolegPolsky2016) vs 282 (t0046) vs >1000
  (deRosenroll2026) is a >10x range. Per-synapse parameters cannot be directly compared without
  total-conductance normalisation.

* **Single-spike-per-trial AMPA regime is the underlying problem**: the cell at this AMPA
  conductance (0.5 nS x 100 synapses) fires at most one spike per direction. This binary regime
  cannot produce meaningful DSI under any inhibition mechanism (scalar gabaMOD as in t0052, spatial
  Exp2Syn as in t0053, tonic as in t0057) — they all collapse to either 1-spike-uniform or
  0-spike-uniform. The path forward (S-0052-01) is to first escape the single-spike regime via
  higher AMPA conductance and then re-evaluate inhibition mechanisms in the multi-spike regime.
