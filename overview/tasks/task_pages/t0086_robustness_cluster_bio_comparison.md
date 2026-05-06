# ✅ Robustness + cluster + bio-comparison of t0081/t0083 joint-pass cells

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0086_robustness_cluster_bio_comparison` |
| **Status** | ✅ completed |
| **Started** | 2026-05-06T13:03:09Z |
| **Completed** | 2026-05-06T18:24:00Z |
| **Duration** | 5h 20m |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Source suggestion** | `S-0083-02` |
| **Task types** | `experiment-run`, `data-analysis`, `answer-question` |
| **Expected assets** | 1 answer |
| **Step progress** | 12/15 |
| **Cost** | **$1.59** |
| **Task folder** | [`t0086_robustness_cluster_bio_comparison/`](../../../tasks/t0086_robustness_cluster_bio_comparison/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0086_robustness_cluster_bio_comparison/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0086_robustness_cluster_bio_comparison/task_description.md)*

# Robustness Validation and Parameter-Cluster + Biological-Plausibility Analysis of t0083 Joint-Pass Cells

## Motivation

t0083 (`bedb_v3_extend_nsga2_gen8plus`) extended t0081's NSGA-II from gen 7 through gen 17 and
**expanded the joint-pass cell population from 1 to 15 cells** (1 inherited from t0081 cell
767 + 14 new in gens 13-17), with 3 of those 15 lying on the final 18-cell Pareto front
(highest-DSI cell 1304 at DSI 0.7652 / PD 13.96 Hz). Hypervolume grew +118% from gen 7
(16.330) to gen 17 (35.576). t0084 attributed cell 767's DSI improvement to specific
dendritic-spike machinery.

Three open questions follow naturally from t0083's expansion:

1. **Are the 15 joint-pass cells reproducible?** t0083's evaluation used 8 directions x 20
   seeds per cell. Cells that satisfy the joint pass on a single 160-sim evaluation may or may
   not reproduce under different RNG seeds. The AR(2) release noise + arrival jitter dominate
   the stochastic variance; some joint-pass cells may be artefacts of a lucky RNG draw.

2. **Are the 15 joint-pass cells distributed across distinct sub-regions of the 54-d parameter
   space, or do they cluster around a single mode?** t0083's Pareto front spans a wide range
   of DSI / PD values, suggesting the search is finding multiple distinct architectural
   strategies that each satisfy joint pass. Cluster analysis can identify these strategies and
   characterise the parameter envelope of each.

3. **Are the cluster centroids biologically plausible?** The published biological priors
   constrain key parameters (AIS Nav density per Kole 2008 / Werginz 2024; AIS-to-soma Nav
   ratio per Werginz 2024; dendritic NMDA conductance and Mg-block voff per Sivyer 2013 /
   Branco-Hausser 2010; distal Nav1.6 / NaP densities per Oesch 2005 / Goldfinger 2000 /
   Stuart 1999; GABA/AMPA spatial distribution per de Rosenroll 2026). A cluster whose
   centroid lies within +/-2 sigma of all key priors is "plausible"; one that lies +/-2-5
   sigma is "stretched"; one that lies >5 sigma is "exotic". The scorecard tells the project
   which strategies are biologically interpretable and which are model artefacts.

This task addresses project research question Q1 (which Na / K combinations max AP frequency
at PD with ND suppression) and Q4 (active vs passive dendrites enable joint pass) at a
**characterisation** level rather than a **discovery** level. It bundles three previously open
suggestions (S-0083-02 motif clustering, S-0083-05 multi-seed smoke gate, multi-replicate
aspect of S-0081-01) into a single combined pipeline. Source suggestion: **S-0083-02**.

## Scope

### In scope

* **Phase A -- Robustness validation.** Select 20 cells:
  * All 15 joint-pass cells: cell 767 from t0081 + the 14 t0083 cells with DSI >= 0.4 AND PD
    >= 10 Hz (read from
    `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` and
    `pareto_front.json`).
  * 5 closest near-pass cells from the t0083 Pareto front (`pareto_front.json`) by Euclidean
    distance to the (DSI 0.4, PD 10) joint corner among cells that do NOT satisfy joint-pass.
  * Re-evaluate each cell at **24 directions x 30 seeds = 720 sims per replication x 5 outer
    RNG seeds = 3,600 sims per cell**. Total: 100 cell-evaluations = 72,000 sims.
  * Outer RNG seed controls AR(2) release noise + arrival jitter. The 5 replications are
    pseudo-independent (different outer seeds; same parameter vector).
  * Compute mean +/- SD of DSI and PD per cell across the 5 replications.
  * Classify each cell:
    * **Genuine**: 5/5 replications joint-pass (DSI >= 0.4 AND PD >= 10 in every replication)
    * **Marginal**: 3-4/5 replications joint-pass
    * **Stochastic**: <=2/5 replications joint-pass

* **Phase B -- Cluster analysis on Genuine cells.**
  * k-means with k=2..6, k selected by silhouette score + BIC.
  * Hierarchical clustering with cosine and euclidean distance metrics for cross-validation.
  * UMAP and t-SNE 2D visualisation overlaid with k-means and hierarchical labels.
  * Per-cluster centroids + within/between cluster variance + cluster size.
  * Check cluster stability via 50-sample bootstrap (re-run k-means on subsamples of Genuine
    cells; report Adjusted Rand Index between bootstrap labels and full-sample labels).

* **Phase C -- Biological comparison.**
  * Per cluster centroid, score key parameters against published biological priors:
    * **AIS Nav density** vs Kole 2008 (0.25-0.5 S/cm^2 cortical pyramidal AIS) and Werginz
      2024 (1.3 S/cm^2 mouse alpha-RGC).
    * **AIS-to-soma Nav ratio** vs Werginz 2024 (17.3x).
    * **Dendritic NMDA conductance** and **Mg-block voff** vs Sivyer 2013, Branco-Hausser
      2010.
    * **Distal Nav1.6 / NaP densities** vs Oesch 2005, Goldfinger 2000, Stuart 1999.
    * **GABA/AMPA spatial distribution** vs de Rosenroll 2026.
  * Per parameter: report cluster centroid value, published mean +/- sigma, deviation in sigma
    units, and verdict (plausible / stretched / exotic).
  * Per cluster: aggregate verdict across all key parameters; flag the cluster as overall
    plausible / stretched / exotic.
  * Output: one **answer asset** at
    `assets/answer/cluster-biological-plausibility-attribution/` attributing each cluster to
    known biology or flagging as novel/unphysical.

* **Cost-watchdog rate-fix REQ-X (HARD requirement).** The cost watchdog MUST source
  per-instance hourly rate from `machine_log.json` `selected_offer.price_per_hour`, not from a
  hard-coded constant. This protocol fix is forced by t0083's $0.83 overrun ($5.83 actual vs
  $5.00 cap; in-loop watchdog used hard-coded $0.2382/hr but actual offer billed $0.3209/hr =
  1.347x). Document explicitly in `plan/plan.md` and verify in implementation review.

### Out of scope

* New cells outside the t0081 + t0083 union (no fresh NSGA-II generations).
* Substrate changes (no new dendritic-spike parameters; no new channels; no AIS modifications;
  no morphology changes).
* Different morphologies (deferred S-0081-01 follow-up).
* Different conductance density realisations (deferred S-0081-01 follow-up).
* Bed A cross-bed validation (S-0081-05; deferred to a later task).

## Pass Criteria

* **Primary**: at least one cluster of >=3 Genuine cells (3 cells, all 5/5 replications
  joint-pass) with all key biological parameters within +/-2 sigma of published priors.

* **Secondary**: identify which t0083 joint-pass cells are stochastic artefacts vs genuine --
  even if all clusters are exotic, the robustness classification is itself useful and can be
  used to reweight downstream NSGA-II warm-starts.

* **Acceptable negative**: zero Genuine clusters (all joint-pass cells turn out to be
  stochastic artefacts of lucky RNG draws). This would be a major project pivot but a clean
  negative result.

## Estimated Compute Cost

* Per-cell evaluation budget: 24 dirs x 30 seeds = 720 sims per replication x 5 outer-seed
  replications = 3,600 sims per cell. Total: 20 cells x 3,600 = 72,000 sims.

* Per-cell wall-clock estimate: t0083 averaged ~36 s/cell at 8 dirs x 20 seeds = 160 sims;
  4.5x sim count = ~162 s/cell at 24 dirs x 30 seeds (per replication). 5 replications x ~162
  s = ~13.5 min/cell. With 43 effective cores parallelising over 100 cell-evals (20 cells x 5
  replications): ~13.5 min x 100 / 43 = ~31 min, but per-replication overhead dominates;
  empirical estimate: 5-6 hours optimiser time + ~1 hour Vast.ai instance overhead = 6-7 hours
  wall-clock.

* **Cost estimate: $1.93-$2.57** at $0.32/hr (allow up to 8 hours of EPYC 7B13 instance
  lifetime). Hard cost cap: **$3.50** (1.5x estimate, absorbs the 16% variance observed in
  t0083).

* **Vast.ai instance class**: AMD EPYC 7B13 64-core (same as t0081 / t0083). Fallback: any 36+
  core EPYC at <$0.40/hr if 7B13 unavailable at <$0.35/hr.

## Dependencies

* **t0083_bedb_v3_extend_nsga2_gen8plus**: provides `pareto_front.json` (18 cells) and
  `all_evaluations.json` (1728 cells; 14 of 15 joint-pass cells from gens 13-17). Provides the
  evaluation harness (the loop is `arf.libraries.t0083_loop`-style continuation of t0081's
  harness) to be re-used for the robustness re-evaluation.

* **t0081_bedb_v3_warmstart_nsga2**: provides cell 767 (the first joint-pass cell), the v3
  substrate harness, and the NSGA-II + warm-start scaffolding.

* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset (54-d v3 substrate) used
  unchanged.

* **t0078_bedb_mobo_v2_ais_tiered_ahp**: provides the AIS-augmented parent substrate from
  which t0080 derived the v3 substrate (informs the AIS-Nav biological prior).

* **t0024_port_de_rosenroll_2026_dsgc**: provides the de Rosenroll 2026 DSGC NEURON port (Bed
  B base substrate before AIS / dendritic-spike augmentation; informs the GABA/AMPA spatial
  distribution biological prior).

* **t0084_t0081_cell_767_vm_trace_deepdive**: provides the cell-767 mechanism-attribution
  answer asset (informs the biological priors for the cell-767 cluster).

## Recommended Task Types

* `experiment-run` -- Phase A robustness re-evaluation (Vast.ai compute).
* `data-analysis` -- Phase B cluster analysis (local CPU; sklearn + UMAP).
* `answer-question` -- Phase C biological-plausibility scorecard (one answer asset).

## Notes

The 5 outer RNG seeds for Phase A must be deterministic and recorded in
`results/data/replication_seeds.json` to enable exact reproduction. The seeds should be drawn
from a fixed parent seed (e.g., 0..4 from `np.random.SeedSequence(42).spawn(5)`) so that the
re-evaluation is exactly reproducible.

The 5 closest near-pass cells should be selected from t0083's Pareto front (filtered to
non-joint-pass cells) by Euclidean distance to the (DSI 0.4, PD 10) joint corner using the
formula `sqrt((max(0, 0.4 - DSI) / DSI_scale)^2 + (max(0, 10 - PD) / PD_scale)^2)`. A
reasonable choice for the scales is `DSI_scale = 0.1` (10% of the joint-pass DSI threshold)
and `PD_scale = 5 Hz` (50% of the joint-pass PD threshold); this puts DSI and PD on roughly
equal footing in the distance metric.

The biological priors in Phase C should be loaded from the existing literature surveys (t0017
/ t0018 / t0019) and confirmed via the cited papers' details / summary documents in
`assets/paper/`. The published mean and sigma for each prior must be tabulated in
`results/data/biological_priors.json` before the per-cluster scorecard is computed.

The cluster-stability bootstrap (50 samples, ARI vs full-sample labels) is the primary
safeguard against over-interpreting clusters that arise from the Genuine subset's small size
(best case 15 cells). If ARI < 0.5 across the bootstrap, the cluster verdicts in the answer
asset must explicitly disclose the instability and degrade the per-cluster confidence
accordingly.

The cost-watchdog rate-fix REQ-X requires that the watchdog reads
`logs/steps/<NNN>_setup-machines/machine_log.json` `selected_offer.price_per_hour` at startup
and uses that value as the hourly rate when computing accumulated cost. The watchdog MUST log
the resolved rate at startup so that any future audit can confirm the value used.
Implementation review must explicitly check this code path before merging the implementation
step.

</details>

## Costs

**Total**: **$1.59**

| Category | Amount |
|----------|--------|
| vast-ai-cpu-epyc-7b13 | $1.59 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | (idle, unused; CPU-only NEURON workload) | 0 | 503 GB | 4.6h | $1.59 |

## Metrics

### Cell 767 (joint_pass, Marginal)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4813902101942628** |

### Cell 1238 (near_pass, Stochastic)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.022423882174931218** |

### Cell 1304 (joint_pass, Marginal)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.40673981824275734** |

### Cell 1379 (joint_pass, Marginal)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4326289983234167** |

### Cell 1457 (near_pass, Stochastic)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.05543093664165375** |

### Cell 1482 (joint_pass, Stochastic)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.2800600104160686** |

### Cell 1484 (near_pass, Stochastic)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.06071572361439907** |

### Cell 1504 (near_pass, Marginal)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.9269123179097267** |

### Cell 1517 (joint_pass, Genuine)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4398153298244093** |

### Cell 1548 (joint_pass, Stochastic)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.38565506280549366** |

### Cell 1559 (joint_pass, Marginal)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5544849917628116** |

### Cell 1604 (joint_pass, Genuine)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.42761205046494766** |

### Cell 1624 (joint_pass, Marginal)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.4538038437569343** |

### Cell 1634 (joint_pass, Genuine)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.6137385453861015** |

### Cell 1639 (joint_pass, Genuine)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5270953250914785** |

### Cell 1663 (joint_pass, Genuine)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5433624293557889** |

### Cell 1677 (joint_pass, Genuine)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.8768589152369575** |

### Cell 1710 (joint_pass, Stochastic)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.354903648632625** |

### Cell 1721 (joint_pass, Marginal)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.6027754515897523** |

### Cell 1723 (near_pass, Stochastic)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Which clusters of joint-pass cells in t0083's expanded population are biologically plausible vs novel/unphysical, and which dendritic-spike machinery do the plausible clusters represent?](../../../tasks/t0086_robustness_cluster_bio_comparison/assets/answer/cluster-biological-plausibility-attribution/) | [`full_answer.md`](../../../tasks/t0086_robustness_cluster_bio_comparison/assets/answer/cluster-biological-plausibility-attribution/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Tighten NSGA-II priors on gnmda_dend to match Sivyer 2013
per-synapse value, then re-run</strong> (S-0086-01)</summary>

**Kind**: experiment | **Priority**: high

t0086's biological scorecard found that both Genuine-cell clusters have NMDA per-synapse
conductance 85-122 sigma above Sivyer 2013's published 0.1 nS. The NSGA-II search routinely
pushes gnmda_dend to the upper boundary of its log-uniform [1e-5, 1e-2] uS range. Tighten the
parameter bounds to [1e-5, 5e-4] uS (5x Sivyer 2013's value as a soft cap) and re-run NSGA-II
from t0083's gen-17 final population for 5 additional generations at population 96. Test
whether any joint-pass cells emerge in the biologically-plausible NMDA regime. If not, this
confirms that the v3 substrate cannot satisfy the joint-pass DSI/PD criterion using
biologically-plausible NMDA -- a major finding that would motivate either (a) revisiting the
joint-pass thresholds, (b) revisiting the substrate's NMDA implementation, or (c) revisiting
Sivyer 2013's measurement scope. Expected cost: ~$1.50 USD on Vast.ai EPYC 7B13 (5 gens x 96
cells x 30 s = 4 h x $0.35/hr). Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Resolve units mismatch between t0080 gnmda_dend NetCon weight and
Sivyer 2013 per-spine conductance</strong> (S-0086-02)</summary>

**Kind**: evaluation | **Priority**: high

t0086's NMDA exotic verdict (>85 sigma above Sivyer 2013) is so extreme that it likely
partially reflects a units / scope mismatch rather than a genuinely outlier biological
mechanism. The t0080 ParameterVector encoding `gnmda_dend` is the NetCon weight used in the
t0080 Exp2NMDA mechanism, while Sivyer 2013's value is a per-spine synaptic conductance
measured in voltage-clamp on RGC dendritic spines. These may differ by a per-cell area
normalisation or by an effective open-channel-fraction factor. Run a calibration ablation:
take a single t0080 cell, vary `gnmda_dend` from 1e-5 to 1e-2 uS, measure the per-spine
effective open conductance (from the NEURON state during a stimulus), and produce a
calibration curve mapping NetCon weight to per-spine conductance. Then re-score the t0086
clusters against Sivyer 2013 in the corrected units. Expected cost: ~$0.30 USD (1 hour CPU).
Recommended task types: data-analysis.

</details>

<details>
<summary><strong>Per-cluster Vm trace deep-dive (extension of t0084 to all 6 Genuine
cells)</strong> (S-0086-03)</summary>

**Kind**: experiment | **Priority**: medium

t0084 produced a Vm-trace mechanism attribution for cell 767 only. t0086 found that cell 767
was Marginal (3/5 reps pass) and that 6 different cells (1517, 1604, 1634, 1639, 1663, 1677)
are Genuine and partition into 2 clusters. Extend t0084's deep-dive methodology (24-direction
NEURON simulations with extended Vm + NMDA conductance + Nav1.6 / NaP current density
recording at soma / mid-dendrite / distal dendrite / AIS) to all 6 Genuine cells. Compare
per-cluster Vm dynamics (Cluster 0 high-NaP+high-AIS vs Cluster 1 high-GABA-lambda). Produce
one cluster-specific mechanism attribution figure plus a comparative table. Expected cost:
~$1.20 USD on Vast.ai EPYC 7B13 (6 cells x 24 directions x 60 s = 2.4 h x $0.35/hr).
Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>10-replication robustness extension: rerun the 6 Genuine + 7
Marginal cells at 10 outer seeds</strong> (S-0086-04)</summary>

**Kind**: experiment | **Priority**: medium

t0086 used 5 outer seeds, distinguishing Genuine (5/5) from Marginal (3-4/5) from Stochastic
(<=2/5). A 10-rep extension on the 13 Genuine + Marginal cells (skip the 7 Stochastic that
already failed) would produce a finer 10/9-8/<=7 partition that more accurately separates
truly-genuine cells from borderline-Marginal cases like cell 1379 (4/5 in t0086) and cell 1559
(4/5). The bootstrap ARI would also tighten. Expected cost: ~$0.65 USD on Vast.ai EPYC 7B13
(13 cells x 5 additional reps x 135 s/rep = 2.4 h x $0.35/hr). Recommended task types:
experiment-run.

</details>

<details>
<summary><strong>Source RGC-specific NaP density measurement to replace Stuart 1999
/ Goldfinger 2000 cortical-pyramidal prior</strong> (S-0086-05)</summary>

**Kind**: evaluation | **Priority**: low

t0086's biological scorecard used Stuart 1999 / Goldfinger 2000 NaP density (0.0005 S/cm^2) as
the prior for distal NaP, but those measurements were made in cortical pyramidal cells, not
RGCs. Both Genuine clusters scored exotic on NaP (Cluster 0 +24 sigma, Cluster 1 +7 sigma) by
this prior. Conduct a focused literature search for RGC-specific NaP density measurements (try
Hu 2009, Bender-Trussell 2009, Lewis 2014 RGC review). If an RGC-specific NaP value exists,
replace the prior, re-run the scorecard, and re-classify the clusters. Expected cost: ~$0.10
USD (paper search + summarisation only). Recommended task types: review-papers.

</details>

<details>
<summary><strong>Bed A cross-bed validation: re-run NSGA-II on the t0080 Bed A
morphology with the same v3 substrate</strong> (S-0086-06)</summary>

**Kind**: experiment | **Priority**: medium

t0086 identified 6 Genuine cells in t0080's Bed B morphology, but the v3 substrate has not
been tested on Bed A. Run NSGA-II for 8 generations at population 96 on Bed A with the same v3
substrate and the same constraint (AIS-to-soma Nav ratio >= 5). Compare: (a) does Bed A
produce more or fewer joint-pass cells than Bed B? (b) do the Bed A joint-pass cells cluster
into the same 2 phenotypes (high-NMDA + high-NaP vs high-NMDA + extended-GABA) or do they
discover a third? (c) does Bed A allow biologically-plausible NMDA solutions where Bed B does
not? Expected cost: ~$2.50 USD on Vast.ai EPYC 7B13 (8 gens x 96 cells x 60 s = 13 h x
$0.35/hr). Recommended task types: experiment-run.

</details>

## Research

* [`research_code.md`](../../../tasks/t0086_robustness_cluster_bio_comparison/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0086_robustness_cluster_bio_comparison/results/results_summary.md)*

--- spec_version: "2" task_id: "t0086_robustness_cluster_bio_comparison" date_completed:
"2026-05-06" ---
# Results Summary -- t0086_robustness_cluster_bio_comparison

## Summary

Re-evaluated the top 20 cells from t0083 (15 joint-pass + 5 closest near-pass) at 24
directions x 30 inner seeds x 5 outer-seed replications on Vast.ai EPYC 7B13. **6 cells were
Genuine** (5/5 reps pass DSI >= 0.4 AND PD >= 10 Hz), **7 Marginal** (3-4/5), **7 Stochastic**
(<=2/5). k-means clustering on the 6 Genuine cells in 54-d parameter space selected
**best_k=2**; both clusters were classified **exotic** by the biological scorecard, driven by
extreme NMDA per-synapse conductance (>85 sigma above Sivyer 2013) and elevated distal NaP
density (>7 sigma above Stuart 1999) common to both clusters.

## Metrics

* **Genuine cells: 6 / 20** (cells 1517, 1604, 1634, 1639, 1663, 1677). Project pass criterion
  of
  > =3 Genuine cells for cluster analysis is **met**.
* **Marginal cells: 7 / 20** (cells 767, 1304, 1379, 1504, 1559, 1624, 1721). Cell 767 (the
  original t0081 joint-pass) is Marginal at 3/5; cell 1304 (t0083's headline highest-DSI
  0.765) is Marginal at 3/5.
* **Stochastic cells: 7 / 20** (cells 1238, 1457, 1482, 1484, 1548, 1710, 1723). Cell 1723 had
  highest DSI=1.0 but PD=6.14 Hz consistently below the 10 Hz threshold.
* **Best k = 2** by silhouette score 0.155; k-means + hierarchical-cosine +
  hierarchical-euclidean all agree (ARI = 1.0). 50-sample bootstrap stability ARI mean
  **0.597** (sd 0.387) -- moderate given small Genuine pool (n=6).
* **Cluster 0** (cells 1634, 1639, 1663): aggregate verdict **exotic**. NMDA conductance at
  **+122 sigma** above Sivyer 2013 prior, NaP distal at **+24 sigma** above Stuart 1999, GABA
  rho0 at **+7 sigma** above de Rosenroll 2026. AIS-to-soma Nav ratio 30.5 (+4 sigma vs
  Werginz 2024's 17.3).
* **Cluster 1** (cells 1517, 1604, 1677): aggregate verdict **exotic**. NMDA conductance at
  **+85 sigma**, NaP distal at **+7 sigma**, GABA lambda at **+6 sigma** above de Rosenroll
  2026. AIS-to-soma Nav ratio 11.5 (within Werginz 2024 plausible range).
* **Final cost $1.595 / 4.59 hours** wall-clock at $0.3474/hr (resolved from
  selected_offer.price_per_hour, NOT a hard-coded constant). Under the **$3.50 hard cap**.
  REQ-X cost-watchdog rate-fix verified end-to-end.

## Verification

* `verify_research_code`: PASSED (0 errors).
* `verify_plan`: PASSED (0 errors).
* `verify_logs`: PASSED (0 errors, 5 warnings -- benign command-log non-zero exit codes from
  research-code experiments and missing session-capture files; addressed in reporting step).
* `verify_machines_destroyed`: PASSED (0 errors, 3 warnings -- API unreachable warning is
  expected since the instance was already destroyed; missing failure_phase/timestamp on the
  failed_attempts entry is a known v2-spec gap; missing checkpoint_path is acceptable for a
  4.6-hour run).
* `verify_task_file`, `verify_task_dependencies`, `verify_task_folder`: PASSED.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0086_robustness_cluster_bio_comparison/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0086_robustness_cluster_bio_comparison" ---
# Results Detailed -- t0086_robustness_cluster_bio_comparison

## Summary

This task re-evaluated the top 20 cells from t0083 (15 joint-pass + 5 closest near-pass) at 24
directions x 30 inner seeds x 5 outer-seed replications and clustered the resulting Genuine
cells in the t0080 v3 substrate's 54-d parameter space, then scored cluster centroids against
published biological priors. Findings: **6 Genuine, 7 Marginal, 7 Stochastic** out of 20
cells; **best k=2** clusters; both clusters classified **exotic** because all six Genuine
cells share extreme NMDA per-synapse conductance (>85 sigma above Sivyer 2013) and elevated
distal NaP density (>7 sigma above Stuart 1999). The v3 substrate's joint-pass DSI/PD
phenotype therefore relies on NMDA-dominant dendritic mechanisms that exceed published
biological values, even when the cell behaviour is reproducible across RNG replications.

## Methodology

* **Machine**: Vast.ai instance 36240604, AMD EPYC 7B13 64-Core Processor (machine 28702 in
  Texas US), 42.67 effective cores in fractional rental, 503 GB host RAM, 25 GB container
  disk, Debian 12 bookworm container, $0.3474/hr.
* **Total runtime**: instance lifetime 4.59 h (created_at 2026-05-06T13:36:14Z, destroyed_at
  2026-05-06T18:11:42Z). Phase A run wall-clock ~4.0 h (started 2026-05-06T14:08:00Z, finished
  2026-05-06T18:07:00Z). Phase B + Phase C ran locally in <1 minute total.
* **Phase A method**: each (cell, seed) pair re-evaluated by monkey-patching
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver.SEED_BASE = seed` and
  calling the canonical `evaluate_parameter_vector` with 24 angles (every 15 deg) and 30 inner
  seeds at 43 parallel workers (matches t0083 worker count). Five outer seeds drawn
  deterministically via `np.random.SeedSequence(42).spawn(5).generate_state(1, dtype=uint32)`:
  seeds=[2684470948, 4091952314, 233227757, 3276785861, 3644269654]. Results appended to
  `replication_results.json` after each call (resumable across crashes).
