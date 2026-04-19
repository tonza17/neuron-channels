---
spec_version: "1"
task_id: "t0007_install_neuron_netpyne"
research_stage: "internet"
searches_conducted: 10
sources_cited: 14
papers_discovered: 0
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Install NEURON 8.2.7 and NetPyNE 1.1.1 into the project's `uv` virtualenv on Windows 11, compile the
bundled Hodgkin-Huxley MOD files with `nrnivmodl`, run a 1-compartment HH sanity simulation twice
(raw NEURON and via NetPyNE's `specs.NetParams` + `sim.createSimulateAnalyze` harness), and record
installed versions, warnings, and wall-clock timings as a single answer asset named
`neuron-netpyne-install-report`.

## Gaps Addressed

This is an infrastructure-setup task with no `research/research_papers.md`, so there are no
literature gaps to close. The task instead demands closure of implementation-environment gaps pulled
from the task description. Each is marked with its resolution status:

1. **Does `uv pip install neuron==8.2.7` produce a working install on native Windows 11?** —
   **Unresolved / blocker**. The NEURON PyPI project ships wheels only for Linux (manylinux 2.17+
   x86-64) and macOS (10.15+ x86-64 and 11.0+ ARM64); there is no Windows wheel on PyPI for any
   NEURON version including 8.2.7 [NEURON-PyPI-2026]. The official install guide is explicit: "on
   Windows, the only recommended way to install NEURON is using the binary installer"
   [NEURON-InstallDocs-2026]. `uv pip install neuron==8.2.7` on Windows will fail with "no matching
   distribution" unless the user targets WSL [NEURON-InstallDocs-2026, uv-Issue1491-2024].

2. **Does the NEURON pip wheel bundle a C compiler for `nrnivmodl` on Windows?** — **Not
   applicable**. There is no pip wheel for Windows. The **Windows `.exe` installer**
   (`nrn-8.2.7-mingw-py-39-310-311-setup.exe`) does bundle a minimal MinGW g++ toolchain so that
   `nrnivmodl` / `mknrndll` can build `nrnmech.dll` [NEURON-WinBuild-2026, NEURON-UsingNMODL-2026].

3. **Where does NEURON store its bundled Hodgkin-Huxley MOD file in the installed package?** —
   **Resolved with a twist**. The `hh` mechanism is a **built-in** mechanism compiled into the core
   NEURON library — `hh`, `pas`, `IClamp`, `ExpSyn`, etc. are always available even without
   running `nrnivmodl` [NEURON-UsingNMODL-2026, NEURON-MoD-Forum-2018]. The `hh.mod` source file
   lives at `nrn/src/nrnoc/hh.mod` in the source tree [NEURON-GH-hhMod-2024], and additional example
   MODs live at `nrn/share/examples/nrniv/nmodl/` in the installed tree. Point 2 of the task scope
   ("compile the bundled HH MOD files with `nrnivmodl`") is therefore **technically redundant for
   producing a working HH simulation** — `soma.insert('hh')` works on a fresh install with zero
   `nrnivmodl` invocations. Running `nrnivmodl` on `share/examples/nrniv/nmodl/` is still useful as
   a **toolchain sanity check** that confirms the compiler is functional.

4. **Is NetPyNE 1.1.1 compatible with NEURON 8.2.7?** — **Resolved (soft constraint)**. NetPyNE's
   `setup.py` at tag v1.1.1 lists
   `numpy, scipy, matplotlib, matplotlib-scalebar, future, pandas, bokeh, schema, lfpykit, tqdm` in
   `install_requires` and **does not pin NEURON at all** [NetPyNE-GH-setup-2024]. The install docs
   simply recommend "the latest NEURON version" and direct users to `pip install neuron`
   [NetPyNE-InstallDocs-2026]. NEURON 8.2.7 is well within the 8.x line that NetPyNE 1.1.x targets,
   so no version override is expected.

5. **How is `nrnivmodl` invoked on Windows?** — **Resolved**. With the `.exe` installer, the
   Windows NEURON installer adds `nrnivmodl` to PATH, so from cmd.exe or PowerShell a plain
   `nrnivmodl` command run from the directory containing `.mod` files produces `nrnmech.dll`
   [NEURON-MknrnDLL-Forum-2012, NEURON-UsingNMODL-2026]. Known gotcha: having Git for Windows'
   `sh.exe` earlier on PATH than NEURON's bundled MinGW `sh.exe` breaks MinGW makefile invocation
   [MinGW-GH-ShConflict-2019]. From MSYS/git-bash the same command also works once PATH contains
   `<NEURONHOME>/mingw/bin`.

6. **What does a minimal 1-compartment HH sanity simulation look like in raw NEURON and in
   NetPyNE?** — **Resolved**. Canonical minimal patterns are documented in the NEURON basics
   tutorial [NEURON-Tutorial-2024] and the NetPyNE tutorial [NetPyNE-Tutorial-2026]; both are
   reproduced in *Implementation Patterns* below.

## Search Strategy

**Sources searched**: NEURON ReadTheDocs, PyPI project pages, NetPyNE documentation, NetPyNE GitHub
(`setup.py` at tag v1.1.1), NEURON Forum (neuron.yale.edu/phpBB), GitHub issues for
`neuronsimulator/nrn`, `astral-sh/uv`, Windows/MinGW toolchain discussions on GitHub, and general
Google Scholar for install gotchas.

**Queries executed** (10 total):

1. `"NEURON 8.2.7 pip install Windows nrnivmodl compiler"`
2. `"NEURON simulator Windows pip wheel MinGW bundled compiler mknrndll"`
3. `"NetPyNE 1.1.1 NEURON compatibility version requirements pypi"`
4. `"NEURON Windows installer nrnivmodl command prompt HH hh.mod location site-packages"`
5. `'"nrnivmodl" Windows "sh.exe" mingw error path not found'`
6. `'"NEURON uv pip install Windows wheel error "no matching distribution"'`
7. `"NEURON Python single compartment soma hh insert stim IClamp voltage record example"`
8. `'NetPyNE single compartment "hh" tutorial NetParams sim.createSimulateAnalyze example'`
9. `"NEURON simulator site-packages neuron demo examples hh.mod folder python"`
10. `'"nrnivmodl" no mod files built-in mechanism hh don\'t need compile'`

**Date range**: 2015-2026, with emphasis on 2022-2026 to capture the NEURON 8.x pip-wheel era.

**Inclusion criteria**: Sources had to (a) address NEURON 8.x install on Windows, or (b) document
NetPyNE's NEURON dependency declaration, or (c) show a runnable 1-compartment HH example, or (d)
describe where NEURON stores MOD files and how `nrnivmodl` compiles them. Excluded: Linux/macOS-only
install walkthroughs (except where they establish the MOD-file layout shared with Windows), posts
about NEURON <7.6, and non-English forum threads.

**Search iterations**: Queries 1-3 probed the install path directly; query 4 looked for the MOD-file
layout after install; query 5 followed the MinGW/sh.exe thread after discovering the toolchain is
MinGW-based; query 6 confirmed the "no Windows wheel" story with a wider search net; queries 7-8
collected the sanity-simulation code templates; queries 9-10 resolved the surprise finding that `hh`
is built in and does not require `nrnivmodl`.

## Key Findings

### The NEURON 8.2.7 PyPI wheel does not ship for Windows

NEURON's PyPI project publishes wheels only for Linux (manylinux 2.17+ x86-64) and macOS (10.15+
x86-64 and 11.0+ ARM64) across Python 3.9-3.13 [NEURON-PyPI-2026]. **There is no Windows wheel for
any NEURON version.** The PyPI project page explicitly notes that "it is possible to install the
Linux Python wheels on Windows via the Windows Subsystem for Linux (WSL)" [NEURON-PyPI-2026]. The
canonical install documentation repeats this: on Windows, the recommended install route is the
`nrn-<version>-mingw-py-38-39-310-311-setup.exe` binary installer
[NEURON-InstallDocs-2026, NEURON-WinBuild-2026]. The installer places NEURON's Python module inside
its own tree and exposes a `nrnpython` interpreter plus PATH entries; it **does not** drop a wheel
into an arbitrary venv.

