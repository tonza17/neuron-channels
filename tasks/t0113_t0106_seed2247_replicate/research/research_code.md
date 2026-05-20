---
spec_version: "1"
task_id: "t0113_t0106_seed2247_replicate"
research_stage: "code"
tasks_reviewed: 12
tasks_cited: 11
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-05-20"
status: "complete"
---
# Research Code — Seed-2247 Random-Seed Replicate of t0106

## Task Objective

t0113 is a deliberately minimum-change replicate of the t0106 long 2-direction NSGA-II run on the
68-d Bed B electrophys + 14-d morphology substrate, forked directly from [t0112]. Where [t0112]
picked GA seed 77 from a small curated candidate set, t0113 uses GA seed 2247 drawn at random via
`secrets.randbelow(10000)` to avoid any "round-ish low number" selection bias and to widen the seed
support beyond the 44-99 range. The same evaluator, the same NSGA-II hyperparameters, the same
silence guard, the same pool-restart cadence (every 10 generations), the same 60-gen ceiling, the
same HV-plateau auto-stop, and the same predictions asset schema are reused verbatim. Only two
constants change relative to [t0112]: `T0112_SEEDS = (77,)` becomes `T0113_SEEDS = (2247,)` and the
matching `T0112_HARD_BUDGET_USD = 25.00` is renamed to `T0113_HARD_BUDGET_USD = 25.00` (value
unchanged). The package import path `tasks.t0112_t0106_seed77_replicate` is globally rewritten to
`tasks.t0113_t0106_seed2247_replicate`. This research stage identifies the exact files to fork from
[t0112], the exact patch sites, the cross-task imports that must remain untouched, and confirms the
predictions asset schema this task must mirror.

## Library Landscape

The project does **not** ship a library aggregator (`arf/scripts/aggregators/aggregate_libraries.py`
does not exist; running it returns `No module named arf.scripts.aggregators.aggregate_libraries`).
The complete aggregator list in `arf/scripts/aggregators/` is: `aggregate_categories.py`,
`aggregate_costs.py`, `aggregate_machines.py`, `aggregate_metric_results.py`,
`aggregate_metrics.py`, `aggregate_suggestions.py`, `aggregate_task_types.py`, `aggregate_tasks.py`.
No answer aggregator exists either. Library and answer enumeration in this project is therefore by
direct filesystem walk of `tasks/*/assets/library/` and `tasks/*/assets/answer/`.

Per [t0112]'s `research_code.md` lines 27-56, the project contains **18 registered library asset
directories** (one empty under [t0010]). None of those libraries is imported via its registered
entry point by the t0078 -> t0106 -> t0112 NSGA-II lineage. The relevant cross-task code paths are
all standard task-imports (`tasks.tXXXX_*.code.<module>`), which the verificator allows but which
are **not** library imports under the project's Cross-Task Code Reuse Rule. The libraries touching
the NSGA-II lineage (`de_rosenroll_2026_dsgc` from [t0024],
`procedural_dsgc_morphology_generator_fix` from [t0092], the [t0080] compiled MOD bundle) are
reached via raw module paths, not entry-point imports.

**Net effect for t0113**: zero library imports via registered entry points, identical to [t0112].
Every shared module between t0113 and the t0024/t0080/t0090/t0092/t0106/t0112 ancestors is reached
via the full-path import pattern. `libraries_found: 0` in the frontmatter reflects that no library
aggregator exists; the 18 raw library directories were considered via [t0112]'s prior enumeration
and none is applicable.

## Key Findings

### The Patch Surface Is Exactly One Constant Rename Plus the Package-Path Rewrite

The entire delta between [t0112] and t0113 lives in three lines of one file plus a global
search-and-replace across every `.py` and `.sh` file. Specifically:

* `tasks/t0112_t0106_seed77_replicate/code/constants.py:59` — `T0112_SEEDS: tuple[int, ...] = (77,)`
  becomes `T0113_SEEDS: tuple[int, ...] = (2247,)`. The value 2247 was drawn locally by
  `secrets.randbelow(10000)` immediately before task creation, per `task_description.md` lines
  21-22.
* `tasks/t0112_t0106_seed77_replicate/code/constants.py:60` — `T0112_HARD_BUDGET_USD: float = 25.00`
  is renamed to `T0113_HARD_BUDGET_USD: float = 25.00`. Value unchanged.
* `tasks/t0112_t0106_seed77_replicate/code/constants.py:61` —
  `T0112_PER_INSTANCE_WATCHDOG_USD: float = 20.00` is renamed to
  `T0113_PER_INSTANCE_WATCHDOG_USD: float = 20.00`. Value unchanged.
* Backwards-compatibility aliases at the bottom of `constants.py` (lines 65-71: `T0104_SEEDS`,
  `T0104_HARD_BUDGET_PER_SEED_USD`, `T0104_TASK_BUDGET_TOTAL_USD`, `T0106_SEEDS`,
  `T0106_HARD_BUDGET_USD`, `T0106_PER_INSTANCE_WATCHDOG_USD`) must be updated to point at the new
  `T0113_*` constants. The `__all__` export list (lines 77-114) likewise gets the three `T0112_*` ->
  `T0113_*` renames.
* Every `.py` and `.sh` file inherits a global package-path rewrite from
  `tasks.t0112_t0106_seed77_replicate` to `tasks.t0113_t0106_seed2247_replicate`. The orchestration
  script `run_seed77.sh` becomes `run_seed2247.sh` (or equivalent) with seed `77` replaced by
  `2247`. The driver docstring and the `_save_algorithm_config` writer pick up the rename
  automatically because they all read the module-level constant by name.

