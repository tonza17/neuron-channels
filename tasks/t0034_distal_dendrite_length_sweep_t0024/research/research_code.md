---
spec_version: "1"
task_id: "t0034_distal_dendrite_length_sweep_t0024"
research_stage: "code"
tasks_reviewed: 10
tasks_cited: 10
libraries_found: 7
libraries_relevant: 2
date_completed: "2026-04-23"
status: "complete"
---
# Research Code: Distal-Dendrite Length Sweep on the t0024 DSGC Port

## Task Objective

Re-run the t0029 distal-dendrite length sweep (seven multipliers, 0.5x-2.0x of baseline `sec.L`, 12
directions, 10 trials/angle = 840 trials) on the **t0024 de Rosenroll 2026 DSGC port** instead of
the t0022 testbed. t0024 carries AR(2)-correlated stochastic release (rho=0.6) that produces
non-zero null-direction firing, so **primary DSI (peak-minus-null) is the operative discriminator**
— unlike t0029 where it pinned at 1.000 because t0022's deterministic E-I driver silenced the null
direction. Classify the resulting DSI-vs-length curve as monotonic (Dan2018 passive-TR weighting),
saturating (Sivyer2013 dendritic-spike branch independence), or non-monotonic (neither). Local-CPU
only, zero external cost, budget 2-4 h wall time. Outputs: per-length canonical curve CSVs,
`results/data/sweep_results.csv`, `results/images/dsi_vs_length.png`, polar overlay, explicit
multi-variant `results/metrics.json`.

## Library Landscape

The ARF library aggregator is not wired into this worktree
(`arf.scripts.aggregators.aggregate_libraries` is absent), so the library enumeration was done by
walking `tasks/*/assets/library/`. Seven libraries exist; two are directly relevant for this task,
the rest are context-only.

* `de_rosenroll_2026_dsgc` ([t0024], v0.1.0) — **Highly relevant.** Registered library providing the
  t0024 DSGC port. Module paths expose
  `tasks.t0024_port_de_rosenroll_2026_dsgc.code.{ar2_noise, build_cell, constants, paths, plot_tuning_curves, run_tuning_curve, score_envelope}`.
  The entry point `build_dsgc_cell` returns a `DSGCCell` dataclass with `soma`, `all_dends`,
  `primary_dends`, `non_terminal_dends`, `terminal_dends`, and `terminal_locs_xy` already
  enumerated. The driver entry point `run_single_trial` accepts
  `(cell, ncs_ach, ncs_gaba, direction_deg, rho, seed)` and the helper `_setup_synapses` creates
  per-terminal ACh + GABA synapses via NetCons.

* `tuning_curve_loss` ([t0012], v0.1.0) — **Highly relevant.** Canonical DSI / peak / null / HWHM /
  reliability scorer. Import via
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve, TuningCurve)`.
  Accepts the canonical `(angle_deg, trial_seed, firing_rate_hz)` CSV that t0024 and t0026 already
  emit, so per-length curves can be scored without format conversion.

* `modeldb_189347_dsgc_dendritic` ([t0022], v0.1.0) — **Not relevant for this task.** This is the
  testbed t0029 swept (different HOC morphology via `RGCmodel.hoc`, deterministic E-I schedule,
  `h.RGC.ON` section list). t0034 deliberately avoids it — the whole point of t0034 is to run on
  t0024 instead.

* `modeldb_189347_dsgc_gabamod` ([t0020], v0.1.0) — Not relevant. Alternative gabaMOD-based driver
  unrelated to the t0024 stochastic-release biophysics.

* `modeldb_189347_dsgc` ([t0008], v0.1.0) — Not relevant. t0022 inherits this HOC template; t0024
  uses a different HOC template (`RGCmodelGD.hoc`).

* `tuning_curve_viz` ([t0011], v0.1.0) — Not directly needed. The primary chart `dsi_vs_length.png`
  is a scalar sweep plot, not a tuning-curve overlay. Optional use for a polar diagnostic where the
  "models" are the 7 multiplier labels.

* `dsgc-baseline-morphology` dataset asset ([t0005]) — Context only; t0024 does not use the
  NeuroMorpho SWC. It uses the vendored `RGCmodelGD.hoc` under
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/`.

## Key Findings

### The t0024 driver entry point is `run_tuning_curve.py` plus a persistent cell context

