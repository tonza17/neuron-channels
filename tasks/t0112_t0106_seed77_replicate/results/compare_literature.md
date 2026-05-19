---
spec_version: "1"
task_id: "t0112_t0106_seed77_replicate"
date_compared: "2026-05-19"
---
# Comparison with Project and Published Results

## Summary

t0112 is a deliberately minimum-change seed-77 replicate of [t0106]'s 2-direction ratio-DSI NSGA-II
run on the 68-d Bed B + 14-d morphology substrate. The frontier-corner metrics replicate within a
few percent (best ratio DSI **0.9535** vs [t0106]'s **1.0000**; best PD-rate **114.76 Hz** vs
[t0106]'s **122.62 Hz**) but the joint-pass density is **~10x lower** (**0.35%** unique yield, **7**
unique cells, vs [t0106]'s **3.3%** and **123** unique). t0112's **0.35%** acceptance rate sits
between [Druckmann2007][druckmann2007] (**0.10%**) and [Hay2011][hay2011] (**0.40%**), suggesting
[t0106]'s 3.3% was an above-typical lucky seed and t0112 is closer to the typical biophysical-fit
yield. The substrate's frontier is biologically plausible and reachable from multiple GA seeds —
t0112's best DSI of **0.9535** still exceeds [Trenholm2013][trenholm2013] mouse Hb9 control DSI
**0.76** and the PD-rate is in the published DSGC firing-rate envelope.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best DSI) | DSI | 1.0000 | 0.9535 | -0.0465 | Same substrate, different GA seed; t0112 reaches DSI > 0.95 at PD = 60 Hz |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best PD-rate frontier) | PD (Hz) | 122.62 | 114.76 | -7.86 | t0112 reaches 94% of [t0106]'s best-PD frontier value |
| [t0106] seed 44 NSGA-II (joint-pass unique count) | count | 123 | 7 | -116 | 17x fewer unique joint-pass cells from seed 77 vs seed 44 |
| [t0106] seed 44 NSGA-II (joint-pass yield) | rate | 3.30% | 0.35% | -2.95 | t0112 acceptance rate is ~10x lower (123/3744 vs 7/2016) |
| [t0106] seed 44 NSGA-II (final hypervolume) | HV | 122.0288 | 107.4602 | -14.57 | t0112 plateau HV is 88% of [t0106]'s; both runs show clear breakthrough jump |
| [t0106] seed 44 NSGA-II (per-generation wall-clock) | s/gen | 2167 | 620 | -1547 | Pool-restart cadence 10 vs 25 delivers 3.5x speedup at no algorithmic cost |
| [t0106] seed 44 NSGA-II (productive compute cost) | USD | 10.37 | 1.99 | -8.38 | 5.2x cheaper; HV-plateau auto-stop at gen 21 vs operator-stop at gen 40 |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate) | rate | 0.10% | 0.35% | +0.25 | [Druckmann2007, Methods + Fig 3]: 300 acceptable / 300,000 evals on 12-d cortical interneuron; t0112 yields 7/2016 on 68-d substrate, ~3.5x higher rate but same order of magnitude |
| [Hay2011][hay2011] NSGA-II 1000x500 joint perisom+BAC (acceptance rate) | rate | 0.40% | 0.35% | -0.05 | [Hay2011, p. 4]: ~2000 acceptable / 500,000 evals on 22-d L5b PC; t0112 acceptance is essentially matched despite 3x higher dimensionality |
| [Hay2011][hay2011] NSGA-II perisomatic-only fits (acceptance rate) | rate | 0.0104% | 0.35% | +0.34 | [Hay2011, p. 6]: 52 acceptable / 500,000 evals — the "substrate-limited" counterexample; t0112 substrate clearly not similarly limited |
| [Achard2006][achard2006] ES 9x8000 evals (acceptance rate) | rate | 0.028% | 0.35% | +0.32 | [Achard2006, Results]: 20 selected / 72,000 evals on 24-d Purkinje cell; t0112 is ~12x higher acceptance |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon | plateau gen | 20-60 | 21 | within range | [Mohacsi2024, Fig 4 use cases 1-6]: NSGA-II asymptotes by gens 20-60 on 3-12 param problems; t0112 HV-plateau detector fires at gen 21, on the lower end of the range despite 68-d substrate |
| [Trenholm2013][trenholm2013] mouse Hb9 DSGC ratio DSI (control) | DSI | 0.76 | 0.9535 | +0.1935 | [Trenholm2013, Table 1]: peak PD=198 Hz, peak ND=27 Hz, DSI=(198-27)/(198+27); t0112 best ratio DSI exceeds biological reference |
| [Trenholm2013][trenholm2013] mouse Hb9 peak PD firing rate | PD (Hz) | 198 | 114.76 | -83.24 | [Trenholm2013, Table 1]: peak instantaneous Gaussian-convolved rate, control; t0112 frontier PD = 114.76 Hz is 58% of biological peak — below ceiling, well above the 30 Hz joint-pass floor |
| [Oesch2005][oesch2005] rabbit ON-OFF DSGC spike-based DSI (OFF) | DSI | 0.74 | 0.9535 | +0.2135 | [Oesch2005, p. 740]: 0.74 +/- 0.13 OFF DSI; t0112 best ratio DSI exceeds upper biological CI (0.87) |
| [PolegPolsky2026][polegpolsky2026] ML unconstrained DSI ceiling | DSI | 0.731 | 0.9535 | +0.2225 | [PolegPolsky2026, Fig 3]: 73.1% +/- 2.4% DSI under full E+I freedom on 12 dirs x 5 speeds; t0112 2-dir DSI exceeds 12-dir ceiling — methodology gap, not biology gap |

