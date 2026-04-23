---
spec_version: "1"
task_id: "t0035_distal_dendrite_diameter_sweep_t0024"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 5
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-23"
status: "complete"
---
# Research Code: Distal-Dendrite Diameter Sweep on t0024 DSGC

## Task Objective

Sweep distal-dendrite diameter across 7 multipliers (0.5× to 2.0× baseline) on the t0024 de
Rosenroll 2026 DSGC port, then classify the primary DSI-vs-diameter slope sign to discriminate
between Schachter2010 active-dendrite amplification (positive slope — thicker distal compartments
host more Nav substrate and amplify preferred-direction local spikes) and passive-filtering
alternatives (negative slope — thicker dendrites lower input impedance, reducing directional
contrast). The sibling task t0030 produced a null result on t0022 because its deterministic E-I
driver pins null firing at 0 Hz and primary DSI at 1.000. The t0024 port's AR(2)-correlated
stochastic release (ρ=0.6) restores non-zero null firing (0.70-1.00 Hz per t0034 confirmation),
giving primary DSI a dynamic range that can express a mechanistic slope. The sweep runs the standard
12-direction × 10-trial protocol (840 trials total); expected wall time is approximately 2.8 hours
on the local Windows CPU. This task covers source suggestion S-0027-03.

## Library Landscape

The library aggregator script (`arf/scripts/aggregators/aggregate_libraries.py`) is not present in
this repository — the project uses a subset of the full ARF aggregator suite and
`aggregate_libraries.py` is not among the scripts in `arf/scripts/aggregators/`. There are therefore
**0 registered library assets** discoverable via the aggregator. However, one de-facto library
exists: the `tuning_curve_loss` package located at
`tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/` (produced by [t0012]). It is
not registered via a library aggregator but is imported by every sweep task (t0026, t0029, t0030,
t0034) as a cross-task import from
`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`. Its public API (13 entry
points including `compute_dsi`, `compute_hwhm_deg`, `compute_reliability`, `score`) is relevant to
this task for per-diameter DSI and HWHM computation. All other reusable components are non-library
code that must be copied into this task's `code/` directory.

## Key Findings

### t0024 Model Architecture and Driver Entry Points

