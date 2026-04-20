# Results Summary: Tuning-Curve Scoring Loss Library

## Summary

Built and registered the `tuning_curve_loss` Python library: an 8-module package that loads a DSGC
tuning curve from CSV, computes DSI, peak, null, and HWHM, and scores a candidate curve against the
t0004 target as a weighted Euclidean residual in envelope-half-width units. The identity gate
`score(target, target).loss_scalar == 0.0` and `passes_envelope is True` holds exactly. All 47
pytest tests pass, ruff and mypy are clean, and the library asset is registered at
`assets/library/tuning_curve_loss/`.

## Metrics

* **Tests passed**: **47 / 47** (0 failed, 0 skipped)
* **Identity loss on t0004 target**: **0.0** (exact)
* **Library modules**: **8** (paths, loader, metrics, envelope, weights, scoring, cli, `__init__`)
* **Public entry points**: **13** (score, compute_dsi, compute_peak_hz, compute_null_hz,
  compute_hwhm_deg, compute_reliability, load_tuning_curve, passes_envelope, validate_weights,
  load_weights_from_json, Envelope, ScoreResult, TuningCurveMetrics)
* **Test modules**: **5** covering loader, metrics, envelope, scoring, and CLI
* **Registered metric keys mapped**: **4** (direction_selectivity_index, tuning_curve_hwhm_deg,
  tuning_curve_reliability, tuning_curve_rmse)
* **DSI on t0004 target**: **0.8824** (matches closed-form `(32 − 2) / (32 + 2)`)
* **HWHM on t0004 target**: **60°** (from 12-angle grid with rotation-based interpolation)

## Verification

* `uv run pytest tasks/t0012_tuning_curve_scoring_loss_library/code -q` — **47 passed**, 0 failed,
  0 skipped
* `uv run ruff check tasks/t0012_tuning_curve_scoring_loss_library/` — PASSED (0 errors)
* `uv run ruff format --check tasks/t0012_tuning_curve_scoring_loss_library/` — PASSED (15 files
  already formatted)
* `uv run mypy .` — PASSED (238 files clean)
* `verify_plan t0012_tuning_curve_scoring_loss_library` — PASSED (0 errors, 0 warnings)
* `verify_research_internet t0012_tuning_curve_scoring_loss_library` — PASSED (0 errors, 0
  warnings)
* `verify_research_code t0012_tuning_curve_scoring_loss_library` — PASSED (0 errors, 0 warnings)
* Library-asset hand-validation against `meta/asset_types/library/specification.md` — PASSED (no
  `verify_library_asset.py` exists; fields, module_paths, ID regex, and 8 mandatory description
  sections all satisfied)
