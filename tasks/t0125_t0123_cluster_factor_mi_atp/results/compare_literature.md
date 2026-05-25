---
spec_version: "1"
task_id: "t0125_t0123_cluster_factor_mi_atp"
date_compared: "2026-05-25"
---
# Comparison with Project and Published Results

## Summary

The headline comparison is project-internal: t0117 confirmed F1 as a joint DSI x PD varimax factor
in the unfiltered 4-seed pool (**r_DSI = +0.421**, **r_PD = +0.352**, **12.6 % variance**),
generalising the truncated-cohort artefact to the DSI / PD pair. t0125 ran the same pipeline (PCA +
KMeans + Kaiser-cap varimax FA) on the t0123 MI / ATP-per-spike single-seed pool of 5,760 cells and
**does not** reproduce a joint factor: the largest joint loading is F1 with **r_MI = -0.358** but
only **r_ATP = +0.205**, below the **|r| > 0.30** threshold on the ATP axis (**0 joint factors**
total). The MI / ATP pair therefore behaves opposite to DSI / PD: the truncated-cohort artefact does
**not** generalise — MI and ATP are decoupled at the latent level even in the unfiltered NSGA-II
output. Against published methodology, t0125's headline ephys k = **4** and morphology k = **5** are
an order of magnitude smaller than [Baden2016][baden2016]'s **32** mouse-RGC functional types from a
real ~11,000-cell cohort, and the low ephys silhouette (**0.083**) is consistent with the parameter
degeneracy [Achard2006][achard2006] reports on Purkinje-cell ensembles (20 acceptable models lying
on "loosely connected hyperplanes"). [Niven2007][niven2007]-style bits-per-ATP scaling is not
re-tested here; it is fully covered by [t0123]'s `compare_literature.md` (Insufficient evidence:
post-hoc Strong-Bialek MI = 0 on top-10 Pareto cells).

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0117] (unfiltered 4-seed DSI x PD pool, varimax F1) | r on first objective (DSI) | +0.421 | -0.358 | -0.779 | t0125 F1 loads on MI with magnitude **0.358** vs t0117 F1 on DSI **0.421**. Sign differs; magnitude is similar. Variance fraction not directly comparable (different pool size and objective pair) |
| [t0117] (unfiltered 4-seed DSI x PD pool, varimax F1) | r on second objective (PD vs ATP) | +0.352 | +0.205 | -0.147 | t0125 F1's ATP loading is **+0.205** vs t0117 F1's PD loading **+0.352** — t0125 fails the joint-threshold on the second axis (needs &#124;r&#124; > 0.30) |
| [t0117] (unfiltered pool, joint factor count) | n_joint_factors (&#124;r&#124; > 0.30 on both) | 1 | 0 | -1 | t0117 found exactly one joint DSI-PD factor; t0125 finds **zero** joint MI-ATP factors across all 10 varimax components. **The truncated-cohort artefact does not generalise to MI x ATP** |
| [t0117] (unfiltered pool, electrophys KMeans) | k_headline (mean silhouette) | 4 (0.158) | 4 (0.083) | k +0, silhouette -0.075 | t0125 picks the same k = 4 on the electrophys subspace but at roughly half the silhouette quality. Smaller cohort (3,125 spiking vs 4,431) and lower-dimensional structure both plausible drivers |
| [t0117] (unfiltered pool, morphology KMeans) | k_headline (mean silhouette) | 5 (0.153) | 5 (0.158) | k +0, silhouette +0.005 | Same k = 5 on the morphology subspace and within rounding of t0117's silhouette — morphology subspace clusters more cleanly than the electrophys subspace in **both** tasks |
| [t0123] (NSGA-II MI vs ATP, single seed 441) | n_evaluated_cells | 5760 | 5760 | 0 | t0125 consumes the t0123 predictions asset verbatim; cohort identity is enforced |
| [t0123] (NSGA-II MI vs ATP, top-Pareto MI) | mi_count_bits | 1.459 | 1.459 | 0 | Top-MI cell `(51, 4810)` reproduced exactly; same predictions asset, same MI ceiling at 73 % of log2(4) = 2.0 |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Baden2016][baden2016] (mouse RGC functional fingerprints, Mixture-of-Gaussians + BIC) | n_clusters_total | 32 RGC functional types | 4 (ephys) + 5 (morphology) | -27 to -28 | [Baden2016, Methods, p. 348 + Results, Fig 2]: clustered ~11,000 mouse RGCs into **32 functional types** plus 17 displaced amacrine types. t0125 finds **4** ephys + **5** morphology KMeans clusters in 5,760 simulated cells — roughly an order of magnitude lower diversity than the biological cohort. Direction: simulated DSGCs from a single 68-d substrate are far less heterogeneous than the real mouse RGC population — expected, because the t0123 NSGA-II explores one cell-type-equivalent parameter cube |
| [Baden2016][baden2016] (cluster-count selection criterion) | criterion | BIC (full curve reported, peak at 32) | silhouette (full sweep k in [3, 7] reported, peak at 4 ephys / 5 morph) | n/a | Methodological difference flagged in [Baden2016, Methods, p. 348]: BIC penalises model complexity and is appropriate for the Mixture-of-Gaussians family; silhouette is geometric and appropriate for KMeans. The two criteria can disagree; t0125 reports the full silhouette curves on disk (`electrophys_silhouette.png`, `morphology_silhouette.png`) per Baden's reporting convention |
| [Achard2006][achard2006] (Purkinje 24-parameter ensemble, 20 acceptable models) | manifold shape | "loosely connected hyperplanes" (thin lower-d sub-manifolds; per-channel ranges narrow on 4 of 24 params, full-range on others; grid search would miss ~65 %) | low electrophys silhouette **0.083** + low NMI vs MI quartile **0.178** + low NMI vs ATP quartile **0.186** | n/a | [Achard2006, Discussion]: the high-d parameter landscape of an MOO-acceptable ensemble forms thin sub-manifolds, not blobs — KMeans on such structure produces poorly-separated clusters (low silhouette) yet still captures statistically significant structure (chi-square p < 1e-160 in t0125). t0125's low ephys silhouette is **consistent** with the Achard "hyperplane" picture: clusters carry MI / ATP information but are not pure MI / ATP partitions |
| [Achard2006][achard2006] (per-parameter variability across acceptable models) | n_params_with_full_range | 4 of 24 (full range); 4 of 24 (tightly bounded) | top-5 Cliff's delta for MI: IH_GBAR **-0.79**, CAD_TAUR_MS **-0.72**, KDR_GBAR **-0.67**, SK_AIS_GBAR **+0.63**, SKAHP_TAU_CA_MULTIPLIER **-0.63** | n/a | [Achard2006][achard2006] enumerates 4 / 24 channels varying across the entire allowed range. t0125 reports 5 / 68 parameters with &#124;Cliff's delta&#124; > 0.6 for MI groups (the top-5 listed). Direction: ratio of "strongly discriminating" parameters in t0125 (~7 %) is similar to Achard's "tightly bounded" ratio (~17 %) — both ensembles concentrate the functional axis on a minority of the parameter cube, consistent with [Marder2006][marder2006]'s parameter-degeneracy framing |
| [Attwell2001][attwell2001] (rodent cortical neuron, biophysical accounting) | ATP compartment share (axon, dendrites, soma) | 82 % axon, 14 % dendrites, 4 % soma | 5.5 % AIS, 17.8 % dendrites, 76.7 % soma (spiking cohort means) | -76.5 pp axon / +3.8 pp dendrites / +72.7 pp soma | [Attwell2001, Table 4, p. 1140]: rodent cortical neuron AP energy budget is axon-dominated (82 %). t0125 t0123 cells are **soma-dominated** (76.7 %). The inversion is documented in t0125 `methodology_notes.md` and originally attributed to the t0080 model's lack of explicit myelinated axon and the procedural-AIS construction; the AIS share (5.5 %) is **15x smaller** than Attwell's axon collateral share. This is a model-architecture artefact, not a biological finding |
| [Sengupta2010][sengupta2010] (cross-cell-type ATP per AP, soma vs axon split) | ATP per AP ratio across cell types | 17-fold range across 7 HH models; alpha (Na+/K+ overlap) **1.0-1.5** for mammals | per-cell ATP/spike range in spiking cohort: ATP Q1 / Q3 = **5.30e6** / **1.24e7** (2.3-fold IQR); per-corner mean ATP-share of soma rises to 93 % in low-ATP corner | n/a | [Sengupta2010, Table 1, p. 5]: 17-fold ATP range across seven HH models is the published prior; t0125's 2.3-fold IQR is **narrower**, reflecting that the t0123 NSGA-II explored a single parameter cube rather than seven distinct cell types. The low-ATP corner concentrating to 93 % soma share is **qualitatively** consistent with Sengupta's "Na+/K+ overlap concentrates where Nav density is highest" but quantitatively inverted from Attwell's axon-dominated picture (see row above) |
| [Niven2007][niven2007] (fly photoreceptors, bits-per-ATP Pareto) | bits_per_sec | 200-1000 (4 species) | not re-computed | n/a | Already analysed in `tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/compare_literature.md` (Niven 2007 verdict: **Insufficient evidence** — post-hoc Strong-Bialek MI = 0 bits/s on all 10 top-Pareto cells because PD-rate 1-3 Hz is too low). t0125 does not re-run the bits/s comparison; the cluster-and-factor analysis is on `mi_count_bits` (the inner-loop count-MI surrogate) rather than the bits/s axis |

## Methodology Differences

* **Pool composition (t0117 vs t0125)**: t0117 pooled **4** NSGA-II seeds (9,124 raw cells, 4,431
  dedup-unique) on a DSI x PD-cube objective pair; t0125 used **1** seed (441) on a MI x
  ATP-per-spike pair (5,760 raw, 5,760 dedup-unique). The single-seed design weakens generalisation
  of the joint-factor verdict — a 4-seed MI / ATP replicate is the natural follow-up.

* **Cohort filter (t0117 vs t0125)**: both pipelines fit standardiser / PCA / KMeans / FA on the
  full-cohort union (no filter). t0125 additionally analyses a **spiking** subcohort
  (`pd_rate_hz > 1.0 AND not silence_failed`, n = 3,125) for the ATP-per-spike comparison because
  near-silent cells drive the denominator toward zero. Group comparisons (Cliff's delta, corner
  heatmap, ATP compartment shares) use the spiking subcohort; PCA / FA fits use the full cohort.

* **Joint-factor threshold (t0117 vs t0125)**: both use **|r| > 0.30** on each of the two objectives
  as the joint-factor criterion. The threshold is held constant to make the verdicts directly
  comparable.

* **Cluster-count selection criterion (t0125 vs Baden 2016)**: t0125 uses silhouette on KMeans (k in
  [3, 7]); [Baden2016][baden2016] uses BIC on Mixture-of-Gaussians. Both report the full curve. BIC
  penalises complexity and produced 32 clusters on real cells; silhouette is geometric and produced
  4-5 on simulated cells. The order-of-magnitude difference is partly a criterion mismatch and
  partly a cohort-diversity mismatch — disentangling the two would require re-running BIC on
  t0125's data.

* **Cell type and substrate (t0125 vs Baden 2016)**: [Baden2016][baden2016] clusters ~11,000 mouse
  RGCs experimentally measured by two-photon Ca2+ imaging on functional features (SVD of moving-bar
  responses + chirp + colour + receptive field + soma area + ON/OFF index + DSi + OSi + IHC); t0125
  clusters 5,760 simulated DSGCs on the 68-d Bed B + 14-d morphology parameter vector. The two
  feature spaces are fundamentally different (function vs parameter), so cluster counts cannot be
  directly compared — but the *order-of-magnitude* gap (32 vs 4-5) is informative about the
  diversity ceiling of the t0123 substrate.

* **Parameter-ensemble analysis tool (t0125 vs Achard 2006)**: [Achard2006][achard2006] reports
  per-channel ranges across 20 acceptable Purkinje models; t0125 reports varimax factor loadings,
  Cliff's delta, and KMeans cluster purity on 5,760 t0123 cells. The two analyses are complementary
  — Achard shows what *individual parameters* do; t0125 shows what *factor axes* do. The "loose
  hyperplane" geometry Achard infers from per-channel ranges manifests in t0125 as low silhouette
  (clusters are not blob-like) combined with high chi-square significance (clusters carry real
  information).

* **ATP recipe (t0125 vs Attwell-Laughlin)**: t0125 consumes the per-cell `atp_per_spike_molecules`
  and `atp_per_ap_compartment_breakdown` from t0123 verbatim. The t0080 model lacks an explicit
  myelinated axon, so Attwell's 82 % axon-collateral share has no analogue in the simulation; the
  t0080 AIS is a procedural construct that contributes only 5.5 % of per-AP ATP. The soma-dominated
  share (76.7 %) is consequently a model-architecture artefact, not a contradicting biological
  finding.

* **No published MI / ATP NSGA-II ensemble exists**: [Hay2011][hay2011],
  [Druckmann2007][druckmann2007], [VanGeit2016][vangeit2016], [Achard2006][achard2006] all optimise
  to *electrophysiological-feature* targets, not to information / energy objectives. The closest
  analogue, [Remme2018][remme2018] (MSO coincidence-detector vs energy MOBO), is not present in the
  project paper corpus. t0125 has no direct published factor-analysis precedent for a
  function-vs-energy MOO ensemble; the project-internal t0117 / t0116 / t0108 lineage is the only
  methodological precedent.

## Analysis

### Truncated-cohort artefact does NOT generalise from DSI x PD to MI x ATP

The headline finding is **negative for the joint-driver hypothesis**. t0117 confirmed F1 as a joint
DSI x PD factor in the unfiltered 4-seed pool with **r_DSI = +0.421** and **r_PD = +0.352**, both
crossing the **|r| > 0.30** threshold and together explaining **12.6 %** of the variance, and
explicitly framed this as confirmation of the truncated-cohort artefact (t0116's strict cohort
erased the joint axis). t0125 ran the equivalent pipeline on the t0123 unfiltered pool of 5,760
cells with the same threshold and the same Kaiser-cap = 10 factor budget, and found **zero** joint
MI x ATP factors. The closest candidate F1 loads on MI with **r_MI = -0.358** (above threshold) but
only **r_ATP = +0.205** (below threshold); F2 loads on MI with **r_MI = +0.463** but has **r_ATP =
+0.063**. The factor structure is **decoupled**: one set of latents controls MI, another set
controls ATP, and the diagonal-corner cell-level correlation (**3.6x** imbalance) emerges from
NSGA-II actively exploring the cheap-and-informative half of the cube rather than from a shared
latent driver. The two truncated-cohort experiments together suggest the artefact is
**objective-pair specific**: DSI / PD reveal a joint axis when the silence guard is removed; MI /
ATP do not.

### Cluster diversity is an order of magnitude below the biological RGC cohort

t0125 finds **4** electrophys clusters + **5** morphology clusters (silhouette peaks) in 5,760
simulated cells. [Baden2016, Fig 2] reports **32** RGC functional types + 17 displaced amacrine
types in ~11,000 mouse RGCs measured by two-photon Ca2+ imaging. The order-of-magnitude gap is
consistent with the simulation exploring a single cell-type-equivalent parameter cube (one 68-d Bed
B + 14-d morphology substrate, one set of channel gating kinetics), whereas the biological cohort
spans the full mouse RGC diversity. The morphology silhouette **0.158** (higher than the electrophys
**0.083**) confirms Baden's observation that morphological / functional dimensions separate cell
types more cleanly than purely electrophysiological dimensions. The cluster-count mismatch is a
**cohort-diversity limitation** of the t0123 substrate, not a methodological defect.

### Low silhouette is consistent with Achard's "loose hyperplane" geometry

[Achard2006][achard2006] characterises the 24-parameter Purkinje-cell parameter landscape as "a
collection of loosely connected hyperplanes" — thin lower-dimensional manifolds where 4 of 24
channels vary across the entire allowed range while others are tightly bounded, and a 6 /
10-point-per-dimension grid search misses ~65 % of the acceptable region. t0125's electrophys
silhouette **0.083** is low in absolute terms but the chi-square p-value for ephys-cluster vs
MI-quartile contingency is **1e-236** (highly significant). The combination — low silhouette +
high chi-square — is the signature of hyperplane-like rather than blob-like cluster geometry: the
clusters are real (carry information) but not well-separated (lie on thin sub-manifolds rather than
tight balls). The top-5 Cliff's delta parameters for MI (IH_GBAR **-0.79**, CAD_TAUR_MS **-0.72**,
KDR_GBAR **-0.67**, SK_AIS_GBAR **+0.63**, SKAHP_TAU_CA_MULTIPLIER **-0.63**) act as the
"Achard-style narrow-range" channels — 5 of 68 parameters (~7 %) drive most of the MI variance,
with the remainder distributed broadly. This pattern is what [Marder2006][marder2006]'s
parameter-degeneracy framing predicts: compensating channels co-vary along factor axes, and only a
small subset of channels are functionally constrained at any one operating point.

