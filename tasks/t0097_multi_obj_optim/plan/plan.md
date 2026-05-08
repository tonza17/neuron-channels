---
spec_version: "2"
task_id: "t0097_multi_obj_optim"
date_completed: "2026-05-08"
status: "complete"
---
# Plan: Literature Survey on Multi-Objective Optimisation of Single-Neuron Compartmental Models

## Objective

Catalogue every objective function used in the published multi-objective single-neuron compartmental
optimisation literature, deliver formula plus units plus NEURON-side computational recipe for at
least one representative objective in each of four mandatory categories (information transfer rate,
metabolic energy / ATP per spike, cytoplasm volume / wiring cost, robustness / degeneracy), and emit
a ranked list of future MOBO tasks the project should commission. Every catalogued objective must be
implementable on top of the project's existing pymoo NSGA-II loop (validated end-to-end by t0091
over 68 free parameters on a procedurally generated DSGC) without infrastructure rewrites. "Done"
means: at least 10 paper assets exist and pass `verify_paper`; one answer asset
`objective-functions-for-single-neuron-multi-objective-optimisation` exists and passes
`verify_answer`; the answer asset's full document covers all four mandatory categories with a
uniform per-objective record (name, LaTeX formula, units, NEURON-side quantities, computational
recipe on the project's t0091 8-direction trial output, biological-plausibility note,
direction-of-optimisation, at least 2 supporting paper citations); ranked future-MOBO suggestions
exist in the orchestrator-managed `results/suggestions.json`; all standard task verificators pass.

## Task Requirement Checklist

The operative task request is the long description at
`tasks/t0097_multi_obj_optim/task_description.md` (motivation, scope, must-find categories,
deliverables) plus the `task.json` `short_description`:

```text
Survey published multi-objective optimisation of single-neuron compartmental models; catalogue
every objective with formula, units, and a NEURON-side computational recipe.
```

The task's strategic directive (researcher quote, brainstorm session 20, 2026-05-08) is:

```text
Now that we have working optimisation for both morphology and channel composition we can optimise
for different things. Currently we optimise for DSI and firing rate. However I would like to
compare results for all sorts of stuff. For example, I would like to optimise for DSI and
information transfer rate; DSI and energy spent, DSI and minimisation of citoplasm volume etc.
Perform an extensive literature search and find papers that use different forms of optimisation.
It does not need to be DSGC but can be any neurons.
```

Concrete requirements extracted from the task text:

* **REQ-1** — Download and create at least 10 new paper assets covering multi-objective
  methodology plus the four must-find biological-objective categories. Each asset must follow
  paper-asset spec v3 with `details.json`, canonical `summary.md`, and `files/` (or `.gitkeep` if
  download failed). *Satisfied by*: Step 4 (paper download orchestration) and Step 5 (per-paper
  summary writing). *Evidence*: count of subfolders under
  `tasks/t0097_multi_obj_optim/assets/paper/` is at least 10 and
  `verify_paper_assets t0097_multi_obj_optim` returns 0 errors.

* **REQ-2** — Write one answer asset at
  `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/`
  with `details.json`, `short_answer.md`, and `full_answer.md` per answer-asset spec v2. The asset
  must answer the question "Which objective functions have been used in published multi-objective
  optimisation of single-neuron compartmental models, and what is each one's formula, units, and
  NEURON-side computational recipe on a t0091-style 8-direction trial output?". *Satisfied by*: Step
  6 (answer-asset construction). *Evidence*: `verify_answer_assets t0097_multi_obj_optim` returns 0
  errors.

* **REQ-3** — The answer asset's `full_answer.md` must contain a
  **`mutual_information_stimulus_spike_train`** entry in the catalogue with: LaTeX formula for
  direct-method MI between stimulus class and binned spike-count vector; units of bits per second
  (or bits per trial); NEURON-side quantities (spike times per direction); recipe step-by-step from
  a t0091-style 8-direction 1400-ms trial output (bin spikes at dt = 5 ms, build binary words of
  length T = 25-100 ms, estimate H(word | direction) and H(word) by counting, take difference,
  repeat at multiple T, fit 1/T linear regression and take the intercept per Strong et al. 1998);
  biological-plausibility note tied to Dhingra & Smith 2004's ~60% gray-level loss
  spike-vs-graded-potential calibration anchor; direction-of-optimisation = maximise; at least 2
  supporting paper citations from the corpus (Strong1998, Dhingra2004, Borst1999, or Brenner2000).
  *Satisfied by*: Step 6, Sub-step 6a. *Evidence*: section heading
  `### mutual_information_stimulus_spike_train` exists in `full_answer.md` and contains all 8
  uniform-record fields.

