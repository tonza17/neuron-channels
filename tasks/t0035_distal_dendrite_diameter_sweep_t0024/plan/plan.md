---
spec_version: "2"
task_id: "t0035_distal_dendrite_diameter_sweep_t0024"
date_completed: "2026-04-23"
status: "complete"
---
# Plan: Distal-Dendrite Diameter Sweep on t0024 DSGC

## Objective

Run a single-parameter sweep of distal-dendrite diameter on the **t0024 de Rosenroll 2026 DSGC
port** (library `de_rosenroll_2026_dsgc`, registered at
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/`) and measure the Direction Selectivity Index (DSI)
at each diameter value. The sweep uses seven diameter multipliers (0.5, 0.75, 1.0, 1.25, 1.5, 1.75,
2.0) applied uniformly to every distal terminal dendrite's per-segment `seg.diam`. At each
multiplier, run the canonical 12-direction tuning protocol (12 angles × 10 trials per angle = 120
trials per sweep point, 840 trials total) and compute **primary DSI (peak-minus-null)** via the
t0012 `tuning_curve_loss` scorer as the operative discriminator, plus vector-sum DSI as a defensive
fallback. The task discriminates **Schachter2010 active-dendrite amplification** (positive
DSI-vs-diameter slope — thicker distal compartments host more Nav substrate and boost
preferred-direction local spikes) from **passive filtering** (negative slope — thicker dendrites
lower input impedance and damp directional contrast). The sibling task t0030 produced a null result
on t0022 because t0022's deterministic E-I driver pins null firing at 0 Hz and primary DSI at 1.000.
t0024's AR(2)-correlated stochastic bipolar release (ρ=0.6) restores non-zero null firing (t0034
confirmed 0.70-1.00 Hz on the length sweep) and primary DSI dynamic range 0.545-0.774 — the
discriminator can now measure a slope. Success means producing: (a) a tidy sweep CSV with 840 trial
rows, (b) seven per-diameter canonical 120-row tuning-curve CSVs, (c) `results/metrics.json` with
seven diameter variants, (d) primary-DSI, vector-sum-DSI, polar-overlay, and peak-Hz vs diameter
charts, and (e) a slope-sign classification (`schachter2010_amplification` / `passive_filtering` /
`flat`). All work runs locally on CPU with $0 external cost. Anticipated wall time ~2.8-3 h.

## Task Requirement Checklist

Operative task text from `tasks/t0035_distal_dendrite_diameter_sweep_t0024/task_description.md`:

> 1. Use the **t0024 de Rosenroll 2026 DSGC port** as-is (no channel modifications, no input
>    rewiring). Keep the AR(2) correlation ρ=0.6 at its t0026 V_rest-sweep default.
> 2. Identify distal dendritic sections (HOC leaves on `h.RGC.ON` arbor). Mirror the selection rule
>    from t0030's `diameter_override.py` but **COPY** the helper into this task's
>    `code/diameter_override_t0024.py` — no cross-task imports per CLAUDE.md.
> 3. Sweep distal diameter in **7 values** spanning **0.5× to 2.0×** baseline (0.5, 0.75, 1.0, 1.25,
>    1.5, 1.75, 2.0×). Apply the multiplier uniformly to all distal branches.
> 4. For each diameter value, run the **standard 12-direction tuning protocol** (12 angles × 10
>    trials) and compute **primary DSI** as the operative metric. Also emit vector-sum DSI and
>    secondary metrics.
> 5. Plot primary DSI vs diameter and classify slope sign: positive (Schachter2010 active), negative
>    (passive filtering), flat (neither or schedule-dominated).
>
> Primary metric: primary DSI (peak-minus-null) at each diameter value.
>
> Secondary: vector-sum DSI, peak Hz, null Hz, HWHM, reliability, preferred-direction firing rate,
> per-direction spike counts, peak voltage at a reference distal compartment.
>
> Key questions: (1) Is the primary DSI-vs-diameter slope positive (Schachter2010), negative
> (passive filtering), or flat? (2) If positive, is the magnitude consistent with Na-channel-density
> amplification? (3) If negative, does preferred-direction firing drop alongside DSI (damping) or
> does only the null-direction rate change (selective mechanism)? (4) Does t0024's AR(2) noise
> broaden HWHM enough to mask the signal? (5) How do t0024 and t0022 compare under identical sweep
> protocols?

Requirements:

* **REQ-1**: Use the t0024 DSGC port as-is — no channel modifications, no input rewiring, no AR(2)
  correlation changes. Only per-segment `seg.diam` on distal terminal dendrites is mutated.
  Satisfied by steps 4-7. Evidence: no edits to any file under
  `tasks/t0024_port_de_rosenroll_2026_dsgc/`; the `rho=C.AR2_CROSS_CORR_RHO_CORRELATED` constant is
  captured once at module scope in `trial_runner_diameter_t0024.py` and never overridden;
  `run_sweep.py` calls `set_distal_diameter_multiplier` on a snapshot of baseline diameters only.

* **REQ-2**: Identify distal dendritic sections in the t0024 morphology. The task text names the
  t0022 rule (`h.RGC.ON` arbor walk) as the template, but t0024's `RGCmodelGD.hoc` has **NO
  `h.RGC.ON` attribute** — it defines a single unified dendritic arbor. The biologically equivalent
  set is `DSGCCell.terminal_dends`, computed by `_map_tree` in
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:140-168` as the list of sections with
  `h.SectionRef(sec=sec).nchild() == 0`. Satisfied by steps 2, 3. Evidence:
  `logs/preflight/distal_sections.json` records count, depth distribution, and baseline diameter
  distribution; `code/distal_selector_t0024.py` uses `cell.terminal_dends`, not `h.RGC.ON`
  (grep-verified in Verification Criteria).

* **REQ-3**: Copy the diameter-override helper into this task (no cross-task imports per CLAUDE.md
  rule 9). Satisfied by step 2. Evidence: `code/diameter_override_t0024.py` exists as a standalone
  file with `snapshot_distal_diameters`, `set_distal_diameter_multiplier`,
  `assert_distal_diameters`; no `from tasks.t0030_...` imports appear in any t0035 file
  (grep-verified in Verification Criteria).

* **REQ-4**: Sweep 7 multipliers in `[0.5, 2.0]`; apply uniformly to all distal branches. Values:
  `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`. Satisfied by steps 5, 6, 7. Evidence:
  `DIAMETER_MULTIPLIERS` constant in `code/constants.py`; `sweep_results.csv` contains exactly 7
  distinct `diameter_multiplier` values; `set_distal_diameter_multiplier` applies the same
  multiplier to every `(section, segment)` in one pass.

* **REQ-5**: For each multiplier, run the 12-direction protocol (12 angles × 10 trials) and compute
  primary DSI via the t0012 scorer. Satisfied by steps 6, 7, 8. Evidence: 840 rows in
  `results/data/sweep_results.csv` (7 × 12 × 10); seven per-diameter canonical CSVs of 120 rows
  each; `results/metrics.json` variants each carry one `direction_selectivity_index` value computed
  by `compute_dsi(curve=load_tuning_curve(...))`.

* **REQ-6**: Preserve AR(2) correlation ρ=0.6 at every call site. Satisfied by steps 4, 5, 6, 7.
  Evidence: `code/trial_runner_diameter_t0024.py` captures
  `_AR2_RHO = C.AR2_CROSS_CORR_RHO_CORRELATED` at module scope and does not accept `rho` as a
  parameter; `run_sweep.py` asserts `C.AR2_CROSS_CORR_RHO_CORRELATED == AR2_RHO` at start-up so a
  later library edit cannot silently change the correlation; no call site hardcodes `0.0` or an
  alternative ρ.

* **REQ-7**: Also emit vector-sum DSI and secondary metrics (peak Hz, null Hz, HWHM, reliability,
  preferred-direction firing rate, mean peak mV). Satisfied by step 8. Evidence:
  `results/data/metrics_per_diameter.csv` contains columns `dsi_primary`, `dsi_vector_sum`,
  `peak_hz`, `null_hz`, `hwhm_deg`, `reliability`, `preferred_direction_deg`, `preferred_hz`,
  `mean_peak_mv`.

* **REQ-8**: Plot primary DSI vs diameter and classify slope sign. Satisfied by steps 9, 10.
  Evidence: `results/images/dsi_vs_diameter.png` exists; `results/data/curve_shape.json` and
  `results/data/slope_classification.json` carry `shape_class` / `mechanism_class` in
  `{"schachter2010_amplification", "passive_filtering", "flat"}` plus `slope`, `p_value`,
  `slope_95_ci_low/high`, `r_squared`, `dsi_range_extremes`.

* **REQ-9**: Emit vector-sum DSI as defensive fallback chart (per t0029/t0030/t0034 learning that
  primary DSI can pin at 1.0 under deterministic drivers or saturate under AR(2) if null-direction
  firing is sparse at a particular sweep point). Satisfied by step 10. Evidence:
  `results/images/vector_sum_dsi_vs_diameter.png` exists as a secondary chart; `classify_slope.py`
  computes a vector-sum `shape_class_vector_sum` label that activates automatically if primary DSI
  range falls below `DSI_SATURATION_THRESHOLD = 0.02`.

* **REQ-10**: Produce a polar overlay of all 7 tuning curves (12-direction firing rate vs angle).
  Satisfied by step 10. Evidence: `results/images/polar_overlay.png` exists and contains seven
  coloured lines, one per diameter multiplier (viridis palette).

* **REQ-11**: Produce a peak-Hz-vs-diameter diagnostic chart (peak and null Hz overlaid). Satisfied
  by step 10. Evidence: `results/images/peak_hz_vs_diameter.png` exists and shows peak and null
  firing rate across multipliers.

* **REQ-12**: Classify slope sign as `schachter2010_amplification` (positive, p<0.05,
  `dsi_range_extremes` ≥ 0.05), `passive_filtering` (negative, p<0.05, `dsi_range_extremes` ≤
  -0.05), or `flat` (otherwise). Satisfied by step 9. Evidence: `slope_classification.json`
  `mechanism_class` value plus `qualitative_description` text.

* **REQ-13**: Incremental checkpointing — crash recovery via per-row `fh.flush()`. Satisfied by step
  7\. Evidence: `run_sweep.py` opens the tidy CSV in append mode with line-buffering and calls
  `fh.flush()` after every trial; a partial run leaves a parseable CSV with complete rows only.

* **REQ-14**: Local CPU only, no remote machines, $0 external cost. Satisfied by all steps.
  Evidence: no `setup-machines` step in the step tracker; no paid-API calls; `plan/plan.md` Remote
  Machines section is "None required".

* **REQ-15**: Primary DSI is the operative discriminator on t0024 (unlike t0030 where it pinned at
  1.000 because t0022's deterministic driver silenced the null direction). Satisfied by step 8.
  Evidence: `metrics_per_diameter.csv` `null_hz` column is expected to be non-zero (bounded away
  from 0 Hz) at every sweep point because t0024's AR(2) stochastic release produces measurable
  null-direction firing; t0034's length sweep on t0024 reports primary DSI range 0.545-0.774
  confirming the discriminator has dynamic range.

* **REQ-16**: Seed-uniqueness guard. Satisfied by step 7. Evidence: `run_sweep.py` collects all
  emitted `trial_seed` values into a set and asserts `len(seed_set) == 840` after the full sweep,
  using the deterministic formula
  `trial_seed = diameter_idx * SEED_DIAMETER_STRIDE + SEED_ANGLE_STRIDE * angle_idx + trial_idx + 1`
  with `SEED_DIAMETER_STRIDE = 10_000_003` and `SEED_ANGLE_STRIDE = 1000`.

* **REQ-17**: Compare the t0035 slope to t0030's null result to confirm the pinned-DSI pathology was
  the structural culprit. Satisfied by the `compare-literature` orchestrator step (out of scope for
  Step by Step) reading `metrics_per_diameter.csv` and t0030's
  `results/data/metrics_per_diameter.csv`. Evidence: the classification JSON carries
  `t0030_comparison_note` summarising the primary-DSI range and slope on t0024 vs t0030's
  `dsi_primary = 1.000` null.

## Approach

**Task type**: `experiment-run` (already set in `task.json` and selected by the orchestrator). The
experiment-run Planning Guidelines require naming every independent and dependent variable, using
the explicit multi-variant metrics format when comparing multiple conditions, specifying baselines,
and running a preflight validation gate before expensive simulation. All four are applied below.

**Independent variable**: `diameter_multiplier` in `{0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0}` (7
levels, applied uniformly to every `(section, segment)` pair in the distal terminal set).

**Primary dependent variable**: primary DSI (peak-minus-null via the t0012 scorer) at each diameter.

**Secondary dependent variables**: vector-sum DSI, peak Hz, null Hz, HWHM, reliability,
preferred-direction firing rate, preferred-direction angle, mean peak mV (at the somatic-recording
compartment).

**Fixed conditions**: AR(2) correlation ρ = 0.6 (`C.AR2_CROSS_CORR_RHO_CORRELATED`), V_rest = -60 mV
(`C.V_INIT_MV`), `h.tstop = C.TSTOP_MS = 1000` ms, `C.DT_MS = 0.1`, `C.CELSIUS_DEG_C = 36.9`,
12-angle grid `C.ANGLES_12ANG_DEG = (0, 30, ..., 330)`, 10 trials per angle, correlated-condition
synapse setup, AP threshold -10 mV. No channel modifications, no input rewiring, no uncorrelated-arm
mixing, no geometry changes except per-segment `seg.diam` rescaling on distal terminals.

**Architecture** (from `research/research_code.md`): the t0034 distal-length sweep on t0024 already
proved the build-once, mutate-once-per-sweep-point pattern on t0024. t0035 is a structural twin of
t0034 with `sec.L` replaced by `seg.diam`. Key mechanical differences:

* `sec.L` is a section-level attribute keyed by `id(sec)`; `seg.diam` is a per-segment RANGE
  variable keyed by `(id(sec), float(seg.x))`. The baseline snapshot type changes from
  `dict[int, float]` to `dict[tuple[int, float], float]`.
* Thinner diameter multipliers (0.5×) run slower because axial resistance rises and NEURON's
  adaptive timestep shrinks (observed on t0030).
* The slope-sign classification (Schachter2010 vs passive) replaces t0034's shape classification
  (monotonic / saturating / non-monotonic) — the scientific question is different.

**Distal identification (t0024-specific)**: t0030's `diameter_override.identify_distal_sections`
iterates `h.RGC.dends` and filters to leaves on `h.RGC.ON`. This works on t0022's `RGCmodel.hoc`
with separate ON/OFF arbors. **t0024's `RGCmodelGD.hoc` has NO `h.RGC.ON` attribute** — it defines a
single `h.DSGC` cell with a unified arbor; walking `h.RGC.ON` raises `AttributeError`. The
biologically equivalent set is already computed by `build_cell._map_tree`: `DSGCCell.terminal_dends`
is the list of HOC leaves. The t0034 companion task already created a 27-line wrapper
`distal_selector_t0024.py` that returns `list(cell.terminal_dends)` from a single function
`identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]`. This module is copied verbatim
into t0035 with a one-line import path change.

**Mechanism predictions (Schachter vs passive)**:

| Mechanism | Predicted DSI-vs-diameter slope | Mechanism signature |
| --- | --- | --- |
| Schachter2010 active-dendrite amplification | **Positive** (p<0.05, ΔDSI ≥ 0.05) | Thicker distal compartments host more Na+ substrate per unit length; preferred-direction local spikes are larger and more reliable; peak Hz rises with diameter; null Hz stays flat. |
| Passive filtering | **Negative** (p<0.05, ΔDSI ≤ -0.05) | Thicker distal compartments have lower input impedance per unit synaptic current; both preferred and null rates decline but null declines less than peak; HWHM broadens with thickening. |
| Flat | No significant slope | Neither mechanism dominates, schedule-level effects mask the signal, or AR(2) noise floor is too high relative to the DSI signal. |

Both mechanisms are predicted *a priori* by the Schachter2010 literature and cable-theory
fundamentals; the experiment observes which one wins under the t0024 biophysics.

**Reusable code (imports, not copies) — via registered libraries**:

* From `de_rosenroll_2026_dsgc` library (t0024):
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell, DSGCCell`;
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve import (_setup_synapses, _bar_arrival_times, _rates_with_ar2_noise, _rates_to_events, _gaba_prob_for_direction, _count_spikes, SynapseBundle, BASE_ACH_PROB, RATE_DT_MS)`;
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C`. C provides
  `AR2_CROSS_CORR_RHO_CORRELATED = 0.6`, `TSTOP_MS`, `DT_MS`, `STEPS_PER_MS`, `V_INIT_MV`,
  `AP_THRESHOLD_MV`, `CELSIUS_DEG_C`, `ANGLES_12ANG_DEG`.

* From `tuning_curve_loss` library (t0012):
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve, TuningCurve)`.

* From `tuning_curve_viz` library (t0011, optional, used by `plot_sweep.py` only):
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve`.

**Reusable code (copies into `code/`, per CLAUDE.md rule 9)**:

* `code/paths.py` (~55 lines) — copied from
  `tasks/t0034_distal_dendrite_length_sweep_t0024/code/paths.py`; rename `TASK_ID` to
  `t0035_distal_dendrite_diameter_sweep_t0024`; rename all `length` path constants to `diameter`
  equivalents (`TUNING_CURVE_DIR_PER_DIAMETER`, `METRICS_PER_DIAMETER_CSV`, `DSI_VS_DIAMETER_PNG`,
  `VECTOR_SUM_DSI_VS_DIAMETER_PNG`, `POLAR_OVERLAY_PNG`, `PEAK_HZ_VS_DIAMETER_PNG`,
  `CURVE_SHAPE_JSON`, `SLOPE_CLASSIFICATION_JSON`, `WALL_TIME_BY_DIAMETER_JSON`).
* `code/constants.py` (~100 lines) — merge of t0030's `constants.py` (slope-sign taxonomy,
  `DSI_SATURATION_THRESHOLD`, `DIAMETER_ASSERT_TOL_UM`) and t0034's t0024-specific additions
  (`N_TRIALS_T0024 = 10`, `AR2_RHO = 0.6`, `SEED_DIAMETER_STRIDE = 10_000_003`,
  `SEED_ANGLE_STRIDE = 1000`). `DIAMETER_MULTIPLIERS = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)`;
  `PREFLIGHT_DIAMETER_MULTIPLIERS = (0.5, 1.0, 2.0)`.
* `code/distal_selector_t0024.py` (~27 lines) — copied verbatim from
  `tasks/t0034_distal_dendrite_length_sweep_t0024/code/distal_selector_t0024.py`. Single function
  `identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]` returning
  `list(cell.terminal_dends)`. **Deliberately NOT using `h.RGC.ON`** — that attribute does not exist
  on the t0024 morphology (`AttributeError` otherwise).
* `code/diameter_override_t0024.py` (~85 lines) — copied from
  `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py` (119 lines). **DROP**
  `identify_distal_sections` and `_on_arbor_section_names` (t0022-specific `h.RGC.ON` walk). Keep
  `snapshot_distal_diameters(*, h, distal_sections) -> dict[tuple[int, float], float]`,
  `set_distal_diameter_multiplier(*, h, distal_sections, baseline_diam, multiplier) -> None`,
  `assert_distal_diameters(*, h, distal_sections, baseline_diam, multiplier, tol) -> None` verbatim.
  Update the `DIAMETER_ASSERT_TOL_UM` import to the t0035 `constants` module.
* `code/preflight_distal.py` (~160 lines) — copied from
  `tasks/t0034_distal_dendrite_length_sweep_t0024/code/preflight_distal.py`. Swap the length
  snapshot helper for the diameter snapshot helper; rename JSON fields from `_L_um` to `_diam_um`.
* `code/trial_runner_diameter_t0024.py` (~180 lines) — copied from
  `tasks/t0034_distal_dendrite_length_sweep_t0024/code/trial_runner_length_t0024.py`. Rename
  `CellContextT0024Length` → `CellContextT0024Diameter`; replace `baseline_L: dict[int, float]` with
  `baseline_diam: dict[tuple[int, float], float]`; swap the imported helpers from
  `length_override_t0024` to `diameter_override_t0024`; retain the
  `_AR2_RHO = C.AR2_CROSS_CORR_RHO_CORRELATED` module-scope pin and the `h.FInitializeHandler`
  keep-alive pattern.
* `code/run_sweep.py` (~300 lines) — copied from
  `tasks/t0034_distal_dendrite_length_sweep_t0024/code/run_sweep.py`. Rename length-specific
  identifiers to diameter; update constant imports; keep the seed-uniqueness guard, the per-row
  `fh.flush()`, the post-sweep baseline restoration (`multiplier=1.0` with
  `assert_distal_diameters(..., tol=DIAMETER_ASSERT_TOL_UM)`), and the CLI `--preflight` flag.
* `code/analyse_sweep.py` (~336 lines) — copied from
  `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/analyse_sweep.py`. Retarget paths to the
  t0035 module; compute per-diameter `dsi_primary`, `dsi_vector_sum`, `peak_hz`, `null_hz`,
  `hwhm_deg`, `reliability`, `preferred_direction_deg`, `preferred_hz`, `mean_peak_mv`. Write the
  explicit multi-variant `metrics.json` (7 variants).
* `code/classify_slope.py` (~320 lines) — copied from
  `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/classify_slope.py`. Retarget paths; no
  algorithmic changes. The slope-sign taxonomy (`schachter2010_amplification` / `passive_filtering`
  / `flat`) is exactly the right classifier for this question.
* `code/plot_sweep.py` (~420 lines) — copied from
  `tasks/t0034_distal_dendrite_length_sweep_t0024/code/plot_sweep.py`. Rename chart output paths and
  axis labels from "length" to "diameter"; keep the four-panel structure (primary, vector-sum, polar
  overlay, peak/null Hz).

**Alternatives considered**:

* **Reuse t0030's `identify_distal_sections` verbatim** (walk `h.RGC.ON` leaves). Rejected: t0024's
  `RGCmodelGD.hoc` has no `h.RGC.ON` attribute — this path raises `AttributeError`. Research-code
  confirmed via inspection of `_map_tree` in `build_cell.py:140-168` that `cell.terminal_dends` is
  the biologically equivalent set, and t0034 already validated the wrapper.

* **Rebuild the cell per sweep point** rather than mutate `seg.diam` on the live handle. Rejected:
  wastes ~10-15 s on 7 rebuilds; introduces stochastic-state drift risk between sweep points; and
  breaks the amortised NEURON build cost that makes the 840-trial budget feasible on local CPU.

* **Port t0034's shape classifier (monotonic / saturating / non-monotonic)**. Rejected: wrong
  taxonomy for the diameter-sweep question. Schachter2010 active amplification vs passive filtering
  is a slope-sign discrimination. Adopting t0030's `classify_slope.py` preserves the mechanism
  labels required by the task text.

* **Use vector-sum DSI as primary metric**. Rejected: task description names primary DSI
  (peak-minus-null) as the operative discriminator, and t0034's length sweep on t0024 already
  demonstrated that primary DSI has a non-saturated dynamic range (0.545-0.774) because AR(2) noise
  guarantees non-zero null firing. Vector-sum DSI is retained as a defensive secondary chart per the
  t0029/t0030/t0034 pattern.

* **Sweep `nseg` jointly with `seg.diam`** to hold d_lambda constant. Rejected for the main run:
  t0024's HOC template uses `forall {nseg=1}` for terminal dendrites; the d_lambda check is logged
  in preflight and a re-run is scheduled for violating endpoints as a follow-up correction. Does not
  block the main sweep.

* **Run correlated (ρ=0.6) and uncorrelated (ρ=0.0) arms**. Rejected: single-condition sweep per
  task description ("Keep the AR(2) correlation ρ=0.6 at its t0026 V_rest-sweep default"). Adding an
  uncorrelated arm would double runtime and conflate the diameter mechanism with a release
  correlation mechanism.

## Cost Estimation

Itemised estimate in USD:

* API calls (LLM / commercial): **$0.00** — no paid API calls. Planning, implementation, and
  analysis all run locally.
* Remote compute (GPU / cloud): **$0.00** — all simulation runs on the local Windows workstation
  CPU. No GPU, no cloud, no queueing service.
* Local compute: **$0.00** — already-paid workstation time. Estimated wall time ~2.8-3 h (840 trials
  × ~12 s/trial on t0024 per t0026's V_rest-sweep anchor; thinner-diameter slowdown adds a ~10-15%
  overhead).
* Storage / network: **$0.00** — all outputs stay on local disk (~50 MB for tidy CSVs + 4 PNGs +
  JSON logs).
* Registered paid services in `project/budget.json.available_services`: empty list; nothing to spend
  on.

**Total estimated cost: $0.00**.

Project budget is **$1.00 USD total**, $0.00 currently spent, $1.00 remaining (per
`project/budget.json`). This task stays within budget by the full margin; no cost cap required.

## Step by Step

### Milestone A: Setup and preflight

1. **[CRITICAL] Create `code/paths.py` and `code/constants.py`.** Copy
   `tasks/t0034_distal_dendrite_length_sweep_t0024/code/paths.py` (54 lines) and rewrite `TASK_ID`
   to `"t0035_distal_dendrite_diameter_sweep_t0024"`; rename every `length` path to `diameter`
   (e.g., `TUNING_CURVE_DIR_PER_LENGTH` → `TUNING_CURVE_DIR_PER_DIAMETER`, `DSI_VS_LENGTH_PNG` →
   `DSI_VS_DIAMETER_PNG`, and so on for all 10 output-path constants). Copy `code/constants.py` by
   merging: take the slope-sign taxonomy from
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/constants.py` (95 lines;
   `DIAMETER_MULTIPLIERS`, `PREFLIGHT_DIAMETER_MULTIPLIERS`, `DIAMETER_ASSERT_TOL_UM = 1e-6`,
   `MECHANISM_SCHACHTER2010`, `MECHANISM_PASSIVE`, `MECHANISM_FLAT`,
   `DSI_SATURATION_THRESHOLD = 0.02`, `DSI_RANGE_MIN_FOR_CONFIDENT_LABEL = 0.05`,
   `MAX_P_VALUE = 0.05`, `MIN_SLOPE_MAGNITUDE = 0.05`, slope-sign constants) and add the
   t0024-specific seed/rho constants from
   `tasks/t0034_distal_dendrite_length_sweep_t0024/code/constants.py` (97 lines): `AR2_RHO = 0.6`,
   `N_TRIALS_T0024 = 10`, `SEED_DIAMETER_STRIDE = 10_000_003`, `SEED_ANGLE_STRIDE = 1000`,
   `TIDY_CSV_HEADER = ("diameter_multiplier", "trial", "direction_deg", "spike_count", "peak_mv", "firing_rate_hz")`,
   `CURVE_CSV_HEADER = ("angle_deg", "trial_seed", "firing_rate_hz")`. Inputs: t0030 constants,
   t0034 constants + paths. Outputs: `code/paths.py`, `code/constants.py`. Expected observable
   output:
   `uv run python -c "from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.constants import DIAMETER_MULTIPLIERS, AR2_RHO, N_TRIALS_T0024, MECHANISM_SCHACHTER2010; print(DIAMETER_MULTIPLIERS, AR2_RHO, N_TRIALS_T0024, MECHANISM_SCHACHTER2010)"`
   prints `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0) 0.6 10 schachter2010_amplification`. Satisfies
   REQ-4.

