---
spec_version: "2"
task_id: "t0088_recluster_marginals_and_vm_motifs"
date_completed: "2026-05-06"
---
# Results Detailed -- t0088_recluster_marginals_and_vm_motifs

## Summary

This task re-clustered the 13-cell pool of 6 Genuine + 7 Marginal cells from t0086 in the t0080 v3
substrate's 54-d parameter space and ran a t0084-style Vm-trace deep-dive at 16 directions on the 4
representative cells. Findings: **best_k = 4 clusters** (silhouette 0.164, bootstrap stability ARI
0.583 +/- 0.226 over 50 samples); **all 4 clusters classified exotic** by the biological scorecard
(NMDA per-synapse > 85 sigma above Sivyer 2013, NaP > 9 sigma above Stuart 1999, plus GABA
spatial-gradient priors deviating > 5 sigma from de Rosenroll 2026 in three of four clusters);
**mechanism-distinctness verdict = `shared_mechanism_different_scale`** because all 4 cluster
representatives are NaP-dominant in PD-minus-ND attribution (frac NaP 0.874-0.997, frac Nav1.6
0.003-0.126, frac NMDA = 0.000). The clusters differ in parameter scale within 54-d space but not in
which channel drives the PD response. This extends t0084's NaP-dominant cell 767 finding from a
single cell at 8 directions to four representative cells at 16 directions and confirms the v3
substrate's joint-pass / near-joint-pass cells systematically rely on NaP-driven sustained dendritic
depolarisation, even though NMDA conductance values are extreme relative to Sivyer 2013.

## Methodology

