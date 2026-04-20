---
spec_version: "1"
task_id: "t0010_hunt_missed_dsgc_models"
research_stage: "code"
tasks_reviewed: 15
tasks_cited: 6
libraries_found: 2
libraries_relevant: 2
date_completed: "2026-04-20"
status: "complete"
---
# Research Code: Hunt Missed DSGC Compartmental Models

## Task Objective

This task hunts DSGC compartmental models missed by the initial literature survey [t0002] and the
ModelDB-189347 port [t0008], downloads their papers, and ports any models whose public code runs in
Python 3.12 + NEURON 8.2.7 (or Arbor 0.12.0) and can produce an angle-resolved tuning curve. Every
candidate is recorded in `data/candidates.csv`, every successful port is registered as a library
asset, and every produced tuning curve must be scorable by the canonical t0012 scorer so the answer
asset can present a uniform per-model comparison row. This code-research document enumerates the
reusable surface (import paths, CSV schema, MOD-compile flow, morphology inputs) that every port
attempt in this task MUST conform to.

## Library Landscape

Two library assets are registered in the project, and both are directly relevant to this task. The
library aggregator (`aggregate_libraries.py`) is not present in this worktree's ARF snapshot, so the
landscape was assembled by reading `assets/library/*/details.json` under completed tasks discovered
via `aggregate_tasks.py --status completed`. No library-correction overlays are active for either
asset.

* **Library** `tuning_curve_loss` v0.1.0 — produced by [t0012], registered at
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/details.json`. 14
  entry points. **Relevant**: yes — the mandated scorer that canonicalises the metric keys
  (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`), envelope thresholds, half-widths, and the CSV schema every ported model must
  emit. Import path:
  ```python
  from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (
      score, score_curves, load_tuning_curve, TuningCurve, ScoreReport,
      METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY, METRIC_KEY_RMSE,
      TUNING_CURVE_CSV_COLUMNS, DEFAULT_ENVELOPE, DEFAULT_WEIGHTS, ENVELOPE_HALF_WIDTHS,
  )
  ```
