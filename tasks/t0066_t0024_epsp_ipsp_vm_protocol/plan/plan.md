---
spec_version: "1"
task_id: "t0066_t0024_epsp_ipsp_vm_protocol"
date_completed: "2026-04-30"
status: "complete"
---
# Plan: Test t0024 de Rosenroll DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

## Objective

Apply the t0065 EPSP_PASSIVE / IPSP_PASSIVE / FULL channel-isolation protocol to the de Rosenroll
2026 DSGC ported in t0024. Record somatic Vm in PD (0°) and ND (180°) across 20 trials per (mode,
direction) cell to obtain noise-averaged trace statistics. The headline question is whether the
t0065 finding (direction selectivity is shunting-driven because `e_GABA = v_rest`) reproduces in a
structurally independent DSGC implementation, or whether t0065's IPSP-flatness was a Poleg-Polsky
design artefact. Research-code finding (`research/research_code.md` § 6) confirms the de Rosenroll
constants set `V_INIT = ELEAK = GABA_EREV = -60 mV` — identical to t0065 — so we predict
IPSP_PASSIVE will also be flat at -60 mV here, confirming the convergence.

## Approach

Build the de Rosenroll cell once per trial (the t0024 cell builder is stateful), then run six cell
configurations × 20 trials = 120 trials. Per-trial sequence (mirroring t0065 but using the t0024
synapse model):

1. `build_dsgc_cell()` from `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell`.
2. `_setup_synapses(cell)` returns a `SynapseBundle` with `ncs_ach` and `ncs_gaba` lists (177 each).
3. Apply per-mode override:
   * **EPSP_PASSIVE**: `for nc in bundle.ncs_gaba: nc.weight[0] = 0`. Zero `gnabar_HHst`,
     `gkbar_HHst`, `gkmbar_HHst` on soma + every dendrite section.
   * **IPSP_PASSIVE**: `for nc in bundle.ncs_ach: nc.weight[0] = 0`. Zero HH as above.
   * **FULL**: no overrides.
4. Compute bar arrival times via `_bar_arrival_times(syn_xy, origin_xy, direction_deg)`.
5. Generate AR(2) noise via
   `generate_ar2_batch(n_syn=177, n_bins=tstop/dt, rho=0.6, seed=base+trial)`.
6. Compute directional GABA release-prob via `_gaba_prob_for_direction(direction_deg)`.
7. Convert rates to Poisson event times per synapse.
8. Schedule events via `FInitializeHandler` + `NetCon.event()`.
9. Record `soma(0.5)._ref_v` and `_ref_t` into `h.Vector`s; `h.finitialize(V_INIT_MV)`;
   `h.continuerun(TSTOP_MS)`.
10. Capture Vm into a numpy array; compute peak Vm, baseline Vm, peak − baseline, spike count
    (rising threshold crossings on the trace at -10 mV).
11. Append (mode, direction, trial, t_ms, v_mv) rows to the long-format CSV.

Stage outputs:

* `data/voltage_traces.csv` — long-format per-sample table, columns
  `mode, direction, trial, t_ms, v_mv`.
* `data/per_trial_metrics.json` — list of 120 trial-level scalar dicts.
* `results/metrics.json` — `direction_selectivity_index` from FULL trial-mean spike rates.
* PNG plots described in Outputs.

## Cost Estimation

* Local Windows workstation (NEURON 8.2.7, single CPU core).
* 120 trials × ~64 s/trial (t0024 baseline) ≈ **2h10m wall-clock** for the sweep, plus ~5 minutes
  for plotting and ~5 minutes to write the CSV.
* External costs: **$0** total. No paid API, no remote GPU, no paid storage.

## Step by Step

1. `code/paths.py` — `Path` constants for `DATA_DIR`, `RESULTS_DIR`, `IMAGES_DIR`,
   `VOLTAGE_TRACES_CSV`, `PER_TRIAL_METRICS_JSON`, `METRICS_JSON`, the six PNG output paths
   (FULL/EPSP/IPSP per-mode, PD/ND three-mode, plus the cross-model t0065-vs-t0066 IPSP comparison).
