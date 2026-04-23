# Distal-Dendrite Diameter Sweep on t0024 DSGC

## Motivation

The sibling task t0030 ran a distal-diameter sweep on the t0022 DSGC testbed and produced a **null
result** for mechanism discrimination: primary DSI pinned at 1.000 across every diameter multiplier
because t0022's deterministic E-I schedule silences null firing (0 Hz). Vector-sum DSI fallback
produced a flat slope too (p=0.18 on t0030).

The t0024 de Rosenroll 2026 port has fundamentally different biophysics that **fix the t0022
pathology**:

* **AR(2)-correlated stochastic bipolar release** (ρ=0.6) produces non-zero null-direction firing.
  Per t0026's V_rest sweep, t0024's DSI ranges 0.36-0.67 with a measurable 1.9× modulation — the
  discriminator has room to act.
* **No Na-inactivation collapse** at depolarised V_rest (peak firing monotone to 7.6 Hz at V_rest =
  -20 mV).
* **AR(2) noise smooths tuning** (HWHM pinned 65-83° across V_rest).

Running the t0030 diameter sweep on t0024 should therefore produce a **measurable primary DSI
slope** that can actually distinguish the two mechanisms:

* **Schachter2010 active-dendrite amplification**: DSI increases with distal thickening because
  thicker compartments host more Na+ substrate per unit length and amplify preferred-direction local
  spikes more strongly.
* **Passive-filtering alternatives**: DSI decreases with distal thickening because thicker dendrites
  have lower input impedance and less local depolarisation per unit synaptic current, damping the
  directional contrast.

Covers source suggestion **S-0027-03** (high priority) on the t0024 biophysics. Companion to t0034
(length sweep on t0024).

## Scope

1. Use the **t0024 de Rosenroll 2026 DSGC port** as-is (no channel modifications, no input
   rewiring). Keep the AR(2) correlation ρ=0.6 at its t0026 V_rest-sweep default.
2. Identify distal dendritic sections (HOC leaves on `h.RGC.ON` arbor). Mirror the selection rule
   from t0030's `diameter_override.py` but **COPY** the helper into this task's
   `code/diameter_override_t0024.py` — no cross-task imports per CLAUDE.md.
3. Sweep distal diameter in **7 values** spanning **0.5× to 2.0×** baseline (0.5, 0.75, 1.0, 1.25,
   1.5, 1.75, 2.0×). Apply the multiplier uniformly to all distal branches.
4. For each diameter value, run the **standard 12-direction tuning protocol** (12 angles × 10
   trials) and compute **primary DSI** as the operative metric. Also emit vector-sum DSI and
   secondary metrics.
5. Plot primary DSI vs diameter and classify slope sign: positive (Schachter2010 active), negative
   (passive filtering), flat (neither or schedule-dominated).

## Approach

* **Local CPU only.** No remote compute, no paid API.
* Reuse the t0024 port code at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/` (the
  de_rosenroll_2026_port library is registered and t0024's driver is the model reference).
* Copy the t0030 workflow template: `paths.py`, `constants.py`, `diameter_override.py` (with
  `identify_distal_sections`), `preflight_distal.py`, `trial_runner_diameter.py`, `run_sweep.py`,
  `analyse_sweep.py`, `classify_slope.py`, and `plot_sweep.py`.
* Save per-sweep-point data to `results/data/sweep_results.csv` (incremental checkpoint) and
  per-diameter tuning curves to `results/data/per_diameter/*.csv`.
* Render DSI-vs-diameter chart at `results/images/dsi_vs_diameter.png` plus secondary diagnostic
  plots.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-diameter slope
  sign and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each diameter value,
  slope classification, mechanism attribution (Schachter2010 vs passive filtering), comparison to
  t0030's null result.
* `results/images/dsi_vs_diameter.png` — primary DSI-vs-diameter slope.
* `results/images/vector_sum_dsi_vs_diameter.png` — vector-sum DSI as secondary diagnostic.
* `results/images/polar_overlay.png` — 12-direction polar overlay across all 7 diameters.
* `results/metrics.json` — registered per-diameter DSI metrics.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* **Local CPU only**; no GPU.
* **Expected runtime: 2-4 hours.** The per-(angle, trial) wall time on t0024 is **~12 s** (per
  t0026's V_rest-sweep baseline), vs t0022's ~3.8 s. Full sweep = 7 × 12 × 10 = 840 trials ≈ **~168
  min** at 12 s/trial, plus overhead. Thinner diameters will run slower due to increased axial
  resistance (same behaviour observed on t0030).
* **$0 external cost.**

## Measurement

* **Primary metric**: **primary DSI (peak-minus-null)** at each diameter value. Unlike t0030, this
  is expected to vary because t0024 has non-zero null-direction firing.
* **Secondary**: vector-sum DSI (sanity cross-check), peak Hz, null Hz, HWHM, reliability,
  preferred-direction firing rate, per-direction spike counts, peak voltage at a reference distal
  compartment (to confirm impedance changes).

## Key Questions

1. Is the primary DSI-vs-diameter slope positive (Schachter2010), negative (passive filtering), or
   flat?
2. If positive, is the slope consistent with Na-channel-density amplification as predicted by
   Schachter2010?
3. If negative, does preferred-direction firing drop alongside DSI (general damping) or does only
   the null-direction rate change (selective mechanism)?
4. Does t0024's AR(2) noise broaden the HWHM enough to mask the mechanism signal, or does the
   primary-DSI trend survive the noise floor?
5. How do t0024 and t0022 compare under identical sweep protocols? A measurable slope on t0024 while
   t0030 was flat would confirm that the pinned-DSI pathology was the culprit.

## Dependencies

* **t0024_port_de_rosenroll_2026_dsgc** (completed) — provides the DSGC port with AR(2) stochastic
  release.
* **t0030_distal_dendrite_diameter_sweep_dsgc** (completed) — provides the workflow template, the
  `identify_distal_sections` helper (to be copied, not imported), and the null-result baseline for
  comparison.

## Scientific Context

Source suggestion **S-0027-03** (high priority) originally planned for t0022 and executed as t0030.
This task re-runs the same experiment on t0024 specifically because t0024's stochastic release
restores non-zero null firing and therefore makes the primary DSI discriminator meaningful.
Companion to **t0034** (length sweep on t0024).

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 synthesis already covered the mechanism
  predictions; t0030 already surveyed the prior code).
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `research-code` — need to read the t0024 driver and the t0030 workflow pattern.
* Include `creative-thinking` — if the primary-DSI discriminator works on t0024, consider what
  schedule-level properties t0022 would need to adopt to recover sensitivity.
* Include `compare-literature` — compare the t0024 DSI-vs-diameter slope to Schachter2010 and
  passive-filtering predictions **and** to the t0030 null result.
* **Can be executed in parallel with t0034 in a separate worktree.**
