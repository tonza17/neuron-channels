# Answers: `voltage-gated-channels` (13)

13 answer(s).

[Back to all answers](../README.md)

---

<details>
<summary><strong>Do the validation triplet results (G.1 AIS-to-soma Nav ratio audit,
G.2 NMDA units calibration, G.3 NaP knockout) confirm or refute the
biological-plausibility flags raised in t0086 and t0088?</strong></summary>

**Confidence**: medium

Conditional. The G.1 AIS-to-soma Nav-ratio audit shows the cluster-1 ratio is a real
biological signal, not a centroid artifact: zero of four cluster-1 cells are pinned to the
soma Nav lower bound and three of four cells individually exceed a ratio of 50, so the
+33-sigma deviation from the Werginz 2024 prior reflects an actual model preference rather
than an inflated denominator. G.2 produces a NetCon-weight to per-spine conductance
calibration that lets us re-score the cluster-NMDA-exotic verdict in calibrated units, but the
conversion does not by itself reduce the deviation enough to rule out a units mismatch. G.3
quantifies the causal contribution of distal NaP to the direction-selectivity index of the
four cluster representatives by comparing knockout DSI against the original t0083 DSI,
providing a per-cell verdict (NaP-dominant, NaP-partial, or NaP-minor). Taken together, the
triplet confirms two of the t0086 / t0088 flags as real biological signals (cluster-1
AIS-to-soma ratio, NaP attribution where the knockout collapses DSI) and leaves the
NMDA-exotic flag in the conditional category pending an independent measurement of per-spine
open conductance in the t0024 voltage-clamp regime.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0090_morphology_generator_diversity_test/assets/answer/validation-triplet-implications-for-biological-plausibility/full_answer.md) |
| **ID** | [`validation-triplet-implications-for-biological-plausibility`](../../../tasks/t0090_morphology_generator_diversity_test/assets/answer/validation-triplet-implications-for-biological-plausibility/) |
| **Question** | Do the validation triplet results (G.1 AIS-to-soma Nav ratio audit, G.2 NMDA units calibration, G.3 NaP knockout) confirm or refute the biological-plausibility flags raised in t0086 and t0088? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | medium |
| **Date created** | 2026-05-07 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Paper sources** | — |
| **Task sources** | [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **URL sources** | — |
| **Created by** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |

</details>

<details>
<summary><strong>Does the 68-d substrate of the t0123 single-seed MI vs
ATP-per-spike NSGA-II run admit a joint MI x ATP latent factor (|r| > 0.30
on both metrics simultaneously), or are MI and ATP driven by decoupled
factors?</strong></summary>

**Confidence**: medium

No, the t0123 substrate does not contain a joint MI x ATP factor. Varimax factor analysis on
the full 5760-cell pool retained 10 factors (16 Kaiser eigenvalues > 1, total variance
explained 34.3%) and zero factors satisfy |r_MI| > 0.30 AND |r_ATP| > 0.30 simultaneously. The
two strongest MI-loaded factors carry r_MI = -0.358 / +0.463 but only r_ATP = +0.205 / +0.063,
and the strongest ATP-loaded factor (F1) ranks 7th on |r_MI|. This contrasts with t0117's
pooled four-seed DSI x PD substrate which found one joint factor F1 (r_DSI = +0.421, r_PD =
+0.352, 12.6% variance).

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/mi-atp-joint-structure-in-t0123-substrate/full_answer.md) |
| **ID** | [`mi-atp-joint-structure-in-t0123-substrate`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/mi-atp-joint-structure-in-t0123-substrate/) |
| **Question** | Does the 68-d substrate of the t0123 single-seed MI vs ATP-per-spike NSGA-II run admit a joint MI x ATP latent factor (|r| > 0.30 on both metrics simultaneously), or are MI and ATP driven by decoupled factors? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | medium |
| **Date created** | 2026-05-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Paper sources** | `10.1371_journal.pcbi.0020094`, `10.1038_nn1352`, `10.1038_nrn1949`, `10.1371_journal.pcbi.1000840`, `10.1103_PhysRevLett.80.197`, `10.1523_jneurosci.5346-03.2004` |
| **Task sources** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md), [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md), [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md), [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md) |
| **URL sources** | — |
| **Created by** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |

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
<summary><strong>What is the Vast.ai GPU cost and recommended organisation of a
joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation
task?</strong></summary>

