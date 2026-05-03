---
spec_version: "3"
paper_id: "10.1371_journal.pcbi.1002107"
citation_key: "Hay2011"
summarized_by_task: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_summarized: "2026-05-03"
---
# Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and Perisomatic Active Properties

## Metadata

* **File**: `files/hay_2011_l5b-pyramidal-models.pdf`
* **Published**: 2011-07-28
* **Authors**: Etay Hay 🇮🇱, Sean Hill 🇨🇭, Felix Schurmann 🇨🇭, Henry Markram
  🇨🇭, Idan Segev 🇮🇱
* **Venue**: PLoS Computational Biology 7(7): e1002107
* **DOI**: `10.1371/journal.pcbi.1002107`
* **ModelDB**: accession 139653

## Abstract

The thick-tufted layer 5b pyramidal cell extends its dendritic tree to all six layers of the
mammalian neocortex and serves as a major building block for the cortical column. L5b pyramidal
cells have been the subject of extensive experimental and modeling studies, yet conductance-based
models of these cells that faithfully reproduce both their perisomatic Na+-spiking behavior as well
as key dendritic active properties, including Ca2+ spikes and back-propagating action potentials,
are still lacking. Based on a large body of experimental recordings from both the soma and dendrites
of L5b pyramidal cells in adult rats, we characterized key features of the somatic and dendritic
firing and quantified their statistics. We used these features to constrain the density of a set of
ion channels over the soma and dendritic surface via multi-objective optimization with an
evolutionary algorithm, thus generating a set of detailed conductance-based models that faithfully
replicate the back-propagating action potential activated Ca2+ spike firing and the perisomatic
firing response to current steps, as well as the experimental variability of the properties.
Furthermore, we show a useful way to analyze model parameters with our sets of models, which enabled
us to identify some of the mechanisms responsible for the dynamic properties of L5b pyramidal cells
as well as mechanisms that are sensitive to morphological changes. This automated framework can be
used to develop a database of faithful models for other neuron types. The models we present provide
several experimentally-testable predictions and can serve as a powerful tool for theoretical
investigations of the contribution of single-cell dynamics to network activity and its computational
capabilities.

## Overview

Hay and colleagues build conductance-based, multi-compartmental models of adult-rat thick-tufted
layer 5b neocortical pyramidal cells (L5b PCs) that simultaneously reproduce two qualitatively
different active firing regimes: the perisomatic Na+ step-current response (frequency-current
relation, ISI-CV, adaptation, AP shape) and the BAP-activated Ca2+ (BAC) firing in the distal apical
dendrite. Earlier published models replicated only one regime at a time; this paper is the first to
fit both jointly, with experimentally measured variability, in detailed reconstructed morphologies.

The fitting strategy is multi-objective optimization (MOO) coupled to an elitist non-dominated
sorting evolutionary algorithm (NSGA-style), with a population of 1000 over 500 generations. The
authors define 20 firing-feature objectives (10 perisomatic, 10 BAC) computed against experimental
mean+/-SD targets, optimize 22 free parameters (mostly conductance densities of nine ion channels
plus Ca2+ buffering parameters tdecay and gamma), and accept models whose every feature falls within
2-3 SD of the experimental mean. The Ih distribution along the apical tree is fixed (not optimized)
to preserve subthreshold properties.

The headline empirical contribution is a set of about 2000 acceptable L5b PC models — published
together with their NEURON code in ModelDB (accession 139653). Crucially for downstream work, the
paper introduces the canonical Blue Brain mechanism set used by ten years of subsequent
biophysical-modeling studies: the SK_E2 small-conductance Ca2+-activated K+ channel model, the
CaDynamics_E2 sub-membrane Ca2+ buffering and decay scheme parameterized by gamma (binding ratio)
and tdecay (decay time constant), Kv3.1, Im, Ca_HVA, Ca_LVA, Nat, Nap, and a fixed Ih kinetic model.
The same MOD files were later vendored into the BluePyOpt example optimizations and, by that route,
into this project's t0074-derived AIS substrate.

