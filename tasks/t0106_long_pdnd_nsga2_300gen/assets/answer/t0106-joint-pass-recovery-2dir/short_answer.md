---
spec_version: "2"
answer_id: "t0106-joint-pass-recovery-2dir"
answered_by_task: "t0106_long_pdnd_nsga2_300gen"
date_answered: "2026-05-18"
---
# 2-direction NSGA-II recovers joint-pass cells

## Question

Does long-running 2-direction NSGA-II on the 68-d Bed B + 14-d morphology substrate recover strict
joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) from random init, and where does hypervolume actually
plateau on this landscape?

## Answer

Yes. Across 3,744 evaluations from a single random-init GA seed running 40 generations of
2-direction NSGA-II with ratio DSI, **123 unique cells cleared the strict joint-pass corner** (DSI
>= 0.5 AND PD >= 30 Hz) — the first joint-pass cells anywhere in the t0080 - t0104 NSGA-II
lineage, every prior task of which returned zero. Hypervolume climbed 604x from 0.2015 at gen 1 to
122.0288 at gen 40 and was effectively flat (under 1% per 60 min) from gen 36 onward, marking the
empirical convergence point on the 2-direction substrate. The reformulation from 16-direction
vector-sum DSI to 2-direction ratio DSI — not the longer generation budget — drove the
breakthrough.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0099_random_init_pareto_robustness`
* Task: `t0102_seedscale_n4_gen20`
* Task: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
