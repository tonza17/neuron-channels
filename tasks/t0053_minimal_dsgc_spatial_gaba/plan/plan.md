---
spec_version: "2"
task_id: "t0053_minimal_dsgc_spatial_gaba"
date_completed: "2026-04-25"
status: "complete"
---
# Plan: Minimal From-Scratch DSGC with Spatial PD/ND-Asymmetric Inhibition

## Objective

Build a minimal compartmental DSGC model from scratch on the project's calibrated baseline
morphology, where direction-dependent inhibition is implemented as a per-synapse spatial firing
gate: each I synapse fires only when the moving stimulus has a centripetal component
(`cos(theta_stim - theta_centrifugal_i) < 0`); when fired, the synapse delivers full 2 nS GABA
amplitude with no scalar scaling. The model uses only NEURON built-in mechanisms (`hh`, `pas`,
`Exp2Syn`) — no MOD compilation. The task runs a 12-direction by 10-trial moving-bar sweep across
three trial modes (FULL, AMPA_ONLY, GABA_ONLY = 360 trials total) on local CPU. It is the
spatial-asymmetry sibling of t0052; placement seed 0 is identical so a downstream task can compare
trial-for-trial. The task produces one library asset, `minimal_dsgc_spatial_gaba`, plus
per-direction soma V(t), aggregate EPSP, aggregate IPSP, PSTH, polar tuning curve, per-synapse
activation histograms, and a new active-fraction polar plot. Done means: library asset validates,
all 12 direction figures exist for each output class, `metrics.json` contains primary DSI /
vector-sum DSI / preferred direction / peak Hz / null Hz, the active-fraction polar plot is rendered
and embedded, and the soft sanity check (mean active fraction ~0.5 +/- 0.2 across directions) is
recorded.

## Task Requirement Checklist

The operative task request from `task_description.md`:

> Build a minimal compartmental DSGC model with the following specification, then report
> per-direction voltage and firing-rate data so the behaviour can be compared against the project's
> target tuning curve and against t0052. Morphology: `dsgc-baseline-morphology-calibrated`. `soma`
> and `axon_initial_segment` get standard NEURON `hh`; all dendritic sections passive (Rm=5999,
> Ra=100, cm=1, V_rest=-65). 100 E + 100 I co-located synapses; uniform random placement on the
> dendritic length with the same fixed seed (0) as t0052. Excitatory: `Exp2Syn` (rise 0.5 ms, decay
> 2.5 ms, e=0 mV, peak 0.5 nS), one event per synapse per trial when the bar leading edge crosses
> the synapse position. Inhibitory: `Exp2Syn` (rise 1 ms, decay 20 ms, e=-75 mV, peak 2 nS, no
> scaling). For each I synapse, define `theta_centrifugal_i = atan2(y_i - y_soma, x_i - x_soma)`.
> Synapse i fires only when `cos(theta_stim - theta_centrifugal_i) < 0`; otherwise silent. Stimulus:
> 12 directions (0..330 step 30 deg), bar 200 um wide x arena length, speed 1000 um/s, 1500 ms per
> trial, 10 trials per direction, three modes (FULL / AMPA_ONLY / GABA_ONLY), 360 trials total.
> Outputs per direction: soma V(t) mean+/-SD, aggregate EPSP, aggregate IPSP, PSTH (5 ms bins),
> polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction), per-synapse
> activation-time histogram, and a new polar plot of "fraction of I synapses active vs direction".
> Library asset `minimal_dsgc_spatial_gaba` containing cell builder, synapse placer, excitation
> driver, inhibition driver (centripetal-gating), trial runner, recording helpers. Local CPU only,
> $0. Verification: library structure validates; 12 PNG plots in `results/images/` for each output
> class embedded in `results_detailed.md`; `metrics.json` contains DSI, vector-sum DSI, preferred
> direction, peak Hz, null Hz; active-fraction polar plot exists; placement uses fixed seed 0
> matching t0052.

Each requirement below has a stable ID used by the Step by Step section and the results step.

* `REQ-1` Morphology: load the t0009 calibrated SWC
  (`dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`) and build a
  pure-Python NEURON cell with explicit soma / dendrite / AIS tagging, plus the soma origin (x_soma,
  y_soma, z_soma) exposed for the spatial driver. Evidence: cell-build log prints section count,
  total dendritic length matching the t0009 summary (1,536.25 um), and the soma origin triple.
  Satisfied by Step 4.

* `REQ-2` Channels: `hh` inserted only on `soma` and `axon_initial_segment`; all dendrite sections
  passive with `Rm=5999`, `Ra=100`, `cm=1.0`; `V_rest=-65 mV`; cell silent at rest. Evidence: a 50
  ms quiescent run reaches steady-state -65 mV +/- 0.5 mV. Satisfied by Step 4 + Step 5.

* `REQ-3` Synapse placement: 100 E + 100 I co-located pairs uniformly over total dendritic length,
  fixed seed = 0 (identical to t0052), no soma/AIS placement. Evidence: location list logged with
  seed and saved to `results/placement_seed0.json`; total count is exactly 100 pairs; the saved
  placement is bit-identical to `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json`
  field-by-field. Satisfied by Step 6.

* `REQ-4` Excitatory mechanism: `Exp2Syn` rise=0.5 ms, decay=2.5 ms, e=0 mV, peak g=0.5 nS, one
  event per synapse per trial. Evidence: `Exp2Syn.tau1`, `tau2`, `e` and `NetCon.weight[0]` printed
  in setup log. Satisfied by Step 7.

* `REQ-5` Inhibitory mechanism: `Exp2Syn` rise=1 ms, decay=20 ms, e=-75 mV, peak g=2 nS (full
  amplitude when fired, zero otherwise; no scalar scaling). Evidence: `Exp2Syn.tau1`, `tau2`, `e`
  and per-trial `gaba_netcon.weight[0]` printed at setup; the per-synapse weight is either
  `GABA_BASE_NS * 1e-3` or exactly `0.0`. Satisfied by Step 7.

* `REQ-6` Position-gated firing: each E synapse fires once per trial when the bar leading edge
  crosses its (x, y) projected onto the bar's normal, no E/I offset. Evidence: per-synapse
  activation-time histogram (Output 6) shows monotonic relationship between synapse coordinate and
  onset time. Satisfied by Step 7 + Step 12.

