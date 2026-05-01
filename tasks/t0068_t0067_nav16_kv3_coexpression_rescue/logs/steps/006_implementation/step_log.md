---
spec_version: "3"
task_id: "t0068_t0067_nav16_kv3_coexpression_rescue"
step_number: 6
step_name: "implementation"
status: "completed"
started_at: "2026-05-01T02:04:30Z"
completed_at: "2026-05-01T02:55:00Z"
---
## Summary

Copied 5 t0067 MOD files into `code/mods/`, compiled t0068-local DLL, wrote
`code/{paths,constants,run_sweep,plot_results}.py`. Ran 90 FULL-mode trials in ~~10 min wall-clock.
**Hypothesis FALSIFIED**: Kv3 co-expression does NOT rescue DSI from Nav1.6's erosion. Across all 8
co-expression conditions DSI changes by less than ±0.025 from the Nav1.6-only anchor; instead Kv3
slightly *boosts* firing rate (~~+10%) by enabling faster Na+ recovery from inactivation, scaling PD
and ND equally so DSI is unchanged.

## Actions Taken

1. Wrote `code/paths.py` and `code/constants.py` with 9-condition schema.
2. Copied t0067 MOD files (`nav16t67`, `napt67`, `nart67`, `kv3t67`, `kv4t67`) verbatim into
   `code/mods/`.
3. Compiled t0068-local nrnmech.dll via `t0008/code/run_nrnivmodl.cmd`.
4. Built t0008 nrnmech.dll in this worktree (worktrees don't inherit build artefacts).
5. Wrote `code/run_sweep.py` — generalised t0067 driver to set both Nav1.6 + Kv3 gbars per trial
   via `_set_active_channels(soma, condition)`.
6. Wrote `code/plot_results.py` — 2 PNGs (DSI rescue curve, firing rate rescue).
7. Ran 90 trials in ~10 min. No instability flags.
8. Generated 2 PNGs from `data/dsi_by_condition.json`.
9. Verified ruff + mypy on all task code.

## Outputs

* code/{paths,constants,run_sweep,plot_results}.py
* code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod
* code/build/nrnmech.dll
* data/per_trial_metrics.json (90 trials)
* data/dsi_by_condition.json (9 conditions)
* results/metrics.json (`direction_selectivity_index = 0.7975` baseline)
* results/images/{dsi_rescue_curve, firing_rate_rescue}.png

## Issues

None blocking. Hypothesis is falsified, which is a clean, useful result. 0/90 trials flagged
unstable.
