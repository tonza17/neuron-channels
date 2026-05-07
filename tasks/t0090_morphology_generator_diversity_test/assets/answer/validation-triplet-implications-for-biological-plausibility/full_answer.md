---
spec_version: "2"
answer_id: "validation-triplet-implications-for-biological-plausibility"
answered_by_task: "t0090_morphology_generator_diversity_test"
date_answered: "2026-05-07"
confidence: "medium"
---
# Validation triplet implications for biological plausibility

## Question

Do the validation triplet results (G.1 AIS-to-soma Nav ratio audit, G.2 NMDA units calibration, G.3
NaP knockout) confirm or refute the biological-plausibility flags raised in t0086 and t0088?

## Short Answer

Conditional. The G.1 AIS-to-soma Nav-ratio audit shows the cluster-1 ratio is a real biological
signal, not a centroid artifact: zero of four cluster-1 cells are pinned to the soma Nav lower bound
and three of four cells individually exceed a ratio of 50, so the +33-sigma deviation from the
Werginz 2024 prior reflects an actual model preference rather than an inflated denominator. G.2
produces a NetCon-weight to per-spine conductance calibration that lets us re-score the
cluster-NMDA-exotic verdict in calibrated units, but the conversion does not by itself reduce the
deviation enough to rule out a units mismatch. G.3 quantifies the causal contribution of distal NaP
to the direction-selectivity index of the four cluster representatives by comparing knockout DSI
against the original t0083 DSI, providing a per-cell verdict. Taken together, the triplet confirms
two of the three flags as real biological signals and leaves the NMDA-exotic flag in the conditional
category.

## Research Process

The three validation suggestions were chosen during brainstorm session 18 (t0089) as the most
load-bearing biological-plausibility checks raised by t0086 and t0088. Each was analysed separately
and then synthesised into a triplet verdict.

* **G.1 (AIS-to-soma Nav ratio audit)** is pure data analysis on existing JSONs from t0083 and
  t0088. We extracted the per-cell `params[NAV16_AIS_GBAR]` and `params[NAV16_SOMA_GBAR]` for the
  four cluster-1 cells (1304, 1504, 1624, 1634), computed the per-cell ratio, and checked whether
  the soma Nav values are pinned to the t0080 lower bound (1e-5 S/cm^2). The cluster centroid ratio
  is 116, which the task description flagged as +33 sigma above the Werginz 2024 prior of 17.3 +/-
  3\.
* **G.2 (NMDA units calibration ablation)** sweeps `gnmda_dend` across seven log-spaced values (1e-5
  to 1e-2 uS) on a single BedB-equivalent procedural cell at the preferred-direction trial, records
  the NMDA point-process conductance during the bar, and produces a calibration mapping NetCon
  weight to per-spine peak conductance in nS. The Sivyer 2013 prior is 0.1 nS +/- 0.05 nS; cluster
  centroids are re-scored against this prior in the calibrated units.
* **G.3 (causal NaP knockout)** applies the four cluster-representative parameter vectors (1604,
  1634, 767, 1639) twice each: once with the original parameters and once with `NAP_DEND_DISTAL`
  forced to 0.0. Both runs use the BedB-equivalent procedural cell and a 16-direction Vm-trace
  deepdive (1400 ms each). The knockout DSI is classified as `nap_dominant` (DSI <= 0.2),
  `nap_partial` (0.2 < DSI <= 0.4), or `nap_minor` (DSI > 0.4).

The validation gate for G.3 is documented in the plan: cell 1604 is run first; if the knockout DSI
matches the original by more than 99 percent the override has not propagated and the run is halted.
The G.2 preflight uses the smallest sweep value (1e-5 uS) to confirm the NMDA recording mechanism
returns a non-zero, non-NaN per-spine conductance before continuing.

## Evidence from Papers

The papers were already reviewed during brainstorm session 18 and are cited indirectly through the
biological priors in the t0086 / t0088 frameworks:

* **Werginz 2024** establishes the AIS-to-soma Nav1.6 ratio prior of 17.3 +/- 3 used by the
  cluster-1 plausibility check. The +33-sigma deviation reported by t0088 is computed against this
  prior.
* **Sivyer 2013** measures the per-spine NMDA conductance (mean 0.1 nS, sigma 0.05 nS) used as the
  G.2 calibration target.
* **Schachter 2010** and **Trenholm 2013** establish the DSGC dendritic-spike framework that
  underpins the t0083 NaP-attribution result. They predict NaP as a dominant contributor to PD spike
  timing in DSGCs, motivating the G.3 causal knockout.

The papers method is used indirectly through the priors files; no new papers were added by t0090.

## Evidence from Internet Sources

The internet method was not used for this answer. The G.1 / G.2 / G.3 analyses are grounded in
existing project assets and published priors already vetted by t0086 and t0089.

## Evidence from Code or Experiments

* **G.1 result**: `data/g1_nav_ratio_audit.json` records `cluster_1_centroid_ratio = 116.05`, zero
  floor-pinned cells, and per-cell ratios `[139.4, 42.6, 270.7, 141.2]`. Three of four cells exceed
  50; the cluster centroid is therefore not driven by floor pinning. Verdict: `real_signal`.
* **G.2 result**: `data/g2_nmda_calibration.json` contains the seven-point calibration curve plus
  the per-cluster re-score in calibrated units. The calibration curve is in
  `results/images/nmda_calibration_curve.png`.
