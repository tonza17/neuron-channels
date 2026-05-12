---
spec_version: "3"
paper_id: "10.48550_arXiv.2401.14014"
citation_key: "Morinaga2024"
summarized_by_task: "t0102_seedscale_n4_gen20"
date_summarized: "2026-05-11"
---
# Theoretical Analysis of Explicit Averaging and Novel Sign Averaging in Comparison-Based Search

## Metadata

* File: `files/morinaga_2024_sign-averaging-noisy-search.pdf`
* Published: 2024-01-25
* Authors: Daiki Morinaga JP, Youhei Akimoto JP
* Venue: arXiv preprint (cs.NE), 13 pages, RIKEN AIP collaboration
* DOI: `10.48550/arXiv.2401.14014`

## Abstract

In black-box optimization, noise in the objective function is inevitable. Noise disrupts the ranking
of candidate solutions in comparison-based optimization, possibly deteriorating the search
performance compared with a noiseless scenario. Explicit averaging takes the sample average of noisy
objective function values and is widely used as a simple and versatile noise-handling technique.
Although it is suitable for various applications, it is ineffective if the mean is not finite. We
theoretically reveal that explicit averaging has a negative effect on the estimation of ground-truth
rankings when assuming stably distributed noise without a finite mean. Alternatively, sign averaging
is proposed as a simple but robust noise-handling technique. We theoretically prove that the sign
averaging estimates the order of the medians of the noisy objective function values of a pair of
points with arbitrarily high probability as the number of samples increases. Its advantages over
explicit averaging and its robustness are also confirmed through numerical experiments.

## Overview

This paper provides a sharp theoretical characterization of when explicit averaging - the standard
noise-handling trick in evolution strategies and comparison-based black-box optimizers - actually
helps, and when it actively hurts. The authors prove that the answer hinges on a single parameter:
the stability index alpha of the noise distribution. For alpha in (1, 2] the noise has a finite
mean, the sample mean concentrates at rate K^(1 - 1/alpha), and explicit averaging is asymptotically
effective. At the critical value alpha = 1 (Cauchy-like noise) averaging is provably ineffective:
the order estimation probability (OEP) does not improve with more samples. For alpha in (0, 1) the
situation is worse than no averaging at all - the OEP strictly decreases as the sample budget K
grows, because the sample mean is itself a stable random variable whose dispersion grows with K.

Having identified this failure mode, the paper introduces sign averaging as a robust alternative.
Sign averaging compares two candidate solutions by counting how many of the K paired noisy
evaluations rank one above the other; it estimates the sign of the median difference rather than the
sign of the mean difference. The central theoretical result (Theorem 9) is that sign averaging OEP
converges to 1 as K grows under very mild conditions on the noise distribution - no finite-mean
assumption is needed, only continuity and a median-additivity property. Numerical experiments on
benchmark functions with stable noise of varying alpha confirm both negative results for explicit
averaging at low alpha and the universal robustness of sign averaging across the whole alpha range.

For the present project, which uses NSGA-II on a stochastic compartmental simulator with K = 4 seeds
per individual, this paper provides the theoretical taxonomy that justifies the regime we operate
in. The fitness landscape of the DSGC tuning problem combines well-behaved EPSP/IPSP statistics with
firing-rate metrics that can have long-tailed seed-to-seed variation; understanding where on the
alpha spectrum each metric lives determines whether K = 4 averaging is informative or actively
misleading.

## Architecture, Models and Methods

The paper is theoretical with numerical validation. The setting is comparison-based search on a
noisy black-box objective f(x; epsilon) = h(x) + sum_m g_m(x) * epsilon_m, where h(x) is the
noiseless objective and the noise vector epsilon has components drawn from a common stable
distribution with stability parameter alpha in (0, 2]. Stable distributions are chosen because they
form the natural generalisation of the central limit theorem: they include Gaussian (alpha = 2,
finite mean and variance), Cauchy (alpha = 1, no finite mean), and Levy-stable laws (alpha < 1, no
finite mean) under one unified parameterisation.

