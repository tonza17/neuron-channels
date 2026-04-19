# Tuning-curve scoring loss library

## Motivation

The t0002 literature survey set four concurrent quantitative targets an optimised DSGC model must
hit: DSI **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM **60-90°**. The
project has four registered metrics (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
`tuning_curve_reliability`, `tuning_curve_rmse`). Every downstream optimisation task (Na/K grid
search S-0002-01, morphology sweep S-0002-04, E/I ratio scan S-0002-05, active-vs-passive dendrites
S-0002-02) needs a shared scoring function: same target, same weighting, same tie-breaks. Without
this library, each task will invent its own scoring and cross-task comparisons of "who wins" become
meaningless. This task provides that canonical scorer.

Covers suggestion **S-0002-09** (and subsumes **S-0004-03** — see the t0006 correction file).

## Scope

The library `tuning_curve_loss` exposes:

1. `score(simulated_curve_csv, target_curve_csv | None) -> ScoreReport` — returns a frozen dataclass
   containing:
   * `loss_scalar` (float) — weighted-Euclidean-distance-in-normalised-space loss combining the four
     envelope targets.
   * `dsi_residual`, `peak_residual_hz`, `null_residual_hz`, `hwhm_residual_deg` — individual
     residuals with signs.
   * `rmse_vs_target` — point-wise RMSE of `(angle, firing_rate)` against the target curve (only
     when a target is supplied).
   * `reliability` — cross-trial coefficient of determination (maps onto the registered
     `tuning_curve_reliability` metric).
   * `passes_envelope` (bool) — whether the simulated curve lands inside the t0002 envelope on all
     four targets simultaneously.
   * `per_target_pass` — dict `{"dsi": bool, "peak": bool, "null": bool, "hwhm": bool}`.
2. `compute_dsi(curve_csv) -> float`
3. `compute_preferred_peak_hz(curve_csv) -> float`
4. `compute_null_residual_hz(curve_csv) -> float`
5. `compute_hwhm_deg(curve_csv) -> float`
6. Tuning-curve CSV schema constant: `(angle_deg, trial_seed, firing_rate_hz)`.
7. CLI: `python -m tuning_curve_loss.cli <simulated.csv> [--target <target.csv>]`.

Weights for the scalar loss default to **DSI 0.25, peak 0.25, null 0.25, HWHM 0.25** but are
user-overridable via a keyword argument and via a JSON config file; the defaults and rationale are
documented in the asset's `description.md`.

## Dependencies

* **t0004_generate_target_tuning_curve** — source of the canonical `target-tuning-curve` dataset
  used as the default comparison target and as the smoke-test fixture.

## Expected Outputs

* **1 library asset** (`assets/library/tuning-curve-loss/`) with:
  * `description.md` covering API, weight defaults, and worked examples
  * `module_paths` pointing at `code/tuning_curve_loss/`
  * `test_paths` pointing at `code/tuning_curve_loss/test_*.py` with at least:
    * Identity test: `score(target, target)` must return `loss_scalar == 0.0` and
      `passes_envelope is True`.
    * Envelope-boundary tests: hand-crafted curves just inside and just outside each of the four
      envelope boundaries.
    * Reliability test: two curves with identical trial-means but very different trial-to-trial
      variance produce different `reliability` values.

## Approach

Pure Python + NumPy + pandas. No simulator dependency. The DSI and HWHM computations must match the
closed-form computations used in t0004 to produce the target curve, so that `score(target, target)`
is exactly zero. Use the registered metric keys from `meta/metrics/` so that scored values can be
written directly into `results/metrics.json` without post-hoc renaming.

## Questions the task answers

1. Does `score(target, target)` return `loss_scalar == 0.0`?
2. Do the envelope-boundary tests flip `passes_envelope` at the correct boundary to within
   floating-point tolerance?
3. Does the scorer accept multi-trial CSVs and correctly combine trials into a mean before computing
   DSI, peak, null and HWHM?

## Risks and Fallbacks

* **The literature envelope numbers conflict with the t0004 target curve** (e.g., the target sits
  right at an envelope boundary): document the target's position on the envelope in the library
  description; do not silently redefine targets.
* **Trial-to-trial variance inflates `reliability` beyond sensible bounds**: clamp to [0, 1] and
  document the clamp.
