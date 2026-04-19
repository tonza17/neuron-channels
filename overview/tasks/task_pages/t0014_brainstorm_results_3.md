# ✅ Brainstorm results session 3

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0014_brainstorm_results_3` |
| **Status** | ✅ completed |
| **Started** | 2026-04-19T23:10:00Z |
| **Completed** | 2026-04-19T23:45:00Z |
| **Duration** | 35m |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0014_brainstorm_results_3/`](../../../tasks/t0014_brainstorm_results_3/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0014_brainstorm_results_3/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0014_brainstorm_results_3/task_description.md)*

# Brainstorm Session 3 — Per-Category Literature-Survey Wave

## Context

The project has completed its first two task waves:

* **Wave 1** (t0001-t0005): foundational brainstorm, DSGC-focused compartmental-model
  literature survey, simulator survey, canonical target tuning curve, baseline DSGC morphology
  download.
* **Wave 2** (t0007-t0013, planned by t0006): NEURON install (t0007 done), plus calibration,
  porting, visualisation, scoring, and provenance tasks (t0008-t0013 still in-flight or not
  started).

The paper corpus contains 20 DOIs from t0002 (DSGC compartmental models). Categories
`direction-selectivity`, `compartmental-modeling`, and `retinal-ganglion-cell` are already
well-covered by that survey. Five remaining categories are under-covered: `cable-theory`,
`dendritic-computation`, `patch-clamp`, `synaptic-integration`, `voltage-gated-channels`.

## Session Goal

Plan a per-category literature-survey wave (Wave 3) that broadens the paper corpus so the
project's research questions about Na/K conductance combinations, active-vs-passive dendrites,
and synaptic kinetics can be grounded in the wider neuroscience literature rather than only
DSGC-specific work.

## Decisions

1. **Drop the 3 saturated categories** (direction-selectivity, compartmental-modeling,
   retinal-ganglion-cell). The existing t0002 corpus + queued t0010 (hunt missed DSGC models)
   cover them adequately.

2. **Create 5 new literature-survey tasks** (t0015-t0019), one per remaining category, each
   targeting ~25 category-relevant papers with cross-category overlap accepted (option (b)
   from the brainstorm discussion). Total attempted: ~125 papers, expected unique ~80-100
   after cross-task dedup (addressed by a later dedup-checkpoint task).

3. **Exclude the 20-DOI t0002 corpus** from each new task's search to avoid wasting download
   budget on already-owned papers.

4. **Bump `project/budget.json` `total_budget` from $0 to $1** so the mechanical
   `has_external_costs: true` gate on the `literature-survey` task type does not block
   execution. Literal expected spend remains $0 (arXiv, PubMed Central, ModelDB, and
   open-access sources are free; summarisation is done in-session).

5. **Paywalled paper protocol**: each task lists paywalled DOIs in
   `intervention/paywalled_papers.md`; the researcher downloads PDFs manually from their
   institutional account into `assets/paper/<paper_id>/files/` and the task then upgrades
   `download_status` to `"success"` with a full summary in a follow-up pass.

## New Suggestions Produced

Five dataset-kind suggestions (S-0014-01 through S-0014-05), each `priority: high`, one per
new task. These are recorded in `results/suggestions.json` and become the `source_suggestion`
for their respective child task.

## Out of Scope

* No experiments this session — this is a planning-only brainstorm.
* No corrections — t0002 corpus is correct; we are extending, not correcting.
* No new asset types or task types — `literature-survey` already exists.

</details>

## Suggestions Generated

<details>
<summary><strong>Literature survey: cable theory and dendritic filtering (target
~25 papers)</strong> (S-0014-01)</summary>

**Kind**: dataset | **Priority**: high

Systematically survey cable-theory and passive dendritic-filtering literature relevant to
direction-selective retinal ganglion cells. Target ~25 category-relevant papers spanning
Rall-era foundations, modern compartmental treatments, impedance / space-constant analyses,
and segment-discretisation guidelines. Exclude the 20 DOIs already in the t0002 corpus.
Output: paper assets + synthesis document organised by theme (classical cable theory, segment
discretisation, branched-tree impedance, frequency-domain analyses, transmission in thin
dendrites).

</details>

<details>
<summary><strong>Literature survey: dendritic computation outside DSGCs (target
~25 papers)</strong> (S-0014-02)</summary>

