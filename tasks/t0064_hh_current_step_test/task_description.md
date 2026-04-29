# HH Current-Step Diagnostic on t0059 Substrate (No Synapses)

## Source

User-commissioned diagnostic, follow-up to t0063 (voltage clamp). Switches to current clamp so
APs can fire. Tests the HH model's spiking output as a function of injected current.

## Protocol

* No synaptic input. IClamp on `soma(0.5)`.
* IClamp protocol:
  * `delay = 50 ms` (initial rest period).
  * `dur = 200 ms` (current step).
  * `amp = target_na` (one of 6 values).
* Total trial: 300 ms.
* Currents: **{0.1, 0.2, 0.3, 0.5, 1.0, 2.0} nA**.
* Modes: **FULL** (HH on, soma + AIS) and **EPSP_PASSIVE** (HH save-and-zero on soma + AIS).
* 6 currents × 2 modes × 1 trial = **12 trials**. Wall-clock ~30-60 s.

## Outputs

* `results/voltage_traces.csv` — Vm and current trace per (target, mode).
* `results/summary.csv` — peak Vm, spike count per (target, mode).
* `results/images/voltage_response_grid.png` — 6 panels (one per current), Vm in both modes.
* `results/images/voltage_response_overlay.png` — all 12 traces overlaid.

## Architecture

Same as t0063 (cell from t0059, soma + AIS HH, passive dendrites) but with IClamp instead of
SEClamp. HH save-and-zero protocol same as before.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.
