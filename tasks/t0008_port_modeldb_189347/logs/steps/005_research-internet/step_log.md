---
spec_version: "3"
task_id: "t0008_port_modeldb_189347"
step_number: 5
step_name: "research-internet"
status: "completed"
started_at: "2026-04-20T10:25:38Z"
completed_at: "2026-04-20T10:40:00Z"
---
## Summary

Internet research recovered the canonical ModelDB 189347 mirror at
`github.com/ModelDBRepository/189347` and extracted authoritative simulation parameters directly
from `main.hoc` (`tstop=1000ms`, `dt=0.1ms`, `tau1NMDA_bipNMDA=60ms`, `e_SACinhib=-60mV`).
Identified `geoffder/Spatial-Offset-DSGC-NEURON-Model` (Hanson 2019) as the highest-priority Phase B
sibling port with usable fallback synaptic weights (`inhibWeight=0.004µS`, `nmdaWeight=0.0015µS`),
plus Ezra-Tsur 2022 (`NBELab/RSME`) as a stretch-goal SAC-DSGC network reference. Confirmed no
erratum exists for Poleg-Polsky 2016 and documented NEURON 8.2 / NetPyNE 1.1.1 porting tips.

## Actions Taken

1. Read `research/research_papers.md` to avoid redundant effort, then issued targeted WebSearch and
   WebFetch queries for ModelDB 189347, Hanson 2019 fork, Ezra-Tsur 2022, and porting issues.
2. Wrote `research/research_internet.md` per `arf/specifications/research_internet_specification.md`
   with all mandatory sections including ModelDB archive structure, authoritative parameters, Phase
   B sibling candidates, and NEURON 8.2 migration notes.
3. Ran `verify_research_internet t0008_port_modeldb_189347` → PASSED with 0 errors, 0 warnings.

## Outputs

* `tasks/t0008_port_modeldb_189347/research/research_internet.md`
* `tasks/t0008_port_modeldb_189347/logs/commands/*_uv-run-python.*` (verify_research_internet)
* `tasks/t0008_port_modeldb_189347/logs/steps/005_research-internet/step_log.md`

## Issues

No issues encountered.
