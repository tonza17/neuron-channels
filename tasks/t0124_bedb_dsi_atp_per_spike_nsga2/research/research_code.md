---
spec_version: "1"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
research_stage: "code"
tasks_reviewed: 17
tasks_cited: 16
libraries_found: 4
libraries_relevant: 4
date_completed: "2026-05-25"
status: "complete"
---
# Research Code: NSGA-II Maximising DSI and Minimising ATP-per-Spike (Bed B + 14-d Morph)

## Task Objective

This task forks the [t0123] 68-d Bed B + 14-d morphology NSGA-II substrate and swaps the two
objectives: drop mutual information (replaced with DSI silence-guarded ratio inherited from [t0122])
and keep ATP-per-spike (Sengupta 2010 recipe inherited verbatim from [t0123]). The direction set is
reduced from [t0123]'s 4 antipodal pairs (0/90/180/270 deg) to the 2 antipodal pair (0/180 deg) that
[t0122] used because DSI only needs one PD/ND pair and ATP-per-spike is direction-independent after
per-spike normalisation. Hard constraints reproduced verbatim are `_POOL_RESTART_EVERY=10`,
`HV_PLATEAU_AUTO_STOP=False`, `POP_SIZE=96`, `N_EVAL_SEEDS=3`, `N_GEN_MAX=60`, `COST_CAP_USD=6.0`,
`SILENCE_PD_SPIKES_THRESHOLD=3`. The headline scientific question is whether the DSGC's
DSI-vs-ATP-per-spike Pareto front shows a Carter-Bean Na/K-overlap penalty and where the top cells
sit relative to the Attwell-Laughlin 2001 47%-of-cortical-signalling-ATP anchor.

## Library Landscape

The project does not ship `aggregate_libraries` in `arf/scripts/aggregators/` (only
`aggregate_categories`, `aggregate_costs`, `aggregate_machines`, `aggregate_metric_results`,
`aggregate_metrics`, `aggregate_suggestions`, `aggregate_task_types`, and `aggregate_tasks` exist).
The library landscape below was enumerated by direct inspection of
`tasks/*/assets/library/*/details.json`. Four registered libraries are directly relevant to t0124;
the rest of the project's library catalogue (e.g., the t0008/t0011/t0012/t0020/t0022/t0046/
t0052/t0053/t0054/t0055/t0057/t0059/t0074/t0078 libraries on the pre-Bed-B lineage) is irrelevant to
a 68-d NSGA-II re-run on the morphology-extended Bed B substrate.

* **`de_rosenroll_2026_dsgc`** (created by [t0024], lives at
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`). Provides
  `build_dsgc_cell` (NEURON bootstrap + RGCmodelGD.hoc + nrnmech.dll load), the AR(2) noise
  generator, the bar-arrival kinematics, and the canonical Bed B dendritic geometry. **Import via
  library** — t0124's `build_cell_ais.py` will call `build_dsgc_cell` then add the AIS extension
  exactly as [t0123] does.

* **`de_rosenroll_2026_dsgc_ais_dendritic_spike`** (created by [t0080], lives at
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/`).
  Provides the 49-d (later 54-d) `ParameterVector` schema, `apply_parameter_vector`, the tiered
  channel write loops (soma / primary / mid / terminal dendrite / AIS), and the compiled MOD pack
  under `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` (the SHARED `nrnmech` namespace
  for every Bed B 68-d run, containing `nav16t80`, `napt80`, `nart80` whose summed `seg.ina` feeds
  the Sengupta recipe). **Import via library** for the ParameterVector + apply_params + AIS
  extension; the MOD library is loaded as a binary asset at runtime via `bootstrap.py`.

* **`procedural_dsgc_morphology_generator`** (created by [t0090], lives at
  `tasks/t0090_morphology_generator_diversity_test/assets/library/procedural_dsgc_morphology_generator/`).
  Provides the `MorphologyParams` frozen dataclass with 14 typed fields (3 ints + 11 floats),
  `MorphologyResult` mirroring the [t0080] `DSGCCellWithAIS` interface, `StabilityKind` enum, and
  the per-parameter bounds (`PARAM_BOUNDS`). **Import via library** — t0124's
  `generator_wrapper.py` consumes `MorphologyParams` and returns `MorphologyResult` exactly as
  [t0122] / [t0123] do.

* **`procedural_dsgc_morphology_generator_fix`** (created by [t0092], lives at
  `tasks/t0092_diagnose_morphology_generator_silence/assets/library/procedural_dsgc_morphology_generator_fix/`).
  Provides `generate_fixed_morphology(*, params, morph_seed) -> MorphologyResult` (drop-in patched
  replacement for [t0090]'s `generate_morphology` that fixes the soma-pt3d area bug causing zero
  spikes under the t0083 best-cell channel set) and `insert_baseline_channels(*, h, cell)`
  (idempotent HHst + cad inserter for soma + dendrites + AIS). C-0093-01 makes this the CANONICAL
  morphology entry point — the unpatched [t0090] `generate_morphology` MUST NOT be called.
  **Import via library** in `generator_wrapper.py`.

All four libraries are imported via full repo-rooted dotted paths (`tasks.tXXXX_*.code.<module>`).
No corrections overlay applies to any of them.

## Key Findings

### ATP-per-spike recipe is fully implemented in [t0123]; copy verbatim with module-path rewrite

