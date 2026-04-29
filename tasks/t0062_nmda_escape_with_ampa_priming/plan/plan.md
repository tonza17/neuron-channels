# Plan: t0062 NMDA + AMPA-Priming PD Diagnostic

## Objective

t0061 with AMPA fixed at 0.5 nS as priming on every E synapse, sweep gNMDA in {0.1, 0.5, 1, 2, 5,
10, 15, 20} nS at FULL and EPSP_PASSIVE.

## Approach

Reuse t0059's library + t0055's NMDA_MgBlock.mod. Co-located AMPA + NMDA on each location with
shared NetStim.

## Cost Estimation

$0.00 — local CPU only.

## Step by Step

1. Build cell, sample placement (seed 0), build co-located AMPA + NMDA pairs.
2. Loop 8 gNMDA × 2 modes × 1 trial = 16 trials at theta=0, AMPA=0.5 nS.
3. Write CSVs and PNGs.

## Remote Machines

None.

## Assets Needed

t0055 NMDA_MgBlock.mod, t0059 library, t0009 morphology.

## Expected Assets

None.

## Time Estimation

~3-5 min for 16 trials.

## Risks & Fallbacks

* Sodium-channel saturation may cap spike count at high gNMDA.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.
