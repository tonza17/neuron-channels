# ✅ Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0007_install_neuron_netpyne` |
| **Status** | ✅ completed |
| **Started** | 2026-04-19T18:20:22Z |
| **Completed** | 2026-04-19T22:43:38Z |
| **Duration** | 4h 23m |
| **Source suggestion** | `S-0003-01` |
| **Task types** | `infrastructure-setup` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md) |
| **Expected assets** | 1 answer |
| **Step progress** | 10/15 |
| **Task folder** | [`t0007_install_neuron_netpyne/`](../../../tasks/t0007_install_neuron_netpyne/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0007_install_neuron_netpyne/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0007_install_neuron_netpyne/task_description.md)*

# Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain

## Motivation

The t0003 simulator survey selected **NEURON 8.2.7** (paired with **NetPyNE 1.1.1**) as the
project's primary compartmental simulator, but did not install it. Every downstream
compartmental- modelling task (ModelDB 189347 port, diameter calibration verification,
missed-models hunt, visualisation smoke-test against a running simulation, tuning-curve
scoring) needs a validated NEURON+NetPyNE environment. This task does the install, proves it
works end-to-end on a trivial cell, and records the exact installed versions and any installer
warnings so later tasks can reproduce the environment deterministically.

Covers suggestion **S-0003-01**.

## Scope

