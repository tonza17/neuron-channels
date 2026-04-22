# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

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

<details>
<summary>⏹ 0030 — <strong>Distal-dendrite diameter sweep on t0022 DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0030_distal_dendrite_diameter_sweep_dsgc` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0027-03` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Distal-dendrite diameter sweep on t0022 DSGC](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Task folder** | [`t0030_distal_dendrite_diameter_sweep_dsgc/`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/) |

# Distal-Dendrite Diameter Sweep on t0022 DSGC

## Motivation

The t0027 literature synthesis identified distal-dendrite diameter as a second-axis
discriminator between competing DS mechanisms that are individually consistent with our
current t0022 tuning data (DSI peak 0.6555 at V_rest = -60 mV, 15 Hz input):

* **Schachter2010 active-dendrite amplification** predicts DSI increases with distal
  thickening, because thicker distal compartments host more Na+ channel substrate per unit
  length and therefore amplify preferred-direction local spikes more strongly than passive
  EPSPs.
* **Passive-filtering alternatives** predict DSI decreases with distal thickening, because
  thicker dendrites have lower input impedance and less local depolarisation per unit synaptic
  current, so the directional contrast from asymmetric input patterns is damped.

A single-parameter sweep of distal diameter on the t0022 testbed, measuring DSI only, will
discriminate these mechanisms — a positive slope favours Schachter2010 active dendrites; a
negative slope favours passive filtering. Source suggestion **S-0027-03** (high priority) from
the t0027 literature synthesis.

## Scope

1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
2. Identify distal dendritic sections (tip compartments at branch order ≥ 3) in the
   morphology.
3. Sweep distal diameter in at least 7 values spanning from 0.5× to 2.0× the baseline diameter
   (e.g., 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0×). Apply the multiplier to all distal branches
   uniformly.
4. For each diameter value, run the standard 12-direction tuning protocol (15 Hz preferred-
   direction input) and compute DSI.
5. Plot DSI vs diameter and classify slope sign: positive (active-dendrite amplification),
   negative (passive filtering), flat (neither).

## Approach

* Local CPU only. No remote compute, no paid API.
* Reuse t0022 testbed code — copy relevant scripts into this task's `code/` directory.
* Vary the `diam` attribute on distal compartments by the sweep multiplier in a single
  experiment driver script.
* Use the existing tuning-curve scoring library from t0012 for DSI computation (consistent
  with t0022/t0026).
* Save per-sweep-point results to `results/data/sweep_results.csv`.
* Generate DSI-vs-diameter chart at `results/images/dsi_vs_diameter.png`.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-diameter
  slope sign and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each diameter
  value, slope sign classification, and discussion of which mechanism the data favours.
* `results/images/dsi_vs_diameter.png` — DSI-vs-diameter plot.
* `results/metrics.json` — DSI values at each diameter point.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* Local CPU only. Expected runtime: 30-90 minutes.
* $0 external cost.

## Measurement

* Primary metric: **DSI** at each diameter value.
* Secondary (recorded but not primary): per-direction spike counts, preferred-direction firing
  rate, peak voltage at a reference distal compartment (to confirm passive-impedance changes).

## Key Questions

1. Is the DSI-vs-diameter slope positive, negative, or flat?
2. If positive, is the slope consistent with Na+ channel-density amplification as predicted by
   Schachter2010?
3. If negative, does the preferred-direction firing rate drop alongside DSI (consistent with
   general damping) or does only the null-direction rate change?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC morphology and channel
  set including Nav density.

## Scientific Context

Source suggestion **S-0027-03** (high priority). Complementary to t0029 distal-length sweep:
length varies the spatial extent of distal integration, diameter varies the local impedance
and channel substrate. Together they span the two most important biophysical axes highlighted
in the t0027 synthesis.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 synthesis already did this), and
  `setup-machines` / `teardown` (local CPU).
* Include `compare-literature` — compare the DSI-vs-diameter curve to Schachter2010
  predictions.
* Can be executed in parallel with t0029 in a separate worktree.

</details>

