---
spec_version: "3"
paper_id: "no-doi_Ament2023_logei-bo"
citation_key: "Ament2023"
summarized_by_task: "t0078_bedb_mobo_v2_ais_tiered_ahp"
date_summarized: "2026-05-03"
---
# Unexpected Improvements to Expected Improvement for Bayesian Optimization

## Metadata

* **File**: `files/ament_2023_logei-bo.pdf`
* **Published**: 2023 (NeurIPS 2023)
* **Authors**: Sebastian Ament 🇺🇸, Samuel Daulton 🇺🇸, David Eriksson 🇺🇸,
  Maximilian Balandat 🇺🇸, Eytan Bakshy 🇺🇸 (all Meta)
* **Venue**: 37th Conference on Neural Information Processing Systems (NeurIPS 2023)
* **DOI**: N/A (arXiv:2310.20708)

## Abstract

Expected Improvement (EI) is arguably the most popular acquisition function in Bayesian optimization
and has found countless successful applications, but its performance is often exceeded by that of
more recent methods. Notably, EI and its variants, including for the parallel and multi-objective
settings, are challenging to optimize because their acquisition values vanish numerically in many
regions. This difficulty generally increases as the number of observations, dimensionality of the
search space, or the number of constraints grow, resulting in performance that is inconsistent
across the literature and most often sub-optimal. Herein, we propose LogEI, a new family of
acquisition functions whose members either have identical or approximately equal optima as their
canonical counterparts, but are substantially easier to optimize numerically. We demonstrate that
numerical pathologies manifest themselves in "classic" analytic EI, Expected Hypervolume Improvement
(EHVI), as well as their constrained, noisy, and parallel variants, and propose corresponding
reformulations that remedy these pathologies. Our empirical results show that members of the LogEI
family of acquisition functions substantially improve on the optimization performance of their
canonical counterparts and surprisingly, are on par with or exceed the performance of recent
state-of-the-art acquisition functions, highlighting the understated role of numerical optimization
in the literature.

## Overview

This paper diagnoses a long-overlooked numerical pathology in the entire Expected Improvement (EI)
family of Bayesian optimization (BO) acquisition functions and proposes a family of reformulations,
collectively called LogEI, that fix it. The core problem is that although EI is mathematically
non-zero almost everywhere under a Gaussian posterior, naive implementations evaluate to literal
floating-point zero across large fractions of the search space, especially as iterations progress
and the optimality gap shrinks. Once the value is zero, its gradient is also zero, so multistart
gradient-based optimizers (the standard recipe in BoTorch and most BO packages) degenerate into
random search. The authors prove a probabilistic lower bound (Theorem 1) on the fraction of the
domain where EI's argument falls below the floating-point support, showing the issue worsens with
dimensionality and the concentration of high objective values.

The fix is methodical: every member of the EI family — analytic EI, constrained EI (CEI), parallel
qEI, expected hypervolume improvement (EHVI/qEHVI), and their noisy variants — is reformulated to
operate in log-space using stable numerical primitives (logsumexp, log1mexp, erfcx, logsoftplus,
softplus, fatplus). The result is qLogEI / qLogCEI / qLogEHVI / qLogNEHVI: acquisition functions
with the same (or provably close) optima as their canonical counterparts, but with non-vanishing
gradients across the entire domain. A relative-error bound (Lemma 2) controls how closely qLogEI
tracks qEI as a function of the smoothing temperatures and batch size.

Empirically, the LogEI variants dominate or match every baseline tested, including state-of-the-art
information-theoretic methods (GIBBON, JES) and trust-region constrained BO (SCBO), across
single-objective, constrained, parallel, high-dimensional, and multi-objective benchmarks. A key
secondary finding is that the LogEI reformulation makes joint batch optimization competitive with
the previously dominant sequential-greedy strategy, which simplifies parallel BO. All methods are
released as part of BoTorch, making them drop-in replacements for the canonical EI APIs.

## Architecture, Models and Methods

The work is a numerical-methods paper rather than a model-architecture paper. The substrate is
standard Gaussian Process (GP) BO using BoTorch with scipy's L-BFGS-B optimizer for acquisition
maximization, 16 uniformly-random multi-start initial points, and the canonical
sample-average-approximation strategy of Balandat et al. [2020] for Monte Carlo acquisitions.

