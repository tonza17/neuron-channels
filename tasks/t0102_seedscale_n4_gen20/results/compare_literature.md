---
spec_version: "1"
task_id: "t0102_seedscale_n4_gen20"
date_compared: "2026-05-12"
---
# Compare to Literature: 68-d NSGA-II at Seeds=2, N_EVAL_SEEDS=4, Gens=20

## Summary

Two random-init NSGA-II seeds (44, 55) on the 68-d Bed B + procedural-morphology DSGC substrate
produced **0/2,592** strict joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz AND rob >= 0.7),
replicating t0099's null at a 5x noise-replicate cut and 2.5x generation extension. Compared against
five methodological references (Mohacsi2024, Druckmann2007, Hay2011, VanGeit2016, PolegPolsky2026)
and two noise-theory references (Dang2023, Morinaga2024), our **2,592-evaluation budget** is **1-2
orders of magnitude below** every cited compartmental-neuron MO study and our **algorithm choice
(NSGA-II)** is documented mid-pack relative to CMAES/IBEA/PSO on 9-12 d benchmarks. Under Hay2011's
**0.4%** joint-acceptance base rate, our budget predicts **~10 expected joint-pass cells**; we found
**0**, which strengthens the substrate-difficulty (or objective-misspecification) reading already
flagged in `creative_analysis.md` Section 1. The t0091 single joint-pass cell, reframed in this
task's reporting as a one-mutation descendant of an alt_topology anchor clone, is consistent with
the literature view that warm-start delivers a **5-10x HV head-start**
[Ament2023, as cited via t0099 `compare_literature.md`] rather than an algorithmic discovery.

## Comparison Table

### Budget envelope vs cited references

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Druckmann2007 NSGA-II 12-d interneuron [Druckmann2007, p. 11] | Total evaluations per fit | 300000 | 2592 | -297408 | 116x under standard |
| Hay2011 NSGA-II 22-d L5PC [Hay2011, Methods, p. 4] | Total evaluations per fit | 500000 | 2592 | -497408 | 193x under standard |
| Mohacsi2024 Neuroptimus 12-d CA1 benchmark [Mohacsi2024, Methods, p. 6] | Total evaluations per algorithm-run | 10000 | 2592 | -7408 | 3.9x under matched-budget benchmark |
| VanGeit2016 BluePyOpt IBEA 18-d L5PC [VanGeit2016, Use Case 2, p. 11] | Total evaluations per fit | 10000 | 2592 | -7408 | 3.9x under modern engineered minimum |
| PolegPolsky2026 DSGC ML search [PolegPolsky2026, Methods, via t0101 brainstorm] | Total evaluations per configuration | 300000 | 2592 | -297408 | 116x under the motivating paper |
| Hay2011 L5PC joint-acceptance yield [Hay2011, Results, p. 7] | Joint-pass cells / total evals | 2000 / 500000 = 0.40% | 0 / 2592 = 0.00% | -0.40 pp | Expected 10 cells under Hay base rate; we found 0 |
| Druckmann2007 strict-pass yield [Druckmann2007, Results, p. 13] | Strict-pass cells / total evals | 300 / 300000 = 0.10% | 0 / 2592 = 0.00% | -0.10 pp | Expected ~2.6 cells under Druckmann base rate; we found 0 |
| Mohacsi2024 NSGA-II rank vs IBEA on 9-d active cell [Mohacsi2024, Use Case 4, Figure references] | Final error (NSGA-II / IBEA ratio) | ~10x (NSGA-II worse) | not directly comparable | n/a | Their evidence flags NSGA-II as mid-pack on 9-12 d; we run at 68 d |
| Dang2023 NSGA-II noisy LOTZ threshold [Dang2023, Theorem 8, p. 6] | Critical noise prob `p` for polynomial runtime | < 0.50 | effective p << 0.50 at N=4 | n/a | Our N=4 explicit-averaging puts us in the polynomial regime per phase-transition theorem |
| PolegPolsky2026 vs t0091 / t0099 / t0102 best PD-rate [PolegPolsky2026, Results table via t0101 brainstorm] | Best preferred-direction DSI under unconstrained config | 73.1% +/- 2.4% (subthreshold-voltage) | 0.958 (spike-rate, seed 44 gen 7) | n/a | Different DSI conventions; both >= 0.5 threshold but units not directly comparable |

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0091 warm-start (5 anchors, gens=8, N=5) [t0091 `results_summary.md`] | Strict joint-pass cells | 1 (DSI=0.511, PD=35.1 Hz, rob=0.79) | 0 (seed 44), 0 (seed 55) | -1 | t0091 cell reframed as one-mutation alt_topology anchor clone per `creative_analysis.md` Section 2 |
| t0099 random-init (3 seeds, gens=5/8/8, N=20) [t0099 `results_summary.md`] | Strict joint-pass cells | 0 across 3 seeds (2208 evals) | 0 across 2 seeds (2592 evals) | 0 | Same null at 5x lower N and 2.5x more gens; pooled Wilson 95% upper CI < 0.0008 |
| t0099 best PD-rate (seed 22) [t0099 `results_summary.md`] | Max PD-rate (Hz) | 18.7 | 64.29 (seed 44) / 66.96 (seed 55) | +45.6 / +48.3 | t0102 reaches higher per-axis PD but at DSI ~ 0 |
| t0091 final HV (gen 2) [t0099 `compare_literature.md`] | Hypervolume at matched generation | 23.71 (gen 2) | 7.53 (seed 44 gen 14) / 3.39 (seed 55 gen 13) | -16.18 / -20.32 | Different reference points; both runs use anchor-based HV calibration so this comparison is qualitative |

