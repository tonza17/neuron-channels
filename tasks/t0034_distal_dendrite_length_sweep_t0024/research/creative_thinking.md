---
spec_version: "1"
task_id: "t0034_distal_dendrite_length_sweep_t0024"
research_stage: "creative_thinking"
date_completed: "2026-04-22"
status: "complete"
---
# Creative Thinking: Distal-Dendrite Length Sweep on the t0024 DSGC Port

## Objective

The sweep produced a non-monotonic decrease in primary DSI (0.774 at 0.5x, 0.770 at 1.00x, dipping
to 0.623 at 1.5x, bouncing to 0.720 at 1.75x, then 0.545 at 2.0x) with a weak negative slope
(-0.1259 per unit multiplier, p = 0.038, R^2 = 0.61) and a vector-sum DSI that drifts monotonically
from 0.507 down to 0.357 (slope -0.082, p < 0.001). Peak firing declines monotonically from 5.7 Hz
to 3.4 Hz as length grows, while null firing fluctuates between 0.7 and 1.0 Hz. Neither Dan2018's
predicted monotonic INCREASE (passive transfer-resistance weighting) nor Sivyer2013's predicted
saturating plateau (dendritic-spike branch independence) fits this pattern. This document considers
alternative mechanisms that are consistent with the downloaded corpus and could jointly produce a
gentle, noisy, non-monotonic primary-DSI decrease together with a steady vector-sum DSI decline and
a clean peak-firing attenuation.

## Alternatives Considered

1. **Passive cable filtering past the optimal electrotonic length** (Tukker2004, Hausselt2007). *a*:
   DSI peaks at an intermediate electrotonic length constant comparable to the dendritic spread and
   falls on either side as low-pass filtering attenuates the soma-to-tip voltage gradient that any
   DS mechanism needs ([Tukker2004] found a lambda ~400 um optimum; [Hausselt2007] saw DSI drop from
   0.35 at 150 um to 0.12 at 50 um). *b*: Unlike Dan2018 (pure TR reweighting, monotonic up) or
   Sivyer2013 (active-spike saturation, saturating up), this predicts a cable-filtering optimum near
   baseline with BOTH shorter and longer extremes losing DSI — matching the 0.5x and 2.0x
   endpoints sitting below 1.0x on the vector-sum curve and below 0.5x on the primary curve. *c*:
   Supporting data: measure somatic EPSP rise-time and half-width vs multiplier (slower rise at
   longer L) and the soma-to-tip voltage gradient for a single preferred-direction sweep; rule out
   by finding unchanged EPSP waveform. *d*: Follow-up — sweep `sec.diam` jointly with `sec.L` to
   map the 2D electrotonic plane and locate the DSI ridge.

2. **Dendritic HCN / Ih current increases with distal membrane area**. *a*: Longer distal cables
   integrate more Ih membrane; Ih provides a tonic depolarising shunt that lowers input resistance
   and attenuates small EPSPs, which could compress preferred- and null-direction responses
   differently. *b*: This is a channel-mediated, length-proportional shunt rather than the
   length-independent TR gradient of Dan2018 or the threshold amplification of Sivyer2013. *c*:
   Supporting data: soma input resistance drops systematically with multiplier; blocking Ih (ZD7288
   in silico — set `gbar_HCN = 0`) would rescue the high-L DSI. *d*: Follow-up — repeat the
   sweep with Ih nulled and compare slopes; a much flatter or positive slope would confirm an Ih
   contribution. The de Rosenroll 2026 HOC template must first be audited for an explicit HCN
   mechanism (Aldor2024 flags perisomatic Kv3 and dendritic mGluR2 for SACs, so channel density on
   DSGC terminals matters).

