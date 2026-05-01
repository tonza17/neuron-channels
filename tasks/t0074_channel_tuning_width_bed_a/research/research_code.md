---
spec_version: "1"
task_id: "t0074_channel_tuning_width_bed_a"
research_stage: "code"
tasks_reviewed: 14
tasks_cited: 11
libraries_found: 13
libraries_relevant: 4
date_completed: "2026-05-01"
status: "complete"
---
# Research Code: Channel Tuning-Width Sweep on Bed A with BK / SK / Kv7

## Task Objective

Vendor three new MOD mechanisms (BK / KCa1.1, SK / KCa2, Kv7 / M-current) plus a `cad`-style
single-shell calcium-pool mechanism, attach them to Bed A (deposited Poleg-Polsky DSGC, library
`modeldb_189347_dsgc` from [t0008]), un-zero the dormant CaL and CaT channels in Bed A's HOC
`init_active` so the calcium pool has a current source, then re-run a regression gate against the
[t0067] reference baseline DSI = 0.797 (5-seed mean, FULL mode). Once the gate passes, run a
12-angle bar-rotation tuning-curve sweep across 25 conditions (1 baseline + 8 channels x 3
densities), 5 seeds per condition for FULL mode (1500 trials) plus 1 seed per condition for two
passive-diagnostic modes (600 trials, EPSP_PASSIVE / IPSP_PASSIVE), and compute HWHM, vector-sum
DSI, peak rate, and RMSE-vs-cosine-target per condition using the t0011 / t0012 libraries. This
research review surveys the project's vendored libraries, the existing channel-insertion sweep, the
existing 12-angle bar-rotation driver on Bed A, the existing `cad`-style calcium-pool MOD on Bed B,
and the EPSP_PASSIVE / IPSP_PASSIVE / FULL mode-toggle protocol so the implementation stage can fork
the right code and import the right libraries.

## Library Landscape

The project's `tasks/*/assets/library/*/details.json` registry contains 13 libraries (no
project-wide library aggregator exists yet, so they were enumerated by globbing
`tasks/*/assets/library/*/details.json` against the worktree). Four are directly relevant.

* **`modeldb_189347_dsgc`** ([t0008],
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/details.json`): the deposited
  Poleg-Polsky DSGC port (Bed A). Provides `build_dsgc()` and `run_one_trial()` Python entry points
  plus the verbatim NEURON HOC sources in `assets/library/modeldb_189347_dsgc/sources/` (HHst.mod,
  dsgc_model.hoc, RGCmodel.hoc, etc.). This is the substrate for the entire t0074 sweep. Import
  path:
  `from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc, apply_params, read_synapse_coords`.
  Relevant — direct dependency of t0074.

* **`tuning_curve_viz`** ([t0011],
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/details.json`):
  matplotlib library for Cartesian / polar / multi-model overlay / raster+PSTH PNGs. Entry points:
  `plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`, `plot_multi_model_overlay`,
  `plot_angle_raster_psth`. Import path:
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_cartesian_tuning_curve, plot_polar_tuning_curve, plot_multi_model_overlay`.
  Reads the canonical `(angle_deg, trial_seed, firing_rate_hz)` CSV schema. Relevant — direct
  dependency of t0074 for the per-channel sensitivity plots and the cross-channel comparison plot.

* **`tuning_curve_loss`** ([t0012],
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/details.json`):
  canonical 12-angle scorer that returns `ScoreReport` with DSI / peak / null / HWHM /
  RMSE-vs-target / reliability + envelope pass/fail. Entry points:
  `score(simulated_curve_csv, target_curve_csv)`, `score_curves(target, candidate)`, `compute_dsi`,
  `compute_hwhm_deg`, `compute_peak_hz`, `compute_null_hz`. Import path:
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import score, score_curves, ScoreReport`
  and
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import compute_hwhm_deg, compute_dsi`.
  Default target is `t0004` curve_mean.csv resolved internally via `TARGET_MEAN_CSV`. Relevant —
  direct dependency of t0074 for HWHM and RMSE-vs-cosine-target.

