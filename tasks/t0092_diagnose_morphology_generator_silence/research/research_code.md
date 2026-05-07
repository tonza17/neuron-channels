---
spec_version: "1"
task_id: "t0092_diagnose_morphology_generator_silence"
research_stage: "code"
tasks_reviewed: 5
tasks_cited: 5
libraries_found: 17
libraries_relevant: 3
date_completed: "2026-05-07"
status: "complete"
---
# Research Code: Diagnose t0090 Procedural-Cell Silence

## Task Objective

This task diagnoses why the t0090 procedural DSGC morphology generator produces 0 / 60 spiking cells
under the t0083 best-cell channel set. The deliverables are a side-by-side comparison of the
procedural BedB-equivalent cell vs the t0024 hand-coded Bed B cell, a ranked root-cause analysis,
and a fix delivered as a new sibling library `procedural_dsgc_morphology_generator_fix` plus an
answer asset that explains the root cause and recommends generator behaviour for t0091's planned
68-d joint NSGA-II run [t0090]. The task does not retune `BEDB_BASE_POINT` parameter values
exhaustively, does not enlarge morphology bounds, and does not repeat the full 60-morphology Phase D
sweep — those belong in t0091.

## Library Landscape

The library aggregator is not present in this branch
(`arf/scripts/aggregators/aggregate_libraries.py` does not exist), so the survey was performed by
walking `tasks/*/assets/library/*/details.json` directly — the same data the aggregator would
surface without correction overlays. **17 library assets** were discovered; **3 are directly
relevant** to this task. The full inventory:

| Library ID | Created by | Relevance |
| --- | --- | --- |
| `procedural_dsgc_morphology_generator` | t0090 | **Relevant** — the buggy generator under diagnosis |
| `de_rosenroll_2026_dsgc_ais_dendritic_spike` | t0080 | **Relevant** — `apply_parameter_vector`, `setup_synapses_parametric`, `run_one_trial`, `_section_midpoint_xy`, `_bar_arrival_times`; trial-driver harness consumed by both cells |
| `de_rosenroll_2026_dsgc` | t0024 | **Relevant** — hand-coded Bed B "ground truth" cell builder, AR(2) noise generator, bar-arrival timing constants |
| `de_rosenroll_2026_dsgc_ais` | t0078 | Not relevant — superseded by t0080's v3 substrate |
| `dsgc_active_channel_pack` | t0074 | Not relevant — independent Bed-A channel calibration line |
| `tuning_curve_loss` | t0012 | Not relevant — scoring library, no morphology code |
| `tuning_curve_viz` | t0011 | Not relevant — visualization only |
| `modeldb_189347_dsgc` | t0008 | Not relevant — Poleg-Polsky lineage, not Bed B |
| `modeldb_189347_dsgc_gabamod` | t0020 | Not relevant — Poleg-Polsky lineage |
| `modeldb_189347_dsgc_dendritic` | t0022 | Not relevant — Poleg-Polsky lineage |
| `modeldb_189347_dsgc_exact` | t0046 | Not relevant — Poleg-Polsky lineage |
| `minimal_dsgc_scalar_gaba` | t0052 | Reference only — uses pt3dadd-only construction (no `sec.L` set) |
| `minimal_dsgc_spatial_gaba` | t0053 | Reference only — same pt3dadd-only pattern |
| `minimal_dsgc_ampa_nmda_scalar_gaba` | t0054 | Reference only — same pattern |
| `minimal_dsgc_mg_block_nmda` | t0055 | Reference only — same pattern |
| `minimal_dsgc_tonic_gaba_sweep` | t0057 | Not relevant |
| `minimal_dsgc_bar_locked_gaba_ampa_sweep` | t0059 | Not relevant |

Aggregator output would otherwise reflect correction overlays; no library is the target of any
correction in this codebase, so the raw filesystem scan and a future corrected aggregator output
would match. Relevant import paths:

* `from tasks.t0090_morphology_generator_diversity_test.code.generator import generate_morphology`
* `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult`
* `from tasks.t0090_morphology_generator_diversity_test.code.constants import BEDB_BASE_POINT, PARENT_TIP_LOC, CHILD_BASE_LOC, StabilityKind`
* `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import apply_parameter_vector`
* `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais import DSGCCellWithAIS, build_dsgc_cell_with_ais`
* `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import run_one_trial`
* `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import setup_synapses_parametric, _section_midpoint_xy, _bar_arrival_times, _count_spikes`
* `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell, DSGCCell`
* `from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24`

## Key Findings

