---
spec_version: "3"
paper_id: "10.1038_nature13240"
citation_key: "Kim2014"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Space-time wiring specificity supports direction selectivity in the retina

## Metadata

* **File**: PDF not downloaded; see `intervention/Kim2014_paywalled.md`. Summary built from PMC HTML
  full text (PMC4074887, NIHMS574498) and the Nature landing page.
* **Published**: 2014 (Nature 509:331-336, online 4 May 2014)
* **Authors**: Jinseop S. Kim 🇺🇸, Matthew J. Greene 🇺🇸, Aleksandar Zlateski 🇺🇸, Kisuk Lee 🇺🇸, Mark
  Richardson 🇺🇸, Srinivas C. Turaga 🇺🇸, Michael Purcaro 🇺🇸, Matthew Balkam 🇺🇸, Amy Robinson 🇺🇸,
  Bardia F. Behabadi 🇺🇸, Michael Campos 🇺🇸, Winfried Denk 🇩🇪, the EyeWirers, H. Sebastian Seung 🇺🇸
* **Venue**: *Nature* (Seung lab at MIT / Princeton, EyeWire citizen-science community, Denk at Max
  Planck)
* **DOI**: `10.1038/nature13240`

## Abstract

How does the mammalian retina detect motion? This classic problem in visual neuroscience has
remained unsolved for 50 years. In search of clues, we reconstructed Off-type starburst amacrine
cells (SACs) and bipolar cells (BCs) in serial electron microscopic images with help from EyeWire,
an online community of "citizen neuroscientists." Based on quantitative analyses of contact area and
branch depth in the retina, we found evidence that one BC type prefers to wire with a SAC dendrite
near the SAC soma, while another BC type prefers to wire far from the soma. The near type is known
to lag the far type in time of visual response. A mathematical model shows how such "space-time
wiring specificity" could endow SAC dendrites with receptive fields that are oriented in space-time
and therefore respond selectively to stimuli that move in the outward direction from the soma.

## Overview

Kim et al. attack the half-century-old question of where retinal direction selectivity (DS) arises.
Prior work had converged on the starburst amacrine cell (SAC): each SAC dendrite has its own
preferred direction (outward from soma to tip) that is intrinsic and survives inhibitory blockade,
meaning the SAC inherits DS from its excitatory bipolar cell (BC) inputs which are themselves
non-DS. The paper proposes and tests a purely anatomical mechanism. If the SAC dendrite is wired so
that proximal (near-soma) positions receive input from BC types with slower visual responses, and
distal positions receive input from BC types with faster responses, then outward motion will produce
synchronous arrival of excitation along the dendrite (large depolarisation), while inward motion
will produce asynchronous arrival (small depolarisation). This "space-time wiring specificity" uses
connectivity geometry, not dendritic biophysics, to build an oriented spatiotemporal receptive
field.

The authors test the hypothesis by densely reconstructing Off BCs and Off SACs from the e2198
mouse-retina serial block-face EM (SBEM) dataset originally acquired by Briggman, Helmstaedter &
Denk (2011). Reconstruction uses a hybrid of a deep-convolutional-network AI (for voxel
oversegmentation into supervoxels) plus manual agglomeration by paid lab workers and the EyeWire
crowd of volunteer "citizen neuroscientists." The resulting connectome is analysed by contact area
between every BC-SAC pair, binned by BC type and by tangential distance from the SAC soma, yielding
the predicted proximal-to-distal BC-type gradient. A linear-nonlinear model with two
space-time-separable subunits (sustained BC2 near, transient BC3a far) reproduces DS and subsumes
both the Reichardt and Barlow-Levick motion detectors as limiting cases.

**Borderline-flag for the t0027 survey on morphology shapes DS via computational modelling**: this
paper is the EM-anatomy + behavioural-model study that supplies the wiring constraint downstream
compartmental models consume as input. It is not itself a compartmental morphology-sweep paper. The
"model" here is a continuous linear-nonlinear space-time filter that treats the dendrite as
isopotential, not a multi-compartment cable simulation. Morphology in this paper means (a) SAC
dendritic stratification depth as a function of distance from soma (the "dendritic tilt" through the
IPL) and (b) the BC-type-specific contact pattern onto SAC dendrites. Later compartmental DSGC/SAC
models (e.g., Poleg-Polsky and Diamond line of work) rely on exactly this connectome plus
stratification substrate for their inputs.

## Architecture, Models and Methods

