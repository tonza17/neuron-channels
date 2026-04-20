# Answers: `direction-selectivity` (7)

7 answer(s).

[Back to all answers](../README.md)

---

<details>
<summary><strong>Can ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC)
be reproduced locally on Windows as a headless library, does it hit the
published direction-selectivity envelope with a canonical 12-angle x
20-trial drifting-bar protocol, and which sibling DSGC compartmental models
are the next-best candidates for porting in the same pipeline?</strong></summary>

**Confidence**: medium

Yes, ModelDB 189347 was ported and runs headless on Windows 11 with NEURON 8.2.7 via a Python
driver that sources the verbatim HOC and MOD files through `h.load_file`/`h.nrn_load_dll`; a
12-angle x 20-trial sweep on the bundled morphology completed end-to-end in roughly 10 minutes
and the four registered metrics (DSI, HWHM, reliability, RMSE vs target) were written to
`results/metrics.json`. The tuning curve does not hit the published envelope at the bundled
parameters (peak well below 40 Hz, DSI well below 0.7), because the paper derives DS from a
`gabaMOD` parameter swap rather than from spatial rotation — the port's rotation-based
protocol is only a proxy for a direction- selective stimulus. The Hanson et al. 2019
Spatial-Offset-DSGC model (GitHub `geoffder/Spatial-Offset-DSGC-NEURON-Model`) is the
next-best port candidate: it shares `RGCmodel.hoc` and `HHst.mod` with 189347 and already
ships a Python driver; Jain 2020 is medium-effort; Ding 2016, Schachter 2010, Koren 2017, and
Ezra-Tsur 2022 either lack a public compartmental model or address a different modelling
class.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report/full_answer.md) |
| **ID** | [`dsgc-modeldb-port-reproduction-report`](../../../tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report/) |
| **Question** | Can ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC) be reproduced locally on Windows as a headless library, does it hit the published direction-selectivity envelope with a canonical 12-angle x 20-trial drifting-bar protocol, and which sibling DSGC compartmental models are the next-best candidates for porting in the same pipeline? |
| **Methods** | `code-experiment`, `internet` |
| **Confidence** | medium |
| **Date created** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Paper sources** | — |
| **Task sources** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **URL sources** | [url 1](https://modeldb.science/189347), [url 2](https://github.com/ModelDBRepository/189347), [url 3](https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model), [url 4](https://elifesciences.org/articles/42392v1) |
| **Created by** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |

</details>

<details>
<summary><strong>How does the existing peer-reviewed literature on compartmental
models of direction-selective retinal ganglion cells structure the five
project research questions (Na/K conductances, morphology sensitivity,
AMPA/GABA balance, active vs passive dendrites, and angle-to-AP-frequency
tuning curves), and what quantitative targets does it provide?</strong></summary>

**Confidence**: medium

The literature structures the five questions around a small set of quantitative targets that
the project must hit. For Na/K conductances the Fohlmeister-Miller parameter set (peak somatic
g_Na around 0.04-0.10 S/cm^2, delayed-rectifier g_K around 0.012 S/cm^2) is the standard
starting point, and no published paper reports a factorial (g_Na, g_K) grid for DSGCs. For
morphology the asymmetric ON-OFF DSGC dendrite is sharply wired in the null direction through
SAC-mediated inhibition, yet global dendrite shape only minimally changes the synaptic map
while local electrotonic compartments still matter. For AMPA/GABA balance the canonical counts
on a reconstructed mouse DSGC are 177 AMPA and 177 GABA synapses, with null-direction
inhibition running three to five times larger than preferred inhibition. Active dendrites with
Fohlmeister-like channel densities roughly double the direction-selectivity index versus
passive trees, and the target mouse ON-OFF DSGC tuning curve should hit DSI 0.7-0.85,
preferred peak 40-80 Hz, null residual under 10 Hz, and a half-width of 60-90 degrees.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/full_answer.md) |
| **ID** | [`how-does-dsgc-literature-structure-the-five-research-questions`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/) |
| **Question** | How does the existing peer-reviewed literature on compartmental models of direction-selective retinal ganglion cells structure the five project research questions (Na/K conductances, morphology sensitivity, AMPA/GABA balance, active vs passive dendrites, and angle-to-AP-frequency tuning curves), and what quantitative targets does it provide? |
| **Methods** | `papers`, `internet` |
| **Confidence** | medium |
| **Date created** | 2026-04-18 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Paper sources** | `10.1113_jphysiol.1965.sp007638`, `10.1162_neco.1997.9.6.1179`, `10.1038_nrn3165`, `10.1016_j.neuron.2016.02.013`, `10.1016_j.neuron.2005.06.036`, `10.1126_science.1189664`, `10.1371_journal.pcbi.1000899`, `10.1152_jn.00123.2009`, `10.1523_JNEUROSCI.22-17-07712.2002`, `10.1113_jphysiol.2008.161240`, `10.1523_JNEUROSCI.5017-13.2014`, `10.1038_nature09818`, `10.1038_nature18609`, `10.1113_jphysiol.2010.192716`, `10.1002_cne.22678`, `10.1016_j.neuron.2017.07.020`, `10.1523_ENEURO.0261-21.2021`, `10.7554_eLife.52949`, `10.7554_eLife.42392`, `10.1016_j.neuron.2016.04.041` |
| **Task sources** | — |
| **URL sources** | — |
| **Created by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |

</details>

<details>
<summary><strong>What does the classical cable-theory and dendritic-computation
literature imply for the compartmental modelling of direction-selective
retinal ganglion cells (DSGCs) in NEURON?</strong></summary>

**Confidence**: medium

DSGC compartmental models in NEURON must use morphologically accurate reconstructions (not
ball- and-stick), discretized with the `d_lambda` rule, and must implement direction
selectivity via postsynaptic dendritic shunting inhibition rather than presynaptic wiring
asymmetry. The DS computation must arise from asymmetric inhibitory input acting locally on
dendritic branches via the Koch-Poggio-Torre on-the-path shunting mechanism, and the model
must be validated by measuring EPSP shape-indices, losing DS under simulated inhibition block,
and reproducing the graded-vs- spike contrast-sensitivity trade-off.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0015_literature_survey_cable_theory/assets/answer/cable-theory-implications-for-dsgc-modelling/full_answer.md) |
| **ID** | [`cable-theory-implications-for-dsgc-modelling`](../../../tasks/t0015_literature_survey_cable_theory/assets/answer/cable-theory-implications-for-dsgc-modelling/) |
| **Question** | What does the classical cable-theory and dendritic-computation literature imply for the compartmental modelling of direction-selective retinal ganglion cells (DSGCs) in NEURON? |
| **Methods** | `papers` |
| **Confidence** | medium |
| **Date created** | 2026-04-20 |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cells`](../../../meta/categories/retinal-ganglion-cells/), [`compartmental-modelling`](../../../meta/categories/compartmental-modelling/) |
| **Paper sources** | `10.1152_jn.1967.30.5.1138`, `10.1098_rstb.1982.0084`, `10.1038_382363a0`, `10.1126_science.289.5488.2347`, `10.1523_jneurosci.5346-03.2004` |
| **Task sources** | — |
| **URL sources** | — |
| **Created by** | [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |

</details>

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
<summary><strong>What DSGC compartmental models published in public literature were
missed by tasks t0002 and t0008, and which of them are viable ports for
this project?</strong></summary>

**Confidence**: medium

Two brand-new DSGC compartmental-model papers were missed by the prior corpus: deRosenroll et
al. 2026 (Cell Reports, DOI `10.1016/j.celrep.2025.116833`) and Poleg-Polsky 2026 (Nature
Communications, DOI `10.1038/s41467-026-70288-4`); Hanson 2019 (`10.7554/eLife.42392`) was in
the t0002 corpus but had never been ported. None of the three HIGH-priority candidates
completed a 12-angle canonical sweep within the 90-minute-per-candidate port budget — each
failed at the P2 upstream-demo gate for a different structural reason (Hanson: headfull Python
driver with hardcoded Windows paths; deRosenroll: hardcoded 8-direction stimulus grid plus
heavy out-of-env dependencies; Poleg-Polsky: genetic-algorithm training driver with `numDir=2`
and no LICENSE). Zero library assets were registered per the "never leave a broken library
behind" rule, and all three candidates are recorded as `p2_failed` in `data/candidates.csv`.
Deeper investment (hand-rewriting each driver) would very plausibly succeed; the 90-minute cap
is the binding constraint, not a definitive portability verdict.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/answer/dsgc-missed-models-survey/full_answer.md) |
| **ID** | [`dsgc-missed-models-survey`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/answer/dsgc-missed-models-survey/) |
| **Question** | What DSGC compartmental models published in public literature were missed by tasks t0002 and t0008, and which of them are viable ports for this project? |
| **Methods** | `papers`, `internet`, `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-04-20 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Paper sources** | `10.1016_j.celrep.2025.116833`, `10.1038_s41467-026-70288-4`, `10.7554_eLife.42392` |
| **Task sources** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **URL sources** | [url 1](https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model), [url 2](https://github.com/geoffder/ds-circuit-ei-microarchitecture), [url 3](https://doi.org/10.5281/zenodo.17666157), [url 4](https://github.com/PolegPolskyLab/DS-mechanisms), [url 5](https://modeldb.science/189347), [url 6](https://modeldb.science/267646) |
| **Created by** | [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |

</details>

<details>
<summary><strong>What quantitative priors does the synaptic-integration literature
supply for the DSGC compartmental model on (1) AMPA/NMDA/GABA receptor
kinetics, (2) shunting inhibition, (3) E-I balance temporal co-tuning, (4)
dendritic-location-dependent PSP integration, and (5) SAC-to-DSGC
inhibitory asymmetry?</strong></summary>

**Confidence**: medium

Receptor kinetics: AMPA uses a fast bi-exponential conductance (rise ~0.2 ms, decay ~1-3 ms,
Erev 0 mV); NMDA uses a slow conductance (rise ~5-10 ms, decay ~50-100 ms, Erev 0 mV) with
Jahr-Stevens Mg2+ block; GABA_A uses a fast bi-exponential (rise ~0.5 ms, decay ~5-10 ms, Erev
-65 to -75 mV). Shunting inhibition vetoes excitation multiplicatively with an "on-the-path"
geometry: only inhibition sitting between the excitatory input and the soma shunts PSP
amplitude, while distal inhibition has negligible effect. Excitation and inhibition co-tune in
time with inhibition lagging excitation by ~1-3 ms in cortex and ~15-50 ms in DSGCs during
null-direction motion, sharpening spike timing. Somatic PSP amplitude decays roughly
exponentially with electrotonic distance (lambda_DC ~100-300 um for RGC dendrites) while local
dendritic non-linearities (Na+, Ca2+, NMDAR) partially compensate for distal attenuation. SAC
boutons onto a DSGC dendrite are spatially asymmetric with stronger inhibition from null-side
SACs, and this cellular asymmetry (not somatic E-I timing alone) is the primary substrate for
direction selectivity at the DSGC level.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0018_literature_survey_synaptic_integration/assets/answer/synaptic-integration-priors-for-dsgc-modelling/full_answer.md) |
| **ID** | [`synaptic-integration-priors-for-dsgc-modelling`](../../../tasks/t0018_literature_survey_synaptic_integration/assets/answer/synaptic-integration-priors-for-dsgc-modelling/) |
| **Question** | What quantitative priors does the synaptic-integration literature supply for the DSGC compartmental model on (1) AMPA/NMDA/GABA receptor kinetics, (2) shunting inhibition, (3) E-I balance temporal co-tuning, (4) dendritic-location-dependent PSP integration, and (5) SAC-to-DSGC inhibitory asymmetry? |
| **Methods** | `papers` |
| **Confidence** | medium |
| **Date created** | 2026-04-20 |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Paper sources** | `10.1038_346565a0`, `10.1073_pnas.80.9.2799`, `10.1038_nature02116`, `no-doi_HausserMel2003_s0959-4388-03-00075-8`, `10.1038_nature00931` |
| **Task sources** | — |
| **URL sources** | — |
| **Created by** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |

</details>

<details>
<summary><strong>Which dendritic-computation motifs observed in cortical,
hippocampal, and cerebellar neurons plausibly transfer to DSGC dendrites,
and what are the biophysical caveats?</strong></summary>

**Confidence**: medium

Three dendritic-computation motifs plausibly transfer from pyramidal, hippocampal, and
cerebellar dendrites to DSGC dendrites: NMDA-receptor-mediated on-branch supralinear
integration, asymmetric shunting inhibition placed on the path between excitation and soma,
and sublinear-to-supralinear regime switching driven by clustered input. Ca2+-plateau BAC
firing and behavioral-timescale plasticity transfer less cleanly because DSGC dendrites are
short and unipolar rather than tufted. All transferred numbers must be treated as targets to
falsify rather than to assume, pending DSGC-specific patch validation.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0016_literature_survey_dendritic_computation/assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/full_answer.md) |
| **ID** | [`dendritic-computation-motifs-for-dsgc-direction-selectivity`](../../../tasks/t0016_literature_survey_dendritic_computation/assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/) |
| **Question** | Which dendritic-computation motifs observed in cortical, hippocampal, and cerebellar neurons plausibly transfer to DSGC dendrites, and what are the biophysical caveats? |
| **Methods** | `papers` |
| **Confidence** | medium |
| **Date created** | 2026-04-20 |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | `10.1038_35005094`, `10.1038_nn1253`, `10.1038_18686`, `10.1126_science.aan3846`, `10.1146_annurev.neuro.28.061604.135703` |
| **Task sources** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **URL sources** | — |
| **Created by** | [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |

</details>
