---
spec_version: "3"
task_id: "t0047_validate_pp16_fig3_cond_noise"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-24T22:15:57Z"
completed_at: "2026-04-24T22:27:00Z"
---
## Summary

Reviewed t0046 library code, MOD source files, and t0011/t0012 helper libraries to answer eight
specific code-research questions for the Fig 3A-F per-synapse conductance recording task. No hard
blockers found. Critical finding: `bipolarNMDA.mod` exposes both `gAMPA` and `gNMDA` as separate
RANGE variables on a single dual-component synapse — there is no separate `bipampa` synapse class.
The `_ref_gAMPA` and `_ref_gNMDA` pointers can be attached for per-component recording. SACinhib
reversal is `-60 mV` per `main.hoc` override (not the MOD default `-65 mV`).

## Actions Taken

1. Inspected
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/sources/`
   for the three MOD files (`bipolarNMDA.mod`, `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`). Confirmed
   RANGE declarations and reversal-potential PARAMETER values.
2. Read t0046's `code/build_cell.py`, `code/run_simplerun.py`, `code/constants.py`, and
   `code/compute_metrics.py` to identify reusable patterns and the synapse-list iteration idiom.
3. Reviewed t0011's `tuning_curve_viz` and t0012's `tuning_curve_loss` libraries for API fit; both
   constrained to 12-angle tuning curves and not directly reusable for Fig 3 panels (raw matplotlib
   needed instead). Noted that `compute_dsi` should be inlined from t0046's 8-line helper rather
   than imported.
4. Wrote `tasks/t0047_validate_pp16_fig3_cond_noise/research/research_code.md` covering the eight
   questions, the recording dt recommendation (0.25 ms), and the no-blocker verdict.
5. Ran `verify_research_code.py` — PASSED with 0 errors and 0 warnings.

## Outputs

* tasks/t0047_validate_pp16_fig3_cond_noise/research/research_code.md

## Issues

No issues encountered. All code-research questions answered with concrete file/line references. The
implementation step has a clear path to attach `Vector.record(syn._ref_gAMPA, dt)`,
`Vector.record(syn._ref_gNMDA, dt)`, and `Vector.record(syn._ref_g, dt)` for the bipNMDA, SACexc,
and SACinhib synapse arrays respectively.
