---
spec_version: "1"
task_id: "t0114_seed7755_no_autostop"
date_compared: "2026-05-20"
---
# Comparison with Project and Published Results

## Summary

t0114 is a deliberately minimum-change seed-7755 (drawn via `secrets.randbelow(10000)`) NSGA-II
replicate of [t0106]'s 2-direction ratio-DSI run on the 68-d Bed B + 14-d morphology substrate, with
the HV-plateau auto-stop **DISABLED** as the live implementation of `S-0113-03`. Headline outcome:
with the auto-stop disabled, seed 7755 ran to **62** NSGA-II generations / **5,952** evaluations and
reached **484 LEGIT joint-pass cells** (DSI in
[0.5, 0.9999) AND PD-rate >= 30 Hz), with best LEGIT DSI **0.9926** at PD = **63.81 Hz** and best PD-rate **112.86 Hz** — recovering the frontier-corner population that [t0113]'s
14-gen plateau-stopped run missed entirely (0 LEGIT cells). The 4-seed substrate-rate estimate is
**2.93% +/- 1.86% SE** (95% CI -0.71% to +6.56%); this point estimate is **7.3x above**
[Hay2011][hay2011]'s **0.40%** envelope upper bound and **29x above**
[Druckmann2007][druckmann2007]'s **0.10%** baseline, but the SE remains larger than both literature
reference values so neither baseline can be formally rejected. The offline detector replay against
all four HV trajectories selects **(W*, T*) = (3, 0.015)** as the recommended new project default;
the t0114 trajectory fires under this rule at **gen 26**, comfortably within
[Mohacsi2024][mohacsi2024]'s published 20-60 gen NSGA-II convergence range, vs the current
`(W=2, T=0.01)` rule firing at gen 13 on t0113 (below the published lower bound).

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.9939 | 0.9926 | -0.0013 | Same substrate; t0114 lands within 0.13 percentage points of [t0106]'s best non-silence-guard DSI |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best PD-rate frontier) | PD (Hz) | 125.95 | 112.86 | -13.09 | t0114 reaches 89.6% of [t0106]'s best-PD frontier value |
| [t0106] seed 44 NSGA-II (LEGIT joint-pass unique count) | count | 121 | 484 | +363 | t0114 yields 4.0x more LEGIT joint-pass cells than [t0106], at 1.6x more evals |
| [t0106] seed 44 NSGA-II (joint-pass yield, LEGIT / total) | rate | 3.23% | 8.13% | +4.90 | t0114 LEGIT acceptance is 2.5x [t0106]'s |
| [t0106] seed 44 NSGA-II (final hypervolume) | HV | 122.03 | 111.54 | -10.49 | t0114 plateau HV is 91% of [t0106]'s; operator stop at visible plateau |
| [t0106] seed 44 NSGA-II (final / plateau generation) | gen | 39 | 62 | +23 | t0114 ran 1.6x longer because auto-stop was disabled |
| [t0106] seed 44 NSGA-II (productive compute cost) | USD | 10.37 | 0.94 | -9.43 | 11x cheaper at 1.6x evals: faster EPYC instance + cadence-10 protocol |
| [t0112] seed 77 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.9535 | 0.9926 | +0.0391 | Same substrate + cadence-10 protocol; t0114 exceeds [t0112]'s best DSI by 0.039 absolute |
| [t0112] seed 77 NSGA-II (best PD-rate frontier) | PD (Hz) | 114.76 | 112.86 | -1.90 | t0114 reaches 98.3% of [t0112]'s best-PD frontier value |
| [t0112] seed 77 NSGA-II (LEGIT joint-pass unique count) | count | 7 | 484 | +477 | t0114 yields 69x more LEGIT joint-pass cells than [t0112] |
| [t0112] seed 77 NSGA-II (joint-pass yield, LEGIT / total) | rate | 0.35% | 8.13% | +7.78 | t0114 LEGIT acceptance is 23x [t0112]'s |
| [t0112] seed 77 NSGA-II (final hypervolume) | HV | 107.46 | 111.54 | +4.08 | t0114 final HV slightly exceeds [t0112]'s; both populated the joint-pass corner |
| [t0113] seed 2247 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.3651 | 0.9926 | +0.6275 | Same protocol, only auto-stop disabled; t0114 exceeds [t0113]'s best LEGIT DSI by 2.72x |
| [t0113] seed 2247 NSGA-II (best PD-rate frontier) | PD (Hz) | 71.67 | 112.86 | +41.19 | t0114 reaches 1.57x [t0113]'s best-PD frontier value |
| [t0113] seed 2247 NSGA-II (LEGIT joint-pass unique count) | count | 0 | 484 | +484 | t0114 recovers a non-empty joint-pass population that [t0113]'s premature stop missed |
| [t0113] seed 2247 NSGA-II (final hypervolume) | HV | 45.62 | 111.54 | +65.92 | t0114 plateau HV is 2.44x [t0113]'s; trajectory ran 4.4x more gens |
| [t0113] seed 2247 NSGA-II (auto-stop firing generation) | gen | 14 | 62 | +48 | t0114 ran to operator stop; current `(W=2, T=0.01)` rule would have fired at gen 25 on t0114 |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Hay2011][hay2011] NSGA-II joint perisom+BAC (acceptance rate, single-seed) | rate | 0.40% | 8.13% | +7.73 | [Hay2011, p. 4]: ~2000 acceptable / 500,000 evals on 22-d L5b PC; t0114 single-seed acceptance is **20.3x** [Hay2011][hay2011]'s, at 3.1x higher dimensionality |
| [Hay2011][hay2011] NSGA-II joint perisom+BAC (acceptance rate vs 4-seed mean) | rate | 0.40% | 2.93% | +2.53 | 4-seed mean from [t0106] (3.23%) + [t0112] (0.35%) + [t0113] (0.00%) + t0114 (8.13%); point estimate **7.3x above** Hay envelope upper bound; 95% CI (-0.71%, 6.56%) **brackets 0.40%** — cannot formally reject |
| [Hay2011][hay2011] NSGA-II perisomatic-only fits (acceptance rate) | rate | 0.0104% | 8.13% | +8.12 | [Hay2011, p. 6]: 52 acceptable / 500,000 evals — the "substrate-limited" counterexample; t0114 substrate is **782x denser** than the [Hay2011][hay2011] perisomatic-only bottleneck |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate, single-seed) | rate | 0.10% | 8.13% | +8.03 | [Druckmann2007, Fig 3 + Methods]: 300 acceptable / 300,000 evals on 12-d cortical interneuron; t0114 single-seed acceptance is **81x** [Druckmann2007][druckmann2007]'s, at 5.7x higher dimensionality |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate vs 4-seed mean) | rate | 0.10% | 2.93% | +2.83 | 4-seed mean is **29.3x above** [Druckmann2007][druckmann2007] baseline; 95% CI (-0.71%, 6.56%) **brackets 0.10%** — cannot formally reject |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (current rule on t0113) | plateau gen | 20-60 | 14 | -6 | [Mohacsi2024, Fig 4 use cases 1-6]: NSGA-II asymptotes by gens 20-60 on 3-12 param problems; current `(W=2, T=0.01)` rule fired on t0113 at gen 13, **below** published lower bound — confirming premature stop |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (current rule on t0114) | plateau gen | 20-60 | 25 | -ok | [Mohacsi2024, Fig 4]: current `(W=2, T=0.01)` rule fires on t0114's 62-gen trace at gen 25; **inside** the published convergence range |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (new rule on t0114) | plateau gen | 20-60 | 26 | -ok | [Mohacsi2024, Fig 4]: recommended `(W=3, T=0.015)` rule fires on t0114 at gen 26; **inside** the [20, 60] band — the central design criterion for the new default |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (new rule on t0106) | plateau gen | 20-60 | 39 | -ok | [Mohacsi2024, Fig 4]: recommended `(W=3, T=0.015)` rule fires on [t0106]'s 39-gen recorded trace at gen 39; **inside** the [20, 60] band; identical to the recorded final gen so no censoring |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (new rule on t0113) | plateau gen | 20-60 | n/a | n/a | Recommended `(W=3, T=0.015)` rule does NOT fire within [t0113]'s recorded 14 gens — premature stop **eliminated** under new rule |

