---
spec_version: "2"
task_id: "t0041_electrotonic_length_collapse_t0034_t0035"
date_completed: "2026-04-24"
status: "complete"
---
# Results Detailed: t0041 Electrotonic-Length Collapse Analysis

## Summary

Tested whether primary DSI and vector-sum DSI from t0034 (distal-length sweep) and t0035
(distal-diameter sweep) collapse onto a single DSI-vs-L/lambda curve under Rall's cable theory.
Computed lambda = sqrt(d * Rm / (4 * Ra)) per operating point using t0024 baseline biophysics,
overlaid both sweeps, and tested for Pearson r > 0.9 on the 3-point paired overlap region (L/lambda
in [0.058, 0.116]). **Verdict: collapse_rejected** (primary r = +0.42; vector-sum r = -0.68, sign
inverted). Recommendation for t0033: retain the 2-D morphology parameterisation.

## Methodology

* **Machine**: local Windows 11 workstation (no remote compute).
* **Runtime**: approximately 2 minutes total across CSV read, L/lambda computation, interpolation,
  Pearson r, polynomial fit, and plotting.
* **Timestamps**: started 2026-04-24T11:53:11Z; completed 2026-04-24T12:08:20Z.
* **Inputs**: `tasks/t0034_distal_dendrite_length_sweep_t0024/results/metrics_per_length.csv` and
  `tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/metrics_per_diameter.csv` (7 rows each).
  Baseline biophysics from t0024 library asset: RA_OHM_CM = 100.0, Rm = 5999 ohm.cm^2,
  BASELINE_DISTAL_LENGTH_UM = 22.63 (mean over 177 terminal dendrites from the SWC morphology),
  BASELINE_DISTAL_DIAM_UM = 0.5033.
* **Formula**: lambda_cm = sqrt(effective_d_cm * RM_OHM_CM2 / (4.0 * RA_OHM_CM)); L/lambda =
  effective_L_cm / lambda_cm. Unit conversions from um to cm are explicit.
* **Collapse test**: (a) compute L/lambda for all 14 operating points; (b) interpolate t0035 DSI
  values onto t0034's L/lambda grid via linear interpolation; (c) compute Pearson r between t0034
  and interpolated t0035 for the n=3 paired points in the overlap region; (d) fit pooled degree-2
  polynomial and report residual RMSE per sweep.

### Master Collapse Plots

![Primary DSI vs L/lambda](images/primary_dsi_vs_L_over_lambda.png)

Primary DSI (peak-direction vs null-direction) plotted against L/lambda for both sweeps. t0034
length-sweep points span 0.041-0.165; t0035 diameter-sweep points span 0.058-0.116. The overlap
region contains only 3 paired points. Primary DSI responses diverge noticeably at matched L/lambda,
confirming that L/lambda is not a sufficient univariate parameter for this metric on the t0024
substrate. t0034's 1.5x and 2.0x multipliers (spike-failure regime) are flagged with hollow markers.

![Vector-sum DSI vs L/lambda](images/vector_sum_dsi_vs_L_over_lambda.png)

Vector-sum DSI plotted against L/lambda. The length sweep trends downward with L/lambda while the
diameter sweep trends slightly upward, producing the negative Pearson r = -0.68 on the overlap
region.

![Peak Hz vs L/lambda](images/peak_hz_vs_L_over_lambda.png)

Peak firing rate vs L/lambda, included for context. Peak rate varies between 3.4 and 5.7 Hz across
all operating points, consistent with t0024's lineage-wide peak-rate gap vs published DSGC
recordings.

## Metrics

| Quantity | Value |
| --- | --- |
| Pearson r primary DSI (n=3 paired) | +0.4161 (p=0.727) |
| Pearson r vector-sum DSI (n=3 paired) | -0.6787 (p=0.525) |
| Pooled poly-fit RMSE primary | 0.0397 |
| Pooled poly-fit RMSE vector-sum | 0.0237 |
| L/lambda overlap interval | [0.058, 0.116] |
| Baseline L/lambda (t0024) | 0.082 |
| Baseline lambda (um) | 274.8 |
| Verdict overall | collapse_rejected |

Full variant breakdown lives in `results/metrics.json` (14 variants); the paired L/lambda table is
in `results/electrotonic_length_table.csv`.

