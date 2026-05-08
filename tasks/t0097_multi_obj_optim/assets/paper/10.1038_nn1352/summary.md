---
spec_version: "3"
paper_id: "10.1038_nn1352"
citation_key: "Prinz2004"
summarized_by_task: "t0097_multi_obj_optim"
date_summarized: "2026-05-08"
---

# Similar Network Activity from Disparate Circuit Parameters

## Metadata

* **File**: `files/prinz_2004_disparate-circuit-parameters.pdf`
* **Published**: 2004
* **Authors**: Astrid A. Prinz US, Dirk Bucher US, Eve Marder US
* **Venue**: Nature Neuroscience, 7(12), 1345-1352
* **DOI**: `10.1038/nn1352`

## Abstract

It is often assumed that cellular and synaptic properties need to be regulated to specific values
to allow a neuronal network to function properly. To determine how tightly neuronal properties and
synaptic strengths need to be tuned to produce a given network output, we simulated more than 20
million versions of a three-cell model of the pyloric network of the crustacean stomatogastric
ganglion using different combinations of synapse strengths and neuron properties. We found that
virtually indistinguishable network activity can arise from widely disparate sets of underlying
mechanisms, suggesting that there could be considerable animal-to-animal variability in many of the
parameters that control network activity, and that many different combinations of synaptic
strengths and intrinsic membrane properties can be consistent with appropriate network performance.

## Overview

This paper is the canonical demonstration that biophysically detailed neuronal networks exhibit
parameter degeneracy: very different combinations of intrinsic conductances and synaptic strengths
can produce nearly indistinguishable functional output. Prinz, Bucher and Marder address a question
that had been raised at the single-neuron level (Goldman, Golowasch, Marder and Abbott, 2001;
Prinz, Billimoria and Marder, 2003) and extend it to a small but biologically realistic network:
the pyloric circuit of the crustacean stomatogastric ganglion (STG).

Their approach is brute-force population modelling. They build a three-cell model of the pyloric
rhythm using single-compartment Hodgkin-Huxley-style neurons drawn from a previously enumerated
1.7-million-neuron database, vary seven synaptic conductances over five or six values each, and
simulate all 20,250,000 resulting networks. Each simulated network is auto-classified by analysing
burst times against 15 pyloric-rhythm features measured from 99 lobsters. The headline result is
that **4,047,375 networks (20%)** produce a "pyloric-like" triphasic rhythm and **452,516 networks
(2.2%)** match all 15 quantitative criteria. Crucially, every one of the 150 cell-combination
configurations and the full functional range of every synaptic conductance is represented in the
matching set, with one notable exception (LP-to-PY).

The work reframes neuronal network design from "tightly tuned parameters" to "functional
performance with compensating parameter combinations" - a view that motivates homeostatic
regulation of network output rather than individual currents, and provides theoretical grounding
for studies of biological variability across animals. This paper is repeatedly cited as the
empirical-computational foundation for the "many models, one behaviour" view that informs
multi-objective optimization, robustness, and homeostatic plasticity work in compartmental
modelling today.

## Architecture, Models and Methods

The model network condenses the biological pyloric circuit (AB, two PD, one LP, five-to-eight PY)
into three single-compartment Hodgkin-Huxley neurons: a lumped AB/PD pacemaker, an LP follower, and
a single PY follower representing all PY cells. Each neuron carries eight membrane currents: fast
Na (`I_Na`), transient and slow Ca (`I_CaT`, `I_CaS`), transient K (`I_A`), Ca-dependent K
(`I_K(Ca)`), delayed-rectifier K (`I_Kd`), hyperpolarisation-activated inward (`I_H`), and leak
(`I_leak`). Voltage dependence and kinetics come from prior STG recordings and are identical across
all model neurons; only the eight maximal conductance densities differ.

The model neurons are selected from the prior 1.7M-neuron Prinz-Billimoria-Marder STG database. Five
AB/PD pacemakers are picked to span intrinsic burst periods 1.46-1.64 s with 0.5-0.75 s burst
duration and 0.3-0.4 duty cycle. Five LP and six PY follower models are selected from candidates
that are silent or slow-spiking (<11.5 Hz), have resting potential between -60 and -50 mV, and
exhibit at least five-spike rebound bursts (>=200 ms) under both weak (10 nS glutamatergic) and
strong (100 nS glutamatergic + 100 nS cholinergic) inhibition. LP and PY are distinguished by
post-inhibitory rebound delay: LP <250 ms versus PY 300-500 ms. Maximal conductance values for the
16 selected neurons are listed in Table 2 of the paper (e.g., AB/PD #1: gNa=400, gCaT=2.5, gCaS=6,
gA=50, gK(Ca)=10, gKd=100, gH=0.01, gleak=0.00 mS/cm^2).

