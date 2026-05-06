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

The 13-cell re-cluster produces **4 clusters**, and the per-cluster Vm-trace deep-dive at 16
directions yields the verdict **shared_mechanism_different_scale**. Unique dominant mechanisms
across clusters: **nap**. Per-cluster fractional channel attributions are tabulated below; the
verdict reflects whether different clusters use different dominant ion-current mechanisms in their
PD-minus-ND integrated dendritic current.

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | 0.988 | nap |
| 1 | 1634 | 0.000 | 0.126 | 0.874 | nap |
| 2 | 767 | 0.000 | 0.125 | 0.875 | nap |
| 3 | 1639 | 0.000 | 0.003 | 0.997 | nap |

All clusters share the same dominant mechanism in PD-minus-ND attribution; they differ in parameter
scale (parameter-vector position in 54-d space) but not in which channel drives the PD response.
verdict = shared_mechanism_different_scale.

Compare to t0084's cell 767 attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%): the per-cluster
re-evaluation at 16 directions reveals whether the cell-767 NaP-dominant signature generalises to
the broader 13-cell pool's clusters.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2` (v3 substrate library)
* Task: `t0081_bedb_v3_warmstart_nsga2` (cell 767 warm-start lineage)
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` (54-d parameter vectors for all 13 cells)
* Task: `t0084_t0081_cell_767_vm_trace_deepdive` (per-direction recording pattern + attribution
  metric)
* Task: `t0086_robustness_cluster_bio_comparison` (Genuine + Marginal classification + clustering
  + biological priors)
