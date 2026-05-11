# Brainstorm Session 21 — Full Transcript

This is the structured transcript of the Poleg-Polsky 2026 deep-dive brainstorming session that took
place on 2026-05-11. Some long tool outputs (PDF text extraction, aggregator JSON) are elided where
they would only repeat content already captured in the verified-numbers tables of
`results/results_detailed.md`; the elisions are marked `[elided — see results_detailed.md]`.

## Project State Presented

* 100 total tasks, 92 completed, 5 cancelled, 2 not-started, 1 intervention-blocked.
* Highest task_index: 100 (`t0100_fix_t0099_morph_charts`). Next brainstorm = t0101; next child task
  = t0102.
* Active (not-started / blocked): `t0023_port_hanson_2019_dsgc` (intervention),
  `t0031_fetch_paywalled_morphology_papers`, `t0075_bio_realistic_ais_param_sweep`. None block this
  brainstorm.
* Spend: $23.91 / $20.00 (119.5%) — `stop_threshold_reached: True`. `t0099` ($7.71) and `t0083`
  ($5.83) drove the overrun.
* Recent NSGA-II lineage: t0078 (BoTorch BO 49-d, $3.93, narrow miss) -> t0080 (NSGA-II 54-d pop=24,
  $0.75) -> t0081 (NSGA-II 54-d pop=96 warm-start, $2.39, joint-pass cell 767) -> t0083 (extension
  to gen 17, $5.83, 15 joint-pass cells) -> t0091 (NSGA-II 68-d joint electrophys+morphology,
  5-anchor warm-start, $0.65, 1 strict joint-pass cell) -> t0099 (3 random-init seeds 68-d, $7.71,
  zero strict joint-pass cells across 55 Pareto cells).

## Clarification Questions

The researcher started the session with a concrete request rather than asking for a brainstorming
review. Two clarification rounds were needed during the discussion (parameter knob interpretation
and substrate / starting condition); they are recorded in the discussion rounds below, not as
pre-discussion clarification.

## Discussion — Round 1: Poleg-Polsky 2026 Deep-Dive

**Researcher** (initial ask):

> Please dig the answers to the following questions about Poleg-Polsky 2026 paper:
> 1. How many and what parameters did they have?
> 2. Did they optimise for morphology and if yes, how many and what morphological parameters did
>    they have?
> 3. How many seeds did they have?
> 4. How many generations of optimisation did they have?
> 5. What are these novel direction selectivity mechanisms they are talking about?
> 6. What is their DSI?
> 7. How biologically realistic their parameters are?

**AI**: extracted answers from the PDF rather than the existing `summary.md` (which contained
fabricated claims). Verbatim findings:

1. **Parameters**: not a single global count. ~10-12 free parameters per presynaptic group (response
   delay 0-50 ms, center FWHM 10-200 um, surround FWHM > 10 um, four kinetic time constants,
   surround strength 0-1, depression/facilitation factors 0-1, synaptic weight, RF orientation,
   spatial position). 4 excitatory groups in most runs (40-48 params); +4 inhibitory groups when
   used (~88-96 params); +2 postsynaptic passive (passive g 1e-5-1e-3 S/cm^2, axial resistance
   50-200 ohm-cm). Unconstrained: ~90 free parameters.

2. **Morphology optimisation: NO**. 352-segment DSGC adapted from Poleg-Polsky and Diamond 2016
   (ModelDB 189347) plus a 69-segment cortical L2/3 reconstruction. Branching, segment lengths,
   diameters, tapering — none varied. Only two "morphology-adjacent" parameters (global passive g
   and axial resistance) optimised.

3. **Seeds**: minimum 50, typical 100 (figure captions consistently report N = 100 independently
   randomly seeded simulation runs per circuit configuration).

4. **Generations**: 300 typical, 1000 for low-performing configurations. Population = 10 NEURON
   models per generation (1 elite + 9 mutated; effectively a (1+9)-ES rather than a true GA).

5. **Novel mechanisms**: 8 computational primitives total, 4 novel. Classical: H&R (delay +
   compare), anti-H&R, B&L (delayed null-side inhibition), directionally-tuned inhibition.
   **Novel**: amplitude (synaptic-weight asymmetry alone), temporal-alignment (synchronising
   preferred-direction peaks via center-surround), anti-B&L (early inhibition preceding excitation
   in PD), pause-in-inhibition (inhibition troughs when excitation peaks in PD). **NOT in the
   paper**: "NMDA multiplicative gating", "velocity-dependent coincidence detection",
   "distance-graded delay lines" — despite our `summary.md` claiming these.

