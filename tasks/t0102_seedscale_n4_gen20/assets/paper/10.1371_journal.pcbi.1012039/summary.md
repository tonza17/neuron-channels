---
spec_version: "3"
paper_id: "10.1371_journal.pcbi.1012039"
citation_key: "Mohacsi2024"
summarized_by_task: "t0102_seedscale_n4_gen20"
date_summarized: "2026-05-11"
---
# Evaluation and comparison of methods for neuronal parameter optimization using the Neuroptimus software framework

## Metadata

* File: `files/mohacsi_2024_neuroptimus-benchmark.pdf`
* Published: 2024-12-23
* Authors: Mate Mohacsi HU, Mark Patrik Torok HU, Sara Saray HU, Luca Tar HU, Gabor Farkas HU,
  Szabolcs Kali HU
* Venue: PLOS Computational Biology (2024)
* DOI: `10.1371/journal.pcbi.1012039`

## Abstract

Finding optimal parameters for detailed neuronal models is a ubiquitous challenge in neuroscientific
research. In recent years, manual model tuning has been gradually replaced by automated parameter
search using a variety of different tools and methods. However, using most of these software tools
and choosing the most appropriate algorithm for a given optimization task require substantial
technical expertise, which prevents the majority of researchers from using these methods
effectively. To address these issues, we developed a generic platform (called Neuroptimus) that
allows users to set up neural parameter optimization tasks via a graphical interface, and to solve
these tasks using a wide selection of state-of-the-art parameter search methods implemented by five
different Python packages. Neuroptimus also offers several features to support more advanced usage,
including the ability to run most algorithms in parallel, which allows it to take advantage of
high-performance computing architectures. We used the common interface provided by Neuroptimus to
conduct a detailed comparison of more than twenty different algorithms (and implementations) on six
distinct benchmarks that represent typical scenarios in neuronal parameter search. We quantified the
performance of the algorithms in terms of the best solutions found and in terms of convergence
speed. We identified several algorithms, including covariance matrix adaptation evolution strategy
and particle swarm optimization, that consistently, without any fine-tuning, found good solutions in
all of our use cases. By contrast, some other algorithms including all local search methods provided
good solutions only for the simplest use cases, and failed completely on more complex problems. We
also demonstrate the versatility of Neuroptimus by applying it to an additional use case that
involves tuning the parameters of a subcellular model of biochemical pathways. Finally, we created
an online database that allows uploading, querying and analyzing the results of optimization runs
performed by Neuroptimus, which enables all researchers to update and extend the current
benchmarking study. The tools and analysis we provide should aid members of the neuroscience
community to apply parameter search methods more effectively in their research.

## Overview

Mohacsi et al. present Neuroptimus, an open-source Python framework that gives users a single GUI-
and CLI-driven interface to more than twenty parameter search algorithms drawn from five Python
packages (SciPy, Inspyred, Pygmo, BluePyOpt, and a parallelised Cmaes implementation). Neuroptimus
is the successor of the authors earlier Optimizer tool and is targeted at single-cell biophysical
modelling in NEURON, but the same framework can wrap any black-box model that reads parameters from
a text file and writes outputs that can be scored. The bulk of the paper is a systematic
benchmarking study that uses this common interface to compare more than 20 distinct algorithms (and
three implementations each for CMAES, PSO and NSGA-II) under matched conditions on six neuronal
optimisation problems.

The benchmark is unusually well controlled: every algorithm is given exactly 10000 model
evaluations, all population-based algorithms use population size 100 and 100 generations, and every
algorithm is run 10 times with different random seeds on every problem. Performance is quantified
both as final error and as area-under-the-cumulative-minimum-error curve (convergence speed). The
use cases span the entire range of neuronal modelling complexity: single-compartment Hodgkin-Huxley
with 3 parameters, simulated voltage-clamp synaptic fitting with 4 parameters, a morphologically
detailed passive cell with 3 parameters, a simplified 6-compartment active model with 9 somatic
conductances, an adaptive exponential integrate-and-fire model with 10 parameters, and a fully
detailed CA1 pyramidal cell with 12 conductance-density and kinetic parameters. A seventh use case
applies the framework to a 12-parameter biochemical pathway model.

The headline finding is that algorithm choice matters enormously: the gap between the best- and
worst-performing methods spans two orders of magnitude on the harder benchmarks. Two
single-objective metaheuristics, CMAES and PSO, win essentially every test, with IBEA leading among
multi-objective algorithms. NSGA-II - in any of its three implementations (Inspyred, Pygmo,
BluePyOpt) - sits in the middle of the multi-objective ranking, well behind IBEA on the harder use
cases and behind random search on the simplest use case. Local search methods (Nelder-Mead,
L-BFGS-B, basinhopping) only work on the simplest problems and collapse on harder ones. The authors
deploy an online database (neuroptimus.koki.hu) that hosts every run from the paper so others can
extend the comparison.

