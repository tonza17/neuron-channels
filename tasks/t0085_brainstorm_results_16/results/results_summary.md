---
spec_version: "1"
task_id: "t0085_brainstorm_results_16"
date_completed: "2026-05-06"
status: "complete"
---
# Results Summary: Brainstorm Session 16

## Summary

Sixteenth strategic brainstorm, run on 2026-05-06 after t0083 (`bedb_v3_extend_nsga2_gen8plus`)
extended t0081's NSGA-II from gen 7 through gen 17 and **expanded the joint-pass cell population
from 1 to 15 cells** (1 inherited cell 767 + 14 new in gens 13-17), with hypervolume +118% (16.330
-> 35.576), and t0084 (`t0081_cell_767_vm_trace_deepdive`) produced the cell-767
mechanism-attribution answer asset at $0 cost. One consolidated follow-up task commissioned: t0086
(`robustness_cluster_bio_comparison`) bundles three open suggestions (S-0083-02 motif clustering,
S-0083-05 multi-seed robustness gate, multi-replicate aspect of S-0081-01) into three sequential
phases on top of t0083's 18-cell Pareto front -- (A) re-evaluate top 20 cells (15 joint-pass + 5
closest near-pass) at 24 directions x 30 seeds x 5 outer-seed replications and classify Genuine /
Marginal / Stochastic; (B) k-means + hierarchical clustering with k=2..6 on Genuine cells' 54-d
parameter vectors plus UMAP/t-SNE 2D visualisation; (C) score each cluster centroid against
published biological priors (Kole 2008, Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005,
Goldfinger 2000, Stuart 1999, de Rosenroll 2026) producing a per-cluster biological-plausibility
scorecard. Output: one answer asset per-cluster attribution + cluster characterisation tables + UMAP
plot + scorecard. Compute estimate $1.93-$2.57; **hard cost cap $3.50** (1.5x estimate); REQ-X (cost
watchdog rate fix) hardens against t0083-style watchdog rate-bug. Three suggestions rejected as
covered (S-0083-02, S-0083-05, S-0081-01). No reprioritisations; t0075 stays queued. Project budget
$20.00; $13.96 spent before t0086; **$6.04 remaining**; t0086's cap leaves $2.54 buffer for
subsequent S-0083-* follow-ups.

## Session Overview

Date: 2026-05-06. Triggered by t0083's expansion of the joint-pass population from 1 cell to 15
cells (the most decisive scale-up in project history) and t0084's confirmation that cell 767's DSI
improvement attributes cleanly to specific dendritic-spike machinery. Three previously open
suggestions naturally bundle into a single combined task per the recorded researcher preference for
one combined task bundling related suggestions + infra/protocol fixes (memory:
feedback_consolidated_task_design): S-0083-02 (motif clustering on Pareto cells), S-0083-05
(multi-seed smoke gate), and S-0081-01 (multi-replicate confirmation). The session opened with an
independent priority reassessment surfacing this bundling opportunity. The researcher confirmed the
proposed scope (defaults: 20 cells, 24 directions, 5 replications, ~$2-3 cost, $3.50 hard cap) via
an explicit "confirm" message, authorising the entire remaining lifecycle through PR merge. The
cost-watchdog rate-fix REQ-X is a project-wide protocol fix forced by t0083's $0.83 overrun ($5.83
actual vs $5.00 cap) due to the in-loop watchdog using a hard-coded $0.2382/hr rate when the actual
offer billed at $0.3209/hr (1.347x).

## Decisions

