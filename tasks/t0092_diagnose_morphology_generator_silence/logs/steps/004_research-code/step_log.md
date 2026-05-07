---
spec_version: "3"
task_id: "t0092_diagnose_morphology_generator_silence"
step_number: 4
step_name: "research-code"
status: "completed"
started_at: "2026-05-07T22:04:17Z"
completed_at: "2026-05-07T22:25:00Z"
---
# Step 4 -- Research code

## Summary

Spawned the `/research-code` subagent to map the t0024 / t0080 / t0090 / t0083 code surface relevant
to the diagnostic. The subagent surveyed 17 libraries (3 directly relevant), cited 5 prior tasks,
and answered each of the 4 candidate-root-cause questions from the task description. Verificator
PASSES with 0 errors and 0 warnings. The big finding is a NEW candidate root cause that supersedes
the pt3d-vs-L hypothesis: the procedural soma is built as a 15 um cylinder (~706 um^2 surface area)
while the t0024 hand-coded soma is a 7-pt3d frustum stack (~220 um^2) — a 3.2x mismatch that would
prevent the cell from reaching AP threshold under t0083 channels calibrated on the smaller soma.

## Actions Taken

1. Ran prestep for `research-code`, creating `logs/steps/004_research-code/`.
2. Spawned a general-purpose subagent with the `/research-code` skill prompt and the 4 candidate
   root causes from the task description as the questions to answer.
3. Subagent walked t0024 hand-coded Bed B builder, t0080 `apply_params.py` /
   `setup_synapses_parametric` / `_section_midpoint_xy` / `_bar_arrival_times`, t0090 generator's
   pt3dadd path, asymmetry transform at lines 333-355, channel insertion via
   `_insert_baseline_channels`, and t0083 pareto_front.json structure.
4. Subagent wrote `research/research_code.md` with all 7 mandatory sections plus optional
   Architecture Overview and Common Patterns. The Recommendations section ranks the soma-area
   mismatch as the leading hypothesis for Phase D.
5. Subagent ran `verify_research_code.py` -- PASSED 0 errors, 0 warnings.

## Outputs

* `tasks/t0092_diagnose_morphology_generator_silence/research/research_code.md`

## Issues

The `aggregate_libraries.py` and `aggregate_answers.py` aggregators are not present in this branch,
so the subagent walked `tasks/*/assets/library/*/details.json` directly to do the survey. Not
blocking.

The pt3d-vs-L override hypothesis (originally my leading suspect) was demoted: for the BedB base
point (`soma_offset_pd_um=0`, `field_elongation_pd=1.0`), the Euclidean distance between `start_xy`
and `end_xy` equals `node.length_um` exactly, so pt3dadd does not actually override sec.L there. The
override matters only for non-trivial asymmetry knob values. The new leading hypothesis is the
soma-area mismatch, which would directly explain the silence even on the BedB base point.
