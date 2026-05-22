---
spec_version: "2"
task_id: "t0118_resimulate_t0117_cluster_samples_ge_gi_vm"
date_completed: "2026-05-22"
status: "complete"
---
# t0118 — Re-Simulate 10 Cells per t0117 Cluster (g_E, g_I, V_m, PD + ND) Plan

## Objective

Stratified-sample 40 representative cells from the four t0117 electrophys clusters (10 per cluster,
spanning the full DSI × PD-rate quality range) and re-simulate each cell on the canonical Bed B +
procedural-morphology DSGC substrate in PD (0°) and ND (180°) directions under the canonical
three-mode trial trio (EPSP_PASSIVE, IPSP_PASSIVE, FULL). Record per-synapse total excitatory
conductance `g_E(t)`, total inhibitory conductance `g_I(t)`, and somatic membrane potential
`V_m(t)`. Save 240 trace parquets (40 cells × 3 modes × 2 directions), compute per-cell summary
metrics (peak conductances, latencies, g_I / g_E ratio, spike counts, V_m extrema), and render four
per-cluster 10 × 3 trace grids plus one cross-cluster 4 × 3 median-trace summary. Done = the
selected-cells manifest exists on disk before any simulation, every selected cell has at least one
trace parquet per (mode, direction) or a recorded failure, all five trace figures render to
`results/images/`, `per_cell_metrics.csv` covers every (cell, direction) pair, and the sanity check
`PD spike count > ND spike count for all cells with dsi_vector_sum > 0.5` passes.

## Task Requirement Checklist

Operative task text from `task.json` and `task_description.md`:

> **Name**: Re-simulate 10 cells per t0117 ephys cluster; plot g_E, g_I, Vm in PD and ND
>
> **Short description**: Stratified-sample 10 cells per t0117 electrophys cluster (40 cells)
> spanning DSI × PD, re-simulate the 3-mode trio in PD+ND, plot per-cluster g_E(t), g_I(t), V_m(t).
>
> **Source data**: `tasks/t0117_*/results/data/electrophys_clusters.csv` (cluster assignments) and
> `tasks/t0117_*/data/pooled_all_cells.parquet` (68-d vectors + DSI / PD per cell).
>
> **Sampling**: per-cluster stratified DSI × PD picker — 5 DSI quintiles × 5 PD quintiles (25
> bins), walk raster order taking one cell per occupied bin until 10 selected; if cluster has < 10
> occupied bins, top up by max-distance in standardised DSI × PD; `SAMPLE_SEED = 117` for
> tie-breaking; manifest persisted to `results/data/selected_cells.csv` before any simulation;
> columns
> `cluster_id, source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, dsi_quintile, pd_quintile`.
>
> **Simulation protocol per cell**: build cell via t0092 `generate_fixed_morphology` from the 14-d
> morphology slice, apply 54-d electrophys vector, build synapse bundle, then for each of the three
> modes (EPSP_PASSIVE = HH off + GABA silenced → record `g_E(t)`; IPSP_PASSIVE = HH off + ACh +
> NMDA silenced → record `g_I(t)`; FULL = HH on, all synapses active → record `V_m(t)`) run a PD
> trial (0°) and an ND trial (180°). 3 modes × 2 directions × 40 cells = 240 NEURON runs.
>
> **Trial length and dt**: 1400 ms simulated, dt = 0.1 ms, recording resolution RECORD_DT_MS = 1.0
> ms (1400 samples per trace).
>
> **Bar parameters**: velocity 1.0 µm/ms, width 250 µm, x_start = −40 µm, y span 25–225 µm,
> start time 0 ms — identical to t0024 / t0080 / t0106 / t0112 / t0114 / t0115.
>
> **Outputs**:
>
> * `results/data/selected_cells.csv` — 40-row manifest (10 per cluster).
> * `results/data/traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` — 240 trace files;
>   columns `t_ms, g_e_us, g_i_us, v_m_mv` with absent columns for non-recorded mode quantities.
> * `results/data/per_cell_metrics.csv` — per (cell, direction) row with peak `g_E`, peak `g_I`,
>   time-to-peak for each, g_I / g_E ratio at peak g_E, g_I onset latency (half-rise), spike count
>   (V_m crosses −10 mV with ≥ 2 ms refractory), mean and max V_m.
> * `results/data/simulation_failures.csv` — any NEURON crash, silent cell, or parameter-bounds
>   violation; columns `(cluster_id, cell_key, mode, direction, error_type, error_message)`.
> * `results/images/cluster_<c>_traces.png` for `c ∈ {0,1,2,3}` — 10-row × 3-col grids, each
>   row a cell ordered by ascending DSI, columns `g_E(t)` / `g_I(t)` / `V_m(t)`; PD solid + ND
>   dashed; cell `(DSI, PD-rate)` annotated in each panel corner; y-axis units µS / µS / mV;
>   x-axis 0–1400 ms.
> * `results/images/cross_cluster_traces.png` — 4-row × 3-col summary; each row the median trace
>   over the cluster's 10 cells; PD and ND overlaid.
>
> **Verification**: `selected_cells.csv` has exactly 40 rows (10 per cluster) and every cell's
> `(seed, generation, individual_idx)` key resolves uniquely in
> `tasks/t0117_*/data/pooled_all_cells.parquet`; every cell has at least one trace per (mode,
> direction) or a recorded failure; per-cluster figures render 10 × 3 non-empty panels;
> cross-cluster figure renders 4 × 3 panels; every parquet has at least 1400 trace samples at
> `RECORD_DT_MS = 1.0 ms` (the task description's "~56 000 rows" estimate was based on a 0.025 ms dt
> — the canonical recording resolution from t0066 / t0072 is 1.0 ms, giving 1400 samples per
> trace); PD direction produces more `V_m` spikes than ND for every cell with
> `dsi_vector_sum > 0.5`.

