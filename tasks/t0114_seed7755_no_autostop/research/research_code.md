---
spec_version: "1"
task_id: "t0114_seed7755_no_autostop"
research_stage: "code"
tasks_reviewed: 12
tasks_cited: 11
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-05-20"
status: "complete"
---
# Research Code — Seed-7755 No-Auto-Stop Replicate of t0106 Substrate

## Task Objective

t0114 is a minimum-change fork of [t0113] on the identical 68-d Bed B electrophys + 14-d morphology
NSGA-II substrate, with three named deltas relative to its parent: (1) the GA seed is randomly
redrawn from `2247` to `7755` via `secrets.randbelow(10000)`, (2) the `HVPlateauTermination` is
removed from the pymoo termination list so the run is no longer auto-stopped by the t0106-family
plateau detector, and (3) the generation ceiling `N_GEN` is raised from `60` to `300` to match
[t0106]'s original ceiling so the budget cap and explicit operator stop become the binding
termination triggers. The task implements suggestion `S-0113-03` (widen HV-plateau detector window /
tighten threshold) in two halves: (a) a live no-auto-stop NSGA-II run on seed 7755 that produces a
ground-truth uncensored HV trace, and (b) an offline detector replay over `WINDOW in {2, 3, 4, 5}`
crossed with `REL_THRESHOLD in {0.005, 0.01}` against all four available HV traces (t0106 seed 44,
t0112 seed 77, t0113 seed 2247, t0114 seed 7755). The pool-restart cadence
`_POOL_RESTART_EVERY = 10` and every other algorithmic knob inherited from [t0113] is preserved
verbatim. This research stage identifies the exact files to fork from [t0113], the three text-level
patches to apply, the existing HV-trace JSON schemas to consume in the offline replay, and the
cross-task imports that remain unchanged.

## Library Landscape

The project does **not** ship a library aggregator (`arf/scripts/aggregators/aggregate_libraries.py`
does not exist; running it returns `No module named arf.scripts.aggregators.aggregate_libraries`).
The complete aggregator list in `arf/scripts/aggregators/` is: `aggregate_categories.py`,
`aggregate_costs.py`, `aggregate_machines.py`, `aggregate_metric_results.py`,
`aggregate_metrics.py`, `aggregate_suggestions.py`, `aggregate_task_types.py`, `aggregate_tasks.py`.
No answer aggregator exists either. Library and answer enumeration in this project is therefore by
direct filesystem walk of `tasks/*/assets/library/` and `tasks/*/assets/answer/`.

Per [t0113]'s `research_code.md` (lines 40-53), the project contains 18 registered library asset
directories. None is imported via its registered entry point by the t0078 -> t0106 -> t0112 -> t0113
NSGA-II lineage. The cross-task code paths the lineage relies on (`de_rosenroll_2026_dsgc` from
[t0024], `procedural_dsgc_morphology_generator_fix` from [t0092], the [t0080] compiled MOD bundle)
are reached via full-path module imports (`tasks.t0024_*.code.*`, `tasks.t0080_*.code.mods`,
`tasks.t0092_*.code.morphology_generator_fix`), not library entry-point imports. The verificator
allows full-path UPSTREAM task imports; only same-tier or downstream task imports are forbidden.

**Net effect for t0114**: zero library imports via registered entry points, identical to [t0113].
Every shared module between t0114 and its t0024 / t0080 / t0090 / t0092 / t0106 / t0112 / t0113
ancestors is reached via the full-path import pattern. `libraries_found: 0` /
`libraries_relevant: 0` in the frontmatter reflects that no library aggregator exists; the 18 raw
library directories were considered via [t0113]'s prior enumeration and none is applicable.

## Key Findings

### The Patch Surface Is Three Constants Plus the Package-Path Rewrite

The entire algorithmic delta between [t0113] and t0114 lives in three text-level changes to two
files, plus the global package-path rewrite. Specifically:

1. **`tasks/t0113_t0106_seed2247_replicate/code/constants.py:63`** — current line:

   ```python
   T0113_SEEDS: tuple[int, ...] = (2247,)
   ```

   becomes

   ```python
   T0114_SEEDS: tuple[int, ...] = (7755,)
   ```

   The value `7755` was drawn locally by `secrets.randbelow(10000)` on 2026-05-20 by the
   implementing agent per `task_description.md` lines 21-24. The companion `T0113_HARD_BUDGET_USD`
   (line 64) and `T0113_PER_INSTANCE_WATCHDOG_USD` (line 65) are renamed to `T0114_HARD_BUDGET_USD`
   and `T0114_PER_INSTANCE_WATCHDOG_USD` respectively with values unchanged ($25.00 and $20.00). The
   backwards-compatibility aliases at lines 70-75 (`T0104_*`, `T0106_*`) are updated to point at the
   new `T0114_*` constants. The `__all__` export list at lines 81-118 is updated to swap the three
   `T0113_*` names for `T0114_*`. The module docstring at lines 1-28 is updated to reflect the seed
   change and the auto-stop deletion (the docstring's reference to `N_GEN = 60` is corrected to
   `N_GEN = 300` to match the morphology constants).