## Methodology Differences

* **Budget**: t0102 ran **2,592 evaluations** (1,344 + 1,248 after the per-seed $4 cost watchdog cut
  both seeds short of generation 20). Druckmann2007 and PolegPolsky2026 each used **300,000**;
  Hay2011 used **500,000**; Mohacsi2024 and VanGeit2016 used **10,000**. t0102 is **116-193x below**
  the high-end envelope and **3.9x below** the modern Mohacsi/BluePyOpt engineered minimum.

* **Algorithm**: t0102 used NSGA-II (pymoo defaults: SBX eta=15, polynomial mutation eta=20). The
  most directly relevant external benchmark, Mohacsi2024, places NSGA-II **mid-pack** on
  multi-objective neuronal problems: CMAES wins essentially every benchmark, PSO is a close runner-
  up, **IBEA is the best multi-objective method**, and on Use Case 1 NSGA-II is worse than random
  search [Mohacsi2024, Results, p. 8]. Our project's NSGA-II choice predates this evidence.

* **Per-cell noise replicates**: t0102 used **N_EVAL_SEEDS=4** (explicit averaging of 4 trial-seed
  evaluations per direction); t0099 used N=20; Druckmann2007 used 15 traces per cell (5 reps x 3
  amplitudes) but averaged feature *errors* not traces [Druckmann2007, Methods, p. 9];
  PolegPolsky2026 used deterministic single-pass evaluation. Per Morinaga2024 Theorem 3, explicit
  averaging at K=4 is in the slow-polynomial-improvement regime only if the per-objective noise
  stability index alpha > 1 [Morinaga2024, Theorem 3, p. 5]; if any objective (likely the
  near-zero-firing DSI) sits closer to alpha = 1, our averaging is "nearly inert" per the same
  theorem.

* **Population and seed/generation balance**: t0102 used **pop=96, gens<=20, GA seeds=2**.
  Druckmann2007 used pop=300, gens=1000, 1 seed; Hay2011 used pop=1000, gens=500, 1 seed;
  Mohacsi2024 used pop=100, gens=100, 10 seeds; PolegPolsky2026 used **pop=10, gens=300-1000, 50-100
  seeds** [PolegPolsky2026, Methods, via t0101 brainstorm]. PP-2026 is a **thin-pop / many-seeds /
  many-gens** recipe; we ran a **thick-pop / few-seeds / few-gens** recipe. The PP-2026 envelope
  spent its budget on diverse parameter initialisation, not noise averaging.

* **Warm-start**: t0091 used 5-anchor warm-start; t0099 and t0102 used pure LHS random init.
  Druckmann2007 hand-shifted Nat/Kslow voltages by +10 mV / +20 mV before optimisation
  [Druckmann2007, Methods, p. 8]; Hay2011 used a restricted Ih upper bound [Hay2011, Methods, p. 4].
  Both literature conventions amount to "informed init"; t0102 is **adversarial random init** vs
  this convention.

* **Population sizing under noise**: Dang2023 Theorem 8 requires `mu = Omega(n log n)` for noisy
  NSGA-II to retain polynomial runtime [Dang2023, Theorem 8, p. 7]. For our problem `n = 68`,
  `Omega(68 * log(68)) ~ 290`; our pop=96 is **~3x below** the theoretical floor for noise survival.
  This is one of the levers Dang2023 explicitly flags as principled to increase before concluding
  noise is the blocker.

* **DSI convention**: PolegPolsky2026 measures DSI as **vector-sum subthreshold peak voltage over 12
  directions x 5 speeds** with values in [0, 1]; t0102 measures DSI as vector-sum on **spike rate
  over 16 directions at one speed**. Both share the 0.5 threshold convention but the underlying
  signal differs (voltage vs spike rate), so the absolute numbers are not directly comparable.