* **REQ-4** — The answer asset's `full_answer.md` must contain a
  **`metabolic_energy_atp_per_spike`** entry with: LaTeX formula
  `ATP per spike = (1/3) * sum_compartments integral_AP(I_Na(t) dt) / e` (where `e` is the
  elementary charge and the factor 1/3 is the Na+/K+ ATPase stoichiometry — three Na+ ions
  exchanged per ATP); units of ATP molecules per spike; NEURON-side quantities (`INa` recordings per
  section, AP-window detector); recipe step-by-step (record `ina` per compartment using NEURON
  `Vector.record(&seg.ina)`; detect AP windows from somatic Vm threshold crossings; integrate INa
  over each AP window per compartment; convert charge to ATP via Na/K pump factor; sum across
  compartments; report ATP-per-AP per direction and total ATP per trial); biological-plausibility
  note tied to Carter & Bean 2009's ~25%-above-minimum cortical-pyramidal benchmark and
  ~100%-above-minimum fast-spiking benchmark; direction-of-optimisation = minimise; at least 2
  supporting citations from Attwell2001, Sengupta2010, Carter2009, Hallermann2012, or Niven2007.
  *Satisfied by*: Step 6, Sub-step 6b. *Evidence*: section heading
  `### metabolic_energy_atp_per_spike` exists in `full_answer.md` and contains all 8 fields.

* **REQ-5** — The answer asset's `full_answer.md` must contain a **`cytoplasm_volume`** entry
  with: LaTeX formula `V_cyto = sum_compartments pi * r^2 * L`; units of cubic micrometres;
  NEURON-side quantities (per-section radius `diam/2` and length `L` after enforcing nseg <= 20 um
  per compartment per Hines & Carnevale 1997); recipe step-by-step (iterate sections from the
  project's morphology generator, sum `pi * (diam/2)^2 * L` over all compartments; optionally also
  report surface area `sum 2*pi*r*L` and bare wiring cost `sum L`); biological-plausibility note
  tied to Cuntz et al. 2010's `bf in [0.2, 0.7]` band for biologically realistic dendritic arbors
  and to Chklovskii et al. 2002's evolutionary 3/5-of-grey-matter rule; direction-of-optimisation =
  minimise; at least 2 supporting citations from Cuntz2010, Chklovskii2002, Cherniak1992, or
  Wen2006. The plan flags this objective as a novel contribution: no paper in the surveyed
  literature implements cytoplasm volume as an explicit MOO target on a single-neuron compartmental
  fit (Cuntz2010 uses it as a generator constraint, not an optimisation target). *Satisfied by*:
  Step 6, Sub-step 6c. *Evidence*: section heading `### cytoplasm_volume` exists in `full_answer.md`
  and contains all 8 fields plus a "novel contribution" annotation.

* **REQ-6** — The answer asset's `full_answer.md` must contain a
  **`robustness_under_perturbation`** entry with: LaTeX formula
  `R = std_{k=1..K}(DSI(theta + delta_k))` where `delta_k` is a +/- 10% uniform random perturbation
  of all channel densities and `K` is the Monte Carlo sample size (Marder-style ensemble); units of
  dimensionless ratio; NEURON-side quantities (ability to re-evaluate the simulation pipeline at
  perturbed channel densities and re-compute DSI from the 8-direction trial output); recipe
  step-by-step (at each Pareto point, sample 50-200 perturbations of all channel densities;
  recompute DSI for each perturbed sample using the same 8-direction protocol; report the standard
  deviation of the DSI distribution, OR the fraction of samples whose DSI drops below a threshold,
  as the robustness objective); biological-plausibility note tied to Prinz, Bucher & Marder 2004's
  20-million STG database and Goldman et al. 2001's compensatory directions;
  direction-of-optimisation = minimise standard deviation (equivalently, maximise robustness); at
  least 2 supporting citations from Marder2006, Prinz2004, Goldman2001, or Olypher2007. *Satisfied
  by*: Step 6, Sub-step 6d. *Evidence*: section heading `### robustness_under_perturbation` exists
  in `full_answer.md` and contains all 8 fields.

* **REQ-7** — The answer asset's `full_answer.md` must include a methodology section synthesising
  Druckmann2007's per-feature SD-normalisation, Hay2011's 2-3 SD acceptance threshold and
  ensemble-as-experiment reporting, Achard2006's loose-hyperplanes parameter-landscape finding, Van
  Geit 2016's BluePyOpt CellEvaluator/Protocol/EFeature triple, and the optimiser-selection rule
  (NSGA-II via pymoo for high-d 2-3 objective problems; NSGA-III for high-d many-objective problems;
  qLogNEHVI per Ament2023 for low-d <= 20 constrained problems). *Satisfied by*: Step 6, Sub-step
  6e. *Evidence*: section heading `## Methodology Synthesis` exists in `full_answer.md` and cites at
  least 4 of the listed methodology references.

* **REQ-8** — Beyond the 4 mandatory categories, the answer asset must add any well-defined
  objective categories the literature surfaces that fit the survey scope, ranked by biological
  plausibility and computational feasibility. Candidate additional categories from the research
  outputs: `coincidence_detection_accuracy` (per Remme et al. 2018), `spike_train_distance` (Victor
  & Purpura 1997), `bits_per_atp_efficiency` (Niven et al. 2007), `parameter_manifold_dimension`
  (Olypher & Calabrese 2007). *Satisfied by*: Step 6, Sub-step 6f. *Evidence*: any catalogued
  additional category beyond the four mandatory ones is listed under
  `## Additional Catalogued Objectives` with the same 8-field uniform record OR the section
  explicitly states "no additional well-defined objectives surfaced beyond the four mandatory
  categories" with reasoning.