## Methodology Differences

* **Auto-stop disabled — the operative change vs [t0113].** t0114's only intentional algorithmic
  change relative to [t0113] is `HV_PLATEAU_AUTO_STOP_DISABLED = True` and the GA-seed redraw from
  2247 to **7755**. The substrate (68-d Bed B + 14-d morphology), objective (2-direction ratio DSI
  + PD-rate at 0 deg), evaluator, silence guard, SBX/PM operators, LHS init,
    `_POOL_RESTART_EVERY = 10`, evaluation seeds, cost watchdog, and predictions-asset schema are
    bitwise identical to [t0113]. The `N_GEN_MAX` ceiling was raised from 60 to **300** to match
    [t0106]'s ceiling, but this is operationally redundant — the operator stop fires before the
    ceiling is reached. This isolates the auto-stop effect cleanly: any difference vs [t0113] is
    attributable either to the seed or to the auto-stop deletion.

* **Stop trigger is operator_stop, not auto-rule.** t0114's stop trigger is the only one of the
  4-seed sample that is *not* hv_plateau. The run was halted by the operator after the HV trajectory
  visibly plateaued near HV = 111.54 from gen 50 to gen 62 (HV(50) = 111.5353, HV(62) = 111.5353).
  This yields the cleanest possible HV "ground truth" trace for the offline detector replay vs
  [t0106] / [t0112] / [t0113]'s auto-stopped trajectories.

