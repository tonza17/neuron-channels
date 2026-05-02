---
spec_version: "1"
task_id: "t0076_bedb_dsi_firing_rate_mobo"
research_stage: "code"
tasks_reviewed: 14
tasks_cited: 11
libraries_found: 14
libraries_relevant: 2
date_completed: "2026-05-01"
status: "complete"
---
# Research Code: Reusable Code Inventory for Bed B Channel + Synapse MOBO

## Task Objective

Build a 25-parameter Bayesian-optimisation loop on the Bed B (de Rosenroll 2026) DSGC that jointly
maximises direction selectivity (DSI) and PD firing rate via BoTorch qNEHVI. The implementation
needs (a) the Bed B cell builder and the moving-bar trial machinery [t0024], (b) the existing 5
soma-channel MOD files [t0067] plus 7 newly-vendored MODs (Kdr, KM, HCN, CaL, CaT, BK, SK) per the
just-completed `research_internet.md` MOD-source survey, (c) a parametric exponential-decay synapse
placer (the only genuinely new non-trivial code in t0076), (d) the t0072 per-synapse recorder for
diagnostic deep-dives of 3-5 best Pareto cells, and (e) the t0072 Typst PDF pipeline for the final
writeup. All compute runs on a Vast.ai 64-core CPU node.

## Library Landscape

The library aggregator script does not exist in `arf/scripts/aggregators/` (the asset-aggregator
suite registers `aggregate_tasks`, `aggregate_costs`, `aggregate_machines`, `aggregate_metrics`,
`aggregate_metric_results`, `aggregate_suggestions`, `aggregate_categories`, `aggregate_task_types`
only). Library assets were therefore enumerated by direct filesystem scan of
`tasks/*/assets/library/*/details.json`, which returned 14 registered libraries: `tuning_curve_loss`
(from [t0012]), `modeldb_189347_dsgc` (from [t0008]), `tuning_curve_viz` (from [t0011]),
`modeldb_189347_dsgc_gabamod` (from t0020_port_modeldb_189347_gabamod),
`modeldb_189347_dsgc_dendritic` (from t0022_modify_dsgc_channel_testbed), `de_rosenroll_2026_dsgc`
(from [t0024]), `modeldb_189347_dsgc_exact` (from t0046_reproduce_poleg_polsky_2016_exact),
`minimal_dsgc_scalar_gaba` (from t0052_minimal_dsgc_scalar_gaba), `minimal_dsgc_spatial_gaba` (from
t0053_minimal_dsgc_spatial_gaba), `minimal_dsgc_ampa_nmda_scalar_gaba` (from
t0054_minimal_dsgc_ampa_nmda_scalar_gaba), `minimal_dsgc_mg_block_nmda` (from
t0055_nmda_mg_block_dsi_recovery), `minimal_dsgc_tonic_gaba_sweep` (from
t0057_tonic_gaba_sweep_t0053), `minimal_dsgc_bar_locked_gaba_ampa_sweep` (from
t0059_bar_locked_gaba_ampa_sweep_t0057), and `dsgc_active_channel_pack` (from [t0074]).

Two libraries are directly relevant to t0076:

* **`de_rosenroll_2026_dsgc` v0.1.0** [t0024] — the Bed B substrate. Registered entry points are
  `build_dsgc_cell()`, `generate_ar2_batch()`, plus the four CLI scripts. Vendored sources
  (`RGCmodelGD.hoc`, `HHst_noiseless.mod`, `cadecay.mod`, `Exp2NMDA.mod`, `nrnmech.dll`) live in
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/`. Import
  path: `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell`.
  Critically, t0024's `cadecay.mod` is already in the Bed B vendored sources — the t0076 plan's
  Approach step 2 ("Add the `cad` calcium-accumulation mechanism if not already in the de Rosenroll
  port") is therefore already satisfied; the existing `cad` SUFFIX is reusable as-is.

* **`dsgc_active_channel_pack` v0.1.0** [t0074] — 8-channel MOD pack for Bed A: `nav16t74`,
  `napt74`, `nart74`, `kv3t74`, `kv4t74`, `bk74`, `sk74`, `kv7t74`, plus `cad` (the t0024 cadecay
  vendored verbatim). All under `t74` SUFFIX namespace. The MOD source files live in
  `tasks/t0074_channel_tuning_width_bed_a/code/mods/`. **This is a major non-obvious finding**: the
  BK, SK, and Kv7 channels that t0076's `research_internet.md` recommends sourcing from Hay 2011 /
  Khaliq 2003 are **already vendored in t0074 with the same provenance** (BK ← Mainen ModelDB 2488
  `kca.mod`, SK ← Hay 2011 `SK_E2.mod`, Kv7 ← Hay 2011 `Im.mod`). Per the cross-task rule these MOD
  files cannot be `import`-ed (NEURON loads them via `nrn_load_dll` not Python import), but they can
  be **copied** verbatim into `code/mods/` with SUFFIX renamed `t74` → `t76`. This collapses the
  t0076 vendoring step from 7 new MODs (Kdr, KM, HCN, CaL, CaT, BK, SK) to 4 new MODs (Kdr, HCN,
  CaL, CaT) plus 3 SUFFIX-renamed copies.

The remaining 12 libraries are not relevant: `tuning_curve_loss` and `tuning_curve_viz` operate on a
12-angle CSV and are out-of-scope for the BoTorch loop (t0076 reports DSI + spike rate directly, not
the t0012 envelope-fit metric); `modeldb_189347_*` and `minimal_dsgc_*` are Bed-A-specific
substrates (t0008 deposited Poleg-Polsky variants); the four `minimal_dsgc_*` libraries are toy-cell
experiments with no compatible morphology or synapse machinery for Bed B.

## Key Findings

### Bed B cell construction is a single-call entry point

`build_dsgc_cell()` [t0024], the registered `de_rosenroll_2026_dsgc` library entry point at
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:251-296`, returns a frozen `DSGCCell`
dataclass with `h`, `rgc`, `soma`, `all_dends` (350 sections), `primary_dends` (8 order-1 sections),
`non_terminal_dends` (165), `terminal_dends` (177), `terminal_locs_xy` (numpy `(177, 2)`), and
`origin_xy`. The function itself is 46 lines and idempotent only at the process level — calling it
twice in a single Python process throws "user defined name already exists: Exp2NMDA" because
`nrn_load_dll` is one-shot. The `_ensure_neuron_loaded()` pattern in
`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py:70-88` (15 lines) wraps the call to be
idempotent by monkey-patching `t0024.code.build_cell.load_neuron`. **Implication for t0076**:
`ProcessPoolExecutor` workers each get a fresh process, so the idempotency wrapper is unnecessary
inside workers; in the BoTorch driver process (which holds the GP and acquisition function but does
not run NEURON) `build_dsgc_cell` is never called. The workers can call `build_dsgc_cell` once at
worker init and reuse the cell across many trials by re-applying parameter overrides per trial — the
`CanonicalState` snapshot/restore pattern from `run_protocol.py:117-175` (60 lines) shows exactly
how to do this with per-segment HHst gnabar/gkbar/gkmbar plus per-NetCon weights.

