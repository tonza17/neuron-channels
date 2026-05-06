---
spec_version: "2"
answer_id: "are-cluster-motifs-mechanistically-distinct"
answered_by_task: "t0088_recluster_marginals_and_vm_motifs"
date_answered: "2026-05-06"
---
# Cluster Motif Mechanism Distinctness

## Question

When the t0086 13-cell pool of 6 Genuine + 7 Marginal cells is re-clustered in the t0080 54-d v3
parameter space and a t0084-style Vm-trace deep-dive is run at 16 directions on per-cluster
representative cells, are the resulting clusters mechanistically distinct (different dominant
channel mechanisms across clusters) or do they share the same mechanism with parameter-scale
variation?

## Answer

No -- the clusters are not mechanistically distinct. The 13-cell re-cluster produces 4 clusters
(best_k = 4 by silhouette) and all 4 cluster representatives are NaP-dominant in PD-minus-ND
attribution at 16 directions (frac NaP 0.874-0.997, frac Nav1.6 0.003-0.126, frac NMDA = 0.000). The
verdict is `shared_mechanism_different_scale`: clusters differ in 54-d parameter scale but not in
which channel drives the PD response. This extends t0084's NaP-dominant cell 767 finding to the
wider 13-cell pool of joint-pass / near-joint-pass cells in the v3 substrate.

Per-cluster fractional channel attribution table (PD = 0 deg, ND = 180 deg, response window
[200, 1200] ms):

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | 0.988 | nap |
| 1 | 1634 | 0.000 | 0.126 | 0.874 | nap |
| 2 | 767 | 0.000 | 0.125 | 0.875 | nap |
| 3 | 1639 | 0.000 | 0.003 | 0.997 | nap |

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2` (v3 substrate library)
* Task: `t0081_bedb_v3_warmstart_nsga2` (cell 767 warm-start lineage)
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` (54-d parameter vectors for all 13 cells)
* Task: `t0084_t0081_cell_767_vm_trace_deepdive` (per-direction recording pattern + attribution
  metric)
* Task: `t0086_robustness_cluster_bio_comparison` (Genuine + Marginal classification + clustering
  + biological priors)
