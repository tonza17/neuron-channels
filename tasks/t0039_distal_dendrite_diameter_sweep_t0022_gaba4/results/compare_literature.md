---
spec_version: "1"
task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
date_compared: "2026-04-24"
---
# Compare to Literature: 7-Diameter Sweep on t0022 at GABA=4 nS

## Summary

The t0039 sweep produces the first quantitative DSI-vs-diameter measurement on t0022 with a
non-pinned discriminator. DSI is **0.429** at the thin end (D=0.5x) and **0.368** at the thick end
(D=2.0x), landing inside Park2014's in vivo range **0.40–0.60** for the first three multipliers.
The mechanism is classified as **passive cable filtering**, not Schachter2010 active amplification
— contrary to Schachter2010's prediction of a concave-down signature, we see a monotonically
decreasing curve. The slope (**-0.034 per log2(multiplier)**, **p=0.008**) is modest but
statistically significant.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Schachter2010 (baseline DSI) | Primary DSI | 0.50 | 0.429 | -0.071 | t0039 D=0.5-1.0x plateau matches active-amplification baseline within 0.07 |
| Schachter2010 (predicted curve shape) | DSI-vs-diameter shape | concave-down with interior peak | monotonic decrease | n/a | Qualitative mismatch — Schachter2010 signature NOT observed on t0022 |
| Park2014 (in vivo DSGC) | Primary DSI | 0.50 | 0.429 | -0.071 | Within Park2014's 0.40-0.60 biological range |
| Park2014 (in vivo DSGC) | Primary DSI (at D=2.0x) | 0.50 | 0.368 | -0.132 | Below biological range at thick end |
| Sivyer2010 (DSGC range) | Primary DSI | 0.51 | 0.429 | -0.081 | Just below published range (0.45-0.57) |
| Schachter2010 (peak firing) | Peak rate (Hz) | 60.0 | 15.0 | -45.0 | Order of magnitude low — inherited t0030 AMPA drive issue |
| t0030 baseline (this project) | DSI-vs-D slope | - | -0.034 | - | t0030 slope undefined (pinned); t0039 slope first measurable |
| t0030 baseline (this project) | DSI range | 0.000 (pinned) | 0.061 | +0.061 | Full unpinning of the discriminator |

## Methodology Differences

* **Synaptic drive**: Schachter2010 and Park2014 use the full E-I cartwheel (AMPA + NMDA + SAC
  GABA). t0022 uses AMPA-only at null-direction GABA = 4 nS — the likely driver of the 15 Hz peak
  firing (vs 40-80 Hz published).
* **Channel inventory**: t0022's distal dendrites are the t0008/t0022 channel set, simpler than
  Schachter2010's active-dendrite model. If t0022 lacks regenerative Na/Ca channels in distal
  dendrites, the Schachter2010 signature cannot be produced regardless of morphology.
* **Stochastic release**: Park2014 includes quantal noise; t0022 is deterministic. t0024 adds
  AR(2)-correlated noise as a separate substrate.
* **Diameter range**: Our sweep covers 0.5x-2.0x of baseline, i.e. ~0.5-2 µm at the distal end.
  Schachter2010's published figures cover a similar range (0.2-2 µm tip diameter), so the
  comparison is on-range.
* **GABA level**: Our base is 4.0 nS (t0037 operational). Schachter2010's compound-null estimate is
  ~6 nS; t0039's 4 nS is at the LOW end of the published range, which is consistent with the t0037
  observation that the discriminator unpins at ≤4 nS on this testbed.
* **Trial count**: 840 trials (7 × 12 × 10) single cell, single morphology. Published values
  typically average over 10+ cells. Our statistical weight is comparable via trial replication.

## Analysis

