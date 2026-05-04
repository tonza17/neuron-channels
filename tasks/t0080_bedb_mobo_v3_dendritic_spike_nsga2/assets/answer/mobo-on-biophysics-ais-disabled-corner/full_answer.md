---
spec_version: "2"
answer_id: "mobo-on-biophysics-ais-disabled-corner"
answered_by_task: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
date_answered: "2026-05-04"
confidence: "high"
---

# MOBO-on-Biophysics AIS-Disabled-Corner Failure Mode

## Question

Why did the t0078 BoTorch qLogNEHVI MOBO collapse `nav16_ais` to the search-space floor (1e-5
S/cm^2) at iter 81, and what biological-prior checklist prevents this failure mode in future
MOBO-on-biophysics tasks?

## Short Answer

The optimiser exploited a soft-prior loophole. t0078's per-tier search bounds let `nav16_ais` go as
low as 1e-5 S/cm^2, four orders of magnitude below Kole 2008's measured cortical AIS Nav range
[0.25, 0.5] S/cm^2 and five orders below Werginz 2024's mouse alpha-RGC measurement of 1.3 S/cm^2.
Multi-objective acquisition discovered that an AIS-disabled cell could match a fragment of the
Pareto front (DSI 0.316, PD 9.68 Hz at iter 81) at a lower implicit cost than a Kole-compliant cell,
because the prior was advisory rather than enforced. The fix is hard parameter bounds, not soft
penalties: pre-register `nav16_ais >= 0.25` S/cm^2 (Kole 2008) and AIS-to-soma Nav ratio `>= 5`
(Werginz 2024) as inviolable constraints, plus equivalent priors on every biophysical parameter
where measurement-grounded ranges exist.

## Research Process

The investigation proceeded in three stages: (1) post-mortem audit of the t0078 Pareto front in
`tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/data/pareto_front.json`, identifying iter 81 as
the canonical failure cell where `nav16_ais` had collapsed to the search-space floor; (2)
literature anchoring with Kole 2008 [Kole2008] cortical AIS Nav patch-clamp measurements and
Werginz 2024 [Werginz2024] mouse alpha-RGC AIS-to-soma ratio; (3) algorithm-design review of the
t0078 BoTorch qLogNEHVI configuration to verify that the Pareto-tracking acquisition function was
behaving as designed (it was), so the failure was a search-space specification bug, not an
acquisition bug. The biological-prior checklist was synthesised from Kole 2008, Werginz 2024,
Werginz 2020 [Werginz2020], Hay 2011 [Hay2011], and the Sivyer 2013 / Schachter 2010 / Oesch 2005
DSGC dendritic-spike literature reviewed during t0078 and t0080.

## Evidence from Papers

Kole 2008 [Kole2008] reports patch-clamp AIS Nav densities of 0.25-0.5 S/cm^2 in cortical
pyramidal neurons; the lower edge 0.25 S/cm^2 is the empirically grounded lower bound for any AIS
Nav prior. Werginz 2024 [Werginz2024] reports mouse alpha-RGC AIS-to-soma Nav density ratios with a
measured value of 17.3, far above any plausible "AIS-disabled" cell. Werginz 2020 [Werginz2020]
provides DSGC AIS context (DSGCs are not alpha-RGCs but share the high-density AIS architecture).
Hay 2011 [Hay2011] caps somatic NaP at biologically realistic densities, providing the upper bound
adapted as `nap_dend_distal <= 0.01` S/cm^2 in t0080's distal-dendrite parameterisation. Together
these establish that any cell with AIS Nav below the Kole 2008 lower bound, or AIS-to-soma ratio
below 5, is outside the empirical envelope and must be excluded by hard constraint, not penalised
softly.

## Evidence from Internet Sources

Internet research was not used as a primary method for this answer; the literature evidence base
was drawn entirely from the paper assets above and the prior-task results below.

## Evidence from Code or Experiments

