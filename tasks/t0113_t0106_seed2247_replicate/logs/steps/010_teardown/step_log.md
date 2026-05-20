---
spec_version: "3"
task_id: "t0113_t0106_seed2247_replicate"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-20T02:09:40Z"
completed_at: "2026-05-20T02:12:46Z"
---
# Step 10: Teardown

## Summary

Destroyed Vast.ai instance 37107202 via `vastai destroy instance` after confirming all results,
predictions assets, hv_trace.jsonl, 14 dill checkpoints, and smoke gate reports were already present
in the worktree. Updated `machine_log.json` with destruction timestamp, duration and cost. Wrote
`results/remote_machines_used.json` (single-entry list with failed attempts captured) and
`results/costs.json` ($0.4773 total: $0.1467 productive driver run + $0.2856 setup/idle + $0.045
wasted SSH-key-failure attempt). `verify_machines_destroyed.py` PASSED with one expected RM-W001
warning (API unreachable because instance is destroyed — same as t0112).

## Actions Taken

1. Verified local data:
   `assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz`
   present; `results/data/` contains 7 JSON files (algorithm_config, all_evaluations,
   evaluation_seeds, hv_trajectory, init_pop, nsga2_checkpoint, pareto_front);
   `logs/steps/009_implementation/` has driver.log, hv_trace.jsonl, smoke_gate.json,
   smoke_gate_report_remote.json, and 14 dill checkpoints (gen0001 through gen0014). All needed
   artifacts confirmed local — no further SCP needed.
2. Pre-destruction status check: `vastai show instance 37107202 --raw` confirmed running, duration
   6309.85 s elapsed.
3. Destroyed instance: `echo y | vastai destroy instance 37107202` returned "destroying instance
   37107202." at 2026-05-20T02:11:25Z.
4. Confirmed destruction: `vastai show instances --raw` no longer lists 37107202.
5. Updated `logs/steps/008_setup-machines/machine_log.json` with `destroyed_at`
   (2026-05-20T02:11:25Z), `total_duration_hours` (1.7589), and `total_cost_usd` (0.4323 = 1.7589 h
   x $0.2458/hr).
6. Wrote `results/remote_machines_used.json` as a single-entry list with the required spec fields
   (provider, machine_id, gpu, gpu_count, ram_gb, duration_hours, cost_usd) plus extended fields
   (instance_id, cpu_name, cpu_cores, dph_total, created_at, destroyed_at, total_duration_hours,
   total_cost_usd, failed_attempts) mirroring the t0112 schema and capturing both failed-attempt
   records from `machine_log.json`.
7. Wrote `results/costs.json` with `total_cost_usd: 0.4773` and a 3-line breakdown using rich
   `cost_usd + description` objects: productive run $0.1467, setup/idle $0.2856 (computed as billed
   total minus productive), and wasted SSH-key-failure attempt $0.045. Added `services`
   (`vast-ai: 0.4773`), `budget_limit` (25.0), and a `note` documenting the comparison with t0112.
8. Ran `verify_machines_destroyed.py t0113_t0106_seed2247_replicate` — PASSED (0 errors, 1 expected
   RM-W001 warning that the API cannot confirm destruction because the instance is gone).

## Outputs

* `tasks/t0113_t0106_seed2247_replicate/logs/steps/008_setup-machines/machine_log.json` (updated)
* `tasks/t0113_t0106_seed2247_replicate/results/remote_machines_used.json`
* `tasks/t0113_t0106_seed2247_replicate/results/costs.json`
* `tasks/t0113_t0106_seed2247_replicate/logs/steps/010_teardown/step_log.md`

## Final Cost Summary

* Instance lifecycle: created 2026-05-20T00:25:53Z, destroyed 2026-05-20T02:11:25Z
* Duration billed: 1.7589 h
* Hourly rate: $0.2458/hr (incl 40 GB storage)
* Instance total: $0.4323
* Additional wasted SSH-key-failure spend (earlier instance 37106453): $0.045
* Task total: **$0.4773** (well under $25 task cap)

## Verification

* `verify_machines_destroyed.py t0113_t0106_seed2247_replicate`: PASSED (0 errors, 1 RM-W001 warning
  — API unreachable for destroyed instance, expected and matches t0112)

## Issues

No issues encountered. The `vastai destroy instance` API returned cleanly on first attempt;
`verify_machines_destroyed.py` passed with only the expected RM-W001 warning (the API cannot confirm
destruction state because the instance no longer exists, which is exactly the success condition).
One minor note: the verificator script takes the task_id as a positional argument, not a `--task-id`
flag — used the positional form.
