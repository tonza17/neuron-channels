---
spec_version: "3"
task_id: "t0083_bedb_v3_extend_nsga2_gen8plus"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-05T13:57:30Z"
completed_at: "2026-05-05T14:11:46Z"
---
# Step 8 -- Setup Machines

## Summary

Provisioned Vast.ai instance **36186200** (AMD EPYC 7B13 64-Core Processor, 42.67 effective cores in
this fractional rental, 995 GB host RAM visible / 552 GB cgroup limit, 25 GB container disk, Texas
US, machine_id 27647) at **$0.3209/hr**. Plan target was the same EPYC 7B13 64-core class as t0081
at $0.2382/hr, but t0081's exact offer 31639237 (machine 55891 in Norway) was unavailable today.
After surveying all current >=99% reliable offers with >=64 GB RAM and >=36 effective cores, this
$0.3209/hr Texas EPYC 7B13 was the cheapest option that preserves microarchitecture identity with
t0081, which is critical for the smoke gate's substrate-consistency check. Cost projection: $1.93
best case (5 gens, 6.0 h) to $4.46 worst case (10 gens, 13.4 h), under the $5.00 hard cap. Installed
NEURON 8.2.7, pymoo 0.6.1.6, numpy 2.4.4, scipy 1.17.1, matplotlib 3.10.9 in a uv-managed venv at
`/root/t0083_workdir/.venv`. Verified NEURON HH smoke insert, full v3 substrate MOD compile (all 13
t80 channel files compile cleanly into a 118 KB libnrnmech.so), all 13 v3 SUFFIXes load and insert
into a fresh `h.Section`, and pymoo NSGA2 + StarmapParallelization + Population imports. SSH proxy's
auto-tmux disabled. Provisioning + environment-setup wall-clock: ~13.5 min. No blockers for
implementation phase.

## Actions Taken

1. Initialized search timestamp (`search_started_at: 2026-05-05T13:57:30Z`).
2. Read `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/plan/plan.md` Section "Remote Machines"
   requirements: AMD EPYC 7B13 64-core, $0.2382/hr target (max $0.24), 503 GB RAM (min 64 GB), 25 GB
   disk, Ubuntu 22.04 / Debian 12 with NEURON 8.2.7 + NetPyNE 1.1.1 + pymoo 0.6.x + numpy/scipy.
3. Read `arf/specifications/remote_machines_specification.md` v2 schema to confirm required
   `machine_log.json` fields including `search_started_at`, `total_provisioning_seconds`,
   `failed_attempts`, `label`.
4. Verified current project spend via `aggregate_costs`: $8.13 of $20.00 used, $11.87 remaining.
   Worst-case t0083 cost ($5.00) would still leave the project at $13.13 / $20.00, well under the
   $16.00 warn threshold.
5. Verified Vast.ai CLI authentication (`vastai show user`) and that the registered SSH key
   (`shefuniad\md1avn@TEN00BE4360B45A`, key id 801863) is present on the account.
6. Confirmed no pre-existing instances are running (`vastai show instances --raw` returned `[]`).
7. Searched offers with
   `cpu_cores_effective>=64 cpu_ram>=64 disk_space>=25 reliability>=0.99 dph<0.30 rentable=true verified=true`
   -- no EPYC 7B13 64-core matches.
8. Broadened search to
   `cpu_cores_effective>=36 cpu_ram>=64 disk_space>=25 reliability>=0.99 rentable=true verified=true`
   (50 offers) and filtered for EPYC 7B13: 5 candidates total, of which only 3 have >=64 GB RAM and
   >=36 cores under $0.50/hr. Cheapest was offer 24887414 at $0.3209/hr (43-core fractional rental
   on machine 27647 in Texas, EPYC 7B13 64-Core Processor, 332 GB RAM advertised, 0.9992
   reliability).
9. Documented selection rationale in `selection_rationale` field: rejected the cheaper Threadripper
   PRO 5995WX at $0.1747/hr (63 GB RAM, below 64 GB minimum); rejected the Xeon E5-2690 v2 at
   $0.0947/hr (Ivy Bridge uArch, ~2-3x slower per-core, substrate-consistency risk); rejected the
   $0.5608/hr 64-core EPYC 7B13 in Quebec (would push 10-gen worst-case cost to $5.97, over the
   $5.00 cap). Selected offer 24887414 as the optimal price/EPYC-identity/cost-cap-headroom balance.
10. Ran `vastai create instance 24887414 --image python:3.12-bookworm --ssh --disk 25 --raw` --
    instance 36186200 created, `created_at: 2026-05-05T14:01:22Z`.
