# Results Detailed: Brainstorm results session 5

## Summary

Session 5 focused on a single researcher-directed follow-up experiment rather than broad backlog
pruning. Three inline Q&A exchanges were answered before the task was captured.

## Methodology

* Machine: local Windows workstation (Windows 11 Education 22631).
* Runtime: ~5 minutes of interactive dialogue.
* Timestamp: 2026-04-21.
* Worker count: 1.

## Metrics Tables

No metrics produced by a brainstorm session.

## Comparison vs Baselines

Not applicable.

## Visualizations

No charts produced by a brainstorm session.

## Analysis / Discussion

### Q1. Count of implemented models

Answer: four DSGC compartmental-model ports now exist, all sharing the t0004 tuning-curve target and
the t0012 scoring library:

| Model | Task | Library asset | Driver paradigm |
| --- | --- | --- | --- |
| 1 | t0008 | `modeldb_189347_dsgc` | Spatial-rotation BIP proxy |
| 2 | t0020 | `modeldb_189347_dsgc_gabamod` | gabaMOD swap (PD=0.33, ND=0.99) |
| 3 | t0022 | `modeldb_189347_dsgc_channel_testbed` | Deterministic per-dendrite E-I scheduling |
| 4 | t0024 | `de_rosenroll_2026_dsgc` | AR(2)-correlated stochastic release |

### Q2. Why t0022 returns DSI = 1; what is HWHM?

t0022 returns DSI = 1.0 because its ND-direction firing rate is exactly 0 Hz — per-dendrite E-I
scheduling delivers a pure inhibitory lead in the ND condition, which silences the cell entirely.
`(R_pref - R_null) / (R_pref + R_null)` with `R_null = 0` collapses to 1.

HWHM = Half-Width at Half-Maximum — the angular width of the tuning curve measured from preferred
direction to the angle where firing drops to half the peak rate. It is the direction-tuning analogue
of full-width-at-half-maximum (FWHM) / 2 and reflects how sharp the tuning is.

### Q3. Stimulus length and firing-rate window

`TSTOP_MS = 1000` ms per trial; the moving bar enters the dendritic field around 40 ms and sweeps
across at `1 um/ms` so it takes ~240 ms to cross. Firing rate is computed as total spikes over the
full 1000 ms window, so it is strictly spikes/s (Hz).

### Follow-up task captured

Researcher requested: "calculate the tuning curves as a function of resting potential. Perform this
for models 3 and 4 start from -90 and go to -20 incrementing by 10 (all in mv). Report data in polar
coordinates."

Clarifications:

1. Shift both `v_init` and `eleak` to the sweep value (true V_rest shift, biophysically consistent).
   Leak reversal must move with the holding potential.
2. Trial counts: 1 trial × 12 angles for t0022 (deterministic driver), 10 trials × 12 angles for
   t0024 (stochastic AR(2) release).
3. Eight V_rest values: -90, -80, -70, -60, -50, -40, -30, -20 mV.

This captured as new task `t0026` via `/create-task`.

## Limitations

* This brainstorm captured only the researcher-directed experiment; the 96 uncovered suggestions
  were not pruned and the higher-priority open questions (AIS compartment, Na/K factorial) remain
  queued for future sessions.

## Verification

* `verify_task_file.py` on `t0025_brainstorm_results_5`: 0 errors.
* `verify_logs.py` on `t0025_brainstorm_results_5`: 0 errors.
* `verify_task_file.py` on `t0026` (created via `/create-task`): 0 errors.

## Files Created

* `tasks/t0025_brainstorm_results_5/` — brainstorm-results task folder.
* `tasks/t0026_<slug>/` — V_rest sweep follow-up task (slug determined by `/create-task`).

## Next Steps / Suggestions

Execute `t0026` via `/execute-task` to produce the V_rest sweep tuning curves.
