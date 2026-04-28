---
spec_version: "3"
task_id: "t0055_nmda_mg_block_dsi_recovery"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-28T11:15:28Z"
completed_at: "2026-04-28T13:42:00Z"
---
## Summary

Forked the t0054 codebase to t0055, authored `code/mod/NMDA_MgBlock.mod` implementing the
Jahr-Stevens Boltzmann Mg-block (n=0.25 / mM, gamma=0.08 / mV, Voff=0), wired the new MOD into
`neuron_bootstrap.py` via an nrnivmodl shim, replaced the NMDA `Exp2Syn` in `synapses.py` with
`h.NMDA_MgBlock`, ran all four validation gates (V_rest, voltage-dep sanity at 6 SEClamp voltages,
placement bit-identity vs t0054, gabaMOD scalar), executed the full 1440-trial sweep (1h 58m
wall-clock, ~5 s/trial), computed 12 multi-variant metrics, rendered 252 PNGs, and built the
`minimal_dsgc_mg_block_nmda` library asset. Headline result: **Mg block recovers DSI** at gNMDA ≥
0.25 nS — vector-sum DSI = 0.7464 (vs t0054's 0.082, a 9× recovery and bit-identical to gNMDA =
0). However, **peak Hz stays at 0.667 Hz** at every gNMDA value in FULL mode because the Mg block is
so effective at V_rest = -65 mV that NMDA never unblocks under the scalar gabaMOD inhibition. The
S-0054-01 pass criterion fails on the peak-Hz half (>= 5 Hz required, 0.667 measured). Cross-task
regression vs t0054 gNMDA = 0 baseline passed at 0.000e+00 Hz max diff across 120 rows.

## Actions Taken

1. Spawned an implementation subagent that (a) forked the t0054 codebase with the import-path
   rewrite and bootstrap-sentinel rename, (b) authored `code/mod/NMDA_MgBlock.mod` with the
   Jahr-Stevens Boltzmann gating equation, (c) wired `nrnivmodl` compilation into
   `neuron_bootstrap.py`, (d) extended `constants.py` with the Mg-block parameter constants, (e) ran
   the 4 validation gates (all passed), (f) launched the 1440-trial sweep.
2. Monitored the sweep via wakeup loop; sweep completed at 14:34 UTC after 1h 58m wall-clock.
3. Ran `compute_metrics.py` via `run_with_logs.py` — gNMDA = 0 cross-task regression gate passed
   at 0.000e+00 Hz, all 12 multi-variant metrics written, S-0054-01 pass criterion evaluated as
   PASS=False.
4. Ran `render_figures.py` via `run_with_logs.py` — 252 PNGs written under `results/images/`.
5. Verified the library asset structure (`details.json`, `description.md`, `sources/`), metrics JSON
   via `verify_task_metrics.py` (PASSED), and task folder structure via `verify_task_folder.py`
   (PASSED with 1 minor warning).

## Outputs

* `tasks/t0055_nmda_mg_block_dsi_recovery/code/` — 12 forked Python modules + 4 new files
  (`mod/NMDA_MgBlock.mod`, `run_nrnivmodl.cmd`, `test_nmda_mg_block_voltage_dep.py`,
  `test_placement_seed0_match.py`)
* `tasks/t0055_nmda_mg_block_dsi_recovery/assets/library/minimal_dsgc_mg_block_nmda/` — library
  asset with `details.json` (12 modules, 8 entry points), `description.md`, and
  `sources/NMDA_MgBlock.mod`
* `tasks/t0055_nmda_mg_block_dsi_recovery/results/` — `metrics.json` (12 variants),
  `derived_quantities.json` (per-variant + per-gNMDA), `placement_seed0.json`,
  `mg_block_g_v_empirical.json`, `wallclock.json`, `tuning_curve_{full,e_only,gaba_only}.csv`,
  `voltage_traces_*.csv`, `spike_times_*.csv`, `activation_times.csv`, plus `images/` with 252 PNGs

## Issues

The S-0054-01 pass criterion fails on the peak-Hz half. This is a **meaningful negative result**,
not an implementation bug:

* Mg-block NMDA correctly recovers DSI to 0.7464 at every gNMDA value (a 9× recovery vs t0054's
  voltage-independent 0.082).
* In FULL mode, peak rate stays at the t0054 / t0052 baseline of 0.667 Hz (one spike per trial) for
  every gNMDA value because the scalar gabaMOD (PD = 0.33 × 2 nS, ND = 0.99 × 2 nS) prevents the
  soma from depolarising above the Mg-unblock threshold.
* In E_ONLY mode (no inhibition), the cell goes from 1 to 2 spikes per trial when gNMDA >= 0.25 nS,
  demonstrating the NMDA conductance does activate when the cell can reach unblocking voltage.
* This rules out the simple PolegPolsky2016 hypothesis "Mg block alone restores DSI without cost to
  peak rate" in this minimal architecture and motivates the joint (gAMPA, gNMDA, gGABA) sweep
  proposed in S-0054-02.

The user (mailto:a.nikolaev@sheffield.ac.uk) flagged a separate protocol issue mid-execution: the
EPSP / IPSP traces in t0054 (and inherited here) record V(t) with HH still active on soma + AIS, so
the "EPSP" panels are spiking traces, not pure synaptic envelopes. This has been saved as a
project-wide feedback memory (`feedback_dsgc_measurement_protocol.md`) and must be applied to all
future DSGC tasks. It is **not** retroactively applied to t0055 — the t0054 protocol was inherited
verbatim per the original plan, and a corrected re-run is a follow-up task (covered by a new
suggestion generated in step 14).
