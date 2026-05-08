---
spec_version: "3"
paper_id: "10.3389_fninf.2016.00017"
citation_key: "VanGeit2016"
summarized_by_task: "t0097_multi_obj_optim"
date_summarized: "2026-05-08"
---

# BluePyOpt: Leveraging Open Source Software and Cloud Infrastructure to Optimise Model Parameters in Neuroscience

## Metadata

* **File**: `files/vangeit_2016_bluepyopt.pdf`
* **Published**: 2016-06-07
* **Authors**: Werner Van Geit 🇨🇭, Michael Gevaert 🇨🇭, Giuseppe Chindemi 🇨🇭, Christian Rössert 🇨🇭,
  Jean-Denis Courcol 🇨🇭, Eilif B. Muller 🇨🇭, Felix Schürmann 🇨🇭, Idan Segev 🇮🇱,
  Henry Markram 🇨🇭
* **Venue**: Frontiers in Neuroinformatics
* **DOI**: `10.3389/fninf.2016.00017`

## Abstract

At many scales in neuroscience, appropriate mathematical models take the form of complex dynamical
systems. Parameterizing such models to conform to the multitude of available experimental
constraints is a global non-linear optimisation problem with a complex fitness landscape, requiring
numerical techniques to find suitable approximate solutions. Stochastic optimisation approaches,
such as evolutionary algorithms, have been shown to be effective, but often the setting up of such
optimisations and the choice of a specific search algorithm and its parameters is non-trivial,
requiring domain-specific expertise. Here we describe BluePyOpt, a Python package targeted at the
broad neuroscience community to simplify this task. BluePyOpt is an extensible framework for
data-driven model parameter optimisation that wraps and standardizes several existing open-source
tools. It simplifies the task of creating and sharing these optimisations, and the associated
techniques and knowledge. This is achieved by abstracting the optimisation and evaluation tasks
into various reusable and flexible discrete elements according to established best-practices.
Further, BluePyOpt provides methods for setting up both small- and large-scale optimisations on a
variety of platforms, ranging from laptops to Linux clusters and cloud-based compute
infrastructures. The versatility of the BluePyOpt framework is demonstrated by working through
three representative neuroscience specific use cases.

## Overview

BluePyOpt is the Blue Brain Project's open-source Python framework for parameter optimisation of
neuroscience models. The paper is a Technology Report rather than a methods paper: it does not
introduce a new algorithm but instead packages and standardises the multi-objective evolutionary
optimisation pipeline that the Blue Brain Project had refined over a decade (Druckmann et al. 2007,
Hay et al. 2011, Markram et al. 2015). Its central contribution is an object-oriented API
(`Optimisation`, `Evaluator`, `CellModel`, `Protocol`, `Stimulus`, `Recording`, `Response`,
`ObjectivesCalculator`, `eFeature`) that decouples the search algorithm from the simulator from the
fitness function, so the same code can target a single-compartment Hodgkin-Huxley toy, a
morphologically detailed L5 pyramidal cell, or a non-electrophysiological STDP synaptic plasticity
model.

The framework leverages DEAP for the evolutionary algorithms (notably IBEA and NSGA-II), NEURON as
the default simulator backend, and the eFEL library for extracting comparable features from voltage
traces. It adds infrastructure-as-code via Ansible playbooks that automate setting up identical
compute environments on laptops, university clusters, or AWS, addressing one of the most common
practical barriers to running multi-objective optimisations at scale.

The paper demonstrates BluePyOpt on three use cases of increasing complexity. The first fits two
Hodgkin-Huxley conductances to a target spike count in a single compartment. The second reproduces
the published L5PC model with 18 free parameters (mostly maximal channel conductances plus calcium
dynamics) by matching 31 eFeatures from in vitro patch-clamp recordings. The third optimises a
calcium-based spike-timing-dependent plasticity (STDP) model to match Nevian and Sakmann (2006)
LTP/LTD curves, demonstrating that the framework generalises beyond electrophysiology. Across all
three cases the optimisations converge to multiple non-unique solutions, which the authors take as
biologically plausible since Nature itself supports degenerate solutions for any given phenotype.

## Architecture, Models and Methods

The BluePyOpt class hierarchy splits the optimisation problem into a generic search layer and an
electrophysiology-specific (`ephys`) abstraction layer. At the top, an `Evaluator` maps a parameter
vector to a list of objectives, and an `Optimisation` runs a search algorithm against the
`Evaluator`. The principal subclass is `IBEADEAPOptimisation`, which wraps DEAP's
Indicator-Based Evolutionary Algorithm (IBEA, Bleuler/Zitzler 2003) which is a Blue Brain custom
port from C to Python. DEAP also exposes NSGA-II (Deb et al. 2002), CMA-ES, and Particle Swarm;
switching algorithms requires only a constructor change.

