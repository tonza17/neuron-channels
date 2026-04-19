---
spec_version: "2"
task_id: "t0007_install_neuron_netpyne"
---
# Detailed Results: NEURON 8.2.7 + NetPyNE 1.1.1 install

## Summary

Installed NEURON 8.2.7 + NetPyNE 1.1.1 on the project's Windows 11 workstation, wired the NEURON
Python bindings into the uv venv via a `.pth` file, compiled `khhchan.mod` with `nrnivmodl`, and
executed two Hodgkin-Huxley single-compartment sanity simulations (raw NEURON and NetPyNE) that both
fire action potentials peaking at **42.003 mV**. Published the `neuron-netpyne-install-report`
answer asset with an eight-section report and embedded trace plots.

## Methodology

The install ran in three phases: (1) NEURON core install from the official `nrn-8.2.7-setup.exe`
Windows installer, (2) NetPyNE install via `uv pip install netpyne==1.1.1` into the repository's uv
venv, and (3) sanity verification through two parallel Hodgkin-Huxley single-compartment simulations
— one in raw NEURON and one wrapped through NetPyNE's `specs.NetParams` / `specs.SimConfig`
harness.

### Machine Specs

* Hardware: Windows 11 Education 22631, 16-core x86_64 workstation.
* Python: 3.13 (pinned by `.python-version`); uv-managed venv at `<repo>\.venv`.
* NEURON: 8.2.7+ (HEAD 34cf696+, release build 2025-05-21) installed to `C:\Users\md1avn\nrn-8.2.7`
  via the interactive GUI installer.
* NetPyNE: 1.1.1 installed from PyPI into the uv venv with all transitive dependencies satisfied.

### Runtime

* Step 9 (implementation) started 2026-04-19T21:00:11Z, completed 2026-04-19T22:34:58Z (~1h 35m
  wall-clock, most of which was interactive installer time).
* Raw NEURON sanity sim: **0.011 s** total (setup 6.7 ms + run 4.4 ms).
* NetPyNE sanity sim: **0.044 s** total (setup 38.7 ms + run 4.8 ms).
* `nrnivmodl` compile time: under **5 seconds**.

### Wiring Strategy

NEURON's installer places its Python bindings under `C:\Users\md1avn\nrn-8.2.7\lib\python\neuron`.
Rather than copy the package into the venv, we created a single `.pth` file at
`<repo>\.venv\Lib\site-packages\neuron.pth` containing the one-line path
`C:\Users\md1avn\nrn-8.2.7\lib\python`. Python's `site.py` expands the `.pth` at import time, so
`from neuron import h` resolves through the native install. The scripts also set
`NEURONHOME=C:\Users\md1avn\nrn-8.2.7` via `os.environ.setdefault` so `os.add_dll_directory` picks
up the correct DLL search root on Windows.

### Sanity Simulation Design

Both simulations use identical biophysics:

* Single soma compartment, 20 μm length × 20 μm diameter.
* NEURON built-in `hh` mechanism inserted on the soma.
* IClamp electrode at soma midpoint (0.5), delay 5 ms, duration 50 ms, amplitude 0.5 nA.
* Integrator: fixed-step, `dt=0.025 ms`, `tstop=80 ms`.
* Threshold used for pass/fail: `v_max > +20 mV`.

The raw NEURON sim (`code/sanity_raw_neuron.py`) uses `h.Section`, `h.IClamp`, and
`h.Vector().record` directly, then `h.finitialize(-65.0)` followed by `h.continuerun(80.0)`. The
NetPyNE sim (`code/sanity_netpyne.py`) constructs the same biophysics through `specs.NetParams` and
`specs.SimConfig`, then runs `sim.initialize`, `sim.net.createPops`, `sim.net.createCells`,
`sim.net.addStims`, `sim.setupRecording`, `sim.runSim`, and `sim.gatherData`.

## Metrics Tables

### Sanity-Simulation Outcomes

| Harness | `v_max` (mV) | `v_min` (mV) | Samples | Setup (s) | Run (s) | Crossed +20 mV |
| --- | ---: | ---: | ---: | ---: | ---: | :--- |
| Raw NEURON | 42.00255 | -75.96756 | 3201 | 0.0067 | 0.0044 | yes |
| NetPyNE | 42.00255 | -75.96756 | 3201 | 0.0387 | 0.0048 | yes |

`v_max` and `v_min` agree to machine precision. NetPyNE's setup is ~6× slower than the raw NEURON
path because the `specs.NetParams` / `specs.SimConfig` expansion does dictionary walks and
network-scaffolding work that raw NEURON skips, but the actual integration runtime is
indistinguishable.

### Spike Count

Both simulations fire **six** action potentials across the 50 ms stimulus window — 120 Hz
instantaneous rate during the stimulus, 75 Hz averaged over the 80 ms simulation.

## Visualizations

![Raw NEURON HH soma trace](../data/images/raw_neuron_trace.png)

![NetPyNE HH soma trace](../data/images/netpyne_trace.png)

## Verification

* `uv run ruff check tasks/t0007_install_neuron_netpyne/code/` — PASSED (all checks).
* `uv run ruff format tasks/t0007_install_neuron_netpyne/code/` — PASSED (no changes).
* `uv run mypy -p tasks.t0007_install_neuron_netpyne.code` — PASSED (no issues).
* Raw NEURON sanity sim exits 0 with the `v_max > +20 mV` assertion satisfied.
* NetPyNE sanity sim exits 0 with the `v_max > +20 mV` assertion satisfied.
* Compiled `nrnmech.dll` loads via `h.nrn_load_dll` with no error.
* `neuron.__version__` prints `"8.2.7+"`; `netpyne.__version__` prints `"1.1.1"`; `h("VERSION")`
  prints the full build string with `34cf696+ (2025-05-21)`.

