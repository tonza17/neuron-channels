# Answers: `cable-theory` (4)

4 answer(s).

[Back to all answers](../README.md)

---

<details>
<summary><strong>Do the t0034 distal-length sweep and the t0035 distal-diameter
sweep collapse onto a single DSI-vs-L/lambda curve under Rall's cable
theory, and should t0033 parameterise dendritic morphology in 1-D
(electrotonic length L/lambda) or 2-D (raw length x raw diameter)?</strong></summary>

**Confidence**: medium

No. The two sweeps do not collapse onto a single DSI-vs-L/lambda curve: in the overlapping
L/lambda interval (0.058-0.116) the Pearson r between the paired sweeps is **+0.42** for
primary DSI and **-0.68** for vector-sum DSI, both well below the 0.9 confirmation threshold,
and the sign of the vector-sum r is opposite to the prediction. Pooled degree-2 polynomial
fits leave residual RMSE of **0.040** (primary) and **0.024** (vector-sum), indicating that
non-cable effects dominate the DSI-vs-L/lambda response. t0033 should retain the 2-D (raw
length x raw diameter) morphology parameterisation rather than compress to 1-D L/lambda,
because the direction of the DSI response is not determined by L/lambda alone.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/full_answer.md) |
| **ID** | [`electrotonic-length-collapse-of-length-and-diameter-sweeps`](../../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/) |
| **Question** | Do the t0034 distal-length sweep and the t0035 distal-diameter sweep collapse onto a single DSI-vs-L/lambda curve under Rall's cable theory, and should t0033 parameterise dendritic morphology in 1-D (electrotonic length L/lambda) or 2-D (raw length x raw diameter)? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-04-24 |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |
| **Paper sources** | — |
| **Task sources** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **URL sources** | — |
| **Created by** | [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md) |

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
<summary><strong>What variables of neuronal morphology have been shown by
computational modeling to affect direction selectivity, by what mechanisms,
and what gaps remain?</strong></summary>

**Confidence**: medium

Computational models have shown that direction selectivity is shaped by dendritic length,
branch-order and branching pattern, dendritic diameter (especially in starburst amacrine
cells), spatial layout and kinetic tiling of bipolar-cell inputs, asymmetric arbors and plexus
density, and the electrotonic compartmentalization of terminal branches. The load-bearing
mechanisms are passive cable filtering with transfer-resistance weighting of distributed
inputs, local-global EPSP summation along soma-to-tip dendritic gradients, space-time input
tiling (sustained proximal, transient distal), dendritic-spike branch independence driven by
voltage-gated Na and Ca channels, and asymmetric SAC-to-DSGC inhibition constrained by
morphology. Gaps remain in systematic sweeps of branch order and dendritic diameter on
realistic reconstructions, in joint manipulation of morphology with active conductances at
DSGC tips, and in morphology-aware modeling of cortical and invertebrate direction selectivity
beyond the retina.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/answer/morphology-direction-selectivity-modeling-synthesis/full_answer.md) |
| **ID** | [`morphology-direction-selectivity-modeling-synthesis`](../../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/answer/morphology-direction-selectivity-modeling-synthesis/) |
| **Question** | What variables of neuronal morphology have been shown by computational modeling to affect direction selectivity, by what mechanisms, and what gaps remain? |
| **Methods** | `papers`, `internet` |
| **Confidence** | medium |
| **Date created** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`cable-theory`](../../../meta/categories/cable-theory/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Paper sources** | `10.1038_s41598-018-23998-9`, `10.1017_S0952523804214109`, `10.1371_journal.pbio.0050185`, `10.1016_j.neuron.2016.02.020`, `10.1038_nature13240`, `10.1038_nn.3565`, `10.7554_eLife.81533`, `10.1371_journal.pcbi.1000877`, `10.1523_JNEUROSCI.17-16-06023.1997`, `10.1038_s41467-024-46234-7`, `10.1523_JNEUROSCI.4013-15.2016`, `10.1038_s41593-017-0046-4`, `10.1371_journal.pcbi.1009754`, `10.1038_12194`, `10.1017_S0952523823000019`, `10.1371_journal.pcbi.1000899`, `10.7554_eLife.52949`, `10.1016_j.cub.2018.03.001`, `10.1038_s41467-026-70288-4`, `10.1016_j.celrep.2025.116833` |
| **Task sources** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **URL sources** | [url 1](https://scholar.google.com/), [url 2](https://pubmed.ncbi.nlm.nih.gov/), [url 3](https://www.biorxiv.org/) |
| **Created by** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |

</details>

<details>
<summary><strong>Which morphology parameters most distinguish low-ATP from high-ATP
cells in the t0123 spiking cohort, and does the low-ATP group spend
relatively more ATP at the AIS than in the dendrites?</strong></summary>

**Confidence**: medium

The top 5 morphology parameters by |Cliff's delta| separating high-ATP (top quartile of
atp_per_spike, n = 782) from low-ATP (bottom quartile, n = 782) cells are:
mean_segment_length_um (delta = -0.725, low-ATP cells have ~43% longer segments),
branch_length_cv (delta = +0.554, low-ATP cells are more uniform in branch length),
branch_density_gradient_pd (delta = +0.504, low-ATP cells have weaker preferred-direction
dendrite-density gradient), field_elongation_pd (delta = -0.469, low-ATP cells have more
elongated dendritic field), and ais_length_um (delta = +0.376, low-ATP cells have shorter AIS
by ~12%). The ATP-share answer is Yes for the AIS but the dendrite/soma swap dominates:
low-ATP cells concentrate 93% of per-AP ATP at the soma and 6% at the AIS with only 0.4% in
dendrites, while high-ATP cells push 62% into dendrites and 35% into soma with only 2.6% at
the AIS.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/low-vs-high-atp-morphology-signature/full_answer.md) |
| **ID** | [`low-vs-high-atp-morphology-signature`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/low-vs-high-atp-morphology-signature/) |
| **Question** | Which morphology parameters most distinguish low-ATP from high-ATP cells in the t0123 spiking cohort, and does the low-ATP group spend relatively more ATP at the AIS than in the dendrites? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | medium |
| **Date created** | 2026-05-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`cable-theory`](../../../meta/categories/cable-theory/) |
| **Paper sources** | `10.1038_382363a0`, `10.1152_jn.1997.78.4.1948`, `10.1371_journal.pcbi.1000877`, `10.1097_00004647-200110000-00001`, `10.1371_journal.pcbi.1000840` |
| **Task sources** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md), [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md), [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **URL sources** | — |
| **Created by** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |

</details>
