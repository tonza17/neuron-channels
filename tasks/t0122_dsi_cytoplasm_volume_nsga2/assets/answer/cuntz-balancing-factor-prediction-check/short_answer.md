---
spec_version: "2"
answer_id: "cuntz-balancing-factor-prediction-check"
answered_by_task: "t0122_dsi_cytoplasm_volume_nsga2"
date_answered: "2026-05-24"
---
## Question

Does NSGA-II with a cytoplasm-volume cost objective produce a high-DSI front in Cuntz 2010's
predicted balancing-factor [0.2, 0.7] band?

## Answer

Yes. The t0122 single-seed NSGA-II run produced a high-DSI Pareto front whose top-10 cells (ranked
by DSI) place 10 of 10 (finite bf) cells inside the Cuntz 2010 [0.2, 0.7] empirical band. Adding the
cytoplasm-volume cost objective pushed the optimiser toward morphologies consistent with the Cajal
wiring-economy principle. This is evidence in favour of using cytoplasm volume as a biological-cost
regulariser in subsequent DSGC MOBO runs.

## Sources

* Paper: `10.1371_journal.pcbi.1002107` (Cuntz et al. 2010)
* Task: `t0122_dsi_cytoplasm_volume_nsga2`
* Predictions asset:
  `tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/predictions/nsga2-cytoplasm-volume-bedb-morph`
* Chart: `tasks/t0122_dsi_cytoplasm_volume_nsga2/results/images/cuntz_balancing_factor_top10.png`