2. **[CRITICAL] Create `code/distal_selector_t0024.py` and `code/diameter_override_t0024.py`.** Copy
   `tasks/t0034_distal_dendrite_length_sweep_t0024/code/distal_selector_t0024.py` (27 lines)
   verbatim; the single function `identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]`
   returns `list(cell.terminal_dends)`. **Do NOT use `h.RGC.ON`** — that attribute does not exist on
   the t0024 morphology. Copy
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py` (119 lines) into
   `code/diameter_override_t0024.py` and drop the `identify_distal_sections` and
   `_on_arbor_section_names` helpers (t0022-specific `h.RGC.ON` walk). Keep
   `snapshot_distal_diameters(*, h, distal_sections) -> dict[tuple[int, float], float]`,
   `set_distal_diameter_multiplier(*, h, distal_sections, baseline_diam, multiplier) -> None`,
   `assert_distal_diameters(*, h, distal_sections, baseline_diam, multiplier, tol = DIAMETER_ASSERT_TOL_UM) -> None`
   verbatim (~85 lines final). Update the `DIAMETER_ASSERT_TOL_UM` import to the t0035 `constants`
   module. Inputs: t0030 source, t0034 source, t0024 `build_cell.DSGCCell`. Outputs:
   `code/distal_selector_t0024.py` (~27 lines), `code/diameter_override_t0024.py` (~85 lines).
   Expected observable output:
   `uv run python -c "from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.distal_selector_t0024 import identify_distal_sections_t0024; from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.diameter_override_t0024 import snapshot_distal_diameters, set_distal_diameter_multiplier, assert_distal_diameters; print('ok')"`
   succeeds without import errors. Satisfies REQ-2, REQ-3.

3. **[CRITICAL] Preflight: build cell and log distal-section distribution.** Create
   `code/preflight_distal.py` (~160 lines) by copying
   `tasks/t0034_distal_dendrite_length_sweep_t0024/code/preflight_distal.py` (158 lines). Adapt: (a)
   swap `snapshot_distal_lengths` for `snapshot_distal_diameters`; (b) rename the JSON summary
   fields from `*_L_um` to `*_diam_um` and keep depth counts unchanged; (c) compute baseline
   per-segment min/median/max/mean `seg.diam` across all `(section, segment)` pairs; (d) optionally
   compute per-section `sec.L / sec.lambda_f` at `multiplier=2.0` (applied via a dummy
   snapshot/restore cycle in preflight) and log any violations of the d_lambda rule. Write
   `logs/preflight/distal_sections.json`:
   `{"count": <int>, "segment_count": <int>, "min_depth": <int>, "median_depth": <int>, "max_depth": <int>, "min_diam_um": <float>, "median_diam_um": <float>, "max_diam_um": <float>, "mean_diam_um": <float>, "identification_rule": "t0024_terminal_dends", "d_lambda_2x_violations": <int>}`.
   **Validation gate (preflight)**: if `len(distal_sections) < 50`, log WARN but do not halt (t0024
   is expected to have ~177 terminals per research_code.md); if `min_depth < 3`, log WARN
   (thresholds may be miscalibrated for `RGCmodelGD.hoc`). Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0035_distal_dendrite_diameter_sweep_t0024 -- uv run python -u -m tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.preflight_distal`.
   Expected wall time ~30 s. Expected observable output: `distal_sections.json` exists with
   `count >= 50` (likely ~177 per research_code.md) and no Python tracebacks. Satisfies REQ-2.

