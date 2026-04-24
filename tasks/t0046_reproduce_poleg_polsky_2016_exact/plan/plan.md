---
spec_version: "2"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
date_completed: "2026-04-24"
status: "complete"
---
# Plan: Exact Reproduction of Poleg-Polsky and Diamond 2016 (ModelDB 189347)

## Objective

Rebuild ModelDB 189347 from scratch into a new library asset `modeldb_189347_dsgc_exact` under
`tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/`, reproduce every quantitative claim
in Figures 1-8 of Poleg-Polsky and Diamond 2016 (Neuron, DOI `10.1016/j.neuron.2016.02.013`) on the
paper's own reported metrics (PSP amplitudes in mV, direction-tuning slope angles in degrees,
subthreshold ROC AUC, and Figure 8 qualitative suprathreshold behaviour), and publish a line-by-line
paper-vs-code-vs-reproduction audit plus a paper-vs-code discrepancy catalogue in the answer asset
`poleg-polsky-2016-reproduction-audit`. "Done" means: new library asset exists and compiles under
NEURON 8.2.7 + NetPyNE 1.1.1; answer asset contains a populated parameter audit table, per-figure
reproduction table, and discrepancy catalogue; every primary pass criterion in the Pass Criterion
below is met or documented with numerical gap; figure PNGs exist under `results/images/` for each
reproduced paper figure; supplementary PDF attached to the existing paper asset
`10.1016_j.neuron.2016.02.013` via corrections overlay. The task does NOT compare against t0004's
tuning-curve envelope (40-80 Hz peak band is rabbit, not mouse, and out of scope per
task_description.md).

## Task Requirement Checklist

Operative task request quoted verbatim from `task.json` and `task_description.md`:

> Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit. Rebuild ModelDB 189347 from
> scratch to match Poleg-Polsky 2016; audit every parameter against paper+code+supplementary;
> reproduce all paper tests within tolerance. Produce a fresh port of ModelDB 189347 that reproduces
> Poleg-Polsky 2016 exactly on the metrics the paper actually reports — PSP amplitudes,
> direction-tuning slope angles, ROC AUC under the noise conditions described in the paper, and
> qualitative Figure 8 suprathreshold behaviour — using the paper's own protocols. Publish a
> line-by-line audit comparing paper · ModelDB code · our reproduction for every quantitative
> claim, and a discrepancy catalogue for any place where the paper text and the ModelDB code
> disagree.

Concrete requirements extracted from the quoted task text and from `task_description.md`:

* **REQ-1** — Create a new library asset `modeldb_189347_dsgc_exact` at
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/` with
  `details.json` and `description.md`, per `meta/asset_types/library/specification.md`. Satisfied by
  Steps 1, 3, 4, 18.
* **REQ-2** — Do NOT fork t0008, t0020, or t0022 library code. Copy ModelDB `.mod`/`.hoc` source
  files into `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/` (and mirror into the library
  asset's `sources/`) with leading-comment citations to ModelDB release and commit SHA
  `87d669dcef18e9966e29c88520ede78bc16d36ff`. Satisfied by Steps 1, 2.
* **REQ-3** — Use the HOC-embedded morphology inside `RGCmodel.hoc` (approx. 11,500 `pt3dadd`
  calls, faithful to the paper) rather than substituting t0005's SWC. Satisfied by Step 1.
* **REQ-4** — Centralise file paths in `code/paths.py` and simulation constants in
  `code/constants.py` per the project Python style guide. Satisfied by Steps 5, 6.
* **REQ-5** — Write a simulation driver that reproduces `simplerun()` semantics from `main.hoc`
  including the `achMOD = 0.33` rebind in `simplerun()`, 8-direction dispatch (45-degree spacing at
  1 mm/sec bar), and the PD/ND gabaMOD swap (PD `gabaMOD = 0.33`, ND `gabaMOD = 0.99`). Satisfied by
  Step 8.
* **REQ-6** — Reproduce Figure 1 (control, 8-direction PSPs with voltage-dependent NMDAR): PD PSP
  **5.8 +/- 3.1 mV**, ND PSP **3.3 +/- 2.8 mV**, slope **62.5 +/- 14.2 degrees**, DSI preserved
  under AP5. Satisfied by Steps 10, 13.
* **REQ-7** — Reproduce Figure 2 (iMK801 + bath AP5 analogue): AP5-after-iMK801 further reduces PD
  PSP by only **16 +/- 17%**. Satisfied by Steps 10, 13.
* **REQ-8** — Reproduce Figure 3 (NEURON model gNMDA sweep). Primary reproduction at
  `gNMDA = 0.5 nS` (code value, via `b2gnmda = 0.5` in `main.hoc`); secondary pass at
  `gNMDA = 2.5 nS` (paper claim) to test whether the paper's stated value or the code's value
  publishes Figures 1-5. Satisfied by Steps 10, 11, 13.
* **REQ-9** — Reproduce Figure 4 (High-Cl- internal, tuned-excitation analogue; implemented in HOC
  as `exptype = 3`): slope **45.5 +/- 3.7 degrees** (additive). DS reverses PD in at least 50% of
  trials (paper's 15/20 is 75%). Satisfied by Steps 10, 12, 13.
* **REQ-10** — Reproduce Figure 5 (0 Mg2+, voltage-independent NMDAR analogue; implemented as
  `exptype = 2` with `Voff_bipNMDA = 1`): slope **45.5 +/- 5.3 degrees** (additive). DSI reduced but
  PD != ND. Satisfied by Steps 10, 12, 13.
* **REQ-11** — Reproduce Figures 6-8 noise-on conditions by overriding `h.flickerVAR` and
  `h.stimnoiseVAR` to `{0.0, 0.1, 0.3, 0.5}` and re-invoking `placeBIP()`; DO NOT write a new noise
  MOD file (the driver is already present in `main.hoc`'s `placeBIP()` but parameterised to zero).
  Satisfied by Steps 14, 15.
* **REQ-12** — Reproduce Figure 7 noise-free subthreshold ROC AUC: **0.99 / 0.98 / 0.83** for
  control / AP5 / 0 Mg2+, tolerance +/-0.05. Satisfied by Step 15.
* **REQ-13** — Reproduce Figure 8 qualitative suprathreshold behaviour: DSI preserved under AP5
  (qualitative); DSI reduced in 0 Mg2+ (qualitative); PD-failure rate increases under AP5. Satisfied
  by Step 16.
* **REQ-14** — Download supplementary PDF `NIHMS766337-supplement.pdf` from
  `https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf` and attach
  it to the existing paper asset
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
  via a corrections overlay (file under `tasks/t0046_.../corrections/`). Do NOT mutate the completed
  t0002 folder. Satisfied by Step 7.
* **REQ-15** — Populate an audit table with one row per basic parameter. Columns: Parameter, Paper
  value (when stated), ModelDB code value, Our reproduction value, Match?, Citation. Use `main.hoc`
  values (not MOD defaults) as the code column, per the corrected table in
  `research/research_code.md`. Satisfied by Steps 17, 19.
* **REQ-16** — Populate a figure-reproduction table with one row per paper figure (1-8). Columns:
  Figure, Paper metric, Our reproduction metric, Tolerance, Match verdict, Paper reference. Separate
  rows for PD PSP, ND PSP, slope, ROC AUC, etc. as applicable. Satisfied by Steps 17, 19.
* **REQ-17** — Populate a discrepancy catalogue that includes the four pre-flagged entries (gNMDA
  2.5 vs 0.5 nS; synapses 177 vs 282; noise driver present but zeroed in code; dendritic Nav 2e-4
  S/cm^2 not strictly zero) plus the corrected `main.hoc` vs MOD-default overrides (n=0.3 vs 0.25,
  gama=0.07 vs 0.08, newves=0.002 vs 0.01, tau1NMDA=60 vs 50 ms, tau_SACinhib=30 vs 10 ms,
  e_SACinhib=-60 vs -65 mV) plus any new discrepancies discovered at implementation. Each entry
  includes numerical evidence. Satisfied by Steps 17, 19.
* **REQ-18** — Create the answer asset `poleg-polsky-2016-reproduction-audit` at
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/`
  with `details.json`, `short_answer.md`, and `full_answer.md` per
  `meta/asset_types/answer/specification.md`. The `full_answer.md` embeds the audit table,
  figure-reproduction table, discrepancy catalogue, reproduction-bug list, and one-paragraph
  project-level summary. Satisfied by Step 19.