**Implication for this task**: `uv pip install neuron==8.2.7` run from native Windows 11 cmd/bash
will return `ERROR: Could not find a version that satisfies the requirement neuron==8.2.7` — the
exact symptom documented for missing Requires-Python or OS wheel combinations [PipFlow-NoDist-2024].
The task's stated command is therefore expected to fail on native Windows. The task description
anticipates this class of failure ("If NEURON 8.2.7 wheels are unavailable for this Python version,
fall back to the nearest supported patch release and record the substitution in the answer asset"
— but the root cause here is **OS**, not patch version). Two recovery paths exist:

* **Path A (WSL)**: Install NEURON in WSL via `pip install neuron==8.2.7`; run the sanity sims
  inside WSL. This matches the PyPI docs' own recommendation [NEURON-PyPI-2026].
* **Path B (native installer)**: Run the bundled Windows `.exe` installer, then point the `uv`
  venv's Python at it via `PYTHONPATH`. This keeps the workflow on native Windows but does not use
  pip.

The orchestrator should pick Path A or Path B based on project conventions; the `uv pip install`
command in the task scope will not succeed unchanged on Windows 11 native.

### The `hh` mechanism is built into core NEURON and does not need `nrnivmodl`

`hh`, `pas`, `IClamp`, `ExpSyn`, `na_ion`, `k_ion` and a handful of other mechanisms are compiled
into `libnrniv` / `libnrnoc` at NEURON build time [NEURON-UsingNMODL-2026, NEURON-MoD-Forum-2018].
`soma.insert('hh')` works on a freshly installed NEURON with **zero `nrnivmodl` invocations** —
this is why tutorials like the MIT one can do `s1.insert('hh')` directly without a prior compile
step [NEURON-Tutorial-2024]. The `hh.mod` *source* file is preserved at `nrn/src/nrnoc/hh.mod` in
the source tree [NEURON-GH-hhMod-2024] for reference and for users who want to re-derive channel
kinetics, but it is not required at runtime.

