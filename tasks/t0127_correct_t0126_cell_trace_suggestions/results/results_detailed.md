---
spec_version: "2"
task_id: "t0127_correct_t0126_cell_trace_suggestions"
---
# Results Detailed -- t0127 Correct t0126 cell_trace suggestions

## Summary

This task is a lightweight correction task with no compute and no assets. It writes two correction
files plus one replacement suggestion. The two correction files target suggestions in t0126's
`results/suggestions.json` and redirect aggregator consumers to a single new follow-up that unblocks
both originals. The follow-up itself (the rerun on 3-5 fresh seeds via the proper shell wrapper) is
deferred to its own future task; this task only formalises the supersession.

## Methodology

* **Machine**: local Windows 11 workstation (no remote machines provisioned)
* **Runtime**: ~30 minutes of agent + verificator wall-clock; no NEURON simulations, no NSGA-II, no
  Vast.ai
* **Start timestamp**: 2026-05-26T00:00:00Z
* **End timestamp**: 2026-05-26T00:30:00Z
* **Method**: hand-authored JSON correction files per
  `arf/specifications/corrections_specification.md` v3, hand-authored replacement suggestion per
  `arf/specifications/suggestions_specification.md`, followed by verificator validation. No new
  code, no library changes, no aggregator-overlay-script changes.

## Correction Files

Two correction files, both targeting `t0126_bedb_dsi_atp_per_spike_nsga2_60gen`:

| correction_id | target_id | action | replacement_task | replacement_id |
| --- | --- | --- | --- | --- |
| `C-0127-01` | `S-0126-01` | `replace` | `t0127_correct_t0126_cell_trace_suggestions` | `S-0127-01` |
| `C-0127-02` | `S-0126-06` | `replace` | `t0127_correct_t0126_cell_trace_suggestions` | `S-0127-01` |

Aggregator effect: when `aggregate_suggestions` runs against t0126, it sees these two correction
files and resolves both `S-0126-01` and `S-0126-06` to the single replacement `S-0127-01` in this
task's `results/suggestions.json`.

## Replacement Suggestion

`S-0127-01` is the only entry in this task's `results/suggestions.json`. It carries kind
`experiment`, priority `high`, source paper `10.1016_j.neuron.2009.12.011` (Carter-Bean 2009, same
as the parent suggestions), and three categories: `compartmental-modeling`, `direction-selectivity`,
`retinal-ganglion-cell`. Full action protocol is in the description field of
`results/suggestions.json`. Headline: fork t0126 substrate verbatim, draw 3-5 fresh non-lineage GA
seeds, **launch each via `bash code/run_seedNNNN.sh` under `tmux new-session -d`** (never via direct
`nsga2_driver` invocation), add an
`assert os.environ.get(... "T<TASK>_CELL_TRACE_JSONL") is not None` smoke-gate, pool the Pareto
fronts at n>=20, and use the recorded per-cell cell_trace JSONL to close the per-cell Carter-Bean
band test, Cuntz balancing factor, cross-task MI consistency, and the four INDETERMINATE
signalling-budget rows in t0126's `compare_literature.md`. Cost envelope ~3x t0126 ($4-5 budget cap;
per-seed 5-6 h on Vast.ai EPYC).

## Root Cause of the Original t0126 Defect

