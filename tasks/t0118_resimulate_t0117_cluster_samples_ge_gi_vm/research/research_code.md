---
spec_version: "1"
task_id: "t0118_resimulate_t0117_cluster_samples_ge_gi_vm"
research_stage: "code"
tasks_reviewed: 14
tasks_cited: 12
libraries_found: 18
libraries_relevant: 3
date_completed: "2026-05-22"
status: "complete"
---
# Research Code — t0118 Re-Simulate 10 Cells per t0117 Cluster (g_E / g_I / V_m, PD + ND)

## Task Objective

Re-simulate 40 cells (10 per t0117 electrophys cluster x 4 clusters) on the canonical Bed B +
morphology DSGC substrate. For each cell, run the three-mode trial trio (`EPSP_PASSIVE` /
`IPSP_PASSIVE` / `FULL`) in PD and ND, record `g_E(t)`, `g_I(t)`, `V_m(t)`, and produce per-cluster
trace grids and a cross-cluster median comparison. The cohort is stratified by DSI x PD-rate
quintiles within each cluster. This code-research task identifies the simulator entry-point, the
68-d parameter unpacking convention, the morphology builder, the conductance-recording recipe, the
NEURON DLL location, and the NEURON statefulness rules so the implementation subagent can wire the
pipeline together by copying validated code blocks rather than re-discovering them.

## Library Landscape

The library aggregator script `arf.scripts.aggregators.aggregate_libraries` is not present in this
fork (only `aggregate_tasks`, `aggregate_metric_results`, `aggregate_suggestions`,
`aggregate_categories`, `aggregate_costs`, `aggregate_machines`, `aggregate_task_types`, and
`aggregate_metrics` exist under `arf/scripts/aggregators/`). Library discovery was therefore done by
direct filesystem inspection of `tasks/*/assets/library/*/details.json`, the same procedure used by
t0116's [t0116] and t0117's research-code stages. 18 registered library assets were enumerated (one
folder per asset under various `tasks/tNNNN_*/assets/library/`).

**Domain-irrelevant libraries (15 of 18)** — not relevant to a 68-d biophysical re-simulation
task: `modeldb_189347_dsgc`, `modeldb_189347_dsgc_gabamod`, `modeldb_189347_dsgc_dendritic`,
`modeldb_189347_dsgc_exact` (ModelDB ports superseded by the de Rosenroll DSGC line);
`tuning_curve_viz`, `tuning_curve_loss` (visualisation / loss helpers for the t0011 / t0012 era);
`minimal_dsgc_scalar_gaba`, `minimal_dsgc_spatial_gaba`, `minimal_dsgc_ampa_nmda_scalar_gaba`,
`minimal_dsgc_mg_block_nmda`, `minimal_dsgc_tonic_gaba_sweep`,
`minimal_dsgc_bar_locked_gaba_ampa_sweep` (t0052-t0059 era minimal-substrate sweeps that pre-date
the Bed B substrate); `dsgc_active_channel_pack` (t0074 single-cell channel-tuning testbed);
`de_rosenroll_2026_dsgc` (t0024 Bed A canonical port); `de_rosenroll_2026_dsgc_ais` (t0078 Bed B v2
substrate without dendritic-spike machinery — superseded by t0080).

**Relevant libraries (3 of 18)** — all needed:

* `de_rosenroll_2026_dsgc_ais_dendritic_spike` (t0080) at
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/`. v3 Bed B substrate with AIS,
  dendritic Mg-block NMDA, distal Nav1.6 + NaP overlay. Library-registered entry points relevant to
  t0118: `build_dsgc_cell_with_ais` (cell builder), `apply_parameter_vector` (writes 54-d
  electrophys params to all sections), `DSGCCellWithAIS` (cell dataclass), `ParameterVector` (54-d
  frozen dataclass with @property accessors). All four are imported via
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.*` per the library asset's `module_paths`
  list. NOTE: the *simulator entry-point* used by t0106 / t0112 / t0114 / t0115 (the
  `evaluate_68d_vector` function in `tasks/t0106_long_pdnd_nsga2_300gen/code/evaluator.py`) is *NOT*
  registered as a library entry — it lives in t0106's code folder, which is not a library, so per
  the cross-task code-reuse rule t0118 must **copy** that machinery into `tasks/t0118_*/code/` and
  adapt it for the mode-trio with conductance recording.

* `procedural_dsgc_morphology_generator` (t0090) at
  `tasks/t0090_morphology_generator_diversity_test/assets/library/`. Provides `MorphologyParams`
  (14-field frozen dataclass for the morphology subspace) and `MorphologyResult` (returns `h`,
  `soma`, `all_dends`, `section_endpoints_xy`, `origin_xy`, `terminal_dends`, `primary_dends`,
  `non_terminal_dends`, `terminal_locs_xy`). Import path:
  `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult`.
  Same usage as t0116, t0117, and t0109 [t0109].

* `procedural_dsgc_morphology_generator_fix` (t0092) at
  `tasks/t0092_diagnose_morphology_generator_silence/assets/library/`. Single canonical entry
  `generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`
  — the soma-pt3d-bug-patched drop-in replacement for t0090's `generate_morphology`. Per
  `C-0093-01`, this is the only morphology builder allowed in the build path. Import:
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
  Also exposes `insert_baseline_channels(*, h, cell)` from
  `tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels`, which inserts HHst
  + cad on every section (needed when the t0080 substrate is applied on top).

## Key Findings

### Canonical Bed-B + morphology simulator entry-point

The function that t0106 [t0106] / t0112 [t0112] / t0114 [t0114] / t0115 [t0115] use to evaluate one
68-d cell is `evaluate_68d_vector` in `tasks/t0106_long_pdnd_nsga2_300gen/code/evaluator.py`
(signature:
`def evaluate_68d_vector(*, vector_68d: NDArray[np.float64], eval_seeds: list[int] | None = None, n_directions: int = N_DIRECTIONS) -> CellEvalResult`).
It does five things, in order:

1. Calls `split_68d_vector` from `generator_wrapper.py` (lines 50-55) to split the 68-d input into
   `(electrophys_54d, morph_14d)`. The split is at index 54.
2. Builds `MorphologyParams` via `morphology_params_from_vector(morph_vector_14d=morph_14d)`
   (`generator_wrapper.py` lines 58-77). This is where the 14-d float vector is unpacked into the
   named morphology fields and the three int fields (`num_primary_branches`, `max_strahler_depth`,
   `morph_seed`) are coerced via `int(round(float(...)))`.
3. Builds the cell via `build_cell(h=h, morph_params=morph_params)` (`generator_wrapper.py` lines
   80-92), which calls
   `generate_fixed_morphology(params=morph_params, morph_seed=morph_params.morph_seed)` from the
   t0092 library and then `insert_baseline_channels(h=h, cell=cell)` from t0092. The result is
   registered in the `_LIVE_CELLS` module-level list to defend against GC-driven cell-id reuse
   (REQ-18 of t0106 plan).
4. Applies the 54-d electrophys vector via
   `apply_parameter_vector(cell=cell, params=electrophys_params)` from
   `tasks/t0106_long_pdnd_nsga2_300gen/code/apply_params.py` (lines 167-234). This loads the t0080
   channel DLL (via `ensure_t91_dll_loaded` -> `t0080.apply_params.ensure_t80_dll_loaded`), inserts
   all 12 t80-namespace channel suffixes plus `skahpt80` on soma + dends + AIS, and writes the 54-d
   densities in the canonical tier-stratified + uniform layout.
