---
spec_version: "1"
task_id: "t0088_recluster_marginals_and_vm_motifs"
date_compared: "2026-05-06"
---
# Compare Literature -- t0088_recluster_marginals_and_vm_motifs

## Summary

Compared the four-cluster re-clustering centroids (best_k = 4 on 13-cell pool of 6 Genuine + 7
Marginal cells) to the same nine published biological priors used by t0086, and compared the
per-cluster Vm-trace deep-dive mechanism attribution at 16 directions to t0084's 8-direction cell
767 attribution. **All 4 clusters score exotic** by the worst-case rule (the same NMDA + NaP
violations as t0086 plus GABA spatial-gradient violations); **all 4 cluster representatives are
NaP-dominant** in PD-minus-ND attribution (frac NaP 0.874-0.997, NMDA = 0.000), confirming and
extending t0084's NaP-dominant cell 767 finding to the wider 13-cell pool. The most novel finding is
that Cluster 1 (cells 1304, 1504, 1624, 1634) has an extreme AIS-to-soma Nav ratio of 116x (vs
Werginz 2024's 17.3 +/- 3 = +33 sigma exotic), the most extreme single-prior violation in either
t0086 or this task.

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

* **NMDA per-synapse conductance** is exotic in all 4 clusters (range +86 to +116 sigma above Sivyer
  2013). This extends t0086's finding (k = 2 clusters at +85 / +122 sigma) to the wider 13-cell
  pool: NMDA exotic-ness is a uniform feature of the v3 substrate's joint-pass / near-joint-pass
  cells, not a cluster-specific anomaly.
* **Distal NaP** is exotic in all 4 clusters (range +9 to +34 sigma above Stuart 1999). This also
  extends t0086's finding (+8 / +24 sigma) to the wider pool.
* **GABA rho0** is exotic (>=+5 sigma) in all 4 clusters; t0086 found this in cluster 0 only at k =
  2\.
* **GABA lambda** is exotic in clusters 0, 1, 2 (>+5 sigma) but plausible in cluster 3 (-1.39
  sigma). Cluster 3 (cells 1639, 1663) is the only cluster with a plausible GABA spatial decay
  length; all other clusters have unphysiologically long lambda (233-348 um vs published ~80 um).
* **Cluster 1's AIS-to-soma Nav ratio = 116** (+33 sigma vs Werginz 2024's 17.3) is the most extreme
  single-prior violation in any t0086 or t0088 analysis. The implementation should be audited to
  confirm this is not a units / scope mismatch (cf. S-0086-02 for the analogous NMDA units audit).
* **Cluster 3** is the closest to biological plausibility -- AIS-to-soma Nav ratio plausible, GABA
  lambda plausible, AIS Nav density Kole-plausible. It remains exotic only because of the shared
  NMDA + NaP + GABA-rho0 violations.

## Methodology Differences

This task uses the same 9-prior database and scoring math as t0086 (re-used unchanged with import
rebinding); the only methodology difference is the **input pool**: t0086 clustered the 6 Genuine
cells from its 20-cell test set into k = 2 clusters; t0088 includes the 7 Marginal cells too, giving
a 13-cell pool clustered into k = 4 clusters. The wider pool produces:

* a finer-grained partition (4 clusters vs 2);
* more variable AIS-to-soma Nav ratios across clusters (Cluster 1 at 116x is far outside t0086's k =
  2 range of 11.5-30.5x);
* a cluster (Cluster 3) closer to biologically-plausible territory than any t0086 cluster.

The 16-direction Vm-trace deep-dive in this task differs from t0084's 8-direction protocol only in
angular resolution; the recording infrastructure (per-segment Vm + per-synapse NMDA + per-segment
Nav1.6 / NaP currents + AIS spike onsets), the PD-minus-ND attribution metric, and the response
window [200, 1200] ms are unchanged. 16 directions allow direction-tuning curves to be fit and polar
AIS spike-onset histograms to be plotted.

## Comparison to t0084 Vm-trace Mechanism Attribution

t0084 ran a Vm-trace deep-dive on cell 767 (and cells 637, 762) at 8 directions; its attribution was
NaP 93%, Nav1.6 7%, NMDA 0% for cell 767. t0088 reproduces this on cell 767 at 16 directions with
NaP 87.5%, Nav1.6 12.5%, NMDA 0% -- consistent within angular-resolution noise. More importantly,
t0088 generalises the NaP-dominant signature to all 4 cluster representatives:

| Cell | t0084 (8 dirs) | t0088 (16 dirs) | Cluster |
| --- | --- | --- | --- |
| 1604 | not done | NaP 0.988 / Nav1.6 0.012 / NMDA 0.000 | 0 |
| 1634 | not done | NaP 0.874 / Nav1.6 0.126 / NMDA 0.000 | 1 |
| 767 | NaP 0.93 / Nav1.6 0.07 / NMDA 0.00 | NaP 0.875 / Nav1.6 0.125 / NMDA 0.000 | 2 |
| 1639 | not done | NaP 0.997 / Nav1.6 0.003 / NMDA 0.000 | 3 |

**Cross-cluster verdict**: `shared_mechanism_different_scale`. All 4 clusters share NaP as the
dominant PD-minus-ND mechanism. NMDA's PD-minus-ND fractional contribution is 0% in every cluster
because the Mg-block makes NMDA depolarisation-dependent but the slow decay integrates symmetric
totals over the response window.

