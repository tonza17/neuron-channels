# Results Summary: Port de Rosenroll 2026 DSGC Model

## Summary

Ported the de Rosenroll et al. 2026 DSGC model into a new library asset `de_rosenroll_2026_dsgc`
(NEURON `HHst_noiseless`/`Exp2NMDA`/`cadecay` MOD mechanisms with the 341-section `RGCmodelGD.hoc`
morphology, vendored from Zenodo `10.5281/zenodo.17666158` at commit `a23f642a`). Drove the cell
through the paper-native 8-direction protocol and the project-standard 12-angle protocol under both
correlated (`rho=0.6`) and uncorrelated (`rho=0.0`) AR(2) release-rate noise (20 trials per angle,
800 trials total, ~4h15m wall time on the local Windows workstation). The port produces strong
direction selectivity but **does not** reproduce the paper's correlation-drop signature; the
port-fidelity gate (REQ-5) failed and the miss is recorded in `intervention/port_fidelity_miss.md`
as a first-class finding per plan step 13.

## Metrics

* **DSI 12-ang correlated** (project-standard, t0004 envelope): **0.7759** — well above t0008's
  0.316 and matching t0020's 0.7838 / t0022's 1.0 lineage
* **DSI 12-ang uncorrelated**: **0.8557** — *higher* than correlated, opposite of paper prediction
* **DSI 8-dir correlated** (paper-match, REQ-5 target [0.30, 0.50]): **0.8182** — FAIL
* **DSI 8-dir uncorrelated** (paper-match, REQ-5 target [0.18, 0.35]): **0.8351** — FAIL
* **Correlation-drop fraction** (target >= 0.20): **0.000** — FAIL
* **Peak firing rate (12-ang correlated)**: **5.15 Hz** — far below t0004 envelope [40, 80] Hz
  (consistent lineage-wide gap; t0008 18.1 Hz, t0020 14.85 Hz, t0022 15 Hz)
* **HWHM (12-ang correlated)**: **68.65 deg** — narrower than t0008 (82.81) and t0022 (116.25);
  inside the t0004 envelope around 66 deg
* **Tuning-curve reliability**: **0.9836** — high trial-to-trial consistency
* **RMSE vs t0004 target**: **15.49 Hz** — comparable to t0008 (13.73) and t0022 (10.48)
* **Wall time**: ~4h15m for 800 trials on the local Windows workstation
* **Cost**: $0.00 (no paid services, no remote compute)

## Verification

* `verify_task_dependencies.py` — PASSED (t0008, t0012, t0022 all completed) at check-deps step
* `verify_task_file.py` — PASSED at init-folders (0 errors)
* **Port-fidelity gate (REQ-5)** — FAILED (3/3 sub-criteria miss); recorded in
  `intervention/port_fidelity_miss.md` and
  `metrics.json["de_rosenroll_port_fidelity_gate_pass"] = false` per plan step 13. Does not block
  step closure.
* **CSV schema (REQ-3, REQ-4)** — PASSED: 4 CSVs under `data/`, 240 rows for 12-angle and 160 rows
  for 8-direction, columns `trial,direction_deg,spike_count,peak_mv`
* **Score report (REQ-3)** — PASSED: `data/score_report.json` populated with all 13 fields
  (loss_scalar 0.99, dsi/hwhm/null/peak residuals, per-target gate)
* **Plots (REQ-3, REQ-4)** — PASSED: 4 PNGs in `results/images/` (polar + Cartesian for both
  12-angle conditions; 8-direction plotting skipped because the t0011/t0012 plotter hardcodes
  N_ANGLES=12)
* **Library asset structure** — PASSED manually against
  `meta/asset_types/library/specification.md` (no automated `verify_library_asset.py` script exists;
  flagged framework-wide gap)
* **Lint / format** — `ruff check --fix . && ruff format .` clean across the task tree