**Implication for this task**: the sanity simulation (`soma.insert('hh')`, 0.5 nA step, check spike)
will run on a vanilla NEURON install even if `nrnivmodl` is never invoked. Task scope point 2
("compile the bundled Hodgkin-Huxley MOD files with `nrnivmodl`") should be reinterpreted as a
**toolchain-validation smoke test** rather than a prerequisite for the HH simulation: pick a trivial
extra `.mod` (e.g., one from `share/examples/nrniv/nmodl/`) and compile it to prove `nrnivmodl` +
the bundled MinGW compiler are wired up correctly. Record the compilation wall-clock and warnings
exactly as the task scope demands — just flag explicitly in the answer asset that the HH sanity
sim is independent of this compile step.

### NetPyNE 1.1.1 does not pin a NEURON version

Inspection of NetPyNE's `setup.py` at tag v1.1.1 on GitHub shows `install_requires` contains only
`numpy, scipy, matplotlib, matplotlib-scalebar, future, pandas, bokeh, schema, lfpykit, tqdm`
[NetPyNE-GH-setup-2024]. **NEURON is not a declared dependency** — NetPyNE assumes the user has
installed NEURON separately, and the install docs tell users to run `pip install neuron` as a peer
step [NetPyNE-InstallDocs-2026]. This means `uv pip install netpyne==1.1.1` will succeed independent
of whether NEURON is installed, and will not override a pre-existing NEURON install. No NetPyNE
1.1.1 ↔ NEURON 8.2.7 version conflict is expected; the pairing is effectively whatever NEURON the
environment provides.

### `nrnivmodl` on Windows requires NEURON's MinGW `sh.exe`, not Git's

The Windows NEURON installer bundles a minimal MinGW toolchain under `<NEURONHOME>/mingw/` that
`nrnivmodl.bat` / `mknrndll.bat` invoke to produce `nrnmech.dll`
[NEURON-WinBuild-2026, NEURON-UsingNMODL-2026]. A **recurring gotcha** across MinGW-based build
systems is that Git for Windows installs its own `sh.exe` under `C:\Program Files\Git\bin\sh.exe`
(or `usr/bin/`) and places it earlier on PATH. MinGW make explicitly refuses to work if **any**
`sh.exe` is earlier on PATH than the MinGW-internal one, producing errors like "sh.exe was found in
your PATH" [MinGW-GH-ShConflict-2019]. The same class of failure appears in reports from NEURON
users running on Windows machines with Git installed. Mitigations:

* Run `nrnivmodl` from `cmd.exe` with `C:\Program Files\Git\bin` removed from PATH for that shell.
* Or: invoke `nrnivmodl` via the NEURON "bash" icon that pre-configures PATH from
  `<NEURONHOME>/mingw_files/nrnmingwenv.sh` [NEURON-WinBuild-2026].
* Or: run under WSL (Path A from the first finding).

**Best practice**: when running `nrnivmodl` programmatically from Python `subprocess`, set
`env={"PATH": f"{NEURONHOME}/bin;{NEURONHOME}/mingw/bin;{os.environ['PATH']}"}` explicitly and drop
Git-bundled `sh.exe` from the copy of PATH used for the subprocess.

### Minimal single-compartment HH sanity-simulation patterns

The raw NEURON canonical pattern [NEURON-Tutorial-2024]:

```python
from neuron import h

soma = h.Section(name="soma")
soma.L = 20
soma.diam = 20
soma.insert("hh")

stim = h.IClamp(soma(0.5))
stim.delay = 5
stim.dur = 50
stim.amp = 0.5  # nA

t_vec = h.Vector().record(h._ref_t)
v_vec = h.Vector().record(soma(0.5)._ref_v)

h.finitialize(-65)
h.continuerun(100)
```

The NetPyNE canonical pattern [NetPyNE-Tutorial-2026]:

```python
from netpyne import specs, sim

netParams = specs.NetParams()
netParams.popParams["S"] = {"cellType": "PYR", "numCells": 1}

cellRule = {"secs": {"soma": {"geom": {"L": 20, "diam": 20, "Ra": 100},
                              "mechs": {"hh": {"gnabar": 0.12,
                                               "gkbar": 0.036,
                                               "gl": 0.0003,
                                               "el": -54.3}}}}}
netParams.cellParams["PYR"] = cellRule
netParams.cellParams["PYR"]["conds"] = {"cellType": "PYR"}

netParams.stimSourceParams["Input"] = {"type": "IClamp", "delay": 5, "dur": 50, "amp": 0.5}
netParams.stimTargetParams["Input->S"] = {"source": "Input",
                                           "conds": {"pop": "S"},
                                           "sec": "soma", "loc": 0.5}

simConfig = specs.SimConfig()
simConfig.duration = 100
simConfig.dt = 0.025
simConfig.recordTraces = {"V_soma": {"sec": "soma", "loc": 0.5, "var": "v"}}
simConfig.recordStep = 0.1

sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
```

Both patterns are minimum viable. A "spike" is any sample in `v_vec` exceeding +20 mV, matching the
task's spike criterion.

## Methodology Insights

* **Reinterpret the task's `uv pip install neuron==8.2.7` command on Windows.** Native Windows has
  no NEURON wheel on PyPI [NEURON-PyPI-2026, NEURON-InstallDocs-2026]. Use WSL (recommended) or the
  `.exe` binary installer; record which path was chosen and why in the install report.

* **Treat `nrnivmodl` as a toolchain check, not an HH prerequisite.** `hh` is built in; the sanity
  simulation runs without any `nrnivmodl` call [NEURON-UsingNMODL-2026]. Still run `nrnivmodl` on a
  trivial extra `.mod` as the task scope requires, and record wall-clock and warnings.

* **Remove Git's `sh.exe` from the PATH used by the `nrnivmodl` subprocess.** Mitigates the single
  most-reported Windows-native failure mode [MinGW-GH-ShConflict-2019, NEURON-WinBuild-2026].

* **Accept that NetPyNE 1.1.1 does not pin NEURON.** Any NEURON 8.x in the venv is acceptable
  [NetPyNE-GH-setup-2024]. The task's 8.2.7 pin is project-internal, not enforced by NetPyNE.

