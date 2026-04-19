# Literature survey: cable theory and dendritic filtering

## Motivation

The t0002 corpus concentrates on direction-selective retinal ganglion cell (DSGC) compartmental
models. Downstream calibration and optimisation tasks (segment discretisation, morphology-sensitive
tuning, dendritic attenuation) need a deeper grounding in classical cable theory and passive
dendritic filtering than t0002 provides. This task broadens the corpus into the foundational theory.
Source suggestion: S-0014-01 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Rall-era foundations — passive cable equation, equivalent cylinder, classical Rall papers.
2. Segment discretisation guidelines — `d_lambda` rule, spatial-frequency constraints on `nseg`.
3. Branched-tree impedance — transfer impedance, voltage attenuation in branched dendrites.
4. Frequency-domain analyses — input impedance, synaptic-event filtering, chirp / ZAP analyses.
5. Transmission in thin dendrites — space constant, propagation failure, passive integration
   limits.

Exclusion: do not re-add any DOI already present in the t0002 corpus (20 DOIs under
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`). Duplicates discovered mid
task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` with search terms targeting each of the five themes above.
2. For each shortlisted paper, invoke `/download-paper` — the skill produces a v3-compliant paper
   asset (`details.json`, summary document, files). Papers behind institutional paywalls are
   recorded as `download_status: "failed"` and added to `intervention/paywalled_papers.md` for the
   researcher to retrieve manually from their institutional account.
3. After the paper set is assembled, write one answer asset that synthesises the corpus by theme and
   maps each paper to its relevance for the project's direction-selectivity modelling work.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant). Some may have
  `download_status: "failed"` pending manual retrieval.
* One answer asset under `assets/answer/` synthesising the five themes and identifying the
  cable-theory parameters most directly useful for downstream DSGC tasks.
* `intervention/paywalled_papers.md` listing DOIs the researcher must download manually.

## Compute and Budget

No paid services required for the automated pass. The task type `literature-survey` is gated on the
project budget — the brainstorm session set `project/budget.json` `total_budget` to $1 to clear
the gate; no actual spend is expected.

## Dependencies

None. This task is independent of the t0002 corpus (beyond the deduplication constraint).

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py` (accounting for some paywalled failures).
* The answer asset passes `verify_answer_asset.py`.
* `intervention/paywalled_papers.md` exists with a DOI list if any downloads failed.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.