## Architecture, Models and Methods

Neuroptimus itself is a Python 3 package with a PyQt5 GUI and a configuration-file-driven CLI. It
loads NEURON `.hoc` or Python models, exposes their parameters for optimisation, and supports
black-box external models via text-file IO. Cost functions are built from a library of error
components: MSE, MSE excluding spikes, derivative difference, spike count (total and within
stimulus), ISI difference, latency to first spike, AP overshoot, AP width, AHP depth.
Single-objective optimisations combine these via uniform-weighted average; multi-objective ones
treat each component as a separate objective. The same weighted average is applied at the end to
pick the single best solution among the multi-objective Pareto front.

Algorithms (incomplete list, by package): Inspyred contributes random search, CES (classic evolution
strategy), DE, PSO, NSGA-II, PAES; Pygmo contributes PSO, PSOG (generational PSO), NSPSO, DE, SADE,
XNES, CMAES, GACO (ant colony), and basinhopping; BluePyOpt contributes IBEA and NSGA-II; the Cmaes
package contributes a parallelised CMAES; SciPy contributes Nelder-Mead and L-BFGS-B. All algorithms
use the package defaults (the only exception is CEO from Inspyred, described in Methods).

The compute budget is fixed at 10000 model evaluations per run, partitioned as 100 generations of
100 individuals for hierarchical algorithms. Each algorithm runs 10 times per benchmark. Use case 1
(HH, 3 params) uses surrogate data and four error components (spike count, AP amplitude, AP width,
MSE excluding spikes), enabling both single- and multi-objective comparison. Use case 2 (voltage
clamp, 4 params: weight, delay, rise, decay) uses surrogate data with a single MSE component
(single-objective only). Use case 3 (passive multi-compartmental, 3 params: Cm, Rm, Ra) fits real
CA1 patch-clamp recordings with one MSE objective. Use case 4 (simplified 6-comp CA1, 9
conductances) fits a detailed-model target via six error components, including spike count, latency,
AP amplitude, AP width and AHP depth. Use case 5 (AdEx, 10 params, NEST simulator black-box) fits
real CA3 step responses via three error components. Use case 6 (detailed CA1, 12 params for ion
channels) fits feature distributions extracted from 66 features across 6 step-current protocols,
treating the optimisation as feature-based statistical matching. Use case 7 (biochemical model, 12
params, NEURON rxd) was run on the Neuroscience Gateway with only CES, PSO and CMAES due to per-run
cost of several minutes per model evaluation and the requirement for parallel execution. The most
expensive use case (detailed CA1) takes roughly 10 days for a serial 10000-evaluation run on the
authors compute server, but only a few hours on a single supercomputer node when the algorithm
supports parallel within-generation evaluation.

## Results

* **Compute budget is fixed at 10000 model evaluations per run** for every algorithm, with
  population-based methods using **pop=100 generations=100**, repeated **10 times with different
  seeds** per algorithm per benchmark.
* **CMAES is the overall winner**: in almost all six benchmarks it delivers the lowest final error
  after 10000 evaluations, and on Use Case 1 (HH, 3 params) it converges to the surrogate optimum
  after about **3500 evaluations** while every other algorithm fails to fully converge.
* **PSO is the consistent runner-up**: all three implementations (Inspyred, Pygmo PSO, Pygmo PSOG)
  closely track CMAES on every benchmark, and on Use Case 6 (detailed CA1, 12 params) all three PSO
  variants match CMAES on the best final error.
* **IBEA is the best multi-objective algorithm** and sits just behind PSO in the aggregate ranking;
  the authors recommend IBEA as the multi-objective method of choice.
* **NSGA-II underperforms on the simplest multi-objective benchmark (HH, 3 params)**: Inspyreds
  NSGA-II, PAES, and Pygmos NSPSO all give worse final errors than Random Search, and Inspyreds
  NSGA-II in particular is significantly worse than Pygmos and BluePyOpts NSGA-II implementations.
* **All three NSGA-II implementations (Inspyred, Pygmo, BluePyOpt) give similar results on Use Case
  4 (9 somatic conductances)** but are clearly behind CMAES, PSO and IBEA on this problem.
* **Local search methods (Nelder-Mead, L-BFGS-B, basinhopping) fail on harder problems**: they only
  beat Random Search on the simplest passive-cell benchmark (Use Case 3), and are worse than Random
  Search on Use Case 4.
