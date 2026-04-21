---
spec_version: "3"
task_id: "t0022_modify_dsgc_channel_testbed"
step_number: 5
step_name: "research-internet"
status: "completed"
started_at: "2026-04-20T23:01:22Z"
completed_at: "2026-04-21T00:15:00Z"
---
## Summary

Produced `research/research_internet.md` covering NEURON-specific implementation conventions for the
new DSGC library asset: per-synapse NetCon scheduling for moving-bar drivers, SectionList / `forsec`
channel-modular layouts, post-2020 MOD files for Nav1.1 / Nav1.6 / Kv1.2 / Kv3, and Python
orchestration patterns for 12-angle tuning-curve sweeps. All six gaps from the `research_papers.md`
Gaps and Limitations section are cross-referenced with a resolution status. The verificator passes
with 0 errors and 0 warnings. Body word count 3073, 14 sources cited, 12 searches conducted, 3 new
papers discovered.

## Actions Taken

1. Ran prestep for `research-internet`, which created the `logs/steps/005_research-internet/` folder
   and marked the step in_progress.
2. Read `arf/specifications/research_internet_specification.md` and the `## Gaps and Limitations`
   section of `research/research_papers.md` to anchor the internet search on gaps not yet closed by
   the paper corpus.
3. Spawned a general-purpose subagent to run 12 web / ModelDB / GitHub / arXiv searches targeting
   NEURON HOC/Python conventions (moving-bar drivers, `forsec` layouts, per-dendrite synapse
   insertion), post-2020 channel-density numbers for Nav1.1/Nav1.6/Kv1.2/Kv3 in RGCs, ModelDB
   Poleg-Polsky 189347 forks, and multi-angle sweep orchestration.
4. Subagent wrote `research/research_internet.md` with YAML frontmatter, all 8 mandatory sections
   plus additional task-specific sections, explicit classifications for each research_papers.md gap,
   and two explicit testable hypotheses (subprocess vs in-process DSI variance; 10 ms E-I offset vs
   0.65-0.75 DSI envelope).
5. Subagent ran `flowmark` and `verify_research_internet`. Initial attempts surfaced spurious
   citation-regex matches inside backticked code spans (code containing `[...]` patterns looked like
   citation keys) and cross-references to paper-corpus keys not present in the Source Index; both
   were rewritten. Final verificator pass: 0 errors, 0 warnings.

## Outputs

* `tasks/t0022_modify_dsgc_channel_testbed/research/research_internet.md` (3073 words, 14 sources,
  12 searches, 3 discovered papers)
* `tasks/t0022_modify_dsgc_channel_testbed/logs/steps/005_research-internet/step_log.md`

## Issues

The verificator's inline-citation regex matches `[...]` patterns inside backticked code spans as
well as prose. Code snippets that contain literal bracket-word-bracket patterns (e.g. list literals
like `h.Vector([onset])`) have to be phrased to avoid looking like citation keys. This is a
verificator quirk rather than a task issue.