### Milestone B: Driver implementation

4. **Create `code/trial_runner_diameter_t0024.py`.** Copy
   `tasks/t0034_distal_dendrite_length_sweep_t0024/code/trial_runner_length_t0024.py` (180 lines) as
   the starting skeleton. Adapt (~180 lines final):

   * Rename `CellContextT0024Length` → `CellContextT0024Diameter`.
   * Replace `baseline_L: dict[int, float]` with `baseline_diam: dict[tuple[int, float], float]`;
     keep `cell: DSGCCell`, `bundle: SynapseBundle`, `distal_sections: list[Any]`,
     `current_multiplier: float = 1.0`.
   * In `build_cell_context()`, after `build_dsgc_cell()` and `_setup_synapses(...)`, call
     `distal_sections = identify_distal_sections_t0024(cell=cell)` and
     `baseline_diam = snapshot_distal_diameters(h=cell.h, distal_sections=distal_sections)`.
   * Replace `run_one_trial_length` with
     `run_one_trial_diameter(*, ctx: CellContextT0024Diameter, direction_deg: float, trial_seed: int) -> TrialResult`.
   * **AR(2) rho capture**: at module scope, `_AR2_RHO: float = C.AR2_CROSS_CORR_RHO_CORRELATED`
     (captured once, never overridden). Do NOT accept `rho` as a function parameter. Satisfies
     REQ-6.
   * Inside `run_one_trial_diameter`, do NOT call `set_distal_diameter_multiplier` — the outer sweep
     driver handles that once per sweep point. Keep the per-trial sequence: `_bar_arrival_times` →
     `_rates_with_ar2_noise(rho=_AR2_RHO, seed=trial_seed)` → `_rates_to_events` → NetCon event
     queue → `fih = h.FInitializeHandler(_queue); _ = fih` (keep-alive; without it the event queue
     is empty, a silent failure) → `h.finitialize(C.V_INIT_MV)` → `h.run()` (NOT `h.continuerun`) →
     `_count_spikes`.
   * Return `TrialResult(spike_count: int, peak_mv: float, firing_rate_hz: float)` where
     `firing_rate_hz = spike_count / (C.TSTOP_MS / 1000.0)`.

   Inputs: t0034 source, t0024 library. Outputs: `code/trial_runner_diameter_t0024.py` (~180 lines).
   Expected observable output:
   `uv run python -c "from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.trial_runner_diameter_t0024 import build_cell_context, run_one_trial_diameter; print('ok')"`
   succeeds. Satisfies REQ-1, REQ-5, REQ-6.