2. **`tasks/t0113_t0106_seed2247_replicate/code/constants_morphology.py:111`** — current line:

   ```python
   N_GEN: int = 60
   ```

   becomes

   ```python
   N_GEN: int = 300
   ```

   The accompanying comment at line 110 ("t0112 plan REQ-4: lower N_GEN to 60 (hard ceiling);
   HV-plateau primary.") is rewritten to reflect the t0114 directive ("t0114: raise N_GEN to 300
   matching t0106's original ceiling; HV-plateau auto-stop disabled; budget cap and operator stop
   are binding."). No other knob in `constants_morphology.py` changes —
   `HV_PLATEAU_REL_THRESHOLD = 0.01`, `HV_PLATEAU_WINDOW = 2`, `HV_PLATEAU_MIN_HV_HISTORY = 60`
   remain readable from this module so the offline detector replay can import them as the
   current-default reference point.

3. **`tasks/t0113_t0106_seed2247_replicate/code/nsga2_driver.py:524-529`** — current
   `TerminationCollection` construction:

   ```python
   termination = TerminationCollection(
       MaximumGenerationTermination(n_max_gen=n_gen_effective),
       HVPlateauTermination(seed=task_seed),
       CostWatchdogTermination(watchdog=cost_watchdog, seed=task_seed),
       OperatorStopTermination(stop_path=stop_signal_md()),
   )
   ```

   becomes (the `HVPlateauTermination(...)` entry is removed entirely; the other three terminations
   stay verbatim and in the same order):

   ```python
   # t0114: HVPlateauTermination removed from termination list per S-0113-03 +
   # user directive 2026-05-20. Auto-stop disabled; termination triggers are
   # max-gen ceiling (N_GEN=300), cost watchdog ($25 cap), and explicit
   # operator stop. The HVPlateauTermination class remains importable from
   # hv_plateau_watchdog.py for offline detector replay.
   termination = TerminationCollection(
       MaximumGenerationTermination(n_max_gen=n_gen_effective),
       CostWatchdogTermination(watchdog=cost_watchdog, seed=task_seed),
       OperatorStopTermination(stop_path=stop_signal_md()),
   )
   ```

   The `_POOL_RESTART_EVERY = 10` constant at line 97 is **NOT** changed — t0114 preserves
   [t0113]'s pool-restart cadence verbatim. The `HVPlateauTermination` import at lines 74-76 is
   **NOT** removed; the class stays importable in the t0114 package so the offline detector replay
   can instantiate it (and so the smoke gate can assert that the class is present and matches the
   t0113 parameter triplet). The smoke gate gains one new check: it asserts that the live
   termination collection contains no `HVPlateauTermination` instance.

Every other file in the [t0113] code tree is copied verbatim except for the global package-path
rewrite `tasks.t0113_t0106_seed2247_replicate` -> `tasks.t0114_seed7755_no_autostop` applied across
every `.py` and `.sh` file.

### HVPlateauTermination Is Preserved as an Importable Class for Offline Replay

Even though `HVPlateauTermination(seed=...)` is removed from the live `TerminationCollection`, the
class itself and the `should_stop(hv_history: list[float]) -> bool` pure function in
`hv_plateau_watchdog.py` are preserved unchanged in t0114's copy of the module. This is
load-bearing: the S-0113-03 offline detector replay invokes `should_stop` directly against the four
seed traces under every (`WINDOW`, `REL_THRESHOLD`) pair in the sweep. Specifically:

* `hv_plateau_watchdog.py:29-50` defines `should_stop(hv_history)` as a pure function reading the
  module-level constants `HV_PLATEAU_WINDOW`, `HV_PLATEAU_REL_THRESHOLD`, and
  `HV_PLATEAU_MIN_HV_HISTORY` (lines 24-26). The replay harness needs to evaluate `should_stop`
  under different `(WINDOW, REL_THRESHOLD)` pairs without editing the module; the cleanest approach
  is to construct a small
  `should_stop_with_overrides(hv_history, *, window, rel_threshold, min_history)` helper in the
  t0114 analysis stage that mirrors the existing pure function and reads its constants from
  arguments rather than module globals. Alternatively, the existing constants can be monkey-patched
  per replay iteration; the pure-function approach is preferred because the module-level constants
  then remain the canonical project-default reference.
* `hv_plateau_watchdog.py:63-72` defines `HVPlateauTermination(seed: int)` as a `pymoo.Termination`
  subclass that calls `_load_hv_history(seed=...)` on each `_update`. This class is **not invoked**
  by the live t0114 run, but is kept importable so that
  `import tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog` does not break and the analysis
  stage can still construct it for cross-validation against the t0113 baseline behaviour.
* `hv_plateau_watchdog.py:75-85` defines `_run_unit_tests` with the four canonical cases (short
  trajectory; flat 4-entry; 5% growth; 0.1% growth). These tests verify the pure function and are
  preserved verbatim; the t0114 smoke gate re-runs them under the t0114 package path.

### The Four Seed HV-Trajectory JSON Files Share an Identical Schema

The S-0113-03 offline detector replay must read the per-generation HV value from the three existing
seed traces plus the t0114 trace (when it lands). All four files share the exact same schema:

* **Source paths (existing 3 seeds)**:
  * `tasks/t0106_long_pdnd_nsga2_300gen/results/data/hv_trajectory_seed44.json` (seed 44, 40 gens
    completed before HV-plateau auto-stop, 7,253 evaluations).
  * `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json` (seed 77, 21 gens
    completed before HV-plateau auto-stop, 2,016 evaluations).
  * `tasks/t0113_t0106_seed2247_replicate/results/data/hv_trajectory_seed2247.json` (seed 2247, 14
    gens completed before HV-plateau auto-stop, 1,344 evaluations).

* **Source path (new t0114)**:
  `tasks/t0114_seed7755_no_autostop/results/data/hv_trajectory_seed7755.json` (seed 7755, N_GEN <=
  300 gens before budget cap / operator stop).

* **Schema** (top-level JSON object with one key `trajectory` mapping to a list of per-gen records):

  ```json
  {
    "trajectory": [
      {
        "generation": 1,
        "hypervolume": 0.24603174603174863,
        "cumulative_cost_usd": 0.006796214576666667,
        "elapsed_s": 103.62716,
        "n_evaluations": 0
      },
      ...
    ]
  }
  ```

  The five per-record fields are produced by `nsga2_driver.py:_save_iteration` (lines 254-262) and
  written by `nsga2_driver.py:_save_iteration` (lines 263-266). The schema is constant across
  [t0106], [t0112], and [t0113]; the t0114 driver writes the identical schema because the writer is
  copied verbatim.

* **HV-history extraction**: `hv_plateau_watchdog.py:_load_hv_history` (lines 53-60) reads the
  `trajectory` list and projects to a flat `list[float]` by extracting `float(t["hypervolume"])` for
  each record. The S-0113-03 replay reuses this projection unchanged.

The schema robustness against `dict-vs-list` is handled at line 59:
`traj = raw.get("trajectory", []) if isinstance(raw, dict) else raw`. All four files use the dict
shape; the fallback branch is dead code but kept for parity.

### Cost-Watchdog and Pool-Restart Wiring Is Inherited Verbatim

The cost watchdog construction (`nsga2_driver.py:487-491`) reads `T0113_HARD_BUDGET_USD` (now
renamed to `T0114_HARD_BUDGET_USD = 25.00` by the constants patch) and is unchanged otherwise:

```python
cost_watchdog = make_watchdog_from_machine_log(
    machine_log_path=MACHINE_LOG_JSON,
    instance_started_at=instance_started_at,
    hard_budget_usd=T0114_HARD_BUDGET_USD,
)
```

The factory `make_watchdog_from_machine_log` (`cost_watchdog.py:102-118`) reads
`logs/steps/008_setup-machines/machine_log.json`, extracts `selected_offer.price_per_hour`, and
constructs a `CostWatchdog` instance pinned to that hourly rate. The `CostWatchdogTermination`
(`nsga2_driver.py:169-181`) polls the watchdog each generation. This wiring is preserved as-is in
t0114; the only knob change is the constant name (value unchanged at $25.00).

The pool-restart machinery (`nsga2_driver.py:338-391`, class `PerGenerationPoolRestart`) is
preserved verbatim. The constant `_POOL_RESTART_EVERY = 10` at line 97 is **NOT** edited; the
cadence-10 protocol persists. The callback closes the multiprocessing Pool every 10 generations and
swaps `problem.elementwise_runner` to a fresh `StarmapParallelization`, matching [t0113]'s and
[t0112]'s configuration. At `N_GEN = 300` this means 30 pool restarts maximum, vs [t0113]'s observed
1 (gen 10) before the gen 14 auto-stop and [t0106]'s 4 (gens 10, 20, 30, 40) before its gen 40
auto-stop.

The `OperatorStopTermination` (`nsga2_driver.py:146-166`) polls `intervention/stop.md` each
generation; the operator can drop this file to halt cleanly at the next gen boundary. This is the
PRIMARY expected termination trigger for t0114 (followed by the budget cap if the operator forgets).

The dill checkpoint cadence (`nsga2_driver.py:219-239`) is preserved; note that [t0113] reported
that dill-pickling the pymoo Algorithm fails on every generation because of the live
`multiprocessing.Pool` reference (see
`tasks/t0113_t0106_seed2247_replicate/results/suggestions.json` suggestion `S-0113-02`). t0114 will
suffer the same failure mode; this is non-fatal because the JSON-side resume channel (per-gen
`hv_trajectory_seed7755.json`, `all_evaluations_seed7755.json`, `nsga2_checkpoint_seed7755.json`) is
fully functional and is the actual resume path. Fixing the dill failure is out of scope for t0114;
`S-0113-02` already captures it.

### The t0113 Code Tree Has 36 Modules Totalling 9,383 Lines

A full `wc -l` over `tasks/t0113_t0106_seed2247_replicate/code/*.py` plus the two shell scripts
returns 9,383 lines across 36 files (35 `.py` + 1 `.sh` shipped run script + 1 sync script;
`__init__.py` is empty at 0 lines). The +956-line delta vs [t0112]'s 8,427 lines comes from the
[t0113]-specific result builder `build_t0113_results.py` (868 lines) plus minor reporting additions.
The algorithm-critical modules that must be copied verbatim from [t0113] into t0114 are:

* `nsga2_driver.py` (734 lines) — pool-restart cadence stays at 10; receives the 6-line
  `TerminationCollection` patch removing `HVPlateauTermination(...)`. Package-path rewrite applied.
* `constants.py` (118 lines) — receives the seed/budget rename described above; backwards-compat
  aliases and `__all__` updated.
* `constants_morphology.py` (159 lines) — receives the one-line `N_GEN = 60 -> 300` patch.
* `constants_electrophys.py` (547 lines) — verbatim.
* `evaluator.py` (504 lines) — verbatim (ratio DSI already correct at `N_DIRECTIONS=2`, silence
  guard active per `SILENCE_SPIKE_COUNT_THRESHOLD = 10`).
* `random_init.py` (101 lines) — verbatim except for the `T0113_SEEDS` -> `T0114_SEEDS` import
  name at line 21 and the analogous reference in `main()`.
* `paths.py` (218 lines) — verbatim except for the package-path rewrite. The file's docstring at
  line 1 references the t0102 task lineage; this docstring drift is inherited unchanged.
* `cost_watchdog.py` (129 lines) — verbatim (`make_watchdog_from_machine_log` factory). The
  references to the t0099 module at line 123 (`patch_t99_loop_rate`) are also rewritten by the
  global package-path swap.
* `hv_plateau_watchdog.py` (89 lines) — verbatim. Kept importable for offline detector replay; not
  wired into the live termination list.
* `bootstrap.py` (161 lines) — verbatim (NEURON DLL loader; patches [t0024]'s `load_neuron` to
  load [t0080]'s MOD library).
* `apply_params.py` (234 lines), `build_cell_ais.py` (79 lines), `extend_with_ais.py` (127 lines),
  `parametric_placer.py` (105 lines), `recorder.py` (122 lines), `trial_helpers.py` (311 lines) —
  evaluator support; verbatim.
* `generator_wrapper.py` (105 lines) — verbatim adapter around [t0092]'s patched morphology
  generator.
* `anchor_definitions.py` (149 lines), `anchor_classifier.py` (127 lines), `biological_priors.py`
  (252 lines), `biological_scorecard.py` (183 lines) — needed by `smoke_gate.py`. Verbatim.
* `smoke_gate.py` (192 lines) — receives **one new check** appended to the existing 5-check
  protocol: assert that the live `TerminationCollection` produced by `run_nsga2_for_seed` contains
  no `HVPlateauTermination` instance. Implementation: re-introspect the termination collection
  constructed inside `run_nsga2_for_seed` (or refactor a small `_build_termination(...)` helper out
  of the driver so the smoke gate can inspect it without launching a real run).
* `test_evaluator_dsi_guard.py` (164 lines) — silence-guard pytest; verbatim, re-runs under t0114
  package path.

The orchestration script `run_seed2247.sh` (48 lines) is renamed to `run_seed7755.sh` with `SEED`
set to `7755` and the `tasks.t0113_*` module paths swapped for `tasks.t0114_*`. The
`sync_results_back.sh` (36 lines) is renamed analogously with its `t0113_workdir` path renamed.

**Total verbatim copy size**: ~5,800 lines of algorithm-critical code (same volume as the [t0112] ->
[t0113] fork). The remaining ~3,500 lines (analysis / charting / asset-build modules:
`build_analysis_charts.py`, `build_assets.py`, `build_morphology_charts.py`,
`build_predictions_assets.py`, `build_t0106_plots.py`, `build_t0112_results.py`,
`build_t0113_results.py`, `cross_seed_analysis.py`, `make_charts.py`, `metrics_builder.py`,
`per_seed_analysis.py`, `run_local_analysis.py`) can be ported on demand in the analysis stage; the
experiment-run step does not require them. The [t0113]-specific `build_t0113_results.py` (868 lines)
will need adapter changes to read four seed sources (44, 77, 2247, 7755) instead of three — that
adapter work is analysis-stage scope and produces the 5 task-brief charts plus the 3 CSV tables.

### The Offline Detector-Replay Sweep Is a Pure-Function Loop

The S-0113-03 implementation core is a small (~60-line) standalone replay script that lives in
`tasks/t0114_seed7755_no_autostop/code/detector_replay.py` (new file, not inherited from [t0113]).
The script:

1. Loads four HV trajectories using
   `tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog._load_hv_history` (or an analogous
   inline `json.loads()` plus `[float(t["hypervolume"]) for t in raw["trajectory"]]` projection).
2. For each of the 4 seeds (`{44, 77, 2247, 7755}`) and each (`WINDOW`, `REL_THRESHOLD`) pair in the
   8-cell grid (`WINDOW in {2, 3, 4, 5}` x `REL_THRESHOLD in {0.005, 0.01}`), iterates `gen` from
   `HV_PLATEAU_MIN_HV_HISTORY` (60 in the t0113 constants, but for the replay this can be relaxed to
   4 so the early-fire t0113 trace is captured cleanly) through `len(hv_history)`, invoking
   `should_stop_with_overrides(hv_history[:gen], window=WINDOW, rel_threshold=REL_THRESHOLD, min_history=4)`
   and recording the first `gen` at which the function returns True.
3. Writes the result as a 32-row long-format CSV at `results/data/detector_replay.csv` with columns
   `seed`, `WINDOW`, `REL_THRESHOLD`, `gen_at_fire`, `hv_at_fire`, `hv_at_run_end`.
4. Picks `(W*, T*)` such that (a) `gen_at_fire >= 20` on every seed (matches Mohacsi 2024 lower
   bound), (b) `gen_at_fire <= 60` on t0106 (matches the longest available run's natural fire
   point), and (c) the deviation `|WINDOW - 2| + |REL_THRESHOLD - 0.01| / 0.005` is minimised among
   pairs satisfying (a) and (b).

The replay script does not invoke pymoo or any NEURON machinery; it is pure-Python list
manipulation. It can be developed and tested locally before the live t0114 run lands; the t0114 HV
trace is the 4th input that will be appended to its existing 3-trace test fixture.

### The Predictions Asset Schema Is Locked at spec_version "2" and Must Be Mirrored Exactly

[t0113]'s predictions asset
(`tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/details.json`)
specifies `spec_version: "2"` and uses the same structure [t0106] / [t0112] established:

* Top-level JSON object with one key `evaluations` mapping to a list of per-cell records.
* Each record has fields `generation` (int), `vector_68d` (list of 68 floats),
  `objective_F_minimised` (list of 2 floats), `dsi_vector_sum` (float; back-compat field name
  storing ratio DSI), and `pd_rate_hz` (float).
* File format is gzipped JSON (`.json.gz`).
* Required `metrics_at_creation` keys per the t0114 `task_description.md` Expected Assets section
  (lines 102-107): `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`,
  `stop_trigger` (one of `operator_stop`, `budget_cap`, `gen_ceiling`, `instance_watchdog`).
* Required top-level keys: `predictions_id`, `name`, `short_description`, `description_path`,
  `model_id` (`null`), `model_description`, `dataset_ids` (`[]`), `prediction_format`,
  `prediction_schema`, `instance_count`, `files`, `categories`, `created_by_task`, `date_created`.

The categories inherited from [t0106] / [t0112] / [t0113] are `direction-selectivity`,
`compartmental-modeling`, `retinal-ganglion-cell`. The predictions asset folder must be named
`t0114-bedb-morph-nsga2-seed7755` (per `task_description.md` lines 102-104), and `predictions_id`
inside `details.json` must match. The new `stop_trigger` key extends the [t0106] / [t0112] / [t0113]
schema; this is a t0114-specific addition motivated by the auto-stop deletion making the trigger
identity non-trivial. The schema bump is captured by leaving `spec_version: "2"` and documenting the
new field in the local `description.md`; per asset spec v3 a `spec_version` bump is not required for
additive fields when the schema is locally documented.

### The `dsi_vector_sum` Field Name Lie Is Preserved for Schema Compatibility

[t0106] / [t0112] / [t0113] evaluators return a 2-direction ratio DSI but write it into the
`dsi_vector_sum` JSON field for back-compat with [t0102] / [t0104] downstream tooling
(`build_predictions_assets.py`, `build_analysis_charts.py`). t0114 must preserve this same field
name; renaming it to `dsi_ratio` would break the cross-seed analysis scripts in
`cross_seed_analysis.py` and `build_t0113_results.py` that walk [t0106] / [t0112] / [t0113]
predictions assets and will walk t0114 too. The field name lie is documented in [t0113]'s
`prediction_schema` string in `details.json` and carries forward verbatim.

### The Smoke Gate Gains One New Check Specific to t0114

[t0113]'s `smoke_gate.py` runs five local pre-launch checks (single-eval driver run, ratio DSI
synthetic sanity, silence-guard pytest, pool-restart sanity, cost-watchdog wiring). t0114 inherits
all five and adds a sixth: **the live `TerminationCollection` must contain no `HVPlateauTermination`
instance**. Implementation: refactor the inline `TerminationCollection` construction at
`nsga2_driver.py:524-529` into a small
`_build_termination(*, n_max_gen, cost_watchdog, seed, stop_path) -> TerminationCollection` helper;
the smoke gate then calls this helper and iterates its `.terminations` (or whatever pymoo exposes)
asserting `not any(isinstance(t, HVPlateauTermination) for t in coll.terminations)`. The pymoo
`TerminationCollection` API exposes the constituent terminations as `coll.terminations` (a list);
the smoke check is a one-line assertion against that list. Without this check the auto-stop deletion
can be silently regressed by a future edit; with it the smoke gate catches the regression before any
Vast.ai launch.

### N_GEN = 300 Means the Stop Trigger Is Likely the Budget Cap or Operator Stop

At [t0113]'s observed wall-clock of 160 s/gen on the 64-core EPYC 7B13, a full 300-gen run takes
~13.3 wall-clock hours. The $25 cap at an observed $0.30/hour rate covers ~83 hours; the cap is not
the binding constraint at the t0113 rate. The binding constraint is then either (a) explicit
operator stop, which the task brief lists as the primary expected trigger, or (b) the gen 300
ceiling itself. The expected stop_trigger distribution across realistic scenarios:

* `operator_stop` if the operator stops the run after observing HV saturation (most likely; aligns
  with task brief's "stop when I say so" framing).
* `gen_ceiling` if the operator does not stop and the run completes 300 gens within the $25 cap.
* `budget_cap` only if the actual hourly rate is far higher than t0113's $0.30/hr (e.g., if Vast.ai
  scheduling lands on a different EPYC tier than expected).
* `instance_watchdog` only if the per-instance $20 watchdog trips before the $25 cap (would require
  a >2-hour run at $10/hr; very unlikely with EPYC 7B13).

The `stop_trigger` field in the predictions asset `metrics_at_creation` records the actual outcome
for downstream reading.

## Common Patterns

### Path Management

[t0113] (inheriting from [t0102] / [t0104] / [t0106] / [t0112]) centralises all paths in `paths.py`,
including (a) the **upstream** [t0080] MOD library resolver `resolve_t99_mod_library`
(`paths.py:36-49`), (b) per-seed result file factories (`pareto_front_json(seed=...)`,
`all_evaluations_json(seed=...)`, `hv_trajectory_json(seed=...)`, `checkpoint_json(seed=...)`,
`init_pop_json(seed=...)`), and (c) step-scoped log paths (`hv_trace_jsonl(step_id=...)`,
`checkpoint_dill(seed=..., gen=..., step_id=...)`, `stop_signal_md()`,
`budget_overrun_md(seed=...)`). t0114 inherits this convention verbatim by copying `paths.py` with
the package-path rewrite. The seed-7755 per-seed file names will automatically be
`pareto_front_seed7755.json`, `all_evaluations_seed7755.json`, `hv_trajectory_seed7755.json`, etc.

### Per-Seed Asset Naming

[t0106] used `nsga2-seed44-bedb-morph-2dir-300gen`; [t0112] used `t0112-bedb-morph-nsga2-seed77`;
[t0113] used `t0113-bedb-morph-nsga2-seed2247`. t0114's `task_description.md` lines 102-104
specifies `t0114-bedb-morph-nsga2-seed7755`, following the `t<TASK_ID>-bedb-morph-nsga2-seed<SEED>`
convention introduced by [t0112]. The predictions asset folder name MUST match `predictions_id` in
`details.json`.

### Run Orchestration

[t0113]'s `run_seed2247.sh` (48 lines) is the canonical orchestration script: Phase A (random_init
build) runs locally; Phase B imports `bootstrap` to compile the [t0080] MOD library if needed; Phase
C launches the NSGA-II driver with `--save-algorithm-config --teardown-on-watchdog`. For t0114 the
script is renamed to `run_seed7755.sh` with `SEED=7755` and the `tasks.t0113_*` module paths swapped
for `tasks.t0114_*` everywhere. The `/root/t0113_workdir` path used by the setup-machines step is
renamed to `/root/t0114_workdir`. The `--n-gen` CLI flag now defaults to 300 (matching the patched
`N_GEN`); explicit `--n-gen 300` in the launch line is recommended as a belt-and-braces.

