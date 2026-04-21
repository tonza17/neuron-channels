---
spec_version: "3"
task_id: "t0026_vrest_sweep_tuning_curves_dsgc"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-21T12:55:04Z"
completed_at: "2026-04-21T13:12:00Z"
---
## Summary

Surveyed the project's existing compartmental-model, trial-runner, and tuning-curve code to locate
the holding-potential handles and reusable utilities needed for the V_rest sweep. Confirmed that
both t0022 and t0024 set `h.v_init` then call `h.finitialize(V_INIT_MV)`, and that the leak reversal
is exposed as the `eleak_HHst` RANGE variable (plus `e_pas` on t0022's passive sections). Identified
the `tuning_curve_loss` library as the single reusable analysis import; all other trial-runner code
must be copied across because cross-task imports are forbidden.

## Actions Taken

1. Read `arf/specifications/research_code_specification.md` to confirm the required frontmatter
   fields and mandatory section list.
2. Read `tasks/t0022_modify_dsgc_channel_testbed/code/constants.py` and `run_tuning_curve.py` to
   identify the V_rest override insertion point (between `apply_params` and `h.finitialize`).
3. Read `tasks/t0008_port_modeldb_189347/code/build_cell.py` `apply_params` body (lines 280-316) to
   confirm it unconditionally sets `h.v_init = V_INIT_MV`, and grepped the backing HOC under
   `assets/library/modeldb_189347_dsgc/sources/` to locate `eleak_HHst` and `e_pas` assignments.
4. Read `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py`, `build_cell.py`, and
   `run_tuning_curve.py` to confirm t0024 uses HHst-only (no `pas`) and sets
   `sec.eleak_HHst = C.ELEAK_MV` per dendrite class.
5. Enumerated the six registered libraries under `tasks/*/assets/library/` and classified each as
   relevant (`modeldb_189347_dsgc`, `modeldb_189347_dsgc_dendritic`, `de_rosenroll_2026_dsgc`,
   `tuning_curve_loss`) or not relevant (`tuning_curve_viz`, `modeldb_189347_dsgc_gabamod`).
6. Wrote `research/research_code.md` with all mandatory sections, an explicit V_rest override block,
   and concrete file paths / function signatures / line counts for each reusable piece.
7. Ran flowmark on `research/research_code.md` then ran
   `verify_research_code.py t0026_vrest_sweep_tuning_curves_dsgc`; the verificator passed on the
   second attempt after correcting the Task Index bullet format to `* **Field**: value` and adding
   the [t0020] Task Index entry to match the inline citation.

## Outputs

* `tasks/t0026_vrest_sweep_tuning_curves_dsgc/research/research_code.md`

## Issues

Two verificator errors on the first run: `RC-E007` (Task Index bullets were missing the required
`**Field**:` bold markup) and `RC-E006` (a `[t0020]` inline citation had no matching Task Index
entry). Both fixed by editing the file and re-running the verificator — no blockers.
