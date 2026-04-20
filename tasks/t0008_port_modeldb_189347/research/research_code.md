---
spec_version: "1"
task_id: "t0008_port_modeldb_189347"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 7
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-04-20"
status: "complete"
---
# Research Code: Port ModelDB 189347 to NEURON/NetPyNE

## Task Objective

Port the Poleg-Polsky & Rivlin-Etzion 2016 DSGC NEURON model (ModelDB 189347) into this project as a
reusable NetPyNE library asset, reproduce the published 12-angle direction-tuning curve on the
calibrated DSGC morphology, and verify that simulated DSI, peak, null, and HWHM fall inside the
envelope targets defined by the project. The deliverables are one library asset and one answer asset
summarising the port and its biological/numerical fidelity. This document surveys existing project
code, libraries, datasets, and prior lessons so the planning and implementation stages can reuse
maximum prior work and avoid reinventing solutions already validated upstream.

## Library Landscape

Only one library asset is registered in the project at the time of this research, and it is the
library we depend on for scoring.

* **Library**: `tuning_curve_loss` (version 0.1.0) — produced by `[t0012]`. Not overridden by any
  corrections in the corrections overlay. Registered under
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/details.json` with
  8 modules and 14 public entry points. **Relevant**: yes — it is the mandated scorer for the
  reproduced tuning curve and it canonicalises the envelope targets, metric keys, and CSV schema
  this task must emit.
* **Import path**:
  ```python
  from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (
      score, score_curves, load_tuning_curve, TuningCurve, ScoreReport,
      Envelope, DEFAULT_ENVELOPE, DEFAULT_WEIGHTS, ENVELOPE_HALF_WIDTHS,
      TUNING_CURVE_CSV_COLUMNS,
      METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY, METRIC_KEY_RMSE,
  )
  ```

No other libraries exist. SWC parsing code lives in `[t0005]` and `[t0009]` but is not registered as
a library, so per the cross-task reuse rule it must be **copied**, not imported, into this task.

## Key Findings

### NEURON/NetPyNE toolchain is already verified on this Windows host

The NEURON 8.2.7 + NetPyNE 1.1.1 stack is fully installed and validated on this host by `[t0007]`.
The install-report answer asset
(`tasks/t0007_install_neuron_netpyne/assets/answer/neuron-netpyne-install-report/`) documents that
`nrnivmodl` compiles MOD files via a `run_nrnivmodl.cmd` Windows wrapper (MSYS path mangling
workaround), a single-cell Hodgkin-Huxley smoke test produced a ~42 mV spike with 4.4 ms wall-clock
runtime, and the interpreter needs
`os.environ.setdefault("NEURONHOME", r"C:\Users\md1avn\nrn-8.2.7")` before importing NEURON in a
uv-managed venv `[t0007]`. This means the port can assume the compile-run cycle works; no
environment-reinstallation step is needed.

### NetPyNE cell construction template already exists

`tasks/t0007_install_neuron_netpyne/code/sanity_netpyne.py` is a 187-line NetPyNE reference script
that exercises every API this task needs: `specs.NetParams()`, `net_params.cellParams[...]` with
`secs`/`geom`/`mechs`, `popParams` to instantiate a single cell,
`stimSourceParams`/`stimTargetParams` for current injection, `specs.SimConfig()` with
`duration`/`dt`/`hParams`/`recordTraces`/`filename`, and the canonical
`sim.initialize -> createPops -> createCells -> addStims -> setupRecording -> runSim -> gatherData -> saveData`
pipeline `[t0007]`. The DSGC port can adopt this scaffolding verbatim and extend `cellParams` to
load the calibrated DSGC morphology via NetPyNE's `importCell()` HOC/SWC importer and register the
ported MOD mechanisms (HHst, SAC2RGCexc, SAC2RGCinhib, bipolarNMDA, SquareInput).

### Morphology is already calibrated and ready to consume

`[t0005]` downloaded NeuroMorpho.Org #141009_Pair1DSGC (6,736 compartments: 19 soma + 6,717 basal
dendrite, 0 axon, 129 branch points, 131 leaves, 1.54 mm total dendritic length, uniform 0.125 µm
placeholder radius). `[t0009]` then calibrated the radii to Poleg-Polsky 2016 harvested values (soma
4.118 µm, primary 3.694 µm, mid 1.653 µm, terminal 0.439 µm) using a Horton-Strahler partition
(max_order = 5; per-order floors of 0.5 µm for soma/primary and 0.15 µm for terminal) `[t0009]`. The
calibrated SWC keeps the baseline topology exactly, so simply swap the input path from baseline to
calibrated and all downstream code is unchanged.

### Target tuning curve and generator provenance are pinned

`[t0004]` emitted the canonical target curve at
`tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/` as three files:
`curve_mean.csv` (12 angles × mean_rate_hz), `curve_trials.csv` (12 angles × 20 trials × rate_hz),
and `generator_params.json`
(`theta_pref=90°, r_peak=32 Hz, r_base=2 Hz, n_angles=12, n_trials=20, noise_sd=3 Hz, seed`)
`[t0004]`. These paths are hard-coded in the tuning_curve_loss library as `TARGET_MEAN_CSV` and
`TARGET_TRIALS_CSV`, so `score(simulated_curve_csv)` with the default second argument scores the
NEURON output directly against this canonical target `[t0012]`.

### Scoring loss semantics and identity gate

`score_curves(target, candidate, ...)` returns a frozen `ScoreReport` dataclass with `loss_scalar`,
per-axis signed residuals (`dsi_residual`, `peak_residual_hz`, `null_residual_hz`,
`hwhm_residual_deg`), `rmse_vs_target`, `reliability`, `passes_envelope`, `per_target_pass` dict,
normalised residuals (residual divided by envelope half-width), the weights used, and both candidate
and target metric snapshots `[t0012]`. The identity gate is exact:
`score(target, target).loss_scalar == 0.0` and `passes_envelope is True` `[t0012]`. The loss is
`sqrt(sum(w_i * (residual_i / half_width_i)^2))` across the four axes, with
`ENVELOPE_HALF_WIDTHS = {"dsi": 0.1, "peak": 25.0, "null": 5.0, "hwhm": 15.0}` and `DEFAULT_WEIGHTS`
at 0.25 each. 47/47 pytest tests pass, ruff/mypy clean `[t0012]`.

### CSV schemas accepted by the loader

`load_tuning_curve(csv_path=...)` accepts three schemas, checked in this order: canonical 3-column
`(angle_deg, trial_seed, firing_rate_hz)` for per-trial output; t0004 3-column trials
`(angle_deg, trial_index, rate_hz)`; and t0004 2-column mean `(angle_deg, mean_rate_hz)`. All three
require a uniform 30° grid with exactly 12 angles `[t0012]`. The simplest simulator output strategy
is the canonical schema — emit one row per (angle_deg, trial_seed, firing_rate_hz) from the 20-trial
× 12-angle NEURON loop.

### Metric registry keys are fixed

Module-level constants in `scoring.py` name the four registered metrics this task must emit in
`results/metrics.json`: `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
`tuning_curve_reliability`, and `tuning_curve_rmse` `[t0012]`. `ScoreReport.to_metrics_dict()`
returns a dict keyed by these constants — dump it straight into `metrics.json`.

