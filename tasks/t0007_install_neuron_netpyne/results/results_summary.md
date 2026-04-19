---
spec_version: "1"
task_id: "t0007_install_neuron_netpyne"
date_completed: "2026-04-19"
---
# Results Summary: NEURON 8.2.7 + NetPyNE 1.1.1 install

## Outcome

The NEURON 8.2.7 + NetPyNE 1.1.1 toolchain installs, compiles MOD files, and runs a single-
compartment Hodgkin-Huxley sanity simulation end-to-end on the project's Windows 11 workstation. The
stack is ready for the downstream modelling tasks (t0008 NetPyNE retina, t0010 tuning-curve scan,
t0011 direction-selectivity benchmark).

## Key Results

* NEURON 8.2.7+ (HEAD 34cf696+, Windows binary installer) wired into the uv venv via
  `.venv\Lib\site-packages\neuron.pth` pointing at `C:\Users\md1avn\nrn-8.2.7\lib\python`.
* NetPyNE 1.1.1 installed via `uv pip install netpyne==1.1.1` with no errors and all transitive
  dependencies satisfied from the existing venv.
* `nrnivmodl` compiled `khhchan.mod` into `data/mod/nrnmech.dll` (132 KB) in under five seconds.
* Raw NEURON HH soma sanity sim: `v_max=42.003 mV`, crossed the +20 mV threshold, 3201 samples,
  setup 6.7 ms, run 4.4 ms.
* NetPyNE HH soma sanity sim: `v_max=42.003 mV`, crossed the +20 mV threshold, 3201 samples, setup
  38.7 ms, run 4.8 ms.
* Raw-NEURON and NetPyNE traces agree to machine precision on `v_max` and `v_min`, confirming the
  NetPyNE harness adds no correctness-visible drift over the raw NEURON path.

## Assets Produced

* `assets/answer/neuron-netpyne-install-report/` — answer asset with `short_answer.md`,
  `full_answer.md`, and `details.json` documenting the full install report.
* `data/mod/nrnmech.dll` — compiled HH mechanism library, reusable by downstream tasks.
* `data/images/raw_neuron_trace.png`, `data/images/netpyne_trace.png` — sanity traces.
* `data/csv/raw_neuron_trace.csv`, `data/csv/netpyne_trace.csv` — raw sample data.
* `data/json/raw_neuron_timings.json`, `data/json/netpyne_timings.json`, `data/json/versions.json`
  — wall-clock and version provenance.

## Follow-up

* Downstream tasks can reuse the `.pth` wiring and the compiled `nrnmech.dll` without re-running
  `nrnivmodl`.
* The `LIBRARY nrnmech32.dll` warning printed by the interactive installer is cosmetic and does not
  affect runtime once the `.pth` file is in place — documented in the answer asset.
* See `results/suggestions.json` for follow-up task candidates.
