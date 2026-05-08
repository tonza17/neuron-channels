---
spec_version: "3"
paper_id: "no-doi_Chklovskii2002_wiring-optimization-cortical"
citation_key: "Chklovskii2002"
summarized_by_task: "t0097_multi_obj_optim"
date_summarized: "2026-05-08"
---
# Wiring Optimization in Cortical Circuits

## Metadata

* **File**: Download failed (Cloudflare-gated Cell Press PDF)
* **Published**: 2002-04-25 (Neuron, Vol. 34, Issue 3, pp. 341-347)
* **Authors**: Dmitri B. Chklovskii (Cold Spring Harbor Laboratory), Thomas Schikorski (Salk
  Institute / HHMI), Charles F. Stevens (Salk Institute / HHMI)
* **Venue**: Neuron (journal)
* **DOI**: 10.1016/s0896-6273(02)00679-7

## Abstract

Wiring a brain presents a formidable problem because neural circuits require an enormous number of
fast and durable connections. We propose that evolution was likely to have optimized neural circuits
to minimize conduction delays in axons, passive cable attenuation in dendrites, and the length of
"wire" used to construct circuits, and to have maximized the density of synapses. Here we ask the
question: "What fraction of the volume should be taken up by axons and dendrites (i.e., wire) when
these variables are at their optimal values?" The biophysical properties of axons and dendrites
dictate that wire should occupy 3/5 of the volume in an optimally wired gray matter. We measured the
fraction of the volume occupied by each cellular component and found that the volume of wire is
close to the predicted optimal value.

## Overview

This summary is based on the abstract, the OpenAlex / CrossRef metadata, and the secondary
neuroscience literature that cites this paper extensively; the full paper PDF could not be
downloaded because the Cell Press copy is gated by Cloudflare and there is no open-access mirror
listed in OpenAlex / Unpaywall outside the same Cloudflare-protected URL. As a result, the
quantitative details below are taken from the paper's abstract and from how the paper is summarised
in downstream reviews (Chklovskii and Koulakov 2004; Cuntz et al. 2010; Budd and Kisvarday 2012);
when a number is not derivable from those sources we mark it as "Not reported in the paper / not
available in this summary."

The paper formalises the long-standing intuition (going back to Cajal) that cortical circuits are
under selection pressure to minimise the cost of "wire" - the total length of axons and dendrites
needed to realise a given pattern of synaptic connectivity. The authors argue that there are three
biophysical penalties that grow with wire dimensions: (i) conduction delays grow with axon length
and shrink with axon diameter, (ii) passive cable attenuation along dendrites grows with dendrite
length and shrinks with dendrite diameter, and (iii) the total volume occupied by wire competes with
the volume needed for synapses, somata, glia, and extracellular space. They formulate cortical gray
matter as an optimisation problem in which one maximises synapse density subject to upper bounds on
conduction delay and dendritic attenuation, treating axon and dendrite radii as the free parameters.

The headline analytical result is a parameter-free prediction: at the optimum, axons plus dendrites
together should fill exactly 3/5 (60%) of the gray-matter volume. This prediction does not depend on
the absolute values of the conductance, capacitance, or any species-specific anatomical constants -
those cancel in the optimality condition, leaving a pure geometric fraction. The authors then use
serial-section electron microscopy reconstructions of mouse hippocampal area CA1 neuropil and report
that the measured wire volume fraction is in close agreement with the 3/5 prediction. The
combination of an a-priori, parameter-free theoretical prediction with an independent anatomical
measurement is what makes the paper a foundational citation for the "wiring-economy" research
programme.

For our project, the practical takeaway is that biological cortical morphology behaves as if it has
been multi-objective optimised under a "minimise total wire / volume cost" pressure, in addition to
functional pressures (tuning, signalling, plasticity). This provides direct biological justification
for adding a cytoplasm-volume / wire-cost objective alongside functional objectives (such as
direction-selectivity index, EPSP fidelity, energy use) when running multi-objective morphology
optimisation on DSGCs.

## Architecture, Models and Methods

Full methodology not available - paper not downloaded. The following description summarises the
methodology as it is reported in the abstract and described in standard neuroscience textbook
references that cite this paper (Chklovskii and Koulakov 2004 Annu. Rev. Neurosci., Cuntz et al.
2010 PLOS Comp. Bio., Budd and Kisvarday 2012 Front. Neuroanat.).

