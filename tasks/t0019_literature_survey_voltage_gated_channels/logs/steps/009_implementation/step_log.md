---
spec_version: "3"
task_id: "t0019_literature_survey_voltage_gated_channels"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-20T12:46:11Z"
completed_at: "2026-04-20T13:02:00Z"
---
# Step 9: implementation

## Summary

Built 5 paper assets for the five voltage-gated-channel themes and synthesised them into one answer
asset tabulating a Nav/Kv combination per DOI and theme. All five source papers are paywalled; their
DOIs are recorded in `intervention/paywalled_papers.md` for manual retrieval.

## Actions Taken

1. Ran `code/build_paper_asset.py` five times (one invocation per DOI, with `--theme` 1-5). All five
   materialised as DOI-slug folders (`10.1002_cne.21173`, `10.1016_j.neuron.2007.07.031`,
   `10.1152_jn.1997.78.4.1948`, `10.1038_nn.2359`, `10.1038_nn2040`). All five assets have
   `download_status: "failed"`, `files/.gitkeep`, and
   `download_failure_reason: "No PDF URL supplied"`.
2. Wrote `intervention/paywalled_papers.md` listing all five DOIs with venue and Crossref-only
   availability note; ordered by retrieval priority (Kole2008, Hu2009, VanWart2006, Fohlmeister1997,
   Kole2007).
3. Created the answer asset `assets/answer/nav-kv-combinations-for-dsgc-modelling/` with
   `details.json` (spec v2, confidence medium, 5 source paper IDs), `short_answer.md` (Question,
   Answer, Sources sections; Answer is 5 sentences covering all 5 themes), and `full_answer.md` (9
   mandatory sections including Research Process, Evidence from Papers with inline citations to all
   5 papers, Synthesis with the Nav/Kv Combinations Table and 6 numbered modelling constraints, and
   Limitations). Flowmark-formatted all three files.
4. Ran
   `meta/asset_types/paper/verificator.py --task-id t0019_literature_survey_voltage_gated_channels`
   and confirmed all five paper assets pass with zero PA-E* errors. Remaining PA-W warnings (PA-W002
   Results bullet count, PA-W007 no country data, PA-W008 empty abstract, PA-W010 null institution
   country) are consistent with the paywalled template from t0018.
5. Ran
   `meta/asset_types/answer/verificator.py --task-id t0019_literature_survey_voltage_gated_channels`
   and confirmed zero errors and zero warnings.

## Outputs

* `assets/paper/10.1002_cne.21173/{details.json,summary.md,files/.gitkeep}` - VanWart2006
* `assets/paper/10.1016_j.neuron.2007.07.031/{details.json,summary.md,files/.gitkeep}` -
  KoleLetzkus2007
* `assets/paper/10.1152_jn.1997.78.4.1948/{details.json,summary.md,files/.gitkeep}` -
  FohlmeisterMiller1997
* `assets/paper/10.1038_nn.2359/{details.json,summary.md,files/.gitkeep}` - Hu2009
* `assets/paper/10.1038_nn2040/{details.json,summary.md,files/.gitkeep}` - Kole2008
* `assets/answer/nav-kv-combinations-for-dsgc-modelling/{details.json,short_answer.md,full_answer.md}`
* `intervention/paywalled_papers.md`

## Issues

No issues encountered. Paper-asset warnings are all expected paywalled-template consequences; the
Fohlmeister-Miller record has one additional PA-W010 warning because the Crossref record lists the
first-author institution as a free-text string with no country tag, consistent with the
pre-standardised 1997 APS metadata.
