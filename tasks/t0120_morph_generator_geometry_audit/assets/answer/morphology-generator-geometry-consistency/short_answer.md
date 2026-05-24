---
spec_version: "2"
answer_id: "morphology-generator-geometry-consistency"
answered_by_task: "t0120_morph_generator_geometry_audit"
date_answered: "2026-05-24"
---
# Yes -- generator geometry is consistent across all 20 cells; the visual artefact is rendering-only and prior NSGA-II runs are NOT invalidated

## Question

Is the procedural morphology generator's asymmetry transform geometrically consistent across the
15-20 sampled cells, and do its results invalidate prior NSGA-II runs?

## Answer

Yes -- across 20 cells sampled from the t0117 pooled pool (stratified across the four asymmetry
parameters plus worst-looking cells and symmetric controls), all three coordinate-consistency checks
pass (60 of 60 evaluations), with maximum Python-side endpoint error of 0.0 um and maximum NEURON
pt3d lateral deviation of 19.6 nm (float-arithmetic noise, four orders below the 0.1 um audit
threshold). The deliberate soma-frame split introduced by the t0092 fix (Python origin_xy at the
post-asymmetry soma position, NEURON soma pt3d pinned at (0, 0)) is benign because SAC synapses are
placed only on dendrites in the t0091 / t0118 protocol, so the bar arrival-time projection
`(syn_xy - origin_xy)` cancels soma_offset correctly. Prior 68-d morphology-extended NSGA-II results
(t0091, t0099, t0102, t0104, t0106, t0112, t0114, t0115, t0118) are NOT invalidated; the
soma-disconnection visual artefact in t0115's top50_morphologies_seed9354.png is a rendering
convention issue, not a geometry bug.

## Sources

* Task: `t0090_morphology_generator_diversity_test`
* Task: `t0091_morphology_extended_nsga2_v1`
* Task: `t0092_diagnose_morphology_generator_silence`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
* Task: `t0119_brainstorm_results_23`
