---
spec_version: "2"
task_id: "t0041_electrotonic_length_collapse_t0034_t0035"
date_completed: "2026-04-24"
status: "complete"
---
# Plan: Electrotonic-Length Collapse Analysis of t0034 and t0035

## Objective

Test whether primary DSI and vector-sum DSI from the t0034 distal-length sweep and the t0035
distal-diameter sweep collapse onto a single DSI-vs-L/lambda curve under Rall's cable theory. Done
when: (a) L/lambda is computed per operating point using t0024 baseline biophysics, (b) both sweeps
are overlaid on a shared L/lambda axis, (c) a Pearson-r-based collapse test is reported with a clear
collapse_confirmed / collapse_rejected verdict, and (d) one answer asset documents the outcome and
its implication for parameterising t0033.

## Task Requirement Checklist

The task request (quoted verbatim from `task_description.md`):

> For every (length multiplier, diameter multiplier) operating point in the combined t0034 U t0035
> dataset, compute the electrotonic length L/lambda of the swept distal section using the t0024
> baseline biophysics (Rm, Ra from the Poleg-Polsky-2016 parameter backbone). Plot primary DSI and
> vector-sum DSI vs L/lambda for both sweeps on the same axes. Test whether the two sweeps collapse
> onto one curve with Pearson r > 0.9, and report the residual variance attributable to non-cable
> effects.

Checklist:

* **REQ-1**: Compute L/lambda per operating point for t0034's 7 length multipliers and t0035's 7
  diameter multipliers using t0024 distal-section Rm and Ra. Output: a per-multiplier table with
  `multiplier`, `effective_L`, `effective_d`, `lambda`, `L_over_lambda`. Evidence: CSV under
  `results/` and rendered in `results_detailed.md`. Satisfied by Step 4.

* **REQ-2**: Overlay primary DSI vs L/lambda and vector-sum DSI vs L/lambda for both sweeps on the
  same axes. Output: two PNG figures under `results/images/`. Evidence: PNG files embedded in
  `results_detailed.md`. Satisfied by Step 5.

* **REQ-3**: Report the Pearson r between t0034 and t0035 on the shared L/lambda axis for both DSI
  metrics, with a clear verdict: collapse_confirmed (r > 0.9) or collapse_rejected (r <= 0.9).
  Evidence: numerical output in `results/metrics.json` and narrative in `results_detailed.md`.
  Satisfied by Step 6.

* **REQ-4**: Report the residual variance after fitting a single L/lambda-parameterised curve.
  Evidence: residual RMSE in `results/metrics.json`. Satisfied by Step 6.

* **REQ-5**: One answer asset at
  `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/` with `details.json`,
  `short_answer.md`, `full_answer.md`. Satisfied by Step 7.

* **REQ-6**: A one-paragraph recommendation for t0033's morphology parameterisation (1-D L/lambda vs
  2-D raw length x diameter) in the answer asset's `full_answer.md`. Satisfied by Step 7.

## Approach

Post-hoc numerical analysis on the existing t0034 and t0035 per-multiplier metrics CSVs. The distal
section in t0024 is uniform (RA_OHM_CM=100, GLEAK_S_CM2=0.0001667 giving Rm approx 5999 ohm.cm^2,
per t0024's `constants.py` as documented in `research/research_code.md`), so lambda = sqrt(d * Rm /
(4 * Ra)) can be computed directly from each (length, diameter) operating point. L = section length.
L/lambda = L divided by lambda. The two sweeps each vary one axis while holding the other at 1.0x
baseline, so the combined dataset spans a 1-D slice through the (L, d) plane along each axis.

Alternative considered: an impedance-loading-corrected electrotonic length that accounts for
sealed-end vs open-end boundary conditions of the distal branch. Rejected for this first pass
because the baseline cable-theory prediction is the simplest falsifiable hypothesis; if the r > 0.9
threshold fails with the simple formula, a follow-up suggestion will propose the corrected analysis.

Task types: `data-analysis` (primary — post-hoc numerical analysis on existing outputs),
`answer-question` (secondary — the deliverable is one answer asset). Both are declared in
`task.json`.

## Cost Estimation

Zero dollar cost. All inputs are existing project artifacts (t0034 and t0035 CSVs, t0024 constants).
No paid API calls, no remote compute. Total project budget remains $0.00 of $1.00 used.

## Step by Step

1. **Copy helpers** into `code/`: `distal_selector.py` (copied from t0034's
   `code/distal_selector.py`), `mazurek_vector_sum.py` (copied from t0034 or t0035 `code/`),
   `tidy_csv_parser.py` (copied from t0034's `code/`), `metrics_csv_reader.py` (copied from t0034's
   `code/`). Label each copy with a comment indicating its source task.

2. **Centralize paths** in `code/paths.py`: constants for `T0034_METRICS_CSV`, `T0035_METRICS_CSV`,
   output CSV path, output image paths, answer asset directory.

3. **Centralize constants** in `code/constants.py`: `RA_OHM_CM = 100.0`,
   `GLEAK_S_CM2 = 0.000166667`, `RM_OHM_CM2 = 1.0 / GLEAK_S_CM2`,
   `BASELINE_DISTAL_LENGTH_UM = 50.0`, `BASELINE_DISTAL_DIAM_UM = 0.5` (fill these from t0024's
   `constants.py` — confirm at the start of implementation).

