# Distal-Dendrite Length Sweep on t0024 DSGC

## Motivation

The sibling task t0029 ran a distal-length sweep on the t0022 DSGC testbed and produced a **null
result** for mechanism discrimination: primary DSI (peak-minus-null) pinned at 1.000 across every
length multiplier because t0022's deterministic E-I schedule silences null firing (0 Hz). The
vector-sum DSI fallback also produced a flat slope (p=0.18 on t0029).

The t0024 de Rosenroll 2026 port has fundamentally different biophysics that **fix the t0022
pathology**:

* **AR(2)-correlated stochastic bipolar release** (ρ=0.6) produces non-zero null-direction firing.
  Per t0026's V_rest sweep, t0024's DSI ranges 0.36-0.67 with a measurable 1.9× modulation — the
  discriminator has room to act.
* **No Na-inactivation collapse** at depolarised V_rest (peak firing monotone to 7.6 Hz at V_rest =
  -20 mV).
* **AR(2) noise smooths tuning** (HWHM pinned 65-83° across V_rest).

Running the t0029 length sweep on t0024 should therefore produce a **measurable primary DSI slope**
that can actually distinguish the two mechanisms:

* **Dan2018 passive transfer-resistance weighting**: DSI increases monotonically with distal length
  (longer distal dendrites → steeper TR gradient → stronger directional weighting).
* **Sivyer2013 dendritic-spike branch independence**: DSI saturates (plateau) once distal branches
  clear local spike threshold; further lengthening adds no DSI.

Covers source suggestion **S-0027-01** (high priority) on the t0024 biophysics. Companion to t0035
(diameter sweep on t0024).

## Scope

1. Use the **t0024 de Rosenroll 2026 DSGC port** as-is (no channel modifications, no input
   rewiring). Keep the AR(2) correlation ρ=0.6 at its t0026 V_rest-sweep default.
2. Identify distal dendritic sections (HOC leaves on `h.RGC.ON` arbor). Mirror the selection rule
   from t0029's `length_override.py:37-52` but **COPY** the helper into this task's
   `code/length_override_t0024.py` — no cross-task imports per CLAUDE.md.
3. Sweep distal length in **7 values** spanning **0.5× to 2.0×** baseline (0.5, 0.75, 1.0, 1.25,
   1.5, 1.75, 2.0×). Apply the multiplier uniformly to all distal branches.
4. For each length value, run the **standard 12-direction tuning protocol** (12 angles × 10 trials)
   and compute **primary DSI** as the operative metric. Also emit vector-sum DSI and secondary
   metrics as t0029 did.
5. Plot primary DSI vs length and classify the curve shape: monotonic (favours Dan2018), saturating
   (favours Sivyer2013), or non-monotonic (neither or kinetic-tiling).

## Approach

* **Local CPU only.** No remote compute, no paid API.
* Reuse the t0024 port code at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/` (the
  de_rosenroll_2026_port library is registered and t0024's driver is the model reference).
* Copy the t0029 workflow template: `paths.py`, `constants.py`, `length_override.py` (with
  `identify_distal_sections`), `preflight_distal.py`, `trial_runner_length.py`, `run_sweep.py`,
  `analyse_sweep.py`, `classify_shape.py` (monotonic / saturating / non-monotonic), and
  `plot_sweep.py`.
* Save per-sweep-point data to `results/data/sweep_results.csv` (incremental checkpoint) and
  per-diameter tuning curves to `results/data/per_length/*.csv`.
* Render DSI-vs-length chart at `results/images/dsi_vs_length.png` plus secondary diagnostic plots.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-length curve
  shape and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each length value,
  curve-shape classification, mechanism attribution (Dan2018 vs Sivyer2013), comparison to t0029's
  null result.
* `results/images/dsi_vs_length.png` — primary DSI-vs-length curve.
* `results/images/vector_sum_dsi_vs_length.png` — vector-sum DSI as secondary diagnostic.
* `results/images/polar_overlay.png` — 12-direction polar overlay across all 7 lengths.
* `results/metrics.json` — registered per-length DSI metrics.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* **Local CPU only**; no GPU.
* **Expected runtime: 2-4 hours.** The per-(angle, trial) wall time on t0024 is **~12 s** (per
  t0026's V_rest-sweep baseline), vs t0022's ~3.8 s. Full sweep = 7 × 12 × 10 = 840 trials ≈ **~168
  min** at 12 s/trial, plus overhead.
* **$0 external cost.**

## Measurement

* **Primary metric**: **primary DSI (peak-minus-null)** at each length value. Unlike t0029, this is
  expected to vary because t0024 has non-zero null-direction firing.
* **Secondary**: vector-sum DSI (sanity cross-check), peak Hz, null Hz, HWHM, reliability,
  preferred-direction firing rate, per-direction spike counts.

## Key Questions

1. Is primary DSI monotonically increasing with distal length (Dan2018), saturating (Sivyer2013), or
   non-monotonic (neither)?
2. At what length does saturation occur (if any)?
3. Does the t0024 AR(2) noise broaden the HWHM enough to mask the mechanism signal, or does the
   primary-DSI trend survive the noise floor?
4. How do the t0024 and t0022 results compare under identical sweep protocols? A matched DSI trend
   on both would strengthen the mechanism claim; divergent trends would indicate that t0022's pinned
   primary DSI masked a real effect.

## Dependencies

* **t0024_port_de_rosenroll_2026_dsgc** (completed) — provides the DSGC port with AR(2) stochastic
  release.
* **t0029_distal_dendrite_length_sweep_dsgc** (completed) — provides the workflow template, the
  `identify_distal_sections` helper (to be copied, not imported), and the null-result baseline for
  comparison.

## Scientific Context

Source suggestion **S-0027-01** (high priority) originally planned for t0022 and executed as t0029.
This task re-runs the same experiment on t0024 specifically because t0024's stochastic release
restores non-zero null firing and therefore makes the primary DSI discriminator meaningful.
Companion to **t0035** (diameter sweep on t0024).

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 synthesis already covered the mechanism
  predictions; t0029 already surveyed the prior code).
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `research-code` — need to read t0024 driver and t0029's workflow pattern.
* Include `creative-thinking` — if the primary-DSI discriminator works on t0024, consider whether
  t0022's null result was due to schedule-only dominance or a deeper pathology.
* Include `compare-literature` — compare the t0024 DSI-vs-length curve to Dan2018 and Sivyer2013
  predictions **and** to the t0029 null result.
