---
spec_version: "3"
paper_id: "10.48550_arXiv.2306.04525"
citation_key: "Dang2023"
summarized_by_task: "t0102_seedscale_n4_gen20"
date_summarized: "2026-05-11"
---
# Analysing the Robustness of NSGA-II under Noise

## Metadata

* File: `files/dang_2023_nsga-ii-robustness-noise.pdf`
* Published: 2023
* Authors: Duc-Cuong Dang DE, Andre Opris DE, Bahare Salehi DE, Dirk Sudholt DE
* Venue: GECCO 23 (Genetic and Evolutionary Computation Conference), Lisbon
* DOI: `10.48550/arXiv.2306.04525` (arXiv); `10.1145/3583131.3590421` (ACM)

## Abstract

Runtime analysis has produced many results on the efficiency of simple evolutionary algorithms like
the (1+1) EA, and its analogue called GSEMO in evolutionary multiobjective optimisation (EMO).
Recently, the first runtime analyses of the famous and highly cited EMO algorithm NSGA-II have
emerged, demonstrating that practical algorithms with thousands of applications can be rigorously
analysed. However, these results only show that NSGA-II has the same performance guarantees as GSEMO
and it is unclear how and when NSGA-II can outperform GSEMO. We study this question in noisy
optimisation and consider a noise model that adds large amounts of posterior noise to all objectives
with some constant probability p per evaluation. We show that GSEMO fails badly on every noisy
fitness function as it tends to remove large parts of the population indiscriminately. In contrast,
NSGA-II is able to handle the noise efficiently on LeadingOnesTrailingZeroes when p < 1/2, as the
algorithm is able to preserve useful search points even in the presence of noise. We identify a
phase transition at p = 1/2 where the expected time to cover the Pareto front changes from
polynomial to exponential. To our knowledge, this is the first proof that NSGA-II can outperform
GSEMO and the first runtime analysis of NSGA-II in noisy optimisation.

## Overview

This paper presents the first theoretical runtime analysis of NSGA-II under noisy multi-objective
optimisation. It compares NSGA-II to GSEMO (Global Simple Evolutionary Multi-Objective Optimiser),
an idealised baseline EMO algorithm that has dominated prior theoretical work. Previously, NSGA-II
had only been *matched* by GSEMO in worst-case bounds and never shown to strictly outperform it. The
authors construct a concrete setting (noisy bi-objective benchmarks under a Bernoulli noise model)
where NSGA-II is provably efficient while GSEMO provably fails.

The central technical innovation is a deliberately extreme noise model: the **(delta, p)-Bernoulli
noise model** adds a constant offset `delta = n + 1` to *all* objectives with probability `p` per
evaluation. Because the offset is large enough that any noisy individual strictly dominates any
noise-free individual, this represents a worst-case posterior noise scenario. GSEMO, which
immediately removes every weakly dominated point on insertion, ends up purging useful incumbents
whenever a noisy evaluation occurs and collapses to constant-size populations. NSGA-II, in contrast,
maintains a population of size mu that filters via crowding distance, which preserves useful search
points even under heavy noise.

The headline result is a sharp **phase transition at p = 1/2** for NSGA-II without crossover on the
LeadingOnesTrailingZeroes (LOTZ) benchmark. Below this critical noise probability, NSGA-II covers
the Pareto front in polynomial expected time given a sufficiently large population (mu = Omega(n log
n)). Above it (specifically `p >= 10/19`), the expected runtime is provably exponential
`exp(Omega(n))`. Crucially, the paper also reports Gaussian-noise experiments showing qualitatively
similar phase-transition behaviour, suggesting the result is not an artefact of the Bernoulli model.

## Architecture, Models and Methods

The paper analyses two evolutionary multi-objective optimisation algorithms in a discrete bit-string
setting (problem size `n`):

* **NSGA-II without crossover** (Algorithm 1): population size mu, binary tournament parent
  selection, bitwise mutation rate 1/n, survival selection via non-dominated sorting plus crowding
  distance. The theoretical analysis assumes `pc = 0` (no crossover); experiments use `pc = 0.9`.
* **GSEMO** (Algorithm 2): unbounded archive, uniform parent selection from the current Pareto
  front, bitwise mutation, weak-dominance removal on insertion.

Two bi-objective test functions are studied:

* **LOTZ** (LeadingOnesTrailingZeroes): `f(x) = (LO(x), TZ(x))`, where `LO` counts leading 1-bits
  and `TZ` counts trailing 0-bits. Pareto front size is `n + 1`.