* **Capture `neuron.__version__`, `netpyne.__version__`, and `h.nrnversion(0)` verbatim.**
  `h.nrnversion(0)` gives the full "about" string including build date and MPI status, which is the
  canonical record of which NEURON binary was actually loaded [NEURON-Tutorial-2024].

* **Spike criterion**: `max(v_vec) > 20` with a 0.5 nA, 50 ms step into a 20 µm x 20 µm soma is a
  textbook suprathreshold stimulus and should produce a burst of 5-10 spikes in raw NEURON — a
  trace with **zero** spikes indicates a failed install, not a subtle calibration issue
  [NEURON-Tutorial-2024].

**Hypotheses** (testable in the install script):

* **H1**: `uv pip install neuron==8.2.7` will fail on native Windows 11 with "no matching
  distribution" — confirmable by running it once and capturing the error verbatim.

* **H2**: After NetPyNE 1.1.1 installs, running the NetPyNE wrapper sim produces a voltage trace
  within **< 0.1 mV RMS** of the raw-NEURON trace on the same cell, because NetPyNE is a thin
  wrapper that calls identical NEURON primitives.

* **H3**: `nrnivmodl` wall-clock for a single trivial `.mod` file on this workstation will be under
  **20 s** on a cold build — order-of-magnitude consistent with reports from
  [NEURON-MknrnDLL-Forum-2012].

**Best practices identified**:

* Always record `h.nrnversion(0)`, not just `neuron.__version__`, because the former reveals MPI,
  Python-coupling, and build-timestamp discrepancies that the pip metadata hides.
* Run `nrnivmodl` from a dedicated scratch directory containing only the `.mod` files being compiled
  — it writes an `x86_64/` (or `nrnmech.dll` on Windows) output tree in the CWD that otherwise
  pollutes source trees.
* For NetPyNE, set `simConfig.saveJson = False` and `simConfig.saveFolder = str(...)` to avoid
  NetPyNE writing sidecar files into whatever CWD the agent happened to pick.

## Discovered Papers

No new papers were discovered. This is an infrastructure-setup task focused on toolchain validation;
all relevant sources are documentation pages, package indices, and forum threads. Nothing in the
reviewed material cites or defines a paper that should be added to the project's paper corpus for
future NEURON/NetPyNE compartmental-modelling work beyond the canonical Hines & Carnevale (1997)
reference already listed in `project/description.md`.

## Recommendations for This Task

1. **Before running `uv pip install neuron==8.2.7`, check for Windows wheel availability
   explicitly.** Run `uv pip install --dry-run neuron==8.2.7` first and capture the resolver's
   verdict [NEURON-PyPI-2026]. If it resolves, proceed. If it errors, record the error verbatim in
   the answer asset and switch to Path B (native `.exe` installer) or Path A (WSL) — the task
   description's own Risks & Fallbacks clause explicitly permits this substitution.

2. **Add an intervention file if native Windows pip fails and WSL is not available.** The task
   description's fallback clause ("If `nrnivmodl` needs `gcc`/`clang` that is not on PATH, create an
   intervention file") should be extended: if neither pip-on-Windows nor WSL nor the binary
   installer is available to the agent, create an intervention file requesting a human to choose
   among the three.

3. **Treat `nrnivmodl` on `share/examples/nrniv/nmodl/` as the toolchain smoke test.** `hh` is built
   in [NEURON-UsingNMODL-2026]; `nrnivmodl` compiling a trivial extra `.mod` still proves the
   compiler toolchain works and satisfies task scope point 2.

4. **Run `nrnivmodl` with a sanitised PATH.** Explicitly remove `C:\Program Files\Git\bin` and
   `C:\Program Files\Git\usr\bin` from the subprocess PATH to avoid the Git `sh.exe` conflict
   [MinGW-GH-ShConflict-2019].

5. **Verify spike by `max(v_vec) > +20 mV`.** The task scope specifies "V crosses +20 mV" as the
   spike criterion; `numpy.max(numpy.array(v_vec)) > 20.0` is the one-liner check. A trace with
   `max(v) < 0 mV` almost always means `hh` was not actually inserted (typo, missing import) or the
   IClamp delay/duration were swapped [NEURON-Tutorial-2024].

