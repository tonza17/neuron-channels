---
spec_version: "3"
paper_id: "10.1097_00004647-200110000-00001"
citation_key: "Attwell2001"
summarized_by_task: "t0097_multi_obj_optim"
date_summarized: "2026-05-08"
---
# An Energy Budget for Signaling in the Grey Matter of the Brain

## Metadata

* **File**: `files/attwell_2001_energy-budget-brain.pdf`
* **Published**: 2001-10-01
* **Authors**: David Attwell 🇬🇧, Simon B. Laughlin 🇬🇧
* **Venue**: Journal of Cerebral Blood Flow & Metabolism, 21(10), 1133-1145
* **DOI**: `10.1097/00004647-200110000-00001`

## Abstract

Anatomic and physiologic data are used to analyze the energy expenditure on different components of
excitatory signaling in the grey matter of rodent brain. Action potentials and postsynaptic effects
of glutamate are predicted to consume much of the energy (47% and 34%, respectively), with the
resting potential consuming a smaller amount (13%), and glutamate recycling using only 3%. Energy
usage depends strongly on action potential rate—an increase in activity of 1 action
potential/cortical neuron/s will raise oxygen consumption by 145 mL/100 g grey matter/h. The energy
expended on signaling is a large fraction of the total energy used by the brain; this favors the use
of energy efficient neural codes and wiring patterns. Our estimates of energy usage predict the use
of distributed codes, with ≤15% of neurons simultaneously active, to reduce energy consumption and
allow greater computing power from a fixed number of neurons. Functional magnetic resonance imaging
signals are likely to be dominated by changes in energy usage associated with synaptic currents and
action potential propagation.

## Overview

Attwell and Laughlin construct the first detailed bottom-up energy budget for excitatory signaling
in mammalian grey matter. Starting from the biophysics of single ion channels, single synaptic
vesicles, and single action potentials, they enumerate every step of glutamatergic signaling
(presynaptic Ca2+ entry, vesicle release and recycling, postsynaptic AMPA/NMDA/metabotropic
currents, glutamate uptake into astrocytes, glutamine cycling) and convert each event to an ATP cost
via the Na+/K+ ATPase stoichiometry of 3 Na+ extruded per ATP hydrolyzed. They then aggregate these
per-event costs to a per-neuron-per-second consumption at a typical 4 Hz mean firing rate and scale
to the rodent neocortical density of 9.2 × 10^7 neurons/cm^3.

The headline result is a quantitative hierarchy: action potentials and postsynaptic glutamate
currents jointly account for 81% of signaling energy, resting potentials another 13%, while
presynaptic Ca2+, glutamate recycling, vesicle cycling, and metabotropic spine signaling are minor.
The predicted whole-tissue specific consumption (30 µmol ATP/g/min for signaling, 40 µmol
ATP/g/min total) sits inside the experimentally measured range of 33–50 µmol ATP/g/min for rat
neocortex, validating the budget end-to-end. The paper also derives a simple linear scaling rule —
1 spike/neuron/s ≈ 6.5 µmol ATP/g/min ≈ 145 mL O2/100 g/h — that has since become the
standard reference for relating spike rate to fMRI BOLD signals and to constraint-based
information-coding arguments. A coding-theory section uses the budget to argue that distributed
sparse codes with ≤15% of neurons active are energetically optimal.

## Architecture, Models and Methods

The paper is a quantitative biophysical model rather than an experiment. The Materials and Methods
section derives every cost from first principles. The core conversion is Eq. 9: when an action
potential or synaptic event injects a Na+ load, the Na+/K+ pump must hydrolyze approximately **(Na+
load) / 3** ATP molecules to restore the gradient (the factor 3 comes from the 3-Na+-per-ATP pump
stoichiometry); deviations from this approximation are quantified at 3–11% depending on gNa/gK and
pump kinetics (Hill coefficient 3, EC50 = 20 mmol/L for [Na+]i).

