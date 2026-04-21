---
spec_version: "3"
paper_id: "10.1017_S0952523823000019"
citation_key: "Wu2023"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Two mechanisms for direction selectivity in a model of the primate starburst amacrine cell

## Metadata

* **File**: `files/wu_2023_primate-sac-ds-mechanisms.pdf`
* **Published**: 2023-05-23
* **Authors**: Jiajia Wu, Yeon Jin Kim, Dennis M. Dacey, John B. Troy, Robert G. Smith (all US)
* **Venue**: Visual Neuroscience 40, E003 (Cambridge University Press)
* **DOI**: `10.1017/S0952523823000019`

## Abstract

In a recent study, visual signals were recorded for the first time in starburst amacrine cells of
the macaque retina, and, as for mouse and rabbit, a directional bias observed in calcium signals was
recorded from near the dendritic tips. Stimulus motion from the soma toward the tip generated a
larger calcium signal than motion from the tip toward the soma. Two mechanisms affecting the
spatiotemporal summation of excitatory postsynaptic currents have been proposed to contribute to
directional signaling at the dendritic tips of starbursts: (1) a "morphological" mechanism in which
electrotonic propagation of excitatory synaptic currents along a dendrite sums bipolar cell inputs
at the dendritic tip preferentially for stimulus motion in the centrifugal direction; (2) a
"space-time" mechanism that relies on differences in the time-courses of proximal and distal bipolar
cell inputs to favor centrifugal stimulus motion. To explore the contributions of these two
mechanisms in the primate, we developed a realistic computational model based on connectomic
reconstruction of a macaque starburst cell and the distribution of its synaptic inputs from
sustained and transient bipolar cell types. Our model suggests that both mechanisms can initiate
direction selectivity in starburst dendrites, but their contributions differ depending on the
spatiotemporal properties of the stimulus. Specifically, the morphological mechanism dominates when
small visual objects are moving at high velocities, and the space-time mechanism contributes most
for large visual objects moving at low velocities.

## Overview

**Morphology variable in this paper: SAC dendritic geometry (diameters of proximal, medial, and
distal sections), not DSGC. Flag: SAC, not DSGC.** The paper evaluates DS at distal SAC dendritic
tips. The cell itself is a compartmental starburst amacrine cell (SAC); there is no
direction-selective ganglion cell (DSGC) in the model. The overall dendritic tree shape is held
fixed using a connectomic reconstruction of a macaque ON SAC (Kim et al. 2022), but dendritic
diameters are parametrically swept in Fig. 9 (distal 0.2 to 1.2 um; medial 0.1 to 0.35 um) while DSI
is measured at the distal tip. In addition, a second, morphologically distinct SAC (mouse; Ding et
al. 2016) is simulated with the same pipeline as a cross-species morphology manipulation.

Wu et al. (2023) use NeuronC compartmental models (400 to 700 compartments, ~0.02 length constants
per compartment) of both macaque and mouse ON SACs to quantify the relative contributions of two
dendritic DS mechanisms that have been debated for two decades. The "morphological" mechanism relies
on electrotonic delay along thin medial dendrites plus a "sealed cable" effect at thicker distal
tips; the "space-time" mechanism relies on the spatial segregation of sustained midget bipolar
inputs (across the whole tree) versus transient DB4/5 bipolar inputs (distal only). The authors
sweep bar width (50 to 500 um) and velocity (100 to 10,000 um/s, i.e. 0.5 to 50 deg/s at the macaque
retina) in a 2D stimulus grid and run 30 random-instance replicates per parameter cell.

The headline qualitative result is a bar-width x velocity "phase diagram": the morphological
mechanism dominates for small, fast stimuli; the space-time mechanism dominates for large, slow
stimuli. Removing the transient DB4/5 inputs (sustained-only model) isolates the morphological
contribution, and its DSI peaks around 2000 um/s regardless of species. Sweeping dendritic diameters
shows that medial diameter ~0.2 to 0.25 um maximises DSI (matching the anatomically measured 0.15 to
0.2 um), while distal diameter saturates DSI once it exceeds ~0.8 um. Adding slowly inactivating
N/P/Q-type dendritic Ca channels amplifies single-trial DSI from 0.28 (voltage) to 0.46 (voltage
with Ca) to 0.78 (Ca concentration), but variance is large because the subthreshold gain is
uncontrolled. The same morphological + space-time partition holds in the mouse SAC model despite
~4-fold higher bipolar input density and the restriction of inputs to the inner 2/3 of the dendritic
tree, indicating that these two mechanisms are robust features of the starburst architecture rather
than species-specific adaptations. For the current task, the critical take-home is that SAC
dendritic diameter (medial and distal) tunes the morphological component of DS in a quantitatively
predictable way in a compartmental model.