The de Rosenroll 2026 DSGC port [t0024] is built around the `RGCmodelGD.hoc` morphology with 177
terminal dendrites enumerated via `DSGCCell.terminal_dends` (computed by `_map_tree` in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py`, 297 lines). `DSGCCell` is a frozen
dataclass exposing `h`, `rgc`, `soma`, `all_dends`, `primary_dends`, `non_terminal_dends`,
`terminal_dends: list[Any]`, `terminal_locs_xy: NDArray[np.float64]`, and `origin_xy`. The entry
point for building the cell is `build_dsgc_cell() -> DSGCCell` (no arguments). Unlike t0022, the
t0024 template uses a single unified arbor with no separate `h.RGC.ON` subtree attribute; the
canonical distal-leaf set is exactly `cell.terminal_dends`.

The per-trial simulation entry point is
`run_single_trial(*, cell, ncs_ach, ncs_gaba, direction_deg, rho, seed) -> TrialResult` in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py` (454 lines). This function
computes AR(2)-modulated ACh and GABA rate traces, converts them to Poisson spike-time events,
queues events via `h.FInitializeHandler`, and calls `h.finitialize` + `h.run`. The `rho` parameter
controls the AR(2) cross-channel correlation; it is set from `C.AR2_CROSS_CORR_RHO_CORRELATED = 0.6`
for the standard correlated condition. Helper functions exported from `run_tuning_curve.py` and
importable for sweep tasks include `_bar_arrival_times`, `_rates_with_ar2_noise`,
`_rates_to_events`, `_gaba_prob_for_direction`, `_count_spikes`, `_setup_synapses`, `SynapseBundle`,
`BASE_ACH_PROB`, and `RATE_DT_MS`.

### Distal-Section Identification Rule on t0024

The t0022 diameter-override helper in t0030's `diameter_override.py` uses `h.RGC.ON` name-matching
to identify ON-arbor sections, then checks `h.SectionRef(sec=sec).nchild() == 0` for leaf status
[t0030]. That path does not exist on the t0024 `RGCmodelGD.hoc` template. The t0034 companion task
[t0034] resolved this cleanly with a 27-line t0024-specific selector at
`tasks/t0034_distal_dendrite_length_sweep_t0024/code/distal_selector_t0024.py`. Its sole public
function is:

```python
def identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]:
    return list(cell.terminal_dends)
```

This wrapper exposes `DSGCCell.terminal_dends` — the leaf list computed by `build_cell.py`'s
`_map_tree` — under a t0024-specific name for unambiguous reading in downstream sweep code. This
exact module should be **copied** into `tasks/t0035.../code/distal_selector_t0024.py` with a
one-line import path change.

### Diameter-Override Pattern from t0030

The t0030 task [t0030] implemented `seg.diam` rescaling for t0022 in
`tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py` (119 lines). The key
semantic difference from t0034's length override is that `seg.diam` is a per-segment RANGE variable
(keyed by `(id(sec), float(seg.x))`), whereas `sec.L` is a section-level attribute (keyed by
`id(sec)` only). The four public functions in `diameter_override.py` are:

* `identify_distal_sections(*, h) -> list[Any]` — walks `h.RGC.ON` for t0022; not valid for t0024.
* `snapshot_distal_diameters(*, h, distal_sections) -> dict[tuple[int, float], float]` — snapshot
  `{(id(sec), seg.x): seg.diam}` per segment. Geometry-agnostic; valid for t0024 unchanged.
* `set_distal_diameter_multiplier(*, h, distal_sections, baseline_diam, multiplier) -> None` —
  assigns `seg.diam = baseline_diam[(id(sec), seg.x)] * multiplier`. Geometry-agnostic.
* `assert_distal_diameters(*, h, distal_sections, baseline_diam, multiplier, tol) -> None` — asserts
  all segments within `DIAMETER_ASSERT_TOL_UM = 1e-6` µm of target.

The t0035 `diameter_override_t0024.py` should **copy** `snapshot_distal_diameters`,
`set_distal_diameter_multiplier`, and `assert_distal_diameters` verbatim from t0030's module, and
**drop** `identify_distal_sections` and `_on_arbor_section_names` (which use the t0022-specific
`h.RGC.ON` path). The new module should import the `DIAMETER_ASSERT_TOL_UM` constant from its own
`constants.py` rather than t0030's.

### t0034 Trial Runner and Sweep Driver as Template

The t0034 task [t0034] provides a complete, working sweep pipeline for the t0024 port at
`tasks/t0034_distal_dendrite_length_sweep_t0024/code/`. The trial runner
`trial_runner_length_t0024.py` (180 lines) demonstrates the correct pattern: build the cell and
synapse bundle once via `build_cell_context() -> CellContextT0024Length`, then call
`run_one_trial_length(*, ctx, direction_deg, trial_seed) -> TrialOutcomeT0024Length` per trial
without rebuilding the cell. The AR(2) rho is captured once at module scope as
`_AR2_RHO: float = C.AR2_CROSS_CORR_RHO_CORRELATED` and never overridden at call sites, satisfying
the REQ-6 rho-preservation requirement. The sweep driver `run_sweep.py` (293 lines) calls
`set_distal_length_multiplier` **once per outer sweep iteration** (not per trial), confirms the
override with `assert_distal_lengths`, and includes a post-sweep baseline-restoration guardrail and
a seed-uniqueness assertion over all 840 seeds.

The diameter equivalent for t0035 should replicate this architecture with `sec.L` → `seg.diam`
semantics and `length_override_t0024` → `diameter_override_t0024`. The outer structure of
`run_sweep.py`, the seed formula, the preflight mode, the tidy CSV flushing after every row, and the
wall-time JSON checkpoint all carry over without change.

### Analysis and Classification: Slope vs Shape

t0030 uses a slope-sign classification scheme in `classify_slope.py` (314 lines) suited to the
diameter sweep [t0030]: it fits a linear regression of DSI vs `log2(multiplier)`, classifies the
slope as `schachter2010_amplification` (positive, p < 0.05, `dsi_range_extremes` >= 0.05),
`passive_filtering` (negative, analogous criteria), or `flat`. It includes a fallback to vector-sum
DSI when primary DSI saturates (`max - min <= DSI_SATURATION_THRESHOLD = 0.02`), which is the t0030
null-result path. Since t0024 is expected to have a non-trivial primary DSI range (t0034 produced
0.545-0.774 over a length sweep), the fallback is unlikely to trigger but should be preserved.

t0034 uses a shape-classification scheme (`classify_shape.py`, 250 lines) better suited to
monotonic/saturating/non-monotonic discrimination [t0034]. For t0035 the correct classifier is
t0030's `classify_slope.py`, because the scientific question (Schachter2010 vs passive) maps exactly
onto the slope-sign taxonomy. The `analyse_sweep.py` from t0030 (336 lines) computes per-diameter
metrics (mean DSI, vector-sum DSI, peak Hz, null Hz, HWHM, reliability) and writes
`results/data/metrics_per_diameter.csv` which feeds `classify_slope.py`. Both should be **copied**
into t0035's `code/` with path constants updated to the t0035 paths module.

### AR(2) Rho Preservation

Both t0034 and t0030 enforce that the AR(2) correlation is not silently changed between tasks. t0034
adds an explicit guard in `run_sweep.py`:

```python
assert C.AR2_CROSS_CORR_RHO_CORRELATED == AR2_RHO, (
    f"t0024 AR2_CROSS_CORR_RHO_CORRELATED drift: "
    f"expected {AR2_RHO}, got {C.AR2_CROSS_CORR_RHO_CORRELATED}"
)
```

where `AR2_RHO = 0.6` is pinned in the task's own `constants.py`. This guard must be retained in
t0035's `run_sweep.py` to satisfy REQ-6.

### t0030 Null Result and t0034 DSI Confirmation

t0030 [t0030] ran 840 trials on t0022 and found primary DSI pinned at 1.000 and vector-sum DSI flat
(slope 0.0083, p=0.1773, range 0.635-0.665). The null result was traced to t0022's deterministic E-I
driver silencing null firing at 0 Hz; the preferred-direction firing rate showed only a mild decline
(15 Hz → 13 Hz) with thickening, consistent with passive impedance changes that never break the
amplification regime (peak distal membrane voltage ~-5 mV, well above spike threshold). Wall time
was ~115 min at ~3.8 s/trial.

t0034 [t0034] ran the same 840-trial protocol on t0024 (length sweep) and confirmed measurable
primary DSI variation: range 0.545-0.774, slope -0.1259 per unit multiplier (p=0.038). Null firing
was 0.70-1.00 Hz across all lengths (never zero). Preferred-direction peak firing declined 40% (5.70
Hz → 3.40 Hz) monotonically. Wall time was approximately 3 hours at ~12 s/trial. The higher
per-trial cost on t0024 relative to t0022 is attributed to the AR(2) rate-generation pass over
n_bins × n_syn samples per trial. Thinner diameter multipliers will run slower on t0024 (same
behaviour as t0030 — raised axial resistance shrinks the NEURON integration timestep).

### V_rest Sweep Baseline

t0026 [t0026] established the t0024 operating baseline: at V_rest = -60 mV with ρ=0.6, DSI ranges
0.36-0.67 over the full V_rest sweep (1.9× modulation). Peak firing is 7.6 Hz at V_rest = -20 mV (no
Na-inactivation collapse), and HWHM is pinned 65-83° across the sweep. Wall time was ~3.21 h for 960
trials (10 trials × 12 angles × 8 V_rest values), confirming the ~12 s/trial estimate used in t0034
and t0035 planning.

## Reusable Code and Assets

### distal_selector_t0024.py — copy into task

**Source**: `tasks/t0034_distal_dendrite_length_sweep_t0024/code/distal_selector_t0024.py` (27
lines)

**What it does**: Returns `list(cell.terminal_dends)` as the canonical distal section set for the
t0024 morphology, through the function
`identify_distal_sections_t0024(*, cell: DSGCCell) -> list[Any]`.

**Reuse method**: **copy into task** as
`tasks/t0035_distal_dendrite_diameter_sweep_t0024/code/distal_selector_t0024.py`.

**Adaptation needed**: Update the import of `DSGCCell` to use the absolute path
`tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell`. No other changes required.

### diameter_override_t0024.py — copy into task (adapted from t0030)

**Source**: `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py` (119 lines)

**What it does**:
`snapshot_distal_diameters(*, h, distal_sections) -> dict[tuple[int, float], float]` snapshots
per-segment `(id(sec), seg.x) -> seg.diam`;
`set_distal_diameter_multiplier(*, h, distal_sections, baseline_diam, multiplier) -> None` rescales
each segment; `assert_distal_diameters` verifies the rescale within `DIAMETER_ASSERT_TOL_UM = 1e-6`
µm.

**Reuse method**: **copy into task** as
`tasks/t0035_distal_dendrite_diameter_sweep_t0024/code/diameter_override_t0024.py`.

**Adaptation needed**: Drop `identify_distal_sections` and `_on_arbor_section_names` (t0022-specific
`h.RGC.ON` walk). Update the `DIAMETER_ASSERT_TOL_UM` import to the t0035 constants module.
Approximately 85 lines after pruning.

### trial_runner_diameter_t0024.py — copy into task (adapted from t0034)

**Source**: `tasks/t0034_distal_dendrite_length_sweep_t0024/code/trial_runner_length_t0024.py` (180
lines)

**What it does**: `build_cell_context() -> CellContextT0024Diameter` builds the cell and synapse
bundle once; `run_one_trial_diameter(*, ctx, direction_deg, trial_seed) -> TrialOutcomeDiameter`
runs one trial with rho pinned at module scope to `C.AR2_CROSS_CORR_RHO_CORRELATED = 0.6`.

**Reuse method**: **copy into task** as `trial_runner_diameter_t0024.py`.

**Adaptation needed**: (1) Rename `CellContextT0024Length` → `CellContextT0024Diameter` and replace
`baseline_L: dict[int, float]` with `baseline_diam: dict[tuple[int, float], float]`. (2) Replace the
import of `identify_distal_sections_t0024` and `snapshot_distal_lengths` with the t0035 equivalents.
(3) The trial function itself (`run_one_trial_*`) does NOT call `set_distal_*_multiplier` — that
stays in the outer sweep driver.

### run_sweep.py — copy into task (adapted from t0034)

**Source**: `tasks/t0034_distal_dendrite_length_sweep_t0024/code/run_sweep.py` (293 lines)

**What it does**: Outer sweep driver that calls `set_distal_length_multiplier` once per sweep point,
runs the inner (angles × trials) loop, writes the tidy CSV incrementally with `fh.flush()`, and
writes per-length/diameter canonical CSVs accepted by the t0012 scorer.

**Reuse method**: **copy into task** as `run_sweep.py`.

**Adaptation needed**: Rename the length-specific imports to diameter equivalents; change the AR2
rho guard to reference `AR2_RHO` from the t0035 constants; update path imports to the t0035
`paths.py`. Minimal structural changes.

### analyse_sweep.py and classify_slope.py — copy into task (from t0030)

**Source**: `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/analyse_sweep.py` (336 lines) and
`tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/classify_slope.py` (314 lines)

**What they do**: `analyse_sweep.py` reads the tidy CSV and computes per-diameter metrics
(`dsi_peak_null`, `dsi_vector_sum`, `peak_hz`, `null_hz`, `hwhm_deg`, `reliability`), writing
`results/data/metrics_per_diameter.csv`. `classify_slope.py` classifies the DSI-vs-diameter slope as
`schachter2010_amplification`, `passive_filtering`, or `flat` using a `log2(multiplier)` linear
regression with a saturation fallback.

**Reuse method**: **copy into task**. Update all imports of t0030 constants and paths to t0035
equivalents. No algorithmic changes required.

### constants.py and paths.py — copy into task (from t0030, extended with t0034 additions)

**Source**: `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/constants.py` (95 lines) and
`tasks/t0034_distal_dendrite_length_sweep_t0024/code/constants.py` (97 lines)

**What they do**: `constants.py` defines `DIAMETER_MULTIPLIERS`, `PREFLIGHT_DIAMETER_MULTIPLIERS`,
`N_TRIALS_T0024 = 10`, `AR2_RHO = 0.6`, `TIDY_CSV_HEADER`, `CURVE_CSV_HEADER`, mechanism
classification thresholds, and seed-stride constants. `paths.py` (50 lines in t0030; 54 lines in
t0034) centralises all file paths under `TASK_DIR`.

**Reuse method**: **copy into task** and merge: t0035's `constants.py` should derive from t0030's
structure plus the t0024-specific additions from t0034 (`N_TRIALS_T0024`, `AR2_RHO`,
`SEED_*_STRIDE`).

### tuning_curve_loss — import via library

**Source**: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/` (8 modules, ~500
lines total)

**What it does**: Provides `compute_dsi`, `compute_hwhm_deg`, `compute_reliability`,
`load_tuning_curve`, `score`, and `TuningCurveMetrics`. Used in `analyse_sweep.py` to compute per-
diameter DSI, HWHM, and reliability from the per-diameter canonical CSVs.

**Reuse method**: **import via library** (the only registered cross-task import). Import path:
`from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import compute_dsi`.

### plot_sweep.py and preflight_distal.py — copy into task (from t0034)

**Source**: `tasks/t0034_distal_dendrite_length_sweep_t0024/code/plot_sweep.py` (422 lines) and
`tasks/t0034_distal_dendrite_length_sweep_t0024/code/preflight_distal.py` (158 lines)

**What they do**: `plot_sweep.py` renders primary DSI-vs-diameter, vector-sum DSI, and polar overlay
charts using matplotlib. `preflight_distal.py` logs the distal section count, depth distribution,
and baseline diameter statistics to `logs/preflight/distal_sections.json`.

**Reuse method**: **copy into task**. Update path imports and rename `length` → `diameter` in
variable names and output paths.

## Lessons Learned

### t0022 Null Result Was Structural, Not Stochastic

The t0030 diameter sweep on t0022 [t0030] produced primary DSI pinned at exactly 1.000 across all 7
multipliers because t0022's deterministic per-dendrite E-I schedule produces zero null firing at
every angle in the null half-plane. This is not a sampling artefact — it is an architectural
property of the deterministic driver. Any sweep on t0022 that measures primary DSI is therefore
uninformative about biophysical mechanisms; only vector-sum DSI has any variation, and even that
variation was not statistically significant (p=0.18). Running a diameter sweep on t0024 instead is
the correct choice and was confirmed viable by t0034 [t0034].

### AR(2) Non-Zero Null Firing Enables Mechanism Discrimination

t0026 [t0026] showed that t0024's DSI has 1.9× modulation over V_rest, and t0034 [t0034] showed that
primary DSI varies 0.545-0.774 (range 0.229) over the length sweep, with null firing of 0.70-1.00 Hz
at every sweep point. This range is sufficient to detect a mechanistic slope. However, t0034 also
found a local-spike-failure transition at 1.5× and 2.0× length (preferred direction jumped from 0°
to 330° to 30°), suggesting that very large multipliers can destabilise the cell. The same failure
mode may occur at large diameter multipliers if distal impedance is raised too much by thinning; the
classify_slope fallback to vector-sum DSI protects against a false-flat result if primary DSI
becomes unreliable at the extremes.

### Per-Trial Build Cost and Crash Recovery

t0024 runs at ~12 s/trial vs t0022's ~3.8 s/trial [t0026]. For 840 trials the expected wall time is
~2.8 hours (consistent with t0034's ~3 h observed). The cell must be built only once per sweep (not
per trial or per diameter point) to amortise the ~1.6 s NEURON build cost; t0034 confirmed this
pattern is safe across all 7 length multipliers because `sec.L` changes are persistent state that
survive across `h.finitialize` calls. The same holds for `seg.diam`. The tidy CSV should be flushed
after every row to enable crash recovery; t0034's `run_sweep.py` demonstrated this pattern.

### Seed Uniqueness and Reproducibility

t0034 used a deterministic seed formula
`length_idx * SEED_LENGTH_STRIDE + SEED_ANGLE_STRIDE * angle_idx + trial_idx + 1` with
`SEED_LENGTH_STRIDE = 10_000_003` and `SEED_ANGLE_STRIDE = 1000`, and confirmed uniqueness via a
post-sweep `assert len(seed_set) == expected_trial_count`. This guard prevented silent seed
collisions. The same formula should be adopted in t0035 with `diameter_idx` replacing `length_idx`.

## Recommendations for This Task

1. **Copy `distal_selector_t0024.py` from t0034** verbatim (27 lines) and update the `DSGCCell`
   import path to the absolute t0024 path. This gives t0035 the correct
   `identify_distal_sections_t0024` function that wraps `cell.terminal_dends`.

2. **Copy and adapt `diameter_override_t0024.py` from t0030's `diameter_override.py`** (~85 lines
   after dropping the two t0022-specific functions). Retain `snapshot_distal_diameters`,
   `set_distal_diameter_multiplier`, and `assert_distal_diameters` unchanged. Import
   `DIAMETER_ASSERT_TOL_UM` from the t0035 constants module.

3. **Use t0034's `trial_runner_length_t0024.py` as the template for the trial runner** (180 lines).
   The only structural change is replacing `baseline_L: dict[int, float]` with
   `baseline_diam: dict[tuple[int, float], float]` in the context dataclass. The `_AR2_RHO`
   module-scope pin, the `FInitializeHandler` keep-alive pattern, and the
   `h.finitialize(C.V_INIT_MV)` → `h.run()` sequence carry over without change.

4. **Copy t0030's `analyse_sweep.py` and `classify_slope.py`** as the analysis pipeline. These
   implement exactly the slope-sign classification taxonomy (Schachter2010 / passive / flat) needed
   for the diameter-sweep science question. t0034's `classify_shape.py` (monotonic / saturating /
   non-monotonic) is the wrong classifier for this task.

5. **Preserve the AR(2) rho guard** from t0034's `run_sweep.py`:
   `assert C.AR2_CROSS_CORR_RHO_CORRELATED == AR2_RHO`. Pin `AR2_RHO = 0.6` in the t0035
   `constants.py`.

6. **Import `compute_dsi`, `compute_hwhm_deg`, and `compute_reliability` from the t0012 library**
   (the only valid cross-task import). Do not copy the t0012 scorer; import it.

7. **Plan for ~2.8 h wall time** (840 trials × ~12 s/trial). Use the preflight mode (3 multipliers ×
   3 angles × 2 trials = 18 trials, ~3.6 min) to validate the diameter override and AR(2) rho before
   committing to the full sweep. Thinner diameter multipliers (0.5×) will run slower due to raised
   axial resistance — the same pattern observed in t0030.

8. **Expect primary DSI range 0.2-0.4** across the sweep if the t0024 biophysics are consistent with
   t0034's length-sweep findings. If primary DSI range falls below
   `DSI_SATURATION_THRESHOLD = 0.02`, the fallback to vector-sum DSI will activate automatically in
   `classify_slope.py`.

## Task Index

### [t0012]

* **Task ID**: t0012_tuning_curve_scoring_loss_library
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Provides the canonical `tuning_curve_loss` DSI / HWHM / reliability scorer used in
  `analyse_sweep.py` to compute per-diameter metrics. The only registered cross-task library
  importable in this project.

### [t0024]

* **Task ID**: t0024_port_de_rosenroll_2026_dsgc
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Primary model under test. Provides `build_dsgc_cell() -> DSGCCell`, the
  `DSGCCell.terminal_dends` distal-leaf list, the AR(2) stochastic driver entry points
  (`run_single_trial`, helper functions), and the constant `AR2_CROSS_CORR_RHO_CORRELATED = 0.6`.

### [t0026]

* **Task ID**: t0026_vrest_sweep_tuning_curves_dsgc
* **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
* **Status**: completed
* **Relevance**: Established the t0024 operating baseline: ~12 s/trial wall time, DSI range
  0.36-0.67 at ρ=0.6, HWHM 65-83°, non-zero null firing (key property enabling mechanism
  discrimination). These numbers underpin the t0035 runtime estimate and expected DSI range.

### [t0030]

* **Task ID**: t0030_distal_dendrite_diameter_sweep_dsgc
* **Name**: Distal-dendrite diameter sweep on t0022 DSGC
* **Status**: completed
* **Relevance**: Provides the diameter-override code pattern (`diameter_override.py`), the slope-
  sign classification pipeline (`classify_slope.py`, `analyse_sweep.py`), and the null-result
  baseline (primary DSI pinned at 1.000, vector-sum DSI flat p=0.18). The t0022-specific
  `identify_distal_sections` function must not be reused; all other modules are adaptable.

### [t0034]

* **Task ID**: t0034_distal_dendrite_length_sweep_t0024
* **Name**: Distal-dendrite length sweep on t0024 DSGC
* **Status**: completed
* **Relevance**: The closest sibling task: same model (t0024), same trial budget (840), same AR(2)
  ρ=0.6, same 12-direction protocol. Confirmed that primary DSI varies measurably on t0024 (range
  0.545-0.774), validated the `distal_selector_t0024.py` + `trial_runner_length_t0024.py` pipeline,
  and produced the ~3 h wall-time reference. All code modules should be used as templates for t0035.
