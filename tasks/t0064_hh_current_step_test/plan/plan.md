# Plan: t0064 HH Current-Step Diagnostic

## Objective

Test HH model AP firing under IClamp current steps {0.1, 0.2, 0.3, 0.5, 1.0, 2.0} nA for 200 ms each
on soma, no synapses. Compare HH on vs HH off.

## Approach

IClamp(soma(0.5)) with delay=50, dur=200 ms; record Vm and spike times.

## Cost Estimation

$0.00 — local CPU.

## Step by Step

1. Build cell.
2. Loop 6 currents x 2 modes = 12 trials.
3. Write CSVs and PNGs.

## Remote Machines

None.

## Assets Needed

t0059 cell builder, t0009 morphology.

## Expected Assets

None.

## Time Estimation

~60-90 s.

## Risks & Fallbacks

* Very strong currents may drive depolarization block — expected, document in results.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.