## Analysis

### Budget is the single most plausible reason for a null result

Mohacsi2024 ran **10,000 evaluations per algorithm-run** on 12-d problems and treated this as a
*matched-budget benchmark*. We ran **2,592 evaluations total across two seeds** on a **68-d**
problem. Linear-in-dimension scaling alone would suggest a baseline of `10000 * 68/12 ~ 56,667`
evaluations per run; we are at **2.3% of that** even ignoring the multi-objective complexity
multiplier. The Wilson 95% upper bound on our joint-pass rate from pooling t0099 + t0102 (0/4,800)
is **< 0.0008**, which is tight enough to reject base rates above 0.001 but cannot distinguish "true
zero acceptance" from "0.0001 acceptance"; either reading requires ~20,000+ additional evaluations
to resolve.

Under the Hay2011 base rate of **0.4%** joint-acceptance on a 22-d joint perisomatic+dendritic fit
[Hay2011, Results, p. 7], 2,592 evaluations *should* have yielded ~10 joint-pass cells. We found
**0**. This is either evidence that (i) our 68-d substrate is intrinsically harder than Hay2011's
22-d L5PC (likely true: 5.7x more dimensions, biological priors more stringent), (ii) the joint-pass
threshold is much stricter than Hay2011's per-feature 2 SD criterion (likely true: our threshold is
a hard 3-axis AND-clause), or (iii) our DSI vector-sum objective is internally mis-specified (very
likely true: Finding 1 in `results_detailed.md` identifies a divide-by-near-zero floating-point
artifact that pulls 27 of our cells to DSI=1.0 on silenced cells). The combined effect of (i)+(ii)
+(iii) is sufficient to explain a true zero result without invoking any algorithmic shortcoming of
NSGA-II.

### Algorithm choice is a second-order but non-zero factor

Mohacsi2024 explicitly recommends **IBEA** over NSGA-II for multi-objective neuronal optimisation
[Mohacsi2024, Discussion, p. 12], with IBEA finishing ahead of all three NSGA-II implementations on
the 9-d active model benchmark (Use Case 4). On their 12-d CA1 benchmark, the gap between NSGA-II
and IBEA narrows but **PSO and CMAES both close to within 5%** of the IBEA best while NSGA-II
trails. The single most defensible methodology change this evidence implies is **switch from NSGA-II
to IBEA** for any continuation of this line of work. NSGA-II being mid-pack at 9-12 d does not prove
it is wrong at 68 d, but the literature does not contain *any* evidence that NSGA-II outperforms
IBEA on neuron-fitting problems, so the burden of proof is on continuing with NSGA-II.

### Noise handling is theoretically adequate but practically marginal

Dang2023 proves NSGA-II survives Bernoulli noise with `p < 0.50` in polynomial expected time
[Dang2023, Theorem 8, p. 7], and reports qualitatively similar phase-transition behaviour under
Gaussian noise: 100% success at `sigma = n * 2^-4`, dropping to 0% at `sigma >= n * 2^-1`
[Dang2023, Results, p. 9]. Our DSGC noise per cell at N=4 is well below the catastrophic threshold,
so noise alone does not predict the null. However, Morinaga2024 Theorem 3 sharpens this: explicit
averaging is only effective when the noise stability index `alpha > 1`. Our DSI objective is a
vector-sum over a low-spike-count denominator; near zero, the noise distribution may be heavy-tailed
(alpha close to 1), in which case K=4 explicit averaging is *nearly inert*
[Morinaga2024, Theorem 3, p. 5]. **Switching the DSI objective to sign-averaging**
[Morinaga2024, Theorem 9, p. 8] would be theoretically more robust at the same compute cost, and is
the most direct literature-recommended change.

### Population/generation balance: thin-pop/many-gens vs thick-pop/few-gens

PolegPolsky2026's published recipe is **pop=10, gens=300-1000, seeds=50-100**
[PolegPolsky2026, Methods, via t0101 brainstorm]: a thin population sustained over many generations
and many random restarts. Our t0102 ran the inverted recipe (**pop=96, gens<=20, seeds=2**). At
equal total evaluation budget B = pop x gens x seeds, the PP-2026 recipe spends B on parameter-space
re-randomisation; the t0102 recipe spends B on within-front diversity preservation. Dang2023's
population-floor result `mu = Omega(n log n)` favours larger pop for noise survival, supporting the
t0102 choice on theoretical grounds. PP-2026's empirical success favours the opposite. **The
literature does not converge** on which is better; this is precisely the deferred suggestion
S-0101-03 (budget-matched ablation).