## Analysis

The four clusters reveal a coherent mechanistic story: the v3 substrate's joint-pass /
near-joint-pass cells systematically rely on NaP-driven sustained dendritic depolarisation as the
PD-vs-ND differentiator, with NMDA conductance providing the underlying baseline depolarisation but
contributing 0% to the differential current. This finding is robust to the cluster choice (k = 4 vs
k = 2 in t0086, 6 vs 13 cells in input pool) and to the angular resolution (8 vs 16 directions in
t0084 vs t0088). The three biological mechanisms the model exploits (high NMDA per-synapse
conductance, high distal NaP density, exotic GABA spatial scale) are mutually reinforcing: NMDA
provides baseline sustained depolarisation, GABA shapes the direction-asymmetry, and NaP amplifies
the resulting PD-only sustained activation. The optimiser cannot achieve joint DSI / PD pass with
biologically-plausible NMDA + NaP at the current parameter bounds; this is a constraint of the
substrate rather than a bug.

## Discrepancies vs Published Mechanisms

The model's NaP-dominant attribution is consistent with **dendritic NaP literature** (Stuart 1999,
Goldfinger 2000, Astman 2006 in cortical pyramidal cells; less data on RGCs specifically -- see
S-0086-05 for the proposed RGC NaP literature search). However, the centroid NaP densities
(0.0022-0.0072 S/cm^2) are 5-15x above published cortical pyramidal values (0.0005 S/cm^2). Either
the model needs higher NaP density than cortex to compensate for other model differences, or the
biological prior needs an RGC-specific update.

The NMDA Mg-block in the v3 model (`voff_nmda` near 0 mV relative to canonical -25 mV midpoint) is
plausible across all 4 clusters (deviation +0.79 to +1.49 sigma). This is consistent with **Branco &
Hausser 2010** mid-range Mg-block published values. The exotic NMDA finding is exclusively in the
per-synapse conductance, not in the gating dynamics.

The GABA spatial gradient violations (rho0 + lambda) extend de Rosenroll 2026's parameterisation
beyond its published range. The optimiser is using GABA spatial scale as a free knob to shape
direction selectivity; the model parameters are exotic but the resulting cell behaviour is a
direction-tuning curve consistent with electrophysiology. This is a known caveat of any
reduced-parameter optimisation.

## Limitations

* **Comparison priors are inherited from t0086 unchanged.** Stuart 1999 / Goldfinger 2000 NaP values
  are from cortical pyramidal cells, not RGCs. The +9-34 sigma NaP exotic verdict could be partly
  explained by an RGC-specific NaP density 2-5x higher than cortical (S-0086-05 proposes this
  RGC-specific search).
* **Single-replicate Phase B** means the per-cell DSI re-evaluation is noisier than t0086's 5-rep
  classification (see cell 1634's measured 0.20 vs 5-rep 0.61 DSI). The mechanism attribution is
  robust to this, but per-cell DSI numbers in the comparison should not be compared against t0086's
  classification thresholds.
* **No causal ablation** -- the attribution is correlation-based (PD-minus-ND integrated current
  difference). To causally confirm NaP as the dominant mechanism, set nap_dend_distal = 0 in each
  representative cell and re-measure DSI; this is a follow-up suggestion in
  `results/suggestions.json`.
* **Cluster 1's AIS-to-soma Nav ratio = 116x** could reflect a units / scope mismatch in the ratio
  computation rather than a genuine biological signal. The audit is recommended.
* **PCA fallback for visualisation** -- UMAP not in dependencies.

## Recommendations

* **High priority**: audit the AIS-to-soma Nav ratio computation in cluster 1 (116x is extreme;
  could be a units / per-section-area mismatch). Combine with S-0086-02 NMDA units audit.
* **High priority**: tighten gnmda_dend NSGA-II bounds to [1e-5, 5e-4] uS (5x Sivyer 2013) and
  re-run from gen 17 (S-0086-01); test whether NaP-dominant joint-pass cells can be found in the
  biologically-plausible NMDA neighbourhood.
* **Medium priority**: ablation experiments per cluster representative -- knock out NaP (set
  nap_dend_distal = 0) and re-measure DSI; this directly tests the NaP-causal hypothesis vs the
  current (correlation-based) attribution.
* **Low priority**: source RGC-specific NaP density (S-0086-05); replace Stuart 1999 / Goldfinger
  2000 cortical-pyramidal prior; re-classify clusters.

## References

* **Kole 2008**: AIS Nav density 0.25-0.5 S/cm^2 (`10.1038_nn.2153`).
* **Werginz 2024**: AIS Nav density 1.3 S/cm^2; AIS-to-soma ratio 17.3x.
* **Oesch 2005**: distal Nav1.6 0.05 S/cm^2.
* **Stuart 1999 / Goldfinger 2000**: distal NaP 0.0005 S/cm^2 (cortical pyramidal cells; not RGC).
* **Sivyer 2013**: dendritic NMDA per-synapse 0.0001 uS = 0.1 nS.
* **Branco-Hausser 2010**: NMDA Mg-block midpoint ~-25 mV.
* **de Rosenroll 2026**: GABA spatial gradient (linear; rho0 ~1, lambda ~80 um).
* **t0084**: cell 767 NaP-dominant attribution at 8 directions.
* **t0086**: 6 Genuine + 7 Marginal + 7 Stochastic classification + k = 2 clustering on Genuine
  cells.
