---
spec_version: "3"
task_id: "t0060_ampa_escape_pd_only_no_gaba"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T21:46:40Z"
completed_at: "2026-04-29T21:50:00Z"
---

# Step 9 — Implementation

## Summary

Wrote 4 small task-specific Python files (paths, constants, run_pd_only, plot_traces) that import
the t0059 minimal_dsgc_bar_locked_gaba_ampa_sweep library primitives and run a 16-trial PD-only
sweep with GABA = 0. Sweep completed in 127.36 s. Both PNGs rendered. Results show: substrate
sub-threshold at gAMPA=0.1, single-spike escape at gAMPA=0.5, plateau at 1-2 spikes for
gAMPA=1-15, mild multi-spike (4 spikes) at gAMPA=20. EPSP_PASSIVE peak Vm rises monotonically from
-60.67 mV to -3.76 mV (asymptotes toward E_AMPA=0 mV) — confirms HH save-and-zero is correctly
wired even at extreme gAMPA.

## Actions Taken

1. Wrote `code/paths.py` with task-local path constants.
2. Wrote `code/constants.py` with sweep parameters (GABA=0, theta=0, gAMPA values, n_trials=1).
3. Wrote `code/run_pd_only.py` that imports t0059 primitives (build_dsgc_from_swc,
   sample_dendritic_locations, build_ei_pairs, run_one_trial) and runs 8 gAMPA × 2 modes × 1
   trial = 16 trials, writing voltage_traces_pd_only.csv, summary_pd_only.csv, wallclock.json.
   Bypasses t0059's setup_sweep_artifacts (which would write placement to t0059's results dir);
   instead writes placement_seed0.json into t0060's results dir using the identical seed=0.
4. Wrote `code/plot_traces.py` that renders voltage_response_grid.png (8 panels) and
   voltage_response_overlay.png (single panel, 16 colour-graded traces).
5. Ran the sweep via `run_with_logs`. Wall-clock 127.36 s; 16 trials × ~8 s/trial.
6. Initial plotting attempt produced empty axes due to a mode-string case mismatch
   (TrialMode.value emits lowercase "full" / "epsp_passive"; my filter used uppercase). Fixed
   the filter strings; plots regenerated successfully.
7. Lint / format / mypy clean across all 4 task code modules.

## Outputs

* `tasks/t0060_ampa_escape_pd_only_no_gaba/code/{paths,constants,run_pd_only,plot_traces}.py`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/voltage_traces_pd_only.csv`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/summary_pd_only.csv`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/wallclock.json`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/placement_seed0.json`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/images/voltage_response_grid.png`
* `tasks/t0060_ampa_escape_pd_only_no_gaba/results/images/voltage_response_overlay.png`

## Issues

The NetCon spike threshold AP_THRESHOLD_MV = -20 mV (inherited from t0059) creates false-positive
"spike" detections in EPSP_PASSIVE mode at gAMPA ≥ 5 nS — the passive Vm legitimately crosses
-20 mV without an actual AP firing. Documented in results_detailed.md; not a bug in the HH
save-and-zero (which is verified working — peak Vm stays well below E_AMPA = 0 mV in all 8
EPSP_PASSIVE conditions).

The plotting case-mismatch was a one-line bug; fixed in place.