For glutamatergic synapses (37 °C, Q10 = 3 for kinetics, Q10 = 1.3 for conductances), each vesicle
contains 4,000 glutamate molecules. Postsynaptic non-NMDA channels deliver an average of 200,000 Na+
per vesicle (weighted across cerebellar mossy fiber, hippocampal Schaffer, and neocortical synapses,
with channel conductance 11.6–13.3 pS, open time 0.6–1.4 ms, and 2/3 of current carried by Na+
at VNa−V = 120 mV). NMDA channels add charge transfer at NMDA:non-NMDA ratios of 0.15–2.0 (50
pS, 50 ms open time, with Mg2+ block reducing current by ~40%). Recycling each vesicle of glutamate
uses 2.67 ATP per glutamate (1 ATP for Na+/K+ pumping after the 3-Na+/1-H+/1-K+ co-transporter, 0.33
ATP for the H+ exchanger, 1 ATP for glutamine conversion, 0.33 ATP for vesicular H+-ATPase loading).

For action potentials, the Na+ entry per spike is computed from the membrane area and capacitance of
a "typical" rodent cortical neuron: total membrane area 1.49 × 10^5 µm^2 distributed across soma,
dendrites, and axon collaterals, capacitance 1 µF/cm^2, AP amplitude 100 mV. This yields **1.15 ×
10^9 Na+ ions per AP**, requiring **3.84 × 10^8 ATP per AP**. The model assumes Na/K overlap such
that 4× the minimum capacitive charge is needed (factor between minimal and actual ion entry).
Resting-potential maintenance (3.42 × 10^8 ATP/s/neuron, 1.02 × 10^8 ATP/s/glia) is computed from
input resistance, Vrest, and Vrev via Eqs. 2–4. Scaling to whole tissue uses 9.2 × 10^7
neurons/cm^3 in rodent neocortex, 1:1 glia:neuron ratio, 8,000 boutons per neuron, and release
probability 0.25 at 4 Hz.

## Results

* Per action potential, **3.84 × 10^8 ATP** are consumed (Na+ load 1.15 × 10^9 ions); axon
  collaterals dominate at **82%**, dendrites take **14%**, soma only **4%**.
* Per glutamate vesicle, **1.64 × 10^5 ATP** total: postsynaptic ion fluxes **84%** (137,000 ATP),
  presynaptic Ca2+ entry **7%** (12,000 ATP), glutamate recycling **7%** (11,000 ATP), metabotropic
  spine signaling **2%**, vesicle cycling **0.5%**.
* Total ATP per neuron per spike (AP + 2,000 released vesicles) = **7.1 × 10^8 ATP/spike**.
* Resting-potential maintenance: **3.42 × 10^8 ATP/s** per neuron and **1.02 × 10^8 ATP/s** per
  glial cell, summing to **4.44 × 10^8 ATP/s** per neuron-plus-glia unit.
* At 4 Hz mean firing, total per neuron is **3.29 × 10^9 ATP/s**; signaling-related fraction splits
  47% APs, 34% postsynaptic, 13% resting, 3% presynaptic Ca2+, 3% glutamate recycling.
* Scaling rule: **1 spike/neuron/s = 6.5 µmol ATP/g/min** = **21 µmol glucose/100 g/min** = **145
  mL O2/100 g/h** of additional consumption.
* Tissue-level specific consumption predicted at **30 µmol ATP/g/min** for signaling (40 with
  housekeeping), inside the rat-cortex measured range of **33–50 µmol ATP/g/min**.
* Mitochondrial distribution from Wong-Riley (1989) — 62% dendrites, 36% axons/terminals, 2% glia
  — matches the predicted energy distribution of 53% / 42% / 5%.
* In primate cortex, the lower neuron density (3–10× lower with unchanged synapse density) is
  predicted to increase postsynaptic share from 34% to 74% and reduce specific consumption by
  **54%**, matching the observed 54% lower metabolic rate in monkey vs rat neocortex.
