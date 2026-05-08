---
spec_version: "3"
paper_id: "10.1371_journal.pcbi.0020094"
citation_key: "Achard2006"
summarized_by_task: "t0097_multi_obj_optim"
date_summarized: "2026-05-08"
---

# Complex Parameter Landscape for a Complex Neuron Model

## Metadata

* **File**: `files/achard_2006_complex-parameter-landscape.pdf`
* **Published**: 2006-07-21
* **Authors**: Pablo Achard BE, Erik De Schutter BE
* **Venue**: PLoS Computational Biology 2(7): e94
* **DOI**: `10.1371/journal.pcbi.0020094`

## Abstract

The electrical activity of a neuron is strongly dependent on the ionic channels present in its
membrane. Modifying the maximal conductances from these channels can have a dramatic impact on
neuron behavior. But the effect of such modifications can also be cancelled out by compensatory
mechanisms among different channels. We used an evolution strategy with a fitness function based on
phase-plane analysis to obtain 20 very different computational models of the cerebellar Purkinje
cell. All these models produced very similar outputs to current injections, including tiny details
of the complex firing pattern. These models were not completely isolated in the parameter space,
but neither did they belong to a large continuum of good models that would exist if weak
compensations between channels were sufficient. The parameter landscape of good models can best be
described as a set of loosely connected hyperplanes. Our method is efficient in finding good models
in this complex landscape. Unraveling the landscape is an important step towards the understanding
of functional homeostasis of neurons.

## Overview

Achard and De Schutter address whether a richly active compartmental neuron, the cerebellar
Purkinje cell (PC), admits multiple distinct sets of channel conductances that all reproduce its
detailed electrophysiology. Their target "data" is the De Schutter and Bower 1994 PM9 PC model -- a
1,600-compartment cell with ten distinct voltage- and calcium-gated channel species and four
morphological zones (soma, main dendrite, smooth dendrites, spiny dendrites), giving 24 free
maximum conductance densities. The cell exhibits four firing modes (silent, tonic spiking, short
bursts, long bursts) depending on injected current, and the authors require new models to reproduce
not just the qualitative mode but the fine waveform of every spike and burst.

The methodological core is an evolution strategy (ES), specifically a (57+19) self-adaptive ES with
correlated Gaussian mutations and global-intermediary recombination, paired with a phase-plane
fitness function originally proposed by LeMasson and Maex. The fitness compares the (V, dV/dt)
density matrix between a candidate model and the data, summed across seven current injection
amplitudes, three recording sites, and two time windows (transitory and stable). After nine
independent runs of approximately 8,000 evaluations each (415 generations, 6 days on a 10-node
Apple G5 cluster), they retain 20 models with fitness 2.58 to 3.45.

The headline finding is that these 20 models are simultaneously diverse and constrained: individual
conductance densities span their entire allowed range for some channels (e.g., gCaTm, gKAm, gKMd,
gKhs) yet remain tightly bounded for others (gNaFs, gCaPd, gKdrs, gKdrm). Crucially, the geometry
of the "good" region in parameter space is neither a single connected blob nor a set of isolated
points, but a collection of loosely connected hyperplanes -- thin lower-dimensional manifolds that
a 6- or 10-points-per-dimension grid search would miss for ~65% of the recovered solutions. This
establishes that compensation among channels is real, multidimensional, and structured, which has
direct implications for any project that uses gradient-free or population-based search to fit
biophysical models.

## Architecture, Models and Methods

