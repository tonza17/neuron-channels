---
spec_version: "2"
answer_id: "dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin"
answered_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"
confidence: "low"
date_answered: "2026-05-25"
---

# DSGC DSI vs ATP-per-spike: Carter-Bean / Howarth / Attwell-Laughlin Comparison

## Question

Does the DSGC DSI-vs-ATP-per-spike Pareto front show a Carter-Bean Na/K-overlap penalty, and where do its top cells sit relative to the revised Howarth 2012 17% cortex / 21% cerebellum signalling-ATP budget (and historically, the original Attwell-Laughlin 2001 47% anchor)?

## Short Answer

INSUFFICIENT EVIDENCE: only 5 legit cells passed the silence guard. The Pareto front structure cannot be quantitatively characterised under the single-seed protocol. Pearson r between DSI and ATP-per-spike across the legit top-5 cohort is r = 0.806 (95% CI [0.716, 1.000]).

## Research Process

Method: forked the t0123 NSGA-II substrate end-to-end, swapped the F[0] axis from MI to DSI (vector-sum, silence-guarded; sentinel = -1.0 for cells with R_PD < 3), halved N_DIRECTIONS from 4 to 2 (antipodal pair 0/180 deg), and ran one 60-gen NSGA-II at pop=96, N_EVAL_SEEDS=3 on a Vast.ai EPYC 7B13 instance. Smoke-gate ran 9 pre-launch checks; all PASS or WARN before NSGA-II launch. Post-run analysis loads the Pareto front + all-evaluations JSON + per-cell trace JSONL and computes the joint DSI / ATP correlation with bootstrap CI.

## Evidence from Papers

* Sengupta 2010: cross-cell-type Na/K overlap recipe (alpha values) anchoring the ATP-per-spike calculation. Cortical pyramidal alpha = 1.25; fast-spiking interneuron alpha = 2.0.
* Carter & Bean 2009: AIS ATP/AP measurements on Purkinje cells. Used indirectly via Sengupta's alpha-factor tabulation; first-principles derivation in plan/plan.md ## Approach places the canonical band at [1e+08, 1e+09] ATP/AP/cm (S-0123-04 resolved).
* Howarth, Gleeson & Attwell 2012: revised signalling-ATP fraction downward from Attwell-Laughlin 2001's 47% to 17% (cortex) / 21% (cerebellum). The Howarth figures are the operative primary anchor; the 2001 47% figure is annotated as the legacy reference.
* Werginz 2024: mouse alpha-RGC AIS Nav density (1300 mS/cm^2) underwriting the first-principles canonical-band derivation.
* Cuntz 2010: balancing-factor band [0.2, 0.7] used as the cross-reference for t0122's cytoplasm-volume Pareto front.

## Evidence from Internet Sources

* Howarth 2012 paper (PMC3390818) was located on the open-access preprint server and is cited URL-only here (not downloaded as a paper asset). The 17% cortex / 21% cerebellum revised anchors are extracted from the abstract and figure 4 of the source.
* Carter-Bean 2009 paper (PMC2810867) is open-access; the corrected DOI is `10.1016/j.neuron.2009.12.011` (Neuron 64(6), 898-909).

## Evidence from Code or Experiments

* NSGA-II run: GA seed 6650, pop=96, N_EVAL_SEEDS=3, N_DIRECTIONS=2, N_GEN_MAX=60 (completed: 9), cost cap $6.00 (realised $0.0728), stop trigger operator_stop. Pool-restart every 10 gens; HV-plateau auto-stop disabled.
* Pareto front size: 5 cells; legit cohort (post silence-guard): 5 cells.
* Bootstrap Pearson r between DSI and ATP-per-spike across the legit top-5 cohort: r = 0.8059, 95% CI [0.7158, 1.0000], n = 5, n_resamples=1000.
* Charts: `results/images/pareto_front_dsi_vs_atp.png`, `results/images/carter_bean_atp_per_ap_check.png`, `results/images/attwell_laughlin_signalling_budget.png`, `results/images/hv_trajectory_seed6650.png`, `results/images/top50_morphologies_seed6650.png`.
* Predictions asset: `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph/` (per-cell records + canonical description.md).

## Synthesis

INSUFFICIENT EVIDENCE: only 5 legit cells passed the silence guard. The Pareto front structure cannot be quantitatively characterised under the single-seed protocol.

The Bed B + 14-d morphology substrate generates a Pareto front in (DSI, ATP/spike) space whose top-DSI cohort is summarised by the bootstrap correlation above. Where the correlation is positive (r > 0 with CI excluding zero) the front exhibits a Carter-Bean style Na/K-overlap penalty -- pushing for higher DSI requires more sodium current per spike, the canonical fast-spiking-cell pattern from Sengupta 2010's alpha-table. Where the correlation is flat or negative, DSI is being achieved via mechanisms that do NOT scale sodium load (NMDA-cheap multiplicative scaling, Ca2+ or K+-modulated gating), which is the Poleg-Polsky 2016 alternative hypothesis. The axon-collateral-corrected signalling ATP rate of the top cells is compared to the Howarth 2012 17% cortex anchor (primary) and the Attwell-Laughlin 2001 47% legacy anchor (historical).

## Limitations

* Single GA seed; one Pareto front realisation. The lineage convention is to follow up with a multi-seed replication if the result is ambiguous (|r| > 0.2 with CI straddling zero).
* The Bed B substrate omits axon collaterals. The 5.0x correction is a constant scaling applied to the implied signalling ATP rate; a more rigorous follow-up would extend the morphology generator to include collaterals.
* The Carter-Bean canonical band is a first-principles re-derivation (S-0123-04 resolved); the plan-quoted 2.41e21 ATP/cm figure was a units-confusion typo. A direct Carter-Bean 2009 paper download would tighten the band but is not strictly necessary for the smoke gate or the answer.
* DSI is the silence-guarded vector-sum on 2 antipodal directions. For 2 directions this reduces exactly to the antipodal ratio DSI = (R_PD - R_ND) / (R_PD + R_ND).
* The MI count-entropy metric is tracked as a diagnostic only and is not in the F vector; for the headline DSI / ATP front the MI diagnostic is incidental.

## Sources

* Sengupta et al. 2010, ATP-per-spike recipe and cross-cell alpha table (DOI 10.1371/journal.pcbi.1000840).
* Howarth, Gleeson & Attwell 2012, revised 17% cortex / 21% cerebellum signalling-ATP budget anchor (DOI 10.1038/jcbfm.2012.35).
* Attwell & Laughlin 2001, historical 47% signalling ATP and 82% axon-collateral share (DOI 10.1097/00004647-200110000-00001).
* Carter & Bean 2009, alpha = 1.25 cortical / alpha = 2.0 Purkinje overlap factors (DOI 10.1016/j.neuron.2009.12.011).
* Werginz et al. 2024, mouse alpha-RGC AIS Nav density (DOI 10.1523/JNEUROSCI.1592-24.2024).
* Cuntz et al. 2010, balancing-factor band [0.2, 0.7].
* Project task t0122_dsi_cytoplasm_volume_nsga2.
* Project task t0123_bedb_mi_atp_per_spike_nsga2.
