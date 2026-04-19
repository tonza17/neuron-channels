---
spec_version: "2"
task_id: "t0007_install_neuron_netpyne"
date_completed: "2026-04-19"
status: "complete"
---
# Plan: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain

## Plan Revision Note

**2026-04-19** — First revision. Original plan selected WSL2 as the install host. Executing plan
step 1 revealed that WSL2 needs the Virtual Machine Platform Windows feature enabled, which in turn
needs elevated privileges and a reboot outside the agent's control. Rather than wait on that
intervention, the researcher redirected the plan to the NEURON Windows `.exe` binary installer
(Option B) wired into the project's uv venv via a `.pth` file. This revision replaces the Approach,
Step-by-Step, Risks & Fallbacks, and Assets Needed sections accordingly. Requirement IDs (REQ-1
through REQ-9) are unchanged.

## Objective

Install NEURON 8.2.7 + NetPyNE 1.1.1 into a reproducible virtualenv, compile a representative
Hodgkin-Huxley MOD file with `nrnivmodl`, run two 1-compartment sanity simulations (one via raw
NEURON, one via NetPyNE) that each fire at least one action potential crossing +20 mV under a 0.5 nA
step, and publish a single `neuron-netpyne-install-report` answer asset. "Done" means all five task
questions are answered with verbatim installer output, voltage-trace PNGs, and a clear "works" /
"does not work" verdict.

## Task Requirement Checklist

Operative task request (from `task.json` `short_description` plus
`long_description_file=task_description.md`):

```text
Install NEURON 8.2.7 + NetPyNE 1.1.1, compile bundled HH MOD files,
run a 1-compartment sanity simulation, and record versions, warnings,
and wall-clock as an answer asset.
```

Full long description scope quoted verbatim:

> 1. Install NEURON 8.2.7 and NetPyNE 1.1.1 into the project's `uv` virtualenv:
>    `uv pip install neuron==8.2.7 netpyne==1.1.1`.
> 2. Compile the bundled Hodgkin-Huxley MOD files with `nrnivmodl`. Record the compilation command,
>    wall-clock, and any warnings.
> 3. Run a 1-compartment sanity simulation:
>    * Create a single-section soma (L = 20 µm, diam = 20 µm) with `hh` inserted.
>    * Inject a 0.5 nA step current for 50 ms, record membrane voltage.
>    * Confirm at least one spike (V crosses +20 mV).
> 4. Repeat the same sanity simulation via NetPyNE's `specs.NetParams` + `sim.createSimulateAnalyze`
>    harness to prove NetPyNE wraps NEURON correctly.
> 5. Record the final installed versions (`neuron.__version__`, `netpyne.__version__`, the NEURON
>    `hoc` "about" string), the `nrnivmodl` output, the sanity-simulation wall-clocks, and any
>    installer warnings into a single answer asset named `neuron-netpyne-install-report`.

Checklist (with requirement IDs that step numbers in `## Step by Step` cross-reference):

* **REQ-1** — Install NEURON 8.2.7 and NetPyNE 1.1.1 reachable from the project's uv virtualenv.
  Evidence:
  `uv run python -c "import neuron, netpyne; print(neuron.__version__, netpyne.__version__)"` prints
  `8.2.7 1.1.1`. Covered by steps 2-4. *Note on deviation from literal task text:* NEURON publishes
  no Windows pip wheel on PyPI, so the exact command `uv pip install neuron==8.2.7` cannot succeed
  on native Windows. The requirement is met by installing NEURON via its official Windows `.exe`
  binary installer and exposing its Python package to the uv venv through a `.pth` file, then
  `uv pip install netpyne==1.1.1`. The substitution and its justification are recorded in
  `full_answer.md` as REQ-1's compliance note.
* **REQ-2** — Compile at least one Hodgkin-Huxley MOD file with `nrnivmodl` and capture command +
  wall-clock + warnings. Evidence: `files/mod/nrnmech.dll` exists and stdout/stderr are captured in
  `files/logs/nrnivmodl.log`. Covered by step 5. Ambiguity flagged: `hh` is built in to NEURON core
  and is not distributed as a user-compilable `.mod`. Requirement is re-scoped to "compile a
  representative MOD file from `<NEURONHOME>/share/examples/nrniv/nmodl/` (e.g., `khhchan.mod`) to
  prove the MinGW toolchain works end to end", and the deviation is documented in `full_answer.md`.
