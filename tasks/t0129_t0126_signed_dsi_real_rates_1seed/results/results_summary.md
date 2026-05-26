---
spec_version: "2"
task_id: "t0129_t0126_signed_dsi_real_rates_1seed"
date_completed: "2026-05-26"
status: "results_complete"
---
# Results Summary -- t0129 NSGA-II Signed DSI vs ATP-per-Spike (60-gen, Seed 3517)

## Summary

Forked-and-corrected re-run of t0126's NSGA-II protocol on one fresh GA seed (**3517**) with signed
antipodal DSI replacing vector-sum DSI and real per-cell PD/ND firing rates replacing t0126's
`pd_rate_hz = 40` synthesised placeholder. The run completed all **60/60 generations** cleanly
(`NSGA2_EXIT=0`, `watchdog_tripped=false`) at **$0.965** total Vast.ai spend (12.1% of the $8 cap),
producing a **9-cell final Pareto front** spanning signed DSI **[0.000, 1.000]** at ATP
**[0.78e6, 6.66e6]** molecules/spike, and surfacing **95 viable cells** with genuinely reversed
preference (`dsi_signed < 0`, deepest reversal **-0.778**) that vector-sum DSI would silently
collapse to positive magnitudes.

## Metrics

* **direction_selectivity_index** (headline, signed antipodal): **1.0000** at ATP **6.66e6**
  molecules/spike (Pareto cell 4, gen 57; canonical ND-silenced corner, PD=6.43 Hz / ND=0.0 Hz)
* **direction_selectivity_index** (Pareto-median, signed antipodal): **0.5714** at ATP **3.63e6**
  molecules/spike (Pareto-median PD rate **2.62 Hz**, ND rate **0.71 Hz** -- far below t0126's
  placeholder 40 Hz)
* **atp_per_spike_molecules** (Pareto min): **7.80e5** at DSI 0.000 (Pareto cell 3, gen 56; **2.3x
  reduction** vs t0126's 1.83e6, attributable to seed variation on a single-seed run)
* **n_viable_cells_with_negative_DSI**: **95 / 5,496 viable** (1.7%), deepest reversal **dsi_signed
  = -0.778** -- structure invisible under t0126's vector-sum DSI
* **t0126-Pareto cells with `dsi_vector_sum > 0.5`**: **4 / 6** (upper bound on potential sign-flip
  population; true sign-flip count is **unknowable** because t0126 did not persist per-direction
  spike counts)
* **Final hypervolume**: **1.9996e+10** at gen 60 (3.385 h active NSGA-II window on Vast.ai EPYC
  7C13, 32 effective vCPUs)
* **Total cost**: **$0.965** ($0.647 active NSGA-II window + $0.318 setup/teardown idle; Vast.ai
  instance 37924958)

## Verification

* `verify_task_metrics` -- **PASSED** (3 variants, only registered metric key is
  `direction_selectivity_index` per `meta/metrics/`; 0 errors, 0 warnings)
* `verify_task_folder` -- **PASSED** (0 errors, 1 warning: empty `logs/searches/`)
* Predictions asset `nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129` -- spec-compliant structure
  (verified by `verify_task_folder` asset content check; no dedicated predictions verificator)
* Answer asset `does-signed-dsi-change-t0126-pareto-structure` -- spec-compliant structure (verified
  by `verify_task_folder` asset content check; no dedicated answer verificator)
* Full `verify_task_results` will be run in the reporting step (step 015)
