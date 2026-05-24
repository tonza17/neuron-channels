---
spec_version: "2"
answer_id: "substrate-rate-5seed-canonical"
answered_by_task: "t0121_5seed_substrate_rate_canonical_report"
date_answered: "2026-05-24"
confidence: "medium"
---
# 5-Seed Substrate-Rate Canonical Estimate

## Question

What is the LEGIT joint-pass acceptance rate on the 68-d Bed B + 14-d morphology NSGA-II substrate,
estimated from a 5-seed random-init batch, and how does it compare to Hay 2011 and Druckmann 2007?

## Short Answer

The 5-seed mean LEGIT joint-pass acceptance rate is 2.58% with sample SE 1.50%, a normal-approx 95%
CI of (-0.35%, 5.51%), and a bootstrap 95% CI of (0.38%, 5.53%); the point estimate is roughly 6.5x
Hay 2011's 0.40% envelope and 25.8x Druckmann 2007's 0.10% baseline, and 3 of 5 seeds individually
exceed the Hay envelope. Both 95% CIs bracket zero and both literature baselines, so this batch
cannot statistically reject the literature rates despite the elevated point estimate.

## Research Process

This task is a pure write-up that consolidates the S-0112-01 substrate-rate confirmation batch into
one canonical document. The pipeline re-loads each of the five source-task raw NSGA-II evaluation
dumps (one per seed: 44, 77, 2247, 7755, 9354), applies the canonical LEGIT predicate
(`DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999`), dedups by the 68-d parameter vector, counts
unique LEGIT joint-pass cells, and recomputes the per-seed acceptance rate as
`n_legit_joint_pass_unique / n_total_evals * 100`. The 5-seed mean, sample SD, and sample SE are
derived from the five per-seed rates; the normal-approx 95% CI uses `mean +/- 1.96 * SE`; the
bootstrap 95% CI uses `B = 10000` resamples of the five rates with replacement, fixed RNG seed 42,
and the 2.5/97.5 percentiles of the resample means. A convention-drift table reconciles the legacy
`joint_pass_summary_4seeds.csv` numbers (silence-guard included for seeds 44, 2247, 7755) against
the canonical LEGIT-only numbers, and a literature comparison table places the headline rate next to
Hay 2011 (full envelope and perisomatic bottleneck), Druckmann 2007 (baseline), and the Mohacsi 2024
convergence band.

## Evidence from Papers

[Hay2011][hay2011] reports approximately 2000 accepted parameter sets out of 500,000 evaluations on
the 22-d L5b pyramidal-cell substrate, giving a 0.40% full-envelope acceptance rate; the same paper
reports 52 accepted / 500,000 in a perisomatic-only fit set, the 0.0104% "substrate-limited
counterexample". [Druckmann2007][druckmann2007] reports 300 accepted parameter sets out of 300,000
evaluations on the 12-d cortical interneuron substrate (0.10% baseline). [Mohacsi2024][mohacsi2024]
reports NSGA-II asymptote within 20-60 generations on 3-12 parameter problems (no acceptance rate
reported); this convergence band frames the [t0113] premature-stop caveat below.

## Evidence from Internet Sources

The `internet` method was not used by this answer. All evidence comes from project paper assets and
prior task results.

## Evidence from Code or Experiments

The five per-seed acceptance numbers, recomputed under the canonical LEGIT convention, are:

| Seed | Task | N evals | LEGIT cells | Acceptance % |
| --- | --- | --- | --- | --- |
| 44 | `t0106_long_pdnd_nsga2_300gen` | 3744 | 121 | **3.2318%** |
| 77 | `t0112_t0106_seed77_replicate` | 2016 | 7 | **0.3472%** |
| 2247 | `t0113_t0106_seed2247_replicate` | 1344 | 0 | **0.0000%** |
| 7755 | `t0114_seed7755_no_autostop` | 5952 | 484 | **8.1317%** |
| 9354 | `t0115_seed9354_no_autostop` | 5280 | 63 | **1.1932%** |

These match the [t0115] `substrate_rate_5seed.csv` headline numbers within rounding. [t0106]
provides seed 44 (3.23%), [t0112] provides seed 77 (0.35%), [t0113] provides seed 2247 (0.00%),
[t0114] provides seed 7755 (8.13%), [t0115] provides seed 9354 (1.19%). [t0106_joint_pass_recovery]
is the original 1-seed answer that this 5-seed batch supersedes. The convention-drift reconciliation
table in `results/data/convention_drift_5seed.csv` quantifies the legacy-vs-canonical delta: under
the silence-guard-included convention historically published by [t0114], seed 7755 reads 12.95% (771
/ 5952), but under the canonical LEGIT-only convention it is 8.13% (484 / 5952), a delta of
approximately -4.82 percentage points.

## Synthesis

The point estimate (2.58%) is roughly 6.5x Hay 2011's full envelope (0.40%) and 25.8x Druckmann
2007's baseline (0.10%), yet both 95% CIs (normal-approx and bootstrap) bracket zero AND both
literature baselines; the 5-seed sample SE (1.50%) is itself larger than either baseline, so
frequentist inference cannot reject the literature rates. The honest framing is "point-estimate
plausibly denser than literature; CI cannot rule out literature". Three of five seeds (44, 7755,
9354\) individually exceed the Hay envelope, which is the right effect-size statement. The
convention-drift reconciliation matters because [t0114]'s pre-correction headline of 12.95% for seed
7755 is a silence-guard artefact under the historical convention; the canonical LEGIT-only number is
8.13%.

## Limitations

The dominant uncertainty is censoring at the lower tail: [t0113]'s zero contribution is plausibly a
censoring artefact, not a true substrate-yield zero. The HV-plateau auto-stop detector at
`(W=2, T=0.01)` fired prematurely at gen 14 on [t0113], well below the [Mohacsi2024][mohacsi2024]
20-60 generation convergence band. The offline detector replay in [t0114] recommended new defaults
`(W*, T*) = (3, 0.015)` but those have not been adopted in production for any of the five batch
seeds. The auto-stop convention itself drifts mid- batch: enabled for [t0106] / [t0112] / [t0113],
disabled per S-0113-03 for [t0114] and [t0115]. The pool-restart cadence also drifts: 25 for [t0106]
(legacy) and 10 for the other four seeds (the project's "10th gen rule"). With n = 5 the 95% CI is
wide and the mean is dominated by the seed 7755 result (8.13%); a future batch should re-run [t0113]
with auto-stop disabled and add at least two more seeds to tighten the CI.

## Sources

* Paper: `10.1371_journal.pcbi.1002107`
* Paper: `10.3389_neuro.01.1.1.001.2007`
* Paper: `10.1371_journal.pcbi.1012039`
* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0113_t0106_seed2247_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* Task: `t0097_multi_obj_optim`
* Task: `t0102_seedscale_n4_gen20`

[hay2011]: ../../../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[druckmann2007]: ../../../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md
[mohacsi2024]: ../../../../t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[t0106]: ../../../../t0106_long_pdnd_nsga2_300gen/
[t0106_joint_pass_recovery]: ../../../../t0106_long_pdnd_nsga2_300gen/assets/answer/t0106-joint-pass-recovery-2dir/
[t0112]: ../../../../t0112_t0106_seed77_replicate/
[t0113]: ../../../../t0113_t0106_seed2247_replicate/
[t0114]: ../../../../t0114_seed7755_no_autostop/
[t0115]: ../../../../t0115_seed9354_no_autostop/