* **REQ-3** — Build a 1-compartment raw-NEURON sanity simulation: single soma, L = diam = 20 µm,
  `hh` mechanism inserted, 0.5 nA step for 50 ms, membrane-voltage trace recorded. Evidence:
  `files/csv/raw_neuron_trace.csv` + `files/images/raw_neuron_trace.png`. Covered by step 6.
* **REQ-4** — Confirm that simulation crosses +20 mV at least once. Evidence: Python check
  `max(v_trace) > 20.0` prints `PASS` and the log captures it. Covered by step 6.
* **REQ-5** — Repeat REQ-3/REQ-4 under NetPyNE's `specs.NetParams` + `sim.createSimulateAnalyze`
  harness. Evidence: `files/csv/netpyne_trace.csv` + `files/images/netpyne_trace.png`, max-voltage
  check passes. Covered by step 7.
* **REQ-6** — Record final installed versions (`neuron.__version__`, `netpyne.__version__`, NEURON
  `h.nrnversion(0)` string). Evidence: `files/json/versions.json`. Covered by step 4.
* **REQ-7** — Record `nrnivmodl` output verbatim, sanity-simulation wall-clocks, and every
  installer warning. Evidence: `files/logs/*.log`, wall-clocks in `files/json/timings.json`. Covered
  by steps 2, 5, 6, 7.
* **REQ-8** — Publish a single `neuron-netpyne-install-report` answer asset with `details.json`,
  `short_answer.md`, and `full_answer.md` per `meta/asset_types/answer/specification.md`. Evidence:
  `assets/answer/neuron-netpyne-install-report/` directory with those three files and the embedded
  PNG/CSV artifacts. Covered by step 8. Match `task.json` `expected_assets.answer = 1`.
* **REQ-9** — If any install step fails irrecoverably, the task files an intervention rather than
  silently skipping. Evidence: `intervention/<issue>.md`. Covered by the Risks & Fallbacks section.

## Approach

Use the **official NEURON Windows binary installer**
(`nrn-8.2.7.w64-mingw-py-37-38-39-310-311-setup.exe`) as the NEURON host, then wire its bundled
Python package into the project's uv venv through a `.pth` file in `site-packages/`. NetPyNE is pure
Python and installs into the uv venv with `uv pip install netpyne==1.1.1` directly. `nrnivmodl`
ships with the installer (via the bundled MinGW toolchain) and runs from `cmd.exe` or `bash` once
PATH is sanitised of Git's `sh.exe`. All project Python code (`code/*.py`) uses the uv venv's Python
— downstream tasks (t0008, t0010, t0011) simply `import neuron` and it resolves via the `.pth`
file.

This path keeps the project's single-virtualenv discipline: one uv venv, one Python, one PATH set
for every task. NEURON lives outside the venv physically but is resolvable from it logically. The
research-internet document already flagged this as the canonical Windows install path
[NEURON-InstallDocs-2026, NEURON-WinBuild-2026].

**Alternatives considered:**

* *WSL2 with Ubuntu (original plan)* — rejected for this revision: WSL2 requires the Virtual
  Machine Platform Windows feature, which in turn requires elevated PowerShell and a reboot. The
  non-elevated `wsl --install -d Ubuntu` run during plan step 1 downloaded the Ubuntu image but
  ended with `"The requested operation requires elevation"` (see command log
  `003_20260419T211340Z_wsl-install-d.*`). The researcher redirected the plan to the `.exe`
  installer rather than wait on the elevation + BIOS-virtualisation + reboot intervention.
* *`conda install -c conda-forge neuron`* — rejected: requires a conda environment alongside the
  uv venv, breaks single-toolchain discipline for every downstream task.
* *Switch simulator to Brian2 or Arbor* — rejected: t0003 selected NEURON+NetPyNE specifically for
  DSGC biophysical accuracy and published-model coverage. Switching invalidates t0003's answer asset
  and the t0008 ModelDB 189347 port.
* *Build NEURON from source* — rejected: overkill for an infrastructure-setup task, multi-hour
  MSVC
  + CMake setup, and would still need PYTHONPATH wiring identical to the `.exe` path.