## Architecture, Models and Methods

**Simulator and cell**: NeuronC (Smith 1992). Macaque ON SAC morphology derived from a 2-photon
reconstruction plus serial EM (Kim et al. 2022). Tree diameter ~250 um. Modelled with 400-700
compartments, each ~0.02 length constants. Soma diameter 9 um. Axial resistivity Ri = 100 Ohm*cm.
Membrane capacitance Cm = 1 uF/cm2. Electrode resistance 20 MOhm. Voltage-gated Na and Ca channels
are omitted from the SAC for the main mechanism comparison (Figs. 5-9); they are added only in Fig.
10\.

**Dendritic diameter fit**: Five free parameters (proximal, medial, distal diameter; Rm soma; Rm
dendrites) fitted by least-squares to a somatic current-clamp charging curve. Best fit: proximal 0.3
um, medial 0.2 um, distal 0.4 um; Rm soma = 22 kOhm*cm2, Rm dendrites = 41 kOhm*cm2. These match
EM-measured diameters (proximal 0.2-0.3 um, medial 0.15-0.2 um, distal 0.4-0.45 um).

**Bipolar cell inputs**: Two types wired onto the SAC tree following connectomics. ON midget
(sustained): density 1900/mm2, covers whole tree; DB4/5 (transient): density 900/mm2, distal only.
Contact made when bipolar soma within 10 um of an SAC dendrite, giving 88 +/- 5.3 contacts per tree
(41 midget, 35 DB4/5). Conductance 10-20 pS, keeping EPSP peak below -50 mV to minimise saturation.
Midget BCs: sustained conductance via slowly inactivating Ca channels + Ca pump, readily releasable
pool 15 vesicles, replenishment 1000/s. DB4/5 BCs: transient response via axon-terminal NaV1.1
(~2500 mS/cm2), Kv1.1 + Kv3 (~1 mS/cm2), vesicle pool 15, replenishment 200/s. Each BC has a
center-surround RF (center 30 um, surround 120 um, surround weight 0.7, surround delay 10 ms).

**Stimulus**: Light bar 500 um long (orthogonal to motion) passed across the full tree. Bar widths
50, 100, 200, 500 um. Velocities 100, 200, 500, 1000, 2000, 5000, 10,000 um/s (covering 0.5-50 deg/s
at macaque retina; mouse retina ~7-fold higher in deg/s because 1 deg = 30 um in mouse versus 200 um
in macaque). Recording at a distal dendritic varicosity (purple asterisk, Fig. 3).

**Metric**: Direction-selective index DSI = (Pref peak - Null peak) / Pref peak, where CF
(centrifugal, soma->tip) is preferred. Thirty replicate models per parameter cell with randomised
SAC rotation and BC locations. Paired two-tailed t-test on DSI of sustained-only versus
sustained+transient models at each (width, velocity).

**Parameter sweep over morphology (Fig. 9)**: Distal diameter varied 0.2 to 1.2 um in 0.2 um steps.
Medial diameter varied 0.1 to 0.35 um in 0.05 um steps. For each diameter set, 30 replicates x 4
stimulus conditions (widths 50, 100 um; velocities 1000, 2000 um/s).

**Mouse model**: Same pipeline with Ding et al. (2016) SAC morphology. Tree ~250 um, bipolar inputs
limited to inner 2/3 of radial extent. Bipolar densities: sustained 10,000/mm2, transient 4600/mm2.
Total ~340 bipolar contacts per tree (215 sustained, 124 transient); BC conductance reduced to 3-7
pS to keep EPSPs subthreshold.

**Calcium channel add-on (Fig. 10)**: Slowly inactivating N/P/Q-type Ca channels at 0.2 mS/cm2 (soma
\+ proximal), 3.5 mS/cm2 (medial), 7.5 mS/cm2 (distal); Ca pump Vmax 0.2-0.7 uA/cm2, Km 30 uM,
setting calcium event fall time 300-500 ms.

**Runtime**: 2-200 min per replicate on 3200 MHz servers; >200,000 total model runs.

## Results

Velocity sweep on a 100 um bar (Fig. 6A-E, Table 2):

* Sustained-only (midget) macaque model: DSI rises from **0.042** at 100 um/s -> **0.055** at 200
  um/s -> **0.110** at 500 um/s -> **0.192** at 1000 um/s -> peak **0.277** at 2000 um/s ->
  **0.274** at 5000 um/s -> drops to **0.176** at 10,000 um/s (morphological mechanism peaks at
  ~2000 um/s, i.e. ~10 deg/s at the macaque retina).
