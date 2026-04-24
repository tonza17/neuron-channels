---
spec_version: "1"
task_id: "t0041_electrotonic_length_collapse_t0034_t0035"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 9
libraries_found: 7
libraries_relevant: 3
date_completed: "2026-04-24"
status: "complete"
---
# Research Code: Electrotonic-Length Collapse of t0034 and t0035

## Task Objective

t0041 is a zero-simulation, post-hoc cable-theory analysis that recomputes electrotonic length
`L/lambda = L / sqrt(d * Rm / (4 * Ra))` per distal section for every (length-multiplier,
diameter-multiplier) operating point already simulated by the t0034 length sweep [t0034] and the
t0035 diameter sweep [t0035] on the t0024 de Rosenroll DSGC testbed [t0024]. The task then tests
whether primary DSI and vector-sum DSI from both sweeps collapse onto a single DSI-vs-L/lambda curve
(target Pearson r > 0.9), and reports residual variance attributable to non-cable effects. Output is
one answer asset, one overlay PNG, `results/metrics.json` with the Pearson r, residual RMSE, and a
collapse-confirmed / collapse-rejected verdict, plus a recommendation for the t0033 morphology /
channel optimiser [t0033]. No NEURON runs, no new trial CSVs.

## Library Landscape

The library aggregator script is not present in this repo snapshot (`arf/scripts/aggregators/`
contains costs, metrics, machines, suggestions, tasks, task-types, and categories aggregators but no
`aggregate_libraries.py`), so libraries were enumerated by direct inspection of
`tasks/*/assets/library/`. Seven library assets exist across completed tasks:

1. **`tuning_curve_viz`** (t0011; v0.1.0) — Matplotlib polar / Cartesian / overlay / raster-PSTH
   plotting. No correction overlay. Relevant to t0041: `plot_multi_model_overlay` and the Cartesian
   primitive are candidates for the DSI-vs-L/lambda overlay PNG. Import path:
   `tasks.t0011_response_visualization_library.code.tuning_curve_viz.{cartesian,overlay,polar}`.
2. **`tuning_curve_loss`** (t0012; v0.1.0) — Canonical 12-angle scorer: `load_tuning_curve`,
   `score_curves`, `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`,
   `compute_reliability`. Relevant: t0041 reuses t0034/t0035's already-computed per-multiplier DSI
   rather than re-scoring, but `load_tuning_curve` is useful if we need to re-derive DSI from the
   per-length / per-diameter CSVs as a cross-check. Import path:
   `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`.
3. **`de_rosenroll_2026_dsgc`** (t0024; v0.1.0) — The NEURON-based testbed library whose distal
   biophysics constants (`RA_OHM_CM = 100.0`, `CM_UF_CM2 = 1.0`, `GLEAK_S_CM2 = 0.0001667`,
   `ELEAK_MV = -60.0`) are the exact parameter backbone used by t0034 and t0035, so they define the
   Rm and Ra that enter the L/lambda formula for this analysis. Relevant.
4. **`modeldb_189347_dsgc_dendritic`** (t0022) — t0022 testbed library; used by t0029/t0030 but
   not by t0034/t0035 and therefore not relevant to t0041's collapse analysis.
5. **`modeldb_189347_dsgc`** (t0008 / t0020) — upstream Poleg-Polsky ports; not relevant.
6. **`hunt_missed_dsgc_models`** (t0010) — literature catalog library; not relevant.

None of the seven libraries has a corrections overlay in `corrections/` of any downstream task.
Three are directly relevant to t0041 (t0011, t0012, t0024), so `libraries_relevant = 3`. The
remaining four were inspected and ruled out as not applicable.

## Key Findings

### Trial CSV schema is stable across t0034 and t0035

Both sibling sweeps emit a tidy CSV `results/data/sweep_results.csv` with a 6-column schema. t0034
uses `(length_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)` and t0035
uses `(diameter_multiplier, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)` — only
the first column name differs [t0034, t0035]. Both also emit a per-multiplier reduction CSV
(`results/data/metrics_per_length.csv`, `results/data/metrics_per_diameter.csv`) with an identical
10-column schema:
`(length|diameter)_multiplier, peak_hz, null_hz, dsi_primary, dsi_vector_sum, hwhm_deg, reliability, preferred_direction_deg, preferred_hz, mean_peak_mv`.
This means t0041's loader can share a single parser with two swappable column names, and the
per-multiplier CSV is the canonical input for the collapse plot: both `dsi_primary` and
`dsi_vector_sum` are already computed and do not need to be re-derived from trial-level spike
counts. Column provenance is the same `_vector_sum_dsi` (Mazurek convention) and t0012 `compute_dsi`
(peak-minus-null) functions in both `analyse_sweep.py` files, which means the two sweeps' DSI
numbers are directly comparable on the same L/lambda axis without any normalisation.

