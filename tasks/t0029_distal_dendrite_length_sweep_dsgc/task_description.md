# Distal-Dendrite Length Sweep on t0022 DSGC

## Motivation

The t0027 literature synthesis identified two published mechanisms that both fit our current t0022
tuning data (DSI peak 0.6555 at V_rest = -60 mV, 15 Hz input): **Dan2018** passive transfer-
resistance weighting, and **Sivyer2013** dendritic-spike branch independence. The two mechanisms
make divergent predictions about how DSI should change as distal-dendrite length varies:

* **Dan2018 passive TR**: DSI increases monotonically with distal length, because longer distal
  dendrites create a steeper transfer-resistance gradient from synapse to soma and therefore
  stronger directional weighting of passive EPSPs.
* **Sivyer2013 dendritic spike**: DSI saturates (plateau) once distal branches are long enough to
  independently generate local dendritic spikes; further length increases contribute no additional
  DSI because the spike threshold is already cleared.

A clean single-parameter sweep of distal length on the t0022 testbed, measuring DSI only, will
discriminate between these mechanisms — a monotonic curve favours Dan2018; a saturating curve
favours Sivyer2013. This is the highest-information-gain experiment identified by the t0027
synthesis (suggestion S-0027-01, high priority).

## Scope

1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
2. Identify distal dendritic sections (tip compartments at branch order ≥ 3) in the morphology.
3. Sweep distal length in at least 7 values spanning from 0.5× to 2.0× the baseline length (e.g.,
   0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0×). Use the same sweep step size for all branches.
4. For each length value, run a full 12-direction tuning protocol (standard t0022 protocol with 15
   Hz preferred-direction input) and compute DSI.
5. Plot DSI vs length and classify the curve shape as monotonic / saturating / non-monotonic.
6. Report the fitted slope (for monotonic), the saturation length (for saturating), or describe the
   qualitative shape (for non-monotonic).

## Approach

* Run locally on CPU only. No remote compute, no paid API.
* Reuse the t0022 testbed code under `tasks/t0022_modify_dsgc_channel_testbed/code/` — copy the
  needed scripts into this task's `code/` directory (per CLAUDE.md rule on cross-task imports).
* Vary the `L` attribute (section length) on all distal compartments by the sweep multiplier in a
  single experiment driver script.
* Use the existing tuning-curve scoring library from
  `tasks/t0012_tuning_curve_scoring_loss_library/` to compute DSI consistently with t0022/t0026.
* Save per-sweep-point results (DSI, per-direction firing rates) to
  `results/data/sweep_results.csv`.
* Generate a DSI-vs-length chart and save to `results/images/dsi_vs_length.png`.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-length
  relationship and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each length value,
  curve-shape classification, and discussion of which mechanism the data favours.
* `results/images/dsi_vs_length.png` — DSI-vs-length plot.
* `results/metrics.json` — DSI values at each length point.
* No paper, dataset, library, model, or answer assets produced by this task.

## Compute and Budget

* Local CPU only, no GPU. Expected runtime: 30-90 minutes depending on per-direction simulation
  cost.
* $0 external cost.

## Measurement

* Primary metric: **DSI** at each length value.
* Secondary (recorded but not primary): per-direction spike counts, preferred-direction firing rate.

## Key Questions

1. Is DSI monotonically increasing with distal length, or does it saturate?
2. At what length does saturation occur (if any)?
3. Is the DSI range at the sweep extremes (0.5× and 2.0×) large enough to distinguish the
   mechanisms, or does the testbed saturate at our default length?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC morphology and channel set.

## Scientific Context

Source suggestion **S-0027-01** (high priority). The t0027 synthesis answer identifies this as the
single highest-information-gain morphology experiment because the two competing mechanisms make
mathematically opposite predictions on the distal-length axis. Baseline papers supporting each
mechanism:

* Dan2018 passive-TR: builds the mechanism on a passive cable derivation.
* Sivyer2013 dendritic-spike: depends on Nav density in distal dendrites, which t0022 retains.

If the experiment reveals a non-monotonic curve, the t0027 synthesis flagged kinetic tiling
(Espinosa 2010) as a possible third mechanism — defer to a follow-up task.

## Execution Notes

* Follow the standard /execute-task flow: create-branch, check-deps, init-folders, implementation,
  results, suggestions, reporting.
* Include the `planning` step (the sweep design and compartment-identification logic benefit from
  explicit planning).
* Skip `research-papers`, `research-internet` (t0027 synthesis already did this), and
  `setup-machines` / `teardown` (local CPU only).
* Include `compare-literature` — the whole point is to compare the DSI-vs-length curve to Dan2018
  and Sivyer2013 predictions.