The analysis half of the paper exploits the model ensemble as an experimental surrogate: by
comparing parameter ranges of acceptable BAC-firing models against those of acceptable
perisomatic-firing models, the authors identify which channel densities are necessary versus
sufficient for each regime, predict that apical Nat and apical Kv3.1 are key determinants of BAP
fidelity, and show that swapping morphologies between fitted parameter sets reveals which mechanisms
are morphology-sensitive. This "ensemble-as-experiment" protocol is itself an innovation that t0078
inherits when interpreting MOBO Pareto fronts.

## Architecture, Models and Methods

The reconstructed L5b PC morphologies are discretized into compartments at most 20 um long
(approximately 200 compartments per cell). Membrane capacitance Cm is 1 uF/cm^2 in soma and axon and
2 uF/cm^2 in basal and apical dendrites (correcting for spine area), and all dendritic conductance
densities are doubled accordingly. Axial resistance Ra = 100 ohm-cm; leak reversal ELeak = -90 mV;
ENa = +50 mV; EK = -85 mV; EIh = -45 mV. Q10 = 2.3 corrects 21 deg C kinetics to the 34 deg C
simulation temperature; channels recorded without junction-potential correction are shifted by -10
mV.

The free-parameter set (22 dimensions, Table 2) covers somatic (s.) and apical (a.) maximal
conductance densities of Nat (s: 0-40000, a: 0-200 pS/um^2), Nap (s: 0-100), Kp (s: 0-10000), Kt (s:
0-1000), Kv3.1 (s: 0-20000, a: 0-200), Ca_HVA (s: 0-10, a: 0-25 distal-zone), Ca_LVA (s: 0-100, a:
0-1000 distal-zone), SK (s: 0-1000, a: 0-50), Im (a: 0-5), plus per-compartment Ca2+ parameters
tdecay (s: 20-1000 ms, a: 20-200 ms) and gamma (s: 0.0005-0.05, a: 0.0005-0.05). Leak densities are
free in soma, basal, apical, and AIS. Axonal Nat and Kv3.1 are also tuned. Apical Ca2+ channels
follow a hot-zone distribution with elevated densities 685-885 um from soma.

All channels use Hodgkin-Huxley formalism I = g * m^x * h^y * (V - E). The SK channel uses
Ca2+-dependent activation with an instantaneous (1 ms) activation time constant — the authors flag
this as an empirical assumption due to the absence of measured kinetics. Sub-membrane Ca2+ follows
shell-buffer dynamics with shell depth d, gamma = inverse of the buffer binding ratio (fraction of
unbound Ca2+), and tdecay = exponential return-to-rest time constant (steady-state [Ca2+] = 1e-4
mM). The objective function is structured as 20 separate fitness scores, each expressed in units of
experimental SD; Pareto-non-dominated solutions are kept and the "acceptable" cutoff is all features
<= 3 SD. Optimization runs on 240-1024 cores (Sun AMD64 grid or IBM BlueGene/P at CADMOS) for 2-5
days per fit. All simulations use NEURON 7.x.

## Results

* About **2000 acceptable models** were generated across the joint perisomatic + BAC firing
  optimization and were released to ModelDB (accession 139653).
* Constraining only on BAC firing yielded **899 acceptable models**; constraining only on
  perisomatic step current firing yielded **52 acceptable models** — the latter is far more
  restrictive.
* In an example BAC-only fit, the model Ca2+ spike peak and width were within **0.86 SD** of the
  experimental mean, BAP amplitudes were within **1.4 SD**, and somatic AP ISI was within **1.1
  SD**, but the same model failed perisomatic-step targets (insufficient Na+ AP frequency and wrong
  AP shape).
* Apical Nat density of **82.5 pS/um^2** in a perisomatic-only fit was below the BAC-acceptable
  range of **101-133.5 pS/um^2**; apical Kv3.1 of **119 pS/um^2** was above the BAC-acceptable range
  of **0-3.05 pS/um^2** — directly explaining the failed BAP propagation.
* Joint BAC + perisomatic optimization recovers a model that simultaneously meets every feature
  within **2-3 SD** of experimental mean across f-I curve shape, ISI-CV, AHP depth, AP half-width,
  Ca2+ spike peak (mean **6.73 +/- 2.54 mV**) and width (**37.43 +/- 1.27 ms**), BAP amplitude at
  620 um (**45 +/- 10 mV**) and at 800 um (**36 +/- 9.33 mV**).