The key analytical quantity is the Order Estimation Probability (OEP): for a fixed pair of points
(x_1, x_2) with true objective gap Delta, the probability that K noisy evaluations correctly recover
sign(h(x_1) - h(x_2)). The explicit averaging estimator computes the sample mean of K paired noisy
differences and takes its sign. The sign averaging estimator instead counts the sign of each of K
paired differences and takes the majority vote.

Theorem 3 is the negative result for explicit averaging. It states that the OEP behaves as

* alpha in (1, 2]: OEP converges to 1, rate driven by K^(1 - 1/alpha).
* alpha = 1: OEP is constant in K - averaging gives no asymptotic improvement.
* alpha in (0, 1): OEP strictly decreases in K - averaging is counterproductive.

The decisive quantity is the factor K^(1 - 1/alpha) in the inequality
Pr[-eta_Delta(x_1, x_2) * epsilon_AVE < K^(1 - 1/alpha) * |f(x_1; Delta) - f(x_2; Delta)|]: when 1 -
1/alpha > 0 the right-hand side grows with K (improvement), when 1 - 1/alpha = 0 it is constant, and
when 1 - 1/alpha < 0 it shrinks with K.

Theorem 9 is the positive result for sign averaging. Under (i) median additivity of f, (ii)
continuity of f(x; epsilon), and (iii) sign(median(f(x_1) - f(x_2))) = sign(h(x_1) - h(x_2)), sign
averaging OEP converges to 1 with K independent of alpha. The proof reduces the sign-averaging
estimator to a Bernoulli sum and applies a Hoeffding-type concentration argument that has no moment
requirement on epsilon - the key reason it works in regimes where explicit averaging fails.

Numerical experiments validate the theory on benchmark optimisation problems with stable noise at
several alpha values, comparing OEP curves of the two estimators as K grows.

## Results

* For Gaussian noise (alpha = 2), explicit averaging OEP converges to 1 at the standard sqrt(K) rate
  \- the textbook regime.
* For sub-Gaussian heavy-tailed but finite-mean noise (alpha in (1, 2)), explicit averaging still
  converges to OEP = 1, but at the slower rate K^(1 - 1/alpha); near alpha = 1+ this approaches an
  arbitrarily slow polynomial decay.
* For Cauchy noise (alpha = 1), explicit averaging OEP is provably constant in K - adding more seeds
  yields zero asymptotic benefit.
* For infinite-mean stable noise (alpha in (0, 1)), explicit averaging OEP is a strictly decreasing
  function of K - increasing the sample budget makes ranking accuracy worse, not better.
* Sign averaging OEP converges to 1 for every alpha in (0, 2], with rate driven by the median
  separation rather than any moment of epsilon.
* Numerical experiments confirm all four explicit-averaging regimes and the alpha-independent
  convergence of sign averaging on the benchmark problems tested.
* The paper notes (and the experiments illustrate) that the cost of sign averaging is no higher than
  explicit averaging: both use K paired evaluations per comparison.

## Innovations

### First Theoretical Decomposition of Explicit Averaging by Noise Stability

Prior work on noisy black-box optimisation treated explicit averaging as a generally useful
heuristic and focused on Gaussian or bounded-variance noise. Morinaga and Akimoto give the first
sharp characterisation of when it works, when it is neutral, and when it is harmful, with the
threshold expressed in terms of a single, easy-to-test property of the noise distribution (alpha >
1, alpha = 1, alpha < 1). This makes the choice of K = 4 vs K = 32 a principled rather than
empirical decision once the noise tail is known.

### Sign Averaging as a Heavy-Tail-Robust Estimator

The proposed sign-averaging estimator is mechanically simple - count majority direction of paired
differences - but theoretically novel as a noise-handling primitive for comparison-based search. It
is the first such estimator with provable convergence under noise distributions that lack a finite
mean, including Cauchy and Levy-stable laws. Because it is comparison-based, it slots directly into
existing ES/CMA-ES/NSGA-II pipelines wherever explicit averaging is currently used.

### Median-Based Ground Truth Reformulation

The paper reframes the ranking target: instead of trying to estimate sign(E[f(x_1) - f(x_2)]), which
requires the expectation to exist, sign averaging estimates sign(median[f(x_1) - f(x_2)]). For
distributions with finite mean these targets typically coincide; for heavy-tailed noise only the
median is well-defined. This conceptual shift is what makes the alpha-independent robustness
possible.