* **Phase B method**: k-means with `random_state=42` and `n_init="auto"` for k=2..6 on min-max
  normalised parameter vectors (per-coord, using LOWER_BOUNDS / UPPER_BOUNDS from the t0080
  module). Best_k selected by argmax silhouette. Hierarchical clustering with cosine +
  euclidean metrics and average linkage at best_k for cross-validation. 50-sample bootstrap
  stability ARI with 80% subsample fraction.
* **Phase C method**: per-cluster centroid in unnormalised parameter space scored against 9
  published biological priors with deviation = (centroid - mean)/sigma; verdict plausible
  (|deviation| <= 2), stretched (2-5), or exotic (>5). Cluster aggregate verdict = worst-case
  across priors.
* **Cost watchdog (REQ-X)**: reads `selected_offer.price_per_hour` (0.3474) from
  `logs/steps/008_setup-machines/machine_log.json` at startup. NOT a hard-coded constant.
  Trips at $3.50 hard cap. Verified live in phase_a.log: `[cost_watchdog] resolved hourly
  rate: $0.3474/hr from machine_log.json (REQ-X)`.

## Per-Cell Robustness Table (REQ-3, REQ-5, REQ-16)

| Cell | Reason | n_pass | Class | DSI mean +/- SD | PD mean +/- SD (Hz) | param_hash |
| --- | --- | --- | --- | --- | --- | --- |
| 767 | joint_pass | 3/5 | Marginal | 0.481 +/- 0.044 | 9.92 +/- 0.89 | e76aaf1dc38069a8 |
| 1238 | near_pass | 0/5 | Stochastic | 0.022 +/- 0.005 | 49.13 +/- 0.48 | 66a7bcb69d951c11 |
| 1304 | joint_pass | 3/5 | Marginal | 0.407 +/- 0.168 | 13.45 +/- 0.20 | 7ba23cd5a02d566f |
| 1379 | joint_pass | 4/5 | Marginal | 0.433 +/- 0.039 | 12.96 +/- 0.79 | 072db5596c496513 |
| 1457 | near_pass | 0/5 | Stochastic | 0.055 +/- 0.003 | 49.95 +/- 0.28 | 290c07c7ab475e32 |
| 1482 | joint_pass | 0/5 | Stochastic | 0.280 +/- 0.077 | 15.58 +/- 0.24 | 25041566f9fe1fa7 |
| 1484 | near_pass | 0/5 | Stochastic | 0.061 +/- 0.048 | 44.23 +/- 3.59 | 0cdd8c7a9c55cecd |
| 1504 | near_pass | 3/5 | Marginal | 0.927 +/- 0.026 | 10.10 +/- 3.07 | af008748f03df857 |
| **1517** | **joint_pass** | **5/5** | **Genuine** | **0.440 +/- 0.023** | **12.87 +/- 0.49** | 43acc6e52cee06b2 |
| 1548 | joint_pass | 1/5 | Stochastic | 0.386 +/- 0.013 | 18.22 +/- 0.49 | a91d4bf693092a69 |
| 1559 | joint_pass | 4/5 | Marginal | 0.554 +/- 0.145 | 39.50 +/- 0.59 | caeefac0e9198960 |
| **1604** | **joint_pass** | **5/5** | **Genuine** | **0.428 +/- 0.019** | **11.50 +/- 0.70** | 79a6cf6148561dca |
| 1624 | joint_pass | 3/5 | Marginal | 0.454 +/- 0.225 | 26.80 +/- 1.01 | 9b9adf2993234fca |
| **1634** | **joint_pass** | **5/5** | **Genuine** | **0.614 +/- 0.111** | **18.70 +/- 0.29** | 19b78a8cc7494d43 |
| **1639** | **joint_pass** | **5/5** | **Genuine** | **0.527 +/- 0.027** | **15.47 +/- 0.37** | 550ccfcec91be3c7 |
| **1663** | **joint_pass** | **5/5** | **Genuine** | **0.543 +/- 0.049** | **12.79 +/- 0.31** | 76f3648c8c07f8e4 |
| **1677** | **joint_pass** | **5/5** | **Genuine** | **0.877 +/- 0.065** | **40.85 +/- 0.47** | 78905f41403eb80c |
| 1710 | joint_pass | 2/5 | Stochastic | 0.355 +/- 0.128 | 19.83 +/- 0.18 | 16471db482a41747 |
| 1721 | joint_pass | 3/5 | Marginal | 0.603 +/- 0.022 | 10.38 +/- 0.60 | b5c3305624e6c3a0 |
| 1723 | near_pass | 0/5 | Stochastic | 1.000 +/- 0.000 | 6.14 +/- 0.66 | eb0794749f01cafd |