5. **[CRITICAL] Create `code/run_sweep.py`.** Copy
   `tasks/t0034_distal_dendrite_length_sweep_t0024/code/run_sweep.py` (293 lines) as the starting
   skeleton. Adapt (~300 lines final):

   * Replace length-specific imports with diameter equivalents; import `DIAMETER_MULTIPLIERS`,
     `PREFLIGHT_DIAMETER_MULTIPLIERS`, `AR2_RHO`, `N_TRIALS_T0024`, `SEED_DIAMETER_STRIDE`,
     `SEED_ANGLE_STRIDE`, `DIAMETER_ASSERT_TOL_UM`, `TIDY_CSV_HEADER`, `CURVE_CSV_HEADER` from
     `.constants`; import `build_cell_context` and `run_one_trial_diameter` from
     `.trial_runner_diameter_t0024`; import `set_distal_diameter_multiplier`,
     `assert_distal_diameters` from `.diameter_override_t0024`.
   * **AR(2) rho guard (start-up assertion)**: `assert C.AR2_CROSS_CORR_RHO_CORRELATED == AR2_RHO`
     raises if a later t0024 library edit silently changes the correlation (REQ-6).
   * Outer loop: `for diameter_idx, multiplier in enumerate(DIAMETER_MULTIPLIERS):`. Inside, call
     `set_distal_diameter_multiplier(h=ctx.cell.h, distal_sections=ctx.distal_sections, baseline_diam=ctx.baseline_diam, multiplier=multiplier)`
     then
     `assert_distal_diameters(h=ctx.cell.h, distal_sections=ctx.distal_sections, baseline_diam=ctx.baseline_diam, multiplier=multiplier, tol=DIAMETER_ASSERT_TOL_UM)`
     ONCE per outer iteration. Inner loops:
     `for angle_idx, direction_deg in enumerate(C.ANGLES_12ANG_DEG):` and
     `for trial_idx in range(N_TRIALS_T0024):`.
   * Seed convention (REQ-16):
     `trial_seed = diameter_idx * SEED_DIAMETER_STRIDE + SEED_ANGLE_STRIDE * angle_idx + trial_idx + 1`.
     Collect every emitted `trial_seed` into a `set[int]` during the run.
   * Tidy CSV schema per row: `TIDY_CSV_HEADER`. Open in append mode with line buffering; call
     `fh.flush()` after every write (REQ-13).
   * After each outer iteration, emit per-diameter canonical curve CSV at
     `results/data/per_diameter/tuning_curve_D<label>.csv` (label via `paths._multiplier_label`)
     with schema `CURVE_CSV_HEADER` (t0012 scorer input).
   * Emit `results/data/wall_time_by_diameter.json` with `{ "D<label>": <seconds>, ... }`.
   * Post-sweep: call `set_distal_diameter_multiplier(..., multiplier=1.0)` +
     `assert_distal_diameters(..., multiplier=1.0, tol=DIAMETER_ASSERT_TOL_UM)` to restore baseline
     and confirm idempotence.
   * Post-sweep: `assert len(seed_set) == 7 * 12 * N_TRIALS_T0024 == 840` (REQ-16).
   * CLI flags: `--preflight` (run `PREFLIGHT_DIAMETER_MULTIPLIERS = (0.5, 1.0, 2.0)` × 3 angles × 2
     trials = 18 trials), `--output <path>`.

   Inputs: t0034 source; `trial_runner_diameter_t0024`; t0024 constants. Outputs:
   `code/run_sweep.py` (~300 lines). Expected observable output: module imports cleanly. Satisfies
   REQ-1, REQ-4, REQ-5, REQ-6, REQ-13, REQ-16.

