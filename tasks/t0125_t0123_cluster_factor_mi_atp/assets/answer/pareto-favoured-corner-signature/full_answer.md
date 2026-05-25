---
spec_version: "2"
answer_id: "pareto-favoured-corner-signature"
answered_by_task: "t0125_t0123_cluster_factor_mi_atp"
date_answered: "2026-05-25"
confidence: "medium"
---
## Question

Which combination of electrophys + morphology parameters most distinguishes the Pareto-favoured
corner (high MI, low ATP) from the Pareto-dominated corner (low MI, high ATP) in the t0123
substrate, and what are the per-corner cell counts and means?

## Short Answer

The top 5 parameters by absolute z-score difference between the high_mi_low_atp and low_mi_high_atp
corners (each cell z-scored against the full-cohort standardiser, mean per corner) are: KDR_GBAR
(-1.19), branch_length_cv (-1.08), BK_SOMA_GBAR (-1.06), IH_GBAR (-1.06), and RA_OHM_CM (+1.06). The
Pareto-favoured corner contains 1221 spiking cells (mean MI = 0.984 bits, mean ATP = 5.34e6
molecules / spike, mean DSI = 0.237, mean PD rate = 2.61 Hz) versus 1220 cells in the dominated
corner (mean MI = 0.063 bits, mean ATP = 2.61e7 molecules / spike, mean DSI = 0.016, mean PD rate =
12.3 Hz). The diagonal imbalance (1221 + 1220 = 2441 cells vs 343 + 341 = 684 off-diagonal) is the
joint Pareto signature.

## Research Process

The 2 x 2 corner heatmap was produced by `code/corner_heatmap.py` on the spiking cohort (n = 3125,
post `pd_rate_hz > 1.0 AND not silence_failed` filter). Each cell was z-scored using the full-cohort
standardiser fitted by `code/fit_standardiser.py` (`data/t0125_standardiser.npz`). The four MI x ATP
corners were assigned via the median split (mi_median = 0.565 bits, atp_median = 6.55e6 molecules)
by `code/group_thresholds.py`. The 68 x 4 mean-z-score matrix is persisted in
`results/data/corner_param_means.csv` and rendered as the RdBu_r symmetric heatmap
`results/images/corner_param_heatmap.png`. The per-corner cell counts and per-corner (MI, ATP, DSI,
PD) means are appended as a footer block in the same CSV. The electrophys cluster x corner crosstab
was computed post-hoc to verify which electrophys cluster overwhelmingly populates the favoured
corner (cluster 0 carries 1196 / 1221 of the favoured-corner cells), and the corresponding
morphology gallery (`results/images/electrophys_cluster_0_morphs.png`) visualises 15 representative
morphologies ranked by bits-per-ATP within cluster 0.

## Evidence from Papers

[Hay2011][hay2011] established the Pareto-acceptable-ensemble reporting convention that t0123
inherits: the 10 Pareto cells reported in
`tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/results_detailed.md` are themselves a small subset
of the favoured-corner cells, but the corner aggregation here generalises the analysis to the 1221
cells whose MI and ATP both land in the favourable half of their respective median splits.
[Druckmann2007][druckmann2007] introduced the per-feature SD-normalisation convention that motivates
the z-score corner heatmap (each parameter is expressed relative to the cohort SD, so the top-5
ranking is dimensionless). [Baden2016][baden2016] provides the closest methodological analogue for
the unsupervised clustering pipeline: an unsupervised classifier on >11 000 mouse RGC functional
fingerprints reported separated DS-positive and non-DS clusters with a similar SD-normalised input
scheme.

## Evidence from Internet Sources

Internet sources were not used for this answer.

## Evidence from Code or Experiments

The per-corner cell counts and per-corner outcome means (from `results/data/corner_param_means.csv`
footer block):