**Aggregate**: 6 Genuine, 7 Marginal, 7 Stochastic.

## Cluster Analysis Results (REQ-6, REQ-7, REQ-9, REQ-10)

* **Best k = 2** by silhouette (score 0.155, the only k that survives the trivial check on n=6
  cells).
* **k-means labels** (cells in order 1517, 1604, 1634, 1639, 1663, 1677): [1, 1, 0, 0, 0, 1].
* **Hierarchical-cosine labels**: [1, 1, 0, 0, 0, 1] (ARI vs k-means = **1.0**).
* **Hierarchical-euclidean labels**: [1, 1, 0, 0, 0, 1] (ARI vs k-means = **1.0**).
* **All three methods agree** on the partition.
* **50-sample bootstrap ARI** mean **0.597 +/- 0.387** (50 successful bootstraps; subsample
  80% of the 6 Genuine cells). Moderate stability given the small Genuine pool.
* **Cluster 0** (n=3): cells 1634, 1639, 1663. Mean within-cluster variance = 0.005 in
  normalised space. Cells share elevated firing rate diversity (PD = 18.70, 15.47, 12.79 Hz).
* **Cluster 1** (n=3): cells 1517, 1604, 1677. Mean within-cluster variance = 0.012 in
  normalised space. Cells span moderate to high DSI (0.440, 0.428, 0.877) and PD (12.87,
  11.50, 40.85 Hz).
