---
spec_version: "3"
task_id: "t0123_bedb_mi_atp_per_spike_nsga2"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-24T13:43:23Z"
completed_at: "2026-05-24T13:50:00Z"
---
## Summary

Provisioned Vast.ai EPYC instance 37599740 (32-core AMD EPYC 7452 Zen-2 at 2.35 GHz, 62.9 GB RAM, 40
GB disk, Norway) at $0.1785/hr — well under the $0.30/h budget assumption. Compiled all 13 t0080
NEURON channels, verified mechanisms loadable, installed sklearn 1.8.0 (new dependency vs t0122
required by `mi_estimator.py`). Instance is healthy and labelled
`neuron-channels/t0123_bedb_mi_atp_per_spike_nsga2`; SSH at `root@ssh2.vast.ai:39740`. Vast.ai
balance $14.37 (above the $7 gating threshold the operator confirmed).

## Actions Taken

1. Spawned a general-purpose subagent to execute the /setup-remote-machine skill through Phase 5
   (Prepare the Environment), reading `plan/plan.md` `## Remote Machines` for the provisioning spec.
2. The subagent searched the Vast.ai offers, picked a 32-core EPYC 7452 at $0.1785/hr passing the
   0.99 reliability floor and the 5-24h spec floor (0.995), and provisioned instance 37599740 in 399
   s with zero failed attempts.
3. Verified SSH connectivity, installed apt build dependencies (build-essential, gfortran, libssl,
   libreadline, libbz2, libffi, rsync, tmux, ...), set up Python 3.12.13 with NEURON 8.2.7+, pymoo
   0.6.1.6, dill, numpy, pandas, scipy, matplotlib, pydantic, tqdm, and sklearn 1.8.0.
4. Compiled the 13 t0080 NEURON channels at /root/t0123_workdir/mods/x86_64/libnrnmech.so (118704
   bytes; byte-identical to the t0122/t0115/t0114 builds).
5. Verified every mechanism loadable via `h.<mech>` introspection (bkt80, calt80, catt80, iht80,
   kdrt80, kv3t80, kv4t80, kv7t80, napt80, nart80, nav16t80, skahpt80, skt80).
6. Wrote `machine_log.json` (v2 schema) with all required fields plus optional `search_started_at`,
   `total_provisioning_seconds`, `failed_attempts: []`, `label`.

## Outputs

* `tasks/t0123_bedb_mi_atp_per_spike_nsga2/logs/steps/008_setup-machines/machine_log.json`.
* Vast.ai instance 37599740, label `neuron-channels/t0123_bedb_mi_atp_per_spike_nsga2`, SSH key
  injected.
* Compiled `libnrnmech.so` on the remote machine (will be reused for the NSGA-II + post-hoc reruns).

## Issues

No issues encountered. Instance is healthy and billing at $0.1785/hr — implementation will start
promptly to minimise idle time.