**Dataset.** The e2198 SBEM volume of mouse retina (covering INL through GCL and large enough to
encompass entire SAC dendrites, ~150 micrometre radius) originally described in Briggman,
Helmstaedter & Denk (Nature 2011). Voxel resolution is coarse relative to synaptic vesicles; the
stain does not mark presynaptic densities, so the analysis uses BC-SAC membrane **contact area** as
a proxy for connectivity rather than identified synapses.

**Reconstruction pipeline.** (1) An AI based on a deep convolutional network (successor of Turaga et
al., Neural Comput. 2010) oversegments the volume into supervoxels. (2) Human agglomerators (paid
lab workers and EyeWire volunteers) colour supervoxels belonging to the same neurite through the
EyeWire gamified web interface, working in 256-cubed-voxel cubes each seeded with a partial neuron.
(3) Consensus across typically 5-10 players per cube is computed by voxel-level voting. Accuracy is
quantified via precision/recall against gold-standard reconstructions; consensus substantially
exceeds any individual player, and the best players reach expert accuracy after hundreds of cubes
(tens of hours of practice).

**Cell identification.** Off SACs are detected by (a) INL soma, (b) narrow IPL stratification at
~32% depth (INL/GCL = 0/100%), (c) characteristic radial starburst. Off BCs are clustered into five
types (BC1, BC2, BC3a, BC3b, BC4) in a hierarchical procedure that uses IPL-stratification profile
percentiles (75th, 25th, 10th), stratification width, and axonal volume (Extended Data Fig. 5). Type
assignments are validated by cell-mosaic regularity (Extended Data Fig. 6) and density comparisons
with Waessle et al. (2009).

**Contact-area analysis.** For every BC-SAC pair, all shared-membrane voxels are summed. The matrix
is sorted by BC type and then, within each type, averaged across pairs binned by tangential distance
between the BC axon and the SAC soma. Absolute contact areas are normalised by the SAC surface area
at that distance (Extended Data Fig. 3b), yielding fraction of SAC area contacted by BCs of type X
versus distance from soma.

**Co-stratification null model.** To test whether the observed wiring just reflects shared IPL depth
(Peters Rule), the authors compute predicted contact as the integral over IPL depth of the product
of the BC-type stratification profile and the SAC stratification profile at each distance bin.
Deviations between observed and predicted contact quantify the strength of wiring specificity beyond
co-stratification.

**DS model.** The SAC dendrite output is modelled as a rectified linear-nonlinear filter applied to
a spatiotemporal convolution of the visual stimulus against a kernel W(x, t) = U_s(x) nu_s(t) +
U_t(x) nu_t(t). The sustained temporal filter nu_s(t) is monophasic (BC2); the transient temporal
filter nu_t(t) is biphasic (BC3a). The two spatial weighting functions U_s(x) and U_t(x) are read
off the BC2 and BC3a contact-versus-distance curves. Because U_s and U_t are spatially displaced and
nu_s, nu_t have different dynamics, W is oriented in space-time and yields DS. Setting nu_t to
monophasic positive recovers a Reichardt detector; setting nu_t to monophasic negative recovers a
Barlow-Levick detector; the full biphasic form combines both enhancement (preferred direction) and
cancellation (null direction) mechanisms.

## Results

* **Reconstruction scale**: 79 Off SACs and 195 Off BC axons reconstructed from the e2198 dataset;
  ~5,881 EyeWire volunteers contributed, with 208 volunteers submitting >=500 cubes each used for
  skill analysis.
* **BC-SAC contact dichotomy**: when the contact matrix is sorted by BC type, **BC2 and BC3a**
  contact SACs far more than the other three Off BC types (BC1, BC3b, BC4); BC2 preferentially
  contacts proximal SAC dendrite segments, whereas BC3a preferentially contacts distal segments
  (Fig. 4b-d).
* **Physiological time-lag constraint**: prior two-photon calcium imaging in BC axons and glutamate
  imaging around BC axons (Baden 2013, Borghuis 2013) show that **BC2 lags BC3a by 50-100 ms** in
  visual responses, consistent with the near-lags-far requirement for an outward preferred
  direction.
* **SAC dendritic tilt**: Off SAC dendrites dive from the INL into the IPL near the soma, then
  continue to deepen slightly over the tangential distance range **20-80 micrometre** from the soma.
  Off SACs stratify at **32%** IPL depth (INL/GCL = 0/100%), On SACs at **62%**; the dendritic tilt
  in depth is consistent with overlapping more with the shallower BC2 proximally and the deeper BC3a
  distally.