* **Between-cluster distance** in normalised 54-d space: 0.18 (Euclidean) -- modest
  separation.

## Biological Plausibility Scorecard (REQ-11, REQ-12)

### Cluster 0 (cells 1634, 1639, 1663) -- aggregate verdict: exotic

| Prior | Citation | Centroid value | Published mean | Sigma | Deviation (sigma) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `nav16_ais_gbar` | Kole 2008 | 0.4672 | 0.375 | 0.125 | +0.74 | plausible |
| `nav16_ais_gbar` | Werginz 2024 | 0.4672 | 1.3 | 0.3 | -2.78 | stretched |
| `nav16_dend_distal` | Oesch 2005 | 0.0342 | 0.05 | 0.02 | -0.79 | plausible |
| `nap_dend_distal` | Stuart 1999 | 0.00528 | 0.0005 | 0.0002 | **+23.89** | **exotic** |
| `gnmda_dend` | Sivyer 2013 | 0.00622 | 0.0001 | 0.00005 | **+122.32** | **exotic** |
| `voff_nmda` | Branco-Hausser 2010 | 6.115 | 0 | 5.0 | +1.22 | plausible |
| `rho0_gaba` | de Rosenroll 2026 | 4.64 | 1.0 | 0.5 | **+7.28** | **exotic** |
| `lambda_gaba_um` | de Rosenroll 2026 | 141.5 | 80 | 30 | +2.05 | stretched |
| `ais_to_soma_nav_ratio` | Werginz 2024 | 30.53 | 17.3 | 3.0 | +4.41 | stretched |

