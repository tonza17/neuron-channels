---
spec_version: "3"
task_id: "t0091_morphology_extended_nsga2_v1"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-08T12:48:29Z"
completed_at: "2026-05-08T13:03:30Z"
---

## Summary

Provisioned a Vast.ai EPYC 7B13 64-core CPU instance (instance_id 36344985, machine_id 55891 — the
same host that t0080 used) for the joint 68-d NSGA-II run. Offer rate $0.2290/hr, instance billing
rate $0.2452/hr; worst-case 16 h x $0.2452 = $3.92 leaves $0.08 buffer under the $4.00 hard cap;
central case 10–12 h ≈ $2.45–$2.94. SSH verified, CPU verified (64 cores, 503 GB RAM, 40 GB disk),
environment ready (Python 3.12, NEURON 8.2.7+ with HH smoke test, pymoo 0.6.1.6 with NSGA-II
import chain verified including `pymoo.parallelization.starmap.StarmapParallelization`).

## Actions Taken

1. Ran prestep to mark step 8 as in_progress.
2. Spawned the `/setup-remote-machine` subagent through Phase 5 only (Phase 6+ is implementation
   work).
3. Subagent searched Vast.ai offers, selected EPYC 7B13 64-core CPU node matching t0080-t0083
   spec, provisioned instance 36344985.
4. Subagent verified SSH, CPU specs, NEURON HH smoke test, nrnivmodl smoke compile, pymoo full
   import chain.
5. Subagent wrote `machine_log.json` with all v2 required fields per
   `arf/specifications/remote_machines_specification.md`.

## Outputs

* `tasks/t0091_morphology_extended_nsga2_v1/logs/steps/008_setup-machines/machine_log.json`
* Active Vast.ai instance 36344985 at `ssh4.vast.ai:24984` (141.0.85.200, Norway)
* Setup cost: $0.04 (10 min provisioning at $0.2452/hr)

## Issues

No issues encountered. Vast.ai auto-tmux SSH gotcha resolved per t0080's documented procedure (set
`/root/.no_auto_tmux`). `gpu_verified: false` is correct for this CPU-only NEURON workload;
`cpu_verified: true` records 64 cores billed.
