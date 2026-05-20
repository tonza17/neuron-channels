---
spec_version: "3"
task_id: "t0113_t0106_seed2247_replicate"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-20T00:09:52Z"
completed_at: "2026-05-20T00:29:30Z"
---
# Step 8: setup-machines

## Summary

Provisioned Vast.ai single instance 37107202 on offer 32827493 (AMD EPYC 7B13 64-core, 125.9 GB RAM,
64 effective cores, Quebec CA, reliability 0.9965, $0.2458/hr billed). SSH verified, mods compiled,
Python/NEURON/pymoo deps installed at versions matching t0112 exactly. Cost projection ~$0.6-1.1
against the $25 hard cap and $20 per-instance watchdog. Two setup-time failures recorded in
`failed_attempts`: a Vast.ai create-instance API race that produced a phantom instance 37106446 (no
cost), and an SSH key rejection on instance 37106453 caused by a literal backslash in the original
key comment (resolved by registering key id 855344 with a clean comment, ~$0.045 wasted).

## Actions Taken

1. Spawned the `/setup-remote-machine` subagent through `arf/skills/setup-remote-machine/SKILL.md`
   Phases 1-5, with budget context ($25 per-task cap, $20 per-instance watchdog, $41.21 project
   remainder).
2. The subagent searched Vast.ai for offers matching the t0106 / t0112 provisioning class (EPYC
   family, >=100 GB RAM, dph <= 0.40, reliability >= 0.99, compute_cap < 1200), selected an EPYC
   7B13 Quebec offer 29 percent cheaper than t0112's selection with 2x effective cores, and created
   instance 37107202.
3. SSH connectivity was verified end-to-end through `run_with_logs.py`. The subagent recorded
   `gpu_verified` = "NVIDIA GeForce RTX 4060 Ti" (idle on this CPU-only workload), CUDA 13.0 via
   driver 580.82.09.
4. Built the t0080 MOD library (`/root/t0113_workdir/mods/x86_64/libnrnmech.so`, 118,704 bytes,
   identical size to t0112). All 13 t0080 mechanisms verified loadable from NEURON.
5. Installed Python 3.12.13 dependencies pinned to t0112 versions (neuron 8.2.7+, pymoo 0.6.1.6,
   dill 0.4.1, numpy 2.4.6, scipy 1.17.1, pandas 3.0.3, matplotlib 3.10.9, pydantic 2.13.4, tqdm
   4.67.3) via `pip --break-system-packages` (uv intentionally not used on the remote, per t0112
   pattern).
6. Wrote `logs/steps/008_setup-machines/machine_log.json` per
   `arf/specifications/remote_machines_specification.md`.

## Outputs

* `tasks/t0113_t0106_seed2247_replicate/logs/steps/008_setup-machines/machine_log.json` — v2-schema
  machine log for instance 37107202 (created_at, ready_at, failed_attempts, environment_setup,
  mod_compile_ok, gpu_verified, ssh_notes).

## Issues

Two setup-time failures, both resolved before the implementation step:

1. Vast.ai create-instance API race produced a phantom instance 37106446; destroyed and recorded in
   `failed_attempts` with zero wasted cost.
2. The pre-existing Vast.ai SSH key (id 801863, comment `shefuniad\md1avn@...`) was rejected by the
   Vast.ai SSH proxy on instance 37106453; the literal backslash in the comment field corrupts key
   parsing on the proxy side. Registered a new key entry id 855344 with comment `md1avn-t0113`, SSH
   connected on first attempt afterward. ~$0.045 wasted on 37106453.

Note for follow-on tasks: attach SSH key id 855344, not 801863. Set `PYTHONIOENCODING=utf-8` and
`PYTHONUTF8=1` in the local shell before pip/ssh commands wrapped in run_with_logs.
