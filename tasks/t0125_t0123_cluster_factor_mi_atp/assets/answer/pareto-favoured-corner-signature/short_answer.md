---
spec_version: "2"
answer_id: "pareto-favoured-corner-signature"
answered_by_task: "t0125_t0123_cluster_factor_mi_atp"
date_answered: "2026-05-25"
---
## Question

Which combination of electrophys + morphology parameters most distinguishes the Pareto-favoured
corner (high MI, low ATP) from the Pareto-dominated corner (low MI, high ATP) in the t0123
substrate, and what are the per-corner cell counts and means?

## Answer

The top 5 parameters by absolute z-score difference between the high_mi_low_atp and low_mi_high_atp
corners (each cell z-scored against the full-cohort standardiser, mean per corner) are: KDR_GBAR
(-1.19), branch_length_cv (-1.08), BK_SOMA_GBAR (-1.06), IH_GBAR (-1.06), and RA_OHM_CM (+1.06). The
Pareto-favoured corner contains 1221 spiking cells (mean MI = 0.984 bits, mean ATP = 5.34e6
molecules / spike, mean DSI = 0.237, mean PD rate = 2.61 Hz) versus 1220 cells in the dominated
corner (mean MI = 0.063 bits, mean ATP = 2.61e7 molecules / spike, mean DSI = 0.016, mean PD rate =
12.3 Hz). The diagonal imbalance (1221 + 1220 = 2441 cells vs 343 + 341 = 684 off-diagonal) is the
joint Pareto signature.

## Sources

* Task: `t0125_t0123_cluster_factor_mi_atp`
* Task: `t0123_bedb_mi_atp_per_spike_nsga2`
* Paper: `10.1371_journal.pcbi.1002107`
* Paper: `10.3389_neuro.01.1.1.001.2007`
* Paper: `10.1038_nature16468`