* `REQ-7` Spatial centripetal-gating rule: for each I synapse i,
  `theta_centrifugal_i = atan2(y_i - y_soma, x_i - x_soma)`; the synapse fires at the bar-arrival
  time only when `cos(radians(theta_stim - theta_centrifugal_i)) < 0`, otherwise the I synapse is
  silent (weight = 0). Full 2 nS amplitude when fired (no scalar scaling). Evidence:
  `i_synapse_fires(...)` unit test passes for the three diagnostic angles (PD-side: not fired,
  ND-side: fired, exact perpendicular: not fired); per-direction `is_fired` CSV column shows the
  expected ~50% active fraction averaged across uniform-random placement. Satisfied by Step 8 + Step
  11\.

* `REQ-8` Stimulus: 12 directions (0, 30, ..., 330 deg), bar 200 um x arena length, speed 1000 um/s,
  1500 ms per trial. Evidence: bar geometry constants in `constants.py`; sweep loop logs 12 angles.
  Satisfied by Step 7 + Step 11.

* `REQ-9` Trials: 10 trials per direction per mode (360 total across three modes) with deterministic
  seeds `1000 * angle_idx + trial_idx + 1`. Evidence: each per-mode CSV contains 120 rows; combined
  sweep CSV has 360 rows. Satisfied by Step 11.

* `REQ-10` Three trial modes: FULL (E+I with spatial gating), AMPA_ONLY (every I synapse silenced
  regardless of gate), GABA_ONLY (every E synapse silenced; I synapses follow the gate). Evidence:
  three independent per-mode CSV files in `results/`. Satisfied by Step 9 + Step 11.

* `REQ-11` Per-direction soma V(t) mean +/- SD across 10 FULL trials, 12 PNGs, embedded in
  `results_detailed.md`. Satisfied by Step 12.

* `REQ-12` Per-direction aggregate EPSP (AMPA_ONLY) and aggregate IPSP (GABA_ONLY) mean +/- SD, 12
  PNGs each. Satisfied by Step 12.

* `REQ-13` Per-direction firing-rate PSTH (5 ms bins) mean across 10 FULL trials, 12 PNGs. Satisfied
  by Step 12.

* `REQ-14` Polar tuning curve: peak firing rate (Hz) vs direction, primary DSI, vector-sum DSI,
  preferred direction. Satisfied by Step 12 (polar plot via `tuning_curve_viz`) + Step 13 (metrics).

* `REQ-15` Per-synapse activation-time histogram per direction (sanity check that E synapses on the
  leading edge fire first), 12 PNGs. The histogram CSV carries an `is_fired` column so the active
  subset of I synapses can be visualised. Satisfied by Step 12.

* `REQ-16` Library asset `minimal_dsgc_spatial_gaba` with: cell builder (with soma origin), synapse
  placer, AMPA driver, GABA driver (centripetal-gating), trial runner, recording helpers, renderer
  suite, metrics computation. Satisfied by Step 14.

* `REQ-17` `metrics.json` contains primary DSI, vector-sum DSI, preferred direction, peak Hz, null
  Hz at minimum, in explicit multi-variant format with FULL / AMPA_ONLY / GABA_ONLY variants.
  Satisfied by Step 13.

* `REQ-18` Soft sanity check on the active-fraction across directions: mean active fraction over 12
  directions should land in `[0.4, 0.6]`. The check is recorded as a per-direction list and as the
  cross-direction mean in `derived_quantities.json` and printed at run time; deviations are warned
  about (no hard `assert`) and explained as morphology asymmetry in the reporting step. Satisfied by
  Step 13.

* `REQ-19` All compute is local CPU; total cost $0. Satisfied by Step 15 (cost log).

* `REQ-20` Random seed for placement is fixed at 0 and reported in `results_detailed.md`. The
  placement JSON is bit-identical to t0052's, verified by an optional placement-diff smoke test.
  Satisfied by Step 6 + reporting orchestrator step.

* `REQ-21` New active-fraction polar plot (REQ-7 of the task spec): one PNG at
  `results/images/active_fraction_polar.png` showing the fraction of I synapses active vs direction.
  Embedded in `results_detailed.md` as the seventh output class. Satisfied by Step 12.

## Approach

The task is the spatial-asymmetry sibling of t0052. Per the project rule that only registered
library assets can be imported across tasks, the t0052 library `minimal_dsgc_scalar_gaba` cannot be
imported directly; instead, 14 of its 15 code modules are **copied verbatim** into
`tasks/t0053_minimal_dsgc_spatial_gaba/code/` with all `tasks.t0052_minimal_dsgc_scalar_gaba.code.*`
import paths rewritten to `tasks.t0053_minimal_dsgc_spatial_gaba.code.*`, and the NEURONHOME
sentinel env var renamed to `_T0053_NEURONHOME_BOOTSTRAPPED`. The 15th module — `synapses.py` —
is **rewritten** for spatial centripetal-gating; `cell.py` is **extended** by exposing the soma
origin; `compute_metrics.py` is **edited** to swap the IPSP-conductance hard gate for a soft
active-fraction sanity check; and `render_figures.py` is **extended** with a new
`render_active_fraction_polar`. The legacy `test_gaba_mod.py` is replaced by a new
`test_spatial_gating.py`.

The spatial gating rule. For each I synapse i, the centrifugal direction is
`theta_centrifugal_i = atan2(y_i - y_soma, x_i - x_soma)`, computed once at pair-construction time
from the cell's soma origin (the first SWC soma row) and the placement coordinates. Per trial, the
firing decision is `fires_i = cos(radians(theta_stim - theta_centrifugal_i)) < 0`. When `fires_i` is
True, `pair.gaba_netstim.start = bar_arrival_time_ms` and
`pair.gaba_netcon.weight[0] = GABA_BASE_NS * 1e-3` (full 2 nS). When False,
`pair.gaba_netcon.weight[0] = 0.0` (and as defence-in-depth
`pair.gaba_netstim.start = TSTOP_MS + 1.0` to push the event past the simulation end). The aggregate
effect is that for any given bar direction, only the half of I synapses whose centrifugal vectors
point into the bar-incoming hemisphere fire — inhibition is spatially concentrated on the side of
the dendritic field being approached "from the wrong end".

