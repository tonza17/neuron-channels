---
spec_version: "3"
task_id: "t0102_seedscale_n4_gen20"
step_number: 10
step_name: "teardown"
status: "completed"
started_at: "2026-05-12T17:54:54Z"
completed_at: "2026-05-12T17:59:30Z"
---
# Step 10: teardown

## Summary

Destroyed Vast.ai instance 36556586 after confirming all NSGA-II results from both GA seeds had been
previously SCP'd back during the implementation step (commit 29dad484). Instance ran for 24.842
hours from start_date 2026-05-11T17:06:50Z to destroyed_at 2026-05-12T17:57:21Z at billing rate
$0.4852/hr, yielding a final total cost of $12.0733 (slightly above the $11.94 previously recorded
in costs.json due to ~39 min of additional uptime between the seed 55 watchdog trip at 17:18:40Z and
teardown at 17:57:21Z). Two previously-uncopied intervention marker files
(`budget_overrun_seed44.md`, `budget_overrun_seed55.md`) recording the per-seed cost watchdog trip
events were SCP'd back before destruction. The `verify_machines_destroyed` verificator passed with 0
errors and 2 expected warnings (RM-W001 API unreachable for the destroyed instance, RM-W003 ran
> 12h).

## Actions Taken

1. Read setup-remote-machine SKILL.md Teardown Protocol section and machine_log.json /
   remote_machines_used.json / costs.json to confirm prior state.
2. Ran `vastai show instance 36556586 --raw` to capture pre-destruction state (uptime 1487.98 min /
   24.80 h, actual_status="running", dph_total=$0.4852/hr).
3. SSH'd to ssh4.vast.ai:36586 and ran `find /root -name '*seed44*' -o -name '*seed55*'` --
   confirmed all 10 results/data/*.json files matched the local repo, and
   `find /root -newer /root/t0102_workdir/run_two_seeds.log` returned nothing important to copy
   back.
4. Discovered 2 watchdog-generated intervention marker files on the remote
   (`intervention/budget_overrun_seed{44,55}.md`) that had not been SCP'd back in commit 29dad484.
   SCP'd both back to `tasks/t0102_seedscale_n4_gen20/intervention/`.
5. Ran `vastai destroy instance 36556586 -y` -- response "destroying instance 36556586." Destruction
   timestamp: 2026-05-12T17:57:21Z.
6. Confirmed destruction by running `vastai show instance 36556586 --raw` after destroy -- returned
   a NoneType error from the CLI indicating the instance row is gone (RM-W001 in the verificator is
   the expected API-unreachable warning).
7. Updated `logs/steps/008_setup-machines/machine_log.json` fields
   `destroyed_at`="2026-05-12T17:57:21Z", `total_duration_hours`=24.842, and
   `total_cost_usd`=12.0733.
8. Updated `results/remote_machines_used.json` with `duration_hours`=24.842 and `cost_usd`=12.0733
   (was 24.61 / $11.94).
9. Updated `results/costs.json` total_cost_usd to $12.0733; the additional $0.13 vs the prior $11.94
   was attributed to the `vast_ai_idle_time` bucket (now $3.5065 vs $3.3732), reflecting the ~39 min
   of uptime between the seed 55 watchdog trip and teardown.
10. Ran the `verify_machines_destroyed` verificator -- PASSED with 0 errors and 2 expected warnings
    (RM-W001 API unreachable, RM-W003 duration >12h, both informational for a properly destroyed
    long-running instance).

## Outputs

* `logs/steps/008_setup-machines/machine_log.json` -- `destroyed_at`, `total_duration_hours`,
  `total_cost_usd` populated.
* `results/remote_machines_used.json` -- final duration/cost recorded ($12.0733 / 24.842 h).
* `results/costs.json` -- total_cost_usd updated to $12.0733 with idle-time bucket adjusted.
* `intervention/budget_overrun_seed44.md`, `intervention/budget_overrun_seed55.md` -- watchdog trip
  markers preserved from the remote machine for traceability.
* Vast.ai instance 36556586 -- destroyed and confirmed.

## Issues

* Final cost $12.0733 exceeds the $8 plan-stated hard cap by $4.07. Cost overrun was previously
  documented in costs.json and was user-authorised in advance. The cost watchdog itself behaved as
  designed (tripped at $4 for both seeds); the overrun came from ~7 hours of idle compute when the
  initial implementation subagent went silent before launching, plus the watchdog's grace period to
  finish the in-progress generation, plus ~39 min of post-watchdog uptime up to teardown. No further
  action required -- this is a known overrun documented across costs.json and the implementation
  step log.
* The 2 intervention/budget_overrun_seed*.md files were not copied back in the implementation step's
  commit 29dad484 SCP batch. They were caught and SCP'd back during the teardown pre-destroy file
  audit. No data lost.
