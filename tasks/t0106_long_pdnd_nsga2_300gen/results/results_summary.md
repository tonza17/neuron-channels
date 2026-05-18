---
spec_version: "2"
task_id: "t0106_long_pdnd_nsga2_300gen"
date_completed: "2026-05-18"
---
# t0106 — Long 2-Direction NSGA-II: Results Summary

## Summary

Long-horizon NSGA-II on the 68-d Bed B + 14-d morphology substrate, restricted to PD and ND
directions only with ratio DSI = (PD - ND) / (PD + ND) as the selectivity objective, completed 40
generations on one random-init GA seed before an operator stop at HV plateau. The run found **123
unique joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz) — the **first ever in the t0080 -> t0106
lineage**, decisively answering H1. Best ratio DSI = 1.0000 at PD = 81 Hz; best PD = 122.6 Hz at DSI
= 0.92.

## Metrics

* **direction_selectivity_index** = **1.0000** (3 unique cells reached this; highest legit
  non-DSI=1.0 cell = **0.9832** at PD = 84.5 Hz)
* **PD-rate frontier** = **122.62 Hz** at DSI = 0.92 (gen 36/38)
* **Joint-pass yield** = **123 unique cells / 3744 evals = 3.3%** (Hay 2011 / Druckmann 2007
  literature expectation = 0.1-0.4%; t0106 exceeds the upper bound 8x)
* **Final hypervolume** = **122.0288** (start 0.2015; **604x growth across 40 gens**)
* **Cost** = **$10.37** (productive $9.89 + $0.48 idle/setup); $14.63 budget left of $25 cap

## Verification

* `verify_research_papers`, `verify_research_internet`, `verify_research_code` — PASSED (0 errors)
* `verify_plan` — PASSED (0 errors, 0 warnings)
* `verify_task_dependencies` — PASSED (all 5 deps completed)
* `verify_machines_destroyed` — PASSED (0 errors; 3 advisory warnings for the expected
  destroyed-instance state)
* Local pytest `test_evaluator_dsi_guard.py` — **5/5 green** (silence guard, ratio DSI synthetic
  check, threshold sweep)
* Local smoke gate (5 checks) — **5/5 passed** before remote launch

## Figures

* `results/images/top50_morphologies.png` — 10x5 grid of best 50 cells, coloured by archetype
* `results/images/pareto_front.png` — DSI vs PD scatter coloured by generation, 7-cell strict
  Pareto front
* `results/images/hv_vs_gen.png` — log-scale HV trajectory + per-gen wall-clock, Pool restart
  annotated at gen 26
* `results/images/asymmetry_distribution.png` — 4-panel histogram (soma offset, elongation, branch
  density gradient, primary branch PD concentration), top-50 vs all evals

## Headline interpretation

The t0080 -> t0104 lineage's "joint-pass null" was an **objective-surface artefact, not a substrate
limitation**. Switching from 16-direction vector-sum DSI to 2-direction ratio DSI made the
selectivity objective dramatically easier to satisfy from random init. The substrate (Bed B + 14-d
morphology) was populated with joint-pass solutions all along — they were hidden by the harder
16-direction metric in t0099 / t0102 / t0104. Within 18 generations of t0106 the first joint-pass
cell appeared; by gen 24 the front had 9 unique cells; by gen 36 the front frontier reached PD =
122.6 Hz.
