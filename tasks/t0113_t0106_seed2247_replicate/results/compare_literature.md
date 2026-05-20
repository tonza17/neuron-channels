---
spec_version: "1"
task_id: "t0113_t0106_seed2247_replicate"
date_compared: "2026-05-20"
---
# Comparison with Project and Published Results

## Summary

t0113 is a deliberately minimum-change seed-2247 (randomly drawn via `secrets.randbelow(10000)`)
replicate of [t0106]'s 2-direction ratio-DSI NSGA-II run on the 68-d Bed B + 14-d morphology
substrate. The frontier-corner metrics replicate **poorly** vs [t0106] and [t0112]: best LEGIT ratio
DSI **0.3651** vs [t0106]'s **0.9939** and [t0112]'s **0.9535**; best PD-rate **71.67 Hz** vs
[t0106]'s **122.62 Hz** and [t0112]'s **114.76 Hz**; and **0 LEGIT joint-pass cells** (the 2
asset-declared joint-pass cells are silence-guard DSI = 1.0 saturations, not biological selectivity)
vs [t0106]'s **123** and [t0112]'s **7**. The three-seed substrate-rate point estimate is **1.26% ±
1.01% SE** (95% CI -0.73% to +3.25%); this CI **brackets both** [Hay2011][hay2011]'s **0.40%** and
[Druckmann2007][druckmann2007]'s **0.10%** biophysical-NSGA-II references and cannot yet reject
either baseline. The HV-plateau detector fired at gen **14**, the earliest of the 3-seed sample (vs
[t0106] gen 40, [t0112] gen 21), and the run terminated at HV = **45.62** — 42% of [t0112]'s 107.46
and 37% of [t0106]'s 122.03 — strongly suggesting a **premature stop** that censored the joint-pass
long tail.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.9939 | 0.3651 | -0.6288 | Same substrate, different GA seed; t0113 reaches only 37% of [t0106]'s best non-silence-guard DSI |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best PD-rate frontier) | PD (Hz) | 122.62 | 71.67 | -50.95 | t0113 reaches 58% of [t0106]'s best-PD frontier value |
| [t0106] seed 44 NSGA-II (LEGIT joint-pass unique count) | count | 122 | 0 | -122 | Zero non-silence-guard joint-pass cells from seed 2247 vs 122 from seed 44 |
| [t0106] seed 44 NSGA-II (joint-pass yield, all cells) | rate | 3.29% | 0.15% | -3.14 | t0113 acceptance rate is ~22x lower (2/1344 vs 123/3744) |
| [t0106] seed 44 NSGA-II (final hypervolume) | HV | 122.0288 | 45.6221 | -76.41 | t0113 plateau HV is 37% of [t0106]'s; trajectory censored at gen 14 |
| [t0106] seed 44 NSGA-II (HV-plateau generation) | gen | 40 | 14 | -26 | Earliest plateau of the 3-seed sample by 26 gens |
| [t0106] seed 44 NSGA-II (productive compute cost) | USD | 10.37 | 0.1467 | -10.22 | 71x cheaper; HV-plateau auto-stop at gen 14 vs operator-stop at gen 40 |
| [t0112] seed 77 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.9535 | 0.3651 | -0.5884 | Same substrate + cadence-10 protocol, different GA seed; t0113 reaches 38% of [t0112]'s best DSI |
| [t0112] seed 77 NSGA-II (best PD-rate frontier) | PD (Hz) | 114.76 | 71.67 | -43.09 | t0113 reaches 62% of [t0112]'s best-PD frontier value |
| [t0112] seed 77 NSGA-II (LEGIT joint-pass unique count) | count | 7 | 0 | -7 | Zero LEGIT joint-pass cells from seed 2247 vs 7 from seed 77 |
| [t0112] seed 77 NSGA-II (joint-pass yield, all cells) | rate | 0.35% | 0.15% | -0.20 | t0113 acceptance is 43% of [t0112]'s |
| [t0112] seed 77 NSGA-II (final hypervolume) | HV | 107.4602 | 45.6221 | -61.84 | t0113 plateau HV is 42% of [t0112]'s; trajectory censored 7 gens earlier |
| [t0107] 8-direction polar re-evaluation (DSI offset vs 2-dir ratio) | absolute DSI | -0.42 | n/a | n/a | Carries forward unchanged: any t0113 DSI claim should be discounted by ~0.42 absolute when compared to 8-direction biological measurements |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate, single-seed) | rate | 0.10% | 0.15% | +0.05 | [Druckmann2007, Methods + Fig 3]: 300 acceptable / 300,000 evals on 12-d cortical interneuron; t0113 yields 2/1344 on 68-d substrate, essentially matched at single-seed point |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate vs 3-seed mean) | rate | 0.10% | 1.26% | +1.16 | 3-seed mean from t0106 (3.29%) + t0112 (0.35%) + t0113 (0.15%); point estimate **13x above** Druckmann baseline but 95% CI (-0.73%, 3.25%) **brackets 0.10%** — cannot reject |
| [Hay2011][hay2011] NSGA-II 1000x500 joint perisom+BAC (acceptance rate, single-seed) | rate | 0.40% | 0.15% | -0.25 | [Hay2011, p. 4]: ~2000 acceptable / 500,000 evals on 22-d L5b PC; t0113 single-seed acceptance is 37% of Hay's published yield at 3x higher dimensionality |
| [Hay2011][hay2011] NSGA-II joint perisom+BAC (acceptance rate vs 3-seed mean) | rate | 0.40% | 1.26% | +0.86 | 3-seed mean is **3.15x above** Hay envelope upper bound; 95% CI (-0.73%, 3.25%) **brackets 0.40%** — cannot reject |
| [Hay2011][hay2011] NSGA-II perisomatic-only fits (acceptance rate) | rate | 0.0104% | 0.15% | +0.14 | [Hay2011, p. 6]: 52 acceptable / 500,000 evals — the "substrate-limited" counterexample; t0113 substrate clearly not similarly limited even at the sparse seed |
| [Achard2006][achard2006] ES 9x8000 evals (acceptance rate) | rate | 0.028% | 0.15% | +0.12 | [Achard2006, Results]: 20 selected / 72,000 evals on 24-d Purkinje cell; t0113 is ~5x higher acceptance |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon | plateau gen | 20-60 | 14 | -6 | [Mohacsi2024, Fig 4 use cases 1-6]: NSGA-II asymptotes by gens 20-60 on 3-12 param problems; t0113 HV-plateau detector fires at gen 14, **below** the published lower bound — suggests premature stop |
| [Trenholm2013][trenholm2013] mouse Hb9 DSGC ratio DSI (control, peak-rate) | DSI | 0.76 | 0.3651 | -0.3949 | [Trenholm2013, Table 1]: peak PD=198 Hz, peak ND=27 Hz, DSI=(198-27)/(198+27); t0113 best LEGIT DSI falls **48% below** biological reference |
| [Trenholm2013][trenholm2013] mouse Hb9 peak PD firing rate | PD (Hz) | 198 | 71.67 | -126.33 | [Trenholm2013, Table 1]: peak instantaneous Gaussian-convolved rate, control; t0113 frontier PD = 71.67 Hz is 36% of biological peak — above the 30 Hz joint-pass floor but far below biology |
| [Oesch2005][oesch2005] rabbit ON-OFF DSGC spike-based DSI (OFF) | DSI | 0.74 | 0.3651 | -0.3749 | [Oesch2005, p. 740]: 0.74 +/- 0.13 OFF DSI; t0113 best LEGIT DSI falls **49% below** biological reference |
| [PolegPolsky2026][polegpolsky2026] ML unconstrained DSI ceiling | DSI | 0.731 | 0.3651 | -0.3659 | [PolegPolsky2026, Fig 3]: 73.1% +/- 2.4% DSI under full E+I freedom on 12 dirs x 5 speeds; t0113 best LEGIT DSI is **50% below** the published computational ceiling |

