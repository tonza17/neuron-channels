---
spec_version: "1"
task_id: "t0007_install_neuron_netpyne"
date_completed: "2026-04-19"
---
# Results Summary: NEURON 8.2.7 + NetPyNE 1.1.1 install

## Summary

The NEURON 8.2.7 + NetPyNE 1.1.1 toolchain installs, compiles MOD files, and runs a
single-compartment Hodgkin-Huxley sanity simulation end-to-end on the project's Windows 11
workstation. Raw NEURON and NetPyNE sanity sims agree to machine precision at **v_max = 42.003 mV**,
confirming the stack is ready for downstream modelling tasks (t0008, t0010, t0011).

## Metrics

* Raw NEURON sanity sim: **v_max = 42.003 mV**, crossed +20 mV threshold, 3201 samples, setup **6.7
  ms**, run **4.4 ms**.
* NetPyNE sanity sim: **v_max = 42.003 mV**, crossed +20 mV threshold, 3201 samples, setup **38.7
  ms**, run **4.8 ms**.
* Raw-NEURON and NetPyNE traces agree on `v_max` to **machine precision** (1e-15 mV).
* `nrnivmodl` compiled `khhchan.mod` into **132 KB** `nrnmech.dll` in under **5 seconds** with no
  warnings or errors.
* Total third-party cost: **$0.00** (local workstation, no remote compute, no paid APIs).

## Verification

* `uv run ruff check tasks/t0007_install_neuron_netpyne/code/` — PASSED (all checks).
* `uv run ruff format tasks/t0007_install_neuron_netpyne/code/` — PASSED (no changes).
* `uv run mypy -p tasks.t0007_install_neuron_netpyne.code` — PASSED (no issues).
* Raw NEURON sanity sim exit code 0 with `v_max > +20 mV` assertion satisfied.
* NetPyNE sanity sim exit code 0 with `v_max > +20 mV` assertion satisfied.
* Compiled `nrnmech.dll` loads successfully via `h.nrn_load_dll` with no error.

## Assets Produced

* `assets/answer/neuron-netpyne-install-report/` — answer asset with `short_answer.md`,
  `full_answer.md`, and `details.json`.
* `data/mod/nrnmech.dll` — compiled HH mechanism library, reusable by downstream tasks.
* `data/images/raw_neuron_trace.png`, `data/images/netpyne_trace.png` — sanity traces.
* `data/csv/raw_neuron_trace.csv`, `data/csv/netpyne_trace.csv` — raw sample data.
* `data/json/raw_neuron_timings.json`, `data/json/netpyne_timings.json`, `data/json/versions.json`
  — wall-clock and version provenance.
