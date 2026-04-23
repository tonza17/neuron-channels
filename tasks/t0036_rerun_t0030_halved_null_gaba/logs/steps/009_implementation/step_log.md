---
spec_version: "3"
task_id: "t0036_rerun_t0030_halved_null_gaba"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-23T21:19:06Z"
completed_at: "2026-04-23T22:45:00Z"
---
## Summary

Ran 840-trial distal-diameter sweep on t0022 with `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` (halved from
12 nS). **Pre-condition gate FAILED**: mean null-Hz at 1.0× baseline is 0.0 Hz at every diameter —
halving the GABA was insufficient to unpin null firing. Classification label emitted: `flat_partial`
(slope 0.0049, p=0.019, DSI range 0.006). Auto-recommendation: further reduce null-GABA to ~4 nS.

## Actions Taken

1. Spawned Phase-1 implementation subagent to write all 11 code files, including the new
   `gaba_override.py` that monkey-patches t0022's GABA constant at module load.
2. Subagent ran preflight: 3 of 4 halt-level gates passed (banner, no assertion error, peak Hz=15);
   4th gate (null-Hz) was informational on 3-angle subset because true null (180°) wasn't sampled.
3. Orchestrator launched full 840-trial sweep as `bvz0xeerh` via run_with_logs.py. First attempt
   (b7vemea6j) crashed due to relative --output path issue; relaunched without the --output flag
   using default path. Ran to exit 0, ~30 min wall time on t0022 (faster than t0024 because
   deterministic).
4. Ran analyse_sweep.py: primary DSI still 1.000 at every diameter; null_hz = 0.0 at every diameter;
   vector-sum DSI 0.579-0.590 (range 0.011).
5. Ran classify_slope.py: pre-condition gate FAILED (null_hz < 0.1 threshold). Label:
   `flat_partial`. Auto-recommendation printed: reduce null-GABA further to ~4 nS.
6. Ran plot_sweep.py: 5 PNGs including the diagnostic `null_hz_vs_diameter.png` which visibly shows
   all 7 values at 0.0 Hz.
7. `ruff check --fix`, `ruff format`, `mypy -p tasks.t0036_rerun_t0030_halved_null_gaba.code` — all
   clean.

## Outputs

### Code (11 Python files, lint + mypy clean)

* `code/paths.py`, `code/constants.py`, `code/gaba_override.py` (NEW), `code/diameter_override.py`,
  `code/preflight_distal.py`, `code/trial_runner_diameter.py`, `code/run_sweep.py`,
  `code/analyse_sweep.py`, `code/classify_slope.py`, `code/plot_sweep.py`

### Data

* `results/data/sweep_results.csv` (840 trials + header)
* `results/data/per_diameter/tuning_curve_D{0p50,0p75,1p00,1p25,1p50,1p75,2p00}.csv`
* `results/data/metrics_per_diameter.csv`, `results/data/dsi_by_diameter.csv`,
  `results/data/metrics_notes.json`
* `results/data/curve_shape.json`, `results/data/slope_classification.json` (carries
  `precondition_pass=False`, `mechanism_label=flat_partial`)
* `results/metrics.json`

### Charts

* `results/images/dsi_vs_diameter.png`, `vector_sum_dsi_vs_diameter.png`, `null_hz_vs_diameter.png`
  (diagnostic — all 7 at 0 Hz), `peak_hz_vs_diameter.png`, `polar_overlay.png`

## Requirement Completion Checklist

| REQ | Status | Evidence |
| --- | --- | --- |
| REQ-1 — REQ-11 | **Done** | All code / charts / analysis / style-checks produced as planned |
| REQ-12 (primary DSI becomes measurable) | **Not done** | null_hz still 0.0 at 1.0×; primary DSI pinned at 1.000; GABA halving insufficient. Classifier emitted `flat_partial` and auto-recommendation to reduce GABA further. |

## Issues

Primary DSI did NOT unpin at GABA=6 nS. Halving was insufficient on the t0022 deterministic testbed
— the remaining 6 nS inhibition is still strong enough to keep null-direction membrane voltage below
AP threshold at every tested diameter. This is the honest result. The suggestions step will queue a
follow-up at a smaller GABA value (4 nS or lower), or a Poisson-noise-based rescue.