### Smoke Gate

[t0113]'s `smoke_gate.py` (192 lines) runs five local pre-launch checks: single-eval driver run on
the 5 anchors with the t0083 best-cell electrophys vector (expected anchor-1 PD-rate ~43.6 Hz with
+/- 2 Hz tolerance), ratio DSI synthetic sanity, silence-guard pytest, pool-restart sanity (one
short 2-pop / 2-gen run with restart cadence 1 confirming the pool is recreated), watchdog wiring
(constructs a `CostWatchdog` from a synthetic `machine_log.json` and asserts the cap reads as
`T0113_HARD_BUDGET_USD = 25.00`). t0114 inherits all five with the `T0114_*` constant rename and
adds the no-HV-plateau-in-termination-list check described above.

### Pool Restart and Memory Mitigation

The `PerGenerationPoolRestart` callback (`nsga2_driver.py:338-391`) is the load-bearing memory
mitigation for long NSGA-II runs. NEURON accumulates per-worker memory; closing and recreating the
`multiprocessing.Pool` every 10 generations resets the worker pool and the freshly-swapped
`StarmapParallelization` routes subsequent evaluations through the new pool. [t0112] established
that cadence-10 produces a 3.5x per-generation speedup vs [t0106]'s cadence-25 with no algorithmic
cost. At t0114's `N_GEN = 300` ceiling this means 30 pool restarts maximum. t0114 makes no change to
this mechanism.