There are **no other algorithm changes**. `nsga2_driver.py` keeps `_POOL_RESTART_EVERY = 10` from
[t0112] verbatim. `constants_morphology.py` keeps `N_GEN = 60` from [t0112] verbatim. The evaluator,
the silence guard, the SBX/PM operators, the LHS init sampler, the cost watchdog, the dill
checkpoint cadence, the operator-stop polling, the HV-plateau termination, and the predictions asset
writer all remain bitwise identical to [t0112] (and therefore to [t0106]).

### The Cross-Task Import Rule Forces a Verbatim Copy of t0112's Code

Per `arf/specifications/research_code_specification.md` and the project rule Cross-Task Code Reuse
Rule, t0113 **MUST NOT** import from `tasks.t0112_t0106_seed77_replicate.code`. Every non-library
[t0112] module must be copied into `tasks/t0113_t0106_seed2247_replicate/code/`. The same rule
already governed [t0112]'s relationship to [t0106] and [t0106]'s relationship to [t0104]; the
established pattern is verbatim copy with a global package-path rewrite plus a one-constant patch.

The verificator does not flag full-path imports of UPSTREAM tasks (e.g.,
`tasks.t0024_*.code.constants`, `tasks.t0090_*.code.morphology_params`,
`tasks.t0092_*.code.morphology_generator_fix`, `tasks.t0080_*.code.mods`); only same-tier or
downstream task imports are forbidden. So the upstream import edges from [t0112] to [t0024],
[t0080], [t0090], [t0092] stay valid in t0113 with the same import strings — only
`t0112_t0106_seed77_replicate` becomes `t0113_t0106_seed2247_replicate` everywhere it appears as a
self-reference.

### The t0112 Code Tree Has 35 Python Modules Totalling 8,427 Lines

A full `wc -l` over `tasks/t0112_t0106_seed77_replicate/code/*.py` returns 8,427 lines across 35
files (including the empty `__init__.py`). The +310-line delta vs [t0106]'s 8,117 lines comes from
the [t0112]-specific result builder `build_t0112_results.py` (303 lines) and a small change in
`run_*.sh`. The algorithm-critical modules that must be copied verbatim from [t0112] into t0113 are:

* `nsga2_driver.py` (734 lines) — pool-restart cadence stays at 10. Only the package-path rewrite
  applies.
* `constants.py` (114 lines) — receives the seed/budget rename described above.
* `constants_morphology.py` (159 lines) — `N_GEN = 60` stays at 60. Only the package-path rewrite
  applies inside the import block at lines 49-60.
* `constants_electrophys.py` (547 lines) — verbatim.
* `evaluator.py` (504 lines) — verbatim (ratio DSI already correct at `N_DIRECTIONS=2`, silence
  guard active).
* `random_init.py` (101 lines) — verbatim except for the `T0112_SEEDS` -> `T0113_SEEDS` import name
  at line 21 and the `T0112_SEEDS` iteration in `main()` at line 96.
