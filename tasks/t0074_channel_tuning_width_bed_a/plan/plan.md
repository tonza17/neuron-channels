---
spec_version: "2"
task_id: "t0074_channel_tuning_width_bed_a"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: Channel Tuning-Width Sweep on Bed A with BK / SK / Kv7 Vendoring

## Objective

Vendor three new NEURON MOD mechanisms (BK / KCa1.1, SK / KCa2, Kv7 / M-current) plus reuse a
`cad`-style single-shell calcium-pool MOD on Bed A (the deposited Poleg-Polsky DSGC, library
`modeldb_189347_dsgc` from t0008), un-zero the dormant CaL and CaT channels in Bed A's HOC
`init_active` so the new calcium pool has a current source, then run a 12-angle bar-rotation
tuning-curve sweep across **25 conditions** (1 baseline + 8 channels x 3 densities) with **5 seeds
per FULL-mode condition** (1500 trials) plus **2 passive diagnostic modes** (600 trials) for a total
of **2100 trials**. For each condition compute the half-width at half-maximum (HWHM) in degrees,
vector-sum DSI, peak rate (Hz), legacy PD-vs-ND DSI, and RMSE vs the t0004 cosine target curve. Done
looks like: (a) Stage-2 regression gate passes (baseline DSI within 1e-3 of t0067's
0.7974683544303798 under the gabaMOD-swap protocol on the un-zeroed-CaL/CaT + zero-density-BK/SK/Kv7
substrate); (b) all 2100 trials complete with no instability flags; (c) the width-metrics table is
fully populated for all 25 conditions (HWHM may be `null` for sub-1-Hz tuning curves, but vector-sum
DSI and peak rate are defined for every condition); (d) per-channel sensitivity plots and one
cross-channel overlay plot exist; (e) one `library` asset is registered.

## Task Requirement Checklist

The operative task text from `tasks/t0074_channel_tuning_width_bed_a/task_description.md`:

> Substrate: Bed A only (deposited Poleg-Polsky DSGC, t0008 library `modeldb_189347_dsgc`).
> Encoding: 12-angle bar-rotation protocol... Channel set: 8 channels — 5 already vendored
> {Nav1.6, NaP, NaR, Kv3, Kv4} plus 3 newly vendored {BK, SK, Kv7}. Each channel inserted on the
> soma at low / medium / high density. Plus a baseline condition with no extra channels. Conditions:
> 1 baseline + 8 channels x 3 densities = 25 conditions. Trials: 25 conditions x 12 angles x 5 seeds
> in FULL mode = 1500 trials. Plus 25 x 12 angles x 1 seed x 2 passive modes (EPSP_PASSIVE /
> IPSP_PASSIVE) = 600 diagnostic trials. Total: 2100 trials.
>
> Stage 1 — vendor 3 new MOD files plus calcium-pool mechanism. Stage 2 — regression gate
> (baseline DSI within 1e-3 of t0067 = 0.797). Stage 3 — 12-angle tuning-curve sweep. Stage 4 —
> passive diagnostics. Stage 5 — width metrics and visualisation.
>
> Pass Criteria: Stage 2 regression gate passes; all 2100 trials complete with no instability flags;
> width metrics table fully populated; for each channel, at least one density produces a measurable
> change in either HWHM or vector-sum DSI (delta > 5 deg HWHM or delta > 0.05 vector-sum DSI
> relative to baseline).
>
> Expected Outputs: Library asset (vendored channel pack); per-condition tuning curves (25 CSVs) and
> combined `tuning_curves.csv`; width metrics table (`results/metrics_summary.csv`); per-channel
> sensitivity plots (8 PNGs); cross-channel comparison plot; `results/metrics.json`.

Concrete requirements extracted from this text:

* **REQ-1**: Vendor a BK (KCa1.1) MOD file from a published model (Mainen-Sejnowski 1996, ModelDB
  2488 `kca.mod` per `research_internet.md`). Steps: 4. Evidence: `code/mods/bk74.mod` exists with
  documented source DOI in `details.json`.

* **REQ-2**: Vendor an SK (KCa2) MOD file from a published model (Hay 2011, ModelDB 139653
  `SK_E2.mod`). Steps: 4. Evidence: `code/mods/sk74.mod` exists with documented source DOI in
  `details.json`.

* **REQ-3**: Vendor a Kv7 / M-current MOD file from a published model (Hay 2011, ModelDB 139653
  `Im.mod`). Steps: 4. Evidence: `code/mods/kv7t74.mod` exists with documented source DOI in
  `details.json`.

* **REQ-4**: Vendor (reuse) a single-shell `cad`-style calcium-pool MOD. Per `research_code.md`,
  copy `cadecay.mod` verbatim from the t0024 Bed B library
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`).
  Steps: 4. Evidence: `code/mods/cadecay.mod` exists with documented source DOI in `details.json`.

* **REQ-5**: Un-zero CaL and CaT in Bed A's `init_active` HOC proc. The original is at
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc` lines
  144-145 (`RGCcaT=0*active`, `RGCcaL=0.0*active`). Bed A's HOC is bundled inside the t0008
  immutable library asset, so this task **forks** the HOC into `code/dsgc_model_t74.hoc` rather than
  editing in place. Steps: 5. Evidence: forked HOC file exists with the two literals replaced by
  `0.0003*active` (matches HHst defaults), and `h.RGCcaL > 0` after `init_active()` is verified at
  runtime.

* **REQ-6**: Stage-2 regression gate. Run the t0067 baseline protocol (FULL mode, 5 seeds, 16
  conditions x 2 directions = 160 trials, gabaMOD-swap with `GABA_MOD_PD = 0.33`,
  `GABA_MOD_ND = 0.99`) on the un-zeroed-CaL/CaT + zero-density-BK/SK/Kv7 substrate, and assert
  `abs(baseline_dsi - 0.7974683544303798) < 1e-3`. Steps: 6. Evidence:
  `results/regression_gate.json` reports `passed: true` and the measured DSI value.

* **REQ-7**: Stage-3 sweep — 25 conditions x 12 angles x 5 seeds = 1500 FULL-mode trials, using
  Bed A's native 12-angle bar-rotation protocol (`N_ANGLES = 12`, `ANGLE_STEP_DEG = 30.0`,
  synapse-coordinate rotation around the soma). Steps: 7. Evidence:
  `results/data/per_trial_full.csv` contains 1500 rows.

