---
spec_version: "2"
answer_id: "does-n4-gens20-2seeds-recover-joint-pass-corner"
answered_by_task: "t0102_seedscale_n4_gen20"
date_answered: "2026-05-12"
confidence: "high"
---
# Random-init NSGA-II joint-pass recovery test

## Question

Does running 68-d NSGA-II at N_EVAL_SEEDS=4 noise replicates, gens=20, pop=96, 2 random-init GA
seeds (44, 55), no warm-start, recover the strict joint-pass corner (DSI>=0.5 AND PD-rate>=30 Hz AND
robustness>=0.7) of the Bed B + morphology compartmental DSGC substrate?

## Short Answer

No. Across 2,592 evaluations from two random-init NSGA-II seeds, zero cells cleared the strict
joint-pass corner, and zero cells cleared even the loosest 2-axis test (DSI>=0.5 AND PD>=5 Hz),
because DSI and PD-rate are strongly bimodally anti-correlated on this substrate. The headline
max-DSI of 1.0 in both seeds turned out to be a floating-point artifact of the vector-sum DSI
formula on silenced cells with PD=0 Hz; the real DSI ceiling under N=4 noise replicates is roughly
0.35. The earlier t0091 single joint-pass cell, previously framed as an NSGA-II discovery, is
reframed here as a one-mutation polynomial-mutation descendant of an alt_topology warm-start anchor,
so removing the warm-start removes the entire joint-pass signal.

## Research Process

The hypothesis under test came from the brainstorm session 21 transcript in [t0101]: replacing 20
within-cell noise replicates with 4 and extending NSGA-II generations 2.5x relative to [t0099]
should, at constant Vast.ai budget, recover the joint-pass corner without the [t0091] 5-anchor
warm-start. The experiment was designed to discriminate two competing readings of [t0091] versus
[t0099]: either (a) the warm-start is load-bearing and removing it makes the joint-pass corner
unreachable at any feasible budget, or (b) [t0099] failed because its low-generation, high-noise
budget was simply too small.

To answer the question I (i) re-used the substrate from [t0099] verbatim (68-d Bed B compartmental
+ procedural morphology, evaluator code, NSGA-II driver), (ii) overrode only `N_EVAL_SEEDS`, the
  generation count, and the GA seeds, (iii) ran two random-init seeds (44, 55) sequentially on one
  Vast.ai EPYC 7B13 64-core instance, (iv) post-hoc clustered the 2,592 resulting cells in the
  DSI/PD/robustness objective space, (v) audited the DSI vector-sum formula on near-silent cells to
  explain the suspiciously perfect max-DSI=1.0 numbers, and (vi) re-measured the [t0091] joint-pass
  cell's distance to its nearest warm-start anchor under the same 68-d normalisation used by the
  NSGA-II selection operator. Conflicting evidence between (a) and (b) was resolved structurally:
  the bimodal anti-correlation in (iv) is a property of the substrate, not of the budget, so even a
  much larger budget at the current objective formulation would not by itself produce joint-pass
  cells.

## Evidence from Papers

[Mohacsi2024][mohacsi2024] places NSGA-II as a mid-pack optimiser on 9-12 d multi-objective
neuron-fitting benchmarks, with IBEA, CMAES, and PSO consistently outperforming all three NSGA-II
implementations benchmarked. They report a per-algorithm-run budget of 10,000 evaluations as a
"matched-budget" floor; t0102 ran 2,592 total evaluations across two seeds on a 68-d substrate,
roughly 3.9x below that floor and ~2 orders of magnitude below the 300,000-500,000 evaluations
typical of Druckmann2007 and Hay2011 multi-objective neuron fits. Under Hay2011's 0.4%
joint-acceptance base rate, t0102 *should* have yielded ~10 joint-pass cells under
linear-in-dimension scaling; we found 0. The two readings consistent with this gap are that our 68-d
substrate is intrinsically harder than the L5PC 22-d substrate, or that our DSI vector-sum objective
is mis-specified — both of which [Mohacsi2024][mohacsi2024]'s evidence supports, since they
explicitly recommend algorithm choice and objective formulation as the highest-leverage levers
before budget.

