# Schachter 2010 Re-Test on t0043 Substrate

## Status: BLOCKED (2026-04-24)

Blocked pending completion of **t0046_reproduce_poleg_polsky_2016_exact** and of this task's
upstream dependency **t0043** (which is itself blocked on t0046). This task depends on the t0043
substrate. Reassess after t0046 merges and t0043's block is reviewed.

## Source Suggestion

S-0002-02 (paired active-vs-passive dendrite experiment to reproduce Schachter 2010 DSI gain ~0.3 ->
~0.7).

## Motivation

Three independent diameter sweeps across two testbeds have failed to show Schachter 2010's predicted
active-amplification signature:

* t0030 on t0022 at GABA = 12 nS: slope +0.008 (p=0.177), DSI pinned at 1.000 (deterministic
  schedule saturates the metric).
* t0035 on t0024 (AR(2) stochastic) at paper-default GABA: slope +0.004 (p=0.88), flat.
* t0039 on t0022 at GABA = 4 nS (t0037 sweet spot): slope -0.034 (p=0.008), monotonic decline
  consistent with passive filtering rather than the predicted concave-down interior peak.

One candidate explanation, surfaced in brainstorm session 8's cross-task audit, is that lumped HHst
lacks the distal Nav1.6 and Kv3 channels needed to recruit the regenerative threshold-crossing
regime Schachter 2010 relies on. t0043 fixes that inventory and restores NMDA. If Schachter 2010 is
correct and our previous null results were confounded by the channel gap, the same 7-diameter sweep
on the t0043 substrate should show a concave-down DSI-vs-diameter curve with a significant negative
quadratic coefficient.

If the curve is still monotonic after t0043, we can close the Schachter 2010 hypothesis on the
Poleg-Polsky-derived morphology and commit to a passive-filtering framing for the t0033 optimiser.

## Objective

Run a 7-diameter distal-section sweep (multipliers 0.5, 0.67, 0.85, 1.0, 1.2, 1.5, 2.0 — same grid
as t0030, t0039, t0035) on the t0043 library asset at GABA = 4 nS. Protocol matches t0039: 12
directions x 10 trials per direction per multiplier, V_rest = -60 mV. Primary outcome is the
DSI-vs-diameter curve shape; fit both linear and quadratic models and report the coefficients with
p-values.

Pass criterion (Schachter 2010 signature recovered):

* Quadratic fit coefficient significantly negative (p < 0.05) with a peak at an interior multiplier
  (between 0.6 and 1.5).

Fail criterion (Schachter hypothesis rejected on Poleg-Polsky morphology):

* Monotonic (linear fit significant, quadratic not significant), or no significant trend. In this
  case, emit a suggestion to formally close S-0002-02 and to add a clarifying note to the t0033 plan
  recommending the passive-filtering framing.

## Scope

* Local CPU only. No remote compute. ~8 hours wall-clock.
* Use the t0043 library asset. Do not modify the channel inventory; this is a pure morphology sweep.
* Keep per-trial stochasticity identical to t0039 so the results are directly comparable.

## Out of Scope

* Nav ablation (covered by S-0029-02, currently medium priority).
* Length-axis sweep on the t0043 substrate (possible follow-up, not this task).
* Re-running on t0024 (possible follow-up under S-0039-01).

## Deliverables

* 7-diameter tuning-curve CSVs under `results/`.
* Overlay plot of DSI-vs-diameter with linear and quadratic fits under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections and an
  explicit Schachter-recovered / Schachter-rejected verdict.
* `results/metrics.json` with the linear slope, quadratic coefficient, and their p-values, plus
  primary DSI, vector-sum DSI, and peak Hz at each multiplier.
* `results/compare_literature.md` explicitly comparing the recovered (or absent) curvature against
  Schachter 2010 and the passive-filtering prediction.

## Anticipated Risks

* If t0043 fails its own Pass criterion (peak rate or DSI preservation), do not proceed with this
  task; the substrate is not fit for use.
* Adding Nav1.6 may change the effective preferred direction; re-seed the E-I schedule only if the
  preferred direction has shifted by more than 30 deg from the t0037 40.8 deg anchor.
* Quadratic fits on 7 points are under-powered if noise is high; if the quadratic p-value is
  borderline (0.05 < p < 0.15), emit a suggestion for a denser 11-point sweep rather than declaring
  a verdict.
