---
spec_version: "3"
task_id: "t0034_distal_dendrite_length_sweep_t0024"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-23T10:10:57Z"
completed_at: "2026-04-23T10:22:00Z"
---
## Summary

Spawned a research-code subagent that identified the t0024 driver, confirmed the distal- selection
rule is **different** from t0029 (t0024 uses its own `cell.terminal_dends` topology walk; t0029's
`h.RGC.ON` filter does NOT apply because t0024's morphology is loaded from `RGCmodelGD.hoc` via
`h.DSGC(0,0)`, not `h.RGC`). AR(2) ρ=0.6 must be preserved at every call site to keep t0024's
non-zero null firing. Anticipated runtime ~2.8 h for 840 trials.

## Actions Taken

1. Spawned a general-purpose subagent with the `/research-code` skill instructions and a prompt
   covering t0024 driver identification, distal-selection rule adaptation, AR(2) preservation,
   wall-time baselines, and Dan2018/Sivyer2013 predictions.
2. Subagent identified driver at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`
   with entry points `run_single_trial` and `run_sweep`; `DSGCCell.terminal_dends` is the
   pre-enumerated distal list (replaces t0029's h.RGC.ON filter).
3. Subagent flagged the critical adapter change: copy t0029 workflow but replace the distal
   selection logic with a t0024-specific helper that uses `cell.terminal_dends` directly.
4. Subagent wrote `research/research_code.md`, ran flowmark, and verified with
   `verify_research_code.py` wrapped in `run_with_logs.py`. Verificator returned 0 errors, 0
   warnings.

## Outputs

* `tasks/t0034_distal_dendrite_length_sweep_t0024/research/research_code.md`
* `tasks/t0034_distal_dendrite_length_sweep_t0024/logs/commands/...` (run_with_logs entries)
* `tasks/t0034_distal_dendrite_length_sweep_t0024/logs/steps/006_research-code/step_log.md` (this
  file)

## Issues

No issues encountered. Critical architectural difference surfaced (t0024 morphology loader differs
from t0022's — no RGC arbor; must use `terminal_dends` attribute). This is now locked into the plan.