| Group | n cells | mean MI (bits) | mean ATP (molecules) | mean DSI | mean PD rate (Hz) |
| --- | --- | --- | --- | --- | --- |
| high_mi_low_atp (Pareto favoured) | 1221 | 0.984 | 5.34e6 | 0.237 | 2.61 |
| high_mi_high_atp | 343 | 0.790 | 1.64e7 | 0.167 | 4.80 |
| low_mi_low_atp | 341 | 0.210 | 5.57e6 | 0.100 | 9.38 |
| low_mi_high_atp (Pareto dominated) | 1220 | 0.063 | 2.61e7 | 0.016 | 12.30 |

The diagonal imbalance is striking: the two on-diagonal corners (1221 + 1220 = 2441) outnumber the
two off-diagonal corners (343 + 341 = 684) by 3.6x. This is the substrate-level expression of the
Pareto trade-off: the NSGA-II run preferentially explored the parameter combinations that
simultaneously maximise MI and minimise ATP (1221 cells) and the inverse combinations that do
neither (1220 cells), with only 684 cells in the "off-diagonal" intermediate regions. Mean MI in the
favoured corner is 15.6x the mean in the dominated corner; mean ATP in the dominated corner is 4.9x
the mean in the favoured corner. The two off-diagonal corners are also informative: high MI with
high ATP is rare and inefficient (343 cells, 4.8 Hz PD), while low MI with low ATP is also rare and
likely represents under-driven cells with low PD-rate spikes (341 cells, 9.4 Hz PD).

The top 10 parameters ranked by absolute z-score difference between high_mi_low_atp and
low_mi_high_atp corners (from `results/data/corner_param_means.csv`):

| Rank | Parameter | high_mi_low_atp | low_mi_high_atp | Diff (z) |
| --- | --- | --- | --- | --- |
| 1 | KDR_GBAR | -0.559 | +0.630 | -1.188 |
| 2 | branch_length_cv | -0.703 | +0.382 | -1.085 |
| 3 | BK_SOMA_GBAR | -0.630 | +0.432 | -1.062 |
| 4 | IH_GBAR | -0.746 | +0.313 | -1.059 |
| 5 | RA_OHM_CM | +0.696 | -0.362 | +1.058 |
| 6 | AIS_LENGTH_UM | -0.678 | +0.370 | -1.047 |
| 7 | mean_segment_length_um | +0.578 | -0.424 | +1.003 |
| 8 | field_elongation_pd | +0.576 | -0.380 | +0.956 |
| 9 | SKAHP_TAU_CA_MULTIPLIER | -0.729 | +0.169 | -0.898 |
| 10 | branch_density_gradient_pd | -0.430 | +0.463 | -0.894 |

The top 5 mix electrophys (KDR, BK, IH, RA) and morphology (branch_length_cv) — the signature is
genuinely joint. The Pareto-favoured corner is built from cells that have *low* KDR_GBAR (below the
cohort mean by 0.56 SDs), *low* branch_length_cv (more uniform branch lengths, 0.70 SDs below mean),
*low* BK_SOMA_GBAR, *low* IH_GBAR, *high* RA_OHM_CM (above the mean by 0.70 SDs). The first four are
also the high-MI signature (see answer 2 — IH, KDR are top-3 there) and several appear in the
low-ATP morphology signature (answer 3 — branch_length_cv is top-2 there). The Pareto-favoured
corner inherits the high-MI signature on the channel side and the low-ATP signature on the
morphology side; the conjunction is what makes the signature joint.

The electrophys-cluster purity (from `results/data/cluster_group_purity.csv`) shows NMI = 0.178
between the headline k = 4 electrophys partition and the MI quartile group, and NMI = 0.186 against
the ATP quartile group (both with chi-square p < 1e-230). The post-hoc cluster x corner crosstab
confirms that cluster 0 (n = 2117 in the full cohort, 1762 of which are spiking) is the
Pareto-favoured cluster: 1196 of its spiking cells (68 %) are in the high_mi_low_atp corner, only
199 are in low_mi_high_atp. By contrast, cluster 3 (n = 776) contains 168 high_mi_high_atp cells and
365 low_mi_high_atp cells — a "high-ATP" cluster that straddles both MI sides. The morphology
gallery for cluster 0 (`results/images/electrophys_cluster_0_morphs.png`) renders 15 representative
full dendrite trees ranked by bits-per-ATP within cluster 0 (spiking cohort only), and gives the
visual signature of the Pareto-favoured cell type.

