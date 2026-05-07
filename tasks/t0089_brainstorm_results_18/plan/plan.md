# Plan: Brainstorm Results Session 18

## Objective

Run an interactive strategic brainstorming session on 2026-05-07 after t0088
(`recluster_marginals_and_vm_motifs`) extended t0086's biological-plausibility analysis to a 13-cell
pool (6 Genuine + 7 Marginal) and confirmed `shared_mechanism_different_scale` across 4 clusters
(all NaP-dominant in PD-minus-ND attribution; NMDA frac 0.000 across all). The researcher's
strategic directive: pivot the project from electrophys-only optimisation (t0080-t0088) to
**morphology-extended optimisation** with morphology generated inside the NSGA-II evaluation loop.
The session commissions two new tasks:

* **t0090** -- procedural DSGC morphology generator with 14 explicit knobs (5 topology + 4 asymmetry
  \+ 3 geometry + 2 stochastic control); 30 very-different + 30 very-similar morphologies;
  visualisation; Bed-B reproducibility; validation bundle (S-0088-02 + S-0086-02 + S-0088-01).
* **t0091** -- first joint 68-d NSGA-II optimisation with morphology generated inside the eval loop;
  warm-started from 5 distinct morph anchors (Bed-B + symmetric + PD-asymmetric + ND-asymmetric +
  alternative-topology).

Reject 5 covered/duplicate suggestions; reprioritise 3 high suggestions to medium.

## Approach

Follow the `/human-brainstorm` skill end-to-end. The discussion required four iterations on
morphology parametrisation: Option A (tier-based scaling) was too narrow for the topology +
asymmetry features the researcher wanted; ultimately settled on Option H (procedural generator with
explicit DS-functional knobs). The researcher then decided to split the work into two tasks
(generator + diversity test as t0090; first joint NSGA-II as t0091) to de-risk the dimensionality
jump (54-d -> 68-d) and validate the generator before committing $3+ to optimisation. The phrase
"all approved. fire away" served as the explicit confirmation, authorising the entire remaining
lifecycle including push, PR, and merge.

## Cost Estimation

No paid services for this brainstorm task. No remote compute. Local CPU only. Zero dollar cost.
Child task t0090 carries ~$0.30 (validation bundle). Child task t0091 carries ~$3.00-3.50 (Vast.ai
EPYC 7B13). Combined child cost ~$3.30-3.80, leaving ~$0.94-1.44 buffer of the $4.44 remaining.

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read t0088 results_summary,
   compare_literature, and the answer asset; the most recent commit
   (`d340a27f overview: refresh after t0088_recluster_marginals_and_vm_motifs`) confirms `overview/`
   is current.
2. Form an independent reassessment of the 15 active high-priority suggestions, grouped by coverage
   status: covered by new tasks (S-0086-02, S-0088-01, S-0088-02), duplicate of others (S-0084-05),
   covered by t0088 (S-0083-03), out-of-budget or superseded (S-0083-01, S-0084-01, S-0084-02),
   still high (S-0086-01, S-0070-01).
3. Present project state to the researcher; record the verbatim strategic-pivot directive.
4. Iterate four times on morphology parametrisation (Option A tier scaling -> rejected; Option H
   procedural generator with topology + asymmetry knobs -> accepted; in-loop generation architecture
   clarified twice; two-task split agreed; 5-anchor warm-start design).
5. Suggestion cleanup discussion: 5 rejections + 3 reprioritisations.
6. Researcher confirmation: "all approved. fire away".
7. Scaffold `tasks/t0089_brainstorm_results_18/` with full folder structure.
8. Write 8 suggestion-correction files under `corrections/`.
9. Create t0090 and t0091 not-started task folders via /create-task.
10. Write step logs, session log, and results files.
11. Capture session transcripts via `capture_task_sessions`.
12. Run verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
    `verify_suggestions`).
13. Re-run materialiser; format markdown; commit, push, PR, premerge, merge.

## Remote Machines

None for this brainstorm task.

## Assets Needed

None. The brainstorm task itself produces no assets.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 60 minutes of interactive discussion (four iterations on morphology parametrisation
took longer than typical) plus 30 minutes of scaffolding, correction authoring, and child-task
creation, plus 15 minutes of verification, PR, and merge. Total ~90-100 minutes wall-clock.

## Risks & Fallbacks

* **Task index drift mid-session**: parallel session merges another task to main while this
  brainstorm runs. Mitigation: re-run task aggregator before reserving the brainstorm task index.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **Two-task split adds latency before first morphology-extended NSGA-II**: explicit researcher
  preference; t0090 outputs gate t0091 architecturally and risk-wise. Acceptable.
* **t0090 generator implementation underestimated at 1.5-2 days**: researcher pushback on the
  initial 3-4 day estimate prompted a tighter breakdown; if implementation runs over 3 days, fall
  back to TREES toolbox (Cuntz 2010) instead of full custom generator.

## Verification Criteria

* `verify_task_file.py t0089_brainstorm_results_18` passes with 0 errors.
* `verify_logs.py t0089_brainstorm_results_18` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture).
* `verify_corrections.py t0089_brainstorm_results_18` passes with 0 errors for 8 correction files.
* `verify_suggestions.py t0089_brainstorm_results_18` passes with 0 errors (empty array).
* The new child tasks t0090 and t0091 exist on disk with valid `task.json`.
* `verify_task_file.py t0090_<slug>` and `verify_task_file.py t0091_<slug>` pass with 0 errors.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
