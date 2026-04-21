# Results Summary: Morphology and Direction Selectivity Modeling Literature Survey

## Summary

This task added **15 new paper assets** to the morphology-and-direction-selectivity modeling corpus,
bringing the total corpus (baseline + new) to **20 papers**. Coverage now spans retinal SAC and DSGC
models, fly lobula-plate VS and T4 neurons, primate SAC, cat V1 cortical cells, and the
TREES-toolbox cable-theory framework. The strongest cross-paper evidence supports **asymmetric SAC
inhibition** and **electrotonic compartmentalisation** as the DS-shaping morphology mechanisms:
these are replicated across mouse, rabbit, and fly; across TREES, NEURON, NeuronC, and patch-clamp;
and across at least seven papers. Kinetic tiling of bipolar input (sustained-proximal,
transient-distal) is the third replicated mechanism, supported by four independent papers.

Key gaps: **dendritic diameter** is systematically swept in only one paper (Wu2023, primate SAC);
**branch order**, **soma size**, and **branch-angle at fixed length** are all effectively untouched
in the DSGC literature. Cortical DS modeling is limited to one paper (Anderson1999) that rejects
dendritic asymmetry as sufficient and has not been updated with kinetic-tiling tests. The corpus
also contains a genuine contradiction: Sivyer2013 and Schachter2010 argue DSGC DS requires active
dendritic conductances, while Dan2018 (fly VS) and Gruntman2018 (fly T4) show that passive cable or
even a collapsed single compartment can produce DS in invertebrate systems.

The recommended **first sweep on t0022** is distal-dendrite scaling (1.5x length on t0022): the
result discriminates between Dan2018-style passive transfer-resistance weighting and
Sivyer2013-style dendritic-spike branch independence, and it is the single experiment most likely to
tell us whether the **15 Hz peak firing rate at DSI 0.66 gap observed in t0026** is geometry-driven
or channel-driven. The recommended **second sweep** is distal-branch diameter thickening (halving
distal input resistance on t0022), which directly addresses the corpus-level gap on dendritic
diameter and distinguishes active amplification from passive filtering. Both sweeps reuse the
existing `dsgc-baseline-morphology` and cost zero additional compute cycles beyond local CPU.

## Metrics

* **Papers added**: **15** new paper assets (target 12-20, midpoint hit).
* **Baseline papers cited**: **5** (Schachter2010, Jain2020, Morrie2018, PolegPolsky2026,
  deRosenroll2026).
* **Total corpus for synthesis**: **20** papers.
* **Paywalled PDFs**: **2** (Kim2014, Sivyer2013); intervention files filed.
* **Morphology variables taxonomized**: **8** (length, branch count / order, diameter, arbor
  asymmetry / plexus, input spatial layout, input kinetic tiling, transfer-resistance weighting,
  collapse-to-point-compartment nulls).
* **Mechanisms taxonomized**: **7** (electrotonic compartmentalisation, dendritic spike
  thresholding, NMDA multiplicative gating, delay lines, coincidence detection, asymmetric SAC
  inhibition, kinetic tiling).
* **Prioritized testbed recommendations**: **5** morphology sweeps specified.
* **Answer assets produced**: **1** (`morphology-direction-selectivity-modeling-synthesis`).
* **Task cost**: **$0.00**; **0** remote machines used.

## Verification

* `verify_task_results.py` — target 0 errors on final pass (run as final step in this task).
* `verify_task_metrics.py` — target 0 errors (`metrics.json` is empty `{}` because none of this
  task's bookkeeping counters are registered in `meta/metrics/`; the registered metrics
  `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse` are not measured by a literature survey).
* `verify_paper_assets.py` and `verify_answer_assets.py` were run earlier in the task pipeline on
  paper-asset and answer-asset steps; results are referenced in `results_detailed.md`.
