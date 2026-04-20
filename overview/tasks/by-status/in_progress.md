# ⏳ Tasks: In Progress

3 tasks. ⏳ **3 in_progress**.

[Back to all tasks](../README.md)

---

## ⏳ In Progress

<details>
<summary>⏳ 0015 — <strong>Literature survey: cable theory and dendritic
filtering</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0015_literature_survey_cable_theory` |
| **Status** | in_progress |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-01` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-19T23:38:43Z |
| **Task page** | [Literature survey: cable theory and dendritic filtering](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Task folder** | [`t0015_literature_survey_cable_theory/`](../../../tasks/t0015_literature_survey_cable_theory/) |

# Literature survey: cable theory and dendritic filtering

## Motivation

The t0002 corpus concentrates on direction-selective retinal ganglion cell (DSGC)
compartmental models. Downstream calibration and optimisation tasks (segment discretisation,
morphology-sensitive tuning, dendritic attenuation) need a deeper grounding in classical cable
theory and passive dendritic filtering than t0002 provides. This task broadens the corpus into
the foundational theory. Source suggestion: S-0014-01 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Rall-era foundations — passive cable equation, equivalent cylinder, classical Rall papers.
2. Segment discretisation guidelines — `d_lambda` rule, spatial-frequency constraints on
   `nseg`.
3. Branched-tree impedance — transfer impedance, voltage attenuation in branched dendrites.
4. Frequency-domain analyses — input impedance, synaptic-event filtering, chirp / ZAP
   analyses.
5. Transmission in thin dendrites — space constant, propagation failure, passive integration
   limits.

Exclusion: do not re-add any DOI already present in the t0002 corpus (20 DOIs under
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`). Duplicates
discovered mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` with search terms targeting each of the five themes above.
2. For each shortlisted paper, invoke `/download-paper` — the skill produces a v3-compliant
   paper asset (`details.json`, summary document, files). Papers behind institutional paywalls
   are recorded as `download_status: "failed"` and added to `intervention/paywalled_papers.md`
   for the researcher to retrieve manually from their institutional account.
3. After the paper set is assembled, write one answer asset that synthesises the corpus by
   theme and maps each paper to its relevance for the project's direction-selectivity
   modelling work.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant). Some may have `download_status:
  "failed"` pending manual retrieval.
* One answer asset under `assets/answer/` synthesising the five themes and identifying the
  cable-theory parameters most directly useful for downstream DSGC tasks.
* `intervention/paywalled_papers.md` listing DOIs the researcher must download manually.

## Compute and Budget

No paid services required for the automated pass. The task type `literature-survey` is gated
on the project budget — the brainstorm session set `project/budget.json` `total_budget` to $1
to clear the gate; no actual spend is expected.

## Dependencies

None. This task is independent of the t0002 corpus (beyond the deduplication constraint).

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py` (accounting for some paywalled
  failures).
* The answer asset passes `verify_answer_asset.py`.
* `intervention/paywalled_papers.md` exists with a DOI list if any downloads failed.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

</details>

<details>
<summary>⏳ 0016 — <strong>Literature survey: dendritic computation beyond
DSGCs</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0016_literature_survey_dendritic_computation` |
| **Status** | in_progress |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-02` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-19T23:38:58Z |
| **Task page** | [Literature survey: dendritic computation beyond DSGCs](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Task folder** | [`t0016_literature_survey_dendritic_computation/`](../../../tasks/t0016_literature_survey_dendritic_computation/) |

# Literature survey: dendritic computation beyond DSGCs

## Motivation

Research question RQ4 (active vs passive dendrites) needs evidence from computational
neuroscience beyond the retinal literature. Cortical and cerebellar dendrites have been
studied far more extensively than DSGC dendrites, and the mechanisms and modelling conventions
developed there (NMDA spikes, Ca/Na plateaus, branch-level nonlinearities) are the natural
reference for whether active dendrites plausibly shape DSGC tuning curves. Source suggestion:
S-0014-02 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. NMDA spikes — thresholds, amplitudes, distance-dependence, supralinear integration.
2. Na+ and Ca2+ dendritic spikes — backpropagation, forward propagation, local spikes.
3. Plateau potentials — in-vivo evidence, role in coincidence detection, duration scaling.
4. Branch-level nonlinearities — independent subunits, clustered-vs-distributed input
   summation.
5. Sublinear-to-supralinear integration regimes — what controls the transition, which
   conditions make dendrites behave passively in practice.
6. Active-vs-passive modelling comparisons — cortical, cerebellar, hippocampal studies that
   built matched active and passive compartmental models and quantified the difference.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each of the six themes above with preference for review
   articles plus 2-4 primary studies per theme.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md` for the
   researcher to retrieve manually.
3. Write one answer asset synthesising which dendritic-computation mechanisms plausibly
   transfer to DSGC dendrites, with explicit caveats about anatomical and biophysical
   differences.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant), some possibly with
  `download_status: "failed"`.
* One answer asset under `assets/answer/` synthesising the six themes and flagging mechanisms
  most plausible for DSGC dendrites.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and explicitly addresses transferability to
  DSGC dendrites.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

</details>

<details>
<summary>⏳ 0017 — <strong>Literature survey: patch-clamp recordings of RGCs and
DSGCs</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0017_literature_survey_patch_clamp` |
| **Status** | in_progress |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-03` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-19T23:39:05Z |
| **Task page** | [Literature survey: patch-clamp recordings of RGCs and DSGCs](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Task folder** | [`t0017_literature_survey_patch_clamp/`](../../../tasks/t0017_literature_survey_patch_clamp/) |

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
