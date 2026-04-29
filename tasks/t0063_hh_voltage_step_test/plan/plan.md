# Plan: t0063 HH Voltage-Step Diagnostic

## Objective

Test the HH model by stepping the soma to {-60, -50, -40, -30, -20, -10} mV for 200 ms via SEClamp,
no synapses. Compare HH on vs HH off to isolate the HH-driven currents.

## Approach

SEClamp on soma(0.5) with dur1+dur2+dur3 protocol, record Vm and clamp current, plot FULL vs
EPSP_PASSIVE and the difference (FULL - PASSIVE = pure HH).

## Cost Estimation

$0.00 — local CPU only.

## Step by Step

1. Build cell (no synapses).
2. Loop 6 targets x 2 modes (FULL/EPSP_PASSIVE) = 12 trials with SEClamp protocol.
3. Write CSVs and 2 PNGs.

## Remote Machines

None.

## Assets Needed

t0059 cell builder, t0009 morphology.

## Expected Assets

None.

## Time Estimation

~30-60 s for 12 trials.

## Risks & Fallbacks

* SEClamp capacitive transients dominate raw clamp current plots — handle by zooming y-axis to
  steady-state region.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.
