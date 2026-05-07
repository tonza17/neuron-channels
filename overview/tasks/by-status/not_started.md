# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0091 — <strong>First joint 68-d NSGA-II with morphology in eval loop,
5-anchor warm-start</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0091_morphology_extended_nsga2_v1` |
| **Status** | not_started |
| **Effective date** | 2026-05-07 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Expected assets** | 1 answer, 1 predictions |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [First joint 68-d NSGA-II with morphology in eval loop, 5-anchor warm-start](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Task folder** | [`t0091_morphology_extended_nsga2_v1/`](../../../tasks/t0091_morphology_extended_nsga2_v1/) |

# First joint 68-d NSGA-II with morphology generation inside the evaluation loop

## Motivation

Brainstorm session 18 (t0089) commissioned a strategic pivot from electrophys-only
optimisation (t0080-t0088) to morphology-extended optimisation. t0090 delivers the procedural
DSGC morphology generator (14 morphology knobs) plus a validated diversity test plus a Bed-B
reproducibility check. This task t0091 is the first NSGA-II run that calls the generator
inside the evaluation loop, jointly optimising morphology + electrophys in a 68-d parameter
space.

The strategic question is whether enabling morphology in the optimisation opens
biologically-plausible joint-pass regions that t0080-t0088's fixed-Bed-B substrate could not
reach. t0086 + t0088 established that all v3 substrate joint-pass / near-joint-pass cells are
NaP-dominant in their PD-vs-ND mechanism and exotic by the biological scorecard (NMDA
per-synapse +85 to +116 sigma above Sivyer 2013, distal NaP +9 to +34 sigma above Stuart 1999,
GABA spatial-gradient violations). If morphology variation can shift cells toward biologically
plausible NMDA / NaP regimes while maintaining joint-pass DSI / firing rate, the project's
direction-selectivity story has a second mechanism (morphological asymmetry) on top of the
channel mechanism. If morphology pegs at near-Bed-B defaults across the entire Pareto, the v3
substrate's biological-plausibility ceiling is not raised by morphology and we revisit with a
real-cell library (Option G from the brainstorm) in a future task.

A secondary question concerns the asymmetry direction: if PD-asymmetric anchor cells are
preserved more than their ND-asymmetric mirrors in the final Pareto, that is strong evidence
for soma-displacement-toward-PD as a functional DS mechanism (Schachter 2010, Trenholm 2013,
Briggman 2011).

## Scope

### In Scope

* 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) using the t0090 procedural generator
* Pop 96, up to 8 generations, adaptive HV-plateau stop, cost watchdog
* 5-anchor warm-start population (Bed-B-like + symmetric + PD-asymmetric + ND-asymmetric +
  alternative-topology), each anchor cloned with ~19 t0083 Pareto electrophys variants
* Pareto-front analysis: comparison to t0083's 54-d front; biological-plausibility scoring per
  t0086 / t0088 framework extended to 68-d cells
* Anchor-tracking analysis: which of the 5 anchors are over- vs under-represented in the final
  Pareto?
* One answer asset on biological plausibility under morphology variation
* One predictions asset (the 68-d Pareto-front cells, with per-cell DSI / PD / robustness /
  morphology vector / electrophys vector)

### Out of Scope

* Topology-changing perturbations beyond t0090's 14 generator knobs
* Real-cell morphology library (deferred to a future task if t0091 negative result motivates)
* NSGA-II at >68-d (e.g., 80-d with extra channels)

## Approach

### Phase A — Build the 5-anchor warm-start population

Pop 96 = 5 anchors x ~19 t0083 Pareto electrophys variants per anchor + 1 random sample.

Anchors:

| Anchor | Description | Source |
| --- | --- | --- |
| 1 | Bed-B-like (matches existing t0083 substrate; the "do not regress from t0083 baseline" anchor) | t0090 Phase F validated point |
| 2 | Symmetric: `soma_offset_pd_um=0`, `field_elongation_pd=1.0`, `branch_density_gradient_pd=0`, `primary_branch_pd_concentration=0` | Tests whether DS can emerge purely from channel/synapse mechanism without morphological asymmetry |
| 3 | PD-asymmetric: soma offset +100 um toward PD, field elongated 2x along PD, branches biased toward PD | Tests whether morphological asymmetry along PD opens biologically-plausible joint-pass |
| 4 | ND-asymmetric: mirror of #3, soma offset -100 um | Mirror sanity check; if optimiser preserves #3 and discards #4, that is strong evidence for soma-displacement-toward-PD as a functional DS mechanism |
| 5 | Alternative topology: more primary branches (`num_primary_branches=6-7`), deeper Strahler depth, smaller field | Diversifies topology axis specifically |

For each anchor:
* Sample ~19 different electrophys vectors from t0083's gen-17 Pareto archive (using the t0086
  classification: prefer Genuine + Marginal cells over Stochastic ones).
* Combine each electrophys vector with the anchor's morphology vector to produce a complete
  68-d warm-start cell.

Total: 95 warm-start cells from 5 anchors x 19 + 1 random sample = pop 96.

**Time**: ~1-2 hours local. **Cost**: $0.

### Phase B — Joint NSGA-II run

68-d NSGA-II using `pymoo` with NSGA-II algorithm, mixed integer-real handling for the
`num_primary_branches` and `max_strahler_depth` integer parameters.

Settings:
* Population size: 96
* Generations: up to 8 (adaptive HV-plateau stop fires earlier if HV growth < 1 percent for 2
  consecutive gens)
* Crossover: SBX with eta = 15
* Mutation: polynomial mutation with eta = 20, prob = 1 / 68
* Cost watchdog: $4.00 hard cap (well below remaining $4.44 buffer)
* Per-cell evaluation: t0090 generator builds NEURON model from 14 morph params; 54 channel /
  synapse params inserted into generated sections; 5 evaluation seeds for inner replication;
  bar-rotation simulation at 16 directions; objectives = (DSI vector-sum, PD firing rate,
  robustness across seeds).

**Hardware**: Vast.ai EPYC 7B13 64-core. 96 cells x 5 seeds x 16 directions x ~60 s/sim / 64
parallel = ~12 minutes per generation. 8 generations: ~1.6 hours / generation x 8 = ~12.8
hours. With overhead: ~14-16 hours wall-clock.

**Cost estimate**: 14-16 hours x $0.40/hr = ~$5.60-6.40. Optimise: drop pop 96 to pop 80 if
cost overshoot looks likely (~80 cells x 8 gens = ~13.3 hours x $0.40 = ~$5.32; still tight).
Fall back: 6 generations (cost watchdog stops at gen 6), ~9-10 hours = ~$3.60-4.00.
**Realistic budget: $3.00-3.50 with adaptive stop or 6-gen cap.**

### Phase C — Pareto-front + biological-plausibility analysis

* Extract 68-d Pareto front from final population.
* Run t0086's `biological_priors.py` + `biological_scorecard.py` on every Pareto cell
  (corrected-units NMDA score from t0090 Phase G.2 validation).
* Compare biological-plausibility distribution to t0083's 54-d Pareto:
  * Do morph-extended cells reach lower NMDA / NaP / GABA exotic-ness while maintaining
    joint-pass DSI / PD / robustness?
  * Do any cells score "plausible" or "stretched" on all 9 priors simultaneously?

### Phase D — Anchor-tracking analysis

For each Pareto cell, compute its 14-d morphology vector's nearest anchor (Euclidean distance
in normalised morph-param space). Tabulate Pareto-cell counts per anchor:

| Anchor | Warm-start contribution (cells) | Final Pareto representation (cells) |
| --- | --- | --- |
| 1 (Bed-B-like) | 19 | ? |
| 2 (Symmetric) | 19 | ? |
| 3 (PD-asymmetric) | 19 | ? |
| 4 (ND-asymmetric) | 19 | ? |
| 5 (Alt-topology) | 19 | ? |

If anchor 3 (PD-asymmetric) is over-represented and anchor 4 (ND-asymmetric) is
under-represented, that is strong evidence for soma-displacement-toward-PD as a functional DS
mechanism. Compute statistical significance via bootstrap.

### Phase E — Answer asset

One answer asset at `assets/answer/morphology-extension-biological-plausibility/`
synthesising:

* Did morphology extension open biologically-plausible joint-pass regions?
* Which of the 5 anchors did the optimiser preserve in the final Pareto?
* Specifically: PD-asymmetric vs ND-asymmetric — is the optimiser-preferred asymmetry
  direction consistent with the published DS mechanism?
* What is the biological-plausibility ceiling of the morphology-extended substrate?
* What follow-ups does this open?

## Pass Criteria

* Phase B converges (HV plateau or 8-gen cap reached) within budget; no NaN propagation; cost
  watchdog not triggered.
* Phase C produces a 68-d Pareto front with at least 8 cells (matching t0083 minimum-Pareto
  threshold).
* Phase D produces a definitive anchor-tracking table with bootstrap-significance p-values.
* Phase E lands a definitive yes / no on whether morphology extension reaches biologically
  plausible cells, with quantitative thresholds.

**Acceptable negative**: optimiser pegs all anchors back toward Bed-B-like (anchor 1 dominates
final Pareto >80 percent) — conclusion is the v3 substrate's biological-plausibility ceiling
is not raised by morphology variation in this parametrisation. Follow-up: Option G real-cell
library in a future task.

## Compute and Budget

* **Vast.ai EPYC 7B13 64-core** for Phase B NSGA-II
* **Local 64-core CPU** for Phases A, C, D, E

**Estimated cost**: $3.00-3.50 (Phase B with adaptive HV-plateau stop or 6-gen cap). Buffer
remaining after t0091: ~$0.94-1.44.

**Cost watchdog**: hard cap at $4.00 (lockout terminates the NSGA-II if cumulative remote
spend exceeds threshold).

## Time Estimation

* Phase A (warm-start): 1-2 h local
* Phase B (NSGA-II): 14-16 h Vast.ai
* Phase C (Pareto analysis): 2-3 h local
* Phase D (anchor-tracking): 2 h local
* Phase E (answer asset): 1 h local

**Total wall-clock**: ~20-24 hours (mostly Phase B remote).

## Expected Assets

* **Answer asset**: morphology-extension biological plausibility synthesis
  (`expected_assets["answer"] = 1`)
* **Predictions asset**: 68-d Pareto-front cells with per-cell DSI / PD / robustness /
  morphology vector / electrophys vector (`expected_assets["predictions"] = 1`)

## Risks and Fallbacks

* **NSGA-II fails to converge in 8 gens**: 68-d is 25 percent more than 54-d; warm-start gives
  strong prior. If HV is still growing at 8 gens, document it and propose extension as a
  future task (only if budget allows).
* **Cost overshoot**: cost watchdog at $4.00 hard cap; drop to 6 gens if approaching.
* **Generator instability under NSGA-II mutation**: if mutated morph_params produce degenerate
  morphologies, the eval function returns a penalty objective; t0090 Phase D verification
  should have caught most degenerate parameter combinations.
* **Anchor 4 ND-asymmetric cells fail to reproduce on the optimiser's seed**: indicates the
  warm-start anchor is unstable; replace with a symmetric anchor variant.
* **All anchors converge to anchor 1 (Bed-B-like)**: acceptable negative; useful finding;
  motivates Option G real-cell library follow-up.

## Verification Criteria

* `verify_research_code.py`, `verify_plan.py`, `verify_logs.py`, `verify_assets.py`,
  `verify_task_file.py` pass with 0 errors.
* `verify_costs.py` passes (cost record present, within budget).
* The answer asset passes `verify_answer.py`.
* The predictions asset passes `verify_predictions.py`.

## Cross-References

* **t0089_brainstorm_results_18** — commissioning brainstorm session.
* **t0090_morphology_generator_diversity_test** — generator dependency.
* **t0083_bedb_v3_extend_nsga2_gen8plus** — warm-start electrophys archive source.
* **t0086_robustness_cluster_bio_comparison**, **t0088_recluster_marginals_and_vm_motifs** —
  biological-plausibility framework.
* Source suggestions: none directly (new direction). Indirect inheritance from S-0086-01
  (NSGA-II re-run with tightened bounds, kept high for post-t0091 follow-up).

</details>

<details>
<summary>⏹ 0075 — <strong>Biologically-realistic AIS one-axis-at-a-time parameter
sweep on Bed A</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0075_bio_realistic_ais_param_sweep` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0069-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Biologically-realistic AIS one-axis-at-a-time parameter sweep on Bed A](../../../overview/tasks/task_pages/t0075_bio_realistic_ais_param_sweep.md) |
| **Task folder** | [`t0075_bio_realistic_ais_param_sweep/`](../../../tasks/t0075_bio_realistic_ais_param_sweep/) |

