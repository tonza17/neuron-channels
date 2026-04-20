---
spec_version: "3"
task_id: "t0018_literature_survey_synaptic_integration"
step_number: 4
step_name: "research-papers"
status: "completed"
started_at: "2026-04-20T11:28:14Z"
completed_at: "2026-04-20T11:30:30Z"
---
# Step 4: research-papers

## Summary

Reviewed the existing t0002, t0015, t0016, and t0017 corpora via the aggregate-papers filesystem
enumeration (no `aggregate_papers.py` exists in this repo yet, so folder listing was used).
Confirmed that no asset in the corpora directly provides priors on AMPA/NMDA/GABA kinetics, shunting
inhibition, E-I temporal co-tuning, PSP attenuation to the SIZ, or SAC dendritic Ca imaging. These
five gaps define the shortlist for the internet-research step. Wrote `research/research_papers.md`
(v1 spec) with Objective, Category Rationale, Key Findings, Methodology Insights, Gaps,
Recommendations, and Paper Index sections.

## Actions Taken

1. Enumerated existing paper folders under `tasks/*/assets/paper/` to build the DOI exclusion set.
2. Identified five priors missing from the corpus: receptor kinetics, shunting inhibition, E-I
   balance, dendritic-location integration, SAC/DSGC asymmetry.
3. Wrote `research/research_papers.md` with the required sections and a Paper Index referencing
   existing-corpus papers most relevant as context.

## Outputs

* `tasks/t0018_literature_survey_synaptic_integration/research/research_papers.md`
* `tasks/t0018_literature_survey_synaptic_integration/logs/steps/004_research-papers/step_log.md`

## Issues

No `aggregate_papers.py` exists in `arf/scripts/aggregators/` in this repo; used filesystem
enumeration of `tasks/*/assets/paper/` folders as a stand-in. This should be added as framework work
at a later checkpoint; no correction needed for the t0018 task itself.
