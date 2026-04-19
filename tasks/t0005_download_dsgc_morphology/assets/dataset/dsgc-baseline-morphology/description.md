---
spec_version: "2"
dataset_id: "dsgc-baseline-morphology"
summarized_by_task: "t0005_download_dsgc_morphology"
date_summarized: "2026-04-19"
---
# DSGC Baseline Morphology (Feller 141009_Pair1DSGC)

## Metadata

* **Name**: DSGC Baseline Morphology (Feller 141009_Pair1DSGC)
* **Year**: 2018
* **Date deposited**: 2018-11-10 (NeuroMorpho.org upload: 2019-04-08)
* **Authors**: Benjamin L. Murphy-Baum, Marla B. Feller (University of California, Berkeley, US)
* **Source paper DOI**: `10.1016/j.cub.2018.03.001` (Murphy-Baum & Feller, *Current Biology* 28 (8):
  1217-1223.e2, 2018 — PMID: 29606419)
* **NeuroMorpho.org neuron ID**: 102976
* **NeuroMorpho.org neuron name**: `141009_Pair1DSGC`
* **Archive**: Feller (UC Berkeley)
* **Species / strain**: mouse, `Sema6+/-` (adult; day 25-120)
* **Cell type**: principal cell, ganglion, direction-selective (ON-OFF DSGC)
* **Brain region**: retina (whole-mount)
* **Reconstruction software**: Neurolucida; original format: Simple Neurite Tracer `.traces`
* **Stain**: Alexa Fluor 488 (filled during paired SAC-DSGC patch recording)
* **License**: CC-BY-4.0 (NeuroMorpho.org standard license)
* **Access**: public
* **Landing page**: <https://neuromorpho.org/neuron_info.jsp?neuron_name=141009_Pair1DSGC>
* **Direct SWC URL**:
  <https://neuromorpho.org/dableFiles/feller/CNG%20version/141009_Pair1DSGC.CNG.swc>
* **File**: `files/141009_Pair1DSGC.CNG.swc` (~227 KB)
* **Size**: 6,736 compartments (19 soma, 6,717 dendrite, 0 axon), 129 branch points, 131 leaves,
  ~1.54 mm total dendritic path length

**Provenance note on DOI.** The planning document references DOI `10.1016/j.neuron.2018.05.028` as
the likely source paper. The NeuroMorpho.org REST record for neuron 102976 instead reports
`reference_doi: ["10.1016/j.cub.2018.03.001"]` and `reference_pmid: ["29606419"]`, which corresponds
to Murphy-Baum & Feller, *Current Biology* 2018. This description records the DOI that
NeuroMorpho.org itself associates with the reconstruction; the full API payload is archived at
`logs/steps/009_implementation/neuromorpho_metadata.json`. `details.json` `source_paper_id` is
`null` because no paper asset has yet been registered in this project for either candidate.

**Folder-name deviation note.** `task_description.md` refers to this asset with the folder name
`dsgc_baseline_morphology` (underscored). Dataset-asset spec v2 forbids underscores in `dataset_id`
(regex `^[a-z0-9]+([.\-][a-z0-9]+)*$`), so the hyphenated form `dsgc-baseline-morphology` is the
only spec-compliant rendering and is used consistently in `details.json`, the filesystem path, and
the frontmatter above.

## Overview

This dataset is a single-cell digital reconstruction of a mouse direction-selective retinal ganglion
cell (DSGC), recorded and traced in the Feller lab at UC Berkeley. The recording was performed as
part of a paired starburst-amacrine-cell (SAC) / DSGC patch experiment on a whole-mount retina from
a `Sema6+/-` adult mouse; after the electrical recording the DSGC was filled with Alexa Fluor 488
via the patch pipette, imaged with confocal microscopy, and the dendritic arbor was traced in Simple
Neurite Tracer and then re-traced into Neurolucida format. NeuroMorpho.org's CNG (Computational
Neuroanatomy Group) pipeline post-processed the raw tracing into a standardized SWC tree that
guarantees a single connected rooted graph with non-negative radii, uniform type codes, and 3D
coordinates in micrometres.

