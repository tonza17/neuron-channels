# HH Voltage-Step Diagnostic on t0059 Substrate (No Synapses)

## Source

User-commissioned diagnostic to test the HH model on the t0059 substrate. No synaptic input —
just SEClamp voltage steps. Goal: characterise the HH active currents at each holding voltage.

## Protocol

* **No synapses constructed** — pure cell + SEClamp on soma.
* **SEClamp** on `soma(0.5)`:
  * `dur1 = 50 ms`, `amp1 = -65 mV` (hold at rest).
  * `dur2 = 200 ms`, `amp2 = target` (step to target voltage).
  * `dur3 = 50 ms`, `amp3 = -65 mV` (hold back at rest).
  * `rs = 0.001` MOhm (low series resistance for tight clamp).
* `TSTOP = 300 ms`.
* Targets: **-60, -50, -40, -30, -20, -10 mV** (6 levels).
* Modes: **FULL** (HH on, soma + AIS) and **EPSP_PASSIVE** (HH save-and-zero on soma + AIS).
* Record: soma Vm, SEClamp current `i`.
* Total: **6 targets x 2 modes x 1 trial = 12 trials**. Wall-clock estimate: ~30-60 s.

## Outputs

* `results/voltage_step_traces.csv` — long-format: gampa is unused, columns are
  `target_mv, mode, sample_idx, t_ms, v_soma_mv, i_clamp_na`.
* `results/summary_voltage_step.csv` — per-(target, mode) peak / steady-state Vm and clamp
  current.
* `results/images/voltage_step_grid.png` — 6 panels (one per target), each showing Vm in both
  modes.
* `results/images/clamp_current_grid.png` — 6 panels (one per target), each showing the
  SEClamp current in both modes — the difference between FULL and EPSP_PASSIVE is the pure
  HH contribution.

## Architecture

Reuses t0059's cell building (build_dsgc_from_swc) and neuron bootstrap. No synapses; only the
SEClamp is wired. HH save-and-zero protocol same as t0060/t0061/t0062.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.