* **`de_rosenroll_2026_dsgc`** ([t0024],
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/details.json`): Bed
  B port. Its `sources/cadecay.mod` is the canonical `cad`-style single-shell calcium-pool mechanism
  that t0074 will copy as a reference template into the new vendored MOD pack (relevant template
  only — t0074 will not import this library directly). Located at
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`.

The remaining nine libraries are not directly relevant: `modeldb_189347_dsgc_gabamod` ([t0020]) is a
gabaMOD-swap variant of Bed A used by the EPSP/IPSP protocol but its mechanism set is identical to
t0008's; `modeldb_189347_dsgc_dendritic` (t0022) and `modeldb_189347_dsgc_exact` ([t0046]) are
alternate Bed-A variants; `minimal_dsgc_*` libraries (t0052, t0053, t0054, t0055, t0057, t0059) are
minimal-cell tonic-GABA / NMDA explorations and use a different mechanism set. None of them ship BK
/ SK / Kv7 MOD files; that gap is addressed by t0074's Stage-1 vendoring step.

No library-aggregator script exists in `arf/scripts/aggregators/` yet (only `aggregate_tasks.py`,
`aggregate_metrics.py`, `aggregate_costs.py`, and a few others); the library survey above was
performed via direct filesystem enumeration with the same effective result because no
library-correction overlay exists in `corrections/`.

## Key Findings

### Bed A's HOC `init_active` Zeroes CaL / CaT and the Calcium Pool Has No Current Source

The deposited Poleg-Polsky DSGC's `init_active` proc lives in the HOC source bundled inside the
[t0008] library asset:
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc:114-152`.
Lines 144-145 read `RGCcaT=0*active` and `RGCcaL=0.0*active`; the `*active` factor is set elsewhere
in `init_active` (line 134) via `active=1-doingVC`, which means CaT and CaL are also zeroed in
voltage-clamp mode. These two HOC variables are then bound to the `glbar_HHst` and `gtbar_HHst`
mechanism parameters inside `proc update()` at
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc:288-289`
(`forsec RGC.all { glbar_HHst=RGCcaL; gtbar_HHst=RGCcaT; ... }`). The `HHst.mod` mechanism at
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/HHst.mod` carries the L-
and T-type calcium currents internally (lines 26 `USEION ca READ eca WRITE ica`, 31-32
`RANGE lm, lh, gl, glbar` / `RANGE tm, th, gt, gtbar`, 219 `ica = il+it`); `glbar` and `gtbar`
default to `0.0003 S/cm2` (lines 57-58) but are overwritten to zero by `init_active` at every trial.
Consequently the existing model has no calcium current at all and adding a `cad`-style calcium pool
by itself would produce a flat `cai = cainf` trace, defeating the BK / SK biophysics. The
single-line edit needed is to replace the two zero literals at lines 144-145 with non-zero defaults;
values around the HHst defaults (`0.0003`) are biologically reasonable as a starting point per
[t0019]'s VGC literature survey. Because the HOC source is bundled inside an immutable library
asset, t0074 must **fork** the HOC into its task-local code/ folder rather than edit the [t0008]
library in place — this is the mechanism by which the un-zeroing becomes task-isolated and
reversible.

### t0067 Provides a Forkable Channel-Insertion Pipeline

[t0067] is the closest precedent and the explicit fork target for t0074. Its sweep driver is
`tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py:1-327` and the channel-pack MODs
live in `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/` (nav16t67.mod, napt67.mod,
nart67.mod, kv3t67.mod, kv4t67.mod plus `mod_func.c` registration). The density-application function
`_set_active_channel(*, soma, key)` at
`tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py:131-148` zeroes all five channel
densities, then sets the active one (in S/cm^2 = mS/cm^2 * 1e-3); it relies on
`_insert_all_channels_with_zero_gbar(*, h, soma)` at lines 123-128 inserting every mechanism once at
build time. The mechanism `SUFFIX` and density grid live in the typed
`CHANNEL_DEFS: tuple[ChannelDef, ...]` registry in
`tasks/t0067_t0065_soma_channel_addition_sweep/code/constants.py:30-63` (3-fold density steps per
channel; e.g. Nav1.6 low/med/high = 10/30/90 mS/cm^2, Kv3 = 7/20/60 mS/cm^2). Each MOD uses
`NONSPECIFIC_CURRENT i` (e.g.
`tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/nav16t67.mod:8`) to avoid `USEION`
collisions with HHst's `USEION na/k/ca`. The DLL is loaded via `_ensure_t67_dll_loaded` at
`run_sweep.py:107-120` after `build_dsgc()`; NEURON allows multiple `nrn_load_dll` calls so long as
no SUFFIX collides. All five t67 MODs are NONSPECIFIC, so the new `cad` calcium-pool MOD t0074
vendors will need a `USEION ca READ ica WRITE cai` declaration that does NOT collide with HHst
(which writes `ica` but does not write `cai`); HHst writes ica and `cad` reads ica + writes cai;
this is exactly the pattern Bed B uses (see Findings below).

### t0067's FULL-Mode Protocol Uses a 2-Direction gabaMOD Swap

[t0067] is **not** a 12-angle bar-rotation; it is a 2-direction gabaMOD swap inherited from [t0065].
The trial schedule at `tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py:72-104`
enumerates `Direction.PD` and `Direction.ND` only. The PD/ND swap is implemented at
`run_sweep.py:162-163` via `h.gabaMOD = GABA_MOD_PD (0.33)` for PD and `GABA_MOD_ND (0.99)` for ND,
using the constants in `tasks/t0067_t0065_soma_channel_addition_sweep/code/constants.py:65-66`. The
`exptype` field is set at `run_sweep.py:164` (`h.exptype = 1` for FULL mode, HH on); FULL is the
only mode this task covers. The 5-seed protocol (5 per direction per condition, base seed
1. lives at `tasks/t0067_t0065_soma_channel_addition_sweep/code/constants.py:67-68`
   (`N_SEEDS_PER_CONDITION: int = 5; SEED_BASE: int = 1`). Trial length is 1000 ms
   (`TSTOP_MS: float = 1000.0` at line 69) and `AP_THRESHOLD_MV: float = -10.0` (line 71) is the
   spike threshold. The order of operations in `_run_one_trial(*, h, baseline_coords, key)` at
   `run_sweep.py:158-205` is critical:
   `apply_params -> set h.gabaMOD -> set h.exptype = 1 -> h("init_active()") -> h("access RGC.soma") -> h("update()") -> h("placeBIP()") -> _set_active_channel`.
   The comment at `run_sweep.py:171-172` warns that `init_active` rebinds `RGCsomana` onto
   `gnabar_HHst` so the new-channel gbars must be set AFTER `init_active`. The recorded baseline DSI
   is **0.7974683544303798** in
   `tasks/t0067_t0065_soma_channel_addition_sweep/results/metrics.json`.

### Bed A Already Has a 12-Angle Bar-Rotation Driver in [t0008]

Despite t0067 using only PD / ND, Bed A **does** have a working 12-angle protocol — it lives in
the upstream [t0008] task itself and is the canonical entry path for the project's tuning- curve
loss library. The driver is `tasks/t0008_port_modeldb_189347/code/run_tuning_curve.py:1-100` and the
angle iteration is the inner loop at
`tasks/t0008_port_modeldb_189347/code/run_tuning_curve.py:56-65`:
`for angle_idx in range(N_ANGLES): angle_deg = angle_idx * ANGLE_STEP_DEG; for trial_idx in range(N_TRIALS): rate = run_one_trial(h=h, angle_deg=angle_deg, seed=seed, ...)`.
Constants in `tasks/t0008_port_modeldb_189347/code/constants.py:49-51` define `N_ANGLES: int = 12`,
`N_TRIALS: int = 20`, `ANGLE_STEP_DEG: float = 30.0` — exactly the 12-angle 30-degree-step
schedule t0074 needs. The angle is encoded by **rotating BIP synapse coordinates** around the soma
rather than by rotating the bar — see `tasks/t0008_port_modeldb_189347/code/build_cell.py:211-262`
(`rotate_synapse_coords_in_place`). The function takes a baseline snapshot (captured once via
`read_synapse_coords` at lines 192-208) and applies a 2-D rotation matrix per BIP synapse, keeping
the SAC inhib / SAC exc coords pinned (the comment at lines 219-238 explains this preserves the
bipolar-SAC arrival-time asymmetry that produces direction selectivity). Trial output is a single
firing rate (Hz) computed by counting upward threshold crossings of soma Vm above `AP_THRESHOLD_MV`
at lines 348-358 of `build_cell.py`. **t0074 should fork this driver and replace the inner FULL-only
loop with the t0067 channel-density / mode-toggle structure while keeping the [t0008] angle-rotation
idiom.** Conclusion for the task description's "12-angle bar-rotation protocol per t0046
reproduction" reference: t0046 itself uses 2-direction (`Direction.PREFERRED / Direction.NULL`)
protocol via `simplerun()` at
`tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:1-100`; the actual 12-angle
driver is t0008's `run_tuning_curve.py`.

### t0024's `cadecay.mod` Is the Canonical `cad`-Style Calcium Pool

The Destexhe 1995 single-shell first-order calcium pool already exists in the [t0024] Bed B library
at
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`.
The MOD declares `SUFFIX cad` (line 25), `USEION ca READ ica, cai WRITE cai` (line 26), and
`RANGE depth, kt, kd, cainf, taur` (line 27); it implements the standard
`drive_channel = -10000 * ica / (2 * FARADAY * depth)` calcium-influx-from-current at line 70 plus
`cai' = drive_channel + (cainf - cai) / taur` first-order decay at line 74; defaults are
`depth=0.1 um`, `taur=5 ms`, `cainf=2e-4 mM` (lines 44-46). t0024 inserts this pool on the soma and
every dendrite via `soma.insert("cad")` and per-dendrite `dend.insert("cad")` calls at
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:194, 219, 230, 241`. **This is the exact
MOD that t0074 should copy** — verbatim file copy into t0074's task-local `code/mods/cadecay.mod`
— since it already follows the project's `USEION ca` convention and will compose cleanly with the
deposited HHst's `WRITE ica` declaration in
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/HHst.mod:26`. No
mechanism-name collision because HHst does not write `cai`.

### EPSP_PASSIVE / IPSP_PASSIVE / FULL Mode Toggling Lives in [t0065]

The Stage-4 passive-diagnostic protocol the t0074 task description asks for is exactly the [t0065]
three-mode protocol. The mode enum and exptype constants are in
`tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/constants.py:8-32`:
`TrialMode { FULL, EPSP_PASSIVE, IPSP_PASSIVE }`, `EXPTYPE_HH_ON = 1`, `EXPTYPE_HH_OFF = 2`,
`GABA_MOD_PD = 0.33`, `GABA_MOD_ND = 0.99`, `GABA_MOD_OFF = 0.0`, plus per-mode synaptic-conductance
overrides (`B_AMPA_OFF_NS = 0.0`, `B_NMDA_OFF_NS = 0.0`, `S_GABA_OFF_NS = 0.0`,
`S_ACH_OFF_NS = 0.0`, `ACH_MOD_OFF = 0.0`). The mode-toggle function is
`_apply_mode_override(*, h, mode)` at
`tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py:144-167`; FULL is a no-op,
EPSP_PASSIVE silences GABA via `gabaMOD = 0` and `s2ggaba = 0`, IPSP_PASSIVE silences both bipolar
(`b2gampa = 0`, `b2gnmda = 0`) and SAC cholinergic (`s2gach = 0`, `achMOD = 0`) pathways. The trial
executor at `run_protocol.py:171-219` runs
`apply_params -> set h.gabaMOD -> set h.exptype -> _apply_mode_override -> init_active -> update -> placeBIP -> finitialize -> continuerun`.
The `BASELINE_END_MS: float = 100.0` window in `constants.py:68` is the t < 100 ms baseline-Vm
window. **t0074 should copy this `_apply_mode_override` function verbatim into its run_sweep.py and
gate it behind a per-trial `TrialMode` field**, applying it between `set h.exptype` and
`init_active`. See related project memory note (`feedback_dsgc_measurement_protocol`) which records
that the standard mode trio is EPSP_PASSIVE / IPSP_PASSIVE / FULL with HH-off-for-traces and
HH-on-for-firing-rate, fixed 1400 ms trial length; the [t0065] implementation uses
`TSTOP_MS = 1000.0` per the deposited model so t0074 should follow t0065 unless the
measurement-protocol note requires extending to 1400 ms.

### t0011 / t0012 Loaders Expect Canonical CSV Schema `(angle_deg, trial_seed, firing_rate_hz)`

The t0011 viz library re-exports t0012's loader at
`tasks/t0011_response_visualization_library/code/tuning_curve_viz/loaders.py:17-37` so both
libraries consume the same CSV. The schema-detection function `_detect_schema(*, columns)` at
`tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/loader.py:43-55` accepts three
column-set variants: `canonical_trials = (angle_deg, trial_seed, firing_rate_hz)`,
`t0004_trials = (angle_deg, trial_index, rate_hz)`, and `t0004_mean = (angle_deg, mean_rate_hz)`.
The angle-grid validator at lines 58-69 enforces exactly 12 angles with 30-deg uniform spacing;
`tuning_curve_viz.loaders.validate_angle_grid` is a permissive 8/12/16-angle variant. Per-trial data
is folded into a `(n_angles, n_trials)` matrix for bootstrap CI plotting; the `firing_rates_hz`
field on the `TuningCurve` dataclass at lines 34-40 is the per-angle mean. The HWHM computation at
`tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py:50-100` rotates the
rate vector so the peak sits at index `n // 2` then linearly interpolates the half-max crossing on
each side and averages — for a flat curve it returns `180.0`. **Per the task description's "report
HWHM as null for low-rate conditions" rule, t0074 must guard the call with a peak-rate check (e.g. <
1 Hz) BEFORE calling `compute_hwhm_deg`** since the library itself never returns null. The score
function at
`tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/scoring.py:199-225` defaults
the target to `t0004` `curve_mean.csv` resolved internally, but t0074 should pass the t0004 mean
curve explicitly to make the dependency visible (the t0004 cosine target is `peak = 32 Hz`,
`r_base = 2 Hz`, `θ_pref = 90 deg`, `n = 2`, see t0004 results_summary).

