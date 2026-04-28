# Results Summary: Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Summary

Replaced t0053's per-event Exp2Syn GABA with a sustained `gaba_tonic` POINT_PROCESS (conductance
held over a configurable `(t_on, t_off) = (100 ms, 1400 ms)` window) and ran a 1800-trial sweep
across `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS. Headline negative finding: no operating
point in the swept grid produces non-trivial direction selectivity. Below 1.5 nS the cell fires its
single-spike-per-trial regime uniformly across all directions (peak = null = 0.667 Hz, identical to
AMPA_ONLY); at 1.5 and 2.0 nS the cell is fully suppressed (peak = null = 0 Hz). The active-fraction
modulation (0.34 → 0.66 across directions) confirms the spatial centripetal-gating rule is intact;
the failure is amplitude calibration interacting with the sustained mechanism, not the gating.

## Metrics

* **Primary DSI (FULL) at all 5 conductances**: **0.0** (degenerate — peak = null at every swept
  value).
* **Vector-sum DSI (FULL) at all 5 conductances**: **0.0** (3.2e-17 numerical floor for the three
  sub-threshold-suppression values; 0.0 exact for the two fully-suppressed values).
* **Peak Hz at gaba in {0.25, 0.5, 1.0} nS**: **0.667 Hz** (identical to AMPA_ONLY single-spike
  regime — tonic GABA at these levels is too weak to override the single AMPA spike).
* **Peak Hz at gaba in {1.5, 2.0} nS**: **0.0 Hz** (full suppression — tonic GABA strong enough to
  keep V below threshold continuously).
* **AMPA_ONLY peak Hz** at all 5 conductances: **0.6667 Hz** uniformly across all 12 directions —
  bit-identical to t0052 / t0053 AMPA_ONLY result. **REQ-14 PASS.**
* **Tuning-curve RMSE vs t0004 target** (FULL): **16.67 Hz** (gaba ≤ 1.0 nS) and **17.18 Hz**
  (gaba ≥ 1.5 nS) — large because the t0004 target peaks near 32 Hz while this model peaks at
  0.667 Hz or 0 Hz.
* **Active-fraction modulation** across directions: **0.34 (θ = 30°) to 0.66 (θ = 210°)**; mean
  **0.500** ∈ [0.4, 0.6] soft band — **PASS**. Bit-identical to t0053 since the spatial gating
  rule is unchanged.
* **Aggregate IPSP voltage envelope** (most-active direction θ = 210°, FULL mode):
  * gaba = 0.25 nS: peak **3.17 mV**
  * gaba = 0.50 nS: peak **4.88 mV**
  * gaba = 1.00 nS: peak **6.55 mV**
  * gaba = 1.50 nS: peak **7.38 mV**
  * gaba = 2.00 nS: peak **7.87 mV**
  * IPSP grows sub-linearly with gaba — driving-force saturation as Vm approaches
    `E_GABA = -75 mV`. The 0.25 → 2.0 nS conductance ratio of 8x produces only a 2.5x
    voltage-envelope ratio.
* **Aggregate EPSP magnitude** (peak ≈ 84 mV above V_rest at all directions and all conductances)
  — confirms AMPA mechanism untouched and direction-independent.
* **Wall-clock**: **6318.34 s = 105.31 min** for 1800 trials (single-threaded local CPU).

## Verification

* `verify_library_asset.py minimal_dsgc_tonic_gaba_sweep` — **PASSED** (0/0).
* `verify_task_metrics.py t0057_tonic_gaba_sweep_t0053` — **PASSED** (0/0).
* `ruff check` and `ruff format` — clean across all task code modules.
* `mypy -p tasks.t0057_tonic_gaba_sweep_t0053.code` — no issues.
* AMPA_ONLY 0.667 Hz regression sentinel (REQ-14): **PASSED** at all 5 conductances.
* IPSP-sustained-window regression test (REQ-13): **PASSED** at all 5 conductances (IPSP at t = 1300
  ms is at least 50% of IPSP at t = 200 ms in the most-active direction — the new tonic mechanism
  is delivering sustained conductance over the full window as designed).
* Placement bit-identical to t0052 / t0053 (`test_placement_seed0_match.py`): **PASSED**.
* Quiescent-rest gate (`test_quiescent_rest.py`, V_rest = -65 mV ± 0.5 mV): **PASSED**.
* Spatial-gating unit test (`test_spatial_gating.py`): **PASSED**.
