# ⚠️ Fine-grained null-GABA ladder (3.5, 3.0, 2.5 nS) on t0022

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0042_fine_grained_null_gaba_ladder_t0022` |
| **Status** | ⚠️ intervention_blocked |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Task types** | `experiment-run` |
| **Task folder** | [`t0042_fine_grained_null_gaba_ladder_t0022/`](../../../tasks/t0042_fine_grained_null_gaba_ladder_t0022/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0042_fine_grained_null_gaba_ladder_t0022/task_description.md)*

# Fine-Grained Null-GABA Ladder on t0022

## Status: BLOCKED (2026-04-24)

Blocked pending completion of **t0046_reproduce_poleg_polsky_2016_exact**. The researcher has
paused all t0022-substrate modification tasks until the faithful ModelDB 189347 reproduction
establishes whether the observed DSI and peak-rate values in t0022 reflect genuine mechanism
gaps (justifying this task) or accumulated deviations from Poleg-Polsky 2016 (making this
task's target irrelevant). Reassess after t0046 merges.

## Motivation

t0037 swept null-GABA at {0, 0.5, 1, 2, 4} nS on t0022 and identified a sweet spot at 4 nS
(primary DSI 0.429, preferred direction 40.8 deg, matching Park 2014's in vivo band
0.40–0.60). Below 2 nS the cell over-excites and preferred direction randomises. t0039 then
showed that at GABA = 4 nS the t0022 diameter axis produces a monotonic DSI decline (slope
-0.034, p=0.008) — passive-filtering rather than Schachter 2010 active amplification.

What t0037 did not probe is the interval between 2 and 4 nS. Brainstorm session 8 requested a
fine-grained ladder at {3.5, 3.0, 2.5} nS to answer: does t0022 admit a GABA level below 4 nS
where DSI exceeds 0.5 without destabilising preferred direction? This directly informs whether
t0022 is usable as an optimisation substrate above its current 0.429 ceiling.

## Objective

Run the t0037 protocol (12 directions × 10 trials per direction, baseline diameter, V_rest =
-60 mV) at three additional null-GABA levels: 3.5 nS, 3.0 nS, 2.5 nS. Report primary DSI,
vector-sum DSI, preferred direction, peak firing rate, and null firing rate at each level.
Compare against t0037's 4 nS and 2 nS anchors.

Pass criterion: at any of the three new levels, primary DSI >= 0.50 AND preferred direction
stability across trials under 10 deg standard deviation. If pass, that GABA level becomes a
candidate new base parameter for t0022 optimisation; emit a suggestion for a follow-up
correction task (analogous to t0038) to propagate the new base into t0033.

Fail criterion: all three new levels yield DSI < 0.50 or preferred-direction standard
deviation
> 10 deg. If fail, report that 4 nS is the effective t0022 ceiling and recommend the t0033 optimiser
> switch substrates to t0024 per S-0034-07.

## Scope

* Local CPU only. No remote compute. ~1 hour total wall-clock.
* Reuse the t0037 trial_runner with only the null-GABA parameter changed; no code changes to
  the testbed.
* Produce tuning curves (Cartesian and polar) at each GABA level.

## Out of Scope

* Morphology sweeps (covered by t0039 at 4 nS).
* Channel-inventory modifications (covered by t0043).
* Schachter re-test (covered by t0044).

## Deliverables

* Per-GABA-level tuning-curve CSV + polar plot under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections,
  explicit Pass/Fail verdict against the criterion above.
* `results/metrics.json` with primary DSI, vector-sum DSI, preferred direction (mean and sd),
  peak Hz, and null Hz at each of the three new GABA levels, plus the two t0037 anchors.
* If Pass: one new suggestion in `results/suggestions.json` proposing a correction task to set
  the new GABA base value in t0033.

## Anticipated Risks

* Narrow sampling (three points) may miss a non-monotonic optimum between 2 and 4 nS; if
  results look non-monotonic, emit a follow-up suggestion for a denser sweep rather than
  extrapolating.
* If the cell destabilises at 2.5 nS or 3.0 nS, record the destabilisation metrics (preferred
  direction sd, coefficient of variation of peak rate) rather than treating those runs as
  failures.

</details>
