---
spec_version: "2"
task_id: "t0030_distal_dendrite_diameter_sweep_dsgc"
date_completed: "2026-04-22"
status: "complete"
---
# Plan: Distal-Dendrite Diameter Sweep on t0022 DSGC

## Objective

Run a single-parameter sweep of distal-dendrite **diameter** on the already-completed t0022 DSGC
channel testbed (library `modeldb_189347_dsgc_dendritic`) and measure the Direction Selectivity
Index (DSI) at each diameter. The sweep uses seven diameter multipliers — **0.5×, 0.75×, 1.0×,
1.25×, 1.5×, 1.75×, 2.0×** — applied uniformly to every distal branch (operationally: HOC
leaves on the `h.RGC.ON` arbor). At each multiplier, execute the canonical t0022 protocol of 12
moving-bar directions (30° spacing) × 10 trials per direction (120 trials per sweep point, **840
trials total**). DSI is computed via the t0012 `tuning_curve_loss` scorer. The research question is
mechanism discrimination: a **positive** DSI-vs-diameter slope favours **Schachter2010
active-dendrite amplification** (thicker dendrites host more Nav/Kv substrate per unit length and
tip preferred-direction EPSPs over the dendritic-spike threshold more readily); a **negative** slope
favours **passive filtering** (thicker distal dendrites have lower input impedance, damping
directional contrast); flat is inconclusive. Success means producing (a) a tidy sweep CSV with 840
trial rows, (b) seven per-diameter canonical 120-row tuning-curve CSVs, (c) `results/metrics.json`
containing one DSI value per diameter under a multi-variant block, (d) `dsi_vs_diameter.png` and
`vector_sum_dsi_vs_diameter.png` charts, and (e) a mechanism classification (Schachter2010
amplification / passive filtering / flat). All work runs locally on CPU with $0 external cost.

## Task Requirement Checklist

Operative task text from `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/task_description.md`:

> 1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
> 2. Identify distal dendritic sections (tip compartments at branch order >= 3) in the morphology.
> 3. Sweep distal diameter in at least 7 values spanning from 0.5x to 2.0x the baseline diameter
>    (e.g., 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0x). Apply the multiplier to all distal branches
>    uniformly.
> 4. For each diameter value, run the standard 12-direction tuning protocol (15 Hz preferred-
>    direction input) and compute DSI.
> 5. Plot DSI vs diameter and classify slope sign: positive (active-dendrite amplification),
>    negative (passive filtering), flat (neither).
>
> Primary metric: DSI at each diameter value. Secondary (recorded but not primary): per-direction
> spike counts, preferred-direction firing rate, peak voltage at a reference distal compartment.
>
> Key questions: (1) Is the DSI-vs-diameter slope positive, negative, or flat? (2) If positive, is
> the slope consistent with Na+ channel-density amplification as predicted by Schachter2010? (3) If
> negative, does the preferred-direction firing rate drop alongside DSI (consistent with general
> damping) or does only the null-direction rate change?

Requirements:

* **REQ-1**: Use the t0022 testbed as-is — no channel changes, no input rewiring. Only `seg.diam`
  on distal compartments is mutated. Satisfied by steps 3, 4, 5, 7. Evidence: no HOC files are
  modified inside this task; per-trial `_assert_bip_and_gabamod_baseline` guard passes at every
  sweep point; per-trial midpoint-snapshot assertion confirms 3D coordinates are unchanged.
* **REQ-2**: Identify distal dendritic sections at branch order >= 3 (HOC leaves on `h.RGC.ON` with
  topological depth >= 3 from soma). Satisfied by step 3. Evidence:
  `logs/preflight/distal_sections.json` records the section count, min/median/max depth, and
  min/median/max baseline diameter.
* **REQ-3**: Sweep at least 7 multipliers in [0.5, 2.0]; apply uniformly to every distal branch. The
  sweep values are `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`. Satisfied by steps 5, 7. Evidence:
  `DIAMETER_MULTIPLIERS` constant in `code/constants.py`; tidy CSV
  (`results/data/sweep_results.csv`) contains 7 unique `diameter_multiplier` values.
* **REQ-4**: For each multiplier, run the full t0022 12-direction tuning protocol (10 trials per
  angle) and compute DSI via the t0012 scorer. Satisfies by steps 7, 8. Evidence: 840 rows in
  `results/data/sweep_results.csv` (7 × 12 × 10); seven per-diameter canonical CSVs of 120 rows
  each; `results/data/dsi_by_diameter.csv` with one row per multiplier including primary DSI and
  vector-sum DSI; `results/metrics.json` contains one `direction_selectivity_index` value per
  diameter variant.
* **REQ-5**: Plot DSI vs diameter and classify slope sign. Satisfied by steps 9, 10. Evidence:
  `results/images/dsi_vs_diameter.png` exists and is a two-panel plot (DSI + peak Hz vs multiplier);
  `results/images/vector_sum_dsi_vs_diameter.png` exists; `results/data/curve_shape.json` records a
  mechanism label from {`schachter2010_amplification`, `passive_filtering`, `flat`}.
* **REQ-6**: Primary metric is DSI (t0012 peak-minus-null) at each diameter. Satisfied by step 8.
  Evidence: `results/metrics.json` has 7 explicit variants, each with a
  `direction_selectivity_index` entry; `results/data/dsi_by_diameter.csv` lists one DSI per
  multiplier.
* **REQ-7**: Secondary metrics recorded but not primary: per-direction spike counts,
  preferred-direction firing rate, peak voltage at a reference distal compartment. Satisfied by
  steps 7, 8. Evidence: tidy CSV columns `spike_count`, `peak_mv`, `firing_rate_hz`;
  `metrics_per_diameter.csv` records `peak_hz`, `null_hz`, `hwhm_deg`, `dsi_vector_sum`,
  `reliability`, and `mean_peak_mv_distal_reference` per multiplier.
