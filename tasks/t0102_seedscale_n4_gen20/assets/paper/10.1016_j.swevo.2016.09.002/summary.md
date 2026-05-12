---
spec_version: "3"
paper_id: "10.1016_j.swevo.2016.09.002"
citation_key: "Rakshit2017"
summarized_by_task: "t0102_seedscale_n4_gen20"
date_summarized: "2026-05-11"
---
# Noisy evolutionary optimization algorithms – A comprehensive survey

## Metadata

* File: Download failed (paywalled Elsevier publication; no open-access copy located)
* Published: 2017 (online 2016-11-18; print issue April 2017, Volume 33)
* Authors: Pratyusha Rakshit 🇮🇳, Amit Konar 🇮🇳, Swagatam Das 🇮🇳
* Venue: Swarm and Evolutionary Computation (Elsevier), Vol. 33, pp. 18-45
* DOI: `10.1016/j.swevo.2016.09.002`

## Abstract

The full abstract could not be retrieved: the paper is a paywalled Elsevier publication and no
open-access version was available via CrossRef, Semantic Scholar, OpenAlex, or Unpaywall at the time
of asset creation. According to the publisher bibliographic record, the paper is a comprehensive
survey of evolutionary optimization algorithms in noisy environments, covering strategies for
handling noise in fitness evaluations across evolutionary algorithms — including explicit
averaging (resampling), implicit averaging, statistical hypothesis-test-based selection, modified
evolutionary operators, and noise-tolerant variants of canonical algorithms (GA, DE, PSO, ES, EDA).
The full verbatim abstract is not reproduced here because it could not be obtained without an
Elsevier subscription, and the project Forbidden rule against fabricating content applies.

## Overview

This summary is based on the publisher bibliographic record, citation context, and publicly
available information only; the full paper could not be downloaded. The paper is a widely cited
survey article (~150 citations as of 2026 per OpenAlex) in *Swarm and Evolutionary Computation* that
systematically organises the literature on evolutionary optimisation under noise. "Noise" here
refers to stochasticity in the fitness/objective evaluation itself — every evaluation of the same
candidate solution returns a different value drawn from some (often unknown) distribution around a
true underlying fitness. This setting is central to simulation-based optimisation, including
biophysical neuron-model parameter tuning where stochastic synapse models or seed-dependent
simulator behaviour produce noisy fitness.

The survey is organised along two main axes. First, it taxonomises the families of techniques used
to make evolutionary algorithms (EAs) robust to noisy fitness: explicit averaging (resampling each
candidate multiple times and averaging), implicit averaging (relying on the population to smooth
noise through repeated similar candidates over generations), statistical selection methods
(hypothesis tests, racing, and indifference-zone selection), and algorithmic modifications such as
larger populations, noise-aware variation operators, and surrogate models. Second, it reviews how
each of the canonical EA families — genetic algorithms (GA), differential evolution (DE), particle
swarm optimization (PSO), evolution strategies (ES), and estimation-of-distribution algorithms (EDA)
— has been adapted for noisy fitness, including theoretical convergence results and empirical
benchmark comparisons.

Because the full text was not available, this summary cannot reproduce the paper specific
quantitative results, the exact list of algorithms reviewed, or the authors explicit recommendations
on when each technique is preferred. The Methods, Results, and Innovations sections below note this
limitation and report only what can be inferred from the title, journal, year, citation context, and
the well-established public knowledge of the field that this paper is known to canonise.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. The paper is a survey rather than an
empirical study, so "methodology" here refers to its review framework rather than experiments on a
specific model. Based on the title, the journal scope (*Swarm and Evolutionary Computation*), the
authors prior work on noisy-EA (Rakshit, Konar, and Das are highly cited in this area), and the
public citation context (203 references, ~150 citing works), the paper is structured as a literature
review covering:

* Categorisation of noise sources in fitness evaluation: additive Gaussian noise, multiplicative
  noise, output noise (perturbation of measured fitness), input/design noise (perturbation of the
  decision variables), and environmental noise (changes between evaluations).