### ATP compartment-share inversion is a model-architecture artefact

The soma-dominated ATP split (mean **76.7 %** soma, **17.8 %** dendrites, **5.5 %** AIS) is inverted
from [Attwell2001, Table 4]'s axon-dominated rodent cortical breakdown (**82 %** axon collaterals,
**14 %** dendrites, **4 %** soma). The inversion is documented in t0125's `methodology_notes.md` and
is attributed to the t0080 model's lack of an explicit myelinated axon and the procedural
construction of the AIS. [Sengupta2010, Eq 9]'s "Na+/K+ overlap concentrates where Nav density is
highest" predicts the soma will dominate in the t0080 / t0123 substrate because the procedural cells
place most Nav density at the soma. This is the second cross-task finding (after the joint-factor
result above) where t0125 does not reproduce a published / prior pattern in the t0123 substrate, and
in both cases the cause is traceable to a single design choice (NSGA-II objective set in the first
case; cell-architecture choice in the second).

### Why t0123's Niven 2007 comparison is not re-analysed here

[t0123]'s `compare_literature.md` already addresses the [Niven2007][niven2007]-anchored bits-per-ATP
Pareto comparison and concluded **Insufficient evidence**: the post-hoc Strong-Bialek direct-method
MI collapsed to **0.0 bits/s** for all 10 top-Pareto cells because PD firing rates of 1-3 Hz cannot
populate non-trivial spike-time words at word lengths T <= 100 ms. t0125 does not re-run the
comparison because the cluster-and-factor analysis operates on `mi_count_bits` (the inner-loop
count-MI surrogate, ceiling **log2(4) = 2.0 bits**, top cell **1.459 bits**) rather than the bits/s
axis. The Niven comparison remains a missing-paper observation for downstream tasks; t0125's
contribution is the latent-structure verdict (no joint factor), not the Pareto-front placement.