* **REQ-19** — Generate per-figure reproduction PNGs under `tasks/t0046_.../results/images/` for
  every paper figure the task reproduces (Figs 1, 2, 3, 4, 5, 6, 7, 8). Each PNG has labelled axes,
  matching ranges, and a clear paper-vs-reproduction overlay where applicable. Use the
  `tuning_curve_viz` library (imported via
  `tasks.t0011_response_visualization_library.code.tuning_curve_viz`) for tuning-curve plots, driven
  with PSP-amplitude CSV schemas. Satisfied by Step 18.
* **REQ-20** — Write `results/metrics.json` in the explicit multi-variant format (per
  `arf/specifications/metrics_specification.md`) with one variant per reproduction condition
  (control, AP5, 0Mg, highCl, control-noise-10%, control-noise-30%, control-noise-50%). Include
  `direction_selectivity_index` per variant from the registered metrics registry; mark peak-Hz
  metrics as `null` for subthreshold variants since they do not apply. Satisfied by Step 17.

## Approach

**Technical approach (grounded in research findings from all three research stages).**

The task implements a faithful from-scratch port of ModelDB 189347 and exercises it against the
eight paper figures. The ModelDB release has a single commit SHA
`87d669dcef18e9966e29c88520ede78bc16d36ff` (2019-05-31) and ships eleven source files: `main.hoc`,
`RGCmodel.hoc`, `HHst.mod`, `bipolarNMDA.mod`, `SAC2RGCinhib.mod`, `SAC2RGCexc.mod`,
`SquareInput.mod`, `spike.mod`, `mosinit.hoc`, `model.ses`, `readme.html`/`.docx` (per
`research/research_internet.md` and `research/research_code.md`).

**Morphology choice.** `RGCmodel.hoc` contains approximately 11,500 hard-coded `pt3dadd` calls
defining a single bundled DSGC reconstruction used by the paper's simulations. `placeBIP()` and
`placeSAC()` depend on section ordering and on the ON/OFF cut `z >= -0.16 * y + 46`; neither can
consume an external SWC without re-implementing synapse placement. The plan therefore uses the
HOC-embedded morphology verbatim (recommended by `research/research_code.md`). The
`[t0005_download_dsgc_morphology]` SWC is documented as a substitute that the plan deliberately does
NOT swap in; the audit records this as a morphology-provenance discrepancy note rather than a
reproduction bug.

