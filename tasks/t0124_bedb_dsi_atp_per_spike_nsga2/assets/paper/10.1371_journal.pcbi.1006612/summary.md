---
spec_version: "3"
paper_id: "10.1371_journal.pcbi.1006612"
citation_key: "Remme2018"
summarized_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_summarized: "2026-05-25"
---
# Function and energy consumption constrain neuronal biophysics in a canonical computation: Coincidence detection

## Metadata

* **File**: `files/remme_2018_mso-coincidence-pareto-energy.pdf`
* **Published**: 2018-12-06
* **Authors**: Michiel W. H. Remme 🇩🇪, John Rinzel 🇺🇸, Susanne Schreiber 🇩🇪
* **Venue**: PLOS Computational Biology, 14(12): e1006612
* **DOI**: `10.1371/journal.pcbi.1006612`
* **Code**: ModelDB accession 245424

## Abstract

Neural morphology and membrane properties vary greatly between cell types in the nervous system. The
computations and local circuit connectivity that neurons support are thought to be the key factors
constraining the cells' biophysical properties. Nevertheless, additional constraints can be expected
to further shape neuronal design. Here, we focus on a particularly energy-intense system (as
indicated by metabolic markers): principal neurons in the medial superior olive (MSO) nucleus of the
auditory brainstem. Based on a modeling approach, we show that a trade-off between the level of
performance of a functionally relevant computation and energy consumption predicts optimal ranges
for cell morphology and membrane properties. The biophysical parameters appear most strongly
constrained by functional needs, while energy use is minimized as long as function can be
maintained. The key factors that determine model performance and energy consumption are (1) the
saturation of the synaptic conductance input and (2) the temporal resolution of the postsynaptic
signals as they reach the soma, which is largely determined by active membrane properties. MSO cells
seem to operate close to pareto optimality, i.e., the trade-off boundary between performance and
energy consumption that is formed by the set of optimal models. Good performance for drastically
lower costs could in theory be achieved by small neurons without dendrites, as seen in the avian
auditory system, pointing to additional constraints for mammalian MSO cells, including their circuit
connectivity.

## Overview

The paper builds a minimal biophysical model of a principal medial superior olive (MSO) neuron of
the mammalian auditory brainstem and uses it to ask whether the cell's measured morphology and
membrane parameters reflect a joint optimisation against (i) functional performance, defined as
ITD-discrimination firing-rate modulation, and (ii) per-second metabolic cost, expressed in ATP
consumed by the Na/K pump. The model has a soma plus two passive cylindrical dendrites carrying a
uniform low-threshold voltage-gated potassium current (IKLT). It is fitted to gerbil patch-clamp
data on EPSP attenuation, somatic EPSP halfwidth, and input resistance with and without DTX block of
IKLT.

The authors then sweep six biophysical parameters one at a time -- dendrite length, dendrite
diameter, soma surface area, leak density, KLT density, KLT activation time constant -- and trace
both performance and energy cost. Costs are computed by the Attwell-Laughlin ion-counting method:
total Na+ influx during the simulation divided by 3 to get ATP per second. The resulting
parameter-by-parameter curves are then collapsed into a 2-D energy-vs-(reciprocal)-performance
space, and the convex lower-left envelope is identified as the local Pareto optimal front.

The headline finding is that the experimentally fitted "default" gerbil MSO model sits essentially
on this Pareto front: no single-parameter perturbation can improve performance without raising cost
or lower cost without sacrificing performance. Two-parameter sweeps (joint leak-KLT density; joint
dendrite length-diameter at fixed surface area) confirm the same picture and identify the saturation
of synaptic input and the temporal resolution of the somatic EPSP -- both shaped by IKLT -- as the
two dominant mechanistic factors that set both performance and cost.

The result is presented as evidence that evolution has prioritised function over energy efficiency
in MSO cells, but has chosen, within the function-feasible region, the cheapest available design. A
point-neuron control shows that a tiny dendrite-less cell could match most of the MSO's performance
at a fraction of the cost, so the actual MSO morphology must reflect further constraints (synapse
surface, circuit connectivity) not captured by the function-cost trade-off alone.

