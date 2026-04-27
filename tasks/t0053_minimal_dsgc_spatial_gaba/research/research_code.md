---
spec_version: "1"
task_id: "t0053_minimal_dsgc_spatial_gaba"
research_stage: "code"
tasks_reviewed: 13
tasks_cited: 12
libraries_found: 9
libraries_relevant: 3
date_completed: "2026-04-25"
status: "complete"
---
# Research Code: Minimal From-Scratch DSGC with Spatial PD/ND-Asymmetric Inhibition

## Task Objective

Build a minimal compartmental DSGC identical to [t0052] in every respect (`hh` on `soma` and
`axon_initial_segment`, passive dendrites with `Rm=5999`, `Ra=100`, `cm=1.0`, 100 co-located E+I
synapse pairs uniformly random over total dendritic length with fixed seed 0, AMPA `Exp2Syn` 0.5 nS
rise=0.5 ms decay=2.5 ms, GABA `Exp2Syn` 2 nS rise=1 ms decay=20 ms, 12 directions x 10 trials at 1
um/ms over 1500 ms) **except** the inhibition driver. Replace the scalar `gabaMOD(theta)` per-NetCon
weight scaling with a per-synapse spatial firing gate: each I synapse fires only when
`cos(theta_stim - theta_centrifugal_i) < 0`, where
`theta_centrifugal_i = atan2(y_i - y_soma, x_i - x_soma)`; full 2 nS amplitude when fired, no firing
otherwise. Produce the same six output classes plus a new direction-specific polar plot of "fraction
of I synapses active vs direction" (REQ-7 in the task verification criteria). Package the model as
the `minimal_dsgc_spatial_gaba` library asset and emit per-direction soma V(t), EPSP/IPSP traces,
PSTH, polar tuning curve, primary DSI, vector-sum DSI, preferred direction, peak/null Hz.

## Library Landscape

The project's library aggregator is not registered as a Python module on this branch (running
`uv run python -m arf.scripts.aggregators.aggregate_libraries` returns
`No module named arf.scripts.aggregators.aggregate_libraries`). Library discovery used a glob of
`tasks/*/assets/library/*` over the worktree state; nine library assets exist, all `details.json`
spec v2, none with correction overlays.

| Library ID | Created by | Relevance | Import path |
| --- | --- | --- | --- |
| `tuning_curve_viz` | [t0011] | **Relevant — import** | `tasks.t0011_response_visualization_library.code.tuning_curve_viz` |
| `tuning_curve_loss` | [t0012] | **Relevant — import** | `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` |
| `minimal_dsgc_scalar_gaba` | [t0052] | **Relevant — pattern source (NOT importable; copy code)** | n/a |
| `modeldb_189347_dsgc_exact` | [t0046] | Marginal — older HOC-driven from-scratch pattern, superseded by t0052 | n/a |
| `modeldb_189347_dsgc_dendritic` | [t0022] | Marginal — Exp2Syn / NetStim / NetCon scheduler patterns, superseded by t0052 | n/a |
| `modeldb_189347_dsgc_gabamod` | [t0020] | Marginal — HOC `gabaMOD` global pattern; superseded by t0052 scalar implementation | n/a |
| `modeldb_189347_dsgc` | [t0008] | Not relevant — placeholder-radius HOC port, superseded by t0009 + t0052 | n/a |
| `de_rosenroll_2026_dsgc` | [t0024] | Not relevant — different cell, NMDA-driven, AR(2) noise; not a substrate | n/a |
| `tuning_curve_viz` and `tuning_curve_loss` are the **only** libraries imported. |  |  |  |

Per the project cross-task import rule, only registered libraries can be imported across tasks. The
sibling library `minimal_dsgc_scalar_gaba` from [t0052] is **structurally identical** to what t0053
needs except for the inhibition driver, but it cannot be imported — every relevant module must be
**copied verbatim** into `tasks/t0053_minimal_dsgc_spatial_gaba/code/` with all
`tasks.t0052_minimal_dsgc_scalar_gaba.code.*` import paths rewritten to
`tasks.t0053_minimal_dsgc_spatial_gaba.code.*`.

## Key Findings

### Sibling Task t0052 Provides 12 Directly Reusable Modules

[t0052] just merged to main (2026-04-25) with a complete, verificator-passing implementation of the
scalar-gabaMOD variant. Its `code/` contains 15 files (2,183 lines total) that map onto every module
t0053 needs except the inhibition rule itself. The file inventory and direct line counts are:
`cell.py` (215 lines, SWC -> NEURON cell builder with explicit soma/AIS/dendrite tagging),
`compute_metrics.py` (304 lines, multi-variant metrics + IPSP-conductance hard gate), `constants.py`
(125 lines, all simulation constants), `metrics_extra.py` (44 lines, vector-sum DSI + preferred
direction), `neuron_bootstrap.py` (82 lines, Windows NEURONHOME bootstrap with sentinel env-var),
`paths.py` (78 lines, centralised path constants), `placement.py` (87 lines, length-weighted random
placement with seed-pinned RNG), `render_figures.py` (231 lines, six figure families plus
polar/Cartesian tuning curves via t0011 library), `run_tuning_curve.py` (390 lines, 12 x 10 x 3
sweep harness with dry-run gate), `swc_io.py` (180 lines, SWC parser), `synapses.py` (181 lines,
EiPair / scalar gabaMOD / per-pair NetStim+NetCon), `trial.py` (140 lines, single-trial NEURON
runner), `test_gaba_mod.py` (22 lines), `test_quiescent_rest.py` (104 lines), and `__init__.py`
(empty). Every file already follows the project Python style guide, `mypy` passes across 263 source
files in [t0052]'s implementation step, and the verificator is clean.

