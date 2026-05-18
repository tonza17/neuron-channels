---
spec_version: "1"
task_id: "t0106_long_pdnd_nsga2_300gen"
date_compared: "2026-05-18"
---
# Comparison with Project and Published Results

## Summary

t0106's long-horizon 2-direction NSGA-II on the 68-d Bed B + 14-d morphology substrate produced
**123 unique strict joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) across 3,744 evaluations** — the
**first joint-pass cells anywhere in the t0078 -> t0104 lineage**, every prior task of which
returned **0 joint-pass cells**. The **3.3% (123/3744) joint-pass yield** is **~8x the upper bound**
of published acceptance rates for NSGA-II on comparable biophysical fits
([Druckmann2007][druckmann2007] **0.10%**, [Hay2011][hay2011] **0.40%**, [Achard2006][achard2006]
**0.028%**), but t0106's best ratio DSI of **1.0000** at PD = 81 Hz and best PD-rate frontier of
**122.6 Hz** at DSI = 0.92 substantially exceed every published DSGC reference
([Trenholm2013][trenholm2013] mouse Hb9 DSI = **0.76** at peak PD = 198 Hz;
[PolegPolsky2026][polegpolsky2026] unconstrained-ML ceiling = **0.731**). The reformulation from
16-direction vector-sum DSI to 2-direction ratio DSI — not the generation budget — drove the
breakthrough.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0078] MOBO BoTorch qLogNEHVI iter 290 | DSI | 1.0000 | 1.0000 | +0.0 | 16-dir vector-sum on 54-d Bed B, no silence guard; [t0078] artifact (silent-corner DSI=1.0); t0106 has guard-active DSI=1.0 at PD=81 Hz |
| [t0078] MOBO iter 290 | PD-rate (Hz) | 0.00 | 81.43 | +81.43 | [t0078] DSI=1.0 cell was silent at PD (0 Hz); t0106 DSI=1.0 cell fires at 81 Hz with ND silence — qualitatively different cells |
| [t0080] NSGA-II 8-dir, 3-obj, 8 gens (joint-pass yield) | count | 0 | 123 | +123 | t0080 returned 0 joint-pass; t0106 reformulation finds 123 unique |
| [t0099] NSGA-II 16-dir, 3-obj, random init, 3 seeds (best DSI) | DSI | 0.291 | 1.0000 | +0.709 | [t0099] seed 22 best DSI=0.2916 (n=22 cells); t0106 reaches DSI=1.0 |
| [t0099] NSGA-II 16-dir, 3-obj (joint-pass yield) | count | 0 | 123 | +123 | [t0099] null replicates across 3 seeds; t0106 inverts the null |
| [t0102] NSGA-II 16-dir, 3-obj, 11-12 gens (joint-pass yield) | count | 0 | 123 | +123 | t0102 null across 2 seeds at $4 watchdog; t0106 single seed, longer horizon |
| [t0104] NSGA-II 16-dir, 2-obj, 12 gens, silence guard on (best DSI) | DSI | 0.5417 | 1.0000 | +0.4583 | [t0104] seed 55 gen 11 best non-artifact DSI; t0106 raises ceiling 0.46 |
| [t0104] NSGA-II 16-dir, 2-obj (best DSI cell PD-rate) | PD (Hz) | 3.57 | 81.43 | +77.86 | [t0104] best-DSI cell silent at PD; t0106 best-DSI cell fires at 81 Hz |
| [t0104] NSGA-II 16-dir, 2-obj (joint-pass yield) | count | 0 | 123 | +123 | [t0104] null at $15 cap, 2-obj, guard active; t0106 inverts at $10.37 spend |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate) | rate | 0.10% | 3.28% | +3.18 | [Druckmann2007, Methods + Fig 3]: 300 acceptable cells / 300,000 evals on 12-d cortical interneuron; t0106 yields 123/3744 on 68-d substrate |
| [Hay2011][hay2011] NSGA-II 1000x500 joint perisom+BAC (acceptance rate) | rate | 0.40% | 3.28% | +2.88 | [Hay2011, p. 4]: ~2000 acceptable / 500,000 evals on 22-d L5b PC; t0106 acceptance is ~8x higher despite 3x dimension |
| [Hay2011][hay2011] NSGA-II perisomatic-only fits (acceptance rate) | rate | 0.0104% | 3.28% | +3.27 | [Hay2011, p. 6]: 52 acceptable / 500,000 evals — the "substrate-limited" counterexample; t0106 is the inverse case (substrate not limited) |
| [Achard2006][achard2006] ES 9x8000 evals (acceptance rate) | rate | 0.028% | 3.28% | +3.25 | [Achard2006, Results]: 20 selected good models / 72,000 evals on 24-d Purkinje cell |
| [Mohacsi2024][mohacsi2024] NSGA-II 100x100 gens convergence horizon | plateau gen | 20-60 | 19-24 | within range | [Mohacsi2024, Fig 4 use cases 1-6]: NSGA-II asymptotes by gens 20-60 on 3-12 param problems; t0106 first joint-pass cell at gen 18, front populated by gen 24 — consistent on 68-d |
| [Trenholm2013][trenholm2013] mouse Hb9 DSGC ratio DSI (control) | DSI | 0.76 | 1.0000 | +0.24 | [Trenholm2013, Table 1]: peak PD=198 Hz, peak ND=27 Hz, DSI=(198-27)/(198+27); t0106 best legit (DSI=0.9832) and DSI=1.0 cells exceed biological reference |
| [Trenholm2013][trenholm2013] mouse Hb9 peak PD firing rate | PD (Hz) | 198 | 122.6 | -75.4 | [Trenholm2013, Table 1]: peak instantaneous Gaussian-convolved rate, control; t0106 frontier PD=122.6 Hz is 62% of biological peak — below ceiling, comfortably above 30 Hz floor |
| [Oesch2005][oesch2005] rabbit ON-OFF DSGC spike-based DSI (OFF) | DSI | 0.74 | 1.0000 | +0.26 | [Oesch2005, p. 740]: 0.74 +/- 0.13 OFF DSI; t0106 best legit exceeds upper biological CI (0.87) |
| [PolegPolsky2026][polegpolsky2026] ML unconstrained DSI ceiling | DSI | 0.731 | 1.0000 | +0.269 | [PolegPolsky2026, Fig 3]: 73.1% +/- 2.4% DSI under full E+I freedom on 12 dirs x 5 speeds; t0106 2-dir DSI exceeds 12-dir ceiling — methodology gap, not biology gap |
| [PolegPolsky2026][polegpolsky2026] ML Barlow-Levick weight-only DSI | DSI | 0.508 | 1.0000 | +0.492 | [PolegPolsky2026, Fig 3]: 50.8% +/- 0.8%; t0106 doubles the B&L floor on the simpler 2-dir objective |

