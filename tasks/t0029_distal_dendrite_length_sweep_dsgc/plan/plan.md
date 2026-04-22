---
spec_version: "2"
task_id: "t0029_distal_dendrite_length_sweep_dsgc"
date_completed: "2026-04-22"
status: "complete"
---
# Plan: Distal-Dendrite Length Sweep on t0022 DSGC

## Objective

Perform a single-parameter sweep of distal-dendrite length on the existing t0022 DSGC channel
testbed (library `modeldb_189347_dsgc_dendritic`) and measure the Direction Selectivity Index (DSI)
at each length. The sweep uses seven length multipliers (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0) of
the baseline distal-compartment length. At each multiplier, run the canonical t0022 protocol of 12
moving-bar directions (30 deg spacing) x 10 trials per direction (120 trials per sweep point, 840
trials total). DSI is computed via the t0012 `tuning_curve_loss` scorer. Outcome: a DSI-vs-length
curve that discriminates Dan2018 (passive transfer-resistance weighting, predicts monotonic
increase) from Sivyer2013 (dendritic-spike branch independence, predicts saturation). Success means
producing (a) a tidy sweep CSV with 840 trial rows, (b) seven per-length canonical 120-row
tuning-curve CSVs, (c) `results/metrics.json` containing one DSI value per length under a
multi-variant block, (d) a `dsi_vs_length.png` two-panel chart, and (e) a curve-shape classification
(monotonic / saturating / non-monotonic). All work runs locally on CPU with $0 external cost.

## Task Requirement Checklist

Operative task text from `tasks/t0029_distal_dendrite_length_sweep_dsgc/task_description.md`:

> 1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
> 2. Identify distal dendritic sections (tip compartments at branch order >= 3) in the morphology.
> 3. Sweep distal length in at least 7 values spanning from 0.5x to 2.0x the baseline length (e.g.,
>    0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0x). Use the same sweep step size for all branches.
> 4. For each length value, run a full 12-direction tuning protocol (standard t0022 protocol with 15
>    Hz preferred-direction input) and compute DSI.
> 5. Plot DSI vs length and classify the curve shape as monotonic / saturating / non-monotonic.
> 6. Report the fitted slope (for monotonic), the saturation length (for saturating), or describe
>    the qualitative shape (for non-monotonic).
>
> Primary metric: DSI at each length value.
>
> Key questions: (1) Is DSI monotonically increasing with distal length, or does it saturate? (2) At
> what length does saturation occur (if any)? (3) Is the DSI range at the sweep extremes (0.5x and
> 2.0x) large enough to distinguish the mechanisms, or does the testbed saturate at our default
> length?

Requirements:

* **REQ-1**: Use the t0022 testbed as-is — no channel changes, no input rewiring. Only `sec.L` on
  distal compartments is mutated. Satisfied by steps 3, 4, 5. Evidence: preflight log confirms the
  imported t0022 library modules are untouched and no HOC files are modified in this task; per-trial
  `_assert_bip_and_gabamod_baseline` guard passes at every sweep point.
* **REQ-2**: Identify distal dendritic sections at branch order >= 3. Satisfied by step 3. Evidence:
  `logs/preflight/distal_sections.json` records the section count and the criterion used.
* **REQ-3**: Sweep at least 7 multipliers in [0.5, 2.0]; use the same multiplier for all distal
  branches. The sweep values are `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`. Satisfied by steps 5, 6.
  Evidence: `LENGTH_MULTIPLIERS` constant in `code/constants.py`; tidy CSV contains 7 unique
  `length_multiplier` values.
* **REQ-4**: For each multiplier, run the full t0022 12-direction tuning protocol (10 trials per
  angle) and compute DSI via the t0012 scorer. Satisfied by steps 6, 7. Evidence: 840 rows in
  `results/data/sweep_results.csv` (7 x 12 x 10); seven per-length canonical CSVs of 120 rows each;
  `results/metrics.json` contains one `direction_selectivity_index` value per length variant.
* **REQ-5**: Plot DSI vs length and classify the curve shape. Satisfied by steps 8, 9. Evidence:
  `results/images/dsi_vs_length.png` exists and is a two-panel plot (DSI + peak Hz vs multiplier);
  classification JSON in `results/data/curve_shape.json` records one of {`monotonic`, `saturating`,
  `non_monotonic`}.
* **REQ-6**: Report fitted slope, saturation length, or qualitative shape depending on
  classification. Satisfied by step 9. Evidence: `results/data/curve_shape.json` carries `slope` and
  `slope_p_value` for monotonic, `saturation_multiplier` and `plateau_dsi` for saturating, or
  `qualitative_description` for non-monotonic.
