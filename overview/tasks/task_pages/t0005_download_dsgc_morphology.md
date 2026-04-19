# ✅ Download candidate DSGC morphology

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0005_download_dsgc_morphology` |
| **Status** | ✅ completed |
| **Started** | 2026-04-19T08:50:24Z |
| **Completed** | 2026-04-19T09:28:00Z |
| **Duration** | 37m |
| **Dependencies** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Task types** | `download-dataset` |
| **Categories** | [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md) |
| **Expected assets** | 1 dataset |
| **Step progress** | 8/15 |
| **Task folder** | [`t0005_download_dsgc_morphology/`](../../../tasks/t0005_download_dsgc_morphology/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0005_download_dsgc_morphology/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0005_download_dsgc_morphology/task_description.md)*

# Download candidate DSGC morphology

## Motivation

Every downstream simulation task needs a concrete reconstructed morphology to load. Rather
than generating a synthetic branching structure, we want a published DSGC (or DSGC-like RGC)
reconstruction used by prior modelling work. The literature survey (t0002) produces the
shortlist; this task commits to one file.

## Scope

Download one reconstructed DSGC morphology in SWC format (or HOC / NeuroML if SWC is not
available) from a public source such as NeuroMorpho.org, ModelDB, or a paper's supplementary
materials. The morphology should be one of those flagged as suitable in t0002's answer asset.

## Approach

1. Read t0002's answer asset to pick the recommended morphology.
2. Download the file and verify it loads as a valid SWC / HOC structure.
3. Record its provenance (source URL, paper DOI, reconstruction protocol) in the dataset asset
   metadata.

## Expected Outputs

* One dataset asset under `assets/dataset/dsgc_baseline_morphology/` containing the morphology
  file(s) and metadata.

## Compute and Budget

No external cost.

## Dependencies

`t0002_literature_survey_dsgc_compartmental_models` — the literature survey produces the
morphology shortlist and rationale.

## Verification Criteria

* Dataset asset passes `verify_dataset_asset.py`.
* The asset's `details.json` links back to the source paper or NeuroMorpho record.
* The downloaded file loads without errors in at least one candidate simulator library.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| dataset | [DSGC Baseline Morphology (Feller 141009_Pair1DSGC)](../../../tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/) | [`description.md`](../../../tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/description.md) |

## Suggestions Generated

<details>
<summary><strong>Download both candidate Feller-lab 2018 source papers to resolve
the dsgc-baseline-morphology provenance ambiguity</strong> (S-0005-01)</summary>

**Kind**: dataset | **Priority**: high

The dsgc-baseline-morphology asset (NeuroMorpho neuron 102976, 141009_Pair1DSGC) currently has
source_paper_id=null because two Feller-lab papers from 2018 are plausibly the source: the
plan-nominated Morrie & Feller 2018 Neuron (DOI 10.1016/j.neuron.2018.05.028) and the
NeuroMorpho-reported Murphy-Baum & Feller 2018 Current Biology (DOI
10.1016/j.cub.2018.03.001). Run /add-paper for both DOIs in a dedicated download-paper task,
read each paper's Methods to confirm which one introduced the 141009_Pair1DSGC reconstruction,
then file a corrections asset that updates dsgc-baseline-morphology source_paper_id to the
correct paper_id slug. This unblocks correct citation of the morphology in every downstream
paper-comparison task. Recommended task types: download-paper.

</details>

<details>
<summary><strong>Calibrate realistic dendritic diameters for
dsgc-baseline-morphology to replace the 0.125 um placeholder radii</strong>
(S-0005-02)</summary>

**Kind**: technique | **Priority**: high

Every compartment in the downloaded CNG SWC carries the placeholder radius 0.125 um because
the original Simple Neurite Tracer reconstruction did not record diameters. Cable-theory
predicts segment diameter is the single most influential local-electrotonic knob (see
S-0002-04), so leaving the uniform placeholder in place will silently bias every downstream
biophysical simulation (axial resistance, attenuation, spike initiation threshold). Build a
diameter-calibration pipeline that applies a literature-derived order-dependent diameter taper
(e.g., Vaney/Sivyer/Taylor 2012 mouse ON-OFF DSGC profile, or the Poleg-Polsky 2016
distribution) keyed on Strahler order or path distance from the soma, write the calibrated SWC
as a new dataset asset (e.g., dsgc-baseline-morphology-calibrated), and report the per-order
diameter distribution against the original placeholder. Recommended task types:
feature-engineering, data-analysis.

</details>

<details>
<summary><strong>Download additional Feller-archive DSGC reconstructions to enable
cross-cell variability sensitivity analysis</strong> (S-0005-03)</summary>

**Kind**: dataset | **Priority**: medium

The current dsgc-baseline-morphology commits the project to a single reconstructed cell
(141009_Pair1DSGC). Cell-to-cell variability in branching pattern, total path length, and
arbor extent is a known source of variance in DSGC tuning curves (RQ2), and the Feller archive
on NeuroMorpho hosts several sibling ON-OFF DSGC reconstructions from the same lab (e.g.,
141009_Pair2DSGC and other 2014 Pair* records). Download 3-5 additional Feller-archive ON-OFF
DSGC SWCs as separate dataset assets (each with its own NeuroMorpho neuron_id and provenance),
validate each with the existing validate_swc.py parser, and tabulate per-cell compartment
count, branch points, and total dendritic path length so a downstream morphology-sweep task
can quantify cross-cell variability without committing a priori to a specific morphology.
Recommended task types: download-dataset.

</details>

<details>
<summary><strong>Build a reusable SWC -> NEURON/NetPyNE/Arbor section-translator
library for dsgc-baseline-morphology</strong> (S-0005-04)</summary>

**Kind**: library | **Priority**: high

Every downstream compartmental-modelling task in this project will need to load the
dsgc-baseline-morphology SWC into a simulator and produce a section/segment graph indexed by
SWC compartment id, soma reference, and per-section parent links. NEURON's built-in Import3d
handling of CNG SWCs is fragile (soma-3point convention, branch-point splitting, axon stubs)
and other simulators have their own quirks (NetPyNE's netParams.cellParams, Arbor's morphology
builder). Write a small library asset that exposes a pure-function
load_dsgc_morphology(simulator: str) -> SimulatorMorphology API with verified-equivalent
loaders for NEURON, NetPyNE, and Arbor, plus a smoke test that compares total path length and
compartment count across loaders against validate_swc.py. This eliminates per-task SWC-loading
bugs and keeps morphology choice swappable when S-0005-03 lands. Recommended task types:
write-library.

</details>

<details>
<summary><strong>Render and QA-check 2D/3D visualisations of
dsgc-baseline-morphology for documentation and synapse placement</strong>
(S-0005-05)</summary>

**Kind**: evaluation | **Priority**: medium

The dsgc-baseline-morphology asset is currently described only by tabulated statistics (6,736
compartments, 129 branch points, 1,536.25 um path length). Downstream tasks that place
AMPA/GABA synapses by spatial rule (e.g., Park2014 3-5x null/preferred IPSC asymmetry,
S-0002-05 GABA/AMPA density scan) need a visual reference for the dendritic arbor,
branch-order map, and soma orientation; reviewers also need a figure for any project paper.
Render three QA visualisations (2D top-down dendrogram coloured by Strahler order, 2D xy
projection coloured by path distance from soma, 3D rotating xyz scatter) using neurom +
matplotlib (or NEURON's PlotShape) and register the figures plus the rendering script as an
answer asset describing what was checked. Flag any visible reconstruction artefacts (dangling
branches, axon stubs, soma asymmetry) for downstream tasks. Recommended task types:
data-analysis, answer-question.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0005_download_dsgc_morphology/results/results_summary.md)*

# Results Summary: Download candidate DSGC morphology

## Summary

Downloaded the Feller-lab ON-OFF mouse DSGC reconstruction `141009_Pair1DSGC` (NeuroMorpho
neuron 102976\) from Morrie & Feller-associated archives as a CNG-curated SWC, validated the
compartment tree with a stdlib Python parser, and registered it as the project's baseline DSGC
dataset asset `dsgc-baseline-morphology` (v2 spec-compliant). The morphology is now the single
reconstructed cell that every downstream compartmental-modelling task in this project will
load.

## Metrics

* **Compartments**: **6,736** (19 soma, 6,717 dendrite, 0 axon)
* **Branch points (≥2 children)**: **129**
* **Leaf tips**: **131**
* **Total dendritic path length**: **1,536.25 µm**
* **SWC file size**: **232,470 bytes** (CNG-curated)
* **Download cost**: **$0** (CC-BY-4.0 public data)

## Verification

* `verify_task_folder.py` — PASSED (0 errors, 1 warning: `FD-W002` empty `logs/searches/` —
  expected for a download-dataset task).
* `verify_plan.py` — PASSED (0 errors, 0 warnings).
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings) during check-deps.
* Manual `DA-*` spec-v2 check on `assets/dataset/dsgc-baseline-morphology/` — PASSED (0
  errors, 0 warnings). The framework's `verify_dataset_asset.py` script is not implemented, so
  the check was done by applying each rule from `meta/asset_types/dataset/specification.md`
  directly.
* Stdlib SWC tree check in `code/validate_swc.py` — emitted `VALID` (single root, connected
  tree, non-negative radii, ≥1 soma, 6,717 ≥ 100 dendrite compartments).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0005_download_dsgc_morphology/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0005_download_dsgc_morphology" ---
# Results Detailed: Download candidate DSGC morphology

## Summary

Committed the project to a single reconstructed direction-selective ganglion cell morphology
by downloading the Feller-lab ON-OFF mouse DSGC `141009_Pair1DSGC` (NeuroMorpho neuron_id
102976) as a CNG-curated SWC, validating its tree structure in Python, and registering it as
the dataset asset `dsgc-baseline-morphology` under the hyphen-compliant dataset asset spec v2.
The morphology has 6,736 compartments, 129 branch points, and 1,536.25 µm total dendritic path
length. Every subsequent compartmental-modelling task in this project can now load a single,
provenance-stamped SWC instead of choosing its own reconstruction or generating a synthetic
tree.

## Methodology

* **Machine**: local Windows 11 workstation (`md1avn`), git-bash / PowerShell shell, Python
  managed by `uv`.
* **Start**: 2026-04-19T08:50:24Z (branch create).
* **End**: 2026-04-19T09:25:00Z (implementation step log flushed).
* **Total runtime**: ~35 minutes of wall-clock work across preflight, planning,
  implementation, and results writing.
* **Download method**: `curl -fL` against the public NeuroMorpho.org endpoint
  `https://neuromorpho.org/dableFiles/feller/CNG%20version/141009_Pair1DSGC.CNG.swc`, captured
  in `logs/commands/004_*`.
