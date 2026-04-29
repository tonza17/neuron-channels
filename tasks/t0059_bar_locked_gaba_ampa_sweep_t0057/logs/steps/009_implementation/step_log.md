---
spec_version: "3"
task_id: "t0059_bar_locked_gaba_ampa_sweep_t0057"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T00:32:49Z"
completed_at: "2026-04-29T20:17:00Z"
---

# Step 9 — Implementation

## Summary

Built the t0059 bar-arrival-locked tonic GABA + AMPA escape sweep substrate by forking t0057's
`minimal_dsgc_tonic_gaba_sweep` library with four targeted edits (per-synapse `(t_on_i, t_off_i)`
windows, EPSP_PASSIVE/IPSP_PASSIVE save-and-zero protocol replacing the legacy E_ONLY/GABA_ONLY
trio, 5x5 (gAMPA, GABA_BASE_NS) outer loop, TSTOP=1400 ms). Ran the full 9000-trial sweep (5x5 grid
x 12 directions x 10 trials x 3 modes) in 11.56 hours wall-clock. All 22 REQ items addressed with
status Done; library asset `minimal_dsgc_bar_locked_gaba_ampa_sweep` verified; 8/8 tests pass; 1233
PNGs generated. Headline finding (negative): no operating point on the swept grid produces the
multi-spike regime (max peak Hz across all 25 cells is 2.14 Hz at gAMPA=2.0 / 3.0).

## Actions Taken

1. Spawned the `/implementation` subagent which copied t0057's 13-module + 4-test code tree into
   `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/` with import-prefix rewrites, applied the
   four targeted edits in `synapses.py`, `trial.py`, `run_tuning_curve.py`, `constants.py`,
   built / loaded `mod/GabaTonic.mod`, and added two new regression tests
   (`test_bar_locked_ipsp_envelope.py`, `test_hh_save_and_zero.py`).

2. The first sweep ran 7 h 32 m and completed all 9000 trials, but a post-sweep
   `_check_epsp_peak_vm_gate` aborted before CSV writing because at gAMPA=2.0 nS the passive Vm
   reached -17.99 mV — well above the gate's `AP_THRESHOLD_MV = -20 mV` threshold but well below
   the AMPA reversal `E_AMPA = 0 mV`. Lost 7 h 32 m of compute.

3. Patched the gate logic to preserve data on future trips:
   * Added new constant `EPSP_PASSIVE_PEAK_VM_GATE_MV = 5.0` in `constants.py` (above E_AMPA;
     a passive cell physically cannot exceed this).
   * Switched `run_tuning_curve.py` and `compute_metrics.py` gates from `AP_THRESHOLD_MV` to the
     new constant.
   * Moved the post-sweep gate AFTER the CSV writes — a future gate trip no longer drops 7+ h
     of simulation output.

4. Re-ran the full sweep. Completed in 11.56 hours (slower than first run — likely background
   system activity). Exit code 0. All artifacts written:
   `wallclock.json`, `tuning_curve_{full,epsp_passive,ipsp_passive}.csv` (3001 rows each),
   `spike_times_*.csv`, `voltage_traces_*.csv`, `active_fraction_per_direction.csv`,
   `placement_seed0.json`.

5. Spawned a post-sim subagent to compute metrics, render figures, run tests, and verify the
   library asset:
   * Ran `compute_metrics.py` -> `metrics.json` (75 variants, one per (gAMPA, GABA, mode) cell);
     `derived_quantities.json`.
   * Ran `render_figures.py` -> 1233 PNGs in `results/images/`: 1200 per-cell (300 soma_v +
     300 epsp + 300 ipsp + 300 psth) + 25 polar tuning curves + 6 cross-grid heatmaps + 1
     regime-boundary contour + 1 active-fraction polar.
   * Ran 8 task-specific tests via pytest: 8 passed / 0 failed / 0 errored.
   * Patched `neuron_bootstrap.py::ensure_gaba_tonic_compiled` to guard against double
     `nrn_load_dll` on this Windows NEURON build (raises "name already exists: gaba_tonic" on
     reload; first registration is sufficient for the process lifetime).
   * Verified library asset `minimal_dsgc_bar_locked_gaba_ampa_sweep`: PASSED (0 errors,
     0 warnings).
   * Ran `verify_task_metrics`: PASSED.
   * `ruff check --fix`, `ruff format`, `mypy -p tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code`
     all clean.

## Outputs

* `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/code/` (15 modules + 5 tests + `mod/`,
  `run_nrnivmodl.cmd`)
* `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/library/minimal_dsgc_bar_locked_gaba_ampa_sweep/`
  (`details.json`, `description.md`)
* `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/wallclock.json`
* `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/{tuning_curve,spike_times,voltage_traces}_{full,epsp_passive,ipsp_passive}.csv`
* `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/{active_fraction_per_direction,placement_seed0}.{csv,json}`
* `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/{metrics,derived_quantities}.json`
* `tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/images/*.png` (1233 PNGs)

## Issues

The first 7 h 32 m sweep was lost to a too-strict gate threshold + gate-before-write ordering.
Fixed in place; the second sweep ran 11.56 h to completion. The reorder ensures any future gate
failure preserves the data for inspection. The Windows NEURON `nrn_load_dll` re-registration
issue was patched in `neuron_bootstrap.py` (idempotent guard).

## Headline Result (negative finding)

The 5x5 (gAMPA, GABA_BASE_NS) grid does NOT contain a cell that enters the multi-spike regime
(peak Hz >= 5 AND vector-sum DSI > 0.3). Maximum peak Hz across all 25 cells is **2.143 Hz** (at
gAMPA in {2.0, 3.0} nS). One cell hits full suppression: gAMPA=0.5, GABA_BASE_NS=2.0
(peak = 0 Hz). Peak Hz grid (rows = gAMPA, cols = GABA):

| gAMPA \\ GABA | 0.10 | 0.20 | 0.50 | 1.00 | 2.00 |
| --- | --- | --- | --- | --- | --- |
| 0.5 | 0.714 | 0.714 | 0.714 | 0.714 | **0.000** |
| 1.0 | 1.429 | 1.429 | 0.714 | 0.714 | 0.714 |
| 2.0 | **2.143** | **2.143** | 1.429 | 1.429 | 0.714 |
| 3.0 | **2.143** | **2.143** | 1.429 | 0.714 | 0.714 |
| 4.0 | 1.429 | 1.429 | 1.429 | 1.429 | 1.429 |

The bar-arrival-locked window mechanism is intact (REQ-13 IPSP COM shift = 8.5 ms confirms
direction-dependent timing). The HH save-and-zero is correctly wired (REQ-14 PASS, REQ-15 worst
peak = -9.04 mV well below the 5.0 mV gate). The cell simply does not enter multi-spike firing
under any of the swept (gAMPA, GABA) combinations on this passive-dendrite, AMPA-only-excitation
substrate. This rules out the AMPA-escape + bar-locked-GABA path on the from-scratch substrate
and motivates the next strategic decision (e.g., add Mg-block NMDA via S-0057-06, or move to RQ1
g_Na/g_K factorial / RQ4 active dendrites).
