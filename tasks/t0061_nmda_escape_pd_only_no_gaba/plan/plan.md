# Plan: t0061 NMDA-Only PD Diagnostic

## Objective

NMDA-only analog of t0060: GABA = 0, AMPA = 0, theta = 0 deg, sweep gNMDA in {0.1, 0.5, 1, 2, 5, 10,
15, 20} nS, record soma V(t) in FULL (HH on) and EPSP_PASSIVE (HH off).

## Approach

Reuse t0059's library for cell + placement; copy NMDA_MgBlock.mod from t0055; build NMDA-only
synapses; loop 16 trials.

## Cost Estimation

$0.00 — local CPU only.

## Step by Step

1. Build cell, sample placement (seed 0), build NMDA-only synapses.
2. Loop 8 gNMDA × 2 modes × 1 trial = 16 trials at theta=0.
3. Write CSVs and PNGs.

## Remote Machines

None.

## Assets Needed

t0055 NMDA_MgBlock.mod (copied), t0059 library (imported), t0009 morphology (read).

## Expected Assets

None.

## Time Estimation

~2-3 minutes for 16 trials.

## Risks & Fallbacks

* Mg block at V_rest = -65 mV may keep cell silent at low gNMDA — acceptable, that's the finding.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.