6. **[CRITICAL] Validation gate: run `run_sweep.py --preflight`.** Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0035_distal_dendrite_diameter_sweep_t0024 -- uv run python -u -m tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.run_sweep --preflight`.
   Expected runtime: **~4-5 min** (18 trials × ~12 s/trial; thinner 0.5× point runs slower).
   Expected observable output: 18 tidy-CSV rows with non-NaN `firing_rate_hz`; three per-diameter
   canonical CSVs emitted (`tuning_curve_D0p50.csv`, `tuning_curve_D1p00.csv`,
   `tuning_curve_D2p00.csv`), each with 6 rows (3 angles × 2 trials).

   **Validation gate thresholds** (expensive-operation gate per experiment-run guidelines):

   * **Trivial baseline**: t0026's V_rest sweep on t0024 at `V_rest=-60 mV` (our fixed condition)
     reported primary DSI ~0.50-0.55, peak firing ~4-5 Hz, null firing ~1-2 Hz. The preflight 1.0×
     midpoint must reproduce **primary DSI ≥ 0.3** and **peak_hz ≥ 2.0** (loose because preflight
     uses only 2 trials per angle). **Failure condition**: if primary DSI at `multiplier=1.0` is **≤
     0.3** (at or below the loose baseline), **STOP and debug** — do not proceed to the full
     840-trial sweep. Debug by running a single-trial case
     `(multiplier=1.0, direction_deg=120, trial_seed=1)` and diffing against t0026's single-trial
     output at `V_rest=-60 mV`.
   * **Individual-output inspection**: read the 6 preflight CSV rows for `multiplier=1.0`; confirm
     `spike_count` is in `[0, 20]` (biologically plausible) and `peak_mv` is in `[-70, +60]`
     (physiological) for each row. If any row has `spike_count > 50` or `peak_mv > +80`, STOP — a
     unit or overflow bug.
   * **AR(2) preservation check**: confirm `_AR2_RHO == 0.6` is used in every trial (start-up
     assertion in `run_sweep.py` raises if violated).
   * **Diameter override check**: after the preflight's 2.0× iteration,
     `assert_distal_diameters(...)` must pass within `DIAMETER_ASSERT_TOL_UM = 1e-6` µm; after the
     post-sweep `multiplier=1.0` restoration, assert again.

   Satisfies REQ-1, REQ-5, REQ-6.

7. **[CRITICAL] Run the full sweep.** Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0035_distal_dendrite_diameter_sweep_t0024 -- uv run python -u -m tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.run_sweep --output results/data/sweep_results.csv`.
   Expected runtime: **~2.8-3 h** (840 trials × ~12 s/trial on t0024 per t0026 anchor; thinner
   diameters add ~10-15% overhead per t0030 observation). Unattended. Inputs: t0024 library, local
   code. Outputs: `results/data/sweep_results.csv` (841 lines = 1 header + 840 data rows), seven
   per-diameter canonical CSVs in `results/data/per_diameter/`,
   `results/data/wall_time_by_diameter.json`. Per-row `fh.flush()` enables crash recovery (REQ-13).
   Post-run: assertions restore and confirm baseline `seg.diam` within
   `DIAMETER_ASSERT_TOL_UM = 1e-6` µm; seed-uniqueness assertion checks `len(seed_set) == 840`.
   Expected observable output: 840 data rows, 7 distinct `diameter_multiplier` values, 12 distinct
   `direction_deg` values per multiplier, no NaN `firing_rate_hz`, no `AssertionError`. Satisfies
   REQ-4, REQ-5, REQ-6, REQ-13, REQ-14, REQ-16.

