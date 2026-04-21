---
spec_version: "3"
task_id: "t0026_vrest_sweep_tuning_curves_dsgc"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-21T13:17:45Z"
completed_at: "2026-04-21T18:30:00Z"
---
# Step 9: Implementation

## Summary

Implemented and executed the V_rest sweeps for both DSGC compartmental models (t0022 deterministic
and t0024 stochastic AR(2) release) across eight resting potentials (-90 mV to -20 mV in 10 mV
steps) crossed with the standard 12-direction moving-bar protocol. Built the analysis pipeline
(per-V_rest metric computation, polar plots, Cartesian summary, multi-variant metrics.json) and
materialised the two predictions assets for downstream consumption.

## Actions Taken

1. Wrote `code/constants.py` centralising all paths, V_rest values, angles, and CSV column names.
2. Wrote `code/vrest_override.py` exposing `set_vrest(h, v_rest_mv)` which simultaneously overrides
   `h.v_init`, every `eleak_HHst`, and every `e_pas` parameter to produce a stable steady-state
   V_rest rather than a transient initial-condition tweak. Wrote `code/vrest_override_smoke.py` to
   validate the override produces a stable steady-state V_rest before running the full sweeps.
3. Wrote `code/trial_runner_t0022.py` and `code/trial_runner_t0024.py` thin wrappers that adapt each
   model's existing `run_trial` / `run_one_trial` function to the V_rest override workflow,
   recording per-trial spike count, peak somatic mV, and firing rate.
4. Wrote `code/run_vrest_sweep_t0022.py` driving the t0022 deterministic harness: 8 V_rest x 12
   angles x 1 trial = 96 trials; cell built once and cached across the entire sweep; output to
   `data/t0022/vrest_sweep_tidy.csv`. Wall time 6.0 min on the local Windows workstation.
5. Wrote `code/run_vrest_sweep_t0024.py` driving the t0024 AR(2)-correlated stochastic harness: 8
   V_rest x 12 angles x 10 trials = 960 trials; output to `data/t0024/vrest_sweep_tidy.csv`. Wall
   time 11,562 s (3.21 h); per-V_rest wall times stored in `data/t0024/wall_time_by_vrest.json`.
   Preflight wall-time probes for both models stored in `data/preflight/`.
6. Wrote `code/compute_vrest_metrics.py` computing per-(V_rest) DSI (Mazurek vector-sum convention),
   HWHM (1-degree linear interpolation around the preferred direction), peak / null firing rates,
   and mean peak somatic voltage. Output to `data/<model>/vrest_metrics.csv`.
7. Wrote `code/plot_polar_tuning.py` producing per-V_rest polar plots, an overlay polar plot, and a
   3-panel Cartesian summary (peak/null Hz, DSI, HWHM vs V_rest) per model. Output to
   `results/images/`.
8. Wrote `code/write_metrics.py` emitting the multi-variant `results/metrics.json` with two
   top-level variants (`t0022`, `t0024`) keyed by registered metric ids
   (`direction_selectivity_index`, `tuning_curve_hwhm_deg`) plus a `project_specific` block for
   peak/null Hz, preferred direction, and mean peak mV.
9. Built the t0022 predictions asset `assets/predictions/t0026-vrest-sweep-t0022/` (details.json,
   description.md, copy of CSV) and the t0024 predictions asset
   `assets/predictions/t0026-vrest-sweep-t0024/` likewise. Both verified with the predictions
   verificator.

## Outputs

* `code/constants.py`, `code/vrest_override.py`, `code/vrest_override_smoke.py`,
  `code/trial_runner_t0022.py`, `code/trial_runner_t0024.py`, `code/run_vrest_sweep_t0022.py`,
  `code/run_vrest_sweep_t0024.py`, `code/compute_vrest_metrics.py`, `code/plot_polar_tuning.py`,
  `code/write_metrics.py`
* `data/preflight/{t0022_preflight.csv,t0022_wall.json,t0024_preflight.csv,t0024_wall.json}`
* `data/t0022/vrest_sweep_tidy.csv` (96 trials), `data/t0022/vrest_metrics.csv`
* `data/t0024/vrest_sweep_tidy.csv` (960 trials), `data/t0024/vrest_metrics.csv`,
  `data/t0024/wall_time_by_vrest.json`
* `results/metrics.json` (multi-variant format)
* `results/images/polar_t0022_vrest_*.png` (8 individual), `polar_t0022_overlay.png`,
  `summary_t0022_vrest.png`
* `results/images/polar_t0024_vrest_*.png` (8 individual), `polar_t0024_overlay.png`,
  `summary_t0024_vrest.png`
* `assets/predictions/t0026-vrest-sweep-t0022/{details.json,description.md,files/predictions-vrest-sweep-t0022.csv}`
* `assets/predictions/t0026-vrest-sweep-t0024/{details.json,description.md,files/predictions-vrest-sweep-t0024.csv}`

## Issues

No issues encountered. Both predictions assets pass verification with the expected PR-W014 (model_id
null) and PR-W015 (dataset_ids empty) warnings — these are correct because the asset links to a
library asset rather than a model asset, and the stimulus is synthetic.
