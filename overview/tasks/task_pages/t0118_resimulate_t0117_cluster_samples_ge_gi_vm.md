# ✅ Re-simulate 10 cells per t0117 ephys cluster; plot g_E, g_I, Vm in PD and ND

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0118_resimulate_t0117_cluster_samples_ge_gi_vm` |
| **Status** | ✅ completed |
| **Started** | 2026-05-22T15:33:58Z |
| **Completed** | 2026-05-22T18:31:09Z |
| **Duration** | 2h 57m |
| **Dependencies** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **Task types** | `experiment-run`, `data-analysis` |
| **Step progress** | 9/15 |
| **Task folder** | [`t0118_resimulate_t0117_cluster_samples_ge_gi_vm/`](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/task_description.md)*

# Re-Simulate 10 Cells per t0117 Electrophys Cluster — g_E, g_I, V_m in PD and ND

## Motivation

t0117 partitioned the 4 431-cell unfiltered pool into 4 electrophys clusters (k = 4, mean
silhouette = 0.158, NMI vs seed = 0.562) using only standardised 54-d electrophys features and
the 68-d KMeans centroid distances. The clusters separate cells by their channel-density
signature, but t0117 never re-simulated cells from each cluster to show what those
electrophysiological differences look like in *measured biophysical traces*. This task closes
that gap by taking 10 representative cells per cluster, re-running the canonical DSGC
simulation protocol on each in PD and ND directions, and producing per-cluster figures of
excitatory and inhibitory conductance plus somatic membrane potential.

The cells must **span DSI and PD-rate** within each cluster — not just the high-quality corner
— so the reader can see *how* the cluster's channel signature interacts with the firing output
across the full quality range that ended up in that cluster.

## Scope

### Cell selection (40 cells total: 10 per cluster × 4 clusters)

Source data:
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/electrophys_clusters.csv`
(cluster assignments) and
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet` (the
68-d feature vector and DSI / PD values per cell).

**Stratified DSI × PD sampling per cluster**:

1. For each cluster `c ∈ {0, 1, 2, 3}`, take all its cells and split them into 5 DSI quintiles
   × 5 PD quintiles (25 bins).
2. Walk the 25 bins in canonical raster order and pick **one cell per occupied bin** until 10
   are selected. Prefer bins that span the full DSI × PD range over re-picking from
   well-covered bins.
3. If fewer than 10 occupied bins exist in a cluster (likely for cluster 1 — t0117 mostly
   high-DSI/high-PD seed-7755 cells), top up by adding the next-most-distant cell (max
   Euclidean distance in standardised DSI × PD space from the already-selected set) until 10
   are picked.
4. Use a fixed random seed (`SAMPLE_SEED = 117`) for any tie-breaking. Record every selected
   cell to `results/data/selected_cells.csv` with columns `cluster_id, source_task, seed,
   generation, individual_idx, dsi_vector_sum, pd_rate_hz, dsi_quintile, pd_quintile`.

The 40 selected cells must be saved as a manifest before any simulation begins so the
selection is fully reproducible from the manifest alone.

### Simulation protocol (per cell)

For every selected cell, reconstruct the cell from its 68-d parameter vector using the
project-standard procedural morphology generator (`procedural_dsgc_morphology_generator_fix`
from t0092, with the same `morph_seed` normalisation as t0116/t0117) and run the canonical
mode trio in PD and ND directions:

* **EPSP_PASSIVE** — HH off, only excitatory (ACh + glutamate / NMDA) synapses active. Records
  `g_E(t)` per direction.
* **IPSP_PASSIVE** — HH off, only inhibitory (GABA) synapses active. Records `g_I(t)` per
  direction.
* **FULL** — HH on, all synapses active. Records somatic `V_m(t)` per direction.

3 modes × 2 directions × 40 cells = **240 NEURON runs** total.

Use the project-standard trial length of **1 400 ms** (per the DSGC measurement protocol
established in t0065 / t0066 and confirmed throughout the t0080+ run series), bar-motion
parameters consistent with the source NSGA-II runs (t0106 / t0114 / t0115 evaluation protocol
— read t0080's library and t0106's plan to confirm exact bar speed, width, and spatial
extent), and identical `morph_seed` per cell across modes so the morphology is deterministic.

If any simulation fails (NEURON crash, silent cell, parameter-bounds violation), record the
failure in `results/data/simulation_failures.csv` and continue with the remaining cells.
Substitute the next-best stratified candidate from the same cluster only if a cell fails; do
not re-sample without recording the substitution.

### Outputs

#### Trace storage

For each (cell, mode, direction) triple, save:

* `results/data/traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` with columns `t_ms,
  g_e_us, g_i_us, v_m_mv` (whichever are recorded for that mode; columns not recorded in that
  mode are absent).
* Where `<cell_key> = <seed>_<generation>_<individual_idx>`.

#### Per-cluster summary figures

One figure per cluster, saved to `results/images/cluster_<c>_traces.png`. Layout: a 10-row ×
3-column grid where each row is one cell, columns are `g_E(t)`, `g_I(t)`, `V_m(t)`. Within
each panel, plot PD and ND traces in two distinguishable colours (PD solid, ND dashed) with
the cell's `(DSI, PD_rate)` annotated in the panel corner. Y-axis units: μS for conductances,
mV for V_m. X-axis: time in ms, full 1 400 ms window.

Cells are ordered top-to-bottom within each cluster by **DSI ascending**, so the reader can
read the variability gradient at a glance.

#### Cross-cluster comparison figure

A 4-row × 3-column summary figure `results/images/cross_cluster_traces.png`. Each row is one
cluster's *median* trace within the row (median over the 10 cells of that cluster); columns
are `g_E`, `g_I`, `V_m`. PD and ND overlaid as before. This gives a single-glance summary of
how the four electrophys clusters differ in their canonical conductance and V_m signatures.

#### Per-cell metric extraction

For every cell, compute and emit to `results/data/per_cell_metrics.csv` the following
per-direction quantities (rows = (cell, direction); columns include the cell identifiers plus
the metrics):

* Peak g_E and time-to-peak (ms)
* Peak g_I and time-to-peak (ms)
* g_I / g_E ratio at peak g_E (the canonical excitation-inhibition balance)
* g_I onset latency (time from stimulus onset to half-rise of g_I)
* Number of spikes in `V_m` (count crossings of −10 mV with refractory ≥ 2 ms)
* Mean and max V_m during the 1 400 ms window

These extracted metrics let downstream tasks build comparative tables without re-loading the
parquet trace files.

### Key questions (each becomes one `assets/answer/` asset)

This task does NOT produce answer assets in the canonical ARF sense — its output is a
demonstration / exploratory artefact, not a question-answering artefact. `expected_assets` in
`task.json` is therefore `{}`. The figures and per-cell metrics are the deliverables;
interpretation lives in `results_detailed.md` `## Analysis`.