### Vector-Sum DSI and Per-Condition Tuning Curves Are New Computations

Neither t0011, t0012, nor any prior task implements vector-sum DSI
(`|sum_i rate_i * exp(i*theta_i)| / sum_i rate_i`). [t0012] only computes the standard DSI =
`(peak - null) / (peak + null)` at
`tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py:41-47`. **t0074
must implement vector-sum DSI as a new function in its task-local code**; it should live in the same
module as the per-condition aggregator. The Hanson 2019 / Rivlin 2012 vector-sum convention
identified in `research_internet.md` is the canonical mouse-DSGC residual metric.

### Project Memory Note: Drop Per-Synapse Activation Histograms; Use Fixed 1400 ms Trial

The `feedback_dsgc_measurement_protocol` user-memory note records that the standard mode trio is
EPSP_PASSIVE / IPSP_PASSIVE / FULL with HH off for EPSP/IPSP traces and HH on for
Vm/firing-rate/DSI; trial length is fixed at 1400 ms; per-synapse activation histograms should be
dropped. t0074's stage 3 / stage 4 protocols match this except for the trial length ([t0065] /
[t0067] use `TSTOP_MS = 1000.0`). The implementation should default to 1000 ms (to preserve the
[t0067] regression-gate fingerprint) and treat 1400 ms as a follow-up extension. Per-synapse
activation histograms are not in the t0074 outputs anyway.