* **Co-stratification fails as a complete explanation**: actual BC2 contact depends on distance more
  strongly than co-stratification predicts; BC3a, BC3b and BC4 stratify at nearly identical IPL
  depths yet BC3a makes far more contact than BC3b or BC4; BC3a contact plummets at the distal-most
  SAC tips while predicted contact does not. Together these violations of Peters Rule confirm that
  the BC-SAC wiring is specific beyond what shared IPL depth can explain.
* **Model behaviour**: the sustained-transient two-subunit model with the fitted BC2/BC3a spatial
  profiles exhibits DS with the correct outward preferred direction, is consistent with isopotential
  SAC dendrites (so the somatic-voltage DSI matches experimental intracellular recordings, unlike
  the pure postsynaptic-delay cable model of Tukker et al. 2004 which predicts an incorrect inward
  preferred direction), and displays a tuned optimum of DSI versus stimulus speed (Extended Data
  Fig. 9).
* **EyeWire accuracy**: the highest-performing EyeWirers achieve near-expert precision and recall on
  ganglion-cell reconstruction; consensus of 5-10 non-expert players exceeds any single player
  accuracy; more than 208 volunteers completed >=500 cubes each.

## Innovations

### Dense-EM-derived space-time wiring specificity

First demonstration that the direction selectivity of a SAC dendrite can be predicted from the
spatial ordering of presynaptic BC types along the dendrite, using dense connectomic reconstruction
rather than electrophysiology. Establishes BC2-proximal / BC3a-distal as the canonical Off-SAC
wiring motif.

### Hybrid AI + crowd connectomics with EyeWire

Operational demonstration that a deep-convolutional-network oversegmentation combined with a
crowdsourced game interface can deliver expert-quality neurite reconstruction at a scale (79 SACs,
195 BCs, 5881 volunteers) far beyond what a lab paid workforce alone could achieve. This predates
MICrONS and FlyWire and seeds the technical pipeline they extend.

### Unifying framework for Reichardt and Barlow-Levick motion detectors

By deriving both detector families as special cases of a single two-subunit linear-nonlinear model
parameterised by the biphasic shape of the transient temporal filter, the paper reconciles
sustained-vs-transient BC dichotomy with classical fly (Reichardt) and rabbit (Barlow-Levick)
motion-detector models, suggesting T4/T5 in *Drosophila* and Off-SAC dendrites compute the same
canonical operation.

### Quantitative violation of Peters Rule in a vertebrate connectome

First dense-EM retinal demonstration that subtle, functionally-important connectivity is missed by
co-stratification (Peters Rule): BC3a, BC3b, BC4 stratify at the same depth but only BC3a
preferentially contacts SAC distal dendrites. Methodological template for separating wiring
specificity from arbor overlap in downstream connectome studies.

## Datasets

* **e2198**: mouse retina SBEM volume originally acquired by Briggman, Helmstaedter & Denk (Nature
  2011); large enough to encompass entire Off SAC dendritic arbors (~150 micrometre radius). Tissue
  shrinkage estimated at 14% by comparison of two-photon and serial EM images. Publicly available
  from the Denk/Helmstaedter archives and downstream via EyeWire.
* **EyeWire reconstructions from e2198**: 79 Off SAC reconstructions + 195 Off BC axon
  reconstructions produced by this study. Released through the EyeWire platform (eyewire.org) and in
  the paper supplementary data. Accompanied by a questionnaire (n = 729 respondents) capturing
  EyeWirer demographics and self-reported playtime.
* **Reference BC density data**: Waessle, Puller, Mueller & Haverkamp (J. Neurosci. 2009) type
  densities (2233, 3212, 1866, 3254, 3005 cells/mm^2 for BC1, BC2, BC3a, BC3b, BC4) used as
  validation against the study own mosaics.
* **Prior BC response timing**: Baden et al. (Curr. Biol. 2013) two-photon calcium imaging in BC
  axons and Borghuis et al. (J. Neurosci. 2013) extracellular glutamate imaging (iGluSnFR) are used
  as external sources for the 50-100 ms BC2-vs-BC3a lag constraint feeding the model.

## Main Ideas

