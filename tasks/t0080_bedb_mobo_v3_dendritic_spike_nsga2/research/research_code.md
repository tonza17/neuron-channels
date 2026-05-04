---
spec_version: "1"
task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
research_stage: "code"
tasks_reviewed: 16
tasks_cited: 11
libraries_found: 15
libraries_relevant: 4
date_completed: "2026-05-04"
status: "complete"
---
# Research Code: Reusable Code Inventory for Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

## Task Objective

Extend the t0078 AIS-augmented Bed B substrate with dendritic-spike machinery (Mg-block NMDA at all
dendritic compartments plus Nav1.6 + NaP at distal-dendrite densities) and replace BoTorch qLogNEHVI
with NSGA-II via pymoo. Enforce hard biological lower bounds on `nav16_ais` (Kole 2008 0.25 S/cm^2)
and AIS-to-soma Nav ratio (Werginz 2024 ratio >= 5) so the optimiser cannot collapse to the
AIS-disabled corner observed at t0078 iter 81. The pass criterion is at least one Pareto cell with
**DSI >= 0.4 AND PD rate >= 10 Hz**, anchored to RivlinEtzion 2012 stable-cell joint distribution
and Trenholm 2013 peak-rate convention. Produce one library asset
`de_rosenroll_2026_dsgc_ais_dendritic_spike` and one answer asset documenting the
AIS-disabled-corner failure mode and the now-enforced biological-prior checklist.

## Library Landscape

The library aggregator (`aggregate_libraries.py`) is **not implemented** in
`arf/scripts/aggregators/`; only `aggregate_categories`, `aggregate_costs`, `aggregate_machines`,
`aggregate_metric_results`, `aggregate_metrics`, `aggregate_suggestions`, `aggregate_task_types`,
and `aggregate_tasks` exist. Per the t0076 / t0078 precedent, libraries were enumerated by direct
filesystem scan of `tasks/*/assets/library/*/details.json`, which returns **15** registered
libraries: `modeldb_189347_dsgc` [t0008], `tuning_curve_viz` [t0011], `tuning_curve_loss` [t0012],
`modeldb_189347_dsgc_gabamod` (t0020), `modeldb_189347_dsgc_dendritic` (t0022),
`de_rosenroll_2026_dsgc` [t0024], `modeldb_189347_dsgc_exact` (t0046), `minimal_dsgc_scalar_gaba`
(t0052), `minimal_dsgc_spatial_gaba` (t0053), `minimal_dsgc_ampa_nmda_scalar_gaba` (t0054),
`minimal_dsgc_mg_block_nmda` [t0055], `minimal_dsgc_tonic_gaba_sweep` (t0057),
`minimal_dsgc_bar_locked_gaba_ampa_sweep` (t0059), `dsgc_active_channel_pack` (t0074),
`de_rosenroll_2026_dsgc_ais` [t0078].

Four libraries are directly relevant to t0080:

* **`de_rosenroll_2026_dsgc_ais` v0.1.0** [t0078] -- the AIS-augmented Bed B substrate that t0080
  extends. Modules: `code/build_cell_ais.py`, `code/extend_with_ais.py`, `code/apply_params.py`,
  `code/constants.py`, `code/paths.py`, `code/bootstrap.py`, `code/parametric_placer.py`,
  `code/trial_helpers.py`, `code/trial_driver.py`, `code/recorder.py`, plus 13 vendored MODs
  (`nav16t78`, `napt78`, `nart78`, `kdrt78`, `kv3t78`, `kv4t78`, `kv7t78`, `iht78`, `calt78`,
  `catt78`, `bkt78`, `skt78`, `skahpt78`). Entry points: `build_dsgc_cell_with_ais`,
  `DSGCCellWithAIS`, `apply_parameter_vector`, `extend_with_ais`, `ParameterVector`. Import:
  `from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.build_cell_ais import build_dsgc_cell_with_ais`.
  The 49-d `ParameterVector` is the canonical interface; t0080 must extend (not replace) it.

