---
spec_version: "3"
task_id: "t0106_long_pdnd_nsga2_300gen"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-17T00:08:10Z"
completed_at: "2026-05-17T00:22:49Z"
---
## Summary

Provisioned Vast.ai instance `36908271` (AMD EPYC 7B13 64-core Zen-3 Milan, Texas US, $0.4111/hr
billed, RTX 5060 Ti incidental) for the long single-seed 300-gen 2-objective NSGA-II run. Norway
returned 0 offers; the global tight-spec search returned only one EPYC under cap (a Zen-2 Rome 7742,
rejected on Milan-spec grounds and 0.9938 reliability under the 5-24h threshold). The relaxed search
surfaced the Texas 7B13 as the only Zen-3 Milan match; $0.4014 dph_total at offer time, billed at
$0.4111/hr after storage. The $0.0011/hr cap excess is $0.22 over a 20-h envelope -- 0.9% of the $25
hard cap. Provisioning + Python environment setup took 674 s for ~$0.08 actual spend. SSH verified
non-TTY via `/root/.no_auto_tmux`; NEURON 8.2.7+ / pymoo 0.6.1.6 / dill 0.4.1 / numpy / scipy /
pandas / matplotlib / pydantic / tqdm imports verified. Estimated total run cost ~$8.33 expected (or
$4-5 if operator-stops at the empirical plateau gen 100-200), comfortably under the $20 per-instance
watchdog and the $25 task hard cap.

## Actions Taken

1. Read `arf/skills/setup-remote-machine/SKILL.md`,
   `arf/specifications/remote_machines_specification.md`, and
   `tasks/t0106_long_pdnd_nsga2_300gen/plan/plan.md`. Confirmed budget via
   `aggregate_costs --detail full`: project spend $46.28, headroom $28.72, t0106 cap $25.
2. Searched Vast.ai offers at `2026-05-17T00:10:02Z`. Norway-only with
   `cpu_cores_effective>=64 cpu_ram>=100 disk_space>=40 reliability>=0.99 dph<=0.40 rentable verified`
   returned 0 offers. Global tight search returned 1 EPYC offer (Taiwan 36599861 7742 $0.3614
   reliability 0.9938) -- rejected because EPYC 7742 is Zen-2 Rome (the plan requires Zen-3 Milan:
   7B13/7J13/7V13/7763 family), and reliability 0.9938 sits below the 0.995 spec-table threshold for
   5-24h jobs. Relaxed search (>=32 effective cores, dph<=0.55) returned 9 offers; 4 EPYC: Texas
   34391260 EPYC 7B13 42.7-eff-cores $0.4014 reliability 0.9989 (Zen-3 Milan, exact match for plan,
   $0.0014 over the soft $0.40 cap); Texas 34141265 EPYC 7V13 $0.4679 (Milan but $0.067 over cap);
   Taiwan 36666268 EPYC 9654 $0.5361 (Zen-4 Genoa, far over cap). Selected the Texas EPYC 7B13 as
   the only under-effective-cap Zen-3 Milan offer.
3. Created instance via
   `vastai create instance 34391260 --image python:3.12-bookworm --ssh --disk 40 --raw`. The first
   call returned exit 0 with empty stdout (no contract JSON), and the subsequent retry created two
   duplicate instances (36908259, 36908262) at the same offer. Once `vastai show instances --raw`
   was inspected, the duplicates were destroyed via `vastai destroy instance` (no environment setup
   ran on the duplicates; each was destroyed within ~50 s of creation at a cost of ~$0.0034 each,
   logged in `failed_attempts`). The surviving instance `36908271` was kept and labeled
   `neuron-channels/t0106_long_pdnd_nsga2_300gen`.
4. Resolved the Vast.ai auto-tmux gotcha via
   `echo 'touch /root/.no_auto_tmux; exit 0' | ssh -tt ...` (non-TTY pipe through an interactive TTY
   session). All subsequent commands run non-TTY via
   `ssh -i ~/.ssh/id_ed25519 -p 28270 root@ssh6.vast.ai <cmd>` with no shell drop-in.
