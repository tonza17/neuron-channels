---
spec_version: "1"
task_id: "t0102_seedscale_n4_gen20"
research_stage: "code"
tasks_reviewed: 10
tasks_cited: 10
libraries_found: 2
libraries_relevant: 2
date_completed: "2026-05-11"
status: "complete"
---
# Research Code — Reusing t0099 Substrate for the N_SEEDS=4 / gens=20 Re-Balance

## Task Objective

t0102 reuses the 68-d random-init NSGA-II substrate from t0099 with two parameters changed
(N_EVAL_SEEDS 5 -> 4, n_gen 8 -> 20) and two new GA seeds (44, 55) instead of t0099's (11, 22, 33),
to test whether a Poleg-Polsky-style seed/generation profile recovers a strict joint-pass cell (DSI
>= 0.5, PD-rate >= 30 Hz, robustness >= 0.7) without a warm-start. This code research audits the
substrate code from t0024 (Bed B DSGC), t0080 (49/54-d MOBO origin), t0083 (NSGA-II extension),
t0086 (clustering/scorecard), t0090/t0092/t0093 (morphology generator + soma-pt3d fix), t0091 (first
68-d joint NSGA-II) and t0099 (the immediate substrate) to determine exactly what to copy into
t0102/code/ and how to override the noise-replicate constant without modifying any prior task.

## Library Landscape

Two registered library assets are directly relevant; both are reached transitively via t0099's
imports.

* `de_rosenroll_2026_dsgc` — Created by t0024 [t0024]. v0.1.0. NEURON HOC template, vendored
  `nrnmech.dll` (Windows) / `libnrnmech.so` (Linux), and Python driver for the Bed B compartmental
  model. Entry points: `build_dsgc_cell`, `run_tuning_curve`, `score_envelope`. Module paths under
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/`. Relevant because the t0099 substrate (and
  therefore t0102) loads its compiled MOD library via t0099's `bootstrap.py` (Linux monkey-patching)
  and reuses `_ensure_neuron_on_path`. The aggregator output does NOT show any correction overlay on
  this library.
* `procedural_dsgc_morphology_generator` — Created by t0090 [t0090]. v0.1.0. `MorphologyParams`,
  `MorphologyResult`, `generate_morphology`, `MorphometricSummary`, `BEDB_BASE_POINT`,
  `PARAM_BOUNDS`, `INT_PARAM_NAMES`. **Replaced** by C-0093-01 with
  `procedural_dsgc_morphology_generator_fix` (t0092 [t0092]) which provides
  `generate_fixed_morphology` + `insert_baseline_channels`. The fix patches the soma-pt3d collapse
  bug that caused NaN voltages under the t0083 best-cell parameter set. The aggregator exposes the
  *effective* corrected state — any library lookup for `procedural_dsgc_morphology_generator`
  resolves to the t0092 fix. t0099's `generator_wrapper.py` already imports from
  `tasks.t0092_*.code.morphology_generator_fix` (canonical per C-0093-01).

No other library assets in the project are relevant to t0102. The library aggregator
(`aggregate_libraries.py`) is not present in this repo's `arf/scripts/aggregators/` (only
categories, costs, machines, metric_results, metrics, suggestions, task_types, tasks); library
metadata was read directly from each task's `assets/library/<id>/details.json`.

## Architecture Overview

The t0099 substrate is a stack of cooperating modules. The dependency graph relevant to t0102 is:

```text
t0102/code/  ->  copies of t0099/code/{nsga2_driver, evaluator, generator_wrapper, ...}
                         |
                         +--> tasks.t0090_*.code.morphology_params   (library import)
                         +--> tasks.t0092_*.code.morphology_generator_fix  (library import)
                         +--> tasks.t0092_*.code.baseline_channels   (library import)
                         +--> tasks.t0024_*.code.build_cell          (library import)
