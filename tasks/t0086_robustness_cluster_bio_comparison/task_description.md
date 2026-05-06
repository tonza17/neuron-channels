# Robustness Validation and Parameter-Cluster + Biological-Plausibility Analysis of t0083 Joint-Pass Cells

## Motivation

t0083 (`bedb_v3_extend_nsga2_gen8plus`) extended t0081's NSGA-II from gen 7 through gen 17 and
**expanded the joint-pass cell population from 1 to 15 cells** (1 inherited from t0081 cell 767 + 14
new in gens 13-17), with 3 of those 15 lying on the final 18-cell Pareto front (highest-DSI cell
1304 at DSI 0.7652 / PD 13.96 Hz). Hypervolume grew +118% from gen 7 (16.330) to gen 17 (35.576).
t0084 attributed cell 767's DSI improvement to specific dendritic-spike machinery.

Three open questions follow naturally from t0083's expansion:

1. **Are the 15 joint-pass cells reproducible?** t0083's evaluation used 8 directions x 20 seeds per
   cell. Cells that satisfy the joint pass on a single 160-sim evaluation may or may not reproduce
   under different RNG seeds. The AR(2) release noise + arrival jitter dominate the stochastic
   variance; some joint-pass cells may be artefacts of a lucky RNG draw.

2. **Are the 15 joint-pass cells distributed across distinct sub-regions of the 54-d parameter
   space, or do they cluster around a single mode?** t0083's Pareto front spans a wide range of DSI
   / PD values, suggesting the search is finding multiple distinct architectural strategies that
   each satisfy joint pass. Cluster analysis can identify these strategies and characterise the
   parameter envelope of each.

3. **Are the cluster centroids biologically plausible?** The published biological priors constrain
   key parameters (AIS Nav density per Kole 2008 / Werginz 2024; AIS-to-soma Nav ratio per Werginz
   2024; dendritic NMDA conductance and Mg-block voff per Sivyer 2013 / Branco-Hausser 2010; distal
   Nav1.6 / NaP densities per Oesch 2005 / Goldfinger 2000 / Stuart 1999; GABA/AMPA spatial
   distribution per de Rosenroll 2026). A cluster whose centroid lies within +/-2 sigma of all key
   priors is "plausible"; one that lies +/-2-5 sigma is "stretched"; one that lies >5 sigma is
   "exotic". The scorecard tells the project which strategies are biologically interpretable and
   which are model artefacts.

This task addresses project research question Q1 (which Na / K combinations max AP frequency at PD
with ND suppression) and Q4 (active vs passive dendrites enable joint pass) at a
**characterisation** level rather than a **discovery** level. It bundles three previously open
suggestions (S-0083-02 motif clustering, S-0083-05 multi-seed smoke gate, multi-replicate aspect of
S-0081-01) into a single combined pipeline. Source suggestion: **S-0083-02**.

## Scope

### In scope

* **Phase A -- Robustness validation.** Select 20 cells:
  * All 15 joint-pass cells: cell 767 from t0081 + the 14 t0083 cells with DSI >= 0.4 AND PD >= 10
    Hz (read from `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` and
    `pareto_front.json`).
  * 5 closest near-pass cells from the t0083 Pareto front (`pareto_front.json`) by Euclidean
    distance to the (DSI 0.4, PD 10) joint corner among cells that do NOT satisfy joint-pass.
  * Re-evaluate each cell at **24 directions x 30 seeds = 720 sims per replication x 5 outer RNG
    seeds = 3,600 sims per cell**. Total: 100 cell-evaluations = 72,000 sims.
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
  * Check cluster stability via 50-sample bootstrap (re-run k-means on subsamples of Genuine cells;
    report Adjusted Rand Index between bootstrap labels and full-sample labels).

* **Phase C -- Biological comparison.**
  * Per cluster centroid, score key parameters against published biological priors:
    * **AIS Nav density** vs Kole 2008 (0.25-0.5 S/cm^2 cortical pyramidal AIS) and Werginz 2024
      (1.3 S/cm^2 mouse alpha-RGC).
    * **AIS-to-soma Nav ratio** vs Werginz 2024 (17.3x).
    * **Dendritic NMDA conductance** and **Mg-block voff** vs Sivyer 2013, Branco-Hausser 2010.
    * **Distal Nav1.6 / NaP densities** vs Oesch 2005, Goldfinger 2000, Stuart 1999.
    * **GABA/AMPA spatial distribution** vs de Rosenroll 2026.
  * Per parameter: report cluster centroid value, published mean +/- sigma, deviation in sigma
    units, and verdict (plausible / stretched / exotic).
  * Per cluster: aggregate verdict across all key parameters; flag the cluster as overall plausible
    / stretched / exotic.
  * Output: one **answer asset** at `assets/answer/cluster-biological-plausibility-attribution/`
    attributing each cluster to known biology or flagging as novel/unphysical.

* **Cost-watchdog rate-fix REQ-X (HARD requirement).** The cost watchdog MUST source per-instance
  hourly rate from `machine_log.json` `selected_offer.price_per_hour`, not from a hard-coded
  constant. This protocol fix is forced by t0083's $0.83 overrun ($5.83 actual vs $5.00 cap; in-loop
  watchdog used hard-coded $0.2382/hr but actual offer billed $0.3209/hr = 1.347x). Document
  explicitly in `plan/plan.md` and verify in implementation review.

### Out of scope

* New cells outside the t0081 + t0083 union (no fresh NSGA-II generations).
* Substrate changes (no new dendritic-spike parameters; no new channels; no AIS modifications; no
  morphology changes).
