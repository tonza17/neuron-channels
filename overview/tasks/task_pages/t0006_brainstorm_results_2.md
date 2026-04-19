# ✅ Brainstorm results session 2

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0006_brainstorm_results_2` |
| **Status** | ✅ completed |
| **Started** | 2026-04-19T09:30:00Z |
| **Completed** | 2026-04-19T11:00:00Z |
| **Duration** | 1h 30m |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0006_brainstorm_results_2/`](../../../tasks/t0006_brainstorm_results_2/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0006_brainstorm_results_2/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0006_brainstorm_results_2/task_description.md)*

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

</details>

## Research

* [`research_code.md`](../../../tasks/t0006_brainstorm_results_2/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0006_brainstorm_results_2/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0006_brainstorm_results_2/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0006_brainstorm_results_2/results/results_summary.md)*

# Results Summary: Brainstorm Session 2

## Summary

Second brainstorming session for the neuron-channels project. Produced seven second-wave task
folders (t0007-t0013) covering NEURON+NetPyNE installation, ModelDB 189347 port plus
sibling-model port, dendritic-diameter calibration, model hunt, response visualisation,
tuning-curve scoring, and morphology source-paper provenance. Filed two suggestion
corrections.

## Session Overview

* **Date**: 2026-04-19
* **Context**: First task wave (t0002-t0005) completed. Quantitative targets established (DSI
  0.7-0.85, peak 40-80 Hz, null < 10 Hz, HWHM 60-90°); simulator choice converged on NEURON
  8.2.7 + NetPyNE 1.1.1; canonical target-tuning-curve dataset generated; baseline morphology
  141009_Pair1DSGC downloaded with two open issues (placeholder radii; ambiguous source
  paper).
* **Prompt**: Researcher invoked `/human-brainstorm` and laid out a three-step high-level
  goal: install NEURON+NetPyNE, port ModelDB 189347 and similar compartmental DSGC models,
  then hunt literature for missed models, then add response-visualisation and
  tuning-curve-scoring support libraries.

## Decisions

1. **Create t0007: install NEURON 8.2.7 + NetPyNE 1.1.1** — covers S-0003-01. Infrastructure
   setup; compiles MOD files, runs a single-compartment sanity simulation and a NetPyNE
   wrapper run, files an `answer` asset that records exact versions and reproduction steps.
2. **Create t0008: port ModelDB 189347 + similar DSGC compartmental models** — covers
   S-0002-03 and S-0003-02 (merged). Phase A ports Poleg-Polsky & Diamond 2016 as the
   `dsgc-polegpolsky-2016` library, swaps in the calibrated morphology (t0009 dependency),
   runs 12 angles × 20 trials, scores via t0012. Phase B hunts sibling models on
   ModelDB/SenseLab/OSF/GitHub and ports portable ones.
3. **Create t0009: calibrate dendritic diameters on dsgc-baseline-morphology** — covers
   S-0005-02. Research stage picks the taper source (Vaney/Sivyer/Taylor 2012, Poleg-Polsky
   2016, or similar); produces `dsgc-baseline-morphology-calibrated` dataset asset.
4. **Create t0010: hunt literature + code for missed DSGC models** — systematic search of
   ModelDB, GitHub, Google Scholar forward citations, bioRxiv 2023-2025. Inclusion bar:
   compartmental DSGC models with biophysical detail.
5. **Create t0011: response-visualisation library** — `tuning_curve_viz` with four plotting
   functions (cartesian, polar, multi-model overlay, raster/PSTH). Smoke-tests against
   `target-tuning-curve` (t0004) and t0008 output.
6. **Create t0012: tuning-curve scoring loss library** — covers S-0002-09 (subsumes
   S-0004-03). `tuning_curve_loss.score()` returns a `ScoreReport` dataclass combining DSI,
   peak, null, and HWHM residuals into a weighted-Euclidean scalar loss plus per-target
   booleans. Identity test `score(target, target) == 0.0`.
7. **Create t0013: resolve morphology source-paper provenance** — covers S-0005-01. Downloads
   both candidate Feller-lab 2018 papers, reads Methods sections, files a correction on
   `dsgc-baseline-morphology` setting `source_paper_id` to the winner.