The main tuning-curve entry point in t0024 is
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py` [t0024]. Its `main` builds a
`DSGCCell` via `build_dsgc_cell()` from `build_cell.py` (~330 lines) and then calls `run_sweep` for
each of four `SweepConfig`s (8-direction and 12-angle each times correlated/uncorrelated). The
per-trial heart is `run_single_trial(cell, ncs_ach, ncs_gaba, direction_deg, rho, seed)` which:
projects bar arrival times for the given direction, generates AR(2)-modulated rate traces via
`_rates_with_ar2_noise`, converts rates to Poisson event lists via `_rates_to_events`, queues the
events through each NetCon via `FInitializeHandler`, records soma voltage, and returns spikes + peak
mV. The DSGCCell and synapse bundle must be reused across (length, angle, trial) combinations to
amortise NEURON build cost. [t0026] established this pattern in `trial_runner_t0024.py:63-72`, where
`CellContextT0024(cell, bundle)` is built once and
`run_one_trial_vrest(ctx=..., direction_deg=..., rho=..., seed=..., v_rest_mv=...)` consumes it
across 960 trials.

### t0029's `identify_distal_sections` uses `h.RGC.ON`; t0024 has no such arbor

t0029's helper at `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py:37-52`
[t0029] iterates `h.RGC.dends`, filters to members of the `h.RGC.ON` SectionList, and further
filters to HOC leaves (`h.SectionRef(sec=sec).nchild() == 0`). This is specific to the t0022 HOC
morphology, which has separate ON/OFF arbors declared in `RGCmodel.hoc`. **t0024's morphology is
different**: `build_cell.build_dsgc_cell()` instantiates `h.DSGC(0, 0)` from `RGCmodelGD.hoc` (lines
255-265), which has a single dendritic arbor, not ON/OFF arbors. Walking `h.RGC.ON` on the t0024
cell raises `AttributeError`. The adapter for t0034 is therefore structurally different but
biologically identical: t0024's `_map_tree` (lines 140-168) already performs an equivalent topology
walk that populates `terminal_dends` (HOC leaves), `non_terminal_dends` (internal dends below the
primaries), and `primary_dends` (depth-1 dends). The `DSGCCell.terminal_dends` list **is** the
distal-leaf list we need — no further filtering required, no Strahler port needed, no `h.RGC.ON`
test.

### Primary DSI is meaningful on t0024 where it was pinned on t0029

[t0029] reports `DSI (preferred/null) = 1.000 at every multiplier` across the full 0.5x-2.0x sweep
because the t0022 deterministic driver produces zero firing at every angle >= 150 deg from
preferred, so `null_hz = 0` and `dsi = (peak - 0)/(peak + 0) = 1.0` by construction [t0029] results.
[t0026]'s V_rest sweep on t0024 shows primary DSI ranges **0.3606 at V_rest=-20 mV** to **0.6746 at
V_rest=-90 mV**, a **1.9x modulation** with measurable dynamic range [t0026]. The reason is AR(2)
noise: stochastic release at the null-direction synapses still drives **non-zero null firing** (null
Hz ranges ~0.5-3 Hz across V_rest values on t0024), so the denominator `peak + null` stays bounded
away from `peak`. This makes primary DSI the operative discriminator for t0034, reversing the
null-result mechanism of t0029.

### AR(2) correlation rho=0.6 is the plan-level baseline and must not be perturbed

`C.AR2_CROSS_CORR_RHO_CORRELATED = 0.6` in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:68` [t0024] is the correlated-condition
default used by both t0024's `run_sweep` (when `cfg.correlated=True`) and by t0026's
`run_vrest_sweep_t0024.py` via `AR2_RHO_T0024 = 0.6` in
`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/constants.py` [t0026]. The length sweep must
preserve this value — changing rho would conflate a morphology effect with a release-correlation
effect. t0024's `_rates_with_ar2_noise(..., rho=rho, ...)` threads rho down to `generate_ar2_batch`,
which is the only consumer. Keep `rho=C.AR2_CROSS_CORR_RHO_CORRELATED` at every call site. Keep
`gaba_weight_scale=1.0` (the correlated default in `_setup_synapses`) and do not set up an
uncorrelated arm — the length sweep is a single-condition sweep.

### Wall time on t0024 is ~12 s per (angle, trial) — full sweep ~2.8 h

[t0026]'s t0024 wall-time log at
`tasks/t0026_vrest_sweep_tuning_curves_dsgc/data/t0024/wall_time_by_vrest.json` reports **~1400-
1580 s per 120-trial V_rest point** (10 trials x 12 angles), i.e. **~11.7-13.2 s/trial** [t0026].
Applying the ~12 s/trial anchor to t0034's sweep: 7 multipliers x 12 angles x 10 trials = 840 trials
x 12 s = **~168 min ~ 2.8 h**. With cell-build overhead (~10-20 s once) and per-length wall-time
logging, the end-to-end estimate is **2-4 h** as stated in the task description. In contrast,
t0029's t0022 sweep completed in **42 min** because t0022 runs at ~3.5 s/trial without stochastic
release [t0029] — a ~3.4x speedup relative to t0024.

### The t0026 trial-runner pattern is the template to copy

