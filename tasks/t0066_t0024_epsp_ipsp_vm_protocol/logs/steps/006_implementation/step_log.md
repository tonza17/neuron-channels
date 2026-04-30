---
spec_version: "3"
task_id: "t0066_t0024_epsp_ipsp_vm_protocol"
step_number: 6
step_name: "implementation"
status: "completed"
started_at: "2026-04-30T16:01:51Z"
completed_at: "2026-04-30T17:36:30Z"
---
## Summary

Implemented `code/{paths,constants,run_protocol,plot_traces}.py`, ran the 120-trial sweep (6 cells
× 20 trials × ~30 s/trial avg = ~30 min FULL + ~15 min EPSP + ~15 min IPSP ≈ 60 min wall-clock),
and emitted six PNG plots from the resulting voltage_traces CSV (1.2M samples, ~85 MB on disk
pre-compress). Headline result: FULL DSI = **0.7391** (matches t0024's 0.776 12-angle correlated
reference within sampling noise); IPSP_PASSIVE peak Vm = -59.62 mV in BOTH PD and ND (flat at e_GABA
= -60 mV, exactly as predicted from research-code finding § 6 — **confirms cross-model design
convergence**: both Poleg-Polsky 2016 and de Rosenroll 2026 pin e_GABA = v_rest, producing pure
shunting inhibition).

## Actions Taken

1. Wrote `code/paths.py` with `Path` constants for DATA_DIR, RESULTS_DIR, IMAGES_DIR, the CSV/JSON
   outputs, the six PNG paths, and a path-import for t0065's voltage_traces.csv (used by the
   cross-model comparison plot).
2. Wrote `code/constants.py` with `TrialMode` and `Condition` `StrEnum`s, direction angles (PD =
   0°, ND = 180°), `N_TRIALS_PER_CELL = 20`, `SEED_BASE = 1`, `RHO_CORRELATED = 0.6`, CSV column
   names, registered metric key, and `BASELINE_WINDOW_MS = 50`.
3. Wrote `code/run_protocol.py`:
   * Imports `build_dsgc_cell`, `_setup_synapses`, `_bar_arrival_times`, `_gaba_prob_for_direction`,
     `_rates_with_ar2_noise`, `_rates_to_events`, `_count_spikes`, `BASE_ACH_PROB`, `RATE_DT_MS`
     from t0024 (same cross-task import precedent as t0065 importing from t0008).
   * Adds idempotent `_ensure_neuron_loaded()` that monkey-patches t0024's `load_neuron` to return
     cached `h` after the first call (NEURON's `nrn_load_dll` cannot be called twice).
   * Builds the cell + synapses **once** at the start of main; snapshots canonical NetCon weights
     and HHst conductances (`gnabar`, `gkbar`, `gkmbar` per segment) into a `CanonicalState`
     dataclass.
   * Per-trial loop: restore canonical state → apply mode override (silence GABA NetCons or ACh
     NetCons; zero HHst conductances on every section for HH-off modes) → generate AR(2) noise +
     Poisson events → schedule via `FInitializeHandler` → run → capture Vm + t into numpy
     arrays.
   * Computes `peak_v_mv`, `baseline_v_mv` (mean over first 50 ms), `peak_minus_baseline_mv`,
     `spike_count` (FULL only; via post-hoc threshold crossings).
   * Writes long-format CSV incrementally per trial; writes per_trial_metrics.json incrementally so
     a crash mid-sweep preserves data.
   * Computes `direction_selectivity_index` from FULL trial-mean spike counts and writes
     `results/metrics.json`.
4. Wrote `code/plot_traces.py`:
   * Reads CSV with explicit dtypes via pandas.
   * `_trial_mean_iqr` pivots per-(mode, direction) traces to (n_samples, n_trials), then computes
     mean and 25/75 percentiles per timepoint.
   * Emits 6 PNGs: per-mode 2-panel (PD vs ND with IQR shading), three-mode PD overlay, three-mode
     ND overlay, and the cross-model t0065-vs-t0066 IPSP_PASSIVE comparison (left panel reads
     t0065's voltage_traces.csv; right panel uses this task's data).
5. **Smoke iteration 1**: built cell per trial → `nrn_load_dll` failure on second trial ("user
   defined name already exists: Exp2NMDA"). Fixed by adding `_ensure_neuron_loaded`.
6. **Smoke iteration 2**: cell builder still failed on second trial because `RGCmodelGD.hoc::DSGC`
   template was already defined. Fixed by switching to **build cell once, restore state per trial**
   strategy (CanonicalState dataclass).
7. **Smoke iteration 3**: 6/6 trials clean. FULL/PD = 5 spikes, FULL/ND = 1 spike, EPSP_PASSIVE peak
   ~-3 mV, IPSP_PASSIVE flat at -60 mV in both directions. Predictions confirmed.
8. **Full sweep**: ran 120 trials in background. Per-trial wall-clock varied: FULL trials slower
   (~60 s due to spike-driven integration), EPSP/IPSP trials faster (~15-30 s). Total ~60 min.
9. Generated 6 PNGs from the 1,200,120-sample CSV. Plot script ran in <2 s.
10. Verified `ruff check`, `ruff format`, `mypy -p tasks.t0066_t0024_epsp_ipsp_vm_protocol.code` all
    pass with no errors.

## Outputs

* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/paths.py`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/constants.py`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/plot_traces.py`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/data/voltage_traces.csv` (4.2 MB, 120,120 rows after 1 ms
  subsample from 0.1 ms simulation dt — see CSV size note in Issues)
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/data/per_trial_metrics.json` (120 entries)
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/metrics.json`
  (`direction_selectivity_index = 0.7391`)
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/vm_full_pd_vs_nd.png`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/epsp_pd_vs_nd.png`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/ipsp_pd_vs_nd.png`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/three_mode_pd_overlay.png`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/three_mode_nd_overlay.png`
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/comparison_t0065_vs_t0066_ipsp.png`

## Issues

Three smoke iterations were needed (mirroring t0065's three-iteration debugging history): (1)
`nrn_load_dll` cannot be called twice in one process; (2) the HOC template `DSGC` was already
defined on second cell build. Both were resolved by switching from "rebuild cell per trial" to
"build cell once, restore canonical state per trial" — which has the additional benefit of being
substantially faster than the t0024 baseline (the per-trial cell-build cost ~3-5 s is amortised over
120 trials).

**CSV size**: the original 0.1 ms-resolution sweep produced an 85 MB `voltage_traces.csv` (1,200,120
rows × 5 columns). This exceeds the 5 MB pre-merge gate (PM-E011). Resolved by subsampling the
saved CSV to 1 ms resolution (every 10th sample, 120,120 rows, 4.2 MB) — `peak_v_mv` and
`spike_count` per trial are computed from the FULL 0.1 ms trace before subsampling, so
`per_trial_metrics.json` is unaffected. Updated `code/run_protocol.py::_append_trace_rows` to
subsample on write via the new `CSV_SUBSAMPLE_STRIDE` constant for reproducibility on future
re-runs.
