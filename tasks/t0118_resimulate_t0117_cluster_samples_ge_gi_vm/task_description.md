# Re-Simulate 10 Cells per t0117 Electrophys Cluster — g_E, g_I, V_m in PD and ND

## Motivation

t0117 partitioned the 4 431-cell unfiltered pool into 4 electrophys clusters (k = 4, mean silhouette
= 0.158, NMI vs seed = 0.562) using only standardised 54-d electrophys features and the 68-d KMeans
centroid distances. The clusters separate cells by their channel-density signature, but t0117 never
re-simulated cells from each cluster to show what those electrophysiological differences look like
in *measured biophysical traces*. This task closes that gap by taking 10 representative cells per
cluster, re-running the canonical DSGC simulation protocol on each in PD and ND directions, and
producing per-cluster figures of excitatory and inhibitory conductance plus somatic membrane
potential.

The cells must **span DSI and PD-rate** within each cluster — not just the high-quality corner —
so the reader can see *how* the cluster's channel signature interacts with the firing output across
the full quality range that ended up in that cluster.

## Scope

### Cell selection (40 cells total: 10 per cluster × 4 clusters)

Source data:
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/electrophys_clusters.csv`
(cluster assignments) and
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet` (the 68-d
feature vector and DSI / PD values per cell).

**Stratified DSI × PD sampling per cluster**:

1. For each cluster `c ∈ {0, 1, 2, 3}`, take all its cells and split them into 5 DSI quintiles ×
   5 PD quintiles (25 bins).
2. Walk the 25 bins in canonical raster order and pick **one cell per occupied bin** until 10 are
   selected. Prefer bins that span the full DSI × PD range over re-picking from well-covered bins.
3. If fewer than 10 occupied bins exist in a cluster (likely for cluster 1 — t0117 mostly
   high-DSI/high-PD seed-7755 cells), top up by adding the next-most-distant cell (max Euclidean
   distance in standardised DSI × PD space from the already-selected set) until 10 are picked.
4. Use a fixed random seed (`SAMPLE_SEED = 117`) for any tie-breaking. Record every selected cell to
   `results/data/selected_cells.csv` with columns
   `cluster_id, source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, dsi_quintile, pd_quintile`.

The 40 selected cells must be saved as a manifest before any simulation begins so the selection is
fully reproducible from the manifest alone.

### Simulation protocol (per cell)

For every selected cell, reconstruct the cell from its 68-d parameter vector using the
project-standard procedural morphology generator (`procedural_dsgc_morphology_generator_fix` from
t0092, with the same `morph_seed` normalisation as t0116/t0117) and run the canonical mode trio in
PD and ND directions:

* **EPSP_PASSIVE** — HH off, only excitatory (ACh + glutamate / NMDA) synapses active. Records
  `g_E(t)` per direction.
* **IPSP_PASSIVE** — HH off, only inhibitory (GABA) synapses active. Records `g_I(t)` per
  direction.
* **FULL** — HH on, all synapses active. Records somatic `V_m(t)` per direction.

3 modes × 2 directions × 40 cells = **240 NEURON runs** total.