The `ephys` layer provides classes for `CellModel`, `Morphology` (e.g., `NrnFileMorphology`),
`Mechanism` (e.g., `NrnMODMechanism` wrapping a NEURON NMODL SUFFIX), `Parameter` (with `frozen`
and `bounds` attributes and optional `NrnDistanceScaler` for distance-dependent ion-channel
distributions), `Location` (e.g., `NrnSeclistLocation`, `NrnSomaDistanceCompLocation`), `Stimulus`
(e.g., `NrnSquarePulse`), `Recording` (`CompRecording`), `Protocol` (`SweepProtocol`,
`SequenceProtocol`), and `eFELFeature` plus `SingletonObjective`. A `CellEvaluator` ties together
a `CellModel`, ordered `param_names`, fitness `protocols`, and an `ObjectivesCalculator`.

Per-feature objective scoring uses the Druckmann (2007) z-score formula:
`objective = |mu_exp - f_model| / sigma_exp`, normalising heterogeneous features (mV, ms, Hz) to a
common scale. Parallelisation is delegated to a user-supplied `map` function which can be Python
`map`, `multiprocessing.map`, SCOOP (ZeroMQ-based, recommended for clusters), MPI4Py, or
ipyparallel. Cloud deployment uses Ansible playbooks for local Vagrant, shared-filesystem
clusters, and AWS.

The L5PC use case has 18 optimised parameters (Table 1) including conductances for NaTs2_t,
SKv3_1, Im, NaTa_t, Nap_Et2, K_Pst, K_Tst, SK_E2, Ca_HVA, Ca_LVAst, plus CaDynamics_E2 gamma and
decay; the apical Ih conductance is exponentially scaled with somatic distance using
`-0.8696 + 2.087 * exp(0.0031 * d)`. The STDP example has 9 parameters of the Graupner-Brunel 2012
calcium-based bistable synapse model.

## Results

* Use case 1 (single-compartment HH): 2 free parameters (gnabar, gkbar), 2 objectives (Spikecount
  for two step amplitudes), IBEA with **offspring size 100, 10 generations**, finishes in
  **approximately 4 minutes on a single 2.9 GHz Intel Core i5 core**, finds multiple individuals
  with **objective sum = 0**.
* Use case 2 (L5PC): 18 free parameters and **31 eFeatures** across 4 protocols (3 step currents
  plus a back-propagating AP protocol), IBEA with **100 individuals over 100 generations**,
  parallelised over **50 Intel Xeon 2.60 GHz cores via SCOOP**, runs in **about 4 hours**, target
  was **all objectives within ~3 standard deviations** of experimental mean, top-10 hall-of-fame
  solutions all meet target.
* L5PC optimisation recovers a **diverse non-unique set** of acceptable parameter vectors (Figure
  6C); the optimised model matches the Markram-2015 reference model under Gaussian noise current
  injection it was not trained on.
* Use case 3 (STDP): 9-parameter Graupner-Brunel calcium synapse model fitted to Nevian and Sakmann
  (2006) LTP/LTD data, IBEA with **max_ngen = 200**, models reproduce LTD peak at
  **Δt = -50 ms** and LTP peak at **Δt = +10 ms** within experimental SEM and predict
  missing data points.
* Across all three use cases, BluePyOpt's IBEA recovers **multiple distinct individuals** that
  satisfy the objectives, supporting the biological-degeneracy interpretation.

## Innovations

### Object-Oriented API for Multi-Objective Neuron Optimisation

The `Optimisation`/`Evaluator`/`CellModel`/`Protocol`/`Stimulus`/`Recording`/`Response`/
`ObjectivesCalculator`/`eFeature` class set encodes the multi-objective neuron-fitting workflow as
reusable Python objects. This is the pattern the Blue Brain Project, Allen Institute, EBRAINS, and
many independent labs have since adopted as the de-facto convention for biophysical neuron model
optimisation.

### Distance-Scaled Range Parameters

`NrnRangeParameter` combined with a `NrnDistanceScaler` allows arbitrary user-supplied
distance-from-soma expressions to be evaluated per morphological segment, supporting non-uniform
ion-channel gradients (e.g., apical Ih) without manual loops over sections. This is essential for
detailed pyramidal-cell models.

### IBEA in DEAP

The authors ported the Blue Brain C IBEA implementation into the DEAP Python ecosystem so it can
sit alongside NSGA-II, CMA-ES, and Particle Swarm. They report IBEA has consistently outperformed
NSGA-II on Blue Brain neuron-fitting problems (Schmücker 2010), making it the recommended default.

### Ansible-Based Cloud Provisioning

Ships Ansible playbooks for Vagrant, shared-FS clusters, and AWS that recreate identical software
environments from textual descriptions, reducing the configuration overhead of cluster/cloud
optimisation runs to a single SSH-driven command. This is unusual for an academic neuroscience
tool and was a deliberate engineering investment.

### Domain-Independent Evaluator Class

By decoupling `Evaluator` from `CellModel`, the same optimisation engine can fit
non-electrophysiological models. The STDP use case demonstrates this with a pure-Python analytical
synaptic-plasticity model that never invokes NEURON.

## Datasets

* **L5PC reference model parameters**: from Markram et al. (2015), available via the Neocortical
  Microcircuit Collaboration Portal (Ramaswamy et al. 2015).
