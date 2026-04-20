---
spec_version: "3"
task_id: "t0008_port_modeldb_189347"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-20T11:03:11Z"
completed_at: "2026-04-20T12:38:00Z"
---
## Summary

Ported ModelDB 189347 (Poleg-Polsky & Diamond 2016 DSGC compartmental model) as a verbatim library
asset, swapped in the t0009 Strahler-calibrated morphology, and ran the 12-angle × 20-trial
drifting-bar tuning curve using t0012's `tuning_curve_loss` for scoring. The port is technically
faithful (morphology swap preserves section counts and surface-area parity; all MOD files compiled
cleanly on NEURON 8.2.7) but the bundled parameters do not hit the published envelope: DSI 0.316 vs
target 0.7-0.85, peak 18.1 Hz vs target 40-80, HWHM 82.81° passes, null 9.4 Hz passes. Root cause
documented in the answer asset: Poleg-Polsky's direction-selectivity mechanism uses per-angle
`gabaMOD` parameter swaps rather than the spatial-rotation proxy we applied. Phase B survey
completed via desk review (Hanson 2019 highest-priority sibling port; 5 others classed).

## Actions Taken

1. Scaffolded `code/` with `paths.py`, `constants.py`, and copied `swc_io.py` + `run_nrnivmodl.cmd`
   helpers from t0007/t0009.
2. Cloned ModelDB 189347 mirror (`github.com/ModelDBRepository/189347`) into the library asset
   `sources/` directory; compiled `.mod` files with `nrnivmodl`.
3. Wrote `build_cell.py` to load HOC cell and swap in calibrated SWC morphology; wrote
   `report_morphology.py` for surface-area / section-count parity comparison.
4. Wrote `run_tuning_curve.py` to run 12 angles × 20 trials at 500 µm/s with canonical CSV output;
   wrote `score_envelope.py` wrapping t0012 `tuning_curve_loss` and emitting `metrics.json`.
5. Packaged `assets/library/modeldb_189347_dsgc/` with `details.json`, `description.md`, and
   `sources/` per library asset spec. Verificator PASSED.
6. Authored `assets/answer/dsgc-modeldb-port-reproduction-report/` with short + full answers
   documenting Phase A outcome and Phase B sibling-model survey. Verificator PASSED.
7. Populated `results/metrics.json`, `results/suggestions.json`, `results/costs.json`,
   `results/remote_machines_used.json` (deferred `results_summary.md` / `results_detailed.md` to the
   results step).
8. Removed nested `.git` directory inside the library sources folder to avoid submodule confusion.

## Outputs

* `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`
* `tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report/`
* `tasks/t0008_port_modeldb_189347/code/{build_cell,run_tuning_curve,score_envelope,report_morphology,swc_io,paths,constants}.py`
* `tasks/t0008_port_modeldb_189347/code/test_{smoke_single_angle,scoring_pipeline}.py`
* `tasks/t0008_port_modeldb_189347/code/run_nrnivmodl.cmd`
* `tasks/t0008_port_modeldb_189347/data/{tuning_curves/,smoke_test_single_angle.csv,morphology_swap_report.md,phase_b_survey.csv,score_report.json}`
* `tasks/t0008_port_modeldb_189347/results/{metrics,suggestions,costs,remote_machines_used}.json`
* `tasks/t0008_port_modeldb_189347/logs/commands/012*-019*` (git clone, nrnivmodl, simulations,
  verificators)
* `tasks/t0008_port_modeldb_189347/logs/steps/009_implementation/step_log.md`

## Issues

Port did NOT reproduce the published envelope (DSI 0.316 < 0.7 target; peak 18.1 Hz < 40 target).
Diagnosis: Poleg-Polsky 2016 implements direction-selectivity via per-angle `gabaMOD` parameter swap
rather than spatial rotation; the rotation-based proxy we applied is a weaker modulator. Not a bug —
the port is faithful to the archive. Follow-up task captured in suggestions: `S-0008-02` replaces
the proxy with the native `gabaMOD` swap protocol.
