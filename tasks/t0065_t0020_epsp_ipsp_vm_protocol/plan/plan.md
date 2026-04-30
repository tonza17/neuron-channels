---
spec_version: "1"
task_id: "t0065_t0020_epsp_ipsp_vm_protocol"
date_completed: "2026-04-30"
status: "complete"
---
# Plan: Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

## Objective

Decompose the somatic voltage trace of the deposited Poleg-Polsky & Diamond 2016 ModelDB 189347 DSGC
into pure-excitatory (EPSP_PASSIVE: HH off, GABA off) and pure-inhibitory (IPSP_PASSIVE: HH off,
AMPA + NMDA off) components in PD and ND directions, and record the full HH-on Vm (FULL) for
reference. Outcome: a six-trace dataset that lets us read the EPSP and IPSP shapes at the soma in
both directions, comparable against the from-scratch family's binary-regime traces from t0059.

## Approach

Build the deposited cell once, then run six trials. Each trial follows the four-step
override-then-rerun pattern established in `t0049_seclamp_cond_remeasure/code/run_seclamp.py`:

1. `apply_params(h, seed=1)` writes canonical paper conductances and the random-stream seed.
2. Set `h.SpikesOn` to `1` (FULL) or `0` (passive modes) so that the deposited `simplerun()` proc
   binds `exptype = 2 - SpikesOn` and `init_active()` decides HH state correctly.
3. Call `h.simplerun(int(EXPTYPE_CONTROL), int(direction))` with `direction = 0` (PD) or `1` (ND);
   discard the run.
4. Apply the per-mode override:
   * `EPSP_PASSIVE`: `h.gabaMOD = 0.0` (silence inhibitory drive).
   * `IPSP_PASSIVE`: `h.b2gampa = 0.0`, `h.b2gnmda = 0.0` (silence excitatory drive).
   * `FULL`: no override — accept the canonical values that simplerun just wrote.
5. Re-call `h("update()")` and `h("placeBIP()")` so the synaptic point processes pick up the
   overridden conductance globals.
6. Attach fresh `h.Vector` recorders for `h.RGC.soma(0.5)._ref_v` and `h._ref_t`. Attach a
   threshold-crossing spike recorder via `h.NetCon` for FULL trials only.
7. Call `h.finitialize(V_INIT_MV)` and `h.continuerun(TSTOP_MS)`. Record the trace.

Stage outputs:

* Long-format trace CSV `data/voltage_traces.csv` with columns `(mode, direction, t_ms, v_mv)`.
* Per-trial scalar metrics JSON `results/metrics.json` listing per-trial `peak_v_mv`,
  `baseline_v_mv`, `peak_minus_baseline_mv`, `spike_count` (FULL only), and `n_samples`.
* Per-mode 2-panel PNG plots (PD overlaid with ND) and 3-mode overlays.

## Cost Estimation

* Local Windows workstation. NEURON DSGC-189347 model under canonical parameters runs at roughly 1.5
  minutes wall-clock per trial (matches t0020 timing). Six trials → ~10 minutes simulation time.
* External costs: **$0** total. No paid API calls, no remote GPU rental, no paid storage. The task
  uses only local CPU compute and pre-installed open-source NEURON.

## Step by Step

The implementation lives in `code/`:

1. `code/paths.py` — `Path` constants for `DATA_DIR`, `IMAGES_DIR`, `VOLTAGE_TRACES_CSV`,
   `METRICS_JSON`, and the four PNG output paths.