**Simulation semantics.** `main.hoc:332-360` defines `simplerun($1,$2)` which: (a) when `$1=1`
(control), sets `Voff_bipNMDA = 0`, `Vset_bipNMDA = -60`, `gabaMOD = 0.33 + 0.66*$2`,
`achMOD = 0.33` (rebinding the module-load default of 0.25); (b) when `$1=2` (0 Mg2+), sets
`Voff_bipNMDA = 1`; (c) when `$1=3` (High-Cl-/tuned-excitation), sets `gabaMOD = 1`, adds
`0.66*(1-$2)` to `achMOD`, and modifies the inhibitory reversal. `$2=0` is PD (`gabaMOD=0.33`),
`$2=1` is ND (`gabaMOD=0.99`). Because `simplerun()` unconditionally rebinds `achMOD = 0.33`, any
Python-level override of `achMOD` before calling into HOC will be overwritten; the plan captures
this by exposing `exptype` and `direction` as the only top-level driver knobs and lets
`simplerun()`-equivalent code (inside `code/run_simplerun.py`) handle the parameter cascade.

**Noise-on conditions.** `main.hoc:99-101` already declares `flickertime = 50`, `flickerVAR = 0`,
`stimnoiseVAR = 0`, and `placeBIP()` (lines 191-282) implements per-50-ms Gaussian perturbation on
both `BIPVbase` and `BIPVamp`. Figures 6-8 therefore need only a Python override of `h.flickerVAR`
and `h.stimnoiseVAR` plus a re-call of `placeBIP()` to re-roll noise vectors. This contradicts
`research/research_internet.md`'s "noise driver missing" claim; `research/research_code.md` is
correct and the audit records the discrepancy as "noise driver present but zeroed" rather than
"missing".

**gNMDA pick.** `main.hoc:43` sets `b2gnmda = 0.5` nS; Figure 3E of the paper states 2.5 nS. Per
task_description.md, primary reproduction uses the code value 0.5 nS. Step 11 runs a secondary sweep
at 2.5 nS to test whether moving to the paper value shifts the Figure 1-5 metrics toward or away
from the paper's targets.

**Parameter-correction table (from `research/research_code.md`).** The `research_internet.md` audit
extracted MOD-file PARAMETER defaults for several rows where `main.hoc` overrides them at module
load. Canonical values (main.hoc wins): `n_bipNMDA = 0.3` (not 0.25), `gama_bipNMDA = 0.07` (not
0.08), `newves_bipNMDA = 0.002` (not 0.01), `tau1NMDA_bipNMDA = 60 ms` (not 50),
`tau_SACinhib = 30 ms` (not 10), `e_SACinhib = -60 mV` (not -65). `achMOD = 0.25` at module load but
`simplerun()` rebinds to 0.33. These corrections enter the audit as rows in the discrepancy
catalogue.

**Cross-task import rule.** `[t0020]` imports from `tasks.t0008_....code`, which violates the
project's rule that only registered libraries may be imported across tasks. This plan copies the
three reusable helper patterns (NEURON bootstrap pattern approximately 55 lines, HOC-safe source-dir
chdir approximately 60 lines, synapse-coordinate snapshot dataclass approximately 40 lines,
BIP-position baseline assertion approximately 20 lines) into `code/` verbatim with renamed sentinels
and constants, and imports the t0011 and t0012 libraries through their registered paths
(`tasks.t0011_response_visualization_library.code.tuning_curve_viz`,
`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`) for plotting and the Figure
8 DSI helper respectively. The MOD and HOC files from the ModelDB release are themselves copied into
`code/sources/` from `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/`
with a leading comment in each file citing ModelDB 189347, commit SHA, and 2019-05-31 date (per
task_description.md cross-task import rule).

**Alternatives considered.** (1) Substituting the t0005 SWC morphology: REJECTED because
`placeBIP()` depends on section ordering and the ON/OFF cut only makes sense on the bundled
morphology; a substitution would require re-implementing synapse placement and would itself be a
reproduction bug, not a faithful port. (2) Forking t0008/t0020 library code in place: FORBIDDEN by
task_description.md. (3) Writing a new luminance-noise MOD file: REJECTED because
`research/research_code.md` proves the shipped `placeBIP()` already carries the driver;
parameterising it to non-zero SD is the correct (and lighter-weight) fix. (4) Using t0012's
firing-rate scorer as the primary metric: REJECTED because the paper's primary metrics are PSP
amplitudes (mV), slope angles (deg), and ROC AUC; firing rates are a Figure 8 secondary check only.

**Task type recommendation.** `task.json` already lists `task_types: ["code-reproduction"]`. The
`meta/task_types/code-reproduction/instruction.md` Planning Guidelines were followed: the
NEURON-simulation step that re-runs `simplerun()` equivalents under each condition is the
`[CRITICAL]` step (marked in Step by Step). The ModelDB release is available and pinned to SHA
`87d669dcef18e9966e29c88520ede78bc16d36ff`. Environment pinning: NEURON 8.2.7 + NetPyNE 1.1.1 at
`C:\Users\md1avn\nrn-8.2.7` as validated by `[t0007_install_neuron_netpyne]`.

