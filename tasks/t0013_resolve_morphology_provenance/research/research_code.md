---
spec_version: "1"
task_id: "t0013_resolve_morphology_provenance"
research_stage: "code"
tasks_reviewed: 1
tasks_cited: 1
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-20"
status: "complete"
---
# Research Code: Morphology Asset Provenance Correction

## Task Objective

This task resolves a known provenance gap in the `dsgc-baseline-morphology` dataset asset registered
by the dependency task [t0005]. That asset's `details.json` currently sets `source_paper_id: null`
because the planning document nominated DOI `10.1016/j.neuron.2018.05.028` (Morrie & Feller 2018
*Neuron*) while the NeuroMorpho.org REST payload archived alongside the asset reports
`reference_doi: ["10.1016/j.cub.2018.03.001"]` (Murphy-Baum & Feller 2018 *Current Biology*). This
task downloads both candidate papers as paper assets, reads their Methods sections, applies the
decision procedure fixed in `task_description.md`, and files a correction that replaces
`source_paper_id: null` with the canonical paper's ID slug. The purpose of this code-research file
is to confirm exactly which field must be corrected and to capture the full archived evidence before
implementation.

## Library Landscape

No libraries are registered under `assets/library/` at this point in the project. The library
aggregator is not yet implemented in `arf/scripts/aggregators/`, and a direct filesystem check of
`assets/library/` confirms it is empty. There is therefore no library to import or reuse for this
task.

This task writes no production code: its deliverables are paper assets (produced by `/add-paper`), a
correction JSON (written by hand per `arf/specifications/corrections_specification.md`), and
analysis markdown. No library landscape exists to survey beyond that absence, and no library is
relevant here.

## Key Findings

### Correction target is a single scalar field on the existing dataset asset

`tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/details.json` encodes
source-paper provenance in exactly one field:

```json
"source_paper_id": null
```

Dataset-asset spec v2 (`meta/asset_types/dataset/specification.md`) defines this field as a
paper-asset ID slug (DOI-derived, slashes replaced with underscores) when the source paper is known.
The correction must replace `null` with the slug of whichever paper asset this task identifies as
canonical. No other field on the dataset asset needs to change — authors, year, URL, compartment
counts, file paths and description text are all independent of which paper first reported the
reconstruction. Source [t0005].

### NeuroMorpho.org machine-readable attribution

The archived REST payload at
`tasks/t0005_download_dsgc_morphology/logs/steps/009_implementation/neuromorpho_metadata.json`
records, for neuron 102976 (`141009_Pair1DSGC`):

```json
"reference_pmid": ["29606419"],
"reference_doi": ["10.1016/j.cub.2018.03.001"]
```

PMID `29606419` resolves to Murphy-Baum & Feller, *Current Biology* **28**(8):1217-1223.e2 (2018).
This is the single authoritative machine-readable attribution the Feller lab (via NeuroMorpho
curation) has assigned to the reconstruction. The description file for the asset already notes this
conflict explicitly in its `## Provenance note on DOI` block. Source [t0005].

### Both candidate papers must still be downloaded and their Methods inspected

Relying on the NeuroMorpho REST attribution alone is insufficient: the t0005 plan nominated
`10.1016/j.neuron.2018.05.028` (Morrie & Feller 2018 *Neuron*) on independent grounds, and the task
description explicitly instructs this task to validate attribution against each paper's Methods
section before committing. Finding `141009` or `Pair1DSGC` referenced in either paper's Methods — or
a matching paired SAC-DSGC recording description — is the intended primary evidence. NeuroMorpho's
REST attribution is corroborating, not decisive. Source [t0005].

### Decision procedure is fully specified in `task_description.md`

`task_description.md` for this task fixes the tie-breaking logic:

1. If exactly one paper's Methods cites the reconstruction (`141009`, `Pair1DSGC`, or a paired
   SAC-DSGC recording matching the deposition date), that paper is the source.
2. If both papers cite it, the earlier-published paper is the source.
3. If neither cites it, write an intervention file requesting the Feller lab resolve the
   attribution.

