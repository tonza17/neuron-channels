# Detailed Results: Brainstorm Session 2

## Session Flow

### Phase 1: Project State Review

Aggregated state at session start:

* **Tasks**: 5 completed (t0001-t0005), 0 in progress, 0 cancelled. Task history below.
* **Suggestions**: 17 active after t0002-t0005. 6 high-priority, 9 medium, 2 low.
* **Answers**: 3 answer assets (`dsgc-compartmental-modeling-state-of-the-art`,
  `simulator-choice-rationale`, `dsgc-baseline-morphology-candidate`).
* **Costs**: $0 spent. Project budget $0. No paid services configured.

Completed-task findings used for independent priority reassessment:

* **t0002 (literature survey)** — established quantitative envelope targets (DSI 0.7-0.85, preferred
  peak 40-80 Hz, null residual < 10 Hz, HWHM 60-90°); identified Poleg-Polsky & Diamond 2016 as the
  primary source compartmental DSGC model with published 177 AMPA + 177 GABA synapse baseline.
* **t0003 (simulator library survey)** — selected NEURON 8.2.7 + NetPyNE 1.1.1 as the primary
  simulator stack; Brian2/MOOSE/Arbor deprioritised but kept in the survey's answer asset.
* **t0004 (target tuning curve)** — generated the canonical `target-tuning-curve` dataset (12 angles
  × 20 trials, analytically simulated cosine-like curve matching the envelope).
* **t0005 (DSGC morphology)** — downloaded NeuroMorpho neuron 102976 (141009_Pair1DSGC) as
  `dsgc-baseline-morphology` dataset. Two issues flagged: (1) CNG-curated SWC has placeholder 0.125
  µm radii across every segment; (2) source_paper_id is null because two Feller-lab 2018 papers are
  plausibly the origin.

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

Proposed seven tasks spanning infrastructure (t0007), code reproduction (t0008, t0010), feature
engineering (t0009), support libraries (t0011, t0012), and provenance correction (t0013).

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
* **S-0002-04** (dendritic morphology sweep) → covered implicitly by t0009 providing the calibrated
  morphology baseline.
* **S-0002-05** (E/I ratio scan) → left active; depends on t0008.
* **S-0002-09** (tuning curve scoring library) → covered by t0012.
* **S-0002-10** (active-vs-passive dendrites) → left active; depends on t0008.
* **S-0003-01** (install NEURON + NetPyNE) → covered by t0007.
* **S-0003-02** (hunt for sibling models) → merged into t0008 Phase B plus t0010.
* **S-0004-03** (tuning-curve metrics library) → **REJECTED**, redundant with S-0002-09/t0012.
* **S-0005-01** (resolve morphology source paper) → covered by t0013.
* **S-0005-02** (calibrate dendritic radii) → covered by t0009.
* **S-0005-04** (SWC -> simulator section-translator library) → **REPRIORITISED HIGH → MEDIUM**
  because premature without at least one port demonstrating cross-simulator behaviours.
* Remaining suggestions left untouched.

#### Round 3: Confirmation

Researcher confirmed the full plan with "confirm".

### Phase 3: Child Task Index Reservation

Highest existing task index M = 5 (t0005). Brainstorm task reserves `task_index = 6` → task ID
`t0006_brainstorm_results_2`. Children use indices 7-13.

### Phase 4: Brainstorm Task Folder

Created `tasks/t0006_brainstorm_results_2/` with the full mandatory structure. Session flow captured
in this file and in `results_summary.md`.

### Phase 5: Apply Decisions

Created seven child task folders directly (not via `/create-task` subagents — the task batch is
well-defined and writing the files directly is faster while still producing spec-valid output). Each
child has `__init__.py`, `task.json` (spec_version 4), and `task_description.md`. The remaining
mandatory folders (research, planning, assets, corrections, intervention, results, logs, code) will
be populated by the respective child tasks when they run.

Correction files written in `corrections/`:

* `suggestion_S-0004-03.json` — `action: update`, `status: rejected`, rationale: redundant with
  S-0002-09.
* `suggestion_S-0005-04.json` — `action: update`, `priority: medium`, rationale: premature until at
  least one port exists.

## Rationale for Key Design Choices

### Why block t0008 on t0009 rather than running them in parallel

The CNG-curated SWC has placeholder 0.125 µm radii across every segment. Running the port against
placeholder geometry would burn compute on a known-wrong baseline; any F1-level metric would be
suspect. Calibrating first (t0009) gives t0008 a trustworthy morphology for the published
parameterisation.

### Why implement t0012 before t0008 finishes

t0008 reports envelope compliance using t0012. Without t0012, t0008 would either invent its own
ad-hoc check (which later tasks would have to throw away) or delay reporting. Making t0012 a
dependency of t0008 ensures exactly one canonical scorer across all optimisation tasks.

### Why t0011 depends on t0008

The visualisation library needs real CSVs to smoke-test against. Using only the
analytically-generated target-tuning-curve would hide edge cases that show up in simulated output
(e.g., noisy trial-to-trial variance, NaN firing rates in null direction). Waiting for t0008 gives
t0011 a realistic second fixture.

### Why reject S-0004-03 rather than merge it into t0012

S-0002-09 explicitly covers the envelope-based scoring that optimisation tasks need. S-0004-03
covers the same metrics but frames them as "target-vs-simulated residuals" without the envelope. The
envelope framing is strictly more useful because it supports both tuning-curve matching and
absolute-target matching. Keeping both would risk parallel library implementations.

### Why reprioritise S-0005-04 rather than covering it now

A SWC -> NEURON/NetPyNE/Arbor section-translator makes sense once multiple simulators are in active
use. Today, NEURON/NetPyNE is the sole pipeline; building an abstraction layer before the second
consumer exists is speculative. After t0008 and t0010 land, the shape of that abstraction will be
clear enough to design it meaningfully.

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

## Limitations

* The brainstorm session does not inspect the child task folders beyond creation; the child tasks
  will verify themselves when they run.
* Suggestion reprioritisation relies on the researcher's domain judgement; no quantitative check
  validated the HIGH → MEDIUM demotion.