### Inhibition Driver Is the Only Real New Code

The task description requires that everything but the I-synapse firing rule be identical to [t0052].
The scalar-gabaMOD logic in [t0052] lives in two places:
`tasks/t0052_minimal_dsgc_scalar_gaba/code/synapses.py:54-73` (the
`gaba_mod(theta_deg, theta_pd_deg)` function returning
`0.33 + 0.66 * (1 - cos(theta - theta_pd)) / 2`) and
`tasks/t0052_minimal_dsgc_scalar_gaba/code/synapses.py:155-181` (`schedule_ei_onsets` setting
`pair.gaba_netcon.weight[0] = GABA_BASE_NS * gaba_mod_theta * 1e-3` for every pair every trial). For
t0053 these two pieces are replaced by a single per-synapse boolean firing mask: precompute
`theta_centrifugal_i = atan2(y_i - y_soma, x_i - x_soma)` once at pair-construction time, then per
trial decide `fires_i = cos(theta_stim - theta_centrifugal_i) < 0`. When `fires_i` is True schedule
`pair.gaba_netstim.start = onset_ms` and `pair.gaba_netcon.weight[0] = GABA_BASE_NS * 1e-3` (no
scaling); when False, suppress the firing entirely (set `gaba_netcon.weight[0] = 0` or set
`gaba_netstim.start` to a value past `TSTOP_MS`). The full-amplitude-when-fired rule is critical:
the task specifies "2 nS no scaling" as the I conductance for any active synapse.

### Soma Position Is Required for theta_centrifugal_i

The centripetal-gating rule needs the soma centroid (x_soma, y_soma) so each synapse's centrifugal
direction can be computed. [t0052]'s `cell.py:146` defines `soma_origin = soma_compartments[0]` (the
SWC's first soma row at coordinate index 0). The soma in the calibrated SWC is at ~(0, 0, 0) but
t0053 must not assume that; the spatial driver must read `soma_origin.x` and `soma_origin.y` from
the constructed cell. The cleanest approach is to extend the [t0052]:`CellHandles` dataclass
(currently `soma`, `axon_initial_segment`, `dendrites`, `dendrite_xyz_um`) with
`soma_origin_um: tuple[float, float, float]` populated from
`(soma_origin.x, soma_origin.y, soma_origin.z)` at build time. The downstream synapse construction
then receives the soma origin and stores `theta_centrifugal_i` per `EiPair`.

### Spatial Gating Has No Hard-Conductance Sanity Check Like t0052's IPSP-Ratio Gate

[t0052]'s `compute_metrics.py:185-206` enforces a hard `gNULL/gPD ~= 3` gate (IPSP_RATIO_LOWER=2.7,
IPSP_RATIO_UPPER=3.3) via `assert` because the scalar gabaMOD endpoints 0.33 / 0.99 are exactly
closed-form. t0053's spatial mechanism does not produce any analogous single-scalar conductance
ratio — every direction either fires a synapse at full amplitude or not at all. The gating
mechanism's analytic prediction is instead the **fraction of I synapses active**: for direction
`theta_stim`, the fraction is the proportion of pairs whose `theta_centrifugal_i` lies in the
half-plane `cos(theta_stim - theta_centrifugal_i) < 0`. With uniform-random seed-0 placement on a
roughly symmetric dendritic field this is approximately 50% across all directions; deviations
measure the dendritic-field asymmetry caused by the off-centre soma position. The new `metrics.json`
derived quantity is therefore `active_fraction_per_direction: dict[int, float]` (12 entries) and the
new figure (REQ-7 in the task description) is a polar plot of those values. Replace the scalar-gate
`assert` in [t0052]:`compute_metrics.py:194-205` with a softer warning: print and record the
per-direction fractions but do not hard-fail; document that the expected mean is ~50% with deviation
from morphology asymmetry.

### t0050 Audit Confirms the Spatial Mechanism Is Novel in This Project

[t0050] showed that the deposited Poleg-Polsky DSGC implements direction selectivity via a single
scalar `gabaMOD = 0.33 + 0.66 * direction` applied to **every** SAC inhibitory synapse, with no
spatial threshold of any kind. The deposited GABA placement is also spatially symmetric around the
arbour midline (side_a/side_b = 0.972), so the lattice itself contributes no asymmetry. t0053 is the
project's first implementation of a true spatial-asymmetry inhibition mechanism. The audit also
confirms that the prior Hanson 2019 / de Rosenroll 2026 ports use NMDA-driven rather than spatial
GABA mechanisms, so there is no library-imported precedent for centripetal gating in the project.

### Reuse the Per-Synapse Activation-Time Histogram Plotter, Add a New Polar-Active-Fraction Plotter