* `paths.py` (218 lines) — verbatim except for the package-path rewrite. Note that the file is named
  with the t0102 module docstring at line 1 ("Centralised path constants for the t0102 random-init
  NSGA-II reproducibility task") — this docstring drift is inherited unchanged.
* `cost_watchdog.py` (129 lines) — verbatim (`make_watchdog_from_machine_log` factory).
* `hv_plateau_watchdog.py` (89 lines) — verbatim.
* `bootstrap.py` (161 lines) — verbatim (NEURON DLL loader).
* `apply_params.py` (234 lines), `build_cell_ais.py` (79 lines), `extend_with_ais.py` (127 lines),
  `parametric_placer.py` (105 lines), `recorder.py` (122 lines), `trial_helpers.py` (311 lines) —
  evaluator support; verbatim.
* `generator_wrapper.py` (105 lines) — verbatim adapter around [t0092]'s patched morphology
  generator.
* `anchor_definitions.py` (149 lines), `anchor_classifier.py` (127 lines), `biological_priors.py`
  (252 lines), `biological_scorecard.py` (183 lines) — needed by `smoke_gate.py`. Verbatim.
* `smoke_gate.py` (192 lines) — verbatim; runs the 5 local pre-launch checks (single-eval driver,
  ratio DSI synthetic sanity, silence-guard pytest, pool-restart sanity, watchdog wiring).
* `test_evaluator_dsi_guard.py` (164 lines) — silence-guard pytest; copy verbatim.

The `run_seed77.sh` orchestration script (49 lines, see
`tasks/t0112_t0106_seed77_replicate/code/run_seed77.sh`) is renamed to `run_seed2247.sh` with `SEED`
set to `2247` and the `tasks.t0112_*` module paths swapped for `tasks.t0113_*`.

**Total verbatim copy size**: ~5,800 lines of algorithm-critical code, identical to the [t0106] ->
[t0112] fork volume. The remaining ~2,600 lines (analysis / charting / asset-build modules:
`build_analysis_charts.py`, `build_assets.py`, `build_morphology_charts.py`,
`build_predictions_assets.py`, `build_t0106_plots.py`, `build_t0112_results.py`, `make_charts.py`,
`metrics_builder.py`, `cross_seed_analysis.py`, `per_seed_analysis.py`, `run_local_analysis.py`) can
be ported on demand in the analysis stage; they are not needed for the experiment-run step. The
[t0112]-specific `build_t0112_results.py` (303 lines) will need adapter changes to read three seed
sources (44, 77, 2247) instead of two; that work is analysis-stage scope.

### The Predictions Asset Schema Is Locked at spec_version "2" and Must Be Mirrored Exactly

[t0112]'s predictions asset
(`tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/details.json`)
specifies `spec_version: "2"` and uses the same structure [t0106] established for the canonical
evaluations file:

* Top-level JSON object with one key `evaluations` mapping to a list of per-cell records.
* Each record has fields: `generation` (int, 1 = LHS init, 2+ = offspring), `vector_68d` (list of 68
  floats = 54-d electrophys + 14-d morphology), `objective_F_minimised` (list of 2 floats =
  sign-flipped `[-ratio_dsi, -pd_rate_hz]`), `dsi_vector_sum` (float in [0, 1], guard-cleaned ratio
  DSI), `pd_rate_hz` (float, mean PD firing rate in Hz across the 3 noise replicates).
* File format is gzipped JSON (`.json.gz`), explicitly to satisfy the project's 5 MB pre-commit
  limit.
* Required `metrics_at_creation` keys (per [t0112] `details.json` lines 13-22 and the t0113 task
  brief): `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`.
* Required top-level keys: `predictions_id`, `name`, `short_description`, `description_path`,
  `model_id` (nullable; [t0106] and [t0112] both used `null`), `model_description`, `dataset_ids`
  (`[]`), `prediction_format`, `prediction_schema`, `instance_count`, `files`, `categories`,
  `created_by_task`, `date_created`.

The categories used by [t0106] and [t0112] are `direction-selectivity`, `compartmental-modeling`,
`retinal-ganglion-cell`; t0113 should inherit these unchanged. The predictions asset folder must be
named `t0113-bedb-morph-nsga2-seed2247` (per `task_description.md` lines 87-88) and `predictions_id`
inside `details.json` must match.

### The `dsi_vector_sum` Field Name Lie Is Preserved for Schema Compatibility

[t0106]'s and [t0112]'s evaluators both return a 2-direction ratio DSI but write it into the
`dsi_vector_sum` JSON field for back-compat with [t0102] / [t0104] downstream tooling
(`build_predictions_assets.py`, `build_analysis_charts.py`). t0113 must preserve this same field
name; renaming it to `dsi_ratio` would break the analysis scripts in `cross_seed_analysis.py` and
`build_t0112_results.py` that walk both [t0106] and [t0112] predictions assets and will walk t0113
too. The field name lie is documented in [t0112]'s `prediction_schema` string in `details.json`
("field name preserved for compatibility with t0102/t0104/t0106 schema").

### The Pool-Restart Cadence (10) Is Already Set; No Driver Edit Needed

[t0112] tightened `_POOL_RESTART_EVERY` from [t0106]'s 25 to 10 at
`tasks/t0112_t0106_seed77_replicate/code/nsga2_driver.py:97`. The [t0112] result note (see
`tasks/t0112_t0106_seed77_replicate/results/results_summary.md` lines 39-41 and
`tasks/t0112_t0106_seed77_replicate/results/suggestions.json` suggestion `S-0112-07`) shows the
cadence-10 protocol produced a 3.5x per-generation wall-clock speedup (620 s/gen vs 2,167 s/gen) at
no algorithmic cost to frontier geometry. t0113 inherits this verbatim — no edit needed at line 97.
The `_save_algorithm_config` writer (line 442) will record `pool_restart_every: 10` in
`algorithm_config.json` automatically.

### The HV-Plateau Auto-Stop and N_GEN=60 Ceiling Are Both Inherited from t0112

The HV-plateau constants (`HV_PLATEAU_WINDOW = 2`, `HV_PLATEAU_MIN_HV_HISTORY = 60`,
`HV_PLATEAU_REL_THRESHOLD = 0.01`) in `constants_morphology.py:120-122` are unchanged from [t0112]
(and from [t0106]). `N_GEN = 60` in `constants_morphology.py:111` is unchanged from [t0112]. The
plateau detector fired at gen 21 in [t0112] (well below the 60-gen ceiling). t0113 will likely
plateau anywhere from gen 15-50 depending on the seed, but the ceiling and the detector parameters
do not change.

### The Cost Watchdog Wiring Already Reads T0112_HARD_BUDGET_USD By Name

The cost watchdog is constructed in `nsga2_driver.py:487-491` via
`make_watchdog_from_machine_log(machine_log_path=..., instance_started_at=..., hard_budget_usd=T0112_HARD_BUDGET_USD)`.
After the `constants.py` rename, this reference becomes `hard_budget_usd=T0113_HARD_BUDGET_USD`
automatically as part of the global package-path rewrite plus the constant rename. The watchdog
factory reads `logs/steps/008_setup-machines/machine_log.json`, extracts
`selected_offer.price_per_hour`, and constructs a `CostWatchdog` instance pinned to that hourly
rate. The 129-line `cost_watchdog.py` is copied verbatim into t0113. The only knob that changes is
the budget constant name; the value ($25.00) is unchanged.

### The t0107 8-Direction Caveat Is Out of Scope but Belongs in the Reporting Stage

[t0107] re-evaluated 10 randomly selected cells from the [t0106] top-50 at 8 directions and found
the t0106 ratio DSI of ~0.94 dropped to 8-direction vector-sum DSI of ~0.52, with rank order
preserved (Spearman ρ = 0.758, p = 0.011). **This is out of scope for t0113**: the task brief
explicitly forbids any change to the substrate, objective, or evaluator. t0113 is a like-for-like
seed sweep, so it must report ratio DSI in the same metric and the same 2-direction protocol as
[t0106] / [t0112]. The [t0107] result is documented here only to signal that downstream comparison
against literature should use the 8-direction vector-sum re-evaluation, not the 2-direction ratio
DSI raw number. The task brief's `cross_references` section (lines 183-185) makes this caveat
explicit and tags S-0112-05 as the polar follow-up suggestion that should be cloned for t0113.

### The Three-Seed Sample (44, 77, 2247) Is Still a 3-Point Estimator

The S-0112-01 suggestion (`tasks/t0112_t0106_seed77_replicate/results/suggestions.json` lines 4-15)
asked for >= 3 additional seeds at cadence 10 to lift the substrate-rate estimate from a 2-point
sample (seeds 44 + 77 = 123 + 7 = 130 cells over 5,760 evals = 2.26% raw mean) to a 5-point sample.
t0113 contributes **one** of those additional seeds; two more seeds are required to complete the
S-0112-01 batch. The combined 3-seed estimate (44, 77, 2247) will be:

* Mean joint-pass rate = (123/3744 + 7/2016 + N_2247/M_2247) / 3, with N_2247 and M_2247 being the
  t0113 outputs.
* Standard error proportional to 1/sqrt(3) of the cross-seed dispersion; even if t0113 lands exactly
  at the 2.26% prior mean, the SE will not yet allow a confident comparison against the Hay2011
  0.40% / Druckmann2007 0.10% literature baselines (the dispersion between 3.3% and 0.35% is so
  large that 3 seeds gives a low-power test).

This research stage does not change the substrate property of the result; it simply notes that the
S-0112-01 acceptance-rate claim still requires the 4th and 5th seeds to follow.

## Common Patterns

### Path Management

[t0112] (and the entire NSGA-II lineage from t0091 forward) centralises all paths in `paths.py`,
including (a) the **upstream** [t0080] MOD library resolver `resolve_t99_mod_library`
(`paths.py:36-49`), (b) per-seed result file factories (`pareto_front_json(seed=...)`,
`all_evaluations_json(seed=...)`, `hv_trajectory_json(seed=...)`, `checkpoint_json(seed=...)`,
`init_pop_json(seed=...)`), and (c) step-scoped log paths (`hv_trace_jsonl(step_id=...)`,
`checkpoint_dill(seed=..., gen=..., step_id=...)`, `stop_signal_md()`,
`budget_overrun_md(seed=...)`). t0113 inherits this convention verbatim by copying `paths.py` with
the package-path rewrite. The seed-2247 per-seed file names will automatically be
`pareto_front_seed2247.json`, `all_evaluations_seed2247.json`, `hv_trajectory_seed2247.json`, etc.

### Per-Seed Asset Naming

[t0106] used the predictions ID `nsga2-seed44-bedb-morph-2dir-300gen`; [t0112] used
`t0112-bedb-morph-nsga2-seed77`. t0113's task brief specifies `t0113-bedb-morph-nsga2-seed2247` (see
`task_description.md` lines 87-88). The naming convention follows
`t<TASK_ID>-bedb-morph-nsga2-seed<SEED>` from [t0112] forward. The predictions asset folder name
MUST match `predictions_id` in `details.json` (per `meta/asset_types/predictions/specification.md`).