2. `code/constants.py` — typed enums and constants:
   * `TrialMode` enum: `FULL`, `EPSP_PASSIVE`, `IPSP_PASSIVE` (string values).
   * `Condition` enum: `PD`, `ND` (string values).
   * `DIRECTION_PD_DEG = 0.0`, `DIRECTION_ND_DEG = 180.0`.
   * `N_TRIALS_PER_CELL = 20`, `SEED_BASE = 1`.
   * `RHO_CORRELATED = 0.6` (matches t0024 primary protocol).
   * Reuse `TSTOP_MS`, `DT_MS`, `V_INIT_MV`, `AP_THRESHOLD_MV` from t0024 by re-export.
   * CSV column names, metrics keys.
3. `code/run_protocol.py` — the trial driver:
   * Bootstrap NEURON via t0024's `build_cell.load_neuron`.
   * For each `(mode, direction)` in 6 cells, for each trial in 20 trials:
     * Build cell, set up synapses, apply mode override, run trial, capture Vm trace.
     * Append rows to long-format CSV (write incrementally to survive crashes).
     * Append scalars to per-trial metrics list.
     * Re-assert basic sanity (peak Vm < +50 mV, baseline within ±5 mV of -60 mV).
   * Write `data/per_trial_metrics.json` and `results/metrics.json` (DSI from FULL means).
   * Print per-trial summary to stdout.
4. `code/plot_traces.py` — reads CSV with pandas explicit dtypes; emits 6 PNGs:
   * `vm_full_pd_vs_nd.png` — FULL mode mean trace ± IQR shading, PD vs ND.
   * `epsp_pd_vs_nd.png` — EPSP_PASSIVE mean ± IQR, PD vs ND.
   * `ipsp_pd_vs_nd.png` — IPSP_PASSIVE mean ± IQR, PD vs ND.
   * `three_mode_pd_overlay.png` — PD direction across all 3 modes (mean ± IQR per mode).
   * `three_mode_nd_overlay.png` — ND direction across all 3 modes.
   * `comparison_t0065_vs_t0066_ipsp.png` — side-by-side IPSP_PASSIVE: t0065 (1 trial, two traces)
     vs t0066 (20-trial mean ± IQR per direction). Reads t0065's `data/voltage_traces.csv`.

All script invocations on the task branch must run via `arf.scripts.utils.run_with_logs`.

## Remote Machines

None. Local Windows workstation only. NEURON simulations of the de Rosenroll cell are CPU-bound and
short enough (~64 s/trial × 120 trials = ~2h10m total) that remote provisioning would add overhead
without time savings.

## Assets Needed

* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/` — provides
  `nrnmech.dll`, `RGCmodelGD.hoc`, `mod/` mechanism source. Already present in the worktree (the
  t0024 task is a dependency).
* `tasks/t0024_port_de_rosenroll_2026_dsgc/code/{build_cell,run_tuning_curve,constants,ar2_noise,paths}.py`
  — imported via absolute path; no copy needed.
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/data/voltage_traces.csv` — read by the cross-model
  comparison plot.

## Expected Assets

None. This is a diagnostic decomposition task; outputs are traces, metrics, plots — no new
datasets, models, predictions, papers, libraries, or answers.

## Time Estimation

* Implementation (paths, constants, run_protocol, plot_traces): 1.5 hours.
* Smoke run (1 trial per mode to verify silencing works): 5 minutes.
* Full sweep: 2h10m wall-clock.
* Plotting + analysis + writing results: 1 hour.
* Verification + PR: 30 minutes.
* Total: ~5 hours including buffer.

