---
spec_version: "3"
task_id: "t0010_hunt_missed_dsgc_models"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-04-20T14:40:04Z"
completed_at: "2026-04-20T14:42:30Z"
---
## Summary

Wrote `results/suggestions.json` (v2 spec) containing six follow-up suggestions: three hand-port
tasks (one per failed HIGH-priority candidate: Hanson2019, deRosenroll2026, PolegPolsky2026), a
simulator-diversity survey covering Arbor and NetPyNE reimplementations, a headless-port scaffold
library to unblock future porting work, and an Elsevier-login fallback for the paper-download
workflow. Suggestions cover every surfaced P2 failure and every workflow gap identified during the
three-pass search. IDs run S-0010-01 through S-0010-06; priorities are 3 high, 2 medium, 1 low.
`verify_suggestions` PASSED with 0 errors and 0 warnings.

## Actions Taken

1. Read `arf/specifications/suggestions_specification.md` to confirm the v2 schema, ID format
   `S-XXXX-NN`, required fields, and allowed `kind`/`priority`/`status` values.
2. Inventoried the existing categories under `meta/categories/` so each suggestion's `categories`
   field only references valid slugs (`direction-selectivity`, `compartmental-modeling`,
   `retinal-ganglion-cell`, `synaptic-integration`).
3. Wrote six suggestions covering: (a) the three P2-failed HIGH-priority ports, (b) a
   simulator-diversity follow-up (Arbor + NetPyNE), (c) a headless-port scaffold library, (d) an
   Elsevier-login fallback for /add-paper. Each includes an `id`, `title`, `description` (20-1000
   chars), `kind`, `priority`, `source_task`, `source_paper`, and `categories`.
4. Ran `verify_suggestions` — PASSED with 0 errors, 0 warnings.

## Outputs

* `tasks/t0010_hunt_missed_dsgc_models/results/suggestions.json`
* `tasks/t0010_hunt_missed_dsgc_models/logs/steps/014_suggestions/step_log.md`

## Issues

No issues encountered. All six suggestions reference real upstream assets (three GitHub repos, one
Zenodo DOI, two paper DOIs already registered in t0010) and realistic follow-up scopes.