<details>
<summary>⏹ 0029 — <strong>Distal-dendrite length sweep on t0022 DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0029_distal_dendrite_length_sweep_dsgc` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0027-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Distal-dendrite length sweep on t0022 DSGC](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Task folder** | [`t0029_distal_dendrite_length_sweep_dsgc/`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/) |

# Distal-Dendrite Length Sweep on t0022 DSGC

## Motivation

The t0027 literature synthesis identified two published mechanisms that both fit our current
t0022 tuning data (DSI peak 0.6555 at V_rest = -60 mV, 15 Hz input): **Dan2018** passive
transfer- resistance weighting, and **Sivyer2013** dendritic-spike branch independence. The
two mechanisms make divergent predictions about how DSI should change as distal-dendrite
length varies:

* **Dan2018 passive TR**: DSI increases monotonically with distal length, because longer
  distal dendrites create a steeper transfer-resistance gradient from synapse to soma and
  therefore stronger directional weighting of passive EPSPs.
* **Sivyer2013 dendritic spike**: DSI saturates (plateau) once distal branches are long enough
  to independently generate local dendritic spikes; further length increases contribute no
  additional DSI because the spike threshold is already cleared.

A clean single-parameter sweep of distal length on the t0022 testbed, measuring DSI only, will
discriminate between these mechanisms — a monotonic curve favours Dan2018; a saturating curve
favours Sivyer2013. This is the highest-information-gain experiment identified by the t0027
synthesis (suggestion S-0027-01, high priority).

## Scope

1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
2. Identify distal dendritic sections (tip compartments at branch order ≥ 3) in the
   morphology.
3. Sweep distal length in at least 7 values spanning from 0.5× to 2.0× the baseline length
   (e.g., 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0×). Use the same sweep step size for all
   branches.
4. For each length value, run a full 12-direction tuning protocol (standard t0022 protocol
   with 15 Hz preferred-direction input) and compute DSI.
5. Plot DSI vs length and classify the curve shape as monotonic / saturating / non-monotonic.
6. Report the fitted slope (for monotonic), the saturation length (for saturating), or
   describe the qualitative shape (for non-monotonic).

## Approach

* Run locally on CPU only. No remote compute, no paid API.
* Reuse the t0022 testbed code under `tasks/t0022_modify_dsgc_channel_testbed/code/` — copy
  the needed scripts into this task's `code/` directory (per CLAUDE.md rule on cross-task
  imports).
* Vary the `L` attribute (section length) on all distal compartments by the sweep multiplier
  in a single experiment driver script.
* Use the existing tuning-curve scoring library from
  `tasks/t0012_tuning_curve_scoring_loss_library/` to compute DSI consistently with
  t0022/t0026.
* Save per-sweep-point results (DSI, per-direction firing rates) to
  `results/data/sweep_results.csv`.
* Generate a DSI-vs-length chart and save to `results/images/dsi_vs_length.png`.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-length
  relationship and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each length
  value, curve-shape classification, and discussion of which mechanism the data favours.
* `results/images/dsi_vs_length.png` — DSI-vs-length plot.
* `results/metrics.json` — DSI values at each length point.
* No paper, dataset, library, model, or answer assets produced by this task.

## Compute and Budget

* Local CPU only, no GPU. Expected runtime: 30-90 minutes depending on per-direction
  simulation cost.
* $0 external cost.

## Measurement

* Primary metric: **DSI** at each length value.
* Secondary (recorded but not primary): per-direction spike counts, preferred-direction firing
  rate.

## Key Questions

1. Is DSI monotonically increasing with distal length, or does it saturate?
2. At what length does saturation occur (if any)?
3. Is the DSI range at the sweep extremes (0.5× and 2.0×) large enough to distinguish the
   mechanisms, or does the testbed saturate at our default length?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC morphology and channel
  set.

## Scientific Context

Source suggestion **S-0027-01** (high priority). The t0027 synthesis answer identifies this as
the single highest-information-gain morphology experiment because the two competing mechanisms
make mathematically opposite predictions on the distal-length axis. Baseline papers supporting
each mechanism:

* Dan2018 passive-TR: builds the mechanism on a passive cable derivation.
* Sivyer2013 dendritic-spike: depends on Nav density in distal dendrites, which t0022 retains.

If the experiment reveals a non-monotonic curve, the t0027 synthesis flagged kinetic tiling
(Espinosa 2010) as a possible third mechanism — defer to a follow-up task.

## Execution Notes

* Follow the standard /execute-task flow: create-branch, check-deps, init-folders,
  implementation, results, suggestions, reporting.
* Include the `planning` step (the sweep design and compartment-identification logic benefit
  from explicit planning).
* Skip `research-papers`, `research-internet` (t0027 synthesis already did this), and
  `setup-machines` / `teardown` (local CPU only).
* Include `compare-literature` — the whole point is to compare the DSI-vs-length curve to
  Dan2018 and Sivyer2013 predictions.

</details>
