---
spec_version: "2"
task_id: "t0034_distal_dendrite_length_sweep_t0024"
date_completed: "2026-04-23"
status: "complete"
---
# Plan: Distal-Dendrite Length Sweep on t0024 DSGC

## Objective

Run a single-parameter sweep of distal-dendrite length on the **t0024 de Rosenroll 2026 DSGC port**
(library `de_rosenroll_2026_dsgc`, registered at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/`)
and measure the Direction Selectivity Index (DSI) at each length. The sweep uses seven length
multipliers (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0) of the baseline distal-compartment length
`sec.L`. At each multiplier, run the canonical 12-direction tuning protocol (12 angles x 10 trials
per angle = 120 trials per sweep point, 840 trials total) and compute primary DSI (peak-minus-null
via the t0012 `tuning_curve_loss` scorer) plus vector-sum DSI as a defensive fallback. The task
discriminates Dan2018 passive transfer-resistance weighting (monotonic DSI increase with length)
from Sivyer2013 dendritic-spike branch independence (saturating DSI curve). Success means producing:
(a) a tidy sweep CSV with 840 trial rows, (b) seven per-length canonical 120-row tuning-curve CSVs,
(c) `results/metrics.json` with seven length variants, (d) primary-DSI and vector-sum-DSI vs length
charts, (e) a polar overlay of all seven tuning curves, and (f) a curve-shape classification
(monotonic / saturating / non-monotonic). All work runs locally on CPU with $0 external cost.
Anticipated wall time ~2.8 h.

## Task Requirement Checklist

Operative task text from `tasks/t0034_distal_dendrite_length_sweep_t0024/task_description.md`:

> 1. Use the **t0024 de Rosenroll 2026 DSGC port** as-is (no channel modifications, no input
>    rewiring). Keep the AR(2) correlation rho=0.6 at its t0026 V_rest-sweep default.
> 2. Identify distal dendritic sections (HOC leaves on `h.RGC.ON` arbor). Mirror the selection rule
>    from t0029's `length_override.py:37-52` but COPY the helper into this task's
>    `code/length_override_t0024.py` - no cross-task imports per CLAUDE.md.
> 3. Sweep distal length in 7 values spanning 0.5x to 2.0x baseline (0.5, 0.75, 1.0, 1.25, 1.5,
>    1.75, 2.0x). Apply the multiplier uniformly to all distal branches.
> 4. For each length value, run the standard 12-direction tuning protocol (12 angles x 10 trials)
>    and compute primary DSI as the operative metric. Also emit vector-sum DSI and secondary metrics
>    as t0029 did.
> 5. Plot primary DSI vs length and classify the curve shape: monotonic (favours Dan2018),
>    saturating (favours Sivyer2013), or non-monotonic (neither or kinetic-tiling).
>
> Primary metric: primary DSI (peak-minus-null) at each length value.
>
> Secondary: vector-sum DSI, peak Hz, null Hz, HWHM, reliability, preferred-direction firing rate.
>
> Key questions: (1) Is primary DSI monotonically increasing with distal length (Dan2018),
> saturating (Sivyer2013), or non-monotonic (neither)? (2) At what length does saturation occur (if
> any)? (3) Does the t0024 AR(2) noise broaden the HWHM enough to mask the mechanism signal? (4) How
> do the t0024 and t0022 results compare under identical sweep protocols?

Requirements:

* **REQ-1**: Use the t0024 DSGC port as-is - no channel modifications, no input rewiring, no AR(2)
  correlation changes. Only `sec.L` on distal compartments is mutated. Satisfied by steps 4-9.
  Evidence: no edits to any file under `tasks/t0024_port_de_rosenroll_2026_dsgc/`; the
  `rho=C.AR2_CROSS_CORR_RHO_CORRELATED` constant is captured once at module scope in
  `trial_runner_length_t0024.py` and never overridden; the per-trial runner only calls the imported
  t0024 helpers and the t0034-local distal overrides.

* **REQ-2**: Identify distal dendritic sections in the t0024 morphology. Mirror the t0029 selection
  *intent* (HOC leaves on the ON arbor at sufficient depth) but use t0024's topology walk - t0024
  has NO `h.RGC.ON` attribute; `cell.terminal_dends` from `DSGCCell` is the biologically correct
  distal-leaf set computed by `_map_tree` in `build_cell.py:140-168`. Satisfied by steps 2, 3.
  Evidence: `logs/preflight/distal_sections.json` records count, depth distribution, and length
  distribution; `code/distal_selector_t0024.py` uses `cell.terminal_dends`, not `h.RGC.ON`.

* **REQ-3**: Copy the length-override helper into this task (no cross-task imports per CLAUDE.md
  rule 9). Satisfied by step 2. Evidence: `code/length_override_t0024.py` exists as a standalone
  file with `snapshot_distal_lengths`, `set_distal_length_multiplier`, `assert_distal_lengths`; no
  `from tasks.t0029_...` imports appear in any t0034 file (grep-verified in Verification Criteria).

* **REQ-4**: Sweep 7 multipliers in [0.5, 2.0]; apply uniformly to all distal branches. Values:
  `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`. Satisfied by steps 5, 6, 7. Evidence:
  `LENGTH_MULTIPLIERS` constant in `code/constants.py`; `sweep_results.csv` contains exactly 7
  distinct `length_multiplier` values; `set_distal_length_multiplier` applies the same multiplier to
  every distal section in one pass.

* **REQ-5**: For each multiplier, run the 12-direction protocol (12 angles x 10 trials) and compute
  primary DSI via the t0012 scorer. Satisfied by steps 6, 7, 8. Evidence: 840 rows in
  `results/data/sweep_results.csv` (7 x 12 x 10); seven per-length canonical CSVs of 120 rows each;
  `results/metrics.json` variants each carry one `direction_selectivity_index` value computed by
  `compute_dsi(curve=load_tuning_curve(...))`.

* **REQ-6**: Preserve AR(2) correlation rho=0.6 at every call site. Satisfied by steps 4, 5, 6, 7.
  Evidence: `code/trial_runner_length_t0024.py` captures `rho=C.AR2_CROSS_CORR_RHO_CORRELATED` at
  module scope and does not accept `rho` as a parameter; no call site hardcodes `0.0` or an
  alternative rho.

* **REQ-7**: Also emit vector-sum DSI and secondary metrics (peak Hz, null Hz, HWHM, reliability,
  preferred-direction firing rate). Satisfied by step 8. Evidence:
  `results/data/metrics_per_length.csv` contains columns `dsi_primary`, `dsi_vector_sum`, `peak_hz`,
  `null_hz`, `hwhm_deg`, `reliability`, `preferred_direction_deg`, `preferred_hz`.

* **REQ-8**: Plot primary DSI vs length and classify the curve shape. Satisfied by steps 9, 10.
  Evidence: `results/images/dsi_vs_length.png` exists; `results/data/curve_shape.json` carries
  `shape_class` in `{"monotonic", "saturating", "non_monotonic"}` plus `slope`, `p_value`,
  `saturation_multiplier`.

* **REQ-9**: Emit vector-sum DSI as defensive fallback chart (per t0029/t0030 learning that primary
  DSI can pin at 1.0 under deterministic drivers). Satisfied by step 10. Evidence:
  `results/images/vector_sum_dsi_vs_length.png` exists as secondary chart - even if primary DSI pins
  at 1.0 on t0024 (unlikely but possible if AR(2) null firing is too sparse at some sweep points),
  the vector-sum chart still resolves directional structure.

* **REQ-10**: Produce a polar overlay of all 7 tuning curves (12-direction firing rate vs angle).
  Satisfied by step 10. Evidence: `results/images/polar_overlay.png` exists and contains seven
  coloured lines, one per length multiplier.

* **REQ-11**: Produce a peak-Hz-vs-length diagnostic chart. Satisfied by step 10. Evidence:
  `results/images/peak_hz_vs_length.png` exists and shows peak firing rate across multipliers.

* **REQ-12**: Classify curve shape as monotonic (favours Dan2018), saturating (favours Sivyer2013),
  or non-monotonic (neither / kinetic-tiling). Satisfied by step 9. Evidence: `curve_shape.json`
  `shape_class` value plus a qualitative description in `qualitative_description`.

* **REQ-13**: Incremental checkpointing - crash recovery via per-row `fh.flush()`. Satisfied by step
  7\. Evidence: `run_sweep.py` opens the tidy CSV in append mode with line-buffering and calls
  `fh.flush()` after every trial; partial run leaves a parseable CSV.

* **REQ-14**: Local CPU only, no remote machines, $0 external cost. Satisfied by all steps.
  Evidence: no `setup-machines` step; no paid-API calls; `plan/plan.md` Remote Machines section is
  "None required".

* **REQ-15**: Primary DSI is the operative discriminator on t0024 (unlike t0029 where it pinned at
  1.000 because t0022's deterministic driver silenced the null direction). Satisfied by step 8.
  Evidence: `metrics_per_length.csv` `null_hz` column is expected to be non-zero (bounded away from
  0\) at every sweep point because t0024's AR(2) stochastic release produces measurable
  null-direction firing; t0026's V_rest sweep on t0024 reports DSI range 0.36-0.67 confirming the
  discriminator has dynamic range.

## Approach

**Task type**: `experiment-run` (already set in `task.json`). The experiment-run Planning Guidelines
require naming every independent and dependent variable, using the explicit multi-variant metrics
format when comparing multiple conditions, specifying baselines, and running a preflight validation
gate before expensive simulation. All four are applied below.

**Independent variable**: `length_multiplier` in `{0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0}` (7 levels,
same multiplier for every distal branch).

**Primary dependent variable**: primary DSI (peak-minus-null via t0012 scorer) at each length.

**Secondary dependent variables**: vector-sum DSI, peak Hz, null Hz, HWHM, reliability,
preferred-direction firing rate, mean peak mV.

**Fixed conditions**: AR(2) correlation rho=0.6 (`C.AR2_CROSS_CORR_RHO_CORRELATED`), V_rest = -60 mV
(`C.V_INIT_MV`), `h.tstop = C.TSTOP_MS = 1000` ms, `C.DT_MS = 0.1`, `C.CELSIUS_DEG_C = 36.9`,
12-angle grid `C.ANGLES_12ANG_DEG = (0, 30, ..., 330)`, 10 trials per angle, correlated-condition
synapse setup (`gaba_weight_scale=1.0`), AP threshold -10 mV. No channel modifications, no input
rewiring, no uncorrelated-arm mixing.

**Architecture** (from `research/research_code.md`): clone the t0026 V_rest-sweep architecture that
already ran on the t0024 port. That task swept a single scalar (`V_rest`) on the t0024 testbed and
produced a two-panel plot. The t0034 sweep is a structural analogue with `L` in place of `V_rest`:
the driver reuses the build-once cell context, the same per-trial tidy CSV schema with `fh.flush()`
per row, the same per-sweep-value reducer pattern. The key behavioural change is that
`set_distal_length_multiplier` is called **once per outer sweep point** (not per trial) because
`sec.L` is a persistent section attribute, whereas t0026's `set_vrest` had to run per trial (before
`h.finitialize`) because V_rest is re-initialised every trial.

**Distal identification (t0024-specific)**: t0029's `identify_distal_sections` at
`length_override.py:37-52` iterates `h.RGC.dends` and filters to HOC leaves on `h.RGC.ON`. This
works on t0022's `RGCmodel.hoc` which has separate ON/OFF arbors. **t0024's `RGCmodelGD.hoc` has NO
`h.RGC.ON` attribute** - it defines a single `h.DSGC` cell with a unified dendritic arbor. Walking
`h.RGC.ON` on t0024 raises `AttributeError`. The biologically equivalent set is already computed by
`build_cell._map_tree`: `DSGCCell.terminal_dends` is the list of HOC leaves (sections with no child
via `h.SectionRef(sec=sec).nchild() == 0`). This list is returned directly by
`identify_distal_sections_t0024(*, cell) -> list[Any]` as `list(cell.terminal_dends)`. Depth >= 3 is
verified in preflight via the same iterative parent walk as t0029 but logged-only (not asserted)
until t0024's actual depth distribution is measured - `RGCmodelGD.hoc` has a different topology and
the hard gate may need recalibration.

**Reusable code (imports, not copies) - all via registered libraries**:

* From `de_rosenroll_2026_dsgc` library (t0024):
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell, DSGCCell`;
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve import (_setup_synapses, _bar_arrival_times, _rates_with_ar2_noise, _rates_to_events, _gaba_prob_for_direction, _count_spikes, SynapseBundle, BASE_ACH_PROB, RATE_DT_MS)`;
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C`. C provides
  `AR2_CROSS_CORR_RHO_CORRELATED = 0.6`, `TSTOP_MS`, `DT_MS`, `STEPS_PER_MS`, `V_INIT_MV`,
  `AP_THRESHOLD_MV`, `CELSIUS_DEG_C`, `ANGLES_12ANG_DEG`.
* From `tuning_curve_loss` library (t0012):
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve, TuningCurve)`.
* From `tuning_curve_viz` library (t0011, optional):
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve`
  for the polar overlay diagnostic.