### Biophysics values for the L/lambda calculation are hard-coded in t0024's library

The electrotonic length formula `lambda = sqrt(d * Rm / (4 * Ra))` requires per-section diameter `d`
(in cm), specific membrane resistance `Rm = 1/g_leak` (in ohm·cm^2), and axial resistance `Ra` (in
ohm·cm). All three values are pinned as named constants in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` [t0024]: `RA_OHM_CM = 100.0`,
`GLEAK_S_CM2 = 0.0001667` (so `Rm = 1 / 0.0001667 ≈ 5999 ohm·cm^2`), and a paper-text alternative
`RA_OHM_CM_PAPER_TEXT = 200.0` (not used by the t0034/t0035 simulations — confirmed by
`build_cell.py` lines 200, 225, 236, 247, which assign `dend.Ra = C.RA_OHM_CM` on every soma /
primary / non-terminal / terminal section). Because the simulations used the `100 ohm·cm` setting,
t0041 must use the same value; the paper-text 200 is out of scope for this collapse analysis. These
values are uniform across every terminal dendrite, so the "section-weighted average L/lambda"
fallback hedged in the task description (`tasks/.../task_description.md` line 58) is not actually
required — uniform Rm and Ra allow a per-section scalar L/lambda with only `sec.L` and `sec.diam`
varying.

### The distal sections and their baseline L, diam must come from a single NEURON boot

t0034 [t0034] uses `tasks/t0034_.../code/distal_selector_t0024.py::identify_distal_sections_t0024`
(returns `list(cell.terminal_dends)` — the HOC-leaf dendrites, 177 sections on this morphology).
t0035 [t0035] uses a structurally identical helper in its own `distal_selector_t0024.py`. Both
helpers depend on `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell.DSGCCell`, which is a
frozen dataclass exposing `terminal_dends: list[Any]`. Because of the cross-task-import rule, t0041
cannot import the t0034 / t0035 selectors directly — the library path is
`tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell.build_dsgc_cell()` via the t0024 library,
and the selector logic (`list(cell.terminal_dends)`) must be re-implemented inline inside t0041's
`code/`. A single NEURON boot of the t0024 cell at baseline multipliers (`length_multiplier = 1.0`
and `diameter_multiplier = 1.0`) is enough to snapshot `(sec.L, seg.diam)` for every terminal
section; the multiplier grid is then applied analytically in pure Python/NumPy without any further
NEURON invocation, consistent with the task's "zero simulation cost" requirement.

### Length and diameter multipliers are applied section-uniformly and reversibly

`length_override_t0024.snapshot_distal_lengths` [t0034] returns `{id(sec): float(sec.L)}`, and
`set_distal_length_multiplier(..., multiplier=m)` sets `sec.L = baseline_L[id(sec)] * m` uniformly
across every terminal section — i.e. every terminal dendrite is scaled by the same multiplier. The
diameter counterpart `diameter_override_t0024.snapshot_distal_diameters` [t0035] keys on
`(id(sec), seg.x)` but the behaviour is identical at `nseg=1` (every terminal section has one
segment on this morphology — confirmed by the in-file comment at line 31 of
`diameter_override_t0024.py`). The upshot: at operating point `(m_L, m_D)`, every distal section
shares the same `L/lambda_i = (m_L * L_baseline_i) / sqrt(m_D * d_baseline_i * Rm / (4 * Ra))`.
Whether t0041 reports a single average `L/lambda` or the full per-section distribution is a
presentation choice, not a modelling one — the cable-theory collapse test only needs one scalar
summary per operating point.

### Sweep grids are identical between t0034 and t0035

Both sweeps use the exact same 7-point multiplier grid `(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)` (see
`LENGTH_MULTIPLIERS` in t0034 constants.py line 11 and `DIAMETER_MULTIPLIERS` in t0035 constants.py
line 12), with the same 12-angle × 10-trial protocol (`N_TRIALS_T0024 = 10`, AR(2) `rho = 0.6`).
The shared `1.0x` baseline operating point is therefore a duplicate observation that t0041 can use
as a noise-floor sanity check — the two sweeps' DSI values at `(m_L=1.0, m_D=1.0)` must agree to
within AR(2) seed-reassignment variance, providing a direct estimate of the DSI noise floor that any
collapse claim must exceed.

### Downstream prior art for plotting and regression on sweep data

`plot_sweep.py` in both t0034 and t0035 already implements Matplotlib-on-Agg bar/line plots with the
Okabe-Ito palette (`COLOR_DSI = "#0072B2"`, `COLOR_PEAK = "#E69F00"`), multiplier-on-x-axis
conventions, 300 dpi output, and dual-axis `dsi_primary` + `peak_hz` overlays [t0034, t0035]. These
patterns can be copied to produce the t0041 overlay plot with minimal adaptation (swap multiplier
axis for L/lambda axis, plot two series with distinguishing markers). `classify_shape.py` (t0034,
line 1-50) and `classify_slope.py` (t0035) both use `scipy.stats.linregress` for the slope and
p-value of DSI vs multiplier; for the collapse analysis, the same `linregress` call combined with
`scipy.stats.pearsonr` (or equivalent) gives the collapse Pearson r and residual RMSE in a few
lines. This is the template the t0037 GABA-ladder analysis [t0037] also follows, so it is a stable
cross-task pattern.

## Reusable Code and Assets

**Critical note**: per the cross-task import rule, only code inside an `assets/library/` directory
can be imported across tasks. All non-library code must be copied.

1. **`tuning_curve_loss.load_tuning_curve`** — Source:
   `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/loader.py`. What: reads a
   `(angle_deg, trial_seed, firing_rate_hz)` CSV and returns a `TuningCurve` dataclass. Signature:
   `load_tuning_curve(*, csv_path: Path) -> TuningCurve`. Reuse method: **import via library**.
   Adaptation: none; t0034 / t0035 both produce per-multiplier canonical CSVs at
   `results/data/per_length/tuning_curve_Lxpyy.csv` and
   `results/data/per_diameter/tuning_curve_Dxpyy.csv` which this helper loads verbatim. Used only if
   t0041 wants to re-verify DSI from raw rates; otherwise skip. Line count: ~80 (import only).

2. **`tuning_curve_loss.compute_dsi` / `compute_peak_hz` / `compute_null_hz`** — Source:
   `tasks/t0012_.../code/tuning_curve_loss/metrics.py`. What: scalar metrics from a `TuningCurve`.
   Signature: `compute_dsi(*, curve: TuningCurve) -> float`. Reuse method: **import via library**.
   Adaptation: none. Line count: ~150 (import only).

3. **`de_rosenroll_2026_dsgc.build_cell.build_dsgc_cell`** — Source:
   `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py`. What: boots NEURON 8.2.7, sources
   `RGCmodelGD.hoc`, returns a `DSGCCell` frozen dataclass exposing `.terminal_dends`. Signature:
   `build_dsgc_cell() -> DSGCCell`. Reuse method: **import via library**. Adaptation: wrap in a
   one-shot helper that snapshots `(sec.L, seg.diam)` for every terminal section, then releases the
   NEURON handle. Line count: ~10 of new caller code.

4. **Biophysics constants `RA_OHM_CM`, `CM_UF_CM2`, `GLEAK_S_CM2`, `ELEAK_MV`** — Source:
   `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` lines 27-30. What: the pinned Rm and
   Ra values used by t0034 and t0035 simulations. Reuse method: **import via library** (importing
   `tasks.t0024_port_de_rosenroll_2026_dsgc.code.constants` works through the library module-path
   list). Adaptation: compute `RM_OHM_CM2 = 1.0 / GLEAK_S_CM2` in t0041's own `constants.py`.

5. **`analyse_sweep._vector_sum_dsi`** — Source:
   `tasks/t0034_distal_dendrite_length_sweep_t0024/code/analyse_sweep.py` lines 80-99 (also at the
   same location in t0035's `analyse_sweep.py`). What: returns Mazurek `(dsi, preferred_dir_deg)`
   from per-angle mean rates. Reuse method: **copy into task** (not in any library). Adaptation: a
   verbatim copy into `tasks/t0041_.../code/vector_sum.py`; ~20 lines.

6. **Trial-CSV loader pattern (`csv.DictReader` over tidy sweep CSV)** — Source:
   `tasks/t0034_.../code/analyse_sweep.py::compute_metrics_from_tidy` lines 165-188. What: a
   schema-aware `csv.DictReader` loop that groups `(multiplier -> angle -> list[rate])` and
   `(multiplier -> list[peak_mv])`. Reuse method: **copy into task**. Adaptation: generalise column
   name from `length_multiplier` / `diameter_multiplier` to a caller-supplied constant; ~30 lines
   each pass.

7. **Per-multiplier metrics reader** — Source: `plot_sweep._read_metrics_csv` in both
   `tasks/t0034_.../code/plot_sweep.py` lines 68-88 and `tasks/t0035_.../code/plot_sweep.py`. What:
   reads `metrics_per_{length,diameter}.csv` into a `list[MetricsRow]` frozen dataclass. Reuse
   method: **copy into task**. Adaptation: rename the multiplier column constant; ~30 lines.

8. **Plot template (Cartesian DSI vs scalar x, Okabe-Ito palette, 300 dpi)** — Source:
   `tasks/t0034_.../code/plot_sweep.py` lines 1-120. What: Matplotlib-Agg Cartesian figure with
   named colour constants, optional regression overlay, baseline star marker, figure-size / dpi
   constants. Reuse method: **copy into task**. Adaptation: replace the multiplier x-axis with
   L/lambda, add two series with distinct markers (square for length sweep, circle for diameter
   sweep); ~120 lines.

9. **Linear regression + collapse test pattern** — Source:
   `tasks/t0034_.../code/classify_shape.py` lines 1-50 (uses `scipy.stats.linregress`). What: slope,
   intercept, r-value, p-value, stderr from `(x, y)` arrays. Reuse method: **copy into task**.
   Adaptation: combine with `numpy.polyfit` residuals or `scipy.stats.pearsonr` for the unified-
   curve Pearson r; ~25 lines.

10. **`paths.py` / `constants.py` / frozen-dataclass scaffold** — Source: every recent task's code
    folder (e.g. `tasks/t0034_.../code/paths.py`). What: centralised `Path` constants, named CSV
    column constants, frozen dataclasses. Reuse method: **copy into task** as the standard per-task
    skeleton. Adaptation: adjust `TASK_ROOT` anchor and asset IDs; ~60 lines total.

## Lessons Learned

The t0034 negative slope (`-0.126 per unit multiplier`, `p = 0.038`) and t0035 flat slope (`+0.004`,
`p = 0.88`) [t0034, t0035] are the central empirical fact this task builds on, and both tasks
explicitly flag the ~30x asymmetry as evidence that raw length and raw diameter are not equally
effective DSI controls. The vector-sum DSI channel in t0034 shows a cleaner monotonic decline (R^2 =
0.91) than primary DSI, suggesting that vector-sum DSI is the better channel on which to claim
collapse if primary DSI is noisier. A pitfall to avoid, flagged in t0029 and carried over to t0034,
is that the prior t0022 testbed pinned null firing at 0 Hz which made primary DSI saturate at 1.0
for many multipliers — the t0024 testbed [t0024] fixed this via AR(2) noise-driven null firing
(0.5-1.0 Hz), which is why this task uses t0024's sweep outputs exclusively and not t0029's /
t0030's. Finally, the t0034 classifier labelled the overall DSI-vs-length curve as `non_monotonic`
with superimposed spike-failure transitions at 1.5x and 2.0x; the collapse plot must therefore
accommodate the possibility that at extreme L/lambda values the curve bends due to active-spike
failure rather than pure cable filtering, and should flag those operating points rather than fit a
single line through them.

## Recommendations for This Task

1. **Import the three relevant libraries directly**: add
   `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` for optional DSI
   re-verification, `tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian` for
   the collapse overlay, and `tasks.t0024_port_de_rosenroll_2026_dsgc.code.{build_cell, constants}`
   for the NEURON snapshot and `Rm, Ra` constants.
2. **Copy (not import) the distal-section selector, sweep-CSV parser, metrics-CSV reader, Mazurek
   vector-sum helper, and linregress-classifier scaffolding** from t0034 and t0035 into
   `tasks/t0041_.../code/`. These are not in `assets/library/` so the cross-task import rule forbids
   importing them directly; structurally identical copies in t0041's `code/` are the
   project-standard answer.
3. **Do not re-score DSI from trial CSVs**; consume `results/data/metrics_per_length.csv` and
   `results/data/metrics_per_diameter.csv` directly. Both files already carry `dsi_primary` and
   `dsi_vector_sum` computed by the same scoring functions, so re-scoring cannot yield different
   values within this testbed and would waste I/O.
4. **Use the 1.0x baseline as a noise-floor anchor**: report the delta between t0034's
   `length_multiplier = 1.0` and t0035's `diameter_multiplier = 1.0` DSI values as the AR(2)
   seed-reassignment noise floor. Any collapse curve residual below this floor is indistinguishable
   from identical data.
5. **Compute a single scalar L/lambda per operating point** (section-mean, since Rm, Ra are
   uniform); additionally report the per-section L/lambda distribution as a diagnostic overlay.
6. **Report both primary and vector-sum DSI collapse curves**. Given t0034's observation that
   vector-sum DSI has a cleaner monotonic signal, vector-sum DSI is a priori the more likely channel
   to show a clean collapse; primary DSI is the task-spec primary and must still be reported.
7. **Flag spike-failure operating points** (t0034's 1.5x and 2.0x length multipliers, noted in
   `classify_shape.py` output) on the collapse plot with distinct markers and exclude them from the
   Pearson r fit, or report the fit both with and without them.
8. **Write the answer asset per the paper / answer spec** (`meta/asset_types/answer/`), summarising
   the Pearson r, residual RMSE, collapse verdict, and the t0033-parameterisation recommendation.

## Task Index

### [t0011]

* **Task ID**: t0011_response_visualization_library
* **Name**: Response Visualization Library
* **Status**: completed
* **Relevance**: Provides the `tuning_curve_viz` library with polar, Cartesian, and
  multi-model-overlay plotters — the direct template for t0041's DSI-vs-L/lambda overlay figure.

### [t0012]

* **Task ID**: t0012_tuning_curve_scoring_loss_library
* **Name**: Tuning Curve Scoring / Loss Library
* **Status**: completed
* **Relevance**: Provides `load_tuning_curve`, `compute_dsi`, `compute_peak_hz`, `compute_null_hz`,
  `compute_hwhm_deg`, `compute_reliability` — the canonical tuning-curve metric library used by
  t0034 and t0035 (and therefore what any DSI re-verification in t0041 must use).

### [t0015]

* **Task ID**: t0015_literature_survey_cable_theory
* **Name**: Literature Survey: Cable Theory and DSGC Modelling
* **Status**: completed
* **Relevance**: The `cable-theory-implications-for-dsgc-modelling` answer asset documents the
  electrotonic-length framework and the 0.5-0.8 L/lambda target range, which is the theoretical
  backbone of t0041's collapse claim.

### [t0024]

* **Task ID**: t0024_port_de_rosenroll_2026_dsgc
* **Name**: Port of de Rosenroll et al. 2026 DSGC model
* **Status**: completed
* **Relevance**: The underlying testbed. Its library
  (`de_rosenroll_2026_dsgc.{build_cell, constants}`) supplies the NEURON cell, the terminal-dendrite
  enumeration, and the biophysics constants (`RA_OHM_CM = 100.0`, `GLEAK_S_CM2 = 0.0001667`,
  `CM_UF_CM2 = 1.0`, `ELEAK_MV = -60.0`) that t0041 needs to compute L/lambda.

### [t0029]

* **Task ID**: t0029_distal_dendrite_length_sweep_dsgc
* **Name**: Distal-dendrite length sweep on t0022 DSGC
* **Status**: completed
* **Relevance**: t0034's structural predecessor on the t0022 testbed; null result (DSI pinned at 1.0
  because null firing was 0 Hz) is the lesson that motivated the t0024-based re-run and is why t0041
  uses t0034/t0035 outputs and not t0029/t0030.

### [t0033]

* **Task ID**: t0033_plan_dsgc_morphology_channel_optimisation
* **Name**: Plan: DSGC morphology + channel optimisation
* **Status**: completed (planning task)
* **Relevance**: Downstream consumer. If t0041 confirms collapse, t0033 can parameterise dendritic
  morphology in 1-D (L/lambda) instead of 2-D (raw L x raw d), shrinking its search space.

### [t0034]

* **Task ID**: t0034_distal_dendrite_length_sweep_t0024
* **Name**: Distal-dendrite length sweep on t0024 DSGC
* **Status**: completed
* **Relevance**: Primary input. t0041 consumes `results/data/sweep_results.csv` and
  `results/data/metrics_per_length.csv`; copies the vector-sum DSI helper, the per-length metrics
  reader, the plot template, and the linregress classifier scaffolding from its `code/`.

### [t0035]

* **Task ID**: t0035_distal_dendrite_diameter_sweep_t0024
* **Name**: Distal-dendrite diameter sweep on t0024 DSGC
* **Status**: completed
* **Relevance**: Primary input. t0041 consumes `results/data/sweep_results.csv` and
  `results/data/metrics_per_diameter.csv`; shares CSV schema with t0034 modulo one column name.

### [t0037]

* **Task ID**: t0037_null_gaba_reduction_ladder_t0022
* **Name**: Null-direction GABA reduction ladder on t0022
* **Status**: completed
* **Relevance**: Demonstrates the shared slope / classifier / linregress / plot-template pattern
  that t0034, t0035, and t0041 all follow; confirms the pattern is stable and copy-worthy.
