---
spec_version: "3"
task_id: "t0062_nmda_escape_with_ampa_priming"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T22:53:57Z"
completed_at: "2026-04-29T22:59:00Z"
---
# Step 9 — Implementation

## Summary

Wrote 6 task-specific Python files. Each E synapse gets a co-located AMPA `Exp2Syn` + NMDA
`NMDA_MgBlock` driven by a shared NetStim. Sweep ran in 269.80 s. AMPA priming (0.5 nS) **changes
the picture entirely vs t0061**: cell now fires 2-4 spikes at every gNMDA value. Peak spike count
(4) at gNMDA = 2.0 nS — the AMPA-NMDA synergy point.

## Actions Taken

1. Copied `NMDA_MgBlock.mod` and `run_nrnivmodl.cmd` from t0055.
2. Wrote 6 code modules (paths, constants, nmda_bootstrap, synapses_ampa_nmda, run_pd_only,
   plot_traces).
3. Each location now has both an AMPA Exp2Syn and an NMDA_MgBlock driven by a single shared NetStim
   with two NetCons; AMPA fixed at 0.5 nS, NMDA swept.
4. Ran 16 trials at theta=0, GABA=0; produced CSVs and 2 PNGs.

## Outputs

* All 6 code modules and the NMDA_MgBlock.mod copy.
* `voltage_traces_pd_only.csv`, `summary_pd_only.csv`, `wallclock.json`, `placement_seed0.json`.
* `voltage_response_grid.png` (8 panels), `voltage_response_overlay.png`.

## Issues

No issues encountered.