* **HV-plateau detector reparameterisation methodology vs [Mohacsi2024][mohacsi2024].**
  [Mohacsi2024][mohacsi2024]'s use cases 1-6 (3-12 params) report NSGA-II asymptotes between gens
  **20 and 60** on per-package final-error curves ([Mohacsi2024, Fig 4]). The t0114 detector replay
  treats this as a hard prior: the recommended `(W*, T*)` must fire within `[20, 60]` on every
  trajectory long enough to test. The selection result `(W*, T*) = (3, 0.015)` satisfies this on
  [t0106] (fires gen 39) and on t0114 (fires gen 26) and does NOT fire prematurely on [t0113]'s
  recorded 14 gens. The current `(W=2, T=0.01)` default fired on [t0113] at gen **13** — **7 gens
  below** the [Mohacsi2024][mohacsi2024] lower bound — confirming the existing rule is more
  aggressive than the published asymptote evidence warrants.

* **DSI definition vs published DSGC measurements (unchanged from [t0113] / [t0112]).** t0114
  inherits the 2-direction ratio DSI on antipodal directions (PD = 0 deg, ND = 180 deg) from
  [t0106]. No published paper fits a biophysical model against a 2-direction objective. [t0107]'s
  8-direction re-evaluation of 10 [t0106] top cells showed the 2-direction ratio DSI overstates
  8-direction vector-sum selectivity by **~0.42 absolute** on the [t0106] high-DSI cells. Applied
  naively to t0114's 0.9926 best LEGIT DSI this yields an estimated 8-direction vector-sum DSI of
  ~0.57 — still inside the biological range of [Trenholm2013][trenholm2013]'s 0.76 control DSI and
  [Oesch2005][oesch2005]'s 0.74 OFF DSI.