The analytic LogEI implementation hinges on a piecewise stable evaluation of `log_h(z)` where
`h(z) = phi(z) + z*Phi(z)` is the EI base function. The piecewise definition uses three branches:
(i) `z > -1` evaluated directly; (ii) `-1/sqrt(eps) < z <= -1` using
`-z^2/2 - log(2*pi)/2 + log1mexp(log(erfcx(-z/sqrt(2)) * |z|) + log(pi/2)/2)`; and (iii)
`z <= -1/sqrt(eps)` using the asymptotic `-z^2/2 - log(2*pi)/2 - 2*log(|z|)`. This makes the
function asymptotically quadratic in the negative tail, which is exactly the regime where canonical
EI underflows. The progenitor implementations in SMAC 1.0 and RoBO are credited but had
instabilities for very negative `z`, which the third branch removes.

For Monte Carlo qEI, the discrete `max_j [xi_i(x_j) - y*]+` over batch members is replaced by a
two-stage smooth approximation: (1) `softplus_tau0(xi_ij - y*)` approximates the rectifier and (2)
the L^(1/tau_max) norm approximates the max. The full qLogEI estimator is a nested
`logsumexp_i(tau_max * logsumexp_j(logsoftplus_tau0(...)) / tau_max)`, computed entirely in
log-space. Lemma 2 bounds the relative approximation error by
`(q^tau_max - 1) qEI(X) + log(2)*tau0*q^tau_max`. For large batch sizes, canonical softplus
saturates and the authors introduce **fatplus**, a fat-tailed non-linearity that retains gradient
signal at large q (Appendix A.4). qLogEHVI applies the same recipe to the differentiable
inclusion-exclusion hypervolume formulation of Daulton et al. [2020], including a noisy variant
**qLogNEHVI** that adapts the same machinery to the noisy multi-objective setting. Constrained
variants (LogCEI, qLogCEI) decompose into `LogEI + sum_i log(P(f_i(x) <= 0))` and use a stable
Gaussian log-CDF.

Benchmarks include: 10D Sum-of-Squares; Ackley at d in {2, 8, 16}; Michalewicz; four constrained
engineering design problems (3D tension-compression spring with 4 constraints, 4D pressure vessel
with 4 constraints, 4D welded beam with 5 constraints, 7D speed reducer with 11 constraints); 16D
Ackley with parallel batch sizes q in {4, 16, 32}; high-dimensional Hartmann6 embedded in 100D; 103D
SVM hyperparameter tuning; 100D rover trajectory; 30D cell-network coverage and 16D DTLZ2
multi-objective. All experiments use mean +/- 2 standard errors over multiple replicates.

## Results

* On the 10D Sum-of-Squares, canonical EI **stalls after about 75 evaluations** with regret
  flat-lining at around `10^-1`, while LogEI continues to descend below `10^-2` (Figure 2).
* In the Ackley d-sweep, the gap between LogEI and canonical EI **widens with dimension**, with EI
  failing to leave the random-search baseline at d=16 while LogEI reaches values near 4 within 250
  evaluations (Figure 3).
* **JES is roughly two orders of magnitude slower** than LogEI per-iteration, and JES fails on
  Michalewicz despite competing with LogEI on Ackley.
* On the 7D Speed Reducer with 11 black-box constraints, LogCEI converges faster than the
  trust-region-based SCBO baseline; on at least one constrained problem, LogCEI improves upon the
  best results in the original engineering literature **using three orders of magnitude fewer
  evaluations** (Appendix D.7).
* For parallel BO on 16D Ackley at batch size **q=32**, jointly optimized qLogEI matches or exceeds
  sequential-greedy qLogEI, and both dominate canonical qEI (Figure 5).
* On the 100D embedded Hartmann6 (q=4), qLogEI plus a SAAS prior reaches the best observed value
  near `-3.5` while canonical qEI plateaus around `-1.5`; canonical-GP qLogEI eventually catches up
  with SAAS-prior qEI (Figure 6).
* On the 30D cell-network multi-objective problem at q in {4, 8, 16}, qLogEHVI reaches a hypervolume
  of about **0.06** while canonical qEHVI tops out near 0.04, and qLogEHVI matches or beats JES
  (Figure 7).
