---
spec_version: "3"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-25T00:23:06Z"
completed_at: "2026-05-25T00:38:00Z"
---
# Step 8: setup-machines

## Summary

Provisioned Vast.ai EPYC instance 37679733 (AMD EPYC 7B13, 128 vCPUs, 220 GB RAM) at $0.1615/hr —
10% cheaper than t0123's $0.1785/hr. SSH verified, NEURON + dependency stack installed at versions
byte-identical to t0123, all 13 channel mechanisms compiled and loaded. Vast.ai balance $11.20
verified above the $7 minimum required by the plan.

## Actions Taken

1. Spawned /setup-remote-machine subagent which verified Vast.ai balance ($11.20 >= $7) and
   provisioned offer 25209337 (cheapest EPYC matching plan filters).
2. Compiled t0080 MOD pack (13 mechanisms) with nrnivmodl; library byte-identical to t0114 / t0115 /
   t0122 / t0123.
3. SSH connection verified (`ssh6.vast.ai:39732`); environment ready for implementation step's SCP
   + NSGA-II launch.
4. Per-instance cost watchdog set at $5; task cap $6. Current accumulated cost $0.02.
5. machine_log.json written with full v2-spec fields.

## Outputs

* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/logs/steps/008_setup-machines/machine_log.json
* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/logs/steps/008_setup-machines/step_log.md (this file)

## Issues

No issues encountered. Instance is running, ready for implementation step to upload t0124 code/ and
launch NSGA-II.