**Confidence**: medium

Run a surrogate-NN-assisted gradient-free evolutionary search (population 150 x 30 generations
x 3 seeds after a 5,000-sample surrogate-training burn-in, 25 free parameters = 5 Cuntz
morphology scalars + 20 channel gbar parameters) on a single RTX 4090 Vast.ai instance at a
central USD cost of about 51 dollars, with a 0.5x-2x sensitivity envelope of roughly 23-119
dollars. This combination is cheapest among the corpus-justified gradient-free strategies
because the surrogate-NN cuts 18,500 evaluations to ~8 GPU-hours of surrogate inference plus a
one-off ~83 GPU-hour CoreNEURON training burn at the RTX 4090 rate of 0.50 dollars/hour.
Confidence is medium: the CoreNEURON CPU-to-GPU speedup and the surrogate-NN economics are
external assumptions not quantified in the downloaded paper corpus, and the sensitivity grid
is propagated across a 0.5x-2x band for both per-sim cost and sample count.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/full_answer.md) |
| **ID** | [`vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/) |
| **Question** | What is the Vast.ai GPU cost and recommended organisation of a joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation task? |
| **Methods** | `papers`, `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-04-22 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Paper sources** | `10.1038_s41467-024-46234-7`, `10.1371_journal.pcbi.1000877`, `10.1016_j.celrep.2025.116833`, `10.1371_journal.pcbi.1009754`, `10.1152_jn.00123.2009`, `10.1152_jn.1997.78.4.1948`, `10.1162_neco.1997.9.6.1179`, `10.1038_nn.2359`, `10.1016_j.neuron.2007.07.031`, `10.1038_nn2040`, `10.1016_j.neuron.2017.07.020`, `10.1038_382363a0`, `10.1038_s41467-026-70288-4`, `10.1371_journal.pcbi.1000899`, `10.7554_eLife.81533`, `10.1002_cne.21173` |
| **Task sources** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **URL sources** | — |
| **Created by** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |

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
<summary><strong>Which electrophys parameters most distinguish high-MI from low-MI
cells in the t0123 spiking cohort, with effect size and direction?</strong></summary>

**Confidence**: medium

The top 5 electrophys parameters by |Cliff's delta| separating high-MI (top quartile of
mi_count_bits, n = 819) from low-MI (bottom quartile, n = 1024) cells are: IH_GBAR (delta =
-0.786, high-MI cells have ~32x lower mean), CAD_TAUR_MS (delta = -0.717, high-MI cells have
~3.6x faster calcium-buffer time constant), KDR_GBAR (delta = -0.668, high-MI cells have ~9x
lower mean), SK_AIS_GBAR (delta = +0.632, high-MI cells have higher AIS-localised SK density),
and SKAHP_TAU_CA_MULTIPLIER (delta = -0.627, high-MI cells have ~2.4x shorter calcium-driven
AHP time constant). All five Mann-Whitney U p-values are below 1e-115, so the effects are
statistically robust against the n ~ 1000 sample sizes.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/high-vs-low-mi-electrophys-signature/full_answer.md) |
| **ID** | [`high-vs-low-mi-electrophys-signature`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/answer/high-vs-low-mi-electrophys-signature/) |
| **Question** | Which electrophys parameters most distinguish high-MI from low-MI cells in the t0123 spiking cohort, with effect size and direction? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | medium |
| **Date created** | 2026-05-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Paper sources** | `10.1371_journal.pcbi.1000840`, `10.1103_PhysRevLett.80.197`, `10.1523_jneurosci.5346-03.2004`, `10.1152_jn.1997.78.4.1948` |
| **Task sources** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md), [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md), [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **URL sources** | — |
| **Created by** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |

</details>

<details>
<summary><strong>Which factors (after varimax rotation on the full 68-d pool) load
most strongly on dsi_vector_sum and pd_rate_hz, and are they
morphology-dominated, electrophys-dominated, or mixed?</strong></summary>

**Confidence**: medium

F1 is the dominant DSI driver (r=-0.589, p ~ 1e-82) and is mixed — its top loadings include
both electrophys channels (SK_AIS, SKAHP, NAP) and a morphology parameter
(primary_branch_pd_concentration). F3 is the dominant PD-rate driver (r=+0.746, p ~ 1e-155)
and is purely electrophys (NAR, IH, NAV16_SOMA, BK channels, RA). No single factor crosses
|r|>0.3 on both DSI and PD simultaneously, so the strict-cohort pool does not contain a joint
DSI-PD axis — the answer to "are the drivers shared?" is no in this strict cohort, but t0110's
relaxed-cohort analysis shows this is a known truncated-cohort artefact.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/assets/answer/pooled-survivors-latent-drivers-dsi07-pd10/full_answer.md) |
| **ID** | [`pooled-survivors-latent-drivers-dsi07-pd10`](../../../tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/assets/answer/pooled-survivors-latent-drivers-dsi07-pd10/) |
| **Question** | Which factors (after varimax rotation on the full 68-d pool) load most strongly on dsi_vector_sum and pd_rate_hz, and are they morphology-dominated, electrophys-dominated, or mixed? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-21 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md), [`t0110_relaxed_cohort_factor_analysis`](../../../overview/tasks/task_pages/t0110_relaxed_cohort_factor_analysis.md) |
| **URL sources** | — |
| **Created by** | [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |

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

<details>
<summary><strong>Why did the t0078 BoTorch qLogNEHVI MOBO collapse `nav16_ais` to
the search-space floor (1e-5 S/cm^2) at iter 81, and what biological-prior
checklist prevents this failure mode in future MOBO-on-biophysics
tasks?</strong></summary>

**Confidence**: high

The optimiser exploited a soft-prior loophole. t0078's per-tier search bounds let `nav16_ais`
go as low as 1e-5 S/cm^2, four orders of magnitude below Kole 2008's measured cortical AIS Nav
range S/cm^2 and five orders below Werginz 2024's mouse alpha-RGC measurement of 1.3 S/cm^2.
Multi-objective acquisition discovered that an AIS-disabled cell could match a fragment of the
Pareto front (DSI 0.316, PD 9.68 Hz at iter 81) at a lower implicit cost than a Kole-compliant
cell, because the prior was advisory rather than enforced. The fix is hard parameter bounds,
not soft penalties: pre-register `nav16_ais >= 0.25` S/cm^2 (Kole 2008) and AIS-to-soma Nav
ratio `>= 5` (Werginz 2024) as inviolable constraints, plus equivalent priors on every
biophysical parameter where measurement-grounded ranges exist.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/answer/mobo-on-biophysics-ais-disabled-corner/full_answer.md) |
| **ID** | [`mobo-on-biophysics-ais-disabled-corner`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/answer/mobo-on-biophysics-ais-disabled-corner/) |
| **Question** | Why did the t0078 BoTorch qLogNEHVI MOBO collapse `nav16_ais` to the search-space floor (1e-5 S/cm^2) at iter 81, and what biological-prior checklist prevents this failure mode in future MOBO-on-biophysics tasks? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | high |
| **Date created** | 2026-05-04 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Paper sources** | `10.1038_nn2040`, `10.1523_JNEUROSCI.1592-24.2024`, `10.1126_sciadv.abb6642`, `10.1371_journal.pcbi.1002107` |
| **Task sources** | [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **URL sources** | — |
| **Created by** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |

</details>