# Biologically-Realistic AIS Parameter Sweep on Bed A

## Motivation

t0069 attached a virtual AIS plus 1 mm axon stub to Bed A (deposited Poleg-Polsky DSGC) and
re-ran the t0067 channel-addition sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} on the AIS
instead of the soma. The sweep falsified S-0067-03's prediction (AIS-localised channels show
*larger* DSI effects than soma-localised) — it actually showed the opposite, with 11 of 15
channel conditions producing zero detectable DSI change. The cause was identified clearly: the
AIS+axon halved baseline PD firing (14.2 → 6.4 spikes) and silenced ND firing (1.6 → 0.0),
pushing baseline DSI to the trivial computational ceiling 1.0. The passive AIS+axon adds an
electrical sink that quenches the cell rather than relocating spike initiation; AIS-localised
channels at our densities cannot overcome the somatic 400 mS/cm² HHst Na drive.

The follow-up question this task answers: is there *any* DSGC + AIS configuration that
simultaneously contains all the channels biologically present in a vertebrate AIS (HHst basal
Na+K, Nav1.6, Kv3, Kv7 — the canonical RGC AIS quartet) and produces non-trivial DSI at a
biologically reasonable peak rate? "Decent DSI, not 1, and reasonable firing rate" maps to the
operational pass band {DSI in [0.3, 0.95], peak Hz in [5, 50]}. The right tool is not
optimisation — it is one axis at a time. NaP is excluded from the AIS channel set on two
grounds: (a) AIS NaP expression in RGCs is controversial; (b) the t0067 NaP-high finding (DSI
sign flip) suggests NaP destabilises the DSI mechanism rather than supporting it. BK and SK
are excluded because they localise primarily to soma and dendrites in RGCs, not to the AIS.

