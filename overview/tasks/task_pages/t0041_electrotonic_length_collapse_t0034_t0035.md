# ⏹ Electrotonic-length collapse analysis of t0034 and t0035

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0041_electrotonic_length_collapse_t0034_t0035` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source suggestion** | `S-0035-01` |
| **Task types** | `data-analysis`, `answer-question` |
| **Expected assets** | 1 answer |
| **Task folder** | [`t0041_electrotonic_length_collapse_t0034_t0035/`](../../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/task_description.md)*

# Electrotonic-Length Collapse Analysis of t0034 and t0035

## Source Suggestion

S-0035-01 (zero-cost L/lambda collapse analysis of t0034 length and t0035 diameter data).

## Motivation

t0034 (distal-length sweep on t0024) and t0035 (distal-diameter sweep on t0024) together
establish a ~25–30x asymmetry in DSI sensitivity: length slope -0.126 (p=0.038) vs diameter
slope +0.004 (p=0.88). Cable theory predicts this asymmetry because electrotonic length scales
as L / sqrt(d * Rm / (4 * Ra)) — linearly in raw length, but as 1/sqrt(d) in raw diameter. If
the cable-theory prediction is tight, primary DSI from both sweeps should collapse onto a
single DSI-vs-L/lambda curve.

Confirming the collapse would allow the t0033 morphology + channel optimiser to parameterise
morphology in 1-D (electrotonic length) rather than 2-D (raw length × raw diameter),
eliminating diameter as a spurious degree of freedom and reducing the search-space size.

## Objective

For every (length multiplier, diameter multiplier) operating point in the combined t0034 ∪
t0035 dataset, compute the electrotonic length L/lambda of the swept distal section using the
t0024 baseline biophysics (Rm, Ra from the Poleg-Polsky-2016 parameter backbone). Plot primary
DSI and vector-sum DSI vs L/lambda for both sweeps on the same axes. Test whether the two
sweeps collapse onto one curve with Pearson r > 0.9, and report the residual variance
attributable to non-cable effects.

## Scope

* Zero simulation cost. No NEURON invocations. Pure post-hoc analysis on the existing t0034
  and t0035 trial-level CSV outputs.
* Use only the primary-DSI and vector-sum-DSI per-trial outputs; do not re-derive quantities
  from raw spike trains.
* Input data: both sweeps' trial-level CSVs in their respective `results/` folders.
* Output: one answer asset documenting the collapse test, one figure showing primary DSI and
  vector-sum DSI on a common L/lambda axis, and a one-paragraph recommendation for the t0033
  parameterisation.

## Deliverables

* `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/` — full answer
  asset per the answer specification.
* `results/images/electrotonic_length_collapse.png` — overlay of both sweeps.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections.
* `results/metrics.json` — at minimum the Pearson r between the two sweeps on the common
  L/lambda axis, the residual RMSE after fitting a single curve, and the recommendation
  verdict (collapse-confirmed / collapse-rejected).

## Out of Scope

* No new simulation runs on any testbed.
* No modifications to t0022, t0024, or the t0033 plan.
* No PDF re-reading of Kim 2014 or Sivyer 2013 (still blocked on paywall access).

## Anticipated Risks

* The distal section in t0024 may not have a single uniform (Rm, Ra); if it does not, compute
  a section-weighted average L/lambda and report the approximation in the results.
* If collapse is weak (Pearson r < 0.7), state this explicitly as a negative result and
  enumerate the non-cable effects (spike failure at extremes, AR(2) noise correlation) that
  the collapse model misses.

</details>