* **REQ-8**: Stage-4 passive diagnostics — 25 conditions x 12 angles x 1 seed x 2 modes
  (EPSP_PASSIVE / IPSP_PASSIVE) = 600 trials, with HH off (`exptype = 2`) and synaptic overrides per
  t0065's `_apply_mode_override`. Steps: 7. Evidence: `results/data/per_trial_passive.csv` contains
  600 rows; IPSP_PASSIVE peak Vm flat at ≈ −60 mV across all conditions.

* **REQ-9**: Compute HWHM (degrees) per condition by linear interpolation around the half-max points
  of the 12-angle polar tuning curve. Set HWHM = `null` for any condition where peak mean rate < 1
  Hz. Steps: 8. Evidence: `results/metrics_summary.csv` HWHM column populated with floats or
  explicit nulls.

* **REQ-10**: Compute vector-sum DSI per condition as
  `|sum_i rate(theta_i) * exp(i*theta_i)| / sum_i rate(theta_i)`. Steps: 8. Evidence:
  `results/metrics_summary.csv` vector_sum_dsi column populated for all 25 conditions.

* **REQ-11**: Compute peak rate (Hz), rate at PD, rate at PD+180 deg (ND), and legacy PD-vs-ND DSI
  per condition. Steps: 8. Evidence: `results/metrics_summary.csv` populated.

* **REQ-12**: Compute RMSE vs the t0004 cosine target curve per condition using the t0012
  `tuning_curve_loss.score()` library. Steps: 8. Evidence: `results/metrics_summary.csv`
  rmse_vs_t0004 column populated.

* **REQ-13**: Save per-condition tuning curves as 25 CSVs (one per condition) in canonical schema
  `(angle_deg, trial_seed, firing_rate_hz)`. Steps: 7-8. Evidence: 25 CSVs in
  `results/data/tuning_curves/`.

* **REQ-14**: Save a combined `tuning_curves.csv` with all 25 x 12 = 300 (condition, angle) rows.
  Steps: 8. Evidence: `results/data/tuning_curves.csv` exists.

* **REQ-15**: Produce per-channel sensitivity plots (8 PNGs, one per channel: HWHM, vector-sum DSI,
  peak rate vs density). Steps: 9. Evidence: 8 PNG files in `results/images/`.

* **REQ-16**: Produce cross-channel comparison plot (`all_channels_dsi_vs_density.png`): vector-sum
  DSI vs density for all 8 channels overlaid. Steps: 9. Evidence: PNG file exists.

* **REQ-17**: Write registered project metrics per condition into `results/metrics.json` using the
  multi-variant format (one variant per condition). Registered metrics:
  `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`. Steps: 8. Evidence: `results/metrics.json` exists with 25 variants.

* **REQ-18**: Register the vendored channel pack (BK + SK + Kv7 + reused cadecay MODs + the t0067
  Nav1.6/NaP/NaR/Kv3/Kv4 MODs) as a library asset. Steps: 10. Evidence:
  `assets/library/dsgc_active_channel_pack/details.json` and `description.md` exist with all
  mandatory fields and sections.

* **REQ-19**: Pass criterion — for each of the 8 channels, at least one density produces |delta
  HWHM| > 5 deg OR |delta vector-sum DSI| > 0.05 relative to baseline. If a channel is inert at
  every density, report it as inert in the conclusion. Steps: 8-9. Evidence:
  `results/metrics_summary.csv` deltas column; inert channels logged.

* **REQ-20**: All 2100 trials complete with no instability flags. Instability = peak Vm > +60 mV, <
  −80 mV, or 0 spikes in PD AND ND directions of the same condition. Steps: 7. Evidence: per-trial
  CSV has an `is_unstable` column populated entirely with `False`.

## Approach

Recommended task types (already in `task.json`): **build-model** (Stage 1 vendors three new NEURON
mechanisms and one un-zeroing edit to Bed A's HOC) and **experiment-run** (Stages 3-5 run a
1500-FULL + 600-passive trial sweep across 25 conditions, with explicit independent variables
{channel kind, density level} and dependent variables {HWHM, vector-sum DSI, peak rate, RMSE}). Per
the build-model planning guidelines, all hyperparameters (channel densities, trial length, AP
threshold, baseline window) are recorded in `code/constants.py` before any trial runs. Per the
experiment-run guidelines, multi-condition results are written to `results/metrics.json` using the
explicit multi-variant format (25 variants), and the file uses fixed seeds for reproducibility.

The technical approach is **fork + extend** rather than rebuild. From `research_code.md` we know
that:

* Bed A's HOC `init_active` proc is at lines 114-152 of
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc` and
  zeroes both `RGCcaT` and `RGCcaL` at lines 144-145. These bind to `glbar_HHst` / `gtbar_HHst`
  inside `proc update()` so the deposited model has zero L-type and T-type calcium current. Without
  un-zeroing, the new `cad` calcium pool would see `cai = cainf` forever and BK / SK biophysics
  would be meaningless. **Replacing the literals with `0.0003 * active`** restores HHst's published
  default current density.

* The HOC source is bundled inside the t0008 immutable library asset. This task forks the HOC into
  `tasks/t0074_channel_tuning_width_bed_a/code/dsgc_model_t74.hoc` and re-sources it after
  `build_dsgc()` returns, replacing the proc body. This pattern matches the precedent set by t0046,
  t0047, t0067, t0065, t0066.

* t0067's `run_sweep.py` provides a complete 5-channel insertion pipeline. Its
  `_set_active_channel(*, soma, key)` zeroes all channel densities then sets the active one in
  S/cm². `_insert_all_channels_with_zero_gbar` inserts every mechanism once at build time. The MOD
  files in `code/mods/` use `NONSPECIFIC_CURRENT i` to avoid `USEION` collisions with HHst's three
  USEIONs (na/k/ca). This exact pattern is forked into t0074.

* The 12-angle bar-rotation protocol lives in t0008's `run_tuning_curve.py` lines 56-65 with
  `N_ANGLES = 12`, `ANGLE_STEP_DEG = 30.0`. Direction is encoded by rotating BIP synapse coordinates
  around the soma (`rotate_synapse_coords_in_place` in `build_cell.py:211-262`), not by changing
  gabaMOD. SAC inhib / SAC exc coords are pinned to baseline, preserving the bipolar-SAC
  arrival-time asymmetry that produces direction selectivity.

* The Stage-2 regression gate is a special case: t0067's baseline DSI = 0.7974683544303798 was
  computed using the **gabaMOD-swap** protocol (PD = 0.33, ND = 0.99, 16 conditions x 2 directions x
  5 seeds = 160 trials). To reproduce that fingerprint exactly, the gate uses the gabaMOD-swap
  protocol, NOT the 12-angle bar-rotation. Once the gate passes, the main sweep switches to the
  12-angle protocol (per `research_code.md` recommendations).

* From `research_internet.md`, the recommended MOD sources are: BK from Mainen-Sejnowski 1996
  (ModelDB 2488, `kca.mod`, V_½ ≈ −28 mV, Q10 = 2.3, Hill exponent 1, citing Pennefather 1990 +
  Reuveni 1993); SK from Hay 2011 (ModelDB 139653, `SK_E2.mod`, voltage-independent, Ca-driven, EC50
  = 0.43 µM, Hill = 4.8, τ = 1 ms, citing Köhler 1996); Kv7 from Hay 2011 (ModelDB 139653,
  `Im.mod`, Adams 1982 formalism, V_½ ≈ −35 mV, Q10 = 2.3). The calcium pool reuses t0024's
  `cadecay.mod` (Destexhe 1995 formalism, single-shell, depth = 0.1 µm, taur = 5 ms, cainf = 2e-4
  mM) which is already proven against the project's `USEION ca` convention on Bed B.

* From `research_internet.md` the recommended density grids (mS/cm²) are: BK low / med / high = 0.3
  / 1.0 / 3.0 (Mainen-Sejnowski range); SK low / med / high = 0.06 / 0.2 / 0.6 (Hay range); Kv7 low
  / med / high = 0.0001 / 0.001 / 0.005 (Hay range, expected mostly inert per Kv7-at-AIS literature
  precedent — Shah 2008, Hu 2007).

* From `research_papers.md`: HWHM is reported by Chen 2009 as the standard polar-tuning-curve width
  metric, decoupled from peak rate; vector-sum DSI is the appropriate residual metric for low-rate
  conditions (Hanson 2019 reports vector-sum DSI = 0.07 in non-DS conditions); standard
  classification threshold is `vector-sum > 0.2 AND DSI > 0.3` (Rivlin-Etzion 2012).

* The t0011 `tuning_curve_viz` library and t0012 `tuning_curve_loss` library are imported as
  registered project libraries. t0012 provides `compute_dsi`, `compute_peak_hz`, `compute_null_hz`,
  `compute_hwhm_deg`, and `score()` for RMSE vs the default t0004 cosine target. t0012 does **not**
  return null for low-rate curves — it returns 180.0 for flat curves. Per the task description's
  null-HWHM rule, t0074 must guard `compute_hwhm_deg` behind a `peak_hz < 1.0` check before calling.

* Vector-sum DSI is **new code** for this task (neither t0011 nor t0012 implement it). It is one
  line of math in a task-local metrics module.

**Alternative considered — feed `cai` from a precomputed time series instead of un-zeroing CaL /
CaT.** Rejected as the primary approach because the closed-form `cai` does not respond to the
voltage-dependent calcium influx that BK and SK kinetics expect; it would produce an artefactual
calcium signal that is independent of the cell's spiking activity. Retained as a **fallback** if
Stage-2 regression gate fails (per task description's risks section).

**Alternative considered — add CaT/CaL as separate MOD mechanisms instead of un-zeroing the HHst
internal currents.** Rejected because HHst already implements both currents internally (lines 26 /
31-32 / 219 of `HHst.mod`); duplicating them would produce double calcium current. The single-line
edit to `init_active` is the minimal-surface-area change.

**Alternative considered — use Mateos-Aparicio 2014 (ModelDB 169240) as the unified SK + Kv7
source.** Rejected because Hay 2011's `SK_E2.mod` and `Im.mod` are independently more canonical
(cited 300+ times) and the dentate-granule-cell-specific kinetics in MMS2014's `DGC_M.mod` are more
removed from the RGC use case than Hay's L5-pyramidal source. Retained as a second-line fallback if
Hay 2011's mechanisms produce instability in the Stage-2 gate.

## Cost Estimation

* **Total cost: $0.** All compute runs on the local Windows workstation. No remote machine, no paid
  API, no cloud storage.

* Local CPU compute: ~3.75 s/trial (t0067 measured rate under CVODE) x 2100 trials ≈ 2.2 hours
  wall-clock. This is the same machine + Python toolchain used by t0067; no new costs.

* External costs: $0. ModelDB MOD files (Mainen-Sejnowski 1996 ModelDB 2488; Hay 2011 ModelDB
  139653\) are publicly downloadable under standard ModelDB terms. No paywalled access.

* Project budget remaining: per `project/budget.json`, `total_budget = $1.00`,
  `per_task_default_limit = $1.00`. With $0 spend, this task is well under budget.

## Step by Step

### Milestone A — Vendor MODs and fork HOC (Stage 1)

1. **Create `code/paths.py`** — Path constants used by every other script. Defines:
   `TASK_DIR: Path` (the task root absolute path); `MODS_DIR = TASK_DIR / "code" / "mods"`;
   `BUILD_DIR = TASK_DIR / "code" / "build"` (where `nrnmech.dll` will live after compile);
   `FORKED_HOC = TASK_DIR / "code" / "dsgc_model_t74.hoc"`; `RESULTS_DIR = TASK_DIR / "results"`;
   `DATA_DIR = RESULTS_DIR / "data"`; `TUNING_CURVES_DIR = DATA_DIR / "tuning_curves"`;
   `IMAGES_DIR = RESULTS_DIR / "images"`; `PER_TRIAL_FULL_CSV = DATA_DIR / "per_trial_full.csv"`;
   `PER_TRIAL_PASSIVE_CSV = DATA_DIR / "per_trial_passive.csv"`;
   `TUNING_CURVES_CSV = DATA_DIR / "tuning_curves.csv"`;
   `METRICS_SUMMARY_CSV = RESULTS_DIR / "metrics_summary.csv"`;
   `METRICS_JSON = RESULTS_DIR / "metrics.json"`;
   `REGRESSION_GATE_JSON = RESULTS_DIR / "regression_gate.json"`; `T0004_TARGET_CSV` = absolute path
   to
   `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`.
   No `REQ-*` directly satisfied (foundation file).

2. **Create `code/constants.py`** — Typed enums and registries. Defines: `class ChannelKind(Enum)`
   with members `BASELINE, NAV16, NAP, NAR, KV3, KV4, BK, SK, KV7`; `class DensityLabel(Enum)` with
   members `LOW, MEDIUM, HIGH`; `class TrialMode(Enum)` with members
   `FULL, EPSP_PASSIVE, IPSP_PASSIVE` (copied from
   `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/constants.py`);
   `@dataclass(frozen=True, slots=True) class ChannelDef` with fields
   `kind: ChannelKind, suffix: str, gbar_attr: str, low_ms_cm2: float, med_ms_cm2: float, high_ms_cm2: float`;
   `CHANNEL_DEFS: tuple[ChannelDef, ...]` containing 8 entries — copy 5 from
   `tasks/t0067_t0065_soma_channel_addition_sweep/code/constants.py:30-63` (NAV16, NAP, NAR, KV3,
   KV4 with their existing low/med/high values) plus 3 new entries for BK (suffix `bk74`, gbar_attr
   `gbar_bk74`, 0.3 / 1.0 / 3.0), SK (suffix `sk74`, 0.06 / 0.2 / 0.6), KV7 (suffix `kv7t74`, 0.0001
   / 0.001 / 0.005); `GABA_MOD_PD: float = 0.33`, `GABA_MOD_ND: float = 0.99`,
   `GABA_MOD_OFF: float = 0.0`; `EXPTYPE_HH_ON: int = 1`, `EXPTYPE_HH_OFF: int = 2`;
   `B_AMPA_OFF_NS = 0.0`, `B_NMDA_OFF_NS = 0.0`, `S_GABA_OFF_NS = 0.0`, `S_ACH_OFF_NS = 0.0`,
   `ACH_MOD_OFF = 0.0`; `N_ANGLES: int = 12`, `ANGLE_STEP_DEG: float = 30.0`;
   `N_SEEDS_FULL: int = 5`, `N_SEEDS_PASSIVE: int = 1`; `SEED_BASE: int = 1`;
   `TSTOP_MS: float = 1000.0`, `BASELINE_END_MS: float = 100.0`, `AP_THRESHOLD_MV: float = -10.0`;
   `INSTABILITY_VM_MAX: float = 60.0`, `INSTABILITY_VM_MIN: float = -80.0`;
   `T0067_BASELINE_DSI: float = 0.7974683544303798`, `REGRESSION_TOLERANCE: float = 1e-3`;
   `LOW_RATE_HZ_THRESHOLD: float = 1.0` (HWHM null-out threshold per Chen 2009 convention). No
   `REQ-*` directly satisfied (foundation file).

3. **Copy 5 existing MODs from t0067**. Copy verbatim:
   `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod`
   into `tasks/t0074_channel_tuning_width_bed_a/code/mods/`. **Rename SUFFIX inside each MOD file**
   from `nav16t67` to `nav16t74` (and similarly for the others) to avoid DLL name collision with
   t0067 if both are loaded. Update each file's RANGE list and gbar attribute name to match.
   Satisfies prerequisites for REQ-7 (5 channels need to be present in t0074's DLL).

4. **Vendor 3 new MODs and copy `cadecay.mod`** [CRITICAL]. Create:
   * `code/mods/bk74.mod` — Adapt Mainen-Sejnowski 1996 `kca.mod` (ModelDB 2488). SUFFIX `bk74`;
     `USEION ca READ cai` (read-only Ca for activation); `NONSPECIFIC_CURRENT i` to avoid write
     conflict with HHst's `USEION k WRITE ik`. Parameters: `gbar (S/cm2) = 0`, V_½ ≈ −28 mV,
     Q10 = 2.3, Hill exponent 1 on Ca. Source: ModelDB 2488, DOI 10.1038/382363a0 (Mainen-Sejnowski
     1996). Document upstream citations Pennefather 1990, Reuveni 1993.
   * `code/mods/sk74.mod` — Adapt Hay 2011 `SK_E2.mod` (ModelDB 139653). SUFFIX `sk74`;
     `USEION ca READ cai`; `NONSPECIFIC_CURRENT i`. Parameters: `gbar (S/cm2) = 0`, EC50 = 0.43 µM,
     Hill = 4.8, τ = 1 ms, voltage-independent. Source: ModelDB 139653, DOI
     10.1371/journal.pcbi.1002107 (Hay 2011). Upstream citation: Köhler 1996, DOI
     10.1126/science.273.5282.1709.
   * `code/mods/kv7t74.mod` — Adapt Hay 2011 `Im.mod` (ModelDB 139653). SUFFIX `kv7t74`;
     `NONSPECIFIC_CURRENT i`. Parameters: `gbar (S/cm2) = 0`, V_½ ≈ −35 mV, Q10 = 2.3, Adams
     1982 formalism (`mAlpha = 3.3e-3 × exp(2.5 × 0.04 × (v + 35))`). Source: ModelDB 139653, DOI
     10.1371/journal.pcbi.1002107 (Hay 2011). Upstream citation: Adams 1982, DOI
     10.1113/jphysiol.1982.sp014102.
   * `code/mods/cadecay.mod` — Copy verbatim from
     `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`.
     Defaults: `depth = 0.1 um`, `taur = 5 ms`, `cainf = 2e-4 mM`. SUFFIX `cad`,
     `USEION ca READ ica, cai WRITE cai`. Source DOI to be recorded: 10.1016/0006-3495(95)80109-9
     (Destexhe 1995 formalism).
   * `code/mods/mod_func.c` — Adapt from t0067's mod_func.c. Register all 9 mechanisms:
     `_nav16t74_reg`, `_napt74_reg`, `_nart74_reg`, `_kv3t74_reg`, `_kv4t74_reg`, `_bk74_reg`,
     `_sk74_reg`, `_kv7t74_reg`, `_cad_reg`.
   * `code/run_nrnivmodl.cmd` — Compile script (Windows). Adapts t0067's compile command to point
     at this task's mods folder; outputs `code/build/nrnmech.dll`. Run `code/run_nrnivmodl.cmd` and
     confirm `code/build/nrnmech.dll` exists. Expected output: "Successfully built mod files."
     Satisfies REQ-1, REQ-2, REQ-3, REQ-4.

5. **Fork the Bed A HOC** [CRITICAL]. Create
   `tasks/t0074_channel_tuning_width_bed_a/code/dsgc_model_t74.hoc` by copying verbatim from
   `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc`, then
   editing only lines 144-145 to read `RGCcaT=0.0003*active` and `RGCcaL=0.0003*active` (matches
   HHst's published default `glbar` / `gtbar` of 0.0003 S/cm²). Document the change with a
   `/* t0074: un-zeroed CaT/CaL to feed cad calcium pool */` comment at the top of the file.
   Satisfies REQ-5.

### Milestone B — Stage 2 regression gate

6. **Create `code/regression_gate.py`** [CRITICAL]. This standalone script:
   * Imports `build_dsgc, apply_params, read_synapse_coords` from
     `tasks.t0008_port_modeldb_189347.code.build_cell`.
   * Calls `h = build_dsgc()`, then `h.load_file(1, str(FORKED_HOC))` to override `init_active` with
     the un-zeroed CaT/CaL version.
   * Loads the t0074 DLL via `h.nrn_load_dll(str(BUILD_DIR / "nrnmech.dll"))`.
   * Calls a copy of t0067's `_insert_all_channels_with_zero_gbar(*, h, soma)` which inserts all 8
     channel mechanisms plus `cad` on the soma, all with `gbar = 0`.
   * Runs the t0067 gabaMOD-swap protocol: 16 baseline conditions x 2 directions (PD via
     `h.gabaMOD = 0.33`, ND via `h.gabaMOD = 0.99`) x 5 seeds = 160 trials. Per trial:
     `apply_params(h=h, seed=seed)` → set `h.gabaMOD` → set `h.exptype = 1` →
     `h("init_active()")` → `h("access RGC.soma")` → `h("update()")` → `h("placeBIP()")` →
     keep all channel gbars at 0 (baseline condition only) → `h.finitialize(-65)` →
     `h.continuerun(TSTOP_MS)`. Counts soma spikes via threshold crossings of
     `AP_THRESHOLD_MV = -10.0`.
   * Aggregates per-condition mean PD spike count and ND spike count; computes
     `dsi = (pd - nd) / (pd + nd)` averaged across 16 conditions.
   * Writes `results/regression_gate.json` with fields:
     `{"measured_dsi": float, "target_dsi": 0.7974683544303798, "tolerance": 1e-3, "passed": bool, "delta": float, "n_trials": 160}`.
   * **Validation gate**: if `abs(measured_dsi - 0.7974683544303798) > 1e-3`, the script writes
     `passed: false` and exits with code 1. The implementation agent must STOP and create an
     intervention file documenting the deviation. Trivial baseline: t0067's measured baseline DSI of
     0.7974683544303798 is the exact target. Failure condition: any deviation > 1e-3 means the
     un-zeroed CaL/CaT changed the resting dynamics; switch to the closed-form `cai` fallback (feed
     `cai` from a precomputed time series). Run:
     `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0074_channel_tuning_width_bed_a -- uv run python -u code/regression_gate.py`.
     Expected output: `regression_gate.json` with `passed: true`. Satisfies REQ-6.

### Milestone C — Stage 3 / Stage 4 main sweep

7. **Create `code/run_sweep.py`** [CRITICAL]. This is the main sweep driver. Forks
   `tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py:1-327` with extensions:
   * Reuses the t0067 helpers `_ensure_t74_dll_loaded`, `_insert_all_channels_with_zero_gbar`,
     `_set_active_channel`. Renames the DLL helper to load this task's DLL.
   * Replaces the 2-direction PD/ND iteration with the **12-angle bar-rotation protocol**.
     Concretely: imports `read_synapse_coords, rotate_synapse_coords_in_place, reset_synapse_coords`
     from `tasks.t0008_port_modeldb_189347.code.build_cell`. Captures
     `baseline_coords = read_synapse_coords(h)` once after `build_dsgc()`. Per trial: call
     `reset_synapse_coords(h=h, baseline=baseline_coords)` then
     `rotate_synapse_coords_in_place(h=h, angle_deg=angle_deg, baseline=baseline_coords)`.
   * Adds a `TrialMode` field to the trial schedule. For each of 25 conditions:
     - 12 angles x 5 seeds in `TrialMode.FULL` (`exptype = 1`, no synaptic override).
     - 12 angles x 1 seed in `TrialMode.EPSP_PASSIVE` (`exptype = 2`, `h.gabaMOD = GABA_MOD_OFF`,
       `h.s2ggaba = 0`).
     - 12 angles x 1 seed in `TrialMode.IPSP_PASSIVE` (`exptype = 2`, `h.b2gampa = 0`,
       `h.b2gnmda = 0`, `h.s2gach = 0`, `h.achMOD = 0`).
   * Copies the `_apply_mode_override(*, h, mode)` function verbatim from
     `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py:144-167`.
   * Per-trial ordering: `apply_params(h=h, seed=seed)` → `_apply_mode_override(h=h, mode=mode)`
     → set `h.exptype` → `h("init_active()")` → `h("access RGC.soma")` → `h("update()")` →
     `h("placeBIP()")` → `_set_active_channel(h=h, soma=soma, channel=channel, density=density)`
     → `rotate_synapse_coords_in_place` → `h.finitialize(-65)` → `h.continuerun(TSTOP_MS)`.
   * Records per trial:
     `condition_id, channel_kind, density_label, angle_deg, trial_seed, trial_mode, n_spikes, firing_rate_hz, peak_vm_mv, baseline_vm_mv, is_unstable`.
   * Writes `results/data/per_trial_full.csv` (1500 rows) and `results/data/per_trial_passive.csv`
     (600 rows).
   * **Validation gate before full sweep**: First runs a single condition (the baseline) at
     `--limit 12` (12 angles, 1 seed, FULL mode = 12 trials), inspects 5 individual trials by
     reading their per-trial spike counts and peak Vm, and confirms peak Vm is in [-80, +60] mV and
     spike counts are in [0, 100]. Trivial baseline: t0067 reports the baseline condition produces
     12-15 spikes per 1 s trial in PD and ~3 spikes in ND. If the small run reports 0 spikes at
     every angle or peak Vm > +60 mV, halt and inspect individual trial logs before proceeding.
     Expected: 12 trials complete, peak Vm in normal range. Run:
     `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0074_channel_tuning_width_bed_a -- uv run python -u code/run_sweep.py`.
     Expected output: 2100 trials complete, no `is_unstable=True` rows. Satisfies REQ-7, REQ-8,
     REQ-13, REQ-20.

### Milestone D — Stage 5 width metrics and visualisation

8. **Create `code/compute_width_metrics.py`**. Reads `results/data/per_trial_full.csv`. For each of
   25 conditions:
   * Aggregates per-trial firing rates into `(angle_deg, trial_seed, firing_rate_hz)` canonical CSV
     and writes one CSV per condition to `results/data/tuning_curves/<condition_id>.csv`.
   * Concatenates all 25 into `results/data/tuning_curves.csv` with an additional `condition_id`
     column (300 rows total).
   * Computes:
     - `peak_hz` via `compute_peak_hz` from
       `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics`.
     - `null_hz` via `compute_null_hz` (rate at peak + 180 deg).
     - `dsi_pd_nd = compute_dsi(curve=tc)` — legacy 2-angle DSI.
     - `hwhm_deg`: gated by `peak_hz < 1.0` — if true, `None`; else `compute_hwhm_deg(curve=tc)`.
       Per Chen 2009 convention.
     - `vector_sum_dsi`: implemented inline as
       `abs(np.sum(rates * np.exp(1j * np.deg2rad(angles)))) / np.sum(rates)`.
     - `pd_angle_deg`: angle of the `vector_sum_dsi` complex argument in degrees.
     - `rate_at_pd_hz`: firing rate at the angle bin closest to `pd_angle_deg`.
     - `rate_at_nd_hz`: firing rate at `pd_angle_deg + 180`.
     - `rmse_vs_t0004`: from
       `score(simulated_curve_csv=condition_csv, target_curve_csv=T0004_TARGET_CSV)` from
       `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring`. Read the
       `rmse_vs_target_hz` field.
     - `tuning_curve_reliability`: Pearson correlation across 5 seeds of per-seed firing rate
       vectors, averaged over the 5*4/2 = 10 seed pairs.
     - `delta_hwhm_deg` = `hwhm_deg - baseline_hwhm_deg` (None-safe).
     - `delta_vector_sum_dsi` = `vector_sum_dsi - baseline_vector_sum_dsi`.
     - `is_inert`: True if `abs(delta_hwhm_deg) <= 5.0 AND abs(delta_vector_sum_dsi) <= 0.05` across
       all densities of the channel.
   * Writes `results/metrics_summary.csv` with 25 rows and columns:
     `condition_id, channel_kind, density_label, peak_hz, null_hz, dsi_pd_nd, hwhm_deg, vector_sum_dsi, pd_angle_deg, rate_at_pd_hz, rate_at_nd_hz, rmse_vs_t0004, tuning_curve_reliability, delta_hwhm_deg, delta_vector_sum_dsi, is_inert`.
   * Writes `results/metrics.json` using the **explicit multi-variant format**: top-level
     `metrics_format: "explicit-variants"`, `variants: list[Variant]` with one variant per
     condition, each variant containing keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
     `tuning_curve_reliability`, `tuning_curve_rmse`. Per
     `arf/specifications/metrics_specification.md`. Use `null` (JSON) for HWHM when low-rate
     condition. Run:
     `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0074_channel_tuning_width_bed_a -- uv run python -u code/compute_width_metrics.py`.
     Expected output: `metrics_summary.csv` (25 rows), `metrics.json` (25 variants), 25
     per-condition CSVs, 1 combined CSV. Satisfies REQ-9, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14,
     REQ-17, REQ-19.

9. **Create `code/plot_per_channel_sensitivity.py` and `code/plot_cross_channel_comparison.py`**.
   * `plot_per_channel_sensitivity.py`: For each of 8 channels (NAV16, NAP, NAR, KV3, KV4, BK, SK,
     KV7), uses
     `tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian.plot_cartesian_tuning_curve`
     with the 3 density-level CSVs overlaid (or a small custom matplotlib panel showing 3 sub-plots:
     HWHM vs density, vector-sum DSI vs density, peak rate vs density, with the baseline value as a
     dashed horizontal reference). Outputs 8 PNGs in `results/images/`: `sensitivity_<channel>.png`
     (one per channel).
   * `plot_cross_channel_comparison.py`: Uses
     `tasks.t0011_response_visualization_library.code.tuning_curve_viz.overlay.plot_multi_model_overlay`
     OR a custom matplotlib chart. Plots vector-sum DSI on the y-axis vs density level (low / med /
     high) on the x-axis, with one line per channel (8 lines total in Okabe-Ito palette). Includes a
     horizontal reference line at the baseline `vector_sum_dsi` value. Output:
     `results/images/all_channels_dsi_vs_density.png`. Run both via run_with_logs. Expected output:
     8 + 1 = 9 PNGs in `results/images/`. Satisfies REQ-15, REQ-16.

### Milestone E — Library asset creation

10. **Register the vendored channel pack as a library asset**. Create:
    * `assets/library/dsgc_active_channel_pack/details.json` with
      `library_id = "dsgc_active_channel_pack"`, `version = "0.1.0"`, `module_paths` listing
      `["code/mods/nav16t74.mod", "code/mods/napt74.mod", "code/mods/nart74.mod", "code/mods/kv3t74.mod", "code/mods/kv4t74.mod", "code/mods/bk74.mod", "code/mods/sk74.mod", "code/mods/kv7t74.mod", "code/mods/cadecay.mod", "code/mods/mod_func.c", "code/dsgc_model_t74.hoc", "code/run_nrnivmodl.cmd"]`,
      `description_path = "description.md"`, `entry_points` listing the compiled DLL and the forked
      HOC as scripts. Document each MOD's source DOI in the `short_description` and the
      description.md.
    * `assets/library/dsgc_active_channel_pack/description.md` with all 7 mandatory sections:
      Metadata (table of MOD files and source DOIs), Overview (purpose: vendored 8-channel pack for
      active-conductance sweeps on Bed A), API Reference (MOD SUFFIX list with V_½, Q10,
      Ca-dependence per channel), Usage Examples (Python snippet showing
      `h.nrn_load_dll(str(BUILD_DIR / "nrnmech.dll"))` and `h.load_file(1, str(FORKED_HOC))`),
      Dependencies (NEURON >= 8.0, no Python deps), Testing (run `code/regression_gate.py` and
      confirm `passed: true`), Main Ideas (3+ bullets covering NONSPECIFIC_CURRENT pattern, Ca-pool
      reuse, density grids), Summary. Satisfies REQ-18.

## Remote Machines

None required. All compute runs on the local Windows workstation in the existing repo + uv venv. The
2100-trial sweep takes ~2.2 hours wall-clock at t0067's measured CVODE rate (~3.75 s/trial); a
remote machine would not meaningfully accelerate this NEURON simulation since CVODE is single-thread
and the trial overhead dominates the per-trial cost. No GPU is needed.

## Assets Needed

* `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/` (Bed A library) — provides
  `build_dsgc`, `apply_params`, `read_synapse_coords`, `rotate_synapse_coords_in_place`, the bundled
  HOC sources (forked into this task's `code/`), HHst.mod, bipNMDA.mod, SACinhib.mod, SACexc.mod.
  Imported via `from tasks.t0008_port_modeldb_189347.code.build_cell import ...`.

* `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/` — provides
  `plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`, `plot_multi_model_overlay`. Imported via
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import ...`.