`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/trial_runner_t0024.py` (169 lines) [t0026] is the
closest existing pattern: it imports `_setup_synapses`, `_bar_arrival_times`,
`_rates_with_ar2_noise`, `_rates_to_events`, `_gaba_prob_for_direction`, `_count_spikes`,
`BASE_ACH_PROB`, `RATE_DT_MS`, `SynapseBundle` from the t0024 library, builds a `CellContextT0024`
once via `build_cell_context()`, and exposes
`run_one_trial_vrest(ctx, direction_deg, rho, seed, v_rest_mv)` that inserts
`set_vrest(h, v_rest_mv)` between `h.tstop=...` and `h.finitialize(v_rest_mv)`. The length-sweep
analogue is trivial: replace `set_vrest` with `set_distal_length_multiplier` (called **at the outer
sweep boundary**, not inside the trial loop), drop the `v_rest_mv` parameter, and keep the
`rho=C.AR2_CROSS_CORR_RHO_CORRELATED` plumb- through.

### Dan2018 vs Sivyer2013 predictions for t0024 DSI-vs-length

From the [t0027] synthesis
`tasks/t0027_literature_survey_morphology_ds_modeling/assets/answer/ morphology-direction-selectivity-modeling-synthesis/full_answer.md`:

* **Dan2018 (passive transfer-resistance weighting)** predicts **monotonic DSI growth with distal
  length**. Dan2018 formalized TR weighting as the canonical dendrite-to-axon integration rule in
  fly VS cells [t0027]. Longer distal branches have lower TR to the soma, so the TR-gradient
  steepens across the tree, up-weighting preferred-direction inputs relative to null-direction
  inputs. The prediction for t0024: DSI should climb monotonically as the distal multiplier
  increases from 0.5x to 2.0x.

* **Sivyer2013 (dendritic-spike branch independence)** predicts a **saturating DSI curve**.
  [Sivyer2013] via [Schachter2010]/[t0027] show that DSGC terminal dendrites initiate fast spikes
  locally, and that input resistance scales from 150-200 MOhm proximally to >1 GOhm distally,
  producing a ~4x DSI amplification via threshold nonlinearity [t0027]. Once distal branches clear
  local spike threshold, further lengthening does not add DSI — the mechanism saturates. The
  prediction for t0024: DSI should plateau at moderate multipliers (likely >= 1.0x-1.25x) and stay
  flat thereafter.

* A **non-monotonic** curve would favour neither Dan2018 nor Sivyer2013 and would suggest
  kinetic-tiling or electrotonic-overshoot regimes (Espinosa 2010 per t0027).

### The override helper must be copied, not imported, per CLAUDE.md rule

CLAUDE.md rule 9 and the Cross-Task Code Reuse Rule in the research-code specification state that
**only library-registered modules can be imported across tasks**. t0029's `length_override.py` is
NOT a registered library — it lives in `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/`. It
must be **copied** into
`tasks/t0034_distal_dendrite_length_sweep_t0024/code/length_override_ t0024.py` with the
distal-identification rule rewritten to target `cell.terminal_dends` instead of `h.RGC.ON`-filtered
leaves. The snapshot / set / assert helpers (`snapshot_distal_lengths`,
`set_distal_length_multiplier`, `assert_distal_lengths`) transfer verbatim — they operate on a
supplied section list and don't care about arbor names.

### Guardrails against baseline drift remain mandatory

t0029's sweep driver (`run_length_sweep.py:217-229`) [t0029] restores baseline `sec.L` after the
sweep and calls `assert_distal_lengths(multiplier=1.0)` to confirm the override is idempotent. The
same pattern must appear in t0034. Additionally, t0024's trial runner does NOT have a gabaMOD /
BIP-coord drift check (those are t0022/t0008 concepts); the t0034 driver therefore does not need
`_assert_bip_and_gabamod_baseline` — the AR(2) stream is stochastic by design and has no persistent
drift state that would leak across trials.

### Canonical CSV schema and metric keys are already pinned