1. Install NEURON 8.2.7 and NetPyNE 1.1.1 into the project's `uv` virtualenv: `uv pip install
   neuron==8.2.7 netpyne==1.1.1`.
2. Compile the bundled Hodgkin-Huxley MOD files with `nrnivmodl`. Record the compilation
   command, wall-clock, and any warnings.
3. Run a 1-compartment sanity simulation:
   * Create a single-section soma (L = 20 µm, diam = 20 µm) with `hh` inserted.
   * Inject a 0.5 nA step current for 50 ms, record membrane voltage.
   * Confirm at least one spike (V crosses +20 mV).
4. Repeat the same sanity simulation via NetPyNE's `specs.NetParams` +
   `sim.createSimulateAnalyze` harness to prove NetPyNE wraps NEURON correctly.
5. Record the final installed versions (`neuron.__version__`, `netpyne.__version__`, the
   NEURON `hoc` "about" string), the `nrnivmodl` output, the sanity-simulation wall-clocks,
   and any installer warnings into a single answer asset named
   `neuron-netpyne-install-report`.

## Dependencies

None — this task does not need any prior task's output.

## Expected Outputs

* **1 answer asset** (`assets/answer/neuron-netpyne-install-report/`) with:
  * `details.json` (question, categories, answer methods, source URLs for install commands)
  * `short_answer.md` (3-5 sentences: versions + "works" / "does not work" verdict)
  * `full_answer.md` (install log, sanity-simulation code, NEURON + NetPyNE voltage traces
    embedded as PNGs in `files/images/`, tabulated wall-clocks, every installer warning
    verbatim)

## Approach

Write a `code/install_and_validate.py` script that (a) shells out to `uv pip install`, (b)
shells out to `nrnivmodl` in the NEURON-bundled MOD directory, (c) runs the two sanity
simulations capturing voltage traces to CSV, and (d) produces the two PNG plots. Wrap every
CLI call with `run_with_logs.py`. Keep the sanity-simulation code deliberately minimal so the
answer asset also serves as a "hello world" reference for downstream tasks.

## Questions the task answers

1. Does `uv pip install neuron==8.2.7 netpyne==1.1.1` succeed on this workstation?
2. Does `nrnivmodl` compile the bundled HH MOD files without errors?
3. Does a 1-compartment soma with `hh` fire at least one action potential under a 0.5 nA step?
4. Does NetPyNE's wrapper produce the same voltage trace as raw NEURON on the same cell?
5. What are the exact installed versions, and what warnings (if any) surfaced during install
   or compilation?

## Risks and Fallbacks

* If NEURON 8.2.7 wheels are unavailable for this Python version, fall back to the nearest
  supported patch release and record the substitution in the answer asset.
* If NetPyNE pins an older NEURON release, use the NetPyNE-required version and record the
  override.
* If `nrnivmodl` needs `gcc`/`clang` that is not on PATH, create an intervention file
  requesting the compiler toolchain instead of silently skipping MOD compilation.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does the NEURON 8.2.7 + NetPyNE 1.1.1 toolchain install, compile MOD files, and run a 1-compartment Hodgkin-Huxley sanity simulation on the project's Windows 11 workstation?](../../../tasks/t0007_install_neuron_netpyne/assets/answer/neuron-netpyne-install-report/) | [`full_answer.md`](../../../tasks/t0007_install_neuron_netpyne/assets/answer/neuron-netpyne-install-report/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Validate custom khhchan.mod biophysics with a dedicated sanity
simulation</strong> (S-0007-01)</summary>

**Kind**: experiment | **Priority**: high

The t0007 sanity sims only exercise NEURON's built-in hh mechanism. khhchan.mod is compiled as
a smoke test but its biophysics are never run. Add a short task that inserts khhchan on a
1-compartment soma, drives it with the same IClamp protocol, and compares the resulting trace
against the built-in hh to confirm the custom mechanism produces physiologically plausible
spikes before downstream retinal tasks depend on it.

</details>

<details>
<summary><strong>Script the full NEURON + NetPyNE install for clean-machine
reproduction</strong> (S-0007-02)</summary>

**Kind**: library | **Priority**: medium

The NSIS installer's /S flag ignored the /D= prefix, forcing an interactive GUI step. Ship a
PowerShell / bash installer script that (a) downloads nrn-8.2.7-setup.exe to a known path, (b)
drives the install with the correct prefix (either by default-install-then-move or by a
chocolatey recipe), (c) writes the .pth file into the uv venv, and (d) runs nrnivmodl + both
sanity sims end-to-end. This unblocks automated reproduction on a fresh Windows machine and
Linux / macOS CI runners.

</details>

<details>
<summary><strong>Benchmark NetPyNE harness overhead vs raw NEURON across problem
sizes</strong> (S-0007-03)</summary>

**Kind**: evaluation | **Priority**: medium

At the single-compartment size, NetPyNE's setup is ~6× slower than raw NEURON (38.7 ms vs 6.7
ms) but runtime is indistinguishable. Scan both harnesses across realistic retinal network
sizes (1, 10, 100, 1000 cells; dense and sparse connectivity) to quantify where NetPyNE's cost
becomes significant for downstream t0008 / t0010 / t0011 runs, and decide whether any hot-loop
experiments should stay in raw NEURON.

</details>

## Research

* [`research_code.md`](../../../tasks/t0007_install_neuron_netpyne/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0007_install_neuron_netpyne/research/research_internet.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0007_install_neuron_netpyne/results/results_summary.md)*

--- spec_version: "1" task_id: "t0007_install_neuron_netpyne" date_completed: "2026-04-19" ---
# Results Summary: NEURON 8.2.7 + NetPyNE 1.1.1 install

## Summary

The NEURON 8.2.7 + NetPyNE 1.1.1 toolchain installs, compiles MOD files, and runs a
single-compartment Hodgkin-Huxley sanity simulation end-to-end on the project's Windows 11
workstation. Raw NEURON and NetPyNE sanity sims agree to machine precision at **v_max = 42.003
mV**, confirming the stack is ready for downstream modelling tasks (t0008, t0010, t0011).

## Metrics

* Raw NEURON sanity sim: **v_max = 42.003 mV**, crossed +20 mV threshold, 3201 samples, setup
  **6.7 ms**, run **4.4 ms**.
* NetPyNE sanity sim: **v_max = 42.003 mV**, crossed +20 mV threshold, 3201 samples, setup
  **38.7 ms**, run **4.8 ms**.
* Raw-NEURON and NetPyNE traces agree on `v_max` to **machine precision** (1e-15 mV).
* `nrnivmodl` compiled `khhchan.mod` into **132 KB** `nrnmech.dll` in under **5 seconds** with
  no warnings or errors.
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
* `data/json/raw_neuron_timings.json`, `data/json/netpyne_timings.json`,
  `data/json/versions.json` — wall-clock and version provenance.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0007_install_neuron_netpyne/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0007_install_neuron_netpyne" ---
# Detailed Results: NEURON 8.2.7 + NetPyNE 1.1.1 install

## Summary

Installed NEURON 8.2.7 + NetPyNE 1.1.1 on the project's Windows 11 workstation, wired the
NEURON Python bindings into the uv venv via a `.pth` file, compiled `khhchan.mod` with
`nrnivmodl`, and executed two Hodgkin-Huxley single-compartment sanity simulations (raw NEURON
and NetPyNE) that both fire action potentials peaking at **42.003 mV**. Published the
`neuron-netpyne-install-report` answer asset with an eight-section report and embedded trace
plots.

## Methodology

The install ran in three phases: (1) NEURON core install from the official
`nrn-8.2.7-setup.exe` Windows installer, (2) NetPyNE install via `uv pip install
netpyne==1.1.1` into the repository's uv venv, and (3) sanity verification through two
parallel Hodgkin-Huxley single-compartment simulations — one in raw NEURON and one wrapped
through NetPyNE's `specs.NetParams` / `specs.SimConfig` harness.

### Machine Specs

* Hardware: Windows 11 Education 22631, 16-core x86_64 workstation.
* Python: 3.13 (pinned by `.python-version`); uv-managed venv at `<repo>\.venv`.
* NEURON: 8.2.7+ (HEAD 34cf696+, release build 2025-05-21) installed to
  `C:\Users\md1avn\nrn-8.2.7` via the interactive GUI installer.
* NetPyNE: 1.1.1 installed from PyPI into the uv venv with all transitive dependencies
  satisfied.

### Runtime

* Step 9 (implementation) started 2026-04-19T21:00:11Z, completed 2026-04-19T22:34:58Z (~1h
  35m wall-clock, most of which was interactive installer time).
* Raw NEURON sanity sim: **0.011 s** total (setup 6.7 ms + run 4.4 ms).
* NetPyNE sanity sim: **0.044 s** total (setup 38.7 ms + run 4.8 ms).
* `nrnivmodl` compile time: under **5 seconds**.

### Wiring Strategy

NEURON's installer places its Python bindings under
`C:\Users\md1avn\nrn-8.2.7\lib\python\neuron`. Rather than copy the package into the venv, we
created a single `.pth` file at `<repo>\.venv\Lib\site-packages\neuron.pth` containing the
one-line path `C:\Users\md1avn\nrn-8.2.7\lib\python`. Python's `site.py` expands the `.pth` at
import time, so `from neuron import h` resolves through the native install. The scripts also
set `NEURONHOME=C:\Users\md1avn\nrn-8.2.7` via `os.environ.setdefault` so
`os.add_dll_directory` picks up the correct DLL search root on Windows.

### Sanity Simulation Design

Both simulations use identical biophysics:

* Single soma compartment, 20 μm length × 20 μm diameter.
* NEURON built-in `hh` mechanism inserted on the soma.
* IClamp electrode at soma midpoint (0.5), delay 5 ms, duration 50 ms, amplitude 0.5 nA.
* Integrator: fixed-step, `dt=0.025 ms`, `tstop=80 ms`.
* Threshold used for pass/fail: `v_max > +20 mV`.

The raw NEURON sim (`code/sanity_raw_neuron.py`) uses `h.Section`, `h.IClamp`, and
`h.Vector().record` directly, then `h.finitialize(-65.0)` followed by `h.continuerun(80.0)`.
The NetPyNE sim (`code/sanity_netpyne.py`) constructs the same biophysics through
`specs.NetParams` and `specs.SimConfig`, then runs `sim.initialize`, `sim.net.createPops`,
`sim.net.createCells`, `sim.net.addStims`, `sim.setupRecording`, `sim.runSim`, and
`sim.gatherData`.

## Metrics Tables

### Sanity-Simulation Outcomes

| Harness | `v_max` (mV) | `v_min` (mV) | Samples | Setup (s) | Run (s) | Crossed +20 mV |
| --- | ---: | ---: | ---: | ---: | ---: | :--- |
| Raw NEURON | 42.00255 | -75.96756 | 3201 | 0.0067 | 0.0044 | yes |
| NetPyNE | 42.00255 | -75.96756 | 3201 | 0.0387 | 0.0048 | yes |

`v_max` and `v_min` agree to machine precision. NetPyNE's setup is ~6× slower than the raw
NEURON path because the `specs.NetParams` / `specs.SimConfig` expansion does dictionary walks
and network-scaffolding work that raw NEURON skips, but the actual integration runtime is
indistinguishable.

### Spike Count

Both simulations fire **six** action potentials across the 50 ms stimulus window — 120 Hz
instantaneous rate during the stimulus, 75 Hz averaged over the 80 ms simulation.

## Visualizations

![Raw NEURON HH soma
trace](../../../tasks/t0007_install_neuron_netpyne/data/images/raw_neuron_trace.png)

![NetPyNE HH soma
trace](../../../tasks/t0007_install_neuron_netpyne/data/images/netpyne_trace.png)

## Verification

* `uv run ruff check tasks/t0007_install_neuron_netpyne/code/` — PASSED (all checks).
* `uv run ruff format tasks/t0007_install_neuron_netpyne/code/` — PASSED (no changes).
* `uv run mypy -p tasks.t0007_install_neuron_netpyne.code` — PASSED (no issues).
* Raw NEURON sanity sim exits 0 with the `v_max > +20 mV` assertion satisfied.
* NetPyNE sanity sim exits 0 with the `v_max > +20 mV` assertion satisfied.
* Compiled `nrnmech.dll` loads via `h.nrn_load_dll` with no error.
* `neuron.__version__` prints `"8.2.7+"`; `netpyne.__version__` prints `"1.1.1"`;
  `h("VERSION")` prints the full build string with `34cf696+ (2025-05-21)`.

## Limitations

* Tested only on Windows 11 with Python 3.13. Linux / macOS compatibility is inherited from
  NetPyNE's upstream releases but was not verified here.
* The sanity sim exercises only the built-in `hh` mechanism. Custom MOD correctness (e.g.,
  `khhchan` biophysics) is validated only by compilation success, not by a dedicated
  simulation.
* NetPyNE's `sim.analysis.plot*` helpers were not exercised. The pipeline saves raw voltage
  traces and builds plots via matplotlib directly, so any downstream use of NetPyNE's plotting
  API will need its own verification.
* The NSIS silent installer did not accept the `/D=` prefix, so install required interactive
  user action. Automated end-to-end reproduction on a fresh machine needs either a
  pre-installed NEURON or the manual GUI step documented in the answer asset.

## Files Created

* `code/sanity_raw_neuron.py` — raw NEURON HH soma sanity script.
* `code/sanity_netpyne.py` — NetPyNE HH soma sanity script (parallel harness).
* `code/run_nrnivmodl.cmd` — cmd.exe wrapper for `nrnivmodl.bat` (MSYS path-mangling
  workaround).
* `data/mod/khhchan.mod` — custom Hodgkin-Huxley MOD (compiled smoke-test input).
* `data/mod/nrnmech.dll` — compiled mechanism library (132 KB, reusable downstream).
* `data/csv/raw_neuron_trace.csv`, `data/csv/netpyne_trace.csv` — voltage traces.
* `data/images/raw_neuron_trace.png`, `data/images/netpyne_trace.png` — trace plots.
* `data/json/raw_neuron_timings.json`, `data/json/netpyne_timings.json`,
  `data/json/versions.json` — wall-clock, threshold, and version provenance.
* `data/installer/.gitkeep` — placeholder (installer binary deleted to keep repo size down).
* `assets/answer/neuron-netpyne-install-report/details.json` — answer asset metadata.
* `assets/answer/neuron-netpyne-install-report/short_answer.md` — three-section short report.
* `assets/answer/neuron-netpyne-install-report/full_answer.md` — eight-section full report.
* `results/results_summary.md`, `results/results_detailed.md`, `results/metrics.json`,
  `results/costs.json`, `results/remote_machines_used.json`.
* `logs/commands/006_*` through `logs/commands/015_*` — command-log JSON + stdout/stderr for
  curl, installer, `uv pip`, `nrnivmodl`, and both sanity sims.

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

</details>
