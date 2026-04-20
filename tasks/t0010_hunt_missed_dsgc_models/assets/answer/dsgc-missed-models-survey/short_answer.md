---
spec_version: "2"
answer_id: "dsgc-missed-models-survey"
answered_by_task: "t0010_hunt_missed_dsgc_models"
date_answered: "2026-04-20"
---
# Missed DSGC compartmental models: hunt and port viability

## Question

What DSGC compartmental models published in public literature were missed by tasks t0002 and t0008,
and which of them are viable ports for this project?

## Answer

Two brand-new DSGC compartmental-model papers were missed by the prior corpus: deRosenroll et al.
2026 (Cell Reports, DOI `10.1016/j.celrep.2025.116833`) and Poleg-Polsky 2026 (Nature
Communications, DOI `10.1038/s41467-026-70288-4`); Hanson 2019 (`10.7554/eLife.42392`) was in the
t0002 corpus but had never been ported. None of the three HIGH-priority candidates completed a
12-angle canonical sweep within the 90-minute-per-candidate port budget — each failed at the P2
upstream-demo gate for a different structural reason (Hanson: headfull Python driver with hardcoded
Windows paths; deRosenroll: hardcoded 8-direction stimulus grid plus heavy out-of-env dependencies;
Poleg-Polsky: genetic-algorithm training driver with `numDir=2` and no LICENSE). Zero library assets
were registered per the "never leave a broken library behind" rule, and all three candidates are
recorded as `p2_failed` in `data/candidates.csv`. Deeper investment (hand-rewriting each driver)
would very plausibly succeed; the 90-minute cap is the binding constraint, not a definitive
portability verdict.

## Sources

* Paper: `10.1016_j.celrep.2025.116833`
* Paper: `10.1038_s41467-026-70288-4`
* Paper: `10.7554_eLife.42392`
* Task: `t0002_literature_survey_dsgc_compartmental_models`
* Task: `t0008_port_modeldb_189347`
* Task: `t0012_tuning_curve_scoring_loss_library`
* URL: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model
* URL: https://github.com/geoffder/ds-circuit-ei-microarchitecture
* URL: https://doi.org/10.5281/zenodo.17666157
* URL: https://github.com/PolegPolskyLab/DS-mechanisms
