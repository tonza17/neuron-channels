---
spec_version: "2"
answer_id: "dsgc-compartmental-simulator-choice"
answered_by_task: "t0003_simulator_library_survey"
date_answered: "2026-04-19"
---
# DSGC compartmental simulator choice

## Question

Which compartmental simulator should the direction-selective ganglion cell (DSGC) project use as its
primary simulator, and which should it keep as a backup?

## Answer

Use NEURON 8.2.7 as the primary simulator, wrapped with NetPyNE 1.1.1 for parameter sweeps and
optimisation. Keep Arbor 0.12.0 as the backup simulator to exploit its 7-12x single-cell speedup
whenever the parameter sweep outgrows the NEURON workstation budget. Brian2 and MOOSE are rejected
because Brian2's own authors describe its multicompartment support as immature and MOOSE shows the
weakest maintenance signal of the five candidates.

## Sources

* URL: https://modeldb.science/189347
* URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9272742/
* URL: https://elifesciences.org/articles/47314
* URL: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013926
* URL: https://github.com/neuronsimulator/nrn/blob/master/docs/changelog.md
* URL: https://github.com/arbor-sim/arbor/releases
* URL: https://docs.arbor-sim.org/en/latest/fileformat/nmodl.html
* URL: http://doc.netpyne.org/
* URL: https://github.com/suny-downstate-medical-center/netpyne
* URL: https://brian2.readthedocs.io/en/stable/user/multicompartmental.html
* URL: https://github.com/brian-team/brian2
* URL: https://github.com/BhallaLab/moose
* URL: https://moose.ncbs.res.in/readthedocs/user/py/rdesigneur/rdes.html