### Milestone C: Metrics, classification, and charts

8. **Create `code/analyse_sweep.py`.** Copy
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/analyse_sweep.py` (336 lines) as the
   starting skeleton. Adapt:

   * Retarget paths to the t0035 `paths` module.
   * For each sweep point, call
     `compute_dsi(curve=load_tuning_curve(csv_path=per_diameter_curve_csv(multiplier=m)))` as the
     primary DSI.
   * Compute vector-sum DSI via the `_vector_sum_dsi` helper (copied verbatim from t0030).
   * Compute `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`.
   * Compute preferred-direction angle (argmax of per-angle mean firing rate) and
     preferred-direction firing rate.
   * Compute mean peak mV per sweep point from the tidy CSV.
   * Write `results/data/metrics_per_diameter.csv` with columns
     `(diameter_multiplier, dsi_primary, dsi_vector_sum, peak_hz, null_hz, hwhm_deg, reliability, preferred_direction_deg, preferred_hz, mean_peak_mv)`.
   * Write `results/metrics.json` using the **explicit multi-variant format** (per
     `arf/specifications/metrics_specification.md`): 7 variants keyed `diameter_0p50`,
     `diameter_0p75`, ..., `diameter_2p00`, each with `dimensions={"diameter_multiplier": <m>}` and
     `metrics={"direction_selectivity_index": <dsi_primary>, "tuning_curve_hwhm_deg": <hwhm>, "tuning_curve_reliability": <rel>}`.
   * Omit `tuning_curve_rmse` (stimulus biophysics unchanged except for `seg.diam`; no target curve
     is meaningful here). Record the omission in `results/data/metrics_notes.json`.

   Registered metrics measurement mapping (applicable metrics confirmed via
   `aggregate_metrics --format ids`):

   * `direction_selectivity_index` — one value per variant (step 8; uses `compute_dsi`).
   * `tuning_curve_hwhm_deg` — one value per variant (step 8; uses `compute_hwhm_deg`).
   * `tuning_curve_reliability` — one value per variant (step 8; uses `compute_reliability`).
   * `tuning_curve_rmse` — **not applicable** (no target curve; omission documented in
     `metrics_notes.json`).

   Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0035_distal_dendrite_diameter_sweep_t0024 -- uv run python -u -m tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.analyse_sweep`.
   Expected observable output: `metrics.json` contains `variants` key with 7 entries;
   `metrics_per_diameter.csv` has 7 rows. Satisfies REQ-5, REQ-7, REQ-15.

9. **Create `code/classify_slope.py`.** Copy
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/classify_slope.py` (314 lines) as the
   starting skeleton. Adapt:

   * Retarget paths to the t0035 `paths` module.
   * Classify using `dsi_primary` column as the primary signal. Fit
     `dsi_primary ~ beta * log2(diameter_multiplier) + alpha` using `scipy.stats.linregress`.
   * Apply t0030 thresholds (`MAX_P_VALUE = 0.05`, `MIN_SLOPE_MAGNITUDE = 0.05`,
     `DSI_RANGE_MIN_FOR_CONFIDENT_LABEL = 0.05`, `DSI_SATURATION_THRESHOLD = 0.02`).
   * Output labels: `schachter2010_amplification` (positive, p<0.05, `dsi_range_extremes ≥ 0.05`),
     `passive_filtering` (negative, p<0.05, `dsi_range_extremes ≤ -0.05`), or `flat` (REQ-12).
   * **Fallback (REQ-9)**: if primary DSI range (`max - min`) ≤ `DSI_SATURATION_THRESHOLD = 0.02`,
     re-fit on `dsi_vector_sum` and classify using the vector-sum slope sign. Emit
     `shape_class_vector_sum` and `slope_vector_sum` / `p_value_vector_sum` alongside the primary
     classification as a secondary check regardless of saturation.
   * Write `results/data/curve_shape.json` and `results/data/slope_classification.json` with every
     underlying quantity: `mechanism_class`, `slope`, `intercept`, `r_squared`, `p_value`,
     `slope_95_ci_low`, `slope_95_ci_high`, `dsi_range_extremes`, `shape_class_vector_sum`,
     `slope_vector_sum`, `p_value_vector_sum`, `qualitative_description`, and a
     `t0030_comparison_note` summarising how the t0024 slope contrasts with t0030's
     `dsi_primary = 1.000` null (REQ-17).

   Execute:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0035_distal_dendrite_diameter_sweep_t0024 -- uv run python -u -m tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.classify_slope`.
   Expected observable output: `slope_classification.json` with `mechanism_class` in
   `{"schachter2010_amplification", "passive_filtering", "flat"}`. Satisfies REQ-8, REQ-9, REQ-12,
   REQ-17.

10. **Create `code/plot_sweep.py`.** Copy
    `tasks/t0034_distal_dendrite_length_sweep_t0024/code/plot_sweep.py` (422 lines) as the starting
    skeleton. Adapt (rename axis labels, file names, and output paths; keep the four-chart
    structure):

    * `results/images/dsi_vs_diameter.png` (primary, REQ-8): Cartesian two-panel — left y-axis
      `dsi_primary` (Okabe-Ito blue) with regression line if `mechanism_class` ≠ `flat`; right
      y-axis `peak_hz` (Okabe-Ito orange); x-axis `diameter_multiplier` on a log-2 scale so the
      regression is symmetric around 1.0×. Baseline (1.0×) annotated with a star. Title carries
      `mechanism_class`.
    * `results/images/vector_sum_dsi_vs_diameter.png` (secondary / defensive fallback, REQ-9):
      single-panel Cartesian, `dsi_vector_sum` vs `diameter_multiplier`. Carries
      `shape_class_vector_sum` in the title — if primary DSI saturates at some sweep points, this
      chart remains resolvable.
    * `results/images/polar_overlay.png` (REQ-10): single polar axes with seven coloured lines, one
      per diameter multiplier. Use `plot_polar_tuning_curve` from the t0011 library for the base
      rendering; colour palette: viridis across the 7 multipliers; legend shows multiplier labels.
    * `results/images/peak_hz_vs_diameter.png` (REQ-11): single-panel Cartesian, `peak_hz` and
      `null_hz` overlaid vs `diameter_multiplier` (two lines, Okabe-Ito palette) — the mechanism
      signature. Schachter2010: peak rises with diameter, null flat. Passive: both decline, null
      less so.

    Save all charts at 300 dpi. Execute:
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0035_distal_dendrite_diameter_sweep_t0024 -- uv run python -u -m tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.plot_sweep`.
    Expected observable output: four PNGs in `results/images/`, each > 20 KB. Satisfies REQ-8,
    REQ-9, REQ-10, REQ-11.

## Remote Machines

**None required.** The entire sweep runs on the local Windows workstation CPU. Per the research-code
wall-time anchor from t0026, t0024 runs at ~12 s per (angle, trial) — significantly slower than
t0022's ~3.5 s/trial because of the AR(2) stochastic rate-generation pass. Total sweep = 7
multipliers × 12 angles × 10 trials = 840 trials × ~12 s ≈ 168 min ≈ **~2.8 h**; plus ~10-15%
overhead at the thinner-diameter multipliers (0.5×) per t0030 observation (raised axial resistance
shrinks NEURON's integration timestep). Plus ~30 s cell-build overhead and ~4-5 min preflight. No
GPU, no cloud. The task description confirms "Local CPU only. No remote compute, no paid API."

## Assets Needed

Input assets this task depends on:

* **`de_rosenroll_2026_dsgc`** (library, registered) — from t0024. Source:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`. Provides
  `build_dsgc_cell`, `DSGCCell`, `_setup_synapses`, `_bar_arrival_times`, `_rates_with_ar2_noise`,
  `_rates_to_events`, `_gaba_prob_for_direction`, `_count_spikes`, `SynapseBundle`, and all t0024
  constants (`AR2_CROSS_CORR_RHO_CORRELATED = 0.6`, `TSTOP_MS`, `V_INIT_MV`, `ANGLES_12ANG_DEG`,
  etc.). The HOC template `RGCmodelGD.hoc` and compiled MOD mechanisms are vendored under `sources/`
  inside this asset.