5. Builds the synapse bundle via `setup_synapses_parametric` from
   `tasks/t0106_long_pdnd_nsga2_300gen/code/trial_helpers.py` (lines 206-311). This creates `n_ach`
   Exp2Syn ACh + co-located Exp2NMDA pairs and `n_gaba` Exp2Syn GABA contacts via the parametric
   placer, with two NetStim drivers per synapse (queued via `NetCon.event` from a
   `FInitializeHandler`).

For each trial, `_run_one_trial` in `evaluator.py` (lines 166-271) generates AR(2)-correlated
release rates, queues NetCon events, runs `h.run()`, and records soma `v` only. The t0118 task needs
a variant that ALSO records per-synapse `_ref_g` for all Exp2Syn ACh + Exp2Syn GABA contacts, and
applies HH-off + selective-synapse-silencing overrides per mode.

The bar direction is set by the `direction_deg` argument to `_bar_arrival_times` (`trial_helpers.py`
lines 64-75): `theta = np.radians(direction_deg)` projects each synapse's xy onto the unit vector,
and the bar's arrival at that synapse is
`BAR_START_TIME_MS + (proj - BAR_X_START_UM) / BAR_VELOCITY_UM_PER_MS`. PD = 0 deg, ND = 180 deg per
`PD_DIRECTION_DEG` / `ND_DIRECTION_DEG` in `constants_electrophys.py` lines 44-45. Arbitrary angles
are valid (the function is fully general).

### 68-d parameter layout and unpacking

