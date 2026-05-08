# Brainstorm Results Session 20

Twentieth strategic brainstorm, run on 2026-05-08 while t0091 (`morphology_extended_nsga2_v1`) is in
flight on Vast.ai. With the joint morphology + channel NSGA-II infrastructure now working
end-to-end, the researcher proposed a strategic broadening of the optimisation objective space.
Current MOBO runs maximise DSI and firing rate. The next research direction is to optimise DSI
jointly against a much wider set of biological objectives: information transfer rate, metabolic
energy / ATP per spike, cytoplasm volume, robustness, and other objectives surfaced by the
literature.

The session's only task is to commission a single consolidated literature survey of multi-objective
optimisation in single-neuron compartmental models, scoped broadly across any neuron type, with
formulas and computational recipes for each objective. Rejection of two already-covered suggestions
is included as housekeeping.

## Decisions

1. **Create t0096_literature_survey_multi_objective_neuron_optimisation**. A consolidated
   literature-survey + internet-research + answer-question task that catalogues every objective
   function used in the published multi-objective single-neuron optimisation literature, including:

   * Information-theoretic objectives (mutual information, Fisher information, channel capacity,
     stimulus-reconstruction MSE).
   * Metabolic / energy objectives (ATP per spike, total ionic flux, Na+/K+ pump cost, bits-per-ATP
     efficiency).
   * Structural objectives (total dendritic length, total membrane area, cytoplasm volume, wiring
     economy).
   * Robustness / degeneracy objectives (parameter-perturbation sensitivity, noise tolerance,
     Marder-style multi-conductance solution-space).
   * Temporal / coding objectives (latency, jitter, reliability, bandwidth, dynamic range).

   Coverage is broad: any neuron type, any species, any modality. Methodology papers (Druckmann
   2007/2011, BluePyOpt, Achard & De Schutter 2006, Rumbell et al., Van Geit / NeuroFitter) are in
   scope alongside biological objective-function origin papers (Attwell & Laughlin 2001, Niven &
   Laughlin 2008, Sengupta et al. 2010, Chklovskii, Cuntz et al. 2010, Marder & Goaillard 2006).
   Output deliverables: `research_papers.md`, `research_internet.md`, an answer asset catalogueing
   each objective with formula + units + NEURON-side computational recipe, and a `suggestions.json`
   proposing future MOBO tasks (DSI x ITR, DSI x ATP, DSI x volume, DSI x robustness) ranked by
   biological plausibility and budget feasibility. Cost: $0. Independent of t0091; runs in parallel.

2. **Reject S-0093-01**
   (`Refresh t0091 task description + dependencies to reference t0092 fix and t0093 correction overlay`).
   t0094_brainstorm_results_19 already executed exactly this work in-place: t0091's dependencies and
   import paths now reference t0092 and t0093, the short_description is refreshed, and the
   cross-references list extends with t0092, t0093, t0094. The suggestion is operationally
   fulfilled.

3. **Reject S-0074-03** (`AIS-localised Kv7 follow-up (t0075 candidate)`). The follow-up is already
   planned as `t0075_bio_realistic_ais_param_sweep`, status `not_started`. The suggestion is
   operationally fulfilled by the existing planned task.

4. **No task cancellations.** No suggestion reprioritisations. No new suggestions written by the
   brainstorm itself (t0096 will generate properly-scoped MOBO suggestions during its suggestions
   stage).

5. **Defer outcome-dependent decisions** about t0091 follow-ups (S-0086-01 NMDA re-run; Bed A
   morphology-extended NSGA-II; new MOBO axes derived from t0096) to a future brainstorm once t0091
   lands.

## Why these decisions

* The morphology + channel optimisation infrastructure is now production-ready (t0091 in flight on
  the t0092-patched generator with t0093 60/60 STABLE validation). The natural next research-depth
  move is to expand the **objective axis** of the Pareto search rather than spend more compute on
  the same DSI + firing-rate objective pair.
* Researcher's stated criterion of "biological plausibility" maps directly to the multi-objective
  framing: optimising DSI alone admits non-physical solutions; jointly optimising DSI vs energy or
  DSI vs volume forces the optimiser into bio-realistic regions of the parameter space.
* Survey is $0 and parallelisable with t0091. Fits the tight $4.45 remaining budget without
  contention.
* S-0093-01 and S-0074-03 are operationally fulfilled — keeping them on the active list wastes
  reviewer attention next session.
* Speculative MOBO tasks (DSI x ITR, etc.) deliberately not pre-created. The literature survey needs
  to ground them in concrete formulas and feasibility estimates first; otherwise we'd be scoping
  work without knowing which objectives are computationally tractable from a t0091-style trial
  output.

## Cross-references

* **t0089_brainstorm_results_18** — committed the morphology-extension pivot.
* **t0090_morphology_generator_diversity_test** — original procedural generator.
* **t0092_diagnose_morphology_generator_silence** — soma-pt3d collapse fix.
* **t0093_resweep_and_t0090_correction** — patched-generator 60/60 STABLE validation.
* **t0094_brainstorm_results_19** — launched t0091; already covered S-0093-01 in-place.
* **t0091_morphology_extended_nsga2_v1** — in flight; current MOBO objectives are DSI + firing
  rate. t0096 will catalogue alternative / additional objectives.
* **t0075_bio_realistic_ais_param_sweep** — planned not_started; covers S-0074-03.
* **t0096_literature_survey_multi_objective_neuron_optimisation** — commissioned by this session.
