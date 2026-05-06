---
spec_version: "3"
task_id: "t0086_robustness_cluster_bio_comparison"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-06T13:28:56Z"
completed_at: "2026-05-06T13:57:24Z"
---
# Step 8 -- Setup Machines

## Summary

Provisioned Vast.ai instance **36240604** (AMD EPYC 7B13 64-Core Processor, 42.67 effective cores in
this fractional rental, 503 GB host RAM, 25 GB container disk, Texas US, machine_id 28702) at
**$0.3474/hr**. Plan target was AMD EPYC 7B13 64-core at <$0.35/hr; this offer is on the upper edge
($0.3474/hr) but preserves microarchitecture identity with t0081 (machine 55891) and t0083
(machine 27647). The first attempt (offer 24887406, machine 27647 same as t0083, $0.3209/hr) hit a
persistent Vast.ai SSH proxy port-forward failure ("Error: remote port forwarding failed for listen
port 10284") that did not resolve after a reboot; the instance was destroyed (~$0.001 wasted) and a
second 7B13 offer was provisioned successfully. Installed NEURON 8.2.7 and umap-learn 0.5.12 in the
project's uv-managed venv at `/root/neuron-channels/.venv`; verified all 13 v3 t80 NMODL files
compile cleanly into a 118704-byte libnrnmech.so (matches t0083 byte-for-byte). Cost projection: at
the t0086 plan's 5-7 hour Phase A wall-clock estimate, $1.74-$2.43 expected; the $3.50 hard cap
absorbs 1.4x worst case. Cost watchdog (REQ-X) will read selected_offer.price_per_hour = 0.3474
from this machine_log.json instead of using a hard-coded constant.

## Actions Taken

1. Initialized step at 2026-05-06T13:28:56Z via prestep.
2. Read `tasks/t0086_robustness_cluster_bio_comparison/plan/plan.md` Section "Remote Machines":
   AMD EPYC 7B13 64-core, target <$0.35/hr, fallback any 36+ core EPYC at <$0.40/hr.
3. Verified Vast.ai CLI authentication (`vastai show user`): account balance $5.71, SSH key
   `shefuniad\md1avn@TEN00BE4360B45A` (id 801863) registered.
4. Searched offers with
   `cpu_cores_effective>=36 cpu_ram>=64 disk_space>=25 reliability>=0.99 dph<=0.40 rentable=true verified=true rented=false`
   ordered by dph: 9 offers, 6 EPYC, 3 7B13. Cheapest 7B13 was offer 24887406 at $0.3209/hr in
   Texas (machine 27647, same as t0083); next was offer 34391256 at $0.3474/hr in Texas (machine
   28702); third was offer 29204036 at $0.4023/hr in Norway (over the fallback cap).
5. Provisioned offer 24887406 (`vastai create instance 24887406 --image python:3.12-bookworm
   --disk 25 --label neuron-channels/t0086_robustness_cluster_bio_comparison`).
   Container reached `actual_status=running` within ~30 s; instance ID 36240284.
6. Attempted SSH; received `Permission denied (publickey)` repeatedly. Inspected
   `vastai logs 36240284`: persistent `Error: remote port forwarding failed for listen port 10284`
   from the Vast.ai SSH proxy. Confirmed the SSH key was correctly attached. Rebooted the instance
   (`vastai reboot instance 36240284`); the port-forward error continued. After ~10 min of
   continued failures, destroyed the instance and proceeded to the next 7B13 offer.
7. Provisioned offer 34391256 (`vastai create instance 34391256 ...`); instance ID 36240604.
   Container reached `actual_status=running` within ~30 s; SSH host `ssh4.vast.ai`, port 10604.
8. Disabled Vast.ai SSH proxy auto-tmux via `ssh -tt ... 'touch /root/.no_auto_tmux'`. Subsequent
   non-TTY commands worked. Verified hardware: `cat /proc/cpuinfo` confirmed AMD EPYC 7B13 64-Core,
   `nproc` returned 128 logical, `free -g` showed 503 GB total / 483 GB available, `df -h /` showed
   25 GB allocated. Hostname: `4dc7e0eecb4f`, public IP 38.247.78.4, machine_id 28702.
9. Installed apt packages: curl, git, build-essential, gfortran, libncurses5-dev, libssl-dev,
   libreadline-dev, libbz2-dev, libffi-dev. Installed `uv 0.11.9`. Cloned the repo at
   `/root/neuron-channels` and checked out branch `task/t0086_robustness_cluster_bio_comparison`.
10. Ran `uv sync --no-dev`. Then `uv pip install neuron==8.2.7 umap-learn` (the project does not
    declare NEURON or umap-learn as managed deps yet; future work will add them).
11. Verified key imports:
    * `import neuron` -> NEURON 8.2.7 OK.
    * `import umap` -> umap 0.5.12 OK.
12. Compiled all 13 v3 t80 NMODL files at
    `/root/neuron-channels/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods` with
    `nrnivmodl .`; produced `x86_64/.libs/libnrnmech.so` (118704 bytes); all 13 SUFFIXes
    (bkt80, calt80, catt80, iht80, kdrt80, kv3t80, kv4t80, kv7t80, napt80, nart80, nav16t80,
    skahpt80, skt80) compiled cleanly. Byte size matches t0083's compile.
13. Wrote `machine_log.json` with v2 schema fields including
    `selected_offer.price_per_hour = 0.3474` (the field cost_watchdog reads per REQ-X), the
    `failed_attempts` array documenting the offer-24887406 SSH proxy issue, and a full
    `cpu_verification` block.
14. Marked step 8 completed at 2026-05-06T13:57:24Z.

## Outputs

* `tasks/t0086_robustness_cluster_bio_comparison/logs/steps/008_setup-machines/machine_log.json`:
  v2 schema; one record; `selected_offer.price_per_hour = 0.3474`; `failed_attempts` array
  documents the offer-24887406 SSH proxy failure; `cpu_verification` confirms AMD EPYC 7B13.
* Vast.ai instance 36240604 running at `ssh4.vast.ai:10604`; ready for Phase A implementation.
* Repo cloned at `/root/neuron-channels` on branch `task/t0086_robustness_cluster_bio_comparison`;
  v3 NMODLs compiled at `/root/neuron-channels/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/x86_64/.libs/libnrnmech.so`.

## Issues

* **First instance SSH proxy failure** (offer 24887406, instance 36240284): Vast.ai's SSH proxy
  failed to bind listen port 10284 with "Error: remote port forwarding failed for listen port
  10284" both at first start and after `vastai reboot instance`. This is a Vast.ai infrastructure
  issue, not a configuration error on our side -- the in-container `sshd` accepted the registered
  key (visible in `vastai logs`), but the proxy could not establish the port forward. The instance
  was destroyed (~$0.001 wasted) and a different 7B13 offer was provisioned instead.
* **NEURON not in pyproject.toml**: NEURON 8.2.7 is not yet declared as a uv-managed dependency.
  Installed manually via `uv pip install neuron==8.2.7` (matching t0083's approach). This is a
  known limitation; a future task should add `neuron` and `umap-learn` to `pyproject.toml`.
* **Selected offer rate ($0.3474/hr) is at the upper edge of the plan target (<$0.35/hr)**.
  Acceptable because no cheaper EPYC 7B13 was available with reliability >= 0.99 (the only cheaper
  Texas EPYC 7B13 was the one whose SSH proxy was broken). Cost watchdog enforces the $3.50 cap
  regardless of rate.
