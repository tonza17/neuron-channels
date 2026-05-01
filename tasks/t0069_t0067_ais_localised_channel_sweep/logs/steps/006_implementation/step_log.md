---
spec_version: "3"
task_id: "t0069_t0067_ais_localised_channel_sweep"
step_number: 6
step_name: "implementation"
status: "completed"
started_at: "2026-05-01T02:25:30Z"
completed_at: "2026-05-01T02:35:00Z"
---
## Summary

Vendored 5 t0067 MOD files into `code/mods/`, compiled the t0069-local DLL, wrote
`code/{paths,constants,extend_with_ais,run_sweep,plot_results}.py`. Ran 160 FULL-mode trials (~8 min
wall-clock, 0/160 unstable). Generated 3 PNGs (firing-rate, DSI, soma-vs-AIS comparison).
**Hypothesis S-0067-03 falsified**: AIS-localised channels show smaller |ΔDSI| than soma-localised.

## Actions Taken

1. Wrote `code/paths.py` and `code/constants.py` (mirrors t0067 plus AIS/axon geometry constants).
2. Copied t0067 MOD files (`nav16t67`, `napt67`, `nart67`, `kv3t67`, `kv4t67`) verbatim into
   `code/mods/`.
3. Built t0008 nrnmech.dll in this worktree (worktrees don't inherit build artefacts).
4. Compiled t0069-local nrnmech.dll into `code/build/`.
5. Wrote `code/extend_with_ais.py` to construct AIS (30 μm × 1 μm × 5 seg) + axon (1000 μm × 1
   μm × 50 seg), insert HHst at AIS / axon densities, attach to soma.
6. Wrote `code/run_sweep.py` mirroring t0067 driver but with `_set_active_channel_on_ais()` instead
   of `_set_active_channel_on_soma()`.
7. Wrote `code/plot_results.py` with 3 plot functions including soma-vs-AIS cross-task comparison.
8. Ran 160 trials in ~8 min. 0/160 unstable.
9. Generated 3 PNGs from `data/dsi_by_condition.json` and t0067's `data/dsi_by_condition.json`.
10. Ran ruff check + format + mypy — all PASSED.

## Outputs

* `code/{paths,constants,extend_with_ais,run_sweep,plot_results}.py`
* `code/mods/{nav16,nap,nar,kv3,kv4}t67.{mod,c,o}` and `mod_func.{c,o}`
* `code/build/nrnmech.dll` (build artefact, gitignored)
* `data/per_trial_metrics.json` (160 trials)
* `data/dsi_by_condition.json` (16 conditions)
* `results/images/{firing_rate_vs_density,dsi_vs_density,soma_vs_ais_comparison}.png`

## Issues

None blocking. AIS+axon attachment alone halved baseline PD firing (14.2 → 6.4) and silenced ND
firing entirely (1.6 → 0.0), pinning baseline DSI at 1.0. This is the substrate problem documented
in `results/results_detailed.md` Analysis section.