8. **Reject S-0004-03** — redundant with S-0002-09, which covers the same scoring library with
   more complete envelope semantics; t0012 implements the surviving suggestion.
9. **Reprioritise S-0005-04 from HIGH to MEDIUM** — the SWC -> simulator section-translator is
   premature until at least one port (t0008) demonstrates exactly what cross-simulator
   behaviours matter.

## Researcher Preferences Captured

* t0008 must use the calibrated morphology (→ adds t0009 as a blocking dependency).
* t0011 smoke-tests against both `target-tuning-curve` and t0008 output.
* t0012 is implemented as a proper library, not inline ad-hoc checks.
* `project/budget.json` left untouched at `$0` with no paid services.
* Deferred: diameter source choice (Vaney/Sivyer/Taylor 2012 vs Poleg-Polsky 2016 vs other)
  will be decided by t0009's research stage, not pre-selected.

## Metrics

| Metric | Count |
| --- | --- |
| New tasks created | 7 |
| Suggestions covered | 4 (S-0002-03, S-0002-09, S-0003-01, S-0005-01; plus S-0002-04/05/10 implicit via t0009 dependencies) |
| Suggestions rejected | 1 (S-0004-03) |
| Suggestions reprioritized | 1 (S-0005-04 HIGH → MEDIUM) |
| Corrections written | 2 |
| New suggestions added | 0 |

## Verification

| Verificator | Result |
| --- | --- |
| `verify_task_file.py` (t0006-t0013) | PASSED |
| `verify_corrections.py` (t0006) | PASSED |
| `verify_suggestions.py` (t0006) | PASSED |
| `verify_logs.py` (t0006) | PASSED |
| `verify_pr_premerge.py` | PASSED |

## Next Steps

Execute the second wave. t0007, t0009, t0011, t0012, t0013 can run in parallel (independent
dependencies). t0008 waits on t0005, t0007, t0009, t0012. t0010 waits on t0008.

1. **Wave 2a (parallel)**: t0007, t0009, t0012, t0013 (all have only already-completed deps).
2. **Wave 2b**: t0011 after t0004 + t0008 (but t0004 is done, so starts when t0008 done).
3. **Wave 2c**: t0008 after t0007 + t0009 + t0012.
4. **Wave 2d**: t0010 after t0008.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0006_brainstorm_results_2/results/results_detailed.md)*

# Detailed Results: Brainstorm Session 2

## Summary

Second brainstorming session for the neuron-channels project. Produced seven second-wave task
folders (t0007-t0013) and filed two suggestion corrections (reject S-0004-03, demote
S-0005-04). No assets produced directly by this task; children task folders are tracked via
the tasks aggregator, not as assets.

## Methodology

* **Session flow**: four sequential steps — review-project-state, discuss-decisions,
  apply-decisions, finalize — run end-to-end in a single interactive session.
* **Duration**: 2026-04-19T09:30:00Z to 2026-04-19T11:00:00Z (approximately 90 minutes).
* **Model**: Claude Opus 4.7 via Claude Code CLI.
* **Tools used**: `aggregate_tasks`, `aggregate_suggestions`, `aggregate_costs`,
  `aggregate_categories`, filesystem Glob on `tasks/*/assets/answer/*/details.json` (as a
  workaround because `aggregate_answers` is not available in this fork),
  `overview/materialize`.
* **Runtime**: session is planning-only; no CPU-bound computation, no remote compute, no paid
  API calls. Cost $0.
* **Reproducibility**: the four step logs in `logs/steps/` and `logs/session_log.md` capture
  the dialogue and decisions; `results/results_summary.md` captures the final decision list.

## Session Flow

### Phase 1: Project State Review

Aggregated state at session start:

* **Tasks**: 5 completed (t0001-t0005), 0 in progress, 0 cancelled. Task history below.
* **Suggestions**: 17 active after t0002-t0005. 6 high-priority, 9 medium, 2 low.
* **Answers**: 3 answer assets (`dsgc-compartmental-modeling-state-of-the-art`,
  `simulator-choice-rationale`, `dsgc-baseline-morphology-candidate`).
