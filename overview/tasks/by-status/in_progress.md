# ⏳ Tasks: In Progress

2 tasks. ⏳ **2 in_progress**.

[Back to all tasks](../README.md)

---

## ⏳ In Progress

<details>
<summary>⏳ 0091 — <strong>First joint 68-d NSGA-II with morphology in eval loop,
5-anchor warm-start</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0091_morphology_extended_nsga2_v1` |
| **Status** | in_progress |
| **Effective date** | 2026-05-08 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Expected assets** | 1 answer, 1 predictions |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-08T11:35:57Z |
| **Task page** | [First joint 68-d NSGA-II with morphology in eval loop, 5-anchor warm-start](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Task folder** | [`t0091_morphology_extended_nsga2_v1/`](../../../tasks/t0091_morphology_extended_nsga2_v1/) |

# First joint 68-d NSGA-II with morphology generation inside the evaluation loop

## Motivation

Brainstorm session 18 (t0089) commissioned a strategic pivot from electrophys-only
optimisation (t0080-t0088) to morphology-extended optimisation. t0090 delivered the procedural
DSGC morphology generator (14 morphology knobs) but committed a soma-`pt3dadd` collapse bug;
t0092 diagnosed the root cause and shipped `generate_fixed_morphology` as a thin shim; t0093
ran the full 60-cell re-sweep under the patched generator (60/60 STABLE-firing, 56/60 with
PD-rate>0, 0 regressions) and issued correction `C-0093-01` (`replace`) redirecting the
canonical procedural generator to t0092's fix. **t0091 imports the t0092 patched generator,
not t0090's unpatched one.** This task is the first NSGA-II run that calls the patched
generator inside the evaluation loop, jointly optimising morphology + electrophys in a 68-d
parameter space.

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

* 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) using the t0092 patched procedural
  generator (`generate_fixed_morphology`, canonicalised by C-0093-01)
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
| 1 | Bed-B-like (matches existing t0083 substrate; the "do not regress from t0083 baseline" anchor) | t0093 patched-generator Bed-B reproducibility (43.6 Hz PD-rate post-fix on the BedB-equivalent point) |
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
* Per-cell evaluation: `from
  tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import
  generate_fixed_morphology` builds the NEURON model from 14 morph params (the soma-pt3d
  collapse bug is fixed at the source); 54 channel / synapse params inserted into generated
  sections; 5 evaluation seeds for inner replication; bar-rotation simulation at 16
  directions; objectives = (DSI vector-sum, PD firing rate, robustness across seeds).

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
  morphologies, the eval function returns a penalty objective. t0093's patched-generator
  re-sweep showed 60/60 STABLE under the t0083 channel set across the wide LHS sample, so the
  patched generator covers the morphology parameter space without NaN_VOLTAGE failures.
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
* **t0090_morphology_generator_diversity_test** — original generator dependency (superseded by
  t0092 / t0093 fix).
* **t0092_diagnose_morphology_generator_silence** — patched generator
  (`generate_fixed_morphology`); canonical entry point for morphology construction.
* **t0093_resweep_and_t0090_correction** — full 60-cell verification of the patched generator
  (60/60 STABLE-firing) and `replace` correction overlay `C-0093-01` redirecting the canonical
  procedural DSGC morphology generator to t0092's fix.
* **t0094_brainstorm_results_19** — brainstorm session that updated this task's dependencies
  and import paths to reference t0092 / t0093 (covers S-0093-01).
* **t0083_bedb_v3_extend_nsga2_gen8plus** — warm-start electrophys archive source.
* **t0086_robustness_cluster_bio_comparison**, **t0088_recluster_marginals_and_vm_motifs** —
  biological-plausibility framework.
* Source suggestions: none directly (new direction). Indirect inheritance from S-0086-01
  (NSGA-II re-run with tightened bounds, kept high for post-t0091 follow-up).

</details>

<details>
<summary>⏳ 0097 — <strong>Literature survey: multi-objective optimisation of
single-neuron models</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0097_multi_obj_optim` |
| **Status** | in_progress |
| **Effective date** | — |
| **Dependencies** | — |
| **Expected assets** | 10 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`internet-research`](../../../meta/task_types/internet-research/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [Literature survey: multi-objective optimisation of single-neuron models](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Task folder** | [`t0097_multi_obj_optim/`](../../../tasks/t0097_multi_obj_optim/) |

# Literature Survey: Multi-Objective Optimisation of Single-Neuron Compartmental Models

> **Note**: This task supersedes `t0096_literature_survey_multi_objective_neuron_optimisation`,
> which was created with a slug too long for Windows worktree paths to handle (the absolute path
> exceeded Windows' 260-char limit when combined with deep existing task paths). The content here is
> identical; only the task ID and slug are shorter.

## Motivation

The morphology + channel optimisation pipeline is now production-ready: t0091
(`morphology_extended_nsga2_v1`) is currently running the first joint 68-d NSGA-II (54-d
electrophys \+ 14-d morphology) on the t0092-patched procedural generator validated at scale
by t0093. Every multi-objective optimisation task this project has run so far (t0076, t0078,
t0080, t0081, t0083, t0086, t0091) has used the same two objectives: direction selectivity
index (DSI) and firing rate. That objective pair was the right choice for the project's
first-question ("which channels maximise DS?") phase, but it leaves the broader
multi-objective landscape unexplored.

The researcher's strategic directive (brainstorm session 20, 2026-05-08) is to broaden the
optimisation objective space:

> Now that we have working optimisation for both morphology and channel composition we can optimise
> for different things. Currently we optimise for DSI and firing rate. However I would like to
> compare results for all sorts of stuff. For example, I would like to optimise for DSI and
> information transfer rate; DSI and energy spent, DSI and minimisation of citoplasm volume etc.
> Perform an extensive literature search and find papers that use different forms of optimisation.
> It does not need to be DSGC but can be any neurons.

This task is the literature-research foundation for that broadening. It catalogues every
objective function used in the published multi-objective single-neuron optimisation
literature, delivers formulas + computational recipes for each, and produces a ranked list of
future MOBO tasks to commission once budget permits. The deliverable is intentionally
actionable: each catalogued objective must be implementable on top of the existing Bed B
NSGA-II loop without infrastructure rewrites.

The task is also the right test of biological plausibility as an optimisation criterion. The
researcher's recurring concern across this project has been that pure DSI maximisation admits
non-physical solutions; jointly optimising DSI vs energy, vs cytoplasm volume, or vs
robustness forces the optimiser into bio-realistic regions of the parameter space. The survey
should explicitly document, per objective, whether published work treats it as a biological
constraint or only as a performance proxy.

## Scope

### In Scope

* **Multi-objective methodology papers** covering single-neuron compartmental models:
  Druckmann et al. 2007 ("A novel multiple objective optimization framework for constraining
  conductance-based neuron models by experimental data"), Druckmann et al. 2011 (eFEL
  precursor), Achard & De Schutter 2006 (first MOEA Purkinje fits), Van Geit et al.
  (NeuroFitter / BluePyOpt), Rumbell et al. (cortical L5 PC MOBO), Hay et al. 2011 (BBP
  cortical L5 multi-objective).
* **Information-theoretic objective functions**: mutual information between stimulus and spike
  train (Bialek, De Ruyter van Steveninck, Strong et al.), Fisher information / discrimination
  capacity (Brunel, Nadal), channel capacity, stimulus-reconstruction MSE, spike-train metrics
  (Victor & Purpura, van Rossum).
* **Metabolic / energy objective functions**: ATP per spike, total ionic flux, Na+/K+ pump
  cost (Attwell & Laughlin 2001 "An energy budget for signaling in the grey matter of the
  brain"), bits-per-ATP energy efficiency (Niven & Laughlin 2008, Sengupta et al. 2010 "Action
  potential energy efficiency varies among neuron types in vertebrates and invertebrates").
* **Structural / wiring objective functions**: total dendritic length, total membrane area,
  cytoplasm / dendritic volume, wiring economy (Chklovskii et al., Cuntz, Forstner, Borst &
  Hausser 2010 "One rule to grow them all").
* **Robustness / degeneracy objective functions**: parameter-perturbation sensitivity, noise
  tolerance (Marder & Goaillard 2006 "Variability, compensation and homeostasis in neuron and
  network function"; Prinz, Bucher & Marder 2004 "Similar network activity from disparate
  circuit parameters").
* **Temporal / coding objective functions**: latency, jitter, spike-timing precision,
  bandwidth, dynamic range.
* **Methods / codebases**: BluePyOpt (Van Geit), NeuroFitter, NSGA-II + NSGA-III in pymoo,
  MOEA literature (Deb et al.), Pareto-front analysis methods (hypervolume, IGD, R2
  indicator).

### Out of Scope

* Network-level optimisation (multi-neuron). Stay on single-neuron compartmental models.
* Reinforcement-learning / deep-learning policy optimisation. Stay on classical MOBO / MOEA.
* Phenomenological integrate-and-fire models without compartmental structure (mention briefly
  if they yield reusable objectives, but do not deep-dive).

## Must-Find Objective Categories

The survey must deliver formula + units + NEURON-side computational recipe for at least one
representative objective in each of these four categories:

1. **Information transfer rate / mutual information** — between stimulus angle and spike-train
   output for our DSGC case. Concrete recipe must specify how to estimate MI from a
   t0091-style 8-direction trial output (e.g., binned spike counts per direction, direct
   method, or extrapolation method).

2. **Metabolic energy / ATP per spike** — computable from HH ionic currents in NEURON.
   Concrete recipe must specify which currents to integrate (Na+ influx, K+ efflux, leak) and
   the conversion factor from charge to ATP molecules (3 Na+ exchanged per ATP via Na+/K+
   ATPase).

3. **Cytoplasm volume / wiring cost** — computable directly from morphology. Concrete recipe:
   sum over compartments of pi * r^2 * L; or total surface area as an alternative; or wiring
   cost = sum of section lengths weighted by diameter.

4. **Robustness / degeneracy** — parameter-perturbation sensitivity of DSI; multi-conductance
   solution-space volume. Concrete recipe must specify a Marder-style protocol: e.g., +/- 10
   percent random perturbation of all channel densities and report DSI standard deviation as
   the objective.

If the literature search uncovers more well-defined objective categories not in this list, add
them to the catalogue and rank them by biological plausibility and computational feasibility.

## Approach

### Stage 1: Research Papers

Survey methodology and biological objective-function origin papers. Download canonical
citations for each objective category. Read full text where available; abstract +
supplementary info otherwise. Produce `research/research_papers.md` with:

* Per-objective subsection grouping the 2-3 canonical papers
* Per-paper extracted formula, units, computational recipe
* Notes on biological plausibility and how the objective would interact with DSI in a
  multi-objective setting

### Stage 2: Research Internet

Survey codebases, tutorials, review articles, and online resources for multi-objective
single-neuron optimisation. Targets: BluePyOpt (Van Geit, github.com/BlueBrain/BluePyOpt),
NeuroFitter, eFEL, pymoo NSGA-II + NSGA-III tutorials, Pareto-front diagnostic libraries
(pyDOE, paretoset). Document API surfaces and example usage that the project could adopt
without rewrites. Produce `research/research_internet.md`.

### Stage 3: Answer Asset

Synthesise findings into a single answer asset
`objective-functions-for-single-neuron-multi-objective-optimisation` (under `assets/answer/`).
Each catalogued objective gets a uniform record:

| Field | Content |
| --- | --- |
| Name | e.g. `mutual_information_stimulus_spike_train` |
| Mathematical formula | LaTeX |
| Units | e.g. bits per second, ATP per spike, um^3 |
| NEURON-side quantities required | Vm trace, ionic currents, spike times, morphology, etc. |
| Recipe | Step-by-step computation from a t0091-style 8-direction trial output |
| Biological plausibility | Notes on whether the objective is a hard biological constraint or a soft proxy |
| Direction-of-optimisation | Maximise / minimise / target value |
| Papers using it | At least 2 citations |

### Stage 4: Suggestions

Emit a ranked list of future MOBO tasks in `results/suggestions.json`. Each suggestion must
include:

* Title (e.g. "Bed B NSGA-II maximising DSI and ITR")
* Kind, priority
* Categories, source_paper if applicable
* Biological plausibility notes
* Budget feasibility estimate (Vast.ai EPYC + GPU hours)
* Cross-references to the catalogued objective entries

Suggestions must be ranked by combined biological-plausibility and budget-feasibility scores.
Aim for 3-6 ranked suggestions; do not pad.

## Cost Estimation

* **Total**: $0
* **Compute**: none. Local-only.
* **Paid services**: none.
* **Risk-of-going-over**: zero. The task is paper download + reading + writing.

## Step by Step

1. `init-folders`, `check-deps` (no deps to check).
2. Stage 1: research papers — download 10+ canonical papers; read; populate
   `research/research_papers.md`; create paper assets.
3. Stage 2: research internet — survey codebases, tutorials, review articles; populate
   `research/research_internet.md`.
4. Stage 3: answer asset — write the consolidated objective-function catalogue.
5. Stage 4: suggestions — write `results/suggestions.json` with the ranked future-MOBO list.
6. Reporting — write `results/results_summary.md` and `results/results_detailed.md`; run
   verificators; PR; merge.

## Remote Machines

None.

## Assets Needed

None. The task downloads its own paper assets.

## Expected Assets

* `paper`: at least 10 (covering methodology + four must-find categories)
* `answer`: 1 (the consolidated objective-function catalogue)

## Time Estimation

Approximately 2-4 hours wall-clock by an autonomous research agent. Roughly: 60-90 min paper
download + reading; 30-60 min internet survey + codebase review; 30-60 min answer asset
writing; 15-30 min suggestions + reporting + verification.

## Risks & Fallbacks

* **Paywalled paper not accessible** via Sci-Hub or institutional proxy: mark in
  `intervention/` and proceed with abstract + citation analysis. Do not block the task.
* **Cytoplasm volume has no direct precedent** in single-neuron optimisation literature: use
  the wiring-cost / total-length proxy and flag it as a novel objective contribution. The
  computational recipe is already trivial (sum over compartments of pi * r^2 * L) so the
  objective stays usable even without a published precedent.
* **Answer asset becomes too long** (>5000 words): split per category but keep one
  consolidated `short_answer.md` as the entry point. Each category subsection in
  `full_answer.md` may be a separate H2 section.
* **Literature search dilutes** because too many off-target papers come up: enforce the
  Out-of-Scope filter; prefer 2-3 canonical citations per category over comprehensive
  coverage.

## Verification Criteria

* All four must-find objective categories covered with formulas and computational recipes.
* At least 5 multi-objective compartmental-model methodology papers reviewed.
* At least 10 paper assets created and passing the paper asset verificator.
* Answer asset passes `meta/asset_types/answer/specification.md`.
* At least 3 ranked, budget-realistic future MOBO suggestions emitted in
  `results/suggestions.json`.
* All standard task verificators pass: `verify_task_file`, `verify_logs`,
  `verify_research_papers`, `verify_research_internet`, `verify_assets`, `verify_suggestions`,
  `verify_task_results`, `verify_pr_premerge`.

## Cross-References

* **t0096_literature_survey_multi_objective_neuron_optimisation** — superseded predecessor
  (cancelled in this PR due to Windows worktree path-length limit).
* **t0091_morphology_extended_nsga2_v1** — current MOBO frontier (DSI + firing rate);
  catalogue's recipes must compose with t0091's trial-output format.
* **t0095_brainstorm_results_20** — commissioned t0096 (this task's predecessor).
* **t0002_literature_survey_dsgc_compartmental_models** — prior literature survey for
  stylistic consistency.
* **t0015 / t0016 / t0017 / t0018 / t0019 / t0027** — prior literature surveys for stylistic
  consistency and for any cross-cited references.

</details>
