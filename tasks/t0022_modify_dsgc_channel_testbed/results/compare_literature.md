---
spec_version: "1"
task_id: "t0022_modify_dsgc_channel_testbed"
date_compared: "2026-04-21"
---
# Comparison with Published DSGC Literature

## Summary

Our per-dendrite E-I scheduling port of ModelDB 189347 produces **DSI 1.0** and a **15 Hz** peak
firing rate over a 12-angle x 10-trial moving-bar sweep, with null-half-plane firing collapsed to
**0 Hz**. The DSI is at or above the upper end of the published DSGC envelope (0.5-0.8 in
Poleg-Polsky & Diamond 2016, Oesch2005, Park2014), while the peak firing rate lands **below** the
published band (**20-80 Hz**). Of the three sibling ports of Poleg-Polsky & Diamond 2016 ModelDB
189347 in this project, t0022 is the first to place direction selectivity inside the DSGC dendrites
via spatiotemporally asymmetric inhibition as Taylor2000 and Park2014 report it experimentally,
rather than through the t0008 per-angle BIP rotation or the t0020 global gabaMOD scalar swap.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Poleg-Polsky & Diamond 2016 (ModelDB 189347 source) | DSI | 0.80 | 1.00 | +0.20 | Our DSI exceeds; we clip null to 0 Hz while the paper retains low non-zero null firing |
| Poleg-Polsky & Diamond 2016 (ModelDB 189347 source) | Peak rate (Hz) | 35.0 | 15.0 | -20.0 | Mid-point of paper's ~30-40 Hz band; peak gap inherited from t0008 HHst density |
| Poleg-Polsky & Diamond 2016 (ModelDB 189347 source) | Null rate (Hz) | 2.0 | 0.0 | -2.0 | Deterministic NetStim driver; no bg activity to keep null > 0 |
| Oesch2005 (rabbit DSGC, in vivo / in vitro) | Spike DSI | 0.70 | 1.00 | +0.30 | Paper reports 0.67-0.74 DSI band at spike level; we exceed upper bound |
| Oesch2005 (rabbit DSGC) | Peak rate (Hz) | 30.0 | 15.0 | -15.0 | Paper band 20-40 Hz for moving-bar PD; we land below |
| Park2014 (mouse ON-OFF DSGC) | Spike DSI | 0.65 | 1.00 | +0.35 | Paper reports DSI 0.65 +/- 0.05; we exceed 0.70 upper bound |
| Park2014 (mouse ON-OFF DSGC) | Null/pref I ratio | 4.0 | 4.0 | +0.0 | Our GABA_NULL/GABA_PREF = 12.0 nS / 3.0 nS = 4.0x, mid-range of paper's 2-4x anchor |
| Park2014 (mouse ON-OFF DSGC) | PD E conductance (nS) | 0.31 | 6.00 | +5.69 | We use 6 nS per-dendrite AMPA; paper reports 0.31 nS whole-cell at soma (space-clamp attenuated) |
| Sivyer2013 (DSGC patch-clamp) | Peak rate (Hz) | 115.0 | 15.0 | -100.0 | Paper band 80-150 Hz over 1-2 s bar; our single-bar steady drive sits far below |
| Schachter2010 (rabbit DSGC compartmental model) | PSP-to-spike DSI amplification | 4.0 | ~7.0 | +3.0 | Paper reports ~4-6x threshold amplification from PSP DSI 0.1 to spike DSI 0.7; we saturate via full null suppression |

## Methodology Differences

* **Bar stimulus and geometry.** We drive a single moving bar at a fixed velocity and synthesise
  per-dendrite bar-arrival times analytically from each section's midpoint coordinate rather than
  simulating bipolar-cell activation on a retina-space grid. Poleg-Polsky & Diamond 2016 and
  Taylor2000 use a moving bar rendered by the upstream BIP layer; Oesch2005 and Park2014 record from
  live retinas responding to a real projected bar. Our analytic scheduling is a simplification —
  it ignores spatial RF structure and the SAC feedforward pathway that shapes inhibition in vivo.
