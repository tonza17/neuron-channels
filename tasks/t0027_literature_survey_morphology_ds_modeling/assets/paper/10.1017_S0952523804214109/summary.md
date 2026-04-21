---
spec_version: "3"
paper_id: "10.1017_S0952523804214109"
citation_key: "Tukker2004"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Direction selectivity in a model of the starburst amacrine cell

## Metadata

* **File**: `files/tukker_2004_sac-ds-model.pdf`
* **Published**: 2004 (Visual Neuroscience 21(4), 611-625)
* **Authors**: John J. Tukker 🇺🇸, W. Rowland Taylor 🇺🇸, Robert G. Smith 🇺🇸
* **Venue**: Visual Neuroscience (Cambridge University Press), journal article
* **DOI**: `10.1017/S0952523804214109`

## Abstract

The starburst amacrine cell (SBAC), found in all mammalian retinas, is thought to provide the
directional inhibitory input recorded in On-Off direction-selective ganglion cells (DSGCs). While
voltage recordings from the somas of SBACs have not shown robust direction selectivity (DS), the
dendritic tips of these cells display direction-selective calcium signals, even when
gamma-aminobutyric acid (GABAa,c) channels are blocked, implying that inhibition is not necessary to
generate DS. This suggested that the distinctive morphology of the SBAC could generate a DS signal
at the dendritic tips, where most of its synaptic output is located. To explore this possibility, we
constructed a compartmental model incorporating realistic morphological structure, passive membrane
properties, and excitatory inputs. We found robust DS at the dendritic tips but not at the soma.
Two-spot apparent motion and annulus radial motion produced weak DS, but thin bars produced robust
DS. For these stimuli, DS was caused by the interaction of a local synaptic input signal with a
temporally delayed "global" signal, that is, an excitatory postsynaptic potential (EPSP) that spread
from the activated inputs into the soma and throughout the dendritic tree. In the preferred
direction the signals in the dendritic tips coincided, allowing summation, whereas in the null
direction the local signal preceded the global signal, preventing summation. Sine-wave grating
stimuli produced the greatest amount of DS, especially at high velocities and low spatial
frequencies. The sine-wave DS responses could be accounted for by a simple mathematical model, which
summed phase-shifted signals from soma and dendritic tip. By testing different artificial
morphologies, we discovered DS was relatively independent of the morphological details, but depended
on having a sufficient number of inputs at the distal tips and a limited electrotonic isolation.
Adding voltage-gated calcium channels to the model showed that their threshold effect can amplify DS
in the intracellular calcium signal.

## Overview

**Borderline inclusion: SAC, not DSGC.** This paper models the starburst amacrine cell (SBAC), the
presynaptic interneuron that provides directional input to On-Off DSGCs, rather than the DSGC
itself. It is included in the survey because it explicitly treats SAC dendritic geometry (branching
pattern, first-branch distance, dendritic tree radius, electrotonic length constant, distal vs
proximal input density) as the manipulated independent variable and reads DS out as the dependent
measurement — exactly the methodology the survey targets, one step upstream of DSGC output.

Tukker, Taylor, and Smith built a biophysically realistic compartmental model in the Neuron-C
simulator using two digitized real SBAC morphologies (sb1 from Tauchi and Masland 1984 and sbac3,
unpublished from Taylor and Vaney) plus a family of procedurally generated artificial morphologies
that let them sweep geometry as a parameter. The cells are passive (no voltage-gated sodium, no
GABAergic inhibition), driven by a semirandom array of 200-300 ON-bipolar synapses with realistic
cone photoreceptor transduction. Stimuli include moving bars, two-spot apparent motion, concentric
annuli, sine-wave gratings, and sine-wave bulls-eye annuli (matching Euler et al. 2002).

The central claim is mechanistic: the radial SBAC morphology itself, without any active conductances
and without inhibition, generates a direction-selective voltage signal at the dendritic tips (but
not at the soma) via interaction of a local synaptic EPSP with a temporally delayed global EPSP
spreading from the soma. This extends and formalizes Rall (1964) asymmetric- dendrite intuition, and
preceded (and seeded the modeling framework for) the widely cited Hausselt, Kyuhou, and Euler SBAC
models of the late 2000s.

## Architecture, Models and Methods

**Simulator and geometry.** All simulations ran in Neuron-C (Smith 1992, 2004). Compartment size was
0.1 electrotonic length constants (l) unless explicitly coarsened to 0.65 l for the
morphology-detail sweep. Passive membrane parameters: axial resistivity Ri = 200 Ohm cm, membrane
resistivity Rm = 50,000 Ohm cm^2, capacitance Cm = 1 uF/cm^2. Real morphologies used digitized
dendritic trees of cells sb1 and sbac3; artificial morphologies were generated with a heuristic
branching-and-mutual-avoidance algorithm (5 initial stubs, 5-um growth increments, +/-30 deg
direction search, branching at a threshold parent-distance of ~25 um, 55 deg branch angles, with
varicosities ~3 um placed randomly in the outer third). Dendritic diameter tapered from 1.0 um
(proximal) to 0.5 um (distal).

