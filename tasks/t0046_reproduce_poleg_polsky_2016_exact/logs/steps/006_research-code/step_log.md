---
spec_version: "3"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-24T13:51:06Z"
completed_at: "2026-04-24T14:05:00Z"
---
## Summary

Produced `research/research_code.md` via the `/research-code` skill subagent. File-by-file catalogue
of the ModelDB 189347 release: `main.hoc` (396 L), `RGCmodel.hoc` (11861 L), `HHst.mod`,
`bipolarNMDA.mod`, `SAC2RGCinhib.mod`, `SAC2RGCexc.mod`, `SquareInput.mod`, `spike.mod`, plus
bootstrap files. Identified 4 relevant libraries (t0008, t0020, t0011, t0012) and 9 cited tasks.
Verificator passed with zero errors and zero warnings.

The research-code step surfaced five additional findings that correct or extend the earlier research
stages and are critical for the implementation plan.

## Actions Taken

1. Spawned a `/research-code` subagent scoped to the ModelDB 189347 release and the t0008/ t0020
   library assets.
2. Subagent read every `.hoc`, `.mod`, `.py`, and bootstrap file in the ModelDB release and built a
   file-by-file catalogue with line counts.
3. Subagent extracted actual runtime parameter values from `main.hoc` overrides (not from MOD
   defaults) and cross-checked against the values in `research/research_internet.md`.
4. Ran `verify_research_code.py` wrapped in `run_with_logs.py`; passed with zero errors and zero
   warnings.

## Key Corrections / New Findings (for Planning)

1. **Luminance-noise driver IS PRESENT**, contradicting the earlier research-internet pre-flag.
   `main.hoc` defines `flickertime=50, flickerVAR=0, stimnoiseVAR=0`, and `placeBIP()` in
   `RGCmodel.hoc` implements per-50-ms Gaussian perturbation. The noise driver is present but
   zeroed; Figures 6-8 reproduction only needs to override those two globals. No new MOD file
   required. Task-description pre-flag should be revised.
2. **Parameter-extraction errors in research_internet.md's audit table**: MOD defaults were read
   instead of `main.hoc` overrides. Corrected values: `n_bipNMDA=0.3` (not 0.25),
   `gama_bipNMDA=0.07` (not 0.08), `newves_bipNMDA=0.002` (not 0.01), `tau1NMDA=60 ms` (not 50),
   `tau_SACinhib=30 ms` (not 10), `e_SACinhib=-60 mV` (not -65).
3. **Morphology is HOC-embedded**, no SWC ships. `RGCmodel.hoc` contains ~11500 `pt3dadd` calls.
   t0005's SWC is a SUBSTITUTE (a different cell). Previous ports using t0005 morphology were not
   faithful reproductions — this is itself a discrepancy that must be flagged in the audit.
4. **`simplerun()` rebinds `achMOD` to 0.33** (not the 0.25 default) during active trials. The
   paper-faithful value is 0.33.
5. **Prior-port cross-task-import violations**: t0020 imports from t0008's code; t0020's registered
   library has empty `code/`. t0046 must follow t0022's copy-with-renamed-sentinel pattern.

## Outputs

* tasks/t0046_reproduce_poleg_polsky_2016_exact/research/research_code.md
* tasks/t0046_reproduce_poleg_polsky_2016_exact/logs/steps/006_research-code/step_log.md

## Issues

No blocking issues. Several corrections to the earlier research stages are captured above and in
research_code.md; planning will synthesise them before implementation starts.