* For perisomatic step targets, the experimentally measured spike-frequency triplet was **9, 14.5,
  22.5 Hz** at low/reference/high current; first-spike latency dropped from **43.25 ms** to **7.25
  ms** across the range; ISI-CV decreased from **0.12** to **0.095**.
* Distal Ca2+ hot-zone densities and somatic Kv3.1 emerged as the dominant levers for BAC firing;
  somatic SK and tdecay-soma covaried with the slow AHP depth (**-58 to -60 mV**) and AHP time
  (about **0.2-0.3** in normalized units).
* Substituting a different L5b morphology into the same parameter set produced moderate but
  reproducible degradation of perisomatic features and large degradation of BAC features,
  identifying apical-tree morphology as a primary source of model brittleness.
* An axon-initiating variant of the model (Text S1, Figure S6) replicates perisomatic and BAC firing
  but is **less successful** at BAP features — establishing the perisomatic-AP-initiation
  simplification as a deliberate trade-off rather than a biophysical claim.

## Innovations

### Multi-Objective Joint Fitting of Perisomatic and Dendritic Firing

First conductance-based L5b PC model that simultaneously reproduces perisomatic step-current f-I
behavior and BAC firing with experimentally measured variability. Prior models (Schaefer et al.
2003, Kole et al. 2008, etc.) captured one regime or the other; the MOO + evolutionary algorithm
combination here recovers the full feature set jointly across an ensemble of about 2000 models.

### The SK_E2 / CaDynamics_E2 Mechanism Set

Defines the canonical Blue Brain mechanism set used in nearly every subsequent biophysical
optimization study from this lineage: the SK_E2 small-conductance Ca2+-activated K+ channel (with
its instantaneous-activation simplification), the CaDynamics_E2 sub-membrane shell model
parameterized by gamma (buffer binding ratio) and tdecay (Ca2+ decay time constant), Kv3.1, Im,
Ca_HVA, Ca_LVA, Nat, Nap, and the Kole-style Ih distribution. These MOD files are the direct
upstream source of the SK_E2 and CaDynamics_E2 vendored by t0074 and extended in t0078 with the
`tau_ca_multiplier` slow-AHP knob.

### Ensemble-as-Experiment Parameter Analysis

By comparing the union of acceptable parameter ranges from one fitting target (e.g. BAC) against a
single model fitted to the other target (e.g. perisomatic), the authors quantify which channel
densities are necessary versus sufficient for each behavior. This non-parametric analysis of the
Pareto-acceptable set is itself a methodological contribution and prefigures modern MOBO-style
analyses of optimization fronts.

### Morphology-Sensitivity Quantification

By transplanting a fitted parameter set onto an alternative reconstructed morphology, the authors
quantify which features collapse and which survive — establishing morphology-conductance
interaction as a measurable property rather than a qualitative concern.

## Datasets

The paper combines previously published in vitro patch-clamp recordings from adult rat L5b pyramidal
cells, including the dendritic recordings of Larkum, Schiller, Helmchen, Berger, Stuart, Kole, and
others (see references in the paper), with the authors' own recordings from somatic and dendritic
patch experiments on mature L5b PCs. No new dataset is introduced; the paper instead distills a
feature-statistics table (Table 1) summarizing means and SDs over multiple cells for the 10
perisomatic-firing features at three normalized current amplitudes and the 10 BAC-firing features.

The reconstructed morphologies used for the example fits are taken from earlier published L5b
reconstructions; one is morphology age p36. All approximately 2000 fitted models, the full feature
list, and the NEURON simulation code are publicly deposited in ModelDB under accession **139653**
(`https://senselab.med.yale.edu/ModelDB/showmodel?model=139653`).

## Main Ideas

* The SK_E2 and CaDynamics_E2 MOD files vendored by t0074 and inherited by t0078 originate directly
  from this paper. The slow-AHP behavior that t0078 tries to optimize via the `tau_ca_multiplier`
  parameter is governed by exactly the gamma and tdecay parameters defined and optimized in Hay 2011
  — t0078's substrate edits should preserve the kinetic conventions established here (SK
  instantaneous activation, sub-membrane shell buffering, fixed [Ca2+]_rest = 1e-4 mM).
