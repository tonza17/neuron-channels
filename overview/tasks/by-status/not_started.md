# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0088 — <strong>Re-cluster t0086 13 cells and per-cluster Vm-trace
deep-dive</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0088_recluster_marginals_and_vm_motifs` |
| **Status** | not_started |
| **Effective date** | 2026-05-06 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0086-03` |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/), [`experiment-run`](../../../meta/task_types/experiment-run/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [Re-cluster t0086 13 cells and per-cluster Vm-trace deep-dive](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Task folder** | [`t0088_recluster_marginals_and_vm_motifs/`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/) |

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

<details>
<summary>⏹ 0075 — <strong>Biologically-realistic AIS one-axis-at-a-time parameter
sweep on Bed A</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0075_bio_realistic_ais_param_sweep` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0069-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Biologically-realistic AIS one-axis-at-a-time parameter sweep on Bed A](../../../overview/tasks/task_pages/t0075_bio_realistic_ais_param_sweep.md) |
| **Task folder** | [`t0075_bio_realistic_ais_param_sweep/`](../../../tasks/t0075_bio_realistic_ais_param_sweep/) |

# Biologically-Realistic AIS Parameter Sweep on Bed A

## Motivation

t0069 attached a virtual AIS plus 1 mm axon stub to Bed A (deposited Poleg-Polsky DSGC) and
re-ran the t0067 channel-addition sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} on the AIS
instead of the soma. The sweep falsified S-0067-03's prediction (AIS-localised channels show
*larger* DSI effects than soma-localised) — it actually showed the opposite, with 11 of 15
channel conditions producing zero detectable DSI change. The cause was identified clearly: the
AIS+axon halved baseline PD firing (14.2 → 6.4 spikes) and silenced ND firing (1.6 → 0.0),
pushing baseline DSI to the trivial computational ceiling 1.0. The passive AIS+axon adds an
electrical sink that quenches the cell rather than relocating spike initiation; AIS-localised
channels at our densities cannot overcome the somatic 400 mS/cm² HHst Na drive.

The follow-up question this task answers: is there *any* DSGC + AIS configuration that
simultaneously contains all the channels biologically present in a vertebrate AIS (HHst basal
Na+K, Nav1.6, Kv3, Kv7 — the canonical RGC AIS quartet) and produces non-trivial DSI at a
biologically reasonable peak rate? "Decent DSI, not 1, and reasonable firing rate" maps to the
operational pass band {DSI in [0.3, 0.95], peak Hz in [5, 50]}. The right tool is not
optimisation — it is one axis at a time. NaP is excluded from the AIS channel set on two
grounds: (a) AIS NaP expression in RGCs is controversial; (b) the t0067 NaP-high finding (DSI
sign flip) suggests NaP destabilises the DSI mechanism rather than supporting it. BK and SK
are excluded because they localise primarily to soma and dendrites in RGCs, not to the AIS.

This task addresses RQ1 (somatic + AIS VGC combinations) and RQ4 (active vs passive
components). Source suggestions covered: S-0068-04 (move Nav1.6 + Kv3 to AIS), S-0069-01
(halve somatic gnabar before AIS), S-0069-02 (shrink AIS diameter to 0.5 micrometre),
S-0069-03 (vary axon length to probe sink), S-0069-04 (Nav1.6 + Kv3 on AIS at biological
densities).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC) plus virtual AIS + axon stub.
* AIS channel set: **{HHst basal Na + K, Nav1.6, Kv3, Kv7}**. NaP, BK, SK explicitly excluded.
* Encoding: 12-angle bar-rotation protocol (same as t0074 — cross-task comparable).
* Two-stage design: Stage 1 baseline calibration; Stage 2 per-axis sweep.

### Stage 1 — Baseline calibration

* Literature-informed AIS configuration (Wang et al. 2011, Carter et al. 2008 on mouse RGC
  AIS): AIS diameter 0.8 micrometre, AIS length 30 micrometre, axon stub 1.0 mm, AIS
  gnabar_HHst 4 0 0 mS/cm^2, AIS Nav1.6 medium density (~0.3 S/cm^2 from t0067 medium), AIS
  Kv3 medium density (~0.3 S/cm^2), AIS Kv7 low density (~0.1 S/cm^2; distal AIS, weaker than
  Nav and Kv3).
* Sweep soma `gnabar_HHst` across 6 candidates: {100, 150, 200, 250, 300, 400} mS/cm^2 (the
  t0069 baseline = 400).
* 6 candidates x 12 angles x 1 seed = 72 trials, ~5 min wall-clock.
* Pick the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]}. If multiple
  candidates qualify, pick the one closest to the centre of the band ({peak ~ 20 Hz, DSI ~
  0.6}).
* If no candidate qualifies, the task halts at Stage 1 and reports a negative result with a
  recommendation for a follow-up that loosens the AIS configuration further (e.g., reduce AIS
  Nav1.6 density first, then re-attempt).

### Stage 2 — Per-axis sweep

From the Stage-1 baseline, vary one parameter at a time with all others held at baseline:

| # | Axis | Values | Non-baseline points |
| --- | --- | --- | --- |
| 1 | Soma `gnabar_HHst` (mS / cm^2) | {100, 200, 300, 400} | 3 |
| 2 | AIS `gnabar_HHst` (mS / cm^2) | {0, 100, 200, 400, 800} | 4 |
| 3 | AIS diameter (micrometre) | {0.4, 0.6, 0.8, 1.0, 1.5} | 4 |
| 4 | AIS length (micrometre) | {15, 30, 45, 60} | 3 |
| 5 | AIS Nav1.6 density | {0, low, medium, high} | 3 |
| 6 | AIS Kv3 density | {0, low, medium, high} | 3 |
| 7 | AIS Kv7 density | {0, low, medium, high} | 3 |
| 8 | Axon length (mm) | {0.1, 0.5, 1.0, 2.0} | 3 |

Total Stage-2 conditions: 1 baseline + 26 non-baseline = **27 conditions x 12 angles x 5 seeds
= 1620 FULL trials**, ~100 min wall-clock at the t0067 measured ~3.75 s / trial under CVODE.

### Width metrics per axis (cross-comparable with t0074)

For each condition, compute:

* **HWHM** in degrees from the 12-angle tuning curve.
* **Vector-sum DSI** (circular concentration).
* **Peak rate (Hz)** at the angle with maximum mean rate.
* Rate at PD (axis-1 peak angle) and at the opposite angle.
* RMSE vs the t0004 cosine target.

### Outputs

* **Library asset**: `bed_a_with_bio_realistic_ais` — Bed A + AIS + axon model variant with
  the {HHst, Nav1.6, Kv3, Kv7} channel set wired in. Reusable by future tasks that need a
  working DSGC + AIS substrate.
* **Stage 1 candidate table** (`results/baseline_candidates.csv`) with 6 rows showing
  soma_gnabar_HHst, peak Hz, DSI, in-band y/n.
* **Stage 2 per-axis sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI,
  peak rate, RMSE vs cosine target, plotted against axis values.
* **Biologically-plausible AIS recommendation table**
  (`results/biological_ais_recommendation.md`): the band-constrained range for each axis (the
  values that keep the cell inside {DSI [0.3, 0.95], peak [5, 50] Hz}), plus a recommended
  canonical configuration.
* `results/metrics.json` with registered project metrics per condition.

## Approach

1. Fork t0069's AIS-attachment code into this task's `code/`. Replace the t0069
   channel-addition loop with the {HHst, Nav1.6, Kv3, Kv7} baseline channel set (with
   t0074-vendored Kv7).
2. Implement Stage 1 calibration as a 6-candidate sweep with explicit pass-band check and
   automated baseline selection.
3. Implement Stage 2 as 8 per-axis sweep functions sharing a common driver.
4. Run Stage 1, log selected baseline, run Stage 2.
5. Compute width metrics, generate per-axis plots, write the recommendation table.
6. Validate against t0069 sanity checks: trials with instability flags = 0, peak Vm bounded.

## Pass Criteria

* Stage 1 finds at least one in-band baseline (peak Hz in [5, 50] AND DSI in [0.3, 0.95]).
* All 1620 + 72 trials complete with no instability flags.
* Per-axis sensitivity plots show monotonic or unimodal sensitivity for at least 6 of the 8
  axes (the axes that don't are flagged as candidates for re-investigation; not a hard fail).
* Recommendation table produced with the band-constrained range for each axis.

## Compute Estimate

* ~2 h wall-clock on local CPU. 72 trials Stage 1 (~5 min) + 1620 trials Stage 2 (~100 min) +
  ~10 min plotting / metrics extraction.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code (Nav1.6, Kv3
  implementation patterns).
* `t0069_t0067_ais_localised_channel_sweep` — AIS attachment code; baseline characterisation
  of the passive-AIS sink effect.
* `t0074_channel_tuning_width_bed_a` — Kv7 MOD vendoring lands in t0074. This task inherits
  the vendored Kv7 mechanism and the calcium-pool unification (the latter is not actively used
  here but must remain compatible).

## Risks and Fallbacks

* **Stage 1 finds no in-band baseline**: the task halts after Stage 1 and reports a negative
  result with a follow-up recommendation. Time-cheap (~5 min). The follow-up would probably be
  a 2D Stage 1.5 sweep over {soma gnabar, AIS gnabar} or a baseline that further reduces AIS
  Nav1.6 density.
* **Stage 1 is over-fitted to soma_gnabar**: if the baseline soma_gnabar value is borderline
  (e.g., exactly at the edge of the in-band region), small parameter changes in Stage 2 may
  push the cell out of band rapidly. Mitigation: pick the Stage-1 baseline closest to the band
  centre, not the band edge.
* **Axes interact strongly**: the one-axis-at-a-time design assumes weak interactions. If a
  Stage-2 axis sweep produces non-monotonic behaviour (e.g., DSI rises then falls), report the
  non-monotonicity explicitly and flag the axis for a future joint sweep with one neighbouring
  axis.
* **AIS+axon discretisation artefacts**: if the segment count along the AIS or axon is too
  low, spike initiation and propagation may be artefactual. Mitigation: use NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) and validate that the
  chosen segment count doubles without changing peak Vm by more than 1 mV at the t0069
  baseline.

## Out of Scope

* Bed B (de Rosenroll) — explicitly out of scope per researcher decision; this task is Bed A
  only.
* Joint multi-axis optimisation — explicitly excluded; this is one-axis-at-a-time only.
* Other AIS channel candidates (Nav1.2, Kv1, Kv4 alpha-DTX-sensitive subtype) — out of scope;
  the channel set is fixed at {HHst, Nav1.6, Kv3, Kv7}. Future follow-ups may extend the
  channel set.

</details>

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