**Registered metrics applicability.** The four registered metrics in `meta/metrics/` are
`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, and
`tuning_curve_rmse`. `direction_selectivity_index` is applicable to every condition (computed on PSP
peak vs v_init for subthreshold, on AP counts for Fig 8 suprathreshold) and is measured in Step 17
using the t0012 `compute_dsi` helper. `tuning_curve_hwhm_deg` is applicable only to the Fig 8 AP
tuning curve (paper does not report PSP HWHM); computed in Step 16. `tuning_curve_reliability` and
`tuning_curve_rmse` are defined in terms of a target firing-rate curve; REJECTED as not applicable
here because the paper reports no per-angle target curve and this task explicitly excludes
comparisons against t0004's envelope (Pass Criterion's "parameter-match criterion" sets the audit
target, not a tuning-curve RMSE). The explicit reason-for-omission is documented in the
discrepancy-catalogue row "registered metric tuning_curve_rmse / tuning_curve_reliability not
applicable: paper does not report a target per-angle firing-rate curve".

## Cost Estimation

Total cost: **$0.00** for this task. Reasoning:

* No paid API calls. All LLM work is local Claude Code.
* No remote compute. Per `task_description.md`: "Local CPU only. No Vast.ai."
* No paid datasets. The ModelDB release, the Neuron paper, and the PMC supplementary PDF are all
  publicly available free of charge.
* NEURON 8.2.7 + NetPyNE 1.1.1 are free open-source packages, already installed and validated in
  `[t0007_install_neuron_netpyne]`.

Running cost: $0.00 / $1.00 per-task budget (`project/budget.json`). Confirmed under budget.

## Step by Step

### Milestone A: Library asset scaffolding and source-file copy

1. **Copy ModelDB release source files into the task.** Copy the eleven files from
   `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/` into
   `tasks/t0046_.../code/sources/` and also into
   `tasks/t0046_.../assets/library/modeldb_189347_dsgc_exact/sources/`: `main.hoc`, `RGCmodel.hoc`,
   `HHst.mod`, `bipolarNMDA.mod`, `SAC2RGCinhib.mod`, `SAC2RGCexc.mod`, `SquareInput.mod`,
   `spike.mod`, `mosinit.hoc`, `model.ses`, `readme.html`, `readme.docx`. Prepend a leading comment
   in each `.hoc` and `.mod` file (HOC/NMODL comment syntax `//` or `COMMENT...ENDCOMMENT`) citing
   "ModelDB accession 189347, commit SHA `87d669dcef18e9966e29c88520ede78bc16d36ff`, authored
   2019-05-31 by tommorse, mirror `https://github.com/ModelDBRepository/189347`". Expected:
   identical byte content to t0008's sources except for the provenance comment. Satisfies REQ-1,
   REQ-2, REQ-3.

2. **Create the GUI-free HOC loader.** Write `code/sources/dsgc_model_exact.hoc` by copying the
   non-GUI parts of `main.hoc` (all parameter declarations from lines 1-330, `init_active()`,
   `placeBIP()`, `update()`, `init_sim()`) and removing every `xpanel`, `xbutton`, `xradiobutton`,
   and `load_file("model.ses")` line. Do NOT import t0008's existing `dsgc_model.hoc`; write
   equivalent semantics from scratch while matching parameter values bit-for-bit. Do NOT remove the
   `simplerun($1,$2)` proc body — the Python driver in Step 8 calls it. Satisfies REQ-2, REQ-5.

3. **Create the library asset metadata.** Write `details.json` at
   `tasks/t0046_.../assets/library/modeldb_189347_dsgc_exact/details.json` per
   `meta/asset_types/library/specification.md` v2. Fields: `spec_version`, `library_id`, `name`,
   `description_path` = `"description.md"`, `module_paths` = list of task-code module paths (e.g.
   `"tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun"`), `languages`, `categories`,
   `added_by_task`, `date_added`. Pin the ModelDB commit SHA
   `87d669dcef18e9966e29c88520ede78bc16d36ff` in the description. Satisfies REQ-1.

4. **Write the library description.** Write
   `tasks/t0046_.../assets/library/modeldb_189347_dsgc_exact/description.md` covering: purpose
   (reproduce ModelDB 189347 faithfully on paper-reported metrics), architecture (soma + 350 dend
   sections, 282 BIP/SACinhib/SACexc triples on ON dendrites), how to build the cell, how to run the
   four canonical conditions (control / AP5 / 0 Mg2+ / High-Cl-), how to enable noise, the
   cross-task import rule (copy rather than import), and the paper-vs-code discrepancy summary.
   Satisfies REQ-1.

### Milestone B: Python driver scaffolding

5. **Centralise paths in `code/paths.py`.** Define `REPO_ROOT`, `TASK_DIR`, `CODE_DIR`,
   `SOURCES_DIR`, `LIBRARY_SOURCES_DIR`, `RESULTS_DIR`, `IMAGES_DIR`, `NEURONHOME` =
   `Path("C:/Users/md1avn/nrn-8.2.7")`, `NRNMECH_DLL` = `SOURCES_DIR / "x86_64" / "nrnmech.dll"`,
   `MAIN_HOC` = `SOURCES_DIR / "main.hoc"`, `DSGC_MODEL_HOC` =
   `SOURCES_DIR / "dsgc_model_exact.hoc"`. Centralisation is mandatory per the project Python style
   guide. Satisfies REQ-4.

6. **Centralise constants in `code/constants.py`.** Define named constants for the paper's
   conditions (`ExperimentType` IntEnum with values `CONTROL = 1`, `ZERO_MG = 2`, `HIGH_CL = 3`),
   directions (`Direction` IntEnum with `PREFERRED = 0`, `NULL = 1`), paper parameter values pulled
   from `main.hoc` (corrected per `research/research_code.md`: `N_BIPNMDA = 0.3`,
   `GAMA_BIPNMDA = 0.07`, `NEWVES_BIPNMDA = 0.002`, `TAU1NMDA_BIPNMDA = 60.0`,
   `TAU_SACINHIB = 30.0`, `E_SACINHIB = -60.0`, `GABAMOD_PD = 0.33`, `GABAMOD_ND = 0.99`,
   `ACHMOD_SIMPLERUN = 0.33`, `B2GNMDA_CODE = 0.5`, `B2GNMDA_PAPER = 2.5`,
   `N_SYNAPSES_EACH_TYPE = 282`), noise levels (`NOISE_SD_LEVELS = [0.0, 0.1, 0.3, 0.5]`),
   8-direction angles (0, 45, 90, 135, 180, 225, 270, 315), and trial count (`NUM_TRIALS = 20` per
   paper n ~ 12-19 cells rounded up). Satisfies REQ-4.

