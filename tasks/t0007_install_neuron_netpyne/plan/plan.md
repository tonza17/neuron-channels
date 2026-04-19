---
spec_version: "2"
task_id: "t0007_install_neuron_netpyne"
date_completed: "2026-04-19"
status: "complete"
---
# Plan: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain

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

* **REQ-1** — Install NEURON 8.2.7 and NetPyNE 1.1.1 into a project-controlled virtualenv.
  Evidence: `pip show neuron` reports `Version: 8.2.7` and `pip show netpyne` reports
  `Version: 1.1.1`. Covered by steps 3-4.
* **REQ-2** — Compile at least one Hodgkin-Huxley MOD file with `nrnivmodl` and capture command +
  wall-clock + warnings. Evidence: `files/mod/x86_64/libnrnmech.so` (or equivalent platform binary)
  exists and stdout/stderr captured in `files/logs/nrnivmodl_*.log`. Covered by step 5. Ambiguity
  flagged: the task says "the bundled HH MOD files", but the `hh` mechanism is built in to the
  NEURON core and is not distributed as a user-compilable `.mod` — so this requirement is
  re-scoped as "compile a representative MOD file from `share/examples/nrniv/nmodl/` (e.g.,
  `khhchan.mod`) to prove the toolchain works end to end", and the deviation is documented in
  `full_answer.md`.
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
  by steps 3, 5, 6, 7.
* **REQ-8** — Publish a single `neuron-netpyne-install-report` answer asset with `details.json`,
  `short_answer.md`, and `full_answer.md` per `meta/asset_types/answer/specification.md`. Evidence:
  `assets/answer/neuron-netpyne-install-report/` directory with those three files and the embedded
  PNG/CSV artifacts. Covered by step 8. Match `task.json` `expected_assets.answer = 1`.
* **REQ-9** — If `nrnivmodl` or any install step fails irrecoverably, the task files an
  intervention rather than silently skipping. Evidence: `intervention/<issue>.md`. Covered by the
  Risks & Fallbacks section.

## Approach

Use **WSL2 with Ubuntu** as the install host. Research-internet confirmed NEURON ships no Windows
pip wheels at any version, so the task's instruction `uv pip install neuron==8.2.7` will fail on
native Windows 11. Linux wheels exist for CPython 3.9-3.11; NetPyNE 1.1.1 has no NEURON version pin,
so the pairing is safe. Inside WSL, `nrnivmodl` uses the system `gcc` that ships with Ubuntu and
compiles MOD files in seconds. The WSL host keeps the project's single-virtualenv discipline (uv
venv inside WSL) that every downstream compartmental-modelling task (t0008, t0010, t0011) inherits,
and avoids the Windows `.exe` installer's split-Python footprint.

All compartmental modelling artifacts live inside the Windows worktree (git source of truth) and are
accessed from WSL via the `/mnt/c/...` path. Python scripts are written and committed on the Windows
side; `run_with_logs.py` wraps the WSL shell invocations using `wsl -e bash -lc "<command>"` so
every NEURON command still produces ARF-standard command logs.

**Alternatives considered:**

* *Windows `.exe` installer* — rejected: installs NEURON into an isolated Python bundled with
  MinGW, which is not the project's uv venv. NetPyNE would need a parallel install. Every later task
  that imports NEURON would have to know about this separate Python, breaking single-venv
  discipline.
* *Switch simulator to Brian2 or Arbor* — rejected: t0003 explicitly selected NEURON+NetPyNE for
  its biophysical-accuracy and published-DSGC-model coverage. Switching would invalidate the t0003
  answer asset and the t0008 ModelDB 189347 port.
* *Skip install and mark the task permanently_failed* — rejected: WSL2 is available on Windows 11
  by default (requires `wsl --install` one-time), reboot included; this is a per-workstation setup
  cost paid once, not an architectural blocker.

**Task types**: `infrastructure-setup`, as declared in `task.json`. Planning guidelines for
infrastructure-setup stress reproducibility (record exact versions, wall-clocks, environment
details) and idempotence (each install step safely re-runnable) — both are built into the step
list below.

## Cost Estimation

**$0.** No paid APIs, no remote compute, no paid services. Project budget is $0 so any paid service
would fail the cost gate. WSL distribution download (Ubuntu-22.04, ~450 MB) and pip wheels (~150 MB
total for neuron + netpyne + deps) are both free and bandwidth-only.

## Step by Step

