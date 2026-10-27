---
spec_version: "1"
task_id: "t0131_rd1_na_k_remodelling_dsgc_dsi"
research_stage: "code"
tasks_reviewed: 24
tasks_cited: 14
libraries_found: 18
libraries_relevant: 5
date_completed: "2026-10-27"
status: "complete"
---
# Research Code: rd1-like Na/K Remodelling of the DSGC Model

## Task Objective

Task t0131 scales the soma and axon-initial-segment (AIS) voltage-gated Na and K conductances of the
project's Bed B compartmental DSGC (NEURON, 68-d parameter vector) to mimic the researcher's rd1 vs
WT data (`SomeResults.pdf`: +100 mV clamp with about 1.7x sustained outward current and a much
smaller Na transient; collapsed +60 pA evoked firing; elevated spontaneous firing). Part 1
calibrates a gNa x gK scaling grid from voltage-clamp data only, Part 2 tests the scaling
out-of-sample in current clamp, Part 3 measures signed antipodal DSI on 5-10 reference cells, and
Part 4 checks the researcher's toy input-output model. This file lists what existing project code
and data can be reused, with exact paths and signatures, and which pieces are missing.

Method note: `arf/scripts/aggregators/` in this worktree contains no `aggregate_libraries.py`,
`aggregate_answers.py` or `aggregate_papers.py`, so those two enumerations could not follow rule 9.
Libraries were enumerated from the git-tracked `tasks/*/assets/library/*/details.json` files, and no
answer assets were enumerated (none is needed for code reuse here). The task list used
`aggregate_tasks --status completed --format ids` (122 completed tasks). Task folders were then read
directly for code, because no aggregator exposes `code/` directories. No corrections overlay was
applied to library metadata.

## Library Landscape

Eighteen library assets exist under `tasks/*/assets/library/`. Only five bear on this task. Library
code is the only code that may be imported across tasks.