Synapses follow the standard Abbott-Marder kinetic form `I_s = g_s * s * (V_post - E_s)`, with a
sigmoidal activation and exponential deactivation. Glutamatergic synapses use `E_s = -70 mV` and
`k- = 1/40 ms`; cholinergic use `E_s = -80 mV` and `k- = 1/100 ms`; both share `V_th = -35 mV` and
`Delta = 5 mV`. Seven synapses are varied independently across {0, 3, 10, 30, 100} nS, except
synapses targeting PY which extend down to 1 nS, giving a total of **20,250,000 networks**
(5^6 x 6^4 in the paper notation, accounting for 5 AB/PD, 5 LP, and 6 PY model neuron pools).
Numerical integration uses an exponential Euler scheme; networks run 3 s to settle then classify in
1-second epochs. The full simulation campaign ran on a Beowulf cluster of 1.2-GHz processors over
several months and produced approximately 4 GB of output data.

Pyloric-like rhythms are defined by burst-order rules (LP starts and ends before PY; AB/PD ends
before LP starts). Pyloric rhythms additionally require all 15 features to fall within mean +/-2
s.d. ranges measured from 99 Homarus americanus preparations (Table 1: cycle period 0.952-2.067 s;
PD burst duration 0.317-0.847 s; LP duty cycle 0.146-0.383; etc.).

## Results

* **20,250,000** networks simulated, with **4,047,375 (20%)** producing pyloric-like triphasic
  output and **452,516 (2.2%)** matching all 15 experimental criteria for true pyloric rhythm.
* **All 150** cell-triple combinations (5 AB/PD x 5 LP x 6 PY) produce at least some pyloric
  rhythms, indicating no obligatory cell tuning.
* Six of seven synaptic conductances span the full **0-100 nS** functional range in pyloric
  networks - strengths can vary by **two orders of magnitude** without breaking pyloric output.
* The lone exception is the LP-to-PY synapse: it exceeds 3 nS in only **0.1%** of pyloric networks
  and never exceeds 30 nS, identifying it as the single critical synaptic constraint and matching
  the biologically observed weak LP-to-PY connection (Miller and Selverston, 1982).
* Burst-period control is dominated by the AB/PD pacemaker: fast (n=534), medium (n=633) and slow
  (n=207) pyloric subsets pull from different AB/PD identities while LP and PY identities remain
  uniformly represented across speed bins.
* Networks with widely differing maximal conductances - for example two pyloric model networks in
  Figure 5 whose conductances differ by **at least a factor of three** in every channel - produce
  visually indistinguishable rhythms.
* Even in the narrow within-10% subsets of the fast/medium/slow groups, most synaptic conductance
  distributions still span the full functional range, showing that even tightly defined output does
  not require tightly tuned parameters.
* Specific connectivity patterns recover known biology: AB/PD-to-LP connections favour strong
  glutamatergic + weak cholinergic, AB/PD-to-PY favour weak glutamatergic + strong cholinergic, and
  PY-to-LP synapses prefer strong values (Figure 6c) - all consistent with prior STG measurements.

## Innovations

### Brute-force Population Modelling at Network Scale

The paper extends Prinz, Billimoria and Marder's 2003 single-neuron-database approach to networks
by enumerating 20.25 million combinations rather than fitting a single best parameter set. This is
the first systematic full-coverage demonstration that the parameter-to-behaviour map is many-to-one
at the network level, not just at the single-neuron level.

### Biologically Calibrated 15-Feature Acceptance Criterion

Rather than reporting a single composite score, the authors define functional output as
simultaneous satisfaction of 15 separate burst-timing measures, each within mean +/- 2 s.d. of
empirical lobster recordings. This anticipates modern multi-objective evaluation and provides a
template for "is this rhythm biologically realistic" tests still cited by STG modelling work today.

### Identification of Solution Manifolds, Not Solution Points

The paper reframes neuronal-network parameterisation: instead of one optimal parameter point, there
is a high-dimensional manifold of equally functional configurations. This is the conceptual
foundation cited by later degeneracy, robustness, and homeostatic compensation work (e.g.,
Marder-Goaillard 2006 review).

### Degeneracy with One Privileged Parameter

By showing that 6 of 7 synapses are unconstrained but LP-to-PY must be weak, the paper distinguishes
"truly redundant" parameters from "few critical bottleneck" parameters within the same network - a
distinction that motivates sensitivity-aware multi-objective optimization in later work.

## Datasets