t0029 writes a tidy sweep CSV with columns
`(length_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)` and per-length
canonical curve CSVs with `(angle_deg, trial_seed, firing_rate_hz)` [t0029]. Both schemas transfer
verbatim — the t0012 scorer accepts the canonical curve schema as-is, and the tidy schema is grouped
by multiplier then scored per group by t0029's `compute_length_metrics.py` [t0029]. The explicit
multi-variant `metrics.json` format (variants keyed `length_0p50`, `length_0p75`, ...,
`length_2p00`) and the three registered metric keys (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`) can be reused without change.

## Reusable Code and Assets

### t0024 DSGC port driver — import via library

* **Source**: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` (~330 lines),
  `run_tuning_curve.py` (~454 lines), `constants.py` (~120 lines), `ar2_noise.py`, `paths.py`.
* **What it does**: Builds the `DSGCCell` dataclass (cell, soma, all_dends, primary_dends,
  non_terminal_dends, terminal_dends, terminal_locs_xy, origin_xy). `run_tuning_curve.py` provides
  the per-trial NEURON driver and the synapse bundle.
* **Reuse method**: **import via library**. The `de_rosenroll_2026_dsgc` library declares these
  files in `module_paths`.
* **Function signatures**:
  * `build_dsgc_cell() -> DSGCCell`
  * `_setup_synapses(*, cell: DSGCCell, gaba_weight_scale: float) -> SynapseBundle`
  * `_bar_arrival_times(syn_xy, origin_xy, direction_deg) -> NDArray`
  * `_rates_with_ar2_noise(*, n_syn, n_bins, rate_dt_ms, arrival_times_ms, rho, seed) -> tuple[NDArray, NDArray]`
  * `_rates_to_events(*, rates_hz, release_prob, rate_dt_ms, rng) -> list[list[float]]`
  * `_gaba_prob_for_direction(direction_deg) -> float`
  * `_count_spikes(v_trace, threshold_mv) -> int`
  * Constants: `BASE_ACH_PROB`, `RATE_DT_MS`, `BAR_SIGMA_MS`, `CELL_PREF_DEG`, `SynapseBundle`.
  * `C.AR2_CROSS_CORR_RHO_CORRELATED = 0.6`, `C.TSTOP_MS = 1000.0`, `C.DT_MS = 0.1`,
    `C.STEPS_PER_MS = 10.0`, `C.V_INIT_MV = -60.0`, `C.AP_THRESHOLD_MV = -10.0`,
    `C.CELSIUS_DEG_C = 36.9`, `C.N_TRIALS_PER_ANGLE = 20` (override to 10), `C.ANGLES_12ANG_DEG`.
* **Adaptation needed**: None for the imported helpers. A thin local `CellContextT0024Length` and
  `run_one_trial_length` will wrap them (copy pattern from [t0026]'s `trial_runner_t0024.py`).

### t0012 tuning-curve scorer — import via library

* **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/` (8 files,
  registered library).
* **What it does**: Load canonical 12-angle CSV; compute DSI, peak, null, HWHM, reliability.
* **Reuse method**: **import via library**.
* **Function signatures** (from `metrics.py` / `loader.py`):
  * `compute_dsi(*, curve: TuningCurve) -> float`
  * `compute_peak_hz(*, curve: TuningCurve) -> float`
  * `compute_null_hz(*, curve: TuningCurve) -> float`
  * `compute_hwhm_deg(*, curve: TuningCurve) -> float`
  * `compute_reliability(*, curve: TuningCurve) -> float | None`
  * `load_tuning_curve(*, csv_path: Path) -> TuningCurve`
  * `TuningCurve(angles_deg, firing_rates_hz, trials)` — frozen dataclass with optional trials
    matrix for split-half reliability.
* **Adaptation needed**: None. Per-length canonical curve CSV -> `load_tuning_curve` ->
  `compute_dsi`/`compute_peak_hz`/etc.

### t0026 t0024 trial-runner pattern — copy into task

* **Source**: `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/trial_runner_t0024.py` (169 lines).
* **What it does**: Imports the t0024 helpers listed above, builds a
  `CellContextT0024(cell, bundle)` once via `build_cell_context()`, and exposes
  `run_one_trial_vrest(ctx, direction_deg, rho, seed, v_rest_mv)` — which interleaves `set_vrest`
  between `h.tstop = C.TSTOP_MS` and `h.finitialize(v_rest_mv)`.
* **Reuse method**: **copy into task** (non-library task code). Adapt to
  `code/trial_runner_length_t0024.py` with these changes:
  1. Rename `CellContextT0024` -> `CellContextT0024Length`, add `distal_sections: list[Any]` and
     `baseline_L: dict[int, float]` fields.
  2. `build_cell_context()` calls `identify_distal_sections_t0024(cell=cell)` and
     `snapshot_distal_lengths(distal_sections=...)` immediately after `build_dsgc_cell()`.
  3. Replace `run_one_trial_vrest(..., v_rest_mv)` with `run_one_trial_length(..., multiplier)`.
     Move `set_distal_length_multiplier` call **outside** the trial loop (the outer sweep caller
     sets it once per multiplier) — the AR(2) driver re-seeds per trial, but `sec.L` is a persistent
     section attribute that does not need per-trial re-application. Still re-assert
     `assert_distal_lengths` once at the start of each outer sweep point as a guard.
  4. Keep `h.finitialize(C.V_INIT_MV)` (the task runs at the default V_rest = -60 mV, not a swept
     value).
* **Line count**: ~180 lines after adaptation.

### t0029 sweep-driver pattern — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/run_length_sweep.py` (239 lines).
* **What it does**: Iterates `LENGTH_MULTIPLIERS x angles_deg x n_trials`, writes tidy CSV one row
  per trial with `fh.flush()`, emits per-length canonical curve CSVs, records wall time per
  multiplier, restores baseline L at the end and asserts idempotence.
* **Reuse method**: **copy into task** (non-library). Adapt to `code/run_sweep_t0024.py`:
  1. Replace t0022 constant imports
     (`tasks.t0022_modify_dsgc_channel_testbed.code.constants.{ANGLE_STEP_DEG, N_ANGLES, N_TRIALS}`)
     with t0024 equivalents. Use `C.ANGLES_12ANG_DEG` directly for the 12-angle grid and define a
     local `N_TRIALS_T0024 = 10` (matching [t0026]).
  2. Replace `build_cell_context` / `run_one_trial_length` imports to point at the new
     `trial_runner_length_t0024` module.
  3. No other structural changes — the tidy CSV schema, per-length curve emit, wall-time JSON, and
     baseline-restore guardrail all transfer verbatim.
* **Line count**: ~240 lines after adaptation.

### t0029 length-override helper — copy into task (with adapter)

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py` (104 lines).
* **What it does**: Identifies HOC distal sections, snapshots baseline `sec.L`, sets
  `sec.L *= multiplier`, and asserts. Current distal rule:
  `sec in h.RGC.ON and h.SectionRef(sec=sec).nchild() == 0`.
* **Reuse method**: **copy into task** as `code/length_override_t0024.py`. The CLAUDE.md cross-task
  import rule forbids importing from a non-library task folder, so the helper must be duplicated.
* **Adaptation needed**: Replace `identify_distal_sections(*, h: Any) -> list[Any]` with
  `identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]` that returns
  `list(cell.terminal_dends)` directly — t0024's `_map_tree` in `build_cell.py:140-168` already
  computes this. Keep `snapshot_distal_lengths`, `set_distal_length_multiplier`, and
  `assert_distal_lengths` verbatim (they operate on supplied section lists).
* **Line count**: ~80 lines after adaptation (the `_on_arbor_section_names` helper becomes
  unnecessary).

### t0029 preflight-distal logger — copy into task (simplified)

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/preflight_distal.py` (149 lines).
* **What it does**: Builds the cell, enumerates distal sections, computes topological depth to soma,
  writes `logs/preflight/distal_sections.json`, asserts `count >= 50` and `min_depth >= 3`.
* **Reuse method**: **copy into task**. Adapt to `code/preflight_distal_t0024.py`:
  1. The depth-computation loop transfers verbatim (it uses `h.SectionRef(sec=sec).parent`, which is
     morphology-agnostic).
  2. `_soma_section_names` must be adapted to pull the soma name from the `DSGCCell.soma` section
     (t0024 exposes `cell.soma` directly, no `h.RGC.soma` indirection needed).
  3. Count and depth gates should be re-evaluated for the t0024 morphology — `RGCmodelGD.hoc` has a
     different topology. Log and warn rather than assert until the expected count range is confirmed
     in the first preflight run.
* **Line count**: ~130 lines after adaptation.

### t0029 per-length metrics reducer — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/compute_length_metrics.py` (291
  lines).