[t0052]:`render_figures.py:181-195` already produces per-direction synapse-activation-time
histograms. That plotter can be reused unchanged for t0053 (every E synapse always fires; only the I
synapses are gated, but the activation-time CSV in [t0052] writes onset times for **all** 100
synapses without per-synapse fired/not-fired info). For t0053 the activation-time CSV should be
extended to include an `is_fired` boolean column per (angle, synapse) so the histogram-renderer can
distinguish E from I and show the active subset. The new polar plot (active fraction vs direction)
is ~25 lines of new matplotlib code wrapping `plot_polar_tuning_curve`-style code or, more simply, a
custom `subplot_kw=dict(projection="polar")` chart drawn from the `active_fraction_per_direction`
dict.

### CSV / JSON Schemas Carry Over Verbatim

[t0052] emits these schemas: tuning curve `(angle_deg, trial_seed, firing_rate_hz)` per mode; spike
times `(angle_deg, trial_index, spike_time_s)` per mode; voltage traces
`(angle_deg, trial_seed, sample_idx, t_ms, voltage_mv)` per mode; activation times
`(angle_deg, synapse_index, onset_time_ms)`. t0053 keeps all four. The activation-times CSV gains a
fifth column `is_fired` (0 or 1, per direction per synapse) for the I synapses; E synapses are
always 1.

### Placement Seed Identity Is Critical

Per the task description ("Synapse placement uses the same fixed seed (0) as t0052") and the
verification criteria ("the two tasks can be compared trial-for-trial in a downstream analysis"),
t0053's `PLACEMENT_SEED = 0` constant and `sample_dendritic_locations(cell, n_pairs=100, seed=0)`
call must produce a `Location` list bit-identical to [t0052]'s. The `sample_dendritic_locations`
function in [t0052]:`placement.py:29-80` uses `np.random.default_rng(seed)` and operates only on the
dendrite list returned by `build_dsgc_from_swc`, so as long as the cell builder is copied verbatim
(same iteration order, same soma collapse) the placement is identical by construction. Add a smoke
test that loads `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` and compares it
against t0053's `RESULTS_DIR/placement_seed0.json` field-by-field.

### Trial Modes Stay But the Trial Runner Changes

[t0052] runs three modes: FULL (E + I), AMPA_ONLY (zero GABA NetCons), GABA_ONLY (zero AMPA
NetCons). t0053 keeps the same three. In FULL mode a per-trial gating pass picks which I synapses
fire; in AMPA_ONLY mode every I synapse is silenced regardless of gating; in GABA_ONLY mode the I
synapses follow the gating rule (so the IPSP per-direction observable reflects the spatial
mechanism) and every E synapse is silenced. The dry-run gate ([t0052]:`run_tuning_curve.py:269-323`)
remains essentially the same: AMPA_ONLY at theta=0 must produce non-zero spikes; FULL at theta=0
must be at least 80% of AMPA_ONLY. Add a second dry-run check: in GABA_ONLY at theta=0 the active
I-synapse fraction must be approximately 0.5 +/- 0.2.

### Test Strategy: Reuse Quiescent-Rest, Replace gaba_mod Test

[t0052]:`test_quiescent_rest.py` (104 lines) validates `V_rest = -65 +/- 0.5 mV` with no synapses
attached; copy verbatim. [t0052]:`test_gaba_mod.py` (22 lines) tests the scalar `gaba_mod(0)=0.33`
and `gaba_mod(180)=0.99`; replace with a unit test for the spatial gate that asserts: (a)
`cos(0 - 0) >= 0` -> not fired (a synapse with `theta_centrifugal_i = 0` and stimulus
`theta_stim = 0` has bar moving away from soma along the synapse's centrifugal direction, so gating
condition `cos(theta_stim - theta_centrifugal) < 0` is False, synapse is silent); (b)
`cos(180 - 0) < 0` -> fired (stimulus 180 deg, centrifugal 0 deg -> `cos(180) = -1 < 0`, gated on);
(c) edge case `cos(90 - 0) = 0` -> by strict inequality, not fired. Add a third test that places 100
synapses uniformly at random angles around the soma and confirms the active fraction is
approximately 0.5 +/- 0.05 for any single test direction.

## Reusable Code and Assets

### Import via library

* **Source**: `tasks.t0011_response_visualization_library.code.tuning_curve_viz` (registered library
  `tuning_curve_viz`)

* **What it does**: Cartesian + polar tuning-curve plots, multi-model overlay, per-angle raster +
  PSTH

* **Reuse method**: **import via library**

* **Key entry points**:
  * `plot_cartesian_tuning_curve(curve_csv: Path, out_png: Path, *, target_csv: Path | None) -> None`
  * `plot_polar_tuning_curve(curve_csv: Path, out_png: Path, *, target_csv: Path | None) -> None`
  * `plot_angle_raster_psth(spike_times_csv: Path, out_png_pattern: str, *, angles_deg: list[float]) -> None`

* **Adaptation needed**: emit CSVs in canonical schemas (same as [t0052]); none of these plotters
  need the spatial gating change.

* **Line count**: zero (library import only)

* **Source**: `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` (registered
  library `tuning_curve_loss`)

* **What it does**: DSI / peak / null / HWHM / reliability / weighted scalar loss + RMSE against
  t0004 target

* **Reuse method**: **import via library**