1. **Create t0086** (`robustness_cluster_bio_comparison`). Three sequential phases on top of t0083's
   18-cell Pareto front:

   * **Phase A (robustness validation)**: select 20 cells = all 15 joint-pass cells (cell 767 from
     t0081 + 14 from t0083 with DSI >= 0.4 AND PD >= 10) + 5 closest near-pass cells from t0083's
     Pareto front by Euclidean distance to (DSI 0.4, PD 10) joint corner among cells that do NOT
     satisfy joint-pass. Re-evaluate each at 24 directions x 30 seeds x 5 outer RNG seeds (controls
     AR(2) release noise + arrival jitter). Compute mean +/- SD of DSI and PD per cell across the 5
     replications. Classify: **Genuine** (5/5 replications joint-pass), **Marginal** (3-4/5),
     **Stochastic** (<=2/5).

   * **Phase B (cluster analysis on Genuine cells)**: k-means with k=2..6 (silhouette + BIC for k
     selection); hierarchical clustering with cosine and euclidean distance metrics for
     cross-validation; UMAP + t-SNE 2D visualisation; per-cluster centroids + within/between cluster
     variance.

   * **Phase C (biological comparison)**: per cluster centroid, score key parameters against
     published biological priors -- AIS Nav density vs Kole 2008 (0.25-0.5 S/cm^2) and Werginz 2024
     (1.3 S/cm^2 mouse alpha-RGC); AIS-to-soma Nav ratio vs Werginz 2024 (17.3x); dendritic NMDA
     conductance and Mg-block voff vs Sivyer 2013, Branco-Hausser 2010; distal Nav1.6 / NaP
     densities vs Oesch 2005, Goldfinger 2000, Stuart 1999; GABA/AMPA spatial distribution vs de
     Rosenroll 2026. Classify each cluster parameter as **plausible** (within +/-2 sigma of
     published mean), **stretched** (+/-2-5 sigma), or **exotic** (>5 sigma). Output: one **answer
     asset** at `assets/answer/cluster-biological-plausibility-attribution/` attributing each
     cluster to known biology or flagging as novel/unphysical, plus per-cluster characterisation
     tables, UMAP plot, biological-plausibility scorecard.

   **Pass criteria**: Primary -- at least one cluster of >=3 Genuine cells, all key biological
   parameters within +/-2 sigma of published priors. Secondary -- robustness classification itself
   useful regardless of cluster verdicts. Acceptable negative -- zero Genuine clusters (all
   joint-pass cells turn out stochastic) is a major project pivot but a clean negative result.

   **Compute**: 100 cell-evals @ ~720 sims (24 dirs x 30 seeds) each. Per-cell wall-clock ~162 s on
   Vast.ai 64-core EPYC 7B13 (4.5x t0083's ~36 s/cell at 8 dirs x 20 seeds = 160 sims). Total ~5-6
   hours optimiser time; with overhead 6-8 hours = **$1.93-$2.57**. **Hard cost cap $3.50** (1.5x of
   estimate to absorb variance).

   **REQ-X (cost watchdog rate fix)**: cost watchdog MUST source per-instance hourly rate from
   `machine_log.json` `selected_offer.price_per_hour`, not from a hard-coded constant. This
   project-wide protocol fix prevents a recurrence of t0083's 16% overrun. Document explicitly in
   the t0086 plan and verify in implementation review.

   **Vast.ai instance class**: same EPYC 7B13 64-core. Fallback: other 36+ core EPYC at <$0.40/hr if
   7B13 unavailable at <$0.35/hr.

   Source suggestions: **S-0083-02** (primary; also covers S-0083-05 and the multi-replicate aspect
   of S-0081-01). Dependencies: t0024, t0078, t0080, t0081, t0083, t0084.
   `expected_assets = {"answer": 1}`.

2. **Reject S-0083-02** -- t0086 Phase B is exactly this analysis (k-means + hierarchical clustering
   on Pareto cells in 54-d parameter space) applied to a stricter subset (Genuine cells only, after
   Phase A robustness filtering) with a richer technique stack (UMAP + t-SNE) and the additional
   biological-comparison Phase C overlaid on top.

3. **Reject S-0083-05** -- t0086 Phase A is exactly this multi-seed smoke gate, run at the larger
   30-seed x 5-outer-rep budget that cleanly separates Genuine / Marginal / Stochastic. Genuine =
   5/5 replications joint-pass; Marginal = 3-4/5; Stochastic = <=2/5.

4. **Reject S-0081-01** -- the multi-replicate confirmation aspect is covered by t0086 Phase A (cell
   767 is included in the 20-cell set; the Genuine/Marginal/Stochastic classification directly
   answers whether 767 reproduces under different RNG seeds). Remaining S-0081-01 aspects (different
   morphologies, conductance noise profiles) deferred to optional follow-ups if Phase A flags
   reproducibility issues.

## Metrics

| Metric | Value |
| --- | --- |
| New tasks created | 1 (t0086 robustness + cluster + bio-comparison) |
| Tasks cancelled | 0 |
| Tasks updated (other than cancellations) | 0 |
| Suggestions rejected | 3 (S-0083-02, S-0083-05, S-0081-01) |
| Suggestions reprioritised | 0 |
| Corrections written | 3 |
| New suggestions created | 0 |
| Answer assets created in this brainstorm | 0 |
| Session duration | ~50 minutes interactive |
| Session cost | $0.00 |
| Estimated cost of commissioned task | $1.93-$2.57 (max $3.50) |

## Verification

* `verify_task_file.py t0085_brainstorm_results_16` -- target 0 errors.
* `verify_corrections.py t0085_brainstorm_results_16` -- target 0 errors across 3 correction files.
* `verify_suggestions.py t0085_brainstorm_results_16` -- target 0 errors (empty array).
* `verify_logs.py t0085_brainstorm_results_16` -- target 0 errors; LG-W005 / LG-W007 / LG-W008
  acceptable per skill guidance and step-4 capture.
* `verify_task_file.py t0086_robustness_cluster_bio_comparison` -- target 0 errors.
* `verify_pr_premerge.py t0085_brainstorm_results_16 --pr-number <N>` -- target 0 errors.

## Next Steps

1. **t0086 execution** is the immediate follow-up: it bundles three previously open suggestions into
   a single end-to-end pipeline (robustness -> cluster -> biological comparison) and produces one
   answer asset with the per-cluster attribution. Expected wall-clock ~6-8 hours on Vast.ai 64-core
   EPYC 7B13 plus ~1-2 hours of local-CPU clustering and biological-comparison analysis. Hard cost
   cap $3.50 with REQ-X cost-watchdog rate-fix.

2. **Decision point after t0086 completes**:
   * If at least one Genuine cluster maps to known biology (Kole/Werginz/Sivyer/Oesch within +/-2
     sigma), the v3 substrate is established as biologically grounded and the next wave can target
     either (a) cross-bed validation on Bed A (~~$3) to test cluster generalisation, or (b)
     cross-morphology validation (~~$5-10) to test whether the clusters are robust to dendritic
     geometry changes.
   * If all Genuine clusters are exotic (>5 sigma from priors), the project pivots to a two-track
     strategy: (a) ablation experiments to identify which exotic parameter is load-bearing for the
     joint pass, and (b) targeted searches in the biologically-plausible neighbourhoods of each
     exotic cluster.
   * If no cell is Genuine (all joint-pass cells turn out stochastic), the project pivots to a major
     rethinking of the substrate and the multi-replicate strategy.

3. **t0075** (Bed A bio-realistic AIS one-axis sweep) remains queued for later opportunistic pickup.
   Different substrate (Bed A) from t0086 (Bed B v3); complementary one-axis sensitivity analysis.

4. **Highest-leverage unaddressed experiments deferred to next brainstorm**: S-0067-01 (NaP density
   crossing DSI = 0; cheap ~25 min sweep), S-0074-01 (SK polar-curve clipping check; pure data
   analysis ~30 min), S-0074-02 (NaR ND-floor verification; ~15 min), S-0081-05 (Bed A cross-bed
   validation, ~$3). All four are inexpensive analyses and / or cheap cross-substrate validations to
   consider after t0086 results land.
