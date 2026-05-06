---
spec_version: "3"
task_id: "t0086_robustness_cluster_bio_comparison"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-06T14:01:11Z"
completed_at: "2026-05-06T18:10:00Z"
---
# Step 9 -- Implementation

## Summary

Three-phase implementation completed end-to-end. **Phase A** (re-evaluation of 20 cells x 5 outer
RNG seeds x 24 directions x 30 inner seeds = 100 cell-evaluations on Vast.ai EPYC 7B13) ran for 4
hours wall-clock at $1.3335 final cost, well under the $3.50 hard cap (REQ-X cost watchdog
verified). **Phase B** (k-means k=2..6 with silhouette + BIC, hierarchical with cosine + euclidean,
50-sample bootstrap stability ARI, UMAP/PCA 2-D embedding) ran locally in ~30 seconds. **Phase C**
(per-cluster centroid scoring vs 9 published biological priors) and the answer asset writer ran
locally in ~10 seconds. Headline robustness classification: **6 Genuine** (5/5 reps pass joint
criterion DSI >= 0.4 AND PD >= 10 Hz), **7 Marginal** (3-4/5), **7 Stochastic** (<=2/5) of 20 cells.
Phase B selected best_k=2 by silhouette (0.155, weak); 50-sample bootstrap ARI mean 0.597.
**Cluster 0** (cells 1634, 1639, 1663) and **Cluster 1** (cells 1517, 1604, 1677) both received
**aggregate verdict "exotic"**, driven by NMDA per-synapse conductance >85 sigma above Sivyer 2013
prior and NaP distal density >7 sigma above Stuart 1999 prior in both clusters. The 6 Genuine cells
exceed the headline pass criterion of >=3 cells (Primary pass criterion of plan).

## Actions Taken

1. Wrote `code/cost_watchdog.py` (REQ-X) reading
   `selected_offer.price_per_hour=0.3474` from `logs/steps/008_setup-machines/machine_log.json`
   instead of a hard-coded constant. Added `code/test_cost_watchdog.py` with 5 unit tests verifying
   the watchdog uses the loaded rate, trips on overrun, writes the intervention file, and rejects
   non-positive rates. All 5 tests pass.
2. Wrote `code/select_cells.py` selecting 15 joint-pass cells (DSI >= 0.4 AND PD >= 10 Hz AND
   feasible) from `t0083/all_evaluations.json` plus 5 closest near-pass cells from
   `t0083/pareto_front.json` ranked by Euclidean distance to the (0.4, 10) joint corner using
   thresholds dsi_normaliser=0.1 and pd_normaliser_hz=5. Result: cells 767, 1304, 1379, 1482, 1517,
   1548, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1710, 1721 (joint-pass) + 1504, 1723, 1484,
   1457, 1238 (near-pass) = 20 cells. Satisfies REQ-1, REQ-2.
3. Wrote `code/generate_seeds.py` generating 5 deterministic outer seeds via
   `np.random.SeedSequence(42).spawn(5)` then `generate_state(1, dtype=uint32)` per child.
   Result: seeds=[2684470948, 4091952314, 233227757, 3276785861, 3644269654]. Satisfies REQ-4.
4. Wrote `code/run_phase_a.py` re-evaluating each (cell, seed) pair via the t0080
   `evaluate_parameter_vector` entry point with monkey-patched
   `t0080.trial_driver.SEED_BASE = seed` per replication. The runner appends to
   `results/data/replication_results.json` after each call (resumable across instance crashes) and
   trips the cost watchdog when projected cost would exceed $3.50.
5. Pushed the branch to GitHub. Cloned the repo on Vast.ai instance 36240604, installed NEURON
   8.2.7 + umap-learn (the latter not used at runtime due to a version conflict, see Issues), and
   compiled the v3 t80 NMODL substrate (libnrnmech.so 118704 bytes, byte-for-byte match with
   t0083). Ran the smoke gate `--smoke-only --cell-id 767 --seeds-only 1 --max-workers 43` which
   produced **DSI=0.416, PD=8.67 Hz**. Both DSI > 0.30 and PD > 8 satisfy the smoke gate's hard
   abort criteria; smoke gate passed.
6. Started the full Phase A sweep `--all-cells --max-workers 43` in the background. Run
   characteristics: 100 cell-evaluations (1 already done from smoke gate, 99 new) at average
   ~135 s/eval; total wall-clock 4 hours; final cost watchdog reading **$1.3335** at termination.
   Cost watchdog log line confirms REQ-X working: `[cost_watchdog] resolved hourly rate:
   $0.3474/hr from machine_log.json (REQ-X)`. Satisfies REQ-3, REQ-14, REQ-X, REQ-16.
