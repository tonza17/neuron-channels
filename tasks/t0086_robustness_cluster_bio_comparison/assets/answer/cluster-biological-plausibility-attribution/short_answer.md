---
spec_version: "2"
answer_id: "cluster-biological-plausibility-attribution"
answered_by_task: "t0086_robustness_cluster_bio_comparison"
date_answered: "2026-05-06"
---
# Cluster Biological Plausibility Attribution

## Question

Which clusters of joint-pass cells in t0083's expanded population are biologically plausible vs novel/unphysical, and which dendritic-spike machinery do the plausible clusters represent?

## Answer

Of 20 re-evaluated cells 6 are Genuine (5/5 reps pass joint criterion), 7 Marginal (3-4/5), 7 Stochastic (<=2/5). The Genuine cells partition into 2 cluster(s) at k-means best_k. Cluster 0 (n=3): exotic; Cluster 1 (n=3): exotic. Cluster centroids were scored against eight published priors (Kole 2008, Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005, Stuart 1999, Goldfinger 2000, de Rosenroll 2026). See full_answer.md for per-cluster and per-prior breakdowns.

## Sources

* Task: `t0086_robustness_cluster_bio_comparison` (this task; 100-evaluation
  replication study, k-means/hierarchical/UMAP cluster analysis, biological
  scorecard).
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` (source of the 18-cell Pareto
  front and 14 of the 15 joint-pass cells).
* Task: `t0081_bedb_v3_warmstart_nsga2` (source of cell 767, the original
  joint-pass cell).
* Task: `t0084_t0081_cell_767_vm_trace_deepdive` (cell 767 mechanism
  attribution informing cluster-67 narrative).
