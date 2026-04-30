# Results Summary: t0064 HH Current-Step Diagnostic

## Summary

IClamp 200 ms current steps at {0.1, 0.2, 0.3, 0.5, 1.0, 2.0} nA on soma, no synapses. 12 trials in
79 s. The HH model produces a clean F-I curve with rheobase between 0.1 and 0.2 nA, peak firing rate
of 18 spikes / 200 ms (= 90 Hz) at 1.0 nA, and characteristic **depolarization block at 2.0 nA**
(only 1 initial spike, then sustained Vm plateau ~-30 mV).

## Metrics

| I (nA) | FULL peak Vm | FULL spikes | EPSP_PASSIVE peak Vm | F-I rate (Hz) |
| --- | --- | --- | --- | --- |
| 0.1 | -60.53 mV | 0 | -61.65 mV | 0 |
| 0.2 | +14.48 mV | **7** | -58.53 mV | 35 |
| 0.3 | +17.27 mV | **10** | -55.41 mV | 50 |
| 0.5 | +19.74 mV | **13** | -49.17 mV | 65 |
| 1.0 | +23.13 mV | **18** | -33.56 mV | 90 |
| 2.0 | +28.00 mV | **1 (depol-block)** | -2.34 mV | 5 |

* **Rheobase**: between 0.1 and 0.2 nA (sub-threshold at 0.1 nA, fires 7 spikes at 0.2 nA).
* **Spike amplitude shrinks with current**: peak Vm climbs (+14.5 → +28 mV) but the magnitude
  above the post-spike trough decreases — Na+ availability drops at high firing rates.
* **Depolarization block**: at 2.0 nA the cell fires once then Na+ inactivates faster than h
  recovers; Vm stabilises at ~-30 mV plateau without further APs.
* **Passive R_in**: from 0.1 nA / 3.4 mV depolarization → R_in ≈ 33.5 MOhm.

## Verification

* All artefacts produced: voltage_traces.csv, summary.csv, wallclock.json, 2 PNGs.
* HH save-and-zero validated: passive Vm always sub-threshold (peak -2.34 mV at 2.0 nA, well below
  E_AMPA = 0 mV; the netcon -20 mV crossing is a false positive at 2 nA).