1. **Verify WSL2 is available.** Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0007_install_neuron_netpyne -- wsl --status`.
   Expected: WSL status output describing a default distribution. If WSL is not installed (exit code
   != 0 and output looks like a `wsl.exe` help banner), write `intervention/wsl_not_installed.md`
   describing the exact commands the user must run (`wsl --install -d Ubuntu-22.04`, reboot,
   first-run Ubuntu UNIX user setup), stop task execution, and update `task.json` status to
   `intervention_blocked`. Do not proceed. Satisfies REQ-1 prerequisite.

2. **Detect Ubuntu distribution + capture environment.** Run
   `wsl -e bash -lc "lsb_release -a && which gcc && gcc --version && which python3 && python3 --version"`
   via `run_with_logs.py`. Capture to `files/logs/wsl_env.log`. Expected: Ubuntu version >= 20.04,
   `gcc` 9+, Python 3.10 or 3.11 available. If Python >= 3.12, install `python3.11` via
   `apt-get install -y python3.11 python3.11-venv` (NEURON 8.2.7 has no cp312 wheel). Satisfies
   REQ-1 prerequisite.

3. **Install NEURON 8.2.7 + NetPyNE 1.1.1 in WSL.** Write `code/install_and_validate.py` (the
   orchestration script) and `code/paths.py` (following the t0004 pattern with typed `Path`
   constants for `FILES_DIR`, `LOGS_DIR`, `CSV_DIR`, `JSON_DIR`, `IMAGES_DIR`, `MOD_DIR`). The
   install-phase portion of the script shells out to
   `wsl -e bash -lc "python3 -m venv /mnt/c/Users/md1avn/Documents/GitHub/neuron-channels-worktrees/t0007_install_neuron_netpyne/.wsl_venv && source /.../.wsl_venv/bin/activate && pip install neuron==8.2.7 netpyne==1.1.1"`.
   Capture stdout/stderr verbatim to `files/logs/pip_install.log`. Record wall-clock. Expected: pip
   install succeeds, reports installed versions. Satisfies REQ-1 and REQ-7 (installer warnings).

4. **Probe installed versions.** In the WSL venv, run a small Python one-liner:
   `python3 -c "import neuron, netpyne, json; print(json.dumps({'neuron': neuron.__version__, 'netpyne': netpyne.__version__, 'hoc': neuron.h.nrnversion(0)}))"`.
   Parse stdout, write `files/json/versions.json`. Expected keys `neuron`, `netpyne`, `hoc`.
   Satisfies REQ-6.

5. **Compile a representative HH-family MOD file with `nrnivmodl`.** Locate a HH-family MOD in the
   NEURON package's `share/examples/nrniv/nmodl/` directory (e.g., `khhchan.mod`). Copy it to
   `files/mod/khhchan.mod`. Run `wsl -e bash -lc "cd /mnt/c/.../files/mod && nrnivmodl"` capturing
   stdout/stderr into `files/logs/nrnivmodl.log` and the wall-clock into `files/json/timings.json`.
   Expected: `x86_64/` subdirectory created containing `libnrnmech.so`, `special` binary, and object
   files. Satisfies REQ-2, REQ-7. The deviation from the literal task text ("bundled HH MOD files"
   — `hh` is actually a built-in) is documented in `full_answer.md`.

6. **Raw-NEURON 1-compartment sanity simulation.** Write `code/sanity_raw_neuron.py`. Build a
   single-section soma: `soma = h.Section(); soma.L = soma.diam = 20.0; soma.insert('hh')`. Add
   `IClamp(amp=0.5, delay=5.0, dur=50.0)`, record `v` and `t` vectors, run 70 ms with dt=0.025 and
   `h.celsius=6.3`. Save trace to `files/csv/raw_neuron_trace.csv`. Produce
   `files/images/raw_neuron_trace.png` using `matplotlib.use("Agg")` (no display in WSL). Compute
   `max(v)` and assert `max(v) > 20.0`. Record wall-clock into timings.json. Execute via
   `wsl -e bash -lc "/.../.wsl_venv/bin/python /mnt/c/.../code/sanity_raw_neuron.py"`. Capture
   stdout/stderr to `files/logs/raw_neuron_run.log`. Satisfies REQ-3, REQ-4, REQ-7.

7. **NetPyNE 1-compartment sanity simulation.** Write `code/sanity_netpyne.py`. Use
   `netpyne.specs.NetParams`: declare a single `popParams` with one cell, one `cellParams` defining
   the same soma with `hh`, one `stimSourceParams` IClamp at 0.5 nA for 50 ms, one
   `stimTargetParams` pointing the clamp at the soma. Use `simConfig.recordTraces` to record
   membrane voltage. Run `sim.createSimulateAnalyze(netParams, simConfig)`. Extract the voltage
   trace from `sim.allSimData['V_soma']['cell_0']`. Save to `files/csv/netpyne_trace.csv`, PNG to
   `files/images/netpyne_trace.png`. Assert `max(v) > 20.0`. Wall-clock to timings.json. Satisfies
   REQ-3, REQ-4, REQ-5, REQ-7.

8. [CRITICAL] **Publish the `neuron-netpyne-install-report` answer asset.** Create
   `assets/answer/neuron-netpyne-install-report/` with (a) `details.json` conforming to
   `meta/asset_types/answer/specification.md` v2 (question, short_title, categories including
   `["simulator-tooling", "reproduction"]` if present in `meta/categories/`, answer_methods
   `["code-experiment"]`, confidence `high`, created_by_task, date_created), (b) `short_answer.md`
   (3-5 sentences: versions + "works" / "does not work" verdict), (c) `full_answer.md` (8 mandatory
   sections per the answer spec, embedding the two PNG traces, the versions.json contents,
   timings.json, a table of installer warnings verbatim, and the HH-built-in deviation note from
   step 5). Validate with
   `uv run python -u -m arf.scripts.verificators.verify_answer t0007_install_neuron_netpyne neuron-netpyne-install-report`.
   Satisfies REQ-8.

## Remote Machines

None required. All work runs locally in WSL2 on the researcher's Windows 11 workstation.

## Assets Needed

* **WSL2 with a recent Ubuntu distribution** — acquired via `wsl --install -d Ubuntu-22.04` on
  first run (one-time user setup, intervention filed if missing).
* **NEURON 8.2.7 Linux wheel** — from PyPI, installed inside the WSL venv.
* **NetPyNE 1.1.1 wheel** — from PyPI, installed alongside NEURON in the WSL venv.
* **A HH-family MOD source file** — copied from the NEURON package's `share/examples/nrniv/nmodl/`
  directory (shipped inside the NEURON wheel).

No prior task assets are required.

## Expected Assets

* **1 answer asset** `assets/answer/neuron-netpyne-install-report/` containing `details.json`
  (spec_version "2", question stating "does the NEURON 8.2.7 + NetPyNE 1.1.1 toolchain install and
  run a 1-compartment sanity simulation on this workstation?"), `short_answer.md` (3-5 sentences
  with verdict), and `full_answer.md` (full install log, sanity-simulation code links, embedded
  voltage-trace PNGs, versions, timings table, installer-warnings table, HH-built-in deviation
  note).

Matches `task.json` `expected_assets.answer = 1`.

## Time Estimation

* WSL installation (if required): ~10-20 min including reboot and Ubuntu first-run setup
  (interactive — filed as intervention, wall-clock outside agent control).
* Environment probe (step 2): <1 min.
* `pip install neuron==8.2.7 netpyne==1.1.1` (step 3): 2-5 min including wheel downloads.
* Versions probe (step 4): <1 min.
* `nrnivmodl` compile (step 5): <30 s.
* Raw NEURON sanity sim (step 6): <1 min including plot rendering.
* NetPyNE sanity sim (step 7): <1 min.
* Answer asset write + verificator (step 8): 2-3 min.
* **Total agent wall-clock (excluding WSL install intervention)**: 10-15 min.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| WSL2 not installed on the host workstation | **High** (confirmed by Phase 0 probe) | Blocker — all work depends on WSL | File `intervention/wsl_not_installed.md` with the exact `wsl --install` commands + reboot note; task enters `intervention_blocked` until user runs them. |
| NEURON 8.2.7 wheel missing for host Python version | Medium | Blocker — cannot install | Detect Python version in WSL; if >= 3.12, install `python3.11` via apt before creating the venv. |
| `gcc` / build-essential missing inside Ubuntu | Low | `nrnivmodl` fails | Fail step 5 with captured stderr; file `intervention/missing_gcc.md` requesting `sudo apt-get install -y build-essential`. |
| NetPyNE 1.1.1 tightens NEURON pin on install (new release) | Low | NEURON downgrade or conflict | Detect in pip output; record substitution in answer asset per task description's explicit fallback. |
| `wsl -e bash -lc` fails because bash is not the default WSL shell | Low | Commands silently fall through | Check `wsl -e echo "$SHELL"` in step 2; adjust quoting if needed. |
| matplotlib Agg backend missing in WSL venv | Very Low | PNG generation fails | pip-install `matplotlib` inside the venv if the NetPyNE install does not pull it transitively. |
| Worktree path `/mnt/c/Users/...` has permission issues for Linux user | Low | Cannot write CSV/PNG outputs | `wsl` by default mounts `/mnt/c` with `metadata,case=off` allowing writes; if writes fail, write to `/tmp/` first and `cp` back. |

Pre-mortem: the most likely failure is step 1 filing an intervention on a stock Windows 11 host with
WSL not yet installed. This is the `infrastructure-setup` task's main risk, already surfaced to the
researcher during planning — the install path was chosen knowing WSL might need a reboot.

## Verification Criteria

* `files/logs/pip_install.log` ends with `Successfully installed neuron-8.2.7 netpyne-1.1.1 ...`.
* `files/json/versions.json` contains keys `neuron` (=`8.2.7`), `netpyne` (=`1.1.1`), `hoc`
  (non-empty).
* `files/mod/x86_64/libnrnmech.so` exists after step 5 and `files/logs/nrnivmodl.log` is
  warning-free or documents each warning verbatim.
* `files/csv/raw_neuron_trace.csv` and `files/csv/netpyne_trace.csv` each have at least one row
  where `v >= 20.0`.
* `files/images/raw_neuron_trace.png` and `files/images/netpyne_trace.png` exist and render a
  voltage spike visually.
* `uv run python -u -m arf.scripts.verificators.verify_answer t0007_install_neuron_netpyne neuron-netpyne-install-report`
  passes.
* `uv run python -u -m arf.scripts.verificators.verify_task_structure t0007_install_neuron_netpyne`
  passes.