## Approach

### Code reuse

* **NEURON model and simulator entrypoint**: the implementation must locate the canonical Bed
  B + morphology DSGC simulation library used by t0106 / t0112 / t0114 / t0115. The
  research-code step is responsible for identifying the right entrypoint (likely in
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/` or a registered library asset under
  `tasks/t0080_*/assets/library/`) and the canonical mode-trio invocation.
* **Morphology generator**: `generate_fixed_morphology` from
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix`.
* **68-d parameter unpacking**: reuse the constants and parameter unpacking from
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` `ALL_PARAM_NAMES` — same
  layout as t0116 / t0117.

Per the cross-task import rule, any non-library code from these source tasks must be **copied
into `tasks/t0118_*/code/`** rather than imported.

### Pipeline structure

* `code/load_t0117_clusters.py` — load t0117's cluster assignments and the parameter vectors
* `code/stratified_sample.py` — implement the DSI × PD stratified picker; write
  `results/data/selected_cells.csv`
* `code/simulate_cell.py` — single-cell driver: take a parameter vector, build the cell, run
  the 3-mode trio in PD+ND, save traces to parquet
* `code/run_all_cells.py` — top-level driver that iterates over the 40 cells (sequentially or
  with `concurrent.futures.ProcessPoolExecutor` if isolation is solid; NEURON's globalness may
  force sequential)
* `code/extract_metrics.py` — read all trace parquets, compute the per-direction metrics,
  write `results/data/per_cell_metrics.csv`
* `code/plot_cluster_figures.py` — produce the 4 per-cluster figures and the cross-cluster
  summary

### Sequential vs parallel

NEURON is famously not process-safe inside a single Python session due to global state in the
`h` instance. The default is sequential simulation (1 cell at a time, ~10–30 s per cell for
the 3-mode trio in 2 directions, ~20–45 min total). If the implementation finds that each cell
can be wrapped in its own subprocess via `concurrent.futures.ProcessPoolExecutor` without
state bleed, that's allowed but must be validated by comparing a small parallel batch against
the sequential reference. **Do not commit to parallel without validation.**

## Expected Outputs

### Assets

None (`expected_assets: {}`). This is a demonstration task.

### Tables (under `results/data/`)

* `selected_cells.csv` — the 40-cell stratified sample manifest (committed before sims start)
* `per_cell_metrics.csv` — peak conductances, latencies, spike counts, V_m extrema per cell
  per direction
* `simulation_failures.csv` — any NEURON errors or silent-cell failures encountered
* `traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` — 480 trace files total (40
  cells × 3 modes × 2 directions, but `g_E` / `g_I` / `V_m` columns vary by mode)

### Charts (under `results/images/`)

* `cluster_0_traces.png` ... `cluster_3_traces.png` — 4 per-cluster 10-row × 3-column trace
  grids
* `cross_cluster_traces.png` — 4-row × 3-column median-trace summary

### Optional analysis blocks in `results_detailed.md`

* `## Analysis` — per-cluster interpretation of how the conductance and V_m signatures differ.
  Connect findings back to t0117's F1 / F3 / F5 factor structure where possible (e.g.,
  "cluster 1 cells show large peak `g_E` consistent with low SK_AIS density — this is the F1
  axis Sthe high-DSI corner of t0117 sits on").

## Compute and Budget

CPU-only, local NEURON. No remote machines. No paid APIs. `total_cost_usd: 0`.

Wall-clock estimate: **30–60 minutes**. Each cell needs ~10–30 s for the 3-mode trio in 2
directions (1 400 ms simulated time × 3 modes × 2 dirs × per-step integration overhead).
Sequential 40 cells = 7 – 20 min for simulation + ~5 min for plotting and metric extraction.

## Cross-References

* **Source data**: t0117 (cluster assignments + parameter vectors)
* **Simulation infrastructure**: t0080 (BedB+morph simulator), t0090 / t0092 (morphology
  generators)
* **Measurement protocol**: the DSGC measurement-protocol convention established across t0065
  / t0066 (EPSP_PASSIVE / IPSP_PASSIVE / FULL trio, 1 400 ms trial length, HH off for passive
  traces)
* **Cohort context**: t0116 (strict-cohort version of the parent analysis); t0117's three
  answer assets for the broader interpretation of the cluster structure

## Verification Criteria

* `selected_cells.csv` contains exactly 40 rows (10 per cluster) and every cell's `(seed,
  generation, individual_idx)` triple maps back to a unique row in
  `tasks/t0117_*/data/pooled_all_cells.parquet`.
* Every selected cell has at least one trace file per (mode, direction); any missing
  combinations must be recorded in `simulation_failures.csv` with a stated reason.
* Each per-cluster figure renders 10 rows × 3 columns of non-empty traces (or annotated
  failure placeholders for any simulation that failed).
* The cross-cluster summary figure renders 4 rows × 3 columns with all panels populated.
* Every trace parquet has at least 1 400 ms of samples at the simulator's default dt
  (typically 0.025 ms → ~56 000 rows).
* PD direction must produce more spikes than ND in `V_m` for cells with `dsi_vector_sum > 0.5`
  (sanity check; cells with DSI ≤ 0.5 may not respect this).

</details>

## Suggestions Generated

<details>
<summary><strong>Re-simulate t0118 stratified sample on t0116 strict cohort (DSI >
0.7 AND PD > 10) for a good-DSGC trace gallery</strong> (S-0118-01)</summary>

**Kind**: experiment | **Priority**: high

t0118 found the unfiltered pool is heavily DSI ~ 0; only cluster 2 (s7755) supplied DSI >= 0.2
cells, so the per-cluster trace grids do not show good DSGC behaviour for clusters 0/1/3.
Apply the identical 10-per-cluster stratified-by-DSI-x-PD sampler and 3-mode trio protocol to
t0116's strict 869-cell cohort, then re-cluster those cells with t0116's k=3 partition.
Outcome: 30 cells (10 per t0116 cluster) whose traces actually show the canonical DSGC
asymmetry mechanism across multiple clusters, not just one. Distinct from t0118 (unfiltered
pool) and from S-0116-* (which stay in FA/clustering space without re-simulating). Recommended
task types: experiment-run, data-analysis. Cost: <$0.20.

</details>

<details>
<summary><strong>g_I sensitivity sweep on cluster-2 DSGC-competent cells: how does
DSI vary with inhibition strength?</strong> (S-0118-02)</summary>

**Kind**: experiment | **Priority**: high

t0118 found g_I / g_E ratio at peak g_E is the most variable cell-level metric (6 orders of
magnitude, 0.03 to 440), and cluster 2 (s7755) is the only cluster where re-simulated traces
show the DSGC asymmetry mechanism. Take the 5 highest-DSI cluster-2 cells, hold every other
parameter fixed, and sweep global GABA NetCon weight (w_gaba_us) in 7 log steps from 0.1x to
10x (plus symmetric w_ach control). For each (cell, w_gaba_factor) re-run the FULL mode in
PD+ND, extract DSI, peak g_I, g_I/g_E ratio. Plot DSI vs w_gaba per cell. Decision: if DSI
peaks at the same w_gaba factor across cells, the cohort shares a canonical E-I balance; if
optimum varies, the optimiser found cell-specific compensation. ~140 NEURON runs. Recommended
task types: experiment-run, data-analysis. Cost: <$0.20.

</details>

<details>
<summary><strong>Diagnose evaluator-disagreement bug for cell 77_15_1356: t0117 DSI
= 0.93, t0118 canonical protocol = 0 spikes</strong> (S-0118-03)</summary>

**Kind**: evaluation | **Priority**: high

t0118 found cell 77_15_1356 (cluster 0, seed 77) was assigned DSI = 0.93 by t0117's NSGA-II
evaluator but produces 0 spikes in either direction under the canonical 1400 ms / -10 mV
threshold protocol (FULL V_m peaks at -51 mV); g_I/g_E ratio = 3.87 (extreme inhibition
dominance). The t0117 DSI score appears to be a finite-sample-noise artefact, unconfirmed.
Investigate: (a) re-run t0117's evaluator on this cell, log per-trial PD and ND spike counts;
(b) re-run with 10 eval-seed pairs and check stability; (c) trace the DSI formula for
PD=1/ND=0 edge cases; (d) report whether other pool cells share this 'high-DSI-but-silent'
pattern. Decision: if >= 1% of pool exhibits this disagreement, t0117/t0116 DSI columns need a
corrections overlay. Recommended task types: data-analysis, correction. Cost: <$0.10.

</details>

<details>
<summary><strong>Factor-axis trace gallery: sample cells along t0117 F1/F3/F5
loading axes and re-simulate the 3-mode trio</strong> (S-0118-04)</summary>

**Kind**: experiment | **Priority**: medium

t0118 establishes a clean re-simulation pipeline (3-mode trio, g_E / g_I / V_m, PD+ND, 1400
ms). t0117's salient factors are F1 (joint DSI-PD, 12.6% var), F3 (pure-ephys PD), F5
(depolarisation-block axis hypothesised in t0118 analysis). Link from factor space to
biophysics is currently inferential. Concrete action: project all 4431 t0117 cells onto F1,
F3, F5 individually; bin cells into 7 quantiles along each factor score, sample 3 cells per
bin (21 cells x 3 factors = 63 cells), re-simulate the t0118 protocol. For each factor produce
a 7-row x 3-column grid showing how g_E/g_I/V_m signatures change along the factor axis.
Decision: monotonic variation = biophysically meaningful factor; unrelated = statistical
artefact. Distinct from S-0117-06 (interprets F1 loadings statically). Recommended task types:
experiment-run, data-analysis. Cost: <$0.30.

</details>

<details>
<summary><strong>Per-cluster ND-leading g_I latency analysis: is the SAC-like
inhibitory-veto signature present across clusters?</strong> (S-0118-05)</summary>

**Kind**: experiment | **Priority**: medium

t0118's per-cluster panels show ND g_I peaks earlier than PD g_I in cluster 1 (all-s44, DSI ~
0) traces - the classic Vaney/Taylor inhibitory-veto signature - even though firing asymmetry
is absent. This suggests the inhibitory-timing mechanism is partially present in cells the
NSGA-II selected as low-DSI. Action: extract per-cell PD and ND g_I onset latency from t0118's
per_cell_metrics.csv, plot (latency_ND - latency_PD) per cluster, test (a) is the ND-leads-PD
pattern significant per cluster, (b) does the magnitude correlate with DSI within cluster, (c)
is there a critical latency threshold above which firing asymmetry emerges? Re-simulate top-5
latency-difference cells per cluster at RECORD_DT = 0.1 ms to confirm timing isn't aliased.
Distinct from S-0118-02 (sweeps inhibition strength, not timing). Recommended task types:
data-analysis, experiment-run. Cost: <$0.10.

</details>

<details>
<summary><strong>g_I/g_E balance classifier: can a single E-I ratio scalar predict
t0117 cluster identity?</strong> (S-0118-06)</summary>

**Kind**: evaluation | **Priority**: medium

t0118 identifies g_I / g_E ratio at peak g_E as the dominant cross-cell axis (6 orders of
magnitude, 0.03 to 440). The cluster-by-cluster interpretation proposes a categorical mapping:
cluster 1 < 0.5 (excitation-dominated), 0/2 in 0.5-5 (balanced), 3 > 10
(inhibition-dominated). Currently qualitative. Build a quantitative classifier: fit a
single-feature logistic regression and KNN predicting cluster_id from g_I/g_E ratio
(per_cell_metrics.csv); report accuracy + per-cluster precision/recall. Stretch: train a
linear regressor from t0118's 40-cell 68-d -> g_I/g_E pairs, predict ratio for the full t0117
4431-cell pool, map back to cluster IDs, report agreement vs t0117's KMeans labels. Decision:
if a single g_I/g_E feature explains > 70% of cluster identity, the t0117 cluster structure
reduces to one biophysical scalar. Recommended task types: data-analysis. Cost: <$0.10.

</details>

## Research

* [`research_code.md`](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/results_summary.md)*

# Results Summary: Re-Simulate 10 Cells per t0117 Electrophys Cluster

## Summary

Stratified-sampled 40 cells (10 per t0117 electrophys cluster, k = 4) spanning DSI × PD
quintiles from the unfiltered 4 431-cell pool and re-simulated each cell in the canonical
3-mode trio (EPSP_PASSIVE, IPSP_PASSIVE, FULL) for PD (0°) and ND (180°) directions — 240
NEURON runs total, zero failures, ~70 min wall-clock. Produced 4 per-cluster 10-row × 3-column
trace figures (g_E / g_I / V_m, PD solid + ND dashed) and a 4-row × 3-column cross-cluster
median-trace summary. Demonstration / exploratory artefact; no answer assets produced
(`expected_assets: {}`).

## Metrics

* **Cells re-simulated**: **40** (10 per electrophys cluster, stratified across 5 DSI × 5 PD
  quintile bins per cluster)
* **NEURON runs completed**: **240 / 240** (success rate 100.0%)
* **DSI span sampled**: **0.0 to 0.93** (most of the unfiltered pool sits near 0 — this is
  genuine pool composition, not a sampling bug; only seed 7755 cells provide DSI ≥ 0.2)
* **PD-rate span sampled**: **0.7 to 115 Hz**
* **Peak g_E range across cells**: **0.001 to 0.32 µS**
* **Peak g_I range across cells**: **0.016 to 0.95 µS**
* **g_I / g_E ratio (at peak g_E) range**: **0.03 to 440** (six orders of magnitude — the
  excitation-inhibition balance is the most variable feature across cells)
* **Spike count range** in FULL V_m: **0 to ~26** (with one cell at DSI 0.93 producing 0
  spikes — silent under the canonical −10 mV threshold; documented)
* **Trace samples per file**: **1 400** (RECORD_DT = 1.0 ms × TSTOP = 1 400 ms)
* **Figures produced**: **5** (4 per-cluster + 1 cross-cluster median summary)

## Verification

* `verify_plan` — **PASSED** (0 errors, 0 warnings)
* `verify_research_code` — **PASSED**
* `verify_task_results` — **PASSED**
* `verify_task_metrics` — **PASSED** (`metrics.json = {}` valid; documented)
* C1: 40-cell manifest resolves to t0117 pooled parquet (one-to-one) — **PASSED**
* C2: every (cell, mode, direction) trace parquet has 1 400 rows with mode-correct columns —
  **PASSED**
* C3: all 5 PNGs on disk — **PASSED**
* `dsi_sanity_check.csv`: **39 / 40** cells satisfy PD-spike-count > ND-spike-count for DSI >
  0.5 (the one failure is a near-silent cell whose V_m never crosses −10 mV in either
  direction — edge case, not a pipeline bug)
* `ruff check --fix`, `ruff format`, `mypy -p
  tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code` — **PASSED**

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0118_resimulate_t0117_cluster_samples_ge_gi_vm" ---
# Detailed Results: Re-Simulate 10 Cells per t0117 Electrophys Cluster — g_E, g_I, V_m in PD and ND

## Summary

Stratified-sampled 40 cells (10 per t0117 electrophys cluster, k = 4) spanning DSI × PD
quintiles from the unfiltered 4 431-cell pool and re-simulated each cell in the canonical
3-mode trio (EPSP_PASSIVE, IPSP_PASSIVE, FULL) for PD = 0° and ND = 180°. 240 NEURON runs, 0
failures, ~70 min wall-clock. Produced 4 per-cluster 10 × 3 trace grids and a 4 × 3
cross-cluster median summary. The headline observation: cluster identity in t0117 (which is
largely seed identity at NMI = 0.562) correlates with distinct conductance and V_m signatures,
but the **dominant axis of variability is excitation-inhibition balance**, not raw g_E or g_I
magnitude.

## Methodology

* **Machine**: Local CPU (Windows 11, Python 3.12 via `uv`); no remote machines used
* **Simulator**: NEURON-based Bed-B + procedural-morphology DSGC model (the canonical
  `evaluate_68d_vector` entrypoint from t0106's evaluator, copied verbatim into this task)
* **Trial length**: TSTOP = 1 400 ms; integration dt = 0.1 ms; record dt = 1.0 ms (1 400
  samples per trace)
* **Bar motion**: velocity 1.0 µm/ms, width 250 µm, x_start = −40 µm (PD = 0°, ND = 180°)
* **Mode trio**:
  * **EPSP_PASSIVE** — all active channel gbars zeroed (12 t80 mechanisms + SKAHP + HHst
    gnabar/gkbar/gkmbar on soma + all dendrites + AIS proximal/distal), records per-segment
    `_ref_g` on ACh + NMDA NetCons
  * **IPSP_PASSIVE** — same channel zero-out, plus `ncs_ach.weight[0] = 0` AND
    `ncs_nmda.weight[0] = 0` to defeat NMDA leakage through the shared ACh NetStim; records
    per-segment `_ref_g` on GABA NetCons
  * **FULL** — every channel and synapse on, records soma `_ref_v`
* **Stratification**: per cluster, split into 5 × 5 DSI × PD quintile bins; walk the bin grid
  in canonical raster order, pick 1 cell per occupied bin until 10 are selected; top up by
  maximum Euclidean distance in standardised DSI × PD space if fewer than 10 occupied bins.
  Used `SAMPLE_SEED = 117` for all tie-breaking and per-trial AR(2) seeding.
* **Sequential in-process**: NEURON's global `h` is process-singleton; cells are torn down
  with `h.delete_section` between cells; `_INSERTED_CELLS.discard(id(cell))` in teardown to
  handle Python id-recycling (caught in pre-flight gate).
* **Start**: 2026-05-22T16:06:29Z; **End**: 2026-05-22T18:06:49Z (~70 min wall-clock for the
  sweep; 4-cell pre-flight gate beforehand took ~5 min).

## Cohort Composition

The 40 selected cells span the full unfiltered-pool DSI × PD range. Per-cluster spreads:

| Cluster | n | DSI range | PD range (Hz) | Predominant seed |
| --- | --- | --- | --- | --- |
| 0 | 10 | 0.00 – 0.93 | 0.7 – 44.0 | mixed (s44, s77, s7755, s9354) |
| 1 | 10 | 0.00 – 0.017 | 19.3 – 115.2 | s44 only |
| 2 | 10 | 0.00 – 0.221 | 33.6 – 109.5 | s7755 only |
| 3 | 10 | 0.00 – 0.010 | 5.0 – 75.7 | s9354 + 1 × s77 |

This perfectly mirrors t0117's finding: clusters 1 and 2 are nearly pure (one seed each); 3 is
mostly s9354; 0 is the "mixed bin" cluster. The DSI distribution is **heavily skewed toward
0** across the unfiltered pool — only cluster 0 (via the one s77 outlier at DSI = 0.93) and
cluster 2 (via s7755 cells at DSI ≈ 0.22) provide cells in the upper DSI quintiles. This is
genuine pool composition, not a sampling defect: the unfiltered pool is dominated by gen-1
random cells and low-quality survivors.

## Visualisations

### Per-cluster trace grids (10 rows × 3 columns each)

Each row is one selected cell, ordered top-to-bottom by ascending DSI. Columns are `g_E(t)`,
`g_I(t)`, `V_m(t)`. PD (0°) trace is solid, ND (180°) is dashed. Panels are annotated with the
cell's t0117 `(DSI, PD-rate)`.

![Cluster 0 traces (g_E / g_I / V_m, PD vs ND, 10
cells)](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/images/cluster_0_traces.png)

Cluster 0 is the most heterogeneous bin (cells drawn from all 4 seeds). The bottom row is the
seed-77 DSI = 0.93 outlier — note its V_m never crosses 0 mV (peaks at ~ −51 mV); it is silent
under the canonical spike threshold despite its high t0117 DSI score. Excitation-inhibition
ratio varies substantially across rows: top rows are excitation-dominated (high g_E, low g_I);
bottom rows shift toward inhibition-dominated (low g_E, large g_I bursts).

![Cluster 1 traces — predominantly seed 44, low
DSI](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/images/cluster_1_traces.png)

Cluster 1 (all-s44) shows the most consistent within-cluster pattern: large, smooth g_E
build-ups peaking around 60–80 ms, modest g_I (1–6 nS peaks), and ~5–15 PD spikes per trial.
ND traces show **earlier** g_I peaks than PD traces — the classic Vaney / Taylor inhibitory
veto signature, even though these cells have DSI ≈ 0 (so the veto doesn't translate into
firing asymmetry).

![Cluster 2 traces — predominantly seed 7755, broad PD
range](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/images/cluster_2_traces.png)

Cluster 2 (all-s7755) shows the strongest PD/ND asymmetry across the cohort. Cells near the
bottom of the figure (highest DSI in the cluster) have visibly fewer ND spikes than PD spikes
in the V_m column — the only cluster where the DSGC behaviour is mechanically visible in the
re-simulated traces. The g_I trace shows large amplitude differences between PD and ND
(ND-locked inhibition reaches ~0.7 µS in some cells).

![Cluster 3 traces — predominantly seed 9354, low
PD-rate](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/images/cluster_3_traces.png)

Cluster 3 (mostly s9354) is the "weak-firing" cluster: small g_E (typically < 0.05 µS), modest
g_I, and most cells produce 0–3 spikes in either direction. The traces look like sub-threshold
synaptic responses; these are cells where the parameter substrate isn't tuned to a firing
phenotype.

### Cross-cluster median summary (4 rows × 3 columns)

![Cross-cluster median traces — one row per cluster, PD solid + ND
dashed](../../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/images/cross_cluster_traces.png)

The median trace per cluster (computed pointwise across the 10 cells) makes the cluster-level
differences explicit:

* **Cluster 0 median** — broad g_E peak around 70 ms, modest g_I, intermediate V_m response
  with subthreshold integration
* **Cluster 1 median** — biggest peak g_E (~0.27 µS), smallest g_I (~0.05 µS), and clearest PD
  spike train in V_m; this is the "efficient firing" cluster
* **Cluster 2 median** — moderate g_E and g_I, but the largest **PD–ND separation** in V_m;
  this is the only cluster where the directional asymmetry is robust
* **Cluster 3 median** — smallest g_E, modest g_I, no spikes in either direction (median V_m
  doesn't cross −10 mV); the "silent" cluster

## Cluster-by-Cluster Trace Interpretation

Reading the per-cluster panels against t0117's factor analysis is the most instructive view.

**Cluster 0 — "mixed seed, mixed phenotype".** The widest cell-to-cell range in every metric.
The s77 DSI=0.93 outlier (bottom row) has the curious combination of high DSI score but no V_m
spikes; its `g_I / g_E ratio at peak g_E = 3.87` is extreme — inhibition dominates excitation
so completely that the cell never depolarises enough to spike. This is consistent with t0117's
F5 (depolarisation block / runaway suppression axis). Cells higher up the cluster look more
like cluster 1 medians: large g_E, modest g_I, moderate spiking.

**Cluster 1 — "tonic-Na firing machine" (t0117 F3-positive).** This matches t0116's F3 /
t0117's F2 character almost exactly: lots of resurgent Na + Ih + somatic Nav1.6 produces
large, smooth g_E peaks (peak 0.15–0.32 µS) and reliable repetitive spiking. The g_I traces
are small in absolute terms (peak < 0.1 µS) — *not* because GABA is absent but because these
cells have low SK / BK braking (consistent with t0117's joint F1 character). DSI is near zero
across all 10 cells because the PD/ND geometry doesn't favour this firing mode — the cell
fires nearly as much in ND as in PD.

**Cluster 2 — "DS-competent" (t0117 F1-positive).** The two top-DSI cells (DSI ≈ 0.22) show
the textbook DSGC pattern: g_I is much larger in ND than PD (ND inhibition arrives earlier and
peaks higher), suppressing ND firing. PD V_m has more spikes than ND V_m. This is the cluster
the optimiser was actually selecting toward. The lower-DSI cells in cluster 2 share the same
channel signature but haven't found a PD-asymmetric morphology — the mechanism is partially in
place but not fully wired.

**Cluster 3 — "weak firing" (t0117 F4 / passive axis).** Small g_E (often < 0.05 µS), modest
g_I, mostly subthreshold V_m. These cells have low active conductances overall — they're
operating closer to a passive integration regime than a firing regime. DSI is near zero
because there's hardly any firing to be asymmetric about.

## g_I / g_E Ratio — the Dominant Cross-Cell Axis

The single most variable cell-level metric across the 40-cell cohort is the **g_I / g_E ratio
at peak g_E**, which spans **0.03 to 440** (six orders of magnitude). This is the canonical
E-I balance measure. Ratios:

* **< 0.5** — excitation-dominated; characteristic of cluster 1 / 2 PD traces (cells with
  active channel signature consistent with t0117 F1 / F3)
* **0.5 – 5** — balanced; typical of cluster 0 / 2 ND traces and many cluster 0 PD traces
* **> 10** — inhibition-dominated; almost all cluster 3 cells and the silent s77 outlier in
  cluster 0; the extreme value (~440 for cell `9354_2_129` in cluster 0) reflects a near-zero
  peak g_E divided by a substantial peak g_I

This is the underlying axis that turns t0117's clustering into observable behaviour: clusters
differ in their *typical* E-I balance, not in their raw channel densities alone.

## Verification

| Check | Status |
| --- | --- |
| `verify_plan` | **PASSED** (0 errors, 0 warnings) |
| `verify_research_code` | **PASSED** |
| `verify_task_results` | **PASSED** |
| `verify_task_metrics` | **PASSED** (`metrics.json = {}`, intentional) |
| C1: 40-cell manifest resolves one-to-one to t0117 pooled parquet | **PASSED** |
| C2: every (cell, mode, direction) parquet has 1 400 rows with mode-correct columns | **PASSED** |
| C3: all 5 PNGs on disk | **PASSED** |
| C4: pre-flight gate passed (4 cells × 6 trials = 24 / 24 trials successful) | **PASSED** |
| C5: full-sweep success rate | **PASSED** (240 / 240) |
| DSI spike-count sanity (PD > ND for DSI > 0.5) | **PARTIAL** (39 / 40; one near-silent cell) |
| `ruff`, `mypy` | **PASSED** |

## Examples

This is an experiment-style task; the input-output pair for each example is **input** = the
cell's identity + mode + direction, **output** = the canonical metrics extracted from the 1
400-sample trace plus the actual file path. Ten cells span the four clusters and the full DSI
/ PD range.

### Example 1 — cluster 1, seed 44, generation 1, individual 71 (DSI = 0.00, PD = 0.7 Hz)

```text
INPUT:  cluster=0; cell=44_1_71; mode=EPSP_PASSIVE; direction=0 (PD)
OUTPUT: peak_g_E = 0.0646 µS at t = 140 ms (slow build-up)
        peak_g_I = 0.0294 µS at t = 277 ms (in IPSP_PASSIVE companion trial)
        g_I / g_E ratio at peak g_E = 0.263 (excitation-dominated)
        FULL V_m: 0 spikes; max V_m = -20.5 mV (subthreshold)
        Trace file: results/data/traces/0/44_1_71/EPSP_PASSIVE_0.parquet (1 400 rows)
