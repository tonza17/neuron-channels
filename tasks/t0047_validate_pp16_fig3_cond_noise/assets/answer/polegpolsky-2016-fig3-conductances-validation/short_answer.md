---
spec_version: "2"
answer_id: "polegpolsky-2016-fig3-conductances-validation"
answered_by_task: "t0047_validate_pp16_fig3_cond_noise"
date_answered: "2026-04-25"
---
## Question

Does the deposited ModelDB 189347 code reproduce Poleg-Polsky 2016's Fig 3A-F per-synapse
conductance balance and DSI-vs-gNMDA flatness, and does the extended noise sweep match the paper's
qualitative shape?

## Answer

No. Every per-synapse-class summed peak conductance at the code-pinned gNMDA = 0.5 nS is 6-9x the
paper's Fig 3A-E target on the summed scale and well below it on the per-synapse-mean scale, so
neither interpretation reconciles. DSI as a function of gNMDA peaks at 0.19 near b2gnmda = 0.5 nS
and decays toward zero by 3.0 nS, never crossing the paper's claimed flat ~0.30 band. The extended
noise sweep shows DSI declining qualitatively as flickerVAR rises in the control and 0Mg conditions
but the trend is weaker than the paper reports, and the ROC AUC metric saturates at 1.0 across every
cell because PSP peaks dwarf baselines on this circuit.

## Sources

* Paper: `10.1016_j.neuron.2016.02.013` (Poleg-Polsky and Diamond 2016, Neuron Fig 3A-F)
* Task: `t0046_reproduce_poleg_polsky_2016_exact` (library asset, prior reproduction audit)