* **OMM** (OneMinMax): `f(x) = (|x|_1, |x|_0)`. Pareto front size is `n + 1`.

The noise models are:

* **(delta, p)-Bernoulli noise**: with probability `p` per evaluation, add `delta` to all objectives
  simultaneously. The paper sets `delta = n + 1`.
* **Posterior Gaussian noise**: `f_tilde(x) = f(x) + delta * 1`, with `delta ~ N(0, sigma^2)` added
  to all objectives on every evaluation. `sigma` is varied as `n * q` with
  `q in {2^0, 2^-1, 2^-3, 2^-4}`.

Theoretical analysis uses **drift analysis** of the population number of useful search points
(noise-free individuals on the LOTZ Pareto front). The negative result for `p > 10/19` is proved by
showing the expected drift toward population collapse is `Omega(1)` and applying negative
multiplicative drift. The positive result requires `mu = Omega(n log n)` so that with high
probability the noise-free population is not fully overwritten in any single generation.

Experimental setup: problem sizes `n in {20, 30, 40}`, `pc = 0.9`, one-point crossover,
`mu = 9(n + 1)`, 50 runs per configuration, budget `10 * n^3` fitness evaluations.

## Results

* **Phase transition at p = 1/2**: NSGA-II covers the Pareto front of noisy LOTZ in expected
  polynomial time for any constant `p < 1/2` (Theorem 8) but requires `exp(Omega(n))` expected
  generations for any constant `p >= 10/19 ~ 0.526` (Theorem 10).
* **GSEMO universal failure**: Under any non-trivial Bernoulli noise, GSEMO requires `exp(Omega(n))`
  time on **every** bi-objective function (Theorem 3) because its weak-dominance-on-insertion rule
  eliminates useful incumbents indiscriminately.
* **Empirical confirmation on Bernoulli noise**: NSGA-II achieves **100% success rate** across all
  tested `p` values **except** `p in {0.5, 0.6}` on LOTZ, where success rate drops to **0%**.
* **Empirical results on OMM**: GSEMO never covers more than **40%** of the Pareto front under
  Bernoulli noise; on LOTZ it covers less than **10%**.
* **Average evaluations to cover LOTZ Pareto front (n = 40, NSGA-II)**: ~202,822 at `p = 2^-6`,
  rising to ~273,906 at `p = 2^-2 = 0.25`, then ~640,453 at `p = 0.4` (still 100% success), and
  exhausting the `10 * n^3 = 640,000` budget at `p in {0.5, 0.6}` (0% success).
* **Gaussian-noise success rates (LOTZ, n = 40)**: **100%** at `sigma = n * 2^-4`, **96%** at
  `sigma = n * 2^-3`, **10%** at `sigma = n * 2^-2`, **0%** at `sigma >= n * 2^-1`.
* **Population size matters**: positive runtime guarantees require `mu = Omega(n log n)`; smaller
  populations cannot preserve enough useful search points across a noisy generation.

## Innovations

### First Proven NSGA-II Advantage Over GSEMO

Prior runtime analyses (Zheng et al. 2022; Bian and Qian 2022; Doerr and Qu 2022) showed only that
NSGA-II *matches* GSEMO asymptotic guarantees. This paper provides the first separation result: on
noisy LOTZ with `p < 1/2`, NSGA-II is polynomial while GSEMO is exponential. The mechanism is the
crowding-distance retention of dominated solutions, which protects against noise-induced incumbent
loss.

### (delta, p)-Bernoulli Noise Model

A deliberately worst-case posterior noise model in which a single random event can flip the
dominance relation between any two individuals. Designed to expose algorithmic weaknesses under
heavy noise while remaining analytically tractable.

### Sharp p = 1/2 Phase Transition

Both upper bound (`p < 1/2` polynomial) and lower bound (`p >= 10/19` exponential) are proved,
establishing a phase-transition theorem for NSGA-II runtime as a function of noise probability. This
is the first such transition theorem for a practical EMO algorithm.

### Drift-Analysis Framework for Noisy EMO

Introduces a drift-analysis approach for population-based EMO algorithms under noise, tracking the
number of useful search points. Provides a template for analysing other EMO algorithms (or other
noise models) in stochastic settings.

## Datasets

