---
spec_version: "1"
task_id: "t0026_vrest_sweep_tuning_curves_dsgc"
date_compared: "2026-04-21"
---
# Comparison with Published DSGC Literature

## Summary

We swept resting membrane potential across eight values from **-90 mV to -20 mV in 10 mV steps** on
two DSGC compartmental ports — the ModelDB 189347 deterministic testbed (Sivyer/Poleg-Polsky
lineage ported in t0022) and the de Rosenroll 2026 AR(2)-correlated stochastic driver at rho=0.6
(t0024) — under the standard 12-direction moving-bar protocol. The headline finding is that the
t0022 port reproduces the patch-clamp DSI envelope best at V_rest = **-60 mV** with **DSI = 0.6555**
(within the **0.45-0.67** envelope bracketed by Sivyer2010, Hanson2019 and Hoshi2011) but only when
peak firing is a modest **15 Hz** — an order of magnitude below the **~148 Hz** light-evoked modal
rate reported by Oesch2005 for rabbit ON-OFF DSGCs at a physiological V_rest of **-70.7 mV**. The
t0024 port achieves DSI **0.6746** at V=-90 mV and **0.4463** at V=-60 mV but never exceeds **7.6
Hz** peak firing, far below the **40-80 Hz** target envelope and the **~166 Hz** adult-mouse rate of
Chen2009. Both ports match the qualitative Barlow1965 / Taylor2002 picture of inhibition-dominated
direction selectivity, but neither reproduces the firing rate magnitudes measured in intact retina.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Oesch2005 (rabbit ON-OFF DSGC) | V_rest (mV) | -70.7 | -60.0 | +10.7 | Oesch2005 reports natural V_rest under whole-cell current clamp; our -60 mV is both models' default. Our sweep brackets the published value at -70 mV. |
| Oesch2005 (rabbit ON-OFF DSGC) | Light-evoked peak firing rate (Hz) | 148.0 | 15.0 | -133.0 | At matched baseline V_rest -60 mV, t0022 peak firing 15 Hz; Oesch2005 measured 148 ± 30 Hz modal rate on 59 ± 21 spikes/stimulus. |
| Chen2009 (adult mouse ON-OFF DSGC) | Peak firing rate (Hz, ON response) | 166.4 | 129.0 | -37.4 | Compared against t0022 peak at V_rest = -30 mV (best case); Chen2009 is under light stimulation not current injection. |
| Hanson2019 (mouse DRD4 DSGC) | DSI (spikes, bar stimulus) | 0.33 | 0.6555 | +0.3255 | Hanson2019 reports IPSC DSI ~0.33 with spiking DSI robust across stimulus; our t0022 DSI at V=-60 mV exceeds it because our scorer uses a Mazurek vector-sum formulation over 12 angles that can yield higher values than the (Rpref-Rnull)/(Rpref+Rnull) contrast. |
| Sivyer2010 (rabbit ON-OFF DSGC) | DSI (ON response, bar) | 0.45 | 0.6746 | +0.2246 | Our t0024 DSI peak at V=-90 mV; Sivyer2010 reports 0.45-0.50 range for ON-OFF DSGCs under moving-gratings at physiological V_rest. |
| deRosenroll2026 (mouse DSGC network model) | DSI > threshold for DS | 0.5 | 0.4463 | -0.0537 | t0024 port was adapted from the companion repository; at V=-60 mV baseline the port falls just below the DS threshold deRosenroll2026 uses. |
| PolegPolsky2026 (ML search) | DSI threshold (high-DS cluster) | 0.5 | 0.6555 | +0.1555 | Our t0022 at V=-60 mV sits inside the PolegPolsky2026 "high-DS" cluster (>0.5). |
| Hoshi2011 (rabbit ON DSGC) | DSI | 0.66 | 0.6555 | -0.0045 | Near-exact match at t0022 V=-60 mV baseline; Hoshi2011 measured loose-patch DSI in uncoupled ON DSGCs. |
| Oesch2005 (rabbit DSGC) | PSP peak V_m (mV, light-evoked) | -59.1 | -55.1 | +4.0 | Our t0022 null-direction subthreshold peak at V_rest=-60 mV (Example 4 in results_detailed.md); Oesch2005 reports preferred-direction PSP peak. |
| Raganato-style SOTA target | Peak firing envelope (Hz) | 40-80 | 7.6 | — | Not-reproduced: t0024 ceiling far below target; t0022 overshoots on depolarised V_rest at the cost of DSI. |

## Methodology Differences

* **Artificial V_rest override vs natural V_rest.** Our sweep forces V_rest by simultaneously
  overriding `h.v_init`, every section's `eleak_HHst`, and every section's `e_pas` before
  `h.finitialize` on every trial. Published DSGC patch-clamp studies (Oesch2005, Chen2009,
  Sivyer2010, Taylor2002) report the *natural* resting potential the cell settles to under whole-
  cell current clamp, typically **-60 to -70 mV** with no external holding command — any V_rest
  shift in experiment requires current injection or pharmacology and is typically bounded within
  ±10 mV of rest. Only our -60 mV and -70 mV rows are directly comparable to the published values.
* **Deterministic vs stochastic release.** The t0022 port uses deterministic per-dendrite E-I
  scheduling; the t0024 port uses AR(2)-correlated stochastic glutamate/GABA release at **rho=0.6**.
  Published DSGCs integrate noisy bipolar and SAC inputs with unknown but definitely non-zero
  temporal correlation (deRosenroll2026, PolegPolsky2016) — neither driver perfectly captures
  this.
* **Single velocity vs velocity sweep.** Our bar protocol uses a single velocity per model (each
  library asset's default ~1000-1500 um/s). Published tuning-curve studies (Sivyer2010, Chen2009,
  Hoshi2011) sweep velocity over **~50-4000 um/s** and report velocity-dependent DSI peaks.