* **Library** `modeldb_189347_dsgc` v0.1.0 — produced by [t0008], registered at
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/details.json`. 5 entry points
  (`build_dsgc`, `run_one_trial`, and three `main` scripts). **Relevant**: yes — the archetype we
  copy when porting any sibling DSGC model (MOD compile flow, nrnmech.dll load,
  Python-driver-over-HOC pattern, 12x20 canonical sweep, identity-gate smoke test). NEVER imported
  across tasks — t0008 code paths are read as a template and functionally equivalent code is
  **copied into** `tasks/t0010_hunt_missed_dsgc_models/code/` (CLAUDE.md rule 3).
* **Third-party dependencies referenced**: `neuron` (>= 8.2.7, validated by [t0007]), `tqdm`,
  `numpy`, `pandas`. No NetPyNE dependency for the port pattern — [t0008] explicitly abandoned
  NetPyNE and fell back to `neuron.h` + `h.load_file`.

Library `tuning-curve-viz` mentioned in the task description is a future deliverable of
`t0011_response_visualization_library`, which has `status: "not_started"`. This means the
side-by-side tuning-curve rendering step cannot be chained inside t0010 and must be deferred to
t0011 in a follow-up.

## Key Findings

### Port Pattern: HOC-First, Python-Driver

[t0008] demonstrates the project's canonical pattern for porting ModelDB NEURON models without
translating their HOC to NetPyNE cellParams. Poleg-Polsky's `RGCmodel.hoc` is bundled verbatim under
`assets/library/modeldb_189347_dsgc/sources/`; a GUI-free derivative `dsgc_model.hoc` strips
`xpanel`/`xbutton` lines so the model runs headless. Python owns only the things HOC cannot cleanly
parameterise: MOD-compile driving (`run_nrnivmodl.cmd`), the `nrn_load_dll` call in
`build_cell.load_neuron()`, spatial rotation of synapse coords for drifting-bar angles, per-trial
seeding via `seed2`, threshold-crossing spike counting above `AP_THRESHOLD_MV=-10`, CSV emission,
and scoring. The [t0008] attempt to wrap the HOC via `netpyne.sim.importCellParams` hit the same
synapse-placement coupling issue as a SWC swap and was abandoned (see [t0008] library description
Dependencies section). Any new DSGC port inside t0010 should start from the same pattern: bundle the
upstream HOC/MOD verbatim under `assets/library/<slug>/sources/`, add a GUI-free derivative if the
upstream has GUI lines, and drive it with a small Python wrapper.

### Canonical 12-Angle x 20-Trial Sweep

Every port in this project emits a tuning curve on the 12-angle x 20-trial grid defined in
`tasks/t0008_port_modeldb_189347/code/constants.py`: `N_ANGLES = 12`, `N_TRIALS = 20`,
`ANGLE_STEP_DEG = 30.0`, covering angles 0, 30, 60, ..., 330 deg. Per-trial seeds are `1..20`. The
driver at `tasks/t0008_port_modeldb_189347/code/run_tuning_curve.py` (96 lines) builds the cell
once, snapshots baseline synapse coords via `read_synapse_coords(h)`, and then iterates a 240-row
nested loop calling `run_one_trial(h=h, angle_deg=..., seed=..., baseline_coords=...)` which returns
a firing rate in Hz. Grid constants are also mirrored inside
`tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/paths.py` (`N_ANGLES=12`,
`ANGLE_STEP_DEG=30.0`). The loader at [t0012]'s `loader.py:_validate_angle_grid` HARD-FAILS on
non-uniform or non-12-angle grids (`ValueError("Expected 12 unique angles; got N")`), so any port
producing a different grid is rejected at scoring time.

### Canonical CSV Schema

The tuning-curve CSV schema is fixed as three columns `(angle_deg, trial_seed, firing_rate_hz)`,
constant `TUNING_CURVE_CSV_COLUMNS` in `tuning_curve_loss/paths.py`. [t0008] emits 240 rows per
sweep to `data/tuning_curves/curve_modeldb_189347.csv` using `csv.writer` with header row
`angle_deg,trial_seed,firing_rate_hz` and integer angles (`int(angle_deg)`), integer seeds, and rate
floats formatted `f"{rate_hz:.6f}"`. The [t0012] `load_tuning_curve` function auto-detects three
schemas: the canonical trials schema, the legacy t0004 `(angle_deg, trial_index, rate_hz)` trials
schema, and the t0004 two-column `(angle_deg, mean_rate_hz)` mean schema. Any new port in t0010 MUST
emit the canonical trials schema; there is no second registered writer.

### MOD-Compile Flow on Windows

[t0008] compiles the six ModelDB 189347 MOD files (`HHst.mod`, `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`,
`SquareInput.mod`, `bipolarNMDA.mod`, `spike.mod`) into a Windows `nrnmech.dll` via
`code/run_nrnivmodl.cmd` (23 lines). The script takes two positional args: MOD source directory and
build directory, both absolute paths; creates the build dir if missing; `pushd`es into it (NEURON
emits `nrnmech.dll` into the `cwd`); then calls NEURON's own
`C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat "%MODDIR%"` wrapper. The `NEURONHOME` environment
variable defaults to `C:\Users\md1avn\nrn-8.2.7` and is set via
`os.environ.setdefault("NEURONHOME", NEURONHOME_DEFAULT)` in `constants.py`. The produced DLL is
discovered by `build_cell._nrnmech_dll_path()` which expects exactly `build/<slug>/nrnmech.dll`; the
[t0008] `paths.MODELDB_NRNMECH_GLOBS` list also catalogues Linux/macOS alternatives
(`x86_64/.libs/libnrnmech.so`, `x86_64/libnrnmech.so`) for future portability but the codepath today
is Windows-only.

### Identity-Gate Invariant and Scoring Contract

Every scoring consumer must honour [t0012]'s **REQ-7 identity invariant**: calling
`score(simulated_curve_csv=TARGET_MEAN_CSV)` must return exactly `loss_scalar == 0.0` and
`passes_envelope is True`. [t0008] enforces this by `test_scoring_pipeline.test_identity` (37 lines)
which is a small gate script that asserts both conditions before trusting the reported loss for the
port's actual tuning curve. The identity gate catches broken scorer wiring (wrong target path, wrong
schema, wrong weights normalisation) before the sweep runs and burns 10-15 minutes of wall-clock.
The [t0012] scorer also exposes a `ScoreReport.to_metrics_dict()` method that returns the four
registered metric keys, which [t0008] feeds directly into `results/metrics.json`.

### NEURON Install and Environment Quirks

[t0007] validated NEURON 8.2.7 and NetPyNE 1.1.1 on the Windows workstation at
`C:\Users\md1avn\nrn-8.2.7`. The answer asset `neuron-netpyne-install-report` records the working
`nrnivmodl.bat` path, the 1-compartment HH sanity simulation, and the required env var `NEURONHOME`.
Two Windows-specific gotchas documented in [t0008]: (1) NEURON's HOC parser treats backslashes as
escape sequences, so HOC path literals MUST use forward slashes — [t0008] has a helper
`_sources_dir_hoc_safe()` that returns `str(path).replace("\\", "/")`; (2) NEURON does not
auto-source `stdrun.hoc` when skipping `nrngui.hoc`, so `run()`, `finitialize()`, `continuerun()`,
and `v_init` are unavailable without an explicit `h.load_file("stdrun.hoc")`. Both gotchas must be
carried into any new t0010 port.

### Morphology: Calibrated SWC Available But Often Not Usable

[t0009] produced `dsgc-baseline-morphology-calibrated` (dataset asset, not a library), the
Horton-Strahler-diameter-calibrated version of the Feller-lab 141009_Pair1DSGC reconstruction at
`tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/ files/141009_Pair1DSGC_calibrated.CNG.swc`.
It is 6,736 compartments (19 soma + 6,717 dend), 129 branches, 131 leaves, 1,536.25 um total
dendritic length, with four Strahler-order radii (soma 4.118 um, primary 3.694 um, mid 1.653 um,
terminal 0.439 um). [t0008]'s morphology swap was deferred because `RGCmodel.hoc`'s
`placeBIP`-driven synapse placement is coupled to the bundled section ordering and the z/y ON/OFF
cut, so swapping the SWC would have required rewriting `placeBIP` — out of plan envelope. For any
new port found in t0010 whose upstream **does** accept an external SWC (e.g., a model that builds
via `h.Import3d_SWC_read`), the calibrated SWC can be fed in; for models with bundled-topology
lock-in like Poleg-Polsky, the upstream morphology should be bundled verbatim.

### SWC I/O Utilities (Stdlib, No Dependencies)

[t0008] contains `code/swc_io.py` (216 lines), itself copied-and-adapted from t0005 per the rule-3
no-cross-task-imports policy. It exposes `parse_swc_file(*, swc_path)` -> list of `SwcCompartment`
dataclasses, `validate_structure(*, compartments)` that raises on missing parents / negative radii /
<100 dendritic compartments, `summarize(*, compartments)` -> `SwcSummary` (counts +
branch/leaf/total dendritic length), `build_children_index(*, compartments)` ->
`dict[int, list[int]]`, and `write_swc_file(*, compartments, output_path, header_comments)`. Pure
stdlib, no dependencies. Ported t0010 models that accept external SWCs should **copy** this module
rather than re-implement SWC parsing.

### Tests and Smoke Gates

[t0008] has two gate scripts that any new port should mirror. (1) `code/test_smoke_single_angle.py`
(83 lines) builds the cell, runs one preferred-direction trial with `seed=1`, asserts the soma
firing rate is strictly positive, and writes a one-row canonical-schema CSV. The threshold is
tolerant (`SMOKE_TEST_MIN_FIRING_HZ = 0.0`, constants.py) — its purpose is to catch a broken MOD
compile / DLL load / dt mis-set, not to enforce the envelope. (2) `code/test_scoring_pipeline.py`
(37 lines) is the identity-gate described above. Both scripts exit nonzero on failure. They run in
well under a minute each and should be executed before the 10-15 minute full sweep so wall-clock is
not wasted on a broken pipeline.

## Reusable Code and Assets

All cross-task code reuse in this task is **copy into task** because CLAUDE.md rule 3 forbids
imports from other tasks' `code/` directories; only library imports are allowed. The two library
imports below come from registered `assets/library/` entries.

### Import via library

1. **`tuning_curve_loss.score()`** — **import via library**
   * **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`
   * **What it does**: CSV -> `ScoreReport`. Loads a simulated-curve CSV and the canonical t0004
     target, computes DSI, peak, null, HWHM, residuals, normalised residuals, weighted Euclidean
     loss, pass-per-target envelope flags, RMSE, and reliability; returns a frozen dataclass.
   * **Signature**:
     ```python
     def score(
         simulated_curve_csv: Path,
         target_curve_csv: Path | None = None,
         *,
         weights: dict[str, float] | None = None,
         envelope: Envelope | None = None,
         weights_path: Path | None = None,
     ) -> ScoreReport
     ```
   * **Identity-gate invariant**: `score(simulated_curve_csv=TARGET_MEAN_CSV).loss_scalar == 0.0`
     AND `passes_envelope is True`. Every port must run this gate before trusting its own loss.
   * **Envelope defaults (from `envelope.py`)**: `DSI_ENVELOPE=(0.7, 0.9)`,
     `PEAK_ENVELOPE_HZ=(30.0, 80.0)`, `NULL_ENVELOPE_HZ=(0.0, 10.0)`,
     `HWHM_ENVELOPE_DEG=(60.0, 90.0)`.
   * **Metric-key constants**: `METRIC_KEY_DSI`, `METRIC_KEY_HWHM`, `METRIC_KEY_RELIABILITY`,
     `METRIC_KEY_RMSE` — must be imported and used as the only keys in `results/metrics.json`.
   * **Adaptation needed**: none. Feed the simulated CSV path directly.