4. **Compute L/lambda** in `code/compute_electrotonic_length.py`:
   * Read `T0034_METRICS_CSV` and `T0035_METRICS_CSV` into DataFrames.
   * For each row: `effective_L = BASELINE_DISTAL_LENGTH_UM * length_multiplier` (t0034) or
     `BASELINE_DISTAL_LENGTH_UM` (t0035).
   * For each row: `effective_d = BASELINE_DISTAL_DIAM_UM * diameter_multiplier` (t0035) or
     `BASELINE_DISTAL_DIAM_UM` (t0034).
   * `lambda_cm = sqrt(effective_d_cm * RM_OHM_CM2 / (4.0 * RA_OHM_CM))` with unit conversions (um
     to cm).
   * `L_over_lambda = effective_L_cm / lambda_cm`.
   * Write `results/electrotonic_length_table.csv` with columns: `sweep` (length or diameter),
     `multiplier`, `effective_L_um`, `effective_d_um`, `lambda_um`, `L_over_lambda`, `primary_dsi`,
     `vector_sum_dsi`, `peak_hz`, `null_hz`.

5. **Make overlay plots** in `code/plot_collapse.py`:
   * Plot 1: `results/images/primary_dsi_vs_L_over_lambda.png` — overlay t0034 and t0035 points on
     the same axis, color-coded by sweep. Error bars from per-trial bootstrapping if available in
     the source CSVs; else point markers only.
   * Plot 2: `results/images/vector_sum_dsi_vs_L_over_lambda.png` — same layout.
   * Plot 3: `results/images/peak_hz_vs_L_over_lambda.png` — optional, for context.
   * Flag t0034's 1.5x and 2.0x multipliers as spike-failure regime (per t0034 results_summary) with
     a distinct marker or hollow symbol.

6. **Test collapse** in `code/test_collapse.py`:
   * Interpolate t0035 primary_dsi and vector_sum_dsi onto the set of L/lambda values the t0034
     sweep visits, using linear interpolation.
   * Compute Pearson r between t0034 values and the interpolated t0035 values for both metrics.
     Verdict: `collapse_confirmed` if r > 0.9 for primary_dsi AND vector_sum_dsi;
     `collapse_rejected` otherwise.
   * Fit a single 1-D L/lambda parameterised curve (polynomial degree 2) to the combined dataset and
     report RMSE vs each sweep.
   * Write verdict and numbers into `results/metrics.json` (plus the residual RMSE and Pearson r
     under project-registered metric keys if any apply; else under task-specific keys that will be
     documented in the results).

7. **Produce the answer asset** in
   `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/`:
   * `details.json` per the answer spec, with `confidence` and `categories` set.
   * `short_answer.md` — 2-5 sentence synthesis.
   * `full_answer.md` — sections per the answer spec, including a one-paragraph recommendation for
     t0033's morphology parameterisation (REQ-6).

## Remote Machines

None. Local CPU only.

## Assets Needed

* `tasks/t0034_distal_dendrite_length_sweep_t0024/results/metrics_per_length.csv` (primary input)
* `tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/metrics_per_diameter.csv` (primary
  input)
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/src/.../constants.py`
  (for confirming RA_OHM_CM, GLEAK_S_CM2, baseline L and d)
* `tasks/t0034_distal_dendrite_length_sweep_t0024/code/distal_selector.py` and related helpers (for
  copy)

## Expected Assets

* One answer asset: `electrotonic-length-collapse-of-length-and-diameter-sweeps`. Matches
  `expected_assets` `{"answer": 1}` in `task.json`.

## Time Estimation

~1 hour of wall-clock time including helper copy (10 min), paths and constants (5 min), L/lambda
computation (10 min), plots (15 min), collapse test (10 min), and answer asset (15 min).

## Risks & Fallbacks

* **t0024 distal biophysics are non-uniform or vary across sections**: then `lambda` is not
  well-defined by a single scalar; compute a section-weighted average and document the
  approximation. Likelihood: low (research_code.md confirmed uniform biophysics).

* **t0034's 1.5x and 2.0x spike-failure points contaminate the collapse test**: flag them as a
  separate regime and report Pearson r both with and without those points.

* **Pearson r is borderline (0.7-0.9)**: report r explicitly and emit a follow-up suggestion for a
  denser sweep or impedance-loading-corrected lambda.

* **Baseline distal length or diameter are not documented in t0024's constants**: read the SWC
  morphology file directly and compute the mean distal-section length and diameter.

## Verification Criteria

* `verify_plan.py` passes with zero errors for this file.
* `verify_research_code.py` passes (already done in step 6).
* `verify_task_results.py`, `verify_task_metrics.py`, `verify_answer_asset.py`,
  `verify_task_folder.py`, `verify_logs.py`, `verify_task_dependencies.py`, and
  `verify_pr_premerge.py` all pass with zero errors at the reporting step.
* All 6 REQ items above are marked Done with a pointer in `results/results_detailed.md`
  `## Task Requirement Coverage`.
