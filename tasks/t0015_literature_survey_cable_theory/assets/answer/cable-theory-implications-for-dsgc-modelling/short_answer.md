---
spec_version: "2"
answer_id: "cable-theory-implications-for-dsgc-modelling"
answered_by_task: "t0015_literature_survey_cable_theory"
date_answered: "2026-04-20"
---
## Question

What does the classical cable-theory and dendritic-computation literature imply for the
compartmental modelling of direction-selective retinal ganglion cells (DSGCs) in NEURON?

## Answer

DSGC compartmental models in NEURON must use morphologically accurate reconstructions (not ball-
and-stick), discretized with the `d_lambda` rule, and must implement direction selectivity via
postsynaptic dendritic shunting inhibition rather than presynaptic wiring asymmetry. The DS
computation must arise from asymmetric inhibitory input acting locally on dendritic branches via the
Koch-Poggio-Torre on-the-path shunting mechanism, and the model must be validated by measuring EPSP
shape-indices, losing DS under simulated inhibition block, and reproducing the graded-vs- spike
contrast-sensitivity trade-off.

## Sources

* Paper: `10.1152_jn.1967.30.5.1138` (Rall 1967)
* Paper: `10.1098_rstb.1982.0084` (Koch, Poggio, Torre 1982)
* Paper: `10.1038_382363a0` (Mainen & Sejnowski 1996)
* Paper: `10.1126_science.289.5488.2347` (Taylor, He, Levick, Vaney 2000)
* Paper: `10.1523_jneurosci.5346-03.2004` (Dhingra & Smith 2004)