2. **`tuning_curve_loss.TUNING_CURVE_CSV_COLUMNS`** — **import via library**
   * **Source**: same library, `paths.py`.
   * **What it does**: tuple `("angle_deg", "trial_seed", "firing_rate_hz")`. Use as the
     `csv.writer` header row when emitting a port's sweep output.
   * **Adaptation needed**: none.

### Copy into task

3. **Windows MOD-compile wrapper** — **copy into task**
   * **Source**: `tasks/t0008_port_modeldb_189347/code/run_nrnivmodl.cmd` (23 lines)
   * **What it does**: parametrised `.cmd` wrapper around NEURON's `nrnivmodl.bat`. Args: MOD source
     dir, build dir (both absolute). Creates build dir, `pushd`es into it, invokes
     `C:\Users\md1avn\nrn-8.2.7\bin\nrnivmodl.bat`, returns exit code.
   * **Adaptation needed**: none; parametrised to be reused for any per-port MOD directory.
   * **Line count**: 23.

4. **`build_cell.load_neuron()` + `build_cell._nrnmech_dll_path()` pattern** — **copy into task**
   * **Source**: `tasks/t0008_port_modeldb_189347/code/build_cell.py:86-117` (32 lines including
     helpers)
   * **What it does**: sets `NEURONHOME`, imports `from neuron import h`, asserts
     `h.nrn_load_dll(<per-port-dll>) == 1.0`, sources `stdrun.hoc`, guards idempotence via a
     module-level `_loaded` flag.
   * **Adaptation needed**: repoint the DLL path to the per-port build dir (e.g.
     `tasks/t0010_.../build/<slug>/nrnmech.dll`).
   * **Line count**: 32 helper + constants. Copy whole `build_cell.py` (359 lines) if the port
     follows the Poleg-Polsky spatial-rotation pattern; otherwise keep only the load/dll helpers.