* **Use Case 4 (simplified active model) shows two orders of magnitude difference** between the best
  and worst final errors, even though all algorithms used the same 10000 evaluations.
* **Use Case 6 (detailed CA1, 12 params)** is the largest benchmark in the suite: PSO (all three
  variants), CMAES (both), GACO and CEO all reach similar low errors; IBEA and NSGA-II also reach
  acceptable solutions, with **GACO providing the single best final score** on this
  highest-dimensional use case.
* **GACO (ant colony) performs better on harder benchmarks than on simpler ones**, suggesting it is
  good at finding low-error regions but less effective at fine-tuning within them.
* **XNES (Pygmo)** sometimes performs worse than Random Search, e.g. on the voltage-clamp use case;
  **PAES (Inspyred)** is also worse than Random Search and fails (errors) on Use Case 5.
* **Parallelisation matters for wall-clock time**: a non-parallel 10000-evaluation run of Use Case 6
  takes about **10 days** on their server; with parallel within-generation evaluation on a
  supercomputer node it takes only a few hours.
* **Implementation differences matter**: Inspyreds NSGA-II is significantly worse than Pygmos and
  BluePyOpts on Use Case 1, even though all three algorithms are nominally the same.

## Innovations

### Unified Benchmark across Five Python Packages

The first head-to-head comparison of more than 20 algorithms drawn from SciPy, Inspyred, Pygmo,
BluePyOpt and Cmaes under matched compute budgets, identical population and generation settings,
identical cost functions and 10 repeated runs per algorithm. Previous neuron-modelling benchmarks
compared at most 4-5 algorithms.

### Three-Implementation Cross-Check for CMAES, PSO, and NSGA-II

By testing two CMAES implementations, three PSO implementations, and three NSGA-II implementations,
the paper isolates the algorithm-vs-implementation question. The finding is that most
implementations of the same algorithm behave similarly except Inspyreds NSGA-II, which is
significantly weaker than Pygmos and BluePyOpts NSGA-II.

### Six Neuronal Use Cases Covering 3-12 Parameters

The benchmark suite is deliberately structured to span complexity: single-compartment HH (3 params),
voltage clamp synaptic (4 params), morphologically detailed passive (3 params), simplified active (9
params), AdEx integrate-and-fire (10 params), and fully detailed CA1 (12 params with spatial
gradients and feature-distribution targets). This stratification lets the authors show how algorithm
rankings change with dimensionality and problem structure.

### Live, Updateable Online Benchmark Database

The Neuroptimus web server (neuroptimus.koki.hu) accepts user uploads of optimisation runs as JSON
metadata, so the benchmark becomes a continuously updated resource rather than a one-shot paper. All
runs from the present paper are pre-loaded, and figures can be regenerated by users.

### Parallelisable CMAES

The paper integrates the standalone `cmaes` Python package into Neuroptimus specifically because
Pygmos CMAES implementation cannot be parallelised within a generation. This makes CMAES practically
usable on supercomputers for expensive models, where serial CMAES would take 10+ days per run.

## Datasets

* **Surrogate data from a single-compartment HH model** (3 parameters: g_Na, g_K, g_L) for Use Case
  1\.
* **Surrogate voltage-clamp data from a single-compartment model** with a simulated synapse (4
  parameters: weight, delay, rise time, decay time) for Use Case 2.
* **In vitro patch-clamp recordings from hippocampal CA1 pyramidal neurons** for Use Case 3 (passive
  parameters Cm, Rm, Ra; one short and one long current step).
* **Simulated voltage trace from a fully detailed CA1 pyramidal model** used as the target for the
  simplified 6-compartment model (Use Case 4, 9 somatic conductances, 6 error functions).
* **In vitro patch-clamp recordings from hippocampal CA3 pyramidal neurons** for Use Case 5 (AdEx
  model fit, 4 different current-step amplitudes, 10 model parameters).
* **In vitro feature statistics from CA1 pyramidal neurons** (66 features of 20 different types
  across 1 hyperpolarising + 5 depolarising current steps) for Use Case 6 (fully detailed CA1 model,
  12 parameters).
* **Experimental EPSP-LTP time courses** from prior work by the authors for Use Case 7 (12
  biochemical parameters; runs performed on Neuroscience Gateway).

All code (`KaliLab/neuroptimus`) is on GitHub; all optimisation runs are hosted at
neuroptimus.koki.hu under permissive terms. Documentation is at neuroptimus.readthedocs.io.

## Main Ideas