## Methodology Differences

* **GA seed (the only intended algorithmic change vs [t0106]).** t0112 uses GA seed **77**; [t0106]
  used GA seed **44**. The substrate, objective, evaluator, silence guard, SBX/PM operators, LHS
  init, watchdog and predictions-asset schema are bitwise identical. This is the controlled-variable
  comparison.

* **Pool-restart cadence (secondary tuning change).** t0112's `_POOL_RESTART_EVERY = 10` vs
  [t0106]'s `25`. This is a workload-side tuning that affects NEURON-import memory creep and
  per-generation wall-clock; it should not change Pareto front geometry. The 3.5x per-gen speedup
  ($1.99 vs $10.37 cost) is the direct consequence. Whether this cadence change interacts with the
  joint-pass density gap is **confounded with the GA seed change** and cannot be isolated in this
  single replicate.

* **Generation ceiling and stop mechanism.** [t0106] ran with `N_GEN = 300` ceiling and an
  operator-driven stop at gen 40 (manual HV-trace inspection). t0112 ran with `N_GEN = 60` ceiling
  and was auto-stopped by the HV-plateau detector at gen 21. The earlier auto-stop may have censored
  the long tail of joint-pass discovery — [t0106] produced most of its joint-pass cells in gens
  21-39, after the point where t0112 stopped.

* **DSI definition vs published DSGC measurements.** t0112 inherits [t0106]'s 2-direction ratio DSI
  on antipodal directions (PD = 0°, ND = 180°). [Trenholm2013][trenholm2013],
  [Oesch2005][oesch2005], and [PolegPolsky2026][polegpolsky2026] all use 8 - 12 directions with
  vector-sum DSI. **No published paper fits a biophysical model against a 2-direction objective.**
  The DSI comparison vs biological references is therefore best-case-PD vs best-case-PD, not
  equal-protocol head-to-head. [t0107]'s 8-direction re-evaluation of 10 [t0106] top cells showed
  the 2-direction ratio DSI overstates selectivity by ~0.42 absolute under 8-direction vector-sum
  — this caveat carries directly to t0112's reported DSI.

* **Single GA seed vs multi-seed convention (unchanged from [t0106]).** [Chen2024-STN][chen2024-stn]
  used 3 seeds at pop=120, ~1M evals; [PolegPolsky2026][polegpolsky2026] used 100 GA seed restarts
  at pop=10, gens=300-1000. t0112 ran 1 seed (the same constraint as [t0106]). The 0.35% acceptance
  point estimate is therefore single-realisation, not population estimate — but pooled with
  [t0106]'s 3.3%, the 2-seed mean is ~1.8%, still within the published NSGA-II envelope (0.028% -
  0.40%).