## Limitations

* **Single NSGA-II seed** (seed 441). The joint-factor verdict (zero) could in principle be a
  single-seed accident, in the same way that t0116 (single-seed-equivalent strict cohort) showed
  zero joint DSI-PD factors before t0117 (4-seed unfiltered) found one. The natural follow-up is a
  multi-seed MI / ATP replicate (suggestion-asset candidate for the t0125 reporting stage).

* **Joint-factor threshold sensitivity**. The **|r| > 0.30** threshold is inherited from t0108 /
  t0116 / t0117 for direct comparability, but t0125's F1 has **r_MI = -0.358** + **r_ATP = +0.205**
  — only **0.095** below the ATP threshold. A threshold of **|r| > 0.20** would reclassify F1 as
  joint. The verdict is robust at the literature-comparable **|r| > 0.30** value but should not be
  interpreted as a sharp dichotomy.

* **MI ceiling at 2 bits**. The 4-direction protocol caps `mi_count_bits` at **log2(4) = 2.0**; 73 %
  of the ceiling is reached. Cells near the ceiling have compressed MI variance, which weakens the
  Pearson r of factor scores vs MI and pulls all joint loadings toward zero. An 8-direction or
  16-direction protocol with a higher MI ceiling would re-test the joint-factor verdict at higher
  resolution.

