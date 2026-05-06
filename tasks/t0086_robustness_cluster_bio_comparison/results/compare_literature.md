---
spec_version: "1"
task_id: "t0086_robustness_cluster_bio_comparison"
date_compared: "2026-05-06"
---
# Compare Literature -- t0086_robustness_cluster_bio_comparison

## Summary

Compared the centroids of the two Genuine-cell clusters (k-means best_k=2 on 6 Genuine cells) to
nine published biological priors covering AIS Nav density (`Kole2008`, `Werginz2024`), distal Nav1.6
(`Oesch2005`), distal NaP (`Stuart1999` / `Goldfinger2000`), dendritic NMDA per-synapse conductance
(`Sivyer2013`), NMDA Mg-block voff (`Branco2010`), GABA spatial gradient (`Rosenroll2026`), and
AIS-to-soma Nav ratio (`Werginz2024`). Both clusters score **exotic** by the worst-case
aggregation rule, driven by NMDA per-synapse conductance >85 sigma above Sivyer 2013 in both
clusters and elevated NaP density >7 sigma above Stuart 1999. The AIS Nav densities sit in or near
the Kole 2008 plausible band but well below the Werginz 2024 published value, reflecting the
stretched / exotic dichotomy between the two AIS papers themselves.

## Comparison Table

| Parameter | Source paper | Published mean | Published sigma | t0086 Cluster 0 centroid | Cluster 0 deviation | Cluster 0 verdict | t0086 Cluster 1 centroid | Cluster 1 deviation | Cluster 1 verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AIS Nav density | Kole 2008 (10.1038_nn.2153) | 0.375 S/cm^2 | 0.125 | 0.467 | +0.74 sigma | plausible | 0.255 | -0.96 sigma | plausible |
| AIS Nav density | Werginz 2024 | 1.3 S/cm^2 | 0.3 | 0.467 | -2.78 sigma | stretched | 0.255 | -3.48 sigma | stretched |
| Distal Nav1.6 density | Oesch 2005 | 0.05 S/cm^2 | 0.02 | 0.034 | -0.79 sigma | plausible | 0.022 | -1.40 sigma | plausible |
| Distal NaP density | Stuart 1999 / Goldfinger 2000 | 0.0005 S/cm^2 | 0.0002 | 0.0053 | **+23.89 sigma** | **exotic** | 0.0020 | **+7.44 sigma** | **exotic** |
| Dendritic NMDA conductance (per synapse) | Sivyer 2013 | 0.0001 uS | 0.00005 | 0.0062 | **+122.32 sigma** | **exotic** | 0.0044 | **+85.51 sigma** | **exotic** |
| NMDA Mg-block voff offset | Branco-Hausser 2010 | 0 mV (rel. to canonical -25 mV) | 5.0 | 6.12 | +1.22 sigma | plausible | 4.26 | +0.85 sigma | plausible |
| GABA rho0 (spatial baseline) | de Rosenroll 2026 | 1.0 | 0.5 | 4.64 | **+7.28 sigma** | **exotic** | 3.48 | +4.97 sigma | stretched |
| GABA lambda (spatial decay length) | de Rosenroll 2026 | 80 um | 30 | 141.5 | +2.05 sigma | stretched | 272.8 | **+6.43 sigma** | **exotic** |
| AIS-to-soma Nav ratio | Werginz 2024 | 17.3 | 3.0 | 30.5 | +4.41 sigma | stretched | 11.5 | -1.92 sigma | plausible |

## Methodology Differences

* **Scope of NMDA measurement**: Sivyer 2013's value (0.1 nS = 0.0001 uS) is a **per-spine synaptic
  conductance** measured in voltage-clamp on RGC dendritic spines. The t0086 ParameterVector
  encoding `gnmda_dend` is the **NetCon weight** used in the t0080 Exp2NMDA mechanism inside the
  re-Rosenroll DSGC simulation. These may differ by a per-cell area normalisation or by an effective
  open-channel-fraction factor that the t0080 substrate does not separate. The +85 sigma to +122
  sigma deviation may therefore partially reflect a units / scope mismatch rather than a genuinely
  outlier biological mechanism. Recorded as a follow-up suggestion for an ablation task that maps
  t0080's `gnmda_dend` onto Sivyer 2013's per-spine measurement.
* **NaP density measurement context**: Stuart 1999 / Goldfinger 2000 measured NaP density in
  cortical pyramidal cells, not RGCs; the 0.0005 S/cm^2 prior may be too tight for RGC dendrites
  where NaP could plausibly be 5-10x higher. Even with a 5x relaxed sigma, t0086's +23 sigma Cluster
  0 NaP centroid (0.0053 S/cm^2 vs published 0.0005) would still be exotic; the +7 sigma Cluster 1
  centroid (0.0020) would become stretched.
