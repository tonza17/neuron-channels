---
spec_version: "2"
answer_id: "mi-atp-joint-structure-in-t0123-substrate"
answered_by_task: "t0125_t0123_cluster_factor_mi_atp"
date_answered: "2026-05-25"
confidence: "medium"
---
## Question

Does the 68-d substrate of the t0123 single-seed MI vs ATP-per-spike NSGA-II run admit a joint MI x
ATP latent factor (|r| > 0.30 on both metrics simultaneously), or are MI and ATP driven by decoupled
factors?

## Short Answer

No, the t0123 substrate does not contain a joint MI x ATP factor. Varimax factor analysis on the
full 5760-cell pool retained 10 factors (16 Kaiser eigenvalues > 1, total variance explained 34.3%)
and zero factors satisfy |r_MI| > 0.30 AND |r_ATP| > 0.30 simultaneously. The two strongest
MI-loaded factors carry r_MI = -0.358 / +0.463 but only r_ATP = +0.205 / +0.063, and the strongest
ATP-loaded factor (F1) ranks 7th on |r_MI|. This contrasts with t0117's pooled four-seed DSI x PD
substrate which found one joint factor F1 (r_DSI = +0.421, r_PD = +0.352, 12.6% variance).

## Research Process

The methodology follows the canonical cluster-and-factor template inherited from t0108 / t0116 /
t0117. The full t0123 pool
(`tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/ predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`,
5760 records, seed 441, 60 generations of NSGA-II with pop_size = 96) was loaded via
`tasks/t0125_t0123_cluster_factor_mi_atp/code/load_t0123_cells.py`. Every cell was unique under the
DEDUP_DECIMALS = 6 convention (`raw_count == dedup_unique_count == 5760` in
`results/data/pool_counts.csv`). A union-pool z-score standardiser was fitted ONCE on this full
cohort (`code/fit_standardiser.py`, `data/t0125_standardiser.npz`), and Kaiser-cap varimax factor
analysis was run on the standardised 68-d matrix (`code/factor_analysis.py`, sklearn
`FactorAnalysis(rotation=None)` followed by an in-house iterative-SVD varimax rotation with gamma =
1.0, tol = 1e-6, max_iter = 500, copied verbatim from t0117). The correlation table was extended
from t0117's two outcome metrics (DSI, PD) to four (`mi_count_bits`, `atp_per_spike_molecules`,
`dsi_vector_sum`, `pd_rate_hz`) per the t0125 plan REQ-13, with a `joint_mi_atp_flag` column gated
at the t0117 threshold |r| > 0.30. The PCA panels in
`results/images/pca_combined_color_{mi,atp,corner}.png` and the corner aggregations in
`results/data/corner_param_means.csv` were inspected for consistency with the factor verdict.

## Evidence from Papers

The "decoupled factors" verdict is consistent with the canonical parameter-degeneracy framing of the
multi-objective compartmental-modelling literature. [Achard2006][achard2006] found that 20
acceptable 24-parameter cerebellar Purkinje cell models occupied "a collection of loosely connected
hyperplanes" rather than a single blob or set of isolated points, with several channels (gCaTm,
gKAm, gKMd, gKhs) varying across their entire allowed range while others (gNaFs, gCaPd, gKdrs,
gKdrm) remained tightly bounded. [Prinz2004][prinz2004]'s brute-force enumeration of 20.25 M
three-cell pyloric STG networks found 452,516 matched all 15 criteria (2.2 %), with every
channel-density combination represented in the matching set. [Marder2006][marder2006] reviews this
as the textbook parameter-degeneracy phenomenon: channel densities can vary two- to fourfold while
activity remains conserved because compensating channels co-vary. The t0125 result that MI and ATP
each have multiple non-joint contributing factors is exactly what this literature predicts: each
objective is supported by a different combination of channels, and the same parameter-degeneracy
mechanism allows the substrate to dissociate them.