7. **Download the supplementary PDF and attach to the existing paper asset via corrections.**
   Download `https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf`
   (approximately 1.4 MB) into
   `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/files/NIHMS766337-supplement.pdf`
   by writing a corrections overlay file at
   `tasks/t0046_.../corrections/replace_paper_10.1016_j.neuron.2016.02.013.json` that appends the
   new file to the paper's `files` list and records the download provenance. Do NOT mutate the
   completed t0002 folder directly (immutability rule). Validate via
   `uv run python -m arf.scripts.aggregators.aggregate_papers --ids 10.1016_j.neuron.2016.02.013 --format json --detail full`
   which must show the supplementary PDF in the `files` list. Satisfies REQ-14.

### Milestone C: NEURON bootstrap and cell build

8. **Copy and adapt the three NEURON helper patterns.** Create `code/neuron_bootstrap.py` from
   `tasks/t0022_modify_dsgc_channel_testbed/code/neuron_bootstrap.py` (approximately 55 lines):
   renamed sentinel env var to `_T0046_NEURONHOME_BOOTSTRAPPED`, re-exec logic, `sys.path.insert` of
   `NEURONHOME/lib/python`, `os.add_dll_directory(NEURONHOME/bin)` on Windows. Create
   `code/build_cell.py` by copying the `_sources_dir_hoc_safe`, `load_neuron`, and `build_dsgc`
   functions from `tasks/t0008_port_modeldb_189347/code/build_cell.py:120-175` (approximately 60
   lines) and the `SynapseCoords` dataclass + `read_synapse_coords` + `get_cell_summary` from lines
   63-74 and 192-208 (approximately 40 lines). Create `_assert_bip_positions_baseline` inside
   `code/build_cell.py` from
   `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py:109-127` (approximately 20
   lines). Every function header must carry a leading comment citing the source task and line range.
   Do NOT use `from tasks.t0008_...` or `from tasks.t0020_...` imports. Satisfies REQ-2, REQ-4.

9. **Compile MOD files on Windows.** Write `code/run_nrnivmodl.cmd` that invokes the MinGW-gcc
   toolchain at `C:\Users\md1avn\nrn-8.2.7\mingw` and compiles `code/sources/*.mod` into
   `code/sources/x86_64/nrnmech.dll`. Run once; verify `x86_64/nrnmech.dll` exists. If compile
   fails, document the error in `logs/` and adjust MOD files minimally (record every adjustment as a
   potential discrepancy in the audit per task_description.md). Expected: dll loads without errors
   when `neuron.h.nrn_load_dll(str(NRNMECH_DLL))` is called.

### Milestone D: Simulation driver and per-figure reproductions

10. **[CRITICAL] Write the simulation driver.** Create `code/run_simplerun.py` exposing
    `def run_one_trial(*, exptype: ExperimentType, direction: Direction, trial_seed: int, flicker_var: float = 0.0, stim_noise_var: float = 0.0, b2gnmda_override: float | None = None, record_soma_v: bool = True, record_spikes: bool = False) -> TrialResult`
    where `TrialResult` is a frozen dataclass with fields `soma_v_trace: np.ndarray`,
    `time_trace: np.ndarray`, `peak_psp_mv: float`, `spike_times_ms: list[float]`. The function: (a)
    calls `ensure_neuron_importable()`; (b) loads `dsgc_model_exact.hoc`; (c) instantiates DSGC; (d)
    sets `h.flickerVAR = flicker_var`, `h.stimnoiseVAR = stim_noise_var`,
    `h.b2gnmda = b2gnmda_override if b2gnmda_override is not None else B2GNMDA_CODE`; (e) calls
    `h.simplerun(int(exptype), int(direction))` which internally rebinds `achMOD = 0.33` and sets
    all condition-specific globals; (f) calls `h.placeBIP()` (required after any global change per
    `research/research_code.md` Lesson Learned 5); (g) asserts BIP positions unchanged via
    `_assert_bip_positions_baseline`; (h) runs `h.run()` to `tstop = 1000 ms`; (i) reads soma v and
    (if `SpikesOn`) spikes. Returns `TrialResult`. Satisfies REQ-5, REQ-6, REQ-7, REQ-8, REQ-9,
    REQ-10.

11. **Run Figure 1-2 reproduction (control vs AP5, subthreshold).** Create `code/run_fig1_fig2.py`.
    For `gNMDA in [0.5]` (primary, code value) and for `gNMDA in [0.0, 0.5]` (control vs AP5
    analogue where `gNMDA = 0` mimics bath AP5 per `research/research_papers.md`), sweep 8
    directions x 20 trials x 2 conditions (`exptype = 1 CONTROL`, direction toggles PD/ND) with
    `flicker_var = 0`. For each direction-trial, record the peak soma V above `v_init = -65 mV` (=
    the PSP amplitude in mV). Also run the secondary sweep at `gNMDA = 2.5` (paper value) as a
    parallel pass. Compute per-condition PD PSP mean +/- SD, ND PSP mean +/- SD, and the slope angle
    of the control-vs-AP5 scatter per paper Figure 1H (slope = `atan2(delta_control, delta_ap5)`
    over the 8 directions). Write CSV outputs to `results/data/fig1_psp.csv` and
    `results/data/fig1_slopes.csv`. Validation gate: if any trial returns NaN or peak > 30 mV, halt
    and inspect the trial trace before proceeding. Satisfies REQ-6, REQ-7, REQ-8.

