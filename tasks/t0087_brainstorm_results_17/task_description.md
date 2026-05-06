# Brainstorm Session 17: Re-cluster t0086 Genuine + Marginal cells and per-cluster Vm-trace deep-dive

Seventeenth brainstorming session. Run on 2026-05-06 after t0086
(`robustness_cluster_bio_comparison`) classified the 20-cell test set as 6 Genuine + 7 Marginal + 7
Stochastic, k=2 clusters on the 6 Genuine cells, both clusters exotic (NMDA per-synapse +85-122
sigma above Sivyer 2013, NaP +7-24 sigma above Stuart 1999), AIS-Nav ratios 11.5-30.5 (one cluster
plausible, the other +4 sigma above Werginz 2024). Project spend reached **$15.56 / $20.00**;
**$4.44 remaining**.

The session is one-shot per the researcher's verbatim directive: extend S-0086-03's per-cluster
Vm-trace deep-dive to a wider cell pool by re-doing clustering with the 7 Marginal cells included
alongside the 6 Genuine cells (13 cells total instead of 6), so the new clustering rests on a
larger, mechanistically heterogeneous pool, and the per-cluster Vm-trace deep-dive is performed on
representatives from the new clusters at higher angular resolution (16 directions instead of t0084's
8). All in one task.

## Decisions

* **Create t0088** -- `recluster_marginals_and_vm_motifs`. Three sequential phases:

  * **Phase A (re-cluster 13 cells)**: load the 6 Genuine + 7 Marginal cells from t0086's
    `cell_classification.json`. Total 13 cells:
    `[767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1721]`. Load their 54-d
    natural-unit parameter vectors from t0083's `all_evaluations.json` (cells 1238-1727) and t0081's
    `all_evaluations.json` (cell 767's warm-start parameters). Re-run KMeans k=2..6, hierarchical
    (ward + cosine + euclidean), UMAP/PCA visualisation; pick best k via silhouette + BIC. Compute
    per-cluster centroids in 54-d natural-unit space. Re-use t0086's `biological_priors.py` and
    `biological_scorecard.py` to score each new centroid against published priors (Kole 2008,
    Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005, Goldfinger 2000, Stuart 1999, de
    Rosenroll 2026).

  * **Phase B (per-cluster Vm-trace deep-dive)**: pick a representative cell per cluster (closest to
    centroid in 54-d Euclidean distance among cells assigned to that cluster). Run a t0084-style
    deep-dive at higher angular resolution: **16 directions** (every 22.5 deg). Record per-segment
    Vm at proximal soma, mid-dendrite, distal-dendrite, AIS; per-segment NMDA conductance
    trajectories; per-segment Nav1.6 (`nav16t80._ref_i`) and NaP (`napt80._ref_i`) currents at
    distal dendrite; AIS Vm and threshold-crossing spike onset times. Per representative, generate 4
    figures matching t0084: per-direction Vm traces (3-row x 16-column grid: proximal soma / mid
    dendrite / distal dendrite); NMDA conductance trajectories at distal dendrite; Nav1.6 / NaP
    current decomposition; AIS spike onset histogram. Compute fractional channel contributions per
    cluster representative.

  * **Phase C (mechanism distinctness analysis)**: compare fractional contributions across clusters;
    do different clusters use different dominant mechanisms (e.g., one NMDA-dominant, one
    NaP-dominant, one Nav1.6-dominant), or do they all share the same mechanism but vary in scale?
    Compare to t0084's cell 767 attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%). Per-cluster
    narrative: which biophysical strategy does this cluster represent?

  Output: one **answer asset** at `assets/answer/are-cluster-motifs-mechanistically-distinct/` per
  the answer-asset specification, with quantitative attribution per cluster.

  **Pass criteria**: Primary -- produce a clear mechanism-distinctness verdict (clusters are
  mechanistically distinct vs share the same mechanism). Secondary -- per-cluster representative
  Vm-trace deep-dive figures published. Acceptable negative -- clusters are NOT mechanistically
  distinct (all use the same NMDA-dominant strategy, differing only in parameter scale) is itself a
  useful finding aligning with t0086's exotic-NMDA verdict.

  **Compute**: Phase A pure data analysis ($0, ~10 min); Phase B per representative cell at 16
  directions x 1 inner replication = 16 NEURON sims at ~60 s each = ~16 min per cell; with 2-3
  cluster representatives = 32-48 min; Phase C analysis ($0). **Local CPU only. No remote machine.
  Total wall-clock ~1-2 hours, $0 cost.**

  Source suggestion: **S-0086-03** (extension scope). Dependencies: t0024, t0078, t0080, t0081,
  t0083, t0084, t0086. `expected_assets = {"answer": 1}`. Task types:
  `["data-analysis", "experiment-run", "answer-question"]`.

## Suggestion Cleanup

* **Reject S-0086-03** -- t0088 covers the per-cluster Vm-trace deep-dive with extended scope (13
  cells re-clustered, 16 directions instead of t0084's 8, mechanism-distinctness narrative as the
  answer asset). The original S-0086-03 scope (deep-dive on 6 Genuine cells only at 24 directions
  remote-CPU) is subsumed by t0088's extended scope; t0088 picks 16 directions for local-CPU
  feasibility.

## Reprioritisations

None.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued.

## Assets Produced

No assets in this brainstorm task. The new task t0088 will produce one answer asset attributing each
re-clustered cluster to a dominant biophysical mechanism (or, in the negative case, confirming a
shared mechanism with parameter-scale variation).

## Budget Context

Project budget $20.00; **$15.56 spent** before t0088; **$4.44 remaining**. t0088 is local-CPU only
and estimated **$0.00**, leaving the **$4.44 buffer intact** for subsequent S-0086-* follow-ups
(notably S-0086-01 NSGA-II re-run with tightened NMDA bounds at $1.50, S-0086-02 NMDA units
calibration at $0.30, S-0086-04 10-rep robustness extension at $0.65, S-0086-06 Bed A cross-bed
validation at $2.50).