* **Key entry points**:
  * `compute_dsi(*, curve: TuningCurve) -> float`
  * `compute_peak_hz(*, curve: TuningCurve) -> float`
  * `compute_null_hz(*, curve: TuningCurve) -> float`
  * `compute_hwhm_deg(*, curve: TuningCurve) -> float`
  * `compute_reliability(*, curve: TuningCurve) -> float | None`
  * `load_tuning_curve(csv_path: Path) -> TuningCurve`

* **Adaptation needed**: none — t0053's tuning-curve CSV uses the same schema as [t0052]'s.

* **Line count**: zero (library import) + 44 lines vector-sum DSI / preferred-direction (copied from
  [t0052]:`metrics_extra.py`)

### Copy into task

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/swc_io.py:1-180`

* **What it does**: SWC parser, structural validator, summary, children index — pure-stdlib

* **Reuse method**: **copy into task** -> `tasks/t0053_minimal_dsgc_spatial_gaba/code/swc_io.py`

* **Function signatures**:
  * `parse_swc_file(*, swc_path: Path) -> list[SwcCompartment]`
  * `validate_structure(*, compartments: list[SwcCompartment]) -> None`
  * `summarize(*, compartments: list[SwcCompartment]) -> SwcSummary`
  * `build_children_index(*, compartments: list[SwcCompartment]) -> dict[int, list[int]]`

* **Adaptation needed**: none beyond updating the file-header docstring's copy-attribution to cite
  [t0052] (which itself cites [t0009]).

* **Line count**: 180 verbatim

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/neuron_bootstrap.py:1-82`

* **What it does**: Windows NEURONHOME bootstrap with sentinel env-var re-exec guard

* **Reuse method**: **copy into task** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/neuron_bootstrap.py`

* **Function signatures**:
  * `ensure_neuron_importable() -> None`
  * `load_stdrun() -> None`
  * `enable_cvode() -> None`

* **Adaptation needed**: rename the sentinel constant `NEURONHOME_SENTINEL_ENV` from
  `_T0052_NEURONHOME_BOOTSTRAPPED` to `_T0053_NEURONHOME_BOOTSTRAPPED` in `constants.py`; rewrite
  `tasks.t0052_minimal_dsgc_scalar_gaba.code.{constants, paths}` imports to point at t0053.

* **Line count**: 82 verbatim

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/cell.py:1-215`

* **What it does**: SWC -> NEURON cell builder, soma collapse, synthetic AIS, dendrite section list,
  midpoint xyz capture

* **Reuse method**: **copy into task** -> `tasks/t0053_minimal_dsgc_spatial_gaba/code/cell.py`

* **Function signatures**:
  * `build_dsgc_from_swc(*, swc_path: Path) -> CellHandles`
  * `summarize_cell(*, cell: CellHandles) -> CellBuildSummary`

* **Adaptation needed**: extend `CellHandles` with `soma_origin_um: tuple[float, float, float]`
  populated from `(soma_origin.x, soma_origin.y, soma_origin.z)` so the spatial-driver can compute
  `theta_centrifugal_i`. Rewrite `tasks.t0052_minimal_dsgc_scalar_gaba.code.{constants, swc_io}`
  imports.

* **Line count**: 215 with ~5-10 lines added for `soma_origin_um`

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/placement.py:1-87`

* **What it does**: length-weighted random placement of 100 synapse pair locations with seed-0 RNG
  + JSON dump

* **Reuse method**: **copy into task** -> `tasks/t0053_minimal_dsgc_spatial_gaba/code/placement.py`

* **Function signatures**:
  * `sample_dendritic_locations(*, cell: CellHandles, n_pairs: int, seed: int) -> list[Location]`
  * `save_placement_json(*, locations: list[Location], out_path: Path) -> None`

* **Adaptation needed**: rewrite `tasks.t0052_minimal_dsgc_scalar_gaba.code.cell` imports. Function
  logic unchanged — seed-0 placement must remain bit-identical to [t0052].

* **Line count**: 87 verbatim modulo the import path rewrite

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/synapses.py:1-181`

* **What it does**: `EiPair` dataclass, `build_ei_pairs`, `_onset_time_ms`, `schedule_ei_onsets`,
  `gaba_mod` (scalar)

* **Reuse method**: **copy into task with major rewrite** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/synapses.py`

* **Function signatures (after rewrite)**:
  * `build_ei_pairs(*, h: Any, locations: list[Location], sections: list[Any], soma_origin_um: tuple[float, float, float]) -> list[EiPair]`
    — extended signature; precomputes and stores `theta_centrifugal_i` per pair.
  * `schedule_ei_onsets(*, pairs: list[EiPair], angle_deg: float, velocity_um_per_ms: float) -> ScheduleResult`
    — new return dataclass
    `ScheduleResult(onset_times_ms: list[float], i_fired_mask: list[bool])`. Drops the
    `gaba_mod_theta` parameter.
  * `i_synapse_fires(*, theta_stim_deg: float, theta_centrifugal_deg: float) -> bool` — new
    function: returns `cos(radians(theta_stim - theta_centrifugal)) < 0`.

* **Adaptation needed**: (a) extend `EiPair` with `theta_centrifugal_rad: float`; (b) compute
  `theta_centrifugal_rad = atan2(y_um - soma_y, x_um - soma_x)` at build time; (c) replace the
  scalar `gaba_mod()` function with `i_synapse_fires()` (cosine half-plane test); (d) in
  `schedule_ei_onsets`, set per-synapse `gaba_netcon.weight[0]` to either `GABA_BASE_NS * 1e-3`
  (full amplitude when fired) or `0.0` (when gated off). Optionally also set
  `gaba_netstim.start = TSTOP_MS + 1.0` for gated-off synapses for defence-in-depth.

* **Line count**: ~190 lines after rewrite (similar in size to [t0052]'s 181)

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/trial.py:1-140`