* **REQ-8**: Answer Key Question 1 (slope sign) via `curve_shape.json` field `slope_sign` and
  `mechanism_label`. Satisfied by step 9. Evidence: `slope`, `slope_95_ci_low`, `slope_95_ci_high`,
  `slope_p_value`, `mechanism_label` all present in the JSON.
* **REQ-9**: Answer Key Question 2 — if positive, is the slope consistent with Na+ channel-density
  amplification? Satisfied by step 9 via the `peak_hz` trend and the reported `dsi_range_extremes`
  (expect a positive-monotonic peak-Hz trend if Schachter2010 is the driver). Evidence:
  `curve_shape.json` field `peak_hz_trend_slope` and `dsi_range_extremes`.
* **REQ-10**: Answer Key Question 3 — if negative, does preferred-direction firing rate drop
  alongside DSI, or does only null-direction rate change? Satisfied by step 9 via `curve_shape.json`
  fields `peak_hz_trend_slope` (preferred-direction rate change) and `null_hz_trend_slope`
  (null-direction rate change). Evidence: both slopes saved; if
  `mechanism_label == "passive_filtering"` the JSON additionally stores a boolean
  `preferred_and_null_both_drop` computed from the signs of the two slopes.
* **REQ-11**: Local CPU only, $0 external cost. Satisfied by steps 0-10. Evidence: no setup-machines
  step; no paid API calls; `project/budget.json.available_services` is empty.
* **REQ-12**: Guard against the t0029 "DSI pins at 1.000" plateau. Satisfied by step 8. Evidence:
  `metrics_per_diameter.csv` reports **vector-sum DSI** alongside primary DSI; step 9 fallback rule
  uses vector-sum DSI for slope-sign classification when primary DSI saturates
  (`max - min <= 0.02`).

## Approach

**Task type**: `experiment-run` (set in `task.json`). The task runs a controlled computational
experiment — one independent variable (`diameter_multiplier`, 7 values), one primary dependent
variable (DSI per diameter), a fixed testbed, deterministic driver, and a mechanism-discrimination
research question. The experiment-run Planning Guidelines require naming every independent and
dependent variable, listing baselines, using the explicit multi-variant metrics format when
comparing multiple conditions, and including at least 2 charts. All are applied below.

**Architecture** (from `research/research_code.md`): clone the t0029 four-file architecture. t0029
is the sibling **distal-length** sweep on the same testbed with an identical workflow — only the
overridden geometry attribute differs (`sec.L` vs `seg.diam`). Every non-library module t0030 needs
has a 100-250-line analogue in `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/` that can be
copied verbatim and adapted with a ~20-line delta per file per rule-3 of CLAUDE.md. The t0029 full
sweep completed in **2,541 s ≈ 42 min** on this workstation (same 840-trial protocol); t0030
anticipates **~40-60 min** wall time.

**Distal identification**: define "distal" operationally as HOC leaves on the ON arbor — a section
`sec` is distal iff `sec.name()` appears in the ON arbor (`sec in h.RGC.ON` by name match) AND
`h.SectionRef(sec=sec).nchild() == 0`. The t0029 helper
`identify_distal_sections(*, h: Any) -> list[Any]` in
`tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py:37-52` encodes this exact
rule. Per CLAUDE.md rule-3 (cross-task non-library imports are prohibited and `length_override.py`
is NOT registered in any library), this helper **must be copied verbatim** into
`code/diameter_override.py`. A preflight assertion `min_depth >= 3` (topological depth from soma)
and `count >= 50` is required before the full sweep launches — the same validation gates t0029
used successfully.

**Diameter override rule**: NEURON convention with `forall { nseg=1 }` (from
`RGCmodel.hoc:11817-11818`) means each section has exactly one segment;
`seg.diam = baseline * multiplier` is an unambiguous uniform rescale. Baseline snapshot keys on
`(id(sec), seg.x)` to remain correct if a future task changes `nseg > 1`. 3D point coordinates
(`pt3dadd(x, y, z, d)`) are NOT mutated — diameter rescaling changes local input impedance,
membrane capacitance, and axial resistance but leaves `pair.x_mid_um` / `y_mid_um` stable,
preserving the bar-arrival-time schedule computed in `_compute_onset_times_ms`.

**Reusable code** (imports, not copies) per `research/research_code.md`:

* From `modeldb_189347_dsgc_dendritic` (t0022 library):
  `from tasks.t0022_modify_dsgc_channel_testbed.code.neuron_bootstrap import ensure_neuron_importable`.
  From `tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve` import: `EiPair`,
  `build_ei_pairs`, `schedule_ei_onsets`, `_preload_nrnmech_dll`, `_source_channel_partition_hoc`,
  `_silence_baseline_hoc_synapses`, `_assert_bip_and_gabamod_baseline`,
  `_count_threshold_crossings`. From `tasks.t0022_modify_dsgc_channel_testbed.code.constants`
  import: `TSTOP_MS`, `DT_MS`, `CELSIUS_DEG_C`, `N_ANGLES`, `N_TRIALS`, `ANGLE_STEP_DEG`,
  `AP_THRESHOLD_MV`, `V_INIT_MV`, `BAR_VELOCITY_UM_PER_MS`, `BAR_BASE_ONSET_MS`,
  `AMPA_CONDUCTANCE_NS`, `GABA_CONDUCTANCE_PREFERRED_NS`, `GABA_CONDUCTANCE_NULL_NS`,
  `AMPA_SEG_LOCATION`, `GABA_SEG_LOCATION`.
* From `modeldb_189347_dsgc` (t0008 library):
  `from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc, apply_params, read_synapse_coords, SynapseCoords`.