### Run Orchestration

[t0112]'s `run_seed77.sh` (`tasks/t0112_t0106_seed77_replicate/code/run_seed77.sh`, 49 lines) is the
canonical orchestration script: it runs Phase A (random_init build), imports `bootstrap` to compile
the t0080 MOD library if needed, then launches the NSGA-II driver with
`--save-algorithm-config --teardown-on-watchdog`. For t0113 the script is renamed to
`run_seed2247.sh` with `SEED=2247` at line 39 and the `tasks.t0112_t0106_seed77_replicate` module
paths swapped for `tasks.t0113_t0106_seed2247_replicate` at lines 30, 35-36, 43. The
`/root/t0112_workdir` path at line 22 should be renamed to `/root/t0113_workdir` for clarity (or
left alone; only the agent's setup-machines step interacts with it).

### Smoke Gate

[t0112]'s `smoke_gate.py` (192 lines) runs five local pre-launch checks: single-eval driver run on
the 5 anchors with the t0083 best-cell electrophys vector, ratio DSI synthetic sanity, silence-
guard pytest (`test_evaluator_dsi_guard.py`), pool-restart sanity, watchdog wiring. The expected
PD-rate for anchor 1 (bedb_like) is ~43.6 Hz with a relaxed +/- 2 Hz tolerance to account for the
sqrt(20/3) noise variance increase at N_EVAL_SEEDS=3 vs the t0099 N=20 calibration. All five must
pass before any Vast.ai provisioning.

## Reusable Code and Assets

Per the cross-task rule, **every** non-library module from [t0112] below is **copy into task**. The
library-asset imports from [t0024] and [t0090] / [t0092] are existing full-path task imports, not
library entry-point imports, but they remain valid in t0113 without any rewrite because they point
at upstream task code.

### Copy into task — algorithm-critical, verbatim except for the package-path rewrite

* `tasks/t0112_t0106_seed77_replicate/code/__init__.py` (0 lines) — package marker.
* `tasks/t0112_t0106_seed77_replicate/code/bootstrap.py` (161 lines) — NEURON DLL loader; patches
  [t0024]'s `load_neuron` to load the [t0080] MOD library. Side-effect import; do not edit.
* `tasks/t0112_t0106_seed77_replicate/code/apply_params.py` (234 lines) — 54-d electrophys-to-cell
  write function. Signature:
  `apply_parameter_vector(*, cell: DSGCCellWithAIS, vector: NDArray) -> None`.
* `tasks/t0112_t0106_seed77_replicate/code/build_cell_ais.py` (79 lines) — `DSGCCellWithAIS`
  dataclass.
* `tasks/t0112_t0106_seed77_replicate/code/extend_with_ais.py` (127 lines) — AIS extender used by
  `apply_params`.
* `tasks/t0112_t0106_seed77_replicate/code/parametric_placer.py` (105 lines) — synapse placer; no
  task-specific knobs.
* `tasks/t0112_t0106_seed77_replicate/code/recorder.py` (122 lines) — Vm recording helper.
* `tasks/t0112_t0106_seed77_replicate/code/trial_helpers.py` (311 lines) — `_bar_arrival_times`,
  `_rates_with_ar2_noise`, `_gaba_prob_for_direction`, `_rates_to_events`, `_count_spikes`,
  `setup_synapses_parametric`, plus `BASE_ACH_PROB`, `RATE_DT_MS`.
* `tasks/t0112_t0106_seed77_replicate/code/generator_wrapper.py` (105 lines) — adapter around
  [t0092]'s `generate_fixed_morphology`. Signature:
  `build_cell(*, morph_params: MorphologyParams, morph_seed: int) -> MorphologyResult`.
* `tasks/t0112_t0106_seed77_replicate/code/cost_watchdog.py` (129 lines) — Vast.ai cost watchdog;
  exports `CostWatchdog`, `load_hourly_rate_from_machine_log`, `make_watchdog_from_machine_log`,
  `patch_t99_loop_rate`. Verbatim. Only the budget constant name changes via `constants.py`.
* `tasks/t0112_t0106_seed77_replicate/code/hv_plateau_watchdog.py` (89 lines) — HV-plateau
  termination; signature: `HVPlateauTermination(seed=task_seed)`. Verbatim.
* `tasks/t0112_t0106_seed77_replicate/code/evaluator.py` (504 lines) — `BedBV3MorphProblem`,
  `evaluate_68d_vector`. Verbatim.
* `tasks/t0112_t0106_seed77_replicate/code/constants_electrophys.py` (547 lines) — verbatim (no
  t0112-specific references inside).
* `tasks/t0112_t0106_seed77_replicate/code/anchor_definitions.py` (149 lines),
  `anchor_classifier.py` (127 lines), `biological_priors.py` (252 lines), `biological_scorecard.py`
  (183 lines) — needed by `smoke_gate.py`. Verbatim.
* `tasks/t0112_t0106_seed77_replicate/code/nsga2_driver.py` (734 lines) — verbatim algorithm. Only
  the package-path rewrite applies; `_POOL_RESTART_EVERY = 10` is kept at line 97.
* `tasks/t0112_t0106_seed77_replicate/code/test_evaluator_dsi_guard.py` (164 lines) — silence-guard
  pytest. Copy verbatim and rerun under t0113 imports as part of smoke gate.

### Copy into task — receives a real patch

| File | Source | Patch |
| --- | --- | --- |
| `constants.py` | t0112 (114 lines) | Rename `T0112_SEEDS = (77,)` -> `T0113_SEEDS = (2247,)` at line 59. Rename `T0112_HARD_BUDGET_USD` -> `T0113_HARD_BUDGET_USD` at line 60 (value 25.00 unchanged). Rename `T0112_PER_INSTANCE_WATCHDOG_USD` -> `T0113_PER_INSTANCE_WATCHDOG_USD` at line 61 (value 20.00 unchanged). Update backwards-compat aliases (`T0104_*`, `T0106_*`) to reference `T0113_*` at lines 66-71. Update `__all__` export list at lines 77-114 to swap the three `T0112_*` names for `T0113_*`. Update assertion comments at lines 73-75. |
| `constants_morphology.py` | t0112 (159 lines) | No constant change; `N_GEN = 60` stays at 60. Package-path rewrite of the import block at lines 49-60 (swap `tasks.t0112_t0106_seed77_replicate` -> `tasks.t0113_t0106_seed2247_replicate`). |
| `paths.py` | t0112 (218 lines) | Replace every occurrence of `t0112_t0106_seed77_replicate` with `t0113_t0106_seed2247_replicate`. |
| `random_init.py` | t0112 (101 lines) | Rename `T0112_SEEDS` import to `T0113_SEEDS` at line 21. Package-path rewrite of the import block at lines 18-26. |
| `smoke_gate.py` | t0112 (192 lines) | Package-path rewrite at lines 26-43. No algorithm change. |
| `run_seed77.sh` | t0112 (49 lines) | Rename to `run_seed2247.sh`. Change `SEED=77` at line 39 to `SEED=2247`. Swap `tasks.t0112_t0106_seed77_replicate` for `tasks.t0113_t0106_seed2247_replicate` at lines 30, 35-36, 43. |

### Cross-task imports kept (no copy)

These are full-path imports of UPSTREAM task code, not library imports, but the verificator allows
them and the entire t0080 -> t0106 -> t0112 lineage uses the same pattern. They remain unchanged in
t0113:

* `tasks.t0024_port_de_rosenroll_2026_dsgc.code.constants` and `.ar2_noise.generate_ar2_batch` —
  upstream constants and AR(2) noise generator (Bed B port). Used by `trial_helpers.py` and
  `evaluator.py`. No change.
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.mods/` — the **compiled MOD library**
  (`x86_64/.libs/libnrnmech.so`) is resolved at runtime by `paths.py:resolve_t99_mod_library`. Linux
  build is via `nrnivmodl` on the Vast.ai instance.
* `tasks.t0090_morphology_generator_diversity_test.code.morphology_params` — `MorphologyParams`,
  `MorphologyResult`, `MorphometricSummary` dataclasses (14-d morphology spec).
* `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix` and
  `baseline_channels.insert_baseline_channels` — patched generator (canonical via [t0093] correction
  C-0093-01).

### Library imports via registered entry points — none

No library is imported via its registered entry point. The cross-task imports above use the raw
`code/` module paths, identical to the t0078 -> t0106 -> t0112 lineage convention. This is
intentional and unchanged from [t0112].

### Analysis modules to port on demand (analysis stage)

The [t0112]-specific analysis modules below operate on two seeds (44, 77). For t0113's three-seed
analysis they need adapter changes; defer to the analysis stage:

* `tasks/t0112_t0106_seed77_replicate/code/build_t0112_results.py` (303 lines) — produces the 5
  task-specified charts and the joint-pass-summary CSV. Adapt to read three sources (t0106 seed 44,
  t0112 seed 77, t0113 seed 2247) and emit `*_3seeds.png` plus `joint_pass_summary_3seeds.csv` /
  `pareto_front_overlap_3seeds.csv` per `task_description.md` lines 131-138.
* `tasks/t0112_t0106_seed77_replicate/code/cross_seed_analysis.py` (317 lines) — generic cross-seed
  framework; needed for the 5 task charts.
* `tasks/t0112_t0106_seed77_replicate/code/build_morphology_charts.py` (328 lines) — needed for
  `top50_morphologies_seed2247.png` (chart 4 of 5 in the task brief).
* `tasks/t0112_t0106_seed77_replicate/code/build_predictions_assets.py` (528 lines) — writes the
  `details.json` and the gzipped evaluations file. Adapt the predictions ID and metrics to t0113
  values.
* `tasks/t0112_t0106_seed77_replicate/code/make_charts.py` (345 lines) — chart orchestrator; ports
  with the package-path rewrite.
* `tasks/t0112_t0106_seed77_replicate/code/metrics_builder.py` (81 lines) — builds
  `results/metrics.json` from the per-seed JSON outputs.
* `tasks/t0112_t0106_seed77_replicate/code/per_seed_analysis.py` (99 lines), `run_local_analysis.py`
  (35 lines) — convenience runners.

## Lessons Learned

### A Cadence-10 Pool Restart Is the Project-Default Speedup

[t0112] proved the 3.5x per-generation wall-clock speedup at cadence 10 is robust (620 s/gen vs
[t0106]'s 2,167 s/gen) with no algorithmic cost to Pareto-front geometry: best DSI 0.9535 vs
[t0106]'s 0.9606 (within noise) and best PD-rate 114.76 Hz vs 122.62 Hz (94%). The change is a
single line in `nsga2_driver.py:97`. t0113 inherits this without further modification. Suggestion
S-0112-07 proposes promoting the cadence-10 to the project default; t0113 is consistent with that
direction.

### Two Seeds Span a 17x Range in Joint-Pass Density

[t0106] (seed 44) found 123 unique joint-pass cells across 3,744 evals (3.3% acceptance); [t0112]
(seed 77) found 7 unique joint-pass cells across 2,016 evals (0.35% acceptance). The between-seed
dispersion is ~17x. This is the central motivation for the random-seed S-0112-01 batch and for t0113
specifically: with only two points the substrate-level acceptance rate is not a substrate property.
Even with t0113 added as a third point, the SE will remain wide; the S-0112-01 batch requires two
further seeds to complete.

### Single GA Seed Reaches the Same Pareto Corner

Both [t0106] (seed 44, best DSI 1.0000 / best PD 122.62 Hz) and [t0112] (seed 77, best DSI 0.9535 /
best PD 114.76 Hz) reach the same upper-corner Pareto region. The substrate is therefore not
seed-specific in terms of reachability; what varies is the **density** of joint-pass cells in the
neighbourhood of that corner. The S-0112-04 suggestion (z-scored parameter-space distance) is the
right tool to test whether seed-2247 cells share a basin with seed-44 / seed-77 cells; if S-0112-04
is implemented before t0113's analysis stage, use it for the `pareto_front_overlap_3seeds.csv`
headline distance; otherwise report raw L2 alongside per-dimension z-scored L2 and document the
choice.

### HV-Plateau Detector Fires Early but May Censor the Long Tail

[t0112]'s HV-plateau detector fired at gen 21 (well below the 60-gen ceiling), and [t0106] produced
most of its joint-pass cells in gens 21-39 — i.e., after [t0112]'s auto-stop generation. The 7-cell
vs 123-cell joint-pass disparity may be partly explained by the detector censoring the long tail
when the seed-77 local mode is "deep but narrow". Suggestion S-0112-03 proposes disabling the
HV-plateau termination on a re-run to test this; t0113 keeps the detector active per the task brief
(which forbids any change beyond the seed/budget constant). If t0113 plateaus before gen 30 and
finds <= 10 joint-pass cells, the censoring hypothesis hardens and S-0112-03 becomes a priority
follow-up.

### Cost Headroom Is Comfortable

[t0106] spent $10.37 at the 40-gen cadence-25 pace; [t0112] spent $1.99 at the 21-gen cadence-10
pace; the $25 cap is comfortable in both directions. t0113 budget is $25 hard cap with $20
per-instance watchdog, matching [t0112]. Expected actual spend is $2-11 depending on whether the
seed plateaus at gen 15-25 (like [t0112]) or runs to gen 40+ (like [t0106]). The project
total_budget was raised from $75 to $100 ahead of t0113 (see git log entry `9eb55892`); the envelope
check is satisfied.

### The Predictions Asset Is the Only Mandatory Output

[t0112]'s code tree has ~2,600 lines of analysis modules. t0113's brief lists 5 charts and 2 CSVs,
but the **mandatory** path is the per-cell predictions table at
`assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz` plus the
matching `details.json` and `description.md`. The 5 charts and 2 CSVs are analysis-stage outputs,
not asset outputs. This keeps the implementation step tight.

### t0107 Caveat Belongs in the Reporting Stage, Not in the Run

[t0107]'s 8-direction polar re-evaluation showed the 2-direction ratio DSI overstates selectivity by
~0.42 absolute. The task brief explicitly forbids any evaluator change in t0113. The reporting stage
should note the caveat in the same language [t0106] and [t0112] used: "DSI values reported are
2-direction ratio DSI; conventional 8-direction vector-sum DSI is expected ~0.42 lower in absolute
value per t0107". A follow-up suggestion mirroring S-0112-05 should be generated to track
8-direction re-evaluation of any t0113 joint-pass cells.

## Recommendations for This Task

1. **Fork the [t0112] `code/` directory verbatim** into
   `tasks/t0113_t0106_seed2247_replicate/code/`, using a single copy + global package-path rewrite
   (`tasks.t0112_t0106_seed77_replicate` -> `tasks.t0113_t0106_seed2247_replicate`) across all `.py`
   and `.sh` files. Do not edit any algorithm logic.

2. **Apply exactly one constant patch** in `constants.py`:
   * Line 59: `T0112_SEEDS: tuple[int, ...] = (77,)` -> `T0113_SEEDS: tuple[int, ...] = (2247,)`.
   * Line 60: `T0112_HARD_BUDGET_USD: float = 25.00` -> `T0113_HARD_BUDGET_USD: float = 25.00`
     (value unchanged; only the name changes).
   * Line 61: `T0112_PER_INSTANCE_WATCHDOG_USD: float = 20.00` ->
     `T0113_PER_INSTANCE_WATCHDOG_USD: float = 20.00` (value unchanged).
   * Update the backwards-compat aliases at lines 66-71 (`T0104_*`, `T0106_*`) to point at the new
     `T0113_*` constants.
   * Update the `__all__` export list at lines 77-114 to swap the three `T0112_*` names for
     `T0113_*`.
   * `nsga2_driver.py:97` `_POOL_RESTART_EVERY = 10` stays unchanged; `constants_morphology.py`
     `N_GEN = 60` stays unchanged.

3. **Verify the predictions asset schema matches [t0112] exactly** before launching. The asset
   folder must be named `t0113-bedb-morph-nsga2-seed2247` (per task brief lines 87-88), the
   `details.json` must list `spec_version: "2"`, and the `prediction_schema` string must declare the
   same five per-cell fields (`generation`, `vector_68d`, `objective_F_minimised`, `dsi_vector_sum`,
   `pd_rate_hz`). Keep the `dsi_vector_sum` field name even though it stores the ratio DSI.

4. **Run the smoke gate locally before any Vast.ai provisioning** — the [t0112] 5-check protocol is
   already wired in `smoke_gate.py` (single-eval driver run, ratio DSI synthetic sanity,
   silence-guard pytest, pool-restart sanity, watchdog wiring). All five must pass before
   `setup-machines`. The expected anchor-1 PD-rate is ~43.6 Hz with a relaxed +/- 2 Hz tolerance.

5. **Wire the cost watchdog explicitly with `T0113_HARD_BUDGET_USD = 25.00`** at the
   `make_watchdog_from_machine_log(...)` call site in `nsga2_driver.py:487-491`. Do not rely on the
   legacy `T0104_HARD_BUDGET_USD = 4.00` default that lives in `cost_watchdog.py:27`.

6. **Do not import any registered library entry point**. The lineage convention is full-path task
   imports of upstream `code/` modules; t0113 preserves this exactly. Keep the upstream imports of
   t0024, t0080, t0090, t0092 unchanged.

7. **Defer the analysis modules** (`build_t0112_results.py`, `cross_seed_analysis.py`,
   `build_morphology_charts.py`, `build_predictions_assets.py`, `make_charts.py`,
   `metrics_builder.py`, `per_seed_analysis.py`, `run_local_analysis.py`) to the analysis stage. The
   implementation stage only needs the driver, the random-init builder, the predictions asset
   writer, and the smoke gate. The 5 task-specified charts and 2 CSVs are analysis-stage outputs;
   they require adapter changes to read three seed sources (44, 77, 2247) instead of two.

8. **Single-seed orchestration**: rename `run_seed77.sh` to `run_seed2247.sh`, set `SEED=2247` at
   line 39, and swap `tasks.t0112_t0106_seed77_replicate` for `tasks.t0113_t0106_seed2247_replicate`
   at lines 30, 35-36, 43.

9. **Note the random-seed provenance in the predictions asset `model_description`**. The asset
   description should mention that GA seed 2247 was drawn via `secrets.randbelow(10000)` to avoid
   selection bias, matching the framing in `task_description.md` lines 21-26.

10. **Generate t0113 follow-up suggestions** mirroring S-0112-05 (8-direction polar re-evaluation of
    t0113 joint-pass cells) and S-0112-06 (N_EVAL_SEEDS >= 20 robustness retest of t0113 joint-pass
    cells) in the reporting stage, scoped to t0113 cells only (distinct from the [t0112]-scoped
    suggestions).

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Upstream Bed B substrate definition. t0113's `evaluator.py` and `trial_helpers.py`
  import `tasks.t0024_*.code.constants` and `ar2_noise.generate_ar2_batch` directly. No change vs
  [t0112].

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Owns the canonical Linux MOD library (13 `.mod` files compiled under
  `mods/x86_64/`) resolved at runtime by t0113 (via [t0106] / [t0112])
  `paths.py:resolve_t99_mod_library`. The package-path rewrite does NOT change this dependency.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Morphology generator diversity test
* **Status**: completed
* **Relevance**: Defines the `MorphologyParams`, `MorphologyResult`, `MorphometricSummary`
  dataclasses imported by t0113 `evaluator.py` (via [t0112]'s copy). The library
  `procedural_dsgc_morphology_generator` is registered here but t0113 uses the [t0092]-patched
  generator per correction C-0093-01.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology generator silence
* **Status**: completed
* **Relevance**: Owns the patched `morphology_generator_fix` and `baseline_channels` modules
  imported by t0113 `generator_wrapper.py`. The patched generator is canonical via [t0093]
  correction C-0093-01.

### [t0093]

* **Task ID**: `t0093_resweep_and_t0090_correction`
* **Name**: Patched-generator full 60-morph re-sweep + t0090 correction overlay
* **Status**: completed
* **Relevance**: Issued correction C-0093-01 marking [t0090]'s generator as superseded by [t0092]'s
  patched generator. t0113 (via [t0106] -> [t0112]) imports [t0092]'s patched generator per this
  correction.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init
* **Status**: completed
* **Relevance**: Distant ancestor of t0113; established the pop=96 N_EVAL_SEEDS=4 gens=20 NSGA-II
  template and the `dsi_vector_sum` field name convention t0113 still uses. The silence guard
  (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`) originates here.

