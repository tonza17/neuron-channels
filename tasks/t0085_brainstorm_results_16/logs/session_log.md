# Brainstorm Session 16 -- Full Transcript

## Project State Presented

Headline: t0083 (`bedb_v3_extend_nsga2_gen8plus`) extended t0081's NSGA-II from gen 7 through gen 17
and **expanded the joint-pass cell population from 1 to 15 cells** (1 inherited cell 767 + 14 new in
gens 13-17), with 3 of those 15 lying on the final 18-cell Pareto front (highest-DSI cell 1304 at
DSI 0.7652 / PD 13.96 Hz). Hypervolume grew +118% from gen 7 (16.330) to gen 17 (35.576) over 960
additional evaluations. t0083's actual cost was $5.83 against a $5.00 cap (16% over) due to the
in-loop cost watchdog using a hard-coded $0.2382/hr rate when the actual instance offer billed at
$0.3209/hr (1.347x). t0084 (`t0081_cell_767_vm_trace_deepdive`) ran in parallel at $0 and produced
the cell-767 Vm-trace mechanism-attribution answer asset.

Recent task results presented:

* t0083 (1728 total evaluations -- 768 inherited from t0081 + 960 new; 18-cell final Pareto front;
  15 joint-pass cells; HV 16.330 -> 35.576; $5.828 actual vs $5.00 cap): cell 1304 DSI 0.7652 / PD
  13.96 Hz; cell 1559 DSI 0.7061 / PD 39.18 Hz; cell 1677 DSI 0.6570 / PD 40.71 Hz on the final
  Pareto front. Watchdog rate-bug noted in `costs.json` `note`.
* t0084 ($0 local-CPU): cell-767 mechanism-attribution answer asset produced.

Project state inventory:

* 84 tasks total; all completed.
* 15 prior brainstorm sessions; this is session 16.
* Substrates: Bed A (ModelDB 189347 / Poleg-Polsky 2016 lineage with gabaMOD scalar inhibition); Bed
  B v3 (de Rosenroll 2026 + AIS hard floors + dendritic-spike machinery, 54-d, established by
  t0081/t0083 as the project's working substrate).
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued.

Budget pre-session:

* Spent: $13.96 / $20.00 (69.78%). Below 80% warn threshold.
* Remaining: $6.04 before stop threshold.
* Open suggestions of interest:
  * S-0083-02 (high; motif clustering on 18 t0083 Pareto cells)
  * S-0083-05 (high; multi-seed smoke gate / robustness check across joint-pass cells)
  * S-0081-01 (high; multi-replicate confirmation, ~$5-10)
  * S-0081-05 (medium; Bed A cross-bed validation, ~$3)

Independent priority reassessment of the highest-leverage suggestions:

| Suggestion | Stored | Reassessed | Reason |
| --- | --- | --- | --- |
| S-0083-02 (motif clustering) | high | BUNDLE INTO t0086 | Needs robustness filtering first; otherwise stochastic cells contaminate cluster signal. |
| S-0083-05 (multi-seed gate) | high | BUNDLE INTO t0086 | Natural Phase A; gates Phase B. |
| S-0081-01 (multi-replicate) | high | BUNDLE INTO t0086 | Multi-replicate aspect satisfied by Phase A 5-replication design. |

The bundle is consistent with the recorded researcher preference for one combined task bundling
related suggestions + infra/protocol fixes (memory: feedback_consolidated_task_design). The
infra/protocol fix is the cost-watchdog rate-fix REQ-X forced by t0083's $0.83 overrun.

## Clarification Questions

AI: Proposed scope for t0086:
* 20 cells (15 joint-pass + 5 closest near-pass from t0083 Pareto front by Euclidean distance to
  (DSI 0.4, PD 10) joint corner)
* 24 directions x 30 seeds x 5 outer RNG-seed replications per cell
* Three sequential phases: Phase A robustness validation; Phase B clustering on Genuine cells
  (k-means + hierarchical with cosine + euclidean + UMAP/t-SNE); Phase C biological scorecard vs
  Kole 2008 / Werginz 2024 / Sivyer 2013 / Branco-Hausser 2010 / Oesch 2005 / Goldfinger 2000 /
  Stuart 1999 / de Rosenroll 2026
* Estimated $1.93-$2.57; hard cap $3.50 (1.5x)
* REQ-X (cost watchdog rate fix) forced by t0083 overrun

Researcher: "confirm"

## Discussion -- Round 1: New Tasks

AI proposed t0086 (`robustness_cluster_bio_comparison`) bundling S-0083-02 / S-0083-05 / S-0081-01
into three sequential phases:

**Phase A (robustness validation)**: select 20 cells = 15 joint-pass cells (cell 767 from t0081
+ 14 from t0083 with DSI >= 0.4 AND PD >= 10) + 5 closest near-pass cells from t0083's Pareto front
  by Euclidean distance to (DSI 0.4, PD 10) joint corner among non-joint-pass cells. Re-evaluate
  each at 24 directions x 30 seeds x 5 outer RNG seeds (controls AR(2) release noise
+ arrival jitter). Compute mean +/- SD of DSI / PD per cell. Classify: Genuine (5/5 pass); Marginal
  (3-4/5); Stochastic (<=2/5).

**Phase B (cluster analysis on Genuine cells)**: k-means with k=2..6 (silhouette + BIC for k
selection); hierarchical clustering with cosine and euclidean distance metrics; UMAP + t-SNE 2D
visualisation; per-cluster centroids + within/between cluster variance.

**Phase C (biological comparison)**: per cluster centroid, score key parameters against published
priors:
* AIS Nav density vs Kole 2008 (0.25-0.5 S/cm^2) and Werginz 2024 (1.3 S/cm^2 mouse alpha-RGC)
* AIS-to-soma Nav ratio vs Werginz 2024 (17.3x)
* Dendritic NMDA conductance and Mg-block voff vs Sivyer 2013, Branco-Hausser 2010
* Distal Nav1.6 / NaP densities vs Oesch 2005, Goldfinger 2000, Stuart 1999
* GABA/AMPA spatial distribution vs de Rosenroll 2026

Classification: plausible (within +/-2 sigma of published mean); stretched (+/-2-5 sigma); exotic
(>5 sigma).

Output: one **answer asset** at `assets/answer/cluster-biological-plausibility-attribution/`
attributing each cluster to known biology or flagging as novel/unphysical, plus per-cluster
characterisation tables, UMAP plot, biological-plausibility scorecard.

Pass criteria:
* Primary: at least one cluster of >=3 Genuine cells, all key biological parameters within +/-2
  sigma of published priors.
* Secondary: robustness classification itself useful regardless of cluster verdicts.
* Acceptable negative: zero Genuine clusters (all joint-pass cells turn out stochastic).

Compute estimate: 100 cell-evals @ ~720 sims (24 dirs x 30 seeds) each. Per-cell wall-clock ~162 s
on Vast.ai 64-core EPYC 7B13 (4.5x t0083's ~36 s/cell at 8 dirs x 20 seeds = 160 sims). Total ~5-6
hours optimiser time; with overhead 6-8 hours = $1.93-$2.57. Hard cost cap $3.50 (1.5x of estimate
to absorb variance).

REQ-X (cost watchdog rate fix): cost watchdog MUST source per-instance hourly rate from
`machine_log.json` `selected_offer.price_per_hour`, not from a hard-coded constant.

Vast.ai instance class: same EPYC 7B13 64-core. Fallback: other 36+ core EPYC at <$0.40/hr if 7B13
unavailable at <$0.35/hr.

Source suggestions: S-0083-02 (primary; also covers S-0083-05 and the multi-replicate aspect of
S-0081-01).

Dependencies: t0024, t0078, t0080, t0081, t0083, t0084.

Researcher: "confirm" (single combined task; 20 cells; 24 directions; 5 replications; ~$2-3
estimated; $3.50 hard cap; REQ-X cost-watchdog rate-fix).

## Discussion -- Round 2: Suggestion Cleanup

AI proposed three rejections:

* **Reject S-0083-02** -- t0086 Phase B is exactly this analysis (k-means + hierarchical clustering
  on Pareto cells in 54-d parameter space) applied to a stricter subset (Genuine cells only, after
  Phase A robustness filtering) with a richer technique stack (UMAP + t-SNE) and the additional
  biological-comparison Phase C overlaid on top.

* **Reject S-0083-05** -- t0086 Phase A is exactly this multi-seed smoke gate, run at the larger
  30-seed x 5-outer-rep budget that cleanly separates Genuine / Marginal / Stochastic.

* **Reject S-0081-01** -- the multi-replicate confirmation aspect is covered by t0086 Phase A (cell
  767 is included in the 20-cell set; the Genuine/Marginal/Stochastic classification directly
  answers whether 767 reproduces under different RNG seeds). Remaining S-0081-01 aspects (different
  morphologies, conductance noise profiles) deferred to optional follow-ups if Phase A flags
  reproducibility issues.

Researcher: confirmed all three (block).

## Discussion -- Round 3: Confirmation

AI summarised all decisions:
* New tasks: t0086 (`robustness_cluster_bio_comparison`); $3.50 hard cap; REQ-X cost-watchdog
  rate-fix
* Suggestions rejected: S-0083-02, S-0083-05, S-0081-01
* Suggestions reprioritised: 0
* Tasks cancelled or updated: 0
* Brainstorm task: t0085_brainstorm_results_16

Researcher: "confirm"

## Decisions Summary

1. Create t0086 (`robustness_cluster_bio_comparison`) with three sequential phases (robustness
   validation, cluster analysis, biological comparison), 20 cells x 24 directions x 30 seeds x 5
   outer RNG-seed replications, $3.50 hard cap, REQ-X cost-watchdog rate-fix sourced from
   `machine_log.json`.

2. Reject S-0083-02 (covered by t0086 Phase B).

3. Reject S-0083-05 (covered by t0086 Phase A).

4. Reject S-0081-01 (multi-replicate aspect covered by t0086 Phase A).
