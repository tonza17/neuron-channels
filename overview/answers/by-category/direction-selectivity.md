# Answers: `direction-selectivity` (32)

32 answer(s).

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
<summary><strong>Do symmetric and asymmetric DSGC morphologies share the same
electrophys parameter regime, or do they form distinct clusters in PC
space?</strong></summary>

**Confidence**: medium

No, they form distinct clusters. PCA on the 54-d electrophys submatrix of the 85-cell primary
cohort (DSI > 0.1 AND PD > 2 Hz, pooled across four 68-d NSGA-II lineages) shows PC1
separating the 20 symmetric and 65 asymmetric cells at Mann-Whitney U=31.0, p=1.5e-10. PC1
captures 29.5 % of variance and loads on terminal-dendrite K-Ca conductances (SK_TERMINAL,
BK_TERMINAL, BK_MID, SK_SOMA) plus primary-dendrite persistent Na (NAP_PRIMARY). The strict
cohort (DSI > 0.2 AND PD > 3 Hz, N=30) preserves the separation (p=8.2e-5), so the result is
not an artefact of the relaxed primary filter. PC2 does not separate the classes (p=0.78), so
the distinction lives on a single axis dominated by terminal-dendrite KCa expression.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/symmetric-vs-asymmetric-electrophys-cluster/full_answer.md) |
| **ID** | [`symmetric-vs-asymmetric-electrophys-cluster`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/symmetric-vs-asymmetric-electrophys-cluster/) |
| **Question** | Do symmetric and asymmetric DSGC morphologies share the same electrophys parameter regime, or do they form distinct clusters in PC space? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-14 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md), [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md), [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **URL sources** | — |
| **Created by** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |

</details>

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
<summary><strong>Does 2-objective NSGA-II (DSI + PD-rate, with the DSI-silence guard
applied) recover joint-pass cells where t0102's 3-objective run found
zero?</strong></summary>

**Confidence**: high

No. Across 2,208 evaluations from two random-init NSGA-II seeds (44 and 55) running the
2-objective DSI + PD formulation with the silence guard active, zero cells cleared the strict
joint-pass corner (DSI >= 0.5 AND PD >= 30 Hz). The DSI extreme broke past 0.5 for the first
time in the t0080-t0104 NSGA-II lineage (seed 55 gen 11, DSI = 0.5417 at PD = 3.57 Hz),
confirming the substrate is not artificially capped by the silenced-cell DSI=1.0
floating-point artifact that contaminated t0102's Pareto front. The L-shaped Pareto front
replicates t0102's exactly — extremes reachable on each axis but the joint corner empirically
empty — ruling out objective-vector dimensionality as the explanation for the
substrate-limited reading.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/assets/answer/t0104-joint-pass-recovery-2obj/full_answer.md) |
| **ID** | [`t0104-joint-pass-recovery-2obj`](../../../tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/assets/answer/t0104-joint-pass-recovery-2obj/) |
| **Question** | Does 2-objective NSGA-II (DSI + PD-rate, with the DSI-silence guard applied) recover joint-pass cells where t0102's 3-objective run found zero? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | high |
| **Date created** | 2026-05-14 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | `10.1371_journal.pcbi.1012039`, `10.48550_arXiv.2306.04525`, `10.48550_arXiv.2401.14014` |
| **Task sources** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md), [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **URL sources** | — |
| **Created by** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |

</details>

<details>
<summary><strong>Does at least one varimax factor recover a joint DSI-PD axis
(|r_DSI| > 0.3 AND |r_PD| > 0.3) when the cohort filter is removed and the
full DSI / PD quality range is in the pool, confirming the truncated-cohort
artefact first observed at t0110 and t0116?</strong></summary>

**Confidence**: high

Yes — F1 of the unfiltered-pool varimax solution is a joint DSI-PD factor (r_DSI = +0.421,
r_PD = +0.352, both p < 1e-100, n = 4431), satisfying |r| > 0.3 on both axes. At the strict
cohort (t0116) zero of ten factors satisfied this criterion. The reappearance of a joint
factor once the filter is lifted confirms the truncated-cohort-artefact hypothesis: the strict
cohort genuinely erases the shared latent that couples DSI and PD; the decoupling is not an
intrinsic substrate property.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-truncated-cohort-artefact-test/full_answer.md) |
| **ID** | [`pooled-all-cells-truncated-cohort-artefact-test`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-truncated-cohort-artefact-test/) |
| **Question** | Does at least one varimax factor recover a joint DSI-PD axis (|r_DSI| > 0.3 AND |r_PD| > 0.3) when the cohort filter is removed and the full DSI / PD quality range is in the pool, confirming the truncated-cohort artefact first observed at t0110 and t0116? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-22 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md), [`t0110_relaxed_cohort_factor_analysis`](../../../overview/tasks/task_pages/t0110_relaxed_cohort_factor_analysis.md), [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **URL sources** | — |
| **Created by** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |

</details>

<details>
<summary><strong>Does long-running 2-direction NSGA-II on the 68-d Bed B + 14-d
morphology substrate recover strict joint-pass cells (DSI >= 0.5 AND PD >=
30 Hz) from random init, and where does hypervolume actually plateau on
this landscape?</strong></summary>

**Confidence**: high

Yes. Across 3,744 evaluations from a single random-init GA seed running 40 generations of
2-direction NSGA-II with ratio DSI, **123 unique cells cleared the strict joint-pass corner**
(DSI
>= 0.5 AND PD >= 30 Hz) — the first joint-pass cells anywhere in the t0080 - t0104 NSGA-II
lineage, every prior task of which returned zero. Hypervolume climbed 604x from 0.2015 at gen
1 to 122.0288 at gen 40 and was effectively flat (under 1% per 60 min) from gen 36 onward,
marking the empirical convergence point on the 2-direction substrate. The reformulation from
16-direction vector-sum DSI to 2-direction ratio DSI — not the longer generation budget —
drove the breakthrough.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0106_long_pdnd_nsga2_300gen/assets/answer/t0106-joint-pass-recovery-2dir/full_answer.md) |
| **ID** | [`t0106-joint-pass-recovery-2dir`](../../../tasks/t0106_long_pdnd_nsga2_300gen/assets/answer/t0106-joint-pass-recovery-2dir/) |
| **Question** | Does long-running 2-direction NSGA-II on the 68-d Bed B + 14-d morphology substrate recover strict joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz) from random init, and where does hypervolume actually plateau on this landscape? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-18 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md), [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md), [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **URL sources** | — |
| **Created by** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |

</details>

<details>
<summary><strong>Does ModelDB 189347 (Poleg-Polsky and Diamond 2016) reproduce every
quantitative claim in Figures 1-8 of the Neuron paper when re-run
faithfully under NEURON 8.2.7, and where do the paper text and the ModelDB
code disagree?</strong></summary>

**Confidence**: medium

Partially. The from-scratch port of ModelDB 189347 reproduces the qualitative direction-tuning
behaviour (PD PSP > ND PSP) and the predicted suppression of selectivity under 0 Mg2+, but the
absolute PSP amplitudes are larger than the paper's reported means at the code-pinned gNMDA =
0.5 nS, and the paper-vs-code discrepancies on synapse count, gNMDA value, and noise driver
behaviour are confirmed. Ten or more discrepancies are catalogued in the full answer including
six MOD-default-vs-main.hoc-override mismatches and four pre-flagged paper-vs-code
disagreements; every Figure 1-8 reproduction outcome is recorded with numerical evidence.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md) |
| **ID** | [`poleg-polsky-2016-reproduction-audit`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/) |
| **Question** | Does ModelDB 189347 (Poleg-Polsky and Diamond 2016) reproduce every quantitative claim in Figures 1-8 of the Neuron paper when re-run faithfully under NEURON 8.2.7, and where do the paper text and the ModelDB code disagree? |
| **Methods** | `papers`, `internet`, `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-04-24 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Paper sources** | `10.1016_j.neuron.2016.02.013` |
| **Task sources** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **URL sources** | [url 1](https://github.com/ModelDBRepository/189347), [url 2](https://senselab.med.yale.edu/ModelDB/showmodel.cshtml?model=189347), [url 3](https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf) |
| **Created by** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |

</details>

<details>
<summary><strong>Does running 68-d NSGA-II at N_EVAL_SEEDS=4 noise replicates,
gens=20, pop=96, 2 random-init GA seeds (44, 55), no warm-start, recover
the strict joint-pass corner (DSI>=0.5 AND PD-rate>=30 Hz AND
robustness>=0.7) of the Bed B + morphology compartmental DSGC
substrate?</strong></summary>

**Confidence**: high

No. Across 2,592 evaluations from two random-init NSGA-II seeds, zero cells cleared the strict
joint-pass corner, and zero cells cleared even the loosest 2-axis test (DSI>=0.5 AND PD>=5
Hz), because DSI and PD-rate are strongly bimodally anti-correlated on this substrate. The
headline max-DSI of 1.0 in both seeds turned out to be a floating-point artifact of the
vector-sum DSI formula on silenced cells with PD=0 Hz; the real DSI ceiling under N=4 noise
replicates is roughly 0.35. The earlier t0091 single joint-pass cell, previously framed as an
NSGA-II discovery, is reframed here as a one-mutation polynomial-mutation descendant of an
alt_topology warm-start anchor, so removing the warm-start removes the entire joint-pass
signal.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0102_seedscale_n4_gen20/assets/answer/does-n4-gens20-2seeds-recover-joint-pass-corner/full_answer.md) |
| **ID** | [`does-n4-gens20-2seeds-recover-joint-pass-corner`](../../../tasks/t0102_seedscale_n4_gen20/assets/answer/does-n4-gens20-2seeds-recover-joint-pass-corner/) |
| **Question** | Does running 68-d NSGA-II at N_EVAL_SEEDS=4 noise replicates, gens=20, pop=96, 2 random-init GA seeds (44, 55), no warm-start, recover the strict joint-pass corner (DSI>=0.5 AND PD-rate>=30 Hz AND robustness>=0.7) of the Bed B + morphology compartmental DSGC substrate? |
| **Methods** | `code-experiment`, `papers`, `internet` |
| **Confidence** | high |
| **Date created** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | `10.1371_journal.pcbi.1012039`, `10.48550_arXiv.2306.04525`, `10.48550_arXiv.2401.14014` |
| **Task sources** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md), [`t0101_brainstorm_results_21`](../../../overview/tasks/task_pages/t0101_brainstorm_results_21.md) |
| **URL sources** | — |
| **Created by** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |

</details>

<details>
<summary><strong>Does setting Voff_bipNMDA = 1 (voltage-independent NMDA, the
deposited 0 Mg2+ condition) reproduce Poleg-Polsky and Diamond 2016's claim
that DSI vs gNMDA is approximately constant ~0.30 across 0-3 nS?</strong></summary>

**Confidence**: medium

No. Voltage-independent NMDA partially flattens the DSI-vs-gNMDA curve — the 0-3 nS range
collapses from 0.174 (Voff_bipNMDA = 0 baseline) to 0.066, satisfying the H1 range threshold
of 0.10 — but the slope test still trends downward at -0.024 per nS, above the 0.02 H1 cutoff
and never within +/- 0.05 of the paper's claimed 0.30. The combined verdict is therefore H2
(flatter than the deposited control but still not flat at 0.30): the Voff = 1 curve runs at
0.04-0.10 across the entire range, not at 0.30. The Voff_bipNMDA = 1 swap by itself does not
reproduce the paper's DSI vs gNMDA claim.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/full_answer.md) |
| **ID** | [`dsi-flatness-test-voltage-independent-nmda`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/) |
| **Question** | Does setting Voff_bipNMDA = 1 (voltage-independent NMDA, the deposited 0 Mg2+ condition) reproduce Poleg-Polsky and Diamond 2016's claim that DSI vs gNMDA is approximately constant ~0.30 across 0-3 nS? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | medium |
| **Date created** | 2026-04-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Paper sources** | `10.1016_j.neuron.2016.02.013` |
| **Task sources** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **URL sources** | — |
| **Created by** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |

</details>

<details>
<summary><strong>Does t0108's all-negative PD-rate factor-correlation column persist
if we re-run the same varimax factor analysis on a less-truncated cohort,
or is it a cohort-selection artifact?</strong></summary>

**Confidence**: high

It is a truncated-cohort artifact. Re-running the same varimax FA pipeline on 247 t0106 cells
at the relaxed threshold DSI > 0.2 AND PD > 3 Hz (vs t0108's 150 cells at DSI > 0.5 AND PD >
10) produces **2 of 10 factors with positive r(PD)** (F2 +0.136 at p=0.033, F4 +0.048 n.s.).
DSI sign distribution flips from t0108's 4 / 6 (positive / negative) to 6 / 4. F1, the
dominant axis in both cohorts, is also reinterpreted: in t0108 it appeared as a PD-only
dropper (r_DSI = +0.06) because the DSI ceiling masked the DSI effect, but in t0110 it is
revealed as the **joint failure axis** (r_DSI = −0.37, r_PD = −0.75). F2's loadings (high
persistent-Na, low Mg-block, low primary-BK) identify "more persistent sodium → more firing"
as a real PD-positive direction that the strict cohort completely hid.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0110_relaxed_cohort_factor_analysis/assets/answer/t0106-pd-correlation-sign-flip-relaxed-cohort/full_answer.md) |
| **ID** | [`t0106-pd-correlation-sign-flip-relaxed-cohort`](../../../tasks/t0110_relaxed_cohort_factor_analysis/assets/answer/t0106-pd-correlation-sign-flip-relaxed-cohort/) |
| **Question** | Does t0108's all-negative PD-rate factor-correlation column persist if we re-run the same varimax factor analysis on a less-truncated cohort, or is it a cohort-selection artifact? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-18 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md) |
| **URL sources** | — |
| **Created by** | [`t0110_relaxed_cohort_factor_analysis`](../../../overview/tasks/task_pages/t0110_relaxed_cohort_factor_analysis.md) |

</details>

<details>
<summary><strong>Does the deposited ModelDB 189347 code reproduce Poleg-Polsky
2016's Fig 3A-F per-synapse conductance balance and DSI-vs-gNMDA flatness,
and does the extended noise sweep match the paper's qualitative
shape?</strong></summary>

**Confidence**: medium

No. Every per-synapse-class summed peak conductance at the code-pinned gNMDA = 0.5 nS is 6-9x
the paper's Fig 3A-E target on the summed scale and well below it on the per-synapse-mean
scale, so neither interpretation reconciles. DSI as a function of gNMDA peaks at 0.19 near
b2gnmda = 0.5 nS and decays toward zero by 3.0 nS, never crossing the paper's claimed flat
~0.30 band. The extended noise sweep shows DSI declining qualitatively as flickerVAR rises in
the control and 0Mg conditions but the trend is weaker than the paper reports, and the ROC AUC
metric saturates at 1.0 across every cell because PSP peaks dwarf baselines on this circuit.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation/full_answer.md) |
| **ID** | [`polegpolsky-2016-fig3-conductances-validation`](../../../tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation/) |
| **Question** | Does the deposited ModelDB 189347 code reproduce Poleg-Polsky 2016's Fig 3A-F per-synapse conductance balance and DSI-vs-gNMDA flatness, and does the extended noise sweep match the paper's qualitative shape? |
| **Methods** | `code-experiment`, `papers` |
| **Confidence** | medium |
| **Date created** | 2026-04-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Paper sources** | `10.1016_j.neuron.2016.02.013` |
| **Task sources** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **URL sources** | — |
| **Created by** | [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |

</details>

<details>
<summary><strong>Does the joint-pass cohort (DSI > 0.7 AND PD > 10 Hz) form a single
connected manifold in 68-d across four NSGA-II seeds (44, 77, 7755, 9354),
or do the seeds occupy seed-specific sub-basins?</strong></summary>

**Confidence**: high

The four-seed pool occupies seed-specific sub-basins, not one connected manifold. KMeans (k=3)
on the standardised 54-d electrophys subspace produces an almost-perfect seed partition
(NMI=0.929, chi-square p<1e-300): cluster 0 = 63/67 seed 9354, cluster 1 = 673/678 seed 7755,
cluster 2 = 121/124 seed 44 (seed 77 contributes 10 scattered cells across all clusters). The
14-d morphology partition is similarly seed-aligned (NMI=0.889). In the combined 68-d PCA
scatter the four seed colours occupy visibly disjoint regions of the PC1-PC2 plane, so the
cross-seed overlap implied by a single connected basin is not observed at the DSI > 0.7 cut.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/assets/answer/pooled-survivors-basin-connectivity-dsi07-pd10/full_answer.md) |
| **ID** | [`pooled-survivors-basin-connectivity-dsi07-pd10`](../../../tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/assets/answer/pooled-survivors-basin-connectivity-dsi07-pd10/) |
| **Question** | Does the joint-pass cohort (DSI > 0.7 AND PD > 10 Hz) form a single connected manifold in 68-d across four NSGA-II seeds (44, 77, 7755, 9354), or do the seeds occupy seed-specific sub-basins? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-21 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md) |
| **URL sources** | — |
| **Created by** | [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |

</details>

<details>
<summary><strong>Does the unfiltered pool (every NSGA-II evaluation, no DSI/PD
cohort filter) form a single connected manifold across seeds 44, 77, 7755,
and 9354, or does the seed-specific basin pattern observed at the strict
cohort (t0116) persist when low-DSI / low-PD cells are also
admitted?</strong></summary>

**Confidence**: high

The seed-specific basin pattern partially dissolves once the cohort filter is removed: the
pool reconnects across seeds but does not form a single connected manifold. Electrophys KMeans
NMI vs seed drops from 0.929 (t0116, strict cohort) to 0.562 (t0117, no filter, n=4431 cells,
k=4), and morphology NMI drops from 0.889 to 0.313 — the morphology subspace shows much
stronger reconnection than the electrophys subspace. Even at the unfiltered pool both
partitions remain significantly seed-aligned (chi-square p<<0.001), so seed effects are
detectable but no longer dominant.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-basin-connectivity-without-filter/full_answer.md) |
| **ID** | [`pooled-all-cells-basin-connectivity-without-filter`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-basin-connectivity-without-filter/) |
| **Question** | Does the unfiltered pool (every NSGA-II evaluation, no DSI/PD cohort filter) form a single connected manifold across seeds 44, 77, 7755, and 9354, or does the seed-specific basin pattern observed at the strict cohort (t0116) persist when low-DSI / low-PD cells are also admitted? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-22 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md), [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **URL sources** | — |
| **Created by** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |

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
<summary><strong>How far did NSGA-II travel from gen-0 (generation == 1) in each
seed when the full quality range is admitted (no DSI / PD filter), and is
the per-seed displacement pattern observed at the strict cohort (seed 44
furthest, seed 9354 closest) preserved at the unfiltered pool?</strong></summary>

**Confidence**: high

Per-seed displacement drops by roughly 5-10x at the unfiltered pool: mean 68-d displacement
collapses from ~60 (all seeds, t0116) to ~9 (all seeds, t0117), and mean PC1+PC2 displacement
from 15.0 / 8.5 / 13.3 / 2.4 (seeds 44 / 77 / 7755 / 9354 at t0116) to 4.9 / 1.5 / 5.7 / 1.6
(t0117). The relative ordering is partially preserved — seeds 44 and 7755 remain the two
furthest from random init at t0117 (4.9 and 5.7 in PC12, top of the table), and seed 9354
remains close to its random init (1.6) — but seed 77 drops from second-furthest to nearly tied
with seed 9354 because the strict cohort retained only the Pareto-front tip of seed 77 (n=10),
while the unfiltered pool admits all 654 of its cells, dominated by lower-quality individuals
near gen-1.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-displacement-from-init-full-pool/full_answer.md) |
| **ID** | [`pooled-all-cells-displacement-from-init-full-pool`](../../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/assets/answer/pooled-all-cells-displacement-from-init-full-pool/) |
| **Question** | How far did NSGA-II travel from gen-0 (generation == 1) in each seed when the full quality range is admitted (no DSI / PD filter), and is the per-seed displacement pattern observed at the strict cohort (seed 44 furthest, seed 9354 closest) preserved at the unfiltered pool? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-22 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **URL sources** | — |
| **Created by** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |

</details>

<details>
<summary><strong>How far did NSGA-II travel from its gen-0 random initialisation in
each seed (44, 77, 7755, 9354), measured in the 68-d standardised parameter
space and in PC1+PC2 space of the combined 68-d PCA?</strong></summary>

**Confidence**: high

The four seeds travel comparably in the full 68-d standardised space (mean displacement
59.7-61.3 standardised units, p95 60.8-61.7) but diverge sharply in the combined PC1+PC2
plane: seed 44 traveled 15.0 PCA units, seed 7755 traveled 13.3, seed 77 traveled 8.5, and
seed 9354 traveled only 2.4. The 68-d uniformity is consistent with each seed's gen-0
distribution covering similar shells of the LHS-sampled parameter space, while the PC1+PC2
divergence reflects the seed-specific direction of NSGA-II descent — the leading components
are exactly the cross-seed axis along which the basins separate. All four seeds traveled
substantially further than their own gen-0 within-seed spread, confirming optimisation moved
the survivors out of the random-init region.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/assets/answer/pooled-survivors-displacement-from-init-dsi07-pd10/full_answer.md) |
| **ID** | [`pooled-survivors-displacement-from-init-dsi07-pd10`](../../../tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/assets/answer/pooled-survivors-displacement-from-init-dsi07-pd10/) |
| **Question** | How far did NSGA-II travel from its gen-0 random initialisation in each seed (44, 77, 7755, 9354), measured in the 68-d standardised parameter space and in PC1+PC2 space of the combined 68-d PCA? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-21 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md), [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **URL sources** | — |
| **Created by** | [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |

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
<summary><strong>When t0106 cells with DSI > 0.5 AND PD > 10 Hz are clustered by
their 14-d morphology parameters, do the clusters carry a distinguishable
electrophys signature?</strong></summary>

**Confidence**: high

Yes, strongly. K-means on the z-scored 14-d morphology submatrix of the 150-cell strict cohort
gives a balanced k=4 split (silhouette 0.233, sizes 21/55/67/7), and 30 of 54 electrophys
parameters separate the clusters at Bonferroni p < 0.05. The strongest discriminators are
NAV16_AIS_GBAR, NAV16_MID_GBAR, CAL_GBAR, CAT_GBAR, IH_GBAR, and AIS_DIAMETER_UM (all p_bonf <
1e-6). Cluster 3 (n=7, low PD ~29 Hz) carries a distinctive high-K low-axonal-Na regime with
very different NAV16_AIS, CAT, SK_TERMINAL, and KV3_PRIMARY values from clusters 0–2. Each
morphology type therefore imposes a distinct channel regime in this cohort.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0108_t0106_cluster_factor_dsi05_pd10/assets/answer/t0106-morphology-clusters-electrophys-signature/full_answer.md) |
| **ID** | [`t0106-morphology-clusters-electrophys-signature`](../../../tasks/t0108_t0106_cluster_factor_dsi05_pd10/assets/answer/t0106-morphology-clusters-electrophys-signature/) |
| **Question** | When t0106 cells with DSI > 0.5 AND PD > 10 Hz are clustered by their 14-d morphology parameters, do the clusters carry a distinguishable electrophys signature? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-18 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **URL sources** | — |
| **Created by** | [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md) |

</details>

<details>
<summary><strong>When t0106 cells with DSI > 0.5 AND PD > 10 Hz are clustered by
their 54-d electrophys parameters, do the clusters carry a distinguishable
morphological signature?</strong></summary>

**Confidence**: medium

Only weakly. K-means on the z-scored 54-d electrophys submatrix of the 150-cell strict cohort
produces an unbalanced k=2 split (10 vs 140; silhouette 0.496) that essentially separates a
small low-firing high-DSI outlier group from the bulk. Across 14 morphology parameters, only 3
differ between the clusters at Bonferroni p < 0.05: mean_branching_angle_deg,
branch_length_cv, ais_length_um. Higher-k partitions degrade silhouette to ~0.13, so no
further morphology-relevant structure exists. The electrophys regime that produces high DSI
and high PD is therefore largely morphology-agnostic within this cohort.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0108_t0106_cluster_factor_dsi05_pd10/assets/answer/t0106-electrophys-clusters-morphology-signature/full_answer.md) |
| **ID** | [`t0106-electrophys-clusters-morphology-signature`](../../../tasks/t0108_t0106_cluster_factor_dsi05_pd10/assets/answer/t0106-electrophys-clusters-morphology-signature/) |
| **Question** | When t0106 cells with DSI > 0.5 AND PD > 10 Hz are clustered by their 54-d electrophys parameters, do the clusters carry a distinguishable morphological signature? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-18 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **URL sources** | — |
| **Created by** | [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md) |

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
<summary><strong>Which factors (combinations of the 68 input parameters) explain DSI
and PD diversity in the strict cohort (DSI > 0.5 AND PD > 10), and is there
a joint factor?</strong></summary>

**Confidence**: medium

Varimax factor analysis on the z-scored 68-d matrix of the 150-cell strict cohort retains 10
factors and identifies F10 as the single joint DSI-PD factor (|r_DSI|=0.31, |r_PD|=0.45).
PD-rate diversity is otherwise dominated by F1 (r=−0.545; SK_TERMINAL, SK_MID, CAT, NAV16_AIS,
NAP_MID loadings); DSI diversity is split between F5 (r=−0.325) and F10 (r=+0.313). F10's
positive direction raises DSI but suppresses PD, making it a trade-off axis along CAD_DEPTH,
CAL, W_ACH, branch_prob_per_um, and mean_segment_length. No single factor jointly increases
both objectives in this cohort.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0108_t0106_cluster_factor_dsi05_pd10/assets/answer/t0106-dsi-pd-factor-decomposition-strict-cohort/full_answer.md) |
| **ID** | [`t0106-dsi-pd-factor-decomposition-strict-cohort`](../../../tasks/t0108_t0106_cluster_factor_dsi05_pd10/assets/answer/t0106-dsi-pd-factor-decomposition-strict-cohort/) |
| **Question** | Which factors (combinations of the 68 input parameters) explain DSI and PD diversity in the strict cohort (DSI > 0.5 AND PD > 10), and is there a joint factor? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-18 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **URL sources** | — |
| **Created by** | [`t0108_t0106_cluster_factor_dsi05_pd10`](../../../overview/tasks/task_pages/t0108_t0106_cluster_factor_dsi05_pd10.md) |

</details>

<details>
<summary><strong>Which factors (combinations of the 68 input parameters) explain DSI
diversity versus PD diversity, and is there a joint factor or are the two
outcomes orthogonal?</strong></summary>

**Confidence**: medium

The two outcomes are mostly orthogonal but partially coupled through one near-joint factor: a
varimax factor analysis on the standardised 68-d matrix (N=85, 10 factors by Kaiser criterion
capped at 10) finds F1 the only factor exceeding |r| = 0.25 on either outcome, with r_DSI =
-0.322 (p=0.003) and r_PD = -0.265 (p=0.014). No factor crosses the joint-factor threshold |r|
> 0.3 on both, so the joint high-DSI / high-PD corner is not unlocked by a single low-d axis.
F1's top loadings (NAP_PRIMARY, SK_MID, MG_CONC_MM, RA_OHM_CM) are bootstrap-stable across 200
resamples, but F3 through F10 are not. The substrate-limited reading from t0102 and t0104 is
reinforced: DSI and PD share a weak common axis but remain substantially orthogonal.

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/dsi-pd-diversity-factor-decomposition/full_answer.md) |
| **ID** | [`dsi-pd-diversity-factor-decomposition`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/answer/dsi-pd-diversity-factor-decomposition/) |
| **Question** | Which factors (combinations of the 68 input parameters) explain DSI diversity versus PD diversity, and is there a joint factor or are the two outcomes orthogonal? |
| **Methods** | `code-experiment` |
| **Confidence** | medium |
| **Date created** | 2026-05-14 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Paper sources** | — |
| **Task sources** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md), [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md), [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **URL sources** | — |
| **Created by** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |

</details>

<details>
<summary><strong>Why do t0090's procedural cells produce zero spikes under the t0083
best-cell channel set, and what is the fix?</strong></summary>

**Confidence**: high

The t0090 generator emits the soma's two pt3d points at coincident `(x, y, 0)` coordinates, so
NEURON computes the cumulative pt3d length as zero, overrides the prior `sec.L =
soma_diameter_um` assignment, and the soma's surface area collapses to ~9.4e-14 µm² —
essentially a point. Synaptic input then drives the somatic Vm to NaN within a few simulation
steps, so every procedural cell in t0090's 60-cell sweep returns `non_finite_voltage` (51
cells) or zero spikes (the 9 STABLE cells that happened to clear the no-stim stability check).
The fix is the `procedural_dsgc_morphology_generator_fix` library: a thin wrapper that
re-emits the soma's pt3d points along the z-axis so the cylinder length equals
`soma_diameter_um` and the surface area matches the t0024 hand-coded reference (~220 µm²).
After applying the fix the BedB-equivalent procedural cell fires 61 spikes in the PD direction
(43.6 Hz, peak Vm ~11 mV).

| Field | Value |
|---|---|
| **Full answer** | [`full_answer.md`](../../../tasks/t0092_diagnose_morphology_generator_silence/assets/answer/t0090-procedural-cell-silence-root-cause/full_answer.md) |
| **ID** | [`t0090-procedural-cell-silence-root-cause`](../../../tasks/t0092_diagnose_morphology_generator_silence/assets/answer/t0090-procedural-cell-silence-root-cause/) |
| **Question** | Why do t0090's procedural cells produce zero spikes under the t0083 best-cell channel set, and what is the fix? |
| **Methods** | `code-experiment` |
| **Confidence** | high |
| **Date created** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |
| **Paper sources** | — |
| **Task sources** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **URL sources** | — |
| **Created by** | [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |

</details>
