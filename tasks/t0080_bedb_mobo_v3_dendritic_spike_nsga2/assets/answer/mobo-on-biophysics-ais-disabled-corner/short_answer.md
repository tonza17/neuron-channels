---
spec_version: "2"
answer_id: "mobo-on-biophysics-ais-disabled-corner"
answered_by_task: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_answered: "2026-05-04"
---

# MOBO-on-Biophysics AIS-Disabled-Corner Failure Mode

## Question

Why did the t0078 BoTorch qLogNEHVI MOBO collapse `nav16_ais` to the search-space floor (1e-5
S/cm^2) at iter 81, and what biological-prior checklist prevents this failure mode in future
MOBO-on-biophysics tasks?

## Answer

The optimiser exploited a soft-prior loophole. t0078's per-tier search bounds let `nav16_ais` go as
low as 1e-5 S/cm^2, four orders of magnitude below Kole 2008's measured cortical AIS Nav range
[0.25, 0.5] S/cm^2 and five orders below Werginz 2024's mouse alpha-RGC measurement of 1.3 S/cm^2.
Multi-objective acquisition discovered that an AIS-disabled cell could match a fragment of the
Pareto front (DSI 0.316, PD 9.68 Hz at iter 81) at a lower implicit cost than a Kole-compliant cell,
because the prior was advisory rather than enforced. The fix is hard parameter bounds, not soft
penalties: pre-register `nav16_ais >= 0.25` S/cm^2 (Kole 2008) and AIS-to-soma Nav ratio `>= 5`
(Werginz 2024) as inviolable constraints, plus equivalent priors on every biophysical
parameter where measurement-grounded ranges exist.

## Sources

* Paper: `10.1038_nn2040` (Kole 2008 — AIS Nav density patch-clamp)
* Paper: `10.1523_JNEUROSCI.1592-24.2024` (Werginz 2024 — mouse alpha-RGC AIS Nav)
* Paper: `10.1126_sciadv.abb6642` (Werginz 2020 — DSGC AIS context)
* Paper: `10.1371_journal.pcbi.1002107` (Hay 2011 — NaP density priors)
* Task: `t0076_bedb_dsi_firing_rate_mobo`
* Task: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
