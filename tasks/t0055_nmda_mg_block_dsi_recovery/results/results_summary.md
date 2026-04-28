# t0055 Results Summary — Mg-Block NMDA DSI Recovery

## Summary

Voltage-dependent (Jahr-Stevens Mg-block) NMDA at every E synapse **recovers vector-sum DSI** from
t0054's collapsed 0.082 (gNMDA = 0.25 nS, voltage-independent) back to **0.7464**, a 9× recovery
and bit-identical to the gNMDA = 0 baseline. **Peak rate stays at 0.667 Hz** at every gNMDA value
because the scalar gabaMOD inhibition prevents the soma from depolarising above the Mg-unblock
threshold. The S-0054-01 pass criterion (DSI > 0.50 AND peak Hz >= 5 Hz at gNMDA = 0.25, FULL) is
**PARTIAL: PASS on DSI, FAIL on peak-Hz**.

## Metrics

* **Vector-sum DSI at gNMDA = 0.25 nS, FULL = 0.7464** vs t0054's 0.082 — a **9.1× recovery** and
  identical to gNMDA = 0 (PASS, threshold > 0.50)
* **Peak Hz at gNMDA = 0.25 nS, FULL = 0.667 Hz** — unchanged from gNMDA = 0 baseline (FAIL,
  threshold >= 5 Hz)
* **DSI is gNMDA-invariant in FULL mode**: 0.7464 at every gNMDA in {0, 0.25, 0.5, 1.0} nS — Mg
  block keeps NMDA fully blocked under inhibition
* **E_ONLY mode reveals NMDA does activate without GABA**: peak Hz rises from 0.667 (gNMDA = 0) to
  1.333 (gNMDA >= 0.25), confirming the Mg-block kinetics work — they are simply outpaced by the
  strong gabaMOD when GABA is restored
* **gNMDA = 0 cross-task regression vs t0054**: max |rate diff| = **0.000e+00 Hz across 120 rows**
  — placement, AMPA, GABA, and HH soma + AIS are bit-identical
* **NMDA voltage-dependence sanity (single-synapse SEClamp at v ∈ {-80, -60, -40, -20, 0, +20}
  mV)**: peak gNMDA monotonic across voltages; ratio peak(-80) / peak(-20) = 0.0167 — Mg block
  strongly attenuates conductance at hyperpolarised voltages as predicted

## Verification

* `verify_task_metrics.py` — PASSED (0 errors, 0 warnings)
* `verify_task_folder.py` — PASSED (0 errors, 1 minor warning: `logs/searches/` empty)
* `verify_research_code.py` — PASSED (0 errors, 0 warnings)
* `verify_plan.py` — PASSED (0 errors, 0 warnings)
* gNMDA = 0 cross-task regression gate — PASSED (0.000e+00 Hz max diff vs t0054)
* Quiescent rest test — PASSED (V_rest = -64.5611 mV, within ±0.5 mV)
* Placement bit-identity vs t0054 — PASSED (all 100 pairs match within 1e-9)
* NMDA voltage-dependence sanity — PASSED (monotonic, ratio < 0.25 at v_clamp=-80 mV)
* gabaMOD scalar — PASSED (PD = 0.33, ND = 0.99, ratio = 3.0)

For the full requirement-level coverage and detailed numbers, see `results_detailed.md`.