* **AIS density disagreement between Kole and Werginz**: Kole 2008 reports 0.25-0.5 S/cm^2; Werginz
  2024 reports 1.3 S/cm^2 (~3x higher) for an updated RGC-specific model. Both clusters fall within
  or below the Kole 2008 band but well below Werginz 2024. The t0086 sample is small (6 Genuine
  cells) and may favor the lower Kole-2008-consistent regime simply because the NSGA-II constraint
  `nav16_ais / nav16_soma >= 5` admits a wide range of AIS values; future work could enforce a
  tighter Werginz 2024-consistent prior.
* **GABA spatial parameters**: de Rosenroll 2026 reports the canonical linear gradient with rho0=1.0
  and lambda~80 um. t0086 centroids are 3-5x higher in both rho0 (4.64 / 3.48) and 3-4x higher in
  lambda (141.5 / 272.8). This is consistent with the v3 substrate's parameter bounds being
  deliberately wider than de Rosenroll's nominal values to allow NSGA-II exploration.

## Analysis

The two-cluster partition is robust at the dataset level (k-means + hierarchical-cosine +
hierarchical-euclidean all agree, ARI=1.0; 50-sample bootstrap ARI 0.597). The headline finding is
that **all six Genuine cells share an NMDA-dominant motif**: Cluster 0 NMDA centroid is 62x higher
than Sivyer 2013, Cluster 1 NMDA centroid is 44x higher. This suggests t0080's v3 substrate found
two NMDA-dominant solutions to the joint-pass DSI/PD criterion -- one with elevated AIS Nav (Cluster
0, ratio 30) and one with moderate AIS Nav (Cluster 1, ratio 11.5). Cluster 0 also has elevated NaP,
GABA rho0, and AIS-to-soma ratio -- making it a "high-NMDA + high-NaP + high-AIS" phenotype. Cluster
1 has lower NaP and AIS but elevated GABA lambda (spatial decay length 273 um vs published 80 um) --
making it a "high-NMDA + extended-GABA" phenotype.

Both clusters share the dominant signature of extreme NMDA, which is the strongest deviation across
all 9 priors. This reinforces a recurring finding from t0080 / t0081 / t0083 / t0084: the NSGA-II
search routinely pushes `gnmda_dend` to the upper boundary of its log-uniform [1e-5, 1e-2] uS range,
and Genuine cells inhabit only the high-conductance regime. The t0084 mechanism attribution for cell
767 (NaP-dominant) does NOT generalise to the wider Genuine pool: cell 767 was Marginal in t0086
(3/5 reps pass) and so does not appear in the cluster analysis, while the 6 Genuine cells uniformly
select NMDA over NaP as the dominant mechanism.

The biologically-plausible verdicts (Kole 2008 AIS, Oesch 2005 distal Nav1.6) and
biologically-stretched / exotic verdicts (Sivyer 2013 NMDA, Stuart 1999 NaP) suggest the t0080 v3
substrate is well-calibrated against AIS / Nav1.6 priors but poorly calibrated against NMDA / NaP
priors. The natural follow-up is to tighten the NSGA-II priors on `gnmda_dend` to match Sivyer
2013's published per-synapse value, then re-run the search and see whether any joint-pass cells
emerge in that biologically-plausible regime.

## Limitations

* **Small Genuine pool (n=6)**. The cluster centroids are means of three cells each, so per-cluster
  uncertainty is high. A future task with more Genuine cells would tighten cluster characterisation.
* **NMDA scale uncertainty**. Sivyer 2013's 0.1 nS prior is a per-spine synaptic conductance, while
  the t0080 `gnmda_dend` parameter is the NetCon weight, which may differ by a per-cell-area scaling
  factor. The +85 to +122 sigma exotic verdict is the most extreme and should be re-checked once
  that scaling is resolved. Recorded as a follow-up suggestion.
* **NaP measurement context**. Stuart 1999 and Goldfinger 2000 measured cortical pyramidal cell NaP,
  not RGC NaP. RGC-specific NaP measurements (where available) would shift the prior by several-fold
  and change the Cluster 1 NaP verdict from exotic to stretched.
* **AIS prior conflict**. Kole 2008 (0.25-0.5 S/cm^2) and Werginz 2024 (1.3 S/cm^2) disagree by ~3x.
  t0086 reports both as separate scorecard entries; future work should adjudicate which paper is the
  authoritative source for ON-OFF DSGC AIS density.
* **No t-SNE alternative for 2-D embedding**. Phase B used UMAP (with PCA fallback because
  umap-learn is not in the local venv) only; the plan also called for t-SNE. With n=6 cells t-SNE
  perplexity is constrained to <=5 and provides little additional information beyond UMAP.