**Task types**: `infrastructure-setup`, as declared in `task.json`. Planning guidelines for
infrastructure-setup stress reproducibility (record exact versions, wall-clocks, environment
details) and idempotence (each install step safely re-runnable) — both are built into the step
list below.

## Cost Estimation

**$0.** No paid APIs, no remote compute, no paid services. Project budget is $0. NEURON `.exe`
installer (~60 MB) and NetPyNE pip wheel (~5 MB plus dependencies ~150 MB total) are free and
bandwidth-only.

## Step by Step

1. **Download the NEURON 8.2.7 Windows installer.** Use `curl.exe` wrapped in `run_with_logs.py` to
   fetch
   `https://github.com/neuronsimulator/nrn/releases/download/8.2.7/nrn-8.2.7.w64-mingw-py-37-38-39-310-311-setup.exe`
   to `files/installer/nrn-8.2.7-setup.exe`. If the GitHub asset URL 404s, fall back to
   `https://www.neuron.yale.edu/ftp/neuron/versions/v8.2.7/`. Verify the file exists and is >= 40
   MB. Satisfies REQ-1 prerequisite.

2. **Install NEURON silently to a user-owned directory.** Run the installer with InnoSetup silent
   flags pointing at a per-user install directory so no admin prompt is required:
   `files/installer/nrn-8.2.7-setup.exe /VERYSILENT /NORESTART /SUPPRESSMSGBOXES /DIR="C:\Users\md1avn\nrn-8.2.7"`.
   Wrap in `run_with_logs.py`. Capture exit code and wall-clock to `files/logs/nrn_install.log`.
   Verify `C:\Users\md1avn\nrn-8.2.7\bin\nrniv.exe` and
   `C:\Users\md1avn\nrn-8.2.7\lib\python\neuron\` exist after install. **Fallback:** if silent mode
   is not honoured (unexpected non-zero exit and no install tree), file
   `intervention/neuron_installer_needs_interactive.md` asking the user to double-click the `.exe`
   and walk through the wizard, targeting the same install directory. Do not proceed until the
   install tree is present. Satisfies REQ-1, REQ-7.

3. **Wire NEURON into the uv venv.** Write a `.pth` file at `.venv/Lib/site-packages/neuron.pth`
   containing the single line `C:\Users\md1avn\nrn-8.2.7\lib\python`. Python auto-processes `.pth`
   files on startup, so `uv run python -c "import neuron"` will then resolve to the installer's
   neuron package with no environment-variable wrangling. Also `uv pip install netpyne==1.1.1` into
   the uv venv (NetPyNE is pure Python, has no NEURON version pin). Capture pip install
   stdout/stderr into `files/logs/pip_install_netpyne.log`. Satisfies REQ-1.

4. **Probe installed versions.** Execute
   `uv run python -c "import neuron, netpyne, json; print(json.dumps({'neuron': neuron.__version__, 'netpyne': netpyne.__version__, 'hoc': neuron.h.nrnversion(0)}))"`.
   Parse stdout, write `files/json/versions.json`. Expected keys `neuron` (=`8.2.7`), `netpyne`
   (=`1.1.1`), `hoc` (non-empty NEURON build string). Satisfies REQ-6.

5. **Compile a representative HH-family MOD file with `nrnivmodl`.** Locate `khhchan.mod` (or
   another simple channel MOD) under `C:\Users\md1avn\nrn-8.2.7\share\examples\nrniv\nmodl\`. Copy
   it to `files/mod/khhchan.mod`. Build a sanitised PATH that puts NEURON's MinGW `sh.exe` ahead of
   Git's — concretely:
   `PATH=C:\Users\md1avn\nrn-8.2.7\bin;C:\Users\md1avn\nrn-8.2.7\mingw\bin;<system32 entries>` with
   `C:\Program Files\Git\bin` and `C:\Program Files\Git\usr\bin` explicitly removed. Run `nrnivmodl`
   from inside `files/mod/` via `run_with_logs.py` with that sanitised PATH passed in `env`. Capture
   stdout/stderr into `files/logs/nrnivmodl.log` and wall-clock into `files/json/timings.json`.
   Expected: `nrnmech.dll` produced in `files/mod/` or an architecture subdirectory, no error
   output. Satisfies REQ-2, REQ-7. The `hh`-is-built-in deviation is noted in `full_answer.md`.

6. **Raw-NEURON 1-compartment sanity simulation.** Write `code/sanity_raw_neuron.py` and
   `code/paths.py` (following the t0004 pattern with typed `Path` constants for `FILES_DIR`,
   `LOGS_DIR`, `CSV_DIR`, `JSON_DIR`, `IMAGES_DIR`, `MOD_DIR`, `INSTALLER_DIR`). The simulation
   script builds a single-section soma
   (`soma = h.Section(); soma.L = soma.diam = 20.0; soma.insert('hh')`), adds
   `IClamp(amp=0.5, delay=5.0, dur=50.0)`, records `v` and `t` vectors, runs 70 ms with `dt = 0.025`
   and `h.celsius = 6.3`. Save trace to `files/csv/raw_neuron_trace.csv`. Produce
   `files/images/raw_neuron_trace.png` using `matplotlib.use("Agg")` so no display is required.
   Compute `max(v)` and assert `max(v) > 20.0`. Record wall-clock into `files/json/timings.json`.
   Execute via `uv run python code/sanity_raw_neuron.py`. Capture stdout/stderr to
   `files/logs/raw_neuron_run.log`. Satisfies REQ-3, REQ-4, REQ-7.

7. **NetPyNE 1-compartment sanity simulation.** Write `code/sanity_netpyne.py`. Use
   `netpyne.specs.NetParams`: declare a single `popParams` with one cell, one `cellParams` defining
   the same soma with `hh`, one `stimSourceParams` IClamp at 0.5 nA for 50 ms, one
   `stimTargetParams` pointing the clamp at the soma. Use `simConfig.recordTraces` to record
   membrane voltage at `soma(0.5)`. Run `sim.createSimulateAnalyze(netParams, simConfig)`. Extract
   the voltage trace from `sim.allSimData['V_soma']['cell_0']`. Save to
   `files/csv/netpyne_trace.csv`, PNG to `files/images/netpyne_trace.png`. Assert `max(v) > 20.0`.
   Wall-clock to timings.json. Execute via `uv run python code/sanity_netpyne.py`. Satisfies REQ-3,
   REQ-4, REQ-5, REQ-7.

8. [CRITICAL] **Publish the `neuron-netpyne-install-report` answer asset.** Create
   `assets/answer/neuron-netpyne-install-report/` with (a) `details.json` conforming to
   `meta/asset_types/answer/specification.md` v2 (question, short_title, categories including
   `["simulator-tooling", "reproduction"]` if present in `meta/categories/`, answer_methods
   `["code-experiment"]`, confidence `high`, created_by_task, date_created), (b) `short_answer.md`
   (3-5 sentences: versions + "works" / "does not work" verdict), (c) `full_answer.md` (8 mandatory
   sections per the answer spec, embedding the two PNG traces, the versions.json contents,
   timings.json, a table of installer warnings verbatim, the HH-built-in deviation note from step 5,
   and the native-Windows-install deviation note from REQ-1). Validate with
   `uv run python -u -m arf.scripts.verificators.verify_answer t0007_install_neuron_netpyne neuron-netpyne-install-report`.
   Satisfies REQ-8.

## Remote Machines

None required. All work runs locally on the researcher's Windows 11 workstation.

## Assets Needed

* **NEURON 8.2.7 Windows binary installer** — downloaded on demand in step 1 from the GitHub
  release (fallback: neuron.yale.edu FTP).
* **NetPyNE 1.1.1 wheel** — from PyPI, installed into the uv venv.
* **A HH-family MOD source file** — copied from NEURON's `share/examples/nrniv/nmodl/` after
  install.

No prior task assets are required.

## Expected Assets

* **1 answer asset** `assets/answer/neuron-netpyne-install-report/` containing `details.json`
  (spec_version "2", question stating "does the NEURON 8.2.7 + NetPyNE 1.1.1 toolchain install and
  run a 1-compartment sanity simulation on this workstation?"), `short_answer.md` (3-5 sentences
  with verdict), and `full_answer.md` (full install log, sanity-simulation code links, embedded
  voltage-trace PNGs, versions, timings table, installer-warnings table, HH-built-in deviation note,
  native-Windows-install deviation note).

Matches `task.json` `expected_assets.answer = 1`.

## Time Estimation

* Installer download (step 1): ~30 s on broadband.
* Silent install (step 2): 1-2 min.
* `.pth` wiring + `uv pip install netpyne==1.1.1` (step 3): 1-2 min.
* Versions probe (step 4): <1 min.
* `nrnivmodl` compile (step 5): <30 s.
* Raw NEURON sanity sim (step 6): <1 min including plot rendering.
* NetPyNE sanity sim (step 7): <1 min.
* Answer asset write + verificator (step 8): 2-3 min.
* **Total agent wall-clock**: 10-12 min assuming no silent-install fallback.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| NEURON `.exe` ignores `/VERYSILENT` and requires interactive click-through | Medium | Blocker — cannot install programmatically | File `intervention/neuron_installer_needs_interactive.md` with instructions for the user to run the installer manually into `C:\Users\md1avn\nrn-8.2.7`, then resume the task. Detection: non-zero exit or missing install tree after step 2. |
| GitHub release URL for the installer has changed | Low | Step 1 download fails | Fall back to `https://www.neuron.yale.edu/ftp/neuron/versions/v8.2.7/`; if both 404, file `intervention/installer_url_not_found.md`. |
| Installer Python-version suffix requires admin to register DLLs | Medium | Silent install appears to succeed but `import neuron` fails later | Prefer the `/DIR` flag to install under the user profile (no registry or C:\Program Files writes). If `import neuron` still fails in step 4, file `intervention/neuron_import_fails.md` with the failure traceback. |
| Git for Windows `sh.exe` on PATH breaks `nrnivmodl` | High | `nrnivmodl` fails with "sh.exe was found in your PATH" | Step 5 explicitly builds a sanitised PATH without `C:\Program Files\Git\bin` and `C:\Program Files\Git\usr\bin` before invoking `nrnivmodl`. Detection: `nrnivmodl.log` contains the string `sh.exe`. |
| NEURON's Python package incompatible with uv venv's Python version | Medium | `import neuron` raises `ImportError: DLL load failed` | uv venv Python is 3.11 (project-wide setting); installer covers 3.7-3.11 so the pairing should work. If it fails, file `intervention/python_version_mismatch.md` suggesting either pinning the uv venv to 3.11 or using a newer NEURON installer. |
| NetPyNE 1.1.1 tightens a NEURON pin on install (new release) | Low | NEURON downgrade or conflict | Detect in pip output; record substitution in answer asset per task description's explicit fallback. |
| `matplotlib` backend issue on headless Windows | Very Low | PNG generation fails | Force `matplotlib.use("Agg")` at top of sanity scripts before any pyplot import. |
| `.pth` file not honoured (non-standard uv venv layout) | Low | `import neuron` fails | Fallback: set `PYTHONPATH=C:\Users\md1avn\nrn-8.2.7\lib\python` in each `uv run` invocation for the remaining task steps. |