### [t0104]

* **Task ID**: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* **Name**: 68-d 2-objective (DSI + PD-rate) NSGA-II at GA seeds=3, N=4, gens=20
* **Status**: completed
* **Relevance**: Drop-robustness-objective predecessor of [t0106]; established the 2-objective HV
  reference point `[0.0, 0.0]` and the `TerminationCollection` pattern (MaxGen + HVPlateau +
  CostWatchdog) inherited unchanged by t0106 / t0112 / t0113.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long 2-direction NSGA-II at 300 gens, 1 seed, 3 trials (ratio DSI + PD-rate)
* **Status**: completed
* **Relevance**: Grandparent task and dependency of t0113. Established the 2-direction ratio DSI
  protocol, the 68-d substrate, the predictions asset schema (`spec_version: "2"`), and the seed-44
  baseline run (123 unique joint-pass cells, best ratio DSI = 1.0000, best PD-rate = 122.62 Hz,
  final HV = 122.0288, cost $10.37) that t0113 is compared against.

### [t0107]

* **Task ID**: `t0107_t0106_polar_8dir_recheck`
* **Name**: 8-direction polar re-evaluation of 10 random top-50 t0106 cells
* **Status**: completed
* **Relevance**: Out-of-scope caveat task. Shows [t0106]'s 2-direction ratio DSI overstates
  selectivity by ~0.42 absolute under conventional 8-direction vector-sum protocol. Relevant only
  for the t0113 reporting stage, not for the experiment-run step. Drives the t0113-cloned follow-up
  suggestion mirroring S-0112-05.