* **What it does**: Groups tidy CSV by multiplier, computes per-group DSI (t0012 scorer, primary),
  vector-sum DSI (secondary), peak Hz, null Hz, HWHM, reliability, preferred-direction angle, and
  mean peak mV. Writes `metrics_per_length.csv` and explicit multi-variant `metrics.json`.
* **Reuse method**: **copy into task** as `code/compute_metrics_t0024.py`. No structural adaptation
  — just rename the t0029 constants import to t0034 equivalents. The three registered metric keys
  are identical.
* **Line count**: ~291 lines after adaptation.

### t0029 curve-shape classifier — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/classify_curve_shape.py` (~170
  lines).
* **What it does**: Reads `metrics_per_length.csv`, runs linear regression of DSI vs multiplier,
  classifies as monotonic / saturating / non-monotonic, writes `curve_shape.json`.
* **Reuse method**: **copy into task** as `code/classify_shape_t0024.py`. No adaptation — same
  classification thresholds (`MONOTONIC_SLOPE_MIN_PER_UNIT = 0.05`, `MONOTONIC_P_MAX = 0.05`,
  `SATURATION_FRACTION_OF_MAX = 0.95`) apply. Expected behaviour on t0024: because the DSI range is
  bounded [0.36, 0.67] (per [t0026]), the classifier should actually produce a meaningful label
  rather than the t0029 outcome where every point pinned at DSI=1.000.
* **Line count**: ~170 lines after adaptation.

### t0029 plot_dsi_vs_length — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/plot_dsi_vs_length.py` (estimated
  ~150 lines based on the [t0029] pattern).
* **What it does**: Two-panel Cartesian plot (DSI left axis, peak Hz right axis, vs multiplier) plus
  a diagnostic polar overlay per length.
* **Reuse method**: **copy into task** as `code/plot_sweep_t0024.py`. No structural adaptation —
  axis labels, output paths, and Okabe-Ito palette transfer verbatim.

### t0029 constants module — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/constants.py` (86 lines).
* **What it does**: Defines `LENGTH_MULTIPLIERS = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`,
  `PREFLIGHT_LENGTH_MULTIPLIERS = (0.5, 1.0, 2.0)`, `PREFLIGHT_ANGLES_DEG = (0, 120, 240)`,
  `PREFLIGHT_N_TRIALS = 2`, tidy-CSV column names, curve-shape thresholds, metric keys,
  `BASELINE_MULTIPLIER = 1.0`, `LENGTH_ASSERT_TOL_UM = 1e-9`.