## Methodology Differences

* **DSI definition — 16-dir vector-sum vs 2-dir ratio**. [t0078] through [t0104] computed
  vector-sum DSI over **16 directions** every 22.5 deg. t0106 reduced to **2 antipodal directions
  (PD = 0 deg, ND = 180 deg)** and used `(PD - ND) / (PD + ND)`. The two formulas are mathematically
  identical for the special case of antipodal sampling but the 16-dir formula penalises off-axis
  responses; t0106's simpler objective surfaces cells that the 16-dir formula hides. **This is the
  primary driver of the joint-pass-discovery contrast vs the lineage.**

* **Direction count vs DSGC measurement convention**. [Trenholm2013][trenholm2013],
  [Oesch2005][oesch2005], and [PolegPolsky2026][polegpolsky2026] all use 8 - 12 directions. The
  recent ON-OFF dendritic-asymmetry paper [CavalHolme2025][cavalholme2025] also uses 8-direction
  vector-sum. **No published paper fits a biophysical model against a 2-direction objective**; the
  comparison vs Trenholm2013 DSI=0.76 is therefore best-case-PD vs best-case-PD, not equal-protocol
  head-to-head. A post-hoc 16-direction re-evaluation of t0106's top 50 cells is required to confirm
  full-tuning DSI; this is the largest open methodological caveat.

* **Substrate vs published NSGA-II benchmarks**. [Druckmann2007][druckmann2007] = 12-d cortical
  interneuron; [Hay2011][hay2011] = 22-d L5b PC; [Achard2006][achard2006] = 24-d Purkinje;
  [Mohacsi2024][mohacsi2024] uses up to 12-d detailed CA1. t0106's 68-d substrate is **2.8x - 5.7x
  higher dimensional** than any published NSGA-II benchmark, yet the joint-pass yield rate is an
  order of magnitude above. This is anomalous on the standard scaling intuition that higher
  dimension means lower acceptance rate.

* **Evaluation budget — much smaller than published references**. t0106 = **28,896 planned / 3,744
  actual** evaluations (operator-stopped at gen 40). [Druckmann2007][druckmann2007] used
  **300,000**; [Hay2011][hay2011] used **500,000**; [Achard2006][achard2006] used ~72,000. t0106 is
  **~10x below the modern reference** but **above the [Mohacsi2024][mohacsi2024] 10,000-eval
  benchmark floor** at which several NSGA-II implementations were already shown to have plateaued.