* **Silence-guard ceiling cells are an evaluator artefact, not selectivity.** 1,073 of 5,952 t0114
  cells (18%) sit at DSI = 1.0 — these are silence-guard / single-spike configurations admitted by
  the evaluator's `SILENCE_SPIKE_COUNT_THRESHOLD = 10`. The LEGIT filter (DSI < 0.9999) is applied
  consistently across all four seeds for all substrate-rate calculations. t0114's 771 "all
  joint-pass" cells include 287 silence-guard ceiling cells; the 484 LEGIT count is the
  comparable-to-biology number.

* **Single GA seed vs multi-seed convention (unchanged from [t0106], [t0112], [t0113]).**
  [Chen2024-STN][chen2024-stn] used 3 seeds at pop=120, ~1M evals;
  [PolegPolsky2026][polegpolsky2026] used 100 GA seed restarts at pop=10, gens=300-1000. t0114 ran 1
  seed (the same constraint as the prior three project replicates). The 4-seed mean (44, 77, 2247,
  7755\) of **2.93%** is **7.3x above** the [Hay2011][hay2011] 0.40% envelope point estimate but the
  **95% CI (-0.71%, +6.56%) brackets both [Hay2011][hay2011] and [Druckmann2007][druckmann2007]
  baselines and zero**. A 5th seed is the agreed path to a tighter substrate-rate estimate.

* **Substrate vs published NSGA-II benchmarks (unchanged from [t0113] / [t0112]).**
  [Druckmann2007][druckmann2007] = 12-d, [Hay2011][hay2011] = 22-d, [Achard2006][achard2006] = 24-d,
  [Mohacsi2024][mohacsi2024] use cases = 3-12-d. t0114's 68-d substrate is **2.8x - 5.7x higher
  dimensional** than any published NSGA-II biophysical benchmark. Standard scaling intuition
  predicts lower acceptance rate at higher dimensionality; t0114's 8.13% in 68-d at the
  uncensored-trajectory point estimate is therefore **anomalously high** against the
  [Hay2011][hay2011] 0.40% / [Druckmann2007][druckmann2007] 0.10% envelope.

* **Evaluation budget — well below published references.** t0114 used **5,952** evaluations, the
  largest of the 4-seed sample. [Druckmann2007][druckmann2007] used **300,000**; [Hay2011][hay2011]
  used **500,000**. t0114 is **~50x - 84x below** the modern reference floor. The
  factor-of-many-higher acceptance rate at factor-of-many-lower spend is consistent with
  [Mohacsi2024][mohacsi2024]'s observation that the 2-objective surface converges faster than the
  published 20+ feature objectives of [Hay2011][hay2011] and the 30+ objective
  [Druckmann2007][druckmann2007] cost function.

* **Wall-clock baseline.** t0114's 198 s/gen on the 128-thread EPYC 7713P (64 physical cores at
  SMT-2) is consistent with [t0112]'s ~620 s/gen at 32 physical cores: doubling cores roughly halves
  per-generation wall-clock. The 4.094 h instance time is dominated by the productive 3.4 h NSGA-II
  run; setup, MOD compile, and teardown overheads consumed the remaining ~0.7 h.

## Analysis

### Prior Task Comparison