### The 8-direction × 20-seed trial pattern is already factored out

`run_single_trial()` [t0024] at `run_tuning_curve.py:235-321` is the canonical 1-trial driver: takes
`(cell, ncs_ach, ncs_gaba, direction_deg, rho, seed)` and returns a `TrialResult` with `spike_count`
and `peak_mv`. Internally it (a) calls `_bar_arrival_times` to project synapse xy-locations onto a
velocity vector, (b) calls `_rates_with_ar2_noise` to draw Gaussian-windowed AR(2) rate traces for
ACh+GABA, (c) calls `_gaba_prob_for_direction` to pick the directional GABA release sigmoid, (d)
calls `_rates_to_events` to Poisson-sample event times, (e) installs a HOC `FInitializeHandler` to
queue the events into the NetCons via `nc.event(t)`, and (f) records `soma(0.5)._ref_v`, runs
`h.run()`, threshold-crosses to count spikes. The whole function is 87 lines. The same trial
machinery is reused verbatim in t0066 and t0072 — every downstream Bed B task imports the helpers
from t0024 [t0066, t0072]. **Implication for t0076**: the trial driver in `code/run_trial.py`
becomes a 30-40 line wrapper around `run_single_trial` that takes a 25-d parameter vector, applies
it to a freshly-built cell, runs (8 directions × 20 seeds = 160) trials, and returns
`(DSI, PD_firing_rate)`. The 8-direction angle list is already in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:87`
(`ANGLES_8DIR_DEG = (0, 45, 90, 135, 180, 225, 270, 315)`).

### Path-distance computation on Bed B uses `h.distance(soma_seg, target_seg)`

The parametric synapse placer (Approach step 3 of the task description) needs path distance from
soma to each candidate dendritic section. The canonical NEURON pattern in this project, used by
[t0050] at `tasks/t0050_audit_syn_distribution/code/extract_coordinates.py:172-202`, is the
two-segment form `h.distance(soma(0.5), target_seg)`. The same file documents (lines 168-177) that
the legacy single-argument form `h.distance(0, seg)` sets a stateful origin and should be avoided.
**Implication for t0076**: the placer in `code/synapse_placer.py` walks `cell.all_dends` (350
sections), calls `h.distance(cell.soma(0.5), sec(0.5))` per section to get path distance `d` in µm,
then computes weights `w_i = ρ_0 · exp(-d_i / λ) · L_i` (where `L_i` is the section length to make
selection length-uniform within a section), normalises, and samples `N` positions without
replacement weighted by `w`. There is no existing code that does this in the project (no prior task
uses an exponential-decay placer); the 7 prior tasks that compute path distance
[t0009, t0050, t0052, t0053, t0054, t0055, t0057, t0059] all use it for analysis or fixed placement,
never for stochastic exponential-density synapse placement. This is the only genuinely new
non-trivial code in t0076.

### Project's MOD-vendoring convention is well-established

The t0067 precedent [t0067] at `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/`
established the `tNN`-suffix namespace convention (`nav16t67`, `napt67`, `nart67`, `kv3t67`,
`kv4t67`) with a 4-line citation header, and the t0074 precedent [t0074] at
`tasks/t0074_channel_tuning_width_bed_a/code/mods/` extended this with `bk74`, `sk74`, `kv7t74` plus
a SUFFIX-renamed copy of `cadecay.mod` (`cad` SUFFIX preserved because the soma already inserts
`cad` from t0024's library). The compilation step uses
`tasks/t0074_channel_tuning_width_bed_a/code/run_nrnivmodl.cmd` (12 lines), which is a thin wrapper
around `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat`. The compiled `nrnmech.dll` lands in
`code/build/`, and `_ensure_t67_dll_loaded()` at
`tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py:107-120` (14 lines) loads it on top
of the Bed B DLL via a second `nrn_load_dll` call. NEURON allows multiple DLLs as long as no SUFFIX
collides — the `tNN` namespace guarantees this.

### NaP and NaR from t0067 are not used in t0076 per task description

The task description explicitly lists 12 channels (Nav1.6, NaP, NaR, Kdr, Kv3, Kv4, KM, HCN, CaL,
CaT, BK, SK) but the `research_internet.md` recommends Mainen's `kv.mod` for Kdr (not already
vendored) and the t0067/t0074 packs already provide Nav1.6, NaP, NaR, Kv3, Kv4. So the t0076 channel
set is the **union** of {t0067 5 channels} ∪ {t0074 BK/SK/Kv7=KM} ∪ {4 new MODs: Kdr, HCN, CaL,
CaT}. NaP and NaR ARE included per the parameter table in `task_description.md` lines 41-43
(parameters 2 and 3 of the 12 channel densities), so the prompt's claim that "t0076 won't use NaP or
NaR" appears to be a misreading — both are in the 12-channel list and need to be vendored from
t0067.

### Per-synapse recorder for the 3-5 Pareto deep-dives is one drop-in module

For the diagnostic deep-dive of representative Pareto cells (REQ-6 of the task description),
`_attach_bed_b_recorders()` [t0072] at `tasks/t0072_synaptic_traces_pd_nd/code/run_bed_b.py:214-248`
(35 lines) records `g_ACh`, `g_GABA`, and `v_local` per synapse via
`Vector.record(syn._ref_g, RECORD_DT_MS)` and `Vector.record(seg._ref_v, RECORD_DT_MS)`. The
`BedBRecorders` dataclass and the `_save_one_type` / `_save_bed_b_direction` helpers
(`run_bed_b.py:298-327`, ~30 lines combined) serialise the recorded vectors into `.npz` per
(direction, synapse_type). **Implication**: the 3-5 best Pareto cells get one `.npz` triple each (PD
ACh + PD GABA + ND ACh + ND GABA = 4 files per cell), wired through the same recorder. ~80 lines of
t0072 code is copy-paste reusable.

### Typst PDF render is a 60-line copy-paste

`render_pdf.py` [t0072] at `tasks/t0072_synaptic_traces_pd_nd/code/render_pdf.py` (64 lines total)
is itself a verbatim copy from t0071's render_pdf.py. The pattern is: read
`results/results_detailed.typ`, call `typst.compile(source, output=PDF_OUTPUT_PATH)`, assert PDF
size > 50 KB. The `typst` Python package is already in the project's `pyproject.toml` line 48
(`"typst>=0.14.8"`). For t0076, copy `render_pdf.py` verbatim, retarget the `paths` import.

### NEURON deployment on Vast.ai has no project precedent

`uv run python -u -m arf.scripts.aggregators.aggregate_machines --format json` returns
`total_machines: 0` and `tasks: []`. Similarly `aggregate_costs` shows `total_cost_usd: 0.0` across
all 68 cost records. **No prior task in this project has provisioned a Vast.ai instance.** t0076 is
the first compute-intensive remote task. The setup-remote-machine skill
[`arf/skills/setup-remote-machine/SKILL.md`] documents the Vast.ai search → create → verify →
environment-prep → teardown lifecycle in detail (471 lines), but it is GPU-oriented (uses
`pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel` as the default image, runs `torch.cuda.is_available()`
as the smoke test, queries `nvidia-smi`). For t0076's CPU-only NEURON workload these defaults need
adaptation: drop the `gpu_ram` filter and `compute_cap` filter, use a CPU-only image (e.g.,
`python:3.12-bookworm`), use `python -c "from neuron import h; print(h.HocError.__name__)"` as the
smoke test. NEURON itself has no PyPI wheel for Linux Python 3.13 (the local install path
`C:\Users\md1avn\nrn-8.2.7` is Windows-only), so NEURON 8.2 must be installed on the remote via
`pip install neuron==8.2.7` (which DOES have a Linux cp312/cp313 wheel) and the MOD files compiled
remotely with `nrnivmodl code/mods/`.

## Reusable Code and Assets

### `build_dsgc_cell()` — Bed B cell construction (import via library)

* **Source**: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:251-296` [t0024]
* **What it does**: Loads NEURON 8.2.7, sources `RGCmodelGD.hoc`, instantiates `h.DSGC(0,0)`, walks
  the dendritic tree, configures every section with HHst + cad, returns a frozen `DSGCCell`
  dataclass with `h`, `rgc`, `soma`, `all_dends` (350), `primary_dends` (8), `non_terminal_dends`
  (165), `terminal_dends` (177), `terminal_locs_xy` (177×2 numpy), `origin_xy`.