## Reusable Code and Assets

Per the cross-task rule, **every** non-library module from [t0113] below is **copy into task**. The
library-asset imports from [t0024] and [t0090] / [t0092] are existing full-path task imports, not
library entry-point imports, but they remain valid in t0114 without any rewrite because they point
at upstream task code.

### Copy into task — algorithm-critical, verbatim except for the package-path rewrite

* `tasks/t0113_t0106_seed2247_replicate/code/__init__.py` (0 lines) — package marker.
* `tasks/t0113_t0106_seed2247_replicate/code/bootstrap.py` (161 lines) — NEURON DLL loader;
  patches [t0024]'s `load_neuron` to load [t0080]'s MOD library. Side-effect import; do not edit.
* `tasks/t0113_t0106_seed2247_replicate/code/apply_params.py` (234 lines) — 54-d
  electrophys-to-cell write function. Signature:
  `apply_parameter_vector(*, cell: DSGCCellWithAIS, vector: NDArray) -> None`.
* `tasks/t0113_t0106_seed2247_replicate/code/build_cell_ais.py` (79 lines) — `DSGCCellWithAIS`
  dataclass.
* `tasks/t0113_t0106_seed2247_replicate/code/extend_with_ais.py` (127 lines) — AIS extender used
  by `apply_params`.
