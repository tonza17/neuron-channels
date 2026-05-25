---
spec_version: "3"
task_id: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-25T12:56:37Z"
completed_at: "2026-05-25T13:08:45Z"
---
# Step 8: setup-machines

## Summary

Spawned the `/setup-remote-machine` subagent to provision Vast.ai instance `37767708` (AMD EPYC 7C13
64-core, 32 effective vCPUs, 64 GB RAM, Zen-3 Milan, Virginia US) at $0.1844/hr realised. SSH
endpoint `ssh2.vast.ai:17708` reachable on first attempt. Python 3.12.13 + NEURON 8.2.7+ + pymoo
0.6.1.6 + dill 0.4.1 environment installed at versions byte-identical to t0124; all 13 t0080 MOD
mechanisms compiled (`libnrnmech.so` byte-identical to the t0114-t0124 lineage). Vast.ai balance
verified at $8.61 (above the $7 plan minimum). Cost projection $0.37-$0.55 for the 2-3 hr run --
well under the $6 task cap.

## Actions Taken

1. Ran `prestep setup-machines` to mark the step in-progress.
2. Spawned `/setup-remote-machine` subagent (Phases 1-5: select offer, provision, SSH check, verify
   env, prepare workspace). Subagent ran all CLI through `run_with_logs.py`.
3. Subagent selected EPYC 7C13 offer 34684543 (cheapest qualifying EPYC at provisioning time;
   t0124's EPYC 7B13 offer was no longer available) and provisioned instance `37767708` at
   $0.1844/hr.
4. Subagent verified SSH, installed Python dependencies (versions byte-identical to t0124), compiled
   all 13 t0080 MOD mechanisms via `nrnivmodl`, and confirmed `libnrnmech.so` size / checksum match
   the t0114-t0124 lineage.
5. Subagent wrote `machine_log.json` with all v2-spec required fields populated.

## Outputs

* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/logs/steps/008_setup-machines/machine_log.json` --
  complete v2-spec record (instance 37767708, EPYC 7C13, SSH endpoint, env versions).
* `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/logs/steps/008_setup-machines/step_log.md` -- this
  log.

## Issues

The subagent flagged an orphaned Vast.ai instance `37545908` (label
`neuron-channels/t0122_dsi_cytoplasm_volume_nsga2`) running 33+ hours at $0.184/hr on the account.
The subagent did NOT touch it (out of t0126 scope) but flagged it for the user. Recommend the user
runs `vastai destroy instance 37545908` to recover the leaked spend; it is unrelated to t0126.