## Examples

Ten concrete operating points from the combined t0034 U t0035 dataset. Each example shows the raw
input row from the source metrics CSV and the computed L/lambda + verdict contribution.

### Example 1 — t0034 length x 0.5

Input (from `metrics_per_length.csv`):

```text
length_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
0.50,0.753846,0.506670,5.7000,0.8000
```

Computed output (from `electrotonic_length_table.csv`):

```text
sweep=length, effective_L=11.31 um, effective_d=0.503 um, lambda=274.8 um,
L_over_lambda=0.0412, spike_failure_flag=0
```

### Example 2 — t0034 length x 0.75

Input:

```text
length_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
0.75,0.774194,0.455440,5.5000,0.7000
```

Computed output:

```text
sweep=length, effective_L=16.97 um, lambda=274.8 um, L_over_lambda=0.0618
```

### Example 3 — t0034 length x 1.0 (baseline)

Input:

```text
length_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
1.00,0.770492,0.449145,5.4000,0.7000
```

Computed output:

```text
sweep=length, effective_L=22.63 um, lambda=274.8 um, L_over_lambda=0.0823
```

### Example 4 — t0034 length x 1.5 (spike-failure regime)

Input:

```text
length_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
1.50,0.622642,0.417301,4.3000,1.0000
```

Computed output:

```text
sweep=length, effective_L=33.94 um, L_over_lambda=0.1235, spike_failure_flag=1
```

### Example 5 — t0034 length x 2.0 (spike-failure regime)

Input:

```text
length_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
2.00,0.545455,0.357491,3.4000,1.0000
```

Computed output:

```text
sweep=length, effective_L=45.25 um, L_over_lambda=0.1647, spike_failure_flag=1
```

### Example 6 — t0035 diameter x 0.5

Input (from `metrics_per_diameter.csv`):

```text
diameter_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
0.50,0.703704,0.462807,4.6000,0.8000
```

Computed output:

```text
sweep=diameter, effective_d=0.252 um, lambda=194.3 um, L_over_lambda=0.1164
```

### Example 7 — t0035 diameter x 1.0 (baseline, same as length x 1.0 by construction)

Input:

```text
diameter_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
1.00,0.770492,0.449145,5.4000,0.7000
```

Computed output:

```text
sweep=diameter, effective_d=0.503 um, lambda=274.8 um, L_over_lambda=0.0823
```

### Example 8 — t0035 diameter x 1.5

Input:

```text
diameter_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
1.50,0.807692,0.418477,4.7000,0.5000
```

Computed output:

```text
sweep=diameter, effective_d=0.755 um, lambda=336.5 um, L_over_lambda=0.0672
```

### Example 9 — t0035 diameter x 2.0

Input:

```text
diameter_multiplier,dsi_primary,dsi_vector_sum,peak_hz,null_hz
2.00,0.680000,0.417209,4.2000,0.8000
```

Computed output:

```text
sweep=diameter, effective_d=1.007 um, lambda=388.6 um, L_over_lambda=0.0582
```

### Example 10 — Overlap-region comparison at L/lambda approx 0.082