* `tasks/t0113_t0106_seed2247_replicate/code/parametric_placer.py` (105 lines) — synapse placer;
  no task-specific knobs.
* `tasks/t0113_t0106_seed2247_replicate/code/recorder.py` (122 lines) — Vm recording helper.
* `tasks/t0113_t0106_seed2247_replicate/code/trial_helpers.py` (311 lines) — `_bar_arrival_times`,
  `_rates_with_ar2_noise`, `_gaba_prob_for_direction`, `_rates_to_events`, `_count_spikes`,
  `setup_synapses_parametric`, plus `BASE_ACH_PROB`, `RATE_DT_MS`.
* `tasks/t0113_t0106_seed2247_replicate/code/generator_wrapper.py` (105 lines) — adapter around
  [t0092]'s `generate_fixed_morphology`. Signature:
  `build_cell(*, morph_params: MorphologyParams, morph_seed: int) -> MorphologyResult`.
* `tasks/t0113_t0106_seed2247_replicate/code/cost_watchdog.py` (129 lines) — Vast.ai cost
  watchdog; exports `CostWatchdog`, `load_hourly_rate_from_machine_log`,
  `make_watchdog_from_machine_log`, `patch_t99_loop_rate`. Verbatim. Only the budget constant name
  changes via `constants.py`.
* `tasks/t0113_t0106_seed2247_replicate/code/hv_plateau_watchdog.py` (89 lines) — HV-plateau
  termination + pure `should_stop` function. **Verbatim and kept importable for offline detector
  replay**, even though no longer wired into the live termination list.
* `tasks/t0113_t0106_seed2247_replicate/code/evaluator.py` (504 lines) — `BedBV3MorphProblem`,
  `evaluate_68d_vector`. Verbatim.
* `tasks/t0113_t0106_seed2247_replicate/code/constants_electrophys.py` (547 lines) — verbatim (no
  t0113-specific references inside).
* `tasks/t0113_t0106_seed2247_replicate/code/anchor_definitions.py` (149 lines),
  `anchor_classifier.py` (127 lines), `biological_priors.py` (252 lines), `biological_scorecard.py`
  (183 lines) — needed by `smoke_gate.py`. Verbatim.
* `tasks/t0113_t0106_seed2247_replicate/code/test_evaluator_dsi_guard.py` (164 lines) —
  silence-guard pytest. Copy verbatim and rerun under t0114 imports as part of smoke gate.

### Copy into task — receives a real patch

| File | Source | Patch |
| --- | --- | --- |
| `constants.py` | t0113 (118 lines) | Rename `T0113_SEEDS = (2247,)` -> `T0114_SEEDS = (7755,)` at line 63. Rename `T0113_HARD_BUDGET_USD` -> `T0114_HARD_BUDGET_USD` at line 64 (value 25.00 unchanged). Rename `T0113_PER_INSTANCE_WATCHDOG_USD` -> `T0114_PER_INSTANCE_WATCHDOG_USD` at line 65 (value 20.00 unchanged). Update backwards-compat aliases at lines 70-75 to reference `T0114_*`. Update `__all__` at lines 81-118 to swap `T0113_*` for `T0114_*`. Update assertion comments at lines 77-79. Update module docstring at lines 1-28 to reflect seed 7755, auto-stop deletion, and `N_GEN = 300`. |
| `constants_morphology.py` | t0113 (159 lines) | One-line patch at line 111: `N_GEN: int = 60` -> `N_GEN: int = 300`. Rewrite the comment at line 110 to reflect the t0114 directive. Package-path rewrite of the import block at lines 49-60 swapping `tasks.t0113_t0106_seed2247_replicate` -> `tasks.t0114_seed7755_no_autostop`. |
| `nsga2_driver.py` | t0113 (734 lines) | Remove `HVPlateauTermination(seed=task_seed)` from the `TerminationCollection` at lines 524-529 (drop one line). Prepend the comment block citing S-0113-03 and the 2026-05-20 user directive. Optionally refactor the termination construction into a `_build_termination(...)` helper so the smoke gate can introspect it. Keep `_POOL_RESTART_EVERY = 10` at line 97 verbatim. Keep the `HVPlateauTermination` import at lines 74-76 verbatim. Package-path rewrite applied. |
| `paths.py` | t0113 (218 lines) | Replace every occurrence of `t0113_t0106_seed2247_replicate` with `t0114_seed7755_no_autostop`. |
| `random_init.py` | t0113 (101 lines) | Rename `T0113_SEEDS` import to `T0114_SEEDS` at line 21. Package-path rewrite of the import block at lines 18-27. |
| `smoke_gate.py` | t0113 (192 lines) | Add new check #6: assert the live `TerminationCollection` contains no `HVPlateauTermination`. Package-path rewrite at lines 26-43. No algorithm change. |
| `run_seed2247.sh` | t0113 (48 lines) | Rename to `run_seed7755.sh`. Change `SEED=2247` to `SEED=7755`. Swap `tasks.t0113_t0106_seed2247_replicate` for `tasks.t0114_seed7755_no_autostop` everywhere. Optionally set `--n-gen 300` explicitly in the launch line. Rename the `/root/t0113_workdir` path to `/root/t0114_workdir`. |
| `sync_results_back.sh` | t0113 (36 lines) | Rename `t0113_workdir` -> `t0114_workdir`. Swap `tasks.t0113_*` -> `tasks.t0114_*` everywhere. |

