---
spec_version: "3"
task_id: "t0034_distal_dendrite_length_sweep_t0024"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-23T10:31:02Z"
completed_at: "2026-04-23T13:30:00Z"
---
## Summary

Ran the full 7-length × 12-angle × 10-trial sweep (840 trials) on the t0024 DSGC port. Unlike
t0029's null result on t0022, **primary DSI actually varies on t0024** — range 0.545-0.774,
non-monotonic, slope -0.1259 per unit multiplier (p=0.038). The discriminator works but the shape
matches neither Dan2018 (predicted monotonic increase) nor Sivyer2013 (predicted saturating
plateau). Vector-sum DSI shows a cleaner negative trend (0.507 → 0.357), consistent with
passive-filtering interpretation.

## Actions Taken

1. Spawned a Phase-1 implementation subagent that wrote all 10 code files under `code/`: `paths.py`,
   `constants.py`, `distal_selector_t0024.py` (uses `cell.terminal_dends`),
   `length_override_t0024.py`, `preflight_distal.py`, `trial_runner_length_t0024.py`,
   `run_sweep.py`, `analyse_sweep.py`, `classify_shape.py`, `plot_sweep.py`.
2. Subagent ran preflight: **177 distal sections** identified via `cell.terminal_dends`, depth 3-18,
   L range 1.09-89.65 μm. Baseline 1.0× 12-angle smoke test: peak 4.5 Hz, null 0.5 Hz, hand-DSI ≈
   0.80 — confirms t0024 yields non-zero null firing (unlike t0022).
3. Orchestrator launched the full 840-trial sweep as persistent background process `bwzcvrnhv` via
   `run_with_logs.py`. Background job ran to completion with exit code 0.
4. Wall time: approximately 3 hours (matches plan's 2.8 h anchor from t0026 t0024 wall-time
   baseline).
5. Ran `analyse_sweep.py` to compute per-length metrics: primary DSI (peak-minus-null), vector-sum
   DSI, peak Hz, null Hz, HWHM, reliability, preferred angle, distal peak mV.
6. Ran `classify_shape.py` — result: **non_monotonic** with slope -0.1259 per unit multiplier
   (p=0.038), DSI range across extremes 0.2084. Vector-sum DSI also classified non_monotonic with
   negative trend.
7. Ran `plot_sweep.py` to render DSI-vs-length, vector-sum-DSI-vs-length, peak-Hz-vs-length, and
   12-direction polar overlay PNGs.
8. Ran `ruff check --fix`, `ruff format`, and
   `mypy -p tasks.t0034_distal_dendrite_length_sweep_t0024.code` — all clean.

## Outputs

### Code (10 Python files, lint + mypy clean)

* `code/paths.py`, `code/constants.py`, `code/distal_selector_t0024.py`,
  `code/length_override_t0024.py`, `code/preflight_distal.py`, `code/trial_runner_length_t0024.py`,
  `code/run_sweep.py`, `code/analyse_sweep.py`, `code/classify_shape.py`, `code/plot_sweep.py`

### Data

* `results/data/sweep_results.csv` (840 trials + header)
* `results/data/per_length/tuning_curve_L{0p50,0p75,1p00,1p25,1p50,1p75,2p00}.csv`
* `results/data/metrics_per_length.csv`, `results/data/metrics_notes.json`
* `results/data/curve_shape.json`
* `results/metrics.json` (registered per-length DSI metrics)

### Charts

* `results/images/dsi_vs_length.png`, `results/images/vector_sum_dsi_vs_length.png`,
  `results/images/peak_hz_vs_length.png`, `results/images/polar_overlay.png`

## Requirement Completion Checklist

| REQ | Status | Evidence |
| --- | --- | --- |
| REQ-1 | Done | t0024 as-is; AR(2) ρ=0.6 preserved in `constants.py` |
| REQ-2 | Done | `distal_selector_t0024.py` uses `cell.terminal_dends` (no `h.RGC.ON`) |
| REQ-3 | Done | `identify_distal_sections` helper COPIED not imported |
| REQ-4 | Done | 7 multipliers in `constants.py` |
| REQ-5 | Done | 12-direction × 10-trial protocol in `trial_runner_length_t0024.py` |
| REQ-6 | Done | AR(2) ρ=0.6 preserved at every call site |
| REQ-7 | Done | Secondary metrics (vector-sum DSI, peak Hz, null Hz, HWHM, rel) in `metrics_per_length.csv` |
| REQ-8 | Done | Curve-shape classification: non_monotonic, slope=-0.1259, p=0.038 |
| REQ-9 | Done | Vector-sum DSI defensive fallback (non_monotonic, consistent trend) |
| REQ-10 | Done | Polar overlay chart `results/images/polar_overlay.png` |
| REQ-11 | Done | Peak-Hz chart `results/images/peak_hz_vs_length.png` |
| REQ-12 | Done | Mechanism classification emitted in `curve_shape.json` |
| REQ-13 | Done | Per-row `fh.flush()` crash-recovery in `run_sweep.py` |
| REQ-14 | Done | $0 local CPU; no remote machines |
| REQ-15 | Done | Primary DSI meaningful on t0024 (range 0.545-0.774, p=0.038) — contrast to t0029's pinned 1.000 |

## Issues

No issues encountered. Sweep completed cleanly. The non-monotonic shape is a genuine negative result
for both Dan2018 and Sivyer2013 — neither a monotonic positive slope nor a saturating plateau is
supported. Vector-sum DSI shows a cleaner negative trend that leans toward passive-filtering-style
attenuation (longer distal cable → more filtering → lower preferred firing → lower DSI) but the
non-monotonicity in primary DSI at 1.5× and the bounce-back at 1.75× suggests additional dynamics
not captured by either mechanism. compare-literature step will explore this further.