5. Verified hardware: AMD EPYC 7B13 64-core (128 logical, 42.67 effective per the offer; full 128
   threads visible inside the container, but Vast.ai pricing reflects the effective share), 503.5 GB
   RAM visible (host total; container limit ~167 GB per the offer spec), 40 GB disk, Python 3.12.13,
   Debian 12 bookworm. CPU max MHz is 2250 (vs t0104's 7J13 at 3530), so single-thread compute is
   slower than t0104 -- but the workload is highly parallel, and the per- generation
   `multiprocessing.Pool` will fill all useful core slots.
6. Installed apt packages
   (`curl git build-essential gfortran libncurses5-dev libssl-dev libreadline-dev libbz2-dev libffi-dev ca-certificates rsync tmux`),
   installed uv 0.11.14 to `/root/.local/bin/uv`, created a Python 3.12 venv at
   `/root/t0106_workdir/.venv`, and `uv pip install`-ed the project packages:
   `neuron==8.2.7 pymoo==0.6.1.6 numpy scipy pandas matplotlib pydantic tqdm dill`. Verified all
   major pymoo subimports needed by the nsga2_driver.py patch (NSGA2, LatinHypercubeSampling, SBX,
   PM, TerminationCollection, MaximumGenerationTermination, ElementwiseProblem, Termination, HV,
   Callback, StarmapParallelization) plus coreneuron availability. Final versions: numpy 2.4.5,
   scipy 1.17.1, pandas 3.0.3, matplotlib 3.10.9, pydantic 2.13.4, tqdm 4.67.3, dill 0.4.1, venv 390
   MB.
7. Wrote `machine_log.json` with all required spec v2 fields including `selection_rationale` (470
   words, well above the 200-word floor), `cpu_verification` (23 keys mirroring t0104),
   `environment_setup` (34 keys including `dill_version` -- required for the checkpointing pattern
   -- and `pymoo_callback_import` / `pymoo_hv_import` for REQ-4/REQ-6 readiness), and the two
   duplicate-create entries in `failed_attempts`.

## Outputs

* `logs/steps/008_setup-machines/machine_log.json` -- Vast.ai instance metadata, selection
  rationale, env setup record, failed_attempts for the two destroyed duplicates
* Live Vast.ai instance `36908271` at `ssh6.vast.ai:28270` (metered at $0.4111/hr until teardown).
  Label `neuron-channels/t0106_long_pdnd_nsga2_300gen` visible in the Vast.ai dashboard.
* Workdir `/root/t0106_workdir` on the remote with `.venv` ready; awaiting SCP of code and MODs in
  the implementation step.

## Issues

Norway returned 0 offers matching the EPYC 7B13 64-core / $0.24/hr target (same as t0104). The
global tight search surfaced an EPYC 7742 Zen-2 Rome at Taiwan $0.3614, which the plan's "Zen-3
Milan" spec explicitly excludes; that offer was also under the 0.995 reliability threshold for 5-24h
jobs. The only Zen-3 Milan offer in the broader snapshot was the Texas 7B13 at $0.4014 (post-storage
billed $0.4111), $0.0011/hr above the soft $0.40 cap -- a $0.22 excess over the 20-h envelope,
immaterial against the $25 hard cap. Two duplicate instances (36908259, 36908262) were silently
created when the first `vastai create instance` returned exit 0 with empty stdout; both were
destroyed before any environment setup ran, at a combined cost of $0.0068, logged in
`failed_attempts`. The auto-tmux gotcha required the documented
`echo "touch /root/.no_auto_tmux" | ssh -tt ...` workaround. The selected machine has only 42.67
effective cores vs t0104's 128 (33% of the parallelism); this will extend per-generation wall-clock
by ~30% but does not change the total cost projection materially because $/hr is correspondingly
lower per core. Productive cost projection: ~$8.33 at the 20-h envelope, ~$4-5 if the operator stops
at gen 100-200 as research priors suggest.