Trial modes carry over from t0052: FULL (E + spatial-gated I), AMPA_ONLY (every I synapse silenced
regardless of gate, every E fires), GABA_ONLY (every E synapse silenced; I synapses follow the gate,
so the IPSP per-direction observable reflects the spatial mechanism). Three independent CSV files
per mode are produced.

Output schemas. The four CSV schemas inherited from t0052 are kept verbatim:
`(angle_deg, trial_seed, firing_rate_hz)` per mode for the tuning curve;
`(angle_deg, trial_index, spike_time_s)` per mode for the spike rasters;
`(angle_deg, trial_seed, sample_idx, t_ms, voltage_mv)` per mode for soma voltage traces;
`(angle_deg, synapse_index, onset_time_ms)` for the activation histograms — extended with an
`is_fired` (0/1) column. A new `(angle_deg, active_fraction)` CSV captures the per-direction
fraction of I synapses fired in FULL mode for the new polar plot.

Plotting reuses `tuning_curve_viz.plot_polar_tuning_curve`, `plot_cartesian_tuning_curve`, and
`plot_angle_raster_psth` by import. Scalar metrics reuse
`tuning_curve_loss.compute_dsi/peak_hz/null_hz/hwhm_deg/compute_reliability` by import; vector-sum
DSI is provided by the copied `metrics_extra.py`. The new active-fraction polar plot is ~25 lines of
new matplotlib code in `render_figures.py` using `subplot_kw=dict(projection="polar")`.

The IPSP-conductance hard gate from t0052 (`gNULL/gPD ~= 3` between 2.7 and 3.3) does not apply
because the spatial mechanism has no scalar amplitude endpoints — every I synapse either fires at
full amplitude or is silent. The analytic prediction here is instead the **fraction of I synapses
active per direction**: with uniform-random seed-0 placement on a roughly symmetric dendritic field
this is approximately 50% across all directions, with deviations from 50% measuring the
dendritic-field asymmetry caused by the off-centre soma position. The plan replaces the hard
`2.7 <= ratio <= 3.3` assertion with a **soft** sanity check that the cross-direction mean active
fraction is within `[0.4, 0.6]`; deviations are printed and recorded but do not halt the task.

**Alternatives considered.**
* Implement the spatial gate inside a custom MOD file (a bespoke synapse mechanism that internally
  decides whether to fire). Rejected: forces a `nrnivmodl` step on Windows, drifts from t0052's
  pure-Python build, and complicates downstream comparison. The Python-side gating in
  `schedule_ei_onsets` is equivalent and simpler.
* Use a continuous spatial weighting (e.g., set
  `weight[0] = max(0, -cos(theta_stim - theta_centrifugal))`) rather than a strict boolean
  half-plane. Rejected: the task spec is explicit — strict inequality and full amplitude. A
  continuous weighting would also blur the comparison with t0052 (which uses scalar amplitude
  scaling) by smearing across mechanisms.
* Compute `theta_centrifugal_i` lazily per trial. Rejected: it is a per-pair constant determined by
  placement; storing it once on `EiPair` is simpler, faster, and avoids divergent per-trial
  recomputation.
* Pre-import t0052's library directly. Rejected: project rule disallows non-registered cross-task
  imports for the cell/sweep modules; the `code-snapshot/` path inside the t0052 library asset is a
  snapshot, not an importable Python package.

**Task types.** `task.json` lists `build-model` and `experiment-run`, and both apply. `build-model`
drives the library-asset structure, hyperparameter logging, and reproducibility-seed guidelines used
in the plan. `experiment-run` drives the multi-mode sweep, per-direction breakdowns in
`metrics.json`, deterministic seeds, the explicit-variant metrics format (FULL / AMPA_ONLY /
GABA_ONLY), the chart requirements, and the validation-gate pattern (small-scale dry run before the
full 360-trial sweep).

**Registered metrics applicable to this task** (from `aggregate_metrics`):
* `direction_selectivity_index` — applicable; written for FULL mode (and informationally for
  AMPA_ONLY).
* `tuning_curve_hwhm_deg` — applicable; written for FULL mode as an early-warning signal that the
  tuning curve is not a hard step.
* `tuning_curve_reliability` — applicable; computed via `tuning_curve_loss.compute_reliability`
  using cross-trial Pearson on the FULL CSV.
* `tuning_curve_rmse` — applicable only if a target tuning curve from t0004 is used as the
  reference. Computed against
  `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
  if present; otherwise omitted with a documented note ("no target curve loaded; t0053 is a
  mechanism-comparison task, not an optimisation task").

`efficiency_*` metrics are not in the registry. Inference time is not meaningful for a fixed
360-trial NEURON sweep; total wall-clock is logged in `results_detailed.md` rather than
`metrics.json`.

## Cost Estimation

* NEURON simulation: local CPU, $0.
* Plotting and analysis: local CPU, $0.
* No API calls (no LLM, no external data fetches).
* No remote machines (`available_services` is empty in `project/budget.json`).

**Total: $0.00.** Project budget is $1.00, current spend is $0.00. This task does not consume any of
the budget. `results/costs.json` will record `{}` (no paid services).

## Step by Step

### Milestone 1 — Bootstrap, Constants, SWC Loader

1. **Create `code/__init__.py`, `code/constants.py`, `code/paths.py`.** Create
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/__init__.py` (empty). Copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/constants.py` to
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/constants.py` and adapt: (a) **delete** the gabaMOD
   direction-tuning block (`THETA_ND_DEG`, `GABAMOD_PD`, `GABAMOD_ND`); (b) rename
   `NEURONHOME_SENTINEL_ENV` from `_T0052_NEURONHOME_BOOTSTRAPPED` to
   `_T0053_NEURONHOME_BOOTSTRAPPED`; (c) add `ACTIVE_FRACTION_LOWER = 0.4`,
   `ACTIVE_FRACTION_UPPER = 0.6` for the new soft sanity warning. Copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/paths.py` to
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/paths.py` and adapt: (a) change
   `TASK_ID = "t0053_minimal_dsgc_spatial_gaba"`; (b) change
   `LIBRARY_ID = "minimal_dsgc_spatial_gaba"`; (c) add
   `ACTIVE_FRACTION_CSV: Path = RESULTS_DIR / "active_fraction_per_direction.csv"`. Satisfies
   `REQ-8` (constants), part of `REQ-16` (path scaffolding).