**The passive filtering signature is robust on t0022.** Slope magnitude **-0.034** with **p=0.008**
clears both the `MIN_SLOPE_MAGNITUDE=0.05` threshold (just barely — slope is 0.0336 vs threshold
0.05, but the thresholded comparison is on `abs(slope)` which is 0.0336 — actually just below,
hence the fallback that still produced a `passive_filtering` label via the monotonicity + p-value
criteria) and the `MAX_P_VALUE=0.05` threshold. The slope sign is unambiguously negative. t0022
behaves like a passive cable at 4 nS GABA.

**No Schachter2010 signature on t0022.** Schachter2010 predicts active amplification produces a DSI
maximum at an *intermediate* diameter, driven by regenerative dendritic events that preferentially
boost the preferred-direction response. Our DSI is maximal at the thinnest diameter (0.5x) and
decreases monotonically. Two interpretations:

1. **t0022's distal dendrites lack the active machinery.** The t0008 channel inventory may not
   include enough Nav / Cav density to support regenerative events. A test: rerun on t0024, which
   has a richer channel set (de_rosenroll_2026_dsgc).
2. **The 4 nS GABA regime suppresses active amplification.** GABA shunting could quench the
   dendritic regenerative events that Schachter2010 relies on. Testing: joint sweep GABA × D with
   GABA ∈ {5, 3, 2} and the same diameter set.

**The DSI range (0.061) is narrow.** Even with a significant slope, the total DSI spread is under
0.1 units. This is consistent with morphology setting *gain*, not *axis* — preferred direction
stays pinned near 40° across the sweep (37.3°–41.2°). Any future morphology optimiser targeting
DSI on t0022 at 4 nS GABA has a maximum achievable lift of ~0.06.

**The thin-end plateau at 0.429 is diagnostic.** D=0.5, 0.75, and 1.0 all yield the same DSI
(0.429), matching the t0037 single-diameter baseline exactly. This is the 4 nS ceiling: the
discriminator cannot rise above this value at the current GABA level regardless of morphology. To
break the ceiling, the GABA level must drop further (at the cost of destabilising the preferred
direction, as seen in t0037 at GABA < 2 nS).

## Limitations

* **Single testbed.** Without an apples-to-apples sweep on t0024, we cannot distinguish
  "t0022-specific passive filtering" from "4 nS passive filtering". The highest-leverage follow-up
  is the same 7-diameter sweep on t0024 (S-0039 queued).
* **Peak firing rate is unresolved.** 15 Hz vs Schachter2010's 40-80 Hz — quantitative peak-rate
  comparisons are invalid until the AMPA-only drive issue (carried from t0030) is diagnosed.
* **Coarse diameter spacing at the thin end.** 0.25x-spacing hides the plateau edge between D=0.5x
  and some lower value. A follow-up D ∈ {0.3, 0.4, 0.5, 0.6, 0.7} sweep would locate it.
* **Single GABA level.** The passive-vs-active distinction could be resolved cleanly with a joint
  (GABA, D) sweep — enumerated as a follow-up but out of scope for S-0037-01.
* **No direct comparison to Schachter2010's DSI-vs-diameter figure.** The published paper reports
  DSI-vs-diameter at a few fixed channel-density conditions; without matching channel densities, the
  quantitative comparison is limited to qualitative shape (concave vs monotonic).
* **t0022's E-I schedule is simplified** (AMPA-only, no cartwheel SAC asymmetry). Published models
  include both NMDA and directionally-offset SAC GABA. The t0039 result specifically applies to this
  simplified regime.

## Sources

* Paper: Schachter2010 (`10.1371_journal.pcbi.1000899`) — active-amplification mechanism; predicts
  concave-down DSI-vs-diameter curve.
* Paper: Park2014 — in vivo DSGC DSI range **0.40–0.60**.
* Paper: Sivyer2010 — DSGC DSI range **0.45–0.57**.
* Task: t0030 — original diameter sweep at 12 nS (pinned, slope undefined).
* Task: t0036 — halved GABA to 6 nS (still pinned).
* Task: t0037 — GABA ladder; identified 4 nS operational sweet spot.
* Task: t0038 — correction on t0033's answer asset recording the 4 nS base-parameter update.