* `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/` — provides
  `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `score`. Imported via
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import score, ScoreReport`
  and equivalent for `metrics`.

* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`
  — copied verbatim into `code/mods/cadecay.mod` (reuse, not import).

* `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod`
  — copied (with SUFFIX rename to `*t74`) into `code/mods/`. The `_set_active_channel` and
  `_insert_all_channels_with_zero_gbar` patterns are forked from
  `tasks/t0067_t0065_soma_channel_addition_sweep/code/run_sweep.py`.

* `tasks/t0067_t0065_soma_channel_addition_sweep/results/metrics.json` — supplies the reference
  baseline DSI value `T0067_BASELINE_DSI = 0.7974683544303798` for the regression gate (REQ-6).

* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py` lines 144-167 — copied
  `_apply_mode_override(*, h, mode)` for Stage 4 passive diagnostics.

* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
  — t0004 cosine target curve, used as the reference for `rmse_vs_t0004` in Stage 5.

* External: ModelDB 2488 (`https://modeldb.science/2488`) `kca.mod` source for BK; ModelDB 139653
  (`https://modeldb.science/139653`) `SK_E2.mod` and `Im.mod` source for SK and Kv7. Inspected via
  research_internet.md; vendored into this task with documented provenance.

## Expected Assets

This task produces exactly **one library asset** (matches `task.json`
`expected_assets.library = 1`):

