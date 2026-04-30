---
spec_version: "3"
task_id: "t0067_t0065_soma_channel_addition_sweep"
step_number: 6
step_name: "implementation"
status: "completed"
started_at: "2026-05-01T00:22:30Z"
completed_at: "2026-05-01T00:35:00Z"
---
## Summary

Implemented `code/{paths,constants,run_sweep,plot_results}.py` and 5 NEURON MOD files
(`code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod`). Compiled the MODs into a task-local
`code/build/nrnmech.dll`, then ran 160 FULL-mode trials in ~10 minutes. All trials completed without
instability flags. Headline results: **NaP at high density inverts DSI to -0.18**; **Nav1.6
monotonically reduces DSI as density increases** (0.80→0.75→0.48→0.23 across
baseline/low/med/high); NaR / Kv3 / Kv4 produce only modest changes at the chosen density range.

## Actions Taken

1. Wrote `code/paths.py` with the t0067-local DLL path and 3 PNG output paths.
2. Wrote `code/constants.py` with `ChannelKind`, `DensityLabel`, `Direction` `StrEnum`s plus
   `CHANNEL_DEFS` tuple containing the 5 channels and their 3-density grids.
3. Wrote 5 minimal NEURON MOD files using NONSPECIFIC_CURRENT pattern (avoids USEION conflicts with
   the existing HHst mechanism). Kinetics from Carter-Bean 2009 (Nav1.6), Magistretti-Alonso 1999
   (NaP), Khaliq-Raman 2003 (NaR, simplified m^3·h·s), Erisir 1999 (Kv3), Hoffman 1997 (Kv4 / IA).
4. Built the t0008 nrnmech.dll in this worktree (worktrees don't inherit build artefacts) by running
   `t0008/code/run_nrnivmodl.cmd` against the deposited sources.
5. Built the t0067-local nrnmech.dll by running the same script against the 5 vendored MODs in
   `code/mods/`. Both DLLs load successfully with no SUFFIX collisions.
6. Wrote `code/run_sweep.py`:
   * `_ensure_t67_dll_loaded` adds the t0067 DLL on top of the t0008 DLL.
   * `_insert_all_channels_with_zero_gbar` inserts all 5 mechanisms on the soma at gbar=0 once at
     startup.
   * `_set_active_channel` zeros all 5 then sets the active one's gbar per trial.
   * Per-trial: apply_params → set gabaMOD → exptype=1 → init_active → update → placeBIP
     → set active channel gbar (AFTER init_active so it survives the rebind) → finitialize →
     continuerun → count spikes via NetCon threshold.
   * Per-condition aggregation: PD/ND mean ± SD across 5 seeds, DSI = (PD-ND)/(PD+ND), count
     unstable trials.
7. Wrote `code/plot_results.py`:
   * 3 PNGs: firing rate vs density (5 panels × PD/ND with baseline reference lines), DSI vs
     density (5 panels with baseline horizontal reference), 2-panel PD/ND spike count heatmap.
8. Smoke test (3 trials): baseline = 15 spikes (matches t0065), Nav1.6 med = 26 spikes, Kv3 high =
   18 spikes — all sensible.
9. Full sweep: 160 trials in ~10 min wall-clock. No instability.
10. Generated 3 PNGs from `data/dsi_by_condition.json` in <2 s.
11. Verified `ruff check`, `ruff format`, `mypy` all pass.

## Outputs

* `tasks/t0067_t0065_soma_channel_addition_sweep/code/{paths,constants,run_sweep,plot_results}.py`
* `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod`
* `tasks/t0067_t0065_soma_channel_addition_sweep/code/build/nrnmech.dll` (t0067-local DLL)
* `tasks/t0067_t0065_soma_channel_addition_sweep/data/per_trial_metrics.json` (160 entries)
* `tasks/t0067_t0065_soma_channel_addition_sweep/data/dsi_by_condition.json` (16 entries)
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/metrics.json`
  (`direction_selectivity_index = 0.7975` for baseline)
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/firing_rate_vs_density.png`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/dsi_vs_density.png`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/spike_count_heatmap.png`

## Issues

None blocking. The t0008 and t0067 DLLs both had to be compiled fresh in this worktree — same
known issue as t0065/t0066 (worktrees don't inherit build artefacts). All compilations succeeded on
the first attempt.