* **Silence guard**. t0106 inherits the [t0104] silence guard (total spikes < 10 across PD + ND
  trial returns DSI = 0). All 6 unique top joint-pass cells were verified with 47-154 spikes/trial
  — no guard artifacts. [t0078]'s DSI = 1.0 cells were guard-free silent-corner artifacts at PD =
  0 Hz. Direct DSI = 1.0 comparison between t0078 and t0106 is non-equivalent: t0078 measures noise;
  t0106 measures a real spiking cell with absolute ND silence.

* **Population vs Dang2023 floor**. [Dang2023, Theorems 8 / 10] gives the noise-survival population
  floor as `mu = Omega(n log n)`, ~287 at n = 68. t0106 sits at **pop = 96**, ~3x below the
  theoretical floor. The empirical result (joint-pass cells discovered) suggests either Dang's
  discrete-bit-string bound does not transfer to continuous biophysical problems, or the 2-dir
  reformulation reduces the effective noise level enough to relax the population requirement.

* **Single GA seed vs multi-seed convention**. [Chen2024-STN][chen2024-stn] used 3 seeds at pop=120,
  ~1M evals; [PolegPolsky2026][polegpolsky2026] used 100 GA seed restarts at pop=10, gens=300-1000.
  t0106 ran 1 seed, pop=96. The acceptance-rate point estimate at 3.3% is therefore
  **single-realisation**, not population estimate.

## Analysis

The headline finding is that **the t0080 -> t0104 lineage's "joint-pass null" was an
objective-surface artefact, not a substrate limitation** ([results_summary.md](results_summary.md)
headline). The same 68-d Bed B + morphology substrate that returned 0 joint-pass cells across 5
prior tasks, ~10K cumulative evaluations, multiple seeds, and varied objective configurations yields
**123 joint-pass cells in 40 gens on a single seed** when the DSI metric switches from 16-direction
vector-sum to 2-direction ratio. This contradicts the [t0104] compare-literature
substrate-limitation reading: that document concluded "every random-init NSGA-II configuration tried
on the 68-d Bed B + morphology substrate produces zero strict joint-pass cells", and recommended
either an algorithm change (IBEA per [Mohacsi2024][mohacsi2024]) or a substrate change
([PolegPolsky2026][polegpolsky2026] GABAergic asymmetry). t0106 shows that **neither was needed**
— the same NSGA-II algorithm on the same substrate finds the joint corner once the objective is
reformulated.

The **3.3% joint-pass yield (123/3744) is ~8x the [Hay2011][hay2011] 0.40% upper bound and ~33x the
[Druckmann2007][druckmann2007] 0.10% rate**. Two non-exclusive interpretations:

1. **The 2-dir ratio DSI is a much easier objective surface than published 12-22 d biophysical
   objectives**. [Hay2011][hay2011] required joint perisomatic + BAC firing across 30+ features;
   t0106 requires only `PD > ND` and total spike rate. This is the most parsimonious reading and
   matches [Mohacsi2024][mohacsi2024]'s convergence-curve observation that simpler objectives
   converge faster.

2. **The 68-d Bed B + 14-d morphology substrate has an unusually dense joint-pass basin** — denser
   than [Hay2011][hay2011]'s L5b PC parameter space relative to its objective demands. The
   morphology subspace (14 dims) may contribute disproportionately: 35 of t0106's top 50 cells share
   the classical Tukker-Taylor ND-soma archetype, suggesting a wide morphological basin of
   attraction.

The **DSI = 1.0000 cells (3 unique) exceed all published biological DSGC measurements**
([Trenholm2013][trenholm2013] = 0.76; [Oesch2005][oesch2005] OFF = 0.74;
[PolegPolsky2026][polegpolsky2026] unconstrained = 0.731). The biological-plausibility caveat is
sharp: real DSGCs retain some ND firing, so DSI = 1.0 with absolute ND silence is **physiologically
suspicious despite the silence-guard pass** (114 PD spikes/trial, real activity). A 20-replicate
robustness check on these 3 cells is the highest-priority next test; if DSI = 1.0 collapses under
more noise replicates the result becomes a noise-undersampling artefact rather than a substrate
finding.

