---
spec_version: "3"
task_id: "t0019_literature_survey_voltage_gated_channels"
step_number: 4
step_name: "research-papers"
status: "completed"
started_at: "2026-04-20T12:27:06Z"
completed_at: "2026-04-20T12:28:30Z"
---
# Step 4: research-papers

## Summary

Reviewed the existing t0002, t0015, t0016, t0017, and t0018 corpora via filesystem enumeration (no
`aggregate_papers.py` exists in this repo, so folder listing under `tasks/*/assets/paper/` was used
as a stand-in). Confirmed that no asset in those corpora directly provides priors on Nav subunit
expression in RGCs, Kv subunit expression, RGC-specific HH-family kinetic models, RGC-type-specific
Nav/Kv subunit co-expression, or compartment-resolved Nav/Kv conductance densities. These five gaps
define the shortlist for the internet-research step. Wrote `research/research_papers.md` (v1 spec)
with Task Objective, Category Selection Rationale, Key Findings, Methodology Insights, Gaps and
Limitations, Recommendations, and Paper Index sections.

## Actions Taken

1. Enumerated existing paper folders under `tasks/*/assets/paper/` to build the DOI exclusion set.
2. Identified five voltage-gated-channel priors missing from the corpus: Nav subunit localisation,
   Kv subunit localisation, HH-family RGC kinetic models, subunit co-expression patterns, and
   compartment-resolved conductance densities.
3. Wrote `research/research_papers.md` with the required sections and a Paper Index referencing
   existing-corpus papers most relevant as context.

## Outputs

* `tasks/t0019_literature_survey_voltage_gated_channels/research/research_papers.md`
* `tasks/t0019_literature_survey_voltage_gated_channels/logs/steps/004_research-papers/step_log.md`

## Issues

No `aggregate_papers.py` exists in `arf/scripts/aggregators/` in this repo; used filesystem
enumeration of `tasks/*/assets/paper/` folders as a stand-in. Same situation encountered in t0018;
no correction needed for t0019 itself.