```

The 68-d vector is `[54 electrophys | 14 morphology]`. Per-cell evaluation: worker subprocess caches
one cell keyed on the 14-d morphology hash; on electrophys-only change the cell is reused and only
`apply_parameter_vector` re-runs. NSGA-II uses `pymoo` with `StarmapParallelization` fanning out to
a `multiprocessing.Pool(processes=min(60, cpu_count()-4))`. Each generation produces `pop_size`
evaluations, each evaluation runs `N_EVAL_SEEDS x n_directions` trials.

## Key Findings

### Substrate origin is t0099/code/nsga2_driver.py, not run_loop.py

The t0102 task description and `step_tracker.json` step 6 both reference
`tasks/t0099_random_init_pareto_robustness/code/run_loop.py` as "THE substrate to reuse" — that
file does not exist in t0099 [t0099]. The actual NSGA-II entry point is
`tasks/t0099_random_init_pareto_robustness/code/nsga2_driver.py` (369 lines) with
`tasks/t0099_random_init_pareto_robustness/code/run_three_seeds.sh` as the shell orchestrator
sequentially driving seeds 11/22/33. The Python function `run_nsga2_for_seed(*, task_seed: int)`
takes one integer seed, loads `init_pop_seed{S}.json`, builds the `BedBV3MorphProblem`, and calls
pymoo's `minimize(problem, algorithm, termination, seed=task_seed, ...)`. t0102 must point its
driver at `nsga2_driver.py` (renamed/copied) and at its own analog of `run_three_seeds.sh` that
iterates `(44, 55)` instead.

### The "N_SEEDS" override target is actually `N_EVAL_SEEDS`, defined in t0099 not t0080

The task description says "import-shadow the value from t0080's `constants.py`" — this conflates
two separately named constants. `tasks/t0080_*/code/constants.py:43` defines `N_SEEDS: int = 20`
[t0080]. But the t0099 substrate does **not** import `N_SEEDS` from t0080 at all; t0099's own
`tasks/t0099_random_init_pareto_robustness/code/constants_morphology.py:114` defines
`N_EVAL_SEEDS: int = 5` and the evaluator imports that. There is a stale `N_SEEDS: int = 20` in
`tasks/t0099_random_init_pareto_robustness/code/constants_electrophys.py:43` but `grep -rn` shows it
is never imported anywhere in t0099's code/ tree — it was carried over from a copy-paste of
t0080's constants and is dead.

So the **operative noise-replicate constant in the t0099 substrate is `N_EVAL_SEEDS` in
constants_morphology.py, value 5**, not `N_SEEDS` in t0080's constants.py, value 20. t0102's
override must set `N_EVAL_SEEDS = 4` in its local copy of `constants_morphology.py`. The plan
documentation should correct the "import-shadow N_SEEDS from t0080" language to "override
`N_EVAL_SEEDS` in the local copy of `constants_morphology.py`".

### Cross-task code imports go through library asset module_paths, not raw task code

The Glite ARF Cross-Task Code Reuse Rule forbids importing from other tasks' `code/` directories
except via libraries [t0090] [t0092]. t0099's `generator_wrapper.py` imports four symbols from
`tasks.t0090_*.code.morphology_params` and `tasks.t0092_*.code.morphology_generator_fix` /
`baseline_channels` — these are allowed because t0090 and t0092 register those modules as library
asset `module_paths` (see each library's `details.json:module_paths`). t0099's `bootstrap.py`
imports `tasks.t0024_*.code.build_cell` / `constants` / `paths` — also allowed because t0024
registers those modules under `de_rosenroll_2026_dsgc` library. All other t0099 modules
(`evaluator`, `nsga2_driver`, `random_init`, `smoke_gate`, `cost_watchdog`, etc.) are task-internal
and **must be copied** into t0102's code/, not imported from `tasks.t0099_*.code.*`.

### t0099 itself copied (did not import) t0080's electrophys constants

t0099 contains its own `constants_electrophys.py` (547 lines) [t0099] which is the t0080 54-d
parameter layout copied verbatim with light edits (the dead `N_SEEDS = 20` line is the giveaway).
This sets the precedent: t0102 should do the same — copy `constants_electrophys.py` and
`constants_morphology.py` from t0099 into `tasks/t0102_*/code/` and edit only `N_EVAL_SEEDS` and the
seed/budget tuple.

### NSGA-II hyperparameters and HV reference are fixed across t0080/t0091/t0099

`POP_SIZE = 96`, `SBX_ETA = 15`, `SBX_PROB = 0.9`, `PM_ETA = 20`, `PM_PROB = 1/68` are stable across
t0080 [t0080], t0091 [t0091], and t0099 [t0099]. `N_GEN` shifted: t0080 set 40, t0091 set 8, t0099
set 8 (constants_morphology.py:99). t0102 must override `N_GEN = 20`. The HV reference point
`(0.0, 0.0, 0.0)` and utopia `(0.7, 0.7, 80.0, 1.0)` are also stable; copy unchanged. The HV plateau
watchdog (`hv_plateau_watchdog.py`, 89 lines) and the `CostWatchdogTermination` /
`HVPlateauTermination` / `MaximumGenerationTermination` collection from t0099/nsga2_driver.py should
be copied unchanged — they are budget-protective for any seed/gen combo.

### Per-seed cost cap must be raised from $1 to $4 to admit the larger gen count

`tasks/t0099_random_init_pareto_robustness/code/constants.py:49` sets
`T0099_HARD_BUDGET_PER_SEED_USD: float = 5.00` (the inline comment says $1.00 but the assigned value
is 5.0; the assert `<= T0099_TASK_BUDGET_TOTAL_USD = 20.00` passes). t0102 has a total $8 cap and
runs 2 seeds, so the per-seed cap is at most $4.00 (and realistically $3.50 to leave headroom for
plot+answer cost). The `cost_watchdog.py` (127 lines) machinery is the t0083-fixed version that
reads `selected_offer.price_per_hour` from `machine_log.json` (it does NOT use a hard-coded
$0.2382/hr like t0080's original) and is the correct version to copy.

### t0099's morphology smoke gate exists but expects t0093 fingerprint files

`tasks/t0099_random_init_pareto_robustness/code/smoke_gate.py` (184 lines) [t0099] loads the t0093
[t0093] post-fix verification fingerprint (`T0093_POST_FIX_VERIFICATION_SUMMARY_JSON`) and the t0083
best-cell electrophys vector (`T0083_PARETO_FRONT_JSON`) to verify the substrate is consistent. It
then re-evaluates 5 anchor morphologies and checks anchor 1 (bedb_like) is within 1.0 Hz of the
expected 43.6 Hz PD-rate. t0102 should reuse this gate but at `N_EVAL_SEEDS=4` **with widened
tolerance**: the smoke seeds in `smoke_gate.py:82` are 3 hard-coded values (`[42, 4242, 424242]`),
not `N_EVAL_SEEDS`, so the smoke itself is unaffected by lowering `N_EVAL_SEEDS`. The widened
tolerance applies only to any auxiliary REQ-7-style anchor-stability gate that re-runs
`BedBV3MorphProblem` at `N_EVAL_SEEDS=4` and compares against t0099's N=5 fingerprint.

### Anchor classification + biological scorecard are re-usable per-seed analysis pipeline

t0099 ships a 4-stage post-processing pipeline [t0099]: (1) `per_seed_analysis.py` (100 lines)
classifies each Pareto cell to its nearest of the 5 anchors and counts strict joint-pass; (2)
`anchor_classifier.py` (127 lines) does the actual nearest-anchor assignment via
`anchor_definitions.py` / `get_anchors()`; (3) `biological_priors.py` (252 lines) +
`biological_scorecard.py` (183 lines) score each cell against 13 biological priors; (4)
`cross_seed_analysis.py` (317 lines) produces the `cross_seed_summary.json` and the 3 plots (HV
trajectory, anchor heatmap, Pareto overlay). All of this should be copied into t0102 with the
input-path constants (`T0099_SEEDS`) replaced by `(44, 55)` and the cross-seed comparison extended
to include the t0099 outputs as a third reference column (alongside t0091).

### Clustering pipeline from t0086 reads t0080 LOWER/UPPER bounds for normalisation

t0086 [t0086] runs k-means k=2..6 + hierarchical clustering with silhouette/BIC + bootstrap ARI
stability on Genuine cells in 54-d parameter space (`cluster_analysis.py`, 359 lines). It normalises
by `LOWER_BOUNDS` / `UPPER_BOUNDS` imported from `tasks.t0080_*.code.constants` — these are the
54-d electrophys bounds. Reusing this for t0102 analysis (where the input is 68-d) requires either
(a) clustering only on the 54-d slice using t0102's local copy of `constants_electrophys.py`
LOWER/UPPER bounds (preferred), or (b) extending the bounds vector to 68 dims via the t0099
`constants_morphology.LOWER_BOUNDS_68`. The t0086 thresholds (`DSI_THRESHOLD = 0.4`,
`PD_THRESHOLD_HZ = 10.0`, `GENUINE_REQUIRED = 5`, `N_REPS = 5`) are LOWER than the t0099/t0091
strict joint-pass thresholds (0.5 / 30 / 0.7); t0102 should keep both ladders distinct: "loose"
t0086 Genuine and "strict" t0091/t0099 joint-pass.

### Bootstrap import side-effect is mandatory for Linux runs

`tasks/t0099_random_init_pareto_robustness/code/bootstrap.py` (161 lines) [t0099] runs
`bootstrap_neuron()` as an import-time side effect (last line) to patch t0024's `load_neuron` and
`_ensure_neuron_on_path` for the Linux Vast.ai environment. t0099's `evaluator.py:33` imports it
with `# noqa: F401` to force the side effect. **t0102 must preserve this pattern**: the copied
`bootstrap.py` must be imported at the top of the copied `evaluator.py` even though the symbol is
unused. Missing this import causes NEURON to fail to find the Linux MOD library.