**Reusable code (copies into `code/`, per CLAUDE.md rule 9)**:

* `code/paths.py` (~55 lines) - copied from
  `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/paths.py`, `TASK_ID` rewritten to
  `t0034_distal_dendrite_length_sweep_t0024`. Adds `VECTOR_SUM_DSI_VS_LENGTH_PNG`,
  `POLAR_OVERLAY_PNG`, `PEAK_HZ_VS_LENGTH_PNG` for the new secondary charts.
* `code/constants.py` (~90 lines) - copied from t0029 with `N_TRIALS_T0024 = 10` and `AR2_RHO = 0.6`
  aliases added. `DISTAL_MIN_COUNT` and `DISTAL_MIN_DEPTH` are relaxed to warn-only thresholds
  (logged in preflight JSON, not hard-asserted) until t0024's distal distribution is measured.
* `code/distal_selector_t0024.py` (~50 lines) - the t0024-specific distal selector. Single function
  `identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]` returning
  `list(cell.terminal_dends)`. **Deliberately NOT using `h.RGC.ON`** - that attribute does not exist
  on the t0024 morphology.
* `code/length_override_t0024.py` (~60 lines) - copied from t0029's `length_override.py` MINUS the
  `identify_distal_sections` and `_on_arbor_section_names` helpers (those move to
  `distal_selector_t0024.py`). Keeps `snapshot_distal_lengths`, `set_distal_length_multiplier`,
  `assert_distal_lengths` verbatim (they operate on a supplied section list).