This task addresses RQ1 (somatic + AIS VGC combinations) and RQ4 (active vs passive
components). Source suggestions covered: S-0068-04 (move Nav1.6 + Kv3 to AIS), S-0069-01
(halve somatic gnabar before AIS), S-0069-02 (shrink AIS diameter to 0.5 micrometre),
S-0069-03 (vary axon length to probe sink), S-0069-04 (Nav1.6 + Kv3 on AIS at biological
densities).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC) plus virtual AIS + axon stub.
* AIS channel set: **{HHst basal Na + K, Nav1.6, Kv3, Kv7}**. NaP, BK, SK explicitly excluded.
* Encoding: 12-angle bar-rotation protocol (same as t0074 — cross-task comparable).
* Two-stage design: Stage 1 baseline calibration; Stage 2 per-axis sweep.

### Stage 1 — Baseline calibration

* Literature-informed AIS configuration (Wang et al. 2011, Carter et al. 2008 on mouse RGC
  AIS): AIS diameter 0.8 micrometre, AIS length 30 micrometre, axon stub 1.0 mm, AIS
  gnabar_HHst 4 0 0 mS/cm^2, AIS Nav1.6 medium density (~0.3 S/cm^2 from t0067 medium), AIS
  Kv3 medium density (~0.3 S/cm^2), AIS Kv7 low density (~0.1 S/cm^2; distal AIS, weaker than
  Nav and Kv3).