### Joint-pass corner is empirically empty without warm-start at N=5 / gens<=8

The t0099 [t0099] null result is the experimental motivation for t0102: 3 random-init seeds at
N_EVAL_SEEDS=5, n_gen 5-8, pop=96 produced **0 strict joint-pass cells across 55 Pareto cells**,
versus 1 such cell in t0091's 57-cell warm-start Pareto. Seed 22 reached DSI=0.49 (just below the
0.5 threshold) but only PD=18.7 Hz (well below 30 Hz). The high-PD-rate dimension is the
load-bearing axis the warm-start enabled. t0102's research question is whether replacing "N=5,
gens=5-8" with "N=4, gens=20" at the same total eval budget recovers PD-rate.

## Reusable Code and Assets

### Substrate copy targets (copy into task)

The following t0099 files must be copied verbatim into `tasks/t0102_seedscale_n4_gen20/code/`, with
edits only in `constants.py`, `constants_morphology.py`, `paths.py`, and the orchestrator shell
script:

* `tasks/t0099_random_init_pareto_robustness/code/nsga2_driver.py` (369 lines) — copy into task.
  Edit the `_eval_seeds()` SeedSequence seed if desired (keep 42 for parity); change all `T0099_*`
  constant references to `T0102_*` after renaming in constants.py. Public function
  `run_nsga2_for_seed(*, task_seed: int) -> dict[str, object]`.
* `tasks/t0099_random_init_pareto_robustness/code/evaluator.py` (481 lines) — copy into task.
  Imports `N_EVAL_SEEDS` from `constants_morphology.py` (line 56); no edits required because the
  override flows through the copied constants file. Public function
  `evaluate_68d_vector(*, vector_68d: NDArray[np.float64], eval_seeds: list[int] | None = None, n_directions: int = N_DIRECTIONS) -> CellEvalResult`
  and class `BedBV3MorphProblem`.
