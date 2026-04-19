---
spec_version: "1"
task_id: "t0007_install_neuron_netpyne"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 4
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-19"
status: "complete"
---
# Research Code: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1

## Task Objective

Install NEURON 8.2.7 and NetPyNE 1.1.1 into the project's `uv` virtualenv on Windows 11, compile the
bundled Hodgkin-Huxley MOD files with `nrnivmodl`, run a 1-compartment HH sanity simulation twice
(raw NEURON and via NetPyNE's `specs.NetParams` + `sim.createSimulateAnalyze` harness), and record
the installed versions, warnings, wall-clock timings, and voltage traces as a single answer asset
named `neuron-netpyne-install-report`. The known Windows constraint (no PyPI wheel, installer-based
path only) must be handled as a primary-path fork, not a late fallback.

## Library Landscape

No library assets exist anywhere in the project yet. A manual walk of `tasks/*/assets/library/`
returned zero entries — confirming the aggregate_libraries aggregator result (the aggregator
script is not yet implemented in `arf/scripts/aggregators/`, but the filesystem is authoritative
because no prior task has produced a library asset). The first library assets are scheduled for
t0008 (ModelDB 189347 NEURON port), t0011 (response-visualisation library) and t0012 (tuning-curve
scoring library), all of which depend on t0007 finishing first. The Library Landscape is therefore
empty by construction: this is the first NEURON/NetPyNE-bearing task in the repo and has nothing to
inherit via the `tasks.tNNNN.code.*` library-import mechanism.

## Key Findings

### NEURON Windows install path is settled upstream — the task plan just has to pick one

Every concrete install fact this task needs was already produced and vetted by the simulator-choice
task [t0003] and the internet research stage of this task. [t0003]'s answer asset
`dsgc-compartmental-simulator-choice` cements NEURON 8.2.7 + NetPyNE 1.1.1 as the primary stack and
lists
`tasks/t0003_simulator_library_survey/assets/answer/dsgc-compartmental-simulator-choice/full_answer.md`
as the canonical version-matrix reference. The unresolved gap is entirely OS-platform: NEURON
publishes no Windows PyPI wheel, so the task's stated `uv pip install neuron==8.2.7` command fails
with "no matching distribution" on native Windows 11. Two recovery paths are documented: (a) install
inside WSL and run the sanity sims there, or (b) run the Windows `.exe` installer
(`nrn-8.2.7-mingw-py-...-setup.exe`) and point the venv at it. Path (a) matches the PyPI project's
own recommendation; path (b) keeps execution on native Windows. The implementation must pick one at
planning time and record the decision in the `neuron-netpyne-install-report` answer asset. No prior
task has installed NEURON or NetPyNE, so there is no in-repo installation telemetry to consult.

### `hh` is a built-in mechanism, so `nrnivmodl` is a toolchain smoke-test, not a prerequisite

The task description reads as if `nrnivmodl` must compile `hh.mod` before `soma.insert('hh')` can
work. Research shows this is false: `hh`, `pas`, `IClamp`, `ExpSyn`, `na_ion`, `k_ion` are compiled
into `libnrniv` at NEURON build time. `soma.insert('hh')` works on a fresh install with zero
`nrnivmodl` invocations. The practical consequence for the implementation: pick any trivial extra
`.mod` (NEURON ships examples under `share/examples/nrniv/nmodl/` in the installed tree) and compile
that to prove the toolchain is wired up. Record compilation wall-clock and warnings as the task
demands, but flag explicitly in the answer asset that the HH sanity sim does not depend on it.

### `run_with_logs.py` is a working, widely-used wrapper — use it for every shell call

The wrapper lives at `arf/scripts/utils/run_with_logs.py` and has been used heavily by [t0005] (21+
calls including a `curl` download, a bash `uv run python` validator, and a verify-dataset run) and
by [t0004] (multiple `uv run ruff`, `uv run mypy`, `uv run pytest` calls). Its CLI is:

```bash
uv run python -u -m arf.scripts.utils.run_with_logs --task-id <task_id> -- <command...>
```

It creates `tasks/<task_id>/logs/commands/NNN_<timestamp>_<slug>.{json,stdout.txt,stderr.txt}` with
a frozen Pydantic `CommandLogEntry` schema (`spec_version`, `task_id`, `command`, `exit_code`,
`duration_seconds`, `started_at`, `completed_at`, `working_directory`, stdout/stderr line counts,
`truncated` flag). Secrets matching `api_key=...`, `Bearer ...`, JSON `"token": "..."` etc. are
redacted before write. `VIRTUAL_ENV` is scrubbed from the child env to silence `uv` worktree
warnings. `MAX_OUTPUT_LINES = 10_000` applies per stream with the last-N-lines retained on
truncation. This is the only supported way to shell out to `uv pip install neuron==8.2.7`,
`nrnivmodl`, or the `.exe` installer — the rule is enforced by project CLAUDE.md §Key Rules, and
the verificator reads `logs/commands/` to confirm compliance.

### Typed frozen dataclass + paths.py module is the canonical code pattern

[t0004]'s `code/generate_target.py` and `code/paths.py` demonstrate the repo's code shape for a
script-producing task. `paths.py` centralises every output path as a module-level `Path` constant
derived from `TASK_ROOT = Path(__file__).resolve().parent.parent`. `generate_target.py` is a single
executable module using `@dataclass(frozen=True, slots=True)` for parameter bundles, explicit type
annotations on every variable (`angles_rad: np.ndarray = ...`), `matplotlib.use("Agg")` before
`pyplot` is imported (critical for headless runs), `assert` for positive-framed precondition checks,
and keyword-only call sites. [t0005]'s `code/validate_swc.py` adds the stdlib-first pattern (avoid
new pip dependencies when possible) and the "try an optional import" hedge via
`importlib.import_module("neurom")` with a string-valued status return when the library is missing
— a direct template for the `import neuron` / `import netpyne` sanity probe this task needs.