* **What it does**: single-trial NEURON runner — schedules onsets, applies mode-specific weight
  overrides, finitialize+continuerun, returns
  `TrialResult(t_ms, v_soma_mv, spike_times_ms, synapse_onset_times_ms, firing_rate_hz, gaba_mod_theta)`

* **Reuse method**: **copy into task with minor rewrite** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/trial.py`

* **Function signatures (after rewrite)**:
  * `run_one_trial(*, h, cell, pairs, mode: TrialMode, angle_deg: float, trial_seed: int) -> TrialResult`
    — same signature; internal logic now drives the spatial gate via `schedule_ei_onsets`.

* **Adaptation needed**: drop the `gaba_mod_theta` field from `TrialResult`; add
  `i_fired_mask: list[bool]` and `i_active_fraction: float` (sum(mask) / len(mask)) so the per-trial
  gate result is captured. Update `_apply_mode_weights` for AMPA_ONLY: every I synapse zeroed
  regardless of mask. For GABA_ONLY: every E synapse zeroed; I weights follow the mask.

* **Line count**: ~140 lines (unchanged, with field swap)

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/run_tuning_curve.py:1-390`

* **What it does**: 12 directions x 10 trials x 3 modes sweep harness with dry-run validation gate
  and per-mode CSV writers (tuning, spikes, voltage), plus activation-times CSV

* **Reuse method**: **copy into task with rewrite** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/run_tuning_curve.py`

* **Function signatures**:
  * `run_full_sweep(*, voltage_sample_stride: int = 8) -> None`
  * `setup_sweep_artifacts() -> SweepArtifacts`

* **Adaptation needed**: (a) extend the activation-times CSV writer to include `is_fired` column;
  (b) at sweep time, accumulate per-direction active-fraction averages and write a new
  `active_fraction_per_direction.csv` with columns `(angle_deg, active_fraction)`; (c) extend the
  dry-run gate with the I-synapse active-fraction sanity check at theta=0; (d) drop `gaba_mod_theta`
  references everywhere; (e) rewrite all `tasks.t0052_*` imports.

* **Line count**: ~400 lines after additions

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/render_figures.py:1-231`

* **What it does**: per-direction soma V, EPSP, IPSP, PSTH, activation histogram + polar/Cartesian
  tuning curves via t0011

* **Reuse method**: **copy into task with addition** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/render_figures.py`

* **Function signatures**:
  * `render_soma_voltage_per_direction(*, out_dir: Path) -> None`
  * `render_aggregate_epsp(*, out_dir: Path) -> None`
  * `render_aggregate_ipsp(*, out_dir: Path) -> None`
  * `render_psth(*, out_dir: Path) -> None`
  * `render_activation_histogram(*, out_dir: Path) -> None`
  * `render_tuning_curves(*, out_dir: Path) -> None`
  * NEW: `render_active_fraction_polar(*, out_dir: Path) -> None`

* **Adaptation needed**: add `render_active_fraction_polar` (~25 lines, polar matplotlib chart of
  fraction vs direction); reuse the activation-histogram renderer with one additional facet showing
  only `is_fired==1` rows.

* **Line count**: ~260 lines after addition

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/compute_metrics.py:1-304`

* **What it does**: per-mode metrics, multi-variant `metrics.json`, IPSP-conductance hard gate

* **Reuse method**: **copy into task with rewrite** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/compute_metrics.py`

* **Function signatures**:
  * `main() -> int`
  * `_build_full_variant`, `_build_ampa_variant`, `_build_gaba_variant`
  * `_peak_depolarization_per_angle`, `_compute_rmse_against_target`

* **Adaptation needed**: replace the IPSP-conductance hard gate (`gaba_mod(180)/gaba_mod(0)`) with a
  soft warning on the active-fraction average across directions (expected ~0.5 +/- 0.2 ; print
  per-direction values, no `assert`). Add `active_fraction_per_direction` to the
  `derived_quantities.json` output. Drop `from ...synapses import gaba_mod`.

* **Line count**: ~280 lines after rewrite

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/metrics_extra.py:1-44`

* **What it does**: vector-sum DSI + preferred-direction angle from a `TuningCurve`

* **Reuse method**: **copy into task** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/metrics_extra.py`

* **Function signatures**:
  * `compute_vector_sum_dsi(*, curve: TuningCurve) -> float`
  * `compute_preferred_direction_deg(*, curve: TuningCurve) -> float`

* **Adaptation needed**: none; copy verbatim.

* **Line count**: 44 verbatim

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/constants.py:1-125`

* **What it does**: simulation timing, bar geometry, passive cable parameters, AIS HH overrides,
  AMPA/GABA Exp2Syn parameters, gabaMOD direction tuning, metric registry keys, CSV column names,
  `TrialMode` enum