* **REQ-1**: Load t0117's cluster assignments from
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/electrophys_clusters.csv`
  and the 68-d feature vectors + DSI / PD-rate per cell from
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet`, joining
  on the `(source_task, seed, generation, individual_idx)` primary key into one labelled DataFrame
  ready for stratified sampling. *Satisfied by Step 3.*

* **REQ-2**: For each of the four clusters (`cluster_id ∈ {0, 1, 2, 3}`), stratified-sample 10
  cells using the DSI × PD quintile picker: bin each cluster's cells into 5 DSI quintiles × 5 PD
  quintiles (25 bins), walk in canonical raster order taking one cell per occupied bin until 10 are
  selected. If a cluster has fewer than 10 occupied bins, top up by the next-most-distant cell in
  standardised DSI × PD Euclidean space until 10 are picked. Use `SAMPLE_SEED = 117` for
  tie-breaking. *Satisfied by Step 4.*

* **REQ-3**: Write the 40-cell manifest to `results/data/selected_cells.csv` **before any simulation
  begins** so the selection is fully reproducible from the manifest alone. Columns:
  `cluster_id, source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, dsi_quintile, pd_quintile`.
  Row count must be exactly 40 (10 per cluster). *Satisfied by Step 4.*

* **REQ-4**: Copy the t0106 simulator stack into `tasks/t0118_*/code/`. Required files:
  `bootstrap.py`, `constants_electrophys.py`, `constants_morphology.py`, `extend_with_ais.py`,
  `parametric_placer.py`, `trial_helpers.py`, `generator_wrapper.py`, `apply_params.py` from
  `tasks/t0106_long_pdnd_nsga2_300gen/code/`. In each copied file replace internal references to
  `tasks.t0106_long_pdnd_nsga2_300gen.code.*` with
  `tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.*`. ~1100 lines total. *Satisfied by
  Step 5.*