### Existing SWC I/O is the same across t0005 and t0009 — copy the newer version

`[t0005]`'s `validate_swc.py` (236 lines) and `[t0009]`'s `swc_io.py` (215 lines) contain the same
`SwcCompartment` dataclass and SWC round-trip logic. `[t0009]`'s version is the supserset: it adds
`write_swc_file()` and `build_children_index()` and keeps `parse_swc_file()`,
`validate_structure()`, `summarize()`, `SwcSummary`, and explicit type-code constants (`SOMA=1`,
`AXON=2`, `BASAL_DENDRITE=3`, `APICAL_DENDRITE=4`, `ROOT_PARENT_ID=-1`) `[t0009]`. Per the
cross-task rule, this code must be copied — copy the `[t0009]` version directly.

### Environment and command-wrapping invariants

Every task-branch CLI call must be wrapped in `uv run python -m arf.scripts.utils.run_with_logs`
(project rule 1). `[t0007]` established that `nrnivmodl` must be invoked through a plain `.cmd`
wrapper rather than directly from an MSYS/bash shell to avoid MSYS path mangling `[t0007]`. The
Windows-side `PYTHONUTF8=1` and `$HOME/.local/bin` PATH prefix are required across the whole
toolchain to keep NEURON and uv co-operative.

## Reusable Code and Assets

