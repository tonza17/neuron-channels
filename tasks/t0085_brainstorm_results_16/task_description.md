# Brainstorm Session 16: Robustness, Cluster Analysis, and Biological Plausibility of t0083 Joint-Pass Cells

Sixteenth brainstorming session. Run on 2026-05-06 after t0083 (`bedb_v3_extend_nsga2_gen8plus`)
extended t0081's NSGA-II from gen 7 through gen 17 and **expanded the joint-pass population from 1
to 15 cells** (1 inherited cell 767 + 14 new cells produced in gens 13-17), with 3 of those 15 lying
on the final 18-cell Pareto front (highest-DSI cell 1304 at DSI 0.7652 / PD 13.96 Hz). Hypervolume
grew +118% from gen 7 (16.330) to gen 17 (35.576) over 960 additional evaluations. t0083's actual
cost was $5.83 against a $5.00 cap (16% over) due to a watchdog rate-bug: the in-loop watchdog used
the hard-coded $0.2382/hr rate inherited from t0080/t0081, but the actual instance offer billed at
$0.3209/hr (1.347x). t0084 (`t0081_cell_767_vm_trace_deepdive`) ran in parallel at $0 and produced
the cell-767 mechanism-attribution answer asset. Total project spend now **$13.96 / $20.00** with
**$6.04 remaining**.

## Decisions

* **Create t0086** -- `robustness_cluster_bio_comparison`. Bundle three previously open suggestions
  (S-0083-02 motif clustering, S-0083-05 multi-seed smoke gate / robustness check, and the
  multi-replicate confirmation aspect of S-0081-01) into a single combined task that runs three
  sequential phases on top of t0083's 18-cell Pareto front: **Phase A (robustness validation)**
  re-evaluate the top 20 cells (15 joint-pass cells + 5 closest near-pass cells from t0083's Pareto
  front by Euclidean distance to the (DSI 0.4, PD 10) joint corner) at 24 directions x 30 seeds x 5
  outer RNG-seed replications and classify each cell as Genuine (5/5 pass), Marginal (3-4/5), or
  Stochastic (<=2/5); **Phase B (cluster analysis)** k-means + hierarchical clustering with k=2..6
  selected by silhouette + BIC on the 54-d parameter vectors of Genuine cells, plus UMAP/t-SNE 2D
  visualisation; **Phase C (biological comparison)** score each cluster centroid against published
  priors (Kole 2008 AIS Nav, Werginz 2024 mouse alpha-RGC AIS-to-soma Nav ratio, Sivyer 2013 +
  Branco-Hausser 2010 dendritic NMDA, Oesch 2005 + Goldfinger 2000 + Stuart 1999 distal Nav1.6/NaP,
  de Rosenroll 2026 GABA/AMPA spatial distribution) producing a per-cluster biological-plausibility
  scorecard (within +/-2 sigma = plausible; +/-2-5 sigma = stretched; >5 sigma = exotic). Output:
  one **answer asset** per-cluster attribution + cluster characterisation tables + UMAP plot +
  biological-plausibility scorecard. Compute estimate: 100 cell-evals @ ~720 sims each = ~5-6 hours
  optimiser time; with overhead ~6-8 hours wall-clock on Vast.ai 64-core EPYC 7B13 =
  **$1.93-$2.57**; **hard cost cap $3.50** (1.5x estimate). **Hard requirement REQ-X (cost watchdog
  rate fix)**: cost watchdog MUST use actual per-instance hourly rate from `machine_log.json`
  `selected_offer.price_per_hour`, not a hard-coded constant. Source suggestions: **S-0083-02**
  (primary); also covers S-0083-05 and the multi-replicate aspect of S-0081-01. Dependencies: t0024,
  t0078, t0080, t0081, t0083, t0084.

## Suggestion Cleanup

* **Reject three suggestions** as covered by t0086 (analogous to session 15's S-0080-01/02/03
  cleanup):

  * **S-0083-02** (motif clustering on the 18 t0083 Pareto cells) -- t0086 Phase B is exactly this
    analysis, applied to a stricter subset (Genuine cells only, after Phase A robustness filtering),
    with a richer technique stack (k-means + hierarchical + UMAP) and the additional
    biological-comparison Phase C overlaid on top.

  * **S-0083-05** (multi-seed smoke gate / robustness check across t0083 joint-pass cells) -- t0086
    Phase A is exactly this gate, run at the larger 30-seed x 5-outer-rep budget that cleanly
    separates Genuine / Marginal / Stochastic.

  * **S-0081-01** (multi-replicate confirmation of cell 767 + neighbour cells) -- the
    multi-replicate confirmation aspect is covered by t0086 Phase A's 5-replication design. Cell 767
    is included in the t0086 cell set; the Genuine/Marginal/Stochastic classification directly
    answers whether 767 reproduces under different RNG seeds. The remaining S-0081-01 aspects
    (different morphologies, different conductance noise profiles) are deferred to optional
    follow-up tasks if Phase A flags reproducibility issues.

## Reprioritisations

None.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued.

## Assets Produced

No assets in this brainstorm task. The new task t0086 will produce: one answer asset attributing
each Genuine cluster to known biology (Kole/Werginz/Sivyer/Oesch priors) or flagging clusters as
novel/unphysical, plus cluster characterisation tables (under `results/`), UMAP/t-SNE plots,
per-cluster centroid + variance tables, per-cluster biological-plausibility scorecard, and the
robustness-classification table over all 20 cells.

## Budget Context

Project budget $20.00; $13.96 spent before t0086; **$6.04 remaining**. t0086's $3.50 hard cap leaves
$2.54 buffer for any subsequent S-0083-* follow-ups (e.g., morphology-variation replicates,
conductance-noise replicates, cross-bed validation). The cost-watchdog rate-fix REQ in t0086's plan
prevents a t0083-style 16% overrun.
