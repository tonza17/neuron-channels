---
spec_version: "1"
task_id: "t0101_brainstorm_results_21"
date_completed: "2026-05-11"
status: "complete"
---
# Results Detailed: Brainstorm Session 21 — Poleg-Polsky 2026 Deep-Dive

## Summary

Decision-recording brainstorm. See `results_summary.md` for the headline outcomes. This document
captures the full methodology trail and the verbatim numbers extracted from the Poleg-Polsky 2026
PDF for the audit record.

## Methodology

1. Researcher submitted seven questions about Poleg-Polsky 2026 covering parameter count, morphology
   optimisation, seed count, generation count, novel mechanisms, DSI values, and biological realism.
2. The existing `summary.md` for the paper was identified as untrustworthy in a quick triage
   (mentions "NMDA multiplicative gating", "velocity-dependent coincidence detection", "A-type
   potassium density" — none in the paper). The PDF at
   `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/files/polegpolsky_2026_ml-motion-primitives.pdf`
   was extracted via `pdftotext -layout` and read end-to-end.
3. Answers were compiled with exact quotes and section references.
4. The researcher asked how seeds/generations compare to our optimisations; the task aggregator was
   used to enumerate the NSGA-II/MOBO lineage (t0076, t0078, t0080, t0081, t0083, t0091, t0099) and
   the relevant `results_summary.md` files were read to extract pop, gens, seeds, cost, and headline
   metrics.
5. The researcher confirmed (via two `AskUserQuestion` rounds) the interpretation of the parameter
   knobs and the substrate / starting-condition for the follow-up task.
6. The cost aggregator surfaced a $3.91 budget overrun; researcher approved a bump to $35 total / $8
   per-task, committed directly to main as `dd9ac77f`.
7. Brainstorm-results task scaffolded on branch `task/t0101_brainstorm_results_21`. Decisions
   recorded.

## Poleg-Polsky 2026: Verified Numbers

(All taken from the PDF, not from `summary.md`.)

* **Title**: "Machine learning discovers numerous new computational principles supporting elementary
  motion detection" (Nat. Commun. 17:3424, 2026).
* **Author**: Alon Poleg-Polsky (sole author, University of Colorado Anschutz).
* **Morphology**: 352-segment DSGC (cited from ref 49 = Poleg-Polsky and Diamond 2016, ModelDB
  189347\) plus a 69-segment cortical L2/3 pyramidal cell. Fixed morphologies — not optimised.
* **Free parameters**: 10-12 per presynaptic group; 4 excitatory groups in most runs (~40-48
  params); +4 inhibitory groups when present (~88-96 params); +2 postsynaptic (passive g 1e-5-1e-3
  S/cm^2, axial resistance 50-200 ohm-cm). Unconstrained ~90 free params total.
* **Seeds**: minimum 50, typical 100 independent randomly-initialised GA restarts per circuit
  configuration.
* **Generations**: 300 typical, 1000 for low-performing configurations.
* **Population per generation**: 10 NEURON models in parallel (1 elite + 9 mutated).
* **Mutation**: each parameter scaled by N(1, 0.10) + U(-0.015, +0.015). Parameters either
  "independent" (per-group) or "shared" (mutated in group 1, copied to others).
* **8 computational primitives, 4 novel** (excitatory: H&R, anti-H&R, **amplitude**,
  **temporal-alignment**; inhibitory: B&L, **anti-B&L**, **pause-in-inhibition**,
  directionally-tuned inhibition).
* **DSI values** (subthreshold somatic peak voltage, vector sum over 12 directions x 5 speeds): 2.4
  +/- 0.1% (symmetric control), 22.1 +/- 0.8% (RF size only), 23.8 +/- 1.6% (kinetics only), 27.9
  +/- 1% (unconstrained excitation), 50.8 +/- 0.8% (B&L weight only), 66.8 +/- 2.4% (inhibitory
  kinetic), **73.1 +/- 2.4%** (fully unconstrained excitation + inhibition).
* **Biological realism**: phenomenological RF + 2D Gaussians, no real synaptic kinetics, no NMDA /
  AMPA / GABA mod files, no SAC, HH off by default. Passive g range upper end (1e-3 S/cm^2 = Rm ~1
  kohm-cm^2) is implausibly leaky for real neurons. Morphology, ~100 bipolar input count, and 0.25-4
  mm/s bar velocities are realistic.

## Discrepancies with `summary.md` (drives suggestion S-0101-01)

| Claim in `summary.md` | Actual paper content |
| --- | --- |
| Title "...underlying direction selectivity in the retina" | "...supporting elementary motion detection" |
| "velocity-dependent coincidence detection" | not in the paper |
| "distance-graded delay lines" | not in the paper |
| "NMDA-mediated multiplicative gating" | not in the paper |
| "A-type potassium density as a search axis" | not in the paper |
| Scope "retinal circuit" | retinal DSGC + cortical L2/3 pyramidal |

## Our Optimisation Lineage (for budget comparison with PP-2026)

| Task | Algorithm | Dim | Pop | Gens | GA seeds | $ | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| t0078 BoTorch qLogNEHVI | qLogNEHVI BO | 49 | - | 491 acq | 1 | $3.93 | pass narrowly missed (DSI=0.316, PD=9.68 Hz) |
| t0080 NSGA-II | NSGA-II | 54 | 24 | 8 | 1 | $0.75 | pass missed |
| t0081 NSGA-II warm-start | NSGA-II | 54 | 96 | 8 | 1 | $2.39 | pass MET (cell 767: DSI=0.494, PD=11.39 Hz) |
| t0083 NSGA-II extension | NSGA-II | 54 | 96 | gens 8-17 | 1 | $5.83 | 15 joint-pass cells, HV 16.33->35.58 |
| t0091 NSGA-II 68-d | NSGA-II | 68 | 96 | 2 of 8 | 1+anchor | $0.65 | 1 strict joint-pass cell |
| t0099 NSGA-II 68-d random-init | NSGA-II | 68 | 96 | 5/8/8 | 3 | $7.71 | 0 strict joint-pass cells / 55 Pareto cells |

* **N_SEEDS** (within-cell noise replicates, `tasks/t0080_*/code/constants.py:43`): 20 per
  direction. 8 directions x 20 trials = 160 sims per parameter-vector evaluation.
* **Total candidates evaluated in our largest single lineage** (t0081+t0083 = 1 728); **per-cell sim
  count 160** -> ~276 480 sims, $8.22 cumulative.
* **PP-2026 per-configuration**: 10 pop x 300 gens x 100 seeds = ~300 000 candidates, but each
  candidate is far cheaper (deterministic phenomenological RF, 60 stim conditions, no real channel
  kinetics).

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 1 |
| New suggestions recorded | 3 |
| Suggestions rejected | 0 |
| Suggestions reprioritised | 0 |
| Tasks cancelled | 0 |
| Corrections written | 0 |
| Answer assets produced | 0 |
| Project budget delta (USD) | +15 |

## Limitations

* Planning-only task. No experiments run, no metrics produced.
* The Poleg-Polsky 2026 numbers above are derived from PDF text extraction; if any figure-caption
  number was lost in extraction, the downstream summary.md correction task (S-0101-01) should
  re-verify against the figure captions.
* No formal independent re-read of summary.md was performed — the discrepancy list above is from a
  single pass and should be confirmed by S-0101-01 before the corrections file is written.

## Files Created

* `tasks/t0101_brainstorm_results_21/__init__.py`
* `tasks/t0101_brainstorm_results_21/task.json`
* `tasks/t0101_brainstorm_results_21/task_description.md`
* `tasks/t0101_brainstorm_results_21/step_tracker.json`
* `tasks/t0101_brainstorm_results_21/plan/plan.md`
* `tasks/t0101_brainstorm_results_21/research/research_papers.md`
* `tasks/t0101_brainstorm_results_21/research/research_internet.md`
* `tasks/t0101_brainstorm_results_21/research/research_code.md`
* `tasks/t0101_brainstorm_results_21/results/results_summary.md`
* `tasks/t0101_brainstorm_results_21/results/results_detailed.md`
* `tasks/t0101_brainstorm_results_21/results/metrics.json`
* `tasks/t0101_brainstorm_results_21/results/suggestions.json`
* `tasks/t0101_brainstorm_results_21/results/costs.json`
* `tasks/t0101_brainstorm_results_21/results/remote_machines_used.json`
* `tasks/t0101_brainstorm_results_21/logs/session_log.md`
* `tasks/t0101_brainstorm_results_21/logs/steps/001_review-project-state/step_log.md`
* `tasks/t0101_brainstorm_results_21/logs/steps/002_discuss-decisions/step_log.md`
* `tasks/t0101_brainstorm_results_21/logs/steps/003_apply-decisions/step_log.md`
* `tasks/t0101_brainstorm_results_21/logs/steps/004_finalize/step_log.md`

Modified outside this task (on main, separate commit):

* `project/budget.json` — total_budget 20 -> 35, per_task_default_limit 5 -> 8

## Verification

* `verify_task_file t0101_brainstorm_results_21` — PASSED.
* `verify_corrections t0101_brainstorm_results_21` — PASSED.
* `verify_suggestions t0101_brainstorm_results_21` — PASSED.
* `verify_logs t0101_brainstorm_results_21` — PASSED with expected `TS-W001`, `LG-W005`.

## Next Steps

1. Push branch, open PR, run pre-merge verificator, merge.
2. Re-checkout main and create `task/t0102_seedscale_n4_gen20` branch.
3. Scaffold t0102 task folder via `/create-task`.
4. Execute t0102 via `/execute-task`.
5. After t0102 completes, pick up S-0101-01 (Poleg-Polsky summary.md correction).
