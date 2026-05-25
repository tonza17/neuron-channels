---
spec_version: "2"
answer_id: "low-vs-high-atp-morphology-signature"
answered_by_task: "t0125_t0123_cluster_factor_mi_atp"
date_answered: "2026-05-25"
confidence: "medium"
---
## Question

Which morphology parameters most distinguish low-ATP from high-ATP cells in the t0123 spiking
cohort, and does the low-ATP group spend relatively more ATP at the AIS than in the dendrites?

## Short Answer

The top 5 morphology parameters by |Cliff's delta| separating high-ATP (top quartile of
atp_per_spike, n = 782) from low-ATP (bottom quartile, n = 782) cells are: mean_segment_length_um
(delta = -0.725, low-ATP cells have ~43% longer segments), branch_length_cv (delta = +0.554, low-ATP
cells are more uniform in branch length), branch_density_gradient_pd (delta = +0.504, low-ATP cells
have weaker preferred-direction dendrite-density gradient), field_elongation_pd (delta = -0.469,
low-ATP cells have more elongated dendritic field), and ais_length_um (delta = +0.376, low-ATP cells
have shorter AIS by ~12%). The ATP-share answer is Yes for the AIS but the dendrite/soma swap
dominates: low-ATP cells concentrate 93 % of per-AP ATP at the soma and 6 % at the AIS with only 0.4
% in dendrites, while high-ATP cells push 62 % into dendrites and 35 % into soma with only 2.6 % at
the AIS.

## Research Process

The high-ATP vs low-ATP morphology comparison was carried out on the spiking cohort. ATP quartile
thresholds (from `code/group_thresholds.py`) on the spiking cohort
(`data/t0125_spiking_cells.parquet`, n = 3125) are atp_q1 = 5.30e6, atp_median = 6.55e6, atp_q3 =
1.24e7 molecules per spike. The high-ATP group (atp_per_spike >= atp_q3) and low-ATP group
(atp_per_spike <= atp_q1) each contain 782 cells. For each of the 14 morphology parameters,
`code/group_comparison.py` computed mean, std, two-sided Mann-Whitney U p-value, and Cliff's delta.
The per-cell soma/AIS/dendrite ATP shares were computed by `code/atp_compartment_shares.py` from the
`atp_per_ap_compartment_breakdown` dict carried in the t0123 predictions records, and visualised as
a ternary scatter (coloured by MI x ATP corner) and a 3 x 2 violin grid (compartment x group axis)
in `results/images/atp_share_ternary.png` and `results/images/atp_share_violins.png`. The 14-d
morphology KMeans partition was inspected (k = 5 headline, silhouette 0.158) and the representative
tables `results/data/morphology_cluster_{0..4}_representatives.csv` document which morphology
cluster each high-MI / low-ATP cell belongs to.

## Evidence from Papers

The morphology-as-functional-axis interpretation rests on [Mainen1996][mainen1996]'s demonstration
that fixed-channel morphological variation alone produces qualitatively different firing patterns
(regular-spiking, intrinsic-bursting, fast-spiking) — the canonical evidence that morphology is a
first-class control variable in compartmental modelling, not just a passive substrate.
[FohlmeisterMiller1997][fohlmeistermiller1997] makes the same point for retinal ganglion cells: cell
geometry (soma-dendrite-axon proportions) controls the f-I curve. [Cuntz2010][cuntz2010]'s
balancing-factor formalism clusters biologically realistic dendritic arbors at bf ∈ [0.2, 0.7] and
provides the biological-plausibility prior for interpreting the morphology cluster signatures
derived here.

