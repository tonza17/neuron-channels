---
spec_version: "3"
task_id: "t0065_t0020_epsp_ipsp_vm_protocol"
step_number: 6
step_name: "implementation"
status: "completed"
started_at: "2026-04-30T08:12:18Z"
completed_at: "2026-04-30T08:25:00Z"
---
## Summary

Implemented `code/paths.py`, `code/constants.py`, `code/run_protocol.py`, and `code/plot_traces.py`.
Compiled the deposited model's `nrnmech.dll` inside the worktree, ran the six-trial sweep in 18
seconds, and produced five PNG plots from the resulting voltage_traces CSV. Headline result: FULL PD
= 15 spikes, FULL ND = 1 spike (DSI ≈ 0.875); EPSP_PASSIVE PD = ND (bit-identical, +28.6 mV peak
depolarisation); IPSP_PASSIVE flat at e_SACinhib = -60 mV in both directions (pure shunting, no
hyperpolarisation).

## Actions Taken

1. Wrote `code/paths.py` with `Path` constants for `DATA_DIR`, `RESULTS_DIR`, `IMAGES_DIR`,
   `VOLTAGE_TRACES_CSV`, `METRICS_JSON`, and the five PNG paths.
2. Wrote `code/constants.py` with `TrialMode` and `Condition` enums, integer `EXPTYPE_HH_ON = 1` /
   `EXPTYPE_HH_OFF = 2`, `GABA_MOD_PD = 0.33` / `GABA_MOD_ND = 0.99` / `GABA_MOD_OFF = 0`,
   excitatory off-values (`B_AMPA_OFF_NS`, `B_NMDA_OFF_NS`, `S_ACH_OFF_NS`, `ACH_MOD_OFF`),
   `S_GABA_OFF_NS`, `SEED = 1`, CSV column names, and metrics keys.
3. Wrote `code/run_protocol.py` implementing the six-trial driver. Direction is encoded purely via
   `h.gabaMOD` (matches t0020). Per-mode overrides:
   * `FULL`: `h.exptype = 1` (HH on), no other override.
   * `EPSP_PASSIVE`: `h.exptype = 2` (HH off), `h.gabaMOD = 0`, `h.s2ggaba = 0` (silence GABA).
   * `IPSP_PASSIVE`: `h.exptype = 2` (HH off), `h.b2gampa = 0`, `h.b2gnmda = 0`, `h.s2gach = 0`,
     `h.achMOD = 0` (silence both bipolar AMPA/NMDA and SAC ACh excitation). Then
     `h("init_active()")`, `h("update()")`, `h("placeBIP()")`, attach Vm + t recorders (and a NetCon
     spike threshold for FULL trials only), `h.finitialize(V_INIT_MV)`, `h.continuerun(TSTOP_MS)`.
     Per-trial `_assert_bip_positions_baseline` guard reused from t0020.
4. Wrote `code/plot_traces.py` reading the CSV with pandas explicit dtypes; emits five PNGs (FULL /
   EPSP / IPSP per-mode PD-vs-ND; PD and ND three-mode overlays).
5. **Build fix**: the worktree's `tasks/t0008_port_modeldb_189347/build/modeldb_189347/` directory
   was empty (worktrees do not inherit build artefacts). Ran
   `tasks/t0008_port_modeldb_189347/code/run_nrnivmodl.cmd` against the deposited `sources/` to
   compile a fresh `nrnmech.dll` (228 KB) inside the worktree.
6. **Run 1 (initial)**: simplerun() not present in t0008's GUI-free HOC. AttributeError on
   `h.simplerun`. Rewrote the trial driver to use the
   `apply_params -> init_active -> update -> placeBIP -> finitialize -> continuerun` chain directly
   (matches t0020/t0008 practice).
7. **Run 2 (loose silencing)**: IPSP_PASSIVE showed +4 mV residual depolarisation. Diagnosed as SAC
   cholinergic excitatory leakage (`achMOD = 0.25` is set by `apply_params` but I had only zeroed
   `b2gampa`/`b2gnmda`). Added `h.s2gach = 0` and `h.achMOD = 0` to the IPSP_PASSIVE branch and
   `h.s2ggaba = 0` to the EPSP_PASSIVE branch for symmetric belt-and-braces silencing.
8. **Run 3 (strict silencing)**: clean output. IPSP_PASSIVE peak ≈ -60 mV in both directions (the
   inhibitory reversal e_SACinhib = -60); EPSP_PASSIVE bit-identical PD vs ND; FULL shows robust
   DSI.
9. Ran `code/plot_traces.py` to emit five PNGs from the 60,006-sample CSV.
10. Verified `ruff check`, `ruff format`, `mypy -p tasks.t0065_t0020_epsp_ipsp_vm_protocol.code` all
    pass with no errors.

## Outputs

* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/paths.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/constants.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/plot_traces.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/data/voltage_traces.csv` (~2.0 MB, 60,006 rows)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/metrics.json`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/vm_full_pd_vs_nd.png` (~92 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/epsp_pd_vs_nd.png` (~74 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/ipsp_pd_vs_nd.png` (~43 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/three_mode_pd_overlay.png` (~89 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/three_mode_nd_overlay.png` (~72 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/logs/commands/*.json` (run_with_logs metadata for the
  sweep and plot scripts)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/logs/steps/006_implementation/step_log.md`

## Issues

Three iterations were needed before the sweep produced clean output: a missing `nrnmech.dll` in the
worktree, an `AttributeError: 'hoc.HocObject' object has no attribute 'simplerun'` caused by relying
on a HOC proc that t0008's GUI-free derivative removed, and SAC cholinergic excitatory leakage in
IPSP_PASSIVE that required also zeroing `achMOD` and `s2gach`. All three were diagnosed and fixed;
the final run is clean and physiologically interpretable.
