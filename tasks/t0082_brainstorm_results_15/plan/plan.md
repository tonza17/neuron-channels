# Plan: Brainstorm Results Session 15

## Objective

Run an interactive strategic brainstorming session on 2026-05-05 after t0081
(`bedb_v3_warmstart_nsga2`) completed and **delivered the project's first joint-pass cell**: gen 7
cell 767 at DSI 0.494 / PD 11.39 Hz on a 16-cell Pareto front (768 evaluations, $2.39 on Vast.ai).
The session acts on two researcher-directed t0081 follow-ups: (a) extend NSGA-II from t0081's gen-7
final population with an adaptive HV-plateau stop rule (S-0081-02), and (b) per-direction Vm-trace
deep-dive of cell 767 plus the two near-pass neighbours 637 and 762 (S-0081-03). Reject three
high-priority t0080 suggestions covered by t0081's positive result. No reprioritisations; no other
task changes; t0075 stays queued.

## Approach

Follow the `/human-brainstorm` skill end-to-end: aggregate project state, read every results summary
and compare-literature file for tasks completed since brainstorm 14 (t0080 and t0081), present an
independent priority reassessment of the 11 high-priority active uncovered suggestions (highlighting
the three S-0080-* now superseded by t0081's positive result), conduct the three-round discussion
(two new tasks; suggestion cleanup; confirmation), scaffold the brainstorm-results folder, write
three correction files, and create the new not-started t0083 and t0084 task folders via the
`/create-task` skill.

## Cost Estimation

No paid services. No remote compute for this brainstorm task. Local CPU only. Zero dollar cost. The
two child tasks (t0083 / t0084) carry a combined estimated cost of $1.50 - $3.00 with a $5.00 hard
cap on t0083 and $0 on t0084 (local CPU).

## Step by Step

1. Review project state: run task / suggestion / cost aggregators; read `results_summary.md`,
   `results_detailed.md`, and `compare_literature.md` for t0080 and t0081 (the two tasks completed
   since brainstorm 14); rebuild `overview/`.
2. Form an independent reassessment of the 11 high-priority active uncovered suggestions, focusing
   on the three S-0080-* superseded by t0081's positive result (S-0080-01/02/03) and the three new
   t0081- derived suggestions (S-0081-01/02/03).
3. Present project state and reassessed priorities to the researcher; highlight the budget context
   ($8.13 / $10.00 spent before researcher top-up).
4. Three-round discussion: agree on two new tasks (t0083 extend t0081 NSGA-II from gen-7 final state
   with adaptive HV-plateau stop, $5.00 hard cap; t0084 Vm-trace deep-dive cells 767/637/762, local
   CPU $0); agree on three rejections (S-0080-01/02/03); explicit go-ahead authorising the entire
   remaining lifecycle.
5. Scaffold `tasks/t0082_brainstorm_results_15/` with full folder structure.
6. Write three suggestion-correction files under `corrections/`: all `update` actions setting
   `status: "rejected"`, with rationale identifying t0081 as the covering task.
7. Create t0083 (`bedb_v3_extend_nsga2_gen8plus`) and t0084 (`t0081_cell_767_vm_trace_deepdive`)
   folders via `/create-task`.
8. Write step logs, session log, and results files.
9. Capture session transcripts via `capture_task_sessions`.
10. Run all relevant verificators (`verify_task_file`, `verify_logs`, `verify_corrections`,
    `verify_suggestions`).
11. Commit, push branch, open PR, run pre-merge verificator, merge.

## Remote Machines

None.

## Assets Needed

None. The brainstorm task itself produces no assets.

## Expected Assets

None. `expected_assets = {}`.

## Time Estimation

Approximately 30 min of interactive discussion plus 15 min of scaffolding, correction authoring, and
child-task creation, plus 15 min of verification, PR, and merge. Total ~60 min wall-clock.

## Risks & Fallbacks

* **Task index drift mid-session**: a parallel session merges another task to main while this
  brainstorm runs. Mitigation: re-run the task aggregator before reserving the brainstorm task
  index; rename branch and folder if a collision is detected.
* **Researcher unavailable mid-session**: skill allows resumption from any phase boundary.
* **Verificator failures at Phase 6**: fix in place and re-run; never rewrite task-branch history
  per `task_git_specification` rule 14.
* **Correction-file typos**: caught by `verify_corrections.py`; fix in place before commit.
* **t0083 dependency surface**: t0083 depends on t0081 (provides gen-7 final population), t0080
  (substrate library), t0078, t0024. All four are completed and not at risk of being rewritten on
  main.
* **t0084 dependency surface**: t0084 depends on t0081 (provides cell 767/637/762 parameter vectors)
  and t0080 (substrate library). Both completed.
* **HV-plateau stop rule under-triggers / over-triggers**: if t0083's adaptive stop fires too early
  (below 5 generations) the run is underbudgeted; if it never fires within 10 additional generations
  the hard cap +10 gens (i.e., gen 17) and $5.00 cost cap take over. Both failure modes documented
  in t0083's plan as expected operating envelope.

## Verification Criteria

* `verify_task_file.py t0082_brainstorm_results_15` passes with 0 errors.
* `verify_logs.py t0082_brainstorm_results_15` passes with 0 errors (LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance).
* `verify_corrections.py t0082_brainstorm_results_15` passes with 0 errors for all 3 correction
  files.
* `verify_suggestions.py t0082_brainstorm_results_15` passes with 0 errors (empty array).
* The two new child tasks (t0083 and t0084) exist on disk with valid `task.json`.
* `verify_task_file.py t0083_bedb_v3_extend_nsga2_gen8plus` passes with 0 errors.
* `verify_task_file.py t0084_t0081_cell_767_vm_trace_deepdive` passes with 0 errors.
* PR opens, pre-merge verificator passes, merge to main succeeds, `overview/` rebuilds cleanly on
  main.
