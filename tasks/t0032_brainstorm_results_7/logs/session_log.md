# Brainstorm Session 7 — Full Transcript

## Project State Presented

**Current Execution State**

| Status | Count | Tasks |
| --- | --- | --- |
| Completed | 28 | t0001-t0022, t0024-t0028 |
| In progress | 1 | t0029 — distal-dendrite length sweep on t0022 (started today, folder has only `task.json` + description) |
| Not started | 2 | t0030 (distal-dendrite diameter sweep), t0031 (fetch paywalled Kim2014/Sivyer2013) |
| Intervention blocked | 1 | t0023 (Hanson2019 port — deferred pending t0022 outcomes) |

Budget: $0.00 / $1.00 spent. No paid services active. Note: t0028 merged only a few hours ago and
queued exactly t0029-t0031. We are effectively brainstorming on top of a freshly-planned wave.

**Key Findings From Recent Tasks**

*t0026 (V_rest sweep, 2026-04-21)* — striking divergence between the two DSGC ports:
- t0022 (deterministic ModelDB 189347): sharp DSI peak 0.6555 at V_rest = -60 mV, 14× modulation.
  Peak firing rate rises to 129 Hz at -30 mV then collapses to 26 Hz at -20 mV (Na inactivation).
  HWHM pinballs from 0.77° (near-binary) to 180° (no tuning).
- t0024 (de Rosenroll 2026, AR(2) noise ρ=0.6): U-shaped DSI 0.36-0.67, only 1.9× modulation. No
  Na-inactivation collapse. HWHM pinned 65-83° across the whole V_rest range.
- Two completely different mechanistic fingerprints — not yet explained.

*t0027 (morphology-DS literature synthesis, 20 papers)* — identified two competing mechanisms that
fit current t0022 data:
- Dan2018 passive transfer-resistance weighting: predicts DSI monotonically increases with
  distal-dendrite length.
- Sivyer2013 dendritic-spike branch independence: predicts DSI saturates with distal length.

t0029 (in_progress) is the length sweep designed to discriminate these; t0030 (queued) is the
diameter sweep.

**Suggestions Backlog**

107 uncovered suggestions total — 36 high / 55 medium / 16 low. AI's independent reassessment
flagged these as strategically important and uncovered:
1. S-0002-01 — Factorial (g_Na, g_K) grid search (RQ1 itself; uncovered).
2. S-0002-02 — Paired active-vs-passive dendrite experiment (RQ4; uncovered).
3. S-0026-06 — NMDA-block and TTX-block sweeps across V_rest (would explain t0022/t0024 divergence).
4. S-0026-02 — AR(2) ρ × V_rest sweep on t0024.
5. S-0027-02 — Swap sustained/transient bipolar kinetics on t0024.

Reassessed-down: 10 high-priority suggestions from t0015-t0019 literature surveys look lower-return
given the experimental pivot.

**Completed Answer Assets (11)**: strongest strategic artefacts are the t0027 morphology-DS
synthesis, t0019 Nav/Kv combinations, and the t0015-t0018 cable/dendritic/patch/synaptic priors. RQ1
(somatic Na/K) is well-surveyed but has no experimental answer yet.

## Clarification Questions

AI asked six questions:
1. Any notes, ideas, or context to guide the session?
2. Brainstorm now while t0029 is in_progress, or pause until t0029 and t0030 finish?
3. Ready to open a second research thread (RQ1 Na/K sweep or RQ4 active-vs-passive) in parallel with
   the morphology wave?
4. t0022 vs t0024 divergence — spin up a task now, or park it?
5. Aggressive backlog pruning of stale t0015-t0019 high-priority suggestions?
6. Session target: 1-2 focused tasks, or 3-5?

Researcher: "1"

AI: Asked whether that meant "no notes (proceeding to Q2-Q6)", "take questions one at a time", or
something else.

Researcher supplied a complete strategic direction in place of answering the clarifying questions
individually:

> I started thinking about an optimisation task in which I want to find optimal neuronal morphology
> and optimal channel combination to create highest DSI. There might be also other criteria — e.g.
> increase in information about the stimulus, decrease energy, some size constraints and also
> Cajal's cytoplasm minimisation. I need you to research the topic in terms of how such project can
> be organised. Only use our downloaded papers (so no extra internet search). Obviously, such jumbo
> task would require lots of resources so what I want to know is how much resources do I need and
> what is the estimated budget of this. I suggest you to count the number of parameters that need to
> be varied (like in Poleg-Polsky 2026 but add top 10 voltage-gated conductances). Assume active
> conductances in the dendrites but no variation on the presynaptic side. The goal of this task is
> to generate optimal neuron for 1. maximisation of DSI (ignore other parameters for now).
> Important! Do not build a task to do this. Just build the task that plans such optimisation and
> estimate the cost of GPU/CPU of such task.

Implicit answers: Q1 = the direction above; Q2 = brainstorm now; Q3 = parallel planning thread; Q6 =
1 task.

## Discussion — Round 1: New Tasks

AI proposed a task:
- Name: "Plan DSGC morphology + voltage-gated channel DSI optimisation; estimate compute budget".
- Types: literature-survey, answer-question.
- Dependencies: t0002, t0019, t0022, t0024, t0026, t0027.
- Constraints locked: downloaded papers only, active dendrites, presynaptic fixed, DSI objective.
- Deliverables: research_papers.md synthesis, results_detailed.md with parameter and cost tables,
  results_summary.md with headline budget, one answer asset.
- Compute for this task: local CPU, $0.
- Flagged: NEURON is natively CPU-bound. Task should evaluate CoreNEURON-on-GPU, surrogate-NN-on-
  GPU, and Vast.ai many-core CPU comparator to produce a true GPU budget.

Researcher: "No, I want to calculate the cost on GPU on remote machine. Use a standard remote GPU
service (I think the original project is tuned to use a specific service)"

AI confirmed via `arf/docs/explanation/remote_machines.md` that the project is configured for
**Vast.ai** as its remote GPU provider, with `arf/scripts/utils/vast_machines.py` as the
provisioning utility. Revised the task to anchor cost on Vast.ai GPU pricing specifically: evaluate
CoreNEURON-on-GPU, surrogate-NN-on-GPU, and a Vast.ai many-core CPU comparator across 2-3 Vast.ai
GPU tiers (e.g., RTX 4090, A100 40 GB, H100).

## Discussion — Round 2: Suggestion Cleanup

AI noted that 10 high-priority suggestions from t0015-t0019 literature surveys look lower-return
after the experimental pivot, and proposed reviewing them for reprioritisation.

Researcher: did not authorise any action. Backlog left intact.

## Discussion — Round 3: Confirmation

AI summarised the single decision:
1. Create t0032_brainstorm_results_7 (session container).
2. Create t0033_plan_dsgc_morphology_channel_optimisation with the revised Vast.ai scope.
3. No suggestions rejected or reprioritised.
4. No tasks cancelled or updated.

Researcher: "approve"

## Decisions Summary

1. **Open a parallel planning thread** while t0029 runs. No dependency on the morphology-sweep wave.
2. **Create t0033** — planner-and-cost-estimator for a future joint morphology + top-10 VGC
   DSI-maximisation optimisation. Types: literature-survey, answer-question. Dependencies: t0002,
   t0019, t0022, t0024, t0026, t0027. Downloaded papers only, active dendritic conductances,
   Poleg-Polsky 2026 backbone, top-10 channels from t0019, presynaptic inputs fixed, DSI objective.
   Vast.ai GPU cost anchor. Local CPU for the planning task, $0.
3. **Do not spawn the optimiser** — t0033 is a planner.
4. **No suggestion cleanup** this session; 107 backlog untouched.
5. **No task updates** — t0023 remains intervention_blocked; t0029 remains in_progress; t0030 and
   t0031 remain not_started.
