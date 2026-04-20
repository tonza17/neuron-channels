---
spec_version: "2"
task_id: "t0008_port_modeldb_189347"
date_completed: "2026-04-20"
status: "complete"
---
# Plan — t0008 Port ModelDB 189347 and Hunt Sibling DSGC Compartmental Models

## Objective

Port ModelDB entry 189347 (Poleg-Polsky & Diamond 2016, ON-OFF DRD4 DSGC NEURON model with 177 AMPA
+ 177 NMDA + 177 GABA synapses and Jahr-Stevens NMDA multiplicative gain) into this project as a
  registered library asset, swap its bundled morphology for the t0009 Strahler-calibrated DSGC SWC,
  run a 12-angle × 20-trial drifting-bar tuning curve on the local Windows workstation (NEURON 8.2.7
+ NetPyNE 1.1.1, `dt = 0.1 ms`, `tstop = 1000 ms`, bar speed 500 µm/s), and score the result with
  the `tuning_curve_loss` library from t0012 against the project envelope (DSI 0.7-0.85, peak 40-80
  Hz, null < 10 Hz, HWHM 60-90°). Then survey sibling DSGC compartmental models (Hanson 2019
  `geoffder/Spatial-Offset-DSGC-NEURON-Model` as the primary Phase B target; Jain 2020, Ding 2016,
  Schachter 2010, Koren 2017, Ezra-Tsur 2022 as documented candidates) and record results in an
  answer asset. "Done" means: (1) one registered library asset `modeldb_189347_dsgc` with compiled
  MOD files, a NetPyNE cell builder, and a smoke-test; (2) one registered answer asset
  `dsgc-modeldb-port-reproduction-report` containing the Phase A envelope verification table and the
  Phase B survey; (3) `results/metrics.json` carries the four registered metrics
  (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`) emitted by the scoring library; (4) all CLI calls are wrapped in
  `run_with_logs.py`.

## Task Requirement Checklist

Task text (quoted verbatim from `tasks/t0008_port_modeldb_189347/task.json` short description and
`task_description.md`):

> Port ModelDB 189347 (Poleg-Polsky 2016) as a library asset, reproduce the published tuning curve,
> verify envelope targets, and port any sibling DSGC compartmental models found along the way.
>
> ### Phase A — Port the Poleg-Polsky 2016 baseline

> 1. Download ModelDB entry 189347 and register the resulting Python package under
>    `assets/library/dsgc-polegpolsky-2016/` with a description, module paths, test paths, and a
>    smoke-test that instantiates the model and runs a single angle.
> 2. Swap in the calibrated morphology produced by t0009 (`dsgc-baseline-morphology-calibrated`) in
>    place of the ModelDB-bundled morphology. Document the swap and any geometric differences
>    (compartment count, dendritic path length, branch points) vs the original ModelDB morphology.
> 3. Run the published stimulus: drifting bar / moving spot at 12 angles (30° spacing), synaptic
>    configuration matching the paper, Poleg-Polsky NMDA parameters.
> 4. Compute the simulated tuning curve (firing rate vs angle, 20 trials per angle with fresh seeds)
>    and score it with the t0012 scoring loss library against the envelope: DSI 0.7-0.85, preferred
>    peak 40-80 Hz, null residual < 10 Hz, HWHM 60-90°.
>
> ### Phase B — Hunt for sibling DSGC compartmental models

> 5. Search ModelDB, SenseLab, OSF, and GitHub for additional DSGC compartmental models cited or
>    adjacent in the literature (Schachter2010 derivatives, Briggman-lineage forks, 2017-2025
>    updates of the Poleg-Polsky model, any post-2020 published code).
> 6. For each model found, record: source URL, NEURON compatibility, morphology it ships with,
>    synaptic configuration, and whether it runs out-of-the-box in this environment.
> 7. Port any model that has public code and runs cleanly as a separate library asset under
>    `assets/library/<model-slug>/`. If a model fails to run, record the failure in the Phase B
>    answer asset and do not register a broken library.

Requirement decomposition:

* **REQ-1** — Download ModelDB 189347 from `github.com/ModelDBRepository/189347` into the library
  asset folder and compile its MOD files with `nrnivmodl`. Evidence: the archive files (`main.hoc`,
  `RGCmodel.hoc`, 6 `.mod` files plus `spike.mod`, `mosinit.hoc`) exist under
  `assets/library/modeldb_189347_dsgc/sources/` and `nrnmech.dll` exists under `build/` in the task
  folder. Commit SHA of the ModelDBRepository checkout is recorded in `details.json`
  `long_description` and in `build_log.txt`. Satisfied by steps 1, 2.
* **REQ-2** — Register `modeldb_189347_dsgc` as a library asset under
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/` with `details.json`
  (spec_version "2", module_paths, entry_points, dependencies, test_paths, categories) and
  `description.md` containing all 8 mandatory sections. Evidence: the library verificator passes for
  this asset folder. Satisfied by step 6.
* **REQ-3** — Provide a smoke-test script that instantiates the ported model and runs a single angle
  (PD) successfully. Evidence: `code/test_smoke_single_angle.py` runs with exit code 0 and produces
  one CSV row `(angle_deg=0, trial_seed=0, firing_rate_hz>0)`. Satisfied by step 5.
* **REQ-4** — Swap in `dsgc-baseline-morphology-calibrated` (from t0009:
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`)
  in place of the ModelDB-bundled morphology. Evidence: `code/build_cell.py` imports the calibrated
  SWC via NetPyNE `importCell`, and a geometry report at `data/morphology_swap_report.md` records
  compartment count, dendritic path length, and branch points for both morphologies. Satisfied by
  steps 4, 7.
* **REQ-5** — Document geometric differences (compartment count, dendritic path length, branch
  points) between the ModelDB-bundled morphology (1 soma + 350 dendrite sections per
  `research_internet.md`) and the calibrated morphology (6,736 compartments per `research_code.md`).
  Evidence: a comparison table appears in `data/morphology_swap_report.md` and is copied into the
  answer asset's full answer document. Satisfied by step 7.
* **REQ-6** — [CRITICAL] Run the published stimulus — a drifting bar — at 12 angles (30° spacing,
  angles 0, 30, ..., 330°). Evidence: `data/tuning_curves/curve_modeldb_189347.csv` has exactly 12 ×
  20 = 240 rows in canonical schema `(angle_deg, trial_seed, firing_rate_hz)`. Satisfied by step 8.
* **REQ-7** — [CRITICAL] Match the paper's synaptic configuration (177 AMPA + 177 NMDA + 177 GABA,
  passive dendrites, Jahr-Stevens NMDA Mg²⁺ block, `tau1NMDA_bipNMDA = 60 ms`,
  `e_SACinhib = -60 mV`) and Poleg-Polsky NMDA parameters as laid down in
  `ModelDBRepository/189347/main.hoc`. Evidence: the HOC parameters are read verbatim from the
  cloned archive, recorded in `code/constants.py`, and asserted identical to the source at build
  time. No architectural modifications are introduced. Satisfied by steps 3, 8.
* **REQ-8** — 20 trials per angle with fresh random seeds. Evidence: trial seeds `0, 1, ..., 19`
  appear in the tuning-curve CSV for each of the 12 angles, and `code/run_tuning_curve.py` uses
  `h.use_mcell_ran4(1); h.mcell_ran4_init(12 * trial + angle_index)` to seed each run independently.
  Satisfied by step 8.
* **REQ-9** — Score the tuning curve with the `tuning_curve_loss` library from t0012 against the
  envelope (DSI 0.7-0.85, peak 40-80 Hz, null < 10 Hz, HWHM 60-90°) and record DSI, peak, null, HWHM
  in the answer asset's verification table. Evidence: `results/metrics.json` contains the four
  registered metrics populated from `ScoreReport.to_metrics_dict()`, and
  `assets/answer/dsgc-modeldb-port-reproduction-report/full_answer.md` contains the verification
  table with numeric values and per-target pass/fail flags. Satisfied by steps 9, 10.
* **REQ-10** — Search ModelDB, SenseLab, OSF, and GitHub for additional DSGC compartmental models
  (Schachter 2010, Briggman-lineage/Ding 2016, post-2016 Poleg-Polsky updates, 2017-2025 published
  DSGC NEURON code). Evidence: the answer asset's full document includes a survey table whose rows
  are drawn from `research_internet.md` findings plus up to 3 additional targeted searches during
  implementation (recorded in logs). Satisfied by step 11.
* **REQ-11** — For each sibling model record source URL, NEURON compatibility, morphology it ships
  with, synaptic configuration, and whether it runs out-of-the-box. Evidence: the answer asset's
  full document has a 5-column survey table covering all candidates in `research_internet.md`
  (Poleg-Polsky 2016, Hanson 2019, Jain 2020, Ding 2016, Schachter 2010, Koren 2017, Ezra-Tsur 2022)
  with the required fields populated. Satisfied by step 11.
* **REQ-12** — Port the Hanson 2019 fork (`geoffder/Spatial-Offset-DSGC-NEURON-Model`) as a separate
  library asset if it compiles and runs a single angle successfully; if it fails, record the failure
  in the answer asset and do not register a broken library. Evidence: either (a) a second library
  asset `hanson_2019_spatial_offset_dsgc` exists with `details.json` and passing smoke test, or (b)
  `assets/answer/dsgc-modeldb-port-reproduction-report/full_answer.md` contains a "Port attempt" row
  for Hanson 2019 with a specific failure reason. Satisfied by step 12.
* **REQ-13** — All task-branch CLI calls are wrapped in
  `uv run python -m arf.scripts.utils.run_with_logs`. Evidence: `logs/steps/*/run_log.txt` captures
  every wrapped invocation; no `nrnivmodl`, `git`, or `uv` call is made outside this wrapper.
  Satisfied by every step.
* **REQ-14** — Budget stays at $0.00 (local only, no remote machines, no paid APIs). Evidence:
  `results/costs.json` shows `{"total_cost_usd": 0.0}` and no entry in `logs/steps/` invokes any
  paid service. Satisfied by every step.
* **REQ-15** — Produce a simulated tuning-curve CSV under `data/tuning_curves/` in canonical schema
  for later consumption by t0011 (response visualization library). Evidence:
  `data/tuning_curves/curve_modeldb_189347.csv` exists with columns
  `angle_deg, trial_seed, firing_rate_hz`; if Hanson 2019 is successfully ported, a second CSV
  `curve_hanson_2019.csv` exists. Satisfied by steps 8, 12.
* **REQ-16** — Register one answer asset summarising Phase A envelope verification + Phase B survey,
  per `meta/asset_types/answer/specification.md`. Evidence: the answer asset's canonical short and
  full answer documents exist and the answer verificator passes. Satisfied by step 13.

## Approach

**Task types (from `task.json`)**: `code-reproduction` (primary) and `write-library` (secondary).
The `code-reproduction` guidelines say "reproduce means running the original process from scratch" —
so Phase A must actually simulate on NEURON 8.2.7 with the real ModelDB archive, not replay stored
outputs, and the tuning-curve step is marked `[CRITICAL]`. The `write-library` guidelines drive the
public-API design: the port's entry point is `build_dsgc_cell(*, swc_path: Path) -> dict` returning
a NetPyNE cellParams dict so downstream tasks (morphology sweep S-0002-04, E/I scan S-0002-05,
active-dendrite RQ4) can import and configure the cell without touching HOC.

**Phase A execution strategy** (grounded in research findings):

1. **Port verbatim first, swap morphology second.** Per `research_papers.md` methodology insight and
   `research_code.md` recommendation 4: clone `github.com/ModelDBRepository/189347` at a pinned
   commit, compile the 6 MOD files (`HHst.mod`, `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`,
   `bipolarNMDA.mod`, `SquareInput.mod`, `spike.mod`) with `nrnivmodl` via the t0007 CMD wrapper
   (MSYS path mangling workaround), and run the shipped `main.hoc` smoke-test on the bundled
   morphology to confirm the port is intact before any morphology swap. This isolates port-breakage
   bugs from morphology-induced envelope shifts.
2. **Use the paper's canonical parameters from `main.hoc`, not the paper prose.** Per
   `research_internet.md` finding 1 and recommendation 5: `tstop = 1000 ms`, `dt = 0.1 ms`,
   `tau1NMDA_bipNMDA = 60 ms`, `e_SACinhib = -60 mV`, bar speed = 1 µm/ms (= 1 mm/s = 1000 µm/s —
   note the task description says 500 µm/s; we follow the ModelDB canonical value and document the
   discrepancy in the answer asset). The PMC manuscript XML truncates Experimental Procedures, so
   the HOC is canonical.
3. **Wrap HOC in NetPyNE via `importCell`.** Per `research_internet.md` finding 6: disable
   `mosinit.hoc` GUI auto-launch by loading `main.hoc` (or a GUI-free derivative `dsgc_model.hoc`)
   directly, wrap as a HOC template with named section lists covering soma + all 350 dendrite
   sections, then call `importCell(fileName="dsgc_model.hoc", cellName="RGC")` inside a NetPyNE
   `cellParams` builder. Reset `h.celsius` after import per NetPyNE issue #31.
4. **Swap morphology via the NetPyNE SWC importer.** Load the t0009 calibrated SWC
   (`141009_Pair1DSGC_calibrated.CNG.swc`, 6,736 compartments, Strahler-calibrated radii: soma 4.118
   µm, primary 3.694 µm, mid 1.653 µm, terminal 0.439 µm) via NetPyNE's SWC importer into a second
   `cellParams` entry. The synapse population (177 AMPA + 177 NMDA + 177 GABA) is re-distributed
   homogeneously on ON dendrites of the new morphology using a deterministic seeded sampler,
   preserving the paper's architecture (per `research_papers.md` best practice).
5. **Score with `tuning_curve_loss`.** Import the registered library from t0012 and call
   `score(simulated_curve_csv=<path>)` with the default target (t0004 canonical curve). The library
   emits the four registered metric keys via `ScoreReport.to_metrics_dict()`, which drops straight
   into `results/metrics.json`.

**Phase B execution strategy**: Use the prioritized port order from `research_internet.md`: (a)
Hanson 2019 (`geoffder/Spatial-Offset-DSGC-NEURON-Model`) as highest priority — same NEURON base,
re-tuned weights. (b) Jain 2020 coverage for free — architecturally identical to Poleg-Polsky 2016,
different weights only, no separate port. (c) Ding 2016 and Schachter 2010 recorded as
NeuronC-incompatible failed candidates (do not attempt port — Smith lab NeuronC is not NEURON). (d)
Koren 2017 recorded as "no standalone DSGC model deposited". (e) Ezra-Tsur 2022 (`NBELab/RSME`)
recorded as SAC-DSGC network stretch goal, out of scope for single-cell port.

**Alternatives considered**:

* **(Rejected) Pure HOC port without NetPyNE.** Would run the published `main.hoc` as-is and
  post-process the traces. Rejected because the project's downstream parameter-sweep tasks (Na/K
  grid S-0002-01, E/I ratio S-0002-05) expect a Python/NetPyNE cellParams builder they can
  re-instantiate with different parameters; a pure-HOC port would force each downstream task to
  re-port.
* **(Rejected) Re-write from scratch in Brian2 or PyNN.** Rejected because (i) the project toolchain
  is already NEURON 8.2.7 + NetPyNE 1.1.1, validated in t0007; (ii) `code-reproduction` explicitly
  requires running the *original* code, and NEURON is the original simulator; (iii) the MOD files
  (`HHst`, Jahr-Stevens NMDA in `bipolarNMDA`) are calibrated against NEURON's integrator and would
  need full re-derivation in any other simulator.
* **(Rejected) Use Hanson 2019 weights as the Phase A baseline.** Per `research_internet.md`
  hypothesis: Hanson 2019's re-tuned weights may produce an envelope closer to the project targets.
  Rejected as the *baseline* because `code-reproduction` requires reproducing the original
  (Poleg-Polsky 2016) parameters first. The Hanson 2019 weights are the documented fallback
  re-tuning step if the baseline fails the envelope after morphology swap.

**Key findings embedded** (so the implementation agent does not need to re-read research):

* ModelDB 189347 ships 14 files + a `readme.fld/` directory; entry points `mosinit.hoc` and
  `main.hoc`; cell template `RGCmodel.hoc` has 1 soma + 350 dendrite sections.
* Canonical simulation parameters (from `main.hoc`): `tstop = 1000 ms`, `dt = 0.1 ms`,
  `tau1NMDA_bipNMDA = 60 ms`, `e_SACinhib = -60 mV`, `lightspeed = 1` µm/ms.
* NEURON 8.2 implicit-declaration collisions: if a MOD compile fails with a redeclaration error for
  `hoc_*` or `nrn_*`, delete the hand-declared prototype from the top of the affected `.mod` file;
  do not rename or rewrite the function.
* Windows `nrnivmodl` requires the CMD wrapper from t0007
  (`tasks/t0007_install_neuron_netpyne/code/run_nrnivmodl.cmd`) — invoking it directly from bash
  fails due to MSYS path mangling.
* `NEURONHOME` must be set before importing NEURON on Windows:
  `os.environ.setdefault("NEURONHOME", r"C:\Users\md1avn\nrn-8.2.7")`.
* `tuning_curve_loss.score(TARGET_MEAN_CSV).loss_scalar == 0.0` is the identity gate; score any
  non-zero identity failure as a pipeline bug, not a model issue.
* Canonical CSV schema is `(angle_deg, trial_seed, firing_rate_hz)` with 12 angles × 20 trials on a
  uniform 30° grid.

**Applicable registered metrics**: all four registered metrics apply because Phase A produces a
tuning curve.

* `direction_selectivity_index` — computed by `tuning_curve_loss.compute_dsi()` on the simulated
  curve, written to `results/metrics.json` via `ScoreReport.to_metrics_dict()`.
* `tuning_curve_hwhm_deg` — computed by `tuning_curve_loss.compute_hwhm_deg()`, written the same
  way.
* `tuning_curve_reliability` — computed by `tuning_curve_loss.score()` from the 20-trial noise
  structure, written the same way.
* `tuning_curve_rmse` — computed by `tuning_curve_loss.score()` as the RMSE vs the t0004 target,
  written the same way. This is the task's headline metric (`is_key=true` per
  `meta/metrics/tuning_curve_rmse/description.json`).

No `efficiency_*` metrics apply: those are registered for tasks that train models or run inference
at scale. This task runs a fixed 240-trial simulation locally (~20-40 minutes per model), which is
not a learning or inference workload.

## Cost Estimation

* Compute: $0.00. All simulation runs on the local Windows workstation (NEURON 8.2.7 + NetPyNE
  1.1.1, already installed and validated by t0007). No GPU needed; NEURON is CPU-only for this model
  size.
* Remote machines: $0.00. No Vast.ai or cloud instance is needed.
* Paid APIs: $0.00. No LLM, embedding, or external service calls.
* Data: $0.00. The ModelDB 189347 archive is public on GitHub; the
  `geoffder/Spatial-Offset- DSGC-NEURON-Model` repository is MIT-licensed and public; the calibrated
  morphology is already in this project (t0009).
* Storage: $0.00. Expected added size is under 50 MB (ModelDB archive ~2 MB; Hanson 2019 fork ~1 MB;
  compiled `nrnmech.dll` ~500 KB; tuning-curve CSVs ~50 KB each; no large datasets).

**Total: $0.00.** Project budget (`project/budget.json`) is $1.00 total with a $1.00 per-task
default limit. This task consumes 0.0% of the project budget and 0.0% of its per-task limit.

## Step by Step

### Milestone 1: Download and compile ModelDB 189347

1. **Clone ModelDB 189347 archive into the library asset folder.** Create
   `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/` with subfolders `sources/`
   (for the cloned HOC/MOD files) and a placeholder `description.md`. Run (wrapped):
   `git clone https://github.com/ModelDBRepository/189347.git tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/`.
   Pin the commit SHA by running `git rev-parse HEAD` inside the clone and recording the hash in
   `details.json` `long_description` and in `logs/steps/01_clone_modeldb/step_log.md`. Verify the
   expected 14 files are present (`HHst.mod`, `RGCmodel.hoc`, `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`,
   `SquareInput.mod`, `bipolarNMDA.mod`, `main.hoc`, `main2.c`, `main3.c`, `model.ses`,
   `mosinit.hoc`, `readme.docx`, `readme.html`, `spike.mod`). Expected output: a `ls` of the clone
   returns ≥ 14 files; commit SHA recorded. Satisfies REQ-1.

2. **Compile the MOD files with `nrnivmodl`.** Copy `run_nrnivmodl.cmd` from
   `tasks/t0007_install_neuron_netpyne/code/run_nrnivmodl.cmd` into
   `tasks/t0008_port_modeldb_189347/code/run_nrnivmodl.cmd`. Create a build directory
   `tasks/t0008_port_modeldb_189347/build/modeldb_189347/` and run (wrapped):
   `run_nrnivmodl.cmd assets/library/modeldb_189347_dsgc/sources`. Capture stdout+stderr to
   `build/modeldb_189347/build_log.txt`. If compile fails with a redeclaration error for `hoc_*` or
   `nrn_*` symbols (expected per `research_internet.md` NEURON 8.2 implicit- declaration collision),
   delete the hand-declared prototype from the top of the affected `.mod` file; log every edit in
   `build_log.txt` and do not change any other line. Expected output: `nrnmech.dll` appears under
   `build/modeldb_189347/nrn/x86_64/` (or Windows equivalent), and the build log ends with
   `Successfully created nrnmech.dll`. Satisfies REQ-1.

### Milestone 2: Build the NetPyNE wrapper and smoke-test

3. **Write `code/constants.py`.** Hardcode Poleg-Polsky canonical parameters read verbatim from
   `sources/main.hoc` and `sources/RGCmodel.hoc`: `TSTOP_MS = 1000.0`, `DT_MS = 0.1`,
   `TAU1_NMDA_BIP_MS = 60.0`, `E_SAC_INHIB_MV = -60.0`, `LIGHTSPEED_UM_PER_MS = 1.0`,
   `N_ANGLES = 12`, `N_TRIALS = 20`, `ANGLE_STEP_DEG = 30.0`, `N_AMPA = 177`, `N_NMDA = 177`,
   `N_GABA = 177`, `CELSIUS_DEG_C = 32.0` (NEURON default; reset after NetPyNE import),
   `PATH_MODELDB_SOURCES`, `PATH_CALIBRATED_SWC`, `PATH_BUILD_DIR`, `PATH_TUNING_CURVE_CSV`. Add
   `NEURONHOME_DEFAULT = r"C:\Users\md1avn\nrn-8.2.7"` and a module-level
   `os.environ.setdefault("NEURONHOME", NEURONHOME_DEFAULT)`. Expected output:
   `python -c "from tasks.t0008_port_modeldb_189347.code.constants import TSTOP_MS; print(TSTOP_MS)"`
   prints `1000.0`. Satisfies REQ-7.

4. **Write `code/build_cell.py`.** Copy `sanity_netpyne.py` from
   `tasks/t0007_install_neuron_netpyne/code/sanity_netpyne.py` as scaffolding. Extend it with: (a) a
   function `build_dsgc_cell(*, swc_path: Path) -> dict` that returns a NetPyNE `cellParams` dict
   built from the calibrated SWC via NetPyNE's SWC importer; (b) a function
   `build_modeldb_bundled_cell() -> dict` that uses
   `importCell(fileName=str(HOC_PATH), cellName="RGC")` against a GUI-free HOC entry point
   `assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc` (created in this step by copying
   `main.hoc` and deleting the `xopen("mosinit.hoc")` / GUI-launch lines); (c) after `importCell`,
   reset `h.celsius = CELSIUS_DEG_C` (NetPyNE issue #31 workaround). The function registers the
   compiled mechanisms (`HHst`, `SAC2RGCexc`, `SAC2RGCinhib`, `bipolarNMDA`, `SquareInput`, `spike`)
   by setting `h.nrn_load_dll(str(PATH_NRNMECH_DLL))` before the import. Do NOT import
   `code.build_cell` from research code directly — copy the sanity template per the cross-task rule.
   Expected output:
   `python -c "from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc_cell; print(type( build_dsgc_cell(swc_path=PATH_CALIBRATED_SWC)))"`
   prints `<class 'dict'>`. Satisfies REQ-4.

5. **[CRITICAL] Write and run the single-angle smoke test.** Create
   `code/test_smoke_single_angle.py`. It instantiates the bundled-morphology cell via
   `build_modeldb_bundled_cell()`, drives a drifting-bar stimulus at angle 0° (preferred direction)
   for one trial (seed=0), records somatic voltage, counts action potentials via a threshold
   crossing at -10 mV, and asserts `firing_rate_hz > 0`. Run (wrapped):
   `uv run pytest code/test_smoke_single_angle.py -v`. Expected output: test passes; one row printed
   with `angle_deg=0, trial_seed=0, firing_rate_hz>0` (any positive rate counts — the smoke test
   only asserts the model fires at all, not that it hits envelope). Satisfies REQ-3. **Validation
   gate**: the trivial baseline is "the model fires at all". If `firing_rate_hz == 0` the pipeline
   is broken (wrong mechanism load path, wrong stimulus mapping, or MOD file incompatibility). STOP
   and debug — do not proceed to milestone 3. The `--limit 1` equivalent here is the single-angle
   single-trial run itself; 1 trial is enough to catch pipeline bugs because a correctly ported DSGC
   cannot produce zero PD firing.

6. **Register the library asset.** Write `details.json` at
   `assets/library/modeldb_189347_dsgc/details.json` per `meta/asset_types/library/specification.md`
   v2: `library_id = "modeldb_189347_dsgc"`,
   `name = "ModelDB 189347 DSGC (Poleg-Polsky & Diamond 2016)"`, `version = "0.1.0"`,
   `short_description` (≥ 10 words), `description_path = "description.md"`,
   `module_paths = ["code/constants.py", "code/build_cell.py", "code/run_tuning_curve.py", "code/score_envelope.py"]`,
   `entry_points` listing `build_dsgc_cell`, `build_modeldb_bundled_cell`, `run_tuning_curve`
   (script), `score_envelope` (script), `dependencies = ["neuron", "netpyne", "numpy", "pandas"]`,
   `test_paths = ["code/test_smoke_single_angle.py"]`,
   `categories = ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell", "synaptic-integration"]`,
   `created_by_task = "t0008_port_modeldb_189347"`, `date_created = "2026-04-20"`. Write
   `description.md` with YAML frontmatter (`spec_version: "2"`, `library_id`, `documented_by_task`,
   `date_documented`) and all 8 mandatory sections: Metadata, Overview (≥ 80 words), API Reference
   (≥ 100 words), Usage Examples (≥ 2 runnable examples), Dependencies, Testing, Main Ideas (≥ 3
   bullets), Summary (≥ 100 words, 2-3 paragraphs). Record the pinned ModelDB commit SHA in
   `description.md` so downstream tasks (S-0002-04 morphology sweep, S-0002-05 E/I scan) can branch
   from a specific baseline. Expected output:
   `uv run python -m arf.scripts.verificators.verify_library_asset tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc`
   reports PASSED with 0 errors. Satisfies REQ-2.

### Milestone 3: Swap morphology and document geometric differences

7. **Swap to the calibrated SWC and write the geometry report.** Extend `build_cell.py`'s
   `build_dsgc_cell()` to load the t0009 calibrated SWC at
   `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`
   via NetPyNE's SWC importer. Copy `swc_io.py` from
   `tasks/t0009_calibrate_dendritic_diameters/code/swc_io.py` into
   `tasks/t0008_port_modeldb_189347/code/swc_io.py` (cross-task copy rule). Write
   `code/report_morphology.py` that: loads the calibrated SWC via `parse_swc_file()`, counts
   compartments, computes total dendritic path length (sum of Euclidean segment lengths for
   `BASAL_DENDRITE` compartments), counts branch points (compartments whose
   `build_children_ index()` entry has ≥ 2 children) and leaves; extracts the bundled-morphology
   counterparts by parsing `RGCmodel.hoc`'s `pt3dadd` blocks with a regex-based parser (quick and
   adequate for a Neuro-only descriptive table); writes `data/morphology_swap_report.md` with a
   2-column comparison table. Expected output: the report file exists with a table listing bundled
   (1 soma + 350 sections) vs calibrated (≥ 6,700 compartments, ≥ 129 branch points, ~1.54 mm
   dendritic length) morphology stats. Satisfies REQ-4, REQ-5.

### Milestone 4: Run the 12-angle tuning curve

8. **[CRITICAL] Write and run `code/run_tuning_curve.py`.** The script takes a library ID
   (`modeldb_189347_dsgc` or `hanson_2019_spatial_offset_dsgc`) plus an SWC path, instantiates the
   cell via `build_dsgc_cell(swc_path=...)` with the calibrated SWC, and loops over 12 angles (0°,
   30°, ..., 330°) × 20 trials with fresh seeds. Seed strategy: for each
   `(angle_index, trial_index)` call `h.use_mcell_ran4(1)` then
   `h.mcell_ran4_init(angle_index * N_TRIALS + trial_index + 1)` — this guarantees 240 independent
   pseudorandom streams across the run. Each trial: build a drifting-bar stimulus of the
   paper-canonical shape (bar length 800 µm, width 80 µm, `lightspeed = 1 µm/ms`, duration
   `800 / 1 ≈ 800 ms` measured at the cell centre; use the ModelDB-bundled `SquareInput.mod`
   mechanism to drive bipolar NetStim activations with the spatial profile described in `main.hoc`'s
   `stim()` procedure), run the simulation for `h.tstop = TSTOP_MS = 1000 ms` at
   `h.dt = DT_MS = 0.1 ms`, record somatic voltage, detect APs with a threshold crossing at -10 mV,
   compute `firing_rate_hz = n_spikes / (tstop / 1000.0)`. After all 240 trials, write
   `data/tuning_curves/curve_modeldb_189347.csv` with columns
   `angle_deg, trial_seed, firing_rate_hz` (canonical schema expected by
   `tuning_curve_loss.load_tuning_curve`). Run (wrapped):
   `uv run python -u code/run_tuning_curve.py --library modeldb_189347_dsgc --swc PATH_CALIBRATED_SWC`.
   Expected output: 240 rows emitted to the CSV; a progress line every 12 trials printed to stdout;
   wall-clock runtime 20-40 minutes per `task_description.md`. Satisfies REQ-6, REQ-7, REQ-8,
   REQ-15. **Validation gate**: before running the full 240-trial loop, run a 12-trial mini-loop at
   `trial_index=0` for all 12 angles (12 trials total, 1 per angle). Inspect the resulting 12 firing
   rates: at least one angle must have `firing_rate_hz > 5` (the model should fire meaningfully in
   PD). The trivial baseline here is "no-spike model" (rate = 0 at every angle). If every rate is ≤
   5 Hz, STOP — there is a stimulus-mapping or mechanism bug. Also inspect the per-trace voltage
   recording for 2 randomly chosen angle-trial pairs and confirm (a) the cell reaches resting
   potential of ~-65 mV at t=0, (b) spike heights are ~+30 to +50 mV (not clipped at 0), (c) the
   spike count matches the threshold-crossing detector. Only then proceed to the full 240-trial run.

9. **Score the tuning curve with `tuning_curve_loss`.** Write `code/score_envelope.py` that imports
   `score` and `ScoreReport` from
   `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` and calls
   `report = score(simulated_curve_csv=PATH_TUNING_CURVE_CSV)` (target resolves to the t0004
   canonical curve automatically). Dump `report.to_metrics_dict()` to `results/metrics.json` in
   legacy flat format (single variant: the baseline). Also dump the full `ScoreReport` (all 9 fields
   including `per_target_pass`, `passes_envelope`, and signed residuals) to `data/score_report.json`
   for the answer asset. Run (wrapped): `uv run python -u code/score_envelope.py`. Expected output:
   `results/metrics.json` contains keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
   `tuning_curve_reliability`, `tuning_curve_rmse` (values are floats, not null);
   `data/score_report.json` contains the full report. Satisfies REQ-9.

10. **Assert the scoring pipeline is wired correctly.** Add a pytest case
    `code/test_scoring_pipeline.py::test_identity` that asserts
    `score(simulated_curve_csv=TARGET_MEAN_CSV).loss_scalar == 0.0` to confirm the scoring library
    is correctly imported and resolves its default target. This is the "identity gate" from
    `research_code.md` recommendation 8 — a non-zero identity loss signals a schema or import-path
    bug. Run (wrapped): `uv run pytest code/test_scoring_pipeline.py -v`. Expected output: test
    passes; loss = 0.0 exactly. Satisfies REQ-9.

### Milestone 5: Phase B sibling survey and optional Hanson 2019 port

11. **Write the Phase B survey.** Create `data/phase_b_survey.csv` with columns
    `model_name, source_url, neuron_compatible, morphology, synapse_config, runs_in_env, port_decision, port_outcome`.
    Populate one row per candidate from `research_internet.md` Section "Sibling-Model Code
    Availability" and from `research_papers.md` Paper Index: Poleg-Polsky 2016 (row 1 — this task's
    Phase A port), Hanson 2019, Jain 2020, Ding 2016, Schachter 2010, Koren 2017, Ezra-Tsur 2022.
    For each: record the fields listed in REQ-11. Perform up to 3 additional targeted web searches
    (wrapped via `run_with_logs`) if the research files leave a candidate's `runs_in_env` status
    ambiguous — specifically check ModelDB citation listings for 189347 for any post-2022
    derivatives. Log every search and URL fetched. Expected output: CSV has ≥ 7 rows; every row has
    all 8 columns populated. Satisfies REQ-10, REQ-11.

12. **Attempt the Hanson 2019 port.** Create the second library asset folder
    `tasks/t0008_port_modeldb_189347/assets/library/hanson_2019_spatial_offset_dsgc/`. Clone
    `https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model.git` into `sources/`. Compile its
    MOD files (`Exp2NMDA.mod`, `HHst.mod`) with the same CMD wrapper. Run a single-angle smoke test
    (`code/test_smoke_single_angle_hanson.py`) via `build_dsgc_cell(swc_path=PATH_CALIBRATED_SWC)`
    using the Hanson 2019 HOC template (`RGCmodel.hoc` in the fork). Two outcomes:
    * **Outcome A — compile and smoke test pass**: write `details.json` and `description.md` for
      `hanson_2019_spatial_offset_dsgc` (same schema as step 6, with library-specific
      short_description, MIT license attribution, `created_by_task` = `t0008_port_modeldb_189347`,
      categories = `["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell"]`).
      Run a full 12×20 tuning curve into `data/tuning_curves/curve_hanson_2019.csv` using the same
      `code/run_tuning_curve.py --library hanson_2019_spatial_offset_dsgc` entry. Score the result
      into `data/score_report_hanson.json`. Record the outcome in `phase_b_survey.csv`
      `port_outcome` column: "Ported; envelope pass/fail per score report".
    * **Outcome B — compile or smoke test fails**: record the exact error message in
      `phase_b_survey.csv` `port_outcome` column and in the answer asset's full document. Do NOT
      register a broken library (REQ-12 explicit requirement). Delete the
      `assets/library/hanson_2019_spatial_offset_dsgc/` folder if created. Expected output: either a
      second registered library + second tuning-curve CSV + second score report, or a documented
      port failure with specific error in the answer asset. Satisfies REQ-12, REQ-15.

### Milestone 6: Build and register the answer asset

13. **Build the answer asset.** Create
    `tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report/` per
    `meta/asset_types/answer/specification.md` v2. Write `details.json`:
    `answer_id = "dsgc-modeldb-port-reproduction-report"`,
    `question = "Does the ported ModelDB 189347 DSGC model reproduce the project's tuning-curve envelope on the calibrated morphology, and which sibling DSGC compartmental models are portable?"`,
    `short_title = "ModelDB 189347 port and Phase B sibling survey"`,
    `short_answer_path = "short_answer.md"`, `full_answer_path = "full_answer.md"`,
    `categories = ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell"]`,
    `answer_methods = ["papers", "internet", "code-experiment"]`, `source_paper_ids` (list all DOI
    slugs cited: `10.1016_j.neuron.2016.02.013`, `10.7554_eLife.42392`, `10.7554_eLife.52949`,
    `10.1038_nature18609`, `10.1371_journal.pcbi.1000899`, `10.1016_j.neuron.2017.07.020`,
    `10.1523_ENEURO.0261-21.2021`, `10.1523_JNEUROSCI.5017-13.2014`,
    `10.1016_j.neuron.2005.06.036`), `source_urls` (ModelDB, ModelDBRepository, Geoffder-GH,
    NBELab-RSME),
    `source_task_ids = ["t0002_literature_survey_dsgc_compartmental_models", "t0004_...", "t0005_...", "t0007_...", "t0009_...", "t0012_..."]`,
    `confidence = "medium"` (Phase A either passes or fails the envelope; Phase B port success of
    Hanson 2019 is uncertain until attempted), `created_by_task = "t0008_port_modeldb_189347"`,
    `date_created = "2026-04-20"`.

    Write `short_answer.md` with YAML frontmatter and three sections (Question, Answer — 2-5
    sentences, direct and citation-free, stating whether Phase A envelope passed, whether Hanson
    2019 was successfully ported; Sources — bullet list of task IDs / paper IDs / URLs).

    Write `full_answer.md` with YAML frontmatter (including `confidence: "medium"`) and all 9
    mandatory sections: Question, Short Answer (2-5 sentences, citation-free), Research Process
    (describe Phase A port workflow + Phase B survey workflow), Evidence from Papers (cite
    Poleg-Polsky 2016 for architecture, El-Quessny 2021 for morphology-tuning relationship, Hanson
    2019 for re-tuned weights), Evidence from Internet Sources (ModelDB archive layout, Geoffder
    fork, NEURON 8.2 porting notes), Evidence from Code or Experiments (the two tuning-curve CSVs
    and their `ScoreReport`s; the Phase B survey CSV; the morphology swap report; the smoke test
    outputs), Synthesis (envelope verification table with DSI / peak / null / HWHM as numbers +
    pass/fail; Phase B survey table; explain how the morphology swap affected tuning if at all),
    Limitations (project 40-80 Hz peak and 60-90° HWHM are project targets, not paper reproductions;
    ModelDB source is canonical while paper prose is truncated; Ding 2016 / Schachter 2010 / Koren
    2017 are NeuronC-incompatible so their tuning cannot be directly compared), Sources (all IDs +
    URLs cited, plus markdown reference-link definitions). Include the complete Phase A envelope
    verification table and the Phase B survey table inline in the Synthesis section. Expected
    output:
    `uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report`
    reports PASSED. Satisfies REQ-16.

14. **Run all verificators and style checks.** Run (all wrapped):
    * `uv run python -u -m arf.scripts.verificators.verify_library_asset tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc`
      → PASSED.
    * If Outcome A in step 12:
      `uv run python -u -m arf.scripts.verificators.verify_library_asset tasks/t0008_port_modeldb_189347/assets/library/hanson_2019_spatial_offset_dsgc`
      → PASSED.
    * `uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report`
      → PASSED.
    * `uv run flowmark --inplace --nobackup` on every edited `.md` file under this task.
    * `uv run ruff check --fix tasks/t0008_port_modeldb_189347/code/ && uv run ruff format tasks/t0008_port_modeldb_189347/code/`
      → 0 errors.
    * `uv run mypy tasks/t0008_port_modeldb_189347/code/` → 0 errors.
    * `uv run pytest tasks/t0008_port_modeldb_189347/code/ -v` → all tests pass. Expected output:
      every command exits 0. Satisfies REQ-2, REQ-3, REQ-13, REQ-16.

## Remote Machines

None required. All simulation runs on the local Windows workstation with NEURON 8.2.7 + NetPyNE
1.1.1 (stack validated in t0007). NEURON does not need a GPU for this model (~6,700 compartments,
~240 trials × 1-second simulated time). The task description pins compute to local. No Vast.ai or
cloud instance is provisioned.

## Assets Needed

* `tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/` — source
  NeuroMorpho.Org SWC (topology reference only; not used directly because t0009 calibrates it).
* `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`
  — calibrated DSGC morphology (6,736 compartments, Strahler-calibrated radii). Consumed as-is by
  NetPyNE's SWC importer.
* `tasks/t0007_install_neuron_netpyne/code/sanity_netpyne.py` — NetPyNE cell-construction
  scaffolding. Copied into `code/build_cell.py` per cross-task copy rule.
* `tasks/t0007_install_neuron_netpyne/code/run_nrnivmodl.cmd` — Windows CMD wrapper for `nrnivmodl`.
  Copied into `code/run_nrnivmodl.cmd` per cross-task copy rule.
* `tasks/t0009_calibrate_dendritic_diameters/code/swc_io.py` — SWC parser with `SwcCompartment`,
  `parse_swc_file`, `build_children_index`. Copied into `code/swc_io.py` per cross-task copy rule.
* `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/` — scoring
  library. Imported (registered library, not copied) via
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import score, ScoreReport, TUNING_CURVE_CSV_COLUMNS`.
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/files/curve_mean.csv`
  — canonical target curve. Resolved automatically by `tuning_curve_loss.score()`'s default target.
* External: `https://github.com/ModelDBRepository/189347.git` — the ModelDB 189347 archive (public,
  no licence restrictions on the code beyond attribution).
* External: `https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model.git` — Hanson 2019 fork
  (MIT licence).
* `meta/metrics/direction_selectivity_index/`, `tuning_curve_hwhm_deg/`,
  `tuning_curve_reliability/`, `tuning_curve_rmse/` — registered metric keys; metric values from
  `ScoreReport.to_metrics_dict()` land directly in `results/metrics.json`.

## Expected Assets

* **1 library asset** at `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/` with
  `details.json` (spec_version "2"), `description.md` (all 8 mandatory sections), and a `sources/`
  subfolder containing the pinned ModelDB 189347 archive. Exposes
  `build_dsgc_cell(*, swc_path: Path) -> dict` (NetPyNE cellParams for a calibrated-morphology DSGC)
  and `build_modeldb_bundled_cell() -> dict` (NetPyNE cellParams for the bundled-morphology DSGC) as
  entry points. Matches the `expected_assets: {"library": 1}` in `task.json`.
* **0 or 1 additional library asset** at
  `tasks/t0008_port_modeldb_189347/assets/library/hanson_2019_spatial_offset_dsgc/` if step 12
  outcome A succeeds. Not counted toward `task.json` `expected_assets` (that declares exactly 1
  library). If it succeeds it is documented as a bonus port in the answer asset.
* **1 answer asset** at
  `tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report/` with
  `details.json`, `short_answer.md` (≥ 3 sections), and `full_answer.md` (≥ 9 mandatory sections).
  Covers Phase A envelope verification and the Phase B sibling survey. Matches the
  `expected_assets: {"answer": 1}` in `task.json`.
* **Simulated tuning-curve CSV** `data/tuning_curves/curve_modeldb_189347.csv` with 240 rows in
  canonical schema — primary Phase A output, consumed by t0011 and by the scoring step. Optionally
  `data/tuning_curves/curve_hanson_2019.csv` (same schema) if step 12 succeeds.
* **Morphology swap report** `data/morphology_swap_report.md` — per REQ-5.
* **Phase B survey** `data/phase_b_survey.csv` — per REQ-10, REQ-11.
* **Build log** `build/modeldb_189347/build_log.txt` (and optionally
  `build/hanson_2019/build_log.txt`) — per REQ-1.
* **`results/metrics.json`** with the four registered metric keys populated with floats from
  `ScoreReport.to_metrics_dict()`. Legacy flat format (single-variant, baseline Poleg-Polsky 2016
  port on calibrated morphology).

## Time Estimation

* Research (already complete): ~5 hours total across `research_papers.md`, `research_internet.md`,
  `research_code.md`.
* Planning (this step): ~1 hour.
* Milestone 1 — clone and compile: ~30 minutes (clone ≈ 5 min, first `nrnivmodl` compile ≈ 5 min,
  possible NEURON 8.2 implicit-declaration fix ≈ 10-20 min).
* Milestone 2 — NetPyNE wrapper + smoke test: ~2-3 hours (copy scaffolding, write `build_cell.py`,
  write constants, wrap HOC, debug NEURONHOME and `h.celsius` reset).
* Milestone 3 — morphology swap + geometry report: ~1 hour.
* Milestone 4 — 12-angle tuning curve + scoring: ~1 hour to write `run_tuning_curve.py` +
  `score_envelope.py`; ~20-40 minutes to execute the 240-trial run per `task_description.md`; ~15
  minutes for the identity-gate pytest.
* Milestone 5 — Phase B survey + Hanson 2019 port attempt: ~2-4 hours depending on outcome A vs B.
  Outcome A (success) adds another ~30 minutes for the second 240-trial run.
* Milestone 6 — build answer asset + verificators: ~1-2 hours.
* Results and reporting (orchestrator-managed, not counted in this plan's steps): ~1 hour for
  `results_summary.md`, `results_detailed.md`, `costs.json`, `suggestions.json`,
  `remote_machines_used.json`.
* **Total wall-clock for implementation: ~8-13 hours** (plus 20-80 minutes of NEURON simulation time
  absorbed into milestones 4 and 5).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| MOD file compile fails on NEURON 8.2.7 due to implicit-declaration collisions in `HHst.mod` / `spike.mod` / `bipolarNMDA.mod` (expected per `research_internet.md` finding 5). | Medium | Medium | Per the NEURON 8.2 changelog, delete the hand-declared `hoc_*`/`nrn_*` prototype from the affected `.mod` file; log every deletion in `build_log.txt`. Do not rename or rewrite the function body. If compile still fails after prototype removal, create an intervention file in `intervention/` naming the specific MOD file and error message; do not silently patch unrelated code. |
| `mosinit.hoc` auto-launches the NEURON GUI at import time, blocking NetPyNE `importCell()`. | High | Low | Load `main.hoc` directly via a GUI-free derivative `dsgc_model.hoc` that removes the GUI-launch lines (per `research_internet.md` recommendation 4). Keep the original `mosinit.hoc` untouched under `sources/` for provenance. |
| Calibrated morphology swap breaks envelope compliance (`research_papers.md` hypothesis: may quantitatively shift tuning per El-Quessny 2021). | Medium | Medium (scientific finding, not blocker) | Report the shift verbatim in the answer asset's full document. Surface a new suggestion via `results/suggestions.json` for morphology-conditioned parameter retuning (precedes S-0002-04 morphology sweep). Do not retune Na/K or synaptic weights within this task — that would contaminate the reproduction. |
| Smoke test passes with zero firing rate (stimulus mapping bug: bar-crossing time profile not correctly driving NetStim activations). | Medium | High (blocks milestone 4) | Validation gate in step 5: if PD firing rate == 0, STOP. Dump the per-synapse NetStim spike times for one angle-trial pair to `data/debug_stim_trace.csv` and the somatic voltage trace to `data/debug_vm_trace.csv`; inspect both; common cause is the `lightspeed` sign or bar-position offset. Fallback: port the paper's `main.hoc` `stim()` procedure verbatim instead of re-implementing the drifting-bar profile in Python. |
| NetPyNE `importCell()` silently mutates `h.celsius`, changing channel kinetics (NetPyNE issue #31). | Medium | Low | Reset `h.celsius = CELSIUS_DEG_C` after every `importCell` call in `build_cell.py`; document in code comments with reference to NetPyNE issue #31. |
| 240-trial run exceeds the `task_description.md` 20-40 minute estimate (e.g. 3-4 hours because per-trial wall-clock is 30 s not 5-10 s on this workstation). | Medium | Low | Run milestone 4 step 8's validation gate (12 trials) first; multiply by 20 to project full runtime. If > 2 hours, drop to 10 trials per angle (120 trials total) and document the reduction in the answer asset — this is above the literature floor of 4-10 trials per `research_papers.md` best-practice note. Do NOT drop below 10 trials. |
| Hanson 2019 fork fails to compile (e.g., `Exp2NMDA.mod` uses a VERBATIM block incompatible with NEURON 8.2.7). | Medium | Low | Outcome B of step 12: record the failure in `phase_b_survey.csv` and the answer asset, delete the partial library folder, do not register a broken library. REQ-12 explicitly allows this fallback. |
| ModelDB 189347 GitHub mirror is archived/unavailable at clone time. | Low | High | Fallback to the direct SenseLab zip via `curl https://senselab.med.yale.edu/modeldb/ShowModel?model=189347&format=zip`. If both fail, create an intervention file requesting human assistance — per `code-reproduction` task type guidelines, do not silently substitute a different archive. |
| Scoring library identity gate fails (`score(TARGET_MEAN_CSV).loss_scalar != 0.0`). | Low | High (invalidates metrics) | Step 10's pytest is the gate. If it fails, the bug is in the scoring pipeline wiring, not the model — inspect the import path, CSV schema, and dtype casts. Do not proceed to milestone 6 until identity holds. |
| Tuning-curve envelope fails (DSI, peak, null, or HWHM outside the project target). | Medium | Low (scientific finding) | Report the specific axis that failed in the answer asset with numeric residuals. Surface a suggestion for the fallback re-tuning step (Hanson 2019 weights) via `results/suggestions.json`. Do not retune synaptic weights within this task. |

## Verification Criteria

* **Library asset verificator passes**:
  `uv run python -u -m arf.scripts.verificators.verify_library_asset tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc`
  exits 0 with 0 errors. Expected output includes "PASSED" and no `LA-E*` diagnostics. Directly
  verifies REQ-1, REQ-2, REQ-3.
* **Answer asset verificator passes**:
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report`
  exits 0 with 0 errors. Expected output includes "PASSED" and no `AA-E*` diagnostics. Directly
  verifies REQ-9, REQ-10, REQ-11, REQ-12, REQ-16.
* **Tuning-curve CSV has 240 rows in canonical schema**:
  `uv run python -c "import pandas as pd; df = pd.read_csv('data/tuning_curves/curve_modeldb_189347.csv'); assert list(df.columns) == ['angle_deg', 'trial_seed', 'firing_rate_hz']; assert len(df) == 240; assert sorted(df['angle_deg'].unique().tolist()) == [0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0]; assert sorted(df['trial_seed'].unique(). tolist()) == list(range(20)); print('OK')"`
  prints `OK`. Verifies REQ-6, REQ-8, REQ-15.
* **Identity gate**:
  `uv run pytest tasks/t0008_port_modeldb_189347/code/test_scoring_pipeline.py::test_identity -v`
  reports 1 passed, 0 failed. Verifies the scoring pipeline wiring (REQ-9).
* **Smoke test**: `uv run pytest tasks/t0008_port_modeldb_189347/code/test_smoke_single_angle.py -v`
  reports 1 passed. Verifies REQ-3.
* **Metrics.json has four registered keys**:
  `uv run python -c "import json; m = json.loads(open('tasks/t0008_port_modeldb_189347/results/metrics.json').read()); expected = {'direction_selectivity_index', 'tuning_curve_hwhm_deg', 'tuning_curve_reliability', 'tuning_curve_rmse'}; assert expected.issubset(set(m)); print('OK')"`
  prints `OK`. Verifies REQ-9.
* **Morphology report exists**: `ls tasks/t0008_port_modeldb_189347/data/morphology_swap_report.md`
  returns the file and it contains a comparison table with both "bundled" and "calibrated" columns;
  `uv run grep -E "(bundled|calibrated)" data/morphology_swap_report.md | wc -l` ≥ 2. Verifies
  REQ-4, REQ-5.
* **Phase B survey has all required columns**:
  `uv run python -c "import pandas as pd; df = pd.read_csv('data/phase_b_survey.csv'); expected = {'model_name', 'source_url', 'neuron_compatible', 'morphology', 'synapse_config', 'runs_in_env', 'port_decision', 'port_outcome'}; assert expected.issubset(set(df.columns)); assert len(df) >= 7; print('OK')"`
  prints `OK`. Verifies REQ-10, REQ-11.
* **Costs stay at $0.00**:
  `uv run python -c "import json; c = json.loads(open('tasks/t0008_port_modeldb_189347/results/costs.json').read()); assert c.get('total_cost_usd', 0.0) == 0.0; print('OK')"`
  prints `OK`. Verifies REQ-14.
* **Style and type checks pass**: `uv run ruff check tasks/t0008_port_modeldb_189347/code/` reports
  0 errors and `uv run mypy tasks/t0008_port_modeldb_189347/code/` reports 0 errors. Verifies
  style-guide compliance for REQ-2.
* **All REQ-* covered**: every `REQ-*` item in the Task Requirement Checklist maps to at least one
  Step by Step item and to at least one verification criterion above. Confirmed by cross- reference
  inspection.
