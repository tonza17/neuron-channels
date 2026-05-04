---
spec_version: "2"
task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_completed: "2026-05-04"
status: "complete"
---
# Results Summary: Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

## Summary

Built a 54-d AIS+dendritic-spike-augmented Bed B substrate (de Rosenroll 2026 DSGC) by extending
t0078's `de_rosenroll_2026_dsgc_ais` library with Mg-block NMDA at all dendritic compartments and
Nav1.6 + NaP at distal-dendrite densities, then ran a small NSGA-II via pymoo (pop=24, gen=8 = **192
evaluations**) on a Vast.ai 64-core EPYC 7B13 instance for **$0.7458**. Hard biological lower bounds
(`nav16_ais` >= 0.25 S/cm² per Kole 2008; AIS-to-soma Nav ratio >= 5 per Werginz 2024 / Goethals
2020\) eliminated the t0078 iter-81 AIS-disabled-corner failure mode by construction. The run
completed cleanly with 5 non-dominated feasible Pareto cells out of 192 total. **Pass criterion (DSI
> = 0.4 AND PD >= 10 Hz) MISSED**: best Pareto cell sits at DSI 0.127 / PD 2.54 Hz (cell 141), and
> the closest-to-joint Pareto cell sits at DSI 0.000 / PD 9.25 Hz (cell 188, distance 0.850 from
> joint). The result is a **clean architectural negative outcome** strongly conditioned by the small
> NSGA-II budget — the 192-cell run on 54-d cannot be directly compared to t0078's 491-cell run on
> 49-d.

## Metrics

* **Final Pareto front (5 cells)**:
  * Cell 141 (max DSI on Pareto): DSI **0.127**, PD **2.54 Hz**, gen 1
  * Cell 58: DSI 0.015, PD 8.57 Hz, gen 0
  * Cell 153: DSI 0.026, PD 8.46 Hz, gen 1
  * Cell 188 (max PD on Pareto): DSI **0.000**, PD **9.25 Hz**, gen 1
  * Cell 190: DSI 0.052, PD 4.00 Hz, gen 1
* **Closest-to-joint Pareto cell (Euclidean distance to (0.4, 10))**: cell 188 at distance **0.850**
  — DSI short by 0.40, PD short by 0.75 Hz
* **Joint pass criterion (DSI >= 0.4 AND PD >= 10 Hz)**: **NOT MET** — no Pareto cell satisfies
  either bound
* **Total cells evaluated**: **192** (all feasible: 168 / 192 = 87.5%; unstable: 0 / 192)
* **Cells with DSI > 0.01**: 17 / 192 (8.9%) — Pareto exploration in 54-d at pop=24 / gen=8 found
  very few non-trivial DSI configurations
* **Compute**: Vast.ai instance 36137287 (AMD EPYC 7B13, 64 effective cores, 503 GB RAM, Norway) at
  **$0.2382/hr** for **3.1311 h** = **$0.7458** total (well under the $1.50 envelope and 63% under
  the $2.00 hard cap). NSGA-II loop alone cost $0.5458 over ~38 minutes.
* **Versus t0078 (49-d AIS-augmented BoTorch run)**: t0078's joint-closest cell sat at DSI 0.316 /
  PD 9.68 Hz with HV 11.41 across 491 cells; t0080's joint-closest sits at DSI 0.000 / PD 9.25 Hz on
  192 cells. The Pareto front is dramatically weaker, but the run budget is also 2.6x smaller and
  the parameter space is 5d larger — direct comparison is not architecturally clean.

## Verification

* `verify_machines_destroyed.py t0080_bedb_mobo_v3_dendritic_spike_nsga2` -- PASSED (0 errors, 1
  expected RM-W001 warning).
* `verify_research_papers.py` / `verify_research_internet.py` / `verify_research_code.py` -- PASSED
  0 errors / 0 warnings each.
* `verify_plan.py t0080_bedb_mobo_v3_dendritic_spike_nsga2` -- PASSED 0 errors / 0 warnings.
* `verify_library_asset.py` (de_rosenroll_2026_dsgc_ais_dendritic_spike) -- to be run at reporting.
* `verify_task_results.py`, `verify_task_metrics.py`, `verify_task_file.py`, `verify_logs.py` -- to
  be run at reporting step.
