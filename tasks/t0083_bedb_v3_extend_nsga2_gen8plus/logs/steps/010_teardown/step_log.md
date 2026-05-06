---
spec_version: "3"
task_id: "t0083_bedb_v3_extend_nsga2_gen8plus"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-06T08:10:12Z"
completed_at: "2026-05-06T08:14:00Z"
---
# Step 10 -- Teardown

## Summary

Destroyed Vast.ai instance 36186200 (AMD EPYC 7B13 64-Core, offer 24887414) after the NSGA-II
warm-start continuation completed. Confirmed the instance was still in `actual_status: running` at
teardown time, then issued `vastai destroy instance 36186200` through the run_with_logs wrapper.
Final billed lifetime was 18.1614 hours (from `created_at` 2026-05-05T14:01:22Z to `destroyed_at`
2026-05-06T08:11:02Z) at $0.3209/hr, totalling $5.828. Updated `machine_log.json` with the final
timestamps and cost; wrote `results/remote_machines_used.json` and `results/costs.json`. The $5.828
actual charge slightly exceeded the $5.00 in-loop watchdog cap because the watchdog inherited the
t0080/t0081 hard-coded $0.2382/hr rate (so it tracked $4.1149 reported), while the real instance
billed at $0.3209/hr; root-cause and corrected cell-cost accounting are documented in `costs.json`
`note`. `verify_machines_destroyed.py` PASSED with 3 informational warnings (API unreachable for
cross-check, runtime > 12 h, no checkpoint_path) -- none of which block progress.

## Actions Taken

1. Ran `vastai show instances --raw` through `run_with_logs` to confirm instance 36186200 was
   `actual_status: running` immediately before destruction; recorded current dph_total of $0.3246/hr
   (matches the offer's $0.3209/hr base + small reliability premium).
2. Ran `vastai destroy instance 36186200` through `run_with_logs` (with `echo y` to confirm the
   prompt). Vast.ai responded `destroying instance 36186200`.
3. Computed final lifetime as the delta between `created_at` (2026-05-05T14:01:22Z) and the teardown
   timestamp (2026-05-06T08:11:02Z): 18.1614 hours; cost at the documented offer rate $0.3209/hr is
   $5.828.
4. Edited `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/logs/steps/008_setup-machines/machine_log.json`
   to fill in `destroyed_at`, `total_duration_hours`, and `total_cost_usd`.
5. Wrote `results/remote_machines_used.json` (one entry: provider vast.ai, machine_id 36186200, gpu
   RTX 4060 Ti idle/unused, gpu_count 0, ram_gb 332, duration_hours 18.1614, cost_usd 5.828).
6. Wrote `results/costs.json` (total_cost_usd 5.828, single breakdown entry vast-ai-cpu-epyc-7b13
   with description, services map vast_ai => 5.828, budget_limit 5.0, note documenting the watchdog
   rate-mismatch and corrected cell-cost accounting).
7. Ran `verify_machines_destroyed.py t0083_bedb_v3_extend_nsga2_gen8plus` -- PASSED with 3
   informational warnings (RM-W001 API unreachable, RM-W003 runtime > 12h, RM-W006 no
   checkpoint_path). None block progress.

## Outputs

* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/logs/steps/008_setup-machines/machine_log.json` --
  updated with destroyed_at, total_duration_hours, total_cost_usd.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/remote_machines_used.json` -- one-machine array
  with full lifetime accounting.
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/costs.json` -- $5.828 total with breakdown,
  services map, budget cap and overrun note.

## Issues

* In-loop budget watchdog used `_HARD_BUDGET_USD` from `arf/libraries/t0080_loop` with the t0081
  hourly rate ($0.2382/hr) hard-coded, while the actual t0083 offer billed at $0.3209/hr. The
  watchdog therefore reported $4.1149 spent at gen-17 termination vs the true Vast.ai charge of
  ~$5.55 at run-end and $5.828 at instance-destroy. The discrepancy is documented in
  `results/costs.json` `note`. A follow-up suggestion has been queued for step 14 to parameterise
  the hourly rate in the budget watchdog.
* `verify_machines_destroyed.py` could not reach the Vast.ai API at verification time (RM-W001), so
  destruction is asserted by the local `destroyed_at` field plus the successful `vastai destroy`
  command response. The instance no longer accepted SSH connections after destruction.