* Different morphologies (deferred S-0081-01 follow-up).
* Different conductance density realisations (deferred S-0081-01 follow-up).
* Bed A cross-bed validation (S-0081-05; deferred to a later task).

## Pass Criteria

* **Primary**: at least one cluster of >=3 Genuine cells (3 cells, all 5/5 replications joint-pass)
  with all key biological parameters within +/-2 sigma of published priors.

* **Secondary**: identify which t0083 joint-pass cells are stochastic artefacts vs genuine -- even
  if all clusters are exotic, the robustness classification is itself useful and can be used to
  reweight downstream NSGA-II warm-starts.

* **Acceptable negative**: zero Genuine clusters (all joint-pass cells turn out to be stochastic
  artefacts of lucky RNG draws). This would be a major project pivot but a clean negative result.

## Estimated Compute Cost

* Per-cell evaluation budget: 24 dirs x 30 seeds = 720 sims per replication x 5 outer-seed
  replications = 3,600 sims per cell. Total: 20 cells x 3,600 = 72,000 sims.

* Per-cell wall-clock estimate: t0083 averaged ~36 s/cell at 8 dirs x 20 seeds = 160 sims; 4.5x sim
  count = ~162 s/cell at 24 dirs x 30 seeds (per replication). 5 replications x ~162 s = ~13.5
  min/cell. With 43 effective cores parallelising over 100 cell-evals (20 cells x 5 replications):
  ~13.5 min x 100 / 43 = ~31 min, but per-replication overhead dominates; empirical estimate: 5-6
  hours optimiser time + ~1 hour Vast.ai instance overhead = 6-7 hours wall-clock.

* **Cost estimate: $1.93-$2.57** at $0.32/hr (allow up to 8 hours of EPYC 7B13 instance lifetime).
  Hard cost cap: **$3.50** (1.5x estimate, absorbs the 16% variance observed in t0083).

* **Vast.ai instance class**: AMD EPYC 7B13 64-core (same as t0081 / t0083). Fallback: any 36+ core
  EPYC at <$0.40/hr if 7B13 unavailable at <$0.35/hr.

## Dependencies

* **t0083_bedb_v3_extend_nsga2_gen8plus**: provides `pareto_front.json` (18 cells) and
  `all_evaluations.json` (1728 cells; 14 of 15 joint-pass cells from gens 13-17). Provides the
  evaluation harness (the loop is `arf.libraries.t0083_loop`-style continuation of t0081's harness)
  to be re-used for the robustness re-evaluation.

* **t0081_bedb_v3_warmstart_nsga2**: provides cell 767 (the first joint-pass cell), the v3 substrate
  harness, and the NSGA-II + warm-start scaffolding.

* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset (54-d v3 substrate) used unchanged.

* **t0078_bedb_mobo_v2_ais_tiered_ahp**: provides the AIS-augmented parent substrate from which
  t0080 derived the v3 substrate (informs the AIS-Nav biological prior).

* **t0024_port_de_rosenroll_2026_dsgc**: provides the de Rosenroll 2026 DSGC NEURON port (Bed B base
  substrate before AIS / dendritic-spike augmentation; informs the GABA/AMPA spatial distribution
  biological prior).

* **t0084_t0081_cell_767_vm_trace_deepdive**: provides the cell-767 mechanism-attribution answer
  asset (informs the biological priors for the cell-767 cluster).

## Recommended Task Types

* `experiment-run` -- Phase A robustness re-evaluation (Vast.ai compute).
* `data-analysis` -- Phase B cluster analysis (local CPU; sklearn + UMAP).
* `answer-question` -- Phase C biological-plausibility scorecard (one answer asset).

## Notes

The 5 outer RNG seeds for Phase A must be deterministic and recorded in
`results/data/replication_seeds.json` to enable exact reproduction. The seeds should be drawn from a
fixed parent seed (e.g., 0..4 from `np.random.SeedSequence(42).spawn(5)`) so that the re-evaluation
is exactly reproducible.

The 5 closest near-pass cells should be selected from t0083's Pareto front (filtered to
non-joint-pass cells) by Euclidean distance to the (DSI 0.4, PD 10) joint corner using the formula
`sqrt((max(0, 0.4 - DSI) / DSI_scale)^2 + (max(0, 10 - PD) / PD_scale)^2)`. A reasonable choice for
the scales is `DSI_scale = 0.1` (10% of the joint-pass DSI threshold) and `PD_scale = 5 Hz` (50% of
the joint-pass PD threshold); this puts DSI and PD on roughly equal footing in the distance metric.

The biological priors in Phase C should be loaded from the existing literature surveys (t0017 /
t0018 / t0019) and confirmed via the cited papers' details / summary documents in `assets/paper/`.
The published mean and sigma for each prior must be tabulated in
`results/data/biological_priors.json` before the per-cluster scorecard is computed.

The cluster-stability bootstrap (50 samples, ARI vs full-sample labels) is the primary safeguard
against over-interpreting clusters that arise from the Genuine subset's small size (best case 15
cells). If ARI < 0.5 across the bootstrap, the cluster verdicts in the answer asset must explicitly
disclose the instability and degrade the per-cluster confidence accordingly.

The cost-watchdog rate-fix REQ-X requires that the watchdog reads
`logs/steps/<NNN>_setup-machines/machine_log.json` `selected_offer.price_per_hour` at startup and
uses that value as the hourly rate when computing accumulated cost. The watchdog MUST log the
resolved rate at startup so that any future audit can confirm the value used. Implementation review
must explicitly check this code path before merging the implementation step.