* **Reuse method**: **copy into task** as `code/constants.py`. Transfer verbatim and add a
  `N_TRIALS_T0024 = 10` constant plus `AR2_RHO = 0.6` alias for clarity. Relax or remove
  `DISTAL_MIN_COUNT = 50` / `DISTAL_MIN_DEPTH = 3` until t0024's actual distal-count distribution is
  measured.

### t0029 paths module — copy into task

* **Source**: `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/paths.py` (52 lines).
* **What it does**: All output paths (`DATA_DIR`, `PER_LENGTH_DIR`, `SWEEP_CSV`, `WALL_TIME_JSON`,
  `METRICS_PER_LENGTH_CSV`, `DISTAL_SECTIONS_JSON`, `DSI_VS_LENGTH_PNG`,
  `per_length_curve_csv(multiplier=...)`, `polar_png(multiplier=...)`).
* **Reuse method**: **copy into task** as `code/paths.py` with `TASK_ID` changed to
  `t0034_distal_dendrite_length_sweep_t0024`. `TASK_ROOT = Path(__file__).resolve().parent.parent`
  anchors correctly out of the box.

## Common Patterns

* **NEURON bootstrap is handled internally by t0024**: `build_cell.py` calls
  `_ensure_neuron_on_path()` and `load_neuron()` internally, so no module-level bootstrap call is
  required (unlike t0022, which requires `ensure_neuron_importable()` at module scope). Keep this
  distinction in the t0034 trial runner — do NOT add a t0022-style bootstrap.
* **Persistent cell context**: `CellContextT0024(cell, bundle)` built once, reused across all
  trials. Pattern from [t0026]:`trial_runner_t0024.py:63-72`.
* **AR(2) rho threading**: `rho=C.AR2_CROSS_CORR_RHO_CORRELATED = 0.6` at every call site. Never
  hardcode `0.0` in the length-sweep runner.
* **Canonical CSV schema**: `(angle_deg, trial_seed, firing_rate_hz)` per-length curve files
  consumed directly by t0012 `load_tuning_curve`.
* **Trial seed convention**: `trial_seed = 1000 * angle_idx + trial_idx + 1` per [t0029]'s
  `run_length_sweep.py:127`. Add the length-multiplier index as an outer prefix
  (`seed = length_idx * 10_000_003 + trial_seed`) to guarantee unique seeds across sweep points.
* **Per-row `fh.flush()`** after each trial so the tidy CSV is crash-recoverable — essential given
  the ~2.8 h total runtime.
* **Explicit multi-variant `metrics.json`**: 7 variants keyed by `length_0p50` ... `length_2p00`,
  each with `dimensions.length_multiplier` and three registered metric keys. Pattern from
  `compute_length_metrics.write_metrics_json` [t0029].

## Lessons Learned

* **t0029's null result traces directly to t0022's zero null firing**: [t0029] `results_summary.md`
  reports `null firing rate = 0 Hz at every multiplier`, which forces `dsi = 1.000`. This is not a
  bug in t0029's driver — it is a property of the t0022 E-I schedule. Running the same sweep on
  t0024 fixes the mechanism because AR(2) noise guarantees non-zero null firing.

* **Building the cell once saves meaningful wall time**: [t0026]'s t0024 sweep took 3.21 h (960
  trials, ~12 s/trial). Re-building the cell per sweep point would add ~1-2 s x 7 = ~10 s, trivial
  relative to total, but introduces a risk that stochastic state differs between sweep points.
  Follow [t0026]'s one-build pattern.

* **t0024's `_setup_synapses` creates NetCons with weight scale = 1.0 (correlated default)**; do not
  pass `gaba_weight_scale=C.GABA_SCALE_UNCORRELATED` unless running the uncorrelated arm. The length
  sweep is single-condition.

* **t0024's trial timing uses `h.run()` not `h.continuerun()`**: unlike t0022's driver,
  `run_single_trial` in t0024 uses `h.run()` after setting `h.tstop`. The trial runner must follow
  this pattern — mixing styles silently breaks the voltage recording.

* **`FInitializeHandler` must be kept alive**: t0024's per-trial
  `fih = h.FInitializeHandler(_queue)` plus `_ = fih` keep-alive line is load-bearing. Without it,
  the events do not land in the NEURON event queue. Preserve exactly in the trial runner.

* **Preflight catches override bugs cheaply**: [t0029]'s 3-multiplier x 3-angle x 2-trial preflight
  (18 trials, ~1 min) validated the override logic before the 840-trial run. t0034 should budget 18
  trials x 12 s = ~4 min for preflight — still well under 10 min and essential before committing to
  the 2.8 h main sweep.

* **Curve-shape thresholds may need recalibration for t0024's DSI range**: [t0029]'s defaults
  (`MONOTONIC_SLOPE_MIN_PER_UNIT = 0.05`, `SATURATION_FRACTION_OF_MAX = 0.95`) were chosen for a
  [0, 1] DSI space. t0024's expected DSI range is [0.36, 0.67], so a slope of 0.05 per unit
  multiplier over a 1.5-unit span represents a 0.075 DSI change — visible but modest relative to the
  0.31 baseline dynamic range. Report the raw slope + CI alongside the class label so a human can
  override if the thresholds are too strict or too loose.

