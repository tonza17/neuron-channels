# Brainstorm Session 1 — Full Transcript

## Project State Presented

Brand-new project. Task aggregator: 0 tasks. Suggestion aggregator: 0 uncovered suggestions. Answer
aggregator: 0 answers. Cost aggregator: total $0.00, budget $0.00, no paid services
(`available_services: []`).

`project/description.md` title: *Electrophysiological Basis of Retinal Direction Selectivity*. Five
research questions covering Na/K somatic conductances, morphology sensitivity, AMPA/GABA input
ratio, active-vs-passive dendrites, and residual error on the tuning-curve fit. Four success
criteria centred on a modifiable compartmental model and a good match to a target
angle-to-AP-frequency curve.

`meta/`: 8 categories (cable-theory, compartmental-modeling, dendritic-computation,
direction-selectivity, patch-clamp, retinal-ganglion-cell, synaptic-integration,
voltage-gated-channels), 4 metrics (`tuning_curve_rmse` [key], `direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`), 17 built-in task types, 6 built-in asset
types.

## Clarification Questions

**AI**: Before I propose specific first tasks, a few quick questions:

1. Published morphology source. Do you already have a candidate reconstructed DSGC morphology in
   mind (e.g., from NeuroMorpho.org, Poleg-Polsky & Diamond 2016's shared model on ModelDB, or the
   Taylor/Vaney lab reconstructions)? Or should task 1 explicitly include surveying and choosing
   one?
2. Target tuning curve source. Is the target angle-to-AP-frequency curve going to come from (a) a
   specific published figure you want to digitise, (b) a canonical cosine-like shape we choose
   analytically, or (c) patch-clamp data you already have access to?
3. NEURON-specific constraints. Is NEURON locked in as the simulator, or should we consider
   alternatives (NetPyNE, Brian2 with cable extensions) in an early tooling task?
4. First-task ambition. One big literature survey covering all five research questions, or 2-3
   smaller focused surveys?
5. Parallelism/autonomy. Happy for me to run tasks autonomously one after the other, or do you want
   to review each task's plan before it executes?

**Researcher**: 1 No. 2. Simulate data with canonical cosine like shape. 3. Use many different
libraries 4. a 5. Run autonomously

## Discussion — Round 1: New Tasks

**AI**: Proposed four tasks:

* **Task 1 (t0002) Literature survey — compartmental models of DS retinal ganglion cells** (task
  type `literature-survey`, no dependencies, no cost, expected ~20 papers + 1 answer asset). Covers
  all 5 research questions at survey level.
* **Task 2 (t0003) Simulator library survey** (`internet-research`, no dependencies, no cost, 1
  answer asset). Compare NEURON, NetPyNE, Brian2, MOOSE, Arbor, recommend a primary + backup.
* **Task 3 (t0004) Generate canonical target tuning curve** (`feature-engineering`, no dependencies,
  no cost, 1 dataset asset). Analytically construct a cosine-like target curve with explicit peak
  rate, baseline rate, width, and synthetic noisy trials so `tuning_curve_reliability` has a real
  reference value.
* **Task 4 (t0005) Download candidate DSGC morphology** (`download-dataset`, depends on t0002, no
  cost, 1 dataset asset).

Dependency graph: t0002, t0003, t0004 run in parallel; t0005 waits on t0002.

**Researcher**: create

## Discussion — Round 2: Suggestion Cleanup

**AI**: No existing suggestions to prune (fresh project). Nothing to do in this round.

**Researcher**: (implicit — skipped via `create`)

## Discussion — Round 3: Confirmation

**AI**: Summary of decisions:

* New tasks: t0002, t0003, t0004, t0005 as above.
* Suggestions rejected: none.
* Suggestions reprioritized: none.
* Tasks cancelled or updated: none.

**Researcher**: create (authorized creation of all four tasks and the remaining Phase 4-6 lifecycle
without further prompts).

## Decisions Summary

1. Create t0002: literature survey covering all 5 research questions.
2. Create t0003: simulator library survey of NEURON, NetPyNE, Brian2, MOOSE, Arbor.
3. Create t0004: analytically generate a canonical cosine-like target tuning curve.
4. Create t0005: download a candidate DSGC morphology after t0002 completes.
5. No suggestions rejected, reprioritized, or created.
6. Execute the first wave autonomously; no per-task plan gates.