* **REQ-9** — Emit a ranked list of 3-6 future MOBO task suggestions in `results/suggestions.json`
  (orchestrator-managed; this plan defines the content and ranking but the file is written by the
  suggestions stage, not the implementation stage). Each suggestion must include: title (e.g., "Bed
  B NSGA-II maximising DSI and ITR"), kind, priority, categories, source_paper if applicable,
  biological-plausibility notes, budget-feasibility estimate (Vast.ai EPYC + GPU hours), and
  cross-references to the catalogued objective entries in the answer asset. Suggestions are ranked
  by combined biological-plausibility + budget-feasibility scores. *Satisfied by*: implementation
  produces a draft suggestion list inside the answer asset's `## Recommended Future MOBO Tasks`
  section that the orchestrator's suggestions step (outside this plan) will lift verbatim into
  `results/suggestions.json`. *Evidence*: `## Recommended Future MOBO Tasks` section in
  `full_answer.md` lists 3-6 ranked suggestions with all required fields.

* **REQ-10** — All standard task verificators pass at PR-merge time: `verify_task_file`,
  `verify_logs`, `verify_research_papers`, `verify_research_internet`, `verify_assets`,
  `verify_suggestions`, `verify_task_results`, `verify_pr_premerge`, plus `verify_paper_assets` and
  `verify_answer_assets` for the new assets. *Satisfied by*: Step 7 (final verification pass).
  *Evidence*: each verificator returns 0 errors. Warnings are tolerated when documented.

## Approach

This is a `literature-survey` + `internet-research` + `answer-question` task (matches `task.json`
`task_types` exactly). The implementation follows three implementation milestones plus a
verification pass:

* **Milestone 1: Paper asset downloads.** The orchestrator has already launched `/add-paper`
  subagents in the background for the first batch of three papers (Druckmann2007, Attwell2001,
  Marder2006). The implementation agent does not touch `tasks/t0097_multi_obj_optim/assets/paper/`
  while those subagents are running. After those three complete, the orchestrator will spawn
  additional `/add-paper` subagents for the next batches: Niven2008, Sengupta2010, Strong1998,
  Borst1999, Prinz2004, Chklovskii2002, Achard2006, VanGeit2016, Druckmann2011 (12-13 total target,
  comfortably exceeding the 10-paper minimum).

* **Milestone 2: Answer asset construction.** Once all paper assets are present, the implementation
  agent reads the new paper summaries (plus the 9 already-corpus papers cited in
  `research/research_papers.md`: Hay2011, Cuntz2010, Ament2023, Dhingra2004, KochPoggio1982,
  Mainen1996, FohlmeisterMiller1997, Hines1997, LondonHausser2005) and writes the consolidated
  answer asset.

* **Milestone 3: Verification.** Run all standard task verificators; fix errors; tolerate documented
  warnings.

Every catalogued objective uses a uniform 8-field record (name, LaTeX formula, units, NEURON-side
quantities, recipe on the project's t0091 trial output, biological-plausibility note,
direction-of-optimisation, supporting citations). This matches `task_description.md`'s field table
verbatim and is what makes the catalogue actionable: each entry is implementable as a single pymoo
`problem.evaluate()` callable on top of the existing 68-d NSGA-II loop without infrastructure
rewrites.

The four mandatory recipes are grounded in research findings, not invented:

* **MI recipe** — Strong et al. 1998's direct method with 1/T extrapolation, calibrated against
  Dhingra & Smith 2004's ~60% gray-level loss benchmark in a real RGC.
* **ATP recipe** — Sengupta et al. 2010's `int(INa) dt / 3` per compartment per AP, with Carter &
  Bean 2009's 25%/100%-above-minimum benchmarks for cortical pyramidal vs fast-spiking cells.
* **Cytoplasm-volume recipe** — Cuntz et al. 2010's Cajal-cytoplasm-conservation `sum pi*r^2*L`,
  with Hines & Carnevale 1997's <= 20-um nseg discretisation rule for mesh-density invariance.
* **Robustness recipe** — Marder & Goaillard 2006 / Prinz et al. 2004's population-statistic
  treatment over a perturbation ensemble, with Goldman et al. 2001's compensatory-direction view.

Pairing rule (a new methodology constraint surfaced in `research_internet.md`): every catalogued
function objective should be paired with at least one biological-cost objective in any downstream
MOBO follow-up. Recommended catalogue pairs for the suggestion list: DSI vs cytoplasm volume, DSI vs
ATP-per-spike, DSI vs robustness, MI vs ATP-per-spike, MI vs cytoplasm volume. This is what makes
the catalogue address the researcher's recurring biological-plausibility concern about pure-DSI
maximisation admitting non-physical solutions.

**Alternatives considered.** (a) Generating one separate answer asset per catalogued objective
(rejected: `task.json` `expected_assets.answer = 1`; the consolidated catalogue is the right
deliverable; one-per-objective fragments evidence and complicates cross-objective pairing
recommendations). (b) Including network-level optimisation, RL/deep-learning policy optimisation,
and integrate-and-fire-only models in the catalogue (rejected: explicitly out of scope per
`task_description.md`; the survey is single-neuron compartmental only). (c) Computing every recipe
inside this task's implementation as a code-experiment to validate it on a 8-direction trial run
(rejected: this task is a literature survey, not a benchmarking task; recipe validation belongs in
the future MOBO task suggestions rather than as a prerequisite for emitting the catalogue). (d)
Using BoTorch qLogNEHVI as the recommended optimiser for the catalogue's MOBO follow-ups (rejected:
the project's own t0078 budget overrun and the Ament2023 GP O(N^3) cost analysis recommend NSGA-II
via pymoo for >= 40-d MOBO; qLogNEHVI is recommended only for low-d <= 20 constrained subsets per
Ament2023).

