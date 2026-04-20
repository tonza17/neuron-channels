# ⏳ Literature survey: patch-clamp recordings of RGCs and DSGCs

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0017_literature_survey_patch_clamp` |
| **Status** | ⏳ in_progress |
| **Started** | 2026-04-19T23:39:05Z |
| **Source suggestion** | `S-0014-03` |
| **Task types** | `literature-survey` |
| **Expected assets** | 25 paper, 1 answer |
| **Task folder** | [`t0017_literature_survey_patch_clamp/`](../../../tasks/t0017_literature_survey_patch_clamp/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0017_literature_survey_patch_clamp/task_description.md)*

# Literature survey: patch-clamp recordings of RGCs and DSGCs

## Motivation

The DSGC model needs validation against real electrophysiology. Patch-clamp recordings of
retinal ganglion cells provide the quantitative targets that optimisation and tuning-curve
scoring tasks (t0004, t0012) must match: somatic action-potential rates, EPSP/IPSC kinetics,
null/preferred response ratios. This survey assembles the experimental-data landscape
separately from the modelling corpus in t0002. Source suggestion: S-0014-03 from
t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Somatic whole-cell recordings of RGCs — firing-rate statistics, spike-threshold
   distributions.
2. Voltage-clamp conductance dissections — separating AMPA/NMDA/GABA currents during DS
   responses.
3. Space-clamp error analyses — how much of published conductance asymmetry is real vs an
   artefact of imperfect voltage clamp in extended dendrites.
4. Spike-train tuning-curve measurements — angle-resolved AP rates and their variability.
5. In-vitro stimulus protocols — moving bars, drifting gratings, and spots used to probe DS.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, giving weight to papers that publish raw
   conductance traces or tabulated tuning-curve peak rates.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset mapping each paper to the model-validation targets it provides (AP
   rate, IPSC asymmetry, EPSP kinetics, null/preferred ratios) with explicit numerical values.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` with a validation-target table keyed by paper DOI.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and contains a validation-target table with
  at least five numerical rows.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

</details>