* **Library**: `dsgc_active_channel_pack` (in `assets/library/dsgc_active_channel_pack/`). Contains
  the 9 vendored MOD files (5 NaP/Nav1.6/NaR/Kv3/Kv4 forked from t0067, 3 new BK/SK/Kv7 from
  Mainen-Sejnowski 1996 + Hay 2011, 1 reused cadecay from t0024), the forked `dsgc_model_t74.hoc`
  (Bed A HOC with un-zeroed CaT/CaL), the `mod_func.c` registration boilerplate, the
  `run_nrnivmodl.cmd` build script, and a description.md documenting every MOD's source DOI,
  parameter defaults, and density grid recommendations. This becomes a dependency for t0075
  (AIS-localised Kv7 follow-up) and any future task needing these channels.

Other outputs (not formal assets per `task.json`): 25 per-condition tuning-curve CSVs, the combined
`tuning_curves.csv`, `metrics_summary.csv` (the width metrics table), `metrics.json` (registered
project metrics with 25 explicit variants), 8 per-channel sensitivity PNGs, 1 cross-channel
comparison PNG, `regression_gate.json`, and `results/data/per_trial_full.csv` /
`per_trial_passive.csv`.

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already done) | 0 (complete) |
| Implementation: paths + constants + MOD vendoring + HOC fork (Steps 1-5) | 2 h |
| Compile DLL + manual smoke test (end of Step 4) | 30 min |
| Stage 2 regression gate code + run (Step 6, 160 trials) | 30 min coding + 10 min run |
| Stage 3/4 sweep code (Step 7) | 1 h coding |
| Stage 3/4 sweep run (2100 trials at ~3.75 s/trial) | 2.2 h compute |
| Stage 5 width metrics + plots (Steps 8-9) | 30 min coding + 10 min run |
| Library asset creation (Step 10) | 30 min |
| Verification + PR | 30 min |
| **Total** | **~7-8 h** (~3-4 h coding + 2.2 h sim + ~1.5 h analysis / asset / verification) |

