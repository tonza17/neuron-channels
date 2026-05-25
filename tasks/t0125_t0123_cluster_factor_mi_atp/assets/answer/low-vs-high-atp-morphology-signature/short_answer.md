---
spec_version: "2"
answer_id: "low-vs-high-atp-morphology-signature"
answered_by_task: "t0125_t0123_cluster_factor_mi_atp"
date_answered: "2026-05-25"
---
## Question

Which morphology parameters most distinguish low-ATP from high-ATP cells in the t0123 spiking
cohort, and does the low-ATP group spend relatively more ATP at the AIS than in the dendrites?

## Answer

The top 5 morphology parameters by |Cliff's delta| separating high-ATP (top quartile of
atp_per_spike, n = 782) from low-ATP (bottom quartile, n = 782) cells are: mean_segment_length_um
(delta = -0.725, low-ATP cells have ~43% longer segments), branch_length_cv (delta = +0.554, low-ATP
cells are more uniform in branch length), branch_density_gradient_pd (delta = +0.504, low-ATP cells
have weaker preferred-direction dendrite-density gradient), field_elongation_pd (delta = -0.469,
low-ATP cells have more elongated dendritic field), and ais_length_um (delta = +0.376, low-ATP cells
have shorter AIS by ~12%). The ATP-share answer is Yes for the AIS but the dendrite/soma swap
dominates: low-ATP cells concentrate 93% of per-AP ATP at the soma and 6% at the AIS with only 0.4%
in dendrites, while high-ATP cells push 62% into dendrites and 35% into soma with only 2.6% at the
AIS.

## Sources

* Task: `t0125_t0123_cluster_factor_mi_atp`
* Task: `t0123_bedb_mi_atp_per_spike_nsga2`
* Paper: `10.1038_382363a0`
* Paper: `10.1371_journal.pcbi.1000877`
* Paper: `10.1097_00004647-200110000-00001`
* Paper: `10.1371_journal.pcbi.1000840`
