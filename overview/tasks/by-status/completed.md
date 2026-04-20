# ✅ Tasks: Completed

12 tasks. ✅ **12 completed**.

[Back to all tasks](../README.md)

---

## ✅ Completed

<details>
<summary>✅ 0016 — <strong>Literature survey: dendritic computation beyond
DSGCs</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0016_literature_survey_dendritic_computation` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-02` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-19T23:38:58Z |
| **End time** | 2026-04-20T10:36:25Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: dendritic computation beyond DSGCs](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Task folder** | [`t0016_literature_survey_dendritic_computation/`](../../../tasks/t0016_literature_survey_dendritic_computation/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0016_literature_survey_dendritic_computation/results/results_detailed.md) |

# Literature survey: dendritic computation beyond DSGCs

## Motivation

Research question RQ4 (active vs passive dendrites) needs evidence from computational
neuroscience beyond the retinal literature. Cortical and cerebellar dendrites have been
studied far more extensively than DSGC dendrites, and the mechanisms and modelling conventions
developed there (NMDA spikes, Ca/Na plateaus, branch-level nonlinearities) are the natural
reference for whether active dendrites plausibly shape DSGC tuning curves. Source suggestion:
S-0014-02 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. NMDA spikes — thresholds, amplitudes, distance-dependence, supralinear integration.
2. Na+ and Ca2+ dendritic spikes — backpropagation, forward propagation, local spikes.
3. Plateau potentials — in-vivo evidence, role in coincidence detection, duration scaling.
4. Branch-level nonlinearities — independent subunits, clustered-vs-distributed input
   summation.
5. Sublinear-to-supralinear integration regimes — what controls the transition, which
   conditions make dendrites behave passively in practice.
6. Active-vs-passive modelling comparisons — cortical, cerebellar, hippocampal studies that
   built matched active and passive compartmental models and quantified the difference.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each of the six themes above with preference for review
   articles plus 2-4 primary studies per theme.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md` for the
   researcher to retrieve manually.
3. Write one answer asset synthesising which dendritic-computation mechanisms plausibly
   transfer to DSGC dendrites, with explicit caveats about anatomical and biophysical
   differences.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant), some possibly with
  `download_status: "failed"`.
* One answer asset under `assets/answer/` synthesising the six themes and flagging mechanisms
  most plausible for DSGC dendrites.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and explicitly addresses transferability to
  DSGC dendrites.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

**Results summary:**

> **Results Summary: Dendritic-Computation Literature Survey**
>
> **Summary**
>
> Surveyed 5 foundational dendritic-computation papers (Schiller 2000, Polsky 2004, Larkum
> 1999,
> Bittner 2017, London & Hausser 2005) and produced a single answer asset synthesising which
> dendritic-computation motifs plausibly transfer to DSGC dendrites and the biophysical
> caveats on
> each transfer. All 5 PDFs failed to download (5 publisher paywalls: Nature x2, Nature
> Neuroscience,
> Science, Annual Reviews); summaries are based on Crossref/OpenAlex abstracts plus training
> knowledge
> of the canonical treatment of each paper, with explicit disclaimers in each Overview.
>
> **Objective**
>
> Survey the foundational dendritic-computation literature (NMDA spikes, Ca2+ dendritic
> spikes, BAC
> firing, plateau potentials/BTSP, branch-level nonlinear integration, and regime switching)
> and
> synthesise a single answer asset mapping which motifs plausibly transfer to DSGC dendrites
> and the
> biophysical caveats on each transfer.
>
> **What Was Produced**
>

</details>

<details>
<summary>✅ 0015 — <strong>Literature survey: cable theory and dendritic
filtering</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0015_literature_survey_cable_theory` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 5 paper, 1 answer |
| **Source suggestion** | `S-0014-01` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-19T23:38:43Z |
| **End time** | 2026-04-20T10:00:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: cable theory and dendritic filtering](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Task folder** | [`t0015_literature_survey_cable_theory/`](../../../tasks/t0015_literature_survey_cable_theory/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0015_literature_survey_cable_theory/results/results_detailed.md) |

# Literature survey: cable theory and dendritic filtering

## Motivation

The t0002 corpus concentrates on direction-selective retinal ganglion cell (DSGC)
compartmental models. Downstream calibration and optimisation tasks (segment discretisation,
morphology-sensitive tuning, dendritic attenuation) need a deeper grounding in classical cable
theory and passive dendritic filtering than t0002 provides. This task broadens the corpus into
the foundational theory. Source suggestion: S-0014-01 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Rall-era foundations — passive cable equation, equivalent cylinder, classical Rall papers.
2. Segment discretisation guidelines — `d_lambda` rule, spatial-frequency constraints on
   `nseg`.
3. Branched-tree impedance — transfer impedance, voltage attenuation in branched dendrites.
4. Frequency-domain analyses — input impedance, synaptic-event filtering, chirp / ZAP
   analyses.
5. Transmission in thin dendrites — space constant, propagation failure, passive integration
   limits.

Exclusion: do not re-add any DOI already present in the t0002 corpus (20 DOIs under
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`). Duplicates
discovered mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` with search terms targeting each of the five themes above.
2. For each shortlisted paper, invoke `/download-paper` — the skill produces a v3-compliant
   paper asset (`details.json`, summary document, files). Papers behind institutional paywalls
   are recorded as `download_status: "failed"` and added to `intervention/paywalled_papers.md`
   for the researcher to retrieve manually from their institutional account.
3. After the paper set is assembled, write one answer asset that synthesises the corpus by
   theme and maps each paper to its relevance for the project's direction-selectivity
   modelling work.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant). Some may have `download_status:
  "failed"` pending manual retrieval.
* One answer asset under `assets/answer/` synthesising the five themes and identifying the
  cable-theory parameters most directly useful for downstream DSGC tasks.
* `intervention/paywalled_papers.md` listing DOIs the researcher must download manually.

## Compute and Budget

No paid services required for the automated pass. The task type `literature-survey` is gated
on the project budget — the brainstorm session set `project/budget.json` `total_budget` to $1
to clear the gate; no actual spend is expected.

## Dependencies

None. This task is independent of the t0002 corpus (beyond the deduplication constraint).

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py` (accounting for some paywalled
  failures).
* The answer asset passes `verify_answer_asset.py`.
* `intervention/paywalled_papers.md` exists with a DOI list if any downloads failed.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

**Results summary:**

> **Results Summary: Cable-Theory Literature Survey**
>
> **Summary**
>
> Surveyed 5 foundational cable-theory and DSGC-biophysics papers and produced a single answer
> asset
> giving a concrete 6-point compartmental-modelling specification for DSGCs in NEURON. All 5
> PDFs
> failed to download (4 paywalls + 1 Cloudflare block); summaries are based on
> Crossref/OpenAlex
> abstracts plus training knowledge with explicit disclaimers.
>
> **Objective**
>
> Survey foundational cable-theory and dendritic-computation literature and synthesize
> concrete
> compartmental-modelling guidance for direction-selective retinal ganglion cells (DSGCs) in
> NEURON.
>
> **What Was Produced**
>
> * **5 paper assets** covering the core cable-theory / DSGC-biophysics literature:
> * Rall 1967 — cable-theoretic foundations and EPSP shape-index diagnostic
> * Koch, Poggio, Torre 1982 — on-the-path shunting DS mechanism
> * Mainen & Sejnowski 1996 — morphology-driven firing diversity, `d_lambda` discretization

</details>

<details>
<summary>✅ 0014 — <strong>Brainstorm results session 3</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0014_brainstorm_results_3` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-19T23:10:00Z |
| **End time** | 2026-04-19T23:45:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 3](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Task folder** | [`t0014_brainstorm_results_3/`](../../../tasks/t0014_brainstorm_results_3/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0014_brainstorm_results_3/results/results_detailed.md) |

# Brainstorm Session 3 — Per-Category Literature-Survey Wave

## Context

The project has completed its first two task waves:

* **Wave 1** (t0001-t0005): foundational brainstorm, DSGC-focused compartmental-model
  literature survey, simulator survey, canonical target tuning curve, baseline DSGC morphology
  download.
* **Wave 2** (t0007-t0013, planned by t0006): NEURON install (t0007 done), plus calibration,
  porting, visualisation, scoring, and provenance tasks (t0008-t0013 still in-flight or not
  started).

The paper corpus contains 20 DOIs from t0002 (DSGC compartmental models). Categories
`direction-selectivity`, `compartmental-modeling`, and `retinal-ganglion-cell` are already
well-covered by that survey. Five remaining categories are under-covered: `cable-theory`,
`dendritic-computation`, `patch-clamp`, `synaptic-integration`, `voltage-gated-channels`.

## Session Goal

Plan a per-category literature-survey wave (Wave 3) that broadens the paper corpus so the
project's research questions about Na/K conductance combinations, active-vs-passive dendrites,
and synaptic kinetics can be grounded in the wider neuroscience literature rather than only
DSGC-specific work.

## Decisions

1. **Drop the 3 saturated categories** (direction-selectivity, compartmental-modeling,
   retinal-ganglion-cell). The existing t0002 corpus + queued t0010 (hunt missed DSGC models)
   cover them adequately.

2. **Create 5 new literature-survey tasks** (t0015-t0019), one per remaining category, each
   targeting ~25 category-relevant papers with cross-category overlap accepted (option (b)
   from the brainstorm discussion). Total attempted: ~125 papers, expected unique ~80-100
   after cross-task dedup (addressed by a later dedup-checkpoint task).

3. **Exclude the 20-DOI t0002 corpus** from each new task's search to avoid wasting download
   budget on already-owned papers.

4. **Bump `project/budget.json` `total_budget` from $0 to $1** so the mechanical
   `has_external_costs: true` gate on the `literature-survey` task type does not block
   execution. Literal expected spend remains $0 (arXiv, PubMed Central, ModelDB, and
   open-access sources are free; summarisation is done in-session).

5. **Paywalled paper protocol**: each task lists paywalled DOIs in
   `intervention/paywalled_papers.md`; the researcher downloads PDFs manually from their
   institutional account into `assets/paper/<paper_id>/files/` and the task then upgrades
   `download_status` to `"success"` with a full summary in a follow-up pass.

## New Suggestions Produced

Five dataset-kind suggestions (S-0014-01 through S-0014-05), each `priority: high`, one per
new task. These are recorded in `results/suggestions.json` and become the `source_suggestion`
for their respective child task.

## Out of Scope

* No experiments this session — this is a planning-only brainstorm.
* No corrections — t0002 corpus is correct; we are extending, not correcting.
* No new asset types or task types — `literature-survey` already exists.

**Results summary:**

> **Brainstorm session 3 — Summary**
>
> **Summary**
>
> Planned a five-task literature-survey wave (t0015-t0019) to broaden the project's paper
> corpus
> beyond the DSGC-specific modelling focus of t0002. Authorised a $1 budget bump (to be
> applied
> directly on `main` as a follow-up commit, since task branches cannot modify
> `project/budget.json`)
> so `literature-survey` tasks clear the project budget gate without incurring real spend.
> Confirmed a
> paywalled-paper workflow where each survey emits an `intervention/paywalled_papers.md` the
> researcher resolves from their institutional account.
>
> **Decisions**
>
> * **Five surveys, one per under-saturated category**: cable-theory, dendritic-computation,
> patch-clamp, synaptic-integration, voltage-gated-channels. Dropped `direction-selectivity`,
> `compartmental-modeling`, and `retinal-ganglion-cell` because t0002 plus t0010 already
> saturate
> them.
> * **Target ~25 category-relevant papers per task** (not 20). Extra headroom compensates for
>   the
> deduplication constraint and for papers that ultimately fail quality filters.
> * **Exclude the 20 DOIs already in the t0002 corpus** from each survey. Duplicate hits must
>   be

</details>

<details>
<summary>✅ 0012 — <strong>Tuning-curve scoring loss library</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0012_tuning_curve_scoring_loss_library` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-09` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-20T01:02:11Z |
| **End time** | 2026-04-20T09:58:10Z |
| **Step progress** | 10/15 |
| **Task page** | [Tuning-curve scoring loss library](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Task folder** | [`t0012_tuning_curve_scoring_loss_library/`](../../../tasks/t0012_tuning_curve_scoring_loss_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0012_tuning_curve_scoring_loss_library/results/results_detailed.md) |

# Tuning-curve scoring loss library

## Motivation

The t0002 literature survey set four concurrent quantitative targets an optimised DSGC model
must hit: DSI **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM
**60-90°**. The project has four registered metrics (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`). Every downstream
optimisation task (Na/K grid search S-0002-01, morphology sweep S-0002-04, E/I ratio scan
S-0002-05, active-vs-passive dendrites S-0002-02) needs a shared scoring function: same
target, same weighting, same tie-breaks. Without this library, each task will invent its own
scoring and cross-task comparisons of "who wins" become meaningless. This task provides that
canonical scorer.

Covers suggestion **S-0002-09** (and subsumes **S-0004-03** — see the t0006 correction file).

## Scope

The library `tuning_curve_loss` exposes:

1. `score(simulated_curve_csv, target_curve_csv | None) -> ScoreReport` — returns a frozen
   dataclass containing:
   * `loss_scalar` (float) — weighted-Euclidean-distance-in-normalised-space loss combining
     the four envelope targets.
   * `dsi_residual`, `peak_residual_hz`, `null_residual_hz`, `hwhm_residual_deg` — individual
     residuals with signs.
   * `rmse_vs_target` — point-wise RMSE of `(angle, firing_rate)` against the target curve
     (only when a target is supplied).
   * `reliability` — cross-trial coefficient of determination (maps onto the registered
     `tuning_curve_reliability` metric).
   * `passes_envelope` (bool) — whether the simulated curve lands inside the t0002 envelope on
     all four targets simultaneously.
   * `per_target_pass` — dict `{"dsi": bool, "peak": bool, "null": bool, "hwhm": bool}`.
2. `compute_dsi(curve_csv) -> float`
3. `compute_preferred_peak_hz(curve_csv) -> float`
4. `compute_null_residual_hz(curve_csv) -> float`
5. `compute_hwhm_deg(curve_csv) -> float`
6. Tuning-curve CSV schema constant: `(angle_deg, trial_seed, firing_rate_hz)`.
7. CLI: `python -m tuning_curve_loss.cli <simulated.csv> [--target <target.csv>]`.

Weights for the scalar loss default to **DSI 0.25, peak 0.25, null 0.25, HWHM 0.25** but are
user-overridable via a keyword argument and via a JSON config file; the defaults and rationale
are documented in the asset's `description.md`.

## Dependencies

* **t0004_generate_target_tuning_curve** — source of the canonical `target-tuning-curve`
  dataset used as the default comparison target and as the smoke-test fixture.

## Expected Outputs

* **1 library asset** (`assets/library/tuning-curve-loss/`) with:
  * `description.md` covering API, weight defaults, and worked examples
  * `module_paths` pointing at `code/tuning_curve_loss/`
  * `test_paths` pointing at `code/tuning_curve_loss/test_*.py` with at least:
    * Identity test: `score(target, target)` must return `loss_scalar == 0.0` and
      `passes_envelope is True`.
    * Envelope-boundary tests: hand-crafted curves just inside and just outside each of the
      four envelope boundaries.
    * Reliability test: two curves with identical trial-means but very different
      trial-to-trial variance produce different `reliability` values.

## Approach

Pure Python + NumPy + pandas. No simulator dependency. The DSI and HWHM computations must
match the closed-form computations used in t0004 to produce the target curve, so that
`score(target, target)` is exactly zero. Use the registered metric keys from `meta/metrics/`
so that scored values can be written directly into `results/metrics.json` without post-hoc
renaming.

## Questions the task answers

1. Does `score(target, target)` return `loss_scalar == 0.0`?
2. Do the envelope-boundary tests flip `passes_envelope` at the correct boundary to within
   floating-point tolerance?
3. Does the scorer accept multi-trial CSVs and correctly combine trials into a mean before
   computing DSI, peak, null and HWHM?

## Risks and Fallbacks

* **The literature envelope numbers conflict with the t0004 target curve** (e.g., the target
  sits right at an envelope boundary): document the target's position on the envelope in the
  library description; do not silently redefine targets.
* **Trial-to-trial variance inflates `reliability` beyond sensible bounds**: clamp to [0, 1]
  and document the clamp.

**Results summary:**

> **Results Summary: Tuning-Curve Scoring Loss Library**
>
> **Summary**
>
> Built and registered the `tuning_curve_loss` Python library: an 8-module package that loads
> a DSGC
> tuning curve from CSV, computes DSI, peak, null, and HWHM, and scores a candidate curve
> against the
> t0004 target as a weighted Euclidean residual in envelope-half-width units. The identity
> gate
> `score(target, target).loss_scalar == 0.0` and `passes_envelope is True` holds exactly. All
> 47
> pytest tests pass, ruff and mypy are clean, and the library asset is registered at
> `assets/library/tuning_curve_loss/`.
>
> **Metrics**
>
> * **Tests passed**: **47 / 47** (0 failed, 0 skipped)
> * **Identity loss on t0004 target**: **0.0** (exact)
> * **Library modules**: **8** (paths, loader, metrics, envelope, weights, scoring, cli,
>   `__init__`)
> * **Public entry points**: **13** (score, compute_dsi, compute_peak_hz, compute_null_hz,
> compute_hwhm_deg, compute_reliability, load_tuning_curve, passes_envelope, validate_weights,
> load_weights_from_json, Envelope, ScoreResult, TuningCurveMetrics)
> * **Test modules**: **5** covering loader, metrics, envelope, scoring, and CLI

</details>

<details>
<summary>✅ 0009 — <strong>Calibrate dendritic diameters for
dsgc-baseline-morphology</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0009_calibrate_dendritic_diameters` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0005-02` |
| **Task types** | [`feature-engineering`](../../../meta/task_types/feature-engineering/), [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-04-19T21:37:04Z |
| **End time** | 2026-04-20T00:12:29Z |
| **Step progress** | 12/15 |
| **Task page** | [Calibrate dendritic diameters for dsgc-baseline-morphology](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Task folder** | [`t0009_calibrate_dendritic_diameters/`](../../../tasks/t0009_calibrate_dendritic_diameters/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0009_calibrate_dendritic_diameters/results/results_detailed.md) |

# Calibrate dendritic diameters for dsgc-baseline-morphology

## Motivation

Every compartment in the downloaded `dsgc-baseline-morphology` CNG-curated SWC (NeuroMorpho
neuron 102976, 141009_Pair1DSGC) carries the placeholder radius **0.125 µm** because the
original Simple Neurite Tracer reconstruction did not record diameters. Cable theory predicts
that segment diameter is the single most influential *local-electrotonic* knob on axial
resistance, spatial attenuation and spike-initiation threshold, so leaving a uniform
placeholder in place will silently bias every downstream biophysical simulation. This task
replaces the placeholder with a literature-derived order-dependent taper keyed on Strahler
order or path distance from the soma, and registers the calibrated morphology as a new dataset
asset that downstream tasks (t0008 reproduction, t0011 visualisation smoke-test, and the
experiment tasks) will load instead of the raw placeholder SWC.

Covers suggestion **S-0005-02**.

## Scope

1. **Research stage**: survey the published mouse ON-OFF DSGC morphometric literature for a
   defensible diameter taper rule. Candidate sources explicitly identified as plausible:
   * Vaney / Sivyer / Taylor 2012 review + original figures
   * Poleg-Polsky & Diamond 2016 (ModelDB 189347) per-order diameter profile
   * Other published Feller-lab / Briggman-lineage DSGC reconstructions with diameters
     recorded. Pick one primary source and one fallback source; document the choice and the
     per-order distribution in `research/research_papers.md`.
2. **Implementation**:
   * Parse the CNG-curated SWC with a stdlib parser (can reuse
     `tasks/t0005_download_dsgc_morphology/code/validate_swc.py` approach).
   * Compute per-compartment Strahler order and path distance from the soma.
   * Apply the chosen taper rule to assign a realistic radius to every dendritic compartment.
     Preserve the 19 soma compartments' original (non-placeholder) radii.
   * Write the new SWC to `assets/dataset/dsgc-baseline-morphology-calibrated/files/`.
3. **Register** the calibrated morphology as a v2 dataset asset
   (`assets/dataset/dsgc-baseline-morphology-calibrated/`) with a `details.json`, a
   `description.md`, and the calibrated SWC file. The `details.json` must reference
   `dsgc-baseline-morphology` as the raw source and cite the chosen taper-source paper.
4. **Validation**:
   * Plot per-Strahler-order radius distributions (original placeholder vs calibrated) and
     save as PNG to `results/images/`.
   * Recompute total surface area and axial resistance per branch; report the change vs the
     placeholder baseline.
   * Confirm compartment count, branch points and connectivity are unchanged from the source
     SWC.

## Dependencies

* **t0005_download_dsgc_morphology** — source of `dsgc-baseline-morphology` raw SWC and the
  stdlib parser.

## Expected Outputs

* **1 dataset asset** (`assets/dataset/dsgc-baseline-morphology-calibrated/`) — calibrated
  SWC.
* Per-order diameter distribution plots in `results/images/` (original vs calibrated).
* Brief answer-style report embedded in `results/results_detailed.md` summarising the chosen
  taper rule, the rationale, and the change in surface area / axial resistance vs the
  placeholder.

## Questions the task answers

1. Which published taper source is most faithful for mouse ON-OFF DSGCs of the
   141009_Pair1DSGC lineage?
2. What is the Strahler-order-to-radius (or path-distance-to-radius) mapping used in the
   calibration?
3. How does total dendritic surface area change from the placeholder baseline to the
   calibrated morphology?
4. How does axial resistance along the preferred-to-null dendritic axis change, and what does
   that predict for spike-attenuation at the soma?

## Risks and Fallbacks

* **No published source gives a cell-matched per-order taper**: fall back to the Poleg-Polsky
  ModelDB distribution and clearly label the calibrated asset as "Poleg-Polsky-profile
  calibrated" rather than "literature-grounded".
* **The chosen taper makes distal tips implausibly thin (< 0.1 µm)**: clamp the radius floor
  at 0.15 µm and document the clamp.
* **Calibration collapses spatial detail (uniform assignment)**: treat as a bug, not a
  feature; re-derive the taper until per-order variability survives.

**Results summary:**

> **Results Summary: Calibrate Dendritic Diameters**
>
> **Summary**
>
> Replaced the uniform **0.125 µm** placeholder radius on every compartment of
> `dsgc-baseline-morphology` with a Poleg-Polsky & Diamond 2016 per-Strahler-order taper,
> registered
> as the new dataset asset `dsgc-baseline-morphology-calibrated`. Topology is preserved
> byte-for-byte
> (**6,736** compartments, **129** branch points, **131** leaves, **1,536.25 µm** dendritic
> length)
> while total dendritic surface area grows **7.99x** and total dendritic axial resistance
> drops to
> **~4.8%** of the placeholder baseline.
>
> **Metrics**
>
> * **Distinct radii (calibrated)**: 4 — soma **4.118 µm**, primary **3.694 µm** (Strahler
>   order
> 5), mid **1.653 µm** (orders 2-4), terminal **0.439 µm** (order 1)
> * **Max Strahler order**: 5 (max-child tie-break, 33 order-5 compartments, 3,915 terminals)
> * **Terminal clamps at 0.15 µm floor**: **0** (Poleg-Polsky terminal mean is 2.9x the floor)
> * **Surface area**: placeholder **1,213.43 µm²** -> calibrated **9,700.10 µm²** (**+7.99x**)
> * **Dendritic axial resistance**: placeholder **3.13e10 Ohm** -> calibrated **1.50e9 Ohm**
> (**4.79%**, a **20.9x** drop)

</details>

<details>
<summary>✅ 0007 — <strong>Install and validate NEURON 8.2.7 + NetPyNE 1.1.1
toolchain</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0007_install_neuron_netpyne` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0003-01` |
| **Task types** | [`infrastructure-setup`](../../../meta/task_types/infrastructure-setup/) |
| **Start time** | 2026-04-19T18:20:22Z |
| **End time** | 2026-04-19T22:43:38Z |
| **Step progress** | 10/15 |
| **Task page** | [Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Task folder** | [`t0007_install_neuron_netpyne/`](../../../tasks/t0007_install_neuron_netpyne/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0007_install_neuron_netpyne/results/results_detailed.md) |

# Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain

## Motivation

The t0003 simulator survey selected **NEURON 8.2.7** (paired with **NetPyNE 1.1.1**) as the
project's primary compartmental simulator, but did not install it. Every downstream
compartmental- modelling task (ModelDB 189347 port, diameter calibration verification,
missed-models hunt, visualisation smoke-test against a running simulation, tuning-curve
scoring) needs a validated NEURON+NetPyNE environment. This task does the install, proves it
works end-to-end on a trivial cell, and records the exact installed versions and any installer
warnings so later tasks can reproduce the environment deterministically.

Covers suggestion **S-0003-01**.

## Scope

1. Install NEURON 8.2.7 and NetPyNE 1.1.1 into the project's `uv` virtualenv: `uv pip install
   neuron==8.2.7 netpyne==1.1.1`.
2. Compile the bundled Hodgkin-Huxley MOD files with `nrnivmodl`. Record the compilation
   command, wall-clock, and any warnings.
3. Run a 1-compartment sanity simulation:
   * Create a single-section soma (L = 20 µm, diam = 20 µm) with `hh` inserted.
   * Inject a 0.5 nA step current for 50 ms, record membrane voltage.
   * Confirm at least one spike (V crosses +20 mV).
4. Repeat the same sanity simulation via NetPyNE's `specs.NetParams` +
   `sim.createSimulateAnalyze` harness to prove NetPyNE wraps NEURON correctly.
5. Record the final installed versions (`neuron.__version__`, `netpyne.__version__`, the
   NEURON `hoc` "about" string), the `nrnivmodl` output, the sanity-simulation wall-clocks,
   and any installer warnings into a single answer asset named
   `neuron-netpyne-install-report`.

## Dependencies

None — this task does not need any prior task's output.

## Expected Outputs

* **1 answer asset** (`assets/answer/neuron-netpyne-install-report/`) with:
  * `details.json` (question, categories, answer methods, source URLs for install commands)
  * `short_answer.md` (3-5 sentences: versions + "works" / "does not work" verdict)
  * `full_answer.md` (install log, sanity-simulation code, NEURON + NetPyNE voltage traces
    embedded as PNGs in `files/images/`, tabulated wall-clocks, every installer warning
    verbatim)

## Approach

Write a `code/install_and_validate.py` script that (a) shells out to `uv pip install`, (b)
shells out to `nrnivmodl` in the NEURON-bundled MOD directory, (c) runs the two sanity
simulations capturing voltage traces to CSV, and (d) produces the two PNG plots. Wrap every
CLI call with `run_with_logs.py`. Keep the sanity-simulation code deliberately minimal so the
answer asset also serves as a "hello world" reference for downstream tasks.

## Questions the task answers

1. Does `uv pip install neuron==8.2.7 netpyne==1.1.1` succeed on this workstation?
2. Does `nrnivmodl` compile the bundled HH MOD files without errors?
3. Does a 1-compartment soma with `hh` fire at least one action potential under a 0.5 nA step?
4. Does NetPyNE's wrapper produce the same voltage trace as raw NEURON on the same cell?
5. What are the exact installed versions, and what warnings (if any) surfaced during install
   or compilation?

## Risks and Fallbacks

* If NEURON 8.2.7 wheels are unavailable for this Python version, fall back to the nearest
  supported patch release and record the substitution in the answer asset.
* If NetPyNE pins an older NEURON release, use the NetPyNE-required version and record the
  override.
* If `nrnivmodl` needs `gcc`/`clang` that is not on PATH, create an intervention file
  requesting the compiler toolchain instead of silently skipping MOD compilation.

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0007_install_neuron_netpyne"
> date_completed: "2026-04-19"
> ---
> **Results Summary: NEURON 8.2.7 + NetPyNE 1.1.1 install**
>
> **Summary**
>
> The NEURON 8.2.7 + NetPyNE 1.1.1 toolchain installs, compiles MOD files, and runs a
> single-compartment Hodgkin-Huxley sanity simulation end-to-end on the project's Windows 11
> workstation. Raw NEURON and NetPyNE sanity sims agree to machine precision at **v_max =
> 42.003 mV**,
> confirming the stack is ready for downstream modelling tasks (t0008, t0010, t0011).
>
> **Metrics**
>
> * Raw NEURON sanity sim: **v_max = 42.003 mV**, crossed +20 mV threshold, 3201 samples,
>   setup **6.7
> ms**, run **4.4 ms**.
> * NetPyNE sanity sim: **v_max = 42.003 mV**, crossed +20 mV threshold, 3201 samples, setup
>   **38.7
> ms**, run **4.8 ms**.

</details>

<details>
<summary>✅ 0006 — <strong>Brainstorm results session 2</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0006_brainstorm_results_2` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-19T09:30:00Z |
| **End time** | 2026-04-19T11:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 2](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md) |
| **Task folder** | [`t0006_brainstorm_results_2/`](../../../tasks/t0006_brainstorm_results_2/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0006_brainstorm_results_2/results/results_detailed.md) |

# Brainstorm Results Session 2

## Objective

Second brainstorming session for the neuron-channels project, held after the first wave of
tasks (t0002-t0005) completed. The goal is to translate the literature survey's quantitative
targets, the simulator recommendation, the canonical target tuning curve, and the baseline
morphology asset into a concrete tooling round that lets every downstream
compartmental-modelling experiment run without per-task re-implementation of shared machinery.

## Context

Going into this session:

* **t0002** produced a 20-paper corpus and an answer asset fixing quantitative targets: DSI
  **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM **60-90°**, **177
  AMPA + 177 GABA** synapses, g_Na **0.04-0.10 S/cm²**.
* **t0003** recommended **NEURON 8.2.7 + NetPyNE 1.1.1** as the primary simulator and **Arbor
  0.12.0** as backup; Brian2 and MOOSE were rejected.
* **t0004** generated the canonical `target-tuning-curve` dataset (cos²-half-rectified, DSI
  0.8824, HWHM 68.5°, 240-row CSV).
* **t0005** downloaded `dsgc-baseline-morphology` (NeuroMorpho 102976, Feller lab
  141009_Pair1DSGC; 6,736 compartments; 1,536.25 µm dendritic path). Two known caveats:
  placeholder uniform radius 0.125 µm, ambiguous source-paper attribution.
* 23 active uncovered suggestions, most concentrated on experiments that cannot run until the
  tooling exists.

No compartmental simulation has run yet.

## Session Outcome

Seven new tasks agreed with the researcher, all `status = not_started`:

* **t0007** — Install and validate NEURON 8.2.7 + NetPyNE 1.1.1. No dependencies.
* **t0008** — Port ModelDB 189347 and similar DSGC compartmental models to NEURON as library
  assets. Depends on t0007, t0005, t0009, t0012.
* **t0009** — Calibrate dendritic diameters on `dsgc-baseline-morphology`. Depends on t0005.
* **t0010** — Literature + code hunt for DSGC compartmental models missed by t0002 and t0008;
  port any found. Depends on t0008.
* **t0011** — Response-visualisation library (firing rate vs angle graphs). Depends on t0004
  and t0008.
* **t0012** — Tuning-curve scoring loss library. Depends on t0004.
* **t0013** — Resolve `dsgc-baseline-morphology` source-paper provenance and file a
  corrections asset. Depends on t0005.

t0007, t0009, t0012, and t0013 can run in parallel. t0008 gates t0010 and (partially) t0011.

## Corrections Filed

* **S-0004-03** → rejected (redundant with S-0002-09, now covered by t0012).
* **S-0005-04** → reprioritised HIGH → MEDIUM (NEURON loader absorbed into t0008;
  multi-simulator translator only needed once Arbor benchmarking starts).

## Researcher Preferences Captured

* Block t0008 on t0009 — use the calibrated morphology, not the placeholder-radius version.
* t0011 smoke-tests visualisation against both the canonical `target-tuning-curve` and
  whatever t0008 produces.
* Leave `project/budget.json` untouched at `$0.00 / no paid services`; everything runs
  locally.
* Defer the dendritic-diameter calibration source choice (Vaney/Sivyer/Taylor 2012 vs
  Poleg-Polsky 2016 vs other) to t0009's research stage rather than pinning it up front.
* Build a proper scoring library (S-0002-09 covered by t0012), not an ad-hoc inline check
  inside t0008.

**Results summary:**

> **Results Summary: Brainstorm Session 2**
>
> **Summary**
>
> Second brainstorming session for the neuron-channels project. Produced seven second-wave
> task
> folders (t0007-t0013) covering NEURON+NetPyNE installation, ModelDB 189347 port plus
> sibling-model
> port, dendritic-diameter calibration, model hunt, response visualisation, tuning-curve
> scoring, and
> morphology source-paper provenance. Filed two suggestion corrections.
>
> **Session Overview**
>
> * **Date**: 2026-04-19
> * **Context**: First task wave (t0002-t0005) completed. Quantitative targets established
>   (DSI
> 0.7-0.85, peak 40-80 Hz, null < 10 Hz, HWHM 60-90°); simulator choice converged on NEURON
> 8.2.7 +
> NetPyNE 1.1.1; canonical target-tuning-curve dataset generated; baseline morphology
> 141009_Pair1DSGC downloaded with two open issues (placeholder radii; ambiguous source
> paper).
> * **Prompt**: Researcher invoked `/human-brainstorm` and laid out a three-step high-level
>   goal:
> install NEURON+NetPyNE, port ModelDB 189347 and similar compartmental DSGC models, then hunt
> literature for missed models, then add response-visualisation and tuning-curve-scoring
> support
> libraries.

</details>

<details>
<summary>✅ 0005 — <strong>Download candidate DSGC morphology</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0005_download_dsgc_morphology` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Expected assets** | 1 dataset |
| **Source suggestion** | — |
| **Task types** | [`download-dataset`](../../../meta/task_types/download-dataset/) |
| **Start time** | 2026-04-19T08:50:24Z |
| **End time** | 2026-04-19T09:28:00Z |
| **Step progress** | 8/15 |
| **Task page** | [Download candidate DSGC morphology](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Task folder** | [`t0005_download_dsgc_morphology/`](../../../tasks/t0005_download_dsgc_morphology/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0005_download_dsgc_morphology/results/results_detailed.md) |

# Download candidate DSGC morphology

## Motivation

Every downstream simulation task needs a concrete reconstructed morphology to load. Rather
than generating a synthetic branching structure, we want a published DSGC (or DSGC-like RGC)
reconstruction used by prior modelling work. The literature survey (t0002) produces the
shortlist; this task commits to one file.

## Scope

Download one reconstructed DSGC morphology in SWC format (or HOC / NeuroML if SWC is not
available) from a public source such as NeuroMorpho.org, ModelDB, or a paper's supplementary
materials. The morphology should be one of those flagged as suitable in t0002's answer asset.

## Approach

1. Read t0002's answer asset to pick the recommended morphology.
2. Download the file and verify it loads as a valid SWC / HOC structure.
3. Record its provenance (source URL, paper DOI, reconstruction protocol) in the dataset asset
   metadata.

## Expected Outputs

* One dataset asset under `assets/dataset/dsgc_baseline_morphology/` containing the morphology
  file(s) and metadata.

## Compute and Budget

No external cost.

## Dependencies

`t0002_literature_survey_dsgc_compartmental_models` — the literature survey produces the
morphology shortlist and rationale.

## Verification Criteria

* Dataset asset passes `verify_dataset_asset.py`.
* The asset's `details.json` links back to the source paper or NeuroMorpho record.
* The downloaded file loads without errors in at least one candidate simulator library.

**Results summary:**

> **Results Summary: Download candidate DSGC morphology**
>
> **Summary**
>
> Downloaded the Feller-lab ON-OFF mouse DSGC reconstruction `141009_Pair1DSGC` (NeuroMorpho
> neuron
> 102976\) from Morrie & Feller-associated archives as a CNG-curated SWC, validated the
> compartment
> tree with a stdlib Python parser, and registered it as the project's baseline DSGC dataset
> asset
> `dsgc-baseline-morphology` (v2 spec-compliant). The morphology is now the single
> reconstructed cell
> that every downstream compartmental-modelling task in this project will load.
>
> **Metrics**
>
> * **Compartments**: **6,736** (19 soma, 6,717 dendrite, 0 axon)
> * **Branch points (≥2 children)**: **129**
> * **Leaf tips**: **131**
> * **Total dendritic path length**: **1,536.25 µm**
> * **SWC file size**: **232,470 bytes** (CNG-curated)
> * **Download cost**: **$0** (CC-BY-4.0 public data)
>
> **Verification**

</details>

<details>
<summary>✅ 0004 — <strong>Generate canonical target angle-to-AP-rate tuning
curve</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0004_generate_target_tuning_curve` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | — |
| **Task types** | [`feature-engineering`](../../../meta/task_types/feature-engineering/) |
| **Start time** | 2026-04-19T08:12:46Z |
| **End time** | 2026-04-19T08:42:30Z |
| **Step progress** | 8/15 |
| **Task page** | [Generate canonical target angle-to-AP-rate tuning curve](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Task folder** | [`t0004_generate_target_tuning_curve/`](../../../tasks/t0004_generate_target_tuning_curve/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0004_generate_target_tuning_curve/results/results_detailed.md) |

# Generate canonical target angle-to-AP-rate tuning curve

## Motivation

The key project metric `tuning_curve_rmse` compares a simulated angle-to-AP-rate tuning curve
against a target. The researcher chose to **simulate** a canonical target curve rather than
digitise one from a paper. This task generates that canonical target and registers it as a
dataset asset so all later optimisation tasks share one fixed reference.

## Scope

Produce a single dataset asset containing:

* A cosine-like target tuning curve sampled at 12 or 24 angles around 360°.
* Explicit generator parameters: preferred direction (deg), baseline rate (Hz), peak rate
  (Hz), tuning half-width (deg or von Mises κ), and random seed.
* Per-angle mean rates plus a small number of synthetic noisy trial replicates so the
  `tuning_curve_reliability` metric has a well-defined ground-truth value.

Suggested functional form:

```
r(θ) = r_base + (r_peak - r_base) * ((1 + cos(θ - θ_pref)) / 2) ** n
```

with `n` controlling sharpness. Any equivalent von Mises formulation is fine. The exact values
of `r_base`, `r_peak`, `θ_pref`, and `n` should be chosen to give a biologically plausible DSI
(roughly 0.6-0.9) and reported in the dataset's `details.json`.

## Approach

1. Write a small Python script under `code/` that generates the curve, saves it to `data/` as
   CSV or JSON, and writes the dataset asset folder under `assets/dataset/`.
2. Include both a mean-rate table and a per-trial table (e.g., 20 synthetic trials) so
   `tuning_curve_reliability` has a real reference value.
3. Plot the curve and save to `results/images/target_tuning_curve.png`.

## Expected Outputs

* One dataset asset under `assets/dataset/target_tuning_curve/` containing the CSV/JSON
  tables, metadata, and description.
* A plot of the target curve in `results/images/`.

## Compute and Budget

Trivial. Runs locally in seconds; no external cost.

## Dependencies

None. Runs in parallel with t0002 and t0003. This task is the reference any later optimisation
task will compare against.

## Verification Criteria

* Dataset asset passes `verify_dataset_asset.py`.
* `details.json` records the generator parameters and random seed explicitly.
* The generated CSV/JSON has one row per angle and the noisy-trial table has at least 10
  trials per angle.

**Results summary:**

> **Results Summary: Generate Canonical Target Tuning Curve**
>
> **Summary**
>
> Synthesised the canonical direction tuning curve `target-tuning-curve` from a closed-form
> half-wave-rectified cosine raised to power `n = 2` with `θ_pref = 90°`, `r_base = 2 Hz`,
> `r_peak = 32 Hz`, and 20 Gaussian-noise trials per angle (`σ = 3 Hz`, seed `42`). The asset
> is
> registered under `assets/dataset/target-tuning-curve/` with explicit generator parameters
> and a
> diagnostic plot.
>
> **Metrics**
>
> * **Direction Selectivity Index (DSI)**: **0.8824** — inside the required [0.6, 0.9] band
> * **Tuning curve HWHM**: **68.5°** — computed from the closed-form curve
> * **Sampled directions**: **12** angles at 30° spacing (0° to 330°)
> * **Trials per direction**: **20** (240 rows total in `curve_trials.csv`)
> * **Mean absolute bias (sample vs closed form)**: **0.419 Hz** (max 1.063 Hz)
>
> **Verification**
>

</details>

<details>
<summary>✅ 0003 — <strong>Simulator library survey for DSGC compartmental
modelling</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0003_simulator_library_survey` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`internet-research`](../../../meta/task_types/internet-research/) |
| **Start time** | 2026-04-19T07:20:04Z |
| **End time** | 2026-04-19T08:05:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Simulator library survey for DSGC compartmental modelling](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Task folder** | [`t0003_simulator_library_survey/`](../../../tasks/t0003_simulator_library_survey/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0003_simulator_library_survey/results/results_detailed.md) |

# Simulator library survey for DSGC compartmental modelling

## Motivation

`project/description.md` mentions NEURON as the canonical simulator but the researcher wants
to evaluate several libraries before committing. A bad simulator choice locks the project into
poor cable-model fidelity, slow parameter sweeps, or brittle tooling for months. A short
survey up front prevents this.

## Scope

Evaluate the following candidate libraries:

* NEURON (plus NEURON+Python bindings)
* NetPyNE (higher-level NEURON wrapper)
* Brian2 with cable-model extensions
* MOOSE
* Arbor

For each library, collect:

1. **Cable-model fidelity** — does it solve the full compartmental cable equation, support
   voltage-gated conductances in arbitrary compartments, and handle reconstructed morphologies
   (SWC, HOC, NeuroML)?
2. **Python ergonomics** — pure Python vs wrapped C++/MOD files, packaging on `uv`, quality of
   current documentation and examples.
3. **Speed and parallelism** — single-cell simulation speed and support for running large
   parameter sweeps.
4. **DSGC examples available** — whether any published DSGC or broader RGC compartmental model
   has been released in that library.
5. **Long-term maintenance** — last release, community activity, active maintainers.

## Approach

1. Run `/research-internet` to gather documentation, benchmarks, and user reports for each
   library.
2. Build a comparison table covering the five axes above.
3. Produce a single answer asset that recommends a **primary** simulator plus one **backup**,
   with explicit rationale.

## Expected Outputs

* One answer asset under `assets/answer/` summarising the library comparison and stating the
  primary plus backup recommendation.

## Compute and Budget

No external cost. Local LLM CLI and internet search only.

## Dependencies

None. Runs in parallel with t0002 and t0004.

## Verification Criteria

* The answer asset passes `verify_answer_asset.py`.
* The `## Answer` section states the primary and backup simulator in one or two sentences.
* The full answer includes the five-axis comparison table for every candidate library.

**Results summary:**

> **Results Summary: Simulator Library Survey for DSGC Compartmental Modelling**
>
> **Summary**
>
> Produced a single answer asset recommending **NEURON 8.2.7** (paired with **NetPyNE 1.1.1**
> for
> parameter sweeps) as the project's primary compartmental simulator and **Arbor 0.12.0** as
> backup,
> after surveying five candidate libraries (NEURON, NetPyNE, Brian2, MOOSE, Arbor) on five
> axes
> (cable-model fidelity, Python ergonomics, speed and parallelism, DSGC/RGC example
> availability,
> long-term maintenance). Brian2 and MOOSE were rejected with grounded evidence. The full
> answer
> embeds a 5-row × 5-column comparison table backed by 20 indexed internet sources.
>
> **Metrics**
>
> * **Libraries evaluated**: 5 (NEURON, NetPyNE, Brian2, MOOSE, Arbor)
> * **Evaluation axes**: 5 (cable-model fidelity, Python ergonomics, speed and parallelism,
>   DSGC/RGC
> examples, long-term maintenance)
> * **Sources cited**: 20 URLs, including 4 newly discovered papers
> * **Answer assets produced**: 1 (`dsgc-compartmental-simulator-choice`)
> * **Task requirements satisfied**: 17 of 17 (REQ-1 through REQ-17)
> * **External cost incurred**: $0.00 (no paid APIs, no remote compute)

</details>

<details>
<summary>✅ 0002 — <strong>Literature survey: compartmental models of DS retinal
ganglion cells</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0002_literature_survey_dsgc_compartmental_models` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 20 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-18T22:28:59Z |
| **End time** | 2026-04-19T01:35:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Literature survey: compartmental models of DS retinal ganglion cells](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Task folder** | [`t0002_literature_survey_dsgc_compartmental_models/`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/results/results_detailed.md) |

# Literature survey: compartmental models of DS retinal ganglion cells

## Motivation

This is the project's first research task. Before building any simulation we need a shared
knowledge base of what prior compartmental modelling work has done on direction-selective
retinal ganglion cells (DSGCs) and what each of the project's five research questions (RQs)
looks like in the literature. The survey feeds every downstream task: the target tuning curve
generator (t0004) needs published tuning-curve shapes, the morphology download (t0005) needs a
shortlist of reconstructed DSGCs, and the later Na/K optimisation and active-vs-passive
dendrite experiments need candidate channel models and parameter ranges.

## Scope

Cover all five project research questions at survey level:

1. **RQ1 Na/K combinations** — how published DSGC and related RGC models parameterise somatic
   sodium and potassium conductances, and what combinations reproduce directional AP firing.
2. **RQ2 morphology sensitivity** — how branching pattern, dendritic diameter, and compartment
   length have been shown to affect DS tuning.
3. **RQ3 AMPA/GABA balance** — ratio and spatial distribution of excitatory and inhibitory
   inputs, and their measured effect on DS sharpness.
4. **RQ4 active vs passive dendrites** — evidence for dendritic voltage-gated conductances in
   DSGCs, and modelling studies that compare active with passive dendrites.
5. **RQ5 angle-to-AP-frequency tuning curves** — reported tuning-curve shapes, peak rates,
   half-widths, and null-direction suppression levels that can serve as optimisation targets.

Minimum breadth:

* Include the six references already listed in `project/description.md` (Barlow & Levick 1965,
  Hines & Carnevale 1997, Vaney/Sivyer/Taylor 2012, Poleg-Polsky & Diamond 2016,
  Oesch/Euler/Taylor 2005, Branco/Clark/Häusser 2010).
* Add at least 14 more papers found by internet search, spread across the five research
  questions.
* Prefer papers with a clearly described compartmental model, published morphology, or
  quantitative angle-to-rate measurements.

## Approach

1. Run `/research-papers` using the six seed references to build initial paper assets.
2. Run `/research-internet` to find additional compartmental DSGC modelling papers and any
   patch-clamp studies that report tuning curves.
3. Download each selected paper via `/download-paper` so every cited paper becomes a paper
   asset with a summary.
4. Produce one answer asset that synthesises, across all five RQs, what the existing
   literature says about how to structure the DSGC modelling problem and what numbers to aim
   for.

## Expected Outputs

* ~20 paper assets under `assets/paper/` (each with `details.json`, `summary.md`, and the
  paper file under `files/`).
* One answer asset under `assets/answer/` summarising how existing compartmental DSGC models
  structure the five research questions and what numerical targets they provide.

## Compute and Budget

No external cost. Local LLM CLI only; no paid APIs or remote machines.

## Dependencies

None. This is the first research task.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and explicitly addresses each of the five
  research questions.
* `compare_literature.md` is not required for a pure literature survey.

**Results summary:**

> **Results Summary: Literature Survey of Compartmental Models of DS Retinal Ganglion Cells**
>
> **Summary**
>
> Produced a 20-paper survey of compartmental models of direction-selective retinal ganglion
> cells
> (DSGCs) covering all five project research questions, plus one synthesis answer asset that
> integrates the findings with per-RQ quantitative targets. The corpus includes all six seed
> references from `project/description.md` and 14 additional peer-reviewed papers spread
> across the
> five RQs, and it establishes concrete numerical targets (DSI **0.7-0.85**, preferred peak
> **40-80
> Hz**, null residual **< 10 Hz**, half-width **60-90 deg**, **177 AMPA + 177 GABA** synapses,
> g_Na
> **0.04-0.10 S/cm^2**) that downstream compartmental-modelling tasks must reproduce.
>
> **Metrics**
>
> * **Paper assets produced**: **20** (6 seeds + 14 additional, matches
>   `expected_assets.paper=20`)
> * **Answer assets produced**: **1** (matches `expected_assets.answer=1`)
> * **Papers with downloaded full text**: **17** (PDF/XML/markdown)
> * **Papers with metadata-only assets**: **3** (Chen2009, Sivyer2010, Sethuramanujam2016, all
> paywalled, `download_status: "failed"` per spec v3)
> * **RQ coverage by non-seed papers**: RQ1 **2**, RQ2 **3**, RQ3 **7**, RQ4 **3**, RQ5 **4**
>   — every

</details>

<details>
<summary>✅ 0001 — <strong>Brainstorm results session 1</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0001_brainstorm_results_1` |
| **Status** | completed |
| **Effective date** | 2026-04-18 |
| **Dependencies** | — |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-18T00:00:00Z |
| **End time** | 2026-04-18T00:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 1](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md) |
| **Task folder** | [`t0001_brainstorm_results_1/`](../../../tasks/t0001_brainstorm_results_1/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0001_brainstorm_results_1/results/results_detailed.md) |

# Brainstorm Results Session 1

## Objective

Run the first brainstorming session for the neuron-channels project, held immediately after
`/setup-project` completed. The goal is to translate `project/description.md` into a concrete
first wave of tasks that the researcher can execute autonomously.

## Context

The project is brand-new. After setup, the repository contains:

* `project/description.md` with five research questions about the electrophysiological basis
  of retinal direction selectivity, and success criteria centred on a modifiable compartmental
  model and a good fit to a target angle-to-AP-frequency tuning curve.
* `project/budget.json` with zero budget and no paid services.
* Eight project categories and four registered metrics (`tuning_curve_rmse` as the key
  metric).
* No existing tasks, suggestions, answers, or results.

## Session Outcome

The session produced four first-wave task folders, all with `status = not_started`:

* `t0002_literature_survey_dsgc_compartmental_models` — one broad literature survey covering
  all five research questions.
* `t0003_simulator_library_survey` — compare NEURON, NetPyNE, Brian2, MOOSE, Arbor, and pick a
  primary + backup simulator.
* `t0004_generate_target_tuning_curve` — analytically generate a canonical cosine-like target
  angle-to-AP-rate curve as the optimisation reference.
* `t0005_download_dsgc_morphology` — download a reconstructed DSGC morphology (depends on
  t0002).

T0002, t0003, and t0004 are independent and can run in parallel. T0005 waits on t0002's
morphology shortlist.

## Researcher Preferences Captured

* Target tuning curve will be simulated with a canonical cosine-like shape, not digitised from
  any published figure.
* The project will try several simulator libraries, not commit to NEURON alone up front.
* One big literature survey rather than several narrow ones.
* Autonomous execution; the researcher does not need to gate each task plan.

**Results summary:**

> **Results Summary: Brainstorm Session 1**
>
> **Summary**
>
> First brainstorming session for the neuron-channels project. Produced four first-wave task
> folders
> (t0002-t0005) covering literature survey, simulator-library comparison, canonical target
> tuning
> curve generation, and DSGC morphology download. No suggestions were rejected, reprioritized,
> or
> created.
>
> **Session Overview**
>
> * **Date**: 2026-04-18
> * **Context**: Run immediately after `/setup-project` completed. Project state was empty: no
>   tasks,
> no suggestions, no answers, no costs, zero budget with no paid services.
> * **Prompt**: Phase 7 of `/setup-project` automatically chains `/human-brainstorm` to plan
>   the first
> tasks.
>
> **Decisions**
>
> 1. **Create t0002: literature survey of DSGC compartmental models** — one broad survey
>    covering

</details>