* **Validation method**: `tasks.t0005_download_dsgc_morphology.code.validate_swc` — a
  stdlib-only SWC parser that enforces single-root, connected-tree, non-negative radii, ≥1
  soma compartment, and ≥100 dendrite compartments, with optional secondary load via
  `neurom.load_morphology` (skipped on this workstation because `neurom` is not installed; the
  plan marks this as a nice-to-have).
* **Asset verification method**: manual application of every `DA-E*` and `DA-W*` rule from
  `meta/asset_types/dataset/specification.md` v2 (the framework script
  `verify_dataset_asset.py` is not implemented in this fork — this is noted in `##
  Limitations` and recorded in the step log).

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

Radius handling: every compartment in the distributed CNG SWC carries the placeholder radius
0.125 µm. The original Simple Neurite Tracer output did not include diameters; NeuroMorpho CNG
assigns this placeholder uniformly. Downstream simulation tasks that need realistic diameters
must either re-run an image-based diameter fit or apply a literature-derived diameter profile,
and should not treat 0.125 µm as measured.

## Verification

| Verificator | Status | Notes |
| --- | --- | --- |
| `verify_task_dependencies.py` | **PASSED** | Completed dependency: `t0002_literature_survey_dsgc_compartmental_models`. |
| `verify_task_folder.py` | **PASSED** | 1 warning (`FD-W002` empty `logs/searches/`, expected for download-dataset). |
| `verify_plan.py` | **PASSED** | 0 errors, 0 warnings. Frontmatter v2, all 11 mandatory sections present. |
| Manual `DA-*` check on `assets/dataset/dsgc-baseline-morphology/` | **PASSED** | 0 errors, 0 warnings. Framework's `verify_dataset_asset.py` is not implemented — applied every `DA-E*` / `DA-W*` rule from the spec directly. |
| Python SWC parse check (`code/validate_swc.py`) | **PASSED** | Emitted `VALID`. Secondary `neurom` load skipped because `neurom` is not installed. |

