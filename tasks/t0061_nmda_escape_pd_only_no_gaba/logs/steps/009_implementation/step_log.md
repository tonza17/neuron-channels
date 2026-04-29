---
spec_version: "3"
task_id: "t0061_nmda_escape_pd_only_no_gaba"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T22:22:09Z"
completed_at: "2026-04-29T22:25:00Z"
---
# Step 9 — Implementation

## Summary

Wrote 6 task-specific Python files plus copied NMDA_MgBlock.mod and run_nrnivmodl.cmd from t0055.
Reused t0059's cell + placement + neuron bootstrap primitives via library imports. Built a custom
NmdaPair (one NMDA_MgBlock POINT_PROCESS per Location, no AMPA, no GABA), wrote a focused 16-trial
runner, plotted via matplotlib. Sweep ran in 118.14 s. Headline: NMDA shows a sharp Mg-block
threshold between gNMDA=1.0 nS (no spike, peak -58.89 mV) and gNMDA=2.0 nS (3 spikes, peak +11.29
mV) — regenerative escape. Above gNMDA=5 nS, the NMDA plateau widens to 200-400 ms.

## Actions Taken

1. Copied `NMDA_MgBlock.mod` and `run_nrnivmodl.cmd` from t0055 into t0061's `code/mod/` and
   `code/`.
2. Wrote `paths.py`, `constants.py` (8 gNMDA values), `nmda_bootstrap.py` (compile + load
   nrnmech.dll), `nmda_synapse.py` (NmdaPair + builder + scheduler), `run_pd_only.py` (16-trial loop
   with HH save-and-zero), `plot_traces.py` (panel grid + overlay).
3. Initial run failed (Location field name mismatch — used `segment_x`, actual field is
   `section_x`); fixed and re-ran.
4. Sweep produced `voltage_traces_pd_only.csv`, `summary_pd_only.csv`, `wallclock.json`,
   `placement_seed0.json`. Plots produced `voltage_response_grid.png` and
   `voltage_response_overlay.png`.

## Outputs

* `tasks/t0061_nmda_escape_pd_only_no_gaba/code/{paths,constants,nmda_bootstrap,nmda_synapse,run_pd_only,plot_traces}.py`
* `tasks/t0061_nmda_escape_pd_only_no_gaba/code/mod/NMDA_MgBlock.mod` (copy from t0055)
* `tasks/t0061_nmda_escape_pd_only_no_gaba/code/run_nrnivmodl.cmd` (copy from t0055)
* `tasks/t0061_nmda_escape_pd_only_no_gaba/results/voltage_traces_pd_only.csv`
* `tasks/t0061_nmda_escape_pd_only_no_gaba/results/{summary_pd_only.csv, wallclock.json, placement_seed0.json}`
* `tasks/t0061_nmda_escape_pd_only_no_gaba/results/images/voltage_response_grid.png`
* `tasks/t0061_nmda_escape_pd_only_no_gaba/results/images/voltage_response_overlay.png`

## Issues

One iteration: Location.section_x (not segment_x). Fixed in place.
