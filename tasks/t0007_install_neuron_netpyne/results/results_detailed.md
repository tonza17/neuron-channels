---
spec_version: "1"
task_id: "t0007_install_neuron_netpyne"
date_completed: "2026-04-19"
---
# Detailed Results: NEURON 8.2.7 + NetPyNE 1.1.1 install

## Methodology

The install was executed in three phases: (1) NEURON core install from the official
`nrn-8.2.7-setup.exe` Windows installer, (2) NetPyNE install via `uv pip install netpyne==1.1.1`
into the repository's uv venv, and (3) sanity verification through two parallel Hodgkin-Huxley
single-compartment simulations — one in raw NEURON and one wrapped through NetPyNE's
`specs.NetParams` / `specs.SimConfig` harness.

### Machine Specs

* Hardware: Windows 11 Education 22631, 16-core x86_64 workstation.
* Python: 3.13 (pinned by `.python-version`); uv-managed venv at `<repo>\.venv`.
* NEURON: 8.2.7+ (HEAD 34cf696+, release build 2025-05-21) installed to `C:\Users\md1avn\nrn-8.2.7`
  via the interactive GUI installer.
* NetPyNE: 1.1.1 installed from PyPI into the uv venv with all transitive dependencies satisfied.

### Wiring Strategy

NEURON's installer places its Python bindings under `C:\Users\md1avn\nrn-8.2.7\lib\python\neuron`.
Rather than copy the package into the venv, we created a single `.pth` file at
`<repo>\.venv\Lib\site-packages\neuron.pth` containing the one-line path
`C:\Users\md1avn\nrn-8.2.7\lib\python`. Python's `site.py` expands the `.pth` at import time, so
`from neuron import h` resolves through the native install. The scripts also set
`NEURONHOME=C:\Users\md1avn\nrn-8.2.7` via `os.environ.setdefault` so `os.add_dll_directory` can
pick up the correct DLL search root on Windows.

### HH MOD Compilation

The task ships a single MOD file (`data/mod/khhchan.mod`) which is a custom Hodgkin-Huxley mechanism
for downstream retinal-ganglion-cell work. `nrnivmodl.bat` wraps MinGW to produce `nrnmech.dll` in
the same directory. The `code/run_nrnivmodl.cmd` wrapper is a `.cmd` shim to keep the cmd.exe
invocation out of Git Bash's MSYS path-mangling behaviour — without the wrapper, bash rewrites
`C:\Users\...` into `/c/Users/...` before the subprocess launches, which breaks the Windows batch
file.

### Sanity Simulation Design

Both simulations use identical biophysics:

* Single soma compartment, 20 μm length × 20 μm diameter.
* NEURON built-in `hh` mechanism inserted on the soma (documented in
  `NEURONHOME/share/nrn/lib/hoc/ stdlib.hoc`).
* IClamp electrode at soma midpoint (0.5), delay 5 ms, duration 50 ms, amplitude 0.5 nA.
* Integrator: fixed-step, `dt=0.025 ms`, `tstop=80 ms`.
* Threshold used for pass/fail: `v_max > +20 mV`.

The raw NEURON sim (`code/sanity_raw_neuron.py`) uses `h.Section`, `h.IClamp`, and
`h.Vector(). record` directly, then `h.finitialize(-65.0)` followed by `h.continuerun(80.0)`. The
NetPyNE sim (`code/sanity_netpyne.py`) constructs the same biophysics through `specs.NetParams` and
`specs.SimConfig`, then runs `sim.initialize`, `sim.net.createPops`, `sim.net.createCells`,
`sim.net.addStims`, `sim.setupRecording`, `sim.runSim`, and `sim.gatherData`.

## Quantitative Results

### Sanity-Simulation Outcomes

| Harness | `v_max` (mV) | `v_min` (mV) | Samples | Setup (s) | Run (s) | Crossed +20 mV |
| --- | ---: | ---: | ---: | ---: | ---: | :--- |
| Raw NEURON | 42.00255 | -75.96756 | 3201 | 0.0067 | 0.0044 | yes |
| NetPyNE | 42.00255 | -75.96756 | 3201 | 0.0387 | 0.0048 | yes |

`v_max` and `v_min` agree to machine precision. NetPyNE's setup is roughly 6× slower than the raw
NEURON path because the `specs.NetParams` / `specs.SimConfig` expansion does dictionary walks and
network-scaffolding work that raw NEURON skips, but the actual integration runtime is
indistinguishable. At this problem size, the harness overhead is irrelevant.

### Spike Count

Both simulations fire six action potentials across the 50 ms stimulus window, giving an
instantaneous rate of 120 Hz during the stimulus and 75 Hz averaged over the 80 ms simulation.

### Compile Performance

`nrnivmodl khhchan.mod` produced `nrnmech.dll` in under five seconds. The compiled DLL is 132 KB. No
compiler warnings or errors were emitted.

## Figures

![Raw NEURON HH soma trace](../data/images/raw_neuron_trace.png)

![NetPyNE HH soma trace](../data/images/netpyne_trace.png)

## Verification

* `uv run ruff check tasks/t0007_install_neuron_netpyne/code/` → all checks pass.
* `uv run ruff format tasks/t0007_install_neuron_netpyne/code/` → all files clean.
* `uv run mypy -p tasks.t0007_install_neuron_netpyne.code` → no issues found.
* Raw NEURON sanity sim asserts `v_max > +20 mV` and exits 0.
* NetPyNE sanity sim asserts `v_max > +20 mV` and exits 0.
* Compiled `nrnmech.dll` loads via `h.nrn_load_dll` with no error.

## Deviations from Plan

* REQ-1 "Silent install to `C:\Users\md1avn\nrn-8.2.7`": the `/S` flag plus `/D=` prefix was
  rejected by the NSIS installer, which defaulted to `C:\nrn-8.2.7`. The researcher completed the
  interactive GUI install manually to reach the desired prefix. The answer asset documents this as a
  known-good fallback.
* REQ-2 "Compile a bundled HH MOD": the plan originally assumed we would need to author a Hodgkin-
  Huxley MOD file from scratch. NEURON 8.2.7 ships a built-in `hh` mechanism in its standard
  library, so the sanity sims insert `"hh"` directly rather than referencing a project-local MOD.
  `khhchan.mod` is still compiled as a smoke test for `nrnivmodl` itself and because downstream
  retinal tasks need this custom mechanism available.

## Limitations

* Tested only on Windows 11 with Python 3.13. Linux / macOS compatibility is inherited from
  NetPyNE's upstream releases but was not verified here.
* The sanity sim exercises only the built-in `hh` mechanism. Custom MOD correctness (e.g., `khhchan`
  biophysics) is validated only by compilation success, not by a dedicated simulation.
* NetPyNE's `sim.analysis.plot*` helpers were not exercised. The pipeline saves raw voltage traces
  and builds plots via matplotlib directly, so any downstream use of NetPyNE's plotting API will
  need its own verification.