* `tasks/t0099_random_init_pareto_robustness/code/generator_wrapper.py` (106 lines) — copy into
  task. No edits needed — already imports the library-asset modules from t0090/t0092. Public
  functions `build_cell(*, h, morph_params) -> MorphologyResult`,
  `morphology_params_from_vector(*, morph_vector_14d) -> MorphologyParams`,
  `split_68d_vector(*, vector_68d) -> tuple[NDArray, NDArray]`,
  `hash_morphology_vector(*, vector) -> int`.
* `tasks/t0099_random_init_pareto_robustness/code/bootstrap.py` (161 lines) — copy into task. No
  edits — Linux .so resolution paths are repo-relative.
* `tasks/t0099_random_init_pareto_robustness/code/random_init.py` (102 lines) — copy into task.
  Edit `main()` to iterate `T0102_SEEDS = (44, 55)` instead of `T0099_SEEDS`. Public function
  `build_random_init_population(*, seed: int) -> NDArray[np.float64]`.
* `tasks/t0099_random_init_pareto_robustness/code/constants_electrophys.py` (547 lines) — copy
  into task verbatim (this file itself is already a copy of t0080's constants.py).
* `tasks/t0099_random_init_pareto_robustness/code/constants_morphology.py` (145 lines) — copy into
  task with one edit: change `N_EVAL_SEEDS: int = 5` to `N_EVAL_SEEDS: int = 4`, and change
  `N_GEN: int = 8` to `N_GEN: int = 20`. This is the entire "N_SEEDS override" mechanism.
* `tasks/t0099_random_init_pareto_robustness/code/constants.py` (89 lines) — copy into task,
  rename `T0099_*` to `T0102_*`, set `T0102_SEEDS: tuple[int, ...] = (44, 55)`, set
  `T0102_HARD_BUDGET_PER_SEED_USD: float = 4.00`, set `T0102_TASK_BUDGET_TOTAL_USD: float = 8.00`.
* `tasks/t0099_random_init_pareto_robustness/code/paths.py` (166 lines) — copy into task, edit
  `TASK_ROOT` (auto via `__file__`), keep upstream references `T0091_*_JSON` paths read-only, add
  new `T0099_*_JSON` paths pointing at t0099's results data for the cross-seed comparison.
* `tasks/t0099_random_init_pareto_robustness/code/cost_watchdog.py` (127 lines) — copy into task.
  No edits required; the per-seed budget is read from `T0102_HARD_BUDGET_PER_SEED_USD` via the
  calling driver.
* `tasks/t0099_random_init_pareto_robustness/code/hv_plateau_watchdog.py` (89 lines) — copy
  unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/trial_helpers.py` (311 lines) — copy unchanged.
  Public functions `setup_synapses_parametric`, `_bar_arrival_times`, `_rates_with_ar2_noise`,
  `_rates_to_events`, `_count_spikes`, `_gaba_prob_for_direction` and constants `BASE_ACH_PROB`,
  `RATE_DT_MS`.
* `tasks/t0099_random_init_pareto_robustness/code/apply_params.py` (234 lines) — copy unchanged.
  Public function `apply_parameter_vector(*, cell, params)`.
* `tasks/t0099_random_init_pareto_robustness/code/parametric_placer.py` (105 lines) — copy
  unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/build_cell_ais.py` (79 lines) — copy unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/extend_with_ais.py` (127 lines) — copy
  unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/recorder.py` (122 lines) — copy unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/smoke_gate.py` (184 lines) — copy with the REQ-7
  widened-tolerance variant: keep the 3 hard-coded smoke seeds; document the wider acceptance window
  in the t0102 plan.
* `tasks/t0099_random_init_pareto_robustness/code/run_three_seeds.sh` (62 lines) — copy as
  `run_two_seeds.sh`. Edit the `for SEED in 11 22 33` loop to `for SEED in 44 55`. Adjust the
  internal `VENV_PYTHON` and module path strings from `t0099_*` to `t0102_*`.

### Analysis pipeline (copy into task)

* `tasks/t0099_random_init_pareto_robustness/code/per_seed_analysis.py` (100 lines) — copy
  unchanged; iterate over `T0102_SEEDS`. Constants `STRICT_DSI_THRESHOLD = 0.5`,
  `STRICT_PD_RATE_HZ_THRESHOLD = 30.0`, `STRICT_ROBUSTNESS_THRESHOLD = 0.7` define the strict
  joint-pass corner.
* `tasks/t0099_random_init_pareto_robustness/code/anchor_classifier.py` (127 lines) — copy
  unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/biological_priors.py` (252 lines) — copy
  unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/biological_scorecard.py` (183 lines) — copy
  unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/cross_seed_analysis.py` (317 lines) — copy with
  edits. Extend the 5x4 anchor distribution table to 5x5 (5 anchors x { seed 44, seed 55, t0091,
  t0099 seed 11+22+33 aggregate }), and the HV/Pareto overlay to include the t0099 reference curves.
  Public function `main()`.
* `tasks/t0099_random_init_pareto_robustness/code/metrics_builder.py` (81 lines) — copy unchanged.
* `tasks/t0099_random_init_pareto_robustness/code/build_assets.py` (659 lines) — copy with edits
  to point at t0102 output paths and to produce 2 predictions assets (not 3) + 1 answer asset (not
  1+1).
* `tasks/t0099_random_init_pareto_robustness/code/build_morphology_charts.py` (328 lines) — copy
  unchanged for the morphology visualisation charts.
* `tasks/t0099_random_init_pareto_robustness/code/run_local_analysis.py` (35 lines) — copy with
  `T0099_*` paths swapped for `T0102_*`.
* `tasks/t0099_random_init_pareto_robustness/code/sync_results_back.sh` — copy with rsync
  source/destination edits.

### Optional reusable patterns from t0086 (copy into task)

For the t0102 clustering analysis step:

* `tasks/t0086_robustness_cluster_bio_comparison/code/cluster_analysis.py` (359 lines) — copy into
  task only if the analysis stage needs cluster centroids on Genuine cells. Edit the `LOWER_BOUNDS`
  / `UPPER_BOUNDS` imports to read from t0102's local `constants_electrophys.py` (54-d slice) rather
  than `tasks.t0080_*.code.constants` — this avoids the cross-task code import.
* `tasks/t0086_robustness_cluster_bio_comparison/code/classify_cells.py` (146 lines) — copy into
  task if t0102 wants the Genuine/Marginal/Stochastic classification at thresholds DSI=0.4 / PD=10
  Hz with 5-rep votes. Note: at `N_EVAL_SEEDS=4` the 5-rep classification rule does not directly
  apply; either lower `N_REPS` to 4 or reframe as 4-rep.

### Library imports (import via library)

* `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult`
  — library asset `procedural_dsgc_morphology_generator` [t0090].
* `from tasks.t0090_morphology_generator_diversity_test.code.constants import INT_PARAM_NAMES, PARAM_BOUNDS, PARAM_NAMES`
  — library asset `procedural_dsgc_morphology_generator` [t0090]. Note: the C-0093-01 correction
  *replaces* the whole library with t0092's fix, but `constants.py` is only present in the original
  t0090 asset's `module_paths`. The aggregator's effective view should resolve this; if it does not,
  copy these three names into t0102's `constants_morphology.py`.
* `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`
  — library asset `procedural_dsgc_morphology_generator_fix` [t0092].
* `from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import insert_baseline_channels`
  — same library [t0092].
* `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import _ensure_neuron_on_path, load_neuron`
  — library asset `de_rosenroll_2026_dsgc` [t0024]. Reached transitively via the copied
  `bootstrap.py`.

## Common Patterns

* **paths.py centralisation**: every task in the lineage (t0080, t0091, t0099 [t0080] [t0091]
  [t0099]) defines all input/output `Path` constants in a single `paths.py`. t0102 must follow the
  same pattern; no scattered hardcoded paths in driver/analysis code.
* **constants split**: t0099 split constants into `constants_electrophys.py` (54-d bounds + sim
  parameters), `constants_morphology.py` (14-d bounds + NSGA-II hyperparameters + tolerance
  windows), and `constants.py` (task-specific schedule wrapper). t0102 should preserve this
  three-file split — it makes the N_EVAL_SEEDS / N_GEN override changes localised to one file.
* **Module-level `_LIVE_CELLS` GC defense**: `generator_wrapper.py:38` keeps a module-level list of
  all built cells to prevent NEURON cell-id reuse after garbage collection (a known failure pattern
  caught in t0093 [t0093]). Preserve verbatim.
* **Bootstrap-by-import**: t0099's `bootstrap.py` triggers its Linux monkey-patches as a
  module-import side effect; all consumers must import it before any t0024 build path runs. Preserve
  verbatim.
* **Cost watchdog reads selected_offer.price_per_hour from machine_log.json**: avoids hard-coded
  hourly rates [t0099]. Preserve verbatim.

## Lessons Learned

* **t0093 [t0093] taught us to gate on a fingerprint**: the t0090 soma-pt3d bug produced silently
  NaN-valued cells in t0091 until t0093's 60-cell post-fix sweep validated 60/60 stability. t0102
  must run the smoke gate before committing to a long Vast.ai run; the fingerprint file
  `tasks/t0093_*/results/data/post_fix_verification_summary.json` is the reference.
* **t0099 [t0099] taught us that warm-start is load-bearing for PD-rate at low gen counts**: random
  init at N=5 gens<=8 produced 0/55 strict joint-pass cells with best PD-rate 18.7 Hz. t0102
  directly tests whether N=4 gens=20 lifts PD-rate by exposing the GA to 2.5x more selection rounds.
* **t0091 [t0091] taught us the warm-start anchor distribution**: bedb_like 20, symmetric 0,
  pd_asymmetric 12, nd_asymmetric 9, alt_topology 16. The symmetric anchor was empty in all 4
  historic datasets (t0091 + 3 t0099 seeds) — t0102 should expect the same and not regard a
  symmetric=0 outcome as failure.
* **t0086 [t0086] taught us the Genuine/Marginal/Stochastic ladder is data-quality dependent**: at
  5/5 reps required and DSI=0.4 / PD=10 Hz thresholds, only 6/20 top-Pareto cells from t0083 were
  Genuine. At N_EVAL_SEEDS=4 t0102 cannot apply the 5-rep rule directly — either downgrade to
  4-rep Genuine, or run a held-out 20-rep re-evaluation on the top cells post-NSGA-II.
* **t0083 budget overrun was caused by a hardcoded hourly rate** [t0099 cost_watchdog comment]:
  t0080 hardcoded $0.2382/hr but billed at $0.3209/hr (+35%). The fixed `cost_watchdog.py` reads the
  rate from `machine_log.json` — t0102 must keep this version.
* **NEURON cell-id reuse after GC is real** [t0093]: keep `_LIVE_CELLS` defense list.
* **pymoo `StarmapParallelization` import path moved**: t0099's nsga2_driver tries
  `from pymoo.parallelization.starmap` first and falls back to `pymoo.core.problem` — preserve
  this try/except for forward compatibility.

## Recommendations for This Task

1. **Copy t0099/code/ into t0102/code/ as the substrate, not re-import**. Copy the 22 Python files
   listed in "Reusable Code and Assets" plus `run_three_seeds.sh`. Total bulk approximately 5 619
   Python lines + 62 bash lines, minus the analysis files t0102 will not reuse. Estimated final
   t0102/code/ size: ~5 500 Python lines after edits. Drop t0099's anchor_definitions.py (kept) and
   any files exclusive to the 3-seed cross-seed plotting that t0102 will rewrite.

2. **Override `N_EVAL_SEEDS` and `N_GEN` by editing the local copy of `constants_morphology.py`**.
   This is the cleanest of the three documented strategies (see Recommended Approach section below).
   Do NOT modify t0080's `constants.py` (forbidden by the immutability rule and explicitly out of
   scope per task description "Out of Scope" line). Do NOT add a runtime env-var override (more
   complex than necessary and brittle).