**Synaptic inputs.** 200-300 ON-bipolar synapses per real SBAC, drawn from a semirandom bipolar
array (nearest-neighbor distance 12 um, regularity 10; 10 um for the single-dendrite case). Each
bipolar contacted the nearest SBAC dendrite within 10 um. Each synapse had unitary conductance 22
pS, 5 channels per synapse, max conductance 110 pS, 2-ms rise/fall, driven via an inverting cone
synapse with realistic photoreceptor saturation and adaptation (Schneeweis and Schnapf 1999). No
surrounds or spatial antagonism in cones/bipolars; no GABA; no Na+.

**Calcium channels (optional).** Eight-state Markov Q-type Ca2+ channel (after Sather et al. 1993;
Serrano et al. 1999) placed in the distal output zone, activation threshold approximately -40 mV,
slow inactivation tau ~150 ms at -30 mV. Density 50 mS/cm^2 (low enough to not feed back on
voltage); radial Ca2+ diffusion shells plus a Ca2+ pump (van Rossum et al. 2003).

**Stimuli.** Bars (widths 20-150 um; default 30 um), two spots, contracting/expanding annuli,
drifting sine-wave gratings (spatial frequency 0.5-3.0 cycles per dendritic-radius in 0.1 steps),
concentric sine-wave annuli (with and without a central 30%-radius mask). Velocities 100-4000 um/s
(sinusoidal) and up to 10,000 um/s (non-sinusoidal). Contrast fixed at 80%. Responses were measured
at 16 dendritic tips per cell plus the soma.

**DSI metric.** DSI = (Vcf - Vcp) / (Vcf + Vcp), where Vcf and Vcp are the peak centrifugal and
centripetal evoked responses; DSI = 1 is maximal centrifugal, 0 is none, -1 maximal centripetal. For
Ca2+ they defined DSCa analogously on peak intracellular calcium concentration.

## Results

* Moving bar (30 um, ~2000 um/s) produced robust DS at dendritic tips (**DSI ~ 0.2**) and
  essentially none at the soma (**DSI ~ 0**), with preferred direction centrifugal.
* Tip-to-tip variability of DSI within a single cell was large (**+/-50%**), but every tip showed
  centrifugal preference and clear velocity tuning.
* Sine-wave gratings gave the strongest DS, approaching ceiling: **DSI up to 0.9** at dendritic
  tips, peaking above 2000 um/s at 0.5 cycles per radius. Soma DSI stayed below **0.1**.
* Optimal grating stimulus: spatial period ~400 um (twice the dendritic length) moving at ~5000
  um/s.
* Stripping the cell to a single branchless dendrite collapsed DSI to **0.03-0.08**, showing that
  sibling dendrites of a full cell contribute to the global EPSP.
* Two-spot apparent motion: **DSI ~ 0.09**; expanding/contracting annulus: **DSI ~ 0.04** —
  confirming that symmetric radial stimuli are poor drivers of the mechanism.
* Branching-pattern sweep: DSI was nearly invariant to the distance of the first branch point,
  except when branching was pushed so distally (less than 20 um from tips) that distal synapse count
  dropped — then DSI fell; and DSI rose with the number of branch points concentrated in the outer
  20% of the tree (**up to 2-fold increase** when synapse density was boosted in the distal zone).
* Electrotonic-length-constant sweep: DSI peaked at an intermediate l of **~400 um** (comparable to
  the dendritic spread), and collapsed at both very small l (pure local, no global) and very large l
  (fully isotropic global).
* Varying dendritic length across the eight dendrites of an artificial cell increased annulus-DSI
  roughly **3-fold**, by breaking the radial symmetry that otherwise cancels annulus DS.
* Adding Q-type Ca2+ channels amplified the voltage DSI by **up to ~3-fold** in DSCa at optimal bar
  velocity (~1000 um/s), thanks to the -40 mV threshold non-linearity.
* Coarsening compartments from 0.1 l to 0.65 l (drastic reduction of morphological detail) left DSI
  essentially unchanged, as long as the soma-centred symmetry was preserved.

## Innovations

### Morphology-Only, Inhibition-Free SBAC DS Model

First peer-reviewed compartmental model to demonstrate quantitatively that a passive, excitatory-
only SBAC with realistic dendritic geometry generates DS at its distal output zones. All prior
SBAC-DS proposals (Vaney 1988; Borg-Graham and Grzywacz 1992; Poznanski 1992) either relied on
active conductances, inhibition, or restricted cable-theoretic approximations; Tukker et al. closed
the loop with full compartmental simulation driven by a physiologically realistic bipolar input
array.

### Local-Global EPSP Summation Mechanism

Formally identified and named the two-component mechanism: a *local* synaptic EPSP generated at the
recorded tip, and a *global* EPSP that spreads from synapses distributed across the rest of the tree
via the soma. Their direction-dependent phase alignment — coincident for centrifugal motion,
out-of-phase for centripetal — is the actual DS operator. Later experimental and modeling work on
SBACs has adopted this decomposition as canonical.

### Simple Two-Sinewave Analytic Model