The 68-d vector layout is **identical** across t0106, t0112, t0114, t0115, t0116, t0117. The
authoritative source of the per-dimension names is
`tasks/t0108_t0106_cluster_factor_dsi05_pd10/code/constants.py` `ALL_PARAM_NAMES` (lines 110-111),
which is `ELECTROPHYS_PARAM_NAMES` (54 names, lines 33-89) concatenated with
`MORPHOLOGY_PARAM_NAMES` (14 names, lines 92-108). The 54-d block is consumed by
`ParameterVector(values=...)` from
`tasks/t0106_long_pdnd_nsga2_300gen/code/constants_electrophys.py` (which is itself a copy of
t0080's `constants.py:ParameterVector`); the 14-d block is consumed by `MorphologyParams` via
`morphology_params_from_vector`.

The 54-d block has the ParamIndex IntEnum layout (`constants_electrophys.py` lines 145-209): indices
0..24 are tier-stratified channel densities (5 channels x 5 tiers in channel-major order: all 5
tiers of Nav1.6, then Kv3, NaP, BK, SK); 25..31 are uniform-density channels (Kdr, Kv4, NaR, Ih,
CaL, CaT, Im); 32-33 are SK-AHP gbar + tau_ca_multiplier; 34..46 are 13 passive + synaptic placement
params (Ra, cm, gleak, cad_depth, cad_taur, N_ach, N_gaba, rho0_ach, lambda_ach_um, rho0_gaba,
lambda_gaba_um, w_ach_us, w_gaba_us); 47-48 are AIS geometry (`ais_length_um`, `ais_diameter_um`);
49..53 are the 5 v3 dendritic-spike params (`gnmda_dend`, `mg_conc_mm`, `voff_nmda`,
`nav16_dend_distal`, `nap_dend_distal`).

The 14-d morphology block has the field order
(`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/constants.py`
`MORPHOLOGY_PARAM_NAMES`, same as t0108's): `num_primary_branches`, `branch_prob_per_um`,
`max_strahler_depth`, `mean_branching_angle_deg`, `rall_exponent`, `soma_offset_pd_um`,
`field_elongation_pd`, `branch_density_gradient_pd`, `primary_branch_pd_concentration`,
`mean_segment_length_um`, `soma_diameter_um`, `ais_length_um` (NB: distinct from the electrophys
`AIS_LENGTH_UM` slot — the morphology one is what the procedural builder uses to size the AIS
section, while the electrophys one is what `apply_parameter_vector` writes via `update_ais_geometry`
after the cell is built), `morph_seed`, `branch_length_cv`. The `morph_seed` field must be coerced
via `int(round(float(...))) % (2**31 - 1)` (the modulo prevents INT32 overflow — see t0109's
pattern copied into t0117's `morphology_rendering.py:to_morph_params` lines 61-77, which uses the
`MAX_MORPH_SEED = 2**31 - 1` constant from t0117 [t0117] `constants.py` line 30).

### Mode-trio (EPSP_PASSIVE / IPSP_PASSIVE / FULL) — adapted for the 68-d substrate

No prior task has applied the three-mode trio to the 68-d Bed B + morphology substrate. The
canonical mode-trio implementation is `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py`
[t0066], which ran on the t0024 Bed A cell and uses an Exp2Syn-only substrate with a single `HHst`
mechanism. Its `_apply_mode_overrides` (lines 178-194) is the canonical mode-silencing logic and
must be adapted for t0118:

* `TrialMode.EPSP_PASSIVE`: zero out all GABA `NetCon.weight[0]` (silences inhibition); set all HH
  conductances to 0.
* `TrialMode.IPSP_PASSIVE`: zero out all ACh `NetCon.weight[0]` (silences excitation); also zero out
  NMDA `NetCon.weight[0]` since NMDA is co-driven by the ACh NetStim; set all HH conductances to 0.
* `TrialMode.FULL`: do not touch synapse weights; leave HH on.

For the 68-d substrate, "HH off" means more than just `HHst.gnabar / gkbar / gkmbar = 0`. The t0080
substrate inserts 12 active channel mechanisms (`CHANNEL_SUFFIXES` in `constants_electrophys.py`
lines 72-85: `nav16t80`, `napt80`, `nart80`, `kdrt80`, `kv3t80`, `kv4t80`, `kv7t80`, `iht80`,
`calt80`, `catt80`, `bkt80`, `skt80`) plus `skahpt80`, with `HHst` also inserted by
`insert_baseline_channels`. To realise EPSP_PASSIVE / IPSP_PASSIVE on this substrate, the override
must set `gbar_<suffix>` to 0.0 for ALL 12 t80 suffixes + `skahpt80` on every segment of soma +
all_dends + ais_proximal + ais_distal, AND set `HHst.gnabar/gkbar/gkmbar = 0`. Without zeroing the
t80 channels, the "passive" trace would still contain regenerative dendritic Nav1.6 / NaP / Kv3
currents, which defeats the purpose of the mode.

For NMDA on IPSP_PASSIVE: the t0106 / t0080 substrate co-locates an Exp2NMDA at every ACh site
(`trial_helpers.py:setup_synapses_parametric` lines 268-280). Since NMDA shares the ACh NetStim,
zeroing `ncs_ach[i].weight[0]` does not silence NMDA. The override must also zero
`ncs_nmda[i].weight[0]` to fully silence excitation in IPSP_PASSIVE mode.

The canonical state restore-then-override pattern from t0066 (`_snapshot_canonical_state` lines
129-154, `_restore_canonical_state` lines 157-175) must be adapted to capture and restore all 13 t80
\+ HHst conductance values per segment. The simpler-and-safer alternative for t0118 is to **apply
electrophys params fresh per mode** (call `apply_parameter_vector` then immediately zero the
channels per the mode), rather than snapshot-and-restore. This is cleaner and avoids a ~250-element
conductance snapshot.

### Conductance recording: `_ref_g` per Exp2Syn

The canonical recipe for recording per-synapse conductances comes from
`tasks/t0072_synaptic_traces_pd_nd/code/run_bed_b.py` [t0072] (lines 214-248). The pattern is:

```python
for i in range(n_terminals):
    v_a = h.Vector()
    v_a.record(bundle.syns_ach[i]._ref_g, RECORD_DT_MS)
    g_ach.append(v_a)
    v_g = h.Vector()
    v_g.record(bundle.syns_gaba[i]._ref_g, RECORD_DT_MS)
    g_gaba.append(v_g)
t_rec = h.Vector()
t_rec.record(h._ref_t, RECORD_DT_MS)
```

The Exp2Syn `_ref_g` returns instantaneous conductance in **microsiemens (uS)** (per t0072's
`aggregate.py` line 51 comment). The t0118 trace_storage convention asks for uS, so no unit
conversion is needed; document the unit explicitly in the parquet column name (`g_e_us`, `g_i_us`).

The "total" `g_E(t)` requested by t0118 must be the SUM over all `n_ach` Exp2Syn contacts at each
time point: `g_E(t) = sum_i(g_ach[i](t))`. Same for `g_I(t) = sum_i(g_gaba[i](t))`. This gives total
cell-level excitatory and inhibitory conductance.

NMDA contribution: the t0080 substrate has both Exp2Syn ACh and Exp2NMDA at every ACh contact
(`trial_helpers.py:setup_synapses_parametric` lines 268-280). The task description specifies
"g_E(t)" without disambiguation — the cleanest interpretation is to sum the ACh Exp2Syn
conductance only, since NMDA conductance is voltage-gated (via the Mg block) and would not be a
"pure synaptic g_E". If NMDA contribution is needed downstream, the implementation can record
`syns_nmda[i]._ref_g` as an extra column. **Recommendation**: record both ACh and NMDA separately,
sum to total `g_E_total = g_E_ach + g_E_nmda`, and store all three columns in the parquet so
downstream consumers can re-decompose if needed.

### Bar-motion parameters

The canonical bar-motion parameters come from
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` (lines 78-84):

* `BAR_VELOCITY_UM_PER_MS = 1.0` (bar moves at 1 um/ms = 1 mm/s).
* `BAR_WIDTH_UM = 250.0` (bar is 250 um wide perpendicular to motion).
* `BAR_X_START_UM = -40.0` (leading edge starts 40 um before the cell origin).
* `BAR_X_END_UM = 200.0` (trailing edge passes at 200 um).
* `BAR_Y_START_UM = 25.0` (bar spans y = 25..225 um).
* `BAR_Y_END_UM = 225.0`.
* `BAR_START_TIME_MS = 0.0` (bar leading edge crosses x=BAR_X_START_UM at t=0).

These are shared by t0106 / t0112 / t0114 / t0115 because they all import via
`from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24`. t0118 must follow suit
(the constants are part of `de_rosenroll_2026_dsgc` library; importing from the t0024 path is the
registered library entry).

### Trial length and dt

`TSTOP_MS = 1400.0` ms — confirmed in
`tasks/t0106_long_pdnd_nsga2_300gen/code/constants_electrophys.py` line 35 and in t0080's
`constants.py:TSTOP_MS` (line 35 too — they are independent copies; both 1400). This is the
1400-ms trial length the t0118 task description mandates. `DT_MS = 0.1` ms (line 33) is the
integration step, `STEPS_PER_MS = 10.0` (line 34), and `RECORD_DT_MS = 1.0` (line 38) is the
recording resolution for soma Vm. For trace storage in t0118, `RECORD_DT_MS = 1.0` gives 1400
samples per (mode, direction) trial, which is ~56 KB per parquet column at float64.

The t0118 task description says "at least 1 400 ms of samples at the simulator's default dt
(typically 0.025 ms -> ~56 000 rows)". This is **incorrect**: the t0106 / t0080 default is
`DT_MS = 0.1` (10 samples/ms x 1400 ms = 14000 raw integration points), and the canonical recording
resolution from t0066 / t0072 is `RECORD_DT_MS = 1.0` (1400 samples). The implementation subagent
should follow `RECORD_DT_MS = 1.0` (1400 rows per trace), which matches the t0066 trace_csv stride
convention (1 ms after the CSV_SUBSAMPLE_STRIDE=10 from the 0.1-ms raw dt). 56000 rows would only
happen if the implementation chose `RECORD_DT_MS = 0.025`, which is unwarranted overkill for this
task.

### NEURON DLL location and gitignore status

The t0080 channel DLL lives at `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/`. On
Windows this is `nrnmech.dll`; the `WINDOWS_MOD_BUILD_DLL` constant in
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/paths.py` line 21 points at exactly that path.
The `resolve_t80_mod_library()` helper (lines 24-37) returns the first existing candidate between
Linux .so and Windows .dll. The repo `.gitignore` line 8 contains `build/`, so the compiled DLL is
NOT tracked in git. On a fresh worktree the DLL is therefore **missing** and must be re-compiled.
The compile step is `nrnivmodl.bat` (Windows) or `nrnivmodl` (Linux) run inside
`tasks/t0080_*/code/mods/` against the 13 `.mod` source files (`bkt80.mod`, `calt80.mod`,
`catt80.mod`, `iht80.mod`, `kdrt80.mod`, `kv3t80.mod`, `kv4t80.mod`, `kv7t80.mod`, `napt80.mod`,
`nart80.mod`, `nav16t80.mod`, `skahpt80.mod`, `skt80.mod`).

Confirmed: the main repo's `tasks/t0080_*/code/build/nrnmech.dll` exists locally (was compiled
during the t0080 task) but is not in the worktree. The implementation subagent must either (a) copy
the DLL from the main repo's build folder into the worktree's `tasks/t0080_*/code/build/`, or (b)
re-run nrnivmodl on the .mod sources inside the worktree. Option (a) is faster and is the t0114 /
t0115 precedent.

### NEURON statefulness — sequential vs parallel

NEURON has process-global state via the `h` instance: section names, mechanism SUFFIXes, ranlist,
ref counts. The canonical pattern across the 68-d substrate tasks is:

* **Sequential in-process with `h.delete_section` cleanup** is safe for *building and rendering*
  many cells in a row. t0109 [t0109], t0116 [t0116], and t0117 [t0117] all do this in their
  morphology gallery / representative rendering scripts. See
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/morphology_rendering.py` lines
  100-103:
  `for s in list(result.all_dends) + [result.soma]: with contextlib.suppress(RuntimeError, AttributeError): h.delete_section(sec=s)`.
  Without this cleanup, the process RSS climbs monotonically as more cells are built.

* **In-process sequential with cell rebuild per cell** is what t0118 needs. Each cell's morphology
  is procedurally generated from its own (params, morph_seed) pair, so the cell must be torn down
  and rebuilt between cells. The mode trio for a single cell can re-use the same cell
  (snapshot-and-restore canonical state per the t0066 pattern, or apply_params fresh per mode per
  the simpler-and-safer alternative above). The same cell can also be re-used for PD and ND since
  direction is changed only via `_bar_arrival_times`, not via the cell.

* **Subprocess parallelisation** is what the t0106 NSGA-II driver uses
  (`evaluator.py:_worker_evaluate_vector` and `BedBV3MorphProblem._evaluate`, `nsga2_driver.py`).
  Each pymoo subprocess gets its own NEURON state, but the wall-clock cost per cell is dominated by
  build + apply_params, not by `h.run()` itself. For t0118's 40 cells the in-process sequential path
  is fine (estimated 30-60 min total per the task description), and the additional subprocess
  machinery is not justified.

* **Risk**: NEURON's `delete_section` does NOT garbage-collect every Python reference to the
  section. The t0109 / t0117 pattern wraps the call in
  `contextlib.suppress(RuntimeError, AttributeError)` because deletes can race against finalizers.
  The t0106 code uses a module-level `_LIVE_CELLS` list (`generator_wrapper.py` line 38) to keep
  every built cell alive — this is REQ-18 of t0106 plan and protects against cell-id reuse after a
  partial GC. For t0118's sequential pipeline, the safer pattern is **explicit teardown** (delete
  sections
  + remove from `_LIVE_CELLS` + del cell) between cells, matching the t0117 morphology rendering
    pattern.

### Mode trio: snapshot-restore vs re-apply

The t0066 protocol uses snapshot-and-restore: capture `HHst.gnabar/gkbar/gkmbar` per segment +
NetCon weights, then per trial: restore -> override -> run. This works because t0024 has only HHst
as an active mechanism plus a few synapse weights. For the 68-d substrate with 13 active mechanisms
x ~200 segments per cell, the snapshot would be ~2600 floats per cell — manageable but
error-prone.

The cleaner alternative for t0118 is to **re-apply electrophys params fresh per mode**:

1. Build cell once per cell (via `generate_fixed_morphology` + `insert_baseline_channels` + t0080
   channel insertion).
2. Build synapse bundle once per cell.
3. For each mode in (EPSP_PASSIVE, IPSP_PASSIVE, FULL): a. Call
   `apply_parameter_vector(cell=cell, params=electrophys_params)` to write all 54-d densities fresh
   (this also rewrites passive Ra/cm/gleak). b. If mode != FULL, zero the 13 active-channel suffixes
   and HHst on every section. c. If mode == EPSP_PASSIVE, zero all `ncs_gaba[i].weight[0]`. If mode
   == IPSP_PASSIVE, zero all `ncs_ach[i].weight[0]` AND `ncs_nmda[i].weight[0]`. d. For each
   direction in (PD, ND): regenerate AR(2) noise + bar arrival + queue events -> h.run() -> record
   traces.

This avoids the snapshot dataclass entirely. The `apply_parameter_vector` call is idempotent (per
the `_INSERTED_CELLS` guard in `apply_params.py:_insert_channels_once` line 65-98), so calling it
three times per cell is cheap (~1 ms after the first call). The trade-off is that HH-off in
EPSP_PASSIVE / IPSP_PASSIVE leaves the *passive* electrophys params (Ra, cm, gleak) at the per-cell
values, which is the correct behaviour for "passive trace" (otherwise the cells would all share an
unrealistic passive substrate).

### Mode-trio per-direction recording handles

The t0066 pattern attaches a single soma `v_vec` per trial. For t0118, the recording differs per
mode:

* `EPSP_PASSIVE`: record per-synapse `_ref_g` on all `bundle.syns_ach` (sum -> total g_E). Also
  record `_ref_g` on all `bundle.syns_nmda` (sum -> total g_E_nmda) since NMDA is part of
  excitation. Do NOT record V_m (the passive trace is uninteresting and would inflate storage).
* `IPSP_PASSIVE`: record per-synapse `_ref_g` on all `bundle.syns_gaba` (sum -> total g_I). Do NOT
  record V_m.
* `FULL`: record soma `_ref_v` only. Do NOT record per-synapse conductances (already captured in the
  passive modes — recording them again in FULL would be redundant unless the voltage-driven
  shaping of synaptic current is being studied, which the task description does not request).

This matches the task description's parquet schema "columns: t_ms, g_e_us, g_i_us, v_m_mv (whichever
are recorded for that mode; columns not recorded in that mode are absent)".

### NEURON bootstrap on Windows

The t0106 `bootstrap.py` (lines 153-156) sets `NEURONHOME` to `C:\Users\md1avn\nrn-8.2.7` on Windows
(the local NEURON install root). This is the canonical Windows-only step and is auto-applied as a
side-effect of `import` (line 161). t0118's implementation modules must
`import tasks.t0106_long_pdnd_nsga2_300gen.code.bootstrap` once at module load to ensure NEURONHOME
is set before any t0024 / t0090 / t0092 / t0080 NEURON code runs. If t0118 copies the t0106
evaluator into its own code/, it should also copy or re-implement bootstrap.py with the same
import-side-effect pattern.

### Cluster source data layout

The t0117 cluster assignments are at
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/results/data/electrophys_clusters.csv`.
Confirmed columns (header row):
`cluster_id, source_task, seed, generation, individual_idx, dsi_vector_sum, pd_rate_hz, pc1_combined, pc2_combined`.
The 68-d feature vector for each cell is at
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet` (4431 rows x
74 cols: 6 metadata + 68 named feature columns). The metadata join key is the
`(source_task, seed, generation, individual_idx)` tuple — present in both files. The 68-d vector
for one cell is the 68-column slice of `pooled_all_cells.parquet` named in `ALL_PARAM_NAMES` order,
which exactly matches the order `evaluate_68d_vector` consumes via `split_68d_vector`.

### Failure-tolerant per-cell simulation

The t0106 evaluator wraps `_run_one_trial` in try/except for
`(RuntimeError, ValueError, ArithmeticError)` (lines 263-271) and returns a TrialResult with
`error=...` instead of raising. For t0118 this pattern is essential: a single bad cell should not
abort the 40-cell run. The failure should be recorded in `results/data/simulation_failures.csv`
(task description deliverable) with columns
`(cluster_id, cell_key, mode, direction, error_type, error_message)`. A second wrap should catch
errors at the cell-build level (`_ensure_worker_cell` -> `build_cell` -> `generate_fixed_morphology`
can raise on extreme morphology vectors per the t0093 silence fix). The t0106 pattern of "return
worst-case fallback" is not appropriate for t0118 because there is no objective to minimise — the
cell is simply dropped from the figure with a placeholder.

## Reusable Code and Assets

### Import via library

* **`generate_fixed_morphology`** — Source: `tasks/t0092_diagnose_morphology_generator_silence/`
  via the registered `procedural_dsgc_morphology_generator_fix` library. Signature:
  `generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`.
  Use to rebuild each selected cell's NEURON morphology from its 14-d morphology slice. Adaptation
  needed: none — same usage as t0117 [t0117] `morphology_rendering.py` line 96.

* **`MorphologyParams` / `MorphologyResult`** — Source:
  `tasks/t0090_morphology_generator_diversity_test/` via the registered
  `procedural_dsgc_morphology_generator` library. `MorphologyParams.from_dict(data=...)` is the
  serialisation entry. Adaptation needed: copy the t0117 `to_morph_params` helper (lines 61-77 of
  `tasks/t0117_*/code/morphology_rendering.py`) which already handles the `int(round(float(...)))`
  coercion for `num_primary_branches` and `max_strahler_depth` and the `morph_seed % MAX_MORPH_SEED`
  modulo.

* **`insert_baseline_channels`** — Source:
  `tasks/t0092_diagnose_morphology_generator_silence/code/baseline_channels.py` via the same
  library. Inserts HHst + cad on every section. Called once per cell after
  `generate_fixed_morphology`. Adaptation needed: none.

### Copy into task

The cross-task-import rule says every block below must be **copied** into
`tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/code/`, not imported. Total approximate copy
budget: ~1000-1200 lines across the simulator + new mode-trio adapter + plotting.

* **t0106 `bootstrap.py`** — Source: `tasks/t0106_long_pdnd_nsga2_300gen/code/bootstrap.py` (162
  lines). Sets `NEURONHOME` on Windows, monkey-patches t0024's `load_neuron` for Linux, and exposes
  `compile_t0024_mods_linux`. Adapt: rename the t0024 paths to make the t0118 bootstrap fully
  self-contained (or leave unchanged and accept the cross-task path references inside the file —
  they are tasks/t0024/ which has its own library asset, so the references are valid). The
  auto-import side effect (line 161) must be preserved.

* **t0106 `constants_electrophys.py`** — Source:
  `tasks/t0106_long_pdnd_nsga2_300gen/code/constants_electrophys.py` (548 lines). Carries
  `ParameterVector`, `ParamIndex`, `Tier`, `CHANNEL_SUFFIXES`, `STRATIFIED_CHANNEL_SUFFIXES`,
  `UNIFORM_CHANNEL_SUFFIXES`, `AIS_PERMITTED_SUFFIXES`, `SLOW_AHP_SUFFIX`, sim defaults
  (`TSTOP_MS = 1400`, `DT_MS = 0.1`, `STEPS_PER_MS = 10`, `V_INIT_MV = -60`, `CELSIUS_DEG_C = 36.9`,
  `PD_DIRECTION_DEG = 0`, `ND_DIRECTION_DEG = 180`), and the kinetic constants (`ACH_TAU1_MS = 0.1`,
  `ACH_TAU2_MS = 4.0`, `ACH_EREV_MV = 0.0`, `GABA_TAU1_MS = 0.5`, `GABA_TAU2_MS = 12.0`,
  `GABA_EREV_MV = -60.0`). Adapt: none for the constants relevant to t0118; t0118 can ignore the
  NSGA-II / cost-watchdog constants at the end of the file.

* **t0106 `constants_morphology.py`** — Source:
  `tasks/t0106_long_pdnd_nsga2_300gen/code/constants_morphology.py` (~120 lines, not yet read but
  exposes `N_PARAMS_54 = 54`, `INT_PARAM_INDICES_68`, `LOWER_BOUNDS_68`, `UPPER_BOUNDS_68`,
  `N_DIRECTIONS`, `N_EVAL_SEEDS`, worst-case fallback constants). Adapt: only `N_PARAMS_54` and
  `INT_PARAM_INDICES_68` are needed by t0118; the NSGA-II constants can stay or be deleted.

* **t0106 `build_cell_ais.py`** — Source:
  `tasks/t0106_long_pdnd_nsga2_300gen/code/build_cell_ais.py` (80 lines). NOT useful for t0118 —
  t0106's `build_cell_ais` wraps t0024's `build_dsgc_cell` (which produces the Bed B base cell), but
  t0118 uses the procedurally-generated morphology via `generate_fixed_morphology`, NOT t0024's
  hardcoded base cell. Skip this file.

* **t0106 `extend_with_ais.py`** — Source:
  `tasks/t0106_long_pdnd_nsga2_300gen/code/extend_with_ais.py` (size unknown). Defines
  `AISExtension` dataclass and `extend_with_ais` / `update_ais_geometry` helpers. **REQUIRED**
  because `apply_parameter_vector` calls `update_ais_geometry` at the start to apply the per-cell
  AIS length and diameter from the 54-d slot. The procedurally generated cell already has an AIS
  section attached by `generate_fixed_morphology` (see the `ais_length_um` field in
  MorphologyParams), so the t0106 `update_ais_geometry` must operate on the morphology-generated AIS
  — verify cross-compatibility by reading
  `tasks/t0090_*/code/morphology_params.py:MorphologyResult` for the AIS attribute names. Adapt: may
  need to swap `cell.ais_proximal` / `cell.ais_distal` for the procedurally- generated AIS section
  name if they differ. **Action item for the planner**: verify the AIS exposed by `MorphologyResult`
  matches the AIS interface `apply_parameter_vector` expects.

* **t0106 `parametric_placer.py`** — Source:
  `tasks/t0106_long_pdnd_nsga2_300gen/code/parametric_placer.py` (size unknown). Defines
  `PlacedSynapse` and `place_synapses`. **REQUIRED** because `setup_synapses_parametric` calls it to
  place `n_ach` and `n_gaba` synapses on the dendritic tree. Adapt: none.

* **t0106 `trial_helpers.py`** — Source:
  `tasks/t0106_long_pdnd_nsga2_300gen/code/trial_helpers.py` (312 lines). Carries
  `BASE_ACH_PROB = 0.5`, `PREF_GABA_PROB = 0.05`, `NULL_GABA_PROB = 0.80`, `RATE_DT_MS = 1.0`,
  `BAR_SIGMA_MS = 30.0`, `CELL_PREF_DEG = 0.0`, `_gaba_prob_for_direction`, `_bar_arrival_times`,
  `_rates_with_ar2_noise`, `_rates_to_events`, `_count_spikes`, `SynapseBundle` (dataclass with
  `syns_ach, syns_gaba, ncs_ach, ncs_gaba, netstims, syn_xy_ach, syn_xy_gaba, syns_nmda, ncs_nmda`),
  `_instantiate_synapse`, `setup_synapses_parametric`, `_section_midpoint_xy`. **REQUIRED — most
  central**. Adapt: none for direct copy. The `setup_synapses_parametric` is the canonical 68-d
  synaptic constructor that places Exp2Syn ACh + co-located Exp2NMDA + Exp2Syn GABA.

* **t0106 `generator_wrapper.py`** — Source:
  `tasks/t0106_long_pdnd_nsga2_300gen/code/generator_wrapper.py` (106 lines). Exposes
  `split_68d_vector`, `morphology_params_from_vector`, `build_cell`, `hash_morphology_vector`,
  `_LIVE_CELLS`. Adapt: none for direct copy. **REQUIRED**.

* **t0106 `apply_params.py`** — Source: `tasks/t0106_long_pdnd_nsga2_300gen/code/apply_params.py`
  (234 lines). Exposes `apply_parameter_vector`, `_insert_channels_once`,
  `_write_passive_and_uniform`, `_write_stratified`, `_write_ais_stratified`, `_write_slow_ahp`,
  `ensure_t91_dll_loaded`. **REQUIRED**. Adapt: replace the `ensure_t91_dll_loaded` import-from-
  t0106 self-reference with a t0118-local equivalent that still delegates to
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params.ensure_t80_dll_loaded` (the
  t0080 library entry that loads the channel DLL).

* **t0066 `_apply_mode_overrides` pattern** — Source:
  `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py` lines 178-194 (17 lines). Reference
  implementation of the mode-trio silencing logic. Adapt: replace the single-mechanism HHst zero-out
  with a 13-mechanism (12 t80 channel suffixes + skahpt80 + HHst) zero-out across all sections; add
  NMDA NetCon zero-out for IPSP_PASSIVE mode.

* **t0066 `TrialMode` / `Condition` StrEnum** — Source:
  `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/constants.py` lines 8-16 (10 lines). Adapt: copy
  verbatim. Used to type-tag the mode-trio enumeration.

* **t0066 `_run_one_trial` skeleton** — Source: same file lines 205-298 (94 lines). Adapt: replace
  t0024 cell + t0024 `_setup_synapses` with t0106 `cell` + `bundle`; replace single soma V_m
  recording with the mode-conditional recording recipe (g_E in EPSP_PASSIVE, g_I in IPSP_PASSIVE,
  V_m in FULL); use the t0106 ACh + GABA event-queueing logic from `evaluator.py:_run_one_trial`
  lines 174-231 (which is the 68-d variant of the t0066 event queueing).

* **t0072 `_attach_bed_b_recorders` pattern** — Source:
  `tasks/t0072_synaptic_traces_pd_nd/code/run_bed_b.py` lines 214-248 (35 lines). Canonical
  per-synapse `_ref_g` recorder for Exp2Syn synapses. Adapt: split into two helpers — one attaches
  ACh + NMDA g recorders (for EPSP_PASSIVE), one attaches GABA g recorder (for IPSP_PASSIVE). Drop
  the per-synapse `_ref_v` recording (t0118 only needs the soma V_m in FULL mode, not per-synapse
  local v).

* **t0117 `morphology_rendering.py`** — Source:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/morphology_rendering.py` (~200
  lines). Carries the `to_morph_params` helper that t0118 needs (lines 61-77) and the
  `delete_section` cleanup pattern in `build_and_extract` (lines 100-103). For t0118 the *plotting*
  helpers in this module are not needed (t0118 plots traces, not morphologies), but the
  `to_morph_params` helper and the section-teardown pattern are essential. **Adapt**: copy just
  `to_morph_params` (~16 lines) plus the section-teardown idiom into t0118's per-cell simulator.

### New code for t0118 (not copied)

* **`paths.py`** — ~50 lines new. Centralised path constants for `tasks/t0118_*/code/`, `data/`,
  `results/data/`, `results/data/traces/<cluster_id>/<cell_key>/`, `results/images/`. Includes
  pointers to the t0117 source files ( `T0117_ELECTROPHYS_CLUSTERS_CSV`, `T0117_POOLED_PARQUET`) and
  the t0080 DLL path.

* **`constants.py`** — ~30 lines new. Carries `SAMPLE_SEED = 117` (task description requirement),
  `N_CELLS_PER_CLUSTER = 10`, `N_CLUSTERS = 4`, `N_DSI_QUINTILES = 5`, `N_PD_QUINTILES = 5`,
  `RECORD_DT_MS = 1.0`, the trace parquet column names, and the per-cell metrics keys (
  `PEAK_G_E_KEY`, `PEAK_G_E_TIME_MS_KEY`, `PEAK_G_I_KEY`, `PEAK_G_I_TIME_MS_KEY`,
  `GI_GE_RATIO_AT_PEAK_GE_KEY`, `G_I_ONSET_LATENCY_MS_KEY`, `SPIKE_COUNT_KEY`, `MEAN_VM_KEY`,
  `MAX_VM_KEY`).

* **`load_t0117_clusters.py`** — ~80 lines new. Loads the t0117 electrophys cluster CSV + pooled
  parquet, joins on `(source_task, seed, generation, individual_idx)`, returns a pandas DataFrame
  with `cluster_id`, DSI, PD-rate, and the 68-d vector per cell.

* **`stratified_sample.py`** — ~120 lines new. Implements the DSI x PD quintile picker per
  cluster: bin each cluster's cells into 5 DSI quintiles x 5 PD quintiles (25 bins), walk in raster
  order taking one cell per occupied bin until 10 are selected. Top-up rule: pick the most-distant
  cell in standardised DSI x PD space until 10 are selected. Writes `selected_cells.csv` with all
  task-description-required columns.

* **`simulate_cell.py`** — ~250 lines new. Single-cell driver: take a 68-d vector + cell key,
  build the cell via `generate_fixed_morphology` + t0080 channel insertion +
  `apply_parameter_vector`, build the synapse bundle, then for each (mode, direction) pair: apply
  mode overrides, attach the appropriate recorder set (g_E in EPSP_PASSIVE, g_I in IPSP_PASSIVE, V_m
  in FULL), generate AR(2) noise + bar arrival + queue events, run h.run(), save the parquet, tear
  down. Uses the t0066 trial pattern + t0072 conductance recorders + the new mode-trio override
  applied per-mode.

* **`run_all_cells.py`** — ~80 lines new. Iterates `selected_cells.csv` row by row, sequentially
  in-process (no ProcessPoolExecutor per the NEURON-statefulness note); calls `simulate_cell` per
  cell; catches errors and writes `simulation_failures.csv`. The cell-build cleanup is
  delete-sections + remove-from-`_LIVE_CELLS` + del cell between cells. Reports per-cell timing and
  a running ETA. Total wall-clock estimate: 30-60 min for the 40 cells x 6 trials = 240 NEURON runs
  at ~3-15 s/run.

* **`extract_metrics.py`** — ~120 lines new. Reads all trace parquets per (cell, mode, direction),
  computes the 7 per-direction metrics listed in the task description, writes `per_cell_metrics.csv`
  with rows `(cell, direction)` and columns
  `(cluster_id, source_task, seed, generation, individual_idx, peak_g_e_us, peak_g_e_time_ms, peak_g_i_us, peak_g_i_time_ms, gi_ge_ratio_at_peak_ge, g_i_onset_latency_ms, n_spikes, mean_v_m_mv, max_v_m_mv)`.

* **`plot_cluster_figures.py`** — ~200 lines new. Renders the 4 per-cluster 10-row x 3-col trace
  grids (`cluster_<c>_traces.png`) and the cross-cluster 4-row x 3-col median summary
  (`cross_cluster_traces.png`). Within each panel, plot PD (solid) and ND (dashed) traces in one
  colour. Annotate each panel corner with the cell's (DSI, PD-rate). Cells within each cluster are
  ordered top-to-bottom by ascending DSI. Layout follows the task description verbatim.

## Lessons Learned

* **NEURON channel-suffix collision** [t0066]. NEURON cannot load the same MOD SUFFIX twice in one
  process. The t0066 `_ensure_neuron_loaded` (lines 70-89) patches t0024's `load_neuron` to be
  idempotent after the first call. t0118 inherits this fragility via t0106's bootstrap; the
  implementation must NOT call `nrn_load_dll` for the t0080 DLL more than once per process (delegate
  to `ensure_t80_dll_loaded`'s `_T80_DLL_LOADED` dict).

* **AIS section sourcing** [t0090, t0106]. The morphology-generated cell exposes an AIS via
  `MorphologyResult`, but t0106's `apply_parameter_vector` calls `update_ais_geometry` on the
  `AISExtension` dataclass which was originally designed for the t0024 base cell + t0078
  AIS-extension pattern. **Verify** that the morphology-generated AIS interface matches what
  `update_ais_geometry` expects before running the full 40-cell sweep. If they differ, either patch
  `update_ais_geometry` or skip it for procedurally-generated cells (the AIS length is already set
  during morphology generation via the `MorphologyParams.ais_length_um` field). **Action item for
  planner**: read `tasks/t0090_*/code/morphology_params.py:MorphologyResult` to confirm AIS
  attribute names and consult t0106's pattern.

* **DLL gitignore** [t0114, t0115]. `*.dll`-bearing `build/` folders are gitignored. t0114 and t0115
  both rebuilt the t0080 DLL on the remote Vast.ai machines using `compile_t0024_mods_linux`
  + `compile_t0080_mods_linux` (the latter not yet found in this read but referenced by line
    comments in t0080's bootstrap pattern). t0118 runs locally on Windows; the DLL must be available
    at `tasks/t0080_*/code/build/nrnmech.dll` before the first simulation starts. The implementation
    step should check `WINDOWS_MOD_BUILD_DLL.exists()` and either copy from the main repo or invoke
    `nrnivmodl.bat` on the worktree's mod sources.

* **`morph_seed` INT32 overflow** [t0109, t0117]. The 14-d morphology vector carries `morph_seed` as
  a float. Without the `% (2**31 - 1)` modulo before the `int()` cast, large GA-mutated seeds raise
  on the NEURON side. The t0117 `to_morph_params` (lines 73-76) is the canonical fix.

* **`_LIVE_CELLS` GC defense** [t0106, t0093 correction]. t0106's `generator_wrapper.py` line 38
  holds every built cell in a module-level list to prevent cell-id reuse after a partial GC. For a
  40-cell sequential run, this list will accumulate references — the implementation must either
  `_LIVE_CELLS.pop()` between cells (matching the new teardown pattern) or accept the RSS cost (40
  cells x ~50 MB / cell = 2 GB at worst, acceptable on a workstation but borderline).

* **Sequential per-cell, in-process** [t0117]. t0117 built ~150 morphologies in one process via
  `delete_section` cleanup, no subprocess needed. The same pattern works for t0118's 40 cells.
  Subprocess parallelisation via `ProcessPoolExecutor` is what t0106's NSGA-II driver does for scale
  (4-32 cells in parallel), but the per-cell wall-clock benefit is small for 40 cells and the
  implementation complexity is non-trivial. **Default to sequential**; validate parallel against
  sequential on a 4-cell subset only if the wall-clock budget is breached.

* **AR(2) release noise is seeded by trial** [t0106, t0066]. The t0106 evaluator uses
  `seed = SEED_BASE + s * 10_007 + int(angle) * 13` (line 372) to pseudo-randomise per (seed,
  direction). For t0118 reproducibility, use a fixed seed per (cell, mode, direction) so the PD and
  ND traces of one cell share the same noise realisation across modes (only mode changes; direction
  and noise stay fixed). Recommended seed: `SEED_BASE + cell_index * 10_007
  + direction_deg * 13`with`SEED_BASE = 117`(matching`SAMPLE_SEED`).

* **Bar-motion parameters are shared across the entire t0024 / t0080 / t0106 line** [t0024, t0106].
  `BAR_VELOCITY_UM_PER_MS = 1.0`, `BAR_X_START_UM = -40.0`, `BAR_START_TIME_MS = 0.0`,
  `BAR_WIDTH_UM = 250.0`. Any t0118 deviation from these breaks comparability with t0106 / t0112 /
  t0114 / t0115 DSI / PD-rate numbers (which the selected cells were ranked by).

## Recommendations for This Task

1. **Adopt the t0106 simulator stack verbatim, then bolt on mode-trio + conductance recording.**
   Copy `bootstrap.py`, `constants_electrophys.py`, `constants_morphology.py`, `extend_with_ais.py`,
   `parametric_placer.py`, `trial_helpers.py`, `generator_wrapper.py`, `apply_params.py` from
   `tasks/t0106_long_pdnd_nsga2_300gen/code/` into `tasks/t0118_*/code/`. Total: ~1100 lines. In
   each copied file, replace `tasks.t0106_long_pdnd_nsga2_300gen.code.*` self-references with
   `tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.*`.

2. **Use library imports for the morphology builder and HHst inserter.** Import
   `generate_fixed_morphology`, `MorphologyParams`, `MorphologyResult` directly from t0090 / t0092
   (registered libraries, allowed cross-task). Do NOT copy these.

3. **Verify the AIS interface match between procedurally-generated cells and
   `apply_parameter_vector`.** Specifically, read `MorphologyResult` and confirm `ais_proximal` /
   `ais_distal` attribute names match the `AISExtension` dataclass. If they differ, either skip
   `update_ais_geometry` (the AIS length is already set during morphology generation) or write an
   adapter that maps the procedurally-generated AIS section onto the AISExtension interface. **Read
   this before writing simulate_cell.py.**

4. **Implement the mode trio as fresh `apply_parameter_vector` calls + per-mode zeroing**, not as
   snapshot-and-restore. Per mode: (a) call `apply_parameter_vector(cell=cell, params=...)`; (b) for
   EPSP_PASSIVE / IPSP_PASSIVE, zero `gbar_<suffix>` for all 12 t80 channel suffixes
   + `gbar_skahpt80` + `HHst.gnabar/gkbar/gkmbar` on every segment of soma + all_dends +
     ais_proximal + ais_distal; (c) for EPSP_PASSIVE, also zero all `ncs_gaba[i].weight[0]`; for
     IPSP_PASSIVE, also zero all `ncs_ach[i].weight[0]` AND `ncs_nmda[i].weight[0]`.

5. **Record per-synapse `_ref_g` for the appropriate synapses in each passive mode**, then sum
   across synapses to get total `g_E(t)` / `g_I(t)`. Save the parquet with column names
   `t_ms, g_e_us, g_i_us, v_m_mv` per the task description, with missing-mode columns absent. Use
   `RECORD_DT_MS = 1.0` (1400 samples per trace) not 0.025 ms.

6. **Re-use the t0066 `_ensure_neuron_loaded` idempotent loader pattern** so re-running the
   simulator in a single Python session does not double-load mechanism SUFFIXes.

7. **Sequential in-process simulation with explicit teardown per cell.** Build cell -> apply params
   -> build bundle -> 6 trials (3 modes x 2 directions) -> teardown (delete sections, remove from
   `_LIVE_CELLS`, del cell). Use `contextlib.suppress(RuntimeError, AttributeError)` around
   `h.delete_section` calls per the t0117 pattern.

8. **Pre-flight check**: confirm `tasks/t0080_*/code/build/nrnmech.dll` exists in the worktree
   before the first simulation. If missing, the implementation must either copy from the main repo
   or `nrnivmodl.bat` on the mod sources. Document this in `plan.md` Verification Criteria as a hard
   prerequisite.

9. **Per-trial seeding**: `seed = SAMPLE_SEED + cell_index * 10_007 + int(direction_deg) * 13` so
   the PD and ND traces of one cell share their respective AR(2) realisations across modes (only the
   cell's electrophys + synapse-mask changes, not the stochastic input). This makes the per-cell
   EPSP_PASSIVE / IPSP_PASSIVE / FULL traces a clean "what does HH-on add on top of the passive g_E
   \+ g_I" comparison.

10. **Error handling**: wrap the per-cell simulation in try/except for (RuntimeError, ValueError,
    AssertionError, ArithmeticError). On failure, write a row to `simulation_failures.csv` and
    continue with the next cell. Do not abort the 40-cell run on a single bad cell.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port the de Rosenroll 2026 DSGC ModelDB entry
* **Status**: completed
* **Relevance**: Source of the canonical bar-motion parameters (`BAR_VELOCITY_UM_PER_MS`,
  `BAR_X_START_UM`, `BAR_WIDTH_UM`, `BAR_START_TIME_MS`) shared by t0080 / t0106 / t0112 / t0114 /
  t0115 / t0118. Also registers the `de_rosenroll_2026_dsgc` library whose internal AR(2) noise
  generator (`ar2_noise.generate_ar2_batch`) is reused by t0106 and inherited by t0118.

### [t0066]

* **Task ID**: `t0066_t0024_epsp_ipsp_vm_protocol`
* **Name**: EPSP / IPSP / FULL three-mode protocol on the t0024 de Rosenroll DSGC
* **Status**: completed
* **Relevance**: Canonical reference for the mode-trio invocation convention. Provides `TrialMode`
  and `Condition` StrEnums, the `_apply_mode_overrides` silencing pattern (lines 178-194), the
  `_run_one_trial` event-queue-then-run skeleton (lines 205-298), and the
  `_compute_dsi_from_full_trials` helper. t0118 copies this skeleton and adapts it for the 68-d
  substrate's 13 active channels and the NMDA NetCon zero-out for IPSP_PASSIVE.

### [t0072]

* **Task ID**: `t0072_synaptic_traces_pd_nd`
* **Name**: Per-synapse conductance and local-voltage traces on Bed A and Bed B
* **Status**: completed
* **Relevance**: Canonical reference for recording Exp2Syn `_ref_g` (lines 214-248 of
  `run_bed_b.py`). t0118 reuses this pattern to attach per-synapse g recorders for the ACh + NMDA
  synapses (EPSP_PASSIVE mode) and GABA synapses (IPSP_PASSIVE mode), sums across synapses to get
  total `g_E(t)` and `g_I(t)`. Also documents that Exp2Syn `_ref_g` is in uS (the canonical task
  convention).

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with AIS + dendritic-spike machinery, NSGA-II
* **Status**: completed
* **Relevance**: Owns the `de_rosenroll_2026_dsgc_ais_dendritic_spike` library that defines the 54-d
  ParameterVector + the 12 t80 channel suffixes + skahpt80 + the v3 dendritic-spike NMDA /
  distal-Nav / distal-NaP overlay. Owns the compiled NEURON DLL at
  `tasks/t0080_*/code/build/nrnmech.dll` (gitignored, must be re-supplied in the t0118 worktree).
  Owns `ensure_t80_dll_loaded` (the idempotent DLL loader) used by every downstream 68-d task
  including t0118.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator + diversity test
* **Status**: completed
* **Relevance**: Producer of the `procedural_dsgc_morphology_generator` library. Defines
  `MorphologyParams` (14-field frozen dataclass) and `MorphologyResult` (the cell wrapper with
  `h, soma, all_dends, terminal_dends, primary_dends, non_terminal_dends, terminal_locs_xy, origin_xy, section_endpoints_xy`).
  t0118 imports these classes to reconstruct cells from the 14-d morphology slice.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology-generator silence; fix soma-pt3d bug
* **Status**: completed
* **Relevance**: Producer of the `procedural_dsgc_morphology_generator_fix` library with the
  canonical `generate_fixed_morphology` entry. Also exposes `insert_baseline_channels` for HHst +
  cad insertion. t0118 imports both. Per `C-0093-01` correction overlay, this is the only morphology
  builder allowed in the t0118 build path.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long 2-direction NSGA-II at 300 gens
* **Status**: completed
* **Relevance**: Owner of the canonical 68-d simulator stack (`bootstrap.py`,
  `constants_electrophys.py`, `constants_morphology.py`, `generator_wrapper.py`, `apply_params.py`,
  `trial_helpers.py`, `evaluator.py`, `parametric_placer.py`, `extend_with_ais.py`,
  `build_cell_ais.py`). Per the cross-task code-reuse rule, every non-library piece of this stack
  must be **copied** into `tasks/t0118_*/code/`. The `evaluate_68d_vector` function (`evaluator.py`
  lines 379-444) is the canonical FULL-mode 68-d entry; t0118 adapts it for the three-mode trio with
  per-mode conductance recording.

### [t0109]

* **Task ID**: `t0109_t0108_morph_cluster_gallery`
* **Name**: Morphology gallery (10 per cluster) for t0108 morphology clusters
* **Status**: completed
* **Relevance**: Source of the canonical NEURON pt3d extraction + `h.delete_section` cleanup pattern
  (`build_cluster_gallery.py:_build_and_extract` lines 147-155) and the `morph_seed % (2**31 - 1)`
  coercion (line 130). t0118 inherits both patterns via t0117's `morphology_rendering.py` which
  already copied them.

### [t0112]

* **Task ID**: `t0112_t0106_seed77_replicate`
* **Name**: Seed-77 minimum-change replicate of t0106
* **Status**: completed
* **Relevance**: Second of the four source NSGA-II runs whose cells populate the t0117 pool.
  Confirms that the t0106 simulator stack is reusable verbatim across seeds (t0112 imported t0106's
  code without modification). Source seed 77 contributes to the t0117 unfiltered cohort.

### [t0114]

* **Task ID**: `t0114_seed7755_no_autostop`
* **Name**: Seed-7755 NSGA-II replicate of t0106 with auto-stop disabled
* **Status**: completed
* **Relevance**: Third of the four source NSGA-II runs in the t0117 pool. Same simulator stack as
  t0106 / t0112. Source seed 7755 dominates the t0117 unfiltered cohort by sheer evaluation count.

### [t0115]

* **Task ID**: `t0115_seed9354_no_autostop`
* **Name**: Seed-9354 NSGA-II replicate of t0106 with auto-stop disabled
* **Status**: completed
* **Relevance**: Fourth source NSGA-II run in the t0117 pool. Same simulator stack as t0106 / t0112
  / t0114. Source seed 9354.

### [t0116]

* **Task ID**: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
* **Name**: Pooled PCA + cluster + factor analysis at DSI > 0.7 ∧ PD > 10
* **Status**: completed
* **Relevance**: Closest research-code precedent. Owns the morphology rendering path (
  `code/morphology_rendering.py`) inherited from t0109; t0117 then re-inherited it from t0116.
  Documents the 68-d feature layout (`constants.py` ELECTROPHYS_PARAM_NAMES +
  MORPHOLOGY_PARAM_NAMES) shared by t0117 and t0118. Its `research/research_code.md` is the
  recommended starting point for the t0118 plan.

### [t0117]

* **Task ID**: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
* **Name**: Pooled PCA + cluster + factor analysis of all 4-seed cells (no DSI/PD filter)
* **Status**: completed
* **Relevance**: t0118's primary dependency. Produces `electrophys_clusters.csv` (the cluster
  assignments t0118 stratifies and re-simulates) and `pooled_all_cells.parquet` (the 68-d parameter
  vector per cell). Confirms the (source_task, seed, generation, individual_idx) primary key and the
  68-d column layout. Its `morphology_rendering.py` contains the `to_morph_params` helper (lines
  61-77) that t0118 copies verbatim for the 14-d morphology slice unpacking.