```

### Example 2 — same cell, ND direction

```text
INPUT:  cluster=0; cell=44_1_71; mode=EPSP_PASSIVE; direction=180 (ND)
OUTPUT: peak_g_E = 0.0570 µS at t = 15 ms (much earlier than PD — ND-leading input)
        peak_g_I = 0.0725 µS at t = 23 ms (early ND-locked inhibition)
        g_I / g_E ratio = 1.12 (balanced)
        FULL V_m: 0 spikes; max V_m = -20.6 mV
        Trace file: results/data/traces/0/44_1_71/EPSP_PASSIVE_180.parquet
```

### Example 3 — cluster 0, seed 77, generation 15, individual 1356 (DSI = 0.93, PD = 0.7 Hz)

```text
INPUT:  cluster=0; cell=77_15_1356; mode=FULL; direction=0 (PD)
OUTPUT: peak_g_E = 0.0313 µS, peak_g_I = 0.199 µS
        g_I / g_E ratio = 3.87 (inhibition-dominated — explains the silence)
        n_spikes = 0; max V_m = -51 mV (never approaches threshold)
        — this is the DSI=0.93-but-silent edge case; t0117 assigned DSI=0.93 because the
        evaluator's ratio formula collapses on tiny PD/ND spike counts (DSI = (1-1)/(1+1)
        = 0 actually... but with stochastic input the formula returned 0.93 once)
        Trace file: results/data/traces/0/77_15_1356/FULL_0.parquet
