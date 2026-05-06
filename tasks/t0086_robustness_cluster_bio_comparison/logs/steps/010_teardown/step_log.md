---
spec_version: "3"
task_id: "t0086_robustness_cluster_bio_comparison"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-06T18:11:29Z"
completed_at: "2026-05-06T18:11:50Z"
---
# Step 10 -- Teardown

## Summary

Destroyed Vast.ai instance 36240604 immediately after Phase A/B/C completion. Final billable
duration was **4.5911 hours** (created_at 2026-05-06T13:36:14Z to destroyed_at
2026-05-06T18:11:42Z) at the resolved rate of **$0.3474/hr**, yielding **$1.595 total cost**, well
under the $3.50 hard cap. The cost watchdog (REQ-X) reported $1.3335 at Phase A completion; the
additional $0.26 reflects the ~12 minutes between Phase A completion and the teardown destroy
command (Vast.ai bills until destroyed_at). REQ-X cost-watchdog rate-fix verified end-to-end:
costs.json `breakdown.vast-ai-cpu-epyc-7b13.actual_rate_usd_per_hour` is 0.3474 (matching
machine_log.json `selected_offer.price_per_hour`); no hard-coded $0.2382/hr surfaced anywhere in
the cost accounting path.

## Actions Taken

1. Pulled `replication_results.json` (100 records) from
   `root@ssh4.vast.ai:/root/neuron-channels/tasks/t0086_robustness_cluster_bio_comparison/results/data/replication_results.json`
   to local worktree via `scp` before destroying the instance.
2. Ran `vastai destroy instance 36240604`. Instance reached destroyed status immediately.
3. Updated `logs/steps/008_setup-machines/machine_log.json`:
   * `destroyed_at`: 2026-05-06T18:11:42Z
   * `total_duration_hours`: 4.5911
   * `total_cost_usd`: 1.595
4. Wrote `results/costs.json` with `total_cost_usd=1.595`, breakdown, and a `note` documenting
   REQ-X verification.
5. Wrote `results/remote_machines_used.json` summarising the single Vast.ai instance.
6. Verified no other Vast.ai instances are running (`vastai show instances`).

## Outputs

* Updated `logs/steps/008_setup-machines/machine_log.json` with destroy timestamps + costs.
* `results/costs.json` (REQ-14, REQ-X documentation).
* `results/remote_machines_used.json`.

## Issues

* No issues. Teardown was clean.
