---
spec_version: "2"
answer_id: "vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation"
answered_by_task: "t0033_plan_dsgc_morphology_channel_optimisation"
date_answered: "2026-04-22"
---
## Question

What is the Vast.ai GPU cost and recommended organisation of a joint DSGC morphology + top-10
voltage-gated channel DSI-maximisation task?

## Answer

Run a surrogate-NN-assisted gradient-free evolutionary search (population 150 x 30 generations x 3
seeds after a 5,000-sample surrogate-training burn-in, 25 free parameters = 5 Cuntz morphology
scalars + 20 channel gbar parameters) on a single RTX 4090 Vast.ai instance at a central USD cost of
about 51 dollars, with a 0.5x-2x sensitivity envelope of roughly 23-119 dollars. This combination is
cheapest among the corpus-justified gradient-free strategies because the surrogate-NN cuts 18,500
evaluations to ~8 GPU-hours of surrogate inference plus a one-off ~83 GPU-hour CoreNEURON training
burn at the RTX 4090 rate of 0.50 dollars/hour. Confidence is medium: the CoreNEURON CPU-to-GPU
speedup and the surrogate-NN economics are external assumptions not quantified in the downloaded
paper corpus, and the sensitivity grid is propagated across a 0.5x-2x band for both per-sim cost and
sample count.

## Sources

* Task: `t0019_literature_survey_voltage_gated_channels`
* Task: `t0022_modify_dsgc_channel_testbed`
* Task: `t0024_port_de_rosenroll_2026_dsgc`
* Task: `t0026_vrest_sweep_tuning_curves_dsgc`
* Task: `t0027_literature_survey_morphology_ds_modeling`
* Paper: `10.1038_s41467-026-70288-4` (Poleg-Polsky 2026)
* Paper: `10.1371_journal.pcbi.1009754` (Ezra-Tsur 2021)
* Paper: `10.1371_journal.pcbi.1000877` (Cuntz 2010)