12. **Run Figure 4-5 reproduction (High-Cl- and 0 Mg2+ analogues).** Create `code/run_fig4_fig5.py`.
    For Figure 4 (`exptype = HIGH_CL = 3`), sweep 8 directions x 20 trials recording PSPs; expect
    slope 45.5 +/- 3.7 degrees (additive) and PD-reversal in >= 50% of trials (paper: 15/20 = 75%).
    For Figure 5 (`exptype = ZERO_MG = 2`, which sets `Voff_bipNMDA = 1`), sweep 8 directions x 20
    trials; expect slope 45.5 +/- 5.3 degrees. Write CSVs to `results/data/fig4_psp.csv`,
    `results/data/fig5_psp.csv`. Satisfies REQ-9, REQ-10.

13. **Run Figure 3 NMDAR sweep.** Create `code/run_fig3_nmda_sweep.py`. Sweep `b2gnmda` in
    `[0.0, 0.25, 0.5, 1.0, 1.5, 2.5]` (0 = AP5 analogue; 0.5 = code; 2.5 = paper claim), 8
    directions x 20 trials per value. Compute DSI vs `gNMDA` and write to
    `results/data/fig3_gnmda_sweep.csv`. Satisfies REQ-8.

### Milestone E: Noise conditions (Figures 6-8)

14. **Run Figure 6 noisy subthreshold.** Create `code/run_fig6_noise.py`. For each
    `flicker_var in [0.0, 0.1, 0.3, 0.5]`, for each `exptype in [CONTROL, ZERO_MG]`, sweep 8
    directions x 20 trials (no `stim_noise_var` override — Figure 6 uses luminance noise only).
    Per `research/research_code.md` the driver is already present in `placeBIP()`; the
    implementation only parameterises it. Record PD PSP, ND PSP, DSI per noise level per condition.
    Write `results/data/fig6_noise.csv`. Satisfies REQ-11.

15. **Run Figure 7 noise-free subthreshold ROC / accuracy.** Create `code/run_fig7_roc.py`. For each
    `exptype in [CONTROL, AP5=control-with-gNMDA=0, ZERO_MG]`, collect 20 trials per direction x 8
    directions = 160 trials per condition. Compute ROC AUC of PD-trial PSP peaks vs baseline
    (pre-stimulus 100 ms window) using `sklearn.metrics.roc_auc_score`. Expected noise-free AUC:
    0.99 control / 0.98 AP5 / 0.83 0Mg, tolerance +/-0.05. Write `results/data/fig7_roc.csv`. Also
    run at the four noise levels and write `results/data/fig7_roc_noise.csv` for the figure's
    noise-ROC panel. Satisfies REQ-11, REQ-12.

16. **Run Figure 8 suprathreshold.** Create `code/run_fig8_spikes.py`. For each
    `exptype in [CONTROL, AP5=control-with-gNMDA=0, ZERO_MG]`, enable `SpikesOn = 1` (sets
    `TTX = 0`, somatic gNa on), sweep 8 directions x 20 trials x four noise levels. Record spikes
    per trial via `NetCon` from `soma._ref_v` with threshold 0 mV. Compute per-condition: AP DSI
    using
    `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics.compute_dsi`;
    per-angle peak-Hz; per-condition PD-failure rate (fraction of PD trials with zero spikes).
    Qualitative checks per paper: DSI preserved under AP5; DSI reduced in 0 Mg2+; PD-failure rate
    increases under AP5. Also compute AP ROC AUC (control vs AP5, control vs 0 Mg2+) under noise.
    Write `results/data/fig8_spikes.csv`. Satisfies REQ-13.

### Milestone F: Audit, metrics, and figure rendering

17. **Compute metrics and write `results/metrics.json`.** Create `code/compute_metrics.py`. Read
    every `results/data/*.csv` produced above. For each reproduction condition (control_gnmda05,
    control_gnmda25, ap5, zero_mg, high_cl, noise_0, noise_10, noise_30, noise_50) produce a variant
    dict containing: `direction_selectivity_index` (on PSP peaks; additionally on AP counts for fig8
    variants); `tuning_curve_hwhm_deg` (fig8 only; `null` for subthreshold variants);
    `psp_pd_mean_mv`, `psp_pd_sd_mv`, `psp_nd_mean_mv`, `psp_nd_sd_mv`, `slope_angle_deg`,
    `slope_angle_sd_deg`, `roc_auc` (fig7 variants only), `pd_failure_rate` (fig8 variants only).
    Write `results/metrics.json` using the explicit multi-variant format per
    `arf/specifications/metrics_specification.md`. Use `None` for measurements that do not apply
    (e.g., `tuning_curve_hwhm_deg = null` for subthreshold variants; `tuning_curve_rmse = null` for
    every variant — explicitly not-applicable per Approach section). Satisfies REQ-15, REQ-16,
    REQ-17, REQ-20.

18. **Generate figure PNGs.** Create `code/render_figures.py`. Import
    `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_cartesian_tuning_curve, plot_polar_tuning_curve, plot_multi_model_overlay`.
    For each paper figure (1, 2, 3, 4, 5, 6, 7, 8), render a PNG under `results/images/` with
    clearly labelled axes, matching ranges to the paper figure, and an overlay of paper values vs
    reproduction values where applicable: `fig1_psp_vs_angle.png`, `fig2_imk801_psp.png`,
    `fig3_gnmda_sweep.png`, `fig4_highcl_psp.png`, `fig5_zeromg_psp.png`,
    `fig6_noise_dsi_by_sd.png`, `fig7_roc_noise.png`, `fig8_spike_tuning_and_failures.png`. Override
    y-axis labels to "PSP amplitude (mV)" where needed. Satisfies REQ-19.

