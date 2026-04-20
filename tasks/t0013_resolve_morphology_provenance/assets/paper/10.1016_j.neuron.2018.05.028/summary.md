---
spec_version: "3"
paper_id: "10.1016_j.neuron.2018.05.028"
citation_key: "Li2018"
summarized_by_task: "t0013_resolve_morphology_provenance"
date_summarized: "2026-04-20"
---

# A Viral Receptor Complementation Strategy to Overcome CAV-2 Tropism for Efficient Retrograde Targeting of Neurons

## Metadata

* **File**: Download failed — paywalled Neuron paper; see `details.json` `download_failure_reason`.
* **Published**: 2018-06-06
* **Authors**: Shu-Jing Li 🇺🇸, Alexander Vaughan 🇺🇸, James Fitzhugh Sturgill 🇺🇸,
  Adam Kepecs 🇺🇸
* **Venue**: Neuron, Vol. 98, Issue 5, pp. 905-917.e5
* **DOI**: `10.1016/j.neuron.2018.05.028`

## Abstract

Retrogradely transported neurotropic viruses enable genetic access to neurons based on their
long-range projections and have become indispensable tools for linking neural connectivity with
function. A major limitation of viral techniques is that they rely on cell-type-specific molecules
for uptake and transport. Consequently, viruses fail to infect variable subsets of neurons depending
on the complement of surface receptors expressed (viral tropism). We report a receptor
complementation strategy to overcome this by potentiating neurons for the infection of the virus of
interest-in this case, canine adenovirus type-2 (CAV-2). We designed AAV vectors for expressing the
coxsackievirus and adenovirus receptor (CAR) throughout candidate projection neurons. CAR expression
greatly increased retrograde-labeling rates, which we demonstrate for several long-range
projections, including some resistant to other retrograde-labeling techniques. Our results
demonstrate a receptor complementation strategy to abrogate endogenous viral tropism and thereby
facilitate efficient retrograde targeting for functional analysis of neural circuits.

## Overview

This summary is based on the abstract and publicly available information only; the full paper could
not be downloaded. The DOI `10.1016/j.neuron.2018.05.028` is paywalled on ScienceDirect and
`cell.com`, and the paper (PMID 29879392) has no open-access copy in PubMed Central, Europe PMC, or
bioRxiv. Metadata was collected from the CrossRef and PubMed records, the Cold Spring Harbor
Laboratory press release, ScienceDaily, EurekAlert, and the Kepecs Lab publications page.

The paper is a neural-circuit methods paper from the Kepecs laboratory at Cold Spring Harbor
Laboratory. It tackles a well-known limitation of retrograde viral tracing: canine adenovirus
type-2 (CAV-2) is widely used for axon-terminal uptake but infects only neurons that express its
natural receptor, the coxsackievirus and adenovirus receptor (CAR). Neurons lacking CAR are
systematically missed, distorting reconstructed circuits. The authors propose forcing CAR
expression in candidate projection neurons with a conventional AAV vector, so that CAR-negative
neurons become permissive to CAV-2 entry. They demonstrate the approach in rats and mice for
multiple long-range projections; the CSHL press release highlights the basolateral
amygdala-to-medial prefrontal cortex projection as a prominent example of a pathway recovered by
the method.

**This paper is not about retinal direction selectivity, starburst amacrine cells (SACs), or
direction-selective ganglion cells (DSGCs).** It does not describe paired SAC-DSGC recordings,
biocytin-filled morphological reconstructions, Neurolucida tracing, or NeuroMorpho deposition, and
it is therefore not the source paper for the `141009_Pair1DSGC` DSGC morphology used by the
`dsgc-baseline-morphology` asset. This is almost certainly a task-input error: the orchestrator
described this DOI as "Morrie & Feller 2018 Neuron," but CrossRef and PubMed confirm the DOI
belongs to Li et al. 2018 on CAV-2 retrograde tracing. The Morrie & Feller "A Dense Starburst
Plexus Is Critical for Generating Direction Selectivity" paper is actually in *Current Biology*
(DOI `10.1016/j.cub.2018.03.001`, PMID 29606419), which is also the second candidate DOI listed in
the task description.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. The abstract and secondary sources identify
the following methodological elements:

* **Species**: rats and mice (CSHL press release; abstract states "neurons" without species, but
  corroborating coverage from ScienceDaily and EurekAlert confirms both rats and mice).