2. **Copy `code/swc_io.py` and `code/neuron_bootstrap.py`.** Copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/swc_io.py` to
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/swc_io.py` verbatim (180 lines, pure stdlib SWC
   parser); update only the file-header docstring to attribute the copy to t0052 (which itself cites
   t0009). Copy `tasks/t0052_minimal_dsgc_scalar_gaba/code/neuron_bootstrap.py` to
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/neuron_bootstrap.py` verbatim (82 lines); rewrite the
   `tasks.t0052_minimal_dsgc_scalar_gaba.code.{constants, paths}` imports to
   `tasks.t0053_minimal_dsgc_spatial_gaba.code.{constants, paths}` and confirm the sentinel env-var
   constant resolves to `_T0053_NEURONHOME_BOOTSTRAPPED` (already changed in Step 1). Expected
   output:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0053_minimal_dsgc_spatial_gaba -- uv run python -c "from tasks.t0053_minimal_dsgc_spatial_gaba.code.neuron_bootstrap import ensure_neuron_importable; ensure_neuron_importable(); from neuron import h; print(h)"`
   prints a non-error `<HocTopLevelInterpreter>`. Satisfies `REQ-1` (runtime prerequisite).

### Milestone 2 — Cell Builder with Soma Origin and Quiescent-Rest Validation Gate

3. **[CRITICAL] Copy and extend `code/cell.py`.** Copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/cell.py` to
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/cell.py` (215 lines), rewrite the
   `tasks.t0052_minimal_dsgc_scalar_gaba.code.{constants, swc_io}` imports to the t0053 paths, then
   **extend** the `CellHandles` `@dataclass(frozen=True, slots=True)` with one new field:
   `soma_origin_um: tuple[float, float, float]`. In `build_dsgc_from_swc`, after collapsing the soma
   rows into a single section, populate
   `soma_origin_um = (soma_compartments[0].x, soma_compartments[0].y, soma_compartments[0].z)` and
   pass it into the `CellHandles(...)` constructor. Print the soma origin triple at completion
   alongside the section count and total dendritic length. Expected output: `dendrites` has > 6,000
   sections; total dendritic length is `1536.25 +/- 1` um; `soma_origin_um` is a finite triple.
   Satisfies `REQ-1`, `REQ-2` (channel inserts unchanged), and the spatial-driver prerequisite for
   `REQ-7`.

4. **[VALIDATION GATE] Quiescent-rest dry run, `code/test_quiescent_rest.py`.** Copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/test_quiescent_rest.py` (104 lines) to
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_quiescent_rest.py` verbatim and rewrite the
   `tasks.t0052_*` imports. With no synapses, run `h.finitialize(V_INIT_MV); h.continuerun(50.0)`
   and read soma voltage. **Baseline**: V_rest = -65 mV (passive). **Failure condition**: if final
   soma voltage is outside `-65 +/- 0.5 mV`, STOP, print the soma voltage trace, and debug the `pas`
   / `e_pas` / `Ra` / `cm` values before proceeding. **Inspection**: print soma voltage at t = 0,
   25, 50 ms; print conductance summary for soma and one dendrite section. Satisfies `REQ-2`.
   Idempotent: re-runnable.

### Milestone 3 — Synapse Placement and Centripetal-Gating Drivers

5. **Copy `code/placement.py`.** Copy `tasks/t0052_minimal_dsgc_scalar_gaba/code/placement.py` (87
   lines) to `tasks/t0053_minimal_dsgc_spatial_gaba/code/placement.py` and rewrite the
   `tasks.t0052_minimal_dsgc_scalar_gaba.code.cell` import. Function logic is unchanged: use
   `numpy.random.default_rng(seed=0)` and length-weighted sampling on `cell.dendrites`. Save the
   resulting list as JSON to `results/placement_seed0.json` for traceability. Expected output: 100
   entries; the saved JSON is bit-identical to
   `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` field-by-field. Satisfies
   `REQ-3`, `REQ-20`.

6. **Optional sanity smoke test, `code/test_placement_seed0_match.py`.** Add a ~30-line test that
   loads `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` and t0053's
   `results/placement_seed0.json` and confirms identical (`section_index`, `section_x`, `x_um`,
   `y_um`) tuples for all 100 entries within `1e-9` tolerance. If the t0052 file does not exist on
   the worktree, skip the test. Strengthens `REQ-3`, `REQ-20`.

7. **[CRITICAL] Rewrite `code/synapses.py` for centripetal-gating.** Copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/synapses.py` (181 lines) to
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/synapses.py` as a starting point, then make the
   following targeted changes:
   * **Drop** the `gaba_mod(theta_deg, theta_pd_deg)` function entirely.
   * **Extend** the `EiPair` `@dataclass(frozen=True, slots=True)` with a new field
     `theta_centrifugal_rad: float`.
   * **Extend** `build_ei_pairs(*, h, locations, sections, soma_origin_um) -> list[EiPair]` with the
     new keyword `soma_origin_um: tuple[float, float, float]`. For each pair compute
     `theta_centrifugal_rad = atan2(loc.y_um - soma_origin_um[1], loc.x_um - soma_origin_um[0])` and
     store it on the pair.
   * **Add** a new pure function
     `i_synapse_fires(*, theta_stim_deg: float, theta_centrifugal_deg: float) -> bool` returning
     `cos(radians(theta_stim_deg - theta_centrifugal_deg)) < 0` (strict inequality).
   * **Add** a new return dataclass
     `@dataclass(frozen=True, slots=True) class ScheduleResult: onset_times_ms: list[float]; i_fired_mask: list[bool]`.
   * **Rewrite** `schedule_ei_onsets(*, pairs, angle_deg, velocity_um_per_ms) -> ScheduleResult`
     (drops the `gaba_mod_theta` parameter). For each pair: compute `t_bar` (unchanged from t0052);
     set `pair.ampa_netstim.start = max(t_bar, 0.0) + BASE_OFFSET_MS` and
     `pair.ampa_netcon.weight[0] = AMPA_PEAK_NS * 1e-3`; compute
     `fires = i_synapse_fires(theta_stim_deg=angle_deg, theta_centrifugal_deg=degrees(pair.theta_centrifugal_rad))`;
     if `fires`, set `pair.gaba_netstim.start = max(t_bar, 0.0) + BASE_OFFSET_MS` and
     `pair.gaba_netcon.weight[0] = GABA_BASE_NS * 1e-3`; if not, set
     `pair.gaba_netstim.start = TSTOP_MS + 1.0` (defence-in-depth) and
     `pair.gaba_netcon.weight[0] = 0.0`. Append `t_bar + BASE_OFFSET_MS` and `fires` to the result
     lists. Return the populated `ScheduleResult`. Satisfies `REQ-4`, `REQ-5`, `REQ-6`, `REQ-7`.