Compute time matches the task description's "~2.2 h wall-clock" estimate (= 2100 trials * 3.75
s/trial / 3600). Coding time (~3-4 h) matches the task description's coding estimate.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Calcium-pool kinetics drift: un-zeroed CaT/CaL changes resting dynamics, baseline DSI deviates from t0067's 0.7974683544303798 by more than 1e-3. | Medium | Blocking (Stage-2 gate fail) | Stage-2 regression gate runs first; if it fails, fall back to closed-form `cai` (precomputed time-series fed into BK/SK as `cai`) which decouples calcium kinetics from CaL/CaT and preserves Bed A's HHst dynamics. Alternative: lower CaT/CaL gbar from 0.0003 to 0.0001 (HHst's lower bound). |
| BK/SK MOD source kinetics inconsistent with RGC firing rates: vendored MODs from cortical/hippocampal models produce instability or unrealistic firing patterns at 35-37 °C. | Medium | Blocking | Apply Q10 = 2.3 correction explicitly in MOD parameters when porting from 21-25 °C reference temperature. If still unstable: fall back to second-line MOD source (Mateos-Aparicio 2014 ModelDB 169240 `DGC_sAHP.mod` for SK; `DGC_M.mod` for Kv7). Document the choice in `details.json`. |
| Kv7 inert at all densities: somatic Kv7 in DSGCs is poorly documented in the literature; the canonical Kv7 site is the AIS (Shah 2008). | High | Non-blocking | This is an expected outcome per `research_papers.md` Hypothesis 4. Log it as a clean negative result and recommend the t0075 AIS-localised Kv7 follow-up. Pass criteria already accommodate inert channels (one channel per row may be inert if every density falls below the |
| HWHM undefined for low-rate conditions: NaP_high, certain Kv7 / SK / BK densities may produce sub-1 Hz curves where HWHM is mathematically ill-defined. | Medium | Non-blocking | `compute_hwhm_deg` is called only when `peak_hz >= 1.0`; otherwise HWHM is set to `null` per Chen 2009 convention and the project's "use None for missing data, not 0.0" style rule. Vector-sum DSI remains defined for all curves and serves as the primary residual metric (Hanson 2019). |
| DLL name collision: t0074's MOD SUFFIXes overlap with t0067's already-loaded DLL. | Low | Blocking (NEURON load error) | Step 3 explicitly renames all SUFFIXes from `*t67` to `*t74`. NEURON allows multiple `nrn_load_dll` calls only when SUFFIXes are unique. If collision occurs at runtime, kill all Python processes (NEURON state persists across `import neuron`) and re-run from a fresh interpreter. |
| 2100-trial sweep runtime exceeds local-machine availability: local CPU contention or thermal throttling slows the sweep below 3.75 s/trial. | Low | Schedule slip | Run the sweep in a single overnight session with the laptop on AC power and screen-saver disabled. Save intermediate per-trial CSV rows after each condition (every 60-84 trials) so a partial restart is possible. Idempotency: the sweep skips conditions whose CSV row count matches the expected per-condition trial count. |
| Trial instability: high-density NaP or Nav1.6 produces depolarisation block (peak Vm > +60 mV held). | Medium | Per-condition flagging, not blocking | Mark with `is_unstable = True` in the per-trial CSV per the t0067 instability policy (peak Vm > +60 mV, < −80 mV, or 0 spikes in PD AND ND). Save the row and continue. Report the count of unstable trials per condition in the results summary. The regression-gate baseline run must have 0 unstable trials. |
| `cad` MOD `USEION ca` collision with HHst: HHst writes ica; cad reads ica + writes cai; this composition is untested on Bed A. | Low | Blocking (NEURON build error) | This pattern is proven on Bed B (`tasks/t0024_*/code/build_cell.py:194` inserts `cad` and HHst-equivalent mechanism on the same compartment). If `nrnivmodl` or `nrn_load_dll` errors, inspect the verbose nrnmech build log and add an explicit `INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}` block to `cadecay.mod` if missing. |

## Verification Criteria

* **Stage-2 regression gate passes**. Run
  `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0074_channel_tuning_width_bed_a -- uv run python -u code/regression_gate.py`.
  Confirm `results/regression_gate.json` exists and contains `"passed": true` with
  `abs(measured_dsi - 0.7974683544303798) < 1e-3`. This satisfies REQ-6.

* **All 2100 trials complete with no instability flags**. Run
  `PYTHONIOENCODING=utf-8 uv run python -c "import pandas as pd; full = pd.read_csv('results/data/per_trial_full.csv'); passive = pd.read_csv('results/data/per_trial_passive.csv'); assert len(full) == 1500; assert len(passive) == 600; assert (~full['is_unstable']).all(); assert (~passive['is_unstable']).all(); print('OK')"`.
  Expected output: `OK`. This satisfies REQ-7, REQ-8, REQ-20.

* **Width metrics table fully populated**. Run
  `PYTHONIOENCODING=utf-8 uv run python -c "import pandas as pd; df = pd.read_csv('results/metrics_summary.csv'); assert len(df) == 25; assert df['vector_sum_dsi'].notna().all(); assert df['peak_hz'].notna().all(); assert df['rmse_vs_t0004'].notna().all(); assert df['dsi_pd_nd'].notna().all(); print('OK')"`.
  Expected output: `OK`. The `hwhm_deg` column may contain nulls only for sub-1-Hz conditions. This
  satisfies REQ-9, REQ-10, REQ-11, REQ-12.

* **Per-condition CSVs and combined CSV exist**. Run
  `PYTHONIOENCODING=utf-8 uv run python -c "from pathlib import Path; assert len(list(Path('results/data/tuning_curves').glob('*.csv'))) == 25; import pandas as pd; assert len(pd.read_csv('results/data/tuning_curves.csv')) == 300; print('OK')"`.
  Expected output: `OK`. This satisfies REQ-13, REQ-14.

* **Plots exist**. Run
  `PYTHONIOENCODING=utf-8 uv run python -c "from pathlib import Path; imgs = list(Path('results/images').glob('*.png')); assert len(imgs) >= 9, imgs; assert (Path('results/images/all_channels_dsi_vs_density.png')).exists(); print('OK')"`.
  Expected output: `OK`. This satisfies REQ-15, REQ-16.

* **Library asset exists and validates**. Run
  `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0074_channel_tuning_width_bed_a -- uv run python -m arf.scripts.verificators.verify_library_asset t0074_channel_tuning_width_bed_a dsgc_active_channel_pack`.
  Expected output: zero errors. This satisfies REQ-18.

* **`metrics.json` registered metrics complete**. Run
  `PYTHONIOENCODING=utf-8 uv run python -c "import json; data = json.load(open('results/metrics.json')); assert data.get('metrics_format') == 'explicit-variants'; assert len(data['variants']) == 25; for v in data['variants']: assert 'direction_selectivity_index' in v['metrics']; assert 'tuning_curve_rmse' in v['metrics']; print('OK')"`.
  Expected output: `OK`. This satisfies REQ-17.

* **Pass criterion: at least one density per channel produces measurable change**. Run
  `PYTHONIOENCODING=utf-8 uv run python -c "import pandas as pd; df = pd.read_csv('results/metrics_summary.csv'); inert = df.groupby('channel_kind')['is_inert'].all(); inert_channels = inert[inert].index.tolist(); print('INERT_CHANNELS:', inert_channels)"`.
  Expected output: a list containing at most one channel name (Kv7 expected per Hypothesis 4). Inert
  channels are reported in the conclusion; the check itself does not fail the task. This satisfies
  REQ-19.

* **Plan verificator passes**. Run
  `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.verificators.verify_plan t0074_channel_tuning_width_bed_a`.
  Expected output: zero errors.
