---
spec_version: "2"
answer_id: "dsi-flatness-test-voltage-independent-nmda"
answered_by_task: "t0048_voff_nmda1_dsi_test"
date_answered: "2026-04-25"
---
## Question

Does setting Voff_bipNMDA = 1 (voltage-independent NMDA, the deposited 0 Mg2+ condition) reproduce
Poleg-Polsky and Diamond 2016's claim that DSI vs gNMDA is approximately constant ~0.30 across 0-3
nS?

## Answer

No. Voltage-independent NMDA partially flattens the DSI-vs-gNMDA curve — the 0-3 nS range
collapses from 0.174 (Voff_bipNMDA = 0 baseline) to 0.066, satisfying the H1 range threshold of 0.10
— but the slope test still trends downward at -0.024 per nS, above the 0.02 H1 cutoff and never
within +/- 0.05 of the paper's claimed 0.30. The combined verdict is therefore H2 (flatter than the
deposited control but still not flat at 0.30): the Voff = 1 curve runs at 0.04-0.10 across the
entire range, not at 0.30. The Voff_bipNMDA = 1 swap by itself does not reproduce the paper's DSI vs
gNMDA claim.

## Sources

* Paper: `10.1016_j.neuron.2016.02.013` (Poleg-Polsky and Diamond 2016, Neuron Fig 3F)
* Task: `t0046_reproduce_poleg_polsky_2016_exact` (library asset, deposited code audit)
* Task: `t0047_validate_pp16_fig3_cond_noise` (Voff = 0 baseline DSI sweep)