### `tuning_curve_loss` library — **import via library** `[t0012]`

* **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`
  (code at `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/`).
* **What it does**: loads a 12-angle tuning curve CSV, computes DSI/peak/null/HWHM/reliability,
  checks them against the envelope, and scores a candidate against the t0004 target as a weighted
  Euclidean residual in envelope-half-width units.
* **Key signatures**:
  ```python
  def score(
      simulated_curve_csv: Path,
      target_curve_csv: Path | None = None,
      *,
      weights: dict[str, float] | None = None,
      envelope: Envelope | None = None,
      weights_path: Path | None = None,
  ) -> ScoreReport
  def score_curves(
      *,
      target: TuningCurve,
      candidate: TuningCurve,
      weights: dict[str, float] | None = None,
      envelope: Envelope | None = None,
      weights_path: Path | None = None,
  ) -> ScoreReport
  def load_tuning_curve(*, csv_path: Path) -> TuningCurve
  ```
* **Adaptation needed**: none — use as-is.
* **How the asset is located**: read
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/details.json` for
  `module_paths`, `entry_points`, and `dependencies`; the description at `.../description.md` has
  usage examples.

### Target tuning curve dataset — **read the files directly** `[t0004]`

* **Source**: `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/`
* **Files**: `curve_mean.csv`, `curve_trials.csv`, `generator_params.json`.
* **Reuse method**: pass `tuning_curve_loss.score(simulated_curve_csv)` with no explicit target —
  the library resolves `TARGET_MEAN_CSV` to this file automatically.
* **Adaptation needed**: none.

### Calibrated DSGC morphology — **read the SWC directly** `[t0009]`