## Recommendations for This Task

### Architecture

1. Four-file code layout mirroring [t0026] + [t0029]:
   * `code/length_override_t0024.py` (~80 lines) — `identify_distal_sections_t0024`,
     `snapshot_distal_lengths`, `set_distal_length_multiplier`, `assert_distal_lengths`.
   * `code/trial_runner_length_t0024.py` (~180 lines) — `CellContextT0024Length`,
     `build_cell_context`, `run_one_trial_length(ctx, direction_deg, seed)`.
   * `code/run_sweep_t0024.py` (~240 lines) — CLI driver, outer sweep loop, tidy CSV, per-length
     curve CSV, wall-time JSON, baseline restore guardrail.
   * `code/compute_metrics_t0024.py` (~290 lines) — per-multiplier DSI / peak / null / HWHM /
     reliability + explicit multi-variant `metrics.json`.
2. Three auxiliary modules:
   * `code/constants.py` (~90 lines) — multipliers, preflight grid, CSV headers, metric keys,
     classifier thresholds. Plus `N_TRIALS_T0024 = 10`, `AR2_RHO = 0.6`.
   * `code/paths.py` (~55 lines) — all output paths.
   * `code/classify_shape_t0024.py` (~170 lines) — DSI-vs-length curve classifier.
   * `code/plot_sweep_t0024.py` (~150 lines) — `dsi_vs_length.png`, `vector_sum_dsi_vs_length.png`,
     `polar_overlay.png`.
   * `code/preflight_distal_t0024.py` (~130 lines) — preflight logger + validation gates.

### Distal-section identification (t0024-specific adapter)

3. Replace t0029's `h.RGC.ON`-based rule with `cell.terminal_dends` directly. t0024's `_map_tree` in
   `build_cell.py:140-168` already returns `terminals, non_terms, order_list[0]` — `terminals`
   **is** the distal-leaf set. Log the count in preflight and compare against the 177 terminals
   mentioned in `run_tuning_curve.py:10-11`.

4. Depth gate: t0024's `_map_tree` computes depth implicitly (it tracks `order_pos`). Leaves are by
   definition at depth >= 1; the [t0029] `DISTAL_MIN_DEPTH = 3` constraint should be verified via
   the same `h.SectionRef(sec=sec).parent` walk as [t0029]. If some leaves turn out to live at depth
   < 3, either (a) filter them out explicitly, or (b) treat the constraint as informational
   (log-only), since terminal dendrites from `_map_tree` are already the biologically correct distal
   set regardless of topological depth.

### Driver wiring

5. **Preserve AR(2) rho = 0.6 at every call site.** In `trial_runner_length_t0024.py`, thread
   `rho=C.AR2_CROSS_CORR_RHO_CORRELATED` as a module-level constant captured once from
   `t0024.constants`. Do NOT accept `rho` as a parameter — hardcoding it guards against accidental
   uncorrelated-arm mixing.

6. Apply `set_distal_length_multiplier` **once per outer sweep point** (before the 120-trial inner
   loop), not per trial. Call `assert_distal_lengths` at the top of every outer iteration as a cheap
   guard. This matches the t0024 biophysics (length is a persistent section attribute, not a
   per-trial resettable property).

7. Seed convention: `seed = length_idx * 10_000_003 + 1000 * angle_idx + trial_idx + 1`. This
   extends [t0029]'s seed rule with a length-index outer prefix so seeds stay unique across the 840
   trials.

### Protocol