* Sustained+transient (midget + DB4/5): DSI **0.179** at 100 um/s -> **0.296** at 1000 um/s ->
  **0.320** at 2000 um/s -> plateau. Adding transient DB4/5 bipolars increases DSI most at low
  velocity (+0.137 at 100 um/s) and negligibly at high velocity (+0.004 at 5000 um/s), isolating the
  space-time contribution.

Bar-width sweep at 1000 um/s (Fig. 7, Table 2):

* Sustained-only: DSI **0.236** (50 um) -> **0.192** (100 um) -> **0.114** (200 um) -> **0.115**
  (500 um). Morphological mechanism is tuned for small objects.
* Sustained+transient: DSI **0.281** (50 um) -> **0.296** (100 um) -> **0.259** (200 um) ->
  **0.262** (500 um). Transient inputs partly rescue DS for large objects.

SAC dendritic morphology sweep (Fig. 9):

* **Distal diameter** increased from 0.2 to 1.2 um: DSI rises monotonically up to 0.8 um then
  saturates. Confirms that the distal "thick" section boosts DS via the sealed-cable effect but
  exact thickness beyond 0.8 um is not critical.
* **Medial diameter** varied 0.1 to 0.35 um: DSI is non-monotonic with a peak between **0.2 and 0.25
  um**, matching the EM-measured 0.15-0.2 um. Thinner or thicker medial dendrites reduce DS,
  demonstrating that the morphological mechanism depends on a specific impedance mismatch between
  the thin medial neck and the thicker distal tips.
* Adding DB4/5 bipolar inputs shifts the whole DSI-vs-diameter curve up by a roughly constant offset
  but does not change its shape, consistent with the two mechanisms being additive.

Dendritic calcium channels (Fig. 10, single representative run; 50 um bar at 1000 um/s):

* Voltage DSI without Ca channels: **0.28**.
* Voltage DSI with N/P/Q Ca channels: **0.46** (regenerative amplification of supra-threshold CF
  EPSPs while subthreshold CP EPSPs stay below the ~-55 mV Ca threshold).
* [Ca]i DSI with Ca channels: **0.78**. Averaged DSI across 30 replicates is much lower because
  subthreshold EPSP amplitude is uncontrolled (some runs above threshold in both CF and CP, others
  below in both).

Mouse SAC model (Table 2): qualitatively identical morphology x stimulus phase diagram. At 100 um
bar and 1000 um/s the mouse sustained-only DSI is **0.204** (vs 0.192 macaque); sustained+transient
is **0.337** (vs 0.296 macaque). The two mechanisms explain DS across species despite ~4-fold
different bipolar densities and a 2/3 versus full-tree input distribution.

Statistics: For all stimuli at 1000 um/s and below, sustained+transient models produced
significantly higher DSI than sustained-only (two-tailed paired t-test, typically **p < 1e-5** and
down to **p < 1e-16** in 30 replicates; starred cells in Table 2). For velocities 2000-10,000 um/s
the added transient input no longer significantly raises DSI, confirming that the morphological
mechanism saturates the DS at those velocities.

## Innovations

### First quantitative primate SAC compartmental model

Previous quantitative SAC models (Tukker et al. 2004, Ding et al. 2016, Vlasits et al. 2016) used
rabbit or mouse morphology. This is the first model built on connectomic reconstructions of the
macaque ON SAC, incorporating experimentally measured midget vs. DB4/5 bipolar input segregation.

### Formal partitioning of two long-debated DS mechanisms

By running identical models with and without the transient DB4/5 bipolar population, the paper gives
a clean factorial comparison. The difference (sustained+transient - sustained-only) isolates the
space-time contribution; the sustained-only baseline isolates the morphological contribution. The
resulting bar-width x velocity phase diagram (Fig. 8) is the headline contribution of the paper.

### Morphological parameter sweep

Rather than treating morphology as fixed, the authors systematically vary distal and medial
dendritic diameters (Fig. 9) and show that DSI is tuned by the medial (~0.2 um) vs distal (>=0.8 um)
impedance mismatch. This is a direct morphology -> DS quantitative mapping in a compartmental model.

### Cross-species replication with a mouse SAC

The same pipeline rerun on the Ding et al. (2016) mouse morphology yields the same phase diagram,
separating species-specific anatomy from the mechanism-level conclusions. Mouse and macaque tune the
same two dendritic computations to different visual-angle velocity ranges by virtue of their
different eye sizes.

## Datasets

* **Macaque ON SAC morphology**: one 2-photon-reconstructed cell from Kim et al. (2022) periphery
  retina, plus EM-measured dendritic diameters (public serial EM dataset).
* **Mouse ON SAC morphology**: from Ding et al. (2016) connectomic reconstruction.
* **Bipolar connectomics**: macaque midget (n=25) and DB4/5 (n=23) synaptic contacts onto a partial
  SAC reconstruction (Kim et al. 2022).
