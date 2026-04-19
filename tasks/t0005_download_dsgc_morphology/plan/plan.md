---
spec_version: "2"
task_id: "t0005_download_dsgc_morphology"
date_completed: "2026-04-19"
status: "complete"
---
# Plan: Download candidate DSGC morphology

## Objective

Commit the project to a single reconstructed direction-selective ganglion cell (DSGC) morphology
that every downstream compartmental-modeling task can load. Download one SWC file from
NeuroMorpho.org that matches a reconstruction flagged by the t0002 literature survey as suitable for
DSGC modelling, verify it parses as a valid SWC tree, and register it as a dataset asset
(`dsgc-baseline-morphology`) with full provenance metadata. "Done" means the asset passes
`verify_dataset_asset.py` and a Python validator script loads it without errors.

## Task Requirement Checklist

The operative task text from `task.json` (`short_description`) and `task_description.md`:

> **Name**: Download candidate DSGC morphology
>
> **Short description**: Download a reconstructed direction-selective ganglion cell morphology (SWC)
> for use as the project's baseline cell.
>
> **Scope**: Download one reconstructed DSGC morphology in SWC format (or HOC / NeuroML if SWC is
> not available) from a public source such as NeuroMorpho.org, ModelDB, or a paper's supplementary
> materials. The morphology should be one of those flagged as suitable in t0002's answer asset.
>
> **Approach**: (1) Read t0002's answer asset to pick the recommended morphology. (2) Download the
> file and verify it loads as a valid SWC / HOC structure. (3) Record its provenance (source URL,
> paper DOI, reconstruction protocol) in the dataset asset metadata.
>
> **Expected Outputs**: One dataset asset under `assets/dataset/dsgc_baseline_morphology/`
> containing the morphology file(s) and metadata.
>
> **Verification Criteria**: Dataset asset passes `verify_dataset_asset.py`. The asset's
> `details.json` links back to the source paper or NeuroMorpho record. The downloaded file loads
> without errors in at least one candidate simulator library.

Concrete requirements extracted:

* **REQ-1** — Select one morphology from t0002's shortlist. Evidence: the Approach section of this
  plan names the chosen source and justifies it; Step 1 documents the selection. Satisfied by Step
  1\.
* **REQ-2** — Download the morphology as SWC (fall back to HOC/NeuroML only if SWC is unavailable)
  from a public source (NeuroMorpho.org / ModelDB / supplementary). Satisfied by Step 3.
* **REQ-3** — Verify the downloaded file parses as a valid SWC tree in a Python simulator-adjacent
  library (morphology parser). Satisfied by Step 4.
* **REQ-4** — Produce a dataset asset at `assets/dataset/dsgc-baseline-morphology/` with a
  `details.json` and `description.md` that record source URL, NeuroMorpho neuron ID, paper DOI, and
  reconstruction protocol. Satisfied by Step 5. Note the folder name uses hyphens
  (`dsgc-baseline-morphology`) rather than the underscore form in `task_description.md`; the dataset
  specification v2 regex `^[a-z0-9]+([.\-][a-z0-9]+)*$` forbids underscores in `dataset_id`, so the
  hyphen form is the only spec-compliant rendering.
* **REQ-5** — `verify_dataset_asset.py` passes with zero errors on the new asset. Satisfied by
  Step 6.

**Ambiguity**: `task_description.md` uses the folder name `dsgc_baseline_morphology` (underscored),
which would fail the dataset v2 asset-id regex. Plan resolves this by using
`dsgc-baseline-morphology` and recording the deviation explicitly in the step log and description.

## Approach

Select the **Feller-lab archive** reconstruction `141009_Pair1DSGC` (NeuroMorpho neuron_id 102976)
from the paper *"A Dense Starburst Plexus Is Critical for Generating Direction Selectivity"* (Morrie
& Feller, *Neuron* 2018, DOI `10.1016/j.neuron.2018.05.028`). This is a mouse ON-OFF DSGC
reconstructed with Neurolucida from confocal stacks, available as CNG-curated SWC
(`141009_Pair1DSGC.CNG.swc`). It is explicitly flagged in t0002's `how-does-dsgc-literature-...`
answer asset as a concrete, publicly hosted reconstruction of the ON-OFF DSGC cell type the project
targets, and its SWC passes NeuroMorpho's CNG curation (standard soma, connected tree, non-negative
radii).