* **Brain regions / projections**: multiple long-range projections, with the press release
  explicitly naming the basolateral amygdala to medial prefrontal cortex projection as a flagship
  test case. Additional projections resistant to standard retrograde labeling are also evaluated
  per the abstract.
* **Key reagents**:
  * Canine adenovirus type-2 (CAV-2) as the retrograde virus of interest.
  * Custom AAV vectors expressing the coxsackievirus and adenovirus receptor (CAR) in candidate
    projection neurons to complement the missing CAR receptor.
  * Addgene-deposited plasmids for the CAR-expressing AAV constructs (Addgene browse page
    catalogues the deposits from this paper).
* **Experimental design**: pair CAV-2 injection at the projection target with AAV-CAR at the
  projection source, then quantify retrograde labeling density in CAR-complemented animals versus
  CAV-2-only controls.
* **Quantification**: retrograde-labeling rates are compared across conditions and projections;
  the abstract states CAR expression "greatly increased retrograde-labeling rates," but the
  specific labeling efficiency values, cell counts, titers, injection volumes, and microscopy
  parameters are not reported in the abstract or public summaries and cannot be quoted here
  without the full paper.
* **Not present**: the paper does not describe retinal preparations, whole-cell patch-clamp
  recordings from retinal neurons, paired SAC-DSGC recordings, biocytin intracellular fills,
  Neurolucida dendrite tracing, or NeuroMorpho deposition. It does not mention recording dates
  such as `141009` or October 9 2014, nor the `Pair1DSGC` cell identifier, nor the Sema6A knockout
  mouse line used in DSGC plexus-density studies.

## Results

