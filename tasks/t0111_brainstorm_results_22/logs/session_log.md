# Brainstorm Session 22 — Full Transcript

Session date: 2026-05-19. Trigger: researcher invoked `/human-brainstorm` after the t0106 -> t0110
NSGA-II + analysis wave. Researcher's opening direction was specific: replicate t0106 at a fresh
seed with a tighter NEURON pool-restart cadence.

## Project State Presented

**Headline numbers**

* 111 tasks (103 completed, 1 intervention_blocked, 2 not_started, 5 cancelled)
* Budget: $56.80 / $75 spent (75.7%), $18.20 left; no thresholds tripped
* 325 uncovered suggestions (31 high, 241 medium, 53 low)

**What happened since the last brainstorm (t0101, 2026-05-11)**

The last brainstorm commissioned t0102 (the "PolegPolsky-mirroring" 68-d NSGA-II at seeds=2,
N_SEEDS=4, gens=20). Since then nine tasks completed and one major story landed:

1. **t0102** — Re-ran NSGA-II 68-d at GA-seeds=2 / N=4 / gens=20 from random init. 0 joint-pass
   cells — replicated the t0099 / t0104 null.
2. **t0103** — Extracted 64 DS cell morphologies from Baden 2016. Three follow-up download
   suggestions.
3. **t0104** — 2-objective 68-d NSGA-II at 3 GA seeds. Best non-artifact DSI = 0.54 at seed 55
   gen 11; 0 joint-pass cells.
4. **t0105 (cluster + factor)** + **t0105 (prelim figures)** — K-means + varimax FA across prior
   optimisations; 11-slide deck for the supervisor report.
5. **t0106 — BREAKTHROUGH.** Long 2-direction NSGA-II, 1 seed x 40 gens x pop 96 = 3,744 evals.
   **123 unique joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) — first ever in t0080 -> t0104
   lineage.** Best ratio DSI = 1.0000 at PD = 81 Hz; best PD = 122.6 Hz at DSI = 0.92. Cost
   $10.37. The reformulation (16-dir vsum -> 2-dir ratio), not the budget, made the difference.
6. **t0107 — CAVEAT.** 8-direction polar re-eval of 10 random top-50 cells: same cells average
   DSI = 0.519 under 8-dir vector-sum (vs t0106's 0.939). Mean drop = 0.42. Rank order preserved
   (Spearman rho = 0.758). t0106's DSI ~= 1.0 is largely a metric artefact; cells remain in the
   biological direction-selective range.
7. **t0108** — Cluster + FA on 150 strict-cohort cells. Morphology K-means k=4 dominates;
   electrophys K-means is an outlier split. F10 = single joint DSI-PD trade-off factor.
8. **t0109** — 4x10 morphology gallery; cluster 1 is visually distinct (tighter, PD-asymmetric).
9. **t0110** — Relaxed-cohort FA (N=247) shows t0108's all-negative PD column was a
   truncated-cohort artifact; F1 is a joint failure axis (r_DSI = -0.37, r_PD = -0.75).

**Active non-completed tasks**

* t0023_port_hanson_2019_dsgc — intervention_blocked (deferred, never reopened)
* t0031_fetch_paywalled_morphology_papers — not_started (Kim2014 + Sivyer2013)
* t0075_bio_realistic_ais_param_sweep — not_started (Bed A AIS sweep)

**Independent priority reassessment of high-priority suggestions**

* Promoted: S-0106-02 (N_EVAL_SEEDS=20 robustness re-eval) — CRITICAL given t0107.
* New need flagged: 8-direction polar re-evaluation of ALL 123 t0106 joint-pass cells.
* Demoted: S-0106-01 (more 2-dir runs not the priority), S-0102-03 / S-0104-04 (IBEA), S-0102-04
  (Dang pop floor).
* Maintenance: S-0101-01 (correct fabricated content in PolegPolsky 2026 summary.md) — still
  load-bearing.

## Clarification

AI: Do you have any notes, ideas, or context that should guide this session?
Researcher: I think we need to repeat t0106 successful optimisation with a different seed.
  Select a new random seed and repeat the optimisation. Probably it makes sense to restart every
  tenth gen rather than 25th given the memory leak in NEURON?

(The researcher's direction reframed the session as a single-task design discussion rather than
the broader 3-area strategic survey originally planned. AI dropped the open strategic-focus,
budget-envelope, and execution-preferences questions and went straight to confirming the
specific parameters of the proposed t0112 task.)

AI: Quoted t0106's actual settings (T0106_SEEDS = (44,), `_POOL_RESTART_EVERY = 25` in
  `nsga2_driver.py:97`, N_GEN = 300 configured but operator-stopped at gen 40 at HV plateau,
  N_EVAL_SEEDS = 3, N_DIRECTIONS = 2, POP_SIZE = 96, cost $10.37 of $25 cap). Confirmed the
  seed change + 10-gen restart proposal as sound; flagged that for a clean comparison the
  replicate should use the same operator-stop criterion (HV plateau via the existing
  `HV_PLATEAU_*` constants) rather than a fixed gen count.

