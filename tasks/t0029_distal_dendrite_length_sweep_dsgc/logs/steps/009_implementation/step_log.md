---
spec_version: "3"
task_id: "t0029_distal_dendrite_length_sweep_dsgc"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-22T11:09:46Z"
completed_at: "2026-04-22T12:16:00Z"
---
## Summary

Implemented the distal-dendrite length sweep on the t0022 DSGC testbed. Built nine Python modules
under `code/` following the t0026 V_rest-sweep template (constants, paths, length_override,
trial_runner_length, run_length_sweep, compute_length_metrics, classify_curve_shape,
plot_dsi_vs_length, preflight_distal). Ran the full 7 × 12 × 10 = 840 trial sweep (distal L
multipliers 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0) through `run_with_logs` in ~42 minutes total wall
time. DSI is saturated at **1.000** (preferred/null definition) across all seven multipliers, so the
curve is classified as `saturating` with slope 0.0. Peak firing rate moves only between **14-15 Hz**
and HWHM oscillates **71.7°-116.2°**. A secondary vector-sum DSI metric was computed offline and
shows a weak monotonic decrease (0.664 → 0.643 from 0.5× to 2.0×) but is not a registered
project metric.

This saturation outcome answers task question 3 with "the testbed saturates at the default length"
and means the primary-DSI axis does **not** discriminate Dan2018 from Sivyer2013. The discrimination
has to fall to vector-sum DSI or to peak firing rate, which the `compare-literature` step will
address. All ruff and mypy checks are clean.

## Actions Taken

1. Ran `prestep implementation`.
2. Spawned the `/implementation` skill subagent which wrote all nine code modules, ran a preflight
   (3 angles × 2 trials × 3 multipliers), resolved early NEURON bootstrap (nrnmech.dll path) and
   API (sec.name vs segment) bugs, and launched the full sweep.
3. Restarted the interrupted full sweep in the background after the subagent's foreground subprocess
   ended; monitored CSV progress via a shell Monitor that emitted a milestone line per 120 rows.
4. Full sweep completed at 12:13:59Z with 840 data rows in `results/data/sweep_results.csv` (42-min
   wall time; per-length wall times recorded in `results/data/wall_time_by_length.json`).
5. Ran `compute_length_metrics` → wrote `results/metrics.json` (7 variants, explicit multi-variant
   format, registered keys only: DSI, HWHM, reliability), plus `results/data/metrics_per_length.csv`
   with extra diagnostics (vector-sum DSI, peak firing, null firing, preferred angle) and
   `results/data/metrics_notes.json` documenting the deliberate omission of `tuning_curve_rmse`.
6. Ran `classify_curve_shape` → classified the DSI-vs-L curve as `saturating` with
   `saturation_multiplier = 0.5` and `plateau_dsi = 1.0`; wrote `results/data/curve_shape.json`.
7. Ran `plot_dsi_vs_length` → wrote primary chart `results/images/dsi_vs_length.png` plus 7
   per-length polar diagnostics (`polar_L0p50.png` … `polar_L2p00.png`).
8. Ran `uv run ruff check --fix .`, `uv run ruff format .`, and
   `uv run mypy -p tasks.t0029_distal_dendrite_length_sweep_dsgc.code` — all three passed clean
   (no issues found in any source file).

## Outputs

* `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/` — nine modules (`constants.py`,
  `paths.py`, `length_override.py`, `trial_runner_length.py`, `run_length_sweep.py`,
  `compute_length_metrics.py`, `classify_curve_shape.py`, `plot_dsi_vs_length.py`,
  `preflight_distal.py`)
* `tasks/t0029_distal_dendrite_length_sweep_dsgc/results/data/sweep_results.csv` — 840-row tidy
  CSV (REQ-4)
* `tasks/t0029_distal_dendrite_length_sweep_dsgc/results/data/per_length/tuning_curve_L*.csv` — 7
  canonical 12-angle curve CSVs (accepted by the t0012 scorer)
* `tasks/t0029_distal_dendrite_length_sweep_dsgc/results/data/metrics_per_length.csv` — per-L
  diagnostics including vector-sum DSI, peak/null firing, preferred angle, peak mV
* `tasks/t0029_distal_dendrite_length_sweep_dsgc/results/data/wall_time_by_length.json` —
  per-multiplier wall-clock times
* `tasks/t0029_distal_dendrite_length_sweep_dsgc/results/data/curve_shape.json` — classification
  output (REQ-5, REQ-6)
* `tasks/t0029_distal_dendrite_length_sweep_dsgc/results/metrics.json` — 7 multi-variant entries
  with registered metrics only
* `tasks/t0029_distal_dendrite_length_sweep_dsgc/results/images/dsi_vs_length.png` — primary chart
  (REQ-5)
* `tasks/t0029_distal_dendrite_length_sweep_dsgc/results/images/polar_L*.png` — 7 per-length polar
  diagnostics

## Requirement Completion Checklist

| ID | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Use t0022 testbed as-is; only mutate `sec.L` on distals | done | `length_override.py` only rewrites `sec.L`; no channel / input / morphology 3d-point edits. `assert_distal_lengths` round-trip confirmed after the sweep. |
| REQ-2 | Identify distal dendritic sections at branch order ≥ 3 | done | `length_override.identify_distal_sections` filters HOC leaves on the ON arbor with depth ≥ 3; `preflight_distal.py` logged the selection before the full sweep. |
| REQ-3 | Sweep 7 multipliers {0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0}, same multiplier on all distals | done | `LENGTH_MULTIPLIERS` in `constants.py`; sweep CSV has 7 × 12 × 10 = 840 rows, each with the same `length_multiplier` applied globally to all distal sections. |
| REQ-4 | 12-direction × 10-trial protocol per length; DSI via t0012 scorer | done | `sweep_results.csv` has 120 rows per multiplier (12 angles × 10 trials); `compute_length_metrics` calls `tuning_curve_loss.compute_dsi` on each per-length curve CSV. |
| REQ-5 | Plot DSI vs length; classify as monotonic / saturating / non-monotonic | done | `results/images/dsi_vs_length.png`; classification = `saturating` in `curve_shape.json`. |
| REQ-6 | Report slope / saturation length / qualitative shape | done | slope = 0.0, `saturation_multiplier` = 0.5, plateau DSI = 1.000, qualitative description recorded. |
| REQ-7 | Answer 3 key questions (saturation y/n, saturation L, DSI range at extremes) | done | saturating = yes at L = 0.5; DSI range at extremes = 0.000; all three questions answered with explicit numbers in `curve_shape.json`. |
| REQ-8 | DSI primary; spike counts / firing rates secondary | done | `metrics.json` publishes only registered metrics (DSI, HWHM, reliability); secondary values live in `metrics_per_length.csv`. |
| REQ-9 | Local CPU only, $0 external cost | done | No remote compute invoked; `results/costs.json` (written in the `results` step) will record $0. |

## Issues

The DSI (preferred/null definition) is pinned at **1.000** across every multiplier, so DSI-vs-length
alone does not discriminate the two mechanisms at the sweep extremes the task description proposed.
This was flagged as a known risk in the plan's Risks & Fallbacks section; the fallback — reporting
secondary metrics (vector-sum DSI, peak rate, HWHM) — is implemented. The saturation itself is a
legitimate finding and feeds directly into the `compare-literature` step (which will reference
Park2014's 0.65 ± 0.05 band and Schachter2010 stochasticity papers) and suggestions (a
Poisson-noise or reduced-EI-asymmetry sweep to desaturate DSI). No blocking errors.
