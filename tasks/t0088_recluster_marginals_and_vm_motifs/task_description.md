# Re-cluster t0086 Genuine + Marginal cells and per-cluster Vm-trace deep-dive (S-0086-03 extension)

## Motivation

t0086 found k=2 clusters on the 6 Genuine cells with both clusters classified exotic by the
biological scorecard (NMDA per-synapse +85-122 sigma above Sivyer 2013, NaP +7-24 sigma above Stuart
1999). This raises two questions that S-0086-03 set out to address: (a) do different cells inside
each cluster share a common biophysical mechanism (e.g., NaP-dominant vs NMDA-dominant), or do they
all use the same mechanism but at different scales; (b) do clusters partition cells by mechanism.
The original S-0086-03 scope ran the deep-dive on the 6 Genuine cells only; this extension adds the
7 Marginal cells from t0086 (cells 767, 1304, 1379, 1504, 1559, 1624, 1721) for a 13-cell
re-clustering pool, then deep-dives at higher angular resolution (16 directions every 22.5 deg) on a
representative cell per cluster. The wider 13-cell pool reveals mechanism heterogeneity that the
6-Genuine-only clustering may miss, and the 16-direction resolution exceeds t0084's 8-direction
deep-dive.

The combined task design follows the recorded researcher preference for one consolidated task
bundling related suggestions and infra/protocol fixes. Source suggestion: **S-0086-03** (extended
scope).

## Cell Set

13 cells from t0086:

* **6 Genuine** (t0086 5/5 reps pass DSI >= 0.4 AND PD >= 10 Hz): 1517, 1604, 1634, 1639, 1663, 1677
* **7 Marginal** (t0086 3-4/5 reps pass): 767, 1304, 1379, 1504, 1559, 1624, 1721