### New file (not inherited from t0113)

* `tasks/t0114_seed7755_no_autostop/code/detector_replay.py` (~60 lines, **new**) — pure-Python
  replay script for the S-0113-03 offline detector sweep. Loads the four HV trajectories (t0106 seed
  44, t0112 seed 77, t0113 seed 2247, t0114 seed 7755), invokes a
  `should_stop_with_overrides(hv_history, *, window, rel_threshold, min_history)` helper for each
  (`seed`, `WINDOW`, `REL_THRESHOLD`) triple at each generation index, and writes the long-format
  `results/data/detector_replay.csv`. Uses `tasks.t0114_seed7755_no_autostop.code.paths` factories
  and inline `json.loads` for the upstream HV traces. Imports the canonical reference constants from
  `tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog`.

### Cross-task imports kept (no copy)

These are full-path imports of UPSTREAM task code, not library imports, but the verificator allows
them and the entire t0080 -> t0106 -> t0112 -> t0113 lineage uses the same pattern. They remain
unchanged in t0114:

* `tasks.t0024_port_de_rosenroll_2026_dsgc.code.constants` and `.ar2_noise.generate_ar2_batch` —
  upstream constants and AR(2) noise generator (Bed B port). Used by `trial_helpers.py` and
  `evaluator.py`. No change.
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.mods/` — the **compiled MOD library**
  (`x86_64/.libs/libnrnmech.so` on Linux, `build/nrnmech.dll` on Windows) resolved at runtime by
  `paths.py:resolve_t99_mod_library`. Linux build via `nrnivmodl` on the Vast.ai instance.
* `tasks.t0090_morphology_generator_diversity_test.code.constants` — `MorphologyParams`,
  `MorphologyResult`, `MorphometricSummary` dataclasses (14-d morphology spec) plus `PARAM_NAMES`,
  `PARAM_BOUNDS`, and `INT_PARAM_NAMES`.
* `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix` and
  `baseline_channels.insert_baseline_channels` — patched generator (canonical via [t0093]
  correction C-0093-01).

### Read-only input HV trajectories for offline replay (no copy; absolute paths)

* `tasks/t0106_long_pdnd_nsga2_300gen/results/data/hv_trajectory_seed44.json` — 40 generations.
* `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json` — 21 generations.
* `tasks/t0113_t0106_seed2247_replicate/results/data/hv_trajectory_seed2247.json` — 14
  generations.

These three files are read directly by the offline detector replay; they are **not** copied into
t0114, they are referenced by absolute path through `paths.py` constants. No verificator rule
forbids reading upstream `results/data/` files; the rule against modifying files outside the task
folder is preserved because the replay only reads.

### Library imports via registered entry points — none

No library is imported via its registered entry point. The cross-task imports above use the raw
`code/` module paths, identical to the t0078 -> t0106 -> t0112 -> t0113 lineage convention. This is
intentional and unchanged from [t0113].

### Analysis modules to port on demand (analysis stage)

The [t0113]-specific analysis modules below operate on three seeds (44, 77, 2247). For t0114's
four-seed analysis they need adapter changes; defer to the analysis stage:

* `tasks/t0113_t0106_seed2247_replicate/code/build_t0113_results.py` (868 lines) — produces the 5
  task-specified charts and the joint-pass-summary CSV for the 3-seed comparison. Adapt to read four
  sources (t0106 seed 44, t0112 seed 77, t0113 seed 2247, t0114 seed 7755) and emit `*_4seeds.png`
  plus `joint_pass_summary_4seeds.csv` / `pareto_front_overlap_4seeds.csv` per `task_description.md`
  lines 149-156.
* `tasks/t0113_t0106_seed2247_replicate/code/cross_seed_analysis.py` (317 lines) — generic
  cross-seed framework; needed for the 5 task charts.
* `tasks/t0113_t0106_seed2247_replicate/code/build_morphology_charts.py` (328 lines) — needed for
  `top50_morphologies_seed7755.png` (chart 5 of 5 in the task brief).
* `tasks/t0113_t0106_seed2247_replicate/code/build_predictions_assets.py` (528 lines) — writes the
  `details.json` and the gzipped evaluations file. Adapt the predictions ID and metrics to t0114
  values; add the new `stop_trigger` field to `metrics_at_creation`.
* `tasks/t0113_t0106_seed2247_replicate/code/make_charts.py` (345 lines) — chart orchestrator;
  ports with the package-path rewrite.
* `tasks/t0113_t0106_seed2247_replicate/code/metrics_builder.py` (81 lines) — builds
  `results/metrics.json` from the per-seed JSON outputs.
* `tasks/t0113_t0106_seed2247_replicate/code/per_seed_analysis.py` (99 lines),
  `run_local_analysis.py` (35 lines) — convenience runners.
* `tasks/t0113_t0106_seed2247_replicate/code/build_t0112_results.py` (303 lines),
  `build_t0106_plots.py` (395 lines), `build_analysis_charts.py` (431 lines), `build_assets.py` (659
  lines) — historical builders kept for cross-task plot generation if needed during the analysis
  stage; ports with the package-path rewrite.

## Lessons Learned

### Cadence-10 Pool Restart Is Robust at Long Run Lengths

[t0112] and [t0113] confirmed the cadence-10 pool restart produces a 3.5x per-generation speedup vs
[t0106]'s cadence-25 with no algorithmic cost to Pareto-front geometry. At [t0113]'s observed 160
s/gen on the 64-core EPYC 7B13, a full 300-gen t0114 run consumes ~13.3 wall-clock hours; the cap
budget supports this comfortably. The cadence-10 is also untested at run lengths beyond [t0106]'s
40-gen extent. t0114 will be the first task in this lineage to exercise cadence-10 across up to 300
generations; the cadence-10 wall-clock confirmation is question 7 in the task brief.

### HV-Plateau Detector Has Censored All Three Existing Seeds

[t0106] auto-stopped at gen 40, [t0112] at gen 21, [t0113] at gen 14. None of the three runs were
allowed to discover further HV growth past the detector trigger. [t0113]'s post-mortem (the gen
13-14 jump of +26% from a single silence-guard cell joining the archive, with the soft gen 11-12
transition satisfying the rule the gen BEFORE the jump) is the direct motivation for S-0113-03 and
for t0114. The offline detector replay will quantify how much HV growth was censored across all
three seeds. The expected pattern (per [t0113]'s `results_detailed.md` "Limitations" section): all
three seeds plateau much later than their detector trigger, with t0113 likely showing the largest
post-trigger HV delta because of its sparse joint-pass bucket.

### Silence-Guard Cells Dominate the t0113 Joint-Pass Count

[t0113] reported **0 LEGIT joint-pass cells**; the 2 asset-declared joint-pass cells were both
silence-guard DSI=1.0 saturations (1 PD spike / 0 ND spikes). The silence-guard threshold
`SILENCE_SPIKE_COUNT_THRESHOLD = 10` is too permissive at sparse seeds; suggestion S-0113-06
proposes tightening it. t0114 inherits the threshold unchanged (the task brief forbids any change to
the silence guard) but may surface more silence-guard cells if seed 7755 lands in a sparse basin.
The substrate-rate question (task question 4) must distinguish LEGIT joint-pass cells from
silence-guard saturations when reporting the 4-seed mean.

### t0113 Pareto Front Is Closer Neither to Seed 44 Nor Seed 77

[t0113] found its 8 strict Pareto cells were roughly equidistant from both t0106 and t0112 Pareto
cells in z-scored 68-d parameter space (mean nearest-neighbour distance ~10.7 to either target).
This is informative for t0114: if seed 7755 lands in a third roughly-equidistant basin, the
substrate is multi-modal in parameter space and the cross-seed Pareto overlap is governed by
basin-of-attraction stochastics rather than any structural property of the seed. The t0114 analysis
should re-run the same 4-seed pairwise nearest-neighbour distance calculation in
`pareto_front_overlap_4seeds.csv`.

### Cost Headroom Is Comfortable At 13-Hour Run Length

[t0113] spent $0.4773 of $25 at 14 generations (160 s/gen). [t0106] spent $10.37 at 40 generations
(2,167 s/gen, cadence-25). t0114 at 300 generations / 160 s/gen on a similar EPYC 7B13 spends ~$5-6
productive compute; the $25 cap is comfortable. The wider $25 cap was already raised vs the $4
default [t0104] level (the $25 was inherited from [t0112]); no further envelope check is needed
beyond confirming the project total budget covers $25 before provisioning.

### Dill Checkpoint Resume Channel Is Broken; JSON Resume Is the Working Path

[t0113] (suggestion S-0113-02) flagged that dill-pickling the pymoo Algorithm fails on every
generation because `pymoo.parallelization.starmap.StarmapParallelization` holds a live
`multiprocessing.Pool` reference. The JSON-side resume path (`hv_trajectory_seed7755.json`,
`all_evaluations_seed7755.json`, `nsga2_checkpoint_seed7755.json`) is fully functional. t0114
inherits this state: dill checkpoints will fail silently every gen and the JSON channel is the
operative resume mechanism. This is non-fatal for the t0114 run but means a mid-run instance
interruption requires JSON-side restart, not dill-restart. S-0113-02 captures the fix.

### Reporting the 8-Direction Polar Caveat Belongs in the Reporting Stage

[t0107] established that 2-direction ratio DSI overstates conventional 8-direction vector-sum DSI by
~0.42 absolute on [t0106] high-DSI cells. The t0114 task brief forbids any change to the evaluator
(no 8-direction re-evaluation in t0114). The reporting stage must include the same caveat language
[t0113] used: "DSI values reported are 2-direction ratio DSI; conventional 8-direction vector-sum
DSI is expected ~0.42 lower in absolute value per t0107." A follow-up suggestion mirroring S-0113-04
should be cloned for t0114's joint-pass cells if any are non-silence-guard.

## Recommendations for This Task

1. **Fork the [t0113] `code/` directory verbatim** into `tasks/t0114_seed7755_no_autostop/code/`,
   using a single copy + global package-path rewrite (`tasks.t0113_t0106_seed2247_replicate` ->
   `tasks.t0114_seed7755_no_autostop`) across all `.py` and `.sh` files. Do not edit any algorithm
   logic beyond the three patches below.

2. **Apply the three text-level patches**:
   * `constants.py` line 63: `T0113_SEEDS = (2247,)` -> `T0114_SEEDS = (7755,)`; rename the
     companion budget constants at lines 64-65 (`T0113_HARD_BUDGET_USD` -> `T0114_HARD_BUDGET_USD`,
     `T0113_PER_INSTANCE_WATCHDOG_USD` -> `T0114_PER_INSTANCE_WATCHDOG_USD`, values unchanged);
     update aliases at lines 70-75 and `__all__` at lines 81-118; rewrite the module docstring at
     lines 1-28.
   * `constants_morphology.py` line 111: `N_GEN: int = 60` -> `N_GEN: int = 300`; rewrite the
     comment at line 110.
   * `nsga2_driver.py` lines 524-529: remove `HVPlateauTermination(seed=task_seed)` from the
     `TerminationCollection`; keep all three other terminations in the same order; prepend a comment
     block citing S-0113-03 and the 2026-05-20 user directive.

3. **Keep `HVPlateauTermination` importable from
   `tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog`** even though it is no longer wired
   into the live termination list. The class and the pure `should_stop` function are both required
   by the offline detector replay; the existing import at `nsga2_driver.py` lines 74-76 stays so the
   smoke gate's "no HV-plateau in termination list" check can introspect it.

4. **Keep `_POOL_RESTART_EVERY = 10` at `nsga2_driver.py:97` verbatim**. The cadence-10 protocol is
   load-bearing for the up-to-300-gen wall-clock. Do not edit this constant under any circumstances;
   t0114 is the first task in the lineage to exercise cadence-10 across 300 generations and the
   per-gen wall-clock confirmation is task question 7.

5. **Add the sixth smoke-gate check**: the live `TerminationCollection` must contain no
   `HVPlateauTermination`. Refactor the inline construction at `nsga2_driver.py:524-529` into a
   `_build_termination(*, n_max_gen, cost_watchdog, seed, stop_path)` helper so the smoke gate can
   instantiate it without launching a real run; iterate `coll.terminations` asserting
   `not any(isinstance(t, HVPlateauTermination) for t in coll.terminations)`.

6. **Write a new `detector_replay.py` (~60 lines)** in `tasks/t0114_seed7755_no_autostop/code/`
   implementing the S-0113-03 offline detector sweep. It must (a) load the four HV trajectories from
   `tasks/t0106_long_pdnd_nsga2_300gen/results/data/hv_trajectory_seed44.json`,
   `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json`,
   `tasks/t0113_t0106_seed2247_replicate/results/data/hv_trajectory_seed2247.json`, and t0114's own
   `results/data/hv_trajectory_seed7755.json`; (b) invoke a
   `should_stop_with_overrides(hv_history, *, window, rel_threshold, min_history)` helper for each
   `(seed, WINDOW, REL_THRESHOLD)` triple at each generation index; (c) write the long-format
   `results/data/detector_replay.csv` (32 rows: 4 seeds x 4 windows x 2 thresholds); (d) pick
   `(W*, T*)` such that `gen_at_fire >= 20` on every seed and `gen_at_fire <= 60` on t0106. Read the
   canonical reference constants from `tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog`.

7. **Verify the predictions asset schema matches [t0113] exactly, plus the `stop_trigger`
   extension**. The asset folder must be named `t0114-bedb-morph-nsga2-seed7755` (per
   `task_description.md` lines 102-104); `details.json` must list `spec_version: "2"`; the
   `prediction_schema` string must declare the same five per-cell fields (`generation`,
   `vector_68d`, `objective_F_minimised`, `dsi_vector_sum`, `pd_rate_hz`). Keep the `dsi_vector_sum`
   field name even though it stores ratio DSI. Add `stop_trigger` to `metrics_at_creation` with
   value in `{operator_stop, budget_cap, gen_ceiling, instance_watchdog}`.

8. **Wire the cost watchdog explicitly with `T0114_HARD_BUDGET_USD = 25.00`** at the
   `make_watchdog_from_machine_log(...)` call site in `nsga2_driver.py:487-491`. Do not rely on the
   legacy `T0104_HARD_BUDGET_USD = 4.00` default that lives in `cost_watchdog.py:27`.

9. **Do not import any registered library entry point**. The lineage convention is full-path task
   imports of upstream `code/` modules; t0114 preserves this exactly. Keep the upstream imports of
   t0024, t0080, t0090, t0092 unchanged.

10. **Defer analysis modules** (`build_t0113_results.py`, `cross_seed_analysis.py`,
    `build_morphology_charts.py`, `build_predictions_assets.py`, `make_charts.py`,
    `metrics_builder.py`, `per_seed_analysis.py`, `run_local_analysis.py`, plus the historical
    builders) to the analysis stage. The implementation stage only needs the driver, the random-init
    builder, the predictions asset writer, the smoke gate, and the detector replay script. The 5
    task-specified charts and 3 CSVs require adapter changes to read four seed sources instead of
    three.

11. **Single-seed orchestration**: rename `run_seed2247.sh` to `run_seed7755.sh`, set `SEED=7755`,
    optionally pass `--n-gen 300` explicitly, and swap `tasks.t0113_t0106_seed2247_replicate` for
    `tasks.t0114_seed7755_no_autostop` everywhere. Rename `/root/t0113_workdir` ->
    `/root/t0114_workdir`. Pass `--teardown-on-watchdog` as the [t0113] script does.

12. **Note the random-seed provenance and the auto-stop deletion in the predictions asset
    `model_description`**. The asset description should mention that GA seed 7755 was drawn via
    `secrets.randbelow(10000)` to avoid selection bias and that HV-plateau auto-stop was disabled
    per S-0113-03 + 2026-05-20 user directive — both facts are essential for downstream
    reproducibility.

13. **Plan for the offline detector replay to run BEFORE the t0114 live run lands**. The replay over
    the existing three traces (44, 77, 2247) is fully implementable without the t0114 trajectory; it
    produces a partial CSV (24 rows: 3 seeds x 8 cells) that the analysis stage extends to 32 rows
    once the t0114 trace is available. This decouples the S-0113-03 reparameter analysis from the
    Vast.ai launch schedule and surfaces any replay bugs early.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Upstream Bed B substrate definition. t0114's `evaluator.py` and `trial_helpers.py`
  import `tasks.t0024_*.code.constants` and `ar2_noise.generate_ar2_batch` directly. No change vs
  [t0113].

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Owns the canonical Linux MOD library (13 `.mod` files compiled under
  `mods/x86_64/`) resolved at runtime by t0114 (via [t0106] / [t0112] / [t0113])
  `paths.py:resolve_t99_mod_library`. The package-path rewrite does NOT change this dependency.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Morphology generator diversity test
* **Status**: completed
* **Relevance**: Defines the `MorphologyParams`, `MorphologyResult`, `MorphometricSummary`
  dataclasses imported by t0114 `evaluator.py` (via [t0113]'s copy). The library
  `procedural_dsgc_morphology_generator` is registered here but t0114 uses the [t0092]-patched
  generator per correction C-0093-01.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology generator silence
* **Status**: completed
* **Relevance**: Owns the patched `morphology_generator_fix` and `baseline_channels` modules
  imported by t0114 `generator_wrapper.py`. The patched generator is canonical via [t0093]
  correction C-0093-01.

### [t0093]

* **Task ID**: `t0093_resweep_and_t0090_correction`
* **Name**: Patched-generator full 60-morph re-sweep + t0090 correction overlay
* **Status**: completed
* **Relevance**: Issued correction C-0093-01 marking [t0090]'s generator as superseded by [t0092]'s
  patched generator. t0114 (via [t0106] -> [t0112] -> [t0113]) imports [t0092]'s patched generator
  per this correction.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init
* **Status**: completed
* **Relevance**: Distant ancestor of t0114; established the pop=96 N_EVAL_SEEDS=4 gens=20 NSGA-II
  template and the `dsi_vector_sum` field name convention t0114 still uses. The silence guard
  (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`) originates here.