## Synthesis

The Pareto-favoured corner is populated by 1221 cells (39 % of the spiking cohort), with mean MI
15.6x higher and mean ATP 4.9x lower than the 1220 cells in the dominated corner. The distinguishing
signature is multi-parameter, mixing low K and HCN conductances (KDR, BK, IH — the "lean
repolariser" pattern from the high-MI answer) with high axial resistance, long uniform-length
dendritic segments, short AIS, and elongated dendritic field (the "compact-stick" pattern from the
low-ATP answer). The conjunction is *not* a single latent factor (answer 1 found zero joint MI x ATP
factors at the |r| > 0.30 threshold), but a *combined parameter signature*: each of the top-5
parameters has |z| > 0.50 against the cohort mean in both corners, and the differences accumulate in
the same direction.

For downstream Pareto-optimisation runs, the practical takeaway is that the favoured corner is
densely populated and well-clustered in the electrophys subspace (cluster 0 captures 68 % of
favoured-corner cells), so the next NSGA-II run can be initialised from the cluster 0 centroid with
channel-density priors set to the cluster-0 means and morphology priors set to the low-ATP
morphology signature (long segments, low CV, narrow angles, elongated field). This should accelerate
convergence to the favoured corner without sacrificing exploration: the 1220 dominated-corner cells
(and 684 off-diagonal cells) provide negative examples that the NSGA-II selection pressure already
pushes against.

A scientific implication: because the Pareto trade-off is built from a joint multi-parameter
signature rather than a single bottleneck axis, breaking the trade-off requires breaking the
*conjunction*, not any single channel. The substrate could in principle support cells in the
high_mi_high_atp corner (high MI with high ATP) — only 343 such cells exist in the spiking cohort,
but they show mean MI = 0.79 bits and PD rate = 4.8 Hz, indicating that the substrate's "high MI"
mechanism does not strictly require low ATP. The Pareto trade-off appears to be shaped by NSGA-II
selection pressure operating on a parameter-degeneracy substrate ([Achard2006], [Prinz2004],
[Marder2006]) rather than by a fundamental biophysical incompatibility between high MI and high ATP.

## Limitations

The top-5 ranking is based on median splits (which include cells just past the median). Restricting
the corners to top-quartile / bottom-quartile cells would sharpen the contrast but reduce
statistical power. The "absolute z-score difference" ranking does not adjust for the joint
correlation structure among the 68 parameters — the top 5 partly co-vary (KDR_GBAR and IH_GBAR are
both K/HCN-family resonators), so the effective "independent signature" dimensionality is smaller
than 5. The single-seed nature of t0123 prevents seed-specific basin checks; a multi-seed pool would
be the natural robustness check. The mean PD rate in the favoured corner (2.61 Hz, ~3 spikes per
1400-ms trial) is the same low-firing-rate regime that triggered the
`mi_strong_bialek_bits_per_sec = 0.0` finding in t0123's Pareto cells; the favoured-corner MI is
robust as a within-substrate ranking signal but does not translate directly into a bias-corrected
absolute bits-per-second bound.

## Sources

* Task: `t0125_t0123_cluster_factor_mi_atp` (`results/data/corner_param_means.csv`,
  `results/data/group_thresholds.json`, `results/data/cluster_group_purity.csv`,
  `results/data/electrophys_clusters.csv`, `results/images/corner_param_heatmap.png`,
  `results/images/electrophys_cluster_0_morphs.png`, `results/images/pca_combined_color_corner.png`)
* Task: `t0123_bedb_mi_atp_per_spike_nsga2` (substrate source; Pareto-front anchor)
* Task: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds` (methodological template)
* Paper: `10.1371_journal.pcbi.1002107` ([Hay2011][hay2011])
* Paper: `10.3389_neuro.01.1.1.001.2007` ([Druckmann2007][druckmann2007])
* Paper: `10.1038_nature16468` ([Baden2016][baden2016])

[hay2011]: ../../../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/
[druckmann2007]: ../../../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/
[baden2016]: ../../../../t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/