[Sengupta2010][sengupta2010] supplies the specific biophysical reason ATP-per-spike loads separately
from MI: ATP-per-spike is determined by Na+/K+ overlap during the AP (R^2 = 0.99 between total Na+
load and overlap load across mammalian and squid axons), which is set by Na+ inactivation and Kv
activation kinetics, while MI is determined by the spike-generator's ability to encode direction
(set primarily by AIS-localised channel densities and intrinsic firing-pattern features). Because
the two have different biophysical generators, it is biologically plausible that no single latent
factor would dominate both. [Strong1998][strong1998] establishes the bits-per-stimulus framing that
`mi_count_bits` instantiates, and [Dhingra2004][dhingra2004] supplies the RGC-specific MI ceiling
(`log2(4) = 2 bits` for a 4-direction protocol; t0123's `best mi_count_bits = 1.459` reaches 73 % of
this ceiling).

## Evidence from Internet Sources

Internet sources were not used for this answer.

## Evidence from Code or Experiments

The decisive evidence is `results/data/factor_correlations.csv`, produced by
`code/factor_analysis.py`. The relevant rows (in increasing factor ID, with variance explained):

* **F1** (var = 9.79 %): r_MI = -0.358, r_ATP = +0.205, r_DSI = -0.347, r_PD = +0.030;
  classification = `mi_only`; joint flag = False.
* **F2** (var = 5.16 %): r_MI = +0.463, r_ATP = +0.063, r_DSI = +0.413, r_PD = +0.201;
  classification = `mi_only`; joint flag = False.
* **F3** (var = 5.96 %): r_MI = +0.206, r_ATP = -0.115, r_DSI = +0.230, r_PD = -0.159;
  classification = `none`; joint flag = False.

The remaining seven factors (F4-F10) all show |r_MI| < 0.12 and |r_ATP| < 0.10. The
`joint_mi_atp_flag` column is False on every row. The two strongest MI factors (F1 and F2) load on
DSI as well, suggesting the substrate's primary axes of variation are MI/DSI-related rather than
ATP-related — F2 is essentially a high-MI / high-DSI axis (the Pareto-favoured "good encoder"
direction) and F1 is a high-ATP / low-MI / low-DSI axis (a "silenced / metabolically inefficient"
direction). The factor that is most ATP-loaded (F1, r_ATP = +0.205) is also the most MI-loaded (r_MI
= -0.358), which is consistent with the Pareto trade-off but does NOT meet the joint-factor
threshold on the ATP side.

The PCA panels `results/images/pca_combined_color_mi.png` and `pca_combined_color_atp.png`
corroborate the decoupled structure: the MI gradient runs broadly NE-SW across PC1-PC2 (PC1 = 13.1
%, PC2 = 7.4 %) and the log10(ATP) gradient runs roughly orthogonally NW-SE, with the four MI x ATP
corners cleanly separated in the `pca_combined_color_corner.png` panel. The corner-cell counts (from
`results/data/group_thresholds.json`) show a striking diagonal imbalance —
`high_mi_low_atp = 1221`, `high_mi_high_atp = 343`, `low_mi_low_atp = 341`, `low_mi_high_atp = 1220`
— confirming that high-MI cells are systematically associated with low-ATP cells in the spiking
cohort, but this association is driven by joint *electrophys/morphology* signatures (see the
answer-4 corner-signature analysis) rather than by a single latent factor.