### [t0104]

* **Task ID**: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* **Name**: 68-d 2-objective (DSI + PD-rate) NSGA-II at GA seeds=3, N=4, gens=20
* **Status**: completed
* **Relevance**: Drop-robustness-objective predecessor of [t0106]; established the 2-objective HV
  reference point `[0.0, 0.0]` and the `TerminationCollection` pattern (MaxGen + HVPlateau +
  CostWatchdog) that t0114 modifies by dropping the HV-plateau entry.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long 2-direction NSGA-II at 300 gens, 1 seed, 3 trials (ratio DSI + PD-rate)
* **Status**: completed
* **Relevance**: Grandparent dependency of t0114. Established the 2-direction ratio DSI protocol,
  the 68-d substrate, the predictions asset schema (`spec_version: "2"`), the original `N_GEN = 300`
  ceiling t0114 restores, and the seed-44 baseline run (123 unique joint-pass cells, best ratio DSI
  = 1.0000, best PD-rate = 122.62 Hz, final HV = 122.0288, cost $10.37) that t0114 is compared
  against. Source of the `tasks/t0106_long_pdnd_nsga2_300gen/results/data/hv_trajectory_seed44.json`
  HV trace consumed by the offline detector replay.

### [t0107]

* **Task ID**: `t0107_t0106_polar_8dir_recheck`
* **Name**: 8-direction polar re-evaluation of 10 random top-50 t0106 cells
* **Status**: completed
* **Relevance**: Out-of-scope caveat task. Shows [t0106]'s 2-direction ratio DSI overstates
  selectivity by ~0.42 absolute under conventional 8-direction vector-sum protocol. Relevant only
  for the t0114 reporting stage, not for the experiment-run step. Drives the t0114-cloned follow-up
  suggestion mirroring S-0113-04.

