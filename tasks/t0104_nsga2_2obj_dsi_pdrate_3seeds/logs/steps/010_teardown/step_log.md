---
spec_version: "3"
task_id: "t0104_nsga2_2obj_dsi_pdrate_3seeds"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-14T03:00:55Z"
completed_at: "2026-05-14T03:02:00Z"
---
## Summary

Tore down Vast.ai instance 36645796 immediately after seed 55 completed and data was pulled back.
Total instance lifetime 28.66 hours, total cost $10.30 (productive $8.88 across two seeds plus $1.42
setup / smoke-gate / inter-seed transitions / final-pull idle). Updated machine_log.json with
destruction fields, wrote results/remote_machines_used.json and results/costs.json.
verify_machines_destroyed PASSED with 3 expected warnings (RM-W001 API unreachable post-destroy
because the instance no longer exists in the Vast.ai API; RM-W003 long runtime; RM-W006 no
checkpoint path — t0104's nsga2_checkpoint files live under results/data/, not under machine_log).

## Actions Taken

1. After seed 55's tmux session exited (NSGA-II watchdog tripped after gen 11), checked instance was
   idle (CPU 0%, no tmux sessions running) and pulled all 13 result data files back via scp to
   `tasks/t0104_*/results/data/`.
2. Issued `vastai destroy instance 36645796` to terminate the rental and stop billing.
3. Verified destruction by re-querying `vastai show instance 36645796` (now errors with NoneType on
   start_date — confirms the instance is gone).
4. Updated `logs/steps/008_setup-machines/machine_log.json` with `destroyed_at`,
   `total_duration_hours`, `total_cost_usd`.
5. Wrote `results/remote_machines_used.json` (per task_results_specification fields: provider,
   machine_id, gpu, gpu_count, ram_gb, duration_hours, cost_usd) — `machine_id` and `cost_usd`
   match `machine_log.json` `instance_id` and `total_cost_usd`.
6. Wrote `results/costs.json` with breakdown summing to $10.30.
7. Ran `verify_machines_destroyed t0104_nsga2_2obj_dsi_pdrate_3seeds` — PASSED with 3 expected
   warnings.

## Outputs

* `logs/steps/008_setup-machines/machine_log.json` — destruction fields populated
* `results/remote_machines_used.json` — per-spec record for the one Vast.ai instance
* `results/costs.json` — `$10.30` total with productive vs idle breakdown
* `logs/commands/` — wrapped `vastai destroy` and `verify_machines_destroyed` logs

## Issues

`verify_machines_destroyed` emitted 3 warnings:

* `RM-W001` — Cannot verify destruction via API. Expected: the instance no longer exists in the
  Vast.ai API once destroyed, so the verificator cannot fetch its state. Manual verification via
  `vastai show instance` confirmed the instance is gone.
* `RM-W003` — Machine ran 28.7 h (>12 h). Expected: this task is a long NSGA-II run; the planning
  step accounts for it (Time Estimation: 32-40 h).
* `RM-W006` — Machine ran 28.7 h but no `checkpoint_path` is set. Expected: t0104's NSGA-II
  per-seed checkpoints live at `results/data/nsga2_checkpoint_seed{44,55}.json` rather than under
  the machine_log's optional `checkpoint_path` field. Both checkpoint files exist and were pulled
  back successfully.

All three warnings are non-blocking and accurately characterise expected behaviour.
