---
spec_version: "2"
answer_id: "dsgc-modeldb-port-reproduction-report"
answered_by_task: "t0008_port_modeldb_189347"
date_answered: "2026-04-20"
---
# ModelDB 189347 DSGC port and sibling-model survey

## Question

Can ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC) be reproduced locally on Windows
as a headless library, does it hit the published direction-selectivity envelope with a canonical
12-angle x 20-trial drifting-bar protocol, and which sibling DSGC compartmental models are the
next-best candidates for porting in the same pipeline?

## Answer

Yes, ModelDB 189347 was ported and runs headless on Windows 11 with NEURON 8.2.7 via a Python driver
that sources the verbatim HOC and MOD files through `h.load_file`/`h.nrn_load_dll`; a 12-angle x
20-trial sweep on the bundled morphology completed end-to-end in roughly 10 minutes and the four
registered metrics (DSI, HWHM, reliability, RMSE vs target) were written to `results/metrics.json`.
The tuning curve does not hit the published envelope at the bundled parameters (peak well below 40
Hz, DSI well below 0.7), because the paper derives DS from a `gabaMOD` parameter swap rather than
from spatial rotation — the port's rotation-based protocol is only a proxy for a direction-
selective stimulus. The Hanson et al. 2019 Spatial-Offset-DSGC model (GitHub
`geoffder/Spatial-Offset-DSGC-NEURON-Model`) is the next-best port candidate: it shares
`RGCmodel.hoc` and `HHst.mod` with 189347 and already ships a Python driver; Jain 2020 is
medium-effort; Ding 2016, Schachter 2010, Koren 2017, and Ezra-Tsur 2022 either lack a public
compartmental model or address a different modelling class.

## Sources

* Task: `t0004_generate_target_tuning_curve`
* Task: `t0007_install_neuron_netpyne`
* Task: `t0009_calibrate_dendritic_diameters`
* Task: `t0012_tuning_curve_scoring_loss_library`
* URL: https://modeldb.science/189347
* URL: https://github.com/ModelDBRepository/189347
* URL: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model
* URL: https://elifesciences.org/articles/42392v1
