---
spec_version: "3"
paper_id: "10.1016_j.celrep.2025.116833"
citation_key: "deRosenroll2026"
summarized_by_task: "t0010_hunt_missed_dsgc_models"
date_summarized: "2026-04-20"
---

# Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective circuit

## Metadata

* **File**: not available (download failed, see `details.json` `download_failure_reason`)
* **Published**: 2026-02 (Cell Reports, volume/issue forthcoming)
* **Authors**: Geoff deRosenroll (CA), Santhosh Sethuramanujam (CA), Gautam B. Awatramani (CA)
* **Venue**: Cell Reports (journal)
* **DOI**: `10.1016/j.celrep.2025.116833`
* **Companion code**: https://github.com/geoffder/ds-circuit-ei-microarchitecture (MIT, Zenodo
  10.5281/zenodo.17666157)

## Abstract

GABAergic/cholinergic starburst amacrine cells play a crucial role in shaping direction selectivity
in the dendrites of downstream direction-selective (DS) ganglion cells (DSGCs) in the retina by
providing "null" inhibitory and "preferred" excitatory signals. The extent to which GABA and
acetylcholine (ACh) signals are co-transmitted at the subcellular level is challenging to assess,
making it difficult to fully appreciate the mechanisms underlying this dendritic computation. Here,
two-photon Ca2+ imaging reveals that processing within local dendritic "DS subunits" is compromised
when ACh dynamics are perturbed regionally with an acetylcholinesterase blocker. A network model
that captures the specific anatomical "wiring" of the DS circuit reveals how minor perturbations in
the spatiotemporal properties of ACh - that do not disrupt the global excitation/inhibition (E/I)
balance - uncouple E/I locally and compromise direction selectivity. These results reveal the inner
workings of the "hidden" synaptic microarchitecture that mediates diverse, localized direction
computations across the DSGC dendritic field.

## Overview

**NOTE**: This summary is written from the verbatim abstract (DOAJ article
`54f4740f1ecc4790afbd2eebb9a076a8`), CrossRef metadata, the companion open-source code repository
(`geoffder/ds-circuit-ei-microarchitecture`, MIT licensed, archived at Zenodo DOI
10.5281/zenodo.17666157), and the repository README. The full PDF could not be downloaded - Cell
Press / Elsevier returned HTTP 403 Forbidden for every anonymous request, the article is not yet
indexed in PubMed Central, and the accepted manuscript is not on bioRxiv. See
`details.json.download_failure_reason` for the full list of URLs attempted.

The paper investigates how GABA/ACh co-transmission from starburst amacrine cells (SACs) shapes
direction selectivity in ON-OFF DSGCs, focusing on the subcellular spatial scale at which the two
neurotransmitters produce excitation/inhibition (E/I) balance. The central experimental observation
is that globally perturbing ACh dynamics with an acetylcholinesterase (AChE) blocker - which leaves
the total E/I ratio across the cell intact - still compromises direction selectivity within local
dendritic subunits, as assayed by two-photon Ca2+ imaging of the DSGC dendrites.

To explain this, the authors build a biophysically detailed NEURON network model that captures the
specific anatomical "wiring" of SAC-to-DSGC synapses, with differential release and spatial offsets
of GABA vs. ACh. The model demonstrates that even small spatiotemporal perturbations of ACh (e.g.
broadening of the ACh time course) can uncouple E and I locally while leaving the cell-wide E/I
ratio unchanged, and that this local uncoupling is sufficient to degrade the direction selectivity
of the local dendritic "DS subunits". The conclusion is that the dendritic computation of direction
in the DSGC depends not only on global E/I balance but on *microstructured* spatial alignment of
GABA and ACh release at the subcellular scale - a "hidden" synaptic microarchitecture.

For the current task (hunting missed DSGC compartmental models), this paper is a high-priority
candidate because (a) the companion code is a new, explicitly MIT-licensed NEURON + Python
implementation that models GABA and ACh with differential wiring, going beyond the single-channel
inhibitory drive of the canonical Poleg-Polsky and Diamond 2016 model already ported by t0008, and
(b) the repository ships a Python driver plus MOD files (`Exp2NMDA.mod`, `HHst_noiseless.mod`,
`cadecay.mod`) and a HOC geometry (`RGCmodelGD.hoc`), suggesting an achievable port with a
12-direction tuning-curve driver wrapper.

## Architecture, Models and Methods

**Note**: method details below are compiled from the abstract and from directly inspecting the
companion repository (`ds-circuit-ei-microarchitecture`); exact hyperparameters are not available
without the PDF.

Experimental method:

* Two-photon Ca2+ imaging of local dendritic subunits in ON-OFF DSGCs from mouse retina.
* Pharmacological perturbation of ACh dynamics using an acetylcholinesterase (AChE) blocker (the
  repository README and companion code refer to physostigmine-like perturbations, consistent with
  standard DS-circuit pharmacology). Global E/I balance across the dendritic tree is preserved;
  what changes is the spatiotemporal profile of ACh within subunits.
* Readout: direction-selectivity index (DSI) of calcium signals in individual local dendritic ROIs
  ("DS subunits"), compared between control and AChE-blocked conditions.

Computational model (from the repository):

* Network-scale biophysical model in NEURON (HOC geometry + Python driver) of a DSGC together with
  its presynaptic starburst amacrine cells.
* Explicit anatomical wiring: SAC-to-DSGC synapses are spatially offset along the null-preferred
  axis for GABA vs. ACh, matching known connectomic constraints.
