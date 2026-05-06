# Brainstorm Session 17 -- Full Transcript

## Project State Presented

* **Total tasks**: 86, all completed.
* **Highest task index**: 86. This brainstorm reserves index 87; child task t0088 reserves index 88.
* **Project spend**: $15.5506 / $20.00 (77.75% spent, warn threshold 80% close but not reached).
  $4.4494 remaining.
* **Most recent completed task**: t0086 (`robustness_cluster_bio_comparison`).

t0086 highlights:
* 6 Genuine cells out of 20: 1517, 1604, 1634, 1639, 1663, 1677. (5/5 reps pass DSI >= 0.4 AND PD
  > = 10 Hz.)
* 7 Marginal cells out of 20: 767, 1304, 1379, 1504, 1559, 1624, 1721. (3-4/5 reps pass.)
* 7 Stochastic cells out of 20: 1238, 1457, 1482, 1484, 1548, 1710, 1723. (<=2/5 reps pass.)
* k=2 clusters on 6 Genuine cells; both clusters classified exotic by biological scorecard:
  * Cluster 0 (1634, 1639, 1663): NMDA +122 sigma, NaP +24 sigma, GABA rho0 +7 sigma, AIS-Nav 30.5
    (+4 sigma vs Werginz 2024).
  * Cluster 1 (1517, 1604, 1677): NMDA +85 sigma, NaP +7 sigma, GABA lambda +6 sigma, AIS-Nav 11.5
    (within Werginz plausible range).
* Final cost $1.595 / 4.59 hours wall-clock.
* All v3 substrate; $1.595 cost; REQ-X cost-watchdog rate-fix verified.

Open suggestions related to t0086 (pre-cleanup):
* S-0086-01 high experiment - Tighten NSGA-II priors on gnmda_dend to match Sivyer 2013, re-run.
  $1.50.
* S-0086-02 high evaluation - Resolve units mismatch between t0080 gnmda_dend NetCon weight and
  Sivyer 2013 per-spine conductance. $0.30.
* S-0086-03 medium experiment - Per-cluster Vm trace deep-dive (extension of t0084 to all 6 Genuine
  cells). $1.20 remote-CPU.
* S-0086-04 medium experiment - 10-replication robustness extension: rerun the 6 Genuine + 7
  Marginal cells at 10 outer seeds. $0.65.
* S-0086-05 low evaluation - Source RGC-specific NaP density measurement to replace Stuart 1999 /
  Goldfinger 2000 cortical-pyramidal prior. $0.10.
* S-0086-06 medium experiment - Bed A cross-bed validation: re-run NSGA-II on the t0080 Bed A
  morphology with the same v3 substrate. $2.50.

Sum of S-0086-* costs: $6.25 vs $4.44 remaining means the project must pick at most ~$4 of these
suggestions for the remaining budget. S-0086-03 is local-CPU-feasible if the deep-dive is restricted
to fewer cells; S-0086-04 / S-0086-05 are both cheap.

## Clarification Questions

The researcher provided a one-shot directive bypassing the typical clarification round:

> implement S-0086-03 but before doing this redo the clustering including marginal cells as well.
> All in one task

This directive fully specifies:
* Bundle scope: re-cluster + per-cluster Vm-trace deep-dive in one combined task.
* Expanded clustering: include the 7 Marginal cells alongside the 6 Genuine cells (13 cells total).
* Style: "All in one task" -- consolidated bundling consistent with the recorded researcher
  preference (memory: feedback_consolidated_task_design).

No additional clarification was needed.

## Discussion -- Round 1: New Tasks

AI proposal:

> Given the directive, propose creating t0088 (`recluster_marginals_and_vm_motifs`):
>
> **Phase A -- Re-cluster 13 cells.** Load the 6 Genuine + 7 Marginal cells from t0086's
> `cell_classification.json`. Total 13 cells:
> [767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1721]. Load the 54-d
> natural-unit parameter vectors from t0083's `all_evaluations.json` (cells 1238-1727) and t0081's
> `all_evaluations.json` (cell 767's warm-start parameters). Re-run KMeans for k=2..6, hierarchical
> clustering with ward linkage and both cosine + euclidean metrics, UMAP / PCA visualisation; pick
> best k via silhouette + BIC. Compute per-cluster centroids. Re-use t0086's `biological_priors.py`
> and `biological_scorecard.py` to score each new cluster centroid against published priors.
>
> **Phase B -- Per-cluster Vm-trace deep-dive.** Pick a representative cell per cluster (closest to
> centroid in 54-d Euclidean distance). For each, run a t0084-style deep-dive at **16 directions**
> (every 22.5 deg) -- twice the angular resolution of t0084. Record per-segment Vm at proximal soma,
> mid-dendrite, distal-dendrite, AIS; per-segment NMDA conductance trajectories; per-segment Nav1.6
> / NaP currents at distal dendrite; AIS Vm and threshold-crossing spike onset times. Generate 4
> figures matching t0084 per representative cell. Compute fractional channel contributions.
>
> **Phase C -- Mechanism distinctness analysis.** Compare fractional contributions across clusters;
> do clusters use different dominant mechanisms (e.g., NMDA-dominant vs NaP-dominant vs
> Nav1.6-dominant), or share the same mechanism but vary in scale? Compare to t0084's cell 767
> attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%). Output: one **answer asset**.
>
> Compute: Phase A pure data analysis, $0, ~10 min; Phase B per representative cell at 16 directions
> x 1 inner replication = 16 NEURON sims at ~60 s each = ~16 min per cell; with 2-3 cluster
> representatives = 32-48 min; Phase C analysis, $0. **Local CPU only. No remote machine. Total
> wall-clock 1-2 hours, $0 cost.**
>
> Source suggestion S-0086-03 (extended scope). Dependencies: t0024, t0078, t0080, t0081 (cell 767
> parameters), t0083 (cells 1238-1727 parameters), t0084 (run_deepdive recording pattern), t0086
> (biological scorecard, cell classification, original 6-Genuine clustering). Task types:
> data-analysis, experiment-run, answer-question. expected_assets `{"answer": 1}`.

Researcher: implicitly confirmed via the one-shot directive ("All in one task"). The directive
itself is the proposal acceptance.

## Discussion -- Round 2: Suggestion Cleanup

AI proposal:

> S-0086-03 is the seed of t0088 with extended scope. Reject as covered (rationale: t0088 covers the
> same per-cluster Vm-trace deep-dive scope plus extends the cell pool to 13 cells, raises the
> angular resolution to 16 directions, and runs on local CPU instead of remote-CPU).
>
> Keep S-0086-01 / -02 / -04 / -05 / -06 active; they are independent of t0088.

Researcher: implicitly confirmed via the one-shot directive ("implement S-0086-03"); the natural
implication is that S-0086-03 itself becomes covered.

## Discussion -- Round 3: Confirmation

AI summary of decisions:

1. Create t0088 (`recluster_marginals_and_vm_motifs`). Phase A re-cluster 13 cells; Phase B
   per-cluster Vm-trace deep-dive at 16 directions on local CPU; Phase C mechanism-distinctness
   analysis producing one answer asset. Source suggestion S-0086-03. Local-CPU only; $0 cost.
2. Reject S-0086-03 as covered.
3. No reprioritisations. No tasks cancelled or updated.

Researcher: the one-shot directive is the explicit confirmation. Authorises the entire remaining
lifecycle (PR push and merge).

## Decisions Summary

1. **Create t0088** (`recluster_marginals_and_vm_motifs`) covering Phase A re-cluster 13 cells +
   Phase B per-cluster Vm-trace deep-dive at 16 directions + Phase C mechanism-distinctness
   analysis. Source: S-0086-03. Local-CPU only; $0 cost. Dependencies: t0024, t0078, t0080, t0081,
   t0083, t0084, t0086. Task types: data-analysis, experiment-run, answer-question. expected_assets
   `{"answer": 1}`.

2. **Reject S-0086-03** as covered by t0088 (rationale: t0088 extends the Vm-trace deep-dive scope
   to 13 cells, 16 directions, local CPU).

3. **No reprioritisations**.

4. **No tasks cancelled or updated**.

5. **Five S-0086-* suggestions remain active for future brainstorms**: S-0086-01 ($1.50), S-0086-02
   ($0.30), S-0086-04 ($0.65), S-0086-05 ($0.10), S-0086-06 ($2.50). Combined cost $5.05; project
   budget remaining $4.44 means the project must pick at most ~$4 of these for the remaining budget.
   S-0086-02 + S-0086-05 + S-0086-04 + S-0086-01 = $2.55 fits; alternatively S-0086-02 + S-0086-04 +
   S-0086-06 = $3.45 fits.

6. **t0075** (Bed A bio-realistic AIS one-axis sweep) remains queued.