Pre-mortem: the most likely failure is the `nrnivmodl` Git `sh.exe` conflict during step 5. The PATH
sanitisation has been pre-engineered into the plan specifically to avoid it. Second most likely is
the silent-install falling back to interactive, which is a user-unblock flow (not a permanent
blocker).

## Verification Criteria

* `files/logs/nrn_install.log` reports exit code 0 AND `C:\Users\md1avn\nrn-8.2.7\bin\nrniv.exe`
  exists after step 2.
* `files/logs/pip_install_netpyne.log` ends with `Successfully installed netpyne-1.1.1 ...`.
* `files/json/versions.json` contains keys `neuron` (=`8.2.7`), `netpyne` (=`1.1.1`), `hoc`
  (non-empty).
* `files/mod/nrnmech.dll` (or `files/mod/x86_64/libnrnmech.so`-equivalent) exists after step 5 and
  `files/logs/nrnivmodl.log` contains neither `sh.exe was found` nor compilation errors.
* `files/csv/raw_neuron_trace.csv` and `files/csv/netpyne_trace.csv` each have at least one row
  where `v >= 20.0`.
* `files/images/raw_neuron_trace.png` and `files/images/netpyne_trace.png` exist and render a
  voltage spike visually.
* `uv run python -u -m arf.scripts.verificators.verify_answer t0007_install_neuron_netpyne neuron-netpyne-install-report`
  passes.
* `uv run python -u -m arf.scripts.verificators.verify_task_structure t0007_install_neuron_netpyne`
  passes.
