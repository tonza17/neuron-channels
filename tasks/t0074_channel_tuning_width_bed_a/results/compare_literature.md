---
spec_version: "1"
task_id: "t0074_channel_tuning_width_bed_a"
date_compared: "2026-05-02"
---
# Compare to Literature: Channel Tuning-Width Sweep on Bed A

## Summary

Compared the t0074 width-metric findings to the source MOD literature (Mainen-Sejnowski 1996 BK, Hay
2011 SK / Kv7), the published RGC channel-modulation literature (Pfeiffer-Friedrich 2012, Wang 2014,
Hu 2007, Shah 2008), and the directional-tuning metric literature (Chen 2009 HWHM, Rivlin-Etzion
2012 vector-sum DSI thresholds). The expected outcomes match the literature for NaP-induced DSI loss
(t0067 reproduced), Kv7 somatic inertness (Hu 2007 prediction), and BK / SK firing-rate suppression
(Pfeiffer-Friedrich, Wang). The most surprising finding — NaR broadening HWHM by +34 deg without
changing peak rate or vector-sum DSI — is not directly addressed in the literature surveyed and is
flagged for follow-up.

## Comparison Table

| Finding | t0074 measured | Published value / prediction | Source | Agreement |
| --- | --- | --- | --- | --- |
| Baseline DSI (no extra channels, no cad) | 0.7975 (delta = 0.0 vs t0067) | 0.7975 | t0067 (this project) | exact |
| NaP_high collapses DSI | vec-DSI 0.193 → 0.050; legacy DSI 0.308 → 0.008 | DSI inverts to negative (t0067 reported -0.18) | t0067; Larsson 2013 reviews persistent-Na suppressing DS | qualitative match |
| Nav1.6 boosts firing without DSI loss | peak 17 → 66 Hz, vec-DSI 0.193 → 0.199 | Nav1.6 boosts firing in DSGCs; AIS-localised effects on AP threshold | Carter-Bean 2009; Trenholm 2014 RGC Nav1.6 | match |
| BK firing-rate suppression (Ca-driven) | peak 17 → 13 Hz at high density; vec-DSI -0.04 | BK suppresses high-rate firing in mouse RGCs | Pfeiffer & Friedrich 2012 (mouse RGC BK) | match |
| SK firing-rate suppression (Ca-driven) | peak 17 → 16 Hz; HWHM 84 → 41 deg at high density | SK suppresses firing rate; reduces firing variability | Wang et al. 2014 (RGC SK) | partial — HWHM narrowing not reported |
| Kv7 somatic inertness | unchanged across all 3 densities | "Kv7 site is the AIS, not the soma" | Hu 2007 (Pyr cells); Shah 2008 (review) | match |
| Kv3 inertness at 20 Hz peak rates | unchanged across all 3 densities | Kv3 engages strongly above 100 Hz; minimal effect at 20 Hz | Erisir 1999; Rudy & McBain 2001 | match |
| Kv4 / IA inertness | unchanged across all 3 densities | Kv4 needs hyperpolarising prepulse to remove inactivation | Hoffman 1997; Cudmore 2010 | match |
| HWHM as direction-tuning width metric | baseline 84 deg | DSGC HWHM "tens of degrees" (typically 60-100 deg); mouse alpha-RGC ~70 deg | Chen 2009 (mouse RGC); Wei 2018 (DSGC review) | match |
| Vector-sum DSI threshold for DS classification | baseline 0.193 (just below 0.2) | classified DS if vector-sum DSI > 0.2 AND DSI_PD-ND > 0.3 | Rivlin-Etzion 2012 | borderline |
| NaR broadens HWHM without affecting DSI | HWHM 84 → 117 / 120 deg at med / high; vec-DSI unchanged | not directly studied at the somatic level | Khaliq 2003 (Purkinje NaR); Lewis 2014 review | NEW — no published comparison |
| RMSE vs target tuning curve | baseline 13.83 Hz; NaP_high 55.44 Hz | n/a — the t0004 cosine target is project-specific | t0004 (this project) | n/a |

## Methodology Differences

* **t0074 uses NONSPECIFIC_CURRENT** in all 9 channel MODs to avoid USEION conflicts with HHst's
  three USEIONs (na / k / ca). Published BK / SK / Kv7 mechanisms in their original ModelDB forms
  use proper ionic currents. This means the channels in t0074 contribute synthetic non-ionic
  currents rather than altering true [K]_i / [Na]_i / [Ca]_i. For the gross effects measured here
  (firing rate, tuning width) the difference is negligible because HHst's reversal potentials are
  the dominant determinant; for finer effects (e.g., spike afterhyperpolarisation shape) it could
  matter.

* **t0074 uses Bed A's existing CaT / CaL via HHst** rather than vendoring separate CaT / CaL
  channels. Published BK / SK models normally couple to dedicated CaT / CaL mechanisms. We un-zero
  HHst's internal CaT / CaL gbars instead. This mixes the published Ca-pool dynamics (from cadecay)
  with HHst's L- and T-type currents. The validation that Bed A's regression DSI reproduces exactly
  (delta = 0.0) when cad is absent demonstrates the un-zeroing alone does not introduce drift.

* **Density grid is coarse (3 levels)** vs published density-response curves (6+ levels). The task
  description's pass criterion (each channel produces measurable change at >= 1 density) is
  satisfied by all 5 non-inert channels; finer threshold characterisation (e.g., the exact density
  where NaP transitions from rate-amplifier to DSI-eroder) requires a denser grid in a follow-up.

* **Single substrate (Bed A only)**: published RGC channel data come from a mix of mouse alpha,
  ON-OFF DSGC, and goldfish RGCs. The closest published DSGC channel-modulation work is Trenholm
  2014 (mouse DSGC AIS Nav1.6) and de-Rosenroll 2026 (Bed B in this project). Direct comparison to a
  single published "DSGC + BK" condition is not available — the literature characterises BK / SK
  in non-DSGC RGCs.

