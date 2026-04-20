---
spec_version: "2"
answer_id: "patch-clamp-techniques-and-constraints-for-dsgc-modelling"
answered_by_task: "t0017_literature_survey_patch_clamp"
date_answered: "2026-04-20"
---
## Question

What does the patch-clamp / voltage-clamp / space-clamp literature imply for the compartmental
modelling of direction-selective retinal ganglion cells (DSGCs) in NEURON, in particular for (a)
treatment of published Ge/Gi traces as model-fitting targets, (b) inclusion of dendritic
voltage-gated channels and the AIS compartment, (c) synaptic receptor complement including NMDARs,
and (d) modelling of maintained activity and intrinsic pacemaker properties?

## Answer

DSGC compartmental models must (a) treat published somatic voltage-clamp Ge/Gi traces as lower
bounds on distal dendritic conductances rather than ground truth, with up to ~80% signal loss on
thin distal dendrites expected even in passive cables and additional error from active dendritic
channels, so the modelling pipeline must include a somatic voltage-clamp block that mimics the
experiment; (b) include an explicit AIS compartment with Nav1.6 enrichment at approximately 7x the
somatic Na+ density, with AIS length as a named tunable parameter constrained by
immunohistochemistry; (c) include NMDARs with proper Mg2+ block kinetics on DSGC dendrites and fit
to AMPA/NMDA charge ratios during preferred and null motion rather than peak-AMPA-current alone; (d)
decide explicitly whether to include intrinsic-pacemaker biophysics (T-type Ca2+, HCN, subthreshold
oscillations) based on the target DSGC subtype, validated by
maintained-activity-under-synaptic-blockade traces.

## Sources

* Paper: `10.1371_journal.pone.0019463` (Poleg-Polsky & Diamond 2011)
* Paper: `10.1016_j.neuroscience.2021.08.024` (To, Honnuraiah, Stuart 2022)
* Paper: `10.1126_sciadv.abb6642` (Werginz, Raghuram, Fried 2020)
* Paper: `10.1016_j.neuron.2017.09.058` (Sethuramanujam et al. 2017)
* Paper: `10.1523_jneurosci.0130-07.2007` (Margolis & Detwiler 2007)