* **REQ-7**: Key question answers must be computable from the sweep outputs. Satisfied by step 9.
  Evidence: `curve_shape.json` answers Q1 (monotonic vs saturating) via `shape_class`; Q2
  (`saturation_multiplier`); Q3 — the DSI range across extremes (`dsi_at_0.5` vs `dsi_at_2.0`) is
  saved in the same JSON.
* **REQ-8**: Primary metric is DSI; secondary (recorded but not primary) are per-direction spike
  counts and preferred-direction firing rate. Satisfied by steps 6, 7. Evidence: tidy CSV columns
  include `spike_count`, `peak_mv`, `firing_rate_hz`; metrics JSON records
  `direction_selectivity_index` per variant and stores the preferred-direction peak as
  `tuning_curve_rmse` is omitted (see step 7).
* **REQ-9**: Local CPU only, no remote machines, $0 external cost. Satisfied by steps 0-9. Evidence:
  no setup-machines step; no paid-API calls.

## Approach

**Task type**: `experiment-run` (already set in `task.json`). The task runs a controlled
computational experiment — one independent variable (`length_multiplier`, 7 values), one primary
dependent variable (DSI per length), a fixed testbed, deterministic driver, and a mechanism-
discrimination research question. The experiment-run Planning Guidelines require naming every
independent and dependent variable, listing baseline comparisons, and using the explicit multi-
variant metrics format when the task compares multiple conditions (here, multiple length points).
All three are applied below.

**Architecture** (from `research/research_code.md`): clone the t0026 V_rest-sweep architecture. That
task swept a single scalar (`V_rest`) on the same t0022 testbed and produced a two-panel Cartesian
DSI+peak plot. t0029 is a structural analogue with `L` in place of `V_rest`: the driver reuses the
same build-once cell context, the same per-trial tidy CSV schema with `fh.flush()` per row, the same
override-then-finitialize ordering, and the same per-sweep-value reducer pattern. Only the override
target differs (`sec.L` on distal compartments instead of `seg.eleak_HHst` / `seg.e_pas` on all
sections).

**Distal identification**: the task description says "tip compartments at branch order >= 3". The
t0022 HOC morphology builds its section tree with `connect dend[i](0), dend[i-1](1)` style
statements and stores 282 ON dendrites in `h.RGC.ON`. We define "distal" operationally as HOC leaf
dendrites: any section in `h.RGC.dends` with `h.SectionRef(sec=sec).nchild() == 0` AND belonging to
the ON arbor (intersection with `h.RGC.ON`). HOC leaves are always at depth >= branch-point count
from the soma, which on this morphology exceeds 3 for every ON leaf (the ON arbor has at least three
bifurcations between soma and any terminal tip — confirmed in step 3 preflight). If the preflight
reveals any leaves at depth < 3, we fall back to a depth-labelled walk that enforces depth >= 3
strictly. This is recorded in `logs/preflight/distal_sections.json`.

**Reusable code** (imports, not copies):

* From t0022 library (`modeldb_189347_dsgc_dendritic`, registered module_paths):
  `from tasks.t0022_modify_dsgc_channel_testbed.code.neuron_bootstrap import ensure_neuron_importable`.
  From `tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve` import: `EiPair`,
  `build_ei_pairs`, `schedule_ei_onsets`, `_preload_nrnmech_dll`, `_source_channel_partition_hoc`,
  `_silence_baseline_hoc_synapses`, `_assert_bip_and_gabamod_baseline`,
  `_count_threshold_crossings`. From `tasks.t0022_modify_dsgc_channel_testbed.code.constants`
  import: `TSTOP_MS`, `DT_MS`, `CELSIUS_DEG_C`, `N_ANGLES`, `N_TRIALS`, `ANGLE_STEP_DEG`,
  `AP_THRESHOLD_MV`, `V_INIT_MV`, `BAR_VELOCITY_UM_PER_MS`, `BAR_BASE_ONSET_MS`,
  `AMPA_CONDUCTANCE_NS`, `GABA_CONDUCTANCE_PREFERRED_NS`, `GABA_CONDUCTANCE_NULL_NS`,
  `AMPA_SEG_LOCATION`, `GABA_SEG_LOCATION`.
* From t0008 library (`modeldb_189347_dsgc`):
  `from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc, apply_params, read_synapse_coords, SynapseCoords`.