3. **Kv3-like high-threshold K+ rectification clips preferred-direction spikes more at long L**.
   *a*: Longer cable delays spike backpropagation and prolongs the dendritic depolarisation window,
   allowing high-threshold K+ currents (Kv3, Kv4) to repolarise before the null-direction envelope
   has decayed, differentially suppressing the preferred-direction peak. *b*: Sivyer2013 predicts
   saturating amplification; this predicts saturating or decreasing amplitude because the K+
   rectifier fights the same spike that the Na/Ca channels initiated. *c*: Supporting data: peak-mV
   traces should show earlier repolarisation at long L even when spike count is preserved. Partial
   confirmation: `mean_peak_mv` in `metrics_per_length.csv` is highest at 1.25x (32.5 mV) and drops
   to 28.3 mV at 1.5x, consistent with earlier repolarisation at extreme lengths. *d*: Follow-up
   task — halve `gbar_Kv3` and re-run a 3-point confirmation sweep (0.5x, 1.0x, 2.0x).

4. **Local distal spike failure at extreme lengths**. *a*: Schachter2010 showed distal input
   resistance >1 GOhm lowers the local dendritic-spike threshold, but cable length past the
   electrotonic space constant can decouple distal tips from the soma so that local spikes either
   fail to propagate OR fail to initiate because the chord conductance of the extended cable drains
   the local depolarisation. *b*: Unlike Sivyer2013 (reliable local spikes saturate DSI) this
   predicts an abrupt DSI dip when the cable crosses a failure threshold. *c*: Supporting data: the
   primary DSI dip at 1.5x (0.62) with preferred-direction angle shifting to 330 deg instead of 0
   deg strongly hints at an unreliable regime; the preferred angle also shifts to 30 deg at 2.0x.
   These preferred-direction jumps are signatures of angular instability that the intermediate 1.25x
   and 1.75x points do not share. *d*: Follow-up — record per-trial spike counts at the distal tip
   vs soma for the 1.5x and 2.0x conditions; a spike-count ratio < 1 at distal tips confirms local
   failure.

5. **Stochastic-release smoothing saturates at long L** (an AR(2) interaction). *a*: t0034
   introduces rho=0.6 AR(2) correlated release; longer cables integrate over more synaptic release
   events per unit time, temporally smoothing the AR(2) noise floor. This could raise null firing
   (slight increase in the 1.5x and 2.0x rows to 1.0 Hz) while preferred firing attenuates from 5.7
   to 3.4 Hz, compressing the DSI numerator faster than the denominator. *b*: Unlike Dan2018 or
   Sivyer2013, both of which were formulated for deterministic drivers, this mechanism is
   specifically a stochastic-release artefact that did not arise in t0029 where the t0022 E-I driver
   is deterministic. *c*: Supporting data: the observed null-Hz pattern (0.7, 0.7, 0.7, 0.7, 1.0,
   0.7, 1.0) does show a weak positive trend at long L; the vector-sum DSI declining monotonically
   with R^2 = 0.91 is consistent with smooth envelope attenuation rather than threshold failure.
   *d*: Follow-up — repeat the sweep at rho=0.0 (uncorrelated AR(2)) and rho=0.9; if the decrease
   flattens or inverts when rho changes, the effect is release-noise-mediated.

6. **Two-regime transition with length-dependent switch point**. *a*: Schachter2010 reports a ~4x
   DSI amplification that kicks in only once local Na/Ca spikes clear threshold; Sivyer2013 and
   Dan2018 each assume a single dominant regime. If a length sweep spans both a passive-cable regime
   (dominant at short L) and a dendritic-spike regime (dominant at intermediate L), the switch point
   could be anywhere in 1.0x-1.75x and a single trial-count may be insufficient to resolve which
   regime each multiplier sits in, producing a ragged curve. *b*: Unlike either baseline hypothesis,
   this is a regime-mixture story with per-multiplier and per-trial variability. *c*: Supporting
   data: the primary DSI bounce from 0.62 at 1.5x to 0.72 at 1.75x is hard to explain with any
   monotonic passive mechanism but natural if both multipliers straddle the spike-initiation
   threshold. *d*: Follow-up — increase trials-per-angle from 10 to 40 at 1.5x and 1.75x; if the
   per-trial DSI bimodal distribution collapses to a single mode, confirm regime-mixture.