* Optimal sparse-coding fraction at 4 Hz is **15% of neurons simultaneously active**, decreasing
  toward higher firing rates; distributed coding gives **4× to 200×** energy savings vs
  grandmother cells when encoding 100 to 10,000 conditions.

## Innovations

### Bottom-Up Per-Event ATP Accounting

The first complete energy budget that decomposes brain metabolism into single elementary events (one
AP, one vesicle, one ion). All previous estimates relied on top-down measurement (whole-brain
glucose or O2 consumption); Attwell and Laughlin showed that summing biophysically computed
per-event costs reproduces the measured tissue-level consumption to within 25%. This established the
methodology for every subsequent neural-energy paper (Lennie 2003, Howarth 2012, Harris 2012, Niven
2008).

### The 1/3 ATP-per-Na+ Conversion Factor

Eq. 9 derives that, to within 3–11%, the ATP cost of any signaling event equals the Na+ load
divided by 3 (the Na+/K+ pump stoichiometry). This reduces an arbitrary biophysical event to a
single quantity: the integrated Na+ influx. For modellers, this is the canonical recipe for adding
an "energy" objective to any compartmental simulation.

### Action-Potential Energy Reassessment

Earlier estimates from heat production (Creutzfeldt 1975) put AP cost at 0.3–3% of brain energy.
Attwell and Laughlin's biophysical analysis raised this to **47%**, a factor of 15× higher. This
correction has been validated by direct mitochondrial-distribution measurements and has been
foundational for arguments that ion-channel kinetics (Hodgkin's 4× safety factor for Na/K overlap)
were under selection pressure for energy efficiency.

### Cell-Density Argument for Primate Brain Scaling

The paper showed that simply changing neuron density at fixed synapse density — with no other
parameter changes — predicts a 54% reduction in primate cortical metabolic rate, matching
measurement. This established that tissue energy budgets can be scaled across species with a small
set of anatomical parameters.

### Energy-Optimal Sparse Coding Prediction

Using the relative cost of resting versus active neurons, the paper derives that 15% sparse codes
are energetically optimal at 4 Hz, increasing to <5% at 40 Hz. This is one of the earliest
quantitative arguments that brain energy constraints select for distributed/sparse representations,
later confirmed for sensory cortex.

## Datasets

This is a theoretical / model-based paper; no datasets were used in the experimental sense. The
authors aggregate published anatomic and physiologic measurements from the literature (rodent
neocortex synaptic density, neuron density, mitochondrial distribution from Wong-Riley 1989,
synaptic conductance values from Silver et al. 1992/1996, Spruston et al. 1995, Markram et al. 1997,
Hestrin 1993; release probability from Markram et al. 1997, Hardingham and Larkman 1998, Silver et
al. 1998; release statistics from Riveros et al. 1986; Q10 and other kinetic data from Hodgkin and
Huxley and successors). All input values and references are tabulated in Materials and Methods. The
70-reference list is the implicit "data source" for the budget.

## Main Ideas

* **ATP per AP via Na+ load / 3**: For the t0097 catalogue's energy objective, the canonical recipe
  is to integrate Na+ influx through every voltage-gated Na channel and Na-permeable synaptic
  channel during a simulation, divide by 3, and report the result in ATP molecules. This is exactly
  what NEURON makes available via the `ina` recording variable per-section, summed over time and
  compartments.
* **AP cost dominates over postsynaptic cost for sparse-spiking cells**: Attwell-Laughlin compute
  that AP propagation accounts for 47% of signaling energy at 4 Hz, with 82% of that going to axon
  collaterals. For a single-cell DSGC simulation that does not include axonal arborization, only the
  somatic + dendritic portion (4% + 14% = 18% of total AP cost in the budget) is internally
  computable; the remaining 82% must be either ignored or estimated via spike count.
* **Resting potential cost is non-negligible (13%)**: A pure spike-counting energy proxy
  underestimates total cost during quiescent periods. For DSGC null-direction trials with suppressed
  firing, the resting cost still consumes substantial ATP — making "minimize energy at null
  direction" a more nuanced objective than just "minimize spike count".
* **Per-vesicle synaptic cost (1.64 × 10^5 ATP) scales linearly with non-NMDA conductance**: The
  84% of synaptic energy that goes to postsynaptic Na+ entry through AMPA/NMDA channels means that,
  for the project's AMPA/GABA input density sweeps, energy cost is approximately proportional to
  AMPA conductance × number of activated synapses. GABA cost is much smaller (Cl- moves down a
  smaller electrochemical gradient).
* **The 1 spike/neuron/s ↔ 145 mL O2/100 g/h scaling rule** is the standard external reference for
  any per-spike energy cost the project reports. Any DSGC simulation that reports an energy
  objective should also report it normalized to "ATP per spike" or "ATP equivalent per simulated
  trial" so it can be compared to the Attwell-Laughlin reference value of 7.1 × 10^8 ATP/spike.

## Summary

Attwell and Laughlin (2001) ask a single quantitative question: how much ATP does each elementary
neuronal signaling event cost, and do these per-event costs sum to the experimentally measured total
energy consumption of brain grey matter? The motivation is that, prior to 2001, neural energy
estimates were either top-down (whole-brain glucose/oxygen consumption with no decomposition) or
based on heat production from single-cell preparations, which severely underestimated AP cost. The
authors aim to construct a biophysically grounded, mechanism-by-mechanism budget that reconciles
micro-scale measurements with whole-tissue metabolism.

The methodology is bottom-up biophysical accounting. They derive a clean scaling result — the ATP
cost of any signaling event equals (Na+ load entering) / 3, set by the Na+/K+ pump stoichiometry —
and apply it to every step of glutamatergic transmission and AP propagation. Inputs are taken from
published patch-clamp, electron-microscopy, and biochemistry literature for rodent neocortex:
synaptic conductance, channel open time, vesicle glutamate content, release probability,
neuron/synapse density, membrane area. The model is intentionally simplified (all neurons treated as
glutamatergic; "typical" cell geometry) so that the dominant contributions can be identified
robustly.

The headline finding is that signaling consumes 75% of grey-matter energy, with action potentials
(47%) and postsynaptic glutamate currents (34%) dominating. The predicted specific consumption of 30
µmol ATP/g/min for signaling, plus 10 µmol/g/min for housekeeping, falls within the measured range
of 33–50 µmol/g/min, validating the budget. The paper also delivers two derived quantities that
have become standard tools: the 1-spike-per-neuron-per-second ≈ 6.5 µmol ATP/g/min scaling rule
(used to convert spike rates to fMRI BOLD predictions) and the 7.1 × 10^8 ATP-per-spike per-neuron
cost. A coding-theory analysis predicts that 15% sparse codes are energetically optimal at
biological firing rates.

For the t0097 multi-objective optimization catalogue, this paper is the foundational citation for
the metabolic-energy objective category. It establishes the "ATP via Na+ load / 3" recipe that maps
any compartmental simulation's integrated Na+ flux to a quantitative ATP cost, gives the per-event
reference values (3.84 × 10^8 ATP per AP, 1.64 × 10^5 ATP per vesicle, 3.42 × 10^8 ATP/s per
resting neuron) needed to validate any future DSGC energy-objective implementation, and provides the
empirical benchmark (7.1 × 10^8 ATP per spike per neuron) against which simulated energy costs can
be sanity-checked. The single-cell, single-event biophysical formulation is directly compatible with
the project's NEURON pipeline, which already records `ina` per-section and per-time-step, so adding
a "minimize ATP per simulated trial" objective to the existing NSGA-II loop is a small extension
rather than an infrastructure rewrite.
