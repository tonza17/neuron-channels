---
spec_version: "2"
answer_id: "seclamp-conductance-remeasurement-fig3"
answered_by_task: "t0049_seclamp_cond_remeasure"
date_answered: "2026-04-25"
---
# SEClamp re-measurement of Fig 3A-E conductances

## Question

Does measuring per-channel synaptic conductance under a somatic SEClamp on the deposited DSGC
reproduce Poleg-Polsky 2016 Fig 3A-E values within +/- 25%, and resolve the t0047 amplitude mismatch
as a measurement-modality artefact?

## Answer

No. Under somatic SEClamp at -65 mV on the deposited DSGC at gNMDA = 0.5 nS, all six channel x
direction cells render an H2 verdict: SEClamp values are 1.6x-3.8x the paper Fig 3A-E targets and
0.2x-0.5x t0047's per-synapse-summed values, so they sit between the two references but match
neither within tolerance. Modality (somatic clamp vs per-synapse direct) explains roughly an order
of magnitude of the t0047 amplitude mismatch but does not fully close the gap to the paper. The
deposited model also fails to reproduce the paper's headline GABA PD/ND asymmetry (SEClamp DSI ~ 0
vs paper ~ -0.4), which points to genuine parameter or protocol differences beyond measurement
modality.

## Sources

* Task: `t0046_reproduce_poleg_polsky_2016_exact`
* Task: `t0047_validate_pp16_fig3_cond_noise`