* **Source**:
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`.
* **What it provides**: 6,736-compartment SWC with Strahler-order-calibrated radii matching
  Poleg-Polsky 2016 bins (soma 4.118 µm, primary 3.694 µm, mid 1.653 µm, terminal 0.439 µm).
* **Reuse method**: pass the path to NetPyNE's `importCell()` (SWC importer) or to NEURON's
  `Import3d_SWC_read`.
* **Adaptation needed**: none — this SWC is the drop-in morphology.

### SWC I/O module — **copy into task** `[t0009]`

* **Source**: `tasks/t0009_calibrate_dendritic_diameters/code/swc_io.py` (~215 lines).
* **What it does**: Provides `SwcCompartment` and `SwcSummary` frozen dataclasses,
  `parse_swc_file(*, swc_path) -> list[SwcCompartment]`, `validate_structure(*, compartments)`,
  `summarize(*, compartments) -> SwcSummary`,
  `build_children_index(*, compartments) -> dict[int, list[int]]`,
  `write_swc_file(*, compartments, output_path, header_comments)`, and the type-code constants
  `SOMA=1`, `AXON=2`, `BASAL_DENDRITE=3`, `APICAL_DENDRITE=4`, `ROOT_PARENT_ID=-1`.
* **Reuse method**: **copy into task** (cross-task rule: non-library code must be copied).
* **Adaptation needed**: none expected for parsing; only extend if the port needs per-compartment
  Strahler order lookup during channel placement.

### NetPyNE sanity template — **copy and extend** `[t0007]`

* **Source**: `tasks/t0007_install_neuron_netpyne/code/sanity_netpyne.py` (187 lines).
* **What it does**: Minimal NEURON+NetPyNE cell-construction pipeline: `specs.NetParams()` with
  `cellParams`/`popParams`/`stimSourceParams`/`stimTargetParams`, `specs.SimConfig()` with
  `duration`/`dt`/`hParams`/`recordTraces`/`filename`, and the
  `sim.initialize -> createPops -> createCells -> addStims -> setupRecording -> runSim -> gatherData -> saveData`
  pipeline.
* **Reuse method**: **copy into task**. Replace the single HH cell with an SWC-imported DSGC, bind
  the ported MOD mechanisms, and add the 177 AMPA + 177 NMDA + 177 GABA synapse populations.
* **Adaptation needed**: swap geometry for `importCell()` on the calibrated SWC, register the ported
  MOD mechanisms under `net_params.mechs`, and drive the simulation with a 12-angle outer loop over
  20 trials each.

### `nrnivmodl` Windows wrapper — **copy into task** `[t0007]`

* **Source**: `tasks/t0007_install_neuron_netpyne/code/run_nrnivmodl.cmd` (7 lines).
* **What it does**: CMD wrapper that invokes `nrnivmodl` without MSYS path mangling.
* **Reuse method**: **copy into task** and run it on the directory containing the ported MOD files
  (HHst, SAC2RGCexc, SAC2RGCinhib, bipolarNMDA, SquareInput, spike) to produce `nrnmech.dll`.
* **Adaptation needed**: adjust the MOD source directory if the task lays files out differently.

### Install-report answer asset — **read only, do not copy** `[t0007]`

* **Source**: `tasks/t0007_install_neuron_netpyne/assets/answer/neuron-netpyne-install-report/`.
* **What it does**: Documents NEURON 8.2.7 + NetPyNE 1.1.1 install paths, `NEURONHOME` env var,
  `nrnivmodl` wrapper usage, and the ~42 mV / 4.4 ms smoke-test baseline.
* **Reuse method**: read during planning to get exact commands and paths; do not copy into the task
  folder.

## Lessons Learned

* **Library scoring has an exact identity gate** — `[t0012]` confirmed `score(target, target)`
  yields `loss_scalar == 0.0` and `passes_envelope is True`. Any non-zero identity loss during port
  implementation signals a pipeline bug (schema mismatch, column swap, or float cast), not a model
  deviation.
* **NEURON on Windows requires a CMD wrapper for `nrnivmodl`** — `[t0007]` hit MSYS path mangling
  when invoking `nrnivmodl` from bash and resolved it by using a plain `.cmd` wrapper. Do not invoke
  `nrnivmodl` directly from the run-with-logs bash wrapper.
* **NEURON import order matters** — `[t0007]` had to set `os.environ["NEURONHOME"]` before
  `import neuron`; otherwise the DLL/`nrnmech` resolution fails on Windows.
* **NEURON 8.2 is stricter about implicit HOC declarations** — the ModelDB 189347 sources documented
  in `research_internet.md` use implicit declarations that break under NEURON 8.2; the port must add
  explicit `objref`/variable declarations at the top of each HOC file it inherits.
* **SWC placeholder radii are biologically meaningless** — `[t0005]` delivered uniform 0.125 µm
  radii; `[t0009]` replaced them with Strahler-calibrated values. Always use the `[t0009]` SWC for
  simulation; the `[t0005]` SWC is only for topology reference.
* **`DEFAULT_WEIGHTS` and `DEFAULT_ENVELOPE` are sufficient defaults** — 47/47 tests pass under them
  `[t0012]`; no need to hand-tune weights for this task unless the envelope envelope check fails
  meaningfully on a first successful port, in which case the loss-scalar breakdown pinpoints which
  of the four axes is drifting.
* **The canonical CSV schema is `(angle_deg, trial_seed, firing_rate_hz)`** — `[t0012]` accepts
  three schemas but the canonical one maps directly onto a per-trial NEURON loop without
  bookkeeping.

## Recommendations for This Task

1. **Import `tuning_curve_loss` directly** from
   `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` and call
   `score(simulated_curve_csv=<path>)` with no explicit target — the library resolves the canonical
   t0004 target for you `[t0012]` `[t0004]`. Dump `ScoreReport.to_metrics_dict()` into
   `results/metrics.json`.
2. **Load the calibrated SWC, not the baseline**, from
   `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`
   via NetPyNE `importCell()` `[t0009]`.
3. **Copy `swc_io.py` from `[t0009]` into this task's `code/`** if per-compartment Strahler-order
   lookup is needed during channel or synapse placement; otherwise NetPyNE's own SWC importer may be
   enough.
4. **Copy `sanity_netpyne.py` from `[t0007]` as the simulator scaffolding** and extend it with the
   SWC import, ported mechanisms, and 177×3 synapse populations `[t0007]`.
5. **Copy `run_nrnivmodl.cmd` from `[t0007]`** and point it at the directory of ported MOD files to
   build `nrnmech.dll` before the first simulation `[t0007]`.
6. **Set `os.environ["NEURONHOME"] = r"C:\Users\md1avn\nrn-8.2.7"` before importing NEURON**, per
   the install-report answer asset `[t0007]`.
7. **Emit simulator output in canonical schema** `(angle_deg, trial_seed, firing_rate_hz)` with 12
   angles × 20 trials and the 30° grid fixed by `tuning_curve_loss.paths` `[t0012]` `[t0004]`.
8. **Gate implementation on the identity check** — before the first run on real NEURON output,
   assert `score(TARGET_MEAN_CSV).loss_scalar == 0.0` to confirm the wiring end-to-end `[t0012]`.
9. **Register the port as a NetPyNE cell-builder library** under `assets/library/` in this task,
   exposing a single `build_dsgc_cell(*, swc_path: Path) -> dict` entry point that returns the
   NetPyNE `cellParams` dict, so downstream tasks can import it without re-copying any code (CLAUDE
   rule 3 & cross-task reuse rule).
10. **Keep all MOD sources and the compiled `nrnmech.dll` inside the task folder** — do not rely on
    any path outside `tasks/t0008_port_modeldb_189347/`; task isolation is rule 3 of CLAUDE.md.

## Task Index

### [t0003]

* **Task ID**: `t0003_simulator_library_survey`
* **Name**: Simulator library survey for the DSGC port
* **Status**: completed
* **Relevance**: answer asset that pins NEURON + NetPyNE as the chosen simulator pair, justifying
  the import surface this task targets.

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate target DSGC tuning curve
* **Status**: completed
* **Relevance**: produces the canonical 12-angle tuning curve dataset (mean + 20 trials) that this
  task's simulator output is scored against via `tuning_curve_loss.score` default target.

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download baseline DSGC morphology
* **Status**: completed
* **Relevance**: provides the upstream NeuroMorpho.Org SWC (141009_Pair1DSGC.CNG.swc) whose topology
  underlies the calibrated morphology this task consumes.

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install NEURON + NetPyNE on Windows host
* **Status**: completed
* **Relevance**: validates the NEURON/NetPyNE toolchain, documents the Windows `nrnivmodl` wrapper
  and `NEURONHOME` requirement, and provides the NetPyNE sanity template to extend.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate DSGC dendritic radii
* **Status**: completed
* **Relevance**: produces the calibrated SWC morphology this task imports into NetPyNE and the
  `swc_io.py` module to copy for any per-compartment topology lookups.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response visualization library
* **Status**: not_started
* **Relevance**: future consumer of this task's simulator output; knowing it exists motivates making
  the NEURON CSV output conform to `tuning_curve_loss`'s canonical schema so t0011 can read it too.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Build tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: provides the only registered library in the project (`tuning_curve_loss`), which
  this task imports to score its reproduced tuning curve and to emit the four registered metrics.
