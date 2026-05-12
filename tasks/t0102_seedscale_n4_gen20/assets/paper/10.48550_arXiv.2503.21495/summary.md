---
spec_version: "3"
paper_id: "10.48550_arXiv.2503.21495"
citation_key: "Budszuhn2025"
summarized_by_task: "t0102_seedscale_n4_gen20"
date_summarized: "2026-05-11"
---
# Adaptive Resampling with Bootstrap for Noisy Multi-Objective Optimization Problems

## Metadata

* **File**: `files/budszuhn_2025_adaptive-bootstrap-resampling.pdf`
* **Published**: 2025 (arXiv v2, 24 April 2025)
* **Authors**: Timo Budszuhn 🇩🇪, Mark Joachim Krallmann 🇩🇪, Daniel Horn 🇩🇪
* **Venue**: arXiv preprint (cs.LG)
* **DOI**: `10.48550/arXiv.2503.21495`

## Abstract

The challenge of noisy multi-objective optimization lies in the constant trade-off between exploring
new decision points and improving the precision of known points through resampling. This decision
should take into account both the variability of the objective functions and the current estimate of
a point in relation to the Pareto front. Since the amount and distribution of noise are generally
unknown, it is desirable for a decision function to be highly adaptive to the properties of the
optimization problem. This paper presents a resampling decision function that incorporates the
stochastic nature of the optimization problem by using bootstrapping and the probability of
dominance. The distribution-free estimation of the probability of dominance is achieved using
bootstrap estimates of the means. To make the procedure applicable even with very few observations,
we transfer the distribution observed at other decision points. The efficiency of this resampling
approach is demonstrated by applying it in the NSGA-II algorithm with a sequential resampling
procedure under multiple noise variations.

## Overview

Budszuhn and colleagues address a central efficiency problem in noisy multi-objective optimization:
how to allocate a finite evaluation budget between exploring new candidate solutions and improving
the precision of existing estimates through resampling. Their target algorithm is NSGA-II, the
canonical elitist non-dominated sorting genetic algorithm, which is particularly sensitive to noise
because an overestimated point can poison the Pareto front for many generations. Existing resampling
strategies are either static (allocate a fixed budget per point), rank-based, variance- based, or
RTEA-style elitist re-evaluation; none of them simultaneously account for both a point's proximity
to the Pareto front and the variability of its objective estimates.

The authors propose Adaptive Resampling with Bootstrap (ARB), a sequential resampling decision
function built on the probability of dominance, where the dominance distribution is estimated by
nonparametric bootstrap of the sample means rather than by assuming Gaussianity (as in earlier work
by Teich). To make bootstrap feasible when a point has only one or two observations, they introduce
an error-pooling trick: a global dispersion set E of size 100 is maintained from the most recent
re-evaluated points across the population, and bootstrap samples for a sparsely evaluated point are
drawn partly from this global set and partly from the point's own residuals. A point is resampled
only when its estimated probability of dominating any current Pareto-front member falls in a window
(alpha_l, alpha_u), so neither already-dominated junk nor already- confirmed elites waste budget.

The simulation study (UPC test functions, NSGA-II popSize 40, 50,000 evaluations per run, 30
replications, Gaussian and chi-squared noise at six standard deviations) shows that ARB is
significantly more robust than RTEA and the other dynamic NSGA-II resampling strategies, and is
competitive with the simple static-N strategy under chi-squared noise. The contribution is therefore
not a single best algorithm but a flexible, distribution-free decision rule that adapts to unknown
noise shape and magnitude.

## Architecture, Models and Methods

ARB is implemented as a drop-in sequential resampling decision function for NSGA-II. The full
procedure is:

* **Initialisation**: a population of size M_i greater than 100 is sampled and evaluated once; the
  best 100 (by NSGA-II non-dominated sort) are evaluated a second time. Each pair (y1, y2)
  contributes scaled residuals (y - mean) * sqrt(N / (N - 1)) to a global dispersion set E of size
  100 with zero mean. Population size during optimisation is fixed at 40.
* **Per-generation loop** (sequential resampling): for every point xj in the current population,
  bootstrap 100 sample-mean draws Y_tilde for xj and for each Pareto-front member xs. If xj has N_j
  observations, each bootstrap draw is built as
  `Y_tilde = ybar_j + (1/N) * (E_tilde + sum_{n=1..N-1} sqrt(N / (N - 1)) * (Y_tilde_n - ybar_j))`,
  where E_tilde is drawn from E and the remaining N - 1 terms from the point's own residuals.
* **Probability of dominance estimate**: P_hat(xj precedes xs) = (1 / (Ni * Nj)) * sum of
  indicator-of-componentwise-less-than over the 100 x 100 bootstrap pairs.
