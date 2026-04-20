---
spec_version: "3"
task_id: "t0013_resolve_morphology_provenance"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-20T16:34:55Z"
completed_at: "2026-04-20T16:36:10Z"
---
## Summary

Reviewed the dependency task `t0005_download_dsgc_morphology` to understand the structure of the
`dsgc-baseline-morphology` dataset asset, identify the exact field that must be updated by the
correction (`source_paper_id`, currently `null`), and confirm the archived NeuroMorpho REST
payload's attribution of the reconstruction to DOI `10.1016/j.cub.2018.03.001`.

## Actions Taken

1. Read `assets/dataset/dsgc-baseline-morphology/details.json` and `description.md` from the
   dependency task to identify the correction target field and capture the already-recorded
   provenance conflict.
2. Read `logs/steps/009_implementation/neuromorpho_metadata.json` from the dependency to confirm the
   NeuroMorpho REST record reports `reference_doi: ["10.1016/j.cub.2018.03.001"]` and
   `reference_pmid: ["29606419"]`.
3. Drafted `research/research_code.md` with the correction target, both candidate DOIs, and the
   recommended implementation approach including the exact structure of the correction asset.

## Outputs

- `tasks/t0013_resolve_morphology_provenance/research/research_code.md`
- `tasks/t0013_resolve_morphology_provenance/logs/steps/006_research-code/step_log.md`

## Issues

No issues encountered.