* **Simulated stimuli**: 4 bar widths x 7 velocities x 2 bipolar configurations x 30 random
  replicates = ~1680 parameter cells, >200,000 simulations in total.
* **Software**: NeuronC simulator, publicly available from
  `https://retina.anatomy.upenn.edu/~rob/neuronc.html`. No proprietary or human subjects data.

## Main Ideas

* SAC dendritic direction selectivity is not a single mechanism; it is the sum of a morphological
  (electrotonic + sealed-cable) contribution and a space-time (sustained vs transient bipolar input)
  contribution, with each dominating a different region of the (object-size, velocity) stimulus
  space.
* Medial dendritic diameter is the single most DS-sensitive morphology parameter in the macaque SAC
  model: the peak at **0.2-0.25 um** matches the real anatomy, and deviations in either direction
  reduce DSI. Distal diameter matters up to ~0.8 um then saturates. For our survey this is a clean
  worked example of a compartmental model that sweeps a morphological parameter and reports DSI as
  the outcome variable.
* Velocity tuning of the morphological mechanism is set by the electrotonic propagation velocity
  along the dendrite (~2000 um/s for these parameters). Any morphology change that alters the length
  constant or dendritic delay will shift the peak DSI velocity; this is a useful prediction to test
  when comparing models that sweep SAC dendritic length.
* The morphology-held-fixed versus morphology-swept dichotomy is nuanced in this paper: the overall
  dendritic tree topology is fixed (from one reconstructed macaque SAC, replicated 30x with random
  rotations), but three key diameter parameters are parametrically varied, and the entire macaque ->
  mouse comparison is effectively a morphology manipulation. This matches our inclusion criterion of
  morphology-as-manipulated-variable.
* NeuronC (Smith 1992) is the simulator of record for this lineage of SAC models. If we later want
  to extend or re-run any of these experiments, NeuronC scripts are publicly available and would be
  a natural starting point.

## Summary

Wu et al. (2023) build a compartmental macaque ON starburst amacrine cell (SAC) model in NeuronC
based on a connectomic reconstruction (Kim et al. 2022) and use it to resolve a two-decade debate
about the origin of direction selectivity (DS) in SAC dendrites. They compare two mechanisms: the
"morphological" mechanism (electrotonic delay along thin medial dendrites plus a sealed-cable effect
at thick distal tips), and the "space-time" mechanism (spatially segregated sustained midget and
transient DB4/5 bipolar inputs). By constructing matched sustained-only and sustained+transient
models they cleanly partition the two contributions.

Methodologically, the model is dense enough to be realistic but simple enough to be interpretable:
400-700 compartments, biophysically parameterised bipolar cells, a 2D stimulus grid of bar widths
(50-500 um) x velocities (100-10,000 um/s), and 30 random replicates per cell. Voltage-gated Na and
Ca channels are deliberately omitted from the SAC in the main analysis to isolate the subthreshold
origin of DS. A separate morphology sweep varies distal (0.2-1.2 um) and medial (0.1-0.35 um)
dendritic diameters, and a mouse SAC model (Ding et al. 2016 morphology) is run alongside as a
cross-species morphology manipulation.

The headline result is a clean phase diagram: the morphological mechanism dominates for small, fast
objects (peak DSI ~0.32 at bar width 50 um, velocity 2000 um/s) while the space-time mechanism
dominates for large, slow objects (DSI goes from ~0.16 sustained-only to ~0.22 sustained+transient
at 500 um bars, 200 um/s). DSI is maximised when medial diameter sits at 0.2-0.25 um (matching the
EM anatomy) and distal diameter >=0.8 um. Dendritic N/P/Q Ca channels regeneratively amplify the
subthreshold DS signal (voltage DSI 0.28 -> 0.46, [Ca] DSI 0.78 in a single run). The mouse model
reproduces the same phase structure despite different bipolar input densities and spatial
distribution.

For our t0027 literature survey on computational models linking neuronal morphology to DS, this
paper is a strong positive example of the sweep-morphology-measure-DS paradigm we are documenting.
The morphology variable is SAC dendritic geometry (not DSGC), and the outcome is DSI at the distal
varicosity. It provides a concrete anchor for (a) the expected DSI range in SAC-only compartmental
models (~0.1-0.4 in voltage, up to ~0.8 in dendritic Ca), (b) the velocity-tuning curve of the
morphological mechanism (peak near 2000 um/s in macaque), and (c) the quantitative impact of medial
vs distal diameter on DSI. Limitations to note for our survey: the model omits GABAergic,
glycinergic, and cholinergic network interactions; DSGC morphology is absent; only one tree topology
is used (diameters are swept but branching pattern and total dendritic length are not). These gaps
will need to be filled by other papers in the survey that sweep DSGC morphology or vary branching
asymmetry.
