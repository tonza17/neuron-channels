---
spec_version: "3"
task_id: "t0009_calibrate_dendritic_diameters"
step_number: 5
step_name: "research-internet"
status: "completed"
started_at: "2026-04-19T23:00:42Z"
completed_at: "2026-04-19T23:08:40Z"
---
## Summary

Extended the corpus survey with 14 external sources, with special focus on harvesting the per-
compartment diameter profile from Poleg-Polsky & Diamond 2016 ModelDB 189347. Confirmed the model
ships a `.hoc` file (not SWC) where morphology lives in `pt3dadd(x, y, z, diam)` calls, and
identified the Hanson-lab MIT-licensed GitHub mirror as the easiest harvest target. Documented
Python tooling (NeuroM, pyswc), confirmed neither is in `pyproject.toml`, and verified no 2023-2026
DSGC reconstruction supersedes Poleg-Polsky for mouse ON-OFF cells.

## Actions Taken

1. Spawned a general-purpose subagent running the `/research-internet` skill to perform web research
   covering ModelDB 189347, SWC-editing Python tools, NeuroMorpho.org calibration conventions, and
   recent DSGC reconstructions.
2. The subagent executed 12 web searches and fetched / inspected ModelDB and GitHub pages to extract
   concrete diameter numbers (soma 0.88-10.6 µm contour, primary dendrite ~11.0-11.5 µm, some
   `diam=0` nodes to filter).
3. The subagent authored `research/research_internet.md` with all seven mandatory sections and 14
   cited sources.
4. Ran `verify_research_internet` — PASSED with 0 errors and 0 warnings.
5. Formatted the research file with `uv run flowmark --inplace --nobackup`.

## Outputs

* `tasks/t0009_calibrate_dendritic_diameters/research/research_internet.md`

## Issues

No issues encountered. A Python harvest script will be needed in the implementation step to parse
`RGCmodel.hoc` from the Hanson mirror and aggregate per-section diameters by Strahler order.
Dependencies NeuroM (or pyswc) may need to be added to `pyproject.toml`.
