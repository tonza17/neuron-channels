---
spec_version: "2"
answer_id: "t0106-dsi-pd-factor-decomposition-strict-cohort"
answered_by_task: "t0108_t0106_cluster_factor_dsi05_pd10"
date_answered: "2026-05-18"
---

# F10 is the single joint DSI-PD trade-off factor in the strict cohort

## Question

Which factors (combinations of the 68 input parameters) explain DSI and PD diversity in the strict
cohort (DSI > 0.5 AND PD > 10), and is there a joint factor?

## Answer

Varimax factor analysis on the z-scored 68-d matrix of the 150-cell strict cohort retains 10
factors and identifies F10 as the single joint DSI-PD factor (|r_DSI|=0.31, |r_PD|=0.45). PD-rate
diversity is otherwise dominated by F1 (r=−0.545; SK_TERMINAL, SK_MID, CAT, NAV16_AIS, NAP_MID
loadings); DSI diversity is split between F5 (r=−0.325) and F10 (r=+0.313). F10's positive
direction raises DSI but suppresses PD, making it a trade-off axis along CAD_DEPTH, CAL, W_ACH,
branch_prob_per_um, and mean_segment_length. No single factor jointly increases both objectives in
this cohort.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0108_t0106_cluster_factor_dsi05_pd10`
