---
spec_version: "3"
task_id: "t0112_t0106_seed77_replicate"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-19T14:19:31Z"
completed_at: "2026-05-19T14:31:00Z"
---
# Step 6: Research Code

## Summary

Reviewed every relevant prior-task code asset in the t0080 -> t0106 NSGA-II lineage and produced
`research/research_code.md` identifying exactly what must be copied into t0112's `code/`, what must
remain as upstream cross-task imports, and where the two minimum-change constants live. The
verificator passes with zero errors and zero warnings.

## Actions Taken

1. Spawned a `/research-code` subagent (general-purpose) restricted to the t0112 worktree, with
   explicit constraints reminding it that cross-task imports from other tasks' `code/` directories
   are forbidden and that t0106 non-library code must be copied verbatim.
2. Subagent surveyed t0106 code tree (34 modules, 8,117 lines), located `_POOL_RESTART_EVERY` at
   `nsga2_driver.py:97`, `T0106_SEEDS` at `constants.py:58`, and the t0106 predictions asset schema.
3. Subagent wrote `research/research_code.md` covering reuse plan, copy plan, exact patch surface
   (three lines in two files plus N_GEN bump), upstream imports, and predictions asset schema.
4. Ran `verify_research_code.py` — passed with zero errors and zero warnings.
5. Ran `flowmark --inplace --nobackup` with `PYTHONUTF8=1` (Windows charmap default cannot decode
   the Greek rho in the document; UTF-8 env var resolves it).

## Outputs

* `tasks/t0112_t0106_seed77_replicate/research/research_code.md`
* `tasks/t0112_t0106_seed77_replicate/logs/steps/006_research-code/step_log.md`

## Issues

Flowmark required `PYTHONUTF8=1` on Windows to decode the markdown file (cp1252 default fails on
`ρ`). This is a known Windows-only flowmark ergonomics issue and is not specific to this task.