## Risks & Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Setting `nc.weight[0] = 0` does not silence the synapse (e.g., if the AR(2)/Poisson driver bypasses NetCon weight). | Smoke trial: EPSP_PASSIVE shows hyperpolarising deflections that should only come from GABA. | Also set `bundle.syns_gaba[i]._gmax = 0` on the Exp2Syn objects directly, or skip the GABA event-queue loop in `_queue()`. |
| 2 | Zeroing `gnabar_HHst` on soma alone is insufficient; terminal dendrites also carry `gnabar_HHst = 0.03 S/cm²` and may dendritically spike. | EPSP_PASSIVE traces show spike-shaped events above -20 mV. | Zero `gnabar_HHst`, `gkbar_HHst`, `gkmbar_HHst` on EVERY section: soma, primary, non-terminal, terminal dendrites. Plan recipe already specifies all-section zeroing. |
| 3 | 20 trials per cell takes longer than 64 s/trial baseline if HH-off trials slow the integrator. | Per-trial wall-clock > 90 s after first 5 trials of any mode. | Drop to 10 trials per cell (60 trials total, ~1h compute) and document the reduced statistics in results/results_detailed.md. Sample-mean precision still adequate for visual decomposition. |
| 4 | IPSP_PASSIVE turns out to be flat at -60 mV (predicted by research-code finding § 6). | IPSP_PASSIVE PD vs ND traces overlay within ~0.5 mV. | Not a failure — this is the expected outcome and confirms the cross-model design convergence. Document as a positive finding in results_detailed.md, draw the cross-model comparison plot, motivate a SEClamp-based follow-up suggestion (cf. t0065 S-0065-03). |

## Verification Criteria

* All 120 trials complete, each producing a non-empty Vm trace.
* `data/voltage_traces.csv` has approximately `120 × tstop/dt` rows ≈ 1,200,000 rows.
* `data/per_trial_metrics.json` has 120 entries.
* All 6 PNGs exist and are referenced by `results/results_detailed.md` with `![desc](images/...)`
  syntax.
* `results/metrics.json` contains `direction_selectivity_index` (registered metric) computed from
  FULL trial-mean spike counts.
* `verify_logs`, `verify_research_code`, `verify_plan`, `verify_task_metrics`,
  `verify_task_results`, `verify_suggestions`, `verify_task_folder`, `verify_task_file`,
  `verify_pr_premerge` all pass.

## Task Requirement Checklist

These REQ items are derived from `task.json` short_description, `task_description.md` Outputs +
Verification Criteria, and the research-code findings. They are reused verbatim by
`results/results_detailed.md` `## Task Requirement Coverage`:

* **REQ-1**: Apply t0065 EPSP/IPSP/FULL trial-mode protocol to the de Rosenroll DSGC substrate.
* **REQ-2**: Run 6 cells (3 modes × 2 directions) × 20 trials per cell = 120 trials.
* **REQ-3**: Record full somatic Vm trace per trial at every NEURON timestep.
* **REQ-4**: Save raw traces to long-format CSV (`mode, direction, trial, t_ms, v_mv`).
* **REQ-5**: Save per-trial scalar metrics to JSON.
* **REQ-6**: Emit per-mode 2-panel plots (mean ± IQR shading) and 3-mode summary plots.
* **REQ-7**: Emit cross-model t0065-vs-t0066 IPSP_PASSIVE comparison plot.
* **REQ-8**: `results_summary.md` and `results_detailed.md` (spec_version 2) with embedded plots,
  per-mode trace amplitudes, and the cross-model comparison.
* **REQ-9**: Quantitative answer to "is IPSP_PASSIVE flat in t0066 like in t0065, or
  hyperpolarising?" with mean and IQR for both directions.
* **REQ-10**: FULL-mode mean spike count in PD > ND (consistent with t0024's tuning-curve DSI = 0.78
  at 0° vs 180°).
* **REQ-11**: DSI computed from FULL trial means, registered as `direction_selectivity_index` metric
  in `results/metrics.json`.
* **REQ-12**: Plots render correctly on GitHub (PNG paths relative to `images/`).