AI: Which seed should we use for the t0106 replicate? (t0106 used 44; t0104 used 11/22/33;
  t0099 used 11/22/33; t0102 used 44/55.)
Researcher: 77 (unused, easy to remember).

AI: Should the replicate stop the same way t0106 did?
Researcher: Same HV-plateau stop, gen cap raised to 60 just in case.

AI: Anything else to change from t0106?
Researcher: Nothing else — minimum-change replicate.

## Discussion — Round 1: New Tasks

AI proposed t0112_t0106_seed77_replicate:

* Substrate: 68-d Bed B + 14-d morphology (identical to t0106).
* Driver: forked from `tasks/t0106_long_pdnd_nsga2_300gen/code/nsga2_driver.py`.
* Changes from t0106: `T0112_SEEDS = (77,)`, `_POOL_RESTART_EVERY = 10`, gen ceiling 60 with
  HV-plateau operator-stop.
* Unchanged: pop=96, N_EVAL_SEEDS=3, N_DIRECTIONS=2, ratio DSI objective, random LHS init, no
  warm-start, silence guard, per-instance watchdog at $20.
* Cost cap: $25 (same per-task cap); expected actual ~$10-11.
* Dependencies: t0106_long_pdnd_nsga2_300gen.
* No companion tasks this wave — t0112 is the gating result for everything downstream.

Researcher: accepted (decision recorded above via the multi-question form).

## Discussion — Round 2: Suggestion Cleanup

AI proposed 4 reprioritisations (S-0106-01, S-0102-03, S-0102-04, S-0104-04 from high to
medium):

* S-0106-01: partially covered by t0112 (one additional seed); medium more accurate.
* S-0102-03 / S-0104-04 (IBEA at matched budget): pre-t0106; value now unclear after the 2-dir
  trick changed the picture.
* S-0102-04 (Dang2023 mu = n log n at pop ≥ 290): pop=96 worked on the 2-dir substrate, so the
  Dang floor is less load-bearing.

Researcher: Skip cleanup this session.

Decision recorded: 0 rejections, 0 reprioritisations.

## Discussion — Round 3: Confirmation

AI summarised the final decision list:

* 1 new task: `t0112_t0106_seed77_replicate` (seed 77, 10-gen pool restart, gen ceiling 60,
  HV-plateau stop, all other parameters identical to t0106).
* 0 suggestion rejections, 0 reprioritisations, 0 new suggestions.
* 0 task cancellations, 0 task updates.
* 0 answer assets.
* Brainstorm task: `t0111_brainstorm_results_22`; child task: `t0112_t0106_seed77_replicate`.

AI: Confirm the full decision list and authorise execution of Phases 4-6 (create brainstorm
  task, then create child task, run verificators, push, PR, merge) without further prompts?
Researcher: Confirmed — proceed all the way through merge.

## Decisions Summary

1. Create `t0111_brainstorm_results_22` (this brainstorm task).
2. Create `t0112_t0106_seed77_replicate` — minimum-change t0106 replicate with seed 77,
   `_POOL_RESTART_EVERY = 10`, gen ceiling 60, HV-plateau stop; cost cap $25;
   dependency `t0106_long_pdnd_nsga2_300gen`; source_suggestion null.
3. Skip suggestion cleanup; the 325 uncovered suggestions remain at their current priorities
   pending the t0112 outcome.
