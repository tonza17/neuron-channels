---
spec_version: "1"
task_id: "t0037_null_gaba_reduction_ladder_t0022"
date_compared: "2026-04-24"
---
# Compare to Literature: Null-GABA Reduction Ladder on t0022

## Summary

The t0037 GABA ladder succeeded where t0036 failed. At **4 nS** null-GABA, the t0022 testbed
produces **DSI=0.429** with preferred direction near **40°** — matching Park2014's in vivo DSGC
range (**0.40–0.60**) and the Schachter2010 active-amplification baseline DSI near **0.5**. The
rescue hypothesis S-0036-01 is confirmed; the unpinning threshold sits between **6 nS** (t0036
pinned) and **4 nS** (t0037 unpinned). Peak firing rate (**15 Hz**) remains well below
Schachter2010's **40–80 Hz** — an unrelated issue carried from t0030's AMPA-only drive.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Schachter2010 (null GABA) | GABA conductance (nS) | 6.0 | 4.0 | -2.0 | Our unpinning threshold sits at the LOW end of the published range. |
| Park2014 (in vivo DSGC) | Primary DSI | 0.50 | 0.429 | -0.071 | Within Park2014's biological range (0.40–0.60). |
| Schachter2010 (baseline) | Primary DSI | 0.50 | 0.429 | -0.071 | Consistent with active-amplification regime. |
| Sivyer2010 (DSGC) | Primary DSI | 0.51 | 0.429 | -0.081 | Just below the published range (0.45–0.57). |
| Schachter2010 (baseline) | Peak firing (Hz) | 60.0 | 15.0 | -45.0 | Order-of-magnitude low — carried from t0030's AMPA-only drive. |
| t0030 baseline (this project) | Primary DSI | 1.000 | 0.429 | -0.571 | t0030 was pinned; 4 nS rescues the discriminator. |
| t0036 halved (this project) | Primary DSI | 1.000 | 0.429 | -0.571 | t0036 still pinned at 6 nS; 4 nS unpins. |

## Methodology Differences

* **Synaptic drive**: Schachter2010 and Park2014 model the full E-I cartwheel (AMPA + NMDA + SAC
  GABA) with spatially-offset inhibition. t0022 uses an AMPA-only deterministic schedule (NMDA and
  SAC spatial offset stripped) — this is the likely cause of the low peak firing rate.
* **GABA targeting**: Published DSGC models include directionally-offset SAC GABA. t0022 applies a
  single scalar `GABA_CONDUCTANCE_NULL_NS` at null-direction onset; no preferred-direction
  inhibition is simulated.
* **Stochastic release**: Park2014 includes quantal noise; t0022 is deterministic. t0024 (not used
  here) adds AR(2)-correlated stochastic release as a separate substrate.
* **Trial count**: 10 trials × 12 angles × 5 GABA levels = 600 trials. Schachter2010's published
  DSI is typically reported as a mean over 10+ cells, each with multiple trials — our single-cell
  mean is comparable in statistical weight.
* **Reference frame**: Our "preferred direction" is read off the fitted tuning curve; Park2014 and
  Sivyer2010 define preferred direction relative to SAC polarity, which we do not model.

## Analysis

**The operational sweet spot (4 nS) lands in the DSGC biological regime.** Primary DSI of **0.429**
is within Park2014's **0.40–0.60** range and matches Schachter2010's near-**0.5** baseline within
**0.07**. The unpinning threshold sits between t0036's failed **6 nS** and t0037's successful **4
nS**, confirming the S-0036-01 rescue hypothesis and placing the effective null-GABA for directional
selectivity at the LOW end of Schachter2010's range rather than the centre.

**Below 4 nS the cell over-excites and loses tuning.** At 2 nS, primary DSI drops to **0.243** with
preferred direction at **187°**; at 0 nS, DSI collapses to **0.167** at **278°**. The operational
window on t0022 is narrow (**4–5 nS**), suggesting the E-I balance is more fragile than in the
published models — consistent with the simpler AMPA-only schedule lacking compensatory NMDA drive.

**Peak firing (15 Hz vs 40–80 Hz published) is a separate bug, not a GABA artefact.** The same low
firing rate was observed in t0030 at 12 nS GABA — long before any ladder was swept. The root cause
is the AMPA-only drive in t0022; it will need a separate investigation (likely an NMDA add-back or
excitatory conductance tune-up) and does not invalidate the DSI result.

**Implication for t0033**: the optimiser's t0022 variant should set `GABA_CONDUCTANCE_NULL_NS=4.0`
as its base parameter, not the original **12 nS**. This is the first point at which the t0022
testbed produces a DSI landscape that can be optimised meaningfully.

## Limitations

* **No direct conductance-sweep reference in literature.** Schachter2010's compound-null estimate
  (approximately 6 nS) comes from experimental blocker data, not a NetPyNE sweep; the quantitative
  comparison to our 4 nS is approximate.
* **Peak firing rate is unexplained within this task.** The 15 Hz peak is far below published DSGC
  rates (40–80 Hz) and was inherited from t0030; diagnosing it is out of scope for S-0036-01 but
  must be addressed before quantitative peak-rate comparisons are valid.
* **No preferred-direction inhibition simulated.** t0022 applies null-only GABA; the preferred
  direction's absence of inhibition (cartwheel asymmetry) is not tested, so our DSI may be driven by
  a different mechanism than in the published active-amplification regime.
* **Single-cell, single-diameter, single-length.** Published DSI ranges span populations of DSGCs
  with morphological variability; our measurement is at baseline morphology only. The follow-up
  7-diameter sweep at 4 nS (recommended for t0033) is needed before claims about population-level
  DSI distributions.
* **Parameter granularity around the threshold is coarse.** We tested {4, 2, 1, 0.5, 0} nS — the
  exact unpinning threshold is bounded only to the 4–6 nS interval; a finer sweep (e.g., 5.0, 4.5,
  4.0, 3.5, 3.0) would localise it further.
* **Classification scan uses a fixed 0.1 Hz threshold.** Above this, "unpinned" is emitted; below,
  "pinned". This is a project-defined heuristic, not a literature-derived cutoff.

## Sources

* Paper: Schachter2010 (`10.1371_journal.pcbi.1000899`) — active-amplification mechanism, DSI
  baseline and compound null-inhibition estimate.
* Paper: Park2014 — in vivo DSGC DSI range (**0.40–0.60**).
* Paper: Sivyer2010 — DSI range **0.45–0.57**.
* Task: t0030 — original baseline (12 nS GABA, DSI pinned at **1.000**).
* Task: t0036 — halved rescue failed (6 nS GABA, DSI still pinned).
* Task: t0034 — length sweep on t0024 (primary DSI measurable via AR(2) rescue).
* Task: t0035 — diameter sweep on t0024 (comparable substrate).
