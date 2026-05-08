---
spec_version: "3"
paper_id: "10.1371_journal.pcbi.1000840"
citation_key: "Sengupta2010"
summarized_by_task: "t0097_multi_obj_optim"
date_summarized: "2026-05-08"
---

# Action Potential Energy Efficiency Varies Among Neuron Types in Vertebrates and Invertebrates

## Metadata

* **File**: `files/sengupta_2010_ap-energy-efficiency.pdf`
* **Published**: 2010-07-01
* **Authors**: Biswa Sengupta GB, Martin Stemmler DE, Simon B. Laughlin GB, Jeremy E. Niven GB
* **Venue**: PLOS Computational Biology 6(7): e1000840
* **DOI**: `10.1371/journal.pcbi.1000840`

## Abstract

The initiation and propagation of action potentials (APs) places high demands on the energetic
resources of neural tissue. Each AP forces ATP-driven ion pumps to work harder to restore the ionic
concentration gradients, thus consuming more energy. Here, we ask whether the ionic currents
underlying the AP can be predicted theoretically from the principle of minimum energy consumption.
A long-held supposition that APs are energetically wasteful, based on theoretical analysis of the
squid giant axon AP, has recently been overturned by studies that measured the currents
contributing to the AP in several mammalian neurons. In the single compartment models studied here,
AP energy consumption varies greatly among vertebrate and invertebrate neurons, with several
mammalian neuron models using close to the capacitive minimum of energy needed. Strikingly, energy
consumption can increase by more than ten-fold simply by changing the overlap of the Na+ and K+
currents during the AP without changing the APs shape. As a consequence, the height and width of
the AP are poor predictors of energy consumption. In the Hodgkin-Huxley model of the squid axon,
optimizing the kinetics or number of Na+ and K+ channels can whittle down the number of ATP
molecules needed for each AP by a factor of four. In contrast to the squid AP, the temporal profile
of the currents underlying APs of some mammalian neurons are nearly perfectly matched to the
optimized properties of ionic conductances so as to minimize the ATP cost.

## Overview

Sengupta and colleagues compare the per-AP metabolic cost of seven published Hodgkin-Huxley
single-compartment models drawn from the squid giant axon, a crab leg motor neuron, a mouse fast
spiking cortical interneuron, a honeybee Kenyon cell, a rat hippocampal interneuron, a rat
cerebellar granule cell, and a mouse thalamo-cortical relay neuron. Each model is driven with a
constant current to elicit repetitive firing, and the per-AP Na+ load is computed by integrating
the inward Na+ current over one period. The Na+ load is then converted to ATP cost using the 3
Na+/ATP stoichiometry of the Na+/K+ pump.

The headline finding is that the **Na+ load varies 17-fold across the seven models**, from
**1098 nC cm^-2** in the squid giant axon at 6.3 degrees C to **65 nC cm^-2** in the mouse
thalamo-cortical relay neuron, while the capacitive-minimum Na+ load (the minimum charge required
to depolarize the membrane to the AP peak) varies only 2.3-fold (98 to 56 nC cm^-2). The difference
is almost entirely accounted for by the **overlap load**: the Na+ that enters the cell while K+ is
also flowing outward, dissipating without contributing to depolarization. The overlap load is
linearly related to the total Na+ load with slope close to 1 and R^2 = 0.99.

The authors then introduce a constrained optimization procedure that simultaneously rescales five
biophysical parameters (Na+ and K+ peak conductances, Na+ activation and inactivation time
constants, and K+ activation time constant) within bounds of 30-400% of published values, subject
to the constraint that the model must continue to spike with a height-bounded AP. A gradient-free
Nelder-Mead simplex search seeds a Newton-method hill-climbing global search. After optimization
the squid Na+ load drops 4.2-fold to 263 nC cm^-2, while highly efficient models such as the mouse
thalamo-cortical neuron barely change. The optimization confirms that AP shape (height and width)
is a poor predictor of energy cost, since two APs with identical waveforms can be built from
currents differing by ~2x in Na+ load.

## Architecture, Models and Methods

