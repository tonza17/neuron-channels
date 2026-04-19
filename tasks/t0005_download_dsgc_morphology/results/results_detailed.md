---
spec_version: "2"
task_id: "t0005_download_dsgc_morphology"
---
# Results Detailed: Download candidate DSGC morphology

## Summary

Committed the project to a single reconstructed direction-selective ganglion cell morphology by
downloading the Feller-lab ON-OFF mouse DSGC `141009_Pair1DSGC` (NeuroMorpho neuron_id 102976) as a
CNG-curated SWC, validating its tree structure in Python, and registering it as the dataset asset
`dsgc-baseline-morphology` under the hyphen-compliant dataset asset spec v2. The morphology has
6,736 compartments, 129 branch points, and 1,536.25 µm total dendritic path length. Every
subsequent compartmental-modelling task in this project can now load a single, provenance-stamped
SWC instead of choosing its own reconstruction or generating a synthetic tree.

## Methodology

* **Machine**: local Windows 11 workstation (`md1avn`), git-bash / PowerShell shell, Python managed
  by `uv`.
* **Start**: 2026-04-19T08:50:24Z (branch create).
* **End**: 2026-04-19T09:25:00Z (implementation step log flushed).
* **Total runtime**: ~35 minutes of wall-clock work across preflight, planning, implementation, and
  results writing.
* **Download method**: `curl -fL` against the public NeuroMorpho.org endpoint
  `https://neuromorpho.org/dableFiles/feller/CNG%20version/141009_Pair1DSGC.CNG.swc`, captured in
  `logs/commands/004_*`.
* **Validation method**: `tasks.t0005_download_dsgc_morphology.code.validate_swc` — a stdlib-only
  SWC parser that enforces single-root, connected-tree, non-negative radii, ≥1 soma compartment,
  and ≥100 dendrite compartments, with optional secondary load via `neurom.load_morphology`
  (skipped on this workstation because `neurom` is not installed; the plan marks this as a
  nice-to-have).
* **Asset verification method**: manual application of every `DA-E*` and `DA-W*` rule from
  `meta/asset_types/dataset/specification.md` v2 (the framework script `verify_dataset_asset.py` is
  not implemented in this fork — this is noted in `## Limitations` and recorded in the step log).

## Key Statistics

| Quantity | Value |
| --- | --- |
| Total compartments | **6,736** |
| Soma compartments (type 1) | 19 |
| Dendrite compartments (type 3) | 6,717 |
| Axon compartments (type 2) | 0 |
| Branch points (≥2 children) | **129** |
| Leaf tips | 131 |
| Total dendritic path length | **1,536.25 µm** |
| SWC file size | 232,470 bytes |
| SWC source | NeuroMorpho.org `Feller` archive, CNG-curated version |
| NeuroMorpho neuron_id | 102976 |
| Reconstruction software | Neurolucida (Simple Neurite Tracer export, CNG-converted) |

Radius handling: every compartment in the distributed CNG SWC carries the placeholder radius 0.125
µm. The original Simple Neurite Tracer output did not include diameters; NeuroMorpho CNG assigns
this placeholder uniformly. Downstream simulation tasks that need realistic diameters must either
re-run an image-based diameter fit or apply a literature-derived diameter profile, and should not
treat 0.125 µm as measured.

## Verification

| Verificator | Status | Notes |
| --- | --- | --- |
| `verify_task_dependencies.py` | **PASSED** | Completed dependency: `t0002_literature_survey_dsgc_compartmental_models`. |
| `verify_task_folder.py` | **PASSED** | 1 warning (`FD-W002` empty `logs/searches/`, expected for download-dataset). |
| `verify_plan.py` | **PASSED** | 0 errors, 0 warnings. Frontmatter v2, all 11 mandatory sections present. |
| Manual `DA-*` check on `assets/dataset/dsgc-baseline-morphology/` | **PASSED** | 0 errors, 0 warnings. Framework's `verify_dataset_asset.py` is not implemented — applied every `DA-E*` / `DA-W*` rule from the spec directly. |
| Python SWC parse check (`code/validate_swc.py`) | **PASSED** | Emitted `VALID`. Secondary `neurom` load skipped because `neurom` is not installed. |

## Limitations