7. **NMDA recruitment on longer distal branches**. *a*: The de Rosenroll 2026 DSGC model
   (`10.1016_j.celrep.2025.116833`, the t0024 substrate) and PolegPolsky2026 both show NMDA-mediated
   multiplicative gain as a morphology-coupled mechanism that can independently drive DSI > 0.5.
   Longer distal branches include more NMDA-rich terminal synapses whose voltage-dependent Mg2+
   block reshapes preferred-direction recruitment — possibly non-monotonically if Mg2+ unblock
   saturates past a length where the distal membrane stays depolarised long enough to recruit NMDA
   but short enough not to inactivate it. *b*: Unlike Dan2018 (linear TR weighting) this is a
   multiplicative, voltage-dependent gain that can amplify OR suppress DSI depending on where the
   dendrite sits in the Mg2+ unblock curve. *c*: Supporting data: the t0024 ACh synapse is NMDA- and
   AMPA-mixed (standard ModelDB convention); the Mg2+-unblock peak is around -40 mV and
   `mean_peak_mv` sits in a 28-32 mV range consistent with near-peak unblock. *d*: Follow-up — set
   the NMDA fraction at ACh synapses to 0 and 1 in two mini-sweeps and compare DSI trajectories; a
   flat or inverted curve at NMDA=0 would confirm NMDA drives the non-monotonicity.

## Recommendation

The highest-value alternatives are **(1) passive cable filtering past an optimal electrotonic
length** and **(4) local distal spike failure at extreme lengths**, with **(5) stochastic-release
smoothing** as a control that must be ruled in or out before either is credible. Alternative (1) has
the strongest literature grounding (Tukker2004 and Hausselt2007 both document intermediate
electrotonic-length optima) and is the most parsimonious explanation for a non-monotonic curve with
a clean peak-firing decline. Alternative (4) uniquely explains the preferred-direction angle jumps
at 1.5x (330 deg) and 2.0x (30 deg), which a smooth cable-filter effect cannot produce.

The single most informative follow-up task is a **2D length x diameter sweep**: fix the distal
length multiplier at 0.5x, 1.0x, and 2.0x and cross it with a distal-diameter multiplier at 0.5x,
1.0x, and 2.0x (9-point grid, ~21 trials/point to tighten the CIs at 1.5x-equivalent regime
boundaries). This maps the electrotonic plane at minimal cost (~9 x 2.8 h / 7 = ~3.6 h), directly
tests alternative (1), and falsifies or confirms alternative (4) by measuring whether DSI recovers
when diameter compensates for length. If resources permit, a parallel rho sweep (rho = 0.0, 0.6, 0.9
at the baseline morphology) disambiguates alternative (5) cheaply.

## Limitations

* **Not considered: GABA kinetic timescale and SAC-plexus anatomy.** t0034 varies a single
  morphology parameter on the postsynaptic DSGC; the presynaptic SAC inhibitory timing is fixed by
  t0024's `_gaba_prob_for_direction` schedule. Morrie2018 and Kim2014 show plexus and timing matter
  first-order; that axis is out of scope.
* **Not considered: morphology changes other than distal-leaf `sec.L`.** Non-terminal branch
  lengths, diameters, and branch count are held fixed. Tukker2004 and Wu2023 both show these matter
  independently.
* **Not considered: channel-density covariance.** Scaling `sec.L` scales total membrane area of
  distal leaves but does not renormalise per-area channel conductance. A length-change-with-fixed-
  density sweep conflates "more distal cable" with "more distal channels"; a follow-up could
  normalise channel density per um.
* **Not considered: effect of trial count.** 10 trials per angle is the t0026 convention but at the
  extremes of the DSI range (0.55-0.77) the 95% CI on a 10-trial DSI is ~+/-0.1 — comparable to
  the slope itself. No bootstrap CI is reported in `metrics_per_length.csv`. A CI-aware re-analysis
  is deferred.
* **Not considered: non-retinal DSGC mechanisms (cortical V1, fly T4).** Anderson1999 and
  Gruntman2018 are corpus nulls for dendritic-asymmetry DS; they apply to those preparations rather
  than to the mammalian DSGC simulated here.
* **Not considered: heterogeneous distal sections.** All distal leaves are scaled by the same
  multiplier; in biology, different branches have different baseline `sec.L`. A selective
  long-branch-only sweep could localise the dominant effect.
