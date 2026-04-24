# ⏹ Tasks: Not Started

5 tasks. ⏹ **5 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0044 — <strong>Schachter 2010 re-test via 7-diameter sweep on t0043 at
GABA = 4 nS</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0044_schachter_retest_on_t0043` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0043_nav16_kv3_nmda_restoration_t0022`](../../../overview/tasks/task_pages/t0043_nav16_kv3_nmda_restoration_t0022.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0002-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Schachter 2010 re-test via 7-diameter sweep on t0043 at GABA = 4 nS](../../../overview/tasks/task_pages/t0044_schachter_retest_on_t0043.md) |
| **Task folder** | [`t0044_schachter_retest_on_t0043/`](../../../tasks/t0044_schachter_retest_on_t0043/) |

# Schachter 2010 Re-Test on t0043 Substrate

## Source Suggestion

S-0002-02 (paired active-vs-passive dendrite experiment to reproduce Schachter 2010 DSI gain
~0.3 -> ~0.7).

## Motivation

Three independent diameter sweeps across two testbeds have failed to show Schachter 2010's
predicted active-amplification signature:

* t0030 on t0022 at GABA = 12 nS: slope +0.008 (p=0.177), DSI pinned at 1.000 (deterministic
  schedule saturates the metric).
* t0035 on t0024 (AR(2) stochastic) at paper-default GABA: slope +0.004 (p=0.88), flat.
* t0039 on t0022 at GABA = 4 nS (t0037 sweet spot): slope -0.034 (p=0.008), monotonic decline
  consistent with passive filtering rather than the predicted concave-down interior peak.

One candidate explanation, surfaced in brainstorm session 8's cross-task audit, is that lumped
HHst lacks the distal Nav1.6 and Kv3 channels needed to recruit the regenerative
threshold-crossing regime Schachter 2010 relies on. t0043 fixes that inventory and restores
NMDA. If Schachter 2010 is correct and our previous null results were confounded by the
channel gap, the same 7-diameter sweep on the t0043 substrate should show a concave-down
DSI-vs-diameter curve with a significant negative quadratic coefficient.

If the curve is still monotonic after t0043, we can close the Schachter 2010 hypothesis on the
Poleg-Polsky-derived morphology and commit to a passive-filtering framing for the t0033
optimiser.

## Objective

Run a 7-diameter distal-section sweep (multipliers 0.5, 0.67, 0.85, 1.0, 1.2, 1.5, 2.0 — same
grid as t0030, t0039, t0035) on the t0043 library asset at GABA = 4 nS. Protocol matches
t0039: 12 directions x 10 trials per direction per multiplier, V_rest = -60 mV. Primary
outcome is the DSI-vs-diameter curve shape; fit both linear and quadratic models and report
the coefficients with p-values.

Pass criterion (Schachter 2010 signature recovered):

* Quadratic fit coefficient significantly negative (p < 0.05) with a peak at an interior
  multiplier (between 0.6 and 1.5).

Fail criterion (Schachter hypothesis rejected on Poleg-Polsky morphology):

* Monotonic (linear fit significant, quadratic not significant), or no significant trend. In
  this case, emit a suggestion to formally close S-0002-02 and to add a clarifying note to the
  t0033 plan recommending the passive-filtering framing.

## Scope

* Local CPU only. No remote compute. ~8 hours wall-clock.
* Use the t0043 library asset. Do not modify the channel inventory; this is a pure morphology
  sweep.
* Keep per-trial stochasticity identical to t0039 so the results are directly comparable.

## Out of Scope

* Nav ablation (covered by S-0029-02, currently medium priority).
* Length-axis sweep on the t0043 substrate (possible follow-up, not this task).
* Re-running on t0024 (possible follow-up under S-0039-01).

## Deliverables

* 7-diameter tuning-curve CSVs under `results/`.
* Overlay plot of DSI-vs-diameter with linear and quadratic fits under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections
  and an explicit Schachter-recovered / Schachter-rejected verdict.
* `results/metrics.json` with the linear slope, quadratic coefficient, and their p-values,
  plus primary DSI, vector-sum DSI, and peak Hz at each multiplier.
* `results/compare_literature.md` explicitly comparing the recovered (or absent) curvature
  against Schachter 2010 and the passive-filtering prediction.

## Anticipated Risks

* If t0043 fails its own Pass criterion (peak rate or DSI preservation), do not proceed with
  this task; the substrate is not fit for use.
* Adding Nav1.6 may change the effective preferred direction; re-seed the E-I schedule only if
  the preferred direction has shifted by more than 30 deg from the t0037 40.8 deg anchor.
* Quadratic fits on 7 points are under-powered if noise is high; if the quadratic p-value is
  borderline (0.05 < p < 0.15), emit a suggestion for a denser 11-point sweep rather than
  declaring a verdict.

</details>

<details>
<summary>⏹ 0043 — <strong>Nav1.6 + Kv3 + NMDA restoration on t0022 channel
testbed</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0043_nav16_kv3_nmda_restoration_t0022` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0019-03` |
| **Task types** | [`feature-engineering`](../../../meta/task_types/feature-engineering/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Nav1.6 + Kv3 + NMDA restoration on t0022 channel testbed](../../../overview/tasks/task_pages/t0043_nav16_kv3_nmda_restoration_t0022.md) |
| **Task folder** | [`t0043_nav16_kv3_nmda_restoration_t0022/`](../../../tasks/t0043_nav16_kv3_nmda_restoration_t0022/) |

# Nav1.6 + Kv3 + NMDA Restoration on t0022

## Source Suggestion

