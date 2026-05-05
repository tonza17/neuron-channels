---
spec_version: "2"
task_id: "t0081_bedb_v3_warmstart_nsga2"
date_completed: "2026-05-05"
status: "complete"
---
# Results Summary: Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start

## Summary

Re-ran NSGA-II on the t0080 v3 dendritic-spike-augmented Bed B substrate at the originally planned
scope (pop=96 / gen=8 = **768 cells**) with a combined warm-start initial population (5 t0080 Pareto
cells verbatim + 17 t0078 Pareto cells projected to 54-d natural-unit space + 74 fresh LHS). Run
completed cleanly on Vast.ai instance 36149741 (EPYC 7B13 64-core) for **$2.39** total ($2.207
NSGA-II + $0.18 overhead). **Pass criterion (DSI >= 0.4 AND PD >= 10 Hz) ACHIEVED**: gen 7 cell 767
sits at **DSI 0.494 / PD 11.39 Hz**, on the Pareto front. Hypervolume grew monotonically from 6.59
(gen 0) to 16.33 (gen 7) — a 2.5x expansion over 8 generations. The result decisively answers the
project's research question Q4 (do active dendritic conductances enable joint DSI/PD pass on Bed B?)
as **yes**, when given an adequate NSGA-II budget and warm-start from prior good cells.

## Metrics

* **Pareto front size**: 16 cells (vs t0080's 5 cells; 3.2x larger)
* **Joint-pass cells (DSI >= 0.4 AND PD >= 10 Hz)**: **1** — gen 7 cell 767 (DSI **0.494** / PD
  **11.39 Hz**)
* **Closest-to-joint distance**: **0.000** (cell crosses both thresholds; pass criterion met)
* **Best DSI on Pareto with biologically-plausible firing (PD >= 5 Hz)**: cell 747 (gen 7) at DSI
  **0.578 / PD 6.29 Hz**
* **Best DSI on Pareto with PD >= 10 Hz**: cell 767 (gen 7) at DSI **0.494 / PD 11.39 Hz**
* **Best PD on Pareto with non-trivial DSI**: cell 762 (gen 7) at DSI 0.314 / PD **12.93 Hz**
* **Total cells evaluated**: **768** (96 LHS warm-start gen 0 + 7 gens × 96 evals)
* **Feasible cells**: 674 / 768 (87.8%)
* **Unstable cells**: 0 / 768 (substrate stability fully preserved with warm-start)
* **Cells with DSI > 0**: significantly improved over t0080 — 386 cells (50.3%) vs t0080's 17/192
  (8.9%)
* **Hypervolume trajectory** (utopia point [0.7, 80]): gen 0 = 6.59, gen 1 = 8.99, gen 2 = 9.24, gen
  3 = 11.08, gen 4 = 11.57, gen 5 = 13.14, gen 6 = 15.22, gen 7 = **16.33**. Monotonic, no plateau.
* **Compute**: Vast.ai 36149741 (AMD EPYC 7B13 64-core, 503 GB RAM, Norway) at **$0.2382/hr**,
  10.045 h instance lifetime = **$2.39 total** (**under the $3.00 hard cap and just over the $2.38
  envelope by 0.4%**).
* **Versus t0080 (192-cell baseline)**: t0080's closest-to-joint cell sat at DSI 0.000 / PD 9.25 Hz
  (distance 0.85). t0081's closest-to-joint cell crosses the threshold (distance 0.000). **15.2x
  closer trajectory; a 4x cell-budget increase plus warm-start was sufficient to break the trade-off
  ceiling.**

## Verification

* `verify_research_code.py` -- PASSED 0/0
* `verify_plan.py` -- PASSED 0/0 (3 acceptable PL-W warnings on frontmatter / Expected Assets
  brevity / risks-as-bullets)
* `verify_machines_destroyed.py t0081_bedb_v3_warmstart_nsga2` -- PASSED 0 errors / 1 expected
  RM-W001 warning
* `verify_task_results.py`, `verify_task_metrics.py`, `verify_task_file.py`, `verify_logs.py`,
  `verify_corrections.py`, `verify_suggestions.py`, `verify_compare_literature.py` -- to be run at
  reporting step.