* On 16D DTLZ2 at q=16, qLogNEHVI takes about **three batches longer** than baselines to first
  improve over the reference point but then dominates the hypervolume curve.
* **Theorem 1** gives a probabilistic lower bound on the fraction of the domain where canonical EI's
  argument falls below any floating-point threshold B, formally explaining the empirical
  vanishing-gradient phenomenon in Figure 1 (where >90% of points have `|grad EI| < 1e-10` by n=1000
  in d=8 on Ackley).
* **Lemma 2** bounds the qLogEI-vs-qEI relative approximation error by
  `(q^tau_max - 1) qEI(X) + log(2)*tau0*q^tau_max`, giving a constructive recipe for choosing
  temperatures.

## Innovations

### Diagnosing the Vanishing-Gradient Pathology of EI

The paper is the first to identify, prove, and quantitatively characterise that the entire EI family
suffers from numerical vanishing gradients in floating-point arithmetic — not because EI is
mathematically zero, but because naive implementations evaluate `phi(z) + z*Phi(z)` to exactly zero
in double precision for `z` more negative than around `-37`. Theorem 1 formalises when this regime
is entered and shows it gets worse with dimension and as the BO loop closes the optimality gap.

### Stable Analytic LogEI via Piecewise log_h

The piecewise log_h evaluation in Equation 9, with its asymptotic `-z^2/2 - 2*log(|z|)` branch
beyond `-1/sqrt(eps)`, is the technical core. It improves on prior log-EI implementations in SMAC
1.0 and RoBO by remaining stable for arbitrarily negative arguments, where those earlier
implementations still produced NaN or zero. This makes EI's gradient available across the full
floating-point domain.

### Smooth-Max-Plus Reformulation for Monte Carlo qEI / qEHVI

For batch acquisitions, the discrete max-plus utility has not just numerically but mathematically
zero gradients on most of the domain. Replacing the discrete max-plus with `softplus + L^(1/tau)`
norm and applying the log everywhere produces qLogEI and qLogEHVI as drop-in replacements with
bounded approximation error (Lemma 2). qLogNEHVI extends this to the noisy multi-objective case that
t0078 actually uses.

### Fat-Tailed Non-Linearities for Large-Batch Parallel BO

For large q (e.g. q >= 32), canonical softplus saturates, undoing the smoothing. The paper
introduces **fatplus** and related fat-tailed approximations (Appendix A.4) that retain gradient
signal at large batch sizes, enabling joint batch optimization to be competitive with — and
sometimes exceed — the previously-dominant sequential-greedy strategy.

### Drop-In BoTorch Implementation

All methods (qLogEI, qLogCEI, qLogEHVI, qLogNEHVI) are released as part of BoTorch with the same
APIs as their canonical counterparts. This is the practical innovation that makes the result
immediately deployable: callers just swap the acquisition class.

## Datasets

This is a methods paper; benchmarks are synthetic test functions and engineering design problems
rather than collected datasets. Specifically:

* **Synthetic test functions**: Sum-of-Squares (10D), Ackley (2D, 8D, 16D), Michalewicz, Hartmann6
  (embedded in 100D), DTLZ2 (16D).
* **Engineering design problems** (4 constrained black-box benchmarks): 3D tension-compression
  string with 4 constraints, 4D pressure vessel with 4 constraints, 4D welded beam with 5
  constraints, 7D speed reducer with 11 constraints; same set used by Eriksson and Poloczek (SCBO,
  2021).
* **Real-world-inspired**: 30D cell-network coverage-and-capacity optimization (Dreifuerst et al.
  2021), 100D rover trajectory planning, 103D SVM hyperparameter tuning (a 100-feature subset of the
  388D problem from Eriksson and Jankowiak 2021), laser-plasma acceleration multi-objective
  benchmark (Irshad et al. 2023, with public dataset DOI 10.5281/zenodo.7565882), and vehicle
  crash-safety multi-objective design.

The reference SVM dataset feature subset and BoTorch implementations of all benchmarks are publicly
available through the paper's BoTorch contribution.

## Main Ideas

* **Replace canonical qEI / qNEHVI with qLogEI / qLogNEHVI in any BoTorch BO loop** — they are
  drop-in replacements with provably equivalent or near-equivalent optima, no extra compute, and
  dramatically better optimization behaviour. This is exactly the migration t0078 is performing away
  from t0076's deprecated qNEHVI.