Use the project-standard trial length of **1 400 ms** (per the DSGC measurement protocol established
in t0065 / t0066 and confirmed throughout the t0080+ run series), bar-motion parameters consistent
with the source NSGA-II runs (t0106 / t0114 / t0115 evaluation protocol — read t0080's library and
t0106's plan to confirm exact bar speed, width, and spatial extent), and identical `morph_seed` per
cell across modes so the morphology is deterministic.

If any simulation fails (NEURON crash, silent cell, parameter-bounds violation), record the failure
in `results/data/simulation_failures.csv` and continue with the remaining cells. Substitute the
next-best stratified candidate from the same cluster only if a cell fails; do not re-sample without
recording the substitution.

### Outputs

#### Trace storage

For each (cell, mode, direction) triple, save:

* `results/data/traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` with columns
  `t_ms, g_e_us, g_i_us, v_m_mv` (whichever are recorded for that mode; columns not recorded in that
  mode are absent).
* Where `<cell_key> = <seed>_<generation>_<individual_idx>`.

#### Per-cluster summary figures

One figure per cluster, saved to `results/images/cluster_<c>_traces.png`. Layout: a 10-row ×
3-column grid where each row is one cell, columns are `g_E(t)`, `g_I(t)`, `V_m(t)`. Within each
panel, plot PD and ND traces in two distinguishable colours (PD solid, ND dashed) with the cell's
`(DSI, PD_rate)` annotated in the panel corner. Y-axis units: μS for conductances, mV for V_m.
X-axis: time in ms, full 1 400 ms window.

Cells are ordered top-to-bottom within each cluster by **DSI ascending**, so the reader can read the
variability gradient at a glance.

#### Cross-cluster comparison figure

A 4-row × 3-column summary figure `results/images/cross_cluster_traces.png`. Each row is one
cluster's *median* trace within the row (median over the 10 cells of that cluster); columns are
`g_E`, `g_I`, `V_m`. PD and ND overlaid as before. This gives a single-glance summary of how the
four electrophys clusters differ in their canonical conductance and V_m signatures.

#### Per-cell metric extraction

For every cell, compute and emit to `results/data/per_cell_metrics.csv` the following per-direction
quantities (rows = (cell, direction); columns include the cell identifiers plus the metrics):

* Peak g_E and time-to-peak (ms)
* Peak g_I and time-to-peak (ms)
* g_I / g_E ratio at peak g_E (the canonical excitation-inhibition balance)
* g_I onset latency (time from stimulus onset to half-rise of g_I)
* Number of spikes in `V_m` (count crossings of −10 mV with refractory ≥ 2 ms)
* Mean and max V_m during the 1 400 ms window

These extracted metrics let downstream tasks build comparative tables without re-loading the parquet
trace files.

### Key questions (each becomes one `assets/answer/` asset)

This task does NOT produce answer assets in the canonical ARF sense — its output is a
demonstration / exploratory artefact, not a question-answering artefact. `expected_assets` in
`task.json` is therefore `{}`. The figures and per-cell metrics are the deliverables; interpretation
lives in `results_detailed.md` `## Analysis`.

## Approach

### Code reuse

* **NEURON model and simulator entrypoint**: the implementation must locate the canonical Bed B +
  morphology DSGC simulation library used by t0106 / t0112 / t0114 / t0115. The research-code step
  is responsible for identifying the right entrypoint (likely in
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/` or a registered library asset under
  `tasks/t0080_*/assets/library/`) and the canonical mode-trio invocation.
* **Morphology generator**: `generate_fixed_morphology` from
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix`.
* **68-d parameter unpacking**: reuse the constants and parameter unpacking from
  `tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` `ALL_PARAM_NAMES` — same layout
  as t0116 / t0117.

Per the cross-task import rule, any non-library code from these source tasks must be **copied into
`tasks/t0118_*/code/`** rather than imported.

### Pipeline structure

* `code/load_t0117_clusters.py` — load t0117's cluster assignments and the parameter vectors
* `code/stratified_sample.py` — implement the DSI × PD stratified picker; write
  `results/data/selected_cells.csv`
* `code/simulate_cell.py` — single-cell driver: take a parameter vector, build the cell, run the
  3-mode trio in PD+ND, save traces to parquet
* `code/run_all_cells.py` — top-level driver that iterates over the 40 cells (sequentially or with
  `concurrent.futures.ProcessPoolExecutor` if isolation is solid; NEURON's globalness may force
  sequential)
* `code/extract_metrics.py` — read all trace parquets, compute the per-direction metrics, write
  `results/data/per_cell_metrics.csv`
* `code/plot_cluster_figures.py` — produce the 4 per-cluster figures and the cross-cluster summary

### Sequential vs parallel

NEURON is famously not process-safe inside a single Python session due to global state in the `h`
instance. The default is sequential simulation (1 cell at a time, ~10–30 s per cell for the 3-mode
trio in 2 directions, ~20–45 min total). If the implementation finds that each cell can be wrapped
in its own subprocess via `concurrent.futures.ProcessPoolExecutor` without state bleed, that's
allowed but must be validated by comparing a small parallel batch against the sequential reference.
**Do not commit to parallel without validation.**

## Expected Outputs

### Assets

None (`expected_assets: {}`). This is a demonstration task.

### Tables (under `results/data/`)

* `selected_cells.csv` — the 40-cell stratified sample manifest (committed before sims start)
* `per_cell_metrics.csv` — peak conductances, latencies, spike counts, V_m extrema per cell per
  direction
* `simulation_failures.csv` — any NEURON errors or silent-cell failures encountered
* `traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` — 480 trace files total (40 cells ×
  3 modes × 2 directions, but `g_E` / `g_I` / `V_m` columns vary by mode)

### Charts (under `results/images/`)

* `cluster_0_traces.png` ... `cluster_3_traces.png` — 4 per-cluster 10-row × 3-column trace grids
* `cross_cluster_traces.png` — 4-row × 3-column median-trace summary

### Optional analysis blocks in `results_detailed.md`

* `## Analysis` — per-cluster interpretation of how the conductance and V_m signatures differ.
  Connect findings back to t0117's F1 / F3 / F5 factor structure where possible (e.g., "cluster 1
  cells show large peak `g_E` consistent with low SK_AIS density — this is the F1 axis Sthe
  high-DSI corner of t0117 sits on").

## Compute and Budget

CPU-only, local NEURON. No remote machines. No paid APIs. `total_cost_usd: 0`.

Wall-clock estimate: **30–60 minutes**. Each cell needs ~10–30 s for the 3-mode trio in 2
directions (1 400 ms simulated time × 3 modes × 2 dirs × per-step integration overhead).
Sequential 40 cells = 7 – 20 min for simulation + ~5 min for plotting and metric extraction.

## Cross-References

* **Source data**: t0117 (cluster assignments + parameter vectors)
* **Simulation infrastructure**: t0080 (BedB+morph simulator), t0090 / t0092 (morphology generators)
* **Measurement protocol**: the DSGC measurement-protocol convention established across t0065 /
  t0066 (EPSP_PASSIVE / IPSP_PASSIVE / FULL trio, 1 400 ms trial length, HH off for passive traces)
* **Cohort context**: t0116 (strict-cohort version of the parent analysis); t0117's three answer
  assets for the broader interpretation of the cluster structure

## Verification Criteria

* `selected_cells.csv` contains exactly 40 rows (10 per cluster) and every cell's
  `(seed, generation, individual_idx)` triple maps back to a unique row in
  `tasks/t0117_*/data/pooled_all_cells.parquet`.
* Every selected cell has at least one trace file per (mode, direction); any missing combinations
  must be recorded in `simulation_failures.csv` with a stated reason.
* Each per-cluster figure renders 10 rows × 3 columns of non-empty traces (or annotated failure
  placeholders for any simulation that failed).
* The cross-cluster summary figure renders 4 rows × 3 columns with all panels populated.
* Every trace parquet has at least 1 400 ms of samples at the simulator's default dt (typically
  0.025 ms → ~56 000 rows).
* PD direction must produce more spikes than ND in `V_m` for cells with `dsi_vector_sum > 0.5`
  (sanity check; cells with DSI ≤ 0.5 may not respect this).
