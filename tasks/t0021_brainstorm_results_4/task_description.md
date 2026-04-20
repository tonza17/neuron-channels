# Brainstorm Session 4 — DSGC Model Channel Testbed

## Context

The project has completed three task waves and reached a pivotal diagnostic milestone:

* **Wave 1** (t0001-t0005): foundational brainstorm, DSGC-focused compartmental-model literature
  survey, simulator survey, canonical target tuning curve, baseline DSGC morphology download.
* **Wave 2** (t0007-t0013, planned by t0006): NEURON install, a first port of ModelDB 189347
  (t0008), calibration, visualisation, scoring, and provenance tasks.
* **Wave 3** (t0015-t0019, planned by t0014): five category-scoped literature surveys producing five
  answer-asset blueprints covering AIS compartment, Nav1.6/Nav1.2/Kv1 channels, NMDARs with Mg2+
  block, GABA_A shunting, E-I temporal co-tuning, and SAC asymmetric inhibition.
* **Diagnostic task** (t0020): reproduced Poleg-Polsky 2016 DSGC under the native `gabaMOD` swap
  protocol and confirmed DSI 0.7838 (inside the envelope [0.70, 0.85]), while the peak firing rate
  14.85 Hz sits below the [40, 80] Hz envelope. This confirmed the t0008 `S-0008-02` hypothesis that
  the earlier low DSI was a protocol mismatch rather than a port bug.

The project now holds 20 tasks, 82 active suggestions (29 high, 41 medium, 12 low), and $0 spent
against a $1 dev-phase budget. The literature blueprints and a working (if under-firing) native port
are in place, but the project still lacks a DSGC model suitable for channel-mechanism testing.

## Session Goal

Decide the next experimental wave. The researcher framed the core gap: "we still lack a decent DSGC
model for testing different channels. It must (1) show DS via internal dendritic computation, (2)
cover 8-12 directions (not just PD/ND), (3) turn local activation+inhibition into spikes." A DSI
threshold of at least 0.5 is acceptable; peak firing rate need not match the Poleg-Polsky envelope.
The strategic question is whether to modify an existing model or port a new one.

## Decisions

1. **Create t0022** — modify the existing `modeldb_189347_dsgc` library asset produced by t0008 to
   produce dendritic-computation DS via spatially-asymmetric inhibition across a 12-angle moving-bar
   sweep, with a channel-modular AIS so future tasks can swap Nav/Kv variants. Status:
   `not_started`, runs immediately after this PR merges.

2. **Create t0023** — port the Hanson 2019 DSGC model as a comparison implementation alongside
   t0022. Status: `intervention_blocked`; an intervention file explains the task is deferred pending
   t0022 results before the porting effort is justified.

3. **Create t0024** — port the de Rosenroll 2026 DSGC model as a second comparison implementation.
   Status: `intervention_blocked`; an intervention file explains the same deferral rationale.

4. **No suggestion cleanup this round.** The researcher steered the session to model-building;
   suggestion backlog pruning is deferred to the next brainstorm.

## Out of Scope

* No experiments this session — planning-only brainstorm.
* No corrections — no prior task produced an outcome that needs correcting.
* No new asset types, task types, metrics, or categories.