## Architecture, Models and Methods

The compartmental model is a soma plus two identical passive cylindrical dendrites; dendrites are
discretised into segments of length 0.02 times the passive space constant. The voltage equation per
compartment is the standard cable equation with three membrane currents: a passive leak, a
low-threshold voltage-dependent potassium current IKLT (uniform density throughout soma and
dendrites, with a fast activation gate w with tau approx 1 ms at rest and a slow inactivation gate z
fixed at its rest value), and a synaptic current. Specific membrane capacitance is **Cm = 1
uF/cm^2**, axial resistivity **Ra = 200 Ohm cm**. The h-current and other non-KLT subthreshold
currents are subsumed into the leak conductance so that the cell's resting potential is **-60 mV**;
**EK = -106 mV**.

Default morphology, taken from gerbil anatomical data, is soma surface **1256 um^2** (equivalent to
a 25 um x 16 um cylinder), dendrite length **150 um**, dendrite diameter **2.5 um**. Default
membrane parameters fitted to gerbil patch-clamp data are leak density **gL = 0.86 mS/cm^2** and KLT
peak density **gKLT = 13.6 mS/cm^2**, chosen as the minimum of summed normalised squared error over
four electrophysiological observables: input resistance under control (**11.4 MOhm**), input
resistance with KLT blocked (**36.2 MOhm**), dendrite-to-soma EPSP attenuation, and somatic EPSP
halfwidth.

Synaptic input is modelled as **6 excitatory fibres per dendrite** (12 total), each making one
synaptic contact uniformly distributed across the distal two thirds of its dendrite. Each fibre
fires at average **240 spikes/s** phase-locked to a **500 Hz pure tone** with a Gaussian jitter
giving vector strength **0.988**, and randomly skips cycles to introduce noise. The synaptic
conductance is an alpha function with **tau = 0.2 ms** and reversal potential **0 mV** (sodium:
potassium conductance ratio fixed at **2:1**, matching Erev = 0 mV given ENa = 53 mV and EK = -106
mV). Synaptic peak conductance is fitted per cell variant to maximise the rate modulation **r0 -
r0.5** (firing rate at ITD = 0 minus rate at ITD = 0.5 ms); the default cell uses **~20 nS per
fibre**.

Spikes are read out from a separate axonal compartment with **threshold = -50 mV**, **reset = -60
mV**, **refractory period = 1 ms**, **tau_m = 0.2 ms**, coupled to the soma with a coupling time
constant of **0.05 ms** in a feed-forward manner so axonal spikes do not perturb the soma.
Simulations are **5000 ms** long with **dt = 0.01 ms**, integrated by Crank-Nicolson in C, analysed
in MATLAB.

Energy cost uses the Attwell-Laughlin ion-counting approach: leak and synaptic currents are split
into separate Na+ and K+ components (the leak split is parameter-dependent because EL is adjusted to
hold Vrest = -60 mV); the total Na+ influx across the whole cell is averaged over the simulation and
converted to ATP/s via **3 Na+ per ATP** (the Na/K pump ratio). Performance is the rate modulation
r0 - r0.5; the reciprocal of performance is plotted on the x-axis of all trade-off panels
(lower-left corner = best).

Pareto fronts are constructed by varying parameters in physiologically realistic ranges (e.g.
dendrite length 5-400 um, leak 0.2-10 mS/cm^2, KLT 0.2-40 mS/cm^2) and tracing the lower-left
envelope of the resulting cloud in (energy, 1/performance) space.

## Results

* Default fitted gerbil MSO model produces a rate modulation **r0 - r0.5 ~ 320 spikes/s** with a
  total cell Na+ current **~3 nA**, equivalent to **6.2 x 10^9 ATP/s** input-processing cost
* Performance peaks at dendrite length **150-190 um**, exactly bracketing the anatomical default of
  150 um; both shorter and much longer dendrites lose performance, while cost rises monotonically
  with length