* **Vanishing gradients explain inconsistent EI results in the BO literature**: when comparing BO
  methods, much of the apparent advantage of "fancier" acquisitions like JES or GIBBON over EI in
  prior work is actually attributable to canonical EI's numerical breakdown, not a fundamental
  algorithmic deficit of EI. This shifts how to interpret prior negative results for EI-based
  multi-objective DSGC tuning.
* **Joint batch optimization becomes practical with qLogEI**: the standard sequential-greedy
  workaround for parallel BO can be replaced with single joint optimization at batch sizes up to
  q=32 without losing performance, reducing implementation complexity for parallel evaluation
  scheduling on the t0078 worker pool.
* **Temperature tuning matters for qLogEI**: the smoothing parameters `tau0` and `tau_max` must be
  set low enough (Lemma 2 gives the recipe) for qLogEI to inherit qEI's optimum tightly. Use
  BoTorch's default temperature schedule unless there is a specific reason to deviate.
* **Performance gap grows with problem dimensionality and constraint count**: t0078's tiered AHP
  formulation has high-dimensional channel-parameter spaces, so qLogNEHVI's advantage over qNEHVI is
  expected to be larger than on the simple synthetic benchmarks the BoTorch tutorial uses.

## Summary

This paper identifies and corrects a numerical pathology that has silently degraded the entire
Expected Improvement family of BO acquisition functions for over two decades. The authors prove
(Theorem 1) that as a BO algorithm closes the optimality gap and the GP posterior becomes
informative, EI's argument `(mu - y*)/sigma` falls into a regime where naive floating-point
implementations evaluate to exactly zero across most of the search space. Once the value is zero,
the gradient is zero, so multi-start gradient-based optimizers — the standard practice in BoTorch
and most BO packages — degenerate into random search precisely when one needs them most.

The fix is a careful reformulation of every EI variant in log-space. Analytic LogEI uses a piecewise
stable `log_h` with an asymptotically quadratic branch for very negative arguments. Monte Carlo
qLogEI replaces the discrete `max_j [.]+` of qEI with a softplus + L^(1/tau)-norm smoothing inside a
log-space estimator, with bounded approximation error (Lemma 2). The same recipe is applied to
constrained EI (LogCEI, qLogCEI), expected hypervolume improvement (qLogEHVI), and noisy expected
hypervolume improvement (qLogNEHVI). Fat-tailed non-linearities (fatplus) are introduced to keep
large-batch parallel BO numerically well-behaved.

Empirically the LogEI family wins or ties everywhere it is tested. On 10D Sum-of-Squares canonical
EI stalls after about 75 evaluations while LogEI continues to descend. On Ackley at d=16 the gap
between LogEI and EI is the entire range of the function. LogCEI matches or beats SCBO on
constrained engineering benchmarks while sometimes improving on the best results in the original
engineering literature using three orders of magnitude fewer evaluations. qLogNEHVI dominates qNEHVI
on multi-objective benchmarks including the 30D cell-network coverage problem, and joint batch
optimization at q=32 becomes competitive with sequential-greedy strategies. Crucially the methods
are drop-in replacements: same APIs, same compute cost, identical-or-near-identical optima.

For this project, this paper is the methodology reference for the t0076-to-t0078 migration from the
deprecated `qNoisyExpectedHypervolumeImprovement` (qNEHVI) to
`qLogNoisyExpectedHypervolumeImprovement` (qLogNEHVI). t0078 inherits exactly the conditions where
qLogNEHVI is expected to dominate canonical qNEHVI: a multi-objective DSI-and-firing-rate
optimization over a tiered, multi-channel AIS parameter space with comparatively high
dimensionality, where canonical qNEHVI's vanishing-gradient regime is reached early. Citing Ament et
al. (2023) is therefore mandatory whenever t0078 reports the optimiser switch, and practical
recommendations from the paper — keep BoTorch's default temperature schedule, prefer joint batch
optimization at the worker counts t0078 uses, and treat any apparent qLogNEHVI under-performance as
either a surrogate-model issue or evidence the entire EI family is mis-specified for this objective
— should guide implementation choices in t0078 plan.md and results_detailed.md.