* **No published function-vs-energy MOO factor analysis exists in the corpus**. The closest
  published analogue is [Remme2018][remme2018] (MSO coincidence-detector vs energy MOBO, DOI
  `10.1371/journal.pcbi.1006612`), which is not present as a paper asset. The joint-factor verdict
  cannot be benchmarked against a directly comparable published number; the strongest published
  anchor is [Achard2006][achard2006]'s per-channel-range analysis on a 24-parameter Purkinje
  ensemble, which is a methodological cousin rather than a direct comparator.

* **Baden 2016 cluster count is not directly comparable**. [Baden2016][baden2016]'s 32 RGC
  functional types are derived from real-cell functional fingerprints (SVD of light-driven Ca2+
  responses, chirp, colour, RF, morphology, IHC markers), not from a model-parameter vector. The
  order-of-magnitude gap (32 biological vs 4-5 simulated) is informative about the diversity ceiling
  of the t0123 substrate but should not be interpreted as a methodological deficiency of the t0125
  pipeline.

* **ATP compartment-share inversion**. The 76.7 % soma share vs Attwell's 4 % soma share is a
  model-architecture artefact (t0080 lacks an explicit myelinated axon). The inversion is documented
  and flagged; it does not contradict [Attwell2001][attwell2001] biologically, only computationally.
  A model-correction follow-up adding an explicit axon would resolve this and is a candidate
  suggestion for downstream tasks.

* **Carter-Bean 2009 paper is not in the project corpus**. The strict ATP/AP/cm benchmark was
  flagged as a plan typo in [t0123]'s compare_literature; t0125 inherits the same limitation and
  cannot re-verify against the original paper (DOI `10.1016/j.neuron.2009.12.011`).

[achard2006]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md
[attwell2001]: ../../t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/summary.md
[baden2016]: ../../t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/summary.md
[druckmann2007]: ../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md
[hay2011]: ../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[marder2006]: ../../t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/summary.md
[niven2007]: https://doi.org/10.1242/jeb.005249
[remme2018]: https://doi.org/10.1371/journal.pcbi.1006612
[sengupta2010]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/summary.md
[vangeit2016]: ../../t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/summary.md
[t0117]: ../../t0117_pooled_pca_cluster_factor_all_cells_4_seeds/
[t0123]: ../../t0123_bedb_mi_atp_per_spike_nsga2/