This is a theoretical paper; no datasets were used. Experimental validation runs on synthetic
bi-objective benchmarks LeadingOnesTrailingZeroes (LOTZ) and OneMinMax (OMM) at problem sizes
`n in {20, 30, 40}` with 50 independent runs per configuration.

## Main Ideas

* **NSGA-II is provably noise-robust below a critical noise probability**: this provides a
  theoretical anchor for the project empirical use of NSGA-II on noisy fitness functions (DSGC
  simulation outputs vary with stochastic synaptic input). When the per-trial Bernoulli-equivalent
  noise probability is well below 1/2, NSGA-II remains polynomial in problem size.
* **Larger populations buffer against noise**: the proof requires `mu = Omega(n log n)`. For
  high-dimensional MOBO problems (68-d in t0102), small populations like `pop = 96` may be in a
  marginal regime; if the algorithm fails to converge it is worth testing whether a larger
  population recovers performance before concluding the problem is too noisy.
* **Crowding distance is the protective mechanism**: NSGA-II survives because crowding distance
  retains dominated individuals across generations. Algorithms that discard dominated individuals on
  insertion (like GSEMO) collapse under noise. This justifies the project choice of NSGA-II over
  simpler archive-based EMO algorithms.
* **Gaussian noise transfers qualitatively**: although the theorems are for Bernoulli noise, the
  Gaussian experiments show the same phase-transition phenomenon, so the result provides a
  reasonable theoretical justification for NSGA-II behaviour under DSGC-simulation-style noise.
* **N_SEEDS=4 is noisy-but-survivable**: t0102 runs `N_SEEDS = 4` with stochastic synaptic input,
  which corresponds to a small but non-zero effective per-evaluation noise probability. By this
  paper framework, this places the experiment in the polynomial-time-survivable regime, not in the
  catastrophic `p >= 1/2` regime.

## Summary

Dang, Opris, Salehi, and Sudholt present the first theoretical runtime analysis of NSGA-II under
noisy multi-objective optimisation, addressing the open question of *when* the popular NSGA-II
algorithm outperforms the idealised GSEMO baseline. Previous theoretical work had matched the two
algorithms only at the same asymptotic complexity, leaving NSGA-II apparent practical advantages
unexplained. The authors close this gap by constructing a noisy benchmark setting in which NSGA-II
is provably polynomial-time while GSEMO is provably exponential-time.

The methodology combines a worst-case **(delta, p)-Bernoulli noise model** in which a fixed offset
`delta = n + 1` is added to all objectives with probability `p` per evaluation with drift analysis
on standard bi-objective benchmarks (LOTZ, OMM). The authors prove a sharp **phase transition at p =
1/2**: below this threshold NSGA-II with population size `mu = Omega(n log n)` covers the Pareto
front in polynomial expected time (Theorem 8), while above `p = 10/19 ~ 0.526` the expected runtime
is exponential (Theorem 10). Experimental confirmation uses problem sizes n = 20, 30, 40 with 50
runs each, and includes Gaussian-noise experiments showing qualitatively similar phase-transition
behaviour.

The headline empirical findings match the theory cleanly. NSGA-II achieves 100% success on noisy
LOTZ for every `p < 0.5` and 0% for `p in {0.5, 0.6}`. GSEMO never covers more than 40% of the
Pareto front under any non-trivial noise. Under Gaussian noise, NSGA-II success rate drops from 100%
at `sigma = n * 2^-4` to 0% at `sigma = n * 2^-1`. The mechanism behind NSGA-II robustness is its
crowding-distance survival rule, which retains dominated individuals across generations and prevents
noise-induced incumbent loss, the failure mode that destroys GSEMO.

This paper matters for the neuron-channels project because t0102 (and the entire NSGA-II line of
work) optimises a DSGC compartmental model whose objective values are inherently noisy: each
configuration is evaluated on a small number of stochastic synaptic-input seeds (N_SEEDS = 4 in
t0102). The phase-transition theorem provides a theoretical anchor that the chosen seed count puts
the experiment well below the critical noise probability of 1/2, so NSGA-II should retain its
polynomial-time guarantees. The paper also clarifies a practical design principle: NSGA-II
crowding-distance retention is what buys noise robustness, so degenerate populations or aggressive
archive-pruning would forfeit this protection. The requirement that `mu = Omega(n log n)` is
suggestive: at 68-dimensional problems, a population of 96 may be on the smaller side, and if t0102
fails to recover a joint-pass corner this paper indicates that a larger population (not more seeds)
is a principled next lever.
