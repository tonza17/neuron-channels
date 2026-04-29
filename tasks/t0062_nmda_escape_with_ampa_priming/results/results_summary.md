# Results Summary: t0062 NMDA + AMPA-Priming PD Diagnostic

## Summary

Ran 16 trials (8 gNMDA values × 2 modes × 1 trial × 1 direction) at theta = 0 deg with GABA = 0
and AMPA fixed at 0.5 nS as priming on every E synapse, NMDA Mg-block sweep gNMDA in {0.1, 0.5, 1,
2, 5, 10, 15, 20} nS. Wall-clock 269.80 s. Headline: **AMPA priming abolishes the silent regime seen
in t0061** — the cell fires 2-4 spikes at every gNMDA value. Peak spike count **4 at gNMDA = 2.0
nS** (AMPA-NMDA synergy point), plateau of 2-3 spikes at gNMDA in [0.1, 1.0] (AMPA-only-like) and
[5, 20] (AMPA + NMDA plateau).

## Metrics

* **gNMDA = 0.1 / 0.5 / 1.0 nS**: FULL = +15.84 / +15.78 / +15.71 mV, **2 spikes** each;
  EPSP_PASSIVE peak = -52.56 / -51.85 / -49.54 mV. AMPA dominates the response.
* **gNMDA = 2.0 nS (synergy peak)**: FULL = +15.58 mV, **4 spikes**; EPSP_PASSIVE = -33.43 mV. AMPA
  primes, NMDA Mg-block opens, sustained depolarization supports multi-spike train.
* **gNMDA = 5.0 nS**: FULL = +15.28 mV / 2 spikes; EPSP_PASSIVE = -8.54 mV / 1 (false).
* **gNMDA = 10.0 nS**: FULL = +14.92 mV / 3 spikes; EPSP_PASSIVE = -4.65 mV / 1 (false).
* **gNMDA = 15.0 nS**: FULL = +14.71 mV / 3 spikes; EPSP_PASSIVE = -3.36 mV / 1 (false).
* **gNMDA = 20.0 nS**: FULL = +14.56 mV / 3 spikes; EPSP_PASSIVE = -2.70 mV / 1 (false).
* Wall-clock: 269.80 s for 16 trials (~17 s/trial average).

## Verification

* CSVs, JSONs, both PNGs produced.
* HH save-and-zero validated: EPSP_PASSIVE peak Vm always below E_AMPA = 0 mV (max -2.70 mV at gNMDA
  = 20 nS).
* Placement seed = 0 (bit-identical to t0052/t0053/t0057/t0059/t0060/t0061).