5. **12-angle x 20-trial sweep driver** — **copy into task**
   * **Source**: `tasks/t0008_port_modeldb_189347/code/run_tuning_curve.py` (96 lines)
   * **What it does**: nested loop over `N_ANGLES * N_TRIALS`, calls `run_one_trial` per cell,
     accumulates `(int(angle_deg), seed, rate)` rows, writes canonical CSV.
   * **Adaptation needed**: replace `build_dsgc()` and `run_one_trial()` with the per-port
     equivalents; update output path constant.
   * **Line count**: 96.

6. **Envelope-scoring wiring** — **copy into task**
   * **Source**: `tasks/t0008_port_modeldb_189347/code/score_envelope.py` (102 lines)
   * **What it does**: loads the emitted CSV, calls `tuning_curve_loss.score`, writes full
     `ScoreReport` dump to `data/score_report.json`, writes registered-metric keys to
     `results/metrics.json`.
   * **Adaptation needed**: repoint CSV and report paths per port. Library import does not change.
   * **Line count**: 102.

7. **Smoke-test single-angle gate** — **copy into task**
   * **Source**: `tasks/t0008_port_modeldb_189347/code/test_smoke_single_angle.py` (83 lines)
   * **What it does**: builds the cell, runs one trial at `angle_deg=0.0, seed=1`, asserts the rate
     \> `SMOKE_TEST_MIN_FIRING_HZ`, emits a one-row canonical-schema CSV.
   * **Adaptation needed**: repoint build and paths to the per-port entries.
   * **Line count**: 83.