The seven single-compartment Hodgkin-Huxley-type models are deterministic and ODE-based. The core
membrane equation is `Cm dv/dt = -gNa*m^3*h*(v - ENa) - gK*n^4*(v - EK) - gl*(v - El) + IDC`, where
the gating variables `m`, `h`, `n` follow first-order kinetics with steady-state targets
`m_inf(v)`, `h_inf(v)`, `n_inf(v)` and voltage-dependent time constants `tau_m(v)`, `tau_h(v)`,
`tau_n(v)`. Each time constant is multiplied by a dimensionless speed factor (`Phi_m`, `Phi_h`,
`Phi_n`) that the optimizer can tune without altering voltage dependence. Conductances per unit
area (`gNa`, `gK`) are also multiplied by scaling factors. Temperature is incorporated via a
Q10-style normalization `Q = 3^((T - T0)/10)` premultiplying every channel time constant, where T0
is the original recording temperature for that model.

Two models contain only the three baseline conductances (squid SA; rat hippocampal interneuron
RHI). The crab motor neuron CA adds an A-type K+ current; mouse fast-spiking MFS adds a
slowly-inactivating D-type K+ current; mouse thalamo-cortical relay MTCR adds a low-threshold
T-type Ca2+ current; honeybee Kenyon BK adds a second voltage-gated Na+ current plus A-type and
slow transient K+ currents; rat granule RG adds A-type, C-type and hyperpolarization-activated K+
currents plus an L-type Ca2+ current. Even in models with extra inward currents (RG, MTCR), 92-95%
of the per-AP energy is spent extruding Na+ via the Na+/K+ pump.

The optimization objective is `Q = integral_0^T I_inward(t) dt` minimized over a five-dimensional
parameter set, subject to a soft quadratic loss enforcing that AP height stays within a narrow
band of the original height. AP existence is enforced by a hard penalty: any parameter set that
fails to produce a periodic orbit (verified by linear stability analysis on the limit cycle) is
treated as the worst simplex vertex. Two complementary strategies are used: a **gradient-free
Nelder-Mead simplex** for exploration plus a **multi-start Newton-method hill climber** for
gradient-based refinement. The two strategies converge to nearly identical optima. Random search,
simulated annealing and differential evolution were tried and gave sub-optimal results. Code was
written in Wolfram Mathematica 7.0 and Matlab 2009a; numerical continuation used AUTO and MATCONT.

The energy conversion uses the Na+/K+ pump stoichiometry of 3 Na+ exported and 2 K+ imported per
ATP hydrolyzed. ATP molecules per AP per unit area = (Na+ load) * NA / (3 * F), where NA is the
Avogadro constant and F is the Faraday constant. The capacitive-minimum Na+ load is the charge
required to bring the membrane from rest to AP peak via membrane capacitance alone; AP efficiency
is reported as the percentage ratio (capacitive-minimum / total Na+ load) * 100.

## Results

* **Per-AP Na+ load spans 17-fold across the seven models**: SA = **1098 nC cm^-2**,
  CA = **364 nC cm^-2**, MFS = **315 nC cm^-2**, BK = **186 nC cm^-2**, RHI = **76 nC cm^-2**,
  RG = **72 nC cm^-2**, MTCR = **65 nC cm^-2** (Table 1, before optimization).
* **ATP cost of the squid AP is 2.3 x 10^12 ATP cm^-2**, ~17x more than the mouse thalamo-cortical
  relay AP at **1.35 x 10^11 ATP cm^-2** (Table 1).
* **AP efficiency (capacitive-minimum / total Na+ load)** ranges from **9% in the squid (6.3
  degrees C)** through **20-40% in CA, MFS, BK**, **75% in RHI**, to **~100% in RG and MTCR**.
* **Overlap load is the dominant cost component**: the linear regression of overlap load vs total
  Na+ load across all seven models has slope ~ 1 and **R^2 = 0.99 (p < 0.0001)**.
* **Na+ overlap factor (alpha = total Na+ load / capacitive minimum)** ranges from **alpha ~ 1.0**
  in MTCR (essentially perfect) and **~1.04** in RG to **alpha ~ 11.2** in the squid at 6.3
  degrees C; the Carter-Bean mouse cortical pyramidal value (cited in the discussion) is **alpha ~
  1.2**.
* **Constrained five-parameter optimization reduces the squid Na+ load 4.2-fold** from 1098 to
  **263 nC cm^-2**, and the corresponding overlap load from 1034 to **185 nC cm^-2** (Figure 5,
  Table 1).