## Limitations

* Tested only on Windows 11 with Python 3.13. Linux / macOS compatibility is inherited from
  NetPyNE's upstream releases but was not verified here.
* The sanity sim exercises only the built-in `hh` mechanism. Custom MOD correctness (e.g., `khhchan`
  biophysics) is validated only by compilation success, not by a dedicated simulation.
* NetPyNE's `sim.analysis.plot*` helpers were not exercised. The pipeline saves raw voltage traces
  and builds plots via matplotlib directly, so any downstream use of NetPyNE's plotting API will
  need its own verification.
* The NSIS silent installer did not accept the `/D=` prefix, so install required interactive user
  action. Automated end-to-end reproduction on a fresh machine needs either a pre-installed NEURON
  or the manual GUI step documented in the answer asset.

## Files Created

* `code/sanity_raw_neuron.py` — raw NEURON HH soma sanity script.
* `code/sanity_netpyne.py` — NetPyNE HH soma sanity script (parallel harness).
* `code/run_nrnivmodl.cmd` — cmd.exe wrapper for `nrnivmodl.bat` (MSYS path-mangling workaround).
* `data/mod/khhchan.mod` — custom Hodgkin-Huxley MOD (compiled smoke-test input).
* `data/mod/nrnmech.dll` — compiled mechanism library (132 KB, reusable downstream).
* `data/csv/raw_neuron_trace.csv`, `data/csv/netpyne_trace.csv` — voltage traces.
* `data/images/raw_neuron_trace.png`, `data/images/netpyne_trace.png` — trace plots.
* `data/json/raw_neuron_timings.json`, `data/json/netpyne_timings.json`, `data/json/versions.json`
  — wall-clock, threshold, and version provenance.
* `data/installer/.gitkeep` — placeholder (installer binary deleted to keep repo size down).
* `assets/answer/neuron-netpyne-install-report/details.json` — answer asset metadata.
* `assets/answer/neuron-netpyne-install-report/short_answer.md` — three-section short report.
* `assets/answer/neuron-netpyne-install-report/full_answer.md` — eight-section full report.
* `results/results_summary.md`, `results/results_detailed.md`, `results/metrics.json`,
  `results/costs.json`, `results/remote_machines_used.json`.
* `logs/commands/006_*` through `logs/commands/015_*` — command-log JSON + stdout/stderr for curl,
  installer, `uv pip`, `nrnivmodl`, and both sanity sims.

## Task Requirement Coverage

Operative task request (`task.json` `short_description`):

> Install NEURON 8.2.7 and NetPyNE 1.1.1 on the project's Windows 11 workstation, compile a minimal
> Hodgkin-Huxley MOD file with `nrnivmodl`, run a 1-compartment sanity simulation in both raw NEURON
> and NetPyNE, and publish a `neuron-netpyne-install-report` answer asset documenting the install,
> compile, and sanity-simulation outcomes.

Requirement status (REQ IDs reused from `plan/plan.md`):

| REQ | Status | Answer and evidence |
| --- | --- | --- |
| REQ-1 — Install NEURON 8.2.7 and NetPyNE 1.1.1 reachable from the project's uv venv | Done | NEURON 8.2.7+ installed to `C:\Users\md1avn\nrn-8.2.7`; NetPyNE 1.1.1 installed into the uv venv. Evidence: `data/json/versions.json`, `logs/commands/008_*` (pip install log). |
| REQ-2 — Compile at least one HH MOD with `nrnivmodl` | Done | `khhchan.mod` compiled to `data/mod/nrnmech.dll` (132 KB). Evidence: `data/mod/nrnmech.dll`, `logs/commands/013_*` (nrnivmodl log). |
| REQ-3 — 1-compartment raw-NEURON sanity sim (L = diam = 20 μm, hh mechanism, 0.5 nA / 50 ms IClamp, 80 ms, dt 0.025 ms) | Done | `code/sanity_raw_neuron.py` implements the spec exactly. Evidence: `data/csv/raw_neuron_trace.csv`, `data/images/raw_neuron_trace.png`. |
| REQ-4 — Confirm sim crosses +20 mV | Done | Raw NEURON `v_max = 42.003 mV`; NetPyNE `v_max = 42.003 mV`. Both assertions pass. Evidence: `data/json/raw_neuron_timings.json`, `data/json/netpyne_timings.json`. |
| REQ-5 — Repeat REQ-3/REQ-4 under NetPyNE's `specs.NetParams` + simulate harness | Done | `code/sanity_netpyne.py` matches raw NEURON at machine precision. Evidence: `data/csv/netpyne_trace.csv`, `data/images/netpyne_trace.png`. |
| REQ-6 — Record final installed versions | Done | `data/json/versions.json` captures `neuron.__version__`, `netpyne.__version__`, NEURON build string, Python version. |
| REQ-7 — Record `nrnivmodl` output, sanity-sim wall-clocks, and every command log | Done | `logs/commands/006_*` through `logs/commands/015_*` capture every shelled command (JSON + stdout + stderr). `data/json/raw_neuron_timings.json` and `data/json/netpyne_timings.json` record sanity-sim wall-clocks. |
| REQ-8 — Publish `neuron-netpyne-install-report` answer asset with `details.json`, `short_answer.md`, `full_answer.md` | Done | `assets/answer/neuron-netpyne-install-report/` contains all three files; full_answer.md includes all eight mandatory answer sections. |
| REQ-9 — File an intervention if any install step fails irrecoverably | Not triggered | Install succeeded (with the interactive-installer fallback for the silent-install deviation). No intervention file needed; `intervention/.gitkeep` placeholder only. |