## Methodology Differences

* **GA seed (the only intended algorithmic change vs [t0112]).** t0113 uses GA seed **2247** drawn
  by `secrets.randbelow(10000)`; [t0112] used GA seed **77** (curated from a small candidate set);
  [t0106] used GA seed **44**. The substrate (68-d Bed B + 14-d morphology), objective (2-direction
  ratio DSI + PD-rate at 0 deg), evaluator, silence guard, SBX/PM operators, LHS init,
  `_POOL_RESTART_EVERY = 10`, `N_GEN = 60`, HV-plateau detector constants, cost watchdog, and
  predictions-asset schema are bitwise identical to [t0112]. This is the controlled-variable
  comparison.

* **HV-plateau detector fired at gen 14 — earliest of the 3-seed sample.** [t0106] (cadence 25) was
  operator-stopped at gen 40; [t0112] (cadence 10) was auto-stopped at gen 21; t0113 (cadence 10\)
  was auto-stopped at gen 14. The detector is identical across t0112 and t0113
  (`HV_PLATEAU_WINDOW = 2`, `HV_PLATEAU_REL_THRESHOLD = 0.01`); the earlier trigger on seed 2247
  reflects a soft plateau between gens 11-12 (HV 35.98 -> 36.07 = +0.24% < 1% threshold) that
  satisfied the detector before the gen 13 -> 14 jump (HV 36.10 -> 45.62 = +26.4%) could
  materialise. This is plausibly **premature censoring** of the long tail — see Limitations.

* **DSI definition vs published DSGC measurements.** t0113 inherits [t0106]'s 2-direction ratio DSI
  on antipodal directions (PD = 0 deg, ND = 180 deg). [Trenholm2013][trenholm2013],
  [Oesch2005][oesch2005], and [PolegPolsky2026][polegpolsky2026] all use 8 - 12 directions with
  vector-sum DSI. **No published paper fits a biophysical model against a 2-direction objective.**
  [t0107]'s 8-direction re-evaluation of 10 [t0106] top cells showed the 2-direction ratio DSI
  overstates selectivity by ~0.42 absolute under 8-direction vector-sum — this caveat carries to
  t0113, but applied to t0113's already-low 0.3651 LEGIT DSI yields an estimated 8-direction
  vector-sum DSI of ~-0.05, i.e. effectively zero biological selectivity at the best legit cell.

* **Silence-guard saturation dominates the asset-declared joint-pass count.** Both of t0113's 2
  unique joint-pass cells are DSI = 1.0 with 1 PD spike and 0 ND spikes — the silence-guard
  threshold (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`) accepts these single-spike configurations.
  [t0106]'s 123 joint-pass cells included 1 silence-guard cell (the remaining 122 were LEGIT);
  [t0112]'s 7 cells were all LEGIT. t0113's count is **0 LEGIT vs 2 asset-declared** — the cleanest
  interpretation is "no biological selectivity discovered at this seed". This silence-guard artefact
  applies to t0113 in a different way than to the prior seeds.

* **Single GA seed vs multi-seed convention (unchanged from [t0106] and [t0112]).**
  [Chen2024-STN][chen2024-stn] used 3 seeds at pop=120, ~1M evals;
  [PolegPolsky2026][polegpolsky2026] used 100 GA seed restarts at pop=10, gens=300-1000. t0113 ran 1
  seed (the same constraint as [t0106] and [t0112]). The 3-seed mean (44, 77, 2247) of **1.26%** is
  **above** the [Hay2011][hay2011] 0.40% envelope point estimate but the **95% CI (-0.73%, +3.25%)
  brackets both [Hay2011][hay2011] and [Druckmann2007][druckmann2007] baselines**. The S-0112-01
  5-seed batch (two further seeds required) is the agreed path to a tighter substrate-rate estimate.

* **Substrate vs published NSGA-II benchmarks (unchanged from [t0112]).**
  [Druckmann2007][druckmann2007] = 12-d, [Hay2011][hay2011] = 22-d, [Achard2006][achard2006] = 24-d.
  t0113's 68-d substrate is **2.8x - 5.7x higher dimensional** than any published NSGA-II
  biophysical benchmark. Standard scaling intuition predicts lower acceptance rate at higher
  dimensionality; t0113's 0.15% in 68-d at **single-seed point estimate** is therefore not anomalous
  against the [Hay2011][hay2011] 0.40% / [Druckmann2007][druckmann2007] 0.10% envelope.

* **Evaluation budget — well below published references.** t0113 = **5,760 planned / 1,344 actual**
  evaluations (the smallest of the 3-seed sample by a factor of 1.5-2.8).
  [Druckmann2007][druckmann2007] used **300,000**; [Hay2011][hay2011] used **500,000**. t0113 is
  **~220x below** the modern reference floor — a comparable acceptance rate at 220x lower spend
  supports the [Mohacsi2024][mohacsi2024] observation that the 2-direction objective surface
  converges faster than the published 30+ feature objectives, but the early plateau-stop (gen 14,
  below the 20-60 range in [Mohacsi2024, Fig 4]) means t0113's spend is anomalously low even by this
  comparison.

* **Wall-clock comparison is instance-size confounded.** t0113's 160 s/gen vs [t0112]'s 620 s/gen is
  a 3.9x speedup, but the t0113 instance (AMD EPYC 7B13, 64 cores / 256 logical threads, 125 GB RAM)
  had 2x more cores than t0112's 32-core EPYC instance. At the per-core level wall-clock is
  consistent with t0112. The cadence-10 protocol speedup vs [t0106]'s cadence-25 reported in
  [t0112]'s comparison still holds, but t0113 cannot independently confirm it without a matched
  32-core run.

## Analysis

### Prior Task Comparison

The headline finding is **non-replication of [t0106]'s breakthrough at seed 2247**: t0113 produced
**0 LEGIT joint-pass cells** and only **2 asset-declared joint-pass cells** (both silence-guard DSI
= 1.0 artefacts). The frontier-corner is **not reached** from this seed — best LEGIT DSI is
**0.3651** at PD = 10.24 Hz, far below [t0106]'s 0.9939 / [t0112]'s 0.9535, and best PD-rate is
**71.67 Hz**, far below [t0106]'s 122.62 Hz / [t0112]'s 114.76 Hz. This is the **third independent
GA-seed data point** for the substrate's joint-pass density, and it falls in the **lowest** bucket
defined by the task brief (0 LEGIT cells, "substrate not populated at this seed").

The three-seed dispersion is now 0.15% (2247) / 0.35% (77) / 3.29% (44) — a **22x range** in
unique-count terms. This **strengthens** the [t0112] finding that [t0106]'s 3.3% was an
above-typical lucky seed: with two of three seeds now in the sub-1% regime, the population mean of
the joint-pass acceptance rate is plausibly **below 1%** and the [t0106] outlier is driving the
3-seed mean of 1.26% almost single-handedly. However, the **standard error (1.01%) is larger than
either of the two literature baselines** (Hay 0.40%, Druckmann 0.10%) — the 95% CI (-0.73%, +3.25%)
brackets zero and both literature points. **No statistical separation is possible at 3 seeds**; the
S-0112-01 5-seed batch is required.

Three non-mutually-exclusive explanations for t0113's sparse result, in decreasing order of
parsimony:

1. **GA-seed variance is genuinely large at this substrate.** The 22x range in unique joint-pass
   counts across seeds 44, 77, 2247 indicates the joint-pass corner is reachable only from specific
   initial-population regions in 68-d space. With seeds 77 and 2247 both producing sub-1% yields
   (and seed 2247 producing zero LEGIT cells), the substrate's joint-pass corner appears to be a
   **narrow, hard-to-reach basin** rather than a broad attractor.

2. **The HV-plateau detector fired prematurely at gen 14.** The HV trajectory shows two large jumps
   (gen 7: +2.85; gen 10: +29.39) followed by a 4-gen soft plateau at HV ~36-46. The detector
   requires HV growth < 1% over 2 consecutive generations; the gen 11-12 transition (35.98 -> 36.07
   = +0.24%) satisfied this **before** the gen 14 jump (36.10 -> 45.62 = +26.4%) could materialise.
   A direct test would re-run seed 2247 with the auto-stop disabled to confirm whether the HV would
   have continued climbing past gen 14 — see suggestion S-0113-04 (to be generated in the next
   stage).

3. **Pool-restart-every-10 may be reducing exploration at certain seeds.** This was originally
   raised after [t0112] as S-0112-03; t0113 strengthens that hypothesis by adding a second seed
   where the cadence-10 protocol plateaued early at a low HV. A controlled test would re-run seed
   2247 with cadence 25 (matching [t0106]) to isolate the cadence effect from the seed effect.

Hypothesis 1 is the most parsimonious; hypotheses 2-3 are not ruled out by this single replicate.

### Published Literature Comparison

The most consequential finding relative to the literature is that **the 3-seed substrate-rate
estimate cannot yet reject either the [Druckmann2007][druckmann2007] 0.10% or [Hay2011][hay2011]
0.40% baseline**. The point estimate of 1.26% is 3.15x above the Hay envelope and 13x above the
Druckmann baseline, but the standard error of 1.01% (driven entirely by the [t0106] outlier at
3.29%) yields a 95% CI of (-0.73%, +3.25%) that brackets both literature reference values and zero.
Pooling t0113's 0.15% with [t0112]'s 0.35% gives a 2-seed sub-substrate mean of **0.25%**, which is
**62% of [Hay2011][hay2011]'s 0.40%** and **2.5x [Druckmann2007][druckmann2007]'s 0.10%** —
**essentially within the published biophysical-NSGA-II envelope** when the [t0106] outlier is
excluded.

The interpretation is **bimodal**: either the substrate genuinely supports joint-pass cells at
~0.25% acceptance (consistent with literature) and [t0106]'s 3.29% was a single-seed extreme, or the
substrate supports joint-pass cells at a true rate near the [t0106] mean (3.3%) and seeds 77 and
2247 both happened to find sparser basins. Without 2 more seeds (S-0112-01 batch completion) the
bimodality cannot be resolved.

The **best LEGIT DSI of 0.3651 falls 48% below [Trenholm2013][trenholm2013] mouse Hb9 control DSI
(0.76)**, **49% below [Oesch2005][oesch2005] rabbit ON-OFF OFF DSI (0.74)**, and **50% below
[PolegPolsky2026][polegpolsky2026]'s unconstrained ML ceiling (0.731)**. Combined with the [t0107]
8-direction overstatement of ~0.42 absolute, the implied 8-direction vector-sum DSI for t0113's best
legit cell is **effectively zero**. By contrast, [t0106]'s and [t0112]'s 2-direction DSI of ~0.95
implied 8-direction DSI of ~0.5 — still in the biological range. **t0113 did not produce
biologically plausible direction-selective cells**, and this is the first 3-seed run to clearly fail
this bar.

The **HV-plateau at gen 14 is BELOW [Mohacsi2024][mohacsi2024]'s 20-60 gen convergence range**
([Mohacsi2024, Fig 4]). [Mohacsi2024][mohacsi2024] reports that even on the simpler 3-12 parameter
problems, NSGA-II takes at least 20 generations to asymptote on HV. The t0113 detector firing 6 gens
earlier than the published lower bound on a 68-d problem is **prima facie evidence of premature
stop** — the detector's 1%-over-2-gens threshold is more aggressive than the literature suggests is
safe for biophysical NSGA-II.

The **PD-rate frontier of 71.67 Hz** is 58% of [t0106]'s 122.62 Hz and 62% of [t0112]'s 114.76 Hz,
and **36% of [Trenholm2013][trenholm2013]'s 198 Hz biological peak**. The PD frontier is above the
30 Hz joint-pass floor in absolute terms but the cell at this peak has DSI = 0.0017 — i.e.
fast-firing but not direction-selective. The substrate did support PD-rate exploration on this seed,
just not direction selectivity.

## Limitations

* **Single GA seed replicate**. t0113 is one GA seed (2247) contributing the third data point to the
  [t0112] S-0112-01 substrate-rate confirmation batch. The S-0112-01 brief requires at least 5
  seeds; t0113 delivers seed 3 of 5. The 95% CI on the 3-seed mean of 1.26% spans (-0.73%, +3.25%) —
  **wider than either of the literature reference values** — so no rejection of
  [Druckmann2007][druckmann2007] or [Hay2011][hay2011] is possible. The remaining 2 seeds will be
  drawn in separate follow-up tasks.

* **HV-plateau premature trigger highly likely**. The 14-gen stop is the earliest of the 3-seed
  sample (t0112 = 21, t0106 = 40) AND is below the [Mohacsi2024][mohacsi2024] published 20-60 gen
  convergence range. The HV trajectory's gen 13 -> 14 jump (+26%) suggests the run had NOT saturated
  — the plateau detector was satisfied by the soft gen 11-12 transition before the gen 14 jump
  materialised. A controlled test (S-0113-04 to be generated) would re-run seed 2247 with the
  auto-stop disabled and a 60-gen ceiling.

* **0 LEGIT joint-pass cells confounds the substrate-rate calculation**. The 2 asset-declared
  joint-pass cells are both silence-guard DSI = 1.0 saturations (1 PD spike, 0 ND spikes), not
  biological selectivity. Whether to report t0113's joint-pass count as 0 (LEGIT reading) or 2
  (asset-declared reading) materially shifts the 3-seed mean: with 0 the mean drops to 1.21% and
  with 2 it is 1.26%. The substrate-rate confidence interval is robust to this choice (both brackets
  contain 0% and both literature baselines), but the **interpretation** of t0113 differs: zero
  biological selectivity discovered (LEGIT) vs evaluation artefact discovered (asset).

* **2-direction protocol is methodologically novel and not directly comparable to published
  multi-direction DSI measurements**. [Trenholm2013][trenholm2013], [Oesch2005][oesch2005], and
  [PolegPolsky2026][polegpolsky2026] use 8-12 directions. The DSI = 0.3651 LEGIT result cannot be
  claimed as "biologically subthreshold" without an 8-direction post-hoc re-evaluation. [t0107]
  established that [t0106]'s 2-direction ratio DSI overstates selectivity by ~0.42 absolute under
  8-direction vector-sum; carrying this caveat forward to t0113's 0.3651 yields an estimated
  8-direction DSI of ~-0.05, i.e. effectively zero — but the offset was measured on the [t0106]
  high-DSI cells, not on the low-DSI region t0113 occupies.

* **Wall-clock comparison is instance-size confounded**. t0113's 160 s/gen vs [t0112]'s 620 s/gen is
  not a clean cadence-10 measurement — t0113's 64-core EPYC has 2x the core count of [t0112]'s
  32-core EPYC. A controlled test would re-run seed 2247 on the same 32-core class as [t0112] to
  isolate the per-core speedup.

* **Pareto-front parameter-space overlap analysis remains heuristic**. The combined-seed (7,104
  cells) z-scored L2 standardisation reference is defensible but not the unique correct choice.
  Per-task standardisation, or literature-derived parameter-range standardisation, would yield
  slightly different rankings. The z-scored distances from t0113 Pareto cells (mean ~10.7,
  comparable to seed-44 and seed-77 nearest neighbours) indicate that t0113 explored a similar
  region of 68-d space to the prior seeds but did not find the joint-pass corner within those
  regions.

* **No comparable published NSGA-II run at this dimensionality**. The 68-d substrate is 2.8x - 5.7x
  higher dimensional than any published biophysical NSGA-II benchmark. The acceptance-rate
  comparison is therefore against extrapolated expectations, not matched-dimensional baselines.
  **Publication-selection bias** also applies: [Hay2011][hay2011] and [Druckmann2007][druckmann2007]
  published successes but not their failed seeds, so the per-seed yield distribution in their
  setting is unknown. t0113's near-zero result could plausibly be a normal "failed seed" that those
  papers also encountered but did not report.

* **Evaluation budget materially below published references**. t0113 used 1,344 evaluations vs
  [Hay2011][hay2011]'s 500,000 and [Druckmann2007][druckmann2007]'s 300,000. The acceptance rate is
  measured at 220x - 370x lower spend; whether the rate would converge to the published value at
  matched spend is open.

* **Random-seed draw is not the same as random-seed selection**. The seed 2247 was drawn via
  `secrets.randbelow(10000)` — uniformly random over [0, 9999]. This avoids the round-ish-low-number
  bias of seeds 44 and 77 but does not guarantee good coverage of the seed-space. A formal sampling
  (e.g. quasi-random Latin hypercube over seeds 0-9999) would give better coverage but is outside
  the scope of a minimum-change replicate.

[t0106]: ../../t0106_long_pdnd_nsga2_300gen/
[t0107]: ../../t0107_t0106_polar_8dir_recheck/
[t0112]: ../../t0112_t0106_seed77_replicate/
[druckmann2007]: ../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md
[hay2011]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[achard2006]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md
[mohacsi2024]: ../../t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[trenholm2013]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/summary.md
[oesch2005]: ../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md
[polegpolsky2026]: ../../t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md
[chen2024-stn]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11383608/