### Answer asset v2 is the exact output shape this task requires

The task's sole expected asset is a v2 answer, and [t0003] and [t0002] each produced one. [t0003]'s
`dsgc-compartmental-simulator-choice` (categories `compartmental-modeling`, `retinal-ganglion-cell`;
`answer_methods: ["internet"]`; `confidence: "high"`; 20 `source_urls`) is the closest template
because it answers a single simulator-tooling question. [t0002]'s
`how-does-dsgc-literature-structure-the-five-research-questions` (`answer_methods` with `"papers"`)
shows the paper-source variant. Both use slug-based folder names matching
`^[a-z0-9]+(-[a-z0-9]+)*$`; the task's stated `neuron-netpyne-install-report` already matches. Both
ship `details.json` + `short_answer.md` + `full_answer.md`; the paths are set explicitly in
`details.json` (`short_answer_path`, `full_answer_path`) — v2 assets must declare them. For this
task, `answer_methods` should be `["code-experiment"]` (install + two sims are code experiments) and
`confidence: "high"` matches the pattern in [t0003].

### Headless matplotlib and `results/images/` convention

Both [t0004] (`PLOT_PATH = RESULTS_IMAGES_DIR / "target_tuning_curve.png"`) and the repo markdown
style guide treat `results/images/` as the canonical location for PNG charts used in reports. The
task description asks for voltage traces "embedded as PNGs in `files/images/`" inside the answer
asset — this is a deliberate asset-scoped override because the PNGs belong to the answer, not the
generic `results/` reporting area. Both locations are valid under spec; the answer-asset path is
closer to what this task demands. Regardless, `matplotlib.use("Agg")` must be called before
`import matplotlib.pyplot as plt`, per [t0004]'s working example.

## Reusable Code and Assets

1. `tasks/t0003_simulator_library_survey/assets/answer/dsgc-compartmental-simulator-choice/`
   * **What it does**: Canonical simulator-choice answer asset; sets versions and backup strategy.
   * **Reuse method**: **read-only reference** (consumed as input evidence, not code). Cite in the
     new answer asset's `source_task_ids` or as prose evidence. Do not copy files.
   * **Structure**: `details.json` (v2), `short_answer.md` (37 lines), `full_answer.md` (comparison
     table + 20 URL citations). Use as the template for the shape of the new answer.
   * **Adaptation needed**: none — read-only input.

2. `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/`
   * **What it does**: Second concrete v2 answer asset in the project (paper-sourced variant).
   * **Reuse method**: **read-only reference** for `answer_methods: ["papers"]` shape only; this
     task uses `["code-experiment"]`.
   * **Adaptation needed**: none — read-only input.

