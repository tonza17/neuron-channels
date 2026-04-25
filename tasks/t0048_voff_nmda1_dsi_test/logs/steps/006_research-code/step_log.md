---
spec_version: "3"
task_id: "t0048_voff_nmda1_dsi_test"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-25T08:25:14Z"
completed_at: "2026-04-25T08:32:00Z"
---
## Summary

Reviewed t0046's `simplerun()` proc, `run_one_trial` API, t0047's conductance recorder, and the
bipolarNMDA.mod `Voff` semantics. Confirmed that exptype=2 differs from exptype=1 ONLY in
`Voff_bipNMDA` (no other parameters touched), making the comparison clean. Identified one critical
blocker: t0047 is NOT a registered library asset, so the project's cross-task import rule requires
copying t0047's `run_with_conductances.py` into t0048's `code/` directory rather than importing it.
Direct import from t0046 IS allowed (t0046's code subtree is the implementation of the registered
`modeldb_189347_dsgc_exact` library asset).

## Actions Taken

1. Read t0046's `main.hoc` (lines 332-360 for the simplerun proc), `run_simplerun.py` API,
   `bipolarNMDA.mod` Voff semantics (line 108: `local_v = v*(1-Voff) + Vset*Voff`).
2. Read t0047's `run_with_conductances.py` API, `dsi.py` helper, and per-trial CSV schema.
3. Confirmed exptype=2 modifies only `Voff_bipNMDA = 1`; all other globals (`b2gampa`, `b2gnmda`,
   `s2ggaba`, `s2gach`, `gabaMOD`, `achMOD`) are set to identical values as exptype=1. The t0048 vs
   t0047 comparison isolates voltage-dependence.
4. Wrote `research/research_code.md` covering all 7 questions; ran `verify_research_code.py` —
   PASSED with 0 errors and 0 warnings.

## Outputs

* tasks/t0048_voff_nmda1_dsi_test/research/research_code.md

## Issues

The cross-task import blocker (t0047 is not a registered library) requires copying
`run_with_conductances.py` and `dsi.py` from t0047 into t0048's `code/` directory with attribution
comments. The implementation step must follow this approach instead of attempting a direct import.
