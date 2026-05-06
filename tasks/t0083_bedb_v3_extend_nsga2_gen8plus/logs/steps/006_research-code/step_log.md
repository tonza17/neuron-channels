---
spec_version: "3"
task_id: "t0083_bedb_v3_extend_nsga2_gen8plus"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-05T13:33:32Z"
completed_at: "2026-05-05T13:43:00Z"
---
# Step 6 -- Research Code

## Summary

Subagent reviewed t0081's NSGA-II harness, the t0080 `de_rosenroll_2026_dsgc_ais_dendritic_spike` v3
substrate library, and pymoo internals to produce a complete reuse-and-extension plan. Key finding:
the pymoo skip-evaluation pattern requires `Population.new("X", X, "F", F, "G", G)` plus
`ind.evaluated.update(["F", "G"])` to make `Evaluator.eval` skip re-evaluation. The gen-7 survivor
pool must be reconstructed from t0081's saved `all_evaluations.json` (768 cells = 96-per-gen across
gens 0-7) by loading gens 6+7 (192 records), substituting unstable cells with worst-case sentinels,
and running `RankAndCrowding().do(problem, pop, n_survive=96)` with the same `LHS_SEED=1` t0081
used. HV-plateau watchdog cleanest as a pymoo `Termination` subclass combined with
`MaxGenerationTermination(10)` via `TerminationCollection`.

## Actions Taken

1. Spawned `general-purpose` subagent with the `/research-code` skill directive and t0083 task
   context.
2. Subagent read `arf/skills/research-code/SKILL.md` and followed the research workflow.
3. Subagent reviewed `tasks/t0081_bedb_v3_warmstart_nsga2/code/` for harness structure,
   `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/` for the substrate library, and pymoo source for
   skip-evaluation internals.
4. Subagent wrote `research/research_code.md` with mandatory sections (Objective, Background,
   Methodology Review, Key Findings, Recommended Approach, References).
5. Subagent ran `verify_research_code` -- PASSED 0 errors / 0 warnings.

## Outputs

* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/research/research_code.md`
* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/logs/steps/006_research-code/step_log.md`

## Issues

Two open questions raised for the planning step:

1. **Deterministic tie-break recovery in RankAndCrowding**: pymoo's crowding-distance tie-break uses
   `randomized_argsort` keyed on `random_state`. The internal random_state evolution across t0081's
   gen 0-7 is opaque from the saved JSON. The research recommends a unit test
   (`test_reload_gen7.py`) that verifies the rebuilt 96-cell survivor subset matches t0081's saved
   `pareto_front.json` exactly. If the test fails, accept a near-equivalent survivor set (NSGA-II is
   robust to small perturbations of starting populations) -- planning step to decide.

2. **Smoke-gate reference cells**: task description says reuse t0081 harness verbatim but does not
   specify which cells the smoke gate should re-evaluate. Research recommends 5 cells including cell
   767 (joint-pass) plus 4 Pareto cells across gens 4-7. Planning step to confirm.
