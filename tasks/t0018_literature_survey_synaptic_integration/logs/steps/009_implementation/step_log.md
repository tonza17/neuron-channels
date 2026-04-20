---
spec_version: "3"
task_id: "t0018_literature_survey_synaptic_integration"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-20T11:54:26Z"
completed_at: "2026-04-20T12:02:00Z"
---
# Step 9: implementation

## Summary

Built 5 paper assets for the five synaptic-integration themes and synthesised them into one answer
asset tabulating a prior distribution per DOI and theme. All five source papers are paywalled; their
DOIs are recorded in `intervention/paywalled_papers.md` for manual retrieval.

## Actions Taken

1. Ran `code/build_paper_asset.py` five times (one invocation per DOI, with `--theme` 1-5 and
   explicit `--citation-key`). Four of the five materialised as DOI-slug folders; Hausser & Mel
   2003's DOI `10.1016/s0959-4388(03)00075-8` contains parentheses that the canonical `doi_to_slug`
   rejects, so the builder fell back to the `no-doi_HausserMel2003_s0959-4388-03-00075-8` slug per
   spec. All five assets have `download_status: "failed"`, `files/.gitkeep`, and
   `download_failure_reason: "No PDF URL supplied"`.
2. Wrote `intervention/paywalled_papers.md` listing all five DOIs with venue and Crossref-only
   availability note; ordered by retrieval priority (EulerDetwilerDenk2002, Lester1990,
   KochPoggio1983, WehrZador2003, HausserMel2003).
3. Created the answer asset `assets/answer/synaptic-integration-priors-for-dsgc-modelling/` with
   `details.json` (spec v2, confidence medium, 5 source paper IDs), `short_answer.md` (Question,
   Answer, Sources sections; Answer is 5 sentences covering all 5 themes), and `full_answer.md` (9
   mandatory sections including Research Process, Evidence from Papers with inline citations to all
   5 papers, Synthesis with the Prior Distribution Table and 6 numbered modelling constraints, and
   Limitations). Flowmark-formatted all three files.
4. Ran
   `meta/asset_types/paper/verificator.py --task-id t0018_literature_survey_synaptic_integration`
   and confirmed all five paper assets pass with zero PA-E* errors. Remaining PA-W warnings (PA-W002
   Results bullet count, PA-W007 no country data, PA-W008 empty abstract) are consistent with the
   paywalled template from t0017.
5. Ran
   `meta/asset_types/answer/verificator.py --task-id t0018_literature_survey_synaptic_integration synaptic-integration-priors-for-dsgc-modelling`
   and confirmed zero errors and zero warnings (after tightening `## Answer` from 6 to 5 sentences
   to satisfy the 2-5 sentence rule).

## Outputs

* `assets/paper/10.1038_346565a0/{details.json,summary.md,files/.gitkeep}` - Lester1990
* `assets/paper/10.1073_pnas.80.9.2799/{details.json,summary.md,files/.gitkeep}` - KochPoggio1983
* `assets/paper/10.1038_nature02116/{details.json,summary.md,files/.gitkeep}` - WehrZador2003
* `assets/paper/no-doi_HausserMel2003_s0959-4388-03-00075-8/{details.json,summary.md,files/.gitkeep}`
  - HausserMel2003
* `assets/paper/10.1038_nature00931/{details.json,summary.md,files/.gitkeep}` -
  EulerDetwilerDenk2002
* `assets/answer/synaptic-integration-priors-for-dsgc-modelling/{details.json,short_answer.md,full_answer.md}`
* `intervention/paywalled_papers.md`

## Issues

Initial `## Answer` section in `short_answer.md` had 6 sentences (enumerated priors with a lead-in
sentence); answer verificator flagged AA-E013 (expected 2-5). Merged the lead sentence into the
first theme sentence to land at exactly 5 sentences; verificator now passes.