The resulting file describes an ON-OFF DSGC's full dendritic arbor in 6,736 compartments organized
as a single tree rooted at the soma. It contains no axon compartments, which is typical of
morphologies collected from retinal whole-mount preparations where the axon leaves the imaging
field. For this project it serves as the baseline cell geometry onto which every downstream
compartmental-modelling task will load ion channels, synapses, and stimuli. Using the same geometry
across tasks lets us attribute performance differences to parameter and model choices rather than to
morphology variability.

## Content & Annotation

The SWC file follows the standard 7-column CNG format (compartment id, SWC type code, x, y, z,
radius, parent id) with `#` header comments preserved from L-Measure post-processing. Coordinates
are in micrometres and the tree has a single root compartment with `parent_id == -1`.

Annotations are minimal — the SWC standard does not support per-compartment labels beyond the type
code. In this file the type codes observed are:

| SWC type code | Meaning (CNG) | Count |
| --- | --- | --- |
| 1 | Soma | 19 |
| 3 | Basal dendrite | 6,717 |
| 2 | Axon | 0 |
| 4 | Apical dendrite | 0 |

All non-soma compartments are encoded as basal dendrites (type 3), which is NeuroMorpho's default
for retinal ganglion cells that do not exhibit a basal/apical distinction. Downstream modelling code
should therefore treat type-3 compartments as the full dendritic arbor rather than discriminating
basal vs apical. The soma is represented as a 19-point contour (not a single sphere), which is
common for Neurolucida exports; Hines-style compartmental simulators (NEURON, Arbor) collapse this
to a cylinder or sphere at load time.

No light-microscopic shrinkage correction was applied (`shrinkage_reported: "Not Reported"` in the
NeuroMorpho record), so absolute dendritic lengths carry a typical ~10-20% confocal under-estimation
bias. Diameters are not encoded reliably in the original Simple Neurite Tracer file
(`attributes: "No Diameter, 3D, Angles"` in the NeuroMorpho metadata), so all radii in the CNG SWC
are a default value of 0.125 µm and should not be used as biophysical inputs without
re-measurement. Branch angle and 3D topology, by contrast, are faithful to the original tracing.

## Statistics

| Metric | Value |
| --- | --- |
| Total compartments | 6,736 |
| Soma compartments (type 1) | 19 |
| Dendrite compartments (type 3) | 6,717 |
| Axon compartments (type 2) | 0 |
| Branch points (≥2 children) | 129 |
| Leaf points (0 children) | 131 |
| Total dendritic path length | 1,536.25 µm (sum of parent-child Euclidean distances, type 3 only) |
| File size on disk | 232,470 bytes (~227 KB) |
| NeuroMorpho-reported soma surface | 6.86 µm² |
| NeuroMorpho-reported total surface | 1,206.57 µm² |
| NeuroMorpho-reported total volume | 75.41 µm³ |

## Usage Notes

* **Loading.** The SWC is plain ASCII and can be loaded with any of: NEURON
  (`h.load_file("import3d.hoc")`
  + `Import3d_SWC_read`), Arbor (`arbor.load_swc_arbor`), `neurom` (`neurom.load_morphology`),
    `morphio`, or the stdlib parser in `tasks/t0005_download_dsgc_morphology/code/validate_swc.py`.
* **Soma representation.** The soma is a 19-point contour, not a single sphere. NEURON's
  `Import3d_SWC_read` will automatically reduce it; Arbor requires explicit handling via
  `arbor.segment_tree`. Do not assume one soma compartment at load time.
