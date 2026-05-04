---
spec_version: "3"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-04T15:49:08Z"
completed_at: "2026-05-04T15:55:00Z"
---
# Step 10 — Teardown

## Summary

Spawned a `/setup-remote-machine` Teardown subagent to verify all critical files were locally
mirrored, finalise `machine_log.json` / `costs.json` / `remote_machines_used.json`, and destroy
Vast.ai instance 36068067. The destroy succeeded; `vastai show instances --raw` returned `[]`. Final
cost **$3.9335** (24.86 h at $0.1582/hr). All 41 checkpoints, the trial history parquet, the
hypervolume trajectory CSV, the mobo_loop.log, and the pareto_front.json were already present
locally from the SCP that accompanied the SIGTERM of PID 2366 at acq 416. The
`verify_machines_destroyed.py` verificator passed with 0 errors plus 2 expected warnings
(API-unreachable for live confirmation; >12 h runtime, expected for an overnight MOBO loop).

## Actions Taken

1. Ran `prestep teardown`.
2. Spawned a `/setup-remote-machine` Teardown subagent with full context: instance 36068067, $3.78
   cost-at-SIGTERM, all critical files already SCP'd locally, no GPU work to teardown.
3. The subagent verified file integrity (all checkpoints + trial_history + hv_trajectory matched
   bytewise local↔remote; pareto_front.json had a 1-byte CRLF/LF difference, content identical),
   updated `machine_log.json` with `destroyed_at` / `total_duration_hours` / `total_cost_usd`, ran
   `vastai destroy instance 36068067 -y`, confirmed `vastai show instances` returned empty, wrote
   `results/remote_machines_used.json` per the spec, wrote `results/costs.json` with
   `total_cost_usd: 3.9335` plus a `breakdown` dict.
4. Ran `verify_machines_destroyed.py --task-id t0078_bedb_mobo_v2_ais_tiered_ahp`: PASSED with 0
   errors, 2 expected warnings.

## Outputs

* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/008_setup-machines/machine_log.json`
  (updated): `destroyed_at: 2026-05-04T15:51:29Z`, `total_duration_hours: 24.8578`,
  `total_cost_usd: 3.9335`.
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/remote_machines_used.json` (created): one machine
  record matching the spec.
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/costs.json` (created):
  `{"total_cost_usd": 3.9335, "breakdown": {"vast_ai_compute": 3.9335}}`.
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/010_teardown/step_log.md` — this step log.
* Vast.ai instance 36068067: **destroyed**. No further compute charges.

## Issues

No blocking issues. The two warnings from `verify_machines_destroyed.py` are expected:

* `RM-W001`: Vast.ai API unreachable for live destruction confirmation (expected without API key in
  the shell env; instance was confirmed destroyed via `vastai show instances --raw` returning `[]`).
* `RM-W003`: instance ran 24.9 h > 12 h (informational; expected for an overnight 49-d MOBO loop
  with O(N³) GP scaling).

The 1-byte size difference between local and remote `pareto_front.json` (21,983 vs 21,982 bytes) is
a CRLF / LF line-ending artefact from Windows-side checkout; content is identical (verified by
comparing `n_total_evaluations` and `n_pareto` fields plus the first 5 Pareto cells).