3. **Rename the seed tuple and budget constants** in the copied `constants.py`:
   `T0099_SEEDS -> T0102_SEEDS = (44, 55)`,
   `T0099_HARD_BUDGET_PER_SEED_USD -> T0102_HARD_BUDGET_PER_SEED_USD = 4.00`,
   `T0099_TASK_BUDGET_TOTAL_USD -> T0102_TASK_BUDGET_TOTAL_USD = 8.00`.

4. **Reuse the t0099 smoke gate against the t0093 fingerprint** with the original 3 hardcoded smoke
   seeds (`[42, 4242, 424242]`). Do not weaken tolerances on the smoke gate itself; the "widened
   tolerance for the lower replicate count" is a separate auxiliary check on the variance gap
   between N_EVAL_SEEDS=4 and N_EVAL_SEEDS=20 (deferred to the analysis stage per the task fallback
   plan).

5. **Run the two seeds sequentially on the same Vast.ai instance** via the shell script
   `run_two_seeds.sh`, mirroring t0099's pattern. Do NOT parallelise across instances — the $8 cap
   is too tight to absorb a second instance's provisioning overhead.

6. **Extend `cross_seed_analysis.py` to a 5x5 anchor distribution and 5-line HV plot** (seed 44,
   seed 55, t0091 reference, t0099 aggregate, baseline). Read the t0091 and t0099 result files via
   the existing `T0091_*_JSON` constants and new `T0099_*_JSON` constants pointing at
   `tasks/t0099_*/results/data/`.

