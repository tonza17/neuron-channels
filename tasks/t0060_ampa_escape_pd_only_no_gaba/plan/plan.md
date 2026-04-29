# Plan: t0060 Quick AMPA-Escape Test (PD only, GABA = 0)

## Objective

Run a 16-trial diagnostic on the t0059 minimal-DSGC substrate to characterise soma V(t) when GABA is
fully removed and gAMPA is swept across an extended range, comparing FULL (HH on) and EPSP_PASSIVE
(HH off) modes at the preferred direction (theta = 0 deg).

## Approach

Reuse the t0059 `minimal_dsgc_bar_locked_gaba_ampa_sweep` library via Python imports (no code copy).
Write a small `run_pd_only.py` that calls the t0059 cell + pair construction primitives, loops over
(gAMPA, mode) pairs, and writes `voltage_traces_pd_only.csv` plus a JSON summary. Render two PNGs
(per-gAMPA panel grid + overlay) via `plot_traces.py`.

## Cost Estimation

$0.00 — local CPU only.

## Step by Step

1. Build NEURON cell, pairs, placement (seed 0, identical to t0059).
2. Loop over 8 gAMPA × 2 modes × 1 trial × 1 direction = 16 trials, calling `run_one_trial(...)`
   with `gaba_base_ns = 0.0` and `angle_deg = 0.0`.
3. Write voltage_traces_pd_only.csv and summary_pd_only.csv.
4. Render voltage_response_grid.png and voltage_response_overlay.png.

## Remote Machines

None.

## Assets Needed

* t0059 library (registered): `minimal_dsgc_bar_locked_gaba_ampa_sweep`.
* t0009 dataset: `dsgc-baseline-morphology-calibrated`.

## Expected Assets

None (diagnostic — no library asset produced).

## Time Estimation

~30-150 s for the 16-trial sweep on local CPU under CVODE.

## Risks & Fallbacks

* **NetCon spike threshold yields false positives in EPSP_PASSIVE at high gAMPA**: the
  AP_THRESHOLD_MV = -20 mV crossings happen on the passive trace at gAMPA ≥ 5 nS; documented in
  results_detailed.md.

## Verification Criteria

* `voltage_traces_pd_only.csv` and the two PNGs exist.
* `verify_task_file`, `verify_task_folder`, `verify_task_results`, `verify_logs` pass with 0 errors.