* **`de_rosenroll_2026_dsgc` v0.1.0** [t0024] -- transitive dependency via t0078. Provides
  `build_dsgc_cell()` and the vendored DLL/`.so` carrying `HHst`, `cadecay`, and **`Exp2NMDA`** (the
  canonical Bed-B Jahr-Stevens NMDA point process; Voff/Vset trick, n=0.213 /mM, gama=0.074 /mV, e=0
  mV at
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod`).

* **`minimal_dsgc_mg_block_nmda` v0.1.0** [t0055] -- minimal NMDA-only library exposing
  `NMDA_MgBlock` POINT_PROCESS at
  `tasks/t0055_nmda_mg_block_dsi_recovery/code/mod/NMDA_MgBlock.mod`, with parameters n=0.25 /mM,
  gama=0.08 /mV, tau1=5 ms, tau2=80 ms (Jahr-Stevens). t0080 will reuse the **t0024 `Exp2NMDA`**
  rather than introducing a different SUFFIX, but the t0055 parameter values and the AMPA+NMDA
  co-located triplet pattern (`build_ei_pairs`, `schedule_ei_onsets`) are useful references.

* **`dsgc_active_channel_pack` v0.1.0** [t0074] -- forerunner of t0078's t78 MOD pack. Confirmed
  irrelevant for direct reuse because t0078's t78 pack already supersedes it.

The other 10 libraries are not relevant: Bed A substrates ([t0008], [t0046]), generic visualization
/ scoring helpers ([t0011], [t0012]), or progressively-deprecated minimal-cell testbeds (t0020,
t0022, t0052, t0053, t0054, t0057, t0059) that do not carry the Bed B morphology or the de Rosenroll
release machinery.

## Architecture Overview

t0080 inherits the t0078 substrate verbatim and adds three things on top:

1. **A v3 ParameterVector** that extends t0078's 49-d `ParameterVector` with ~5-7 new dendritic-
   spike parameters and a redefined `nav16_ais` lower bound. Total dimensionality 54-56 d.
2. **Dendritic NMDA placement** at all dendritic compartments (proximal, mid, terminal) using the
   t0024 `Exp2NMDA` POINT_PROCESS plus three new MOBO parameters `gnmda_dend`, `mg_conc` (= `n` in
   /mM), and optionally `voff_nmda`. The placement is colocated with the existing ACh
   bipolar-derived synapse bundle so the AR(2)-noise driven release schedule already used by t0078
   doubles as the NMDA arrival schedule.
3. **NSGA-II via pymoo** as the optimiser, replacing the entire `mobo_loop.py` BoTorch+GP path. The
   trial driver (`evaluate_parameter_vector`) is reused unchanged; only the loop above it is
   replaced.

The t0078 module dependency graph is: `bootstrap.py` -> `paths.py` -> `constants.py` ->
`extend_with_ais.py` -> `build_cell_ais.py` -> `parametric_placer.py` -> `apply_params.py` ->
`trial_helpers.py` -> `trial_driver.py` -> `mobo_loop.py`. t0080 must copy and lightly modify
`constants.py`, `apply_params.py`, `trial_helpers.py`, and `build_cell_ais.py`; can copy
`extend_with_ais.py` verbatim; reimplements `mobo_loop.py` from scratch as `nsga2_loop.py`; and
copies `paths.py`, `bootstrap.py`, `parametric_placer.py`, `recorder.py`, `trial_driver.py`,
`plot_pareto.py`, `render_pdf.py` with SUFFIX/import path renames only.

## Key Findings

### The 49-d ParameterVector layout is the load-bearing data structure

The `ParameterVector` dataclass [t0078] at
`tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/constants.py:290-426` is a frozen slotted dataclass
wrapping a `(49,) NDArray[np.float64]`. The ParamIndex IntEnum (lines 138-193) lays out the 49
slots: 25 tier-stratified densities (5 channels x 5 tiers, channel-major order), 7 uniform-density
channels, 2 slow-AHP params (SK_E2 gbar + tau_ca_multiplier), 13 synaptic / passive parameters
identical to t0076, and 2 free AIS geometry parameters (AIS_LENGTH_UM index 47, AIS_DIAMETER_UM
index 48). `LOWER_BOUNDS` and `UPPER_BOUNDS` are `(49,)` numpy arrays; `LOG_PARAM_INDICES` is the
tuple of 30 indices the optimiser samples in log10 space. **t0080 must add new ParamIndex entries
strictly at the end of the enum** (indices 49+) to preserve the t0078 backward-compat invariant that
`tau_ca_multiplier=1.0` reproduces t0074 sk74 dynamics. Likely new indices: `GNMDA_DEND` (49,
log-uniform 1e-5 .. 1e-2 uS), `MG_CONC_MM` (50, linear 0.5 .. 2.0), `VOFF_NMDA` (51, optional binary
0/1 -- may drop), `NAV16_DEND_DISTAL` (52, log-uniform 1e-5 .. 0.05 S/cm^2), `NAP_DEND_DISTAL` (53,
log-uniform 1e-5 .. 0.01 S/cm^2). Plus **redefining** `LOWER_BOUNDS[ParamIndex.NAV16_AIS_GBAR=4]`
from 1e-5 to 0.25 (Kole hard floor). The AIS-to-soma Nav ratio constraint must be enforced in the
loop either by (a) reparameterising `nav16_soma` as `nav16_ais / ratio` or (b) passing pymoo a
`Constraint` (NSGA-II supports this via `n_ieq_constr`).

### The trial driver is loop-agnostic and reusable verbatim

`evaluate_parameter_vector` [t0078] at `code/trial_driver.py:327-389` takes a `ParameterVector`, an
angles tuple, n_seeds, and max_workers; returns
`EvalResult(dsi, pd_rate_hz, n_trials, n_errors, elapsed_s, is_unstable, peak_vm_mv)`. Internally it
spawns a `ProcessPoolExecutor` and dispatches `_worker_run_trial` (line 252-276). This pickleable
top-level worker is the NEURON-fresh-subprocess fix that bypasses the `Exp2NMDA name already exists`
error. **The pymoo NSGA-II `ElementwiseProblem._evaluate` can call `evaluate_parameter_vector`
directly** without modification (the additional pymoo `multiprocessing.Pool` +
`StarmapParallelization` would just nest the existing pool; better to call the trial driver's
existing pool from inside a non-elementwise pymoo `Problem._evaluate(X, out)` that loops over the
population). t0080 must rebuild the ParameterVector with the wider 54-56 d shape and update bounds;
otherwise the driver works as-is.

### apply_parameter_vector imposes a strict 7-step write order

`apply_parameter_vector` [t0078] at `code/apply_params.py:159-215` executes seven steps in order:
(1) update AIS geometry BEFORE channel insertion (so d_lambda nseg sees the right L), (2) ensure t78
DLL loaded, (3) insert all 12 channels + skahpt78 idempotently on soma+dendrites and the
AIS-permitted subset on AIS, (4) write passive Ra/cm/gleak + 7 uniform channels on soma+dendrites,
(5) write tier-stratified densities per tier (soma, primary, mid, terminal), (6) write AIS-tier
densities for the AIS-permitted SUFFIXes (Nav1.6, Kv3, Kv7), (7) write slow-AHP gbar +
tau_ca_multiplier on soma + AIS only. **t0080 must insert two new write steps**: (4b) write
`gbar_nav16t78` and `gbar_napt78` at the distal-dendrite tier with the new `nav16_dend_distal` and
`nap_dend_distal` values, and (4c) instantiate Exp2NMDA point processes co-located with the existing
ACh bipolar synapses with weight `gnmda_dend` and update the `n` RANGE variable from `mg_conc`.
Distal-dendrite identification: t0078 already exposes `cell.terminal_dends` (177 sections) as
Tier.TERMINAL.

### The Exp2NMDA mechanism is already vendored via t0024

`Exp2NMDA.mod` [t0024] at
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod`
is the Jahr-Stevens-style POINT_PROCESS used by the published Bed B substrate. Its compiled SUFFIX
is loaded by the t0024 vendored DLL/`.so` that t0078's bootstrap loads first. **t0080 must NOT
duplicate this MOD file in the t80 pack** because the t78 pack itself avoids the duplicate SUFFIX
issue this way. Parameters: `tau1=50 ms` (deactivation), `tau2=2 ms` (activation), `e=0 mV`,
`n=0.213 /mM` (Mg block voltage dependence; this is the Mg2+ concentration multiplier),
`gama=0.074 /mV`, `Voff=0`, `Vset=-60`. The voltage dependence formula
`g = gmax / (1 + n * exp(-gama * v))` is mathematically identical to the canonical Jahr-Stevens form
once `n` is reinterpreted as `[Mg]/IC50_at_0mV`. The t0080 plan exposes `n` (renamed to `mg_conc` in
the parameter vector for clarity) as a free MOBO parameter in [0.1, 0.5] /mM, which spans the
published 1.0-1.5 mM physiological range divided by Jahr-Stevens IC50 ~ 4.1 mM.

### Synapse placement uses parametric_placer with cell.all_dends

`setup_synapses_parametric` [t0078] at `code/trial_helpers.py:202-285` calls `place_synapses` from
`parametric_placer.py` with `candidate_sections=cell.all_dends`. `cell.all_dends` excludes the AIS
subsegments (the AIS lives in `cell.ais_proximal` / `cell.ais_distal`), so synapses are
automatically excluded from the AIS without any special-casing. **t0080's Exp2NMDA placements must
use the same candidate set** -- one Exp2NMDA per ACh placement, sharing the same NetStim
+ NetCon driver to mimic the bipolar-NMDA pairing pattern from t0055's `build_ei_pairs` [t0055]. The
  `SynapseBundle` dataclass (line 138-153) currently has `syns_ach`, `syns_gaba`, `ncs_ach`,
  `ncs_gaba`, `netstims`, `syn_xy_ach`, `syn_xy_gaba`. t0080's expanded bundle should add
  `syns_nmda` and `ncs_nmda` (one per ACh synapse).

### The substrate-regression cell exists in t0076's pareto_front.json

Iter-424 best-joint cell from t0076 [t0076]'s
`tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` lines 70-99 records
`dsi=0.4244604316546763`, `pd_rate_hz=4.95`, and the 25-d natural-units parameter vector. The 12
channel densities are: nav16=2.60e-4, nap=6.51e-3, nar=2.44e-3, kdr=1.42e-4, kv3=6.12e-4,
kv4=1.63e-4, kv7=2.21e-2, ih=8.17e-2, cal=3.82e-4, cat=1.24e-2, bk=7.12e-5, sk=4.54e-3 S/cm^2;
passive Ra=248.68, cm=1.557, gleak=7.81e-4; cad depth=0.0542 um, taur=61.21; n_ach=348, n_gaba=132;
rho0_ach=3.77, lambda_ach=488.3, rho0_gaba=3.84, lambda_gaba=126.4; w_ach=4.45e-3, w_gaba=3.46e-4.
**The pre-launch substrate regression must map this 25-d vector into the v3 54-56-d
ParameterVector** by replicating each uniform density across all 5 tiers (so all tiers get the same
density), setting `nav16_ais` to the Kole prior centre 0.375 S/cm^2, AIS geometry to midpoint
(length 30 um, diameter 0.8 um), `tau_ca_multiplier=1.0`, all new dendritic-spike parameters at 0
(no NMDA, no distal Nav, no distal NaP), and running `evaluate_parameter_vector` once. Pass
criterion: reproduce DSI within +/- 0.05 of 0.42 at PD ~ 8.34 Hz.

The published t0076 result for iter-424 lists `pd_rate_hz=4.95` in pareto_front.json but the task
description and the t0078 task_description both report `PD 8.34 Hz` for the same cell. The
discrepancy is because pareto_front.json was emitted with `TSTOP_MS=1000` (t0076 default), but t0078
/ t0080 use `TSTOP_MS=1400`. The substrate-regression check should report the v3 1400-ms peak rate
alongside the t0076 1000-ms peak rate so the comparison is unambiguous.

### t0078 documents the canonical NEURON re-init bug fix

t0078's `plot_pareto.py` [t0078] uses `ProcessPoolExecutor(max_workers=1)` to wrap each deep-dive
`_save_deep_dive` call in a fresh subprocess, bypassing the `Exp2NMDA name already exists` error
that occurs when NEURON re-initialises within the same Python process. The trial driver does the
same via `ProcessPoolExecutor` per cell evaluation. **t0080 carries this pattern unchanged** --
pymoo's `Problem._evaluate` can call `evaluate_parameter_vector(max_workers=cpu_count()-1)`, and
pymoo itself does not need parallelization (the trial driver already provides cell-level
parallelism). The pymoo `StarmapParallelization` recipe documented in `research_internet.md` is not
needed and would double-nest pools.

### t0069 AIS extension is a Bed-A reference, NOT directly reusable

`extend_with_ais` [t0069] at `tasks/t0069_t0067_ais_localised_channel_sweep/code/extend_with_ais.py`
builds a single 30-um AIS section + 1-mm passive axon cable, uses HHst with hard-coded densities (no
parametric MOBO bounds). The t0078 `extend_with_ais.py` [t0078] is a more advanced two-subsegment
fork; t0080 should use **t0078's two-subsegment AIS verbatim**, not t0069's single-segment one. The
t0069 reference is documented in t0078's research_code.md as the biological-prior source for
AIS_LENGTH_UM / AIS_DIAMETER_UM defaults but does not contribute import-eligible code beyond the
t0078 fork.

### Channel SUFFIX renaming pattern: t78 -> t80

t0078 renamed the t76 SUFFIXes to t78 to namespace the new `tau_ca_multiplier`-extended SK_E2
(`skahpt78`) and to allow co-loading the t78 DLL after the t0024 DLL without SUFFIX collisions
(`cadecay` from t0024 is excluded from the t78 pack). **t0080 must rename t78 -> t80 in its copies**
to allow the v3 substrate to be imported alongside t0078 in the same session if needed (which the
substrate-regression check might do). The 13 vendored t78 MODs must each be copied with simple
`git mv ...t78.mod ...t80.mod` followed by SUFFIX rename inside each file. No new MOD file is needed
for NMDA (Exp2NMDA from t0024) or for distal Nav1.6 / NaP (already in the t78/t80 pack -- only the
placement / density at the distal-dendrite tier is new).

### t0078 cost-of-progress and BO scaling lesson

t0078 [t0078] hit O(N^3) Cholesky scaling in BoTorch SingleTaskGP: per-cell wall-clock grew from 28
s in early phase to 9-12 min after acq 480 (491 cells, 78,560 simulations, 24.86 wall hours,
**$3.93** on a Vast.ai 64-core EPYC 7B13 instance). This drove the t0080 decision to switch
optimiser families. NSGA-II per-generation cost is independent of N (only depends on pop_size, fixed
at 96 here), so 3,840 evaluations at ~~50 s/cell = 53.3 CPU-hours / 0.83 wall-hours / **~~$1-1.50**
(target) / **$2.00** (hard cap). The NSGA-II loop is independent of the trial driver, so the cost
saving comes from the algorithmic choice, not from infra changes.

## Reusable Code and Assets

For each item below, **copy into task** means the file must be physically copied into
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/` (with SUFFIX / import-path renames as noted);
**import via library** means the upstream task's library asset is referenced via absolute import
path.

### Substrate construction

* **Source**: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:251-296` --
  `build_dsgc_cell()` returns
  `DSGCCell(h, rgc, soma, all_dends, primary_dends, non_terminal_dends, terminal_dends, terminal_locs_xy, origin_xy)`.
  **Reuse method**: **import via library** (`de_rosenroll_2026_dsgc` registered library); via
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell`. Adaptation:
  none.

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/build_cell_ais.py` (~77 LOC) --
  `build_dsgc_cell_with_ais(*, ais_length_um, ais_diameter_um) -> DSGCCellWithAIS`. **Reuse
  method**: **import via library** (`de_rosenroll_2026_dsgc_ais` registered library) via
  `from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.build_cell_ais import build_dsgc_cell_with_ais`.
  Adaptation: none required for t0080 (the new dendritic-spike parameters are written by the t0080
  `apply_parameter_vector` after this call).

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/extend_with_ais.py` (~127 LOC) --
  `extend_with_ais()`, `update_ais_geometry()`, `AISExtension` dataclass, `_compute_nseg()`. **Reuse
  method**: **import via library** (`de_rosenroll_2026_dsgc_ais`). Adaptation: none.

### Vendored MOD files

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/mods/` (13 files: nav16t78, napt78,
  nart78, kdrt78, kv3t78, kv4t78, kv7t78, iht78, calt78, catt78, bkt78, skt78, skahpt78). **Reuse
  method**: **copy into task** (rename to t80 SUFFIXes; `s/t78/t80/g` in the SUFFIX line and
  filename). Total: 13 files, ~50-150 LOC each; the SUFFIX rename is the only change. **NEW NMDA
  MOD: not needed** -- use the t0024 `Exp2NMDA` POINT_PROCESS (already loaded by the t0024 DLL). The
  t0080 `apply_params.py` instantiates `h.Exp2NMDA(seg)` and writes per-process RANGE variables `n`
  (= `mg_conc`), `gama`, `Voff`, `Vset`, `tau1`, `tau2`. **NEW Nav1.6 / NaP MODs: not needed** --
  the t78/t80 pack's `nav16t80` (formerly `nav16t78`, source paper Khaliq 2003 / Carter & Bean 2009)
  and `napt80` (formerly `napt78`, source paper Magistretti & Alonso 1999) suffice for
  distal-dendrite insertion at the tier-stratified `Tier.TERMINAL` and a new `Tier.MID_DISTAL` (or
  simply repurposing `Tier.TERMINAL`) without any kinetic-scheme changes.

### Constants and parameter vector

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/constants.py` (~471 LOC, ParamIndex
  IntEnum, ParameterVector dataclass, _build_bounds(), LOG_PARAM_INDICES, CHANNEL_SUFFIXES,
  STRATIFIED_CHANNEL_SUFFIXES, AIS_PERMITTED_SUFFIXES, simulation defaults, BO defaults). **Reuse
  method**: **copy into task**, EXTEND. Adaptation: (a) add 5 new ParamIndex entries (GNMDA_DEND,
  MG_CONC_MM, NAV16_DEND_DISTAL, NAP_DEND_DISTAL, optionally VOFF_NMDA), (b) bump N_PARAMS to 54 (or
  55 if Voff is kept), (c) extend LOWER_BOUNDS / UPPER_BOUNDS arrays in `_build_bounds()`, (d)
  extend LOG_PARAM_INDICES, (e) replace `LOWER_BOUNDS[NAV16_AIS_GBAR=4] = 1e-5` with `0.25` (Kole
  hard floor), (f) add new ParameterVector @property accessors for the 5 new fields, (g) replace
  BoTorch defaults (N_SOBOL_INITIAL etc.) with NSGA-II defaults (POP_SIZE=96, N_GENERATIONS=40,
  SBX_ETA=15, PM_ETA=20). New LOC: ~80-100.

### Apply parameter vector

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/apply_params.py` (~215 LOC,
  `apply_parameter_vector`, `_insert_channels_once`, `_write_passive_and_uniform`,
  `_write_stratified`, `_write_slow_ahp`, `_write_ais_stratified`, `ensure_t78_dll_loaded`). **Reuse
  method**: **copy into task**, EXTEND. Adaptation: (a) rename `ensure_t78_dll_loaded` ->
  `ensure_t80_dll_loaded` and update `resolve_t78_mod_library` -> `resolve_t80_mod_library`, (b) add
  new `_write_dendritic_distal_nav` step that writes `gbar_nav16t80` and `gbar_napt80` only on the
  distal-dendrite (terminal) sections at the new densities, (c) add a new `_write_dendritic_nmda`
  step that updates Exp2NMDA RANGE parameters (`n`, `gama`, `Voff`, `Vset`) on the NMDA point
  processes in the bundle (the Exp2NMDA instances are owned by the SynapseBundle, so this step must
  be called after `setup_synapses_parametric` -- consider moving the NMDA-write to
  `setup_synapses_parametric` itself). New LOC: ~30-40.

### Synapse placement and trial helpers

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/parametric_placer.py` (~105 LOC,
  `place_synapses` with exponential-decay weighting, `PlacedSynapse` dataclass). **Reuse method**:
  **copy into task** verbatim; no adaptation (only import-path renames if any). LOC: ~105.

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/trial_helpers.py` (~285 LOC,
  `setup_synapses_parametric`, `_bar_arrival_times`, `_rates_with_ar2_noise`,
  `_gaba_prob_for_direction`, `_rates_to_events`, `_count_spikes`, `BASE_ACH_PROB`, `RATE_DT_MS`,
  `BAR_SIGMA_MS`, `CELL_PREF_DEG`, `PREF_GABA_PROB`, `NULL_GABA_PROB`, `SynapseBundle`,
  `_section_midpoint_xy`, `_instantiate_synapse`). **Reuse method**: **copy into task**, EXTEND.
  Adaptation: (a) extend `SynapseBundle` with `syns_nmda: list[Any]` and `ncs_nmda: list[Any]`
  fields, (b) extend `setup_synapses_parametric` to instantiate one `h.Exp2NMDA` per ACh placement
  co-located on the same section/position, with a NetCon from the SAME NetStim that already drives
  the ACh Exp2Syn (mirrors t0055 `build_ei_pairs` triplet pattern), (c) write `syn.tau1`,
  `syn.tau2`, `syn.e`, `syn.n`, `syn.gama`, `syn.Voff`, `syn.Vset` on the new Exp2NMDA instances.
  New LOC: ~30-40.

### Trial driver

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/trial_driver.py` (~422 LOC,
  `evaluate_parameter_vector`, `run_one_trial`, `_worker_run_trial`, `_worker_prepare`,
  `_summarise_trials`, `TrialResult`, `EvalResult`). **Reuse method**: **copy into task** verbatim
  with import-path renames. Adaptation: none for the loop logic; only the import paths need to point
  at the t0080 modules. The pickleable top-level `_worker_run_trial` works as-is for the wider
  ParameterVector because it pickles the `(N_PARAMS,)` ndarray, not the dataclass shape. LOC: ~422.

### Bootstrap and paths

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/bootstrap.py` (~116 LOC, Linux
  `compile_t0024_mods_linux`, monkey-patches t0024 `_ensure_neuron_on_path` and `load_neuron`).
  **Reuse method**: **copy into task** verbatim. LOC: ~116.

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/paths.py` (~76 LOC, MOD library
  resolver, output directories). **Reuse method**: **copy into task** with SUFFIX renames
  (`resolve_t78_mod_library` -> `resolve_t80_mod_library`). LOC: ~76.

### NSGA-II loop (NEW)

* **Source**: NONE (BoTorch loop in `mobo_loop.py` not reused; t0080 writes a fresh
  `nsga2_loop.py`). The pymoo `ElementwiseProblem` + `NSGA2(pop_size=96, sampling=LHS())`
  + `minimize(problem, algorithm, ('n_gen', 40), seed=...)` recipe documented in
    `research_internet.md` is the implementation template. The new module needs: (a)
    `BedBV3Problem(Problem)` with `n_var=54-56`, `n_obj=2`, `n_ieq_constr=1` (AIS-to-soma Nav ratio
    constraint), `xl/xu` from `LOWER_BOUNDS/UPPER_BOUNDS` with log-space transforms, (b)
    `_evaluate(X, out)` calling `evaluate_parameter_vector` for each row, with
    `out["F"] = [-dsi, -pd_rate_hz]` (negate for minimization) and
    `out["G"] = [5.0 - ais_to_soma_ratio]` (>= 0 means feasible), (c) hypervolume tracking via
    `pymoo.indicators.hv.HV` ref point [0, 0] with sign-flip to maximisation, (d) per-generation
    checkpoint pickle of the pymoo `Algorithm` state, (e) cost gating identical to t0078
    mobo_loop.py lines 222-238 (BUDGET_OVERRUN_MD). Estimated LOC: 250-300.

### Plotting and PDF rendering

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/plot_pareto.py` (~408 LOC). **Reuse
  method**: **copy into task** verbatim with import-path renames. The deep-dive selection logic
  (highest-DSI, highest-rate, knee point) and `ProcessPoolExecutor` subprocess wrapping for NEURON
  re-init both transfer unchanged.

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/recorder.py` (~122 LOC,
  `attach_recorders`, `save_recorders_npz`). **Reuse method**: **copy into task** verbatim.

* **Source**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/render_pdf.py`. **Reuse method**: **copy
  into task** verbatim with import-path renames.

### Dataset for substrate-regression check

* **Source**: `tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` iter 424 entry
  (pareto_front.json lines 70-99). **Reuse method**: read at task setup time; encode the 25-d vector
  into a Python literal in t0080's substrate-regression module. The expected substrate-regression
  target is `dsi=0.42`, `pd_rate_hz=8.34` (per t0078 task description, which used the t0078 1400 ms
  protocol). Total reused: 25 floats.

## Lessons Learned

* **t0078 substrate works as-is on Vast.ai EPYC 7B13 64-core**. The t0078 24.86-h / $3.93 run
  [t0078] proved the trial driver's `ProcessPoolExecutor` + `cpu_count()-1` pattern is stable for
  > 78,000 NEURON simulations. t0080 reuses this exactly; expected wall-clock at 3,840 evaluations
  > is ~0.83 hours / $0.13-0.20 raw + setup overhead = $1.00-$1.50 [t0078].
* **BoTorch SingleTaskGP is the wrong tool for >40-d problems**. t0078 [t0078] saw per-cell
  wall-clock grow from 28 s to 9-12 min as Cholesky size scaled O(N^3); the loop was forced-stopped
  at acq 416 / 700. **t0080 NSGA-II eliminates this scaling** because each generation's cost is
  fixed by population size (96), not by accumulated history.
* **MOBO can collapse biologically-priored parameters to floor when the prior is soft**. t0078 iter
  81 [t0078] pushed `nav16_ais` to 1e-5 S/cm^2 (five orders below Kole 2008's 0.25-0.5 prior, six
  orders below Werginz 2024's 1.3 measurement) producing a Pareto cell with DSI=0.316 / PD=9.68 Hz
  that misses the joint pass criterion. The fix is to encode the prior as a **hard parameter
  bound**, not a regularising term in the objective. NSGA-II's bound handling guarantees no
  individual ever has `nav16_ais < 0.25 S/cm^2`.
* **Substrate regression checks catch silent regressions in shared substrates**. t0076 -> t0078
  changed TSTOP_MS from 1000 to 1400 [t0076, t0078]; the iter-424 cell's pareto_front.json
  `pd_rate_hz=4.95` was at TSTOP=1000 but t0078's task description reports the same cell at PD=8.34
  Hz under TSTOP=1400. t0080 must report **both** values in the substrate-regression block.
* **NEURON SUFFIX collisions and namespacing**. The t0078 `cadecay`-from-t0024 +
  `skahpt78`-from-t0078 collision-avoidance pattern [t0078] (load t0024 DLL first, t78 DLL second;
  do NOT include `cadecay` in the t78 pack) is the canonical recipe for multi-task MOD libraries.
  t0080 follows the same pattern (load t0024 first, t80 second; no SUFFIX duplication; Exp2NMDA
  stays in t0024 DLL only).
* **The `Exp2NMDA name already exists` re-init bug is silent and intermittent**. t0078 documented
  [t0078] that NEURON's POINT_PROCESS class registry is global and not cleared on `h.finitialize()`,
  so any subprocess that loads the t0024 DLL twice (e.g., via two distinct `build_dsgc_cell` calls
  in the same Python interpreter) raises `Exp2NMDA name already exists`. The fix is
  `ProcessPoolExecutor(max_workers=N)` with one fresh worker per trial-cell. t0080 keeps this
  pattern; pymoo nesting must NOT introduce additional `multiprocessing.Pool` layers.
* **Bed B's published model has NMDA only on ON dendrites**. ModelDB 189347 [t0008, t0046] places
  NMDARs only on ON-layer bipolar contacts (177 of them) per the Poleg-Polsky 2016 paper's diagram.
  t0080's plan to extend NMDA to all dendritic compartments (proximal + mid + terminal, ON and OFF)
  is a **deliberate extension** beyond the published model; the substrate-regression cell at t0076
  iter-424 parameters with `gnmda_dend=0` will be the proxy validation.

## Recommendations for This Task

1. **Reuse the t0078 trial driver verbatim**. `evaluate_parameter_vector` is loop-agnostic and
   already supports the t0080 worker / subprocess pattern. Do NOT modify `_worker_run_trial`; only
   rebuild the ParameterVector with the wider 54-56 d shape.

2. **Extend, don't replace, the t0078 ParameterVector**. Add 5 new ParamIndex entries at indices
   49-53 (after AIS_DIAMETER_UM), bump N_PARAMS to 54, replace `LOWER_BOUNDS[NAV16_AIS_GBAR=4]` from
   1e-5 to 0.25 (Kole), enforce AIS-to-soma Nav ratio >= 5 as a pymoo `n_ieq_constr` constraint
   (`G = 5.0 - nav16_ais / nav16_soma`). Keep the t0078 backward-compat invariant that
   `tau_ca_multiplier=1.0` reproduces sk74 dynamics by NOT reordering the existing 49 indices.

3. **Reuse Exp2NMDA from t0024**. Do not vendor a new NMDA MOD file. Instantiate `h.Exp2NMDA(seg)`
   co-located with each ACh Exp2Syn placement, share the NetStim, set the new RANGE parameters from
   the ParameterVector. Three new MOBO parameters: `gnmda_dend` (NetCon weight in uS, log-uniform
   1e-5 .. 1e-2), `mg_conc_mm` (linear 0.1 .. 0.5, written to Exp2NMDA's `n` field), and optionally
   `voff_nmda` (binary 0/1; researcher decision pending). Use `tau1=50 ms`, `tau2=2 ms`,
   `gama=0.074 /mV`, `e=0 mV` per the t0024 Exp2NMDA defaults.

4. **Reuse Nav1.6 (`nav16t80`) and NaP (`napt80`) from the t78/t80 pack at distal- dendrite tier**.
   No new MOD file needed. Bound `nav16_dend_distal` at [1e-5, 0.05] S/cm^2 (Schachter 2010 / Sivyer
   2013 prior) and `nap_dend_distal` at [1e-5, 0.01] S/cm^2 (Hay 2011 somatic NaP upper bound).
   Initial LHS sample biased toward 0.02-0.04 / 0.001-0.005 respectively.

5. **Extend `apply_parameter_vector` with two new write steps** (4b: distal Nav1.6 + NaP at
   `cell.terminal_dends`; 4c: Exp2NMDA RANGE updates on the bundle's NMDA point processes).
   Estimated +30-40 LOC. The new SynapseBundle must hold `syns_nmda` and `ncs_nmda` lists.

6. **Write a fresh `nsga2_loop.py`** (~250-300 LOC) using the
   `pymoo.algorithms.moo.nsga2.NSGA2(pop_size=96, sampling=LHS())` recipe documented in
   `research_internet.md`. Use `pymoo.core.problem.Problem` (NOT `ElementwiseProblem`) so the
   population batch can be dispatched in one call to the trial driver's ProcessPoolExecutor. Pin
   `pymoo>=0.6.1.6` in `pyproject.toml`. Reference point [0, 0] (negation-flipped to match t0076 /
   t0078 maximisation HV convention). Per-generation checkpoints. Cost gating identical to t0078
   with HARD_BUDGET_USD=2.00.

7. **Pre-launch substrate-regression check at t0076 iter-424 vector**. Hardcode the 25-d vector from
   `tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` lines 70-99 into a Python
   literal; map it to the v3 54-56-d ParameterVector by replicating each density across all 5 tiers,
   setting `nav16_ais` to the Kole prior centre 0.375 S/cm^2, AIS geometry to midpoint,
   `tau_ca_multiplier=1`, all new dendritic-spike parameters at 0. Run `evaluate_parameter_vector`
   once; document DSI / PD-rate delta in `results/results_summary.md`.

8. **Copy and rename the 13 t78 MODs to t80**. Use `git mv` followed by SUFFIX rename inside each
   .mod file. Verify on Linux via `nrnivmodl mods/` builds the t80 shared object cleanly; verify on
   Windows via `nrnivmodl.bat`. Note: NaP at distal dendrites must be enabled in the
   `apply_parameter_vector` write steps; the existing NaP_AIS ParamIndex slot stays at 0 conductance
   (NaP forbidden at AIS).

9. **Do NOT register a new library asset for the NSGA-II harness**. Per the task description's "Out
   of scope" section, the NSGA-II machinery promotion to a substrate-agnostic library is deferred
   until at least one more substrate uses it. The t0080 library asset is the v3 substrate (cell +
   apply_params + MODs); the `nsga2_loop.py` is task-private.

10. **Carry the cost-gate, intervention-file pattern from t0078 verbatim**. Copy
    `_write_budget_overrun` and the SOFT/HARD budget USD constants (set to $1.50 / $2.00 per task
    description) into the t0080 NSGA-II loop. The intervention file path should be
    `tasks/t0080_*/intervention/budget_overrun.md`.

## Common Patterns

* **Path centralisation**: every task has `code/paths.py` with `pathlib.Path` constants; no string
  concatenation or `os.path.join` calls anywhere in the t0078 code [t0078]. t0080 copies this
  pattern.
* **Bootstrap as side-effect of import**: `tasks/t0078_*/code/bootstrap.py` runs
  `bootstrap_neuron()` at module import time so any module that does
  `from tasks.t0078_*.code import bootstrap as _bootstrap` gets the Linux monkey-patches applied
  automatically [t0078]. t0080 copies this pattern.
* **`@dataclass(frozen=True, slots=True)` for all structured data**: ParameterVector, TrialResult,
  EvalResult, PlacedSynapse, SynapseBundle, AISExtension, DeepDivePick all use frozen+slots [t0078].
  Two t0078 dataclasses use `slots=True` only without `frozen` because they hold NEURON section
  handles (`AISExtension`, `DSGCCellWithAIS`, `SynapseBundle`); t0080 should follow the same
  convention.
* **Worker-process global state caches**: `_WORKER_CELL`, `_WORKER_BUNDLE`, `_WORKER_PARAMS_HASH`
  are module-level Optional dataclasses set on first call inside each worker [t0078]. This lets the
  cell + bundle be built once per worker and reused across the 8 directions x 20 seeds = 160 trials
  per cell evaluation. t0080 inherits this verbatim.
* **AR(2) correlated noise from t0024**: `generate_ar2_batch` [t0024] is the canonical noise
  generator; t0078 [t0078] imports it directly. t0080 follows the same import.
* **Citation-anchored hard bounds**: t0078 [t0078] task_description explicitly cites Kole 2008 /
  Werginz 2024 / Hay 2011 in the bound docstrings. t0080 plan specifies five citation-anchored hard
  bounds (`nav16_ais >= 0.25` Kole, AIS-to-soma ratio >= 5 Werginz, `nav16_dend_distal <= 0.05`
  Schachter / Sivyer, `nap_dend_distal <= 0.01` Hay, `mg_conc` in [0.1, 0.5] /mM Jahr-Stevens) --
  this becomes the answer-asset checklist.

## Estimated Total New LOC

* Constants extension: +80-100 LOC (5 new ParamIndex entries, bounds, properties, NSGA-II defaults).
* Apply params extension: +30-40 LOC (two new write steps).
* Trial helpers extension: +30-40 LOC (NMDA bundle fields, Exp2NMDA instantiation).
* NSGA-II loop (fresh): 250-300 LOC.
* Substrate-regression module (new): ~80-120 LOC (parameter mapping + single-call driver +
  results_summary delta block).
* SUFFIX renames in 13 MOD files: trivial (~13 LOC churn).
* Library asset details + description: ~250 LOC of markdown.
* **Total NEW Python LOC**: ~470-600.
* **Total COPIED+RENAMED Python LOC**: ~1500 (constants, apply_params, trial_helpers, trial_driver,
  parametric_placer, paths, bootstrap, build_cell_ais, extend_with_ais, plot_pareto, recorder,
  render_pdf).

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 (Poleg-Polsky 2016 DSGC) into the project
* **Status**: completed
* **Relevance**: Bed-A substrate with NMDARs on ON-dendrite-only bipolar contacts. Reference for the
  NMDA-only-on-ON-dendrites convention that t0080 deliberately extends to ON+OFF dendrites.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response visualisation library
* **Status**: completed
* **Relevance**: Provides `tuning_curve_viz` library with Cartesian + polar plotters; not used
  directly by t0080's NSGA-II loop but available for downstream Pareto-cell tuning curve
  visualisations.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning curve scoring loss library
* **Status**: completed
* **Relevance**: `tuning_curve_loss` library exposes `compute_dsi`, `compute_peak_hz`,
  `compute_null_hz`. Not strictly needed by t0080 (the trial driver computes DSI inline) but useful
  for cross-task metric consistency in the answer asset.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC into the project
* **Status**: completed
* **Relevance**: Direct dependency. Provides `build_dsgc_cell()`, the morphology HOC template, and
  the Bed-B vendored DLL with `HHst`, `cadecay`, **`Exp2NMDA`** SUFFIXes. t0080's dendritic NMDA
  insertion uses the t0024 `Exp2NMDA` POINT_PROCESS unchanged.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Reproduce Poleg-Polsky 2016 exactly
* **Status**: completed
* **Relevance**: `bipolarNMDA.mod` from this task's library is the upstream Mg-block source cited by
  t0055's `NMDA_MgBlock.mod` and the t0024 `Exp2NMDA.mod` (which has the same Voff/Vset trick).
  Reference for confirming that the t0024 Exp2NMDA is mathematically equivalent to the canonical
  Bed-B Mg-block.

### [t0055]

* **Task ID**: `t0055_nmda_mg_block_dsi_recovery`
* **Name**: NMDA Mg-block DSI recovery experiment
* **Status**: completed
* **Relevance**: Reference for the AMPA + NMDA + GABA co-located triplet pattern (`build_ei_pairs`,
  `schedule_ei_onsets`). Confirms the canonical Jahr-Stevens parameters (n=0.25 /mM, gama=0.08 /mV)
  used by t0080's `mg_conc_mm` MOBO bound derivation.

### [t0067]

* **Task ID**: `t0067_t0065_soma_channel_addition_sweep`
* **Name**: Soma channel addition sweep
* **Status**: completed
* **Relevance**: Origin of the `nav16t67` / `napt67` SUFFIX naming convention that t0078
  (`nav16t78`/`napt78`) and t0080 (`nav16t80`/`napt80`) inherit unchanged in kinetics, only renamed
  in SUFFIX.

### [t0069]

* **Task ID**: `t0069_t0067_ais_localised_channel_sweep`
* **Name**: AIS-localised channel sweep
* **Status**: completed
* **Relevance**: First task to attach an AIS to the project's DSGC cells. Bed A reference for AIS
  construction patterns; superseded by t0078's two-subsegment AIS for Bed B. t0080 uses t0078's AIS,
  not t0069's.

### [t0074]

* **Task ID**: `t0074_channel_tuning_width_bed_a`
* **Name**: Channel tuning width on Bed A
* **Status**: completed
* **Relevance**: Origin of the `sk74` SK_E2 MOD file that t0078 extended into `skahpt78` with
  `tau_ca_multiplier`. Reference for confirming the SK_E2 kinetics carried into t0080's `skahpt80`.

### [t0076]

* **Task ID**: `t0076_bedb_dsi_firing_rate_mobo`
* **Name**: Bed B DSI / firing rate MOBO baseline
* **Status**: completed
* **Relevance**: Direct dependency. Provides the 25-d ParameterSpec scaffolding that t0078 extended
  to 49-d and t0080 extends to 54-56-d. Provides the iter-424 best-joint cell parameter values (DSI
  0.42 / PD ~ 8.34 Hz) needed for t0080's substrate-regression pre-launch check at
  `tasks/t0076_bedb_dsi_firing_rate_mobo/results/data/pareto_front.json` lines 70-99.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B v2 MOBO with AIS, tier-stratified channels, slow Kv-AHP
* **Status**: completed
* **Relevance**: Direct dependency. Provides the AIS-augmented Bed B substrate library
  (`de_rosenroll_2026_dsgc_ais`) that t0080 extends. The 49-d ParameterVector,
  `apply_parameter_vector` write order, two-subsegment AIS builder, NEURON re-init subprocess
  pattern, ProcessPoolExecutor trial driver, and 13 vendored t78 MODs all carry into t0080. The
  t0078 iter-81 AIS-disabled-corner failure is the canonical case study for the t0080 answer asset.
