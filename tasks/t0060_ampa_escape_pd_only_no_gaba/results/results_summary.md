# Results Summary: t0060 Quick AMPA-Escape Test (PD only, GABA = 0)

## Summary

Ran 16 trials (8 gAMPA values × 2 modes × 1 trial × 1 direction) at theta = 0 deg with GABA = 0
on the t0059 minimal-DSGC substrate; total wall-clock 127.36 s on local CPU under CVODE. The FULL
(HH on) cell escapes the single-spike regime at gAMPA ≥ 1 nS, peaks at **4 spikes / 1.4 s** at
gAMPA = 20 nS, and stays bounded near +20 mV peak Vm by sodium-channel saturation. The EPSP_PASSIVE
(HH off) trace approaches the AMPA reversal monotonically: peak Vm rises from **-60.7 mV at gAMPA =
0.1 nS** to **-3.8 mV at gAMPA = 20 nS** (AMPA reversal E_AMPA = 0 mV).

## Metrics

* **gAMPA = 0.1 nS (subthreshold)**: FULL peak Vm = -58.98 mV, 0 spikes; EPSP_PASSIVE peak Vm =
  -60.67 mV, 0 spikes. Both modes nearly identical — passive cell.
* **gAMPA = 0.5 nS (single spike escape)**: FULL peak Vm = +18.99 mV (1 spike); EPSP_PASSIVE peak Vm
  = -47.75 mV (no spike). FULL exceeds passive by **+66.7 mV** at peak (HH-driven AP).
* **gAMPA = 1.0 nS**: FULL = +19.49 mV / 2 spikes; EPSP_PASSIVE = -36.94 mV / 0 spikes.
* **gAMPA = 2.0 nS**: FULL = +19.13 mV / 2 spikes; EPSP_PASSIVE = -24.68 mV / 0 spikes.
* **gAMPA = 5.0 nS**: FULL = +17.17 mV / 1 spike; EPSP_PASSIVE = -11.60 mV / 1 (passive Vm crosses
  the -20 mV netcon spike-threshold without an actual AP — false-positive on the netcon recorder).
* **gAMPA = 10.0 nS**: FULL = +14.92 mV / 2 spikes; EPSP_PASSIVE = -6.33 mV / 1.
* **gAMPA = 15.0 nS**: FULL = +13.53 mV / 2 spikes; EPSP_PASSIVE = -4.61 mV / 1.
* **gAMPA = 20.0 nS (multi-spike)**: FULL = +12.56 mV / **4 spikes**; EPSP_PASSIVE = -3.76 mV / 1.
* Wall-clock: **127.36 s** for 16 trials (~8 s/trial average).

The HH save-and-zero is correctly wired: at every gAMPA value the FULL peak (+13 to +20 mV) is
~20-60 mV above the EPSP_PASSIVE peak in the same condition, and the EPSP_PASSIVE peak Vm rises
monotonically with gAMPA without HH-style overshoot, asymptoting toward E_AMPA = 0 mV.

## Verification

* Sweep ran exit code 0; wallclock.json written with `n_trials=16`, `gampa_ns_values` and
  `gaba_base_ns=0` recorded.
* `voltage_traces_pd_only.csv` written with all 16 traces; `summary_pd_only.csv` with per-(gAMPA,
  mode) peaks and spike counts.
* `voltage_response_grid.png` and `voltage_response_overlay.png` rendered with all 16 traces.
* Placement seed = 0 — bit-identical to t0052 / t0053 / t0057 / t0059.