* From t0012 library (`tuning_curve_loss`):
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import ( compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, load_tuning_curve, TuningCurve)`.
* From t0011 library (`tuning_curve_viz`): `plot_polar_tuning_curve` for optional diagnostic
  per-length polar plots.

**Reusable code** (copies into `code/`, structural clones only):

* `code/length_override.py` (~60 lines) — clone of
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/vrest_override.py`. Functions:
  `identify_distal_sections(*, h) -> list`,
  `snapshot_distal_lengths(*, h, distal_sections) -> dict [int, float]`,
  `set_distal_length_multiplier(*, h, distal_sections, baseline_L, multiplier) -> None`,
  `assert_distal_lengths(*, h, distal_sections, baseline_L, multiplier, tol=1e-9) -> None`.
* `code/trial_runner_length.py` (~170 lines) — clone of
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/trial_runner_t0022.py`. Replaces
  `run_one_trial_vrest` with `run_one_trial_length`. The only behavioural change is that the
  override call inserts `set_distal_length_multiplier` between `apply_params` and `h.finitialize`;
  all other sequencing is preserved.
* `code/run_length_sweep.py` (~180 lines) — clone of
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/run_vrest_sweep_t0022.py`. Swaps the outer sweep
  list for `LENGTH_MULTIPLIERS`, changes the CSV header's first column from `v_rest_mv` to
  `length_multiplier`, and emits seven per-length canonical CSVs in addition to the tidy sweep CSV.
* `code/compute_length_metrics.py` (~260 lines) — clone of
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/compute_vrest_metrics.py`. Groups the tidy CSV by
  `length_multiplier` and computes DSI via `compute_dsi` (t0012 scorer) plus HWHM, peak, null.
* `code/plot_dsi_vs_length.py` (~100 lines) — clone of the summary-plot function in
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/plot_polar_tuning.py`. Two-panel Cartesian: left
  axis DSI, right axis peak Hz; x-axis is the length multiplier.
* `code/classify_curve_shape.py` (~80 lines, new code written for this task). Reads the per-length
  metrics CSV and classifies the DSI-vs-length curve as monotonic, saturating, or non-monotonic per
  the REQ-5 thresholds. Writes `results/data/curve_shape.json`.
* `code/constants.py` (~50 lines) — task-local constants:
  `LENGTH_MULTIPLIERS = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`, output paths, CSV column names, and
  the classification thresholds (`MONOTONIC_SLOPE_MIN_PER_UNIT = 0.05`, `MONOTONIC_P_MAX = 0.05`,
  `SATURATION_FRACTION_OF_MAX = 0.95`).
* `code/paths.py` — centralised path constants per the Python style guide.

**Alternatives considered**:

* **Rebuild the cell per sweep point** rather than mutate `sec.L` on the live handle. Rejected:
  wastes ~11 s on 7 rebuilds, introduces potential cell-build state drift between sweep points, and
  breaks the baseline-midpoint-snapshot guard that depends on a single cell instance.
* **Port t0009's Horton-Strahler calculator to HOC** to enforce "branch order >= 3" strictly via
  SWC->HOC coordinate matching. Rejected for the initial run: leaf-dendrite identification with a
  depth-sanity check covers the requirement on this morphology (the ON arbor's shortest soma-to- tip
  path is longer than 3 bifurcations). If the depth check fails in preflight, the plan escalates to
  the Strahler port via an intervention file.
