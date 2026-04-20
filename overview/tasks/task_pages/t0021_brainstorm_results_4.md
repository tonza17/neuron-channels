# ✅ Brainstorm Session 4: DSGC Model Channel Testbed

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0021_brainstorm_results_4` |
| **Status** | ✅ completed |
| **Started** | 2026-04-20T10:00:00Z |
| **Completed** | 2026-04-20T14:00:00Z |
| **Duration** | 4h 0m |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Step progress** | 4/4 |
| **Task folder** | [`t0021_brainstorm_results_4/`](../../../tasks/t0021_brainstorm_results_4/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0021_brainstorm_results_4/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0021_brainstorm_results_4/task_description.md)*

# Brainstorm Session 4 — DSGC Model Channel Testbed

## Context

The project has completed three task waves and reached a pivotal diagnostic milestone:

* **Wave 1** (t0001-t0005): foundational brainstorm, DSGC-focused compartmental-model
  literature survey, simulator survey, canonical target tuning curve, baseline DSGC morphology
  download.
* **Wave 2** (t0007-t0013, planned by t0006): NEURON install, a first port of ModelDB 189347
  (t0008), calibration, visualisation, scoring, and provenance tasks.
* **Wave 3** (t0015-t0019, planned by t0014): five category-scoped literature surveys
  producing five answer-asset blueprints covering AIS compartment, Nav1.6/Nav1.2/Kv1 channels,
  NMDARs with Mg2+ block, GABA_A shunting, E-I temporal co-tuning, and SAC asymmetric
  inhibition.
* **Diagnostic task** (t0020): reproduced Poleg-Polsky 2016 DSGC under the native `gabaMOD`
  swap protocol and confirmed DSI 0.7838 (inside the envelope [0.70, 0.85]), while the peak
  firing rate 14.85 Hz sits below the [40, 80] Hz envelope. This confirmed the t0008
  `S-0008-02` hypothesis that the earlier low DSI was a protocol mismatch rather than a port
  bug.

The project now holds 20 tasks, 82 active suggestions (29 high, 41 medium, 12 low), and $0
spent against a $1 dev-phase budget. The literature blueprints and a working (if under-firing)
native port are in place, but the project still lacks a DSGC model suitable for
channel-mechanism testing.

## Session Goal

Decide the next experimental wave. The researcher framed the core gap: "we still lack a decent
DSGC model for testing different channels. It must (1) show DS via internal dendritic
computation, (2) cover 8-12 directions (not just PD/ND), (3) turn local activation+inhibition
into spikes." A DSI threshold of at least 0.5 is acceptable; peak firing rate need not match
the Poleg-Polsky envelope. The strategic question is whether to modify an existing model or
port a new one.

## Decisions

1. **Create t0022** — modify the existing `modeldb_189347_dsgc` library asset produced by
   t0008 to produce dendritic-computation DS via spatially-asymmetric inhibition across a
   12-angle moving-bar sweep, with a channel-modular AIS so future tasks can swap Nav/Kv
   variants. Status: `not_started`, runs immediately after this PR merges.

2. **Create t0023** — port the Hanson 2019 DSGC model as a comparison implementation alongside
   t0022. Status: `intervention_blocked`; an intervention file explains the task is deferred
   pending t0022 results before the porting effort is justified.

3. **Create t0024** — port the de Rosenroll 2026 DSGC model as a second comparison
   implementation. Status: `intervention_blocked`; an intervention file explains the same
   deferral rationale.

4. **No suggestion cleanup this round.** The researcher steered the session to model-building;
   suggestion backlog pruning is deferred to the next brainstorm.

## Out of Scope

* No experiments this session — planning-only brainstorm.
* No corrections — no prior task produced an outcome that needs correcting.
* No new asset types, task types, metrics, or categories.

</details>

## Research

* [`research_code.md`](../../../tasks/t0021_brainstorm_results_4/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0021_brainstorm_results_4/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0021_brainstorm_results_4/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0021_brainstorm_results_4/results/results_summary.md)*

--- spec_version: "2" task_id: "t0021_brainstorm_results_4" ---
# Brainstorm Session 4 — Summary

## Summary

Fourth brainstorm of the project. Authorised three new tasks: t0022 (active) modifies the
existing `modeldb_189347_dsgc` library asset into a channel-modular DSGC testbed that produces
dendritic-computation DS over 12 bar angles, while t0023 (Hanson 2019 port) and t0024 (de
Rosenroll 2026 port) are created `intervention_blocked` and deferred pending t0022 results. No
suggestion cleanup this round.

## Session Overview

* **Date**: 2026-04-20
* **Duration**: 4 hours (10:00-14:00 UTC)
* **Prompt**: the researcher asked for a DSGC model suitable for channel-mechanism testing,
  triggered by the t0020 diagnostic (DSI 0.7838 in-envelope, peak 14.85 Hz below envelope,
  confirmed S-0008-02 protocol-mismatch hypothesis) and the five literature blueprints
  delivered by t0015-t0019. Project holds 20 tasks, 82 active suggestions (29 high / 41 medium
  / 12 low), $0 of $1 dev-phase budget spent.

## Decisions

1. **Create t0022** — modify the existing `modeldb_189347_dsgc` library asset (from t0008,
   vetted by t0020) to produce dendritic-computation DS via spatially-asymmetric inhibition
   across a 12-angle moving-bar sweep, with a channel-modular AIS. Rationale: t0020 already
   proved the library runs correctly under the native protocol; modifying it is cheaper than a
   fresh port and preserves continuity with the reference DSI envelope. DSI >= 0.5 accepted —
   peak firing rate matching is out of scope. Runs immediately after this PR merges.

2. **Create t0023** — port the Hanson 2019 DSGC model as an independent comparison
   implementation. Status: `intervention_blocked` with an intervention file explaining the
   deferral. Rationale: keep the option open for cross-model comparison without committing
   compute until t0022 produces either a usable testbed (then one comparison port is enough)
   or a clear failure mode (then porting strategy needs rethinking).

3. **Create t0024** — port the de Rosenroll 2026 DSGC model as a second comparison
   implementation. Status: `intervention_blocked` with the same deferral rationale as t0023.
   Rationale: same as t0023; de Rosenroll 2026 complements Hanson 2019 with more recent
   modelling assumptions.

4. **No suggestion cleanup this round.** The researcher focused the session on model building.
   The 82-entry backlog will be revisited in the next brainstorm.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created (active) | 1 |
| New tasks created (intervention_blocked) | 2 |
| Suggestions emitted | 0 |
| Suggestions rejected | 0 |
| Suggestions reprioritised | 0 |
| Corrections written | 0 |
| Intervention files written | 2 |
| Remote machines | 0 |
| Direct cost (USD) | 0.00 |

## Verification

* `verify_task_file t0021_brainstorm_results_4` — pending (expected: 1 warning TF-W005 for
  empty `expected_assets`).
* `verify_corrections t0021_brainstorm_results_4` — pending (expected: 0 errors, 0 warnings;
  no correction files created).
* `verify_suggestions t0021_brainstorm_results_4` — pending (expected: 0 errors, 0 warnings;
  no suggestions emitted).
* `verify_logs t0021_brainstorm_results_4` — pending (expected: 0 errors; possible LG-W005 /
  LG-W007 / LG-W008 depending on session capture).
* `verify_task_file` — pending for each of t0022, t0023, t0024.

## Next Steps

1. Execute t0022 immediately after this PR merges. Target: DSI >= 0.5 on a 12-angle moving-bar
   sweep with a channel-modular AIS scaffold.
2. Hold t0023 and t0024 until t0022 results are in. Unblock them by removing the intervention
   file or by creating follow-up correction / update tasks.
3. Defer the 82-suggestion backlog prune to the next brainstorm session.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0021_brainstorm_results_4/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0021_brainstorm_results_4" ---
# Brainstorm Session 4 — Detailed Results

## Summary

Fourth brainstorm session of the project. Authorised a three-task model-building wave: t0022
(active) modifies the existing `modeldb_189347_dsgc` library into a channel-modular DSGC
testbed that produces dendritic-computation DS over 12 bar angles, while t0023 (Hanson 2019
port) and t0024 (de Rosenroll 2026 port) are created `intervention_blocked` and deferred
pending t0022 results. A DSI threshold of at least 0.5 is the accepted success level; matching
the Poleg-Polsky peak-firing-rate envelope is explicitly out of scope. No suggestion cleanup
this round.

## Methodology

### Session Flow

The brainstorm followed the four canonical phases defined by `human-brainstorm` skill v8:

1. **Review project state** — ran `aggregate_tasks`, `aggregate_suggestions`,
   `aggregate_costs`, `aggregate_answers`; read `results/results_summary.md` for t0020 and for
   each of t0015-t0019; confirmed the project gap is "no DSGC model suitable for
   channel-mechanism testing."
2. **Discuss decisions** — the researcher gave strategic direction: the testbed must (1) show
   DS via internal dendritic computation, (2) cover 8-12 directions, (3) turn local
   activation+inhibition into spikes; DSI >= 0.5 is acceptable. Resolved modify-existing over
   new-port; authorised two comparison ports as deferred options.
3. **Apply decisions** — scaffolded the t0021 folder, created t0022 (not_started), t0023 and
   t0024 (intervention_blocked) with matching intervention files.
4. **Finalize** — wrote results documents, step logs, captured sessions, ran verificators,
   opened PR, merged.

### State of the Project at Session Start

* Tasks: 20 total — 20 completed, 0 in-progress, 0 not-started.
* Suggestions: 82 active uncovered (29 high, 41 medium, 12 low).
* Budget: `total_budget` 1.0 USD, spent 0.0 USD. No threshold warnings.
* Answer corpus: 5 blueprint answers from t0015-t0019 specifying AIS compartment,
  Nav1.6/Nav1.2/Kv1 channels, NMDARs with Mg2+ block, GABA_A shunting, E-I temporal co-tuning,
  and SAC asymmetric inhibition.
* Library assets: `modeldb_189347_dsgc` (t0008, vetted in t0020), `response-visualization`
  (t0011), `tuning-curve-scoring` (t0012).
* t0020 diagnostic: DSI 0.7838 inside envelope [0.70, 0.85] but peak 14.85 Hz below [40, 80]
  Hz envelope; confirmed S-0008-02 protocol-mismatch hypothesis.

### Gap Identified

The project now has the literature blueprints and a library asset that reproduces Poleg-Polsky
under its native protocol, but no model that (a) produces DS via internal dendritic
computation rather than via pre-synaptic SAC asymmetric-inhibition input, (b) sweeps 8-12
angles, and (c) is wired for channel-swap experiments at the AIS.

### Researcher Strategic Direction

Verbatim: "We still lack a decent DSGC model for testing different channels. It must (1) show
DS via internal dendritic computation, (2) cover 8-12 directions (not just PD/ND), (3) turn
local activation+inhibition into spikes. DSI >= 0.5 is acceptable. Modify existing or port
new?"

### Resolution

#### t0022 — Modify Existing (Active)

Take the `modeldb_189347_dsgc` library asset produced by t0008 and vetted in t0020. Modify it
to:

* Drive 12 equally-spaced bar angles (every 30 degrees) instead of the Poleg-Polsky PD-only
  sweep.
* Impose spatially-asymmetric inhibition on the dendritic tree so DS arises from internal
  dendritic computation, not solely from pre-synaptic SAC input asymmetry.
* Add an AIS compartment wired for channel modularity per the t0019 blueprint
  (Nav1.6/Nav1.2/Kv1), so channel swaps become parameter changes.
* Measure DSI and per-angle firing rate; target DSI >= 0.5.

Rationale: cheaper than a fresh port, preserves continuity with the t0020 reference-DSI
envelope, and de-risks the channel-swap infrastructure before committing compute to new ports.

#### t0023 — Hanson 2019 Port (Intervention Blocked)

Created as a second comparison implementation, but with status `intervention_blocked` and an
intervention file explaining the deferral. Will be unblocked once t0022 results indicate
whether a second independent implementation is worthwhile.

#### t0024 — de Rosenroll 2026 Port (Intervention Blocked)

Same rationale as t0023 with a more recent reference model. The parallel deferral lets the
researcher pick one of Hanson / de Rosenroll (or both) based on what t0022 reveals.

#### No Suggestion Cleanup

The session focused on model building. The 82-entry backlog will be pruned in the next
brainstorm.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created (active) | 1 |
| New tasks created (intervention_blocked) | 2 |
| Suggestions emitted | 0 |
| Suggestions rejected | 0 |
| Suggestions reprioritised | 0 |
| Corrections written | 0 |
| Intervention files written | 2 |
| Remote machines | 0 |
| Direct cost (USD) | 0.00 |

## Task Requirement Coverage

This is a planning-only brainstorm task. The `human-brainstorm` skill's requirements are:

* Four-phase flow executed: yes.
* Every decision recorded with rationale: yes (see Decisions in results_summary).
* Intervention files accompany every `intervention_blocked` task: yes (for t0023 and t0024).
* Session log preserves the researcher-AI exchange: yes (logs/session_log.md).

## Visualizations

Not applicable for a brainstorming task.

## Analysis / Discussion

Choosing modify-existing over new-port trades novelty for speed. The t0020 diagnostic already
showed that `modeldb_189347_dsgc` runs correctly under the native protocol — the only
shortfall was peak firing rate, which is out of scope for the testbed. A fresh Hanson or de
Rosenroll port would take an unknown number of task-weeks with no guaranteed payoff in DS
behaviour; the modify-existing route has a concrete first test it can pass or fail within
t0022's scope.

Creating the two comparison ports now, but blocked, is a deliberate hedge: the scaffolding
cost is one `/create-task` invocation each, and the intervention file keeps the option on the
radar. If t0022 cannot reach DSI >= 0.5 under spatially-asymmetric inhibition, the researcher
has a second path pre-authorised.

## Limitations

* No experiments — planning-only session.
* No suggestion backlog pruning — 82 suggestions remain active; deferred to next brainstorm.
* Intervention-blocked tasks need a follow-up researcher decision to unblock; they will not
  progress on their own.
* DSI >= 0.5 threshold is lenient compared to Poleg-Polsky's 0.7-0.85 envelope; a t0022 result
  at 0.5 is a testbed milestone, not a match to literature.

## Verification

* `verify_task_file t0021_brainstorm_results_4` — pending (expected: 1 warning TF-W005 for
  empty `expected_assets`).
* `verify_corrections t0021_brainstorm_results_4` — pending (expected: 0 errors, 0 warnings;
  no correction files created).
* `verify_suggestions t0021_brainstorm_results_4` — pending (expected: 0 errors, 0 warnings;
  no suggestions emitted).
* `verify_logs t0021_brainstorm_results_4` — pending (expected: 0 errors; possible LG-W005 /
  LG-W007 / LG-W008 depending on session capture).
* `verify_task_file` — pending for each of t0022, t0023, t0024.

## Files Created

### This Task

* `tasks/t0021_brainstorm_results_4/` — full brainstorm task folder with results, research
  placeholders, plan, step logs, and session log.

### Child Tasks Created

* `tasks/t0022_<slug>/` — active, `not_started`. Modify `modeldb_189347_dsgc` for
  dendritic-computation DS and channel-modular AIS.
* `tasks/t0023_<slug>/` — `intervention_blocked`. Hanson 2019 port, deferred pending t0022.
* `tasks/t0024_<slug>/` — `intervention_blocked`. de Rosenroll 2026 port, deferred pending
  t0022.

The exact slugs are chosen by `/create-task` from the task descriptions.

## Next Steps

1. Execute t0022 immediately after this PR merges. Target: DSI >= 0.5 on a 12-angle moving-bar
   sweep with a channel-modular AIS scaffold.
2. Hold t0023 and t0024 until t0022 results are in. Unblock them by removing the intervention
   file or by creating follow-up correction / update tasks.
3. Defer the 82-suggestion backlog prune to the next brainstorm session.

</details>