Pairing (after interpolation of t0035 onto t0034's L/lambda grid):

```text
L_over_lambda=0.0823
t0034 length x 1.0   : primary_dsi=0.770 vector_sum_dsi=0.449
t0035 interpolated   : primary_dsi=0.770 vector_sum_dsi=0.449
```

At the exact baseline the two sweeps coincide by construction (both use 1.0x length and 1.0x
diameter). Diverging behaviour shows up only when one axis is varied, which is exactly why the
off-baseline overlap points disagree and the Pearson r is low.

## Analysis

The sign-inverted vector-sum Pearson r is the most striking finding. Under strict cable theory,
primary DSI and vector-sum DSI should both be monotonic in L/lambda through the passive-filtering
regime, with the same sign. The observation that the two metrics disagree on direction at matched
L/lambda indicates that additional non-cable mechanisms modulate each metric differently. The
leading candidate is AR(2) stochastic release in t0024: diameter changes modify the synaptic surface
area (and thus the number of release events contributing to the postsynaptic depolarisation
envelope), while length changes primarily modify the electrotonic attenuation of those events. The
two pathways are not commensurable under a single L/lambda scalar.

Contradicted plan assumption: the plan acknowledged an alternative with impedance-loading
corrections would be more accurate but started with the simple formula as the simplest falsifiable
hypothesis. The simple formula was falsified as expected; the impedance-loading variant is a natural
follow-up and is surfaced in `results/suggestions.json`.

## Limitations

* **Sample size in overlap region**: only 3 paired points after interpolation (L/lambda in
  [0.058, 0.116]). Pearson r on n=3 points has very low statistical power; both primary (p=0.73) and
  vector-sum (p=0.53) fail to reach significance. The directional conclusion (sign of r) is more
  reliable than its magnitude.
* **Baseline L estimate**: used the mean across 177 terminal dendrites (22.63 um). The actual t0024
  SWC has heterogeneous terminal-dendrite lengths; a per-section L/lambda would be more precise but
  requires morphology-aware refactoring that is outside this task's scope.
* **Single-parameter cable-theory model**: ignores sealed-end vs open-end boundary conditions,
  tapering, and active conductances. These are known to matter for realistic DSGCs and the
  impedance-loading-corrected alternative is queued as a follow-up suggestion.

## Files Created

* `code/paths.py`, `code/constants.py`, `code/vector_sum.py`, `code/metrics_csv_reader.py`,
  `code/compute_electrotonic_length.py`, `code/plot_collapse.py`, `code/test_collapse.py`
* `results/electrotonic_length_table.csv` (14 rows, paired L/lambda table)
* `results/collapse_stats.json` (Pearson r, polynomial coefficients, RMSE, verdicts)
* `results/metrics.json` (14-variant DSI breakdown)
* `results/images/primary_dsi_vs_L_over_lambda.png`
* `results/images/vector_sum_dsi_vs_L_over_lambda.png`
* `results/images/peak_hz_vs_L_over_lambda.png`
* `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/` — `details.json`,
  `short_answer.md`, `full_answer.md`

## Verification

* `verify_research_code.py` — PASSED (0 errors, 0 warnings).
* `verify_plan.py` — PASSED (0 errors, 2 cosmetic warnings).
* `verify_task_folder.py` — PASSED (1 warning: empty `logs/searches/`; acceptable for a task that
  did no internet research).
* `verify_task_metrics.py` — PASSED.
* `ruff check --fix .` and `ruff format .` — clean.
* `mypy -p tasks.t0041_electrotonic_length_collapse_t0034_t0035.code` — no issues across 256
  source files.

## Task Requirement Coverage

Operative task text (quoted from `task.json` and `task_description.md`):

> **short_description**: Zero-cost post-hoc analysis: compute electrotonic length L/lambda for t0034
> length sweep and t0035 diameter sweep and test for cable-theory collapse onto a single
> DSI-vs-L/lambda curve.
>
> **Objective (from task_description.md)**: For every (length multiplier, diameter multiplier)
> operating point in the combined t0034 U t0035 dataset, compute the electrotonic length L/lambda of
> the swept distal section using the t0024 baseline biophysics. Plot primary DSI and vector-sum DSI
> vs L/lambda for both sweeps on the same axes. Test whether the two sweeps collapse onto one curve
> with Pearson r > 0.9, and report the residual variance attributable to non-cable effects.

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Compute L/lambda per operating point | Done | `results/electrotonic_length_table.csv` (14 rows) |
| REQ-2 | Overlay primary DSI and vector-sum DSI vs L/lambda | Done | `results/images/primary_dsi_vs_L_over_lambda.png` and `results/images/vector_sum_dsi_vs_L_over_lambda.png` |
| REQ-3 | Report Pearson r and collapse verdict | Done | `collapse_rejected` (primary r=+0.42, vector-sum r=-0.68) in `results/collapse_stats.json` and `results_summary.md` |
| REQ-4 | Report residual variance of pooled fit | Done | Pooled RMSE 0.040 (primary) and 0.024 (vector-sum) in `results/collapse_stats.json` |
| REQ-5 | Produce one answer asset | Done | `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/` with `details.json`, `short_answer.md`, `full_answer.md` |
| REQ-6 | One-paragraph recommendation for t0033 parameterisation | Done | Recommendation in answer asset's `full_answer.md` and in this file's `## Analysis`: retain 2-D morphology parameterisation |
