---
spec_version: "2"
answer_id: "dsgc-bits-per-atp-vs-niven-2007"
answered_by_task: "t0123_bedb_mi_atp_per_spike_nsga2"
date_answered: "2026-05-24"
---
## Question

Where does the DSGC bits-per-ATP front sit relative to Niven 2007's fly-photoreceptor curve, and
does it match the Niven super-linear cost-vs-information scaling?

## Answer

Insufficient evidence. The t0123 single-seed NSGA-II run produced 10 top-Pareto cells under the
post-hoc Strong-Bialek 1998 direct method; the log-log fit exponent p = n/a at r^2 = n/a is too
noisy (n < 10 or r^2 < 0.5) to make a definitive statement about super-linear scaling.

## Sources

* Paper: `10.1103_PhysRevLett.80.197` (Strong et al. 1998)
* External: Niven et al. 2007 (https://doi.org/10.1242/jeb.005249)
* Task: `t0123_bedb_mi_atp_per_spike_nsga2`
* Predictions asset:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph`
* Chart: `tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/niven_2007_comparison.png`
* Chart: `tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/carter_bean_atp_per_ap_check.png`
