---
spec_version: "3"
task_id: "t0106_long_pdnd_nsga2_300gen"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-17T00:27:19Z"
completed_at: "2026-05-18T01:18:30Z"
---
# Step 9: implementation

## Summary

Forked the t0104 evaluator into `tasks/t0106_long_pdnd_nsga2_300gen/code/`, applied the 2-direction
+ ratio DSI + 300-gen + per-25-gen Pool restart patches from `research/research_code.md`, ran the
  5-step local smoke gate (all green), provisioned a Vast.ai EPYC 7B13 / RTX 3060 Ti instance, SCP'd
  code + 13 MOD files, compiled with `nrnivmodl`, and launched NSGA-II in tmux session
  `t0106-nsga2`. The driver completed 40 generations (3,744 cell evaluations) over 24.1 h before the
  operator stop signal triggered a clean halt at the gen 39 boundary.

## Actions Taken

1. Patched constants (N_GEN 300, N_EVAL_SEEDS 3, N_DIRECTIONS 2), forked evaluator and driver files,
   added `OperatorStopTermination`, extended `_GenerationCallback` to write `hv_trace.jsonl`, added
   per-25-gen `PerGenerationPoolRestart`, wrote `code/test_evaluator_dsi_guard.py` (5 tests, all
   green).
2. Ran the 5-step local smoke gate (DSI in [0,1], PD in [0,200], silence-guard sensitivity at {5,
   10, 20}, ratio-DSI synthetic check at PD=5/ND=1 -> 0.6667, pytest). All passed.
3. Provisioned Vast.ai instance 36908271 (EPYC 7B13, 42.67 eff cores, 503 GB RAM, $0.4111/hr, Texas
   US) after 2 failed `vastai create` attempts ($0.0068 wasted).
4. SCP'd code + 13 MOD files, compiled MODs, launched NSGA-II in tmux session `t0106-nsga2`.
5. Polled `hv_trace.jsonl` and `all_evaluations_seed44.json` over 24.1 h; pulled snapshots at gen 11
   / 21 / 24 / 38 / 39 for per-cell analyses.
6. Dropped `intervention/stop.md` after gen 38 once HV plateaued at +2.2% and all top-40 cells were
   joint-pass. Driver halted cleanly at the gen 39 boundary; wrote `pareto_front_seed44.json` with 7
   strict Pareto cells.
7. SCP'd all final artifacts back into `results/data/` and `logs/steps/009_implementation/`. Built
   `code/build_t0106_plots.py` and rendered 4 final figures: `top50_morphologies.png`,
   `pareto_front.png`, `hv_vs_gen.png`, `asymmetry_distribution.png`.

## Outputs

* `code/` — forked + patched evaluator (28 .py files), 13 MOD files, new `build_t0106_plots.py`,
  new `test_evaluator_dsi_guard.py`
* `results/data/all_evaluations_seed44.json` — 3,744 cells across 40 gens
* `results/data/pareto_front_seed44.json` — 7 strict Pareto cells
* `results/data/hv_trajectory_seed44.json` — 40-row HV history
* `results/data/init_pop_seed44.json` — LHS-init population
* `results/data/evaluation_seeds.json` — N_EVAL_SEEDS = 3 configuration
* `results/data/nsga2_checkpoint_seed44.json` — final population snapshot
* `logs/steps/009_implementation/hv_trace.jsonl` — 40-line HV trace
* `logs/steps/009_implementation/nsga2_run.log` — full driver stdout
* `logs/steps/009_implementation/launch_record.json` — launch metadata + smoke gate results
* `logs/steps/009_implementation/snapshots/` — five mid-run cell-data snapshots
* `results/images/{top50_morphologies,pareto_front,hv_vs_gen,asymmetry_distribution}.png`
* `intervention/stop.md` — operator stop signal record

## Headline Numbers

* 40 generations, 3,744 evaluations completed
* Final HV = 122.0288 (start 0.2015 -> 604x growth)
* 123 unique joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) — zero in the entire t0080 -> t0104
  lineage
* Best cell: DSI = 0.9606, PD = 82.86 Hz (gen 19)
* Best PD: 122.6 Hz at DSI = 0.92 (gen 36/38)
* Top-50 morphology archetype split: 35 ND-soma / 4 central / 1 PD-soma
* Cost: $9.89 productive + ~$0.40 idle/setup ~ $10.30 total of $25 cap

## Issues

* `dill` checkpoint of the pymoo `Algorithm` failed every gen with
  `NotImplementedError: pool objects cannot be passed between processes or pickled`. Driver fell
  back to writing `all_evaluations_seed44.json` + plain-JSON population snapshots, so resume
  capability is preserved through those.
* Per-25-gen `Pool` restart fires off-by-one (gen 26 instead of gen 25). Harmless; worth fixing in a
  follow-up.
* `init_task_folders.py` rejects absolute `--step-log-dir` paths on Windows. Worked around by
  writing the step log manually. Worth a small infrastructure fix later.