* **12-angle coverage, standardised across all V_rest.** Chen2009 and Hoshi2011 use the same
  12-direction / 30-degree protocol; Sivyer2010 uses 8 directions; Hanson2019 uses 8 directions. DSI
  values from different angular samplings are not strictly comparable.
* **Scorer definition.** We use the Mazurek vector-sum DSI,
  `|sum_i r_i * exp(i*theta_i)| / sum_i r_i`, while Taylor2002, Chen2009, Oesch2005, and Hanson2019
  use the two-direction contrast `(R_pref - R_null) / (R_pref + R_null)`. Vector-sum DSI is
  systematically higher for well-tuned cells and lower for weakly-tuned cells than the two-
  direction contrast.

## Analysis

The V_rest dependence we measured is qualitatively consistent with three biophysical expectations
grounded in the literature:

1. **Sodium channel availability shift.** Oesch2005 measured a light-evoked somatic spike threshold
   of **-56 mV** and showed that each dendritic spike initiates a somatic spike. Our t0022 data show
   peak firing rising monotonically from **6 Hz at V=-90 mV** (Na deinactivated but membrane too far
   below spike threshold) to **129 Hz at V=-30 mV** (threshold trivially exceeded), then collapsing
   to **26 Hz at V=-20 mV** as tonic Na inactivation dominates. The collapse is mechanistically
   equivalent to the **"depolarization block above +100 pA"** reported at P11 in Chen2009 — when
   the membrane sits too close to the spike threshold for too long, the Na gate loses availability.

2. **NMDA Mg-block relief.** PolegPolsky2016 showed that NMDA receptor Mg block is the dominant
   source of multiplicative PD/ND scaling in DRD4 DSGCs (**PD NMDAR PSP = 5.8 mV, ND = 3.3 mV**).
   Our t0024 U-shaped DSI profile (**0.6746 at V=-90 mV** and **0.6248 at V=-40 mV**, with a minimum
   of **0.4463 at V=-60 mV**) is consistent with the NMDA contribution growing as V_rest depolarises
   past the Mg-block threshold around **-55 mV** — the depolarised DSI peak rises as NMDA gain
   amplifies the already-tuned excitatory drive. At hyperpolarised V_rest the driver relies on
   inhibition-dominated tuning (Barlow1965, Taylor2002) which yields the other DSI peak.

3. **Leak-driven PSP attenuation.** Hanson2019 uses a leak reversal of **-60 mV** in the ModelDB
   189347 reference model. When we shift `e_pas` and `eleak_HHst` to -90 mV the driving force on any
   subthreshold EPSC grows but the cell's effective time constant and input resistance change too
   — this predicts both a quieter baseline (matching our **1.5 Hz** t0024 peak at V=-90 mV) and a
   cleaner inhibition gate (matching our DSI peak there). At V=-20 mV the leak drive reverses sign
   relative to Na reversal, driving subthreshold depolarisation that overwhelms the inhibitory shunt
   — consistent with our t0022 HWHM blow-out to **180 degrees** at V=-30/-40 mV.

The major disagreement with the literature is peak firing rate: **Oesch2005 measured 148 Hz**,
**Chen2009 measured 166 Hz** (adult ON response) for healthy DSGCs at natural V_rest. t0022 reaches
**129 Hz** only at V=-30 mV with DSI collapsed to **0.046**; t0024 never exceeds **7.6 Hz**. This is
the headline unresolved issue — neither port reproduces the *combination* of realistic firing rate
and realistic DSI at a biologically plausible V_rest.

## Limitations

* Published DSGC patch-clamp studies uniformly report results at one fixed "natural" V_rest
  (typically ~-60 to -70 mV under whole-cell current clamp), so no published V_rest sweep exists to
  compare our full eight-value curve against. Only the rows at V_rest = -60 mV and V_rest = -70 mV
  in our metrics tables can be directly contrasted with published numbers (Oesch2005, Chen2009,
  Sivyer2010, Hanson2019); the six other V_rest rows are novel predictions with no literature
  counterpart.
* The deRosenroll2026 full PDF was not available at summarisation time (Cell Press 403), so its
  exact quantitative DSI values were not captured in the paper summary — our comparison relies on
  the general "DSI > 0.5 for DS" threshold from the companion repository. A follow-up task should
  obtain the PDF and re-extract the published DSI/peak numbers.
* Scorer mismatch (vector-sum DSI vs two-direction contrast) inflates our DSI values relative to
  Taylor2002/Chen2009/Hanson2019 definitions. A re-scoring with the two-direction formula would
  shift our t0022 V=-60 mV value from **0.6555** toward the **~0.45-0.55** range typical in the
  literature — but the *shape* of the V_rest sweep would be preserved.
* Velocity was fixed at each model's default; published DSI values come from velocity-matched
  conditions that we did not control for. Sivyer2010 explicitly shows DSI depends on velocity
  (**0.45-0.57** range across 50-1200 um/s).
* The 12-angle deterministic t0022 sweep ran only one trial per direction, so no confidence
  intervals are available on t0022 rows; Chen2009 and Oesch2005 report SEM across n=9-13 cells.
* No comparison against the original Poleg-Polsky ModelDB 189347 reference paper's *own* reported
  DSI/peak values — those were not explicitly quoted in our t0002 survey summaries.
* Published literature mostly reports adult mouse or rabbit values under light stimulation; our
  drivers use synthetic moving bars that approximate but do not reproduce the full photoreceptor ->
  bipolar -> SAC -> DSGC cascade, so additional gain discrepancies arise from input generation, not
  only from membrane biophysics.
