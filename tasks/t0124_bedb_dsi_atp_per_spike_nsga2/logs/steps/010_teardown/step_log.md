---
spec_version: "3"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-25T02:15:07Z"
completed_at: "2026-05-25T02:18:39Z"
---
# Step 10: teardown

## Summary

Destroyed Vast.ai instance 37679733. Verified no active tmux sessions and all 7 remote results files
byte-matched local copies before destroying. Final cost $0.2935 (4.9% of $6 task cap, well under
expected $1-3 band). Updated machine_log.json with destroyed_at + total_duration_hours; wrote
remote_machines_used.json (v2 list-form) and costs.json (single service breakdown).
verify_machines_destroyed.py PASSED with 0 errors (1 expected warning RM-W001: API returns 404 on
destroyed instance — the canonical post-destruction signal).

## Actions Taken

1. Spawned /setup-remote-machine teardown protocol subagent.
2. Verified remote-vs-local checksum on all 7 result data files.
3. Destroyed instance 37679733 via `vastai destroy instance 37679733 -y --raw`; confirmed 404 on
   follow-up show-instance.
4. Updated machine_log.json: destroyed_at=2026-05-25T02:18:39Z, total_duration_hours=1.8178,
   total_cost_usd=0.2935.
5. Wrote results/remote_machines_used.json with full v2 schema.
6. Wrote results/costs.json: total_cost_usd=0.2935, service breakdown (vast-ai-epyc-7b13-t0124:
   $0.2935), budget_limit=$6.0.
7. Ran verify_machines_destroyed.py via run_with_logs.py: 0 errors, 1 expected RM-W001 warning.

## Outputs

* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/logs/steps/008_setup-machines/machine_log.json (updated)
* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/remote_machines_used.json
* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/costs.json
* tasks/t0124_bedb_dsi_atp_per_spike_nsga2/logs/steps/010_teardown/step_log.md (this file)

## Issues

No issues encountered. The meter is stopped; no leaked compute. Total run cost $0.29 (5% of budget
cap). The RM-W001 warning is expected (Vast.ai API returns 404 on a destroyed instance).