Cell 767's 54-d natural-unit parameter vector lives in
`tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` (the warm-start lineage).
Cells 1238-1727 (which include all 12 of the remaining 13-cell pool) live in
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json`. The implementation
must verify which task contains each cell's saved parameters before loading.

## Scope

### Phase A -- Re-cluster 13 cells

* Load `tasks/t0086_robustness_cluster_bio_comparison/results/data/cell_classification.json` to
  identify the 6 Genuine + 7 Marginal cells.
* Load 54-d natural-unit parameter vectors per cell from t0081 / t0083 `all_evaluations.json`.
* Re-run KMeans for k = 2..6, hierarchical clustering with ward linkage and both cosine + euclidean
  metrics, and 2D visualisation via UMAP (or PCA fallback if UMAP fit fails).
* Pick best k via silhouette + BIC.
* Compute per-cluster centroids in 54-d natural-unit space.
* Re-use `tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py` and
  `biological_scorecard.py` to score each new cluster centroid against published priors (Kole 2008
  AIS Nav, Werginz 2024 mouse alpha-RGC AIS-to-soma Nav ratio, Sivyer 2013 dendritic NMDA, Oesch
  2005 + Goldfinger 2000 + Stuart 1999 distal Nav1.6 / NaP, de Rosenroll 2026 GABA / AMPA spatial
  distribution, Branco-Hausser 2010 NMDA Mg-block).
* Output: `results/data/recluster_assignments.json`, `results/data/recluster_centroids.json`,
  `results/data/recluster_biological_scorecard.json`. Plus PNGs: cluster UMAP / silhouette /
  dendrogram / heatmap, matching t0086's plotting style.

### Phase B -- Per-cluster Vm-trace deep-dive

* For each cluster, pick a representative cell as the cell with minimum 54-d Euclidean distance to
  the cluster centroid.

* For each representative cell, run a t0084-style deep-dive at **16 directions** (every 22.5 deg)
  instead of t0084's 8 directions. Use 1 inner replication per direction.

* Re-use t0084's `run_deepdive.py` per-segment recording pattern. Record per-segment Vm at proximal
  soma, mid-dendrite, distal-dendrite, AIS; per-segment NMDA conductance trajectories (`gnmda` over
  time at each `bundle.syns_nmda` synapse, distal dendrite); per-segment Nav1.6 (`nav16t80._ref_i`)
  and NaP (`napt80._ref_i`) currents at distal dendrite; AIS Vm and threshold-crossing spike onset
  times.

* Per representative cell, generate 4 figures matching t0084:

  1. Per-direction Vm traces (3-row x 16-column grid: proximal soma / mid dendrite / distal
     dendrite)
  2. NMDA conductance trajectories at distal dendrite per direction (16-line plot)
  3. Nav1.6 / NaP current decomposition at distal dendrite per direction (16-direction subplots)
  4. AIS spike onset histogram per direction (polar or 16-bin bar)

* Compute fractional channel contributions per cluster representative (matching t0084's
  `attribution_metric.py` pattern but applied to the new cells).

### Phase C -- Mechanism distinctness analysis

* Compare fractional contributions across clusters: do different clusters use different dominant
  mechanisms (e.g., one NMDA-dominant, one NaP-dominant, one Nav1.6-dominant), or do they all share
  the same mechanism but vary in scale?
* Compare to t0084's cell 767 attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%): does the per-seed
  re-evaluation reveal mechanism heterogeneity that single-seed attribution missed?
* Per-cluster narrative: which biophysical strategy does this cluster represent?

### Output

Answer asset at `assets/answer/are-cluster-motifs-mechanistically-distinct/` per the answer asset
specification (`meta/asset_types/answer/specification.md`), with quantitative attribution per
cluster.

## Pass criteria

* **Primary**: produce a clear mechanism-distinctness verdict (clusters are mechanistically distinct
  vs share the same mechanism).
* **Secondary**: per-cluster representative Vm-trace deep-dive figures published.
* **Acceptable negative**: clusters are NOT mechanistically distinct (all use the same NMDA-dominant
  strategy, differing only in parameter scale) is itself a useful finding aligning with t0086's
  exotic-NMDA verdict.

## Compute and Budget

* Phase A: pure data analysis, $0, ~10 min.
* Phase B: per representative cell at 16 directions x 1 inner replication = 16 NEURON sims at ~60 s
  each per cell = ~16 min per cell. With 2-3 cluster representatives = 32-48 min total local CPU.
* Phase C: data analysis, $0.

**Local CPU only. No remote machine. Total wall-clock ~1-2 hours, $0 cost.** No remote-machine
provisioning or Vast.ai authentication required.

Project budget after t0086: ~$15.56 / $20.00 used, ~$4.44 remaining. t0088 estimated $0 -- no budget
impact.

## Dependencies

* **t0024_port_de_rosenroll_2026_dsgc** -- the de Rosenroll 2026 base port that defines the model
  substrate.
* **t0078_bedb_mobo_v2_ais_tiered_ahp** -- the v2 substrate predecessor.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** -- the v3 substrate library (active dendritic
  conductances + tiered AHP) used for re-evaluation.
* **t0081_bedb_v3_warmstart_nsga2** -- contains cell 767's 54-d parameter vector in
  `results/data/all_evaluations.json`.
* **t0083_bedb_v3_extend_nsga2_gen8plus** -- contains the 12 remaining cells' 54-d parameter vectors
  in `results/data/all_evaluations.json`.
* **t0084_t0081_cell_767_vm_trace_deepdive** -- contains `code/run_deepdive.py` and the per-segment
  recording pattern this task re-uses.
* **t0086_robustness_cluster_bio_comparison** -- contains `code/biological_priors.py`,
  `biological_scorecard.py`, the cell classification, and the original 6-Genuine clustering this
  task extends.

## Cross-task code reuse

Per the cross-task import rule (no direct imports across task folders; only library asset imports),
this task copies the needed code into its own `code/` directory:

* Copy `tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py` and
  `biological_scorecard.py` into `tasks/t0088_recluster_marginals_and_vm_motifs/code/`, rebinding
  imports.
* Copy `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/run_deepdive.py` (or equivalent)
  per-segment recording pattern into `tasks/t0088_recluster_marginals_and_vm_motifs/code/`,
  rebinding imports.

The library asset `de_rosenroll_2026_dsgc_ais_dendritic_spike` (the v3 substrate from t0080) is
imported normally.

## Expected Assets

`expected_assets = {"answer": 1}`. The single answer asset at
`assets/answer/are-cluster-motifs-mechanistically-distinct/` per the answer-asset specification.

## Task Types

`["data-analysis", "experiment-run", "answer-question"]`. Phase A is data-analysis (Pandas / sklearn
/ matplotlib); Phase B is experiment-run (NEURON simulations local CPU); Phase C produces the answer
asset.

## Output specification

* `results/data/recluster_assignments.json`: per-cell cluster id (Phase A).
* `results/data/recluster_centroids.json`: cluster centroids in 54-d natural-unit space (Phase A).
* `results/data/recluster_biological_scorecard.json`: per-cluster biological-plausibility scorecard
  (Phase A).
* `results/data/representative_cells.json`: which cell represents each cluster (Phase B).
* `results/data/per_direction_recordings_<cell_id>.npz`: per-segment Vm + NMDA + Nav1.6 + NaP
  recordings per direction per representative cell (Phase B).
* `results/data/attribution_<cell_id>.json`: fractional channel contributions per representative
  cell (Phase B).
* `results/data/mechanism_distinctness.json`: per-cluster mechanism narrative + verdict (Phase C).
* `results/images/cluster_umap.png`, `cluster_silhouette.png`, `cluster_dendrogram.png`,
  `cluster_heatmap.png` (Phase A).
* `results/images/vm_traces_<cell_id>.png`, `nmda_conductance_<cell_id>.png`,
  `nav_decomp_<cell_id>.png`, `ais_spike_onset_<cell_id>.png` per representative cell (Phase B).
* `assets/answer/are-cluster-motifs-mechanistically-distinct/{details.json, short_answer.md, full_answer.md}`
  (Phase C).

## Concrete questions answered

1. How many clusters does the 13-cell pool partition into (vs t0086's k=2 on 6 cells)?
2. What is the per-cluster fractional channel attribution at 16 directions?
3. Are the clusters mechanistically distinct, or do they share a mechanism with parameter-scale
   variation?
4. Does cell 767's NaP-dominant attribution from t0084 (single-seed 8 directions) hold up at
   16-direction resolution and after re-clustering with the 13-cell pool?