### Prior Task Comparison

The t0091 joint-pass cell (DSI=0.511, PD=35.1 Hz, rob=0.79 at `source_generation=2`) is the only
strict joint-pass cell in the entire t0080-t0102 NSGA-II lineage [t0091 `results_summary.md`]. Per
`creative_analysis.md` Section 2, this cell sits **3.55 normalised units** from alt_topology anchor
row 84 and **>= 11 units** from any other anchor in t0091's warm-start population. With per-dim
mutation probability 0.015 over 68 dims, the expected number of mutated parameters per offspring is
**~ 1.0** — consistent with the cell being a one-polynomial-mutation descendant of an anchor
clone, not an NSGA-II discovery. The t0091 published narrative of "warm-start NSGA-II finds joint-
pass corner" is reframed in this task as **"the anchor library already contains the joint-pass
corner, and one generation of NSGA-II is sufficient to preserve it"** — a methodological
clarification consistent with both Hay2011's joint-vs-single-target finding (joint fits need
informed init) and Ament2023's 5-10x warm-start HV envelope
[Ament2023, as cited via t0099 `compare_literature.md`]. This is the same reading the t0099
compare-literature reached independently and t0102 strengthens it: 2,208 + 2,592 = 4,800 random-init
evaluations now find **0/4800** joint-pass cells, while the single t0091 joint-pass cell sits within
a one-mutation neighbourhood of a warm-start anchor.

## Limitations

* **No same-substrate published baseline.** No cited paper runs MO optimisation on a 68-d DSGC
  substrate with our specific Bed B + 14-d morphology parameterisation; all comparisons are with
  external substrates (CA1, L5PC, Purkinje, AdEx, biochemical). Acceptance-rate transfer (Hay2011's
  0.4% to our 68-d) is therefore an **assumption**, not a measurement.

* **PolegPolsky2026 DSI numbers come from a brainstorm-session extraction, not from the canonical
  paper asset.** Per `research_papers.md`, the existing `summary.md` for PolegPolsky2026 contains
  fabricated mechanistic claims (deferred suggestion S-0101-01); the 73.1%/50.8%/2.4% DSI numbers
  cited here come from `tasks/t0101_brainstorm_results_21/results/results_detailed.md`'s direct
  PDF-text extraction. A correction-pass on the paper summary is pending. Our cited values are
  therefore from a brainstorm transcript, not an unimpeached paper summary.

* **Cost-watchdog truncation: gens 14/13 instead of 20.** Both seeds were cut short before reaching
  the planned generation 20. Neither HV trajectory had plateaued (seed 44 made +0.3 HV jump at gen
  14; seed 55 made +0.2 jump at gen 13). It is possible — though the structural bimodality finding
  argues against it — that 6-7 additional generations would have produced a joint-pass cell. The
  literature comparison reads our 14-gen / 13-gen result as a hard endpoint, but it is more
  correctly a **truncated** endpoint.

* **DSI floating-point artifact contaminates the headline number.** Our reported `max DSI = 1.0`
  values in both seeds are silenced-cell artifacts (Finding 1, `results_detailed.md`). The
  Mohacsi2024 / Hay2011 / Druckmann2007 acceptance-rate comparison assumes our DSI metric is a
  faithful selectivity measure; under that assumption the comparison is valid for cells with PD > 0,
  but the artifact means our headline `metrics.json` value cannot be compared like-for-like to any
  published DSI number without first gating by a minimum spike-count threshold.

* **NSGA-II is the only algorithm tested.** Mohacsi2024 puts NSGA-II at 3rd or 4th in their 6-use-
  case ranking; we cannot tell from t0102 alone whether the null result is NSGA-II-specific or truly
  algorithm-independent. A follow-up at matched budget with IBEA or CMAES would be the cheapest
  one-variable test (deferred suggestion: switch optimiser).

* **Population floor not respected.** Dang2023's `mu = Omega(n log n) ~ 290` for `n = 68` is **~3x
  larger** than our pop=96; we cannot rule out that pop=96 is below the noise-survival floor for our
  problem dimensionality. Raising pop to 256 or 512 is a principled lever before concluding the
  substrate is structurally empty of joint-pass cells.

* **No tail-diagnostic per objective.** Morinaga2024's stability-index `alpha` diagnostic was not
  computed for any of our objectives. Whether DSI / PD / robustness sit at `alpha > 1`, `alpha = 1`,
  or `alpha < 1` is an open empirical question; the choice of explicit averaging at K=4 is
  theoretically justified only if `alpha > 1`. Computing alpha per objective on the t0093 anchor
  library would close this gap at zero additional Vast.ai cost.
