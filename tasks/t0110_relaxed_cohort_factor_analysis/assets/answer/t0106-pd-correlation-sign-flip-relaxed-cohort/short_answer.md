---
spec_version: "2"
answer_id: "t0106-pd-correlation-sign-flip-relaxed-cohort"
answered_by_task: "t0110_relaxed_cohort_factor_analysis"
date_answered: "2026-05-18"
---

# All-negative PD column is a truncated-cohort artifact

## Question

Does t0108's all-negative PD-rate factor-correlation column persist if we re-run the same
varimax factor analysis on a less-truncated cohort, or is it a cohort-selection artifact?

## Answer

It is a truncated-cohort artifact. Re-running the same varimax FA pipeline on 247 t0106 cells
at the relaxed threshold DSI > 0.2 AND PD > 3 Hz (vs t0108's 150 cells at DSI > 0.5 AND PD > 10)
produces **2 of 10 factors with positive r(PD)** (F2 +0.136 at p=0.033, F4 +0.048 n.s.). DSI
sign distribution flips from t0108's 4 / 6 (positive / negative) to 6 / 4. F1, the dominant
axis in both cohorts, is also reinterpreted: in t0108 it appeared as a PD-only dropper
(r_DSI = +0.06) because the DSI ceiling masked the DSI effect, but in t0110 it is revealed as
the **joint failure axis** (r_DSI = −0.37, r_PD = −0.75). F2's loadings (high persistent-Na,
low Mg-block, low primary-BK) identify "more persistent sodium → more firing" as a real
PD-positive direction that the strict cohort completely hid.

## Sources

* Task: `t0106_long_pdnd_nsga2_300gen` — source cells.
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` — strict-cohort comparison baseline.
* Task: `t0110_relaxed_cohort_factor_analysis` — this task.
