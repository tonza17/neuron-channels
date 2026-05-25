# Answers: `dendritic-computation` (13)

13 answer(s).

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
<summary><strong>Does NSGA-II with a cytoplasm-volume cost objective produce a
high-DSI front in Cuntz 2010's predicted balancing-factor [0.2, 0.7]
band?</strong></summary>

**Confidence**: medium

Yes. The t0122 single-seed NSGA-II run produced a high-DSI Pareto front whose top-10 cells
(ranked by DSI) place 10 of 10 (finite bf) cells inside the Cuntz 2010  empirical band. Adding
the cytoplasm-volume cost objective pushed the optimiser toward morphologies consistent with
the Cajal wiring-economy principle. This is evidence in favour of using cytoplasm volume as a
biological-cost regulariser in subsequent DSGC MOBO runs.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/answer/cuntz-balancing-factor-prediction-check/full_answer.md) |
| **ID** | [`cuntz-balancing-factor-prediction-check`](../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/answer/cuntz-balancing-factor-prediction-check/) |
| **Question** | Does NSGA-II with a cytoplasm-volume cost objective produce a high-DSI front in Cuntz 2010's predicted balancing-factor [0.2, 0.7] band? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | medium |
| **Date created** | 2026-05-24 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Paper sources** | `10.1371_journal.pcbi.1002107` |
| **Task sources** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0120_morph_generator_geometry_audit`](../../../overview/tasks/task_pages/t0120_morph_generator_geometry_audit.md), [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **URL sources** | [url 1](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107) |
| **Created by** | [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |

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
<summary><strong>When the t0086 13-cell pool of 6 Genuine + 7 Marginal cells is
re-clustered in the t0080 54-d v3 parameter space and a t0084-style
Vm-trace deep-dive is run at 16 directions on per-cluster representative
cells, are the resulting clusters mechanistically distinct (different
dominant channel mechanisms across clusters) or do they share the same
mechanism with parameter-scale variation?</strong></summary>

**Confidence**: medium

No -- the clusters are not mechanistically distinct. The 13-cell re-cluster produces 4
clusters (best_k = 4 by silhouette) and all 4 cluster representatives are NaP-dominant in
PD-minus-ND attribution at 16 directions (frac NaP 0.874-0.997, frac Nav1.6 0.003-0.126, frac
NMDA = 0.000). The verdict is `shared_mechanism_different_scale`: clusters differ in 54-d
parameter scale but not in which channel drives the PD response. This extends t0084's
NaP-dominant cell 767 finding to the wider 13-cell pool of joint-pass / near-joint-pass cells
in the v3 substrate.

Per-cluster fractional channel attribution table (PD = 0 deg, ND = 180 deg, response window
ms):

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | 0.988 | nap |
| 1 | 1634 | 0.000 | 0.126 | 0.874 | nap |
| 2 | 767 | 0.000 | 0.125 | 0.875 | nap |
| 3 | 1639 | 0.000 | 0.003 | 0.997 | nap |

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/assets/answer/are-cluster-motifs-mechanistically-distinct/full_answer.md) |
| **ID** | [`are-cluster-motifs-mechanistically-distinct`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/assets/answer/are-cluster-motifs-mechanistically-distinct/) |
| **Question** | When the t0086 13-cell pool of 6 Genuine + 7 Marginal cells is re-clustered in the t0080 54-d v3 parameter space and a t0084-style Vm-trace deep-dive is run at 16 directions on per-cluster representative cells, are the resulting clusters mechanistically distinct (different dominant channel mechanisms across clusters) or do they share the same mechanism with parameter-scale variation? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-06 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Paper sources** | — |
| **Task sources** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **URL sources** | — |
| **Created by** | [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |

</details>

<details>
<summary><strong>Where does the DSGC bits-per-ATP front sit relative to Niven 2007's
fly-photoreceptor curve, and does it match the Niven super-linear
cost-vs-information scaling?</strong></summary>

**Confidence**: medium

Insufficient evidence. The t0123 single-seed NSGA-II run produced 10 top-Pareto cells under
the post-hoc Strong-Bialek 1998 direct method; the log-log fit exponent p = n/a at r^2 = n/a
is too noisy (n < 10 or r^2 < 0.5) to make a definitive statement about super-linear scaling.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/answer/dsgc-bits-per-atp-vs-niven-2007/full_answer.md) |
| **ID** | [`dsgc-bits-per-atp-vs-niven-2007`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/answer/dsgc-bits-per-atp-vs-niven-2007/) |
| **Question** | Where does the DSGC bits-per-ATP front sit relative to Niven 2007's fly-photoreceptor curve, and does it match the Niven super-linear cost-vs-information scaling? |
| **Methods** | `code-experiment`, `papers`, `internet` |
| **Confidence** | medium |
| **Date created** | 2026-05-24 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Paper sources** | `10.1103_PhysRevLett.80.197` |
| **Task sources** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md), [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md), [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md) |
| **URL sources** | [url 1](https://doi.org/10.1242/jeb.005249), [url 2](https://doi.org/10.1103/PhysRevLett.80.197) |
| **Created by** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md) |

</details>

<details>
<summary><strong>Which biophysical mechanism - NMDA Mg-block, distal Nav1.6, NaP, or
a combination - is responsible for cell 767's joint-pass DSI improvement
in the v3 Bed B substrate?</strong></summary>

**Confidence**: medium

Cell 767's PD/ND difference in integrated dendritic current is attributed primarily to **NaP
sustained depolarisation** (0.0% NMDA, 7.0% Nav1.6, 93.0% NaP) over the response window ms.
Cells 637 and 762 show the same NaP-dominant signature (98.5% and 99.9%), suggesting NaP is a
systematic feature of the v3 Pareto near-pass cluster rather than idiosyncratic to cell 767.
This single-replicate deep-dive did not reproduce cell 767's original 5-seed joint-pass DSI of
0.494 (re-evaluated DSI = 0.000), so the attribution describes the underlying biophysical
signature of these parameters rather than confirming a per-trial joint-pass mechanism;
multi-replicate confirmation requires t0083 or a follow-up multi-seed study.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/full_answer.md) |
| **ID** | [`cell-767-dendritic-spike-mechanism-attribution`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/) |
| **Question** | Which biophysical mechanism - NMDA Mg-block, distal Nav1.6, NaP, or a combination - is responsible for cell 767's joint-pass DSI improvement in the v3 Bed B substrate? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-05 |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Paper sources** | — |
| **Task sources** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **URL sources** | — |
| **Created by** | [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |

</details>

<details>
<summary><strong>Which combination of electrophys + morphology parameters most
distinguishes the Pareto-favoured corner (high MI, low ATP) from the
Pareto-dominated corner (low MI, high ATP) in the t0123 substrate, and what
are the per-corner cell counts and means?</strong></summary>

**Confidence**: medium

The top 5 parameters by absolute z-score difference between the high_mi_low_atp and
low_mi_high_atp corners (each cell z-scored against the full-cohort standardiser, mean per
corner) are: KDR_GBAR (-1.19), branch_length_cv (-1.08), BK_SOMA_GBAR (-1.06), IH_GBAR
(-1.06), and RA_OHM_CM (+1.06). The Pareto-favoured corner contains 1221 spiking cells (mean
MI = 0.984 bits, mean ATP = 5.34e6 molecules / spike, mean DSI = 0.237, mean PD rate = 2.61
Hz) versus 1220 cells in the dominated corner (mean MI = 0.063 bits, mean ATP = 2.61e7
molecules / spike, mean DSI = 0.016, mean PD rate = 12.3 Hz). The diagonal imbalance (1221 +
1220 = 2441 cells vs 343 + 341 = 684 off-diagonal) is the joint Pareto signature.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/pareto-favoured-corner-signature/full_answer.md) |
| **ID** | [`pareto-favoured-corner-signature`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/pareto-favoured-corner-signature/) |
| **Question** | Which combination of electrophys + morphology parameters most distinguishes the Pareto-favoured corner (high MI, low ATP) from the Pareto-dominated corner (low MI, high ATP) in the t0123 substrate, and what are the per-corner cell counts and means? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | medium |
| **Date created** | 2026-05-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Paper sources** | `10.1371_journal.pcbi.1002107`, `10.3389_neuro.01.1.1.001.2007`, `10.1038_nature16468` |
| **Task sources** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md), [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md), [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **URL sources** | — |
| **Created by** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |

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

<details>
<summary><strong>Which objective functions have been used in published
multi-objective optimisation of single-neuron compartmental models, and
what is each one's formula, units, and NEURON-side computational recipe
on a t0091-style 8-direction trial output?</strong></summary>

**Confidence**: high

The published multi-objective single-neuron optimisation literature converges on four
canonical biological objective categories that fit directly on top of the project's existing
pymoo NSGA-II loop: stimulus-spike-train mutual information via the direct method with 1/T
extrapolation, ATP-per-spike via per-compartment integration of Na+ inward current divided by
three (the Na+/K+ ATPase stoichiometry), cytoplasm volume as the sum of pi*r^2*L over
compartments (novel as an explicit MOO target on a single neuron), and Marder-style robustness
as the standard deviation of DSI under +/-10% perturbation of all channel densities. Each
catalogued objective is implemented as one pymoo evaluator callable on the project's existing
8-direction 1400-ms trial output and is reported with a uniform 8-field record (name, LaTeX
formula, units, NEURON-side quantities, recipe, biological-plausibility note,
direction-of-optimisation, supporting paper citations). The methodology synthesis adopts
per-feature SD-normalisation, the 2-3 SD acceptance threshold and ensemble-as-experiment
reporting pattern, and the optimiser-selection rule NSGA-II for high-d 2-3-objective problems,
NSGA-III for high-d many-objective problems, and qLogNEHVI for low-d constrained problems with
population fewer than 20 evaluations. Two additional well-defined objectives surfaced by the
survey are also catalogued with the full 8-field record: coincidence-detection accuracy (the
closest published function-vs-energy MOO analogue to the project's planned DSI-vs-energy work)
and bits-per-ATP efficiency (the canonical empirical Pareto curve in the field). This answer
is grounded in 21 newly catalogued papers plus 9 corpus papers and the BluePyOpt / eFEL /
pymoo / AllenSDK documentation.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/full_answer.md) |
| **ID** | [`objective-functions-for-single-neuron-multi-objective-optimisation`](../../../tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/) |
| **Question** | Which objective functions have been used in published multi-objective optimisation of single-neuron compartmental models, and what is each one's formula, units, and NEURON-side computational recipe on a t0091-style 8-direction trial output? |
| **Methods** | `papers`, `internet` |
| **Confidence** | high |
| **Date created** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Paper sources** | `10.3389_neuro.01.1.1.001.2007`, `10.1371_journal.pcbi.0020094`, `10.3389_fninf.2016.00017`, `10.1097_00004647-200110000-00001`, `10.1242_jeb.017574`, `10.1371_journal.pcbi.1000840`, `10.1038_nrn1949`, `10.1038_nn1352`, `10.1103_PhysRevLett.80.197`, `no-doi_Chklovskii2002_wiring-optimization-cortical`, `10.1371_journal.pcbi.1002107`, `10.1371_journal.pcbi.1000877`, `no-doi_Ament2023_logei-bo`, `10.1523_jneurosci.5346-03.2004`, `10.1098_rstb.1982.0084`, `10.1038_382363a0`, `10.1152_jn.1997.78.4.1948`, `10.1162_neco.1997.9.6.1179`, `10.1146_annurev.neuro.28.061604.135703` |
| **Task sources** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **URL sources** | [url 1](https://github.com/BlueBrain/BluePyOpt), [url 2](https://bluepyopt.readthedocs.io/en/latest/index.html), [url 3](https://github.com/BlueBrain/eFEL), [url 4](https://pymoo.org/), [url 5](https://allensdk.readthedocs.io/en/latest/biophysical_models.html) |
| **Created by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |

</details>