* `de_rosenroll_2026_dsgc_ais_dendritic_spike` v0.1.0, created by [t0080]. Relevant and the primary
  source. Modules: `code/apply_params.py` (`apply_parameter_vector`), `code/constants.py`
  (`ParameterVector`, `ParamIndex`, `Tier`), `code/trial_helpers.py`, `code/parametric_placer.py`,
  `code/recorder.py`, `code/build_cell_ais.py`, `code/extend_with_ais.py`, `code/paths.py`, and the
  13 MOD sources `code/mods/*.mod`. Import path:
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.<module>`.
* `procedural_dsgc_morphology_generator` v0.1.0, created by [t0090]. Relevant: it builds the cell
  from the 14-d morphology vector. Import path
  `tasks.t0090_morphology_generator_diversity_test.code.generator` / `...code.morphology_params`
  (`MorphologyParams`, `MorphologyResult`).
* `procedural_dsgc_morphology_generator_fix` v0.1.0, created by [t0092]. Relevant and mandatory: it
  patches a soma-area bug in [t0090] (the unpatched generator gives a zero-area soma and NaN
  voltage). Entry points `generate_fixed_morphology` and `insert_baseline_channels`
  (`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix` /
  `...code.baseline_channels`).
* `de_rosenroll_2026_dsgc` v0.1.0, created by [t0024]. Relevant indirectly: its vendored
  `assets/library/de_rosenroll_2026_dsgc/sources/nrnmech.dll` provides the `HHst`, `cad` and
  `Exp2NMDA` mechanisms, and `code/ar2_noise.py` provides the AR(2) noise used by the synaptic
  drive. The [t0090] generator loads this DLL itself.
* `de_rosenroll_2026_dsgc_ais` v0.1.0 (created by t0078): superseded by the [t0080] library for this
  task (older `*t78` MOD suffixes). Not used.

The other 13 libraries (ModelDB 189347 ports, tuning-curve scoring and visualisation, minimal DSGC
variants, Poleg-Polsky reproductions, `dsgc_active_channel_pack`) are Bed A or older models and are
irrelevant. No library reflects a correction or replacement, but this could not be confirmed through
the aggregator because it is absent.

## Key Findings

### The cell model: build path and what "soma/AIS gNa and gK" mean

The evaluator in [t0129] builds a cell in this order (`tasks/t0129_.../code/evaluator.py`,
`_ensure_worker_cell` then `_ensure_synapse_bundle`): `split_68d_vector` splits the 68-d vector into
54-d electrophys and 14-d morphology; `morphology_params_from_vector` converts the morphology part
to `MorphologyParams`; `build_cell` (`generator_wrapper.py`) calls t0092 `generate_fixed_morphology`
and `insert_baseline_channels`; `apply_parameter_vector` (identical in [t0080], [t0129]) writes
channels; `setup_synapses_parametric` builds the synaptic bundle. The built cell has soma
`soma_t90`, AIS sections `ais_proximal_t90` and `ais_distal_t90`, and 19 dendrite sections for the
vector tested. I verified this by running the [t0129] code on a LEGIT vector (see Local
Feasibility).

Na and K conductances relevant to the remodelling, all in S/cm2, with the 54-d `ParamIndex` slot
(`constants_electrophys.py` in [t0129], same in [t0080]):

| Channel (MOD SUFFIX) | Current | Where it is written | Slot |
| --- | --- | --- | --- |
| `nav16t80` (Nav1.6, `m^3 h`, erev 50 mV) | Na | soma slot 0, AIS slot 4, primary 1, mid 2, terminal 3 (overlaid by slot 52) | 0-4, 52 |
| `napt80` (persistent Na) | Na | soma 10, primary 11, mid 12, terminal 13 (not on AIS; terminal overlaid by slot 53) | 10-13, 53 |
| `nart80` (resurgent Na) | Na | uniform on soma and dendrites, slot 27 | 27 |
| `HHst` `gnabar` / `gkbar` | Na / K | MOD defaults 0.12 and 0.036 S/cm2 on soma, dendrites, and both AIS sections | not in vector |
| `kv3t80` (Kv3, erev -85 mV) | K | soma 5, primary 6, mid 7, terminal 8, AIS 9 | 5-9 |
| `kdrt80` (delayed rectifier) | K | uniform soma and dendrites, slot 25 | 25 |
| `kv4t80` (A-type) | K | uniform soma and dendrites, slot 26 | 26 |
| `kv7t80` (M-type) | K | uniform soma and dendrites, slot 31; permitted on AIS but never written there | 31 |
| `bkt80`, `skt80`, `skahpt80` | Ca-activated K | stratified (slots 15-24), slow AHP slots 32-33 | 15-24, 32-33 |

All `*t80` mechanisms use `NONSPECIFIC_CURRENT` with a GLOBAL `erev` (Na 50 mV, K -85 mV), so their
currents are not recorded in the `ina`/`ik` ion pools; only `HHst` writes `ina`/`ik` (ions `ena` =
50 mV and `ek` = -77 mV are NEURON defaults). To read currents per channel, sum the `i_<suffix>`
range variables per segment, plus `ina`/`ik` for `HHst`.

Key facts that matter for the calibration design:

* `HHst.gnabar` and `gkbar` are never written by any task in the lineage ([t0080], [t0090], [t0092],
  [t0129]); every compartment, including the AIS, keeps the MOD defaults 0.12 and 0.036 S/cm2
  (confirmed by reading the values off a built cell). This is a fixed baseline Na/K background that
  is NOT in the 68-d vector. A "soma plus AIS gNa scale" must decide explicitly whether to scale
  `HHst` as well as the `nav16t80` slots; I recommend scaling both, and recording that choice.
* The LEGIT cohort is dominated by `nav16t80` (soma median 0.85, AIS median 2.5 S/cm2, versus `HHst`
  0.12). K is spread across `kdrt80` (median 0.36), `kv4t80` (0.47), `kv3t80` (soma 0.22, AIS 0.11)
  and `kv7t80` (0.33). Sustained outward current in a +100 mV clamp will be set mainly by `kdr`,
  `kv3` and `kv4`, so the "gK scale" should multiply the whole set (`kdrt80`, `kv3t80`, plus
  `HHst.gkbar`, probably `kv4t80`), not a single slot. The [t0080] `apply_params.py` writes density
  by `setattr(seg, f"gbar_{suffix}", ...)`, which is the natural place to apply per-channel scale
  factors after `apply_parameter_vector` returns.
* The uniform `kdr`, `kv4`, `nar` channels exist only on soma and dendrites; AIS gets only
  `nav16t80`, `kv3t80` (written) and `HHst` (default), so an "AIS gK scale" acts on `kv3t80` and
  `HHst.gkbar` only.

### Signed DSI evaluator and the standard protocol

[t0129] `evaluator.py` (729 lines) is the signed antipodal evaluator. Public functions:
`evaluate_68d_vector(*, vector_68d, eval_seeds=None, n_directions=N_DIRECTIONS) -> CellEvalResult`,
`_run_one_trial(*, cell, bundle, direction_deg, seed, eval_seed_index, record_ina_for_atp) -> TrialResult`,
`_signed_antipodal_dsi(*, spike_counts_per_dir)` and `_summarise_trials`. Protocol facts read from
the code:

* Trial length `TSTOP_MS = 1400.0`, `DT_MS = 0.1`, `STEPS_PER_MS = 10`, `V_INIT_MV = -60`,
  `CELSIUS_DEG_C = 36.9`, spike threshold `AP_THRESHOLD_MV = -10` (constants in
  `constants_electrophys.py`). Synaptic drive is a moving bar: `_bar_arrival_times`, AR(2)
  correlated rate noise with `RHO_CORRELATED = 0.6`, GABA release probability set per direction by
  `_gaba_prob_for_direction`, ACh probability `BASE_ACH_PROB = 0.5`, rate bins `RATE_DT_MS = 1.0`.
  Synaptic events are queued through `h.FInitializeHandler`.
* Directions: `angles = d * 360 / n_directions`. The default `N_DIRECTIONS` used by the
  `evaluate_68d_vector` import is 2 (`constants_morphology.py`: antipodal 0/180 deg), and
  `N_EVAL_SEEDS = 3`. The task needs 8 directions, so call with `n_directions=8`; PD = 0 deg and ND
  = 180 deg are both in the 8-direction set. The 8-direction run does not change the signed DSI (it
  uses only 0 and 180); the other six directions are only needed for an angular tuning curve.
* Signed DSI = (R_PD - R_ND) / (R_PD + R_ND) over mean spike counts; `pd_rate_hz` and `nd_rate_hz`
  are mean spike counts divided by 1.4 s. Silence guard: if the summed PD spike count over seeds is
  below `SILENCE_PD_SPIKES_THRESHOLD = 3`, `silence_failed = True` and DSI is set to the sentinel
  `WORST_CASE_DSI = -1.0`. Stability guard: peak Vm outside [-80, +60] mV sets `is_unstable`.
* HH on/off: the evaluator always runs full active channels (no HH-off mode). The EPSP_PASSIVE
  switch used in earlier tasks lives in [t0063]'s `_save_and_zero_hh` for the old Bed A `hh`
  mechanism; for Bed B it would mean zeroing every `gbar_*t80` and `HHst` `gnabar`/`gkbar`. The task
  says to use the EPSP_PASSIVE / IPSP_PASSIVE / FULL trio only where the existing protocol calls for
  it, and the existing signed-DSI evaluator has no such trio, so Part 3 needs no HH-off mode unless
  the researcher asks for it.
* Per-cell parameter dump: `BedBV3MorphProblem._evaluate` appends one JSON line per cell via
  `_append_cell_params` with keys `gen`, `cell_idx`, `param_vector` (68 floats), `dsi_signed`,
  `atp_per_spike_molecules`, `pd_rate_hz`, `nd_rate_hz`, `silence_failed`, `n_errors`. The sink path
  is captured at problem construction (no env var). Caveat: in the saved `results/cell_params.jsonl`
  every row has `cell_idx = 0` (the counter is not shared across worker processes), so use
  `(gen, row order)` rather than `cell_idx` as an identifier.

### Where to get the reference cells: use the t0121 parquet plus the source evaluation dumps

The t0121 parquet does NOT contain parameter vectors, and the t0129 dump contains no LEGIT cells.

* `tasks/t0121_5seed_substrate_rate_canonical_report/results/data/pooled_legit_jointpass_cells.parquet`
  (15,647 bytes, 675 rows) has only 6 columns: `seed`, `source_task_id`, `generation`, `dsi`,
  `pd_rate_hz`, `cell_id`. Counts per `seed`: `t0114_seed7755` 484, `t0106_seed44` 121,
  `t0115_seed9354` 63, `t0112_seed77` 7 (t0113 contributes 0). `dsi` is the vector-sum DSI of the
  older lineage; range 0.5 to 0.9939, `pd_rate_hz` range 30.2 to 122.6 Hz.
* The 68-d vectors are in the source evaluation dumps, key `vector_68d` (also `generation`,
  `dsi_vector_sum`, `pd_rate_hz`, `objective_F_minimised`):
  * `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz` (2.1 MB)
  * `tasks/t0112_t0106_seed77_replicate/results/data/all_evaluations_seed77.json.gz` (1.2 MB)
  * `tasks/t0114_seed7755_no_autostop/results/data/all_evaluations_seed7755.json` (13.4 MB)
  * `tasks/t0115_seed9354_no_autostop/results/data/all_evaluations_seed9354.json` (11.8 MB) The top
    level is `{"evaluations": [...]}`; [t0106] has 3,744 records.
* The LEGIT rule, from `tasks/t0121_.../code/constants.py` and `loaders.py::is_legit_joint_pass`:
  `0.5 <= dsi_vector_sum < 0.9999` AND `pd_rate_hz >= 30.0`. Records are then de-duplicated per seed
  on the exact 68-d vector tuple in file order, and `cell_id = f"{seed}_{seq:04d}"` with `seq`
  counting kept records from 0 (`csv_writers.py::build_pooled_legit_cells`). I re-ran this logic on
  the four dumps and reproduced all 675 rows exactly (121, 7, 484, 63), asserting that each row's
  `dsi` equals `dsi_vector_sum`. So `cell_id` maps one-to-one to a vector.
* The t0129 dump has 5,760 rows but no LEGIT cell: 458 rows have `dsi_signed >= 0.5` but the maximum
  `pd_rate_hz` among them is 15 Hz (only 3 rows have `pd_rate_hz >= 30`, all with `dsi_signed = 0`),
  so the PD >= 30 Hz criterion is empty there. It cannot be the reference-cell source.
* Cohort caveat: the quartiles of the LEGIT parameters are tight (for example `nav16t80` soma
  25th/75th percentile 0.847/0.909, AIS 2.53/2.74), which means many LEGIT cells are near-duplicates
  from one basin, and 72% come from one seed. A fixed-seed random draw of 5-10 cells may be
  redundant; stratify by seed (and ideally by a distance cluster) and report the chosen `cell_id`s.
* The DSI in the parquet is vector-sum DSI from a 2-direction, 3-evaluation-seed protocol. The same
  cell re-run under the signed antipodal evaluator should give a similar PD rate; I confirmed this
  on one cell (see below). Reported signed DSI will differ somewhat, so t0131 must re-evaluate the
  WT-like condition (scale 1.0) rather than trusting the parquet DSI.

### Existing clamp helpers: Bed A only, none for Bed B

No voltage-clamp or current-clamp helper exists for the Bed B procedural cell. Existing helpers are
on the old Bed A SWC cell with Hodgkin-Huxley `hh`:

* [t0063] `code/run_step.py` (268 lines): `h.SEClamp(cell.soma(0.5))` with `dur1/amp1` = 50 ms hold
  at -65 mV, `dur2/amp2` = 200 ms step, `dur3/amp3` = hold, `rs = 0.001` MOhm (`constants.py`),
  records `seclamp._ref_i`, `v`, `t`; `_save_and_zero_hh` / `_restore_hh` zero `hh.gnabar/gkbar`. It
  uses CVode (`enable_cvode`) with `DT_MS = 0.025`. Its clamp-current sign and tight-`rs`
  conventions are directly reusable; the `hh`-specific parts are not. The [t0063] summary reports
  transient inward Na of -13 to -15 nA and a sustained outward current of +1 to +5 nA at -40 to -10
  mV steps on Bed A, 12 trials in 24.6 s.
* [t0064] `code/run_step.py` (246 lines): `h.IClamp(cell.soma(0.5))` with `delay`, `dur`, `amp`
  (nA), a spike `NetCon` at `AP_THRESHOLD_MV`; `constants.py` has `CURRENT_NA_VALUES`,
  `DELAY_MS = 50`, `DURATION_MS = 200`. The Bed A F-I curve had rheobase between 0.1 and 0.2 nA and
  depolarisation block at 2 nA. 12 trials in 79 s.
* [t0049] `code/run_seclamp.py` and `run_seclamp_sweep.py`: SEClamp used to measure synaptic
  conductance; a second example of the SEClamp recording pattern.

The +60 pA, 500 ms step (panel B) and the +100 mV step (panel C) therefore need new code on the Bed
B cell. Scale caution: the 100 mV step is stated as a step "of" 100 mV; whether it is from a holding
potential near -60 to -70 mV to +30 to +40 mV, or a 100 mV increment, is not defined in the task and
must be fixed in the plan (the researcher's PDF should be checked).

### Running NEURON locally on Windows: confirmed feasible, with one setup step

* NEURON 8.2.7 is importable in the project venv through `uv run python`: `neuron.__file__` resolves
  to `C:\Users\md1avn\nrn-8.2.7\lib\python\neuron\__init__.py`, and `h.nrnversion()` reports
  `8.2.7+ HEAD (34cf696+) 2025-05-21`. The `mingw` toolchain ships in that install. Linux uses the
  pip wheel instead ([t0129] `bootstrap.py` handles that, and is a no-op on Windows).
* Two compiled libraries are needed, loaded in this order by [t0090] `generator.py` and [t0080]
  `apply_params.ensure_t80_dll_loaded`: the [t0024] vendored
  `.../de_rosenroll_2026_dsgc/sources/nrnmech.dll` (`HHst`, `cad`, `Exp2NMDA`; tracked in git) and
  the t0080 library `.../t0080_.../code/build/nrnmech.dll` (the 13 `*t80` channels).
* The t0080 DLL path is gitignored (`build/` is in `.gitignore`), so it is ABSENT in this worktree.
  A byte-identical copy (238,838 bytes, verified with `cmp`) is tracked in git at
  `tasks/t0107_t0106_polar_8dir_recheck/code/mods/nrnmech.dll`, built from MOD sources that are
  identical to `tasks/t0080_.../code/mods/*.mod`. It also exists in the main repo at
  `tasks/t0080_.../code/build/nrnmech.dll`. For t0131, copy one of them to
  `tasks/t0131_.../code/build/nrnmech.dll` (gitignored, so not committed) and load it with
  `h.nrn_load_dll`; do not edit the [t0080] `paths.py` constant. The stray `.c`/`.o` files in the
  main repo's t0080 `mods/` folder are `nrnivmodl` build artefacts and are not needed.
* [t0129] reported that `mknrndll` compilation on this workstation "did not produce a loadable DLL
  in the path order the bootstrap expects". That was a recompile problem; loading the existing DLL
  works. I did not attempt recompilation.
* Feasibility test I ran (scratch script in `/tmp`, nothing written to the repo): I loaded the main
  repo's t0080 DLL by overriding `WINDOWS_MOD_BUILD_DLL`, took the first LEGIT record from [t0106]
  (`dsi_vector_sum` 0.82, `pd_rate_hz` 33.8), built the cell in 0.22 s, and ran the [t0129]
  `_run_one_trial` at 0 deg and 180 deg. Result: 46 spikes at 0 deg (32.9 Hz, consistent with the
  33.8 Hz record) and 2 spikes at 180 deg; each 1400 ms trial took about 8.7-9.0 s single-process
  with the Na-current recorders attached. Soma `L` = 8.18 um, `diam` = 8.56 um, area 220 um2.
* Timing implications: one cell, 8 directions, 1 seed is about 72 s (more with 3 seeds, about 216 s)
  at that speed; the [t0129] full run used about 68 core-seconds per cell evaluation on Vast.ai. The
  [t0129] local 4-worker NSGA-II attempt was killed after extrapolating 5-7 days, which concerns
  thousands of evaluations, not the few hundred in this task. A 6 x 6 clamp grid on 10 cells is 360
  short clamp runs, plus DSI runs for at least 2 conditions x 10 cells x 8 directions (about 1,440 s
  with 1 seed, parallelisable over 8 cores). The 36-cell DSI heatmap over the gNa x gK grid is the
  expensive part: 36 x 10 cells x 8 directions x 9 s = about 7.2 core-hours. Subsample the heatmap
  (fewer cells or 2-direction trials) if needed.
* Dropping `record_ina_for_atp` (`record_ina_for_atp=False` in `_run_one_trial`) should speed
  trials; I did not measure by how much.

## Reusable Code and Assets

All items below are either "import via library" (allowed) or "copy into task". Never import from
another task's `code/` unless that task registered it as a library.

### Import via library

* [t0092] library `procedural_dsgc_morphology_generator_fix`: import via library.
  `generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`
  and `insert_baseline_channels(*, h, cell) -> None`
  (`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix`,
  `...code.baseline_channels`; 98 + 33 lines). Do not call [t0090]'s unpatched
  `generate_morphology`.
* [t0090] library `procedural_dsgc_morphology_generator`: import via library. `MorphologyParams` (14
  fields), `MorphologyResult`
  (`tasks.t0090_morphology_generator_diversity_test.code.morphology_params`, 155 lines).
* [t0080] library `de_rosenroll_2026_dsgc_ais_dendritic_spike`: import via library.
  `apply_parameter_vector(*, cell, params: ParameterVector) -> None`
  (`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params`, about 230 lines),
  `ParameterVector(values=...)`, `ParamIndex`, `Tier`, `CHANNEL_SUFFIXES` and related constants
  (`...code.constants`, 547 lines), `setup_synapses_parametric(...)`, `SynapseBundle`
  (`...code.trial_helpers`, about 311 lines), `ensure_t80_dll_loaded(*, h)`. Differences versus the
  [t0129] copies: `trial_helpers`, `parametric_placer`, `build_cell_ais`, `extend_with_ais` differ
  only in import paths (0-2 changed lines); `apply_params` differs by 32 changed lines (mostly the
  DLL-loader delegation); `recorder` differs by 80 lines. `ensure_t80_dll_loaded` needs the DLL at
  the [t0080] `code/build` path, so in t0131 either load the DLL yourself or pre-place the DLL there
  (it is gitignored); copying the loader into t0131 `code/` with a t0131 path constant is safer.
* [t0024] library `de_rosenroll_2026_dsgc`: import via library, indirectly. `generate_ar2_batch`
  (`...code.ar2_noise`) is used by the synaptic drive; the `nrnmech.dll` is loaded by the generator.

### Copy into task

* [t0129] `tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/evaluator.py` (729 lines): copy into
  task. Keep `TrialResult`, `CellEvalResult`, `_run_one_trial`, `_signed_antipodal_dsi`,
  `_summarise_trials`, `evaluate_68d_vector`, `_ensure_worker_cell`, `_ensure_synapse_bundle`. Drop
  `BedBV3MorphProblem` and the pymoo import (about 130 lines), `_append_cell_params`'s lock
  plumbing, and the MI/ATP computations if not needed (they import `atp_per_spike`, `mi_estimator`;
  removing them also removes the `record_ina_for_atp` option; keep
  `recorder.attach_ina_recorders_for_atp` only if per-section Na charge is wanted). Adaptation:
  replace imports of `tasks.t0129_.../code.*` with the t0131 copies or library imports; add
  per-channel scale factors applied after `apply_parameter_vector`; add `n_directions=8`; add a
  tonic bias `h.IClamp` option. About 400-450 lines remain after trimming.
* [t0129] `code/generator_wrapper.py` (about 100 lines): copy into task, or replace with direct
  calls to the [t0092] library: `split_68d_vector`, `morphology_params_from_vector`,
  `hash_morphology_vector`, `build_cell`, `_LIVE_CELLS` (a GC-defence list that must be kept so that
  NEURON sections are not collected).
* [t0129] `code/constants_electrophys.py` (547 lines) and `code/constants_morphology.py` (169
  lines): copy the slices needed (`TSTOP_MS`, `DT_MS`, `STEPS_PER_MS`, `V_INIT_MV`, `CELSIUS_DEG_C`,
  `AP_THRESHOLD_MV`, `RHO_CORRELATED`, `SEED_BASE`, `PD_DIRECTION_DEG`, stability limits,
  `N_PARAMS_54`, `WORST_CASE_*`, `LOWER_BOUNDS_68`/`UPPER_BOUNDS_68`, the suffix tuples,
  `ParamIndex`). Do not import `ParameterVector` from [t0129]; import it from the [t0080] library.
* [t0129] `code/trial_helpers.py` constants and the five private helpers `_bar_arrival_times`,
  `_rates_with_ar2_noise`, `_rates_to_events`, `_gaba_prob_for_direction`, `_count_spikes` are used
  by `_run_one_trial`; they are private in the [t0080] library module, so importing them via library
  is allowed but fragile. Copy them (about 100 lines).
* [t0121] `code/loaders.py::load_evaluations`, `is_legit_joint_pass`, `cell_vector_key` and
  `csv_writers.py::build_pooled_legit_cells` lines 419-464 (about 90 lines): copy into task to
  rebuild the cell-to-vector map from the four dumps in section "Where to get the reference cells".
* [t0063] `code/run_step.py` SEClamp block (about 35 lines) and [t0064] `run_step.py` IClamp block
  (about 25 lines): copy the pattern only, rewritten for Bed B (record `seclamp._ref_i`, `v`, `t` as
  `h.Vector`; sum the per-channel `i_<suffix>` for the Na transient and K sustained split).

### Data assets (read in place, do not copy files)

* `tasks/t0121_.../results/data/pooled_legit_jointpass_cells.parquet` (675 rows, 6 columns).
* The four `all_evaluations_seed*.json[.gz]` dumps listed above (about 28.5 MB in total).
* `tasks/t0129_.../results/cell_params.jsonl` (9.2 MB, 5,760 rows): useful as a source of
  `silence_failed`-labelled cells and of the signed-DSI pairs, not as a LEGIT source. Also
  `tasks/t0129_.../results/data/pareto_front_seed3517.json` for t0129's 9 Pareto cells.
* `SomeResults.pdf` in the repository root is untracked in the main repo; a copy is at
  `tasks/t0131_.../research/inputs/SomeResults.pdf` for this task.

## Lessons Learned

* The most expensive trap is a missing or unloadable MOD library. [t0129] could not load a locally
  compiled DLL and fell back to a Vast.ai machine at $0.965; the tracked, byte-identical `t0107` DLL
  avoids recompilation. Verify `h.nrn_load_dll(...) == 1.0` at the start of every run and fail
  loudly otherwise (as [t0080] does with `assert rc == 1.0`).
* [t0090]'s generator produced a zero-area soma and NaN voltage ([t0092]); never bypass
  `generate_fixed_morphology`.
* The t0126 `pd_rate_hz = 40` placeholder was fabricated; [t0129] replaced it with real rates and
  found that almost no Pareto cell fires above 30 Hz in the signed-DSI protocol. The LEGIT cells
  from [t0106]/[t0112]/[t0114]/[t0115] have real, recorded rates (computed from `pd_spikes` in the
  evaluator), so those 675 cells remain valid references. Rates must always be computed from spike
  counts, with `None`/failure rather than a default when unavailable.
* Local NEURON evaluation is about 9 s per 1400 ms trial; budget wall-clock by core count (8 cores
  here) and avoid dense heatmaps over many cells. [t0129]'s local NSGA-II attempt shows that
  underestimating runtime by 10x is the usual failure mode.
* `cell_idx` in `cell_params.jsonl` is always 0 ([t0129]); do not rely on it as a key.
* Silence guard: any rd1-like cell with fewer than 3 PD spikes over the seeds receives DSI = -1.0
  (`WORST_CASE_DSI`). For the rd1 condition, where collapsed firing is the expected outcome, this
  sentinel would be wrongly read as "reversed preference". Report DSI as `None` plus the spike
  counts for silent conditions instead of using the sentinel (project style: `None` for missing
  data).
* SEClamp only clamps the soma. A fraction of the Na current in this model comes from the AIS and
  dendrites, whose voltage is not controlled, so the clamp transient is a space-clamp-limited
  measure. I did not test this; flag it in the plan as a risk and compare with the researcher's
  whole-cell recording, which has the same limitation.

## Recommendations for This Task

1. Import the morphology, parameter application and synapse code from the [t0092], [t0090], [t0080]
   and [t0024] libraries; copy the [t0129] evaluator, the electrophys constants and the [t0121]
   loaders into `tasks/t0131_.../code/` (as listed above), keeping imports absolute and under
   `tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code`.
2. Reference cells: build the vector table from the four dumps by re-running the t0121 LEGIT + dedup
   logic, assert 675 rows match the parquet `cell_id`s, draw 5-10 cells with a fixed seed stratified
   by seed (the draw should include [t0106] and [t0115] cells rather than only [t0114]), and write
   their `cell_id`s and full 68-d vectors into `tasks/t0131_.../data/reference_cells.jsonl`
   (`cell_params.jsonl`-compatible keys: `param_vector`, `dsi_vector_sum`, `pd_rate_hz`, `cell_id`).
3. Copy `tasks/t0107_t0106_polar_8dir_recheck/code/mods/nrnmech.dll` to
   `tasks/t0131_.../code/build/nrnmech.dll` (gitignored) and write a small loader that loads the
   t0024 DLL first and then this one; do not depend on the gitignored t0080 build path.
4. Implement the scaling as a post-processing step after `apply_parameter_vector`: multiply
   `gbar_nav16t80` (soma, AIS, and optionally dendrites in the second arm) and `HHst.gnabar` by
   `s_Na`, and `gbar_kdrt80`, `gbar_kv3t80`, `gbar_kv4t80` and `HHst.gkbar` by `s_K`. Decide and
   record whether `kv7t80`, the Ca-activated K and the persistent/resurgent Na channels are scaled
   (I suggest leaving them fixed in the base arm). Apply the scale to both soma and the AIS sections
   `ais_proximal_t90` and `ais_distal_t90`.
5. Write new Bed B clamp code using the [t0063]/[t0064] templates: a +100 mV `SEClamp` at
   `soma(0.5)` recording total and per-channel currents, and a `IClamp` at `soma(0.5)` for +60 pA,
   500 ms. Run clamp and current clamp without synapses (no synapse bundle needed).
   `h.celsius = 36.9`, `dt` 0.025 ms or CVode. Fix the +100 mV step definition (increment vs
   absolute) from the PDF before coding.
6. For Part 3, call the copied `evaluate_68d_vector(vector_68d=..., n_directions=8)` after applying
   the scaling; handle silent conditions without the -1.0 sentinel. Parallelise over cells with
   `ProcessPoolExecutor` and `MAX_WORKERS = max(1, (cpu_count() or 4) - 3)`, one NEURON process per
   worker (the [t0129] worker caches the cell by hash, so scale changes must reset the cache: use a
   fresh process or call `apply_parameter_vector` again before scaling).
7. Plan the compute: about 9 s per 1400 ms trial; Part 3 baseline and rd1 conditions for 10 cells
   and 8 directions are about 1,440 core-seconds per seed, but the 36-point DSI heatmap is about 7
   core hours; reduce the heatmap to a 2-direction, 1-seed evaluation or fewer cells.
8. Do not use the [t0129] dump as the LEGIT source (zero cells meet PD >= 30 Hz); its value is as a
   sanity check of the signed-DSI evaluator (e.g. `dsi_signed` and `pd_rate_hz` pairs).
9. Gaps with no prior code: Bed B voltage and current clamp, per-channel current recording, the
   scaling grid, the tonic bias, the toy model for panel D, the three-pulse input drive for Part 4
   and the DSI-vs-scaling heatmap. Nothing was found for a toy rate model; plan to write it.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Provides the `de_rosenroll_2026_dsgc` library with the vendored `nrnmech.dll`
  (`HHst`, `cad`, `Exp2NMDA`) and the AR(2) noise generator used by the synaptic drive.

### [t0049]

* **Task ID**: `t0049_seclamp_cond_remeasure`
* **Name**: Re-measure Fig 3A-E conductances under somatic SEClamp on the deposited DSGC
* **Status**: completed
* **Relevance**: Contains a second SEClamp recording example (`run_seclamp.py`) on a DSGC model.

### [t0063]

* **Task ID**: `t0063_hh_voltage_step_test`
* **Name**: HH voltage-step diagnostic on t0059 substrate (no synapses)
* **Status**: completed
* **Relevance**: Template for a soma SEClamp voltage-step protocol with HH on/off, including sign
  conventions and a tight clamp series resistance; run on the Bed A cell.

### [t0064]

* **Task ID**: `t0064_hh_current_step_test`
* **Name**: HH current-step diagnostic on t0059 substrate (no synapses)
* **Status**: completed
* **Relevance**: Template for a soma IClamp current step, spike detection and F-I curve; run on the
  Bed A cell.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Source of the 13 `*t80` MOD files, the `apply_parameter_vector` implementation,
  `ParameterVector` and the library that [t0129] forked from.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator + diversity test + validation bundle
* **Status**: completed
* **Relevance**: Provides the procedural morphology generator library and `MorphologyParams` /
  `MorphologyResult` (14-d morphology to cell).

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose why t0090 procedural cells produce no action potentials
* **Status**: completed
* **Relevance**: Provides `generate_fixed_morphology` (soma-area fix) and
  `insert_baseline_channels`; the only valid cell-construction path.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long 2-direction NSGA-II at 300 gens, 1 seed, 3 trials (ratio DSI + PD-rate)
* **Status**: completed
* **Relevance**: Source dump with 121 LEGIT cells; `all_evaluations_seed44.json.gz` holds the 68-d
  vectors; the cell used in my feasibility test came from here.

### [t0107]

* **Task ID**: `t0107_t0106_polar_8dir_recheck`
* **Name**: 8-direction polar re-evaluation of 10 random top-50 t0106 cells
* **Status**: completed
* **Relevance**: Precedent for an 8-direction polar re-evaluation of LEGIT-lineage cells. Holds the
  only git-tracked build of the t0080 `nrnmech.dll` (identical to the main-repo build), usable
  without recompiling.

### [t0112]

* **Task ID**: `t0112_t0106_seed77_replicate`
* **Name**: Seed-77 minimum-change replicate of t0106 long 2-direction NSGA-II
* **Status**: completed
* **Relevance**: Source dump with 7 LEGIT cells in the pooled parquet.

### [t0114]

* **Task ID**: `t0114_seed7755_no_autostop`
* **Name**: Seed-7755 NSGA-II replicate of t0106 with auto-stop disabled
* **Status**: completed
* **Relevance**: Source dump with 484 of the 675 LEGIT cells (13.4 MB
  `all_evaluations_seed7755.json`).

### [t0115]

* **Task ID**: `t0115_seed9354_no_autostop`
* **Name**: Seed-9354 NSGA-II replicate of t0106 with auto-stop disabled
* **Status**: completed
* **Relevance**: Source dump with 63 LEGIT cells and the canonical LEGIT predicate that [t0121]
  copied.

### [t0121]

* **Task ID**: `t0121_5seed_substrate_rate_canonical_report`
* **Name**: Canonical 5-seed substrate-rate report (S-0112-01 batch closed)
* **Status**: completed
* **Relevance**: Dependency of this task; defines the LEGIT rule and produces the pooled parquet
  (675 rows, no parameter vectors).

### [t0129]

* **Task ID**: `t0129_t0126_signed_dsi_real_rates_1seed`
* **Name**: Reproduce t0126 with signed DSI=(PD-ND)/(PD+ND) and real per-cell firing rates
* **Status**: completed
* **Relevance**: Dependency of this task; provides the signed antipodal evaluator, the
  `cell_params.jsonl` dump protocol, and the evidence that local Windows NEURON runs work but are
  slow.
