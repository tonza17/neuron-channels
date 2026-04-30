---
spec_version: "3"
task_id: "t0067_t0065_soma_channel_addition_sweep"
step_number: 8
step_name: "suggestions"
status: "completed"
started_at: "2026-05-01T00:55:30Z"
completed_at: "2026-05-01T01:00:00Z"
---
## Summary

Authored 5 follow-up suggestions (S-0067-01 through S-0067-05) based on the t0067 sweep findings.
Two highest-priority items (high) directly follow from the headline NaP/Nav1.6 results: refine the
NaP DSI-inversion threshold density (S-0067-01), and test Nav1.6+Kv3 co-expression to see if Kv3
rescues the DSI loss (S-0067-02).

## Actions Taken

1. Reviewed `results/results_detailed.md` Analysis & Discussion sections to extract follow-up
   directions.
2. Wrote `results/suggestions.json` with 5 entries (2 high, 2 medium, 1 low priority):
   * S-0067-01 (high experiment): finer NaP density grid to find DSI=0 crossing.
   * S-0067-02 (high experiment): Nav1.6 + Kv3 co-insertion DSI rescue test.
   * S-0067-03 (medium experiment): add virtual AIS to deposited cell, re-run sweep.
   * S-0067-04 (medium experiment): vendor canonical ModelDB MOD files for NaR/Kv3/Kv4.
   * S-0067-05 (low evaluation): literature survey of NaP dysregulation in retinal disease.
3. Verified with `verify_suggestions.py` — PASSED 0/0.

## Outputs

* `tasks/t0067_t0065_soma_channel_addition_sweep/results/suggestions.json`
* `tasks/t0067_t0065_soma_channel_addition_sweep/logs/steps/008_suggestions/step_log.md`

## Issues

No issues encountered.