* Sweep soma `gnabar_HHst` across 6 candidates: {100, 150, 200, 250, 300, 400} mS/cm^2 (the
  t0069 baseline = 400).
* 6 candidates x 12 angles x 1 seed = 72 trials, ~5 min wall-clock.
* Pick the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]}. If multiple
  candidates qualify, pick the one closest to the centre of the band ({peak ~ 20 Hz, DSI ~
  0.6}).
* If no candidate qualifies, the task halts at Stage 1 and reports a negative result with a
  recommendation for a follow-up that loosens the AIS configuration further (e.g., reduce AIS
  Nav1.6 density first, then re-attempt).

### Stage 2 — Per-axis sweep

From the Stage-1 baseline, vary one parameter at a time with all others held at baseline:

| # | Axis | Values | Non-baseline points |
| --- | --- | --- | --- |
| 1 | Soma `gnabar_HHst` (mS / cm^2) | {100, 200, 300, 400} | 3 |
| 2 | AIS `gnabar_HHst` (mS / cm^2) | {0, 100, 200, 400, 800} | 4 |
| 3 | AIS diameter (micrometre) | {0.4, 0.6, 0.8, 1.0, 1.5} | 4 |
| 4 | AIS length (micrometre) | {15, 30, 45, 60} | 3 |
| 5 | AIS Nav1.6 density | {0, low, medium, high} | 3 |
| 6 | AIS Kv3 density | {0, low, medium, high} | 3 |
| 7 | AIS Kv7 density | {0, low, medium, high} | 3 |
| 8 | Axon length (mm) | {0.1, 0.5, 1.0, 2.0} | 3 |

Total Stage-2 conditions: 1 baseline + 26 non-baseline = **27 conditions x 12 angles x 5 seeds
= 1620 FULL trials**, ~100 min wall-clock at the t0067 measured ~3.75 s / trial under CVODE.

### Width metrics per axis (cross-comparable with t0074)

For each condition, compute:

