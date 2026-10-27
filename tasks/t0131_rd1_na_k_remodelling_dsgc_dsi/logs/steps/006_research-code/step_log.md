---
spec_version: "3"
task_id: "t0131_rd1_na_k_remodelling_dsgc_dsi"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-10-27T10:20:29Z"
completed_at: "2026-10-27T10:29:02Z"
---
# Step 6: Research Code

## Summary

Identified the reusable model, evaluator and reference-cell sources. Reference 68-d vectors live in
the t0106/t0112/t0114/t0115 evaluation files, not the t0121 parquet, and a 1400 ms local trial takes
about 9 s.

## Actions Taken

1. Spawned a research-code subagent over libraries and prior task code
2. Wrote research/research_code.md with copy-versus-import guidance
3. Ran verify_research_code (passed)

## Outputs

* tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/research/research_code.md

## Issues

aggregate_libraries, aggregate_answers and aggregate_papers do not exist in this repo, so libraries
were enumerated from tracked asset folders. Three items were not confirmed: meaning of the +100 mV
step, trial speed without recorders, and local MOD recompilation.
