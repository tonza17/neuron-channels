# Results Summary: t0061 NMDA-Only PD Diagnostic

## Summary

Ran 16 trials (8 gNMDA values × 2 modes × 1 trial) at theta = 0 deg with GABA = 0, AMPA = 0,
NMDA-only excitation (Mg-block, Jahr-Stevens). Wall-clock 118.14 s on local CPU under CVODE.
Headline: **regenerative Mg-block escape between gNMDA = 1.0 nS** (peak Vm = -58.89 mV, 0 spikes)
**and gNMDA = 2.0 nS** (peak Vm = +11.29 mV, **3 spikes**). The NMDA plateau widens to ~200-400 ms
at gNMDA >= 5 nS, far longer than the AMPA EPSP in t0060 (~10 ms).

## Metrics

* **gNMDA = 0.1 nS**: FULL peak Vm = -64.22 mV, 0 spikes; EPSP_PASSIVE peak Vm = -64.47 mV, 0
  spikes. Mg block fully engaged.
* **gNMDA = 0.5 nS**: FULL peak = -62.61 mV, 0 spikes. Tiny depolarization.
* **gNMDA = 1.0 nS**: FULL peak = -58.89 mV, 0 spikes. Below the regenerative threshold.
* **gNMDA = 2.0 nS (Mg-block escape)**: FULL peak = +11.29 mV, **3 spikes**; EPSP_PASSIVE peak =
  -52.58 mV, 0 spikes. Sudden transition: depolarization unblocks Mg, NMDA opens, drives more
  depolarization, fires action potentials.
* **gNMDA = 5.0 nS**: FULL = +13.12 mV / 3 spikes; EPSP_PASSIVE = -8.59 mV / 1 (false threshold
  crossing).
* **gNMDA = 10.0 nS**: FULL = +13.21 mV / 3 spikes; EPSP_PASSIVE = -4.67 mV / 1 (false).
* **gNMDA = 15.0 nS**: FULL = +13.15 mV / 2 spikes; EPSP_PASSIVE = -3.37 mV / 1 (false).
* **gNMDA = 20.0 nS**: FULL = +13.21 mV / 1 spike (sodium-channel saturation truncates the spike
  train); EPSP_PASSIVE = -2.70 mV / 1 (false).
* Wall-clock: 118.14 s for 16 trials.

## Verification

* `wallclock.json` written; `voltage_traces_pd_only.csv` and `summary_pd_only.csv` complete.
* `voltage_response_grid.png` (8 panels) and `voltage_response_overlay.png` (16 traces) rendered.
* Placement seed = 0 (bit-identical to t0052/t0053/t0057/t0059/t0060).
* HH save-and-zero validated: EPSP_PASSIVE peak Vm asymptotes to E_AMPA = 0 mV (max -2.70 mV at
  gNMDA = 20 nS) without HH-driven overshoot.
