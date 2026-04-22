# Creative Thinking: Alternative Search Strategies and Cost-Reduction Tricks for the Future Optimiser

## Objective

The plan already compares five baseline search strategies (grid, random, CMA-ES, Bayesian
optimisation, surrogate-NN-GA) against three compute modes and four GPU tiers, and recommends
Surrogate-NN-GA × Surrogate-NN-GPU × RTX 4090 at a central \$50.54 with a 0.5×-2× sensitivity band
of \$23-\$119. This note explores creative alternatives *beyond* that baseline grid — methods that
either exploit corpus-documented structure (Cuntz 2010 symmetries, Mainen 1996 morphology-biophysics
coupling, Poleg-Polsky 2026 surrogate pipeline) or borrow well-established tricks from adjacent
numerical-methods literature — to ask whether any of them materially change the headline
recommendation or buy a meaningful cost / risk reduction.

## Alternatives Considered

1. **Multi-fidelity surrogates (coarse → fine compartmental cascade)**. (a) Train a cheap surrogate
   on a coarsened backbone (e.g. t0024 single-compartment kinetics or a 3.8 s/angle-trial t0022
   deterministic path), filter to the top 10 % of candidates, then re-score only those on the 12.0
   s/angle-trial stochastic AR(2) model. (b) Differs from the baseline surrogate-NN-GA, which trains
   one surrogate at a single fidelity. (c) Cost impact: the central surrogate-training USD (\$41.56
   = 5000 deterministic 91 s sims at RTX 4090) plausibly drops 2-3×, pulling the recommended cell
   down to ~\$25-\$35. (d) Risk: coarsening violates the [deRosenroll2026] / Jain-2020 5-10 μm
   subunit floor for the DSI objective, so the *coarse* fidelity cannot be coarse in compartment
   count, only in `dt`, trial count, or stochastic AR(2) depth. Needs careful fidelity selection.

2. **Active learning / acquisition-function-directed sampling**. (a) Replace uniform surrogate
   training with a Bayesian-active-learning loop: at each iteration, pick the next NEURON evaluation
   that maximises surrogate uncertainty or expected-information-gain on DSI. (b) Differs from the
   baseline, which treats the 5000-sample surrogate-training burn as a one-shot Latin-hypercube or
   Sobol sample. (c) Cost impact: empirically, active learning reduces the samples needed for a
   fixed surrogate accuracy by **2-5×** in the generic ML literature; applied here it could take the
   training burn from \$41.56 to \$10-\$20. (d) Risk: no DSGC-specific precedent in the corpus; the
   acquisition function adds control-flow complexity and a fresh hyperparameter surface that itself
   needs tuning.

3. **Transfer learning / surrogate warm-start from t0022 and t0024 checkpoints**. (a) Initialise the
   surrogate from features or a partial NN pre-trained on the 16-parameter HHst gbar topology
   already exercised by the t0022 testbed and the t0024 port's V_rest / stochastic-AR(2) sweeps; the
   t0026 artefacts provide thousands of existing (gbar, DSI) evaluations. (b) Differs from the
   baseline, which assumes the surrogate trains from scratch on a cold 5000-sample burn. (c) Cost
   impact: if half the 5000-sample training burn is replaced by existing evaluations, surrogate
   training USD could drop from \$41.56 to ~\$20, pulling the recommended cell to ~\$30. (d) Risk:
   the existing evaluations cover only the 16 HHst gbar parameters, not the 5 Cuntz morphology
   scalars or the top-10 VGC expansion, so transfer is partial and may introduce sampling bias
   unless the warm-start weights are clearly isolated from the new axes.

4. **Batched Bayesian optimisation (parallel proposals across workers)**. (a) Instead of sequential
   BO, propose a batch of q ~ 8-32 candidates per round using q-EI / q-UCB, each evaluated on a
   separate Vast.ai worker. (b) Differs from the baseline BO row, which assumes sequential
   evaluation and therefore 500 sequential rounds for 500 samples. (c) Cost impact: wall-clock
   compresses by ~q× with total GPU-hours unchanged — relevant only if the 2-h checkpoint cliff or
   the CREATION_TIMEOUT_SECONDS=600 provisioning gate is the binding constraint, otherwise no USD
   saving. (d) Risk: BO itself has no DSGC precedent in the corpus ([PolegPolsky2026, Ezra-Tsur2021]
   use evolutionary methods), and GP batched acquisition scales poorly above ~30 dims, so this buys
   schedule compression but not strategy robustness.