* **HWHM** in degrees from the 12-angle tuning curve.
* **Vector-sum DSI** (circular concentration).
* **Peak rate (Hz)** at the angle with maximum mean rate.
* Rate at PD (axis-1 peak angle) and at the opposite angle.
* RMSE vs the t0004 cosine target.

### Outputs

* **Library asset**: `bed_a_with_bio_realistic_ais` — Bed A + AIS + axon model variant with
  the {HHst, Nav1.6, Kv3, Kv7} channel set wired in. Reusable by future tasks that need a
  working DSGC + AIS substrate.
* **Stage 1 candidate table** (`results/baseline_candidates.csv`) with 6 rows showing
  soma_gnabar_HHst, peak Hz, DSI, in-band y/n.
* **Stage 2 per-axis sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI,
  peak rate, RMSE vs cosine target, plotted against axis values.
* **Biologically-plausible AIS recommendation table**
  (`results/biological_ais_recommendation.md`): the band-constrained range for each axis (the
  values that keep the cell inside {DSI [0.3, 0.95], peak [5, 50] Hz}), plus a recommended
  canonical configuration.
* `results/metrics.json` with registered project metrics per condition.

## Approach

1. Fork t0069's AIS-attachment code into this task's `code/`. Replace the t0069
   channel-addition loop with the {HHst, Nav1.6, Kv3, Kv7} baseline channel set (with
   t0074-vendored Kv7).
2. Implement Stage 1 calibration as a 6-candidate sweep with explicit pass-band check and
   automated baseline selection.
3. Implement Stage 2 as 8 per-axis sweep functions sharing a common driver.
4. Run Stage 1, log selected baseline, run Stage 2.
5. Compute width metrics, generate per-axis plots, write the recommendation table.
6. Validate against t0069 sanity checks: trials with instability flags = 0, peak Vm bounded.

## Pass Criteria

* Stage 1 finds at least one in-band baseline (peak Hz in [5, 50] AND DSI in [0.3, 0.95]).
* All 1620 + 72 trials complete with no instability flags.
* Per-axis sensitivity plots show monotonic or unimodal sensitivity for at least 6 of the 8
  axes (the axes that don't are flagged as candidates for re-investigation; not a hard fail).
* Recommendation table produced with the band-constrained range for each axis.

## Compute Estimate

* ~2 h wall-clock on local CPU. 72 trials Stage 1 (~5 min) + 1620 trials Stage 2 (~100 min) +
  ~10 min plotting / metrics extraction.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code (Nav1.6, Kv3
  implementation patterns).
* `t0069_t0067_ais_localised_channel_sweep` — AIS attachment code; baseline characterisation
  of the passive-AIS sink effect.
* `t0074_channel_tuning_width_bed_a` — Kv7 MOD vendoring lands in t0074. This task inherits
  the vendored Kv7 mechanism and the calcium-pool unification (the latter is not actively used
  here but must remain compatible).

## Risks and Fallbacks

* **Stage 1 finds no in-band baseline**: the task halts after Stage 1 and reports a negative
  result with a follow-up recommendation. Time-cheap (~5 min). The follow-up would probably be
  a 2D Stage 1.5 sweep over {soma gnabar, AIS gnabar} or a baseline that further reduces AIS
  Nav1.6 density.
* **Stage 1 is over-fitted to soma_gnabar**: if the baseline soma_gnabar value is borderline
  (e.g., exactly at the edge of the in-band region), small parameter changes in Stage 2 may
  push the cell out of band rapidly. Mitigation: pick the Stage-1 baseline closest to the band
  centre, not the band edge.
* **Axes interact strongly**: the one-axis-at-a-time design assumes weak interactions. If a
  Stage-2 axis sweep produces non-monotonic behaviour (e.g., DSI rises then falls), report the
  non-monotonicity explicitly and flag the axis for a future joint sweep with one neighbouring
  axis.
* **AIS+axon discretisation artefacts**: if the segment count along the AIS or axon is too
  low, spike initiation and propagation may be artefactual. Mitigation: use NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) and validate that the
  chosen segment count doubles without changing peak Vm by more than 1 mV at the t0069
  baseline.

## Out of Scope

* Bed B (de Rosenroll) — explicitly out of scope per researcher decision; this task is Bed A
  only.
* Joint multi-axis optimisation — explicitly excluded; this is one-axis-at-a-time only.
* Other AIS channel candidates (Nav1.2, Kv1, Kv4 alpha-DTX-sensitive subtype) — out of scope;
  the channel set is fixed at {HHst, Nav1.6, Kv3, Kv7}. Future follow-ups may extend the
  channel set.

</details>

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