6. **Record `h.nrnversion(0)` verbatim** in the answer asset alongside `neuron.__version__` and
   `netpyne.__version__`. This is the string every downstream reproduction task will look for.

7. **Record install wall-clocks per phase** (uv pip NEURON, uv pip NetPyNE, nrnivmodl, raw-NEURON
   sim, NetPyNE sim) to give downstream tasks a runtime baseline for this workstation. Tabulate in
   `full_answer.md` as demanded by the task description.

## Source Index

### [NEURON-InstallDocs-2026]

* **Type**: documentation
* **Title**: Installing Binary Distribution — NEURON documentation
* **Author/Org**: NEURON Simulator project
* **Date**: 2026 (live docs site; latest revision)
* **URL**: https://nrn.readthedocs.io/en/latest/install/install_instructions.html
* **Peer-reviewed**: no
* **Relevance**: Canonical install instructions. States unambiguously that Windows native install
  must use the `.exe` binary installer, not pip, and documents that the installer bundles a MinGW
  g++ toolchain for `nrnivmodl`.

### [NEURON-WinBuild-2026]

* **Type**: documentation
* **Title**: Windows build — NEURON documentation
* **Author/Org**: NEURON Simulator project
* **Date**: 2026
* **URL**: https://nrn.readthedocs.io/en/latest/install/windows.html
* **Peer-reviewed**: no
* **Relevance**: Windows-specific install and build guidance. Documents the
  `nrn-<version>-mingw-py-38-39-310-311-setup.exe` naming convention, the bundled MinGW toolchain,
  and how `nrnivmodl` is wired up via `mingw_files/nrnmingwenv.sh`.

### [NEURON-PyPI-2026]

* **Type**: documentation
* **Title**: neuron 8.2.7 — PyPI project page
* **Author/Org**: NEURON Simulator project / PyPI
* **Date**: 2026
* **URL**: https://pypi.org/project/neuron/8.2.7/
* **Peer-reviewed**: no
* **Relevance**: Authoritative record of which wheels exist. Confirms no Windows wheel for 8.2.7 —
  the core finding that blocks the task's `uv pip install neuron==8.2.7` command on native Windows.

### [NEURON-UsingNMODL-2026]

* **Type**: documentation
* **Title**: Using NMODL Files
* **Author/Org**: NEURON Simulator project (neuron.yale.edu)
* **Date**: 2026
* **URL**: https://neuron.yale.edu/neuron/docs/using-nmodl-files
* **Peer-reviewed**: no
* **Relevance**: Documents the built-in mechanisms (`hh`, `pas`, `IClamp`, `ExpSyn`) that are always
  available without `nrnivmodl`. Key source for the finding that the HH sanity simulation does not
  actually require a compile step.

### [NEURON-GH-hhMod-2024]

* **Type**: repository
* **Title**: nrn/src/nrnoc/hh.mod
* **Author/Org**: NEURON Simulator project (GitHub)
* **Date**: 2024 (latest commit on master)
* **URL**: https://github.com/neuronsimulator/nrn/blob/master/src/nrnoc/hh.mod
* **Last updated**: 2024
* **Peer-reviewed**: no
* **Relevance**: The canonical Hodgkin-Huxley MOD file inside the NEURON source tree. Useful as the
  reference for gnabar, gkbar, gl, el defaults cited in the NetPyNE sanity example.

### [NEURON-MknrnDLL-Forum-2012]

* **Type**: forum
* **Title**: Running mknrndll from the command line
* **Author/Org**: NEURON user forum (neuron.yale.edu/phpBB)
* **Date**: 2012 (thread with updates through 2020)
* **URL**: https://www.neuron.yale.edu/phpBB/viewtopic.php?t=2777
* **Peer-reviewed**: no
* **Relevance**: Long-running thread documenting how `mknrndll` / `nrnivmodl` is invoked on Windows,
  including the MinGW PATH setup. Note: forum content; treat as practitioner experience rather than
  official spec.

### [NEURON-Tutorial-2024]