The cell model is the published 1,600-compartment Purkinje cell "PM9" of De Schutter and Bower
(1994), simulated in Genesis 2.2.1. Channel distribution: soma carries NaF, NaP, CaT, Kdr, Kh, KM,
KA; smooth and spiny dendrites carry CaP, CaT, KM, KC, K2; the main dendrite additionally carries
Kdr and KA. Per-zone densities give 24 free parameters, all simultaneously released to the search.
Lower and upper bounds (mS/cm^2) defining the search hypercube are given in Table 1 of the paper:
gNaFs in **50,000-100,000** with data **75,000**; gNaPs in **3-30** with data **10**; gCaTs/m/t/d
in **1-20** with data **5**; gCaPm/t/d in **10-100** with data **45**; gKAs in **50-500** (data
**150**), gKAm in **3-60** (data **20**); gKdrs in **2,000-10,000** (data **6,000**), gKdrm in
**200-1,000** (data **600**); gKM coefficients spanning **0-3** for soma, **0-1** for main and
distal compartments; gKCm/t/d in **200-2,000** (data **800**); gK2m/t/d in **0.5-10** (data
**3.9**); gKhs in **0.5-10** (data **3**).

The ES strategy is (57+19): each of nine independent runs maintains a population of 57 individuals
producing 19 offspring per generation, with parents and offspring competing for the next
generation. Mutation is performed by adding Gaussian noise whose standard deviations and
correlation matrix are themselves part of the genome and evolve under selection (self-adaptive
correlated mutation, Eiben and Smith 2003). Recombination uses "global intermediary" averaging:
two random parents per parameter, offspring inherits the mean. Each run was stopped after 415
generations (~8,000 evaluations).

The phase-plane fitness builds a 100x100 (V, dV/dt) histogram with V from -80 to +120 mV and dV/dt
from -1500 to +2500 mV/ms, sampled at 50 kHz. The squared L2 distance between normalized data and
model histograms is computed (equation 1), and the overall fitness F sums weighted square roots
across seven current amplitudes (1.5 nA dendritic, 0, 0.5, 1, 1.5, 2.5, 3 nA somatic), three
recording sites (soma plus two thick dendrites with weights 1 vs 0.5, dropping to 0.6 and 0.3 at
zero current) and two time windows (first 100 ms transitory, >=1 s stable). The threshold for
"good" was fitness <= 3.45; 23 individuals passed; 3 were excluded for failing to spike at 0.25 nA
somatic injection, leaving the final 20.

Compute used a parallel ESEA (Evolving Objects library) on 10 dual-G5 nodes; 6 days per run.
Hyperplane analysis defines linear combinations of solution triplets with weights running from
-1.5 to +2.5 in steps of 0.04 (third weight chosen so weights sum to 1), yielding thousands of
points per hyperplane. Grid-search comparison uses 6 and 10 points per dimension (so 6^24 ~ 4.7e18
and 10^24 grid points, neither remotely tractable in 2006).

## Results

* The ES recovered **20 selected good models** from 9 runs of ~8,000 evaluations each, with fitness
  values in the range **2.58 to 3.45** (the threshold for selection).
* Total conductance dispersion across the 20 models ranges from a low of **1.2x** for gNaF total to
  **6.2x** for gKM total and **9.7x** for gKh total -- but gKh has very small influence on the
  model, and similar studies on stomatogastric ganglion neurons report up to **40x** variation,
  making the PC dispersion intermediate. Experimentally measured channel variability in crab
  stomatogastric neurons is **2-4x** (Schulz et al. 2006), close to this study.
* Of 276 pairwise Pearson correlations between channel densities, only **5 pairs** had p < 0.01:
  (gK2t, gK2d) r=**0.78**, (gKdrm, gK2d) r=**0.63**, (gKdrm, gCaPm) r=**0.59**, (gKdrm, gK2t)
  r=**0.57**, and (gCaPt, gCaPd) r=**0.58**. Linear pairwise correlation thus explains only a
  fraction of the variability.
* Among the 10 total conductances (44 pair combinations), only **(gCaT, gCaP) was significantly
  anti-correlated** with r=**-0.62** (p < 0.01), suggesting that net calcium influx is constrained.
* Sensitivity analysis (24 x 500 = 12,000 single-parameter perturbations from the data point)
  showed that **7 parameters** (gKAs, gKAm, gKdrm, gKMs, gkMm, gKMt, gK2m) had small individual
  effects on fitness, but setting all 7 to zero simultaneously gave a poor fitness of **4.25**,
  showing collective effects matter.
