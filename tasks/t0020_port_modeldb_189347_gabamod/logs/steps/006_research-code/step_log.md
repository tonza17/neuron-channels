---
spec_version: "3"
task_id: "t0020_port_modeldb_189347_gabamod"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-20T19:24:27Z"
completed_at: "2026-04-20T19:25:30Z"
---
## Summary

Reviewed the t0008 NEURON-driver code and the t0012 scorer library to plan the gabaMOD-swap
refactor. Confirmed that `build_dsgc`, `apply_params`, the spike-counting tail of `run_one_trial`,
and the canonical paper constants (`TSTOP_MS`, `GABA_MOD`, `N_TRIALS`) can be imported and reused
without modification. Identified that the t0012 `score()` entry point cannot be invoked on a
two-condition CSV because its loader enforces a 12-angle uniform grid; the new scorer must compute
DSI and peak by direct formula. Cross-task imports are permitted because both source modules are
registered in their tasks' library assets.

## Actions Taken

1. Read `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/details.json` to
   understand the canonical library-asset layout (spec_version 2, module_paths, `description_path`,
   `entry_points`).
2. Read `tasks/t0008_port_modeldb_189347/code/build_cell.py` to identify reusable helpers
   (`build_dsgc`, `apply_params`, `read_synapse_coords`, `run_one_trial`) and to confirm `h.gabaMOD`
   is set Python-side from the `GABA_MOD` constant inside `apply_params`.
3. Read `tasks/t0008_port_modeldb_189347/code/run_tuning_curve.py`, `score_envelope.py`, and
   `paths.py` to mirror the driver/scorer/path conventions in the new task.
4. Read `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/__init__.py`,
   `envelope.py`, `loader.py`, and `metrics.py` to understand the scorer's API and confirm the
   12-angle grid constraint that motivates writing a separate two-point scorer.
5. Wrote `research/research_code.md` with all six mandatory sections, listing reuse vs. write- new
   components and recommending a single-library design with five new code files.

## Outputs

* `tasks/t0020_port_modeldb_189347_gabamod/research/research_code.md`
* `tasks/t0020_port_modeldb_189347_gabamod/logs/steps/006_research-code/step_log.md`

## Issues

No issues encountered.