* **REQ-5**: Ensure the compiled NEURON channel DLL is available at
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/nrnmech.dll` inside the worktree. The
  `build/` folder is gitignored so the DLL must either be copied from the main repo's compiled build
  folder or rebuilt via `nrnivmodl.bat` on `tasks/t0080_*/code/mods/`. *Satisfied by Step 6.*

* **REQ-6**: For each of the 40 cells, build the cell once via `generate_fixed_morphology` (from the
  t0092 `procedural_dsgc_morphology_generator_fix` library) + `insert_baseline_channels` +
  `apply_parameter_vector` from the copied `apply_params.py`, then build the synapse bundle once via
  `setup_synapses_parametric` from the copied `trial_helpers.py`. The cell + bundle are reused
  across the 6 trials (3 modes × 2 directions) for that cell. *Satisfied by Step 7.*

* **REQ-7**: Implement the three-mode trio per cell. For each mode, apply electrophys params fresh
  (call `apply_parameter_vector` again — idempotent), then apply mode-specific overrides:

  * **EPSP_PASSIVE**: zero `gbar_<suffix>` for all 12 t80 channel suffixes
    (`nav16t80, napt80, nart80, kdrt80, kv3t80, kv4t80, kv7t80, iht80, calt80, catt80, bkt80, skt80`)
    plus `gbar_skahpt80` and `HHst.gnabar/gkbar/gkmbar` on every segment of soma + all_dends +
    ais_proximal + ais_distal; zero all `ncs_gaba[i].weight[0]` to silence inhibition.

  * **IPSP_PASSIVE**: same channel zero-out as EPSP_PASSIVE; zero all `ncs_ach[i].weight[0]` AND
    `ncs_nmda[i].weight[0]` (NMDA shares the ACh NetStim so silencing only ACh leaves NMDA active).

  * **FULL**: HH on, no synapse silencing — call `apply_parameter_vector` fresh and leave all
    `NetCon.weight[0]` at their canonical values.

  *Satisfied by Step 7.*

* **REQ-8**: Per mode, attach the appropriate recorders before each trial. EPSP_PASSIVE: record
  `syns_ach[i]._ref_g` and `syns_nmda[i]._ref_g` for every Exp2Syn ACh + Exp2NMDA contact. The total
  `g_E(t)` reported in the parquet is the sum over all ACh contacts at each time point; store NMDA
  separately (per `research_code.md` recommendation 5 — record both, sum to total g_E in the
  parquet). IPSP_PASSIVE: record `syns_gaba[i]._ref_g` for every Exp2Syn GABA contact; sum to total
  `g_I(t)`. FULL: record soma `_ref_v` only. All recorders use
  `h.Vector().record(..., RECORD_DT_MS)` with `RECORD_DT_MS = 1.0` (1400 samples per 1400-ms trial).
  *Satisfied by Step 7.*

* **REQ-9**: For each (mode, direction) pair generate AR(2)-correlated release rates per the
  canonical t0106 recipe (`_rates_with_ar2_noise` in `trial_helpers.py`), seed
  `cell_seed = SAMPLE_SEED + cell_index * 10_007 + int(direction_deg) * 13` so the PD and ND traces
  of a single cell share their direction-specific noise realisation across modes, queue events via a
  `FInitializeHandler` + `NetCon.event` (the t0106 pattern), run `h.run()` and save the per-trial
  trace to `results/data/traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` where
  `<cell_key> = <seed>_<generation>_<individual_idx>`. Parquet columns: `t_ms` plus whichever of
  `g_e_us, g_i_us, v_m_mv` are recorded for that mode (absent columns omitted). *Satisfied by Step
  7.*

* **REQ-10**: Run the full 40-cell sweep sequentially in-process per `research_code.md`
  recommendation 7 (NEURON's globalness rules out naive process-pool parallelism). Between cells,
  tear down via `h.delete_section` wrapped in `contextlib.suppress(RuntimeError, AttributeError)`
  + remove from `_LIVE_CELLS` + `del cell`. Wrap each cell's six trials in a try/except for
    `(RuntimeError, ValueError, AssertionError, ArithmeticError)`; on failure, append a row to
    `results/data/simulation_failures.csv` and continue with the next cell. Do not abort the run on
    a single bad cell. *Satisfied by Step 8.*

* **REQ-11**: Extract per-cell metrics: for every (cell, direction) pair compute and write to
  `results/data/per_cell_metrics.csv`: peak `g_E` and time-to-peak (ms); peak `g_I` and time-to-peak
  (ms); g_I / g_E ratio at peak g_E (the canonical excitation-inhibition balance); g_I onset latency
  = time from `BAR_START_TIME_MS = 0` to half-rise of `g_I`; spike count = V_m crossings of −10 mV
  with refractory ≥ 2 ms; mean and max V_m across the 1400 ms window. *Satisfied by Step 9.*

* **REQ-12**: Render four per-cluster figures `results/images/cluster_<c>_traces.png` for
  `c ∈ {0, 1, 2, 3}`. Layout: 10-row × 3-col grid; each row is one cell ordered top-to-bottom by
  ascending DSI; columns are `g_E(t)`, `g_I(t)`, `V_m(t)`. Plot PD solid + ND dashed in one colour;
  y-axis units µS / µS / mV; x-axis 0–1400 ms; annotate each panel corner with the cell's
  `(DSI, PD-rate)`. *Satisfied by Step 10.*

* **REQ-13**: Render the cross-cluster summary `results/images/cross_cluster_traces.png`. Layout:
  4-row × 3-col, each row one cluster's *median* trace over its 10 cells; columns are `g_E`, `g_I`,
  `V_m`; PD and ND overlaid as in the per-cluster figures. *Satisfied by Step 10.*

* **REQ-14**: Run a quality sanity check: for every selected cell with `dsi_vector_sum > 0.5`, the
  PD `V_m` spike count must exceed the ND `V_m` spike count. Emit the per-cell pass / fail table to
  `results/data/dsi_sanity_check.csv`. Cells with DSI ≤ 0.5 are not subject to this constraint.
  *Satisfied by Step 11.*

* **REQ-15**: Manifest-resolves-to-source verification: every row of `selected_cells.csv` must
  resolve to a unique row of `tasks/t0117_*/data/pooled_all_cells.parquet` when joined on
  `(source_task, seed, generation, individual_idx)`, and every trace parquet file path on disk must
  match the canonical layout
  `results/data/traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet`. *Satisfied by Step 12.*

## Approach

The task is split into two phases. **Phase A (selection)** turns t0117's cluster assignments into a
40-cell stratified manifest using DSI × PD quintile binning per cluster. **Phase B (simulation +
analysis)** re-builds each selected cell on the canonical 68-d Bed B + procedural-morphology DSGC
substrate, runs the three-mode trial trio in PD and ND, records `g_E(t)` / `g_I(t)` / `V_m(t)`,
extracts per-cell summary metrics, and renders the per-cluster and cross-cluster figures.

**Simulator entrypoint identified in research-code**: `evaluate_68d_vector` in
`tasks/t0106_long_pdnd_nsga2_300gen/code/evaluator.py` is the canonical 68-d simulator used by
t0106, t0112, t0114, and t0115. Its dependencies (bootstrap, constants, parameter unpacking, synapse
bundling, channel insertion) live entirely inside `tasks/t0106_*/code/` and must be **copied** into
`tasks/t0118_*/code/` per the cross-task code-reuse rule. Total copy budget ~1100 lines across 8
files. The morphology builder (`generate_fixed_morphology` from t0092) and HHst inserter
(`insert_baseline_channels` from t0092) are registered library entries — those are imported, not
copied.

**Mode-trio adaptation**: t0066 owns the canonical EPSP_PASSIVE / IPSP_PASSIVE / FULL trio on the
old t0024 Bed A substrate. Its silencing logic (zero HH conductances + zero opposing-synapse
`NetCon.weight[0]`) must be adapted for the 68-d substrate's 13 active channel mechanisms (12 t80
suffixes + skahpt80 + HHst) by zeroing every active gbar on every segment of soma + all_dends +
ais_proximal + ais_distal, AND zeroing NMDA `NetCon.weight[0]` in IPSP_PASSIVE since NMDA shares the
ACh NetStim and would otherwise leak through. Per `research_code.md` recommendation 4, the mode
override is applied by **re-applying electrophys params fresh per mode** (idempotent thanks to
`_INSERTED_CELLS` guard in `apply_params.py`) and then zeroing the channels per the mode — cleaner
than snapshot-and-restore over ~250 segment-channel slots.

**Conductance recording**: per t0072's `run_bed_b.py` lines 214–248, each Exp2Syn synapse exposes
`_ref_g` in microsiemens. Total `g_E(t)` and `g_I(t)` are computed as the sum across all ACh
contacts (for `g_E`) or all GABA contacts (for `g_I`) at each recorded time point. NMDA is recorded
separately and summed into `g_E` in the parquet `g_e_us` column (NMDA is part of excitation; storing
it separately preserves the option of re-decomposing downstream).

**Recording resolution**: `RECORD_DT_MS = 1.0` ms per the t0066 / t0072 canonical convention, giving
1400 samples per 1400-ms trial. The task description's "~56 000 rows" estimate assumed `dt = 0.025`
ms recording, which is unwarranted overkill for this task. The plan corrects this to 1400 rows per
trace; the verificator check in REQ-15 verifies 1400-row minima.

**NEURON statefulness**: NEURON has process-global state via `h`. The 40 cells run sequentially
in-process with explicit teardown (`h.delete_section` + `_LIVE_CELLS.pop()` + `del cell`) between
cells, matching the t0117 morphology-rendering pattern. Subprocess parallelisation is not justified
for 40 cells (estimated 30–60 min sequential wall-clock).

**Bar-motion parameters** (from `tasks/t0024_*/code/constants.py` lines 78–84, shared across the
entire t0024 / t0080 / t0106 line): velocity 1.0 µm/ms, width 250 µm, x_start = −40 µm, y span
25–225 µm, start time 0 ms, PD = 0° / ND = 180°. The bar arrival time at synapse `i` is
`BAR_START_TIME_MS + (proj_i - BAR_X_START_UM) / BAR_VELOCITY_UM_PER_MS` where `proj_i` is the
projection of the synapse xy onto the unit vector at `direction_deg`.

**Alternatives considered**:

1. *Subprocess-parallel NEURON via `ProcessPoolExecutor`* — what t0106's NSGA-II driver uses for
   scale. Rejected for 40 cells because the wall-clock benefit is small (per-cell wall-clock is
   dominated by build + apply_params, not by `h.run()`) and the cross-process state-management
   complexity (DLL reloading per child, partial-result aggregation) is not justified at this scale.
2. *Snapshot-and-restore canonical conductance state per mode* — the t0066 pattern. Rejected
   because the 68-d substrate has 13 active mechanisms × ~200 segments = ~2600 floats per cell; the
   re-apply-fresh-per-mode alternative is cleaner, since `apply_parameter_vector` is already
   idempotent (cheap second-call cost thanks to the `_INSERTED_CELLS` guard).
3. *NSGA-II-style cross-seed re-sampling instead of cluster-stratified sampling* — would mix cells
   across clusters, defeating the per-cluster signature comparison. Rejected because the task
   explicitly demands "10 cells per cluster spanning DSI × PD".

**Task types**: `experiment-run` (the simulation runs are computational experiments with controlled
independent variables — mode + direction + cell) and `data-analysis` (the per-cell metric
extraction and figure rendering are quantitative analysis over the trace dataset). Both are already
declared in `task.json`. The experiment-run Planning Guidelines drove the explicit fixed-seed
convention (per `research_code.md` recommendation 9), the failure-tolerant per-cell wrap (REQ-10),
and the manifest-before-simulation discipline (REQ-3). The data-analysis Planning Guidelines drove
the figure-per-deliverable layout (REQ-12, REQ-13), the per-cell metrics CSV (REQ-11), and the
named-constants discipline (`SAMPLE_SEED`, `RECORD_DT_MS`, `N_CELLS_PER_CLUSTER` in
`code/constants.py`).

**Registered metrics**: the four registered project metrics (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) are **not applicable** to
this task. DSI is sourced from t0117 / t0106 (the pre-existing per-cell DSI is used only for sample
stratification, not re-measured here). Tuning curves require an angular sweep — this task runs
only two directions (PD + ND), insufficient for tuning-curve metrics. Per the planning skill rule
"do not force-fit metrics", no registered metric is written to `results/metrics.json`; the file will
be an empty JSON object `{}` per the existing step_tracker step 12 description. The per-cell metrics
live in `results/data/per_cell_metrics.csv` instead — task-specific, not project-wide.

## Cost Estimation

* LLM / API costs: **$0** — no external API calls.
* Remote compute: **$0** — local CPU-only execution on the developer's workstation.
* Storage: **$0** — 240 parquet files at ~10 KB each + 5 PNG figures + 3 CSVs fits under 5 MB.
* **Total: $0.** Project budget is $100 total / $8 per-task default; this task consumes 0% of the
  per-task default and 0% of the project total.

## Step by Step

### Milestone 1 — Project scaffolding and selection

1. **Create `code/paths.py`.** Define all path constants: `T0117_ELECTROPHYS_CLUSTERS_CSV`,
   `T0117_POOLED_PARQUET`, `T0080_DLL_WIN`, `RESULTS_DATA_DIR`, `RESULTS_IMAGES_DIR`, `TRACES_ROOT`,
   `SELECTED_CELLS_CSV`, `PER_CELL_METRICS_CSV`, `SIMULATION_FAILURES_CSV`, `DSI_SANITY_CHECK_CSV`,
   `CLUSTER_TRACES_FIGURES_TEMPLATE = RESULTS_IMAGES_DIR / "cluster_{c}_traces.png"`,
   `CROSS_CLUSTER_FIGURE = RESULTS_IMAGES_DIR / "cross_cluster_traces.png"`. Use `pathlib.Path`
   throughout. Expected: 1 new file, ~50 lines. No I/O at this step.

2. **Create `code/constants.py`.** Define: `SAMPLE_SEED = 117`, `N_CELLS_PER_CLUSTER = 10`,
   `N_CLUSTERS = 4`, `N_DSI_QUINTILES = 5`, `N_PD_QUINTILES = 5`, `RECORD_DT_MS = 1.0`,
   `DSI_SANITY_THRESHOLD = 0.5`, `SPIKE_THRESHOLD_MV = -10.0`, `SPIKE_REFRACTORY_MS = 2.0`, trace
   parquet column names (`T_MS_COL = "t_ms"`, `G_E_US_COL = "g_e_us"`, `G_I_US_COL = "g_i_us"`,
   `V_M_MV_COL = "v_m_mv"`), per-cell metric keys (`PEAK_G_E_KEY`, `PEAK_G_E_TIME_MS_KEY`,
   `PEAK_G_I_KEY`, `PEAK_G_I_TIME_MS_KEY`, `GI_GE_RATIO_AT_PEAK_GE_KEY`, `G_I_ONSET_LATENCY_MS_KEY`,
   `SPIKE_COUNT_KEY`, `MEAN_VM_KEY`, `MAX_VM_KEY`), and the `TrialMode` StrEnum (`EPSP_PASSIVE`,
   `IPSP_PASSIVE`, `FULL`) + `Direction` enum (`PD_DEG = 0`, `ND_DEG = 180`). Expected: 1 new file,
   ~80 lines. Satisfies REQ-2 / REQ-7 / REQ-9 / REQ-11 plumbing.

3. **Create `code/load_t0117_clusters.py`.** Load
   `tasks/t0117_*/results/data/electrophys_clusters.csv` (cluster assignments) and
   `tasks/t0117_*/data/pooled_all_cells.parquet` (68-d vectors + DSI / PD). Join on
   `(source_task, seed, generation, individual_idx)`. Return a `pd.DataFrame` with columns
   `cluster_id, source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz` plus all
   68 named feature columns from `ALL_PARAM_NAMES`. Use explicit dtypes per the project pandas rule.
   Assert join cardinality equals the cluster CSV row count (no orphan rows). Expected: 1 new file,
   ~80 lines. Satisfies REQ-1.

4. **Create `code/stratified_sample.py`.** Implement the DSI × PD quintile picker:

   * For each cluster, compute 5 DSI quintile edges and 5 PD quintile edges over the cluster's
     cells; assign each cell its `(dsi_quintile, pd_quintile)` bin index.
   * Walk the 25 bins in canonical raster order (DSI ascending then PD ascending) and pick one cell
     per occupied bin until 10 are selected.
   * If fewer than 10 occupied bins exist, top up using max-Euclidean-distance in standardised DSI
     × PD space from the already-selected set.
   * Use `numpy.random.default_rng(SAMPLE_SEED)` for any tie-breaking within a bin.
   * Write the 40-row manifest to `results/data/selected_cells.csv` with the column order specified
     in REQ-3.
   * Assert: exactly 40 rows; 10 per cluster; every
     `(source_task, seed, generation, individual_idx)` tuple unique.

   Expected: 1 new file, ~120 lines. Satisfies REQ-2 and REQ-3. *Run this step end-to-end before any
   simulation code — the manifest must exist on disk before Milestone 3 begins.*

### Milestone 2 — Simulator scaffolding

5. **Copy the t0106 simulator stack into `code/`.** From `tasks/t0106_long_pdnd_nsga2_300gen/code/`
   copy verbatim (~1100 lines total): `bootstrap.py`, `constants_electrophys.py`,
   `constants_morphology.py`, `extend_with_ais.py`, `parametric_placer.py`, `trial_helpers.py`,
   `generator_wrapper.py`, `apply_params.py`. Inside each copied file, replace every occurrence of
   `tasks.t0106_long_pdnd_nsga2_300gen.code.` with
   `tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.`. The library imports for
   `generate_fixed_morphology` (t0092 library) and `MorphologyParams` / `MorphologyResult` (t0090
   library) stay as cross-task library imports — these are registered libraries, not raw code
   copy. **Do not copy** `evaluator.py` or `build_cell_ais.py` from t0106; t0118 writes its own
   mode-trio driver that reuses the bundle helpers and the morphology-generated cell instead of the
   t0024 base cell. Expected: 8 new files in `code/`. Satisfies REQ-4.

6. **Pre-flight: ensure NEURON DLL is present.** Run
   `uv run python -m arf.scripts.utils.run_with_logs python -u -c "from pathlib import Path; p = Path('tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/nrnmech.dll'); assert p.exists(), f'missing {p}'"`.
   If the DLL is missing, either (a) copy the existing compiled DLL from the main repo's
   `tasks/t0080_*/code/build/nrnmech.dll` into the worktree at the same relative path, or (b)
   re-compile via `nrnivmodl.bat` run inside `tasks/t0080_*/code/mods/`. The Linux fallback
   `compile_t0080_mods_linux` is not needed on this Windows workstation. Expected: `nrnmech.dll`
   exists at `tasks/t0080_*/code/build/nrnmech.dll`. Satisfies REQ-5.

### Milestone 3 — Per-cell simulator and 40-cell sweep

7. **Create `code/simulate_cell.py`.** Per-cell driver function
   `simulate_cell(*, cell_row: pd.Series, cell_index: int) -> CellSimResult`. Logic:

   a. Bootstrap NEURON (`import tasks.t0118_*.code.bootstrap` — auto-applies NEURONHOME side
   effect).

   b. Unpack the 68-d vector into a 54-d `ParameterVector` and a 14-d `MorphologyParams` via
   `split_68d_vector` and `morphology_params_from_vector` (the copied `generator_wrapper.py`
   helpers).

   c. Build the morphology via the t0092 library import
   `generate_fixed_morphology(params=morph_params, morph_seed=morph_params.morph_seed)` then call
   `insert_baseline_channels(h=h, cell=cell)` from t0092. Apply the 54-d vector via the copied
   `apply_parameter_vector(cell=cell, params=electrophys_params)`. Append the cell to `_LIVE_CELLS`.

   d. Build the synapse bundle via the copied
   `setup_synapses_parametric(cell=cell, params=electrophys_params, n_ach=..., n_gaba=...)`.

   e. For each `mode in (EPSP_PASSIVE, IPSP_PASSIVE, FULL)`:

   * Call `apply_parameter_vector(cell=cell, params=electrophys_params)` fresh (idempotent).

   * If mode != FULL: zero `gbar_<suffix>` for every t80 suffix + skahpt80 + HHst on every segment
     of soma + all_dends + ais_proximal + ais_distal.

   * If mode == EPSP_PASSIVE: zero all `bundle.ncs_gaba[i].weight[0]`.

   * If mode == IPSP_PASSIVE: zero all `bundle.ncs_ach[i].weight[0]` AND
     `bundle.ncs_nmda[i].weight[0]`.

   * Attach recorders per mode:
     * EPSP_PASSIVE → `h.Vector().record(bundle.syns_ach[i]._ref_g, RECORD_DT_MS)` for every ACh
       synapse + same for `syns_nmda`; sum across synapses post-run to give total `g_E(t)`.
     * IPSP_PASSIVE → `h.Vector().record(bundle.syns_gaba[i]._ref_g, RECORD_DT_MS)` for every GABA
       synapse; sum to total `g_I(t)`.
     * FULL → `h.Vector().record(cell.soma(0.5)._ref_v, RECORD_DT_MS)`.
     * Always record `h._ref_t` to a shared time vector.

   * For each `direction_deg in (0.0, 180.0)`:
     - Compute `cell_seed = SAMPLE_SEED + cell_index * 10_007 + int(direction_deg) * 13`.
     - Generate AR(2) noise rates via the copied
       `_rates_with_ar2_noise(rng=np.random.default_rng(cell_seed), ...)`.
     - Compute bar arrival times via `_bar_arrival_times(direction_deg=direction_deg, ...)`.
     - Queue NetCon events via `_rates_to_events` and a `FInitializeHandler`.
     - Run `h.run()` (relies on the bootstrap's `TSTOP_MS = 1400` + `DT_MS = 0.1`).
     - Convert the per-synapse `Vector` objects to numpy, sum across synapses for `g_E` / `g_I`, and
       save the parquet to `results/data/traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet`
       with columns `t_ms` + whichever of `g_e_us, g_i_us, v_m_mv` apply.

   f. Teardown: for each section in `result.all_dends + [result.soma, ais_proximal, ais_distal]`,
   call `h.delete_section(sec=s)` wrapped in `contextlib.suppress(RuntimeError, AttributeError)`.
   Pop the cell from `_LIVE_CELLS` and `del cell`.

   Expected: 1 new file, ~280 lines. Satisfies REQ-6, REQ-7, REQ-8, REQ-9.

8. **Create `code/run_all_cells.py`.** Top-level driver. Reads `results/data/selected_cells.csv`,
   iterates row-by-row in DataFrame order, calls
   `simulate_cell(cell_row=row, cell_index=row_index)`. Wraps each call in
   `try/except (RuntimeError, ValueError, AssertionError, ArithmeticError)`. On failure: append a
   row to `results/data/simulation_failures.csv` with columns
   `(cluster_id, cell_key, mode, direction, error_type, error_message)`; continue with the next
   cell. Prints per-cell wall-clock + running ETA via `tqdm`. Validation gate before the full sweep:
   * **Trivial baseline**: for cells with DSI > 0.5 the PD `V_m` trial must contain more spikes than
     the ND `V_m` trial. (Same as REQ-14, applied as a pipeline-health check.)
   * **Small-scale pre-flight**: first run on `--limit 2` (one cell from cluster 0 and one from
     cluster 1). After the pre-flight, read the 12 trace parquets the script produced (2 cells × 3
     modes × 2 directions) and visually inspect: (i) `g_E(t)` and `g_I(t)` parquets contain
     non-zero peaks; (ii) the `V_m(t)` parquet contains a non-flat trace; (iii) trace row count is
     exactly 1400; (iv) the high-DSI cell shows more PD `V_m` spikes than ND.
   * **Failure condition**: if any pre-flight cell crashes, or if the high-DSI cell shows
     `PD_spikes <= ND_spikes`, STOP and debug the simulator wiring (likely wrong direction argument,
     wrong NMDA NetCon zeroing, or wrong gbar-suffix list) before launching the full 40-cell sweep.
     Wall-clock for the full sweep estimated at 30–60 min.

   Expected: 1 new file, ~120 lines. Satisfies REQ-10.

### Milestone 4 — Metric extraction and figure rendering

9. **Create `code/extract_metrics.py`.** For each cell in `selected_cells.csv` and each direction in
   `{0.0, 180.0}`:
   * Load the three trace parquets `<mode>_<direction>.parquet` from the cell's traces folder.
   * Compute: peak `g_E` (µS) and time-to-peak (ms); peak `g_I` (µS) and time-to-peak (ms);
     `g_I / g_E` ratio at the peak-`g_E` time index; g_I onset latency = first `t_ms` value at which
     `g_I(t) >= 0.5 * peak_g_I`; spike count = count of upward crossings of
     `SPIKE_THRESHOLD_MV = -10.0` in `V_m(t)` with refractory ≥ `SPIKE_REFRACTORY_MS = 2.0` ms;
     mean and max `V_m`.
   * Write `results/data/per_cell_metrics.csv` with 80 rows (40 cells × 2 directions) and columns
     `(cluster_id, source_task, seed, generation, individual_idx, direction_deg, peak_g_e_us, peak_g_e_time_ms, peak_g_i_us, peak_g_i_time_ms, gi_ge_ratio_at_peak_ge, g_i_onset_latency_ms, n_spikes, mean_v_m_mv, max_v_m_mv)`.

   Expected: 1 new file, ~150 lines. Satisfies REQ-11.

10. **Create `code/plot_cluster_figures.py`.** Render two output families:

    * **Per-cluster** `results/images/cluster_<c>_traces.png` for `c ∈ {0,1,2,3}`. Layout
      `matplotlib.subplots(nrows=10, ncols=3, figsize=(15, 30), sharex=True)`. Each row is one cell
      ordered top-to-bottom by ascending `dsi_vector_sum` within the cluster. Columns: `g_E(t)`,
      `g_I(t)`, `V_m(t)`. Plot PD trace as solid line and ND trace as dashed line in one colour per
      cell. Y-axis units: µS for the first two columns, mV for the third. X-axis: `t_ms` over
      0–1400. Annotate `(DSI=...; PD=...)` in the top-right corner of each panel.

    * **Cross-cluster** `results/images/cross_cluster_traces.png`. Layout
      `subplots(nrows=4, ncols=3, figsize=(15, 12))`. Each row is one cluster's *median* trace
      across its 10 cells (compute pointwise median over `t_ms`). Columns: `g_E`, `g_I`, `V_m`. PD
      solid + ND dashed; one colour per cluster.

    * Use a clear figure title per file (`Cluster <c> — n=10 cells, PD (solid) vs ND (dashed)` for
      per-cluster; `Cross-cluster median traces — k=4 t0117 clusters` for the summary). Save at
      `dpi=120`. Expected: 5 PNG files. Satisfies REQ-12 and REQ-13.

### Milestone 5 — Quality checks and manifest verification

11. **Create `code/dsi_sanity_check.py`.** Read `per_cell_metrics.csv` and `selected_cells.csv`,
    pivot to one row per cell with PD and ND spike counts, compute
    `passed = (dsi_vector_sum <= 0.5) | (n_spikes_pd > n_spikes_nd)`. Write the per-cell pass / fail
    table to `results/data/dsi_sanity_check.csv` (columns
    `cluster_id, cell_key, dsi_vector_sum, n_spikes_pd, n_spikes_nd, passed`). Print the failure
    list to stdout. Expected: 1 new file, ~50 lines. Satisfies REQ-14.

12. **Create `code/verify_outputs.py`.** Manifest-resolution check (REQ-15):
    * Assert `selected_cells.csv` has exactly 40 rows (10 per cluster).
    * For every row, assert the `(source_task, seed, generation, individual_idx)` tuple resolves to
      exactly one row of `pooled_all_cells.parquet`.
    * For every (cell, mode, direction) triple, assert either the trace parquet exists at
      `results/data/traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` AND has exactly 1400
      rows, OR a matching row exists in `simulation_failures.csv`.
    * For every existing parquet, assert the recorded columns match the mode (EPSP_PASSIVE →
      `t_ms, g_e_us`; IPSP_PASSIVE → `t_ms, g_i_us`; FULL → `t_ms, v_m_mv`).

    Expected: 1 new file, ~80 lines. Satisfies REQ-15.

## Remote Machines

None required. Runs locally on a Windows CPU workstation with NEURON 8.2.7 installed and the
compiled t0080 channel DLL at `tasks/t0080_*/code/build/nrnmech.dll`. No GPU / no remote provider
needed.

## Assets Needed

* **From t0117**:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/electrophys_clusters.csv`
  (cluster assignments) and `tasks/t0117_*/data/pooled_all_cells.parquet` (68-d vectors + DSI / PD
  per cell). Both produced by t0117 (dependency).
