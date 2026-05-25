---
spec_version: "2"
answer_id: "high-vs-low-mi-electrophys-signature"
answered_by_task: "t0125_t0123_cluster_factor_mi_atp"
date_answered: "2026-05-25"
---
## Question

Which electrophys parameters most distinguish high-MI from low-MI cells in the t0123 spiking cohort,
with effect size and direction?

## Answer

The top 5 electrophys parameters by |Cliff's delta| separating high-MI (top quartile of
mi_count_bits, n = 819) from low-MI (bottom quartile, n = 1024) cells are: IH_GBAR (delta = -0.786,
high-MI cells have ~32x lower mean), CAD_TAUR_MS (delta = -0.717, high-MI cells have ~3.6x faster
calcium-buffer time constant), KDR_GBAR (delta = -0.668, high-MI cells have ~9x lower mean),
SK_AIS_GBAR (delta = +0.632, high-MI cells have higher AIS-localised SK density), and
SKAHP_TAU_CA_MULTIPLIER (delta = -0.627, high-MI cells have ~2.4x shorter calcium-driven AHP time
constant). All five Mann-Whitney U p-values are below 1e-115, so the effects are statistically
robust against the n ~ 1000 sample sizes.

## Sources

* Task: `t0125_t0123_cluster_factor_mi_atp`
* Task: `t0123_bedb_mi_atp_per_spike_nsga2`
* Paper: `10.1371_journal.pcbi.1000840`
* Paper: `10.1523_jneurosci.5346-03.2004`
* Paper: `10.1152_jn.1997.78.4.1948`
