---
spec_version: "3"
task_id: "t0041_electrotonic_length_collapse_t0034_t0035"
step_number: 8
step_name: "implementation"
status: "completed"
started_at: "2026-04-24T11:53:11Z"
completed_at: "2026-04-24T12:05:51Z"
---
## Summary

Computed per-operating-point electrotonic length L/lambda for the combined t0034 length sweep and
t0035 diameter sweep, overlaid primary and vector-sum DSI on the shared L/lambda axis, and tested
the cable-theory collapse. **Verdict: collapse_rejected** for both metrics (primary r = +0.42,
vector-sum r = -0.68 over n=3 paired points in the L/lambda overlap 0.058-0.116; both well below the
0.9 confirmation threshold, and the vector-sum sign is inverted). Recommendation for t0033 is to
retain the 2-D (raw length x raw diameter) morphology parameterisation.

## Actions Taken

1. Read plan and research outputs; extracted baseline per-section distal L (mean 22.63 um over 177
   distal sections, from t0034 preflight `distal_sections.json`) and d (mean 0.5035 um, from t0035
   preflight) since the plan's placeholders (50.0 um, 0.5 um) did not match the real t0024
   morphology.
2. Created `code/paths.py` (all input/output path constants) and `code/constants.py` (passive cable
   constants copied from t0024, baseline L/d, sweep grid, CSV headers, collapse thresholds).
3. Copied the Mazurek vector-sum helper from t0034 into `code/vector_sum.py` and adapted the
   per-multiplier metrics-CSV reader from t0034's `plot_sweep.py` into `code/metrics_csv_reader.py`,
   each file prefixed with a `# Copied from ...` comment per the cross-task rule.
4. Implemented `code/compute_electrotonic_length.py` — reads upstream metrics CSVs, computes
   `lambda = sqrt(d * Rm / (4 * Ra))` with explicit um->cm conversion, writes 14-row
   `results/electrotonic_length_table.csv`.
5. Implemented `code/plot_collapse.py` — three 300 dpi PNGs (primary DSI, vector-sum DSI, peak Hz)
   with distinct colour+marker per sweep and hollow markers on t0034's 1.5x/2.0x spike-failure
   points.
6. Implemented `code/test_collapse.py` — interpolates t0035 onto t0034 L/lambda grid via
   `np.interp`, computes Pearson r (with and without spike-failure points) and degree-2 polynomial
   fit with pooled and per-sweep RMSE, writes `results/collapse_stats.json` and
   `results/metrics.json` (14 variants, registered `direction_selectivity_index` metric).
7. Created the answer asset at
   `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/` with `details.json`
   (v2 spec), `short_answer.md` (2-5 sentence conclusion-first answer), and `full_answer.md` (9
   mandatory sections including the t0033 2-D recommendation paragraph in Synthesis).
8. Ran flowmark (width 100) on both answer markdown files via `/tmp` workaround due to the long
   Windows path of the answer asset directory.
9. Ran `ruff check --fix .` (one fix — line length in test_collapse.py), `ruff format .` (3 files
   reformatted), and `mypy -p tasks.t0041_electrotonic_length_collapse_t0034_t0035.code` (no
   issues). Full-project mypy: 0 issues across 256 source files.
10. Re-ran the full pipeline (compute -> plot -> test) after formatting to confirm identical numeric
    output.
11. Ran verify_task_folder (PASSED — 1 warning on empty `logs/searches/`) and verify_task_metrics
    (PASSED — no errors or warnings after renaming `L_over_lambda` -> `l_over_lambda` in the
    metrics-variant dimensions block to satisfy the snake_case rule). No `verify_answer_asset`
    script exists in this repo snapshot; answer-asset structure conforms to
    `meta/asset_types/answer/specification.md` v2.

## Outputs

### Code (7 Python files, all lint + mypy clean)

* `code/paths.py` — centralised Path constants.
* `code/constants.py` — passive cable constants (RA, Rm), baseline L/d, sweep grid, CSV headers,
  collapse thresholds.
* `code/vector_sum.py` — Mazurek vector-sum helper (copied from t0034 analyse_sweep.py).
* `code/metrics_csv_reader.py` — upstream per-multiplier metrics CSV reader (copied and
  generalised from t0034 plot_sweep.py).