* **Baseline synapse silencing.** We set `h.b2gampa = h.b2gnmada = h.s2ggaba = h.s2gach = 0` and
  re-run `update()` + `placeBIP()` so that only the per-dendrite E-I pairs fire. Poleg-Polsky &
  Diamond 2016 retains the full bipolar / amacrine drive. This cleaner baseline is the main reason
  our null rate collapses to **0 Hz** while the paper retains ~2 Hz of null-direction firing.
* **E-I scheduling mechanism.** We implement a hard per-half-plane switch: if
  `|angle_offset| < 90 deg`, excitation leads inhibition by **+10 ms** with GABA at **3 nS**; if
  `|angle_offset| >= 90 deg`, inhibition leads excitation by **10 ms** with GABA at **12 nS** (4x
  null/preferred ratio). Park2014 reports a continuous cosine-like direction tuning of inhibition
  rather than a half-plane step; real DSGCs additionally have direction-tuned presynaptic E input
  (Fried2002, Taylor2003) layered onto the SAC-driven I asymmetry, which we do not model.
* **Per-dendrite conductance magnitudes.** We use **6 nS** AMPA and **3-12 nS** GABA per dendritic
  subunit. Park2014 reports **0.31 nS E** and **2.43 nS I** measured at the soma by whole-cell
  voltage clamp at the DSI ~0.65 working point; these somatic values are space-clamp-attenuated
  estimates of dendritic conductance (Schachter2010 reports 40-100% attenuation), so our
  per-dendrite values are not directly comparable to the paper's somatic numbers, but are consistent
  with the paper's 2-4x null/preferred ratio.
* **Trial-to-trial variability.** Our `NetStim` burst driver uses `noise = 0` and the upstream BIP
  RNG is bypassed by the silencing step, so per-angle std is exactly **0 Hz** and reliability is
  **1.0** at every angle. Real DSGCs and the full Poleg-Polsky & Diamond 2016 simulation have
  stochastic transmitter release and bipolar spike jitter producing ~2-5 Hz per-trial variability.
* **Spike-initiation apparatus.** We inherit the t0008 HHst Na/K density set from the ModelDB
  source; no axon, no distal AIS Nav1.6 / Kv1.2 block, no proximal AIS Nav1.1 block per VanWart2006.
  This caps sustained firing in the 10-20 Hz range and is the intended target for the Nav1.6 and Kv3
  channel-swap follow-up tasks that the t0022 `forsec` partition exists to support.

## Analysis

**Why does our DSI saturate at 1.0?** Three forces combine to push DSI above the 0.5-0.8 published
band. First, baseline synapse silencing strips out the bipolar/amacrine drive that keeps null firing
non-zero in both the paper and in vivo recordings — our cell only hears the per-dendrite E-I
pairs, so the null-direction shunt has no background firing to partially escape. Second, the
per-dendrite GABA conductance in the null direction is **12 nS**, which is 2x the ~6 nS that
Schachter2010 identifies as sufficient to gate dendritic spike initiation. Combined with the **-10
ms** I-before-E offset, this produces a reliable veto on every subunit at every trial. Third, the
E-I scheduling is deterministic across trials (`noise = 0`), so there is no single-trial failure
mode that would allow occasional null-direction spikes. The result is clean mechanism verification
(DSI 1.0 >= 0.5 with zero ambiguity) but loses the graded shape that real DSGCs exhibit.

**Why is the peak firing rate at 15 Hz rather than 30-80 Hz?** The gap is attributable to three
known factors. First, the spike-generation machinery. We inherit the t0008 HHst Na/K density set
unchanged, which produces peak rates in the 10-20 Hz band for sustained synaptic drive regardless of
stimulus mechanism — t0008 (rotation-proxy DSI 0.316) peaks at 18.1 Hz, t0020 (gabaMOD-swap DSI
0.7838) peaks at 14.85 Hz, and t0022 at 15 Hz confirms this is mechanism-independent. The fix is the
Nav1.6 distal-AIS + Kv3 distal-AIS channel swap supported by VanWart2006 and KoleLetzkus2007, which
is explicitly out of scope for this testbed task. Second, our stimulus is a single pass of a moving
bar rather than the multi-second drifting stimulus used in Sivyer2013 (80-150 Hz peak over 1-2 s);
the per-trial integration window is shorter and contains fewer bursts. Third, our per-dendrite AMPA
conductance of **6 nS** and burst count of **6 events** deliver modest charge compared to the full
SAC-to-DSGC synaptic complement; we do not model the NMDA-mediated gain boost (Lester1990, Jain2020)
that amplifies preferred-direction firing in real DSGCs.