* **Type**: documentation
* **Title**: A NEURON Programming Tutorial, Part B
* **Author/Org**: MIT / NEURON project (mirror of Hines & Carnevale tutorial)
* **Date**: 2024 (stable tutorial)
* **URL**: http://web.mit.edu/neuron_v7.4/nrntuthtml/tutorial/tutB.html
* **Peer-reviewed**: no (tutorial)
* **Relevance**: Canonical single-compartment HH example. Supplies the raw-NEURON code template for
  the sanity simulation and the `soma.insert('hh')` idiom.

### [NEURON-MoD-Forum-2018]

* **Type**: forum
* **Title**: mod files: what they are, and how to use them
* **Author/Org**: NEURON user forum (neuron.yale.edu/phpBB)
* **Date**: 2018
* **URL**: https://www.neuron.yale.edu/phpBB/viewtopic.php?t=3263
* **Peer-reviewed**: no
* **Relevance**: Community-written explanation of the distinction between built-in and user MOD
  mechanisms. Cross-confirms the "hh is built in" finding.

### [NetPyNE-InstallDocs-2026]

* **Type**: documentation
* **Title**: Installation — NetPyNE documentation
* **Author/Org**: SUNY Downstate NetPyNE project
* **Date**: 2026
* **URL**: http://doc.netpyne.org/install.html
* **Peer-reviewed**: no
* **Relevance**: Official NetPyNE install docs. Confirms Linux/macOS as primary platforms, does not
  pin a specific NEURON version, and recommends `pip install neuron` as a peer step.

### [NetPyNE-GH-setup-2024]

* **Type**: repository
* **Title**: netpyne/setup.py at tag v1.1.1
* **Author/Org**: suny-downstate-medical-center/netpyne
* **Date**: 2024
* **URL**: https://github.com/suny-downstate-medical-center/netpyne/blob/v1.1.1/setup.py
* **Last updated**: 2024
* **Peer-reviewed**: no
* **Relevance**: Authoritative dependency declaration for NetPyNE 1.1.1. Confirms the package does
  not pin any NEURON version, so NetPyNE 1.1.1 ↔ NEURON 8.2.7 is expected to work.

### [NetPyNE-Tutorial-2026]

* **Type**: documentation
* **Title**: NetPyNE Tutorial
* **Author/Org**: SUNY Downstate NetPyNE project
* **Date**: 2026
* **URL**: http://doc.netpyne.org/tutorial.html
* **Peer-reviewed**: no
* **Relevance**: Canonical NetPyNE HH network example. Supplies the `specs.NetParams` /
  `sim.createSimulateAnalyze` template adapted for the single-cell sanity simulation.

### [MinGW-GH-ShConflict-2019]

* **Type**: forum
* **Title**: MinGW not usable because there is Git's sh.exe in the PATH
* **Author/Org**: actions/runner-images (GitHub Issues)
* **Date**: 2019
* **URL**: https://github.com/actions/virtual-environments/issues/111
* **Peer-reviewed**: no
* **Relevance**: Documents the Git-`sh.exe`-on-PATH problem that breaks MinGW makefile-based builds.
  Applies directly to NEURON's `nrnivmodl` on Windows, which invokes MinGW make internally.

### [uv-Issue1491-2024]

* **Type**: forum
* **Title**: `uv pip install` inconsistent failure on Windows
* **Author/Org**: astral-sh/uv (GitHub Issues)
* **Date**: 2024
* **URL**: https://github.com/astral-sh/uv/issues/1491
* **Peer-reviewed**: no
* **Relevance**: Documents `uv`-specific quirks on Windows package resolution. Context for the
  expected "no matching distribution" behaviour when the target wheel is genuinely missing from PyPI
  for the Windows/Python combination.

### [PipFlow-NoDist-2024]

* **Type**: documentation
* **Title**: ERROR: No matching distribution found
* **Author/Org**: RepoFlow documentation
* **Date**: 2024
* **URL**: https://www.repoflow.io/errors/pip/no-matching-distribution-found
* **Peer-reviewed**: no
* **Relevance**: General reference for the error class that `uv pip install neuron==8.2.7` will
  produce on Windows. Explains the three common root causes (Python version, OS/arch, Python ABI).
