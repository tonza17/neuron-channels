---
spec_version: "3"
task_id: "t0010_hunt_missed_dsgc_models"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-20T13:13:44Z"
completed_at: "2026-04-20T13:23:40Z"
---
## Summary

Produced `research/research_code.md` (3,327 body words) cataloguing every reusable entrypoint any
t0010 port-attempt needs: the t0012 `tuning_curve_loss.score()` library function and its identity
gate, the `TUNING_CURVE_CSV_COLUMNS` schema constant, t0008 scripts (`run_nrnivmodl.cmd`,
`build_cell.load_neuron`, `run_tuning_curve.py`, `score_envelope.py`, the two smoke tests,
`swc_io.py`), and the t0009 calibrated morphology SWC. Flagged seven concrete port-blocking gotchas
(Windows-only DLL path, HOC backslash escaping, missing `stdrun.hoc` auto-source, HOC `create`-block
bundled-topology coupling, NetPyNE incompatibility with DSGC HOC templates, the DS-protocol-mismatch
risk that sunk t0008's envelope score, and the library aggregator absence in this snapshot). Ends
with a CONFORMANCE CHECKLIST (library asset + canonical `tuning_curve.csv` + t0012 envelope scoring
with identity gate + `data/candidates.csv` row) every port-attempt agent must satisfy.
`verify_research_code.py` PASSED with 0 errors and 0 warnings.

## Actions Taken

1. Delegated to a subagent running the `/research-code` skill; subagent enumerated task artefacts
   via aggregators (tasks, libraries, datasets, answers) and read the t0008, t0012, t0009, and t0007
   code/library surfaces without walking `tasks/` directly.
2. Subagent wrote `research/research_code.md` with the spec sections (Objective, Background,
   Methodology Review, Key Findings, Recommended Approach, References) plus a CONFORMANCE CHECKLIST,
   indexed 10 reusable entrypoints with labels (import-via-library vs copy-into-task), and ran
   `flowmark` on the result.
3. Subagent ran `verify_research_code.py` — PASSED 0/0.

## Outputs

* `tasks/t0010_hunt_missed_dsgc_models/research/research_code.md`
* `tasks/t0010_hunt_missed_dsgc_models/logs/steps/006_research-code/step_log.md`

## Issues

No issues encountered. t0011 (`tuning-curve-viz`) is still `not_started`, so the visualisation
chaining cannot happen in this task; port-attempt CSVs must stick strictly to the canonical schema
so t0011 can consume them later when it runs.