* **Costs**: $0 spent. Project budget $0. No paid services configured.

Completed-task findings used for independent priority reassessment:

* **t0002 (literature survey)** — established quantitative envelope targets (DSI 0.7-0.85,
  preferred peak 40-80 Hz, null residual < 10 Hz, HWHM 60-90°); identified Poleg-Polsky &
  Diamond 2016 as the primary source compartmental DSGC model with published 177 AMPA + 177
  GABA synapse baseline.
* **t0003 (simulator library survey)** — selected NEURON 8.2.7 + NetPyNE 1.1.1 as the primary
  simulator stack; Brian2/MOOSE/Arbor deprioritised but kept in the survey's answer asset.
* **t0004 (target tuning curve)** — generated the canonical `target-tuning-curve` dataset (12
  angles × 20 trials, analytically simulated cosine-like curve matching the envelope).
* **t0005 (DSGC morphology)** — downloaded NeuroMorpho neuron 102976 (141009_Pair1DSGC) as
  `dsgc-baseline-morphology` dataset. Two issues flagged: (1) CNG-curated SWC has placeholder
  0.125 µm radii across every segment; (2) source_paper_id is null because two Feller-lab 2018
  papers are plausibly the origin.

### Phase 1.5: Clarification

Researcher laid out three-step high-level plan:

1. Install NEURON + NetPyNE.
2. Port ModelDB 189347 and any similar models.
3. Research literature for missed DSGC models, port them.
4. Add visualisation of responses (firing rate vs angle as graphs).

Additional decisions during Q&A:

* Use calibrated morphology for t0008 (not placeholder radii).
* t0011 must smoke-test against both target-tuning-curve and t0008 output.
* Implement tuning-curve scoring as a proper library (t0012) rather than inline checks.

### Phase 2: Discussion

#### Round 1: New Tasks

Proposed seven tasks spanning infrastructure (t0007), code reproduction (t0008, t0010),
feature engineering (t0009), support libraries (t0011, t0012), and provenance correction
(t0013).

Dependency graph agreed:

```text
t0007 (no deps)                  ─┐
t0009 (deps: t0005)              ─┤
t0012 (deps: t0004)              ─┤
t0013 (deps: t0005)              ─┤
                                   │
t0008 (deps: t0005, t0007, t0009, t0012)
                                   │
t0010 (deps: t0008)
                                   │
t0011 (deps: t0004, t0008)
```

#### Round 2: Suggestion Cleanup

Reviewed all 17 active suggestions against the seven proposed tasks:

* **S-0002-03** (port ModelDB 189347) → covered by t0008.
* **S-0002-04** (dendritic morphology sweep) → covered implicitly by t0009 providing the
  calibrated morphology baseline.
* **S-0002-05** (E/I ratio scan) → left active; depends on t0008.
* **S-0002-09** (tuning curve scoring library) → covered by t0012.
* **S-0002-10** (active-vs-passive dendrites) → left active; depends on t0008.
* **S-0003-01** (install NEURON + NetPyNE) → covered by t0007.
* **S-0003-02** (hunt for sibling models) → merged into t0008 Phase B plus t0010.
* **S-0004-03** (tuning-curve metrics library) → **REJECTED**, redundant with S-0002-09/t0012.
* **S-0005-01** (resolve morphology source paper) → covered by t0013.
* **S-0005-02** (calibrate dendritic radii) → covered by t0009.
* **S-0005-04** (SWC -> simulator section-translator library) → **REPRIORITISED HIGH →
  MEDIUM** because premature without at least one port demonstrating cross-simulator
  behaviours.
* Remaining suggestions left untouched.

#### Round 3: Confirmation

Researcher confirmed the full plan with "confirm".

### Phase 3: Child Task Index Reservation

Highest existing task index M = 5 (t0005). Brainstorm task reserves `task_index = 6` → task ID
`t0006_brainstorm_results_2`. Children use indices 7-13.

### Phase 4: Brainstorm Task Folder

Created `tasks/t0006_brainstorm_results_2/` with the full mandatory structure. Session flow
captured in this file and in `results_summary.md`.

