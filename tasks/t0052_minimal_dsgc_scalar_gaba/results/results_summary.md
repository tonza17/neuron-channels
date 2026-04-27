# Results Summary: Minimal From-Scratch DSGC with Scalar gabaMOD Inhibition

## Summary

Built a from-scratch minimal DSGC on `dsgc-baseline-morphology-calibrated` with 100 E + 100 I
co-located synapses, position-gated AMPA-only excitation, and scalar `gabaMOD`-scaled inhibition;
ran the full 12-direction × 10-trial × 3-mode sweep (360 trials in 19 min 13 s on local CPU). The
cell produces **primary DSI = 1.0** in FULL mode (null direction silent, all preferred-side
directions fire 0.667 Hz = 1 spike/trial), **vector-sum DSI = 0.746**, and preferred direction = 0°
as designed. The IPSP conductance ratio `gabaMOD(180)/gabaMOD(0) = 3.0` matches the spec exactly;
the observed somatic IPSP voltage ratio of 1.54 reflects driving-force saturation under realistic
synaptic crowding and is the headline secondary finding.

## Metrics

* **Primary DSI (FULL)**: **1.000** — perfect; null direction never spikes (all spikes occur on
  the preferred half of the angle wheel, consistent with `gabaMOD(180) = 0.99` fully shunting
  null-direction firing).
* **Vector-sum DSI (FULL)**: **0.746** — high but below the perfect-1.0 primary DSI because
  multiple preferred-side angles fire equally (the cell is broadly tuned at the chosen AMPA / GABA
  gain).
* **Peak firing rate (FULL, preferred direction)**: **0.667 Hz** = 1 spike per 1500 ms trial on
  every preferred-side direction; **null-direction rate = 0.000 Hz**.
* **Preferred direction**: **0°** (rightward, as designed by `θ_PD = 0`).
* **HWHM**: **82.5°** — broad tuning curve, consistent with a cell that fires a single spike at
  peak excitation across all directions where IPSP suppression is sub-threshold.
* **Tuning-curve reliability (FULL)**: **1.000** — perfect consistency across the 10 trials per
  direction (single-spike-per-trial deterministic firing).
* **Tuning-curve RMSE vs t0004 target**: **16.98 Hz** — large because the t0004 target peaks near
  30 Hz while this minimal model peaks at 0.67 Hz.
* **IPSP conductance ratio (gNULL / gPD)**: **3.0** — exactly matches the
  `gabaMOD(180)/gabaMOD(0) = 1.0/0.33` design target. Hard-fail assertion in `compute_metrics.py`
  passed.
* **IPSP somatic voltage ratio (gNULL_voltage / gPD_voltage)**: **1.54** — substantially below the
  3.0 conductance ratio because driving force `(V − E_GABA)` saturates as multiple GABA synapses
  fire near-synchronously and local Vm approaches `E_GABA = −75 mV`. Reported as a derived
  observable, not a gate.
* **AMPA-only DSI**: **0.0** — confirms inhibition is the entire source of direction selectivity;
  AMPA alone fires uniformly across all directions.
* **GABA-only spikes**: **0** — confirms no excitation without AMPA.

## Verification

* `verify_library_asset.py minimal_dsgc_scalar_gaba` — **PASSED** (0 errors / 0 warnings).
* `verify_task_metrics.py t0052_minimal_dsgc_scalar_gaba` — **PASSED** (0 errors / 0 warnings).
* `verify_step.py implementation` — **PASSED** (0 errors / 0 warnings).
* `verify_research_code.py` — **PASSED** (0 errors / 0 warnings).
* `verify_plan.py` — **PASSED** (0 errors / 0 warnings).
* `ruff check` and `ruff format` — clean across all 15 task code modules.
* `mypy -p tasks.t0052_minimal_dsgc_scalar_gaba.code` — no issues across 263 source files.
* IPSP-ratio hard gate (`compute_metrics.py`): `gNULL/gPD = 3.0 ∈ [2.7, 3.3]` — **PASSED**.
* Quiescent-rest gate (`test_quiescent_rest.py`): `V_rest = -65 mV ± 0.5 mV` — **PASSED**.
* Dry-run validation gate (1 angle × 2 trials × 3 modes before full sweep) — **PASSED**.