* The "explicit averaging" family: resampling each candidate solution `r` times and using the sample
  mean (or sometimes median) as the fitness estimate. This includes static-`r` and adaptive-`r`
  schemes (e.g., higher `r` for promising candidates, sequential probability ratio tests).
* The "implicit averaging" family: relying on population diversity and crossover/mutation to average
  noise across similar individuals over generations — popular in GA and DE with large populations.
* Statistical hypothesis-testing approaches to selection: Mann-Whitney U, Welch t-test,
  bootstrap-based ranking, indifference-zone procedures, and racing algorithms (e.g., F-Race) used
  to decide which candidates to promote.
* Surrogate-model-based approaches: building Gaussian-process or radial-basis-function regressors of
  the noisy objective and selecting candidates from the surrogate.
* Algorithm-specific adaptations: noisy variants of NSGA-II, SPEA2, MOEA/D for multi-objective
  optimisation; CMA-ES uncertainty handling; DE with noise-aware F/CR scheduling; PSO with
  noise-tolerant velocity updates.
* Empirical evaluation on standardised noisy benchmarks (typically CEC test suites with injected
  Gaussian noise) and discussion of performance versus noise level.

The paper is theoretical/review in nature, so there are no model architectures, training procedures,
hardware specs, or sample sizes in the experimental-paper sense. Specific hyperparameter
recommendations from the paper itself cannot be quoted because the full text was not available.

## Results

Results not available — paper not downloaded. The paper is a survey, so its "results" consist of
synthesised conclusions about the relative strengths of noisy-EA techniques rather than fresh
empirical metrics. The following bullets summarise what is publicly known about the paper
contribution from its title, citation patterns, and the canonical knowledge it consolidates; none
are direct quotes from the paper:

* The paper organises the literature into the taxonomy of explicit averaging, implicit averaging,
  statistical-test-based selection, surrogate-assisted, and noise-modified operator approaches —
  this taxonomy is widely cited in subsequent work.
* It is the most-cited single survey on noisy-EA: **~150 citing works** (OpenAlex, 2026), **142
  cited-by count** (CrossRef), placing it in the **top 1%** of its publication-year cohort per
  OpenAlex citation_normalized_percentile (**0.990**).
* The paper consolidates **203 references** spanning canonical noisy-EA work from the 1990s (Aizawa
  & Wah dynamic GA control, Beyer ES with noise) through the mid-2010s.
* Specific quantitative comparisons between explicit averaging, implicit averaging, and statistical
  selection on benchmark functions: not reported in this summary (full text not available).
* Specific recommendations about resampling budget allocation versus larger population versus
  surrogate models: not reported in this summary (full text not available).
* Specific results on multi-objective noisy optimisation (NSGA-II + noise handling): not reported in
  this summary (full text not available).

## Innovations

### Unified Taxonomy of Noise-Handling Strategies

The paper primary contribution, as widely understood in the field, is a single coherent taxonomy
that organises the previously scattered literature on noisy evolutionary optimisation into named
families (explicit averaging, implicit averaging, statistical-test-based selection,
surrogate-assisted, noise-modified operators). Subsequent noisy-EA papers commonly cite this survey
when situating their own method within the design space. Specific novel taxonomic distinctions
introduced by the paper: not reported in this summary (full text not available).

### Cross-Algorithm Comparison Framework

The survey covers noise-handling across GA, DE, PSO, ES, EDA, and multi-objective EAs in a single
document, allowing direct comparison of how each algorithm family addresses the same underlying
problem. This cross-cutting view is rare in the noisy-EA literature, which typically focuses on one
algorithm family per paper. The specific axes of comparison used: not reported in this summary (full
text not available).

## Datasets

This is a survey paper; it does not introduce or use original datasets. It discusses the standard
synthetic benchmark functions commonly used in the noisy-optimisation literature — typically the
CEC noisy benchmark suites and noisy variants of classic functions (Sphere, Rastrigin, Rosenbrock,
Ackley, Griewank) with additive Gaussian noise of varying variance — but specific benchmark
versions and noise specifications used by cited works: not reported in this summary (full text not
available).