* **Reuse method**: **copy into task with deletion** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/constants.py`

* **Adaptation needed**: drop the gabaMOD direction tuning block (`THETA_ND_DEG`, `GABAMOD_PD`,
  `GABAMOD_ND` constants) since the spatial mechanism has no scalar endpoints. Rename
  `NEURONHOME_SENTINEL_ENV` to `_T0053_NEURONHOME_BOOTSTRAPPED`. All other constants unchanged
  (timing, bar geometry, passive parameters, AIS overrides, synapse kinetics, placement seed=0).

* **Line count**: ~115 lines after deletion

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/paths.py:1-78`

* **What it does**: centralised path constants — task root, results, images, library asset, SWC
  source, target tuning curve, NEURONHOME, all CSV outputs, placement JSON, metrics JSON

* **Reuse method**: **copy into task with rename** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/paths.py`

* **Adaptation needed**: change `TASK_ID = "t0053_minimal_dsgc_spatial_gaba"` and
  `LIBRARY_ID = "minimal_dsgc_spatial_gaba"`. Add a new path constant
  `ACTIVE_FRACTION_CSV: Path = RESULTS_DIR / "active_fraction_per_direction.csv"`.

* **Line count**: ~80 lines after addition

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/test_quiescent_rest.py:1-104`

* **What it does**: validation gate for `V_rest = -65 +/- 0.5 mV` after 200 ms passive run with no
  synapses

* **Reuse method**: **copy into task** ->
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_quiescent_rest.py`

* **Adaptation needed**: rewrite imports; logic unchanged.

* **Line count**: 104 verbatim modulo imports

* **Source**: `tasks/t0052_minimal_dsgc_scalar_gaba/code/test_gaba_mod.py:1-22`

* **What it does**: tests scalar `gaba_mod(0)=0.33`, `gaba_mod(180)=0.99`

* **Reuse method**: **REPLACE — drop and write new** -> create
  `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_spatial_gating.py`

* **What the new test does**: validates the cosine half-plane firing gate at three known angles
  (PD-side: not fired, ND-side: fired, exact perpendicular: not fired by strict inequality), plus a
  uniform-random-angle sample test that confirms the active fraction is approximately 0.5 +/- 0.05
  for a sample direction.

* **Line count**: ~50 lines new

### Asset reuse

* **Source dataset**: `dsgc-baseline-morphology-calibrated` from [t0009] at
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`

* **What it provides**: 6,736-compartment SWC, four-tier diameter taper, 1,536.25 um total dendritic
  length

