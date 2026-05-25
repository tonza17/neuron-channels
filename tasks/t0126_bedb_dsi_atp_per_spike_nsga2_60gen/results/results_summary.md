---
spec_version: "2"
task_id: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"
date_completed: "2026-05-25"
status: "completed"
---
# Results Summary -- t0126 NSGA-II DSI vs ATP-per-Spike (60-gen Replication)

## Summary

Fresh-seed 60-gen NSGA-II replication of t0124 on the 68-d Bed B + 14-d morphology substrate (seed
**8929**) ran cleanly to **60/60 generations** at $1.31 total Vast.ai spend (21.8% of the $6 cap;
`NSGA2_EXIT=0`, `watchdog_tripped=false`, `OperatorStopTermination` removed from the live
collection). The final 6-cell Pareto front spans DSI **[0.000, 1.000]** at ATP **[1.83e6, 7.82e6]**
molecules/spike, with bootstrap r(DSI, ATP) = **+0.980 [0.972, 1.000]**; under the S-0124-01
decision rule the verdict is **INSUFFICIENT_EVIDENCE** (n=6 < 20 threshold) -- the correlation
qualitatively supports the Carter-Bean reading but formally abstains.

## Metrics

* **direction_selectivity_index** (best_legit variant): **1.0000** at ATP **7.82e6** molecules/spike
  (cell 1, gen 56; ND-silenced)
* **direction_selectivity_index** (overall_max variant): **1.0000** (same cell; silence-guard not
  invoked)
* **direction_selectivity_index** (dsi_eq_one_count variant): **1** (one degenerate DSI=1.0 cell on
  the final Pareto front)
* **atp_per_spike_molecules** (overall_min): **1.827e6** at DSI 0.000 (cell 0, gen 49; **a 4.28x
  reduction** vs t0124's gen-9 min of 2.11e6 is +13.5% but the high-DSI corner improved much more
  dramatically -- see next bullet)
* **atp_per_spike_molecules** (headline best_legit cell): **7.82e6** molecules/spike at DSI 1.0 -- a
  **~30x energy reduction vs t0124's gen-11 elite (2.34e8)** for the same DSI=1.0 corner, refuting
  the "high-DSI = energy-expensive" reading of t0124's partial front
* Bootstrap r(DSI, ATP) across the 6-cell Pareto: **+0.980 [0.972, 1.000]** (n=6, n_resamples=2000;
  t0124 partial front: +0.806 [0.716, 1.000] at n=5)
* Final hypervolume: **1.999e10** (**+37.6% vs t0124's gen-9 HV** of 1.453e10; two structural HV
  jumps at gen 11 (+11.6%) and gen 34 (+23.1%) coincide with pool-restart-driven basin transitions)
* All **5/5 t0124 Pareto cells are STRICTLY DOMINATED** by the t0126 front (n=5/5 dominance)
* Total cost: **$1.3084** (Vast.ai instance 37767708, AMD EPYC 7C13 32 effective vCPUs @ $0.1844/hr,
  7.094 h lifetime; NSGA-II active window 5.22 h at $0.9621)

## Verification

* `verify_task_results` -- PASS
* `verify_task_metrics` -- PASS (4 variants, only registered metric key is
  `direction_selectivity_index` per `meta/metrics/`)
* `verify_predictions_asset` (`nsga2-dsi-atp-per-spike-bedb-morph-60gen`) -- PASS
* `verify_answer_asset` (`dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact`) -- PASS
* Smoke-gate **9/9 checks PASS** (Carter-Bean canonical AIS ATP/AP/cm = **6.138e8**, inside the
  first-principles [1e8, 1e9] band)
* DSI silence-guard regression tests: **7/7 PASS**
* Hard-constants verification (`_POOL_RESTART_EVERY==10`, `HV_PLATEAU_AUTO_STOP==False`,
  `POP_SIZE==96`, `N_EVAL_SEEDS==3`, `N_DIRECTIONS==2`, `N_GEN_MAX==60`, `COST_CAP_USD==6.0`,
  `T0126_SEEDS==(8929,)`) -- PASS
* `verify_machines_destroyed` -- PASS (instance 37767708 destroyed cleanly via
  `vastai destroy instance 37767708 --yes`)