The t0076 [t0076] (25-d MOBO, no AIS) and t0078 [t0078] (49-d MOBO with AIS) Pareto fronts were
audited row-by-row for biophysical-prior collapse patterns. t0078 iter 81 was found at
`nav16_ais = 1e-5` S/cm^2, the lowest possible value within the search bounds, indicating the
optimiser had bumped against the floor rather than landed inside the Kole 2008 prior. Two
additional iterations exhibited milder versions of the same pattern (iter 117, iter 142). The
t0076 audit found no equivalent collapses because t0076 lacked an AIS — every t0076 cell was an
AIS-absent cell by construction, so there was no "AIS-disabled corner" to find. This rules out the
hypothesis that the failure mode is intrinsic to MOBO; it is a soft-prior exploitation that
emerges only when the search space is wider than the biological envelope. t0080 [t0080] is the
methodological control: with hard lower bound `nav16_ais >= 0.25` S/cm^2 enforced through
`LOWER_BOUNDS` and AIS-to-soma ratio `>= 5` enforced through pymoo `n_ieq_constr=1`, NSGA-II's
constraint handling guarantees no Pareto cell ever has the t0078-iter-81 collapse pattern.

## Synthesis

The t0078 iter-81 collapse is a generalisable MOBO-on-biophysics failure mode: any soft prior on a
biological parameter is, in expectation, exploited by a sufficiently powerful multi-objective
acquisition function whenever violating the prior reduces the implicit cost of a competing
objective. The remedy is not better acquisition design or higher-quality priors; it is to convert
every measurement-grounded prior into a hard constraint at the search-space level. The
biological-prior checklist for MOBO-on-biophysics tasks is therefore: (1) Kole 2008 lower bound
(0.25 S/cm^2) on AIS Nav density; (2) Werginz 2024 AIS-to-soma Nav ratio floor (>= 5, well below
the measured 17.3); (3) Hay 2011 NaP density cap; (4) Schachter 2010 / Sivyer 2013 dendritic Nav
range; (5) Jahr-Stevens NMDA Mg-block convention. Each is encoded as either a hard parameter bound
or a hard inequality constraint depending on whether the rule applies per-parameter or
between-parameters. The checklist is transferable: any future MOBO task on a biophysical
substrate should pre-register equivalent hard constraints from the substrate's measurement
literature before launching the loop.

## Limitations

The 5x AIS-to-soma Nav ratio floor is inferred from non-DSGC patch-clamp (Werginz 2024 measured
mouse alpha-RGCs, not the DRD4 ON-OFF DSGCs simulated here); a stricter ratio prior may apply to
DSGCs once direct measurements appear. The Kole 2008 lower bound 0.25 S/cm^2 is from cortical
pyramidal neurons; mammalian RGCs may have a slightly different lower edge but cannot plausibly be
five orders of magnitude lower. The checklist does not yet cover dendritic-spike-machinery priors
beyond the bounds adopted in t0080 (Sivyer 2013 / Oesch 2005 are qualitative); future
MOBO-on-biophysics tasks introducing new conductances should add hard bounds when measurement
ranges become available.

## Sources

* Paper: `10.1038_nn2040` (Kole 2008)
* Paper: `10.1523_JNEUROSCI.1592-24.2024` (Werginz 2024)
* Paper: `10.1126_sciadv.abb6642` (Werginz 2020)
* Paper: `10.1371_journal.pcbi.1002107` (Hay 2011)
* Task: `t0076_bedb_dsi_firing_rate_mobo`
* Task: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`

[Kole2008]: ../../../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1038_nn2040/summary.md
[Werginz2024]: ../../../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/summary.md
[Werginz2020]: ../../../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1126_sciadv.abb6642/summary.md
[Hay2011]: ../../../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[t0076]: ../../../../t0076_bedb_dsi_firing_rate_mobo/
[t0078]: ../../../../t0078_bedb_mobo_v2_ais_tiered_ahp/
[t0080]: ../../../../t0080_bedb_mobo_v3_dendritic_spike_nsga2/