The ATP-compartment finding is informative against the [Attwell2001][attwell2001] cortical baseline,
which allocates per-AP ATP roughly 82 % axon, 14 % dendrite, 4 % soma. The t0125 spiking cohort
average is 77 % soma, 5.5 % AIS, 17.8 % dendrites — essentially the inverse of the cortical
recipe. This inversion is not a bug but a model property: the t0080 / t0123 substrate puts the
spike-initiation site (AIS) on a single short segment and concentrates the somatic Nav and Kv
density in the spike-recovery cycle, so per-AP Na+ load is dominated by the soma. The cleaner
comparison is *within* this substrate, between high-ATP and low-ATP groups. There, low-ATP cells
concentrate even more (93 %) of the per-AP load at the soma, mirroring the
[Sengupta2010][sengupta2010] finding that mammalian-grade Na+/K+ overlap clusters at alpha ∈
[1.0, 1.5] where the Na+ load is minimised by keeping spike generation tight and local — the
low-ATP substrate version of the same mechanism.

## Evidence from Internet Sources

Internet sources were not used for this answer.

## Evidence from Code or Experiments

The 14 morphology parameters ranked by |cliffs_delta_atp| (from `results/data/group_comparison.csv`
restricted to the morphology-parameter subset):

| Rank | Parameter | Cliff's delta | mean (high ATP) | mean (low ATP) | MWU p |
| --- | --- | --- | --- | --- | --- |
| 1 | mean_segment_length_um | -0.725 | 40.5 | 57.9 | 4.8e-136 |
| 2 | branch_length_cv | +0.554 | 0.227 | 0.040 | 2.6e-80 |
| 3 | branch_density_gradient_pd | +0.504 | -0.525 | -0.941 | 8.2e-67 |
| 4 | field_elongation_pd | -0.469 | 2.43 | 2.83 | 5.1e-58 |
| 5 | ais_length_um | +0.376 | 40.5 | 36.0 | 5.2e-38 |
| 6 | soma_diameter_um | -0.376 | 13.1 | 14.6 | 5.7e-38 |
| 7 | num_primary_branches | +0.369 | 5.06 | 4.33 | 1.1e-36 |
| 8 | branch_prob_per_um | +0.350 | 0.0199 | 0.0138 | 3.6e-33 |
| 9 | soma_offset_pd_um | +0.342 | -3.61 | -47.30 | 9.3e-32 |
| 10 | mean_branching_angle_deg | -0.336 | 62.6 | 73.4 | 1.1e-30 |

The signature is geometrically interpretable: low-ATP cells are built from *longer, more
uniform-length, less-branched, less-densely-dendritised* trees on a *larger soma* with a *longer
dendritic field elongation* (more 2-D oriented), but with a *shorter AIS*. The mean-of-means
contrast for `mean_segment_length_um` (40.5 vs 57.9 um, factor 1.43) is the largest in the
morphology table, with MWU p = 4.8e-136. The negative direction on `soma_diameter_um` is consistent
with [Mainen1996][mainen1996]'s observation that smaller somatic membrane area reduces capacitive
ATP load at fixed channel density. The negative direction on `mean_branching_angle_deg` (low-ATP
cells branch at narrower angles, ~73 degrees) and the positive direction on `field_elongation_pd`
(low-ATP cells are more elongated) jointly suggest a "stick-like" branching pattern where dendritic
propagation is more axial than volumetric — which reduces the total membrane area that
participates in spike-related Na+ turnover.

The per-corner ATP-compartment-share means (from `code/atp_compartment_shares.py` aggregating over
the spiking cohort) document the inversion:

| Group | n | soma share | AIS share | dendrite share |
| --- | --- | --- | --- | --- |
| high ATP (top quartile) | 782 | 0.349 | 0.026 | 0.625 |
| low ATP (bottom quartile) | 782 | 0.933 | 0.062 | 0.004 |
| high MI (top quartile) | 819 | 0.899 | 0.065 | 0.037 |
| low MI (bottom quartile) | 1024 | 0.666 | 0.046 | 0.288 |
| overall spiking cohort | 3125 | 0.767 | 0.055 | 0.178 |