* **Optimization improvements** (post-/pre-optimization Na+ load): SA = 24%, CA = 46% (169 vs
  364 nC cm^-2), MFS = 71% (225 vs 315), BK = 65% (121 vs 186), RHI = 78% (59 vs 76), MTCR = 100%
  (already at capacitive minimum at 65 nC cm^-2).
* **AP height ranges 55.5-129 mV (2.3-fold)**; **AP half-width ranges 0.2-2.6 ms (13-fold)**;
  height/width are not reliable predictors of energy cost (Figure 2, Figure S1).
* **Resting energy consumption is < 1.5% of per-AP cost** across all seven models, regardless of
  AP efficiency (Table S5).
* **Temperature effect on the squid model**: Na+ load drops from 1098 nC cm^-2 at 6.3 degrees C to
  331 nC cm^-2 at 18 degrees C; capacitive minimum rises slightly because the AP is taller, so
  efficiency improves from 9% to ~25%.
* **Cortex-level extrapolation**: replacing the Attwell-Laughlin (2001) squid overlap factor of 4
  with the Carter-Bean cortical alpha = 1.2 raises the supportable cortical firing rate from
  4 Hz/neuron to **6.8 Hz/neuron** (60% increase).

## Innovations

### Cross-Species Per-AP Energy Catalogue

First systematic side-by-side comparison of per-AP Na+ load and ATP cost across seven published HH
models spanning vertebrate and invertebrate cell types. The catalogue (Table 1) gives
per-cell-type calibration anchors that downstream modelers can use to sanity-check their own
per-AP energy estimates.

### Overlap Load as the Universal Cost Driver

Demonstrates with R^2 = 0.99 across seven heterogeneous models that the Na+/K+ overlap load
linearly explains the total Na+ load with slope ~ 1, formally generalizing the Hodgkin (1975)
observation from the squid axon to mammalian and insect neurons. Establishes the overlap factor
**alpha = total Na+ / capacitive minimum** as the canonical efficiency metric.

### Constrained Five-Parameter Optimization for Biophysical AP Energy

Introduces a constrained Nelder-Mead-plus-Newton optimization that varies gNa, gK, tau_m, tau_h,
tau_n simultaneously while enforcing AP existence and bounded height. Shows that the same
optimization yields qualitatively different parameter-change patterns across models (e.g. Na+
inactivation shortens in SA, CA, MFS, RHI but lengthens in BK), refuting any one-size-fits-all
rule about how to make APs cheaper. Each model sees its own local energy landscape.

### Quantitative Refutation of AP-Shape-Predicts-Cost

Demonstrates with paired examples (Figure S1) that two APs with identical height and half-width
can be produced by current pairs differing 1.76-fold in Na+ load (1275 vs 2244 nC cm^-2).
Establishes that AP shape is not a reliable predictor of energy cost across heterogeneous neuron
types, so energy must be treated as an independent objective rather than a function of waveform.

## Datasets

This is a theoretical and computational paper; no datasets were used in the empirical sense. The
seven HH models were re-implemented from previously published parameter tables in references
[9-14, 16] of the paper. Parameter tables are reproduced verbatim in the paper Supporting
Information (Table S1) and the optimized parameter sets are tabulated in Table S3. The Mathematica
and Matlab source code for the optimization is described in the Methods but is not posted as a
public repository in the article itself.

## Main Ideas

* The **per-compartment per-AP energy objective** for the t0097 catalogue is exactly the integral
  Sengupta et al. propose: `int(I_Na) dt` over one spike period, divided by 3 to convert Na+
  charge to ATP molecules via the Na+/K+ pump stoichiometry. This is the project canonical energy
  recipe and the cited authority for it.
* The **Na+ overlap factor alpha = total Na+ load / capacitive minimum** is the right
  cross-neuron normalization. Mammalian neurons sit at **alpha ~ 1.0-1.5** (this paper plus the
  Carter and Bean and Alle et al. data cited in its discussion); the squid sits near **alpha ~ 4**
  at 18 degrees C and **alpha ~ 11** at 6.3 degrees C. For a mammalian DSGC compartmental model
  the energy objective should be benchmarked against alpha ~ 1.0-1.5 per soma AP, not 4.
