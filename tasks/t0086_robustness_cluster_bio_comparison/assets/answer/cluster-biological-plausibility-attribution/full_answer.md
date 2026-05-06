---
spec_version: "2"
answer_id: "cluster-biological-plausibility-attribution"
answered_by_task: "t0086_robustness_cluster_bio_comparison"
date_answered: "2026-05-06"
confidence: "medium"
---
# Cluster Biological Plausibility Attribution -- Full Answer

## Question

Which clusters of joint-pass cells in t0083's expanded population are biologically plausible vs novel/unphysical, and which dendritic-spike machinery do the plausible clusters represent?

## Short Answer

Of 20 re-evaluated cells 6 are Genuine (5/5 reps pass joint criterion), 7 Marginal (3-4/5), 7 Stochastic (<=2/5). The Genuine cells partition into 2 cluster(s) at k-means best_k. Cluster 0 (n=3): exotic; Cluster 1 (n=3): exotic. Cluster centroids were scored against eight published priors (Kole 2008, Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005, Stuart 1999, Goldfinger 2000, de Rosenroll 2026). See full_answer.md for per-cluster and per-prior breakdowns.

## Research Process

The investigation proceeded in three phases on top of t0083's 18-cell Pareto
front. Phase A re-evaluated 20 cells (15 joint-pass: cell 767 + 14 t0083
joint-pass cells; 5 closest near-pass cells from the t0083 Pareto front
ranked by Euclidean distance to the (DSI=0.4, PD=10 Hz) joint corner) at 24
directions x 30 inner seeds x 5 outer-seed replications using the t0080
`evaluate_parameter_vector` entry point. Each replication monkey-patches the
t0080 module-level `SEED_BASE` constant to one of 5 deterministic seeds drawn
from `np.random.SeedSequence(42).spawn(5)` so that DSI and PD variance across
replications reflect inter-RNG variability rather than parameter changes
(REQ-3, REQ-4, REQ-16). Each cell was classified Genuine (5/5 reps pass),
Marginal (3-4/5), or Stochastic (<=2/5) (REQ-5).

Phase B applied k-means clustering with k=2..6 to the 54-d parameter vectors
of the Genuine cells in min-max normalised space, selecting best_k by
silhouette score. Hierarchical clustering with cosine and euclidean metrics
provided cross-validation; 50-sample bootstrap stability ARI quantified
robustness of the k-means partition (REQ-6, REQ-7, REQ-9, REQ-10). UMAP
(falling back to PCA if umap-learn unavailable) produced a 2-D embedding for
visualisation (REQ-8).

Phase C scored each cluster centroid in unnormalised parameter space against
eight published biological priors (Kole 2008, Werginz 2024, Sivyer 2013,
Branco-Hausser 2010, Oesch 2005, Stuart 1999, Goldfinger 2000, de Rosenroll
2026; REQ-11). Per (cluster, prior) pair, deviation = (centroid - mean)/sigma
with verdict plausible (|deviation| <= 2), stretched (2-5), or exotic (> 5).
Cluster aggregate verdict = worst-case (REQ-12).

## Evidence from Papers

The biological priors database (`code/biological_priors.py`) hard-codes published
measurements with paper_id references so the audit trail back to the corpus
is explicit. Kole 2008 (`10.1038_nn.2153`) and Werginz 2024 supply the AIS
Nav density priors; Oesch 2005 supplies distal Nav1.6; Stuart 1999 and
Goldfinger 2000 supply distal NaP; Sivyer 2013 supplies dendritic NMDA;
Branco-Hausser 2010 supplies the NMDA Mg-block voff; de Rosenroll 2026
supplies the GABA spatial gradient.

## Evidence from Internet Sources

No new internet research was conducted in this task; published values were
sourced from the existing paper corpus inherited from t0024, t0078, and
t0080.

## Evidence from Code or Experiments

The 100-cell-evaluation replication run (Phase A) generated
`results/data/replication_results.json` (one record per cell-eval pair),
classified at `results/data/cell_classification.json`. Phase B clustering
results live in `results/data/clustering_results.json` and centroids in
`results/data/cluster_centroids.json`. Phase C scorecard lives in
`results/data/biological_scorecard.json` with the heatmap at
`results/images/biological_plausibility_heatmap.png`. The cost watchdog
(REQ-X, `code/cost_watchdog.py`) read the actual hourly rate
(\$0.3474/hr) from `logs/steps/008_setup-machines/machine_log.json`
`selected_offer.price_per_hour` -- this fixes the t0083 \$0.83 budget overrun
caused by a hard-coded \$0.2382/hr default.

## Synthesis

Robustness summary: 6 Genuine, 7 Marginal, 7
Stochastic of 20 re-evaluated cells. Cluster summary at best_k:

### Cluster 0 -- exotic

Members (3): [1634, 1639, 1663].