* **`tuning_curve_loss`** (library, registered) — from t0012. Source:
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`. Provides
  `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`,
  `load_tuning_curve`, `TuningCurve`.
* **`tuning_curve_viz`** (library, registered, optional) — from t0011. Source:
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`. Provides
  `plot_polar_tuning_curve` used by `plot_sweep.py` for the polar overlay chart.
* **t0030 workflow template (file-level copies, not library imports)** — source:
  `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/`. The structural clones of `constants.py`
  (slope-sign taxonomy), `diameter_override.py` (snapshot / rescale / assert helpers),
  `analyse_sweep.py`, and `classify_slope.py` are all copied per CLAUDE.md rule 9 (no cross-task
  imports from non-library task folders).
* **t0034 workflow template (file-level copies)** — source:
  `tasks/t0034_distal_dendrite_length_sweep_t0024/code/`. Structural clones of `paths.py`,
  `distal_selector_t0024.py`, `preflight_distal.py`, `trial_runner_length_t0024.py`, `run_sweep.py`,
  and `plot_sweep.py` (each adapted to diameter).

## Expected Assets

`task.json` declares `expected_assets: {}` — no paper, dataset, library, model, predictions, or
answer assets are produced. This is a pure experiment-run task whose deliverables are metrics,
charts, and the slope-sign classification, all of which live under `results/`. The expected output
artefacts (non-assets, delivered under `tasks/t0035_distal_dendrite_diameter_sweep_t0024/`):

* `results/data/sweep_results.csv` — 840 tidy trial rows (7 multipliers × 12 angles × 10 trials).
* `results/data/per_diameter/tuning_curve_D<label>.csv` × 7 — canonical 120-row tuning-curve CSVs
  consumed by the t0012 scorer (schema: `angle_deg, trial_seed, firing_rate_hz`).
* `results/data/metrics_per_diameter.csv` — one row per diameter with primary DSI, vector-sum DSI,
  peak Hz, null Hz, HWHM, reliability, preferred-direction angle, preferred-direction firing rate,
  mean peak mV.
* `results/data/curve_shape.json` / `results/data/slope_classification.json` — primary-DSI mechanism
  classification (`schachter2010_amplification` / `passive_filtering` / `flat`) plus vector-sum-DSI
  secondary classification, slope / p-value / 95% CI, `dsi_range_extremes`, qualitative description,
  `t0030_comparison_note`.
* `results/data/metrics_notes.json` — documents the intentional omission of `tuning_curve_rmse`.
* `results/data/wall_time_by_diameter.json` — per-sweep-point wall time.
* `results/metrics.json` — explicit multi-variant format with 7 diameter variants.
* `results/images/dsi_vs_diameter.png` — primary chart (DSI + peak Hz vs multiplier) with regression
  overlay if slope is significant.
* `results/images/vector_sum_dsi_vs_diameter.png` — defensive fallback chart.
* `results/images/polar_overlay.png` — 7-line viridis polar overlay of tuning curves.
* `results/images/peak_hz_vs_diameter.png` — peak + null Hz diagnostic chart (mechanism signature).
* `logs/preflight/distal_sections.json` — distal identification rule, counts, depth, and baseline
  diameter distribution.

## Time Estimation

* Research: already complete (`research/research_code.md`; no further research needed). 0 h.
* Planning: this document. ~1 h.
* Implementation:
  * Milestone A (steps 1-3, setup + preflight): ~1 h coding + ~5 min runtime.
  * Milestone B step 4 (trial runner): ~45 min coding.
  * Milestone B step 5 (sweep driver): ~40 min coding.
  * Milestone B step 6 (preflight sweep validation gate): ~4-5 min runtime + ~15 min triage.
  * Milestone B step 7 (full sweep run): **~2.8-3 h runtime (unattended)**.
  * Milestone C steps 8-10 (metrics + classification + charts): ~1.5 h coding + <1 min runtime.
* Validation and coverage check: ~30 min.