* **t0074 uses the gabaMOD-swap variant for the regression gate but bar-rotation for the sweep.**
  This is intentional: the regression gate must match t0067's reference fingerprint (DSI = 0.7975
  under the gabaMOD-swap protocol), while the sweep itself uses the model's native 12-angle
  bar-rotation protocol (per t0046 reproduction). Comparison to published literature is via the
  bar-rotation sweep; the gate is a code-path validation only.

## Analysis

**Where t0074 confirms the literature**:

* **NaP-induced DSI loss** is reproduced from t0067 (this project) and confirms Larsson 2013's
  prediction that persistent Na current suppresses direction selectivity by saturating the cell's
  response.

* **BK suppression of firing** matches Pfeiffer-Friedrich 2012 mouse RGC BK behavior. Our BK doesn't
  have the in-vitro voltage-clamp validation they performed, but the gross effect (lower peak rate,
  mild DSI reduction) is consistent.

* **Kv7 somatic inertness** confirms Hu 2007's prediction (which was based on cortical pyramidal
  neurons where Kv7 was demonstrated to be AIS-localised). Our DSGC result extends this finding to a
  retinal cell type, supporting the AIS-localised follow-up (t0075).

* **Kv3 / Kv4 inertness** at the firing rates we reach (peak ~20 Hz) is consistent with Rudy &
  McBain's 2001 review identifying Kv3 as a "fast-spiking-cell" channel that engages above 100 Hz,
  and Hoffman 1997's observation that Kv4 requires hyperpolarisation to remove inactivation.

**Where t0074 extends the literature**:

* **NaR broadening HWHM without affecting peak rate or vector-sum DSI** is not directly described in
  the literature surveyed. The closest precedent is Khaliq 2003's NaR work in Purkinje cells, which
  characterises the channel's slow `s` reactivation gate but does not measure tuning-curve width
  effects. The t0074 finding suggests NaR's slow reactivation creates a "subthreshold floor" that
  pushes ND-direction firing above zero, broadening the curve symmetrically — a hypothesis that
  should be tested by inspecting the per-trial spike counts at angles 90-180 deg (the ND lobe).

* **SK_high HWHM narrowing to 41 deg** is a much more dramatic effect than reported for SK in RGCs
  (Wang 2014 reports modest firing-rate reduction but no dramatic tuning narrowing). Three
  possibilities: (1) SK at 0.6 mS/cm² is super-physiological; (2) the narrowing is a flat-top
  clipping artefact (creative-thinking step); (3) SK in DSGCs is genuinely more width-modulating
  than in non-DSGCs. The follow-up suggested in the creative-thinking step (plot the polar curve to
  distinguish narrowing from clipping) will resolve which.

**Where t0074 is in modest tension with the literature**:

* Our with-cad **baseline vector-sum DSI of 0.193 sits just below Rivlin-Etzion 2012's
  classification cutoff of 0.2**. This is a known calibration concern: the 0.2 cutoff was
  established for in-vivo recorded DSGCs; our compartmental model may have a slightly different
  baseline. The 0.193 is comfortably within the population spread Rivlin-Etzion reports (mouse DSGC
  vector-sum DSI ranges 0.07-0.85 across recorded cells).

* The legacy DSI_PD-ND of 0.308 (with-cad) vs 0.797 (no-cad regression gate) shows that adding cad
  at zero density already shifts ND-direction firing by ~1 spike/trial. This is partly an artefact
  of our soma-only insertion — published BK / SK models that integrate Ca-pool with CaT / CaL
  distributed across the cell would show smaller substrate shifts. Documented as a limitation;
  follow-up could test cad insertion only on dendrites + AIS rather than the soma.

## Limitations

* **No direct DSGC + BK / DSGC + SK / DSGC + Kv7 published comparison exists.** The closest
  references are Pfeiffer-Friedrich 2012 (mouse alpha-RGC, not DSGC), Wang 2014 (mouse RGC, not
  DSGC), and Hu 2007 (cortical pyramidal). Our DSGC-specific findings are novel; we can only confirm
  broad agreement (suppression direction matches), not quantitative match (Hill coefficients, EC50
  values, density thresholds).

* **The vector-sum DSI 0.2 / DSI_PD-ND 0.3 classification cutoffs (Rivlin-Etzion 2012)** apply to
  in-vivo recordings where SAC inputs and synaptic noise produce a different stochastic regime than
  our deterministic compartmental model. Strict cutoff-based classification ("borderline DS at
  baseline") should be interpreted with this caveat.

* **The cosine target curve (t0004)** is a project-internal optimisation reference, not a published
  literature value. No literature comparison is available for `rmse_vs_t0004`.

* **No biophysical validation of vendored MODs against patch-clamp data**: the BK MOD comes from
  Mainen-Sejnowski 1996 (cortical pyramidal neuron), the SK and Kv7 MODs come from Hay 2011 (L5
  pyramidal). Their kinetics may not match RGC patch-clamp recordings exactly. The plan's fallback
  (validate vs Pfeiffer-Friedrich 2012 / Wang 2014 RGC patch-clamp) was not exercised because the
  vendored MODs produced stable, sensible behaviour in the regression gate and the sweep. A post-hoc
  validation against RGC patch-clamp data is a recommended follow-up but is outside this task's
  scope.

* **Kv7 follow-up at the AIS (t0075)** is the canonical next step for the only inert channel with a
  clear AIS-mismatch literature signal. The other two inert channels (Kv3, Kv4) need different
  experimental designs (high-firing-rate condition for Kv3; hyperpolarising prepulse for Kv4) to be
  tested fairly.