**Where t0022 sits relative to the other two ports in this project.** The three sibling ports
represent three distinct implementations of direction selectivity on the same ModelDB 189347
skeleton, and their rank on the literature envelope is informative. t0008 (per-angle BIP coordinate
rotation, **DSI 0.316**) falls **below** the published DSI envelope because rotating the upstream
BIP array does not produce true spatiotemporally asymmetric inhibition — the DSGC still integrates
the same bipolar pattern at every angle and the DSI comes only from morphology-induced rate
variation. t0020 (global `h.gabaMOD` scalar swap between PD=0.33 and ND=0.99, **DSI 0.7838**)
**matches** the published envelope numerically but is mechanistically a parameter toggle with no
angle axis and no dendritic localisation; it cannot serve as a channel-density testbed because no
part of the cell sees direction-specific synaptic timing. t0022 (per-dendrite E-I scheduling, **DSI
1.000**) is the first port to place direction selectivity inside the DSGC dendrites through
spatiotemporally asymmetric inhibition, which is the mechanism Taylor2000 and Oesch2005 establish
experimentally and which Park2014 and Schachter2010 quantify. The **+0.20** DSI delta above
Poleg-Polsky & Diamond 2016 is a byproduct of the cleaner baseline rather than a mechanism error,
and the **-20 Hz** peak gap is shared with t0008 and t0020 and localised to the spike-generation
machinery — which is precisely what the 5-region `forsec` partition exists to fix in follow-up
tasks.

## Limitations

* **No direct replication of the Poleg-Polsky & Diamond 2016 Figure-level tuning curves.** We
  compare against the paper's headline DSI and peak-rate envelope rather than against per-angle
  tuning curves, because the paper reports tuning curves only for representative cells rather than a
  tabulated dataset. The +0.20 DSI delta cannot be attributed to a specific figure row.
* **Per-dendrite conductance values are not directly comparable to Park2014 somatic measurements.**
  Park2014 reports 0.31 nS E and 2.43 nS I measured at the soma under voltage clamp, which
  Schachter2010 notes are space-clamp-attenuated by 40-100% relative to the dendritic source. Our 6
  nS per-dendrite AMPA is a forward-model choice informed by Schachter2010 but is not itself a
  number the paper reports; the comparison table row flags this in the Notes column.
* **Sivyer2013 80-150 Hz peak rate is not a valid comparison target for this task.** The paper
  reports peak rates over 1-2 s bar stimuli with the full synaptic complement intact; our 1000 ms
  run window with baseline synapses silenced cannot reach that range. The comparison row is included
  for completeness but the **-100 Hz** delta is not a mechanism failure.
* **No HWHM comparison in the main table.** The corpus does not tabulate a single agreed HWHM number
  for DSGC tuning curves — individual cells in Oesch2005, Park2014, and Taylor2000 span 30-60 deg,
  but no single number is reproducible across papers. Our HWHM of **116.25 deg** is broader than
  this range because the half-plane step rule lights up 5 of 12 angles uniformly rather than
  producing a narrow peak, which is discussed in `results_detailed.md` `## Limitations`.
* **No SAC-feedforward model.** Real DSGC direction selectivity is built on top of SAC dendritic
  direction tuning (Euler-Detwiler-Denk 2002) which shapes the inhibition profile; our driver
  schedules GABA directly without modeling the SAC layer. This is an intentional simplification for
  the testbed role and is documented in the library `description.md`.
* **No velocity sweep.** DSGC DSI and peak rate depend on bar velocity (Taylor2000 discusses but
  does not tabulate a full curve); we fix velocity at the t0008 baseline. Comparison rows from
  papers that report velocity-dependent numbers (Oesch2005, Sivyer2013) are taken at their stated
  peak-velocity condition, which may not match our velocity exactly.
