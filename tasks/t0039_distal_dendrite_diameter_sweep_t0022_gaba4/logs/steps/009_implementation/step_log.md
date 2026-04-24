---
spec_version: "3"
task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-24T08:08:37Z"
completed_at: "2026-04-24T08:10:00Z"
---
## Summary

Ran the full 840-trial diameter sweep at GABA=4 nS (preflight 18 trials confirmed firing rates match
t0037 baseline-diameter values, then full sweep in ~38 min wall clock). Analysis classified the
mechanism as **passive_filtering**: DSI decreases monotonically from 0.429 (D=0.5) to 0.368 (D=2.0),
slope=-0.0336 per log2(multiplier), p=0.008. Seven per-diameter tuning curves + four charts +
metrics.json all written.

## Actions Taken

1. Copied t0030 diameter-sweep code + t0037 gaba_override; bulk-renamed module refs.
2. Edited `trial_runner_diameter.py` to apply both overrides per trial with t0037's lazy re-read
   pattern.
3. Added `set_null_gaba_ns(4.0)` belt-and-braces at top of `run_sweep.main()`.
4. Ran `ruff check --fix`, `ruff format`, `mypy -p tasks.t0039...code` — all clean (11 files).
5. Copied `nrnmech.dll` from the t0030 worktree into t0039's `t0022/build/modeldb_189347/` to avoid
   rebuilding MOD files.
6. Preflight: 3 × 3 × 2 = 18 trials; firing rates D=1.00x baseline matched t0037 (peak 15 Hz, null
   0-6 Hz, preferred direction DSGC-like).
7. Full sweep: 840 trials, exit code 0, ~38 min wall clock.
8. Ran `analyse_sweep.py` → metrics_per_diameter.csv, metrics.json.
9. Ran `classify_slope.py` → slope_classification.json (mechanism=passive_filtering).
10. Ran `plot_sweep.py` → 4 PNG charts.

## Outputs

* `code/` — 11 files (gaba_override.py, trial_runner_diameter.py, run_sweep.py, analyse_sweep.py,
  classify_slope.py, plot_sweep.py, constants.py, paths.py, diameter_override.py,
  preflight_distal.py, **init**.py)
* `results/data/sweep_results.csv` — 840 trials
* `results/data/per_diameter/tuning_curve_D{0p50,...,2p00}.csv` — 7 per-diameter curves
* `results/data/metrics_per_diameter.csv`, `dsi_by_diameter.csv`, `curve_shape.json`,
  `slope_classification.json`, `wall_time_by_diameter.json`, `metrics_notes.json`
* `results/metrics.json` — 21 metric entries (7 diameters × 3 registered keys)
* `results/images/dsi_vs_diameter.png`, `vector_sum_dsi_vs_diameter.png`, `peak_hz_vs_diameter.png`,
  `polar_overlay.png`

## Issues

One mid-sweep git conflict: the pre-commit hook failed on `sweep_results.csv` while the sweep was
actively writing it (open file lock on Windows). Resolved by excluding `results/data/` from the
staging command until the sweep completed.