### [t0112]

* **Task ID**: `t0112_t0106_seed77_replicate`
* **Name**: Seed-77 minimum-change replicate of t0106 long 2-direction NSGA-II
* **Status**: completed
* **Relevance**: Parent-of-parent of t0114. Introduced the cadence-10 `_POOL_RESTART_EVERY` setting
  inherited unchanged. Source of the
  `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json` HV trace consumed by
  the offline detector replay. Seed-77 baseline run (7 unique joint-pass cells, best ratio DSI =
  0.9535, best PD-rate = 114.76 Hz, final HV = 107.4602, cost $1.99). Source of suggestion S-0112-03
  (re-run with auto-stop disabled) which t0114 partially realises.

### [t0113]

* **Task ID**: `t0113_t0106_seed2247_replicate`
* **Name**: Seed-2247 random-seed replicate of t0106 long 2-direction NSGA-II
* **Status**: completed
* **Relevance**: **Direct fork base and dependency of t0114.** Provides the entire code tree to copy
  (36 files, 9,383 lines), the predictions asset schema to mirror (plus the `stop_trigger`
  extension), the cadence-10 `_POOL_RESTART_EVERY` setting to inherit, the smoke-gate harness to
  extend with the no-HV-plateau check, the orchestration script template (`run_seed2247.sh` ->
  `run_seed7755.sh`), the analysis modules to port on demand, and the seed-2247 baseline run (0
  LEGIT joint-pass cells, 2 silence-guard DSI=1.0 cells, best legit ratio DSI = 0.3651, best PD-rate
  = 71.67 Hz, HV-plateau auto-stop at gen 14, cost $0.4773) that t0114 is compared against alongside
  [t0106] and [t0112]. Source of suggestion S-0113-03 (HV-plateau detector window widening) — the
  direct motivation for t0114. Source of the
  `tasks/t0113_t0106_seed2247_replicate/results/data/hv_trajectory_seed2247.json` HV trace consumed
  by the offline detector replay.