8. **Identity-gate scoring test** — **copy into task**
   * **Source**: `tasks/t0008_port_modeldb_189347/code/test_scoring_pipeline.py` (37 lines)
   * **What it does**: calls `score(TARGET_MEAN_CSV, TARGET_MEAN_CSV)` and asserts
     `loss_scalar == 0.0` and `rmse_vs_target == 0.0`. Catches broken scoring wiring before the full
     sweep.
   * **Adaptation needed**: none; the test is already library-centric.
   * **Line count**: 37.

9. **SWC reader/writer utilities** — **copy into task** (only if porting a model that accepts
   external SWC)
   * **Source**: `tasks/t0008_port_modeldb_189347/code/swc_io.py` (216 lines)
   * **What it does**: `parse_swc_file`, `validate_structure`, `summarize`, `build_children_index`,
     `write_swc_file`. Pure stdlib.
   * **Adaptation needed**: none.
   * **Line count**: 216.

10. **Calibrated DSGC morphology** — **dataset asset (no copy; reference by path)**
    * **Source**:
      `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/ dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`
    * **What it does**: 6,736-compartment diameter-calibrated DSGC SWC for models that accept
      external morphology. Four Strahler-order radii from Poleg-Polsky 2016.
    * **Adaptation needed**: absolute path via `paths.CALIBRATED_SWC_PATH`-style constant.
    * **Line count**: N/A (dataset asset, not code).

## Lessons Learned

**[t0008] port attempt produced a technically faithful but envelope-missing reproduction.** The
Poleg-Polsky port had DSI 0.316 (target 0.70-0.85) and peak 18.1 Hz (target 40-80 Hz). The diagnosed
cause was a **protocol mismatch**, not a port bug: Poleg-Polsky 2016 imposes DS via a per-angle
`gabaMOD` parameter swap, while [t0008] applied a spatial-rotation proxy on BIPsyn coords. Takeaway:
reading the paper's Methods section is mandatory before choosing the port's stimulus protocol —
matching the HOC's stimulus proc API is not enough if the paper drives direction selectivity via
parameter swaps instead of spatial geometry.

**Bundled morphology is often topologically coupled to synapse placement.** [t0008] tried to swap in
the t0009 calibrated SWC but found `placeBIP` walked bundled section indices; the swap was deferred
as a downstream suggestion. Takeaway: do not promise a calibrated-SWC swap in the port plan unless
the upstream HOC/Python builds its synapse layout from geometric rules rather than section ordering.

**NetPyNE `importCellParams` does not generalise over HOC DSGC templates.** Both the SWC swap and
the NetPyNE wrap attempts in [t0008] hit the same coupling issue. Pure `from neuron import h`
driving is both simpler and more faithful.