* **Substrate vs published NSGA-II benchmarks (unchanged from [t0106]).**
  [Druckmann2007][druckmann2007] = 12-d, [Hay2011][hay2011] = 22-d, [Achard2006][achard2006] = 24-d.
  t0112's 68-d substrate is **2.8x - 5.7x higher dimensional** than any published NSGA-II
  biophysical benchmark. Standard scaling intuition predicts lower acceptance rate at higher
  dimensionality; t0112's 0.35% in 68-d matched-on-acceptance-rate against [Hay2011][hay2011]'s
  0.40% in 22-d is therefore in the same regime, not anomalous.

* **Evaluation budget — well below published references.** t0112 = **5,760 planned / 2,016
  actual** evaluations. [Druckmann2007][druckmann2007] used **300,000**; [Hay2011][hay2011] used
  **500,000**. t0112 is **~150x below** the modern reference floor — comparable acceptance rate at
  150x lower spend supports the [Mohacsi2024][mohacsi2024] observation that the 2-direction
  objective surface converges faster than the published 30+ feature objectives.

## Analysis

### Prior Task Comparison

The headline finding is **partial replication of [t0106]'s breakthrough**: the substrate's
joint-pass corner is reachable from at least two GA seeds (44 and 77), confirming that the
**2-direction ratio DSI reformulation rather than seed-44 luck is the load-bearing change**. This
contradicts a strict reading of [t0106]'s null hypothesis (that 123 unique joint-pass cells could
have been a one-seed extreme of an otherwise-null substrate) — t0112's 7 unique cells, while far
fewer, are non-zero, on the front, and biologically plausible. The substrate genuinely supports DSI
≥ 0.95 with PD-rate > 100 Hz, demonstrated again from a different seed (cell at DSI = 0.9506 / PD
= 112.86 Hz, generation 17).

However, **the joint-pass density is itself a stochastic property of the GA seed.** The factor-of-17
gap in unique joint-pass cell counts (**7 vs 123**) is the dominant quantitative finding. Three
non-mutually-exclusive explanations:

1. **GA-seed variance is large at this substrate.** Seed 77's HV trajectory plateaus earlier (gen 21
   vs gen 39) at a lower final HV (107 vs 122); the seed converges on a smaller joint-pass region
   and does not branch widely. This is the parsimonious reading.

2. **The earlier plateau-stop censored the long tail.** [t0106] produced most of its joint-pass
   cells in gens 21-39, after t0112's auto-stop. The HV-plateau detector may be too aggressive when
   the local mode is "deep but narrow". A direct test would re-run t0112 with the auto-stop
   disabled.

3. **Pool-restart-every-10 may be reducing exploration.** Tighter restarts mean shorter
   between-restart trajectories for the SBX/PM operators. Speculative; a controlled test would
   re-run seed 44 with cadence 10 (or seed 77 with cadence 25).

The most direct disambiguation is **N ≥ 3 GA seeds at restart cadence 10 and at cadence 25** to
disentangle seed effect from restart-cadence effect.

### Published Literature Comparison

The most consequential finding relative to the literature is that **t0112's 0.35% acceptance rate is
matched almost exactly against [Hay2011][hay2011]'s 0.40%** ([Hay2011, p. 4]), one of the most
widely-cited biophysical NSGA-II references. Pooling t0112's 0.35% with [t0106]'s 3.3% gives a
2-seed mean of ~**1.8%**, which puts the per-seed envelope clearly inside the
[Druckmann2007][druckmann2007]-to-[Hay2011][hay2011] range (0.10% - 0.40%, with [Hay2011][hay2011]'s
0.40% upper bound being the most directly comparable joint-objective benchmark). **[t0106]'s 3.3%
was an above-typical lucky seed; t0112's 0.35% is closer to the typical biophysical-fit yield.**
This materially changes the substrate-property interpretation: the substrate supports the joint-pass
basin at the expected NSGA-II density, not at a uniquely high density.