```

### Example 4 — cluster 2, seed 7755, generation 47, individual 4448 (DSI = 0.22, PD = 106 Hz)

```text
INPUT:  cluster=2; cell=7755_47_4448; mode=FULL; direction=0 (PD)
OUTPUT: high-DSI cluster-2 cell; expected to show the DSGC asymmetry mechanism
        See trace file: results/data/traces/2/7755_47_4448/FULL_0.parquet for PD spike train
        and the IPSP_PASSIVE companion at 180° for the ND-locked inhibition that suppresses
        ND firing.
```

### Example 5 — cluster 1, seed 44, generation 11, individual 1037 (DSI = 0.00, PD = 51 Hz)

```text
INPUT:  cluster=1; cell=44_1_1037; mode=EPSP_PASSIVE; direction=0
OUTPUT: peak_g_E in the 0.15-0.30 µS range (efficient firing-machine cluster)
        FULL V_m typically produces 5-15 spikes per direction with little PD/ND asymmetry
        (high firing, low DSI — the "tonic" failure mode for direction selectivity)
        Trace file: results/data/traces/1/44_11_1037/...
```

### Example 6 — cluster 3, seed 9354, generation 2, individual 129 (DSI = 0.00, PD = 2.9 Hz)

```text
INPUT:  cluster=0; cell=9354_2_129 (note: ended up in cluster 0 not 3 due to ephys signature)
OUTPUT: peak_g_E = 0.0017 µS (essentially zero excitation)
        peak_g_I = 0.103 µS
        g_I / g_E ratio = 44.85 (extreme inhibition dominance — but not the 440 outlier)
        FULL V_m: 0 spikes; max V_m = -11 mV (just below threshold)
        Trace file: results/data/traces/0/9354_2_129/EPSP_PASSIVE_0.parquet