2. `code/constants.py` — typed constants:
   * `TrialMode` enum: `FULL`, `EPSP_PASSIVE`, `IPSP_PASSIVE` (string values used in the CSV).
   * `Condition` enum: `PD`, `ND` (string values used in the CSV).
   * Direction integer codes for `simplerun`'s second arg: `DIRECTION_PD_INT = 0`,
     `DIRECTION_ND_INT = 1`.
   * `EXPTYPE_CONTROL_INT = 1` (for `simplerun`'s first arg).
   * `GABA_MOD_PD = 0.33`, `GABA_MOD_ND = 0.99`, `GABA_MOD_OFF = 0.0`, `B_AMPA_OFF_NS = 0.0`,
     `B_NMDA_OFF_NS = 0.0`, `SEED = 1`.
   * Column names: `MODE_COLUMN`, `DIRECTION_COLUMN`, `T_MS_COLUMN`, `V_MV_COLUMN`.
3. `code/run_protocol.py` — the trial driver:
   * Bootstrap NEURON via `t0008.code.build_cell.load_neuron`.
   * Build the cell once, snapshot synapse coords.
   * For each `(mode, direction)` in the six-trial plan, run the four-step override-then-rerun
     pattern, copy the trace into a list, and re-assert BIP positions.
   * Write the long-format CSV at `data/voltage_traces.csv`.
   * Write per-trial scalar metrics to `results/metrics.json`.
   * Print a per-trial summary to stdout for sanity checking.
4. `code/plot_traces.py` — reads the CSV and emits PNGs:
   * `vm_full_pd_vs_nd.png` — FULL mode, PD vs ND.
   * `epsp_pd_vs_nd.png` — EPSP_PASSIVE, PD vs ND (expected to overlay).
   * `ipsp_pd_vs_nd.png` — IPSP_PASSIVE, PD vs ND.
   * `three_mode_pd_overlay.png` — all three modes for PD on one axis.
   * `three_mode_nd_overlay.png` — all three modes for ND on one axis.

All script invocations on the task branch must run via
`uv run python -m arf.scripts.utils.run_with_logs`.

## Remote Machines

None. The full protocol runs on the local Windows workstation. NEURON simulations of the DSGC-189347
cell are CPU-bound and short enough (~1.5 minutes/trial, six trials total) that remote provisioning
would add overhead without time savings. No GPU is required for any stage.

## Assets Needed

The deposited DSGC source files at `tasks/t0008_port_modeldb_189347/code/sources/` and the compiled
`nrnmech.dll` produced by `code/run_nrnivmodl.cmd` (already present in this repo from t0007/t0008
setup).

## Expected Assets

None. This is a diagnostic decomposition task; outputs are traces, metrics, and plots — no new
datasets, models, predictions, papers, libraries, or answers.

## Time Estimation

* Implementation (code + paths + constants): 1 hour.
* Six-trial sweep: ~10 minutes.
* Plotting: 15 minutes.
* Reporting (results, suggestions): 30 minutes.
* Verification + PR: 15 minutes.
* Total: ~2 hours including buffer.

## Risks & Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | `b2gampa = 0` + `b2gnmda = 0` does not actually silence excitatory drive (deposited HOC may have additional hooks). | IPSP_PASSIVE trace shows depolarising contamination above the inhibitory `e_SACinhib` reversal. | Also set `h.nmdaOn = 0` and `h.flickerVAR = 0` and re-run. |
| 2 | `SpikesOn = 0` does not fully suppress HH (e.g., `RGCdendna` stays nonzero per `init_active`). | Passive-mode trace shows a spike-shaped depolarisation above -20 mV. | Directly write `h.RGCsomana = 0` and `h.RGCdendna = 0` after `apply_params` and re-call `h("update()")`. |
| 3 | `simplerun`'s randomisation of BIP synapses makes EPSP_PASSIVE PD and EPSP_PASSIVE ND traces non-identical despite both having `gabaMOD = 0`. | The two traces fail a `np.allclose` check. | Acceptable — the deposited model uses direction-coupled stimulus timing in `placeBIP`, so PD and ND can diverge even with no inhibition. Document in the results file rather than treat as a bug. |

## Verification Criteria

* All six trials complete, each producing a non-empty Vm trace.
* Per-trial assertion `assert_bip_positions_baseline` succeeds — no rotation re-engagement.
* `data/voltage_traces.csv` has approximately `6 × tstop / dt` rows (~`6 × 14001` samples for
  default `tstop = 1400 ms` and `dt = 0.1 ms`).
* `results/metrics.json` has six entries.
* All five PNGs exist and are referenced by `results_detailed.md` with `![desc](images/...)` syntax.
* `verify_logs`, `verify_step_tracker`, `verify_research_code`, and `verify_pr_premerge` all pass.