* **Radii are placeholders.** Every radius in the file is the default 0.125 µm because the original
  tracing (Simple Neurite Tracer) did not record diameters. Downstream tasks that depend on axial
  resistance or passive surface area **must** either remeasure diameters, apply a literature-derived
  taper model, or use morphology-agnostic spatial discretization.
* **No axon.** Any downstream task that needs spike initiation must add a synthetic axon or model
  spiking directly in the soma, since the reconstruction has no axon compartments.
* **Coordinate system.** The arbor is centred near the origin; there is no stereotaxic frame.
  Downstream orientation (preferred-direction alignment, ON/OFF lamination) must be specified
  explicitly in the task that uses this cell.
* **Validation.** Re-run the stdlib validator at
  `tasks/t0005_download_dsgc_morphology/code/validate_swc.py` on any copy of the file to confirm
  integrity. It checks: exactly one root, fully connected tree, non-negative radii, at least one
  soma compartment, and at least 100 dendritic compartments.

## Main Ideas

* **Single canonical morphology.** This is the only DSGC reconstruction the project commits to.
  Every downstream compartmental simulation (cable modelling, synaptic integration, direction
  tuning) should load this exact SWC so that cross-task comparisons are not confounded by morphology
  variability.
* **Topology is trustworthy; diameters are not.** The 3D branch points, leaf positions, and
  inter-branch distances are faithful to the Neurolucida tracing, but the CNG SWC carries a default
  0.125 µm radius everywhere. Any biophysical model that depends on diameter must supply its own
  taper rule or diameter distribution and document the choice.
* **ON-OFF type; no axon.** The reconstruction is explicitly tagged as a direction-selective
  ganglion cell in NeuroMorpho's `cell_type` field, recorded in a paired SAC-DSGC experiment (see
  `note: "Paired SAC-DSGC recording"`), so downstream SAC-DSGC synaptic tasks can reuse it directly.
  The absence of axon compartments means spike-initiation models must inject the axon manually.
* **Provenance is preserved in the asset.** The NeuroMorpho REST payload is archived at
  `tasks/t0005_download_dsgc_morphology/logs/steps/009_implementation/neuromorpho_metadata.json` and
  the source paper DOI (`10.1016/j.cub.2018.03.001`) is captured here; no information needs to be
  re-fetched from NeuroMorpho to use the asset.

## Summary

This asset registers a single CNG-curated SWC reconstruction of the Feller-lab mouse ON-OFF DSGC
`141009_Pair1DSGC` (NeuroMorpho.org neuron 102976) as the project's baseline morphology. The cell
was patched in a paired SAC-DSGC experiment on a whole-mount `Sema6+/-` adult mouse retina, filled
with Alexa Fluor 488, imaged confocally, traced in Simple Neurite Tracer, re-rendered in
Neurolucida, and then standardized by NeuroMorpho.org's CNG pipeline. The resulting tree has 6,736
compartments (19 soma + 6,717 dendrite), 129 branch points, 131 leaves, and ~1.54 mm of total
dendritic path length.

For this project the asset plays a single, narrow role: it fixes a known, curated geometry that
every downstream compartmental-modelling task can load without choosing a new cell. Because the
project's research questions target direction-selectivity mechanisms, synaptic integration, and
channel tuning — all of which depend on dendritic branching patterns — the topological fidelity
of this reconstruction matters more than its absolute length or diameter. The main documented
limitations (placeholder radii, no axon, no shrinkage correction, only one cell) are therefore
acceptable for the project's scope but must be remembered and surfaced in any diameter-dependent or
spike-initiation-dependent downstream task.

Compared to alternative reconstructions (Briggman et al. 2011 SBEM skeletons, ModelDB entries that
bundle morphology with specific biophysical parameters), the Feller CNG SWC has two advantages: it
is distributed as a pure morphology (no model-specific parameters baked in) and it is already
curated and immediately loadable by every major compartmental simulator. Its main disadvantage
versus SBEM data is the missing diameter information, which a later task can partially address with
a diameter-taper model.