* Removing IKLT (passive model) approximately **halves** peak performance and approximately
  **doubles** cost at matched performance -- IKLT is critical for the sharp EPSP that enables
  microsecond ITD discrimination
* Joint leak-KLT density sweep at fixed Vrest = -60 mV pushes maximum performance to **~440
  spikes/s** but at substantially higher cost; the default cell sits very close to this 2-D Pareto
  front
* A point-neuron (zero-dendrite) control reaches **~360 spikes/s** at far lower cost than the
  default, showing that the dendritic morphology is not energy-optimal in isolation
* Axonal output spike cost is estimated at **3.2 x 10^8 to 9.6 x 10^8 ATP/s** for 100-300 spikes/s,
  about an order of magnitude smaller than the input-processing cost
* Estimated cortical-pyramidal input-processing cost from Attwell & Laughlin 2001 is **1.44 x 10^9
  ATP/s**, i.e. only **~23%** of the MSO input-processing cost; cerebellar granule cells are cheaper
  still (~0.12 x 10^9 ATP/s) while Purkinje/Golgi reach ~3.7 x 10^9 ATP/s
* Energy density of the MSO cell is approximately **1.7 x 10^6 ATP per um^3 per second** assuming a
  cell volume of 3600 um^3
* Spontaneous-input energy cost (no relevant sound stimulus) is **~50%** of the sound-driven cost,
  driven by ~55 spikes/s spontaneous excitatory fibre activity
* Performance degrades sharply once dendritic synaptic input depolarisation exceeds **~40 mV**
  because saturation broadens the somatic EPSP and shrinks somatic voltage fluctuations -- the
  trade-off curve becomes simultaneously worse in both dimensions, ruling out that regime

## Innovations

### Explicit Pareto-front Framing of Single-Neuron Multi-Objective Optimisation

The paper is the most-cited prior work to cast single-neuron parameter selection as a Pareto
optimisation between a computational performance metric and a per-second ATP cost computed by ion
counting. Both axes are scalar, biophysically grounded, and computed from the same simulation,
allowing one trade-off plot to summarise five biophysical parameters at once. This is the direct
methodological ancestor of the NSGA-II "DSI vs ATP-per-spike" formulation used in t0124.

### Identification of Saturation and Temporal Resolution as the Two Dominant Trade-off Drivers

By varying six parameters one at a time and projecting the results into the 2-D cost-performance
space, the authors show that the entire Pareto front is governed by just two derived quantities: the
saturation level of the synaptic conductance input in the dendrite and the halfwidth of the
propagated somatic EPSP. This is a reduction of a six-dimensional parameter sweep to a
two-dimensional mechanistic explanation, and provides a template for how to interpret
high-dimensional NSGA-II fronts in terms of a small number of biophysical bottlenecks.

### Per-Spike-Decomposed ATP Accounting from the Ion-Counting Method

The paper applies the Attwell-Laughlin ion-counting approach (Attwell & Laughlin 2001) at the level
of a single compartmental cell with explicit per-current Na+/K+ splits (synaptic, leak, KLT), making
the cost calculation reproducible from simulation output alone. This is the same accounting scheme
that t0124 inherits to compute ATP per spike on the DSGC model.

### Empirical Default Falls on the Pareto Front

The experimentally fitted MSO cell parameters sit essentially on the modelled Pareto boundary in
both the one-parameter sweeps and the two-parameter sweeps. This is a falsifiable prediction of the
joint function-energy hypothesis and supports the broader claim that real neurons can be read as
Pareto-optimal designs, not as separate function-only or energy-only optima.

## Datasets