* `code/preflight_distal.py` (~130 lines) - copied from t0029's `preflight_distal.py`. Adapt: (a)
  build the DSGCCell via `build_dsgc_cell()`, (b) call `identify_distal_sections_t0024(cell=...)`,
  (c) compute depth via `h.SectionRef(sec=sec).parent` walk (transfers verbatim), (d) warn rather
  than assert on `min_depth < 3` or `count < 50` until thresholds are recalibrated for
  `RGCmodelGD.hoc`.
* `code/trial_runner_length_t0024.py` (~180 lines) - copied from t0026's
  `trial_runner_t0024.py:63-72` pattern. Adapt: (a) rename `CellContextT0024` ->
  `CellContextT0024Length`, add `distal_sections`, `baseline_L`, `current_multiplier` fields; (b) in
  `build_cell_context`, call `identify_distal_sections_t0024` and `snapshot_distal_lengths` after
  `build_dsgc_cell` + `_setup_synapses`; (c) drop the `v_rest_mv` parameter; (d) replace
  `run_one_trial_vrest` with `run_one_trial_length(*, ctx, direction_deg, trial_seed)` that does NOT
  mutate `sec.L` (the outer sweep driver handles that); (e) thread
  `rho=C.AR2_CROSS_CORR_RHO_CORRELATED` captured once at module scope; (f) preserve the
  `FInitializeHandler` keep-alive line (`_ = fih`) - without it the event queue is empty, a silent
  failure mode.
* `code/run_sweep.py` (~240 lines) - copied from t0029's `run_length_sweep.py`. Adapt: (a) replace
  t0022 imports with t0024 equivalents; (b) use `C.ANGLES_12ANG_DEG` directly (no t0022
  `ANGLE_STEP_DEG / N_ANGLES` imports); (c) local `N_TRIALS_T0024 = 10`; (d) call the new
  `trial_runner_length_t0024.run_one_trial_length`; (e) before each outer sweep iteration, call
  `set_distal_length_multiplier(distal_sections=..., baseline_L=..., multiplier=m)` then
  `assert_distal_lengths(..., multiplier=m)` as a guard; (f) post-sweep, restore `multiplier=1.0`
  and assert idempotence.
* `code/analyse_sweep.py` (~290 lines) - copied from t0029's `compute_length_metrics.py`. No
  structural adaptation - just rename the t0029 paths import to t0034 `paths.py`. Emits primary DSI
  (t0012 scorer), vector-sum DSI (helper `_vector_sum_dsi` from t0029), peak Hz, null Hz, HWHM,
  reliability, preferred-direction angle + firing rate, and mean peak mV into
  `metrics_per_length.csv` and `results/metrics.json` (explicit multi-variant, 7 variants).
* `code/classify_shape.py` (~170 lines) - copied from t0029's `classify_curve_shape.py`. Reads
  `metrics_per_length.csv` and runs the classifier (monotonic / saturating / non-monotonic) using
  the same thresholds (`MONOTONIC_SLOPE_MIN_PER_UNIT = 0.05`, `MONOTONIC_P_MAX = 0.05`,
  `SATURATION_FRACTION_OF_MAX = 0.95`). Writes `curve_shape.json` with `shape_class`, `slope`,
  `p_value`, `saturation_multiplier`, `plateau_dsi`, `qualitative_description`.
* `code/plot_sweep.py` (~200 lines) - copied from t0029's `plot_dsi_vs_length.py`. Extended to emit
  four charts: (1) `dsi_vs_length.png` primary, (2) `vector_sum_dsi_vs_length.png` defensive
  fallback, (3) `polar_overlay.png` (seven-colour polar via `plot_polar_tuning_curve`), (4)
  `peak_hz_vs_length.png` diagnostic.

**Alternatives considered**:

* **Port t0029's `identify_distal_sections` verbatim** (iterate `h.RGC.dends`, filter to `h.RGC.ON`
  leaves). Rejected: t0024's `RGCmodelGD.hoc` has NO `h.RGC.ON` attribute - this path raises
  `AttributeError`. Research-code confirmed via inspection of `_map_tree` in `build_cell.py:140-168`
  that `cell.terminal_dends` is the biologically equivalent set.

* **Rebuild the cell per sweep point** rather than mutate `sec.L` on the live handle. Rejected:
  wastes ~10-15 s on 7 rebuilds, introduces stochastic-state drift risk between sweep points, and
  breaks the amortised NEURON build cost that makes the 840-trial budget feasible.

* **Use vector-sum DSI as primary metric**. Rejected: task description explicitly names primary DSI
  (peak-minus-null) as the operative discriminator, and t0026's V_rest sweep on t0024 already
  demonstrated that primary DSI has a 1.9x dynamic range on t0024 (0.36-0.67) because AR(2) noise
  guarantees non-zero null firing. Vector-sum DSI is retained as a defensive secondary chart per
  t0029/t0030 learning.

* **Sweep `nseg` in addition to `L`** to keep d_lambda constant across the sweep. Rejected for
  initial run: t0024's HOC template uses `forall {nseg=1}` for terminal dendrites. A d_lambda
  post-check is logged in preflight; if the 2.0x endpoint violates `sec.L / sec.lambda_f < 0.2`, we
  re-run that single length with adaptive `nseg` as a follow-up correction - it does not block the
  main sweep.

