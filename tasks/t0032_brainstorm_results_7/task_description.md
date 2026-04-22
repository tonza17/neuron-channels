# Brainstorm Results Session 7

## Motivation

Seventh strategic brainstorming session. Run on 2026-04-22, a few hours after t0028 (brainstorm
session 6) merged and queued the morphology-sweep wave (t0029, t0030, t0031). The researcher opened
a second, parallel planning thread focused on a much larger future ambition: a joint optimisation
over DSGC dendritic morphology and the top-10 voltage-gated channel types to maximise DSI.

The immediate purpose of this session is not to launch that optimisation, but to commission a
planning-and-costing task that answers: *is a full joint optimisation affordable on our Vast.ai GPU
budget, and how should it be organised?*

## Scope

* Review project state after the t0028 merge: 28 tasks completed, 1 in progress (t0029), 2 not
  started (t0030, t0031), 1 intervention_blocked (t0023); 107 uncovered suggestions (36 high / 55
  medium / 16 low); $0.00 / $1.00 budget used.
* Summarise t0026 (V_rest sweep) and t0027 (morphology-DS synthesis) as the strategic context the
  researcher is reacting to.
* Decide whether to open a parallel planning thread during the morphology-sweep wave.
* Decide on a single new task: a feasibility-and-costing plan for a large joint morphology + VGC
  DSI-maximisation optimisation on Vast.ai GPU.
* Capture the researcher's constraints (no internet research, active dendritic conductances,
  presynaptic inputs fixed, single-objective DSI, do not create the child optimiser task itself).

## Researcher Decisions

* **Open a parallel planning thread**: yes. Do not wait for the morphology-sweep wave (t0029, t0030,
  t0031) to complete.
* **New task**: exactly one task, scoping and costing a future joint morphology + top-10 VGC
  DSI-maximisation optimisation. The task is a **planner, not an optimiser** — it must not launch
  any optimisation runs.
* **Research scope**: downloaded paper corpus only. No internet search.
* **Biophysical assumptions** (locked in for the plan): active dendritic conductances, Poleg-Polsky
  2026 parameter backbone, top-10 voltage-gated channel types sourced from t0019, presynaptic inputs
  held fixed.
* **Objective**: DSI only. Future criteria (information content, energy, size constraints, Cajal's
  cytoplasm minimisation) are noted but explicitly out of scope for this plan.
* **Compute target**: Vast.ai GPU pricing as the primary cost reference. Evaluate CoreNEURON-on-GPU,
  surrogate-NN-on-GPU, and a Vast.ai many-core CPU comparator. Pick the cheapest viable strategy ×
  tier.
* **Suggestion backlog**: no rejections or reprioritisations this session. Pruning deferred.
* **Task updates**: none.

## New Task Created

The session authorised one child task, created via `/create-task` immediately after this
brainstorm-results folder was scaffolded. Task index is auto-assigned as 33 (strictly greater than
32 per the ordering invariant).

* **t0033** — Plan DSGC morphology + top-10 voltage-gated channel DSI-maximisation optimisation
  task; synthesise methodology from the downloaded paper corpus only; enumerate parameter counts and
  search-space sizes; estimate Vast.ai GPU wall-time and USD cost for 2-3 search strategies × 2-3
  GPU tiers; recommend the cheapest viable combination. Deliverable includes an answer asset
  capturing the cost envelope. Planning only — no optimiser runs, no child optimiser task spawned
  from this plan. Local CPU only, $0.

## Suggestion Cleanup

Zero suggestions rejected or reprioritised. Pruning of stale high-priority suggestions from the
t0015-t0019 literature surveys was raised in the AI's reassessment but the researcher did not
authorise any action this session.

## Task Updates

None. t0023 (Hanson2019 port) remains `intervention_blocked`. t0029 remains `in_progress` in its own
worktree. t0030 and t0031 remain `not_started`.

## Expected Assets

This brainstorm session produces no assets beyond the brainstorm-results task folder and its
downstream child task. `expected_assets` is `{}`.

## Dependencies

All 27 completed tasks up through t0028. t0029, t0030, t0031 are excluded because they are not yet
completed.