[t0123]'s `code/atp_per_spike.py` (254 lines) implements the Sengupta 2010 recipe end-to-end as
specified in `task_description.md` `## ATP-per-Spike Recipe` (lines 91-120 of t0124's task
description). The module exposes
`detect_ap_windows(*, t_ms, v_soma_mv, threshold_mv=-20.0, refractory_ms=2.0, window_half_ms=2.0)`
(returns `list[APWindow]`), the inward-Na charge integrator
`_integrate_inward_na_charge_coulombs(*, t_ms, ina_ma_per_cm2, area_cm2, t_start_ms, t_end_ms)`
(returns charge magnitude in coulombs, applies the leading minus to convert NEURON's inward-negative
convention to positive magnitude and the 1e-3 mA-to-A conversion),
`compute_atp_per_ap(*, t_ms, ina_by_section, ap_windows)` (returns `list[AtpPerApResult]` with the
per-AP per-group breakdown), `compute_atp_per_spike(*, atp_per_ap_results)` (returns float ATP
molecules per spike; `nan` if no APs), and `compute_compartment_breakdown(*, atp_per_ap_results)`
(returns `{"soma", "ais", "dendrites_total"}` dict). The critical unit-conversion factor
`UM2_TO_CM2 = 1.0e-8` is hardcoded (NOT 1e-2 — misreading this is the highest-risk failure mode
per the [t0097] catalogue). The elementary charge `1.602176634e-19 C` and Na/K-ATPase stoichiometry
`3` are also module-level constants. t0124 copies this module verbatim with only the `tasks.t0123_*`
import-path string rewritten to `tasks.t0124_*`. Zero algorithmic changes — the recipe is
direction-independent and the 2-direction protocol is supported as-is.

### seg.ina recorder is implemented in [t0123]; the 2-direction protocol works as-is

[t0123]'s `code/recorder.py` (196 lines) exposes
`attach_ina_recorders_for_atp(*, h, cell) -> InaRecorders` which attaches
`Vector.record(seg._ref_ina, ATP_RECORD_DT_MS)` to every segment in soma + AIS proximal + AIS distal
\+ every dendrite section, captures per-segment `seg.area() * UM2_TO_CM2` once at attach time, and
adds the somatic Vm + time recorders so AP detection can run on the same recording window. The
sampling interval is `ATP_RECORD_DT_MS = DT_MS = 0.1 ms` (NOT the legacy `RECORD_DT_MS = 1.0 ms`
used by the per-synapse recorder — too coarse to capture the ~1-2 ms Na transient). The recorder
is direction-independent and called once per trial regardless of how many directions a cell is run
at. t0124 copies this module verbatim with import-path rewrites only. The 2-direction protocol (PD =
0 deg, ND = 180 deg) reduces trial count from [t0123]'s `12 = 3 seeds * 4 directions` to
`6 = 3 seeds * 2 directions` per cell — halving per-evaluation wall-clock without touching the
recorder.

### DSI silence-guarded ratio is implemented in [t0122] and re-exposed in [t0123]

[t0122]'s `code/evaluator.py` (`_summarise_trials` line 346, `_vector_sum_dsi` line 322) implements
the silence-guarded vector-sum DSI: pd_spikes_sum is computed over the 3 PD-direction trials; if
`pd_spikes_sum < SILENCE_PD_SPIKES_THRESHOLD` (= 3) the DSI is forced to 0.0 — equivalent to the
`-1.0` worst-case sentinel after applying `WORST_CASE_DSI = -1.0` at the outer-most fallback.
Otherwise `_vector_sum_dsi` computes `|sum_dir(spikes_dir * unit_vec(dir))| / sum_dir(spikes_dir)`,
which for 2 antipodal directions reduces to `(R_PD - R_ND) / (R_PD + R_ND)` — exactly the formula
in t0124's task description (lines 77-83). [t0123]'s `evaluator.py` line 137 retains
`SILENCE_PD_SPIKES_THRESHOLD = 3` and line 442 calls `_vector_sum_dsi` identically. The threshold
constant and the vector-sum reduction must be carried into t0124 verbatim and the DSI lifted from a
TRACKED DIAGNOSTIC ([t0123]) to a HEADLINE OPTIMISED OBJECTIVE (t0124).

### Project-policy NSGA-II driver lives in [t0115] and is forked verbatim by [t0122] / [t0123]

The 763-line `nsga2_driver.py` first carrying the "auto-stop disabled per project policy" convention
is [t0115]'s. [t0122] and [t0123] are 776-line and 775-line forks (Pareto plot / pop restart code
identical). All three encode `_POOL_RESTART_EVERY: int = 10` at line 104-105 with an assert and a
print at startup confirming the value. `_build_termination` (lines 200-211 in [t0123]) constructs
`TerminationCollection(MaximumGenerationTermination(n_max_gen=n_max_gen), CostWatchdogTermination(watchdog=cost_watchdog, seed=seed), OperatorStopTermination(stop_path= stop_path))`
— there is NO `HVPlateauTermination` in the live collection (the class remains importable from
`hv_plateau_watchdog.py` only for the smoke-gate REQ-8 introspection check and the offline replay
detector). `PerGenerationPoolRestart` (lines 376-429 in [t0123]) closes / terminates the current
`multiprocessing.Pool`, creates a fresh `Pool(processes=n_workers)`, and swaps
`problem.elementwise_runner` to a new `StarmapParallelization` every `gen % 10 == 0`. t0124 forks
[t0123]'s `nsga2_driver.py` with three deltas: (a) F is `[-dsi, +atp_per_spike]` instead of
`[-mi, +atp_per_spike]`; (b) HV utopia / ref point swap the MI axis for the DSI axis; (c) the
per-gen `all_evaluations` dict records `"dsi_best_legit"` instead of `"mi_count_bits"`.

### 68-d parameter scheme + apply_params imports through [t0080]'s library asset