* **AP shape is not a reliable proxy for energy cost** so the t0097 multi-objective optimization
  must include a true integrated-Na+ energy objective rather than a shape-based surrogate (e.g.
  AP width or amplitude penalty). Otherwise the Pareto front will be biased toward solutions that
  look efficient but are not.
* **Reducing Na+ inactivation tau is the single most effective biophysical lever** for lowering
  AP energy in HH-type models, more effective than reducing channel density. This identifies
  tau_h for the somatic Na+ conductance as a high-leverage decision variable in the t0097
  parameter catalogue ranking-based (NSGA-II) Pareto search.
* **Optimal parameter changes are model-dependent** (signs and magnitudes differ across models).
  Do not impose a single make-AP-cheaper template across DSGC models with different morphologies
  or channel sets; let the optimizer discover the local valley for each configuration.
* **Resting energy is < 1.5% of per-AP energy** in all seven Sengupta models so the t0097 energy
  objective can safely use per-AP integrated `int(I_Na) dt / 3` as a proxy for total metabolic
  cost during repetitive firing without separately accounting for resting Na+ leakage, provided
  firing rates are non-trivial.

## Summary

Sengupta, Stemmler, Laughlin and Niven (2010) ask whether the per-action-potential energy cost of
biological neurons is set by waveform alone, or whether the underlying ionic currents allow large
cost differences hidden by similar AP shapes. They re-implement seven published Hodgkin-Huxley
single-compartment models spanning the squid giant axon, a crab leg motor neuron, four mammalian
neurons (mouse fast-spiking interneuron, rat hippocampal interneuron, rat cerebellar granule cell,
mouse thalamo-cortical relay) and a honeybee Kenyon cell, and compare per-AP Na+ loads on a
common, model-independent basis. The motivation is to establish a principled per-cell-type energy
metric that can serve as a bottom-up calibration anchor for cortical energy budgets and for
downstream modelers comparing their own neurons energy use to literature.

The methodology is a deterministic single-compartment HH simulation driven by constant injected
current to elicit repetitive firing, with per-AP Na+ load computed by integrating the inward Na+
current over one limit-cycle period. Cost is converted to ATP using the 3 Na+/ATP stoichiometry
of the Na+/K+ pump. The authors then introduce a five-parameter constrained optimization (gNa,
gK, tau_m, tau_h, tau_n) that combines a Nelder-Mead simplex with a Newton-method hill climber,
enforcing AP existence by a hard penalty and AP height by a soft quadratic loss. Conductances and
time constants are bounded to 30-400% of the original published values. The same optimization is
run across six of the seven models, and the changes in parameters are compared.

The headline result is that the per-AP Na+ load varies 17-fold across the seven models, while the
capacitive-minimum Na+ load varies only 2.3-fold; the difference is almost entirely the overlap
load, which has a linear correlation R^2 = 0.99 with the total Na+ load (slope ~ 1). Mammalian
neurons (RG, RHI, MTCR) operate near the capacitive minimum (efficiency ~ 75-100%, alpha ~
1.0-1.3), while the squid axon at 6.3 degrees C is profligate (efficiency 9%, alpha = 11.2).
Constrained optimization reduces the squid Na+ load 4.2-fold while leaving the mouse
thalamo-cortical neuron essentially unchanged, confirming that mammalian APs already sit close to
a local optimum. Optimized parameter changes vary qualitatively across models: each model has its
own local energy valley.

For this project, the paper is the canonical citation for the per-AP energy objective in the
t0097 multi-objective optimization catalogue. The energy recipe `int(I_Na) dt / 3` (per
compartment, per AP, in ATP molecules) is exactly what t0097 will report alongside the
angle-tuning loss as a co-objective in the NSGA-II Pareto search. The Na+ overlap factor alpha is
the natural normalized cost metric for cross-neuron comparison, and the mammalian alpha range of
1.0-1.5 calibrated here sets the realistic biological lower bound for any DSGC compartmental
model. The model-dependence of optimal parameter changes also reinforces the project preference
for a population-based ranking search (NSGA-II) over a one-shot template, since each DSGC
morphology will see a different energy landscape under the joint angle-tuning + energy objective.