* **From t0080**: `procedural_dsgc_morphology_generator_fix` and
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` libraries (registered library assets) plus the
  compiled NEURON channel DLL `tasks/t0080_*/code/build/nrnmech.dll` (gitignored — copy from main
  repo or rebuild).
* **From t0090 / t0092**: `procedural_dsgc_morphology_generator` and
  `procedural_dsgc_morphology_generator_fix` libraries — used for `MorphologyParams`,
  `MorphologyResult`, `generate_fixed_morphology`, `insert_baseline_channels`.
* **From t0106 (copied, not imported)**: 8 files of simulator scaffolding listed in REQ-4 / Step 5.

## Expected Assets

`expected_assets` in `task.json` is `{}` — this is a demonstration / exploratory task whose
outputs are figures, traces, and per-cell metrics rather than canonical asset-typed artifacts. The
deliverables are:

* **Tables** (under `results/data/`): `selected_cells.csv` (40 rows), `per_cell_metrics.csv` (80
  rows = 40 cells × 2 directions), `simulation_failures.csv` (one row per failed (cell, mode,
  direction)), `dsi_sanity_check.csv` (40 rows), and 240 trace parquets under
  `traces/<cluster_id>/<cell_key>/`.
* **Figures** (under `results/images/`): four per-cluster figures `cluster_<c>_traces.png` for
  `c ∈ {0, 1, 2, 3}` and one cross-cluster summary `cross_cluster_traces.png`.

No `assets/` subfolder is populated by this task. `assets/answer/`, `assets/dataset/`,
`assets/library/`, `assets/model/`, `assets/paper/`, and `assets/predictions/` remain empty (the
existing `.gitkeep` files preserve the empty subfolders).

## Time Estimation

| Phase | Estimate |
| --- | --- |
| Research (done) | ~2 h |
| Planning (this stage) | ~1 h |
| Scaffolding (Steps 1–5) | ~1 h (copying files, paths, constants, loader, sampler) |
| DLL pre-flight (Step 6) | ~5 min (copy from main repo) or ~10 min (`nrnivmodl.bat` rebuild) |
| Simulator + sweep (Steps 7–8) | 30–60 min (240 NEURON runs, ~7–15 s each, sequential) |
| Metric extraction + plotting (Steps 9–10) | ~10 min |
| Sanity checks + manifest verify (Steps 11–12) | ~5 min |
| **Total implementation** | **~2.5 – 3 h** |

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| NEURON DLL missing in worktree (`build/` gitignored) | High | Blocking | Pre-flight check in Step 6; copy from main repo's `tasks/t0080_*/code/build/nrnmech.dll` or rebuild via `nrnivmodl.bat` on the mod sources before any simulation starts. |
| AIS section mismatch between procedural morphology and `apply_parameter_vector`'s `update_ais_geometry` | Medium | Blocking for the sweep | Read `MorphologyResult` AIS attribute names before Step 7; if they differ from `AISExtension`, either patch `update_ais_geometry` to call the procedural AIS section or skip it (the AIS length is already set during morphology generation via `MorphologyParams.ais_length_um`). |
| NMDA leaks through IPSP_PASSIVE because NMDA shares the ACh NetStim | Medium | Confounds the g_I trace | Zero `ncs_nmda[i].weight[0]` in IPSP_PASSIVE mode (REQ-7) in addition to `ncs_ach[i].weight[0]`. Verified via the validation gate in Step 8 (small-scale pre-flight: `g_I` in IPSP_PASSIVE must NOT contain a transient ACh-driven spike). |
| `gbar_<suffix>` zero-out misses an active channel, leaving HH-on residue in passive trace | Medium | Confounds g_E / g_I traces | Use the explicit 13-mechanism list from `constants_electrophys.py:CHANNEL_SUFFIXES` + `SLOW_AHP_SUFFIX` + `HHst.gnabar/gkbar/gkmbar`, applied to every segment of soma + all_dends + ais_proximal + ais_distal. Validation gate in Step 8: check that the EPSP_PASSIVE `V_m` trace (if recorded as a debug aid) is monotonic with no spikes. |
| Sequential NEURON sweep exceeds the 60-min wall-clock estimate | Low–Medium | Slow iteration | Cut to 20 cells (5 per cluster) for a fast iteration cycle if needed, but ship the full 40-cell sweep as the final deliverable. Subprocess parallelisation is documented as a fallback but not required by default. |
| Cluster 1 has < 10 occupied DSI × PD bins (it's mostly the t0114 seed-7755 high-DSI corner) | Medium | Cluster-1 selection drifts from the stratified ideal | The top-up rule in `stratified_sample.py` (Step 4) picks the next-most-distant cell in standardised DSI × PD space, ensuring 10 cells per cluster even when the quintile picker exhausts occupied bins. The per-cell `dsi_quintile` and `pd_quintile` columns let the reader see how diverse the sample really was. |
| `_LIVE_CELLS` accumulates references; RSS climbs past workstation RAM | Low | Crash mid-sweep | Explicit teardown per cell (`_LIVE_CELLS.pop()` + `h.delete_section` + `del cell`) keeps RSS bounded. If RSS still climbs, fall back to subprocess-per-cell isolation. |
| One bad parameter vector silences a cell (no synapses fire) | Medium | Empty / flat traces for that cell | The per-cell try/except in Step 8 catches `(RuntimeError, ValueError, AssertionError, ArithmeticError)` and writes a row to `simulation_failures.csv`. Sweep continues. The figure renderer (Step 10) plots a "FAILED" placeholder in any panel whose trace file is missing. |

## Verification Criteria

* **Selected-cells manifest** — run
  `uv run python -u -c "import pandas as pd; df = pd.read_csv('tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/data/selected_cells.csv'); print(df.groupby('cluster_id').size())"`
  and confirm output `0 10 / 1 10 / 2 10 / 3 10` (exactly 40 rows, 10 per cluster). Then run the
  t0117 join check via the script written in Step 12. Covers REQ-1, REQ-2, REQ-3, REQ-15.

* **Trace parquets** — run
  `uv run python -m arf.scripts.utils.run_with_logs python -u tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/code/verify_outputs.py`
  and confirm zero assertion failures. The script asserts for every (cell, mode, direction) triple
  that either the parquet exists at the canonical path with exactly 1400 rows AND the correct
  columns for the mode, OR a matching row is present in `simulation_failures.csv`. Covers REQ-6
  through REQ-10 and REQ-15.

* **Per-cell metrics CSV** — run
  `uv run python -u -c "import pandas as pd; df = pd.read_csv('tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/data/per_cell_metrics.csv'); assert len(df) == 80, len(df); print(df.columns.tolist())"`
  and confirm 80 rows (40 cells × 2 directions) with columns
  `[cluster_id, source_task, seed, generation, individual_idx, direction_deg, peak_g_e_us, peak_g_e_time_ms, peak_g_i_us, peak_g_i_time_ms, gi_ge_ratio_at_peak_ge, g_i_onset_latency_ms, n_spikes, mean_v_m_mv, max_v_m_mv]`.
  Covers REQ-11.

* **Five figure PNGs** — run
  `uv run python -u -c "from pathlib import Path; expected = [f'tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/images/cluster_{c}_traces.png' for c in range(4)] + ['tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/images/cross_cluster_traces.png']; missing = [p for p in expected if not Path(p).exists()]; assert not missing, missing; print('all 5 figures present')"`
  and confirm "all 5 figures present". Covers REQ-12 and REQ-13.

* **DSI sanity check** — run
  `uv run python -u -c "import pandas as pd; df = pd.read_csv('tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/results/data/dsi_sanity_check.csv'); failed = df.loc[~df['passed']]; print('failures:', len(failed)); print(failed[['cluster_id','cell_key','dsi_vector_sum','n_spikes_pd','n_spikes_nd']])"`
  and confirm zero failures among cells with `dsi_vector_sum > 0.5`. Cells with DSI ≤ 0.5 are
  exempt and their `passed` value is unconditionally `True`. Covers REQ-14.

* **REQ coverage** — every `REQ-*` item from the Task Requirement Checklist is referenced by at
  least one step in `## Step by Step`. Run
  `uv run python -u -m arf.scripts.verificators.verify_plan t0118_resimulate_t0117_cluster_samples_ge_gi_vm`
  and confirm zero errors and that warning `PL-W007` (Step by Step does not reference any `REQ-*`
  items) is not raised.