**Task types (matches `task.json`).** `literature-survey` (find canonical methodology + biological
objective papers, write structured per-paper `summary.md`), `internet-research` (search beyond the
existing corpus to close the four canonical-objective gaps documented in `research_papers.md`'s Gaps
section — already done in the research_internet stage), and `answer-question` (one consolidated
answer asset answering the catalogue question).

**Registered metrics.** The four registered project metrics (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) are NOT applicable to this
task — they measure simulation outputs, and this task runs no simulations. Per the planning
SKILL.md instruction, this is documented explicitly so the omission is deliberate rather than
accidental. The task's `expected_assets` field also lists no `model`, `predictions`, or `dataset`
deliverable, consistent with the metric omission.

## Cost Estimation

* **API calls**: $0 — paper metadata fetched via free OpenAlex / CrossRef / Semantic Scholar APIs;
  no paid LLM calls (per-paper summaries written by the `/add-paper` subagents in-context; the
  consolidated answer asset is written by this task's implementation agent in-context).
* **Remote compute**: $0 — runs entirely on the local Windows workstation. No simulation, no
  training, no inference, no GPU.
* **PDF retrieval**: $0 — open-access PDFs via DOI resolution; paywalled PDFs (Nature, Cell Press,
  Elsevier) via Sheffield institutional SSO at no marginal cost.
* **Total**: **$0**. Project budget remaining (per `aggregate_costs` at task start): well above the
  per-task default limit of $5; this task does not move the needle. The task is paper download
  + reading + writing, all local.

## Step by Step

**No validation gates are needed.** This task runs no inference, no model training, no paid API
calls, and no remote compute. The only "expensive" operations are paper-PDF downloads (free, local,
parallel) and reading per-paper summaries. The 10-paper minimum from `task.json`
`expected_assets.paper` is the only quantitative baseline; verification criterion VC-1 enforces it
explicitly.

### Milestone 1: Wait for paper-download subagents to complete

1. **Wait for the in-flight `/add-paper` background batch.** The orchestrator has already launched
   `/add-paper` subagents for Druckmann2007, Attwell2001, Marder2006. Do not touch
   `tasks/t0097_multi_obj_optim/assets/paper/` until those subagents complete. *Expected*: each of
   the three subagents reports completion; three new paper-asset folders exist under
   `tasks/t0097_multi_obj_optim/assets/paper/` with valid `details.json`, `summary.md`, and
   `files/`. Satisfies REQ-1 (partial; first batch).

2. **Confirm or trigger the next paper-download batches.** Inspect the asset folder count under
   `tasks/t0097_multi_obj_optim/assets/paper/`. If fewer than 10 paper assets are present, the
   orchestrator must spawn the next batches of `/add-paper` for: Niven2008, Sengupta2010,
   Strong1998, Borst1999, Prinz2004, Chklovskii2002, Achard2006, VanGeit2016, Druckmann2011 (in that
   priority order; target 12-13 total). The implementation agent does not invoke `/add-paper`
   itself; it waits for the orchestrator's signal that the paper-asset folder is complete.
   *Expected*: at least 10 paper-asset folders present after orchestrator finishes spawning batches.
   Satisfies REQ-1 (full).

3. **Verify paper assets.** Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0097_multi_obj_optim -- uv run python -m arf.scripts.verificators.verify_paper_assets t0097_multi_obj_optim`.
   Expected: 0 errors. Warnings allowed (PA-W007 missing-author-country, PA-W009 year-only-date,
   PA-W010 missing-institution-country are common for older or non-OA papers). If any error, surface
   to the orchestrator before proceeding to Milestone 2. Satisfies REQ-1.

### Milestone 2: Construct the consolidated answer asset

4. **[CRITICAL] Create the answer-asset folder structure.** Create
   `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/`
   with three files: `details.json`, `short_answer.md`, `full_answer.md`. The `details.json` must
   include:
   * `spec_version: "2"`
   * `answer_id: "objective-functions-for-single-neuron-multi-objective-optimisation"`
   * `question`: "Which objective functions have been used in published multi-objective optimisation
     of single-neuron compartmental models, and what is each one's formula, units, and NEURON-side
     computational recipe on a t0091-style 8-direction trial output?"
   * `short_title: "Catalogue of multi-objective single-neuron objective functions"`
   * `short_answer_path: "short_answer.md"`, `full_answer_path: "full_answer.md"`
   * `categories: ["compartmental-modeling", "voltage-gated-channels", "dendritic-computation"]`
   * `answer_methods: ["papers", "internet"]`
   * `source_paper_ids`: list of every paper_id cited in the full answer (all new t0097 papers plus
     relevant corpus papers — Hay2011, Cuntz2010, Ament2023, Dhingra2004, LondonHausser2005,
     Hines1997, FohlmeisterMiller1997, KochPoggio1982, Mainen1996)
   * `source_urls`: BluePyOpt GH/Docs, eFEL GH, pymoo Docs, AllenSDK Docs from
     `research_internet.md`
   * `source_task_ids`: `["t0091_morphology_extended_nsga2_v1"]` (the catalogue's downstream
     consumer)
   * `confidence: "high"` (well-established methodology + biological literature; primary risk is
     novelty of the cytoplasm-volume recipe, which is acknowledged inline)
   * `created_by_task: "t0097_multi_obj_optim"`, `date_created: "2026-05-08"` *Expected*: file
     passes `verify_answer_assets` schema check. Satisfies REQ-2.

5. **Write the short answer document.** Write
   `tasks/t0097_multi_obj_optim/assets/answer/.../short_answer.md` with YAML frontmatter
   (`spec_version: "2"`, `answer_id`, `answered_by_task`, `date_answered`) and three mandatory
   sections: `## Question` (verbatim from `details.json`), `## Answer` (2-5 sentences stating the
   catalogue's 4-mandatory-category coverage, the uniform 8-field per-objective record structure,
   and the optimiser-selection rule; no inline citations), `## Sources` (bullet list of paper_ids,
   task_ids, and URLs). *Expected*: `verify_answer_assets` passes the short-answer structural
   checks. Satisfies REQ-2.