* Around each of the 20 individuals, +/-1% perturbations preserved good fitness, but **+/-5%
  perturbations of a single parameter could push the model into bad-fitness territory** -- the
  parameter landscape is not smooth.
* A grid search at **6 points per dimension** would have recovered at most **~35% (7/20)** of the
  ES-discovered solutions; nine of the 20 (numbers 2, 3, 7, 8, 9, 11, 12, 18, 19) had **all** their
  6-point-grid neighbors with bad fitness; even a 10-point grid failed to rescue four borderline
  cases.
* Models reproduce features that were **not in the fitness function**: complex spikes from climbing
  fiber input match across soma, main dendrite, and smooth dendrite; firing rate vs.
  excitation/inhibition balance is reproduced; passive EPSP propagation from four parallel-fiber
  branchlets to the soma matches across all 20 models, indicating real generalization beyond the
  fit targets.
* Spatial pattern: for all dendritic conductances except gKM, the **20 models systematically place
  lower density in distal spiny dendrites and higher density in proximal smooth and main
  dendrites**, contradicting the original PM9 model''s choice of equal smooth/spiny densities.

## Innovations

### Phase-Plane Fitness for Complex Firing

The (V, dV/dt) density-matrix fitness from LeMasson and Maex avoids time-shift penalties (two
spike trains with the same shape but slightly different timing get a low distance) and avoids the
need to hand-engineer feature extractors for spike width, ISI, AHP, burst duration, etc. The
authors demonstrate that despite no explicit feature targets, the fit models still recover spike
height, AHP, burst structure, and inter-burst dynamics -- useful as a precedent for fitness design
in this project''s optimization stages.

### Self-Adaptive Correlated-Mutation ES on 24-D Real-Valued Parameter Space

Achard and De Schutter use ES rather than a binary-coded GA precisely because: parameters are real
numbers, mutation strength can co-evolve with the genome (impossible in standard GAs), and
crossover does not require parameters to be physically adjacent in the genotype. This is a strong
methodological argument that carries over to our own multi-objective work.

### First Detailed Compensatory-Diversity Analysis on a Large Compartmental Model

Prior work by Goldman et al. (2001) and Prinz et al. (2003, 2004) demonstrated parameter
degeneracy in **single-compartment** stomatogastric models with a handful of free parameters. This
paper extends the result to a **24-parameter, 1,600-compartment Purkinje cell** with four firing
modes -- the largest such study at that time -- and characterizes the geometry of the good region.

### Loose-Hyperplane Geometry of the Good-Fitness Region

The hyperplane visualization (linear combinations of solution triplets, projected onto pairs of
parameters) is a novel tool that makes the structure of the good region tangible. Some triplet
hyperplanes contain large connected good regions; others contain isolated solutions. Parallel
hyperplanes (offset by +/-5%, +/-10% of solution standard deviation) show that the good region is
a thin shell around the recovered hyperplanes, not a thick volume.

### Quantitative Failure Mode of Grid Search

The paper provides one of the first concrete demonstrations that systematic grid sampling, even at
6 or 10 points per dimension, would fail to discover a majority (~65%) of the ES-found solutions
on a complex compartmental model. This is a direct argument for stochastic global search on
high-dimensional problems.

## Datasets

This is a theoretical and computational paper; no biological datasets were used. The "data"
against which models are fit is itself a published computational model -- the De Schutter and
Bower 1994 "PM9" Purkinje cell model (J. Neurophysiol. 71: 375-400 and 401-419, and Proc. Natl.
Acad. Sci. USA 91: 4736-4740). The PM9 model and the 20 best-fit alternatives are not deposited as
explicit code releases in the paper; the optimization library used (ESEA from Evolving Objects)
and the simulator (Genesis 2.2.1) are publicly available.

## Main Ideas

* **Multi-objective and degenerate-by-design**: a complex compartmental model has many distinct
  "good" parameter sets, with up to ~10x variation in individual conductance densities while
  preserving detailed waveforms -- the project''s parameter sweeps and multi-objective optimization
  must expect families of good solutions, not unique optima.
