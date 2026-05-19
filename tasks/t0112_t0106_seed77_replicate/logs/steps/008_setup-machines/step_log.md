---
spec_version: "3"
task_id: "t0112_t0106_seed77_replicate"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-19T15:31:43Z"
completed_at: "2026-05-19T15:41:00Z"
---
# Step 8: Setup Remote Machines

## Summary

Spawned the /setup-remote-machine subagent which provisioned a single Vast.ai EPYC 7B13 instance in
Quebec, verified SSH and GPU, compiled the t0080 MOD library on the remote, and confirmed the Python
\+ NEURON + pymoo stack is ready. The orchestrator-level cost cap is $25 and the per-instance
watchdog is $20. Provisioning took 169 s; expected total spend on this instance is ~$1.50.

## Actions Taken

1. Spawned a `/setup-remote-machine` subagent restricted to the t0112 worktree, with explicit
   filters (EPYC 7B13/7763, >= 100 GB RAM, RTX 3060 Ti or equivalent idle GPU, reliability >= 0.99,
   dph <= 0.40) mirroring t0106's pattern.
2. Subagent searched Vast.ai (24 offers), selected EPYC 7B13 Quebec at $0.3426/h (only Zen-3 Milan
   match), created instance 37076157, verified SSH (ssh6.vast.ai:36156), and confirmed NEURON
   8.2.7+, Python 3.12.13, pymoo 0.6.1.6, dill 0.4.1.
3. Uploaded the t0080 `mods/` directory and ran `nrnivmodl` on the remote; verified
   `/root/t0112_workdir/mods/x86_64/libnrnmech.so` (118,704 bytes) loads and exposes all 13
   channels.
4. Wrote `machine_log.json` (top-level list, single entry, all required keys per
   `remote_machines_specification.md`) and `offers_raw.json` (audit trail of the 24-offer search
   snapshot).

## Outputs

* `tasks/t0112_t0106_seed77_replicate/logs/steps/008_setup-machines/machine_log.json`
* `tasks/t0112_t0106_seed77_replicate/logs/steps/008_setup-machines/offers_raw.json`
* `tasks/t0112_t0106_seed77_replicate/logs/steps/008_setup-machines/step_log.md`
* Vast.ai instance 37076157 live at `ssh6.vast.ai:36156`

## Issues

The only available Milan offer was Quebec at $0.3426/h. The cheaper $0.1934/h EPYC 7R32 Italy offer
was excluded because it is Zen-2, not Zen-3 (the plan explicitly requires Milan to mirror t0106's
substrate). The slight cost premium (~$0.15/h) is acceptable given the $20 per-instance watchdog and
$25 task cap.