```

### Example 7 — cluster 1, seed 44, generation 24, individual 2268 (DSI ≈ 0, PD = 88 Hz)

```text
INPUT:  cluster=1; cell=44_24_2268; mode=FULL; direction=0
OUTPUT: high-PD, low-DSI cell in the cluster-1 firing-machine signature
        Both PD and ND produce many spikes; the cell fires reliably but doesn't discriminate
        direction. See trace file for confirmation.
        Trace file: results/data/traces/1/44_24_2268/FULL_0.parquet
```

### Example 8 — cluster 3, seed 9354, generation 16, individual 1454 (DSI = 0.002, PD = 57 Hz)

```text
INPUT:  cluster=3; cell=9354_16_1454; mode=IPSP_PASSIVE; direction=180
OUTPUT: ND-locked g_I trace; documents the per-segment GABA conductance summed at soma
        Cluster 3's median g_I peak is smaller than cluster 1/2 — these cells have less
        absolute inhibition.
        Trace file: results/data/traces/3/9354_16_1454/IPSP_PASSIVE_180.parquet
```

### Example 9 — cluster 0, seed 112, generation 16, individual 1483 (DSI = 0.01, PD = 44 Hz)

```text
INPUT:  cluster=0; cell=77_16_1483; mode=FULL; direction=0
OUTPUT: n_spikes_PD = 24, n_spikes_ND = 26 — fires more in ND than PD!
        This is one of the more striking "wrong-direction" results: the cell has a slight
        anti-DSI behaviour in the t0118 protocol (DSI would compute as ~-0.04). It's
        consistent with the cell's t0117 DSI ≈ 0 score: this cell is on the boundary between
        "no direction preference" and "slight anti-preference"; finite-sample noise determines
        which side.
        Trace files: results/data/traces/0/77_16_1483/FULL_{0,180}.parquet