### Project Memory Note: Consolidated Task Design

The `feedback_consolidated_task_design` user-memory note records the researcher's preference for
combined tasks with biological-plausibility motivation. t0074's bundling of {Nav1.6, NaP, NaR, Kv3,
Kv4, BK, SK, Kv7} sweep + tuning-width metrics + calcium-pool + CaL/CaT un-zeroing matches this
preference and addresses suggestions {S-0068-01, S-0068-02, S-0068-05} in one go.

## Reusable Code and Assets

### From [t0008] Bed A library

* **Source**: `tasks/t0008_port_modeldb_189347/code/build_cell.py:96-176` (`build_dsgc`,
  `load_neuron`, `apply_params`).

* **What it does**: bootstraps NEURON, loads HHst / bipNMDA / SACinhib / SACexc DLL, sources
  RGCmodel.hoc + dsgc_model.hoc, returns initialised `h` with `h.RGC` cell template.

* **Reuse method**: **import via library** (`modeldb_189347_dsgc`).

* **Function signatures**: `build_dsgc() -> Any`, `apply_params(h: Any, *, seed: int) -> None`,
  `read_synapse_coords(h: Any) -> list[SynapseCoords]`.

* **Adaptation needed**: none for the import; but t0074 must override `init_active` after build by
  sourcing a forked HOC (see "copy into task" below) BEFORE the first trial.