**Kind**: dataset | **Priority**: high

Systematically survey dendritic-computation literature beyond DSGC-specific work. Target ~25
category-relevant papers covering NMDA spikes, Na+/Ca2+ dendritic spikes, plateau potentials,
branch-level nonlinearities, sublinear-to-supralinear integration regimes, and
active-vs-passive comparisons in cortical and cerebellar neurons. Exclude the 20 DOIs already
in the t0002 corpus. Output: paper assets + synthesis highlighting which mechanisms plausibly
transfer to DSGC dendrites.

</details>

<details>
<summary><strong>Literature survey: patch-clamp recordings of RGCs and DSGCs (target
~25 papers)</strong> (S-0014-03)</summary>

**Kind**: dataset | **Priority**: high

Systematically survey patch-clamp recording literature relevant to validating DSGC
compartmental models. Target ~25 category-relevant papers covering somatic whole-cell
recordings of RGCs, voltage-clamp conductance dissections, space-clamp error analyses,
spike-train tuning-curve measurements, and in-vitro stimulus protocols. Exclude the 20 DOIs
already in the t0002 corpus. Output: paper assets + synthesis mapping each paper to the model
validation targets (AP rate, IPSC asymmetry, EPSP kinetics, null/preferred ratios).

</details>

<details>
<summary><strong>Literature survey: synaptic integration in RGC-adjacent systems
(target ~25 papers)</strong> (S-0014-04)</summary>

**Kind**: dataset | **Priority**: high

Systematically survey synaptic-integration literature relevant to DSGC dendrites. Target ~25
category-relevant papers covering AMPA/NMDA/GABA receptor kinetics, shunting inhibition, E-I
balance, temporal summation, dendritic-location dependence, synaptic-density scaling, and
SAC/DSGC inhibitory asymmetry. Exclude the 20 DOIs already in the t0002 corpus. Output: paper
assets + synthesis of kinetics parameters and E-I ratios usable as prior distributions in
later optimisation tasks.

</details>

<details>
<summary><strong>Literature survey: voltage-gated channels in retinal ganglion cells
(target ~25 papers)</strong> (S-0014-05)</summary>

**Kind**: dataset | **Priority**: high

Systematically survey voltage-gated-channel literature relevant to RGC/DSGC modelling. Target
~25 category-relevant papers covering Na_v 1.1-1.6 and K_v subtype expression, HH-family
kinetic models, subunit co-expression patterns in RGCs, ModelDB MOD-file provenance, and
Nav/Kv conductance-density estimates. Exclude the 20 DOIs already in the t0002 corpus. Output:
paper assets + synthesis mapping candidate Na/K conductance combinations to published DSGC
tuning-curve fits.

</details>

## Research

* [`research_code.md`](../../../tasks/t0014_brainstorm_results_3/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0014_brainstorm_results_3/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0014_brainstorm_results_3/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0014_brainstorm_results_3/results/results_summary.md)*

# Brainstorm session 3 — Summary

## Summary

Planned a five-task literature-survey wave (t0015-t0019) to broaden the project's paper corpus
beyond the DSGC-specific modelling focus of t0002. Authorised a $1 budget bump (to be applied
directly on `main` as a follow-up commit, since task branches cannot modify
`project/budget.json`) so `literature-survey` tasks clear the project budget gate without
incurring real spend. Confirmed a paywalled-paper workflow where each survey emits an
`intervention/paywalled_papers.md` the researcher resolves from their institutional account.

## Decisions

* **Five surveys, one per under-saturated category**: cable-theory, dendritic-computation,
  patch-clamp, synaptic-integration, voltage-gated-channels. Dropped `direction-selectivity`,
  `compartmental-modeling`, and `retinal-ganglion-cell` because t0002 plus t0010 already
  saturate them.
* **Target ~25 category-relevant papers per task** (not 20). Extra headroom compensates for
  the deduplication constraint and for papers that ultimately fail quality filters.
* **Exclude the 20 DOIs already in the t0002 corpus** from each survey. Duplicate hits must be
  dropped and recorded in the task log.
* **Budget bump to $1** — nominal, only to clear the `has_external_costs: true` gate on
  `literature-survey`; no paid service is expected to bill. Applied as a separate direct
  commit on `main` (not in this PR) because `verify_pr_premerge` forbids task branches from
  modifying `project/budget.json`.
