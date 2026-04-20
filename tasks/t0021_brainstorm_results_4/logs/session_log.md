---
spec_version: "3"
task_id: "t0021_brainstorm_results_4"
---
# Brainstorm Session 4 — Researcher-AI Transcript

## Session Context

Fourth brainstorm of the project. Called after the t0020 diagnostic merged, which confirmed that the
`modeldb_189347_dsgc` port from t0008 runs correctly under the native Poleg-Polsky protocol (DSI
0.7838 inside envelope) but with peak firing rate 14.85 Hz below the [40, 80] Hz envelope. The five
literature surveys t0015-t0019 (planned by t0014) had also delivered their answer-asset blueprints.
The researcher called this session to pick the next experimental wave.

## Project State Presented

* **Tasks**: 20 total, all completed. No in-progress or not-started work left.
* **Suggestions**: 82 active uncovered — 29 high, 41 medium, 12 low.
* **Budget**: $0 spent of $1 dev-phase total. No threshold warnings.
* **Answer corpus (from t0015-t0019)**: five blueprint answers specifying AIS compartment,
  Nav1.6/Nav1.2/Kv1 channels, NMDARs with Mg2+ block, GABA_A shunting, E-I temporal co-tuning, SAC
  asymmetric inhibition.
* **Library assets**: `modeldb_189347_dsgc` (t0008, vetted by t0020), `response-visualization`
  (t0011), `tuning-curve-scoring` (t0012).
* **Diagnostic headline (t0020)**: DSI 0.7838 in envelope [0.70, 0.85]; peak 14.85 Hz below [40, 80]
  Hz envelope. Confirmed S-0008-02 hypothesis that t0008's low DSI was protocol mismatch, not a port
  bug.

**Gap**: no DSGC model that (a) shows DS via internal dendritic computation, (b) sweeps 8-12 angles,
(c) is wired for channel-swap experiments at the AIS.

## Clarification Questions

**AI**: Before proposing tasks, four clarifying questions. (1) Is the goal a channel-testing testbed
or a literature-matching DSGC model? They imply different success thresholds. (2) Must the testbed
reproduce the Poleg-Polsky peak firing rate envelope, or is DSI sufficient? (3) Any preference on
modify-existing vs. new port? (4) Should we prune suggestions this round or focus on model building?

**Researcher**: (1) Channel-testing testbed — we need a model where we can vary AIS channels and
see what happens. (2) DSI is enough; peak rate out of scope for now. DSI >= 0.5 acceptable. (3) Open
question — propose both and we decide. (4) Focus on model building; defer suggestion cleanup to
the next session.

## Discussion — Round 1: New Tasks

**AI** (proposals):

* **Option A** — Modify `modeldb_189347_dsgc` (t0008, vetted by t0020) to produce
  dendritic-computation DS via spatially-asymmetric inhibition across 12 angles, with a
  channel-modular AIS. Pros: leverages already-vetted library; one PR; faster. Cons: inherits
  Poleg-Polsky's architectural choices.
* **Option B** — Port Hanson 2019 DSGC as a fresh independent model. Pros: independent reference
  implementation; cleaner abstractions. Cons: unknown effort; no guarantee it reaches the DS goal
  any faster.
* **Option C** — Port de Rosenroll 2026 DSGC. Pros: most recent modelling assumptions. Cons: same
  effort uncertainty as B.

**Researcher**: Start with A (modify existing) because t0020 already proved the library is sound.
But keep B and C on the plan as deferred comparison ports — I want both Hanson and de Rosenroll in
the project as optional later comparisons. Don't run B or C until A tells us whether the
modify-existing path produces the testbed we need.

**AI**: Translating that into task shape: t0022 runs A (status `not_started`, active). t0023 runs B
(status `intervention_blocked`). t0024 runs C (status `intervention_blocked`). The
`intervention_blocked` status with an intervention file is the right shape — it keeps them in the
project record without starting them.

**Researcher**: Confirmed. Target for t0022 is DSI >= 0.5 on a 12-angle moving-bar sweep with
channel-modular AIS. Do not spend effort on peak firing rate matching.

**AI**: Task scope for t0022:

1. Take `modeldb_189347_dsgc` library asset as starting point.
2. Drive a 12-angle moving-bar sweep (every 30 degrees).
3. Impose spatially-asymmetric inhibition on the dendritic tree — DS should arise from internal
   dendritic computation, not solely from pre-synaptic SAC input asymmetry.
4. Add an AIS compartment wired for channel modularity per t0019 blueprint (Nav1.6/Nav1.2/Kv1) —
   each channel density becomes a parameter.
5. Measure DSI + per-angle firing rate. Success: DSI >= 0.5.

**Researcher**: That is the task. Add t0023 and t0024 as deferred shells now so they exist in the
task history.

## Discussion — Round 2: Suggestion Cleanup

**AI**: 82 active suggestions remain. Given the researcher's stated focus on model building, I
recommend deferring a full cleanup pass to the next brainstorm. Proceed?

**Researcher**: Yes, skip the cleanup this round.

## Discussion — Round 3: Confirmation

**AI** (summary of decisions):

1. Create t0022 (active, `not_started`): modify `modeldb_189347_dsgc` for dendritic-computation DS
   over 12 angles, channel-modular AIS, DSI >= 0.5 target.
2. Create t0023 (`intervention_blocked`): Hanson 2019 DSGC port, deferred pending t0022 results.
   Intervention file explains the deferral.
3. Create t0024 (`intervention_blocked`): de Rosenroll 2026 DSGC port, deferred pending t0022
   results. Intervention file explains the deferral.
4. No suggestion cleanup this round.
5. No new suggestions, no corrections, no new categories / metrics / task types.

**Researcher**: Confirmed. Proceed through Phase 5 and Phase 6 to merge.

## Decisions Summary

1. **t0022 — active**. Modify existing `modeldb_189347_dsgc` library asset for
   dendritic-computation DS over 12 angles with channel-modular AIS. DSI >= 0.5.
2. **t0023 — intervention_blocked**. Hanson 2019 port, deferred pending t0022.
3. **t0024 — intervention_blocked**. de Rosenroll 2026 port, deferred pending t0022.
4. **No suggestion cleanup this round.** 82-entry backlog revisited next brainstorm.