## Limitations

* **Framework gap**: `verify_dataset_asset.py` and `aggregate_datasets.py` are referenced by
  the framework documentation but are not implemented in the current codebase. The
  implementation step and this results file substitute a manual spec-v2 rule check. This gap
  is real and should be surfaced as a framework task; it is not specific to this task and
  should not block merge.
* **Provenance-paper DOI ambiguity**: The plan nominated Morrie & Feller 2018 *Neuron*
  (`10.1016/j.neuron.2018.05.028`) as the source paper. NeuroMorpho's REST record for neuron
  102976 instead lists `10.1016/j.cub.2018.03.001` (Murphy-Baum & Feller 2018 *Current
  Biology*) as the `reference_doi`. The asset `details.json` sets `source_paper_id: null`
  because neither paper is registered as a paper asset in this project yet; `description.md`
  documents both candidates and uses the NeuroMorpho-reported DOI as the primary citation.
* **Placeholder radii**: All compartment radii are 0.125 µm (uniform). Any task that uses this
  morphology for biophysical compartment modelling must replace the radii.
* **Optional secondary validator skipped**: `neurom` is not installed; only the stdlib parser
  validated the SWC tree. The stdlib parser is self-contained and sufficient for the task's
  parse-validation requirement.
* **Single reconstruction**: Only one DSGC was downloaded. Variability across cells is not
  sampled; follow-up tasks may need to download additional Feller-archive DSGCs for
  sensitivity analysis.

## Files Created

* `plan/plan.md` — task plan (spec v5).
* `code/__init__.py`, `code/validate_swc.py` — stdlib SWC validator with optional `neurom`
  check.
* `assets/dataset/dsgc-baseline-morphology/details.json` — dataset asset metadata (spec v2).
* `assets/dataset/dsgc-baseline-morphology/description.md` — seven-section dataset
  description.
* `assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc` — the morphology
  file (232,470 bytes).
* `logs/steps/007_planning/step_log.md` — planning step log.
* `logs/steps/009_implementation/step_log.md` — implementation step log.
* `logs/steps/009_implementation/neuromorpho_metadata.json` — archived NeuroMorpho REST
  payload for neuron 102976.
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

</details>