6. **DSI**: vector-sum DSI computed from **subthreshold somatic peak voltage** (not spikes), 12
   directions x 5 speeds. 2.4 +/- 0.1% (symmetric control), 22-28% for single-parameter excitation,
   50.8 +/- 0.8% (B&L weight only), 66.8 +/- 2.4% (inhibitory kinetic), 73.1 +/- 2.4% (fully
   unconstrained excitation + inhibition). Real DSGC spike DSI in vivo is ~70-90%.

7. **Biological realism**: morphology and bipolar count realistic; passive parameters fine (Rm ~2500
   ohm-cm^2, Cm 1 uF/cm^2, Vrest -60 mV, Ra 150 ohm-cm). Significant abstractions: no SAC, no real
   NMDA/AMPA/GABA, RFs are 2D Gaussians, RRP depression but no stochastic release, HH off by default
   (DSI from subthreshold V), no dendritic active channels varied, passive g range upper end (1e-3
   S/cm^2 = Rm ~1 kohm-cm^2) implausibly leaky.

**Flagged finding**: `summary.md` at
`tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md` has the
wrong title and lists fabricated novel primitives. Worth a downstream correction task.

## Discussion — Round 2: Comparison with Our Optimisations

**Researcher**: "How do 3 [seeds] and 4 [generations] differ from our optimisations?"

**AI**: produced the comparison table reproduced in `results/results_detailed.md`. Key points:

* PP uses 50-100 independent GA seed restarts per configuration; we use 1 (except t0099, which used
  3).
* PP uses 300 typical / 1000 max generations at pop=10; we use 8 typical / 17 max at pop=24-96.
* PP per-configuration candidate budget: ~300 000. Our largest single lineage (t0081+t0083): 1 728
  candidates.
* Per-candidate sim count: PP = 60 (deterministic, 12 dir x 5 speeds x 1 trial); ours = 160 (8 dir x
  20 trials).
* PP's per-sim cost is far lower (phenomenological RF, no real channel kinetics, HH off).

**Researcher**: "Do I understand correctly that each stimulus we apply 20 times?"

**AI**: confirmed via `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py:43` where
`N_SEEDS: int = 20`. These are **within-cell noise replicates** (averaging over AR(2) synaptic noise
with rho = 0.6), not GA-level seeds.

## Discussion — Round 3: New Task Design

**Researcher** (issuing the directive):

> I want you to reduce the number of seeds to 2 and number of trials by 5. Increase the number of
> gen to 20. Create a task and execute. Save the summary of our discussion as a brainstorm session.

**AI**: flagged ambiguity (the words "seeds" and "trials" map to multiple distinct knobs in our
code) and asked via `AskUserQuestion`.

**Researcher answer**: GA seeds = 2, N_SEEDS = 4 (factor of 5 reduction from 20), generations = 20.
Substrate = 68-d joint electrophys + morphology (extending t0099), random init (no warm-start).

## Discussion — Round 4: Budget Resolution

**AI**: before scaffolding, checked the project budget via `aggregate_costs` and surfaced the $3.91
overrun. Asked researcher how to handle.

**Researcher answer**: raise budget to $35 total, per-task default to $8, and proceed.

**AI**: committed `project/budget.json` change directly to main as `dd9ac77f` per the framework's
"infrastructure changes outside task folders" rule, then created the brainstorm branch from the
updated main.

## Decisions Summary

1. **Create t0102_seedscale_n4_gen20** — 68-d substrate, GA seeds=2 (random init, seeds 44 / 55),
   N_SEEDS=4, gens=20, pop=96, cost cap $8.

2. **Raise project budget** 20 -> 35 USD total, 5 -> 8 USD per-task (committed `dd9ac77f` on main).

3. **Record three new suggestions**:
   - S-0101-01 (high, evaluation): correct fabricated content in PP-2026 `summary.md`.
   - S-0101-02 (medium, library): lock N_SEEDS=4 default if t0102 scatter is acceptable.
   - S-0101-03 (medium, experiment): PP-style budget-matched ablation (few-seeds-many-gens vs
     many-seeds-few-gens).

4. **No suggestion rejections**, **no reprioritisations**, **no task cancellations** in this
   brainstorm.

## Open Items After This Brainstorm

* `t0102_seedscale_n4_gen20` must be scaffolded and executed in a separate task branch immediately
  after this brainstorm merges.
* The Poleg-Polsky 2026 `summary.md` correction (S-0101-01) should be picked up in a future sweep
  but does not block t0102.
* Re-running `aggregate_costs` after the budget bump should show `stop_threshold_reached` flipping
  back to `False` until t0102 completes.