* Multi-objective optimization with an evolutionary algorithm and per-feature SD-normalized
  objectives is the canonical pattern for parameter-rich biophysical fits; t0078's MOBO design
  inherits the same per-feature, SD-normalized scoring philosophy and similarly accepts solutions
  whose every feature lies within a small SD multiple of target.
* "Acceptable model" cutoffs at 2-3 SD plus ensemble-of-solutions reporting (rather than a single
  best fit) is standard in this lineage. t0078 should report the Pareto front and acceptable
  ensemble distribution rather than a single point estimate when the MOBO finishes.
* The 22-parameter, 20-feature optimization here required 1000-population x 500-generation runs on
  240-1024 cores for 2-5 days. This sets a realistic compute baseline against which t0078's MOBO
  budget should be sized.
* SK and CaDynamics activation-time-constant assumptions in this paper (instantaneous SK activation;
  gamma in 0.0005-0.05; tdecay in 20-1000 ms soma, 20-200 ms apical) define the prior ranges that
  t0078's tau_ca_multiplier should explore on top of the t0074 baseline.

## Summary

Hay et al. (2011) address a long-standing gap in compartmental modeling of L5b cortical pyramidal
cells: no published model simultaneously reproduced the perisomatic Na+ step-current f-I behavior
and the BAP-activated dendritic Ca2+ ("BAC") firing observed in adult-rat slice recordings. The
paper's research question is whether a single conductance-based model in a reconstructed morphology
can be fit to both regimes with experimentally measured cell-to-cell variability, and which channel
densities and Ca2+-dynamics parameters are necessary or sufficient for each regime.

Methodologically, the authors define 20 firing features (10 perisomatic, 10 BAC), each with an
experimental mean and SD computed across several cells. They use multi-objective optimization with
an elitist non-dominated sorting evolutionary algorithm — population 1000, 500 generations, 240 to
1024 CPU cores, 2-5 days runtime — to optimize 22 free parameters. The free parameters are the
maximal densities of nine ion channels (Nat, Nap, Kp, Kt, Kv3.1, Ca_HVA, Ca_LVA, SK, Im) in soma and
apical compartments, plus the Ca2+ buffer parameters gamma and tdecay. The Ih distribution is fixed
to preserve subthreshold properties. Models are accepted when every feature falls within 2-3 SD of
the experimental mean. Mechanism kinetics use Hodgkin-Huxley formalism with Q10 = 2.3 and a -10 mV
junction-potential shift where applicable.

The headline result is a set of about 2000 acceptable L5b PC models published in ModelDB (accession
139653). Single-target fits are easier (899 BAC-only, 52 perisomatic-only) but typically fail the
other target. Joint fits achieve every feature within 2-3 SD: e.g. BAP amplitude **45 +/- 10 mV** at
620 um, Ca2+ spike peak **6.73 +/- 2.54 mV**, perisomatic spike frequencies of **9 / 14.5 / 22.5
Hz**, AP half-width of **1.31 ms**, slow AHP depth around **-60 mV**. Cross-target parameter
analysis identifies apical Nat and apical Kv3.1 densities as the dominant levers controlling BAP
propagation, and shows that morphology swaps degrade BAC features more than perisomatic features.

For this project, Hay 2011 is a direct upstream dependency of t0074 and t0078: the SK_E2 and
CaDynamics_E2 MOD files vendored under t0074 originate here, and t0078's `tau_ca_multiplier`
extension to CaDynamics_E2 is an additional knob on the same gamma + tdecay sub-membrane shell
formalism defined in this paper. The cited parameter ranges (gamma in 0.0005-0.05; soma tdecay
20-1000 ms; apical tdecay 20-200 ms) provide the prior box that t0078's MOBO should explore. The
multi-objective + per-feature-SD scoring + Pareto-acceptable-ensemble methodology is also the
template t0078 inherits for reporting and analyzing its own MOBO results. Citing Hay 2011 in the
t0078 substrate documentation is therefore mandatory.