S-0019-03 primary (implement Nav1.6 / Nav1.2 / Kv1 / Kv3 channels with AIS-specific
densities). This task covers the Nav1.6 and Kv3 portion of S-0019-03. It also partially covers
S-0018-03 (NMDA restoration) and S-0022-02 (Nav1.6 distal-AIS density).

## Motivation

The cross-task audit in brainstorm session 8 (see
`tasks/t0040_brainstorm_results_8/results/test_vs_literature_table.md`) identifies peak firing
rate as the most universal mismatch: 15 Hz across t0022 baseline and every t0022-based sweep,
vs 30–150 Hz in every cited published source (Oesch 2005: 148 Hz; Chen 2009: 166 Hz; Sivyer
2013: 80–150 Hz). The likely causes stack: (a) t0022 uses lumped HHst which lacks Nav1.6
persistent Na current and Kv3 fast repolarisation, both of which are needed for high-frequency
AP firing; (b) the t0022 E-I schedule zeros NMDA at both PD and ND BIPs, removing the expected
NMDA-mediated gain boost; (c) AMPA-only drive caps the effective depolarisation.

The audit also shows that Schachter 2010's predicted active-amplification diameter signature
is absent on every diameter sweep we have run (t0030, t0035, t0039). One candidate explanation
is that without Nav1.6 / Kv3 in the distal dendrite, the regenerative threshold-crossing
regime Schachter 2010 relies on cannot be recruited.

This task restores the channel inventory and NMDA drive so the peak-rate mismatch can be
attacked, and so the Schachter re-test in t0044 runs against a model that matches published
DSGC channel priors.

## Objective

Produce a new library asset (tentatively `modeldb_189347_dsgc_t0043` or similar) that is a
fork of the t0022 testbed with three modifications:

1. Nav1.6 mechanism inserted in AIS_DISTAL and all distal dendrite sections at density ~8
   mS/cm^2 (per t0019's cited DSGC priors). If a Nav1.6 MOD file is not already available,
   adapt one from the t0019 channel corpus.
2. Kv3 mechanism inserted in AIS_DISTAL and all distal dendrite sections at density ~5
   mS/cm^2.
3. NMDA synapse component restored at both PD and ND BIP terminals with conductance matching
   the Poleg-Polsky 2016 parameter backbone (read from t0008's library asset if available,
   else sourced from the Poleg-Polsky 2016 paper).

Hold the t0037 null-GABA sweet spot of 4 nS as the base parameter per t0038's correction. Keep
the 12-direction × 10-trial sweep protocol identical to t0022 / t0037 / t0039 so results are
directly comparable.

Pass criterion (both must hold):

* Peak firing rate in [40, 80] Hz at V_rest = -60 mV.
* Primary DSI within +/- 0.1 of the t0037 anchor of 0.429 at the 1.0x baseline diameter.

## Scope

* Local CPU only. No remote compute. ~6 hours wall-clock including MOD recompilation.
* Produce a library asset with the modified model plus a baseline 12-direction x 10-trial
  sweep at V_rest = -60 mV, GABA = 4 nS.
* Write a test harness that can be reused by t0044 for the diameter sweep.

## Out of Scope

* Nav1.2 and Kv1 (part of the fuller S-0019-03 scope, deferred).
* Morphology sweeps (covered by t0044 which uses this task's output as substrate).
* V_rest sweep (covered by t0026 on the prior testbed; a re-run on the new testbed could be a
  follow-up suggestion emitted from this task).

## Deliverables

* `assets/library/modeldb_189347_dsgc_t0043/` — library asset with the modified model,
  compiled MOD files, and baseline sweep driver.
* Baseline 12-direction x 10-trial sweep CSV under `results/`.
* Tuning curve (Cartesian and polar) under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections
  and an explicit Pass/Fail verdict against both criteria above.
* `results/metrics.json` with baseline primary DSI, vector-sum DSI, preferred direction, peak
  Hz, null Hz, and a boolean `peak_rate_pass` and `dsi_preserved_pass`.
* If Pass: the library asset is fit for use as t0044's substrate. If Fail: emit a suggestion
  for a follow-up calibration task (BIP burst rate + AMPA scale; see S-0040-01 or analogous)
  and stop before t0044.

## Anticipated Risks

* Nav1.6 MOD files in the t0019 corpus may not compile under NEURON 8.2.7 without adaptation;
  budget time for MOD debugging.
* Adding Nav1.6 may push the cell into runaway firing if the Kv3 density is too low; tune Kv3
  first, Nav1.6 second.
* Restoring NMDA may break the t0037 4 nS sweet spot by over-exciting at the null direction;
  if this happens, emit a follow-up suggestion to repeat a GABA sweet-spot search on the new
  testbed.

</details>

<details>
<summary>⏹ 0042 — <strong>Fine-grained null-GABA ladder (3.5, 3.0, 2.5 nS) on
t0022</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0042_fine_grained_null_gaba_ladder_t0022` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Fine-grained null-GABA ladder (3.5, 3.0, 2.5 nS) on t0022](../../../overview/tasks/task_pages/t0042_fine_grained_null_gaba_ladder_t0022.md) |
| **Task folder** | [`t0042_fine_grained_null_gaba_ladder_t0022/`](../../../tasks/t0042_fine_grained_null_gaba_ladder_t0022/) |

# Fine-Grained Null-GABA Ladder on t0022

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

<details>
<summary>⏹ 0041 — <strong>Electrotonic-length collapse analysis of t0034 and
t0035</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0041_electrotonic_length_collapse_t0034_t0035` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0035-01` |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [Electrotonic-length collapse analysis of t0034 and t0035](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md) |
| **Task folder** | [`t0041_electrotonic_length_collapse_t0034_t0035/`](../../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/) |

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

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