* **Treat SAC dendritic morphology as a prior for a compartmental DSGC/SAC model input layer**: when
  building a compartmental sweep downstream of this paper, the BC2 (proximal) + BC3a (distal)
  contact-versus-distance curves from Fig. 4d are the canonical spatial weighting to use for
  excitatory conductances, and the 50-100 ms BC2-BC3a lag is the canonical input timing offset.
* **The SAC dendrite can be approximated as isopotential for DS purposes**: morphology still
  matters, but through *where different BC types synapse*, not through passive cable conduction
  delays. A pure passive-cable model (Tukker 2004) predicts the wrong preferred direction at the
  soma. Any downstream compartmental model has to either reproduce the Kim2014 wiring or add active
  dendritic conductances to rescue the cable-delay hypothesis.
* **Co-stratification is a biased estimator of connectivity**: Peters Rule systematically misses the
  functionally-important BC3a vs BC3b/BC4 distinction at the same IPL depth. Any automated model
  that draws synapses from shared stratification alone will fail to reproduce SAC DS. Compartmental
  models must use reconstructed contact or synapse data, not proximity.
* **Inhibition is adjunct, not essential**: DS survives inhibitory blockade, so the Kim2014 model
  keeps only excitatory BC-SAC inputs. Downstream compartmental models can adopt the same
  excitation-only minimal circuit for a first-pass DS prediction before layering SAC-SAC inhibition
  on top for tuning-curve refinement.
* **The e2198 reconstructions define a shared benchmark**: the 79 SACs + 195 BCs here, plus the DSGC
  subset from Briggman et al. 2011, form the standard connectome substrate for *all* mouse-retina
  DSGC compartmental modelling through at least 2026.

## Summary

Kim et al. answer a 50-year-old question about where direction selectivity arises in the mammalian
retina by combining dense electron-microscopy reconstruction with a minimal mathematical model.
Rather than attributing DS to biophysical properties of the SAC dendrite itself (an earlier
hypothesis that predicts the wrong preferred direction at the soma), they propose that DS is built
into the wiring diagram: BC types with slow visual responses synapse near the SAC soma, BC types
with fast responses synapse far from it, so outward motion produces synchronous arrival of
excitation along the dendrite and inward motion produces asynchronous arrival.

The test is carried out on the e2198 mouse-retina SBEM dataset using a deep-convolutional-network AI
for voxel oversegmentation and a crowdsourced game, EyeWire, for the neurite-agglomeration step.
Paid lab workers and 5881 volunteer citizen-neuroscientists reconstructed 79 Off SACs and 195 Off BC
axons. Contact area between every BC-SAC pair was computed, sorted by BC type and by distance from
the SAC soma, and compared against a co-stratification null model based on Peters Rule. The five Off
BC types (BC1, BC2, BC3a, BC3b, BC4) were classified by IPL-stratification profile and validated by
mosaic regularity and density.

The contact analysis reveals a sharp dichotomy: among the five Off BC types, only BC2 (proximal) and
BC3a (distal) contact SACs substantially, and published two-photon calcium and glutamate imaging
show BC2 lags BC3a by 50-100 ms, exactly the sign and order required for outward preferred
direction. A linear-nonlinear model with a sustained (BC2) and a transient biphasic (BC3a) subunit
produces DS that subsumes Reichardt and Barlow-Levick detectors as limiting cases, survives the
isopotential-dendrite approximation (matching somatic intracellular recordings), and suggests
mammalian Off-SAC dendrites and *Drosophila* T4/T5 cells implement the same canonical motion
operator. A subtle dendritic tilt through the IPL (20-80 micrometre distance from soma) partially
supports the wiring specificity but fails to fully account for it, demonstrating quantitative
violation of Peters Rule.

For the t0027 literature survey on morphology-driven DS modelling, Kim2014 is the canonical
connectome + anatomical-wiring input that every downstream compartmental DSGC/SAC model (including
Poleg-Polsky and Diamond 2026 work) consumes as its substrate. The paper is flagged as borderline
because it is primarily an EM + behavioural-model paper, not a morphology-sweep paper: the
morphology captured is the SAC stratification-depth profile and the BC2/BC3a proximal/distal contact
pattern, not a multi-compartment cable simulation. When reviewing compartmental DS models, Kim2014
contact-vs-distance curves (Fig. 4d) should be treated as ground-truth boundary conditions for the
excitatory input spatial weighting, and the 50-100 ms BC2-vs-BC3a lag as the ground-truth
input-timing offset. Any compartmental model that cannot reproduce this wiring is missing the
principal mechanism of SAC DS as currently understood.