* **Run both correlated (rho=0.6) and uncorrelated (rho=0.0) arms**. Rejected: single-condition
  sweep per task description ("Keep the AR(2) correlation rho=0.6 at its t0026 V_rest-sweep
  default"). Adding an uncorrelated arm would double runtime to ~5.6 h and conflate the length
  mechanism with a release-correlation mechanism.

## Cost Estimation

Itemised estimate in USD:

* API calls (LLM / commercial): $0.00 - no paid API calls.
* Remote compute (GPU / cloud): $0.00 - all simulation runs on the local Windows workstation CPU. No
  GPU, no cloud.
* Local compute: $0.00 - already-paid workstation time. Estimated wall time ~2.8 h (840 trials at
  ~12 s/trial on t0024, per t0026's wall-time anchor).
* Storage / network: $0.00 - all outputs stay on local disk (~50 MB for 8 CSVs + 4 PNGs + JSON
  logs).
* Registered paid services in `project/budget.json.available_services`: empty list; nothing to spend
  on.

**Total estimated cost: $0.00**.

Project budget is $1.00 USD total, $0.00 currently spent, $1.00 remaining (per
`project/budget.json`). This task stays within budget by the full margin; no cost cap required.

## Step by Step

### Milestone A: Setup and preflight

1. **[CRITICAL] Create `code/paths.py` and `code/constants.py`.** Copy
   `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/paths.py` verbatim, then rewrite `TASK_ID` to
   `"t0034_distal_dendrite_length_sweep_t0024"` and add three new path constants:
   `VECTOR_SUM_DSI_VS_LENGTH_PNG = IMAGES_DIR / "vector_sum_dsi_vs_length.png"`,
   `POLAR_OVERLAY_PNG = IMAGES_DIR / "polar_overlay.png"`,
   `PEAK_HZ_VS_LENGTH_PNG = IMAGES_DIR / "peak_hz_vs_length.png"`. Copy
   `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/constants.py` verbatim and add
   `N_TRIALS_T0024: int = 10` and `AR2_RHO: float = 0.6`. Relax `DISTAL_MIN_DEPTH` and
   `DISTAL_MIN_COUNT` to warn-only thresholds (they are logged but not asserted in preflight).
   Inputs: research_code.md recommendations; t0029 files. Outputs: `code/paths.py` (~55 lines),
   `code/constants.py` (~90 lines). Expected observable output: running
   `uv run python -c "from tasks.t0034_distal_dendrite_length_sweep_t0024.code.constants import LENGTH_MULTIPLIERS, AR2_RHO, N_TRIALS_T0024; print(LENGTH_MULTIPLIERS, AR2_RHO, N_TRIALS_T0024)"`
   prints `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0) 0.6 10`. Satisfies REQ-4.

2. **[CRITICAL] Create `code/distal_selector_t0024.py` and `code/length_override_t0024.py`.** The
   distal selector file contains a single function
   `identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]` that returns
   `list(cell.terminal_dends)`. **Do NOT use `h.RGC.ON`** - that attribute does not exist on the
   t0024 morphology (`AttributeError` otherwise). Copy
   `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py` into
   `code/length_override_t0024.py` but delete the `identify_distal_sections` and
   `_on_arbor_section_names` helpers - keep only `snapshot_distal_lengths`,
   `set_distal_length_multiplier`, `assert_distal_lengths` verbatim. Inputs: t0029 source; t0024
   `build_cell.DSGCCell` definition. Outputs: `code/distal_selector_t0024.py` (~50 lines),
   `code/length_override_t0024.py` (~60 lines). Expected observable output:
   `uv run python -c "from tasks.t0034_distal_dendrite_length_sweep_t0024.code.distal_selector_t0024 import identify_distal_sections_t0024; print(identify_distal_sections_t0024)"`
   succeeds without import errors. Satisfies REQ-2, REQ-3.

3. **[CRITICAL] Preflight: build cell and log distal-section distribution.** Create
   `code/preflight_distal.py` (~130 lines) by copying
   `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/preflight_distal.py`. Adapt: (a) replace
   `build_dsgc() + _source_channel_partition_hoc()` with `cell = build_dsgc_cell()` from t0024; (b)
   call `distal_sections = identify_distal_sections_t0024(cell=cell)`; (c) compute depth per leaf
   via `h.SectionRef(sec=sec).parent` walk until reaching `cell.soma`; (d) snapshot baseline lengths
   via `snapshot_distal_lengths`; (e) compute min/median/max/total distal L. Write
   `logs/preflight/distal_sections.json`:
   `{"count": <int>, "min_depth": <int>, "median_depth": <int>, "max_depth": <int>, "min_L_um": <float>, "median_L_um": <float>, "max_L_um": <float>, "total_L_um": <float>, "identification_rule": "t0024_terminal_dends"}`.
   **Validation gate (preflight)**: if `len(distal_sections) < 50`, log WARN but do not halt;
   research_code.md notes t0024 has 177 terminals so this is not expected to trip. If
   `min_depth < 3`, log WARN (the t0024 morphology is different from t0022's; thresholds may be
   miscalibrated initially). Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0034_distal_dendrite_length_sweep_t0024 -- uv run python -u -m tasks.t0034_distal_dendrite_length_sweep_t0024.code.preflight_distal`.
   Expected wall time ~30 s. Expected observable output: `distal_sections.json` exists with `count`
   >= 50 (likely ~177 per research_code.md) and no Python tracebacks. Satisfies REQ-2.

### Milestone B: Driver implementation

4. **Create `code/trial_runner_length_t0024.py`.** Copy
   `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/trial_runner_t0024.py` as the starting skeleton
   (~170 lines). Adapt (~180 lines final):

   * Rename `CellContextT0024` -> `CellContextT0024Length`.
   * Add fields: `distal_sections: list[Any]`, `baseline_L: dict[int, float]`,
     `current_multiplier: float` (initialised to 1.0). Keep `cell: DSGCCell`,
     `bundle: SynapseBundle`.
   * In `build_cell_context()`, after `build_dsgc_cell()` and `_setup_synapses(...)`, call
     `distal_sections = identify_distal_sections_t0024(cell=cell)` and
     `baseline_L = snapshot_distal_lengths(distal_sections=distal_sections)`.
   * Drop the `v_rest_mv` parameter. Replace `run_one_trial_vrest` with
     `run_one_trial_length(*, ctx: CellContextT0024Length, direction_deg: float, trial_seed: int) -> TrialResult`.
   * **AR(2) rho capture**: at module scope, `_AR2_RHO: float = C.AR2_CROSS_CORR_RHO_CORRELATED`
     (captured once, never overridden). Do NOT accept `rho` as a function parameter. Satisfies
     REQ-6.
   * Inside `run_one_trial_length`, do NOT call `set_distal_length_multiplier` - the outer sweep
     driver handles that once per sweep point. Keep the rest of the t0024 per-trial sequence:
     `_bar_arrival_times` -> `_rates_with_ar2_noise(rho=_AR2_RHO, seed=trial_seed)` ->
     `_rates_to_events` -> NetCon event queue -> `fih = h.FInitializeHandler(_queue); _ = fih`
     (keep-alive) -> `h.finitialize(C.V_INIT_MV)` -> `h.run()` (NOT `h.continuerun`) ->
     `_count_spikes`.
   * Return `TrialResult(spike_count: int, peak_mv: float, firing_rate_hz: float)` where
     `firing_rate_hz = spike_count / (C.TSTOP_MS / 1000.0)`.

   Inputs: t0026 source, t0024 library. Outputs: `code/trial_runner_length_t0024.py` (~180 lines).
   Expected observable output:
   `uv run python -c "from tasks.t0034_distal_dendrite_length_sweep_t0024.code.trial_runner_length_t0024 import build_cell_context, run_one_trial_length; print('ok')"`
   succeeds. Satisfies REQ-1, REQ-5, REQ-6.

5. **[CRITICAL] Create `code/run_sweep.py`.** Copy
   `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/run_length_sweep.py` as the starting skeleton
   (~239 lines). Adapt (~240 lines final):

   * Replace t0022 constant imports with t0024 equivalents. Remove
     `ANGLE_STEP_DEG / N_ANGLES / N_TRIALS` imports; use `C.ANGLES_12ANG_DEG` and local
     `N_TRIALS_T0024 = 10`.
   * Replace `build_cell_context` and `run_one_trial_length` imports to point at the new
     `trial_runner_length_t0024` module.
   * Preserve the outer structure: `for length_idx, multiplier in enumerate(LENGTH_MULTIPLIERS):`;
     inside: call
     `set_distal_length_multiplier(distal_sections=ctx.distal_sections, baseline_L=ctx.baseline_L, multiplier=multiplier)`
     and `assert_distal_lengths(distal_sections=..., baseline_L=..., multiplier=multiplier)` ONCE
     per outer iteration, then loop over
     `for angle_idx, direction_deg in enumerate(C.ANGLES_12ANG_DEG):` and
     `for trial_idx in range(N_TRIALS_T0024):`.
   * Seed convention: `trial_seed = length_idx * 10_000_003 + 1000 * angle_idx + trial_idx + 1`.
     Research-code flagged this as the t0029 pattern extended with a length-index outer prefix for
     uniqueness across 840 trials.
   * Tidy CSV schema:
     `(length_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`. Call
     `fh.flush()` after every trial write (REQ-13).
   * After each outer iteration, emit per-length canonical curve CSV at
     `results/data/per_length/tuning_curve_L<label>.csv` (label via `paths._multiplier_label`) with
     schema `(angle_deg, trial_seed, firing_rate_hz)` (t0012 scorer input).
   * Emit `results/data/wall_time_by_length.json` with `{ "L<label>": <seconds>, ... }`.
   * Post-sweep: call `set_distal_length_multiplier(..., multiplier=1.0)` +
     `assert_distal_lengths(..., multiplier=1.0)` to restore baseline and confirm idempotence.
   * CLI flags: `--preflight` (run 3 angles x 2 trials x 3 multipliers `(0.5, 1.0, 2.0)` only),
     `--output <path>`.

   Inputs: t0029 source; `trial_runner_length_t0024`; t0024 constants. Outputs: `code/run_sweep.py`
   (~240 lines). Expected observable output: module imports cleanly. Satisfies REQ-1, REQ-4, REQ-5,
   REQ-6, REQ-13.

6. **[CRITICAL] Validation gate: run `run_sweep.py --preflight`.** Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0034_distal_dendrite_length_sweep_t0024 -- uv run python -u -m tasks.t0034_distal_dendrite_length_sweep_t0024.code.run_sweep --preflight`.
   Expected runtime: ~4 min (18 trials x ~12 s/trial). Expected observable output: 18 tidy-CSV rows
   with non-NaN `firing_rate_hz`, three per-length canonical CSVs emitted (`tuning_curve_L0p50.csv`,
   `tuning_curve_L1p00.csv`, `tuning_curve_L2p00.csv`), each with 6 rows.

   **Validation gate thresholds** (expensive-operation gate per experiment-run guidelines):

   * **Trivial baseline**: t0026's V_rest sweep on t0024 at `V_rest=-60 mV` (our condition) reported
     DSI ~0.50-0.55, peak firing ~4-5 Hz, null firing ~1-2 Hz. The preflight 1.0x midpoint should
     reproduce **DSI >= 0.3** and **peak_hz >= 2.0** at least (loose because preflight uses only 2
     trials per angle). If either is below these thresholds at 1.0x, STOP and debug.
   * **Inspect 5 individual trial outputs** at `multiplier=1.0`: read the preflight CSV rows for
     `multiplier=1.0`; for each of the 6 rows (3 angles x 2 trials), confirm `spike_count` is in
     [0, 20] (biologically plausible range) and `peak_mv` is in [-70, +60] (physiological range). If
     any row has `spike_count > 50` or `peak_mv > +80`, STOP and debug - a unit or overflow bug.
   * **Failure condition**: if preflight 1.0x primary DSI <= 0.0 (no directional tuning), STOP - the
     override pipeline has leaked into the driver. Debug by running a single-trial case
     `(multiplier=1.0, direction_deg=120, trial_seed=1)` and diffing against t0026's single-trial
     output at `V_rest=-60 mV`.
   * **AR(2) preservation check**: confirm `_AR2_RHO == 0.6` is used in every trial by asserting
     `C.AR2_CROSS_CORR_RHO_CORRELATED == 0.6` at the top of `run_sweep.py` (raises if someone later
     edits the t0024 library constant).

   Satisfies REQ-1, REQ-5, REQ-6.

7. **[CRITICAL] Run the full sweep.** Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0034_distal_dendrite_length_sweep_t0024 -- uv run python -u -m tasks.t0034_distal_dendrite_length_sweep_t0024.code.run_sweep --output results/data/sweep_results.csv`.
   Expected runtime: ~2.8 h (840 trials x ~12 s/trial on t0024, per t0026 anchor). Unattended.
   Inputs: t0024 library, local code. Outputs: `results/data/sweep_results.csv` (841 lines = 1
   header + 840 data rows), seven per-length canonical CSVs in `results/data/per_length/`,
   `results/data/wall_time_by_length.json`. Per-row `fh.flush()` enables crash recovery (REQ-13).
   Post-run: assertion restores and confirms baseline `sec.L`. Expected observable output: 840 data
   rows, 7 distinct `length_multiplier` values, 12 distinct `direction_deg` values per multiplier,
   no NaN `firing_rate_hz`. Satisfies REQ-4, REQ-5, REQ-6, REQ-13, REQ-14.

### Milestone C: Metrics, classification, and charts

8. **Create `code/analyse_sweep.py`.** Copy
   `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/compute_length_metrics.py` (~291 lines) as
   the starting skeleton. Adapt (~290 lines final):

   * Rename the paths import to point at t0034 `code/paths.py`.
   * For each sweep point, call
     `compute_dsi(curve=load_tuning_curve(csv_path=per_length_curve_csv(multiplier=m)))` as the
     primary DSI.
   * Compute vector-sum DSI via the `_vector_sum_dsi` helper (copied verbatim from t0029).
   * Compute `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`.
   * Compute preferred-direction angle (argmax of per-angle mean firing rate) and
     preferred-direction firing rate.
   * Compute mean peak mV per sweep point from the tidy CSV.
   * Write `results/data/metrics_per_length.csv` with columns
     `(length_multiplier, dsi_primary, dsi_vector_sum, peak_hz, null_hz, hwhm_deg, reliability, preferred_direction_deg, preferred_hz, mean_peak_mv)`.
   * Write `results/metrics.json` using the explicit multi-variant format: 7 variants keyed
     `length_0p50`, `length_0p75`, ..., `length_2p00`, each with
     `dimensions={"length_multiplier": <m>}` and
     `metrics={"direction_selectivity_index": <dsi_primary>, "tuning_curve_hwhm_deg": <hwhm>, "tuning_curve_reliability": <rel>}`.
   * Omit `tuning_curve_rmse` (t0022-style target-curve metric is not meaningful here; stimulus
     biophysics unchanged except for `sec.L`). Record the omission in
     `results/data/metrics_notes.json`.

   Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0034_distal_dendrite_length_sweep_t0024 -- uv run python -u -m tasks.t0034_distal_dendrite_length_sweep_t0024.code.analyse_sweep`.
   Expected observable output: `metrics.json` contains `variants` key with 7 entries;
   `metrics_per_length.csv` has 7 rows. Satisfies REQ-5, REQ-7, REQ-15.

9. **Create `code/classify_shape.py`.** Copy
   `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/classify_curve_shape.py` (~170 lines) as the
   starting skeleton. Adapt (minor):

   * Rename the paths import to t0034.
   * Classify using `dsi_primary` column (not `dsi_vector_sum`) as the primary signal.
   * Apply t0029 thresholds (`MONOTONIC_SLOPE_MIN_PER_UNIT = 0.05`, `MONOTONIC_P_MAX = 0.05`,
     `SATURATION_FRACTION_OF_MAX = 0.95`, `SATURATION_MULTIPLIER_MAX = 1.25`).
   * Output `results/data/curve_shape.json` with
     `{"shape_class": <str>, "slope": <float>, "intercept": <float>, "r_squared": <float>, "p_value": <float>, "saturation_multiplier": <float|null>, "plateau_dsi": <float|null>, "dsi_range_extremes": <float>, "qualitative_description": <str>}`.
   * Also write the same analysis for `dsi_vector_sum` as a secondary `shape_class_vector_sum` field
     inside the same JSON (defensive fallback, REQ-9).

   Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0034_distal_dendrite_length_sweep_t0024 -- uv run python -u -m tasks.t0034_distal_dendrite_length_sweep_t0024.code.classify_shape`.
   Expected observable output: `curve_shape.json` with `shape_class` in
   `{"monotonic", "saturating", "non_monotonic"}`. Satisfies REQ-8, REQ-9, REQ-12.

10. **Create `code/plot_sweep.py`.** Start from
    `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/plot_dsi_vs_length.py` and extend to emit
    four charts (~200 lines total):

    * `results/images/dsi_vs_length.png` (primary): Cartesian two-panel - left y-axis `dsi_primary`
      (Okabe-Ito blue), right y-axis `peak_hz` (Okabe-Ito orange), x-axis `length_multiplier`.
      Overlay regression line if classification is `monotonic`; vertical dashed line at
      `saturation_multiplier` if `saturating`. Baseline (1.0x) annotated with a star.
    * `results/images/vector_sum_dsi_vs_length.png` (secondary / defensive fallback, REQ-9):
      single-panel Cartesian, `dsi_vector_sum` vs `length_multiplier`. Even if primary DSI pins at
      1.0 at some sweep points (unlikely on t0024 but the t0029/t0030 learning dictates a defensive
      chart), vector-sum DSI resolves directional structure independently.
    * `results/images/polar_overlay.png` (REQ-10): a single polar axes with seven coloured lines,
      one per length multiplier, using `plot_polar_tuning_curve` from the t0011 `tuning_curve_viz`
      library for the base rendering. Colour palette: viridis across the 7 multipliers. Legend shows
      multiplier labels.
    * `results/images/peak_hz_vs_length.png` (REQ-11): single-panel Cartesian, `peak_hz` and
      `null_hz` overlaid vs `length_multiplier` (two lines, Okabe-Ito palette).

    Save all charts at 300 dpi. Execute:
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0034_distal_dendrite_length_sweep_t0024 -- uv run python -u -m tasks.t0034_distal_dendrite_length_sweep_t0024.code.plot_sweep`.
    Expected observable output: four PNGs in `results/images/`, each > 20 KB. Satisfies REQ-8,
    REQ-9, REQ-10, REQ-11.

## Remote Machines

**None required.** The entire sweep runs on the local Windows workstation CPU. Per the research-code
wall-time anchor from t0026, t0024 runs at ~12 s per (angle, trial) - significantly slower than
t0022's ~3.5 s/trial because of AR(2) stochastic release. Total sweep = 7 multipliers x 12 angles x
10 trials = 840 trials x ~12 s = ~168 min = **~2.8 h**. Plus ~30 s cell-build overhead and ~5 min
preflight. No GPU, no cloud. The task description confirms "Local CPU only. No remote compute, no
paid API."

## Assets Needed

Input assets this task depends on:

* **`de_rosenroll_2026_dsgc`** (library, registered) - from t0024. Source:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`. Provides
  `build_dsgc_cell`, `DSGCCell`, `_setup_synapses`, `_bar_arrival_times`, `_rates_with_ar2_noise`,
  `_rates_to_events`, `_gaba_prob_for_direction`, `_count_spikes`, `SynapseBundle`, and all t0024
  constants (`AR2_CROSS_CORR_RHO_CORRELATED = 0.6`, `TSTOP_MS`, `V_INIT_MV`, `ANGLES_12ANG_DEG`,
  etc.). The HOC template `RGCmodelGD.hoc` and compiled MOD mechanisms are vendored under `sources/`
  inside this asset.
* **`tuning_curve_loss`** (library, registered) - from t0012. Source:
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`. Provides
  `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`,
  `load_tuning_curve`, `TuningCurve`.
* **`tuning_curve_viz`** (library, registered, optional) - from t0011. Source:
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`. Provides
  `plot_polar_tuning_curve` used by `plot_sweep.py` for the polar overlay chart.
* **t0029 workflow template (file-level copies, not library imports)** - source:
  `tasks/t0029_distal_dendrite_length_sweep_dsgc/code/`. The structural clones of `paths.py`,
  `constants.py`, `length_override.py`, `preflight_distal.py`, `run_length_sweep.py`,
  `compute_length_metrics.py`, `classify_curve_shape.py`, `plot_dsi_vs_length.py` are all copied per
  CLAUDE.md rule 9 (no cross-task imports from non-library task folders).

## Expected Assets

`task.json` declares `expected_assets: {}` - no paper, dataset, library, model, predictions, or
answer assets are produced. This is a pure experiment-run task whose deliverables are metrics,
charts, and the curve-shape classification, all of which live under `results/`. The expected output
artefacts (non-assets, delivered under `tasks/t0034_distal_dendrite_length_sweep_t0024/`):

* `results/data/sweep_results.csv` - 840 tidy trial rows (7 multipliers x 12 angles x 10 trials).
* `results/data/per_length/tuning_curve_L<label>.csv` x 7 - canonical 120-row tuning-curve CSVs
  consumed by the t0012 scorer.
* `results/data/metrics_per_length.csv` - one row per length with primary DSI, vector-sum DSI, peak
  Hz, null Hz, HWHM, reliability, preferred-direction angle, preferred-direction firing rate, mean
  peak mV.
* `results/data/curve_shape.json` - primary-DSI classification (monotonic / saturating /
  non-monotonic) plus vector-sum-DSI secondary classification, slope/p-value, saturation multiplier,
  qualitative description.
* `results/data/metrics_notes.json` - documents the intentional omission of `tuning_curve_rmse`.
* `results/data/wall_time_by_length.json` - per-sweep-point wall time.
* `results/metrics.json` - explicit multi-variant format with 7 length variants.
* `results/images/dsi_vs_length.png` - primary chart (DSI + peak Hz vs multiplier).
* `results/images/vector_sum_dsi_vs_length.png` - defensive fallback chart.
* `results/images/polar_overlay.png` - 7-line polar overlay of tuning curves.
* `results/images/peak_hz_vs_length.png` - peak + null Hz diagnostic chart.
* `logs/preflight/distal_sections.json` - distal identification rule + counts + depth + length
  distribution.

## Time Estimation

* Research: already complete (`research/research_code.md` synthesised 10 prior tasks; no further
  research needed). 0 h.
* Planning: this document. ~1 h.
* Implementation:
  * Milestone A (steps 1-3, setup + preflight): ~1 h coding + ~5 min runtime.
  * Milestone B step 4 (trial runner): ~45 min coding.
  * Milestone B step 5 (sweep driver): ~40 min coding.
  * Milestone B step 6 (preflight sweep validation gate): ~4 min runtime + ~15 min triage.
  * Milestone B step 7 (full sweep run): **~2.8 h runtime (unattended)**.
  * Milestone C steps 8-10 (metrics + classification + charts): ~1.5 h coding + <1 min runtime.
* Validation and coverage check: ~30 min.

**Total implementation wall time: ~7.5 h** (~2.8 h of which is unattended simulation time; human
engagement ~4.7 h for coding, triage, and verification).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Primary DSI pins at 1.0 across the whole sweep despite AR(2) stochastic release (if the AR(2) noise is insufficient at some sweep points to sustain null-direction firing, the primary DSI discriminator could still flatten). Research-code predicts 0.36-0.67 range based on t0026 V_rest sweep, but length sweep may expose a different noise regime. | Medium-Low | Medium | Emit the vector-sum DSI chart (`vector_sum_dsi_vs_length.png`) as a defensive secondary chart per the t0029/t0030 learning. `analyse_sweep.py` also computes peak Hz and null Hz per length; even if primary DSI pins at 1.0, the peak/null split still distinguishes Dan2018 (peak grows with length) from Sivyer2013 (peak saturates). The `classify_shape.py` produces a vector-sum secondary classification (`shape_class_vector_sum`) that works independently of the primary classifier. |
| t0024 morphology has different distal count or depth distribution than t0022, breaking the `DISTAL_MIN_COUNT >= 50` / `DISTAL_MIN_DEPTH >= 3` hard gates inherited from t0029. Research-code notes t0024 has 177 terminals but depth distribution is unmeasured. | Medium | Low | Preflight step 3 relaxes these to warn-only (logged in `distal_sections.json`, not asserted). If `count < 50` or `min_depth < 3`, the preflight WARNS but does not halt; a human reviewer decides whether the relaxed set is acceptable before running step 7. If unacceptable, create `intervention/distal_identification_recalibration.json` and halt. |
| 2.0x length violates d_lambda rule at `nseg=1` (under-resolved segmentation at the long-dendrite endpoint). | Medium | Low | Preflight step 3 records per-section `sec.L / sec.lambda_f` at multiplier 2.0 (computed via the dummy applied inside preflight after snapshot/restore). Post-sweep, if violation detected (> 0.2 for any distal section), re-run just the 2.0x point with adaptive `nseg = ceil(L / (0.1 * lambda_f))` and update the corresponding row in `metrics_per_length.csv`. Does not block the main sweep. |
| NEURON crash or Windows-specific DLL issue during the ~2.8 h unattended run. | Low-Medium | High | Crash recovery via per-row `fh.flush()` (REQ-13). On restart, the sweep driver can either resume from the last completed `(length_multiplier, trial, direction_deg)` tuple or re-run fully (cell build is only ~30 s). Acceptance: at least 836/840 trials (99.5%) must succeed; if fewer, halt and debug. Also run from a clean Python process each attempt (NEURON global state leaks if the process is reused). |
| Baseline distal `sec.L` not restored after sweep, corrupting any downstream use of the live cell handle. | Low | Medium | Post-sweep assertion in step 7 calls `set_distal_length_multiplier(..., multiplier=1.0)` + `assert_distal_lengths(..., multiplier=1.0)` with `tol=1e-9`; failure raises `AssertionError`. Pattern from t0029 `run_length_sweep.py:217-229`. |
| `h.RGC.ON` attribute access in an overlooked t0029 copy-paste raises `AttributeError` on t0024. | Low | Blocking | Grep-verification in Verification Criteria confirms no file under `tasks/t0034_.../code/` contains the string `h.RGC.ON` or `RGC.ON`. The `distal_selector_t0024.py` module exists specifically to prevent this by exposing `identify_distal_sections_t0024` as the only legitimate distal selector in this task. |
| Classification thresholds (`MONOTONIC_SLOPE_MIN_PER_UNIT = 0.05`) were calibrated for t0029's [0, 1] DSI range but t0024's expected range is [0.36, 0.67] - a 0.05 slope represents a 0.075 DSI change across 1.5 multiplier units, visible but modest relative to the 0.31 baseline dynamic range. | Medium | Low | `classify_shape.py` emits the raw slope, R-squared, p-value, and saturation multiplier alongside the categorical `shape_class` label. A human reviewer can override the automatic label in `results_detailed.md` if the thresholds are too strict or too loose for the observed DSI range. The vector-sum secondary classification provides an independent check. |
| Per-trial AR(2) seed collision produces non-unique random streams across the 840 trials (e.g., `seed = length_idx * 10_000_003 + 1000 * angle_idx + trial_idx + 1` formula bug). | Low | Low | `run_sweep.py` asserts seed uniqueness after the full sweep by collecting all emitted `trial_seed` values into a set and checking `len(seeds) == 840`. Research-code prescribes the exact seed formula; a unit test in `run_sweep.py` confirms no collisions at the preflight scale before the full run. |

## Verification Criteria

Testable checks run at the end of implementation:

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0034_distal_dendrite_length_sweep_t0024 -- uv run python -u -m arf.scripts.verificators.verify_plan t0034_distal_dendrite_length_sweep_t0024`;
  expect zero errors.
* Run
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open('tasks/t0034_distal_dendrite_length_sweep_t0024/results/data/sweep_results.csv'))); assert len(rows) == 840, len(rows); assert len({r['length_multiplier'] for r in rows}) == 7; assert all(r['firing_rate_hz'] not in ('', 'nan', 'NaN') for r in rows); print('OK', len(rows))"`;
  expect `OK 840` (confirms REQ-4 and REQ-5).
* Run
  `uv run python -u -c "import json, pathlib; m = json.loads(pathlib.Path('tasks/t0034_distal_dendrite_length_sweep_t0024/results/metrics.json').read_text()); assert 'variants' in m and len(m['variants']) == 7; assert all('direction_selectivity_index' in v['metrics'] for v in m['variants']); print('OK')"`;
  expect `OK` (confirms REQ-5 and REQ-7 - DSI variants present for all 7 lengths).
* Run
  `uv run python -u -c "import pathlib; imgs = ['dsi_vs_length.png','vector_sum_dsi_vs_length.png','polar_overlay.png','peak_hz_vs_length.png']; [print('OK', p, pathlib.Path(f'tasks/t0034_distal_dendrite_length_sweep_t0024/results/images/{p}').stat().st_size) for p in imgs if pathlib.Path(f'tasks/t0034_distal_dendrite_length_sweep_t0024/results/images/{p}').exists() and pathlib.Path(f'tasks/t0034_distal_dendrite_length_sweep_t0024/results/images/{p}').stat().st_size > 20000]"`;
  expect four `OK ...` lines with sizes > 20000 bytes each (confirms REQ-8, REQ-9, REQ-10, REQ-11).
* Run
  `uv run python -u -c "import json, pathlib; s = json.loads(pathlib.Path('tasks/t0034_distal_dendrite_length_sweep_t0024/results/data/curve_shape.json').read_text()); assert s['shape_class'] in ('monotonic','saturating','non_monotonic'); assert 'shape_class_vector_sum' in s; print('OK', s['shape_class'], s['shape_class_vector_sum'])"`;
  expect `OK <primary> <secondary>` (confirms REQ-8, REQ-9, REQ-12 classification).
* Run
  `uv run python -u -c "import json, pathlib; p = json.loads(pathlib.Path('tasks/t0034_distal_dendrite_length_sweep_t0024/logs/preflight/distal_sections.json').read_text()); assert p['count'] > 0 and p['identification_rule'] == 't0024_terminal_dends'; print('OK', p['count'], p.get('min_depth'))"`;
  expect `OK <count> <min_depth>` (confirms REQ-2 - t0024-specific distal rule used, not
  `h.RGC.ON`).
* Run
  `uv run python -u -c "import pathlib, re; files = list(pathlib.Path('tasks/t0034_distal_dendrite_length_sweep_t0024/code').glob('*.py')); bad = [(f.name, i+1) for f in files for i, line in enumerate(f.read_text(encoding='utf-8').splitlines()) if re.search(r'h\\.RGC\\.ON|RGC\\.ON\\b', line)]; assert not bad, f'h.RGC.ON found: {bad}'; print('OK no h.RGC.ON references in', len(files), 'files')"`;
  expect `OK no h.RGC.ON references in N files` (confirms REQ-2 - t0024-specific selector used).
* Run
  `uv run python -u -c "import pathlib, re; files = list(pathlib.Path('tasks/t0034_distal_dendrite_length_sweep_t0024/code').glob('*.py')); bad = [(f.name, i+1) for f in files for i, line in enumerate(f.read_text(encoding='utf-8').splitlines()) if re.search(r'from\\s+tasks\\.t0029_', line)]; assert not bad, f'cross-task import from t0029: {bad}'; print('OK no t0029 imports')"`;
  expect `OK no t0029 imports` (confirms REQ-3 - helper was copied, not imported).
* Run
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open('tasks/t0034_distal_dendrite_length_sweep_t0024/results/data/metrics_per_length.csv'))); cols = {'dsi_primary','dsi_vector_sum','peak_hz','null_hz','hwhm_deg','reliability','preferred_direction_deg','preferred_hz'}; assert cols.issubset(rows[0].keys()), set(rows[0].keys()) - cols; print('OK', len(rows), 'rows')"`;
  expect `OK 7 rows` (confirms REQ-7 - secondary metrics present).
* Run
  `uv run ruff check --fix . && uv run ruff format . && uv run mypy tasks/t0034_distal_dendrite_length_sweep_t0024`;
  expect zero errors and zero warnings.
* REQ-coverage check: every `REQ-*` ID in `## Task Requirement Checklist` is mentioned in at least
  one numbered step (`## Step by Step`). Run
  `uv run python -u -c "import re, pathlib; t = pathlib.Path('tasks/t0034_distal_dendrite_length_sweep_t0024/plan/plan.md').read_text(encoding='utf-8'); reqs = set(re.findall(r'REQ-\\d+', t)); print(sorted(reqs, key=lambda s: int(s.split('-')[1])))"`;
  expect exactly
  `['REQ-1', 'REQ-2', 'REQ-3', 'REQ-4', 'REQ-5', 'REQ-6', 'REQ-7', 'REQ-8', 'REQ-9', 'REQ-10', 'REQ-11', 'REQ-12', 'REQ-13', 'REQ-14', 'REQ-15']`.
