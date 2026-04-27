---
spec_version: "3"
task_id: "t0053_minimal_dsgc_spatial_gaba"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-27T13:02:46Z"
completed_at: "2026-04-27T13:50:31Z"
---
# implementation

## Summary

Ran the 12-direction x 10-trial x 3-mode (FULL, AMPA_ONLY, GABA_ONLY = 360 trials total)
spatial-centripetal-gating sweep to completion in 17 min 11 s, computed per-mode tuning-curve
metrics with the new soft active-fraction sanity check, rendered 63 result PNGs (the 12-direction
v_soma / EPSP / IPSP / PSTH / activation panels plus polar, Cartesian, and the new active-fraction
polar plot), and validated the library asset and `metrics.json` against their respective
verificators with zero errors and zero warnings. Ruff and mypy checks pass on the task package. Mean
active fraction = 0.5000 lands exactly on the centre of the soft band.

## Actions Taken

1. Launched the 360-trial sweep via
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0053_minimal_dsgc_spatial_gaba -- uv run python -u tasks/t0053_minimal_dsgc_spatial_gaba/code/run_tuning_curve.py`
   in the background (Bash `run_in_background=true`) so the harness 10-min hard timeout would not
   kill the long-running NEURON simulation. Sweep wall-clock = 1031.2 s (17 min 11 s) for 360 trials
   at ~2.9 s per trial under CVODE adaptive step. Outputs:
   `tuning_curve_{full,ampa_only,gaba_only}.csv` (120 rows each), `voltage_traces_*.csv`,
   `spike_times_*.csv` (FULL is header-only because spiking is fully suppressed by spatial
   inhibition), `activation_times.csv` (1,200 data rows with the new `is_fired` column), and
   `active_fraction_per_direction.csv` (12 rows). The dry-run gate at theta=0 reported
   `i_active_fraction = 0.360` which is inside the per-angle dry-run band `[0.3, 0.7]`.
2. Ran `compute_metrics.py` -> `results/metrics.json` (registered keys only: DSI, HWHM, reliability,
   RMSE) and `results/derived_quantities.json` (peak Hz, null Hz, vector-sum DSI, preferred
   direction, per-direction aggregate EPSP / IPSP peaks, and the active-fraction soft sanity block).
   Mean active fraction = 0.5000 lies exactly inside `[0.4, 0.6]`; per-direction values range from
   0.34 (theta=30) to 0.66 (theta=210), demonstrating the spatial mechanism's asymmetry. The check
   printed an informational summary (no warning fired).
3. Ran `render_figures.py` to produce 63 PNGs under `results/images/`: 12 soma V(t), 12 aggregate
   EPSP (AMPA_ONLY), 12 aggregate IPSP (GABA_ONLY), 12 PSTH (5 ms bins), 12 synapse activation-time
   histograms, polar tuning curve, Cartesian tuning curve, and the new `active_fraction_polar.png`
   (REQ-21).
4. Ran `meta.asset_types.library.verificator` on the `minimal_dsgc_spatial_gaba` library asset:
   PASSED with zero errors and zero warnings.
5. Ran `arf.scripts.verificators.verify_task_metrics t0053_minimal_dsgc_spatial_gaba`: PASSED with
   zero errors and zero warnings.
6. Ran `uv run ruff check --fix . && uv run ruff format .`: All checks passed; 537 files left
   unchanged by the formatter.
7. Ran `uv run mypy -p tasks.t0053_minimal_dsgc_spatial_gaba.code`:
   `Success: no issues found in 1 source file`.

## Outputs

* `tasks/t0053_minimal_dsgc_spatial_gaba/results/tuning_curve_full.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/tuning_curve_ampa_only.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/tuning_curve_gaba_only.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/voltage_traces_full.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/voltage_traces_ampa_only.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/voltage_traces_gaba_only.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/spike_times_full.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/spike_times_ampa_only.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/spike_times_gaba_only.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/activation_times.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/active_fraction_per_direction.csv`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/placement_seed0.json`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/metrics.json`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/derived_quantities.json`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/images/v_soma_dir_{000..330}.png` (12 PNGs)
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/images/epsp_dir_{000..330}.png` (12 PNGs)
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/images/ipsp_dir_{000..330}.png` (12 PNGs)
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/images/psth_dir_{000..330}.png` (12 PNGs)
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/images/activation_dir_{000..330}.png` (12 PNGs)
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/images/polar_tuning_curve.png`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/images/cartesian_tuning_curve.png`
* `tasks/t0053_minimal_dsgc_spatial_gaba/results/images/active_fraction_polar.png`
* `tasks/t0053_minimal_dsgc_spatial_gaba/assets/library/minimal_dsgc_spatial_gaba/details.json`
* `tasks/t0053_minimal_dsgc_spatial_gaba/assets/library/minimal_dsgc_spatial_gaba/description.md`
* `tasks/t0053_minimal_dsgc_spatial_gaba/code/{cell,synapses,trial,run_tuning_curve,compute_metrics,render_figures,paths,constants,neuron_bootstrap,swc_io,placement,metrics_extra,test_quiescent_rest,test_placement_seed0_match,test_spatial_gating}.py`

## Issues

The FULL-mode tuning curve is identically 0 Hz across all 12 directions: the spatial centripetal
gating with full 2 nS GABA amplitude on ~50% of synapses fully suppresses spiking on the seed-0
placement, even on the directions where only ~34% of I synapses fire (theta=30, 330). The AMPA_ONLY
mode reaches 0.667 Hz uniformly across all directions (one spike per 1.5 s trial), so the underlying
excitation is functional but extremely close to threshold. As a result, primary DSI is undefined / 0
(peak == null == 0) in FULL and exactly 0 in AMPA_ONLY. This is a real biophysical observation, not
a code defect: the spatial mechanism with the chosen 2 nS GABA amplitude is genuinely too inhibitory
for measurable firing on this morphology and placement seed. The active-fraction asymmetry
(0.34..0.66 across directions, mean 0.50) and the per-direction aggregate IPSP peaks (6.33-7.82 mV;
ND-side larger by ~22%) are the recoverable spatial-mechanism observables. This should be the
headline finding for the suggestions step: a follow-up task should sweep GABA amplitude to find an
operating point where FULL spiking is non-zero so primary DSI can be measured directly.

The `run_with_logs` wrapper buffers all subprocess stdout/stderr until process exit, which made
mid-run tqdm progress invisible to the parent shell — same as t0052. Live PID CPU was polled to
confirm progress.

## REQ Completion Checklist

* `REQ-1` Morphology — Done. Cell built from
  `tasks/t0009_calibrate_dendritic_diameters/.../141009_Pair1DSGC_calibrated.CNG.swc`. Setup log:
  `n_dendrites=6717 total_dendritic_length_um=1528.62 soma_L_um=8.74 soma_diam_um=8.24 soma_origin_um=(0.0, 0.0, 0.0)`.
* `REQ-2` Channels — Done. `hh` only on soma + AIS; all dendrites passive.
  `test_quiescent_rest.py` passes the V_rest = -65 mV +/- 0.5 mV gate.
* `REQ-3` Synapse placement — Done. 100 E + 100 I co-located pairs with seed 0;
  `placement_seed0.json` written; `test_placement_seed0_match.py` confirms bit-identical match
  against t0052's `placement_seed0.json` within 1e-09 across all 100 pairs.
* `REQ-4` Excitatory mechanism — Done. AMPA `Exp2Syn` tau1=0.5, tau2=2.5, e=0, peak g=0.5 nS
  pinned in `constants.py`; `synapses.build_ei_pairs` sets `weight[0] = 0.5e-3` uS.
* `REQ-5` Inhibitory mechanism — Done. GABA `Exp2Syn` tau1=1, tau2=20, e=-75, peak g=2 nS full
  amplitude when fired; weight is exactly `2.0 * 1e-3` uS or `0.0` (no scalar scaling).
* `REQ-6` Position-gated firing — Done. Per-synapse activation-time histograms (12 PNGs) show the
  expected monotonic relationship between projected synapse coordinate and onset time.
* `REQ-7` Spatial centripetal-gating rule — Done. `i_synapse_fires(theta_stim, theta_centrifugal)`
  unit-tested in `test_spatial_gating.py` (PD-side: not fired, ND-side: fired, perpendicular: not
  fired). Per-direction `is_fired` column averages 0.34..0.66 across the 12 angles with mean 0.5000.
* `REQ-8` Stimulus — Done. 12 directions x 200 um bar at 1.0 um/ms over 1500 ms, hard-coded in
  `constants.py` and exercised by the sweep.
* `REQ-9` Trials — Done. 10 trials per direction (120 rows each per-mode CSV); deterministic seeds
  `1000 * angle_idx + trial_idx + 1`.
* `REQ-10` Three trial modes — Done. FULL, AMPA_ONLY, GABA_ONLY each produced
  `tuning_curve_*.csv`, `spike_times_*.csv`, and `voltage_traces_*.csv`.
* `REQ-11` Per-direction soma V(t) — Done. 12 `v_soma_dir_<deg>.png` PNGs (mean +/- SD across 10
  FULL trials).
* `REQ-12` Aggregate EPSP / IPSP — Done. 12 `epsp_dir_<deg>.png` (AMPA_ONLY) + 12
  `ipsp_dir_<deg>.png` (GABA_ONLY) PNGs.
* `REQ-13` PSTH — Done. 12 `psth_dir_<deg>.png` PNGs at 5 ms bins (FULL-mode; all bins are zero
  because FULL spiking is suppressed).
* `REQ-14` Polar tuning curve + DSI — Partial. `polar_tuning_curve.png` rendered, but FULL peak Hz
  = null Hz = 0 so primary DSI is undefined / 0 and vector-sum DSI = 0.0. The polar plot still
  conveys the (zero) tuning shape. Active-fraction polar (REQ-21) is the substantive
  spatial-mechanism observable.
* `REQ-15` Activation histograms — Done. 12 `activation_dir_<deg>.png` PNGs; `is_fired` column in
  the CSV separates fired vs silent I synapses.
* `REQ-16` Library asset — Done. `assets/library/minimal_dsgc_spatial_gaba/` with `details.json`
  and `description.md`; library verificator PASSED with 0/0.
* `REQ-17` `metrics.json` content — Done. Registered keys only (DSI, HWHM, reliability, RMSE) per
  the project metric registry; multi-variant FULL / AMPA_ONLY / GABA_ONLY layout. Vector-sum DSI,
  peak Hz, null Hz, preferred direction, and per-variant variants live in `derived_quantities.json`
  (non-registered scalars). `verify_task_metrics` PASSED 0/0.
* `REQ-18` Soft active-fraction sanity check — Done. Per-direction list and cross-direction mean
  written to `derived_quantities.json`; mean = 0.5000 inside `[0.4, 0.6]`; soft pass = true; no
  warning printed (the WARN branch was not entered).
* `REQ-19` Local CPU only — Done. No remote machines used (Step 8 skipped); no third-party API
  costs.
* `REQ-20` Random seed reported — Done. `PLACEMENT_SEED = 0` pinned in `constants.py`,
  `placement_seed0.json` written and verified bit-identical to t0052's.
* `REQ-21` Active-fraction polar plot — Done. `results/images/active_fraction_polar.png` exists
  (~10 KB). Will be embedded in `results_detailed.md` by the reporting step.