* **Reuse method**: **import via library**.
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell, DSGCCell`
* **Function signature**: `def build_dsgc_cell() -> DSGCCell`
* **Adaptation needed**: NONE for cell construction, but t0076 must call the function ONCE per
  worker process (in `ProcessPoolExecutor` initializer), then re-apply 25-d parameter overrides per
  trial via the t0066 `_apply_mode_overrides` pattern (see below).
* **Line count**: 0 to copy (library import).

### t0066 `CanonicalState` snapshot/restore + `_apply_mode_overrides` (copy into task)

* **Source**: `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py:117-194` [t0066]
* **What it does**: `_snapshot_canonical_state(cell, bundle)` walks every section's segments,
  records baseline `HHst.gnabar/gkbar/gkmbar` plus baseline NetCon weights into a `CanonicalState`
  dataclass; `_restore_canonical_state(bundle, state)` writes them back;
  `_apply_mode_overrides(cell, bundle, mode)` applies per-mode silencing.
* **Reuse method**: **copy into task** (`run_protocol.py` is not a registered library entry point).
  Adapt the snapshot to also capture the 12 new channel densities (one per `tNN` SUFFIX); rewrite
  `_apply_mode_overrides` as `_apply_parameter_overrides(cell, bundle, params)` taking the 25-d
  parameter vector and writing the 12 channel densities + 3 passive
  + 2 calcium + 2 weights to all sections, per-segment.
* **Function signatures**:
  * `def _snapshot_canonical_state(*, cell: DSGCCell, bundle: SynapseBundle) -> CanonicalState`
  * `def _restore_canonical_state(*, bundle: SynapseBundle, state: CanonicalState) -> None`
* **Line count**: ~80 lines to copy and adapt for the t0076 25-d parameter override.

### t0024 trial-driver helpers — `_setup_synapses`, `SynapseBundle`, `_bar_arrival_times`, `_rates_with_ar2_noise`, `_gaba_prob_for_direction`, `_rates_to_events`, `_count_spikes`, `BASE_ACH_PROB`, `RATE_DT_MS`, `BAR_SIGMA_MS` (copy into task)

* **Source**: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:52-232` [t0024]
* **What it does**: Module-level constants for the bar geometry; `_setup_synapses` creates ACh+GABA
  Exp2Syn pairs on every terminal dendrite with NetStim+NetCon sources; `SynapseBundle` dataclass
  holds the strong refs; `_bar_arrival_times` projects synapse xy onto a velocity vector;
  `_rates_with_ar2_noise` returns the Gaussian-windowed AR(2) rate traces;
  `_gaba_prob_for_direction` is the per-direction GABA release sigmoid; `_rates_to_events`
  Poisson-samples event times; `_count_spikes` threshold-crosses for spike count.