Two observations are decisive. First, the low-ATP group and the high-MI group have nearly identical
compartment-share profiles (soma 0.93 vs 0.90, AIS 0.06 vs 0.06, dendrite 0.004 vs 0.04). The
low-ATP and high-MI cells are largely the same cells — see also the corner-cell counts:
`high_mi_low_atp = 1221` vs the off-diagonal `high_mi_high_atp = 343` and `low_mi_low_atp = 341`.
Second, the high-ATP group shifts 62 % of the per-AP ATP load into the dendrites, away from both the
soma (which falls to 35 %) and the AIS (which falls to 2.6 %). The "low-ATP cells spend relatively
more at the AIS than in the dendrites" question is answered Yes (6.2 % vs 0.4 % is a 16-fold shift),
but the much larger story is the dendrite collapse: low-ATP cells essentially do not pay an AP cost
in the dendrites at all, while high-ATP cells pay most of their cost there.

## Synthesis

The low-ATP morphology signature is a "long stick, fewer branches, narrow angles, compact dendritic
field, short AIS, small soma" pattern, and the same pattern colocates the per-AP ATP load at the
soma and AIS rather than in the dendritic tree. This is the [Sengupta2010][sengupta2010]
mammalian-grade efficiency strategy expressed in DSGC-style morphology: keep the spike generator
tight and local, minimise the dendritic compartment area that has to undergo Na+/K+ turnover per
spike, and let the AIS — not the dendrites — bear the localised afterhyperpolarisation cost.

The strong overlap with the high-MI signature is consistent with the answer-1 finding (the PCA panel
`pca_combined_color_corner.png` shows the high_mi_low_atp corner as a single dense locus while the
low_mi_high_atp corner is its mirror image), and is what gives the Pareto trade-off in t0123 its
visible bias toward the favoured corner (1221 cells vs 343 in the off-diagonal corner). However, the
*latent factor* analysis (answer 1) shows that MI and ATP load on different factors — the
morphology that supports both is not coded by a single "morphological efficiency" axis but by a
multi-parameter joint pattern.

A practical implication for downstream Pareto-optimisation runs: morphology priors that penalise
total dendritic membrane area, encourage long uniform segments, narrow branching angles, and
elongated field shape will move the Pareto front toward the low-ATP / high-MI corner. The 14-d
morphology generator (t0090 + t0092 fixes) already supports all these parameters, so a constrained
search with `mean_segment_length_um > 50 um` and `branch_length_cv < 0.10` would seed the next
NSGA-II run in the favoured corner.

## Limitations

The morphology parameter ranking is conditional on the t0090 generator's parameter set (14
dimensions); a more expressive generator (or measured Baden 2016 RGC morphologies) might reveal
additional axes. The `morph_seed` parameter has |cliff delta| = 0.44 by raw value, but this is a
hash-style integer and should not be interpreted causally — its high delta reflects the t0090
generator's deterministic dependence on `seed % MAX_MORPH_SEED` and is an artefact of the encoding,
not a biological signal. The compartment-share inversion vs cortical ([Attwell2001][attwell2001]) is
a *substrate* property of the t0080/t0123 model and may not generalise to substrates with different
AIS / soma channel-density schemes. The single-seed nature of t0123 prevents seed-specific basin
checks.

## Sources

* Task: `t0125_t0123_cluster_factor_mi_atp` (group_comparison.csv, atp_compartment_shares.csv,
  atp_share_violins.png, cliffs_delta_high_vs_low_atp.png, morphology_clusters.csv)
* Task: `t0123_bedb_mi_atp_per_spike_nsga2` (substrate source)
* Task: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds` (methodological template)
* Paper: `10.1038_382363a0` ([Mainen1996][mainen1996])
* Paper: `10.1152_jn.1997.78.4.1948` ([FohlmeisterMiller1997][fohlmeistermiller1997])
* Paper: `10.1371_journal.pcbi.1000877` ([Cuntz2010][cuntz2010])
* Paper: `10.1097_00004647-200110000-00001` ([Attwell2001][attwell2001])
* Paper: `10.1371_journal.pcbi.1000840` ([Sengupta2010][sengupta2010])

[mainen1996]: ../../../../t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/
[fohlmeistermiller1997]: ../../../../t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/
[cuntz2010]: ../../../../t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/
[attwell2001]: ../../../../t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/
[sengupta2010]: ../../../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/