* `code/compute_electrotonic_length.py` — L/lambda computation and table writer.
* `code/plot_collapse.py` — three 300 dpi overlay PNGs.
* `code/test_collapse.py` — Pearson r + poly2 fit + verdict writer.

### Data

* `results/electrotonic_length_table.csv` — 14-row per-operating-point electrotonic table.
* `results/collapse_stats.json` — full CollapseReport with Pearson r summaries (with/without
  spike-failure), poly2 coefficients, pooled and per-sweep RMSE, verdicts.
* `results/metrics.json` — explicit multi-variant format, 14 variants (one per operating point)
  carrying `direction_selectivity_index` and `l_over_lambda` dimension.

### Charts (results/images/, 300 dpi)

* `primary_dsi_vs_L_over_lambda.png` — REQ-2 headline.
* `vector_sum_dsi_vs_L_over_lambda.png` — REQ-2 headline.
* `peak_hz_vs_L_over_lambda.png` — context panel.

### Assets

* `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/details.json` (v2).
* `assets/answer/.../short_answer.md` — conclusion-first 2-5 sentence answer.
* `assets/answer/.../full_answer.md` — 9 mandatory sections including t0033 parameterisation
  recommendation.

## Issues

No issues encountered. Three noteworthy notes:

1. **Baseline distal L in the plan was wrong**: the plan's placeholder
   `BASELINE_DISTAL_LENGTH_UM = 50.0` did not match the real t0024 morphology, whose 177 terminal
   dends have mean length 22.63 um (total 4004.83 um / 177). The actual value was used and
   documented in `code/constants.py`.
2. **n=3 paired samples in the overlap**: the two sweeps' L/lambda ranges overlap on only
   [0.058, 0.116], giving n=3 paired t0034 points (multipliers 0.75, 1.0, 1.25). The Pearson r is
   therefore low-power. However, the vector-sum r being NEGATIVE (-0.68) is the strongest
   qualitative evidence: the two sweeps trend in opposite directions through the overlap, which is
   incompatible with cable-theory collapse regardless of sample size.
3. **Flowmark failed on the very long Windows path** (answer asset folder name is 57 chars combined
   with the deep worktree path exceeds 260 chars when flowmark appends its `.<hash>.partial`
   suffix). Worked around by copying the files to `/tmp`, running flowmark, and copying back.
   LongPathsEnabled is 0 on this machine.

## Requirement Completion Checklist

| REQ | Status | Evidence |
| --- | --- | --- |
| REQ-1 — L/lambda per operating point for t0034's 7 length and t0035's 7 diameter multipliers using t0024 distal Rm and Ra | **done** | `results/electrotonic_length_table.csv` (14 rows with `effective_L_um`, `effective_d_um`, `lambda_um`, `L_over_lambda`); computation in `code/compute_electrotonic_length.py::compute_lambda_um` |
| REQ-2 — Overlay primary DSI vs L/lambda AND vector-sum DSI vs L/lambda for both sweeps on same axes | **done** | `results/images/primary_dsi_vs_L_over_lambda.png` and `results/images/vector_sum_dsi_vs_L_over_lambda.png`, both with distinct colour + marker per sweep and hollow markers on spike-failure points |
| REQ-3 — Pearson r between t0034 and t0035 on shared L/lambda axis with verdict collapse_confirmed (r > 0.9) or collapse_rejected | **done** | Primary r = +0.4161 (p=0.727), vector-sum r = -0.6787 (p=0.525); both below 0.9 -> `verdict_overall = collapse_rejected` in `results/collapse_stats.json` |
| REQ-4 — Residual variance after fitting single L/lambda-parameterised curve | **done** | Poly2 pooled RMSE: primary 0.0397, vector-sum 0.0237; per-sweep RMSE in `collapse_stats.json` fields `poly_fit_primary` and `poly_fit_vector_sum` |
| REQ-5 — One answer asset at `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/` with details.json, short_answer.md, full_answer.md | **done** | Three files present, spec_version "2", all 9 mandatory sections in full_answer.md, 2-5-sentence short_answer.md, citation-free short answer, evidence references recorded in details.json |
| REQ-6 — One-paragraph recommendation for t0033 morphology parameterisation in full_answer.md | **done** | `## Synthesis` section of `full_answer.md` ends with the explicit "Recommendation for t0033" paragraph stating 2-D (raw L x raw d) over 1-D L/lambda |
