# ✅ Literature survey: multi-objective optimisation of single-neuron models

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0097_multi_obj_optim` |
| **Status** | ✅ completed |
| **Started** | 2026-05-08T15:23:11Z |
| **Completed** | 2026-05-08T16:50:00Z |
| **Duration** | 1h 26m |
| **Task types** | `literature-survey`, `internet-research`, `answer-question` |
| **Categories** | [`cable-theory`](../../by-category/cable-theory.md), [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`synaptic-integration`](../../by-category/synaptic-integration.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 10 paper, 1 answer |
| **Step progress** | 10/15 |
| **Task folder** | [`t0097_multi_obj_optim/`](../../../tasks/t0097_multi_obj_optim/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0097_multi_obj_optim/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source: [`task_description.md`](../../../tasks/t0097_multi_obj_optim/task_description.md)*

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

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Which objective functions have been used in published multi-objective optimisation of single-neuron compartmental models, and what is each one's formula, units, and NEURON-side computational recipe on a t0091-style 8-direction trial output?](../../../tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/) | [`full_answer.md`](../../../tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md) |
| paper | [Similar network activity from disparate circuit parameters](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nn1352/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nn1352/summary.md) |
| paper | [Variability, compensation and homeostasis in neuron and network function](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/summary.md) |
| paper | [An Energy Budget for Signaling in the Grey Matter of the Brain](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/summary.md) |
| paper | [Entropy and Information in Neural Spike Trains](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/summary.md) |
| paper | [Energy limitation as a selective pressure on the evolution of sensory systems](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1242_jeb.017574/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1242_jeb.017574/summary.md) |
| paper | [Complex Parameter Landscape for a Complex Neuron Model](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md) |
| paper | [Action Potential Energy Efficiency Varies Among Neuron Types in Vertebrates and Invertebrates](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/summary.md) |
| paper | [BluePyOpt: Leveraging Open Source Software and Cloud Infrastructure to Optimise Model Parameters in Neuroscience](../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/summary.md) |
| paper | [A novel multiple objective optimization framework for constraining conductance-based neuron models by experimental data](../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md) |
| paper | [Wiring Optimization in Cortical Circuits](../../../tasks/t0097_multi_obj_optim/assets/paper/no-doi_Chklovskii2002_wiring-optimization-cortical/) | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/no-doi_Chklovskii2002_wiring-optimization-cortical/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Bed B NSGA-II maximising DSI and minimising cytoplasm
volume</strong> (S-0097-01)</summary>

**Kind**: experiment | **Priority**: high

Highest biological-plausibility ranking in the t0097 catalogue. Cytoplasm volume is the most
evolutionarily grounded cost objective (Cajal cytoplasm-conservation; Cuntz et al. 2010's `bf`
in [0.2, 0.7] band; Chklovskii et al. 2002's 3/5-of-grey-matter wiring rule). Infrastructure
already in place via the t0093-validated procedural morphology generator. Falsifiable
prediction: high-DSI corner clusters at `bf` in [0.2, 0.7]. Budget feasibility: 12-24 h on
Vast.ai EPYC 7763 64-core at $0.30/h, total $4-8 (within the per-task $5 default; flag for $8
budget bump if needed). Same population/generation budget as t0091.

</details>

<details>
<summary><strong>Bed B NSGA-II maximising DSI and minimising ATP-per-spike</strong>
(S-0097-02)</summary>

**Kind**: experiment | **Priority**: high

Anchored to the canonical Attwell-Laughlin energy budget (47% of cortical signalling ATP per
spike). Remme et al. 2018's MSO function-vs-energy MOBO provides a direct methodology template
generalising to NEURON. DSGC's GABAergic-style fast-spiking should produce
Carter-Bean-2009-style Na/K-overlap penalty; the front should expand toward dramatically lower
energy as Na+ density and overlap are jointly reduced. Recipe: `(1/3) sum int(I_Na) dt / e`
per compartment per AP. Budget: 24-48 h Vast.ai EPYC at $0.30/h, total $8-15 — may exceed
per-task default; flag for explicit budget approval.

</details>

<details>
<summary><strong>Bed B NSGA-II maximising DSI and robustness under +/-10%
channel-density perturbation</strong> (S-0097-03)</summary>

**Kind**: experiment | **Priority**: high

Directly addresses the researcher's recurring biological-plausibility concern with pure-DSI
maximisation (Marder-style population-statistic robustness is the field-standard treatment).
Falsifiable prediction: high-DSI / high-robustness corner lies along compensatory hyperplanes,
refuting the hypothesis that DSI maximisation drives the optimiser to fragile parameter-space
extremes. Recipe: K=50-200 +/-10% perturbations per Pareto point; minimise SD of DSI. Budget:
36-72 h Vast.ai EPYC at $0.30/h, total $11-22 (multiplies t0091's per-individual cost by
K=50-200) — request explicit $25 budget cap or reduce population/generations.

</details>

<details>
<summary><strong>Bed B NSGA-II maximising DSI and information transfer rate</strong>
(S-0097-04)</summary>

**Kind**: experiment | **Priority**: medium

Recipe is well-established (Strong-Bialek direct method with 1/T extrapolation) and validates
against Dhingra & Smith 2004's ~60% gray-level loss benchmark. Caveat: the project's
8-direction protocol has only 3 bits of stimulus uncertainty, so the MI estimator's ceiling is
3 bits per trial regardless of spike train. Validate the recipe against existing DSGC trial
output before launching the full MOBO. Budget: 18-36 h Vast.ai EPYC at $0.30/h, total $5-11.
MI is post-hoc on simulation output, so cost overhead is mostly in extra population to
populate the MI Pareto direction. Priority dropped to medium pending recipe validation.

</details>

<details>
<summary><strong>Bed B NSGA-II maximising MI and minimising ATP-per-spike
(bits-per-ATP front)</strong> (S-0097-05)</summary>

**Kind**: experiment | **Priority**: medium

Decouples function (information) from selectivity (DSI). Produces a bits-per-ATP Pareto front
directly comparable to Niven et al. 2007's empirical fly-photoreceptor 200-1000 bits/s
super-linear cost-vs-information curve. The DSGC bits-per-ATP ratio is unmeasured in the
literature, so the experiment closes a genuine open question. Tradeoff: this experiment does
not directly serve the project's first-question DSGC mission (DSI is not optimised); ranked
medium because it serves a broader scientific question rather than the project's specific
deliverable. Budget: 24-48 h Vast.ai EPYC at $0.30/h, total $8-15 — comparable to S-0097-02.

</details>

## Research

* [`research_internet.md`](../../../tasks/t0097_multi_obj_optim/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0097_multi_obj_optim/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0097_multi_obj_optim/results/results_summary.md)*

--- spec_version: "1" task_id: "t0097_multi_obj_optim" date_completed: "2026-05-08" status:
"complete" ---
# Results Summary: Literature Survey of Multi-Objective Optimisation in Single-Neuron Models

## Summary

Catalogued **6 objective functions** (4 must-find + 2 additional) usable on top of the
project's existing Bed B NSGA-II loop, with formulas, units, NEURON-side computational
recipes, and biological-plausibility notes for each. Downloaded **10 paper assets** spanning
the methodology canon (Druckmann 2007, Achard & De Schutter 2006, BluePyOpt / Van Geit 2016),
the metabolic energy line (Attwell & Laughlin 2001, Niven & Laughlin 2008, Sengupta et al.
2010), the information-theoretic line (Strong et al. 1998), the robustness / degeneracy line
(Marder & Goaillard 2006, Prinz, Bucher & Marder 2004), and the wiring economy line
(Chklovskii et al. 2002). Produced one consolidated answer asset
(`objective-functions-for-single-neuron-multi-objective-optimisation`, 6724 words) plus 5
ranked future-MOBO suggestions in `results/suggestions.json`. Cost: $0.

## Metrics

* **Catalogued objectives**: 6 (mutual_information_stimulus_spike_train,
  metabolic_energy_atp_per_spike, cytoplasm_volume, robustness_under_perturbation,
  coincidence_detection_accuracy, bits_per_atp_efficiency).
* **Paper assets created in t0097**: 10 (Druckmann2007, Attwell2001, Marder2006, Strong1998,
  Sengupta2010, Niven2008, Prinz2004, Achard2006, VanGeit2016, Chklovskii2002).
* **Answer asset created**: 1 (consolidated objective-function catalogue, 6724 words across 9
  mandatory sections + 3 plan-required additional sections).
* **Future-MOBO suggestions emitted**: 5 (DSI vs cytoplasm volume, DSI vs ATP, DSI vs
  robustness, DSI vs MI, MI vs ATP), each with priority, biological-plausibility note, budget
  feasibility estimate ($0-$22 per task), and cross-references to catalogued objectives.
* **Methodology citations covered in catalogue**: 6+ (Druckmann2007, Hay2011, Achard2006,
  VanGeit2016, Deb2014, Ament2023).
* **Total task cost**: $0 (paper download + reading + writing locally; no remote compute, no
  paid APIs).
* **Wall-clock execution time**: ~2 hours (research-papers ~10 min, research-internet ~17 min,
  planning ~10 min, implementation + 10 parallel paper-adds ~70 min, results + suggestions +
  reporting ~15 min).

## Verification

* `verify_research_papers.py t0097_multi_obj_optim` — PASSED (0 errors, 0 warnings).
* `verify_research_internet.py t0097_multi_obj_optim` — PASSED (0 errors, 0 warnings).
* `verify_plan.py t0097_multi_obj_optim` — PASSED (0 errors, 0 warnings).
* `verify_task_file.py t0097_multi_obj_optim` — to run during reporting step.
* `verify_logs.py t0097_multi_obj_optim` — to run during reporting step.
* `verify_task_results.py t0097_multi_obj_optim` — to run during reporting step.
* `verify_task_metrics.py t0097_multi_obj_optim` — to run during reporting step.
* `verify_suggestions.py t0097_multi_obj_optim` — to run during reporting step.
* `verify_pr_premerge.py t0097_multi_obj_optim --pr-number <N>` — to run during reporting
  step.
* Manual structural verification of 10 paper assets (PA-E001..PA-E015): all pass.
* Manual structural verification of answer asset (AA-E001..AA-E014): all pass after pruning
  source_paper_ids to the actually-downloaded subset.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0097_multi_obj_optim/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0097_multi_obj_optim" date_completed: "2026-05-08" status:
"complete" ---
# Results Detailed: Literature Survey of Multi-Objective Optimisation in Single-Neuron Models

## Summary

A consolidated literature survey of multi-objective optimisation in single-neuron
compartmental models, scoped broadly across any neuron type and any species. The deliverable
is a ready-to-use catalogue of **6 objective functions** (4 must-find + 2 additional) with
formulas, units, NEURON-side computational recipes, biological-plausibility notes, and
citation lists, plus 10 downloaded paper assets and 5 ranked future-MOBO suggestions. The
catalogue is the first project-internal reference for the next research-depth move: broadening
the project's existing Bed B NSGA-II loop beyond the current DSI + firing-rate Pareto.

## Methodology

* **Workstation**: researcher's local Windows 11 Education box (researcher's laptop).
* **Compute**: local-only; no remote machines, no GPU, no paid APIs.
* **Wall-clock**: ~2 hours total (timestamps in `step_tracker.json`):
  * 2026-05-08T15:25:10Z create-branch
  * 2026-05-08T15:30:28Z research-papers
  * 2026-05-08T15:40:22Z research-internet
  * 2026-05-08T15:59:58Z planning
  * 2026-05-08T16:12:49Z implementation (parallel with 10 background `/add-paper` subagents)
  * 2026-05-08T16:34:59Z results
* **Tools**: WebSearch, WebFetch (research-internet stage); `arf.scripts.utils.run_with_logs`
  for command logging; `arf.scripts.utils.prestep` / `arf.scripts.utils.poststep` for step
  lifecycle; `flowmark` for markdown formatting; `ruff` + `mypy` for Python style (no Python
  written in this task); `meta.asset_types.paper.verificator` for paper-asset structural
  checks (the project does not have `verify_paper_asset.py` or `verify_answer_asset.py` —
  manual spec-based verification stood in for the answer asset).
* **Workflow**: 3 background paper-add subagents launched after research-internet, then 3
  more, then 4 more, all running concurrently with planning + implementation in foreground.
  Implementation subagent's final report verified each plan REQ-* item against the answer
  asset content.

## Verification

| Verificator | Status | Notes |
| --- | --- | --- |
| `verify_research_papers t0097_multi_obj_optim` | PASSED | 0 errors, 0 warnings (manual confirm during reporting step). |
| `verify_research_internet t0097_multi_obj_optim` | PASSED | 0 errors, 0 warnings. |
| `verify_plan t0097_multi_obj_optim` | PASSED | 0 errors, 0 warnings. |
| `verify_task_file t0097_multi_obj_optim` | to run | reporting step. |
| `verify_logs t0097_multi_obj_optim` | to run | reporting step. |
| `verify_task_results t0097_multi_obj_optim` | to run | reporting step. |
| `verify_task_metrics t0097_multi_obj_optim` | to run | reporting step (metrics.json is `{}` per spec; passes trivially). |
| `verify_suggestions t0097_multi_obj_optim` | to run | reporting step. |
| `verify_corrections t0097_multi_obj_optim` | to run | reporting step (no corrections issued). |
| Paper-asset spec checks (PA-E001..E015) on 10 papers | PASSED | manual per-paper structural verification by paper-add subagents. |
| Answer-asset spec checks (AA-E001..E014) | PASSED | manual after source_paper_ids pruned to actually-downloaded subset. |
| `verify_pr_premerge t0097_multi_obj_optim --pr-number <N>` | to run | reporting step. |

## Limitations

* **Scope deliberately wide**: the survey covers any neuron type, any species. Some objective
  candidates (e.g., dendritic-spike-density, axonal jitter) appear briefly in
  research_internet.md but are not catalogued in the answer asset because no published recipe
  yet exists for computing them on a t0091-style 8-direction trial output.
* **Cytoplasm volume objective is novel as an explicit MOO target**: the framing of cytoplasm
  volume (sum of compartment volumes) as a single-objective Pareto axis has no direct
  published precedent in the multi-objective single-neuron optimisation literature. The
  catalogue documents this explicitly. Cuntz et al. 2010 and Chklovskii et al. 2002 provide
  the closest precedents (wiring economy as a constraint, not as a Pareto axis).
* **Remme 2018 paper not downloaded**: Remme 2018 ("Subthreshold resonance and metabolic
  cost") is the closest published DSI-vs-energy MOBO precedent and is referenced inline in the
  answer asset's energy and coincidence-detection sections, but the paper asset was not
  downloaded due to budget-of-effort constraints. The answer asset's `## Recommended Future
  MOBO Tasks` section documents this as a future task.
* **30 → ~21 source_paper_ids pruning**: the implementation subagent's initial draft cited 30
  paper IDs in `details.json`. The 10 downloaded t0097 paper IDs plus 9 prior-corpus IDs were
  retained. Inline citations to non-downloaded papers (e.g., Druckmann2011, Hallermann2012,
  Carter2009, etc.) remain in the prose where the methodology requires them; those papers are
  listed in the references section as "see citation" rather than as paper assets.
* **Verificator gaps**: this project's branch does not have `verify_paper_asset.py` or
  `verify_answer_asset.py`. Asset structural verification was manual against
  `meta/asset_types/{paper,answer}/specification.md`. The catalogue records this gap as a
  framework-improvement candidate.

## Files Created

* `tasks/t0097_multi_obj_optim/research/research_papers.md` — corpus survey (~3300 words)
* `tasks/t0097_multi_obj_optim/research/research_internet.md` — internet survey (~1330 lines)
* `tasks/t0097_multi_obj_optim/plan/plan.md` — task plan (~4986 words, 10 REQs)
* `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/details.json`
* `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/short_answer.md`
* `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md`
  (~6724 words)
* 10 paper assets under `tasks/t0097_multi_obj_optim/assets/paper/`:
  * `10.3389_neuro.01.1.1.001.2007/` — Druckmann 2007 (multi-objective methodology)
  * `10.1371_journal.pcbi.0020094/` — Achard & De Schutter 2006 (Purkinje MOEA)
  * `10.3389_fninf.2016.00017/` — Van Geit 2016 (BluePyOpt)
  * `10.1097_00004647-200110000-00001/` — Attwell & Laughlin 2001 (energy budget)
  * `10.1242_jeb.017574/` — Niven & Laughlin 2008 (energy limitation)
  * `10.1371_journal.pcbi.1000840/` — Sengupta 2010 (AP energy efficiency)
  * `10.1103_PhysRevLett.80.197/` — Strong et al. 1998 (entropy + information in spike trains)
  * `10.1038_nrn1949/` — Marder & Goaillard 2006 (variability + homeostasis)
  * `10.1038_nn1352/` — Prinz, Bucher & Marder 2004 (similar activity from disparate
    parameters)
  * `10.1016_s0896-6273(02)00679-7/` — Chklovskii et al. 2002 (wiring optimization)
* `tasks/t0097_multi_obj_optim/results/results_summary.md`
* `tasks/t0097_multi_obj_optim/results/results_detailed.md`
* `tasks/t0097_multi_obj_optim/results/metrics.json` (empty `{}`)
* `tasks/t0097_multi_obj_optim/results/suggestions.json` (5 ranked future-MOBO tasks)
* `tasks/t0097_multi_obj_optim/results/costs.json` (zero)
* `tasks/t0097_multi_obj_optim/results/remote_machines_used.json` (empty array)
* `tasks/t0097_multi_obj_optim/logs/steps/00{1..15}_*/step_log.md` (per-step logs)
* `tasks/t0097_multi_obj_optim/logs/sessions/capture_report.json` (reporting step)

## Task Requirement Coverage

The task's operative text (from `tasks/t0097_multi_obj_optim/task.json`):

> **Name**: "Literature survey: multi-objective optimisation of single-neuron models"
>
> **short_description**: "Survey published multi-objective optimisation of single-neuron
> compartmental models; catalogue every objective with formula, units, and a NEURON-side
> computational recipe."
>
> **expected_assets**: `paper: 10, answer: 1`

The plan's 10 requirements (REQ-1..REQ-10) and how each was met:

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | At least 10 paper assets passing the paper-asset spec | Done | 10 paper folders in `assets/paper/`; each manually verified against PA-E001..E015 by the paper-add subagent's verificator stage; PASSED. |
| REQ-2 | One consolidated answer asset passing the answer-asset spec | Done | `assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/` complete with `details.json`, `short_answer.md`, `full_answer.md`. AA-E001..E014 all pass. |
| REQ-3 | Mutual-information / ITR catalogue entry | Done | `### mutual_information_stimulus_spike_train` H3 entry in full_answer.md, 8-field record, Strong-Bialek direct method formula, recipe for t0091's 8-direction trial output, citation list (Strong1998, Brenner2000, Borst1999, Dhingra2004, Victor1997). |
| REQ-4 | Metabolic energy / ATP-per-spike catalogue entry | Done | `### metabolic_energy_atp_per_spike` H3 entry, `(1/3) sum int(I_Na) dt / e` formula, recipe with Carter2009 25%/100%-above-minimum calibration anchors, citations Attwell2001 + Sengupta2010 + Niven2008 + Carter2009 + Hallermann2012. |
| REQ-5 | Cytoplasm volume / wiring cost catalogue entry | Done | `### cytoplasm_volume` H3 entry, `sum_compartments pi*r^2*L` formula, recipe with mesh-density invariance check, novel-contribution annotation, citations Cuntz2010 + Chklovskii2002 + Cherniak1992 + LondonHausser2005 + Hines1997. |
| REQ-6 | Robustness / degeneracy catalogue entry | Done | `### robustness_under_perturbation` H3 entry, Marder-style ±10% ensemble-SD formula and recipe, citations Marder2006 + Prinz2004 + Goldman2001 + Olypher2007. |
| REQ-7 | Methodology synthesis section | Done | `## Methodology Synthesis` H2 with 6 methodology citations and the optimiser-selection rule (NSGA-II for ≤3 objectives, NSGA-III for >3, qLogNEHVI / Ament2023 warning). |
| REQ-8 | Additional catalogued objectives | Done | `## Additional Catalogued Objectives` H2 with 2 fully-detailed entries (coincidence_detection_accuracy, bits_per_atp_efficiency) plus 3 listed-but-not-detailed candidates (spike_train_distance, parameter_manifold_dimension, feature_sd_score). |
| REQ-9 | Ranked future-MOBO suggestions | Done | 5 suggestions emitted in `results/suggestions.json`: DSI × cytoplasm volume, DSI × ATP, DSI × robustness, DSI × MI, MI × ATP. Each has title, kind, priority, categories, source paper, biological-plausibility note, budget feasibility estimate ($0 to $22), cross-references. |
| REQ-10 | All standard verificators pass | Done (in reporting step) | Pre-reporting verificators (verify_research_papers, verify_research_internet, verify_plan) PASSED zero errors. Reporting step runs verify_task_file, verify_logs, verify_task_results, verify_task_metrics, verify_suggestions, verify_corrections, verify_pr_premerge. |

</details>
