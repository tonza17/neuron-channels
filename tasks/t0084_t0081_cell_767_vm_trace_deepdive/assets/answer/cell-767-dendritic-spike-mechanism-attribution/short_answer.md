---
spec_version: "2"
answer_id: "cell-767-dendritic-spike-mechanism-attribution"
answered_by_task: "t0084_t0081_cell_767_vm_trace_deepdive"
date_answered: "2026-05-05"
---
# Cell 767 DSI Mechanism Attribution

## Question

Which biophysical mechanism - NMDA Mg-block, distal Nav1.6, NaP, or a combination - is responsible
for cell 767's joint-pass DSI improvement in the v3 Bed B substrate?

## Answer

Cell 767's PD/ND difference in integrated dendritic current is attributed primarily to **NaP
sustained depolarisation** (0.0% NMDA, 7.0% Nav1.6, 93.0% NaP) over the response window [200, 1200]
ms. Cells 637 and 762 show the same NaP-dominant signature (98.5% and 99.9%), suggesting NaP is a
systematic feature of the v3 Pareto near-pass cluster rather than idiosyncratic to cell 767. This
single-replicate deep-dive did not reproduce cell 767's original 5-seed joint-pass DSI of 0.494
(re-evaluated DSI = 0.000), so the attribution describes the underlying biophysical signature of
these parameters rather than confirming a per-trial joint-pass mechanism; multi-replicate
confirmation requires t0083 or a follow-up multi-seed study.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0081_bedb_v3_warmstart_nsga2`