* From `tuning_curve_loss` (t0012 library):
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve, TuningCurve, METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY)`.
* From `tuning_curve_viz` (t0011 library, optional): `plot_polar_tuning_curve` for per-diameter
  diagnostic polar plots; Okabe-Ito palette from `tuning_curve_viz.constants.OKABE_ITO` for the
  primary scalar-sweep chart.

**Reusable code** (copies into `code/`, structural clones only — per CLAUDE.md rule-3):

* `code/paths.py` — centralised `pathlib.Path` constants (per the Python style guide).
* `code/constants.py` (~60 lines) — local constants:
  `DIAMETER_MULTIPLIERS = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`, tidy-CSV header tuple,
  classification thresholds (`MIN_SLOPE_MAGNITUDE = 0.05`, `MAX_P_VALUE = 0.05`,
  `DSI_SATURATION_THRESHOLD = 0.02`).
* `code/diameter_override.py` (~120 lines) — clone of
  `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py`. Copy
  `identify_distal_sections(*, h)` (lines 37-52) **verbatim**. Rename other symbols:
  `snapshot_distal_lengths` → `snapshot_distal_diameters` (dict keys become `(id(sec), seg.x)` →
  `float(seg.diam)`); `set_distal_length_multiplier` → `set_distal_diameter_multiplier` (iterate
  `for seg in sec` inside each distal section, write `seg.diam = baseline * multiplier`);
  `assert_distal_lengths` → `assert_distal_diameters` (compare `seg.diam` against
  `baseline_diam[(id(sec), seg.x)] * multiplier` within `tol=1e-9` µm).
* `code/preflight_distal.py` (~150 lines) — clone of t0029's `preflight_distal.py`. Call
  `ensure_neuron_importable` → `_preload_nrnmech_dll` → `build_dsgc` →
  `_source_channel_partition_hoc`, then `identify_distal_sections(h=h)`. Assert `len(distal) >= 50`
  and `min_depth >= 3` (via iterative `h.SectionRef(sec=sec).parent` walk until `h.RGC.soma`).
  Snapshot diameters via `snapshot_distal_diameters`. Emit `logs/preflight/distal_sections.json`
  with distal count, min/median/max depth, min/median/max baseline diameter, and total distal
  surface area Σ(π · L · d).
* `code/trial_runner_diameter.py` (~180 lines) — clone of t0029's `trial_runner_length.py`.
  `build_cell_context` runs **once** per process (build cost ~1.6 s) and stores baseline coords,
  baseline `gaba_mod`, baseline distal-diameter snapshot, and per-pair `(x_mid_um, y_mid_um)`
  snapshot.
  `run_one_trial_diameter(*, ctx, distal_sections, baseline_diam, multiplier, angle_deg, trial_idx) -> TrialOutcome`
  interleaves the override sequence in the exact order: `apply_params(h=ctx.h, seed=seed)` →
  `_silence_baseline_hoc_synapses(h=ctx.h)` →
  `_assert_bip_and_gabamod_baseline(h=ctx.h, baseline_coords=ctx.baseline_coords, baseline_gaba_mod=ctx.baseline_gaba_mod)`
  → `set_distal_diameter_multiplier(...)` → `assert_distal_diameters(...)` → midpoint-snapshot
  assertion (compare `pair.x_mid_um`, `pair.y_mid_um` to snapshot within tol 1e-9 µm) →
  `schedule_ei_onsets(...)` → `h.finitialize(V_INIT_MV)` → simulation loop →
  `_count_threshold_crossings` → `TrialOutcome`. Trial seed convention:
  `1000 * angle_idx + trial_idx + 1` (shared with t0022/t0026/t0029 so baseline overlap is exact at
  multiplier = 1.0).
* `code/run_sweep.py` (~240 lines) — clone of t0029's `run_length_sweep.py`. Main driver with CLI
  flags `--preflight`, `--output`, `--wall-time-output`. Replaces outer loop sweep list with
  `DIAMETER_MULTIPLIERS`. Tidy CSV header:
  `(diameter_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`; `fh.flush()`
  after every row (crash recovery). After each outer iteration, emits a per-diameter canonical CSV
  `results/data/per_diameter/tuning_curve_D<label>.csv` with the t0012 schema
  `(angle_deg, trial_seed, firing_rate_hz)`. File labels: `D0p50`, `D0p75`, …, `D2p00`. Emits
  `results/data/wall_time_by_diameter.json`.
* `code/analyse_sweep.py` (~260 lines) — clone of t0029's `compute_length_metrics.py`. Reads the
  tidy CSV, groups by `diameter_multiplier`, calls t0012 scorers on each per-diameter canonical CSV,
  computes **vector-sum DSI** (Mazurek & Kagan 2020 formulation) alongside the primary
  peak-minus-null DSI, also computes `mean_peak_mv_distal_reference` (mean peak V across all distal
  sections' 0.5 location at the preferred direction for the 1.0× midpoint only — used for REQ-7).
  Emits `results/data/metrics_per_diameter.csv`, `results/data/dsi_by_diameter.csv` (a focused
  one-row-per-multiplier table with primary DSI + vector-sum DSI), `results/data/metrics_notes.json`
  (documents why `tuning_curve_rmse` is omitted), and `results/metrics.json` using the explicit
  multi-variant format (one variant per multiplier, `variant_id = "diameter_<m>"`,
  `dimensions = {"diameter_multiplier": <m>}`).
* `code/classify_slope.py` (~100 lines) — clone of t0029's `classify_curve_shape.py`, simplified
  for this task's **ternary mechanism classification**. Fits
  `numpy.polyfit(np.log2(multipliers), dsi, 1)` (slope vs log2-multiplier so the curve is symmetric
  around 1.0×) with a two-tailed t-test for slope != 0. Produces
  `mechanism_label ∈ {"schachter2010_amplification", "passive_filtering", "flat"}`:
  * **positive** slope with p < 0.05 and `dsi_range_extremes >= 0.05` →
    `"schachter2010_amplification"`.
  * **negative** slope with p < 0.05 and `dsi_range_extremes >= 0.05` → `"passive_filtering"`.
  * otherwise → `"flat"`. When primary DSI saturates
    (`max - min <= DSI_SATURATION_THRESHOLD = 0.02`), falls back to vector-sum DSI as the slope-sign
    input. Emits `results/data/curve_shape.json` with `slope`, `slope_95_ci_low`,
    `slope_95_ci_high`, `slope_p_value`, `slope_sign`, `dsi_range_extremes`, `peak_hz_trend_slope`,
    `null_hz_trend_slope`, `preferred_and_null_both_drop` (boolean), `used_fallback_vector_sum_dsi`
    (boolean), and `mechanism_label`.
* `code/plot_sweep.py` (~160 lines) — clone of t0029's `plot_dsi_vs_length.py`. Two outputs:
  * Primary: `results/images/dsi_vs_diameter.png` — two-panel Cartesian, left axis primary DSI vs
    `diameter_multiplier`, right axis peak Hz vs `diameter_multiplier`. Okabe-Ito palette. Annotate
    baseline (1.0×) with a star; overlay a dotted regression line if `mechanism_label != "flat"`.
  * Secondary: `results/images/vector_sum_dsi_vs_diameter.png` — single-panel vector-sum DSI vs
    `diameter_multiplier` (this is the slope-sign diagnostic that survives the t0029 primary-DSI
    plateau).
  * Optional overlay: `results/images/polar_overlay.png` — seven-colour polar overlay of the
    per-diameter tuning curves via `tuning_curve_viz.plot_multi_model_overlay`. This is the visual
    QA view; it is not strictly required for slope-sign classification but is cheap to produce.

**Alternatives considered**:

* **Rebuild the cell per sweep point** rather than mutate `seg.diam` on the live handle. Rejected:
  wastes ~11 s on 7 rebuilds, introduces stochastic cell-build state drift between sweep points, and
  breaks the midpoint-snapshot guard that depends on a single cell instance.
* **Port t0009's Horton-Strahler calculator** to enforce "branch order >= 3" strictly via SWC→HOC
  coordinate matching. Rejected: leaf-dendrite identification with a depth-sanity check covers the
  requirement on this morphology (the ON arbor's shortest soma-to-tip path is longer than 3
  bifurcations — confirmed by the [t0029] preflight that applied the identical rule and passed).
  If the preflight `min_depth >= 3` check fails for t0030, the plan halts via an intervention file.
* **Use vector-sum DSI as the primary metric**. Rejected: the task description explicitly says
  "primary metric: DSI at each diameter value" in the t0022/t0026/t0012 sense (peak-minus-null).
  Vector-sum DSI is computed alongside and serves as the fallback slope-sign diagnostic under
  REQ-12.
* **Sweep `nseg` with `seg.diam`** to maintain `d_lambda` constant. Rejected for the initial run:
  t0008/t0022 HOC uses `forall {nseg=1}`. At the 2.0× endpoint the baseline distal diameter is
  typically ~0.4-1.0 µm, giving a lambda_f well over the segment length, so the `nseg=1` regime
  remains valid. A d_lambda post-check in the preflight records `sec.L / sec.lambda_f` to flag any
  violation (risk row below).

## Cost Estimation

Itemized estimate in USD:

* API calls (LLM / commercial): **$0.00** — no API calls.
* Remote compute (GPU / cloud): **$0.00** — all simulation runs on the local Windows workstation
  CPU.
* Local compute: **$0.00** — already-paid workstation time.
* Storage / network: **$0.00** — all outputs stay on local disk (~50 MB for CSVs + PNGs).
* Registered paid services in `project/budget.json.available_services`: empty list; nothing to spend
  on.

**Total estimated cost: $0.00**.

Project budget is $1.00 USD total, $0.00 currently spent, $1.00 remaining. This task stays within
budget by a wide margin; no cost cap is needed.

## Step by Step

### Milestone A: Setup and preflight

1. **[CRITICAL] Create `code/paths.py` and `code/constants.py`**. Inputs: task description,
   research_code.md. Outputs: `code/paths.py` defines `TASK_ROOT`, `RESULTS_DIR`, `DATA_DIR`,
   `PER_DIAMETER_DIR`, `IMAGES_DIR`, `LOGS_PREFLIGHT_DIR`, `SWEEP_CSV`, `PER_DIAMETER_CSV_TEMPLATE`,
   `METRICS_PER_DIAMETER_CSV`, `DSI_BY_DIAMETER_CSV`, `CURVE_SHAPE_JSON`, `DSI_VS_DIAMETER_PNG`,
   `VECTOR_SUM_DSI_VS_DIAMETER_PNG`, `POLAR_OVERLAY_PNG`, `WALL_TIME_JSON`, `PREFLIGHT_JSON` as
   `pathlib.Path` constants. `code/constants.py` defines
   `DIAMETER_MULTIPLIERS: tuple[float, ...] = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`, typed CSV
   header tuples, and classification thresholds (`MIN_SLOPE_MAGNITUDE = 0.05`, `MAX_P_VALUE = 0.05`,
   `DSI_SATURATION_THRESHOLD = 0.02`, `DSI_RANGE_MIN_FOR_CONFIDENT_LABEL = 0.05`). Expected
   observable output: running
   `uv run python -u -c "from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.constants import DIAMETER_MULTIPLIERS; print(DIAMETER_MULTIPLIERS)"`
   prints the 7-tuple. Satisfies REQ-3, REQ-11.

2. **[CRITICAL] Create `code/diameter_override.py`**. **Copy verbatim** the
   `identify_distal_sections(*, h: Any) -> list[Any]` function from
   `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py:37-52` into this module
   (the rule is geometry-agnostic). Then add three new functions adapted from the t0029 length
   pattern:
   * `snapshot_distal_diameters(*, h: Any, distal_sections: list[Any]) -> dict[tuple[int, float], float]`
     — iterate `for sec in distal_sections: for seg in sec`, store
     `{(id(sec), float(seg.x)): float(seg.diam)}`. Also log baseline min/median/max to the preflight
     file.
   * `set_distal_diameter_multiplier(*, h: Any, distal_sections: list[Any], baseline_diam: dict[tuple[int, float], float], multiplier: float) -> None`
     — iterate
     `for sec in distal_sections: for seg in sec: seg.diam = baseline_diam[(id(sec), seg.x)] * multiplier`.
   * `assert_distal_diameters(*, h: Any, distal_sections: list[Any], baseline_diam: dict[tuple[int, float], float], multiplier: float, tol: float = 1e-9) -> None`
     — verify every `(sec, seg)` satisfies
     `abs(seg.diam - baseline_diam[(id(sec), seg.x)] * multiplier) <= tol`; raise `AssertionError`
     otherwise. Expected observable output: smoke test
     `uv run python -u -c "from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.diameter_override import identify_distal_sections, snapshot_distal_diameters, set_distal_diameter_multiplier, assert_distal_diameters; print('ok')"`
     prints `ok`. Satisfies REQ-2.

3. **[CRITICAL] Preflight: build cell and identify distal sections**. Create
   `code/preflight_distal.py` (~150 lines, cloned from t0029). Call `ensure_neuron_importable()` →
   `_preload_nrnmech_dll()` → `build_dsgc()` once → `_source_channel_partition_hoc(h=h)`. Call
   `identify_distal_sections(h=h)`. Compute the shortest topological depth from soma for every leaf
   via iterative `h.SectionRef(sec=sec).parent` traversal (terminate when parent is `h.RGC.soma`).
   Assert `len(distal) >= 50` and `min_depth >= 3`. Snapshot baseline diameters via
   `snapshot_distal_diameters`. Compute total distal surface area `Σ(π · sec.L · seg.diam)`
   across all distal `(sec, seg)` pairs. Emit `logs/preflight/distal_sections.json`:
   `{ "count": <int>, "min_depth": <int>, "max_depth": <int>, "min_diam_um": <float>, "median_diam_um": <float>, "max_diam_um": <float>, "total_surface_area_um2": <float>, "identification_rule": "hoc_leaves_on_arbor_depth_ge_3" }`.
   **Validation gate (preflight)**: if `min_depth < 3`, STOP — create
   `intervention/distal_identification_fallback.json` explaining the need for a Strahler port and
   halt. Satisfies REQ-2.

### Milestone B: Driver implementation

4. **Create `code/trial_runner_diameter.py`** by cloning t0029's `trial_runner_length.py` (~180
   lines). Swap the override call inside `run_one_trial_length` for `set_distal_diameter_multiplier`
   and rename the function to
   `run_one_trial_diameter(*, ctx, distal_sections, baseline_diam, multiplier, angle_deg, trial_idx) -> TrialOutcome`.
   Preserve the exact override sequence listed in the Approach section. Add a per-trial
   midpoint-snapshot assertion: capture `pair.x_mid_um`, `pair.y_mid_um` once in
   `build_cell_context` and compare at the top of `run_one_trial_diameter` to confirm the diameter
   override did not perturb 3D coordinates (tolerance 1e-9 µm). Function returns
   `TrialOutcome(spike_count: int, peak_mv: float, firing_rate_hz: float)`. Expected observable
   output: module import succeeds. Satisfies REQ-1, REQ-4.

5. **[CRITICAL] Create `code/run_sweep.py`** by cloning t0029's `run_length_sweep.py` (~240 lines).
   Replace `LENGTH_MULTIPLIERS` with `DIAMETER_MULTIPLIERS`; change the tidy-CSV header's first
   column from `length_multiplier` to `diameter_multiplier`; swap the override call signature.
   Preserve `fh.flush()` after every row. After each outer iteration, emit a per-diameter canonical
   CSV at `results/data/per_diameter/tuning_curve_D<label>.csv` with columns
   `(angle_deg, trial_seed, firing_rate_hz)` (t0012 `load_tuning_curve` input format). File labels:
   `D0p50`, `D0p75`, `D1p00`, `D1p25`, `D1p50`, `D1p75`, `D2p00`. Emit per-sweep-point wall time to
   `results/data/wall_time_by_diameter.json`. CLI flags: `--preflight` (runs 3 angles × 2 trials ×
   3 multipliers [0.5, 1.0, 2.0] = 18 trials), `--output`, `--wall-time-output`. Outputs:
   `results/data/sweep_results.csv` (840 rows full run, 18 rows preflight), seven per-diameter
   canonical CSVs, `results/data/wall_time_by_diameter.json`. Satisfies REQ-3, REQ-4, REQ-7.

6. **[CRITICAL] Validation gate: run `run_sweep.py --preflight`**. Execute:
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0030_distal_dendrite_diameter_sweep_dsgc -- uv run python -u -m tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.run_sweep --preflight`.
   Expected runtime: ~1 minute (18 trials).

   **Validation gate thresholds** (expensive-operation gate per the experiment-run guidelines):

   * **Trivial baseline** for the inner check: the t0022 baseline at diameter multiplier 1.0 is DSI
     ~1.0, peak ~15 Hz, null ~0 Hz (deterministic driver, per t0022 and t0029 acceptance). The
     preflight at multiplier 1.0 must reproduce **DSI >= 0.9 and peak Hz >= 12** — anything below
     this means the override leaked into the baseline path.
   * **Inspect 5 individual trial outputs** at `multiplier=1.0, angle=0, trial∈{0,1}` (preferred
     direction in this coord convention after EI scheduling): manually confirm spike count is 12-18.
     If any of the 5 trials returns 0 spikes or > 25 spikes, STOP and debug the override-ordering in
     `run_one_trial_diameter`.
   * **Failure condition**: if preflight DSI at 1.0× <= 0.9 (baseline-equivalent threshold), STOP
     — do not proceed to the full 840-trial sweep. Debug by running `run_one_trial_diameter` on a
     single (angle=0, trial=0, multiplier=1.0) case and comparing its output to t0022/t0029 baseline
     single-trial output (DSI 1.0 at 1.0× is the ground truth from the testbed's own acceptance
     gate). Satisfies REQ-1, REQ-4.

7. **[CRITICAL] Run the full sweep**. Execute:
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0030_distal_dendrite_diameter_sweep_dsgc -- uv run python -u -m tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.run_sweep --output results/data/sweep_results.csv --wall-time-output results/data/wall_time_by_diameter.json`.
   Expected runtime: **~42-60 min** (840 trials, extrapolated from t0029's 2,541 s full-sweep wall
   time at identical protocol). Outputs: `results/data/sweep_results.csv` (841 lines: 1 header + 840
   data rows), seven per-diameter canonical CSVs, and `results/data/wall_time_by_diameter.json`.
   Expected observable output: final-line byte count > 80 000, 840 `direction_deg` rows, 7 distinct
   `diameter_multiplier` values, no NaN `firing_rate_hz`. Post-run: assert all baseline distal
   diameters are restored — call `assert_distal_diameters(..., multiplier=1.0, tol=1e-9)` after
   the sweep. Satisfies REQ-1, REQ-3, REQ-4, REQ-7.

### Milestone C: Metrics and visualisation

8. **Create `code/analyse_sweep.py`** by cloning t0029's `compute_length_metrics.py` (~260 lines).
   Replace `length_multiplier` grouping key with `diameter_multiplier`. For each group, call
   `compute_dsi(curve=load_tuning_curve(csv_path=per_diameter_csv))` on the per-diameter canonical
   CSV from step 5, plus `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`,
   `compute_reliability`. Also compute **vector-sum DSI** via the helper cloned from t0029
   (`_vector_sum_dsi(*, curve)` — implements Mazurek & Kagan 2020: `DSI_vs = |R| / Σ r_i` where
   `R = Σ r_i · e^{i·θ_i}`). For the `diameter_multiplier == 1.0` group additionally compute
   `mean_peak_mv_distal_reference` (mean of `peak_mv` across all 120 trials at 1.0×). Outputs:
   * `results/data/metrics_per_diameter.csv` — columns `diameter_multiplier`,
     `direction_selectivity_index`, `dsi_vector_sum`, `peak_hz`, `null_hz`, `hwhm_deg`,
     `reliability`, `mean_peak_mv`.
   * `results/data/dsi_by_diameter.csv` — focused columns `diameter_multiplier`,
     `direction_selectivity_index`, `dsi_vector_sum` (the REQ-4/REQ-6 deliverable table).
   * `results/data/metrics_notes.json` — records why `tuning_curve_rmse` is omitted (stimulus and
     biophysics identical to t0022 baseline except for `seg.diam`, so RMSE-vs-target is not a
     meaningful metric).
   * `results/metrics.json` — explicit multi-variant format with 7 variants, one per multiplier;
     `variant_id = "diameter_<m>"`, `dimensions = {"diameter_multiplier": <m>}`,
     `metrics = {"direction_selectivity_index": <dsi>, "tuning_curve_hwhm_deg": <hwhm>, "tuning_curve_reliability": <rel>}`.
     Expected observable output: `metrics.json` contains a `variants` key with 7 entries and
     `dsi_by_diameter.csv` has 7 data rows. Satisfies REQ-4, REQ-6, REQ-7, REQ-12.

9. **Create `code/classify_slope.py`** (~100 lines, simplified clone of t0029's
   `classify_curve_shape.py`). Read `results/data/metrics_per_diameter.csv`. Compute:
   * Linear regression of primary DSI vs `log2(multiplier)` via `numpy.polyfit` with residual
     analysis; report `slope`, `slope_95_ci_low`, `slope_95_ci_high`, `slope_p_value` (two-tailed
     t-test for H0: slope = 0).
   * `dsi_range_extremes = dsi_at_2.0 - dsi_at_0.5`.
   * `peak_hz_trend_slope` — linear regression of peak Hz vs `log2(multiplier)`.
   * `null_hz_trend_slope` — linear regression of null Hz vs `log2(multiplier)`.
   * Fallback detection: if `max(dsi) - min(dsi) <= DSI_SATURATION_THRESHOLD = 0.02`, set
     `used_fallback_vector_sum_dsi = True` and re-fit the regression on vector-sum DSI.
   * `mechanism_label`:
     * If `slope > 0`, `slope_p_value < 0.05`, `dsi_range_extremes >= 0.05` →
       `"schachter2010_amplification"`.
     * If `slope < 0`, `slope_p_value < 0.05`, `dsi_range_extremes <= -0.05` →
       `"passive_filtering"`.
     * Otherwise → `"flat"`.
   * If `mechanism_label == "passive_filtering"`, also compute
     `preferred_and_null_both_drop = (peak_hz_trend_slope < 0) and (null_hz_trend_slope <= 0)` (Key
     Question 3 answer). Write `results/data/curve_shape.json` with every field above plus
     `slope_sign ∈ {"+", "-", "~"}` and a one-sentence `qualitative_description`. Also log a
     one-line summary to stdout. Satisfies REQ-5, REQ-8, REQ-9, REQ-10, REQ-12.

10. **Create `code/plot_sweep.py`** (~160 lines). Read `results/data/metrics_per_diameter.csv` and
    `results/data/curve_shape.json`. Produce three charts:
    * **Primary `results/images/dsi_vs_diameter.png`** (two-panel Cartesian, Okabe-Ito palette):
      left axis primary `direction_selectivity_index` (blue, marker + line) vs
      `diameter_multiplier`, right axis `peak_hz` (orange) vs `diameter_multiplier`. Baseline
      (1.0×) annotated with a star. If `mechanism_label != "flat"`, overlay the regression line on
      the DSI panel as a dotted series. 300 dpi, >=20 KB output.
    * **Secondary `results/images/vector_sum_dsi_vs_diameter.png`** (single-panel): vector-sum DSI
      vs `diameter_multiplier` with the regression line; this is the slope-sign diagnostic that
      remains informative even under primary DSI saturation (REQ-12 mitigation).
    * **Diagnostic `results/images/polar_overlay.png`** (optional but strongly recommended via
      `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_multi_model_overlay`):
      overlay of the seven per-diameter tuning curves in a single polar axes. Colours: Okabe-Ito
      7-colour cycle. Expected observable output: `dsi_vs_diameter.png` exists with size > 20 KB;
      `vector_sum_dsi_vs_diameter.png` exists with size > 15 KB; `polar_overlay.png` exists (if
      diagnostics branch ran). Satisfies REQ-5.

## Remote Machines

**None required.** The entire sweep runs on the local Windows workstation CPU. t0029 executed the
identical 840-trial protocol on the same testbed in 2,541 s (~42 min), comfortably under the task
description's 30-90 min envelope. t0030 budgets 840 trials, so expected wall time is **~42-60 min**.
No GPU, no cloud, no paid API.

## Assets Needed

Input assets this task depends on:

* **`modeldb_189347_dsgc_dendritic`** — library asset from t0022. Source:
  `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic/`. Provides
  the HOC model (`RGCmodel.hoc`, `dsgc_model.hoc`), compiled MOD mechanisms (`nrnmech.dll`), the
  per-dendrite E-I driver, the channel-partition HOC overlay (soma/dend/AIS `SectionList`s), the
  canonical constants, the Windows NEURON bootstrap, and the per-trial baseline-drift guardrails.
  All t0022 imports listed in Approach resolve through this asset.
* **`modeldb_189347_dsgc`** — library asset from t0008. Source:
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`. Provides `build_dsgc`,
  `apply_params`, `read_synapse_coords`, `SynapseCoords`.
* **`tuning_curve_loss`** — library asset from t0012. Source:
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`. Provides the
  canonical DSI / peak / null / HWHM / reliability scorer.
* **`tuning_curve_viz`** — library asset from t0011 (optional). Source:
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`. Provides
  `plot_multi_model_overlay` and `plot_polar_tuning_curve`, plus the Okabe-Ito palette.
* **t0029 non-library code** — `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/` files are
  used only as **copy sources** (structural templates); t0030 never imports them.

## Expected Assets

`task.json` declares `expected_assets: {}` — no paper, dataset, library, model, predictions, or
answer assets are produced. This is a pure experiment-run task whose deliverables are metrics,
charts, and the mechanism classification, all of which live under `results/`. The expected output
artefacts (non-assets) are:

* `results/data/sweep_results.csv` — 840 tidy trial rows (7 multipliers × 12 angles × 10
  trials), columns
  `(diameter_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`.
* `results/data/per_diameter/tuning_curve_D<label>.csv` × 7 — canonical 120-row tuning-curve CSVs
  in the t0012 `(angle_deg, trial_seed, firing_rate_hz)` schema.
* `results/data/metrics_per_diameter.csv` — one row per multiplier with primary DSI, vector-sum
  DSI, peak Hz, null Hz, HWHM, reliability, mean peak mV.
* `results/data/dsi_by_diameter.csv` — focused DSI table (`diameter_multiplier`,
  `direction_selectivity_index`, `dsi_vector_sum`).
* `results/data/curve_shape.json` — mechanism label, slope, 95 % CI, p-value, sign, fallback flag,
  peak-Hz trend, null-Hz trend.
* `results/data/wall_time_by_diameter.json` — per-sweep-point wall time.
* `results/data/metrics_notes.json` — RMSE omission rationale.
* `results/metrics.json` — explicit multi-variant format with 7 variants.
* `results/images/dsi_vs_diameter.png` — primary two-panel chart (DSI + peak Hz vs multiplier).
* `results/images/vector_sum_dsi_vs_diameter.png` — secondary single-panel chart.
* `results/images/polar_overlay.png` — optional diagnostic polar overlay of 7 tuning curves.
* `logs/preflight/distal_sections.json` — distal identification rule + counts + diameter
  distribution.

## Time Estimation

* Research: already complete (research_code.md synthesised 11 prior tasks incl. t0029). **0 h**.
* Planning: this document. **~1 h**.
* Implementation (milestones A + B + C, steps 1-10):
  * Milestone A (steps 1-3, setup + preflight): **~45 min coding + ~5 min preflight runtime**.
  * Milestone B step 4 (trial-runner clone): **~30 min coding**.
  * Milestone B step 5 (sweep-driver clone): **~30 min coding**.
  * Milestone B step 6 (preflight sweep run + inspection): **~1 min runtime + ~10 min triage**.
  * Milestone B step 7 (full sweep run): **~42-60 min runtime** (unattended).
  * Milestone C steps 8-10 (metrics + classifier + charts): **~1.5 h coding + <1 min runtime**.
* Validation and coverage check: **~30 min**.

**Total implementation wall time: ~5-6 h** (most of which is unattended simulation time).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Primary DSI pins at 1.000 across the whole sweep (t0029 discovered this on the sibling length axis — null-direction firing is zero at every angle >= 150° from preferred, so peak-minus-null DSI saturates regardless of geometry). | High | Low-Medium | REQ-12 mitigation already baked in: compute vector-sum DSI in parallel and use it as the slope-sign diagnostic when `max(dsi) - min(dsi) <= 0.02` (step 9 fallback). Emit `vector_sum_dsi_vs_diameter.png` unconditionally as the secondary chart. The t0029 sweep showed vector-sum DSI moved 0.021 across 0.5x-2.0x even though primary DSI did not move at all — enough to set the slope sign in most cases. |
| Leaf-dendrite identification returns `min_depth < 3` on the ON arbor (violates "branch order >= 3"). | Low | Medium | Preflight step 3 asserts `min_depth >= 3` and halts by creating `intervention/distal_identification_fallback.json` if it fails. Fallback: port t0009's Horton-Strahler DFS to HOC (~1 day) and re-identify distals as sections with Strahler order >= 3. t0029 passed this gate with the same rule on the same morphology. |
| 2.0x diameter violates d_lambda rule at `nseg=1` (under-resolved spatial discretisation, spurious EPSP shapes). | Low | Low | Preflight step 3 logs per-section `sec.L / sec.lambda_f` at 2.0x as a diagnostic. Post-sweep sanity check in step 7 asserts `sec.L / sec.lambda_f < 0.2` for every distal section at the 2.0x run. If violated, re-run just the 2.0x point with adaptive `nseg` (one-line patch in `set_distal_diameter_multiplier`) and update the corresponding row in `metrics_per_diameter.csv`. |
| NEURON crash or Windows-specific DLL issue during the ~42-60 min unattended run. | Low | High | Crash recovery pattern: tidy CSV is written row-by-row with `fh.flush()` (step 5). On restart, the sweep driver can resume from the last completed `(diameter_multiplier, trial, direction_deg)` tuple. Acceptance: at least 836/840 trials (99.5 %) must succeed; if fewer, halt and debug. |
| Baseline distal `seg.diam` not restored after the sweep, corrupting any downstream use of the live cell handle. | Low | Medium | Post-sweep assertion in step 7 calls `assert_distal_diameters(..., multiplier=1.0, tol=1e-9)`; failure raises `AssertionError`. Additionally, the t0022 per-trial `_assert_bip_and_gabamod_baseline` guard remains enabled across the sweep — independent safety net. |
| Classification thresholds (slope 0.05 per `log2(multiplier)`, p < 0.05) reject a legitimately interpretable curve. | Low-Medium | Low | Classifier emits every underlying quantity (`slope`, `slope_95_ci_low`, `slope_95_ci_high`, `slope_p_value`, `dsi_range_extremes`, `peak_hz_trend_slope`, `null_hz_trend_slope`) regardless of label so a human can override the automatic label in `results_detailed.md`. The JSON output is self-describing. |
| Diameter override perturbs 3D midpoint coordinates, breaking bar-arrival-time schedule. | Very Low | High | NEURON does not mutate 3D points when `seg.diam` is assigned (documented in `research_code.md`). Step 4 adds a per-trial midpoint-snapshot assertion (`pair.x_mid_um`, `pair.y_mid_um` compared to build-time snapshot within 1e-9 µm) that fires if this invariant is ever violated. |

## Verification Criteria

Testable checks run at the end of implementation (all commands use the Windows worktree prefix
`cd "C:/Users/md1avn/Documents/GitHub/neuron-channels-worktrees/t0030_distal_dendrite_diameter_sweep_dsgc" &&`
and `PYTHONIOENCODING=utf-8 PYTHONUTF8=1` where required for aggregators/verificators):

* Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0030_distal_dendrite_diameter_sweep_dsgc -- uv run python -u -m arf.scripts.verificators.verify_plan t0030_distal_dendrite_diameter_sweep_dsgc`;
  expect zero errors.
* Run
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open( 'tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/data/sweep_results.csv'))); assert len(rows) == 840, len(rows); assert len({r['diameter_multiplier'] for r in rows}) == 7; print('OK', len(rows))"`;
  expect `OK 840` (confirms REQ-3 and REQ-4).
* Run
  `uv run python -u -c "import json, pathlib; m = json.loads(pathlib.Path( 'tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/metrics.json').read_text()); assert 'variants' in m and len(m['variants']) == 7; assert all('direction_selectivity_index' in v['metrics'] for v in m['variants']); print('OK')"`;
  expect `OK` (confirms REQ-4 and REQ-6 — DSI present for all 7 variants).
* Run
  `uv run python -u -c "import pathlib; p = pathlib.Path( 'tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/images/dsi_vs_diameter.png'); assert p.exists() and p.stat().st_size > 20000; print('OK', p.stat().st_size)"`;
  expect `OK <size>` with size > 20 000 bytes (confirms REQ-5 primary plot exists).
* Run
  `uv run python -u -c "import pathlib; p = pathlib.Path( 'tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/images/vector_sum_dsi_vs_diameter.png'); assert p.exists() and p.stat().st_size > 15000; print('OK', p.stat().st_size)"`;
  expect `OK <size>` > 15 000 (confirms REQ-5 secondary plot + REQ-12 vector-sum fallback rendered).
* Run
  `uv run python -u -c "import json, pathlib; s = json.loads(pathlib.Path( 'tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/data/curve_shape.json').read_text()); assert s['mechanism_label'] in ('schachter2010_amplification','passive_filtering','flat'); print('OK', s['mechanism_label'])"`;
  expect `OK <label>` (confirms REQ-5, REQ-8, REQ-9, REQ-10 classification).
* Run
  `uv run python -u -c "import json, pathlib; p = json.loads(pathlib.Path( 'tasks/t0030_distal_dendrite_diameter_sweep_dsgc/logs/preflight/distal_sections.json').read_text()); assert p['min_depth'] >= 3 and p['count'] >= 50; print('OK', p['count'], p['min_depth'])"`;
  expect `OK <count> <min_depth>` (confirms REQ-2).
* Run
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open( 'tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/data/dsi_by_diameter.csv'))); assert len(rows) == 7; assert all('dsi_vector_sum' in r for r in rows); print('OK', len(rows))"`;
  expect `OK 7` (confirms REQ-6 and REQ-12 — vector-sum column present).
* Run
  `uv run ruff check --fix . && uv run ruff format . && uv run mypy tasks/t0030_distal_dendrite_diameter_sweep_dsgc`;
  expect zero errors.
* REQ-coverage check: every `REQ-*` ID in `## Task Requirement Checklist` appears in at least one
  numbered step. Run
  `uv run python -u -c "import re, pathlib; t = pathlib.Path( 'tasks/t0030_distal_dendrite_diameter_sweep_dsgc/plan/plan.md').read_text(); reqs = set(re.findall(r'REQ-\d+', t)); print(sorted(reqs))"`;
  expect at least
  `['REQ-1','REQ-2','REQ-3','REQ-4','REQ-5','REQ-6','REQ-7','REQ-8','REQ-9','REQ-10', 'REQ-11','REQ-12']`.