**Total implementation wall time: ~7.5-8 h** (~2.8-3 h of which is unattended simulation;
human-engaged ~4.7-5 h for coding, triage, and verification).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Primary DSI saturates across the whole sweep (AR(2) noise insufficient at some sweep points to sustain null firing, collapsing dynamic range). Research-code predicts 0.2-0.4 range; t0034 length-sweep observed 0.545-0.774. If thinner diameters raise distal input impedance to the point that null-direction synaptic currents fail to reach the soma, null_hz may drop below threshold and primary DSI may pin at 1.0 at some sweep points. | Medium-Low | Medium | `analyse_sweep.py` computes vector-sum DSI and per-angle peak/null rates at every sweep point; `classify_slope.py` auto-falls-back to vector-sum DSI when `max(dsi_primary) - min(dsi_primary) <= DSI_SATURATION_THRESHOLD = 0.02`. `vector_sum_dsi_vs_diameter.png` is emitted unconditionally as a defensive secondary chart. The peak-Hz/null-Hz diagnostic plot still distinguishes Schachter2010 (peak rises, null flat) from passive filtering (both decline) even if DSI itself saturates. |
| t0024 morphology distal distribution differs from t0022; count or depth thresholds inherited from t0030 may not fit. Research-code notes t0024 has 177 terminals (well above 50) but depth distribution is unmeasured. | Medium | Low | Preflight step 3 relaxes `DISTAL_MIN_COUNT` and `DISTAL_MIN_DEPTH` to warn-only (logged in `distal_sections.json`, not asserted). Human reviewer decides whether the relaxed set is acceptable before step 7. If unacceptable, create `intervention/distal_identification_recalibration.json` and halt. |
| Thinner diameter (0.5×) violates d_lambda rule at `nseg=1` (under-resolved segmentation when axial resistance is high enough that `sec.L / sec.lambda_f > 0.2`). | Medium | Low | Preflight step 3 logs per-section `sec.L / sec.lambda_f` at `multiplier=0.5` and `multiplier=2.0` (via a dummy snapshot/restore cycle) and records any violations. Post-sweep, if violation detected, re-run the offending multiplier with adaptive `nseg = ceil(L / (0.1 * lambda_f))` and update the corresponding row in `metrics_per_diameter.csv` as a follow-up correction. Does not block the main sweep. |
| NEURON crash or Windows-specific DLL issue during the ~2.8-3 h unattended run. | Low-Medium | High | Crash recovery via per-row `fh.flush()` (REQ-13). On restart, the sweep driver can resume from the last completed `(diameter_multiplier, trial, direction_deg)` tuple or re-run fully (cell build is only ~30 s). Acceptance: at least 836/840 trials (99.5%) must succeed; if fewer, halt and debug. Run from a clean Python process each attempt (NEURON global state can leak across processes). |
| Baseline `seg.diam` not restored after sweep, corrupting downstream use of the live cell handle. | Low | Medium | Post-sweep assertion in step 7 calls `set_distal_diameter_multiplier(..., multiplier=1.0)` + `assert_distal_diameters(..., multiplier=1.0, tol=DIAMETER_ASSERT_TOL_UM = 1e-6)`; failure raises `AssertionError`. Pattern borrowed from t0034's `run_sweep.py`. |
| `h.RGC.ON` attribute access in an overlooked t0030 copy-paste raises `AttributeError` on t0024. | Low | Blocking | Grep-verification in Verification Criteria confirms no file under `tasks/t0035_.../code/` contains `h.RGC.ON` or `RGC.ON`. `distal_selector_t0024.py` is the only legitimate distal selector in this task. |
| Thinner-diameter slowdown blows the time budget (carried over from t0030: raised axial resistance shrinks the adaptive NEURON timestep). | Medium | Low | Wall-time checkpoint `wall_time_by_diameter.json` records per-sweep-point runtime; if the 0.5× point exceeds 30 min, log WARN and continue (the full budget is still within the ~3.5 h ceiling). Run is unattended — a 10-15% overhead is acceptable. |
| Slope thresholds (`MIN_SLOPE_MAGNITUDE = 0.05`) were calibrated for t0030 on t0022 but t0024's expected DSI range is different. On a measurable 0.2-0.4 range, a 0.05 slope per `log2(multiplier)` unit represents a 0.1 DSI change across the 0.5×→2.0× range (log2 span = 2.0) — detectable but modest. | Medium | Low | `classify_slope.py` emits raw slope, 95% CI, R-squared, p-value, and `dsi_range_extremes` alongside the categorical `mechanism_class`. A human reviewer can override the automatic label in `results_detailed.md` if the thresholds are too strict or too loose. The vector-sum secondary classification provides an independent check. |
| Per-trial AR(2) seed collision produces non-unique random streams across the 840 trials (seed-formula bug). | Low | Low | `run_sweep.py` asserts `len(seed_set) == 840` post-sweep (REQ-16). The preflight (18 trials) exercises the same seed formula at small scale, catching collisions early. |

## Verification Criteria

Testable checks run at the end of implementation:

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0035_distal_dendrite_diameter_sweep_t0024 -- uv run python -u -m arf.scripts.verificators.verify_plan t0035_distal_dendrite_diameter_sweep_t0024`;
  expect zero errors.
* Run
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open('tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/data/sweep_results.csv'))); assert len(rows) == 840, len(rows); assert len({r['diameter_multiplier'] for r in rows}) == 7; assert all(r['firing_rate_hz'] not in ('', 'nan', 'NaN') for r in rows); print('OK', len(rows))"`;
  expect `OK 840` (confirms REQ-4 and REQ-5).
* Run
  `uv run python -u -c "import json, pathlib; m = json.loads(pathlib.Path('tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/metrics.json').read_text()); assert 'variants' in m and len(m['variants']) == 7; assert all('direction_selectivity_index' in v['metrics'] for v in m['variants']); print('OK')"`;
  expect `OK` (confirms REQ-5, REQ-7, and registered-metric coverage — 7 variants with DSI).
* Run
  `uv run python -u -c "import pathlib; imgs = ['dsi_vs_diameter.png','vector_sum_dsi_vs_diameter.png','polar_overlay.png','peak_hz_vs_diameter.png']; [print('OK', p, pathlib.Path(f'tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/images/{p}').stat().st_size) for p in imgs if pathlib.Path(f'tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/images/{p}').exists() and pathlib.Path(f'tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/images/{p}').stat().st_size > 20000]"`;
  expect four `OK ...` lines with sizes > 20000 bytes each (confirms REQ-8, REQ-9, REQ-10, REQ-11).
* Run
  `uv run python -u -c "import json, pathlib; s = json.loads(pathlib.Path('tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/data/slope_classification.json').read_text()); assert s['mechanism_class'] in ('schachter2010_amplification','passive_filtering','flat'); assert 'shape_class_vector_sum' in s; assert 't0030_comparison_note' in s; print('OK', s['mechanism_class'], s['shape_class_vector_sum'])"`;
  expect `OK <primary> <secondary>` (confirms REQ-8, REQ-9, REQ-12, REQ-17 classification + t0030
  comparison).
* Run
  `uv run python -u -c "import json, pathlib; p = json.loads(pathlib.Path('tasks/t0035_distal_dendrite_diameter_sweep_t0024/logs/preflight/distal_sections.json').read_text()); assert p['count'] > 0 and p['identification_rule'] == 't0024_terminal_dends'; print('OK', p['count'], p.get('min_depth'))"`;
  expect `OK <count> <min_depth>` (confirms REQ-2 — t0024-specific distal rule used, not
  `h.RGC.ON`).
* Run
  `uv run python -u -c "import pathlib, re; files = list(pathlib.Path('tasks/t0035_distal_dendrite_diameter_sweep_t0024/code').glob('*.py')); bad = [(f.name, i+1) for f in files for i, line in enumerate(f.read_text(encoding='utf-8').splitlines()) if re.search(r'h\\.RGC\\.ON|RGC\\.ON\\b', line)]; assert not bad, f'h.RGC.ON found: {bad}'; print('OK no h.RGC.ON references in', len(files), 'files')"`;
  expect `OK no h.RGC.ON references in N files` (confirms REQ-2 — t0024-specific selector used).
* Run
  `uv run python -u -c "import pathlib, re; files = list(pathlib.Path('tasks/t0035_distal_dendrite_diameter_sweep_t0024/code').glob('*.py')); bad = [(f.name, i+1) for f in files for i, line in enumerate(f.read_text(encoding='utf-8').splitlines()) if re.search(r'from\\s+tasks\\.t0030_', line)]; assert not bad, f'cross-task import from t0030: {bad}'; print('OK no t0030 imports')"`;
  expect `OK no t0030 imports` (confirms REQ-3 — helper was copied, not imported).
* Run
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open('tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/data/metrics_per_diameter.csv'))); cols = {'dsi_primary','dsi_vector_sum','peak_hz','null_hz','hwhm_deg','reliability','preferred_direction_deg','preferred_hz','mean_peak_mv'}; assert cols.issubset(rows[0].keys()), set(rows[0].keys()) - cols; print('OK', len(rows), 'rows')"`;
  expect `OK 7 rows` (confirms REQ-7 — secondary metrics present).
* Run
  `uv run ruff check --fix . && uv run ruff format . && uv run mypy tasks/t0035_distal_dendrite_diameter_sweep_t0024`;
  expect zero errors and zero warnings.
* REQ-coverage check: every `REQ-*` ID in `## Task Requirement Checklist` is mentioned in at least
  one numbered step (`## Step by Step`) or in the Verification Criteria. Run
  `uv run python -u -c "import re, pathlib; t = pathlib.Path('tasks/t0035_distal_dendrite_diameter_sweep_t0024/plan/plan.md').read_text(encoding='utf-8'); reqs = set(re.findall(r'REQ-\\d+', t)); print(sorted(reqs, key=lambda s: int(s.split('-')[1])))"`;
  expect exactly
  `['REQ-1', 'REQ-2', 'REQ-3', 'REQ-4', 'REQ-5', 'REQ-6', 'REQ-7', 'REQ-8', 'REQ-9', 'REQ-10', 'REQ-11', 'REQ-12', 'REQ-13', 'REQ-14', 'REQ-15', 'REQ-16', 'REQ-17']`.
