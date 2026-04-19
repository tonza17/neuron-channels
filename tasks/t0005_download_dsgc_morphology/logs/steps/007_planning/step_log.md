---
spec_version: "3"
task_id: "t0005_download_dsgc_morphology"
step_number: 7
step_name: "planning"
status: "completed"
started_at: "2026-04-19T09:03:17Z"
completed_at: "2026-04-19T09:20:00Z"
---
# planning

## Summary

Selected the morphology to download, justified the selection against the t0002 shortlist, and wrote
`plan/plan.md` (spec v5) with all eleven mandatory sections plus frontmatter. Target is the Feller
archive ON-OFF mouse DSGC `141009_Pair1DSGC` (NeuroMorpho neuron_id 102976) from Morrie & Feller
2018, distributed as a CNG-curated SWC. The plan decomposes the task text into five `REQ-*`
requirements, each mapped to one of six implementation steps grouped into three milestones
(selection, download+validate, asset registration), and closes with concrete verificator commands.
The plan also records that the dataset folder will be `dsgc-baseline-morphology` (hyphens) rather
than `dsgc_baseline_morphology` (underscores) because the dataset asset spec v2 regex forbids
underscores in `dataset_id`.

## Actions Taken

1. Ran `uv run python -u -m arf.scripts.utils.prestep t0005_download_dsgc_morphology planning` to
   flip step 7 to `in_progress` and create the step log directory.
2. Re-read the t0002 answer asset `full_answer.md` and `task_description.md`, queried NeuroMorpho's
   REST API to confirm the target neuron record exists, and reviewed the dataset asset specification
   v2 and plan specification v5.
3. Wrote `plan/plan.md` covering Objective, Task Requirement Checklist (REQ-1..REQ-5), Approach
   (with one rejected alternative: Briggman SBEM reconstructions), Cost Estimation ($0), Step by
   Step (6 numbered steps, Step 4 marked `[CRITICAL]`), Remote Machines (none), Assets Needed,
   Expected Assets, Time Estimation, Risks & Fallbacks (5-row table), and Verification Criteria (4
   bullet points with exact commands).

## Outputs

* `tasks/t0005_download_dsgc_morphology/plan/plan.md`
* `tasks/t0005_download_dsgc_morphology/logs/steps/007_planning/step_log.md`

## Issues

No issues encountered. One design decision to flag for the implementation step: the dataset folder
must be `dsgc-baseline-morphology` (hyphens), not `dsgc_baseline_morphology` (underscores, as
suggested by `task_description.md`), because the dataset asset v2 regex
`^[a-z0-9]+([.\-][a-z0-9]+)*$` does not permit underscores. The plan records this explicitly.