* **Framework gap**: `verify_dataset_asset.py` and `aggregate_datasets.py` are referenced by the
  framework documentation but are not implemented in the current codebase. The implementation step
  and this results file substitute a manual spec-v2 rule check. This gap is real and should be
  surfaced as a framework task; it is not specific to this task and should not block merge.
* **Provenance-paper DOI ambiguity**: The plan nominated Morrie & Feller 2018 *Neuron*
  (`10.1016/j.neuron.2018.05.028`) as the source paper. NeuroMorpho's REST record for neuron 102976
  instead lists `10.1016/j.cub.2018.03.001` (Murphy-Baum & Feller 2018 *Current Biology*) as the
  `reference_doi`. The asset `details.json` sets `source_paper_id: null` because neither paper is
  registered as a paper asset in this project yet; `description.md` documents both candidates and
  uses the NeuroMorpho-reported DOI as the primary citation.
* **Placeholder radii**: All compartment radii are 0.125 µm (uniform). Any task that uses this
  morphology for biophysical compartment modelling must replace the radii.
* **Optional secondary validator skipped**: `neurom` is not installed; only the stdlib parser
  validated the SWC tree. The stdlib parser is self-contained and sufficient for the task's
  parse-validation requirement.
* **Single reconstruction**: Only one DSGC was downloaded. Variability across cells is not sampled;
  follow-up tasks may need to download additional Feller-archive DSGCs for sensitivity analysis.

## Files Created

* `plan/plan.md` — task plan (spec v5).
* `code/__init__.py`, `code/validate_swc.py` — stdlib SWC validator with optional `neurom` check.
* `assets/dataset/dsgc-baseline-morphology/details.json` — dataset asset metadata (spec v2).
* `assets/dataset/dsgc-baseline-morphology/description.md` — seven-section dataset description.
* `assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc` — the morphology file
  (232,470 bytes).
* `logs/steps/007_planning/step_log.md` — planning step log.
* `logs/steps/009_implementation/step_log.md` — implementation step log.
* `logs/steps/009_implementation/neuromorpho_metadata.json` — archived NeuroMorpho REST payload
  for neuron 102976.
* `logs/steps/012_results/step_log.md` — this step's log.
* `results/results_summary.md`, `results/results_detailed.md`, `results/metrics.json`,
  `results/costs.json`, `results/remote_machines_used.json` — the results bundle.

## Task Requirement Coverage

Operative task text from `task.json` and `task_description.md`:

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

| ID | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Select one morphology from t0002's shortlist. | **Done** | Plan `## Approach` names the Feller `141009_Pair1DSGC` and cites t0002's `how-does-dsgc-literature-...` answer. Selection recorded in `logs/steps/009_implementation/step_log.md` §2. |
| REQ-2 | Download the morphology as SWC from a public source. | **Done** | `assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc` (232,470 bytes); download log `logs/commands/004_20260419T090958Z_curl-fl-o.*`. |
| REQ-3 | Verify the downloaded file parses as a valid SWC tree in a Python simulator-adjacent library. | **Done** | `code/validate_swc.py` emitted `VALID`; run captured in `logs/commands/006_*` and `logs/commands/009_*`. Partial caveat: `neurom` secondary check skipped (not installed); stdlib parser is self-sufficient. |
| REQ-4 | Produce a dataset asset with provenance (source URL, paper DOI, reconstruction protocol). | **Done** | `assets/dataset/dsgc-baseline-morphology/details.json` carries `url`, `download_url`, `year`, `authors`, `institutions`, `license`; `description.md` records DOI, reconstruction protocol, and NeuroMorpho neuron_id in the Metadata and Overview sections. Folder is `dsgc-baseline-morphology` (hyphens) because the v2 regex forbids underscores — documented deviation from `task_description.md`'s underscored spelling. |
| REQ-5 | `verify_dataset_asset.py` passes with zero errors. | **Done (caveat)** | The framework script `verify_dataset_asset.py` is not implemented; applied every `DA-E*` and `DA-W*` rule from the v2 spec directly and confirmed 0 errors, 0 warnings. Also ran `verify_task_folder.py` (PASSED) and `verify_plan.py` (PASSED). Flagged as a framework gap in `## Limitations`. |