* **Line count**: 0 (import).

* **Source**: `tasks/t0008_port_modeldb_189347/code/build_cell.py:211-277`
  (`rotate_synapse_coords_in_place`, `reset_synapse_coords`).

* **What it does**: 12-angle rotation of BIP synapse coordinates around the soma; preserves SAC
  coords pinned to baseline.

* **Reuse method**: **import via library**.

* **Function signatures**:
  `rotate_synapse_coords_in_place(*, h: Any, angle_deg: float, baseline: list[SynapseCoords], rotate_sac: bool = False) -> None`,
  `reset_synapse_coords(*, h: Any, baseline: list[SynapseCoords]) -> None`.

* **Adaptation needed**: none.

* **Line count**: 0 (import).

* **Source**:
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc:114-152`
  (`proc init_active`).

* **What it does**: HOC proc that sets channel-density globals
  `RGCsomana / RGCsomakv / RGCsomakm / RGCdendna / RGCdendkv / RGCdendkm / RGCcaT / RGCcaL / RGCcaP / RGCih / RGCkca / RGCgpas / RGCepas`
  based on `exptype`.

* **Reuse method**: **copy into task** with edits to lines 144-145 to replace `RGCcaT=0*active` and
  `RGCcaL=0.0*active` with non-zero defaults (e.g. `0.0003*active`) and re-source the forked HOC
  after `build_dsgc()`. Alternatively the full HOC file can be task-local with a
  `proc override_init_active()` that t0074 calls each trial before `init_active()` and which sets
  RGCcaT / RGCcaL post-hoc.

* **Adaptation needed**: replace two HOC literals; preserve all other logic.

* **Line count**: ~40 lines for the proc itself; the surrounding HOC file is ~600 lines but only the
  proc body needs forking.

### From [t0067] channel-insertion pipeline

* **Source**: `tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py:107-205`
  (`_ensure_t67_dll_loaded`, `_insert_all_channels_with_zero_gbar`, `_set_active_channel`,
  `_run_one_trial`).

* **What it does**: loads the channel-pack DLL, inserts all mechanisms once with gbar=0, toggles the
  active channel per trial via `setattr(seg, f"gbar_{ch.suffix}", g_s_cm2)`, runs one FULL-mode
  trial.

* **Reuse method**: **copy into task** (NOT a registered library; t0067 has no library asset).

* **Adaptation needed**: extend `CHANNEL_DEFS` registry to add `BK`, `SK`, `KV7` mechanism suffixes;
  rename DLL path to t0074-local; insert `cad` mechanism on the soma at build time alongside the
  BK/SK/Kv7 mechanisms; add `TrialMode` field to `TrialKey` and call `_apply_mode_override` between
  `set h.exptype` and `init_active()`.

* **Line count**: ~100 lines (sweep driver + helper functions).

* **Source**: `tasks/t0067_t0065_soma_channel_addition_sweep/code/constants.py:9-77` (`ChannelKind`,
  `DensityLabel`, `Direction`, `ChannelDef`, `CHANNEL_DEFS`, `GABA_MOD_PD/ND`,
  `N_SEEDS_PER_CONDITION`, `SEED_BASE`, `TSTOP_MS`, `AP_THRESHOLD_MV`).

* **What it does**: typed constants and channel registry.

* **Reuse method**: **copy into task**.

* **Adaptation needed**: add `BK`, `SK`, `KV7` enum values and `ChannelDef` rows; add `TrialMode`
  enum import from t0065's pattern; densities for new channels per `research_internet.md`
  recommendations.

* **Line count**: ~80 lines (constants only).

* **Source**: `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/*.mod` and `mod_func.c`.

* **What it does**: 5 NONSPECIFIC_CURRENT MOD mechanisms (Nav1.6, NaP, NaR, Kv3, Kv4) plus the
  modl_reg registration boilerplate.

* **Reuse method**: **copy into task** (verbatim; t67 MODs are needed in the t0074 channel pack
  alongside the new BK / SK / Kv7).

* **Adaptation needed**: rename SUFFIX from `nav16t67` -> `nav16t74` (or keep t67 names) to avoid
  DLL name collision if both DLLs are loaded; update `mod_func.c` to register the new BK / SK / Kv7
  / cad mechanisms in addition.

* **Line count**: ~50 lines per MOD x 5 = 250 lines plus 30 for mod_func.c.

### From [t0024] Bed B `cad` calcium pool

* **Source**:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod:1-75`.
* **What it does**: Destexhe 1995 single-shell first-order calcium pool, `SUFFIX cad`,
  `USEION ca READ ica, cai WRITE cai`, defaults `depth=0.1 um`, `taur=5 ms`, `cainf=2e-4 mM`.
* **Reuse method**: **copy into task** (despite living inside [t0024]'s library asset, it is not
  exported as a Python entry point; the MOD file itself must be vendored into t0074's channel pack
  alongside BK / SK / Kv7).
* **Adaptation needed**: none for the MOD; just include it in t0074's `code/mods/cadecay.mod` and
  register in `mod_func.c`.
* **Line count**: 75 lines.

### From [t0065] EPSP / IPSP / FULL mode-toggle protocol

* **Source**: `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/constants.py:8-68` (`TrialMode`,
  `EXPTYPE_*`, `GABA_MOD_*`, `B_*OFF_NS`, `S_*OFF_NS`, `ACH_MOD_OFF`, `BASELINE_END_MS`).

* **What it does**: typed mode enum, exptype mapping, per-mode synaptic-conductance overrides.

* **Reuse method**: **copy into task**.

* **Adaptation needed**: merge with the t0067-derived constants module (single `constants.py` for
  t0074).

* **Line count**: ~60 lines.

* **Source**: `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py:144-167`
  (`_apply_mode_override`).

* **What it does**: zeroes the right synaptic conductance globals per `TrialMode`.

* **Reuse method**: **copy into task**.

* **Adaptation needed**: none.

* **Line count**: ~25 lines.

### From [t0011] viz library

* **Source**: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/cartesian.py`,
  `polar.py`, `overlay.py`.
* **What it does**: Cartesian / polar / multi-model overlay tuning-curve plots with optional target
  overlay.
* **Reuse method**: **import via library** (`tuning_curve_viz`).
* **Function signatures**:
  `plot_cartesian_tuning_curve(curve_csv: Path, out_png: Path, *, show_trials: bool = True, target_csv: Path | None = None) -> None`,
  `plot_polar_tuning_curve(curve_csv: Path, out_png: Path, *, target_csv: Path | None = None) -> None`,
  `plot_multi_model_overlay(curve_csvs: list[Path], labels: list[str], out_png: Path, *, target_csv: Path | None = None) -> None`.
* **Adaptation needed**: none for the library; t0074 must emit canonical
  `(angle_deg, trial_seed, firing_rate_hz)` CSVs per condition before calling.
* **Line count**: 0 (import).

### From [t0012] tuning-curve loss library

* **Source**:
  `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/scoring.py:199-225`
  (`score`),
  `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py:32-100`
  (`compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`).
* **What it does**: load, score, and compute DSI / HWHM / RMSE-vs-target on a 12-angle CSV.
* **Reuse method**: **import via library** (`tuning_curve_loss`).
* **Function signatures**:
  `score(simulated_curve_csv: Path, target_curve_csv: Path | None = None, *, weights: dict[str, float] | None = None) -> ScoreReport`,
  `compute_hwhm_deg(*, curve: TuningCurve) -> float`, `compute_dsi(*, curve: TuningCurve) -> float`.
* **Adaptation needed**: per-condition wrapper that gates `compute_hwhm_deg` behind a peak-rate < 1
  Hz check and returns `None` when the curve is sub-threshold.
* **Line count**: 0 (import).

### New code t0074 must write (no prior precedent)

* **Vector-sum DSI**: `vector_sum_dsi(rates_hz: NDArray, angles_rad: NDArray) -> float`, ~10 lines,
  lives in t0074's task-local metrics module.
* **BK / SK / Kv7 MOD files**: 3 new MODs, ~50 lines each, sourced from published hippocampal /
  cortical models per `research_internet.md` (Migliore CA1 BK, Hines/Carnevale Purkinje SK,
  classical Kv7 / M-current).
* **Per-condition tuning-curve aggregator**: pivots a per-trial DataFrame of
  `(condition_id, channel, density_label, angle_deg, seed, firing_rate_hz)` into 25 per-condition
  CSVs in canonical schema; ~60 lines.
* **HOC `init_active` fork**: a task-local copy of dsgc_model.hoc with CaL/CaT un-zeroed, loaded
  after `build_dsgc()` to override the library's HOC; ~600 lines verbatim with two edits.
* **Stage-2 regression gate**: small driver that runs the no-extra-channels baseline, computes
  5-seed mean DSI, asserts `abs(dsi - 0.797) < 1e-3`, and exits non-zero on failure. ~40 lines.

## Lessons Learned

* **[t0008] tuning-curve driver is correct** — `run_tuning_curve.py` produces a canonical-schema
  CSV that scores cleanly against t0004 via t0012; the 12-angle 30-deg-step protocol is the
  project's de facto standard.
* **[t0067] sweep is robust** — 160/160 trials completed with 0 instabilities; the
  `_set_active_channel` zero-then-set pattern reliably swaps the active channel per trial without
  requiring rebuild. Baseline DSI = 0.7975 reproducibly. Use this exact pattern unchanged for t0074.
* **NONSPECIFIC_CURRENT is required** — every t67 MOD declares `NONSPECIFIC_CURRENT i` to avoid
  `USEION` SUFFIX conflicts with HHst's three USEIONs (na/k/ca). The new BK / SK MODs may need to
  USEION ca READ cai (because BK/SK kinetics are calcium-dependent) but they must NOT WRITE ica or
  any HHst-controlled ion. Only the `cad` MOD should WRITE cai. This composition matches Bed B's
  pattern.
* **`init_active` rebinds gbar globals** — calling `h("init_active()")` after a per-trial setup
  will overwrite the just-set gbar values for HHst (`gnabar_HHst`, etc.). t0067 documents this and
  sets `gbar_<new>` AFTER `init_active`. t0074 must follow the same ordering for any new mechanism
  whose density is hand-set.
* **CaL / CaT zeroing was deliberate in the deposited model** — Poleg-Polsky 2016 ran the model
  TTX-on (`exptype=2 / TTX=1`) for some figures and chose to zero L/T to avoid calcium-current
  contamination of the predominantly Na/K spike. Un-zeroing risks shifting the spike threshold and
  AP shape. This is the rationale for the Stage-2 regression gate.
* **Library imports work cleanly** — [t0011] imports [t0012]'s loader at
  `tuning_curve_viz/loaders.py:17-20` without trouble. The t0074 task can rely on both libraries
  being importable simultaneously.
* **DLL load order matters** — t0067's `_ensure_t67_dll_loaded` is called AFTER `build_dsgc()`.
  NEURON allows multiple `nrn_load_dll` calls only when SUFFIXes don't collide; t0074's new DLL must
  use unique SUFFIXes (e.g. `bk74`, `sk74`, `kv7t74`, `cad`) and not reuse t67's `nav16t67`/etc.

## Recommendations for This Task

* **Fork [t0067]'s `run_sweep.py` wholesale** into
  `tasks/t0074_channel_tuning_width_bed_a/code/run_sweep.py` and extend with a `TrialMode` field on
  `TrialKey`, copying [t0065]'s `_apply_mode_override` for the EPSP_PASSIVE / IPSP_PASSIVE branches.
  Keep the FULL branch byte-identical to t0067's.
* **Replace the 2-direction PD/ND iteration with the [t0008] 12-angle rotation**. Concretely the
  trial-enumeration in `_enumerate_trials` should iterate over
  `range(N_ANGLES) * N_TRIALS_PER_CONDITION * N_MODES * N_CHANNELS * N_DENSITIES` per-mode schedule
  (1500 FULL + 600 passive); per trial, set `angle_deg = idx * 30.0` and call [t0008]'s
  `rotate_synapse_coords_in_place` after `apply_params`. Don't use [t0067]'s `gabaMOD_PD/ND` swap;
  let the BIP-rotation idiom encode direction.
* **Copy [t0024]'s `cadecay.mod` verbatim** into
  `tasks/t0074_channel_tuning_width_bed_a/code/mods/cadecay.mod` and add it to the new channel
  pack's `mod_func.c`. Insert `cad` on the soma immediately after the t0067 channel-pack
  `_insert_all_channels_with_zero_gbar` call so it has a current source available when CaL/CaT are
  un-zeroed.
* **Fork the [t0008] `dsgc_model.hoc` proc `init_active` rather than monkey-patch**. Place the fork
  at `tasks/t0074_channel_tuning_width_bed_a/code/dsgc_model_t74.hoc` with lines 144-145 set to
  `RGCcaT=0.0003*active` and `RGCcaL=0.0003*active` (match HHst defaults). After `build_dsgc()`
  returns h, `h.load_file(1, ".../dsgc_model_t74.hoc")` to replace the proc; verify the override by
  reading `h.RGCcaL` after `init_active()`.
* **Use [t0012]'s `score()` per condition** for the RMSE-vs-cosine-target metric, but write a thin
  wrapper that gates `compute_hwhm_deg` behind `peak_hz < 1.0` and returns `None` per the task
  description's null-HWHM rule.
* **Implement vector-sum DSI in a task-local metrics module** since neither [t0011] nor [t0012]
  provides it. The function is one line of math and should not pollute either library.
* **Stage-2 regression gate**: implement as a standalone Python script
  `tasks/t0074_.../code/run_regression_gate.py` that runs the baseline-only condition with 5 seeds
  (`SEED_BASE = 1`, `N_SEEDS_PER_CONDITION = 5`, FULL mode, 12 angles, BIP rotation), aggregates
  spike counts at angle = 0 deg (PD) and angle = 180 deg (ND), computes DSI = (PD - ND) / (PD + ND),
  and asserts `abs(DSI - 0.7974683544303798) < 1e-3`. This is the [t0067] reference. Note the
  [t0067] DSI was computed with the gabaMOD swap, not BIP rotation; the comparison may need to use
  the gabaMOD swap protocol for the gate alone, then switch to BIP rotation for the main sweep.
* **Per-channel sensitivity plots**: use [t0011]'s `plot_cartesian_tuning_curve` per channel with
  the three densities overlaid (call once per channel with multi-curve overlay).
* **Cross-channel comparison plot**: use [t0011]'s `plot_multi_model_overlay` with up to 8 curves;
  the Okabe-Ito palette has 8 colours so 8 channels fit cleanly.
* **Mind the user-memory note**: keep the trial length at the [t0067] standard `TSTOP_MS = 1000.0`
  for the regression gate (so the t0067 fingerprint reproduces); flag the 1400 ms alternative as a
  follow-up if `feedback_dsgc_measurement_protocol` is enforced strictly. Drop any per-synapse
  activation histograms.

## Task Index

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate Canonical Target Tuning Curve
* **Status**: completed
* **Relevance**: Provides the cosine target curve at peak = 32 Hz, peak at 90 deg, used as the RMSE
  reference by t0074. Lives in `assets/dataset/target-tuning-curve/files/` (`curve_mean.csv` and
  `curve_trials.csv`).

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 (Poleg-Polsky DSGC)
* **Status**: completed
* **Relevance**: Bed A library `modeldb_189347_dsgc`; provides `build_dsgc()`, `apply_params`,
  `read_synapse_coords`, `rotate_synapse_coords_in_place`, `run_one_trial`, the canonical 12-angle
  bar-rotation driver in `run_tuning_curve.py`, and the bundled HOC sources where `init_active` and
  the CaL/CaT zeroing live.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response Visualization Library
* **Status**: completed
* **Relevance**: Library `tuning_curve_viz` for Cartesian / polar / overlay tuning-curve plots;
  t0074's per-channel sensitivity and cross-channel comparison plots use this.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning Curve Scoring Loss Library
* **Status**: completed
* **Relevance**: Library `tuning_curve_loss` for DSI / HWHM / RMSE-vs-cosine-target / score metrics
  on the canonical 12-angle CSV; t0074 uses `score`, `compute_dsi`, `compute_hwhm_deg`.

### [t0019]

* **Task ID**: `t0019_literature_survey_voltage_gated_channels`
* **Name**: Literature Survey: Voltage-Gated Channels
* **Status**: completed
* **Relevance**: Source of channel-density priors (already used by [t0067] for the original 5
  channels); BK / SK / Kv7 priors not present, motivating the Stage-1 vendoring step.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 with GABA Modulation
* **Status**: completed
* **Relevance**: Bed A variant providing the gabaMOD swap that [t0065] / [t0067] use as the PD/ND
  encoding; not directly imported by t0074 but documents the protocol fork.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Bed B port whose `cadecay.mod` (Destexhe 1995 single-shell first-order Ca pool) is
  the canonical `cad` mechanism that t0074 will copy verbatim into its channel pack.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Reproduce Poleg-Polsky 2016 Exact
* **Status**: completed
* **Relevance**: Exact reproduction of Bed A; uses the 2-direction `simplerun()` protocol rather
  than the 12-angle bar-rotation. Documents the Direction.PREFERRED / Direction.NULL convention and
  the integer `exptype` argument.

### [t0065]

* **Task ID**: `t0065_t0020_epsp_ipsp_vm_protocol`
* **Name**: EPSP / IPSP / FULL Vm Protocol on Bed A
* **Status**: completed
* **Relevance**: Source of the `TrialMode { FULL, EPSP_PASSIVE, IPSP_PASSIVE }` enum, exptype
  mapping, and `_apply_mode_override` mode-toggle function that t0074 will copy for its Stage-4
  passive-diagnostic protocol.

### [t0067]

* **Task ID**: `t0067_t0065_soma_channel_addition_sweep`
* **Name**: Soma Channel-Addition Sweep on Bed A
* **Status**: completed
* **Relevance**: Direct fork target. Provides the 5-channel pack (Nav1.6, NaP, NaR, Kv3, Kv4) MOD
  files plus the `_set_active_channel` density-toggle pattern, the `_ensure_t67_dll_loaded` DLL-load
  helper, the typed `CHANNEL_DEFS` registry, the `_run_one_trial` FULL-mode trial executor, and the
  reference baseline DSI = 0.7975 for the Stage-2 regression gate.

### [t0072]

* **Task ID**: `t0072_synaptic_traces_pd_nd`
* **Name**: Synaptic Traces PD vs ND on Bed A and Bed B
* **Status**: completed
* **Relevance**: Latest task that imports
  `from tasks.t0008_port_modeldb_189347.code.build_cell import apply_params, build_dsgc`. Confirms
  the Bed A library API is stable and the per-trial seed / coords / rotation pattern works for
  t0074's purposes.