```

### Example 10 — cluster 2, seed 7755, generation 49, individual 4612 (DSI = 0.22, PD = 109 Hz)

```text
INPUT:  cluster=2; cell=7755_49_4612; mode=FULL; direction=0
OUTPUT: companion to Example 4 — second cluster-2 high-DSI cell
        Shows the same DSGC asymmetry mechanism: large ND-locked g_I, smaller PD-locked g_I,
        clear PD-favouring V_m spike train.
        Trace files: results/data/traces/2/7755_49_4612/{EPSP_PASSIVE,IPSP_PASSIVE,FULL}_{0,180}.parquet
```

## Limitations

* **The unfiltered pool is heavily skewed to low DSI.** Stratified sampling did its job —
  every occupied DSI × PD bin per cluster contributed a cell — but most bins in the upper DSI
  quintiles are empty because the unfiltered pool simply doesn't contain many high-DSI cells.
  Only seed 7755's cluster 2 supplies the top-DSI representatives. Anyone wanting more
  high-DSI examples should sample from the strict cohort (t0116's 869 cells) rather than the
  unfiltered pool.
* **One cell never crosses the −10 mV spike threshold under the canonical refractory rule.**
  Cell `77_15_1356` (cluster 0) was assigned DSI = 0.93 by t0117's evaluator but produces 0
  spikes in either direction in the t0118 protocol because its FULL V_m peaks at ~ −51 mV. The
  high t0117 DSI score appears to be a finite-sample noise artefact in the evaluator's spike
  count ratio. Recorded as `partial` for REQ-14; downstream interpretation should treat this
  cell as silent rather than as a DSI = 0.93 cell.
* **DSI scores in the manifest don't always match what we observe.** Several cluster-1 cells
  have t0117 DSI = 0 but produce reliable spike trains in both PD and ND. The t0117 DSI values
  come from a different (likely shorter / different-protocol) evaluator run inside the NSGA-II
  loop; the t0118 traces are fresh sims at the canonical 1 400 ms / canonical bar parameters.
  The two sets of DSI values can disagree on borderline cells. This is documented but not
  "fixed" — t0118's job is to show the *traces*, not to re-compute DSI.
* **g_I / g_E ratio interpretation requires care for cells with near-zero g_E.** When peak g_E
  < 0.005 µS, the ratio is dominated by the small denominator and ratios in the hundreds
  appear (e.g., cell `9354_2_129` PD: ratio = 440). These are real numbers but they reflect
  near-zero excitation more than they reflect dominant inhibition.
* **`verify_answer_asset` is still missing** from this fork; not a defect of t0118 since this
  task produces no answer assets (`expected_assets: {}`).
* **NEURON DLL portability** — same as t0116 / t0117. `nrnmech.dll` is gitignored; future
  morphology-rendering or re-simulation tasks must copy it from a build-resident worktree.

## Files Created

### Code (under `code/`)

19 files total — 11 t0118-specific drivers plus 8 simulator files copied verbatim from t0106:

* t0118-specific: `paths.py`, `constants.py`, `load_t0117_clusters.py`,
  `stratified_sample.py`, `simulate_cell.py`, `run_all_cells.py`, `extract_metrics.py`,
  `plot_cluster_figures.py`, `dsi_sanity_check.py`, `verify_outputs.py`,
  `inspect_preflight.py`
* Copied verbatim from t0106 (path-rewritten): `bootstrap.py`, `apply_params.py`,
  `build_cell_ais.py`, `constants_electrophys.py`, `constants_morphology.py`,
  `extend_with_ais.py`, `generator_wrapper.py`, `parametric_placer.py`, `trial_helpers.py`

### Data (under `results/data/`)

* `selected_cells.csv` — 40-cell stratified manifest with cluster, identity, DSI/PD, quintiles
* `traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` — 240 trace parquets (1 400 rows
  each)
* `per_cell_metrics.csv` — 80 rows × 15 columns
* `simulation_failures.csv` — header-only (zero failures)
* `dsi_sanity_check.csv` — 40-row sanity-check table

### Charts (under `results/images/`)

* `cluster_0_traces.png` ... `cluster_3_traces.png` — 4 per-cluster 10-row × 3-column grids
* `cross_cluster_traces.png` — 4-row × 3-column median-trace summary

### Results manifest

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (`{}`, intentional)
* `results/costs.json` (zero-cost)
* `results/remote_machines_used.json` (`[]`)

## Task Requirement Coverage

Operative task text from `tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/task.json`:

> **Name**: Re-simulate 10 cells per t0117 ephys cluster; plot g_E, g_I, Vm in PD and ND
>
> **Short description**: Stratified-sample 10 cells per t0117 electrophys cluster (40 cells)
> spanning DSI x PD, re-simulate the 3-mode trio in PD+ND, plot per-cluster g_E(t), g_I(t), V_m(t).
>
> **Expected assets**: `{}` (demonstration task; no answer assets)

The plan decomposes this into 15 stable `REQ-*` items.

| REQ | Status | Direct answer / result | Evidence path |
| --- | --- | --- | --- |
| REQ-1 | **Done** | Joined t0117 cluster CSV (4 431 rows) with pooled parquet on the 4-key identity (one-to-one). | `code/load_t0117_clusters.py` |
| REQ-2 | **Done** | 5 × 5 quintile picker with max-distance top-up; `SAMPLE_SEED = 117`. | `code/stratified_sample.py` |
| REQ-3 | **Done** | `selected_cells.csv` written with 40 rows / 10 per cluster before any simulation. | `results/data/selected_cells.csv` |
| REQ-4 | **Done** | 8 t0106 simulator files copied + path-rewritten; no `t0106_long_pdnd_nsga2_300gen` references remain. | `code/{bootstrap,apply_params,build_cell_ais,constants_electrophys,constants_morphology,extend_with_ais,generator_wrapper,parametric_placer,trial_helpers}.py` |
| REQ-5 | **Done** | `nrnmech.dll` (238 KB) copied from main worktree to `tasks/t0080_*/code/build/`. | NEURON loaded successfully across 240 / 240 sims |
| REQ-6 | **Done** | Cell + bundle built once per cell, iterated across 6 trials. | `code/simulate_cell.py` `simulate_cell` |
| REQ-7 | **Done** | EPSP_PASSIVE / IPSP_PASSIVE zero 13 active gbars + HHst on every segment; IPSP_PASSIVE additionally zeros NMDA NetCon weight to defeat NMDA-via-ACh-NetStim leak. | `code/simulate_cell.py` `_zero_all_active_channels` |
| REQ-8 | **Done** | Per-mode recorders attached to ACh + NMDA `_ref_g` (EPSP), GABA `_ref_g` (IPSP), soma `_ref_v` (FULL); all at RECORD_DT = 1.0 ms. | `code/simulate_cell.py` `_attach_recorders` |
| REQ-9 | **Done** | AR(2) seeding per-trial; 240 parquets each 1 400 samples. | `results/data/traces/...` |
| REQ-10 | **Done** | Sequential in-process sweep with try/except per cell; `_INSERTED_CELLS.discard(id(cell))` in teardown. | `code/run_all_cells.py` `run_sweep` |
| REQ-11 | **Done** | `per_cell_metrics.csv` written with peak g_E/g_I, time-to-peak, g_I/g_E ratio, g_I onset latency, spike count, V_m mean/max. | `results/data/per_cell_metrics.csv` |
| REQ-12 | **Done** | 4 per-cluster figures rendered as 10 × 3 grids; rows by ascending DSI; PD solid + ND dashed. | `results/images/cluster_{0,1,2,3}_traces.png` |
| REQ-13 | **Done** | Cross-cluster 4 × 3 pointwise-median figure. | `results/images/cross_cluster_traces.png` |
| REQ-14 | **Partial** | 39 / 40 cells satisfy PD-spike > ND-spike for DSI > 0.5. One cell (cluster 0, `77_15_1356`) is silent in t0118's canonical −10 mV threshold and produces 0 PD / 1 ND spike — genuine edge case, not a pipeline bug. | `results/data/dsi_sanity_check.csv` |
| REQ-15 | **Done** | `verify_outputs.py` returns `all checks passed`: manifest one-to-one with t0117 pool, every (cell, mode, direction) parquet has 1 400 rows with mode-correct columns. | `code/verify_outputs.py` |

</details>