* For our 68-d NSGA-II optimisation question (t0102), this paper provides the most directly relevant
  external benchmark: it confirms that **NSGA-II at pop=100, gens=100, 10000 evaluations** is
  mid-pack on neuronal multi-objective problems and is decisively beaten by IBEA, CMAES and PSO on
  every problem with 9+ parameters. Our 68-d setting is well outside this papers hardest 12-d use
  case, so any expectation that NSGA-II should work is unsupported by this evidence; the project
  should treat the t0099-t0102 NSGA-II runs as a known-weak baseline, not as a definitive answer.
* The compute envelope used in this paper (pop=100, gens=100, 10 repeats, 10000 evals) is a
  reasonable default that the authors arrived at empirically; our t0102 pop=96 + gens=20 is roughly
  1/5 of their per-run budget for a problem with ~5x higher dimensionality, so the budget question
  is not subtle - we are several orders of magnitude under what the literature treats as standard.
* The paper finds that **algorithm choice matters more than seed/implementation choice on hard
  problems**: the gap between CMAES/PSO and NSGA-II at 9-12 parameters is roughly 2 orders of
  magnitude in final error. If our project must do multi-objective optimisation in the future, IBEA
  (BluePyOpt) is the strongest single recommendation from this benchmark.
* The papers GACO-improves-with-difficulty finding is a useful counterweight to the CMAES-is-best
  summary: ant-colony-style algorithms may be worth trying for our 68-d problem even if they are
  mid-pack at 9-12 d, because they appear to scale differently.
* Parallelisability is a practical constraint - serial CMAES takes 10 days for the hardest use case,
  parallel CMAES a few hours. For us this argues against the standalone `cmaes` package unless we
  explicitly support batch-of-100 model evaluation, which we do.

## Summary

Mohacsi et al. address a long-standing methodological gap in computational neuroscience: parameter
optimisation of biophysical neuron models is unavoidable, but the field has no agreed benchmark and
no clear answer to which algorithm to use. The authors develop Neuroptimus, an open-source PyQt5/CLI
framework that gives users uniform access to more than 20 optimisation algorithms from SciPy,
Inspyred, Pygmo, BluePyOpt and a standalone Cmaes package. The framework is targeted at NEURON-based
single-cell models but supports any black-box model via file IO.

The bulk of the paper is a controlled benchmark: each algorithm gets exactly 10000 model
evaluations, hierarchical algorithms use pop=100 and gens=100, and every algorithm is repeated 10
times per problem. The benchmark suite spans single-compartment Hodgkin-Huxley with 3 parameters,
voltage-clamp synaptic fitting with 4 parameters, morphologically detailed passive cells with 3
parameters, simplified active models with 9 parameters, an AdEx integrate-and-fire model with 10
parameters, and a fully detailed CA1 pyramidal cell with 12 parameters and feature-distribution
targets. A seventh use case applies the same framework to a 12-parameter biochemical signalling
cascade model.

The headline finding is that **CMAES dominates** every benchmark, **PSO is a close runner-up** (with
three implementations giving nearly identical results), and **IBEA is the best multi-objective
method**. **NSGA-II in any of its three implementations sits mid-pack on multi-objective problems**,
and is worse than random search on the simplest 3-parameter HH benchmark. **Local search methods
(Nelder-Mead, L-BFGS-B, basinhopping) collapse on hard problems**. The performance gap between best
and worst algorithms reaches two orders of magnitude on the simplified active model (Use Case 4).
Implementation matters less than expected within an algorithm family, with the notable exception
that Inspyreds NSGA-II is significantly weaker than Pygmos and BluePyOpts. The paper releases all
benchmark results as a live database that other researchers can extend.

For our t0102 NSGA-II work this paper is directly load-bearing evidence on the central question of
whether NSGA-II at our compute budget is likely to find good solutions on a 68-parameter problem.
The paper says no - NSGA-II is mid-pack on 9-12 parameter problems even at 10000 evaluations, and
the authors explicitly recommend CMAES, PSO or IBEA over NSGA-II for neuronal optimisation. Our
t0102 configuration (pop=96, gens=20, 1920 evaluations per seed) is roughly 1/5 of their per-run
budget on problems with ~5x higher dimensionality, so any null result we get for NSGA-II is
consistent with the published literature rather than a new finding about our problem. If the project
decides to continue multi-objective optimisation it should switch to IBEA via BluePyOpt; if it
instead moves to single-objective scalarisation, CMAES (parallelisable variant) is the clearest
evidence-based default. The papers online database also provides a forward-looking opportunity to
contribute our DSGC tuning runs as additional benchmark data.