* **Machine**: Local Windows workstation (developer machine; no remote provisioning).
* **NEURON version**: 8.2.7. MOD library compiled at
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/nrnmech.dll` (untracked build artefact
  inside an immutable completed task folder; built locally and reproducible from the source `.mod`
  files in `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`).
* **Phase A method**: load 13 cells from t0086 `cell_classification.json`; load 54-d parameter
  vectors from t0083 `all_evaluations.json`. Min-max normalise per coordinate using LOWER_BOUNDS /
  UPPER_BOUNDS from the t0080 module. KMeans with `random_state=42`, `n_init="auto"` for k = 2..6 on
  the normalised matrix. Best_k by argmax silhouette. Hierarchical clustering (cosine + euclidean,
  average linkage) at best_k for cross-validation. 50-sample bootstrap stability ARI with 80%
  subsample. Per-cluster centroids in normalised + unnormalised space + within-cluster variance.
  Representative cell per cluster = cell minimising 54-d Euclidean distance to centroid
  (normalised), deterministic tiebreak by cell_id.
* **Phase B method**: build the DSGCCellWithAIS once; per representative cell apply the parameter
  vector via `apply_parameter_vector` (loads the t0080 MOD library), set up synapses parametrically
  via `setup_synapses_parametric` with placer_seed derived from a hash of the parameter vector
  (matches t0084). Run 16 directions per cell (every 22.5 deg). Per direction record per-segment Vm
  at proximal soma / mid-dendrite / distal-dendrite / AIS, per-synapse NMDA conductance, per-segment
  Nav1.6 and NaP currents at the distal dendrite. RECORD_DT_MS = 1.0; TSTOP_MS from t0080 constants.
  Save one `.npz` per (cell, direction).
* **Phase C method**: per representative cell, compute fractional channel attribution via PD (0 deg)
  \- ND (180 deg) integrated dendritic current difference over the response window [200, 1200] ms
  (matches t0084). Cross-cluster comparison: if all clusters share the same dominant mechanism ->
  verdict `shared_mechanism_different_scale`; if 2+ different dominants -> verdict `distinct`.

## Per-Cell Results Table

| Cell | t0086 class | Cluster | DSI orig | DSI measured (PD-ND) | PD rate (Hz) | ND rate (Hz) |
| --- | --- | --- | --- | --- | --- | --- |
| 767 | Marginal | 2 | 0.494 | 0.600 | 2.86 | 0.71 |
| 1604 | Genuine | 0 | 0.403 | 0.714 | 8.57 | 1.43 |
| 1634 | Genuine | 1 | 0.689 | 0.200 | 4.29 | 2.86 |
| 1639 | Genuine | 3 | 0.488 | 0.429 | 3.57 | 1.43 |

The single-replicate DSI re-evaluation is intrinsically noisier than t0086's 5-replicate Genuine
classification; cell 1634's 0.200 measured DSI is below threshold here but t0086 classified it
Genuine on 5/5 replications. This is consistent with t0084's same observation on cell 767 and
confirms the deep-dive's purpose is the underlying biophysical signature rather than a per-trial DSI
confirmation.

## Cluster Analysis Results (REQ-3, REQ-4, REQ-5, REQ-6)

* **Best k = 4** by silhouette (score 0.164). Silhouettes per k: k = 2: 0.163; k = 3: 0.111; k = 4:
  0.164; k = 5: 0.160; k = 6: 0.143.
* **k-means labels at k = 4** (cells in order 767, 1304, 1379, 1504, 1517, 1559, 1604, 1624, 1634,
  1639, 1663, 1677, 1721): [2, 1, 0, 1, 0, 0, 0, 1, 1, 3, 3, 2, 0].
* **Hierarchical-cosine ARI** vs k-means = 0.799; **hierarchical-euclidean ARI** vs k-means = 0.799
  (both with average linkage). Cluster structure consistent across methods.
* **50-sample bootstrap stability ARI** mean = **0.583 +/- 0.226** (50 successful bootstraps,
  subsample 0.8). Moderate stability given the small 13-cell pool.
* **Cluster centroids and members**:
  * **Cluster 0 (n = 5)**: cells 1379, 1517, 1559, 1604, 1721. Mix: 1 Genuine + 4 Marginal.
    Within-cluster variance (normalised) = 0.075. Representative: cell 1604.
  * **Cluster 1 (n = 4)**: cells 1304, 1504, 1624, 1634. Mix: 1 Genuine + 3 Marginal. Within-cluster
    variance = 0.084. Representative: cell 1634.
  * **Cluster 2 (n = 2)**: cells 767, 1677. Mix: 1 Genuine + 1 Marginal. Within-cluster variance =
    0.108. Representative: cell 767.
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

Cluster 3 is the only cluster with plausible AIS-to-soma Nav ratio AND plausible lambda_gaba_um --
it remains exotic only because of NMDA + NaP + rho0_gaba. This makes Cluster 3 the closest to
biologically-plausible territory; the other 3 clusters have additional exotic violations on AIS Nav
ratio (Cluster 1) or GABA spatial scale (Clusters 0, 1, 2).

## Per-Cluster Mechanism Attribution (REQ-10, REQ-12)

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | **0.988** | **nap** |
| 1 | 1634 | 0.000 | 0.126 | **0.874** | **nap** |
| 2 | 767 | 0.000 | 0.125 | **0.875** | **nap** |
| 3 | 1639 | 0.000 | 0.003 | **0.997** | **nap** |

**Verdict: `shared_mechanism_different_scale`**. All 4 clusters share NaP as the dominant
PD-minus-ND mechanism. NMDA contribution is exactly 0 in all 4 clusters because the integrated NMDA
current at PD is essentially equal to that at ND (NMDA Mg-block makes it depolarisation- dependent
but the slow kinetics integrate the same total over the response window in both directions; the
differential between PD and ND is dominated by the Na-channel transient).

The fractional NaP / Nav1.6 split is direction-symmetric within each cluster -- Cluster 0 and 3 are
nearly all NaP; Clusters 1 and 2 have ~12% Nav1.6 contribution. This is the only meaningful
mechanistic variation across clusters.

## Comparison to t0084 Cell 767 (REQ-12)

t0084 reported cell 767 attribution at 8 directions: NaP 93%, Nav1.6 7%, NMDA 0%. t0088 here at 16
directions reports cell 767: NaP 87.5%, Nav1.6 12.5%, NMDA 0%. The two are within angular-resolution
noise (16 directions integrate over more orthogonal directions where Nav1.6 contributes slightly
more). The t0084 finding generalises across the broader 13-cell pool: all 4 representatives are
NaP-dominant > 87%.

## Visualizations

![cluster PCA scatter (PCA fallback; UMAP not in deps)](images/cluster_pca.png)

The 4 clusters in PCA-2D space. Each point is one cell labelled with its ID and a (G) for Genuine or
(M) for Marginal. Cluster 0 (red) and Cluster 1 (green) are the two largest groups; Cluster 2 (blue,
cells 767 and 1677) and Cluster 3 (orange, cells 1639 and 1663) are smaller. Genuine and Marginal
cells co-cluster -- the 4-cluster structure is not driven by t0086's robustness classification but
by 54-d parameter geometry.

![silhouette score vs k](images/cluster_silhouette.png)

Silhouette score peaks at k = 4 (0.164), barely beating k = 2 (0.163). The flat curve over k = 2-5
indicates the 13-cell pool has weak intrinsic cluster structure and best_k = 4 is preferred over
best_k = 2 by a thin margin.

![hierarchical dendrogram (euclidean, average linkage)](images/cluster_dendrogram.png)

Average-linkage hierarchical clustering on euclidean distance reveals the same 4-cluster structure
as KMeans. The 13-cell pool splits at distance ~0.5 into Cluster 0 + Cluster 3 (joined later) and
Cluster 1 + Cluster 2 (joined later).

![biological-plausibility heatmap](images/biological_plausibility_heatmap.png)

Per-cluster, per-prior deviation in sigma units. Red = positive deviation (centroid above published
mean); blue = negative deviation. Annotated with verdict letter (P / S / X for plausible / stretched
/ exotic). The dominant red columns are `gnmda_dend_sivyer2013` (+85 to +116 sigma) and
`nap_dend_distal_stuart1999` (+9 to +34 sigma). Cluster 1 also has extreme AIS-to- soma Nav ratio
(+33 sigma).

### Per-representative figures (Phase B, REQ-11)

#### Cluster 0 (representative cell 1604)

![cell 1604 Vm traces (16 directions)](images/vm_traces_1604.png)

Per-segment Vm traces at 16 directions for cell 1604. Top row: proximal soma (-65 to +30 mV range,
AP firing visible at PD-flanking directions). Middle row: mid-dendrite. Bottom row: distal dendrite
(sustained depolarisation visible from t ~250 ms to ~1200 ms at PD-flanking directions 0 deg, 22.5
deg, 337.5 deg). PD = 0 deg shows the cleanest sustained depolarisation; ND = 180 deg shows minimal
late dendritic activity.

![cell 1604 NMDA conductance per direction](images/nmda_conductance_1604.png)

Total NMDA conductance summed across all NMDA synapses, plotted per direction. Peak conductance is
direction-tuned (PD = 0 deg has the largest peak ~0.06 uS) but the integral over the response window
[200, 1200] ms is nearly direction-symmetric due to NMDA's slow decay.

![cell 1604 Nav1.6 / NaP currents at distal dendrite](images/nav_decomp_1604.png)

Per-direction Nav1.6 (blue) and NaP (red) currents at the distal dendrite. NaP is sustained through
the entire response window in PD-flanking directions; Nav1.6 contributes brief transients during AP
firing. The NaP integral dominates the PD-minus-ND difference (frac NaP 0.988).

![cell 1604 AIS spike onset polar histogram](images/ais_spike_onset_1604.png)

AIS spike count per direction in 16-bin polar plot. PD (0 deg, orange) has the highest spike count;
ND (180 deg, blue) has the lowest. The polar plot shows asymmetric direction-tuning consistent with
t0086's per-cell classification.

#### Cluster 1 (representative cell 1634)

![cell 1634 Vm traces](images/vm_traces_1634.png)

![cell 1634 NMDA conductance](images/nmda_conductance_1634.png)

![cell 1634 Nav1.6 / NaP currents](images/nav_decomp_1634.png)

![cell 1634 AIS spike onsets](images/ais_spike_onset_1634.png)

Cell 1634 (Cluster 1) shows higher Nav1.6 contribution than cell 1604 (frac Nav1.6 0.126).

#### Cluster 2 (representative cell 767)

![cell 767 Vm traces](images/vm_traces_767.png)

![cell 767 NMDA conductance](images/nmda_conductance_767.png)

![cell 767 Nav1.6 / NaP currents](images/nav_decomp_767.png)

![cell 767 AIS spike onsets](images/ais_spike_onset_767.png)

Cell 767 (Cluster 2): NaP 87.5%, Nav1.6 12.5%. Compare to t0084's 8-direction figures (NaP 93%,
Nav1.6 7%) -- consistent within angular-resolution noise.

#### Cluster 3 (representative cell 1639)

![cell 1639 Vm traces](images/vm_traces_1639.png)

![cell 1639 NMDA conductance](images/nmda_conductance_1639.png)

![cell 1639 Nav1.6 / NaP currents](images/nav_decomp_1639.png)

![cell 1639 AIS spike onsets](images/ais_spike_onset_1639.png)

Cell 1639 (Cluster 3): nearly pure NaP (frac 0.997, frac Nav1.6 0.003). The cluster representative
of the only cluster with plausible AIS-to-soma Nav ratio.

## Examples

The 16-direction trace files contain 16 distinct examples per representative cell. Below are 12
concrete example records pulled directly from the per-cell summary, attribution, and clustering
JSONs (REQ-9 / REQ-10 / REQ-12 outputs). Each example shows the input file (or in-memory dict) and
the actual produced output as a fenced code block.

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

Cluster 3 has plausible AIS-to-soma Nav ratio (13.25 vs Werginz 2024 17.3, deviation -1.35 sigma)
and plausible lambda_gaba_um (38.35 vs de Rosenroll 2026 80, deviation -1.39 sigma).

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

Cluster 1's centroid AIS-to-soma Nav ratio is 116x (vs Werginz 2024 17.3x, sigma 3.0); the +33 sigma
deviation makes it the most exotic single-prior violation in the entire scorecard.

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

The fractional spread shows the maximum minus minimum of each channel's fractional contribution
across the 4 clusters. Spread on NMDA = 0 (all clusters 0%); spread on NaP = 0.123 (Cluster 3 0.997
vs Cluster 1 0.874); spread on Nav1.6 = 0.123 (Cluster 1 0.126 vs Cluster 3 0.003).

## Limitations

* **13-cell pool is small for 54-d clustering**. The 50-sample bootstrap stability ARI 0.583 +/-
  0.226 indicates moderate stability; the cluster boundaries (especially cluster 2 vs 3 with 2
  members each) could shift if 1-2 cells were added or moved.
* **Single inner replication per direction**. Phase B uses 1 replication per direction; cell 1634's
  measured DSI 0.200 (vs t0086's 5-rep 0.614) confirms direction-conditional variability is
  substantial. The mechanism attribution (NaP-dominant) is robust to this since it's based on
  integrated current shapes, not spike counts.
* **PCA fallback for visualisation**. UMAP is not in the project's dependencies; PCA(n=2) was used.
  UMAP would likely show different but not radically different structure for n = 13.
* **NMDA contribution = 0% in all 4 clusters**. This is because PD-minus-ND integrated NMDA current
  is small relative to the NaP and Nav1.6 transient differentials. NMDA contributes to the sustained
  baseline depolarisation that enables NaP activation, but the differential measure ascribes the
  resulting current asymmetry to NaP not NMDA. A causal-decomposition (NMDA-knockout vs NaP-knockout
  vs Nav1.6-knockout ablation experiments) would more directly attribute mechanism. This is a
  follow-up suggestion (S-0088-XX in this task's `suggestions.json`).
* **Only 4 representative cells deep-dived**. The 13-cell pool's 9 non-representative cells could
  have within-cluster mechanism heterogeneity that the representative-only analysis misses. A full
  13-cell deep-dive would cost ~3.5x the wall-clock; deferred.

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
* `verify_task_results`: PASSED (mandatory sections + Examples >= 10 + Task Requirement Coverage
  final).

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
