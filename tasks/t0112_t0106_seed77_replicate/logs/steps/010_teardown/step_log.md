---
spec_version: "3"
task_id: "t0112_t0106_seed77_replicate"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-19T21:24:54Z"
completed_at: "2026-05-19T21:30:00Z"
---
# Step 10: Teardown

## Summary

Destroyed Vast.ai instance 37076157 via `vastai destroy instance`, updated `machine_log.json` with
the destroyed_at timestamp and final duration / cost, wrote `results/remote_machines_used.json` and
`results/costs.json` with the productive-compute breakdown. Final instance spend: $1.99 over 5.82 h
(well under the $20 per-instance watchdog and $25 task cap). `verify_machines_destroyed.py` passes.

## Actions Taken

1. Final cost check via `vastai show instance 37076157 --raw` — elapsed 5.82 h × $0.3426/h = $1.99
   estimated.
2. Destroyed the instance with `echo y | vastai destroy instance 37076157`.
3. Confirmed destruction via follow-up `vastai show instance` — API now returns null start_date
   (expected post-destruction state).
4. Updated `logs/steps/008_setup-machines/machine_log.json` with `destroyed_at`,
   `total_duration_hours`, and `total_cost_usd`.
5. Wrote `results/remote_machines_used.json` (single-entry list mirroring t0106's format).
6. Wrote `results/costs.json` with `total_cost_usd: 1.9934` and a single breakdown line
   `vast-ai-epyc-7b13: 1.9934`.
7. Ran `verify_machines_destroyed.py` — PASSED (2 expected warnings: RM-W001 API unreachable because
   instance is destroyed, RM-W006 no checkpoint_path which is non-blocking).

## Outputs

* `tasks/t0112_t0106_seed77_replicate/logs/steps/008_setup-machines/machine_log.json` (updated)
* `tasks/t0112_t0106_seed77_replicate/results/remote_machines_used.json`
* `tasks/t0112_t0106_seed77_replicate/results/costs.json`
* `tasks/t0112_t0106_seed77_replicate/logs/steps/010_teardown/step_log.md`

## Issues

No issues encountered.