Results not available — paper not downloaded. The abstract reports only qualitative outcomes
("greatly increased retrograde-labeling rates," "some resistant to other retrograde-labeling
techniques"). The following bullets record what is and is not reported in the accessible materials:

* **Retrograde labeling efficiency**: CAR complementation "greatly increased" CAV-2 retrograde
  labeling, per the abstract. Specific fold-change values, absolute neuron counts, and statistical
  comparisons are not reported in the abstract.
* **Projections tested**: multiple long-range projections were evaluated, with the
  basolateral-amygdala-to-medial-prefrontal-cortex pathway as a named example (CSHL press
  release). Exact projection-by-projection labeling efficiencies are not reported in accessible
  materials.
* **Failure-mode recovery**: projections "resistant to other retrograde-labeling techniques" were
  successfully labeled (abstract); the identity and number of these projections are not reported
  in accessible materials.
* **Species cross-validation**: the method is reported to work in both rats and mice (CSHL press
  release); per-species efficiency numbers are not reported in accessible materials.
* **Retinal / DSGC results**: none — the paper does not include any retinal work. No F1 scores,
  tuning indices, direction-selectivity indices, SAC dendrite lengths, or DSGC reconstructions
  are reported.

## Innovations

### Receptor-Complementation Paradigm for Viral Tracing

The paper's central novelty is framing viral tropism as an engineerable property: rather than
selecting a virus whose natural receptor matches the target cell, the authors install the virus's
receptor in the target cell via an AAV vector. The Kepecs-lab quote from the CSHL press release —
"It's a little like we're going around changing the locks on all the doors. They're still locked,
but now we have all the keys" — captures the conceptual shift.

### CAR-AAV Vector Toolkit for CAV-2 Retrograde Tracing

A practical contribution is a set of AAV constructs for expressing the coxsackievirus and
adenovirus receptor (CAR) that are deposited on Addgene (see Addgene browse article 28193439).
These reagents are what made CAV-2 retrograde tracing tractable in CAR-negative projections after
2018.

### Rescue of Circuits Lost to Conventional Tracing

The demonstration that CAR complementation recovers projections previously resistant to
retrograde labeling is an empirical innovation: it converts a categorical failure (virus does not
infect neuron type X) into a quantitative gain (labeling rates are recoverable with
pre-treatment).

## Datasets

This paper reports primary experimental data (viral labeling in rat and mouse brains). It does not
use any public neuronal morphology repository such as NeuroMorpho.Org, the Allen Brain Atlas
cell-type database, or DANDI. No public dataset is deposited with the paper according to the
materials consulted; the AAV-CAR plasmids are distributed through Addgene rather than as a
dataset.

Not reported in the accessible materials: injection volumes, AAV and CAV-2 titers, number of
animals per projection, or per-projection labeling counts. These would be in the STAR Methods and
figure legends of the full paper.

## Main Ideas

* **This DOI is not the source paper for the DSGC `141009_Pair1DSGC` morphology.** The Li et al.
  paper is a viral-tracing methods paper about brain projection neurons; it contains no retinal
  work, no paired SAC-DSGC recordings, and no NeuroMorpho deposition. The task should record this
  as strong evidence that Morrie & Feller 2018 *Neuron* (as the orchestrator labels this DOI)
  does not exist — the correct Morrie & Feller paper is DOI `10.1016/j.cub.2018.03.001`
  (*Current Biology*).
* **Task-input sanity check**: before adding a paper asset, verify that the CrossRef `title`
  returned for the DOI matches the orchestrator's declared paper title. A mismatch indicates a
  transcription error in the task setup that must be surfaced rather than silently corrected.
* **Morphology provenance resolution path**: since this DOI is unrelated to DSGC morphology, the
  task's `dsgc-baseline-morphology` correction should evaluate only the Murphy-Baum & Feller 2018
  *Current Biology* paper (`10.1016/j.cub.2018.03.001`) — which is in fact the Morrie & Feller
  Dense Starburst Plexus paper — against NeuroMorpho's metadata attribution. If NeuroMorpho
  attributes neuron 102976 to Murphy-Baum & Feller, then the conflict is between NeuroMorpho's
  attribution and Morrie & Feller's Methods; if NeuroMorpho attributes to Morrie & Feller, then
  the apparent "two-paper" conflict collapses into a single candidate.
* **CAV-2 / CAR toolkit is irrelevant to this project**: the project studies single-RGC
  electrophysiology and cable-theoretic modelling; retrograde viral tracing of brain projections
  is out of scope and does not inform the direction-selectivity modelling work.

## Summary

Li, Vaughan, Sturgill, and Kepecs (2018) report a receptor-complementation strategy that enables
canine adenovirus type-2 (CAV-2) to retrogradely infect neurons that lack its natural receptor, the
coxsackievirus and adenovirus receptor (CAR). Their motivating question is methodological: how can
neuroscientists access all neurons projecting to a target region when the standard retrograde virus
misses CAR-negative cell types? The scope is brain-wide retrograde tracing in rodents, with the
basolateral-amygdala-to-medial-prefrontal-cortex projection named as a worked example.

The method pairs an AAV vector that delivers CAR transgene expression to candidate source regions
with a subsequent CAV-2 injection at the projection target. Previously CAR-negative neurons become
permissive to CAV-2 entry, and the virus is transported retrogradely to the source where it can
drive Cre, fluorophores, or other payloads. The team tested the approach in both rats and mice
across several long-range pathways, including projections that had previously failed to label with
conventional retrograde techniques. AAV-CAR plasmids were deposited on Addgene for community use.

The headline finding, as reported in the abstract, is that CAR complementation "greatly increased
retrograde-labeling rates" and recovered projections "resistant to other retrograde-labeling
techniques." Specific fold-change numbers, per-projection labeling efficiencies, cell counts, and
titers cannot be quoted here because the full paper could not be downloaded from the worktree.
Secondary sources (CSHL press release, ScienceDaily, EurekAlert) corroborate the qualitative claim
but do not provide quantitative results.

For this project, the paper's practical relevance is approximately zero. The DSGC morphology
provenance task requires paired SAC-DSGC recordings, biocytin fills, and Neurolucida
reconstructions deposited on NeuroMorpho — none of which appear in this paper. The key takeaway is
a metadata-integrity finding: the orchestrator's task input pairs a paper title ("Morrie & Feller
2018 *Neuron*, A Dense Starburst Plexus Is Critical...") with a DOI that does not resolve to that
title. The correct Morrie & Feller paper is `10.1016/j.cub.2018.03.001` (*Current Biology*), which
is separately listed as the "Murphy-Baum & Feller 2018" candidate in the task description — so the
two supposed candidate papers likely collapse to one paper mis-labelled twice. The provenance
resolution should therefore focus on whether NeuroMorpho's attribution matches the Morrie & Feller
*Current Biology* Methods, not on adjudicating between two distinct Feller-lab 2018 papers.
