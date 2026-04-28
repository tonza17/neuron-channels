# Results Summary: Minimal DSGC with AMPA + NMDA Excitation and Scalar gabaMOD

## Summary

Built a minimal DSGC extending t0052 with co-located NMDA `Exp2Syn` (tau1=5 ms, tau2=80 ms, e=0 mV)
at every E synapse and ran a 4-value gNMDA sweep (`{0.0, 0.25, 0.5, 1.0}` nS) × 12 directions × 10
trials × 3 modes (1440 trials, 4 h 19 min wall-clock on local CPU). The gNMDA=0 regression gate
against t0052's `tuning_curve_full.csv` passed at **max |rate diff| = 0.000e+00 Hz** across all 120
rows. Headline finding: NMDA dramatically closes the peak-rate gap (peak Hz at preferred direction
goes from 0.667 (t0052) to 8.0 at gNMDA=0.25 nS), but scalar `gabaMOD` inhibition is too weak to
maintain direction selectivity once NMDA is active — vector-sum DSI collapses from 0.746 (gNMDA=0)
to 0.082 (gNMDA=0.25) and approaches 0 at higher gNMDA.

## Metrics

* **gNMDA=0.0 nS, FULL**: peak 0.667 Hz, null 0.000 Hz, vector-sum DSI 0.746, primary DSI 1.000
  (degenerate). **Matches t0052 exactly** — regression gate passed at 0e+00 Hz max diff.
* **gNMDA=0.25 nS, FULL**: peak 8.000 Hz, null 6.000 Hz, vector-sum DSI 0.082. ~12× firing rate vs
  gNMDA=0; DSI collapses ~9×.
* **gNMDA=0.5 nS, FULL**: peak 7.333 Hz, null 6.000 Hz, vector-sum DSI 0.029. Saturating; scalar
  gabaMOD can't keep up with NMDA-amplified excitation.
* **gNMDA=1.0 nS, FULL**: peak 4.667 Hz, null 4.667 Hz, vector-sum DSI 0.017. Effectively zero DSI
  at high NMDA — preferred and null directions fire at the same rate.
* **AMPA + NMDA only (E_ONLY)** at gNMDA=0.25/0.5/1.0: 6.7 / 4.7 / multiple Hz — confirms
  excitation is no longer single-spike-per-trial like t0052.
* **GABA_ONLY** at all gNMDA values: 0.000 Hz (no excitation, no spikes — sanity check).
* **EPSP decay-to-1/e** (REQ-20): null for all 4 gNMDA values; the windowed E_ONLY trace doesn't
  return below 1/e of peak within the trial because stacked NMDA conductance keeps the cell
  depolarised at trial end. Qualitative decay-vs-gNMDA effect is visible in the per-direction EPSP
  PNGs (sweep_summary `epsp_decay_vs_gnmda.png` plot is rendered but shows an empty / null y-axis).

## Verification

* `meta.asset_types.library.verificator minimal_dsgc_ampa_nmda_scalar_gaba` — **PASSED** (0 errors
  / 0 warnings).
* `verify_task_metrics t0054_minimal_dsgc_ampa_nmda_scalar_gaba` — **PASSED** (0/0).
* gNMDA=0 regression gate (compute_metrics.py): **PASSED** at max |rate diff| = 0.000e+00 Hz vs
  t0052's tuning_curve_full.csv across 120 rows.
* Quiescent-rest gate: V_rest = -64.56 mV (within ±0.5 mV target).
* Placement bit-identical to t0052 — `test_placement_seed0_match.py` PASSED.
* NMDA-inert smoke test at gNMDA=0: rate matched t0052 within 1e-6 Hz before the sweep.
* `ruff check` / `ruff format` — clean across all task code modules.
* `mypy .` — no issues across 265 source files.