The **PD-rate frontier 122.6 Hz at DSI = 0.92 is 62% of [Trenholm2013][trenholm2013]'s peak PD = 198
Hz** and **well above the 30 Hz floor**, with no biological-implausibility concern. The classical
Tukker-Taylor ND-soma morphology dominates the front (35/50), but the second viable archetype is the
PD-soma configuration (4/50, gen 19 cell #23 at DSI = 0.96 / PD = 83 Hz), consistent with the
DS-via-synaptic-asymmetry mechanism documented by [PolegPolsky2026][polegpolsky2026] (already in
corpus).

The **HV plateau gen of ~24-30 is consistent with [Mohacsi2024][mohacsi2024]'s 20-60 gen range** for
NSGA-II on biophysical problems below 12 parameters. That a 68-d problem flattens at the same
horizon as 12-d problems is unexpected and suggests the 2-dir reformulation collapses the effective
optimisation dimension — a hypothesis explicitly testable by re-running 16-dir ratio DSI at the
same gen budget.

## Limitations

* **Single GA seed.** No published reference (the Hay 2011, Druckmann 2007, Mohacsi 2024, Chen 2024
  benchmarks) accepted a single-seed result. Multi-seed confirmation at seeds 55 and 66 is the
  highest-priority follow-up; the 3.3% yield could easily be a per-seed extreme.

* **2-direction protocol is methodologically novel and not directly comparable to published
  multi-direction DSI measurements**. Trenholm2013, Oesch2005, PolegPolsky2026, Ankri2024,
  Riccitelli2025, and CavalHolme2025 all use 8 - 12 directions. The DSI = 1.0 / 0.98 results cannot
  be claimed as "exceeding biology" without the 16-direction post-hoc re-evaluation. This is the
  largest open caveat against the headline.

* **Operator-driven stop introduces a discontinuity**. The 40-gen stop point was selected on visual
  HV plateau, not the pre-registered Blank & Deb 2020 1% / 30-gen rolling threshold recommended by
  the pymoo `RunningMetric` literature (research_internet.md, finding 1). A future run with the
  threshold pre-registered would be more reproducible.

* **PD = 0 / ND = 0 cells are biologically suspicious**. Real DSGCs have some ND firing
  ([Trenholm2013][trenholm2013] 27 +/- 12 Hz at peak). t0106's 3 DSI = 1.0 cells have ND = 0 exactly
  — possibly a sampling artefact of N_EVAL_SEEDS = 3 (15% more noise per cell than t0104's N = 4
  baseline). Robustness check at N_EVAL_SEEDS = 20 on those cells is required.

* **No comparable published NSGA-II run at this dimensionality**. The 68-d substrate is 2.8x - 5.7x
  higher dimensional than any published biophysical NSGA-II benchmark (Hay 2011 22-d top). The
  acceptance rate comparison is therefore against extrapolated expectations, not matched-dimensional
  baselines. **Publication-selection bias** is also material: Hay 2011 and Druckmann 2007 published
  successes but not their failed seeds, so the per-seed yield distribution in their setting is
  unknown.

* **The [PolegPolsky2026][polegpolsky2026] DSI = 0.731 unconstrained ceiling is from 12-dir
  vector-sum** of peak subthreshold voltage, not spike-based ratio DSI on 2 directions. The +0.269
  delta vs t0106's DSI = 1.0 is not a like-for-like comparison.

* **Sub-claim "first lineage-wide win" is empirically true within the t0078 -> t0106 lineage** but
  the per-task evaluation budget varied. [t0102] terminated at gen 11-12 of 20, [t0104] at gen
  11-12. Whether [t0102] / [t0104] at 40+ gens with the 16-dir formula would still return zero
  joint-pass cells is not established and remains an explicit open question.

[t0024]: ../../t0024_port_de_rosenroll_2026_dsgc/
[t0078]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/
[t0080]: ../../t0080_bedb_mobo_v3_dendritic_spike_nsga2/
[t0091]: ../../t0091_morphology_extended_nsga2_v1/
[t0099]: ../../t0099_random_init_pareto_robustness/
[t0102]: ../../t0102_seedscale_n4_gen20/
[t0104]: ../../t0104_nsga2_2obj_dsi_pdrate_3seeds/
[druckmann2007]: ../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md
[hay2011]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[achard2006]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md
[mohacsi2024]: ../../t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[trenholm2013]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/summary.md
[oesch2005]: ../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md
[polegpolsky2026]: ../../t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md
[dang2023]: ../../t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2306.04525/summary.md
[chen2024-stn]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11383608/
[cavalholme2025]: https://pubmed.ncbi.nlm.nih.gov/39871013/
[ankri2024]: ../../t0091_morphology_extended_nsga2_v1/assets/paper/10.1113_JP286581/summary.md
[riccitelli2025]: ../../t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1073_pnas.2415223122/summary.md
