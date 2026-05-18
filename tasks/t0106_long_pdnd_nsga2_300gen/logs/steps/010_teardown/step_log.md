---
spec_version: "3"
task_id: "t0106_long_pdnd_nsga2_300gen"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-18T01:23:16Z"
completed_at: "2026-05-18T01:27:00Z"
---
# Step 10: teardown

## Summary

Verified that the orchestrator had already SCP'd all six expected NSGA-II result files (Pareto
front, full evaluations, HV trajectory, init pop, evaluation seeds, dill checkpoint) and the three
expected implementation log artifacts (hv_trace.jsonl, nsga2_run.log, plus orchestrator-managed
launch_record.json, step_log.md, and snapshots/) back to the local task folder. Compared remote and
local sizes for the six results/data files: all matched within one byte (CRLF normalisation noise),
so no further SCP was needed. Destroyed Vast.ai instance 36908271 via
`vastai destroy instance 36908271 -y` and confirmed removal via `vastai show instances --raw` (zero
instances remaining) and `vastai show instance 36908271 --raw` (errors with NoneType on missing
start_date — the standard "instance gone" signature). Filled in `destroyed_at`,
`total_duration_hours` (25.2232 h), `total_cost_usd` ($10.3693 = $0.4111/hr * 25.2232 h) in
`machine_log.json`. Wrote `remote_machines_used.json` (one entry) and `costs.json` (single line item
`vast-ai-epyc-7b13: 10.3693`). Final billed wall-clock cost ran $0.48 over the NSGA-II driver's
self-reported $9.89 (productive 24.1 h) because provisioning (~11 min) plus operator-stop idle (~63
min between gen 39 end and destroy) are also billed. Verificator `verify_machines_destroyed.py`
returned PASSED with 0 errors and 3 advisory warnings (long-running job and no formal
checkpoint_path field, both expected for this CPU NSGA-II workload).

## Actions Taken

1. Listed local `tasks/t0106_long_pdnd_nsga2_300gen/results/data/` and confirmed all six expected
   files present: `all_evaluations_seed44.json` (8.12 MB), `pareto_front_seed44.json` (29 KB),
   `hv_trajectory_seed44.json` (7.3 KB), `init_pop_seed44.json` (173 KB), `evaluation_seeds.json`
   (118 B), `nsga2_checkpoint_seed44.json` (8.09 MB). Listed local `logs/steps/009_implementation/`
   and confirmed `hv_trace.jsonl` (3.8 KB), `nsga2_run.log` (14.7 KB), `launch_record.json` (6.2
   KB), `step_log.md` (4.4 KB), and `snapshots/` with three `.json` snapshots present.
2. SSH'd to `ssh6.vast.ai:28270` using `C:/Users/md1avn/.ssh/id_ed25519` (default WSL `~/.ssh/` was
   empty; key actually lives under the Windows profile). Listed remote
   `/root/t0106_workdir/tasks/t0106_long_pdnd_nsga2_300gen/results/data/` and confirmed remote sizes
   matched local within one byte. The remote `logs/steps/009_implementation/checkpoints/` directory
   had 39 intermediate dill checkpoints (`checkpoint_seed44_gen0001.pkl` through `gen0039.pkl`,
   total ~95 MB), which are not in the expected-file list and whose final state is already captured
   in `nsga2_checkpoint_seed44.json` — left on the remote (destroyed with the instance).
3. Captured final billing metadata via `vastai show instance 36908271 --raw`: `dph_total=0.4111`,
   `start_date=2026-05-17T00:12:52.797768Z`, `uptime_mins=1511.89`, `actual_status=running`. Ran
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0106_long_pdnd_nsga2_300gen -- vastai destroy instance 36908271 -y`;
   stdout was `destroying instance 36908271.`. Verified with `vastai show instances --raw` (zero
   instances) and `vastai show instance 36908271 --raw` (Python TypeError on `start_date`, the
   standard "instance no longer exists" signature).
4. Updated `tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/008_setup-machines/machine_log.json`:
   `destroyed_at="2026-05-18T01:26:15Z"`, `total_duration_hours=25.2232`, `total_cost_usd=10.3693`.
   Wrote `results/remote_machines_used.json` with one machine entry (provider `vast.ai`, machine_id
   `36908271`, gpu `RTX 5060 Ti (idle, unused; CPU-only NEURON workload on AMD EPYC 7B13)`,
   gpu_count 1, ram_gb 504, duration_hours 25.2232, cost_usd 10.3693). Wrote `results/costs.json`
   with `total_cost_usd=10.3693` and `breakdown={"vast-ai-epyc-7b13": 10.3693}`.
5. Ran
   `uv run python -m arf.scripts.verificators.verify_machines_destroyed t0106_long_pdnd_nsga2_300gen`
   via run_with_logs: PASSED with 0 errors and 3 warnings (`RM-W001` API "unreachable" on the
   destroyed instance, `RM-W003` 25.2h > 12.0h long-run advisory, `RM-W006` no `checkpoint_path` set
   on the machine_log entry — all expected and non-blocking).

## Outputs

* `tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/008_setup-machines/machine_log.json` (updated:
  `destroyed_at`, `total_duration_hours`, `total_cost_usd`).
* `tasks/t0106_long_pdnd_nsga2_300gen/results/remote_machines_used.json` (created, one machine).
* `tasks/t0106_long_pdnd_nsga2_300gen/results/costs.json` (created, `total_cost_usd=10.3693`, one
  breakdown line).
* `tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/010_teardown/step_log.md` (this file).
* Vast.ai instance `36908271` destroyed at `2026-05-18T01:26:15Z`.

## Issues

* `verify_machines_destroyed.py` accepts the task ID as a positional argument, not via `--task-id`
  (the SKILL.md `Teardown Protocol` shows `--task-id`, but the script's argparse rejects it). Used
  positional form.
* SSH key lives under the Windows user profile `C:/Users/md1avn/.ssh/id_ed25519` rather than at
  `~/.ssh/` (which under Git Bash resolves to an empty `/u/.ssh/`). Hard-coded the absolute path on
  the `ssh -i` flag for the verification commands.
* 39 intermediate dill `checkpoint_seed44_gen*.pkl` files (~95 MB total) remained on the remote
  inside `logs/steps/009_implementation/checkpoints/`. They are not in the expected-file list and
  the final `nsga2_checkpoint_seed44.json` already captures gen-39 state, so they were left to be
  destroyed with the instance rather than pulled.
* Final billed wall-clock cost ($10.37) is $0.48 above the NSGA-II driver's self-reported $9.89
  (covering only the productive 24.1 h between gen 1 start and gen 39 finish). The extra $0.48
  reflects ~11 min of provisioning + environment setup before NSGA-II launch and ~63 min of idle
  time between the operator-stop completion at 01:18:30Z and the destroy call at 01:26:15Z.