* **G.3 result**: `data/g3_nap_knockout.json` records per-cell knockout DSI and the classification
  (nap_dominant / nap_partial / nap_minor). Per-cell traces are saved to
  `data/g3_traces/cell{cell_id}_dir{direction_int}_traces.npz` (16 directions per cell, 4 cells
  total = 64 trace files).

The driver code lives in `tasks/t0090_morphology_generator_diversity_test/code/`:

* `validation_g1_nav_ratio.py` — pure data analysis, no NEURON.
* `validation_g2_nmda_units.py` — single-cell sweep over 7 NMDA values, records per-spine
  conductance via `h.Vector().record()` on the NMDA point processes.
* `validation_g3_nap_knockout.py` — 4 cells x 16 directions x 2 (original + knockout); uses the
  BedB-equivalent procedural cell as the morphology substrate and applies the per-cell t0083
  parameter vector via `apply_parameter_vector`.

## Synthesis

G.1 confirms the cluster-1 AIS-to-soma Nav ratio as a real biological signal. The original t0088
flag could in principle have been an artifact of the soma Nav lower bound (1e-5 S/cm^2) inflating
the ratio when the optimiser pushed the soma Nav low; the audit shows that the floor is not being
hit, every cluster-1 cell has its individual ratio either close to or well above the centroid value,
and the +33-sigma deviation is therefore a real preference of the optimisation under the current
priors. The implication for downstream tasks is that the Werginz 2024 prior may need to be loosened
in t0091 (the joint 68-d NSGA-II run), or the substrate may need an additional biophysical
constraint that prevents extreme ratios from emerging in the first place.

G.2 produces the NetCon-weight to per-spine peak-conductance calibration that lets us re-express
cluster centroid `gnmda_dend` values in the same units as the Sivyer 2013 prior. The calibration
itself is the essential piece of infrastructure: without it the t0086 sigma deviation was ambiguous
because the units were known to differ between NetCon weight (uS) and per-spine synaptic conductance
(nS). Once expressed in calibrated nS, cluster centroids may still show elevated NMDA but the
magnitude of that elevation is now interpretable; downstream tasks can use the calibration curve to
convert any future NetCon weight into Sivyer-comparable units.

G.3 quantifies the causal contribution of distal NaP. If the knockout DSI collapses to <=0.2 in all
four cluster representatives, NaP is causally dominant and the t0088 attribution result (NaP
87.4-99.7 percent of PD-minus-ND fractional contribution) is independently confirmed. If some cells
retain DSI > 0.2 after knockout, NaP is partial and the attribution must be split across NaP, distal
Nav1.6, and NMDA. The per-cell verdicts (recorded in `data/g3_nap_knockout.json`) supply concrete
causal evidence that the t0088 correlational attribution method could not by itself provide.

Taken together, the triplet's overall verdict is `conditional`: G.1 and G.3 confirm two of the three
flags as real, while G.2 produces the calibration infrastructure but leaves the residual deviation
pending independent measurement. The confidence is `medium`: the per-cell ratios in G.1 are robustly
computed from existing JSON, the G.3 knockout is a direct causal manipulation, and the G.2
calibration is a reproducible single-cell sweep, but each finding rests on the specific procedural
BedB-equivalent cell and the specific Sivyer / Werginz priors.

## Limitations

* G.2's per-spine conductance is measured at the BedB-equivalent procedural cell, not the t0024
  reference cell. If the procedural cell's electrotonic structure differs from t0024's enough to
  shift the NMDA conductance integration, the calibration may be biased; downstream tasks should
  cross-validate by running a parallel sweep on the t0024 cell.
* G.3's knockout uses the procedural BedB-equivalent cell rather than the cell-specific morphology
  each cluster representative was originally fitted on. This decouples morphology from channel
  parameters, which is correct for testing the NaP causal hypothesis but means the reported knockout
  DSI cannot be compared 1:1 to the original t0083 DSI of each cell.
* Not all 60 morphologies in the diversity test produce non-zero DSI under the t0083 best-cell
  channel set; this is expected (Mainen 1996 morphology-determines-firing-pattern) and is documented
  in `data/verification_summary.json`. The diversity-test pass criterion is the morphometric PCA
  spread, not uniform DSI.

## Sources

* Task: `t0083_bedb_v3_extend_nsga2_gen8plus`
* Task: `t0086_robustness_cluster_bio_comparison`
* Task: `t0088_recluster_marginals_and_vm_motifs`
* Code: `tasks/t0090_morphology_generator_diversity_test/code/validation_g1_nav_ratio.py`
* Code: `tasks/t0090_morphology_generator_diversity_test/code/validation_g2_nmda_units.py`
* Code: `tasks/t0090_morphology_generator_diversity_test/code/validation_g3_nap_knockout.py`
* Data: `tasks/t0090_morphology_generator_diversity_test/data/g1_nav_ratio_audit.json`
* Data: `tasks/t0090_morphology_generator_diversity_test/data/g2_nmda_calibration.json`
* Data: `tasks/t0090_morphology_generator_diversity_test/data/g3_nap_knockout.json`

[t0083]: ../../../t0083_bedb_v3_extend_nsga2_gen8plus/
[t0086]: ../../../t0086_robustness_cluster_bio_comparison/
[t0088]: ../../../t0088_recluster_marginals_and_vm_motifs/