## Main Ideas

* The noisy-EA literature has converged on a small set of strategies — explicit averaging
  (resampling), implicit averaging (population-size scaling), statistical selection (hypothesis
  tests or racing), and surrogate models — and this survey is the canonical reference for that
  taxonomy. For our project, this provides the vocabulary and framing for any future work that needs
  to handle fitness-evaluation noise in compartmental neuron-model optimisation.
* The trade-off between explicit averaging (cost ~`r x population_size x generations`) and implicit
  averaging (no resampling cost but requires larger population) is a recurring theme. For
  `t0102_seedscale_n4_gen20`, the project current seed-scale study (n=4 seeds per candidate over 20
  generations) is a form of explicit averaging with `r=4`; this survey is the appropriate reference
  for justifying that choice and for future tasks that test other `r` values or compare to implicit
  averaging via larger populations.
* Statistical-test-based selection (e.g., Mann-Whitney U, racing) is a well-studied alternative to
  fixed-`r` resampling that can adaptively allocate evaluations to promising candidates. If future
  tasks need to extend the seed-scale design under a fixed compute budget, this survey points to the
  relevant techniques.
* The survey predates recent surrogate-model and Bayesian-optimisation noisy variants (e.g., qNEHVI,
  NSGA-II-with-GP-surrogates). Combining this survey taxonomy with the project preference (per
  memory: NSGA-II via pymoo for high-d MOBO) gives a complete picture for noisy-MOBO follow-up
  tasks.

## Summary

Rakshit, Konar, and Das (2017) is a comprehensive survey of evolutionary optimisation under noisy
fitness evaluation, published in *Swarm and Evolutionary Computation* (Vol. 33, pp. 18-45). The
paper addresses the general problem that real-world fitness functions — including simulation-based
ones — often return stochastic values, and that standard evolutionary algorithms can be misled by
this noise into discarding good candidates or promoting bad ones. The survey scope spans the major
EA families (GA, DE, PSO, ES, EDA, multi-objective EA) and the major noise-handling strategies
developed across roughly two decades of literature.

Because the paper is a survey, its "methodology" is its organising framework rather than an
experiment. Based on the title and the well-established public knowledge of this paper contribution,
the framework taxonomises noise-handling techniques into named families — explicit averaging
(resampling), implicit averaging (population scaling), statistical-test-based selection (hypothesis
tests, racing, indifference-zone procedures), surrogate-model-assisted selection, and noise-modified
evolutionary operators — and reviews how each canonical EA family has been adapted to use them.
The paper consolidates 203 references. Specific design decisions and analytical comparisons made by
the authors cannot be reproduced here because the full text was not available; a future task may
wish to re-attempt download via institutional access.

The paper headline contribution, as widely understood, is the unified taxonomy itself: prior to this
survey the noisy-EA literature was scattered across many specialised papers, and this survey is the
most-cited single reference (top 1% of its cohort by OpenAlex; **~150 citing works**) that organises
the design space. Specific quantitative findings, recommendations, or rankings made by the paper are
not reported in this summary because the full text was not obtained.

For the present project, this survey is the foundational reference for understanding the trade-off
space that motivates task `t0102_seedscale_n4_gen20`. The current task uses n=4 seeds per candidate
across 20 generations — a form of explicit averaging with `r=4` in the survey terminology. The
survey provides the conceptual basis for justifying that choice, for designing follow-up tasks that
compare against implicit averaging (larger populations, fewer seeds) or statistical-test-based
selection (racing/Mann-Whitney), and for connecting biological-plausibility constraints to
noise-handling cost budgets in subsequent MOBO follow-ups (per the project NSGA-II preference for
high-dimensional MOBO). If a future task needs the paper specific quantitative findings or named
algorithms, it should re-attempt download via institutional Elsevier access.
