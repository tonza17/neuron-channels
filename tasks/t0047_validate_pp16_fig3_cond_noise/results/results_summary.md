# Results Summary: Validate Poleg-Polsky 2016 Fig 3A-F Conductances and Extend Noise Sweep

## Summary

The deposited ModelDB 189347 code does **not** reproduce Poleg-Polsky 2016's Fig 3A-F simulation
targets: per-synapse-class conductances are 6-9x the paper's stated values on the summed scale (or
30-90x under on a per-synapse-mean scale, so neither interpretation reconciles), and the DSI vs
gNMDA curve peaks at 0.19 and decays to 0.018 instead of staying flat near 0.30. The extended noise
sweep does show DSI declining as flickerVAR rises (qualitative match for Figs 6-7), but the ROC AUC
metric saturates at 1.0 in every cell because the implementation uses pre-stimulus baseline voltage
as the negative class and PSP peaks dwarf baselines on this circuit.

## Metrics

* **NMDA conductance at gNMDA = 0.5 nS** (summed across 282 synapses): PD **69.55 +/- 5.86 nS** vs
  paper **~7.0 nS** (9.9x over); ND **33.98 +/- 1.83 nS** vs paper **~5.0 nS** (6.8x over).
* **AMPA conductance at gNMDA = 0.5 nS** (summed): PD **10.92 +/- 0.37 nS** vs paper **~3.5 nS**
  (3.1x over); ND **10.77 +/- 0.60 nS** vs paper **~3.5 nS** (3.1x over). AMPA shows essentially
  zero direction selectivity (PD/ND = 1.01) consistent with the paper's qualitative claim.
* **GABA conductance at gNMDA = 0.5 nS** (summed): PD **106.13 +/- 5.77 nS** vs paper **~12.5 nS**
  (8.5x over); ND **215.57 +/- 2.72 nS** vs paper **~30.0 nS** (7.2x over). The ND/PD ratio is 2.03,
  qualitatively matching the paper's stronger ND inhibition.
* **DSI vs gNMDA curve**: peaks at **0.19** at gNMDA = 0.5 nS, decays through {0.11, 0.04, 0.03,
  0.02, 0.018} at gNMDA = {1.0, 1.5, 2.0, 2.5, 3.0} nS. Paper claims DSI is approximately constant
  **~0.30** across this range. Mismatch confirmed at all 7 grid points.
* **DSI vs noise (control)**: declines from **0.189** at flickerVAR = 0.0 to **0.153** at 0.5 (-19%,
  qualitatively monotonic).
* **DSI vs noise (AP5)**: declines from **0.093** to **0.046** (-50%, with a small non-monotonic
  bump at 0.5).
* **DSI vs noise (0Mg)**: declines from **0.090** to **0.047** (-48%, cleanest monotonic).
* **ROC AUC**: saturates at **1.000** in every (condition, noise) cell — implementation limitation
  of the t0046 helper, not a model finding. Documented as discrepancy entry 15.
* **Discrepancy catalogue update**: extends t0046's 12 entries with 3 new findings (per-synapse
  conductance scale mismatch, DSI-vs-gNMDA non-flatness reproducibility, ROC AUC saturation).

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors) on the multi-variant `metrics.json` (19 variants)
* `verify_plan.py` — PASSED (0 errors)
* `verify_research_code.py` — PASSED (0 errors)
* `ruff check` and `ruff format` — clean across all 9 task code modules
* `mypy -p tasks.t0047_validate_pp16_fig3_cond_noise.code` — clean (no errors)
* Smoke test (Step 5 from plan): per-trial conductance recording confirmed; PD soma trace shape
  matches t0046's previously-recorded trace within rounding (sanity check passed)
