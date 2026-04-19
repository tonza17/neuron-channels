# Brainstorm session 3 — Detailed Results

## Session Context

Third brainstorm in the project. Called by the researcher after the t0007 NEURON/NetPyNE install
task merged, while t0009 was in progress on a separate worktree. The researcher asked for eight new
literature-survey tasks, twenty papers each, one per project category.

## State of the Project at Session Start

* Tasks: 13 total — 7 completed (t0001 to t0007), 1 in-progress (t0009), 5 not-started (t0008,
  t0010, t0011, t0012, t0013).
* Suggestions: 20 active uncovered, spread across all project categories.
* Budget: `total_budget` 0.0 USD, spend 0.0 USD, stop threshold reached (trivially, because the
  budget is zero). This blocks any task whose task-type has `has_external_costs: true`.
* Paper corpus: 20 papers in
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`. Categories are heavily
  overlapping — most papers carry two to four category tags.

## Concerns Surfaced

1. **Category overlap across existing papers** — the 20 t0002 papers each carry 2-4 category tags,
   so eight surveys at 20 papers each would generate heavy duplication.
2. **Saturation of some categories** — `direction-selectivity`, `compartmental-modeling`, and
   `retinal-ganglion-cell` are already well-covered by t0002 plus t0010.
3. **Budget gate** — `literature-survey` has `has_external_costs: true`. A zero `total_budget`
   blocks task creation outright, even though the actual spend for paper downloads is zero.
4. **Paywalled papers** — many relevant papers are behind institutional paywalls. The agent cannot
   download them. The researcher can, from their university account.

## Resolution

### Scope Cut

Drop the three saturated categories. Keep five: `cable-theory`, `dendritic-computation`,
`patch-clamp`, `synaptic-integration`, `voltage-gated-channels`. Target ~25 papers per survey
instead of 20 — extra headroom for dedup against the t0002 corpus and for papers that fail quality
filters mid-task. Total target: ~125 papers, expected ~80-100 unique after dedup across tasks.

### Budget Bump

Raise `project/budget.json` `total_budget` from 0.0 to 1.0 USD. This is nominal — the budget field
tracks paid third-party services, not Claude Code tokens, and the planned surveys use no paid APIs.
The bump exists only to clear the mechanical gate on `literature-survey`.

### Paywalled-Paper Workflow

Each survey task writes an `intervention/paywalled_papers.md` listing DOIs for papers it could not
download. The researcher retrieves these from their institutional account. A follow-up correction
pass then upgrades each affected paper asset's `download_status` from `"failed"` to `"success"` and
places the PDF under `files/`. The paper-asset specification v3 supports this failure-then-retrieval
pattern natively.

## File Manifest

### Created or Modified in This Task

* `tasks/t0014_brainstorm_results_3/` — full brainstorm task folder (scaffolded Phase 4, written
  Phase 5, finalised Phase 6)
* `tasks/t0014_brainstorm_results_3/results/suggestions.json` — 5 suggestions S-0014-01 through
  S-0014-05
* `project/budget.json` — `total_budget` 0.0 → 1.0

### Child Tasks Created

* `tasks/t0015_literature_survey_cable_theory/` — S-0014-01
* `tasks/t0016_literature_survey_dendritic_computation/` — S-0014-02
* `tasks/t0017_literature_survey_patch_clamp/` — S-0014-03
* `tasks/t0018_literature_survey_synaptic_integration/` — S-0014-04
* `tasks/t0019_literature_survey_voltage_gated_channels/` — S-0014-05

Each child task has `task_types: ["literature-survey"]`, no dependencies,
`expected_assets: {"paper": 25, "answer": 1}`, and `source_suggestion` pointing back to its
originating suggestion.

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

Cross-task duplicates (same DOI appearing in e.g. both t0015 and t0018) are allowed — each task
keeps its own copy. A later deduplication task will apply corrections.

## Verification

* `verify_task_file t0014_brainstorm_results_3` — passed (1 warning TF-W005 for empty
  `expected_assets`; brainstorm tasks produce no assets).
* `verify_suggestions t0014_brainstorm_results_3` — passed, 0 errors, 0 warnings.
* `verify_logs t0014_brainstorm_results_3` — passed, 0 errors (warnings about missing session
  captures resolved by running `capture_task_sessions`).
* `verify_task_file` — passed with 0 errors on each of t0015-t0019.
