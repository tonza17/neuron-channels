---
spec_version: "3"
task_id: "t0049_seclamp_cond_remeasure"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-25T09:39:15Z"
completed_at: "2026-04-25T09:48:00Z"
---
## Summary

Reviewed t0046's `run_one_trial` API, the NEURON SEClamp insertion pattern, the channel isolation
override pattern (writable Python globals after `simplerun()`), and the `bipolarNMDA.mod` AMPA/NMDA
independence. Confirmed: SEClamp inserts cleanly at `h.RGC.soma(0.5)` with
`dur1=h.tstop, amp1=-65, rs=0.001`; channel isolation via `h.b2gampa = 0` / `h.b2gnmda = 0` /
`h.gabaMOD = 0` zeroes each component independently; reversal potentials are 0 / 0 / -60 mV (NMDA /
AMPA / SACinhib). No hard blockers.

## Actions Taken

1. Read t0046's `run_simplerun.py` (the `run_one_trial` API and the AP5-override branch pattern at
   lines 135-151), `bipolarNMDA.mod` (AMPA/NMDA component independence), `RGCmodel.hoc` (DSGC
   template, `public soma` access), and `dsgc_model_exact.hoc` (the `b2gampa` / `b2gnmda` /
   `gabaMOD` write-accessible globals at lines 31-35, 263-265).
2. Confirmed t0047's per-synapse-direct conductances at gNMDA = 0.5 nS (PD/ND for NMDA, AMPA, GABA)
   match the baseline used in `results/results_summary.md` lines 15-22.
3. Wrote `research/research_code.md` covering all 7 questions with concrete file:line references;
   ran `verify_research_code.py` — PASSED with 0 errors and 0 warnings.

## Outputs

* tasks/t0049_seclamp_cond_remeasure/research/research_code.md

## Issues

No issues encountered. The library aggregator does not exist in this branch (libraries were
enumerated by direct filesystem walk inside the research file); this is documented but not a blocker
for the implementation step.