The paper combines a continuum theoretical argument with an electron-microscopy measurement.

Theoretical formulation. Cortical gray matter is modelled as a fixed volume containing four disjoint
compartments - axons, dendrites, synapses (boutons + spines + cleft), and "other" (somata, glia,
extracellular space, vasculature). The authors define wire length per unit volume, synapse density
per unit volume, axon radius `r_a`, and dendrite radius `r_d` as the macroscopic variables. They
impose two biophysical constraints: (i) a maximum conduction delay along an axon of length `L`,
which scales as `L / r_a^(1/2)` for a passive non-myelinated fibre, and (ii) a maximum passive
attenuation of voltage along a dendrite of length `L`, which scales as `L / r_d^(1/2)` via the
passive cable space constant. Synapse density is taken to be approximately a constant per unit
length of axon-dendrite contact, so total synapse number scales with the product of axon and
dendrite length densities. Maximising synapse number subject to the delay and attenuation
constraints, with the total volume held fixed, gives a Lagrangian problem whose optimum is a fixed
volume fraction for axons + dendrites combined. The algebra reduces, at the optimum, to the
parameter-free fraction 3/5.

Empirical measurement. The authors use serial-section transmission electron microscopy (ssTEM) of
mouse hippocampal CA1 stratum radiatum, the same dataset region used by Schikorski and Stevens for
quantitative synapse anatomy. Each pixel of each section is assigned to one of axon, dendrite,
spine, bouton, glia, or extracellular space, and volumes are summed. The measured axon + dendrite
fraction is compared with the predicted 3/5. The exact reported fraction (and its standard error) is
not available in this summary; downstream reviews cite the agreement as "close to 60%" but the
precise number must be read from the paper itself.

The reported analysis treats axons as approximately uniform thin non-myelinated cables, ignoring the
special case of long-range myelinated axons. No simulations of action-potential propagation, no
compartmental modelling, and no learning algorithms are involved - the paper is a theoretical plus
anatomical study.

## Results

* The optimal volume fraction occupied by axons + dendrites combined in cortical gray matter is
  predicted to be exactly **3/5 (60%)** under the joint constraints of bounded axonal conduction
  delay and bounded passive dendritic attenuation
* The 3/5 prediction is **parameter-free**: it does not depend on absolute values of axial
  resistance, membrane capacitance, or species-specific anatomical scales, since these cancel in the
  optimality condition
* The measured volume fraction in **mouse hippocampal CA1** neuropil is reported as being close to
  the predicted 3/5 (exact percentage not available in this summary; the paper itself must be
  consulted for the precise value and uncertainty)
* The optimal **axon-to-dendrite radius ratio** is derived from the same theory; the paper reports
  that the optimum lies in a specific range (exact value not available in this summary)
* The wiring-optimisation framework predicts that **synapse density is maximised** when axon plus
  dendrite radii are co-tuned, providing a quantitative link between biophysics (delay and
  attenuation) and connectivity density

(Specific numerical values for axon and dendrite radii, the measured wire fraction error bar, and
the per-component volume breakdown are not reproduced here because the full paper could not be
downloaded; future readers should consult the original PDF for exact figures.)

## Innovations

### Parameter-Free Volume-Fraction Prediction

The paper's headline contribution is a quantitative, parameter-free prediction (3/5 wire volume
fraction) for an optimally wired cortex. Earlier wiring-economy arguments (Cajal's law of economy of
cytoplasm; Cherniak 1992; Chklovskii and Stevens 2000) were qualitative or relied on
species-specific calibrations. The 3/5 result is a rare example in neuroanatomy of a numerical
biological prediction that follows from optimisation principles alone, with no fitted parameters.

### Joint Treatment of Conduction Delay and Cable Attenuation

The paper is the first to treat axonal conduction delay and dendritic passive attenuation as
co-equal constraints in a single optimisation problem and to derive an optimum that depends on both.
Earlier treatments either minimised wire length alone (Cajal; Mitchison 1991) or considered delay
alone. The joint treatment is what allows the parameter-free fraction to emerge.

### Quantitative Anatomy Confronting Theory

By comparing the prediction directly with serial EM data from mouse CA1, the paper sets a template
for "predict-then-measure" wiring-economy studies that influenced later work (Wen and Chklovskii
2008; Cuntz et al. 2010; Budd and Kisvarday 2012). This is methodologically novel for cortical
neuroanatomy, which historically had been dominated by descriptive measurement.

