---
spec_version: "3"
task_id: "t0121_5seed_substrate_rate_canonical_report"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-24T01:23:10Z"
completed_at: "2026-05-24T01:36:00Z"
---
# Step 6: Research Code

## Summary

Spawned a `/research-code` subagent that reviewed the 5 source tasks (t0106, t0112, t0113, t0114,
t0115) and wrote `research/research_code.md` (529 lines). Key findings: (a) result data layout is
uniform across all 5 source tasks; (b) t0115 already has a `substrate_rate_5seed.csv` with the
canonical numbers; (c) joint_pass_pct convention drift between LEGIT and raw counts is the
load-bearing harmonisation deliverable; (d) Hay/Druckmann/Mohacsi citations are already pinned by
t0114 / t0115 compare_literature.md.

## Actions Taken

1. Spawned a subagent to execute the `/research-code` skill against task t0121.
2. The subagent enumerated 10 cited tasks (the 5 5-seed sources + t0117 parquet pattern + t0119
   commissioning brainstorm + t0078 / t0097 / t0102 paper-asset hosts).
3. The subagent identified ~500-600 lines of reusable code from t0115's `build_results.py` plus
   suffix-branching loader from t0117.
4. The subagent ran `verify_research_code` -- PASSED with 0 errors / 0 warnings.

## Outputs

* `tasks/t0121_5seed_substrate_rate_canonical_report/research/research_code.md` (529 lines)
* `tasks/t0121_5seed_substrate_rate_canonical_report/logs/steps/006_research-code/step_log.md`

## Key Findings (carried into planning)

1. Adopt t0115's LEGIT-only joint_pass_pct convention; surface a convention-drift table to reconcile
   against t0113/t0114 published numbers.
2. Recompute the canonical 5-seed table with bootstrap-CI (B=10000) in addition to the normal-approx
   CI already in t0115.
3. Document HV-plateau auto-stop and pool-restart cadence drift between t0106 / t0112-t0113 /
   t0114-t0115.
4. Leverage existing Hay 2011 / Druckmann 2007 / Mohacsi 2024 paper assets (DOIs already resolved
   via t0078 / t0097 / t0102).

## Issues

No issues encountered.
