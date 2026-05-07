---
spec_version: "3"
task_id: "t0089_brainstorm_results_18"
step_number: 2
step_name: "discuss-decisions"
status: "completed"
started_at: "2026-05-07T10:15:00Z"
completed_at: "2026-05-07T11:00:00Z"
---
# Step 2 -- Discuss Decisions

## Summary

Conducted a four-iteration interactive discussion with the researcher on morphology parametrisation
strategy; settled on Option H (procedural generator with 14 explicit DS-relevant knobs spanning
topology + asymmetry + geometry); split the work into two tasks (t0090 generator
+ diversity test, t0091 first joint NSGA-II) with 5-anchor warm-start (Bed-B + symmetric +
  PD-asymmetric + ND-asymmetric + alt-topology); cleaned 5 covered / duplicate suggestions and
  reprioritised 3 high to medium; received explicit "all approved. fire away" confirmation
  authorising the entire remaining lifecycle.

## Actions Taken

1. **Iteration 1 (parametrisation strategy)**: presented three options -- Option A (tier-based
   geometric scaling, 8 params), Option B (real-cell library + categorical selector), Option C
   (stochastic L-system tree generator). Recommended Option A with 8 params. Researcher rejected
   ("It has to reflect branching morphology and also asymmetry etc. Think more").
2. **Iteration 2 (parametrisation rev 2)**: identified that Option A only addressed geometry, not
   topology or asymmetry. Re-proposed Option H -- procedural DSGC morphology generator with 14
   explicit knobs spanning 5 topology + 4 asymmetry + 3 geometry + 2 stochastic control. Anchored
   asymmetry knobs to DS-functional features documented in Schachter 2010 / Trenholm 2013 / Briggman
   2011 (soma offset toward PD, dendritic field elongation along PD-ND axis, primary-branch
   direction bias). Researcher then asked the architectural-clarification question: "why can't we
   incorporate generation of neurons into the optimisation?"
3. **Iteration 3 (architectural clarification round 1)**: confirmed in-loop generation is the
   architecture; the procedural generator is a deterministic function
   `(params, seed) -> NEURON sections + connectivity` called inside the NSGA-II evaluation function
   per candidate. Researcher then asked again to confirm: "wait, I still don't understand. Why don't
   we generate morphologies during optimisation? Or is it what you propose?"
4. **Iteration 4 (architectural clarification round 2)**: explicitly contrasted the proposed
   architecture vs alternatives ((a) library selector + NSGA-II picks; (b) sensitivity-then-
   optimisation; (c) fixed-Bed-B); confirmed Plan A (in-loop generation per evaluation) is the
   target. Walked through the per-evaluation pseudocode showing where generator is called.
   Researcher confirmed: "OK, great. But you are right. Let's split it into two tasks. 1 - write and
   test generator - generate and visualise say 30 random very different morphologies and 30 very
   similar ones. U assume we can still use 64 core to parallelise the generation? And then second
   task - first optimisation attempt. Use one seed that we currently have (WITH MORPHOLOGY SIMILAR
   TO WHAT WE HAVE) and few more very different seeds - symmetric and asymmetric."
5. **Round 1 -- New tasks**: proposed t0090 (generator + 30 different + 30 similar + viz + Bed-B
   reproducibility + validation bundle, ~$0.30, ~3-4 days local) and t0091 (joint 68-d NSGA-II with
   5-anchor warm-start: Bed-B-like + symmetric + PD-asymmetric + ND-asymmetric + alt-topology, pop
   96 x ~19 t0083 Pareto electrophys variants per anchor, ~$3.00-3.50 Vast.ai, ~14-16 hours
   wall-clock).
6. **Round 2 -- Suggestion cleanup**: proposed 5 rejections (S-0086-02, S-0088-01, S-0088-02,
   S-0084-05, S-0083-03) and 3 reprioritisations (S-0083-01, S-0084-01, S-0084-02 high -> medium).
   Rationales: validation bundle covered by t0090 Phase G (S-0086-02, S-0088-01, S-0088-02);
   S-0084-05 duplicate of S-0088-01; S-0083-03 covered by t0088 cluster 1 attribution; S-0083-01
   out-of-budget and superseded by morphology direction; S-0084-01 / S-0084-02 superseded by
   population-level mechanism attribution.
7. **Researcher pushback on Phase A time estimate**: researcher questioned 3-4 day estimate ("Why
   phase A takes 4 days?"); revised to 1.5-2 days based on honest sub-step breakdown (recursive tree
   builder ~3-4 h, asymmetry transforms ~2-3 h, NEURON section translation ~2-3 h, determinism +
   unit tests ~3-4 h, Bed-B reproducibility check ~2-3 h; total ~12-17 hours wall-clock).
8. **Round 3 -- Confirmation**: presented compact decision list. Researcher responded "all approved.
   fire away" -- the explicit Phase 2 Round 3 confirmation authorising the entire remaining
   lifecycle including push, PR, premerge, and merge per the skill specification.

## Outputs

* No files produced in this step. Decisions are recorded in this step log and in the brainstorm
  task's `task_description.md` and `results/results_summary.md`.

## Issues

No issues encountered. Four iterations on parametrisation took longer than typical (~45 min vs the
usual ~15 min) but produced a substantially better-aligned result. The architectural- clarification
round (iterations 3-4) was a self-correction triggered by initial over-bundling of the task design
with sensitivity-sweep de-risking that obscured the simple in-loop-generation architecture.