**10-15 minute sweep wall-clock makes upstream gating essential.** The full 240-trial sweep in
[t0008] takes 10-15 minutes on the project workstation. Every minute spent on a broken pipeline
compounds. The smoke-test and identity-gate pattern from [t0008] (two small scripts, each under a
minute) should run before every sweep attempt in t0010.

**The `project envelope widening is explicit and documented` lesson from [t0012] applies.** [t0012]
widened the literature envelope from `DSI (0.7, 0.85)` to `(0.7, 0.9)` and `peak (40, 80)` to
`(30, 80)` so the t0004 canonical target passes the envelope. Any t0010 port that misses these
widened bounds is a stronger failure than previously believed.

## Recommendations for This Task

1. **Follow the [t0008] port archetype for any candidate found.** Bundle upstream HOC/MOD verbatim
   under `tasks/t0010_.../assets/library/<slug>/sources/`. Add a GUI-free derivative HOC if
   necessary. Copy the eight reusable modules listed in Reusable Code above. Import `score` and
   `TUNING_CURVE_CSV_COLUMNS` from the `tuning_curve_loss` library.

2. **Refuse to port any candidate whose upstream cannot produce an angle-resolved tuning curve.**
   The task's inclusion bar already states this. The first reason a candidate should be marked "not
   ported" in `data/candidates.csv` is: "upstream produces only single-direction voltage traces; no
   stimulus geometry for angular sweep".

3. **Run the identity gate and the single-angle smoke test before every per-port sweep.** Both gates
   are under-a-minute; a failed gate means the sweep's 10-15 minute cost is avoided. Store their
   stdout/stderr under `tasks/t0010_.../logs/` per CLAUDE.md rule 4 and the task's Approach section.

4. **Emit every sweep's CSV using the canonical schema `(angle_deg, trial_seed, firing_rate_hz)`.**
   Use `TUNING_CURVE_CSV_COLUMNS` from the library as the header row. Write under
   `data/tuning_curves/curve_<model-slug>.csv`. The [t0012] loader will reject anything else.

5. **Record every outcome in `data/candidates.csv`.** For each candidate: paper DOI, code URL,
   NEURON compatibility (yes/no), port attempted (yes/no), port outcome (ported / failed-with-
   reason / not-attempted-with-reason), and if ported, DSI + peak + null + HWHM + passes-envelope.
   Rows are atomic; do not produce the answer asset's table without this CSV.

6. **Register every successful port as a library asset.** The folder must be
   `tasks/t0010_hunt_missed_dsgc_models/assets/library/<model-slug>/` with `details.json` v2,
   `description.md`, and a `sources/` subfolder holding the upstream code verbatim. Follow the
   [t0008] `modeldb_189347_dsgc` asset as the template.

7. **Score every port with the t0012 library and write `results/metrics.json` using the four library
   metric-key constants only.** Do not invent new metric keys inside this task.

8. **Defer the multi-model overlay figure to [t0011].** The `tuning-curve-viz` library is a future
   deliverable. [t0011] is `status: "not_started"` in the task aggregator, so t0010 cannot chain it.
   Emit all per-port CSVs in the canonical schema under `data/tuning_curves/` so [t0011] can pick
   them up later without rework.

9. **Do not swap in the t0009 calibrated SWC unless the candidate's upstream explicitly supports
   external SWC.** Bundled-topology upstreams (Poleg-Polsky-style) are too coupled to
   `placeBIP`-style synapse-placement procs; leave morphology untouched. Only feed the calibrated
   SWC to candidates that use `h.Import3d_SWC_read` or an equivalent geometric loader.

10. **Stop at 3-5 ports.** The task description's fallback section caps scope at 3-5 ports; further
    candidates are logged as suggestions. Prioritise by (a) citation count, (b) publication year
    (newer first), (c) simulator already on the workstation (NEURON beats Arbor beats NEST).

## Conformance Checklist

For any candidate model a port-attempt agent must produce:

* [ ] **(a) Registered library asset** at
  `tasks/t0010_hunt_missed_dsgc_models/assets/library/<model-slug>/` containing `details.json` (spec
  v2), `description.md`, a `sources/` subfolder with the upstream code verbatim, `module_paths`
  listing copied-into-task modules under
  `tasks/t0010_hunt_missed_dsgc_models/code/<model-slug>_*.py`, and at least one entry point (the
  sweep driver or the build function).

* [ ] **(b) Tuning-curve CSV** at
  `tasks/t0010_hunt_missed_dsgc_models/data/tuning_curves/curve_<model-slug>.csv` with:
  * canonical columns `(angle_deg, trial_seed, firing_rate_hz)` via `TUNING_CURVE_CSV_COLUMNS` — no
    other schema accepted by [t0012] `load_tuning_curve`;
  * exactly `N_ANGLES * N_TRIALS = 12 * 20 = 240` rows;
  * integer `angle_deg` and `trial_seed`, float `firing_rate_hz` formatted `f"{rate:.6f}"`;
  * same number of trials per angle (the loader rejects inconsistent trial counts).

* [ ] **(c) Envelope scoring via the t0012 library**, with the documented identity gate checked
  first:
  * call
    `tuning_curve_loss.score(simulated_curve_csv=TARGET_MEAN_CSV, target_curve_csv= TARGET_MEAN_CSV)`
    and assert `loss_scalar == 0.0` AND `passes_envelope is True` (copy from
    `tasks/t0008_port_modeldb_189347/code/test_scoring_pipeline.py`);
  * then call `score(simulated_curve_csv=<port CSV>)` and dump `ScoreReport` to
    `data/score_report_<model-slug>.json`;
  * write the four registered keys (`METRIC_KEY_DSI`, `METRIC_KEY_HWHM`, `METRIC_KEY_RELIABILITY`,
    `METRIC_KEY_RMSE`) into a per-port metrics JSON (or the task's `results/metrics.json` if the
    task has a single ported model).

* [ ] **(d) Row in `data/candidates.csv`** (task-description-mandated file) with columns recording:
  `paper_doi`, `code_url`, `neuron_compatible` (bool), `port_attempted` (bool), `port_outcome`
  (`ported` / `failed-<reason>` / `not_attempted-<reason>`), and if ported, the four envelope axes
  (`dsi`, `peak_hz`, `null_hz`, `hwhm_deg`) plus `passes_envelope`. Every candidate found in any
  search pass (ModelDB / GitHub / Scholar / bioRxiv) gets a row, including those excluded for
  not-compartmental or upstream-dead reasons.

## Task Index

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: compartmental models of DS retinal ganglion cells
* **Status**: completed
* **Relevance**: the survey whose gap this task closes; provides the seed-paper list (Poleg-Polsky,
  Schachter, Park, Sethuramanujam, Hanson) for forward-citation chains and establishes the project's
  corpus of 20 papers that any new candidate must be deduplicated against.

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain
* **Status**: completed
* **Relevance**: validates the Windows 11 workstation NEURON install at `C:\Users\md1avn\nrn-8.2.7`,
  provides the `run_nrnivmodl.cmd` wrapper pattern, and the `NEURONHOME` env-var / `nrnivmodl.bat`
  path used by every port in this task.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: the archetype port. Supplies the HOC-first Python-driver pattern, the canonical
  12x20 sweep driver, the MOD-compile wrapper, the `nrnmech.dll` load helper, the smoke-test and
  identity-gate scripts, and the library-asset layout that every new t0010 port must mirror.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: completed
* **Relevance**: source of the calibrated 6,736-compartment DSGC SWC
  (`dsgc-baseline-morphology-calibrated`) that t0010 can feed into any ported model that accepts an
  external morphology.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: not_started
* **Relevance**: planned consumer of t0010's per-port tuning-curve CSVs. Because t0011 is not yet
  started, the side-by-side rendering step cannot be chained from t0010; the per-port CSVs must
  conform to the canonical schema so t0011 can pick them up later without rework.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: the mandated scoring library. Supplies the `score()` entry point, the four
  registered metric-key constants, the canonical CSV schema constant, the envelope defaults, and the
  identity-gate invariant that every t0010 port must honour.
