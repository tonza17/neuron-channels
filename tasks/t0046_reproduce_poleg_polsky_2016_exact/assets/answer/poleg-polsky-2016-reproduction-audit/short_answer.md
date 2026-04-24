---
spec_version: "2"
answer_id: "poleg-polsky-2016-reproduction-audit"
answered_by_task: "t0046_reproduce_poleg_polsky_2016_exact"
date_answered: "2026-04-24"
---

## Question

Does ModelDB 189347 (Poleg-Polsky and Diamond 2016) reproduce every quantitative claim in
Figures 1-8 of the Neuron paper when re-run faithfully under NEURON 8.2.7, and where do the
paper text and the ModelDB code disagree?

## Answer

Partially. The from-scratch port of ModelDB 189347 reproduces the qualitative direction-tuning
behaviour (PD PSP > ND PSP) and the predicted suppression of selectivity under 0 Mg2+, but
the absolute PSP amplitudes are larger than the paper's reported means at the code-pinned
gNMDA = 0.5 nS, and the paper-vs-code discrepancies on synapse count, gNMDA value, and noise
driver behaviour are confirmed. Ten or more discrepancies are catalogued in the full answer
including six MOD-default-vs-main.hoc-override mismatches and four pre-flagged paper-vs-code
disagreements; every Figure 1-8 reproduction outcome is recorded with numerical evidence.

## Sources

* Paper: `10.1016_j.neuron.2016.02.013` (Poleg-Polsky and Diamond 2016, Neuron)
* Task: `t0008_port_modeldb_189347` (initial port)
* Task: `t0020_port_modeldb_189347_gabamod` (gabaMOD-swap protocol fix)
* URL: https://github.com/ModelDBRepository/189347
* URL: https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf
