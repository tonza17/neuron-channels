---
spec_version: "2"
answer_id: "does-rd1-like-na-k-remodelling-of-the-dsgc-model-reproduce-the-rd1-phenotype-and-change-dsi"
answered_by_task: "t0131_rd1_na_k_remodelling_dsgc_dsi"
date_answered: "2026-10-27"
---
# Does rd1-like Na/K remodelling of the DSGC model reproduce the rd1 phenotype and change DSI?

## Question

Does rd1-like remodelling of soma and AIS Na and K conductances in the Bed B DSGC model reproduce
the researcher's rd1 phenotype (panels A to C), and what does it do to signed direction selectivity
and to the panel D toy-model predictions?

## Answer

No, only the clamp-current ratio is reproduced: the sustained-current ratio reaches 1.63 to 1.70 on
all 8 reference cells, but only at the grid edges (s_Na 0.25, s_K 2.36 to 3.0), and the Na transient
falls to 0.40 to 0.57 of WT-like instead of 0.25. The WT-like reference cells fire spontaneously at
a median of 73.5 Hz without any input, so panels A and B cannot be tested as intended. The rd1-like
cells are silent in every current-clamp, bias and synaptic protocol (dendritic arm included), signed
DSI is therefore undefined for rd1-like cells, and all four panel D predictions are disproved in the
NEURON model, whereas the toy model matches its by-eye anchors by construction. This rests on local
NEURON experiments on 8 LEGIT cells (exploratory, with by-eye targets).

## Sources

* Task: `t0131_rd1_na_k_remodelling_dsgc_dsi` (data in `data/`, summary in
  `results/data_summary.json`)
* Task: `t0121_5seed_substrate_rate_canonical_report`
* Task: `t0129_t0126_signed_dsi_real_rates_1seed`
* Paper: `10.1523_JNEUROSCI.1592-24.2024`
* Paper: `10.1101_2020.09.15.297937`
* Paper: `10.1016_j.neuron.2005.06.036`