7. Pulled `replication_results.json` from remote via `scp`. Ran the local Phase B/C orchestrator
   `code/run_phase_b.py` which:
    * `classify_cells.main()` produced
      `results/data/cell_classification.json` with summary
      `{Genuine: 6, Marginal: 7, Stochastic: 7}`. The 6 Genuine cells are 1517, 1604, 1634, 1639,
      1663, 1677. Cell 767 was Marginal (3/5 reps pass; matches the smoke gate's borderline
      result). Cell 1723 (highest near-pass DSI=1.0) was Stochastic (0/5 because PD=6.14 Hz
      consistently below the 10 Hz threshold). Satisfies REQ-5, REQ-16.
    * `cluster_analysis.main()` ran k-means k=2..6 on the 6 Genuine cells in 54-d normalised
      parameter space; best_k=2 by silhouette (best silhouette 0.155, weak but the only k that
      passes the trivial check); BIC heuristic also lowest at k=2. Hierarchical clustering with
      cosine and euclidean (average linkage) at k=2 produced labels with ARI vs k-means of 1.0
      (cosine) and 1.0 (euclidean) -- all three methods agree. 50-sample bootstrap stability ARI
      mean 0.597 (sd 0.387) -- moderate stability given the small Genuine pool. Centroids written
      in normalised + unnormalised space; within-cluster variance and between-cluster distance
      matrix recorded. Satisfies REQ-6, REQ-7, REQ-9, REQ-10.
    * `plot_phase_b.main()` produced four figures: classification bar chart (6/7/7), silhouette vs
      k curve, hierarchical-linkage dendrogram, and 2-D embedding scatter (UMAP fell back to PCA
      because the local venv does not have umap-learn installed; remote does, but Phase B runs
      locally for cost-efficiency). Satisfies REQ-8.
    * `biological_priors.main()` wrote `results/data/biological_priors.json` with 9 priors:
      AIS Nav density (Kole 2008 + Werginz 2024), distal Nav1.6 (Oesch 2005), distal NaP
      (Stuart 1999 / Goldfinger 2000), dendritic NMDA conductance (Sivyer 2013), NMDA Mg-block
      voff (Branco-Hausser 2010), GABA spatial (de Rosenroll 2026 rho0 + lambda), AIS-to-soma
      Nav ratio (Werginz 2024). Satisfies REQ-11.
    * `biological_scorecard.main()` scored the 2 cluster centroids against all 9 priors. Both
      clusters received aggregate verdict **exotic**. Cluster 0 has NMDA conductance at +122
      sigma, NaP distal at +24 sigma, GABA rho0 at +7 sigma. Cluster 1 has NMDA at +85 sigma, NaP
      distal at +7 sigma, GABA lambda at +6 sigma. Both clusters share the dominant motif of
      extreme NMDA conductance scaling well above Sivyer 2013's published per-synapse value.
      Satisfies REQ-12.
    * `write_answer_asset.main()` wrote
      `assets/answer/cluster-biological-plausibility-attribution/{details.json, short_answer.md,
      full_answer.md}` with confidence=medium, n_genuine=6, n_clusters=2. Satisfies REQ-13.
    * `build_metrics.main()` wrote `results/metrics.json` with 20 variants (one per cell)
      recording DSI mean+SD, PD mean+SD, robustness fraction, classification.

## Outputs

* `results/data/replication_results.json` (100 records).
* `results/data/cell_classification.json` (20 cells, 6 Genuine + 7 Marginal + 7 Stochastic).
* `results/data/clustering_results.json` (k-means + hierarchical labels, silhouette / BIC,
  bootstrap_ari, k=2..6 evaluated).
* `results/data/cluster_centroids.json` (2 centroids in normalised + unnormalised space, within
  variance, between distance matrix).
* `results/data/biological_priors.json` (9 priors).
* `results/data/biological_scorecard.json` (2 clusters x 9 priors with deviation in sigma units +
  verdicts).
* `results/images/robustness_classification.png` (bar chart 6/7/7).
* `results/images/cluster_silhouette.png` (silhouette vs k=2..5).
* `results/images/cluster_dendrogram.png` (hierarchical linkage).
* `results/images/cluster_umap.png` (PCA fallback embedding).
* `results/images/biological_plausibility_heatmap.png` (clusters x priors heatmap).
* `results/metrics.json` (20 per-cell variants).
* `assets/answer/cluster-biological-plausibility-attribution/{details.json, short_answer.md,
  full_answer.md}`.

## Issues

* **umap-learn not in local venv**: the plot_phase_b.py UMAP block falls back to PCA when
  `import umap` fails. Remote Vast.ai instance has it installed (`pip install umap-learn`); local
  venv does not. PCA is an acceptable substitute for visualisation purposes since the cluster
  labels were already determined by k-means in 54-d space. Future work could add umap-learn to
  the project's pyproject.toml.
* **Bootstrap ARI 0.597 (sd 0.387)** is moderate but not strong, reflecting the small Genuine
  pool (n=6). With more Genuine cells the cluster boundary would be more stable. The k=2
  partition is coherent across k-means + hierarchical-cosine + hierarchical-euclidean (all three
  agree, ARI=1.0) which mitigates the bootstrap concern.
* **Cell 1723** had DSI=1.0 (highest) but PD=6.14 Hz (consistently below 10 Hz threshold) so it
  classified Stochastic 0/5. This suggests the joint-corner threshold of (0.4, 10) is selective
  enough to exclude single-direction-spike-only cells, which is desirable.