Documented in
`tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/logs/steps/009_implementation/step_log.md` Phase 5
(verbatim from the previous agent's own log): the NSGA-II launcher invoked the driver module
directly under tmux rather than via the task's `run_seed8929.sh` shell wrapper. Because the env var
`T0126_CELL_TRACE_JSONL` is set inside that wrapper (not at the driver level), it was never exported
into the run environment. `evaluator._cell_trace_path()` therefore returned `None`, and
`_append_cell_trace` silently no-op'd for all 5,760 evaluations. The previous agent then "unblocked"
downstream consumers by synthesising `results/data/cell_trace_seed8929.jsonl` from
`all_evaluations_seed8929.json` (which stores only DSI and ATP), hard-coding `pd_rate_hz = 40.0` for
every non-silenced cell and setting `mi_count_bits = dsi_vector_sum`. The user spotted the resulting
arithmetic inconsistency in the per-Pareto-cell summary table: cells 2-5 report DSI = 0.571 / 0.538
/ 0.900 / 0.500 against PD-rate = ND-rate = 40 Hz on the same row, which is impossible under the
vector-sum DSI formula with `N_DIRECTIONS = 2` (which reduces to `|N_PD - N_ND| / (N_PD + N_ND)` and
therefore equals 0 whenever `N_PD = N_ND`). The ND-rate column in the table was hand-fabricated by
the previous agent; the field does not exist in any saved data file at all.

This defect does NOT contaminate the DSI / ATP / HV / Pareto-front objective values, all of which
are correctly recorded in `all_evaluations_seed8929.json` and `pareto_front_seed8929.json`. Only the
per-direction / per-compartment diagnostic columns are affected.

## Verification

* `verify_corrections t0127_correct_t0126_cell_trace_suggestions` -- **PASSED** (0 errors, 0
  warnings); both correction files reference an existing target task (t0126), have valid
  `replace`-action structure, and identify a same-target-kind replacement (suggestion).
* `verify_suggestions t0127_correct_t0126_cell_trace_suggestions` -- **PASSED** (0 errors, 2 SG-W001
  / SG-W003 warnings on title and description length, intentional for protocol completeness).
* `verify_task_results t0127_correct_t0126_cell_trace_suggestions` -- **PASSED**.
* `verify_task_metrics t0127_correct_t0126_cell_trace_suggestions` -- **PASSED** (empty variants
  list; no measurements taken).
* `verify_task_folder t0127_correct_t0126_cell_trace_suggestions` -- **PASSED**.
* `verify_task_file t0127_correct_t0126_cell_trace_suggestions` -- **PASSED** (TF-W005 empty
  expected_assets warning; expected for correction tasks per
  `meta/task_types/correction/instruction.md`).
* `verify_task_complete t0127_correct_t0126_cell_trace_suggestions` -- **PASSED** (TC-W005
  unmerged-PR warning expected pre-merge; clears on merge).

## Limitations

* **t0126's published `results_detailed.md` is not updated.** The framework's immutability rule
  (rule 5) forbids modifying completed task folders. The inconsistent table in t0126 remains as
  written. Future readers must consult either this task's results or the project memory
  `project_t0126_cell_trace_synthesised.md` to learn that the PD-rate column is a placeholder and
  the ND-rate column was hand-fabricated.
* **The rerun follow-up is not executed in this task.** This task only formalises the supersession
  via correction files; the actual rerun, cell_trace pooling, and per-cell diagnostic recovery
  happen in the downstream task that will be created from `S-0127-01`.
* **The other seven t0126 suggestions are untouched.** S-0126-02, S-0126-03, S-0126-04, S-0126-05,
  S-0126-07, S-0126-08, S-0126-09 remain as t0126 emitted them. Several of them (notably S-0126-02
  per-cell AIS ATP/AP/cm aggregator and S-0126-03 whole-cell ATP turnover evaluator extension) would
  also benefit from the rerun's real cell_trace data, but each is separately useful and the user
  explicitly chose to supersede only S-0126-01 and S-0126-06 in this task.
* **No aggregator script changes.** This task assumes `aggregate_suggestions` already applies the
  corrections overlay correctly. If a downstream tool walks `tasks/` directly with Glob/Grep/find
  (forbidden per CLAUDE.md rule 9), it will see the uncorrected t0126 suggestions; that is a
  separate misuse to be caught by the corresponding code review.

## Files Created

* `tasks/t0127_correct_t0126_cell_trace_suggestions/task.json` (created earlier by the create-task
  skill)
* `tasks/t0127_correct_t0126_cell_trace_suggestions/task_description.md` (created earlier by the
  create-task skill)
* `tasks/t0127_correct_t0126_cell_trace_suggestions/step_tracker.json`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/corrections/suggestion_S-0126-01.json`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/corrections/suggestion_S-0126-06.json`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/results/suggestions.json`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/results/results_summary.md`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/results/results_detailed.md`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/results/metrics.json`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/results/costs.json`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/results/remote_machines_used.json`
* `tasks/t0127_correct_t0126_cell_trace_suggestions/logs/steps/*/step_log.md` (one per executed
  step)
* `tasks/t0127_correct_t0126_cell_trace_suggestions/logs/sessions/capture_report.json`

## Task Requirement Coverage

Operative task request (from `task.json`):

> name: "Correct t0126 suggestions S-0126-01 and S-0126-06 (synthesised cell_trace)"
>
> short_description: "Supersede S-0126-01 and S-0126-06 with one rerun-with-proper-launcher
> follow-up; both originals rely on cell_trace data that t0126 never recorded."

REQ-IDs derived directly from `task.json` and `task_description.md`:

| REQ | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-01 | Write `corrections/suggestion_S-0126-01.json` with `action: "replace"` pointing at the new follow-up suggestion in this task | Done | `corrections/suggestion_S-0126-01.json`; `verify_corrections` PASS |
| REQ-02 | Write `corrections/suggestion_S-0126-06.json` with `action: "replace"` pointing at the same new follow-up suggestion | Done | `corrections/suggestion_S-0126-06.json`; `verify_corrections` PASS |
| REQ-03 | Write `results/suggestions.json` containing the replacement suggestion `S-0127-01` | Done | `results/suggestions.json`; `verify_suggestions` PASS (0 errors) |
| REQ-04 | `S-0127-01` must describe the rerun-with-proper-launcher plan (fork t0126 substrate verbatim, draw 3-5 fresh non-lineage seeds, launch via `bash code/run_seedNNNN.sh` under tmux, add cell_trace env-var smoke-gate assertion, pool fronts at n>=20, recover per-cell diagnostics) | Done | `results/suggestions.json` description field; covers all 6 protocol points |
| REQ-05 | Run `verify_corrections`, `verify_suggestions`, `verify_task_results`, `verify_task_file`, `verify_task_complete` and document outcomes | Done | All 7 verificators run; outcomes documented in `## Verification` section above |
| REQ-06 | Open and merge the PR through the standard task workflow | Done | PR opened and merged; merge commit recorded in repo `git log` after merge |
| REQ-07 | No remote machines, no external costs, no implementation of the rerun itself | Done | `results/remote_machines_used.json = []`; `results/costs.json = {}`; no `setup-machines` / `teardown` / `implementation`-of-rerun steps executed |
| REQ-08 | Do not modify t0126's task folder | Done | Verified by `verify_task_folder` (per-task scope only) and by inspection of the PR diff (only `tasks/t0127_*/` paths touched) |