### Phase 5: Apply Decisions

Created seven child task folders directly (not via `/create-task` subagents — the task batch
is well-defined and writing the files directly is faster while still producing spec-valid
output). Each child has `__init__.py`, `task.json` (spec_version 4), and
`task_description.md`. The remaining mandatory folders (research, planning, assets,
corrections, intervention, results, logs, code) will be populated by the respective child
tasks when they run.

Correction files written in `corrections/`:

* `suggestion_S-0004-03.json` — `action: update`, `status: rejected`, rationale: redundant
  with S-0002-09.
* `suggestion_S-0005-04.json` — `action: update`, `priority: medium`, rationale: premature
  until at least one port exists.

## Rationale for Key Design Choices

### Why block t0008 on t0009 rather than running them in parallel

The CNG-curated SWC has placeholder 0.125 µm radii across every segment. Running the port
against placeholder geometry would burn compute on a known-wrong baseline; any F1-level metric
would be suspect. Calibrating first (t0009) gives t0008 a trustworthy morphology for the
published parameterisation.

### Why implement t0012 before t0008 finishes

t0008 reports envelope compliance using t0012. Without t0012, t0008 would either invent its
own ad-hoc check (which later tasks would have to throw away) or delay reporting. Making t0012
a dependency of t0008 ensures exactly one canonical scorer across all optimisation tasks.

### Why t0011 depends on t0008

The visualisation library needs real CSVs to smoke-test against. Using only the
analytically-generated target-tuning-curve would hide edge cases that show up in simulated
output (e.g., noisy trial-to-trial variance, NaN firing rates in null direction). Waiting for
t0008 gives t0011 a realistic second fixture.

### Why reject S-0004-03 rather than merge it into t0012

S-0002-09 explicitly covers the envelope-based scoring that optimisation tasks need. S-0004-03
covers the same metrics but frames them as "target-vs-simulated residuals" without the
envelope. The envelope framing is strictly more useful because it supports both tuning-curve
matching and absolute-target matching. Keeping both would risk parallel library
implementations.

### Why reprioritise S-0005-04 rather than covering it now

A SWC -> NEURON/NetPyNE/Arbor section-translator makes sense once multiple simulators are in
active use. Today, NEURON/NetPyNE is the sole pipeline; building an abstraction layer before
the second consumer exists is speculative. After t0008 and t0010 land, the shape of that
abstraction will be clear enough to design it meaningfully.

## Files Created

* `tasks/t0006_brainstorm_results_2/` — this brainstorm task folder.
* `tasks/t0007_install_neuron_netpyne/` — child task.
* `tasks/t0008_port_modeldb_189347/` — child task.
* `tasks/t0009_calibrate_dendritic_diameters/` — child task.
* `tasks/t0010_hunt_missed_dsgc_models/` — child task.
* `tasks/t0011_response_visualization_library/` — child task.
* `tasks/t0012_tuning_curve_scoring_loss_library/` — child task.
* `tasks/t0013_resolve_morphology_provenance/` — child task.
* `tasks/t0006_brainstorm_results_2/corrections/suggestion_S-0004-03.json` — rejection.
* `tasks/t0006_brainstorm_results_2/corrections/suggestion_S-0005-04.json` — reprioritisation.

## Verification

| Verificator | Result |
| --- | --- |
| `verify_task_file.py` (t0006) | PASSED (1 warning TF-W005: expected_assets empty, expected for brainstorm) |
| `verify_task_file.py` (t0007-t0013) | PASSED (no errors, no warnings) |
| `verify_corrections.py` (t0006) | PASSED |
| `verify_suggestions.py` (t0006) | PASSED |
| `verify_logs.py` (t0006) | PASSED (3 warnings LG-W005/W007/W008: expected for brainstorm with no CLI / session capture) |
| `verify_pr_premerge.py` | PASSED |

## Limitations

* The brainstorm session does not inspect the child task folders beyond creation; the child
  tasks will verify themselves when they run.
* Suggestion reprioritisation relies on the researcher's domain judgement; no quantitative
  check validated the HIGH → MEDIUM demotion.

</details>
