# Brainstorm Session 20 - Full Transcript

Date: 2026-05-08 Skill: `/human-brainstorm` Researcher: Andrey Nikolaev
(mailto:a.nikolaev@sheffield.ac.uk)

## Project State Presented

**Date**: 2026-05-08. Brainstorm session 20 (next would be t0095).

### Budget Status

* Total: $20.00 | Spent: $15.55 (77.7%) | Remaining: $4.45.
* t0083 already exceeded its per-task limit ($5.83 vs $5.00).
* t0091 currently running: estimated $3.00-3.50; post-t0091 buffer $0.95-1.45.
* Warn threshold ($16) not yet hit; one expensive remote task remains feasible after t0091.

### Tasks

* 94 completed, 1 in-progress, 2 not-started.
* In progress (started today): `t0091_morphology_extended_nsga2_v1` — first joint 68-d NSGA-II
  (54-d electrophys + 14-d morphology) with t0092-patched generator, pop 96, <=8 gens, 5-anchor
  warm-start. Wall-clock estimate ~14-16 h Vast.ai. Headline experiment of the current cycle.
* Not-started: `t0031_fetch_paywalled_morphology_papers` (Kim2014 + Sivyer2013 retrieval, no
  compute); `t0075_bio_realistic_ais_param_sweep` (Bed A bio-AIS sweep, local).

### Recent results (since brainstorm 19, the last session)

* **t0094 (brainstorm 19, today)**: launched t0091; rejected S-0092-03 and S-0090-04 as
  covered/falsified.
* **t0093**: patched-generator 60-cell re-sweep — 60/60 STABLE-firing (vs 9/60 pre-fix), 56/60
  PD-rate>0, 21/60 DSI>0.5, mean DSI ~0.33, total spikes 16,107 vs 0 pre-fix. Soma-pt3d collapse fix
  from t0092 fully validated at scale.
* **t0092**: diagnosed and fixed `procedural_dsgc_morphology_generator` — soma `pt3dadd` collapse
  forced section length to ~1e-9 um and area to ~9.4e-14 um^2. Shim `generate_fixed_morphology`
  re-emits soma pt3d along z; BedB-equivalent post-fix fires 43.6 Hz PD; morph_14 hits DSI 0.962.

### Suggestion backlog (uncovered, active)

* 264 total: 10 high, 207 medium, 47 low.
* Medium tail likely contains stale items — better target for a dedicated cleanup pass once t0091
  lands.

### High-priority suggestions — reassessed view

| ID | Title | Reassessed priority | Why |
| --- | --- | --- | --- |
| S-0067-01 | Find NaP density at which DSI crosses zero | high (keep) | Local-only $0; targets a real finding from t0067 |
| S-0070-01 | Harmonise PD/ND encoding across Bed A and Bed B | high (keep) | Infra, no compute; unlocks cross-bed comparability |
| S-0074-01 | Polar tuning curves — distinguish SK_high narrowing from clipping | high (keep) | Likely doable on existing data; cheap |
| S-0074-02 | Verify NaR broadening hypothesis (ND-lobe rescue) | high (keep) | Local sweep, focused mechanism test |
| S-0074-03 | AIS-localised Kv7 follow-up | redundant with t0075 | Already planned; reject as covered |
| S-0076-04 | Direct test of t0076-vs-t0068 contradiction | high (keep) | Resolves a real contradiction; small-scope |
| S-0086-01 | NSGA-II re-run with tightened gnmda_dend bounds | deprioritise to medium until t0091 lands | $1.50 estimate may not fit; outcome-dependent |
| S-0090-02 | NaP-knockout sweep at scale on local 64-core | high (keep) | Local $0; covers t0090 partial REQ-12 |
| S-0090-03 | Re-run G.2 NMDA units calibration after BEDB_BASE_POINT retune | high (keep) | Local $0; unblocks cluster re-score |
| S-0093-01 | Refresh t0091 task description + dependencies | REJECT (covered) | t0094 already did this in-place |

### Strategic constraints

1. Budget tight: $4.45 left, $3.00-3.50 reserved for t0091.
2. t0091 in flight: outcome-dependent follow-ups cannot be designed sensibly until it completes.
3. Local-only work is currently free.

## Clarification Questions (Round 1)

AI asked 4 multi-choice questions: notes / t0091 timing / budget appetite / bundling.

Researcher: requested clarification of the questions themselves before answering.

AI: offered to clarify scope of "local-only", origin of $0.95-1.45 buffer, why S-0086-01 flagged but
S-0090-02/03 kept, and t0091 outcome paths.

## Strategic Broadening Directive

Researcher (verbatim):

> OK, so now that we have working optimisation for both morphology and channel composition we can
> optimise for different things. Currently we optimise for DSI and firing rate. However I would like
> to compare results for all sorts of stuff. For example, I would like to optimise for DSI and
> information transfer rate; DSI and energy spent, DSI and minimisation of citoplasm volume etc.
> Perform an extensive literature search and find papers that use different forms of optimisation.
> IT does not need to be DSGC but can be any neurons.

## Reframed Discussion - Round 1 (New Tasks)

AI: acknowledged the strategic pivot; sketched expected literature categories
(information-theoretic, metabolic / energy, structural / wiring, robustness / degeneracy, temporal /
coding); proposed multi-objective methodology line (Druckmann 2007/2011, BluePyOpt, Achard & De
Schutter 2006, Rumbell, Van Geit / NeuroFitter); proposed a single consolidated literature-survey
task t0096 with paper + internet + answer-question deliverables, $0 cost, runs in parallel with
t0091. Offered alternative of 3 themed surveys for cleaner per-topic folders.

AI asked 4 focused multi-choice questions: lit scope / bundling / output depth / must-have
objectives multi-select.

Researcher answered 3:
* Lit scope: Any neuron, any species, any modality (recommended).
* Bundling: One consolidated survey (recommended).
* Output depth: Catalogue + formulas + computational recipes (recommended).

Must-have objectives multi-select: unanswered. AI defaulted to the researcher's three named
objectives (ITR, energy, cytoplasm volume) plus robustness as the natural Marder-style addition.

## Reframed Discussion - Round 2 (Suggestion Cleanup)

AI proposed:
* Reject S-0093-01 as covered (t0094 did the t0091 update in-place).
* Reject S-0074-03 as covered (t0075 already planned).
* Do NOT prune the 207 medium-priority backlog this session.
* Do NOT deprioritise S-0086-01 yet — wait for t0091.
* Do NOT create speculative MOBO tasks (DSI x ITR, etc.) — t0096 will surface those.

## Reframed Discussion - Round 3 (Confirmation)

AI summarised tentative decisions:
1. Create t0096 (multi-objective optimisation literature survey, ~$0).
2. Reject S-0093-01 (covered by t0094).
3. Reject S-0074-03 (covered by t0075).
4. No task cancellations.
5. No suggestion reprioritisations.
6. No new suggestions written by the brainstorm itself.

Researcher: "fire away"

## Decisions Summary

1. **Create** `t0096_literature_survey_multi_objective_neuron_optimisation` (consolidated
   literature-survey + internet-research + answer-question task, $0, broad scope, formulas +
   computational recipes deliverable, must-cover ITR + energy + cytoplasm volume + robustness).
2. **Reject** S-0093-01 (correction `C-0095-01`).
3. **Reject** S-0074-03 (correction `C-0095-02`).
4. No task cancellations.
5. No suggestion reprioritisations.
6. No new suggestions written by this brainstorm.
