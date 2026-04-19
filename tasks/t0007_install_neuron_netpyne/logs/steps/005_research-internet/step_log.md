---
spec_version: "3"
task_id: "t0007_install_neuron_netpyne"
step_number: 5
step_name: "research-internet"
status: "completed"
started_at: "2026-04-19T20:31:34Z"
completed_at: "2026-04-19T20:37:00Z"
---
## Summary

Spawned a research-internet subagent to survey Windows install gotchas for NEURON 8.2.7 + NetPyNE
1.1.1 and the real-world behaviour of `nrnivmodl`; produced `research/research_internet.md` with all
mandatory sections and uncovered a critical finding that native Windows pip wheels for NEURON do not
exist.

## Actions Taken

1. Ran `uv run python -m arf.scripts.utils.prestep t0007_install_neuron_netpyne research-internet`.
2. Spawned a general-purpose subagent with the research-internet brief (focus on Windows install,
   `nrnivmodl` C-compiler requirements, HH MOD location, NetPyNE ↔ NEURON compatibility).
3. Subagent produced `tasks/t0007_install_neuron_netpyne/research/research_internet.md` covering the
   8 mandatory sections, 10 queries, 14 sources cited, and ran flowmark.
4. Ran
   `uv run python -u -m arf.scripts.verificators.verify_research_internet t0007_install_neuron_netpyne`
   which returned `PASSED — no errors or warnings`.

## Outputs

* `tasks/t0007_install_neuron_netpyne/research/research_internet.md`
* `tasks/t0007_install_neuron_netpyne/logs/steps/005_research-internet/step_log.md`

## Issues

Research surfaced a blocking constraint for implementation: NEURON ships **no Windows pip wheel** at
any version — `uv pip install neuron==8.2.7` will fail on native Windows 11. The install path must
be either WSL (Linux wheel) or the official `.exe` binary installer (bundles MinGW for `nrnivmodl`).
Planning (step 7) must pick one path and may need to file an intervention if UI interaction or WSL
setup is required.