* **Decision function Delta_PD(S_hat, j)**: resample xj only if alpha_l less than max over Pareto
  front of P_hat(xj weakly dominates xs) less than alpha_u. Outside this band, do not resample.
  Authors sweep alpha_l in {0.1, 0.2, 0.5} and alpha_u in {0.75, 0.9, 1.0}.
* **Error-base maintenance**: the 100 most recently observed scaled residuals are kept, mean-
  centred before every sampling step.
* **Bootstrap parameters**: B = 100 bootstrap samples per point per generation; the global E set is
  forced to size 100 to ensure 100 distinct bootstrap draws are available even after a single
  observation.

Competing strategies are implemented in the same framework: NSGA-II without resampling (static N =
1), static resampling with N in {1, 5, 10, 20}, dynamic decision functions from Siegmund-Ng-Deb
(domination-strength, rank-based, time-based), standard-error dynamic resampling with sigma_thr in
{0.01, 0.05, 0.1}, and the Rolling Tide Evolutionary Algorithm (RTEA) with one resample per
iteration, starting population 40, refinement fraction z = 0.1. All algorithms share the same
mutation and crossover operators. Test problems are the UPC multi-objective benchmark functions
[14]; noise is added as `Y_d = g_d(x) + v_d(x) * eps` with eps drawn from N(0, 1) or (1 / sqrt(2k))
\* (chi2_k - k) for k in {1, 2}, and a constant scale v_d in {0.01, 0.1, 0.5, 1, sqrt(2), 2}. Each
setting is run for 30 independent replications of 50,000 evaluations. Two unbiased comparison
protocols are used: random 20-vs-10 replication splits for parameter selection and comparison (100
random splits), and a realistic pre-study protocol that uses an initial 5,000-evaluation run to fix
parameters, then 30 replications of the full 50,000- evaluation run for hypothesis testing. Quality
measures are scaled dominated hypervolume HV and inverted generational distance IGD_p; IGD results
are reported as substantively similar to HV.

## Results

* Under Gaussian noise across all six standard deviations, ARB outperforms RTEA and the dynamic
  NSGA-II family in the majority of split-comparison runs (Figure 1; Section 6.1).
* Under chi-squared noise, the no-resample static NSGA-II (N = 1) wins most settings because
  one-sided bounded noise cannot strongly overestimate a point; ARB still ranks second across all
  noise types.
* In the realistic 5,000-evaluation pre-study counts of best-performing strategy across all settings
  (Table 1): **ARB chi2 = 1194, NSGA-II STA chi2 = 1614, NSGA-II DYN chi2 = 175, RTEA chi2 = 617**;
  **ARB Gaussian = 549, NSGA-II STA Gaussian = 280, NSGA-II DYN Gaussian = 542, RTEA Gaussian =
  609**; **ARB no-noise = 107, NSGA-II STA no-noise = 104, NSGA-II DYN no-noise = 17, RTEA no-noise
  = 72**.
* Statistical tests with parameters chosen on the 5,000-evaluation pre-study show ARB significantly
  better than RTEA in **64.7 percent** of simulated scenarios and significantly worse in **24.7
  percent**.
* ARB beats the other dynamic sequential resampling strategies (domination-strength, rank-based,
  time-based, standard-error) in **71.0 percent** of scenarios and loses in only **8.7 percent**.
* The one-shot static-N strategy is the only competitor that wins more often than ARB overall
  (**22.4 percent vs 20.7 percent** of scenarios), and the gap is driven entirely by the chi-squared
  regime.
* Dynamic NSGA-II resampling strategies as a group perform poorly across all noise types except
  high-variance Gaussian, where they begin to win a small fraction of settings.

## Innovations

### Bootstrap-Based Probability of Dominance

ARB replaces Teich's normal-distribution assumption for the probability of dominance with a
nonparametric bootstrap estimate of the sample-mean distribution, removing the need to specify or
estimate a noise model. This makes the decision rule robust to skewed noise (chi-squared) and to
unknown distribution shapes that arise in practice (e.g., chi-squared-like error from bad train-test
splits in hyperparameter optimisation).

### Error Pooling Across the Population (Homoscedastic Transfer)

To enable bootstrap with as few as N = 1 observations at a point, the authors maintain a global
dispersion set E of the 100 most recent scaled residuals across the population and mix global draws
with point-local draws. As N grows, point-local variability progressively dominates. This is the key
practical innovation: it avoids the cost of a mandatory second evaluation per point while preserving
statistical interpretability.

### Two-Sided Decision Window with alpha_l and alpha_u

The decision rule does not simply threshold "is this point promising?". It carves out an explicit
no-resample band on both sides: already-dominated junk (P less than alpha_l) and already-confirmed
elites (P greater than alpha_u) are both refused additional budget. This is a clean structural
generalisation of rank-based and standard-error rules into a single probabilistic statement.