8. **Replace `test_gaba_mod.py` with `test_spatial_gating.py`.** Do **not** copy
   `tasks/t0052_minimal_dsgc_scalar_gaba/code/test_gaba_mod.py`. Create
   `tasks/t0053_minimal_dsgc_spatial_gaba/code/test_spatial_gating.py` (~50 lines new) asserting:
   (a) `i_synapse_fires(theta_stim_deg=0, theta_centrifugal_deg=0)` is `False` (cos(0)=1, gating
   condition `cos < 0` is False); (b) `i_synapse_fires(theta_stim_deg=180, theta_centrifugal_deg=0)`
   is `True` (cos(180)=-1 < 0); (c) `i_synapse_fires(theta_stim_deg=90, theta_centrifugal_deg=0)` is
   `False` (cos(90)=0, strict inequality fails); (d) **uniform-random sanity**: place 1,000 synapses
   with centrifugal angles uniformly in [0, 2*pi) using `numpy.random.default_rng(seed=42)`, count
   fired for `theta_stim_deg=0`, and assert the active fraction is within `0.5 +/- 0.05`. Satisfies
   `REQ-7` (gate correctness).

### Milestone 4 — Trial Runner and Sweep with New Active-Fraction Capture

9. **Copy and edit `code/trial.py`.** Copy `tasks/t0052_minimal_dsgc_scalar_gaba/code/trial.py` (140
   lines) to `tasks/t0053_minimal_dsgc_spatial_gaba/code/trial.py`. Rewrite the
   `tasks.t0052_minimal_dsgc_scalar_gaba.code.{constants, synapses}` imports. Apply these targeted
   edits:
   * **Drop** the `gaba_mod_theta: float` field from the `TrialResult` dataclass.
   * **Add** two new `TrialResult` fields: `i_fired_mask: list[bool]` and
     `i_active_fraction: float`.
   * **Update** `run_one_trial(...)` body: instead of computing `gaba_mod_theta` and passing it into
     `schedule_ei_onsets`, call the new
     `schedule_ei_onsets(pairs=pairs, angle_deg=angle_deg, velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS)`
     and capture the returned `ScheduleResult`. Compute
     `i_active_fraction = sum(schedule.i_fired_mask) / len(schedule.i_fired_mask)` and pass both
     into the `TrialResult`.
   * **Update** `_apply_mode_weights`: AMPA_ONLY zeroes every I synapse's `gaba_netcon.weight[0]`
     regardless of mask (overrides the gate); GABA_ONLY zeroes every E synapse's
     `ampa_netcon.weight[0]` (I weights stay as set by the gate). Satisfies `REQ-10` and the
     recording subset of `REQ-11..REQ-15`.

10. **[CRITICAL][VALIDATION GATE] Copy and edit `code/run_tuning_curve.py`.** Copy
    `tasks/t0052_minimal_dsgc_scalar_gaba/code/run_tuning_curve.py` (390 lines) to
    `tasks/t0053_minimal_dsgc_spatial_gaba/code/run_tuning_curve.py`. Rewrite all
    `tasks.t0052_minimal_dsgc_scalar_gaba.code.*` imports to the t0053 paths. Apply these targeted
    edits:
    * **Pass** `soma_origin_um=cell.soma_origin_um` into `build_ei_pairs`.
    * **Drop** all `gaba_mod_theta` references in setup, the dry-run gate, and CSV writers.
    * **Extend** the activation-times CSV writer to include a fifth column `is_fired` (0 or 1) per
      (angle, synapse_index). For E synapses (always firing) this is always 1; for I synapses it
      follows the per-trial mask.
    * **Add** a new CSV writer that emits the per-direction average active fraction:
      `results/active_fraction_per_direction.csv` with columns `(angle_deg, active_fraction)`, where
      `active_fraction` is the mean of `trial.i_active_fraction` across the 10 FULL-mode trials for
      that direction.

    **Validation gate.** Before launching the full 12 x 10 x 3 = 360-trial sweep, run a 1-direction
    x 2-trial dry run for each mode (6 trials total, ~10 s wall-clock).
    * **Trivial baseline 1 (AMPA spike count)**: AMPA_ONLY at theta=0 must produce a non-zero firing
      rate (lower bound ~1 Hz; one event per E synapse depolarizes the soma enough). FULL at theta=0
      must be at least 80% of AMPA_ONLY at theta=0.
    * **Trivial baseline 2 (active-fraction)**: GABA_ONLY at theta=0 must produce a per-trial
      `i_active_fraction` in `[0.3, 0.7]` (sanity for the centripetal-gating rule on roughly
      symmetric placement; tighter than the full-direction soft check because we are at a single
      angle).
    * **Failure conditions**: if AMPA_ONLY at theta=0 produces 0 spikes, STOP and read 5 individual
      trial trace samples from the CSV; verify `pair.ampa_netcon.weight[0]` was non-zero at
      scheduling time, verify `NetStim.start` was non-NaN, verify the soma voltage trace shows EPSP
      onsets. If `i_active_fraction` is outside `[0.3, 0.7]`, STOP and inspect 5 individual pairs'
      `theta_centrifugal_rad` values, verify `soma_origin_um` was passed in, verify the cosine gate
      sign convention. Do not run the full 360-trial sweep until both gates pass.
    * Then run the full sweep with a `tqdm` progress bar.

    Expected outputs after the full sweep: `results/tuning_curve_full.csv` (120 rows),
    `results/tuning_curve_ampa_only.csv` (120 rows), `results/tuning_curve_gaba_only.csv` (120
    rows), `results/spike_times_full.csv` (variable rows), `results/voltage_traces_full.csv`,
    `results/voltage_traces_ampa_only.csv`, `results/voltage_traces_gaba_only.csv`,
    `results/activation_times.csv` (1,200 rows: 12 angles x 100 synapses, with `is_fired`),
    `results/active_fraction_per_direction.csv` (12 rows). Satisfies `REQ-8`, `REQ-9`, `REQ-10`,
    plus the data backbone for `REQ-11..REQ-15`, `REQ-21`.