| Prior | Citation | Centroid | Mean | Sigma | Dev. | Verdict |
|-------|----------|----------|------|-------|------|---------|
| `nav16_ais_gbar_kole2008` | Kole 2008 (Nat Neurosci) | 0.4672 | 0.375 | 0.125 | +0.74 | plausible |
| `nav16_ais_gbar_werginz2024` | Werginz 2024 (RGC physio update) | 0.4672 | 1.3 | 0.3 | -2.78 | stretched |
| `nav16_dend_distal_oesch2005` | Oesch 2005 (RGC dendritic spike) | 0.03417 | 0.05 | 0.02 | -0.79 | plausible |
| `nap_dend_distal_stuart1999` | Stuart 1999 / Goldfinger 2000 | 0.005277 | 0.0005 | 0.0002 | +23.89 | exotic |
| `gnmda_dend_sivyer2013` | Sivyer 2013 | 0.006216 | 0.0001 | 5e-05 | +122.32 | exotic |
| `voff_nmda_branco2010` | Branco & Hausser 2010 | 6.115 | 0 | 5 | +1.22 | plausible |
| `rho0_gaba_de_rosenroll_2026` | de Rosenroll 2026 | 4.64 | 1 | 0.5 | +7.28 | exotic |
| `lambda_gaba_um_de_rosenroll_2026` | de Rosenroll 2026 | 141.5 | 80 | 30 | +2.05 | stretched |
| `ais_to_soma_nav_ratio_werginz2024` | Werginz 2024 | 30.53 | 17.3 | 3 | +4.41 | stretched |

### Cluster 1 -- exotic

Members (3): [1517, 1604, 1677].

| Prior | Citation | Centroid | Mean | Sigma | Dev. | Verdict |
|-------|----------|----------|------|-------|------|---------|
| `nav16_ais_gbar_kole2008` | Kole 2008 (Nat Neurosci) | 0.2551 | 0.375 | 0.125 | -0.96 | plausible |
| `nav16_ais_gbar_werginz2024` | Werginz 2024 (RGC physio update) | 0.2551 | 1.3 | 0.3 | -3.48 | stretched |
| `nav16_dend_distal_oesch2005` | Oesch 2005 (RGC dendritic spike) | 0.022 | 0.05 | 0.02 | -1.40 | plausible |
| `nap_dend_distal_stuart1999` | Stuart 1999 / Goldfinger 2000 | 0.001988 | 0.0005 | 0.0002 | +7.44 | exotic |
| `gnmda_dend_sivyer2013` | Sivyer 2013 | 0.004375 | 0.0001 | 5e-05 | +85.51 | exotic |
| `voff_nmda_branco2010` | Branco & Hausser 2010 | 4.261 | 0 | 5 | +0.85 | plausible |
| `rho0_gaba_de_rosenroll_2026` | de Rosenroll 2026 | 3.484 | 1 | 0.5 | +4.97 | stretched |
| `lambda_gaba_um_de_rosenroll_2026` | de Rosenroll 2026 | 272.8 | 80 | 30 | +6.43 | exotic |
| `ais_to_soma_nav_ratio_werginz2024` | Werginz 2024 | 11.53 | 17.3 | 3 | -1.92 | plausible |


## Limitations

* Only 5 outer-seed replications per cell. A 10-replication study would
  distinguish 10/10 from 8-9/10 from <=7/10 with finer granularity but
  would double the wall-clock and \$ cost.
* Bootstrap subsample size = 80 percent of Genuine cells. With small N this
  produces wide ARI confidence intervals.
* Biological sigma values are conservative best-effort estimates where the
  source paper does not report formal uncertainty. Stretched / exotic
  verdicts may shift if a future task tightens the priors.

## Sources

* Task: `t0024_port_de_rosenroll_2026_dsgc` (de Rosenroll 2026 substrate).
* Task: `t0078_bedb_mobo_v2_ais_tiered_ahp` (AIS-tiered AHP recovery).
* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2` (v3 substrate; 54-d
  parameter space; AIS-to-soma constraint; cost-watchdog pattern).
* Task: `t0081_bedb_v3_warmstart_nsga2` (8-gen warmstart; cell 767).
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus` (gen 8-17 extension; 14 t0083
  joint-pass cells; 18-cell Pareto front; \$0.83 cost overrun motivating
  REQ-X).
* Task: `t0084_t0081_cell_767_vm_trace_deepdive` (cell 767 mechanism
  attribution).
* Paper: `10.1038_nn.2153` (Kole 2008 AIS Nav density).
* Paper: `werginz_2024` (Werginz 2024 AIS-to-soma ratio).
* Paper: `sivyer_2013` (Sivyer 2013 dendritic NMDA).
* Paper: `branco_hausser_2010` (NMDA Mg-block voff).
* Paper: `oesch_2005` (distal Nav1.6).
* Paper: `stuart_1999` (distal NaP).
* Paper: `goldfinger_2000` (distal NaP cross-reference).
* Paper: `de_rosenroll_2026` (GABA spatial gradient).
