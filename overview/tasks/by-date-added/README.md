# Tasks by Date Added

97 tasks grouped by effective task date.

[Back to all tasks](../README.md)

---

## 2026-05-08 (6)

## ⏳ In Progress

<details>
<summary>⏳ 0091 — <strong>First joint 68-d NSGA-II with morphology in eval loop,
5-anchor warm-start</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0091_morphology_extended_nsga2_v1` |
| **Status** | in_progress |
| **Effective date** | 2026-05-08 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Expected assets** | 1 answer, 1 predictions |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-08T11:35:57Z |
| **Task page** | [First joint 68-d NSGA-II with morphology in eval loop, 5-anchor warm-start](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Task folder** | [`t0091_morphology_extended_nsga2_v1/`](../../../tasks/t0091_morphology_extended_nsga2_v1/) |

# First joint 68-d NSGA-II with morphology generation inside the evaluation loop

## Motivation

Brainstorm session 18 (t0089) commissioned a strategic pivot from electrophys-only
optimisation (t0080-t0088) to morphology-extended optimisation. t0090 delivered the procedural
DSGC morphology generator (14 morphology knobs) but committed a soma-`pt3dadd` collapse bug;
t0092 diagnosed the root cause and shipped `generate_fixed_morphology` as a thin shim; t0093
ran the full 60-cell re-sweep under the patched generator (60/60 STABLE-firing, 56/60 with
PD-rate>0, 0 regressions) and issued correction `C-0093-01` (`replace`) redirecting the
canonical procedural generator to t0092's fix. **t0091 imports the t0092 patched generator,
not t0090's unpatched one.** This task is the first NSGA-II run that calls the patched
generator inside the evaluation loop, jointly optimising morphology + electrophys in a 68-d
parameter space.

The strategic question is whether enabling morphology in the optimisation opens
biologically-plausible joint-pass regions that t0080-t0088's fixed-Bed-B substrate could not
reach. t0086 + t0088 established that all v3 substrate joint-pass / near-joint-pass cells are
NaP-dominant in their PD-vs-ND mechanism and exotic by the biological scorecard (NMDA
per-synapse +85 to +116 sigma above Sivyer 2013, distal NaP +9 to +34 sigma above Stuart 1999,
GABA spatial-gradient violations). If morphology variation can shift cells toward biologically
plausible NMDA / NaP regimes while maintaining joint-pass DSI / firing rate, the project's
direction-selectivity story has a second mechanism (morphological asymmetry) on top of the
channel mechanism. If morphology pegs at near-Bed-B defaults across the entire Pareto, the v3
substrate's biological-plausibility ceiling is not raised by morphology and we revisit with a
real-cell library (Option G from the brainstorm) in a future task.

A secondary question concerns the asymmetry direction: if PD-asymmetric anchor cells are
preserved more than their ND-asymmetric mirrors in the final Pareto, that is strong evidence
for soma-displacement-toward-PD as a functional DS mechanism (Schachter 2010, Trenholm 2013,
Briggman 2011).

## Scope

### In Scope

* 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) using the t0092 patched procedural
  generator (`generate_fixed_morphology`, canonicalised by C-0093-01)
* Pop 96, up to 8 generations, adaptive HV-plateau stop, cost watchdog
* 5-anchor warm-start population (Bed-B-like + symmetric + PD-asymmetric + ND-asymmetric +
  alternative-topology), each anchor cloned with ~19 t0083 Pareto electrophys variants
* Pareto-front analysis: comparison to t0083's 54-d front; biological-plausibility scoring per
  t0086 / t0088 framework extended to 68-d cells
* Anchor-tracking analysis: which of the 5 anchors are over- vs under-represented in the final
  Pareto?
* One answer asset on biological plausibility under morphology variation
* One predictions asset (the 68-d Pareto-front cells, with per-cell DSI / PD / robustness /
  morphology vector / electrophys vector)

### Out of Scope

* Topology-changing perturbations beyond t0090's 14 generator knobs
* Real-cell morphology library (deferred to a future task if t0091 negative result motivates)
* NSGA-II at >68-d (e.g., 80-d with extra channels)

## Approach

### Phase A — Build the 5-anchor warm-start population

Pop 96 = 5 anchors x ~19 t0083 Pareto electrophys variants per anchor + 1 random sample.

Anchors:

| Anchor | Description | Source |
| --- | --- | --- |
| 1 | Bed-B-like (matches existing t0083 substrate; the "do not regress from t0083 baseline" anchor) | t0093 patched-generator Bed-B reproducibility (43.6 Hz PD-rate post-fix on the BedB-equivalent point) |
| 2 | Symmetric: `soma_offset_pd_um=0`, `field_elongation_pd=1.0`, `branch_density_gradient_pd=0`, `primary_branch_pd_concentration=0` | Tests whether DS can emerge purely from channel/synapse mechanism without morphological asymmetry |
| 3 | PD-asymmetric: soma offset +100 um toward PD, field elongated 2x along PD, branches biased toward PD | Tests whether morphological asymmetry along PD opens biologically-plausible joint-pass |
| 4 | ND-asymmetric: mirror of #3, soma offset -100 um | Mirror sanity check; if optimiser preserves #3 and discards #4, that is strong evidence for soma-displacement-toward-PD as a functional DS mechanism |
| 5 | Alternative topology: more primary branches (`num_primary_branches=6-7`), deeper Strahler depth, smaller field | Diversifies topology axis specifically |

For each anchor:
* Sample ~19 different electrophys vectors from t0083's gen-17 Pareto archive (using the t0086
  classification: prefer Genuine + Marginal cells over Stochastic ones).
* Combine each electrophys vector with the anchor's morphology vector to produce a complete
  68-d warm-start cell.

Total: 95 warm-start cells from 5 anchors x 19 + 1 random sample = pop 96.

**Time**: ~1-2 hours local. **Cost**: $0.

### Phase B — Joint NSGA-II run

68-d NSGA-II using `pymoo` with NSGA-II algorithm, mixed integer-real handling for the
`num_primary_branches` and `max_strahler_depth` integer parameters.

Settings:
* Population size: 96
* Generations: up to 8 (adaptive HV-plateau stop fires earlier if HV growth < 1 percent for 2
  consecutive gens)
* Crossover: SBX with eta = 15
* Mutation: polynomial mutation with eta = 20, prob = 1 / 68
* Cost watchdog: $4.00 hard cap (well below remaining $4.44 buffer)
* Per-cell evaluation: `from
  tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import
  generate_fixed_morphology` builds the NEURON model from 14 morph params (the soma-pt3d
  collapse bug is fixed at the source); 54 channel / synapse params inserted into generated
  sections; 5 evaluation seeds for inner replication; bar-rotation simulation at 16
  directions; objectives = (DSI vector-sum, PD firing rate, robustness across seeds).

**Hardware**: Vast.ai EPYC 7B13 64-core. 96 cells x 5 seeds x 16 directions x ~60 s/sim / 64
parallel = ~12 minutes per generation. 8 generations: ~1.6 hours / generation x 8 = ~12.8
hours. With overhead: ~14-16 hours wall-clock.

**Cost estimate**: 14-16 hours x $0.40/hr = ~$5.60-6.40. Optimise: drop pop 96 to pop 80 if
cost overshoot looks likely (~80 cells x 8 gens = ~13.3 hours x $0.40 = ~$5.32; still tight).
Fall back: 6 generations (cost watchdog stops at gen 6), ~9-10 hours = ~$3.60-4.00.
**Realistic budget: $3.00-3.50 with adaptive stop or 6-gen cap.**

### Phase C — Pareto-front + biological-plausibility analysis

* Extract 68-d Pareto front from final population.
* Run t0086's `biological_priors.py` + `biological_scorecard.py` on every Pareto cell
  (corrected-units NMDA score from t0090 Phase G.2 validation).
* Compare biological-plausibility distribution to t0083's 54-d Pareto:
  * Do morph-extended cells reach lower NMDA / NaP / GABA exotic-ness while maintaining
    joint-pass DSI / PD / robustness?
  * Do any cells score "plausible" or "stretched" on all 9 priors simultaneously?

### Phase D — Anchor-tracking analysis

For each Pareto cell, compute its 14-d morphology vector's nearest anchor (Euclidean distance
in normalised morph-param space). Tabulate Pareto-cell counts per anchor:

| Anchor | Warm-start contribution (cells) | Final Pareto representation (cells) |
| --- | --- | --- |
| 1 (Bed-B-like) | 19 | ? |
| 2 (Symmetric) | 19 | ? |
| 3 (PD-asymmetric) | 19 | ? |
| 4 (ND-asymmetric) | 19 | ? |
| 5 (Alt-topology) | 19 | ? |

If anchor 3 (PD-asymmetric) is over-represented and anchor 4 (ND-asymmetric) is
under-represented, that is strong evidence for soma-displacement-toward-PD as a functional DS
mechanism. Compute statistical significance via bootstrap.

### Phase E — Answer asset

One answer asset at `assets/answer/morphology-extension-biological-plausibility/`
synthesising:

* Did morphology extension open biologically-plausible joint-pass regions?
* Which of the 5 anchors did the optimiser preserve in the final Pareto?
* Specifically: PD-asymmetric vs ND-asymmetric — is the optimiser-preferred asymmetry
  direction consistent with the published DS mechanism?
* What is the biological-plausibility ceiling of the morphology-extended substrate?
* What follow-ups does this open?

## Pass Criteria

* Phase B converges (HV plateau or 8-gen cap reached) within budget; no NaN propagation; cost
  watchdog not triggered.
* Phase C produces a 68-d Pareto front with at least 8 cells (matching t0083 minimum-Pareto
  threshold).
* Phase D produces a definitive anchor-tracking table with bootstrap-significance p-values.
* Phase E lands a definitive yes / no on whether morphology extension reaches biologically
  plausible cells, with quantitative thresholds.

**Acceptable negative**: optimiser pegs all anchors back toward Bed-B-like (anchor 1 dominates
final Pareto >80 percent) — conclusion is the v3 substrate's biological-plausibility ceiling
is not raised by morphology variation in this parametrisation. Follow-up: Option G real-cell
library in a future task.

## Compute and Budget

* **Vast.ai EPYC 7B13 64-core** for Phase B NSGA-II
* **Local 64-core CPU** for Phases A, C, D, E

**Estimated cost**: $3.00-3.50 (Phase B with adaptive HV-plateau stop or 6-gen cap). Buffer
remaining after t0091: ~$0.94-1.44.

**Cost watchdog**: hard cap at $4.00 (lockout terminates the NSGA-II if cumulative remote
spend exceeds threshold).

## Time Estimation

* Phase A (warm-start): 1-2 h local
* Phase B (NSGA-II): 14-16 h Vast.ai
* Phase C (Pareto analysis): 2-3 h local
* Phase D (anchor-tracking): 2 h local
* Phase E (answer asset): 1 h local

**Total wall-clock**: ~20-24 hours (mostly Phase B remote).

## Expected Assets

* **Answer asset**: morphology-extension biological plausibility synthesis
  (`expected_assets["answer"] = 1`)
* **Predictions asset**: 68-d Pareto-front cells with per-cell DSI / PD / robustness /
  morphology vector / electrophys vector (`expected_assets["predictions"] = 1`)

## Risks and Fallbacks

* **NSGA-II fails to converge in 8 gens**: 68-d is 25 percent more than 54-d; warm-start gives
  strong prior. If HV is still growing at 8 gens, document it and propose extension as a
  future task (only if budget allows).
* **Cost overshoot**: cost watchdog at $4.00 hard cap; drop to 6 gens if approaching.
* **Generator instability under NSGA-II mutation**: if mutated morph_params produce degenerate
  morphologies, the eval function returns a penalty objective. t0093's patched-generator
  re-sweep showed 60/60 STABLE under the t0083 channel set across the wide LHS sample, so the
  patched generator covers the morphology parameter space without NaN_VOLTAGE failures.
* **Anchor 4 ND-asymmetric cells fail to reproduce on the optimiser's seed**: indicates the
  warm-start anchor is unstable; replace with a symmetric anchor variant.
* **All anchors converge to anchor 1 (Bed-B-like)**: acceptable negative; useful finding;
  motivates Option G real-cell library follow-up.

## Verification Criteria

* `verify_research_code.py`, `verify_plan.py`, `verify_logs.py`, `verify_assets.py`,
  `verify_task_file.py` pass with 0 errors.
* `verify_costs.py` passes (cost record present, within budget).
* The answer asset passes `verify_answer.py`.
* The predictions asset passes `verify_predictions.py`.

## Cross-References

* **t0089_brainstorm_results_18** — commissioning brainstorm session.
* **t0090_morphology_generator_diversity_test** — original generator dependency (superseded by
  t0092 / t0093 fix).
* **t0092_diagnose_morphology_generator_silence** — patched generator
  (`generate_fixed_morphology`); canonical entry point for morphology construction.
* **t0093_resweep_and_t0090_correction** — full 60-cell verification of the patched generator
  (60/60 STABLE-firing) and `replace` correction overlay `C-0093-01` redirecting the canonical
  procedural DSGC morphology generator to t0092's fix.
* **t0094_brainstorm_results_19** — brainstorm session that updated this task's dependencies
  and import paths to reference t0092 / t0093 (covers S-0093-01).
* **t0083_bedb_v3_extend_nsga2_gen8plus** — warm-start electrophys archive source.
* **t0086_robustness_cluster_bio_comparison**, **t0088_recluster_marginals_and_vm_motifs** —
  biological-plausibility framework.
* Source suggestions: none directly (new direction). Indirect inheritance from S-0086-01
  (NSGA-II re-run with tightened bounds, kept high for post-t0091 follow-up).

</details>

## ✅ Completed

<details>
<summary>✅ 0095 — <strong>Brainstorm results session 20</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0095_brainstorm_results_20` |
| **Status** | completed |
| **Effective date** | 2026-05-08 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md), [`t0073_brainstorm_results_12`](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0077_brainstorm_results_13`](../../../overview/tasks/task_pages/t0077_brainstorm_results_13.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0079_brainstorm_results_14`](../../../overview/tasks/task_pages/t0079_brainstorm_results_14.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0082_brainstorm_results_15`](../../../overview/tasks/task_pages/t0082_brainstorm_results_15.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md), [`t0085_brainstorm_results_16`](../../../overview/tasks/task_pages/t0085_brainstorm_results_16.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0087_brainstorm_results_17`](../../../overview/tasks/task_pages/t0087_brainstorm_results_17.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md), [`t0089_brainstorm_results_18`](../../../overview/tasks/task_pages/t0089_brainstorm_results_18.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md), [`t0094_brainstorm_results_19`](../../../overview/tasks/task_pages/t0094_brainstorm_results_19.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-08T20:00:00Z |
| **End time** | 2026-05-08T20:45:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 20](../../../overview/tasks/task_pages/t0095_brainstorm_results_20.md) |
| **Task folder** | [`t0095_brainstorm_results_20/`](../../../tasks/t0095_brainstorm_results_20/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0095_brainstorm_results_20/results/results_detailed.md) |

# Brainstorm Results Session 20

Twentieth strategic brainstorm, run on 2026-05-08 while t0091 (`morphology_extended_nsga2_v1`)
is in flight on Vast.ai. With the joint morphology + channel NSGA-II infrastructure now
working end-to-end, the researcher proposed a strategic broadening of the optimisation
objective space. Current MOBO runs maximise DSI and firing rate. The next research direction
is to optimise DSI jointly against a much wider set of biological objectives: information
transfer rate, metabolic energy / ATP per spike, cytoplasm volume, robustness, and other
objectives surfaced by the literature.

The session's only task is to commission a single consolidated literature survey of
multi-objective optimisation in single-neuron compartmental models, scoped broadly across any
neuron type, with formulas and computational recipes for each objective. Rejection of two
already-covered suggestions is included as housekeeping.

## Decisions

1. **Create t0096_literature_survey_multi_objective_neuron_optimisation**. A consolidated
   literature-survey + internet-research + answer-question task that catalogues every
   objective function used in the published multi-objective single-neuron optimisation
   literature, including:

   * Information-theoretic objectives (mutual information, Fisher information, channel
     capacity, stimulus-reconstruction MSE).
   * Metabolic / energy objectives (ATP per spike, total ionic flux, Na+/K+ pump cost,
     bits-per-ATP efficiency).
   * Structural objectives (total dendritic length, total membrane area, cytoplasm volume,
     wiring economy).
   * Robustness / degeneracy objectives (parameter-perturbation sensitivity, noise tolerance,
     Marder-style multi-conductance solution-space).
   * Temporal / coding objectives (latency, jitter, reliability, bandwidth, dynamic range).

   Coverage is broad: any neuron type, any species, any modality. Methodology papers
   (Druckmann 2007/2011, BluePyOpt, Achard & De Schutter 2006, Rumbell et al., Van Geit /
   NeuroFitter) are in scope alongside biological objective-function origin papers (Attwell &
   Laughlin 2001, Niven & Laughlin 2008, Sengupta et al. 2010, Chklovskii, Cuntz et al. 2010,
   Marder & Goaillard 2006). Output deliverables: `research_papers.md`,
   `research_internet.md`, an answer asset catalogueing each objective with formula + units +
   NEURON-side computational recipe, and a `suggestions.json` proposing future MOBO tasks (DSI
   x ITR, DSI x ATP, DSI x volume, DSI x robustness) ranked by biological plausibility and
   budget feasibility. Cost: $0. Independent of t0091; runs in parallel.

2. **Reject S-0093-01** (`Refresh t0091 task description + dependencies to reference t0092 fix
   and t0093 correction overlay`). t0094_brainstorm_results_19 already executed exactly this
   work in-place: t0091's dependencies and import paths now reference t0092 and t0093, the
   short_description is refreshed, and the cross-references list extends with t0092, t0093,
   t0094. The suggestion is operationally fulfilled.

3. **Reject S-0074-03** (`AIS-localised Kv7 follow-up (t0075 candidate)`). The follow-up is
   already planned as `t0075_bio_realistic_ais_param_sweep`, status `not_started`. The
   suggestion is operationally fulfilled by the existing planned task.

4. **No task cancellations.** No suggestion reprioritisations. No new suggestions written by
   the brainstorm itself (t0096 will generate properly-scoped MOBO suggestions during its
   suggestions stage).

5. **Defer outcome-dependent decisions** about t0091 follow-ups (S-0086-01 NMDA re-run; Bed A
   morphology-extended NSGA-II; new MOBO axes derived from t0096) to a future brainstorm once
   t0091 lands.

## Why these decisions

* The morphology + channel optimisation infrastructure is now production-ready (t0091 in
  flight on the t0092-patched generator with t0093 60/60 STABLE validation). The natural next
  research-depth move is to expand the **objective axis** of the Pareto search rather than
  spend more compute on the same DSI + firing-rate objective pair.
* Researcher's stated criterion of "biological plausibility" maps directly to the
  multi-objective framing: optimising DSI alone admits non-physical solutions; jointly
  optimising DSI vs energy or DSI vs volume forces the optimiser into bio-realistic regions of
  the parameter space.
* Survey is $0 and parallelisable with t0091. Fits the tight $4.45 remaining budget without
  contention.
* S-0093-01 and S-0074-03 are operationally fulfilled — keeping them on the active list wastes
  reviewer attention next session.
* Speculative MOBO tasks (DSI x ITR, etc.) deliberately not pre-created. The literature survey
  needs to ground them in concrete formulas and feasibility estimates first; otherwise we'd be
  scoping work without knowing which objectives are computationally tractable from a
  t0091-style trial output.

## Cross-references

* **t0089_brainstorm_results_18** — committed the morphology-extension pivot.
* **t0090_morphology_generator_diversity_test** — original procedural generator.
* **t0092_diagnose_morphology_generator_silence** — soma-pt3d collapse fix.
* **t0093_resweep_and_t0090_correction** — patched-generator 60/60 STABLE validation.
* **t0094_brainstorm_results_19** — launched t0091; already covered S-0093-01 in-place.
* **t0091_morphology_extended_nsga2_v1** — in flight; current MOBO objectives are DSI + firing
  rate. t0096 will catalogue alternative / additional objectives.
* **t0075_bio_realistic_ais_param_sweep** — planned not_started; covers S-0074-03.
* **t0096_literature_survey_multi_objective_neuron_optimisation** — commissioned by this
  session.

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0095_brainstorm_results_20"
> date_completed: "2026-05-08"
> status: "complete"
> ---
> **Results Summary: Brainstorm Session 20**
>
> **Summary**
>
> Twentieth strategic brainstorm, run on 2026-05-08 while t0091
> (`morphology_extended_nsga2_v1`) is in
> flight on Vast.ai. The researcher proposed broadening the MOBO objective space beyond DSI +
> firing
> rate to include information transfer rate, metabolic energy, cytoplasm volume, and
> robustness;
> commissioned a single consolidated literature survey
> (`t0096_literature_survey_multi_objective_neuron_optimisation`) at $0 cost, scoped broadly
> across
> any neuron type, with formulas + computational recipes + future MOBO suggestion list as
> deliverables. Two already-covered suggestions (S-0093-01, S-0074-03) rejected.
>
> **Session Overview**
>

</details>

<details>
<summary>✅ 0094 — <strong>Brainstorm results session 19</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0094_brainstorm_results_19` |
| **Status** | completed |
| **Effective date** | 2026-05-08 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md), [`t0073_brainstorm_results_12`](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0077_brainstorm_results_13`](../../../overview/tasks/task_pages/t0077_brainstorm_results_13.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0079_brainstorm_results_14`](../../../overview/tasks/task_pages/t0079_brainstorm_results_14.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0082_brainstorm_results_15`](../../../overview/tasks/task_pages/t0082_brainstorm_results_15.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md), [`t0085_brainstorm_results_16`](../../../overview/tasks/task_pages/t0085_brainstorm_results_16.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0087_brainstorm_results_17`](../../../overview/tasks/task_pages/t0087_brainstorm_results_17.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md), [`t0089_brainstorm_results_18`](../../../overview/tasks/task_pages/t0089_brainstorm_results_18.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-08T18:00:00Z |
| **End time** | 2026-05-08T18:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 19](../../../overview/tasks/task_pages/t0094_brainstorm_results_19.md) |
| **Task folder** | [`t0094_brainstorm_results_19/`](../../../tasks/t0094_brainstorm_results_19/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0094_brainstorm_results_19/results/results_detailed.md) |

# Brainstorm Results Session 19

Nineteenth strategic brainstorm, run on 2026-05-08 immediately after t0093
(`resweep_and_t0090_correction`) merged to main. The full 60-cell re-sweep under the t0092
patched generator landed at 60/60 STABLE-firing (vs 0/60 pre-fix), 56/60 cells with PD-rate>0,
mean DSI 0.32 (different) / 0.35 (similar), 21/60 cells with DSI > 0.5, and 0 regressions. The
`replace` correction overlay `C-0093-01` is in place, redirecting the canonical procedural
DSGC morphology generator to t0092's `generate_fixed_morphology`.

The researcher's directive for this session was simple: **launch the morphology-extended
NSGA-II optimisation now**. The session's only outstanding work was to make t0091 actually
launchable — its dependencies and import paths still pointed at t0090's unpatched generator.

## Decisions

1. **Update t0091 in place** (allowed because it is `not_started`):

   * Add `t0092_diagnose_morphology_generator_silence` and
     `t0093_resweep_and_t0090_correction` to the dependencies list.
   * Replace the import-path reference in `task_description.md` Phase B per-cell evaluation
     from "t0090 generator" to
     `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`.
   * Update the Bed-B-like anchor (Phase A anchor #1) source from "t0090 Phase F validated
     point" to "t0093 patched-generator Bed-B reproducibility (43.6 Hz PD-rate post-fix)".
   * Add t0092, t0093, and t0094 to Cross-References.
   * Refresh the generator-instability risk to reflect t0093's 60/60 STABLE evidence.
   * Refresh the short_description to reference the patched generator.

2. **Reject S-0092-03** (issue a correction overlay against t0090's generator). t0093 has
   already committed the `replace` correction overlay `C-0093-01` and `verify_corrections.py`
   PASSES. The suggestion is fully covered.

3. **Reject S-0090-04** (tighten t0091 LHS bounds using the 9 STABLE cells from the t0090
   diversity sweep). t0093's patched-generator re-sweep made 60/60 cells STABLE-firing — the
   original "9 STABLE" pool was an artefact of the soma-pt3d collapse bug. The premise that
   "51/60 morphologies failed NAN_VOLTAGE" no longer holds, so the tightening rationale is
   invalidated.

4. **Keep S-0090-02 active** (NaP-knockout sweep at scale on local 64-core EPYC). The fix
   unblocks it; the sweep is partially superseded by t0091 but still useful as an isolated
   mechanism test.

5. **Keep S-0090-03 active** (G.2 NMDA units calibration). Researcher chose to keep it as a
   post-t0091 task instead of folding it into t0091 as a Phase A.5 prerequisite, on the
   grounds that t0091 launch should stay simple and re-scoring after calibration is
   acceptable.

6. **Keep S-0086-01, S-0070-01, S-0067-01, S-0074-01/02/03, S-0076-04, S-0093-01 active.**
   S-0093-01 is operationally fulfilled by this brainstorm (the t0091 update is exactly what
   it asks for) but kept active as a status marker until the next brainstorm session sweeps
   it.

7. **Cost-watchdog cap for t0091 stays at $4.00**, matching the existing plan; gives NSGA-II
   room to hit 8 generations and leaves $0.45 buffer against the $4.45 budget cap.

## Why these decisions

* The morphology pivot is the project's committed strategic direction (set in brainstorm 18);
  the generator pipeline is now fully validated at scale; budget remaining ($4.45) just covers
  t0091's $3.00–3.50 plan estimate. This is the right window to launch.
* S-0092-03 and S-0090-04 are both falsified by the t0093 outcome — keeping them active wastes
  reviewer attention.
* Folding S-0090-03 NMDA calibration into t0091 was tempting (it's local-only, $0 incremental)
  but adds wall-clock and complexity ahead of an already-tight remote run. Researcher
  preferred to keep the launch surface minimal.

## Cross-references

* **t0089_brainstorm_results_18** — committed the morphology-extension pivot; commissioned
  t0090 and t0091.
* **t0090_morphology_generator_diversity_test** — generator with the soma-pt3d collapse bug.
* **t0092_diagnose_morphology_generator_silence** — root cause + `generate_fixed_morphology`
  shim.
* **t0093_resweep_and_t0090_correction** — patched-generator re-sweep + correction overlay.
* **t0091_morphology_extended_nsga2_v1** — updated by this session; ready for execute-task.

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0094_brainstorm_results_19"
> date_completed: "2026-05-08"
> status: "complete"
> ---
> **Results Summary: Brainstorm Session 19**
>
> **Summary**
>
> Nineteenth strategic brainstorm, run on 2026-05-08 immediately after t0093
> (`resweep_and_t0090_correction`) merged with 60/60 cells STABLE-firing under the t0092
> patched
> generator and `C-0093-01` correction overlay in place. The researcher's directive was
> direct: launch
> the morphology-extended NSGA-II optimisation now. The session updated t0091
> (`morphology_extended_nsga2_v1`) in place — added t0092 + t0093 to dependencies, swapped the
> generator import path to
> `tasks.t0092_..code.morphology_generator_fix.generate_fixed_morphology`,
> refreshed the Bed-B-anchor source to t0093's verified post-fix reproducibility point, and
> extended
> cross-references — and rejected two suggestions falsified by the t0093 outcome (S-0092-03,
> S-0090-04). Project budget $20.00; $15.55 spent; **$4.45 remaining** before t0091; estimated
> **$0.95–1.45 buffer remaining** after t0091 with the existing $4.00 cost watchdog.

</details>

<details>
<summary>✅ 0093 — <strong>Patched-generator full 60-morph re-sweep + t0090
correction overlay</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0093_resweep_and_t0090_correction` |
| **Status** | completed |
| **Effective date** | 2026-05-08 |
| **Dependencies** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0092-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`correction`](../../../meta/task_types/correction/) |
| **Start time** | 2026-05-08T00:43:40Z |
| **End time** | 2026-05-08T03:55:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Patched-generator full 60-morph re-sweep + t0090 correction overlay](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Task folder** | [`t0093_resweep_and_t0090_correction/`](../../../tasks/t0093_resweep_and_t0090_correction/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0093_resweep_and_t0090_correction/results/results_detailed.md) |

# Patched-generator full 60-morph re-sweep + t0090 correction overlay

## Motivation

Task t0092 confirmed the soma `pt3dadd` collapse as the load-bearing root cause of t0090's
0/60 spike rate, and shipped a thin shim `generate_fixed_morphology` that recovered firing for
the BedB-equivalent and 5/5 STABLE-from-t0090 cells under the t0083 best-cell channel set. But
the t0092 validation set was small: 1 BedB-equivalent + 5 of t0090's 9 STABLE cells. The
remaining 51 NAN_VOLTAGE cells from t0090's diversity sweep were never re-tested with the
patch, so the project-level evidence that the bug is fully fixed is incomplete.

This task closes that gap by re-running t0090's full 60-morph Phase D verification (30
LHS-sampled "different" + 30 +/-5% "similar") under the patched generator and the unmodified
t0083 best-cell parameter vector, then issuing a correction overlay against t0090's
`procedural_dsgc_morphology_generator` library asset so that downstream consumers (t0091
NSGA-II, future morph-extended runs, t0086 / t0088 cluster re-score work) see the patched
generator as the canonical entry point. Without the correction, downstream skills walking the
library aggregator would re-import the unpatched generator and re-introduce the bug.

## Scope

### In Scope

* Re-run the t0090 60-morphology Phase D verification (30 different + 30 similar) under the
  patched `generate_fixed_morphology` from t0092, with the unmodified t0083 best-cell
  parameter vector and the same 8-direction bar protocol (1400 ms / direction, HH on, single
  seed per direction matching t0090's protocol).
* Compare per-morph results to t0090's pre-fix `verification_summary.json` and produce a
  side-by-side delta JSON quantifying: how many of the 51 NAN_VOLTAGE cells now reach STABLE,
  how many of the 9 STABLE cells now produce spikes, total fraction of cells producing PD-rate
  > 0 Hz post-fix.
* Visualisations: morphology-grid panel coloured by post-fix stability flag (STABLE-firing /
  STABLE-silent / NAN_VOLTAGE / DIVERGED); paired bar chart of pre-fix vs post-fix spike count
  per cell.
* Issue a `replace` correction overlay against t0090's `procedural_dsgc_morphology_generator`
  library asset pointing consumers at t0092's `procedural_dsgc_morphology_generator_fix`.
  Verify the corrections-aware aggregator output reflects the supersession.
* Document the registered metric `direction_selectivity_index` per population
  (`different_set_post_fix`, `similar_set_post_fix`) in the explicit-variant `metrics.json`.

### Out of Scope

* Modifying t0090's library or any other completed task folder (immutable per ARF rules; the
  correction overlay is the only mechanism).
* Refining the soma area to match t0024's 287 µm² reference (S-0092-02 follow-up).
* Investigating the synapse-XY symmetry residual on the BedB base point (S-0092-04 follow-up).
* Joint 68-d NSGA-II run (deferred to t0091).
* Phase G validation triplet re-runs (deferred until BedB-equivalent DSI > 0.1, addressed by
  S-0092-04).

## Approach

### Phase A — Re-sweep driver (under the patched generator)

Implement `code/resweep_driver.py` modelled on t0090's `verification.py` but importing
`generate_fixed_morphology` from t0092's library asset (`from
tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import
generate_fixed_morphology`). For each of the 60 morphologies in t0090's
`data/different_morphologies/` and `data/similar_morphologies/`, build the patched cell, run
the 50 ms no-stim stability check, then the 8-direction bar protocol with the t0083 best-cell
vector. Use the same `SEED_BASE + int(morph_seed)` trial-seed pattern as t0090 to keep results
comparable.

Parallelise on the 64-core EPYC via `ProcessPoolExecutor`. Save 60 results to
`data/post_fix_verification_summary.json` with the same row schema as t0090's
`verification_summary.json` plus a `pre_fix_stability_flag` and `pre_fix_spike_count_total`
column copied from t0090 for easy diffing.

**Validation gate**: run on the first 5 morphologies (limit=5) before scaling to 60. Baseline
expectation: at least 4/5 reach STABLE (vs t0090's 0/5 for the same first-5 cells). If the
small-run reproduces t0090's NAN_VOLTAGE pattern, halt and debug — the patch is not being
applied.

**Time**: ~30 min on 64 cores. **Cost**: $0.

### Phase B — Pre-fix vs post-fix delta analysis

Implement `code/delta_analysis.py` reading both t0090's `verification_summary.json` and the
new `post_fix_verification_summary.json`. Produce `data/pre_post_delta.json` with:

* Per-cell delta entries: `morph_id`, `population`, `pre_stability_flag`,
  `post_stability_flag`, `pre_spike_count_total`, `post_spike_count_total`, `transition_label`
  (e.g. `nan_to_stable_firing`, `stable_silent_to_stable_firing`, `unchanged_nan`,
  `regression_stable_to_nan`).
* Aggregate counts: how many cells in each transition class.
* Pass criterion: at least 50/60 cells produce non-zero PD-rate post-fix. Stretch: 55/60.

If pass criterion is not met, surface which cells regressed and why; document but do not halt
(the correction overlay is independent of the pass-criterion outcome — t0091 needs the
correction whether 50 or 55 or 60 cells fire).

### Phase C — Visualisations

* `results/images/post_fix_morphology_grid.png`: 5x6 grid of the 30 different morphologies (or
  60 in a 6x10 layout) coloured by post-fix stability flag.
* `results/images/pre_vs_post_spike_counts.png`: paired bar chart, one bar pair per cell,
  pre-fix red vs post-fix green, sorted by post-fix spike count descending.
* `results/images/transition_sankey.png` (or stacked bar if Sankey is too heavy): cell-count
  flow from pre-fix-flag to post-fix-flag, showing how many NAN_VOLTAGE cells became STABLE,
  etc.

### Phase D — Correction overlay against t0090

Write `tasks/t0093_../corrections/library_procedural_dsgc_morphology_generator.json` per
`arf/specifications/corrections_specification.md` with:

* `spec_version: "3"`
* `correction_id: "C-0093-01"`
* `correcting_task: "t0093_patched_morph_generator_resweep_and_t0090_correction"`
* `target_task: "t0090_morphology_generator_diversity_test"`
* `target_kind: "library"`
* `target_id: "procedural_dsgc_morphology_generator"`
* `action: "replace"`
* `changes`: pointer to the replacement asset
  (`tasks/t0092_diagnose_morphology_generator_silence/assets/library/procedural_dsgc_morphology_generator_fix/`)
* `rationale`: cite the post-fix re-sweep results, the t0092 root-cause diagnosis (soma pt3d
  collapse), and the t0091 dependency.

Verify the correction format passes `verify_corrections.py` and the library aggregator's
effective output now lists the t0092 library as the canonical procedural DSGC morphology
generator.

### Phase E — Metrics + summary

Read `data/post_fix_verification_summary.json`; aggregate `direction_selectivity_index` per
population (mean over STABLE-and-firing cells only; null if none). Write
`results/metrics.json` in explicit-variant format with two variants (`different_set_post_fix`,
`similar_set_post_fix`).

## Pass Criteria

* **At least 50/60 cells produce non-zero PD-rate** post-fix on the full re-sweep (vs 0/60
  pre-fix).
* **Stretch: 55/60 cells fire post-fix.**
* The `replace` correction overlay against t0090's `procedural_dsgc_morphology_generator` is
  written and `verify_corrections.py` passes.
* The library aggregator's corrections-aware output lists t0092's
  `procedural_dsgc_morphology_generator_fix` as the canonical entry for the procedural DSGC
  morphology generator after running with the corrections overlay applied.
* `data/post_fix_verification_summary.json` exists with 60 entries; matches t0090's row schema
  plus pre-fix-comparison columns.
* All visualisations under `results/images/` are embedded in `results_detailed.md`.

**Acceptable negative**: if fewer than 50/60 cells fire post-fix, document the breakdown of
remaining failure modes (e.g. asymmetry-knob extreme values that survive the soma fix), record
the per-population pass rate, and still issue the correction overlay — the correction is about
canonicalising the patched generator regardless of how many cells the patch recovers.

## Compute and Budget

* **Local 64-core EPYC** for Phase A. No remote machines required.
* **Total cost**: $0. Single-process NEURON simulations parallelised across 64 cores; ~30 min
  wall-clock for Phase A; visualisations and correction overlay add ~30 min total.

## Time Estimation

* Phase A (re-sweep driver + run): ~45 min including the validation-gate small run.
* Phase B (delta analysis): ~30 min.
* Phase C (visualisations): ~30 min.
* Phase D (correction overlay): ~15 min including verifier.
* Phase E (metrics + summary): ~15 min.
* Plus reporting, results, suggestions, PR + merge.
* **Total wall-clock**: ~3-4 hours.

## Expected Assets

* No new library or answer assets. The deliverables are: the post-fix verification summary,
  the delta analysis, the visualisations, the registered-metric report, and the correction
  overlay.

## Risks and Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| The validation-gate small run reproduces t0090's NAN_VOLTAGE pattern (patch not being applied) | Low | Bug in import path or fix-shim invocation | Halt at the gate; inspect `cell.soma.L` after `generate_fixed_morphology`; should be ~15 µm not ~1e-9. |
| Post-fix re-sweep has fewer than 50/60 cells firing | Medium | Pass criterion miss | Document the surviving failure modes per `transition_label`; correction overlay is independent. The acceptable-negative branch records the per-population pass rate. |
| ProcessPoolExecutor on Windows has high per-worker NEURON DLL load cost | Medium | Wall-clock blow-out | Single-process serial execution as fallback; ~5 min × 60 = 5 hours, still within the day's budget. |
| Correction-overlay format error | Low | `verify_corrections.py` fails | Read the spec carefully before writing; test on a copy first. |

## Verification Criteria

* `data/post_fix_verification_summary.json` exists with **60 entries**.
* At least 50/60 entries have `pd_rate_hz > 0` (pass criterion).
* `data/pre_post_delta.json` exists with `transition_label` per cell.
* `corrections/library_procedural_dsgc_morphology_generator.json` exists and
  `verify_corrections.py` PASSES.
* `aggregate_libraries.py` (with corrections applied) lists the t0092 library as the canonical
  `procedural_dsgc_morphology_generator` entry.
* `results/metrics.json` uses explicit-variant format with two variants and only registered
  metric keys; `verify_task_metrics.py` PASSES.
* `verify_task_results.py`, `verify_logs.py`, `verify_task_folder.py`, `verify_task_file.py`,
  `verify_suggestions.py` all PASS with 0 errors.

## Cross-References

* **t0024_port_de_rosenroll_2026_dsgc** — original Bed B port for reference comparisons (no
  imports in this task).
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** — `apply_parameter_vector`,
  `setup_synapses_parametric`, `run_one_trial`, `_compute_nseg`. Used unchanged.
* **t0083_bedb_v3_extend_nsga2_gen8plus** — source of the best-cell parameter vector applied
  to every cell in the re-sweep.
* **t0090_morphology_generator_diversity_test** — source of the 60 morph spec JSONs and the
  pre-fix `verification_summary.json` for delta comparison. **Target of the correction
  overlay.**
* **t0092_diagnose_morphology_generator_silence** — source of the patched generator
  (`generate_fixed_morphology`) and the diagnosis the correction cites.
* Source suggestion: **S-0092-01** (full 60-morph re-sweep). Also implements **S-0092-03**
  (correction overlay) bundled per the consolidated-task preference.

**Results summary:**

> **Results Summary: Patched-Generator 60-Morph Re-Sweep + t0090 Correction Overlay**
>
> **Summary**
>
> The t0092 soma-pt3d fix is fully validated at scale: **60 / 60 cells STABLE-firing**
> post-fix (51
> NAN_VOLTAGE→firing, 9 STABLE-silent→firing, 0 regressions). Pass criterion (≥50/60 with
> non-zero PD-rate) met at **56/60**; stretch (≥55/60) also exceeded. Mean DSI
> different=0.323,
> similar=0.352. The `replace` correction overlay against t0090's
> `procedural_dsgc_morphology_generator` library asset is in place and `verify_corrections.py`
> PASSES;
> supersession check confirms the redirect to t0092's
> `procedural_dsgc_morphology_generator_fix`.
>
> **Metrics**
>
> * **Total cells re-swept**: **60** (30 different + 30 similar).
> * **Post-fix stability**: **60 / 60 STABLE** (vs t0090 pre-fix: 9 / 60).
> * **Cells firing post-fix (any direction)**: **60 / 60** (vs 0 / 60 pre-fix).
> * **Cells with PD-rate > 0 Hz**: **56 / 60** — pass criterion ≥50 met; stretch ≥55 also met.
> * **Cells with DSI > 0.5**: **21 / 60**.
> * **Total spikes across re-sweep**: **16,107** (different=5,608, similar=10,499) vs 0
>   pre-fix.
> * **Mean direction_selectivity_index, different_set_post_fix**: **0.432** (over the 30
>   STABLE cells

</details>

<details>
<summary>✅ 0092 — <strong>Diagnose why t0090 procedural cells produce no action
potentials</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0092_diagnose_morphology_generator_silence` |
| **Status** | completed |
| **Effective date** | 2026-05-08 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Expected assets** | 1 answer, 1 library |
| **Source suggestion** | `S-0090-01` |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/), [`experiment-run`](../../../meta/task_types/experiment-run/), [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-05-07T21:58:19Z |
| **End time** | 2026-05-08T00:55:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Diagnose why t0090 procedural cells produce no action potentials](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Task folder** | [`t0092_diagnose_morphology_generator_silence/`](../../../tasks/t0092_diagnose_morphology_generator_silence/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0092_diagnose_morphology_generator_silence/results/results_detailed.md) |

# Diagnose why t0090 procedural cells produce no action potentials

## Motivation

Task t0090 delivered the 14-knob procedural DSGC morphology generator and ran it through a
60-morphology Phase D verification under the t0083 best-cell parameter vector. The result was
that **0 / 60 cells fired any spikes**: 51 / 60 collapsed to NaN voltage during the early
stability check, and the remaining 9 sat silent (peak Vm = -70 mV exactly for 6 of them, only
-66 to -67 mV for the other 3) across all 8 directions of the bar protocol. The Phase F Bed-B
reproducibility check, Phase G.2 NMDA calibration, and Phase G.3 NaP knockout all bottomed out
on this silence: G.2 produced all-NaN per-spine recordings, G.3 had no non-zero baseline to
knock down, and Phase F had no measurable DSI to compare against the t0083 Pareto reference.

This silence is the gating blocker for **t0091**'s planned 68-d joint NSGA-II run. Warm-start
anchors do not exist; LHS bound tightening cannot be done meaningfully because the 9 STABLE
cells are also silent; any joint optimisation would burn its budget on infeasible
morphologies. Before t0091 can launch, the question "why does the procedural BedB-equivalent
cell, under the exact t0083 best-cell channels, fail to spike?" has to be answered concretely,
with a fix in hand.

This task is the focused diagnostic that answers that question. It does not attempt the full
joint optimisation; it does not retune the BedB base point exhaustively; it does not enlarge
the morphology bounds. It compares the procedural BedB-equivalent cell to the t0024 hand-coded
Bed B cell side-by-side under identical channels and identical synaptic input, isolates the
structural difference that causes silence, and lands a fix as a new generator-side library
that t0091 can adopt.

## Scope

### In Scope

* Build the procedural BedB-equivalent cell from `BEDB_BASE_POINT` via t0090's
  `generate_morphology` and the t0024 hand-coded Bed B cell via t0024's
  `de_rosenroll_2026_dsgc` library (or via t0080's `build_cell_ais.py` which wraps it for the
  trial driver).
* Apply the t0083 best-cell parameter vector to both cells via t0080's
  `apply_parameter_vector`.
* Run identical 8-direction bar trials (1400 ms each, the recorded researcher protocol's HH-on
  Vm/firing-rate mode, single seed) with bit-exact synapse placement seeds on both cells.
* Diagnose the difference. Specifically inspect: (a) `sec.L` after `pt3dadd` calls (does the
  procedural generator emit pt3d points whose Euclidean distance overrides `sec.L =
  node.length_um` silently?), (b) effective electrotonic length per-section (`L /
  lambda_f(100)`) compared to Bed B's, (c) `_section_midpoint_xy` outputs for placed synapses,
  (d) bar arrival times at each synapse vs the trial window `[0, 1400] ms`, (e)
  `cell.origin_xy` vs synapse XY centroid, (f) whether `apply_parameter_vector` actually sets
  channel densities on the procedural sections (no silent-skip on missing mechanism names).
* Implement the identified fix as a new generator helper in `tasks/t0092_.../code/` (NOT a
  modification to t0090's immutable code). The most likely shapes of the fix are: pt3dclear +
  explicit single pt3d-pair sized to L; or asymmetry transform that preserves cable length
  while only re-arranging xy; or a synapse-XY recomputation that uses the intended geometric
  layout rather than NEURON-stored pt3d midpoints.
* Re-run the 8-direction protocol on the patched procedural BedB-equivalent cell and 5 of the
  9 STABLE-but-silent cells from t0090 (different/morph_00, 13, 14, 15, 19, similar/morph_00).
  Pass criterion: at least the BedB-equivalent procedural cell, post-fix, fires under the
  t0083 best-cell channels with non-zero PD-rate AND DSI > 0.1.
* Produce one library asset (the fix module + any helper) and one answer asset (the diagnosis
  + recommended generator behaviour for t0091).

### Out of Scope

* Joint 68-d NSGA-II run (deferred to t0091).
* Retuning `BEDB_BASE_POINT` parameter values in any non-trivial way. If the diagnosis points
  at a mis-specified base point, that is recorded but the parameter retune happens in t0091's
  warm-up phase, not here.
* Repeating Phase D over the full 60-morphology sweep. The task validates fix on a small
  subset (1 BedB-equivalent + 5 STABLE-from-t0090 cells); a full re-sweep belongs in t0091.
* Per-asset re-scoring of t0086 / t0088 cluster centroids.

## Approach

### Phase A — Two-cell side-by-side build

Build both cells inside the same NEURON process and dump their structural state to a single
JSON file:

* For each section: name, parent name, attach end (`PARENT_TIP_LOC`), `L` value as set in
  code, `L` value as NEURON reports it after `pt3dadd` (these may differ — that is the bug we
  are hunting), `nseg`, diameter, all `pt3dadd` x/y/z/diam tuples, computed Euclidean section
  length from the pt3d points, electrotonic length `L / lambda_f(100)`.
* For each cell: `origin_xy`, total dendritic length, soma-to-terminal max path length,
  soma-to- terminal max electrotonic distance.

Output: `data/structural_comparison.json` with two entries (`procedural_bedb`,
`handcoded_bedb`). Per-section dump with side-by-side comparable rows.

### Phase B — Synaptic-placement comparison

For both cells, run `setup_synapses_parametric(cell, n_ach=..., n_gaba=..., placer_seed=42)`
with the t0083 best-cell parameters. Record:

* For each placed synapse: section name, position-along-section, NEURON-reported (x, y) via
  `_section_midpoint_xy`, intended (x, y) from the procedural generator's
  `section_endpoints_xy` midpoint.
* Per-cell: synapse-XY centroid, synapse-XY bounding box, distribution of arrival times under
  the PD bar (direction = 0 deg) — minimum, maximum, mean, fraction of arrivals within `[0,
  1400] ms` (the trial window).

Output: `data/synapse_comparison.json`.

### Phase C — Soma-Vm trace comparison under PD bar

For both cells, run a single PD-direction bar trial (1400 ms, HH on, single fixed seed) with
identical synapse placements (same `placer_seed`). Record the soma Vm trace at 0.1 ms
resolution to a `.npy` file per cell. Plot both traces overlaid; embed in
`results_detailed.md`.

Compute and record per cell: peak Vm, time to peak, spike count using `_count_spikes(threshold
= -10 mV)`, total integrated EPSP area above -70 mV. The hand-coded Bed B cell should produce
a clear spike train under the t0083 best-cell channels (this was t0083's whole point); if it
does NOT, the bug is in `apply_parameter_vector` or the trial driver itself, not the
morphology — that flips the diagnosis to a t0080-side bug.

Output: `data/vm_trace_procedural.npy`, `data/vm_trace_handcoded.npy`,
`results/images/vm_trace_comparison.png`.

### Phase D — Diagnose and isolate root cause

From the structural and synaptic dumps, identify the structural difference(s) that explain the
soma-Vm difference. Document each candidate root cause and the evidence for/against it as a
ranked list. The 4 leading candidates from the t0090 post-mortem:

1. **pt3d-vs-L mismatch.** `pt3dadd(start, end)` with start-end Euclidean distance !=
   `node.length_um` silently overrides `sec.L`. If true, the procedural cell's effective cable
   lengths are determined by xy-coords rather than the intended `mean_segment_length_um`,
   breaking the d_lambda nseg sizing and electrotonic distance assumptions.
2. **Asymmetry transform double-stretch.** The asymmetry block applies `soma_offset` then
   `field_elongation_pd` to xy-coords. For the BedB-equivalent base point both knobs are
   neutral (`soma_offset_pd_um=0, field_elongation_pd=1.0`), so this should be a no-op — but
   the math at lines 350-355 of `generator.py` may have an off-by-something even in the
   neutral case that changes endpoint coordinates.
3. **Synapse XY mismatch with bar geometry.** `BAR_X_START_UM = -40, BAR_VELOCITY = 1 um/ms,
   TSTOP_MS = 1400` is calibrated to Bed B's ~300-um field. If procedural cell's synapse-XY
   bounding box extends well beyond [-40, +1360] in the PD direction, some synapses fire
   outside the trial window and the bar's spatiotemporal envelope mis-aligns with the cell.
4. **Channel application skip.** `apply_parameter_vector` may silently skip sections it does
   not recognise (e.g., expects sections named with a Bed-B-specific prefix). Procedural
   sections are named `*_t90` — verify each section receives the intended `gbar_nav16`,
   `gbar_kdr`, etc.

For each candidate, run a targeted check (read code + dump intermediate state). Mark each as
CONFIRMED, REFUTED, or PARTIAL.

Output: `data/root_cause_analysis.json` with the 4-candidate ranked list and per-candidate
verdict + supporting numbers.

### Phase E — Implement fix

Write the fix as a new helper library at `tasks/t0092_.../code/morphology_generator_fix.py`
(plus tests). The library exposes:

```python
def generate_fixed_morphology(
    params: MorphologyParams,
    morph_seed: int,
) -> MorphologyResult: ...
```

with the same signature as t0090's `generate_morphology` but with the bug fix(es) applied. The
fix is structured as a thin wrapper if possible (call t0090's `generate_morphology` then patch
the result), or as a forked builder if a deeper change is needed (e.g., `pt3dclear` + single
`pt3dadd` pair). Ship unit tests covering the original failure case (BedB-equivalent base
point) plus determinism and no-NaN.

### Phase F — Validation re-run

Run the 8-direction protocol on the patched cells:

* The procedural BedB-equivalent base point.
* The 5 STABLE-but-silent cells from t0090 (different/morph_00, 13, 14, 15, 19;
  similar/morph_00).

Pass criterion: at least the BedB-equivalent procedural cell post-fix has PD-rate > 0 Hz and
DSI > 0.1. Stretch goal: at least 3 of the 5 STABLE-from-t0090 cells produce spikes after the
fix (the other 2 may still fail because of asymmetry-knob extreme values).

Output: `data/post_fix_verification.json` and a polar tuning panel
`results/images/post_fix_polar_tuning.png`.

### Phase G — Answer asset

Synthesise into the answer asset:

* What was the bug (or bugs)?
* How does the fix work, and what is its API?
* Does the fix recover the BedB-equivalent cell's spiking under t0083 channels?
* What does this imply for t0091 — does the joint NSGA-II run need any further preparation
  before it can be launched?

## Pass Criteria

* `data/structural_comparison.json` exists with side-by-side per-section data for both cells.
* `data/synapse_comparison.json` quantifies synapse-XY mismatch (or confirms there is none).
* `data/root_cause_analysis.json` identifies at least one CONFIRMED root cause with evidence.
* The fixed generator produces a procedural BedB-equivalent cell whose PD-rate > 0 Hz and DSI
  > 0.1 under the t0083 best-cell parameter vector.
* Library asset `procedural_dsgc_morphology_generator_fix` and answer asset
  `t0090-procedural-cell-silence-root-cause` both pass their schema verifiers.

**Acceptable negative**: if Phase D identifies that the hand-coded Bed B cell ALSO fails to
spike under the t0083 best-cell channels (i.e., the bug is in t0080's trial driver or in how
the t0083 parameter vector was loaded), record that as the root cause and stop — Phase E and F
become a separate downstream task targeting `apply_parameter_vector` or
`load_default_params.py` rather than the generator.

## Compute and Budget

* **Local 64-core EPYC** for all phases. No remote machines required.
* **Total cost**: $0. Single-process NEURON simulations on the order of seconds-to-minutes per
  cell; comfortably fits in the local budget.
* Budget remaining after t0090: ~$4.45. This task does not move the project total.

## Time Estimation

* Phase A (structural dump): ~30 min.
* Phase B (synapse comparison): ~30 min.
* Phase C (Vm trace comparison): ~15 min.
* Phase D (root cause analysis): ~1-2 hours.
* Phase E (fix implementation): ~2-4 hours depending on whether a thin patch suffices or a
  builder rewrite is needed.
* Phase F (validation re-run): ~30 min.
* Phase G (answer asset): ~30 min.
* **Total wall-clock**: ~1 day.

## Expected Assets

* **Library asset (1)**: `assets/library/procedural_dsgc_morphology_generator_fix/` — the
  patched generator. Categories: `compartmental-modeling`, `direction-selectivity`,
  `retinal-ganglion-cell`.
* **Answer asset (1)**: `assets/answer/t0090-procedural-cell-silence-root-cause/` — the
  diagnosis synthesis. Question: "Why do t0090's procedural cells produce zero spikes under
  the t0083 best-cell channel set, and what is the fix?". Categories:
  `compartmental-modeling`, `direction-selectivity`.

## Risks and Fallbacks

* **The hand-coded Bed B cell also fails to spike under t0083 best-cell channels.** Then the
  bug is in t0080's `apply_parameter_vector` or in the t0083 parameter-vector loader — not in
  the t0090 generator. Record as the root cause, scope a follow-up task targeting t0080 /
  t0083.
* **The procedural cell's structural dump matches the hand-coded cell's section-for-section
  but the soma-Vm traces still diverge.** That points at a subtle NEURON-state bug (e.g., the
  procedural cell's sections are not in the same `h.SectionList` as the hand-coded cell's, so
  some background mechanism enumerator skips them). Investigate via `for sec in h.allsec():
  print(sec.name())` and `h.distance(soma(0.5), terminal(0.5))`.
* **Fix changes the generator's API enough that t0091 needs a new wrapper.** Expose
  `generate_fixed_morphology` as a drop-in replacement so t0091's NSGA-II loop just swaps the
  import path; no signature changes.
* **More than one root cause is involved.** Apply each fix incrementally and document which
  one was load-bearing.

## Verification Criteria

* `verify_task_file.py t0092_diagnose_morphology_generator_silence` passes.
* `verify_logs.py t0092_diagnose_morphology_generator_silence` passes.
* `verify_plan.py`, `verify_task_results.py`, `verify_suggestions.py` all pass.
* The library asset and answer asset both pass their respective verifiers.
* `data/post_fix_verification.json` shows PD-rate > 0 and DSI > 0.1 for the BedB-equivalent
  cell.

## Cross-References

* **t0024_port_de_rosenroll_2026_dsgc** — hand-coded Bed B cell (the "ground truth"
  comparison).
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** — `apply_parameter_vector`,
  `setup_synapses_parametric`, `run_one_trial`, `_section_midpoint_xy`, `_bar_arrival_times`.
  The trial-driver harness consumed by both cells in this task.
* **t0083_bedb_v3_extend_nsga2_gen8plus** — source of the best-cell parameter vector.
* **t0090_morphology_generator_diversity_test** — the task whose silence finding motivates
  this diagnostic. Uses its committed `BEDB_BASE_POINT` and `generate_morphology`. The fix in
  this task does NOT modify t0090; it adds a new sibling library.
* Source suggestion: **S-0090-01** (Retune BEDB_BASE_POINT to elicit spikes under the t0083
  channel set). This task generalises the suggestion: rather than retuning parameter values,
  it diagnoses the structural cause of silence and patches the generator.

**Results summary:**

> **Results Summary: Diagnose t0090 Procedural Cell Silence**
>
> **Summary**
>
> Identified the root cause of t0090's 0/60 spike rate as a **soma `pt3dadd` collapse**: the
> generator
> emits two coincident soma pt3d points, NEURON computes cumulative pt3d distance ≈ 0 and
> overrides
> `sec.L` to ~1e-9 µm, collapsing soma area to ~9.4e-14 µm² (vs hand-coded 287 µm²). Synaptic
> input drives Vm to NaN within a few simulation steps. Fix landed as a thin shim
> `generate_fixed_morphology` that re-emits the soma's two pt3d points along the z-axis.
> Post-fix the
> BedB-equivalent fires **43.6 Hz PD-rate** and all **5/5 STABLE-from-t0090 cells** produce
> spikes
> (stretch target was 3/5).
>
> **Metrics**
>
> * **Hand-coded Bed B (validation gate)**: **41 spikes** under t0083 best-cell vector — gate
> passes, bug is in the generator.
> * **Procedural BedB-equivalent (pre-fix)**: peak Vm = NaN within first few steps; **0
>   spikes**
> across 8 directions.
> * **Procedural BedB-equivalent (post-fix)**: PD-rate = **43.6 Hz**, ND-rate = 40.7 Hz, peak
>   Vm =
> +11.0 mV, DSI = **0.034**.

</details>

## ❌ Cancelled

<details>
<summary>❌ 0096 — <strong>Literature survey: multi-objective optimisation of
single-neuron models</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0096_literature_survey_multi_objective_neuron_optimisation` |
| **Status** | cancelled |
| **Effective date** | 2026-05-08 |
| **Dependencies** | — |
| **Expected assets** | 10 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`internet-research`](../../../meta/task_types/internet-research/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **End time** | 2026-05-08T15:30:00Z |
| **Task page** | [Literature survey: multi-objective optimisation of single-neuron models](../../../overview/tasks/task_pages/t0096_literature_survey_multi_objective_neuron_optimisation.md) |
| **Task folder** | [`t0096_literature_survey_multi_objective_neuron_optimisation/`](../../../tasks/t0096_literature_survey_multi_objective_neuron_optimisation/) |

# Literature Survey: Multi-Objective Optimisation of Single-Neuron Compartmental Models

## Motivation

The morphology + channel optimisation pipeline is now production-ready: t0091
(`morphology_extended_nsga2_v1`) is currently running the first joint 68-d NSGA-II (54-d
electrophys \+ 14-d morphology) on the t0092-patched procedural generator validated at scale
by t0093. Every multi-objective optimisation task this project has run so far (t0076, t0078,
t0080, t0081, t0083, t0086, t0091) has used the same two objectives: direction selectivity
index (DSI) and firing rate. That objective pair was the right choice for the project's
first-question ("which channels maximise DS?") phase, but it leaves the broader
multi-objective landscape unexplored.

The researcher's strategic directive (brainstorm session 20, 2026-05-08) is to broaden the
optimisation objective space:

> Now that we have working optimisation for both morphology and channel composition we can optimise
> for different things. Currently we optimise for DSI and firing rate. However I would like to
> compare results for all sorts of stuff. For example, I would like to optimise for DSI and
> information transfer rate; DSI and energy spent, DSI and minimisation of citoplasm volume etc.
> Perform an extensive literature search and find papers that use different forms of optimisation.
> It does not need to be DSGC but can be any neurons.

This task is the literature-research foundation for that broadening. It catalogues every
objective function used in the published multi-objective single-neuron optimisation
literature, delivers formulas + computational recipes for each, and produces a ranked list of
future MOBO tasks to commission once budget permits. The deliverable is intentionally
actionable: each catalogued objective must be implementable on top of the existing Bed B
NSGA-II loop without infrastructure rewrites.

The task is also the right test of biological plausibility as an optimisation criterion. The
researcher's recurring concern across this project has been that pure DSI maximisation admits
non-physical solutions; jointly optimising DSI vs energy, vs cytoplasm volume, or vs
robustness forces the optimiser into bio-realistic regions of the parameter space. The survey
should explicitly document, per objective, whether published work treats it as a biological
constraint or only as a performance proxy.

## Scope

### In Scope

* **Multi-objective methodology papers** covering single-neuron compartmental models:
  Druckmann et al. 2007 ("A novel multiple objective optimization framework for constraining
  conductance-based neuron models by experimental data"), Druckmann et al. 2011 (eFEL
  precursor), Achard & De Schutter 2006 (first MOEA Purkinje fits), Van Geit et al.
  (NeuroFitter / BluePyOpt), Rumbell et al. (cortical L5 PC MOBO), Hay et al. 2011 (BBP
  cortical L5 multi-objective).
* **Information-theoretic objective functions**: mutual information between stimulus and spike
  train (Bialek, De Ruyter van Steveninck, Strong et al.), Fisher information / discrimination
  capacity (Brunel, Nadal), channel capacity, stimulus-reconstruction MSE, spike-train metrics
  (Victor & Purpura, van Rossum).
* **Metabolic / energy objective functions**: ATP per spike, total ionic flux, Na+/K+ pump
  cost (Attwell & Laughlin 2001 "An energy budget for signaling in the grey matter of the
  brain"), bits-per-ATP energy efficiency (Niven & Laughlin 2008, Sengupta et al. 2010 "Action
  potential energy efficiency varies among neuron types in vertebrates and invertebrates").
* **Structural / wiring objective functions**: total dendritic length, total membrane area,
  cytoplasm / dendritic volume, wiring economy (Chklovskii et al., Cuntz, Forstner, Borst &
  Hausser 2010 "One rule to grow them all").
* **Robustness / degeneracy objective functions**: parameter-perturbation sensitivity, noise
  tolerance (Marder & Goaillard 2006 "Variability, compensation and homeostasis in neuron and
  network function"; Prinz, Bucher & Marder 2004 "Similar network activity from disparate
  circuit parameters").
* **Temporal / coding objective functions**: latency, jitter, spike-timing precision,
  bandwidth, dynamic range.
* **Methods / codebases**: BluePyOpt (Van Geit), NeuroFitter, NSGA-II + NSGA-III in pymoo,
  MOEA literature (Deb et al.), Pareto-front analysis methods (hypervolume, IGD, R2
  indicator).

### Out of Scope

* Network-level optimisation (multi-neuron). Stay on single-neuron compartmental models.
* Reinforcement-learning / deep-learning policy optimisation. Stay on classical MOBO / MOEA.
* Phenomenological integrate-and-fire models without compartmental structure (mention briefly
  if they yield reusable objectives, but do not deep-dive).

## Must-Find Objective Categories

The survey must deliver formula + units + NEURON-side computational recipe for at least one
representative objective in each of these four categories:

1. **Information transfer rate / mutual information** — between stimulus angle and spike-train
   output for our DSGC case. Concrete recipe must specify how to estimate MI from a
   t0091-style 8-direction trial output (e.g., binned spike counts per direction, direct
   method, or extrapolation method).

2. **Metabolic energy / ATP per spike** — computable from HH ionic currents in NEURON.
   Concrete recipe must specify which currents to integrate (Na+ influx, K+ efflux, leak) and
   the conversion factor from charge to ATP molecules (3 Na+ exchanged per ATP via Na+/K+
   ATPase).

3. **Cytoplasm volume / wiring cost** — computable directly from morphology. Concrete recipe:
   sum over compartments of pi * r^2 * L; or total surface area as an alternative; or wiring
   cost = sum of section lengths weighted by diameter.

4. **Robustness / degeneracy** — parameter-perturbation sensitivity of DSI; multi-conductance
   solution-space volume. Concrete recipe must specify a Marder-style protocol: e.g., +/- 10
   percent random perturbation of all channel densities and report DSI standard deviation as
   the objective.

If the literature search uncovers more well-defined objective categories not in this list, add
them to the catalogue and rank them by biological plausibility and computational feasibility.

## Approach

### Stage 1: Research Papers

Survey methodology and biological objective-function origin papers. Download canonical
citations for each objective category. Read full text where available; abstract +
supplementary info otherwise. Produce `research/research_papers.md` with:

* Per-objective subsection grouping the 2-3 canonical papers
* Per-paper extracted formula, units, computational recipe
* Notes on biological plausibility and how the objective would interact with DSI in a
  multi-objective setting

### Stage 2: Research Internet

Survey codebases, tutorials, review articles, and online resources for multi-objective
single-neuron optimisation. Targets: BluePyOpt (Van Geit, github.com/BlueBrain/BluePyOpt),
NeuroFitter, eFEL, pymoo NSGA-II + NSGA-III tutorials, Pareto-front diagnostic libraries
(pyDOE, paretoset). Document API surfaces and example usage that the project could adopt
without rewrites. Produce `research/research_internet.md`.

### Stage 3: Answer Asset

Synthesise findings into a single answer asset
`objective-functions-for-single-neuron-multi-objective-optimisation` (under `assets/answer/`).
Each catalogued objective gets a uniform record:

| Field | Content |
| --- | --- |
| Name | e.g. `mutual_information_stimulus_spike_train` |
| Mathematical formula | LaTeX |
| Units | e.g. bits per second, ATP per spike, um^3 |
| NEURON-side quantities required | Vm trace, ionic currents, spike times, morphology, etc. |
| Recipe | Step-by-step computation from a t0091-style 8-direction trial output |
| Biological plausibility | Notes on whether the objective is a hard biological constraint or a soft proxy |
| Direction-of-optimisation | Maximise / minimise / target value |
| Papers using it | At least 2 citations |

### Stage 4: Suggestions

Emit a ranked list of future MOBO tasks in `results/suggestions.json`. Each suggestion must
include:

* Title (e.g. "Bed B NSGA-II maximising DSI and ITR")
* Kind, priority
* Categories, source_paper if applicable
* Biological plausibility notes
* Budget feasibility estimate (Vast.ai EPYC + GPU hours)
* Cross-references to the catalogued objective entries

Suggestions must be ranked by combined biological-plausibility and budget-feasibility scores.
Aim for 3-6 ranked suggestions; do not pad.

## Cost Estimation

* **Total**: $0
* **Compute**: none. Local-only.
* **Paid services**: none.
* **Risk-of-going-over**: zero. The task is paper download + reading + writing.

## Step by Step

1. `init-folders`, `check-deps` (no deps to check).
2. Stage 1: research papers — download 10+ canonical papers; read; populate
   `research/research_papers.md`; create paper assets.
3. Stage 2: research internet — survey codebases, tutorials, review articles; populate
   `research/research_internet.md`.
4. Stage 3: answer asset — write the consolidated objective-function catalogue.
5. Stage 4: suggestions — write `results/suggestions.json` with the ranked future-MOBO list.
6. Reporting — write `results/results_summary.md` and `results/results_detailed.md`; run
   verificators; PR; merge.

## Remote Machines

None.

## Assets Needed

None. The task downloads its own paper assets.

## Expected Assets

* `paper`: at least 10 (covering methodology + four must-find categories)
* `answer`: 1 (the consolidated objective-function catalogue)

## Time Estimation

Approximately 2-4 hours wall-clock by an autonomous research agent. Roughly: 60-90 min paper
download + reading; 30-60 min internet survey + codebase review; 30-60 min answer asset
writing; 15-30 min suggestions + reporting + verification.

## Risks & Fallbacks

* **Paywalled paper not accessible** via Sci-Hub or institutional proxy: mark in
  `intervention/` and proceed with abstract + citation analysis. Do not block the task.
* **Cytoplasm volume has no direct precedent** in single-neuron optimisation literature: use
  the wiring-cost / total-length proxy and flag it as a novel objective contribution. The
  computational recipe is already trivial (sum over compartments of pi * r^2 * L) so the
  objective stays usable even without a published precedent.
* **Answer asset becomes too long** (>5000 words): split per category but keep one
  consolidated `short_answer.md` as the entry point. Each category subsection in
  `full_answer.md` may be a separate H2 section.
* **Literature search dilutes** because too many off-target papers come up: enforce the
  Out-of-Scope filter; prefer 2-3 canonical citations per category over comprehensive
  coverage.

## Verification Criteria

* All four must-find objective categories covered with formulas and computational recipes.
* At least 5 multi-objective compartmental-model methodology papers reviewed.
* At least 10 paper assets created and passing the paper asset verificator.
* Answer asset passes `meta/asset_types/answer/specification.md`.
* At least 3 ranked, budget-realistic future MOBO suggestions emitted in
  `results/suggestions.json`.
* All standard task verificators pass: `verify_task_file`, `verify_logs`,
  `verify_research_papers`, `verify_research_internet`, `verify_assets`, `verify_suggestions`,
  `verify_task_results`, `verify_pr_premerge`.

## Cross-References

* **t0091_morphology_extended_nsga2_v1** — current MOBO frontier (DSI + firing rate);
  catalogue's recipes must compose with t0091's trial-output format.
* **t0095_brainstorm_results_20** — commissioned this task.
* **t0002_literature_survey_dsgc_compartmental_models** — prior literature survey for
  stylistic consistency.
* **t0015 / t0016 / t0017 / t0018 / t0019 / t0027** — prior literature surveys for stylistic
  consistency and for any cross-cited references.

</details>

## 2026-05-07 (2)

## ✅ Completed

<details>
<summary>✅ 0090 — <strong>Procedural DSGC morphology generator + diversity test
+ validation bundle</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0090_morphology_generator_diversity_test` |
| **Status** | completed |
| **Effective date** | 2026-05-07 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Expected assets** | 1 library, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-07T14:35:43Z |
| **End time** | 2026-05-07T18:25:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Procedural DSGC morphology generator + diversity test + validation bundle](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Task folder** | [`t0090_morphology_generator_diversity_test/`](../../../tasks/t0090_morphology_generator_diversity_test/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0090_morphology_generator_diversity_test/results/results_detailed.md) |

# Procedural DSGC morphology generator + diversity test + validation bundle

## Motivation

The project is making a strategic pivot from electrophys-only optimisation (t0080-t0088) to
**morphology-extended optimisation**. Up to t0088, all NSGA-II runs (t0076 through t0083) used
the fixed Bed B morphology (de Rosenroll 2026 port from t0024). Morphology was
sensitivity-tested one-axis-at-a-time (t0029, t0030, t0034, t0035, t0041) but was never inside
the optimisation vector.

Brainstorm session 18 (t0089) commissioned a procedural DSGC morphology generator that exposes
explicit knobs for topology, asymmetry, and geometry. Once validated, the generator will be
called inside t0091's NSGA-II evaluation loop, producing a 68-d joint optimisation (54-d v3
electrophys + 14-d morphology) warm-started from 5 distinct morph anchors.

This task delivers the validated generator, a diversity test demonstrating it covers the
intended morphology space, a Bed-B reproducibility check, and three bundled validation
suggestions that sharpen the biological interpretation of t0091's results.

## Scope

### In Scope

* Procedural Python generator emitting NEURON sections + connectivity from 14 morphology
  parameters
* Deterministic given (`params`, `morph_seed`) — same inputs produce identical sections
* 30 very-different morphologies generated via wide Latin Hypercube over the 14-d parameter
  space
* 30 very-similar morphologies generated via tight perturbations (+/- 5 percent) around a
  Bed-B-equivalent base point
* Verification simulation per morphology (50 ms no-stim stability + 8-direction bar protocol
  with default t0083 best-cell channels)
* 2D dendrogram visualisation for all 60 morphologies + PCA / UMAP of morphometric features
* Bed-B reproducibility check on 5 t0083 Pareto cells
* Validation bundle (S-0088-02 AIS-to-soma Nav ratio audit, S-0086-02 NMDA units calibration,
  S-0088-01 causal NaP-knockout per cluster representative)
* One library asset (the generator) and one answer asset (mechanism distinctness across the
  validation triplet)

### Out of Scope

* The joint 68-d NSGA-II run itself (deferred to t0091)
* Topology-changing perturbations beyond the generator's parametric knobs (e.g., stochastic
  L-system extensions, real-cell library)
* Alternative simulators (NetPyNE / Brian2 / Arbor); NEURON only

## Approach

### Phase A — Implement procedural generator

Implement a Python module under `tasks/t0090_morphology_generator_diversity_test/code/` that
exposes:

```python
def generate_morphology(
    params: MorphologyParams,
    morph_seed: int,
) -> MorphologyResult:
    ...
```

The 14 morphology parameters:

| Group | Parameter | Range | Type |
| --- | --- | --- | --- |
| Topology | `num_primary_branches` | 3-7 | int |
| Topology | `branch_prob_per_um` | 0.005-0.05 | float |
| Topology | `max_strahler_depth` | 2-6 | int |
| Topology | `mean_branching_angle_deg` | 30-90 | float |
| Topology | `rall_exponent` | 0.5-2.0 | float |
| Asymmetry | `soma_offset_pd_um` | -150 to +150 | float |
| Asymmetry | `field_elongation_pd` | 1.0-3.0 | float |
| Asymmetry | `branch_density_gradient_pd` | -1 to +1 | float |
| Asymmetry | `primary_branch_pd_concentration` | 0-5 (von Mises kappa) | float |
| Geometry | `mean_segment_length_um` | 10-60 | float |
| Geometry | `soma_diameter_um` | 8-18 | float |
| Geometry | `ais_length_um` | 15-60 | float |
| Stochastic | `morph_seed` | int | int |
| Stochastic | `branch_length_cv` | 0-0.5 | float |

Sampling primary branches at angles drawn from a von Mises distribution biased by
`primary_branch_pd_concentration`; recursive branching constrained by `branch_prob_per_um`,
`mean_branching_angle_deg`, `max_strahler_depth`; daughter / parent diameter scaling by
`rall_exponent` (Rall's law); asymmetry transforms applied post-hoc (soma offset, field
elongation, branch density gradient).

Unit tests (in `code/test_*.py`):
* Determinism: same `(params, seed)` produces identical sections (compare section count,
  lengths, diameters)
* Edge cases: `num_primary_branches=3` (minimum) and `=7` (maximum), `max_strahler_depth=2`
  (shallow) and `=6` (deep)
* Round-trip: serialise NEURON sections to dict, reconstruct, confirm electrical-equivalence
* No-NaN: all section lengths > 0, all diameters > 0, no disconnected sections

Style: follow `arf/styleguide/python_styleguide.md`. Centralise paths in `paths.py`, constants
in `constants.py`. Use frozen dataclasses for `MorphologyParams` and `MorphologyResult`.

**Time**: ~1.5-2 days local development.

### Phase B — Generate 30 very-different morphologies

Wide Latin Hypercube sample over the 14-d morph parameter space. Each LHS row is a complete
parameter vector; generation is embarrassingly parallel across 64 cores using a
`ProcessPoolExecutor`.

Output: 30 morphology specifications saved to
`tasks/t0090_morphology_generator_diversity_test/data/different_morphologies/`.

**Time**: seconds (generation only).

### Phase C — Generate 30 very-similar morphologies

Define a Bed-B-equivalent base point (matches de Rosenroll 2026 morphology approximately).
Generate 30 perturbations: each parameter independently jittered uniform +/- 5 percent of its
range. Same parallel infrastructure as Phase B.

Output: 30 morphology specifications saved to `data/similar_morphologies/`.

**Time**: seconds.

### Phase D — Verification simulation per morphology

For each of the 60 morphologies (30 different + 30 similar):

1. Build the morphology as NEURON sections.
2. Run a 50 ms no-stim stability check at V_rest = -70 mV; confirm no NaN voltages, no
   divergence, no disconnected sections.
3. Run an 8-direction bar protocol with default t0083 best-cell channels (1400 ms trial length
   per the recorded researcher protocol; HH on for Vm / firing rate / DSI mode); confirm DSI
   is computable, simulation does not diverge.

Parallelise on 64 cores. Catch NaN / divergence / disconnected sections per morphology and
write a per-morphology stability flag.

**Cost**: $0 if local 64-core CPU; ~$0.10-0.20 if Vast.ai. **Time**: ~5-10 min on 64 cores.

### Phase E — Visualisation

Per morphology:
* 2D dendrogram (parent-segment radial layout)
* Morphometric features: total dendritic length (um), branch count, max Strahler depth,
  electrotonic length, soma displacement (sqrt of `soma_offset_pd_um^2`), dendritic field
  major-axis length

Across morphologies:
* Side-by-side panel: 30 different morphologies in a 5x6 grid; 30 similar morphologies in a
  5x6 grid; visual comparison of diversity coverage.
* Morphometric PCA: scatter of all 60 morphologies in PC1-PC2 with different / similar
  colour-coded.
* UMAP if `umap-learn` is available; PCA fallback if not (per t0088 precedent).

**Charts** (saved to `results/images/`):
* `morphology_grid_different.png` — 5x6 panel of 30 different morphologies
* `morphology_grid_similar.png` — 5x6 panel of 30 similar morphologies
* `morphometric_pca.png` — PCA of morphometric features
* `morphometric_umap.png` — UMAP if available

**Time**: ~1 hour local.

### Phase F — Bed-B reproducibility

Identify the `morph_params` point that approximates the de Rosenroll 2026 / Bed B port from
t0024:
* Use `num_primary_branches` matching the published value
* `mean_segment_length_um` calibrated to the published total dendritic length
* `soma_offset_pd_um=0` (Bed B is symmetric in the absence of explicit asymmetry)
* `field_elongation_pd=1.0`, `branch_density_gradient_pd=0`,
  `primary_branch_pd_concentration=0`
* `rall_exponent` matching Bed B's diameter taper
* `soma_diameter_um` matching Bed B's soma
* `ais_length_um` matching Bed B's AIS

Run 5 t0083 Pareto cells through the generator at this point; compare DSI / PD firing rate to
their original Bed B values (from t0083's `all_evaluations.json`). Pass criterion: within 5
percent.

**Time**: ~1 hour on 64 cores.

### Phase G — Validation bundle

Three bundled validation suggestions:

#### G.1 — S-0088-02: AIS-to-soma Nav ratio audit (cluster 1)

t0088 reported cluster 1 (cells 1304, 1504, 1624, 1634) has an AIS-to-soma Nav ratio = 116,
+33 sigma above Werginz 2024's 17.3 +/- 3 — the most extreme single-prior violation in t0086
or t0088. Audit the ratio computation:

* Confirm `centroid_unnormalised[NAV16_AIS_GBAR] / centroid_unnormalised[NAV16_SOMA_GBAR]` is
  in matching units (S/cm^2 / S/cm^2 = dimensionless).
* Check the soma Nav lower bound is not pinning the centroid soma value to a near-zero value,
  inflating the ratio.
* Check whether the 4 cluster-1 cells individually have AIS-to-soma ratios near 116, or
  whether the centroid is averaging across heterogeneous values.

Pure data analysis on existing JSON outputs from t0088 / t0086. **Time**: ~30 min, **cost**:
$0.

#### G.2 — S-0086-02: NMDA units calibration ablation

t0086's NMDA exotic verdict (>=85 sigma above Sivyer 2013) is so extreme that it likely
partially reflects a units / scope mismatch rather than a genuinely outlier biological
mechanism. The t0080 ParameterVector encoding `gnmda_dend` is the NetCon weight used in the
Exp2NMDA mechanism, while Sivyer 2013's value is a per-spine synaptic conductance measured in
voltage-clamp on RGC dendritic spines. These may differ by a per-cell area normalisation or by
an effective open-channel-fraction factor.

Run a calibration ablation: take a single t0080 cell, vary `gnmda_dend` from 1e-5 to 1e-2 uS,
measure the per-spine effective open conductance from the NEURON state during a stimulus, and
produce a calibration curve mapping NetCon weight to per-spine conductance. Then re-score the
t0086 / t0088 clusters against Sivyer 2013 in the corrected units. **Time**: ~1 hour,
**cost**: ~$0.30.

#### G.3 — S-0088-01: Causal NaP-knockout per cluster representative

t0088 attributed PD-minus-ND fractional contributions correlationally (NMDA 0%, Nav1.6
0.3-12.6%, NaP 87.4-99.7% across the 4 cluster representatives). To causally confirm NaP as
the dominant mechanism, set `nap_dend_distal = 0` in each of the 4 representative cells (1604,
1634, 767, 1639) and re-measure DSI at the 16 directions used by t0088. Expected effect: DSI
collapses to <0.2 in all 4 cells if NaP is causally responsible; DSI partially preserved if
NMDA + Nav1.6 + GABA also contribute.

Local-CPU only: 4 cells x 16 directions x ~60 s/sim = ~64 min wall-clock, **cost** $0.

#### G — Synthesis answer asset

One answer asset at
`assets/answer/validation-triplet-implications-for-biological-plausibility/` synthesising the
three findings: (a) does the cluster-1 AIS-to-soma Nav ratio reflect a units bug or a real
biological signal? (b) does the NMDA units calibration shift the cluster-NMDA-exotic verdict?
(c) does causal NaP-knockout confirm NaP-dominance, or does the attribution shift? Confidence
rating based on which findings converge.

## Pass Criteria

* Generator deterministic: 100 random `(params, seed)` pairs produce byte-identical NEURON
  section dumps when re-run.
* 60 / 60 morphologies (30 different + 30 similar) build successfully and pass the 50 ms
  no-stim stability check.
* "Different" set covers visibly distinct morphology classes when laid out in
  `morphology_grid_different.png`.
* "Similar" set produces tight clusters in morphometric PCA (cluster radius <= 10 percent of
  PC1-PC2 axis range).
* Bed-B reproducibility: 5 / 5 t0083 Pareto cells reproduce DSI / PD within 5 percent.
* All 3 validation suggestions produce concrete answers with quantitative verdicts.

**Acceptable negative**: if the Bed-B reproducibility check fails, fall back to the TREES
toolbox (Cuntz 2010) for the generator. If 60 / 60 morphologies do not all simulate cleanly,
the generator's parameter ranges are too wide; tighten before t0091.

## Compute and Budget

* **Local 64-core EPYC** for Phases B, C, D, E, F (generation and verification simulations).
* **No remote machine for t0090 Phases A-F**.
* **Vast.ai EPYC 7B13** optional for Phase G.2 (NMDA units calibration ablation, ~$0.30).

**Total estimated cost**: ~$0.30 (Phase G.2 only). Buffer remaining after t0090: ~$4.14.

## Time Estimation

* Phase A (generator implementation): 1.5-2 days local
* Phase B (30 different): seconds
* Phase C (30 similar): seconds
* Phase D (verification sims): ~5-10 min on 64 cores
* Phase E (visualisation): ~1 hour
* Phase F (Bed-B reproducibility): ~1 hour
* Phase G (validation bundle): ~3-4 hours total

**Total wall-clock**: ~3-4 days.

## Expected Assets

* **Library asset**: the procedural DSGC morphology generator (`expected_assets["library"] =
  1`)
* **Answer asset**: validation-triplet biological-plausibility synthesis
  (`expected_assets["answer"] = 1`)

## Risks and Fallbacks

* **Generator implementation slips beyond 3 days**: fall back to TREES toolbox (Cuntz 2010)
  with asymmetry knobs added post-hoc.
* **Some morphologies fail to simulate**: mark them in the `verification_summary.json`,
  exclude from the warm-start anchor archive for t0091, narrow the LHS bounds for the next
  run.
* **Bed-B reproducibility outside 5 percent**: investigate before t0091; the generator may
  need a diameter-taper correction or an axial connectivity fix.
* **NMDA units calibration shows the Sivyer 2013 prior is correctly applied (no units bug)**:
  the
  >=85 sigma exotic verdict is genuine, motivating S-0086-01 (NSGA-II re-run with tightened NMDA
  bounds) as a higher-priority follow-up after t0091.

## Verification Criteria

* All unit tests pass (`uv run pytest tasks/t0090_morphology_generator_diversity_test/code/`).
* `verify_logs.py t0090_morphology_generator_diversity_test` passes.
* `verify_task_file.py t0090_morphology_generator_diversity_test` passes.
* `verify_research_code.py`, `verify_plan.py`, `verify_assets.py` pass.
* The answer asset passes `verify_answer.py`.

## Cross-References

* **t0089_brainstorm_results_18** — commissioning brainstorm session.
* **t0086_robustness_cluster_bio_comparison**, **t0088_recluster_marginals_and_vm_motifs** —
  biological-plausibility framework re-used for cluster scoring.
* **t0024_port_de_rosenroll_2026_dsgc** — Bed B reference for reproducibility check.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**, **t0083_bedb_v3_extend_nsga2_gen8plus** —
  source of the 5 t0083 Pareto cells used in Phase F and the cluster representatives used in
  Phase G.3.
* Source suggestions covered: **S-0088-02** (Phase G.1), **S-0086-02** (Phase G.2),
  **S-0088-01** (Phase G.3).

**Results summary:**

> **Results Summary: Procedural DSGC Morphology Generator + Diversity Test + Validation
> Bundle**
>
> **Summary**
>
> Delivered a deterministic 14-knob procedural DSGC morphology generator (library asset
> `procedural_dsgc_morphology_generator`) plus a 60-morphology diversity sweep, a Phase G
> validation
> triplet (G.1 done, G.2 / G.3 partial), and the
> `validation-triplet-implications-for-biological-plausibility` answer asset. **13/16 REQs
> done, 3
> partial** — partial REQs (REQ-9 Bed-B reproducibility, REQ-11 G.2 NMDA calibration, REQ-12
> G.3 NaP
> knockout) all share the same root cause: the procedural Bed-B-equivalent cell paired with
> the t0083
> best-cell channel set is silent (DSI=0), so the downstream simulations cannot produce
> informative
> deltas. Drivers and infrastructure are committed for all phases; a follow-up correction task
> should
> retune `BEDB_BASE_POINT` so the procedural cell elicits spikes under the t0083 channel set
> before
> re-running F / G.2 / G.3.
>
> **Metrics**
>
> * **Generator unit tests**: **9 / 9** passing (`uv run pytest tasks/t0090_.../code/`).
> * **Different-set verification stability**: **6 / 30** STABLE (24/30 NAN_VOLTAGE; consistent
>   with
> Mainen 1996 morphology-determines-firing-pattern when applying a fixed channel set to
> morphologies

</details>

<details>
<summary>✅ 0089 — <strong>Brainstorm results session 18</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0089_brainstorm_results_18` |
| **Status** | completed |
| **Effective date** | 2026-05-07 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md), [`t0073_brainstorm_results_12`](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0077_brainstorm_results_13`](../../../overview/tasks/task_pages/t0077_brainstorm_results_13.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0079_brainstorm_results_14`](../../../overview/tasks/task_pages/t0079_brainstorm_results_14.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0082_brainstorm_results_15`](../../../overview/tasks/task_pages/t0082_brainstorm_results_15.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md), [`t0085_brainstorm_results_16`](../../../overview/tasks/task_pages/t0085_brainstorm_results_16.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0087_brainstorm_results_17`](../../../overview/tasks/task_pages/t0087_brainstorm_results_17.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-07T10:00:00Z |
| **End time** | 2026-05-07T11:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 18](../../../overview/tasks/task_pages/t0089_brainstorm_results_18.md) |
| **Task folder** | [`t0089_brainstorm_results_18/`](../../../tasks/t0089_brainstorm_results_18/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0089_brainstorm_results_18/results/results_detailed.md) |

# Brainstorm Session 18: Strategic pivot to morphology-extended optimisation

Eighteenth brainstorming session. Run on 2026-05-07 after t0088
(`recluster_marginals_and_vm_motifs`) extended t0086's biological-plausibility analysis to a
13-cell pool (6 Genuine + 7 Marginal), confirmed `shared_mechanism_different_scale` across all
4 clusters (NaP-dominant in PD-minus-ND attribution at 87.4-99.7%, NMDA frac 0.000), and
surfaced a new extreme prior violation (Cluster 1 AIS-to-soma Nav ratio 116x = +33 sigma above
Werginz 2024). Project spend $15.56 / $20.00; **$4.44 remaining**.

The researcher's directive was a strategic pivot: "Optimisation technique seems to work. We
now need to add a big and important part of cells - cell morphology." After two iterations on
parametrisation strategy, the agreed approach is a **procedural DSGC morphology generator with
14 explicit knobs** covering topology, asymmetry, and geometry, called inside the NSGA-II
evaluation loop.

## Decisions

* **Create t0090** -- procedural DSGC morphology generator + 30-different + 30-similar
  diversity test + Bed-B reproducibility check + validation bundle. Phases:

  * **Phase A (generator implementation)**: implement procedural generator in Python that
    takes 14 morphology parameters plus a `morph_seed` and emits NEURON sections +
    connectivity. Parameters: 5 topology (`num_primary_branches` 3-7, `branch_prob_per_um`
    0.005-0.05, `max_strahler_depth` 2-6, `mean_branching_angle_deg` 30-90, `rall_exponent`
    0.5-2.0); 4 asymmetry (`soma_offset_pd_um` -150 to +150, `field_elongation_pd` 1.0-3.0,
    `branch_density_gradient_pd` -1 to +1, `primary_branch_pd_concentration` 0-5 von Mises
    kappa); 3 geometry (`mean_segment_length_um` 10-60, `soma_diameter_um` 8-18,
    `ais_length_um` 15-60); 2 stochastic control (`morph_seed`, `branch_length_cv` 0-0.5).
    Deterministic given (`params`, `seed`).

  * **Phase B (30 very-different morphologies)**: wide Latin Hypercube sample over the 14-d
    morph param space; generate in parallel on 64-core EPYC.

  * **Phase C (30 very-similar morphologies)**: tight perturbations (+/- 5%) around a
    Bed-B-equivalent base point; generate in parallel.

  * **Phase D (verification simulation)**: build each morphology in NEURON, run a 50 ms
    no-stim stability check + 8-direction bar protocol with default t0083 best-cell channels;
    catch degenerate geometries (NaN, divergence, disconnected sections). Parallelise on 64
    cores.

  * **Phase E (visualisation)**: 2D dendrograms for all 60 morphologies, PCA / UMAP of
    morphometric features (total dendritic length, branch count, electrotonic length, soma
    displacement, max Strahler depth); side-by-side panels of 30-different vs 30-similar so
    the diversity coverage is visually obvious.

  * **Phase F (Bed-B reproducibility)**: pick a `morph_params` point that approximates de
    Rosenroll 2026 / Bed B; run 5 t0083 Pareto cells through the generator at that point;
    confirm DSI / PD within 5% of original Bed B.

  * **Phase G (validation bundle)**: bundle three cheap validation suggestions that sharpen
    biological interpretation in t0091. (1) **S-0088-02** AIS-to-soma Nav ratio audit (cluster
    1's 116x is suspicious; 30 min, $0). (2) **S-0086-02** NMDA units calibration ablation (1
    hour, ~$0.30). (3) **S-0088-01** causal NaP-knockout per cluster representative (4 cells x
    16 dirs; ~64 min, $0).

  **Pass criteria**: generator deterministic; 60 / 60 morphologies simulate without errors;
  "different" set covers visibly distinct morphology classes; "similar" set produces tight
  clusters in morphometric PCA; Bed-B reproducibility within 5%; all 3 validation suggestions
  answered.

  **Output**: validated generator library + a curated warm-start anchor archive of viable
  diverse morphologies for t0091. **Cost ~$0.30, ~3-4 days wall-clock, mostly local 64-core
  CPU.**

  Source suggestions: covers S-0088-02, S-0086-02, S-0088-01 in Phase G; t0090 is otherwise a
  new direction with no source suggestion. Dependencies: t0024, t0078, t0080, t0081, t0083,
  t0086, t0088. `expected_assets = {"library": 1, "answer": 1}`. Task types:
  `["library-implementation", "data-analysis", "answer-question"]`.

* **Create t0091** -- first joint 68-d NSGA-II optimisation with morphology generated inside
  the evaluation loop, warm-started from 5 distinct morphology anchor points. Phases:

  * **Phase A (warm-start population)**: build pop 96 from 5 anchors x ~19 t0083 Pareto
    electrophys variants each. Anchors: (1) **Bed-B-like** (matches existing t0083 substrate);
    (2) **symmetric** (`soma_offset_pd_um=0`, `field_elongation_pd=1.0`,
    `branch_density_gradient_pd=0`, `primary_branch_pd_concentration=0`); (3)
    **PD-asymmetric** (soma offset +100 um toward PD, field elongated 2x along PD, branches
    biased toward PD); (4) **ND-asymmetric** mirror of #3; (5) **alternative-topology** (more
    primary branches, deeper Strahler depth, smaller field).

  * **Phase B (joint NSGA-II)**: pop 96, <=8 generations, generator inside eval loop; adaptive
    HV-plateau stop + cost watchdog (post-S-0083-04 fix). On Vast.ai EPYC 7B13 64-core. Each
    evaluation: NSGA-II proposes 68-d vector -> generator builds NEURON model from 14 morph
    params + morph_seed -> 54 channel/synapse params inserted into generated sections ->
    bar-rotation simulation -> objectives returned (DSI, PD firing rate, robustness).

  * **Phase C (Pareto + biological-plausibility analysis)**: extend t0086 / t0088 framework to
    68-d cells; do morph-extended Pareto cells reach biologically-plausible NMDA / NaP regimes
    that 54-d cells could not?

  * **Phase D (anchor-tracking analysis)**: which of the 5 anchors are over- vs
    under-represented in the final Pareto? If anchor #3 (PD-asymmetric) is preserved more than
    anchor #4 (ND-asymmetric), that is strong evidence for soma-displacement-toward-PD as a
    functional DS mechanism (Schachter 2010, Trenholm 2013).

  * **Phase E (answer asset)**: "Does in-loop morphology optimisation open
    biologically-plausible joint-pass regions, and which morphological asymmetries does the
    optimiser favour?"

  **Pass criteria**: Phase B converges with HV plateau or 8-gen cap; Phase C extends t0086
  framework cleanly; Phase D produces a definitive yes/no on whether morphology variation
  reaches biologically plausible cells; anchor-tracking yields a clear PD-vs-ND asymmetry
  verdict. **Acceptable negative**: optimiser pegs all anchors back toward Bed-B-like ->
  conclusion is the v3 substrate's biological-plausibility ceiling is not raised by this
  morphology parametrisation, motivating Option G (NeuroMorpho real-cell library) in a future
  task.

  **Cost ~$3.00-3.50, ~14-16 hours Vast.ai. Buffer remaining ~$0.94-1.44.**

  Source suggestions: none directly (new direction). Dependencies: t0024, t0078, t0080, t0081,
  t0083, t0086, t0088, t0090. `expected_assets = {"answer": 1, "predictions": 1}`. Task types:
  `["experiment-run", "data-analysis", "answer-question"]`.

## Suggestion Cleanup

### Rejected (covered by new tasks)

* **S-0086-02** (NMDA units calibration) -- covered by t0090 Phase G.
* **S-0088-01** (causal NaP-knockout per cluster representative) -- covered by t0090 Phase G.
* **S-0088-02** (AIS-to-soma Nav ratio audit) -- covered by t0090 Phase G.
* **S-0084-05** (channel-knockout DSI causal-attribution variant) -- duplicate of S-0088-01
  (which itself is now covered by t0090 Phase G).
* **S-0083-03** (per-direction Vm-trace deep-dive of cell 1304) -- covered by t0088 (cell 1304
  is a member of cluster 1 with representative cell 1634; mechanism attribution NaP 87.4% /
  Nav1.6 12.6% / NMDA 0.0% applies to all cluster-1 cells including 1304).

### Reprioritised (high -> medium)

* **S-0083-01** (extend NSGA-II from t0083 gen 17 to gen 25 with pop 144) -- estimated $8-12,
  out of remaining $4.44 budget; superseded by the morphology-extended NSGA-II direction in
  t0091.
* **S-0084-01** (NaP density sweep on cells 767 / 637 / 762) -- superseded by S-0088-01-style
  binary knockout in t0090 Phase G; older single-cell scope.
* **S-0084-02** (per-seed mechanism decomposition of cell 767) -- older single-cell scope;
  mechanism attribution at population level already established by t0088.

### Stays high

* **S-0086-01** (NSGA-II re-run with tightened NMDA bounds, $1.50) -- natural follow-up after
  t0091; if t0091 finds biologically plausible joint-pass cells under morphology variation,
  may also benefit from tightened-bounds variant.
* **S-0070-01** (harmonise PD / ND encoding across Bed A and Bed B) -- independent infra; not
  affected by morphology direction.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.

## Assets Produced

No assets in this brainstorm task. The new tasks t0090 and t0091 will produce: t0090 a
morphology generator library + a mechanism-distinctness answer asset; t0091 a Pareto-front
predictions asset + an answer asset on morphology-extended biological plausibility.

## Budget Context

Project budget $20.00; **$15.56 spent** before t0090 / t0091; **$4.44 remaining**. t0090
estimated **$0.30** (validation bundle in Phase G). t0091 estimated **$3.00-3.50** (Vast.ai
EPYC 7B13). Buffer remaining after both: **$0.94-1.44**.

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0089_brainstorm_results_18"
> date_completed: "2026-05-07"
> status: "complete"
> ---
> **Results Summary: Brainstorm Session 18**
>
> **Summary**
>
> Eighteenth strategic brainstorm, run on 2026-05-07 after t0088
> (`recluster_marginals_and_vm_motifs`)
> extended t0086's biological-plausibility analysis to a 13-cell pool and confirmed
> `shared_mechanism_different_scale` across 4 clusters (all NaP-dominant in PD-minus-ND
> attribution).
> The researcher's strategic directive was a pivot from electrophys-only optimisation
> (t0080-t0088) to
> **morphology-extended optimisation**: "Optimisation technique seems to work. We now need to
> add a
> big and important part of cells - cell morphology." After four iterations on parametrisation
> strategy, the agreed approach is a procedural DSGC morphology generator with 14 explicit
> knobs
> spanning topology + asymmetry + geometry, called inside the NSGA-II evaluation loop. The
> work is
> split into two tasks: t0090 (`morphology_generator_diversity_test`, ~$0.30, ~3-4 days local)
> builds
> and validates the generator with 30 different + 30 similar morphologies and bundles three
> validation

</details>

## 2026-05-06 (5)

## ✅ Completed

<details>
<summary>✅ 0088 — <strong>Re-cluster t0086 13 cells and per-cluster Vm-trace
deep-dive</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0088_recluster_marginals_and_vm_motifs` |
| **Status** | completed |
| **Effective date** | 2026-05-06 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0086-03` |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/), [`experiment-run`](../../../meta/task_types/experiment-run/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-06T19:40:18Z |
| **End time** | 2026-05-06T21:10:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Re-cluster t0086 13 cells and per-cluster Vm-trace deep-dive](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Task folder** | [`t0088_recluster_marginals_and_vm_motifs/`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0088_recluster_marginals_and_vm_motifs/results/results_detailed.md) |

# Re-cluster t0086 Genuine + Marginal cells and per-cluster Vm-trace deep-dive (S-0086-03 extension)

## Motivation

t0086 found k=2 clusters on the 6 Genuine cells with both clusters classified exotic by the
biological scorecard (NMDA per-synapse +85-122 sigma above Sivyer 2013, NaP +7-24 sigma above
Stuart 1999). This raises two questions that S-0086-03 set out to address: (a) do different
cells inside each cluster share a common biophysical mechanism (e.g., NaP-dominant vs
NMDA-dominant), or do they all use the same mechanism but at different scales; (b) do clusters
partition cells by mechanism. The original S-0086-03 scope ran the deep-dive on the 6 Genuine
cells only; this extension adds the 7 Marginal cells from t0086 (cells 767, 1304, 1379, 1504,
1559, 1624, 1721) for a 13-cell re-clustering pool, then deep-dives at higher angular
resolution (16 directions every 22.5 deg) on a representative cell per cluster. The wider
13-cell pool reveals mechanism heterogeneity that the 6-Genuine-only clustering may miss, and
the 16-direction resolution exceeds t0084's 8-direction deep-dive.

The combined task design follows the recorded researcher preference for one consolidated task
bundling related suggestions and infra/protocol fixes. Source suggestion: **S-0086-03**
(extended scope).

## Cell Set

13 cells from t0086:

* **6 Genuine** (t0086 5/5 reps pass DSI >= 0.4 AND PD >= 10 Hz): 1517, 1604, 1634, 1639,
  1663, 1677
* **7 Marginal** (t0086 3-4/5 reps pass): 767, 1304, 1379, 1504, 1559, 1624, 1721

Cell 767's 54-d natural-unit parameter vector lives in
`tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` (the warm-start
lineage). Cells 1238-1727 (which include all 12 of the remaining 13-cell pool) live in
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json`. The
implementation must verify which task contains each cell's saved parameters before loading.

## Scope

### Phase A -- Re-cluster 13 cells

* Load `tasks/t0086_robustness_cluster_bio_comparison/results/data/cell_classification.json`
  to identify the 6 Genuine + 7 Marginal cells.
* Load 54-d natural-unit parameter vectors per cell from t0081 / t0083 `all_evaluations.json`.
* Re-run KMeans for k = 2..6, hierarchical clustering with ward linkage and both cosine +
  euclidean metrics, and 2D visualisation via UMAP (or PCA fallback if UMAP fit fails).
* Pick best k via silhouette + BIC.
* Compute per-cluster centroids in 54-d natural-unit space.
* Re-use `tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py` and
  `biological_scorecard.py` to score each new cluster centroid against published priors (Kole
  2008 AIS Nav, Werginz 2024 mouse alpha-RGC AIS-to-soma Nav ratio, Sivyer 2013 dendritic
  NMDA, Oesch 2005 + Goldfinger 2000 + Stuart 1999 distal Nav1.6 / NaP, de Rosenroll 2026 GABA
  / AMPA spatial distribution, Branco-Hausser 2010 NMDA Mg-block).
* Output: `results/data/recluster_assignments.json`, `results/data/recluster_centroids.json`,
  `results/data/recluster_biological_scorecard.json`. Plus PNGs: cluster UMAP / silhouette /
  dendrogram / heatmap, matching t0086's plotting style.

### Phase B -- Per-cluster Vm-trace deep-dive

* For each cluster, pick a representative cell as the cell with minimum 54-d Euclidean
  distance to the cluster centroid.

* For each representative cell, run a t0084-style deep-dive at **16 directions** (every 22.5
  deg) instead of t0084's 8 directions. Use 1 inner replication per direction.

* Re-use t0084's `run_deepdive.py` per-segment recording pattern. Record per-segment Vm at
  proximal soma, mid-dendrite, distal-dendrite, AIS; per-segment NMDA conductance trajectories
  (`gnmda` over time at each `bundle.syns_nmda` synapse, distal dendrite); per-segment Nav1.6
  (`nav16t80._ref_i`) and NaP (`napt80._ref_i`) currents at distal dendrite; AIS Vm and
  threshold-crossing spike onset times.

* Per representative cell, generate 4 figures matching t0084:

  1. Per-direction Vm traces (3-row x 16-column grid: proximal soma / mid dendrite / distal
     dendrite)
  2. NMDA conductance trajectories at distal dendrite per direction (16-line plot)
  3. Nav1.6 / NaP current decomposition at distal dendrite per direction (16-direction
     subplots)
  4. AIS spike onset histogram per direction (polar or 16-bin bar)

* Compute fractional channel contributions per cluster representative (matching t0084's
  `attribution_metric.py` pattern but applied to the new cells).

### Phase C -- Mechanism distinctness analysis

* Compare fractional contributions across clusters: do different clusters use different
  dominant mechanisms (e.g., one NMDA-dominant, one NaP-dominant, one Nav1.6-dominant), or do
  they all share the same mechanism but vary in scale?
* Compare to t0084's cell 767 attribution (NaP-dominant 93%, Nav1.6 7%, NMDA 0%): does the
  per-seed re-evaluation reveal mechanism heterogeneity that single-seed attribution missed?
* Per-cluster narrative: which biophysical strategy does this cluster represent?

### Output

Answer asset at `assets/answer/are-cluster-motifs-mechanistically-distinct/` per the answer
asset specification (`meta/asset_types/answer/specification.md`), with quantitative
attribution per cluster.

## Pass criteria

* **Primary**: produce a clear mechanism-distinctness verdict (clusters are mechanistically
  distinct vs share the same mechanism).
* **Secondary**: per-cluster representative Vm-trace deep-dive figures published.
* **Acceptable negative**: clusters are NOT mechanistically distinct (all use the same
  NMDA-dominant strategy, differing only in parameter scale) is itself a useful finding
  aligning with t0086's exotic-NMDA verdict.

## Compute and Budget

* Phase A: pure data analysis, $0, ~10 min.
* Phase B: per representative cell at 16 directions x 1 inner replication = 16 NEURON sims at
  ~60 s each per cell = ~16 min per cell. With 2-3 cluster representatives = 32-48 min total
  local CPU.
* Phase C: data analysis, $0.

**Local CPU only. No remote machine. Total wall-clock ~1-2 hours, $0 cost.** No remote-machine
provisioning or Vast.ai authentication required.

Project budget after t0086: ~$15.56 / $20.00 used, ~$4.44 remaining. t0088 estimated $0 -- no
budget impact.

## Dependencies

* **t0024_port_de_rosenroll_2026_dsgc** -- the de Rosenroll 2026 base port that defines the
  model substrate.
* **t0078_bedb_mobo_v2_ais_tiered_ahp** -- the v2 substrate predecessor.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** -- the v3 substrate library (active dendritic
  conductances + tiered AHP) used for re-evaluation.
* **t0081_bedb_v3_warmstart_nsga2** -- contains cell 767's 54-d parameter vector in
  `results/data/all_evaluations.json`.
* **t0083_bedb_v3_extend_nsga2_gen8plus** -- contains the 12 remaining cells' 54-d parameter
  vectors in `results/data/all_evaluations.json`.
* **t0084_t0081_cell_767_vm_trace_deepdive** -- contains `code/run_deepdive.py` and the
  per-segment recording pattern this task re-uses.
* **t0086_robustness_cluster_bio_comparison** -- contains `code/biological_priors.py`,
  `biological_scorecard.py`, the cell classification, and the original 6-Genuine clustering
  this task extends.

## Cross-task code reuse

Per the cross-task import rule (no direct imports across task folders; only library asset
imports), this task copies the needed code into its own `code/` directory:

* Copy `tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py` and
  `biological_scorecard.py` into `tasks/t0088_recluster_marginals_and_vm_motifs/code/`,
  rebinding imports.
* Copy `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/run_deepdive.py` (or equivalent)
  per-segment recording pattern into `tasks/t0088_recluster_marginals_and_vm_motifs/code/`,
  rebinding imports.

The library asset `de_rosenroll_2026_dsgc_ais_dendritic_spike` (the v3 substrate from t0080)
is imported normally.

## Expected Assets

`expected_assets = {"answer": 1}`. The single answer asset at
`assets/answer/are-cluster-motifs-mechanistically-distinct/` per the answer-asset
specification.

## Task Types

`["data-analysis", "experiment-run", "answer-question"]`. Phase A is data-analysis (Pandas /
sklearn / matplotlib); Phase B is experiment-run (NEURON simulations local CPU); Phase C
produces the answer asset.

## Output specification

* `results/data/recluster_assignments.json`: per-cell cluster id (Phase A).
* `results/data/recluster_centroids.json`: cluster centroids in 54-d natural-unit space (Phase
  A).
* `results/data/recluster_biological_scorecard.json`: per-cluster biological-plausibility
  scorecard (Phase A).
* `results/data/representative_cells.json`: which cell represents each cluster (Phase B).
* `results/data/per_direction_recordings_<cell_id>.npz`: per-segment Vm + NMDA + Nav1.6 + NaP
  recordings per direction per representative cell (Phase B).
* `results/data/attribution_<cell_id>.json`: fractional channel contributions per
  representative cell (Phase B).
* `results/data/mechanism_distinctness.json`: per-cluster mechanism narrative + verdict (Phase
  C).
* `results/images/cluster_umap.png`, `cluster_silhouette.png`, `cluster_dendrogram.png`,
  `cluster_heatmap.png` (Phase A).
* `results/images/vm_traces_<cell_id>.png`, `nmda_conductance_<cell_id>.png`,
  `nav_decomp_<cell_id>.png`, `ais_spike_onset_<cell_id>.png` per representative cell (Phase
  B).
* `assets/answer/are-cluster-motifs-mechanistically-distinct/{details.json, short_answer.md,
  full_answer.md}` (Phase C).

## Concrete questions answered

1. How many clusters does the 13-cell pool partition into (vs t0086's k=2 on 6 cells)?
2. What is the per-cluster fractional channel attribution at 16 directions?
3. Are the clusters mechanistically distinct, or do they share a mechanism with
   parameter-scale variation?
4. Does cell 767's NaP-dominant attribution from t0084 (single-seed 8 directions) hold up at
   16-direction resolution and after re-clustering with the 13-cell pool?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0088_recluster_marginals_and_vm_motifs"
> date_completed: "2026-05-06"
> ---
> **Results Summary -- t0088_recluster_marginals_and_vm_motifs**
>
> **Summary**
>
> Re-clustered the 13-cell pool of 6 Genuine + 7 Marginal cells from t0086 in the t0080 54-d
> v3
> parameter space; KMeans + silhouette selected **best_k = 4 clusters**. Ran a t0084-style
> Vm-trace
> deep-dive at 16 directions on the 4 representative cells (1604, 1634, 767, 1639) on local
> CPU, all
> 64 simulations stable. **Mechanism-distinctness verdict =
> `shared_mechanism_different_scale`**: all
> 4 cluster representatives are NaP-dominant in PD-minus-ND attribution (frac NaP 0.874-0.997,
> frac
> Nav1.6 0.003-0.126, frac NMDA = 0.000); clusters differ in parameter scale within 54-d space
> but not
> in which channel drives the PD response. This extends t0084's NaP-dominant cell 767 finding
> from a
> single cell at 8 directions to four representative cells at 16 directions and confirms the
> v3
> substrate's joint-pass / near-joint-pass cells systematically rely on NaP-driven sustained
> dendritic
> depolarisation. All 4 clusters classified exotic by the biological scorecard (extending
> t0086's
> exotic-NMDA verdict to the 13-cell pool).

</details>

<details>
<summary>✅ 0087 — <strong>Brainstorm results session 17</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0087_brainstorm_results_17` |
| **Status** | completed |
| **Effective date** | 2026-05-06 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md), [`t0073_brainstorm_results_12`](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0077_brainstorm_results_13`](../../../overview/tasks/task_pages/t0077_brainstorm_results_13.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0079_brainstorm_results_14`](../../../overview/tasks/task_pages/t0079_brainstorm_results_14.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0082_brainstorm_results_15`](../../../overview/tasks/task_pages/t0082_brainstorm_results_15.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md), [`t0085_brainstorm_results_16`](../../../overview/tasks/task_pages/t0085_brainstorm_results_16.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-06T11:00:00Z |
| **End time** | 2026-05-06T11:50:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 17](../../../overview/tasks/task_pages/t0087_brainstorm_results_17.md) |
| **Task folder** | [`t0087_brainstorm_results_17/`](../../../tasks/t0087_brainstorm_results_17/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0087_brainstorm_results_17/results/results_detailed.md) |

# Brainstorm Session 17: Re-cluster t0086 Genuine + Marginal cells and per-cluster Vm-trace deep-dive

Seventeenth brainstorming session. Run on 2026-05-06 after t0086
(`robustness_cluster_bio_comparison`) classified the 20-cell test set as 6 Genuine + 7
Marginal + 7 Stochastic, k=2 clusters on the 6 Genuine cells, both clusters exotic (NMDA
per-synapse +85-122 sigma above Sivyer 2013, NaP +7-24 sigma above Stuart 1999), AIS-Nav
ratios 11.5-30.5 (one cluster plausible, the other +4 sigma above Werginz 2024). Project spend
reached **$15.56 / $20.00**; **$4.44 remaining**.

The session is one-shot per the researcher's verbatim directive: extend S-0086-03's
per-cluster Vm-trace deep-dive to a wider cell pool by re-doing clustering with the 7 Marginal
cells included alongside the 6 Genuine cells (13 cells total instead of 6), so the new
clustering rests on a larger, mechanistically heterogeneous pool, and the per-cluster Vm-trace
deep-dive is performed on representatives from the new clusters at higher angular resolution
(16 directions instead of t0084's 8). All in one task.

## Decisions

* **Create t0088** -- `recluster_marginals_and_vm_motifs`. Three sequential phases:

  * **Phase A (re-cluster 13 cells)**: load the 6 Genuine + 7 Marginal cells from t0086's
    `cell_classification.json`. Total 13 cells: `[767, 1304, 1379, 1504, 1517, 1559, 1604,
    1624, 1634, 1639, 1663, 1677, 1721]`. Load their 54-d natural-unit parameter vectors from
    t0083's `all_evaluations.json` (cells 1238-1727) and t0081's `all_evaluations.json` (cell
    767's warm-start parameters). Re-run KMeans k=2..6, hierarchical (ward + cosine +
    euclidean), UMAP/PCA visualisation; pick best k via silhouette + BIC. Compute per-cluster
    centroids in 54-d natural-unit space. Re-use t0086's `biological_priors.py` and
    `biological_scorecard.py` to score each new centroid against published priors (Kole 2008,
    Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005, Goldfinger 2000, Stuart 1999,
    de Rosenroll 2026).

  * **Phase B (per-cluster Vm-trace deep-dive)**: pick a representative cell per cluster
    (closest to centroid in 54-d Euclidean distance among cells assigned to that cluster). Run
    a t0084-style deep-dive at higher angular resolution: **16 directions** (every 22.5 deg).
    Record per-segment Vm at proximal soma, mid-dendrite, distal-dendrite, AIS; per-segment
    NMDA conductance trajectories; per-segment Nav1.6 (`nav16t80._ref_i`) and NaP
    (`napt80._ref_i`) currents at distal dendrite; AIS Vm and threshold-crossing spike onset
    times. Per representative, generate 4 figures matching t0084: per-direction Vm traces
    (3-row x 16-column grid: proximal soma / mid dendrite / distal dendrite); NMDA conductance
    trajectories at distal dendrite; Nav1.6 / NaP current decomposition; AIS spike onset
    histogram. Compute fractional channel contributions per cluster representative.

  * **Phase C (mechanism distinctness analysis)**: compare fractional contributions across
    clusters; do different clusters use different dominant mechanisms (e.g., one
    NMDA-dominant, one NaP-dominant, one Nav1.6-dominant), or do they all share the same
    mechanism but vary in scale? Compare to t0084's cell 767 attribution (NaP-dominant 93%,
    Nav1.6 7%, NMDA 0%). Per-cluster narrative: which biophysical strategy does this cluster
    represent?

  Output: one **answer asset** at `assets/answer/are-cluster-motifs-mechanistically-distinct/`
  per the answer-asset specification, with quantitative attribution per cluster.

  **Pass criteria**: Primary -- produce a clear mechanism-distinctness verdict (clusters are
  mechanistically distinct vs share the same mechanism). Secondary -- per-cluster
  representative Vm-trace deep-dive figures published. Acceptable negative -- clusters are NOT
  mechanistically distinct (all use the same NMDA-dominant strategy, differing only in
  parameter scale) is itself a useful finding aligning with t0086's exotic-NMDA verdict.

  **Compute**: Phase A pure data analysis ($0, ~10 min); Phase B per representative cell at 16
  directions x 1 inner replication = 16 NEURON sims at ~60 s each = ~16 min per cell; with 2-3
  cluster representatives = 32-48 min; Phase C analysis ($0). **Local CPU only. No remote
  machine. Total wall-clock ~1-2 hours, $0 cost.**

  Source suggestion: **S-0086-03** (extension scope). Dependencies: t0024, t0078, t0080,
  t0081, t0083, t0084, t0086. `expected_assets = {"answer": 1}`. Task types:
  `["data-analysis", "experiment-run", "answer-question"]`.

## Suggestion Cleanup

* **Reject S-0086-03** -- t0088 covers the per-cluster Vm-trace deep-dive with extended scope
  (13 cells re-clustered, 16 directions instead of t0084's 8, mechanism-distinctness narrative
  as the answer asset). The original S-0086-03 scope (deep-dive on 6 Genuine cells only at 24
  directions remote-CPU) is subsumed by t0088's extended scope; t0088 picks 16 directions for
  local-CPU feasibility.

## Reprioritisations

None.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued.

## Assets Produced

No assets in this brainstorm task. The new task t0088 will produce one answer asset
attributing each re-clustered cluster to a dominant biophysical mechanism (or, in the negative
case, confirming a shared mechanism with parameter-scale variation).

## Budget Context

Project budget $20.00; **$15.56 spent** before t0088; **$4.44 remaining**. t0088 is local-CPU
only and estimated **$0.00**, leaving the **$4.44 buffer intact** for subsequent S-0086-*
follow-ups (notably S-0086-01 NSGA-II re-run with tightened NMDA bounds at $1.50, S-0086-02
NMDA units calibration at $0.30, S-0086-04 10-rep robustness extension at $0.65, S-0086-06 Bed
A cross-bed validation at $2.50).

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0087_brainstorm_results_17"
> date_completed: "2026-05-06"
> status: "complete"
> ---
> **Results Summary: Brainstorm Session 17**
>
> **Summary**
>
> Seventeenth strategic brainstorm, run on 2026-05-06 after t0086
> (`robustness_cluster_bio_comparison`) classified the 20-cell test set as 6 Genuine + 7
> Marginal + 7
> Stochastic, found k=2 clusters on the 6 Genuine cells, both clusters classified exotic by
> the
> biological scorecard (NMDA per-synapse +85-122 sigma above Sivyer 2013, NaP +7-24 sigma
> above Stuart
> 1999). One consolidated follow-up task commissioned: t0088
> (`recluster_marginals_and_vm_motifs`)
> extends S-0086-03's per-cluster Vm-trace deep-dive scope by re-clustering the 13-cell pool
> of 6
> Genuine + 7 Marginal cells (instead of 6 Genuine cells only), then runs a t0084-style
> deep-dive at
> 16 directions on local CPU on representative cells, computes fractional channel attribution
> per
> cluster, and produces one mechanism-distinctness answer asset. S-0086-03 rejected as
> covered.
> Project budget $20.00; $15.56 spent before t0088; **$4.44 remaining**; t0088 estimated $0
> (local-CPU

</details>

<details>
<summary>✅ 0086 — <strong>Robustness + cluster + bio-comparison of t0081/t0083
joint-pass cells</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0086_robustness_cluster_bio_comparison` |
| **Status** | completed |
| **Effective date** | 2026-05-06 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0083-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-06T13:03:09Z |
| **End time** | 2026-05-06T18:24:00Z |
| **Step progress** | 12/15 |
| **Task page** | [Robustness + cluster + bio-comparison of t0081/t0083 joint-pass cells](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Task folder** | [`t0086_robustness_cluster_bio_comparison/`](../../../tasks/t0086_robustness_cluster_bio_comparison/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0086_robustness_cluster_bio_comparison/results/results_detailed.md) |

# Robustness Validation and Parameter-Cluster + Biological-Plausibility Analysis of t0083 Joint-Pass Cells

## Motivation

t0083 (`bedb_v3_extend_nsga2_gen8plus`) extended t0081's NSGA-II from gen 7 through gen 17 and
**expanded the joint-pass cell population from 1 to 15 cells** (1 inherited from t0081 cell
767 + 14 new in gens 13-17), with 3 of those 15 lying on the final 18-cell Pareto front
(highest-DSI cell 1304 at DSI 0.7652 / PD 13.96 Hz). Hypervolume grew +118% from gen 7
(16.330) to gen 17 (35.576). t0084 attributed cell 767's DSI improvement to specific
dendritic-spike machinery.

Three open questions follow naturally from t0083's expansion:

1. **Are the 15 joint-pass cells reproducible?** t0083's evaluation used 8 directions x 20
   seeds per cell. Cells that satisfy the joint pass on a single 160-sim evaluation may or may
   not reproduce under different RNG seeds. The AR(2) release noise + arrival jitter dominate
   the stochastic variance; some joint-pass cells may be artefacts of a lucky RNG draw.

2. **Are the 15 joint-pass cells distributed across distinct sub-regions of the 54-d parameter
   space, or do they cluster around a single mode?** t0083's Pareto front spans a wide range
   of DSI / PD values, suggesting the search is finding multiple distinct architectural
   strategies that each satisfy joint pass. Cluster analysis can identify these strategies and
   characterise the parameter envelope of each.

3. **Are the cluster centroids biologically plausible?** The published biological priors
   constrain key parameters (AIS Nav density per Kole 2008 / Werginz 2024; AIS-to-soma Nav
   ratio per Werginz 2024; dendritic NMDA conductance and Mg-block voff per Sivyer 2013 /
   Branco-Hausser 2010; distal Nav1.6 / NaP densities per Oesch 2005 / Goldfinger 2000 /
   Stuart 1999; GABA/AMPA spatial distribution per de Rosenroll 2026). A cluster whose
   centroid lies within +/-2 sigma of all key priors is "plausible"; one that lies +/-2-5
   sigma is "stretched"; one that lies >5 sigma is "exotic". The scorecard tells the project
   which strategies are biologically interpretable and which are model artefacts.

This task addresses project research question Q1 (which Na / K combinations max AP frequency
at PD with ND suppression) and Q4 (active vs passive dendrites enable joint pass) at a
**characterisation** level rather than a **discovery** level. It bundles three previously open
suggestions (S-0083-02 motif clustering, S-0083-05 multi-seed smoke gate, multi-replicate
aspect of S-0081-01) into a single combined pipeline. Source suggestion: **S-0083-02**.

## Scope

### In scope

* **Phase A -- Robustness validation.** Select 20 cells:
  * All 15 joint-pass cells: cell 767 from t0081 + the 14 t0083 cells with DSI >= 0.4 AND PD
    >= 10 Hz (read from
    `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` and
    `pareto_front.json`).
  * 5 closest near-pass cells from the t0083 Pareto front (`pareto_front.json`) by Euclidean
    distance to the (DSI 0.4, PD 10) joint corner among cells that do NOT satisfy joint-pass.
  * Re-evaluate each cell at **24 directions x 30 seeds = 720 sims per replication x 5 outer
    RNG seeds = 3,600 sims per cell**. Total: 100 cell-evaluations = 72,000 sims.
  * Outer RNG seed controls AR(2) release noise + arrival jitter. The 5 replications are
    pseudo-independent (different outer seeds; same parameter vector).
  * Compute mean +/- SD of DSI and PD per cell across the 5 replications.
  * Classify each cell:
    * **Genuine**: 5/5 replications joint-pass (DSI >= 0.4 AND PD >= 10 in every replication)
    * **Marginal**: 3-4/5 replications joint-pass
    * **Stochastic**: <=2/5 replications joint-pass

* **Phase B -- Cluster analysis on Genuine cells.**
  * k-means with k=2..6, k selected by silhouette score + BIC.
  * Hierarchical clustering with cosine and euclidean distance metrics for cross-validation.
  * UMAP and t-SNE 2D visualisation overlaid with k-means and hierarchical labels.
  * Per-cluster centroids + within/between cluster variance + cluster size.
  * Check cluster stability via 50-sample bootstrap (re-run k-means on subsamples of Genuine
    cells; report Adjusted Rand Index between bootstrap labels and full-sample labels).

* **Phase C -- Biological comparison.**
  * Per cluster centroid, score key parameters against published biological priors:
    * **AIS Nav density** vs Kole 2008 (0.25-0.5 S/cm^2 cortical pyramidal AIS) and Werginz
      2024 (1.3 S/cm^2 mouse alpha-RGC).
    * **AIS-to-soma Nav ratio** vs Werginz 2024 (17.3x).
    * **Dendritic NMDA conductance** and **Mg-block voff** vs Sivyer 2013, Branco-Hausser
      2010.
    * **Distal Nav1.6 / NaP densities** vs Oesch 2005, Goldfinger 2000, Stuart 1999.
    * **GABA/AMPA spatial distribution** vs de Rosenroll 2026.
  * Per parameter: report cluster centroid value, published mean +/- sigma, deviation in sigma
    units, and verdict (plausible / stretched / exotic).
  * Per cluster: aggregate verdict across all key parameters; flag the cluster as overall
    plausible / stretched / exotic.
  * Output: one **answer asset** at
    `assets/answer/cluster-biological-plausibility-attribution/` attributing each cluster to
    known biology or flagging as novel/unphysical.

* **Cost-watchdog rate-fix REQ-X (HARD requirement).** The cost watchdog MUST source
  per-instance hourly rate from `machine_log.json` `selected_offer.price_per_hour`, not from a
  hard-coded constant. This protocol fix is forced by t0083's $0.83 overrun ($5.83 actual vs
  $5.00 cap; in-loop watchdog used hard-coded $0.2382/hr but actual offer billed $0.3209/hr =
  1.347x). Document explicitly in `plan/plan.md` and verify in implementation review.

### Out of scope

* New cells outside the t0081 + t0083 union (no fresh NSGA-II generations).
* Substrate changes (no new dendritic-spike parameters; no new channels; no AIS modifications;
  no morphology changes).
* Different morphologies (deferred S-0081-01 follow-up).
* Different conductance density realisations (deferred S-0081-01 follow-up).
* Bed A cross-bed validation (S-0081-05; deferred to a later task).

## Pass Criteria

* **Primary**: at least one cluster of >=3 Genuine cells (3 cells, all 5/5 replications
  joint-pass) with all key biological parameters within +/-2 sigma of published priors.

* **Secondary**: identify which t0083 joint-pass cells are stochastic artefacts vs genuine --
  even if all clusters are exotic, the robustness classification is itself useful and can be
  used to reweight downstream NSGA-II warm-starts.

* **Acceptable negative**: zero Genuine clusters (all joint-pass cells turn out to be
  stochastic artefacts of lucky RNG draws). This would be a major project pivot but a clean
  negative result.

## Estimated Compute Cost

* Per-cell evaluation budget: 24 dirs x 30 seeds = 720 sims per replication x 5 outer-seed
  replications = 3,600 sims per cell. Total: 20 cells x 3,600 = 72,000 sims.

* Per-cell wall-clock estimate: t0083 averaged ~36 s/cell at 8 dirs x 20 seeds = 160 sims;
  4.5x sim count = ~162 s/cell at 24 dirs x 30 seeds (per replication). 5 replications x ~162
  s = ~13.5 min/cell. With 43 effective cores parallelising over 100 cell-evals (20 cells x 5
  replications): ~13.5 min x 100 / 43 = ~31 min, but per-replication overhead dominates;
  empirical estimate: 5-6 hours optimiser time + ~1 hour Vast.ai instance overhead = 6-7 hours
  wall-clock.

* **Cost estimate: $1.93-$2.57** at $0.32/hr (allow up to 8 hours of EPYC 7B13 instance
  lifetime). Hard cost cap: **$3.50** (1.5x estimate, absorbs the 16% variance observed in
  t0083).

* **Vast.ai instance class**: AMD EPYC 7B13 64-core (same as t0081 / t0083). Fallback: any 36+
  core EPYC at <$0.40/hr if 7B13 unavailable at <$0.35/hr.

## Dependencies

* **t0083_bedb_v3_extend_nsga2_gen8plus**: provides `pareto_front.json` (18 cells) and
  `all_evaluations.json` (1728 cells; 14 of 15 joint-pass cells from gens 13-17). Provides the
  evaluation harness (the loop is `arf.libraries.t0083_loop`-style continuation of t0081's
  harness) to be re-used for the robustness re-evaluation.

* **t0081_bedb_v3_warmstart_nsga2**: provides cell 767 (the first joint-pass cell), the v3
  substrate harness, and the NSGA-II + warm-start scaffolding.

* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset (54-d v3 substrate) used
  unchanged.

* **t0078_bedb_mobo_v2_ais_tiered_ahp**: provides the AIS-augmented parent substrate from
  which t0080 derived the v3 substrate (informs the AIS-Nav biological prior).

* **t0024_port_de_rosenroll_2026_dsgc**: provides the de Rosenroll 2026 DSGC NEURON port (Bed
  B base substrate before AIS / dendritic-spike augmentation; informs the GABA/AMPA spatial
  distribution biological prior).

* **t0084_t0081_cell_767_vm_trace_deepdive**: provides the cell-767 mechanism-attribution
  answer asset (informs the biological priors for the cell-767 cluster).

## Recommended Task Types

* `experiment-run` -- Phase A robustness re-evaluation (Vast.ai compute).
* `data-analysis` -- Phase B cluster analysis (local CPU; sklearn + UMAP).
* `answer-question` -- Phase C biological-plausibility scorecard (one answer asset).

## Notes

The 5 outer RNG seeds for Phase A must be deterministic and recorded in
`results/data/replication_seeds.json` to enable exact reproduction. The seeds should be drawn
from a fixed parent seed (e.g., 0..4 from `np.random.SeedSequence(42).spawn(5)`) so that the
re-evaluation is exactly reproducible.

The 5 closest near-pass cells should be selected from t0083's Pareto front (filtered to
non-joint-pass cells) by Euclidean distance to the (DSI 0.4, PD 10) joint corner using the
formula `sqrt((max(0, 0.4 - DSI) / DSI_scale)^2 + (max(0, 10 - PD) / PD_scale)^2)`. A
reasonable choice for the scales is `DSI_scale = 0.1` (10% of the joint-pass DSI threshold)
and `PD_scale = 5 Hz` (50% of the joint-pass PD threshold); this puts DSI and PD on roughly
equal footing in the distance metric.

The biological priors in Phase C should be loaded from the existing literature surveys (t0017
/ t0018 / t0019) and confirmed via the cited papers' details / summary documents in
`assets/paper/`. The published mean and sigma for each prior must be tabulated in
`results/data/biological_priors.json` before the per-cluster scorecard is computed.

The cluster-stability bootstrap (50 samples, ARI vs full-sample labels) is the primary
safeguard against over-interpreting clusters that arise from the Genuine subset's small size
(best case 15 cells). If ARI < 0.5 across the bootstrap, the cluster verdicts in the answer
asset must explicitly disclose the instability and degrade the per-cluster confidence
accordingly.

The cost-watchdog rate-fix REQ-X requires that the watchdog reads
`logs/steps/<NNN>_setup-machines/machine_log.json` `selected_offer.price_per_hour` at startup
and uses that value as the hourly rate when computing accumulated cost. The watchdog MUST log
the resolved rate at startup so that any future audit can confirm the value used.
Implementation review must explicitly check this code path before merging the implementation
step.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0086_robustness_cluster_bio_comparison"
> date_completed: "2026-05-06"
> ---
> **Results Summary -- t0086_robustness_cluster_bio_comparison**
>
> **Summary**
>
> Re-evaluated the top 20 cells from t0083 (15 joint-pass + 5 closest near-pass) at 24
> directions x 30
> inner seeds x 5 outer-seed replications on Vast.ai EPYC 7B13. **6 cells were Genuine** (5/5
> reps
> pass DSI >= 0.4 AND PD >= 10 Hz), **7 Marginal** (3-4/5), **7 Stochastic** (<=2/5). k-means
> clustering on the 6 Genuine cells in 54-d parameter space selected **best_k=2**; both
> clusters were
> classified **exotic** by the biological scorecard, driven by extreme NMDA per-synapse
> conductance
> (>85 sigma above Sivyer 2013) and elevated distal NaP density (>7 sigma above Stuart 1999)
> common to
> both clusters.
>
> **Metrics**
>
> * **Genuine cells: 6 / 20** (cells 1517, 1604, 1634, 1639, 1663, 1677). Project pass
>   criterion of

</details>

<details>
<summary>✅ 0085 — <strong>Brainstorm results session 16</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0085_brainstorm_results_16` |
| **Status** | completed |
| **Effective date** | 2026-05-06 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md), [`t0073_brainstorm_results_12`](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0077_brainstorm_results_13`](../../../overview/tasks/task_pages/t0077_brainstorm_results_13.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0079_brainstorm_results_14`](../../../overview/tasks/task_pages/t0079_brainstorm_results_14.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0082_brainstorm_results_15`](../../../overview/tasks/task_pages/t0082_brainstorm_results_15.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-06T09:00:00Z |
| **End time** | 2026-05-06T10:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 16](../../../overview/tasks/task_pages/t0085_brainstorm_results_16.md) |
| **Task folder** | [`t0085_brainstorm_results_16/`](../../../tasks/t0085_brainstorm_results_16/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0085_brainstorm_results_16/results/results_detailed.md) |

# Brainstorm Session 16: Robustness, Cluster Analysis, and Biological Plausibility of t0083 Joint-Pass Cells

Sixteenth brainstorming session. Run on 2026-05-06 after t0083
(`bedb_v3_extend_nsga2_gen8plus`) extended t0081's NSGA-II from gen 7 through gen 17 and
**expanded the joint-pass population from 1 to 15 cells** (1 inherited cell 767 + 14 new cells
produced in gens 13-17), with 3 of those 15 lying on the final 18-cell Pareto front
(highest-DSI cell 1304 at DSI 0.7652 / PD 13.96 Hz). Hypervolume grew +118% from gen 7
(16.330) to gen 17 (35.576) over 960 additional evaluations. t0083's actual cost was $5.83
against a $5.00 cap (16% over) due to a watchdog rate-bug: the in-loop watchdog used the
hard-coded $0.2382/hr rate inherited from t0080/t0081, but the actual instance offer billed at
$0.3209/hr (1.347x). t0084 (`t0081_cell_767_vm_trace_deepdive`) ran in parallel at $0 and
produced the cell-767 mechanism-attribution answer asset. Total project spend now **$13.96 /
$20.00** with **$6.04 remaining**.

## Decisions

* **Create t0086** -- `robustness_cluster_bio_comparison`. Bundle three previously open
  suggestions (S-0083-02 motif clustering, S-0083-05 multi-seed smoke gate / robustness check,
  and the multi-replicate confirmation aspect of S-0081-01) into a single combined task that
  runs three sequential phases on top of t0083's 18-cell Pareto front: **Phase A (robustness
  validation)** re-evaluate the top 20 cells (15 joint-pass cells + 5 closest near-pass cells
  from t0083's Pareto front by Euclidean distance to the (DSI 0.4, PD 10) joint corner) at 24
  directions x 30 seeds x 5 outer RNG-seed replications and classify each cell as Genuine (5/5
  pass), Marginal (3-4/5), or Stochastic (<=2/5); **Phase B (cluster analysis)** k-means +
  hierarchical clustering with k=2..6 selected by silhouette + BIC on the 54-d parameter
  vectors of Genuine cells, plus UMAP/t-SNE 2D visualisation; **Phase C (biological
  comparison)** score each cluster centroid against published priors (Kole 2008 AIS Nav,
  Werginz 2024 mouse alpha-RGC AIS-to-soma Nav ratio, Sivyer 2013 + Branco-Hausser 2010
  dendritic NMDA, Oesch 2005 + Goldfinger 2000 + Stuart 1999 distal Nav1.6/NaP, de Rosenroll
  2026 GABA/AMPA spatial distribution) producing a per-cluster biological-plausibility
  scorecard (within +/-2 sigma = plausible; +/-2-5 sigma = stretched; >5 sigma = exotic).
  Output: one **answer asset** per-cluster attribution + cluster characterisation tables +
  UMAP plot + biological-plausibility scorecard. Compute estimate: 100 cell-evals @ ~720 sims
  each = ~5-6 hours optimiser time; with overhead ~6-8 hours wall-clock on Vast.ai 64-core
  EPYC 7B13 = **$1.93-$2.57**; **hard cost cap $3.50** (1.5x estimate). **Hard requirement
  REQ-X (cost watchdog rate fix)**: cost watchdog MUST use actual per-instance hourly rate
  from `machine_log.json` `selected_offer.price_per_hour`, not a hard-coded constant. Source
  suggestions: **S-0083-02** (primary); also covers S-0083-05 and the multi-replicate aspect
  of S-0081-01. Dependencies: t0024, t0078, t0080, t0081, t0083, t0084.

## Suggestion Cleanup

* **Reject three suggestions** as covered by t0086 (analogous to session 15's S-0080-01/02/03
  cleanup):

  * **S-0083-02** (motif clustering on the 18 t0083 Pareto cells) -- t0086 Phase B is exactly
    this analysis, applied to a stricter subset (Genuine cells only, after Phase A robustness
    filtering), with a richer technique stack (k-means + hierarchical + UMAP) and the
    additional biological-comparison Phase C overlaid on top.

  * **S-0083-05** (multi-seed smoke gate / robustness check across t0083 joint-pass cells) --
    t0086 Phase A is exactly this gate, run at the larger 30-seed x 5-outer-rep budget that
    cleanly separates Genuine / Marginal / Stochastic.

  * **S-0081-01** (multi-replicate confirmation of cell 767 + neighbour cells) -- the
    multi-replicate confirmation aspect is covered by t0086 Phase A's 5-replication design.
    Cell 767 is included in the t0086 cell set; the Genuine/Marginal/Stochastic classification
    directly answers whether 767 reproduces under different RNG seeds. The remaining S-0081-01
    aspects (different morphologies, different conductance noise profiles) are deferred to
    optional follow-up tasks if Phase A flags reproducibility issues.

## Reprioritisations

None.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued.

## Assets Produced

No assets in this brainstorm task. The new task t0086 will produce: one answer asset
attributing each Genuine cluster to known biology (Kole/Werginz/Sivyer/Oesch priors) or
flagging clusters as novel/unphysical, plus cluster characterisation tables (under
`results/`), UMAP/t-SNE plots, per-cluster centroid + variance tables, per-cluster
biological-plausibility scorecard, and the robustness-classification table over all 20 cells.

## Budget Context

Project budget $20.00; $13.96 spent before t0086; **$6.04 remaining**. t0086's $3.50 hard cap
leaves $2.54 buffer for any subsequent S-0083-* follow-ups (e.g., morphology-variation
replicates, conductance-noise replicates, cross-bed validation). The cost-watchdog rate-fix
REQ in t0086's plan prevents a t0083-style 16% overrun.

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0085_brainstorm_results_16"
> date_completed: "2026-05-06"
> status: "complete"
> ---
> **Results Summary: Brainstorm Session 16**
>
> **Summary**
>
> Sixteenth strategic brainstorm, run on 2026-05-06 after t0083
> (`bedb_v3_extend_nsga2_gen8plus`)
> extended t0081's NSGA-II from gen 7 through gen 17 and **expanded the joint-pass cell
> population
> from 1 to 15 cells** (1 inherited cell 767 + 14 new in gens 13-17), with hypervolume +118%
> (16.330
> -> 35.576), and t0084 (`t0081_cell_767_vm_trace_deepdive`) produced the cell-767
> mechanism-attribution answer asset at $0 cost. One consolidated follow-up task commissioned:
> t0086
> (`robustness_cluster_bio_comparison`) bundles three open suggestions (S-0083-02 motif
> clustering,
> S-0083-05 multi-seed robustness gate, multi-replicate aspect of S-0081-01) into three
> sequential
> phases on top of t0083's 18-cell Pareto front -- (A) re-evaluate top 20 cells (15 joint-pass
> + 5
> closest near-pass) at 24 directions x 30 seeds x 5 outer-seed replications and classify
> Genuine /
> Marginal / Stochastic; (B) k-means + hierarchical clustering with k=2..6 on Genuine cells'
> 54-d

</details>

<details>
<summary>✅ 0083 — <strong>Extend t0081 NSGA-II from gen-7 with adaptive HV-plateau
stop</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0083_bedb_v3_extend_nsga2_gen8plus` |
| **Status** | completed |
| **Effective date** | 2026-05-06 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0081-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-05-05T13:02:26Z |
| **End time** | 2026-05-06T08:31:36Z |
| **Step progress** | 12/15 |
| **Task page** | [Extend t0081 NSGA-II from gen-7 with adaptive HV-plateau stop](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) |
| **Task folder** | [`t0083_bedb_v3_extend_nsga2_gen8plus/`](../../../tasks/t0083_bedb_v3_extend_nsga2_gen8plus/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/results_detailed.md) |

# Extend t0081 NSGA-II from gen-7 with Adaptive HV-Plateau Stop

## Motivation

t0081 (`bedb_v3_warmstart_nsga2`) delivered the project's first joint-pass cell at gen 7 cell
767 (DSI 0.494 / PD 11.39 Hz) on a 16-cell Pareto front across 768 evaluations ($2.39 on
Vast.ai 64-core EPYC 7B13, $0.2382/hr). Three observations from t0081's results motivate
continuing the run:

1. **Hypervolume grew monotonically with no plateau**: 6.59 (gen 0) -> 8.99 (gen 1) -> 9.24
   (gen 2) -> 11.08 (gen 3) -> 11.57 (gen 4) -> 13.14 (gen 5) -> 15.22 (gen 6) -> 16.33 (gen
   7). The 7.4% increase from gen 6 to gen 7 indicates the Pareto front is still actively
   expanding; the optimiser stopped not because it converged but because the planned gen=8
   budget ran out.

2. **Single joint-pass cell out of 768 evaluations.** Cell 767 is the only cell in the (DSI >=
   0.4 AND PD >= 10 Hz) box. The pass region of the parameter space is **discovered but not
   characterised**. A neighbourhood cluster (cell 637 at distance 0.063, cell 762 at distance
   0.086) sits just outside the box. Additional generations should populate this cluster and
   produce more joint-pass cells.

3. **The natural extension preserves t0081's evolutionary trajectory.** Continuing from
   t0081's gen-7 final population (96 surviving individuals after RankAndCrowding survival)
   avoids the cost of re-evaluating the warm-start initial population and lets NSGA-II
   continue evolving from a known good state.

This task addresses project research question **Q4** (active vs passive dendritic conductances
on directional tuning sharpness) by extending the search budget on the v3
dendritic-spike-augmented Bed B substrate that t0081 established as the project's working
substrate. Source suggestion: **S-0081-02** (extend t0081 NSGA-II to gen 12-15).

## Scope

### In scope

* Reuse t0081's harness (`tasks/t0081_bedb_v3_warmstart_nsga2/code/`) verbatim with two
  modifications:
  * Replace the Sobol/LHS + projected-Pareto warm-start init with a direct load of t0081's
    gen-7 final population (96 individuals, with objective values pre-computed and re-injected
    into pymoo's `Algorithm` state to skip re-evaluation).
  * Add an **adaptive HV-plateau watchdog** that terminates NSGA-II when `(HV(gen N) - HV(gen
    N-3)) / HV(gen N-3) < 0.01` averaged over the last 3 generations, AND only after a minimum
    of **5 additional generations** has been run (i.e., earliest possible stop is gen 12). The
    watchdog evaluates after every generation starting at gen 11 (so gen 11 needs HV from gens
    8, 9, 10, 11 -- a 3-gen lookback window starting at gen 8 is the first eligible window).
* Hard cap on total additional generations: **10** (gen 8 through gen 17 maximum). If the
  watchdog never fires, terminate at gen 17.
* Hard cost cap: **$5.00**. Spawn a budget watchdog identical to t0081's that monitors
  `instance_lifetime_hr * $0.2382/hr` and forces graceful termination if the projected
  end-of-generation cost would exceed $5.00.
* Reuse the `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset from t0080 unchanged.
  No substrate changes.
* Same Vast.ai instance class as t0081 (AMD EPYC 7B13 64-core, 503 GB RAM, $0.2382/hr).
* Compare final Pareto front, joint-pass cell count, HV trajectory, and per-generation
  parameter-distribution diagnostics against t0081 and t0080 baselines.

### Out of scope

* Substrate changes (no new dendritic-spike parameters; no new channels; no AIS
  modifications).
* Optimiser changes (NSGA-II via pymoo only; no NSGA-III, hybrid, or BO comparison).
* Multi-replicate confirmation (S-0081-01 covers that; deferred to a later task).
* Vm-trace analysis of cell 767 (S-0081-03 covers that; addressed in t0084 in parallel with
  this task).
* Bed A cross-bed replication (S-0081-05).

## Pass Criteria

* **Primary**: at least one **additional** Pareto cell with `DSI >= 0.4 AND PD >= 10 Hz`
  beyond t0081's cell 767 (i.e., total joint-pass cells
  > = 2). Characterises the joint-passing region by populating the near-pass cluster (cells 637 and
  > 762 from t0081 should evolve into the joint-pass box if the cluster is robust).

* **Secondary**: HV trajectory continues monotonically; final HV > t0081's 16.33; HV-plateau
  stop rule fires before the gen-17 hard cap OR the budget watchdog fires.

* **Acceptable negative**: zero additional joint-pass cells but final HV
  > t0081's 16.33 with HV-plateau detected before gen 17 -- documented as evidence that t0081's cell
  > 767 is an isolated point in the parameter space rather than a cluster, with implications for
  > downstream multi-replicate strategy.

## Estimated Compute Cost

* Per-cell wall-clock on t0081's instance: ~30 s (768 cells / 10.045 h instance lifetime ~= 47
  s/cell including overhead; NSGA-II gen 7 cells averaged ~30 s each).
* 5 additional generations at pop 96 = 480 cells @ 30 s = 4.0 h optimiser time; with 30 min
  Vast.ai instance overhead = 4.5 h * $0.2382 = ~$1.07.
* 10 additional generations at pop 96 = 960 cells @ 30 s = 8.0 h optimiser time; with overhead
  = 8.5 h * $0.2382 = ~$2.02.
* Most-likely range: **$1.50 - $3.00** depending on when the HV-plateau rule fires.
* **Hard cost cap: $5.00** (allows up to ~21 hours of instance lifetime, enough to absorb any
  per-cell wall-clock variance from the v3 substrate's dendritic-spike machinery).

## Dependencies

* **t0081_bedb_v3_warmstart_nsga2**: provides gen-7 final population (96 individuals with
  parameter vectors and objective values), the NSGA-II harness to extend, and the warm-start
  projection logic to inherit unchanged.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset (54-d v3 substrate) used
  unchanged.
* **t0078_bedb_mobo_v2_ais_tiered_ahp**: provides the AIS-augmented parent substrate from
  which t0080 derived the v3 substrate.
* **t0024_port_de_rosenroll_2026_dsgc**: provides the de Rosenroll 2026 DSGC NEURON port (Bed
  B base substrate before AIS / dendritic-spike augmentation).

## Recommended Task Types

* `experiment-run` -- the primary mode (NSGA-II continuation).

## Notes

The watchdog logic must be additive, not destructive: each new generation appends to t0081's
saved evaluation history rather than overwriting it. The final `all_evaluations.json` should
contain the union of t0081's 768 cells plus this task's additional cells (480-960), with
consistent generation numbering (t0081 ends at gen 7; this task starts at gen 8).

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0083_bedb_v3_extend_nsga2_gen8plus"
> date_completed: "2026-05-06"
> ---
> **Results Summary -- t0083_bedb_v3_extend_nsga2_gen8plus**
>
> **Summary**
>
> The NSGA-II warm-start continuation extended t0081's run from gen 7 through gen 17 on the
> same v3
> Bed B substrate, producing **14 new joint-pass cells** (DSI >= 0.4 AND PD >= 10 Hz) on top
> of
> t0081's single inherited cell 767, for a project total of **15 joint-pass cells** at
> completion.
> Hypervolume grew from **16.330 at gen 7** to **35.576 at gen 17** (+118%) over 960
> additional
> evaluations; the run terminated under the gen-17 hard cap rather than the HV-plateau
> watchdog.
>
> **Metrics**
>
> * **15 joint-pass cells** across 1728 total evaluations: 1 inherited from t0081 (cell 767,
>   gen 7,
> DSI 0.494 / PD 11.39 Hz) and 14 new ones produced in t0083 generations 13-17.
> * **3 of those 15 joint-pass cells lie on the final Pareto front**: cell 1304 (gen 13, DSI
>   0.7652 /

</details>

## 2026-05-05 (3)

## ✅ Completed

<details>
<summary>✅ 0084 — <strong>Vm-trace deep-dive of t0081 cell 767 to attribute the
joint-pass DSI mechanism</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0084_t0081_cell_767_vm_trace_deepdive` |
| **Status** | completed |
| **Effective date** | 2026-05-05 |
| **Dependencies** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0081-03` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-05T15:41:07Z |
| **End time** | 2026-05-05T16:45:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Vm-trace deep-dive of t0081 cell 767 to attribute the joint-pass DSI mechanism](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Task folder** | [`t0084_t0081_cell_767_vm_trace_deepdive/`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/results_detailed.md) |

# Vm-Trace Deep-Dive of t0081 Cell 767 to Attribute the Joint-Pass DSI Mechanism

## Motivation

t0081 (`bedb_v3_warmstart_nsga2`) delivered the project's first joint-pass cell: **gen 7 cell
767 at DSI 0.494 / PD 11.39 Hz** on the v3 dendritic- spike-augmented Bed B substrate. This is
a major architectural milestone -- the first single-cell substrate in the project lineage to
satisfy `DSI >= 0.4 AND PD >= 10 Hz` simultaneously. However, the **biophysical mechanism for
the DSI improvement is unattributed**: cell 767's parameter vector contains non-zero values
for all five dendritic-spike machinery dimensions added in t0080 (`gnmda_dend`, `mg_conc_mm`,
`voff_nmda`, `nav16_dend_distal`, `nap_dend_distal`), and the joint-pass result could
plausibly arise from any one of three mechanisms or a combination:

1. **NMDA Mg-block recruitment.** Active dendritic NMDA receptors with Mg-block produce
   voltage-dependent multiplicative gain that supercharges ND-suppressed but PD-active
   synaptic input. This is the Sivyer 2013 / Branco-Hausser 2010 mechanism.
2. **Distal Nav1.6 dendritic spikes.** Backpropagating APs and locally initiated dendritic
   spikes from distal Nav1.6 produce non-linear amplification of PD-correlated input. This is
   the Oesch 2005 mechanism.
3. **NaP sustained depolarisation.** Persistent Na current at distal dendrites produces a
   sustained depolarising plateau that enhances PD firing without proportionally enhancing ND
   firing (assuming GABA asymmetry suppresses ND-direction NaP recruitment). This is the
   Goldfinger 2000 / Stuart 1999 mechanism.

Without per-direction Vm traces and per-channel current-flow analysis, we cannot distinguish
which mechanism (or combination) drives cell 767's DSI improvement. The attribution matters
strategically: it determines which mechanism to optimise first if t0083's extension finds
additional joint- pass cells, and which to test on Bed A in S-0081-05's cross-bed validation.

This task addresses project research question **Q4** (do active dendritic voltage-gated
conductances improve, degrade, or have no effect on the match to the target angle-frequency
curve compared with passive dendrites?) by mechanistically dissecting the first cell in the
project to deliver a positive answer to Q4 in joint form. Source suggestion: **S-0081-03**.

## Scope

### In scope

* Re-evaluate three cells from t0081's Pareto front in subprocess (eval-mode, no NSGA-II loop)
  on the v3 substrate (`de_rosenroll_2026_dsgc_ais_dendritic_spike`):
  * Cell 767 (joint-pass; DSI 0.494 / PD 11.39 Hz; gen 7).
  * Cell 637 (near-pass; distance 0.063; gen 6).
  * Cell 762 (near-pass; distance 0.086; gen 7).
* For each cell and each of 8 stimulus directions (0, 45, 90, 135, 180, 225, 270, 315 deg),
  record:
  * Vm at proximal soma.
  * Vm at one mid-dendrite section.
  * Vm at one distal-dendrite section (the same one that carries nav16_dend_distal and
    nap_dend_distal channel insertions).
  * Per-segment NMDA conductance trajectories (`gnmda` over time) at the distal dendrite
    synapses recruited during the simulation window.
  * Per-segment Nav1.6 and NaP currents at the distal dendrite (`ina` decomposed by
    mechanism).
  * Per-direction AIS spike onset times (zero-crossing of Vm at the AIS threshold trigger).
* Generate four figure assets per cell (12 figures total):
  1. **Per-direction Vm traces** at proximal soma, mid dendrite, distal dendrite (3-row
     stacked, 8-column grid).
  2. **NMDA conductance trajectories** at distal dendrite per direction (8-line plot).
  3. **Nav1.6 / NaP current decomposition** at distal dendrite per direction (8-direction
     stacked plot).
  4. **AIS spike onset histogram** per direction (polar plot or 8-bin bar chart).
* Identify, per cell, which mechanism dominates the DSI difference between PD (gen direction
  with peak rate) and ND (gen direction with minimum rate). Use a quantitative attribution
  metric: the **fractional contribution of each channel to the integrated dendritic
  depolarisation during the PD response window minus the same during the ND response window**.
* Produce one **answer asset** at
  `assets/answer/cell-767-dendritic-spike-mechanism-attribution/` with short and full answer
  documents per the answer-asset specification, attributing cell 767's DSI mechanism to one
  (or a combination) of the three candidates.

### Out of scope

* Re-running NSGA-II or any optimisation (use cell 767/637/762 parameters verbatim).
* Modifying the substrate library asset.
* Bed A cross-bed comparisons (S-0081-05).
* Statistical multi-replicate confirmation across seeds (S-0081-01).
* Comparing alternative dendritic mechanisms (Ca2+ plateau, Ih, HCN) -- scope limited to the
  three machinery components present in the v3 substrate.

## Pass Criteria

* All 24 simulations (3 cells * 8 directions) complete with stable Vm traces (no numerical
  instabilities, no NaN values).
* All 12 figures generated and embedded in `results/results_detailed.md`.
* The answer asset clearly identifies the dominant mechanism (or combination, with relative
  weights) for cell 767's DSI improvement.
* The mechanism attribution for cells 637 and 762 (near-pass neighbours) is consistent with
  cell 767's attribution -- if not, the discrepancy is documented as a "near-pass cluster
  heterogeneity" finding.

## Estimated Compute Cost

* Local CPU only. No remote machine.
* Per-cell wall-clock: 8 directions * ~30-45 s/direction = ~3-6 min, plus per-segment
  recording overhead = ~5-10 min per cell.
* Total runtime: ~15-30 min for 3 cells.
* **Compute cost: $0**.

## Dependencies

* **t0081_bedb_v3_warmstart_nsga2**: provides cell 767, 637, 762 parameter vectors (54-d
  natural-unit vectors from `results/data/all_evaluations.json`), the v3 substrate evaluation
  harness (`evaluate_cell.py` or equivalent), and the recording infrastructure for per-segment
  Vm / conductance / current trajectories.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset and its channel-insertion API
  (Nav1.6, NaP, NMDA Mg-block per dendritic section).

## Recommended Task Types

* `experiment-run` -- 24 single-cell NEURON simulations with extended recording.
* `data-analysis` -- per-channel current decomposition and figure generation.
* `answer-question` -- mechanism-attribution answer asset.

## Notes

The recording infrastructure for per-segment Vm, NMDA conductance, and Nav1.6 / NaP currents
must be added to or wrapped around t0081's eval harness. The harness currently records spike
counts per direction; this task adds full Vm traces and per-mechanism current decomposition.
Keep the recording additive -- the eval harness must remain backwards-compatible with t0081's
NSGA-II loop in case t0083 needs to re-use it.

The answer asset's confidence level should reflect the single-cell-replicate nature of the
analysis: cell 767's mechanism is attributed for that specific cell, but generalisation to
"all joint-pass cells in the v3 substrate" requires t0083's additional joint-pass cells (or
S-0081-01's multi-replicate study). The answer asset should state this explicitly in its `##
Limitations` section.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0084_t0081_cell_767_vm_trace_deepdive"
> ---
> **Results Summary: Vm-Trace Deep-Dive of t0081 Cell 767**
>
> **Summary**
>
> Re-evaluated t0081 Pareto cells 767 (joint-pass), 637, 762 (near-pass) on the v3 Bed B
> substrate
> with extended Vm/conductance/current recording across 8 directions and computed an
> integrated
> PD-vs-ND fractional channel contribution. Cell 767's PD/ND integrated-current asymmetry is
> **NaP-dominant** (NMDA 0.0%, Nav1.6 7.0%, NaP 93.0%), and cells 637 and 762 share the same
> NaP-dominant signature (98.5% and 99.9%). The single-replicate run did not reproduce cell
> 767's
> original 5-seed mean DSI (0.494 vs. measured 0.000), so the attribution describes the
> parameter-set
> biophysical signature rather than a per-trial joint-pass mechanism; multi-replicate
> confirmation
> requires t0083 or a follow-up multi-seed study.
>
> **Metrics**
>
> * **Cell 767 fractional contributions**: NMDA **0.0%**, Nav1.6 **7.0%**, NaP **93.0%**
>   (dominant)

</details>

<details>
<summary>✅ 0082 — <strong>Brainstorm results session 15</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0082_brainstorm_results_15` |
| **Status** | completed |
| **Effective date** | 2026-05-05 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md), [`t0073_brainstorm_results_12`](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0077_brainstorm_results_13`](../../../overview/tasks/task_pages/t0077_brainstorm_results_13.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0079_brainstorm_results_14`](../../../overview/tasks/task_pages/t0079_brainstorm_results_14.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-05T16:00:00Z |
| **End time** | 2026-05-05T17:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 15](../../../overview/tasks/task_pages/t0082_brainstorm_results_15.md) |
| **Task folder** | [`t0082_brainstorm_results_15/`](../../../tasks/t0082_brainstorm_results_15/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0082_brainstorm_results_15/results/results_detailed.md) |

# Brainstorm Session 15: Extend t0081 NSGA-II + Vm-Trace Deep-Dive of Cell 767

Fifteenth brainstorming session. Run on 2026-05-05 after t0081 (`bedb_v3_warmstart_nsga2`)
completed and **delivered the project's first joint-pass cell**: gen 7 cell 767 at **DSI 0.494
/ PD 11.39 Hz** on a 16-cell Pareto front (768 evaluations, $2.39 on Vast.ai). t0081 satisfied
the project's working pass criterion `DSI >= 0.4 AND PD >= 10 Hz` simultaneously for the first
time in the project lineage, decisively answering research question Q4 (do active dendritic
conductances enable joint DSI/PD pass on Bed B?) as **yes** when given an adequate NSGA-II
budget plus combined t0078 + t0080 warm-start. Hypervolume grew monotonically from 6.59 (gen
0) to 16.33 (gen 7) with **no plateau**, suggesting more generations can both characterise the
joint-passing region and potentially find additional joint-pass cells. The researcher topped
up the project budget by $10 (now $11.87 remaining out of an effective $20 cap) to enable
t0081 follow-ups.

## Decisions

* **Create t0083** -- `bedb_v3_extend_nsga2_gen8plus`. Continue NSGA-II from t0081's gen-7
  final population (96 surviving individuals) for **at least 5 more generations** (gen 8-12)
  with an **adaptive HV-plateau stop rule**: terminate when relative HV improvement averaged
  over the last 3 generations falls below **1%** (i.e., `(HV(gen N) - HV(gen N-3)) / HV(gen
  N-3) < 0.01`). Hard cap on total additional generations: **10** (gen 8-17 maximum). Reuse
  the t0081 harness verbatim with `n_gen` parameterised and a HV-plateau watchdog added. Pass
  criterion: characterise the joint-passing region (count of Pareto cells with `DSI >= 0.4 AND
  PD >= 10 Hz`; final HV; HV trajectory). Compute estimate ~$1.50 - $3.00 over ~6-12
  wall-clock hours on Vast.ai 64-core EPYC 7B13 at $0.2382/hr; **hard cost cap $5.00**. Source
  suggestion: S-0081-02. Dependencies: t0081 (provides gen-7 final population), t0080
  (substrate library), t0078, t0024.

* **Create t0084** -- `t0081_cell_767_vm_trace_deepdive`. Local-CPU per-direction (8 angles)
  Vm-trace deep-dive of cell 767 (joint-pass) plus the two neighbouring near-pass cells 637
  (distance 0.063) and 762 (distance 0.086) on the t0081 v3 substrate. Record proximal-soma,
  mid-dendrite, and distal-dendrite traces; plot dendritic-spike onset times, NMDA conductance
  trajectories per dendritic site, and AIS spike correlation per direction. Output: figure
  assets and an answer asset attributing cell 767's DSI improvement to specific
  dendritic-spike machinery (NMDA Mg-block recruitment vs distal Nav1.6 dendritic spikes vs
  NaP sustained depolarisation, or a combination). Local CPU only, **no remote machine, $0
  compute cost**, ~10 min runtime per cell. Source suggestion: S-0081-03. Dependencies: t0081
  (cell 767/637/762 parameter vectors and v3 substrate library reference), t0080 (substrate
  library `de_rosenroll_2026_dsgc_ais_dendritic_spike`).

## Suggestion Cleanup

* **Reject three suggestions** as covered by t0081 (the prior-task analogue of session 14's
  S-0078-01/02/08 cleanup):

  * **S-0080-01** (high) -- Re-run NSGA-II at the full plan scope (pop=96, gen=40 = 3,840
    cells) on the v3 54-d Bed B substrate. **Covered by t0081**, which ran 768 cells at pop=96
    / gen=8 with combined warm-start and **achieved the joint pass criterion**. The full-scope
    re-run was successful at 4x t0080's evaluation budget; further extension is addressed by
    t0083.

  * **S-0080-02** (high) -- Substrate regression check on the t0076 iter-424 vector mapped to
    the v3 54-d parameter space. **Covered by t0081's positive result**: t0081's
    compare-literature analysis explicitly states "the v3 substrate is not regressed -- it
    admits joint-pass cells when given an adequate budget plus warm-start". The regression
    hypothesis is ruled out by direct demonstration.

  * **S-0080-03** (high) -- Warm-start NSGA-II from t0078 Pareto cells mapped into the v3 54-d
    parameter space. **Covered by t0081**, which is exactly this approach: 5 t0080 Pareto
    cells verbatim + 17 t0078 Pareto cells projected from 49-d to 54-d + 74 fresh LHS = pop=96
    warm-start. The deciding ingredient that produced cell 767.

## Reprioritisations

None.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued for later opportunistic
  pickup; researcher confirmed "leave queued" disposition. Different substrate (Bed A) from
  t0083 / t0084 (Bed B v3) and provides complementary one-axis sensitivity analysis.

## Assets Produced

No assets in this brainstorm task. The two new tasks t0083 / t0084 will produce: t0083 -- one
Pareto-front result bundle (extended HV trajectory, joint-pass cell count, cost record,
machine log); t0084 -- Vm-trace figure assets and one answer asset attributing the cell-767
DSI mechanism, all under the t0084 task folder.

## Budget Context

The researcher topped up the project budget by $10 mid-session, raising the effective cap from
$10 to $20 with $1.87 + $10 = **$11.87 remaining**. This unlocked S-0081-02 (estimated $1.50 -
$3.00 with $5.00 hard cap) and S-0081-03 (estimated $0). Combined estimated total $1.50 -
$3.00; combined hard cap $5.00. Both fit comfortably in the topped-up $11.87 envelope while
preserving runway for at least one further follow-up (e.g., S-0081-01 multi-replicate
confirmation at $5-10 across 3-5 replicates).

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0082_brainstorm_results_15"
> date_completed: "2026-05-05"
> status: "complete"
> ---
> **Results Summary: Brainstorm Session 15**
>
> **Summary**
>
> Fifteenth strategic brainstorm, run on 2026-05-05 after t0081 (`bedb_v3_warmstart_nsga2`)
> **delivered the project's first joint-pass cell** at gen 7 cell 767 (DSI 0.494 / PD 11.39 Hz
> on 768
> evaluations, $2.39). The session is triggered by the t0081 architectural milestone: the
> project's
> working pass criterion `DSI >= 0.4 AND PD >= 10 Hz` was satisfied simultaneously for the
> first time,
> decisively answering research question Q4 (active vs passive dendritic conductances) in the
> positive
> on Bed B. Two follow-up tasks commissioned in parallel: t0083
> (`bedb_v3_extend_nsga2_gen8plus`)
> extends t0081's NSGA-II from its gen-7 final population for at least 5 more generations with
> an
> adaptive HV-plateau stop rule (<1% relative HV improvement averaged over a 3-gen window) and
> a $5.00
> hard cost cap; t0084 (`t0081_cell_767_vm_trace_deepdive`) runs a local-CPU per-direction
> Vm-trace
> deep-dive of cells 767, 637, 762 to attribute the DSI mechanism to NMDA Mg-block, distal
> Nav1.6,

</details>

<details>
<summary>✅ 0081 — <strong>Bed B v3 NSGA-II at full scope with combined t0078+t0080
warm-start</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0081_bedb_v3_warmstart_nsga2` |
| **Status** | completed |
| **Effective date** | 2026-05-05 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0080-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-05-04T23:20:10Z |
| **End time** | 2026-05-05T09:55:00Z |
| **Step progress** | 12/15 |
| **Task page** | [Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Task folder** | [`t0081_bedb_v3_warmstart_nsga2/`](../../../tasks/t0081_bedb_v3_warmstart_nsga2/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0081_bedb_v3_warmstart_nsga2/results/results_detailed.md) |

# Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start

## Motivation

t0080 ran NSGA-II on the v3 dendritic-spike-augmented Bed B substrate at a heavily reduced
scope (pop=24 / gen=8 = 192 cells; 5% of the planned 96 / 40 = 3,840 cells) due to a
planning-stage miscalculation about cell parallelism. The result was a clean architectural
negative outcome (best Pareto cell DSI 0.127 / PD 2.54 Hz; pass criterion `DSI ≥ 0.4 AND PD ≥
10 Hz` missed by a wide margin), but the small budget makes it impossible to distinguish a
fundamental substrate limitation from undersampled NSGA-II convergence.

This task re-runs NSGA-II on the **same t0080 v3 substrate** at **pop=96 / gen=8 = 768 cells**
(4× the t0080 scope) with a **combined warm-start** from t0080 and t0078 Pareto cells,
designed to give the optimiser a strong head start in the 54-d search space.

Source suggestion: **S-0080-01** (with scope and strategy modifications agreed in conversation
before launch — see Approach for the deviations from the suggestion's literal text).

## Scope

### In scope

- Re-use the t0080 library asset `de_rosenroll_2026_dsgc_ais_dendritic_spike` and its 13
  vendored MOD files unchanged. No new substrate work.
- Re-use the t0080 NSGA-II harness (`code/nsga2_loop.py` and friends) unchanged. The only
  change is the warm-start initialisation logic and the larger pop / gen counts.
- Generate the warm-start initial population:
  - **5 t0080 Pareto cells** verbatim (cells 58, 141, 153, 188, 190 from
    `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/data/pareto_front.json`). Already
    54-d.
  - **17 t0078 Pareto cells** projected from 49-d to 54-d, with the 5 new dims (`GNMDA_DEND`,
    `MG_CONC_MM`, `VOFF_NMDA`, `NAV16_DEND_DISTAL`, `NAP_DEND_DISTAL`) sampled at **random LHS
    within their full ranges** — NOT zero. Source vectors from
    `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/data/pareto_front.json`.
  - **74 LHS-sampled cells** for diversity.
  - Total initial pop: **96 cells (22 seeded + 74 LHS)**.
- Run NSGA-II via pymoo: `NSGA2(pop_size=96)` with the 96-cell custom initial population,
  gen=8, default operators (SBX η=15, polynomial mutation η=20, tournament selection). Same
  hard biological lower bounds as t0080 (`nav16_ais ≥ 0.25 S/cm²`; AIS-to-soma Nav ratio ≥ 5).
- Pull `pareto_front.json`, `all_evaluations.json`, `hv_trajectory.json` from the remote.
- Generate the same charts as t0080: Pareto front, hypervolume trajectory, all-cells scatter.
- Compute per-cell registered metrics; identify the closest-to-joint Pareto cell.

### Out of scope

- Substrate redesign (still on the v3 dendritic-spike substrate from t0080).
- New MOD files (none needed).
- Library asset (re-uses t0080's; no new asset).
- Answer asset (the failure-mode answer asset already exists from t0080).
- Substrate regression check on t0076 iter-424 (still deferred; would be a separate small
  task).

## Approach

### Warm-start initial population

A new module `code/warm_start.py` in this task generates the 96-cell initial population:

1. Load the 5 t0080 Pareto cells from
   `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/data/pareto_front.json`
   (`cells[*].params`, each 54-d).
2. Load the 17 t0078 Pareto cells from
   `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/data/pareto_front.json`
   (`cells[*].params`, each 49-d).
3. For each t0078 cell, project to 54-d:
   - Indices 0–48: copy verbatim (preserves t0078's 49-d ParamIndex layout, which t0080
     inherited).
   - Indices 49–53: sample uniformly within the v3 lower / upper bounds for the 5 new params,
     using a fixed seed for reproducibility.
4. Generate 74 LHS samples in 54-d using pymoo's `LHS()` operator, then concatenate the 5 + 17
   + 74 = 96 cells into the initial population matrix.
5. Pass the matrix to `NSGA2(pop_size=96, sampling=Population(...))` (or equivalent pymoo API
   for custom initial populations).

### NSGA-II configuration

- pop_size: 96
- n_gen: 8
- sampling: custom 96-cell warm-started population
- crossover: SBX (default η=15)
- mutation: polynomial (default η=20)
- selection: tournament (default)
- constraint: AIS-to-soma Nav ratio ≥ 5 via `n_ieq_constr=1`
- Bounds: identical to t0080 (`nav16_ais ≥ 0.25` lower bound; `tau_ca_multiplier ≤ 20` upper
  bound)

### Pre-launch validation

Before the full NSGA-II run, validate that:
- The 5 t0080 Pareto cells still produce their recorded DSI / PD values when re-evaluated on
  the v3 substrate compiled fresh on the new instance (smoke test for substrate consistency
  across runs).
- The 17 projected t0078 cells produce non-`NaN` results (NSGA-II handles infeasible /
  unstable cells, but truly-broken cells slow convergence).

### Compute

- Vast.ai 64-core CPU EPYC 7B13 class (target same instance class as t0080: $0.16-$0.24/hr).
- Wall-clock estimate: 768 cells × 45 s/cell sequential = ~9.6 h on a 64-core instance.
- **Cost target: ~$2.40** (768 × $0.00284 + $0.20 overhead, t0080-measured per-cell rate).
- **Hard cap: $3.00** (re-armed cost-cap watchdog in `nsga2_loop.py`; existing watchdog logic
  re-used).

## Pass criterion

Locate at least one Pareto cell with **DSI ≥ 0.4 AND PD ≥ 10 Hz**, OR rule it out
architecturally across 768 cells in the warm-started 54-d space — a much stronger negative
result than t0080's 192-cell run. A negative result here, paired with t0080's, makes a clean
architectural case that the v3 substrate cannot reach the joint operating point and the
project should pivot.

## Expected assets

None. The substrate library and answer asset already exist from t0080. This task produces only
results files (Pareto front, hypervolume trajectory, metrics, compare_literature) and
follow-up suggestions. `expected_assets`: `{}`.

## Outputs

- `results/results_summary.md` (Summary, Metrics, Verification)
- `results/results_detailed.md` (Methodology, Pareto Front, Visualisations, Examples,
  Architectural Diagnostic, Limitations, Files Created, Verification, Next Steps, Task
  Requirement Coverage)
- `results/metrics.json` with per-Pareto-cell variants
- `results/costs.json` with the final Vast.ai cost
- `results/remote_machines_used.json`
- `results/data/pareto_front.json`, `all_evaluations.json`, `hv_trajectory.json`,
  `example_cells.json`
- `results/images/pareto_front.png`, `hypervolume_trajectory.png`, `all_cells_scatter.png`
- `results/compare_literature.md` updating the t0080 / t0078 baseline comparisons

## Dependencies

- `t0024_port_de_rosenroll_2026_dsgc` — the upstream Bed B substrate
- `t0069_t0067_ais_localised_channel_sweep` — Bed A AIS reference
- `t0076_bedb_dsi_firing_rate_mobo` — 25-d BO baseline for HV anchor
- `t0078_bedb_mobo_v2_ais_tiered_ahp` — 49-d AIS-augmented substrate; provides 17 warm-start
  cells
- `t0080_bedb_mobo_v3_dendritic_spike_nsga2` — v3 substrate library + 5 warm-start cells +
  harness

## Risks and fallbacks

- **Per-cell wall-clock higher than t0080's 45 s** (e.g., the v3 substrate may be slower for
  active-dendrite cells): cost-cap watchdog kills run if approaching $3.00; partial Pareto
  front is still useful.
- **Warm-start cells produce NaN / unstable behaviour** (e.g., t0078 cells with random new-dim
  values trigger runaway depolarisation): NSGA-II's `is_unstable` filter handles them;
  documented as `n_unstable / n_total` in results.
- **NSGA-II diversity collapse on warm-started population**: small risk that all seeded cells
  cluster too tightly, reducing exploration. The 74 LHS cells mitigate this.
- **Vast.ai 64-core unavailable**: fall back to 36-core or 72-core EPYC instances; re-estimate
  cost proportionally.

## Verification criteria

- Task results pass `verify_task_results.py` with 0 errors.
- Task metrics pass `verify_task_metrics.py` with 0 errors.
- Vast.ai instance destroyed cleanly per `verify_machines_destroyed.py`.
- Cost ≤ $3.00 hard cap.
- All 13 task verificators pass (file, deps, suggestions, metrics, results, folder, logs,
  research_*, compare_literature, machines_destroyed, plan).
- Pre-merge verificator passes with 0 errors.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0081_bedb_v3_warmstart_nsga2"
> date_completed: "2026-05-05"
> status: "complete"
> ---
> **Results Summary: Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start**
>
> **Summary**
>
> Re-ran NSGA-II on the t0080 v3 dendritic-spike-augmented Bed B substrate at the originally
> planned
> scope (pop=96 / gen=8 = **768 cells**) with a combined warm-start initial population (5
> t0080 Pareto
> cells verbatim + 17 t0078 Pareto cells projected to 54-d natural-unit space + 74 fresh LHS).
> Run
> completed cleanly on Vast.ai instance 36149741 (EPYC 7B13 64-core) for **$2.39** total
> ($2.207
> NSGA-II + $0.18 overhead). **Pass criterion (DSI >= 0.4 AND PD >= 10 Hz) ACHIEVED**: gen 7
> cell 767
> sits at **DSI 0.494 / PD 11.39 Hz**, on the Pareto front. Hypervolume grew monotonically
> from 6.59
> (gen 0) to 16.33 (gen 7) — a 2.5x expansion over 8 generations. The result decisively
> answers the
> project's research question Q4 (do active dendritic conductances enable joint DSI/PD pass on
> Bed B?)
> as **yes**, when given an adequate NSGA-II budget and warm-start from prior good cells.
>

</details>

## 2026-05-04 (3)

## ✅ Completed

<details>
<summary>✅ 0080 — <strong>Bed B v3 MOBO with dendritic-spike machinery and
NSGA-II</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0080_bedb_mobo_v3_dendritic_spike_nsga2` |
| **Status** | completed |
| **Effective date** | 2026-05-04 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Expected assets** | 1 library, 1 answer |
| **Source suggestion** | `S-0078-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-04T18:02:48Z |
| **End time** | 2026-05-04T22:45:00Z |
| **Step progress** | 14/15 |
| **Task page** | [Bed B v3 MOBO with dendritic-spike machinery and NSGA-II](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Task folder** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2/`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/results_detailed.md) |

# Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

## Motivation

t0078 (49-d Bed B v2 BoTorch qLogNEHVI MOBO with AIS, tier-stratified channels, and slow
Kv-AHP) expanded the achievable Pareto front by **+36% in hypervolume** over t0076 (8.41 ->
11.41) but still missed the joint pass criterion `DSI >= 0.4 AND PD rate >= 10 Hz`. The
closest cell (iter 81) sits at DSI 0.316 / PD 9.68 Hz, short by 0.084 on DSI and 0.32 Hz on PD
rate. The compare-literature analysis identified two follow-on diagnostics:

1. **Passive dendrites are the bottleneck on the high-DSI rail.** The PD ceiling pinned at
   2.86 Hz across 109 acquisitions despite continuous optimiser exploration -- the signature
   of a saturated negative-feedback loop. Published mouse DSGC DSI > 0.4 is computed at peak
   rates after Gaussian convolution (Trenholm 2013) and / or relies on active dendritic Nav
   (Sivyer 2013) and dendritic spike initiation (Oesch 2005). The augmented substrate added an
   AIS but kept dendrites passive; the missing dendritic-spike machinery is the dominant
   explanation for the compressed high-rail DSI.

2. **MOBO-on-biophysics failure mode at iter 81.** `nav16_ais` collapsed to the search-space
   floor (1e-5 S/cm^2), four orders below Kole 2008's [0.25, 0.5] S/cm^2 prior and five orders
   below Werginz 2024's measured mouse alpha-RGC AIS Nav of 1.3 S/cm^2. The AIS-to-soma Nav
   ratio at iter 81 was 5.5e-5 vs Werginz 2024's measured 17.3. The optimiser converged on a
   configuration where the AIS contributes nothing to spike initiation -- contradicting REQ-2
   / REQ-3 / REQ-4's biological intent. This is a generalisable MOBO-on-biophysics failure
   mode.

Additionally, t0078 hit O(N^3) Cholesky scaling in BoTorch SingleTaskGP: per-cell wall-clock
grew from 28 s in early phase to 9-12 min after acq 480, forcing early stop at acq 416 / 700
and a final cost of $3.93 over 24.86 h on a Vast.ai 64-core CPU instance.

This task addresses all three issues in a single bundled run: (a) add dendritic-spike
machinery, (b) switch optimiser from BoTorch qLogNEHVI to NSGA-II via pymoo to eliminate the
O(N^3) blow-up, (c) enforce biological hard lower bounds so the optimiser cannot exploit the
AIS-disabled corner.

This task directly addresses project research question **Q4** (do active dendritic
voltage-gated conductances improve, degrade, or have no effect on the match to the target
angle-frequency curve compared with passive dendrites?) on the Bed B substrate, and provides a
methodological control for **Q1** (which combinations of somatic Na/K conductances maximise AP
frequency at PD while suppressing firing at ND?).

Source suggestion: **S-0078-01**.

## Scope

### In scope

* Build a new library asset extending the t0078 `de_rosenroll_2026_dsgc_ais` substrate with
  dendritic-spike machinery: Mg-block NMDA at active densities on dendrites (Exp2NMDA with
  voltage-dependent Mg block bound into the bipolar -> DSGC excitatory channel) and Nav1.6 +
  NaP at distal-dendrite densities sufficient for back-propagating APs and dendritic spikes
  per Sivyer 2013 / Oesch 2005 priors.
* Replace the BoTorch qLogNEHVI optimiser with NSGA-II via pymoo
  (`pymoo.algorithms.moo.nsga2.NSGA2`). Configuration: pop 96, 40 generations (3,840
  evaluations), SBX crossover eta=15, polynomial mutation eta=20, tournament selection, Latin
  Hypercube Sampling or Sobol initial population.
* Enforce hard biological lower bounds on AIS-related parameters:
  * `nav16_ais` >= 0.25 S/cm^2 (Kole 2008 cortical pyramidal patch-clamp prior; lower bound of
    the Kole [0.25, 0.5] range)
  * AIS-to-soma Nav ratio >= 5 (Werginz 2024 mouse alpha-RGC; biologically plausible lower
    bound, well below the measured 17.3)
* Pre-run substrate regression check (folded in from S-0078-02): re-evaluate the t0076
  iter-424 parameter vector (DSI 0.42 / PD 8.34 Hz) on the v3 49-d substrate as a one-shot
  validation cell before launching the NSGA-II loop. Document the substrate-regression delta.
* Produce one answer asset (folded in from S-0078-08) documenting the AIS-disabled-corner
  failure mode observed at t0078 iter 81 and the biological-prior checklist now enforced as
  hard MOBO bounds. The answer asset should include: the iter-81 example as the canonical
  case; an audit of t0076 + t0078 Pareto fronts for similar collapse-to-floor patterns on
  biologically-priored parameters; the now-enforced biological-prior checklist (Kole 2008 /
  Werginz 2024); general guidance for future MOBO-on-biophysics tasks.

### Out of scope

* `tau_ca_multiplier` upper bound stays at 20x (S-0078-03 NOT folded in per researcher
  decision; keeps the slow-AHP substrate identical to t0078 for cleaner architectural-delta
  comparison).
* Single-objective scalarised BO comparison (S-0078-04 -- separate methodological task).
* Multi-replicate Sobol seed and BO chain replication for HV uncertainty (S-0078-06 --
  separate evaluation task).
* Promotion of the t0080 NSGA-II harness into a substrate-agnostic library (deferred until at
  least one more substrate uses it).

## Approach

### Substrate v3

Extend the t0078 `de_rosenroll_2026_dsgc_ais` library (the AIS-augmented Bed B from t0078)
with:

1. **Mg-block NMDA on dendrites**: Add Exp2NMDA point process with voltage-dependent Mg block
   to the bipolar -> DSGC excitatory drive at all dendritic compartments (proximal, mid,
   terminal). Conductance and `Mg2+` concentration become free MOBO parameters (~3 new
   parameters: `gnmda_dend`, `mg_conc`, optionally `voff_nmda`).
2. **Nav1.6 + NaP at distal-dendrite densities**: Insert Nav1.6 (already SUFFIX-defined in
   t0078) into the distal-dendrite tier at densities sufficient for back-propagating APs.
   Insert a NaP SUFFIX into the distal-dendrite tier. Density bounds informed by Sivyer 2013
   (rabbit DSGC dendritic spike thresholds) and Oesch 2005 (rabbit ON DSGC peak-rate DSI 0.67
   ON / 0.74 OFF correlated with dendritic spike initiation).

The v3 substrate retains all 49 t0078 MOBO parameters plus ~5-7 new dendritic-spike
parameters. Estimated total dimensionality: **54-56 d**.

### Optimiser: NSGA-II via pymoo

* Algorithm: `pymoo.algorithms.moo.nsga2.NSGA2`
* Population size: 96
* Generations: 40
* Total evaluations: 3,840 cells (each cell = 8 directions x 20 seeds x 1400 ms = 160 NEURON
  simulations)
* Crossover: SBX (`SimulatedBinaryCrossover`) with eta=15 (moderate exploration)
* Mutation: Polynomial mutation (`PolynomialMutation`) with eta=20
* Selection: Tournament selection
* Initial population: Latin Hypercube Sampling (LHS) for spread; falls back to Sobol if LHS is
  not available in pymoo's sampling module
* Reference point for hypervolume: `[0, 0]` (matches t0076 / t0078)
* Hard bounds enforced as parameter bounds (no penalty terms, no log-priors) -- pymoo's bound
  handling guarantees no individual ever has `nav16_ais` < 0.25 or AIS-to-soma Nav ratio < 5

### Pre-run substrate regression check (S-0078-02 folded in)

Before launching the NSGA-II loop:

1. Map the t0076 iter-424 parameter vector to the v3 49-d parameterisation (tier-stratified
   channels at uniform t0076-matching values; AIS Nav at Kole prior centre 0.375 S/cm^2; AIS
   geometry at midpoint; `tau_ca_multiplier=1`). Set the new dendritic-spike parameters at
   their lower bounds (0 dendritic NMDA, 0 distal Nav1.6 / NaP) so the regression check is at
   the architectural baseline equivalent to t0076's substrate.
2. Run `_worker_run_trial` once on local CPU (or as the first NSGA-II eval) and report DSI /
   PD rate.
3. Document the substrate-regression delta in `results/results_summary.md`. Pass: reproduce
   DSI within +/- 0.05 of t0076's 0.42 at PD ~ 8.34 Hz, or document a clean substrate
   regression.

### NEURON re-init bug carry-over

t0078 documented an `Exp2NMDA name already exists` error when re-initialising NEURON inside
the same Python process. The fix from t0078 (subprocess-per-deep-dive) is carried into t0080
via ProcessPoolExecutor with NEURON-fresh-subprocess workers.

### Compute

* Vast.ai 64-core CPU instance (target same EPYC 7B13 64-core class as t0078 instance 36068067
  at $0.1582/hr if available; equivalent if not)
* Estimated wall-clock: 3,840 cells x ~50 s/cell = 192,000 s = 53.3 CPU-hours. With 64
  effective cores in parallel, ~0.83 wall-hours.
* Cost target: $0.13-$0.20 raw + setup overhead = **$1.00-$1.50** total
* **Hard cap: $2.00**. Beyond this, kill the run and document with a clean cost-of-progress
  decision.

## Pass criterion

Locate at least one Pareto cell with **DSI >= 0.4 AND PD rate >= 10 Hz** anchored to
RivlinEtzion 2012 stable-cell joint distribution (DSI 0.78 +/- 0.19, PD 10.38 +/- 8.53 Hz, n =
8), OR rule it out architecturally with a clean negative result documented against the t0078
+36% HV improvement and the substrate-regression delta. Either outcome is a strong project
result:

* **Positive**: dendritic-spike-augmented Bed B v3 becomes the project's standard substrate
  for further joint-optimisation work; the answer asset documents the biological-prior
  checklist as a transferable methodology.
* **Negative**: the trade-off is intrinsic to the de Rosenroll Bed B substrate's morphology or
  SAC-release machinery; the project pivots to alternative dendritic mechanisms (Ca^2+ plateau
  zones per Larkum / Branco-Hausser; Ih / HCN conductances) or substrate redesign.

## Expected assets

* **1 library asset**: `de_rosenroll_2026_dsgc_ais_dendritic_spike` (or similar) -- the v3
  substrate with active dendritic NMDA + Nav1.6 / NaP.
* **1 answer asset**: AIS-disabled-corner MOBO-on-biophysics failure mode write-up with the
  enforced biological-prior checklist.

`expected_assets`: `{"library": 1, "answer": 1}`.

## Outputs

* `results/results_summary.md` (Summary, Methodology, Metrics, Verification, Next Steps -- all
  with the pass-criterion verdict prominently stated)
* `results/results_detailed.md` with embedded Pareto-front PNG, hypervolume-trajectory PNG,
  and per-direction Vm-trace PNGs for the closest-to-joint cell, the max-DSI cell, and the
  max-PD cell
* `results/metrics.json` reporting the final hypervolume, the pass-criterion-closest cell's
  DSI and PD rate, the substrate regression delta, and the new dendritic-spike parameters'
  Pareto values
* `results/suggestions.json` with downstream suggestions
* `results/costs.json` with the final Vast.ai cost
* `results/remote_machines_used.json` with the Vast.ai instance metadata
* `results/compare_literature.md` updating the t0078 literature anchors against the v3 results
* `results/images/pareto_front.png`, `images/hypervolume_trajectory.png`, three deep-dive Vm
  PNGs

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` -- the upstream Bed B substrate
* `t0069_t0067_ais_localised_channel_sweep` -- the Bed A AIS architecture reference for
  cross-bed AIS-construction patterns
* `t0076_bedb_dsi_firing_rate_mobo` -- the BoTorch BO harness baseline that t0078 extended
  (still useful for ParameterSpec scaffolding even though the optimiser changes)
* `t0078_bedb_mobo_v2_ais_tiered_ahp` -- the AIS-augmented 49-d substrate library that t0080
  extends with dendritic-spike machinery

## Risks and fallbacks

* **NSGA-II fails to match t0078's HV 11.41**: itself a useful methodological finding;
  document as a clean comparison and decide whether to switch back to BO with a smaller
  acquisition budget. Do not block on this.
* **Vast.ai 64-core CPU unavailable**: fall back to 36-core or 72-core instances at the same
  CPU class (EPYC 7B13 family) and re-estimate cost. The NSGA-II scaling is linear in cores,
  so a 36-core instance roughly doubles wall-clock (still within the cost cap at $0.10/hr
  rates).
* **Substrate regression check fails**: documents a t0078 substrate regression but is not a
  blocker for the NSGA-II run; the result is a useful note for t0080's results.
* **Cost cap hit before convergence**: kill the run cleanly; report the partial Pareto front
  and the cost-of-progress decision in `results/results_summary.md`. Do not extend the cap
  beyond $2.00 without a brainstorm consult.
* **Dendritic-spike machinery destabilises the substrate (runaway depolarisation)**: detect
  during the substrate regression check; tighten Nav1.6 / NaP upper bounds before launching
  NSGA-II.

## Verification criteria

* Library asset passes `verify_library_asset.py` with 0 errors.
* Answer asset passes the answer-asset verificator with 0 errors.
* Task results pass `verify_task_results.py` with 0 errors.
* Task metrics pass `verify_task_metrics.py` with 0 errors.
* Vast.ai instance destroyed cleanly per `verify_machines_destroyed.py`.
* `verify_pr_premerge.py` passes with 0 errors before merge.
* Cost is at or below the $2.00 hard cap.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
> date_completed: "2026-05-04"
> status: "complete"
> ---
> **Results Summary: Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II**
>
> **Summary**
>
> Built a 54-d AIS+dendritic-spike-augmented Bed B substrate (de Rosenroll 2026 DSGC) by
> extending
> t0078's `de_rosenroll_2026_dsgc_ais` library with Mg-block NMDA at all dendritic
> compartments and
> Nav1.6 + NaP at distal-dendrite densities, then ran a small NSGA-II via pymoo (pop=24, gen=8
> = **192
> evaluations**) on a Vast.ai 64-core EPYC 7B13 instance for **$0.7458**. Hard biological
> lower bounds
> (`nav16_ais` >= 0.25 S/cm² per Kole 2008; AIS-to-soma Nav ratio >= 5 per Werginz 2024 /
> Goethals
> 2020\) eliminated the t0078 iter-81 AIS-disabled-corner failure mode by construction. The
> run
> completed cleanly with 5 non-dominated feasible Pareto cells out of 192 total. **Pass
> criterion (DSI
> > = 0.4 AND PD >= 10 Hz) MISSED**: best Pareto cell sits at DSI 0.127 / PD 2.54 Hz (cell
> 141), and
> > the closest-to-joint Pareto cell sits at DSI 0.000 / PD 9.25 Hz (cell 188, distance 0.850
> from
> > joint). The result is a **clean architectural negative outcome** strongly conditioned by
> the small

</details>

<details>
<summary>✅ 0079 — <strong>Brainstorm results session 14</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0079_brainstorm_results_14` |
| **Status** | completed |
| **Effective date** | 2026-05-04 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md), [`t0073_brainstorm_results_12`](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0077_brainstorm_results_13`](../../../overview/tasks/task_pages/t0077_brainstorm_results_13.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-04T16:00:00Z |
| **End time** | 2026-05-04T17:45:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 14](../../../overview/tasks/task_pages/t0079_brainstorm_results_14.md) |
| **Task folder** | [`t0079_brainstorm_results_14/`](../../../tasks/t0079_brainstorm_results_14/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0079_brainstorm_results_14/results/results_detailed.md) |

# Brainstorm Session 14: Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

Fourteenth brainstorming session. Run on 2026-05-04 after t0078 (49-d Bed B v2 BoTorch
qLogNEHVI multi-objective Bayesian optimisation with AIS, tier-stratified channels, and slow
Kv-AHP) completed. The session is triggered by t0078's headline architectural diagnostic: the
AIS-augmented 49-d substrate expanded the achievable Pareto front by **+36% in hypervolume**
over t0076 but still missed the joint pass criterion of `DSI >= 0.4 AND PD rate >= 10 Hz`
(closest cell iter 81: DSI 0.316 / PD 9.68 Hz, short by 0.084 on DSI and 0.32 Hz on PD). The
compare-literature analysis identified two follow-on diagnostics: (a) the high-DSI rail's PD
ceiling pinned at ~2.86 Hz across 109 acquisitions signals the missing **dendritic-spike
machinery** (Mg-block NMDA at active densities on dendrites + Nav1.6 / NaP at distal-dendrite
densities for back-propagating APs); (b) the iter-81 closest-to-joint cell collapsed AIS Nav
to the search-space floor (1e-5 S/cm^2, four orders below the Kole 2008 patch-clamp prior of
0.25 - 0.5 S/cm^2) -- a generalisable MOBO-on-biophysics failure mode where the optimiser
exploits an AIS-disabled corner that contradicts REQ-2 / REQ-3 / REQ-4's biological intent.

## Decisions

* **Create t0080** -- `bedb_mobo_v3_dendritic_spike_nsga2`. Bed B v3 multi-objective
  optimisation that bundles three follow-ups in a single run: (a) add **dendritic-spike
  machinery** to the t0078 AIS-augmented substrate (Mg-block NMDA at active densities on
  dendrites; Nav1.6 + NaP at distal-dendrite densities sufficient for back-propagating APs and
  dendritic spikes per Sivyer 2013 / Oesch 2005 priors); (b) switch the optimiser from BoTorch
  qLogNEHVI to **NSGA-II via pymoo** (pop 96, 40 generations, SBX crossover eta=15, polynomial
  mutation eta=20, tournament selection, LHS or Sobol initial population) eliminating O(N^3)
  GP-fit scaling that pushed t0078 to $3.93 at 60% of planned acquisitions; (c) enforce
  **biological hard lower bounds** per Kole 2008 / Werginz 2024 priors (`nav16_ais` >= 0.25
  S/cm^2; AIS-to-soma Nav ratio >= 5) to eliminate the t0078 iter-81 collapse-to-floor failure
  mode by construction. Folded-in scope: (i) S-0078-02 substrate regression check by
  re-evaluating the t0076 iter-424 parameter vector on the v3 substrate as a one-shot
  validation cell before the NSGA-II run launches; (ii) S-0078-08 produces an answer asset
  documenting the AIS-disabled-corner failure mode and the now-enforced biological-prior
  checklist. `tau_ca_multiplier` upper bound is kept at 20x (S-0078-03 NOT folded in per
  researcher decision, to keep the substrate identical to t0078 for cleaner
  architectural-delta comparison). Pass criterion: locate at least one Pareto cell with DSI >=
  0.4 AND PD rate >= 10 Hz, OR rule it out architecturally with a clean negative result.
  Compute estimate ~$1.00 - $1.50 over ~0.8 - 1.2 h on a Vast.ai 64-core CPU; hard cap $2.00.
  Source suggestion: S-0078-01 (declared primary; S-0078-02 and S-0078-08 also covered).
  Dependencies: t0024, t0069, t0076, t0078.

## Suggestion Cleanup

* **Reject three suggestions** as covered by t0080:

  * **S-0078-01** (high) -- Add dendritic-spike machinery and re-optimise with NSGA-II under
    an AIS Nav lower-bound prior. Primary scope of t0080.
  * **S-0078-02** (medium) -- Substrate regression check by re-evaluating t0076 iter-424
    parameters on the AIS-augmented 49-d Bed B substrate. Folded into t0080 as a pre-run
    validation cell.
  * **S-0078-08** (medium) -- Investigate AIS-disabled-corner exploitation as a general
    MOBO-on-biophysics failure mode. Folded into t0080 as an answer asset documenting the
    failure mode and the now-enforced biological-prior checklist.

## Reprioritisations

None.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued for later opportunistic
  pickup; it uses a different substrate (Bed A) from t0080 and provides complementary
  one-axis-at-a-time sensitivity vs t0080's joint optimisation.

## Assets Produced

No assets in this brainstorm task. The new task t0080 will produce one library asset (the
dendritic-spike-augmented Bed B v3 variant) plus one answer asset (the AIS-disabled-corner
failure-mode write-up) and the standard results bundle (Pareto front, hypervolume trajectory,
metrics, cost record, machine log) when executed downstream.

**Results summary:**

> **Results Summary: Brainstorm Session 14**
>
> **Summary**
>
> Fourteenth strategic brainstorm, run on 2026-05-04 after t0078 (49-d AIS-augmented Bed B v2
> BoTorch
> qLogNEHVI MOBO with tier-stratified channels and slow Kv-AHP) completed. The session is
> triggered by
> the t0078 architectural diagnostic: the AIS-augmented substrate expanded the achievable
> Pareto front
> by **+36% in hypervolume** over t0076 but still missed the joint pass criterion
> `DSI >= 0.4 AND PD rate >= 10 Hz` -- the closest cell (iter 81) sits at DSI 0.316 / PD 9.68
> Hz,
> short by 0.084 on DSI and 0.32 Hz on PD. The compare-literature analysis identified two
> follow-on
> diagnostics: passive dendrites are the bottleneck on the high-DSI rail (PD ceiling pinned at
> 2.86
> Hz), and the optimiser exploited an AIS-disabled corner (nav16_ais collapsed to the search
> floor at
> 1e-5 S/cm^2, four orders below the Kole 2008 prior). Decision: commission a single bundled
> task
> t0080 (`bedb_mobo_v3_dendritic_spike_nsga2`) covering dendritic-spike machinery, NSGA-II via
> pymoo
> (replacing BoTorch qLogNEHVI), and biological hard lower bounds; reject three suggestions
> covered by
> t0080 (S-0078-01, S-0078-02, S-0078-08); no reprioritisations; no other task changes. t0075
> remains
> queued.
>
> **Session Overview**
>

</details>

<details>
<summary>✅ 0078 — <strong>Bed B v2 MOBO with AIS, tier-stratified channels, and
slow Kv-AHP</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0078_bedb_mobo_v2_ais_tiered_ahp` |
| **Status** | completed |
| **Effective date** | 2026-05-04 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0076-02` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-05-03T13:02:20Z |
| **End time** | 2026-05-04T16:25:00Z |
| **Step progress** | 15/15 |
| **Task page** | [Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Task folder** | [`t0078_bedb_mobo_v2_ais_tiered_ahp/`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/results_detailed.md) |

# Bed B v2 Multi-Objective BO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Motivation

t0076 ran a 25-d BoTorch qNEHVI multi-objective Bayesian optimisation on the Bed B (de
Rosenroll 2026\) DSGC compartmental model in NEURON, jointly maximising direction selectivity
index (DSI) and preferred-direction firing rate over 30 Sobol DoE + 400 acquisition steps (430
cell evaluations, 68,800 NEURON simulations). The headline finding is a **smooth monotone
trade-off** on the Pareto front spanning DSI in [0.003, 1.0] and PD rate in [0.4, 127.75 Hz],
with **no operating point satisfying DSI >= 0.4 AND PD rate >= 30 Hz** simultaneously. Every
Pareto cell with DSI >= 0.4 has PD rate <= 5.0 Hz; every cell with PD rate >= 30 Hz has DSI <=
0.07. The matched cell at iter 424 (DSI 0.42, PD rate 4.95 Hz) reproduces the published
deRosenroll2026 baseline (DSI 0.39) within +0.03, validating the substrate.

The t0076 compare-literature analysis identifies **three architectural omissions** that
plausibly explain the trade-off:

1. **No AIS section**. Real RGCs initiate spikes at the AIS, where Nav density is ~7x soma per
   Kole 2008 / Van Wart 2007. Bed B applies all sodium uniformly to the soma + 350 dendrites;
   the high-rate Pareto extremes (iter 319, 127.75 Hz, DSI 0.003) reflect saturated dendritic
   spiking without a directional gate.
2. **Uniform-density channels**. Real RGCs have graded Ih / Kv / Nav distributions across soma
   and dendritic tiers. The 25-d t0076 search collapses each channel to a single density
   applied everywhere, which cannot exploit the tier-specific gradients that biological cells
   use to compute direction.
3. **Absent slow-AHP machinery**. The t0076 high-rate Pareto extreme (iter 319, 127.75 Hz)
   exceeds biologically plausible mean PD rates (30 - 80 Hz per Trenholm / Borst literature)
   precisely because Bed B lacks slow Ca-activated K+ adaptation. The vendored SK and BK
   mechanisms (from Hay 2011 / Khaliq 2003 cortical / Purkinje sources) and the single-shell
   `cad` Ca pool (taur 5 ms) collectively fail to cap firing on the timescale real RGCs use.

This task closes all three architectural gaps in a single bundled MOBO run, plus folds in the
three implementation defects identified during the t0076 retrospective so the new BO loop runs
on a clean stack.

The goal is binary: locate at least one Pareto cell with **DSI >= 0.4 AND PD rate >= 30 Hz**
on the augmented Bed B substrate, OR rule out the joint operating point even with AIS +
tier-stratification + slow AHP. Either outcome is a strong project result. A success would
establish the AIS-augmented Bed B as the project's standard substrate for further
joint-optimisation work; a clean negative result would clarify that dendritic-spike machinery
is the remaining missing ingredient, redirecting the project toward dendritic-spike modelling.

This task addresses RQ1 (somatic + AIS VGC combinations for DSI / firing rate trade-off), RQ3
(AMPA / GABA ratio and spatial distribution effects), and RQ4 (active vs passive components,
now with AIS active). Source suggestion: **S-0076-02** (primary). Also covers: S-0076-01
(tier-stratified channel densities), S-0076-03 (qLogNEHVI / GP-normalise / NEURON re-init
fixes), S-0076-05 (slow Kv-mediated AHP via SK_E2), S-0024-03 (Van Wart + Werginz AIS overlay
on the deRosenroll morphology as a new library asset).

## Scope

### Substrate: AIS-augmented Bed B

Build a new library asset by forking the de Rosenroll 2026 DSGC builder from t0024 and
attaching a two-subsegment AIS at the soma:

* **AIS geometry priors (Van Wart 2007 / Werginz 2020 / Kole 2008)**:
  * AIS length 25 - 50 um (default 30 um)
  * AIS diameter ~0.8 um
  * Two subsegments: proximal (Nav1.2 + Nav1.1) and distal (Nav1.6 + Kv1.2)
  * AIS-to-soma Na ratio ~7x (the strongest single Kole 2008 prior)
* **AIS channel set**: HHst basal Na+K, Nav1.6, Kv3, Kv7. NaP, BK, SK explicitly excluded from
  the AIS section (biologically not at AIS in RGCs).
* **AIS attachment code**: lift the architecture from t0069 (which built a virtual AIS on Bed
  A); port the segment-count rule (`d_lambda = 0.1` at 100 Hz) and the section-naming
  convention.

### Slow Kv-AHP mechanism

* **Implementation**: SK_E2 with **extended Ca-binding time constant** (per researcher
  decision — smallest change, reuses the Hay 2011 SK code path that t0074 already vendored).
  Add an `extended_tau_ca` parameter to the SK_E2 MOD that lengthens the Ca-binding kinetics
  by a factor configurable per simulation (treat the multiplier as a free MOBO parameter).
* **Insertion sites**: soma + AIS only. Not all dendrites — the Hu 2007 / Shah 2008 literature
  and the t0074 result both put SK / KAHP machinery at soma + AIS-adjacent compartments rather
  than distal dendrites.

### Tier-stratified channel densities

Stratify a subset of channels (those where the literature predicts strong gradients) across 5
region tiers; keep other channels uniform:

* **Stratified channels** (5 channels x 5 tiers = 25 density parameters):
  * Nav1.6 — soma, proximal-dendrite, mid-dendrite, terminal-dendrite, AIS
  * Kv3 — same 5 tiers
  * NaP — same 5 tiers (NaP at AIS is controversial; allow the optimiser to drive it to zero)
  * BK — same 5 tiers
  * SK — same 5 tiers (orthogonal to the slow-Kv-AHP SK_E2 mechanism, which has its own peak
    conductance + tau multiplier parameters)
* **Uniform channels** (kept as in t0076): the remaining channels in the t0076 12-channel set
  (~7 channels, ~7 density parameters).
* **Slow Kv-AHP** (SK_E2 with extended Ca-binding): peak conductance + Ca-binding multiplier
  (2 parameters; insertion at soma + AIS only).
* **Synaptic placement parameters** (kept as in t0076): ~13 parameters covering AMPA / NMDA /
  GABA spatial distribution, density ratios, and per-synapse drive scaling.

**Total parameter dimensionality**: ~25 + ~7 + 2 + ~13 = **~47 d**. This sits in the 40 - 50 d
band agreed with the researcher.

### Optimiser

* **Acquisition**: `qLogNEHVI` (migrating off the deprecated
  `qNoisyExpectedHypervolumeImprovement` used in t0076). Numerically stabler than qNEHVI on
  high-dimensional inputs.
* **Input transform**: wrap GP inputs in a `Normalize` transform on `[0, 1]^d`. t0076 passed
  natural-units bounds directly to the GP and BoTorch warned the fit was suboptimal.
* **DoE**: Sobol initial design of 50 - 100 cells (larger than t0076's 30 to compensate for
  the larger input dimensionality). **Fresh restart** — no warm start from the t0076 12-cell
  Pareto front, per researcher decision.
* **Total budget**: 600 - 800 acquisition iterations after the Sobol DoE.
* **NEURON re-init fix**: launch a fresh subprocess per cell evaluation in a
  `ProcessPoolExecutor` worker, bypassing the `Exp2NMDA name already exists` non-idempotent
  loader bug. This was identified as a bug in t0076 where `plot_pareto.py` called
  `build_dsgc_cell()` multiple times in one Python process and only 1 of 3 deep-dive PNGs was
  produced.

### Stimulus protocol

* Same as t0076: 8-direction bar at 1 mm/s width 250 um with 20 seeds per direction. Per-trial
  trial_length 1400 ms (matches the standard mode trio EPSP_PASSIVE / IPSP_PASSIVE / FULL).
* Trial mode: FULL (HH on for Vm / firing rate / DSI per the project's measurement protocol).

### Width metrics (cross-comparable with t0076 + t0074)

For each cell, compute:

* `direction_selectivity_index` (registered metric)
* PD firing rate (Hz)
* `tuning_curve_hwhm_deg`
* `tuning_curve_reliability`
* `tuning_curve_rmse` vs the t0004 cosine target

### Outputs

* **Library asset**: `de_rosenroll_2026_dsgc_ais` (or similar) — Bed B + AIS variant of the de
  Rosenroll cell builder, with the AIS channel set wired in. Reusable by future tasks that
  need a working AIS-augmented Bed B substrate.
* **Pareto front**: list of non-dominated (DSI, PD rate) cells across the entire BO
  trajectory.
* **Hypervolume trajectory** plot showing convergence vs the t0076 final HV of 8.4129 (sanity
  check on the ablation).
* **Per-axis sensitivity plots**: marginal effect of each tier-stratified channel density on
  DSI and PD rate at the Pareto-best operating point.
* **Compare-literature deep-dive** comparing the AIS-augmented Bed B Pareto front to the t0076
  uniform-density front, plus to the published mouse / rabbit DSI + firing-rate values
  (Sivyer2010, PolegPolsky2016, Oesch2005, deRosenroll2026, Park2014).
* `results/metrics.json` with per-cell registered project metrics.
* `results/costs.json` with full Vast.ai cost breakdown.
* `results/remote_machines_used.json` with the Vast.ai instance metadata.

## Approach

1. **Build AIS-augmented Bed B library asset**: fork t0024's de_rosenroll_2026_dsgc cell
   builder; import the AIS-attachment architecture from t0069's Bed A AIS code; wire in HHst,
   Nav1.6, Kv3, Kv7 on the AIS section with the Van Wart 2007 priors; register as a new
   library asset.
2. **Vendor SK_E2-with-extended-Ca-binding**: clone the t0074-vendored SK_E2 MOD; add a
   `tau_ca_multiplier` parameter that scales the Ca-binding rate constants; sanity-check at
   multiplier = 1 reproduces the t0074 SK behaviour exactly.
3. **Define the 47-d parameter space**: parameter ranges for each of the 25 tier-stratified
   channel densities, 7 uniform channel densities, 2 slow-Kv-AHP parameters, 13 synaptic
   placement parameters. Use t0076 ranges for the uniform-density channels and the synaptic
   parameters; use biologically informed priors for the AIS-tier ranges (e.g., Nav1.6_AIS in
   [0.0, 1.0] S/cm^2 to span the Kole 2008 AIS prior).
4. **Migrate the BoTorch loop to qLogNEHVI**: replace `qNoisyExpectedHypervolumeImprovement`
   with `qLogNoisyExpectedHypervolumeImprovement`; wrap inputs in `Normalize`; verify GP fit
   messages are warning-free.
5. **Fix the NEURON re-init bug**: launch each cell evaluation in a fresh subprocess (already
   the default for the trial-driver; ensure `plot_pareto.py` and other deep-dive scripts also
   use subprocess-per-deep-dive).
6. **Run the BO loop**: provision a Vast.ai 72-core CPU instance similar to the t0076
   instance; run 50 - 100 Sobol DoE cells, then 600 - 800 qLogNEHVI iterations. Total ~650 -
   900 cell evaluations x 8 dirs x 20 seeds = 104,000 - 144,000 NEURON simulations; ~9 - 12 h
   wall-clock.
7. **Generate the Pareto front and hypervolume trajectory**: use the same scripts as t0076
   with the subprocess-per-deep-dive fix.
8. **Generate per-axis sensitivity plots and compare-literature**: identify the Pareto-best
   joint operating point (max DSI s.t. PD rate >= 30 Hz, or max PD rate s.t. DSI >= 0.4); for
   each tier-stratified channel, plot DSI / rate / HWHM as a function of that channel's
   density at the best-joint values of all other parameters.
9. **Validate against the t0076 Pareto front**: confirm hypervolume monotonically increases
   over the t0076 final HV of 8.4129 by the end of the run; if not, the new architecture has
   not improved on the bare 25-d substrate and the negative result is reported with that
   diagnostic.

## Pass Criteria

**Primary (binary)**: locate at least one Pareto cell with **DSI >= 0.4 AND PD rate >= 30
Hz**, OR rule it out by demonstrating the Pareto front converges with no such cell after >=
600 acquisition iterations and HV >= 1.5x the t0076 final HV.

**Secondary**:

* All cell evaluations complete with `is_unstable = False` (peak Vm in [-80, +60] mV at every
  trial).
* Hypervolume monotonically increases from the Sobol baseline through the qLogNEHVI
  iterations.
* The matched cell at the Pareto-best joint operating point reproduces the t0076 best-joint
  cell (iter 424 DSI 0.42 PD rate 4.95 Hz) within +/-0.05 DSI and +/-1 Hz at matching
  parameter values — a sanity check that the new AIS / slow-AHP / tier-stratification
  machinery does not regress on the t0076 baseline at trivial parameter settings.
* `verify_machines_destroyed` passes after the Vast.ai instance teardown.
* `verify_pr_premerge` passes with 0 errors.

## Compute Estimate

Extrapolating from the t0076 measurement ($1.0583 over 6.4697 h on Vast.ai 72-core CPU for 430
cells x 8 dirs x 20 seeds = 68,800 NEURON simulations at 25 d):

* New cell count: 650 - 900 cells (50 - 100 Sobol + 600 - 800 qLogNEHVI).
* New trial count: 104,000 - 144,000 NEURON simulations.
* Per-trial wall-clock: similar to t0076 (~3.4 s per trial including AIS overhead, ~10% slower
  than t0076's ~3.1 s).
* Total NEURON wall-clock: 104,000 - 144,000 trials / 72 cores * 3.4 s/trial ~= 4900 - 6800 s
  of per-core trial time, parallelised across 72 cores ~= 9.7 - 13.6 h.
* Total Vast.ai cost at $0.16357 /hr (t0076 instance type): **$1.59 - $2.22**.
* Add 20% contingency for BoTorch acquisition computation time on the larger input
  dimensionality and for any retry / restart overhead: **$1.91 - $2.66**.
* Round up to budget cap: **$3.50** (well within the $8.94 remaining project budget).

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` — Bed B substrate (de_rosenroll_2026_dsgc library asset;
  the cell builder that this task forks).
* `t0069_t0067_ais_localised_channel_sweep` — Bed A AIS attachment architecture and
  segment-count conventions.
* `t0076_bedb_dsi_firing_rate_mobo` — BoTorch MOBO harness, ProcessPoolExecutor trial driver,
  Vast.ai provisioning scripts.

## Remote Machines

One Vast.ai 72-core CPU instance (matching t0076's instance type: Xeon E5-2686 v4 or similar
at ~$0.16 /hr) for ~9 - 12 h of BO loop wall-clock plus ~30 min provisioning + ~30 min
teardown + deep-dive plotting.

## Risks and Fallbacks

* **AIS section adds significant per-trial wall-clock overhead**: mitigation via NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) — discretise the AIS just
  enough to capture spike initiation without inflating compartment count beyond ~5 - 10
  segments. If wall-clock grows by more than 25%, reduce DoE size from 100 to 50 and target
  600 acquisition iterations.
* **GP fit becomes unstable on 47 d**: BoTorch qLogNEHVI is more numerically stable than
  qNEHVI on high dimensions. If the GP fit still warns or fails, drop the per-tier
  stratification on channels with weak literature gradients (NaP, BK) — keeping only Nav1.6,
  Kv3, SK stratified brings the count to ~35 d, restoring t0076-like behaviour.
* **No DSI >= 0.4 AND PD rate >= 30 Hz Pareto cell found**: this is a clean negative result.
  The task records the result, generates a compare-literature deep-dive identifying which
  architectural ingredient (AIS / tier-stratification / slow Kv-AHP) was insufficient, and
  proposes dendritic-spike machinery as the next architectural extension for a follow-up task.
* **NEURON `Exp2NMDA name already exists` re-init bug returns**: ensure
  subprocess-per-deep-dive is in place for plot_pareto.py and any post-hoc scripts that
  re-instantiate the cell. Verify by running plot_pareto.py at >= 3 deep-dive cells and
  confirming all PNGs are produced.
* **Vast.ai instance availability or pricing shifts**: fall back to a different 72-core CPU
  instance type at <= $0.20 /hr; if no comparable instance is available, run on local CPU at
  reduced iteration count (300 acquisitions) and report the partial result with the truncation
  documented.
* **AIS Nav1.6 density priors do not match Kole 2008 in any Pareto cell**: report the
  optimiser's preferred density range; flag cells where AIS Nav1.6 falls outside [0.25, 0.5]
  S/cm^2 (the Kole 2008 prior) as biologically marginal in compare-literature; do not
  constrain the search space to the prior, since one of the questions is whether biologically
  plausible densities reach the joint operating point.

## Out of Scope

* **Bed A** — t0078 is Bed B only. The t0075 task (still not_started at the time of t0077)
  covers the equivalent AIS extension on Bed A under one-axis-at-a-time sensitivity analysis.
* **Joint optimisation of synaptic mechanism types** — t0078 keeps the deRosenroll 2026
  synaptic protocol fixed (correlated SAC release model); only the synaptic placement
  parameters are free.
* **Dendritic-spike machinery (Nav1.2 / Nav1.6 / NaP on dendrites at high density)** — the
  tier-stratified Nav1.6 and NaP densities are free, but no explicit "dendritic-spike
  enabling" code path is added. If the negative result indicates dendritic spikes are
  required, that architectural extension is the natural follow-up.
* **t0076 contradiction-test isolation experiment (S-0076-04)** — the contradiction between
  t0068 (Nav1.6 + Kv3 jointly rescues DSI + rate on Bed A) and t0076 (no such cell on Bed B
  25-d) is not directly tested here; t0078's tier-stratified search may or may not reveal a
  Bed B Nav1.6 + Kv3 rescue, but that is an emergent finding rather than the task's primary
  goal.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
> date_completed: "2026-05-04"
> status: "complete"
> ---
> **Results Summary: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP**
>
> **Summary**
>
> Ran a 49-d BoTorch qLogNEHVI multi-objective Bayesian optimisation on the AIS-augmented de
> Rosenroll
> 2026 Bed B DSGC compartmental model in NEURON, jointly maximising direction selectivity
> index (DSI)
> and preferred-direction (PD) firing rate over 75 Sobol DoE + 416 acquisition iterations (491
> total
> cell evaluations × 8 directions × 20 seeds = **78,560** NEURON simulations) on a Vast.ai
> 64-core
> CPU instance for **$3.93** (24.86 h total). The loop was stopped early via SIGTERM at acq
> 416 (vs
> the planned 700) per researcher decision after the hypervolume curve plateaued and per-cell
> wall-clock grew super-linearly under O(N³) GP-fit scaling. **The 49-d substrate produces a
> Pareto
> front with 17 non-dominated cells and final hypervolume 11.41**, exceeding the t0076 final
> HV (8.41)
> by **+36%**. The pass criterion (`DSI ≥ 0.4 AND PD ≥ 10 Hz`) was **narrowly missed**: the
> closest Pareto cell (iter 81) has **DSI 0.316, PD 9.68 Hz** — short by 0.084 on DSI and 0.32
> Hz on

</details>

## 2026-05-03 (3)

## ✅ Completed

<details>
<summary>✅ 0077 — <strong>Brainstorm results session 13</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0077_brainstorm_results_13` |
| **Status** | completed |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md), [`t0073_brainstorm_results_12`](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-03T11:00:00Z |
| **End time** | 2026-05-03T12:55:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 13](../../../overview/tasks/task_pages/t0077_brainstorm_results_13.md) |
| **Task folder** | [`t0077_brainstorm_results_13/`](../../../tasks/t0077_brainstorm_results_13/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0077_brainstorm_results_13/results/results_detailed.md) |

# Brainstorm Session 13: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

Thirteenth brainstorming session. Run on 2026-05-03 after t0074 (channel tuning-width sweep on
Bed A) and t0076 (25-d Bed B BoTorch qNEHVI multi-objective Bayesian optimisation) both
completed. The session is triggered by the t0076 headline negative result: the bare 25-d Bed B
(de Rosenroll 2026) substrate cannot reach a biologically realistic joint operating point of
DSI >= 0.4 AND PD rate >= 30 Hz, with every Pareto cell trading off severely between the two
objectives. The t0076 compare-literature analysis identified three architectural omissions
that plausibly explain the trade-off: (a) no AIS section, (b) uniform-density channels rather
than tier-stratified densities (real RGCs have ~50x higher Nav at AIS than soma per Kole
2008), and (c) absent slow-AHP machinery to cap the high-rate Pareto extremes (iter 319
reached 127.75 Hz with DSI = 0.003).

## Decisions

* **Create t0078** — `bedb_mobo_v2_ais_tiered_ahp`. Bed B v2 multi-objective Bayesian
  optimisation that bundles three high-priority follow-ups in a single run: build an AIS
  section onto Bed B (S-0 076-02; covers S-0024-03 as the AIS library asset), tier-stratify
  channel densities into 5 tiers per Nav1.6 / Kv3 / NaP / BK / SK (S-0076-01), and add a slow
  Kv-mediated AHP via SK_E2 with extended Ca-binding as a new optimisation parameter
  (S-0076-05). Migrate the BoTorch loop to qLogNEHVI, wrap GP inputs in Normalize on [0, 1]^d,
  and fix the NEURON `Exp2NMDA name already exists` re-init bug via subprocess-per-deep-dive
  (covers S-0076-03). 40 - 50 d total parameter space. Restart fresh with Sobol DoE +
  qLogNEHVI (no warm-start from t0076). Pass criterion: locate at least one Pareto cell with
  DSI >= 0.4 AND PD rate >= 30 Hz, OR rule it out architecturally. Compute estimate ~$2.50 -
  $4.00 over 9 - 12 h on a Vast.ai 72-core CPU (well within the $8.94 remaining budget).
  Source suggestion: S-0076-02 (declared primary; S-0076-01, S-0076-03, S-0076-05, and
  S-0024-03 also covered).

* **Cancel t0045** — `coreneuron_vastai_speedup_benchmark`. The task was originally framed as
  the 5x CoreNEURON-on-GPU vs stock-NEURON-on-CPU benchmark to validate the assumption baked
  into t0033's cost model. t0076 has now actually run on a Vast.ai 72-core CPU instance for
  $1.0583 over 6.4697 h with 68,800 NEURON simulations and produced useful science, validating
  that stock NEURON on Vast.ai CPU is cost-feasible for the project's scale. The original
  urgency (the t0033 cost-model uncertainty) is gone, and CoreNEURON-on-GPU is no longer
  load-bearing for any planned task. The benchmark retains academic interest but is not on the
  project's critical path.

## Suggestion Cleanup

* **Reject four high-priority suggestions** as covered by t0078:

  * **S-0076-01** — tier-stratified channel densities. Folded into t0078 as the 5-tier
    expansion of the input space.
  * **S-0076-02** — AIS-augmented Bed B MOBO. Primary scope of t0078.
  * **S-0076-03** — three implementation fixes (qLogNEHVI migration, GP input normalisation,
    NEURON re-init bug). Folded into t0078 as required infrastructure for the new MOBO to run
    cleanly.
  * **S-0076-05** — slow Kv-mediated AHP mechanism. Folded into t0078 as the new optimisation
    parameter; SK_E2 with extended Ca-binding chosen as the implementation per researcher
    decision.

* **Reject one medium-priority suggestion** as covered by t0078:

  * **S-0024-03** — Van Wart + Werginz AIS overlay on the deRosenroll morphology. The AIS
    section construction is part of t0078's scope; the resulting AIS-augmented Bed B will be
    registered as a new library asset by t0078 (`de_rosenroll_2026_dsgc_ais` or similar).

* **Reject eleven high-priority suggestions** as stale (from-scratch DSGC family, t0052 -
  t0059): the project has pivoted to deposited Bed A (t0008) and Bed B (t0024) substrates
  where biological grounding is stronger. Recent work (t0067 - t0076) operates exclusively on
  the deposited beds. The from-scratch family remains in a binary regime
  (single-spike-trivial-DSI or full-suppression-zero-DSI) and these eleven follow-ups are no
  longer load-bearing for the project's research questions.

  S-0052-01 (AMPA per-synapse conductance sweep on t0052), S-0052-02 (GABA-synapse-count sweep
  on t0052), S-0054-02 (3D gAMPA / gNMDA / gGABA sweep on t0054), S-0055-02 (re-run t0055
  Mg-block sweep on corrected protocol), S-0055-03 (GABA-reduction ladder on Mg-block t0055),
  S-0057-06 (tonic GABA + Mg-block NMDA on t0054-style), S-0059-01 (active dendritic
  conductances on t0059), S-0059-02 (Mg-block NMDA + bar-locked tonic GABA on t0059),
  S-0059-03 (synapse-count scaling on t0059), S-0065-02 (match from-scratch GABA reversal to
  v_rest), S-0066-02 (EPSP / IPSP / FULL protocol on from-scratch family).

## Tasks Cancelled or Updated

* **Cancelled**: t0045 (CoreNEURON benchmark; superseded by t0076 actual Vast.ai run).
* **Updated**: none.

## Assets Produced

No assets in this brainstorm task. The new task t0078 will produce one library asset (the
AIS-augmented Bed B variant) plus the standard results bundle (Pareto front, hypervolume
trajectory, metrics, cost record, machine log) when executed downstream.

**Results summary:**

> **Results Summary: Brainstorm Session 13**
>
> **Summary**
>
> Thirteenth strategic brainstorm, run on 2026-05-03 after t0074 (channel tuning-width sweep
> on Bed A)
> and t0076 (25-d Bed B BoTorch qNEHVI multi-objective Bayesian optimisation) both completed.
> The
> session is triggered by the t0076 headline negative result: the bare 25-d Bed B substrate
> cannot
> reach DSI >= 0.4 AND PD rate >= 30 Hz simultaneously, with every Pareto cell trading off
> severely
> between the two objectives. The t0076 compare-literature analysis identified three
> architectural
> omissions that plausibly explain the trade-off: no AIS section, uniform-density channels,
> and absent
> slow-AHP machinery. Decision: commission a single bundled MOBO task (t0078
> `bedb_mobo_v2_ais_tiered_ahp`) covering all three architectural fixes plus the t0076
> implementation
> defects; reject sixteen suggestions (five covered by t0078, eleven stale from-scratch-family
> follow-ups); cancel t0045 (CoreNEURON-on-GPU benchmark) as superseded by t0076's actual
> Vast.ai-CPU
> run; no reprioritisations; no new suggestions; no answer assets.
>
> **Session Overview**
>
> Date: 2026-05-03. Triggered by the t0076 headline negative result and the convergent
> compare-literature analysis pointing to AIS / tier-stratification / slow-AHP as the missing

</details>

<details>
<summary>✅ 0076 — <strong>Multi-objective BO of channels + synapse placement on
Bed B (max DSI + max firing rate)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0076_bedb_dsi_firing_rate_mobo` |
| **Status** | completed |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-05-02T20:20:04Z |
| **End time** | 2026-05-03T04:18:00Z |
| **Step progress** | 13/15 |
| **Task page** | [Multi-objective BO of channels + synapse placement on Bed B (max DSI + max firing rate)](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Task folder** | [`t0076_bedb_dsi_firing_rate_mobo/`](../../../tasks/t0076_bedb_dsi_firing_rate_mobo/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0076_bedb_dsi_firing_rate_mobo/results/results_detailed.md) |

# Multi-objective Bayesian optimisation of channels + synapse placement on Bed B

## Motivation

The project has two well-characterised DSGC model beds (Bed A: t0008 deposited Poleg-Polsky;
Bed B: t0024 de Rosenroll port) and a thorough understanding of how individual channels and
synapse subsystems behave (t0019 literature survey, t0067 single-channel soma sweep, t0068
co-expression rescue test, t0069 AIS sweep, t0070/t0071 writeup, t0072 per-synapse traces).
None of this work has yet asked the headline scientific question: **what combination of
voltage-gated channels and synaptic input placement gives the best joint trade-off between
direction selectivity (DSI) and firing rate?** This task answers that for Bed B.

We fix the de Rosenroll morphology (the geometric structure has already been characterised in
the t0029/t0034 dendrite sweeps — it is not the bottleneck for direction selectivity).
Channels and synapses are the search space.

## Scope

* **Cell substrate**: Bed B (t0024 de Rosenroll port). Morphology fixed (1 soma + 350
  dendrites, 10,649 `pt3dadd` points; built once via `build_dsgc_cell()` from the registered
  `de_rosenroll_2026_dsgc` library asset).
* **Search dimensions**: 25 free parameters (see Parameters section).
* **Objectives**: 2 (DSI and PD firing rate) — both maximised.
* **Optimisation algorithm**: multi-objective Bayesian optimisation via BoTorch's qNEHVI
  acquisition function (q-noisy expected hypervolume improvement). Multi-output Gaussian
  Process surrogate.
* **Compute platform** (REQUIRED): **Vast.ai 64-core CPU node**. Local-workstation execution
  is not acceptable for this task — the optimisation needs ~64-way trial-level parallelism to
  keep per-iteration wall time at ~30 s. The task plan therefore includes the canonical
  `setup-machines` and `teardown` steps; the `/setup-remote-machine` skill provisions the
  Vast.ai instance, installs the project's NEURON + Python environment via the standard `uv
  sync` flow, runs the optimisation, downloads results, and destroys the instance. No work
  runs on the local workstation beyond orchestration of the SSH session.
* **Per-iteration cost**: 8 directions × 20 seeds = 160 trials × ~3 s wall ≈ ~30 s on the
  Vast.ai 64-core node (`ProcessPoolExecutor` over trials).
* **Total compute budget**: 300-500 iterations × ~30 s ≈ **2.5-4 h wall on the Vast.ai 64-core
  node**.

## Parameters (25 free)

| # | Category | Parameter | Range | Notes |
| --- | --- | --- | --- | --- |
| 1-12 | **Channel densities** (`gbar`, S/cm²) | One per channel, log-uniform: Nav1.6, NaP, NaR, Kdr, Kv3, Kv4, KM, HCN, CaL, CaT, BK, SK | 1e-5 - 0.5 | Single density across the cell; tier-stratification deferred. |
| 13 | **Passive** | `Ra` (Ω·cm) | 50 - 250 | Linear |
| 14 | **Passive** | `cm` (µF/cm²) | 0.5 - 2.0 | Linear |
| 15 | **Passive** | `gleak` (S/cm²) | 1e-5 - 1e-3 | Log-uniform |
| 16 | **Calcium** | `cad.depth` (µm) | 0.05 - 0.5 | Internal Ca shell depth |
| 17 | **Calcium** | `cad.taur` (ms) | 5 - 100 | Ca extrusion time constant |
| 18 | **Synapse count** | `N_ACh` (int) | 50 - 350 | Total ACh terminals; default 177 |
| 19 | **Synapse count** | `N_GABA` (int) | 50 - 350 | Total GABA terminals; default 177 |
| 20 | **Synapse spatial rule** | `rho_0_ACh` (rel.) | 0.1 - 5.0 | Density at soma for ρ(d) = ρ_0 · exp(-d/λ) |
| 21 | **Synapse spatial rule** | `lambda_ACh` (µm) | 30 - 500 | Spatial decay length for ACh |
| 22 | **Synapse spatial rule** | `rho_0_GABA` (rel.) | 0.1 - 5.0 | Density at soma for GABA |
| 23 | **Synapse spatial rule** | `lambda_GABA` (µm) | 30 - 500 | Spatial decay length for GABA |
| 24 | **Synapse weight** | `w_ACh` (µS) | 1e-4 - 1e-2 | NetCon weight for ACh; default 0.003 |
| 25 | **Synapse weight** | `w_GABA` (µS) | 1e-4 - 1e-2 | NetCon weight for GABA; default 0.003 |

Channel kinetics (V_half, τ) are NOT optimised — they are fixed at literature values per
t0019, with MOD files vendored from t0067 (5 channels: Nav1.6, NaP, NaR, Kv3, Kv4) plus 6 new
MODs to vendor in this task (Kdr, KM, HCN, CaL, CaT, BK, SK — see Risks fallback if any prove
hard to source).

Reversal potentials (E_Na, E_K, E_Ca, E_GABA) are fixed by physics and NOT optimised.

## Objectives (2)

| Objective | Direction | Definition |
| --- | --- | --- |
| **DSI** (direction selectivity index) | **maximise** | `(spike_pd - spike_nd) / (spike_pd + spike_nd)`, where `spike_pd` and `spike_nd` are mean spike counts across 20 seeds at the preferred direction (0°) and null direction (180°) respectively. Range: [-1, +1]; perfect DSGC ≈ 1. |
| **PD firing rate** | **maximise** | Mean spike count over 1000 ms at the PD direction (0°), averaged across 20 seeds. In Hz: divide by 1.0 s. |

The optimiser produces a **Pareto front** — the set of cell configurations where no other
configuration is simultaneously better on both DSI and firing rate. The user picks the
operating point afterward based on biological constraints (e.g., "I need DSI ≥ 0.7 with firing
rate ≥ 30 Hz" → the Pareto front shows whether that point is achievable and what configuration
reaches it).

Although the user is NOT optimising for cytoplasm volume (morphology is fixed → cytoplasm
volume is constant), the task records cytoplasm volume per cell for completeness; it just
doesn't enter the objective function.

## Approach

1. **Vendor 6-7 new MOD files** from canonical published sources (ModelDB, Allen Institute)
   into `code/mods/`: Kdr, KM (Kv7), HCN (Ih), CaL (CaV1.x), CaT (CaV3.x), BK (KCa1.1), SK
   (KCa2). Plus the existing 5 from t0067 (Nav1.6, NaP, NaR, Kv3, Kv4) copied verbatim.
   Compile to a t0076-local `nrnmech.dll`.
2. **Add the `cad` calcium-accumulation mechanism** if not already in the de Rosenroll port
   (needed because BK and SK depend on intracellular [Ca²⁺]).
3. **Write the parametric synapse placer**: given (`N_type`, `ρ_0`, `λ`), draw N positions
   along the dendritic tree with density proportional to `exp(-d/λ)` where `d` is the path
   distance from the soma. Use `sec.distance()` to compute path distance per section midpoint.
4. **Write the trial driver**: takes a 25-d parameter vector → builds the parametric cell →
   runs 8 directions × 20 seeds (160 trials) via `ProcessPoolExecutor` over directions × seeds
   on a 64-core CPU → returns (DSI, PD firing rate).
5. **Wire up BoTorch qNEHVI**: 25-d input space, 2-d output space, multi-task GP, qNEHVI
   acquisition with reference point at (DSI=0, rate=0). Initial design-of-experiments: 30
   Sobol-sampled cells. Optimisation loop: 300-500 acquisition steps.
6. **Plot the Pareto front** at iteration 50, 100, 200, 300, ..., final. Show how the front
   converges. Highlight 3-5 representative cells from the front in detail (parameter values,
   tuning curves, spike rasters, synaptic conductance traces — reusing the t0072 recorder).
7. **Render writeup as markdown + Typst PDF** (consistent with t0070-t0072).

The orchestrator wraps steps 1-7 between a `setup-machines` step (provisions the Vast.ai node,
installs NEURON + uv-managed deps, compiles the t0076 MOD library on the remote) and a
`teardown` step (downloads all results back to the local task folder, destroys the Vast.ai
instance, updates `results/costs.json` and `results/remote_machines_used.json` with the actual
billed amount).

## Cost estimation

* **Compute platform**: Vast.ai 64-core CPU instance (no GPU needed — see Risk #2 if 64-core
  CPU nodes are unavailable in the chosen region).
* **External costs**:
  * Vast.ai 64-core CPU node typical pricing: $0.20 - $0.60 / hr (varies by host, region, bid
    vs on-demand).
  * Run duration: 2.5-4 h compute + ~10-20 min provisioning/install + ~5 min teardown.
  * **Expected billed total: $0.75 - $3.00 for the optimisation run**, plus ~$0.10 - $0.30 for
    the provisioning overhead.
  * Budget cap: $5.00 (conservative — if the run exceeds this, the implementation step halts
    and writes an intervention file).
* Disk: ~50-200 MB for raw per-iteration trial summaries (no per-synapse traces saved per
  iteration to keep size down — only the 3-5 best Pareto cells get full traces). Output is
  rsync-pulled back to the local task folder during teardown.
* Time:
  * MOD vendoring + driver code (local human time): ~6-10 h.
  * Optimisation run on Vast.ai 64-core: ~2.5-4 h wall, billed.
  * Plotting + analysis + PDF (local human time, post-teardown): ~2-3 h.
  * Total: ~12-18 h human-time + ~$1-3 cloud spend.

## Dependencies

* `t0008_port_modeldb_189347` — Bed B reuses Poleg-Polsky's morphology.
* `t0019_literature_survey_voltage_gated_channels` — V_half / τ priors for the 12 channels.
* `t0024_port_de_rosenroll_2026_dsgc` — Bed B itself; entry point `build_dsgc_cell()`.
* `t0066_t0024_epsp_ipsp_vm_protocol` — direction-encoding mechanism on Bed B (bar angle).
* `t0067_t0065_soma_channel_addition_sweep` — provides 5 vendored MODs to copy verbatim.
* `t0070_writeup_two_model_beds` — reference writeup (cite for context).
* `t0072_synaptic_traces_pd_nd` — per-synapse recorder pattern + Typst PDF pipeline.

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | One or more of the 6 new MOD files (Kdr, KM, HCN, CaL, CaT, BK, SK) cannot be sourced from a clean published implementation. | Vendor step fails on a specific channel. | Drop to 8 channels (HHst's built-in Na/Kdr/leak + the 5 t0067 channels) and document the reduction in the writeup. The optimisation framework (BoTorch + driver) doesn't care about the channel count — only the parameter dimension changes. |
| 2 | Vast.ai has no 64-core CPU node available in the requested region/price tier at provisioning time. | `setup-machines` step's instance search returns 0 matches. | Try adjacent regions; relax the price cap (typical 64-core nodes are $0.20-$0.60/hr); or accept a 32-core node (run wall doubles to ~5-8 h, still tractable). Do NOT fall back to local-workstation execution — this task is explicitly cloud-compute. If no remote node is available within the $5 budget cap, write an `intervention/` file and stop. |
| 3 | BoTorch qNEHVI fails to converge in 500 iterations (Pareto front still expanding). | Manually inspect the front at iter 100, 200, 400; check the hypervolume metric for monotonic increase. | Switch to NSGA-II via DEAP/pymoo (more iterations needed but more robust). Cap at 5000 trials. |
| 4 | Calcium dynamics make the cell numerically unstable at extreme channel-density combinations. | Trial errors out with NaN voltage or NEURON solver complaint. | Catch the exception, return a worst-case score (DSI = -1, rate = 0) so the optimiser learns to avoid that region. |
| 5 | Stochastic per-trial noise on DSI is large enough that the GP can't learn (DSI estimates have SE > 0.1). | High GP residual variance after 50 iterations. | Increase seeds per direction from 20 to 40 (doubles per-iteration time). Or use a noise-aware GP kernel (BoTorch's HeteroscedasticGP). |
| 6 | The parametric synapse placer (exponential decay) is too restrictive; the optimal cell needs a non-monotonic spatial pattern. | Best-Pareto cells cluster at parameter-bound extremes. | Add a quadratic term to the spatial rule (`ρ(d) = ρ_0 · exp(-d/λ) · (1 + α · d²)`) — adds 2 params per type, total dim = 29. |
| 7 | Adding `botorch` + `gpytorch` + `torch` to `pyproject.toml` is a large dependency footprint (~2 GB). | uv sync slow / disk concern. | Acceptable cost for the gain; document in the writeup. Alternative: use Ax (lighter wrapper around BoTorch) or scikit-optimize (much smaller, less powerful). |

## Verification criteria

* All 25 free parameters have explicit log/linear bounds documented.
* The driver handles a NaN/error trial gracefully (worst-case-score fallback).
* The Pareto front contains at least 5 distinct cell configurations after 200 iterations.
* Hypervolume metric is monotonically increasing across iterations (modulo small noise).
* At least 3 representative Pareto cells have full diagnostic traces saved (tuning curve,
  spike raster, synaptic conductances).
* All standard verificators pass.
* The writeup PDF embeds the Pareto front figure and at least 3 representative-cell figures.

## Task Requirement Checklist

* **REQ-1** — 12 voltage-gated channel mechanisms vendored or implemented (or 8 if MOD-vendor
  fallback is invoked, with documented justification).
* **REQ-2** — Parametric synapse placer takes (N, ρ_0, λ) and produces a valid synapse
  placement with the requested density pattern.
* **REQ-3** — Trial driver runs 8 directions × 20 seeds for any 25-d parameter vector and
  returns (DSI, PD firing rate). Handles NaN errors gracefully.
* **REQ-4** — BoTorch qNEHVI optimiser wired up and runs ≥ 300 iterations.
* **REQ-5** — Pareto front + hypervolume trajectory plotted; saved to `results/images/`.
* **REQ-6** — At least 3 representative Pareto cells documented in detail (parameter values,
  tuning curves, spike traces).
* **REQ-7** — `results/results_summary.md` + `results_detailed.md` (with the mandatory
  sections per the results spec) + Typst PDF.
* **REQ-8** — All standard verificators pass.
* **REQ-9** — `pyproject.toml` updated with `botorch`, `gpytorch`, `torch` (and any related
  deps) cleanly.
* **REQ-10** — A documented "next steps" suggestion: tier-stratify the channel densities of
  the best 3 Pareto cells and re-optimise locally (extends the search to ~40 dim).
* **REQ-11** — All compute (cell builds, NEURON sims, BoTorch acquisition steps) runs on the
  Vast.ai 64-core node, NOT on the local workstation. The local workstation only orchestrates
  the SSH session, holds the task folder, and pulls results back during teardown.
* **REQ-12** — `results/costs.json` records the actual Vast.ai bill (≤ $5.00) and
  `results/remote_machines_used.json` records the instance ID, GPU/CPU specs (no GPU
  expected), hourly rate, total billed time, and provisioning + teardown timestamps.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0076_bedb_dsi_firing_rate_mobo"
> date_completed: "2026-05-03"
> status: "complete"
> ---
> **Multi-Objective BO of Channels + Synapse Placement on Bed B**
>
> **Summary**
>
> Ran a 25-parameter BoTorch qNEHVI multi-objective Bayesian optimisation on the Bed B (de
> Rosenroll
> 2026\) DSGC compartmental model in NEURON, jointly maximising direction selectivity index
> (DSI) and
> preferred-direction firing rate over 30 Sobol DoE + 400 acquisition steps (430 total cell
> evaluations × 8 directions × 20 seeds = **68,800** NEURON simulations) on a Vast.ai 72-core
> CPU
> instance for **$1.0583**. Hypervolume climbed monotonically from **3.4083** (Sobol baseline)
> to
> **8.4129** (final, **+147%**), and the converged Pareto front spans DSI ∈ **[0.003, 1.0]** ×
> PD rate
> ∈ **[0.4, 127.75 Hz]**. The headline finding is that the 25-d Bed B search **cannot reach a
> biologically realistic joint operating point of DSI ≥ 0.4 AND PD rate ≥ 30 Hz**: every
> Pareto cell
> with DSI ≥ 0.4 has PD rate ≤ **5.0 Hz**, and every cell with PD rate ≥ 30 Hz has DSI ≤
> **0.07**,
> revealing an inherent architectural trade-off in the substrate.

</details>

## ❌ Cancelled

<details>
<summary>❌ 0045 — <strong>CoreNEURON Vast.ai RTX 4090 speedup benchmark</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0045_coreneuron_vastai_speedup_benchmark` |
| **Status** | cancelled |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0033-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`baseline-evaluation`](../../../meta/task_types/baseline-evaluation/) |
| **End time** | 2026-05-03T12:55:00Z |
| **Task page** | [CoreNEURON Vast.ai RTX 4090 speedup benchmark](../../../overview/tasks/task_pages/t0045_coreneuron_vastai_speedup_benchmark.md) |
| **Task folder** | [`t0045_coreneuron_vastai_speedup_benchmark/`](../../../tasks/t0045_coreneuron_vastai_speedup_benchmark/) |

# CoreNEURON Vast.ai RTX 4090 Speedup Benchmark

## Source Suggestion

S-0033-01 (CoreNEURON Vast.ai RTX 4090 benchmark to validate or replace the assumed 5x speedup
in the t0033 cost model).

## Motivation

The t0033 planning task estimated a $50.54 central Vast.ai budget for the future joint DSGC
morphology + top-10 VGC DSI-maximisation optimiser. That estimate rests on an unvalidated
CoreNEURON-on-GPU-over-stock-CPU-NEURON speedup factor of 5x (91 s deterministic sim on RTX
4090 vs 456 s on single CPU core). The corpus documents Hines 1997 O(N) cable-solver scaling
but predates GPU NEURON variants, so the 5x figure is a literature-less guess that drives the
largest sensitivity-band column ($23–$119 under 0.5x–2x perturbations).

Brainstorm session 8 (t0040) considered offloading t0041–t0044 to Vast.ai to cut wall-clock,
and rejected that plan because the per-task compute is small and the 5x speedup is
unvalidated. This task directly addresses the validation gap: run a short, well-scoped Vast.ai
experiment that replaces the 5x assumption with a measured value and tightens (or widens) the
$23–$119 sensitivity band before the joint optimiser is commissioned.

This also exercises the project's Vast.ai provisioning workflow for the first time (total
project spend to date: $0.00 / $1.00), surfacing any setup issues before the far more
expensive t0033 optimiser run.

## Objective

Provision one Vast.ai RTX 4090 instance under the existing `setup-remote-machine` filters.
Build CoreNEURON against NEURON 8.2.7 with OpenACC / CUDA. Run the t0022 deterministic
12-angle x 10-trial protocol (same sim used in t0022 baseline) under:

1. Stock NEURON on CPU (single core).
2. CoreNEURON on GPU (RTX 4090).

Report wall-clock per sim, throughput (sims/hour), measured speedup factor, cost per sim in
USD at RTX 4090 Vast.ai rate, and a recommended replacement value for t0033's 5x assumption.
Produce one answer asset capturing the measured speedup and its implications for the t0033
cost envelope.

## Scope

* One Vast.ai RTX 4090 instance. Estimated wall-clock 1–3 h; estimated cost $2–5 at $0.50/h.
* Use t0022's `trial_runner` unchanged; do not modify biophysics or protocol.
* Match stock-NEURON and CoreNEURON runs trial-for-trial for apples-to-apples comparison.
* Record provisioning time and setup friction separately so the t0033 plan can budget for it.

## Out of Scope

* Multi-GPU scaling (t0033 assumes single-GPU).
* A100 / H100 benchmarks (cost column in t0033 already recomputes from measured RTX 4090
  speedup).
* CPU-96 many-core benchmark (t0033 already recommends ignoring that column).
* Any morphology or channel modifications (pure runtime benchmark).

## Deliverables

* `assets/answer/coreneuron-rtx4090-speedup-vs-stock-neuron/` — full answer asset with
  measured speedup, per-sim cost, and recommended t0033 budget update.
* `results/results_summary.md` and `results/results_detailed.md` with Methodology, Metrics,
  Comparison vs Baselines (5x assumption), and Next Steps.
* `results/metrics.json` with: `stock_neuron_s_per_sim`, `coreneuron_s_per_sim`,
  `speedup_factor`, `coreneuron_usd_per_sim`, `provisioning_minutes`, `setup_minutes`.
* `results/compare_literature.md` comparing the measured speedup to Hines 1997 cable-solver
  scaling expectations and any CoreNEURON GPU benchmarks found in the corpus.
* `results/suggestions.json` with at minimum a follow-up proposing a correction to t0033's
  answer asset if the measured speedup differs from 5x by more than 20%.
* `results/costs.json` and `results/remote_machines_used.json` with the full Vast.ai
  provisioning record.

## Anticipated Risks

* **Vast.ai provisioning may fail or block on verification**: the project has never
  provisioned a Vast.ai instance; the `setup-remote-machine` skill may hit unexpected
  friction. Budget extra time for first-run troubleshooting and record every setup step for
  future tasks.
* **CoreNEURON build may require NEURON 8.2.7 patch or a newer version**: if CoreNEURON does
  not build cleanly against the project's NEURON version, document the workaround or flag the
  task as intervention_blocked rather than silently bumping the NEURON version.
* **Deterministic-reproducibility caveat**: stock NEURON on CPU and CoreNEURON on GPU may not
  produce bit-identical spike trains due to floating-point ordering differences; report the
  max-spike-time-deviation and any DSI delta explicitly so the t0033 optimiser knows whether
  GPU and CPU runs are substitutable.
* **Cost overrun**: hard-cap the instance runtime at 3 hours. If the benchmark cannot finish
  within the cap, post-mortem the provisioning and setup overhead and re-scope before a second
  attempt.

## Verification Criteria

* `measured_speedup_factor` is reported with both mean and 95% CI.
* `coreneuron_usd_per_sim` is reported at the actual Vast.ai instance rate at runtime (not the
  snapshot rate from t0033).
* At least one answer asset is produced per the answer specification.
* If the measured speedup differs from 5x by more than 20%, a correction-proposal suggestion
  is filed in `results/suggestions.json` against t0033's answer asset.

</details>

## 2026-05-02 (1)

## ✅ Completed

<details>
<summary>✅ 0074 — <strong>Channel tuning-width sweep on Bed A with BK/SK/Kv7
vendoring</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0074_channel_tuning_width_bed_a` |
| **Status** | completed |
| **Effective date** | 2026-05-02 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0068-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-05-01T21:51:44Z |
| **End time** | 2026-05-02T03:55:00Z |
| **Step progress** | 13/15 |
| **Task page** | [Channel tuning-width sweep on Bed A with BK/SK/Kv7 vendoring](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Task folder** | [`t0074_channel_tuning_width_bed_a/`](../../../tasks/t0074_channel_tuning_width_bed_a/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0074_channel_tuning_width_bed_a/results/results_detailed.md) |

# Channel Tuning-Width Sweep on Bed A with BK / SK / Kv7 Vendoring

## Motivation

The t0067 soma-channel-addition sweep on Bed A (deposited Poleg-Polsky DSGC, library
`modeldb_189347_dsgc` from t0008) measured DSI as a point estimate from PD vs ND only — a
2-angle protocol. That left the more biologically interesting question unanswered: do the
tested channels also reshape the *width* of the angle-to-AP-rate tuning curve, and if so, do
they sharpen or broaden it? t0067 reported NaP_high inverts DSI (sign flip), Nav1.6_high
erodes DSI from 0.80 to 0.23, and {NaR, Kv3, Kv4} are nearly inert at the chosen densities;
t0068 then falsified the Nav1.6 + Kv3 co-expression rescue. Three biologically natural rescue
candidates remain untested because their MOD mechanisms are not yet vendored in the project:
BK (KCa1.1 / KCNMA1), SK (KCa2 / KCNN), and Kv7 (KCNQ2 + KCNQ3, the M-current). All three are
calcium-activated or slow-activating and could in principle differentially suppress the
high-firing-rate PD direction and rescue DSI without flipping it. Adding them to the channel
sweep and measuring tuning width across all eight channels at three densities each closes both
gaps in one task.

This task addresses RQ1 (somatic VGC combinations) and provides a tuning-width baseline that
any future RQ4 active-dendrite test will compare against. Source suggestions covered:
S-0068-01 (BK / SK with Nav1.6), S-0068-02 (Kv7 with Nav1.6), S-0068-05 (Kv3 alone
validation).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC, t0008 library `modeldb_189347_dsgc`).
* Encoding: 12-angle bar-rotation protocol (the model's native protocol per t0046
  reproduction). Bar-arrival times sweep through 12 angles in 30-degree steps.
* Channel set: 8 channels — 5 already vendored {Nav1.6, NaP, NaR, Kv3, Kv4} plus 3 newly
  vendored {BK, SK, Kv7}. Each channel inserted on the soma at low / medium / high density (3
  densities each, matching the t0067 grid). Plus a baseline condition with no extra channels.
* **Conditions**: 1 baseline + 8 channels x 3 densities = **25 conditions**.
* **Trials**: 25 conditions x 12 angles x 5 seeds in FULL mode = 1500 trials. Plus 25 x 12
  angles x 1 seed x 2 passive modes (EPSP_PASSIVE / IPSP_PASSIVE) = 600 diagnostic trials.
  **Total: 2100 trials**, ~2.2 h wall-clock on local CPU under CVODE at the t0067 measured
  rate of ~3.75 s / trial.

## Approach

### Stage 1 — vendor 3 new MOD files plus calcium-pool mechanism

* Vendor a BK (KCa1.1) MOD file, sourced from a standard published model (e.g., Migliore CA1,
  Hines & Carnevale Purkinje). Validate kinetics against expected V- and Ca-dependence.
* Vendor an SK (KCa2 / SK2) MOD file from the same kind of source.
* Vendor a Kv7 / M-current MOD file (KCNQ2 + KCNQ3 mixture or composite Kv7) from a standard
  published model.
* Vendor a calcium-pool mechanism (single-shell `cad`-style decay model, mirrors Bed B's
  existing `cad`) to provide [Ca]_i for BK and SK.
* Un-zero CaL and CaT in Bed A's `init_active` so that the calcium pool has a current source.
  This is the only change to the existing Bed A model and must pass a regression gate (see
  Stage 2).

### Stage 2 — regression gate

* Run the t0067 baseline (no extra channels, no BK / SK / Kv7) under the new code path with
  CaL + CaT un-zeroed and the calcium-pool mechanism live but at zero density (BK = 0, SK = 0,
  Kv7 = 0).
* Pass criterion: baseline DSI matches t0067's reported DSI = 0.797 within 1e-3 (allowing
  sampling noise across the 5-seed mean). Failure means the un-zeroing introduced unintended
  dynamics; fix before proceeding to Stage 3.

### Stage 3 — 12-angle tuning-curve sweep

* For each of 25 conditions (1 baseline + 5 existing channels x 3 densities + 3 new channels x
  3 densities) run 12 angles x 5 seeds in FULL mode. Save:
  * Per-trial soma spike times.
  * Per-trial peak Vm and baseline Vm.
  * Per-condition tuning curve (mean +/- SD spike count per angle).
* Same channel insertion code as t0067 with three new branches for BK, SK, Kv7. Holds all
  other parameters at the t0067 baseline.

### Stage 4 — passive diagnostics (EPSP_PASSIVE / IPSP_PASSIVE)

* For each of 25 conditions run 12 angles x 1 seed x 2 passive modes = 600 trials.
* Save per-trial peak Vm in the EPSP_PASSIVE and IPSP_PASSIVE traces. These should be flat at
  -60 mV in IPSP_PASSIVE for all conditions (cross-checks with t0065's shunting-design
  finding) and direction-invariant in EPSP_PASSIVE under Bed A's gabaMOD = 0 zeroing.

### Stage 5 — width metrics and visualisation

* Per condition, compute:
  * **HWHM** (half-width at half-max) in degrees, by linear interpolation around the half-max
    points of the 12-angle tuning curve.
  * **Vector-sum DSI** = `|sum_i rate(theta_i) * exp(i * theta_i)| / sum_i rate(theta_i)` —
    circular concentration metric.
  * **Peak rate (Hz)** at the angle with maximum mean rate.
  * **Rate at PD** and **rate at PD + 180 deg** (ND).
  * **RMSE vs t0004 cosine target** — the canonical project tuning-curve loss, computed using
    the t0012 library.
* For any condition where the tuning curve has no clear peak (mean rate < 1 Hz at every
  angle), report HWHM as `null` rather than fabricating a value.
* Produce a per-channel sensitivity plot (HWHM, vector-sum DSI, peak rate vs density) using
  the t0011 visualisation library.

## Expected Outputs

* **Library asset**: a vendored channel pack containing the BK, SK, Kv7 MODs plus the
  calcium-pool mechanism, registered as a project library. This becomes a dependency for t0075
  and any future task that needs these channels.
* **Per-condition tuning curves** (25 CSVs, one per condition) and a combined
  `tuning_curves.csv` with all 25 x 12 = 300 (condition, angle) rows.
* **Width metrics table** (`results/metrics_summary.csv`): 25 rows x 6 columns (HWHM,
  vector-sum DSI, peak rate, PD rate, ND rate, RMSE vs cosine target).
* **Per-channel sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI, peak
  rate vs density per channel.
* **Cross-channel comparison plot** (`results/images/all_channels_dsi_vs_density.png`):
  vector-sum DSI vs density for all 8 channels overlaid.
* `results/metrics.json` with the registered project metrics applied per condition.

## Pass Criteria

* Stage 2 regression gate passes (baseline DSI within 1e-3 of t0067 = 0.797).
* All 2100 trials complete with no instability flags.
* Width metrics table is fully populated (HWHM may be `null` for low-rate conditions;
  vector-sum DSI and peak rate must be defined for all 25 conditions).
* For each channel, at least one density produces a measurable change in either HWHM or
  vector-sum DSI (delta > 5 deg HWHM or delta > 0.05 vector-sum DSI relative to baseline).
  Channels that produce no measurable change at any density are reported as inert in the
  conclusion section.

## Compute Estimate

* ~2.2 h wall-clock on local CPU under CVODE for the 2100 trials.
* ~3-4 h coding time for the 3 channel MOD vendoring + calcium-pool mechanism + Stage 2
  regression gate.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library `modeldb_189347_dsgc`.
* `t0011_response_visualization_library` — tuning-curve visualisation.
* `t0012_tuning_curve_scoring_loss_library` — RMSE vs cosine target.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code is forkable; baseline DSI
  = 0.797 reference for the regression gate.

## Risks and Fallbacks

* **Calcium-pool kinetics drift**: the un-zeroing of CaL / CaT in Bed A's `init_active` is the
  most disruptive change. If the regression gate (Stage 2) fails, fall back to a closed-form
  external calcium-pool mechanism that does not depend on CaL / CaT (e.g., feed [Ca]_i
  directly from a precomputed time series). This preserves BK / SK kinetics while leaving Bed
  A's existing HHst dynamics untouched.
* **BK / SK MOD source discrepancy**: if the chosen source MOD has different kinetics from the
  canonical RGC literature, validate against published whole-cell recordings (e.g., Pfeiffer &
  Friedrich 2012 mouse RGC BK; Wang et al. 2014 RGC SK). Document the source paper for each
  MOD in the library asset's `details.json`.
* **Kv7 expression density unclear**: Kv7 in DSGC AIS is documented but somatic Kv7 in DSGC is
  less studied. If the t0067 "low / medium / high" density grid produces only inert results
  across the Kv7 row, log the negative result and recommend an AIS-localised follow-up
  (deferring to t0075).

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0074_channel_tuning_width_bed_a"
> date_completed: "2026-05-02"
> status: "complete"
> ---
> **Results Summary: Channel Tuning-Width Sweep on Bed A**
>
> **Summary**
>
> Across 25 conditions (1 baseline + 8 channels × 3 densities) × 12 angles × 5 seeds = 1500
> FULL +
> 600 passive = 2100 trials, **NaP_high collapses vector-sum DSI from 0.193 to 0.050** (legacy
> DSI_PD-ND from 0.308 to 0.008) and produces the highest peak rate in the sweep (74.2 Hz vs
> 17.4 Hz
> baseline); **SK_high cuts HWHM in half** (83.5 deg → 41.1 deg) while suppressing peak rate;
> **Kv3,
> Kv4, and Kv7 are inert at all three densities tested** (no condition trips the |delta_HWHM|
> > 5 deg
> or |delta_vec_DSI| > 0.05 thresholds). All 2100 trials completed with zero instability
> flags.
>
> **Metrics**
>
> * **Baseline (no extra channels)**: vector-sum DSI = **0.193**, legacy DSI_PD-ND =
>   **0.308**, peak

</details>

## 2026-05-01 (8)

## ⏹ Not Started

<details>
<summary>⏹ 0075 — <strong>Biologically-realistic AIS one-axis-at-a-time parameter
sweep on Bed A</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0075_bio_realistic_ais_param_sweep` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0069-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Biologically-realistic AIS one-axis-at-a-time parameter sweep on Bed A](../../../overview/tasks/task_pages/t0075_bio_realistic_ais_param_sweep.md) |
| **Task folder** | [`t0075_bio_realistic_ais_param_sweep/`](../../../tasks/t0075_bio_realistic_ais_param_sweep/) |

# Biologically-Realistic AIS Parameter Sweep on Bed A

## Motivation

t0069 attached a virtual AIS plus 1 mm axon stub to Bed A (deposited Poleg-Polsky DSGC) and
re-ran the t0067 channel-addition sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} on the AIS
instead of the soma. The sweep falsified S-0067-03's prediction (AIS-localised channels show
*larger* DSI effects than soma-localised) — it actually showed the opposite, with 11 of 15
channel conditions producing zero detectable DSI change. The cause was identified clearly: the
AIS+axon halved baseline PD firing (14.2 → 6.4 spikes) and silenced ND firing (1.6 → 0.0),
pushing baseline DSI to the trivial computational ceiling 1.0. The passive AIS+axon adds an
electrical sink that quenches the cell rather than relocating spike initiation; AIS-localised
channels at our densities cannot overcome the somatic 400 mS/cm² HHst Na drive.

The follow-up question this task answers: is there *any* DSGC + AIS configuration that
simultaneously contains all the channels biologically present in a vertebrate AIS (HHst basal
Na+K, Nav1.6, Kv3, Kv7 — the canonical RGC AIS quartet) and produces non-trivial DSI at a
biologically reasonable peak rate? "Decent DSI, not 1, and reasonable firing rate" maps to the
operational pass band {DSI in [0.3, 0.95], peak Hz in [5, 50]}. The right tool is not
optimisation — it is one axis at a time. NaP is excluded from the AIS channel set on two
grounds: (a) AIS NaP expression in RGCs is controversial; (b) the t0067 NaP-high finding (DSI
sign flip) suggests NaP destabilises the DSI mechanism rather than supporting it. BK and SK
are excluded because they localise primarily to soma and dendrites in RGCs, not to the AIS.

This task addresses RQ1 (somatic + AIS VGC combinations) and RQ4 (active vs passive
components). Source suggestions covered: S-0068-04 (move Nav1.6 + Kv3 to AIS), S-0069-01
(halve somatic gnabar before AIS), S-0069-02 (shrink AIS diameter to 0.5 micrometre),
S-0069-03 (vary axon length to probe sink), S-0069-04 (Nav1.6 + Kv3 on AIS at biological
densities).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC) plus virtual AIS + axon stub.
* AIS channel set: **{HHst basal Na + K, Nav1.6, Kv3, Kv7}**. NaP, BK, SK explicitly excluded.
* Encoding: 12-angle bar-rotation protocol (same as t0074 — cross-task comparable).
* Two-stage design: Stage 1 baseline calibration; Stage 2 per-axis sweep.

### Stage 1 — Baseline calibration

* Literature-informed AIS configuration (Wang et al. 2011, Carter et al. 2008 on mouse RGC
  AIS): AIS diameter 0.8 micrometre, AIS length 30 micrometre, axon stub 1.0 mm, AIS
  gnabar_HHst 4 0 0 mS/cm^2, AIS Nav1.6 medium density (~0.3 S/cm^2 from t0067 medium), AIS
  Kv3 medium density (~0.3 S/cm^2), AIS Kv7 low density (~0.1 S/cm^2; distal AIS, weaker than
  Nav and Kv3).
* Sweep soma `gnabar_HHst` across 6 candidates: {100, 150, 200, 250, 300, 400} mS/cm^2 (the
  t0069 baseline = 400).
* 6 candidates x 12 angles x 1 seed = 72 trials, ~5 min wall-clock.
* Pick the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]}. If multiple
  candidates qualify, pick the one closest to the centre of the band ({peak ~ 20 Hz, DSI ~
  0.6}).
* If no candidate qualifies, the task halts at Stage 1 and reports a negative result with a
  recommendation for a follow-up that loosens the AIS configuration further (e.g., reduce AIS
  Nav1.6 density first, then re-attempt).

### Stage 2 — Per-axis sweep

From the Stage-1 baseline, vary one parameter at a time with all others held at baseline:

| # | Axis | Values | Non-baseline points |
| --- | --- | --- | --- |
| 1 | Soma `gnabar_HHst` (mS / cm^2) | {100, 200, 300, 400} | 3 |
| 2 | AIS `gnabar_HHst` (mS / cm^2) | {0, 100, 200, 400, 800} | 4 |
| 3 | AIS diameter (micrometre) | {0.4, 0.6, 0.8, 1.0, 1.5} | 4 |
| 4 | AIS length (micrometre) | {15, 30, 45, 60} | 3 |
| 5 | AIS Nav1.6 density | {0, low, medium, high} | 3 |
| 6 | AIS Kv3 density | {0, low, medium, high} | 3 |
| 7 | AIS Kv7 density | {0, low, medium, high} | 3 |
| 8 | Axon length (mm) | {0.1, 0.5, 1.0, 2.0} | 3 |

Total Stage-2 conditions: 1 baseline + 26 non-baseline = **27 conditions x 12 angles x 5 seeds
= 1620 FULL trials**, ~100 min wall-clock at the t0067 measured ~3.75 s / trial under CVODE.

### Width metrics per axis (cross-comparable with t0074)

For each condition, compute:

* **HWHM** in degrees from the 12-angle tuning curve.
* **Vector-sum DSI** (circular concentration).
* **Peak rate (Hz)** at the angle with maximum mean rate.
* Rate at PD (axis-1 peak angle) and at the opposite angle.
* RMSE vs the t0004 cosine target.

### Outputs

* **Library asset**: `bed_a_with_bio_realistic_ais` — Bed A + AIS + axon model variant with
  the {HHst, Nav1.6, Kv3, Kv7} channel set wired in. Reusable by future tasks that need a
  working DSGC + AIS substrate.
* **Stage 1 candidate table** (`results/baseline_candidates.csv`) with 6 rows showing
  soma_gnabar_HHst, peak Hz, DSI, in-band y/n.
* **Stage 2 per-axis sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI,
  peak rate, RMSE vs cosine target, plotted against axis values.
* **Biologically-plausible AIS recommendation table**
  (`results/biological_ais_recommendation.md`): the band-constrained range for each axis (the
  values that keep the cell inside {DSI [0.3, 0.95], peak [5, 50] Hz}), plus a recommended
  canonical configuration.
* `results/metrics.json` with registered project metrics per condition.

## Approach

1. Fork t0069's AIS-attachment code into this task's `code/`. Replace the t0069
   channel-addition loop with the {HHst, Nav1.6, Kv3, Kv7} baseline channel set (with
   t0074-vendored Kv7).
2. Implement Stage 1 calibration as a 6-candidate sweep with explicit pass-band check and
   automated baseline selection.
3. Implement Stage 2 as 8 per-axis sweep functions sharing a common driver.
4. Run Stage 1, log selected baseline, run Stage 2.
5. Compute width metrics, generate per-axis plots, write the recommendation table.
6. Validate against t0069 sanity checks: trials with instability flags = 0, peak Vm bounded.

## Pass Criteria

* Stage 1 finds at least one in-band baseline (peak Hz in [5, 50] AND DSI in [0.3, 0.95]).
* All 1620 + 72 trials complete with no instability flags.
* Per-axis sensitivity plots show monotonic or unimodal sensitivity for at least 6 of the 8
  axes (the axes that don't are flagged as candidates for re-investigation; not a hard fail).
* Recommendation table produced with the band-constrained range for each axis.

## Compute Estimate

* ~2 h wall-clock on local CPU. 72 trials Stage 1 (~5 min) + 1620 trials Stage 2 (~100 min) +
  ~10 min plotting / metrics extraction.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code (Nav1.6, Kv3
  implementation patterns).
* `t0069_t0067_ais_localised_channel_sweep` — AIS attachment code; baseline characterisation
  of the passive-AIS sink effect.
* `t0074_channel_tuning_width_bed_a` — Kv7 MOD vendoring lands in t0074. This task inherits
  the vendored Kv7 mechanism and the calcium-pool unification (the latter is not actively used
  here but must remain compatible).

## Risks and Fallbacks

* **Stage 1 finds no in-band baseline**: the task halts after Stage 1 and reports a negative
  result with a follow-up recommendation. Time-cheap (~5 min). The follow-up would probably be
  a 2D Stage 1.5 sweep over {soma gnabar, AIS gnabar} or a baseline that further reduces AIS
  Nav1.6 density.
* **Stage 1 is over-fitted to soma_gnabar**: if the baseline soma_gnabar value is borderline
  (e.g., exactly at the edge of the in-band region), small parameter changes in Stage 2 may
  push the cell out of band rapidly. Mitigation: pick the Stage-1 baseline closest to the band
  centre, not the band edge.
* **Axes interact strongly**: the one-axis-at-a-time design assumes weak interactions. If a
  Stage-2 axis sweep produces non-monotonic behaviour (e.g., DSI rises then falls), report the
  non-monotonicity explicitly and flag the axis for a future joint sweep with one neighbouring
  axis.
* **AIS+axon discretisation artefacts**: if the segment count along the AIS or axon is too
  low, spike initiation and propagation may be artefactual. Mitigation: use NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) and validate that the
  chosen segment count doubles without changing peak Vm by more than 1 mV at the t0069
  baseline.

## Out of Scope

* Bed B (de Rosenroll) — explicitly out of scope per researcher decision; this task is Bed A
  only.
* Joint multi-axis optimisation — explicitly excluded; this is one-axis-at-a-time only.
* Other AIS channel candidates (Nav1.2, Kv1, Kv4 alpha-DTX-sensitive subtype) — out of scope;
  the channel set is fixed at {HHst, Nav1.6, Kv3, Kv7}. Future follow-ups may extend the
  channel set.

</details>

## ✅ Completed

<details>
<summary>✅ 0073 — <strong>Brainstorm results session 12</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0073_brainstorm_results_12` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md), [`t0058_brainstorm_results_11`](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md), [`t0062_nmda_escape_with_ampa_priming`](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md), [`t0064_hh_current_step_test`](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-01T17:00:00Z |
| **End time** | 2026-05-01T18:55:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 12](../../../overview/tasks/task_pages/t0073_brainstorm_results_12.md) |
| **Task folder** | [`t0073_brainstorm_results_12/`](../../../tasks/t0073_brainstorm_results_12/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0073_brainstorm_results_12/results/results_detailed.md) |

# Brainstorm Session 12: Channel Tuning-Width and Biologically-Realistic AIS Parameter Sweeps on Bed A

Twelfth brainstorming session. Run on 2026-05-01 after t0070 (two-bed writeup), t0071 (typeset
PDF + synaptic-current equations), and t0072 (synaptic conductance/current traces for PD and
ND on both beds) all completed. The session is triggered by two convergent gaps in the t0067 /
t0068 / t0069 voltage-gated-channel arc on Bed A (the deposited Poleg-Polsky 2016 ON-OFF DRD4
DSGC):

* **Tuning-width gap**: t0067 measured DSI as a point estimate from PD vs ND only. Whether the
  channels {Nav1.6, NaP, NaR, Kv3, Kv4} also reshape the *width* of the angle-to-AP-rate
  tuning curve has not been measured. The biologically more interesting question is whether
  channels broaden or sharpen tuning, not just whether they raise or lower DSI at the two
  cardinal angles.

* **Biologically-realistic AIS gap**: t0069 falsified the AIS-channel-relocation hypothesis on
  the 4 0 0 mS/cm² somatic Na background, but did so by collapsing the cell into a regime
  where ND firing = 0 and DSI = 1 trivially. We therefore have no DSGC + AIS configuration
  that simultaneously contains all the channels biologically present in a vertebrate AIS (HHst
  basal Na+K, Nav1.6, Kv3, Kv7) while keeping DSI in the [0.3, 0.95] band and the peak rate in
  the [5, 50] Hz band. Finding such a configuration via one-axis-at-a-time parameter sweeps
  (not optimisation) is a prerequisite for any future AIS-localised-channel hypothesis test.

## Decisions

* **Create t0074** — `channel_tuning_width_bed_a`. Forks t0067's somatic channel-addition
  layer on Bed A and runs a 12-angle bar-rotation tuning-curve protocol per condition. Channel
  set is the five existing channels {Nav1.6, NaP, NaR, Kv3, Kv4} plus three newly vendored
  channels {BK, SK, Kv7/M-current} at low/medium/high densities. 8 channel types times 3
  densities plus 1 baseline = 25 conditions; 25 times 12 angles times 5 seeds = 1500 FULL
  trials, plus 25 times 12 angles times 1 seed times 2 passive modes = 600 EPSP_PASSIVE /
  IPSP_PASSIVE diagnostic trials; total ~2.2 h wall-clock on local CPU under CVODE. Width
  metrics: HWHM (deg), vector-sum DSI, peak rate at PD, RMSE vs the t0004 cosine target.
  Vendoring overhead (~3-4 h coding) covers BK + SK + Kv7 MOD files, a calcium-pool mechanism
  for BK / SK, and unzeroing CaL / CaT in Bed A's `init_active` with a regression gate that
  reproduces t0067's baseline DSI = 0.797 within 1e-3 before any new channel is added.

* **Create t0075** — `bio_realistic_ais_param_sweep`. Forks t0069's AIS attachment code on Bed
  A. AIS channel set: {HHst basal Na+K, Nav1.6, Kv3, Kv7} (NaP, BK, and SK explicitly excluded
  — NaP inverts DSI per t0067 and is controversial in AIS; BK / SK are more soma / dendrite
  than AIS in RGCs). Two-stage design: Stage 1 calibrates a working baseline by running 6
  candidate soma-gnabar settings at a literature-informed AIS configuration (diameter 0.8
  micrometre, length 3 0 micrometre, axon stub 1 mm) at 12 angles times 1 seed = 72 trials;
  the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]} is selected. Stage
  2 runs 8 one-at-a-time axes from that baseline (soma `gnabar_HHst`, AIS `gnabar_HHst`, AIS
  diameter, AIS length, AIS Nav1.6 density, AIS Kv3 density, AIS Kv7 density, axon length); 27
  conditions times 12 angles times 5 seeds = 1620 FULL trials, ~100 min wall-clock. Total
  compute ~2 h. Outputs: per-axis HWHM / DSI / peak Hz sensitivity plots and a
  "biologically-plausible AIS recommendation" table. t0075 depends on t0074 (Kv7 vendoring
  lands in t0074); the two are commissioned in this brainstorm but serialised by dependency.

## Suggestion Cleanup

* **Reject nine high-priority suggestions** as covered by the new tasks or as duplicates:
  S-0068-01 (BK / SK with Nav1.6 — covered by t0074), S-0068-02 (Kv7 with Nav1.6 — covered by
  t0074), S-0068-04 (move Nav1.6 + Kv3 to AIS — covered by t0075), S-0068-05 (Kv3 alone
  validation — superseded by t0074's per-channel tuning-width sweep), S-0069-01 (halve somatic
  gnabar — covered by t0075 axis 1), S-0069-02 (shrink AIS diameter to 0.5 micrometre —
  covered by t0075 axis 3), S-0069-03 (vary axon length to probe sink — covered by t0075 axis
  8), S-0069-04 (Nav1.6 + Kv3 on AIS at biological densities — covered by t0075 baseline plus
  axes 5 + 6), S-0065-01 (apply EPSP / IPSP / FULL to from-scratch family — duplicate of
  S-0066-02; the more recent S-0066-02 is kept).

* **Reprioritise three high-priority suggestions to medium** where the t0065 / t0066 / t0067
  shunting-inhibition discovery has changed the strategic frame: S-0002-01 (factorial g_Na x
  g_K grid search) and S-0002-04 (factorial morphology sweep) — both pre-shunting-discovery
  framing, the project has moved on; S-0070-02 (unified model-bed-runner library) — pure
  infrastructure, not blocking any current experiment.

## Tasks Cancelled or Updated

None.

## Assets Produced

No assets in this brainstorm task. The two new tasks (t0074 and t0075) will produce one
library asset each (channel-vendoring library plus tuning-width sweep code in t0074;
biologically-realistic AIS variant of Bed A plus per-axis sweep code in t0075) and a results
bundle each when executed downstream.

**Results summary:**

> **Results Summary: Brainstorm Session 12**
>
> **Summary**
>
> Twelfth strategic brainstorm, run on 2026-05-01 after t0070 (two-bed writeup), t0071
> (typeset PDF +
> synaptic-current equations), and t0072 (synaptic conductance / current traces for PD and ND
> on both
> beds) all completed. The session is triggered by two convergent gaps in the t0067-t0069
> voltage-gated-channel arc on Bed A: the unmeasured tuning-width effect of channel addition
> (t0067
> measured DSI at PD and ND only), and the absence of any DSGC + AIS configuration that
> simultaneously
> contains all biologically-present AIS channels and produces non-trivial DSI at a
> biologically
> reasonable peak rate. Decision: commission two new tasks (t0074 `channel_tuning_width_bed_a`
> —
> 12-angle bar-rotation tuning curves on Bed A with 8-channel set including newly vendored BK
> / SK /
> Kv7; t0075 `bio_realistic_ais_param_sweep` — biologically-realistic AIS one-axis-at-a-time
> parameter sweep on Bed A with channel set {HHst, Nav1.6, Kv3, Kv7}); reject nine covered or
> duplicate suggestions; reprioritise three high-priority suggestions to medium where the
> t0065 /
> t0066 shunting-inhibition discovery has changed the strategic frame.
>
> **Session Overview**
>
> Date: 2026-05-01. Triggered by the convergent t0067-t0069 channel-arc findings: NaP_high
> inverts DSI

</details>

<details>
<summary>✅ 0072 — <strong>Plot synaptic conductances and currents for PD and ND
on both model beds</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0072_synaptic_traces_pd_nd` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-05-01T16:46:03Z |
| **End time** | 2026-05-01T17:50:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Plot synaptic conductances and currents for PD and ND on both model beds](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md) |
| **Task folder** | [`t0072_synaptic_traces_pd_nd/`](../../../tasks/t0072_synaptic_traces_pd_nd/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0072_synaptic_traces_pd_nd/results/results_detailed.md) |

# Plot synaptic conductances and currents for PD and ND on both model beds

## Motivation

The t0070 / t0071 writeups document every synaptic-current equation analytically (canonical
`I_syn(t,V) = g_syn(t,V) · (V − E_syn)` form per channel, with parameters and
direction-encoding mechanism). What they do NOT show is the actual time-domain shape of these
conductances and currents during a real trial — i.e., what does `g_AMPA(t)` actually look like
across the bar sweep, and how does the PD vs ND swap reshape `g_GABA(t)`? Visual traces make
the direction-encoding mechanism viscerally obvious in a way the equations alone cannot.

This task records every synaptic state variable (`gAMPA`, `gNMDA`, `g` for SACinhib/SACexc,
`g` for Exp2Syn) during one PD and one ND trial on each model bed, then plots the population
mean ± SD per synapse type. Result: a presentation-ready figure pair (one per bed) showing
exactly how each synaptic conductance (and the resulting current) evolves over time, and how
PD vs ND differ.

## Scope

* **Two model beds**:
  * **Bed A** — t0008 deposited Poleg-Polsky, with the t0020 gabaMOD-swap protocol applied
    (PD: `gabaMOD = 0.33`; ND: `gabaMOD = 0.99`). 282 ON dendrites, each carrying one BIPsyn
    (AMPA + NMDA), one SACinhibsyn (GABA), and one SACexcsyn (ACh). 4 synapse types to plot.
  * **Bed B** — t0024 de Rosenroll port. Uses moving-bar angle for direction encoding, with
    per-event Bernoulli release sigmoid (PD: bar at preferred angle; ND: bar at null angle,
    i.e. rotated 180°). Active synapses on this bed are Exp2Syn ACh and Exp2Syn GABA. 2
    synapse types to plot.
* **Two directions per bed**: PD and ND, single trial each, fixed seed for reproducibility.
* **Trial duration**: full bar-sweep duration as defined by each bed's existing driver (~1000
  ms for Bed A; whatever t0066's protocol uses for Bed B).
* **Quantities recorded per synapse**:
  * Conductance state: `g(t)` in nS (or µS for Bed B; converted to nS for plotting
    consistency).
  * Local membrane voltage at the synapse insertion point: `v_local(t)` in mV.
  * Current: `I(t) = g(t) · (v_local(t) − E_rev)` computed post-hoc, in pA.
* **Aggregation**: across all synapse instances of a given type, compute mean and SD at each
  recorded time point. Plot mean as a solid line, ±1 SD as a shaded band.

## Approach

1. For each bed, write a driver script that:
   * Builds the cell using the existing dependency-task code (no modification of t0008 / t0020
     / t0024 source files).
   * Sets the direction (PD or ND) via the canonical mechanism for that bed.
   * Iterates over every synapse instance of every type, attaches NEURON Vector recorders to
     the relevant `_ref_g` (or `_ref_gAMPA` / `_ref_gNMDA` for Bed A's BIPsyn) plus the local
     membrane voltage `_ref_v` at the synapse's section.
   * Runs `h.continuerun(tstop)`.
   * Saves raw traces to `data/` as compressed numpy arrays (one .npz per `bed × direction ×
     synapse_type`).
2. Compute population mean ± SD across synapses for each synapse type, in each direction.
3. Compute currents from g(t) and v_local(t) post-hoc, then average across synapses.
4. Generate two figures (one per bed):
   * Bed A figure: 4 rows (AMPA, NMDA, GABA, ACh), 2 columns (g(t), I(t)), PD and ND overlaid
     in each panel as solid lines with shaded ±SD bands.
   * Bed B figure: 2 rows (ACh, GABA), 2 columns (g(t), I(t)), same overlay format.
5. Optionally add a third "comparison" figure showing the dendritic spatial pattern of
   per-synapse mean conductance (e.g., heatmap over the dendritic tree) — only if it doesn't
   significantly increase task time.
6. Author a `results/results_detailed.md` writeup describing methodology and the visible PD vs
   ND structure (e.g., "Bed A: AMPA/NMDA/ACh traces are identical between PD and ND because
   excitation is direction-symmetric on this bed; only g_GABA differs, scaled by gabaMOD").
   Render to `results/results_detailed.pdf` via Typst (consistent with t0071).

## Outputs

* `tasks/t0072_synaptic_traces_pd_nd/code/{paths,constants,record_synapses,plot_traces,
  render_pdf}.py` — driver, plot generator, PDF compiler.
* `tasks/t0072_synaptic_traces_pd_nd/data/bed_a_{pd,nd}_{ampa,nmda,gaba,ach}.npz` and
  `bed_b_{pd,nd}_{ach,gaba}.npz` — raw per-synapse traces (compressed numpy).
* `tasks/t0072_synaptic_traces_pd_nd/results/images/bed_a_synaptic_traces.png` — Bed A figure
  (4 rows × 2 cols).
* `tasks/t0072_synaptic_traces_pd_nd/results/images/bed_b_synaptic_traces.png` — Bed B figure
  (2 rows × 2 cols).
* `tasks/t0072_synaptic_traces_pd_nd/results/results_summary.md` — abstract.
* `tasks/t0072_synaptic_traces_pd_nd/results/results_detailed.md` + `.typ` + `.pdf` — full
  writeup.
* `tasks/t0072_synaptic_traces_pd_nd/results/{metrics,costs,remote_machines_used}.json` +
  `suggestions.json` — standard bookkeeping.

## Compute and budget

* Local Windows workstation. Each bed simulation is ~1-3 seconds for one trial; with recorders
  on every synapse (282 × 3 types for Bed A, plus voltage on each section), expect 10-30
  seconds per trial. Total: < 5 minutes wall-clock.
* External costs: $0.
* Disk: raw .npz traces ~10-50 MB total; PDF ~1 MB.
* Time estimate: 2-3 hours (most of it is the driver code + plotting).

## Dependencies

Six tasks: t0008 (Bed A cell builder), t0020 (Bed A gabaMOD protocol), t0024 (Bed B cell
builder), t0065 / t0066 (EPSP/IPSP/FULL protocol drivers — for tstop and direction
conventions), t0070 (the writeup these traces complement), t0071 (the Typst PDF pipeline
reused here).

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Recording vectors on 282 synapses × 3 types × 4 sections each may consume >2 GB RAM. | OOM error or slow execution. | Reduce recording dt from default `h.dt` (~25 µs) to 1 ms; subsample to 1 sample per ms. |
| 2 | Bed B's Exp2Syn `g` accessor returns the post-factor conductance directly (not the raw A/B states). | g(t) shape doesn't match the canonical bi-exponential. | Document: Bed B's `g` is the post-factor conductance, ready for the I = g·(v-e) computation. No bug. |
| 3 | Bed A's BIPsyn release model is stochastic; per-synapse traces are noisy. | Individual traces look like sparse spikes. | Population mean ± SD across 282 synapses smooths this out (this is the whole point of plotting the population, not one synapse). |
| 4 | Bed B's PD/ND encoding requires correctly-set bar angle in the t0024 driver; misconfiguring it yields wrong asymmetry. | Bed B GABA traces look identical between PD and ND. | Mirror t0066's PD/ND configuration exactly; cite source line. |
| 5 | Typst PDF compilation fails on the new figures. | Compile error. | Fallback to embedding PNGs as raster only (no MathML) or use t0071's working render_pdf.py verbatim. |

## Verification criteria

* All 6 (Bed A: 4 + Bed B: 2) synapse types have raw .npz traces in `data/`.
* Both PNG figures exist and are non-trivial (>50 KB each, > 5 panels each).
* PD and ND lines are visibly different on at least the GABA channel (Bed A) and the GABA
  channel (Bed B).
* `results_detailed.md`, `.typ`, and `.pdf` all exist.
* All standard verificators pass.

## Task Requirement Checklist

* **REQ-1**: Bed A — record `gAMPA(t)`, `gNMDA(t)` from every BIPsyn instance, in PD and ND.
* **REQ-2**: Bed A — record `g(t)` from every SACinhibsyn (GABA) and SACexcsyn (ACh), PD and
  ND.
* **REQ-3**: Bed B — record `g(t)` from every Exp2Syn ACh and Exp2Syn GABA instance, PD and
  ND.
* **REQ-4**: Compute `I(t) = g(t) · (v_local(t) − E_rev)` post-hoc for every synapse.
* **REQ-5**: Aggregate to population mean ± SD per synapse type per direction.
* **REQ-6**: Bed A figure: 4 rows × 2 cols (g and I per synapse type), PD and ND overlaid.
* **REQ-7**: Bed B figure: 2 rows × 2 cols, PD and ND overlaid.
* **REQ-8**: Both figures embedded in `results_detailed.md` with descriptive captions.
* **REQ-9**: Typst-typeset PDF produced (consistent with t0071 pipeline).
* **REQ-10**: Discussion in `results_detailed.md` highlighting which traces differ between PD
  and ND for each bed, and what that reveals about the direction-encoding mechanism.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0072_synaptic_traces_pd_nd"
> date_completed: "2026-05-01"
> status: "complete"
> ---
> **Synaptic Conductance and Current Traces (PD vs ND)**
>
> **Summary**
>
> Recorded `g(t)` and `v_local(t)` from every synapse on each model bed (Bed A: 282 BIPsyn +
> SACinhibsyn + SACexcsyn = 4 synapse types; Bed B: 177 Exp2Syn ACh + GABA = 2 types) for one
> PD and
> one ND trial each at 1 ms resolution, computed `I = g · (v_local − E_rev)` post-hoc, and
> plotted
> population mean ± 1 SD per synapse type with PD and ND overlaid. Two multi-panel figures
> (Bed A:
> 4×2; Bed B: 2×2) plus a 1.0 MB Typst-typeset PDF embedding both figures and the full
> methodology.
>
> **Metrics**
>
> * **Bed A GABA peak conductance**: PD = **0.38 nS** vs ND = **0.70 nS** (1.87× ratio,
>   matches the
> `gabaMOD = 0.99 / 0.33` envelope ratio diluted by post-synaptic v feedback).

</details>

<details>
<summary>✅ 0071 — <strong>t0070 v2 - synaptic-current equations + typeset
PDF</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0071_t0070_synaptic_eqs_pdf` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`correction`](../../../meta/task_types/correction/) |
| **Start time** | 2026-05-01T14:40:52Z |
| **End time** | 2026-05-01T15:25:00Z |
| **Step progress** | 7/15 |
| **Task page** | [t0070 v2 - synaptic-current equations + typeset PDF](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md) |
| **Task folder** | [`t0071_t0070_synaptic_eqs_pdf/`](../../../tasks/t0071_t0070_synaptic_eqs_pdf/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.md) |

# t0070 v2 — synaptic-current equations + typeset PDF

## Motivation

t0070 produced a research-paper writeup of the project's two DSGC model beds (Bed A: t0008
deposited Poleg-Polsky 2016; Bed B: t0024 de Rosenroll 2026 port). The writeup is otherwise
thorough but it has two gaps:

1. **Missing canonical synaptic-current equations.** The HH membrane equation is written
   explicitly at the top of each bed's section, and every active conductance is enumerated as
   `Iᵢ = gᵢ · ... · (V − Eᵢ)`. But for synaptic currents (AMPA, NMDA, GABA, ACh in Bed A;
   Exp2Syn ACh and GABA in Bed B) the parameters and kinetics are described in prose and
   parameter tables only — the canonical `I_syn = g_syn(t,V) · (V − E_syn)` blocks are absent.
   The user explicitly noted this gap.
2. **No typeset PDF.** t0070 produced markdown only. The user wants a PDF with proper math
   typesetting (italic Greek, real subscripts/superscripts, real fractions) for use in a
   written report and a presentation.

The corrections specification (`arf/specifications/corrections_specification.md` v3) restricts
formal correction files to asset kinds (suggestion, paper, answer, dataset, library, model,
predictions). It does not cover result documents. So this task is a **semantic** correction
implemented as a new `correction`-type task: t0071's `results/results_detailed.md` is the v2
of the writeup and supersedes t0070's. Readers should use t0071's version.

## Scope

This task does NOT re-derive any equations or change any biophysical parameter values. Every
parameter cited in t0071 is the same parameter cited in t0070, with the same
`code/<file>:<line>` provenance. The only changes are:

* **Add** the missing synaptic-current equation blocks under each bed's "Synaptic excitation"
  and "Synaptic inhibition" subsections. Five blocks total:
  * Bed A `BIPsyn` AMPA (single-decay; `bipolarNMDA.mod:103, 156`)
  * Bed A `BIPsyn` NMDA (bi-exponential rise/decay × Mg block; `bipolarNMDA.mod:102-104`)
  * Bed A `SACinhibsyn` GABA (single-decay + presynaptic envelope × `gabaMOD`;
    `SAC2RGCinhib.mod`)
  * Bed A `SACexcsyn` ACh (single-decay + presynaptic envelope × `achMOD`; `SAC2RGCexc.mod`)
  * Bed B Exp2Syn ACh + Exp2Syn GABA (NEURON's standard `Exp2Syn` form, normalised
    bi-exponential) — one block per channel, with the GABA block adding the per-event
    Bernoulli direction-encoding and AR(2) noise envelope from
    `tasks/t0066_t0024_epsp_ipsp_vm_protocol/`.
* **Rewrite** every equation block (existing HH equations, Mg-block, vesicular release, and
  the new synaptic blocks) in LaTeX math syntax (`$...$` inline, `$$...$$` display) so that
  Typst (and any future pandoc/MathJax/KaTeX renderer) typesets them properly.
* **Produce** `results/results_detailed.pdf` via the Typst compiler (`pip install typst`,
  pure-Python wheel that bundles the Rust binary — no LaTeX install required).
* **Produce** `results/results_detailed.typ` (Typst source) so the PDF is reproducible.
* **Update** `results/results_summary.md` to reference the new PDF and equation additions.

The four schematic PNGs from t0070 (`bed_a_morphology.png`, `bed_b_morphology.png`,
`bed_a_synaptic_diagram.png`, `bed_b_synaptic_diagram.png`) are reused verbatim — copied into
this task's `results/images/` so the v2 document is fully self-contained.

## Approach

1. Add `typst` as a dependency in `pyproject.toml`.
2. Write `code/render_pdf.py` — small script that compiles `results/results_detailed.typ` to
   `results/results_detailed.pdf` via the `typst` Python API.
3. Author `results/results_detailed.md` (v2 markdown) by:
   * Copying t0070's `results/results_detailed.md` text verbatim as the starting point.
   * Replacing every fenced-text equation block with LaTeX math (`$$...$$`).
   * Adding the 5 new synaptic-current equation blocks under the appropriate subsections.
   * Updating the frontmatter to reference t0071 and noting the supersession of t0070.
4. Author `results/results_detailed.typ` — same content as the markdown but in Typst syntax.
   Equations in Typst use `$ ... $` (display) and `$...$` (inline) with Typst's math notation.
5. Run `code/render_pdf.py` to produce `results/results_detailed.pdf`. Verify visually (open
   the PDF, confirm equations render with proper math fonts).
6. Copy the 4 PNGs from t0070 into `results/images/`.
7. Write `results/results_summary.md` referencing the PDF.
8. Standard task closure: metrics.json (`{}`), costs.json, remote_machines_used.json,
   suggestions.json (likely 1-2 suggestions about the PDF pipeline becoming a project
   library).

## Outputs

* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.md` — v2 markdown with all
  equations (HH + 5 new synaptic blocks + existing) in LaTeX math syntax.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.typ` — Typst source.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf` — typeset PDF.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_summary.md` — abstract pointing at the
  PDF.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/{bed_a,bed_b}_morphology.png` and
  `{bed_a,bed_b}_synaptic_diagram.png` — copied verbatim from t0070.
* `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py` — Typst→PDF compile script.
* `tasks/t0071_t0070_synaptic_eqs_pdf/results/{metrics,costs,remote_machines_used}.json` +
  `suggestions.json` — standard bookkeeping.

## Compute and budget

* Local Windows workstation. ~$0 external cost. Adds one Python wheel (`typst`).
* Time: ~1.5-2 hours (most of it is the careful equation transcription).

## Dependencies

Only `t0070_writeup_two_model_beds`. The starting point is t0070's
`results/results_detailed.md`.

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Typst Python wheel not available for Windows / Python 3.13. | `pip install typst` fails. | Install Quarto (`winget install --id Posit.Quarto`) or use `pandoc + tectonic` instead. Document the chosen pipeline in the task. |
| 2 | Typst's math syntax differs subtly from LaTeX (e.g., `dot.c` vs `\cdot`, `op("...")` for multi-letter function names). | PDF compiles but equations look wrong. | Use Typst's own math reference; for any equation that won't render correctly in Typst, fall back to a rendered SVG via matplotlib mathtext and embed as image. |
| 3 | PDF includes the schematic PNGs but Typst can't find them at compile time. | Compile error or missing-image placeholder. | Use absolute paths in the Typst source; verify with a smoke test on one image before adding all four. |
| 4 | The corrections-spec restriction means there's no formal way to mark t0070's writeup as superseded. | Aggregators may still surface t0070 as the canonical writeup. | The user is informed — t0071's results_detailed.md is the new canonical version and t0070 stays as historical record. Add a clear note at the top of t0071's results document. |
| 5 | Equation transcription introduces a numerical error vs t0070. | Manual cross-check against t0070's parameter tables. | Diff t0071 against t0070 on every numerical value before commit; only structural and syntactic changes should differ. |

## Verification criteria

* `results/results_detailed.md` exists with all standard sections per the results
  specification, contains every equation block from t0070 in LaTeX math syntax, and has the 5
  new synaptic-current equation blocks.
* `results/results_detailed.typ` exists and compiles to PDF without errors.
* `results/results_detailed.pdf` exists, is non-empty, and renders the equations with proper
  math fonts (visual check).
* All standard verificators pass (verify_task_results, verify_task_metrics,
  verify_suggestions, verify_logs, verify_task_complete).

## Task Requirement Checklist

* **REQ-1 (5 synaptic-current equation blocks present)**: BIPsyn AMPA, BIPsyn NMDA,
  SACinhibsyn GABA, SACexcsyn ACh, Exp2Syn ACh+GABA on bed B.
* **REQ-2 (HH equation in LaTeX math)**: each bed's `C_m · dV/dt = -Σ I_i - I_syn - I_inj`
  block converted to `$$C_m \frac{dV}{dt} = ...$$` form.
* **REQ-3 (every equation in LaTeX math syntax)**: no fenced-text equations remain; all are
  `$...$` or `$$...$$`.
* **REQ-4 (Typst PDF rendered)**: `results_detailed.pdf` exists, non-empty, equations visibly
  typeset in math fonts.
* **REQ-5 (typst dep added)**: `typst` listed in `pyproject.toml`.
* **REQ-6 (PNGs preserved)**: 4 PNGs copied from t0070 into `results/images/`.
* **REQ-7 (results_summary.md updated)**: references the new PDF and notes the additions.
* **REQ-8 (every numeric parameter unchanged from t0070)**: structural and syntactic changes
  only; no biophysical value changed.
* **REQ-9 (note in results_detailed.md that this supersedes t0070)**: clear notice in the
  Summary or front-matter.
* **REQ-10 (PDF compile script in code/)**: `code/render_pdf.py` reproducible.

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0071_t0070_synaptic_eqs_pdf"
> date: "2026-05-01"
> ---
> **Results Summary: Two Standard DSGC Model Beds (v2 — synaptic-current equations + typeset
> PDF)**
>
> **Summary**
>
> This task delivers the **v2 writeup** of the project's two standard DSGC model beds and
> **supersedes** [t0070]'s `results/results_detailed.md`. The v1 writeup was thorough but had
> two
> gaps: (1) the canonical synaptic-current ohmic blocks (one per mechanism, of the form
> $I_\mathrm{syn} = g_\mathrm{syn}(t,V)\,(V - E_\mathrm{syn})$) for the AMPA, NMDA, GABA, and
> ACh
> point-process mechanisms in Bed A and the Exp2Syn ACh + GABA mechanisms in Bed B were never
> spelled
> out (only the parameters appeared, in prose and tables); (2) there was no typeset PDF —
> equations
> lived inside fenced `text` blocks and rendered in monospace. Both gaps are now closed. Bed A
> is the
> deposited Poleg-Polsky 2016 ON-OFF DRD4 DSGC ported in [t0008] (ModelDB 189347, library
> `modeldb_189347_dsgc`), used by [t0020], [t0065], [t0067], [t0068], and [t0069]. Bed B is
> the de
> Rosenroll 2026 DSGC ported in [t0024] (library `de_rosenroll_2026_dsgc`), used by [t0066].
> Each bed
> section opens with the canonical Hodgkin-Huxley membrane equation $C_m \,dV/dt = -\sum_i I_i
> -

</details>

<details>
<summary>✅ 0070 — <strong>Writeup of two standard DSGC model beds in HH-equation
research-paper format</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0070_writeup_two_model_beds` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Start time** | 2026-05-01T13:07:47Z |
| **End time** | 2026-05-01T14:05:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Writeup of two standard DSGC model beds in HH-equation research-paper format](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md) |
| **Task folder** | [`t0070_writeup_two_model_beds/`](../../../tasks/t0070_writeup_two_model_beds/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0070_writeup_two_model_beds/results/results_detailed.md) |

# Writeup of two standard DSGC model beds in HH-equation research-paper format

## Motivation

The project routinely runs experiments on two distinct DSGC model substrates:

* **Bed A — t0008 deposited Poleg-Polsky 2016 DSGC** (ModelDB 189347), used as the substrate
  for t0020 (gabaMOD-swap protocol), t0065 (EPSP/IPSP/FULL Vm protocol), t0067 (soma channel
  sweep), t0068 (Nav1.6 + Kv3 co-expression rescue), and t0069 (AIS-localised channel sweep).
* **Bed B — t0024 de Rosenroll 2026 DSGC port**, used as the substrate for t0066
  (EPSP/IPSP/FULL Vm protocol on de Rosenroll cell).

A single canonical writeup of both beds — with the standard Hodgkin-Huxley membrane equation
up front and every conductance defined explicitly, plus the excitation and inhibition models
for PD and ND directions — does not exist in one place in the project. Each task references
its substrate but assumes prior familiarity. The user needs this writeup as both a
self-contained report and as the basis for a presentation; the writeup must therefore stand
alone, be printable, and avoid implicit assumptions about which task did what.

## Scope

* Two model beds, treated symmetrically: same section structure, same equation conventions,
  same level of detail.
* For each bed:
  1. **Cell morphology** — section list, lengths, diameters, electrotonic structure, and
     source of the morphology (deposited file, generated, scaled, etc.).
  2. **Membrane equation** — start with the canonical HH form and then enumerate every current
     term Iᵢ that appears in the model, with V_half, time constants, and gbar values where
     applicable. Use the same notation in both beds for cross-comparison.
  3. **Synaptic excitation in PD vs ND** — bipolar drive (AMPA + NMDA where present), Mg-block
     parameters, peak conductance, timing pattern, source of asymmetry between PD and ND.
  4. **Synaptic inhibition in PD vs ND** — SAC GABA model, spatial pattern, gabaMOD or
     equivalent direction-encoding mechanism, e_GABA, peak conductance, timing pattern.
* A short side-by-side comparison table at the end, summarising the headline differences
  (e.g., number of compartments, presence of NMDA, AIS or no AIS, gabaMOD vs spatial
  inhibition).
* Output is a single research-paper-format document under
  `tasks/t0070_writeup_two_model_beds/results/results_detailed.md` plus a brief
  `results/results_summary.md` (per the standard task file structure).

## Approach

1. Read the t0008, t0020, t0024 task code (NEURON `.hoc`, MOD files, Python wrappers) and
   confirm every conductance with cited file/line references.
2. Read the t0065, t0066 protocol code to extract the exact PD vs ND encoding for each bed
   (gabaMOD-swap for bed A; whatever t0066 uses for bed B).
3. Cross-check against the original papers (Poleg-Polsky 2016 and de Rosenroll 2026) where
   available in the project's paper assets — but the canonical source for the writeup is the
   project's own ported code, not the original papers.
4. Write the document section by section, alternating per bed for parallel structure. Use
   LaTeX- style equations rendered as fenced inline blocks (GitHub markdown tolerates `$...$`
   math).
5. Include a small morphology diagram per bed (axial schematic of compartments, not 3D), saved
   as PNG under `results/images/`. Use NEURON's section topology to generate or hand-draw the
   schematic.
6. Cross-reference every quoted parameter back to a file path and (where stable) a line
   number, so the writeup is auditable.

## Expected outputs

* `results/results_detailed.md` — the full writeup, research-paper format, all mandatory
  sections from `arf/specifications/results_specification.md` plus the bed-by-bed equation
  blocks.
* `results/results_summary.md` — 2-3 paragraph summary suitable as a presentation abstract.
* `results/images/bed_a_morphology.png`, `results/images/bed_b_morphology.png` — schematic
  morphology diagrams.
* `results/images/bed_a_synaptic_diagram.png`, `results/images/bed_b_synaptic_diagram.png` —
  PD vs ND excitation / inhibition timing diagrams.
* `results/metrics.json`, `results/costs.json`, `results/remote_machines_used.json` — standard
  bookkeeping (no external costs, no remote machines, no registered metrics produced).
* `results/suggestions.json` — follow-on tasks (e.g., a unified model-bed-runner library).

## Document format

Each bed section follows this template:

```markdown
## Bed X: <name>

### Morphology

* Compartment list with L (μm), diam (μm), nseg
* Electrotonic length and connectivity diagram

### Membrane equation

The Hodgkin-Huxley membrane equation governs each compartment:

C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj

where Iᵢ enumerates the active conductances:

I_Na    = g_Na · m³ · h · (V - E_Na)        -- HHst Na
I_K     = g_K  · n⁴   · (V - E_K)            -- HHst K (delayed rectifier)
I_Km    = g_Km · w    · (V - E_K)            -- HHst K_m
I_leak  = g_leak      · (V - E_leak)
... (one line per channel, with parameters in a separate table)

### Conductance table

| Channel | gbar (S/cm²) | E_rev (mV) | V_half_act (mV) | τ_m (ms) | V_half_inact (mV) | τ_h (ms) | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... | ... | code/HHst.mod L<n> |

### Synaptic excitation (PD vs ND)

* AMPA: peak g_AMPA, τ_rise, τ_decay, E_rev = 0 mV
* NMDA: peak g_NMDA, τ_rise, τ_decay, Mg-block parameters, V_off
* Bipolar drive: timing of activations, spatial pattern across dendrites
* PD encoding: <how PD is set>
* ND encoding: <how ND is set>

### Synaptic inhibition (PD vs ND)

* SAC GABA: peak g_GABA, τ, E_rev = e_GABA
* Spatial pattern across dendrites
* PD encoding: gabaMOD = ... or asymmetric SAC drive
* ND encoding: gabaMOD = ... or asymmetric SAC drive

### Differences from the original paper

(brief notes on simplifications, missing features, known divergences)
```

## Stages

* `research-code` — read both beds' code in full, extract every conductance and synapse
  parameter with file:line citations.
* `planning` — write `plan/plan.md` with the section-by-section outline.
* `implementation` — produce the schematic PNGs and write the `results/*` documents.
* `results` + `suggestions` + `reporting` — finalise.

## Compute and budget

* Local Windows workstation. No remote machines, no external API costs.
* Time estimate: 2-3 hours total. No simulation runs (the data is read from existing code).

## Dependencies

The five dependencies above are needed because the writeup *describes* them. None of these are
"data dependencies" in the experiment sense — they are source dependencies: the writeup must
reference their committed code.

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Bed B (t0024) uses different mechanism naming than bed A; cross-bed table doesn't align cleanly. | The bed-A and bed-B conductance tables don't share a column structure. | Use two separate tables with explicit column headers, then a third "shared parameters" table. |
| 2 | NMDA / GABA peak conductance values aren't directly readable from the code (set via HOC params). | grep for `gNMDA`, `s2gampa`, `s2ggaba`, `gabaMOD` returns ambiguous results. | Trace via t0008.code.build_cell.apply_params and t0024 equivalent; cite the params dict. |
| 3 | Morphology PNGs require a NEURON GUI session that doesn't run in headless mode. | matplotlib can't fall back. | Produce a hand-drawn schematic in matplotlib (rectangles + lines) showing the topology, not the 3D morphology. |

## Verification criteria

* Both `results_summary.md` and `results_detailed.md` exist and pass `verify_task_results`.
* Every conductance / synapse parameter has a `code/<file>:<line>` citation.
* The HH membrane equation appears as the first equation in each bed's section.
* Side-by-side comparison table is present.
* All standard verificators pass.

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0070_writeup_two_model_beds"
> ---
> **Results Summary: Writeup of Two Standard DSGC Model Beds**
>
> **Summary**
>
> This task delivers a single, self-contained, presentation-ready research-paper document
> (`results/results_detailed.md`) describing the two canonical direction-selective ganglion
> cell
> (DSGC) model substrates that every other modelling task in the project uses as a backbone.
> **Bed A**
> is the deposited Poleg-Polsky 2016 ON-OFF DRD4 DSGC ported in [t0008] (ModelDB 189347,
> library
> `modeldb_189347_dsgc`), used by [t0020], [t0065], [t0067], [t0068], and [t0069]; **Bed B**
> is the de
> Rosenroll 2026 DSGC ported in [t0024], used by [t0066]. Each bed section opens with the
> canonical
> Hodgkin-Huxley membrane equation `C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj` rendered identically
> in
> fenced math blocks, then enumerates every active conductance with `gbar`, `V_half`,
> kinetics, and
> reversal potential in a markdown table, then defines the synaptic excitation and inhibition
> models
> for the preferred direction (PD) and null direction (ND). A side-by-side comparison table at
> the end
> summarises the headline differences across **18 dimensions**. Every numerical parameter
> carries a
> `code/<file>:line` citation back to the committed source so the document is fully auditable.

</details>

<details>
<summary>✅ 0069 — <strong>Add virtual AIS to deposited DSGC and re-run t0067 channel
sweep on AIS</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0069_t0067_ais_localised_channel_sweep` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0067-03` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-05-01T02:13:59Z |
| **End time** | 2026-05-01T03:10:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Add virtual AIS to deposited DSGC and re-run t0067 channel sweep on AIS](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md) |
| **Task folder** | [`t0069_t0067_ais_localised_channel_sweep/`](../../../tasks/t0069_t0067_ais_localised_channel_sweep/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0069_t0067_ais_localised_channel_sweep/results/results_detailed.md) |

# Add virtual AIS to deposited DSGC and re-run t0067 channel sweep on AIS

## Motivation

t0067 inserted 5 voltage-gated channels (Nav1.6, NaP, NaR, Kv3, Kv4) on the deposited
Poleg-Polsky DSGC soma. Three of the five (NaR, Kv3, Kv4) had essentially no effect on firing
rate or DSI at any density. The strongest plausible explanation: these channels are normally
AIS-localised in real RGCs (per t0019 priors), and putting them on the soma puts them in a
compartment where the existing massive HHst Na (~400 mS/cm²) drowns out their contribution
plus the soma's electrotonic geometry doesn't favour AP-shape modulation. t0019 documents
distal-AIS Nav densities of 2500-5000 pS/μm² (~25-50 mS/cm²) — the AIS is a much smaller
compartment with much higher input resistance per area.

This task tests S-0067-03: append a virtual AIS + axon cable to the deposited cell, then
re-run the t0067 channel-density sweep with the 5 channels inserted on the **AIS** instead of
the soma. Hypothesis: the AIS-localised channels show substantially larger effects on firing
rate and DSI than the soma-localised versions, because the AIS is a high-input-resistance
spike-initiation zone.

## Scope

* Cell: deposited Poleg-Polsky 2016 DSGC (t0008) PLUS a new virtual AIS section (30 μm × 1 μm,
  5 segments) PLUS a passive axon cable (1000 μm × 1 μm, 50 segments). AIS connects to
  soma(1); axon connects to AIS(1).
* AIS active conductances: HHst at biologically-realistic AIS density — `gnabar = 30 mS/cm²`,
  `gkbar = 20 mS/cm²`, `gkmbar = 3 mS/cm²` (per t0019 priors).
* Axon active conductances: HHst at low density — `gnabar = 5 mS/cm²`, `gkbar = 3 mS/cm²` —
  sufficient for AP propagation, low enough to not affect somatic firing significantly.
* Mode: only `FULL` (HH on, all synapses at canonical defaults).
* Direction: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`).
* Seeds per condition: 5.
* Channels on AIS (one per experiment, 3 densities each): same as t0067.

## Conditions

16 conditions × 2 directions × 5 seeds = **160 FULL trials**.

| condition_id | channel | density (mS/cm²) | Notes |
| --- | --- | --- | --- |
| baseline_ais | (none) | — | AIS+axon attached, no extra channels — t0069 reference |
| nav16_low_ais | Nav1.6 | 10 | t0067-equivalent on AIS |
| nav16_med_ais | Nav1.6 | 30 |  |
| nav16_high_ais | Nav1.6 | 90 |  |
| nap_low_ais | NaP | 0.3 |  |
| nap_med_ais | NaP | 0.8 |  |
| nap_high_ais | NaP | 2.4 |  |
| nar_low_ais | NaR | 3 |  |
| nar_med_ais | NaR | 8 |  |
| nar_high_ais | NaR | 24 |  |
| kv3_low_ais | Kv3 | 7 |  |
| kv3_med_ais | Kv3 | 20 |  |
| kv3_high_ais | Kv3 | 60 |  |
| kv4_low_ais | Kv4 | 4 |  |
| kv4_med_ais | Kv4 | 12 |  |
| kv4_high_ais | Kv4 | 36 |  |

Densities match t0067's exactly so we can directly compare effect sizes between soma and AIS
insertion.

## Approach

1. Build the cell via t0008's `build_dsgc()` unchanged.
2. After build, add 2 new sections from Python:
   * `ais` section, 30 μm × 1 μm, 5 segments, HHst inserted with realistic AIS densities.
   * `axon` section, 1000 μm × 1 μm, 50 segments, HHst inserted at lower density.
3. Connect: `ais.connect(soma, 1, 0)`, then `axon.connect(ais, 1, 0)`.
4. Insert the 5 t0067 mechanisms on the AIS at gbar=0; per-trial set the active channel's gbar
   to the target density.
5. Run 160 trials using the t0067 driver template adapted for AIS-localised insertion.
6. Compute DSI per condition; compare to t0067 anchors (soma-localised counterparts).

## Outputs

* `data/per_trial_metrics.json` — 160 trial records.
* `data/dsi_by_condition.json` — 16 conditions.
* `results/metrics.json` — registered DSI for the t0069 baseline.
* `results/images/firing_rate_vs_density.png` — 5 panels (per channel), PD/ND firing rate with
  t0069-baseline reference.
* `results/images/dsi_vs_density.png` — 5 panels (per channel), DSI vs density with
  t0069-baseline reference.
* `results/images/soma_vs_ais_comparison.png` — for each channel, side-by-side bar chart of
  DSI change at low/med/high (soma from t0067 vs AIS from t0069).
* `results/results_summary.md`, `results/results_detailed.md` (spec_version 2).

## Failure-mode policy

Same as t0067/t0068: peak Vm > +60 mV or < -80 mV → flag `is_unstable = true`. Trial data
still saved.

## Key Questions

1. Does the t0069 baseline (AIS+axon attached, no extra channels) reproduce the t0067 baseline
   firing rate and DSI? If yes: AIS topology change is benign. If no: the AIS itself reshapes
   the cell's behaviour and we need to account for that before comparing channel effects.
2. For each of the 5 channels: is the |Δ DSI| at AIS substantially larger than at soma?
   Rule-of-thumb: ≥2× larger.
3. Do the 3 channels that were inert in t0067 (NaR, Kv3, Kv4) become active when relocated to
   the AIS?
4. Does Nav1.6 still erode DSI on the AIS, or does the smaller compartment change the
   directionality of the effect?
5. Does NaP still invert DSI on the AIS, or does the more isolated compartment change the
   sign?

## Compute and Budget

* Local Windows workstation. ~3 s/trial × 160 = ~10 min (same as t0067).
* External costs: $0.

## Time Estimation

* Implementation (cell-extension code, AIS construction, port channel-set logic): 1 hour.
* Sweep: 10 min.
* Plotting + reporting: 1 hour (3 plots + cross-task comparison).
* Verification + PR: 30 min.
* Total: ~3 hours.

## Dependencies

* `t0008_port_modeldb_189347` — cell builder.
* `t0019_literature_survey_voltage_gated_channels` — AIS Nav/Kv density priors.
* `t0065_t0020_epsp_ipsp_vm_protocol` — gabaMOD-swap protocol.
* `t0067_t0065_soma_channel_addition_sweep` — MOD files (vendored verbatim), trial driver
  template, soma-anchor DSIs for cross-comparison.

## Risks and Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Adding HHst-bearing AIS changes the cell's spike-initiation site, making the t0069 baseline very different from t0067 baseline. | t0069 baseline DSI < 0.5 or > 1.0; or PD spike count < 5 or > 30. | This IS expected — biologically correct cells initiate at AIS. Document the new baseline; comparisons are done relative to t0069 baseline, not t0067 baseline, for fair within-task contrast. The cross-task soma-vs-AIS comparison is then "channel effect on top of each task's own baseline." |
| 2 | Axon HHst at low density doesn't propagate APs, causing reflection at AIS-axon junction. | Axon Vm shows damped APs (<+10 mV peak). | Increase axon `gnabar` to 10 mS/cm². |
| 3 | t0067 MOD files are still incompatible after mechanism re-insertion on AIS. | nrnivmodl error or runtime AttributeError. | Reuse t0068's recipe (which worked); only the section target changes. |

## Verification Criteria

* All 160 trials complete without instability.
* `data/per_trial_metrics.json` has 160 entries.
* `data/dsi_by_condition.json` has 16 entries.
* All 3 PNG plots exist and embedded in `results_detailed.md`.
* All standard verificators pass.

**Results summary:**

> **Results Summary: Add virtual AIS to deposited DSGC and re-run t0067 channel sweep on AIS**
>
> **Summary**
>
> Appended a 30 μm AIS + 1 mm passive axon to the deposited Poleg-Polsky DSGC, then re-ran the
> t0067
> channel sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} inserted on the AIS instead of the
> soma at
> the same low/med/high densities. 16 conditions × 2 directions × 5 seeds = 160 FULL trials,
> ~8 min
> wall-clock. **Hypothesis S-0067-03 (AIS-localised channels show substantially LARGER DSI
> effects
> than soma-localised) is falsified.** Adding the AIS+axon halved baseline PD firing (14.2 →
> 6.4
> spikes) and silenced ND firing entirely (1.6 → 0.0), pushing baseline DSI from **0.80 →
> 1.00**.
> On this quieter AIS-anchored baseline, **11 of 15 channel conditions produced zero
> detectable DSI
> change**; only NaP (med, high) and Nav1.6 (high) moved DSI at all, and **|ΔDSI| was strictly
> smaller on the AIS than on the soma for every channel that had any effect**. The AIS+axon
> adds a
> large electrical sink that quenches the cell rather than relocating spike initiation.
>
> **Metrics**
>
> | Condition | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI | Δ DSI vs t0069 baseline |
> | --- | --- | --- | --- | --- |
> | baseline_ais | 6.4 ± 0.5 | 0.0 ± 0.0 | 1.000 | (reference) |

</details>

<details>
<summary>✅ 0068 — <strong>Nav1.6 + Kv3 co-expression: does Kv3 rescue the DSI loss
caused by Nav1.6?</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0068_t0067_nav16_kv3_coexpression_rescue` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0067-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-05-01T01:41:29Z |
| **End time** | 2026-05-01T03:05:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Nav1.6 + Kv3 co-expression: does Kv3 rescue the DSI loss caused by Nav1.6?](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md) |
| **Task folder** | [`t0068_t0067_nav16_kv3_coexpression_rescue/`](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/results_detailed.md) |

# Nav1.6 + Kv3 co-expression: does Kv3 rescue the DSI loss caused by Nav1.6?

## Motivation

t0067 found that adding Nav1.6 to the deposited Poleg-Polsky soma monotonically erodes
direction selectivity (DSI = 0.80 → 0.75 → 0.48 → 0.23 across baseline → low → med → high
density). Nav1.6 alone raises both PD and ND firing, but ND climbs faster proportionally
because the baseline ND firing was sub-threshold. The hypothesis (suggestion S-0067-02): if we
ALSO add Kv3 at the same time, Kv3's fast repolarisation could allow the cell to recover from
each AP faster and let the inhibitory shunt regain modulatory power — restoring the DSI gap.

This task tests that hypothesis directly by sweeping Kv3 density at two fixed Nav1.6 densities
(med = 30 mS/cm², high = 90 mS/cm²) and measuring whether Kv3 co-expression progressively
rescues DSI back toward baseline.

## Scope

* Cell: deposited Poleg-Polsky 2016 ModelDB 189347 DSGC, exactly as in t0008 / t0065 / t0067.
* Mode: only `FULL` (HH on, all synapses at canonical defaults). Same gabaMOD-swap protocol as
  t0067.
* Direction: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`).
* Seeds per condition: 5.
* Channels: Nav1.6 + Kv3 from t0067's vendored MODs (kinetics from Carter-Bean 2009 and Erisir
  1999 respectively).

## Conditions

9 conditions × 2 directions × 5 seeds = **90 FULL trials**.

| condition_id | Nav1.6 (mS/cm²) | Kv3 (mS/cm²) | Notes |
| --- | --- | --- | --- |
| baseline | 0 | 0 | Reference (matches t0067 baseline DSI = 0.80) |
| nav16_med | 30 | 0 | t0067 anchor (DSI = 0.48) |
| nav16_med_kv3_low | 30 | 7 | Co-insertion: low Kv3 |
| nav16_med_kv3_med | 30 | 20 | Co-insertion: med Kv3 |
| nav16_med_kv3_high | 30 | 60 | Co-insertion: high Kv3 |
| nav16_high | 90 | 0 | t0067 anchor (DSI = 0.23) |
| nav16_high_kv3_low | 90 | 7 | Co-insertion: low Kv3 |
| nav16_high_kv3_med | 90 | 20 | Co-insertion: med Kv3 |
| nav16_high_kv3_high | 90 | 60 | Co-insertion: high Kv3 |

## Approach

1. Vendor the same 5 MOD files from t0067 (`nav16t67`, `napt67`, `nart67`, `kv3t67`, `kv4t67`)
   into the task's `code/mods/`. The t0067 MOD files are reused verbatim — same kinetics, same
   NONSPECIFIC_CURRENT pattern.
2. Compile a task-local DLL.
3. Build the t0008 cell once. Insert all 5 mechanisms on the soma at gbar=0; per-trial set the
   active Nav1.6 and Kv3 gbars to the target densities (others stay at 0).
4. Run 90 FULL-mode trials using the t0067 trial-driver structure adapted to support
   simultaneous setting of Nav1.6 and Kv3 densities.
5. Aggregate per-trial scalars to per-condition mean ± SD; compute DSI per condition.

## Outputs

* `data/per_trial_metrics.json` — 90 trial records.
* `data/dsi_by_condition.json` — 9 conditions.
* `results/metrics.json` — registered `direction_selectivity_index` for the baseline.
* `results/images/dsi_rescue_curve.png` — DSI vs Kv3 density at fixed Nav1.6 (2 lines for
  Nav1.6_med vs Nav1.6_high, with baseline reference).
* `results/images/firing_rate_rescue.png` — PD and ND firing rate vs Kv3 density at fixed
  Nav1.6 (2 sub-panels).
* `results/results_summary.md`, `results/results_detailed.md` (spec_version 2) with
  rescue-effect interpretation.

## Failure-mode policy

Same as t0067: peak Vm > +60 mV or < −80 mV → flag `is_unstable = true`. Trial data still
saved.

## Key Questions

1. Does Kv3 co-insertion progressively rescue DSI as Kv3 density increases? Specifically: is
   DSI(nav16_high + kv3_high) > DSI(nav16_high) by a meaningful margin (Δ > 0.1)?
2. Does Kv3 reduce firing rate (the expected effect of fast K+ repolarisation) preferentially
   in ND (which would scale DSI back up) or in both directions equally (which would not)?
3. Is the rescue effect different for Nav1.6_med vs Nav1.6_high? At med, the cell is in a
   regime where DSI was 0.48 (still quite directional); at high, DSI was 0.23 (close to
   collapse). Which regime benefits more from Kv3?

## Compute and Budget

* Local Windows workstation. ~3 s/trial × 90 trials ≈ 5 min.
* External costs: $0.

## Time Estimation

* Implementation (port t0067 code, adapt for co-expression): 1 hour.
* Sweep: 5 min.
* Plotting + reporting: 45 min.
* Verification + PR: 30 min.
* Total: ~2.5 hours.

## Dependencies

* `t0008_port_modeldb_189347` — cell builder + base nrnmech.dll.
* `t0065_t0020_epsp_ipsp_vm_protocol` — gabaMOD-swap baseline.
* `t0067_t0065_soma_channel_addition_sweep` — vendored MOD files (Nav1.6 + Kv3 reused
  verbatim), trial driver template, baseline DSI = 0.80, Nav1.6 anchor DSIs (med = 0.48, high
  = 0.23).

## Risks and Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Kv3 at high density breaks the cell at Nav1.6_high (e.g., AP suppressed entirely). | spike_count = 0 in BOTH directions. | Document as "rescue-overshoot": Kv3 reverses Nav1.6's effect too aggressively. |
| 2 | Kv3 has no rescue effect at either Nav1.6 level (DSI unchanged from t0067 anchors). | DSI(Nav1.6_X + Kv3_Y) ≈ DSI(Nav1.6_X) for all Y. | Report null result; the rescue hypothesis is falsified. Kv3 alone may have been inert in t0067 because the cell wasn't in a fast-spiking regime; it may also be inert when added to Nav1.6 because the kinetic regime still doesn't engage Kv3 strongly. |
| 3 | Kv3 actually amplifies DSI loss (DSI drops further than Nav1.6 alone). | DSI(co-insertion) < DSI(Nav1.6 alone). | Surprising but possible. Document and explore in suggestions. |

## Verification Criteria

* All 90 trials complete.
* `data/per_trial_metrics.json` has 90 entries.
* `data/dsi_by_condition.json` has 9 entries.
* Both PNG plots exist and are embedded in `results_detailed.md`.
* All standard verificators pass.

**Results summary:**

> **Results Summary: Nav1.6 + Kv3 co-expression rescue test**
>
> **Summary**
>
> Tested whether co-inserting Kv3 with Nav1.6 on the deposited Poleg-Polsky DSGC soma rescues
> the
> direction selectivity that Nav1.6 alone erodes (t0067 anchors: DSI = 0.48 at Nav1.6_med,
> 0.23 at
> Nav1.6_high). 9 conditions × 2 directions × 5 seeds = 90 FULL trials, ~~10 min compute.
> **Hypothesis FALSIFIED**: Kv3 does NOT rescue DSI. Across all 8 co-expression conditions DSI
> changes
> by less than ±0.025 from the Nav1.6-only anchor. Instead, Kv3 slightly *boosts* firing rate
> (~~+10%
> at high Kv3), scaling PD and ND equally.
>
> **Metrics**
>
> | Condition | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI | ΔDSI vs Nav1.6 anchor |
> | --- | --- | --- | --- | --- |
> | baseline | 14.2 ± 1.9 | 1.6 ± 1.3 | 0.797 | (vs no Nav1.6) |
> | nav16_med (anchor) | 26.8 ± 3.6 | 9.4 ± 2.6 | 0.481 | (reference) |
> | nav16_med + kv3_low | 27.2 ± 3.3 | 9.4 ± 2.6 | 0.486 | +0.005 (noise) |
> | nav16_med + kv3_med | 28.6 ± 3.6 | 9.4 ± 2.6 | 0.505 | +0.024 (tiny) |
> | nav16_med + kv3_high | 30.2 ± 4.3 | 10.4 ± 2.6 | 0.488 | +0.007 (noise) |

</details>

<details>
<summary>✅ 0067 — <strong>Add 5 voltage-gated channels to t0065 soma; sweep
densities; measure firing rate and DSI change</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0067_t0065_soma_channel_addition_sweep` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-30T23:07:09Z |
| **End time** | 2026-05-01T01:05:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Add 5 voltage-gated channels to t0065 soma; sweep densities; measure firing rate and DSI change](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Task folder** | [`t0067_t0065_soma_channel_addition_sweep/`](../../../tasks/t0067_t0065_soma_channel_addition_sweep/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0067_t0065_soma_channel_addition_sweep/results/results_detailed.md) |

# Add 5 voltage-gated channels to the t0065 soma; sweep densities; measure firing rate and DSI

## Motivation

The deposited Poleg-Polsky 2016 DSGC (used by t0008/t0020/t0065) carries only the Fohlmeister-
Miller `HHst` mechanism for somatic active conductances — one Nav and one Kv compartment-wide.
t0019's voltage-gated-channel literature survey documents that real RGCs co-express multiple
Nav subtypes (Nav1.2, Nav1.6) and multiple Kv families (Kv1, Kv3, Kv4, KCNQ) with distinct
kinetics and localisations. t0043 was scoped to add Nav1.6 + Kv3 to the t0022 channel testbed
but was cancelled. No prior task has measured the per-channel impact on DSGC firing rate and
direction selectivity index (DSI) on the deposited cell.

This task systematically tests, **one channel at a time**, how adding extra Nav and Kv
mechanisms to the soma changes (a) FULL-mode firing rate and (b) DSI, relative to the t0065
baseline (DSI = 0.875, PD = 15 spikes, ND = 1 spike).

## Scope

* Cell: deposited Poleg-Polsky 2016 ModelDB 189347 DSGC, exactly as built in
  `tasks/t0008_port_modeldb_189347/code/build_cell.py::build_dsgc()`. No changes to dendrites,
  synapses, or the existing `HHst` mechanism on the soma.
* Mode: only `FULL` (HH on, all synapses at canonical defaults). Passive modes (EPSP_PASSIVE,
  IPSP_PASSIVE) are deliberately omitted because they are insensitive to active-channel
  changes by construction (HH off → new mechanisms also produce zero current at rest, traces
  would match t0065 exactly).
* Direction: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`), per t0020 / t0065 protocol.
* Seeds per condition: 5 (gives a mean ± SD on spike count and DSI; matches the user-confirmed
  cost-vs-precision tradeoff).
* Channels added (one per experiment): Nav1.6, NaP, NaR, Kv3, Kv4.
* Densities per channel: low / medium / high (factor of ~3 between levels). Medium is the
  literature-default density.

## Channel inventory

| Channel | Reference / MOD source | Low | Medium | High | Units |
| --- | --- | --- | --- | --- | --- |
| Nav1.6 (fast, low-threshold transient) | Carter & Bean 2009 / Khaliq 2003 ModelDB | 10 | 30 | 90 | mS/cm² |
| NaP (persistent sodium) | Magistretti & Alonso 1999 | 0.3 | 0.8 | 2.4 | mS/cm² |
| NaR (resurgent sodium) | Khaliq, Gouwens, Raman 2003 (Purkinje) | 3 | 8 | 24 | mS/cm² |
| Kv3 (fast delayed rectifier) | Erisir, Lau, Rudy, Leonard 1999 | 7 | 20 | 60 | mS/cm² |
| Kv4 / IA (transient A-type) | Hoffman, Magee, Colbert, Johnston 1997 | 4 | 12 | 36 | mS/cm² |

**16 conditions in total**: 1 baseline (HHst-only, no channel added) + 5 channels × 3
densities. Each runs in PD and ND with 5 seeds = **160 FULL trials**.

## Approach

1. Vendor 5 MOD files (Nav1.6, NaP, NaR, Kv3, Kv4) into the task's `code/sources/` from the
   published model sources (preferred order: ModelDB first, then re-implementation from
   published kinetics if the ModelDB MOD is incompatible with the deposited cell's MOD set).
2. Compile a task-local `nrnmech.dll` that includes the deposited Poleg-Polsky mechanisms PLUS
   the 5 new channels.
3. Reuse the t0008 cell builder unchanged. After building, programmatically `insert(<mech>)`
   the single new channel on the soma section and set its peak conductance density.
4. Reuse the t0065 trial driver structure (gabaMOD-swap, FULL mode only) but loop over
   `(channel_kind, density_level, direction, seed)`.
5. For each trial, capture peak Vm, baseline Vm, spike count. No per-sample Vm trace stored to
   CSV (each trial would produce 10001 rows × 160 trials = 1.6M rows, exceeds the 5 MB
   pre-merge gate). Save only per-trial scalars to `data/per_trial_metrics.json`.

## Configurations

| condition_id | channel | density_label | density_mS_cm2 |
| --- | --- | --- | --- |
| baseline | (none) | n/a | 0 |
| nav16_low | Nav1.6 | low | 10 |
| nav16_med | Nav1.6 | med | 30 |
| nav16_high | Nav1.6 | high | 90 |
| nap_low | NaP | low | 0.3 |
| nap_med | NaP | med | 0.8 |
| nap_high | NaP | high | 2.4 |
| nar_low | NaR | low | 3 |
| nar_med | NaR | med | 8 |
| nar_high | NaR | high | 24 |
| kv3_low | Kv3 | low | 7 |
| kv3_med | Kv3 | med | 20 |
| kv3_high | Kv3 | high | 60 |
| kv4_low | Kv4 | low | 4 |
| kv4_med | Kv4 | med | 12 |
| kv4_high | Kv4 | high | 36 |

## Outputs

* `data/per_trial_metrics.json` — list of 160 trial records with `condition_id`, `channel`,
  `density_label`, `direction`, `seed`, `peak_v_mv`, `baseline_v_mv`, `spike_count`,
  `n_samples`.
* `data/dsi_by_condition.json` — for each of the 16 conditions: PD spike-count mean ± SD, ND
  spike-count mean ± SD, DSI ((PD − ND) / (PD + ND)), PD firing rate (Hz), ND firing rate
  (Hz).
* `results/metrics.json` — registered project metric `direction_selectivity_index` for the
  baseline condition only (since the metric is per-task, not per-variant in the legacy schema
  — or use the variants format to register one DSI per condition).
* `results/images/firing_rate_vs_density.png` — 5 panels (one per channel), each showing PD
  and ND mean firing rate ± SD across the 3 density levels, with the baseline as a horizontal
  reference line.
* `results/images/dsi_vs_density.png` — 5 panels (one per channel), each showing DSI vs
  density level, baseline as horizontal reference.
* `results/images/spike_count_heatmap.png` — channel × density grid heatmap of mean spike
  count in PD and ND, side by side.
* `results/results_summary.md`, `results/results_detailed.md` (spec_version 2) with
  per-channel narrative findings, instability flagging, and the cross-channel comparison.

## Failure-mode policy

A trial is flagged "unstable" if **either**:

* peak Vm > +60 mV (depolarisation runaway), or
* peak Vm < −80 mV (hyperpolarisation past leak reversal), or
* spike count = 0 in BOTH PD and ND (no spike generation despite full synaptic drive).

Flagged trials are still saved (their data is part of the per_trial_metrics dump), but they
are called out in `results_detailed.md` as "channel + density failed sanity gate". No
automatic re-run.

## Key Questions

1. Which channel produces the largest absolute change in FULL-mode firing rate from the t0065
   baseline (15 spikes PD, 1 spike ND)?
2. Which channel produces the largest absolute change in DSI?
3. Are there channel + density combinations that **break** the cell (depolarisation block,
   silence)? Does the failure scale predictably with density?
4. Do Na channels and K channels have opposite signs of effect on firing rate (Na ↑, K ↓), or
   are there exceptions (e.g., Kv3 enabling sustained trains → firing ↑)?
5. Does any channel preferentially affect PD over ND (or vice versa), changing DSI in a non-
   trivial way (i.e., not just scaling both directions equally)?

## Compute and Budget

* Local Windows workstation. Per-trial wall-clock for the deposited Poleg-Polsky cell is ~3 s.
  160 trials × 3 s ≈ **8 minutes**.
* External costs: **$0**.

## Time Estimation

* Implementation (paths, constants, vendor MODs, recompile DLL, run driver): 2 hours (most
  time on sourcing and validating MOD files).
* Sweep run: 8 minutes.
* Plotting + reporting: 1 hour.
* Verification + PR: 30 minutes.
* Total: ~3.5 hours.

## Dependencies

* `t0008_port_modeldb_189347` — provides the cell builder and the existing MOD mechanisms
  (HHst, bipNMDA, SACinhib, SACexc).
* `t0019_literature_survey_voltage_gated_channels` — provides the kinetic priors and
  references for the 5 added channels via answer asset
  `nav-kv-combinations-for-dsgc-modelling`.
* `t0065_t0020_epsp_ipsp_vm_protocol` — provides the gabaMOD-swap FULL trial driver template,
  baseline DSI = 0.875, baseline PD spike count = 15, baseline ND spike count = 1.

## Risks and Fallbacks

* **Risk 1**: ModelDB MOD files for some channels (especially NaR, Kv3) use NEURON conventions
  incompatible with the deposited Poleg-Polsky MOD set (e.g., SUFFIX collisions, USEION
  conflicts). Detection: `nrnivmodl` fails or `nrn_load_dll` errors. Fallback: re-implement
  the mechanism from published kinetics in a clean MOD file using only NONSPECIFIC_CURRENT (no
  Ca USEION), matching the HHst pattern.
* **Risk 2**: A channel at the high density makes the cell unstable (depolarisation block, no
  spikes). Detection: failure-mode policy above. Fallback: documented in results, no re-run.
* **Risk 3**: The deposited cell has no AIS — somatic insertion of channels typically AIS-
  localised in real RGCs is a simplification. Detection: results may diverge from in-vivo
  intuition. Fallback: document the limitation; this task's purpose is to scan parameter
  space, not to claim biological fidelity.

## Verification Criteria

* All 160 trials complete without raising `_assert_bip_positions_baseline`.
* `data/per_trial_metrics.json` has 160 entries.
* `data/dsi_by_condition.json` has 16 entries.
* All 3 PNG plots exist and are embedded in `results_detailed.md`.
* `verify_logs`, `verify_research_code`, `verify_plan`, `verify_task_results`,
  `verify_task_metrics`, `verify_suggestions`, `verify_pr_premerge` all pass.

**Results summary:**

> **Results Summary: Add 5 voltage-gated channels to the t0065 soma; sweep densities**
>
> **Summary**
>
> Added each of {Nav1.6, NaP, NaR, Kv3, Kv4} to the deposited Poleg-Polsky DSGC soma, one at a
> time,
> at low / medium / high densities (3-fold steps), and ran the t0065 FULL-mode gabaMOD-swap
> protocol
> with 5 seeds per (condition, direction). 16 conditions × 2 directions × 5 seeds = 160
> trials, ~10
> minutes wall-clock. Headline finding: **NaP at high density inverts direction selectivity**
> (DSI =
> -0.18, cell fires more in null than preferred); **Nav1.6 monotonically erodes DSI** as
> density rises
> (0.80 → 0.23 across the density grid); **NaR / Kv3 / Kv4 produce only modest changes** at
> the
> chosen densities.
>
> **Metrics**
>
> | Condition | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI | Δ DSI vs baseline |
> | --- | --- | --- | --- | --- |
> | baseline | 14.2 ± 1.9 | 1.6 ± 1.3 | 0.797 | (reference) |
> | nav16_low | 18.2 ± 2.9 | 2.6 ± 1.5 | 0.750 | -0.05 |
> | nav16_med | 26.8 ± 3.6 | 9.4 ± 2.6 | 0.481 | **-0.32** |
> | nav16_high | 57.4 ± 2.9 | 36.0 ± 3.1 | 0.229 | **-0.57** |

</details>

## 2026-04-30 (3)

## ✅ Completed

<details>
<summary>✅ 0066 — <strong>Test t0024 de Rosenroll DSGC under EPSP_PASSIVE /
IPSP_PASSIVE / FULL protocol</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0066_t0024_epsp_ipsp_vm_protocol` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-04-30T15:47:25Z |
| **End time** | 2026-04-30T16:48:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Test t0024 de Rosenroll DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md) |
| **Task folder** | [`t0066_t0024_epsp_ipsp_vm_protocol/`](../../../tasks/t0066_t0024_epsp_ipsp_vm_protocol/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/results_detailed.md) |

# Test t0024 de Rosenroll DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

## Motivation

Task t0065 applied the EPSP_PASSIVE / IPSP_PASSIVE / FULL trial-mode decomposition to the
deposited Poleg-Polsky & Diamond 2016 DSGC and produced a clean diagnostic finding: direction
selectivity in that cell is purely shunting-driven, because the model's design choice of
`e_SACinhib = v_rest = -60 mV` makes inhibitory current vanish at rest. The IPSP_PASSIVE
traces were flat at -60 mV in both PD and ND despite a 3× difference in inhibitory
conductance.

The de Rosenroll et al. 2026 DSGC (ported in t0024) is structurally independent from the
Poleg-Polsky lineage: a 341-section morphology with `HHst_noiseless` channels, `Exp2Syn` ACh
(E = 0 mV) and `Exp2Syn` GABA (E = -60 mV) synapses on 177 terminal dendrites,
AR(2)-correlated Poisson release, and a per-synapse GABA release-probability sigmoid that
swings from 0.05 (PD) to 0.80 (ND) — a much steeper directional asymmetry than Poleg-Polsky's
3× scalar swap.

Because the de Rosenroll resting potential is set by `HHst_noiseless` parameters (not pinned
to e_GABA), the IPSP_PASSIVE trace should be a **real hyperpolarising response** rather than a
flat trace. This gives us a direct test of whether the t0065 shunting-only finding is generic
to DSGC modelling or specific to Poleg-Polsky's design choice.

## Scope

Apply the same EPSP_PASSIVE / IPSP_PASSIVE / FULL decomposition to the de Rosenroll cell,
recording somatic Vm in PD (0°) and ND (180°). The protocol mapping is:

* **EPSP_PASSIVE** — Set GABA `Exp2Syn` weight to 0 on every terminal dendrite; zero HH
  conductances on soma + AIS (turn off `HHst_noiseless` Na and K). Records the pure excitatory
  PSP from ACh + AR(2) noise drive.
* **IPSP_PASSIVE** — Set ACh `Exp2Syn` weight to 0 on every terminal dendrite; zero HH
  conductances. Records the pure inhibitory PSP, with the per-synapse GABA release-probability
  sigmoid still encoding direction (PD: ~5% release prob, ND: ~80%).
* **FULL** — All synapses + HH active at canonical t0024 defaults. Standard PD/ND condition
  matching the t0024 12-angle tuning curve at 0° and 180°.

Unlike t0065 (which is deterministic given seed and used 1 trial per cell), the de Rosenroll
model is stochastic — release rates are AR(2) noise → Poisson → NetCon.event injection. A
single seed gives a noisy single realisation. We use **20 trials per (mode, direction) cell**
to match t0024's existing tuning-curve practice and obtain a noise-averaged trace plus
per-trial scalar distributions.

This gives 6 cells × 20 trials = 120 trials total.

## Approach

1. Reuse `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell.build_dsgc_cell()` to
   construct the cell exactly as in t0024.
2. Reuse `tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve.py`'s per-trial driver
   as a starting template, including the AR(2) noise generator and the per-synapse Poisson
   injection (`FInitializeHandler` + `NetCon.event`).
3. Channel-isolation overrides happen at the synapse-weight / HH-conductance level, set after
   cell construction and before each trial:
   * EPSP_PASSIVE: iterate the GABA NetCon list and set each `weight[0] = 0`; iterate soma +
     AIS sections and zero `gnabar_HHst_noiseless` and `gkbar_HHst_noiseless`.
   * IPSP_PASSIVE: iterate the ACh NetCon list and set each `weight[0] = 0`; zero HH as above.
   * FULL: no overrides — accept canonical t0024 weights.
4. Per-trial sequence: build cell → apply overrides → set seed → generate AR(2) noise +
   Poisson spike times → schedule `NetCon.event` injections → attach Vm + t recorders + spike
   NetCon → `h.finitialize` → `h.continuerun(TSTOP_MS)`.
5. Save raw traces to `data/voltage_traces.csv` (long-format: `mode, direction, trial, t_ms,
   v_mv`) and per-trial scalars to `data/per_trial_metrics.json` (mode, direction, trial,
   peak_v_mv, baseline_v_mv, peak_minus_baseline_mv, spike_count, n_samples).
6. Plot per-mode 2-panel figures (PD vs ND, mean trace + IQR shading) and 3-mode summary
   panels (mean ± IQR per mode, PD and ND on separate axes).

## Configurations

Six cells (3 modes × 2 directions), 20 trials per cell, all using AR(2) `rho = 0.6`
(correlated condition matching t0024's primary protocol):

| Mode | Direction | ACh weight | GABA weight | HH | Bar direction (deg) |
| --- | --- | --- | --- | --- | --- |
| EPSP_PASSIVE | PD | canonical | 0 (all syn) | OFF (gnabar = gkbar = 0) | 0 |
| EPSP_PASSIVE | ND | canonical | 0 (all syn) | OFF | 180 |
| IPSP_PASSIVE | PD | 0 (all syn) | canonical | OFF | 0 |
| IPSP_PASSIVE | ND | 0 (all syn) | canonical | OFF | 180 |
| FULL | PD | canonical | canonical | ON | 0 |
| FULL | ND | canonical | canonical | ON | 180 |

`canonical` means the t0024 default weights and conductances. The 20 trials per cell use seeds
`base + trial_index` per `code/ar2_noise.py`'s seed protocol.

## Outputs

* `data/voltage_traces.csv` — long-format per-sample table (~120 trials × ~tstop/dt samples).
* `data/per_trial_metrics.json` — per-trial scalar summaries.
* `results/metrics.json` — registered metric: `direction_selectivity_index` from FULL mode
  trial averages.
* `results/images/vm_full_pd_vs_nd.png` — FULL mean Vm trace, PD vs ND with IQR shading.
* `results/images/epsp_pd_vs_nd.png` — EPSP_PASSIVE mean trace, PD vs ND with IQR shading.
* `results/images/ipsp_pd_vs_nd.png` — IPSP_PASSIVE mean trace, PD vs ND with IQR shading
  (expected to show clear hyperpolarising deflection in this model, unlike t0065).
* `results/images/three_mode_pd_overlay.png` — PD direction across all three modes.
* `results/images/three_mode_nd_overlay.png` — ND direction across all three modes.
* `results/images/comparison_t0065_vs_t0066_ipsp.png` — side-by-side IPSP_PASSIVE comparison
  between deposited (t0065, flat at -60 mV) and de Rosenroll (t0066, expected
  hyperpolarising).
* `results/results_summary.md`, `results/results_detailed.md` with per-mode peak/trough
  amplitudes, the cross-model IPSP comparison, and DSI from FULL mode.

## Key Questions

1. What is the peak EPSP amplitude (passive, GABA off, HH off) in PD versus ND in the de
   Rosenroll cell? Does the AR(2) noise produce direction-coupled trace differences even with
   GABA off?
2. What is the peak/trough IPSP deflection in PD versus ND, and is this a real hyperpolarising
   response (expected, given e_GABA = -60 mV with v_rest typically lower than -60 mV)?
3. How does the de Rosenroll IPSP_PASSIVE trace shape compare to the t0065 deposited cell's
   flat IPSP_PASSIVE trace? Does the cross-model contrast confirm that t0065's flat result was
   a model-specific design artefact?
4. What is the FULL-mode DSI (spike count or firing rate) in PD vs ND? Does it match t0024's
   tuning-curve mean (DSI 12-angle correlated = 0.7759 at 0° vs 180°)?

## Compute and Budget

* Local Windows workstation. Per-trial wall-clock for de Rosenroll is ~64 s based on t0024's
  4h15m for 240 trials. 120 trials × 64 s ≈ **2h10m** wall-clock for the sweep, plus ~5
  minutes for plotting.
* External costs: **$0** total. No paid API calls, no remote GPU rental.

## Time Estimation

* Implementation (code + paths + constants + per-mode override functions): 1.5 hours.
* Sweep run: 2.5 hours wall-clock.
* Plotting + analysis + reporting: 1 hour.
* Verification + PR: 30 minutes.
* Total: ~5.5 hours including buffer.

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` — provides `build_dsgc_cell`, the AR(2) noise generator,
  per-synapse Exp2Syn / NetCon construction, and the per-trial driver template.
* `t0065_t0020_epsp_ipsp_vm_protocol` — provides the protocol design, the `TrialMode` enum
  pattern, and the t0065 IPSP_PASSIVE result (flat at -60 mV) which is the reference
  comparison point. Also supplies the `## Examples` and `## Task Requirement Coverage`
  formatting pattern refined in t0065's results.

## Risks and Fallbacks

* **Risk 1**: Setting GABA `weight[0] = 0` does not silence the synapse if t0024 also injects
  the release event via a separate mechanism (Poisson FInitializeHandler may pre-bind
  weights). Detection: IPSP_PASSIVE PD with GABA-weight=0 still shows hyperpolarising
  deflection. Fallback: instead set `gaba_netcon.event(0, weight=-1)` invalid, or skip the
  GABA spike-time injection entirely in the EPSP_PASSIVE branch by zeroing the per-synapse
  release-probability sigmoid output.
* **Risk 2**: Zeroing `gnabar_HHst_noiseless` may not fully suppress AP firing if the
  mechanism has a passive depolarisation path. Detection: EPSP_PASSIVE traces show
  spike-shaped events above -20 mV. Fallback: also zero `gkbar_HHst_noiseless` and `gcal_*`
  and verify Vm cannot exceed -10 mV in any passive trial.
* **Risk 3**: 20 trials per cell may take longer than the 64 s/trial t0024 baseline if HH-off
  trials are slower (CVODE step density may grow with subthreshold dynamics). Detection:
  per-trial wall-clock > 90 s after first 5 trials. Fallback: drop to 10 trials per cell (60
  trials total, ~1h compute) and document the reduced statistics.

## Verification Criteria

* All 120 trials complete, each producing a non-empty Vm trace.
* Per-trial sanity: EPSP_PASSIVE peak Vm > IPSP_PASSIVE trough Vm (excitation depolarises,
  inhibition hyperpolarises).
* Mean IPSP_PASSIVE trough in ND < mean trough in PD (more inhibition → deeper
  hyperpolarisation).
* FULL-mode mean spike count in PD > ND (consistent with t0024's tuning-curve DSI = 0.78).
* Cross-model comparison plot renders both t0065 and t0066 IPSP_PASSIVE traces with consistent
  axes for direct visual comparison.
* `verify_logs`, `verify_step_tracker`, `verify_research_code`, `verify_task_results`,
  `verify_task_metrics`, and `verify_pr_premerge` all pass.

**Results summary:**

> **Results Summary: Test t0024 de Rosenroll DSGC under EPSP/IPSP/FULL protocol**
>
> **Summary**
>
> The de Rosenroll 2026 DSGC was driven through the EPSP_PASSIVE / IPSP_PASSIVE / FULL
> trial-mode
> protocol — 120 trials (3 modes × 2 directions × 20 seeds) — decomposing the somatic Vm into
> pure-excitatory and pure-inhibitory components. Headline finding: **the model's IPSP_PASSIVE
> trace
> is flat at -60 mV in both PD and ND**, exactly as in t0065's deposited Poleg-Polsky cell.
> Two
> structurally independent DSGC implementations therefore converge on the same design pattern
> (`e_GABA = v_rest = -60 mV` → pure shunting inhibition); the t0065 finding is **not** a
> Poleg-Polsky idiosyncrasy.
>
> **Metrics**
>
> * **direction_selectivity_index (FULL trial-mean spike-count)**: **0.7391** — matches
>   t0024's
> reference DSI = 0.776 (12-angle correlated) within sampling noise.
> * **FULL PD spike count (mean ± SD across 20 trials)**: **5.00 ± 0.65 spikes/trial**, peak
>   Vm
> **+37.29 ± 0.45 mV**.
> * **FULL ND spike count**: **0.75 ± 0.55 spikes/trial**, peak Vm +10.02 ± 41.00 mV (high
>   variance
> because most ND trials have no spike — peak Vm reflects subthreshold envelope).

</details>

<details>
<summary>✅ 0065 — <strong>Test t0020 deposited DSGC under EPSP_PASSIVE /
IPSP_PASSIVE / FULL protocol</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0065_t0020_epsp_ipsp_vm_protocol` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-04-30T07:58:16Z |
| **End time** | 2026-04-30T15:16:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md) |
| **Task folder** | [`t0065_t0020_epsp_ipsp_vm_protocol/`](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/results_detailed.md) |

# Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

## Motivation

The from-scratch DSGC family (t0052-t0059) is trapped in a binary regime —
single-spike-per-trial giving a trivial DSI of 1.0, or full suppression giving DSI of 0.
Diagnostic tasks t0060-t0064 characterised that trap from several angles (AMPA-only escape,
NMDA-only escape, AMPA priming, HH voltage-step and current-step tests) but the central
question remains open: how does a model that *does* show graded direction selectivity
decompose into excitatory and inhibitory drives?

Task t0020 is one of the few prior runs that produced both a non-trivial firing rate (~14.85
Hz peak) and a meaningful DSI (0.7838) — using the deposited Poleg-Polsky & Diamond 2016
ModelDB 189347 cell under the native `gabaMOD` parameter-swap protocol (PD = 0.33, ND = 0.99).
That same deposited model has not yet been measured with the new EPSP_PASSIVE / IPSP_PASSIVE /
FULL trial-mode protocol that the from-scratch family standardised in t0059.

The goal of this task is to apply that protocol to the deposited model:

* **EPSP_PASSIVE** — Hodgkin-Huxley (HH) channels off, GABA off, AMPA + NMDA active. Records
  the pure excitatory PSP at the soma.
* **IPSP_PASSIVE** — HH off, AMPA + NMDA off, GABA active. Records the pure inhibitory PSP.
* **FULL** — HH on, all synapses at canonical defaults. Records full somatic Vm (the t0020
  reference condition).

Together these three traces decompose the FULL Vm into its excitatory and inhibitory
components under exactly the same stimulus, in a model that is known to produce graded
direction selectivity. This gives us a reference Vm/EPSP/IPSP triplet to compare against the
from-scratch family's binary-regime traces — telling us whether the binary regime is (a)
excitatory under-drive, (b) inhibitory over-shunt, or (c) HH miscalibration.

## Scope

* Cell: deposited Poleg-Polsky 2016 ModelDB 189347 DSGC, exactly as built in
  `tasks/t0008_port_modeldb_189347/code/build_cell.py::build_dsgc()`.
* Stimulus: deposited drifting-bar stimulus, default parameters from `t0008.apply_params`.
* Directions: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`) — matching t0020.
* Trial modes: `EPSP_PASSIVE`, `IPSP_PASSIVE`, `FULL` (the same enum used in t0059's
  `code/trial.py`, redefined locally because we are running on the deposited cell, not the
  from-scratch one).
* Per-trial Vm trace: full somatic voltage trace recorded at every NEURON timestep; saved to a
  per-mode CSV.
* Trials per (mode, direction) cell: 1 (single seed = 1). This is a diagnostic decomposition,
  not a tuning-curve sweep — one trace per condition is sufficient to read off EPSP/IPSP
  shape.

This gives 6 trials total: 3 modes × 2 directions × 1 trial.

## Approach

1. Reuse `t0008.apply_params` and `t0008.build_dsgc` to construct the deposited cell.
2. Reuse `t0020.run_gabamod_sweep::run_one_trial_gabamod`'s structure as a starting template.
3. Channel-isolation overrides follow the t0049 pattern:
   * Call `apply_params(h, seed=1)` and `h("update()")` and `h("placeBIP()")` first (so that
     the default conductances are written to all point processes),
   * Override the relevant globals from Python (`h.SpikesOn`, `h.gabaMOD`, `h.b2gampa`,
     `h.b2gnmda`),
   * Re-call `h("update()")` and `h("placeBIP()")` so the synaptic point processes pick up the
     overridden globals,
   * Attach Vm + t recorders, `finitialize`, `continuerun`.
4. Save raw traces to `data/voltage_traces.csv` (long-format: `mode, direction, t_ms, v_mv`)
   so a downstream plot script can re-read without re-simulating.
5. Plot per-mode 2-panel figures (PD vs ND) and a 3-mode summary panel; embed in
   `results_detailed.md`.

The `EPSP_PASSIVE` setting `gabaMOD = 0` collapses PD and ND to the same condition (no
inhibition to swap). We still run both directions for completeness — they should overlay
exactly. If they do not, the deposited model has direction-dependent state we have not yet
identified.

## Configurations

Six trials, all `seed = 1`:

| Mode | Direction | SpikesOn | gabaMOD | b2gampa | b2gnmda |
| --- | --- | --- | --- | --- | --- |
| EPSP_PASSIVE | PD | 0 | 0.0 | default | default |
| EPSP_PASSIVE | ND | 0 | 0.0 | default | default |
| IPSP_PASSIVE | PD | 0 | 0.33 | 0.0 | 0.0 |
| IPSP_PASSIVE | ND | 0 | 0.99 | 0.0 | 0.0 |
| FULL | PD | 1 | 0.33 | default | default |
| FULL | ND | 1 | 0.99 | default | default |

`default` means whatever value `apply_params(h, seed=1)` writes (canonical paper values).
`SpikesOn = 0` activates the deposited model's built-in HH disable path (the same one t0046
and t0049 already use for sub-threshold measurements).

## Outputs

* `data/voltage_traces.csv` — long-format per-sample table.
* `results/metrics.json` — per-trial scalar summaries: peak Vm, baseline-subtracted peak
  amplitude, spike count (FULL only), trial duration.
* `results/images/vm_full_pd_vs_nd.png` — FULL-mode Vm trace, PD overlaid with ND.
* `results/images/epsp_pd_vs_nd.png` — EPSP_PASSIVE trace, PD overlaid with ND (expected to
  superimpose).
* `results/images/ipsp_pd_vs_nd.png` — IPSP_PASSIVE trace, PD overlaid with ND.
* `results/images/three_mode_pd_overlay.png` — PD direction across all three modes on one
  axis.
* `results/images/three_mode_nd_overlay.png` — ND direction across all three modes on one
  axis.
* `results/results_summary.md`, `results/results_detailed.md` with per-mode peak amplitudes
  and a qualitative description of the decomposition.

## Key Questions

1. What is the peak EPSP amplitude (passive, GABA-off) in PD versus ND? Are they identical?
2. What is the peak IPSP deflection in PD versus ND, and does the PD-vs-ND difference
   quantitatively match the gabaMOD scalar ratio (0.33 vs 0.99)?
3. When EPSP and IPSP are summed by hand, does the result resemble the FULL Vm under HH-off
   conditions? Or is the cell's nonlinear summation contributing meaningfully?
4. How do the deposited model's EPSP and IPSP shapes compare to the from-scratch family's
   EPSP/IPSP traces from t0059? This contextualises whether the binary regime is a
   synaptic-balance issue or an HH-calibration issue.

## Compute and Budget

* Local Windows workstation. Six trials × ~1.5 minutes each ≈ 10 minutes wall-clock.
* No paid API or remote GPU costs.

## Time Estimation

* Implementation: 1 hour.
* Run + plotting: 30 minutes.
* Reporting: 30 minutes.

## Dependencies

* `t0020_port_modeldb_189347_gabamod` — provides `run_one_trial_gabamod` template, the
  `apply_params` import, the `_assert_bip_positions_baseline` guard, and the validated PD/ND
  scalar values.

We do not formally depend on t0059 because that task uses the from-scratch cell substrate. We
do copy its `TrialMode` enum spelling for consistency, but the implementation is independent.

## Risks and Fallbacks

* If the deposited model's `b2gampa = 0` + `b2gnmda = 0` does not actually silence excitatory
  drive (the deposited code is a HOC tangle), we will detect this by the
  EPSP_PASSIVE-vs-IPSP_PASSIVE trace shapes being non-orthogonal. Fallback: also zero `nmdaOn
  = 0` and verify excitatory drive vanishes.
* If `SpikesOn = 0` does not fully suppress HH (it should, per t0046 / t0049 usage), the
  FULL-vs- passive traces will be ambiguous. Fallback: explicitly zero the soma `gnabar_hh`
  and `gkbar_hh` via Python after `apply_params` and verify Vm cannot exceed -20 mV in passive
  trials.

## Verification Criteria

* All six trials complete without raising `_assert_bip_positions_baseline`.
* EPSP_PASSIVE PD and ND traces are bit-identical (gabaMOD = 0 in both).
* IPSP_PASSIVE peak amplitude in ND > peak amplitude in PD (more inhibition → larger
  hyperpolarisation in ND).
* FULL-mode PD trace shows higher firing rate than ND, consistent with t0020's headline
  result.
* Plots embedded in `results_detailed.md` render correctly on GitHub.

**Results summary:**

> **Results Summary: Test t0020 deposited DSGC under EPSP/IPSP/FULL protocol**
>
> **Summary**
>
> The deposited Poleg-Polsky & Diamond 2016 DSGC was driven through the EPSP_PASSIVE /
> IPSP_PASSIVE /
> FULL trial-mode protocol — six trials (3 modes × 2 directions × 1 seed) — decomposing the
> somatic Vm into pure-excitatory and pure-inhibitory components. Headline finding: **the
> model's
> direction selectivity is produced almost entirely by shunting inhibition, not
> hyperpolarising
> inhibition**. The IPSP_PASSIVE traces stay flat at the inhibitory reversal potential
> e_SACinhib =
> -60 mV in both PD and ND, while the EPSP_PASSIVE traces are bit-identical between directions
> (gabaMOD = 0). The FULL trace shows a 15× spike count difference (15 PD vs 1 ND) driven
> entirely by
> the PD-vs-ND difference in the inhibitory *conductance* (gabaMOD 0.33 vs 0.99) shunting away
> the
> otherwise direction-invariant excitatory drive.
>
> **Metrics**
>
> * **FULL PD spike count**: **15** (firing rate ≈ **15.0 Hz** over 1000 ms)
> * **FULL ND spike count**: **1** (firing rate ≈ **1.0 Hz** over 1000 ms)
> * **DSI (single-seed point estimate, spike-count-based)**: **0.875** ((15 − 1) / (15 + 1))
> * **EPSP_PASSIVE peak Vm**: **-29.8 mV** (PD = ND, bit-identical, +28.6 mV above baseline)

</details>

<details>
<summary>✅ 0064 — <strong>HH current-step diagnostic on t0059 substrate (no
synapses)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0064_hh_current_step_test` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0063_hh_voltage_step_test`](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-29T23:54:52Z |
| **End time** | 2026-04-30T00:06:00Z |
| **Step progress** | 7/15 |
| **Task page** | [HH current-step diagnostic on t0059 substrate (no synapses)](../../../overview/tasks/task_pages/t0064_hh_current_step_test.md) |
| **Task folder** | [`t0064_hh_current_step_test/`](../../../tasks/t0064_hh_current_step_test/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0064_hh_current_step_test/results/results_detailed.md) |

# HH Current-Step Diagnostic on t0059 Substrate (No Synapses)

## Source

User-commissioned diagnostic, follow-up to t0063 (voltage clamp). Switches to current clamp so
APs can fire. Tests the HH model's spiking output as a function of injected current.

## Protocol

* No synaptic input. IClamp on `soma(0.5)`.
* IClamp protocol:
  * `delay = 50 ms` (initial rest period).
  * `dur = 200 ms` (current step).
  * `amp = target_na` (one of 6 values).
* Total trial: 300 ms.
* Currents: **{0.1, 0.2, 0.3, 0.5, 1.0, 2.0} nA**.
* Modes: **FULL** (HH on, soma + AIS) and **EPSP_PASSIVE** (HH save-and-zero on soma + AIS).
* 6 currents × 2 modes × 1 trial = **12 trials**. Wall-clock ~30-60 s.

## Outputs

* `results/voltage_traces.csv` — Vm and current trace per (target, mode).
* `results/summary.csv` — peak Vm, spike count per (target, mode).
* `results/images/voltage_response_grid.png` — 6 panels (one per current), Vm in both modes.
* `results/images/voltage_response_overlay.png` — all 12 traces overlaid.

## Architecture

Same as t0063 (cell from t0059, soma + AIS HH, passive dendrites) but with IClamp instead of
SEClamp. HH save-and-zero protocol same as before.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.

**Results summary:**

> **Results Summary: t0064 HH Current-Step Diagnostic**
>
> **Summary**
>
> IClamp 200 ms current steps at {0.1, 0.2, 0.3, 0.5, 1.0, 2.0} nA on soma, no synapses. 12
> trials in
> 79 s. The HH model produces a clean F-I curve with rheobase between 0.1 and 0.2 nA, peak
> firing rate
> of 18 spikes / 200 ms (= 90 Hz) at 1.0 nA, and characteristic **depolarization block at 2.0
> nA**
> (only 1 initial spike, then sustained Vm plateau ~-30 mV).
>
> **Metrics**
>
> | I (nA) | FULL peak Vm | FULL spikes | EPSP_PASSIVE peak Vm | F-I rate (Hz) |
> | --- | --- | --- | --- | --- |
> | 0.1 | -60.53 mV | 0 | -61.65 mV | 0 |
> | 0.2 | +14.48 mV | **7** | -58.53 mV | 35 |
> | 0.3 | +17.27 mV | **10** | -55.41 mV | 50 |
> | 0.5 | +19.74 mV | **13** | -49.17 mV | 65 |
> | 1.0 | +23.13 mV | **18** | -33.56 mV | 90 |
> | 2.0 | +28.00 mV | **1 (depol-block)** | -2.34 mV | 5 |
>

</details>

## 2026-04-29 (6)

## ✅ Completed

<details>
<summary>✅ 0063 — <strong>HH voltage-step diagnostic on t0059 substrate (no
synapses)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0063_hh_voltage_step_test` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-29T23:31:00Z |
| **End time** | 2026-04-29T23:46:00Z |
| **Step progress** | 7/15 |
| **Task page** | [HH voltage-step diagnostic on t0059 substrate (no synapses)](../../../overview/tasks/task_pages/t0063_hh_voltage_step_test.md) |
| **Task folder** | [`t0063_hh_voltage_step_test/`](../../../tasks/t0063_hh_voltage_step_test/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0063_hh_voltage_step_test/results/results_detailed.md) |

# HH Voltage-Step Diagnostic on t0059 Substrate (No Synapses)

## Source

User-commissioned diagnostic to test the HH model on the t0059 substrate. No synaptic input —
just SEClamp voltage steps. Goal: characterise the HH active currents at each holding voltage.

## Protocol

* **No synapses constructed** — pure cell + SEClamp on soma.
* **SEClamp** on `soma(0.5)`:
  * `dur1 = 50 ms`, `amp1 = -65 mV` (hold at rest).
  * `dur2 = 200 ms`, `amp2 = target` (step to target voltage).
  * `dur3 = 50 ms`, `amp3 = -65 mV` (hold back at rest).
  * `rs = 0.001` MOhm (low series resistance for tight clamp).
* `TSTOP = 300 ms`.
* Targets: **-60, -50, -40, -30, -20, -10 mV** (6 levels).
* Modes: **FULL** (HH on, soma + AIS) and **EPSP_PASSIVE** (HH save-and-zero on soma + AIS).
* Record: soma Vm, SEClamp current `i`.
* Total: **6 targets x 2 modes x 1 trial = 12 trials**. Wall-clock estimate: ~30-60 s.

## Outputs

* `results/voltage_step_traces.csv` — long-format: gampa is unused, columns are `target_mv,
  mode, sample_idx, t_ms, v_soma_mv, i_clamp_na`.
* `results/summary_voltage_step.csv` — per-(target, mode) peak / steady-state Vm and clamp
  current.
* `results/images/voltage_step_grid.png` — 6 panels (one per target), each showing Vm in both
  modes.
* `results/images/clamp_current_grid.png` — 6 panels (one per target), each showing the
  SEClamp current in both modes — the difference between FULL and EPSP_PASSIVE is the pure HH
  contribution.

## Architecture

Reuses t0059's cell building (build_dsgc_from_swc) and neuron bootstrap. No synapses; only the
SEClamp is wired. HH save-and-zero protocol same as t0060/t0061/t0062.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.

**Results summary:**

> **Results Summary: t0063 HH Voltage-Step Diagnostic**
>
> **Summary**
>
> Stepped the soma from -65 mV to {-60, -50, -40, -30, -20, -10} mV via SEClamp for 200 ms
> each, 12
> trials (6 targets x 2 modes) in 24.60 s. SEClamp held Vm tight to target across all
> conditions. The
> FULL-vs-PASSIVE clamp current difference reveals classic HH dynamics: transient inward Na+
> current
> at step onset (-13 to -15 nA) at all depolarised levels; sustained outward residual at -30
> to -10 mV
> (persistent K+ delayed-rectifier minus residual Na+) growing from ~+1 to +5 nA.
>
> **Metrics**
>
> * **Tight clamp**: Vm tracks target voltage within 1 mV at all 6 targets in both modes
>   (clamp rs =
> 0.001 MOhm).
> * **Capacitive transients**: clamp current spikes to the limit at step edges (-5000 nA at
>   -60,
> -55000 nA at -10) due to dV/dt charging the soma capacitance — these are not HH currents.
> * **HH transient (Na+ activation)**: at step onset, FULL clamp current dips ~15 nA below
>   PASSIVE for
> ~5 ms, indicating brief inward Na+ activation before h-inactivation.
> * **HH steady-state at -60 mV**: I_HH = 0 nA (Na+/K+ channels closed).
> * **HH steady-state at -50 mV**: I_HH near 0 (Na+ activates briefly but inactivates; K+
>   slow).

</details>

<details>
<summary>✅ 0062 — <strong>NMDAR-escape test with AMPA priming on t0059 substrate
at PD with GABA=0</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0062_nmda_escape_with_ampa_priming` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md), [`t0061_nmda_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-29T22:46:47Z |
| **End time** | 2026-04-29T23:04:00Z |
| **Step progress** | 7/15 |
| **Task page** | [NMDAR-escape test with AMPA priming on t0059 substrate at PD with GABA=0](../../../overview/tasks/task_pages/t0062_nmda_escape_with_ampa_priming.md) |
| **Task folder** | [`t0062_nmda_escape_with_ampa_priming/`](../../../tasks/t0062_nmda_escape_with_ampa_priming/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0062_nmda_escape_with_ampa_priming/results/results_detailed.md) |

# NMDAR-Escape Test with AMPA Priming on t0059 Substrate at PD with GABA = 0

## Source

User-commissioned diagnostic, parallel to t0061 but with AMPA priming. Goal: characterise how
co-located AMPA + NMDA (no GABA) responds to PD bar input across the same gNMDA range as
t0061.

## Mechanism Choice

* **AMPA**: standard `Exp2Syn` (rise 0.5 ms, decay 2.5 ms, e = 0 mV), fixed at **gAMPA = 0.5
  nS**.
* **NMDA**: t0055's `NMDA_MgBlock` (Jahr-Stevens voltage-dependent), swept gNMDA in {0.1, 0.5,
  1, 2, 5, 10, 15, 20} nS.
* Both AMPA and NMDA at the same dendritic locations, driven by a shared NetStim. AMPA primes
  the cell with a fast (~10 ms) depolarization, partially unblocking Mg from the NMDA channel.

## Sweep

| Axis | Values |
| --- | --- |
| `GABA_BASE_NS` | **0** |
| `gAMPA_PRIMING_NS` | **0.5** (fixed) |
| Direction | theta = 0 deg only |
| Trials per condition | 1 |
| `gNMDA` (nS) | {0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} |
| Mode | `FULL` and `EPSP_PASSIVE` |

Total: 8 gNMDA × 2 modes × 1 trial × 1 direction = **16 trials**.

## Outputs

Same shape as t0061: `voltage_traces_pd_only.csv`, `summary_pd_only.csv`, `wallclock.json`,
`placement_seed0.json`, `voltage_response_grid.png` (8 panels), `voltage_response_overlay.png`
(all 16 traces).

## Architecture

Reuses t0059's library for cell + placement and t0055's NMDA_MgBlock.mod (copied verbatim).
Each E location gets both an AMPA `Exp2Syn` and an `NMDA_MgBlock` POINT_PROCESS, both wired to
the same NetStim that fires once at bar-arrival time.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.

**Results summary:**

> **Results Summary: t0062 NMDA + AMPA-Priming PD Diagnostic**
>
> **Summary**
>
> Ran 16 trials (8 gNMDA values × 2 modes × 1 trial × 1 direction) at theta = 0 deg with GABA
> = 0
> and AMPA fixed at 0.5 nS as priming on every E synapse, NMDA Mg-block sweep gNMDA in {0.1,
> 0.5, 1,
> 2, 5, 10, 15, 20} nS. Wall-clock 269.80 s. Headline: **AMPA priming abolishes the silent
> regime seen
> in t0061** — the cell fires 2-4 spikes at every gNMDA value. Peak spike count **4 at gNMDA =
> 2.0
> nS** (AMPA-NMDA synergy point), plateau of 2-3 spikes at gNMDA in [0.1, 1.0]
> (AMPA-only-like) and
> [5, 20] (AMPA + NMDA plateau).
>
> **Metrics**
>
> * **gNMDA = 0.1 / 0.5 / 1.0 nS**: FULL = +15.84 / +15.78 / +15.71 mV, **2 spikes** each;
> EPSP_PASSIVE peak = -52.56 / -51.85 / -49.54 mV. AMPA dominates the response.
> * **gNMDA = 2.0 nS (synergy peak)**: FULL = +15.58 mV, **4 spikes**; EPSP_PASSIVE = -33.43
>   mV. AMPA
> primes, NMDA Mg-block opens, sustained depolarization supports multi-spike train.
> * **gNMDA = 5.0 nS**: FULL = +15.28 mV / 2 spikes; EPSP_PASSIVE = -8.54 mV / 1 (false).
> * **gNMDA = 10.0 nS**: FULL = +14.92 mV / 3 spikes; EPSP_PASSIVE = -4.65 mV / 1 (false).
> * **gNMDA = 15.0 nS**: FULL = +14.71 mV / 3 spikes; EPSP_PASSIVE = -3.36 mV / 1 (false).

</details>

<details>
<summary>✅ 0061 — <strong>Quick NMDAR-escape test on t0059 substrate at preferred
direction with GABA=0</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0061_nmda_escape_pd_only_no_gaba` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md), [`t0060_ampa_escape_pd_only_no_gaba`](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-29T22:15:49Z |
| **End time** | 2026-04-29T22:32:00Z |
| **Step progress** | 7/15 |
| **Task page** | [Quick NMDAR-escape test on t0059 substrate at preferred direction with GABA=0](../../../overview/tasks/task_pages/t0061_nmda_escape_pd_only_no_gaba.md) |
| **Task folder** | [`t0061_nmda_escape_pd_only_no_gaba/`](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0061_nmda_escape_pd_only_no_gaba/results/results_detailed.md) |

# Quick NMDAR-Escape Test on t0059 Substrate at Preferred Direction with GABA = 0

## Source

User-commissioned diagnostic, parallel to t0060 but with NMDAR (Mg-block) replacing AMPA.
Goal: characterise how the from-scratch DSGC's somatic V(t) responds to a single bar moving in
the preferred direction when inhibition is fully removed (GABA = 0) and **NMDA**-only
excitation is swept across a wide range — both with HH active (FULL mode) and disabled
(EPSP_PASSIVE mode).

## Mechanism Choice

This task uses the biologically correct **Mg-block NMDA** (Jahr-Stevens) mechanism inherited
from t0055's `NMDA_MgBlock.mod`. The Mg-block formula and parameter values are taken verbatim
from ModelDB 189347 (Poleg-Polsky 2016): `n = 0.25 /mM`, `gamma = 0.08 /mV`, `tau1 = 5 ms`,
`tau2 = 80 ms`, `e = 0 mV`, `Voff = 0` (voltage-dependent). Without AMPA priming, low-gNMDA
trials are expected to produce minimal response (Mg block is engaged at V_rest = -65 mV); the
sweep tests whether sufficiently high gNMDA can self-prime via leaky Mg-block conductance.

## Sweep

| Axis | Values |
| --- | --- |
| `GABA_BASE_NS` | **0** (no inhibition) |
| AMPA | **0** (no AMPA — NMDA-only excitation) |
| Direction | **theta = 0 deg** only (preferred direction) |
| Trials per condition | **1** |
| `gNMDA` (nS) | {0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} (8 values) |
| Mode | `FULL` (HH on, soma + AIS) and `EPSP_PASSIVE` (HH off, save-and-zero gnabar / gkbar) |

Total: **8 gNMDA x 2 modes x 1 trial x 1 direction = 16 trials**. Wall-clock estimate: ~1-3
minutes on local CPU under CVODE.

## Outputs

* `results/voltage_traces_pd_only.csv` — 16 traces (one row group per (gNMDA, mode) cell),
  full V_soma(t).
* `results/summary_pd_only.csv` — per-(gNMDA, mode) peak / min Vm and spike count.
* `results/images/voltage_response_grid.png` — 8 panels (one per gNMDA), each panel overlays
  FULL (HH-on) and EPSP_PASSIVE (HH-off) trace at theta = 0 deg.
* `results/images/voltage_response_overlay.png` — single combined panel with all 16 traces.
* `results/results_summary.md` and `results_detailed.md`.

## Architecture

Reuses t0059's morphology, placement (seed 0), neuron bootstrap, and trial-mode dispatcher.
The synapse layer is replaced wholesale: each E location gets ONE `NMDA_MgBlock` POINT_PROCESS
plus a NetStim + NetCon (no AMPA Exp2Syn, no GABA tonic). Spatial gating is preserved but with
`GABA = 0` and no AMPA, only the NMDA mechanism is active.

The `NMDA_MgBlock.mod` source is copied verbatim from t0055 (provenance: ModelDB 189347
`bipolarNMDA.mod`) and recompiled in t0061's `code/mod/` for this task's NEURON kernel.

## Out of Scope

* AMPA + NMDA combination (that's t0054 / S-0057-06 territory).
* Voltage-independent NMDA (`Voff = 1`) — fixed `Voff = 0` (Mg-block on).
* Multi-trial statistics, DSI, compare-literature, suggestions.
* Asset production (no library produced).

## Verification Criteria

* Both `voltage_traces_pd_only.csv` and the two PNGs exist.
* `verify_task_file.py`, `verify_task_folder.py`, `verify_task_results.py`, `verify_logs.py`
  all pass with 0 errors.

**Results summary:**

> **Results Summary: t0061 NMDA-Only PD Diagnostic**
>
> **Summary**
>
> Ran 16 trials (8 gNMDA values × 2 modes × 1 trial) at theta = 0 deg with GABA = 0, AMPA = 0,
> NMDA-only excitation (Mg-block, Jahr-Stevens). Wall-clock 118.14 s on local CPU under CVODE.
> Headline: **regenerative Mg-block escape between gNMDA = 1.0 nS** (peak Vm = -58.89 mV, 0
> spikes)
> **and gNMDA = 2.0 nS** (peak Vm = +11.29 mV, **3 spikes**). The NMDA plateau widens to
> ~200-400 ms
> at gNMDA >= 5 nS, far longer than the AMPA EPSP in t0060 (~10 ms).
>
> **Metrics**
>
> * **gNMDA = 0.1 nS**: FULL peak Vm = -64.22 mV, 0 spikes; EPSP_PASSIVE peak Vm = -64.47 mV,
>   0
> spikes. Mg block fully engaged.
> * **gNMDA = 0.5 nS**: FULL peak = -62.61 mV, 0 spikes. Tiny depolarization.
> * **gNMDA = 1.0 nS**: FULL peak = -58.89 mV, 0 spikes. Below the regenerative threshold.
> * **gNMDA = 2.0 nS (Mg-block escape)**: FULL peak = +11.29 mV, **3 spikes**; EPSP_PASSIVE
>   peak =
> -52.58 mV, 0 spikes. Sudden transition: depolarization unblocks Mg, NMDA opens, drives more
> depolarization, fires action potentials.
> * **gNMDA = 5.0 nS**: FULL = +13.12 mV / 3 spikes; EPSP_PASSIVE = -8.59 mV / 1 (false
>   threshold

</details>

<details>
<summary>✅ 0060 — <strong>Quick AMPA-escape test on t0059 substrate at preferred
direction with GABA=0</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0060_ampa_escape_pd_only_no_gaba` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-29T21:39:21Z |
| **End time** | 2026-04-29T22:00:00Z |
| **Step progress** | 7/15 |
| **Task page** | [Quick AMPA-escape test on t0059 substrate at preferred direction with GABA=0](../../../overview/tasks/task_pages/t0060_ampa_escape_pd_only_no_gaba.md) |
| **Task folder** | [`t0060_ampa_escape_pd_only_no_gaba/`](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0060_ampa_escape_pd_only_no_gaba/results/results_detailed.md) |

# Quick AMPA-Escape Test on t0059 Substrate at Preferred Direction with GABA = 0

## Source

User-commissioned quick diagnostic test (no brainstorm). Goal: characterise how the
from-scratch DSGC's somatic V(t) responds to a single bar moving in the preferred direction
when inhibition is fully removed (GABA = 0) and AMPA per-synapse conductance is swept across a
wide range — both with HH active (FULL mode) and disabled (EPSP_PASSIVE mode).

## Motivation

t0059 swept gAMPA in {0.5, 1, 2, 3, 4} nS with bar-arrival-locked GABA from 0.1 to 2 nS and
found the cell trapped in a single-spike-per-trial regime — max peak Hz = 2.143 Hz across all
25 grid cells. The interpretation depended on whether the cap is set by inhibition timing,
AMPA strength, the absence of dendritic conductances, or driving-force saturation. Removing
GABA entirely and extending gAMPA up to 20 nS isolates the AMPA pathway alone, gives the
upper-bound passive depolarization (HH off) and the upper-bound spike count (HH on), and
clarifies whether the single-spike cap is set by AMPA insufficiency or by the
morphology/active-channel substrate.

## Sweep

| Axis | Values |
| --- | --- |
| `GABA_BASE_NS` | **0** (no inhibition, no I synapses driven) |
| Direction | **theta = 0 deg** only (preferred direction) |
| Trials per condition | **1** |
| `gAMPA` (nS) | {0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} (8 values) |
| Mode | `FULL` (HH on, soma + AIS) and `EPSP_PASSIVE` (HH off, save-and-zero gnabar / gkbar) |

Total: **8 gAMPA x 2 modes x 1 trial x 1 direction = 16 trials**. Wall-clock estimate: ~30-90
seconds on local CPU under CVODE.

## Outputs

* `results/voltage_traces_pd_only.csv` — 16 traces (one row group per (gAMPA, mode) cell),
  full V_soma(t) at native dt = 0.025 ms (no down-sampling — total data is small).
* `results/images/voltage_response_grid.png` — 8 panels (one per gAMPA), each panel overlays
  the FULL (HH-on) and EPSP_PASSIVE (HH-off) trace at theta = 0 deg.
* `results/images/voltage_response_overlay.png` — single combined panel with all 16 traces, 8
  colours for gAMPA, 2 line styles for HH on / off.
* `results/results_summary.md` — per-(gAMPA, mode) peak Vm, spike count (FULL only),
  description of the trend.

## Architecture

Reuses t0059's `minimal_dsgc_bar_locked_gaba_ampa_sweep` substrate verbatim with three runtime
overrides:

1. `GABA_BASE_NS_VALUES = (0.0,)` — single value at zero. The bar-arrival-locked window
   mechanism and centripetal-gating predicate remain in place but produce zero conductance per
   synapse.
2. `ANGLES_DEG = (0,)` — preferred direction only.
3. `AMPA_PEAK_NS_VALUES = (0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0)` — extended escape
   range.
4. `N_TRIALS_PER_ANGLE = 1` — single trial per condition (deterministic; trial-to-trial noise
   not relevant for a diagnostic test).

No code copy is needed. The t0059 entry point already supports CLI overrides for AMPA and GABA
subsets, angle subset, and n-trials. The plotting logic is task-specific (custom, not from
t0059) since t0059's plots are designed for the 25-cell grid.

## Out of Scope

* DSI / tuning curve analysis (only one direction).
* Compare-literature (diagnostic test, no published baseline match).
* Multi-trial statistics (single-trial design).
* Negative GABA / inhibition contributions (GABA = 0 by design).
* Asset production (this is a diagnostic — no library asset).

## Verification Criteria

* Both `voltage_traces_pd_only.csv` and the two PNGs exist.
* Each PNG shows monotonic peak-Vm-vs-gAMPA in EPSP_PASSIVE (no HH non-linearity expected) and
  a superlinear regime in FULL once gAMPA crosses spike threshold.
* `verify_task_file.py`, `verify_task_folder.py`, `verify_task_results.py`, `verify_logs.py`
  all pass with 0 errors.

**Results summary:**

> **Results Summary: t0060 Quick AMPA-Escape Test (PD only, GABA = 0)**
>
> **Summary**
>
> Ran 16 trials (8 gAMPA values × 2 modes × 1 trial × 1 direction) at theta = 0 deg with GABA
> = 0
> on the t0059 minimal-DSGC substrate; total wall-clock 127.36 s on local CPU under CVODE. The
> FULL
> (HH on) cell escapes the single-spike regime at gAMPA ≥ 1 nS, peaks at **4 spikes / 1.4 s**
> at
> gAMPA = 20 nS, and stays bounded near +20 mV peak Vm by sodium-channel saturation. The
> EPSP_PASSIVE
> (HH off) trace approaches the AMPA reversal monotonically: peak Vm rises from **-60.7 mV at
> gAMPA =
> 0.1 nS** to **-3.8 mV at gAMPA = 20 nS** (AMPA reversal E_AMPA = 0 mV).
>
> **Metrics**
>
> * **gAMPA = 0.1 nS (subthreshold)**: FULL peak Vm = -58.98 mV, 0 spikes; EPSP_PASSIVE peak
>   Vm =
> -60.67 mV, 0 spikes. Both modes nearly identical — passive cell.
> * **gAMPA = 0.5 nS (single spike escape)**: FULL peak Vm = +18.99 mV (1 spike); EPSP_PASSIVE
>   peak Vm
> = -47.75 mV (no spike). FULL exceeds passive by **+66.7 mV** at peak (HH-driven AP).
> * **gAMPA = 1.0 nS**: FULL = +19.49 mV / 2 spikes; EPSP_PASSIVE = -36.94 mV / 0 spikes.
> * **gAMPA = 2.0 nS**: FULL = +19.13 mV / 2 spikes; EPSP_PASSIVE = -24.68 mV / 0 spikes.
> * **gAMPA = 5.0 nS**: FULL = +17.17 mV / 1 spike; EPSP_PASSIVE = -11.60 mV / 1 (passive Vm
>   crosses

</details>

<details>
<summary>✅ 0059 — <strong>Bar-arrival-locked tonic GABA + AMPA escape sweep on t0057
substrate</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0059_bar_locked_gaba_ampa_sweep_t0057` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0057-04` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-28T23:58:19Z |
| **End time** | 2026-04-29T20:55:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Bar-arrival-locked tonic GABA + AMPA escape sweep on t0057 substrate](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Task folder** | [`t0059_bar_locked_gaba_ampa_sweep_t0057/`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/results/results_detailed.md) |

# Bar-Arrival-Locked Tonic GABA + AMPA Escape Sweep on t0057 Substrate

## Source

Approved in brainstorm session 11 (t0058) and covers four high-priority suggestions in one
combined experimental task:

* **S-0057-04** (primary `source_suggestion`) — per-synapse stimulus-window-tied `(t_on,
  t_off)` tonic GABA on t0057 to model bar-arrival-locked inhibition.
* **S-0057-02** — AMPA conductance escape sweep on the t0057 tonic-GABA substrate.
* **S-0057-01** — sub-0.25 nS finer GABA sweep on t0057 (graded-suppression hypothesis).
* **S-0055-01** — project-wide DSGC measurement-protocol fix (drop legacy E_ONLY / GABA_ONLY
  trio in favour of EPSP_PASSIVE / IPSP_PASSIVE / FULL with HH save-and-zero on the passive
  modes; drop per-synapse activation-time histogram; standardise trial length at 1400 ms).

## Motivation

Five completed from-scratch minimal DSGCs (t0052, t0053, t0054, t0055, t0057) all converge on
a binary regime: either **single-spike-per-trial** (peak Hz = 0.667, vector-sum DSI = 0.7464
with scalar gabaMOD or 1.0 trivially with full PD/ND inhibition) **or full inhibitory
suppression** (peak Hz = 0, DSI = 0). The cell never enters the 5-50 Hz multi-spike band where
DSI metrics become biologically informative.

The convergent diagnosis from this body of work:

1. **AMPA at 0.5 nS x 100 synapses is too weak** to drive multi-spike trains on the t0009
   calibrated morphology. t0052/t0053/t0054/t0055/t0057 all top out at 0.667 Hz under any
   non-saturating inhibition.
2. **Tonic GABA at the per-synapse amplitudes already swept** (0.25-2.0 nS in t0057) either
   does not engage at all (sub-veto, 0.667 Hz uniform) or fully suppresses (0 Hz uniform). No
   intermediate operating point exists in the t0057 grid.
3. **Sustained tonic GABA over a 1300 ms window per active synapse is not biologically
   realistic** either. SAC outputs onto a DSGC dendrite arrive in a brief 100-300 ms envelope
   as the stimulus bar passes the SAC's dendritic field — not as a constant 1.3-second leak.

This task addresses all three issues simultaneously on one combined substrate. It (a)
implements biologically plausible **per-synapse bar-arrival-locked GABA windows** (each active
SAC fires a 200 ms tonic conductance starting at the stimulus's geometric arrival time at that
synapse), (b) sweeps **AMPA conductance** to break the single-spike regime, (c) sweeps **GABA
conductance** including sub-0.25 nS values to characterise the graded-suppression regime, and
(d) ships the **EPSP_PASSIVE / IPSP_PASSIVE / FULL** measurement protocol so synaptic envelope
traces are spike-free and the EPSP-decay metric stops returning null.

## Objective

Build the new bar-arrival-locked tonic GABA mechanism, integrate it into a fork of t0057's
minimal DSGC code, ship the corrected measurement-protocol trio, sweep a 5x5 (gAMPA,
GABA_BASE_NS) grid, and report whether any operating point on the swept grid produces
non-trivial direction selectivity in the multi-spike regime — or rule it out.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction). Identical to t0052 / t0053 / t0054 / t0055 / t0057.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1
  uF/cm^2`.
* V_rest: -65 mV.
* Identical to t0057.

### Synapses

* 100 E + 100 I synapses, **co-located in pairs**, uniform random over dendrites with the same
  fixed seed (0) as t0052 / t0053 / t0057. Identical placement so the placement_seed0 fixture
  from t0057 applies bit-for-bit.

### Excitatory mechanism

* `Exp2Syn`: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV.
* Position-gated firing: each E synapse fires once when the bar's leading edge crosses it;
  direction-independent waveform.
* **Per-synapse peak conductance is the swept variable** — see Sweep section below.

### Inhibitory mechanism (NEW — bar-arrival-locked tonic windows)

* Reuses t0057's `gaba_tonic.mod` POINT_PROCESS with parameters `(g, e, t_on, t_off)`:
  * Sustained conductance `g` (in microsiemens) between `t_on` and `t_off`.
  * Zero conductance outside that window.
  * Reversal `e = -75 mV`.
  * Rise / fall envelope at the window edges as in t0057 (piecewise constant or 1-2 ms cosine
    ramp).
* Per-synapse instance: each I synapse pair gets one `gaba_tonic` mechanism.
* **Spatial gating preserved from t0053 / t0057**: gated synapses are those whose
  `cos(theta_stim - theta_centrifugal_synapse) < 0`. Silent synapses get `g = 0` throughout.
* **NEW per-synapse bar-arrival-locked window** (replaces t0057's global `(100, 1400)`
  window):
  * For each active synapse `i` at coordinate `(x_i, y_i)`:
    * `t_on_i = (x_i * cos(theta_stim) + y_i * sin(theta_stim)) / v + 100 ms`
    * `t_off_i = t_on_i + window_ms`
  * `v` is bar velocity (1000 um/s as in t0053 / t0057).
  * `window_ms = 200` ms (FIXED — biologically motivated midpoint of the 100-300 ms SAC IPSC
    envelope range; not swept in this task).
* Total inhibition envelope per trial: a moving wave of GABA windows that tracks the stimulus
  bar's progression across the dendritic arbor.

### Stimulus protocol

* 12 directions x 10 trials per direction, bar 200 um x full arena, 1000 um/s.
* **Trial length T = 1400 ms** (was 1500 ms in t0052 / t0053 / t0054 / t0055 / t0057; this
  task ships the standardised 1400 ms per S-0055-01 / researcher memory note).
* `dt = 0.025 ms`.

### Measurement-protocol fix (S-0055-01 bundled)

* **Drop** the legacy `E_ONLY` and `GABA_ONLY` modes from the trial code.
* **Add** two new passive modes that share the same synapse activation but disable spike
  generation:
  * `EPSP_PASSIVE` — keep AMPA active, set GABA `g = 0`, save and zero `gnabar_hh` and
    `gkbar_hh` on `soma` and `axon_initial_segment` (restore at end of trial). Records the
    clean EPSP envelope at the soma without spike contamination.
  * `IPSP_PASSIVE` — keep GABA active, set AMPA peak conductance to 0, save and zero
    `gnabar_hh` and `gkbar_hh` on `soma` and `axon_initial_segment` (restore at end of trial).
    Records the clean IPSP envelope at the soma without spike contamination.
* Keep `FULL` with HH active for spike rates / DSI / firing-rate PSTH metrics.
* **Drop** the per-synapse activation-time histogram output (no longer informative once the
  bar-arrival-locked windows are explicit in the design).

## Sweep

| Axis | Values | Units |
| --- | --- | --- |
| `gAMPA` | {0.5, 1.0, 2.0, 3.0, 4.0} | nS per E synapse |
| `GABA_BASE_NS` | {0.1, 0.2, 0.5, 1.0, 2.0} | nS per active I synapse |
| `window_ms` | 200 (FIXED) | ms |

* Total grid: 5 x 5 = **25 grid cells**.
* Per cell: 12 directions x 10 trials x 3 modes (FULL / EPSP_PASSIVE / IPSP_PASSIVE) = 360
  trials.
* Total: **9000 trials**.
* Estimated wall-clock: 9000 / 1800 x 105 min ≈ 8.75 h on local CPU (extrapolating t0057's
  measured 6318 s for 1800 trials).

## Outputs

For each `(gAMPA, GABA_BASE_NS)` grid cell:

1. Soma `V(t)` per direction (12 PNGs, FULL mode).
2. Aggregate EPSP at soma per direction (12 PNGs, EPSP_PASSIVE mode — clean envelope, no
   spikes).
3. Aggregate IPSP at soma per direction (12 PNGs, IPSP_PASSIVE mode — clean envelope, no
   spikes; each direction's plot should show the moving wave of GABA windows).
4. Firing-rate PSTH per direction (12 PNGs, FULL mode).
5. Polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction).

Cross-grid summary plots:

* DSI (primary) heatmap over `(gAMPA, GABA_BASE_NS)`.
* DSI (vector-sum) heatmap over `(gAMPA, GABA_BASE_NS)`.
* Peak Hz heatmap over `(gAMPA, GABA_BASE_NS)` — for locating multi-spike regime.
* Null Hz heatmap over `(gAMPA, GABA_BASE_NS)`.
* HWHM heatmap over `(gAMPA, GABA_BASE_NS)`.
* RMSE vs t0004 target heatmap over `(gAMPA, GABA_BASE_NS)`.
* Regime-boundary contour overlay: single-spike-degenerate vs multi-spike vs full-suppression
  bands on the `(gAMPA, GABA_BASE_NS)` plane.

## Library Asset

Produce one library asset: `minimal_dsgc_bar_locked_gaba_ampa_sweep` (or similar slug). Same
component structure as `minimal_dsgc_tonic_gaba_sweep` from t0057, with three substantive
changes:

1. The GABA driver computes per-synapse `(t_on_i, t_off_i)` from synapse coordinate and
   stimulus direction (replacing t0057's global window).
2. The trial-mode dispatcher exposes `FULL`, `EPSP_PASSIVE`, `IPSP_PASSIVE` (replacing t0057's
   `FULL`, `AMPA_ONLY`, `GABA_ONLY`); HH save-and-zero is implemented inside the passive-mode
   entry points.
3. `gAMPA` is exposed as a public per-synapse parameter (was hard-coded at 0.5 nS in t0057).

## Key Questions

1. Does any `(gAMPA, GABA_BASE_NS)` grid cell produce FULL-mode peak Hz in the **5-50 Hz**
   band?
2. Among grid cells in the multi-spike regime, does any one produce **vector-sum DSI > 0.3**?
3. Does the bar-arrival-locked window mechanism produce direction-dependent IPSP timing that
   the global-window t0057 mechanism could not (i.e., does the IPSP envelope shift with
   `theta`)?
4. Where does the regime boundary lie between single-spike-degenerate, multi-spike, and
   full-suppression behaviour on the `(gAMPA, GABA_BASE_NS)` plane?
5. With clean spike-free EPSP and IPSP traces from EPSP_PASSIVE / IPSP_PASSIVE modes, does the
   EPSP-decay metric (which returned null on t0054 / t0055 due to spike contamination) become
   well-defined and produce useful per-direction values?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~8.75 h for the simulation sweep, plus implementation,
unit testing, and reporting time. Cost: $0.00.

## Out of Scope

* NMDA receptors (AMPA-only on the E pathway; the AMPA + Mg-block-NMDA combination on this
  bar-locked substrate is the natural next task, covered by the still-active S-0057-06).
* Active dendritic conductances (passive dendrites by design — RQ4 follow-up territory).
* Synaptic noise (deterministic NetStim trials).
* Network-level inputs.
* `window_ms` sweep — fixed at 200 ms in this task.
* AMPA values above 4.0 nS — the top of the swept range was trimmed from S-0057-02's 5.0 nS to
  4.0 nS by researcher decision; if the multi-spike regime is not entered at 4.0 nS, a
  follow-up task can extend.

## Verification Criteria

* Library asset validates against `meta/asset_types/library/specification.md`.
* All 25 grid cells produce per-direction PNG plots in `results/images/` and selected
  representatives are embedded in `results_detailed.md`.
* Cross-grid summary heatmaps (DSI / Peak Hz / Null Hz / HWHM / RMSE / regime contour) exist
  and are embedded in `results_detailed.md`.
* `results/metrics.json` contains, for each `(gAMPA, GABA_BASE_NS)` cell: primary DSI,
  vector-sum DSI, preferred direction, peak Hz, null Hz, HWHM, RMSE vs t0004 target.
* Per-synapse bar-arrival-locked window mechanism unit-tested: a regression test asserts that
  the IPSP envelope's centre of mass shifts with bar direction by an amount consistent with
  the stimulus geometry (i.e., centre-of-mass `theta = 0` differs from `theta = 90` by a
  predictable amount given the synapse coordinates).
* HH save-and-zero correctness regression test: at one representative `(gAMPA, GABA_BASE_NS)`
  point, the FULL trace under the new code is bit-identical (within 1e-6 mV) to a reference
  produced from the old t0057 code path with HH active throughout.
* EPSP_PASSIVE peak Vm < spike threshold (~ -50 mV) at every direction and grid cell — gates
  that the save-and-zero is working.
* Same fixed placement seed (0) as t0052 / t0053 / t0057; placement_seed0 match test passes
  bit-for-bit against t0057's placement_seed0.json.
* `verify_research_code.py`, `verify_plan.py`, `verify_task_metrics.py`, and the library asset
  verificator all pass with 0 errors.

**Results summary:**

> **Results Summary: Bar-Arrival-Locked Tonic GABA + AMPA Escape Sweep on t0057 Substrate**
>
> **Summary**
>
> Forked t0057's `minimal_dsgc_tonic_gaba_sweep` library, replaced the global
> `(t_on, t_off) = (100, 1400) ms` tonic-GABA window with per-synapse bar-arrival-locked
> windows
> `t_on_i = (x_i cos theta + y_i sin theta) / v + 100 ms`, `t_off_i = t_on_i + 200 ms`, swept
> a 5x5
> `(gAMPA, GABA_BASE_NS)` grid over `gAMPA in {0.5, 1.0, 2.0, 3.0, 4.0}` nS x
> `GABA_BASE_NS in {0.1, 0.2, 0.5, 1.0, 2.0}` nS, and bundled the project-wide S-0055-01
> measurement-protocol fix (drop `AMPA_ONLY` / `GABA_ONLY`; add `EPSP_PASSIVE` /
> `IPSP_PASSIVE` with
> HH save-and-zero on soma + AIS; standardise trial length at 1400 ms). Headline negative
> finding:
> **no operating point in the swept grid produces multi-spike firing or non-trivial direction
> selectivity**. The maximum FULL-mode peak rate across all 25 cells is **2.143 Hz** (3 spikes
> / 1.4
> s, four cells); the maximum primary DSI is **0.5** at gAMPA=3.0/gaba=0.10 and 0.20; the
> maximum
> vector-sum DSI is **0.209** at gAMPA=1.0/gaba=0.10. The bar-locked window mechanism and HH
> save-and-zero protocol are both validated independently (REQ-13 IPSP centre-of-mass shift =
> 8.5 ms
> between theta=0 and theta=90; REQ-15 worst-case EPSP_PASSIVE peak Vm = -9.04 mV << +5 mV
> gate
> threshold).
>
> **Metrics**

</details>

<details>
<summary>✅ 0058 — <strong>Brainstorm results session 11</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0058_brainstorm_results_11` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md), [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md), [`t0056_brainstorm_results_10`](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md), [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-29T10:00:00Z |
| **End time** | 2026-04-29T12:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 11](../../../overview/tasks/task_pages/t0058_brainstorm_results_11.md) |
| **Task folder** | [`t0058_brainstorm_results_11/`](../../../tasks/t0058_brainstorm_results_11/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0058_brainstorm_results_11/results/results_detailed.md) |

# Brainstorm Session 11: Bar-Arrival-Locked GABA + AMPA Escape on t0057 Substrate

Eleventh brainstorming session. Run on 2026-04-29 after t0055 (Mg-block NMDA recovery test)
and t0057 (tonic-GABA amplitude sweep on t0053 spatial substrate) both completed. The session
is triggered by the convergent finding across the from-scratch minimal DSGC family (t0052,
t0053, t0054, t0055, t0057) that every variant is locked in a binary regime — either
single-spike-per-trial (DSI = 1.0 trivially, peak Hz = 0.667) or full inhibitory suppression
(DSI = 0). The cell needs to escape this binary regime into the 5-50 Hz multi-spike band
before DSI metrics are biologically informative.

## Decision

* **Create t0059** — `bar_locked_gaba_ampa_sweep_t0057`. Forks t0057's
  `minimal_dsgc_tonic_gaba_sweep` library and (a) replaces the global `(t_on, t_off) = (100,
  1400)` ms tonic GABA window with a per-synapse bar-arrival-locked window (`t_on_i = (x_i
  cos(theta) + y_i sin(theta)) / v + 100 ms`, `t_off_i = t_on_i + 200 ms`), (b) bundles the
  project-wide measurement-protocol fix (drop `E_ONLY` / `GABA_ONLY` legacy modes, add
  `EPSP_PASSIVE` / `IPSP_PASSIVE` modes that save-and-zero `gnabar_hh` / `gkbar_hh` on soma +
  AIS so synaptic envelopes are spike-free; drop the per-synapse activation histogram; fix
  trial length at 1400 ms), and (c) sweeps a 5x5 (gAMPA, GABA_BASE_NS) grid covering both the
  sub-veto and multi-spike regimes. Source suggestions: S-0057-01, S-0057-02, S-0057-04,
  S-0055-01 (all four covered).

## Suggestion Cleanup

* **Reject seven high-priority suggestions** as covered or superseded by completed work:
  S-0011-01 (deposited-DSGC line retired; plot_angle_raster_psth exercised on from-scratch
  wave), S-0012-01 (verify_library_asset.py exists and is in active use across
  t0052/t0053/t0054/t0057), S-0012-03 (deposited-DSGC line retired; tuning_curve_loss already
  integrated via metrics.json RMSE on the from-scratch lineage), S-0055-01 (covered by t0059's
  bundled protocol fix), S-0057-01 (covered by t0059's GABA grid including 0.1 / 0.2 nS),
  S-0057-02 (covered by t0059's AMPA grid axis), S-0057-04 (covered by t0059's
  bar-arrival-locked window mechanism).

* **Reprioritise eighteen high-priority suggestions to medium** where the brainstorm-9
  from-scratch pivot or recent results have de-urgented them:

  * Deposited-DSGC and deRosenroll port lineage (retired): S-0003-02, S-0008-01, S-0010-02,
    S-0010-05, S-0024-01, S-0027-02, S-0046-02, S-0020-01, S-0020-02.
  * Morphology and active-channel calibration (deferred to RQ2 / RQ4 follow-ups once a working
    multi-spike substrate exists): S-0009-01, S-0009-02, S-0009-03.
  * Channel/tooling infrastructure (no longer top-of-queue): S-0007-01, S-0013-01, S-0013-02.
  * From-scratch comparisons (defer until working spatial operating point exists): S-0052-04,
    S-0053-02, S-0053-03.

## Tasks Cancelled or Updated

None.

## Assets Produced

No assets in this brainstorm task. The new task t0059 will produce one library asset
(`minimal_dsgc_bar_locked_gaba_ampa_sweep` or similar slug) and an experiment-results bundle
when executed downstream.

**Results summary:**

> **Results Summary: Brainstorm Session 11**
>
> **Summary**
>
> Eleventh strategic brainstorm, run on 2026-04-29 after t0055 (Mg-block NMDA recovery test)
> and t0057
> (tonic-GABA amplitude sweep on t0053 spatial substrate) completed. The session is triggered
> by the
> convergent finding across the from-scratch minimal DSGC family (t0052/t0053/t0054/t0055/
> t0057) that
> every variant is locked in a binary regime — either single-spike-per-trial (peak Hz = 0.667,
> DSI =
> 1.0 trivially) or full inhibitory suppression (peak Hz = 0, DSI = 0). Decision: commission a
> single
> combined task (t0059 — bar-arrival-locked tonic GABA + AMPA escape sweep + bundled
> measurement-protocol fix) covering S-0057-01, S-0057-02, S-0057-04, and S-0055-01 in one
> experimental run; reject seven covered or superseded high-priority suggestions; reprioritise
> eighteen high-priority suggestions to medium where the brainstorm-9 from-scratch pivot or
> recent
> results have de-urgented them.
>
> **Session Overview**
>
> Date: 2026-04-29. Triggered by the convergent binary-regime finding across t0052-t0057. The
> session
> opened with an independent priority reassessment of the 32 high-priority active suggestions
> in light
> of the new t0055 / t0057 evidence (Mg-block NMDA recovers DSI but peak Hz stays at 0.667
> under

</details>

## 2026-04-28 (4)

## ✅ Completed

<details>
<summary>✅ 0057 — <strong>Tonic GABA + amplitude sweep on t0053 spatial
DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0057_tonic_gaba_sweep_t0053` |
| **Status** | completed |
| **Effective date** | 2026-04-28 |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0053-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-28T14:18:58Z |
| **End time** | 2026-04-28T18:02:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Tonic GABA + amplitude sweep on t0053 spatial DSGC](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Task folder** | [`t0057_tonic_gaba_sweep_t0053/`](../../../tasks/t0057_tonic_gaba_sweep_t0053/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0057_tonic_gaba_sweep_t0053/results/results_detailed.md) |

# Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Source

Approved in brainstorm session 10 (t0056) and covers suggestion **S-0053-01** (GABA
conductance sweep on t0053 spatial DSGC to recover a non-zero FULL tuning curve).

## Motivation

t0053 reported a degenerate FULL-mode tuning curve of 0 Hz across all 12 directions because 2
nS GABA on roughly half of 100 synapses (100 nS mean total per trial) fully suppressed spiking
on the t0009-calibrated morphology. While reviewing t0053's traces, the researcher noticed a
second, more fundamental issue: GABA conductance is only present in a narrow ~100-200 ms
window per trial because each spatial-gating GABA synapse fires exactly once at the
bar-arrival time (`t_onset = (x*cos(theta) + y*sin(theta)) / velocity + 100 ms`) and the
Exp2Syn decay is only `tau2 = 20 ms`. With a 1500 ms trial, this leaves the cell uninhibited
for the remaining ~1100 ms — biologically wrong (real SAC→DSGC IPSCs envelope over 100-300 ms
via multiple GABA release events) and the likely root cause of the t0053 amplitude-calibration
sensitivity.

This task fixes the timing problem with a **tonic GABA conductance gated by stimulus window**
(brainstorm-10 Option C: simplest "always-on during stimulus" model) and then sweeps the
per-synapse peak conductance to find the operating point that produces a non-zero FULL-mode
tuning curve while preserving direction selectivity.

## Objective

Build a new GABA mechanism (`gaba_tonic.mod`) that delivers a sustained conductance over a
configurable `(t_on, t_off)` window per synapse, integrate it into the t0053 minimal DSGC code
as a drop-in replacement for the current Exp2Syn GABA mechanism, sweep per-synapse peak
conductance across five values, and report the directional response.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (the t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction). Identical to t0053.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1
  uF/cm^2`.
* V_rest: -65 mV.
* Identical to t0053.

### Synapses

* 100 E + 100 I synapses, **co-located in pairs**, uniform random over dendrites with the same
  fixed seed (0) as t0052 / t0053. Identical placement so the placement_seed0 fixture from
  t0053 applies bit-for-bit.

### Excitatory mechanism (identical to t0053)

* `Exp2Syn`: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV, peak 0.5 nS.
* Position-gated firing: each E synapse fires once when bar leading edge crosses it;
  direction-independent waveform.

### Inhibitory mechanism (NEW — tonic gated by stimulus window)

* New point process: **`gaba_tonic.mod`** with parameters `(g, e, t_on, t_off)`:
  * Sustained conductance `g` (in microsiemens) between simulation times `t_on` and `t_off`.
  * Zero conductance outside that window.
  * Reversal `e = -75 mV` (matches `GABA_E_MV` from t0053).
  * Rise / fall envelope at the window edges: piecewise constant is acceptable, but a 1-2 ms
    cosine ramp to avoid step-function artefacts in the integrator is preferred.
* Per-synapse instance: each pair gets one `gaba_tonic` mechanism.
* **Spatial gating preserved from t0053**: gated synapses are those whose
  `cos(radians(theta_stim - theta_centrifugal_synapse)) < 0`. For each direction:
  * Active synapses: `g = GABA_BASE_NS` (the swept value), `t_on = 100 ms`, `t_off = 1400 ms`.
  * Silent synapses: `g = 0`.
* The `(t_on, t_off) = (100 ms, 1400 ms)` window matches the trial duration minus the 100 ms
  BASE_OFFSET buffer; effectively the GABA conductance is on throughout the entire stimulus
  presentation interval for the active half of the synapse population.

### Stimulus protocol

* Identical to t0053: 12 directions, 10 trials each, bar 200 um x full arena, 1000 um/s, T =
  1500 ms, dt = 0.025 ms.

## Sweep

* `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS — five conductance values.
* Total: 12 directions x 10 trials x 3 modes (FULL / AMPA_ONLY / GABA_ONLY) x 5 conductances =
  1800 trials.
* Estimated wall-clock: ~25-30 min on local CPU per the t0052 / t0053 wall-clock data (19m 13s
  for 360 trials / 17m 11s for 360 trials respectively).

## Outputs

For each conductance value in the sweep:

1. Soma V(t) per direction (12 PNGs).
2. Aggregate EPSP at soma per direction (12 PNGs).
3. Aggregate IPSP at soma per direction (12 PNGs) — the new headline observable; should now
   span the full trial window 100-1400 ms instead of collapsing at ~200 ms.
4. Firing-rate PSTH per direction (12 PNGs).
5. Polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction).
6. Per-synapse activation-time histogram per direction (still informative — synapse onset
   times match t0053 even though the conductance envelope differs).
7. Polar plot of "fraction of I synapses active vs direction" (carried over from t0053; should
   match t0053's 0.34-0.66 modulation since the spatial gating rule is unchanged).

Cross-conductance summary plots:

* DSI (primary) vs `GABA_BASE_NS` — single curve.
* DSI (vector-sum) vs `GABA_BASE_NS` — single curve.
* Peak Hz vs `GABA_BASE_NS` — preferred-direction firing rate as a function of inhibition
  mass.
* Null Hz vs `GABA_BASE_NS` — null-direction firing rate as a function of inhibition mass.
* HWHM vs `GABA_BASE_NS` — tuning sharpness as a function of inhibition mass.
* RMSE vs t0004 target curve at each `GABA_BASE_NS` — distance from project target tuning
  curve.

## Library Asset

Produce one library asset: **`minimal_dsgc_tonic_gaba_sweep`** (or similar slug). Same
component structure as `minimal_dsgc_spatial_gaba` except the inhibition driver uses the new
`gaba_tonic` point process instead of Exp2Syn. The library should expose `GABA_BASE_NS` as a
public parameter so the sweep harness can vary it without re-importing.

## Key Questions

1. Does the tonic-GABA mechanism produce a non-zero FULL-mode tuning curve at any of the swept
   conductance values? If so, at which value(s)?
2. How does direction selectivity (primary DSI, vector-sum DSI) scale with `GABA_BASE_NS`?
   Specifically, is there a window of conductances where DSI is both non-trivial (not 1.0
   single-spike-degenerate, not 0.0 fully-suppressed) and biologically plausible?
3. Does the IPSP somatic voltage envelope now span the full stimulus window (100-1400 ms) as
   intended, or does driving-force saturation still cause the IPSP voltage to collapse early?
4. At the conductance value matching t0053's 2 nS, does the tonic mechanism produce any
   spiking (vs t0053's 0 Hz across all directions), and if so what DSI does it report? This is
   the direct head-to-head against t0053.
5. How does the cross-conductance peak Hz vs target tuning curve compare? Does any single
   `GABA_BASE_NS` value land within an order of magnitude of the t0004 target peak (32 Hz)?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~25-30 min for the simulation sweep, plus implementation
and verification time. Cost: $0.00.

## Out of Scope

* NMDA receptors (AMPA-only minimal model by design, matching t0053).
* Active dendritic conductances (passive dendrites by design).
* Synaptic noise (deterministic NetStim trials).
* Propagation of the tonic-GABA mechanism back to t0052 (scalar gabaMOD) — deferred to a
  future brainstorm if t0057 results justify it.
* Network-level inputs.

## Verification Criteria

* Library asset validates against `meta/asset_types/library/specification.md`.
* All 12 directions x 5 conductances produce per-direction PNG plots in `results/images/` and
  selected representatives are embedded in `results_detailed.md`.
* Cross-conductance summary plots (DSI / Peak Hz / Null Hz / HWHM / RMSE vs `GABA_BASE_NS`)
  exist and are embedded in `results_detailed.md`.
* `results/metrics.json` contains, for each `GABA_BASE_NS` value: primary DSI, vector-sum DSI,
  preferred direction, peak Hz, null Hz, HWHM, RMSE vs t0004 target.
* IPSP voltage trace at the tonic window matches the tonic-GABA design (sustained over
  100-1400 ms, modulo driving-force saturation effects); regression test asserts the IPSP
  voltage at t = 1300 ms is at least 50% of the IPSP voltage at t = 200 ms in the most-active
  direction.
* Same fixed placement seed (0) as t0052 / t0053; placement_seed0_match test passes
  bit-for-bit against t0053's placement_seed0.json.
* AMPA_ONLY mode produces the same 0.667 Hz uniform peak rate as t0052 / t0053 (regression
  gate on the unchanged AMPA path).
* `verify_research_code.py`, `verify_plan.py`, `verify_task_metrics.py`, and the library asset
  verificator all pass with 0 errors.

**Results summary:**

> **Results Summary: Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC**
>
> **Summary**
>
> Replaced t0053's per-event Exp2Syn GABA with a sustained `gaba_tonic` POINT_PROCESS
> (conductance
> held over a configurable `(t_on, t_off) = (100 ms, 1400 ms)` window) and ran a 1800-trial
> sweep
> across `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS. Headline negative finding: no
> operating
> point in the swept grid produces non-trivial direction selectivity. Below 1.5 nS the cell
> fires its
> single-spike-per-trial regime uniformly across all directions (peak = null = 0.667 Hz,
> identical to
> AMPA_ONLY); at 1.5 and 2.0 nS the cell is fully suppressed (peak = null = 0 Hz). The
> active-fraction
> modulation (0.34 → 0.66 across directions) confirms the spatial centripetal-gating rule is
> intact;
> the failure is amplitude calibration interacting with the sustained mechanism, not the
> gating.
>
> **Metrics**
>
> * **Primary DSI (FULL) at all 5 conductances**: **0.0** (degenerate — peak = null at every
>   swept
> value).
> * **Vector-sum DSI (FULL) at all 5 conductances**: **0.0** (3.2e-17 numerical floor for the
>   three
> sub-threshold-suppression values; 0.0 exact for the two fully-suppressed values).
> * **Peak Hz at gaba in {0.25, 0.5, 1.0} nS**: **0.667 Hz** (identical to AMPA_ONLY
>   single-spike

</details>

<details>
<summary>✅ 0056 — <strong>Brainstorm results session 10</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0056_brainstorm_results_10` |
| **Status** | completed |
| **Effective date** | 2026-04-28 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md), [`t0051_brainstorm_results_9`](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-28T12:00:00Z |
| **End time** | 2026-04-28T13:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 10](../../../overview/tasks/task_pages/t0056_brainstorm_results_10.md) |
| **Task folder** | [`t0056_brainstorm_results_10/`](../../../tasks/t0056_brainstorm_results_10/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0056_brainstorm_results_10/results/results_detailed.md) |

# Brainstorm Session 10: Tonic GABA Window Fix on t0053

Tenth brainstorming session. Run on 2026-04-28 after the from-scratch minimal DSGC wave
(t0052, t0053, t0054) completed and t0055 (Mg-block NMDA recovery test) started. The session
is triggered by a researcher observation while reviewing t0053's traces: GABA conductance is
only present in a narrow ~100-200 ms window per trial because each spatial-gating GABA synapse
fires exactly once at the bar-arrival time and the Exp2Syn decay is only `tau2 = 20 ms`. With
a 1500 ms trial duration, this leaves the cell uninhibited for the remaining ~1100 ms —
biologically wrong (real SAC→DSGC IPSCs envelope over 100-300 ms via multiple release events)
and a likely contributor to the amplitude-calibration sensitivity that produced t0053's
degenerate flat-zero FULL tuning.

## Decision

* **Create t0057** — `tonic_gaba_sweep_t0053`. Replace t0053's per-event Exp2Syn GABA
  mechanism with a new `gaba_tonic.mod` point process that delivers a sustained conductance
  over a configurable `(t_on, t_off)` window. Default window: `t_on = 100 ms`, `t_off = 1400
  ms` (full trial minus 100 ms BASE_OFFSET buffer). Preserve t0053's spatial
  centripetal-gating rule (`cos(theta_stim - theta_centrifugal) < 0` selects active synapses);
  replace amplitude. Sweep `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS to locate the
  operating point that produces a non-zero FULL-mode tuning curve. Source suggestion:
  S-0053-01 (covered).

## Suggestion Cleanup

* **Reject four high-priority suggestions** as covered or superseded by completed work:
  S-0015-04 (covered by t0052), S-0016-03 (covered by t0054 + t0055), S-0017-03 (AIS+NMDA done
  in t0052/t0054 and voltage-clamp block in t0049), S-0018-03 (AMPA+NMDA+GABA done in
  t0053+t0054, temporal co-tuning piece deferred to a future fresh suggestion).

* **Reprioritise nineteen high-priority suggestions to medium**:

  * t0022 testbed lineage (de-emphasised by brainstorm 9 pivot): S-0022-01, S-0022-02,
    S-0022-03.
  * t0024 testbed follow-ups: S-0026-02, S-0026-06, S-0034-01, S-0034-02, S-0034-07,
    S-0035-02, S-0039-01.
  * t0033 optimiser prerequisites (deferred until from-scratch substrate is mature):
    S-0033-02, S-0033-03, S-0033-06.
  * Sheffield paywalled-paper retrievals (already bundled into not-started t0031): S-0015-01,
    S-0016-01, S-0017-01, S-0018-01, S-0019-01.
  * Retired deposited-DSGC line: S-0048-01.

## Tasks Cancelled or Updated

None.

## Assets Produced

No assets in this brainstorm task. The new task t0057 will produce a library asset (the new
`gaba_tonic.mod` mechanism wrapped in a Python builder) and an experiment-results bundle when
executed.

**Results summary:**

> **Results Summary: Brainstorm Session 10**
>
> **Summary**
>
> Tenth strategic brainstorm, run on 2026-04-28 after the from-scratch minimal DSGC wave
> (t0052,
> t0053, t0054) completed and t0055 (Mg-block NMDA recovery test) started. Triggered by a
> researcher
> observation that t0053's GABA conductance is only present in a narrow ~100-200 ms window per
> trial
> because each spatial-gating GABA synapse fires exactly once at the bar-arrival time and the
> Exp2Syn
> decay is only `tau2 = 20 ms`. Decision: commission a single new task (t0057) that replaces
> the
> per-event Exp2Syn GABA mechanism with a tonic conductance gated by stimulus window and
> sweeps the
> per-synapse peak conductance to recover non-zero FULL-mode tuning curves; reject four
> covered
> high-priority suggestions; reprioritise nineteen high-priority suggestions to medium where
> the
> brainstorm-9 pivot or recent results have de-urgented them.
>
> **Session Overview**
>
> Date: 2026-04-28. Triggered by the researcher reading t0053's traces and noticing that GABA
> inhibition collapses ~200 ms into the trial, leaving the cell uninhibited for the remaining
> ~1100
> ms. The session opened with an independent priority reassessment of the 50 high-priority
> active
> suggestions in light of the t0052-t0054 findings (t0052's perfect-but-trivial single-spike
> DSI;

</details>

<details>
<summary>✅ 0055 — <strong>Add Mg-block NMDA to recover DSI in t0054 minimal
architecture</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0055_nmda_mg_block_dsi_recovery` |
| **Status** | completed |
| **Effective date** | 2026-04-28 |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0054-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-28T10:48:52Z |
| **End time** | 2026-04-28T13:55:30Z |
| **Step progress** | 9/15 |
| **Task page** | [Add Mg-block NMDA to recover DSI in t0054 minimal architecture](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Task folder** | [`t0055_nmda_mg_block_dsi_recovery/`](../../../tasks/t0055_nmda_mg_block_dsi_recovery/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0055_nmda_mg_block_dsi_recovery/results/results_detailed.md) |

# Add Voltage-Dependent NMDA Mg Block to Recover DSI in the t0054 Minimal Architecture

## Source

Suggestion S-0054-01 (high priority): "Add voltage-dependent NMDA Mg block to recover DSI in
the t0054 minimal AMPA + NMDA + scalar gabaMOD architecture."

## Motivation

t0054 demonstrated that adding a voltage-independent NMDA Exp2Syn (`tau1 = 5 ms`, `tau2 = 80
ms`, `e = 0 mV`) at every AMPA location collapses vector-sum DSI from **0.746** at `gNMDA = 0`
to **0.082** at `gNMDA = 0.25 nS` and to **0.017** at `gNMDA = 1.0 nS`. Peak rate also
degrades because the long-tail NMDA depolarisation removes the directional gating that the
scalar gabaMOD relies on (PD `gaba_mod = 0.33`, ND `gaba_mod = 0.99`). The DSI collapse is
expected from PolegPolsky 2016 (Fig 5) — without a voltage-dependent Mg block, NMDA
conductance fires regardless of postsynaptic voltage and washes out the inhibition-driven
directional asymmetry. Mg block restores multiplicative gain by suppressing NMDA conductance
at hyperpolarised voltages and unblocking it once the cell is already depolarised by AMPA.

This task replaces the t0054 voltage-independent NMDA Exp2Syn with a Jahr-Stevens Mg-block
point process at every E synapse, keeps every other parameter identical, and re-runs the same
gNMDA sweep. The headline question is: does Mg block recover the DSI that t0054 lost?

## Model Specification

Identical to t0054 unless explicitly noted. The change is **only** the NMDA point process;
AMPA, GABA, morphology, HH soma+AIS, placement seed, and stimulus protocol are bit-identical
to t0054.

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (same as t0054).
* 100 dendritic locations sampled with seed = 0 (bit-identical placement to t0054 — enforced
  by a placement-match test against
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/placement_seed0.json`).

### Sections and channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` with the same boosted AIS
  parameters as t0054 (`AIS_LENGTH_UM=30`, `AIS_DIAMETER_UM=2`, `AIS_GNABAR=1.2`,
  `AIS_GKBAR=0.04`, `AIS_GL=0.008`, `AIS_EL_HH=-65`).
* All dendritic sections passive: `Rm = 5999 Ω·cm²`, `Ra = 100 Ω·cm`, `cm = 1 µF/cm²`, `V_rest
  = -65 mV`.

### Synapses

* 100 E + 100 I co-located pairs (identical to t0054).

* **AMPA**: `Exp2Syn` with `tau1 = 0.5 ms`, `tau2 = 2.5 ms`, `e = 0 mV`, peak `0.5 nS`. Driven
  by the same `NetStim` event as the NMDA point process (one event per synapse per trial).

* **NMDA (CHANGED)**: a custom `NMDA_MgBlock` point process replacing the t0054 `Exp2Syn`.
  Same dual-exponential gating kinetics (`tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`) but
  multiplied by the Jahr-Stevens Mg-block factor:

  ```text
  g_NMDA(v, t) = gNMDA_max * s(t) * 1 / (1 + n * exp(-gamma * v))
  ```

  with `n = 0.25 / mM`, `gamma = 0.08 / mV` (the values used in `bipolarNMDA.mod` in t0046's
  ModelDB 189347 reproduction). `s(t)` is the standard Exp2Syn dual-exponential gating
  variable driven by `NetCon` events. `[Mg2+]` is folded into the `n` constant. A `Voff`
  parameter (default `0`) preserves the option to compare against the voltage-independent
  regime.

* **Inhibition**: scalar gabaMOD identical to t0054. `theta_PD = 0`, `theta_ND = 180`, peak `2
  nS × gaba_mod(theta)` where `gaba_mod(0) = 0.33` and `gaba_mod(180) = 0.99`.

### Stimulus protocol

* 12 directions × 10 trials × 3 trial modes × 4 `gNMDA` values = **1440 trials total** (same
  as t0054).
* Bar 200 µm × full arena, 1.0 µm/ms (= 1000 µm/s), 1500 ms per trial.
* `BASE_OFFSET_MS = 100` (bar enters arena at t = 100 ms).

### gNMDA sweep

Four values: `{0.0, 0.25, 0.5, 1.0}` nS — identical to t0054 to enable direct DSI deltas.

* `gNMDA = 0` reproduces t0052 / t0054 within rounding (validation gate).
* `gNMDA = 0.25` is the failure point in t0054 (DSI 0.082); the pass criterion targets this
  point.
* `gNMDA = 0.5` matches the Poleg-Polsky 2016 baseline.
* `gNMDA = 1.0` is twice the Poleg-Polsky baseline; a coarse high-end probe.

### Trial modes

* `FULL` — AMPA + NMDA + GABA active.
* `E_ONLY` — AMPA + NMDA active, GABA `NetCon` weights zeroed.
* `GABA_ONLY` — AMPA + NMDA `NetCon` weights zeroed, GABA active.

## Pass / Fail Criterion

The headline gate from S-0054-01:

* **Vector-sum DSI at `gNMDA = 0.25 nS` must exceed 0.50** (vs t0054 result 0.082).
* **Peak Hz at `gNMDA = 0.25 nS` (preferred direction, FULL) must reach >= 5 Hz**.

Reporting must explicitly state PASS or FAIL against this criterion in the headline summary.

## Outputs

### Per `gNMDA` value × per direction (4 × 12 = 48 panels per output type)

* Soma `V(t)` (FULL mode), mean ± SD across 10 trials.
* Aggregate EPSP (`E_ONLY`), mean ± SD.
* Aggregate IPSP (`GABA_ONLY`), mean ± SD.
* PSTH (5 ms bins, FULL mode).
* Per-synapse activation-time histogram.

### Sweep summary (the headline plots)

1. **Vector-sum DSI vs gNMDA** with t0054 (no-Mg) curve overlaid as a baseline — directly
   visualises the recovery (or lack thereof). X-axis: `gNMDA` (4 points). Y-axis: DSI. Two
   curves: this task vs t0054.
2. **Peak Hz vs gNMDA** with t0054 overlaid.
3. **EPSP decay-time-constant vs gNMDA** with t0054 overlaid (note: t0054 reports null for
   this metric due to the 1500 ms window; this task may inherit the same limitation).
4. **NMDA Mg-block g(v) curve** at the synapse — sanity plot showing the Boltzmann factor at
   `v ∈ [-80, +20] mV`.

### `metrics.json` (multi-variant format)

One variant per `(gNMDA, mode)` combination = 12 variants. Each variant carries the registered
keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`. Variant `id` schema: `gnmda_<value>_<mode>` (e.g., `gnmda_0.50_full`).

### `derived_quantities.json`

Per-variant: `peak_hz`, `null_hz`, `vector_sum_dsi`, `preferred_direction_deg`,
`active_fraction`. Per-`gNMDA`: `epsp_decay_to_1e_ms` for the `E_ONLY` variant at the
preferred direction. Plus `pass_criterion_dsi_at_gnmda_025`,
`pass_criterion_peak_hz_at_gnmda_025`, `pass_criterion_overall` (boolean).

## Library Asset

`minimal_dsgc_mg_block_nmda` under `tasks/t0055_nmda_mg_block_dsi_recovery/assets/library/`.
Includes:

* The new `NMDA_MgBlock.mod` MOD file.
* The full Python codebase (forked from t0054 with NMDA-only changes).
* A README documenting the Mg-block formula, parameter choices, and provenance (derived from
  bipolarNMDA.mod in t0046 / ModelDB 189347).

## Code Design

### Modules to copy verbatim from t0054 (with import-path rewrite to `tasks.t0055_*` and bootstrap sentinel renamed to `_T0055_NEURONHOME_BOOTSTRAPPED`)

`paths.py`, `swc_io.py`, `cell.py`, `placement.py`, `neuron_bootstrap.py`, `trial.py`,
`metrics_extra.py`, `test_quiescent_rest.py`, `test_gaba_mod.py`, `__init__.py`,
`run_tuning_curve.py`, `compute_metrics.py`, `render_figures.py`. (13 files.)

### New files

* **`code/mod/NMDA_MgBlock.mod`** — the new NMDA point process with Mg-block. Provenance noted
  in the file header (derived from bipolarNMDA.mod, ModelDB 189347).

### Modules to extend

* **`constants.py`** — copy from t0054, then rename references such that NMDA point process is
  `NMDA_MgBlock` rather than `Exp2Syn`. Add `MG_BLOCK_N = 0.25` (per-mM coefficient),
  `MG_BLOCK_GAMMA = 0.08` (per-mV coefficient), `MG_BLOCK_VOFF = 0` (0 = voltage-dependent).
* **`synapses.py`** — replace `h.Exp2Syn` for NMDA with `h.NMDA_MgBlock`. Set `tau1`, `tau2`,
  `e`, `n`, `gamma`, `Voff` from constants. The `NetCon.weight[0] = gnmda_ns * 1e-3` mechanism
  is unchanged. Keep AMPA `Exp2Syn` exactly as in t0054.
* **`neuron_bootstrap.py`** — extend the `nrnivmodl` step to compile `mod/NMDA_MgBlock.mod`
  alongside the existing MODs (this task is the first to introduce a custom MOD into the
  minimal architecture).

### Validation gates (run before the full sweep)

* **Quiescent rest test**: `V_rest = -65 ± 0.5 mV` with no synapses (same as t0054).
* **`gNMDA = 0` cross-task regression gate**: `tuning_curve_full` rows at `gNMDA = 0` must
  match t0054's `tuning_curve_full.csv` row-by-row at `gNMDA = 0` within 1e-6 Hz tolerance.
  With `gNMDA = 0` the Mg-block factor evaluates to a finite number but multiplies a zero
  conductance, so the result must be bit-identical to t0054 at gNMDA = 0 (which itself was
  bit-identical to t0052).
* **Placement bit-identical to t0054**: read
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/placement_seed0.json` and assert
  per-synapse coordinates match.
* **NMDA voltage-dependence sanity test**: with a single NMDA_MgBlock point process
  voltage-clamped at v ∈ {-80, -60, -40, -20, 0, +20} mV, drive a single NetCon event and
  record peak gNMDA. Expected pattern: peak gNMDA at -80 mV is ~5x smaller than at -20 mV;
  peak gNMDA monotonically increases with depolarisation up to the asymptote.

## Compute and Budget

Local CPU only. Estimated wall-clock ≈ 75 minutes for 1440 trials at ~3 s/trial (matching
t0054). $0 cost. No remote machines.

If wall-clock exceeds 4 hours (as t0054's actual run did), abort and create a separate
parallelisation task (S-0054-06 covers exactly this).

## Out of Scope

* Joint (gAMPA, gNMDA, gGABA) conductance sweep (covered by S-0054-02).
* NMDA tau2 sweep at fixed gNMDA (covered by S-0054-05).
* Switching back to voltage-independent NMDA (`Voff = 1`) — kept available as a parameter for
  future ablation, not exercised in this task's sweep.
* Spatial PD/ND-asymmetric inhibition (covered by t0053).
* Any morphology, AMPA, GABA, or HH parameter changes.
* Improved EPSP-decay metric (covered by S-0054-03).

## Key Questions

1. Does the Mg-block NMDA recover vector-sum DSI at `gNMDA = 0.25 nS` to >= 0.50 (PASS) or
   does the collapse persist (FAIL)?
2. Does peak rate at `gNMDA = 0.25 nS` reach the >= 5 Hz threshold?
3. How does the DSI vs gNMDA curve compare to t0054's voltage-independent curve at every
   `gNMDA` value?
4. Does the Boltzmann gating work as expected in single-synapse voltage-clamp tests (sanity
   gate above)?

## Verification Criteria

* Library asset structure validates against `meta/asset_types/library/specification.md`.
* `metrics.json` contains 12 variants (4 × 3); all use the registered metric keys.
* All gates pass (quiescent rest, gNMDA=0 cross-task regression vs t0054, placement match,
  NMDA voltage-dependence sanity).
* The `gNMDA = 0` FULL variant reproduces t0054's gNMDA=0 row at 0e+00 Hz max diff across 120
  rows.
* Headline summary in `results_summary.md` explicitly states PASS or FAIL on the S-0054-01
  pass criterion (`vector-sum DSI > 0.50` and `peak Hz >= 5 Hz` at `gNMDA = 0.25 nS`, FULL).
* All 240+ per-direction PNGs and 11+ sweep-summary PNGs exist and are embedded in
  `results_detailed.md` (sample of headline figures inline; rest linked).

**Results summary:**

> **t0055 Results Summary — Mg-Block NMDA DSI Recovery**
>
> **Summary**
>
> Voltage-dependent (Jahr-Stevens Mg-block) NMDA at every E synapse **recovers vector-sum
> DSI** from
> t0054's collapsed 0.082 (gNMDA = 0.25 nS, voltage-independent) back to **0.7464**, a 9×
> recovery
> and bit-identical to the gNMDA = 0 baseline. **Peak rate stays at 0.667 Hz** at every gNMDA
> value
> because the scalar gabaMOD inhibition prevents the soma from depolarising above the
> Mg-unblock
> threshold. The S-0054-01 pass criterion (DSI > 0.50 AND peak Hz >= 5 Hz at gNMDA = 0.25,
> FULL) is
> **PARTIAL: PASS on DSI, FAIL on peak-Hz**.
>
> **Metrics**
>
> * **Vector-sum DSI at gNMDA = 0.25 nS, FULL = 0.7464** vs t0054's 0.082 — a **9.1×
>   recovery** and
> identical to gNMDA = 0 (PASS, threshold > 0.50)
> * **Peak Hz at gNMDA = 0.25 nS, FULL = 0.667 Hz** — unchanged from gNMDA = 0 baseline (FAIL,
> threshold >= 5 Hz)
> * **DSI is gNMDA-invariant in FULL mode**: 0.7464 at every gNMDA in {0, 0.25, 0.5, 1.0} nS —
>   Mg
> block keeps NMDA fully blocked under inhibition
> * **E_ONLY mode reveals NMDA does activate without GABA**: peak Hz rises from 0.667 (gNMDA =
>   0) to

</details>

<details>
<summary>✅ 0054 — <strong>Minimal DSGC with AMPA + NMDA excitation and scalar
gabaMOD inhibition</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0054_minimal_dsgc_ampa_nmda_scalar_gaba` |
| **Status** | completed |
| **Effective date** | 2026-04-28 |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0052-03` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-27T21:14:19Z |
| **End time** | 2026-04-28T05:00:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Minimal DSGC with AMPA + NMDA excitation and scalar gabaMOD inhibition](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Task folder** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba/`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/results_detailed.md) |

# Minimal DSGC with Co-Located AMPA + NMDA Excitation and Scalar gabaMOD Inhibition

## Source

Suggestion S-0052-03 (medium priority): "Add NMDA component to t0052 minimal DSGC and measure
DSI / peak-rate response."

## Motivation

t0052 produced a from-scratch minimal DSGC with AMPA-only excitation and scalar gabaMOD
inhibition. The aggregate EPSP at the soma decays within ~30 ms after the last synapse fires
because per-synapse AMPA `tau2 = 2.5 ms` and the membrane time constant `τ_m = R_m × C_m ≈ 6
ms`. Real DSGC EPSPs decay much more slowly because they have a substantial NMDA component
(typical NMDA decay τ ≈ 50-200 ms). t0052 also produced only one spike per trial in FULL mode
at the preferred direction, which over-saturates primary DSI to 1.0 trivially.

This task extends t0052 by adding a co-located NMDA `Exp2Syn` at each E synapse location and
runs a small `gNMDA` sweep so we can directly answer:

* How does the EPSP decay time constant scale with `gNMDA`?
* Does NMDA close the peak-rate gap (t0052: 0.667 Hz vs Park 2014 in vivo 30-100 Hz)?
* Does NMDA improve or degrade DSI under the scalar `gabaMOD` inhibition mechanism?
* At what `gNMDA` does the cell start firing multiple spikes per trial (escaping the
  single-spike degenerate regime)?

## Model Specification

Identical to t0052 unless explicitly noted.

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (same as t0052/t0053).
* 100 dendritic locations sampled with seed = 0 (bit-identical placement to t0052/t0053 —
  enforced by a placement-match test).

### Sections and channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` with the same boosted AIS
  parameters as t0052 (`AIS_LENGTH_UM=30`, `AIS_DIAMETER_UM=2`, `AIS_GNABAR=1.2`,
  `AIS_GKBAR=0.04`, `AIS_GL=0.008`, `AIS_EL_HH=-65`).
* All dendritic sections passive: `Rm = 5999 Ω·cm²`, `Ra = 100 Ω·cm`, `cm = 1 µF/cm²`, `V_rest
  = -65 mV`.

### Synapses

* 100 E + 100 I co-located pairs.
* **Excitation**: at each E location, both an AMPA and an NMDA `Exp2Syn` are co-located on the
  same segment, driven by **the same** `NetStim` event (one event per synapse per trial,
  position-gated by the bar). AMPA: `tau1 = 0.5 ms`, `tau2 = 2.5 ms`, `e = 0 mV`, peak `0.5
  nS` (same as t0052). NMDA: `tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`, peak conductance
  `gNMDA` (swept).
* NMDA is **voltage-independent** in this minimal model (no Mg²⁺ block). Voltage-dependent
  NMDA with proper Mg block is deferred to a follow-up task.
* **Inhibition**: scalar gabaMOD identical to t0052. `theta_PD = 0`, `theta_ND = 180`, peak `2
  nS × gaba_mod(theta)` where `gaba_mod(0) = 0.33` and `gaba_mod(180) = 0.99`.

### Stimulus protocol

* 12 directions × 10 trials × 3 trial modes × 4 `gNMDA` values = 1440 trials total.
* Bar 200 µm × full arena, 1.0 µm/ms (= 1000 µm/s), 1500 ms per trial.
* `BASE_OFFSET_MS = 100` (bar enters arena at t = 100 ms).

### gNMDA sweep

Four values: `{0.0, 0.25, 0.5, 1.0}` nS.

* `gNMDA = 0` reproduces t0052 within rounding (validation gate).
* `gNMDA = 0.5` matches the Poleg-Polsky 2016 baseline.
* `gNMDA = 1.0` is twice the Poleg-Polsky baseline; a coarse high-end probe.

### Trial modes

* `FULL` — AMPA + NMDA + GABA active.
* `E_ONLY` — AMPA + NMDA active, GABA `NetCon` weights zeroed (replaces t0052's `AMPA_ONLY`).
* `GABA_ONLY` — AMPA + NMDA `NetCon` weights zeroed, GABA active.

## Outputs

### Per `gNMDA` value × per direction (4 × 12 = 48 panels per output type)

* Soma `V(t)` (FULL mode), mean ± SD across 10 trials.
* Aggregate EPSP (`E_ONLY`), mean ± SD.
* Aggregate IPSP (`GABA_ONLY`), mean ± SD.
* PSTH (5 ms bins, FULL mode).
* Per-synapse activation-time histogram.

Approximately 12 × 5 = 60 PNGs per `gNMDA` value × 4 sweep values = ~240 per-direction PNGs,
plus 8 polar/Cartesian per-`gNMDA` overview PNGs and 3 sweep-summary PNGs.

### Sweep summary (the headline plots)

1. **EPSP decay-time-constant vs gNMDA** — directly answers the user's question. X-axis:
   `gNMDA` (4 points). Y-axis: time from EPSP peak to `1/e` (≈ 36.8 %) of peak. One line per
   direction or one aggregate.
2. **Peak Hz vs gNMDA** — line plot, one curve per direction.
3. **DSI vs gNMDA** — primary DSI and vector-sum DSI vs `gNMDA`.

### `metrics.json` (multi-variant format)

One variant per `(gNMDA, mode)` combination = 12 variants. Each variant carries the registered
keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`. Variant `id` schema: `gnmda_<value>_<mode>` (e.g., `gnmda_0.50_full`).

### `derived_quantities.json`

Per-variant: `peak_hz`, `null_hz`, `vector_sum_dsi`, `preferred_direction_deg`,
`active_fraction` (constant 1.0 here; included for parity with t0053). Per-`gNMDA`:
`epsp_decay_to_1e_ms` for the `E_ONLY` variant at the preferred direction. Plus the existing
t0052 fields (`gaba_mod_pd`, `gaba_mod_nd`, etc.).

## Library Asset

`minimal_dsgc_ampa_nmda_scalar_gaba` under
`tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/library/`.

## Code Design

### Modules to copy verbatim from t0052 (with import-path rewrite to `tasks.t0054_*` and bootstrap sentinel renamed to `_T0054_NEURONHOME_BOOTSTRAPPED`)

`paths.py`, `swc_io.py`, `cell.py`, `placement.py`, `neuron_bootstrap.py`, `trial.py`,
`metrics_extra.py`, `test_quiescent_rest.py`, `test_gaba_mod.py`, `__init__.py`. (10 files.)

### Modules to extend

* **`constants.py`** — add `NMDA_TAU1_MS=5.0`, `NMDA_TAU2_MS=80.0`, `NMDA_E_MV=0.0`,
  `NMDA_PEAK_NS_VALUES=(0.0, 0.25, 0.5, 1.0)`, `COL_GNMDA_NS = "gnmda_ns"`, and rename
  `TrialMode.AMPA_ONLY` → `TrialMode.E_ONLY` (or add `E_ONLY` and keep `AMPA_ONLY` as a legacy
  alias).
* **`synapses.py`** — extend `EiPair` with `nmda_syn`, `nmda_netcon`. `build_ei_pairs` creates
  the NMDA `Exp2Syn` at the same segment and a single shared `NetStim`-driven `NetCon`.
  `schedule_ei_onsets` accepts `gnmda_ns: float` and sets `nmda_netcon.weight[0] = gnmda_ns *
  1e-3`. NMDA fires from the same `NetStim.start` as AMPA — no second NetStim is needed.
* **`run_tuning_curve.py`** — add an outer loop over `gNMDA` values. Per-mode CSVs gain a
  `gnmda_ns` column. File names get a per-`gNMDA` suffix or all `gNMDA` rows are appended to a
  single CSV (the latter is preferred for downstream analysis ergonomics).
* **`compute_metrics.py`** — group by `(gnmda_ns, mode)` to compute one variant per group;
  also compute `epsp_decay_to_1e_ms` at the preferred direction per `gNMDA`.
* **`render_figures.py`** — extend with per-`gNMDA` per-direction loops and the three
  sweep-summary plots.

### Validation gates (run before the full sweep)

* **Quiescent rest test**: `V_rest = -65 ± 0.5 mV` with no synapses (same as t0052).
* **gNMDA = 0 sanity**: `tuning_curve_full` rows at `gNMDA = 0` must match t0052's
  `tuning_curve_full.csv` row-by-row within 1e-6 Hz tolerance. This validates that the NMDA
  branch is correctly inert at `gNMDA = 0` and that nothing else regressed.
* **Placement bit-identical to t0052**: read
  `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` and assert per-synapse
  coordinates match (same test as t0053).

## Compute and Budget

Local CPU only. ~75 min wall-clock for 1440 trials at ~3 s/trial. $0 cost.

## Out of Scope

* Voltage-dependent NMDA with Mg²⁺ block (deferred to a future task).
* Spatial PD/ND-asymmetric inhibition (covered by t0053).
* Any morphology or HH parameter changes.
* AMPA conductance sweep (covered by suggestion S-0052-01).
* Cross-comparison with t0053 (covered by suggestion S-0052-04).

## Key Questions

1. How does the EPSP decay-to-1/e time scale with `gNMDA`? At what `gNMDA` does it reach the
   "biologically realistic" 50-100 ms range?
2. Does adding NMDA close the peak-rate gap (t0052: 0.667 Hz, in vivo 30-100 Hz)?
3. Does NMDA improve or degrade primary DSI under scalar `gabaMOD`? Does the trivial
   single-spike DSI = 1 of t0052 give way to a more interesting non-trivial tuning curve?
4. At what `gNMDA` does the cell start firing multiple spikes per trial (escaping the
   single-spike degenerate regime)?

## Verification Criteria

* Library asset structure validates against `meta/asset_types/library/specification.md`.
* `metrics.json` contains 12 variants (4 × 3); all use the registered metric keys.
* All gates pass (quiescent rest, gNMDA=0 sanity, placement match).
* The `gNMDA = 0` FULL variant reproduces t0052's primary DSI = 1.0, peak Hz = 0.667 Hz, and
  null Hz = 0.0 Hz to within rounding.
* All 240+ per-direction PNGs and 11+ sweep-summary PNGs exist and are embedded in
  `results_detailed.md` (sample of headline figures inline; rest linked).

**Results summary:**

> **Results Summary: Minimal DSGC with AMPA + NMDA Excitation and Scalar gabaMOD**
>
> **Summary**
>
> Built a minimal DSGC extending t0052 with co-located NMDA `Exp2Syn` (tau1=5 ms, tau2=80 ms,
> e=0 mV)
> at every E synapse and ran a 4-value gNMDA sweep (`{0.0, 0.25, 0.5, 1.0}` nS) × 12
> directions × 10
> trials × 3 modes (1440 trials, 4 h 19 min wall-clock on local CPU). The gNMDA=0 regression
> gate
> against t0052's `tuning_curve_full.csv` passed at **max |rate diff| = 0.000e+00 Hz** across
> all 120
> rows. Headline finding: NMDA dramatically closes the peak-rate gap (peak Hz at preferred
> direction
> goes from 0.667 (t0052) to 8.0 at gNMDA=0.25 nS), but scalar `gabaMOD` inhibition is too
> weak to
> maintain direction selectivity once NMDA is active — vector-sum DSI collapses from 0.746
> (gNMDA=0)
> to 0.082 (gNMDA=0.25) and approaches 0 at higher gNMDA.
>
> **Metrics**
>
> * **gNMDA=0.0 nS, FULL**: peak 0.667 Hz, null 0.000 Hz, vector-sum DSI 0.746, primary DSI
>   1.000
> (degenerate). **Matches t0052 exactly** — regression gate passed at 0e+00 Hz max diff.
> * **gNMDA=0.25 nS, FULL**: peak 8.000 Hz, null 6.000 Hz, vector-sum DSI 0.082. ~12× firing
>   rate vs
> gNMDA=0; DSI collapses ~9×.
> * **gNMDA=0.5 nS, FULL**: peak 7.333 Hz, null 6.000 Hz, vector-sum DSI 0.029. Saturating;
>   scalar

</details>

## 2026-04-27 (2)

## ✅ Completed

<details>
<summary>✅ 0053 — <strong>Minimal from-scratch DSGC with spatial PD/ND-asymmetric
inhibition</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0053_minimal_dsgc_spatial_gaba` |
| **Status** | completed |
| **Effective date** | 2026-04-27 |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | — |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-27T12:36:44Z |
| **End time** | 2026-04-27T14:10:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Minimal from-scratch DSGC with spatial PD/ND-asymmetric inhibition](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Task folder** | [`t0053_minimal_dsgc_spatial_gaba/`](../../../tasks/t0053_minimal_dsgc_spatial_gaba/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0053_minimal_dsgc_spatial_gaba/results/results_detailed.md) |

# Minimal From-Scratch DSGC with Spatial PD/ND-Asymmetric Inhibition

## Source

Approved in brainstorm session 9 (t0051) as Task B of a paired wave (t0052 scalar gabaMOD,
t0053 spatial PD/ND-asymmetric). No upstream suggestion ID; this task is created directly from
the session's strategic pivot to a from-scratch minimal-DSGC substrate.

## Motivation

This task is the spatial-asymmetry sibling of t0052. Where t0052 scales each I synapse's
amplitude by a global direction-dependent scalar, t0053 instead activates a synapse only when
the moving stimulus is approaching the synapse from outside the soma (centripetal motion). The
aggregate effect mimics the SAC network's known centrifugal preference (SAC dendrites release
GABA preferentially when stimuli move centrifugally over them, so from the post-synaptic
DSGC's perspective inhibition concentrates on dendrites being approached from the wrong side).

The two tasks isolate the impact of inhibition mechanism (scalar amplitude scaling vs spatial
gating) on direction selectivity at otherwise-identical morphology, excitation, spike
generation, and stimulus.

## Objective

Build and run a minimal compartmental DSGC model with the following specification, then report
per-direction voltage and firing-rate data so the behaviour can be compared against the
project's target tuning curve and against t0052.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (the t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction).
* Compartments: as defined in the asset; standard NEURON section discretisation.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1
  uF/cm^2`.
* V_rest: -65 mV.

### Synapses

* 100 E + 100 I synapses, **co-located in pairs**, uniform random over dendrites with the same
  fixed seed (0) as t0052. (Identical placement across the two tasks lets later comparison
  isolate the inhibition mechanism.)

### Excitatory mechanism (identical to t0052)

* `Exp2Syn`: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV, peak 0.5 nS.
* Position-gated firing: each E synapse fires once when bar leading edge crosses it;
  direction-independent waveform.

### Inhibitory mechanism (spatial PD/ND-asymmetric, centripetal-only firing)

* `Exp2Syn`: rise = 1 ms, decay = 20 ms, e = -75 mV, peak 2 nS (no scalar scaling).
* For each I synapse i, define a centrifugal direction `theta_centrifugal_i = atan2(y_i -
  y_soma, x_i - x_soma)`.
* Synapse i fires only when the bar direction `theta_stim` satisfies `cos(theta_stim -
  theta_centrifugal_i) < 0`. Equivalently, the synapse fires when the stimulus motion has a
  component pointing back toward the soma (centripetal).
* When the firing condition is satisfied, the synapse fires one event at the moment the bar
  leading edge crosses its (x, y).
* Aggregate effect: for any given bar direction, only the half of I synapses whose centrifugal
  vectors point into the bar-incoming hemisphere will fire. Inhibition is spatially
  concentrated on the side of the dendritic field being approached "from the wrong end".

### Stimulus protocol

* Identical to t0052: 12 directions, 10 trials each, bar 200 um x full arena, 1000 um/s, T =
  1500 ms.

## Outputs

Same six output classes as t0052, plus one additional plot specific to the spatial mechanism:

1. Soma V(t) per direction.
2. Aggregate EPSP at soma per direction.
3. Aggregate IPSP at soma per direction.
4. Firing-rate PSTH per direction.
5. Polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction).
6. Per-synapse activation-time histogram per direction.
7. **Polar plot of "fraction of I synapses active vs direction"** — confirms the
   centripetal-gating mechanism produces the expected directional asymmetry in the active I
   population.

## Library Asset

Produce one library asset: `minimal_dsgc_spatial_gaba`. Same component structure as
`minimal_dsgc_scalar_gaba` except the inhibition driver implements the centripetal-gating rule
instead of scalar gabaMOD scaling.

## Key Questions

1. Does spatial gating produce a higher or lower DSI than scalar gabaMOD on the same
   morphology and excitation?
2. Is the preferred direction of the model the same as t0052's, given that the underlying
   morphology is asymmetric (the soma is offset from the dendritic-field centroid)?
3. Does the "fraction of I synapses active" curve show the predicted ~50% modulation across
   direction, or does the morphology asymmetry produce a stronger / weaker modulation?
4. Does the spatial mechanism reproduce a biologically-realistic null-side-leading null
   inhibition timing pattern in the IPSP traces?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~1 week. Cost: $0.00.

## Out of Scope

* NMDA receptors (AMPA-only minimal model by design).
* Active dendritic conductances.
* Synaptic noise.
* Network-level inputs.
* Cross-comparison to t0052 (handled by a downstream task once both finish).

## Verification Criteria

* Library asset validates against `meta/asset_types/library/specification.md`.
* All 12 directions produce a per-direction PNG plot in `results/images/` and are embedded in
  `results_detailed.md`.
* `results/metrics.json` contains primary DSI, vector-sum DSI, preferred direction, peak Hz,
  null Hz at minimum.
* The synapse-activation polar plot shows roughly 50% of I synapses active in each direction
  (any deviation must be explained by the dendritic-field asymmetry).
* Synapse placement uses the same fixed seed (0) as t0052 so the two tasks can be compared
  trial-for-trial in a downstream analysis.

**Results summary:**

> **Results Summary: Minimal From-Scratch DSGC with Spatial PD/ND-Asymmetric Inhibition**
>
> **Summary**
>
> Built a from-scratch minimal DSGC on `dsgc-baseline-morphology-calibrated` (same morphology
> and
> synapse placement seed as t0052) with 100 E + 100 I co-located synapses, position-gated
> AMPA-only
> excitation, and **centripetal-only spatial gating** of GABA inhibition (each I synapse fires
> at full
> 2 nS amplitude only when `cos(θ_stim − θ_centrifugal_synapse) < 0`, zero otherwise). Ran the
> full 12-direction × 10-trial × 3-mode sweep (360 trials in 17 min 11 s on local CPU).
> Headline
> finding: **the FULL-mode tuning curve is identically 0 Hz across all directions** — the
> spatial
> mechanism with full 2 nS GABA on ~50% of synapses fully suppresses spiking on this
> morphology /
> synapse-density configuration. AMPA_ONLY fires uniformly at 0.667 Hz (excitation works at
> threshold). The active-fraction soft sanity check passes (mean = 0.5000 ∈ [0.4, 0.6]).
>
> **Metrics**
>
> * **Primary DSI (FULL)**: **0.0** — degenerate; both peak and null directions fire 0 Hz.
> * **Peak Hz / Null Hz (FULL)**: **0.0 / 0.0** — full inhibitory suppression.
> * **Vector-sum DSI (FULL)**: **0.0** — degenerate.
> * **HWHM**: **180.0°** — degenerate (flat-zero tuning curve).

</details>

<details>
<summary>✅ 0052 — <strong>Minimal from-scratch DSGC with scalar gabaMOD
inhibition</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0052_minimal_dsgc_scalar_gaba` |
| **Status** | completed |
| **Effective date** | 2026-04-27 |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | — |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-27T09:58:55Z |
| **End time** | 2026-04-27T12:20:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Minimal from-scratch DSGC with scalar gabaMOD inhibition](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Task folder** | [`t0052_minimal_dsgc_scalar_gaba/`](../../../tasks/t0052_minimal_dsgc_scalar_gaba/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0052_minimal_dsgc_scalar_gaba/results/results_detailed.md) |

# Minimal From-Scratch DSGC with Scalar gabaMOD Inhibition

## Source

Approved in brainstorm session 9 (t0051) as Task A of a paired wave (t0052 scalar gabaMOD,
t0053 spatial PD/ND-asymmetric). No upstream suggestion ID; this task is created directly from
the session's strategic pivot away from the deposited Poleg-Polsky 2016 lineage and the t0022
channel-testbed lineage.

## Motivation

The t0046–t0050 reproduction wave demonstrated that the deposited ModelDB 189347 code does not
implement the mechanism described in the Poleg-Polsky 2016 paper text, and that the t0022
modified-port lineage carries accumulated deviations from that paper as well. Brainstorm
session 9 commissioned a new from-scratch minimal DSGC built on the project's calibrated
baseline morphology so that all parameters and mechanisms are explicit, audited, and clean of
upstream-code legacy.

This task implements the **scalar gabaMOD** variant of deRosenroll-style direction-dependent
inhibition, which is the form actually published in Poleg-Polsky 2016 and also a faithful
abstraction of de Rosenroll 2026's effective DSGC inhibition: every inhibitory synapse fires
when the bar covers it, but its amplitude is scaled by a direction-dependent scalar so that
inhibition is strongest in null direction and weakest in preferred direction.

The sibling task t0053 implements a true spatial PD/ND-asymmetric variant.

## Objective

Build and run a minimal compartmental DSGC model with the following specification, then report
per-direction voltage and firing-rate data so the behaviour can be compared against the
project's target tuning curve and against t0053.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (the t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction).
* Compartments: as defined in the asset; standard NEURON section discretisation.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism (Na, K
  active conductances; leak built into the mechanism). Default densities from `hh.mod` unless
  explicit re-tuning is required to keep the cell silent at rest with V_rest = -65 mV.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1
  uF/cm^2` (matching t0024 baseline).
* V_rest: -65 mV.

### Synapses

* 100 excitatory (E) + 100 inhibitory (I) synapses, **co-located in pairs**.
* Placement: 100 dendritic locations sampled uniformly at random from the dendritic length (no
  distal bias; no exclusion of soma- or AIS-adjacent sections beyond the soma/AIS themselves).
  Each location hosts exactly one E + one I synapse.
* Random seed for placement: fixed (0) and reported in `results/results_detailed.md`.

### Excitatory mechanism (direction-independent, position-gated)

* `Exp2Syn` configured as a classical EPSP: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV.
* Peak conductance per synapse: 0.5 nS.
* Trigger: each E synapse fires **one event** when the moving bar's leading edge crosses the
  synapse's (x, y) position projected along the bar's normal direction.
* Direction-independent waveform: identical EPSC shape regardless of bar direction.

### Inhibitory mechanism (direction-dependent via scalar gabaMOD)

* `Exp2Syn` configured as classical IPSC: rise = 1 ms, decay = 20 ms, e = -75 mV.
* Peak conductance per synapse: 2 nS times `gabaMOD(theta)`.
* `gabaMOD(theta) = 0.33 + 0.66 * (1 - cos(theta - theta_ND)) / 2`, where `theta_ND` is the
  null direction of the cell. By convention, set `theta_PD = 0` (rightward), `theta_ND = 180`
  (leftward); `theta` is the bar direction.
* Trigger: each I synapse fires **one event** when the moving bar's leading edge crosses the
  synapse's (x, y) position; the event's amplitude is scaled by `gabaMOD(theta)`.

### Stimulus protocol

* 12 bar directions: 0, 30, 60, ..., 330 degrees.
* Bar dimensions: 200 um wide x full arena length.
* Bar speed: 1000 um/s.
* Trial duration: 1500 ms.
* Trials per direction: 10.
* Total trials: 120.

## Outputs

For each of the 12 directions, produce:

1. **Soma V(t)** — mean trace +/- SD across the 10 trials. PNG under `results/images/`,
   embedded in `results_detailed.md`.
2. **Aggregate EPSP at soma** — sum of EPSC-driven somatic depolarisation per trial, mean
   trace +/- SD across trials. (Computed by simulating the synapse population with only E
   active.)
3. **Aggregate IPSP at soma** — analogous, with only I active.
4. **Firing-rate PSTH** — 5 ms bins, mean across 10 trials.
5. **Polar tuning curve** — peak firing rate (Hz) vs direction; primary DSI; vector-sum DSI;
   preferred direction.
6. **Per-synapse activation-time histogram** (sanity check): for each direction, histogram of
   when each E synapse fires. Confirms position-gating logic is correct.

## Library Asset

Produce one library asset: `minimal_dsgc_scalar_gaba`. Contents:

* Cell builder (morphology load + section channel assignment + V_rest setup).
* Synapse placer (uniform random over dendrites, 100 co-located pairs, fixed seed).
* Excitation driver (position-gated AMPA event scheduler).
* Inhibition driver (position-gated GABA event scheduler with scalar gabaMOD scaling).
* Trial runner (12 directions x 10 trials, deterministic seeds).
* Recording helpers (soma V, EPSC/IPSC components, spike times).

Follow the project's library asset specification
(`meta/asset_types/library/specification.md`).

## Key Questions

1. With AMPA-only excitation, what peak firing rate does the cell produce in the preferred
   direction at default HH densities?
2. What is the primary DSI of this minimal model? Does it land in the project's target band
   (Park 2014 in vivo: 0.40 - 0.60)?
3. Does the position-gated firing pattern match expectations (E synapses on the leading edge
   of the bar fire first, trailing-edge last)?
4. How do EPSP and IPSP aggregate amplitudes scale with direction under scalar gabaMOD?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~1 week including library development and reporting.
Cost: $0.00.

## Out of Scope

* NMDA receptors (this is an AMPA-only minimal model by design).
* Active dendritic conductances.
* Synaptic noise (deterministic protocol; one event per synapse per trial).
* Network-level inputs (no SAC network; inhibition is a phenomenological scalar gating).
* Cross-comparison to t0053 (handled by a downstream task once both finish).

## Verification Criteria

* Library asset structure validates against `meta/asset_types/library/specification.md`.
* All 12 directions produce a per-direction PNG plot in `results/images/` and are embedded in
  `results_detailed.md`.
* `results/metrics.json` contains primary DSI, vector-sum DSI, preferred direction, peak Hz,
  null Hz at minimum.
* Sanity check: in the null direction, IPSP aggregate should be approximately 3x the
  preferred-direction IPSP aggregate (`gabaMOD(180)/gabaMOD(0) = 1.0/0.33`).

**Results summary:**

> **Results Summary: Minimal From-Scratch DSGC with Scalar gabaMOD Inhibition**
>
> **Summary**
>
> Built a from-scratch minimal DSGC on `dsgc-baseline-morphology-calibrated` with 100 E + 100
> I
> co-located synapses, position-gated AMPA-only excitation, and scalar `gabaMOD`-scaled
> inhibition;
> ran the full 12-direction × 10-trial × 3-mode sweep (360 trials in 19 min 13 s on local
> CPU). The
> cell produces **primary DSI = 1.0** in FULL mode (null direction silent, all preferred-side
> directions fire 0.667 Hz = 1 spike/trial), **vector-sum DSI = 0.746**, and preferred
> direction = 0°
> as designed. The IPSP conductance ratio `gabaMOD(180)/gabaMOD(0) = 3.0` matches the spec
> exactly;
> the observed somatic IPSP voltage ratio of 1.54 reflects driving-force saturation under
> realistic
> synaptic crowding and is the headline secondary finding.
>
> **Metrics**
>
> * **Primary DSI (FULL)**: **1.000** — perfect; null direction never spikes (all spikes occur
>   on
> the preferred half of the angle wheel, consistent with `gabaMOD(180) = 0.99` fully shunting
> null-direction firing).
> * **Vector-sum DSI (FULL)**: **0.746** — high but below the perfect-1.0 primary DSI because
> multiple preferred-side angles fire equally (the cell is broadly tuned at the chosen AMPA /
> GABA

</details>

## 2026-04-25 (5)

## ✅ Completed

<details>
<summary>✅ 0051 — <strong>Brainstorm results session 9</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0051_brainstorm_results_9` |
| **Status** | completed |
| **Effective date** | 2026-04-25 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md), [`t0040_brainstorm_results_8`](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md), [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md), [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md), [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-25T13:00:00Z |
| **End time** | 2026-04-25T15:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 9](../../../overview/tasks/task_pages/t0051_brainstorm_results_9.md) |
| **Task folder** | [`t0051_brainstorm_results_9/`](../../../tasks/t0051_brainstorm_results_9/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0051_brainstorm_results_9/results/results_detailed.md) |

# Brainstorm Session 9: From-Scratch Minimal DSGC Wave

Ninth brainstorming session. Run after the t0046–t0050 reproduction wave revealed that the
deposited Poleg-Polsky 2016 ModelDB 189347 code does not match the paper's Fig 3A-E claims
(282 vs 177 synapses; per-channel conductances 6-9x over paper; DSI vs gNMDA peaks at 0.19 not
the paper's flat 0.30; spatially-symmetric SAC inhibition mechanically incapable of producing
the paper's GABA PD/ND asymmetry).

## Strategic Pivot

The researcher decided to step away from modifying the deposited code and from the t0022
channel-testbed lineage, and instead build a new minimal DSGC model from scratch on the
project's calibrated baseline morphology. The new model uses 100 excitatory and 100 inhibitory
synapses, position-gated AMPA-only excitation with classical EPSP kinetics, deRosenroll-style
direction-dependent inhibition, and standard Hodgkin-Huxley spike generation on soma + AIS
only. Because there are two natural ways to implement "deRosenroll-style direction-dependent
inhibition" (scalar `gabaMOD` per synapse vs true spatial PD/ND asymmetry), the researcher
asked for both to be implemented in two parallel tasks.

## Decisions

* **Create t0052** — minimal DSGC with scalar `gabaMOD = 0.33 +
  0.66*(1-cos(theta-theta_ND))/2` per-synapse inhibition.
* **Create t0053** — minimal DSGC with spatial PD/ND-asymmetric inhibition; each I synapse
  fires only when `cos(theta_stim - theta_centrifugal_synapse) < 0` (centripetal-only firing).
* **Cancel t0042, t0043, t0044** — all `intervention_blocked` on the t0022 testbed; the
  reproduction wave reframes that substrate as non-canonical and the new minimal model
  supersedes their motivation.
* **Reprioritise six t0046–t0050 follow-up suggestions** from high to medium (S-0046-01,
  S-0046-03, S-0048-02, S-0049-02, S-0050-01, S-0050-02) — all become non-urgent now that the
  from-scratch model is the primary substrate.
* **Keep deferred** t0023, t0031, t0045 — none on critical path.

## Assets Produced

No assets in this brainstorm task. The two new tasks (t0052, t0053) will each produce a
library asset and an experiment-results bundle when executed.

**Results summary:**

> **Results Summary: Brainstorm Session 9**
>
> **Summary**
>
> Ninth strategic brainstorm, run on 2026-04-25 after the t0046–t0050 reproduction wave.
> Produced a
> strategic pivot: step away from modifying the deposited Poleg-Polsky 2016 ModelDB 189347
> code and
> from the t0022 channel-testbed lineage; build a from-scratch minimal DSGC on the project's
> calibrated baseline morphology with two parallel inhibition mechanisms (scalar `gabaMOD` and
> spatial
> PD/ND-asymmetric); cancel three obsolete `intervention_blocked` tasks; reprioritise six
> follow-up
> suggestions whose urgency the new substrate dissolves.
>
> **Session Overview**
>
> Date: 2026-04-25. Triggered by the researcher reading the t0046–t0050 reproduction wave
> findings
> (deposited code mismatches paper Fig 3A-E in synapse count, conductances, and mechanism;
> spatial
> GABA asymmetry mechanically impossible in the deposited synapse layout). The session opened
> with an
> independent priority reassessment of the 49 high-priority active suggestions, focusing on
> those
> superseded by the new substrate. The researcher specified the new model design directly
> during Round
> 1 (100 E + 100 I co-located synapses, position-gated AMPA-only EPSPs, classical IPSPs,
> soma+AIS HH
> on `dsgc-baseline-morphology-calibrated`) and asked for the deRosenroll-style direction-
> dependent

</details>

<details>
<summary>✅ 0050 — <strong>Audit deposited GABA/NMDA/AMPA synapse spatial
distribution vs paper</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0050_audit_syn_distribution` |
| **Status** | completed |
| **Effective date** | 2026-04-25 |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0049-01` |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-04-25T11:15:53Z |
| **End time** | 2026-04-25T12:11:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Audit deposited GABA/NMDA/AMPA synapse spatial distribution vs paper](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md) |
| **Task folder** | [`t0050_audit_syn_distribution/`](../../../tasks/t0050_audit_syn_distribution/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0050_audit_syn_distribution/results/results_detailed.md) |

# Audit Deposited GABA/NMDA/AMPA Synapse Spatial Distribution vs Poleg-Polsky 2016 Text

## Motivation

Task t0049 measured per-channel synaptic conductance under a somatic SEClamp on the deposited
DSGC (gNMDA = 0.5 nS, exptype = control) and found that the GABA PD/ND symmetry collapses
entirely (PD = 47.47 nS, ND = 48.04 nS, DSI ≈ -0.006), contradicting Poleg-Polsky 2016's
stated PD ~12.5 / ND ~30 nS (DSI ≈ -0.41). The compare_literature analysis identified three
candidate mechanisms for this discrepancy:

1. **Spatial-distribution hypothesis**: deposited GABA synapses are distributed roughly
   equally across PD-side and ND-side dendrites, so the somatic measurement sees no asymmetry.
   The paper's actual GABA distribution may put more synapses on ND-side dendrites.
2. **Cable-filtering hypothesis**: deposited cable filtering averages out local asymmetry by
   the time the current reaches the soma; paper's morphology may preserve the asymmetry
   better.
3. **Modality-of-paper-measurement hypothesis**: paper's PD ~12.5 / ND ~30 nS may reflect a
   sublocal dendritic measurement, not a true somatic SEClamp.

Hypothesis (1) is the most directly testable from the deposited code alone — by extracting the
(x, y, z) coordinates of every BIP (NMDA + AMPA), SACexc, and SACinhib synapse instance and
computing per-direction spatial densities. If the deposited distribution is symmetric, the
spatial-distribution hypothesis is supported and the deposited code is missing the paper's
PD/ND asymmetry by construction. If the deposited distribution is asymmetric, the hypothesis
is rejected and (2) or (3) becomes more likely.

This task does not modify the model — it is a measurement and audit of what is already in the
deposited code, plus a side-by-side comparison with the paper's text.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or
  fork.
* Build the cell once via `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell.
  build_dsgc()`, then call `placeBIP()` (control condition, gNMDA = 0.5 nS, exptype = 1).
  Extract for every synapse the (x, y, z) center coordinate of its parent section, plus the
  section name and section length.
* Compute per-channel-class spatial statistics:
  * **Per-channel synapse counts**: total, PD-side, ND-side. (Reproduce/confirm the 282 count
    from t0046's audit.)
  * **Per-channel x-position histograms**: PD-side dendrites are at one extreme of the x-axis
    (or whichever axis the deposited code uses for the wave-stimulus direction); ND- side at
    the other. The `placeBIP()` `gabaMOD` swap protocol uses x-position to determine PD vs ND.
    Compute the bimodal histogram per channel.
  * **Per-channel mean radial distance from soma**: distance in 3D from soma center to each
    synapse, summarized as mean ± SD. Also broken down by PD-side vs ND-side.
  * **Per-channel mean dendritic-tree distance from soma** (path length along the cable):
    using `h.distance(0, sec(0.5))` from the soma. Mean ± SD per channel × side.
  * **PD-side vs ND-side density**: number of synapses per unit dendritic length on each side,
    per channel.
* Compare these statistics against the paper's text descriptions:
  * Paper text states 177 BIP synapses; deposited code has 282 (already catalogued as
    discrepancy entry 4 in t0046's audit).
  * Paper text describes the spatial distribution of GABA synapses (likely SAC-derived,
    asymmetric across PD/ND).
  * Paper text describes the AMPA + NMDA distribution (BIP synapses, likely symmetric).
* Identify the synapse-distribution discrepancies that explain the t0049 GABA symmetry
  collapse.

### Out of Scope

* Any modification to the model (synapse positions, counts, or kinetics). This task is audit
  and measurement only.
* Re-running the SEClamp protocol (already done in t0049).
* Higher-N reruns or new sweeps (covered by S-0046-01 / S-0048-04).
* Reading the supplementary PDF for paper protocol details (covered by S-0046-05; if the PDF
  is fetched manually before this task starts, use it; otherwise rely on paper main text and
  t0046's research_papers.md notes).
* Implementing iMK801 or any other model modification.

## Reproduction Targets

There are no quantitative reproduction targets per se; this task produces measurements that
the paper does not state numerically. The audit compares the extracted spatial statistics
against the paper's qualitative claims:

| Paper claim | Expected if H1 (spatial-distribution discrepancy) |
| --- | --- |
| GABA stronger on ND side | Deposited GABA density should NOT be ND-biased |
| BIP (AMPA+NMDA) symmetric | Deposited BIP density should be symmetric |
| 177 BIP synapses | Deposited has 282 (already known) |

If H1 is supported, the deposited GABA spatial distribution is symmetric across PD/ND, with
PD-side count ≈ ND-side count. The paper's GABA ND-bias is then inherent to the ND-side
distribution itself, and the deposited code's `gabaMOD` swap protocol cannot reproduce it
because it scales gain symmetrically without changing positions.

## Approach

The implementation extracts synapse coordinates via:

1. Build cell via
   `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell.build_dsgc()`.
2. Call `simplerun(exptype=1, direction=0)` to populate `placeBIP()` with the control
   conditions.
3. Iterate over `h.RGC.BIPsyn[i]`, `h.RGC.SACexcsyn[i]`, `h.RGC.SACinhibsyn[i]` for `i in
   range(int(h.RGC.numsyn))`. For each synapse, extract:
   * Parent section name (via `syn.get_segment().sec.name()`).
   * Center segment (x, y, z) via `h.x3d`, `h.y3d`, `h.z3d` on the parent section's center.
   * Section path-distance from soma via `h.distance(0, syn.get_segment())` (after setting
     `h.distance(0, h.RGC.soma(0.5))` as the origin).
   * Section length via `sec.L`.
4. Build a per-synapse DataFrame and compute per-channel spatial statistics.

The deposited `placeBIP()` (per t0049's research_code.md) uses the x-coordinate of the synapse
to determine PD vs ND-side: synapses with x > 0 are on one side, x < 0 on the other. Confirm
this convention by inspecting `placeBIP()` source code in `main.hoc` / `dsgc_model_exact.hoc`.

For each channel class, compute:

* `count_pd = number of synapses with x > 0`
* `count_nd = number of synapses with x < 0`
* `pd_nd_count_ratio = count_pd / count_nd`
* `mean_radial_distance_pd_um = mean(sqrt(x^2 + y^2 + z^2)) for x > 0`
* `mean_radial_distance_nd_um = mean(sqrt(x^2 + y^2 + z^2)) for x < 0`
* `mean_path_distance_pd_um = mean(h.distance(0, syn) for x > 0)`
* `mean_path_distance_nd_um = mean(h.distance(0, syn) for x < 0)`
* `density_pd = count_pd / total_pd_dendritic_length_um`
* `density_nd = count_nd / total_nd_dendritic_length_um`

Plot per-channel x-coordinate histograms (PD vs ND overlay) and per-channel radial-distance
histograms.

## Pass Criterion

* Per-channel synapse counts confirmed (BIP = SACexc = SACinhib = 282 expected from t0046).
* Per-channel PD-side vs ND-side count ratio reported numerically with verdict (symmetric if
  ratio in [0.9, 1.1]; asymmetric otherwise).
* H1 (spatial-distribution hypothesis) verdict: SUPPORTED, REJECTED, or PARTIAL with numerical
  evidence. SUPPORTED if GABA is symmetric (count_pd / count_nd in [0.9, 1.1]) AND paper
  claims ND-bias. REJECTED if GABA shows ND-bias matching paper claim. PARTIAL if weakly
  asymmetric.
* Spatial-distribution discrepancy catalogue updated: any per-channel × per-side asymmetry or
  symmetry that differs from paper text is logged.

## Deliverables

### Answer asset (1)

`assets/answer/synapse-distribution-audit-deposited-vs-paper/` per
`meta/asset_types/answer/specification.md` v2 with `details.json`, `short_answer.md`,
`full_answer.md`. The `full_answer.md` must contain:

* Question framing: "Does the deposited DSGC's spatial distribution of NMDA/AMPA/GABA synapses
  match Poleg-Polsky 2016's text descriptions, and does it explain the t0049 GABA PD/ND
  symmetry collapse under SEClamp?"
* Per-channel synapse-count and spatial-statistics table (counts, PD/ND ratio, mean radial
  distance, mean path distance, density per side).
* Per-channel x-coordinate histogram with PD/ND-side annotation.
* H1 verdict (spatial-distribution hypothesis) with numerical evidence.
* Synthesis paragraph: which of the three t0049-flagged candidate mechanisms is supported by
  the spatial audit; what the next test should be.

### Per-figure PNGs (under `results/images/`)

* `syn_x_hist_per_channel.png` — three subplots (NMDA, AMPA, GABA), each an x-coordinate
  histogram with a PD/ND median line.
* `syn_radial_distance_per_channel.png` — three subplots, radial-distance histograms PD vs ND
  overlay.
* `syn_count_pd_vs_nd_per_channel.png` — bar chart, 3 channels × 2 sides, per-channel PD vs ND
  counts side-by-side.

## Execution Guidance

* **Task type**: `data-analysis`. Optional steps to include: research-code (review t0046's
  `placeBIP()` to identify x-coordinate convention and `read_synapse_coords()` pattern),
  planning, implementation, results, suggestions, reporting. Skip research-papers /
  research-internet (paper text already covered by t0046's research_papers.md), skip
  compare-literature (this task IS the literature comparison; compare-literature would
  duplicate it). Skip creative-thinking.
* **Local CPU only**. No Vast.ai. The task requires a single NEURON cell build + one simplerun
  call to populate placeBIP coordinates; ~1 minute wall-clock for the measurement phase. Total
  task estimate: 1-2 hours including coding + analysis + answer asset writing.
* Use absolute imports per the project's Python style guide.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **x-coordinate axis convention**: confirmed in t0049's research that `placeBIP()` uses
  x-position to determine PD vs ND. If the convention is actually y-coordinate or some other
  axis, the audit must use the correct axis. Mitigation: read `placeBIP()` source carefully
  before writing the analysis script.
* **Path-distance computation**: `h.distance()` in NEURON requires setting an origin first via
  `h.distance(0, soma(0.5))`. Forgetting to set the origin gives wrong distances. Mitigation:
  explicit assertion in the wrapper that `h.distance(0, ...)` was called before measuring
  synapse distances.
* **Section name parsing**: synapse positions returned via `syn.get_segment().sec.name()` may
  include the template prefix (e.g., `RGC[0].dend[5]`). Strip the prefix consistently.
* **Paper text descriptions may be vague**: the paper may not state the spatial distribution
  numerically. The audit will then compare deposited values against the qualitative claims
  only. Mitigation: also report what the paper does NOT state, so future tasks know what to
  fetch from the supplementary.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0046 (library asset + `read_synapse_coords()` pattern),
  t0049 (provides the SEClamp evidence that motivates this audit).
* **Source suggestion**: S-0049-01 (HIGH priority evaluation).
* **Complements**: t0049's compare_literature analysis. This task is the direct test of
  hypothesis (1) (spatial-distribution discrepancy).
* **Precedes**: any future synapse-redistribution modification task (would adjust the
  deposited code's `placeBIP()` to better match paper text, after this audit identifies the
  exact discrepancies).

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection) passes for the answer asset.
* Per-channel synapse-count table is populated for NMDA / AMPA / GABA × PD-side / ND-side.
* Per-channel x-coordinate histograms exist as PNGs and are embedded in `results_detailed.md`.
* H1 verdict (SUPPORTED / REJECTED / PARTIAL) is stated with numerical evidence.
* `metrics.json` is `{}` (this task does not measure registered metrics; spatial counts and
  ratios are task-specific operational data, reported in `results_detailed.md` and
  `full_answer.md`).

**Results summary:**

> **Results Summary: Synapse-Distribution Audit (Deposited DSGC vs Paper)**
>
> **Summary**
>
> Confirms t0049's spatial-distribution hypothesis (H1) at both the structural and numerical
> levels:
> the deposited ModelDB 189347 PD/ND condition swap is implemented as a pure scalar
> `gabaMOD = 0.33 + 0.66*direction` applied uniformly to ALL 282 SAC inhibitory synapses with
> NO
> spatial threshold. The underlying synapse spatial distribution is symmetric around the
> synapse
> population's own median (count_pd / count_nd = 139 / 143 = 0.972, within the [0.9, 1.1]
> symmetric
> band). The deposited code therefore cannot produce the paper's somatic GABA PD/ND asymmetry
> — the
> t0049 SEClamp symmetry collapse (PD = 47.47, ND = 48.04 nS) is the direct mechanical
> consequence of
> (1) a non-spatial gabaMOD protocol and (2) a spatially-symmetric underlying SAC inhibitory
> synapse
> distribution.
>
> **Metrics**
>
> * **Per-channel synapse counts**: BIPsyn = SACexcsyn = SACinhibsyn = **282** synapses each.
>   All
> three channels share identical parent sections per index (asserted in the extraction
> wrapper).
> * **Side-a vs side-b at synapse-population median midline (x = 88.77 µm)**: **139 / 143**
>   (ratio
> **0.972**, symmetric per [0.9, 1.1] threshold).

</details>

<details>
<summary>✅ 0049 — <strong>Re-measure Fig 3A-E conductances under somatic SEClamp
on the deposited DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0049_seclamp_cond_remeasure` |
| **Status** | completed |
| **Effective date** | 2026-04-25 |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0047-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-25T09:35:35Z |
| **End time** | 2026-04-25T10:42:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Re-measure Fig 3A-E conductances under somatic SEClamp on the deposited DSGC](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Task folder** | [`t0049_seclamp_cond_remeasure/`](../../../tasks/t0049_seclamp_cond_remeasure/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0049_seclamp_cond_remeasure/results/results_detailed.md) |

# Re-measure Fig 3A-E Conductances Under Somatic SEClamp on the Deposited DSGC

## Motivation

Task t0047 recorded per-synapse direct conductances (`syn._ref_g`) on the deposited DSGC and
found summed-across-282-synapses peak conductances 6-9x over the paper's Fig 3A-E stated
values (NMDA PD 69.55 nS vs paper ~7.0 nS; AMPA PD 10.92 nS vs paper ~3.5 nS; GABA ND 215.57
nS vs paper ~30.0 nS), and 28-90x under on the per-synapse-mean scale. Neither the summed nor
the per-synapse-mean interpretation reconciles with the paper's numbers.

The compare_literature analysis identified the most likely source: the paper's Fig 3A-E most
likely reports a **somatic voltage-clamp**-recorded conductance (the integrated synaptic
current seen at the soma after cable propagation), which is a third quantity that t0047 did
not measure. Per-synapse direct conductance vs somatic-voltage-clamp conductance differ
because of cable attenuation and synaptic location heterogeneity along the dendrite.

This task adds a NEURON SEClamp at the soma of the deposited DSGC, voltage-clamps it at -65
mV, and records the total synaptic current per channel as the wave stimulus sweeps. The
current divided by the driving force `(V_clamp - E_rev)` gives the
somatic-voltage-clamp-equivalent conductance per channel. This is the apples-to-apples
comparison with the paper's Fig 3A-E.

## Hypothesis

If the t0047 amplitude mismatch is purely a measurement-modality artefact, the SEClamp
re-measurement should land much closer to the paper's stated values (within +/- 25% or so) on
absolute amplitudes. If even the SEClamp values are still 5-10x over the paper, the deposited
synaptic conductances themselves are higher than the paper's text describes — a real
parameter-vs-paper discrepancy beyond just modality.

* **H1**: SEClamp NMDA / AMPA / GABA conductances at gNMDA = 0.5 nS land within +/- 25% of the
  paper's Fig 3A-E values (~7 / ~5 nS NMDA, ~3.5 / ~3.5 nS AMPA, ~12.5 / ~30 nS GABA). The
  amplitude mismatch was modality, not parameters.
* **H2**: SEClamp values are closer to paper than t0047's per-synapse-summed values, but still
  outside +/- 25%. Modality is part of the explanation but not all.
* **H0**: SEClamp values are essentially the same as t0047's per-synapse-summed values
  (modality irrelevant). The amplitude mismatch is real and parameter-driven.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or
  fork.
* Re-use t0046's `code/run_simplerun.py` `run_one_trial` for the wave stimulus dispatch.
* Add a new wrapper `code/run_seclamp.py` that:
  1. Builds the cell and places synapses (same as t0046's protocol).
  2. Inserts a NEURON `SEClamp` at the soma center segment with `dur1 = tstop`, `amp1 = -65
     mV`, `rs = 0.001 MOhm` (strong clamp).
  3. Records the SEClamp's total current `i_clamp` via `_ref_i` (sub-sampled at dt = 0.25 ms).
  4. To separate per-channel currents under the clamp, runs **four separate trials per
     direction**: full circuit (all synapses on), AMPA-only (NMDA gNMDA=0, GABA blocked via
     `gabaMOD = 0`), NMDA-only (AMPA blocked via `b2gampa = 0`), GABA-only (NMDA gNMDA=0, AMPA
     blocked).
  5. The SEClamp current per channel = sum across trials with that channel left on minus
     baseline.
* Compute somatic-equivalent conductance per channel as `g_soma_eq = mean_peak_i_channel /
  (V_clamp - E_rev)`. With `V_clamp = -65 mV` and `E_rev_NMDA = E_rev_AMPA = 0 mV` and
  `E_rev_GABA = -60 mV`, the driving forces are -65 mV, -65 mV, and -5 mV respectively.
* Run at the single condition gNMDA = 0.5 nS, exptype = 1 (control), 4 trials per direction
  per channel-isolation. That is 2 directions × 4 channel-isolations × 4 trials = 32 trials.
* Compare per-channel SEClamp conductance to t0047's per-synapse-summed conductance and to
  paper Fig 3A-E targets. Verdict on H0 / H1 / H2.

### Out of Scope

* Sweep across multiple gNMDA values (gNMDA = 0.5 only, the code-pinned value).
* Voff_bipNMDA = 1 condition (separate task t0048, S-0047-01).
* Higher-N rerun (separate task, S-0046-01).
* Modifying the deposited synapse parameters even if SEClamp shows them too large (this task
  is measurement, not modification).

## Approach

The implementation re-uses t0046's library entirely:

1. Cross-task import: `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun
   import run_one_trial`.
2. The new wrapper `code/run_seclamp.py` extends `run_one_trial` semantics to additionally
   insert a SEClamp at the soma and record `_ref_i` from the SEClamp object. The clamp is
   inserted AFTER `placeBIP()` so it does not interfere with synapse placement.
3. Channel isolation via four trial types: (a) full circuit; (b) AMPA-only via overriding
   `b2gnmda = 0` and `gabaMOD = 0`; (c) NMDA-only via overriding `b2gampa = 0` and `gabaMOD =
   0`; (d) GABA-only via overriding `b2gnmda = 0` and `b2gampa = 0`. Subtract baseline
   (no-input pre-stimulus window) from each peak to get net per-channel current.
4. Conversion `i_peak_pA` → `g_soma_eq_nS = i_peak_pA / (V_clamp - E_rev_mV)`. Sign
   convention: inward current at clamp = positive g.

### Driver design

* `code/run_seclamp.py` exposes `run_seclamp_trial(*, direction, trial_seed, channel_on)`
  where `channel_on in {"all", "ampa_only", "nmda_only", "gaba_only"}`. Returns a dataclass
  with the per-channel peak SEClamp current and the derived `g_soma_eq_nS`.
* `code/run_full_seclamp_sweep.py` orchestrates the 32-trial sweep (2 directions × 4
  isolations × 4 trials), writes per-trial CSV, and computes the per-channel comparison table.

## Pass Criterion

* Per-channel somatic-equivalent conductance is recorded for NMDA, AMPA, GABA at PD and ND, at
  gNMDA = 0.5 nS, with 4 trials per direction per isolation.
* Comparison table contains: t0047 per-synapse summed (nS), this task's SEClamp summed (nS),
  paper target (nS), verdict on H0/H1/H2 per channel × direction.
* Synthesis paragraph identifying which interpretation (modality vs parameters) is supported.

## Deliverables

### Answer asset (1)

`assets/answer/seclamp-conductance-remeasurement-fig3/` per
`meta/asset_types/answer/specification.md` v2 with `details.json`, `short_answer.md`,
`full_answer.md`. The `full_answer.md` must contain:

* Question framing: "Does measuring per-channel synaptic conductance under a somatic SEClamp
  on the deposited DSGC reproduce Poleg-Polsky 2016 Fig 3A-E values within tolerance, and
  resolve the t0047 amplitude mismatch as a measurement-modality artefact?"
* Per-channel comparison table (paper Fig 3A-E vs SEClamp this task vs per-synapse-summed
  t0047 vs per-synapse-mean t0047).
* H0 / H1 / H2 verdict per channel × direction.
* SEClamp methodology notes (clamp parameters, channel isolation protocol).
* Synthesis paragraph: whether the deposited synapse parameters match the paper's Fig 3A-E
  values once the measurement modality is corrected.

### Per-figure PNGs (under `results/images/`)

* `seclamp_conductance_pd_vs_nd.png` — bar chart, 3 channels × 2 directions, our SEClamp +
  paper target side-by-side.
* `seclamp_vs_per_syn_direct_modality_comparison.png` — bar chart comparing the two modalities
  at gNMDA = 0.5.

## Execution Guidance

* **Task type**: `experiment-run`. Optional steps to include: research-code (review t0046's
  `run_one_trial` and the soma section access pattern; review NEURON SEClamp docs), planning,
  implementation, results, compare-literature, suggestions, reporting. Skip research-papers /
  research-internet (paper and corpus already covered).
* **Local CPU only**. No Vast.ai. Total sweep is 32 trials. At ~5 sec/trial that is ~3 minutes
  wall-clock plus SEClamp insertion overhead. Total task wall-clock estimate: 1-2 hours
  including coding + planning + answer asset writing.
* Use absolute imports per the project's Python style guide.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **SEClamp may interfere with synaptic transmission** if the clamp is too strong or
  positioned suboptimally. Mitigation: use the standard NEURON SEClamp pattern with `rs =
  0.001` (effectively voltage source); confirm by inspecting the soma voltage trace during the
  trial — should stay locked at -65 mV throughout.
* **Channel isolation protocol may not cleanly separate per-channel currents** if there are
  cross-channel interactions (e.g., NMDA needs glutamate from AMPA release). Mitigation: the
  deposited bipolarNMDA.mod is a single dual-component synapse with separate `gAMPA` and
  `gNMDA` RANGE variables driven by the same presynaptic event, so AMPA-block via `b2gampa =
  0` and NMDA-block via `b2gnmda = 0` are independent. Verify this by reading the MOD source.
* **Voltage clamp at -65 mV may not match the paper's clamp potential**. Mitigation: paper's
  Methods may state the clamp potential explicitly; if so, use that value. -65 mV is a
  reasonable default matching `v_init` in the deposited code.
* **SEClamp current sign convention** may be confusing (NEURON inward current is positive when
  entering the clamp from the cell, negative when sourced by the clamp). Document the sign
  explicitly in the wrapper.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0046 (library asset), t0047 (per-synapse-direct
  baseline data for comparison).
* **Source suggestion**: S-0047-02 (HIGH priority experiment).
* **Complements**: t0047's per-synapse-direct measurement. This task is the modality-corrected
  re-measurement.
* **Precedes**: any future modification task that adjusts deposited synaptic conductances to
  match paper values (such a task needs the modality-corrected baseline this task produces to
  decide what "match paper" means).

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection against the v2 spec) passes for the answer
  asset.
* `verify_task_metrics.py` passes; `metrics.json` contains at least one variant per channel x
  direction (6 variants minimum).
* Per-channel SEClamp conductance is recorded for NMDA / AMPA / GABA at PD and ND with
  numerical evidence and SD.
* H0 / H1 / H2 verdict is stated per channel x direction with the numerical test that supports
  it.

**Results summary:**

> **Results Summary: SEClamp Conductance Re-Measurement**
>
> **Summary**
>
> Measuring per-channel conductance under a somatic SEClamp at -65 mV on the deposited DSGC
> (gNMDA =
> 0.5 nS, exptype = control) yields values that lie **between** paper Fig 3A-E targets and
> t0047's
> per-synapse-direct measurements — but match **neither** within tolerance. Verdict: **H2
> (intermediate)** for all 6 channel × direction cells. SEClamp is closer to paper than
> per-synapse-direct (5-10x reduction from t0047) but still 1.7-5x over paper. **Critically:
> GABA
> PD/ND symmetry under SEClamp** (PD = 47.47 nS, ND = 48.04 nS, DSI = -0.006) **contradicts
> the
> paper's stated PD ~12.5 / ND ~30 nS** (DSI ≈ -0.41). Modality alone does not reconcile the
> deposited code with paper Fig 3A-E.
>
> **Metrics**
>
> * **NMDA SEClamp at gNMDA = 0.5 nS**: PD **13.89 +/- 0.38 nS**, ND **13.71 +/- 0.19 nS**.
>   Paper: PD
> ~7.0, ND ~5.0. Delta: PD +98%, ND +174%. PD/ND ratio = **1.01** (paper expects ~1.4 with PD
> bias).
> * **AMPA SEClamp at gNMDA = 0.5 nS**: PD **5.93 +/- 0.27 nS**, ND **5.79 +/- 0.19 nS**.
>   Paper: PD
> ~3.5, ND ~3.5. Delta: PD +69%, ND +65%. PD/ND ratio = **1.02** (paper expects ~1.0,
> qualitative
> match for AMPA-no-DSI claim).

</details>

<details>
<summary>✅ 0048 — <strong>Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI
vs gNMDA flatness</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0048_voff_nmda1_dsi_test` |
| **Status** | completed |
| **Effective date** | 2026-04-25 |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0047-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-25T08:20:33Z |
| **End time** | 2026-04-25T09:32:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI vs gNMDA flatness](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Task folder** | [`t0048_voff_nmda1_dsi_test/`](../../../tasks/t0048_voff_nmda1_dsi_test/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0048_voff_nmda1_dsi_test/results/results_detailed.md) |

# Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI vs gNMDA Flatness

## Motivation

Task t0047 measured DSI as a function of `b2gnmda` across {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}
nS in the deposited ModelDB 189347 control condition (`exptype = 1`, `Voff_bipNMDA = 0`,
voltage-dependent NMDA with Mg block). DSI peaked at 0.19 (gNMDA = 0.5) and decayed
monotonically to 0.018 (gNMDA = 3.0) — not the paper's claimed flat ~0.30 across the range.
The compare_literature analysis identified the deposited control's voltage-dependent NMDA as
the most plausible mechanistic source of the collapse: at high gNMDA, the ND dendrite
depolarizes enough to relieve Mg block, ND NMDA opens, and the PD/ND distinction collapses.

The paper's biological finding (text statement in Poleg-Polsky and Diamond 2016) is that DSGC
NMDA is largely **voltage-independent** in vivo. The deposited code already provides a
voltage-independent NMDA setting via `exptype = 2` (`Voff_bipNMDA = 1`), used in the 0 Mg2+
condition. **This is not a model modification — it is a choice of which deposited exptype best
matches the paper's biological NMDA condition.**

This task runs the exact same gNMDA sweep as t0047, but at `exptype = 2` instead of `exptype =
1`, to directly test the hypothesis: does voltage-independent NMDA flatten the DSI-vs-gNMDA
curve to match the paper's flat ~0.30 claim?

## Hypothesis

If voltage-dependent NMDA is the cause of the DSI-vs-gNMDA collapse in the t0047 control, then
running the same sweep at `Voff_bipNMDA = 1` should produce a flat DSI-vs-gNMDA curve close to
the paper's ~0.30 target.

* **H0 (null)**: DSI vs gNMDA at `Voff_bipNMDA = 1` looks the same as t0047's `Voff_bipNMDA =
  0` curve (peaks then decays). NMDA voltage-dependence is NOT the cause; the divergence comes
  from somewhere else.
* **H1 (alternative)**: DSI vs gNMDA at `Voff_bipNMDA = 1` is flat across the range (within
  +/- 0.05 of some constant value). NMDA voltage-dependence WAS the cause; switching to the
  voltage-independent setting reproduces the paper's claim.
* **H2 (intermediate)**: DSI vs gNMDA at `Voff_bipNMDA = 1` is flatter than t0047's curve but
  still does not match the paper's ~0.30 line. Voltage-dependence is part of the problem but
  not the only contributor.

Each outcome is informative. The pass criterion is to record numerical evidence sufficient to
distinguish among the three.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or
  fork.
* Re-use t0047's `code/run_with_conductances.py` recorder pattern via cross-task package
  import (`from tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import
  ...`).
* Add a thin Python driver `code/run_voff1_sweep.py` that calls `run_one_trial(exptype=2,
  ...)` for the same `b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS grid, 4 trials per
  direction per value (matching t0047's protocol exactly).
* Record per-synapse NMDA / AMPA / GABA conductances for cross-comparison with t0047's
  `Voff_bipNMDA = 0` data.
* Compute DSI per gNMDA value via the same inlined `_dsi(*, pd_values, nd_values)` helper
  pattern from t0047.
* Plot DSI vs gNMDA for `Voff_bipNMDA = 1` overlaid on t0047's `Voff_bipNMDA = 0` curve plus
  the paper's flat ~0.30 line, on a single panel.
* Report per-direction PSP amplitudes at gNMDA = 0.5, 1.5, 2.5 nS to characterize how
  voltage-independence affects the absolute amplitudes.

### Out of Scope

* Any modification to the model beyond switching `Voff_bipNMDA` (the deposited exptype = 2
  already handles this). This is an exptype-choice test, not a code modification.
* SEClamp re-measurement of conductances (separate task t0049, S-0047-02).
* Higher-N (12-19 trials) re-run (separate task, S-0046-01).
* Re-running noise sweeps under `Voff_bipNMDA = 1` (out of scope — focus is the DSI-vs-gNMDA
  flatness test).
* Modifying the AP5 analogue (separate task, S-0046-03).

## Reproduction Targets

### Primary target: DSI vs gNMDA flatness

| gNMDA (nS) | t0047 control (Voff=0) | Voff=1 hypothesis | Paper target |
| --- | --- | --- | --- |
| 0.0 | 0.103 | ? (unknown) | ~0.30 |
| 0.5 | 0.192 | ? (test value) | ~0.30 |
| 1.0 | 0.114 | ? (test value) | ~0.30 |
| 1.5 | 0.042 | ? (test value) | ~0.30 |
| 2.0 | 0.032 | ? (test value) | ~0.30 |
| 2.5 | 0.022 | ? (test value) | ~0.30 |
| 3.0 | 0.018 | ? (test value) | ~0.30 |

H1 verdict: every Voff=1 DSI value within +/- 0.05 of a constant (target constant ~0.30 if it
matches the paper exactly; lower constant if it matches paper qualitatively). H2 verdict:
clearly flatter than t0047's curve but still trending downward. H0 verdict: same shape as
t0047.

### Secondary target: per-synapse conductance comparison

Compare summed-across-282-synapses peak conductance at gNMDA = 0.5 nS for `Voff = 1` vs `Voff
= 0` (from t0047's data). NMDA should be similar magnitude (the underlying gNMDA is the same),
but PD/ND ratio should change because Mg block is no longer suppressing ND.

## Approach

The implementation re-uses every piece of t0046 + t0047 infrastructure unchanged:

1. Cross-task import: `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun
   import run_one_trial` and `from
   tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import
   ConductanceRecorder` (or equivalent — the recorder API is documented in t0047's README).
2. Driver `code/run_voff1_sweep.py` calls the wrapper in a loop over the 7 gNMDA values × 2
   directions × 4 trials = 56 trials. Same trial seeds as t0047 for reproducibility.
3. Aggregator `code/compute_metrics.py` builds the multi-variant `metrics.json` (7 variants
   per gNMDA value, with `direction_selectivity_index` per variant). Format matches t0047's.
4. Renderer `code/render_figures.py` produces the overlay PNG: x-axis gNMDA, y-axis DSI, two
   curves (Voff=0 from t0047's data, Voff=1 from this task's data) plus a horizontal reference
   line at 0.30 (paper claim). Also produces a per-synapse conductance comparison bar chart
   (Voff=0 vs Voff=1 at gNMDA=0.5).

Cross-task data import: t0047's per-trial CSVs are in
`tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` and were
merged to main. Read them via aggregator-style filtering (or directly via `pandas.read_csv`
with the absolute task path) to compute the t0047 baseline DSI for the overlay.

## Pass Criterion

* DSI vs gNMDA at `Voff_bipNMDA = 1` is recorded numerically for all 7 grid points with 4
  trials per direction per cell.
* Verdict on H0 / H1 / H2 is stated with numerical evidence (per-grid-point DSI within +/-
  0.05 band test, slope-of-DSI-vs-gNMDA test).
* Per-synapse conductance comparison at gNMDA = 0.5 nS (Voff=0 from t0047 vs Voff=1 from this
  task) is reported in a table.

## Deliverables

### Answer asset (1)

`assets/answer/dsi-flatness-test-voltage-independent-nmda/` per
`meta/asset_types/answer/specification.md` v2 with `details.json`, `short_answer.md`,
`full_answer.md`. The `full_answer.md` must contain:

* Question framing: "Does setting `Voff_bipNMDA = 1` (voltage-independent NMDA) reproduce the
  paper's claim that DSI vs gNMDA is approximately constant ~0.30 across 0-3 nS?"
* DSI-vs-gNMDA table (Voff=0 from t0047 vs Voff=1 from this task vs paper).
* Hypothesis verdict (H0 / H1 / H2) with numerical evidence.
* Per-synapse conductance comparison table at gNMDA = 0.5.
* Synthesis paragraph explaining the mechanistic interpretation and what the result means for
  the deposited control choice.

### Per-figure PNGs (under `results/images/`)

* `dsi_vs_gnmda_voff0_vs_voff1.png` — overlay curve plot.
* `conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png` — bar chart.

## Execution Guidance

* **Task type**: `experiment-run`. Optional steps to include: research-code (review t0047's
  recorder API), planning, implementation, results, compare-literature (compare to paper's
  flat claim), suggestions, reporting. Skip research-papers / research-internet (paper and
  corpus already covered by t0046 + t0047).
* **Local CPU only**. No Vast.ai. Total sweep is 56 trials. At ~5 sec/trial that is ~5 minutes
  wall-clock. Total task wall-clock estimate: 1-2 hours including coding + planning + answer
  asset writing.
* Use absolute imports per the project's Python style guide.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **Voff_bipNMDA = 1 may produce unphysical results** at high gNMDA (the cell may saturate or
  spike inappropriately with TTX off). Mitigation: confirm `SpikesOn = 0` (TTX on) for the
  entire sweep and inspect the soma trace at the highest gNMDA value before fitting.
* **t0047 cross-task import may not work** if t0047's recorder API is not packaged at a stable
  module path. Mitigation: if direct import fails, copy the recorder code into this task's
  `code/` folder with attribution comments (the project's cross-task import rule allows
  copying for non-library code).
* **DSI may turn out to be constantly low** (e.g., flat at 0.05 instead of 0.30) under Voff =
  1, which would be H2 — flatter than Voff = 0 but not matching the paper's amplitude. This is
  still informative; record honestly.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0046 (library asset), t0047 (recorder pattern + Voff=0
  baseline data for the overlay).
* **Source suggestion**: S-0047-01 (HIGH priority experiment).
* **Complements**: t0047's compare_literature analysis. This task is the direct test of
  t0047's mechanistic hypothesis.
* **Precedes**: any future modification task that decides between exptype = 1 vs exptype = 2
  as the canonical "control" for the project's DSGC simulations.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection against the v2 spec) passes for the answer
  asset.
* `verify_task_metrics.py` passes; `metrics.json` contains 7 variants (one per gNMDA value).
* DSI vs gNMDA at `Voff = 1` is recorded for all 7 grid points with numerical evidence.
* H0 / H1 / H2 verdict is stated with the numerical test that supports it.

**Results summary:**

> **Results Summary: Voff_bipNMDA=1 DSI vs gNMDA Test**
>
> **Summary**
>
> Switching the deposited DSGC's NMDA model from voltage-dependent (`Voff_bipNMDA = 0`,
> exptype = 1)
> to voltage-independent (`Voff_bipNMDA = 1`, exptype = 2) flattens the DSI vs gNMDA curve
> substantially — verdict **H2 (intermediate)**: max-min DSI range drops from 0.174 to
> **0.066**
> (within H1's 0.10 cutoff), but the linear-fit slope is still **-0.024 per nS** (above H1's
> 0.02
> cutoff and below t0047's reference -0.058 per nS). The absolute DSI values stay between
> **0.04 and
> 0.10** — never reaching the paper's claimed flat ~0.30 line. Mechanism confirmed: NMDA PD/ND
> ratio
> collapses from 2.05 (Voff=0 Mg-block runaway) to 1.00 (Voff=1 symmetric) at gNMDA = 0.5 nS,
> exactly
> as predicted.
>
> **Metrics**
>
> * **DSI vs gNMDA at Voff=1**: 0.103 (gNMDA=0), **0.102** (gNMDA=0.5), 0.078 (gNMDA=1.0),
>   0.057
> (gNMDA=1.5), 0.053 (gNMDA=2.0), 0.044 (gNMDA=2.5), 0.037 (gNMDA=3.0).
> * **Range test**: max-min DSI = **0.066** vs H1 threshold 0.10 → **H1 passes** (curve is
>   flatter
> than 0.10 in absolute range).
> * **Slope test**: linear-fit slope = **-0.024 per nS** vs H1 threshold |slope| < 0.02 → **H1

</details>

<details>
<summary>✅ 0047 — <strong>Validate Poleg-Polsky 2016 Fig 3A-F conductances and
extend noise sweep</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0047_validate_pp16_fig3_cond_noise` |
| **Status** | completed |
| **Effective date** | 2026-04-25 |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-24T22:11:04Z |
| **End time** | 2026-04-25T00:00:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Validate Poleg-Polsky 2016 Fig 3A-F conductances and extend noise sweep](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Task folder** | [`t0047_validate_pp16_fig3_cond_noise/`](../../../tasks/t0047_validate_pp16_fig3_cond_noise/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0047_validate_pp16_fig3_cond_noise/results/results_detailed.md) |

# Validate Poleg-Polsky 2016 Fig 3A-F Conductances and Extend Noise Sweep

## Motivation

Task t0046 produced an exact reproduction of ModelDB 189347 (Poleg-Polsky and Diamond 2016)
and catalogued paper-vs-code discrepancies, but its figure-by-figure comparison conflated
experimental data (Figs 1-2, in vitro patch-clamp recordings) with simulation outputs (Fig 3
onward). The correct simulation-vs-simulation comparison was therefore incomplete. Two
specific gaps remain:

1. **Per-synapse conductances (Fig 3A-E) were never recorded.** t0046 captured soma membrane
   voltage only, so the paper's per-direction NMDA, AMPA, and GABA conductance targets could
   not be cross-checked. The audit could not say whether the model's synaptic conductance
   balance matches the paper.

2. **The noise sweep stopped at flickerVAR = 0.10.** Paper Figs 6-8 sweep luminance noise SD
   over {0.0, 0.1, 0.3, 0.5} across control / AP5 / 0 Mg conditions. t0046 ran only the first
   two levels for control + 0 Mg, omitting AP5 noise entirely and the high-noise tail for all
   conditions.

Without filling these gaps, the project cannot answer whether the deposited ModelDB code
reproduces the paper's primary simulation claims (Fig 3A-F per-synapse conductance balance,
Fig 3F constant DSI vs gNMDA, Figs 6-8 noise tolerance). Two preliminary findings from t0046
raise the stakes:

* DSI vs gNMDA is **not constant** in our reproduction (0.124 -> 0.204 -> 0.049 -> 0.026
  across gNMDA = 0.0, 0.5, 1.5, 2.5 nS). Paper Fig 3F bottom claims DSI is approximately
  constant (~0.3) across the entire range. If our per-synapse conductances also miss the
  paper's targets, the source of the divergence may lie in the synaptic balance rather than
  the active currents.

* The "control" exptype = 1 in `simplerun()` sets `Voff_bipNMDA = 0` (voltage-dependent NMDA
  with Mg block); the "0 Mg" exptype = 2 sets `Voff_bipNMDA = 1` (voltage-independent). The
  paper's biological finding is that DSGC NMDA is largely voltage-independent in vivo. Whether
  the deposited control was meant to model this is unclear from the code alone and may be the
  root of the DSI-vs-gNMDA divergence. This task does **not** modify the model — it only
  records what the deposited control actually does, providing the evidence base for any future
  modification.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or
  fork.
* Add a thin Python wrapper `code/run_with_conductances.py` that drives `simplerun()` and
  records:
  * Soma voltage (already recorded by t0046's `run_simplerun.py`).
  * Per-synapse-class summed conductance over the trial (NMDA, AMPA, GABA), peak in nS over
    the trial window, separately for PD vs ND.
  * Per-synapse-class summed current (i = g * (V - E_rev)), peak in nA, for diagnostic.
* Run the gNMDA sweep at `b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS, 4 trials per
  direction per value, recording all of the above. Reproduces Fig 3A-E (per-synapse balance)
  and Fig 3F bottom (DSI vs gNMDA).
* Reproduce Fig 3F top: simulated PSP traces PD vs ND at gNMDA = 0.0, 0.5, 2.5 nS. Plot the
  soma voltage traces (mV vs ms) and overlay paper figure where possible.
* Extend the noise sweep to `flickerVAR in {0.0, 0.1, 0.3, 0.5}` for `exptype in {control,
  AP5, 0Mg}`. AP5 is modelled as `b2gnmda = 0` per t0046's convention. 4 trials per direction
  per (condition, noise) cell.
* Compare every recorded conductance against the paper's Fig 3A-E values:
  * **NMDAR**: PD ~7 nS, ND ~5 nS (clear PD bias).
  * **AMPAR**: PD ~3.5 nS, ND ~3.5 nS (no DSI).
  * **GABA**: PD ~12-13 nS, ND ~30 nS (much stronger in ND).
* Catalogue any conductance-balance discrepancies and the simulated DSI-vs-gNMDA mismatch.

### Out of Scope

* Any modification to the model (channel conductances, Voff_bipNMDA, etc.). This is validation
  only. Future modification tasks (e.g., "what if control had Voff_bipNMDA = 1?") are
  separate.
* Re-running Figures 1-2 (those are experimental in vitro data — not valid simulation
  comparison targets).
* Full 8-direction sweep (PD/ND only is sufficient for these comparisons; the slope-angle
  reproduction was already done in t0046 and is preserved by this validation).
* Increasing trial count to the paper's 12-19 (separate task, S-0046-01).
* Re-running Fig 8 suprathreshold spike sweeps (already covered in t0046; the AP5 silencing
  finding stands).
* Root-causing the 282-vs-177 synapse-count discrepancy from t0046 (separate task, S-0046-02).
* Implementing an iMK801 analogue (separate task, S-0046-03).

## Reproduction Targets

### Fig 3A-E (per-synapse peak conductance, simulated)

| Channel | PD target (nS) | ND target (nS) | DSI target |
| --- | --- | --- | --- |
| NMDAR | ~7.0 | ~5.0 | ~0.17 (PD-biased) |
| AMPAR | ~3.5 | ~3.5 | ~0.0 (no DSI) |
| GABA | ~12-13 | ~30 | ~-0.40 (ND-biased) |

Tolerance: +/- 25% on each value (paper does not state SDs explicitly; this is a permissive
band for first-cut comparison).

### Fig 3F top (PSP traces, simulated)

PSP traces PD vs ND at gNMDA = 0.0, 0.5, 2.5 nS. Tolerance: PSP peak amplitude within +/- 20%
of t0046's previously recorded values (sanity check that the new wrapper has not changed
semantics).

### Fig 3F bottom (DSI vs gNMDA, simulated)

DSI approximately constant (~0.3) across `b2gnmda in [0, 3]` nS. Tolerance: every gNMDA
value's DSI within +/- 0.05 of 0.3, i.e. DSI in [0.25, 0.35].

### Figs 6-7 (subthreshold ROC AUC and DSI under noise, simulated)

Per-condition (control / AP5 / 0 Mg) per-noise-level (flickerVAR in {0.0, 0.1, 0.3, 0.5}):

* DSI declines monotonically as noise increases (qualitative).
* ROC AUC declines monotonically as noise increases (qualitative).

Paper does not state per-cell SDs; comparison is qualitative shape-of-curve plus headline
numbers (noise = 0 control AUC ~0.99 already validated by t0046; noise = 0.5 control AUC
should drop clearly below noise = 0.0).

## Approach

The implementation re-uses `modeldb_189347_dsgc_exact` from t0046 unchanged and imports its
driver code via the project's standard cross-task package path (`from
tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial` is fine
because the entire `code/` subtree is the implementation of the registered library).

The new wrapper `code/run_with_conductances.py` wraps `run_one_trial` and additionally:

1. After the cell is built and synapses are placed (inside `run_one_trial`), iterates over the
   sectioned synapse arrays (`bipampa`, `bipNMDA`, `SACinhib`) and attaches NEURON
   `Vector.record` handles to each synapse's `_ref_g`. Sums per-class across the synapse array
   at every dt.
2. Records per-class current via `i = g * (V - E_rev)` using the recorded conductance and the
   companion soma voltage trace (this avoids a second NEURON record vector).
3. After the trial finishes, returns a `TrialResultWithConductances` dataclass containing the
   t0046 `TrialResult` plus the per-class peak conductance (nS) and peak current (nA) over the
   trial.

The driver in `code/run_fig3_validation.py` then sweeps gNMDA and exptype as defined in the In
Scope section, writes per-trial CSVs to `results/data/`, and produces the comparison tables.

The driver in `code/run_noise_extension.py` sweeps `flickerVAR in {0.0, 0.1, 0.3, 0.5}` for
control / AP5 / 0Mg, computing PSPs, DSI, and ROC AUC per condition per noise level.

The validation report (answer asset `polegpolsky-2016-fig3-conductances-validation`)
integrates:

* The per-synapse conductance comparison table (Fig 3A-E targets vs ours).
* The PSP trace comparison (Fig 3F top, t0046 vs new wrapper sanity check).
* The DSI-vs-gNMDA curve (Fig 3F bottom, paper claim vs ours).
* The extended noise-sweep tables (DSI vs flickerVAR, AUC vs flickerVAR per condition).
* A discrepancy catalogue building on t0046's catalogue, focused on the synapse-balance gap.

## Pass Criterion

* Per-synapse conductance values for NMDA, AMPA, GABA (PD and ND) are recorded for every gNMDA
  value in the sweep and reported in the validation table.
* For each conductance channel, the comparison verdict (within +/- 25%, outside +/- 25%) is
  numerically substantiated.
* The DSI-vs-gNMDA curve is plotted and the divergence from the paper's flat ~0.3 line is
  either confirmed (catalogued as a discrepancy) or reproduced (catalogued as a
  sanity-restoring observation).
* The noise-sweep extension (flickerVAR in {0.3, 0.5}) is reported for control / AP5 / 0Mg
  with per-condition DSI and AUC.

## Deliverables

### Answer asset (1)

`assets/answer/polegpolsky-2016-fig3-conductances-validation/` per
`meta/asset_types/answer/specification.md` v2. The `full_answer.md` must contain:

* Question framing: "Does the deposited ModelDB 189347 code reproduce Poleg-Polsky 2016's Fig
  3A-F per-synapse conductance balance and DSI-vs-gNMDA flatness, and does the extended noise
  sweep match the paper's qualitative shape?"
* Per-synapse conductance table (NMDA, AMPA, GABA, PD vs ND, paper target vs ours, verdict).
* PSP-trace overlay table (Fig 3F top, gNMDA = 0.0, 0.5, 2.5 nS).
* DSI-vs-gNMDA table and chart (Fig 3F bottom).
* Noise-sweep tables: DSI vs flickerVAR per condition, AUC vs flickerVAR per condition.
* Updated discrepancy catalogue: build on t0046's 12 entries with any new entries from the
  per-synapse data.
* One-paragraph synthesis: whether the deposited control is faithful to the paper's primary
  simulation claims, and which discrepancies (if any) are the first targets for the next
  modification task.

### Per-figure reproduction PNGs (under `results/images/`)

* `fig3a_nmda_conductance_pd_vs_nd.png`
* `fig3b_ampa_conductance_pd_vs_nd.png`
* `fig3c_gaba_conductance_pd_vs_nd.png`
* `fig3f_top_psp_traces.png`
* `fig3f_bottom_dsi_vs_gnmda.png`
* `fig6_dsi_vs_noise_per_condition.png`
* `fig7_auc_vs_noise_per_condition.png`

## Execution Guidance

* **Task type**: `experiment-run`. Optional steps to include: research-code (review t0046's
  `run_simplerun.py` for the recording-vector pattern), planning, implementation, results,
  compare-literature (the noise-sweep targets are qualitative; conductance targets are
  numerical), suggestions, reporting. Skip research-papers and research-internet (the paper
  and ModelDB release are already in the corpus and were exhaustively reviewed in t0046).
* **Local CPU only**. No Vast.ai. The full sweep is approximately (2 directions x 4 trials) x
  (7 gNMDA values + 3 conditions x 4 noise levels) = approximately 152 trials. At ~5 seconds
  per trial that is approximately 13 minutes wall-clock plus I/O and per-trial `placeBIP()`
  overhead. Estimate total task wall-clock at 1-2 hours.
* Use absolute imports per the project's Python style guide: `from
  tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial`,
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import ...`.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **Per-synapse `_ref_g` may not be straightforwardly accessible** for the bipNMDA / SACinhib
  / SACexc MOD models if they expose conductance under a different name (e.g. `g_NMDA` vs
  `g`). Mitigation: inspect the MOD source files for each synapse class to find the correct
  `_ref_*` pointer; if no single-variable handle is available, sum component conductances
  (e.g. AMPA + NMDA for the dual-component synapse) at the recording stage.
* **NEURON Vector.record at every dt for hundreds of synapses** may exhaust memory on a long
  trial. Mitigation: record at a subsample interval (e.g. every 0.5 ms vs the simulation dt of
  0.025 ms) and confirm the peak is captured by the sub-sampled trace.
* **Paper Fig 3 conductance values may be per-synapse rather than summed** (the paper's
  plotting conventions are not crystal clear from the figure caption alone). Mitigation:
  report both per-synapse-mean and summed values in the validation table; cross-check against
  the supplementary PDF if it can be obtained (S-0046-05 manual fetch).
* **gNMDA = 3.0 nS may push the soma into AP territory** even with TTX off — making PSP peak
  unreliable. Mitigation: re-confirm `SpikesOn = 0` (TTX on) for the entire sweep and validate
  by inspecting the soma voltage trace at the highest gNMDA value before fitting any peak.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0011 (visualisation library), t0012 (DSI helper), t0046
  (the library asset and driver this task wraps).
* **Complements**: t0046's audit. This task fills the per-synapse and high-noise gaps that
  t0046 flagged but did not measure.
* **Precedes**:
  * Any modification task that tweaks the synaptic conductance balance (e.g., a downstream
    "increase GABA ND-bias to recover paper's flat DSI-vs-gNMDA" task) needs the
    per-synapse-conductance baseline this task produces.
  * S-0046-04 (decide fate of t0042/t0043/t0044) becomes more informed once the
    per-synapse-conductance gap is quantified.
  * Any future iMK801-analogue modification task (S-0046-03) inherits the noise-tail data this
    task produces for AP5.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection against the v2 spec) passes for
  `polegpolsky-2016-fig3-conductances-validation`.
* `verify_task_metrics.py` passes; `metrics.json` uses the explicit multi-variant format with
  one variant per (gNMDA value) and one variant per (condition, noise level) pair.
* Per-synapse conductance values for NMDA, AMPA, GABA, PD and ND are reported numerically for
  the full gNMDA sweep.
* Discrepancy catalogue is updated relative to t0046's 12 entries with any new entries from
  the conductance-balance comparison.

**Results summary:**

> **Results Summary: Validate Poleg-Polsky 2016 Fig 3A-F Conductances and Extend Noise Sweep**
>
> **Summary**
>
> The deposited ModelDB 189347 code does **not** reproduce Poleg-Polsky 2016's Fig 3A-F
> simulation
> targets: per-synapse-class conductances are 6-9x the paper's stated values on the summed
> scale (or
> 30-90x under on a per-synapse-mean scale, so neither interpretation reconciles), and the DSI
> vs
> gNMDA curve peaks at 0.19 and decays to 0.018 instead of staying flat near 0.30. The
> extended noise
> sweep does show DSI declining as flickerVAR rises (qualitative match for Figs 6-7), but the
> ROC AUC
> metric saturates at 1.0 in every cell because the implementation uses pre-stimulus baseline
> voltage
> as the negative class and PSP peaks dwarf baselines on this circuit.
>
> **Metrics**
>
> * **NMDA conductance at gNMDA = 0.5 nS** (summed across 282 synapses): PD **69.55 +/- 5.86
>   nS** vs
> paper **~7.0 nS** (9.9x over); ND **33.98 +/- 1.83 nS** vs paper **~5.0 nS** (6.8x over).
> * **AMPA conductance at gNMDA = 0.5 nS** (summed): PD **10.92 +/- 0.37 nS** vs paper **~3.5
>   nS**
> (3.1x over); ND **10.77 +/- 0.60 nS** vs paper **~3.5 nS** (3.1x over). AMPA shows
> essentially
> zero direction selectivity (PD/ND = 1.01) consistent with the paper's qualitative claim.
> * **GABA conductance at gNMDA = 0.5 nS** (summed): PD **106.13 +/- 5.77 nS** vs paper
>   **~12.5 nS**

</details>

## 2026-04-24 (9)

## ✅ Completed

<details>
<summary>✅ 0046 — <strong>Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347)
with audit</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0046_reproduce_poleg_polsky_2016_exact` |
| **Status** | completed |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Expected assets** | 1 library, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Start time** | 2026-04-24T13:02:27Z |
| **End time** | 2026-04-24T17:45:00Z |
| **Step progress** | 12/15 |
| **Task page** | [Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Task folder** | [`t0046_reproduce_poleg_polsky_2016_exact/`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/results_detailed.md) |

# Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Correction — 2026-04-24

The original version of this task_description.md (as merged in PR #44) framed the peak-rate
mismatch (~15 Hz in our ports vs "paper's 40-80 Hz range") as a Poleg-Polsky 2016 claim and
included a pass criterion of "firing rates within +/-10% of the paper's stated value". This
was wrong. **Poleg-Polsky & Diamond 2016 is primarily a subthreshold-PSP paper.** Its main
figures report PSP amplitudes (mV), direction-tuning slope angles (degrees), and subthreshold
ROC AUC. Only Figure 8 includes spikes, and even there the paper reports qualitative DSI
preservation / reduction and PD-failure rate — not specific peak Hz numbers. The 40-80 Hz
target traces back to t0004's project-internal tuning-curve envelope (sourced from Oesch 2005
rabbit recordings and Sivyer 2013), not to Poleg-Polsky 2016.

This revision corrects the pass criteria to target PSP amplitudes, slope angles, and ROC AUC
as the primary reproduction metrics, with Figure 8 suprathreshold checks as a secondary
qualitative pass. Spike-rate comparisons against t0004's envelope are explicitly out of scope
for this task.

## Motivation

The project has two prior ports of Poleg-Polsky & Diamond 2016 (ModelDB 189347): **t0008**
(initial port using a spatial-rotation proxy for the gabaMOD swap) and **t0020** (re-run with
the native gabaMOD parameter-swap protocol; DSI 0.784 ~ paper's median of ~0.80). Both focused
primarily on the tuning curve as measured through DSI and did not audit every parameter
against the paper, did not reproduce the other tests the paper runs, and did not publish a
systematic paper-vs-code discrepancy catalogue.

The brainstorm-8 audit (t0040) identified paper-vs-observation mismatches across every port
and sweep; some of those mismatches — particularly the peak-rate framing — conflated
Poleg-Polsky 2016 with other DSGC papers (Oesch 2005, Sivyer 2013) and therefore do not belong
to this task. This task steps back to establish the faithful reproduction of Poleg-Polsky 2016
on its own terms, using the paper's own figures and metrics as the target.

## Objective

Produce a fresh port of ModelDB 189347 that reproduces Poleg-Polsky 2016 exactly on the
metrics the paper actually reports — PSP amplitudes, direction-tuning slope angles, ROC AUC
under the noise conditions described in the paper, and qualitative Figure 8 suprathreshold
behaviour — using the paper's own protocols. Publish a line-by-line audit comparing **paper ·
ModelDB code · our reproduction** for every quantitative claim, and a discrepancy catalogue
for any place where the paper text and the ModelDB code disagree.

## Paper's Reported Metrics (target of reproduction)

Primary (subthreshold PSP, Figures 1-7):

* **Figure 1** — 8-direction PSPs. PD PSP **5.8 +/- 3.1 mV**, ND PSP **3.3 +/- 2.8 mV**,
  direction-tuning slope **62.5 +/- 14.2 degrees** (multiplicative scaling under
  voltage-dependent NMDAR). DSI preserved under AP5. n=19.
* **Figure 2** — iMK801 (2 mM) dialysis + bath AP5: AP5-after-iMK801 further reduces PD PSP by
  only **16 +/- 17%**. n=15.
* **Figure 3** — NEURON model: 282 presynaptic cells, homogeneous ON-dendrite synapses, tuned
  inhibition, paper-stated **gNMDA = 2.5 nS** (paper) vs **0.5 nS** (ModelDB code)
  **[discrepancy flagged]**. Alternative tuned-excitation scheme predicts additive scaling.
* **Figure 4** — High-Cl- internal (tuned-excitation analogue): slope **45.5 +/- 3.7 degrees**
  (additive). DS reverses PD in 15/20 cells. n=12.
* **Figure 5** — 0 Mg2+ (voltage-dependent NMDAR removed, Ohmic NMDAR analogue): slope **45.5
  +/- 5.3 degrees** (additive). DSI reduced but PD != ND. n=8.
* **Figure 6** — Noisy PSPs under bar + background luminance noise at SD **0 / 10 / 30 /
  50%**. DSI reduced by noise, strongest in 0 Mg2+. n=12.
* **Figure 7** — Subthreshold ROC / accuracy (noise-free): AUC **0.99 / 0.98 / 0.83** for
  control / AP5 / 0 Mg2+. Accuracy curve area larger in control.

Secondary (suprathreshold APs, Figure 8 only):

* **Figure 8** — DSI preserved under AP5 (qualitative); DSI reduced in 0 Mg2+ (qualitative);
  AP5 **raises PD-failure rate**; ROC AUC on spikes under noise. **The paper does not report
  specific peak Hz or aggregate firing-rate numbers for the model.**

Basic parameters (read from ModelDB source, audited vs paper prose where stated):

* V_rest, Ra, Rm, Cm, soma/dendrite channel gbar densities, synaptic kinetics, Jahr-Stevens
  parameters, stimulus timing. See `research/research_internet.md` for extracted ModelDB
  values.

## Scope

### In Scope

* Full from-scratch port of ModelDB 189347 into a new library asset (do NOT fork t0008, t0020,
  or t0022). Target location:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`.
* Download and attach the supplementary PDF (NIHMS766337; PMC4795984) to the existing
  `10.1016_j.neuron.2016.02.013` paper asset.
* Paper corpus review: Poleg-Polsky & Diamond 2016 (Neuron) PDF + supplementary.
* ModelDB 189347 release: every `.hoc`, `.mod`, `.py`, README, comment, and parameter file in
  the release. Cross-check the release version against the paper's cited version.
* **Reproduce every quantitative claim in Figures 1-8**, as enumerated in "Paper's Reported
  Metrics" above.
* Basic parameters audited against paper + code + supplementary.

### Out of Scope

* **Comparisons against t0004's target tuning-curve envelope** (peak Hz 40-80, null Hz <10,
  HWHM 60-90). Those targets come from Oesch 2005 / Sivyer 2013 / Chen 2009 and do not belong
  in a Poleg-Polsky 2016 reproduction task.
* Modifications or improvements beyond the original paper.
* Integration with t0022, t0024, or other downstream modified testbeds.
* Any DSGC models other than Poleg-Polsky 2016.

## Source of Truth

Audit uses all three sources:

1. **Published PDF** — Poleg-Polsky & Diamond 2016, Neuron.
2. **ModelDB 189347 release** — README, `.hoc`, `.mod`, `.py`, parameter files, and all code
   comments. Canonical commit `87d669dcef18e9966e29c88520ede78bc16d36ff` (2019-05-31).
3. **Supplementary materials** — NIHMS766337 (PMC4795984), bundled Supplemental Experimental
   Procedures plus supplementary figures S1-S8. Download during implementation and attach to
   the existing paper asset.

## Paper-vs-Code Discrepancy Handling

The primary reproduction **follows their code** (what they actually ran). If the code fails to
reproduce a specific paper claim within tolerance, flag the discrepancy explicitly with the
paper claim, the code's actual behaviour, and the numerical gap. Known pre-implementation
flags from the research stages:

* **gNMDA discrepancy**: paper Fig 3E states 2.5 nS, ModelDB code uses 0.5 nS.
* **Synapse count discrepancy**: paper states 177 synapses, ModelDB code instantiates 282.
* **Noise driver missing**: shipped `SquareInput.mod` has no luminance-noise driver despite
  Figures 6-8 describing per-50-ms noise SD = 0 / 10 / 30 / 50%. Figures 6-8 cannot be
  reproduced from stock code without adding a noise driver; this must itself be flagged as a
  significant paper-vs-code discrepancy (the Figures 6-8 results in the paper must have come
  from a different code variant).
* **Dendritic Nav**: 2e-4 S/cm2 (small but non-zero), not strictly zero — refines the "passive
  dendrites" wording.

## Pass Criterion

Primary pass criteria (Figures 1-7 subthreshold):

* PD PSP amplitude within **1 SD** of the paper's reported mean (within 3.1 mV of 5.8 mV for
  Fig 1 control).
* ND PSP amplitude within **1 SD** (within 2.8 mV of 3.3 mV).
* Slope angle within **1 SD** (within 14.2 degrees of 62.5 degrees for Fig 1; within 3.7-5.3
  degrees for Figs 4-5 additive regime).
* Under 0 Mg2+: DSI reduced but not zero; preferred direction preserved (paper claim).
* Under High-Cl-: DS reverses PD in >= 50% of trials (paper's 15/20 is 75%; allow
  flexibility).
* Subthreshold noise-free ROC AUC within **+/- 0.05** of each paper value (0.99 / 0.98 / 0.83
  for control / AP5 / 0 Mg2+).

Secondary pass criteria (Figure 8 suprathreshold):

* DSI qualitatively preserved under AP5 (both conditions direction-selective).
* DSI qualitatively reduced in 0 Mg2+.
* PD-failure rate increases under AP5 (direction: positive, magnitude not specified by paper).
* No numeric peak-Hz target is asserted; the paper does not state one.

Parameter-match criterion:

* Every basic parameter in the audit table matches ModelDB code exactly; any deviation is
  documented as a reproduction bug, not an intentional modification.

Discrepancy-catalogue criterion:

* Every paper-vs-code discrepancy is catalogued with numerical evidence, including the four
  pre-flagged above (gNMDA, synapse count, missing noise driver, dendritic Nav wording) and
  any further discrepancies found during implementation.

## Deliverables

### Library asset (1)

`assets/library/modeldb_189347_dsgc_exact/`:

* Full NEURON port runnable under the project's NEURON 8.2.7 + NetPyNE 1.1.1 toolchain (from
  t0007).
* Uses the baseline DSGC morphology from t0005 (or the ModelDB-shipped morphology if that is
  what the paper actually used — audit this; if they differ, this is a discrepancy to flag).
* Source files mirror the ModelDB release structure where practical, with a clear mapping from
  each ModelDB file to the corresponding file in this library.
* Per-file comments identifying the ModelDB source file and line ranges that the port
  transcribes.
* Adds a luminance-noise driver that reproduces the Figure 6-8 noise protocol (the shipped
  ModelDB code lacks one); this addition must itself be flagged as a paper-vs-code
  discrepancy.
* Meets the library-asset specification in `meta/asset_types/library/specification.md`.

### Answer asset (1)

`assets/answer/poleg-polsky-2016-reproduction-audit/` with a full audit report.

The `full_answer.md` must include:

* **Audit table** — one row per basic parameter. Columns: **Parameter**, **Paper value** (when
  stated), **ModelDB code value**, **Our reproduction value**, **Match?**, **Citation**.
* **Figure-reproduction table** — one row per figure (1-8) with the paper's reported metric,
  our reproduction metric, tolerance, match verdict, and paper figure reference. Separate rows
  for PD/ND PSP, slope, ROC AUC, etc. as applicable.
* **Discrepancy catalogue** — one entry per paper-vs-code disagreement with numerical
  evidence.
* **Reproduction bugs** — any place where our port diverges from ModelDB code; each must be
  fixed before the library asset is considered complete.
* One-paragraph summary of what this reproduction establishes for the broader project.
  Specifically: whether Poleg-Polsky's PSP + slope + ROC claims hold under a faithful
  reimplementation, and a note on whether Figure 8 suprathreshold behaviour depends on details
  that the published code does not specify.

### Per-paper figure reproductions (under `results/images/`)

Each paper figure that reports a test this task reproduces gets its own PNG comparing our
reproduction against the paper's figure. Clearly labelled axes and matching ranges.

## Execution Guidance

* **Code-reproduction task type**. Steps: research-papers (done), research-internet (done),
  research-code, planning, implementation, results, compare-literature, suggestions,
  reporting. Skipped: setup-machines, teardown, creative-thinking.
* Local CPU only. No Vast.ai. Estimate 1-2 days of execution time; MOD compilation on Windows
  may take a non-trivial fraction of that, and the noise-driver addition adds one iteration
  cycle.
* Use absolute imports and centralised `paths.py` / `constants.py` per the project's Python
  style guide.

## Anticipated Risks

* **ModelDB 189347 may reference a morphology file not in t0005**: audit carefully; if the
  paper used a different morphology, flag and either fetch the paper's morphology or document
  the substitution as a reproduction bug.
* **MOD file compilation on Windows NEURON 8.2.7**: some MOD files in older ModelDB releases
  need minor adjustments to compile under modern NEURON. Record every adjustment as a
  potential discrepancy.
* **Noise driver**: the shipped code cannot produce Figures 6-8 because it lacks a luminance
  noise driver. Our port must add one; document the addition as a discrepancy (the paper's
  Figure 6-8 results therefore came from a version of the code the authors did not deposit).
* **gNMDA pick**: paper says 2.5 nS, code uses 0.5 nS. Primary reproduction uses 0.5 nS
  (follow code); secondary run at 2.5 nS documents whether the paper claim or the code
  publishes the Figure 1-5 behaviour.

## Relationship to Other Tasks

* **Currently blocks (administrative)**: t0042, t0043, t0044 are `intervention_blocked`
  pending this task. **Note**: t0043's peak-rate framing was built on the same category error
  this task's revised scope addresses; after this task completes, the case for t0043 as
  currently scoped should be reviewed explicitly.
* **Complements**: t0008 (initial port) and t0020 (gabaMOD protocol fix) remain in the history
  as partial reproductions focused on DSI. This task does not modify them; it produces an
  independent, more complete reproduction against the paper's actual reported metrics.
* **Precedes**: any future optimisation task (t0033 style) should use this library asset as
  the starting point.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_library_asset.py` passes for `modeldb_189347_dsgc_exact`.
* Answer-asset verificator passes for `poleg-polsky-2016-reproduction-audit`.
* All pass criteria above met: PSP amplitudes within 1 SD, slope angles within 1 SD, ROC AUC
  within +/-0.05, Figure 8 qualitative checks pass, basic parameters match ModelDB code
  exactly.
* Every paper test attempted is represented in the figure-reproduction table with a match /
  no-match verdict and numerical evidence.
* Discrepancy catalogue is complete and includes the four pre-flagged items plus any new
  findings.

**Results summary:**

> **Results Summary: Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)**
>
> **Summary**
>
> The from-scratch port of ModelDB 189347 reproduces the qualitative direction-tuning
> behaviour
> (preferred-direction PSP > null-direction PSP) and matches the paper's slope-angle and
> ROC-AUC
> targets within tolerance, but absolute PSP amplitudes at the code-pinned `b2gnmda = 0.5 nS`
> overshoot the paper's reported means by approximately 4x. The paper-vs-code discrepancies on
> synapse
> count, gNMDA value, and noise driver behaviour are confirmed; **12 discrepancies** are
> catalogued in
> the audit, including six MOD-default vs `main.hoc`-override mismatches.
>
> **Metrics**
>
> * **Fig 1 PD PSP** (b2gnmda = 0.5 nS, code value): **23.25 mV** vs paper **5.8 +/- 3.1 mV**
>   —
> outside 1-SD band (synapse-count discrepancy).
> * **Fig 1 slope angle** (b2gnmda = 0.5 nS): **54.8 deg** vs paper **62.5 +/- 14.2 deg** —
>   within
> tolerance.
> * **Fig 4 high-Cl- slope**: **47.3 deg** vs paper **45.5 +/- 3.7 deg** — within tolerance.
> * **Fig 5 0 Mg2+ slope**: **50.7 deg** vs paper **45.5 +/- 5.3 deg** — within tolerance.
> * **Fig 7 ROC AUC** (control / AP5 / 0 Mg2+): **1.00 / 1.00 / 1.00** vs paper **0.99 / 0.98
>   / 0.83**

</details>

<details>
<summary>✅ 0041 — <strong>Electrotonic-length collapse analysis of t0034 and
t0035</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0041_electrotonic_length_collapse_t0034_t0035` |
| **Status** | completed |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0035-01` |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-04-24T11:33:06Z |
| **End time** | 2026-04-24T12:15:00Z |
| **Step progress** | 9/12 |
| **Task page** | [Electrotonic-length collapse analysis of t0034 and t0035](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md) |
| **Task folder** | [`t0041_electrotonic_length_collapse_t0034_t0035/`](../../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/results/results_detailed.md) |

# Electrotonic-Length Collapse Analysis of t0034 and t0035

## Source Suggestion

S-0035-01 (zero-cost L/lambda collapse analysis of t0034 length and t0035 diameter data).

## Motivation

t0034 (distal-length sweep on t0024) and t0035 (distal-diameter sweep on t0024) together
establish a ~25–30x asymmetry in DSI sensitivity: length slope -0.126 (p=0.038) vs diameter
slope +0.004 (p=0.88). Cable theory predicts this asymmetry because electrotonic length scales
as L / sqrt(d * Rm / (4 * Ra)) — linearly in raw length, but as 1/sqrt(d) in raw diameter. If
the cable-theory prediction is tight, primary DSI from both sweeps should collapse onto a
single DSI-vs-L/lambda curve.

Confirming the collapse would allow the t0033 morphology + channel optimiser to parameterise
morphology in 1-D (electrotonic length) rather than 2-D (raw length × raw diameter),
eliminating diameter as a spurious degree of freedom and reducing the search-space size.

## Objective

For every (length multiplier, diameter multiplier) operating point in the combined t0034 ∪
t0035 dataset, compute the electrotonic length L/lambda of the swept distal section using the
t0024 baseline biophysics (Rm, Ra from the Poleg-Polsky-2016 parameter backbone). Plot primary
DSI and vector-sum DSI vs L/lambda for both sweeps on the same axes. Test whether the two
sweeps collapse onto one curve with Pearson r > 0.9, and report the residual variance
attributable to non-cable effects.

## Scope

* Zero simulation cost. No NEURON invocations. Pure post-hoc analysis on the existing t0034
  and t0035 trial-level CSV outputs.
* Use only the primary-DSI and vector-sum-DSI per-trial outputs; do not re-derive quantities
  from raw spike trains.
* Input data: both sweeps' trial-level CSVs in their respective `results/` folders.
* Output: one answer asset documenting the collapse test, one figure showing primary DSI and
  vector-sum DSI on a common L/lambda axis, and a one-paragraph recommendation for the t0033
  parameterisation.

## Deliverables

* `assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/` — full answer
  asset per the answer specification.
* `results/images/electrotonic_length_collapse.png` — overlay of both sweeps.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections.
* `results/metrics.json` — at minimum the Pearson r between the two sweeps on the common
  L/lambda axis, the residual RMSE after fitting a single curve, and the recommendation
  verdict (collapse-confirmed / collapse-rejected).

## Out of Scope

* No new simulation runs on any testbed.
* No modifications to t0022, t0024, or the t0033 plan.
* No PDF re-reading of Kim 2014 or Sivyer 2013 (still blocked on paywall access).

## Anticipated Risks

* The distal section in t0024 may not have a single uniform (Rm, Ra); if it does not, compute
  a section-weighted average L/lambda and report the approximation in the results.
* If collapse is weak (Pearson r < 0.7), state this explicitly as a negative result and
  enumerate the non-cable effects (spike failure at extremes, AR(2) noise correlation) that
  the collapse model misses.

**Results summary:**

> **Results Summary: t0041 Electrotonic-Length Collapse Analysis**
>
> **Summary**
>
> Tested whether primary DSI and vector-sum DSI from t0034 (distal length sweep) and t0035
> (distal
> diameter sweep) collapse onto a single DSI-vs-L/lambda curve under Rall's cable theory.
> **Verdict:
> collapse_rejected.** The two sweeps do not share a common L/lambda parameterisation: Pearson
> r =
> +0.42 for primary DSI and -0.68 for vector-sum DSI (sign inverted), both well below the 0.9
> confirmation threshold. Recommendation for t0033: keep the 2-D (raw length x raw diameter)
> morphology parameterisation.
>
> **Metrics**
>
> * **Pearson r primary DSI (overlap region, n=3 paired points)**: **+0.4161** (p=0.727).
>   Threshold
> for collapse_confirmed is r > 0.9. **Collapse rejected.**
> * **Pearson r vector-sum DSI (overlap region, n=3 paired points)**: **-0.6787** (p=0.525).
>   Sign is
> inverted from the cable-theory prediction. **Collapse rejected.**
> * **Pooled polynomial-fit residual RMSE**: primary DSI **0.0397**, vector-sum DSI
>   **0.0237**.
> Residuals of this magnitude relative to the 0.23 and 0.15 total DSI spread confirm that
> non-cable
> effects dominate the response.

</details>

<details>
<summary>✅ 0040 — <strong>Brainstorm results session 8</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0040_brainstorm_results_8` |
| **Status** | completed |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0032_brainstorm_results_7`](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md), [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0038_correct_t0033_base_gaba_to_4ns`](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md), [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-24T14:00:00Z |
| **End time** | 2026-04-24T15:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 8](../../../overview/tasks/task_pages/t0040_brainstorm_results_8.md) |
| **Task folder** | [`t0040_brainstorm_results_8/`](../../../tasks/t0040_brainstorm_results_8/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0040_brainstorm_results_8/results/results_detailed.md) |

# Brainstorm Results Session 8

## Motivation

Eighth strategic brainstorming session, run on 2026-04-24 after the t0037–t0039 wave merged.
The researcher requested a cross-task audit of every test run so far against published data,
with the explicit goal of identifying discrepancies and designing corrections. The session
produced a master test table, a published-data comparison table (both saved under `results/`),
and a prioritised list of four follow-up tasks that target the discrepancies.

## Scope

* Review project state after the t0037–t0039 merges: 37 tasks completed, 1 `not_started`
  (t0031), 1 `intervention_blocked` (t0023), 151 uncovered suggestions, $0.00 / $1.00 budget
  used.
* Build a master table summarising every simulation test we have run (13 tests across t0008,
  t0020, t0022, t0024, t0026, t0029, t0030, t0034, t0035, t0036, t0037, t0039).
* Build a published-data comparison table listing every quantitative claim from the
  `compare_literature.md` files and classify each as MATCH / PARTIAL / MISMATCH.
* Group the mismatches into discrepancy themes and propose root-cause corrections.
* Approve four tasks (t0041–t0044) that address the top-leverage discrepancies.
* Apply one suggestion rejection and four reprioritisations based on recent findings.

## Researcher Decisions

* **Four new tasks, all zero-cost local runs**:
  * **t0041** — L/lambda electrotonic-length collapse analysis of t0034 and t0035 data. Data
    analysis only, no simulation. Covers S-0035-01.
  * **t0042** — Fine-grained null-GABA ladder {3.5, 3.0, 2.5} nS on t0022 baseline diameter.
    Tests whether t0022 can reach DSI >= 0.5 below 4 nS without destabilising preferred
    direction.
  * **t0043** — Add Nav1.6 + Kv3 to AIS\_DISTAL and distal dendrites of t0022; restore NMDA at
    PD and ND BIPs; validate peak rate against t0004 envelope (40–80 Hz). Covers S-0019-03
    (partial), S-0018-03 (partial), S-0022-02.
  * **t0044** — 7-diameter Schachter2010 re-test on the t0043 output substrate at GABA = 4 nS.
    Pass/fail on quadratic curvature sign. Covers S-0002-02.
* **Execution order**: t0041 and t0042 can run in parallel; t0043 can run in parallel with
  them; t0044 depends on t0043 completion.
* **Suggestion corrections**:
  * Reject S-0030-06 (vector-sum DSI as t0033 objective). Superseded by S-0034-07 (primary DSI
    on t0024).
  * Reprioritise S-0029-01, S-0029-02, S-0030-02, S-0010-01 from high to medium pending t0043
    and t0044 outcomes.
* **Sheffield paywalled-paper retrieval** (Kim2014 + Sivyer2013): deferred to a later wave.
* **t0023**: remains intervention_blocked; not revisited this session.

## New Tasks Created

Five child tasks (t0041, t0042, t0043, t0044) are authorised by this session. Task indices are
auto-assigned by `/create-task` and will be strictly greater than 40 per the ordering
invariant. Full scopes live in each child task's `task_description.md`.

## Correction Files

Five corrections written to `corrections/`:

* `suggestion_S-0030-06.json` — update status to rejected
* `suggestion_S-0029-01.json` — update priority to medium
* `suggestion_S-0029-02.json` — update priority to medium
* `suggestion_S-0030-02.json` — update priority to medium
* `suggestion_S-0010-01.json` — update priority to medium

## Published-Data Comparison Artifact

Per the researcher's explicit request, the master test table and the published-data comparison
table are stored as `results/test_vs_literature_table.md`. They are also embedded in
`results/results_detailed.md` under the Methodology section and reproduced in
`logs/session_log.md` as part of the session transcript.

## Expected Assets

This brainstorm session produces no assets beyond the brainstorm-results task folder and its
downstream child tasks. `expected_assets` is `{}`.

## Dependencies

All 37 completed tasks up through t0039. t0023 and t0031 are excluded because they are not
completed.

**Results summary:**

> **Results Summary: Brainstorm Session 8**
>
> **Summary**
>
> Eighth strategic brainstorm, run on 2026-04-24 after the t0037–t0039 merges. The session
> produced
> a cross-task audit comparing every DSGC simulation test we have run against published data,
> and
> approved four follow-up tasks (t0041–t0044) that target the discrepancies. One suggestion
> was
> rejected and four were reprioritised from high to medium.
>
> **Session Overview**
>
> Date: 2026-04-24. Duration: ~90 min. The researcher requested a master table of every test
> plus a
> side-by-side comparison to published data, with the explicit purpose of identifying
> discrepancies
> and designing corrections. Phase 1 aggregated project state (39 tasks total, 37 completed, 1
> `intervention_blocked`, 1 `not_started`; 151 uncovered suggestions; $0.00 / $1.00 budget
> used) and
> delegated the cross-task synthesis to subagents. Phase 2 proposed four tasks (t0041–t0044)
> plus
> five suggestion corrections; the researcher confirmed all five decisions and explicitly
> deferred a
> Sheffield paywalled-paper retrieval task.
>
> **Decisions**

</details>

<details>
<summary>✅ 0039 — <strong>7-diameter sweep on t0022 DSGC at GABA=4 nS</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0039_distal_dendrite_diameter_sweep_t0022_gaba4` |
| **Status** | completed |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0037-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-24T07:15:32Z |
| **End time** | 2026-04-24T08:18:00Z |
| **Step progress** | 11/15 |
| **Task page** | [7-diameter sweep on t0022 DSGC at GABA=4 nS](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Task folder** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4/`](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/results/results_detailed.md) |

# 7-Diameter Sweep on t0022 DSGC at GABA=4 nS

## Motivation

t0030 originally ran a 7-diameter sweep on t0022 to measure the
Schachter2010-vs-passive-filtering DSI slope — the project's headline discriminator target
since its inception. The attempt failed because the t0022 default `GABA_CONDUCTANCE_NULL_NS =
12 nS` pins primary DSI at 1.000 (null firing = 0 Hz), leaving the discriminator flat across
all diameters. t0036 halved the GABA to 6 nS; still pinned. t0037 then swept the ladder {4, 2,
1, 0.5, 0} nS and found **4 nS** is the operational sweet spot (DSI=0.429, DSGC-like preferred
direction 40.8°, matches Park2014's biological range 0.40–0.60).

This task reruns t0030's geometry sweep at the newly-discovered working GABA level, producing
the first diameter-vs-DSI measurement on t0022 with a discriminator that has dynamic range.
The resulting slope is the quantity the project needs to test the Schachter2010
active-amplification hypothesis against the passive cable-theory prediction.

## Scope

Sweep **distal dendrite diameter** across 7 levels at `GABA_CONDUCTANCE_NULL_NS = 4.0 nS` on
the t0022 testbed. All other parameters match the t0030 baseline, so the two sweeps are
directly comparable except for the GABA value.

* Diameters (µm): {0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0}
* Trials per angle per diameter: 10
* Angles per sweep: 12 (standard DSGC tuning directions)
* Total trials: 7 × 12 × 10 = **840 trials**
* Expected wall time on local Windows CPU: ~30 minutes (~2 s/trial)
* Cost: $0.00

## Dependencies

* `t0022_modify_dsgc_channel_testbed` — testbed + `GABA_CONDUCTANCE_NULL_NS` knob
* `t0030_distal_dendrite_diameter_sweep_dsgc` — reuses diameter-sweep driver and analysis code
* `t0037_null_gaba_reduction_ladder_t0022` — source of the 4 nS GABA choice

## Approach

1. Copy t0030's code into t0039's `code/` folder (ARF cross-task import rule requires
   copying).
2. Adapt t0037's `gaba_override.py` — call `set_null_gaba_ns(4.0)` at the start of each trial
   before invoking `run_tuning_curve`.
3. Parameterise the diameter sweep over the t0030 diameter list.
4. Run all 840 trials locally; monitor the process until completion.
5. Analyse per-diameter DSI means and stddev; fit the DSI-vs-diameter slope and compare to
   Schachter2010 (active amplification expects concave-down, passive filtering expects
   monotonically decreasing).
6. Write `compare_literature.md` matching our slope against published DSGC diameter
   dependence.

## Expected Outputs

* `results/data/sweep_results.csv` — full 840-trial raw output (diameter, angle, trial,
  peak_hz, null_hz, dsi_primary, dsi_vector_sum, pref_angle).
* `results/data/metrics_per_diameter.csv` — per-diameter aggregated metrics (mean, stddev, n).
* `results/data/slope_fit.json` — fitted slope of DSI vs diameter with CI.
* `results/images/dsi_vs_diameter.png` — DSI means with error bars across 7 diameters.
* `results/images/tuning_curves_per_diameter.png` — 7-panel plot of fitted tuning curves.
* `results/results_summary.md`, `results/results_detailed.md` — full writeup.
* `results/compare_literature.md` — comparison to Schachter2010 vs passive cable predictions.
* `results/suggestions.json` — follow-ups based on outcome.

## Expected Assets

None beyond CSV / JSON / images. Task type: `experiment-run`.

## Compute and Budget

* Local Windows CPU only. No GPU, no remote machines, no paid APIs.
* Wall time: ~30 minutes for the sweep; total task wall time including ARF pipeline ~60
  minutes.
* Cost: $0.00.

## Cross-References

* Source suggestion: **S-0037-01** — "Rerun t0030's 7-diameter sweep at GABA=4 nS on t0022".
* Evidence task: t0037 (DSI=0.429 at 4 nS, DSGC-like pref 40.8°).
* Pinned baselines: t0030 (12 nS, DSI=1.000 flat), t0036 (6 nS, DSI=1.000 still flat).
* Correction task: t0038 (recorded the base-parameter update on t0033's answer asset).

## Verification Criteria

1. 840 trials complete successfully (exit code 0 from the sweep driver).
2. `metrics_per_diameter.csv` has 7 rows, all with non-null DSI values.
3. At least one diameter has primary DSI measurably different from every other diameter (the
   sweep is informative, not pinned).
4. The DSI-vs-diameter slope is reported with a numeric value and 95% CI.
5. All standard verificators PASS with zero errors.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
> date_completed: "2026-04-24"
> status: "complete"
> ---
> **Results Summary: 7-Diameter Sweep on t0022 at GABA=4 nS**
>
> **Summary**
>
> Rerunning t0030's 7-diameter sweep at the t0037-validated operational GABA level
> (`GABA_CONDUCTANCE_NULL_NS = 4.0 nS`) produces the first diameter-vs-DSI measurement on
> t0022 with a
> discriminator that has dynamic range. DSI decreases monotonically from **0.429** at D=0.5x
> baseline
> to **0.368** at D=2.0x, slope=**-0.034** per log2(multiplier), **p=0.008**. Mechanism
> classified as
> **passive_filtering** on t0030's inherited thresholds. The preferred direction stays pinned
> near
> **40°** across the full sweep, confirming the E-I schedule encodes the DS axis; morphology
> sets the
> gain.
>
> **Metrics**
>

</details>

<details>
<summary>✅ 0038 — <strong>Correct t0033 base GABA to 4 nS on t0022 variant</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0038_correct_t0033_base_gaba_to_4ns` |
| **Status** | completed |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0037-02` |
| **Task types** | [`correction`](../../../meta/task_types/correction/) |
| **Start time** | 2026-04-24T07:01:47Z |
| **End time** | 2026-04-24T07:12:00Z |
| **Step progress** | 7/15 |
| **Task page** | [Correct t0033 base GABA to 4 nS on t0022 variant](../../../overview/tasks/task_pages/t0038_correct_t0033_base_gaba_to_4ns.md) |
| **Task folder** | [`t0038_correct_t0033_base_gaba_to_4ns/`](../../../tasks/t0038_correct_t0033_base_gaba_to_4ns/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0038_correct_t0033_base_gaba_to_4ns/results/results_detailed.md) |

# Correct t0033 base GABA to 4 nS on t0022 variant

## Motivation

t0033's Vast.ai optimisation plan was written before the GABA-ladder rescue was available. At
the time, the plan implicitly assumed the t0022 default `GABA_CONDUCTANCE_NULL_NS = 12 nS` as
the base parameter for the joint morphology + channel optimisation. Subsequent experimental
tasks showed this default is incompatible with a working DSI objective:

* **t0030** — 7-diameter sweep at 12 nS: primary DSI pinned at 1.000; diameter effect
  unmeasurable.
* **t0036** — halved to 6 nS: primary DSI still pinned at 1.000; null firing = 0 Hz.
* **t0037** — ladder sweep across {4, 2, 1, 0.5, 0} nS: 4 nS is the operational sweet spot
  (primary DSI = 0.429, preferred direction = 40.8°, matches Park2014's biological range
  0.40–0.60). Below 2 nS the cell over-excites and preferred direction randomises.

Without this correction, any downstream task that reads t0033's plan and instantiates an
optimiser on t0022 with the legacy 12 nS default would burn compute on a pinned objective: the
optimiser would see a flat DSI=1.000 landscape and converge to anything.

## Scope

Create a correction file in `corrections/` that updates t0033's answer asset
(`vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation`) to document the new
base-parameter recommendation. The correction's `changes` payload adds or overrides a
parameter note so that aggregators and downstream consumers expose the corrected effective
view.

This is a **correction-type task**. No sweep, no plan rewrite, no new answer asset. The
completed t0033 folder remains untouched, per the ARF immutability rule.

## Dependencies

* `t0033_plan_dsgc_morphology_channel_optimisation` — target of the correction
* `t0037_null_gaba_reduction_ladder_t0022` — source of the 4 nS evidence

## Approach

1. Read `arf/specifications/corrections_specification.md` to confirm the correction file
   format for `target_kind: "answer"` with `action: "update"`.
2. Read t0033's `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/`
   details and full answer document to understand what the correction must override.
3. Write
   `corrections/answer_vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation.json`
   with a concise `changes` object and a `rationale` citing t0037's DSI=0.429 result at 4 nS
   and t0036's pinned result at 6 nS.
4. Run `verify_correction.py` (or equivalent) to confirm the correction file is valid.
5. Run `aggregate_answers.py` to confirm the effective aggregated view of the answer reflects
   the new base parameter.

## Expected Outputs

* `corrections/answer_vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation.json` —
  single correction file with `correction_id: "C-0038-01"`, `action: "update"`, and
  `target_kind: "answer"`.
* `results/results_summary.md` — brief confirmation that the correction was written and
  verified.
* `results/suggestions.json` — empty or minimal; this task closes S-0037-02 and does not
  generate new experimental follow-ups.

## Expected Assets

None. This task produces a correction file and a results writeup, not new assets.

## Compute and Budget

* Local only. No remote machines. No paid APIs.
* Expected wall time: under 5 minutes total (metadata edit + verificator runs).
* Cost: $0.00.

## Cross-References

* Source suggestion: **S-0037-02** ("Update t0033 optimiser base GABA on t0022 variant to 4.0
  nS")
* Evidence task: t0037 (DSI=0.429 at 4 nS; DSGC-like preferred direction 40.8°)
* Pinned baselines: t0030 (12 nS, DSI=1.000), t0036 (6 nS, DSI=1.000)

## Verification Criteria

1. `corrections/answer_vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation.json`
   exists and passes the corrections verificator.
2. The `correction_id` matches the regex `^C-0038-\d{2}$`.
3. `correcting_task` equals `t0038_correct_t0033_base_gaba_to_4ns` and `target_task` equals
   `t0033_plan_dsgc_morphology_channel_optimisation`.
4. Running `aggregate_answers` with the correction overlay in place surfaces the updated base
   parameter (or a field recording the update) in the effective answer object.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0038_correct_t0033_base_gaba_to_4ns"
> date_completed: "2026-04-24"
> status: "complete"
> ---
> **Results Summary: Correct t0033 Base GABA to 4 nS on t0022 Variant**
>
> **Summary**
>
> Wrote correction `C-0038-01` against t0033's answer asset
> `vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation` encoding the t0037 finding
> that the
> operational base parameter on t0022 is `GABA_CONDUCTANCE_NULL_NS = 4.0 nS`, not the original
> 12 nS
> default. Closes suggestion **S-0037-02**. Verificator PASSED. No sweep, no code, no new
> assets.
> Total cost $0.00, wall time under 10 minutes.
>
> **Metrics**
>
> * **Correction files produced**: **1** (`answer_vastai-*.json`).
> * **Correction ID**: `C-0038-01`.

</details>

<details>
<summary>✅ 0037 — <strong>Null-GABA reduction ladder on t0022 DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0037_null_gaba_reduction_ladder_t0022` |
| **Status** | completed |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0036-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-23T22:56:20Z |
| **End time** | 2026-04-24T00:10:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Null-GABA reduction ladder on t0022 DSGC](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Task folder** | [`t0037_null_gaba_reduction_ladder_t0022/`](../../../tasks/t0037_null_gaba_reduction_ladder_t0022/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0037_null_gaba_reduction_ladder_t0022/results/results_detailed.md) |

# Null-GABA Reduction Ladder on t0022 DSGC

## Motivation

t0036 reduced `GABA_CONDUCTANCE_NULL_NS` from 12 nS to 6 nS (Schachter2010-matched) on the
t0022 distal-diameter sweep and found **null firing still pinned at 0.0 Hz** across every
diameter — the rescue hypothesis S-0030-01 was falsified at 6 nS. t0036's creative-thinking
enumerated 5 explanations (notably: 12 nS was far above threshold, so 6 nS is still too high),
and suggestion S-0036-01 proposed further reductions in sequence: **4 nS → 2 nS → 1 nS**.

This task runs that ladder efficiently as a focused **1D sweep at baseline diameter only**
(instead of 3× full diameter sweeps). The question: at what GABA level (if any) does null-
direction firing become non-zero on the t0022 deterministic schedule? The answer bounds
whether a future full diameter sweep at the unpinning level is worth the compute.

If **all** tested GABA levels still yield 0 Hz null firing (including 0 nS — full GABA block),
the null result falsifies any conductance-only rescue on t0022 and rules out future work along
that axis — forcing the optimiser to either use t0024 or adopt vector-sum DSI on t0022
(already queued as S-0030-06).

## Scope

1. Use the **t0022 DSGC testbed** as-is. Distal diameter locked at **1.0× baseline** (no
   diameter variation).
2. Sweep `GABA_CONDUCTANCE_NULL_NS` across **5 levels**: **{4.0, 2.0, 1.0, 0.5, 0.0}** nS.
   Brackets S-0036-01's specified 4/2/1 with a finer end (0.5) and full GABA block (0.0) as a
   sanity extreme.
3. At each GABA level, run the standard **12-direction × 10-trial protocol = 120 trials**.
   Total = **5 × 120 = 600 trials**.
4. Measure **null-direction firing rate (critical diagnostic)** + primary DSI + vector-sum DSI
   + peak Hz + HWHM per GABA level.
5. Report: the lowest GABA level at which null firing becomes non-zero (if any); recommend a
   follow-up full diameter sweep at that level OR definitively falsify the conductance-only
   rescue.

## Approach

* **Local CPU only.** No remote compute, $0.
* Copy the t0036 `gaba_override` monkey-patch pattern into a CLI-switchable version that
  accepts a numeric GABA value per run.
* Run the 12-direction × 10-trial protocol five times, one per GABA level, accumulating into a
  tidy CSV keyed by `(gaba_null_ns, direction_deg, trial)`.
* Analyse: per-GABA null_hz, peak_hz, DSI primary, DSI vector-sum, HWHM.
* Chart: `null_hz_vs_gaba.png` (critical diagnostic), `primary_dsi_vs_gaba.png`,
  `vector_sum_dsi_vs_gaba.png`, `peak_hz_vs_gaba.png`, polar overlay of all 5 levels.

## Expected Outputs

* `results/results_summary.md` — headline: lowest GABA level with non-zero null firing (or
  definitive falsification).
* `results/results_detailed.md` — per-GABA metrics, per-direction breakdown at each level,
  recommendation for follow-up.
* `results/images/null_hz_vs_gaba.png` (THE key chart), plus primary-DSI, vector-sum-DSI,
  peak-Hz, polar-overlay.
* `results/metrics.json` — per-GABA-level registered DSI metrics.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* Local CPU only. Expected runtime: **~20-30 minutes** (600 trials × ~2 s/trial on t0022
  deterministic).
* $0 external cost.

## Measurement

* **Primary diagnostic**: **null-direction firing rate per GABA level**. Non-zero at any level
  → the rescue works at that level.
* **Secondary**: primary DSI (expected to drop below 1.000 once null firing unpins),
  vector-sum DSI, peak Hz, HWHM, per-direction spike counts.

## Key Questions

1. At what (if any) GABA level does null-direction firing become non-zero?
2. If null firing unpins at some level, what is the primary DSI at that level?
3. If NO level unpins null firing — including 0 nS full GABA block — what does that imply
   about the t0022 schedule? Does the AMPA EPSP simply never reach AP threshold at null
   angles, independent of GABA?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the testbed architecture.
* **t0036_rerun_t0030_halved_null_gaba** (completed) — provides the `gaba_override`
  monkey-patch pattern, the baseline-GABA=6 nS null result, and the 177-section distal-
  selection rule. Also provides code/constants inheritance.

## Scientific Context

Source suggestion **S-0036-01** (high priority). The 4/2/1 nS sequence was the explicit
recommendation; extended here to 0.5 and 0 nS to bracket the extreme case. Result interacts
directly with:
- **S-0030-02** (Poisson noise rescue): if GABA ladder fails, Poisson is the next attempt
- **S-0030-06** (vector-sum DSI objective): if GABA ladder fails, this becomes the recommended
  t0033 objective on t0022

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 + t0030 + t0036 cover mechanism priors).
* Include `research-code` — need to copy t0036's `gaba_override` and generalise it.
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `creative-thinking` — if rescue fails even at 0 nS, the finding is mechanism-
  defining for t0022.
* Include `compare-literature` — compare unpinning threshold to Schachter2010 / Park2014
  null-inhibition ranges.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0037_null_gaba_reduction_ladder_t0022"
> date_completed: "2026-04-24"
> status: "complete"
> ---
> **Results Summary: Null-GABA Reduction Ladder on t0022 DSGC**
>
> **Summary**
>
> Swept `GABA_CONDUCTANCE_NULL_NS` across 5 levels {4, 2, 1, 0.5, 0} nS at baseline diameter
> on t0022
> (600 trials). **S-0036-01 rescue hypothesis CONFIRMED**: null firing unpinned at every
> tested level
> (6-15 Hz vs t0036's 0 Hz at 6 nS baseline). The **operational sweet spot is 4 nS**:
> DSI=0.429, peak
> 15 Hz, null 6 Hz, preferred direction ~40° — biologically realistic DSGC regime. At ≤ 2 nS
> the cell
> fires everywhere and preferred direction randomises. The follow-up recommendation is to
> **rerun
> t0030's 7-diameter sweep at GABA=4 nS** to measure the Schachter2010 vs passive-filtering
> slope.
>
> **Metrics**
>
> * **GABA unpinning threshold**: **≤ 4.0 nS** (highest tested level with null firing already

</details>

## ❌ Cancelled

<details>
<summary>❌ 0042 — <strong>Fine-grained null-GABA ladder (3.5, 3.0, 2.5 nS) on
t0022</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0042_fine_grained_null_gaba_ladder_t0022` |
| **Status** | cancelled |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Fine-grained null-GABA ladder (3.5, 3.0, 2.5 nS) on t0022](../../../overview/tasks/task_pages/t0042_fine_grained_null_gaba_ladder_t0022.md) |
| **Task folder** | [`t0042_fine_grained_null_gaba_ladder_t0022/`](../../../tasks/t0042_fine_grained_null_gaba_ladder_t0022/) |

# Fine-Grained Null-GABA Ladder on t0022

## Status: BLOCKED (2026-04-24)

Blocked pending completion of **t0046_reproduce_poleg_polsky_2016_exact**. The researcher has
paused all t0022-substrate modification tasks until the faithful ModelDB 189347 reproduction
establishes whether the observed DSI and peak-rate values in t0022 reflect genuine mechanism
gaps (justifying this task) or accumulated deviations from Poleg-Polsky 2016 (making this
task's target irrelevant). Reassess after t0046 merges.

## Motivation

t0037 swept null-GABA at {0, 0.5, 1, 2, 4} nS on t0022 and identified a sweet spot at 4 nS
(primary DSI 0.429, preferred direction 40.8 deg, matching Park 2014's in vivo band
0.40–0.60). Below 2 nS the cell over-excites and preferred direction randomises. t0039 then
showed that at GABA = 4 nS the t0022 diameter axis produces a monotonic DSI decline (slope
-0.034, p=0.008) — passive-filtering rather than Schachter 2010 active amplification.

What t0037 did not probe is the interval between 2 and 4 nS. Brainstorm session 8 requested a
fine-grained ladder at {3.5, 3.0, 2.5} nS to answer: does t0022 admit a GABA level below 4 nS
where DSI exceeds 0.5 without destabilising preferred direction? This directly informs whether
t0022 is usable as an optimisation substrate above its current 0.429 ceiling.

## Objective

Run the t0037 protocol (12 directions × 10 trials per direction, baseline diameter, V_rest =
-60 mV) at three additional null-GABA levels: 3.5 nS, 3.0 nS, 2.5 nS. Report primary DSI,
vector-sum DSI, preferred direction, peak firing rate, and null firing rate at each level.
Compare against t0037's 4 nS and 2 nS anchors.

Pass criterion: at any of the three new levels, primary DSI >= 0.50 AND preferred direction
stability across trials under 10 deg standard deviation. If pass, that GABA level becomes a
candidate new base parameter for t0022 optimisation; emit a suggestion for a follow-up
correction task (analogous to t0038) to propagate the new base into t0033.

Fail criterion: all three new levels yield DSI < 0.50 or preferred-direction standard
deviation
> 10 deg. If fail, report that 4 nS is the effective t0022 ceiling and recommend the t0033 optimiser
> switch substrates to t0024 per S-0034-07.

## Scope

* Local CPU only. No remote compute. ~1 hour total wall-clock.
* Reuse the t0037 trial_runner with only the null-GABA parameter changed; no code changes to
  the testbed.
* Produce tuning curves (Cartesian and polar) at each GABA level.

## Out of Scope

* Morphology sweeps (covered by t0039 at 4 nS).
* Channel-inventory modifications (covered by t0043).
* Schachter re-test (covered by t0044).

## Deliverables

* Per-GABA-level tuning-curve CSV + polar plot under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections,
  explicit Pass/Fail verdict against the criterion above.
* `results/metrics.json` with primary DSI, vector-sum DSI, preferred direction (mean and sd),
  peak Hz, and null Hz at each of the three new GABA levels, plus the two t0037 anchors.
* If Pass: one new suggestion in `results/suggestions.json` proposing a correction task to set
  the new GABA base value in t0033.

## Anticipated Risks

* Narrow sampling (three points) may miss a non-monotonic optimum between 2 and 4 nS; if
  results look non-monotonic, emit a follow-up suggestion for a denser sweep rather than
  extrapolating.
* If the cell destabilises at 2.5 nS or 3.0 nS, record the destabilisation metrics (preferred
  direction sd, coefficient of variation of peak rate) rather than treating those runs as
  failures.

</details>

<details>
<summary>❌ 0043 — <strong>Nav1.6 + Kv3 + NMDA restoration on t0022 channel
testbed</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0043_nav16_kv3_nmda_restoration_t0022` |
| **Status** | cancelled |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0019-03` |
| **Task types** | [`feature-engineering`](../../../meta/task_types/feature-engineering/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Nav1.6 + Kv3 + NMDA restoration on t0022 channel testbed](../../../overview/tasks/task_pages/t0043_nav16_kv3_nmda_restoration_t0022.md) |
| **Task folder** | [`t0043_nav16_kv3_nmda_restoration_t0022/`](../../../tasks/t0043_nav16_kv3_nmda_restoration_t0022/) |

# Nav1.6 + Kv3 + NMDA Restoration on t0022

## Status: BLOCKED (2026-04-24)

Blocked pending completion of **t0046_reproduce_poleg_polsky_2016_exact**. This task proposes
channel inventory modifications beyond Poleg-Polsky 2016's original model to close the
observed peak-rate gap (15 Hz vs paper's 40-80 Hz range). If t0046 shows the peak-rate gap is
inherent to the faithful reproduction of the paper (present in their code too), this task's
motivation evaporates and the gap must be addressed differently (stimulus duration, drive
amplitude, paper claim re-interpretation). If t0046 matches the paper's firing rates, then our
prior modifications introduced the gap and this task's channel-additions become a well-founded
fix. Reassess after t0046 merges.

## Source Suggestion

S-0019-03 primary (implement Nav1.6 / Nav1.2 / Kv1 / Kv3 channels with AIS-specific
densities). This task covers the Nav1.6 and Kv3 portion of S-0019-03. It also partially covers
S-0018-03 (NMDA restoration) and S-0022-02 (Nav1.6 distal-AIS density).

## Motivation

The cross-task audit in brainstorm session 8 (see
`tasks/t0040_brainstorm_results_8/results/test_vs_literature_table.md`) identifies peak firing
rate as the most universal mismatch: 15 Hz across t0022 baseline and every t0022-based sweep,
vs 30–150 Hz in every cited published source (Oesch 2005: 148 Hz; Chen 2009: 166 Hz; Sivyer
2013: 80–150 Hz). The likely causes stack: (a) t0022 uses lumped HHst which lacks Nav1.6
persistent Na current and Kv3 fast repolarisation, both of which are needed for high-frequency
AP firing; (b) the t0022 E-I schedule zeros NMDA at both PD and ND BIPs, removing the expected
NMDA-mediated gain boost; (c) AMPA-only drive caps the effective depolarisation.

The audit also shows that Schachter 2010's predicted active-amplification diameter signature
is absent on every diameter sweep we have run (t0030, t0035, t0039). One candidate explanation
is that without Nav1.6 / Kv3 in the distal dendrite, the regenerative threshold-crossing
regime Schachter 2010 relies on cannot be recruited.

This task restores the channel inventory and NMDA drive so the peak-rate mismatch can be
attacked, and so the Schachter re-test in t0044 runs against a model that matches published
DSGC channel priors.

## Objective

Produce a new library asset (tentatively `modeldb_189347_dsgc_t0043` or similar) that is a
fork of the t0022 testbed with three modifications:

1. Nav1.6 mechanism inserted in AIS_DISTAL and all distal dendrite sections at density ~8
   mS/cm^2 (per t0019's cited DSGC priors). If a Nav1.6 MOD file is not already available,
   adapt one from the t0019 channel corpus.
2. Kv3 mechanism inserted in AIS_DISTAL and all distal dendrite sections at density ~5
   mS/cm^2.
3. NMDA synapse component restored at both PD and ND BIP terminals with conductance matching
   the Poleg-Polsky 2016 parameter backbone (read from t0008's library asset if available,
   else sourced from the Poleg-Polsky 2016 paper).

Hold the t0037 null-GABA sweet spot of 4 nS as the base parameter per t0038's correction. Keep
the 12-direction × 10-trial sweep protocol identical to t0022 / t0037 / t0039 so results are
directly comparable.

Pass criterion (both must hold):

* Peak firing rate in [40, 80] Hz at V_rest = -60 mV.
* Primary DSI within +/- 0.1 of the t0037 anchor of 0.429 at the 1.0x baseline diameter.

## Scope

* Local CPU only. No remote compute. ~6 hours wall-clock including MOD recompilation.
* Produce a library asset with the modified model plus a baseline 12-direction x 10-trial
  sweep at V_rest = -60 mV, GABA = 4 nS.
* Write a test harness that can be reused by t0044 for the diameter sweep.

## Out of Scope

* Nav1.2 and Kv1 (part of the fuller S-0019-03 scope, deferred).
* Morphology sweeps (covered by t0044 which uses this task's output as substrate).
* V_rest sweep (covered by t0026 on the prior testbed; a re-run on the new testbed could be a
  follow-up suggestion emitted from this task).

## Deliverables

* `assets/library/modeldb_189347_dsgc_t0043/` — library asset with the modified model,
  compiled MOD files, and baseline sweep driver.
* Baseline 12-direction x 10-trial sweep CSV under `results/`.
* Tuning curve (Cartesian and polar) under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections
  and an explicit Pass/Fail verdict against both criteria above.
* `results/metrics.json` with baseline primary DSI, vector-sum DSI, preferred direction, peak
  Hz, null Hz, and a boolean `peak_rate_pass` and `dsi_preserved_pass`.
* If Pass: the library asset is fit for use as t0044's substrate. If Fail: emit a suggestion
  for a follow-up calibration task (BIP burst rate + AMPA scale; see S-0040-01 or analogous)
  and stop before t0044.

## Anticipated Risks

* Nav1.6 MOD files in the t0019 corpus may not compile under NEURON 8.2.7 without adaptation;
  budget time for MOD debugging.
* Adding Nav1.6 may push the cell into runaway firing if the Kv3 density is too low; tune Kv3
  first, Nav1.6 second.
* Restoring NMDA may break the t0037 4 nS sweet spot by over-exciting at the null direction;
  if this happens, emit a follow-up suggestion to repeat a GABA sweet-spot search on the new
  testbed.

</details>

<details>
<summary>❌ 0044 — <strong>Schachter 2010 re-test via 7-diameter sweep on t0043 at
GABA = 4 nS</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0044_schachter_retest_on_t0043` |
| **Status** | cancelled |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md), [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md), [`t0043_nav16_kv3_nmda_restoration_t0022`](../../../overview/tasks/task_pages/t0043_nav16_kv3_nmda_restoration_t0022.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0002-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Schachter 2010 re-test via 7-diameter sweep on t0043 at GABA = 4 nS](../../../overview/tasks/task_pages/t0044_schachter_retest_on_t0043.md) |
| **Task folder** | [`t0044_schachter_retest_on_t0043/`](../../../tasks/t0044_schachter_retest_on_t0043/) |

# Schachter 2010 Re-Test on t0043 Substrate

## Status: BLOCKED (2026-04-24)

Blocked pending completion of **t0046_reproduce_poleg_polsky_2016_exact** and of this task's
upstream dependency **t0043** (which is itself blocked on t0046). This task depends on the
t0043 substrate. Reassess after t0046 merges and t0043's block is reviewed.

## Source Suggestion

S-0002-02 (paired active-vs-passive dendrite experiment to reproduce Schachter 2010 DSI gain
~0.3 -> ~0.7).

## Motivation

Three independent diameter sweeps across two testbeds have failed to show Schachter 2010's
predicted active-amplification signature:

* t0030 on t0022 at GABA = 12 nS: slope +0.008 (p=0.177), DSI pinned at 1.000 (deterministic
  schedule saturates the metric).
* t0035 on t0024 (AR(2) stochastic) at paper-default GABA: slope +0.004 (p=0.88), flat.
* t0039 on t0022 at GABA = 4 nS (t0037 sweet spot): slope -0.034 (p=0.008), monotonic decline
  consistent with passive filtering rather than the predicted concave-down interior peak.

One candidate explanation, surfaced in brainstorm session 8's cross-task audit, is that lumped
HHst lacks the distal Nav1.6 and Kv3 channels needed to recruit the regenerative
threshold-crossing regime Schachter 2010 relies on. t0043 fixes that inventory and restores
NMDA. If Schachter 2010 is correct and our previous null results were confounded by the
channel gap, the same 7-diameter sweep on the t0043 substrate should show a concave-down
DSI-vs-diameter curve with a significant negative quadratic coefficient.

If the curve is still monotonic after t0043, we can close the Schachter 2010 hypothesis on the
Poleg-Polsky-derived morphology and commit to a passive-filtering framing for the t0033
optimiser.

## Objective

Run a 7-diameter distal-section sweep (multipliers 0.5, 0.67, 0.85, 1.0, 1.2, 1.5, 2.0 — same
grid as t0030, t0039, t0035) on the t0043 library asset at GABA = 4 nS. Protocol matches
t0039: 12 directions x 10 trials per direction per multiplier, V_rest = -60 mV. Primary
outcome is the DSI-vs-diameter curve shape; fit both linear and quadratic models and report
the coefficients with p-values.

Pass criterion (Schachter 2010 signature recovered):

* Quadratic fit coefficient significantly negative (p < 0.05) with a peak at an interior
  multiplier (between 0.6 and 1.5).

Fail criterion (Schachter hypothesis rejected on Poleg-Polsky morphology):

* Monotonic (linear fit significant, quadratic not significant), or no significant trend. In
  this case, emit a suggestion to formally close S-0002-02 and to add a clarifying note to the
  t0033 plan recommending the passive-filtering framing.

## Scope

* Local CPU only. No remote compute. ~8 hours wall-clock.
* Use the t0043 library asset. Do not modify the channel inventory; this is a pure morphology
  sweep.
* Keep per-trial stochasticity identical to t0039 so the results are directly comparable.

## Out of Scope

* Nav ablation (covered by S-0029-02, currently medium priority).
* Length-axis sweep on the t0043 substrate (possible follow-up, not this task).
* Re-running on t0024 (possible follow-up under S-0039-01).

## Deliverables

* 7-diameter tuning-curve CSVs under `results/`.
* Overlay plot of DSI-vs-diameter with linear and quadratic fits under `results/images/`.
* `results/results_summary.md` and `results/results_detailed.md` with the standard sections
  and an explicit Schachter-recovered / Schachter-rejected verdict.
* `results/metrics.json` with the linear slope, quadratic coefficient, and their p-values,
  plus primary DSI, vector-sum DSI, and peak Hz at each multiplier.
* `results/compare_literature.md` explicitly comparing the recovered (or absent) curvature
  against Schachter 2010 and the passive-filtering prediction.

## Anticipated Risks

* If t0043 fails its own Pass criterion (peak rate or DSI preservation), do not proceed with
  this task; the substrate is not fit for use.
* Adding Nav1.6 may change the effective preferred direction; re-seed the E-I schedule only if
  the preferred direction has shifted by more than 30 deg from the t0037 40.8 deg anchor.
* Quadratic fits on 7 points are under-powered if noise is high; if the quadratic p-value is
  borderline (0.05 < p < 0.15), emit a suggestion for a denser 11-point sweep rather than
  declaring a verdict.

</details>

## 2026-04-23 (3)

## ✅ Completed

<details>
<summary>✅ 0036 — <strong>Rerun distal-diameter sweep on t0022 with halved
null-GABA</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0036_rerun_t0030_halved_null_gaba` |
| **Status** | completed |
| **Effective date** | 2026-04-23 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0030-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-23T20:56:59Z |
| **End time** | 2026-04-23T22:40:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Rerun distal-diameter sweep on t0022 with halved null-GABA](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Task folder** | [`t0036_rerun_t0030_halved_null_gaba/`](../../../tasks/t0036_rerun_t0030_halved_null_gaba/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0036_rerun_t0030_halved_null_gaba/results/results_detailed.md) |

# Rerun Distal-Diameter Sweep on t0022 with Halved Null-GABA

## Motivation

t0030 (distal-diameter sweep on t0022) produced a **null result** for the Schachter2010 vs
passive-filtering discriminator because **primary DSI was pinned at 1.000 across every
diameter multiplier**. Null-direction firing was exactly 0 Hz under the t0022 E-I schedule at
every diameter, so the peak-minus-null DSI metric had no dynamic range to express either
predicted mechanism slope.

t0030's compare_literature traced the ceiling to `GABA_CONDUCTANCE_NULL_NS = 12 nS` delivered
10 ms before AMPA on null trials — approximately **2× the ~6 nS compound null inhibition
reported by Schachter2010**. Lowering the null-GABA conductance to 6 nS (halved) should leave
enough residual excitation for occasional null-direction spikes while preserving preferred-
direction firing, restoring a measurable primary-DSI signal.

Source suggestion **S-0030-01** (high priority).

## Scope

1. Use the **t0022 DSGC testbed** as-is (channel set, morphology, AIS partition, 12-direction
   protocol, 10 trials per angle) — EXCEPT: set `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` (half of
   the default 12 nS). Preferred-direction GABA stays at its default.
2. Identify distal dendritic sections via t0030's selection rule (HOC leaves on `h.RGC.ON`,
   branch order ≥ 3). COPY the helper into this task's `code/`; no cross-task imports.
3. Sweep 7 distal-diameter multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×) uniformly
   on all distal branches. Same set as t0030.
4. 12-direction moving-bar tuning × 10 trials per angle per diameter = **840 trials total**.
5. Compute **primary DSI (peak-minus-null)** as the operative metric. Unlike t0030, this is
   expected to vary because null-direction firing should now be non-zero. Also compute
   vector-sum DSI and standard secondary metrics.
6. Plot primary DSI vs diameter and classify slope sign:
   - Positive slope → **Schachter2010 active-dendrite amplification** supported
   - Negative slope → **Passive-filtering** supported
   - Flat → mechanism remains ambiguous; diagnose cause (inspect null-firing rate change)

## Approach

* **Local CPU only.** No remote compute, no paid APIs, $0.
* Copy the t0030 code/ workflow verbatim: `paths.py`, `constants.py`, `diameter_override.py`
  (with `identify_distal_sections`), `preflight_distal.py`, `trial_runner_diameter.py`,
  `run_sweep.py`, `analyse_sweep.py`, `classify_slope.py`, `plot_sweep.py`.
* Override the `GABA_CONDUCTANCE_NULL_NS` constant at import time (or expose a CLI override).
  Keep preferred-direction GABA at default.
* Save per-sweep-point tidy CSV incrementally (crash recovery via `fh.flush()`).
* Render DSI-vs-diameter curve, vector-sum DSI curve, polar overlay, null-Hz-vs-diameter curve
  (new diagnostic to confirm the fix is working).

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary including null-Hz-vs-diameter
  baseline (should be non-zero), primary DSI dynamic range, slope classification, mechanism
  attribution.
* `results/results_detailed.md` — per-direction breakdown, slope classification, comparison to
  t0030's pinned-1.000 baseline, discussion of which mechanism the schedule-fixed data
  favours.
* `results/images/dsi_vs_diameter.png`, `vector_sum_dsi_vs_diameter.png`, `polar_overlay.png`,
  `null_hz_vs_diameter.png` (new: confirms the fix desaturates null firing),
  `peak_hz_vs_diameter.png`.
* `results/metrics.json` — DSI primary, vector-sum, peak Hz, null Hz per diameter.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* Local CPU only. Expected runtime: **~2 hours** (extrapolated from t0030's ~115 min on same
  testbed; non-zero null firing doesn't change per-trial wall time meaningfully).
* $0 external cost.

## Measurement

* **Primary metric**: **primary DSI (peak-minus-null)** per diameter — expected to vary now
  that null firing is unpinned.
* **Critical diagnostic**: **null-direction firing rate per diameter** — must be non-zero to
  confirm the GABA change had the intended effect.
* **Secondary**: vector-sum DSI, peak Hz, HWHM, reliability, preferred-direction firing,
  per-direction spike counts, distal peak mV.

## Key Questions

1. Does null-direction firing become non-zero with GABA reduced to 6 nS? (Pre-condition for
   everything else. If it's still 0 Hz, the fix failed; consider a smaller reduction.)
2. With null firing unpinned, what is the primary DSI-vs-diameter slope sign?
3. Does the slope match Schachter2010 (positive), passive filtering (negative), or neither?
4. How does the halved-GABA result on t0022 compare to t0035 (same diameter sweep on t0024)?
   Both should now have unpinned primary DSI — do they agree on the diameter axis being a weak
   discriminator?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC testbed architecture
  and the default `GABA_CONDUCTANCE_NULL_NS = 12 nS` to be overridden.
* **t0030_distal_dendrite_diameter_sweep_dsgc** (completed) — provides the workflow template,
  the `identify_distal_sections` helper (to be copied), and the null-result baseline for
  before/after comparison.

## Scientific Context

Source suggestion **S-0030-01** (high priority). Complementary to S-0029-04 (null-GABA sweep
at fixed length) and S-0029-01 (Poisson + length sweep) — this specifically targets the
diameter axis with a fixed halved-GABA schedule change. Also parallels t0035 (diameter sweep
on t0024) which found flat DSI, allowing a cross-testbed comparison under unpinned primary-DSI
conditions.

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 + t0030 already cover the mechanism
  predictions).
* Include `research-code` — inherit t0030 workflow + t0022 driver.
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `creative-thinking` — if null-Hz rescue works, interpret the slope in the context of
  t0035 (diameter on t0024) result.
* Include `compare-literature` — compare DSI-vs-diameter slope to Schachter2010 /
  passive-filtering predictions AND to t0030 null baseline AND to t0035 flat-on-t0024 result.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0036_rerun_t0030_halved_null_gaba"
> date_completed: "2026-04-23"
> status: "complete"
> ---
> **Results Summary: Rerun Distal-Diameter Sweep on t0022 with Halved Null-GABA**
>
> **Summary**
>
> Reran the t0030 distal-diameter sweep on t0022 with `GABA_CONDUCTANCE_NULL_NS = 6.0 nS`
> (halved from
> 12 nS, matching Schachter2010's compound null inhibition). **The halving was INSUFFICIENT to
> unpin
> null firing**: mean null-direction firing remained exactly **0.0 Hz at every diameter
> multiplier**,
> primary DSI stayed pinned at 1.000, and the classification label is **`flat_partial`**
> (pre-condition gate failed). Vector-sum DSI range 0.579-0.590 (range 0.011, p=0.019 —
> statistically
> significant but practically negligible). The GABA- reduction rescue hypothesis from
> S-0030-01 is
> falsified at 6 nS; follow-up queued to try further reductions (4/2/1 nS) or switch to
> Poisson-noise
> rescue.
>
> **Metrics**

</details>

<details>
<summary>✅ 0035 — <strong>Distal-dendrite diameter sweep on t0024 DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0035_distal_dendrite_diameter_sweep_t0024` |
| **Status** | completed |
| **Effective date** | 2026-04-23 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0027-03` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-23T14:09:57Z |
| **End time** | 2026-04-23T18:00:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Distal-dendrite diameter sweep on t0024 DSGC](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Task folder** | [`t0035_distal_dendrite_diameter_sweep_t0024/`](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/results_detailed.md) |

# Distal-Dendrite Diameter Sweep on t0024 DSGC

## Motivation

The sibling task t0030 ran a distal-diameter sweep on the t0022 DSGC testbed and produced a
**null result** for mechanism discrimination: primary DSI pinned at 1.000 across every
diameter multiplier because t0022's deterministic E-I schedule silences null firing (0 Hz).
Vector-sum DSI fallback produced a flat slope too (p=0.18 on t0030).

The t0024 de Rosenroll 2026 port has fundamentally different biophysics that **fix the t0022
pathology**:

* **AR(2)-correlated stochastic bipolar release** (ρ=0.6) produces non-zero null-direction
  firing. Per t0026's V_rest sweep, t0024's DSI ranges 0.36-0.67 with a measurable 1.9×
  modulation — the discriminator has room to act.
* **No Na-inactivation collapse** at depolarised V_rest (peak firing monotone to 7.6 Hz at
  V_rest = -20 mV).
* **AR(2) noise smooths tuning** (HWHM pinned 65-83° across V_rest).

Running the t0030 diameter sweep on t0024 should therefore produce a **measurable primary DSI
slope** that can actually distinguish the two mechanisms:

* **Schachter2010 active-dendrite amplification**: DSI increases with distal thickening
  because thicker compartments host more Na+ substrate per unit length and amplify
  preferred-direction local spikes more strongly.
* **Passive-filtering alternatives**: DSI decreases with distal thickening because thicker
  dendrites have lower input impedance and less local depolarisation per unit synaptic
  current, damping the directional contrast.

Covers source suggestion **S-0027-03** (high priority) on the t0024 biophysics. Companion to
t0034 (length sweep on t0024).

## Scope

1. Use the **t0024 de Rosenroll 2026 DSGC port** as-is (no channel modifications, no input
   rewiring). Keep the AR(2) correlation ρ=0.6 at its t0026 V_rest-sweep default.
2. Identify distal dendritic sections (HOC leaves on `h.RGC.ON` arbor). Mirror the selection
   rule from t0030's `diameter_override.py` but **COPY** the helper into this task's
   `code/diameter_override_t0024.py` — no cross-task imports per CLAUDE.md.
3. Sweep distal diameter in **7 values** spanning **0.5× to 2.0×** baseline (0.5, 0.75, 1.0,
   1.25, 1.5, 1.75, 2.0×). Apply the multiplier uniformly to all distal branches.
4. For each diameter value, run the **standard 12-direction tuning protocol** (12 angles × 10
   trials) and compute **primary DSI** as the operative metric. Also emit vector-sum DSI and
   secondary metrics.
5. Plot primary DSI vs diameter and classify slope sign: positive (Schachter2010 active),
   negative (passive filtering), flat (neither or schedule-dominated).

## Approach

* **Local CPU only.** No remote compute, no paid API.
* Reuse the t0024 port code at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/` (the
  de_rosenroll_2026_port library is registered and t0024's driver is the model reference).
* Copy the t0030 workflow template: `paths.py`, `constants.py`, `diameter_override.py` (with
  `identify_distal_sections`), `preflight_distal.py`, `trial_runner_diameter.py`,
  `run_sweep.py`, `analyse_sweep.py`, `classify_slope.py`, and `plot_sweep.py`.
* Save per-sweep-point data to `results/data/sweep_results.csv` (incremental checkpoint) and
  per-diameter tuning curves to `results/data/per_diameter/*.csv`.
* Render DSI-vs-diameter chart at `results/images/dsi_vs_diameter.png` plus secondary
  diagnostic plots.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-diameter
  slope sign and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each diameter
  value, slope classification, mechanism attribution (Schachter2010 vs passive filtering),
  comparison to t0030's null result.
* `results/images/dsi_vs_diameter.png` — primary DSI-vs-diameter slope.
* `results/images/vector_sum_dsi_vs_diameter.png` — vector-sum DSI as secondary diagnostic.
* `results/images/polar_overlay.png` — 12-direction polar overlay across all 7 diameters.
* `results/metrics.json` — registered per-diameter DSI metrics.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* **Local CPU only**; no GPU.
* **Expected runtime: 2-4 hours.** The per-(angle, trial) wall time on t0024 is **~12 s** (per
  t0026's V_rest-sweep baseline), vs t0022's ~3.8 s. Full sweep = 7 × 12 × 10 = 840 trials ≈
  **~168 min** at 12 s/trial, plus overhead. Thinner diameters will run slower due to
  increased axial resistance (same behaviour observed on t0030).
* **$0 external cost.**

## Measurement

* **Primary metric**: **primary DSI (peak-minus-null)** at each diameter value. Unlike t0030,
  this is expected to vary because t0024 has non-zero null-direction firing.
* **Secondary**: vector-sum DSI (sanity cross-check), peak Hz, null Hz, HWHM, reliability,
  preferred-direction firing rate, per-direction spike counts, peak voltage at a reference
  distal compartment (to confirm impedance changes).

## Key Questions

1. Is the primary DSI-vs-diameter slope positive (Schachter2010), negative (passive
   filtering), or flat?
2. If positive, is the slope consistent with Na-channel-density amplification as predicted by
   Schachter2010?
3. If negative, does preferred-direction firing drop alongside DSI (general damping) or does
   only the null-direction rate change (selective mechanism)?
4. Does t0024's AR(2) noise broaden the HWHM enough to mask the mechanism signal, or does the
   primary-DSI trend survive the noise floor?
5. How do t0024 and t0022 compare under identical sweep protocols? A measurable slope on t0024
   while t0030 was flat would confirm that the pinned-DSI pathology was the culprit.

## Dependencies

* **t0024_port_de_rosenroll_2026_dsgc** (completed) — provides the DSGC port with AR(2)
  stochastic release.
* **t0030_distal_dendrite_diameter_sweep_dsgc** (completed) — provides the workflow template,
  the `identify_distal_sections` helper (to be copied, not imported), and the null-result
  baseline for comparison.

## Scientific Context

Source suggestion **S-0027-03** (high priority) originally planned for t0022 and executed as
t0030. This task re-runs the same experiment on t0024 specifically because t0024's stochastic
release restores non-zero null firing and therefore makes the primary DSI discriminator
meaningful. Companion to **t0034** (length sweep on t0024).

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 synthesis already covered the mechanism
  predictions; t0030 already surveyed the prior code).
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `research-code` — need to read the t0024 driver and the t0030 workflow pattern.
* Include `creative-thinking` — if the primary-DSI discriminator works on t0024, consider what
  schedule-level properties t0022 would need to adopt to recover sensitivity.
* Include `compare-literature` — compare the t0024 DSI-vs-diameter slope to Schachter2010 and
  passive-filtering predictions **and** to the t0030 null result.
* **Can be executed in parallel with t0034 in a separate worktree.**

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0035_distal_dendrite_diameter_sweep_t0024"
> date_completed: "2026-04-23"
> status: "complete"
> ---
> **Results Summary: Distal-Dendrite Diameter Sweep on t0024 DSGC**
>
> **Summary**
>
> Swept distal-dendrite diameter across seven multipliers (0.5×-2.0× baseline) on the t0024 de
> Rosenroll DSGC port under the standard 12-direction × 10-trial moving-bar protocol (840
> trials
> total). **DSI-vs-diameter slope is flat** (slope 0.0041 per log2(multiplier), **p=0.8808**,
> range
> across extremes -0.0237). **Neither Schachter2010 (predicted positive slope) nor passive
> filtering
> (predicted negative slope) is supported.** Primary DSI range 0.680-0.808 — measurable
> (unlike
> t0030's pinned 1.000 on t0022) but with no mechanism-driven trend. Contrasts sharply with
> sibling
> t0034 (length sweep on same t0024 port) which showed a statistically significant
> non-monotonic
> negative slope (p=0.038): **length modulates DSI on t0024, diameter does not.**
>
> **Metrics**

</details>

<details>
<summary>✅ 0034 — <strong>Distal-dendrite length sweep on t0024 DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0034_distal_dendrite_length_sweep_t0024` |
| **Status** | completed |
| **Effective date** | 2026-04-23 |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0027-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-23T10:07:02Z |
| **End time** | 2026-04-23T14:05:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Distal-dendrite length sweep on t0024 DSGC](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Task folder** | [`t0034_distal_dendrite_length_sweep_t0024/`](../../../tasks/t0034_distal_dendrite_length_sweep_t0024/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0034_distal_dendrite_length_sweep_t0024/results/results_detailed.md) |

# Distal-Dendrite Length Sweep on t0024 DSGC

## Motivation

The sibling task t0029 ran a distal-length sweep on the t0022 DSGC testbed and produced a
**null result** for mechanism discrimination: primary DSI (peak-minus-null) pinned at 1.000
across every length multiplier because t0022's deterministic E-I schedule silences null firing
(0 Hz). The vector-sum DSI fallback also produced a flat slope (p=0.18 on t0029).

The t0024 de Rosenroll 2026 port has fundamentally different biophysics that **fix the t0022
pathology**:

* **AR(2)-correlated stochastic bipolar release** (ρ=0.6) produces non-zero null-direction
  firing. Per t0026's V_rest sweep, t0024's DSI ranges 0.36-0.67 with a measurable 1.9×
  modulation — the discriminator has room to act.
* **No Na-inactivation collapse** at depolarised V_rest (peak firing monotone to 7.6 Hz at
  V_rest = -20 mV).
* **AR(2) noise smooths tuning** (HWHM pinned 65-83° across V_rest).

Running the t0029 length sweep on t0024 should therefore produce a **measurable primary DSI
slope** that can actually distinguish the two mechanisms:

* **Dan2018 passive transfer-resistance weighting**: DSI increases monotonically with distal
  length (longer distal dendrites → steeper TR gradient → stronger directional weighting).
* **Sivyer2013 dendritic-spike branch independence**: DSI saturates (plateau) once distal
  branches clear local spike threshold; further lengthening adds no DSI.

Covers source suggestion **S-0027-01** (high priority) on the t0024 biophysics. Companion to
t0035 (diameter sweep on t0024).

## Scope

1. Use the **t0024 de Rosenroll 2026 DSGC port** as-is (no channel modifications, no input
   rewiring). Keep the AR(2) correlation ρ=0.6 at its t0026 V_rest-sweep default.
2. Identify distal dendritic sections (HOC leaves on `h.RGC.ON` arbor). Mirror the selection
   rule from t0029's `length_override.py:37-52` but **COPY** the helper into this task's
   `code/length_override_t0024.py` — no cross-task imports per CLAUDE.md.
3. Sweep distal length in **7 values** spanning **0.5× to 2.0×** baseline (0.5, 0.75, 1.0,
   1.25, 1.5, 1.75, 2.0×). Apply the multiplier uniformly to all distal branches.
4. For each length value, run the **standard 12-direction tuning protocol** (12 angles × 10
   trials) and compute **primary DSI** as the operative metric. Also emit vector-sum DSI and
   secondary metrics as t0029 did.
5. Plot primary DSI vs length and classify the curve shape: monotonic (favours Dan2018),
   saturating (favours Sivyer2013), or non-monotonic (neither or kinetic-tiling).

## Approach

* **Local CPU only.** No remote compute, no paid API.
* Reuse the t0024 port code at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/` (the
  de_rosenroll_2026_port library is registered and t0024's driver is the model reference).
* Copy the t0029 workflow template: `paths.py`, `constants.py`, `length_override.py` (with
  `identify_distal_sections`), `preflight_distal.py`, `trial_runner_length.py`,
  `run_sweep.py`, `analyse_sweep.py`, `classify_shape.py` (monotonic / saturating /
  non-monotonic), and `plot_sweep.py`.
* Save per-sweep-point data to `results/data/sweep_results.csv` (incremental checkpoint) and
  per-diameter tuning curves to `results/data/per_length/*.csv`.
* Render DSI-vs-length chart at `results/images/dsi_vs_length.png` plus secondary diagnostic
  plots.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-length
  curve shape and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each length
  value, curve-shape classification, mechanism attribution (Dan2018 vs Sivyer2013), comparison
  to t0029's null result.
* `results/images/dsi_vs_length.png` — primary DSI-vs-length curve.
* `results/images/vector_sum_dsi_vs_length.png` — vector-sum DSI as secondary diagnostic.
* `results/images/polar_overlay.png` — 12-direction polar overlay across all 7 lengths.
* `results/metrics.json` — registered per-length DSI metrics.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* **Local CPU only**; no GPU.
* **Expected runtime: 2-4 hours.** The per-(angle, trial) wall time on t0024 is **~12 s** (per
  t0026's V_rest-sweep baseline), vs t0022's ~3.8 s. Full sweep = 7 × 12 × 10 = 840 trials ≈
  **~168 min** at 12 s/trial, plus overhead.
* **$0 external cost.**

## Measurement

* **Primary metric**: **primary DSI (peak-minus-null)** at each length value. Unlike t0029,
  this is expected to vary because t0024 has non-zero null-direction firing.
* **Secondary**: vector-sum DSI (sanity cross-check), peak Hz, null Hz, HWHM, reliability,
  preferred-direction firing rate, per-direction spike counts.

## Key Questions

1. Is primary DSI monotonically increasing with distal length (Dan2018), saturating
   (Sivyer2013), or non-monotonic (neither)?
2. At what length does saturation occur (if any)?
3. Does the t0024 AR(2) noise broaden the HWHM enough to mask the mechanism signal, or does
   the primary-DSI trend survive the noise floor?
4. How do the t0024 and t0022 results compare under identical sweep protocols? A matched DSI
   trend on both would strengthen the mechanism claim; divergent trends would indicate that
   t0022's pinned primary DSI masked a real effect.

## Dependencies

* **t0024_port_de_rosenroll_2026_dsgc** (completed) — provides the DSGC port with AR(2)
  stochastic release.
* **t0029_distal_dendrite_length_sweep_dsgc** (completed) — provides the workflow template,
  the `identify_distal_sections` helper (to be copied, not imported), and the null-result
  baseline for comparison.

## Scientific Context

Source suggestion **S-0027-01** (high priority) originally planned for t0022 and executed as
t0029. This task re-runs the same experiment on t0024 specifically because t0024's stochastic
release restores non-zero null firing and therefore makes the primary DSI discriminator
meaningful. Companion to **t0035** (diameter sweep on t0024).

## Execution Notes

* Follow standard `/execute-task` flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 synthesis already covered the mechanism
  predictions; t0029 already surveyed the prior code).
* Skip `setup-machines` / `teardown` (local CPU only).
* Include `research-code` — need to read t0024 driver and t0029's workflow pattern.
* Include `creative-thinking` — if the primary-DSI discriminator works on t0024, consider
  whether t0022's null result was due to schedule-only dominance or a deeper pathology.
* Include `compare-literature` — compare the t0024 DSI-vs-length curve to Dan2018 and
  Sivyer2013 predictions **and** to the t0029 null result.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0034_distal_dendrite_length_sweep_t0024"
> date_completed: "2026-04-23"
> status: "complete"
> ---
> **Results Summary: Distal-Dendrite Length Sweep on t0024 DSGC**
>
> **Summary**
>
> Swept distal-dendrite length across seven multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×,
> 1.75×, 2.0×
> baseline) on the t0024 de Rosenroll DSGC port under the standard 12-direction × 10-trial
> moving-bar
> protocol (840 trials total). **Unlike t0029's null result on t0022, primary DSI varies
> measurably on
> t0024** (range 0.545-0.774) because AR(2) stochastic release produces non-zero null firing.
> The
> slope is **-0.1259 per unit multiplier (p=0.038)** — a statistically significant
> **negative** trend,
> classified as **non_monotonic** overall. Neither Dan2018 (predicted monotonic increase) nor
> Sivyer2013 (predicted saturating plateau) is supported; the data leans toward passive cable
> filtering past an optimal electrotonic length, with superimposed local-spike-failure
> transitions at
> 1.5× and 2.0×.
>

</details>

## 2026-04-22 (6)

## ⏹ Not Started

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>

## ✅ Completed

<details>
<summary>✅ 0033 — <strong>Plan DSGC morphology + VGC DSI optimisation; estimate
Vast.ai GPU budget</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0033_plan_dsgc_morphology_channel_optimisation` |
| **Status** | completed |
| **Effective date** | 2026-04-22 |
| **Dependencies** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-04-22T12:26:07Z |
| **End time** | 2026-04-22T15:40:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Plan DSGC morphology + VGC DSI optimisation; estimate Vast.ai GPU budget](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Task folder** | [`t0033_plan_dsgc_morphology_channel_optimisation/`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/results_detailed.md) |

# Plan DSGC Morphology + Voltage-Gated Channel DSI Optimisation; Estimate Vast.ai GPU Budget

## Motivation

The project's long-term ambition, implied by project research questions RQ1, RQ2, and RQ4, is
a joint optimisation over DSGC dendritic morphology and voltage-gated channel (VGC)
combinations that maximises the direction-selectivity index (DSI). No task to date has
attempted such a large-scale joint sweep; every completed experiment to date has varied only
one axis at a time (V_rest, distal length, distal diameter) on a fixed morphology and a fixed
channel set inherited from the Poleg-Polsky 2026 port.

Before committing the project budget to a joint optimisation, we need a feasibility plan and a
defensible compute-budget estimate. This task produces exactly that plan. It does **not**
launch the optimisation and does **not** create a child optimiser task. The optimisation
itself, if approved, will be spawned from a future brainstorm session after this plan lands.

## Scope

**In scope**:

* Synthesise existing methodology for compartmental-model parameter optimisation from the
  downloaded paper corpus in `tasks/*/assets/paper/` and `assets/paper/` (as surfaced by
  `aggregate_papers`). No internet search.
* Enumerate the parameter set that the future optimisation would vary, in two groups:
  1. **Morphology** — variables taken from the Poleg-Polsky 2026 backbone as exposed by the
     t0024 port and the channel-modular AIS architecture of the t0022 testbed. Include all
     per-section geometry that Poleg-Polsky 2026 varies, plus explicit morphology knobs
     (per-branch length, diameter, branch order, arbor-asymmetry summary statistics)
     identified by t0027.
  2. **Voltage-gated channels** — the top-10 VGC types from the t0019 survey (sourced from
     `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/`).
     For each VGC, enumerate the per-channel biophysical parameters that will be varied
     (typically `gbar`, possibly kinetic shifts).
* Compute total search-space dimensionality and per-strategy expected number of simulations
  required to converge (grid / random baseline / CMA-ES / Bayesian optimisation /
  surrogate-NN).
* Estimate per-simulation wall-time using the empirical baselines recorded by t0026:
  * t0022 deterministic: ~6.0 min / 96 trials ≈ **3.8 s per (angle, trial)**
  * t0024 stochastic AR(2) ρ=0.6: ~11,562 s / 960 trials ≈ **12.0 s per (angle, trial)**
  * Extrapolate per-simulation cost per the 12-angle × trial-count standard protocol.
* Translate wall-time into Vast.ai USD cost across 2-3 representative GPU tiers, using the
  pricing conventions documented in `arf/docs/explanation/remote_machines.md` and the tier
  filters encoded in `arf/scripts/utils/vast_machines.py`. Tiers to consider: RTX 4090, A100
  40 GB, H100 (or the closest available tier). Include the `compute_cap<1200` and
  `cuda_max_good>=12.6` pre-validated filters in the cost derivation.
* Evaluate three compute strategies and produce a wall-time + USD envelope for each:
  1. **CoreNEURON on Vast.ai GPU** (OpenACC/CUDA-accelerated NEURON variant).
  2. **Surrogate NN on Vast.ai GPU** (train a neural-network surrogate from a limited
     CPU-NEURON sample, then optimise on the surrogate; account for training cost, sample
     cost, and transfer/inference cost).
  3. **Vast.ai many-core CPU** (comparator — cost floor assuming stock NEURON).
* Produce a sensitivity analysis: what if per-simulation cost is 0.5×, 1×, or 2× the t0026
  baseline? What if search-strategy sample counts are 0.5×, 1×, or 2× the literature default?
* Recommend the cheapest viable (strategy × Vast.ai GPU tier) combination, with explicit
  caveats on any assumptions that the downloaded corpus did not resolve.

**Out of scope** (explicit):

* Running the optimisation. This task is pure planning.
* Creating the child optimiser task.
* Any internet search.
* Any experimentation on t0022, t0024, or other existing ports.
* Multi-objective optimisation. The future plan is for single-objective DSI maximisation only.
  Other criteria (information, energy, size, Cajal's cytoplasm minimisation) are noted but are
  explicitly not costed in this task.
* Variation on the presynaptic side (bipolar / SAC input schedule and kinetics are held
  fixed).

## Approach

1. **Corpus read.** Aggregate all papers via `aggregate_papers --format json --detail full`
   and filter to summaries relevant to compartmental-model optimisation, surrogate modelling,
   CoreNEURON / GPU NEURON, and active-dendrite parameter reduction. Expect strong hits from
   t0015 (cable theory), t0016 (dendritic computation), t0019 (VGCs), t0027 (morphology-DS).
2. **Parameter enumeration.** Read the t0022 code under
   `tasks/t0022_modify_dsgc_channel_testbed/code/` and the t0024 code under
   `tasks/t0024_port_de_rosenroll_2026_dsgc/code/` to identify every mechanism instantiated
   across `SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, and `THIN_AXON`.
   Tabulate which parameters would vary under the joint optimisation and which are held fixed.
3. **Top-10 VGC selection.** Read the t0019 answer asset at
   `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/full_answer.md`
   and commit to a canonical top-10 list with biophysical-parameter counts per channel.
4. **Search-space arithmetic.** Under each strategy, compute dimensionality and expected
   simulation count. Record all assumptions explicitly.
5. **Vast.ai pricing lookup.** Use `arf/scripts/utils/vast_machines.py` (read the library; no
   provisioning calls) to identify current tier pricing and filter constraints. Document the
   snapshot date in the plan.
6. **Cost model.** For each (strategy × tier) pair: expected simulations × per-sim wall-time /
   parallelism factor × hourly rate → total $.
7. **Sensitivity.** Produce a 3 × 3 sensitivity table (per-sim cost × sample-count
   multipliers).
8. **Answer asset.** Produce one answer asset: *"What is the Vast.ai GPU cost and recommended
   organisation of a joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation
   task?"*.
9. **Results output.** `results_detailed.md` contains parameter-count tables,
   search-space-size tables, per-sim wall-time, cost tables, and sensitivity.
   `results_summary.md` states the headline recommended (strategy, tier, total $) with
   confidence band.

## Dependencies

* `t0002_literature_survey_dsgc_compartmental_models` — compartmental-model methodology
  priors.
* `t0019_literature_survey_voltage_gated_channels` — source of the top-10 VGC list.
* `t0022_modify_dsgc_channel_testbed` — architecture that the future optimisation would vary.
* `t0024_port_de_rosenroll_2026_dsgc` — Poleg-Polsky 2026 parameter backbone.
* `t0026_vrest_sweep_tuning_curves_dsgc` — empirical per-simulation wall-time baselines.
* `t0027_literature_survey_morphology_ds_modeling` — morphology-variable taxonomy.

## Expected Assets

One answer asset, matching `expected_assets = {"answer": 1}`:

* `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/` — with
  `details.json`, `short_answer.md`, and `full_answer.md`. The short answer must state the
  recommended (strategy, Vast.ai GPU tier, headline USD budget, and confidence) in 2-5
  sentences. The full answer must document methodology, parameter enumeration, cost model,
  sensitivity, and limitations.

No library, model, dataset, paper, or prediction assets are produced by this task.

## Compute and Budget

* Local CPU only. No remote machines. No paid APIs.
* $0.00 estimated task cost.
* Task budget limit: project default ($1.00).

## Measurement

This is not an experimental task; no registered metrics are measured. `metrics.json` will be
`{}`. Decision-level quantities that the task produces (parameter counts, search-space sizes,
cost estimates) live in `results_detailed.md` tables and in the answer asset, not in
`metrics.json`.

## Key Questions

1. How many free parameters does the joint morphology + top-10 VGC optimisation have under
   reasonable parameterisation choices?
2. What is the expected number of simulations required to converge under grid / random /
   CMA-ES / Bayesian / surrogate-NN strategies?
3. What is the per-simulation wall-time on (a) CoreNEURON on Vast.ai GPU, (b) surrogate NN on
   Vast.ai GPU, and (c) Vast.ai many-core CPU, extrapolated from the t0026 baselines?
4. What is the total Vast.ai USD cost for each (strategy × tier) combination?
5. Which (strategy × tier) combination minimises cost while remaining technically viable, and
   what are the key assumptions behind the ranking?
6. Under 0.5×, 1×, 2× perturbations to per-simulation cost and sample count, does the
   recommended combination still win?

## Execution Notes

* Follow the standard `/execute-task` flow: `create-branch`, `check-deps`, `init-folders`,
  `research-papers`, `planning`, `implementation`, `results`, `suggestions`, `reporting`.
* Skip `research-internet` (researcher constraint: downloaded papers only).
* Skip `research-code` unless corpus analysis reveals code assets inside our `assets/library/`
  that are directly relevant to parameter-count justification.
* Skip `setup-machines` / `teardown` (local CPU only for this task).
* Skip `compare-literature` (this task IS a literature synthesis; the comparison happens in
  the answer asset).
* Researcher constraint — **do not** create the future optimiser task from within this task.
  That decision is deferred to a future brainstorm session.

## Scientific Context

No single source suggestion covers this task. It was commissioned by the researcher directly
in brainstorm session 7 (t0032) as a parallel planning thread to the morphology-sweep wave
(t0029-t0031).

**Results summary:**

> **Results Summary: Plan DSGC Morphology + VGC DSI Optimisation on Vast.ai GPU**
>
> **Summary**
>
> Produced a full feasibility plan and Vast.ai GPU cost envelope for a future joint DSGC
> morphology
> + top-10 voltage-gated channel DSI-maximisation optimisation. Committed parameter count:
> **25 free
> parameters tight** (5 Cuntz morphology scalars + 20 per-region channel gbar) with a
> **45-parameter
> rich** upper-bound envelope. Recommended (strategy × compute mode × GPU tier):
> **Surrogate-NN-assisted GA × Surrogate-NN-GPU × RTX 4090 × tight parameterisation** →
> central
> estimate **$50.54**, sensitivity band **$23-$119** under 0.5×/1×/2× perturbations to per-sim
> cost
> and sample count.
>
> **Metrics**
>
> * **Parameter count (tight committed)**: **25** free parameters (5 Cuntz morphology + 20
>   per-region
> VGC gbar); rich upper-bound envelope: **45** parameters.
> * **Expected simulation counts**: random baseline **2,000**; CMA-ES **1,300**; Bayesian
>   optimisation
> **500**; surrogate-NN-GA **18,500** (5,000 NEURON training samples + 13,500 GA evaluations
> on the
> surrogate); grid **10^25** (reported as infeasibility anchor).
> * **Per-simulation wall-time (empirical, from t0026)**: **456 s** deterministic, **1,440 s**

</details>

<details>
<summary>✅ 0032 — <strong>Brainstorm results session 7</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0032_brainstorm_results_7` |
| **Status** | completed |
| **Effective date** | 2026-04-22 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md), [`t0028_brainstorm_results_6`](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-22T11:45:00Z |
| **End time** | 2026-04-22T12:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 7](../../../overview/tasks/task_pages/t0032_brainstorm_results_7.md) |
| **Task folder** | [`t0032_brainstorm_results_7/`](../../../tasks/t0032_brainstorm_results_7/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0032_brainstorm_results_7/results/results_detailed.md) |

# Brainstorm Results Session 7

## Motivation

Seventh strategic brainstorming session. Run on 2026-04-22, a few hours after t0028
(brainstorm session 6) merged and queued the morphology-sweep wave (t0029, t0030, t0031). The
researcher opened a second, parallel planning thread focused on a much larger future ambition:
a joint optimisation over DSGC dendritic morphology and the top-10 voltage-gated channel types
to maximise DSI.

The immediate purpose of this session is not to launch that optimisation, but to commission a
planning-and-costing task that answers: *is a full joint optimisation affordable on our
Vast.ai GPU budget, and how should it be organised?*

## Scope

* Review project state after the t0028 merge: 28 tasks completed, 1 in progress (t0029), 2 not
  started (t0030, t0031), 1 intervention_blocked (t0023); 107 uncovered suggestions (36 high /
  55 medium / 16 low); $0.00 / $1.00 budget used.
* Summarise t0026 (V_rest sweep) and t0027 (morphology-DS synthesis) as the strategic context
  the researcher is reacting to.
* Decide whether to open a parallel planning thread during the morphology-sweep wave.
* Decide on a single new task: a feasibility-and-costing plan for a large joint morphology +
  VGC DSI-maximisation optimisation on Vast.ai GPU.
* Capture the researcher's constraints (no internet research, active dendritic conductances,
  presynaptic inputs fixed, single-objective DSI, do not create the child optimiser task
  itself).

## Researcher Decisions

* **Open a parallel planning thread**: yes. Do not wait for the morphology-sweep wave (t0029,
  t0030, t0031) to complete.
* **New task**: exactly one task, scoping and costing a future joint morphology + top-10 VGC
  DSI-maximisation optimisation. The task is a **planner, not an optimiser** — it must not
  launch any optimisation runs.
* **Research scope**: downloaded paper corpus only. No internet search.
* **Biophysical assumptions** (locked in for the plan): active dendritic conductances,
  Poleg-Polsky 2026 parameter backbone, top-10 voltage-gated channel types sourced from t0019,
  presynaptic inputs held fixed.
* **Objective**: DSI only. Future criteria (information content, energy, size constraints,
  Cajal's cytoplasm minimisation) are noted but explicitly out of scope for this plan.
* **Compute target**: Vast.ai GPU pricing as the primary cost reference. Evaluate
  CoreNEURON-on-GPU, surrogate-NN-on-GPU, and a Vast.ai many-core CPU comparator. Pick the
  cheapest viable strategy × tier.
* **Suggestion backlog**: no rejections or reprioritisations this session. Pruning deferred.
* **Task updates**: none.

## New Task Created

The session authorised one child task, created via `/create-task` immediately after this
brainstorm-results folder was scaffolded. Task index is auto-assigned as 33 (strictly greater
than 32 per the ordering invariant).

* **t0033** — Plan DSGC morphology + top-10 voltage-gated channel DSI-maximisation
  optimisation task; synthesise methodology from the downloaded paper corpus only; enumerate
  parameter counts and search-space sizes; estimate Vast.ai GPU wall-time and USD cost for 2-3
  search strategies × 2-3 GPU tiers; recommend the cheapest viable combination. Deliverable
  includes an answer asset capturing the cost envelope. Planning only — no optimiser runs, no
  child optimiser task spawned from this plan. Local CPU only, $0.

## Suggestion Cleanup

Zero suggestions rejected or reprioritised. Pruning of stale high-priority suggestions from
the t0015-t0019 literature surveys was raised in the AI's reassessment but the researcher did
not authorise any action this session.

## Task Updates

None. t0023 (Hanson2019 port) remains `intervention_blocked`. t0029 remains `in_progress` in
its own worktree. t0030 and t0031 remain `not_started`.

## Expected Assets

This brainstorm session produces no assets beyond the brainstorm-results task folder and its
downstream child task. `expected_assets` is `{}`.

## Dependencies

All 27 completed tasks up through t0028. t0029, t0030, t0031 are excluded because they are not
yet completed.

**Results summary:**

> **Results Summary: Brainstorm Session 7**
>
> **Summary**
>
> Seventh strategic brainstorm, run a few hours after the t0028 merge while t0029
> (distal-length
> sweep) is still in_progress. One new task approved: **t0033** — a planner-and-cost-estimator
> for a
> future joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation optimisation,
> scoped
> against the downloaded paper corpus only and anchored on Vast.ai GPU pricing. No suggestions
> rejected or reprioritised; t0023 remains intervention_blocked.
>
> **Session Overview**
>
> Date: 2026-04-22. Duration: ~45 min. Context: the morphology-sweep wave (t0029, t0030,
> t0031) is
> already queued from t0028 and is unlikely to change the feasibility of a large-scale joint
> optimisation. The researcher therefore opened a parallel planning thread to assess whether a
> full
> morphology + channel sweep is affordable on the project's Vast.ai GPU budget before the
> morphology-sweep wave returns. The session produced exactly one task (t0033) whose
> deliverable is a
> plan and cost estimate, explicitly not the optimiser itself.
>
> **Decisions**

</details>

<details>
<summary>✅ 0030 — <strong>Distal-dendrite diameter sweep on t0022 DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0030_distal_dendrite_diameter_sweep_dsgc` |
| **Status** | completed |
| **Effective date** | 2026-04-22 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0027-03` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-22T20:08:09Z |
| **End time** | 2026-04-22T22:00:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Distal-dendrite diameter sweep on t0022 DSGC](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Task folder** | [`t0030_distal_dendrite_diameter_sweep_dsgc/`](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/results/results_detailed.md) |

# Distal-Dendrite Diameter Sweep on t0022 DSGC

## Motivation

The t0027 literature synthesis identified distal-dendrite diameter as a second-axis
discriminator between competing DS mechanisms that are individually consistent with our
current t0022 tuning data (DSI peak 0.6555 at V_rest = -60 mV, 15 Hz input):

* **Schachter2010 active-dendrite amplification** predicts DSI increases with distal
  thickening, because thicker distal compartments host more Na+ channel substrate per unit
  length and therefore amplify preferred-direction local spikes more strongly than passive
  EPSPs.
* **Passive-filtering alternatives** predict DSI decreases with distal thickening, because
  thicker dendrites have lower input impedance and less local depolarisation per unit synaptic
  current, so the directional contrast from asymmetric input patterns is damped.

A single-parameter sweep of distal diameter on the t0022 testbed, measuring DSI only, will
discriminate these mechanisms — a positive slope favours Schachter2010 active dendrites; a
negative slope favours passive filtering. Source suggestion **S-0027-03** (high priority) from
the t0027 literature synthesis.

## Scope

1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
2. Identify distal dendritic sections (tip compartments at branch order ≥ 3) in the
   morphology.
3. Sweep distal diameter in at least 7 values spanning from 0.5× to 2.0× the baseline diameter
   (e.g., 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0×). Apply the multiplier to all distal branches
   uniformly.
4. For each diameter value, run the standard 12-direction tuning protocol (15 Hz preferred-
   direction input) and compute DSI.
5. Plot DSI vs diameter and classify slope sign: positive (active-dendrite amplification),
   negative (passive filtering), flat (neither).

## Approach

* Local CPU only. No remote compute, no paid API.
* Reuse t0022 testbed code — copy relevant scripts into this task's `code/` directory.
* Vary the `diam` attribute on distal compartments by the sweep multiplier in a single
  experiment driver script.
* Use the existing tuning-curve scoring library from t0012 for DSI computation (consistent
  with t0022/t0026).
* Save per-sweep-point results to `results/data/sweep_results.csv`.
* Generate DSI-vs-diameter chart at `results/images/dsi_vs_diameter.png`.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-diameter
  slope sign and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each diameter
  value, slope sign classification, and discussion of which mechanism the data favours.
* `results/images/dsi_vs_diameter.png` — DSI-vs-diameter plot.
* `results/metrics.json` — DSI values at each diameter point.
* No paper, dataset, library, model, or answer assets produced.

## Compute and Budget

* Local CPU only. Expected runtime: 30-90 minutes.
* $0 external cost.

## Measurement

* Primary metric: **DSI** at each diameter value.
* Secondary (recorded but not primary): per-direction spike counts, preferred-direction firing
  rate, peak voltage at a reference distal compartment (to confirm passive-impedance changes).

## Key Questions

1. Is the DSI-vs-diameter slope positive, negative, or flat?
2. If positive, is the slope consistent with Na+ channel-density amplification as predicted by
   Schachter2010?
3. If negative, does the preferred-direction firing rate drop alongside DSI (consistent with
   general damping) or does only the null-direction rate change?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC morphology and channel
  set including Nav density.

## Scientific Context

Source suggestion **S-0027-03** (high priority). Complementary to t0029 distal-length sweep:
length varies the spatial extent of distal integration, diameter varies the local impedance
and channel substrate. Together they span the two most important biophysical axes highlighted
in the t0027 synthesis.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step.
* Skip `research-papers`, `research-internet` (t0027 synthesis already did this), and
  `setup-machines` / `teardown` (local CPU).
* Include `compare-literature` — compare the DSI-vs-diameter curve to Schachter2010
  predictions.
* Can be executed in parallel with t0029 in a separate worktree.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0030_distal_dendrite_diameter_sweep_dsgc"
> date_completed: "2026-04-22"
> status: "complete"
> ---
> **Results Summary: Distal-Dendrite Diameter Sweep on t0022 DSGC**
>
> **Summary**
>
> Swept distal-dendrite diameter across seven multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×,
> 1.75×, 2.0×
> baseline) on the t0022 DSGC testbed under the standard 12-direction × 10-trial protocol (840
> trials
> total). **Vector-sum DSI is essentially flat** across the 4× diameter range: slope 0.0083
> per
> log2(multiplier), p=0.1773, DSI range 0.635-0.665 across extremes. **Neither the
> Schachter2010
> active-dendrite amplification prediction (positive slope) nor the passive-filtering
> prediction
> (negative slope) is supported** — the t0022 testbed's E-I timing carries DSI almost
> entirely,
> leaving distal diameter with no measurable mechanistic role.
>
> **Metrics**
>

</details>

<details>
<summary>✅ 0029 — <strong>Distal-dendrite length sweep on t0022 DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0029_distal_dendrite_length_sweep_dsgc` |
| **Status** | completed |
| **Effective date** | 2026-04-22 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0027-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-22T10:41:56Z |
| **End time** | 2026-04-22T15:40:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Distal-dendrite length sweep on t0022 DSGC](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Task folder** | [`t0029_distal_dendrite_length_sweep_dsgc/`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/results_detailed.md) |

# Distal-Dendrite Length Sweep on t0022 DSGC

## Motivation

The t0027 literature synthesis identified two published mechanisms that both fit our current
t0022 tuning data (DSI peak 0.6555 at V_rest = -60 mV, 15 Hz input): **Dan2018** passive
transfer- resistance weighting, and **Sivyer2013** dendritic-spike branch independence. The
two mechanisms make divergent predictions about how DSI should change as distal-dendrite
length varies:

* **Dan2018 passive TR**: DSI increases monotonically with distal length, because longer
  distal dendrites create a steeper transfer-resistance gradient from synapse to soma and
  therefore stronger directional weighting of passive EPSPs.
* **Sivyer2013 dendritic spike**: DSI saturates (plateau) once distal branches are long enough
  to independently generate local dendritic spikes; further length increases contribute no
  additional DSI because the spike threshold is already cleared.

A clean single-parameter sweep of distal length on the t0022 testbed, measuring DSI only, will
discriminate between these mechanisms — a monotonic curve favours Dan2018; a saturating curve
favours Sivyer2013. This is the highest-information-gain experiment identified by the t0027
synthesis (suggestion S-0027-01, high priority).

## Scope

1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
2. Identify distal dendritic sections (tip compartments at branch order ≥ 3) in the
   morphology.
3. Sweep distal length in at least 7 values spanning from 0.5× to 2.0× the baseline length
   (e.g., 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0×). Use the same sweep step size for all
   branches.
4. For each length value, run a full 12-direction tuning protocol (standard t0022 protocol
   with 15 Hz preferred-direction input) and compute DSI.
5. Plot DSI vs length and classify the curve shape as monotonic / saturating / non-monotonic.
6. Report the fitted slope (for monotonic), the saturation length (for saturating), or
   describe the qualitative shape (for non-monotonic).

## Approach

* Run locally on CPU only. No remote compute, no paid API.
* Reuse the t0022 testbed code under `tasks/t0022_modify_dsgc_channel_testbed/code/` — copy
  the needed scripts into this task's `code/` directory (per CLAUDE.md rule on cross-task
  imports).
* Vary the `L` attribute (section length) on all distal compartments by the sweep multiplier
  in a single experiment driver script.
* Use the existing tuning-curve scoring library from
  `tasks/t0012_tuning_curve_scoring_loss_library/` to compute DSI consistently with
  t0022/t0026.
* Save per-sweep-point results (DSI, per-direction firing rates) to
  `results/data/sweep_results.csv`.
* Generate a DSI-vs-length chart and save to `results/images/dsi_vs_length.png`.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-length
  relationship and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each length
  value, curve-shape classification, and discussion of which mechanism the data favours.
* `results/images/dsi_vs_length.png` — DSI-vs-length plot.
* `results/metrics.json` — DSI values at each length point.
* No paper, dataset, library, model, or answer assets produced by this task.

## Compute and Budget

* Local CPU only, no GPU. Expected runtime: 30-90 minutes depending on per-direction
  simulation cost.
* $0 external cost.

## Measurement

* Primary metric: **DSI** at each length value.
* Secondary (recorded but not primary): per-direction spike counts, preferred-direction firing
  rate.

## Key Questions

1. Is DSI monotonically increasing with distal length, or does it saturate?
2. At what length does saturation occur (if any)?
3. Is the DSI range at the sweep extremes (0.5× and 2.0×) large enough to distinguish the
   mechanisms, or does the testbed saturate at our default length?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC morphology and channel
  set.

## Scientific Context

Source suggestion **S-0027-01** (high priority). The t0027 synthesis answer identifies this as
the single highest-information-gain morphology experiment because the two competing mechanisms
make mathematically opposite predictions on the distal-length axis. Baseline papers supporting
each mechanism:

* Dan2018 passive-TR: builds the mechanism on a passive cable derivation.
* Sivyer2013 dendritic-spike: depends on Nav density in distal dendrites, which t0022 retains.

If the experiment reveals a non-monotonic curve, the t0027 synthesis flagged kinetic tiling
(Espinosa 2010) as a possible third mechanism — defer to a follow-up task.

## Execution Notes

* Follow the standard /execute-task flow: create-branch, check-deps, init-folders,
  implementation, results, suggestions, reporting.
* Include the `planning` step (the sweep design and compartment-identification logic benefit
  from explicit planning).
* Skip `research-papers`, `research-internet` (t0027 synthesis already did this), and
  `setup-machines` / `teardown` (local CPU only).
* Include `compare-literature` — the whole point is to compare the DSI-vs-length curve to
  Dan2018 and Sivyer2013 predictions.

**Results summary:**

> **Results Summary: Distal-Dendrite Length Sweep on t0022 DSGC**
>
> **Summary**
>
> Swept distal-dendrite length on the t0022 DSGC testbed across seven multipliers (**0.5×,
> 0.75×,
> 1.0×, 1.25×, 1.5×, 1.75×, 2.0×**) of baseline `sec.L` while holding the rest of the testbed
> fixed — **840 trials** across **12 directions × 10 trials × 7 lengths** in **~42 min** wall
> time
> on the local Windows workstation. **DSI (preferred/null definition) pins at 1.000 at every
> multiplier**, so the experiment cannot discriminate Dan2018 passive-transfer-resistance
> weighting
> from Sivyer2013 dendritic-spike branch independence on the DSI axis. Secondary metrics
> (vector-sum
> DSI, peak firing rate, HWHM) move only weakly or non-monotonically.
>
> **Metrics**
>
> * **DSI (preferred/null)**: **1.000** at every multiplier (range = **0.000**)
> * **Vector-sum DSI**: **0.664** at 0.5× → **0.643** at 2.0× (weak monotonic decrease,
> **−0.021** across the sweep)
> * **Peak firing rate**: **15 Hz** at L ≤ 1.00× → **14 Hz** at L ≥ 1.25× (single-Hz step)
> * **Null firing rate**: **0 Hz** at every multiplier
> * **HWHM**: oscillates **71.7°–116.2°**, non-monotonic

</details>

<details>
<summary>✅ 0028 — <strong>Brainstorm results session 6</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0028_brainstorm_results_6` |
| **Status** | completed |
| **Effective date** | 2026-04-22 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0025_brainstorm_results_5`](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-22T10:15:00Z |
| **End time** | 2026-04-22T13:10:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 6](../../../overview/tasks/task_pages/t0028_brainstorm_results_6.md) |
| **Task folder** | [`t0028_brainstorm_results_6/`](../../../tasks/t0028_brainstorm_results_6/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0028_brainstorm_results_6/results/results_detailed.md) |

# Brainstorm Results Session 6

## Motivation

Sixth strategic brainstorming session, run after completion of t0026 (V_rest sweep tuning
curves for t0022 and t0024 DSGC ports) and t0027 (literature survey on modeling effect of cell
morphology on direction selectivity). The session reviewed new findings from both completed
tasks, reassessed active suggestion priorities against actual task outputs, and committed to
the next batch of experimental tasks focused on dendritic morphology sweeps on the t0022
testbed.

## Scope

* Review project state after t0027 merge: 27 tasks total, 25 completed, 1 intervention_blocked
  (t0023 Hanson2019 port), $0.00 / $1.00 budget used, 110 uncovered suggestions (37 high, 57
  medium, 16 low).
* Summarise t0026 findings: V_rest sweep across 8 values on both DSGC ports; t0022 peaks DSI
  0.6555 at V=-60 mV with 15 Hz firing; t0024 U-shaped DSI (0.36 at -20 mV, 0.67 at -90 mV)
  never exceeds 7.6 Hz. Neither port reproduces the ~148-166 Hz published firing envelope at
  physiological V_rest.
* Summarise t0027 findings: 15 new paper assets + 1 synthesis answer. Strongest cross-paper
  evidence supports asymmetric SAC inhibition, electrotonic compartmentalisation, and kinetic
  tiling. Biggest gap: dendritic diameter swept in only 1 paper; branch order and soma size
  effectively untouched. Genuine contradiction: DSGC DS requires active dendrites (Sivyer2013,
  Schachter2010) vs collapsed compartment produces DS in fly T4 (Gruntman2018).
* Decide research direction for the next task batch.
* Decide on t0023 (Hanson2019 port) disposition.
* Prune the suggestion backlog.
* Plan 3-5 new tasks.

## Researcher Decisions

* **Research direction**: Morphology sweeps next (over peak-firing-rate gap or
  third-model-port paths). Rationale: t0027 synthesis identified distal-dendrite scaling as
  the single highest information-gain next experiment, and dendritic diameter is a corpus-wide
  blindspot.
* **t0023 Hanson2019 port**: Keep intervention_blocked / deprioritised. Rationale: two working
  testbeds (t0022 + t0024) already yield rich mechanism-level findings; adding a third DSGC
  model risks spreading effort thin.
* **Batch size**: 3 focused tasks.
* **Execution**: Local CPU only, sequential (no parallelisation prerequisite, no remote
  compute, no paid services).
* **Firing-rate gap**: Measure DSI only this batch; revisit firing-rate gap in a dedicated
  future batch.

## New Tasks Created

The session authorised three child tasks, each created via the `/create-task` skill
immediately after this brainstorm-results folder was scaffolded. Task indices are
auto-assigned as 29, 30, 31 (strictly greater than 28 per the ordering invariant).

* **t0029** — Distal-dendrite length scaling sweep on t0022. Scale distal dendritic segment
  lengths × {0.75, 1.0, 1.25, 1.5} under the 12-direction bar protocol, for each scale running
  both (a) active conductances intact and (b) Na/Ca ablated passive variant. Covers S-0027-01
  (high). Local CPU, ~30 min runtime.
* **t0030** — Distal-dendrite diameter thickening sweep on t0022. Scale distal dendritic
  segment diameters × {0.5, 1.0, 1.5, 2.0}, same protocol and active-vs-passive pairing.
  Covers S-0027-03 (medium, upgraded effectively to high by bundling with t0029). Local CPU,
  ~30 min runtime.
* **t0031** — Paywalled PDF retrieval for Kim2014 and Sivyer2013 via Sheffield institutional
  SSO, followed by full-text summary upgrade and t0027 synthesis answer asset citation
  refresh. Covers S-0027-06 (medium). Local CPU + network, ~30-60 min runtime.

## Suggestion Cleanup

No suggestions were rejected or reprioritised in this session. The researcher opted to keep
all three AI-proposed rejection candidates (S-0003-02, S-0010-01, S-0026-05) active in case
the t0022/t0024 analysis line hits a wall and a third DSGC model becomes valuable later.

## Task Updates

No existing task was cancelled, updated, or re-opened. t0023 (Hanson2019 port) remains in
status `intervention_blocked`.

## Expected Assets

This brainstorm session produces no assets beyond the brainstorm-results task folder and its
downstream child tasks. `expected_assets` is `{}`.

## Dependencies

Dependencies are all currently completed tasks up through t0027.

**Results summary:**

> **Results Summary: Brainstorm Session 6**
>
> **Summary**
>
> Sixth strategic brainstorm following the completion of t0026 (V_rest sweep and tuning curves
> on
> t0022/t0024 DSGCs) and t0027 (15-paper morphology-direction-selectivity literature survey
> with
> synthesis answer). Three new tasks approved: t0029 (distal-dendrite length sweep on t0022),
> t0030
> (distal-dendrite diameter sweep on t0022), t0031 (paywalled PDF fetch for Kim2014 and
> Sivyer2013).
> Zero suggestions rejected or reprioritised; t0023 remains intervention_blocked.
>
> **Session Outcome**
>
> The researcher directed the session toward dendritic morphology sweeps, keeping t0023
> (Hanson2019
> port) intervention_blocked, preferring a 3-5 task focused batch executed locally on CPU and
> measured
> by DSI alone. The two sweep tasks act as mechanistic discriminators: distal-length variation
> separates Dan2018 passive-TR weighting from Sivyer2013 dendritic-spike branch independence
> (both
> compatible with current t0022 data), while distal-diameter variation separates Schachter2010
> active-dendrite amplification from passive-filtering alternatives.
>
> **Decisions**

</details>

## 2026-04-21 (5)

## ✅ Completed

<details>
<summary>✅ 0027 — <strong>Literature survey: modeling effect of cell morphology
on direction selectivity</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0027_literature_survey_morphology_ds_modeling` |
| **Status** | completed |
| **Effective date** | 2026-04-21 |
| **Dependencies** | — |
| **Expected assets** | 15 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-04-21T18:33:02Z |
| **End time** | 2026-04-21T22:23:03Z |
| **Step progress** | 12/15 |
| **Task page** | [Literature survey: modeling effect of cell morphology on direction selectivity](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Task folder** | [`t0027_literature_survey_morphology_ds_modeling/`](../../../tasks/t0027_literature_survey_morphology_ds_modeling/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0027_literature_survey_morphology_ds_modeling/results/results_detailed.md) |

# Literature Survey: Modeling the Effect of Cell Morphology on Direction Selectivity

## Motivation

Our recent V_rest sweep (`t0026`) on the t0022 (deterministic ModelDB 189347 port) and t0024
(de Rosenroll 2026 AR(2)-correlated stochastic port) DSGC compartmental models produced a
headline finding: neither port simultaneously reproduces the published DSI (0.45–0.67) and the
published peak firing rate (40–166 Hz) at any biologically plausible resting potential. Both
ports use a single fixed dendritic morphology — `dsgc-baseline-morphology` for t0022/t0024 —
and we have not yet asked how much of the gap is attributable to morphology versus channels,
synaptic kinetics, or input statistics.

Before we commit compute and engineering effort to a morphology-sweep experiment on these
testbeds, we need to know what the published modeling literature already says: which
morphology variables (dendritic length, branch order, segment diameter, asymmetry, input
layout on dendrites, soma-dendrite ratios, etc.) have been shown to affect direction
selectivity, by what causal mechanisms, and where the published findings disagree or have
gaps. This survey directly informs the design of follow-up experiments on t0022/t0024 and
constrains which morphology dimensions are worth sweeping.

## Scope

Survey the published computational, biophysical, and theoretical modeling literature on the
effect of neuronal cell morphology on direction selectivity. Primary focus: retinal
direction-selective ganglion cells (DSGCs — ON, OFF, ON-OFF subtypes) and starburst amacrine
cells (SACs). Secondary focus: other direction-selective neurons (cortical V1 / MT, fly lobula
plate / motion-sensitive neurons, vestibular nuclei) where morphology is treated as a
manipulated variable in a model.

### Already-covered baseline

Five papers in our existing corpus already meet the inclusion criteria below and were
identified during a prior in-session corpus search. **Do NOT re-download these** — link to
them by `paper_id` in the synthesis report and cite them alongside any new papers found:

* `10.1371_journal.pcbi.1000899` — Schachter 2010 — dendrite electrotonic length × Na density
  distribution → spike-DSI amplification (NeuronC compartmental)
* `10.7554_eLife.52949` — Jain 2020 — dendritic compartment scale (5–10 µm) × CaV/NMDA
  thresholding → dendritic Ca²⁺ DSI (NEURON + 2P imaging)
* `10.1016_j.cub.2018.03.001` — Morrie 2018 — SAC arbor size & plexus density (Sema6A−/−) →
  DSGC spike DSI collapse (TREES-toolbox IPSC simulation)
* `10.1038_s41467-026-70288-4` — Poleg-Polsky 2026 — bipolar input location on dendrite ×
  A-type K × NMDA ratio × passive Rm/Cm via ML search → DSI mechanisms (NEURON + ML)
* `10.1016_j.celrep.2025.116833` — de Rosenroll 2026 — SAC GABA/ACh spatial offset × subunit
  E/I geometry → subunit-level DSI (NEURON network)

The task's job is to **extend** coverage beyond these five, not duplicate them.

## Inclusion Criteria

A paper is included if it satisfies **all three** criteria:

1. **Builds a model** — compartmental simulation (NEURON, Arbor, NetPyNE, Brian, GENESIS,
   NeuronC, custom solver), cable-theory derivation, or abstract neural network model with
   explicit morphology (not just point neurons).
2. **Morphology is a manipulated or causally-relevant variable** — dendritic branching
   pattern, branch order, dendritic length, segment diameter, surface area, soma-dendrite
   ratio, asymmetric vs symmetric arbors, isotropic vs anisotropic arbors,
   primary/secondary/tertiary hierarchy, or the spatial layout of synaptic inputs ON the
   dendrites. Just *using* a morphology without varying it does not qualify.
3. **Direction selectivity as outcome** — directional tuning curves, DSI / DS index,
   preferred-vs- null direction asymmetry, vector-sum direction, or equivalent measure of
   direction-dependent firing or PSP.

### Borderline cases — include and flag

* **SAC morphology → DS** papers — include; flag as `"SAC, not DSGC"`.
* **Passive cable theory** papers deriving DS from input asymmetry on a passive cylinder —
  include; flag as `"passive cable, geometry-only"`.
* **Insect / invertebrate DS-circuit** modeling — include if morphology is varied; flag
  organism (e.g., `"Drosophila lobula plate"`, `"hawkmoth"`).
* **Cortical or subcortical DS neurons** modeled with morphology variation — include; flag
  region.

### Borderline cases — exclude

* Papers fitting DSI to **one fixed morphology** without varying it — exclude; they do not
  model the *effect* of morphology.
* Pure **NMDA-Mg-block** or pure **E/I-timing** papers without morphology variation — exclude.
* Pure experimental papers (no model) — exclude unless the experimental finding is explicitly
  used to constrain a model in the same paper.

## Search Strategy

### Citation-graph expansion

Pull forward and backward citations for each of the five baseline papers using:

* Google Scholar "Cited by" — forward citation graph
* OpenCitations / Semantic Scholar API — both directions
* Each paper's reference list — backward citations

### Targeted keyword searches

Run on Google Scholar, PubMed, bioRxiv, arXiv:

* `"DSGC compartmental model morphology"`
* `"direction selectivity dendritic geometry"`
* `"starburst amacrine cell morphology direction selectivity"`
* `"asymmetric dendritic arbor direction selective"`
* `"branch order morphology direction tuning"`
* `"compartmental model dendritic length DSI"`
* `"cable theory direction selective neuron"`
* `"synaptic input asymmetry dendritic compartment direction"`

### Author-targeted searches

Pull recent and seminal works from authors known to publish in this space:

* Sebastian Espinosa (Schachter senior author), Greg Field, Marla Feller, Jonathan Demb,
  Florentina Soto, Alex Poleg-Polsky, Justin de Rosenroll, Stuart Trenholm, Anastasia Jain,
  Adam Mani, Wei Wei, David Berson, Richard Masland, Robert Smith.

### Repository searches

* **ModelDB** (`modeldb.science`) — search for compartmental DSGC and SAC models; each model
  entry typically links to one or more publications.
* **SenseLab Yale** — DSGC-related model lookups.
* **Open Source Brain** — published compartmental model collection.

### Beyond retina

Do not limit to retinal DSGCs. Include:

* Classic cable-theory papers (Rall, Branco-Häusser-Clark) deriving DS from input pattern
  asymmetry on dendritic geometry.
* Cortical DS modeling (V1 simple/complex cells, MT) where morphology is varied.
* Fly motion-sensitive neuron modeling (HS/VS cells, T4/T5) where dendritic geometry is
  varied.

## Budget and Stop Criterion

**Target**: 12–20 new paper assets downloaded and summarised (in addition to the 5 baseline
papers, for a final corpus of ~17–25 morphology-DS papers).

**Stop criterion**: stop earlier if returns diminish — when newly-found candidates stop
satisfying the inclusion criteria or stop introducing novel mechanisms / morphology variables.
Push to **25 new papers** if novel mechanisms keep appearing (e.g., a previously-unknown class
of morphology manipulation shows up).

**Per-paper cost**: $0. No paid APIs. PDF retrieval is via open access, preprint servers, or
Sheffield institutional access (VPN / SSO). For paywalled PDFs that cannot be retrieved (e.g.,
Cell Press / Elsevier / Springer-Nature / Wiley), generate an intervention file in
`intervention/` rather than blocking the survey — record the metadata and abstract from the
landing page, mark `download_status: "failed"` in `details.json`, and proceed.

## Deliverables

`expected_assets`: `{"paper": 15, "answer": 1}` — the `15` is the midpoint of the 12–20 target
range; the actual count may legitimately fall anywhere in 12–25 depending on the stop
criterion.

### 1. Paper assets (target 12–20)

Each new paper assets goes under
`tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/<paper_id>/` and follows
`meta/asset_types/paper/specification.md` exactly:

* `details.json` with all required fields, including all relevant `categories` from
  `meta/categories/`
* `summary.md` with all mandatory sections (Metadata, Abstract, Overview, Architecture/Models/
  Methods, Results, Innovations, Datasets, Main Ideas, Summary), summarised after reading the
  full paper text per the spec
* `files/` containing at minimum the PDF (or markdown conversion if no PDF is available)

For every included paper, the `summary.md` must explicitly note in the `## Architecture,
Models and Methods` section: which morphology variable was manipulated, how it was manipulated
(range, levels, parametric vs categorical), and the DS metric reported.

### 2. Answer asset

One answer asset at
`tasks/t0027_literature_survey_morphology_ds_modeling/assets/answer/morphology-direction-selectivity-modeling-synthesis/`
following `meta/asset_types/answer/specification.md`.

Question (verbatim, to appear in the answer asset's `details.json`):

> **What variables of neuronal morphology have been shown by computational modeling to affect
> direction selectivity, by what mechanisms, and what gaps remain?**

The answer must cite by `paper_id` every paper used as evidence — both the 5 baseline papers
(from t0002, t0010, t0013, t0024) and every new paper added in this task. Confidence level
should reflect the consistency of findings across papers and across modelling approaches.

### 3. `results_detailed.md` synthesis

Required sections (in this order):

* **Coverage table** — one row per included paper (baseline + new). Columns: `paper_id`,
  first-author year, organism / cell type, morphology variable manipulated, DS outcome
  measured, model type, mechanism flag.
* **Morphology variable taxonomy** — group findings by which variable was studied: dendritic
  length, branch count, branch order, segment diameter, total surface area, asymmetric vs
  symmetric arbor, input-on-dendrite spatial layout, soma-dendrite ratio, dendritic
  compartmentalisation scale. For each variable: how many papers studied it, what range was
  swept, what direction the effect on DSI went, and the strength of the consensus.
* **Mechanism taxonomy** — group findings by causal mechanism: electrotonic
  compartmentalisation, dendritic spike thresholding, NMDA-Mg gating in dendritic context,
  delay lines via dendritic cable propagation, coincidence detection at branch points,
  asymmetric SAC inhibition driven by presynaptic geometry, leak-driven attenuation,
  axial-resistance-driven sequence selectivity.
* **Gaps and contradictions** — which morphology variables are under-explored in the
  literature, where published findings disagree (e.g., Schachter 2010 vs Jain 2020 on the
  dominant scale of compartmentalisation), and which findings are most replicable across labs
  / model frameworks.
* **Recommendations** — 3–5 concrete morphology-sweep experiments worth running on our t0022 /
  t0024 testbeds, prioritised by expected information gain. Each recommendation must specify:
  the morphology variable to sweep, the range and step size, the predicted effect on DSI /
  peak firing rate based on the literature, and which baseline paper the prediction comes
  from.

### 4. `results_summary.md`

A 2–3 paragraph executive summary with headline findings: how many papers were found in total
(baseline + new), which morphology variables have the strongest cross-paper evidence, what the
field disagrees on, what the project should sweep first on the t0022 / t0024 testbeds.

## Categories

For each new paper, mark with the most specific applicable subset of: `direction-selectivity`,
`compartmental-modeling`, `dendritic-computation`, `retinal-ganglion-cell`. Add `cable-theory`
for passive-cable theoretical papers, `patch-clamp` only if the paper jointly contributes
patch-clamp data plus a morphology-varying model, `synaptic-integration` if the morphology
variation is on synaptic input layout.

## Dependencies

**None.** This is an independent literature survey that runs in parallel with any active
experimental work on t0022 / t0024 / t0026 follow-ups.

## Compute and Budget

* No remote compute.
* No paid API.
* Runs entirely on the local Windows workstation using existing tooling (paper-download skill,
  paper-asset spec).
* PDF retrieval may require Sheffield VPN or institutional SSO for paywalled journals — flag
  as intervention if a needed PDF cannot be retrieved.
* Estimated wall time: 4–8 hours of human-supervised execution, depending on how many
  borderline papers require careful judgment calls and how many PDFs are paywalled.

## Key Questions (numbered, falsifiable)

1. Which morphology variable (dendritic length, branch count, segment diameter, asymmetry,
   input layout) has the **most cross-paper evidence** for affecting DSI in DSGCs and SACs?
2. Is the **dominant compartmentalisation scale** for direction selectivity at the level of
   whole dendrites (Schachter 2010), 5–10 µm sub-segments (Jain 2020), or somewhere else?
3. Where do **published findings disagree**, and is the disagreement attributable to species
   (mouse vs rabbit), cell-type (ON vs OFF vs ON-OFF), simulator (NEURON vs NeuronC vs
   custom), or genuine biological diversity?
4. Which **3–5 morphology sweeps** should we prioritise on t0022 / t0024 next, given our
   headline gap (peak firing rate 15 Hz at DSI 0.66, vs published 148 Hz)?
5. Is there a **published morphology that simultaneously reproduces DSI ≈ 0.5 AND peak firing
   rate ≈ 100 Hz** in a compartmental model? If so, what makes that morphology different from
   `dsgc-baseline-morphology`?

## Risks and Fallbacks

* **PDF paywall**: flag as intervention; abstract-only summary is acceptable for paywalled
  papers if the abstract contains enough information to confirm inclusion.
* **Borderline judgment calls**: when the inclusion criteria are ambiguous for a given paper,
  default to **include and flag**, with a brief borderline note in the paper's `summary.md`.
  The synthesis report can re-exclude flagged papers if the synthesis-stage review finds the
  morphology link too weak.
* **Search exhaustion before target hit**: if fewer than 12 new papers are found after
  exhausting the search strategy, document the gap in `results_summary.md` and proceed with
  whatever coverage was achieved. Do not pad the corpus with weakly-relevant papers to meet
  the count.
* **Search overshoot**: if more than 25 strong candidates are found, prioritise by recency
  (post-2010) and by mechanism novelty, and defer the rest to a follow-up survey task
  suggestion.

## Verification Criteria

* Each new paper asset passes `verify_paper_asset.py` with 0 errors.
* `details.json` for every new paper has a non-empty `categories` field including at least one
  of `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`, or
  `retinal-ganglion-cell`.
* The answer asset cites every included paper by `paper_id` (no orphan citations, no missing
  evidence).
* `results_detailed.md` Coverage Table includes a row for every included paper (baseline +
  new).
* `results_summary.md` opens with a single sentence stating the final paper count and the most
  consensus-supported morphology variable.

**Results summary:**

> **Results Summary: Morphology and Direction Selectivity Modeling Literature Survey**
>
> **Summary**
>
> This task added **15 new paper assets** to the morphology-and-direction-selectivity modeling
> corpus,
> bringing the total corpus (baseline + new) to **20 papers**. Coverage now spans retinal SAC
> and DSGC
> models, fly lobula-plate VS and T4 neurons, primate SAC, cat V1 cortical cells, and the
> TREES-toolbox cable-theory framework. The strongest cross-paper evidence supports
> **asymmetric SAC
> inhibition** and **electrotonic compartmentalisation** as the DS-shaping morphology
> mechanisms:
> these are replicated across mouse, rabbit, and fly; across TREES, NEURON, NeuronC, and
> patch-clamp;
> and across at least seven papers. Kinetic tiling of bipolar input (sustained-proximal,
> transient-distal) is the third replicated mechanism, supported by four independent papers.
>
> Key gaps: **dendritic diameter** is systematically swept in only one paper (Wu2023, primate
> SAC);
> **branch order**, **soma size**, and **branch-angle at fixed length** are all effectively
> untouched
> in the DSGC literature. Cortical DS modeling is limited to one paper (Anderson1999) that
> rejects
> dendritic asymmetry as sufficient and has not been updated with kinetic-tiling tests. The
> corpus
> also contains a genuine contradiction: Sivyer2013 and Schachter2010 argue DSGC DS requires
> active
> dendritic conductances, while Dan2018 (fly VS) and Gruntman2018 (fly T4) show that passive
> cable or
> even a collapsed single compartment can produce DS in invertebrate systems.

</details>

<details>
<summary>✅ 0026 — <strong>V_rest sweep tuning curves for t0022 and t0024 DSGC
ports</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0026_vrest_sweep_tuning_curves_dsgc` |
| **Status** | completed |
| **Effective date** | 2026-04-21 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Expected assets** | 2 predictions |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-04-21T12:47:42Z |
| **End time** | 2026-04-21T17:43:26Z |
| **Step progress** | 10/15 |
| **Task page** | [V_rest sweep tuning curves for t0022 and t0024 DSGC ports](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Task folder** | [`t0026_vrest_sweep_tuning_curves_dsgc/`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_detailed.md) |

# V_rest sweep tuning curves for t0022 and t0024 DSGC ports

## Motivation

Two of the four DSGC compartmental-model ports in this project
(`modeldb_189347_dsgc_channel_testbed` from t0022 and `de_rosenroll_2026_dsgc` from t0024)
produce direction-selective tuning curves at the default resting potential of `-60 mV`. The
project's research questions (RQ1, RQ4) ask how the cell's biophysics — particularly
voltage-gated-channel availability and dendritic integration — shape tuning. Resting potential
is the single most direct experimental knob for probing those mechanisms because it controls:

1. **Na channel inactivation availability**: at hyperpolarized holding (e.g. `-90 mV`) the
   fast sodium gate sits in its deinactivated state, producing a larger pool available for
   spiking; at depolarized holding (e.g. `-30 mV`) a large fraction is tonically inactivated.
2. **NMDA receptor Mg block**: the voltage-dependent Mg block relieves as the membrane
   depolarizes, so NMDA contribution to synaptic integration grows with V_rest. This should
   shift the E/I balance that implements asymmetric inhibition in both ports.
3. **Leak driving force and input resistance**: with `eleak` pinned to a new holding, the leak
   current's reversal and the cell's apparent input resistance both change, altering how
   strong BIP/SAC input currents look to the soma.

The two driver paradigms under test — deterministic per-dendrite E-I scheduling in t0022
versus AR(2)-correlated stochastic release in t0024 — should respond differently to V_rest
because they differ in how they compose inhibitory current magnitude against voltage-gated
drive.

## Scope

Run a V_rest sweep on both ports. All other protocol knobs (bar velocity, 12 angles, tstop,
morphology) are held fixed to the defaults of the respective library assets.

### V_rest values

Exactly eight values, all in mV: `-90, -80, -70, -60, -50, -40, -30, -20`.

### Holding strategy

At every V_rest value, set **both** `V_INIT_MV` **and** `ELEAK_MV` (leak reversal) to the
sweep value before initialising NEURON. Moving only `v_init` re-settles to `eleak` within a
few milliseconds and does not implement a true resting-potential shift; moving only `eleak`
leaves the initial condition mismatched. Both must move together.

### Models and trial budgets

| Model | Task | Driver | Trials per angle | Total trials |
| --- | --- | --- | --- | --- |
| `modeldb_189347_dsgc_channel_testbed` | t0022 | Deterministic per-dendrite E-I | 1 | 1 × 12 × 8 = 96 |
| `de_rosenroll_2026_dsgc` (correlated `rho=0.6`) | t0024 | AR(2)-correlated stochastic release | 10 | 10 × 12 × 8 = 960 |

One trial per angle is sufficient for t0022 because its driver is deterministic; only the
V_rest value changes between (angle, V_rest) runs. Ten trials per angle are retained for t0024
so that trial-to-trial variance in the AR(2) release process remains visible in the tuning
curve — lower counts would fold V_rest effects into noise.

### Protocol

For each model and each V_rest value, run the existing 12-angle protocol (`0, 30, 60, …, 330`
degrees) using the library asset's stock `run_trial` / `run_one_trial` function. Only override
the two holding-potential constants — do not modify the library asset itself (immutability
rule 5) and do not change bar velocity, tstop, or any other constant.

## Approach

### Implementation

Two thin wrapper drivers live in `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/`:

* `run_vrest_sweep_t0022.py` — imports from `tasks.t0022_modify_dsgc_channel_testbed.code`,
  parameterises `V_REST_MV`, sets both `h.v_init` and every leak section's `e` parameter to
  that value, then invokes the stock tuning-curve routine across the 12 angles. Loops the 8
  V_rest values serially.
* `run_vrest_sweep_t0024.py` — same idea against
  `tasks.t0024_port_de_rosenroll_2026_dsgc.code`. Uses the correlated `rho=0.6` AR(2) path
  (the task's headline condition).

Each wrapper writes one CSV per V_rest value under `data/t0022/` or `data/t0024/`, then
concatenates them into `data/t0022/vrest_sweep_tidy.csv` and `data/t0024/vrest_sweep_tidy.csv`
with columns `(v_rest_mv, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`. Also
records per-V_rest wall time to `data/t0022/wall_time_by_vrest.json` and
`data/t0024/wall_time_by_vrest.json`.

### Analysis

A single analysis script computes, for each (model, V_rest):

* Preferred direction and DSI (reusing the t0012 `tuning_curve_loss` scorer's DSI formula)
* Peak firing rate (Hz)
* Null-direction firing rate (Hz)
* HWHM (degrees)

Those values are written to `data/t0022/vrest_metrics.csv` and `data/t0024/vrest_metrics.csv`,
and summary tables are embedded in `results/results_detailed.md`.

### Plots (all in `results/images/`)

* 16 individual polar plots: `polar_<model>_vrest_<value>.png` (one per model × V_rest pair,
  plotting firing rate in Hz vs direction in degrees on a polar axis).
* 2 overlay polar plots: `polar_overlay_t0022.png` and `polar_overlay_t0024.png` showing all 8
  V_rest tuning curves on the same polar axes with a perceptually ordered colormap. Each
  answers the question "how does the tuning curve morph as V_rest moves from hyperpolarized to
  depolarized?"
* 2 Cartesian summary plots: `dsi_vs_vrest.png` and `peak_hz_vs_vrest.png` with both models
  overlaid, showing how DSI and peak firing rate trend with V_rest.

## Expected Assets

Two predictions assets, one per model. Each contains:

* `details.json` (predictions asset metadata following `meta/asset_types/predictions/`)
* The full tidy CSV as the predictions payload
* A short description linking back to this task and the source model's library asset

`expected_assets` in `task.json` is `{"predictions": 2}`.

## Dependencies

* `t0022_modify_dsgc_channel_testbed` — provides the `modeldb_189347_dsgc_channel_testbed`
  library asset and the `run_tuning_curve.py` driver that this task reuses.
* `t0024_port_de_rosenroll_2026_dsgc` — provides the `de_rosenroll_2026_dsgc` library asset
  and the correlated-AR(2) driver.

Both dependencies are completed and on main.

## Compute and Budget

* No remote compute, no paid API calls, no GPUs.
* Runs entirely on the local Windows workstation using the existing NEURON + Python stack.
* Expected wall time: ~25 min for t0022 (96 trials) + ~4 h 15 min for t0024 (960 trials at
  scale comparable to t0024's original 800-trial run).
* Total budget: `$0`.

## Metrics

Register the following if not already registered in `meta/metrics/` (propose as suggestions
otherwise; do not block on meta gaps):

* `dsi_at_vrest_<mv>` for each V_rest value
* `peak_hz_at_vrest_<mv>` for each V_rest value
* `hwhm_deg_at_vrest_<mv>` for each V_rest value
* `efficiency_wall_time_per_trial_seconds` (one value per model — total wall time / total
  trial count)

## Output Specification

### Charts (all in `results/images/`, embedded in `results_detailed.md`)

| Chart | Axes | Question answered |
| --- | --- | --- |
| `polar_<model>_vrest_<value>.png` | θ = direction (deg), r = firing rate (Hz) | What is the tuning curve shape at this specific V_rest? |
| `polar_overlay_<model>.png` | θ = direction (deg), r = firing rate (Hz), 8 curves | How does the tuning curve morph with V_rest? |
| `dsi_vs_vrest.png` | x = V_rest (mV), y = DSI, 2 lines (one per model) | Is there a V_rest that maximises direction selectivity? |
| `peak_hz_vs_vrest.png` | x = V_rest (mV), y = peak firing rate (Hz), 2 lines | Where is peak firing rate highest? Does the 40-80 Hz envelope open up? |

### Tables in `results_detailed.md`

* Per-(model, V_rest) metrics: V_rest, DSI, peak_hz, null_hz, HWHM, wall_time_s
* Per-model aggregate efficiency: total trials, total wall time, seconds per trial

## Key Questions

1. Does either DSGC port show a V_rest value at which DSI is higher than at the default `-60
   mV` baseline?
2. Does either port reach the t0004 target peak-firing-rate envelope (40-80 Hz) at any V_rest
   value? This is the headline unresolved problem across all four existing ports.
3. Is the direction-selectivity mechanism in t0022 (deterministic per-dendrite E-I) more or
   less V_rest-dependent than in t0024 (AR(2) stochastic release)?
4. At what V_rest does each port silence (all-angle firing rate ≈ 0 Hz) on the hyperpolarized
   end, and at what V_rest does it enter depolarization block on the depolarized end?
5. Does HWHM narrow systematically as V_rest increases (depolarization-driven gain change), or
   is it relatively flat across the sweep (consistent with inhibition-dominated tuning)?

## Source Suggestion

None. Researcher-directed experiment captured in brainstorming session 5
(`t0025_brainstorm_results_5`).

**Results summary:**

> **Results Summary: V_rest sweep tuning curves for t0022 and t0024 DSGC ports**
>
> **Summary**
>
> Swept resting potential across eight values (**-90 mV to -20 mV in 10 mV steps**) for two
> DSGC
> compartmental models under the standard 12-direction moving-bar protocol. Model t0022
> (deterministic
> ModelDB 189347 port) ran **96 trials** (~6.0 min wall time); model t0024 (de Rosenroll 2026
> port
> with AR(2)-correlated stochastic release at rho=0.6) ran **960 trials** (~3.21 h wall time).
> Both
> models show strong V_rest dependence but with qualitatively different shapes: t0022 peaks
> DSI
> sharply at V_rest=-60 mV, while t0024 is U-shaped with maxima at the extremes.
>
> **Metrics**
>
> * **t0022 DSI range**: **0.046** (V=-30 mV) to **0.6555** (V=-60 mV) — 14x modulation
> * **t0024 DSI range**: **0.3606** (V=-20 mV) to **0.6746** (V=-90 mV) — 1.9x modulation,
>   U-shaped
> * **t0022 peak firing rate**: **6 Hz** at V=-90 mV, monotone up to **129 Hz** at V=-30 mV,
>   collapses
> to **26 Hz** at V=-20 mV (Na inactivation)
> * **t0024 peak firing rate**: **1.5 Hz** at V=-90 mV, monotone up to **7.6 Hz** at V=-20 mV
>   (no
> hyper-depolarisation collapse)
> * **t0022 HWHM**: 0.77 deg at V≤-80 mV (near-binary curve) vs. 180 deg at V=-30/-40 mV
>   (complete

</details>

<details>
<summary>✅ 0025 — <strong>Brainstorm results session 5</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0025_brainstorm_results_5` |
| **Status** | completed |
| **Effective date** | 2026-04-21 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md), [`t0021_brainstorm_results_4`](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Start time** | 2026-04-21T12:30:00Z |
| **End time** | 2026-04-21T12:35:52Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 5](../../../overview/tasks/task_pages/t0025_brainstorm_results_5.md) |
| **Task folder** | [`t0025_brainstorm_results_5/`](../../../tasks/t0025_brainstorm_results_5/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0025_brainstorm_results_5/results/results_detailed.md) |

# Brainstorm results session 5

Brainstorming session 5 covering project state after the t0024 de Rosenroll 2026 DSGC port
merged in PR #23. The research environment now contains four DSGC compartmental-model ports
(`modeldb_189347_dsgc`, `modeldb_189347_dsgc_gabamod`, `modeldb_189347_dsgc_channel_testbed`,
`de_rosenroll_2026_dsgc`) all sharing the t0004 target tuning-curve envelope and the t0012
tuning-curve scoring library. The session answered the researcher's three inline questions
(effective model count, why t0022 returns DSI = 1, HWHM definition, individual stimulus length
and firing-rate window) and then planned a single concrete next experiment.

## Decision

Create **one** new experimental task (`t0026`): sweep the resting potential of the t0022 and
t0024 ports from `-90 mV` to `-20 mV` in `10 mV` steps, holding both `v_init` and `eleak`
together to the sweep value (true resting-potential shift, not just initial-condition tweak),
and report the resulting tuning curves in polar coordinates.

## Context captured for the next task

* t0022 driver uses deterministic per-dendrite E-I scheduling; a single trial per angle is
  adequate. Total: 1 trial × 12 angles × 8 V_rest values = 96 trials (~25 min wall time).
* t0024 driver uses AR(2)-correlated stochastic release; keep 10 trials per angle to retain
  trial-to-trial variance. Total: 10 trials × 12 angles × 8 V_rest values = 960 trials (~4 h
  wall time).
* Both ports already return tuning curves via the t0012 `tuning_curve_loss` API; the sweep
  only varies `v_init` and `eleak` at driver setup.
* Expected assets: 2 predictions assets (one per model) plus polar-coordinate plots per V_rest
  plus overlay plots per model.

No new suggestions created, no suggestion rejections or reprioritizations this session — the
focus was a single researcher-directed experiment rather than backlog pruning.

**Results summary:**

> **Results Summary: Brainstorm results session 5**
>
> **Summary**
>
> Brainstorming session 5 held after the t0024 de Rosenroll 2026 DSGC port merged (PR #23).
> The
> session answered three researcher questions on model count, DSI = 1 saturation in t0022,
> HWHM
> definition, and stimulus length, then captured one concrete follow-up task: a V_rest sweep
> of the
> t0022 and t0024 ports from -90 mV to -20 mV in 10 mV steps, reported in polar coordinates.
>
> **Metrics**
>
> No quantitative metrics produced by a brainstorm session.
>
> **Verification**
>
> * `verify_task_file.py` passed on `t0025_brainstorm_results_5` with 0 errors.
> * `verify_logs.py` passed on `t0025_brainstorm_results_5` with 0 errors.
> * Follow-up task `t0026` created via `/create-task` and verified (0 errors on
> `verify_task_file.py`).

</details>

<details>
<summary>✅ 0024 — <strong>Port de Rosenroll 2026 DSGC model</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0024_port_de_rosenroll_2026_dsgc` |
| **Status** | completed |
| **Effective date** | 2026-04-21 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Expected assets** | 1 library, 1 paper |
| **Source suggestion** | — |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Start time** | 2026-04-21T01:51:48Z |
| **End time** | 2026-04-21T08:55:00Z |
| **Step progress** | 12/15 |
| **Task page** | [Port de Rosenroll 2026 DSGC model](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Task folder** | [`t0024_port_de_rosenroll_2026_dsgc/`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/results/results_detailed.md) |

# Port de Rosenroll 2026 DSGC Model

## Motivation

The project currently has DSGC compartmental model ports derived from a single lineage: t0008
and t0020 both port ModelDB 189347 (Poleg-Polsky & Diamond 2016), and t0022 modifies that same
port for dendritic-computation DS. A sibling port of Hanson et al. 2019 is reserved in t0023.
Adding de Rosenroll et al. 2026 as an independent third implementation provides a third
structurally independent comparison point and, because the paper is recent, is the port most
likely to incorporate modern methodology and channel mechanisms. In particular, it may include
an explicit Nav1.6 / Nav1.2 split at the axon initial segment consistent with the patch-clamp
priors reviewed in t0017, and may use more recent Kv and Cav formulations than the older
Poleg-Polsky and Hanson models. This makes it especially relevant to the project's
channel-testbed goal of evaluating how specific channel combinations shape direction
selectivity.

## Scope

Port the de Rosenroll et al. 2026 DSGC model into the project as a new library asset (proposed
slug `de_rosenroll_2026_dsgc`) following the HOC/MOD/morphology layout established by t0008.
Fetch the paper as a paper asset if it is not already present. Run the standard 12-angle
moving-bar tuning-curve protocol using the driver infrastructure from t0022 where compatible,
producing `tuning_curves.csv` and a `score_report.json` against the target tuning curve from
t0004. Compare results against the Poleg-Polsky lineage (t0008, t0020, t0022) and the Hanson
port (t0023) in `results_detailed.md`.

## Deferred Status

This task is deferred. It is created and reserved now but must NOT be executed by the
execute-task loop until t0022 completes and the researcher explicitly reviews its outcomes.
After task-folder creation the orchestrator will write an intervention file to block
execution. The decision to proceed depends on what t0022 reveals about the channel-testbed
framework and whether a third independent implementation adds value.

## Deliverables

* New library asset `de_rosenroll_2026_dsgc` with HOC, MOD, and morphology files,
  `details.json`, and `description.md`.
* Source paper downloaded and registered as a paper asset if not already in the corpus.
* 12-angle moving-bar tuning curve: `tuning_curves.csv` and `score_report.json`.
* Cross-model comparison in `results_detailed.md` against t0008, t0020, t0022, and t0023.

## Dependencies

* `t0008_port_modeldb_189347` — reference HOC/MOD library-asset skeleton.
* `t0012_tuning_curve_scoring_loss_library` — scorer used for `score_report.json`.
* `t0022_modify_dsgc_channel_testbed` — driver infrastructure (soft dependency; reuse if
  compatible, otherwise adapt).

## Risks and Unknowns

* The 2026 paper may have restricted full-text access or be paywalled at porting time,
  limiting methodological detail.
* Original source code may not be publicly released or may not target NEURON, forcing partial
  reimplementation from the paper.
* Morphology may live in a different repository with different conventions.
* The model may rely on MOD mechanisms (Nav1.6, Nav1.2, modern Kv1, updated Cav) not yet in
  the project's MOD set, requiring new mechanism files and validation.
* Rough effort estimate: 1-2 days if source is NEURON and openly available; 3-5 days if
  partial reimplementation is needed.

## Out of Scope

* Parameter fitting or channel-density sweeps on the ported model (future task).
* Cross-simulator porting (e.g., NetPyNE, Brian) beyond the NEURON target.
* Re-running t0022's channel-testbed modifications on this model (future task if justified by
  t0022 outcomes).
* Executing this task now — execution is blocked pending t0022 review.

**Results summary:**

> **Results Summary: Port de Rosenroll 2026 DSGC Model**
>
> **Summary**
>
> Ported the de Rosenroll et al. 2026 DSGC model into a new library asset
> `de_rosenroll_2026_dsgc`
> (NEURON `HHst_noiseless`/`Exp2NMDA`/`cadecay` MOD mechanisms with the 341-section
> `RGCmodelGD.hoc`
> morphology, vendored from Zenodo `10.5281/zenodo.17666158` at commit `a23f642a`). Drove the
> cell
> through the paper-native 8-direction protocol and the project-standard 12-angle protocol
> under both
> correlated (`rho=0.6`) and uncorrelated (`rho=0.0`) AR(2) release-rate noise (20 trials per
> angle,
> 800 trials total, ~4h15m wall time on the local Windows workstation). The port produces
> strong
> direction selectivity but **does not** reproduce the paper's correlation-drop signature; the
> port-fidelity gate (REQ-5) failed and the miss is recorded in
> `intervention/port_fidelity_miss.md`
> as a first-class finding per plan step 13.
>
> **Metrics**
>
> * **DSI 12-ang correlated** (project-standard, t0004 envelope): **0.7759** — well above
>   t0008's
> 0.316 and matching t0020's 0.7838 / t0022's 1.0 lineage
> * **DSI 12-ang uncorrelated**: **0.8557** — *higher* than correlated, opposite of paper
>   prediction
> * **DSI 8-dir correlated** (paper-match, REQ-5 target [0.30, 0.50]): **0.8182** — FAIL

</details>

<details>
<summary>✅ 0022 — <strong>Modify DSGC port with spatially-asymmetric inhibition
for channel testbed</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0022_modify_dsgc_channel_testbed` |
| **Status** | completed |
| **Effective date** | 2026-04-21 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | — |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Start time** | 2026-04-20T22:41:11Z |
| **End time** | 2026-04-21T01:50:00Z |
| **Step progress** | 12/15 |
| **Task page** | [Modify DSGC port with spatially-asymmetric inhibition for channel testbed](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Task folder** | [`t0022_modify_dsgc_channel_testbed/`](../../../tasks/t0022_modify_dsgc_channel_testbed/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0022_modify_dsgc_channel_testbed/results/results_detailed.md) |

# Modify DSGC Port with Spatially-Asymmetric Inhibition for Channel Testbed

## Motivation

The project now has two ports of the Poleg-Polsky & Diamond 2016 ModelDB 189347 DSGC model,
and neither demonstrates direction selectivity through the biologically meaningful mechanism
of postsynaptic dendritic integration of asymmetric synaptic input. Task t0008 produced
`modeldb_189347_dsgc` with DSI 0.316 and peak 18.1 Hz using a spatial-rotation proxy driver
that rotates BIP synapse coordinates per angle. Task t0020 produced
`modeldb_189347_dsgc_gabamod` with DSI 0.7838 (inside the paper's envelope [0.70, 0.85]) and
peak 14.85 Hz using the paper's native gabaMOD parameter-swap protocol, which toggles a single
global GABA scalar between PD (0.33) and ND (0.99) conditions. Both are valid scientific
reproductions, but neither produces DS via the cell's own integration of spatio-temporally
asymmetric inputs — a requirement for any downstream channel experiment that asks "does this
channel combination preserve the dendritic-computation mechanism?" Literature priors from
t0015 through t0019 provide concrete blueprints for on-the-path shunting inhibition, AIS
channel split (Nav1.6/Nav1.2 at ~7x somatic density), and E-I temporal co-tuning. This task
consolidates those priors into a channel-testbed model.

## Scope

Produce a new sibling library asset (proposed slug `modeldb_189347_dsgc_dendritic`) derived
from `modeldb_189347_dsgc`. The asset shares MOD files (HHst.mod, spike.mod) and the
RGCmodel.hoc skeleton with the two prior ports but replaces the rotation and gabaMOD drivers
with a dendritic-computation driver based on spatially-asymmetric inhibition. The driver
sweeps a moving bar across the cell in 12 directions (30 degree spacing) at a fixed biological
velocity; direction selectivity arises because inhibitory synapses are positioned or timed so
that bars moving in the null direction see inhibition arriving before excitation on any given
dendrite (shunting veto) while bars moving in the preferred direction see excitation arriving
first (pass-through). The AIS/soma/ dendrite compartments are organized into explicit `forsec`
channel-insertion blocks so follow-up tasks can add, remove, or replace channels without
editing the driver.

## Requirements

1. **Dendritic-computation DS**: stimulus is a moving bar in 12 directions (0, 30, ..., 330);
   no per-condition gabaMOD swaps or per-angle BIP coordinate rotation. DS arises from
   spatially-asymmetric inhibition (Koch-Poggio-Torre / Barlow-Levick on-the-path shunting).
2. **12-angle coverage**: `tuning_curves.csv` with columns `(angle_deg, trial_seed,
   firing_rate_hz)`, at least 10 trials per angle, >=120 rows total.
3. **Dendritic-computation only**: a single fixed mechanism set across all 12 angles; only the
   stimulus direction changes. No parameter swaps, no driver tricks.
4. **Spike output**: somatic spikes detectable at least in the preferred direction. Peak
   firing rate
   >=10 Hz target; DSI >=0.5 acceptable (hitting the paper's [40, 80] Hz peak envelope is not
   required).
5. **Channel-modular AIS**: AIS, soma, and dendrite regions in separate `forsec` blocks with
   explicit channel-insertion points. `description.md` documents how to add/remove channels
   and how to swap the spike.mod channel set.
6. **Metrics**: use t0012's `tuning_curve_loss` scorer to compute DSI, HWHM, peak firing rate,
   and per-angle reliability. Produce `score_report.json`.
7. **Comparison**: `results_detailed.md` includes a comparison table vs t0008 (rotation proxy:
   DSI 0.316, peak 18.1 Hz) and t0020 (gabaMOD swap: DSI 0.7838, peak 14.85 Hz) covering DSI,
   peak, HWHM, and reliability.

## Deliverables

* New library asset `modeldb_189347_dsgc_dendritic` (sibling to the two existing ports) with
  spatially-asymmetric-inhibition driver, channel-modular AIS, and documentation in
  `description.md`.
* `tuning_curves.csv` with 12 angles x >=10 trials = >=120 rows.
* `score_report.json` from the t0012 scorer with DSI, HWHM, peak, per-angle reliability.
* Comparison note in `results_detailed.md` quantifying differences vs t0008 and t0020.
* Channel-modularity documentation inside the new library asset's `description.md` explaining
  how to add, remove, or replace channels in each compartment without touching the driver.

## Dependencies

* `t0008_port_modeldb_189347` — source HOC/MOD files and library-asset skeleton to fork.
* `t0012_tuning_curve_scoring_loss_library` — DSI / HWHM / reliability scorer.
* `t0015_literature_survey_cable_theory` — cable-theory priors constraining dendritic geometry
  and space constants.
* `t0016_literature_survey_dendritic_computation` — on-the-path shunting prior that motivates
  the spatially-asymmetric inhibition mechanism.
* `t0017_literature_survey_patch_clamp` — AIS channel-density priors (Nav1.6/Nav1.2 ~7x
  somatic).
* `t0018_literature_survey_synaptic_integration` — E-I temporal co-tuning priors for driver
  design.
* `t0019_literature_survey_voltage_gated_channels` — Kv1/Kv3 AIS placement priors for the
  channel- modular AIS layout.

## Out of Scope

* No remote GPU compute — runs on the local Windows workstation.
* No channel-swap experiments in this task. This task delivers the testbed; follow-up tasks
  will use it to evaluate specific channel combinations (Nav1.6-only, Nav1.2-only, +Ih, Kv1 vs
  Kv3).
* No attempt to match the paper's peak firing envelope [40, 80] Hz — closing the peak gap is a
  separate investigation.
* No modifications to t0008 or t0020 assets; both ports remain intact for comparison.

**Results summary:**

> **Results Summary: Modify DSGC Port with Spatially-Asymmetric Inhibition for Channel
> Testbed**
>
> **Summary**
>
> Built the `modeldb_189347_dsgc_dendritic` library asset, a sibling to the t0008
> rotation-proxy and
> t0020 gabaMOD-swap ports of Poleg-Polsky & Diamond 2016. Direction selectivity now arises
> from
> per-dendrite E-I temporal scheduling (E leads I by **+10 ms** in the preferred half-plane; I
> leads E
> by **10 ms** in the null half-plane) on top of a channel-modular AIS partitioned into five
> `forsec`
> regions (`SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON`). The
> canonical
> 12-angle x 10-trial sweep (120 rows) yields **DSI 1.0**, **peak 15 Hz** at 120 deg, and
> **null 0
> Hz** across 150-300 deg, clearing both acceptance gates (DSI >= 0.5 and peak >= 10 Hz).
>
> **Metrics**
>
> * **Direction Selectivity Index**: **1.0** (gate >= 0.5 — pass; up from 0.316 in t0008 and
>   0.7838
> in t0020)
> * **Peak firing rate**: **15 Hz** at 120 deg (gate >= 10 Hz — pass)
> * **Null firing rate**: **0 Hz** (150-300 deg half-plane completely silenced by early
>   inhibition)
> * **HWHM**: **116.25 deg** (broader than t0008's 82.81 deg — the 120-deg lit half-plane
>   covers 5
> of 12 angles)

</details>

## 2026-04-20 (14)

## ⚠️ Intervention Blocked

<details>
<summary>⚠️ 0023 — <strong>Port Hanson 2019 DSGC model</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0023_port_hanson_2019_dsgc` |
| **Status** | intervention_blocked |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Expected assets** | 1 library, 1 paper |
| **Source suggestion** | — |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Task page** | [Port Hanson 2019 DSGC model](../../../overview/tasks/task_pages/t0023_port_hanson_2019_dsgc.md) |
| **Task folder** | [`t0023_port_hanson_2019_dsgc/`](../../../tasks/t0023_port_hanson_2019_dsgc/) |

# Port Hanson 2019 DSGC Model

## Motivation

The project currently has two direction-selective retinal ganglion cell (DSGC) ports, both
derived from the same underlying ModelDB 189347 (Poleg-Polsky & Diamond 2016) codebase. Task
t0008 produced the initial port `modeldb_189347_dsgc` using a spatial-rotation proxy driver
(DSI 0.316, peak 18.1 Hz), and task t0020 produced the sibling port
`modeldb_189347_dsgc_gabamod` using the paper's native gabaMOD scalar swap (DSI 0.7838, peak
14.85 Hz). Both share the same morphology, channel densities, and synaptic topology — so any
channel-mechanism finding drawn from them is a claim about one model, not about DSGCs in
general.

Hanson et al. 2019 published an independent DSGC implementation with distinct channel
densities, morphology detail, and synaptic placement patterns. Task t0010 identified this
model as a high-value alternative. Porting it adds a second, genuinely independent NEURON DSGC
that supports cross-model comparison of direction-selectivity mechanisms, channel
sensitivities, and dendritic computation patterns — the pattern of agreement (or disagreement)
between the two models is what makes any downstream claim robust.

## Scope

Port the Hanson et al. 2019 DSGC model into NEURON as a new library asset sibling to
`modeldb_189347_dsgc`. Reproduce the model's published direction-selective response under a
12-angle moving-bar sweep, reusing task t0022's driver infrastructure if compatible (soft
dependency) or copying from t0020 otherwise. Produce a tuning curve and score report directly
comparable to the existing ports.

## Deferred Status

This task is deferred. It is reserved and planned but must NOT be executed by the execute-task
loop until a human decision is made after reviewing t0022's outcomes. Upon creation, the
orchestrator will add an intervention file that blocks execute-task. The `status` field
remains `not_started`; the intervention file, not the status, is what suspends execution.

## Deliverables

1. New library asset (proposed slug `hanson_2019_dsgc`) containing the model's
   HOC/MOD/morphology files, `details.json`, and `description.md`, following the same layout
   as `modeldb_189347_dsgc`.
2. Source paper (Hanson et al. 2019) downloaded and registered as a paper asset, if not
   already present in the project.
3. A 12-angle moving-bar tuning curve producing `tuning_curves.csv` and `score_report.json`,
   using t0022's driver if compatible or a port of t0020's driver otherwise.
4. Comparison section in `results/results_detailed.md` reporting DSI, peak firing rate, HWHM,
   and reliability against t0008, t0020, and t0022.

## Dependencies

* `t0008_port_modeldb_189347` — reference HOC/MOD/asset layout for a NEURON DSGC library port.
* `t0012_tuning_curve_scoring_loss_library` — tuning-curve scorer applied to the new model.
* `t0022_modify_dsgc_channel_testbed` — soft dependency providing the 12-angle driver
  infrastructure; reuse if available, otherwise fall back to t0020's driver.

## Risks and Unknowns

* Simulator mismatch: Hanson et al. 2019 may use NEST, Brian, custom Python, or another
  simulator instead of NEURON. A non-NEURON source increases effort from roughly 1-2 days to
  up to a week.
* Morphology provenance: the model's morphology may come from NeuroMorpho.Org or another
  external repository and may require a separate retrieval step before porting can proceed.
* Channel mechanisms: the paper may rely on ion-channel MOD mechanisms not currently present
  in this project, requiring new `.mod` files and compilation into the existing mechanism set.

## Out of Scope

No analyses beyond the basic 12-angle tuning curve and score report. Channel-sensitivity
sweeps, parameter-space exploration, dendritic-computation decomposition,
optogenetic/pharmacological perturbation studies, or other downstream analyses belong to
follow-up tasks and must not be performed here.

</details>

## ✅ Completed

<details>
<summary>✅ 0021 — <strong>Brainstorm Session 4: DSGC Model Channel Testbed</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0021_brainstorm_results_4` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md), [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md), [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md), [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md), [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md), [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Start time** | 2026-04-20T10:00:00Z |
| **End time** | 2026-04-20T14:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm Session 4: DSGC Model Channel Testbed](../../../overview/tasks/task_pages/t0021_brainstorm_results_4.md) |
| **Task folder** | [`t0021_brainstorm_results_4/`](../../../tasks/t0021_brainstorm_results_4/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0021_brainstorm_results_4/results/results_detailed.md) |

# Brainstorm Session 4 — DSGC Model Channel Testbed

## Context

The project has completed three task waves and reached a pivotal diagnostic milestone:

* **Wave 1** (t0001-t0005): foundational brainstorm, DSGC-focused compartmental-model
  literature survey, simulator survey, canonical target tuning curve, baseline DSGC morphology
  download.
* **Wave 2** (t0007-t0013, planned by t0006): NEURON install, a first port of ModelDB 189347
  (t0008), calibration, visualisation, scoring, and provenance tasks.
* **Wave 3** (t0015-t0019, planned by t0014): five category-scoped literature surveys
  producing five answer-asset blueprints covering AIS compartment, Nav1.6/Nav1.2/Kv1 channels,
  NMDARs with Mg2+ block, GABA_A shunting, E-I temporal co-tuning, and SAC asymmetric
  inhibition.
* **Diagnostic task** (t0020): reproduced Poleg-Polsky 2016 DSGC under the native `gabaMOD`
  swap protocol and confirmed DSI 0.7838 (inside the envelope [0.70, 0.85]), while the peak
  firing rate 14.85 Hz sits below the [40, 80] Hz envelope. This confirmed the t0008
  `S-0008-02` hypothesis that the earlier low DSI was a protocol mismatch rather than a port
  bug.

The project now holds 20 tasks, 82 active suggestions (29 high, 41 medium, 12 low), and $0
spent against a $1 dev-phase budget. The literature blueprints and a working (if under-firing)
native port are in place, but the project still lacks a DSGC model suitable for
channel-mechanism testing.

## Session Goal

Decide the next experimental wave. The researcher framed the core gap: "we still lack a decent
DSGC model for testing different channels. It must (1) show DS via internal dendritic
computation, (2) cover 8-12 directions (not just PD/ND), (3) turn local activation+inhibition
into spikes." A DSI threshold of at least 0.5 is acceptable; peak firing rate need not match
the Poleg-Polsky envelope. The strategic question is whether to modify an existing model or
port a new one.

## Decisions

1. **Create t0022** — modify the existing `modeldb_189347_dsgc` library asset produced by
   t0008 to produce dendritic-computation DS via spatially-asymmetric inhibition across a
   12-angle moving-bar sweep, with a channel-modular AIS so future tasks can swap Nav/Kv
   variants. Status: `not_started`, runs immediately after this PR merges.

2. **Create t0023** — port the Hanson 2019 DSGC model as a comparison implementation alongside
   t0022. Status: `intervention_blocked`; an intervention file explains the task is deferred
   pending t0022 results before the porting effort is justified.

3. **Create t0024** — port the de Rosenroll 2026 DSGC model as a second comparison
   implementation. Status: `intervention_blocked`; an intervention file explains the same
   deferral rationale.

4. **No suggestion cleanup this round.** The researcher steered the session to model-building;
   suggestion backlog pruning is deferred to the next brainstorm.

## Out of Scope

* No experiments this session — planning-only brainstorm.
* No corrections — no prior task produced an outcome that needs correcting.
* No new asset types, task types, metrics, or categories.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0021_brainstorm_results_4"
> ---
> **Brainstorm Session 4 — Summary**
>
> **Summary**
>
> Fourth brainstorm of the project. Authorised three new tasks: t0022 (active) modifies the
> existing
> `modeldb_189347_dsgc` library asset into a channel-modular DSGC testbed that produces
> dendritic-computation DS over 12 bar angles, while t0023 (Hanson 2019 port) and t0024 (de
> Rosenroll
> 2026 port) are created `intervention_blocked` and deferred pending t0022 results. No
> suggestion
> cleanup this round.
>
> **Session Overview**
>
> * **Date**: 2026-04-20
> * **Duration**: 4 hours (10:00-14:00 UTC)
> * **Prompt**: the researcher asked for a DSGC model suitable for channel-mechanism testing,
> triggered by the t0020 diagnostic (DSI 0.7838 in-envelope, peak 14.85 Hz below envelope,
> confirmed

</details>

<details>
<summary>✅ 0020 — <strong>Port ModelDB 189347 DSGC under native gabaMOD
parameter-swap protocol</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0020_port_modeldb_189347_gabamod` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0008-02` |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Start time** | 2026-04-20T19:13:31Z |
| **End time** | 2026-04-20T20:35:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Task folder** | [`t0020_port_modeldb_189347_gabamod/`](../../../tasks/t0020_port_modeldb_189347_gabamod/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0020_port_modeldb_189347_gabamod/results/results_detailed.md) |

# Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

## Motivation

This task implements suggestion **S-0008-02** raised by t0008. The existing port
(`modeldb_189347_dsgc`, library asset produced by t0008) reaches **DSI 0.316 / peak 18.1 Hz**,
well below the Poleg-Polsky & Diamond 2016 envelope (**DSI 0.70-0.85, peak 40-80 Hz**). The
shortfall is not a bug in the port — it comes from t0008's choice to substitute a
spatial-rotation proxy for the paper's native direction-selectivity protocol.

In the original ModelDB 189347 driver the direction-selectivity test does not rotate a
stimulus. Instead it runs the *same* synaptic input pattern under two different parameter
settings of the inhibitory `gabaMOD` scalar:

* **Preferred direction (PD)**: `gabaMOD = 0.33` — weak inhibition, strong spike output.
* **Null direction (ND)**: `gabaMOD = 0.99` — strong inhibition, suppressed spike output.

The DSI emerges from the PD/ND firing-rate ratio. t0008's `run_one_trial` implementation kept
`gabaMOD` fixed and instead rotated BIP synapse coordinates around the soma, which
approximates direction tuning geometrically but does not exercise the inhibition-modulation
mechanism the paper relies on. This task adds a **second** library asset that runs the paper's
native protocol so the project can quote a fair reproduction number against the published
envelope, and so subsequent sensitivity-analysis tasks can manipulate `gabaMOD` directly.

The rotation-proxy port from t0008 stays unchanged and remains valid for direction-tuning
curves that need an explicit angle axis (e.g. tuning-curve fitting, HWHM measurement). The two
protocols are kept side by side so future tasks can pick whichever matches their question.

## Scope

Produce a **new sibling library asset** with proposed id `modeldb_189347_dsgc_gabamod`. The
new asset shares the MOD files and `RGCmodel.hoc` skeleton with `modeldb_189347_dsgc` (do not
vendor a second copy of the source HOC/MOD — load them via the path conventions established in
t0008) and replaces only the per-angle BIP rotation in `run_one_trial` with a two-condition
`gabaMOD` sweep.

In scope:

* New driver script (e.g. `code/run_gabamod_sweep.py`) that runs N PD trials and N ND trials,
  varying only the `gabaMOD` scalar between the two conditions.
* New tuning-curve CSV with schema `(condition, trial_seed, firing_rate_hz)` instead of
  t0008's `(angle_deg, trial_seed, firing_rate_hz)`. `condition` takes values `PD` and `ND`.
* Two-point envelope gate that scores the run against the published envelope using DSI from
  the PD/ND ratio and peak from the PD condition (HWHM and null are read from the
  rotation-proxy port in the comparison note — they have no analogue in the two-point
  protocol).
* Library asset metadata (`details.json`, `description.md`) registering the new asset under
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/`.

Out of scope:

* Re-deriving the underlying NEURON model. The HOC/MOD files used by t0008 are reused
  unchanged.
* Sensitivity sweeps over `gabaMOD` values other than the canonical 0.33 / 0.99 pair (proposed
  as follow-up suggestions).
* Re-fitting tuning curves with a Gaussian or von Mises function — the two-point protocol does
  not produce an angle axis.

## Approach

The work is a single implementation step plus a comparison note:

1. Initialise the new library asset folder and copy the t0008 driver as the starting point.
2. Refactor `run_one_trial` to accept a `gabaMOD` value as a keyword argument and remove the
   BIP `locx` rotation. The BIP synapse stays at its canonical position; only the inhibitory
   scalar changes between conditions.
3. Wire a new top-level driver that loops over `(condition, trial_seed)` pairs:
   * `condition = "PD"` → set `gabaMOD = 0.33` on every inhibitory point process before the
     run.
   * `condition = "ND"` → set `gabaMOD = 0.99` similarly.
   * `trial_seed` varies the RNG seed used for synaptic-release noise so each repeat is
     independent.
4. Write `tuning_curves.csv` with one row per `(condition, trial_seed)`. Default sweep: **2
   conditions × 20 trials = 40 trials per run**. Total runtime estimate: ~1.5 minutes on the
   local Windows workstation (240-trial t0008 run took ~9 minutes; 40 trials scales linearly).
5. Score the CSV with the t0012 `tuning_curve_loss` scorer using a **two-point envelope
   gate**:
   * Compute mean firing rate for PD and ND across trials.
   * `DSI = (mean_PD - mean_ND) / (mean_PD + mean_ND)`.
   * `peak = mean_PD`.
   * Pass = DSI in [0.70, 0.85] AND peak in [40, 80] Hz; fail otherwise.
6. Write `score_report.json` and a comparison table in `results/results_detailed.md` showing:
   * Rotation-proxy port (t0008): DSI / peak / null / HWHM / reliability.
   * gabaMOD-swap port (t0020): DSI / peak (null and HWHM marked N/A — no angle axis).

## Deliverables

* **New library asset**:
  `tasks/t0020_port_modeldb_189347_gabamod/assets/library/modeldb_189347_dsgc_gabamod/` with
  `details.json`, `description.md`, and the gabaMOD-swap driver code under
  `assets/library/modeldb_189347_dsgc_gabamod/code/`.
* **Tuning curves CSV**: `data/tuning_curves.csv` with columns `(condition, trial_seed,
  firing_rate_hz)`.
* **Score report**: `results/score_report.json` produced by the t0012 scorer with the
  two-point envelope gate, including DSI, peak, pass/fail, and the envelope used.
* **Comparison note**: a section in `results/results_detailed.md` quantifying how the
  gabaMOD-swap port differs from the t0008 rotation-proxy port on DSI, peak, null, and HWHM.
  The note must be embedded in `results_detailed.md`, not a separate file, so it shows up in
  the materialized overview.
* **Charts**: bar chart of mean firing rate by condition (PD vs ND, with per-trial scatter)
  saved to `results/images/` and embedded in `results_detailed.md`.

## Dependencies

* `t0008_port_modeldb_189347` — provides the source HOC/MOD layout, `run_one_trial` template,
  and the rotation-proxy baseline numbers used in the comparison note.
* `t0012_tuning_curve_scoring_loss_library` — provides the scorer library used to compute DSI,
  apply the envelope gate, and write `score_report.json`.

## Compute and Budget

* No remote machines. Runs locally on the Windows workstation that t0008 used. NEURON 8.2.7 +
  NetPyNE 1.1.1 are already installed.
* Estimated wall-clock: **~1.5 minutes** for the canonical 40-trial sweep (2 conditions × 20
  trials). t0008's 240-trial sweep took ~9 minutes; this sweep is 6× smaller.
* Estimated cost: **$0** (local compute, no paid API calls).

## Output Specification

CSV schema (`data/tuning_curves.csv`):

| Column | Type | Description |
| --- | --- | --- |
| `condition` | string | `PD` or `ND` |
| `trial_seed` | int | RNG seed for synaptic-release noise on this trial |
| `firing_rate_hz` | float | Mean spike rate over the stimulus window for this trial |

Score report schema (`results/score_report.json`):

* `protocol`: `"gabamod_swap"`
* `dsi`: float (PD/ND ratio)
* `peak_hz`: float (mean PD firing rate)
* `gate`: object with `dsi_min`, `dsi_max`, `peak_min`, `peak_max`, `passed` (bool)
* `n_trials_per_condition`: int

Comparison table (`results/results_detailed.md`):

| Metric | Rotation proxy (t0008) | gabaMOD swap (t0020) | Envelope |
| --- | --- | --- | --- |
| DSI | 0.316 | <measured> | 0.70-0.85 |
| Peak (Hz) | 18.1 | <measured> | 40-80 |
| Null (Hz) | 9.4 | N/A | <10 |
| HWHM (deg) | 82.81 | N/A | 60-90 |
| Reliability | 0.991 | <measured> | high |

## Verification

* `data/tuning_curves.csv` has exactly `2 * n_trials_per_condition` rows with the canonical
  schema.
* `results/score_report.json` validates against the t0012 scorer's schema.
* Library asset folder passes the library-asset verificator (mirroring the layout used by
  `modeldb_189347_dsgc` in t0008).
* Comparison table in `results_detailed.md` quotes the t0008 numbers verbatim from
  `tasks/t0008_port_modeldb_189347/results/results_summary.md` (no rounding drift).

## Risks and Fallbacks

* **gabaMOD scalar not exposed at the Python level**: if the t0008 port wraps `gabaMOD` inside
  a HOC-only context that is not directly settable from Python, the implementation may need to
  set it via `h.gabaMOD = value` as a global before instantiating the inhibitory point
  processes, or reach into each `inh_syn` object after instantiation. Either path is
  straightforward; flag in the implementation step log if a HOC patch is needed.
* **Two-point gate too permissive**: if the run produces a DSI inside the envelope but spike
  counts are unrealistically low (e.g. peak < 5 Hz), record this in the limitations section.
  The envelope is necessary but not sufficient — a follow-up suggestion can add a per-trial
  spike-count floor.
* **Driver divergence from rotation-proxy port**: the new driver must not silently
  re-introduce the `locx` rotation. The implementation step must include an assertion that BIP
  `locx` stays at its canonical value across all trials.

## Cross-references

* Source suggestion: **S-0008-02** (active, high priority, raised by t0008).
* Source paper: Poleg-Polsky & Diamond 2016, ModelDB 189347 (DOI
  `10.1016/j.neuron.2016.02.013`).
* Sibling library asset: `modeldb_189347_dsgc` from t0008 (rotation-proxy port).
* Scorer dependency: `tuning_curve_loss` library from t0012.

**Results summary:**

> **Results Summary: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol**
>
> **Summary**
>
> Built a new sibling library asset `modeldb_189347_dsgc_gabamod` that drives the Poleg-Polsky
> &
> Diamond 2016 DSGC under the paper's native two-condition `gabaMOD` swap protocol (PD = 0.33,
> ND =
> 0.99) instead of t0008's spatial-rotation proxy. The canonical 2 × 20 = 40-trial sweep
> reproduces
> the direction-selectivity contrast (**DSI 0.7838** inside the literature envelope **[0.70,
> 0.85]**)
> but the absolute firing rates remain depressed (**peak 14.85 Hz** vs envelope **[40, 80]
> Hz**), so
> the combined two-point gate fails. This matches the Risk-3 scenario anticipated in the plan
> and is
> recorded as a genuine experimental finding, not an implementation defect.
>
> **Metrics**
>
> * **Direction Selectivity Index (DSI)**: **0.7838** — inside envelope [0.70, 0.85] ✓
> * **Peak firing rate (mean PD)**: **14.85 Hz** — below envelope [40, 80] Hz ✗
> * **Null firing rate (mean ND)**: **1.80 Hz**
> * **PD firing rate stddev**: **1.59 Hz** across 20 trials
> * **ND firing rate stddev**: **1.03 Hz** across 20 trials
> * **Two-point envelope gate**: **failed** (DSI passes, peak fails)

</details>

<details>
<summary>✅ 0019 — <strong>Literature survey: voltage-gated channels in retinal
ganglion cells</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0019_literature_survey_voltage_gated_channels` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-05` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-20T12:16:45Z |
| **End time** | 2026-04-20T13:00:08Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: voltage-gated channels in retinal ganglion cells](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Task folder** | [`t0019_literature_survey_voltage_gated_channels/`](../../../tasks/t0019_literature_survey_voltage_gated_channels/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0019_literature_survey_voltage_gated_channels/results/results_detailed.md) |

# Literature survey: voltage-gated channels in retinal ganglion cells

## Motivation

Research question RQ1 (Na/K combinations) drives the project's main optimisation experiment.
Good priors on which Nav and Kv subunits are expressed in RGCs, their kinetic parameters, and
their conductance densities are needed to constrain the search space before optimisation
begins. The t0002 corpus provides DSGC modelling context but does not systematically cover
channel-expression or channel-kinetics literature. Source suggestion: S-0014-05 from
t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Nav subunit expression in RGCs — Nav1.1, Nav1.2, Nav1.6 distributions across soma, AIS,
   dendrite.
2. Kv subunit expression in RGCs — Kv1, Kv2, Kv3, Kv4, BK, SK distributions.
3. HH-family kinetic models — published rate functions, activation/inactivation curves, time
   constants.
4. Subunit co-expression patterns — Nav + Kv combinations reported in specific RGC types.
5. ModelDB MOD-file provenance — which published MOD files implement which Nav/Kv kinetics.
6. Nav/Kv conductance-density estimates — somatic vs AIS vs dendritic densities.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, including explicit ModelDB searches for
   RGC-relevant Nav and Kv MOD files.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset mapping candidate Nav/Kv combinations to published DSGC tuning-curve
   fits, with a row per combination giving the subunits, their densities, and the source
   paper.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` mapping Nav/Kv combinations to DSGC tuning-curve
  fits.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and contains a combination table with at
  least five rows keyed by Nav/Kv subunits and source paper DOI.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0019_literature_survey_voltage_gated_channels"
> ---
> **Results Summary: Voltage-Gated-Channel Literature Survey**
>
> **Summary**
>
> Surveyed **5** high-leverage voltage-gated-channel papers covering the five canonical themes
> (Nav
> subunit localisation at RGC AIS, Kv1 subunit expression at AIS, RGC HH-family kinetic rate
> functions, Nav1.6 vs Nav1.2 co-expression kinetics, AIS Nav conductance density) and
> produced one
> answer asset tabulating a Nav/Kv combination per DOI and theme. All **5** PDFs were
> paywalled
> (Wiley, Elsevier, American Physiological Society, Nature Neuroscience x2); summaries are
> based on
> Crossref abstracts plus training knowledge, and DOIs are recorded in
> `intervention/paywalled_papers.md` for manual retrieval via Sheffield institutional access.
>
> **Metrics**
>
> * **papers_built**: **5** (one per theme: VanWart2006, KoleLetzkus2007,
>   FohlmeisterMiller1997,
> Hu2009, Kole2008)

</details>

<details>
<summary>✅ 0018 — <strong>Literature survey: synaptic integration in RGC-adjacent
systems</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0018_literature_survey_synaptic_integration` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-04` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-20T11:18:49Z |
| **End time** | 2026-04-20T12:15:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: synaptic integration in RGC-adjacent systems](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Task folder** | [`t0018_literature_survey_synaptic_integration/`](../../../tasks/t0018_literature_survey_synaptic_integration/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0018_literature_survey_synaptic_integration/results/results_detailed.md) |

# Literature survey: synaptic integration in RGC-adjacent systems

## Motivation

Research question RQ3 (AMPA/GABA balance) and later synaptic-parameter optimisation need prior
distributions for receptor kinetics, E-I ratios, and spatial-distribution patterns. The
modelling literature in t0002 touches these parameters but does not systematically cover the
synaptic- integration experimental and theoretical work that underpins them. Source
suggestion: S-0014-04 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. AMPA/NMDA/GABA receptor kinetics — rise and decay time constants, reversal potentials.
2. Shunting inhibition — location-dependent vetoing, input resistance changes.
3. E-I balance — temporal co-tuning, conductance ratios in retinal and cortical systems.
4. Temporal summation — how closely spaced inputs integrate vs saturate.
5. Dendritic-location dependence — soma-vs-dendrite integration, attenuation before the spike
   initiation zone.
6. Synaptic-density scaling — synapses per micrometre of dendrite, bouton counts.
7. SAC/DSGC inhibitory asymmetry — starburst amacrine cell GABA output onto DSGC dendrites in
   the preferred vs null directions.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, preferring studies that publish fitted
   kinetic parameters or conductance-ratio measurements rather than qualitative reports.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset tabulating receptor kinetics and E-I ratios usable as prior
   distributions for later optimisation tasks.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` with a prior-distribution table for kinetics and E-I
  ratios, keyed by paper DOI and region.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and provides a numeric prior-distribution
  table.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0018_literature_survey_synaptic_integration"
> ---
> **Results Summary: Synaptic-Integration Literature Survey**
>
> **Summary**
>
> Surveyed **5** high-leverage synaptic-integration papers covering the five canonical themes
> (AMPA/NMDA/GABA receptor kinetics, shunting inhibition, E-I balance temporal co-tuning,
> dendritic-location-dependent PSP integration, SAC-to-DSGC inhibitory asymmetry) and produced
> one
> answer asset tabulating a prior distribution per DOI and theme. All **5** PDFs were
> paywalled
> (Nature, PNAS, Current Opinion in Neurobiology); summaries are based on Crossref abstracts
> plus
> training knowledge, and DOIs are recorded in `intervention/paywalled_papers.md` for manual
> retrieval
> via Sheffield institutional access.
>
> **Metrics**
>
> * **papers_built**: **5** (one per theme: Lester1990, KochPoggio1983, WehrZador2003,
>   HausserMel2003,
> EulerDetwilerDenk2002)

</details>

<details>
<summary>✅ 0017 — <strong>Literature survey: patch-clamp recordings of RGCs and
DSGCs</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0017_literature_survey_patch_clamp` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-03` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-19T23:39:05Z |
| **End time** | 2026-04-20T11:08:30Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: patch-clamp recordings of RGCs and DSGCs](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Task folder** | [`t0017_literature_survey_patch_clamp/`](../../../tasks/t0017_literature_survey_patch_clamp/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0017_literature_survey_patch_clamp/results/results_detailed.md) |

# Literature survey: patch-clamp recordings of RGCs and DSGCs

## Motivation

The DSGC model needs validation against real electrophysiology. Patch-clamp recordings of
retinal ganglion cells provide the quantitative targets that optimisation and tuning-curve
scoring tasks (t0004, t0012) must match: somatic action-potential rates, EPSP/IPSC kinetics,
null/preferred response ratios. This survey assembles the experimental-data landscape
separately from the modelling corpus in t0002. Source suggestion: S-0014-03 from
t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Somatic whole-cell recordings of RGCs — firing-rate statistics, spike-threshold
   distributions.
2. Voltage-clamp conductance dissections — separating AMPA/NMDA/GABA currents during DS
   responses.
3. Space-clamp error analyses — how much of published conductance asymmetry is real vs an
   artefact of imperfect voltage clamp in extended dendrites.
4. Spike-train tuning-curve measurements — angle-resolved AP rates and their variability.
5. In-vitro stimulus protocols — moving bars, drifting gratings, and spots used to probe DS.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, giving weight to papers that publish raw
   conductance traces or tabulated tuning-curve peak rates.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset mapping each paper to the model-validation targets it provides (AP
   rate, IPSC asymmetry, EPSP kinetics, null/preferred ratios) with explicit numerical values.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` with a validation-target table keyed by paper DOI.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and contains a validation-target table with
  at least five numerical rows.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

**Results summary:**

> **Results Summary: Patch-Clamp Literature Survey**
>
> **Summary**
>
> Surveyed 5 high-leverage patch-clamp / voltage-clamp / space-clamp / DSGC papers and
> produced a
> single answer asset giving a concrete 7-point compartmental-modelling specification for
> DSGCs in
> NEURON covering voltage-clamp pipeline, AIS compartment, NMDAR synaptic complement, and
> intrinsic vs
> synaptic maintained-activity biophysics. All 5 PDFs failed to download (4 paywalls + 1
> Cloudflare/cookie-wall); summaries are based on Crossref abstracts plus training knowledge
> with
> explicit disclaimers.
>
> **Objective**
>
> Survey foundational patch-clamp / voltage-clamp / space-clamp literature and synthesize
> concrete
> compartmental-modelling guidance for direction-selective retinal ganglion cells (DSGCs) in
> NEURON,
> covering experimental technique bias corrections and DSGC-specific biophysics.
>
> **What Was Produced**
>
> * **5 paper assets** covering the core patch-clamp / DSGC-biophysics literature:

</details>

<details>
<summary>✅ 0016 — <strong>Literature survey: dendritic computation beyond
DSGCs</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0016_literature_survey_dendritic_computation` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 25 paper, 1 answer |
| **Source suggestion** | `S-0014-02` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-19T23:38:58Z |
| **End time** | 2026-04-20T10:36:25Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: dendritic computation beyond DSGCs](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Task folder** | [`t0016_literature_survey_dendritic_computation/`](../../../tasks/t0016_literature_survey_dendritic_computation/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0016_literature_survey_dendritic_computation/results/results_detailed.md) |

# Literature survey: dendritic computation beyond DSGCs

## Motivation

Research question RQ4 (active vs passive dendrites) needs evidence from computational
neuroscience beyond the retinal literature. Cortical and cerebellar dendrites have been
studied far more extensively than DSGC dendrites, and the mechanisms and modelling conventions
developed there (NMDA spikes, Ca/Na plateaus, branch-level nonlinearities) are the natural
reference for whether active dendrites plausibly shape DSGC tuning curves. Source suggestion:
S-0014-02 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. NMDA spikes — thresholds, amplitudes, distance-dependence, supralinear integration.
2. Na+ and Ca2+ dendritic spikes — backpropagation, forward propagation, local spikes.
3. Plateau potentials — in-vivo evidence, role in coincidence detection, duration scaling.
4. Branch-level nonlinearities — independent subunits, clustered-vs-distributed input
   summation.
5. Sublinear-to-supralinear integration regimes — what controls the transition, which
   conditions make dendrites behave passively in practice.
6. Active-vs-passive modelling comparisons — cortical, cerebellar, hippocampal studies that
   built matched active and passive compartmental models and quantified the difference.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each of the six themes above with preference for review
   articles plus 2-4 primary studies per theme.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md` for the
   researcher to retrieve manually.
3. Write one answer asset synthesising which dendritic-computation mechanisms plausibly
   transfer to DSGC dendrites, with explicit caveats about anatomical and biophysical
   differences.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant), some possibly with
  `download_status: "failed"`.
* One answer asset under `assets/answer/` synthesising the six themes and flagging mechanisms
  most plausible for DSGC dendrites.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and explicitly addresses transferability to
  DSGC dendrites.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

**Results summary:**

> **Results Summary: Dendritic-Computation Literature Survey**
>
> **Summary**
>
> Surveyed 5 foundational dendritic-computation papers (Schiller 2000, Polsky 2004, Larkum
> 1999,
> Bittner 2017, London & Hausser 2005) and produced a single answer asset synthesising which
> dendritic-computation motifs plausibly transfer to DSGC dendrites and the biophysical
> caveats on
> each transfer. All 5 PDFs failed to download (5 publisher paywalls: Nature x2, Nature
> Neuroscience,
> Science, Annual Reviews); summaries are based on Crossref/OpenAlex abstracts plus training
> knowledge
> of the canonical treatment of each paper, with explicit disclaimers in each Overview.
>
> **Objective**
>
> Survey the foundational dendritic-computation literature (NMDA spikes, Ca2+ dendritic
> spikes, BAC
> firing, plateau potentials/BTSP, branch-level nonlinear integration, and regime switching)
> and
> synthesise a single answer asset mapping which motifs plausibly transfer to DSGC dendrites
> and the
> biophysical caveats on each transfer.
>
> **What Was Produced**
>

</details>

<details>
<summary>✅ 0015 — <strong>Literature survey: cable theory and dendritic
filtering</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0015_literature_survey_cable_theory` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | — |
| **Expected assets** | 5 paper, 1 answer |
| **Source suggestion** | `S-0014-01` |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-19T23:38:43Z |
| **End time** | 2026-04-20T10:00:00Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: cable theory and dendritic filtering](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Task folder** | [`t0015_literature_survey_cable_theory/`](../../../tasks/t0015_literature_survey_cable_theory/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0015_literature_survey_cable_theory/results/results_detailed.md) |

# Literature survey: cable theory and dendritic filtering

## Motivation

The t0002 corpus concentrates on direction-selective retinal ganglion cell (DSGC)
compartmental models. Downstream calibration and optimisation tasks (segment discretisation,
morphology-sensitive tuning, dendritic attenuation) need a deeper grounding in classical cable
theory and passive dendritic filtering than t0002 provides. This task broadens the corpus into
the foundational theory. Source suggestion: S-0014-01 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. Rall-era foundations — passive cable equation, equivalent cylinder, classical Rall papers.
2. Segment discretisation guidelines — `d_lambda` rule, spatial-frequency constraints on
   `nseg`.
3. Branched-tree impedance — transfer impedance, voltage attenuation in branched dendrites.
4. Frequency-domain analyses — input impedance, synaptic-event filtering, chirp / ZAP
   analyses.
5. Transmission in thin dendrites — space constant, propagation failure, passive integration
   limits.

Exclusion: do not re-add any DOI already present in the t0002 corpus (20 DOIs under
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`). Duplicates
discovered mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` with search terms targeting each of the five themes above.
2. For each shortlisted paper, invoke `/download-paper` — the skill produces a v3-compliant
   paper asset (`details.json`, summary document, files). Papers behind institutional paywalls
   are recorded as `download_status: "failed"` and added to `intervention/paywalled_papers.md`
   for the researcher to retrieve manually from their institutional account.
3. After the paper set is assembled, write one answer asset that synthesises the corpus by
   theme and maps each paper to its relevance for the project's direction-selectivity
   modelling work.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant). Some may have `download_status:
  "failed"` pending manual retrieval.
* One answer asset under `assets/answer/` synthesising the five themes and identifying the
  cable-theory parameters most directly useful for downstream DSGC tasks.
* `intervention/paywalled_papers.md` listing DOIs the researcher must download manually.

## Compute and Budget

No paid services required for the automated pass. The task type `literature-survey` is gated
on the project budget — the brainstorm session set `project/budget.json` `total_budget` to $1
to clear the gate; no actual spend is expected.

## Dependencies

None. This task is independent of the t0002 corpus (beyond the deduplication constraint).

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py` (accounting for some paywalled
  failures).
* The answer asset passes `verify_answer_asset.py`.
* `intervention/paywalled_papers.md` exists with a DOI list if any downloads failed.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

**Results summary:**

> **Results Summary: Cable-Theory Literature Survey**
>
> **Summary**
>
> Surveyed 5 foundational cable-theory and DSGC-biophysics papers and produced a single answer
> asset
> giving a concrete 6-point compartmental-modelling specification for DSGCs in NEURON. All 5
> PDFs
> failed to download (4 paywalls + 1 Cloudflare block); summaries are based on
> Crossref/OpenAlex
> abstracts plus training knowledge with explicit disclaimers.
>
> **Objective**
>
> Survey foundational cable-theory and dendritic-computation literature and synthesize
> concrete
> compartmental-modelling guidance for direction-selective retinal ganglion cells (DSGCs) in
> NEURON.
>
> **What Was Produced**
>
> * **5 paper assets** covering the core cable-theory / DSGC-biophysics literature:
> * Rall 1967 — cable-theoretic foundations and EPSP shape-index diagnostic
> * Koch, Poggio, Torre 1982 — on-the-path shunting DS mechanism
> * Mainen & Sejnowski 1996 — morphology-driven firing diversity, `d_lambda` discretization

</details>

<details>
<summary>✅ 0013 — <strong>Resolve dsgc-baseline-morphology source-paper
provenance</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0013_resolve_morphology_provenance` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0005-01` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/), [`correction`](../../../meta/task_types/correction/) |
| **Start time** | 2026-04-20T16:26:01Z |
| **End time** | 2026-04-20T17:21:30Z |
| **Step progress** | 9/15 |
| **Task page** | [Resolve dsgc-baseline-morphology source-paper provenance](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Task folder** | [`t0013_resolve_morphology_provenance/`](../../../tasks/t0013_resolve_morphology_provenance/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0013_resolve_morphology_provenance/results/results_detailed.md) |

# Resolve dsgc-baseline-morphology source-paper provenance

## Motivation

The `dsgc-baseline-morphology` dataset asset (NeuroMorpho neuron 102976, 141009_Pair1DSGC)
currently has `source_paper_id = null` because two Feller-lab 2018 papers are plausibly the
source:

* Morrie & Feller 2018 Neuron (DOI `10.1016/j.neuron.2018.05.028`) — nominated in the t0005
  download plan.
* Murphy-Baum & Feller 2018 Current Biology (DOI `10.1016/j.cub.2018.03.001`) — reported as
  the source by NeuroMorpho's metadata.

Until this is resolved, every downstream paper that uses the morphology will cite it
incorrectly or omit a citation entirely. This task downloads both candidate papers, reads
their Methods sections, confirms which one introduced the 141009_Pair1DSGC reconstruction, and
files a corrections asset that updates `dsgc-baseline-morphology.source_paper_id` to the
correct slug.

Covers suggestion **S-0005-01**.

## Scope

1. Download Morrie & Feller 2018 Neuron via `/add-paper`. Register as a v3 paper asset under
   `assets/paper/10.1016_j.neuron.2018.05.028/`.
2. Download Murphy-Baum & Feller 2018 Current Biology via `/add-paper`. Register as a v3 paper
   asset under `assets/paper/10.1016_j.cub.2018.03.001/`.
3. Read both papers' Methods sections. Look specifically for:
   * The recording date `141009` (October 9, 2014) or neighbouring dates.
   * The `Pair1DSGC` / `Pair 1 DSGC` / `paired recording` language matching the NeuroMorpho
     reconstruction metadata.
   * An explicit citation of the 141009_Pair1DSGC reconstruction or its deposit to
     NeuroMorpho.
4. If one paper is unambiguously the source, file a correction asset
   (`corrections/dataset_dsgc-baseline-morphology.json`) that sets `source_paper_id` to the
   winning paper's DOI-slug. If neither is an unambiguous match, file a correction that
   records both DOIs under a new `candidate_source_paper_ids` field and opens an intervention
   file explaining that Feller-lab contact is required.
5. Record the full reasoning in `results/results_detailed.md` so the provenance decision is
   auditable.

## Dependencies

* **t0005_download_dsgc_morphology** — owns the `dsgc-baseline-morphology` asset this task
  corrects.

## Expected Outputs

* **2 paper assets** (Morrie & Feller 2018 Neuron, Murphy-Baum & Feller 2018 Current Biology),
  both v3-spec-compliant with full summaries.
* **1 correction asset** in `corrections/dataset_dsgc-baseline-morphology.json` setting
  `source_paper_id` to the resolved winner (or documenting ambiguity).
* A provenance-reasoning section in `results/results_detailed.md`.

## Approach

1. Run `/add-paper` twice, once per DOI, following the paper-asset spec v3.
2. Read both full PDFs and extract the Methods paragraphs that describe the paired
   recording(s) from which 141009_Pair1DSGC was reconstructed.
3. If both papers cite the same recording session, pick the earlier one (lower DOI publication
   date). If only one paper cites the recording session, pick that one. If neither paper cites
   it, treat as ambiguous and flag for human review.

## Questions the task answers

1. Which Feller-lab 2018 paper introduced the 141009_Pair1DSGC reconstruction?
2. Does NeuroMorpho's metadata attribution (Murphy-Baum & Feller 2018) match the paper's
   Methods section, or does it disagree?
3. If both papers plausibly cite the recording, what are the tie-breakers?

## Risks and Fallbacks

* **Neither paper explicitly cites the 141009 reconstruction**: file an intervention asking
  the researcher to email the Feller lab. Do not silently pick one.
* **Both papers cite it**: pick the earlier publication date and document the tie-break.
* **Paper downloads fail (paywall / captcha)**: fall back to metadata-only paper assets (v3
  spec `download_status: "failed"`) and raise an intervention file requesting library access.

**Results summary:**

> **Results Summary: Resolve DSGC Morphology Provenance**
>
> **Summary**
>
> Closed the provenance gap on `dsgc-baseline-morphology.source_paper_id`. Registered both
> candidate
> Feller-lab 2018 papers as v3 paper assets, read their Methods sections, applied the
> pre-specified
> decision procedure, and filed a single correction that sets `source_paper_id` to
> `10.1016_j.cub.2018.03.001` (Morrie & Feller 2018 *Current Biology*, "A Dense Starburst
> Plexus Is
> Critical for Generating Direction Selectivity"). Discovered along the way that the t0005
> plan's
> "Morrie & Feller 2018 *Neuron*" DOI nomination was an error: `10.1016/j.neuron.2018.05.028`
> resolves
> to Li, Vaughan, Sturgill & Kepecs (2018), an unrelated CSHL viral-tracing paper.
>
> **Metrics**
>
> * **Paper assets registered**: **2** (expected: 2)
> * **Correction assets produced**: **1** (`C-0013-01`)
> * **Winning source paper**: `10.1016_j.cub.2018.03.001` (Morrie & Feller 2018, *Current
>   Biology*)
> * **Decision branch taken**: criterion 1 ("exactly one paper's Methods cites the
>   reconstruction")
> * **PDFs successfully downloaded**: **1/2** (CB open-access on eScholarship; Neuron DOI
>   paywalled
> and metadata-only per v3 spec)

</details>

<details>
<summary>✅ 0012 — <strong>Tuning-curve scoring loss library</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0012_tuning_curve_scoring_loss_library` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-09` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-20T01:02:11Z |
| **End time** | 2026-04-20T09:58:10Z |
| **Step progress** | 10/15 |
| **Task page** | [Tuning-curve scoring loss library](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Task folder** | [`t0012_tuning_curve_scoring_loss_library/`](../../../tasks/t0012_tuning_curve_scoring_loss_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0012_tuning_curve_scoring_loss_library/results/results_detailed.md) |

# Tuning-curve scoring loss library

## Motivation

The t0002 literature survey set four concurrent quantitative targets an optimised DSGC model
must hit: DSI **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM
**60-90°**. The project has four registered metrics (`direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`). Every downstream
optimisation task (Na/K grid search S-0002-01, morphology sweep S-0002-04, E/I ratio scan
S-0002-05, active-vs-passive dendrites S-0002-02) needs a shared scoring function: same
target, same weighting, same tie-breaks. Without this library, each task will invent its own
scoring and cross-task comparisons of "who wins" become meaningless. This task provides that
canonical scorer.

Covers suggestion **S-0002-09** (and subsumes **S-0004-03** — see the t0006 correction file).

## Scope

The library `tuning_curve_loss` exposes:

1. `score(simulated_curve_csv, target_curve_csv | None) -> ScoreReport` — returns a frozen
   dataclass containing:
   * `loss_scalar` (float) — weighted-Euclidean-distance-in-normalised-space loss combining
     the four envelope targets.
   * `dsi_residual`, `peak_residual_hz`, `null_residual_hz`, `hwhm_residual_deg` — individual
     residuals with signs.
   * `rmse_vs_target` — point-wise RMSE of `(angle, firing_rate)` against the target curve
     (only when a target is supplied).
   * `reliability` — cross-trial coefficient of determination (maps onto the registered
     `tuning_curve_reliability` metric).
   * `passes_envelope` (bool) — whether the simulated curve lands inside the t0002 envelope on
     all four targets simultaneously.
   * `per_target_pass` — dict `{"dsi": bool, "peak": bool, "null": bool, "hwhm": bool}`.
2. `compute_dsi(curve_csv) -> float`
3. `compute_preferred_peak_hz(curve_csv) -> float`
4. `compute_null_residual_hz(curve_csv) -> float`
5. `compute_hwhm_deg(curve_csv) -> float`
6. Tuning-curve CSV schema constant: `(angle_deg, trial_seed, firing_rate_hz)`.
7. CLI: `python -m tuning_curve_loss.cli <simulated.csv> [--target <target.csv>]`.

Weights for the scalar loss default to **DSI 0.25, peak 0.25, null 0.25, HWHM 0.25** but are
user-overridable via a keyword argument and via a JSON config file; the defaults and rationale
are documented in the asset's `description.md`.

## Dependencies

* **t0004_generate_target_tuning_curve** — source of the canonical `target-tuning-curve`
  dataset used as the default comparison target and as the smoke-test fixture.

## Expected Outputs

* **1 library asset** (`assets/library/tuning-curve-loss/`) with:
  * `description.md` covering API, weight defaults, and worked examples
  * `module_paths` pointing at `code/tuning_curve_loss/`
  * `test_paths` pointing at `code/tuning_curve_loss/test_*.py` with at least:
    * Identity test: `score(target, target)` must return `loss_scalar == 0.0` and
      `passes_envelope is True`.
    * Envelope-boundary tests: hand-crafted curves just inside and just outside each of the
      four envelope boundaries.
    * Reliability test: two curves with identical trial-means but very different
      trial-to-trial variance produce different `reliability` values.

## Approach

Pure Python + NumPy + pandas. No simulator dependency. The DSI and HWHM computations must
match the closed-form computations used in t0004 to produce the target curve, so that
`score(target, target)` is exactly zero. Use the registered metric keys from `meta/metrics/`
so that scored values can be written directly into `results/metrics.json` without post-hoc
renaming.

## Questions the task answers

1. Does `score(target, target)` return `loss_scalar == 0.0`?
2. Do the envelope-boundary tests flip `passes_envelope` at the correct boundary to within
   floating-point tolerance?
3. Does the scorer accept multi-trial CSVs and correctly combine trials into a mean before
   computing DSI, peak, null and HWHM?

## Risks and Fallbacks

* **The literature envelope numbers conflict with the t0004 target curve** (e.g., the target
  sits right at an envelope boundary): document the target's position on the envelope in the
  library description; do not silently redefine targets.
* **Trial-to-trial variance inflates `reliability` beyond sensible bounds**: clamp to [0, 1]
  and document the clamp.

**Results summary:**

> **Results Summary: Tuning-Curve Scoring Loss Library**
>
> **Summary**
>
> Built and registered the `tuning_curve_loss` Python library: an 8-module package that loads
> a DSGC
> tuning curve from CSV, computes DSI, peak, null, and HWHM, and scores a candidate curve
> against the
> t0004 target as a weighted Euclidean residual in envelope-half-width units. The identity
> gate
> `score(target, target).loss_scalar == 0.0` and `passes_envelope is True` holds exactly. All
> 47
> pytest tests pass, ruff and mypy are clean, and the library asset is registered at
> `assets/library/tuning_curve_loss/`.
>
> **Metrics**
>
> * **Tests passed**: **47 / 47** (0 failed, 0 skipped)
> * **Identity loss on t0004 target**: **0.0** (exact)
> * **Library modules**: **8** (paths, loader, metrics, envelope, weights, scoring, cli,
>   `__init__`)
> * **Public entry points**: **13** (score, compute_dsi, compute_peak_hz, compute_null_hz,
> compute_hwhm_deg, compute_reliability, load_tuning_curve, passes_envelope, validate_weights,
> load_weights_from_json, Envelope, ScoreResult, TuningCurveMetrics)
> * **Test modules**: **5** covering loader, metrics, envelope, scoring, and CLI

</details>

<details>
<summary>✅ 0011 — <strong>Response-visualisation library (firing rate vs angle
graphs)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0011_response_visualization_library` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | — |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-20T14:52:53Z |
| **End time** | 2026-04-20T15:50:00Z |
| **Step progress** | 10/15 |
| **Task page** | [Response-visualisation library (firing rate vs angle graphs)](../../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Task folder** | [`t0011_response_visualization_library/`](../../../tasks/t0011_response_visualization_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0011_response_visualization_library/results/results_detailed.md) |

# Response-visualisation library (firing rate vs angle graphs)

## Motivation

Every downstream experiment in this project will produce angle-resolved firing-rate data
(tuning curves). Without a shared visualisation library, each task will re-implement its own
plotting code, the plots will drift in style, and cross-model comparisons will need manual
re-work. This task builds one library, used by every later task, that turns a standard-schema
tuning-curve CSV into a consistent set of publication-quality PNGs.

## Scope

The library `tuning_curve_viz` exposes four plotting functions:

1. `plot_cartesian_tuning_curve(curve_csv, out_png, *, show_trials=True, target_csv=None)` —
   firing rate (Hz) vs direction (deg). Shows per-trial points, mean line, and a 95% bootstrap
   confidence band. Optional overlay of a target curve (dashed line) from t0004's
   `target-tuning-curve`.
2. `plot_polar_tuning_curve(curve_csv, out_png, *, target_csv=None)` — classical polar plot
   with the preferred direction annotated.
3. `plot_multi_model_overlay(curves_dict, out_png, *, target_csv=None)` — side-by-side
   Cartesian + polar overlay of multiple models (e.g., the Poleg-Polsky port from t0008, any
   models ported in t0010, and the canonical target curve).
4. `plot_angle_raster_psth(spike_times_csv, out_png, *, angle_deg)` — per-trial spike raster
   above a PSTH (Peri-Stimulus-Time Histogram), one figure per angle.

A CLI `tuning_curve_viz.cli` consumes a tuning-curve CSV path and produces all four plot types
into an output directory.

## Dependencies

* **t0004_generate_target_tuning_curve** — source of the canonical target curve for overlays
  and the smoke-test fixture.
* **t0008_port_modeldb_189347** — provides a real simulated tuning curve to smoke-test the
  library against alongside the target.

## Expected Outputs

* **1 library asset** (`assets/library/tuning-curve-viz/`) with:
  * `description.md` covering purpose, API, and example usage.
  * `module_paths` pointing at `code/tuning_curve_viz/`.
  * `test_paths` pointing at `code/tuning_curve_viz/test_*.py`.
  * Example output PNGs under the asset's `files/` (smoke-test outputs against
    `target-tuning-curve` and the t0008 simulated curve).

## Approach

Standard matplotlib + pandas. Tuning-curve CSV schema is fixed at `(angle_deg, trial_seed,
firing_rate_hz)`. Use `bootstrap` from scipy (or a small local implementation) for the 95% CI
band. For the multi-model overlay, auto-pick a colour-blind-safe palette (Okabe-Ito). No
animated plots, no interactive plots; PNG output only.

Smoke tests:

1. Generate all four plot types against `target-tuning-curve` (the pre-existing canonical
   curve).
2. Generate all four plot types against the t0008 Poleg-Polsky port's simulated tuning curve.
3. Generate the `plot_multi_model_overlay` figure combining both with the target as a dashed
   overlay.

Each smoke-test writes its output PNG to the library asset's `files/` folder so the asset
itself demonstrates what each plot looks like.

## Questions the task answers

1. Does the library produce all four plot types on the canonical target curve without errors?
2. Does it produce all four plot types on a real simulated curve (t0008) with the same code
   path?
3. Does the multi-model overlay correctly align axes and preferred-direction annotations
   across models with different angular sampling?

## Risks and Fallbacks

* **Polar-axis convention mismatch between matplotlib and the tuning-curve convention (0° =
  east)**: document the convention in the library's `description.md` and stick to
  `theta_direction=1, theta_offset=0` (standard).
* **`scipy.stats.bootstrap` unavailable**: fall back to a 4-line NumPy bootstrap.
* **Multi-model overlay becomes illegible with > 6 models**: cap overlay at 6 and surface a
  warning; the CLI batches additional models into separate PNGs.

**Results summary:**

> ---
> spec_version: "3"
> task_id: "t0011_response_visualization_library"
> date_completed: "2026-04-20"
> ---
> **Results Summary**
>
> **Summary**
>
> Built the `tuning_curve_viz` matplotlib library: **4** plotting functions (Cartesian, polar,
> multi-model overlay, raster+PSTH), a CLI, a deterministic synthetic Poisson spike fixture
> for the
> raster smoke test, and **1** library asset at `assets/library/tuning_curve_viz/`.
> Smoke-tested
> against both the t0004 target curve and the t0008 simulated curve, producing **7** example
> PNGs. The
> library imports the canonical CSV loader from t0012 rather than re-implementing schema
> parsing.
>
> **Metrics**
>
> * **Plotting functions**: **4** (`plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`,
> `plot_multi_model_overlay`, `plot_angle_raster_psth`)
> * **Python modules**: **11** under `code/tuning_curve_viz/`

</details>

<details>
<summary>✅ 0010 — <strong>Hunt DSGC compartmental models missed by prior survey;
port runnable ones</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0010_hunt_missed_dsgc_models` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`download-paper`](../../../meta/task_types/download-paper/), [`code-reproduction`](../../../meta/task_types/code-reproduction/) |
| **Start time** | 2026-04-20T12:25:27Z |
| **End time** | 2026-04-20T14:42:24Z |
| **Step progress** | 12/15 |
| **Task page** | [Hunt DSGC compartmental models missed by prior survey; port runnable ones](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Task folder** | [`t0010_hunt_missed_dsgc_models/`](../../../tasks/t0010_hunt_missed_dsgc_models/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0010_hunt_missed_dsgc_models/results/results_detailed.md) |

# Hunt DSGC compartmental models missed by t0002 and t0008; port any with code

## Motivation

The t0002 literature survey built a 20-paper corpus biased toward the six seed references from
`project/description.md` and adjacent DSGC papers. The t0008 ModelDB port focussed on entry
189347 (Poleg-Polsky & Diamond 2016) and its immediate siblings. Neither task exhaustively
searched post-2020 publications, non-ModelDB repositories (GitHub / OSF / Zenodo /
institutional pages), or adjacent computational neuroscience venues (NeurIPS, Cosyne, bioRxiv)
for DSGC compartmental models. This task closes that gap: actively hunt for DSGC compartmental
models the project might have missed, download their papers, and port any models that have
runnable code and are scientifically relevant.

## Scope

1. **Systematic search** across:
   * ModelDB full listing under keywords `direction selective`, `retina`, `DSGC`, `RGC`,
     `Starburst`, `SAC` (broader than the t0008 sweep).
   * GitHub search: `DSGC`, `retinal ganglion direction`, `NetPyNE direction`, `Arbor retina`,
     `NEURON DSGC`.
   * Google Scholar + Semantic Scholar forward-citation chains of:
     * Poleg-Polsky & Diamond 2016
     * Schachter et al. 2010
     * Park et al. 2014
     * Sethuramanujam et al. 2016
     * Hanson et al. 2019
   * bioRxiv + preprint servers, 2023-2025, keyword `direction-selective ganglion cell`.
2. **Download** any paper not already in `assets/paper/` that meets the inclusion bar:
   publishes a compartmental (not rate-coded / not purely statistical) DSGC model with at
   least partial biophysical detail.
3. **Port** any paper with public code that:
   * Runs in Python 3.12 + NEURON 8.2.7 (or Arbor 0.12.0).
   * Can load `dsgc-baseline-morphology-calibrated` or bring its own morphology.
   * Produces an angle-resolved tuning curve.
4. **Report** every candidate in a single answer asset with a per-model row: paper DOI, code
   URL, NEURON compatibility, whether ported, and if not, why not.

## Dependencies

* **t0008_port_modeldb_189347** — gives us a working NEURON-based reference implementation to
  contrast with any newly ported model and a pattern for how to port additional models.

## Expected Outputs

* **1 answer asset** (`assets/answer/missed-dsgc-models-hunt-report/`) summarising every
  candidate found and the outcome of each port attempt.
* **N paper assets** for any new papers (DOI-keyed, v3-spec-compliant). Exact count depends on
  what the search turns up.
* **0 or more library assets** for any successfully ported models
  (`assets/library/<model-slug>/`). Exact count depends on what was portable.
* **Simulated tuning-curve CSVs** under `data/tuning_curves/` for every ported model,
  formatted identically to the t0008 outputs so t0011 can render them side-by-side.

## Approach

Run the search in three passes (ModelDB full sweep, GitHub + OSF + Zenodo, Google Scholar
forward citations). Maintain a single `data/candidates.csv` that grows across passes and
records duplicate-vs-new status against t0002's corpus. Decide portability by actually cloning
the repo and running the demo, not by reading the README; record every port attempt's
stdout/stderr under `logs/` so reviewers can audit the call.

## Questions the task answers

1. Which DSGC compartmental models exist in the literature or in public code that the t0002
   survey and the t0008 ModelDB port missed?
2. Of those, which have runnable public code in this environment?
3. How does each successfully ported model's tuning curve compare with the t0008 Poleg-Polsky
   reproduction and with the canonical `target-tuning-curve`?
4. Are there consistent disagreements across ports (e.g., systematically narrower HWHM, higher
   null firing) that warrant new experiment suggestions?

## Risks and Fallbacks

* **Search finds no new portable models**: document the gap as a new suggestion; the answer
  asset's table should still be produced listing every candidate considered and why each was
  excluded.
* **Port attempts consistently fail**: surface that as a finding — published DSGC
  compartmental code is often fragile — rather than inventing fixes that change the original
  model's behaviour.
* **Search produces too many candidates to port within this task**: triage by (a) citation
  count, (b) publication year (newer first), (c) whether the code is in a simulator already on
  this workstation. Port the top 3-5 and list the rest as suggestions.

**Results summary:**

> **Results Summary: Hunt DSGC Compartmental Models Missed by Prior Survey**
>
> **Summary**
>
> Executed a three-pass literature + public-code hunt for DSGC compartmental models missed by
> t0002
> and t0008. Registered the two new qualifying papers (deRosenroll 2026 Cell Reports,
> Poleg-Polsky
> 2026 Nat Commun) and attempted three HIGH-priority ports (Hanson 2019, deRosenroll 2026,
> Poleg-Polsky 2026). All three ports exited at P2 (upstream demo) within the 90-minute
> wall-clock
> budget due to structural driver incompatibility with the canonical 12-angle x 20-trial
> sweep, not
> biophysics bugs. Produced one answer asset summarising every candidate and outcome.
>
> **Metrics**
>
> * **Candidates found**: **14** (3 HIGH-priority, 2 MEDIUM, 1 LOW, 8 DROP) across 37 queries
> * **New papers registered**: **2** (one `download_status=success`, one
>   `download_status=failed` due
> to Elsevier HTTP 403 on anonymous access)
> * **Port attempts**: **3/3 HIGH-priority** completed and logged; **0/3 reached P3**
>   (canonical
> sweep); all three marked `p2_failed` with explicit structural-block reasons
> * **Library assets produced**: **0** (plan explicitly permits this outcome; no broken
>   scaffolds were
> left behind)

</details>

<details>
<summary>✅ 0009 — <strong>Calibrate dendritic diameters for
dsgc-baseline-morphology</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0009_calibrate_dendritic_diameters` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0005-02` |
| **Task types** | [`feature-engineering`](../../../meta/task_types/feature-engineering/), [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-04-19T21:37:04Z |
| **End time** | 2026-04-20T00:12:29Z |
| **Step progress** | 12/15 |
| **Task page** | [Calibrate dendritic diameters for dsgc-baseline-morphology](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Task folder** | [`t0009_calibrate_dendritic_diameters/`](../../../tasks/t0009_calibrate_dendritic_diameters/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0009_calibrate_dendritic_diameters/results/results_detailed.md) |

# Calibrate dendritic diameters for dsgc-baseline-morphology

## Motivation

Every compartment in the downloaded `dsgc-baseline-morphology` CNG-curated SWC (NeuroMorpho
neuron 102976, 141009_Pair1DSGC) carries the placeholder radius **0.125 µm** because the
original Simple Neurite Tracer reconstruction did not record diameters. Cable theory predicts
that segment diameter is the single most influential *local-electrotonic* knob on axial
resistance, spatial attenuation and spike-initiation threshold, so leaving a uniform
placeholder in place will silently bias every downstream biophysical simulation. This task
replaces the placeholder with a literature-derived order-dependent taper keyed on Strahler
order or path distance from the soma, and registers the calibrated morphology as a new dataset
asset that downstream tasks (t0008 reproduction, t0011 visualisation smoke-test, and the
experiment tasks) will load instead of the raw placeholder SWC.

Covers suggestion **S-0005-02**.

## Scope

1. **Research stage**: survey the published mouse ON-OFF DSGC morphometric literature for a
   defensible diameter taper rule. Candidate sources explicitly identified as plausible:
   * Vaney / Sivyer / Taylor 2012 review + original figures
   * Poleg-Polsky & Diamond 2016 (ModelDB 189347) per-order diameter profile
   * Other published Feller-lab / Briggman-lineage DSGC reconstructions with diameters
     recorded. Pick one primary source and one fallback source; document the choice and the
     per-order distribution in `research/research_papers.md`.
2. **Implementation**:
   * Parse the CNG-curated SWC with a stdlib parser (can reuse
     `tasks/t0005_download_dsgc_morphology/code/validate_swc.py` approach).
   * Compute per-compartment Strahler order and path distance from the soma.
   * Apply the chosen taper rule to assign a realistic radius to every dendritic compartment.
     Preserve the 19 soma compartments' original (non-placeholder) radii.
   * Write the new SWC to `assets/dataset/dsgc-baseline-morphology-calibrated/files/`.
3. **Register** the calibrated morphology as a v2 dataset asset
   (`assets/dataset/dsgc-baseline-morphology-calibrated/`) with a `details.json`, a
   `description.md`, and the calibrated SWC file. The `details.json` must reference
   `dsgc-baseline-morphology` as the raw source and cite the chosen taper-source paper.
4. **Validation**:
   * Plot per-Strahler-order radius distributions (original placeholder vs calibrated) and
     save as PNG to `results/images/`.
   * Recompute total surface area and axial resistance per branch; report the change vs the
     placeholder baseline.
   * Confirm compartment count, branch points and connectivity are unchanged from the source
     SWC.

## Dependencies

* **t0005_download_dsgc_morphology** — source of `dsgc-baseline-morphology` raw SWC and the
  stdlib parser.

## Expected Outputs

* **1 dataset asset** (`assets/dataset/dsgc-baseline-morphology-calibrated/`) — calibrated
  SWC.
* Per-order diameter distribution plots in `results/images/` (original vs calibrated).
* Brief answer-style report embedded in `results/results_detailed.md` summarising the chosen
  taper rule, the rationale, and the change in surface area / axial resistance vs the
  placeholder.

## Questions the task answers

1. Which published taper source is most faithful for mouse ON-OFF DSGCs of the
   141009_Pair1DSGC lineage?
2. What is the Strahler-order-to-radius (or path-distance-to-radius) mapping used in the
   calibration?
3. How does total dendritic surface area change from the placeholder baseline to the
   calibrated morphology?
4. How does axial resistance along the preferred-to-null dendritic axis change, and what does
   that predict for spike-attenuation at the soma?

## Risks and Fallbacks

* **No published source gives a cell-matched per-order taper**: fall back to the Poleg-Polsky
  ModelDB distribution and clearly label the calibrated asset as "Poleg-Polsky-profile
  calibrated" rather than "literature-grounded".
* **The chosen taper makes distal tips implausibly thin (< 0.1 µm)**: clamp the radius floor
  at 0.15 µm and document the clamp.
* **Calibration collapses spatial detail (uniform assignment)**: treat as a bug, not a
  feature; re-derive the taper until per-order variability survives.

**Results summary:**

> **Results Summary: Calibrate Dendritic Diameters**
>
> **Summary**
>
> Replaced the uniform **0.125 µm** placeholder radius on every compartment of
> `dsgc-baseline-morphology` with a Poleg-Polsky & Diamond 2016 per-Strahler-order taper,
> registered
> as the new dataset asset `dsgc-baseline-morphology-calibrated`. Topology is preserved
> byte-for-byte
> (**6,736** compartments, **129** branch points, **131** leaves, **1,536.25 µm** dendritic
> length)
> while total dendritic surface area grows **7.99x** and total dendritic axial resistance
> drops to
> **~4.8%** of the placeholder baseline.
>
> **Metrics**
>
> * **Distinct radii (calibrated)**: 4 — soma **4.118 µm**, primary **3.694 µm** (Strahler
>   order
> 5), mid **1.653 µm** (orders 2-4), terminal **0.439 µm** (order 1)
> * **Max Strahler order**: 5 (max-child tie-break, 33 order-5 compartments, 3,915 terminals)
> * **Terminal clamps at 0.15 µm floor**: **0** (Poleg-Polsky terminal mean is 2.9x the floor)
> * **Surface area**: placeholder **1,213.43 µm²** -> calibrated **9,700.10 µm²** (**+7.99x**)
> * **Dendritic axial resistance**: placeholder **3.13e10 Ohm** -> calibrated **1.50e9 Ohm**
> (**4.79%**, a **20.9x** drop)

</details>

<details>
<summary>✅ 0008 — <strong>Port ModelDB 189347 and similar DSGC compartmental models
to NEURON</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0008_port_modeldb_189347` |
| **Status** | completed |
| **Effective date** | 2026-04-20 |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Expected assets** | 1 library, 1 answer |
| **Source suggestion** | `S-0002-03` |
| **Task types** | [`code-reproduction`](../../../meta/task_types/code-reproduction/), [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-20T10:08:09Z |
| **End time** | 2026-04-20T12:10:00Z |
| **Step progress** | 12/15 |
| **Task page** | [Port ModelDB 189347 and similar DSGC compartmental models to NEURON](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Task folder** | [`t0008_port_modeldb_189347/`](../../../tasks/t0008_port_modeldb_189347/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0008_port_modeldb_189347/results/results_detailed.md) |

# Port ModelDB 189347 and similar DSGC compartmental models to NEURON as library assets

## Motivation

Poleg-Polsky & Diamond 2016 (paper `10.1016_j.neuron.2016.02.013`, ModelDB 189347) is the
closest published match to this project's goal: a NEURON multi-compartmental mouse ON-OFF DSGC
model with **177 AMPA + 177 GABA** synapses and NMDA multiplicative gain. Reproducing it
creates the reference implementation that every later parameter-variation task (Na/K grid
S-0002-01, morphology sweep S-0002-04, E/I ratio scan S-0002-05, active-vs-passive dendrites
S-0002-02) will fork from. It is also the cleanest end-to-end test that the NEURON+NetPyNE
install from t0007 and the calibrated morphology from t0009 are fit for purpose.

Covers suggestions **S-0002-03** and **S-0003-02** (merged — the two suggestions describe the
same work from slightly different angles).

## Scope

### Phase A — Port the Poleg-Polsky 2016 baseline

1. Download ModelDB entry 189347 and register the resulting Python package under
   `assets/library/dsgc-polegpolsky-2016/` with a description, module paths, test paths, and a
   smoke-test that instantiates the model and runs a single angle.
2. Swap in the calibrated morphology produced by t0009 (`dsgc-baseline-morphology-calibrated`)
   in place of the ModelDB-bundled morphology. Document the swap and any geometric differences
   (compartment count, dendritic path length, branch points) vs the original ModelDB
   morphology.
3. Run the published stimulus: drifting bar / moving spot at 12 angles (30° spacing), synaptic
   configuration matching the paper, Poleg-Polsky NMDA parameters.
4. Compute the simulated tuning curve (firing rate vs angle, 20 trials per angle with fresh
   seeds) and score it with the t0012 scoring loss library against the envelope: DSI
   **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM **60-90°**.

### Phase B — Hunt for sibling DSGC compartmental models

5. Search ModelDB, SenseLab, OSF, and GitHub for additional DSGC compartmental models cited or
   adjacent in the literature (Schachter2010 derivatives, Briggman-lineage forks, 2017-2025
   updates of the Poleg-Polsky model, any post-2020 published code).
6. For each model found, record: source URL, NEURON compatibility, morphology it ships with,
   synaptic configuration, and whether it runs out-of-the-box in this environment.
7. Port any model that has public code and runs cleanly as a separate library asset under
   `assets/library/<model-slug>/`. If a model fails to run, record the failure in the Phase B
   answer asset and do not register a broken library.

## Dependencies

* **t0005_download_dsgc_morphology** — source of `dsgc-baseline-morphology`
* **t0007_install_neuron_netpyne** — NEURON+NetPyNE must work before any simulation runs
* **t0009_calibrate_dendritic_diameters** — needs calibrated morphology to avoid biasing the
  reproduction with placeholder 0.125 µm radii
* **t0012_tuning_curve_scoring_loss_library** — envelope verification must use the canonical
  scoring library, not an ad-hoc check

## Expected Outputs

* **1 library asset** (`assets/library/dsgc-polegpolsky-2016/`) — the ported ModelDB 189347.
* **1 answer asset** (`assets/answer/dsgc-modeldb-port-reproduction-report/`) covering:
  * Phase A: envelope verification table (DSI, peak, null, HWHM) vs targets
  * Phase B: a survey row-per-model listing each candidate found, its source, its NEURON
    compatibility, whether it was ported, and if not, why
* **0 or more additional library assets** for any sibling models successfully ported.
* **Simulated tuning-curve CSVs** under `data/tuning_curves/` (per model, per seed) for t0011
  to consume.

## Approach

* Write `code/port_modeldb_189347.py` that downloads the ModelDB zip, unpacks it into the
  library asset folder, compiles its MOD files with `nrnivmodl`, and runs the published demo
  to confirm the port is intact before any morphology swap.
* Write `code/run_tuning_curve.py` that takes a library name and a morphology (calibrated
  SWC), runs 12 angles × 20 seeded trials, writes `tuning_curve.csv` with `(angle_deg,
  trial_seed, firing_rate_hz)`.
* Write `code/score_envelope.py` that imports the t0012 scoring library and produces the
  verification table.
* For Phase B: write `code/hunt_sibling_models.py` that scrapes ModelDB's category listings
  (the author's own follow-up entries, neighbouring DSGC entries, 2017+ entries citing 189347)
  and writes a candidate-list CSV. Human review selects which candidates to attempt porting
  before Phase B code runs.

## Compute and Budget

Local only. 12 angles × 20 trials × ~5-10 s wall-clock per trial ≈ 20-40 minutes per model on
this workstation. Budget remains `$0.00`.

## Questions the task answers

1. Does the reproduced Poleg-Polsky 2016 model hit the envelope: DSI 0.7-0.85, peak 40-80 Hz,
   null < 10 Hz, HWHM 60-90°?
2. Does swapping the ModelDB morphology for the calibrated Feller morphology preserve envelope
   compliance, or does it shift the model outside the envelope?
3. Which sibling DSGC compartmental models exist in public repositories, and which run in this
   environment?
4. Are there published DSGC compartmental models whose tuning curves systematically disagree
   with the Poleg-Polsky envelope, and if so, by how much?

## Risks and Fallbacks

* **ModelDB 189347 has drifted or the Python wrapper is stale**: port the `hoc`/`mod` files
  directly and wrap in a minimal Python loader; record the drift in the answer asset.
* **Swapping to the calibrated morphology produces envelope failure**: treat that as a
  scientific finding, not a blocker — report it verbatim and surface a new suggestion for
  morphology- conditioned parameter retuning.
* **Phase B finds no portable sibling models**: document the gap as a new suggestion and do
  not invent models to port.

**Results summary:**

> **Results Summary: Port ModelDB 189347 DSGC and Hunt Sibling Models**
>
> **Summary**
>
> Ported ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC compartmental model) as
> a
> registered library asset, compiled its six MOD files cleanly on NEURON 8.2.7, and ran a
> canonical
> 12-angle x 20-trial (240 total) drifting-bar tuning-curve sweep using the t0012
> `tuning_curve_loss`
> scoring library. The port is **technically faithful** — all MOD files compile, the
> morphology-swap
> report confirms section-count and surface-area parity, and every trial completes end-to-end
> on the
> local Windows workstation — but it does **not** reproduce the project envelope (DSI
> **0.316** vs
> target 0.70-0.85; peak **18.1 Hz** vs 40-80 Hz). The gap is a protocol mismatch, not a port
> bug:
> Poleg-Polsky 2016 implements direction selectivity via a per-angle `gabaMOD` parameter swap,
> whereas
> this task applied a spatial-rotation proxy. Follow-up captured in `S-0008-02`. Phase B
> completed as
> a desk survey ranking Hanson 2019 as the highest-priority sibling port.
>
> **Metrics**
>
> * **DSI (direction-selectivity index)**: **0.316** (target 0.70-0.85) - **FAIL**
> * **Peak firing rate**: **18.1 Hz** (target 40-80 Hz) - **FAIL**
> * **Null firing rate**: **9.4 Hz** (target <10 Hz) - **PASS**

</details>

## 2026-04-19 (7)

## ✅ Completed

<details>
<summary>✅ 0014 — <strong>Brainstorm results session 3</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0014_brainstorm_results_3` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0006_brainstorm_results_2`](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-19T23:10:00Z |
| **End time** | 2026-04-19T23:45:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 3](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Task folder** | [`t0014_brainstorm_results_3/`](../../../tasks/t0014_brainstorm_results_3/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0014_brainstorm_results_3/results/results_detailed.md) |

# Brainstorm Session 3 — Per-Category Literature-Survey Wave

## Context

The project has completed its first two task waves:

* **Wave 1** (t0001-t0005): foundational brainstorm, DSGC-focused compartmental-model
  literature survey, simulator survey, canonical target tuning curve, baseline DSGC morphology
  download.
* **Wave 2** (t0007-t0013, planned by t0006): NEURON install (t0007 done), plus calibration,
  porting, visualisation, scoring, and provenance tasks (t0008-t0013 still in-flight or not
  started).

The paper corpus contains 20 DOIs from t0002 (DSGC compartmental models). Categories
`direction-selectivity`, `compartmental-modeling`, and `retinal-ganglion-cell` are already
well-covered by that survey. Five remaining categories are under-covered: `cable-theory`,
`dendritic-computation`, `patch-clamp`, `synaptic-integration`, `voltage-gated-channels`.

## Session Goal

Plan a per-category literature-survey wave (Wave 3) that broadens the paper corpus so the
project's research questions about Na/K conductance combinations, active-vs-passive dendrites,
and synaptic kinetics can be grounded in the wider neuroscience literature rather than only
DSGC-specific work.

## Decisions

1. **Drop the 3 saturated categories** (direction-selectivity, compartmental-modeling,
   retinal-ganglion-cell). The existing t0002 corpus + queued t0010 (hunt missed DSGC models)
   cover them adequately.

2. **Create 5 new literature-survey tasks** (t0015-t0019), one per remaining category, each
   targeting ~25 category-relevant papers with cross-category overlap accepted (option (b)
   from the brainstorm discussion). Total attempted: ~125 papers, expected unique ~80-100
   after cross-task dedup (addressed by a later dedup-checkpoint task).

3. **Exclude the 20-DOI t0002 corpus** from each new task's search to avoid wasting download
   budget on already-owned papers.

4. **Bump `project/budget.json` `total_budget` from $0 to $1** so the mechanical
   `has_external_costs: true` gate on the `literature-survey` task type does not block
   execution. Literal expected spend remains $0 (arXiv, PubMed Central, ModelDB, and
   open-access sources are free; summarisation is done in-session).

5. **Paywalled paper protocol**: each task lists paywalled DOIs in
   `intervention/paywalled_papers.md`; the researcher downloads PDFs manually from their
   institutional account into `assets/paper/<paper_id>/files/` and the task then upgrades
   `download_status` to `"success"` with a full summary in a follow-up pass.

## New Suggestions Produced

Five dataset-kind suggestions (S-0014-01 through S-0014-05), each `priority: high`, one per
new task. These are recorded in `results/suggestions.json` and become the `source_suggestion`
for their respective child task.

## Out of Scope

* No experiments this session — this is a planning-only brainstorm.
* No corrections — t0002 corpus is correct; we are extending, not correcting.
* No new asset types or task types — `literature-survey` already exists.

**Results summary:**

> **Brainstorm session 3 — Summary**
>
> **Summary**
>
> Planned a five-task literature-survey wave (t0015-t0019) to broaden the project's paper
> corpus
> beyond the DSGC-specific modelling focus of t0002. Authorised a $1 budget bump (to be
> applied
> directly on `main` as a follow-up commit, since task branches cannot modify
> `project/budget.json`)
> so `literature-survey` tasks clear the project budget gate without incurring real spend.
> Confirmed a
> paywalled-paper workflow where each survey emits an `intervention/paywalled_papers.md` the
> researcher resolves from their institutional account.
>
> **Decisions**
>
> * **Five surveys, one per under-saturated category**: cable-theory, dendritic-computation,
> patch-clamp, synaptic-integration, voltage-gated-channels. Dropped `direction-selectivity`,
> `compartmental-modeling`, and `retinal-ganglion-cell` because t0002 plus t0010 already
> saturate
> them.
> * **Target ~25 category-relevant papers per task** (not 20). Extra headroom compensates for
>   the
> deduplication constraint and for papers that ultimately fail quality filters.
> * **Exclude the 20 DOIs already in the t0002 corpus** from each survey. Duplicate hits must
>   be

</details>

<details>
<summary>✅ 0007 — <strong>Install and validate NEURON 8.2.7 + NetPyNE 1.1.1
toolchain</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0007_install_neuron_netpyne` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0003-01` |
| **Task types** | [`infrastructure-setup`](../../../meta/task_types/infrastructure-setup/) |
| **Start time** | 2026-04-19T18:20:22Z |
| **End time** | 2026-04-19T22:43:38Z |
| **Step progress** | 10/15 |
| **Task page** | [Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Task folder** | [`t0007_install_neuron_netpyne/`](../../../tasks/t0007_install_neuron_netpyne/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0007_install_neuron_netpyne/results/results_detailed.md) |

# Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain

## Motivation

The t0003 simulator survey selected **NEURON 8.2.7** (paired with **NetPyNE 1.1.1**) as the
project's primary compartmental simulator, but did not install it. Every downstream
compartmental- modelling task (ModelDB 189347 port, diameter calibration verification,
missed-models hunt, visualisation smoke-test against a running simulation, tuning-curve
scoring) needs a validated NEURON+NetPyNE environment. This task does the install, proves it
works end-to-end on a trivial cell, and records the exact installed versions and any installer
warnings so later tasks can reproduce the environment deterministically.

Covers suggestion **S-0003-01**.

## Scope

1. Install NEURON 8.2.7 and NetPyNE 1.1.1 into the project's `uv` virtualenv: `uv pip install
   neuron==8.2.7 netpyne==1.1.1`.
2. Compile the bundled Hodgkin-Huxley MOD files with `nrnivmodl`. Record the compilation
   command, wall-clock, and any warnings.
3. Run a 1-compartment sanity simulation:
   * Create a single-section soma (L = 20 µm, diam = 20 µm) with `hh` inserted.
   * Inject a 0.5 nA step current for 50 ms, record membrane voltage.
   * Confirm at least one spike (V crosses +20 mV).
4. Repeat the same sanity simulation via NetPyNE's `specs.NetParams` +
   `sim.createSimulateAnalyze` harness to prove NetPyNE wraps NEURON correctly.
5. Record the final installed versions (`neuron.__version__`, `netpyne.__version__`, the
   NEURON `hoc` "about" string), the `nrnivmodl` output, the sanity-simulation wall-clocks,
   and any installer warnings into a single answer asset named
   `neuron-netpyne-install-report`.

## Dependencies

None — this task does not need any prior task's output.

## Expected Outputs

* **1 answer asset** (`assets/answer/neuron-netpyne-install-report/`) with:
  * `details.json` (question, categories, answer methods, source URLs for install commands)
  * `short_answer.md` (3-5 sentences: versions + "works" / "does not work" verdict)
  * `full_answer.md` (install log, sanity-simulation code, NEURON + NetPyNE voltage traces
    embedded as PNGs in `files/images/`, tabulated wall-clocks, every installer warning
    verbatim)

## Approach

Write a `code/install_and_validate.py` script that (a) shells out to `uv pip install`, (b)
shells out to `nrnivmodl` in the NEURON-bundled MOD directory, (c) runs the two sanity
simulations capturing voltage traces to CSV, and (d) produces the two PNG plots. Wrap every
CLI call with `run_with_logs.py`. Keep the sanity-simulation code deliberately minimal so the
answer asset also serves as a "hello world" reference for downstream tasks.

## Questions the task answers

1. Does `uv pip install neuron==8.2.7 netpyne==1.1.1` succeed on this workstation?
2. Does `nrnivmodl` compile the bundled HH MOD files without errors?
3. Does a 1-compartment soma with `hh` fire at least one action potential under a 0.5 nA step?
4. Does NetPyNE's wrapper produce the same voltage trace as raw NEURON on the same cell?
5. What are the exact installed versions, and what warnings (if any) surfaced during install
   or compilation?

## Risks and Fallbacks

* If NEURON 8.2.7 wheels are unavailable for this Python version, fall back to the nearest
  supported patch release and record the substitution in the answer asset.
* If NetPyNE pins an older NEURON release, use the NetPyNE-required version and record the
  override.
* If `nrnivmodl` needs `gcc`/`clang` that is not on PATH, create an intervention file
  requesting the compiler toolchain instead of silently skipping MOD compilation.

**Results summary:**

> ---
> spec_version: "1"
> task_id: "t0007_install_neuron_netpyne"
> date_completed: "2026-04-19"
> ---
> **Results Summary: NEURON 8.2.7 + NetPyNE 1.1.1 install**
>
> **Summary**
>
> The NEURON 8.2.7 + NetPyNE 1.1.1 toolchain installs, compiles MOD files, and runs a
> single-compartment Hodgkin-Huxley sanity simulation end-to-end on the project's Windows 11
> workstation. Raw NEURON and NetPyNE sanity sims agree to machine precision at **v_max =
> 42.003 mV**,
> confirming the stack is ready for downstream modelling tasks (t0008, t0010, t0011).
>
> **Metrics**
>
> * Raw NEURON sanity sim: **v_max = 42.003 mV**, crossed +20 mV threshold, 3201 samples,
>   setup **6.7
> ms**, run **4.4 ms**.
> * NetPyNE sanity sim: **v_max = 42.003 mV**, crossed +20 mV threshold, 3201 samples, setup
>   **38.7
> ms**, run **4.8 ms**.

</details>

<details>
<summary>✅ 0006 — <strong>Brainstorm results session 2</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0006_brainstorm_results_2` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md), [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-19T09:30:00Z |
| **End time** | 2026-04-19T11:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 2](../../../overview/tasks/task_pages/t0006_brainstorm_results_2.md) |
| **Task folder** | [`t0006_brainstorm_results_2/`](../../../tasks/t0006_brainstorm_results_2/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0006_brainstorm_results_2/results/results_detailed.md) |

# Brainstorm Results Session 2

## Objective

Second brainstorming session for the neuron-channels project, held after the first wave of
tasks (t0002-t0005) completed. The goal is to translate the literature survey's quantitative
targets, the simulator recommendation, the canonical target tuning curve, and the baseline
morphology asset into a concrete tooling round that lets every downstream
compartmental-modelling experiment run without per-task re-implementation of shared machinery.

## Context

Going into this session:

* **t0002** produced a 20-paper corpus and an answer asset fixing quantitative targets: DSI
  **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM **60-90°**, **177
  AMPA + 177 GABA** synapses, g_Na **0.04-0.10 S/cm²**.
* **t0003** recommended **NEURON 8.2.7 + NetPyNE 1.1.1** as the primary simulator and **Arbor
  0.12.0** as backup; Brian2 and MOOSE were rejected.
* **t0004** generated the canonical `target-tuning-curve` dataset (cos²-half-rectified, DSI
  0.8824, HWHM 68.5°, 240-row CSV).
* **t0005** downloaded `dsgc-baseline-morphology` (NeuroMorpho 102976, Feller lab
  141009_Pair1DSGC; 6,736 compartments; 1,536.25 µm dendritic path). Two known caveats:
  placeholder uniform radius 0.125 µm, ambiguous source-paper attribution.
* 23 active uncovered suggestions, most concentrated on experiments that cannot run until the
  tooling exists.

No compartmental simulation has run yet.

## Session Outcome

Seven new tasks agreed with the researcher, all `status = not_started`:

* **t0007** — Install and validate NEURON 8.2.7 + NetPyNE 1.1.1. No dependencies.
* **t0008** — Port ModelDB 189347 and similar DSGC compartmental models to NEURON as library
  assets. Depends on t0007, t0005, t0009, t0012.
* **t0009** — Calibrate dendritic diameters on `dsgc-baseline-morphology`. Depends on t0005.
* **t0010** — Literature + code hunt for DSGC compartmental models missed by t0002 and t0008;
  port any found. Depends on t0008.
* **t0011** — Response-visualisation library (firing rate vs angle graphs). Depends on t0004
  and t0008.
* **t0012** — Tuning-curve scoring loss library. Depends on t0004.
* **t0013** — Resolve `dsgc-baseline-morphology` source-paper provenance and file a
  corrections asset. Depends on t0005.

t0007, t0009, t0012, and t0013 can run in parallel. t0008 gates t0010 and (partially) t0011.

## Corrections Filed

* **S-0004-03** → rejected (redundant with S-0002-09, now covered by t0012).
* **S-0005-04** → reprioritised HIGH → MEDIUM (NEURON loader absorbed into t0008;
  multi-simulator translator only needed once Arbor benchmarking starts).

## Researcher Preferences Captured

* Block t0008 on t0009 — use the calibrated morphology, not the placeholder-radius version.
* t0011 smoke-tests visualisation against both the canonical `target-tuning-curve` and
  whatever t0008 produces.
* Leave `project/budget.json` untouched at `$0.00 / no paid services`; everything runs
  locally.
* Defer the dendritic-diameter calibration source choice (Vaney/Sivyer/Taylor 2012 vs
  Poleg-Polsky 2016 vs other) to t0009's research stage rather than pinning it up front.
* Build a proper scoring library (S-0002-09 covered by t0012), not an ad-hoc inline check
  inside t0008.

**Results summary:**

> **Results Summary: Brainstorm Session 2**
>
> **Summary**
>
> Second brainstorming session for the neuron-channels project. Produced seven second-wave
> task
> folders (t0007-t0013) covering NEURON+NetPyNE installation, ModelDB 189347 port plus
> sibling-model
> port, dendritic-diameter calibration, model hunt, response visualisation, tuning-curve
> scoring, and
> morphology source-paper provenance. Filed two suggestion corrections.
>
> **Session Overview**
>
> * **Date**: 2026-04-19
> * **Context**: First task wave (t0002-t0005) completed. Quantitative targets established
>   (DSI
> 0.7-0.85, peak 40-80 Hz, null < 10 Hz, HWHM 60-90°); simulator choice converged on NEURON
> 8.2.7 +
> NetPyNE 1.1.1; canonical target-tuning-curve dataset generated; baseline morphology
> 141009_Pair1DSGC downloaded with two open issues (placeholder radii; ambiguous source
> paper).
> * **Prompt**: Researcher invoked `/human-brainstorm` and laid out a three-step high-level
>   goal:
> install NEURON+NetPyNE, port ModelDB 189347 and similar compartmental DSGC models, then hunt
> literature for missed models, then add response-visualisation and tuning-curve-scoring
> support
> libraries.

</details>

<details>
<summary>✅ 0005 — <strong>Download candidate DSGC morphology</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0005_download_dsgc_morphology` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Expected assets** | 1 dataset |
| **Source suggestion** | — |
| **Task types** | [`download-dataset`](../../../meta/task_types/download-dataset/) |
| **Start time** | 2026-04-19T08:50:24Z |
| **End time** | 2026-04-19T09:28:00Z |
| **Step progress** | 8/15 |
| **Task page** | [Download candidate DSGC morphology](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Task folder** | [`t0005_download_dsgc_morphology/`](../../../tasks/t0005_download_dsgc_morphology/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0005_download_dsgc_morphology/results/results_detailed.md) |

# Download candidate DSGC morphology

## Motivation

Every downstream simulation task needs a concrete reconstructed morphology to load. Rather
than generating a synthetic branching structure, we want a published DSGC (or DSGC-like RGC)
reconstruction used by prior modelling work. The literature survey (t0002) produces the
shortlist; this task commits to one file.

## Scope

Download one reconstructed DSGC morphology in SWC format (or HOC / NeuroML if SWC is not
available) from a public source such as NeuroMorpho.org, ModelDB, or a paper's supplementary
materials. The morphology should be one of those flagged as suitable in t0002's answer asset.

## Approach

1. Read t0002's answer asset to pick the recommended morphology.
2. Download the file and verify it loads as a valid SWC / HOC structure.
3. Record its provenance (source URL, paper DOI, reconstruction protocol) in the dataset asset
   metadata.

## Expected Outputs

* One dataset asset under `assets/dataset/dsgc_baseline_morphology/` containing the morphology
  file(s) and metadata.

## Compute and Budget

No external cost.

## Dependencies

`t0002_literature_survey_dsgc_compartmental_models` — the literature survey produces the
morphology shortlist and rationale.

## Verification Criteria

* Dataset asset passes `verify_dataset_asset.py`.
* The asset's `details.json` links back to the source paper or NeuroMorpho record.
* The downloaded file loads without errors in at least one candidate simulator library.

**Results summary:**

> **Results Summary: Download candidate DSGC morphology**
>
> **Summary**
>
> Downloaded the Feller-lab ON-OFF mouse DSGC reconstruction `141009_Pair1DSGC` (NeuroMorpho
> neuron
> 102976\) from Morrie & Feller-associated archives as a CNG-curated SWC, validated the
> compartment
> tree with a stdlib Python parser, and registered it as the project's baseline DSGC dataset
> asset
> `dsgc-baseline-morphology` (v2 spec-compliant). The morphology is now the single
> reconstructed cell
> that every downstream compartmental-modelling task in this project will load.
>
> **Metrics**
>
> * **Compartments**: **6,736** (19 soma, 6,717 dendrite, 0 axon)
> * **Branch points (≥2 children)**: **129**
> * **Leaf tips**: **131**
> * **Total dendritic path length**: **1,536.25 µm**
> * **SWC file size**: **232,470 bytes** (CNG-curated)
> * **Download cost**: **$0** (CC-BY-4.0 public data)
>
> **Verification**

</details>

<details>
<summary>✅ 0004 — <strong>Generate canonical target angle-to-AP-rate tuning
curve</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0004_generate_target_tuning_curve` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | — |
| **Task types** | [`feature-engineering`](../../../meta/task_types/feature-engineering/) |
| **Start time** | 2026-04-19T08:12:46Z |
| **End time** | 2026-04-19T08:42:30Z |
| **Step progress** | 8/15 |
| **Task page** | [Generate canonical target angle-to-AP-rate tuning curve](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Task folder** | [`t0004_generate_target_tuning_curve/`](../../../tasks/t0004_generate_target_tuning_curve/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0004_generate_target_tuning_curve/results/results_detailed.md) |

# Generate canonical target angle-to-AP-rate tuning curve

## Motivation

The key project metric `tuning_curve_rmse` compares a simulated angle-to-AP-rate tuning curve
against a target. The researcher chose to **simulate** a canonical target curve rather than
digitise one from a paper. This task generates that canonical target and registers it as a
dataset asset so all later optimisation tasks share one fixed reference.

## Scope

Produce a single dataset asset containing:

* A cosine-like target tuning curve sampled at 12 or 24 angles around 360°.
* Explicit generator parameters: preferred direction (deg), baseline rate (Hz), peak rate
  (Hz), tuning half-width (deg or von Mises κ), and random seed.
* Per-angle mean rates plus a small number of synthetic noisy trial replicates so the
  `tuning_curve_reliability` metric has a well-defined ground-truth value.

Suggested functional form:

```
r(θ) = r_base + (r_peak - r_base) * ((1 + cos(θ - θ_pref)) / 2) ** n
```

with `n` controlling sharpness. Any equivalent von Mises formulation is fine. The exact values
of `r_base`, `r_peak`, `θ_pref`, and `n` should be chosen to give a biologically plausible DSI
(roughly 0.6-0.9) and reported in the dataset's `details.json`.

## Approach

1. Write a small Python script under `code/` that generates the curve, saves it to `data/` as
   CSV or JSON, and writes the dataset asset folder under `assets/dataset/`.
2. Include both a mean-rate table and a per-trial table (e.g., 20 synthetic trials) so
   `tuning_curve_reliability` has a real reference value.
3. Plot the curve and save to `results/images/target_tuning_curve.png`.

## Expected Outputs

* One dataset asset under `assets/dataset/target_tuning_curve/` containing the CSV/JSON
  tables, metadata, and description.
* A plot of the target curve in `results/images/`.

## Compute and Budget

Trivial. Runs locally in seconds; no external cost.

## Dependencies

None. Runs in parallel with t0002 and t0003. This task is the reference any later optimisation
task will compare against.

## Verification Criteria

* Dataset asset passes `verify_dataset_asset.py`.
* `details.json` records the generator parameters and random seed explicitly.
* The generated CSV/JSON has one row per angle and the noisy-trial table has at least 10
  trials per angle.

**Results summary:**

> **Results Summary: Generate Canonical Target Tuning Curve**
>
> **Summary**
>
> Synthesised the canonical direction tuning curve `target-tuning-curve` from a closed-form
> half-wave-rectified cosine raised to power `n = 2` with `θ_pref = 90°`, `r_base = 2 Hz`,
> `r_peak = 32 Hz`, and 20 Gaussian-noise trials per angle (`σ = 3 Hz`, seed `42`). The asset
> is
> registered under `assets/dataset/target-tuning-curve/` with explicit generator parameters
> and a
> diagnostic plot.
>
> **Metrics**
>
> * **Direction Selectivity Index (DSI)**: **0.8824** — inside the required [0.6, 0.9] band
> * **Tuning curve HWHM**: **68.5°** — computed from the closed-form curve
> * **Sampled directions**: **12** angles at 30° spacing (0° to 330°)
> * **Trials per direction**: **20** (240 rows total in `curve_trials.csv`)
> * **Mean absolute bias (sample vs closed form)**: **0.419 Hz** (max 1.063 Hz)
>
> **Verification**
>

</details>

<details>
<summary>✅ 0003 — <strong>Simulator library survey for DSGC compartmental
modelling</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0003_simulator_library_survey` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`internet-research`](../../../meta/task_types/internet-research/) |
| **Start time** | 2026-04-19T07:20:04Z |
| **End time** | 2026-04-19T08:05:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Simulator library survey for DSGC compartmental modelling](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Task folder** | [`t0003_simulator_library_survey/`](../../../tasks/t0003_simulator_library_survey/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0003_simulator_library_survey/results/results_detailed.md) |

# Simulator library survey for DSGC compartmental modelling

## Motivation

`project/description.md` mentions NEURON as the canonical simulator but the researcher wants
to evaluate several libraries before committing. A bad simulator choice locks the project into
poor cable-model fidelity, slow parameter sweeps, or brittle tooling for months. A short
survey up front prevents this.

## Scope

Evaluate the following candidate libraries:

* NEURON (plus NEURON+Python bindings)
* NetPyNE (higher-level NEURON wrapper)
* Brian2 with cable-model extensions
* MOOSE
* Arbor

For each library, collect:

1. **Cable-model fidelity** — does it solve the full compartmental cable equation, support
   voltage-gated conductances in arbitrary compartments, and handle reconstructed morphologies
   (SWC, HOC, NeuroML)?
2. **Python ergonomics** — pure Python vs wrapped C++/MOD files, packaging on `uv`, quality of
   current documentation and examples.
3. **Speed and parallelism** — single-cell simulation speed and support for running large
   parameter sweeps.
4. **DSGC examples available** — whether any published DSGC or broader RGC compartmental model
   has been released in that library.
5. **Long-term maintenance** — last release, community activity, active maintainers.

## Approach

1. Run `/research-internet` to gather documentation, benchmarks, and user reports for each
   library.
2. Build a comparison table covering the five axes above.
3. Produce a single answer asset that recommends a **primary** simulator plus one **backup**,
   with explicit rationale.

## Expected Outputs

* One answer asset under `assets/answer/` summarising the library comparison and stating the
  primary plus backup recommendation.

## Compute and Budget

No external cost. Local LLM CLI and internet search only.

## Dependencies

None. Runs in parallel with t0002 and t0004.

## Verification Criteria

* The answer asset passes `verify_answer_asset.py`.
* The `## Answer` section states the primary and backup simulator in one or two sentences.
* The full answer includes the five-axis comparison table for every candidate library.

**Results summary:**

> **Results Summary: Simulator Library Survey for DSGC Compartmental Modelling**
>
> **Summary**
>
> Produced a single answer asset recommending **NEURON 8.2.7** (paired with **NetPyNE 1.1.1**
> for
> parameter sweeps) as the project's primary compartmental simulator and **Arbor 0.12.0** as
> backup,
> after surveying five candidate libraries (NEURON, NetPyNE, Brian2, MOOSE, Arbor) on five
> axes
> (cable-model fidelity, Python ergonomics, speed and parallelism, DSGC/RGC example
> availability,
> long-term maintenance). Brian2 and MOOSE were rejected with grounded evidence. The full
> answer
> embeds a 5-row × 5-column comparison table backed by 20 indexed internet sources.
>
> **Metrics**
>
> * **Libraries evaluated**: 5 (NEURON, NetPyNE, Brian2, MOOSE, Arbor)
> * **Evaluation axes**: 5 (cable-model fidelity, Python ergonomics, speed and parallelism,
>   DSGC/RGC
> examples, long-term maintenance)
> * **Sources cited**: 20 URLs, including 4 newly discovered papers
> * **Answer assets produced**: 1 (`dsgc-compartmental-simulator-choice`)
> * **Task requirements satisfied**: 17 of 17 (REQ-1 through REQ-17)
> * **External cost incurred**: $0.00 (no paid APIs, no remote compute)

</details>

<details>
<summary>✅ 0002 — <strong>Literature survey: compartmental models of DS retinal
ganglion cells</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0002_literature_survey_dsgc_compartmental_models` |
| **Status** | completed |
| **Effective date** | 2026-04-19 |
| **Dependencies** | — |
| **Expected assets** | 20 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-18T22:28:59Z |
| **End time** | 2026-04-19T01:35:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Literature survey: compartmental models of DS retinal ganglion cells](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Task folder** | [`t0002_literature_survey_dsgc_compartmental_models/`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/results/results_detailed.md) |

# Literature survey: compartmental models of DS retinal ganglion cells

## Motivation

This is the project's first research task. Before building any simulation we need a shared
knowledge base of what prior compartmental modelling work has done on direction-selective
retinal ganglion cells (DSGCs) and what each of the project's five research questions (RQs)
looks like in the literature. The survey feeds every downstream task: the target tuning curve
generator (t0004) needs published tuning-curve shapes, the morphology download (t0005) needs a
shortlist of reconstructed DSGCs, and the later Na/K optimisation and active-vs-passive
dendrite experiments need candidate channel models and parameter ranges.

## Scope

Cover all five project research questions at survey level:

1. **RQ1 Na/K combinations** — how published DSGC and related RGC models parameterise somatic
   sodium and potassium conductances, and what combinations reproduce directional AP firing.
2. **RQ2 morphology sensitivity** — how branching pattern, dendritic diameter, and compartment
   length have been shown to affect DS tuning.
3. **RQ3 AMPA/GABA balance** — ratio and spatial distribution of excitatory and inhibitory
   inputs, and their measured effect on DS sharpness.
4. **RQ4 active vs passive dendrites** — evidence for dendritic voltage-gated conductances in
   DSGCs, and modelling studies that compare active with passive dendrites.
5. **RQ5 angle-to-AP-frequency tuning curves** — reported tuning-curve shapes, peak rates,
   half-widths, and null-direction suppression levels that can serve as optimisation targets.

Minimum breadth:

* Include the six references already listed in `project/description.md` (Barlow & Levick 1965,
  Hines & Carnevale 1997, Vaney/Sivyer/Taylor 2012, Poleg-Polsky & Diamond 2016,
  Oesch/Euler/Taylor 2005, Branco/Clark/Häusser 2010).
* Add at least 14 more papers found by internet search, spread across the five research
  questions.
* Prefer papers with a clearly described compartmental model, published morphology, or
  quantitative angle-to-rate measurements.

## Approach

1. Run `/research-papers` using the six seed references to build initial paper assets.
2. Run `/research-internet` to find additional compartmental DSGC modelling papers and any
   patch-clamp studies that report tuning curves.
3. Download each selected paper via `/download-paper` so every cited paper becomes a paper
   asset with a summary.
4. Produce one answer asset that synthesises, across all five RQs, what the existing
   literature says about how to structure the DSGC modelling problem and what numbers to aim
   for.

## Expected Outputs

* ~20 paper assets under `assets/paper/` (each with `details.json`, `summary.md`, and the
  paper file under `files/`).
* One answer asset under `assets/answer/` summarising how existing compartmental DSGC models
  structure the five research questions and what numerical targets they provide.

## Compute and Budget

No external cost. Local LLM CLI only; no paid APIs or remote machines.

## Dependencies

None. This is the first research task.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and explicitly addresses each of the five
  research questions.
* `compare_literature.md` is not required for a pure literature survey.

**Results summary:**

> **Results Summary: Literature Survey of Compartmental Models of DS Retinal Ganglion Cells**
>
> **Summary**
>
> Produced a 20-paper survey of compartmental models of direction-selective retinal ganglion
> cells
> (DSGCs) covering all five project research questions, plus one synthesis answer asset that
> integrates the findings with per-RQ quantitative targets. The corpus includes all six seed
> references from `project/description.md` and 14 additional peer-reviewed papers spread
> across the
> five RQs, and it establishes concrete numerical targets (DSI **0.7-0.85**, preferred peak
> **40-80
> Hz**, null residual **< 10 Hz**, half-width **60-90 deg**, **177 AMPA + 177 GABA** synapses,
> g_Na
> **0.04-0.10 S/cm^2**) that downstream compartmental-modelling tasks must reproduce.
>
> **Metrics**
>
> * **Paper assets produced**: **20** (6 seeds + 14 additional, matches
>   `expected_assets.paper=20`)
> * **Answer assets produced**: **1** (matches `expected_assets.answer=1`)
> * **Papers with downloaded full text**: **17** (PDF/XML/markdown)
> * **Papers with metadata-only assets**: **3** (Chen2009, Sivyer2010, Sethuramanujam2016, all
> paywalled, `download_status: "failed"` per spec v3)
> * **RQ coverage by non-seed papers**: RQ1 **2**, RQ2 **3**, RQ3 **7**, RQ4 **3**, RQ5 **4**
>   — every

</details>

## 2026-04-18 (1)

## ✅ Completed

<details>
<summary>✅ 0001 — <strong>Brainstorm results session 1</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0001_brainstorm_results_1` |
| **Status** | completed |
| **Effective date** | 2026-04-18 |
| **Dependencies** | — |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-18T00:00:00Z |
| **End time** | 2026-04-18T00:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm results session 1](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md) |
| **Task folder** | [`t0001_brainstorm_results_1/`](../../../tasks/t0001_brainstorm_results_1/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0001_brainstorm_results_1/results/results_detailed.md) |

# Brainstorm Results Session 1

## Objective

Run the first brainstorming session for the neuron-channels project, held immediately after
`/setup-project` completed. The goal is to translate `project/description.md` into a concrete
first wave of tasks that the researcher can execute autonomously.

## Context

The project is brand-new. After setup, the repository contains:

* `project/description.md` with five research questions about the electrophysiological basis
  of retinal direction selectivity, and success criteria centred on a modifiable compartmental
  model and a good fit to a target angle-to-AP-frequency tuning curve.
* `project/budget.json` with zero budget and no paid services.
* Eight project categories and four registered metrics (`tuning_curve_rmse` as the key
  metric).
* No existing tasks, suggestions, answers, or results.

## Session Outcome

The session produced four first-wave task folders, all with `status = not_started`:

* `t0002_literature_survey_dsgc_compartmental_models` — one broad literature survey covering
  all five research questions.
* `t0003_simulator_library_survey` — compare NEURON, NetPyNE, Brian2, MOOSE, Arbor, and pick a
  primary + backup simulator.
* `t0004_generate_target_tuning_curve` — analytically generate a canonical cosine-like target
  angle-to-AP-rate curve as the optimisation reference.
* `t0005_download_dsgc_morphology` — download a reconstructed DSGC morphology (depends on
  t0002).

T0002, t0003, and t0004 are independent and can run in parallel. T0005 waits on t0002's
morphology shortlist.

## Researcher Preferences Captured

* Target tuning curve will be simulated with a canonical cosine-like shape, not digitised from
  any published figure.
* The project will try several simulator libraries, not commit to NEURON alone up front.
* One big literature survey rather than several narrow ones.
* Autonomous execution; the researcher does not need to gate each task plan.

**Results summary:**

> **Results Summary: Brainstorm Session 1**
>
> **Summary**
>
> First brainstorming session for the neuron-channels project. Produced four first-wave task
> folders
> (t0002-t0005) covering literature survey, simulator-library comparison, canonical target
> tuning
> curve generation, and DSGC morphology download. No suggestions were rejected, reprioritized,
> or
> created.
>
> **Session Overview**
>
> * **Date**: 2026-04-18
> * **Context**: Run immediately after `/setup-project` completed. Project state was empty: no
>   tasks,
> no suggestions, no answers, no costs, zero budget with no paid services.
> * **Prompt**: Phase 7 of `/setup-project` automatically chains `/human-brainstorm` to plan
>   the first
> tasks.
>
> **Decisions**
>
> 1. **Create t0002: literature survey of DSGC compartmental models** — one broad survey
>    covering

</details>

## unknown (1)

## ⏳ In Progress

<details>
<summary>⏳ 0097 — <strong>Literature survey: multi-objective optimisation of
single-neuron models</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0097_multi_obj_optim` |
| **Status** | in_progress |
| **Effective date** | — |
| **Dependencies** | — |
| **Expected assets** | 10 paper, 1 answer |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`internet-research`](../../../meta/task_types/internet-research/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [Literature survey: multi-objective optimisation of single-neuron models](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Task folder** | [`t0097_multi_obj_optim/`](../../../tasks/t0097_multi_obj_optim/) |

# Literature Survey: Multi-Objective Optimisation of Single-Neuron Compartmental Models

> **Note**: This task supersedes `t0096_literature_survey_multi_objective_neuron_optimisation`,
> which was created with a slug too long for Windows worktree paths to handle (the absolute path
> exceeded Windows' 260-char limit when combined with deep existing task paths). The content here is
> identical; only the task ID and slug are shorter.

## Motivation

The morphology + channel optimisation pipeline is now production-ready: t0091
(`morphology_extended_nsga2_v1`) is currently running the first joint 68-d NSGA-II (54-d
electrophys \+ 14-d morphology) on the t0092-patched procedural generator validated at scale
by t0093. Every multi-objective optimisation task this project has run so far (t0076, t0078,
t0080, t0081, t0083, t0086, t0091) has used the same two objectives: direction selectivity
index (DSI) and firing rate. That objective pair was the right choice for the project's
first-question ("which channels maximise DS?") phase, but it leaves the broader
multi-objective landscape unexplored.

The researcher's strategic directive (brainstorm session 20, 2026-05-08) is to broaden the
optimisation objective space:

> Now that we have working optimisation for both morphology and channel composition we can optimise
> for different things. Currently we optimise for DSI and firing rate. However I would like to
> compare results for all sorts of stuff. For example, I would like to optimise for DSI and
> information transfer rate; DSI and energy spent, DSI and minimisation of citoplasm volume etc.
> Perform an extensive literature search and find papers that use different forms of optimisation.
> It does not need to be DSGC but can be any neurons.

This task is the literature-research foundation for that broadening. It catalogues every
objective function used in the published multi-objective single-neuron optimisation
literature, delivers formulas + computational recipes for each, and produces a ranked list of
future MOBO tasks to commission once budget permits. The deliverable is intentionally
actionable: each catalogued objective must be implementable on top of the existing Bed B
NSGA-II loop without infrastructure rewrites.

The task is also the right test of biological plausibility as an optimisation criterion. The
researcher's recurring concern across this project has been that pure DSI maximisation admits
non-physical solutions; jointly optimising DSI vs energy, vs cytoplasm volume, or vs
robustness forces the optimiser into bio-realistic regions of the parameter space. The survey
should explicitly document, per objective, whether published work treats it as a biological
constraint or only as a performance proxy.

## Scope

### In Scope

* **Multi-objective methodology papers** covering single-neuron compartmental models:
  Druckmann et al. 2007 ("A novel multiple objective optimization framework for constraining
  conductance-based neuron models by experimental data"), Druckmann et al. 2011 (eFEL
  precursor), Achard & De Schutter 2006 (first MOEA Purkinje fits), Van Geit et al.
  (NeuroFitter / BluePyOpt), Rumbell et al. (cortical L5 PC MOBO), Hay et al. 2011 (BBP
  cortical L5 multi-objective).
* **Information-theoretic objective functions**: mutual information between stimulus and spike
  train (Bialek, De Ruyter van Steveninck, Strong et al.), Fisher information / discrimination
  capacity (Brunel, Nadal), channel capacity, stimulus-reconstruction MSE, spike-train metrics
  (Victor & Purpura, van Rossum).
* **Metabolic / energy objective functions**: ATP per spike, total ionic flux, Na+/K+ pump
  cost (Attwell & Laughlin 2001 "An energy budget for signaling in the grey matter of the
  brain"), bits-per-ATP energy efficiency (Niven & Laughlin 2008, Sengupta et al. 2010 "Action
  potential energy efficiency varies among neuron types in vertebrates and invertebrates").
* **Structural / wiring objective functions**: total dendritic length, total membrane area,
  cytoplasm / dendritic volume, wiring economy (Chklovskii et al., Cuntz, Forstner, Borst &
  Hausser 2010 "One rule to grow them all").
* **Robustness / degeneracy objective functions**: parameter-perturbation sensitivity, noise
  tolerance (Marder & Goaillard 2006 "Variability, compensation and homeostasis in neuron and
  network function"; Prinz, Bucher & Marder 2004 "Similar network activity from disparate
  circuit parameters").
* **Temporal / coding objective functions**: latency, jitter, spike-timing precision,
  bandwidth, dynamic range.
* **Methods / codebases**: BluePyOpt (Van Geit), NeuroFitter, NSGA-II + NSGA-III in pymoo,
  MOEA literature (Deb et al.), Pareto-front analysis methods (hypervolume, IGD, R2
  indicator).

### Out of Scope

* Network-level optimisation (multi-neuron). Stay on single-neuron compartmental models.
* Reinforcement-learning / deep-learning policy optimisation. Stay on classical MOBO / MOEA.
* Phenomenological integrate-and-fire models without compartmental structure (mention briefly
  if they yield reusable objectives, but do not deep-dive).

## Must-Find Objective Categories

The survey must deliver formula + units + NEURON-side computational recipe for at least one
representative objective in each of these four categories:

1. **Information transfer rate / mutual information** — between stimulus angle and spike-train
   output for our DSGC case. Concrete recipe must specify how to estimate MI from a
   t0091-style 8-direction trial output (e.g., binned spike counts per direction, direct
   method, or extrapolation method).

2. **Metabolic energy / ATP per spike** — computable from HH ionic currents in NEURON.
   Concrete recipe must specify which currents to integrate (Na+ influx, K+ efflux, leak) and
   the conversion factor from charge to ATP molecules (3 Na+ exchanged per ATP via Na+/K+
   ATPase).

3. **Cytoplasm volume / wiring cost** — computable directly from morphology. Concrete recipe:
   sum over compartments of pi * r^2 * L; or total surface area as an alternative; or wiring
   cost = sum of section lengths weighted by diameter.

4. **Robustness / degeneracy** — parameter-perturbation sensitivity of DSI; multi-conductance
   solution-space volume. Concrete recipe must specify a Marder-style protocol: e.g., +/- 10
   percent random perturbation of all channel densities and report DSI standard deviation as
   the objective.

If the literature search uncovers more well-defined objective categories not in this list, add
them to the catalogue and rank them by biological plausibility and computational feasibility.

## Approach

### Stage 1: Research Papers

Survey methodology and biological objective-function origin papers. Download canonical
citations for each objective category. Read full text where available; abstract +
supplementary info otherwise. Produce `research/research_papers.md` with:

* Per-objective subsection grouping the 2-3 canonical papers
* Per-paper extracted formula, units, computational recipe
* Notes on biological plausibility and how the objective would interact with DSI in a
  multi-objective setting

### Stage 2: Research Internet

Survey codebases, tutorials, review articles, and online resources for multi-objective
single-neuron optimisation. Targets: BluePyOpt (Van Geit, github.com/BlueBrain/BluePyOpt),
NeuroFitter, eFEL, pymoo NSGA-II + NSGA-III tutorials, Pareto-front diagnostic libraries
(pyDOE, paretoset). Document API surfaces and example usage that the project could adopt
without rewrites. Produce `research/research_internet.md`.

### Stage 3: Answer Asset

Synthesise findings into a single answer asset
`objective-functions-for-single-neuron-multi-objective-optimisation` (under `assets/answer/`).
Each catalogued objective gets a uniform record:

| Field | Content |
| --- | --- |
| Name | e.g. `mutual_information_stimulus_spike_train` |
| Mathematical formula | LaTeX |
| Units | e.g. bits per second, ATP per spike, um^3 |
| NEURON-side quantities required | Vm trace, ionic currents, spike times, morphology, etc. |
| Recipe | Step-by-step computation from a t0091-style 8-direction trial output |
| Biological plausibility | Notes on whether the objective is a hard biological constraint or a soft proxy |
| Direction-of-optimisation | Maximise / minimise / target value |
| Papers using it | At least 2 citations |

### Stage 4: Suggestions

Emit a ranked list of future MOBO tasks in `results/suggestions.json`. Each suggestion must
include:

* Title (e.g. "Bed B NSGA-II maximising DSI and ITR")
* Kind, priority
* Categories, source_paper if applicable
* Biological plausibility notes
* Budget feasibility estimate (Vast.ai EPYC + GPU hours)
* Cross-references to the catalogued objective entries

Suggestions must be ranked by combined biological-plausibility and budget-feasibility scores.
Aim for 3-6 ranked suggestions; do not pad.

## Cost Estimation

* **Total**: $0
* **Compute**: none. Local-only.
* **Paid services**: none.
* **Risk-of-going-over**: zero. The task is paper download + reading + writing.

## Step by Step

1. `init-folders`, `check-deps` (no deps to check).
2. Stage 1: research papers — download 10+ canonical papers; read; populate
   `research/research_papers.md`; create paper assets.
3. Stage 2: research internet — survey codebases, tutorials, review articles; populate
   `research/research_internet.md`.
4. Stage 3: answer asset — write the consolidated objective-function catalogue.
5. Stage 4: suggestions — write `results/suggestions.json` with the ranked future-MOBO list.
6. Reporting — write `results/results_summary.md` and `results/results_detailed.md`; run
   verificators; PR; merge.

## Remote Machines

None.

## Assets Needed

None. The task downloads its own paper assets.

## Expected Assets

* `paper`: at least 10 (covering methodology + four must-find categories)
* `answer`: 1 (the consolidated objective-function catalogue)

## Time Estimation

Approximately 2-4 hours wall-clock by an autonomous research agent. Roughly: 60-90 min paper
download + reading; 30-60 min internet survey + codebase review; 30-60 min answer asset
writing; 15-30 min suggestions + reporting + verification.

## Risks & Fallbacks

* **Paywalled paper not accessible** via Sci-Hub or institutional proxy: mark in
  `intervention/` and proceed with abstract + citation analysis. Do not block the task.
* **Cytoplasm volume has no direct precedent** in single-neuron optimisation literature: use
  the wiring-cost / total-length proxy and flag it as a novel objective contribution. The
  computational recipe is already trivial (sum over compartments of pi * r^2 * L) so the
  objective stays usable even without a published precedent.
* **Answer asset becomes too long** (>5000 words): split per category but keep one
  consolidated `short_answer.md` as the entry point. Each category subsection in
  `full_answer.md` may be a separate H2 section.
* **Literature search dilutes** because too many off-target papers come up: enforce the
  Out-of-Scope filter; prefer 2-3 canonical citations per category over comprehensive
  coverage.

## Verification Criteria

* All four must-find objective categories covered with formulas and computational recipes.
* At least 5 multi-objective compartmental-model methodology papers reviewed.
* At least 10 paper assets created and passing the paper asset verificator.
* Answer asset passes `meta/asset_types/answer/specification.md`.
* At least 3 ranked, budget-realistic future MOBO suggestions emitted in
  `results/suggestions.json`.
* All standard task verificators pass: `verify_task_file`, `verify_logs`,
  `verify_research_papers`, `verify_research_internet`, `verify_assets`, `verify_suggestions`,
  `verify_task_results`, `verify_pr_premerge`.

## Cross-References

* **t0096_literature_survey_multi_objective_neuron_optimisation** — superseded predecessor
  (cancelled in this PR due to Windows worktree path-length limit).
* **t0091_morphology_extended_nsga2_v1** — current MOBO frontier (DSI + firing rate);
  catalogue's recipes must compose with t0091's trial-output format.
* **t0095_brainstorm_results_20** — commissioned t0096 (this task's predecessor).
* **t0002_literature_survey_dsgc_compartmental_models** — prior literature survey for
  stylistic consistency.
* **t0015 / t0016 / t0017 / t0018 / t0019 / t0027** — prior literature surveys for stylistic
  consistency and for any cross-cited references.

</details>