The 54-d electrophys ParameterVector and `apply_parameter_vector(*, cell, params)` write loops were
established in [t0080]'s `apply_params.py` (228 lines) and exposed via
`de_rosenroll_2026_dsgc_ais_dendritic_spike`. [t0123]'s `apply_params.py` (234 lines) is a near-
verbatim copy with the task-internal module path renamed to `tasks.t0123_*` and the DLL loader
`ensure_t91_dll_loaded` adapted to delegate to [t0080]'s idempotent loader (to avoid double-loading
the same SUFFIXes). The full 68-d vector is split into (54-d electrophys, 14-d morphology) by
`generator_wrapper.split_68d_vector` (line 50 of [t0123]'s `generator_wrapper.py`); the morphology
half feeds `morphology_params_from_vector` (line 58) which round-and-cast-int-on the three int
fields (`num_primary_branches`, `max_strahler_depth`, `morph_seed`) and float-cast the other 11.
t0124 copies [t0123]'s `apply_params.py`, `constants_electrophys.py`, `build_cell_ais.py`,
`extend_with_ais.py`, `trial_helpers.py`, `parametric_placer.py`, `generator_wrapper.py`, and
`constants_morphology.py` verbatim with import-path rewrites only.

### Smoke-gate is the load-bearing pre-launch verification step in [t0123]

[t0123]'s `code/smoke_gate.py` (672 lines) implements a 9-check pre-launch verification harness. Six
checks are inherited from [t0115] and three are [t0123]-new. The check that matters for t0124 is
**check 9** (`_check_9_carter_bean_atp_per_ap_at_ais`, lines 420-571): builds the canonical Bed B
anchor cell, runs `_run_one_trial` with `record_ina_for_atp=True` at PD = 0 deg, detects APs on the
somatic Vm trace, integrates inward Na charge per AP per AIS segment via `compute_atp_per_ap`,
divides by the AIS axial length in cm to get ATP/AP/cm, and compares to
`CARTER_BEAN_ATP_PER_AP_PER_CM_REF = 2.41e21` ATP/cm within `CARTER_BEAN_TOLERANCE_FRAC = 0.30`
(30%) OR a fallback `[1e6, 1e14]` physically-plausible range. The [t0123] smoke-gate report
explicitly noted that the 2.41e21 ATP/cm benchmark is a plan-quoted typo (implies ~10^18 ATP per AP
at a ~25 um AIS, physically implausible) and that the fallback band is the practical pass criterion.
t0124's task description (lines 122-133, `### Smoke-gate (inherited from t0123)`) follows up on
S-0123-04 by re-deriving the Carter-Bean canonical value from first principles in the smoke gate;
this means **`smoke_gate.py` is the one [t0123] file t0124 must EDIT** rather than copy verbatim.
The other 8 checks (anchor PD-rate, ratio DSI synthetic sanity, silence guard, pool-restart cadence,
cost-watchdog wiring, no HVPlateau in TerminationCollection, MI/ATP sanity range on anchor, MI/ATP
sign in problem F) need only F-axis-name updates: MI -> DSI on checks 7 and 8. Check 6
(`HV_PLATEAU_AUTO_STOP = False` and `HVPlateauTermination` absent from the live collection) is
unchanged.

### Smoke-gate test harness pattern: 9 numbered `_check_N_*` functions, JSON report, fail-fast

The harness pattern in [t0123]'s `smoke_gate.py` is uniform across all 9 checks: each
`_check_N_*(*, allow_skip_on_import_error: bool = False)` returns a `dict[str, Any]` with keys
`{"id", "name", "status", "passed", "evidence"}`. `run_smoke_gate` (lines 574-652) aggregates all 9
dicts into a single report (key `checks`), computes `fast_checks_passed` over the subset
`{2, 3, 4, 5, 6, 8}` (the Windows-runnable ones), and writes the report to
`logs/steps/009_implementation/smoke_gate.json`. If `fast_checks_passed` is False the harness ALSO
writes a markdown failure summary to `SMOKE_GATE_FAILURE_MD`. The Carter-Bean check 9 (and checks 1
and 7 that need NEURON + the compiled t0080 MOD library) are explicitly deferred to the Vast.ai
remote when running on Windows — the `allow_skip_on_import_error=True` flag propagates this. The
[t0123] unit test [`test_evaluator_dsi_guard.py`](#) (7391 bytes, 7 test functions) is a regression
harness specifically for the DSI silence guard and the 2-direction ratio DSI — this is the
canonical test file t0124 inherits, with import-path rewrites only. It covers
`pd_spikes_sum in {0, 1, 2, 3, 30}` cases plus a direct `_vector_sum_dsi(PD=5, ND=1) = 0.6667`
synthetic check.

### 14-d morphology generator wrapper is a 105-line thin adapter in [t0123]

[t0123]'s `code/generator_wrapper.py` (105 lines) is the single entry point for cell construction in
the 68-d NSGA-II pipeline. It imports `MorphologyParams` and `MorphologyResult` from [t0090]'s
library, `generate_fixed_morphology` and `insert_baseline_channels` from [t0092]'s library, and
exposes four task-local functions: `hash_morphology_vector(*, vector)` for the worker-process cell
cache key, `split_68d_vector(*, vector_68d)` returning `(electrophys_54d, morph_14d)`,
`morphology_params_from_vector(*, morph_vector_14d)` constructing a `MorphologyParams` dataclass
with explicit int rounding on indices 0, 2, 12 (`num_primary_branches`, `max_strahler_depth`,
`morph_seed`), and `build_cell(*, h, morph_params)` calling the patched generator + baseline channel
inserter + the `_LIVE_CELLS` GC-defense list (per [t0093]'s mitigation pattern). t0124 copies this
module verbatim with import-path rewrites only. The 14-d morphology vector lives at indices 54-67 of
the 68-d vector and feeds the procedural generator without modification at the 2-direction protocol
(morphology is direction-independent).

### Cost watchdog and pool restart are inherited unchanged at the $6 cap

[t0123]'s `code/cost_watchdog.py` (129 lines) is a near-verbatim port of [t0115]'s. The
`CostWatchdog` dataclass reads `selected_offer.price_per_hour` from
`logs/steps/008_setup-machines/machine_log.json` at run launch (resolves t0083's $0.83 overrun
caused by hard-coded $0.2382/hr). `trip_if_over_cap` is called every generation by
`CostWatchdogTermination._update` (line 185 of [t0123]'s `nsga2_driver.py`) and writes an
intervention markdown if the elapsed cost exceeds the cap. t0124 inherits the $6 cap by copying
`cost_watchdog.py` verbatim and pinning `COST_CAP_USD = 6.0` in `constants.py`. The plan-mandated
re-verification of Vast.ai balance at launch is operator-side; if balance < $7 the cap is to be
reduced to (balance - $1) per the task description.

### Bed B canonical cell + dendrite geometry from [t0024]

The `de_rosenroll_2026_dsgc` library imports the RGCmodelGD.hoc morphology template and the vendored
`nrnmech.dll`, and `build_dsgc_cell` returns a `DSGCCell` dataclass with `soma`, `all_dends`,
`primary_dends`, `non_terminal_dends`, `terminal_dends`, `terminal_locs_xy`, and `origin_xy`.
[t0123]'s `build_cell_ais.py` (80 lines) wraps this by calling `build_dsgc_cell()`, running
`extend_with_ais(h, soma, total_length_um=AIS_DEFAULT_LENGTH_UM, diameter_um=AIS_DEFAULT_DIAMETER_UM)`
to attach a two-subsegment AIS (proximal + distal), and exposing the result as `DSGCCellWithAIS`.
t0124 uses the [t0092] **procedural** generator (via `generator_wrapper.build_cell`) for the NSGA-II
population, but the canonical Bed B cell construction path through [t0024] / [t0080] is still
required for the smoke gate's `_check_9_carter_bean_atp_per_ap_at_ais` anchor evaluation: this
routes through `_load_t0083_best_cell_electrophys()` +
`anchor_to_14d_vector(anchor=anchors[ANCHOR_NAMES[0]])`, where the "bedb_like" anchor's 14-d
morphology vector reproduces the t0024 geometry as closely as the 14 procedural knobs allow.

## Reusable Code and Assets

Items below are listed by the t0124 code/ filename that will host the carried-over code. All "copy
into task" items are forked from [t0123] verbatim with two transformations: (a) string substitute
`tasks.t0123_bedb_mi_atp_per_spike_nsga2.code` -> `tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code`
across all import statements, and (b) replace the second optimised objective key (`mi_count_bits`)
with the new headline DSI objective (`dsi_best_legit`).

* **`code/atp_per_spike.py`** (~254 lines). Source:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/atp_per_spike.py`. What it does: Sengupta 2010
  ATP-per-spike recipe (AP-window detection, per-segment inward-Na charge integration, ATP molecule
  computation via `Q / e / 3`). Reuse method: **copy into task** (verbatim; the module has no import
  dependency on the rest of the [t0123] code base). Function signatures:
  `detect_ap_windows(*, t_ms, v_soma_mv, threshold_mv=-20.0, refractory_ms=2.0, window_half_ms=2.0) -> list[APWindow]`,
  `compute_atp_per_ap(*, t_ms, ina_by_section, ap_windows) -> list[AtpPerApResult]`,
  `compute_atp_per_spike(*, atp_per_ap_results) -> float`,
  `compute_compartment_breakdown(*, atp_per_ap_results) -> dict[str, float]`. Adaptation needed:
  none.

* **`code/recorder.py`** (~196 lines). Source:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/recorder.py`. What it does: attaches per-segment
  `seg.ina` Vector recorders + somatic Vm + time recorders for the ATP recipe; also keeps the legacy
  per-synapse g/v_local recorders inherited from [t0072] for deep-dive trials. Reuse method: **copy
  into task** (verbatim except import-path string rewrites to the new task namespace). Function
  signatures: `attach_ina_recorders_for_atp(*, h, cell: MorphologyResult) -> InaRecorders`,
  `attach_recorders(*, h, soma, bundle: SynapseBundle) -> BedBRecorders`,
  `save_recorders_npz(*, output_path, recorders, direction_label)`. Adaptation needed: string
  substitute `tasks.t0123_*` -> `tasks.t0124_*` in the three intra-task imports
  (`atp_per_spike.UM2_TO_CM2`, `constants_electrophys`, `trial_helpers.SynapseBundle`).

* **`code/evaluator.py`** (~700 lines, may shorten by ~80 lines once MI is dropped). Source:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/evaluator.py`. What it does: the per-cell evaluation
  harness — builds / caches the worker cell + synapse bundle, runs N_EVAL_SEEDS x N_DIRECTIONS
  trials, summarises spike counts into the DSI silence- guarded vector-sum + ATP/spike + diagnostics
  (pd_rate_hz, firing_hz_per_dir, cytoplasm_volume_um3, mi_count_bits the latter retained as a
  diagnostic per t0124's task description line 89). Reuse method: **copy into task** with the
  following modifications: (a) `CellEvalResult` reorder — promote `dsi_vector_sum` to a HEADLINE
  field, demote `mi_count_bits` to a DIAGNOSTIC field; (b) `BedBV3MorphProblem._evaluate` (the pymoo
  Problem hook): rewrite `out["F"] = [-result.mi_count_bits, +result.atp_per_spike_molecules]` to
  `out["F"] = [-result.dsi_vector_sum, +result.atp_per_spike_molecules]`; (c) `evaluate_68d_vector`
  default arg `n_directions: int = 2` (was 4); (d) `_summarise_trials` continues to gate
  ATP-per-spike on silence; the new "best_legit" DSI variant filters cells with
  `silence_failed = True`; (e) all `tasks.t0123_*` imports rewritten. Function signatures
  (post-edit):
  `evaluate_68d_vector(*, vector_68d, eval_seeds=None, n_directions=2) -> CellEvalResult`,
  `_vector_sum_dsi(*, spike_counts_per_dir) -> float`,
  `_summarise_trials(*, results, n_seeds, n_directions) -> CellEvalResult`.

* **`code/smoke_gate.py`** (~672 lines, plus ~30-50 lines of new code for the first-principles
  Carter-Bean derivation). Source: `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/smoke_gate.py`.
  What it does: 9-check pre-launch verification harness, writes
  `logs/steps/009_implementation/smoke_gate.json`. Reuse method: **copy into task with
  modifications** (NOT verbatim — this is the one [t0123] file t0124 must edit per task
  description lines 122-133, S-0123-04 follow-up): (a) check 3 retains
  `SILENCE_PD_SPIKES_THRESHOLD == 3` unchanged; (b) check 5 retains `T0123_HARD_BUDGET_USD == 6.00`
  unchanged, but the constant name updates to `T0124_HARD_BUDGET_USD`; (c) check 6 retains the
  `HV_PLATEAU_AUTO_STOP = False` assertion unchanged; (d) check 7 (sanity range on MI/ATP) becomes
  sanity range on DSI/ATP — `DSI in [0, 1]` instead of `MI in [0, 2]`, ATP range unchanged at
  `[1e7, 1e11]`; (e) check 8 (`BedBV3MorphProblem._evaluate` emits F[0]=-MI, F[1]=+ATP) becomes
  F[0]=-DSI, F[1]=+ATP; (f) check 9 (Carter-Bean) gets a NEW first-principles derivation block
  prepended that documents the canonical 2.41e21 ATP/cm value (or replaces it if S-0123-04's verdict
  is that the value is wrong); the fallback `[1e6, 1e14]` plausible band is retained. Function
  signatures: `run_smoke_gate(*, output_path, run_check_1=True) -> dict[str, object]`, plus 9
  `_check_N_*(*, allow_skip_on_import_error=True) -> dict[str, Any]` helpers.

* **`code/test_evaluator_dsi_guard.py`** (~186 lines). Source:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/test_evaluator_dsi_guard.py`. What it does:
  regression tests for the silence guard and the 2-direction ratio DSI. Seven pytest functions
  covering `pd_spikes_sum in {0, 1, 2, 3, 30}`, the threshold constant value, and the
  `_vector_sum_dsi` synthetic check at PD=5, ND=1 (= 0.6667). Reuse method: **copy into task**
  (verbatim with import-path rewrites only — this is the test harness for the Carter-Bean
  smoke-gate item 4 in the task description). Function signatures: 7 `test_*()` functions.
  Adaptation needed: string substitute `tasks.t0123_*` -> `tasks.t0124_*`.

* **`code/nsga2_driver.py`** (~775 lines). Source:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/nsga2_driver.py`. What it does: the NSGA-II
  minimize() loop with per-gen pool restart, dill checkpoint, JSONL trace, HV trajectory,
  cost-watchdog termination, and operator-stop termination. Encodes `_POOL_RESTART_EVERY = 10` and
  excludes `HVPlateauTermination` from the live `TerminationCollection`. Reuse method: **copy into
  task** with these edits: (a) F-axis label updates:
  `state.all_evaluations.append({"mi_count_bits": float(-f_row[0]), ...})` becomes
  `{"dsi_best_legit": float(-f_row[0]), ...}`; (b) `hv_utopia` value: drop `HV_UTOPIA_MI_BITS` (=
  1.5 bits) and use `HV_UTOPIA_DSI` (= 0.7) which already exists at `constants_morphology.py` line
  146; (c) `ref_point` for HV: `(0.0, WORST_CASE_ATP_PER_SPIKE)` is retained (DSI worst-case = 0
  after negation, matching MI's worst-case = 0); (d) `T0123_*` -> `T0124_*` symbol renames; (e) all
  imports updated. Function signatures: `run_nsga2_for_seed(*, seed, step_id, ...) -> None`,
  `PerGenerationPoolRestart(Callback)`, `CostWatchdogTermination(Termination)`,
  `OperatorStopTermination(Termination)`.

* **`code/generator_wrapper.py`** (~105 lines). Source:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/generator_wrapper.py`. What it does: thin adapter
  around the [t0092] `generate_fixed_morphology` patched morphology generator. Exposes
  `split_68d_vector`, `morphology_params_from_vector`, `build_cell`, and the `_LIVE_CELLS`
  GC-defense list. Imports `MorphologyParams` / `MorphologyResult` from [t0090]'s library and
  `generate_fixed_morphology` / `insert_baseline_channels` from [t0092]'s library. Reuse method:
  **copy into task** (verbatim except `tasks.t0123_*` -> `tasks.t0124_*` import rewrites). Function
  signatures: `split_68d_vector(*, vector_68d) -> tuple[NDArray, NDArray]`,
  `morphology_params_from_vector(*, morph_vector_14d) -> MorphologyParams`,
  `hash_morphology_vector(*, vector) -> int`, `build_cell(*, h, morph_params) -> MorphologyResult`.

* **`code/apply_params.py`** (~234 lines), **`code/constants_electrophys.py`** (~547 lines),
  **`code/build_cell_ais.py`** (~80 lines), **`code/extend_with_ais.py`** (~150 lines),
  **`code/trial_helpers.py`** (~311 lines), **`code/parametric_placer.py`** (~105 lines),
  **`code/constants_morphology.py`** (~168 lines), **`code/biological_priors.py`** (~252 lines),
  **`code/anchor_definitions.py`** (~149 lines), **`code/anchor_classifier.py`** (~127 lines),
  **`code/biological_scorecard.py`** (~250 lines), **`code/random_init.py`** (~101 lines),
  **`code/cost_watchdog.py`** (~129 lines), **`code/hv_plateau_watchdog.py`** (~89 lines),
  **`code/cytoplasm_volume.py`** (~101 lines), **`code/bootstrap.py`** (~250 lines),
  **`code/paths.py`** (~250 lines), **`code/cuntz_balancing_factor.py`** (~200 lines). Source:
  corresponding files in `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/`. What they do: the
  carry-over infrastructure modules (electrophys constants, AIS extension, parametric synapse
  placer, AR(2) noise trial driver, hyper-parameter / hypervolume utopia constants, biological-prior
  scorecards, anchor cell definitions for the smoke gate, Phase-A Latin-Hypercube random initial
  population, cost watchdog reading machine_log.json, HV plateau detector kept as importable but NOT
  registered in TerminationCollection, cytoplasm-volume helper free since [t0122] tracked as
  diagnostic, Linux/Windows NEURON bootstrap, path constants). Reuse method: all **copy into task**
  (verbatim with `tasks.t0123_*` -> `tasks.t0124_*` import rewrites; some files like
  `cuntz_balancing_factor.py` and `cytoplasm_volume.py` are not in the inherited 49 [t0123] code/
  files but in [t0122]; the [t0123] code/ directory was forked from [t0122] which forked from
  [t0115]).

* **`code/mi_estimator.py`** (~235 lines). Source:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/mi_estimator.py`. What it does: discrete count-MI
  estimator with Miller-Madow bias correction; returns `mi_count_bits`. Reuse method: **copy into
  task** (verbatim with import-path rewrites only — even though MI is no longer optimised, it is a
  TRACKED DIAGNOSTIC per task description line 89; per cell evaluation runs the estimator for free
  and the result is written into the predictions asset).

* **`code/post_hoc_strong_bialek.py`** (~250 lines). Source:
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/post_hoc_strong_bialek.py`. What it does:
  Strong-Bialek direct-method MI bits/s estimator run on top-10 Pareto cells post-hoc. Reuse method:
  **do NOT copy** — this is [t0123]-specific MI-verification scaffolding. t0124 does not optimise
  MI and the headline scientific output is the DSI-vs-ATP Pareto front comparison with Carter-Bean
  and Attwell-Laughlin, not Niven 2007.

* **`code/build_predictions_assets.py`** (~600 lines), **`code/build_results.py`** (~200 lines),
  **`code/build_pareto_plots.py`** (~400 lines), **`code/build_top50_morphologies.py`** (~310
  lines), **`code/build_assets.py`** (~600 lines), **`code/metrics_builder.py`** (~250 lines).
  Source: `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/`. What they do: post-run assembly of the
  predictions asset (one record per cell with the 68-d vector, ATP/spike, DSI, etc.),
  `results_summary.md` / `results_detailed.md` skeletons, the Pareto front chart, the top-50
  morphology grid (per the project default of FULL DENDRITE TREES — memory
  `feedback_top50_morphologies_full_dendrites.md`), the answer asset, and the metrics.json schema.
  Reuse method: **copy into task with modifications** — these builders are tightly coupled to the
  (MI, ATP) F-axis convention. t0124 must rewrite the F-axis labels (MI -> DSI), re-order the
  predictions asset record fields (DSI before ATP, ATP-per-AP after, MI demoted to diagnostic), and
  update the chart titles / axis labels (`Pareto Front: DSI vs ATP-per-Spike`,
  `DSI (silence-guarded)` on y, `ATP per Spike (molecules)` on x).

* **NEW for t0124: `code/dsi_atp_comparators.py`** (~200-300 new lines, no source). What it does:
  Carter-Bean 2009 ATP-per-AP-per-cm comparison on top-3 Pareto cells; the Attwell-Laughlin 2001
  implied per-cell signalling ATP rate (ATP/spike * PD-rate) overlay vs the 47%-of-cortical-budget
  anchor; the Cuntz 2010 balancing-factor cross-reference to [t0122]'s cytoplasm-volume front. Reuse
  method: **new code** — the Carter-Bean and Attwell-Laughlin comparators do not exist in [t0123];
  they are part of the t0124 headline analysis (task description lines 159-167). Bootstrap CIs use
  the same `bootstrap.py` helper [t0123] inherited from [t0115].

## Lessons Learned

* **The Sengupta recipe surface-area unit conversion (`UM2_TO_CM2 = 1e-8`) is the single
  highest-risk failure mode.** [t0123]'s `atp_per_spike.py` docstring lines 11-13 calls out the
  [t0097] catalogue's warning that misreading this as 1e-2 is the most common bug. The Carter-Bean
  smoke-gate check 9 catches it. t0124 must NOT touch this constant.

* **The 2.41e21 ATP/cm Carter-Bean benchmark in [t0123]'s plan is a typo.** [t0123]'s smoke-gate
  report explicitly noted that 2.41e21 ATP/cm implies ~10^18 ATP per AP at a ~25 um AIS, which is
  physically implausible; the actual textbook RGC AIS energy budget is ~1e6 ATP per AP per AIS
  segment, i.e. ~4e8 ATP/cm. The fallback `[1e6, 1e14]` plausible band is the practical pass
  criterion. t0124 resolves S-0123-04 by re-deriving the canonical value from first principles in
  `smoke_gate.py` and replacing the plan-quoted number.

* **[t0122]'s cytoplasm-volume + DSI Pareto run finished at $0.50 of $6 cap on 2 directions, 60
  gens.** Half the per-trial budget vs [t0123]'s 4-direction run. t0124's 2-direction + DSI + ATP
  run extrapolates to ~$1-2 — comfortably inside the $6 cap.

* **[t0123]'s MI-vs-ATP run hit a silence-corner artefact: count-MI = 1.459 bits at the
  silence-guard boundary (~3 PD spikes/trial) where spike-time information is degenerate.**
  Strong-Bialek bits/s = 0.0 across all 10 top-MI cells. t0124 does NOT optimise MI, so this
  artefact does not recur, but the silence-guard threshold (`SILENCE_PD_SPIKES_THRESHOLD = 3`) is
  precisely the lever that pushes [t0123]'s optimiser into the corner — t0124 MUST retain the same
  threshold so its DSI-vs-ATP Pareto front is comparable.

* **The 10-gen pool restart cadence (memory `feedback_nsga2_pool_restart_every_10.md`) is
  load-bearing for memory mitigation on 60+ gen runs.** [t0123] fired pool restart at gens 10, 20,
  30, 40, 50 with no degradation. t0124 must NOT change this.

* **HV-plateau auto-stop is DISABLED by project policy (memory
  `feedback_disable_hv_plateau_autostop.md`).** Termination is by max-gen ceiling + cost cap +
  operator stop only. t0124 keeps the policy.

* **The top-50 morphology grid must render FULL DENDRITE TREES, not just somas (memory
  `feedback_top50_morphologies_full_dendrites.md`).** [t0114] got this wrong; [t0122] / [t0123] got
  it right. t0124 inherits the corrected `build_top50_morphologies.py`.

* **Aggregator-based task / cost / metric enumeration must be used; never walk `tasks/` with Glob.**
  This applies to t0124's post-run reporting. Library and answer asset enumeration is the only
  manual case because `aggregate_libraries` and `aggregate_answers` are not implemented in this
  project.

* **The smoke-gate's 9-check structure is robust; the failure-mode pattern is to defer
  NEURON-dependent checks (1, 7, 9) to the remote when running on Windows.** t0124 inherits the same
  Windows-deferral pattern.

* **The `_LIVE_CELLS` GC-defense list ([t0093] mitigation pattern) prevents cell-id reuse after
  garbage collection.** [t0123]'s `generator_wrapper.py` line 38 and `evaluator.py` line 170 both
  append to it. t0124 must retain this — the bug surfaced as silent stale-cell reuse on [t0091]
  before [t0093] introduced the mitigation.

## Recommendations for This Task

* **Fork [t0123]'s code/ directory verbatim** as the t0124 starting point. Run a global string
  substitution `tasks.t0123_bedb_mi_atp_per_spike_nsga2.code` ->
  `tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code` across every `.py` file, then `T0123_` -> `T0124_`
  for the budget / seed symbol renames.

* **Drop `post_hoc_strong_bialek.py`.** It is MI-specific and adds no value to a DSI-vs-ATP
  optimisation.

* **Edit `smoke_gate.py` to update checks 7 and 8** (replace MI sanity / sign checks with DSI sanity
  / sign checks) and prepend a first-principles Carter-Bean derivation block to check 9 (S-0123-04
  follow-up).

* **Edit `evaluator.py`** as listed under Reusable Code: promote `dsi_vector_sum` to a headline
  objective in `CellEvalResult` and in `BedBV3MorphProblem._evaluate`, demote `mi_count_bits` to
  diagnostic, change `evaluate_68d_vector` default `n_directions` from 4 to 2.

* **Edit `nsga2_driver.py`** to update the per-gen `all_evaluations` schema (`mi_count_bits` ->
  `dsi_best_legit`), `hv_utopia` (drop MI utopia 1.5 bits; use existing `HV_UTOPIA_DSI = 0.7`), and
  the F-axis labels in print statements.

* **Edit `constants.py`** to rename `T0123_*` symbols to `T0124_*`, keep all asserted invariants
  (`_POOL_RESTART_EVERY == 10`, `HV_PLATEAU_AUTO_STOP is False`, `POP_SIZE == 96`,
  `N_EVAL_SEEDS == 3`, `COST_CAP_USD == 6.0`, `N_GEN_MAX == 60`), and override `N_DIRECTIONS == 2`
  (not 4) per t0124's task description.

* **Edit `constants_morphology.py`** to set `N_DIRECTIONS: int = 2` (was 4 in [t0123]), retain
  `N_EVAL_SEEDS = 3`, retain `POP_SIZE = 96`, retain `N_GEN = 60`.

* **Adopt a NEW GA seed** via `secrets.randbelow(10000)` per the [t0113] / [t0115] / [t0122] /
  [t0123] convention; avoid round numbers and the lineage seeds 77 / 441 / 2247 / 7755 / 9354 /
  1524\. Pin it in `constants.py` `T0124_SEEDS: tuple[int, ...] = (<seed>,)`.

* **Use the [t0090] / [t0092] morphology generator libraries via library import.** Do not copy
  `generator.py` or `morphology_generator_fix.py` into the t0124 code/ — they remain cross-task
  imports per their `details.json` `library_id`.

* **Use [t0080]'s compiled MOD library** (the shared `nrnmech` namespace) for cell construction. The
  Vast.ai remote MUST run `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`
  at provisioning time.

* **Use [t0024]'s `build_dsgc_cell` library** for the smoke-gate's canonical Bed B anchor cell
  (route through `_load_t0083_best_cell_electrophys()` + the "bedb_like" anchor's 14-d vector).

* **Add a new module `code/dsi_atp_comparators.py`** for the Carter-Bean 2009 and Attwell-Laughlin
  2001 quantitative overlays on the top-N Pareto cells. Bootstrap CIs reuse `bootstrap.py` from
  [t0123]. Re-use the existing top-50 morphology renderer (`build_top50_morphologies.py`) verbatim
  and ensure FULL DENDRITE TREES (project default).

* **Run the [t0123] smoke-gate test harness (`test_evaluator_dsi_guard.py`) as the t0124 pre-launch
  regression suite.** All 7 tests should pass unchanged after the import-path rewrite because they
  test the silence guard + 2-direction ratio DSI in isolation from MI / ATP.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Provides the canonical Bed B DSGC NEURON cell + dendrite geometry + nrnmech.dll
  vendoring via the `de_rosenroll_2026_dsgc` library, which is the foundation of every subsequent
  68-d run. The smoke-gate's Carter-Bean anchor check ultimately routes through [t0024]'s
  `build_dsgc_cell`.

### [t0072]

* **Task ID**: `t0072_synaptic_traces_pd_nd`
* **Name**: Per-synapse PD/ND trace recorder
* **Status**: completed
* **Relevance**: Source of the per-synapse g/v_local recorder helpers (`BedBRecorders`,
  `attach_recorders`) that [t0123] and the current task inherit alongside the new
  `attach_ina_recorders_for_atp`.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B MOBO v3 (dendritic spike + 54-d electrophys)
* **Status**: completed
* **Relevance**: Established the 54-d `ParameterVector`, tiered `apply_parameter_vector` write
  loops, AIS extension, dendritic-spike biological priors, and the compiled MOD pack that serves as
  the shared `nrnmech` namespace for every subsequent 68-d run. Exposed via the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural 14-d morphology generator diversity test
* **Status**: completed
* **Relevance**: Provides the `MorphologyParams` (14 typed fields), `MorphologyResult`, and
  `StabilityKind` API via the `procedural_dsgc_morphology_generator` library. The task's
  `generator_wrapper.py` imports `MorphologyParams` directly from here.

### [t0091]

* **Task ID**: `t0091_morphology_extended_nsga2_v1`
* **Name**: Morphology-extended NSGA-II v1 (first 68-d run)
* **Status**: completed
* **Relevance**: First task to combine the 54-d electrophys vector with the 14-d morphology vector
  into the 68-d NSGA-II problem. The cell-id reuse bug surfaced here is what [t0093]'s `_LIVE_CELLS`
  GC-defense list later mitigated. The 5-anchor warm-start in [t0091] was replaced by
  Latin-Hypercube sampling in [t0102] onwards.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: Seedscale n=4, gen 20 (Latin-Hypercube random-init)
* **Status**: completed
* **Relevance**: First task to replace [t0091]'s 5-anchor warm-start with a Latin-Hypercube
  random-init NSGA-II population. The Phase-A LHS pattern in `random_init.py` is carried through
  [t0115] / [t0122] / [t0123] and into the current task.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology generator silence; canonical patched generator
* **Status**: completed
* **Relevance**: Provides the CANONICAL `generate_fixed_morphology` patched generator (C-0093-01)
  via the `procedural_dsgc_morphology_generator_fix` library — the unpatched [t0090] generator
  MUST NOT be called directly. The task imports from here.

### [t0093]

* **Task ID**: `t0093_resweep_and_t0090_correction`
* **Name**: Resweep + t0090 morphology correction
* **Status**: completed
* **Relevance**: Source of the `_LIVE_CELLS` GC-defense mitigation pattern (REQ-18 in [t0091]) that
  prevents NEURON cell-id reuse after Python garbage collection — load-bearing for every 68-d run
  that uses procedural morphologies. Inherited by [t0123]'s `generator_wrapper.py` and carried into
  the current task.

### [t0097]

* **Task ID**: `t0097_multi_obj_optim`
* **Name**: Multi-objective optimisation objective-function catalogue
* **Status**: completed
* **Relevance**: Source of the `metabolic_energy_atp_per_spike` recipe (Sengupta 2010) and the
  Carter-Bean / Attwell-Laughlin / Niven 2007 anchor references. Source suggestion S-0097-02 ("Bed B
  NSGA-II maximising DSI and minimising ATP-per-spike") is the origin of the current task.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: 300-generation PD-vs-ND NSGA-II
* **Status**: completed
* **Relevance**: Established the 300-gen NSGA-II driver substrate (per-gen pool restart, dill
  checkpoint, JSONL trace). Carried through [t0113] / [t0114] / [t0115] / [t0122] / [t0123] and now
  the current task.

### [t0113]

* **Task ID**: `t0113_t0106_seed2247_replicate`
* **Name**: NSGA-II seed 2247 replicate of [t0106]
* **Status**: completed
* **Relevance**: Established the `secrets.randbelow(10000)` GA-seed-drawing convention that avoids
  round-ish numbers. The current task draws its single GA seed the same way and avoids the lineage
  seeds 77 / 441 / 2247 / 7755 / 9354 / 1524.

### [t0114]

* **Task ID**: `t0114_seed7755_no_autostop`
* **Name**: NSGA-II seed 7755 with HV-plateau auto-stop disabled
* **Status**: completed
* **Relevance**: First task to bake the `HV_PLATEAU_AUTO_STOP = False` policy and the associated
  `TerminationCollection` content into the driver. Source of the rule that `HVPlateauTermination`
  stays importable for smoke-gate REQ-8 but is NOT in the live collection. Also surfaced the [t0114]
  mistake of rendering top-N morphology grids as just somas (the project default is now FULL
  DENDRITE TREES, per `feedback_top50_morphologies_full_dendrites.md`).

### [t0115]

* **Task ID**: `t0115_seed9354_no_autostop`
* **Name**: NSGA-II seed 9354 with HV-plateau auto-stop disabled
* **Status**: completed
* **Relevance**: Encodes `HV_PLATEAU_AUTO_STOP = False` and the per-gen pool-restart cadence in its
  763-line `nsga2_driver.py`; canonical fork point for the auto-stop-disabled convention. [t0122] /
  [t0123] / current task all inherit it verbatim with three-symbol deltas.

### [t0120]

* **Task ID**: `t0120_morph_generator_geometry_audit`
* **Name**: Morphology generator geometry audit
* **Status**: completed
* **Relevance**: Verdict "rendering-only / no re-runs needed" remains in force. The [t0090] /
  [t0092] morphology generator substrate is approved as-is.

### [t0122]

* **Task ID**: `t0122_dsi_cytoplasm_volume_nsga2`
* **Name**: NSGA-II maximising DSI and minimising cytoplasm volume
* **Status**: completed
* **Relevance**: Source of the DSI silence-guarded ratio implementation (`_summarise_trials` +
  `_vector_sum_dsi` + `SILENCE_PD_SPIKES_THRESHOLD = 3`), the tightened `pd_spikes_sum < 3` guard,
  and the `N_DIRECTIONS = 2` antipodal-pair protocol that the current task adopts. Sibling task on
  the function objective (DSI); the current task's cost objective is per-spike ATP rather than
  [t0122]'s cytoplasm volume.

### [t0123]

* **Task ID**: `t0123_bedb_mi_atp_per_spike_nsga2`
* **Name**: NSGA-II maximising MI and minimising ATP-per-spike
* **Status**: completed
* **Relevance**: Direct fork point. Source of `atp_per_spike.py` (Sengupta recipe verbatim),
  `recorder.py` `attach_ina_recorders_for_atp`, the smoke-gate check 9 Carter-Bean comparator,
  `test_evaluator_dsi_guard.py`, and the modified `evaluator.py` / `nsga2_driver.py` that carry both
  ATP-per-spike and the silence-guarded DSI together. The current task swaps the MI objective for
  the headline DSI silence-guarded ratio and halves the direction count.
