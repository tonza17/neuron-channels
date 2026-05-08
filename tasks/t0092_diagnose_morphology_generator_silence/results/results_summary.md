# Results Summary: Diagnose t0090 Procedural Cell Silence

## Summary

Identified the root cause of t0090's 0/60 spike rate as a **soma `pt3dadd` collapse**: the generator
emits two coincident soma pt3d points, NEURON computes cumulative pt3d distance ≈ 0 and overrides
`sec.L` to ~1e-9 µm, collapsing soma area to ~9.4e-14 µm² (vs hand-coded 287 µm²). Synaptic
input drives Vm to NaN within a few simulation steps. Fix landed as a thin shim
`generate_fixed_morphology` that re-emits the soma's two pt3d points along the z-axis. Post-fix the
BedB-equivalent fires **43.6 Hz PD-rate** and all **5/5 STABLE-from-t0090 cells** produce spikes
(stretch target was 3/5).

## Metrics

* **Hand-coded Bed B (validation gate)**: **41 spikes** under t0083 best-cell vector — gate
  passes, bug is in the generator.
* **Procedural BedB-equivalent (pre-fix)**: peak Vm = NaN within first few steps; **0 spikes**
  across 8 directions.
* **Procedural BedB-equivalent (post-fix)**: PD-rate = **43.6 Hz**, ND-rate = 40.7 Hz, peak Vm =
  +11.0 mV, DSI = **0.034**.
* **Soma area pre-fix**: ~**9.4e-14 µm²** (degenerate-zero-area sub-case).
* **Soma area post-fix**: ~**287 µm²** (matches hand-coded Bed B within 5 percent).
* **Stretch validation**: **5 / 5** STABLE-from-t0090 cells fire post-fix; morph_14 reaches PD-rate
  = **36.4 Hz / DSI = 0.962**, morph_13 reaches **DSI = 1.00** (PD-only spikes), morph_19 reaches
  DSI = 0.21.
* **Unit tests**: **4 / 4** PASS in `code/test_morphology_generator_fix.py`.

## Verification

* `uv run pytest tasks/t0092_diagnose_morphology_generator_silence/code/` — **4/4 PASS**
* `verify_research_code.py` — PASSED
* `verify_plan.py` — PASSED (0/0)
* `verify_task_metrics.py` — PASSED
* `verify_task_results.py` — to be run during the reporting step
* `ruff check . && ruff format .` clean
* `mypy -p tasks.t0092_..code` clean