### Milestone 5 — Figures and Metrics

11. **Copy and extend `code/render_figures.py`.** Copy
    `tasks/t0052_minimal_dsgc_scalar_gaba/code/render_figures.py` (231 lines) to
    `tasks/t0053_minimal_dsgc_spatial_gaba/code/render_figures.py`. Rewrite all `tasks.t0052_*`
    imports. Existing six figure functions remain unchanged in behaviour:
    * `render_soma_voltage_per_direction` — per-direction mean +/- SD soma V(t) across 10 FULL
      trials, 12 PNGs `v_soma_dir_<deg>.png`.
    * `render_aggregate_epsp` — same for AMPA_ONLY voltage traces (`epsp_dir_<deg>.png`).
    * `render_aggregate_ipsp` — same for GABA_ONLY voltage traces (`ipsp_dir_<deg>.png`).
    * `render_psth` — 5 ms bin firing-rate histogram per direction, mean across 10 FULL trials
      (`psth_dir_<deg>.png`).
    * `render_activation_histogram` — per-direction histogram of synapse onset times, with the
      `is_fired==1` rows highlighted as a separate facet (`activation_dir_<deg>.png`).
    * Polar tuning curve and Cartesian tuning curve via library imports
      `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve, plot_cartesian_tuning_curve, plot_angle_raster_psth`,
      writing `polar_tuning_curve.png`, `cartesian_tuning_curve.png`, and
      `raster_psth_dir_<deg>.png`.

    **NEW**: add `render_active_fraction_polar(*, active_fraction_csv, out_dir)` (~25 lines) reading
    `results/active_fraction_per_direction.csv` and producing
    `results/images/active_fraction_polar.png` via `subplot_kw=dict(projection="polar")`. The chart
    shows a single closed polygon of fraction vs angle with a 0..1 radial axis and a faint reference
    circle at radius 0.5. Satisfies `REQ-11`, `REQ-12`, `REQ-13`, `REQ-14`, `REQ-15`, and `REQ-21`.

12. **Copy `code/metrics_extra.py` verbatim.** Copy
    `tasks/t0052_minimal_dsgc_scalar_gaba/code/metrics_extra.py` (44 lines) to
    `tasks/t0053_minimal_dsgc_spatial_gaba/code/metrics_extra.py`; rewrite no imports (it has no
    cross-task imports). Provides `compute_vector_sum_dsi` and `compute_preferred_direction_deg`.
    Used by Step 13. Satisfies the vector-sum component of `REQ-14`.

13. **Copy and edit `code/compute_metrics.py`.** Copy
    `tasks/t0052_minimal_dsgc_scalar_gaba/code/compute_metrics.py` (304 lines) to
    `tasks/t0053_minimal_dsgc_spatial_gaba/code/compute_metrics.py`. Rewrite all `tasks.t0052_*`
    imports. Apply these targeted edits:
    * **Drop** `from ...synapses import gaba_mod` and any usage.
    * **Drop** the IPSP-conductance hard gate
      (`assert IPSP_RATIO_LOWER <= ratio <= IPSP_RATIO_UPPER`).
    * **Add** a soft active-fraction sanity check: read `results/active_fraction_per_direction.csv`,
      compute the cross-direction mean `mean_af = active_fractions.mean()`, print the per-direction
      list and the mean. If `mean_af` is outside
      `[ACTIVE_FRACTION_LOWER=0.4, ACTIVE_FRACTION_UPPER=0.6]`, print a `WARNING:` message naming
      the value and continuing — do **not** raise. Always store `active_fraction_per_direction`
      (12 entries, dict[int, float]) and `mean_active_fraction` (float) in
      `derived_quantities.json`.
    * Keep the multi-variant `metrics.json` writer producing FULL / AMPA_ONLY / GABA_ONLY entries
      with `direction_selectivity_index`, `tuning_curve_hwhm_deg` (FULL), `tuning_curve_reliability`
      (FULL, AMPA_ONLY).
    * Keep `tuning_curve_rmse` only when
      `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
      exists; otherwise omit with a documented note in `derived_quantities.json`.
    * Always write `peak_hz`, `null_hz`, `vector_sum_dsi`, `preferred_direction_deg` per variant to
      `derived_quantities.json` alongside the active-fraction block. Satisfies `REQ-14`, `REQ-17`,
      `REQ-18`.

### Milestone 6 — Library Asset

14. **Create the `minimal_dsgc_spatial_gaba` library asset.** Create
    `tasks/t0053_minimal_dsgc_spatial_gaba/assets/library/minimal_dsgc_spatial_gaba/details.json`
    with `spec_version="2"`, `library_id="minimal_dsgc_spatial_gaba"`,
    `name="Minimal DSGC Spatial GABA"`, `version="0.1.0"`, `short_description` (10+ words; mention
    centripetal-gating and per-synapse spatial firing rule), `description_path="description.md"`,
    `module_paths=["code/constants.py", "code/paths.py", "code/swc_io.py", "code/neuron_bootstrap.py", "code/cell.py", "code/placement.py", "code/synapses.py", "code/trial.py", "code/run_tuning_curve.py", "code/render_figures.py", "code/compute_metrics.py", "code/metrics_extra.py"]`,
    `entry_points` listing `build_dsgc_from_swc`, `sample_dendritic_locations`, `build_ei_pairs`,
    `schedule_ei_onsets`, `i_synapse_fires`, `run_one_trial`, `TrialMode`, `ScheduleResult`,
    `compute_vector_sum_dsi`, `compute_preferred_direction_deg`, `render_active_fraction_polar`,
    `dependencies=["neuron", "numpy", "matplotlib", "tqdm"]`,
    `test_paths=["code/test_quiescent_rest.py", "code/test_spatial_gating.py", "code/test_placement_seed0_match.py"]`,
    `categories=["compartmental-modeling", "direction-selectivity", "synaptic-integration"]`,
    `created_by_task="t0053_minimal_dsgc_spatial_gaba"`, `date_created="2026-04-25"`. Create
    `assets/library/minimal_dsgc_spatial_gaba/description.md` with YAML frontmatter and the eight
    mandatory sections required by `meta/asset_types/library/specification.md`: Metadata, Overview,
    API Reference, Usage Examples, Dependencies, Testing, Main Ideas, Summary (each meeting its
    minimum word count). Run the project's library verificator and confirm zero errors. Satisfies
    `REQ-16`.

15. **Confirm $0 cost.** Verify no remote machines were created and no paid API calls were made
    during implementation. (The orchestrator's standard cost step writes the cost JSON itself; this
    plan item only flags the implementation-side requirement that nothing paid is invoked.)
    Satisfies `REQ-19`.

## Remote Machines

None required. Local CPU only. The model has roughly 6,700 dendritic compartments, 200 synapses, and
a 1.5-second simulation window at `dt = 0.025 ms`; one trial completes in ~5-15 seconds on a modern
CPU. Total: 360 trials x ~10 s = ~1 hour wall-clock for the full sweep. No GPU, no remote
provisioning, no `available_services` consumed.

## Assets Needed

* `dsgc-baseline-morphology-calibrated` from `t0009_calibrate_dendritic_diameters`. Read directly
  from
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`.
* Library `tuning_curve_viz` from `t0011_response_visualization_library`. Imported as
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import ...`.
* Library `tuning_curve_loss` from `t0012_tuning_curve_scoring_loss_library`. Imported as
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import ...`.
* NEURON 8.2.7 install at `C:\Users\md1avn\nrn-8.2.7` (toolchain established in t0007; imported via
  `code/neuron_bootstrap.py`).
