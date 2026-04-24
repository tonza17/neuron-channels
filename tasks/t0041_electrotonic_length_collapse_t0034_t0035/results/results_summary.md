# Results Summary: t0041 Electrotonic-Length Collapse Analysis

## Summary

Tested whether primary DSI and vector-sum DSI from t0034 (distal length sweep) and t0035 (distal
diameter sweep) collapse onto a single DSI-vs-L/lambda curve under Rall's cable theory. **Verdict:
collapse_rejected.** The two sweeps do not share a common L/lambda parameterisation: Pearson r =
+0.42 for primary DSI and -0.68 for vector-sum DSI (sign inverted), both well below the 0.9
confirmation threshold. Recommendation for t0033: keep the 2-D (raw length x raw diameter)
morphology parameterisation.

## Metrics

* **Pearson r primary DSI (overlap region, n=3 paired points)**: **+0.4161** (p=0.727). Threshold
  for collapse_confirmed is r > 0.9. **Collapse rejected.**
* **Pearson r vector-sum DSI (overlap region, n=3 paired points)**: **-0.6787** (p=0.525). Sign is
  inverted from the cable-theory prediction. **Collapse rejected.**
* **Pooled polynomial-fit residual RMSE**: primary DSI **0.0397**, vector-sum DSI **0.0237**.
  Residuals of this magnitude relative to the 0.23 and 0.15 total DSI spread confirm that non-cable
  effects dominate the response.
* **Overlap region**: L/lambda in [0.058, 0.116] (3 paired points after interpolation).
* **Baseline distal-section geometry** (t0024 baseline): length 22.63 um (mean across 177 terminal
  dendrites), diameter 0.5 um, Rm 5999 ohm.cm^2, Ra 100 ohm.cm.
* **lambda at baseline**: 274.8 um; L/lambda at baseline: 0.082.

## Verification

* `verify_research_code.py` — PASSED (0 errors, 0 warnings).
* `verify_plan.py` — PASSED (0 errors, 2 cosmetic warnings).
* `verify_task_folder.py` — PASSED (1 warning: empty `logs/searches/`).
* `verify_task_metrics.py` — PASSED (0 errors, 0 warnings).
* `ruff check --fix .` and `ruff format .` — clean.
* `mypy -p tasks.t0041_electrotonic_length_collapse_t0034_t0035.code` — no issues.
* All six plan REQ items (REQ-1 through REQ-6) are marked done in `results/results_detailed.md`
  `## Task Requirement Coverage`.