7. **Apply the t0086 cluster ladder only post-hoc on Genuine cells** (if any). At N_EVAL_SEEDS=4
   there are at most 4 reps per cell, so reframe Genuine as "4/4 reps pass DSI
   > = 0.4 AND PD >= 10 Hz" rather than 5/5. Document this in the t0102 plan REQ.

8. **Do not import the t0086 cluster_analysis module directly** — copy the relevant 359 lines into
   t0102/code/ if needed, and swap the LOWER/UPPER imports from `tasks.t0080_*.code` to t0102's
   local `constants_electrophys.py`. This satisfies the cross-task import rule.

## Recommended Approach

### Import-Shadow Strategy: copy `constants_morphology.py` into t0102 and edit `N_EVAL_SEEDS`

Three strategies were considered for overriding the noise-replicate constant:

| Strategy | Pros | Cons | Recommendation |
| --- | --- | --- | --- |
| **Copy t0099/constants_morphology.py and edit the copy** | Single source of truth in t0102; type-checkable; no runtime side-channels; obeys cross-task code reuse rule; matches the precedent set by t0099's own copy of t0080's constants. | One-line edit in a 145-line file; no automatic propagation if upstream constants change. | **CHOSEN**. |
| Environment-variable override read in the driver | Lets us flip values per-run without code edits. | Requires runtime guard in evaluator; loses static type checking; "secret" configuration; conflicts with the constants module's `assert` statements. | Rejected. |
| CLI flag / YAML config in the driver | Documented config; runtime-flexible. | Requires plumbing through evaluator + every termination + smoke gate; adds dataclass/argparse complexity; constants module asserts still need to run. | Rejected. |

**Concrete steps**:

1. `cp tasks/t0099_random_init_pareto_robustness/code/constants_morphology.py tasks/t0102_seedscale_n4_gen20/code/constants_morphology.py`.
2. Edit two lines: `N_EVAL_SEEDS: int = 5` -> `N_EVAL_SEEDS: int = 4` and `N_GEN: int = 8` ->
   `N_GEN: int = 20`.
3. Update the docstring at top of file to note the t0102 override.
4. The constants module's `assert N_EVAL_SEEDS >= 1`-style guards (currently absent — only the
   `LOWER_BOUNDS_68` shape asserts exist) are unaffected.