This is a modelling and theoretical paper; no new datasets were collected. The model is fitted to
previously published gerbil (Meriones unguiculatus) patch-clamp data from Mathews et al. 2010 (J
Neurosci) for IKLT-dependent EPSP attenuation, somatic EPSP halfwidth, and input resistance with and
without DTX block, and gerbil MSO anatomical data from Rautenberg et al. 2009 (J Comp Neurol). The
simulation code is publicly available in the ModelDB database under accession **245424**
(http://modeldb.yale.edu/245424); it is written in C with MATLAB analysis. No human or animal data
were collected by the authors.

## Main Ideas

* The Pareto-front framing in (energy cost, 1/performance) space is directly portable to t0124: swap
  "ITD rate modulation" for "DSI" and "MSO Na+ ATP" for "DSGC ATP per spike", and the same
  diagnostic plot applies. NSGA-II is doing what Remme et al. did by exhaustive single-parameter
  sweeps; the front interpretation is the same.
* Ion-counting cost (sum of Na+ influx divided by 3) is the most defensible per-second metabolic
  metric for a compartmental model and should be used for t0124's ATP axis. Splitting leak and
  synaptic currents into Na+/K+ components requires only the reversal potentials and the imposed
  Vrest, no extra fitting.
* The two-mechanism explanation (synaptic saturation + somatic EPSP halfwidth) is a strong hint that
  high-dimensional NSGA-II fronts can be projected onto a small number of derived,
  cable-theory-grounded summary statistics for interpretation. Worth probing for an analogous pair
  in the DSGC case (e.g. dendritic local depolarisation level + somatic preferred-direction EPSP
  shape).
* Input-processing costs in the auditory brainstem dwarf spike output costs by ~10x in MSO. Whether
  this remains true for a DSGC under preferred/null wave stimuli is an open question that t0124 can
  quantify directly.
* The empirical-on-Pareto-front result is the comparison anchor for t0124: the published DSGC
  morphology and channel densities should be reported with their (DSI, ATP/spike) coordinates
  relative to the NSGA-II front the task computes.

## Summary

Remme, Rinzel, and Schreiber address whether the morphology and membrane parameters of a real
mammalian neuron reflect a joint optimisation between functional performance and metabolic energy
consumption, or whether one of those two constraints dominates. They choose the principal MSO cell
of the auditory brainstem as their test case because (i) the functional computation -- interaural
time difference coincidence detection -- is unambiguous and quantifiable, and (ii) prior
immunohistochemistry has flagged MSO neurons as exceptionally energy-intense, making any
function-energy compromise easy to detect.

They build a minimal compartmental model -- soma plus two passive dendrites carrying a uniform
voltage-gated low-threshold potassium current IKLT -- fit it to published gerbil patch-clamp data on
EPSP attenuation, EPSP halfwidth, and input resistance with and without DTX block, and exhaustively
sweep six biophysical parameters (three morphological, three membrane) one at a time and in selected
two-parameter combinations. Performance is the firing-rate modulation between ITD = 0 ms and ITD =
0.5 ms under a 500 Hz phase-locked pure-tone input; energy cost is total Na+ influx across the cell
converted to ATP/s via the Attwell-Laughlin 3-Na+-per-ATP ion-counting scheme. Each parameter sweep
is plotted as a curve in (energy cost, 1/performance) space, and the lower-left envelope across all
sweeps is identified as the local Pareto-optimal front.

The empirically fitted MSO model produces **~320 spikes/s** rate modulation at **6.2 x 10^9 ATP/s**
and sits essentially on the Pareto front: no single-parameter perturbation can improve performance
without raising cost or vice versa. The KLT current is essential -- passive variants halve
performance and double cost. Most morphological and membrane parameters show a clear performance
peak near the measured default, while energy cost rises monotonically with cell size; the cell
appears to spend energy only where function demands it. A dendrite-less point-neuron control matches
most of the performance at far lower cost, so the measured dendritic morphology must reflect
non-function-non-energy constraints (e.g. surface area for synapses, circuit wiring).

This paper is the direct methodological template for t0124. The task's "DSI vs ATP per spike"
NSGA-II optimisation is the natural extension of Remme et al.'s exhaustive sweep into many more
dimensions, on a direction-selective retinal ganglion cell instead of an MSO cell. The ion-counting
cost calculation, the choice to use a scalar performance metric in opposition to a scalar metabolic
metric, the practice of locating empirical defaults on the computed Pareto front, and the search for
a small set of mechanistic factors that explain the front shape are all strategies t0124 should
reuse. This will be the primary literature anchor for t0124's compare-literature stage.
