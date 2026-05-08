---
spec_version: "2"
answer_id: "objective-functions-for-single-neuron-multi-objective-optimisation"
answered_by_task: "t0097_multi_obj_optim"
date_answered: "2026-05-08"
---
# Catalogue of Multi-Objective Single-Neuron Objective Functions

## Question

Which objective functions have been used in published multi-objective optimisation of single-neuron
compartmental models, and what is each one's formula, units, and NEURON-side computational recipe on
a t0091-style 8-direction trial output?

## Answer

The published multi-objective single-neuron optimisation literature converges on four canonical
biological objective categories that fit directly on top of the project's existing pymoo NSGA-II
loop: stimulus-spike-train mutual information via the direct method with 1/T extrapolation,
ATP-per-spike via per-compartment integration of Na+ inward current divided by three (the Na+/K+
ATPase stoichiometry), cytoplasm volume as the sum of pi*r^2*L over compartments (novel as an
explicit MOO target on a single neuron), and Marder-style robustness as the standard deviation of
DSI under +/-10% perturbation of all channel densities. Each catalogued objective is implemented as
one pymoo evaluator callable on the project's existing 8-direction 1400-ms trial output and is
reported with a uniform 8-field record (name, LaTeX formula, units, NEURON-side quantities, recipe,
biological-plausibility note, direction-of-optimisation, supporting paper citations). The
methodology synthesis adopts per-feature SD-normalisation, the 2-3 SD acceptance threshold and
ensemble-as-experiment reporting pattern, and the optimiser-selection rule NSGA-II for high-d
2-3-objective problems, NSGA-III for high-d many-objective problems, and qLogNEHVI for low-d
constrained problems with population fewer than 20 evaluations. Two additional well-defined
objectives surfaced by the survey are also catalogued with the full 8-field record:
coincidence-detection accuracy (the closest published function-vs-energy MOO analogue to the
project's planned DSI-vs-energy work) and bits-per-ATP efficiency (the canonical empirical Pareto
curve in the field). This answer is grounded in 21 newly catalogued papers plus 9 corpus papers and
the BluePyOpt / eFEL / pymoo / AllenSDK documentation.

## Sources

* Papers (newly catalogued): `10.3389_neuro.01.1.1.001.2007`, `10.1371_journal.pcbi.1002133`,
  `10.1371_journal.pcbi.0020094`, `10.3389_neuro.11.001.2007`, `10.3389_fninf.2016.00017`,
  `10.1038_s41467-017-02718-3`, `10.1097_00004647-200110000-00001`, `10.1242_jeb.017574`,
  `10.1371_journal.pcbi.1000840`, `10.1016_j.neuron.2009.12.011`, `10.1038_nn.3132`,
  `10.1371_journal.pbio.0050116`, `10.1371_journal.pcbi.1006612`, `10.1038_nrn1949`,
  `10.1038_nn1352`, `10.1523_JNEUROSCI.21-14-05229.2001`, `10.1152_jn.00842.2007`,
  `10.1103_PhysRevLett.80.197`, `10.1038_14731`, `10.1162_089976600300015259`,
  `10.1016_S0896-6273(02)00679-7`
* Papers (corpus): `10.1371_journal.pcbi.1002107`, `10.1371_journal.pcbi.1000877`,
  `no-doi_Ament2023_logei-bo`, `10.1523_jneurosci.5346-03.2004`, `10.1098_rstb.1982.0084`,
  `10.1038_382363a0`, `10.1152_jn.1997.78.4.1948`, `10.1162_neco.1997.9.6.1179`,
  `10.1146_annurev.neuro.28.061604.135703`
* Tasks: `t0091_morphology_extended_nsga2_v1`
* URLs: <https://github.com/BlueBrain/BluePyOpt>,
  <https://bluepyopt.readthedocs.io/en/latest/index.html>, <https://github.com/BlueBrain/eFEL>,
  <https://pymoo.org/>, <https://allensdk.readthedocs.io/en/latest/biophysical_models.html>