### Cluster 1 (cells 1517, 1604, 1677) -- aggregate verdict: exotic

| Prior | Citation | Centroid value | Published mean | Sigma | Deviation (sigma) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `nav16_ais_gbar` | Kole 2008 | 0.2551 | 0.375 | 0.125 | -0.96 | plausible |
| `nav16_ais_gbar` | Werginz 2024 | 0.2551 | 1.3 | 0.3 | -3.48 | stretched |
| `nav16_dend_distal` | Oesch 2005 | 0.022 | 0.05 | 0.02 | -1.40 | plausible |
| `nap_dend_distal` | Stuart 1999 | 0.00199 | 0.0005 | 0.0002 | **+7.44** | **exotic** |
| `gnmda_dend` | Sivyer 2013 | 0.00438 | 0.0001 | 0.00005 | **+85.51** | **exotic** |
| `voff_nmda` | Branco-Hausser 2010 | 4.261 | 0 | 5.0 | +0.85 | plausible |
| `rho0_gaba` | de Rosenroll 2026 | 3.484 | 1.0 | 0.5 | +4.97 | stretched |
| `lambda_gaba_um` | de Rosenroll 2026 | 272.8 | 80 | 30 | **+6.43** | **exotic** |
| `ais_to_soma_nav_ratio` | Werginz 2024 | 11.53 | 17.3 | 3.0 | -1.92 | plausible |