Download pipeline: fetch the SWC with `curl` (or `urllib`) from the NeuroMorpho
`dableFiles/feller/CNG%20version/` endpoint → save under
`assets/dataset/dsgc-baseline-morphology/files/` → parse the SWC with a small Python validator
(`code/validate_swc.py`) that uses the stdlib to walk the compartment tree (no extra dependency
required; if `neurom` is already installed it will be used as a secondary check). Metadata derives
from the NeuroMorpho REST API record for neuron 102976 plus the Morrie & Feller 2018 DOI.

**Alternative considered**: the Briggman-lab SBEM DSGC reconstructions (Briggman et al. 2011).
Rejected because the SBEM dendrogram is distributed as MATLAB `.mat` skeletons rather than SWC, and
extracting a single DSGC skeleton requires running their custom MATLAB pipeline — out of scope for
a "download one file" task. The Feller SWC is already curated and immediately loadable.

**Task types**: `download-dataset` (matches the type in `task.json`). The download-dataset planning
guideline calls for a single asset with complete provenance and a parse-time validation check —
both are built into Steps 5-6 below.

## Cost Estimation

Total: **$0**. NeuroMorpho.org is free public data (CC-BY when cited). No paid APIs, no remote
compute. The project budget is unchanged; `download-dataset` has `has_external_costs: false`, so the
project-level budget gate is not engaged.

## Step by Step

Milestone A — Selection and preparation:

1. **Confirm selection from t0002.** Re-read
   `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/full_answer.md`,
   confirm the Morrie & Feller 2018 Feller-archive ON-OFF DSGC is in the shortlist, and write the
   neuron identifier (`141009_Pair1DSGC`, NeuroMorpho neuron_id 102976) to the step log. Satisfies
   REQ-1.

2. **Fetch NeuroMorpho metadata.** Query `https://neuromorpho.org/api/neuron/name/141009_Pair1DSGC`
   via `curl` and capture the JSON payload to
   `logs/steps/009_implementation/neuromorpho_metadata.json`. Expected: a JSON object including
   `neuron_id`, `archive: "Feller"`, `species: "mouse"`, `cell_type` list containing `ganglion`, and
   `reconstruction_software: "Neurolucida"`. This record populates the provenance fields in
   `details.json`. Satisfies REQ-4.

Milestone B — Download and validation:

3. **Download SWC.** Run
   `curl -fL -o assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc 'https://neuromorpho.org/dableFiles/feller/CNG%20version/141009_Pair1DSGC.CNG.swc'`.
   Expected output: a non-empty SWC file (> 10 KB). Fail hard if `curl` exits non-zero or the file
   is under 1 KB. Satisfies REQ-2.

4. **[CRITICAL] Validate SWC parse.** Create `code/validate_swc.py` that (a) reads the SWC
   line-by-line with the stdlib, skipping `#` comments, (b) parses each data row into a
   `SwcCompartment` frozen dataclass (id, type, x, y, z, radius, parent), (c) confirms exactly one
   root (`parent == -1`), connected tree (every non-root parent id exists), non-negative radii, at
   least one soma compartment (type 1), at least 100 dendrite compartments (types 3 or 4). Also
   attempt a secondary load with `neurom.load_morphology` if `neurom` is importable; log the result
   but do not fail if `neurom` is missing. Run:
   `uv run python -u -m tasks.t0005_download_dsgc_morphology.code.validate_swc assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc`.
   Expected: prints compartment count, branch count, total dendritic length, and `VALID` on stdout.
   Satisfies REQ-3.

Milestone C — Asset registration:

5. **Write asset metadata.** Create `assets/dataset/dsgc-baseline-morphology/details.json` (spec v2)
   with `dataset_id: "dsgc-baseline-morphology"`, `name`, `version: "1.0"`, `short_description`,
   `description_path: "description.md"`, `source_paper_id: "10.1016_j.neuron.2018.05.028"`
   (placeholder — the paper is not yet registered as an asset in this project, so the field is set
   to `null` and the DOI is captured in `description.md` as provenance),
   `url: https://neuromorpho.org/neuron_info.jsp?neuron_name=141009_Pair1DSGC`,
   `download_url: https://neuromorpho.org/dableFiles/feller/CNG%20version/141009_Pair1DSGC.CNG.swc`,
   `year: 2018`, `date_published: 2018-06-27`, `authors` (Morrie & Feller), `institutions` (UC
   Berkeley, US), `license: "CC-BY-4.0"`, `access_kind: "public"`, `size_description`,
   `files: ["files/141009_Pair1DSGC.CNG.swc"]`,
   `categories: ["direction-selectivity", "retinal-ganglion-cell"]`, `added_by_task`, `date_added`.
   Also create `description.md` with all seven mandatory sections (Metadata, Overview ≥80 words,
   Content & Annotation, Statistics, Usage Notes, Main Ideas ≥3 bullets, Summary). Satisfies
   REQ-4.