* **Paywalled papers**: each survey task writes `intervention/paywalled_papers.md` with DOIs;
  the researcher downloads manually from their institutional account; a follow-up pass
  upgrades `download_status` from `"failed"` to `"success"` for each file retrieved.

## Metrics

Brainstorm tasks do not produce numerical metrics. Session metrics: 5 suggestions emitted, 5
child tasks created, 0 corrections, 0 paper assets, 0 remote machines, $0.00 direct cost.

## Verification

* `verify_task_file t0014_brainstorm_results_3` passed (1 warning TF-W005 for empty
  `expected_assets`).
* `verify_suggestions t0014_brainstorm_results_3` passed, 0 errors, 0 warnings.
* `verify_logs t0014_brainstorm_results_3` passed, 0 errors.
* `verify_task_file` passed with 0 errors on each of t0015-t0019.

## Outputs

* Five suggestions (S-0014-01 to S-0014-05) recorded in `results/suggestions.json`, one per
  surviving category.
* Five not-started child tasks created: `t0015_literature_survey_cable_theory`,
  `t0016_literature_survey_dendritic_computation`, `t0017_literature_survey_patch_clamp`,
  `t0018_literature_survey_synaptic_integration`,
  `t0019_literature_survey_voltage_gated_channels`.

## Next Steps

After this PR merges, bump `project/budget.json` `total_budget` to 1.0 USD on `main` directly,
then execute t0015-t0019 in parallel (up to three worktrees concurrent). After execution, a
follow-up correction task resolves any paywalled-paper failures using manually retrieved PDFs
from the researcher.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0014_brainstorm_results_3/results/results_detailed.md)*

# Brainstorm session 3 — Detailed Results

## Summary

Third brainstorm in the project. Planned a five-task literature-survey wave (t0015-t0019) to
broaden the paper corpus beyond DSGC-specific modelling. Dropped three already-saturated
categories, reduced the researcher's original ask from 8 × 20 to 5 × ~25 papers, and deferred
the required `project/budget.json` bump to a direct commit on `main` after merge (task
branches cannot modify `project/budget.json`). Locked in the paywalled-paper workflow: each
survey emits `intervention/paywalled_papers.md` so the researcher can manually retrieve PDFs
from their institutional account.

## Methodology

### Session Flow

The brainstorm followed the four canonical phases defined by `human-brainstorm` skill v8:

1. **Review project state** — ran `aggregate_tasks`, `aggregate_suggestions`,
   `aggregate_costs`; enumerated the 20-DOI t0002 corpus; read
   `meta/task_types/literature-survey/description.json`.
2. **Discuss decisions** — surfaced category overlap, saturation, budget-gate, and
   paywalled-paper concerns; offered researcher three scope options; confirmed option (b) with
   dropped categories.
3. **Apply decisions** — scaffolded the t0014 folder, wrote 5 suggestions, created 5 child
   task folders, and (attempted) a budget bump that later had to be reverted for verificator
   scope reasons.
4. **Finalize** — wrote results documents, captured sessions, ran verificators, opened PR,
   merged.

### State of the Project at Session Start

* Tasks: 13 total — 7 completed (t0001 to t0007), 1 in-progress (t0009), 5 not-started (t0008,
  t0010, t0011, t0012, t0013).
* Suggestions: 20 active uncovered, spread across all project categories.
* Budget: `total_budget` 0.0 USD, spend 0.0 USD, stop threshold reached (trivially, because
  the budget is zero). This blocks any task whose task-type has `has_external_costs: true`.