## Datasets

This is a theoretical paper with numerical validation experiments; no external datasets are used.
The numerical experiments are on standard synthetic benchmark optimisation problems with
controllable stable noise (alpha is a tunable parameter). The exact benchmark functions are
described in Section IV of the paper.

## Main Ideas

* The alpha threshold is the right diagnostic for whether seed-replicate averaging helps in noisy
  comparison-based optimisation. For the DSGC project specifically, this gives a principled basis to
  evaluate whether N_SEEDS = 4 lies in the regime where averaging is useful (alpha > 1, "noisy but
  algorithm survives") or in a regime where extra seeds give diminishing or negative returns.
* For metrics whose seed-to-seed variation is approximately Gaussian (EPSP/IPSP amplitudes,
  passive-mode integrals), explicit averaging converges at sqrt(K) and K = 4 is comfortably in the
  effective regime. For sharply non-linear metrics (firing rate at threshold, DSI on near-zero
  baseline) the effective alpha may be lower, and small-K averaging may be far less informative than
  it appears.
* Sign averaging is a drop-in replacement for explicit averaging in ranking-based selection (e.g.,
  NSGA-II non-dominated sort). When seed-to-seed variability is suspected to be heavy-tailed for any
  objective, switching that objective seed reduction to a sign-majority rule is theoretically
  preferable and computationally free.
* The K^(1 - 1/alpha) convergence rate gives a quantitative cost-benefit ratio for increasing
  N_SEEDS: doubling K only improves OEP at rate 2^(1 - 1/alpha), which is much less than sqrt(2) for
  alpha close to 1 and zero for alpha = 1. This argues against blanket "more seeds" strategies and
  in favour of metric-by-metric tail diagnostics before scaling.

## Summary

Morinaga and Akimoto address a fundamental and previously under-analysed question in noisy black-box
optimisation: when does explicit averaging - the default seed-replicate strategy in ES, CMA-ES,
NSGA-II, and most evolutionary optimisers - actually improve solution ranking, and when does it
fail? Prior work largely assumed Gaussian or bounded-variance noise; this paper drops that
assumption and analyses the full family of stable-distribution noises parameterised by a single
stability index alpha in (0, 2].

The methodology centres on the Order Estimation Probability (OEP), the probability that K noisy
paired evaluations recover the true ranking of two candidate solutions. The authors prove two
theorems with sharp characterisations. Theorem 3 dissects explicit averaging into three regimes:
beneficial (alpha > 1, OEP converges to 1 at rate K^(1 - 1/alpha)), neutral (alpha = 1, OEP is
constant in K), and actively harmful (alpha < 1, OEP strictly decreases as K grows). Theorem 9 then
proves that a newly introduced sign-averaging estimator - which counts majority direction over K
paired comparisons rather than averaging magnitudes - converges to OEP = 1 for every alpha in (0, 2]
under only mild continuity and median-additivity assumptions, requiring no finite moment of the
noise.

The headline findings are that explicit averaging is provably worse than no averaging for
heavy-tailed (infinite-mean) noise, that sign averaging is a free, drop-in fix that works
universally, and that the alpha index of the noise distribution is the right and complete diagnostic
for choosing between them. Numerical experiments at a range of alpha values confirm all four
predicted regimes of explicit averaging and the alpha-independent robustness of sign averaging.

For this project, where t0102 explicitly probes seed-scale behaviour with N_SEEDS = 4 over 20
NSGA-II generations, the paper supplies the theoretical taxonomy that the experiment will land in.
The working hypothesis is that DSGC fitness objectives sit at alpha well above 1 (EPSP/IPSP
integrals, passive-mode metrics) where K = 4 explicit averaging is effective at slow-polynomial
rate, but that some firing-rate-derived objectives may sit closer to alpha = 1 where averaging is
nearly inert. This anchors the present task scope to the "noisy but algorithm survives" regime
predicted by Theorem 3 and motivates a follow-up where sign averaging replaces explicit averaging
for heavy-tailed objectives specifically.