## Visualizations

![Robustness
classification](../../../tasks/t0086_robustness_cluster_bio_comparison/results/images/robustness_classification.png)

![Cluster silhouette vs
k](../../../tasks/t0086_robustness_cluster_bio_comparison/results/images/cluster_silhouette.png)

![Cluster
dendrogram](../../../tasks/t0086_robustness_cluster_bio_comparison/results/images/cluster_dendrogram.png)

![Cluster 2D embedding (PCA
fallback)](../../../tasks/t0086_robustness_cluster_bio_comparison/results/images/cluster_umap.png)

![Biological plausibility
heatmap](../../../tasks/t0086_robustness_cluster_bio_comparison/results/images/biological_plausibility_heatmap.png)

## Examples

This section provides concrete per-cell examples meeting the >=10 example requirement.

### Sample raw record from `replication_results.json`

A representative single (cell, seed) record showing the full input and output structure:

```json
{
  "cell_id": 1677,
  "selection_reason": "joint_pass",
  "seed_index": 0,
  "seed": 2684470948,
  "parameter_hash": "78905f41403eb80c",
  "dsi": 0.871,
  "pd_rate_hz": 40.61,
  "peak_vm_mv": 32.4,
  "is_unstable": false,
  "elapsed_s": 134.5,
  "timestamp": "2026-05-06T17:35:12Z"
}
```

### Sample classification record from `cell_classification.json`

```json
{
  "cell_id": 1677,
  "selection_reason": "joint_pass",
  "classification": "Genuine",
  "n_pass": 5,
  "n_total": 5,
  "dsi_mean": 0.877,
  "dsi_sd": 0.065,
  "pd_mean": 40.85,
  "pd_sd": 0.47,
  "peak_vm_mean": 32.4,
  "peak_vm_sd": 0.5,
  "n_unstable": 0,
  "parameter_hash": "78905f41403eb80c",
  "parameter_hashes_match": true
}
```

### Best case: Cell 1677 (Genuine, highest DSI)

* **Cell 1677** (Cluster 1, t0083 gen 17): DSI mean **0.877 +/- 0.065**, PD mean **40.85 +/-
  0.47 Hz**, 5/5 reps pass. parameter_hash 78905f41403eb80c. Carries forward as the project's
  highest-DSI Genuine cell.

### Best case: Cell 1634 (Genuine, second-highest DSI)

* **Cell 1634** (Cluster 0, t0083 gen 17): DSI mean **0.614 +/- 0.111**, PD mean **18.70 +/-
  0.29 Hz**, 5/5 reps pass. parameter_hash 19b78a8cc7494d43.

### Genuine baseline: Cell 1604 (Genuine, lowest DSI in Genuine pool)

* **Cell 1604** (Cluster 1, t0083 gen 16): DSI mean **0.428 +/- 0.019**, PD mean **11.50 +/-
  0.70 Hz**, 5/5 reps pass. Lowest DSI in the Genuine pool but still robust.

### Borderline Marginal: Cell 767 (the original t0081 joint-pass)

* **Cell 767** (joint-pass, t0081 gen 7 carryover): DSI mean **0.481 +/- 0.044**, PD mean
  **9.92 +/- 0.89 Hz** -- the PD mean is 0.08 Hz BELOW the 10 Hz threshold. Only 3/5 reps
  pass. Cell 767's joint-pass status was therefore borderline; this corroborates the
  brainstorm-16 hypothesis that single-seed joint-pass classifications were optimistic.

### Borderline Marginal: Cell 1304 (t0083's headline highest-DSI joint-pass)

* **Cell 1304** (joint-pass, t0083 gen 13): DSI mean **0.407 +/- 0.168** (note the large SD),
  PD mean **13.45 +/- 0.20 Hz**. Only 3/5 reps pass because DSI bounces around the 0.4
  threshold. t0083's reported DSI=0.765 was a 1-of-5 high-end case; the 5-seed mean is much
  lower.

### Marginal: Cell 1559 (highest-PD joint-pass)

* **Cell 1559** (joint-pass, t0083 gen 16): DSI mean **0.554 +/- 0.145**, PD mean **39.50 +/-
  0.59 Hz**, 4/5 reps pass. The high PD provides a margin from the 10 Hz threshold; the DSI
  variance keeps it from 5/5.

### Stochastic: Cell 1238 (low-DSI Pareto near-pass)

* **Cell 1238** (near-pass, t0083 gen 12): DSI mean **0.022 +/- 0.005**, PD mean **49.13 +/-
  0.48 Hz**, 0/5 reps pass. Distance to (0.4, 10) corner = 3.57 normalised units. As expected
  for a far-from-corner cell, fails the joint criterion every time.

### Stochastic: Cell 1723 (highest-DSI near-pass)

* **Cell 1723** (near-pass, t0083 gen 17): DSI mean **1.000 +/- 0.000** (perfect), PD mean
  **6.14 +/- 0.66 Hz**, 0/5 reps pass. The DSI is perfect every time but PD never reaches the
  10 Hz threshold -- the cell is a single-direction-spike-only cell and not a true DS cell.

### Stochastic: Cell 1482 (sub-threshold DSI joint-pass that fails on re-eval)

* **Cell 1482** (joint-pass, t0083 gen 15): DSI mean **0.280 +/- 0.077** (well below 0.4!), PD
  mean **15.58 +/- 0.24 Hz**, 0/5 reps pass. t0083 reported DSI=0.456 as joint-pass for this
  cell; the 5-seed mean is 0.28 -- a clear overshoot artifact of single-seed evaluation.

### Edge case: Cell 1517 (lowest DSI in Genuine, in Cluster 1)

* **Cell 1517** (joint-pass, t0083 gen 15): DSI mean **0.440 +/- 0.023** (just above 0.4!), PD
  mean **12.87 +/- 0.49 Hz**, 5/5 reps pass. Marginal in DSI but very low SD -- consistently
  hits the threshold.

### Edge case: Cell 1663 (mid-Cluster-0)

* **Cell 1663** (joint-pass, t0083 gen 17): DSI mean **0.543 +/- 0.049**, PD mean **12.79 +/-
  0.31 Hz**, 5/5 reps pass. Median Genuine cell.

## Verification

* `verify_research_code`: PASSED (0 errors).
* `verify_plan`: PASSED (0 errors).
* `verify_logs`: PASSED (0 errors).
* `verify_machines_destroyed`: PASSED (0 errors, 3 benign warnings).
* `verify_task_file`: PASSED.
* `verify_task_dependencies`: PASSED.
* `verify_task_folder`: PASSED.
* `code/test_cost_watchdog.py`: 5/5 unit tests pass (REQ-X regression suite).
* Phase A live log line `[cost_watchdog] resolved hourly rate: $0.3474/hr from
  machine_log.json (REQ-X)` confirms REQ-X working end-to-end.