8. **12 angles x 10 trials x 7 multipliers = 840 trials**, matching the task description. Use
   `C.ANGLES_12ANG_DEG = (0, 30, 60, ..., 330)` from t0024's constants (no t0022 import).
   `N_TRIALS = 10` (matches [t0026]'s t0024 convention).

9. Budget **~2.8 h wall time** at 12 s/trial; target range 2-4 h. Write tidy CSV rows with
   `fh.flush()` after every trial for crash recovery.

10. Preflight first: `PREFLIGHT_LENGTH_MULTIPLIERS = (0.5, 1.0, 2.0)`,
    `PREFLIGHT_ANGLES_DEG = (0, 120, 240)`, `PREFLIGHT_N_TRIALS = 2`. Total 18 trials x 12 s ~ 4
    min. Validates the override pipeline before the full run.

### Scoring and classification

11. Call `compute_dsi(curve=load_tuning_curve(csv_path=per_length_curve_csv(multiplier=m)))` as the
    **primary DSI** per sweep point. Also emit vector-sum DSI via `_vector_sum_dsi` helper from
    [t0029]'s `compute_length_metrics.py`.

12. Classify the DSI-vs-length curve using [t0029]'s `classify_curve_shape.py` thresholds. Report
    the raw slope + R^2 + p-value alongside the label so a human can override in
    `results_detailed.md` if the 0.36-0.67 DSI range makes the thresholds too loose or too tight.

### Comparison to t0029

13. Include a side-by-side comparison table in `results_detailed.md`: (multiplier, t0029 DSI_pn,
    t0034 primary DSI, t0034 vector-sum DSI) for all 7 points. t0029's DSI_pn column is all 1.000;
    t0034 should show a meaningful curve.

14. In the `compare-literature` step, map the observed curve shape to Dan2018 vs Sivyer2013 as
    predicted in [t0027]. Note that t0029's null result means Sivyer2013's plateau mechanism is
    consistent with either no length effect or a very early saturation — t0034's non-zero null
    firing makes this distinction measurable.

### Guardrails

15. Post-sweep, restore `multiplier=1.0` and call `assert_distal_lengths` to confirm the override is
    idempotent. Pattern from [t0029] `run_length_sweep.py:217-229`.

16. Log distal-section count, depth distribution, and length distribution in
    `logs/preflight/distal_sections.json` — for parity with [t0029] and for post-hoc
    interpretability.

## Task Index

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download candidate DSGC morphology
* **Status**: completed
* **Relevance**: Background context only. t0024 uses the vendored `RGCmodelGD.hoc` under its library
  asset, not the NeuroMorpho SWC produced by t0005.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 DSGC model (12-angle tuning curve)
* **Status**: completed
* **Relevance**: Registers the `modeldb_189347_dsgc` library used by t0022. Not directly imported by
  t0034 (t0024 uses its own HOC template), but provides context for why t0024's morphology differs
  from t0022's.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Tuning-curve response visualization library
* **Status**: completed
* **Relevance**: Provides the `tuning_curve_viz` library with polar / Cartesian / multi-model-
  overlay plot functions. Not directly needed for t0034's primary scalar `dsi_vs_length.png` chart,
  but the polar plot helpers may be used for the diagnostic `polar_overlay.png`.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring and loss library
* **Status**: completed
* **Relevance**: Provides the `tuning_curve_loss` library with `compute_dsi`, `compute_peak_hz`,
  `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`, `load_tuning_curve`, and the
  `TuningCurve` dataclass. Primary DSI scorer for t0034 — one call per sweep point.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC with gabaMOD driver
* **Status**: completed
* **Relevance**: Registers the `modeldb_189347_dsgc_gabamod` library. Sibling DSGC port driven by
  gabaMOD PD/ND scalar swap rather than per-dendrite E-I timing or AR(2) release. Not relevant for
  t0034's biophysics; documented in the Library Landscape for completeness.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC channel testbed for mechanism experiments
* **Status**: completed
* **Relevance**: Reference point for why t0029 got a null result. t0022's deterministic E-I driver
  produces zero null firing, which forces DSI_pn = 1.000. t0034 deliberately runs on t0024 instead.
  Not imported by t0034.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model with AR(2) stochastic release
* **Status**: completed
* **Relevance**: Direct dependency. Provides the `de_rosenroll_2026_dsgc` library with
  `build_dsgc_cell`, `_setup_synapses`, `_rates_with_ar2_noise`, `_gaba_prob_for_direction`,
  `_count_spikes`, all synapse / bar / AR(2) helpers, and the canonical constants
  (`AR2_CROSS_CORR_RHO_CORRELATED = 0.6`, `TSTOP_MS`, `V_INIT_MV`, `ANGLES_12ANG_DEG`, etc.). The
  core driver t0034 imports from.

### [t0026]

* **Task ID**: `t0026_vrest_sweep_tuning_curves_dsgc`
* **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
* **Status**: completed
* **Relevance**: Provides the direct architectural template. `trial_runner_t0024.py` is the model
  for `trial_runner_length_t0024.py`. Establishes the ~12 s/trial wall-time anchor on t0024
  (1400-1580 s per 120-trial V_rest point). Reports DSI range 0.36-0.67 on t0024 vs 0.046-0.66 on
  t0022, demonstrating that primary DSI is a meaningful discriminator on t0024.

### [t0027]

* **Task ID**: `t0027_literature_survey_morphology_ds_modeling`
* **Name**: Literature survey: morphology and direction-selectivity modeling
* **Status**: completed
* **Relevance**: Provides the Dan2018 (passive transfer-resistance weighting, predicts monotonic
  DSI-vs-length) and Sivyer2013 (dendritic-spike branch independence, predicts saturating curve)
  mechanism predictions. Source of the `morphology-direction-selectivity-modeling-synthesis` answer
  asset that anchors the mechanism-discrimination framework for t0034.

### [t0029]

* **Task ID**: `t0029_distal_dendrite_length_sweep_dsgc`
* **Name**: Distal-dendrite length sweep on the t0022 DSGC testbed
* **Status**: completed
* **Relevance**: Direct dependency. Provides the workflow template (constants, paths,
  length_override, sweep driver, metrics reducer, classifier, plot scripts) that t0034 copies with
  the t0024 driver swap. Also provides the null-result baseline for the comparison table in
  `results_detailed.md` — t0029's DSI pinned at 1.000 across all 7 multipliers because t0022's
  deterministic driver silenced the null direction.