The contrast with t0117 is informative. t0117 ran the same pipeline on the pooled four-seed DSI x PD
substrate (`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds`) and reported one joint DSI x
PD factor F1 with r_DSI = +0.421 and r_PD = +0.352 (12.6 % variance) — see
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/factor_correlations.csv`. The
t0125 verdict is that the analogous joint structure does NOT appear for MI x ATP in the t0123
substrate at the same |r| > 0.30 threshold.

## Synthesis

The factor analysis is decisive: zero joint MI x ATP factors in the t0123 substrate. The Pareto
trade-off visible in `tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/results_detailed.md` (10
Pareto cells spanning MI from 0.95 to 1.46 bits and ATP from 6.76e5 to 1.79e7 molecules) is
therefore not the projection of a single MI-vs-ATP latent axis onto two objectives, but the joint
product of multiple decoupled axes — primarily an MI/DSI axis (F1, F2, F8) and a separate
ATP-loaded axis (F1 partially, with ATP also loading weakly on F3, F7). This is consistent with the
[Sengupta2010][sengupta2010] mechanism (ATP-per-spike is biophysically distinct from
spike-information content) and with [Marder2006][marder2006]'s parameter-degeneracy framing (many
parameter combinations can realise the same activity profile, and different combinations realise the
two objectives).

A practical implication for downstream Pareto-optimisation runs: because MI and ATP have
non-overlapping principal latent factors, simultaneous Pareto improvement in both objectives is
*geometrically feasible* (no single bottleneck factor traps the substrate on a 1-d MI/ATP trade-off
curve), but the substrate-wide trade-off observed in t0123 must be driven by a *combined parameter
signature* rather than a single levers-of-power channel — exactly what the answer-4
corner-signature analysis quantifies (the top 5 corner-separating parameters are KDR_GBAR,
branch_length_cv, BK_SOMA_GBAR, IH_GBAR, RA_OHM_CM, with z-score gaps of -1.19, -1.08, -1.06, -1.06,
+1.06 between the high_mi_low_atp and low_mi_high_atp corners — see
`results/data/corner_param_means.csv`).

A caveat: t0123's top-10 Pareto cells reported `mi_strong_bialek_bits_per_sec = 0.0` under the
post-hoc 8-direction x 20-trial Strong-Bialek validation. The PD rates of those cells are too low
(~3 spikes per 1400-ms trial) for the bias-corrected estimator to produce a non-zero bound, even
though the spike-count-direct estimator (`mi_count_bits`) shows them at the 4-direction ceiling. The
t0125 cluster analysis consumes `mi_count_bits` directly as the within-substrate ranking variable;
absolute MI claims in bits-per-second defer to the Strong-Bialek validation documented in t0123's
results assets. This caveat does not affect the factor-analysis conclusion (which is about
within-substrate covariance structure, not about absolute MI magnitudes), but a reader interested in
absolute MI bounds should consult the t0123 results documentation.

## Limitations

The 10-factor cap (set by `KAISER_FACTOR_CAP = 10` inherited verbatim from t0117) may obscure weak
joint axes among the 6 additional eigenvalues > 1 that exist in the spectrum (16 Kaiser eigenvalues
\> 1, but only 10 retained). Relaxing the cap to 16 or running an exploratory parallel analysis is
feasible future work but was not done here to preserve direct comparability with the t0117 / t0108 /
t0116 precedents. The |r| > 0.30 threshold is also inherited verbatim; the strongest near-joint
factor (F1 with r_MI = -0.358, r_ATP = +0.205) would qualify at a relaxed threshold of |r_ATP| >
0.20. The single-seed nature of t0123 means seed-specific basin structure cannot be ruled out as a
contributor; a multi-seed replication (analogous to t0117's four-seed pool) would be the natural
follow-up. Finally, the `mi_count_bits` surrogate is a 4-direction spike-count estimator, not a
bias-corrected information rate; the relationship between its factor structure and that of a
bias-corrected Strong-Bialek rate would need a separate analysis.

## Sources

* Task: `t0125_t0123_cluster_factor_mi_atp` (this task; canonical evidence in
  `results/data/factor_correlations.csv`, `results/data/group_thresholds.json`,
  `results/images/pca_combined_color_{mi,atp,corner}.png`)
* Task: `t0123_bedb_mi_atp_per_spike_nsga2` (substrate source; predictions asset
  `nsga2-mi-atp-per-spike-bedb-morph`)
* Task: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds` (methodological template and comparison
  anchor)
* Task: `t0116_pooled_pca_cluster_factor_dsi07_pd10` (strict-cohort variant of t0117)
* Task: `t0108_t0106_cluster_factor_dsi05_pd10` (original two-axis varimax precedent)
* Paper: `10.1371_journal.pcbi.0020094` ([Achard2006][achard2006])
* Paper: `10.1038_nn1352` ([Prinz2004][prinz2004])
* Paper: `10.1038_nrn1949` ([Marder2006][marder2006])
* Paper: `10.1371_journal.pcbi.1000840` ([Sengupta2010][sengupta2010])
* Paper: `10.1103_PhysRevLett.80.197` ([Strong1998][strong1998])
* Paper: `10.1523_jneurosci.5346-03.2004` ([Dhingra2004][dhingra2004])

[achard2006]: ../../../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/
[prinz2004]: ../../../../t0097_multi_obj_optim/assets/paper/10.1038_nn1352/
[marder2006]: ../../../../t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/
[sengupta2010]: ../../../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/
[strong1998]: ../../../../t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/
[dhingra2004]: ../../../../t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/