* **Use the vector-sum DSI convention** (t0026's `_vector_sum_dsi`) as the primary metric. Rejected:
  the task description says "compute DSI consistently with t0022/t0026", which both use the t0012
  peak-minus-null scorer as the primary DSI. The vector-sum DSI is still computed alongside as a
  diagnostic in `compute_length_metrics.py` but is not the primary metric.
* **Sweep `nseg` in addition to `L`** to keep d_lambda constant. Rejected for the initial run:
  t0008/t0022 HOC uses `forall {nseg=1}`, so `nseg` stays at 1 throughout the sweep. We log a
  d_lambda post-check and, if the 2.0x endpoint violates the rule (lambda_f < 0.05 * L * 10 per
  segment), we re-run that single length with adaptive `nseg` as a follow-up — but it does not
  block the main sweep.

## Cost Estimation

Itemized estimate in USD:

* API calls (LLM / commercial): $0.00 — no API calls.
* Remote compute (GPU / cloud): $0.00 — all simulation runs on the local Windows workstation CPU.
* Local compute: $0.00 — already-paid workstation time.
* Storage / network: $0.00 — all outputs stay on local disk (~50 MB for CSVs + PNGs).
* Registered paid services in `project/budget.json.available_services`: empty list; nothing to spend
  on.

**Total estimated cost: $0.00**.

Project budget is $1.00 USD total, $0.00 currently spent, $1.00 remaining. This task stays within
budget by a wide margin; no cost cap is needed.

## Step by Step

### Milestone A: Setup and preflight

1. **[CRITICAL] Create `code/paths.py` and `code/constants.py`**. Inputs: task description,
   research_code.md. Outputs: `code/paths.py` (defines `TASK_ROOT`, `RESULTS_DIR`, `DATA_DIR`,
   `IMAGES_DIR`, `LOGS_PREFLIGHT_DIR`, `SWEEP_CSV`, `PER_LENGTH_CSV_TEMPLATE`,
   `METRICS_PER_LENGTH_ CSV`, `CURVE_SHAPE_JSON`, `DSI_VS_LENGTH_PNG`) and `code/constants.py`
   (`LENGTH_MULTIPLIERS`, `MONOTONIC_SLOPE_MIN_PER_UNIT = 0.05`, `MONOTONIC_P_MAX = 0.05`,
   `SATURATION_FRACTION_OF_MAX = 0.95`,
   `TIDY_CSV_HEADER = ("length_multiplier","trial","direction_deg","spike_count","peak_mv","firing_rate_hz")`).
   Expected output: running
   `uv run python -c "from tasks.t0029_distal_dendrite_length_sweep_dsgc.code.constants import LENGTH_MULTIPLIERS; print(LENGTH_MULTIPLIERS)"`
   prints the 7-tuple. Satisfies REQ-3.

2. **[CRITICAL] Copy and adapt `length_override.py`**. Copy
   `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/vrest_override.py` to
   `code/length_override. py`. Rename symbols: `set_vrest` -> `set_distal_length_multiplier`; remove
   `seg.eleak_HHst` and `seg.e_pas` mutation; add `sec.L = baseline_L[idx] * multiplier`. Add four
   new functions:
   * `identify_distal_sections(*, h) -> list` — iterate `h.RGC.dends`; for each section, check
     `h.SectionRef(sec=sec).nchild() == 0`; intersect with `h.RGC.ON` membership via section-name
     matching (`sec.name()` appears in `[s.name() for s in h.RGC.ON]`). Return the filtered list.
   * `snapshot_distal_lengths(*, h, distal_sections) -> dict[int, float]` — return
     `{id(sec): float(sec.L) for sec in distal_sections}` keyed by `id()` (stable within one
     process). Also compute baseline min/median/max/total distal length for logging.
   * `set_distal_length_multiplier(*, h, distal_sections, baseline_L, multiplier) -> None` — for
     each distal section, set `sec.L = baseline_L[id(sec)] * multiplier`.
   * `assert_distal_lengths(*, h, distal_sections, baseline_L, multiplier, tol=1e-9) -> None` —
     verify every distal section's current `sec.L` equals `baseline_L[id(sec)] * multiplier` within
     `tol`; raise `AssertionError` if not. Inputs: read t0026 source. Outputs:
     `code/length_override.py` (~60 lines). Expected: unit- smoke test
     `uv run python -c "from tasks.t0029_distal_dendrite_length_sweep_dsgc.code. length_override import identify_distal_sections; print(identify_distal_sections)"`
     succeeds without import errors. Satisfies REQ-2.

3. **[CRITICAL] Preflight: build cell and identify distal sections**. Create
   `code/preflight_distal.py` (~80 lines). Call `ensure_neuron_importable()`,
   `_preload_nrnmech_dll()`, `build_dsgc()` once, then `_source_channel_partition_hoc(h=h)`. Call
   `identify_distal_sections(h=h)` and assert `len(distal_sections) >= 50`. Also compute the
   shortest path-depth from soma to each leaf via an iterative HOC walk
   (`h.SectionRef(sec=sec).parent` until reaching `h.RGC.soma`); assert `min_depth >= 3`. Snapshot
   baseline lengths and compute min/median/max/total. Write `logs/preflight/distal_sections.json`:
   `{ "count": <int>, "min_depth": <int>, "max_depth": <int>, "min_L_um": <float>, "median_L_um": <float>, "max_L_um": <float>, "total_L_um": <float>, "identification_rule": "hoc_leaves_on_arbor_depth_ge_3" }`.
   **Validation gate (preflight)**: if `min_depth < 3`, STOP — create
   `intervention/distal_identification_fallback.json` explaining the need for a Strahler port and
   halt. Satisfies REQ-2.

### Milestone B: Driver implementation

4. **Copy and adapt `trial_runner_length.py`**. Copy
   `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/trial_runner_t0022.py` to
   `code/trial_runner_length.py` (~170 lines). Replace the `set_vrest(h=h, v_rest_mv=v_rest_mv)`
   call inside `run_one_trial_vrest` with
   `set_distal_length_multiplier(h=h, distal_sections=distal_sections, baseline_L=baseline_L, multiplier=multiplier)`
   and rename the function to
   `run_one_trial_length(*, ctx, distal_sections, baseline_L, multiplier, angle_deg, trial_idx)`.
   Preserve the exact ordering: `apply_params(h=ctx.h, seed=seed)` ->
   `_silence_baseline_hoc_synapses(h=ctx.h)` ->
   `_assert_bip_and_gabamod_baseline(h=ctx.h, baseline_coords=ctx.baseline_coords, baseline_gaba_mod=ctx.baseline_gaba_mod)`
   -> `set_distal_length_multiplier(...)` -> `assert_distal_lengths(...)` ->
   `schedule_ei_onsets(...) ` -> `h.finitialize(V_INIT_MV)` -> simulation loop -> spike count. Trial
   seed convention: `1000 * angle_idx + trial_idx + 1` (same as t0022/t0026). Output: function
   returns `TrialResult(spike_count: int, peak_mv: float, firing_rate_hz: float)`. Expected output:
   importable without errors. Satisfies REQ-1 (no input rewiring), REQ-4.

5. **[CRITICAL] Copy and adapt `run_length_sweep.py`**. Copy
   `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/run_vrest_sweep_t0022.py` to
   `code/run_length_sweep.py` (~180 lines). Replace `V_REST_VALUES_MV` outer loop with
   `LENGTH_MULTIPLIERS`. Change the tidy-CSV header first column from `v_rest_mv` to
   `length_multiplier`. Keep `fh.flush()` after every row for crash recovery. After each outer
   iteration, also emit a per-length canonical CSV at
   `results/data/per_length/tuning_curve_L<multiplier>.csv` with columns
   `(angle_deg, trial_seed, firing_rate_hz)` (the schema accepted by t0012 `load_tuning_curve`).
   Emit per-sweep-point wall time to `results/data/wall_time_by_length. json`. CLI flags:
   `--preflight` (run 3 angles x 2 trials x 3 multipliers [0.5, 1.0, 2.0] only), `--output`. Inputs:
   none besides the imports. Outputs: `results/data/sweep_results.csv` (840 rows in full run, 18
   rows in preflight), seven per-length canonical CSVs, `results/data/wall_time_by_length.json`.
   Satisfies REQ-3, REQ-4, REQ-8.

6. **[CRITICAL] Validation gate: run `run_length_sweep.py --preflight`**. Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0029_distal_dendrite_length_sweep_dsgc -- uv run python -u -m tasks.t0029_distal_dendrite_length_sweep_dsgc.code.run_length_sweep --preflight`.
   Expected runtime: ~1 minute (18 trials). Expected observable output: 18 tidy-CSV rows with
   non-NaN `firing_rate_hz`, three per-length canonical CSVs emitted.

   **Validation gate thresholds** (expensive-operation gate per the experiment-run guidelines):

   * **Trivial baseline** for the inner check: the t0022 baseline at length multiplier 1.0 is DSI
     1.0, peak 15 Hz, null 0 Hz (deterministic driver). The preflight must reproduce DSI >= 0.9 and
     peak Hz >= 12 at the 1.0x midpoint — anything below this means the override leaked into the
     baseline path.
   * **Inspect 5 individual trial outputs** at `1.0x, angle=120 deg` (preferred): manually confirm
     spike count is 13-17 (baseline is 15 for a deterministic run). If any of the 5 trials returns 0
     spikes or > 25 spikes, STOP and debug the override-ordering in `run_one_trial_length`.
   * **Failure condition**: if preflight DSI at 1.0x <= 0.9 (baseline-equivalent threshold), STOP
     — do not proceed to the full 840-trial sweep. Debug by running `run_one_trial_length` on a
     single (angle=0, trial=0, multiplier=1.0) case and comparing its output to t0022's baseline
     single-trial output (DSI 1.0 at 1.0x is the ground truth from the testbed's own acceptance
     gate). Satisfies REQ-1, REQ-4.

7. **[CRITICAL] Run the full sweep**. Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0029_distal_dendrite_length_sweep_dsgc -- uv run python -u -m tasks.t0029_distal_dendrite_length_sweep_dsgc.code.run_length_sweep --output results/data/sweep_results.csv`.
   Expected runtime: ~52 minutes (840 trials at ~3.75 s/trial, per t0026 benchmarks). Inputs: t0022
   library. Outputs: `results/data/sweep_results.csv` (841 lines: 1 header + 840 data rows), seven
   per-length canonical CSVs in `results/data/per_length/`, and
   `results/data/wall_time_by_length.json`. Expected observable output: final-line byte count >
   80000, 840 `direction_deg` values, 7 distinct `length_multiplier` values, no NaN
   `firing_rate_hz`. Post-run: assert all baseline distal `sec.L` values are restored (call
   `assert_distal_lengths(..., multiplier=1.0)` after the sweep). Satisfies REQ-3, REQ-4, REQ-8.

### Milestone C: Metrics and visualisation

8. **Copy and adapt `compute_length_metrics.py`**. Copy
   `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/compute_vrest_metrics.py` to
   `code/compute_length_metrics.py` (~260 lines). Replace `v_rest_mv` grouping key with
   `length_multiplier`. For each group, call
   `compute_dsi(curve=load_tuning_curve( csv_path=per_length_csv))` on the per-length canonical CSV
   emitted in step 5, and `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`. Keep the
   `_vector_sum_dsi` helper and report it under column `dsi_vector_sum`; mark the t0012 scorer's DSI
   as the primary `direction_selectivity_index`. Additionally emit `results/metrics.json` using the
   explicit multi-variant format — one variant per sweep point with `variant_id = "length_<m>"`,
   `dimensions = {"length_multiplier": <m>}`,
   `metrics = {"direction_selectivity_index": <dsi>, "tuning_curve_hwhm_deg": <hwhm>, "tuning_curve_reliability": <rel>}`.
   Intentionally omit `tuning_curve_rmse` because t0022's RMSE-vs-target metric is not meaningful
   when the stimulus/biophysics are unchanged except for `sec.L`; record the omission rationale in
   `results/data/metrics_notes.json` (a small file created by this same script). Outputs:
   `results/data/metrics_per_length.csv`, `results/data/metrics_notes.json`, `results/metrics.json`.
   Expected observable output: `metrics.json` contains a `variants` key with 7 entries. Satisfies
   REQ-4, REQ-5, REQ-8.

9. **Classify DSI-vs-length curve shape**. Create `code/classify_curve_shape.py` (~80 lines). Read
   `results/data/metrics_per_length.csv`. Compute:
   * Linear regression of DSI vs multiplier using `numpy.polyfit` with residual analysis; record
     `slope`, `intercept`, `r_squared`, and a two-tailed t-test p-value for non-zero slope.
   * `saturation_multiplier`: smallest multiplier m* such that `dsi(m) >= 0.95 * max(dsi)` for all m
     > = m*.
   * `dsi_range_extremes` = `dsi[2.0] - dsi[0.5]`.
   * Classify as:
     * `monotonic` if DSI is non-decreasing across consecutive multipliers AND slope >= 0.05 AND
       p-value < 0.05.
     * `saturating` if `saturation_multiplier <= 1.25` AND max(dsi) - dsi(m >= saturation_
       multiplier) <= 0.05.
     * `non_monotonic` otherwise. Output: `results/data/curve_shape.json` =
       `{"shape_class": <str>, "slope": <float>, "p_value": <float>, "saturation_multiplier": <float|null>, "plateau_dsi": <float|null>, "dsi_range_extremes": <float>, "qualitative_description": <str>}`.
       Also log a one-line summary to stdout. Satisfies REQ-5, REQ-6, REQ-7.

10. **Plot DSI vs length**. Create `code/plot_dsi_vs_length.py` (~100 lines, cloned from the summary
    function of `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/plot_polar_tuning.py`). Read
    `results/data/metrics_per_length.csv`. Plot two Cartesian axes sharing the x-axis (length
    multiplier): left axis `direction_selectivity_index` (blue, from Okabe-Ito palette), right axis
    `peak_hz` (orange). Overlay vertical dashed line at `saturation_multiplier` if classification is
    `saturating`. Overlay the regression line if classification is `monotonic`. Annotate baseline
    (1.0x) with a star. Save to `results/images/dsi_vs_length.png` at 300 dpi. Also emit seven
    optional diagnostic polar plots to `results/images/polar_L<multiplier>.png` using
    `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve`
    with the per-length canonical CSV as input. Expected observable output:
    `results/images/dsi_vs_length.png` exists with file size > 20 KB; seven `polar_L*.png` files
    exist. Satisfies REQ-5.

## Remote Machines

**None required.** The entire sweep runs on the local Windows workstation CPU. t0026 executed a
similar-scale sweep (960 V_rest trials) locally in ~60 minutes. The t0029 sweep budgets 840 trials,
so expected wall time is ~50-55 minutes — comfortably under the task description's 30-90 minute
envelope. No GPU, no cloud.

## Assets Needed

Input assets this task depends on:

* **`modeldb_189347_dsgc_dendritic`** — library asset from t0022. Source:
  `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic/`. Provides
  the HOC model (`RGCmodel.hoc`, `dsgc_model.hoc`), compiled MOD mechanisms (`nrnmech. dll`), the
  E-I driver, the channel-partition overlay, the NEURON bootstrap, the canonical constants, and the
  baseline-drift guardrails. All imports above resolve through this asset.
* **`modeldb_189347_dsgc`** — library asset from t0008. Source:
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`. Provides `build_dsgc`,
  `apply_params`, `read_synapse_coords`, `SynapseCoords`.
* **`tuning_curve_loss`** — library asset from t0012. Source:
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`. Provides the
  canonical DSI / peak / null / HWHM scorer.
* **`tuning_curve_viz`** — library asset from t0011 (optional). Source:
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`. Provides
  `plot_polar_tuning_curve` for diagnostic per-length polar plots.

## Expected Assets

`task.json` declares `expected_assets: {}` — no paper, dataset, library, model, predictions, or
answer assets are produced. This is a pure experiment-run task whose deliverables are metrics,
charts, and the curve-shape classification, all of which live under `results/`. The expected output
artefacts (non-assets) are:

* `results/data/sweep_results.csv` — 840 tidy trial rows (7 multipliers x 12 angles x 10 trials).
* `results/data/per_length/tuning_curve_L<m>.csv` x 7 — canonical 120-row tuning-curve CSVs.
* `results/data/metrics_per_length.csv` — one row per length with DSI, peak, null, HWHM,
  reliability, vector-sum DSI.
* `results/data/curve_shape.json` — classification, slope/p-value, saturation multiplier,
  qualitative description.
* `results/data/wall_time_by_length.json` — per-sweep-point wall time.
* `results/metrics.json` — explicit multi-variant format with 7 variants.
* `results/images/dsi_vs_length.png` — primary two-panel chart.
* `results/images/polar_L<m>.png` x 7 — optional diagnostic polar plots.
* `logs/preflight/distal_sections.json` — distal identification rule + counts + length
  distribution.

## Time Estimation

* Research: already complete (research_code.md synthesised 9 prior tasks; no further research
  needed). 0 hours.
* Planning: this document. ~1 hour.
* Implementation (milestones A + B + C, steps 1-10):
  * Milestone A (steps 1-3, setup + preflight): ~1 hour coding + ~5 min runtime.
  * Milestone B step 4 (driver clone): ~40 minutes coding.
  * Milestone B step 5 (sweep driver clone): ~40 minutes coding.
  * Milestone B step 6 (preflight sweep run): ~1 minute runtime + ~10 minutes triage.
  * Milestone B step 7 (full sweep run): ~55 minutes runtime (unattended).
  * Milestone C steps 8-10 (metrics + classification + charts): ~1.5 hours coding + <1 minute
    runtime.
* Validation and coverage check: ~30 minutes.

**Total implementation wall time: ~6 hours** (most of which is unattended simulation time).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| DSI pins at 1.0 across the whole sweep (t0022 baseline is already DSI=1.0 — `research_code.md` flags this as a real possibility). | Medium | Low-Medium | Compute peak Hz and null Hz per length in addition to DSI (step 8). If DSI is saturated at 1.0 even at 0.5x, the peak/null delta vs length still distinguishes Dan2018 (peak increases) from Sivyer2013 (peak plateaus). The plan emits both and reports both; the `dsi_vs_length.png` chart has a peak-Hz panel on the right axis specifically for this case. |
| Leaf-dendrite identification returns depth < 3 for some leaf (violates "branch order >= 3"). | Low | Medium | Preflight step 3 asserts `min_depth >= 3` and halts by creating `intervention/distal_identification_fallback.json` if it fails. Fallback: port t0009's Horton-Strahler DFS to HOC (adds ~1 day) and re-identify distals as sections with Strahler order >= 3. |
| 2.0x length violates d_lambda rule (under-resolved segmentation at coarse `nseg=1`). | Medium | Low | Preflight log records per-section `sec.lambda_f` at 2.0x; post-sweep sanity check in step 7 asserts `sec.L / sec.lambda_f < 0.2` for every distal section at the 2.0x run. If violated, re-run just the 2.0x point with adaptive `nseg` (one-line patch in `set_distal_length_multiplier`) and update the corresponding row in `metrics_per_length.csv`. |
| NEURON crash or Windows-specific DLL issue during the ~55 min unattended run. | Low | High | Crash recovery pattern: tidy CSV is written row-by-row with `fh.flush()` (step 5). On restart, the sweep driver can resume from the last completed `(length_multiplier, trial, direction_deg)` tuple. Acceptance: at least 836/840 trials (99.5%) must succeed; if fewer, halt and debug. |
| Baseline distal `sec.L` not restored after sweep, corrupting any downstream use of the live cell handle. | Low | Medium | Post-sweep assertion in step 7 calls `assert_distal_lengths(..., multiplier=1.0)` with `tol=1e-9`; failure raises `AssertionError`. Additionally, the t0022 per-trial `_assert_bip_and_gabamod_baseline` guard remains enabled across the sweep — gives an independent safety net. |
| Classification thresholds (slope 0.05, saturation 0.95x max by 1.25x) reject a legitimately interpretable curve. | Low-Medium | Low | Classification logic emits every underlying quantity (`slope`, `p_value`, `saturation_multiplier`, `plateau_dsi`, `dsi_range_extremes`) regardless of category so a human can override the automatic label in `results_detailed.md`. The JSON output is self-describing. |

## Verification Criteria

Testable checks run at the end of implementation:

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0029_distal_dendrite_length_sweep_dsgc -- uv run python -u -m arf.scripts.verificators.verify_plan t0029_distal_dendrite_length_sweep_dsgc`;
  expect zero errors.
* Run
  `uv run python -u -c "import csv, pathlib; rows = list(csv.DictReader(open('tasks/ t0029_distal_dendrite_length_sweep_dsgc/results/data/sweep_results.csv'))); assert len(rows) == 840, len(rows); assert len({r['length_multiplier'] for r in rows}) == 7; print('OK', len(rows))"`;
  expect `OK 840` (confirms REQ-3 and REQ-4).
* Run
  `uv run python -u -c "import json, pathlib; m = json.loads(pathlib.Path('tasks/t0029_distal_dendrite_length_sweep_dsgc/results/metrics.json'). read_text()); assert 'variants' in m and len(m['variants']) == 7; assert all( 'direction_selectivity_index' in v['metrics'] for v in m['variants']); print('OK')"`;
  expect `OK` (confirms REQ-4 and REQ-8 — DSI present for all 7 variants).
* Run
  `uv run python -u -c "import pathlib; p = pathlib.Path('tasks/ t0029_distal_dendrite_length_sweep_dsgc/results/images/dsi_vs_length.png'); assert p.exists(); assert p.stat().st_size > 20000; print('OK', p.stat().st_size)"`;
  expect `OK <size>` with size
  > 20000 bytes (confirms REQ-5 plot exists).
* Run
  `uv run python -u -c "import json, pathlib; s = json.loads(pathlib.Path('tasks/t0029_distal_dendrite_length_sweep_dsgc/results/data/ curve_shape.json').read_text()); assert s['shape_class'] in ('monotonic','saturating', 'non_monotonic'); print('OK', s['shape_class'])"`;
  expect `OK <class>` (confirms REQ-5, REQ-6, REQ-7 classification).
* Run
  `uv run python -u -c "import json, pathlib; p = json.loads(pathlib.Path('tasks/t0029_distal_dendrite_length_sweep_dsgc/logs/preflight/ distal_sections.json').read_text()); assert p['min_depth'] >= 3 and p['count'] >= 50; print('OK', p['count'], p['min_depth'])"`;
  expect `OK <count> <min_depth>` (confirms REQ-2).
* Run
  `uv run ruff check --fix . && uv run ruff format . && uv run mypy tasks/t0029_distal_dendrite_length_sweep_dsgc`;
  expect zero errors and zero warnings.
* REQ-coverage check: every `REQ-*` ID in the `## Task Requirement Checklist` is mentioned in at
  least one numbered step (`## Step by Step`). Run
  `uv run python -u -c "import re, pathlib; t = pathlib.Path('tasks/t0029_distal_dendrite_length_sweep_dsgc/plan/plan.md').read_text(); reqs = set(re.findall(r'REQ-\d+', t)); print(sorted(reqs))"`;
  expect at least `['REQ-1','REQ-2', 'REQ-3','REQ-4','REQ-5','REQ-6','REQ-7','REQ-8','REQ-9']`.