### How NEURON resolves `sec.L` after `pt3dadd`

The first candidate root cause flagged in the task description is whether t0090's pattern of setting
`sec.L = node.length_um` BEFORE calling `pt3dadd(start, end)` causes NEURON to silently override
`sec.L` with the Euclidean pt3d distance. The relevant t0090 sequence is at
`tasks/t0090_morphology_generator_diversity_test/code/generator.py:422-445` [t0090]:

```python
sec.L = float(node.length_um)
sec.diam = float(node.diameter_um)
sec.Ra = DEFAULT_RA_OHM_CM
sec.cm = DEFAULT_CM_UF_CM2
sec.nseg = _compute_nseg(h=h, section=sec)  # uses sec.L BEFORE pt3dadd
sec.push()
try:
    h.pt3dadd(node.start_xy[0], node.start_xy[1], 0.0, node.diameter_um)
    h.pt3dadd(node.end_xy[0], node.end_xy[1], 0.0, node.diameter_um)
finally:
    h.pop_section()
```

NEURON's documented behaviour: when `pt3dadd()` is called on a section, the cable length used by the
simulator is the cumulative Euclidean distance between successive pt3d points. This **overrides any
prior `sec.L` assignment unless `pt3dconst == 1`** (which is never set in this codebase). Confirming
the rule by comparing to the t0024 hand-coded HOC template
(`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/RGCmodelGD.hoc:211-252`):
the template calls `pt3dclear()` then a sequence of `pt3dadd(x, y, z, diam)` rows for each
compartment and **never sets `sec.L` explicitly** [t0024]. The t0024 builder also does not write
`sec.L` from Python (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:251-296`) — it
relies entirely on the HOC-derived pt3d geometry.

For the BedB-equivalent base point (`soma_offset_pd_um=0.0`, `field_elongation_pd=1.0`,
`branch_length_cv=0.1`), the asymmetry transform at `generator.py:333-355` [t0090] is a no-op for
both the soma_offset and elong terms, so for **straight radial primary stems** the Euclidean
distance between `start_xy` and `end_xy` equals `node.length_um` exactly, and the post-pt3dadd
`sec.L` matches the pre-pt3dadd assignment. For **non-primary recursive children**, however, the
`base_xy` is the parent's `end_xy` and the child's `end_xy` is computed at `generator.py:261-264` as
`base_xy + length_um * (cos angle_rad, sin angle_rad)`, so the Euclidean distance also matches
exactly. **Conclusion**: under the BedB base point the pt3d-vs-L mismatch should be exactly zero.
The pt3d-override rule is not the smoking gun for BedB silence, but it remains a real concern when
`field_elongation_pd > 1.0` (where elong stretches `(end_x - 0)` but does NOT scale `length_um`,
making post-pt3d `sec.L > node.length_um`) — this matters for the 5 STABLE-but-silent cells from
t0090 that have non-trivial asymmetry knobs.

### Section-list contract: `all_dends == terminal_dends + non_terminal_dends`?

The task description asks whether the procedural cell's `cell.all_dends` list contains the same
section objects as `cell.terminal_dends + cell.non_terminal_dends`. Reading `generator.py:416-471`
[t0090]: every `_Node` in `all_dend_nodes` is materialised into a section, appended to
`all_dend_secs`, then **separately classified** in a second loop:

```python
for node in all_dend_nodes:
    sec = sections_by_node[node.name]
    if node.is_primary:
        primary_secs.append(sec)
    if len(node.children) == 0:
        terminal_secs.append(sec)
    else:
        non_terminal_secs.append(sec)
```

Every node ends up in **either** `terminal_secs` (no children) **or** `non_terminal_secs` (has
children). The primary classification is **orthogonal**. So
**`all_dend_secs == terminal_secs + non_terminal_secs`** as section sets, and
`apply_parameter_vector` writes mid-tier OR terminal-tier densities to every dendrite section
exactly once during the stratified pass.

The t0024 cell uses `_map_tree` (`build_cell.py:140-168`), which appends a section to `non_terms`
**when the walk descends into it** (any section with children) and to `terminals` at leaves. Same
partition rule. **No silent omission or double-count** of dendrite sections in either cell. The
write order in `apply_params.py:206-211` writes PRIMARY before MID, so a primary stem that has
children (which is the typical case at `branch_prob_per_um=0.04`) gets PRIMARY-tier densities first
and then OVERWRITTEN with MID-tier densities. The t0024 cell exhibits the same overwrite pattern, so
the channel layout the procedural cell receives matches the t0024 cell's by construction [t0080].

### How `apply_parameter_vector` decides which sections receive which channel densities

Reading `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/apply_params.py:161-228` [t0080]: the
decision is **list-membership-based**, NOT name-based. The function reads `cell.soma`,
`cell.primary_dends`, `cell.non_terminal_dends`, `cell.terminal_dends`, `cell.ais_proximal`,
`cell.ais_distal` directly off the cell object and writes per-tier densities to each segment of each
section in those lists. It does NOT introspect section names like `dend[3]_t90` vs `dend[3]`. **This
is critical for the procedural cell**: as long as the `MorphologyResult` dataclass exposes the
correct section lists with the correct section objects in them, the procedural cell's `*_t90`-named
sections receive the same writes as the t0024 cell's sections. The procedural generator's section
names (`soma_t90`, `dend_p0_d1_n0_t90`, `ais_proximal_t90`, `ais_distal_t90`) play no role in
channel selection.

The function does, however, depend on each section having its 13 channel mechanisms and `cad`
already inserted (`apply_params.py:59-92`). The procedural cell does not call `insert("HHst")`
during `_materialise_neuron_sections`; the t0024 cell does it in `_configure_dends`. This gap is
patched in t0090 by `verification.py:_insert_baseline_channels`
(`tasks/t0090_morphology_generator_diversity_test/code/verification.py:125-137`) which inserts
`HHst` and `cad` on every soma + dendrite + AIS section before calling `apply_parameter_vector`
[t0090]. **Therefore channel insertion is correct**; it is not a candidate root cause.

### Synapse XY: `_section_midpoint_xy` reads from pt3dadd

`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_helpers.py:160-178` [t0080] computes
`_section_midpoint_xy` by calling `h.x3d(mid)` / `h.y3d(mid)` at the middle pt3d index. For a
section with only 2 pt3d points (the procedural cell's pattern), `n_pts == 2` so the function falls
into the even branch:

```python
a = n_pts // 2  # = 1
b = a - 1  # = 0
return ((h.x3d(1) + h.x3d(0)) / 2.0, (h.y3d(1) + h.y3d(0)) / 2.0)
```

This is the `(start + end) / 2` midpoint — **what the procedural generator intends**. So the
synapse XY readout matches the geometric midpoint of the procedural section exactly. The t0024 cell
has many pt3d points per section (real reconstructed morphology) so its midpoint is the geometric
midpoint of the real cable, which is also semantically correct. **Synapse XY readout is correct in
both cases**.

### Bar-arrival geometry: `cell.origin_xy` and PD-axis projection

`_bar_arrival_times` (`trial_helpers.py:64-76`) computes
`arrival_time = T_start + (proj - BAR_X_START_UM) / BAR_VELOCITY` where
`proj = (syn_xy - origin_xy) · direction_vector` [t0080]. With `BAR_START_TIME_MS=0`,
`BAR_X_START_UM=-40`, `BAR_VELOCITY_UM_PER_MS=1.0`, `TSTOP_MS=1400`, the bar sweeps over PD
coordinates from `proj=-40` (at t=0) to `proj=+1360` (at t=1400 ms). Synapses with `proj < -40`
would receive the bar **before t=0** and never see the trial's release events (events at `t<0` are
filtered by the `if t < TSTOP_MS:` guard but events at `t<0` are not filtered at the lower end —
they would simply be queued at t<0 and `nc.event(t)` with t<0 NEURON-disregards them; they would not
contribute to the post-init voltage trajectory).

For the t0024 hand-coded cell, the soma origin is around `(104.59, 123.486)` (from the HOC pt3d
points) [t0024]. `_find_origin` (`build_cell.py:109-137`) computes the dendritic-arbour bbox
centroid from all dendrite pt3d midpoints; the resulting `origin_xy` is offset from soma. For the
procedural cell, `origin_xy` is set to `soma_node.end_xy` which is `(0, 0) + soma_offset_pd_um` —
`(0, 0)` for the BedB base point (`generator.py:634`) [t0090]. The two cells use different absolute
coordinate frames but the relative synapse-to-origin geometry is what matters, and both cells
compute synapse XY in the same frame as their respective origin. **No origin-frame bug**.

The procedural BedB cell with `primary_branch_pd_concentration=0.0` distributes primary stems
uniformly in `[-π, π]`, so synapses spread roughly symmetrically around `(0, 0)`. About half have
`proj < -40` for the PD direction, which means about half of the synapses arrive at `t<0` and their
stimulus is wasted. The t0024 cell has a real reconstructed morphology where the dendritic arbour is
biased toward one side of the soma, and the bar protocol was originally calibrated for that
geometry. **This bar-vs-cell-geometry asymmetry is a genuine design issue that reduces the effective
synapse count by ~50% for the procedural BedB cell, but it does not zero them out** — the cell
should still see ~half its synapses fire and should produce some spikes.

### t0083 best-cell parameter vector loading and the 54-d shape

The t0083 Pareto front has 18 cells in
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json` [t0083]; each cell record
has fields `cell_index`, `generation`, `params`, `dsi`, `pd_rate_hz`, `is_unstable`, `peak_vm_mv`,
`elapsed_s`, `constraint_violation`, `is_feasible`. The `params` field is a list of 54 floats in the
natural-units order defined by the `ParamIndex` IntEnum at
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py:145-206` [t0080]:

* indices 0-24: 5 stratified channels x 5 tiers (Nav1.6, Kv3, NaP, BK, SK) for tiers (SOMA, PRIMARY,
  MID, TERMINAL, AIS)
* indices 25-31: 7 uniform-density channels (Kdr, Kv4, Nar, Ih, Cal, Cat, Kv7)
* indices 32-33: SK_E2 slow-AHP (gbar_soma_ais, tau_ca_multiplier)
* indices 34-46: 13 synaptic + passive parameters (Ra, cm, gleak, cad_depth, cad_taur, n_ach,
  n_gaba, rho0_ach, lambda_ach_um, rho0_gaba, lambda_gaba_um, w_ach_us, w_gaba_us)
* indices 47-48: 2 AIS geometry (length, diameter)
* indices 49-53: 5 dendritic-spike (gnmda_dend, mg_conc_mm, voff_nmda, nav16_dend_distal,
  nap_dend_distal)

`load_t0083_best_cell_param_vector`
(`tasks/t0090_morphology_generator_diversity_test/code/load_default_params.py:48-51`) selects the
`is_feasible=True ∧ is_unstable=False` cell with the highest `dsi`, converts its `params` list to
a numpy float64 array, and constructs `ParameterVector(values=...)`. The shape assertion at line 44
(`assert vals.shape == (N_PARAMS,)`) catches any drift from 54-d. **No loading bug** [t0090].

### Trial-driver event queueing

`run_one_trial` (`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_driver.py:137-249`)
queues synaptic events via `nc.event(t)` inside a closure passed to `h.FInitializeHandler` [t0080].
The events are gated by `if t < TSTOP_MS:` so events past TSTOP are dropped. **There is no lower
bound** on event times — events with `t<0` would be queued and NEURON would call them at `t=0` (or
ignore them, depending on version). For the procedural BedB cell, the half of synapses with
`proj<-40` would receive their entire firing-rate envelope at `t<0` and contribute zero to
post-`finitialize` events. The 8-direction protocol in `verification.py:170-188` runs one seed per
angle.

### Procedural-cell structural contract with `DSGCCellWithAIS`

`MorphologyResult` is declared at
`tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py:131-156` [t0090] and
exposes the fields
`h, rgc, soma, all_dends, primary_dends, non_terminal_dends, terminal_dends, terminal_locs_xy, origin_xy, ais_proximal, ais_distal, stability_flag, morphometric_summary, connectivity, section_endpoints_xy`.
The first 11 fields **exactly mirror** `DSGCCellWithAIS` at
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build_cell_ais.py:33-51` [t0080], which is why
the t0090 verification `cast(DSGCCellWithAIS, cell)` works. The four extra fields
(`stability_flag, morphometric_summary, connectivity, section_endpoints_xy`) are read by t0090
verification only and are invisible to `apply_parameter_vector`. **Duck-type contract is
satisfied**.

One subtle gap: `DSGCCellWithAIS` is a regular dataclass (not `frozen`), but `MorphologyResult` is
`frozen=True, slots=True`. `apply_parameter_vector` does not mutate any cell field directly — it
only writes to NEURON section attributes — so the frozen-ness does not break the contract [t0080].

### `_LIVE_CELLS` GC guard and the `_INSERTED_CELLS` cache

`tasks/t0090_morphology_generator_diversity_test/code/verification.py:118-122` [t0090] notes a
critical Python-NEURON interaction: when a procedural cell is built and then garbage-collected,
Python may **reuse its `id()`**. The t0080 `_INSERTED_CELLS: set[int]` cache
(`apply_params.py:56-57`) keys on `id(cell)`; if the cache contains a stale id, the new cell with
the same id is treated as already-inserted and `_insert_channels_once` becomes a no-op. The
verification code defends against this by appending each built cell to a module-level `_LIVE_CELLS`
list, keeping it alive for the whole sequential run. This guard works for sequential runs but
introduces a memory leak proportional to the number of morphologies verified.

This is a known-good pattern; not a candidate root cause for silence. But if the diagnostic in this
task launches both cells in the same process, the t0090 generator's `_get_neuron_h()`
process-singleton (`generator.py:70-107`) and the t0024 builder's separate `load_neuron()` will both
interact with the same `h` object. The t0024 builder calls `h.nrn_load_dll` for the t0024 DLL, and
t0090 calls it for the t0080 DLL; both calls are idempotent at the DLL-path level via
`_T80_DLL_LOADED` and t0024's DLL is loaded once-per-process by the t0090 `_get_neuron_h`. **Both
cells can coexist in the same process** for diagnostic comparison.

### Soma diameter conventions and unstimulated stability

The t0090 procedural soma is built as a single point with `sec.L = soma_diameter_um=15.0` and
`pt3dadd` at the same xy with `diam=15.0` (`generator.py:380-405`) [t0090]. NEURON treats this as a
1-segment cylinder of length 15 um and diameter 15 um, giving a soma surface area of π·15·15 ≈
706.86 µm². The t0024 hand-coded soma uses 7 pt3d points with diameters varying from 0.88 to 10.62
um and the spheroid-by-Frustums area is roughly 220 µm² (estimated from the pt3d table at
`RGCmodelGD.hoc:211-218`). **The two cells have ~3.2x different soma surface areas**. A larger soma
sinks more current and depolarises slower — under the same `apply_parameter_vector` writes, the
procedural cell's soma will charge to V_threshold more slowly than the t0024 soma, and the SAME
total dendritic input current may **fail to reach AP threshold at all** for the larger soma. This is
a strong candidate root cause and can be verified by comparing soma `area()` between the two cells
in the structural dump.

## Reusable Code and Assets

The following items will be reused for this task. **Cross-task import rule**: only libraries
registered in `assets/library/` may be imported across tasks. Non-library code must be **copied**
into the current task's `code/` directory.

* **Source**: `tasks/t0090_morphology_generator_diversity_test/code/generator.py` —
  `generate_morphology(params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`.
  Builds the procedural DSGC cell. **Reuse method**: **import via library**
  (`procedural_dsgc_morphology_generator`). **Adaptation**: none — call as-is to instantiate the
  buggy reference cell for the side-by-side comparison [t0090]. Approx. 642 lines.

* **Source**: `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` —
  `MorphologyParams` (frozen dataclass, 14 fields), `MorphologyResult` (frozen, 15 fields),
  `MorphometricSummary` (6 fields). **Reuse method**: **import via library**
  (`procedural_dsgc_morphology_generator`). **Adaptation**: none. Use
  `MorphologyParams.from_bedb_base_point()` to construct the BedB-equivalent input [t0090]. Approx.
  156 lines.

* **Source**: `tasks/t0090_morphology_generator_diversity_test/code/constants.py` —
  `BEDB_BASE_POINT` dict, `PARENT_TIP_LOC=1.0`, `CHILD_BASE_LOC=0.0`,
  `DEFAULT_DENDRITE_DIAMETER_UM=1.5`, `DEFAULT_TIP_DIAMETER_UM=0.4`, `AIS_DEFAULT_DIAMETER_UM=0.8`,
  `AIS_PROXIMAL_FRACTION=0.5`, `LAMBDA_F_FREQ_HZ=100`, `D_LAMBDA=0.1`, `StabilityKind` enum. **Reuse
  method**: **import via library** (`procedural_dsgc_morphology_generator`). **Adaptation**: none
  [t0090]. Approx. 187 lines.

* **Source**: `tasks/t0090_morphology_generator_diversity_test/code/load_default_params.py` —
  `load_t0083_best_cell_param_vector()`. Loads the 54-d t0083 best-cell `ParameterVector`. **Reuse
  method**: **import via library** (`procedural_dsgc_morphology_generator`). **Adaptation**: none
  [t0090]. Approx. 57 lines.

* **Source**: `tasks/t0090_morphology_generator_diversity_test/code/verification.py` —
  `_insert_baseline_channels(cell)`. Inserts `HHst` + `cad` on soma + dendrites + AIS. **Reuse
  method**: **copy into task** (this is a task-internal helper, not a library entry point).
  **Adaptation**: trim to the helper itself, ~12 lines [t0090].

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build_cell_ais.py` —
  `build_dsgc_cell_with_ais(*, ais_length_um, ais_diameter_um) -> DSGCCellWithAIS`. **Reuse
  method**: **import via library** (`de_rosenroll_2026_dsgc_ais_dendritic_spike`). **Adaptation**:
  pass `ais_length_um=31.0` to match `BEDB_BASE_POINT['ais_length_um']` [t0080]. Approx. 80 lines.

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/apply_params.py` —
  `apply_parameter_vector(*, cell: DSGCCellWithAIS, params: ParameterVector) -> None`. **Reuse
  method**: **import via library** (`de_rosenroll_2026_dsgc_ais_dendritic_spike`). **Adaptation**:
  none — works on both cell kinds via duck typing [t0080]. Approx. 229 lines.

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_helpers.py` —
  `setup_synapses_parametric(*, cell, n_ach, n_gaba, ...)` returns `SynapseBundle`;
  `_section_midpoint_xy(*, h, section) -> (float, float)`;
  `_bar_arrival_times(syn_xy, origin_xy, direction_deg) -> NDArray`;
  `_count_spikes(v_trace, threshold_mv) -> int`. **Reuse method**: **import via library**
  (`de_rosenroll_2026_dsgc_ais_dendritic_spike`). **Adaptation**: none [t0080]. Approx. 312 lines.

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_driver.py` —
  `run_one_trial(*, cell, bundle, direction_deg, seed) -> TrialResult`. **Reuse method**: **import
  via library** (`de_rosenroll_2026_dsgc_ais_dendritic_spike`). **Adaptation**: none [t0080].
  Approx. 427 lines.

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py` —
  `ParameterVector`, `ParamIndex`, `Tier`, `N_PARAMS=54`, `TSTOP_MS=1400`, `DT_MS`, `STEPS_PER_MS`,
  `SEED_BASE`, `PD_DIRECTION_DEG=0`, `ND_DIRECTION_DEG=180`, `AP_THRESHOLD_MV`,
  `STABILITY_PEAK_VM_MIN_MV=-80`, `STABILITY_PEAK_VM_MAX_MV=+60`. **Reuse method**: **import via
  library** (`de_rosenroll_2026_dsgc_ais_dendritic_spike`). **Adaptation**: none [t0080].

* **Source**: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` —
  `build_dsgc_cell() -> DSGCCell`, `_find_origin(h, dends)`, `_map_tree(h, cell)`,
  `_terminal_midpoint(h, dend)`. **Reuse method**: **import via library**
  (`de_rosenroll_2026_dsgc`). **Adaptation**: none — this is the hand-coded "ground truth" cell
  for the comparison [t0024]. Approx. 332 lines.

* **Source**: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` — `BAR_X_START_UM=-40`,
  `BAR_VELOCITY_UM_PER_MS=1.0`, `BAR_START_TIME_MS=0.0`, `AR2_PHI`, `AR2_BASE_RATE_HZ`,
  `AR2_INNOV_SCALE`, `RA_OHM_CM`, `CM_UF_CM2`, `GLEAK_S_CM2`. **Reuse method**: **import via
  library** (`de_rosenroll_2026_dsgc`). **Adaptation**: none [t0024].

## Architecture Overview

The diagnostic compares two cells through the same trial-driver harness:

1. **Procedural BedB cell**: `MorphologyParams.from_bedb_base_point()` →
   `generate_morphology(params, morph_seed=1234)` → `MorphologyResult` (~341 sections, soma at
   (0,0)).

2. **Hand-coded Bed B cell**: `build_dsgc_cell()` → `DSGCCell` from t0024 (HOC `RGCmodelGD.hoc`
   morphology, soma at ~(104, 122)).

3. **Wrap hand-coded cell with AIS**:
   `build_dsgc_cell_with_ais(ais_length_um=31.0, ais_diameter_um=0.8)` → `DSGCCellWithAIS`.

4. **Apply identical channel densities**: For both cells,
   `apply_parameter_vector(cell=..., params=t0083_best_cell)`.

5. **Place identical synapse counts via the same placer seed**:
   `setup_synapses_parametric(cell=..., placer_seed=42, ...)` for both cells, with all 13 synaptic
   parameters from the t0083 best-cell vector.

6. **Run a single PD-direction bar trial on each**:
   `run_one_trial(cell=..., bundle=..., direction_deg=0.0, seed=SEED_BASE)`.

7. **Compare**: soma Vm trace, peak Vm, spike count, EPSP area, synapse-XY distribution.

For the procedural cell, the channel densities are written to sections that NEURON sees as cables of
length `Euclidean(start_xy, end_xy)` (NOT `node.length_um`). For BedB-equivalent base point, those
two values are identical, so this is not a problem under the BedB base point but IS a problem under
non-trivial asymmetry knobs. The trial-driver harness consumes both cells through the duck-typed
`DSGCCellWithAIS` field interface; section names are irrelevant to the harness.

## Common Patterns

### Path-management pattern

Every reviewed task follows the same `paths.py` + `constants.py` split documented in the task rules:
paths centralised in `paths.py`, magic strings centralised as typed constants in `constants.py`. The
diagnostic should follow the same pattern with
`tasks/t0092_diagnose_morphology_generator_silence/code/paths.py` for `STRUCTURAL_COMPARISON_JSON`,
`SYNAPSE_COMPARISON_JSON`, `VM_TRACE_PROCEDURAL_NPY`, `VM_TRACE_HANDCODED_NPY`,
`ROOT_CAUSE_ANALYSIS_JSON`, `POST_FIX_VERIFICATION_JSON`, and image paths.

### NEURON DLL loading pattern

Both t0024 and t0080 use idempotent DLL loading via per-DLL boolean caches keyed on `id(h)`. The
diagnostic must NOT call `h.nrn_load_dll` twice for the same DLL in one process — that raises
`NEURON: The user defined name already exists`. Use the t0090 `_get_neuron_h()` singleton when both
cells coexist in one process.

### Channel insertion idempotency

NEURON `sec.insert("HHst")` is silently no-op on duplicate calls. Both `_configure_dends` (t0024)
and `_insert_baseline_channels` (t0090) rely on this. The diagnostic can call
`apply_parameter_vector` without worrying about double-insertion.

## Lessons Learned

* **The procedural generator's silence is not caused by a section-list contract bug.**
  `apply_parameter_vector` writes to `cell.primary_dends`, `cell.non_terminal_dends`,
  `cell.terminal_dends` and these are correctly populated by t0090's `_materialise_neuron_sections`
  [t0080] [t0090].

* **The most likely root cause is soma surface area.** The procedural soma is a 15 µm × 15 µm
  cylinder (706 µm² area) while the hand-coded soma is a multi-pt3d frustum stack (~220 µm²
  area). A larger soma needs ~3x more synaptic charge to reach threshold and is much harder for the
  t0083 best-cell channels (calibrated against the smaller hand-coded soma) to drive. This is
  testable in the structural dump by comparing `area()` between the two cells [t0024] [t0090].

* **The pt3d-vs-L override is a real concern only for non-trivial asymmetry knobs**
  (`field_elongation_pd > 1.0`, large `soma_offset_pd_um`). For the BedB base point both knobs are
  neutral, so this candidate is a secondary contributor at most for the BedB-equivalent cell. But it
  is a load-bearing concern for the 5 STABLE-from-t0090 cells the diagnostic re-runs in Phase F
  [t0090].

* **Synapse arrival-time geometry mismatch is real but partial.** Bar arrival times for synapses
  with `proj < -40` fall at `t<0` — ~half of the procedural cell's symmetric synapses are wasted
  per direction. Not zero spikes, but a substantial reduction in effective drive [t0080].

* **The t0090 verification harness is correctly defended against id-reuse GC bugs** by the
  `_LIVE_CELLS` module-level list (`verification.py:122`); imitate this pattern in any sequential
  diagnostic that builds many cells [t0090].

* **t0083 is feasibility-filtered by `is_feasible ∧ ¬is_unstable`.** The selected best-cell
  vector is guaranteed feasible against the AIS-Nav-ratio constraint and stable on the t0024 cell.
  No additional filtering is needed when loading the vector [t0083].

* **t0090's per-cell "0 spikes" stems from running the trial driver to completion** — the cells
  are STABLE during the 50 ms no-stim check, then the 8-direction protocol runs but every direction
  returns spike_count=0. This rules out a setup-time crash and points at a quantitative drive
  insufficiency, consistent with the soma-surface-area hypothesis [t0090].

## Recommendations for This Task

1. **Phase A first**: dump structural state for both cells. Include `sec.L` AS-WRITTEN by the
   builder code, `sec.L` AS-REPORTED-BY-NEURON after pt3d resolution, `sec.area()`, `sec.nseg`,
   `sec.diam`, all pt3d points, and connectivity. Confirm or refute the pt3d-vs-L override candidate
   quantitatively for the BedB base point. Save to `data/structural_comparison.json`.

2. **Compare soma area directly**: this is the leading hypothesis. If the procedural soma is 3.2x
   larger than the t0024 soma, the fix is to use a 7-pt3d stack mirroring the t0024 soma profile, or
   to set `pt3dclear()` then `pt3dadd(0, 0, 0, soma_diameter_um/2)`,
   `pt3dadd(0, 0, soma_diameter_um, soma_diameter_um/2)` to make NEURON treat it as a sphere of
   matching area, OR to keep the simple cylinder but match Bed B's soma area by setting both L and
   diam to the cube root of the target volume. **Recommendation**: in Phase E, fix soma geometry to
   deliver ~220 µm² area (matching the t0024 hand-coded cell) by either (a) emitting 7 pt3d points
   reproducing the t0024 frustum stack at scale `soma_diameter_um/15`, or (b) setting
   `sec.L = soma_diameter_um` and `sec.diam = soma_diameter_um / 3.2` so the cylinder area matches
   the hand-coded cell's at `soma_diameter_um=15`.

3. **Implement the fix as a thin wrapper if possible**: in `code/morphology_generator_fix.py` define
   `generate_fixed_morphology(*, params, morph_seed) -> MorphologyResult` that delegates to the
   t0090 `generate_morphology` and then patches the soma's pt3d points (using `h.pt3dclear` + new
   `h.pt3dadd` calls inside `soma.push() / pop_section()`). This keeps the API a drop-in replacement
   so t0091 can
   `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`
   and substitute it for `generate_morphology`.

4. **Validate with the hand-coded cell**: if Phase C shows the t0024 hand-coded Bed B cell ALSO
   fails to spike under the t0083 best-cell channels, the bug is in t0080's `apply_parameter_vector`
   or `load_default_params.py`, NOT in the t0090 generator. In that case stop, write the diagnosis
   as the answer asset, and flag a downstream task targeting t0080.

5. **Keep both cells in the same process**: use the t0090 `_get_neuron_h()` singleton and append
   each built cell to a `_LIVE_CELLS` list in this task's diagnostic driver to defend against GC id
   reuse during sequential builds.

6. **Reuse the t0083 best-cell loader directly**: import `load_t0083_best_cell_param_vector` from
   the t0090 library via the existing relative path
   `tasks.t0090_morphology_generator_diversity_test.code.load_default_params`. Do not re-implement
   the loader.

7. **Document the fix's API contract**: the answer asset `t0090-procedural-cell-silence-root-cause`
   should specify the exact call signature t0091 must use, the assertion that
   `generate_fixed_morphology` is feature-equivalent to `generate_morphology` for non-BedB base
   points, and any loss-of-determinism warning if the fix introduces additional pt3d points (which
   would change `sec.area()` and therefore per-segment current).

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Source of the hand-coded Bed B cell (`build_dsgc_cell`), the `RGCmodelGD.hoc`
  morphology template, the AR(2) noise generator, and bar timing constants. The "ground truth"
  comparison cell for this task's side-by-side diagnostic.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic spike machinery (NSGA-II)
* **Status**: completed
* **Relevance**: Source of `apply_parameter_vector`, `setup_synapses_parametric`, `run_one_trial`,
  `_section_midpoint_xy`, `_bar_arrival_times`, the 54-d `ParameterVector` definition, and the
  `DSGCCellWithAIS` interface. Core trial-driver harness for both cells.

### [t0083]

* **Task ID**: `t0083_bedb_v3_extend_nsga2_gen8plus`
* **Name**: Extend Bed B v3 NSGA-II from generation 8+
* **Status**: completed
* **Relevance**: Source of the 54-d best-cell parameter vector loaded from
  `results/data/pareto_front.json` and applied to both cells in the diagnostic. The vector is
  selected as `argmax(dsi)` over feasible non-unstable Pareto front cells.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator + diversity test + validation triplet
* **Status**: completed
* **Relevance**: The buggy generator under diagnosis. Source of `generate_morphology`,
  `MorphologyParams`, `MorphologyResult`, `BEDB_BASE_POINT`, `_insert_baseline_channels`,
  `load_t0083_best_cell_param_vector`, `_LIVE_CELLS` GC defense, and the verification result showing
  0/60 spiking cells.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B MOBO v2 with AIS-tiered AHP
* **Status**: completed
* **Relevance**: Predecessor of t0080; defined the original 49-d ParameterVector and AIS-tiered
  channel layout that t0080's v3 substrate extends to 54-d. Not directly imported but provides
  context for ParamIndex tier ordering.