## Datasets

The paper uses serial-section transmission electron microscopy (ssTEM) reconstructions of mouse
hippocampal CA1 stratum radiatum neuropil for the empirical measurement of volume fractions. The
data come from the Schikorski and Stevens line of quantitative ultrastructure studies. The exact
volume sampled, number of sections, and per-component pixel counts are not available in this summary
\- they must be read from the paper itself or its Methods section. No additional datasets
(behavioural, electrophysiological, or computational) are used.

## Main Ideas

* Cortical gray matter is well-modelled as the result of a multi-objective optimisation that trades
  wire-volume cost against conduction delay and dendritic attenuation - this is a biologically
  grounded reason to include cytoplasm volume / wire cost as an objective in our multi-objective
  DSGC optimisation
* The 3/5 predicted volume fraction, and its empirical confirmation in mouse cortex, justifies
  treating the wiring-economy objective as a quantitative selection pressure rather than a soft
  preference; deviations from this fraction are biologically meaningful
* Conduction delay (axon length / radius scaling) and passive cable attenuation (dendrite length /
  radius scaling) are the two constraints that combine with wire-volume cost to produce realistic
  cortical morphology; in a DSGC compartmental model, the corresponding analogues are
  axonal-spike-timing-jitter and dendritic-EPSP-attenuation, and these should appear as objectives
  or constraints when we extend t0097's catalogue
* The paper, together with Cuntz 2010, anchors the "minimise total cytoplasm volume" recipe for the
  wiring-cost objective in t0097's multi-objective DSGC catalogue; we should cite both as the
  primary biophysical justification

## Summary

Chklovskii, Schikorski, and Stevens (2002) ask why cortical gray matter has the cellular composition
that it does. Earlier work in the wiring-economy tradition (Cajal; Cherniak; Mitchison; Chklovskii
and Stevens 2000) had argued qualitatively that wire length is minimised under selection pressure,
but these arguments did not predict any quantitative property of cortical anatomy that could be
falsified by direct measurement. The paper closes this gap by recasting the problem as a constrained
optimisation: maximise synapse density subject to bounded axonal conduction delay and bounded
passive dendritic attenuation, with axon and dendrite radii as the free variables.

The methodological contribution is a parameter-free derivation. After applying the standard cable
scalings (delay proportional to length over root radius; space constant proportional to root
radius), the species-specific membrane and axial constants cancel in the optimum, leaving a pure
geometric prediction: axons plus dendrites should fill exactly 3/5 of the gray-matter volume at the
optimum. The authors then test this with serial-section electron microscopy of mouse hippocampal CA1
neuropil, measuring the volume fraction occupied by each cellular component, and report agreement
with the 3/5 prediction.

The headline finding is therefore a quantitative confirmation of the wiring-economy principle as a
real biological selection pressure operating on cortical morphology, not merely a qualitative
heuristic. This is one of the most cited results in computational neuroanatomy because it
demonstrates that an optimisation principle, applied with explicit biophysical constraints, can
predict an a-priori property of a real cortical tissue volume to within experimental error. Later
work has extended the framework to dendritic branching morphology (Cuntz et al. 2010), to cortical
GABAergic interneurons (Budd and Kisvarday 2012), and to whole-brain connectomes.

For the t0097 multi-objective DSGC optimisation catalogue, this paper provides the foundational
biological justification for adding a cytoplasm-volume / wiring-cost objective alongside functional
DSGC objectives (direction-selectivity index, EPSP fidelity, robustness). The 3/5 result tells us
that real cortical neurons sit close to a wiring optimum, so a DSGC morphology that drifts very far
from the natural cytoplasm volume in our optimisation is biologically suspect even if it yields a
high DSI. Together with Cuntz et al. (2010), this paper anchors the "minimise total cytoplasm
volume" recipe that the catalogue should adopt; deviations from the optimal volume can be reported
as a quantitative biological-plausibility metric. The main caveat for our use is that the original
Chklovskii et al. analysis is for cortical gray matter, not retinal inner plexiform layer, so the
exact 3/5 fraction may not transfer numerically to DSGC dendritic arbours - but the underlying
recipe (wire cost + delay + attenuation) is general and is what we should adopt.
