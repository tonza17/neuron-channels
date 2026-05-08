---
spec_version: "1"
task_id: "t0095_brainstorm_results_20"
date_completed: "2026-05-08"
status: "complete"
---
# Results Summary: Brainstorm Session 20

## Summary

Twentieth strategic brainstorm, run on 2026-05-08 while t0091 (`morphology_extended_nsga2_v1`) is in
flight on Vast.ai. The researcher proposed broadening the MOBO objective space beyond DSI + firing
rate to include information transfer rate, metabolic energy, cytoplasm volume, and robustness;
commissioned a single consolidated literature survey
(`t0096_literature_survey_multi_objective_neuron_optimisation`) at $0 cost, scoped broadly across
any neuron type, with formulas + computational recipes + future MOBO suggestion list as
deliverables. Two already-covered suggestions (S-0093-01, S-0074-03) rejected.

## Session Overview

Date: 2026-05-08. Triggered by completion of the t0090 -> t0092 -> t0093 -> t0091-launch chain in
brainstorm session 19 earlier today. With the morphology + channel NSGA-II infrastructure
production-ready and t0091 already running, the researcher's strategic message was a pivot: "Now
that we have working optimisation for both morphology and channel composition we can optimise for
different things... DSI and information transfer rate; DSI and energy spent; DSI and minimisation of
cytoplasm volume etc. Perform an extensive literature search and find papers that use different
forms of optimisation. It does not need to be DSGC but can be any neurons."

Three multi-choice clarifications resolved the survey scope:

* **Lit scope**: any neuron, any species, any modality (recommended option chosen). Maximises the
  diversity of objective functions surfaced and matches the researcher's stated framing ("any
  neurons").
* **Bundling**: one consolidated survey (recommended option chosen). Matches the researcher's stated
  preference for consolidated tasks (memory entry `feedback_consolidated_task_design`).
* **Output depth**: catalogue + formulas + computational recipes (recommended option chosen). Each
  objective documented with formula, units, NEURON-side quantities required, and a recipe to compute
  it from a t0091-style trial output. Heavier deliverable, much more actionable for downstream MOBO
  task creation.

The fourth question (must-have objectives multi-select) was not answered explicitly. Defaulted to
the researcher's three named objectives (ITR, energy, cytoplasm volume) plus robustness as the
natural Marder-style addition. Phase 2 Round 3 confirmation arrived as "fire away".

## Decisions

1. **Create t0096_literature_survey_multi_objective_neuron_optimisation**. Single consolidated
   literature-survey + internet-research + answer-question task covering:

   * Information-theoretic objectives (mutual information / ITR, Fisher information, channel
     capacity, stimulus-reconstruction MSE).
   * Metabolic / energy objectives (ATP per spike, total ionic flux, Na+/K+ pump cost,
     bits-per-ATP).
   * Structural objectives (total dendritic length, total membrane area, cytoplasm volume, wiring
     economy).
   * Robustness / degeneracy objectives (parameter-perturbation sensitivity, noise tolerance,
     Marder-style multi-conductance solution-space).
   * Temporal / coding objectives (latency, jitter, reliability, bandwidth, dynamic range).

   Methodology line: Druckmann 2007/2011, BluePyOpt, Achard & De Schutter 2006, Rumbell et al., Van
   Geit / NeuroFitter. Biological objective-function origin papers: Attwell & Laughlin 2001, Niven &
   Laughlin 2008, Sengupta et al. 2010, Chklovskii, Cuntz et al. 2010, Marder & Goaillard 2006.
   Cost: $0. Independent of t0091; runs in parallel.

   Deliverables: `research_papers.md`, `research_internet.md`, an answer asset catalogueing each
   objective with formula + units + NEURON-side computational recipe, and `suggestions.json`
   proposing future MOBO tasks (DSI x ITR, DSI x ATP, DSI x volume, DSI x robustness) ranked by
   biological plausibility and budget feasibility.

2. **Reject S-0093-01**
   (`Refresh t0091 task description + dependencies to reference t0092 fix and t0093 correction overlay`).
   t0094_brainstorm_results_19 already executed exactly this work in-place. Operationally fulfilled.
   Correction file `C-0095-01`.

3. **Reject S-0074-03** (`AIS-localised Kv7 follow-up (t0075 candidate)`). The follow-up is already
   planned as `t0075_bio_realistic_ais_param_sweep` (status `not_started`). Operationally fulfilled.
   Correction file `C-0095-02`.

4. **No task cancellations.** **No suggestion reprioritisations.** **No new suggestions written by
   the brainstorm.** The medium-priority backlog (207 suggestions) is left untouched; better target
   for a dedicated cleanup pass once t0091 lands.

5. **Defer outcome-dependent decisions** about t0091 follow-ups (S-0086-01 NMDA re-run; Bed A
   morphology-extended NSGA-II; new MOBO axes derived from t0096) to a future brainstorm.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 1 (t0096_literature_survey_multi_objective_neuron_optimisation) |
| Tasks updated | 0 |
| Tasks cancelled | 0 |
| Suggestions rejected | 2 (S-0093-01, S-0074-03) |
| Suggestions reprioritised | 0 |
| Corrections written | 2 |
| New suggestions created | 0 |
| Answer assets created | 0 |
| Session duration | ~45 minutes interactive |
| Session cost | $0.00 |
| Estimated cost of commissioned tasks | $0.00 (t0096 is paper + internet research, no compute) |

## Verification

* `verify_task_file.py t0095_brainstorm_results_20` — target 0 errors.
* `verify_task_file.py t0096_literature_survey_multi_objective_neuron_optimisation` — target 0
  errors.
* `verify_corrections.py t0095_brainstorm_results_20` — target 0 errors for 2 correction files.
* `verify_suggestions.py t0095_brainstorm_results_20` — target 0 errors (empty array).
* `verify_logs.py t0095_brainstorm_results_20` — target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_pr_premerge.py t0095_brainstorm_results_20 --pr-number <N>` — target 0 errors.

## Next Steps

1. **Execute t0096** in a fresh worktree once t0091 lands and the researcher reviews its output.
   Expected wall-clock: 2-4 hours by an autonomous research agent. Cost: $0. Output: downloaded
   papers + research_papers.md + research_internet.md + objective-function answer asset + ranked
   future-MOBO suggestion list.

2. **Decision point after t0091 + t0096 both complete**:

   * t0091 outcome will tell us whether morphology extension materially shifts the DSI Pareto.
   * t0096 catalogue will give us a feasibility-ranked list of new objective functions and concrete
     formulas to plug into the existing Bed B NSGA-II loop.
   * Combined, these determine which DSI x {ITR, ATP, volume, robustness} MOBO task to commission
     next, scoped within the remaining ~$0.95-1.45 buffer.

3. **Post-t0091 follow-ups** still on the radar (deferred, not commissioned this session):

   * **S-0086-01** (NSGA-II re-run with tightened NMDA bounds, ~$1.50) — high priority if t0091
     motivates revisiting the 54-d search.
   * **S-0090-03** (G.2 NMDA units calibration) — local-only $0.
   * **S-0090-02** (NaP-knockout sweep at scale on local 64-core) — local-only $0.
   * **S-0070-01** (harmonise PD/ND encoding across Bed A and Bed B) — high priority infra, no
     compute.
   * **S-0067-01** (NaP density at which DSI crosses zero) — local-only $0.
   * **S-0074-01 / S-0074-02** (polar tuning curves; NaR broadening hypothesis) — likely doable on
     existing data.
   * **S-0076-04** (direct test of t0076-vs-t0068 contradiction) — focused experiment.