## Datasets

This is a methodological paper with simulated benchmarks. The objective functions are the **UPC
multi-objective test functions** [14], used as the noise-free mean function. Noise is injected as
Gaussian N(0, 1) or scaled chi-squared (1 / sqrt(2k)) * (chi2_k - k) with k in {1, 2}, multiplied by
a constant noise scale v_d in {0.01, 0.1, 0.5, 1, sqrt(2), 2}, plus a no-noise control. Each
combination is run for 30 replications of 50,000 evaluations under each of: NSGA-II with no
resampling, NSGA-II with static resampling N in {1, 5, 10, 20}, NSGA-II with dynamic resampling
(domination-strength, rank-based, time-based, standard-error), RTEA, and ARB with alpha_l in {0.1,
0.2, 0.5}, alpha_u in {0.75, 0.9, 1.0}, popSize 40. No real-world dataset is used. Code availability
is not stated in the paper text.

## Main Ideas

* **Static N is not always wrong** -- with bounded/skewed noise (chi-squared), the simplest static N
  = 1 strategy wins more scenarios than any adaptive strategy in this study. For t0102's question
  (replace static N_SEEDS with adaptive resampling), this is a serious caveat: an adaptive scheme is
  only clearly better than static N when the noise is approximately Gaussian.
* **Sequential resampling beats one-shot for elitist algorithms** under noisy MOO, but only when the
  decision rule jointly considers both Pareto-rank proximity and variance. Pure variance-only
  (standard-error) and pure rank-only (domination-strength, rank-based) rules underperform.
* **Probability of dominance is the right summary statistic** for combining rank and variance.
  Bootstrap estimation of it removes the distributional assumption that previously limited this
  approach.
* **Error pooling is essential** for any adaptive resampler that must operate from a single
  evaluation per point. Without a global dispersion set, no statistical decision can be made before
  at least two evaluations, which already commits the budget the adaptive scheme is trying to save.
* **Heteroscedasticity is an open question**: the paper only studies homoscedastic noise. DSGC
  multi-seed loss noise across morphologies / parameter sets is plausibly heteroscedastic, so this
  technique would need empirical validation before adoption in t0102's follow-up.

## Summary

Budszuhn, Krallmann, and Horn study the resource-allocation problem at the heart of noisy
multi-objective optimization: every evaluation either explores a new candidate or sharpens an
existing estimate, and the algorithm must decide which without knowing the noise distribution. Their
target is NSGA-II, an elitist algorithm that is particularly damaged by overestimated points. Prior
work either fixes a static number of evaluations per point, uses rank or variance heuristics, or
assumes Gaussian noise to estimate a probability of dominance. None of these adapt to unknown noise
shape.

The authors' contribution is Adaptive Resampling with Bootstrap (ARB), a sequential decision
function that bootstraps the sample-mean distribution at each point, estimates the probability of
dominating any current Pareto-front member from 100 paired bootstrap draws, and triggers resampling
only when that probability lies in a tunable window (alpha_l, alpha_u). To make the bootstrap work
after a single observation, they maintain a population-level pool E of the 100 most recent scaled
residuals and mix global draws with point-local draws, weighting the local component more heavily as
N grows. The full evaluation uses UPC benchmark functions with Gaussian and chi-squared noise at six
standard deviations, NSGA-II popSize 40, and 30 replications of 50,000 evaluations per setting.

ARB is the most flexible algorithm tested. With realistic pre-study parameter selection it ranks
second across all noise regimes and significantly beats RTEA in **64.7 percent** of scenarios and
the other dynamic NSGA-II resamplers in **71.0 percent**. The only competitor that wins overall is
static N = 1 (no resampling), and only because chi-squared noise is one-sided bounded -- when
overestimation is impossible, paying for resamples is pure waste. Under Gaussian noise, RTEA's
strict elitism does well but is still beaten by ARB on average. The headline finding is therefore
not "ARB is universally best" but "ARB is the only strategy that does not collapse on at least one
noise type, because its decision rule is distribution-free".

This paper matters for t0102 because the current DSGC compartmental-modelling pipeline fixes the
number of stochastic-seed evaluations (N_SEEDS) statically per design point -- exactly the static N
strategy the paper compares against. ARB is the natural candidate for a follow-up suggestion
S-0102-NEW-01 that would replace that constant with an adaptive resampler driven by the probability
of dominance over the running Pareto front of (loss, cost) or (loss, biological plausibility).
Before adoption we must verify that DSGC noise is closer to Gaussian than to a bounded chi-squared
shape -- if seed-to-seed loss variation is heavily right-skewed and one-sided, the paper's own
results suggest static N might still be near-optimal and the engineering cost of ARB would not pay
back. Heteroscedasticity across morphologies is also untested in the paper and must be checked
empirically before any production switch.
