---
spec_version: "3"
task_id: "t0011_response_visualization_library"
research_stage: "code"
date_completed: "2026-04-20"
---

# Research Code

## Objective

Review tuning-curve outputs produced by t0004 and t0008 so the library's CSV loaders use the actual
on-disk schemas and the smoke tests plot real project data.

## Background

t0011 depends on two completed tasks that each produce angle-resolved firing-rate data in slightly
different CSV layouts. The library must settle a canonical schema and provide a small loader to
read each upstream format.

## Methodology Review

Inspected every CSV under both dependency asset folders. Compared columns, dtypes, and angular
sampling.

## Key Findings

### t0004_generate_target_tuning_curve

Two files in `assets/dataset/target-tuning-curve/files/`:

* `curve_mean.csv` — columns `(angle_deg, mean_rate_hz)`. Mean response per angle, no trial
  information. This is the canonical "target curve" overlay for every later experiment.
* `curve_trials.csv` — columns `(angle_deg, trial_index, rate_hz)`. Per-trial samples that feed the
  bootstrap CI band. Column names differ from t0008's (`trial_index` vs `trial_seed`,
  `rate_hz` vs `firing_rate_hz`).

### t0008_port_modeldb_189347

* `data/tuning_curves/curve_modeldb_189347.csv` — columns
  `(angle_deg, trial_seed, firing_rate_hz)`. 8 angles × 8 trials = 64 rows. This matches the task
  description's canonical schema exactly.
* `data/smoke_test_single_angle.csv` — same schema, one angle only; not useful as a full tuning
  curve.
* No raster/spike-time CSV. The t0008 port emits firing rates but not per-trial spike times, so the
  raster+PSTH smoke test must synthesise a small spike-time file from scratch.

### Implications for the library

* Adopt `(angle_deg, trial_seed, firing_rate_hz)` as the canonical tuning-curve schema — matches
  t0008 and the task description.
* Provide a `load_t0004_trials(path)` helper that reads `curve_trials.csv` and renames columns
  (`trial_index` → `trial_seed`, `rate_hz` → `firing_rate_hz`) so the same plotting code path
  handles both datasets.
* For the target overlay, accept `curve_mean.csv` directly (columns `angle_deg, mean_rate_hz`) via
  the `target_csv` keyword argument.
* For the raster+PSTH smoke test, generate a synthetic spike-times CSV (columns
  `trial_seed, angle_deg, spike_time_s`) locally inside the smoke test — no upstream file to reuse.

## Recommended Approach

1. Put the loader helpers in `code/tuning_curve_viz/loaders.py` with an explicit conversion from
   the t0004 layout to the canonical schema.
2. Use the t0008 curve (`curve_modeldb_189347.csv`) verbatim for the multi-model-overlay smoke test.
3. Generate a small synthetic spike-time fixture (Poisson with lambda depending on `angle_deg`) in
   the smoke-test script. Store it under `code/tuning_curve_viz/smoke_data/` so the raster
   smoke test has a deterministic input.

## References

* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_trials.csv`
* `tasks/t0008_port_modeldb_189347/data/tuning_curves/curve_modeldb_189347.csv`
* `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/description.md`
