---
spec_version: "1"
task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
---
# Research Code: Prior-Task Code Reuse for t0039

## Task Objective

Identify the reusable code from prior tasks that can be copied into t0039's `code/` folder and
adapted for the 7-diameter sweep at `GABA_CONDUCTANCE_NULL_NS = 4.0` on the t0022 testbed. Per the
ARF cross-task import rule (CLAUDE.md rule 9: tasks must not import from other tasks' code
directories; only libraries are importable), all reused code must be copied.

## Library Landscape

Two libraries are importable across tasks:

* `tasks.t0022_modify_dsgc_channel_testbed.code.*` (treated as library imports via t0022 package
  symbols — matches pattern used by t0030, t0036, t0037).
* `tasks.t0008_port_modeldb_189347.code.build_cell` (cell-build helpers; imported by every DSGC
  sweep task).
* `tasks.t0011_response_visualization_library.code.tuning_curve_viz` (polar / overlay plotting used
  by `plot_sweep.py`).
* `tasks.t0012_build_wsd_data_loader_and_scorer.code.tuning_curve_loss` (DSI scoring — not
  directly imported here but consumed via `analyse_sweep.py`).

## Reusable Code and Assets

### From t0030 (diameter sweep driver)

* `constants.py` — `DIAMETER_MULTIPLIERS`, `PREFLIGHT_DIAMETER_MULTIPLIERS`, CSV columns,
  mechanism classification thresholds. **Copied verbatim**.
* `paths.py` — centralised `Path` constants anchored at task root. **Copied**, `TASK_ID` updated.
* `diameter_override.py` — `identify_distal_sections`, `snapshot_distal_diameters`,
  `set_distal_diameter_multiplier`, `assert_distal_diameters`. **Copied verbatim**.
* `preflight_distal.py`, `analyse_sweep.py`, `classify_slope.py`, `plot_sweep.py`, `run_sweep.py`,
  `trial_runner_diameter.py` — **copied**, module-path self-references bulk-renamed from
  `t0030_distal_dendrite_diameter_sweep_dsgc` →
  `t0039_distal_dendrite_diameter_sweep_t0022_gaba4`.

### From t0037 (null-GABA override)

* `gaba_override.py` — `set_null_gaba_ns(value_ns: float)` runtime patch of
  `tasks.t0022...constants.GABA_CONDUCTANCE_NULL_NS`. **Copied verbatim** (no renaming needed; no
  inter-task references).

### Substantive edits in t0039

* `constants.py` — added `GABA_NULL_NS_VALUE: float = 4.0` for the fixed GABA level.
* `trial_runner_diameter.py` — merged t0030's diameter override pattern with t0037's lazy re-read
  of the patched `GABA_CONDUCTANCE_NULL_NS`. Both overrides apply at every trial. The
  `schedule_ei_onsets` call now computes `gaba_null_pref_ratio` from the effective (post-patch)
  value, matching the t0037 pattern that cleared the `run_tuning_curve.py:327` assertion.
* `run_sweep.py` — calls `set_null_gaba_ns(value_ns=GABA_NULL_NS_VALUE)` at startup as a
  belt-and-braces patch. Outer loop iterates diameter multipliers (not GABA levels as in t0037).

## Key Findings

1. **The t0037 lazy re-read pattern is the canonical way** to apply a runtime GABA patch inside a
   trial runner without triggering the `run_tuning_curve.py:327` assertion. The fix is to re-import
   `GABA_CONDUCTANCE_NULL_NS` AFTER `set_null_gaba_ns` has fired, so the local binding sees the
   updated value.
2. **Diameter and GABA overrides are orthogonal** — both can be applied in the same trial with no
   ordering conflict beyond `apply_params` (which resets v_init and Random123) having to run first.
3. **No analytical code from t0030 needs modification** — `analyse_sweep.py`, `classify_slope.py`,
   and `plot_sweep.py` all operate on the per-trial CSV format, which is unchanged. The mechanism
   classification thresholds (MIN_SLOPE_MAGNITUDE, MAX_P_VALUE, DSI_SATURATION_THRESHOLD) are
   inherited from t0030 as-is.

## Lessons Learned

* When merging two upstream runners that each monkey-patch a module-level constant, keep the
  `from X import Y as _Y` lazy re-read pattern localised to one helper; do not distribute it across
  call sites.
* The ARF copy-not-import rule makes code reuse verbose but keeps the dependency graph explicit,
  which matters when inherited behaviour (like the `run_tuning_curve.py` assertion) changes between
  tasks.

## Recommendations for This Task

1. Use t0037's trial runner pattern, merged with t0030's diameter override. See
   `code/trial_runner_diameter.py`.
2. Keep the analysis / classification / plotting code byte-identical to t0030 so the slope fit is
   directly comparable.
3. Run a preflight (3 diameters × 3 angles × 2 trials = 18 trials) before the full 840-trial sweep
   to validate the merged overrides.

## Task Index

| Task | Code Reused | Notes |
| --- | --- | --- |
| t0022 | constants, `run_tuning_curve`, `neuron_bootstrap` | library-style imports |
| t0008 | `build_cell` helpers | library-style imports |
| t0030 | constants, paths, diameter_override, runner, analysis, classifier, plot | copied |
| t0037 | `gaba_override` | copied |
| t0036 | (ancestor of t0037; not directly copied) | - |
| t0011 | `tuning_curve_viz` | library-style imports (via `plot_sweep.py`) |