* **Pyloric rhythm recordings from 99 Homarus americanus** (lobster) preparations under control
  conditions, used to derive the 15-feature acceptance ranges (Table 1). Listed as unpublished data
  by D. Bucher, A. A. Prinz and E. Marder.
* **STG model-neuron database**: ~1.7 million single-compartment STG model neurons from Prinz,
  Billimoria and Marder, J. Neurophysiol. 90:3998-4015 (2003), the source pool from which the 16
  network neurons (5 AB/PD, 5 LP, 6 PY) were drawn.
* **Pyloric network database**: the 20,250,000 simulated networks with classification labels
  (pyloric / pyloric-like / other) and ~4 GB of output traces. The paper does not provide a public
  download link for this database; subsequent literature treats the population-modelling protocol
  rather than the raw output traces as the reusable artefact.

## Main Ideas

* Network function is a property of the parameter manifold, not of a single optimal point: any
  multi-objective optimization run for direction-selective RGC models should expect a high-volume
  Pareto front rather than a tight optimum, and report manifold structure (volume, spread, principal
  axes) alongside best-objective values.
* Degeneracy is the rule, not the exception: tasks like t0097 should treat the existence of many
  near-optimal parameter sets as the expected and biologically meaningful result, and use
  population-level diagnostics (e.g., NSGA-II population spread, ensemble variance) to characterise
  it instead of collapsing to a single "winner".
* Identify privileged parameters explicitly: the LP-to-PY result shows that within a generally
  degenerate space there can be a small number of tightly constrained dimensions. Multi-objective
  optimisation should report which conductances or synaptic densities are tightly constrained across
  the Pareto front versus which are free, since the former are the biologically meaningful targets.
* Biological-feature acceptance criteria should be multi-dimensional: matching a single summary
  metric (mean firing rate, peak EPSP) is insufficient. The 15-feature template here motivates
  multi-objective evaluation using simultaneous burst-timing, amplitude, and tuning-curve features
  - directly applicable to t0097's catalogue of objectives for direction-selective ganglion cells.
* Homeostatic and developmental plasticity targets network output rather than individual
  conductances: this argues against fitting individual-channel densities to single literature point
  estimates and instead encourages varying them within biologically observed ranges to find any
  combination that matches target output.

## Summary

Prinz, Bucher and Marder ask how tightly neuronal properties and synaptic strengths must be tuned
to produce a specific network output. They focus on the crustacean pyloric rhythm because its
connectivity, neurons, and motor pattern are unusually well characterised. The motivation is to
test the implicit assumption underlying much of neurophysiology, that animal-to-animal variability
is "experimental noise" rather than a structural feature of the nervous system. The hypothesis is
that, just as similar single-neuron firing can arise from many channel-density combinations, similar
network output can arise from many cellular and synaptic parameter combinations.

Methodologically, they enumerate 20,250,000 three-neuron model networks built from a 16-neuron pool
selected from a prior 1.7-million-neuron STG database, varying seven synaptic conductances across
five or six values. Each network is simulated, auto-classified, and tested against 15 burst-timing
features measured from 99 Homarus americanus pyloric recordings. The model uses standard
Hodgkin-Huxley dynamics with eight membrane currents per cell and Abbott-Marder synapse kinetics.
The full simulation ran for several months on a Beowulf cluster of 1.2-GHz processors and produced
approximately 4 GB of classification output.

The headline finding is that 2.2% (452,516) of all networks satisfy the strict 15-feature pyloric
criterion, every cell-combination is represented in this set, and six of the seven synaptic
conductances span the full 0-100 nS range. Only LP-to-PY is tightly constrained (>3 nS in just
0.1% of pyloric networks), matching its weak biological strength. Networks with conductances
differing by factors of three or more produce visually indistinguishable rhythms. Burst period is
controlled mainly by the AB/PD pacemaker identity, while LP and PY identity is essentially free.

For the t0097 multi-objective optimization catalogue this paper anchors the biological plausibility
and degeneracy objective. It directly motivates: (i) treating the optimization output as a Pareto
manifold rather than a point, (ii) using multi-feature biological acceptance criteria with explicit
mean +/- 2 s.d. bands instead of single-objective fitting, (iii) reporting which conductances
remain unconstrained and which are tightly bottlenecked across the Pareto front, and (iv)
interpreting variability across the recovered solution set as a biologically meaningful prediction
about animal-to-animal heterogeneity in direction-selective retinal ganglion cells, not as
optimization noise. Combined with the Marder-Goaillard 2006 review (already in this task as
nrn1949), Prinz2004 grounds the t0097 robustness analysis in the canonical "many disparate
parameter sets, one functional output" result.