* Paper corpus: 20 papers in
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`. Categories are
  heavily overlapping — most papers carry two to four category tags.

### Concerns Surfaced

1. **Category overlap across existing papers** — the 20 t0002 papers each carry 2-4 category
   tags, so eight surveys at 20 papers each would generate heavy duplication.
2. **Saturation of some categories** — `direction-selectivity`, `compartmental-modeling`, and
   `retinal-ganglion-cell` are already well-covered by t0002 plus t0010.
3. **Budget gate** — `literature-survey` has `has_external_costs: true`. A zero `total_budget`
   blocks task creation outright, even though the actual spend for paper downloads is zero.
4. **Paywalled papers** — many relevant papers are behind institutional paywalls. The agent
   cannot download them. The researcher can, from their university account.

### Resolution

#### Scope Cut

Drop the three saturated categories. Keep five: `cable-theory`, `dendritic-computation`,
`patch-clamp`, `synaptic-integration`, `voltage-gated-channels`. Target ~25 papers per survey
instead of 20 — extra headroom for dedup against the t0002 corpus and for papers that fail
quality filters mid-task. Total target: ~125 papers, expected ~80-100 unique after dedup
across tasks.

#### Budget Bump — Deferred to Main

Raise `project/budget.json` `total_budget` from 0.0 to 1.0 USD. This is nominal — the budget
field tracks paid third-party services, not Claude Code tokens, and the planned surveys use no
paid APIs. The bump exists only to clear the mechanical gate on `literature-survey`.

Applied as a **separate direct commit on `main`** after this PR merges, because
`verify_pr_premerge` (check `PM-E003`) forbids a task branch from modifying
`project/budget.json` — it is not in the `ALLOWED_OUTSIDE_FILES` list in
`arf/scripts/verificators/common/constants.py`.

#### Paywalled-Paper Workflow

Each survey task writes an `intervention/paywalled_papers.md` listing DOIs for papers it could
not download. The researcher retrieves these from their institutional account. A follow-up
correction pass then upgrades each affected paper asset's `download_status` from `"failed"` to
`"success"` and places the PDF under `files/`. The paper-asset specification v3 supports this
failure-then-retrieval pattern natively.

## Verification

* `verify_task_file t0014_brainstorm_results_3` passed (1 warning TF-W005 for empty
  `expected_assets`; brainstorm tasks produce no assets).
* `verify_suggestions t0014_brainstorm_results_3` passed, 0 errors, 0 warnings.
* `verify_logs t0014_brainstorm_results_3` passed, 0 errors (warnings about missing session
  captures resolved by running `capture_task_sessions`; one residual non-zero-exit warning
  from a mis-invoked capture call kept in the log history).
* `verify_task_file` passed with 0 errors on each of t0015-t0019.

## Limitations

* Budget bump deferred to post-merge main commit; this PR alone does not enable t0015-t0019 to
  start. The researcher must run the main-branch commit before the child tasks can execute.
* Paper overlap between surveys is allowed by design (same DOI may appear in e.g. both t0015
  and t0018 paper folders). A later deduplication task will apply corrections.
* Surveys are capped at ~25 papers each to keep per-task scope manageable; coverage of any
  given category is not guaranteed exhaustive.

## Files Created

### This Task

* `tasks/t0014_brainstorm_results_3/` — full brainstorm task folder.
* `tasks/t0014_brainstorm_results_3/results/suggestions.json` — 5 suggestions S-0014-01
  through S-0014-05.

### Child Tasks Created

* `tasks/t0015_literature_survey_cable_theory/` — S-0014-01.
* `tasks/t0016_literature_survey_dendritic_computation/` — S-0014-02.
* `tasks/t0017_literature_survey_patch_clamp/` — S-0014-03.
* `tasks/t0018_literature_survey_synaptic_integration/` — S-0014-04.
* `tasks/t0019_literature_survey_voltage_gated_channels/` — S-0014-05.

Each child task has `task_types: ["literature-survey"]`, no dependencies, `expected_assets:
{"paper": 25, "answer": 1}`, and `source_suggestion` pointing back to its originating
suggestion.

## Deduplication Constraint

Each child survey must exclude the 20 DOIs in
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`:

```text
10.1002_cne.22678
10.1016_j.neuron.2005.06.036
10.1016_j.neuron.2016.02.013
10.1016_j.neuron.2016.04.041
10.1016_j.neuron.2017.07.020
10.1038_nature09818
10.1038_nature18609
10.1038_nrn3165
10.1113_jphysiol.1965.sp007638
10.1113_jphysiol.2008.161240
10.1113_jphysiol.2010.192716
10.1126_science.1189664
10.1152_jn.00123.2009
10.1162_neco.1997.9.6.1179
10.1371_journal.pcbi.1000899
10.1523_ENEURO.0261-21.2021
10.1523_JNEUROSCI.22-17-07712.2002
10.1523_JNEUROSCI.5017-13.2014
10.7554_eLife.42392
10.7554_eLife.52949
```

Cross-task duplicates (same DOI appearing in e.g. both t0015 and t0018) are allowed — each
task keeps its own copy. A later deduplication task will apply corrections.

</details>
