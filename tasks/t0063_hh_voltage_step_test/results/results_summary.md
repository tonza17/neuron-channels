# Results Summary: t0063 HH Voltage-Step Diagnostic

## Summary

Stepped the soma from -65 mV to {-60, -50, -40, -30, -20, -10} mV via SEClamp for 200 ms each, 12
trials (6 targets x 2 modes) in 24.60 s. SEClamp held Vm tight to target across all conditions. The
FULL-vs-PASSIVE clamp current difference reveals classic HH dynamics: transient inward Na+ current
at step onset (-13 to -15 nA) at all depolarised levels; sustained outward residual at -30 to -10 mV
(persistent K+ delayed-rectifier minus residual Na+) growing from ~+1 to +5 nA.

## Metrics

* **Tight clamp**: Vm tracks target voltage within 1 mV at all 6 targets in both modes (clamp rs =
  0.001 MOhm).
* **Capacitive transients**: clamp current spikes to the limit at step edges (-5000 nA at -60,
  -55000 nA at -10) due to dV/dt charging the soma capacitance — these are not HH currents.
* **HH transient (Na+ activation)**: at step onset, FULL clamp current dips ~15 nA below PASSIVE for
  ~5 ms, indicating brief inward Na+ activation before h-inactivation.
* **HH steady-state at -60 mV**: I_HH = 0 nA (Na+/K+ channels closed).
* **HH steady-state at -50 mV**: I_HH near 0 (Na+ activates briefly but inactivates; K+ slow).
* **HH steady-state at -40 / -30 mV**: I_HH = 0 to +1 nA (small outward, K+ rising slightly).
* **HH steady-state at -20 mV**: I_HH = +2.5 nA (clear outward K+ residual).
* **HH steady-state at -10 mV**: I_HH = +5 nA (persistent outward, dominated by K+ delayed
  rectifier).

## Verification

* `voltage_step_traces.csv`, `summary_voltage_step.csv`, `wallclock.json` produced.
* `voltage_step_grid.png` (6 panels, Vm) and `clamp_current_grid.png` (12 panels: zoomed clamp
  current + HH difference) rendered.