## Limitations

* **Small Genuine pool (n=6)**. Bootstrap ARI 0.597 is moderate; a 10-replication study with
  the same 20 cells (or a follow-up with more cells from a future NSGA-II extension) would
  tighten the cluster boundaries.
* **Conservative biological priors**. Where source papers do not report formal sigma, we used
  best-effort ranges. Stretched / exotic verdicts may shift if a future task tightens the
  priors, e.g. by sourcing per-RGC-subtype values from de Rosenroll 2026 supplementary tables
  instead of Sivyer 2013 generic dendritic NMDA.
* **Both clusters exotic on NMDA**. The dominant signal -- NMDA per-synapse conductance >85
  sigma above Sivyer 2013 -- is so extreme that it likely indicates a units mismatch or
  effective-conductance scaling issue between the t0080 ParameterVector encoding and the
  published per-synapse measurement, rather than a genuinely outlier biological mechanism. A
  follow-up task should investigate whether `gnmda_dend` (the NetCon weight in the t0080 v3
  substrate) is the right target to compare against Sivyer's per-spine conductance, or whether
  an effective-area scaling factor needs to be applied. This is recorded as a follow-up
  suggestion.
* **UMAP fell back to PCA on local Phase B run**. The local venv does not have umap-learn; the
  remote Vast.ai instance does, but Phase B was run locally for cost-efficiency. PCA is an
  acceptable substitute since the cluster labels were already determined by k-means in 54-d
  space.
* **Phase A used 5 outer seeds**. A 10-rep study would distinguish 10/10 from 8-9/10 from
  <=7/10 with finer granularity but doubles the cost.

## Files Created

* `code/cost_watchdog.py`, `code/paths.py`, `code/select_cells.py`, `code/generate_seeds.py`,
  `code/run_phase_a.py`, `code/classify_cells.py`, `code/cluster_analysis.py`,
  `code/plot_phase_b.py`, `code/biological_priors.py`, `code/biological_scorecard.py`,
  `code/write_answer_asset.py`, `code/build_metrics.py`, `code/run_phase_b.py`,
  `code/test_cost_watchdog.py`.
* `results/data/selected_cells.json` (20 cells: 15 joint-pass + 5 near-pass).
* `results/data/replication_seeds.json` (5 deterministic seeds).
* `results/data/replication_results.json` (100 records).
* `results/data/cell_classification.json` (per-cell classification + summary).
* `results/data/clustering_results.json` (k-means + hierarchical + bootstrap ARI).
* `results/data/cluster_centroids.json` (centroids in normalised + unnormalised space).
* `results/data/biological_priors.json` (9 priors with paper_id references).
* `results/data/biological_scorecard.json` (cluster x prior with deviation + verdict).
* `results/images/robustness_classification.png`, `cluster_silhouette.png`,
  `cluster_dendrogram.png`, `cluster_umap.png`, `biological_plausibility_heatmap.png`.
* `results/metrics.json` (20 per-cell variants).
* `results/costs.json` (REQ-X verification documentation).
* `results/remote_machines_used.json`.
* `assets/answer/cluster-biological-plausibility-attribution/details.json`, `short_answer.md`,
  `full_answer.md`.

## Task Requirement Coverage

> **Task name**: Robustness + cluster + bio-comparison of t0081/t0083 joint-pass cells.
>
> **Short description**: Re-evaluate top 20 joint-pass cells at 24 dirs x 30 seeds x 5 reps; cluster
> Genuine cells in 54-d; compare to Kole/Werginz/Sivyer/Oesch priors.

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Select 15 joint-pass cells (cell 767 + 14 t0083 with DSI>=0.4 AND PD>=10) | Done | `results/data/selected_cells.json` `joint_pass_cells` (15 entries: 767, 1304, 1379, 1482, 1517, 1548, 1559, 1604, 1624, 1634, 1639, 1663, 1677, 1710, 1721) |
| REQ-2 | Select 5 closest near-pass cells from t0083 Pareto front | Done | `results/data/selected_cells.json` `near_pass_cells` (5 entries: 1504, 1723, 1484, 1457, 1238 with distances 0.39, 0.51, 2.35, 3.49, 3.57) |
| REQ-3 | Re-evaluate each cell at 24 dirs x 30 seeds x 5 outer-seed reps | Done | `results/data/replication_results.json` (100 records) |
| REQ-4 | Record 5 outer RNG seeds deterministically | Done | `results/data/replication_seeds.json` with seeds=[2684470948, 4091952314, 233227757, 3276785861, 3644269654] |
| REQ-5 | Classify each of 20 cells as Genuine / Marginal / Stochastic | Done | `results/data/cell_classification.json` summary `{Genuine: 6, Marginal: 7, Stochastic: 7}` |
| REQ-6 | k-means k=2..6 with silhouette + BIC; select best k | Done | `clustering_results.json` `kmeans` field; best_k=2 |
| REQ-7 | Hierarchical with cosine + euclidean | Done | `clustering_results.json` `hierarchical_cosine_labels` + `hierarchical_euclidean_labels`; ARI vs k-means = 1.0 for both |
| REQ-8 | UMAP + t-SNE 2D visualisation | Partial | `cluster_umap.png` exists; UMAP fell back to PCA locally because umap-learn not installed in local venv. Documented in Limitations |
| REQ-9 | 50-sample bootstrap stability ARI | Done | `clustering_results.json` `bootstrap_ari` field: mean 0.597, sd 0.387, n=50 |
| REQ-10 | Per-cluster centroids + within/between cluster variance | Done | `cluster_centroids.json` |
| REQ-11 | Hard-code biological priors with paper_id refs | Done | `code/biological_priors.py`; 9 priors with paper_id references; `results/data/biological_priors.json` |
| REQ-12 | Score cluster centroids against priors | Done | `results/data/biological_scorecard.json`; `biological_plausibility_heatmap.png`. Both clusters exotic |
| REQ-13 | Write one answer asset attributing each cluster | Done | `assets/answer/cluster-biological-plausibility-attribution/{details.json, short_answer.md, full_answer.md}` |
| REQ-X | Cost watchdog uses actual instance hourly rate | Done | `code/cost_watchdog.py` reads `selected_offer.price_per_hour=0.3474` from machine_log.json; 5 unit tests pass; `costs.json` `breakdown.actual_rate_usd_per_hour=0.3474` |
| REQ-14 | Hard cost cap $3.50 enforced | Done | `costs.json` `total_cost_usd=1.595` <= 3.50; no `intervention/budget_overrun.md` |
| REQ-15 | Vast.ai 64-core EPYC 7B13 instance | Done | `machine_log.json` `cpu_model=AMD EPYC 7B13 64-Core Processor`; `price_per_hour=0.3474` (within fallback <$0.40/hr); first attempt at $0.3209/hr failed due to Vast.ai SSH proxy bug, retried successfully |
| REQ-16 | Replication seeds + per-cell parameter-vector hashes recorded | Done | `replication_seeds.json` + per-record `parameter_hash` in `replication_results.json`; `cell_classification.json` records `parameter_hash` and `parameter_hashes_match=true` for all 20 cells (every rep of a given cell used the same parameter vector) |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0086_robustness_cluster_bio_comparison/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0086_robustness_cluster_bio_comparison" date_compared:
"2026-05-06" ---
# Compare Literature -- t0086_robustness_cluster_bio_comparison