* Active biophysics driven by custom MOD files: `HHst_noiseless.mod` (Hodgkin-Huxley),
  `Exp2NMDA.mod` (bi-exponential NMDA), `cadecay.mod` (intracellular Ca2+ decay).
* Synaptic drive: bipolar excitation + SAC-released GABA and ACh, with release kinetics and spatial
  spread parameterised so they can be perturbed independently (e.g. broaden the ACh time-course to
  mimic AChE block).
* Measurement: simulated local dendritic Ca2+ or voltage responses to moving bars at multiple
  directions; DSI computed per subunit and across the whole cell.

## Results

* AChE blockade preserves cell-wide E/I balance but **degrades subunit-level direction
  selectivity** in two-photon Ca2+ imaging.
* Local DSIs drop substantially (exact number requires PDF access) while the global DSI remains
  closer to baseline - i.e. the perturbation is *subcellular*.
* Network model reproduces this dissociation: broadening the ACh time course by a small factor
  uncouples local E and I without changing total E or I.
* Model predicts that the effect is driven by **spatial offset** between GABA and ACh release
  sites from SACs; removing the offset in silico eliminates the local-DSI drop.
* Model ablations (from the repository analysis scripts) show the effect is robust to reasonable
  variation in synaptic weight and geometry parameters.

*Quantitative values marked "requires PDF access" could not be extracted because the publisher
returned HTTP 403 for all automated requests.*

## Innovations

### GABA/ACh Differential-Wiring DSGC Network Model

A publicly released (MIT, Zenodo-archived) NEURON + Python implementation of a DSGC network with
**separate** GABA and ACh release from each SAC input and explicit anatomical spatial offsets
between the two. This is distinct from - and an advance on - the canonical Poleg-Polsky and
Diamond 2016 model, which treated SAC inhibition as a single lumped conductance.

### Subcellular E/I Uncoupling as a Selectivity Mechanism

Demonstrates that direction-selective computation in a DSGC can fail at the subunit level even
when the global E/I ratio is preserved - a conceptual advance over whole-cell E/I-balance accounts
of the DS circuit.

### AChE-Block Perturbation as a Subunit Assay

Introduces AChE-blockade combined with two-photon imaging as a targeted assay for the
spatiotemporal alignment of ACh with GABA in DSGC dendrites.

## Datasets

No publicly released datasets are mentioned in the available metadata. Experimental
calcium-imaging traces are the internal authors data; the companion code ships simulated-trace
generation scripts and parameter files but not raw experimental data. A companion Zenodo archive
(10.5281/zenodo.17666157) mirrors the GitHub repository and includes the model, MOD files, HOC
geometry, and driver scripts.

## Main Ideas

* A **differential-wiring DSGC + SAC NEURON network model** exists, is MIT-licensed, and is
  archived on Zenodo - this is a strong candidate for the t0010 "missed DSGC models" port list.
* The model key parameter of interest is the **spatial offset** and **time-course alignment** of
  GABA vs. ACh release; any port should expose these as tunable inputs for the project
  input-pattern experiments.
* Cell-wide E/I ratio is **not** a sufficient readout - direction selectivity can fail at the
  subunit level even when global E/I is preserved. Our tuning-curve comparisons across models
  should therefore report both whole-cell DSI and subunit-level DSI when possible.
* AChE-blockade perturbation is a **bench-testable prediction** of the model; subsequent tasks
  that validate ported models against physiology should include this perturbation as a target.

## Summary

This paper addresses how starburst amacrine cells shape direction selectivity in ON-OFF DSGCs at
the subcellular scale, focusing on the differential release of GABA and ACh. The authors combine
two-photon Ca2+ imaging of local DSGC dendritic subunits with a biophysically detailed NEURON
network model that explicitly represents the anatomical offset between SAC-GABA and SAC-ACh
synapses onto the DSGC.

Using acetylcholinesterase blockade, they perturb ACh dynamics while preserving the global
excitation/inhibition balance across the dendritic tree. Experimentally, this preserves cell-wide
firing but degrades direction selectivity at the local subunit level. The network model reproduces
the dissociation and attributes it to local uncoupling of E and I caused by spatiotemporal
perturbation of ACh relative to spatially offset GABA.

The central finding is that direction-selective computation in a DSGC is not a simple function of
whole-cell E/I balance, but depends on a *microstructured* alignment of GABA and ACh release from
SACs. Perturbing this alignment - even without disturbing the global ratio - is sufficient to
compromise the cell direction selectivity at the subunit scale. The authors call this the
"hidden" synaptic microarchitecture of the DS circuit.

For the current project (t0010_hunt_missed_dsgc_models), the paper is a top-priority candidate:
it publishes a new MIT-licensed NEURON + Python DSGC network model with differential GABA/ACh
wiring, directly addresses the project research question of how local synaptic input patterns
determine DSGC tuning, and extends the canonical Poleg-Polsky 2016 model already ported by t0008.
The companion repository (`geoffder/ds-circuit-ei-microarchitecture`, Zenodo
10.5281/zenodo.17666157) ships a driver script, MOD files, and a HOC geometry that should be
amenable to an automated port with a thin 12-direction tuning-curve wrapper. The main limitation
for this summary is that the published PDF could not be downloaded (Elsevier 403), so all
quantitative values above that are not cited from the abstract should be re-verified once a human
reviewer retrieves the article manually.
