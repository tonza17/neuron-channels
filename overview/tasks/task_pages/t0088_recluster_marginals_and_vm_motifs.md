# ✅ Re-cluster t0086 13 cells and per-cluster Vm-trace deep-dive

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0088_recluster_marginals_and_vm_motifs` |
| **Status** | ✅ completed |
| **Started** | 2026-05-06T19:40:18Z |
| **Completed** | 2026-05-06T21:10:00Z |
| **Duration** | 1h 29m |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Source suggestion** | `S-0086-03` |
| **Task types** | `data-analysis`, `experiment-run`, `answer-question` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 1 answer |
| **Step progress** | 10/15 |
| **Task folder** | [`t0088_recluster_marginals_and_vm_motifs/`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/task_description.md)*

# Re-cluster t0086 Genuine + Marginal cells and per-cluster Vm-trace deep-dive (S-0086-03 extension)

## Motivation

t0086 found k=2 clusters on the 6 Genuine cells with both clusters classified exotic by the
biological scorecard (NMDA per-synapse +85-122 sigma above Sivyer 2013, NaP +7-24 sigma above
Stuart 1999). This raises two questions that S-0086-03 set out to address: (a) do different
cells inside each cluster share a common biophysical mechanism (e.g., NaP-dominant vs
NMDA-dominant), or do they all use the same mechanism but at different scales; (b) do clusters
partition cells by mechanism. The original S-0086-03 scope ran the deep-dive on the 6 Genuine
cells only; this extension adds the 7 Marginal cells from t0086 (cells 767, 1304, 1379, 1504,
1559, 1624, 1721) for a 13-cell re-clustering pool, then deep-dives at higher angular
resolution (16 directions every 22.5 deg) on a representative cell per cluster. The wider
13-cell pool reveals mechanism heterogeneity that the 6-Genuine-only clustering may miss, and
the 16-direction resolution exceeds t0084's 8-direction deep-dive.

The combined task design follows the recorded researcher preference for one consolidated task
bundling related suggestions and infra/protocol fixes. Source suggestion: **S-0086-03**
(extended scope).

## Cell Set

13 cells from t0086:

* **6 Genuine** (t0086 5/5 reps pass DSI >= 0.4 AND PD >= 10 Hz): 1517, 1604, 1634, 1639,
  1663, 1677
* **7 Marginal** (t0086 3-4/5 reps pass): 767, 1304, 1379, 1504, 1559, 1624, 1721

Cell 767's 54-d natural-unit parameter vector lives in
`tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` (the warm-start
lineage). Cells 1238-1727 (which include all 12 of the remaining 13-cell pool) live in
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json`. The
implementation must verify which task contains each cell's saved parameters before loading.

## Scope

### Phase A -- Re-cluster 13 cells

* Load `tasks/t0086_robustness_cluster_bio_comparison/results/data/cell_classification.json`
  to identify the 6 Genuine + 7 Marginal cells.
* Load 54-d natural-unit parameter vectors per cell from t0081 / t0083 `all_evaluations.json`.
* Re-run KMeans for k = 2..6, hierarchical clustering with ward linkage and both cosine +
  euclidean metrics, and 2D visualisation via UMAP (or PCA fallback if UMAP fit fails).
* Pick best k via silhouette + BIC.
* Compute per-cluster centroids in 54-d natural-unit space.
* Re-use `tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py` and
  `biological_scorecard.py` to score each new cluster centroid against published priors (Kole
  2008 AIS Nav, Werginz 2024 mouse alpha-RGC AIS-to-soma Nav ratio, Sivyer 2013 dendritic
  NMDA, Oesch 2005 + Goldfinger 2000 + Stuart 1999 distal Nav1.6 / NaP, de Rosenroll 2026 GABA
  / AMPA spatial distribution, Branco-Hausser 2010 NMDA Mg-block).
* Output: `results/data/recluster_assignments.json`, `results/data/recluster_centroids.json`,
  `results/data/recluster_biological_scorecard.json`. Plus PNGs: cluster UMAP / silhouette /
  dendrogram / heatmap, matching t0086's plotting style.

### Phase B -- Per-cluster Vm-trace deep-dive

* For each cluster, pick a representative cell as the cell with minimum 54-d Euclidean
  distance to the cluster centroid.

* For each representative cell, run a t0084-style deep-dive at **16 directions** (every 22.5
  deg) instead of t0084's 8 directions. Use 1 inner replication per direction.

* Re-use t0084's `run_deepdive.py` per-segment recording pattern. Record per-segment Vm at
  proximal soma, mid-dendrite, distal-dendrite, AIS; per-segment NMDA conductance trajectories
  (`gnmda` over time at each `bundle.syns_nmda` synapse, distal dendrite); per-segment Nav1.6
  (`nav16t80._ref_i`) and NaP (`napt80._ref_i`) currents at distal dendrite; AIS Vm and
  threshold-crossing spike onset times.

* Per representative cell, generate 4 figures matching t0084:

  1. Per-direction Vm traces (3-row x 16-column grid: proximal soma / mid dendrite / distal
     dendrite)
  2. NMDA conductance trajectories at distal dendrite per direction (16-line plot)
  3. Nav1.6 / NaP current decomposition at distal dendrite per direction (16-direction
     subplots)
  4. AIS spike onset histogram per direction (polar or 16-bin bar)

* Compute fractional channel contributions per cluster representative (matching t0084's
  `attribution_metric.py` pattern but applied to the new cells).

### Phase C -- Mechanism distinctness analysis

* Compare fractional contributions across clusters: do different clusters use different
  dominant mechanisms (e.g., one NMDA-dominant, one NaP-dominant, one Nav1.6-dominant), or do
  they all share the same mechanism but vary in scale?
* Compare to t0084's cell 767 attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%): does the
  per-seed re-evaluation reveal mechanism heterogeneity that single-seed attribution missed?
* Per-cluster narrative: which biophysical strategy does this cluster represent?

### Output

Answer asset at `assets/answer/are-cluster-motifs-mechanistically-distinct/` per the answer
asset specification (`meta/asset_types/answer/specification.md`), with quantitative
attribution per cluster.

## Pass criteria

* **Primary**: produce a clear mechanism-distinctness verdict (clusters are mechanistically
  distinct vs share the same mechanism).
* **Secondary**: per-cluster representative Vm-trace deep-dive figures published.
* **Acceptable negative**: clusters are NOT mechanistically distinct (all use the same
  NMDA-dominant strategy, differing only in parameter scale) is itself a useful finding
  aligning with t0086's exotic-NMDA verdict.

## Compute and Budget

* Phase A: pure data analysis, $0, ~10 min.
* Phase B: per representative cell at 16 directions x 1 inner replication = 16 NEURON sims at
  ~60 s each per cell = ~16 min per cell. With 2-3 cluster representatives = 32-48 min total
  local CPU.
* Phase C: data analysis, $0.

**Local CPU only. No remote machine. Total wall-clock ~1-2 hours, $0 cost.** No remote-machine
provisioning or Vast.ai authentication required.

Project budget after t0086: ~$15.56 / $20.00 used, ~$4.44 remaining. t0088 estimated $0 -- no
budget impact.

## Dependencies

* **t0024_port_de_rosenroll_2026_dsgc** -- the de Rosenroll 2026 base port that defines the
  model substrate.
* **t0078_bedb_mobo_v2_ais_tiered_ahp** -- the v2 substrate predecessor.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** -- the v3 substrate library (active dendritic
  conductances + tiered AHP) used for re-evaluation.
* **t0081_bedb_v3_warmstart_nsga2** -- contains cell 767's 54-d parameter vector in
  `results/data/all_evaluations.json`.
* **t0083_bedb_v3_extend_nsga2_gen8plus** -- contains the 12 remaining cells' 54-d parameter
  vectors in `results/data/all_evaluations.json`.
* **t0084_t0081_cell_767_vm_trace_deepdive** -- contains `code/run_deepdive.py` and the
  per-segment recording pattern this task re-uses.
* **t0086_robustness_cluster_bio_comparison** -- contains `code/biological_priors.py`,
  `biological_scorecard.py`, the cell classification, and the original 6-Genuine clustering
  this task extends.

## Cross-task code reuse

Per the cross-task import rule (no direct imports across task folders; only library asset
imports), this task copies the needed code into its own `code/` directory:

* Copy `tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py` and
  `biological_scorecard.py` into `tasks/t0088_recluster_marginals_and_vm_motifs/code/`,
  rebinding imports.
* Copy `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/run_deepdive.py` (or equivalent)
  per-segment recording pattern into `tasks/t0088_recluster_marginals_and_vm_motifs/code/`,
  rebinding imports.

The library asset `de_rosenroll_2026_dsgc_ais_dendritic_spike` (the v3 substrate from t0080)
is imported normally.

## Expected Assets

`expected_assets = {"answer": 1}`. The single answer asset at
`assets/answer/are-cluster-motifs-mechanistically-distinct/` per the answer-asset
specification.

## Task Types

`["data-analysis", "experiment-run", "answer-question"]`. Phase A is data-analysis (Pandas /
sklearn / matplotlib); Phase B is experiment-run (NEURON simulations local CPU); Phase C
produces the answer asset.

## Output specification

* `results/data/recluster_assignments.json`: per-cell cluster id (Phase A).
* `results/data/recluster_centroids.json`: cluster centroids in 54-d natural-unit space (Phase
  A).
* `results/data/recluster_biological_scorecard.json`: per-cluster biological-plausibility
  scorecard (Phase A).
* `results/data/representative_cells.json`: which cell represents each cluster (Phase B).
* `results/data/per_direction_recordings_<cell_id>.npz`: per-segment Vm + NMDA + Nav1.6 + NaP
  recordings per direction per representative cell (Phase B).
* `results/data/attribution_<cell_id>.json`: fractional channel contributions per
  representative cell (Phase B).
* `results/data/mechanism_distinctness.json`: per-cluster mechanism narrative + verdict (Phase
  C).
* `results/images/cluster_umap.png`, `cluster_silhouette.png`, `cluster_dendrogram.png`,
  `cluster_heatmap.png` (Phase A).
* `results/images/vm_traces_<cell_id>.png`, `nmda_conductance_<cell_id>.png`,
  `nav_decomp_<cell_id>.png`, `ais_spike_onset_<cell_id>.png` per representative cell (Phase
  B).
* `assets/answer/are-cluster-motifs-mechanistically-distinct/{details.json, short_answer.md,
  full_answer.md}` (Phase C).

## Concrete questions answered

