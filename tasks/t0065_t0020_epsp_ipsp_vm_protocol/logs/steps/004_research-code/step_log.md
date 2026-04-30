---
spec_version: "3"
task_id: "t0065_t0020_epsp_ipsp_vm_protocol"
step_number: 4
step_name: "research-code"
status: "completed"
started_at: "2026-04-30T08:04:28Z"
completed_at: "2026-04-30T08:10:30Z"
---
## Summary

Surveyed prior task code (t0008, t0020, t0046, t0049) to identify reusable helpers and the correct
override sequencing for the deposited Poleg-Polsky 2016 cell. Wrote `research/research_code.md`
documenting the four-step "simplerun → override → re-update + re-placeBIP → finitialize +
continuerun" pattern that t0049 established and that this task adapts for EPSP/IPSP/FULL recording.

## Actions Taken

1. Read `tasks/t0008_port_modeldb_189347/code/build_cell.py` to confirm the public surface
   (`build_dsgc`, `apply_params`, `read_synapse_coords`, `SynapseCoords`).
2. Read `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py` to understand the
   gabaMOD-swap trial structure and the BIP-position guard.
3. Read `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py` and
   `sources/dsgc_model_exact.hoc` to confirm the `SpikesOn` → `exptype` → `init_active` → HH
   suppression chain.
4. Read `tasks/t0049_seclamp_cond_remeasure/code/run_seclamp.py` to identify the canonical
   override-then-rerun pattern for channel-isolation studies on this cell.
5. Inspected `dsgc_model_exact.hoc:115-150` (`init_active`) and `:316-334` (`simplerun`) to confirm
   that `simplerun` rewrites `b2gampa`, `b2gnmda`, `gabaMOD` on every call — meaning all
   conductance overrides must be applied AFTER simplerun.
6. Wrote `research/research_code.md` with the seven mandatory sections plus a Reusable Code and
   Assets table that cites function/file paths from t0008, t0020, t0046, t0049.

## Outputs

* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/research/research_code.md`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/logs/steps/004_research-code/step_log.md`

## Issues

No issues encountered.
