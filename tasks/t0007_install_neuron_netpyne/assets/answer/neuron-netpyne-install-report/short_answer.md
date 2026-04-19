---
spec_version: "2"
answer_id: "neuron-netpyne-install-report"
answered_by_task: "t0007_install_neuron_netpyne"
date_answered: "2026-04-19"
---
# NEURON 8.2.7 + NetPyNE 1.1.1 install report

## Question

Does the NEURON 8.2.7 + NetPyNE 1.1.1 toolchain install, compile MOD files, and run a 1-compartment
Hodgkin-Huxley sanity simulation on the project's Windows 11 workstation?

## Answer

Yes. NEURON 8.2.7+ (HEAD 34cf696+, build 2025-05-21) installs via the Windows `.exe` binary wired
into the uv venv with a `.pth` file, NetPyNE 1.1.1 installs via `uv pip`, `nrnivmodl` compiles
`khhchan.mod` into `nrnmech.dll` with no errors, and both sanity simulations (raw NEURON and
NetPyNE) fire action potentials reaching **42.003 mV** (> **+20 mV** threshold) under a 0.5 nA / 50
ms IClamp. Raw NEURON run time is **4.4 ms** wall-clock; NetPyNE run time is **4.8 ms**. The
toolchain is validated end-to-end for downstream t0008 / t0010 / t0011 tasks.

## Sources

* Task: `t0007_install_neuron_netpyne`
* URL: <https://github.com/neuronsimulator/nrn/releases/tag/8.2.7>
* URL: <https://pypi.org/project/netpyne/1.1.1/>