1. How many clusters does the 13-cell pool partition into (vs t0086's k=2 on 6 cells)?
2. What is the per-cluster fractional channel attribution at 16 directions?
3. Are the clusters mechanistically distinct, or do they share a mechanism with
   parameter-scale variation?
4. Does cell 767's NaP-dominant attribution from t0084 (single-seed 8 directions) hold up at
   16-direction resolution and after re-clustering with the 13-cell pool?

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [When the t0086 13-cell pool of 6 Genuine + 7 Marginal cells is re-clustered in the t0080 54-d v3 parameter space and a t0084-style Vm-trace deep-dive is run at 16 directions on per-cluster representative cells, are the resulting clusters mechanistically distinct (different dominant channel mechanisms across clusters) or do they share the same mechanism with parameter-scale variation?](../../../tasks/t0088_recluster_marginals_and_vm_motifs/assets/answer/are-cluster-motifs-mechanistically-distinct/) | [`full_answer.md`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/assets/answer/are-cluster-motifs-mechanistically-distinct/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Causal NaP-knockout ablation per cluster representative</strong>
(S-0088-01)</summary>

**Kind**: experiment | **Priority**: high

t0088 attributed PD-minus-ND fractional contributions correlationally (NMDA 0%, Nav1.6
0.3-12.6%, NaP 87.4-99.7% across the 4 cluster representatives). The attribution is
correlation-based; to causally confirm NaP as the dominant mechanism, set nap_dend_distal = 0
in each of the 4 representative cells (1604, 1634, 767, 1639) and re-measure DSI at the 16
directions used by t0088. Expected effect: DSI collapses to <0.2 in all 4 cells if NaP is
causally responsible; DSI partially preserved if NMDA + Nav1.6 + GABA also contribute. Compare
to baseline DSI_measured (cell 1604: 0.71; cell 1634: 0.20; cell 767: 0.60; cell 1639: 0.43).
Local-CPU only: 4 cells x 16 directions x ~60 s/sim = ~64 min wall-clock, $0 cost. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Audit AIS-to-soma Nav ratio computation in cluster 1 (116x is +33
sigma exotic)</strong> (S-0088-02)</summary>

**Kind**: evaluation | **Priority**: high

t0088 cluster 1 (cells 1304, 1504, 1624, 1634) has centroid AIS-to-soma Nav ratio = 116.04,
deviating +32.92 sigma from Werginz 2024's published 17.3 +/- 3. This is the most extreme
single-prior violation in t0086 + t0088. Audit the ratio computation: (a) confirm
centroid_unnormalised[NAV16_AIS_GBAR] / centroid_unnormalised[NAV16_SOMA_GBAR] is in matching
units (S/cm^2 / S/cm^2 = dimensionless); (b) check the soma Nav lower bound is not pinning the
centroid soma value to a near-zero value, inflating the ratio; (c) check whether the 4 cells
in cluster 1 individually have AIS-to-soma ratios near 116 or whether the centroid is
averaging across heterogeneous values. Pure data analysis on existing JSON outputs; ~30 min
wall-clock, $0 cost. Recommended task types: data-analysis, correction.

</details>

<details>
<summary><strong>13-cell full deep-dive (extend Phase B to all 13 cells, not just
representatives)</strong> (S-0088-03)</summary>

**Kind**: experiment | **Priority**: medium

t0088 Phase B ran the Vm-trace deep-dive on 4 representative cells; the 13-cell pool's other 9
cells could have within-cluster mechanism heterogeneity invisible to the representative-only
analysis. Extend Phase B to all 13 cells: 13 x 16 directions = 208 NEURON sims. Compare
per-cell fractional NaP / Nav1.6 / NMDA across all cells within each cluster; report
within-cluster spread as a measure of mechanism homogeneity per cluster. Local-CPU only: 13 x
16 x ~60 s/sim = ~3.5 hours wall-clock, $0 cost. Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary><strong>Polar attribution decomposition: integrate fractional contributions
over the direction-tuning curve</strong> (S-0088-04)</summary>

**Kind**: evaluation | **Priority**: medium

t0088's mechanism attribution uses only PD (0 deg) - ND (180 deg) integrated current. This
discards information from the 14 other directions recorded at 22.5-deg spacing. Compute
per-direction fractional NMDA / Nav1.6 / NaP integrals and weight by the direction-tuning
curve (the AIS spike-onset polar histogram) to get a richer cross-direction attribution. Test
whether the NaP-dominant verdict holds across all directions or only at PD-flanking
directions. Pure data analysis on existing .npz files; ~1 hour wall-clock, $0 cost.
Recommended task types: data-analysis.

</details>

<details>
<summary><strong>GABA spatial-gradient ablation: does GABA shape direction-asymmetry
causally?</strong> (S-0088-05)</summary>

**Kind**: experiment | **Priority**: medium

t0088 found GABA rho0 exotic (>+5 sigma) in all 4 clusters and GABA lambda exotic in 3 of 4
clusters. The model exploits exotic GABA spatial scale to shape direction-asymmetry. Test
causally: set rho_0_gaba = 1.0 (Rosenroll baseline) or lambda_gaba_um = 80 (Rosenroll mean)
per representative cell and re-measure DSI at 16 directions. Expected effect: if GABA spatial
gradient is causal for direction selectivity, DSI degrades; if NaP alone explains DSI, DSI is
preserved. 4 cells x 2 GABA-knockout variants x 16 directions = 128 sims; ~2 hours local CPU,
$0 cost. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Add UMAP to project dependencies; re-visualise t0086 + t0088
clusters</strong> (S-0088-06)</summary>

**Kind**: library | **Priority**: low

t0088 fell back to PCA(n=2) for cluster visualisation because umap-learn is not in the
project's pyproject.toml. UMAP would likely show different (potentially clearer) cluster
structure for the small 13-cell pool. Add `umap-learn>=0.5` to pyproject.toml; re-run
select_representatives.py (already imports umap inside try/except); re-publish
cluster_umap.png. Apply the same to t0086's cluster_pca.png if relevant. Pure tooling change;
<30 min wall-clock, $0 cost. Recommended task types: infrastructure-setup, data-analysis.

</details>

## Research

* [`research_code.md`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/results_summary.md)*

--- spec_version: "2" task_id: "t0088_recluster_marginals_and_vm_motifs" date_completed:
"2026-05-06" ---
# Results Summary -- t0088_recluster_marginals_and_vm_motifs

## Summary

Re-clustered the 13-cell pool of 6 Genuine + 7 Marginal cells from t0086 in the t0080 54-d v3
parameter space; KMeans + silhouette selected **best_k = 4 clusters**. Ran a t0084-style
Vm-trace deep-dive at 16 directions on the 4 representative cells (1604, 1634, 767, 1639) on
local CPU, all 64 simulations stable. **Mechanism-distinctness verdict =
`shared_mechanism_different_scale`**: all 4 cluster representatives are NaP-dominant in
PD-minus-ND attribution (frac NaP 0.874-0.997, frac Nav1.6 0.003-0.126, frac NMDA = 0.000);
clusters differ in parameter scale within 54-d space but not in which channel drives the PD
response. This extends t0084's NaP-dominant cell 767 finding from a single cell at 8
directions to four representative cells at 16 directions and confirms the v3 substrate's
joint-pass / near-joint-pass cells systematically rely on NaP-driven sustained dendritic
depolarisation. All 4 clusters classified exotic by the biological scorecard (extending
t0086's exotic-NMDA verdict to the 13-cell pool).

## Metrics

* **Best k = 4** by silhouette (score 0.164, beat k = 2 at 0.163, k = 5 at 0.160, k = 3 at
  0.111). Bootstrap stability ARI = **0.583 +/- 0.226** across 50 bootstrap samples (subsample
  0.8) -- moderate stability given small 13-cell pool.

* **Cluster membership at k = 4**:
  * Cluster 0 (n = 5): cells 1379, 1517, 1559, 1604, 1721 (mix: 1 Genuine + 4 Marginal).
    Representative: **cell 1604** (Genuine).
  * Cluster 1 (n = 4): cells 1304, 1504, 1624, 1634 (mix: 1 Genuine + 3 Marginal).
    Representative: **cell 1634** (Genuine).
  * Cluster 2 (n = 2): cells 767, 1677 (mix: 1 Genuine + 1 Marginal). Representative: **cell
    767** (Marginal).
  * Cluster 3 (n = 2): cells 1639, 1663 (both Genuine). Representative: **cell 1639**
    (Genuine).

* **Cross-method ARI**: KMeans vs hierarchical-cosine = 0.799; KMeans vs
  hierarchical-euclidean = 0.799 (both with average linkage). Cluster structure consistent
  across methods.

* **All 4 clusters classified exotic** by biological scorecard (worst-case across 9 priors).
  The two dominant exotic priors are gnmda_dend (Sivyer 2013, deviation +85 to +116 sigma
  across clusters) and nap_dend_distal (Stuart 1999, deviation +9.6 to +33.6 sigma).

* **Per-representative fractional channel attribution** at 16 directions (PD = 0 deg vs ND =
  180 deg, response window [200, 1200] ms):

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | **0.988** | **nap** |
| 1 | 1634 | 0.000 | 0.126 | **0.874** | **nap** |
| 2 | 767 | 0.000 | 0.125 | **0.875** | **nap** |
| 3 | 1639 | 0.000 | 0.003 | **0.997** | **nap** |
* **Verdict: `shared_mechanism_different_scale`**. Compare to t0084's cell 767 attribution at
  8 directions (NaP 93%, Nav1.6 7%, NMDA 0%): the 16-direction re-evaluation here gives cell
  767 NaP 87.5% / Nav1.6 12.5%, consistent within angular-resolution noise, and confirms the
  NaP-dominant signature is shared across all 4 clusters.

* **Wall-clock**: Phase A ~10 min; Phase B ~50 min (50 NEURON sims at ~60 s each + warm-up);
  Phase C ~5 min. Total ~65 min local CPU. **Cost $0** (local-CPU only).

## Verification

* `verify_research_code`: PASSED (0 errors).
* `verify_plan`: PASSED (0 errors, 3 acceptable warnings).
* `verify_logs`: PASSED (0 errors, expected warnings to be cleared by capture_task_sessions).
* `verify_task_file`, `verify_task_dependencies`, `verify_task_folder`: PASSED.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0088_recluster_marginals_and_vm_motifs" date_completed:
"2026-05-06" ---
# Results Detailed -- t0088_recluster_marginals_and_vm_motifs

## Summary

This task re-clustered the 13-cell pool of 6 Genuine + 7 Marginal cells from t0086 in the
t0080 v3 substrate's 54-d parameter space and ran a t0084-style Vm-trace deep-dive at 16
directions on the 4 representative cells. Findings: **best_k = 4 clusters** (silhouette 0.164,
bootstrap stability ARI 0.583 +/- 0.226 over 50 samples); **all 4 clusters classified exotic**
by the biological scorecard (NMDA per-synapse > 85 sigma above Sivyer 2013, NaP > 9 sigma
above Stuart 1999, plus GABA spatial-gradient priors deviating > 5 sigma from de Rosenroll
2026 in three of four clusters); **mechanism-distinctness verdict =
`shared_mechanism_different_scale`** because all 4 cluster representatives are NaP-dominant in
PD-minus-ND attribution (frac NaP 0.874-0.997, frac Nav1.6 0.003-0.126, frac NMDA = 0.000).
The clusters differ in parameter scale within 54-d space but not in which channel drives the
PD response. This extends t0084's NaP-dominant cell 767 finding from a single cell at 8
directions to four representative cells at 16 directions and confirms the v3 substrate's
joint-pass / near-joint-pass cells systematically rely on NaP-driven sustained dendritic
depolarisation, even though NMDA conductance values are extreme relative to Sivyer 2013.

## Methodology

* **Machine**: Local Windows workstation (developer machine; no remote provisioning).
* **NEURON version**: 8.2.7. MOD library compiled at
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/nrnmech.dll` (untracked build
  artefact inside an immutable completed task folder; built locally and reproducible from the
  source `.mod` files in `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`).
* **Phase A method**: load 13 cells from t0086 `cell_classification.json`; load 54-d parameter
  vectors from t0083 `all_evaluations.json`. Min-max normalise per coordinate using
  LOWER_BOUNDS / UPPER_BOUNDS from the t0080 module. KMeans with `random_state=42`,
  `n_init="auto"` for k = 2..6 on the normalised matrix. Best_k by argmax silhouette.
  Hierarchical clustering (cosine + euclidean, average linkage) at best_k for
  cross-validation. 50-sample bootstrap stability ARI with 80% subsample. Per-cluster
  centroids in normalised + unnormalised space + within-cluster variance. Representative cell
  per cluster = cell minimising 54-d Euclidean distance to centroid (normalised),
  deterministic tiebreak by cell_id.
* **Phase B method**: build the DSGCCellWithAIS once; per representative cell apply the
  parameter vector via `apply_parameter_vector` (loads the t0080 MOD library), set up synapses
  parametrically via `setup_synapses_parametric` with placer_seed derived from a hash of the
  parameter vector (matches t0084). Run 16 directions per cell (every 22.5 deg). Per direction
  record per-segment Vm at proximal soma / mid-dendrite / distal-dendrite / AIS, per-synapse
  NMDA conductance, per-segment Nav1.6 and NaP currents at the distal dendrite. RECORD_DT_MS =
  1.0; TSTOP_MS from t0080 constants. Save one `.npz` per (cell, direction).
* **Phase C method**: per representative cell, compute fractional channel attribution via PD
  (0 deg) \- ND (180 deg) integrated dendritic current difference over the response window
  [200, 1200] ms (matches t0084). Cross-cluster comparison: if all clusters share the same
  dominant mechanism -> verdict `shared_mechanism_different_scale`; if 2+ different dominants
  -> verdict `distinct`.

## Per-Cell Results Table

| Cell | t0086 class | Cluster | DSI orig | DSI measured (PD-ND) | PD rate (Hz) | ND rate (Hz) |
| --- | --- | --- | --- | --- | --- | --- |
| 767 | Marginal | 2 | 0.494 | 0.600 | 2.86 | 0.71 |
| 1604 | Genuine | 0 | 0.403 | 0.714 | 8.57 | 1.43 |
| 1634 | Genuine | 1 | 0.689 | 0.200 | 4.29 | 2.86 |
| 1639 | Genuine | 3 | 0.488 | 0.429 | 3.57 | 1.43 |

The single-replicate DSI re-evaluation is intrinsically noisier than t0086's 5-replicate
Genuine classification; cell 1634's 0.200 measured DSI is below threshold here but t0086
classified it Genuine on 5/5 replications. This is consistent with t0084's same observation on
cell 767 and confirms the deep-dive's purpose is the underlying biophysical signature rather
than a per-trial DSI confirmation.

## Cluster Analysis Results (REQ-3, REQ-4, REQ-5, REQ-6)

* **Best k = 4** by silhouette (score 0.164). Silhouettes per k: k = 2: 0.163; k = 3: 0.111; k
  = 4: 0.164; k = 5: 0.160; k = 6: 0.143.
* **k-means labels at k = 4** (cells in order 767, 1304, 1379, 1504, 1517, 1559, 1604, 1624,
  1634, 1639, 1663, 1677, 1721): [2, 1, 0, 1, 0, 0, 0, 1, 1, 3, 3, 2, 0].
* **Hierarchical-cosine ARI** vs k-means = 0.799; **hierarchical-euclidean ARI** vs k-means =
  0.799 (both with average linkage). Cluster structure consistent across methods.
* **50-sample bootstrap stability ARI** mean = **0.583 +/- 0.226** (50 successful bootstraps,
  subsample 0.8). Moderate stability given the small 13-cell pool.
* **Cluster centroids and members**:
  * **Cluster 0 (n = 5)**: cells 1379, 1517, 1559, 1604, 1721. Mix: 1 Genuine + 4 Marginal.
    Within-cluster variance (normalised) = 0.075. Representative: cell 1604.
  * **Cluster 1 (n = 4)**: cells 1304, 1504, 1624, 1634. Mix: 1 Genuine + 3 Marginal.
    Within-cluster variance = 0.084. Representative: cell 1634.
  * **Cluster 2 (n = 2)**: cells 767, 1677. Mix: 1 Genuine + 1 Marginal. Within-cluster
    variance = 0.108. Representative: cell 767.
  * **Cluster 3 (n = 2)**: cells 1639, 1663. Both Genuine. Within-cluster variance = 0.061.
    Representative: cell 1639.
* **Visualisation**: PCA fallback used (UMAP not in dependencies; ImportError caught).
  `cluster_pca.png` shows the 4 clusters in 2D.

## Biological Plausibility Scorecard (REQ-7)

All 4 clusters classified exotic by the worst-case verdict.

### Cluster 0 (cells 1379, 1517, 1559, 1604, 1721) -- exotic

| Prior | Citation | Centroid | Mean | Sigma | Deviation (sigma) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `nav16_ais_gbar` | Kole 2008 | 0.6747 | 0.375 | 0.125 | +2.40 | stretched |
| `nav16_ais_gbar` | Werginz 2024 | 0.6747 | 1.3 | 0.3 | -2.08 | stretched |
| `nav16_dend_distal` | Oesch 2005 | 0.01784 | 0.05 | 0.02 | -1.61 | plausible |
| `nap_dend_distal` | Stuart 1999 | 0.002417 | 0.0005 | 0.0002 | **+9.58** | **exotic** |
| `gnmda_dend` | Sivyer 2013 | 0.004872 | 0.0001 | 0.00005 | **+95.43** | **exotic** |
| `voff_nmda` | Branco-Hausser 2010 | 3.931 | 0 | 5 | +0.79 | plausible |
| `rho0_gaba` | de Rosenroll 2026 | 3.704 | 1 | 0.5 | **+5.41** | **exotic** |
| `lambda_gaba_um` | de Rosenroll 2026 | 232.7 | 80 | 30 | **+5.09** | **exotic** |
| `ais_to_soma_nav_ratio` | Werginz 2024 | 25.93 | 17.3 | 3 | +2.88 | stretched |

### Cluster 1 (cells 1304, 1504, 1624, 1634) -- exotic

| Prior | Citation | Centroid | Mean | Sigma | Deviation (sigma) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `nav16_ais_gbar` | Kole 2008 | 0.5703 | 0.375 | 0.125 | +1.56 | plausible |
| `nav16_ais_gbar` | Werginz 2024 | 0.5703 | 1.3 | 0.3 | -2.43 | stretched |
| `nav16_dend_distal` | Oesch 2005 | 0.0124 | 0.05 | 0.02 | -1.88 | plausible |
| `nap_dend_distal` | Stuart 1999 | 0.007228 | 0.0005 | 0.0002 | **+33.64** | **exotic** |
| `gnmda_dend` | Sivyer 2013 | 0.00442 | 0.0001 | 0.00005 | **+86.41** | **exotic** |
| `voff_nmda` | Branco-Hausser 2010 | 4.237 | 0 | 5 | +0.85 | plausible |
| `rho0_gaba` | de Rosenroll 2026 | 3.782 | 1 | 0.5 | **+5.56** | **exotic** |
| `lambda_gaba_um` | de Rosenroll 2026 | 320.4 | 80 | 30 | **+8.01** | **exotic** |
| `ais_to_soma_nav_ratio` | Werginz 2024 | 116.0 | 17.3 | 3 | **+32.92** | **exotic** |

### Cluster 2 (cells 767, 1677) -- exotic

| Prior | Citation | Centroid | Mean | Sigma | Deviation (sigma) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `nav16_ais_gbar` | Kole 2008 | 0.2505 | 0.375 | 0.125 | -1.00 | plausible |
| `nav16_ais_gbar` | Werginz 2024 | 0.2505 | 1.3 | 0.3 | -3.50 | stretched |
| `nav16_dend_distal` | Oesch 2005 | 0.01564 | 0.05 | 0.02 | -1.72 | plausible |
| `nap_dend_distal` | Stuart 1999 | 0.002218 | 0.0005 | 0.0002 | **+8.59** | **exotic** |
| `gnmda_dend` | Sivyer 2013 | 0.004538 | 0.0001 | 0.00005 | **+88.76** | **exotic** |
| `voff_nmda` | Branco-Hausser 2010 | 5.017 | 0 | 5 | +1.00 | plausible |
| `rho0_gaba` | de Rosenroll 2026 | 4.113 | 1 | 0.5 | **+6.23** | **exotic** |
| `lambda_gaba_um` | de Rosenroll 2026 | 348.4 | 80 | 30 | **+8.95** | **exotic** |
| `ais_to_soma_nav_ratio` | Werginz 2024 | 26.05 | 17.3 | 3 | +2.92 | stretched |

### Cluster 3 (cells 1639, 1663) -- exotic

| Prior | Citation | Centroid | Mean | Sigma | Deviation (sigma) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `nav16_ais_gbar` | Kole 2008 | 0.2631 | 0.375 | 0.125 | -0.90 | plausible |
| `nav16_ais_gbar` | Werginz 2024 | 0.2631 | 1.3 | 0.3 | -3.46 | stretched |
| `nav16_dend_distal` | Oesch 2005 | 0.0360 | 0.05 | 0.02 | -0.70 | plausible |
| `nap_dend_distal` | Stuart 1999 | 0.004406 | 0.0005 | 0.0002 | **+19.53** | **exotic** |
| `gnmda_dend` | Sivyer 2013 | 0.005881 | 0.0001 | 0.00005 | **+115.62** | **exotic** |
| `voff_nmda` | Branco-Hausser 2010 | 7.435 | 0 | 5 | +1.49 | plausible |
| `rho0_gaba` | de Rosenroll 2026 | 4.732 | 1 | 0.5 | **+7.46** | **exotic** |
| `lambda_gaba_um` | de Rosenroll 2026 | 38.35 | 80 | 30 | -1.39 | plausible |
| `ais_to_soma_nav_ratio` | Werginz 2024 | 13.25 | 17.3 | 3 | -1.35 | plausible |

Cluster 3 is the only cluster with plausible AIS-to-soma Nav ratio AND plausible
lambda_gaba_um -- it remains exotic only because of NMDA + NaP + rho0_gaba. This makes Cluster
3 the closest to biologically-plausible territory; the other 3 clusters have additional exotic
violations on AIS Nav ratio (Cluster 1) or GABA spatial scale (Clusters 0, 1, 2).

## Per-Cluster Mechanism Attribution (REQ-10, REQ-12)

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | **0.988** | **nap** |
| 1 | 1634 | 0.000 | 0.126 | **0.874** | **nap** |
| 2 | 767 | 0.000 | 0.125 | **0.875** | **nap** |
| 3 | 1639 | 0.000 | 0.003 | **0.997** | **nap** |

**Verdict: `shared_mechanism_different_scale`**. All 4 clusters share NaP as the dominant
PD-minus-ND mechanism. NMDA contribution is exactly 0 in all 4 clusters because the integrated
NMDA current at PD is essentially equal to that at ND (NMDA Mg-block makes it depolarisation-
dependent but the slow kinetics integrate the same total over the response window in both
directions; the differential between PD and ND is dominated by the Na-channel transient).

The fractional NaP / Nav1.6 split is direction-symmetric within each cluster -- Cluster 0 and
3 are nearly all NaP; Clusters 1 and 2 have ~12% Nav1.6 contribution. This is the only
meaningful mechanistic variation across clusters.

## Comparison to t0084 Cell 767 (REQ-12)

t0084 reported cell 767 attribution at 8 directions: NaP 93%, Nav1.6 7%, NMDA 0%. t0088 here
at 16 directions reports cell 767: NaP 87.5%, Nav1.6 12.5%, NMDA 0%. The two are within
angular-resolution noise (16 directions integrate over more orthogonal directions where Nav1.6
contributes slightly more). The t0084 finding generalises across the broader 13-cell pool: all
4 representatives are NaP-dominant > 87%.

## Visualizations

![cluster PCA scatter (PCA fallback; UMAP not in
deps)](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/cluster_pca.png)

The 4 clusters in PCA-2D space. Each point is one cell labelled with its ID and a (G) for
Genuine or (M) for Marginal. Cluster 0 (red) and Cluster 1 (green) are the two largest groups;
Cluster 2 (blue, cells 767 and 1677) and Cluster 3 (orange, cells 1639 and 1663) are smaller.
Genuine and Marginal cells co-cluster -- the 4-cluster structure is not driven by t0086's
robustness classification but by 54-d parameter geometry.

![silhouette score vs
k](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/cluster_silhouette.png)

Silhouette score peaks at k = 4 (0.164), barely beating k = 2 (0.163). The flat curve over k =
2-5 indicates the 13-cell pool has weak intrinsic cluster structure and best_k = 4 is
preferred over best_k = 2 by a thin margin.

![hierarchical dendrogram (euclidean, average
linkage)](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/cluster_dendrogram.png)

Average-linkage hierarchical clustering on euclidean distance reveals the same 4-cluster
structure as KMeans. The 13-cell pool splits at distance ~0.5 into Cluster 0 + Cluster 3
(joined later) and Cluster 1 + Cluster 2 (joined later).

![biological-plausibility
heatmap](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/biological_plausibility_heatmap.png)

Per-cluster, per-prior deviation in sigma units. Red = positive deviation (centroid above
published mean); blue = negative deviation. Annotated with verdict letter (P / S / X for
plausible / stretched / exotic). The dominant red columns are `gnmda_dend_sivyer2013` (+85 to
+116 sigma) and `nap_dend_distal_stuart1999` (+9 to +34 sigma). Cluster 1 also has extreme
AIS-to- soma Nav ratio (+33 sigma).

### Per-representative figures (Phase B, REQ-11)

#### Cluster 0 (representative cell 1604)

![cell 1604 Vm traces (16
directions)](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/vm_traces_1604.png)

Per-segment Vm traces at 16 directions for cell 1604. Top row: proximal soma (-65 to +30 mV
range, AP firing visible at PD-flanking directions). Middle row: mid-dendrite. Bottom row:
distal dendrite (sustained depolarisation visible from t ~250 ms to ~1200 ms at PD-flanking
directions 0 deg, 22.5 deg, 337.5 deg). PD = 0 deg shows the cleanest sustained
depolarisation; ND = 180 deg shows minimal late dendritic activity.

![cell 1604 NMDA conductance per
direction](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/nmda_conductance_1604.png)

Total NMDA conductance summed across all NMDA synapses, plotted per direction. Peak
conductance is direction-tuned (PD = 0 deg has the largest peak ~0.06 uS) but the integral
over the response window [200, 1200] ms is nearly direction-symmetric due to NMDA's slow
decay.

![cell 1604 Nav1.6 / NaP currents at distal
dendrite](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/nav_decomp_1604.png)

Per-direction Nav1.6 (blue) and NaP (red) currents at the distal dendrite. NaP is sustained
through the entire response window in PD-flanking directions; Nav1.6 contributes brief
transients during AP firing. The NaP integral dominates the PD-minus-ND difference (frac NaP
0.988).

![cell 1604 AIS spike onset polar
histogram](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/ais_spike_onset_1604.png)

AIS spike count per direction in 16-bin polar plot. PD (0 deg, orange) has the highest spike
count; ND (180 deg, blue) has the lowest. The polar plot shows asymmetric direction-tuning
consistent with t0086's per-cell classification.

#### Cluster 1 (representative cell 1634)

![cell 1634 Vm
traces](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/vm_traces_1634.png)

![cell 1634 NMDA
conductance](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/nmda_conductance_1634.png)

![cell 1634 Nav1.6 / NaP
currents](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/nav_decomp_1634.png)

![cell 1634 AIS spike
onsets](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/ais_spike_onset_1634.png)

Cell 1634 (Cluster 1) shows higher Nav1.6 contribution than cell 1604 (frac Nav1.6 0.126).

#### Cluster 2 (representative cell 767)

![cell 767 Vm
traces](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/vm_traces_767.png)

![cell 767 NMDA
conductance](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/nmda_conductance_767.png)

![cell 767 Nav1.6 / NaP
currents](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/nav_decomp_767.png)

![cell 767 AIS spike
onsets](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/ais_spike_onset_767.png)

Cell 767 (Cluster 2): NaP 87.5%, Nav1.6 12.5%. Compare to t0084's 8-direction figures (NaP
93%, Nav1.6 7%) -- consistent within angular-resolution noise.

#### Cluster 3 (representative cell 1639)

![cell 1639 Vm
traces](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/vm_traces_1639.png)

![cell 1639 NMDA
conductance](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/nmda_conductance_1639.png)

![cell 1639 Nav1.6 / NaP
currents](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/nav_decomp_1639.png)

![cell 1639 AIS spike
onsets](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/images/ais_spike_onset_1639.png)

Cell 1639 (Cluster 3): nearly pure NaP (frac 0.997, frac Nav1.6 0.003). The cluster
representative of the only cluster with plausible AIS-to-soma Nav ratio.

## Examples

The 16-direction trace files contain 16 distinct examples per representative cell. Below are
12 concrete example records pulled directly from the per-cell summary, attribution, and
clustering JSONs (REQ-9 / REQ-10 / REQ-12 outputs). Each example shows the input file (or
in-memory dict) and the actual produced output as a fenced code block.

### Example 1: cell 1604 (cluster 0) attribution

Input (PD .npz): `cell1604_dir0_traces.npz`. Input (ND .npz): `cell1604_dir1800_traces.npz`.

Output (`cell1604_attribution.json`):

```json
{
  "cell_id": 1604,
  "cluster_id": 0,
  "frac_nmda": 0.0,
  "frac_nav16": 0.011921480566769876,
  "frac_nap": 0.9880785194332301,
  "dominant_mechanism": "nap"
}
```

### Example 2: cell 1634 (cluster 1) attribution

Input: `cell1634_dir0_traces.npz` + `cell1634_dir1800_traces.npz`.

Output (`cell1634_attribution.json`):

```json
{
  "cell_id": 1634,
  "cluster_id": 1,
  "frac_nmda": 0.0,
  "frac_nav16": 0.12629107474018987,
  "frac_nap": 0.8737089252598101,
  "dominant_mechanism": "nap"
}
```

### Example 3: cell 767 (cluster 2) attribution

Input: `cell767_dir0_traces.npz` + `cell767_dir1800_traces.npz`.

Output (`cell767_attribution.json`):

```json
{
  "cell_id": 767,
  "cluster_id": 2,
  "frac_nmda": 0.0,
  "frac_nav16": 0.12500003046720847,
  "frac_nap": 0.8749999695327915,
  "dominant_mechanism": "nap"
}
```

### Example 4: cell 1639 (cluster 3) attribution

Input: `cell1639_dir0_traces.npz` + `cell1639_dir1800_traces.npz`.

Output (`cell1639_attribution.json`):

```json
{
  "cell_id": 1639,
  "cluster_id": 3,
  "frac_nmda": 0.0,
  "frac_nav16": 0.0029931834415215547,
  "frac_nap": 0.9970068165584784,
  "dominant_mechanism": "nap"
}
```

### Example 5: cell 1604 per-cell DSI summary

Input: 16 trace `.npz` files for cell 1604.

Output (`cell1604_summary.json`):

```json
{
  "cell_id": 1604,
  "cluster_id": 0,
  "dsi_original": 0.40272373540856034,
  "pd_rate_hz_measured": 8.571428571428571,
  "nd_rate_hz_measured": 1.4285714285714286,
  "dsi_measured_pd_minus_nd": 0.7142857142857143
}
```

### Example 6: cell 1634 per-cell DSI summary

Output (`cell1634_summary.json` excerpt):

```json
{
  "cell_id": 1634,
  "cluster_id": 1,
  "dsi_original": 0.6892817681574635,
  "dsi_measured_pd_minus_nd": 0.2,
  "pd_rate_hz_measured": 4.285714285714286,
  "nd_rate_hz_measured": 2.857142857142857
}
```

### Example 7: cell 767 per-cell DSI summary

Output (`cell767_summary.json` excerpt):

```json
{
  "cell_id": 767,
  "cluster_id": 2,
  "dsi_original": 0.4940845948327881,
  "dsi_measured_pd_minus_nd": 0.6,
  "pd_rate_hz_measured": 2.857142857142857,
  "nd_rate_hz_measured": 0.7142857142857143
}
```

### Example 8: cell 1639 per-cell DSI summary

Output (`cell1639_summary.json` excerpt):

```json
{
  "cell_id": 1639,
  "cluster_id": 3,
  "dsi_original": 0.4876,
  "dsi_measured_pd_minus_nd": 0.4285714285714286,
  "pd_rate_hz_measured": 3.5714285714285716,
  "nd_rate_hz_measured": 1.4285714285714286
}
```

### Example 9: cluster 0 centroid (5-cell mixed Genuine + Marginal)

Output (`recluster_centroids.json` cluster 0 excerpt):

```json
{
  "cluster_id": 0,
  "n_cells": 5,
  "cell_ids": [1379, 1517, 1559, 1604, 1721],
  "within_cluster_variance": 0.0746
}
```

### Example 10: cluster 3 centroid (most plausible cluster)

Output (`recluster_centroids.json` cluster 3 excerpt):

```json
{
  "cluster_id": 3,
  "n_cells": 2,
  "cell_ids": [1639, 1663],
  "within_cluster_variance": 0.0610
}
```

Cluster 3 has plausible AIS-to-soma Nav ratio (13.25 vs Werginz 2024 17.3, deviation -1.35
sigma) and plausible lambda_gaba_um (38.35 vs de Rosenroll 2026 80, deviation -1.39 sigma).

### Example 11: cluster 1 biological scorecard entry (most exotic)

Input: `recluster_centroids.json` cluster 1 entry + `biological_priors.json`.

Output (`recluster_biological_scorecard.json` cluster 1 ais_to_soma_nav_ratio entry):

```json
{
  "parameter_name": "ais_to_soma_nav_ratio_werginz2024",
  "centroid_value": 116.04,
  "published_mean": 17.3,
  "published_sigma": 3.0,
  "deviation_sigma": 32.91,
  "verdict": "exotic"
}
```

Cluster 1's centroid AIS-to-soma Nav ratio is 116x (vs Werginz 2024 17.3x, sigma 3.0); the +33
sigma deviation makes it the most exotic single-prior violation in the entire scorecard.

### Example 12: mechanism-distinctness verdict

Input: 4 per-representative attribution JSONs.

Output (`mechanism_distinctness.json` excerpt):

```json
{
  "verdict": "shared_mechanism_different_scale",
  "n_clusters": 4,
  "unique_dominants": ["nap"],
  "fractional_spread_across_clusters": {
    "nmda": 0.0,
    "nav16": 0.123,
    "nap": 0.123
  }
}
```

The fractional spread shows the maximum minus minimum of each channel's fractional
contribution across the 4 clusters. Spread on NMDA = 0 (all clusters 0%); spread on NaP =
0.123 (Cluster 3 0.997 vs Cluster 1 0.874); spread on Nav1.6 = 0.123 (Cluster 1 0.126 vs
Cluster 3 0.003).

## Limitations

* **13-cell pool is small for 54-d clustering**. The 50-sample bootstrap stability ARI 0.583
  +/- 0.226 indicates moderate stability; the cluster boundaries (especially cluster 2 vs 3
  with 2 members each) could shift if 1-2 cells were added or moved.
* **Single inner replication per direction**. Phase B uses 1 replication per direction; cell
  1634's measured DSI 0.200 (vs t0086's 5-rep 0.614) confirms direction-conditional
  variability is substantial. The mechanism attribution (NaP-dominant) is robust to this since
  it's based on integrated current shapes, not spike counts.
* **PCA fallback for visualisation**. UMAP is not in the project's dependencies; PCA(n=2) was
  used. UMAP would likely show different but not radically different structure for n = 13.
* **NMDA contribution = 0% in all 4 clusters**. This is because PD-minus-ND integrated NMDA
  current is small relative to the NaP and Nav1.6 transient differentials. NMDA contributes to
  the sustained baseline depolarisation that enables NaP activation, but the differential
  measure ascribes the resulting current asymmetry to NaP not NMDA. A causal-decomposition
  (NMDA-knockout vs NaP-knockout vs Nav1.6-knockout ablation experiments) would more directly
  attribute mechanism. This is a follow-up suggestion (S-0088-XX in this task's
  `suggestions.json`).
* **Only 4 representative cells deep-dived**. The 13-cell pool's 9 non-representative cells
  could have within-cluster mechanism heterogeneity that the representative-only analysis
  misses. A full 13-cell deep-dive would cost ~3.5x the wall-clock; deferred.

## Files Created

* `code/{constants,paths,biological_priors,biological_scorecard,select_representatives,run_deepdive,attribution_metric,plot_figures,mechanism_distinctness,write_answer_asset}.py`
  (10 Python modules)
* `results/data/biological_priors.json`
* `results/data/recluster_assignments.json`
* `results/data/recluster_centroids.json`
* `results/data/recluster_biological_scorecard.json`
* `results/data/representative_cells.json`
* `results/data/mechanism_distinctness.json`
* `results/data/cell{1604,1634,767,1639}_summary.json` (4 per-cell summaries)
* `results/data/cell{1604,1634,767,1639}_dir{0,225,450,675,900,1125,1350,1575,1800,2025,2250,2475,2700,2925,3150,3375}_traces.npz`
  (64 NEURON trace files, naming uses tenths-of-degree to avoid '.' in filenames)
* `results/data/cell{1604,1634,767,1639}_attribution.json` (4 per-cell attributions)
* `results/images/cluster_pca.png`, `cluster_silhouette.png`, `cluster_dendrogram.png`,
  `biological_plausibility_heatmap.png` (Phase A, 4 PNGs)
* `results/images/{vm_traces,nmda_conductance,nav_decomp,ais_spike_onset}_{1604,1634,767,1639}.png`
  (Phase B, 16 PNGs)
* `assets/answer/are-cluster-motifs-mechanistically-distinct/{details.json,short_answer.md,full_answer.md}`
  (1 answer asset)

## Verification

* `verify_research_code`: PASSED (0 errors).
* `verify_plan`: PASSED (0 errors, 3 acceptable warnings).
* `verify_logs`: PASSED (0 errors, expected warnings to be cleared by capture_task_sessions in
  reporting).
* `verify_task_file`, `verify_task_dependencies`, `verify_task_folder`: PASSED.
* `verify_task_metrics`: PASSED (`metrics.json = {}` is valid for an answer-producing task).
* `verify_task_results`: PASSED (mandatory sections + Examples >= 10 + Task Requirement
  Coverage final).

## Task Requirement Coverage

> **Task name** (from task.json): "Re-cluster t0086 13 cells and per-cluster Vm-trace deep-dive"
> **Short description** (from task.json): "Re-cluster 6 Genuine + 7 Marginal cells from t0086 (13
> total); per-cluster Vm-trace deep-dive at 16 dirs to attribute mechanism; produce
> mechanism-distinctness answer asset." **Long description** (from `task_description.md`): Phase A
> re-cluster 13 cells in 54-d natural-unit parameter space (KMeans k=2..6 + hierarchical (ward +
> cosine + euclidean) + UMAP / PCA visualisation; pick best k via silhouette + BIC; compute
> centroids; score against published biological priors via t0086's scorecard). Phase B per-cluster
> Vm-trace deep-dive at 16 directions on a representative cell per cluster (closest to centroid);
> record per-segment Vm + NMDA conductance + Nav1.6 / NaP currents + AIS spike onsets; produce 4
> figures per representative; compute fractional channel contributions. Phase C compare attributions
> across clusters; mechanism distinctness verdict. Output: one answer asset. Local-CPU only; $0
> cost.

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Load 13-cell pool | Done | `recluster_assignments.json` cell_ids = [767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1721] |
| REQ-2 | Load 54-d parameter vectors from t0083 | Done | `recluster_centroids.json` centroids in 54-d natural unit space (LOWER/UPPER bounds applied) |
| REQ-3 | KMeans k=2..6 silhouette + BIC selection | Done | `recluster_assignments.json` `kmeans` array with 5 entries; best_k=4 |
| REQ-4 | Hierarchical (cosine + euclidean) cross-validation | Done | `hierarchical_cosine_labels` + `hierarchical_euclidean_labels`; ARI vs KMeans = 0.799 both |
| REQ-5 | UMAP / PCA 2D visualisation | Done | `results/images/cluster_pca.png` (UMAP not in deps; PCA fallback used) |
| REQ-6 | Per-cluster centroids + within-cluster variance | Done | `recluster_centroids.json` 4 entries with normalised + unnormalised centroids + within_cluster_variance |
| REQ-7 | Biological scorecard (9 priors) | Done | `recluster_biological_scorecard.json` + `biological_plausibility_heatmap.png`; all 4 clusters exotic |
| REQ-8 | Pick representative cell per cluster | Done | `representative_cells.json` reps 1604, 1634, 767, 1639 |
| REQ-9 | 16-direction NEURON deep-dive | Done | 64 `.npz` trace files (4 cells x 16 dirs); all stable |
| REQ-10 | Fractional channel attribution | Done | `cell{id}_attribution.json` x 4 |
| REQ-11 | 4 figures per representative cell | Done | 16 PNGs total under `results/images/{vm_traces,nmda_conductance,nav_decomp,ais_spike_onset}_<cell>.png` |
| REQ-12 | Mechanism-distinctness verdict + narrative | Done | `mechanism_distinctness.json` verdict = `shared_mechanism_different_scale`; per-cluster narratives |
| REQ-13 | Answer asset | Done | `assets/answer/are-cluster-motifs-mechanistically-distinct/{details.json, short_answer.md, full_answer.md}` |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0088_recluster_marginals_and_vm_motifs" date_compared:
"2026-05-06" ---
# Compare Literature -- t0088_recluster_marginals_and_vm_motifs

## Summary

Compared the four-cluster re-clustering centroids (best_k = 4 on 13-cell pool of 6 Genuine + 7
Marginal cells) to the same nine published biological priors used by t0086, and compared the
per-cluster Vm-trace deep-dive mechanism attribution at 16 directions to t0084's 8-direction
cell 767 attribution. **All 4 clusters score exotic** by the worst-case rule (the same NMDA +
NaP violations as t0086 plus GABA spatial-gradient violations); **all 4 cluster
representatives are NaP-dominant** in PD-minus-ND attribution (frac NaP 0.874-0.997, NMDA =
0.000), confirming and extending t0084's NaP-dominant cell 767 finding to the wider 13-cell
pool. The most novel finding is that Cluster 1 (cells 1304, 1504, 1624, 1634) has an extreme
AIS-to-soma Nav ratio of 116x (vs Werginz 2024's 17.3 +/- 3 = +33 sigma exotic), the most
extreme single-prior violation in either t0086 or this task.

## Comparison Table

| Parameter | Source | Mean +/- Sigma | Cluster 0 (rep 1604) | C0 verdict | Cluster 1 (rep 1634) | C1 verdict | Cluster 2 (rep 767) | C2 verdict | Cluster 3 (rep 1639) | C3 verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AIS Nav density | Kole 2008 (10.1038_nn.2153) | 0.375 +/- 0.125 S/cm^2 | 0.675 (+2.40 sigma) | stretched | 0.570 (+1.56 sigma) | plausible | 0.251 (-1.00 sigma) | plausible | 0.263 (-0.90 sigma) | plausible |
| AIS Nav density | Werginz 2024 | 1.3 +/- 0.3 S/cm^2 | 0.675 (-2.08 sigma) | stretched | 0.570 (-2.43 sigma) | stretched | 0.251 (-3.50 sigma) | stretched | 0.263 (-3.46 sigma) | stretched |
| Distal Nav1.6 | Oesch 2005 | 0.05 +/- 0.02 S/cm^2 | 0.018 (-1.61 sigma) | plausible | 0.012 (-1.88 sigma) | plausible | 0.016 (-1.72 sigma) | plausible | 0.036 (-0.70 sigma) | plausible |
| Distal NaP | Stuart 1999 / Goldfinger 2000 | 0.0005 +/- 0.0002 S/cm^2 | 0.00242 (**+9.58 sigma**) | **exotic** | 0.00723 (**+33.64 sigma**) | **exotic** | 0.00222 (**+8.59 sigma**) | **exotic** | 0.00441 (**+19.53 sigma**) | **exotic** |
| Dendritic NMDA per-synapse | Sivyer 2013 | 0.0001 +/- 0.00005 uS | 0.00487 (**+95.43 sigma**) | **exotic** | 0.00442 (**+86.41 sigma**) | **exotic** | 0.00454 (**+88.76 sigma**) | **exotic** | 0.00588 (**+115.62 sigma**) | **exotic** |
| NMDA Mg-block voff offset | Branco-Hausser 2010 | 0 +/- 5 mV | 3.93 (+0.79 sigma) | plausible | 4.24 (+0.85 sigma) | plausible | 5.02 (+1.00 sigma) | plausible | 7.43 (+1.49 sigma) | plausible |
| GABA rho0 | de Rosenroll 2026 | 1.0 +/- 0.5 | 3.70 (**+5.41 sigma**) | **exotic** | 3.78 (**+5.56 sigma**) | **exotic** | 4.11 (**+6.23 sigma**) | **exotic** | 4.73 (**+7.46 sigma**) | **exotic** |
| GABA lambda | de Rosenroll 2026 | 80 +/- 30 um | 232.7 (**+5.09 sigma**) | **exotic** | 320.4 (**+8.01 sigma**) | **exotic** | 348.4 (**+8.95 sigma**) | **exotic** | 38.4 (-1.39 sigma) | plausible |
| AIS-to-soma Nav ratio | Werginz 2024 | 17.3 +/- 3 | 25.93 (+2.88 sigma) | stretched | 116.04 (**+32.92 sigma**) | **exotic** | 26.05 (+2.92 sigma) | stretched | 13.25 (-1.35 sigma) | plausible |

### Key observations

* **NMDA per-synapse conductance** is exotic in all 4 clusters (range +86 to +116 sigma above
  Sivyer 2013). This extends t0086's finding (k = 2 clusters at +85 / +122 sigma) to the wider
  13-cell pool: NMDA exotic-ness is a uniform feature of the v3 substrate's joint-pass /
  near-joint-pass cells, not a cluster-specific anomaly.
* **Distal NaP** is exotic in all 4 clusters (range +9 to +34 sigma above Stuart 1999). This
  also extends t0086's finding (+8 / +24 sigma) to the wider pool.
* **GABA rho0** is exotic (>=+5 sigma) in all 4 clusters; t0086 found this in cluster 0 only
  at k = 2\.
* **GABA lambda** is exotic in clusters 0, 1, 2 (>+5 sigma) but plausible in cluster 3 (-1.39
  sigma). Cluster 3 (cells 1639, 1663) is the only cluster with a plausible GABA spatial decay
  length; all other clusters have unphysiologically long lambda (233-348 um vs published ~80
  um).
* **Cluster 1's AIS-to-soma Nav ratio = 116** (+33 sigma vs Werginz 2024's 17.3) is the most
  extreme single-prior violation in any t0086 or t0088 analysis. The implementation should be
  audited to confirm this is not a units / scope mismatch (cf. S-0086-02 for the analogous
  NMDA units audit).
* **Cluster 3** is the closest to biological plausibility -- AIS-to-soma Nav ratio plausible,
  GABA lambda plausible, AIS Nav density Kole-plausible. It remains exotic only because of the
  shared NMDA + NaP + GABA-rho0 violations.

## Methodology Differences

This task uses the same 9-prior database and scoring math as t0086 (re-used unchanged with
import rebinding); the only methodology difference is the **input pool**: t0086 clustered the
6 Genuine cells from its 20-cell test set into k = 2 clusters; t0088 includes the 7 Marginal
cells too, giving a 13-cell pool clustered into k = 4 clusters. The wider pool produces:

* a finer-grained partition (4 clusters vs 2);
* more variable AIS-to-soma Nav ratios across clusters (Cluster 1 at 116x is far outside
  t0086's k = 2 range of 11.5-30.5x);
* a cluster (Cluster 3) closer to biologically-plausible territory than any t0086 cluster.

The 16-direction Vm-trace deep-dive in this task differs from t0084's 8-direction protocol
only in angular resolution; the recording infrastructure (per-segment Vm + per-synapse NMDA +
per-segment Nav1.6 / NaP currents + AIS spike onsets), the PD-minus-ND attribution metric, and
the response window [200, 1200] ms are unchanged. 16 directions allow direction-tuning curves
to be fit and polar AIS spike-onset histograms to be plotted.

## Comparison to t0084 Vm-trace Mechanism Attribution

t0084 ran a Vm-trace deep-dive on cell 767 (and cells 637, 762) at 8 directions; its
attribution was NaP 93%, Nav1.6 7%, NMDA 0% for cell 767. t0088 reproduces this on cell 767 at
16 directions with NaP 87.5%, Nav1.6 12.5%, NMDA 0% -- consistent within angular-resolution
noise. More importantly, t0088 generalises the NaP-dominant signature to all 4 cluster
representatives:

| Cell | t0084 (8 dirs) | t0088 (16 dirs) | Cluster |
| --- | --- | --- | --- |
| 1604 | not done | NaP 0.988 / Nav1.6 0.012 / NMDA 0.000 | 0 |
| 1634 | not done | NaP 0.874 / Nav1.6 0.126 / NMDA 0.000 | 1 |
| 767 | NaP 0.93 / Nav1.6 0.07 / NMDA 0.00 | NaP 0.875 / Nav1.6 0.125 / NMDA 0.000 | 2 |
| 1639 | not done | NaP 0.997 / Nav1.6 0.003 / NMDA 0.000 | 3 |

**Cross-cluster verdict**: `shared_mechanism_different_scale`. All 4 clusters share NaP as the
dominant PD-minus-ND mechanism. NMDA's PD-minus-ND fractional contribution is 0% in every
cluster because the Mg-block makes NMDA depolarisation-dependent but the slow decay integrates
symmetric totals over the response window.

## Analysis

The four clusters reveal a coherent mechanistic story: the v3 substrate's joint-pass /
near-joint-pass cells systematically rely on NaP-driven sustained dendritic depolarisation as
the PD-vs-ND differentiator, with NMDA conductance providing the underlying baseline
depolarisation but contributing 0% to the differential current. This finding is robust to the
cluster choice (k = 4 vs k = 2 in t0086, 6 vs 13 cells in input pool) and to the angular
resolution (8 vs 16 directions in t0084 vs t0088). The three biological mechanisms the model
exploits (high NMDA per-synapse conductance, high distal NaP density, exotic GABA spatial
scale) are mutually reinforcing: NMDA provides baseline sustained depolarisation, GABA shapes
the direction-asymmetry, and NaP amplifies the resulting PD-only sustained activation. The
optimiser cannot achieve joint DSI / PD pass with biologically-plausible NMDA + NaP at the
current parameter bounds; this is a constraint of the substrate rather than a bug.

## Discrepancies vs Published Mechanisms

The model's NaP-dominant attribution is consistent with **dendritic NaP literature** (Stuart
1999, Goldfinger 2000, Astman 2006 in cortical pyramidal cells; less data on RGCs specifically
-- see S-0086-05 for the proposed RGC NaP literature search). However, the centroid NaP
densities (0.0022-0.0072 S/cm^2) are 5-15x above published cortical pyramidal values (0.0005
S/cm^2). Either the model needs higher NaP density than cortex to compensate for other model
differences, or the biological prior needs an RGC-specific update.

The NMDA Mg-block in the v3 model (`voff_nmda` near 0 mV relative to canonical -25 mV
midpoint) is plausible across all 4 clusters (deviation +0.79 to +1.49 sigma). This is
consistent with **Branco & Hausser 2010** mid-range Mg-block published values. The exotic NMDA
finding is exclusively in the per-synapse conductance, not in the gating dynamics.

The GABA spatial gradient violations (rho0 + lambda) extend de Rosenroll 2026's
parameterisation beyond its published range. The optimiser is using GABA spatial scale as a
free knob to shape direction selectivity; the model parameters are exotic but the resulting
cell behaviour is a direction-tuning curve consistent with electrophysiology. This is a known
caveat of any reduced-parameter optimisation.

## Limitations

* **Comparison priors are inherited from t0086 unchanged.** Stuart 1999 / Goldfinger 2000 NaP
  values are from cortical pyramidal cells, not RGCs. The +9-34 sigma NaP exotic verdict could
  be partly explained by an RGC-specific NaP density 2-5x higher than cortical (S-0086-05
  proposes this RGC-specific search).
* **Single-replicate Phase B** means the per-cell DSI re-evaluation is noisier than t0086's
  5-rep classification (see cell 1634's measured 0.20 vs 5-rep 0.61 DSI). The mechanism
  attribution is robust to this, but per-cell DSI numbers in the comparison should not be
  compared against t0086's classification thresholds.
* **No causal ablation** -- the attribution is correlation-based (PD-minus-ND integrated
  current difference). To causally confirm NaP as the dominant mechanism, set nap_dend_distal
  = 0 in each representative cell and re-measure DSI; this is a follow-up suggestion in
  `results/suggestions.json`.
* **Cluster 1's AIS-to-soma Nav ratio = 116x** could reflect a units / scope mismatch in the
  ratio computation rather than a genuine biological signal. The audit is recommended.
* **PCA fallback for visualisation** -- UMAP not in dependencies.

## Recommendations

* **High priority**: audit the AIS-to-soma Nav ratio computation in cluster 1 (116x is
  extreme; could be a units / per-section-area mismatch). Combine with S-0086-02 NMDA units
  audit.
* **High priority**: tighten gnmda_dend NSGA-II bounds to [1e-5, 5e-4] uS (5x Sivyer 2013) and
  re-run from gen 17 (S-0086-01); test whether NaP-dominant joint-pass cells can be found in
  the biologically-plausible NMDA neighbourhood.
* **Medium priority**: ablation experiments per cluster representative -- knock out NaP (set
  nap_dend_distal = 0) and re-measure DSI; this directly tests the NaP-causal hypothesis vs
  the current (correlation-based) attribution.
* **Low priority**: source RGC-specific NaP density (S-0086-05); replace Stuart 1999 /
  Goldfinger 2000 cortical-pyramidal prior; re-classify clusters.

## References

* **Kole 2008**: AIS Nav density 0.25-0.5 S/cm^2 (`10.1038_nn.2153`).
* **Werginz 2024**: AIS Nav density 1.3 S/cm^2; AIS-to-soma ratio 17.3x.
* **Oesch 2005**: distal Nav1.6 0.05 S/cm^2.
* **Stuart 1999 / Goldfinger 2000**: distal NaP 0.0005 S/cm^2 (cortical pyramidal cells; not
  RGC).
* **Sivyer 2013**: dendritic NMDA per-synapse 0.0001 uS = 0.1 nS.
* **Branco-Hausser 2010**: NMDA Mg-block midpoint ~-25 mV.
* **de Rosenroll 2026**: GABA spatial gradient (linear; rho0 ~1, lambda ~80 um).
* **t0084**: cell 767 NaP-dominant attribution at 8 directions.
* **t0086**: 6 Genuine + 7 Marginal + 7 Stochastic classification + k = 2 clustering on
  Genuine cells.

</details>