* **Reuse method**: **read SWC file directly** (path resolved through t0053's own `paths.py`)

* **Adaptation needed**: none.

* **Source dataset (optional)**: `target-tuning-curve` from [t0004] at
  `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`

* **What it provides**: 12-direction canonical target tuning curve for RMSE comparison

* **Reuse method**: **read CSV file directly** if present (compute_metrics tolerates absence)

* **Adaptation needed**: none.

* **Sibling reference output**: `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json`

* **What it provides**: a ground-truth placement file generated by the seed-0 RNG on the same
  morphology

* **Reuse method**: **read JSON for unit-test diff** in `test_placement_seed0_match.py` (new
  optional sanity check)

* **Adaptation needed**: none.

## Dataset Landscape

Only two project datasets are relevant to t0053. (1) `dsgc-baseline-morphology-calibrated` from
[t0009] is the morphology substrate. (2) `target-tuning-curve` from [t0004] provides the
12-direction Cartesian target curve (`(angle_deg, firing_rate_hz)` mean) used for RMSE comparison in
`compute_metrics.py`. The non-calibrated `dsgc-baseline-morphology` from [t0005] is superseded and
must not be consumed (placeholder 0.125 um radii). No new datasets are produced or required by
t0053; the placement JSON (`placement_seed0.json`) is a results artefact, not an asset.

## Common Patterns

### Cross-Task Code Reuse via Copy

Per the project rule, only registered library assets can be imported across tasks. [t0052]'s
`minimal_dsgc_scalar_gaba` library is registered but the import path it exposes is not the `code/`
directory — it lists its module paths but other tasks must still copy files for any
non-`tuning_curve_viz` / `tuning_curve_loss` consumption. Every NEURON-using task in the project
([t0008], [t0020], [t0022], [t0024], [t0046], [t0052]) follows the same module-organisation pattern:
`cell.py`, `synapses.py`, `trial.py`, `run_tuning_curve.py`, `render_figures.py`,
`compute_metrics.py`, `metrics_extra.py`, `constants.py`, `paths.py`, `swc_io.py` (or HOC source),
`neuron_bootstrap.py`. t0053 inherits this layout from [t0052].

### Single Source of Truth for Numerical Constants

[t0052]:`constants.py` is the canonical example of the project's "no magic numbers" rule applied to
NEURON simulations: every timing parameter, geometry parameter, kinetic parameter, and AIS override
lives in one file with a documented rationale (the `AIS_GNABAR_S_PER_CM2 = 1.2` boost, for example,
has a 5-line comment explaining why the default 0.12 fails to fire). t0053 inherits this discipline;
the only constants change is the deletion of the gabaMOD endpoints.

### Multi-Variant `metrics.json`

The project's metrics specification supports both the legacy flat format and the explicit
multi-variant format. [t0052] uses the multi-variant format for FULL / AMPA_ONLY / GABA_ONLY; t0053
keeps the same three variants. Each variant gets primary DSI, vector-sum DSI, preferred direction,
peak Hz, null Hz; the shared sweep produces `derived_quantities.json` for non-registered scalars
(peak / null Hz absolutes, IPSP component magnitudes, and the new `active_fraction_per_direction`
dict).

## Lessons Learned

* **[t0052]'s primary DSI = 1.0 hard-step is a useful comparison anchor.** [t0052] reports primary
  DSI = 1.0 at peak 0.667 Hz / null 0 Hz (single-spike-per-trial deterministic firing). The
  vector-sum DSI was 0.746 because preferred-side angles fire equally. t0053's spatial gating
  removes the graded-conductance smoothness — every synapse is full-on or fully silent — so a
  similar binary-spiking failure mode is even more likely. Include vector-sum DSI and HWHM in
  `metrics.json` for early detection.

* **Driving-force saturation matters under heavy synaptic crowding.** [t0052] reported a conductance
  ratio gNULL/gPD = 3.0 (exact) but the somatic IPSP voltage ratio was only 1.54 because once Vm
  approaches E_GABA = -75 mV the per-synapse driving force collapses. t0053 will see an even sharper
  driving-force ceiling because the active subset of I synapses fires at full 2 nS amplitude (vs the
  0.66 nS scaled value at PD in [t0052]). Plan for the IPSP somatic deflection to be substantially
  larger than [t0052]'s; this does not invalidate the result but changes the scaling expectation.

* **Per-synapse activation-time histograms catch position-gating bugs.** [t0052]:Lessons-Learned
  identifies this as a cheap sanity check: for a leftward bar, activation times must decrease with
  synapse x-coordinate. t0053 should keep the histogram and add the per-synapse `is_fired` flag so a
  bug in the cosine half-plane test surfaces visually.

* **The seed-0 placement requirement is a load-bearing test gate.** Both [t0052]'s placement and
  t0053's placement must produce the same `Location` list for trial-for-trial cross-task comparison.
  Add a smoke test that diff-checks
  `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` against t0053's. Failure to
  reproduce identical placement means the cell builder iteration order has drifted.

* **Don't reintroduce HOC dependencies.** [t0046]'s reproduction wave demonstrated extensive HOC
  globals (`gabaMOD`, `b2gnmda`, etc.) that interact unpredictably with Python state. [t0052]
  cleanly avoided HOC entirely (only `Exp2Syn`, `hh`, `pas` built-ins). t0053 does the same — no
  MOD compilation, no HOC procs, no `apply_params` calls.

* **The dry-run gate is cheap and catches catastrophic failures early.**
  [t0052]:`run_tuning_curve.py` spends ~30 seconds on the 1-angle-x-2-trial dry-run before launching
  the 360-trial sweep, and refuses to proceed if AMPA_ONLY at theta=0 produces zero spikes. Keep
  this; add an active- fraction sanity check (~0.5 +/- 0.2) to the dry-run.

* **The polar plot library does not currently render arbitrary scalar-vs-direction data.**
  [t0011]:`tuning_curve_viz.polar.plot_polar_tuning_curve` expects a tuning-curve CSV with
  `firing_rate_hz`. t0053's new active-fraction polar chart cannot reuse this entry point; write a
  small ~25-line `render_active_fraction_polar` in `render_figures.py` using
  `subplot_kw=dict(projection="polar")` and a fraction-axis label.

## Recommendations for This Task

1. **Adopt [t0052]'s layout wholesale.** Copy 14 of the 15 files from
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/` into `tasks/t0053_minimal_dsgc_spatial_gaba/code/`,
   rewrite all `tasks.t0052_minimal_dsgc_scalar_gaba.code.*` imports to
   `tasks.t0053_minimal_dsgc_spatial_gaba.code.*`, rename
   `NEURONHOME_SENTINEL_ENV = "_T0052_NEURONHOME_BOOTSTRAPPED"` ->
   `"_T0053_NEURONHOME_BOOTSTRAPPED"`, change `TASK_ID`/`LIBRARY_ID` constants in `paths.py`. Delete
   `test_gaba_mod.py` and the gabaMOD constants block in `constants.py`.

2. **Rewrite `synapses.py` for spatial gating.** Replace the scalar `gaba_mod` function with
   `i_synapse_fires(theta_stim_deg, theta_centrifugal_deg)` returning
   `cos(radians(theta_stim - theta_centrifugal)) < 0`. Extend `EiPair` with
   `theta_centrifugal_rad: float`. In `build_ei_pairs` add a `soma_origin_um` parameter and
   precompute `theta_centrifugal_rad = atan2(y_um - soma_y, x_um - soma_x)`. Rewrite
   `schedule_ei_onsets` to set `gaba_netcon.weight[0]` to `GABA_BASE_NS * 1e-3` (full amplitude)
   when the synapse fires and `0.0` otherwise; return a `ScheduleResult` carrying the per-synapse
   `i_fired_mask` for downstream metrics.

3. **Extend `cell.py:CellHandles`** with `soma_origin_um: tuple[float, float, float]` populated from
   `soma_origin = soma_compartments[0]` so the spatial driver can compute centrifugal directions.

4. **Update `trial.py`** to drop `gaba_mod_theta` from `TrialResult` and add
   `i_fired_mask: list[bool]` and `i_active_fraction: float`. Mode-specific weight overrides remain
   for AMPA_ONLY / GABA_ONLY.

5. **Update `run_tuning_curve.py`** to (a) write the new active-fraction CSV per direction, (b)
   extend the activation-times CSV with an `is_fired` column for I synapses, (c) add an
   active-fraction dry-run sanity check at theta=0.

6. **Update `compute_metrics.py`** to drop the IPSP-conductance hard gate (no scalar gabaMOD
   exists), replace it with a per-direction active-fraction print and a soft sanity warning if the
   across-direction mean falls outside `[0.4, 0.6]`. Add `active_fraction_per_direction` (12
   entries) to `derived_quantities.json`.

7. **Update `render_figures.py`** to add `render_active_fraction_polar(out_dir)` (~25 lines new
   matplotlib polar chart). Optionally split the per-direction synapse activation histogram into E
   vs gated-I subsets so the spatial-gating mechanism is visually verifiable.

8. **Replace `test_gaba_mod.py` with `test_spatial_gating.py`** validating the cosine half-plane
   firing rule on three known angles plus the uniform-random-angle ~0.5 active-fraction sanity.

9. **Add `test_placement_seed0_match.py` (optional but cheap)** to diff the t0053 placement against
   `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` — this enforces the
   trial-for-trial comparison criterion in the task description.

10. **Import `tuning_curve_viz` and `tuning_curve_loss`** as in [t0052]; do not reimplement DSI /
    polar rendering.

11. **Keep the multi-variant `metrics.json` structure** with FULL / AMPA_ONLY / GABA_ONLY variants
    (same as [t0052]); the task description's verification criteria expect primary DSI, vector-sum
    DSI, preferred direction, peak Hz, null Hz at minimum.

12. **Add the new REQ-7 figure** (polar plot of active fraction vs direction) to
    `results/images/active_fraction_polar.png` and embed it in `results_detailed.md`.

## Task Index

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate canonical target angle-to-AP-rate tuning curve
* **Status**: completed
* **Relevance**: Defines the canonical CSV schema `(angle_deg, trial_seed, firing_rate_hz)` and
  provides the optional 12-direction target curve for RMSE comparison in `compute_metrics.py`.

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download candidate DSGC morphology
* **Status**: completed
* **Relevance**: Originator of the `dsgc-baseline-morphology` SWC; superseded by [t0009]'s
  diameter-calibrated variant. Cited only as a reminder that t0053 must consume the calibrated
  variant, not the placeholder-radius variant.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Originator of the HOC-driven cell builder. Not directly reused; cited as part of
  the lineage that t0046 / t0022 / t0052 inherited and that t0053 explicitly avoids.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: completed
* **Relevance**: Direct dependency. Produces the `dsgc-baseline-morphology-calibrated` SWC consumed
  by t0053 (the same morphology used by [t0052]).

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: completed
* **Relevance**: Direct dependency. Library `tuning_curve_viz` provides per-angle Cartesian / polar
  / raster + PSTH plotters used by t0053 for output rendering.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Direct dependency. Library `tuning_curve_loss` provides DSI / peak / null / HWHM /
  reliability / RMSE for t0053 metrics computation.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Pattern reference for HOC-driven scalar gabaMOD that [t0052] reimplemented in pure
  Python; cited to flag that t0053's spatial mechanism is structurally different (per-synapse
  boolean firing rather than per-synapse scalar amplitude).

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially-asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: Earlier attempt at spatial inhibition asymmetry on the deposited HOC port. The
  t0022 mechanism was a half-plane preferred/null GABA conductance switch (per-pair, not per-event);
  [t0052] inherited the EiPair / NetStim / NetCon scaffolding from this task. Cited as the pattern
  source for position-gated bar-arrival timing.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Provides the `de_rosenroll_2026_dsgc` library with HOC-template-based cell
  construction and AR(2) NMDA-noise machinery. Not a t0053 reuse target (different cell, different
  mechanism); cited only to flag that this library exists and is **not** consumed by t0053.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit
* **Status**: completed
* **Relevance**: Originator of the NEURON-on-Windows bootstrap pattern that [t0052] inherited. Cited
  to anchor the bootstrap-and-recording-skeleton lineage.

### [t0050]

* **Task ID**: `t0050_audit_syn_distribution`
* **Name**: Audit deposited GABA/NMDA/AMPA synapse spatial distribution vs paper
* **Status**: completed
* **Relevance**: Provides the `synapse-distribution-audit-deposited-vs-paper` answer asset
  confirming that the deposited DSGC's `gabaMOD` is non-spatial and that the project has no prior
  implementation of true spatial-asymmetry inhibition. This justifies t0053's novel contribution.

### [t0052]

* **Task ID**: `t0052_minimal_dsgc_scalar_gaba`
* **Name**: Minimal from-scratch DSGC with scalar gabaMOD inhibition
* **Status**: completed
* **Relevance**: Sibling task and primary code source. Provides 14 of the 15 modules t0053 needs via
  copy-into-task. Library asset `minimal_dsgc_scalar_gaba` is the structural template; t0053's
  `minimal_dsgc_spatial_gaba` library is its inhibition-driver-swapped twin.