### [t0112]

* **Task ID**: `t0112_t0106_seed77_replicate`
* **Name**: Seed-77 minimum-change replicate of t0106 long 2-direction NSGA-II
* **Status**: completed
* **Relevance**: **Direct fork base and dependency of t0113.** Provides the entire code tree to copy
  (35 files, 8,427 lines), the predictions asset schema to mirror, the cadence-10
  `_POOL_RESTART_EVERY` setting to inherit, the N_GEN=60 ceiling, the HV-plateau detector
  configuration, the smoke-gate harness to re-run, the orchestration script template
  (`run_seed77.sh` -> `run_seed2247.sh`), the analysis modules to port on demand, and the seed-77
  baseline run (7 unique joint-pass cells, best ratio DSI = 0.9535, best PD-rate = 114.76 Hz, final
  HV = 107.4602, cost $1.99) that t0113 is compared against alongside [t0106]. Source of S-0112-01
  (the suggestion t0113 partially fulfils), S-0112-04 (z-scored parameter-space distance metric
  proposed for analysis stage), and S-0112-07 (promote cadence-10 to project default).

### [t0010]

* **Task ID**: `t0010_hunt_missed_dsgc_models`
* **Name**: Hunt DSGC compartmental models missed by prior survey; port runnable ones
* **Status**: completed
* **Relevance**: Owns the empty `assets/library/` directory referenced by [t0112]'s research code
  enumeration; the only library asset directory with no contents. Not used by t0113. Listed here
  only to fully account for the 18-library landscape inherited from [t0112].