* **Fitness function choice matters**: phase-plane density distance handles time-shift and avoids
  feature engineering, generalizing to features it did not see (synaptic responses, EPSP
  propagation). For this project''s tuning of angle-to-AP-frequency curves, an equivalent
  shift-invariant or phase-aware metric is worth considering alongside direct trace-difference
  losses.
* **Stochastic global search beats grid search**: at 24 free parameters, even a 6-point grid would
  miss ~65% of valid solutions; this validates the project''s planned use of NSGA-II (per memory
  on high-d MOBO) over grid sweeps for any optimization at moderate-to-high dimensionality.
* **Channel-density covariance is real but sparse**: only 5 of 276 channel pairs and 1 of 44 total
  pairs show significant linear correlation; expecting strong pairwise correlations as a search
  prior is wrong. Rather, compensation lives in low-dimensional curved manifolds that need to be
  discovered.
* **Local landscape is rough**: +/-5% perturbations of a single channel density can knock a model
  out of good fitness even when +/-1% is fine. Optimization protocols should use small mutation
  steps near convergence and treat hand-tuning as essentially impossible.

## Summary

Achard and De Schutter ask whether a complex, biophysically detailed compartmental neuron
admits multiple distinct sets of voltage- and calcium-gated channel conductances that reproduce
the cell''s detailed firing behavior. The motivation comes from two convergent lines of evidence:
experimental work on lobster and crab stomatogastric ganglion neurons showing 2-4x interanimal
variability in channel expression with preserved activity, and prior modelling work (Goldman 2001,
Prinz 2003-2004) showing parameter degeneracy in low-dimensional stomatogastric models. The paper
extends this question to the cerebellar Purkinje cell -- a 1,600-compartment, 24-parameter model
with four firing modes -- and asks both whether degeneracy exists and what shape the good region
of parameter space takes.

The methodology pairs a self-adaptive correlated-mutation evolution strategy ((57+19) population,
~8,000 evaluations per run, 9 independent runs) with a phase-plane density distance fitness
function summed across 7 current amplitudes, 3 recording sites, and 2 time windows. Each run took
~6 days on a 10-node G5 cluster. Twenty good solutions are retained (fitness 2.58 to 3.45). The
authors then probe the parameter landscape using single-parameter sensitivity sweeps, +/-1% and
+/-5% local perturbations, pairwise Pearson correlations on individual and total conductances, and
a novel hyperplane visualization that fits triplet-defined planes and parallel offset planes
through the solution cloud.

The 20 models reproduce somatic and dendritic voltage waveforms, complex spike responses, and
EPSP propagation despite the latter two not being in the fitness function. Total conductance
ratios across the 20 models range from 1.2x (gNaF) to 9.7x (gKh). Only 5 of 276 pairwise
correlations are significant at p < 0.01, and only the gCaT-gCaP total-conductance pair shows
a strong anti-correlation (r=-0.62). Local landscape is rough: +/-1% perturbations preserve
fitness, +/-5% can break it. Most importantly, the good region is shown to be a set of loosely
connected hyperplanes -- neither isolated points nor a single connected volume -- and a
6-points-per-dimension grid search would discover at most ~35% of the recovered solutions.

For this project, the paper establishes the methodological line that justifies using stochastic
multi-objective evolutionary search (NSGA-II in our case) on the cell''s voltage-gated channel
parameter space rather than grid sampling, and it establishes that we should expect families of
diverse solutions rather than a unique optimum. The specific innovations relevant to t0097''s
optimization design are: phase-plane or shift-tolerant fitness as a complement to direct
trace-distance metrics; self-adaptive mutation strengths in the genome; and hyperplane analysis
of the recovered Pareto front to understand which conductance combinations actually trade off.
Achard 2006 is the natural methodology citation alongside Druckmann 2007 and Hay 2011 in this
task''s catalogue, providing the earliest detailed demonstration that complex compartmental models
have low-dimensional curved manifolds of good parameters that only population-based search can
recover.