19. **Populate the answer asset.** Create the answer asset at
    `tasks/t0046_.../assets/answer/poleg-polsky-2016-reproduction-audit/` with `details.json`,
    `short_answer.md`, and `full_answer.md` per `meta/asset_types/answer/specification.md`. The
    `full_answer.md` contains: (a) the one-paragraph question framing; (b) the audit table with one
    row per basic parameter (Ra, g_pas, V_rest, Cm, soma gNa/gKv/gKm, dend gNa/gKv/gKm, n_bipNMDA,
    gama_bipNMDA, newves_bipNMDA, tau1NMDA, tauAMPA, tau_SACinhib, e_SACinhib, tauACh, e_nACh,
    b2gnmda, b2gampa, s2ggaba, s2gach, maxves, Vtau, lightspeed, lightwidth, SACdur, dt, tstop,
    countON, numsyn) comparing Paper / ModelDB code / Reproduction / Match? / Citation; (c) the
    figure-reproduction table with one row per paper figure 1-8 (separate rows for PD PSP, ND PSP,
    slope, DSI, ROC AUC, PD-failure rate where applicable); (d) the discrepancy catalogue containing
    the pre-flagged four (gNMDA 2.5 vs 0.5; 177 vs 282; noise driver present but zeroed; dendritic
    Nav 2e-4 not zero) plus the main.hoc-override corrections (n_bipNMDA 0.3 vs 0.25, gama 0.07 vs
    0.08, newves 0.002 vs 0.01, tau1NMDA 60 vs 50, tau_SACinhib 30 vs 10, e_SACinhib -60 vs -65,
    achMOD simplerun rebind) plus any new discrepancies found during implementation; (e) the
    reproduction-bug list (any place our port diverges from ModelDB code; each must be fixed before
    sign-off); (f) the morphology-provenance note (paper used the HOC-embedded reconstruction; t0005
    SWC is a different cell; we used the paper's); (g) the one-paragraph project-level summary
    stating whether Poleg-Polsky's PSP + slope + ROC claims hold under faithful reimplementation and
    whether Figure 8 depends on undocumented details. Satisfies REQ-15, REQ-16, REQ-17, REQ-18.

## Remote Machines

None required. The task runs entirely on the local Windows workstation under NEURON 8.2.7 + NetPyNE
1.1.1 at `C:\Users\md1avn\nrn-8.2.7` validated by `[t0007_install_neuron_netpyne]`. Paper
task_description.md explicitly forbids Vast.ai and paid services. Estimated total simulation budget
fits in an afternoon.

## Assets Needed

Input assets this task depends on:

* Paper asset `10.1016_j.neuron.2016.02.013` (Poleg-Polsky and Diamond 2016 Neuron) from
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
  — the paper being reproduced.
* Library asset `modeldb_189347_dsgc` from
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/` — source of the
  eleven ModelDB source files to copy (NOT imported). The HOC/MOD files are verbatim copies of the
  ModelDB 189347 release.
* Library asset `tuning_curve_viz` from
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/` — imported through
  its registered module path for tuning-curve plots.
* Library asset `tuning_curve_loss` from
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/` — imported
  through its registered module path for the Figure 8 secondary suprathreshold DSI helper.
* External resource: PMC supplementary PDF
  `https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf`
  (downloaded in Step 7 and attached to the existing paper asset via corrections overlay).
* NEURON toolchain from `[t0007_install_neuron_netpyne]` at `C:\Users\md1avn\nrn-8.2.7`.

## Expected Assets

Matches `task.json` `expected_assets`: `{ "library": 1, "answer": 1 }`.

* **Library asset** `modeldb_189347_dsgc_exact` at
  `tasks/t0046_.../assets/library/modeldb_189347_dsgc_exact/`. Contains `details.json`,
  `description.md`, and `sources/` (eleven ModelDB files plus `dsgc_model_exact.hoc`). The Python
  driver lives in `tasks/t0046_.../code/` with `module_paths` pointers in `details.json` per
  `meta/asset_types/library/specification.md`.
* **Answer asset** `poleg-polsky-2016-reproduction-audit` at
  `tasks/t0046_.../assets/answer/poleg-polsky-2016-reproduction-audit/` containing `details.json`,
  `short_answer.md`, and `full_answer.md` with audit table, figure-reproduction table, discrepancy
  catalogue, reproduction-bug list, and project-level summary paragraph.

## Time Estimation

* Research: done (papers, internet, code stages all complete per their frontmatter).
* Implementation scaffolding (Steps 1-9): approximately 4-6 hours. Dominant cost is the verbatim
  source-file copy and the Windows MOD compile loop (MinGW invocations plus error triage).
* Figure-1 through Figure-8 simulation runs (Steps 10-16): approximately 4-8 hours total. Per
  `research/research_code.md` a 20-trial run takes roughly 1.5 minutes; a full sweep is
  approximately (8 angles x 20 trials) x (3 base conditions + 1 High-Cl- + 5 noise levels + 1 gNMDA
  sweep) ~ approximately 1,500-3,000 trials => 40-75 minutes plus wall time for I/O, logging, and
  per-trial placeBIP overhead.
* Metric computation, figure rendering, and audit-asset authoring (Steps 17-19): approximately 3-4
  hours.
* Total implementation wall-clock: approximately 1-2 local-CPU working days (consistent with the
  "1-2 days" estimate in task_description.md).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| MOD file compilation fails under NEURON 8.2.7 + MinGW on Windows (known sensitivity with `USEION ca` warnings in `HHst.mod` per research_internet.md) | Medium | Blocks all simulation | Follow the MinGW-gcc recipe validated in `[t0007]` and used by `[t0008]`, `[t0020]`, `[t0022]`. Document every toolchain adjustment as a potential discrepancy per task_description.md rather than silently editing MOD files. If compile fails, run `nrnivmodl -verbose` and attach the full log to `logs/`. |
| Morphology port subtly differs from the paper (section ordering, ON/OFF cut, diameter taper) | Low | Invalidates every per-dendrite metric | Use the bundled `RGCmodel.hoc` verbatim (no SWC substitution). Run `code/verify_morphology.py` smoke test that asserts `countON == 282`, `numsyn == 282`, section count == 1 soma + 350 dend, ON/OFF cut at `z >= -0.16 * y + 46`. Compare against t0008's identical metrics. |
| Noise driver behaves differently from paper Figures 6-8 (`placeBIP()` was authored but never exercised at non-zero SD in the shipped code, so it may carry latent bugs) | Medium | Figures 6-8 ROC AUC and DSI-by-noise targets miss | Inspect `placeBIP()` output vectors at SD = 0.1, 0.3, 0.5 before running the full sweep: assert the empirical SD of `basenoise` and `ampnoise` Vectors matches the requested `flickerVAR` within 5%. If the noise distribution is not Gaussian-centred on the baseline, document in the audit as a new discrepancy and fall back to seeding `rnoise` explicitly. |
| gNMDA pick ambiguity (paper Fig 3E says 2.5 nS; `main.hoc` says 0.5 nS) causes Figure 1 PSP amplitudes to land outside tolerance | Medium | Primary pass criterion on Fig 1 fails | Run the primary reproduction at 0.5 nS (code) and a secondary pass at 2.5 nS (paper). Report both; if the code value lands outside tolerance and the paper value lands inside, document as a code-vs-paper discrepancy (paper claim wins on the specific metric). If neither lands inside, log as a reproduction bug and investigate the `main.hoc` override chain. |
| Jahr-Stevens Mg-block parameter mismatch (research_internet.md extracted MOD defaults n=0.25, gama=0.08; main.hoc overrides to n=0.3, gama=0.07 per research_code.md) | Low | Wrong parameter in audit column | Use `main.hoc` values as the canonical code-column, per research_code.md's correction table. Add the MOD-default-vs-main.hoc-override row as a discrepancy catalogue entry. |
| `achMOD` global silently rebound by `simplerun()` causes Python-level overrides to be ignored | High | Subtle bug: runs without error but with unintended parameters | Do NOT expose `achMOD` as a Python driver knob. The plan captures this explicitly (Approach section) and `run_simplerun.py` calls `h.simplerun($1, $2)` directly after setting `flicker_var`, `stim_noise_var`, and `b2gnmda` (which `simplerun()` does not overwrite). Add an assertion after `simplerun()` that `h.achMOD == 0.33` to surface any future regression. |

## Verification Criteria

* **Plan verificator passes** with zero errors: run
  `PYTHONIOENCODING=utf-8 uv run python -u -m arf.scripts.verificators.verify_plan t0046_reproduce_poleg_polsky_2016_exact`
  and expect exit code 0.
* **Library asset exists and passes its verificator**: run
  `uv run python -u -m arf.scripts.verificators.verify_library_asset t0046_reproduce_poleg_polsky_2016_exact modeldb_189347_dsgc_exact`
  and expect exit code 0.
* **Answer asset exists and passes its verificator**: run
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset t0046_reproduce_poleg_polsky_2016_exact poleg-polsky-2016-reproduction-audit`
  and expect exit code 0.
* **Task-file verificator passes**: run
  `uv run python -u -m arf.scripts.verificators.verify_task_file t0046_reproduce_poleg_polsky_2016_exact`
  and expect exit code 0.
* **Metrics file is valid**: run
  `uv run python -u -m json.tool tasks/t0046_.../results/metrics.json` and expect valid JSON
  containing the explicit multi-variant schema per `arf/specifications/metrics_specification.md`.
* **Requirement coverage check**: `grep -c "REQ-" tasks/t0046_.../plan/plan.md` returns at least
  REQ-1 through REQ-20, and every `REQ-*` token appears in at least one step of `## Step by Step`
  (grep confirms cross-reference).
* **Figure PNGs exist**: confirm `ls tasks/t0046_.../results/images/fig{1,2,3,4,5,6,7,8}_*.png`
  lists eight or more files, each non-empty.
* **Pass criterion assertion**: the answer asset's figure-reproduction table must show each of
  REQ-6, REQ-9, REQ-10, REQ-12, REQ-13 as "match" (within the tolerances in task_description.md's
  Pass Criterion) or flag the miss with numerical evidence in the reproduction-bug list.
* **Discrepancy catalogue completeness**: the answer asset's catalogue contains at least the four
  pre-flagged items (gNMDA, synapse count, noise driver, dendritic Nav) plus the six main.hoc
  override corrections (n=0.3, gama=0.07, newves=0.002, tau1NMDA=60, tau_SACinhib=30,
  e_SACinhib=-60) — at least ten rows total before any new discoveries.
* **Supplementary PDF attached**: run
  `uv run python -u -m arf.scripts.aggregators.aggregate_papers --ids 10.1016_j.neuron.2016.02.013 --format json --detail full`
  and confirm that the `files` list contains `NIHMS766337-supplement.pdf` (from the corrections
  overlay applied to the paper asset).