No separate planning decision about the procedure is needed: implementation follows it mechanically.
Source [t0005].

## Reusable Code and Assets

No code or library reuse applies. The task writes no Python and imports from no prior task.

Reusable project artefacts that this task *reads* (not copies):

* **`tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/details.json`**
  (~48 lines). **Reuse method: read-only reference**. Identifies the correction target field
  (`source_paper_id`) and the asset slug (`dsgc-baseline-morphology`). Not copied — this task must
  not modify the completed dependency's files. No adaptation needed.
* **`tasks/t0005_download_dsgc_morphology/logs/steps/009_implementation/neuromorpho_metadata.json`**
  (~1 line, ~2 KB JSON payload). **Reuse method: read-only reference**. Provides the archived
  NeuroMorpho REST attribution (`reference_doi`, `reference_pmid`) that this task validates. Not
  copied — the archived payload in the dependency is the single source of truth.
* **`tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/description.md`**
  (~180 lines). **Reuse method: read-only reference**. Confirms the `## Provenance note on DOI`
  block acknowledging the conflict this task resolves.

No `/add-paper`-produced helper, DOI slugger, or correction-writer needs to be copied: the canonical
DOI-to-slug converter `arf.scripts.utils.doi_to_slug` is a framework module invoked via `uv run` and
does not require copying into `code/`.

## Lessons Learned

The dependency task [t0005] registered the morphology asset with `source_paper_id: null` and a
hand-written `## Provenance note on DOI` block rather than blocking to resolve the attribution in
line. That deferral was the right call because it kept t0005 scoped to its single deliverable (a
verified SWC morphology) and produced an explicit, auditable provenance gap that a later task (this
one) could close via the corrections mechanism. The lesson is that provenance conflicts between a
planning document's nomination and an asset-provider's metadata should be surfaced as an explicit
note and a `null` field rather than being silently split-the-difference. Source [t0005].

A second lesson: archiving the full REST payload at a known path
(`logs/steps/009_implementation/neuromorpho_metadata.json`) made this task trivially verifiable. Any
future asset whose provenance depends on a third-party database should preserve the raw API response
the same way — without it, this correction would have required a fresh NeuroMorpho fetch and carried
the risk of silent schema changes.

## Recommendations for This Task

Derived directly from the findings above:

1. **Do not write any Python.** The deliverables are a correction JSON file, two paper assets, and
   markdown analysis; no `code/` module is warranted. This matches the correction task type pattern.
2. **Read-only references to [t0005] artefacts.** Never modify any file under
   `tasks/t0005_download_dsgc_morphology/`. All changes flow through a single correction file at
   `tasks/t0013_resolve_morphology_provenance/corrections/dataset_dsgc-baseline-morphology.json`.
3. **Invoke `/add-paper` twice.** Once for `10.1016/j.neuron.2018.05.028` and once for
   `10.1016/j.cub.2018.03.001`. Use the full `/add-paper` skill end-to-end so each paper asset
   passes `verify_paper_asset` with a v3-compliant summary that actually reflects having read the
   Methods.
4. **Grep Methods for `141009`, `Pair1DSGC`, `paired SAC-DSGC`, and `Sema6`.** These are the strings
   that unambiguously link a paper to the reconstruction. Record the exact quote(s) used.
5. **Apply the pre-specified decision procedure verbatim.** Do not introduce extra criteria. Record
   the mapping (evidence → chosen paper) in `results/results_detailed.md`.
6. **Write one correction file.** Per `corrections_specification.md`: `action: "update"`, target
   `dataset/dsgc-baseline-morphology`, `changes: {"source_paper_id": "<slug>"}`, and a rationale
   that cites the exact Methods quote(s).

## Task Index

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download DSGC Baseline Morphology
* **Status**: completed
* **Relevance**: Produced the `dsgc-baseline-morphology` dataset asset whose `source_paper_id` field
  is the sole target of this task's correction. Also archived the NeuroMorpho REST payload providing
  the machine-readable attribution that corroborates the Methods-based decision, and documented the
  pre-existing DOI conflict in its description file.