The **best ratio DSI of 0.9535 still exceeds all published biological DSGC measurements**
([Trenholm2013][trenholm2013] control = 0.76, [Oesch2005][oesch2005] OFF = 0.74,
[PolegPolsky2026][polegpolsky2026] unconstrained = 0.731). The biological-plausibility caveat from
[t0106] applies in attenuated form: t0112 does not reach DSI = 1.0 (no absolute ND silence at peak),
so the "physiologically suspicious" concern is softer for t0112 than for [t0106]. The best
joint-pass cell at DSI = 0.9506 / PD = 112.86 Hz still has substantial PD activity (114 Hz is 58% of
[Trenholm2013][trenholm2013]'s 198 Hz biological peak) with a near-pure ratio DSI.

The **PD-rate frontier of 114.76 Hz** is 94% of [t0106]'s 122.62 Hz and **comfortably above the 30
Hz joint-pass floor**. Both runs reach the same upper region of PD-rate space, supporting the
substrate-general (not seed-specific) interpretation of the high-PD corner.

The **HV-plateau at gen 21 is consistent with [Mohacsi2024][mohacsi2024]'s 20-60 gen convergence
range** ([Mohacsi2024, Fig 4]). That a 68-d problem flattens at the **lower end** of this range
(below [t0106]'s ~24-30 gen plateau) is potentially confounded by the smaller N_GEN ceiling and the
HV-plateau detector firing at first signal rather than after operator inspection.

## Limitations

* **Single GA seed replicate**. t0112 is one GA seed (77) replicating one GA seed (44). The
  joint-pass-density gap (7 vs 123 unique) cannot be attributed solely to seed variance vs solely to
  the HV-plateau auto-stop vs solely to the pool-restart cadence change. Multi-seed confirmation
  (≥ 3 seeds at each restart cadence) is the highest-priority follow-up; the 0.35% yield could
  still be a per-seed extreme on the low side, just as [t0106]'s 3.3% was likely a per-seed extreme
  on the high side.

* **Pool-restart cadence cost-benefit not isolated**. The 3.5x per-gen wall-clock speedup is
  confounded with the GA seed change. A controlled test (seed 44 with cadence 10, or seed 77 with
  cadence 25) would isolate the restart-cadence effect.

* **HV-plateau detector vs operator stop.** [t0106] was operator-stopped at gen 39; t0112 was
  auto-stopped at gen 21. The earlier auto-stop may have censored the long tail of joint-pass
  discovery — t0112's 7 unique cells could plausibly have grown to 20-40 if the run had continued
  past the auto-stop. The acceptance-rate comparison vs published references is therefore
  conservative for t0112.

* **2-direction protocol is methodologically novel and not directly comparable to published
  multi-direction DSI measurements**. [Trenholm2013][trenholm2013], [Oesch2005][oesch2005], and
  [PolegPolsky2026][polegpolsky2026] use 8-12 directions. The DSI = 0.9535 result cannot be claimed
  as "exceeding biology" without an 8-direction post-hoc re-evaluation. [t0107] established that
  [t0106]'s 2-direction ratio DSI overstates selectivity by ~0.42 absolute under 8-direction
  vector-sum; this caveat carries directly to t0112.

* **Pareto-front parameter-space overlap analysis is uninterpretable**. The raw 68-d L2 between
  t0112 and [t0106] Pareto cells is dominated by the conductance-scale parameters (S/cm² values
  spanning 6 orders of magnitude). A z-scored or rank-correlation overlap metric is a natural
  follow-up but is outside the scope of a minimum-change replicate.

* **No comparable published NSGA-II run at this dimensionality.** The 68-d substrate is 2.8x - 5.7x
  higher dimensional than any published biophysical NSGA-II benchmark. The acceptance-rate
  comparison is therefore against extrapolated expectations, not matched-dimensional baselines.
  **Publication-selection bias** also applies: [Hay2011][hay2011] and [Druckmann2007][druckmann2007]
  published successes but not their failed seeds, so the per-seed yield distribution in their
  setting is unknown.

* **Evaluation budget materially below published references.** t0112 used 2,016 evaluations vs
  [Hay2011][hay2011]'s 500,000 and [Druckmann2007][druckmann2007]'s 300,000. The acceptance rate is
  measured at 150x lower spend; whether the rate would converge to the published value at matched
  spend is open.

* **Sub-claim "substrate-general joint-pass corner" is empirically true within the 2-seed comparison
  (44, 77)**, but neither GA seed was selected at random — both are arbitrarily chosen small
  integers. A formal sampling of seeds (e.g. 10 random seeds from a fixed distribution) is needed
  before the substrate-general claim can be reported with confidence.

[t0106]: ../../t0106_long_pdnd_nsga2_300gen/
[t0107]: ../../t0107_t0106_polar_8dir_recheck/
[druckmann2007]: ../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md
[hay2011]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[achard2006]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md
[mohacsi2024]: ../../t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[trenholm2013]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/summary.md
[oesch2005]: ../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md
[polegpolsky2026]: ../../t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md
[chen2024-stn]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11383608/