Built a reduced mathematical model that takes a single tip-stimulus response and a single
soma-stimulus response as measured-in-simulator primitives, introduces a stimulus-dependent phase
delay, and sums. This minimal model reproduces the contour shape of the full-simulator
velocity/spatial-frequency DS surface, giving an intuitive, cable-theory-grounded explanation.

### Artificial-Morphology Parameter Sweeps

Introduced a procedural SBAC generator as an experimental tool — mutual-avoidance growth, tunable
radius and branching density, optional per-dendrite length randomization, random varicosities. This
made geometry itself a manipulated variable rather than a fixed input, enabling clean dissociation
of number of distal inputs from branching pattern from electrotonic length.

### Ca2+ Channel Amplification of Voltage DS

First SBAC model to couple the morphology-driven voltage DSI to a voltage-gated Ca2+ conductance in
the synaptic output zone and quantify the threshold amplification from DSI to DSCa (up to 3x),
bridging the gap between intracellular voltage (hard to measure in SBACs) and calcium imaging (Euler
et al. 2002).

## Datasets

No external datasets were used in the traditional sense. The model consumed two digitized SBAC
morphologies:

* **Cell sb1** — rabbit SBAC, digitized from Tauchi and Masland (1984).
* **Cell sbac3** — rabbit SBAC, unpublished digitization by Taylor and Vaney.

Neither reconstruction is deposited in a public repository cited by the paper. The Neuron-C
simulator and the artificial-morphology generator are available at
`ftp://retina.anatomy.upenn.edu/pub/nc.tgz` (Smith 2004), which also distributes the procedural SBAC
code.

## Main Ideas

* **Geometry alone is sufficient for DS at SBAC tips.** No active dendritic conductances and no
  inhibitory input are needed; passive cable propagation over the radial dendritic tree does the
  work. Useful as a strong null model against which active- and inhibition-based DSGC models should
  be compared.
* **Local + delayed global is the reusable operator.** The phase alignment between a tip-local EPSP
  and a soma-routed global EPSP generalizes beyond SBACs: any centripetally-asymmetric recording
  site on a branched passive dendrite inherits this motion-sensitivity. Directly relevant to DSGC
  dendrites that accumulate SAC and bipolar inputs with similar asymmetry.
* **Distal input count and intermediate electrotonic length (~l = dendritic spread) are the two
  geometry levers that matter.** Exact branching topology and fine compartment detail are
  second-order. This is actionable: if a DSGC model aims to manipulate morphology for DS, vary these
  two quantities first.
* **Symmetric radial stimuli (annuli) are poor probes of morphology-driven DS.** Planar bars and
  gratings reveal the mechanism; this matters for experimental design when comparing model DSIs to
  published SBAC calcium-imaging measurements.
* **Static Ca2+-channel thresholding can inflate output DS by ~3x.** For the survey, this means
  reported DSI values are only comparable when the readout variable (voltage at tip vs calcium
  concentration vs synaptic release) is matched.

## Summary

Tukker, Taylor, and Smith address a specific puzzle raised by Euler et al. (2002): SBAC dendritic
tips show direction-selective calcium signals even with GABAa/c blocked, so where does the DS come
from? The authors hypothesize that the answer is geometry. Their scope is a passive, excitatory-only
SBAC with realistic or parameterizable morphology; their motivation is that the SBAC is the dominant
source of directional inhibition onto DSGCs, so explaining SBAC DS bounds the morphology-to-DSGC
mapping.

The method is a full Neuron-C compartmental simulation built on two digitized rabbit SBACs and a
procedural artificial-morphology generator, driven by a semirandom bipolar array (200-300 synapses)
with physiological cone and synaptic dynamics. They systematically manipulate independent geometric
variables — first-branch distance, distal branching density, dendritic-tree radius, electrotonic
length constant, compartment resolution, and per-dendrite length variability — and read out DSI at
16 dendritic tips and the soma for bars, spots, annuli, and gratings. An optional Q-type Ca2+
channel layer provides the voltage-to-release amplification step.

The headline findings are that (a) morphology alone generates DSI ~ 0.2 at dendritic tips for bars
and DSI up to ~0.9 for gratings; (b) the mechanism is the direction-dependent summation of a local
tip-EPSP with a soma-mediated global EPSP, with optimal electrotonic length ~ dendritic spread; (c)
DS is surprisingly robust to branching detail but sensitive to distal synapse count and to
symmetry-breaking in dendritic length; and (d) a Ca2+-channel threshold can amplify the voltage DSI
roughly threefold in intracellular calcium concentration.

For this project, Tukker 2004 is the canonical starting point for morphology as a causal variable
for DS. It fits the inclusion criteria with the caveat that the cell modeled is the SBAC rather than
the DSGC itself (borderline — flagged in Overview). Its artificial-morphology methodology, DSI
definition, and local-global summation framing should be treated as reference points when comparing
to downstream DSGC-centric modeling work, and its demonstration that passive-only, inhibition-free
morphology can yield strong DS establishes the baseline any more complex retinal DS model must
improve upon.
