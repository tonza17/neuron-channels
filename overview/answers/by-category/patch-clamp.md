# Answers: `patch-clamp` (2)

2 answer(s).

[Back to all answers](../README.md)

---

<details>
<summary><strong>What does the patch-clamp / voltage-clamp / space-clamp literature
imply for the compartmental modelling of direction-selective retinal
ganglion cells (DSGCs) in NEURON, in particular for (a) treatment of
published Ge/Gi traces as model-fitting targets, (b) inclusion of dendritic
voltage-gated channels and the AIS compartment, (c) synaptic receptor
complement including NMDARs, and (d) modelling of maintained activity and
intrinsic pacemaker properties?</strong></summary>

**Confidence**: medium

DSGC compartmental models must treat published somatic voltage-clamp Ge/Gi traces as lower
bounds on distal dendritic conductances rather than ground truth, because up to ~80% of the
synaptic signal is lost on thin distal dendrites even in passive cables and active dendritic
channels add further error. The modelling pipeline therefore needs a simulated somatic
voltage-clamp block that mimics the experimental amplifier so simulation and experiment are
compared on the same footing. The model must include an explicit AIS compartment with Nav1.6
enrichment at approximately 7x the somatic Na+ density, with AIS length as a named tunable
parameter constrained by immunohistochemistry, and NMDARs with standard Mg2+ block kinetics on
DSGC dendrites, fit to AMPA/NMDA charge ratios during preferred and null motion rather than
peak-AMPA-current alone. Finally the modeller must decide explicitly whether to include
intrinsic-pacemaker biophysics (T-type Ca2+, HCN, subthreshold oscillations) based on the
target DSGC subtype, validated by maintained-activity-under-synaptic-blockade traces.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/answer/patch-clamp-techniques-and-constraints-for-dsgc-modelling/full_answer.md) |
| **ID** | [`patch-clamp-techniques-and-constraints-for-dsgc-modelling`](../../../tasks/t0017_literature_survey_patch_clamp/assets/answer/patch-clamp-techniques-and-constraints-for-dsgc-modelling/) |
| **Question** | What does the patch-clamp / voltage-clamp / space-clamp literature imply for the compartmental modelling of direction-selective retinal ganglion cells (DSGCs) in NEURON, in particular for (a) treatment of published Ge/Gi traces as model-fitting targets, (b) inclusion of dendritic voltage-gated channels and the AIS compartment, (c) synaptic receptor complement including NMDARs, and (d) modelling of maintained activity and intrinsic pacemaker properties? |
| **Methods** | `papers` |
| **Confidence** | medium |
| **Date created** | 2026-04-20 |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Paper sources** | `10.1371_journal.pone.0019463`, `10.1016_j.neuroscience.2021.08.024`, `10.1126_sciadv.abb6642`, `10.1016_j.neuron.2017.09.058`, `10.1523_jneurosci.0130-07.2007` |
| **Task sources** | — |
| **URL sources** | — |
| **Created by** | [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |

</details>

<details>
<summary><strong>What quantitative priors does the voltage-gated-channels literature
supply for the DSGC compartmental model on (1) Nav subunit localisation at
the RGC AIS, (2) Kv1 subunit expression at the AIS, (3) RGC HH-family
kinetic rate functions, (4) Nav1.6 vs Nav1.2 subunit co-expression
kinetics, and (5) Nav conductance density at the AIS?</strong></summary>

**Confidence**: medium

RGC AIS Nav subunits segregate into microdomains with Nav1.6 concentrated distally and Nav1.2
enriched proximally, and Kv1.1/Kv1.2 co-localising with Nav1.6 in the distal AIS.
AIS-localised Kv1 channels activate near threshold (V_half around -40 to -50 mV) with
sub-millisecond kinetics and control AP waveform and somatic repolarisation. The
Fohlmeister-Miller RGC HH kinetics provide canonical alpha/beta rate functions for Nav and Kv
at 22 degC with Nav activation V_half near -40 mV and a Q10 near 3 for warming to 37 degC.
Nav1.6 activates about 10-15 mV more negative than Nav1.2, so distal Nav1.6 initiates the AP
while proximal Nav1.2 supports backpropagation into the soma. Peak AIS Nav conductance density
is about 2500-5000 pS/um2 (roughly 50x somatic density), an order-of-magnitude prior essential
for reproducing fast, reliable AP initiation in compartmental models.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/full_answer.md) |
| **ID** | [`nav-kv-combinations-for-dsgc-modelling`](../../../tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/) |
| **Question** | What quantitative priors does the voltage-gated-channels literature supply for the DSGC compartmental model on (1) Nav subunit localisation at the RGC AIS, (2) Kv1 subunit expression at the AIS, (3) RGC HH-family kinetic rate functions, (4) Nav1.6 vs Nav1.2 subunit co-expression kinetics, and (5) Nav conductance density at the AIS? |
| **Methods** | `papers` |
| **Confidence** | medium |
| **Date created** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Paper sources** | `10.1002_cne.21173`, `10.1016_j.neuron.2007.07.031`, `10.1152_jn.1997.78.4.1948`, `10.1038_nn.2359`, `10.1038_nn2040` |
| **Task sources** | — |
| **URL sources** | — |
| **Created by** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |

</details>