* **Reuse method**: **copy into task** (these are private helpers in `run_tuning_curve.py`, not
  registered as library entry points; the same copy-precedent is established by t0066 and t0072 —
  see t0072's `run_bed_b.py:13-16` "COPIED verbatim from t0024 lines 52-232" comment).
* **Function signatures**:
  * `def _setup_synapses(*, cell: DSGCCell, gaba_weight_scale: float) -> SynapseBundle` — for t0076,
    must be ADAPTED to accept (N_ACh, N_GABA, ρ_0_ACh, λ_ACh, ρ_0_GABA, λ_GABA) and use the new
    parametric placer instead of the fixed `for dend in cell.terminal_dends` loop.
  * `def _bar_arrival_times(syn_xy, origin_xy, direction_deg) -> NDArray[np.float64]` — copy
    verbatim.
  * `def _rates_with_ar2_noise(*, n_syn, n_bins, rate_dt_ms, arrival_times_ms, rho, seed) -> tuple[NDArray, NDArray]`
    — copy verbatim.
  * `def _gaba_prob_for_direction(direction_deg: float) -> float` — copy verbatim.
  * `def _rates_to_events(*, rates_hz, release_prob, rate_dt_ms, rng) -> list[list[float]]` — copy
    verbatim.
  * `def _count_spikes(v_trace, threshold_mv) -> int` — copy verbatim.
* **Line count**: ~180 lines (the 52-232 block); ~30 of those are the `_setup_synapses` body that
  t0076 must rewrite to use the parametric placer.

### t0024 `run_single_trial()` — 1-trial wrapper with FInitializeHandler (copy into task)

* **Source**: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:235-321` [t0024]
* **What it does**: Glues all the helpers together for one (direction, seed) trial, queues events
  via `FInitializeHandler`, records soma voltage, runs `h.run()`, returns spike count and peak
  voltage in a `TrialResult` dataclass.
* **Reuse method**: **copy into task** (private function). Adapt to take the new
  `bundle.ncs_ach`/`ncs_gaba` from the parametric placer (length is now `N_ACh`/`N_GABA`, not always
  177); add a try/except around `h.run()` that returns the worst-case score `(DSI=-1.0, rate=0.0)`
  on `RuntimeError` per Risk #4 of the task plan.
* **Function signature**:
  `def run_single_trial(*, cell, ncs_ach, ncs_gaba, direction_deg, rho, seed) -> TrialResult`
* **Line count**: ~87 lines.

### t0067 5-channel MOD pack — Nav1.6, NaP, NaR, Kv3, Kv4 (copy into task)

* **Source**:
  `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/{nav16t67,napt67,nart67, kv3t67,kv4t67}.mod`
  [t0067]
* **What it does**: 5 NMODL files defining `SUFFIX nav16t67`, `napt67`, `nart67`, `kv3t67`,
  `kv4t67`, each `NONSPECIFIC_CURRENT i` to avoid the HHst USEION conflict, with literature V_half /
  tau values per the t0067 citation headers.
* **Reuse method**: **copy into task**. Copy verbatim into `code/mods/` and rename SUFFIX `t67` →
  `t76` (also rename file basename) per the t0074 precedent. Reverify each compiles with `nrnivmodl`
  BEFORE wiring up BoTorch (per `research_internet.md` recommendation 5).
* **Line count**: ~50 lines per MOD × 5 MODs = ~250 lines.

### t0074 BK + SK + Kv7 (= KM) MOD pack (copy into task)

* **Source**: `tasks/t0074_channel_tuning_width_bed_a/code/mods/{bk74,sk74,kv7t74}.mod` [t0074]
* **What it does**: 3 NMODL files defining `SUFFIX bk74` (Mainen-Sejnowski `kca.mod`-derived BK,
  voltage- and Ca-dependent), `sk74` (Hay 2011 `SK_E2`-derived SK, purely Ca-driven Hill = 4.8),
  `kv7t74` (Hay 2011 `Im`-derived Kv7/M-current, Adams 1982 alpha/beta formalism). All three use
  `USEION ca READ cai` (BK, SK) and `NONSPECIFIC_CURRENT i` to avoid HHst conflicts.
* **Reuse method**: **copy into task**. Copy verbatim into `code/mods/` and rename SUFFIX `t74` →
  `t76`. **CRITICAL**: this collapses the Approach step 1 of the task description from "vendor 6-7
  NEW MODs" to "vendor 4 new MODs (Kdr, HCN, CaL, CaT) + reuse 3 existing (BK, SK, KM=Kv7) + reuse 5
  existing (Nav1.6, NaP, NaR, Kv3, Kv4)". Net: only **4 truly new MODs** to source from
  `research_internet.md`'s Hay-2011-and-Mainen recipe. The KM mapping works because
  `research_internet.md` recommends Hay 2011 `Im.mod` for KM, which is exactly what t0074's
  `kv7t74.mod` is derived from.
* **Line count**: ~50 lines per MOD × 3 MODs = ~150 lines.

### t0024 `cad` (cadecay) — already vendored in Bed B (no action)

* **Source**:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`
  [t0024]
* **What it does**: Single-shell calcium pool with `depth = 0.1 µm`, `taur = 5 ms`, Destexhe 1995
  formalism; SUFFIX is `cad`. Already inserted on every Bed B section by `_configure_soma` and
  `_configure_dends` in `build_cell.py:192-248`.
* **Reuse method**: **import via library** (transitively, via `build_dsgc_cell`). NO copy needed.
  The t0076 25-d parameter vector exposes `cad.depth` (param 16, range 0.05-0.5 µm) and `cad.taur`
  (param 17, range 5-100 ms) as RANGE variables of the existing `cad` SUFFIX, so the parameter
  override step writes them per-segment as `seg.cad.depth = depth_um` and `seg.cad.taur = taur_ms`.
* **Line count**: 0 (already loaded by `build_dsgc_cell`).

### t0067 `_ensure_t67_dll_loaded()` pattern (copy into task)

* **Source**: `tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py:107-120` [t0067]
* **What it does**: Idempotent loader that calls `h.nrn_load_dll(t76_dll_path)` once per process,
  asserting `rc == 1.0`, gating on a function-attribute flag.
* **Reuse method**: **copy into task** (private function). Adapt the DLL path to the t0076 build
  location (`tasks/t0076_*/code/build/nrnmech.dll`). The function is called inside each
  `ProcessPoolExecutor` worker AFTER `build_dsgc_cell` (which loads t0024's DLL) and BEFORE any
  t76-SUFFIX `insert()` call.
* **Function signature**: `def _ensure_t76_dll_loaded(*, h: Any) -> None`
* **Line count**: ~14 lines.

### t0072 per-synapse recorder for Pareto deep-dives (copy into task)

* **Source**: `tasks/t0072_synaptic_traces_pd_nd/code/run_bed_b.py:203-327` [t0072]
* **What it does**: `_attach_bed_b_recorders()` (35 lines) creates
  `Vector.record(syn._ref_g, RECORD_DT_MS)` for ACh and GABA Exp2Syn `_ref_g` plus a
  `Vector.record(seg._ref_v, ...)` for the local membrane voltage at the synapse insertion point per
  terminal. `BedBRecorders` dataclass holds the strong refs; `_save_one_type` and
  `_save_bed_b_direction` serialise to `.npz` per direction.
* **Reuse method**: **copy into task** (private functions). Reusable verbatim with the new
  parametric `bundle` (the recorder iterates `bundle.syns_ach` and `bundle.syns_gaba` which works
  regardless of the new variable count `N_ACh, N_GABA`).
* **Function signatures**:
  * `def _attach_bed_b_recorders(*, h: Any, bundle: SynapseBundle) -> BedBRecorders`
  * `def _save_one_type(*, output_path: Path, g_vectors, v_vectors, t_rec, e_rev_mv) -> None`
* **Line count**: ~125 lines.

### t0072 Typst PDF compile pipeline (copy into task)

* **Source**: `tasks/t0072_synaptic_traces_pd_nd/code/render_pdf.py:1-64` [t0072]
* **What it does**: 64-line script that calls `typst.compile(source, output=PDF_OUTPUT_PATH)`,
  asserts the produced PDF is at least 50 KB; the `typst` Python package is already in
  `pyproject.toml` line 48.
* **Reuse method**: **copy into task** verbatim, retarget the `paths` import from
  `tasks.t0072_synaptic_traces_pd_nd.code.paths` to
  `tasks.t0076_bedb_dsi_firing_rate_mobo.code.paths`.
* **Function signature**:
  `def compile_typst(*, source_path: Path, output_path: Path) -> CompileResult`
* **Line count**: 64 lines (verbatim).

### t0024 / t0074 `run_nrnivmodl.cmd` pattern (copy into task)

* **Source**: `tasks/t0074_channel_tuning_width_bed_a/code/run_nrnivmodl.cmd:1-12` [t0074]
* **What it does**: 12-line Windows batch that hardcodes
  `C:\Users\md1avn\nrn-8.2.7\bin\ nrnivmodl.bat`, runs it on `code/mods/`, emits
  `code/build/nrnmech.dll`.
* **Reuse method**: **copy into task** verbatim. Note that on Vast.ai (Linux) the equivalent is
  `cd code/mods && nrnivmodl .` — Linux NEURON's `nrnivmodl` script is bundled with the
  `pip install neuron==8.2.7` wheel and ends up on the worker `PATH` by default. The `.cmd` file is
  local-only; the remote uses a 1-line shell command.
* **Line count**: 12 lines.

## New Code Needed (no prior task implements this)

| Module | Purpose | Approx LOC |
| --- | --- | --- |
| `code/synapse_placer.py` | Walk `cell.all_dends` (350 sections), compute path-distance per section midpoint via `h.distance(cell.soma(0.5), sec(0.5))`, build per-section weight `w = ρ_0 · exp(-d/λ) · L`, normalise, sample `N` positions without replacement weighted by `w`. Returns a list of `(sec, position_in_01)` tuples that the new `_setup_synapses` consumes. | ~90 |
| `code/parameter_vector.py` | Frozen 25-d `ParameterVector` dataclass plus `from_botorch(x: torch.Tensor) -> ParameterVector` for the 12 channel-density log-mappings, 3 passive linear/log mappings, 2 calcium linear, 2 synapse counts (int rounding from continuous), 4 spatial-rule values, 2 weight log-mappings. The 12-channel SUFFIX-list lives here as a tuple of constants. | ~120 |
| `code/apply_parameters.py` | Given a `ParameterVector` and a freshly built `DSGCCell`, write the 12 new channel densities + 3 passive + 2 calcium + 2 weights to all segments, swap the synapse bundle to a new one built via `synapse_placer`. ~50 lines for channel-density writes, ~30 for the placer-driven `_setup_synapses` call. | ~100 |
| `code/run_trial.py` | Single-trial driver compatible with `ProcessPoolExecutor`: takes a `(ParameterVector, direction_deg, seed)` triple, builds (or reuses) a Bed B cell, applies parameters, calls the adapted `run_single_trial`, returns `(spike_count, peak_mv)`. Wraps `h.run()` in try/except for the NaN/error fallback (Risk #4). | ~80 |
| `code/run_botorch.py` | Main BoTorch loop: 30-Sobol DOE, 25→2 multi-task GP, qNEHVI acquisition with reference point `(DSI=0, rate=0)`, 300-500 acquisition steps. Each step: ask 1 candidate, dispatch 160 trials via `ProcessPoolExecutor(max_workers=64)`, aggregate to `(DSI, PD_rate)`, tell. Save trial summaries to `data/trial_history.parquet` after each step. | ~280 |
| `code/plot_pareto.py` | Plot the Pareto front at iter 50, 100, 200, 300, ..., final; plot hypervolume trajectory; pick 3-5 representative Pareto cells and dispatch deep-dive runs through the t0072 recorder. | ~250 |
| `code/render_pdf.py` | Verbatim copy from t0072 (`render_pdf.py`) with paths retargeted. | 64 |
| `code/mods/{kdr76,iht76,calt76,catt76}.mod` | Newly vendored MODs per `research_internet.md`: Mainen `kv.mod` for Kdr, Hay `Ih.mod` for HCN, Hay `Ca_HVA.mod` for CaL, Hay `Ca_LVAst.mod` for CaT. Add citation header per t0067 convention. | ~50 each = ~200 |
| `code/run_nrnivmodl.cmd` + `run_nrnivmodl.sh` | Windows + Linux compile wrappers. | ~25 combined |

Total new code: ~1,200 LOC. Total copied code: ~700 LOC. Total imported code: 0 LOC (all cross-task
code copied per the project rule, except `build_dsgc_cell` which is library-imported).

## NEURON Deployment on Vast.ai

This subsection captures the implementation pattern for getting NEURON 8.2.7 + the t0076 MOD library
running on a Vast.ai 64-core CPU node. **No prior task in this project has used Vast.ai**
(`aggregate_machines` returns `total_machines: 0`); the patterns here are derived from the
setup-remote-machine skill at `arf/skills/setup-remote-machine/SKILL.md` adapted from its
GPU-focused defaults to CPU-only.

### `pyproject.toml` dependencies

The project's current `pyproject.toml:36-49` pins `openai>=1.0`, `pydantic>=2.0`, `pyyaml>=6.0`,
`tqdm>=4.0`, `pymupdf>=1.27.2.2`, `vastai>=1.0.1`, `matplotlib>=3.10.8`, `pandas>=3.0.2`,
`numpy>=2.4.4`, `scipy>=1.17.1`, `typst>=0.14.8`. Three packages need to be added for t0076:

* `neuron==8.2.7` — Linux cp312 wheel exists on PyPI; the local Windows install at
  `C:\Users\md1avn\nrn-8.2.7` is NOT used on the remote.
* `botorch>=0.12` — multi-objective Bayesian optimisation; pulls in `gpytorch>=1.13` and
  `torch>=2.4` transitively. Per task plan Risk #7, total install footprint is ~2 GB. The `torch`
  dep can be CPU-only (`torch>=2.4+cpu`) which roughly halves the install.
* `pyarrow>=15.0` — for `data/trial_history.parquet` (BoTorch trial history serialisation; Parquet
  is faster than JSON for the 300-500 × 160 trials × 25 params × 2 metrics matrix).

### Vast.ai search query (CPU-only adaptation)

The setup-remote-machine skill's default `vastai search offers` query at SKILL.md:76-82 includes
`num_gpus=1 gpu_ram>=<X>` plus `compute_cap<1200`. For t0076's CPU-only workload, the adapted query
is:

```bash
vastai search offers \
  'num_gpus=0 cpu_cores>=64 cpu_ram>=64 disk_space>=20 \
  reliability>0.98 rentable=true verified=true' \
  --order 'dph' --limit 20 --raw
```

Per task description Cost estimation, expected pricing is $0.20-$0.60/hr for a 64-core CPU node.
Reliability threshold is `>0.98` per the 1-5h estimated runtime tier (task description: 2.5-4h
compute + 10-20 min provisioning + 5 min teardown).

### Vast.ai instance image

The default GPU image `pytorch/pytorch:2.6.0-cuda12.6-cudnn9-devel` (SKILL.md:158) is wrong for this
CPU workload. The recommended image is `python:3.12-bookworm` (~1.2 GB, includes pip and gcc), which
gives the freedom to `pip install neuron==8.2.7` cleanly. Smaller alternatives like
`python:3.12-slim` (60 MB) lack the C compiler that `nrnivmodl` needs to compile the t0076 MOD files
on the remote.

### Remote setup sequence (one-shot tmux command)

```bash
# Inside tmux session "work" on the remote:
apt-get update && apt-get install -y --no-install-recommends \
  build-essential libncurses5-dev libreadline-dev libxext-dev libxt-dev libxmu-dev mpich
pip install --no-cache-dir uv
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip sync requirements.txt    # rsync'd from local pyproject.toml export
cd /root/code/mods && nrnivmodl .   # compiles MODs into /root/code/mods/x86_64/
cd /root && python -u -m tasks.t0076_bedb_dsi_firing_rate_mobo.code.run_botorch \
  --n-iterations 400 --workers 64 > /root/output.log 2>&1
echo DONE >> /root/output.log
```

The `nrnivmodl` step (line 7) compiles all 12 MOD files (5 from t0067 verbatim + 3 from t0074
verbatim + 4 newly vendored) plus the `cadecay.mod` (already in t0024's library sources, also copied
into `code/mods/` to keep the t0076 build self-contained) into a single `code/mods/x86_64/special`
Linux executable plus the equivalent `nrnmech.dll` (called `libnrnmech.so` on Linux). The MOD
compilation takes ~30 s on a 64-core node.

### Smoke test for CPU-only NEURON

The setup-remote-machine skill at SKILL.md:265 suggests
`python -c "import torch; print(torch.cuda.is_available())"` as a smoke test — wrong for t0076. The
CPU-only adapted smoke test is:

```bash
python -c "from neuron import h; h.load_file('stdrun.hoc'); s = h.Section(); s.insert('hh'); print('OK', s.gnabar_hh)"
```

If this prints `OK 0.12`, NEURON is installed and the built-in HH mechanism resolves. A second smoke
test confirms the local MOD library:

```bash
cd /root/code/mods && python -c "from neuron import h; h.nrn_load_dll('./x86_64/.libs/libnrnmech.so'); s = h.Section(); s.insert('nav16t76'); print('OK')"
```

### Teardown — pulling results back

Per the setup-remote-machine SKILL.md:354-357 protocol:

```bash
scp -r -P <PORT> -i ~/.ssh/id_ed25519 \
  root@<HOST>:/root/data/ tasks/t0076_bedb_dsi_firing_rate_mobo/data/
scp -r -P <PORT> -i ~/.ssh/id_ed25519 \
  root@<HOST>:/root/results/ tasks/t0076_bedb_dsi_firing_rate_mobo/results/
vastai destroy instance <INSTANCE_ID>
```

Expected return payload (per task description Cost estimation): ~50-200 MB of
`data/trial_history.parquet` plus the 3-5 deep-dive `.npz` triples (~5 MB each = ~25 MB) plus the
`results/images/*.png` (~10 MB). Total transfer ≤ 250 MB.

## Lessons Learned

### Cross-process NEURON state — "user defined name already exists" pitfall

Both t0066 (`run_protocol.py:70-88`) and t0072 had to wrap `build_dsgc_cell` in an idempotent loader
because calling NEURON's `nrn_load_dll` twice in one process throws "user defined name already
exists: Exp2NMDA". This affected t0066 because its trial driver builds the cell ONCE and runs 120
trials in the same process. **For t0076 the picture is different**: the BoTorch driver process never
touches NEURON; only the `ProcessPoolExecutor` workers do, and each worker is its own process so
NEURON loads cleanly on first `build_dsgc_cell()` call. The t0066 idempotent wrapper is not needed
inside workers, but it MAY be needed if the driver process itself does a one-shot initial cell build
for parameter validation before launching the BO loop (unlikely but possible — defer the decision to
implementation).

### Single-DLL-per-task vs multi-DLL load — Bed A precedent vs Bed B

t0067 [t0067] showed (`run_sweep.py:107-120`) that NEURON happily loads **two** DLLs as long as no
SUFFIX collides — the t0067 DLL only contains the 5 new SUFFIXes (`nav16t67`, `napt67`, `nart67`,
`kv3t67`, `kv4t67`), none of which collide with t0008's `HHst`/`bipNMDA`/`SACinhib`/ `SACexc`. **For
t0076 the analogous setup is**: t0024's vendored DLL (containing `HHst`, `HHst_noiseless`,
`cadecay`, `Exp2NMDA`) is loaded by `build_dsgc_cell` first; the t0076 local DLL (containing the 12
new `t76`-namespace SUFFIXes plus a copy of `cadecay` — though the copy must NOT collide with the
already-loaded `cad`, so the t0076 build must EXCLUDE `cadecay.mod` and rely on the t0024-loaded
`cad`) is loaded second. This means **t0076 must NOT include `cadecay.mod` in its `code/mods/`
folder** even though t0074 did include it — the difference is that t0074 forks Bed A's HOC and
replaces the t0008 `cad` mechanism, while t0076 uses Bed B unchanged and inherits t0024's `cad`.
**Implication for compile script**: the t0076 MOD pack is exactly 12 files, no `cadecay.mod`.

### `BoTorch` qNEHVI — known not-to-converge symptom and fallback

Per `research_internet.md` and task description Risk #5 (DSI noise too large for the GP) and Risk #6
(exponential placer too restrictive), the standard mitigation is doubling seeds-per- direction from
20 to 40 (Risk #5) or extending the spatial rule with a quadratic term
`ρ(d) = ρ_0 · exp(-d/λ) · (1 + α · d²)` (Risk #6). Neither has prior implementation in this project
but both are linear additions on top of the parametric placer. Plan to monitor the hypervolume
metric every 50 iterations and decide at iter 100 whether to invoke either mitigation.

### Copy-precedent for cross-task non-library code is firmly established

`run_bed_b.py` [t0072] explicitly documents (lines 13-16): "Helpers `_setup_synapses`,
`SynapseBundle`, ... are COPIED verbatim from
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/ run_tuning_curve.py` (lines 52-232) per the project's
cross-task code-reuse rule (these are private helpers in t0024, not entry points of the registered
`de_rosenroll_2026_dsgc` library asset)." The same pattern applies to t0076. The "COPIED verbatim
from t0024 lines X-Y" comment header is the project convention and should be followed.

### Bed B has a 1-trial wall time of ~3 s on the local workstation

The t0066 sweep ran 120 trials in ~360 s (3 s/trial) per `tasks/t0066_*/results/results_summary.md`,
matching the task description's per-trial estimate of ~3 s. Confirms that 160 trials/iteration × 300
iterations = 48,000 trials × 3 s = 40 hours **single-threaded**. Per task description this divides
by 64 cores → ~30 s/iteration → ~2.5-4 h total. Validates the Vast.ai 64-core CPU node choice.

## Recommendations for This Task

1. **Library-import `build_dsgc_cell` from `de_rosenroll_2026_dsgc` (t0024)**. Do NOT re-implement
   cell construction; the registered library entry point is precisely the right interface.

2. **Copy 5 t0067 MODs + 3 t0074 MODs + 4 newly-vendored MODs** into `code/mods/`. SUFFIX rename
   `t67` → `t76` and `t74` → `t76` (per the project's `tNN`-namespace convention). This means only
   **4 truly new MODs** need to be sourced from `research_internet.md`'s recipe: `kdr76.mod` ←
   Mainen ModelDB 2488 `kv.mod`, `iht76.mod` ← Hay 2011 `Ih.mod`, `calt76.mod` ← Hay 2011
   `Ca_HVA.mod`, `catt76.mod` ← Hay 2011 `Ca_LVAst.mod`. Each gets a citation header per the t0067
   convention. **Do NOT include `cadecay.mod`** — t0024's `cad` is already loaded by
   `build_dsgc_cell` and a duplicate would collide.

3. **Copy the t0024 trial-driver helpers into `code/trial_helpers.py`** (the ~180-line block from
   `run_tuning_curve.py:52-232` minus `_setup_synapses` which gets rewritten to use the new
   parametric placer). Add the COPIED-verbatim comment header per t0072 precedent.

4. **Copy the t0066 `CanonicalState`/`_apply_mode_overrides` pattern into
   `code/apply_parameters.py`** (~80 lines) and adapt to write 25-d parameter overrides (12 channel
   densities, 3 passive, 2 calcium, 2 weights) instead of the 3-mode overrides. Synapse counts and
   spatial rule parameters are NOT runtime overrides on an existing bundle — they require rebuilding
   the `SynapseBundle` from scratch via the parametric placer, so handle those separately.

5. **Write the parametric synapse placer (`code/synapse_placer.py`) from scratch** — the only
   genuinely new non-trivial code. Use `h.distance(cell.soma(0.5), sec(0.5))` per the t0050
   precedent for path-distance computation. Sample positions weighted by
   `ρ(d) = ρ_0 · exp(-d/λ) · L_section`. Test before wiring up BoTorch by visualising the placement
   on an x-y scatter at 4 sample (ρ_0, λ) values.

6. **Copy t0067 `_ensure_t67_dll_loaded` into `code/dll_loader.py`** (~14 lines), retarget to the
   t0076 build path. Call inside each `ProcessPoolExecutor` worker after `build_dsgc_cell`.

7. **Copy t0072 `_attach_bed_b_recorders` + `_save_one_type` + `_save_bed_b_direction` into
   `code/recorder.py`** (~125 lines). Use unchanged for the 3-5 best-Pareto deep-dives.

8. **Copy t0072 `render_pdf.py` verbatim** with `paths` import retargeted (64 lines).

9. **Add `botorch>=0.12`, `gpytorch>=1.13`, `torch>=2.4`, `pyarrow>=15.0` to `pyproject.toml`**. The
   CPU-only PyTorch variant (`torch>=2.4+cpu`) is sufficient — qNEHVI does not need GPU.

10. **For the Vast.ai setup, override the GPU defaults in setup-remote-machine SKILL.md**: use
    `num_gpus=0 cpu_cores>=64`, image `python:3.12-bookworm`, and the NEURON smoke test documented
    in the "NEURON Deployment on Vast.ai" subsection. Provision **before** implementing the
    `run_botorch.py` driver — the worker count and the `nrnivmodl` build path on the remote both
    inform the driver's hardcoded defaults.

11. **Validate the MOD pack BEFORE the BoTorch loop**: per `research_internet.md` recommendation 5,
    run a 1-channel current-step test on a single-section toy cell with each of the 4 newly-
    vendored SUFFIXes to confirm `nrnivmodl` compiles and `insert(suffix)` resolves. If any fails,
    fall back per the priority order: drop BK first, then CaT, then CaL (per the t0076 Risk #1
    fallback). The 8-channel reduced set is `(Nav1.6, NaP, NaR, Kdr, Kv3, Kv4, KM, HCN, SK)` if BK
    fails; smaller dimensions only mean a faster GP.

12. **Adopt the t0072 `.npz` format for per-Pareto-cell trace dumps** so the existing `aggregate.py`
    plotting infrastructure can be reused for the diagnostic figures.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Bed A substrate; deposited Poleg-Polsky 2016 DSGC. Listed as a t0076 dependency.
  Bed B reuses Poleg-Polsky's morphology principles, but the actual cell construction in t0076 goes
  through Bed B (`build_dsgc_cell`), not Bed A (`build_dsgc`). Cited for completeness — Bed A is not
  an active substrate for t0076.

### [t0019]

* **Task ID**: `t0019_literature_survey_voltage_gated_channels`
* **Name**: Literature survey: voltage-gated channels in retinal ganglion cells
* **Status**: completed
* **Relevance**: Source for V_half and τ literature priors used in the new MOD vendoring step. Cited
  in `task.json` as a t0076 dependency.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port the de Rosenroll et al. 2026 DSGC into the project
* **Status**: completed
* **Relevance**: Bed B substrate. Provides the registered library `de_rosenroll_2026_dsgc` with
  `build_dsgc_cell` entry point (the only library import t0076 uses), the `cadecay.mod` vendored at
  `assets/library/.../sources/cadecay.mod`, and the trial-driver helpers in
  `run_tuning_curve.py:52-321` that t0076 must copy into its own `code/`.

### [t0050]

* **Task ID**: `t0050_audit_syn_distribution`
* **Name**: Audit synapse-distribution discrepancies between deposited code and paper
* **Status**: completed
* **Relevance**: Provides the canonical `h.distance(soma_seg, target_seg)` two-segment path-distance
  pattern at `extract_coordinates.py:172-202`, including the explicit assertion that
  `h.distance(soma(0.5), soma(0.5)) ≈ 0`. Reused by the t0076 parametric synapse placer.

### [t0066]

* **Task ID**: `t0066_t0024_epsp_ipsp_vm_protocol`
* **Name**: EPSP/IPSP/Vm protocol on the de Rosenroll DSGC
* **Status**: completed
* **Relevance**: Listed as a t0076 dependency. Provides the `CanonicalState` snapshot/restore
  pattern at `run_protocol.py:117-194` plus the `_ensure_neuron_loaded` idempotent NEURON loader at
  lines 70-88 that t0076 copies into its parameter-override module.

### [t0067]

* **Task ID**: `t0067_t0065_soma_channel_addition_sweep`
* **Name**: Soma channel addition sweep
* **Status**: completed
* **Relevance**: Listed as a t0076 dependency. Provides 5 vendored MOD files (Nav1.6, NaP, NaR, Kv3,
  Kv4 with SUFFIXes `nav16t67`/`napt67`/`nart67`/`kv3t67`/`kv4t67`) at `code/mods/`, the
  citation-header convention, and the `_ensure_t67_dll_loaded` idempotent DLL-loader pattern at
  `run_sweep.py:107-120`.

### [t0070]

* **Task ID**: `t0070_writeup_two_model_beds`
* **Name**: Writeup of two standard DSGC model beds in HH-equation research-paper format
* **Status**: completed
* **Relevance**: Listed as a t0076 dependency. Provides the canonical writeup template for both
  beds; t0076's results PDF should follow the same Bed A vs Bed B presentation pattern.

### [t0072]

* **Task ID**: `t0072_synaptic_traces_pd_nd`
* **Name**: Plot synaptic conductances and currents for PD and ND on both model beds
* **Status**: completed
* **Relevance**: Listed as a t0076 dependency. Provides the `_attach_bed_b_recorders` per- synapse
  `g`/`v_local` recorder at `run_bed_b.py:214-248`, the `BedBRecorders` dataclass and `.npz`
  serialisation helpers at `run_bed_b.py:298-327` (~125 lines total), and the `render_pdf.py` Typst
  pipeline (64 lines, copied verbatim).

### [t0074]

* **Task ID**: `t0074_channel_tuning_width_bed_a`
* **Name**: Channel tuning-width sweep on Bed A with BK/SK/Kv7 vendoring
* **Status**: completed
* **Relevance**: NOT in t0076's `task.json` dependency list, but a major non-obvious finding: the
  BK, SK, and Kv7 (= KM) MODs that `research_internet.md` recommends sourcing from Hay 2011 / Mainen
  1996 are ALREADY vendored here as `bk74.mod`, `sk74.mod`, `kv7t74.mod` with the exact same ModelDB
  provenance. Copying these (with SUFFIX rename `t74` → `t76`) collapses t0076's vendoring step from
  7 new MODs to 4 new MODs.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Registered library `tuning_curve_loss`. Considered for the t0076 metric computation
  but rejected — t0076 reports DSI + spike rate directly per (DSI, rate) Pareto point, not the t0012
  envelope-fit weighted scalar loss. Library landscape entry only.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: completed
* **Relevance**: Registered library `tuning_curve_viz`. Operates on tuning-curve CSVs
  (matplotlib-based polar/Cartesian plots). Considered for the Pareto-front deep-dive plots but
  rejected — t0076's deep-dive figures are 8-direction tuning curves per representative cell, which
  the library can produce, but the new `plot_pareto.py` already needs to plot the Pareto front
  itself (not a tuning curve), so adding `tuning_curve_viz` for the deep-dive panels would be an
  additional dependency for marginal benefit. Library landscape entry only.
