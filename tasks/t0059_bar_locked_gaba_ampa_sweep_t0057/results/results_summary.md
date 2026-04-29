# Results Summary: Bar-Arrival-Locked Tonic GABA + AMPA Escape Sweep on t0057 Substrate

## Summary

Forked t0057's `minimal_dsgc_tonic_gaba_sweep` library, replaced the global
`(t_on, t_off) = (100, 1400) ms` tonic-GABA window with per-synapse bar-arrival-locked windows
`t_on_i = (x_i cos theta + y_i sin theta) / v + 100 ms`, `t_off_i = t_on_i + 200 ms`, swept a 5x5
`(gAMPA, GABA_BASE_NS)` grid over `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS x
`GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS, and bundled the project-wide S-0055-01
measurement-protocol fix (drop `AMPA_ONLY` / `GABA_ONLY`; add `EPSP_PASSIVE` / `IPSP_PASSIVE` with
HH save-and-zero on soma + AIS; standardise trial length at 1400 ms). Headline negative finding:
**no operating point in the swept grid produces multi-spike firing or non-trivial direction
selectivity**. The maximum FULL-mode peak rate across all 25 cells is **2.143 Hz** (3 spikes / 1.4
s, four cells); the maximum primary DSI is **0.5** at gAMPA=3.0/gaba=0.10 and 0.20; the maximum
vector-sum DSI is **0.209** at gAMPA=1.0/gaba=0.10. The bar-locked window mechanism and HH
save-and-zero protocol are both validated independently (REQ-13 IPSP centre-of-mass shift = 8.5 ms
between theta=0 and theta=90; REQ-15 worst-case EPSP_PASSIVE peak Vm = -9.04 mV << +5 mV gate
threshold).

## Metrics

* **Max FULL peak Hz across all 25 cells**: **2.143 Hz** (3 spikes / 1.4 s) at four cells:
  gAMPA=2.0/gaba=0.10, gAMPA=2.0/gaba=0.20, gAMPA=3.0/gaba=0.10, gAMPA=3.0/gaba=0.20. **No cell
  enters the 5-50 Hz multi-spike band** (RQ1 = NO).
* **Max primary DSI (FULL)**: **0.500** at gAMPA=3.0/gaba=0.10 and gAMPA=3.0/gaba=0.20 (peak Hz =
  2.143, null Hz = 0.714 — discrete-spike artefact, not a true tuned response).
* **Max vector-sum DSI (FULL)**: **0.209** at gAMPA=1.0/gaba=0.10. **No cell exceeds the 0.3
  vector-sum DSI threshold** (RQ2 = NO).
* **Best HWHM (FULL)**: **30.0 deg** at gAMPA=2.0/gaba=0.20 (peak Hz = 2.143, primary DSI = 0.2,
  vector-sum DSI = 0.196).
* **Regime distribution** (over 25 FULL cells): full-suppression (peak Hz = 0) = **1/25**;
  single-spike-degenerate (peak Hz = 0.714) = **9/25**; two-spike (peak Hz = 1.429) = **11/25**;
  three-spike (peak Hz = 2.143) = **4/25**; multi-spike (>= 5 Hz) = **0/25**.
* **Tuning-curve RMSE vs t0004 target (32 Hz peak)**: range **16.06 Hz** (best, gAMPA=2.0/gaba=0.10)
  to **17.18 Hz** (worst, gAMPA=0.5/gaba=2.0; full-suppression cell).
* **Bar-locked IPSP centre-of-mass shift** (REQ-13): **8.5 ms** between theta=0 and theta=90 in
  IPSP_PASSIVE traces — confirms the per-synapse bar-arrival-locked window mechanism is delivering
  direction-dependent inhibitory timing, which the global-window t0057 mechanism could not (RQ3 =
  YES).
* **HH save-and-zero correctness** (REQ-14, REQ-15): worst-case EPSP_PASSIVE peak Vm across all 300
  EPSP_PASSIVE direction-cells = **-9.04 mV** (well below the +5 mV gate, i.e., the soma is
  passive); FULL-mode bit-identity test passed against reference at atol = 1e-6 mV.
* **Active-fraction modulation** (carried over from t0053 / t0057 spatial gating, conductance- and
  gAMPA-independent): **0.34** (theta = 30 deg) to **0.66** (theta = 210 deg), mean **0.50** within
  the [0.4, 0.6] soft sanity band.
* **Wall-clock**: **41621.91 s = 11.56 h** for 9000 trials on single-threaded local CPU under CVODE
  (`atol = 1e-3`).

## Verification

* `verify_task_metrics.py t0059_bar_locked_gaba_ampa_sweep_t0057` — **PASSED** (0 errors, 0
  warnings); 75 variants (5 gAMPA x 5 gaba x 3 modes).
* `verify_task_results.py t0059_bar_locked_gaba_ampa_sweep_t0057` — **PASSED**.
* `verify_assets.py t0059_bar_locked_gaba_ampa_sweep_t0057` — **PASSED**
  (`minimal_dsgc_bar_locked_gaba_ampa_sweep` library asset, 0/0).
* `test_bar_locked_ipsp_envelope.py` (REQ-13): **PASSED** at gAMPA=1.0/gaba=1.0; centre-of-mass
  shift = 8.5 ms exceeds geometric lower bound.
* `test_hh_save_and_zero.py` (REQ-14): **PASSED**; FULL-mode reference trace match within atol =
  1e-6 mV.
* `test_placement_seed0_match.py` (REQ-16): **PASSED**; 100/100 pairs match t0057's
  `placement_seed0.json` at POSITION_TOLERANCE = 1e-9.
* `test_quiescent_rest.py`: **PASSED** (V_rest = -65 mV +/- 0.5 mV).
* `test_spatial_gating.py` (REQ-2): **PASSED** (4/4).
* EPSP_PASSIVE peak-Vm soft gate (REQ-15): **PASSED**; worst-case peak Vm = -9.04 mV across all
  EPSP_PASSIVE traces (gate threshold +5 mV).