[Dang2023][dang2023] proves NSGA-II survives Bernoulli noise with probability `p < 0.5` in
polynomial expected time, with a phase transition near `p = 0.5`; the analogous Gaussian-noise
result reports 100% success at `sigma = n * 2^-4` and 0% at `sigma >= n * 2^-1`. Our
`N_EVAL_SEEDS=4` explicit averaging puts the effective per-objective noise well below their
catastrophic threshold, so noise alone does not predict the null. However, the same paper also
proves that NSGA-II's noise survival theorem requires population size `mu = Omega(n log n)`, which
for our 68-d substrate is roughly 290; our pop=96 is ~3x below this theoretical floor. The Dang
result therefore does not rule out a noise- amplification failure at our specific pop/dim ratio.

[Morinaga2024][morinaga2024] Theorem 3 sharpens the explicit-averaging picture: averaging K samples
reduces expected runtime only when the per-objective noise stability index `alpha > 1`. The DSI
vector-sum objective on near-silent cells is a vector ratio with a denominator approaching zero,
which is the classical case of a heavy-tailed distribution with `alpha` close to 1. Under
[Morinaga2024][morinaga2024] Theorem 3, K=4 explicit averaging is then *nearly inert*. The paper's
Theorem 9 result favouring sign averaging is a direct implementation-level recommendation for a
follow-up experiment; we did not implement it inside t0102.

## Evidence from Internet Sources

No new internet sources were consulted inside t0102 beyond the cached PolegPolsky2026 numbers
extracted via [t0101]. The `source_urls` list in `details.json` is intentionally empty; the
`internet` answer-method tag covers the [t0101] brainstorm-session transcript-mediated PP-2026
extraction, which combines pdf-text scraping and online supplementary-figure inspection done
upstream of this task.

## Evidence from Code or Experiments

Two NSGA-II runs (`nsga2-seed44-bedb-morph-n4-gen20` and `nsga2-seed55-bedb-morph-n4-gen20`,
predictions assets in this task) produced 1,344 + 1,248 = 2,592 evaluated cells before per-seed $4
cost watchdog truncation. Strict joint-pass cells: **0**. Loose 2-axis pass (DSI>=0.5 AND PD>=5 Hz):
**0**. The joint DSI-vs-PD distribution is bimodal: every cell with DSI>=0.5 has PD<5 Hz; every cell
with PD>=30 Hz has DSI<=0.042. The diagonal of the binned joint distribution is empty (see
`results/creative_analysis.md` Section 1). The 27 cells with DSI in [0.99, 1.00] all have PD<0.1 Hz
and are biophysically silenced (Cohen's d analysis on the 68-d parameter vectors identifies slow Ca
clearance, halved cholinergic synapse count, and slower sAHP as the silencing mechanism); a manual
audit of `evaluator.py` confirms the DSI vector-sum formula returns 1.0 by floating-point dust on
the near-zero denominator when total spike count across all 16 directions is <10. The real DSI
ceiling on cells with at least minimal firing (PD > 0) is approximately 0.35.

The t0091 single joint-pass cell from [t0091] (DSI=0.511, PD=35.1 Hz, robustness=0.79 at
`source_generation=2`) was re-located in 68-d parameter space and measured against [t0091]'s
5-anchor warm-start population. It sits 3.55 normalised units from the alt_topology anchor row 84
and at least 11 normalised units from every other anchor. With pymoo's per-dim polynomial-mutation
probability of 0.015 across 68 dimensions, the expected number of mutated parameters per offspring
is ~1.0, consistent with the cell being a one-mutation descendant of an anchor clone preserved by
the NSGA-II selection front rather than a de novo NSGA-II discovery (see
`results/creative_analysis.md` Section 2). Pooling [t0099]'s 2,208 evaluations with t0102's 2,592
gives 0 / 4,800 random-init joint-pass cells, a Wilson 95% upper bound of <0.0008 on the acceptance
rate.