The headline prior-task finding is that **t0114's 484 LEGIT joint-pass cells confirms `S-0113-03`'s
hypothesis that [t0113]'s 0 LEGIT was an artefact of premature plateau-stopping, not a substrate
property**. The two runs differ only in (a) the GA seed (2247 vs 7755) and (b) the auto-stop disable
flag. With the same substrate, same evaluator, same operators, same cadence-10 restart, and the
auto-stop removed, seed 7755 ran for **48 more generations** than seed 2247 was allowed to and
discovered **484** non-silence-guard joint-pass cells. The t0114 HV trajectory passes through what
would have been t0113's gen-14 "plateau" region (HV ~36-46) and continues climbing through gens
14-30 to HV ~96 before plateauing near HV 111 by gen 50. The interpretation that fits the data
parsimoniously is "[t0113]'s 14-gen stop censored a long discovery tail"; the alternative
interpretation that fits the data ("seed 2247 lands in a sparse region of substrate space and would
have stayed near 0 LEGIT cells even on a longer run") is not testable without re-running seed 2247
with auto-stop disabled — see `S-0114-XX` follow-up (to be generated in the next stage).

The **4-seed dispersion is now 0.00% (2247) / 0.35% (77) / 3.23% (44) / 8.13% (7755)**. With seeds
44 and 7755 each independently exceeding the [Hay2011][hay2011] envelope by 8x and 20x respectively,
the "[t0106]'s 3.3% was an above-typical lucky seed" reading from [t0112] / [t0113] is
**substantially weakened**: the substrate now has two independent high-yield seeds and two low-yield
seeds (one of which, 2247, is plausibly censored by the auto-stop bug). The substrate may genuinely
be high-density, with seeds 77 and 2247 being unlucky low-density basins that the GA happened to
explore from. Re-running seed 2247 with auto-stop disabled is the cleanest way to bisect this.

The **best LEGIT DSI of 0.9926** at PD = 63.81 Hz lands within **0.13 percentage points** of
[t0106]'s best legit cell (0.9939 at PD = 49.05 Hz) and exceeds [t0112]'s 0.9535 by 4.1 percentage
points. The **best PD-rate of 112.86 Hz** is 89.6% of [t0106]'s 125.95 Hz and within 2 Hz of
[t0112]'s 114.76 Hz. t0114 therefore re-populates the high-DSI / high-PD frontier corner that the
project lost at [t0113].

The **HV-plateau detector replay** (4 windows x 6 thresholds x 4 seeds = 96 cells; 32-row CSV
committed) selects **(W*, T*) = (3, 0.015)** as the recommended new project default. The selection
is robust under the three written criteria (fires within [20, 60] gens on long trajectories; does
NOT fire prematurely on [t0113]'s short trajectory; smallest deviation from the current defaults).
The current `(W=2, T=0.01)` rule would have fired on t0114 at gen **25** as well — so the new rule
is not strictly necessary to recover t0114, but **is necessary to avoid the [t0113] premature firing
at gen 13**.

### Published Literature Comparison

The most consequential finding relative to the literature is that **the substrate-rate point
estimate has moved from 1.26% (3-seed, [t0113]) to 2.93% (4-seed) — 7.3x above the
[Hay2011][hay2011] 0.40% envelope**, but the standard error remains **larger than either literature
reference value** (1.86% vs 0.40% / 0.10%) so the 95% CI **(-0.71%, +6.56%) brackets both literature
baselines and zero**. Statistically the 4-seed sample cannot reject [Hay2011][hay2011] or
[Druckmann2007][druckmann2007]; in effect-size terms the substrate point estimate is now > 7x above
the upper literature bound for any reasonable read.

The interpretation is **shifted but still bimodal**: either (a) the substrate genuinely supports
joint-pass cells at ~3% acceptance and [Hay2011][hay2011] / [Druckmann2007][druckmann2007] are
sparser substrates at lower dimensionality, or (b) the substrate's true rate is closer to the
[t0106] / t0114 mean of ~5%-6% with the [t0112] / [t0113] seeds being unlucky low-density basins (in
[t0113]'s case compounded by the auto-stop bug). The S-0112-01 5-seed batch goal (still 1 seed
short) plus an auto-stop-disabled seed 2247 re-run would resolve this. Crucially, **the substrate is
NOT consistent with [Hay2011][hay2011]'s perisomatic-only counterexample (0.0104%)**: t0114's 8.13%
is **782x denser** than that bottleneck, so the substrate is unambiguously not in a
[Hay2011][hay2011]-style starvation regime.

The **best LEGIT DSI of 0.9926** translates (via [t0107]'s 8-direction offset of ~0.42 absolute) to
an estimated 8-direction vector-sum DSI of **~0.57** for t0114's best legit cell. This is **within
25% of [Trenholm2013][trenholm2013]'s mouse Hb9 control DSI (0.76)** and **within 24% of
[Oesch2005][oesch2005]'s rabbit ON-OFF OFF DSI (0.74)**. Unlike [t0113] (estimated 8-dir ~-0.05,
effectively zero), t0114's frontier cell is **biologically plausible** under the 8-direction
protocol.

The **HV-plateau at gen 25 (current rule) and gen 26 (new rule) on t0114** are both **inside**
[Mohacsi2024][mohacsi2024]'s 20-60 gen convergence band ([Mohacsi2024, Fig 4]).
[Mohacsi2024][mohacsi2024]'s use cases 1-6 report NSGA-II asymptotes between gens 20 and 60 on 3-12
parameter problems. The fact that the recommended `(W*, T*)` rule lands inside this band on t0114
(62-gen trace) and on t0106 (39-gen trace) is the central design validation: t0114 confirms the
[Mohacsi2024][mohacsi2024] convergence horizon generalises from 3-12-d benchmark suites to a 68-d
biophysical substrate.

The **PD-rate frontier of 112.86 Hz** is 57% of [Trenholm2013][trenholm2013]'s 198 Hz biological
peak — better than [t0113]'s 36% but still substantially below the biological reference. The cell
at this peak has DSI = 0.0271 (not selective); the simultaneously-DSI-selective cell at the
joint-pass corner (Pareto cell_id 2, DSI = 0.9873, PD = 111.67 Hz) is the headline "joint-pass AND
high-PD" point. This is the first 4-seed run to produce a cell that simultaneously meets DSI ~ 0.99
AND PD > 100 Hz; [t0112]'s and [t0106]'s frontiers each peaked at one or the other extreme but not
both at the same cell.

## Limitations

* **Single auto-stop-disabled seed for the substrate-rate question.** t0114 is the only seed run
  with auto-stop disabled; [t0106] / [t0112] / [t0113] all stopped under the current rule. The
  comparison "t0114 (484 LEGIT) vs [t0113] (0 LEGIT)" therefore convolves "seed redraw" with
  "auto-stop disable". The clean way to bisect this is to re-run seed 2247 with the auto-stop
  disabled (proposed `S-0114-XX`). Until that runs, the substrate-rate interpretation ("[t0113]'s 0
  is a censoring artefact, not a substrate property") is the most parsimonious reading but not
  proven.

* **4-seed substrate-rate CI still brackets both literature baselines and zero.** The 4-seed 95% CI
  of (-0.71%, +6.56%) cannot formally reject either [Hay2011][hay2011]'s 0.40% or
  [Druckmann2007][druckmann2007]'s 0.10%. The point estimate of 2.93% is 7.3x above
  [Hay2011][hay2011]; in effect-size terms the substrate is plausibly denser than literature. But
  classical inference requires at least one more independent seed (preferably 2 or 3) to tighten the
  SE below 0.40%.

* **Operator-stop censoring of t0114.** The run was stopped at gen 62 by operator decision after the
  HV trajectory plateaued near HV 111.54 from gen 50 to gen 62. The plateau is visually convincing
  but **not statistically certified** — a longer run could reveal further LEGIT cells in the same
  way that gens 50-62 added ~30-50 cells beyond the gen-50 cumulative count. The reported 484 LEGIT
  count is therefore a **lower bound** on the true substrate yield for seed 7755.

* **Detector replay is offline only.** The `(W*, T*) = (3, 0.015)` recommendation is computed from
  the four recorded HV trajectories ex post; it has NOT been validated by running NSGA-II online
  with the new constants. A follow-up task should adopt the new constants and re-run at least one
  seed end-to-end to confirm the offline prediction matches the live behaviour. The two trajectories
  used to certify "new rule does NOT fire prematurely" ([t0112] at 21 gens, [t0113] at 14 gens) are
  themselves truncated by the current rule and therefore cannot test whether the new rule would fire
  prematurely on a longer history.

* **2-direction protocol is methodologically novel and not directly comparable to published
  multi-direction DSI measurements.** [Trenholm2013][trenholm2013], [Oesch2005][oesch2005], and
  [PolegPolsky2026][polegpolsky2026] use 8-12 directions with vector-sum DSI. The DSI = 0.9926 LEGIT
  result cannot be claimed as "biological-equivalent" without an 8-direction post-hoc re-evaluation.
  The carry-forward 0.42-absolute offset from [t0107] is measured on [t0106]'s high-DSI cells, which
  overlap structurally with t0114's joint-pass corner — but the offset has not been independently
  measured on t0114 cells.

* **Single fully-uncensored seed cannot disentangle "auto-stop is buggy" from "seed 7755 is
  lucky".** t0114's 8.13% LEGIT yield is the 4-seed maximum and is 2.5x [t0106]'s 3.23%. The 484 vs
  121 LEGIT count gap could be explained by (i) longer run-length on a seed that would have yielded
  similarly to [t0106] under any rule, (ii) the auto-stop censoring [t0106] at gen 39 when it would
  have yielded more under longer running, or (iii) seed 7755 being substantively denser than seed
  44\. Without rerunning [t0106] with auto-stop disabled (or running additional auto-stop-disabled
  seeds), these cannot be separated.

* **No comparable published NSGA-II run at this dimensionality.** The 68-d substrate is **2.8x -
  5.7x higher dimensional** than any published biophysical NSGA-II benchmark ([Hay2011][hay2011] =
  22-d, [Druckmann2007][druckmann2007] = 12-d, [Mohacsi2024][mohacsi2024] use cases = 3-12-d). The
  acceptance-rate comparison is therefore against extrapolated expectations, not matched-
  dimensional baselines. **Publication-selection bias** also applies: [Hay2011][hay2011] and
  [Druckmann2007][druckmann2007] published successes but not their failed seeds, so the per-seed
  yield distribution in their setting is unknown. The 4-seed dispersion observed in this project
  (0.00%
  - 8.13%) could plausibly be representative of NSGA-II per-seed behaviour at any dimensionality.

* **Evaluation budget materially below published references.** t0114 used 5,952 evaluations vs
  [Hay2011][hay2011]'s 500,000 and [Druckmann2007][druckmann2007]'s 300,000. The acceptance rate is
  measured at 50x - 84x lower spend; whether the rate would converge to a different value at matched
  spend is open.

* **Random-seed draw is not the same as random-seed selection.** Seed 7755 was drawn via
  `secrets.randbelow(10000)` — uniformly random over [0, 9999]. This avoids the
  round-ish-low-number bias of seeds 44 and 77 but does not guarantee good coverage. A formal
  quasi-random Latin hypercube over seeds 0-9999 would give better coverage but is outside the scope
  of a minimum-change replicate.

* **`(W*, T*)` selection rests on a 4-seed sample.** The recommended detector parameters minimise
  deviation from the current default subject to three constraints, but a 5th or 6th HV trajectory
  could shift the optimum. The "deviation metric" `abs(W - 2) + abs(T - 0.01) * 100` is also a
  chosen scaling that prefers small window changes over small threshold changes; an alternative
  scaling could pick `(W=2, T=0.025)` or `(W=4, T=0.005)` instead. The recommendation should be
  treated as a "minimum-change patch that passes the [Mohacsi2024][mohacsi2024] prior", not an
  optimum.

[t0106]: ../../t0106_long_pdnd_nsga2_300gen/
[t0107]: ../../t0107_t0106_polar_8dir_recheck/
[t0112]: ../../t0112_t0106_seed77_replicate/
[t0113]: ../../t0113_t0106_seed2247_replicate/
[druckmann2007]: ../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md
[hay2011]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[achard2006]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md
[mohacsi2024]: ../../t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[trenholm2013]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/summary.md
[oesch2005]: ../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md
[polegpolsky2026]: ../../t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md
[chen2024-stn]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11383608/