3. `arf/scripts/utils/run_with_logs.py`
   * **What it does**: Wraps every shell call, captures stdout/stderr, writes a structured JSON log
     under `logs/commands/`.
   * **Reuse method**: **invoke via CLI** —
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0007_install_neuron_netpyne -- <command...>`.
     This is framework code, not task code; it is never copied.
   * **Key API**: single CLI with `--task-id <task_id>`, then `--` separator, then the command
     tokens. Exit code propagates from the child process. Any `VIRTUAL_ENV` env var is stripped in
     the child, so calls from the outer shell into a sibling worktree do not print uv warnings.
   * **Adaptation needed**: none.

4. `tasks/t0004_generate_target_tuning_curve/code/paths.py` (≈18 lines)
   * **What it does**: Demonstrates the `TASK_ROOT = Path(__file__).resolve().parent.parent` idiom
     plus explicit typed `Path` constants for every output.
   * **Reuse method**: **copy into task** — create
     `tasks/t0007_install_neuron_netpyne/code/paths.py` with the same idiom but pointing at
     `assets/answer/neuron-netpyne-install-report/` and its `files/`, `files/images/`
     subdirectories.
   * **Adaptation needed**: change `DATASET_ID` → `ANSWER_ID`, update downstream paths (no CSVs
     here; instead `install_log.txt`, `nrnivmodl_output.txt`, `neuron_trace.csv`,
     `netpyne_trace.csv`, `neuron_trace.png`, `netpyne_trace.png`).
   * **Estimated size**: ~25 lines.

5. `tasks/t0004_generate_target_tuning_curve/code/generate_target.py` (≈258 lines)
   * **What it does**: End-to-end example of a task's `code/<script>.py`: typed params dataclass,
     pure-function compute steps, CSV writers, matplotlib `Agg` plotting, argparse-free `main()`.
   * **Reuse method**: **copy patterns, not code** — structural template only. The NEURON +
     NetPyNE simulation and the `subprocess`-free approach (this task calls `run_with_logs` via the
     CLI, not via a Python `subprocess.run`) are entirely new.
   * **Adaptation needed**: entire compute replaced with two sanity-sim functions
     (`run_raw_neuron_sim()`, `run_netpyne_sim()`), each returning a frozen
     `@dataclass(frozen=True, slots=True) SimResult(t_vec, v_vec, n_spikes, wall_clock_s)`.
   * **Estimated size**: new module ~200 lines modelled on this file's structure.

6. `tasks/t0005_download_dsgc_morphology/code/validate_swc.py` (≈237 lines)
   * **What it does**: Demonstrates the stdlib-first pattern, the optional-import hedge
     (`importlib.import_module("neurom")`) with a string status return, frozen dataclass summary,
     and `argparse` CLI.
   * **Reuse method**: **copy pattern** — the optional-import hedge is the exact shape needed for
     the `import neuron` / `import netpyne` version probe at the top of `install_and_validate.py`.
     Do not copy the SWC parsing code.
   * **Adaptation needed**: replace `neurom.load_morphology` with `neuron.__version__` +
     `import neuron; h = neuron.h; h('nrnversion()')` and `netpyne.__version__`.
   * **Estimated size**: ~30 lines of the optional-import pattern reused.

## Lessons Learned

* **No prior task has installed a Python package via `uv pip install`**. [t0005] used `curl` for a
  file download; [t0004] and [t0005] only ran `uv run python`, `uv run ruff`, `uv run mypy`,
  `uv run flowmark`. Running `uv pip install neuron==8.2.7 netpyne==1.1.1` wrapped in
  `run_with_logs` is therefore a new code path for this repo — expect surprises around exit codes,
  stderr warnings that are not errors, and `uv`'s `VIRTUAL_ENV` handling. Allow extra wall-clock in
  the plan.
* **Verificator availability is inconsistent**. [t0004]'s and [t0005]'s results summaries both note
  that `verify_dataset_asset.py` is not implemented; both worked around it by applying the dataset
  spec rules manually. The answer-asset verificator (`verify_answer_asset.py`) exists and was run
  clean by [t0003]; this task should rely on it for the sole expected asset.
* **Plan ambiguity about `.mod` file compilation**. [t0005] logged a deliberate deviation
  (`dsgc_baseline_morphology` → `dsgc-baseline-morphology`) in its plan. This task will similarly
  need to document the "`hh` is built-in, so `nrnivmodl` compiles a different `.mod`" deviation from
  the literal task description, in the plan's Task Requirement Checklist and in the answer asset
  itself.
* **Intervention mechanism is defined but never exercised**. No `intervention/*.json` file exists in
  any completed task. The task description calls for an intervention file if `gcc`/`clang` is
  missing for `nrnivmodl`; if that path triggers, this task will be the first to write one, and its
  format should be locked down by re-reading the intervention verificator output before writing.
* **Headless plotting must be set up explicitly**. [t0004] called `matplotlib.use("Agg")` before
  importing `pyplot`. Skipping this step on Windows can produce a "no DISPLAY" error when running
  under WSL via an X-forwarding shell, or interactive-backend warnings on native Windows.

## Recommendations for This Task

1. **Pick the install path up-front (WSL vs Windows `.exe`) and commit to one in the plan.** Do not
   branch at implementation time. The choice should be recorded in a `### Install Path` subsection
   of the plan. Evidence: [t0003]'s answer asset sets the version pair; research_internet.md
   documents that the literal `uv pip install neuron==8.2.7` cannot succeed natively on Windows.
2. **Copy [t0004]'s `paths.py` + `generate_target.py` structure into
   `tasks/t0007_install_neuron_netpyne/code/`**, then replace the compute with two sanity-sim
   functions and a `main()` that orchestrates install → nrnivmodl → sim-raw → sim-netpyne →
   write answer asset. Keep the typed frozen-dataclass convention and the explicit
   `matplotlib.use("Agg")` line from [t0004].
3. **Wrap every shell-out (`uv pip install`, `nrnivmodl`, the `.exe` installer if Path B is taken)
   in `arf/scripts/utils/run_with_logs.py`**, following [t0005]'s 21-call usage pattern. Invoke it
   as a CLI subprocess from the task's `install_and_validate.py`, not from inside Python via
   `subprocess.run`; this keeps the logging surface centralised.
4. **Use [t0005]'s optional-import hedge pattern** (`importlib.import_module` wrapped in
   `try/except ImportError`) for the `import neuron` and `import netpyne` probes so that a failed
   install produces a clean status string in the answer asset instead of an uncaught `ImportError`.
5. **Model the answer asset on [t0003]'s `dsgc-compartmental-simulator-choice`** — v2 spec,
   explicit `short_answer_path`/`full_answer_path`, `answer_methods: ["code-experiment"]`,
   `categories: ["compartmental-modeling"]` (add `retinal-ganglion-cell` only if the report relates
   the install to RGC work; otherwise omit), `confidence: "high"`. Embed voltage-trace PNGs under
   `assets/answer/neuron-netpyne-install-report/files/images/` per the task description.
6. **Re-interpret task scope point 2 before coding.** Document the "`hh` is built-in" finding in the
   plan's Task Requirement Checklist as an explicit deviation, then pick a trivial alternate `.mod`
   from `<NEURONHOME>/share/examples/nrniv/nmodl/` for the `nrnivmodl` smoke test. Record which
   `.mod` was chosen and why in the short answer.

## Task Index

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: compartmental models of DS retinal ganglion cells
* **Status**: completed
* **Relevance**: Second concrete v2 answer-asset example in the project. Referenced as a template
  for `answer_methods: ["papers"]`-shaped assets (this task will produce a different-methods
  variant).

### [t0003]

* **Task ID**: `t0003_simulator_library_survey`
* **Name**: Simulator library survey for DSGC compartmental modelling
* **Status**: completed
* **Relevance**: Upstream decision task that picked NEURON 8.2.7 + NetPyNE 1.1.1. Its answer asset
  `dsgc-compartmental-simulator-choice` is the canonical version reference and the closest v2
  answer-asset template (single simulator-tooling question). This task's report must be consistent
  with [t0003]'s recommendations.

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate canonical target angle-to-AP-rate tuning curve
* **Status**: completed
* **Relevance**: Canonical example of the repo's task-code layout: `code/paths.py` for centralised
  Path constants and `code/<script>.py` for a typed, frozen-dataclass implementation with
  `matplotlib.use("Agg")` and a `main()` entry point. This task will copy the structural pattern.

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download candidate DSGC morphology
* **Status**: completed
* **Relevance**: Only prior task that shelled out heavily via `run_with_logs.py` (21+ commands
  including `curl` downloads). Source of the optional-import hedge pattern in `validate_swc.py` that
  will be reused for the `import neuron` / `import netpyne` probe. Also the template for the
  "document plan deviation in the Task Requirement Checklist" pattern.