6. **Run dataset verificator.** Run
   `uv run python -u -m arf.scripts.verificators.verify_dataset_asset dsgc-baseline-morphology --task-id t0005_download_dsgc_morphology`.
   Expected: 0 errors, 0 or minimal warnings. Fix any reported issues before proceeding. Satisfies
   REQ-5.

## Remote Machines

None required. The task runs entirely on the local workstation using `curl` for the download and
Python's stdlib for SWC parsing.

## Assets Needed

* The morphology shortlist from `t0002_literature_survey_dsgc_compartmental_models` (dependency
  task, answer asset `how-does-dsgc-literature-...`). Already completed and read during Step 1.
* Public NeuroMorpho.org REST API (`https://neuromorpho.org/api/neuron/name/...`) for provenance
  metadata.
* Public NeuroMorpho.org file endpoint for the CNG-curated SWC.

No new pip dependencies need to be added to `pyproject.toml`; the validator uses only stdlib.

## Expected Assets

One dataset asset: `dsgc-baseline-morphology` (asset type `dataset`). Brief description: the Morrie
& Feller 2018 Feller-archive ON-OFF mouse DSGC (`141009_Pair1DSGC`), Neurolucida reconstruction,
distributed as CNG-curated SWC via NeuroMorpho.org neuron 102976. This matches `task.json`
`expected_assets: {"dataset": 1}`.

## Time Estimation

Research: already done (t0002). Step 1 (selection review): ~2 minutes. Step 2 (metadata fetch): ~1
minute. Step 3 (download): ~1 minute. Step 4 (validator script + run): ~10 minutes. Step 5
(details.json + description.md): ~15 minutes. Step 6 (verificator loop): ~5 minutes. Total
implementation ~35 minutes of wall-clock work.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| NeuroMorpho download endpoint returns 404 or times out | Low | Blocking Step 3 | Retry once; fall back to the NeuroMorpho web UI "Download" button and save manually; last resort is a different Feller-archive DSGC neuron (e.g., `141009_Pair2DSGC`) from the same paper. |
| SWC fails tree-integrity checks in Step 4 (dangling parent, negative radius) | Low | Blocking REQ-3 | Log the exact violating compartment ids, try the raw (non-CNG) SWC from the same record, or switch to a different Feller neuron and re-run Steps 2-4. |
| `neurom` not installed on this workstation | Medium | Nice-to-have secondary check skipped | Stdlib parser in `validate_swc.py` is the primary check; `neurom` is optional. Document skip in the step log. |
| Dataset spec v2 fields change interpretation (e.g., categories regex) | Low | Verificator warnings | Read category slug listing via `uv run python -u -m arf.scripts.aggregators.aggregate_categories --format ids` before writing `details.json` and only use listed slugs. |
| Folder name mismatch between task_description.md (`dsgc_baseline_morphology`) and v2 regex | Certain | Would fail PA-like verificator | Use `dsgc-baseline-morphology` and record the deviation in the step log and description.md. |

## Verification Criteria

* `assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc` exists, is > 10 KB, and
  begins with the standard SWC header. Check with `ls -l` and `head -5`.
* `uv run python -u -m tasks.t0005_download_dsgc_morphology.code.validate_swc assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc`
  exits 0 and prints `VALID` (confirms REQ-3).
* `uv run python -u -m arf.scripts.verificators.verify_dataset_asset dsgc-baseline-morphology --task-id t0005_download_dsgc_morphology`
  reports 0 errors (confirms REQ-4 and REQ-5).
* `assets/dataset/dsgc-baseline-morphology/details.json` contains `url` and `download_url` pointing
  to NeuroMorpho neuron `141009_Pair1DSGC`, and `description.md` cites DOI
  `10.1016/j.neuron.2018.05.028` (Morrie & Feller 2018) in the Metadata section (confirms REQ-4 and
  the task's own verification criterion "details.json links back to the source paper or NeuroMorpho
  record").
* Every `REQ-*` item from the Task Requirement Checklist is cited at least once in the step logs for
  steps 7 (planning) through 15 (reporting), proving full requirement coverage.