5. **Asynchronous parallel CMA-ES across N Vast.ai workers (horizontal scaling)**. (a) Run
   population members on N workers concurrently, each finishing asynchronously and feeding back into
   the evolution-path update. (b) Differs from the baseline CMA-ES row, which implicitly serialises
   λ = 13 candidates per generation on one worker. (c) Cost impact: pure wall-clock compression at
   fixed USD (1300 sims × \$0.50/h / N workers) — makes CMA-ES competitive on wall-clock with
   surrogate-NN-GA while staying at its \$34 central USD. (d) Risk: Vast.ai provisioning overhead
   (`MAX_RETRY_OFFERS=3`, `POLL_INTERVAL_SECONDS=30`) multiplied by N workers dominates for short
   individual jobs; the per-worker `CREATION_TIMEOUT_SECONDS=600` becomes the floor.

6. **Exploit Cuntz 2010 morphology symmetries to halve the morphology sub-space**. (a) [Cuntz2010]
   documents that `bf` maps monotonically to electrotonic compartmentalisation and that root
   location symmetries exist across DSGC-like arbors. Use those symmetries (e.g. reflect-and-merge
   candidate trees with equivalent `bf` but mirrored root offsets) to reduce the effective
   morphology axis from 5 to 3-4 free scalars. (b) Differs from all baseline strategies, which treat
   the 5 Cuntz scalars as independent. (c) Cost impact: a 30-50 % sample reduction on the morphology
   axis, which at 25 dims is a ~10 % total sample reduction — modest (\$5 saved at the central
   cell). (d) Risk: the monotonicity claim is corpus-documented only at the single-parameter level;
   higher-order symmetries are assumed, not proven for DSGC.

7. **Evolutionary multi-objective extension (NSGA-II with DSI + energy + wiring cost)**. (a)
   [Ezra-Tsur2021] already uses NSGA-II — a trivial extension would add a second objective (spike
   energy proxy, or Cajal cytoplasm / total wiring length à la [Cuntz2010]) to expose the
   DSI-vs-energy Pareto front. (b) Differs from the baseline, which optimises DSI scalar only. (c)
   Cost impact: at equal sample count, roughly neutral (NSGA-II already is the default selector) —
   but produces a Pareto set rather than one winner, improving scientific yield per dollar. (d)
   Risk: `task_description.md` explicitly marks multi-objective out of scope for *this* planning
   task; it must be deferred to a future-task suggestion, not folded into the recommendation.

## Recommendation

The baseline recommendation — Surrogate-NN-GA × Surrogate-NN-GPU × RTX 4090 at \$50.54 central — is
already near-optimal under corpus-justified strategies, and none of the seven alternatives changes
its ranking. However, two alternatives are worth **supplementing** the recommendation with:
**multi-fidelity surrogates (#1)** and **transfer-learning warm-start (#3)**. Both attack the
dominant \$41.56 surrogate-training cost rather than the near-zero \$8.98 inference cost, and both
are compatible with the baseline pipeline as drop-in optimisations during the training phase.
Combined, they are plausibly worth **\$15-\$25 of savings** on the central cell and, more
importantly, halve the surrogate-training burn that [PolegPolsky2026] left unquantified — the single
largest sensitivity-band contributor in the current plan.

Active learning (#2) and asynchronous CMA-ES (#5) are attractive but corpus-unsupported and add
engineering complexity; they should be noted as future-task suggestions rather than folded into the
recommended pipeline now. Batched BO (#4), Cuntz symmetries (#6), and multi-objective (#7) are
interesting but produce small cost savings or are explicitly out of scope. The headline
recommendation therefore stands, with a recommended annotation that the surrogate-training phase
should (a) reuse t0022/t0024 evaluations as warm-start and (b) treat fidelity as a configurable
lever, not a fixed choice.

## Limitations

* **No internet-sourced benchmarks**. Quantitative claims (2-5× active-learning speedup, q×
  batched-BO compression) are drawn from general ML heuristics, not from the downloaded DSGC corpus.
  They are directional, not auditable.
* **Gradient-based autodiff-through-NEURON** was considered and rejected already in `plan.md` §
  Alternatives; not re-examined here.
* **Schedule-compression alternatives** (batched BO, async CMA-ES) save wall-clock but not USD; they
  only matter if the researcher adds a wall-clock constraint that the current plan does not declare.
* **Multi-objective extension** is deliberately deferred per `task_description.md` out-of-scope
  clause; listed only as a suggestion-track idea.
* **Quantitative re-scoring** of alternatives #1, #2, #3 under the sensitivity grid was not
  performed — it would require extending `cost_model.py`, which is scope for a future implementation
  task.
