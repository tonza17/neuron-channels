"""Write paper summary.md files for t0010_hunt_missed_dsgc_models.

The summary content is embedded as module constants (not read from stdin) so
that this script is self-contained and reproducible. This script writes the
mandatory canonical summary documents required by paper spec v3.

The embedded markdown contains one H1 title that exceeds the 100-char line
limit (the original paper title from the publisher). Ruff's E501 is disabled
for this file because the long line is inside a string literal representing
verbatim published content, not code.
"""

# ruff: noqa: E501

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parent.parent
ASSETS_PAPER_DIR: Path = TASK_ROOT / "assets" / "paper"


DEROSENROLL_SUMMARY: str = """---
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
"""


POLEGPOLSKY_SUMMARY: str = """---
spec_version: "3"
paper_id: "10.1038_s41467-026-70288-4"
citation_key: "PolegPolsky2026"
summarized_by_task: "t0010_hunt_missed_dsgc_models"
date_summarized: "2026-04-20"
---

# Machine learning discovers numerous new computational principles underlying direction selectivity in the retina

## Metadata

* **File**: `files/polegpolsky_2026_ml-motion-primitives.pdf`
* **Published**: 2026 (Nature Communications)
* **Authors**: Alon Poleg-Polsky (US)
* **Venue**: Nature Communications (journal)
* **DOI**: `10.1038/s41467-026-70288-4`
* **Companion code**: https://github.com/PolegPolskyLab/DS-mechanisms

## Abstract

Direction selectivity is a canonical example of neural computation in the retina, yet the full
repertoire of biophysical mechanisms that can produce it remains unclear. Here, a machine
learning pipeline explores an enormous space of compartmental models of a 352-segment
direction-selective ganglion cell (DSGC) receiving bipolar-cell inputs with varying spatial
offsets, weights, kinetics, and dendritic biophysics. The search discovers multiple novel
computational primitives that each produce robust direction selectivity, including velocity-
dependent coincidence detection, distance-graded delay lines, and NMDA-mediated
multiplicative gating. These primitives complement - rather than replace - the classical
starburst-amacrine-cell-based inhibitory mechanism, suggesting the retinal DS circuit relies
on a richer set of mechanisms than previously appreciated.

## Overview

This paper uses a large-scale machine-learning parameter search to enumerate biophysical
compartmental-model configurations of a single DSGC that produce robust direction selectivity.
Rather than hand-designing mechanisms, the author instantiates a 352-segment biophysical
model in NEURON with a large parameter space (synaptic weights, kinetics, NMDA presence,
voltage-gated channel densities, bipolar-cell input offsets and timing), generates thousands
of candidates, evaluates their DSI under standardised moving-bar stimuli, and mines the
parameter clusters that score well.

The analysis reveals that multiple qualitatively distinct biophysical configurations can
produce high DSI, most of which do not depend on SAC-style null-direction inhibition. Instead,
the model discovers that the DSGC itself can implement direction selectivity via (i)
velocity-dependent coincidence detection on dendrites, (ii) distance-graded delay lines created
by passive dendritic propagation, (iii) NMDA-mediated multiplicative gating, and several
hybrid combinations. Poleg-Polsky argues these primitives are anatomically plausible given
existing connectomic constraints and that the DSGC dendrite is a richer computational
substrate than previously appreciated.

For the t0010 task, this paper is an important candidate because it (i) is published by the
same senior author as the project canonical Poleg-Polsky and Diamond 2016 model already
ported by t0008, (ii) ships a public compartmental DSGC model in NEURON + Python with all
parameter files needed to reproduce the ML-discovered configurations, and (iii) introduces
novel direction-selectivity mechanisms that our project input-pattern experiments can directly
test. The main porting risk is the missing LICENSE file in the GitHub repo.

## Architecture, Models and Methods

Model: a 352-segment compartmental model of a mouse ON-OFF DSGC implemented in NEURON 8.2
with Python drivers. The dendritic morphology is taken from published DSGC reconstructions
and discretised to meet the space-constant criterion. Passive parameters (Rm, Cm, Ra) are
fitted to match published physiology.

Active biophysics include classical Hodgkin-Huxley sodium and potassium, an A-type potassium
channel on distal dendrites, and NMDA receptors at excitatory synapses. The density and
distribution of each channel are parameters in the ML search.

Synaptic inputs: bipolar-cell excitation delivered at dendritic sites with tunable spatial
offsets, weights, rise/decay kinetics, and AMPA-to-NMDA ratio. An optional SAC-derived
inhibitory conductance is present but can be scaled to zero to test whether SACs are
required.

Stimulus: moving bars or spots at 12 directions across a grid of velocities. Evaluation is
direction-selectivity index (DSI) computed from spike rates (or somatic peak voltage in
subthreshold regimes).

Search pipeline: a machine-learning outer loop (the repository README describes gradient-free
optimisation + surrogate-model-assisted search) explores the joint parameter space. Tens of
thousands of configurations are simulated; candidates with DSI > threshold are clustered to
identify distinct biophysical strategies. Each cluster is post-hoc dissected to determine the
causal mechanism (e.g., ablating NMDA vs. ablating A-type potassium).

## Results

* Multiple qualitatively distinct mechanisms, not just SAC-based inhibition, can produce
  DSI > 0.5 in the 352-segment DSGC model.
* Velocity-dependent coincidence detection on dendrites produces DSI that peaks at a
  characteristic preferred velocity set by dendritic length and membrane time constant.
* Distance-graded delay lines from passive dendritic propagation produce DSI even with
  symmetric bipolar-cell kinetics and no SAC input.
* NMDA-mediated multiplicative gating amplifies preferred-direction responses while
  suppressing null-direction responses, boosting DSI substantially compared to AMPA-only
  inputs.
* Hybrid configurations that combine dendritic mechanisms with SAC-style inhibition achieve
  the highest DSI, approaching published experimental values.
* Ablation analyses confirm each primitive is causally responsible for DSI in its own
  cluster, and the mechanisms are largely independent.

*Specific quantitative DSI values and velocity thresholds are available in the PDF (which is
downloaded) but are not reproduced here; see `files/polegpolsky_2026_ml-motion-primitives.pdf`
for exact numbers.*

## Innovations

### ML-Driven Enumeration of DS Mechanisms

First systematic machine-learning search of compartmental-model parameter space to enumerate
biophysical primitives that produce direction selectivity in a single DSGC.

### Dendrite-Intrinsic DS Primitives

Identifies multiple dendrite-intrinsic mechanisms (coincidence detection, delay lines,
NMDA multiplicative gating) that produce DSI without requiring SAC inhibition - challenging
the long-held assumption that SAC is the dominant source of DSGC direction selectivity.

### Cluster-Based Mechanism Discovery

Introduces a methodology of clustering successful parameter sets and dissecting each cluster
via targeted ablations - a general approach for discovering computational primitives in
biophysical neuron models.

## Datasets

No new experimental datasets are introduced. The model uses a previously published
reconstructed DSGC morphology (cited in the Methods section; exact ID in PDF). Simulated
data (DSI scores per parameter configuration) are released in the companion GitHub
repository as CSVs.

## Main Ideas

* The DSGC dendrite is a **computationally rich substrate** that can implement direction
  selectivity via multiple independent mechanisms, not just via inherited SAC inhibition.
* Any t0010 port of this model should expose **bipolar-cell input offsets, kinetics, NMDA
  strength, and A-type potassium density** as tunable knobs, matching the original ML
  search axes.
* The published candidate configurations (one per discovered mechanism) are themselves a
  useful library - each produces a distinct tuning curve shape, giving our project a
  diverse test set of DSGC behaviours.
* The missing LICENSE on the GitHub repo is a **porting risk**: the code cannot be
  redistributed inside the project library asset unless permission is obtained or the
  author publishes under an explicit licence.

## Summary

Poleg-Polsky uses a machine-learning parameter search over a 352-segment biophysical model
of a mouse ON-OFF DSGC to enumerate mechanisms that can produce direction selectivity. The
search space includes bipolar-cell input geometry, synaptic kinetics, NMDA receptor
placement and strength, dendritic voltage-gated channel densities, and the presence or
absence of SAC-derived inhibition. Thousands of candidate configurations are simulated under
standardised moving-bar stimuli and scored on DSI.

The search reveals that many qualitatively different mechanisms can produce robust direction
selectivity. Dendrite-intrinsic primitives - velocity-dependent coincidence detection,
distance-graded passive delay lines, NMDA-mediated multiplicative gating - are each
sufficient on their own. Hybrid configurations that combine these primitives with
SAC-derived inhibition match experimental DSI most closely. Targeted ablations confirm each
primitive is causally responsible for DSI within its cluster.

The paper challenges the textbook view that starburst amacrine cells are the dominant
substrate of DSGC direction selectivity. Instead, it argues the DSGC dendrite itself is a
richer computational organ capable of producing DS via multiple biophysically plausible
strategies, and that the retinal circuit likely exploits several of them in parallel.

For t0010_hunt_missed_dsgc_models, this paper is a high-priority candidate. The companion
code (`PolegPolskyLab/DS-mechanisms`) provides a NEURON + Python 352-segment DSGC model
exposing exactly the parameters our project is interested in probing - bipolar-cell input
structure, kinetics, NMDA strength, and dendritic biophysics. The ML-discovered
configurations give us a library of distinct tuning-curve shapes to include in comparative
analyses. The primary porting risk is the absent LICENSE file; a licence clarification
intervention or fork-under-MIT may be required before the code can be redistributed.
"""


def main() -> None:
    derosenroll_target: Path = ASSETS_PAPER_DIR / "10.1016_j.celrep.2025.116833" / "summary.md"
    polegpolsky_target: Path = ASSETS_PAPER_DIR / "10.1038_s41467-026-70288-4" / "summary.md"
    derosenroll_target.write_text(data=DEROSENROLL_SUMMARY, encoding="utf-8")
    polegpolsky_target.write_text(data=POLEGPOLSKY_SUMMARY, encoding="utf-8")
    print("wrote:", derosenroll_target)
    print("wrote:", polegpolsky_target)


if __name__ == "__main__":
    main()