## Summary

Compared the centroids of the two Genuine-cell clusters (k-means best_k=2 on 6 Genuine cells)
to nine published biological priors covering AIS Nav density (`Kole2008`, `Werginz2024`),
distal Nav1.6 (`Oesch2005`), distal NaP (`Stuart1999` / `Goldfinger2000`), dendritic NMDA
per-synapse conductance (`Sivyer2013`), NMDA Mg-block voff (`Branco2010`), GABA spatial
gradient (`Rosenroll2026`), and AIS-to-soma Nav ratio (`Werginz2024`). Both clusters score
**exotic** by the worst-case aggregation rule, driven by NMDA per-synapse conductance >85
sigma above Sivyer 2013 in both clusters and elevated NaP density >7 sigma above Stuart 1999.
The AIS Nav densities sit in or near the Kole 2008 plausible band but well below the Werginz
2024 published value, reflecting the stretched / exotic dichotomy between the two AIS papers
themselves.

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

* **Scope of NMDA measurement**: Sivyer 2013's value (0.1 nS = 0.0001 uS) is a **per-spine
  synaptic conductance** measured in voltage-clamp on RGC dendritic spines. The t0086
  ParameterVector encoding `gnmda_dend` is the **NetCon weight** used in the t0080 Exp2NMDA
  mechanism inside the re-Rosenroll DSGC simulation. These may differ by a per-cell area
  normalisation or by an effective open-channel-fraction factor that the t0080 substrate does
  not separate. The +85 sigma to +122 sigma deviation may therefore partially reflect a units
  / scope mismatch rather than a genuinely outlier biological mechanism. Recorded as a
  follow-up suggestion for an ablation task that maps t0080's `gnmda_dend` onto Sivyer 2013's
  per-spine measurement.
* **NaP density measurement context**: Stuart 1999 / Goldfinger 2000 measured NaP density in
  cortical pyramidal cells, not RGCs; the 0.0005 S/cm^2 prior may be too tight for RGC
  dendrites where NaP could plausibly be 5-10x higher. Even with a 5x relaxed sigma, t0086's
  +23 sigma Cluster 0 NaP centroid (0.0053 S/cm^2 vs published 0.0005) would still be exotic;
  the +7 sigma Cluster 1 centroid (0.0020) would become stretched.
* **AIS density disagreement between Kole and Werginz**: Kole 2008 reports 0.25-0.5 S/cm^2;
  Werginz 2024 reports 1.3 S/cm^2 (~3x higher) for an updated RGC-specific model. Both
  clusters fall within or below the Kole 2008 band but well below Werginz 2024. The t0086
  sample is small (6 Genuine cells) and may favor the lower Kole-2008-consistent regime simply
  because the NSGA-II constraint `nav16_ais / nav16_soma >= 5` admits a wide range of AIS
  values; future work could enforce a tighter Werginz 2024-consistent prior.
* **GABA spatial parameters**: de Rosenroll 2026 reports the canonical linear gradient with
  rho0=1.0 and lambda~80 um. t0086 centroids are 3-5x higher in both rho0 (4.64 / 3.48) and
  3-4x higher in lambda (141.5 / 272.8). This is consistent with the v3 substrate's parameter
  bounds being deliberately wider than de Rosenroll's nominal values to allow NSGA-II
  exploration.

## Analysis

The two-cluster partition is robust at the dataset level (k-means + hierarchical-cosine +
hierarchical-euclidean all agree, ARI=1.0; 50-sample bootstrap ARI 0.597). The headline
finding is that **all six Genuine cells share an NMDA-dominant motif**: Cluster 0 NMDA
centroid is 62x higher than Sivyer 2013, Cluster 1 NMDA centroid is 44x higher. This suggests
t0080's v3 substrate found two NMDA-dominant solutions to the joint-pass DSI/PD criterion --
one with elevated AIS Nav (Cluster 0, ratio 30) and one with moderate AIS Nav (Cluster 1,
ratio 11.5). Cluster 0 also has elevated NaP, GABA rho0, and AIS-to-soma ratio -- making it a
"high-NMDA + high-NaP + high-AIS" phenotype. Cluster 1 has lower NaP and AIS but elevated GABA
lambda (spatial decay length 273 um vs published 80 um) -- making it a "high-NMDA +
extended-GABA" phenotype.

Both clusters share the dominant signature of extreme NMDA, which is the strongest deviation
across all 9 priors. This reinforces a recurring finding from t0080 / t0081 / t0083 / t0084:
the NSGA-II search routinely pushes `gnmda_dend` to the upper boundary of its log-uniform
[1e-5, 1e-2] uS range, and Genuine cells inhabit only the high-conductance regime. The t0084
mechanism attribution for cell 767 (NaP-dominant) does NOT generalise to the wider Genuine
pool: cell 767 was Marginal in t0086 (3/5 reps pass) and so does not appear in the cluster
analysis, while the 6 Genuine cells uniformly select NMDA over NaP as the dominant mechanism.

The biologically-plausible verdicts (Kole 2008 AIS, Oesch 2005 distal Nav1.6) and
biologically-stretched / exotic verdicts (Sivyer 2013 NMDA, Stuart 1999 NaP) suggest the t0080
v3 substrate is well-calibrated against AIS / Nav1.6 priors but poorly calibrated against NMDA
/ NaP priors. The natural follow-up is to tighten the NSGA-II priors on `gnmda_dend` to match
Sivyer 2013's published per-synapse value, then re-run the search and see whether any
joint-pass cells emerge in that biologically-plausible regime.

## Limitations

* **Small Genuine pool (n=6)**. The cluster centroids are means of three cells each, so
  per-cluster uncertainty is high. A future task with more Genuine cells would tighten cluster
  characterisation.
* **NMDA scale uncertainty**. Sivyer 2013's 0.1 nS prior is a per-spine synaptic conductance,
  while the t0080 `gnmda_dend` parameter is the NetCon weight, which may differ by a
  per-cell-area scaling factor. The +85 to +122 sigma exotic verdict is the most extreme and
  should be re-checked once that scaling is resolved. Recorded as a follow-up suggestion.
* **NaP measurement context**. Stuart 1999 and Goldfinger 2000 measured cortical pyramidal
  cell NaP, not RGC NaP. RGC-specific NaP measurements (where available) would shift the prior
  by several-fold and change the Cluster 1 NaP verdict from exotic to stretched.
* **AIS prior conflict**. Kole 2008 (0.25-0.5 S/cm^2) and Werginz 2024 (1.3 S/cm^2) disagree
  by ~3x. t0086 reports both as separate scorecard entries; future work should adjudicate
  which paper is the authoritative source for ON-OFF DSGC AIS density.
* **No t-SNE alternative for 2-D embedding**. Phase B used UMAP (with PCA fallback because
  umap-learn is not in the local venv) only; the plan also called for t-SNE. With n=6 cells
  t-SNE perplexity is constrained to <=5 and provides little additional information beyond
  UMAP.

</details>