This requires zero changes to `evaluator.py`, `nsga2_driver.py`, `random_init.py`, or the smoke
gate; they all import from `constants_morphology` and pick up the new values automatically once the
copies live in `tasks/t0102_*/code/` and use t0102-relative module paths
(`from tasks.t0102_seedscale_n4_gen20.code.constants_morphology import N_EVAL_SEEDS`).

The same rationale applies to `N_GEN`: edit the copy, no runtime override.

### File copy sequence (recommended order)

1. Copy `bootstrap.py` first (no dependencies inside t0102/code/).
2. Copy `constants_electrophys.py`, `constants_morphology.py` (with edits), `constants.py` (with
   `T0099_*` -> `T0102_*` renaming).
3. Copy `paths.py` (with `T0102_*_JSON` additions for new outputs).
4. Copy `generator_wrapper.py`, `apply_params.py`, `parametric_placer.py`, `build_cell_ais.py`,
   `extend_with_ais.py`, `recorder.py`, `trial_helpers.py`.
5. Copy `evaluator.py`, `cost_watchdog.py`, `hv_plateau_watchdog.py`, `random_init.py`,
   `smoke_gate.py`, `anchor_definitions.py`.
6. Copy `nsga2_driver.py`, `run_three_seeds.sh -> run_two_seeds.sh`.
7. Copy analysis files `per_seed_analysis.py`, `anchor_classifier.py`, `biological_priors.py`,
   `biological_scorecard.py`, `cross_seed_analysis.py`, `metrics_builder.py`, `build_assets.py`,
   `build_morphology_charts.py`, `run_local_analysis.py`, `sync_results_back.sh`.
8. Run `uv run ruff check --fix tasks/t0102_seedscale_n4_gen20/code` and
   `uv run mypy -p tasks.t0102_seedscale_n4_gen20.code` to catch any missed `t0099_*` -> `t0102_*`
   import paths or constant references.

### Verification before launch

Run the smoke gate on a local Windows workstation with one anchor and 3 smoke seeds at
`N_EVAL_SEEDS=4` (the smoke gate's own seeds are hardcoded so this is a no-op for the smoke check,
but it exercises the import chain and the constants override). Compare against the t0093 anchor 1
fingerprint of 43.6 Hz +/- 1.0 Hz. If smoke fails, do not provision Vast.ai.

## Known Issues and Gotchas

* The task description and `step_tracker.json` step 6 reference `run_loop.py` — that file does not
  exist; the entry point is `nsga2_driver.py` + `run_three_seeds.sh`. Plan documentation should
  match the actual filenames.
* The task description says "import-shadow N_SEEDS from t0080's constants.py" — but the operative
  constant in the t0099 substrate is `N_EVAL_SEEDS` in t0099's own `constants_morphology.py`, not
  `N_SEEDS` in t0080. Plan/REQ language should use `N_EVAL_SEEDS`.
* t0099's `constants_electrophys.py:43` contains a dead `N_SEEDS = 20` that is never imported. When
  copying, leave it as-is or delete it; do not edit to `N_SEEDS = 4`, because doing so would imply
  someone consumes it and confuse future readers.
* `constants_morphology.py:142-145` asserts a 96-cell warmstart layout
  (`N_ANCHORS * N_CLONES_PER_ANCHOR + N_RANDOM_FILL == POP_SIZE`) which is dead code for the
  random-init path but the assert still fires at import time. It currently passes (5 * 19 + 1 = 96);
  do not touch it.
* `constants.py:54` asserts
  `sum([T0099_HARD_BUDGET_PER_SEED_USD] * len(T0099_SEEDS)) <= T0099_TASK_BUDGET_TOTAL_USD`. At
  t0102 values (`4.00 * 2 = 8.00 <= 8.00`) this passes exactly; if the per-seed budget is set
  higher, the assert will fire. Keep per-seed at $4 or lower.
* The pymoo `MaximumGenerationTermination(n_max_gen=N_GEN)` will run for 20 generations on t0102;
  combined with `HVPlateauTermination` and `CostWatchdogTermination` in `TerminationCollection`, any
  one of the three can stop the run. The HV plateau threshold is `HV_PLATEAU_REL_THRESHOLD = 0.01`
  over `HV_PLATEAU_WINDOW = 2` with `HV_PLATEAU_MIN_HV_HISTORY = 4` — meaning the plateau check is
  suppressed for the first 4 generations, then trips on <1% improvement over the trailing 2. At
  gens=20 this may terminate the run before reaching 20 generations if HV plateaus; this is desired
  behaviour, not a bug.
* Compiled MOD files at `tasks/t0080_*/code/mods/x86_64/` are NOT in t0099's library asset. t0099's
  `paths.py` references them directly via `T0080_MODS_DIR`. t0102 must do the same; do NOT recompile
  MODs into t0102's tree. NEURON SUFFIX namespace is shared and t0080's MODs satisfy the t0102
  evaluator.
* `apply_params.py` writes to NEURON section attributes by suffix name; the 12 channel suffixes
  (`nav16t80`, `kv3t80`, ...) are baked into t0080's MODs. t0102 must continue using those exact
  suffix strings — do not rename channels.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Source of the Bed B compartmental substrate; provides `de_rosenroll_2026_dsgc`
  library asset (HOC template, vendored MOD library, `build_cell`, `_ensure_neuron_on_path`,
  `load_neuron`) which t0099's `bootstrap.py` monkey-patches for Linux and t0102 will inherit
  verbatim.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery
* **Status**: completed
* **Relevance**: Source of the 54-d electrophys parameter layout (`ParamIndex`, `LOWER_BOUNDS`,
  `UPPER_BOUNDS`, `LOG_PARAM_INDICES`, `INT_PARAM_INDICES`), the 12 channel SUFFIX names, the
  compiled MOD library at `code/mods/`, and the NSGA-II hyperparameter defaults. Contains the
  `N_SEEDS = 20` constant that the task description mentioned but t0099 (and t0102) actually bypass
  via `N_EVAL_SEEDS` in t0099's own constants_morphology.

### [t0083]

* **Task ID**: `t0083_bedb_v3_extend_nsga2_gen8plus`
* **Status**: completed
* **Relevance**: Provides the best-cell electrophys vector used by t0099's smoke gate
  (`T0083_PARETO_FRONT_JSON`); t0102 reuses the same anchor for substrate-consistency verification.

### [t0086]

* **Task ID**: `t0086_robustness_cluster_bio_comparison`
* **Name**: Robustness cluster + bio comparison on t0083 top cells
* **Status**: completed
* **Relevance**: Source of the clustering pipeline (`cluster_analysis.py` k=2..6 with silhouette +
  BIC + bootstrap ARI), the Genuine/Marginal/Stochastic classification (`classify_cells.py`
  thresholds DSI=0.4, PD=10 Hz, 5/5 reps), and the biological scorecard pattern. Reusable for t0102
  post-NSGA-II analysis with the 5-rep rule reframed as 4-rep at `N_EVAL_SEEDS=4`.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Morphology generator diversity test
* **Status**: completed
* **Relevance**: Source of the `procedural_dsgc_morphology_generator` library asset:
  `MorphologyParams`, `MorphologyResult`, `MorphometricSummary`, `BEDB_BASE_POINT`, `PARAM_BOUNDS`,
  `PARAM_NAMES`, `INT_PARAM_NAMES`. The library is now superseded by C-0093-01 redirecting to
  t0092's fix; t0090's dataclass and constants modules are still the canonical type definitions used
  by t0099/t0102.

### [t0091]

* **Task ID**: `t0091_morphology_extended_nsga2_v1`
* **Name**: First joint 68-d NSGA-II with morphology generator in-loop
* **Status**: completed
* **Relevance**: The warm-start reference: 57 Pareto cells, 1 strict joint-pass cell at DSI=0.511
  PD=35.1 Hz robust=0.79, anchor distribution
  [bedb_like 20, symmetric 0, pd_asymm 12, nd_asymm 9, alt_topology 16]. Result files
  (`tasks/t0091_*/results/data/pareto_front.json`, `hv_trajectory.json`, `anchor_tracking.json`,
  `biological_scorecard_68d.json`) are read by t0099 and will be read by t0102's cross-seed
  analysis.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology generator silence
* **Status**: completed
* **Relevance**: Source of the `procedural_dsgc_morphology_generator_fix` library asset
  (`generate_fixed_morphology`, `insert_baseline_channels`) that patches the soma-pt3d collapse bug.
  t0099's `generator_wrapper.py` and (transitively) t0102's copy import from t0092 via the library's
  `module_paths`. C-0093-01 redirects any lookup of `procedural_dsgc_morphology_generator` to this
  asset.

### [t0093]

* **Task ID**: `t0093_resweep_and_t0090_correction`
* **Name**: 60-morph re-sweep + t0090 correction overlay
* **Status**: completed
* **Relevance**: Validates the t0092 fix at scale (60/60 stable, 56/60 with PD-rate > 0) and records
  the `replace` correction overlay (C-0093-01) against the t0090 library. The post-fix verification
  fingerprint `tasks/t0093_*/results/data/post_fix_verification_summary.json` is the reference for
  t0102's smoke gate (anchor 1 bedb_like PD-rate ~43.6 Hz +/- 1.0 Hz).

### [t0099]

* **Task ID**: `t0099_random_init_pareto_robustness`
* **Name**: Random-init NSGA-II reproducibility test
* **Status**: completed
* **Relevance**: THE substrate to reuse. 5 619 Python lines of NSGA-II driver, evaluator, generator
  wrapper, bootstrap, constants, cost watchdog, smoke gate, and analysis pipeline. t0102 copies ~22
  of t0099's `.py` files verbatim with only constants edits. Result data (3 seeds 11/22/33 at
  N_EVAL_SEEDS=5 gens=5-8 pop=96, 55 Pareto cells total, 0 strict joint-pass) is the null baseline
  t0102 is trying to overturn.

### [t0101]

* **Task ID**: `t0101_brainstorm_results_21`
* **Name**: Brainstorm session 21 — Poleg-Polsky 2026 deep-dive
* **Status**: completed
* **Relevance**: Commissioned t0102 with explicit parameter targets (N_SEEDS=4, gens=20, GA
  seeds=(44,55), $8 cap). No answer assets were produced — the task is a pure decision-recording
  brainstorm; the parameter choice is documented in `tasks/t0101_*/results/results_summary.md` and
  in the t0102 task_description. The deferred suggestion S-0101-02 (lower the project-wide N_SEEDS
  default in t0080) is contingent on t0102's outcome.