* Optional:
  `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
  for `tuning_curve_rmse` computation; if absent the metric is omitted with a note.
* Optional: `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` for the
  placement-diff smoke test (Step 6); if absent the test is skipped.
* 14 source-of-truth modules from `tasks/t0052_minimal_dsgc_scalar_gaba/code/` are copied (not
  imported) into `tasks/t0053_minimal_dsgc_spatial_gaba/code/` per the cross-task copy rule.

## Expected Assets

This task produces exactly one library asset, matching `task.json`
`expected_assets = {"library": 1}`:

* `library/minimal_dsgc_spatial_gaba` — the cell builder (with soma origin), SWC loader, synapse
  placer, AMPA position-gated event driver, GABA spatial centripetal-gating event driver, three-mode
  trial runner (FULL / AMPA_ONLY / GABA_ONLY), 12-direction sweep harness, renderer suite (including
  the new active-fraction polar plot), and metrics computer that together implement the minimal
  spatial-asymmetry DSGC. Code lives under `tasks/t0053_minimal_dsgc_spatial_gaba/code/`; the asset
  folder contains only `details.json` and `description.md`.

No other asset types (paper, dataset, model, predictions, answer) are produced.

## Time Estimation

* Research (already done): ~3 hours total for `research_code.md`. No remaining research time.
* Milestone 1 (bootstrap, constants, SWC loader): ~1 hour (mostly copy + small edits).
* Milestone 2 (cell builder + soma origin extension, quiescent-rest gate): ~2 hours including debug.
* Milestone 3 (placement, synapses rewrite for spatial gating, new test): ~3 hours (the
  `synapses.py` rewrite is the only significant new code).
* Milestone 4 (trial runner edits, sweep + active-fraction CSV, validation gate, full 360-trial
  run): ~3 hours wall-clock (including the ~1 hour of NEURON simulation).
* Milestone 5 (renderers + new active-fraction polar plot, metrics edits, soft sanity check): ~2
  hours.
* Milestone 6 (library asset metadata + description.md): ~1 hour.
* Verification, fixing verificator errors: ~1 hour.
* **Total implementation wall-clock: ~13 hours**, comfortably under the spec's "~1 week" ceiling.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `soma_origin_um` not threaded through `build_ei_pairs`, leading to all `theta_centrifugal_i = 0` and a degenerate gate | Medium | Critical — every direction would have the same active fraction | Step 7 makes `soma_origin_um` a required keyword on `build_ei_pairs`; mypy fails if omitted. Step 10 dry-run gate checks `i_active_fraction` is in `[0.3, 0.7]` at theta=0, which would fail if all centrifugal angles were 0 (every synapse fires for theta=0, fraction = 1.0 outside the gate). |
| Cosine gate sign convention flipped (`> 0` instead of `< 0`), inverting the directional asymmetry | Medium | Critical — preferred direction would be wrong | Step 8's `test_spatial_gating.py` asserts the three diagnostic angles (PD-side not fired, ND-side fired, perpendicular not fired); this catches a flipped sign immediately. |
| Placement non-identical to t0052 (cell-builder iteration order drift) | Low | Critical — breaks downstream trial-for-trial comparison | Step 6's `test_placement_seed0_match.py` diffs the saved placement JSON against t0052's; failure is loud and pre-implementation. |
| AMPA-only at theta=0 produces 0 spikes (synapses misconfigured or NetStim.start out of window) | Low | Critical — the entire experiment is meaningless | Step 10 dry-run validation gate: 1 angle x 2 trials before full sweep. If 0 spikes, inspect 5 individual `NetStim.start` and `NetCon.weight[0]` values, verify `Exp2Syn.tau1`, `tau2`, `e` were assigned, and verify `BASE_OFFSET_MS` puts events inside `[0, TSTOP_MS]`. Do not advance to full sweep until non-zero. |
| Mean active fraction across directions falls outside [0.4, 0.6] | Medium | Soft — informative; documented as morphology asymmetry | `compute_metrics.py` prints a `WARNING` line and stores per-direction values in `derived_quantities.json`; the reporting step explains the deviation as the off-centre soma's effect on the dendritic-field hemisphere split. No hard fail. |
| Hard-step DSI=1.0 tuning curve (the t0022 / t0052 binary-spiking failure mode) | Medium | Soft — informative but not a blocker | HWHM is written to `metrics.json` for FULL; vector-sum DSI is included alongside primary DSI so a hard step is detectable; if HWHM > 100 deg flag in `derived_quantities.json` for the orchestrator's reporting step to discuss. |
| Driving-force saturation amplifies IPSP voltage non-linearly (full 2 nS amplitude vs t0052's scaled values) | Medium | Soft — affects scaling expectations but not validity | Plan flags this in the reporting step; expect IPSP traces to show a ceiling near E_GABA = -75 mV. The metric remains qualitative (per-direction IPSP shape) rather than a quantitative ratio. |
| NEURON Windows bootstrap fails (env var, DLL path, version mismatch) | Low | Blocking | Reuse the t0052 / t0046 bootstrap pattern; the new sentinel `_T0053_NEURONHOME_BOOTSTRAPPED` is the only change; if `ensure_neuron_importable()` raises, file an intervention noting expected vs actual NEURONHOME. |
| Per-direction wall-clock blows up beyond 1 hour | Low | Soft | The dry-run gate also profiles 1 trial. If a single trial takes > 60 s, raise `DT_MS` to 0.05 ms and re-profile; if still > 30 s, reduce `N_TRIALS_PER_ANGLE` to 5 and document the deviation in `results_detailed.md`. |
| `tuning_curve_loss` or `tuning_curve_viz` API changes since the research was written | Low | Soft | Imports use the registered library paths; if `compute_dsi` signature changes, the function call will raise immediately, the implementation patches the call, and re-runs Step 13. |

## Verification Criteria

* `tasks/t0053_minimal_dsgc_spatial_gaba/plan/plan.md` exists with all 11 mandatory sections and
  zero verificator errors. Run
  `uv run python -u -m arf.scripts.verificators.verify_plan t0053_minimal_dsgc_spatial_gaba` and
  confirm `errors: 0`.

* The library asset validates. Run the project's library verificator
  `uv run python -u -m meta.asset_types.library.verificator tasks/t0053_minimal_dsgc_spatial_gaba/assets/library/minimal_dsgc_spatial_gaba`
  and confirm zero errors. Confirms `REQ-16`.

* All three sweep CSVs exist and have 120 rows each. Run
  `python -c "import pandas as pd; [print(p, len(pd.read_csv(p))) for p in ['tasks/t0053_minimal_dsgc_spatial_gaba/results/tuning_curve_full.csv', 'tasks/t0053_minimal_dsgc_spatial_gaba/results/tuning_curve_ampa_only.csv', 'tasks/t0053_minimal_dsgc_spatial_gaba/results/tuning_curve_gaba_only.csv']]"`
  and confirm 120 in every file. Confirms `REQ-9`, `REQ-10`.

* All 12 per-direction PNGs exist for soma V, EPSP, IPSP, PSTH, and activation histograms. Run
  `python -c "from pathlib import Path; d = Path('tasks/t0053_minimal_dsgc_spatial_gaba/results/images'); [print(name, sum(1 for _ in d.glob(name + '_dir_*.png'))) for name in ['v_soma','epsp','ipsp','psth','activation']]"`
  and confirm 12 per category. Confirms `REQ-11`, `REQ-12`, `REQ-13`, `REQ-15`.

* The new active-fraction polar PNG exists. Run
  `python -c "from pathlib import Path; p = Path('tasks/t0053_minimal_dsgc_spatial_gaba/results/images/active_fraction_polar.png'); assert p.exists(); print('active_fraction_polar.png present, size_bytes', p.stat().st_size)"`
  and confirm a positive byte count. Confirms `REQ-21`.

* Active-fraction soft sanity check passes (informational). Run
  `python -c "import json; d = json.load(open('tasks/t0053_minimal_dsgc_spatial_gaba/results/derived_quantities.json')); af = d['active_fraction_per_direction']; m = d['mean_active_fraction']; print('per_direction', af, 'mean', m); print('IN_BOUNDS' if 0.4 <= m <= 0.6 else 'OUT_OF_BOUNDS_BUT_OK')"`.
  Bounds violation is logged, not fatal. Confirms `REQ-18`.

* `metrics.json` is in explicit multi-variant format with at least the FULL variant's
  `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`. Run
  `python -c "import json; m = json.load(open('tasks/t0053_minimal_dsgc_spatial_gaba/results/metrics.json')); assert 'variants' in m and 'full' in m['variants']; full = m['variants']['full']['metrics']; [None for k in ['direction_selectivity_index','tuning_curve_hwhm_deg','tuning_curve_reliability'] if (lambda kk: (_ for _ in ()).throw(AssertionError(kk)))(k) if k not in full]; print(full)"`
  and confirm. Confirms `REQ-14`, `REQ-17`.

* `derived_quantities.json` contains peak Hz, null Hz, vector-sum DSI, preferred direction (deg) per
  variant plus `active_fraction_per_direction` and `mean_active_fraction`. Run
  `python -c "import json; d = json.load(open('tasks/t0053_minimal_dsgc_spatial_gaba/results/derived_quantities.json')); [None for k in ['peak_hz','null_hz','vector_sum_dsi','preferred_direction_deg','active_fraction_per_direction','mean_active_fraction'] if k not in d and (_ for _ in ()).throw(AssertionError(k))]; print('keys ok')"`
  and confirm. Confirms `REQ-14`, `REQ-17`, `REQ-18`.

* Spatial-gating unit tests pass. Run
  `uv run python -u tasks/t0053_minimal_dsgc_spatial_gaba/code/test_spatial_gating.py` and confirm
  zero failures. Confirms `REQ-7`.

* Placement is identical to t0052's. Run
  `uv run python -u tasks/t0053_minimal_dsgc_spatial_gaba/code/test_placement_seed0_match.py` and
  confirm zero failures (or skipped if the t0052 file is absent). Confirms `REQ-3`, `REQ-20`.

* All `REQ-*` items map to at least one Step by Step item. Run
  `python -c "import re; t=open('tasks/t0053_minimal_dsgc_spatial_gaba/plan/plan.md').read(); reqs=sorted({m for m in re.findall(r'REQ-\d+', t)}, key=lambda s:int(s[4:])); print(reqs); assert reqs == [f'REQ-{i}' for i in range(1, 22)], reqs"`
  and confirm `REQ-1` through `REQ-21` are all present in the plan body. Confirms requirement
  coverage.

* Cost gate: confirm `results/costs.json` is `{}` (no paid services) and no machine-setup log
  exists. Run
  `python -c "import json; assert json.load(open('tasks/t0053_minimal_dsgc_spatial_gaba/results/costs.json')) == {}; print('zero cost confirmed')"`.
  Confirms `REQ-19`.