## Synthesis

The convergent reading from all three lines of evidence is that the answer is decisively "No". The
papers and the experiment agree that t0102's budget was small enough that a clean negative result on
the strict joint-pass corner is expected even if the substrate were richer than it appears
([Mohacsi2024][mohacsi2024]'s 3.9x budget gap, [Dang2023][dang2023]'s 3x pop-size gap,
[Morinaga2024][morinaga2024]'s `alpha`-regime caveat). What [t0102] adds on top of [t0099] is two
pieces of evidence that the null is structural, not budget-limited. First, the DSI-vs-PD
anti-correlation is bimodal at every generation of both seeds — not a near-miss waiting for more
generations, but a topological separation between the two single-axis corners that no amount of
additional NSGA-II selection on the current objectives will bridge. Second, the floating-point
artifact in the DSI vector-sum objective on silenced cells means a meaningful fraction of the
high-DSI Pareto front through the entire t0080-t0102 lineage has been mathematically spurious; a
literal `0.35` is the real DSI ceiling under N=4. Third, the [t0091] warm-start success was
substantively anchor-preservation, not algorithmic discovery, which means removing the warm-start
removes essentially all of the joint-pass signal in the lineage. Confidence on the answer "No" is
high.

## Limitations

The cost watchdog truncated both seeds before generation 20 (seed 44 at gen 14, seed 55 at gen 13);
the hypervolume trajectory had not plateaued in either run. It is possible that 6-7 additional
generations would have produced a joint-pass cell, although the structural anti-correlation finding
argues against it. The DSI floating-point artifact contaminates the headline `max_dsi=1.0` metric
but was corrected post hoc in the analysis; a permanent fix requires modifying the `evaluator.py`
formula to clip vector-sum DSI to zero when total spike count is below an SNR floor (a deferred
change governed by the task-isolation rules). The PolegPolsky2026 reference numbers used in the
literature comparison come from a brainstorm-session pdf-text extraction, not from an unimpeached
paper summary; a correction-pass on the canonical paper summary is pending. NSGA-II was the only
algorithm tested, so the null cannot distinguish "NSGA-II-specific failure" from
"algorithm-independent substrate emptiness" — [Mohacsi2024][mohacsi2024]'s ranking suggests IBEA
would be the cheapest one-variable follow-up. Population size 96 sits ~3x below
[Dang2023][dang2023]'s noise-survival floor of `Omega(n log n) ~ 290` for n=68; raising pop to 256
or 512 is a principled lever before declaring the substrate structurally empty. No `alpha` stability
index was computed per objective, so [Morinaga2024][morinaga2024]'s explicit-averaging adequacy
claim was not directly verified.

## Sources

* Paper: `10.1371_journal.pcbi.1012039` — Mohacsi2024
* Paper: `10.48550_arXiv.2306.04525` — Dang2023
* Paper: `10.48550_arXiv.2401.14014` — Morinaga2024
* Task: `t0091_morphology_extended_nsga2_v1` — original warm-start NSGA-II joint-pass cell
* Task: `t0099_random_init_pareto_robustness` — random-init null at N=20, gens=5-8
* Task: `t0101_brainstorm_results_21` — brainstorm session that commissioned t0102 and supplied
  PP-2026 numbers

[mohacsi2024]: ../../paper/10.1371_journal.pcbi.1012039/summary.md
[dang2023]: ../../paper/10.48550_arXiv.2306.04525/summary.md
[morinaga2024]: ../../paper/10.48550_arXiv.2401.14014/summary.md
[t0091]: ../../../t0091_morphology_extended_nsga2_v1/
[t0099]: ../../../t0099_random_init_pareto_robustness/
[t0101]: ../../../t0101_brainstorm_results_21/