6. **[CRITICAL] Write the full answer document.** Write
   `tasks/t0097_multi_obj_optim/assets/answer/.../full_answer.md` with YAML frontmatter
   (`spec_version`, `answer_id`, `answered_by_task`, `date_answered`, `confidence: "high"`) and the
   mandatory sections per answer-asset spec v2: `## Question`, `## Short Answer`,
   `## Research Process`, `## Evidence from Papers`, `## Evidence from Internet Sources`,
   `## Evidence from Code or Experiments` (state explicitly: not used; this is a literature survey),
   `## Synthesis`, `## Limitations`, `## Sources` (with markdown reference link definitions for
   clickable citations). Embed the catalogue under `## Synthesis` with the following sub-step
   ordering:

   * **6a (REQ-3) — `mutual_information_stimulus_spike_train` entry.** Section heading
     `### mutual_information_stimulus_spike_train` followed by 8-field uniform record: name; LaTeX
     formula `I(D; S) = H(S) - H(S | D)` with the binned-word direct-method specification; units
     `bits per second` (or bits per trial when extrapolated to T=infinity); NEURON-side quantities
     (spike times per compartment per direction, optionally Vm trace when HH is off for the
     EPSP/IPSP-passive trio); recipe (5-step Strong-Bialek procedure plus 1/T extrapolation,
     calibrated against Dhingra2004's ~60% gray-level loss); biological-plausibility note
     (information capacity is a hard biological constraint; RGCs published at 200-1000 bits/s in
     Dhingra2004 / Niven2007); direction-of-optimisation `maximise`; supporting citations
     `[Strong1998]`, `[Dhingra2004]`, `[Borst1999]`, `[Brenner2000]`. Satisfies REQ-3.

   * **6b (REQ-4) — `metabolic_energy_atp_per_spike` entry.** Section heading
     `### metabolic_energy_atp_per_spike` followed by 8-field record: LaTeX formula
     `E_AP = (1/3) sum_compartments (1/e) integral_AP I_Na(t) dt`; units of ATP molecules per spike;
     NEURON-side quantities (`INa` per section via `Vector.record(&seg.ina)`, AP-window detector
     from somatic Vm threshold crossings); recipe (record `ina` per compartment; detect AP windows;
     integrate INa over each AP window; convert charge to ATP via the Na/K-ATPase factor 1/3; sum
     across compartments; report ATP-per-AP per direction and total ATP per trial);
     biological-plausibility note (ATP per spike is the canonical Attwell-Laughlin energy budget —
     APs consume 47% of cortical signalling ATP; project's existing HH model substrate already
     exposes the required currents); direction-of-optimisation `minimise`; supporting citations
     `[Attwell2001]`, `[Sengupta2010]`, `[Carter2009]`, `[Hallermann2012]`. Satisfies REQ-4.

   * **6c (REQ-5) — `cytoplasm_volume` entry.** Section heading `### cytoplasm_volume` followed by
     8-field record: LaTeX formula `V_cyto = sum_compartments pi r_i^2 L_i`; units of cubic
     micrometres; NEURON-side quantities (per-section `diam` and `L` after enforcing `nseg` so that
     segment length <= 20 um per Hines1997); recipe (iterate sections from the project's procedural
     morphology generator; sum `pi * (diam/2)^2 * L`; optionally also report surface area
     `sum 2*pi*(diam/2)*L` and bare wiring cost `sum L` as alternative formulations);
     biological-plausibility note (Cuntz2010's `bf in [0.2, 0.7]` band defines biologically
     realistic dendritic arbors; Chklovskii2002 makes the wiring-3/5-of-grey-matter rule
     evolutionarily explicit); direction-of-optimisation `minimise`; supporting citations
     `[Cuntz2010]`, `[Chklovskii2002]`. **Annotate as a novel contribution: no surveyed paper
     implements cytoplasm volume as an explicit single-neuron MOO target — Cuntz2010 uses it as a
     generator constraint, not an optimisation objective.** Satisfies REQ-5.

   * **6d (REQ-6) — `robustness_under_perturbation` entry.** Section heading
     `### robustness_under_perturbation` followed by 8-field record: LaTeX formula
     `R(theta) = std_{k=1..K} DSI(theta + delta_k)` with
     `delta_k ~ Uniform(-0.10*theta, +0.10*theta)` applied independently to every channel-density
     parameter; units of dimensionless ratio (DSI is a ratio); NEURON-side quantities (re-evaluable
     simulation pipeline that produces DSI from the 8-direction trial output); recipe (at each
     Pareto point, sample K=50-200 perturbations of all channel densities; recompute DSI for each
     perturbed sample using the same 8-direction protocol; report standard deviation OR the fraction
     whose DSI drops below a threshold; report the full distribution in the analysis stage);
     biological plausibility note (Marder2006/Prinz2004 establish that biological robustness is best
     measured as a population statistic over a parameter manifold; Goldman2001 finds compensatory
     directions); direction-of-optimisation `minimise standard deviation` (equivalently maximise
     robustness); supporting citations `[Marder2006]`, `[Prinz2004]`, `[Goldman2001]`,
     `[Olypher2007]`. Satisfies REQ-6.

   * **6e (REQ-7) — Methodology section.** Add a `## Methodology Synthesis` section above the
     catalogue covering: Druckmann2007's per-feature SD-normalisation; Hay2011's 2-3 SD acceptance
     threshold and ensemble-as-experiment reporting (referencing the existing corpus paper);
     Achard2006's loose-hyperplanes parameter-landscape finding; VanGeit2016's BluePyOpt
     CellEvaluator/Protocol/EFeature triple as the structural template the project's evaluator
     should adopt while keeping pymoo NSGA-II as the optimiser; the optimiser-selection rule
     (NSGA-II via pymoo for high-d 2-3 objective; NSGA-III via pymoo for high-d many-objective per
     Deb2014/Blank2020; qLogNEHVI per Ament2023 for low-d <= 20 constrained problems; never
     canonical qNEHVI which has the vanishing-gradient pathology Ament2023 documents). Satisfies
     REQ-7.

   * **6f (REQ-8) — Additional catalogued objectives section.** Add a
     `## Additional Catalogued Objectives` section listing any well-defined objective categories
     beyond the four mandatory ones, each with the same 8-field uniform record format. Candidate
     additions surfaced by the research stages: `coincidence_detection_accuracy` (Remme2018; pairs
     function with energy in MSO neurons — closest published precedent for the project's planned
     DSI-vs-energy MOBO), `bits_per_atp_efficiency` (Niven2007's fly photoreceptor 200-1000 bits/s
     super-linear cost-vs-information curve), `spike_train_distance` (Victor1997's metric-space
     spike-train discrimination; binning-free alternative to MI), `parameter_manifold_dimension`
     (Olypher2007's implicit-function-theorem manifold codimension as a structural complexity
     objective). Include at least the strongest 2 of these (`coincidence_detection_accuracy`,
     `bits_per_atp_efficiency`); document the others as listed-but-not-detailed. If the survey
     surfaces zero credible additional categories, this section must explicitly state that and
     explain why. Satisfies REQ-8.

   * **6g (REQ-9) — Recommended Future MOBO Tasks section.** Add a
     `## Recommended Future MOBO Tasks` section listing 3-6 ranked future MOBO task suggestions,
     each with: title (e.g., "Bed B NSGA-II maximising DSI and information transfer rate"); kind
     (`experiment`); priority (`high` / `medium` / `low`); relevant categories; the pair of
     catalogued objectives it would optimise; biological-plausibility note; budget feasibility
     estimate (e.g., "12-24 h on Vast.ai EPYC 7763 with 64 cores at $0.30/h, total cost $4-8 within
     the per-task default $5 limit"); cross-references to the catalogued entries by anchor name.
     Suggestions must be ranked by combined biological plausibility + budget feasibility.
     Recommended starter ranking (in priority order): (1) DSI vs cytoplasm volume (highest
     biological plausibility, infrastructure already in place via procedural morphology generator);
     (2) DSI vs ATP-per-spike (closest published analogue Remme2018, recipe from Sengupta2010); (3)
     DSI vs robustness (directly addresses the researcher's biological-plausibility concern with
     pure-DSI maximisation); (4) DSI vs information transfer rate (recipe from
     Strong1998/Dhingra2004, validates against ~60% gray-level-loss benchmark); (5) MI vs
     ATP-per-spike (decouples function from selectivity; yields the bits-per-ATP Pareto curve
     directly comparable to Niven2007's fly photoreceptors). Satisfies REQ-9.

7. **Run flowmark on the answer document.** Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0097_multi_obj_optim -- uv run flowmark --inplace --nobackup tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md`
   then the same command on `short_answer.md`. *Expected*: both files reflowed to 100-char target;
   no structural change; subsequent `verify_answer_assets` still passes.

### Milestone 3: Verification

8. **[CRITICAL] Run all task verificators.** Run each of the following inside the `run_with_logs`
   wrapper, in order:
   * `uv run python -m arf.scripts.verificators.verify_task_file t0097_multi_obj_optim`
   * `uv run python -m arf.scripts.verificators.verify_logs t0097_multi_obj_optim`
   * `uv run python -m arf.scripts.verificators.verify_research_papers t0097_multi_obj_optim`
   * `uv run python -m arf.scripts.verificators.verify_research_internet t0097_multi_obj_optim`
   * `uv run python -m arf.scripts.verificators.verify_paper_assets t0097_multi_obj_optim`
   * `uv run python -m arf.scripts.verificators.verify_answer_assets t0097_multi_obj_optim`
   * `uv run python -m arf.scripts.verificators.verify_assets t0097_multi_obj_optim`

   Expected: each returns 0 errors. Warnings allowed if documented inline. Satisfies REQ-10
   (partial; the orchestrator-managed verifiers `verify_suggestions`, `verify_task_results`,
   `verify_pr_premerge` run in their own stages outside this plan).

This is the end of implementation work. Subsequent orchestrator-managed stages (results writing,
suggestion emission, literature comparison, and the post-implementation verificators) are out of
scope for this plan.

## Remote Machines

None required. The task runs entirely on the local Windows workstation. Paper PDF downloads use
local HTTP requests (no GPU). Summary writing happens in the implementation agent's context (no paid
API). No simulation, no training, no inference.

## Assets Needed

* **9 already-corpus papers** cited in `research/research_papers.md`: Hay2011, Cuntz2010, Ament2023,
  Dhingra2004, KochPoggio1982, Mainen1996, FohlmeisterMiller1997, Hines1997, LondonHausser2005. Cite
  by paper_id only; no copying.
* **12-13 new papers** (REQ-1) downloaded by background `/add-paper` subagents in batches:
  Druckmann2007, Druckmann2011, Achard2006, VanGeit2016, Attwell2001, Niven2008, Sengupta2010,
  Marder2006, Prinz2004, Chklovskii2002, Strong1998, Borst1999, plus 1 buffer paper for
  download-failure resilience. Source: `research/research_internet.md` Discovered Papers section.
* **4 prior literature-survey answer assets for stylistic consistency**: t0002 DSGC compartmental
  models, t0015 cable theory, t0016 dendritic computation, t0027 morphology + DS modeling. Read for
  tone and structure only; no copying.
* **External resources**: BluePyOpt GitHub + Read the Docs URLs, eFEL GitHub, pymoo Read the Docs,
  AllenSDK Docs (per `research/research_internet.md` Tool and Library Landscape section).

## Expected Assets

Matches `task.json` `expected_assets`:

* **paper × at least 10** (target 12-13) — new paper assets at
  `tasks/t0097_multi_obj_optim/assets/paper/<paper_id>/{details.json, summary.md, files/}`, each
  covering a methodology or biological-objective reference for single-neuron MOO. Each asset follows
  paper-asset spec v3 with the canonical 9-section summary.
* **answer × 1** —
  `tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/{details.json, short_answer.md, full_answer.md}`,
  the consolidated objective-function catalogue with all four mandatory categories plus any
  additional surfaced categories, methodology synthesis, and ranked future MOBO suggestions.

## Time Estimation

* Research (already done): 60-90 min papers + 30-60 min internet, complete.
* Implementation Milestone 1 (paper-download wait + verification): orchestrator-paced; the
  `/add-paper` subagents run in parallel and the implementation agent simply waits.
* Implementation Milestone 2 (answer-asset construction): 60-90 min for 7 sub-steps (4 mandatory
  category entries, methodology synthesis, additional-objectives section, future-MOBO
  recommendations).
* Implementation Milestone 3 (verification): 5-10 min to run all verificators.
* Reporting + suggestions + PR (orchestrator-owned): 30-60 min.
* **Total wall-clock from start of implementation to PR merge**: 2-4 hours, matching
  `task_description.md`'s estimate.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| One or more paper PDFs cannot be retrieved (paywall, dead URL, archived journal) | Medium | Asset has only abstract-based summary; if 3+ fail, the 10-paper minimum (REQ-1) may be threatened | The `/add-paper` subagents already write `download_status: "failed"` with `download_failure_reason` per paper-asset spec v3 when a PDF fails; abstract-based summary is allowed by the spec. The orchestrator's batch list includes 12-13 candidate papers vs the 10-paper floor, providing 2-3 paper buffer. If even that buffer is exhausted, the orchestrator queues additional papers from the "Optional Discovered Papers" list in `research/research_internet.md` (Cherniak1992, Wen2006, Victor1997, Deb2002, Deb2014). |
| Cytoplasm-volume recipe has no published precedent as an explicit single-neuron MOO objective | High (acknowledged) | Reviewer may flag REQ-5 as speculative | The plan flags this as a novel contribution (per `task_description.md` Risks & Fallbacks). The recipe is mathematically trivial (`sum pi*r^2*L`), the biological grounding via Cuntz2010's `bf in [0.2, 0.7]` band is well-established, and Chklovskii2002 supplies the evolutionary justification. The answer asset's `## Limitations` section will state explicitly that no surveyed paper implements this as an MOO target. |
| Answer asset's full document exceeds the 5000-word soft ceiling from `task_description.md` | Medium | Document becomes hard to read | Each catalogued objective uses an 8-field uniform record format, capping per-entry length. The methodology synthesis (REQ-7) is consolidated into one section, not duplicated per objective. Word-count check at the end of Step 6: if `wc -w full_answer.md` exceeds 5000, split per-category subsections into separate H2 sections while keeping `short_answer.md` as a single-page entry point. |
| Implementation agent invents citations not present in the downloaded paper assets | Low (per `meta/task_types/literature-survey/instruction.md` warning) | Hard verificator failure (`AA-E009`) | Step 6 cites every paper by `paper_id` and the answer asset's `details.json` `source_paper_ids` field is fact-checked against `assets/paper/` folder names before committing. The literature-survey type's "NEVER fabricate citations" rule is enforced. |
| Background `/add-paper` subagents complete out of order or one stalls | Medium | Implementation agent blocked at Milestone 1 | The orchestrator owns `/add-paper` lifecycle; if a subagent stalls > 30 min, it is killed and re-spawned with the next-priority paper. Implementation agent inspects `assets/paper/` folder count, not subagent identity, so partial completions are fine as long as the 10-paper floor is met. |
| The four registered project metrics get force-fitted into `metrics.json` even though they do not apply | Low | False metric values pollute `aggregate_metric_results` | The plan documents the metric-omission decision explicitly (see Approach final paragraph): the literature survey runs no simulations, produces no DSI/HWHM/RMSE/reliability values, and `results/metrics.json` will be an empty object or absent (orchestrator-managed). |

## Verification Criteria

* **VC-1 (REQ-1)**: Run
  `find tasks/t0097_multi_obj_optim/assets/paper -mindepth 1 -maxdepth 1 -type d | wc -l` and
  confirm count is at least 10.
* **VC-2 (REQ-1)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0097_multi_obj_optim -- uv run python -m arf.scripts.verificators.verify_paper_assets t0097_multi_obj_optim`
  and confirm 0 errors. Warnings PA-W007 / PA-W009 / PA-W010 / PA-W011 allowed.
* **VC-3 (REQ-2 to REQ-9)**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0097_multi_obj_optim -- uv run python -m arf.scripts.verificators.verify_answer_assets t0097_multi_obj_optim`
  and confirm 0 errors. The answer asset's `details.json` `source_paper_ids` must include at least
  10 of the new t0097 papers plus 4-6 corpus papers (Hay2011, Cuntz2010, Ament2023, Dhingra2004,
  optionally LondonHausser2005, Hines1997).
* **VC-4 (REQ-3, REQ-4, REQ-5, REQ-6)**: Run
  `grep -E "^### (mutual_information_stimulus_spike_train|metabolic_energy_atp_per_spike|cytoplasm_volume|robustness_under_perturbation)$" tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md`
  and confirm all four headings present, each occurring exactly once.
* **VC-5 (REQ-7)**: Run
  `grep -E "^## Methodology Synthesis$" tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md`
  and confirm the heading is present. Inspect the section and confirm at least 4 of Druckmann2007,
  Hay2011, Achard2006, VanGeit2016, Deb2014, Ament2023 are cited.
* **VC-6 (REQ-8)**: Run
  `grep -E "^## Additional Catalogued Objectives$" tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md`
  and confirm the section exists. Inspect: it must either list at least 2 additional objectives with
  full 8-field records (e.g., `coincidence_detection_accuracy`, `bits_per_atp_efficiency`) OR
  explicitly state no additional well-defined objectives surfaced beyond the four mandatory.
* **VC-7 (REQ-9)**: Run
  `grep -E "^## Recommended Future MOBO Tasks$" tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md`
  and confirm the section exists. Inspect: 3-6 ranked future-MOBO suggestions with title, kind,
  priority, biological-plausibility note, and budget-feasibility estimate per suggestion.
* **VC-8 (REQ-10)**: Run each of `verify_task_file`, `verify_logs`, `verify_research_papers`,
  `verify_research_internet`, `verify_paper_assets`, `verify_answer_assets`, `verify_assets` (the
  implementation-stage subset) on `t0097_multi_obj_optim` and confirm each returns 0 errors. The
  orchestrator's later stages run `verify_suggestions`, `verify_task_results`, `verify_pr_premerge`
  separately.
* **VC-9 (REQ-1, REQ-2 coverage)**: Run the answer-aggregator
  `uv run python -m arf.scripts.aggregators.aggregate_answers --ids objective-functions-for-single-neuron-multi-objective-optimisation --format json --detail full`
  and confirm the asset is enumerated with the expected `source_paper_ids` count.