11. Labeled the instance `neuron-channels/t0083_bedb_v3_extend_nsga2_gen8plus` for dashboard
    visibility.
12. Polled `vastai show instance 36186200 --raw` until `actual_status == "running"` (achieved on
    first poll, ~90 s after instance creation).
13. Disabled SSH-proxy auto-tmux via interactive `ssh -tt` -> `touch /root/.no_auto_tmux`. After
    this, non-TTY SSH commands work directly via `ssh2.vast.ai:26200`.
14. Verified hardware: `lscpu` reports AMD EPYC 7B13 64-Core Processor with 128 SMT threads and 64
    physical cores per socket; `free -g` reports 995 GB total / 972 GB available; `df -h /` shows 25
    G disk; `cat /sys/fs/cgroup/cpu.max` reports `4095999/100000` (40.96 effective cores cgroup
    quota); `cat /sys/fs/cgroup/memory.max` reports 552 GB cgroup memory limit; OS is Debian 12
    bookworm in container, kernel Linux 6.8.0-52-generic Ubuntu 22.04 host. Public IP 38.247.78.2,
    machine_id 27647, hostname `d0a7cdb945df`.
15. Installed apt build deps:
    `curl git build-essential gfortran libncurses5-dev libssl-dev libreadline-dev libbz2-dev libffi-dev`.
16. Installed `uv 0.11.9` via the official installer at `/root/.local/bin/uv`.
17. Created venv at `/root/t0083_workdir/.venv` with Python 3.12.13.
18. Installed Python deps via
    `uv pip install --python .venv/bin/python neuron==8.2.7 pymoo==0.6.1.6 numpy scipy matplotlib`.
    uv resolved 27 packages and installed in <1 second (cached).
19. Verified imports: NEURON 8.2.7+ (HH smoke test: `Section.insert("hh")` -> `gnabar_hh` default
    0.12 OK), pymoo 0.6.1.6 (NSGA2, StarmapParallelization at `pymoo.parallelization.starmap` -- NOT
    the deprecated `pymoo.core.problem` path -- Population, LHS, minimize, ElementwiseProblem all
    OK), numpy 2.4.4, scipy 1.17.1, matplotlib 3.10.9.
20. SCP'd a single v3 mod file (`nav16t80.mod`) to `/root/t0083_workdir/mod_test/`, ran
    `nrnivmodl .` -> compiled cleanly to `x86_64/.libs/libnrnmech.so` (22 KB), loaded via
    `h.nrn_load_dll` from a fresh CWD (avoiding NEURON's auto-discovery double-load) and inserted
    SUFFIX `nav16t80` into a `h.Section` -- gbar default 0.0 confirmed.
21. SCP'd the FULL v3 mods directory (`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods`, 13
    .mod files) to `/root/t0083_workdir/v3_mods_test/`, ran `nrnivmodl .` -> compiled all 13 files
    cleanly into a 118 KB libnrnmech.so. Loaded via `h.nrn_load_dll` and inserted all 13 SUFFIXes
    (bkt80, calt80, catt80, iht80, kdrt80, kv3t80, kv4t80, kv7t80, napt80, nart80, nav16t80,
    skahpt80, skt80) into one `h.Section` -- all 13 channels registered correctly in NEURON's symbol
    table. v3 substrate compile chain verified end-to-end.
22. Recorded all hardware specs, environment setup details, smoke-test results, SSH details, and
    cost-so-far in `machine_log.json` per the v2 schema (including `search_started_at`,
    `total_provisioning_seconds`, `failed_attempts: []`, `label`, and `cpu_verification` /
    `environment_setup` / `ssh_notes` extension blocks for downstream reference).

## Outputs

* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/logs/steps/008_setup-machines/machine_log.json`
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/logs/steps/008_setup-machines/step_log.md`

## Issues

The plan-targeted EPYC 7B13 64-core class at $0.2382/hr (matching t0081's exact offer) was
unavailable today on Vast.ai. Selected the cheapest current EPYC 7B13 offer (24887414, $0.3209/hr,
42.67 effective cores) as the closest microarchitecture match. This is +$0.083/hr above the plan's
soft cap but stays within the $5.00 hard cost cap given the 10-generation worst-case envelope ($4.46
projected). The 1.5x per-cell wall-clock penalty (43-core fractional rental vs t0081's 64-core) is
documented in plan.md Risks & Fallbacks and is the primary cost-cap exposure for the NSGA-II
continuation run; the $5.00 cost-cap watchdog is the backstop.