* **L5PC eFeatures**: 31 features per cell extracted from in vitro patch-clamp recordings of layer
  5 pyramidal cells (mean and standard deviation per feature; see paper Table 2).
* **bAP target values**: from Larkum et al. (2001), used as targets for backpropagating-AP feature
  amplitudes at 660 µm and 800 µm dendritic distances.
* **STDP experimental data**: digitised LTP/LTD curves from Nevian and Sakmann (2006) (digitisation
  via Rohatgi 2015), packaged in the BluePyOpt example module `stdputil.load_neviansakmann()`.
* **Source code and example scripts**: BluePyOpt itself plus all three use-case scripts are
  released under LGPLv3 at `https://github.com/BlueBrain/BluePyOpt`. Documentation and Ansible
  cloud scripts are released under BSD.

## Main Ideas

* For this project's optimisation stage (t0097), BluePyOpt is the **canonical adoption target**:
  use `CellEvaluator` plus `Protocol`/`Stimulus`/`Recording`/`eFELFeature`/`SingletonObjective` to
  encode the angle-to-AP-frequency tuning curve target as a multi-objective problem, then call
  `IBEADEAPOptimisation` (or `NSGA-II` from DEAP) with `offspring_size=100` and tune `max_ngen`
  to the available compute budget.
* The Druckmann z-score `|mu_exp - f_model| / sigma_exp` is the recommended objective form for
  combining heterogeneous features (DSI, AP frequency, EPSP amplitude, IPSP amplitude) on a common
  scale; this also gives a natural "within 3 SD" acceptance threshold for solutions.
* The L5PC use case sets a reasonable expectation for compute cost on a problem of similar
  complexity to a DSGC: **18 parameters, 31 features, ~50 cores for ~4 hours = ~200 CPU-hours per
  optimisation run**. This is a useful upper bound for budgeting our own runs.
* Solutions are expected to be **non-unique**; BluePyOpt's hall-of-fame and Pareto-front output
  should be examined as a population, not collapsed to a single best individual. Aligns with this
  project's interest in identifying multiple electrophysiologically distinct DSGC parameter
  regimes.
* Use BluePyOpt's `NrnRangeParameter` plus `NrnDistanceScaler` for any morphology-dependent
  channel distributions in the DSGC dendritic-conductance follow-ups (e.g., distal vs proximal
  dendritic Na/K gradients).

## Summary

This Technology Report introduces BluePyOpt, a Python package developed at the Blue Brain Project
to standardise the multi-objective evolutionary optimisation of neuroscience models. The
motivation is that while stochastic search methods like genetic algorithms and CMA-ES have proven
effective for fitting compartmental neuron models, configuring them correctly remains a domain
expertise problem that excludes most neuroscientists from the technique. BluePyOpt addresses this
by providing a reusable object-oriented API and turn-key cloud-deployment scripts, lowering the
barrier so that a working optimisation can be expressed in a short Python script.

The framework wraps DEAP for the evolutionary algorithms (IBEA, NSGA-II, CMA-ES, PSO), NEURON for
electrophysiological simulation, and eFEL for feature extraction. Its core abstraction is a clean
separation between an `Optimisation` (the search algorithm), an `Evaluator` (the parameter-to-
objective mapping), and an `ephys` model layer (`CellModel`, `Morphology`, `Mechanism`, `Protocol`,
`Stimulus`, `Recording`, `eFELFeature`, `SingletonObjective`, `ObjectivesCalculator`). Distance-
dependent ion-channel distributions, parameter freezing, holding currents, and back-propagating-
AP protocols are all first-class API objects. Parallelisation is handled by user-supplied `map`
functions (Python, multiprocessing, SCOOP, MPI4Py); Ansible playbooks automate AWS, Vagrant, and
cluster deployment.

The paper validates the framework on three representative use cases. A single-compartment
Hodgkin-Huxley fit converges in 4 minutes on one CPU. A 18-parameter, 31-feature optimisation of
a layer-5 pyramidal cell reproduces the published Markram et al. 2015 model in approximately 4
hours on 50 cores, recovering a diverse hall-of-fame of equally good solutions. A 9-parameter
calcium-based STDP model is fit to LTP/LTD curves from Nevian and Sakmann (2006), demonstrating
that the framework is not restricted to voltage-trace fitting.

For this project, BluePyOpt is the methodology backbone of the parameter-optimisation work. The
paper is the canonical citation for the project's chosen optimisation toolchain, sitting
alongside Druckmann et al. (2007) and Hay et al. (2011) as the methodological core. It directly
specifies the recommended adoption pattern: encode each project objective (DSI matching, target
firing rates, EPSP/IPSP amplitudes) as an `eFELFeature` plus `SingletonObjective`, package the
model as a `CellModel` with `Protocol` per stimulus condition, and run IBEA or NSGA-II via DEAP.
The L5PC compute budget and the reported non-uniqueness of solutions also set practical
expectations for this project's own optimisation runs and for how to interpret their output as a
population of electrophysiological regimes rather than a single best individual.
