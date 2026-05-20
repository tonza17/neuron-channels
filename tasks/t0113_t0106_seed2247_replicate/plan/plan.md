---
spec_version: "2"
task_id: "t0113_t0106_seed2247_replicate"
date_completed: "2026-05-20"
status: "complete"
---
# Plan: Seed-2247 Random-Seed Replicate of t0106 Long 2-Direction NSGA-II

## Objective

Re-run the t0106 long 2-direction NSGA-II run on the identical 68-d Bed B electrophys + 14-d
morphology substrate using GA seed 2247 (drawn at random via `secrets.randbelow(10000)` immediately
before task creation) under the t0112 protocol: pool-restart cadence of 10 generations and an
`N_GEN = 60` ceiling with the HV-plateau auto-stop preserved as the primary trigger. This task is a
direct fork of `t0112_t0106_seed77_replicate` with exactly two changes vs t0112: (a) the seed
constant (`T0112_SEEDS = (77,)` becomes `T0113_SEEDS = (2247,)`) and (b) the package path
(`tasks.t0112_t0106_seed77_replicate` becomes `tasks.t0113_t0106_seed2247_replicate`). The task
contributes the third independent seed point to the S-0112-01 substrate-rate confirmation batch,
which currently spans only seeds 44 (t0106: 123 joint-pass cells, 3.3%) and 77 (t0112: 7 joint-pass
cells, 0.35%) — a 17x dispersion that prevents reporting any substrate-level mean joint-pass
acceptance rate from a 2-point sample. **Done** means: (1) the seed-2247 NSGA-II run completes on a
single Vast.ai CPU instance under the $25 hard cost cap; (2) a single predictions asset
`t0113-bedb-morph-nsga2-seed2247` is produced under `assets/predictions/`, mirroring t0112's schema
(`spec_version: "2"`, gzipped JSON, per-cell records with the t0106/t0112 five-field shape); (3)
`results/metrics.json` records the registered `direction_selectivity_index` metric plus operational
metrics (joint-pass count, n_cells_evaluated_total, hv_plateau_gen); (4) the 5 task-specified charts
are saved to `results/images/` and the 2 CSV tables to `results/data/`. The replicate is meaningful
regardless of outcome: a high joint-pass count (>= 40) tightens the substrate-populated reading; a
low count (0-6) hardens the "seed-specific density" reading; an intermediate count keeps the
S-0112-01 batch moving with at least a 3-point estimator.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0113_t0106_seed2247_replicate/task.json` and the resolved long
description at `tasks/t0113_t0106_seed2247_replicate/task_description.md`:

```text
Name: Seed-2247 random-seed replicate of t0106 long 2-direction NSGA-II

Short description: Re-run the t0106 NSGA-II substrate with a randomly drawn GA seed (2247),
pool-restart-every=10, and HV-plateau auto-stop to add a third independent seed point for the
substrate-rate confirmation.

Dependencies: t0106_long_pdnd_nsga2_300gen, t0112_t0106_seed77_replicate.
Expected assets: 1 predictions.
Task types: experiment-run.
Source suggestion: S-0112-01.

Long description (excerpts):
* In scope (unchanged from t0106 / t0112): substrate (Bed B 54-d electrophys + 14-d morphology =
  68 free parameters), objectives (2-direction ratio DSI + PD-rate at 0 deg), NSGA-II
  hyperparameters (pop=96, SBX/PM operators), evaluation protocol (N_EVAL_SEEDS = 3, ratio DSI,
  silence guard active), HV-plateau termination constants.
* In scope, changed from t0106: GA seed (44 -> 2247, randomly drawn), pool-restart cadence
  (25 -> 10 gens, same as t0112), gen ceiling (300 -> 60 with HV-plateau operator-stop preserved
  as the primary trigger).
* Out of scope: any change to substrate, objective formulation, evaluation protocol, silence
  guard, NSGA-II driver beyond the three constants above, predictions asset schema, metrics list,
  or cost-watchdog wiring.
* Fork t0112 code into tasks/t0113_t0106_seed2247_replicate/code/ (verbatim algorithm-critical
  modules + orchestration shell script).
* Rewrite package import paths: tasks.t0112_t0106_seed77_replicate ->
  tasks.t0113_t0106_seed2247_replicate across every .py and .sh file. Do not touch upstream
  imports (t0024, t0080, t0090, t0092).
* Apply exactly one constant patch: T0112_SEEDS = (77,) -> T0113_SEEDS = (2247,);
  T0112_HARD_BUDGET_USD -> T0113_HARD_BUDGET_USD (value 25.00 unchanged);
  T0112_PER_INSTANCE_WATCHDOG_USD -> T0113_PER_INSTANCE_WATCHDOG_USD (value 20.00 unchanged).
  Update backwards-compat aliases and __all__ export list. nsga2_driver.py keeps
  _POOL_RESTART_EVERY = 10 from t0112 verbatim; constants_morphology.py keeps N_GEN = 60 from
  t0112 verbatim.
* Smoke gate locally (5 checks identical to t0106 / t0112): single-eval driver, ratio DSI
  synthetic sanity, silence-guard unit tests, pool-restart sanity, watchdog wiring.
* Provision Vast.ai single instance (same filter class as t0106 / t0112: EPYC class CPU,
  >= 100 GB RAM, RTX 3060 Ti or equivalent idle GPU, reliability >= 0.99, dph <= 0.40, EPYC
  family post-filter).
* Launch with cost cap $25 per-task and per-instance watchdog $20. Operator-stop on HV plateau
  or at gen 60 ceiling.
* Collect 1 predictions asset at
  assets/predictions/t0113-bedb-morph-nsga2-seed2247/
  with spec_version "2", gzipped JSON, fields generation, vector_68d, objective_F_minimised,
  dsi_vector_sum (back-compat name storing ratio DSI), pd_rate_hz. Required metrics_at_creation
  keys: n_generations_completed, n_cells_total, best_dsi_ratio, best_pd_rate_hz,
  n_joint_pass_unique, n_joint_pass_evaluations, final_hypervolume, final_cost_usd.
* 5 charts (pareto_front_3seeds.png, hv_vs_gen_3seeds.png, joint_pass_yield_per_gen_3seeds.png,
  top50_morphologies_seed2247.png, asymmetry_distribution_3seeds.png).
* 2 tables (joint_pass_summary_3seeds.csv, pareto_front_overlap_3seeds.csv) in results/data/.
* Registered metrics: direction_selectivity_index (sub-variants best_legit, dsi_eq_one_count).
* Key questions answered in results_summary.md: (1) seed-2247 joint-pass count bucket
  (>=40 / 7-39 / 1-6 / 0); (2) best ratio DSI >= 0.95?; (3) best PD-rate >= 100 Hz?;
  (4) three-seed substrate-rate mean and SE vs Hay2011 0.40% / Druckmann2007 0.10% baselines;
  (5) HV-plateau gen vs t0106 gen 40 / t0112 gen 21; (6) per-gen wall-clock within 20% of
  t0112's 620 s/gen baseline; (7) Pareto front overlap in normalised parameter space.
```

Concrete requirements decomposed (each item names the step that satisfies it and the evidence that
proves completion):

* **REQ-1** — **Verbatim t0112 code fork.** Copy every algorithm-critical Python module from
  `tasks/t0112_t0106_seed77_replicate/code/` into `tasks/t0113_t0106_seed2247_replicate/code/`
  (algorithm-critical modules per research_code.md: `__init__.py`, `bootstrap.py`,
  `apply_params.py`, `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`,
  `recorder.py`, `trial_helpers.py`, `generator_wrapper.py`, `cost_watchdog.py`,
  `hv_plateau_watchdog.py`, `evaluator.py`, `constants_electrophys.py`, `anchor_definitions.py`,
  `anchor_classifier.py`, `biological_priors.py`, `biological_scorecard.py`, `nsga2_driver.py`,
  `test_evaluator_dsi_guard.py`, `constants.py`, `constants_morphology.py`, `paths.py`,
  `random_init.py`, `smoke_gate.py`, plus `run_seed77.sh` renamed). Satisfied by step 1 (copy) and
  step 2 (import rewrite). Evidence:
  `grep -r "t0112_t0106_seed77_replicate" tasks/t0113_t0106_seed2247_replicate/code/` returns zero
  matches; `ls tasks/t0113_t0106_seed2247_replicate/code/*.py | wc -l` is at least 22 modules.

* **REQ-2** — **GA seed change 77 -> 2247.** `constants.py` declares
  `T0113_SEEDS: tuple[int, ...] = (2247,)` (renamed from `T0112_SEEDS = (77,)`); the
  backwards-compat aliases (`T0104_SEEDS`, `T0106_SEEDS`) are updated to reference `T0113_SEEDS`;
  the `__all__` export list lists `T0113_SEEDS` (not `T0112_SEEDS`). Satisfied by step 3. Evidence:
  `grep -n "T0113_SEEDS: tuple" tasks/t0113_t0106_seed2247_replicate/code/constants.py` returns one
  line containing `(2247,)`;
  `grep -n "T0112_SEEDS" tasks/t0113_t0106_seed2247_replicate/code/constants.py` returns zero lines.

* **REQ-3** — **Budget constant rename (value unchanged).** `T0112_HARD_BUDGET_USD = 25.00` becomes
  `T0113_HARD_BUDGET_USD = 25.00`; `T0112_PER_INSTANCE_WATCHDOG_USD = 20.00` becomes
  `T0113_PER_INSTANCE_WATCHDOG_USD = 20.00`. Values unchanged; only names change. Satisfied by step
  3\. Evidence:
  `grep -n "T0113_HARD_BUDGET_USD: float = 25.00" tasks/t0113_t0106_seed2247_replicate/code/constants.py`
  returns one line;
  `grep -n "T0113_PER_INSTANCE_WATCHDOG_USD: float = 20.00" tasks/t0113_t0106_seed2247_replicate/code/constants.py`
  returns one line; `results/data/algorithm_config.json` `"hard_budget_usd"` equals `25.00`.

* **REQ-4** — **No driver edits beyond constant references.** `nsga2_driver.py:97` keeps
  `_POOL_RESTART_EVERY: int = 10` from t0112 verbatim; `constants_morphology.py` keeps
  `N_GEN: int = 60` from t0112 verbatim. The HV-plateau constants (`HV_PLATEAU_WINDOW = 2`,
  `HV_PLATEAU_MIN_HV_HISTORY = 60`, `HV_PLATEAU_REL_THRESHOLD = 0.01` per research_code.md) are not
  touched. Satisfied by step 3 (do-not-edit constraint) and step 4 (diff verification). Evidence:
  `grep -n "_POOL_RESTART_EVERY: int = 10" tasks/t0113_t0106_seed2247_replicate/code/nsga2_driver.py`
  returns one line;
  `grep -n "N_GEN: int = 60" tasks/t0113_t0106_seed2247_replicate/code/constants_morphology.py`
  returns one line.

* **REQ-5** — **Diff against t0112 is exactly the seed/budget rename plus the package-path
  rewrite.** After the package-path rewrite, the only non-mechanical diff between the t0112 and
  t0113 code trees is the three `T0112_*` -> `T0113_*` renames in `constants.py` (plus back-compat
  alias and `__all__` updates) and the seed value `(77,)` -> `(2247,)`. No edits to `evaluator.py`,
  `apply_params.py`, `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`,
  `recorder.py`, `trial_helpers.py`, `generator_wrapper.py`, `hv_plateau_watchdog.py`,
  `cost_watchdog.py`, `bootstrap.py`, the silence guard, the SBX/PM operators, the LHS init sampler,
  the dill checkpoint cadence, the operator-stop polling, or the predictions asset writer beyond the
  package-path rewrite. Satisfied by steps 1, 2, 4. Evidence:
  `diff -r tasks/t0112_t0106_seed77_replicate/code/ tasks/t0113_t0106_seed2247_replicate/code/`
  filtered against the package-path string returns only the expected constant lines (REQ-2/REQ-3
  changes and the `run_seed*.sh` rename).

* **REQ-6** — **5-check local smoke gate passes before remote provisioning.** Run `smoke_gate.py`
  and the silence-guard pytest before provisioning. All 5 checks must pass: (1) single-eval driver
  run completes with DSI in `[0, 1]` and PD-rate in `[0, 200] Hz` (anchor-1 bedb_like expected ~43.6
  Hz +/- 2 Hz per research_code.md); (2) ratio DSI synthetic sanity (PD=5, ND=1 -> 0.6667 +/- 1e-6);
  (3) silence-guard unit tests pass; (4) pool-restart sanity (`_POOL_RESTART_EVERY = 10` reads
  correctly from `nsga2_driver`); (5) watchdog wiring (`make_watchdog_from_machine_log` returns a
  `CostWatchdog` with `hard_budget_usd = 25.00`). Satisfied by step 6. Evidence:
  `logs/steps/<step_id>/smoke_gate.json` (or stdout) reports all 5 checks `passed: true`. If any
  check fails, step 7 (provisioning) MUST NOT proceed; an intervention file must be created.

* **REQ-7** — **Vast.ai provisioning matches t0106 / t0112 class.** A single Vast.ai CPU instance is
  provisioned with the same filter class as t0106 / t0112: EPYC class CPU (e.g. AMD EPYC 7B13/7763),
  >= 100 GB RAM, RTX 3060 Ti or equivalent idle GPU, reliability >= 0.99, dph <= 0.40, EPYC family
  post-filter (`cpu_name LIKE '%EPYC%'`). Satisfied by step 7. Evidence:
  `logs/steps/<step_id>_setup-machines/machine_log.json` records the selected offer; the `cpu_name`
  field contains "EPYC".

* **REQ-8** — **Cost watchdog wired correctly with $25 hard cap.** The driver's call site for
  `make_watchdog_from_machine_log` (in `nsga2_driver.py:487-491` per research_code.md) passes
  `T0113_HARD_BUDGET_USD = 25.00`, NOT the legacy `T0104_HARD_BUDGET_USD = 4.00` default that lives
  in `cost_watchdog.py:27`. Per-instance watchdog is $20. Satisfied by step 3 (constant declaration)
  and step 8 (driver invocation). Evidence:
  `grep -n "T0113_HARD_BUDGET_USD" tasks/t0113_t0106_seed2247_replicate/code/constants.py` shows the
  value `25.00`; `results/data/algorithm_config.json` `"hard_budget_usd"` equals `25.00`;
  `results/costs.json` `total_usd <= 25.00`.

* **REQ-9** — **MOD library compiles on the Vast.ai instance.** 13 `.mod` files from
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` plus the t0024 vendored MODs are SCP'd
  to the instance and compiled with `nrnivmodl`, producing `x86_64/.libs/libnrnmech.so`. The compile
  is handled at runtime by `bootstrap.py:_compile_t0024_mods_linux` plus
  `paths.resolve_t99_mod_library` for the t0080 MODs. Satisfied by step 7. Evidence:
  `logs/steps/<step_id>_setup-machines/mod_compile.log` shows `nrnivmodl` exit 0 and a non-empty
  `libnrnmech.so` listing.

* **REQ-10** — **NSGA-II run terminates correctly.** The run terminates either at the HV-plateau
  stop (primary), at `N_GEN = 60` (hard ceiling), at the $25 cost watchdog, or via the operator-stop
  file `intervention/stop.md`. Satisfied by step 8. Evidence: `results/data/termination_reason.json`
  (or equivalent log) names the trigger; `logs/steps/<step_id>_implementation/hv_trace.jsonl` line
  count <= 60.

* **REQ-11** — **Predictions asset format matches t0106 / t0112 exactly.** Asset folder is named
  `assets/predictions/t0113-bedb-morph-nsga2-seed2247/`. `details.json` has `spec_version: "2"`,
  same five per-cell schema fields as t0106 / t0112 (`generation`, `vector_68d`,
  `objective_F_minimised`, `dsi_vector_sum` (note: stores ratio DSI; field name kept for back-compat
  with t0102/t0104/t0106/t0112 downstream tooling), `pd_rate_hz`), same categories
  (`direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`), same gzipped-JSON
  file format (`files/all_evaluations_seed2247.json.gz`).
  `instance_count = 96 x (1 + n_gen_completed)`. Required `metrics_at_creation` keys per
  `task_description.md` lines 89-91: `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`,
  `best_pd_rate_hz`, `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`,
  `final_cost_usd`. The `model_description` records the random-seed provenance (drawn via
  `secrets.randbelow(10000)`) per research_code.md recommendation 9. Satisfied by step 9. Evidence:
  `uv run python -u -m arf.scripts.aggregators.aggregate_predictions --ids t0113-bedb-morph-nsga2-seed2247 --format json`
  returns one record with the correct `instance_count`; the predictions verificator passes.

* **REQ-12** — **Registered metric written to `results/metrics.json`.** The registered
  `direction_selectivity_index` metric is reported using the explicit multi-variant metrics format
  (same shape as t0106 / t0112 for cross-task comparability) with sub-variants `best_legit` (highest
  non-DSI=1.0 cell) and `dsi_eq_one_count` (number of cells at exactly DSI = 1.0 — these are
  silence-guard or single-spike artefacts per t0106 / t0112 reporting). Plus operational metrics
  (not registered): `joint_pass_count`, `best_pd_rate_hz`, `n_cells_evaluated_total`,
  `hv_plateau_gen` (`null` if not reached), `n_gen_completed`,
  `efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`.
  `pd_rate_hz` is NOT a registered project metric (only `direction_selectivity_index`,
  `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse` exist in
  `meta/metrics/`); it is reported as an operational metric only. Training-time efficiency is
  explicitly omitted (NSGA-II is not conventional model training). Satisfied by step 10. Evidence:
  `uv run python -c "import json; d=json.load(open('tasks/t0113_t0106_seed2247_replicate/results/metrics.json')); print(list(d['variants'][0]['metrics']))"`
  lists `direction_selectivity_index` plus the operational keys.

* **REQ-13** — **5 charts produced in `results/images/`.** Per `task_description.md` lines 111-130:
  (a) `pareto_front_3seeds.png` (DSI vs PD-rate overlay for seeds 44, 77, 2247); (b)
  `hv_vs_gen_3seeds.png` (log-scale HV trajectory for all three seeds); (c)
  `joint_pass_yield_per_gen_3seeds.png` (joint-pass cell count per gen for all three seeds); (d)
  `top50_morphologies_seed2247.png` (10x5 grid of best 50 t0113 cells, coloured by archetype, same
  format as t0106/t0112); (e) `asymmetry_distribution_3seeds.png` (4-panel histogram of soma offset,
  elongation, branch density gradient, primary branch PD concentration for top-50 cells of all three
  seeds). All saved as PNG. Satisfied by step 10. Evidence:
  `ls tasks/t0113_t0106_seed2247_replicate/results/images/*.png | wc -l >= 5` and exact filenames
  match.

* **REQ-14** — **2 summary tables produced in `results/data/`.** Per `task_description.md` lines
  132-138: (a) `joint_pass_summary_3seeds.csv` (per-seed (44, 77, 2247) totals: evals, joint-pass
  count, joint-pass %, best DSI, best PD-rate, plateau generation); (b)
  `pareto_front_overlap_3seeds.csv` (for each t0113 Pareto cell, nearest-neighbour distance in
  normalised parameter space to its closest t0106 cell AND its closest t0112 cell; use the z-scored
  L2 metric from S-0112-04 if available, otherwise report both raw L2 and z-scored L2 and document
  the choice in the orchestrator-managed reporting outputs). Satisfied by step 10. Evidence: both
  CSV files exist and parse as pandas DataFrames with the expected columns.

* **REQ-15** — **Vast.ai instance destroyed within 5 min of last completed gen or operator-stop.**
  Satisfied by step 11. Evidence: `verify_machines_destroyed t0113_t0106_seed2247_replicate` returns
  0 errors; `machine_log.json` `destroyed: true` and `destroyed_at` timestamp <= 5 min after the
  last `hv_trace.jsonl` line.

* **REQ-16** — **Random-seed provenance documented in the predictions asset.** The predictions
  asset's `model_description` field and the asset's `description.md` mention that GA seed 2247 was
  drawn via `secrets.randbelow(10000)` to avoid the "round-ish-low-number" selection bias of seeds
  44 and 77, mirroring `task_description.md` lines 21-26. Satisfied by step 9. Evidence:
  `grep -n "secrets.randbelow" tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/description.md`
  returns at least one line.

* **REQ-17** — **No edits to upstream task imports.** The imports from `tasks.t0024_*`,
  `tasks.t0080_*`, `tasks.t0090_*`, `tasks.t0092_*` remain unchanged (the verificator allows
  full-path imports of UPSTREAM tasks per the Cross-Task Code Reuse Rule). Satisfied by step 2
  (rewrite restricted to t0112 -> t0113). Evidence:
  `grep -rn "tasks.t0024_\|tasks.t0080_\|tasks.t0090_\|tasks.t0092_" tasks/t0113_t0106_seed2247_replicate/code/`
  returns the same upstream import line set as t0112's tree (no spurious adds or drops).

* * *

## Approach

**Task type recommended**: `experiment-run` (matches `task.json` `task_types: ["experiment-run"]`).
The Planning Guidelines from `meta/task_types/experiment-run/instruction.md` drive the design: fixed
and recorded random seed (GA seed 2247, drawn via `secrets.randbelow(10000)`), per-condition metrics
breakdown in explicit multi-variant `metrics.json` for cross-task comparability with t0106 / t0112,
an explicit validation gate (5-step local smoke gate) before any Vast.ai provisioning, cost tracking
against the $25 hard cap (per-task default $8 explicitly overridden in `task_description.md`), >= 2
charts saved to `results/images/` (this task produces 5 plus 2 CSV tables), predictions asset under
`assets/predictions/`. Reproducibility: seed 2247 is the only stochastic input; the NSGA-II run is
deterministic given the seed, the Bed B substrate, the t0092-patched morphology generator, and the
t0080-vendored MOD library.

**Technical approach (grounded in `research/research_code.md` findings).** The entire delta between
t0112 and t0113 lives in three lines of `constants.py` plus a global search-and-replace across every
`.py` and `.sh` file. Per research_code.md finding "The Patch Surface Is Exactly One Constant Rename
Plus the Package-Path Rewrite":

1. **GA seed 77 -> 2247.** `constants.py` line 59: `T0112_SEEDS: tuple[int, ...] = (77,)` ->
   `T0113_SEEDS: tuple[int, ...] = (2247,)`. The value 2247 was drawn locally by
   `secrets.randbelow(10000)` immediately before task creation (recorded in `task_description.md`
   lines 21-22). Consumed by `random_init.main()` and by `run_seed77.sh` (renamed to
   `run_seed2247.sh`).
2. **Budget constants renamed (values unchanged).** `T0112_HARD_BUDGET_USD = 25.00` ->
   `T0113_HARD_BUDGET_USD = 25.00`; `T0112_PER_INSTANCE_WATCHDOG_USD = 20.00` ->
   `T0113_PER_INSTANCE_WATCHDOG_USD = 20.00`. Backwards-compat aliases at lines 65-71 of
   `constants.py` (`T0104_SEEDS`, `T0104_HARD_BUDGET_PER_SEED_USD`, `T0104_TASK_BUDGET_TOTAL_USD`,
   `T0106_SEEDS`, `T0106_HARD_BUDGET_USD`, `T0106_PER_INSTANCE_WATCHDOG_USD`) are updated to point
   at the new `T0113_*` constants. The `__all__` export list at lines 77-114 likewise gets the three
   `T0112_*` -> `T0113_*` renames.
3. **No driver edits.** `nsga2_driver.py:97` keeps `_POOL_RESTART_EVERY = 10` from t0112 verbatim
   (the cadence-10 protocol that delivered the 3.5x per-gen wall-clock speedup vs t0106's
   cadence-25). `constants_morphology.py` keeps `N_GEN = 60` from t0112 verbatim. The HV-plateau
   detector constants (`HV_PLATEAU_WINDOW = 2`, `HV_PLATEAU_MIN_HV_HISTORY = 60`,
   `HV_PLATEAU_REL_THRESHOLD = 0.01`) stay at t0106 / t0112 values so the stopping criterion is
   bitwise identical across all three seeds.

The cross-task import rule (per `arf/specifications/research_code_specification.md`'s
`Cross-Task Code Reuse Rule`) forbids `tasks.t0112_t0106_seed77_replicate.code` imports. Per
research_code.md finding "The Cross-Task Import Rule Forces a Verbatim Copy of t0112's Code", the
established pattern (t0106 -> t0112 already used it) is verbatim copy with a global `sed` rewrite:
`tasks.t0112_t0106_seed77_replicate` -> `tasks.t0113_t0106_seed2247_replicate`. Upstream task
imports (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`, `tasks.t0092_*`) stay valid unchanged —
the verificator allows full-path imports of UPSTREAM tasks.

**Predictions asset schema.** Per research_code.md finding "The Predictions Asset Schema Is Locked
at spec_version '2' and Must Be Mirrored Exactly": t0112's
`assets/predictions/t0112-bedb-morph-nsga2-seed77/details.json` defines `spec_version: "2"` with
per-cell schema fields `generation`, `vector_68d`, `objective_F_minimised`, `dsi_vector_sum` (stores
ratio DSI; name preserved for back-compat with t0102/t0104), `pd_rate_hz`. File format is gzipped
JSON (`.json.gz`). t0113 mirrors this exactly with folder name `t0113-bedb-morph-nsga2-seed2247`
(task-brief-specified at `task_description.md` lines 87-88) and file
`files/all_evaluations_seed2247.json.gz`. The `dsi_vector_sum` field name lie (it stores a
2-direction ratio DSI, not a vector-sum DSI) is preserved verbatim: renaming it to `dsi_ratio` would
break `cross_seed_analysis.py` and `build_t0112_results.py` (which walk t0106 / t0112 / t0113
predictions assets simultaneously).

**Cost watchdog.** Per research_code.md finding "The Cost Watchdog Wiring Already Reads
T0112_HARD_BUDGET_USD By Name": the factory `make_watchdog_from_machine_log` is called in
`nsga2_driver.py:487-491` with `hard_budget_usd=T0112_HARD_BUDGET_USD`. After the global rewrite,
this reference becomes `hard_budget_usd=T0113_HARD_BUDGET_USD` automatically. The legacy
`T0104_HARD_BUDGET_USD = 4.00` default in `cost_watchdog.py:27` MUST be overridden at the driver
call site to `T0113_HARD_BUDGET_USD = 25.00`. Per-instance watchdog: $20.

**Project budget envelope check (research_code.md "Cost Headroom Is Comfortable" + task description
"Compute and Budget").** Project `project/budget.json` has `total_budget = $100.0`,
`per_task_default_limit = $8.0`. Per the orchestrator context, $58.79 has been spent and $41.21
remains. The $25 per-task cap fits comfortably in the $41.21 remainder. Expected actual spend per
research_code.md is $2-11 depending on plateau gen (t0112 plateaued at gen 21 for $1.99; t0106
plateaued at gen 40 for $10.37). The $25 hard cap is honoured by passing
`T0113_HARD_BUDGET_USD = 25.00` into `make_watchdog_from_machine_log` at the driver call site.

**Alternatives considered**:

* **Run two or three new seeds in this task at fewer gens (e.g., 3 seeds x 25 gens).** Rejected
  because (a) the task brief explicitly says "this task contributes one of those additional seeds"
  and the S-0112-01 batch will run other seeds in separate parallel tasks; (b) collapsing multiple
  seeds into one task collapses the per-seed cost cap and removes the ability to discover
  per-seed-specific failures; (c) the t0106 / t0112 single-seed-per-task pattern is the established
  convention. Multi-seed-per-task would be a process change, not a substrate change.
* **Pick the seed from a curated low-number candidate set (like t0112 did with 77).** Rejected per
  `task_description.md` lines 22-27 — the explicit motivation for this task is to draw a random seed
  and widen the support beyond the 44-99 range, so any pattern of "low seeds favourable / high seeds
  unfavourable" becomes detectable across the eventual 5-seed sample. Seed 2247 was drawn via
  `secrets.randbelow(10000)` immediately before task creation.
* **Disable the HV-plateau stop (suggestion S-0112-03 from t0112).** Rejected because the task brief
  forbids any change beyond the seed/budget rename. If t0113 plateaus before gen 30 and finds <= 10
  joint-pass cells, the censoring hypothesis hardens and S-0112-03 becomes a priority follow-up
  generated in t0113's reporting stage.
* **Re-evaluate t0106 / t0112 cells at 8 directions (t0107 pattern, suggestion S-0112-05).**
  Rejected — out of scope per the task brief's "out of scope" list. The 8-direction re-evaluation is
  a separate downstream re-evaluation task type, not a substrate replicate. A follow-up suggestion
  mirroring S-0112-05 should be generated in t0113's reporting stage scoped to t0113 cells only.
* **Change the silence guard, DSI metric, or substrate definition.** Rejected explicitly per the
  task brief's "out of scope" list. Any evaluator change breaks the like-for-like comparison with
  t0106 / t0112.

**Validation gate**: the 5-check local smoke gate (single-eval driver, ratio DSI synthetic sanity,
silence-guard unit tests, pool-restart sanity, watchdog wiring) is the only gate between local fork
and the $20-25 Vast.ai spend. All 5 checks must pass; if any fails, an intervention file is created
and provisioning halted. The single-eval driver run is the expensive operation proxy on Windows (~5
min wall-clock) and serves as the explicit experiment-run validation gate per the task type Planning
Guidelines.

**Baseline comparisons**: t0106 seed-44 results (123 unique joint-pass cells, best ratio DSI =
1.0000, best PD-rate = 122.62 Hz, final HV = 122.0288, final cost $10.37, 40 gens completed of 300);
t0112 seed-77 results (7 unique joint-pass cells, best ratio DSI = 0.9535, best PD-rate = 114.76 Hz,
final HV = 107.4602, final cost $1.99, 21 gens completed of 60). t0113 results are compared against
these in `joint_pass_summary_3seeds.csv` and the 5 charts. The Hay 2011 (0.40%) and Druckmann 2007
(0.10%) literature joint-pass acceptance-rate envelope is the substrate-level target for the
eventual S-0112-01 5-seed sample; t0113 is one of the >= 3 additional seeds required to complete
that batch.

* * *

## Cost Estimation

* **Vast.ai single CPU instance (EPYC class, RTX 3060 Ti idle)**: expected hourly rate ~$0.24-0.36/h
  (t0106 selected at $0.24/h on an EPYC 7B13 64-core Norway instance; t0112 ran at the same class
  with comparable rate). Expected wall-clock 2-4 h for the t0112-cadence-10 protocol (t0112
  plateaued at gen 21 in ~3.6 h; t0106 plateaued at gen 40 in ~~24 h at the slower cadence-25).
  Productive compute: **~~$0.50-1.60**.
* **Setup + MOD compilation + idle**: ~30 min at $0.36/h = **$0.18**.
* **Conservative buffer for retries / post-run download**: **$1.00**.
* **No LLM API costs** — all NSGA-II logic runs locally on the Vast.ai instance with no external API
  calls. No paid third-party services beyond Vast.ai compute.
* **Estimated total**: **$2-11 expected**, **$25 hard cap** (per-instance watchdog $20 inside
  `CostWatchdogTermination`; $25 orchestrator-level ceiling via `T0113_HARD_BUDGET_USD`).
* **t0106 / t0112 precedent**: t0106 spent $10.37 at cadence-25 / 40 gens; t0112 spent $1.99 at
  cadence-10 / 21 gens. t0113 inherits t0112's cadence-10 protocol; the most likely spend is $2-3 if
  the plateau detector fires near gen 21 (like t0112), or $5-11 if it runs out to gen 40-60 (like
  t0106 would have at cadence-10).
* **Project budget context**: `project/budget.json` `total_budget = $100.0`. $58.79 already spent;
  **$41.21 remaining**. The $25 hard cap fits the remainder comfortably with $16.21 reserve after
  this task at the cap, and ~$30+ reserve at the expected $2-11 spend. The total_budget was raised
  from $75 to $100 ahead of t0113 (per git log entry `9eb55892`).
* **Per-task default limit override**: the per-task default in `project/budget.json` is $8; this
  task explicitly overrides to $25 (declared in `task_description.md`'s "Compute and Budget"
  section). The override is honoured by passing `T0113_HARD_BUDGET_USD = 25.00` into
  `make_watchdog_from_machine_log` at the driver call site.

* * *

## Step by Step

Implementation work only. Orchestrator-managed steps (results writing, suggestions,
compare-literature, reporting) are not in this list per the plan specification.

### Milestone 1: Local Code Fork + Smoke Gate (steps 1-6)

1. **Copy t0112 `code/` verbatim into `tasks/t0113_t0106_seed2247_replicate/code/`.** Source:
   `tasks/t0112_t0106_seed77_replicate/code/` (algorithm-critical subset, ~5,800 lines across the
   modules listed in research_code.md "The t0112 Code Tree Has 35 Python Modules Totalling 8,427
   Lines"). The required algorithm-critical files are: `__init__.py`, `bootstrap.py`,
   `apply_params.py`, `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`,
   `recorder.py`, `trial_helpers.py`, `generator_wrapper.py`, `cost_watchdog.py`,
   `hv_plateau_watchdog.py`, `evaluator.py`, `constants_electrophys.py`, `anchor_definitions.py`,
   `anchor_classifier.py`, `biological_priors.py`, `biological_scorecard.py`, `nsga2_driver.py`,
   `test_evaluator_dsi_guard.py`, `constants.py`, `constants_morphology.py`, `paths.py`,
   `random_init.py`, `smoke_gate.py`, plus the orchestration shell script `run_seed77.sh` (rename to
   `run_seed2247.sh` in step 3). Analysis modules (`build_t0112_results.py`,
   `cross_seed_analysis.py`, `build_morphology_charts.py`, `build_predictions_assets.py`,
   `make_charts.py`, `metrics_builder.py`, `per_seed_analysis.py`, `run_local_analysis.py`,
   `build_analysis_charts.py`, `build_assets.py`, `build_t0106_plots.py`) are deferred to the
   analysis stage and ported on demand in step 10. Inputs: t0112 code directory. Outputs:
   `tasks/t0113_t0106_seed2247_replicate/code/` mirror containing >= 22 algorithm-critical modules.
   Expected observable output: `ls tasks/t0113_t0106_seed2247_replicate/code/*.py | wc -l >= 22` and
   each named file present. **Satisfies REQ-1 (groundwork), REQ-5.**

2. **Rewrite package import paths.** In every copied `.py` and `.sh` file, replace
   `tasks.t0112_t0106_seed77_replicate` with `tasks.t0113_t0106_seed2247_replicate`. Use a single
   PowerShell pass
   (`(Get-Content -Raw $file) -replace 'tasks\.t0112_t0106_seed77_replicate', 'tasks.t0113_t0106_seed2247_replicate' | Set-Content $file -Encoding utf8`)
   across all files, or
   `sed -i 's/tasks\.t0112_t0106_seed77_replicate/tasks.t0113_t0106_seed2247_replicate/g'` on the
   bash side. Do NOT touch upstream task references (`tasks.t0024_*`, `tasks.t0080_*`,
   `tasks.t0090_*`, `tasks.t0092_*`, `tasks.t0093_*`) — those are valid as full-path imports of
   UPSTREAM tasks per the Cross-Task Code Reuse Rule. The `random_init.py` docstring and the
   `paths.py` historical docstring drift (mentioning t0102 per research_code.md) are inherited
   unchanged; only the import paths change. Inputs: step 1 output. Outputs: identical structure with
   corrected imports. Expected output:
   `grep -r "t0112_t0106_seed77_replicate" tasks/t0113_t0106_seed2247_replicate/code/` returns zero
   matches;
   `grep -r "tasks.t0024_\|tasks.t0080_\|tasks.t0090_\|tasks.t0092_" tasks/t0113_t0106_seed2247_replicate/code/`
   still returns the expected upstream imports unchanged. **Satisfies REQ-1, REQ-5, REQ-17.**

3. **Apply the constant patch and rename the orchestration script.** Edit
   `tasks/t0113_t0106_seed2247_replicate/code/constants.py`:

   * Line 59: rename `T0112_SEEDS: tuple[int, ...] = (77,)` to
     `T0113_SEEDS: tuple[int, ...] = (2247,)`.
   * Line 60: rename `T0112_HARD_BUDGET_USD: float = 25.00` to
     `T0113_HARD_BUDGET_USD: float = 25.00` (value unchanged).
   * Line 61: rename `T0112_PER_INSTANCE_WATCHDOG_USD: float = 20.00` to
     `T0113_PER_INSTANCE_WATCHDOG_USD: float = 20.00` (value unchanged).
   * Backwards-compat aliases at lines 65-71 (`T0104_SEEDS`, `T0104_HARD_BUDGET_PER_SEED_USD`,
     `T0104_TASK_BUDGET_TOTAL_USD`, `T0106_SEEDS`, `T0106_HARD_BUDGET_USD`,
     `T0106_PER_INSTANCE_WATCHDOG_USD`): update to reference the new `T0113_*` constants.
   * Assertion comments at lines 73-75 (if present in t0112): update to reference `T0113_*`
     constants.
   * `__all__` export list at lines 77-114: swap the three `T0112_*` names for `T0113_*`.

   `nsga2_driver.py:97` `_POOL_RESTART_EVERY = 10` is NOT touched (kept from t0112 verbatim).
   `constants_morphology.py` `N_GEN = 60` is NOT touched (kept from t0112 verbatim). Update the
   `random_init.py:21` import name from `T0112_SEEDS` to `T0113_SEEDS` (and any other site that
   references `T0112_SEEDS`, e.g. line 96 in `main()`). Rename the orchestration script
   `run_seed77.sh` to `run_seed2247.sh`; inside the script change `SEED=77` at line 39 to
   `SEED=2247`. Inputs: step 2 output. Outputs: patched `constants.py`, patched `random_init.py`,
   renamed orchestration script. Expected output:
   `grep -n "T0113_SEEDS: tuple\[int, \.\.\.\] = (2247,)" tasks/t0113_t0106_seed2247_replicate/code/constants.py`
   returns one line;
   `grep -n "T0113_HARD_BUDGET_USD: float = 25.00" tasks/t0113_t0106_seed2247_replicate/code/constants.py`
   returns one line; `grep -n "T0112" tasks/t0113_t0106_seed2247_replicate/code/constants.py`
   returns zero lines (all renamed); `ls tasks/t0113_t0106_seed2247_replicate/code/run_seed2247.sh`
   exists. **Satisfies REQ-2, REQ-3, REQ-4 (do-not-touch confirmation), REQ-8 (constant declaration
   half).**

4. **Verify the diff against t0112 is exactly the intended changes.** Run
   `diff -r tasks/t0112_t0106_seed77_replicate/code/ tasks/t0113_t0106_seed2247_replicate/code/`
   (excluding `__pycache__`, `.pyc`, analysis modules not copied, and the `run_seed77.sh` ->
   `run_seed2247.sh` rename) and confirm the non-mechanical diffs are ONLY: (a) the `T0112_*` ->
   `T0113_*` renames in `constants.py` (5 lines: `T0112_SEEDS`, `T0112_HARD_BUDGET_USD`,
   `T0112_PER_INSTANCE_WATCHDOG_USD`, backwards-compat aliases, `__all__` entries); (b) the `(77,)`
   -> `(2247,)` value change; (c) the `T0112_SEEDS` -> `T0113_SEEDS` import-name change in
   `random_init.py`; (d) the package-path string `t0112_t0106_seed77_replicate` ->
   `t0113_t0106_seed2247_replicate` throughout; (e) the `SEED=77` -> `SEED=2247` change in the
   renamed orchestration script. If unexpected diffs appear, fix them before proceeding. Inputs:
   step 3 output. Outputs: a diff log confirming a tight delta. Expected output: the filtered diff
   contains only the categories (a)-(e) above. **Satisfies REQ-5 (verification), REQ-17.**

5. **Sanity-import the code package.** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0113_t0106_seed2247_replicate -- uv run python -c "import tasks.t0113_t0106_seed2247_replicate.code.constants as c; import tasks.t0113_t0106_seed2247_replicate.code.constants_morphology as cm; import tasks.t0113_t0106_seed2247_replicate.code.nsga2_driver; import tasks.t0113_t0106_seed2247_replicate.code.evaluator; assert c.T0113_SEEDS == (2247,), c.T0113_SEEDS; assert c.T0113_HARD_BUDGET_USD == 25.00, c.T0113_HARD_BUDGET_USD; assert cm.N_GEN == 60, cm.N_GEN; print('imports ok')"`.
   Expected: prints `imports ok` and exits 0. If any ImportError or AssertionError, halt and fix
   package paths or constants. **Satisfies REQ-1, REQ-2, REQ-3, REQ-4 (importability gate + value
   spot-check).**

6. **[CRITICAL] Run the 5-check local smoke gate (validation gate before remote provisioning).**
   This is the explicit validation gate per the experiment-run task type Planning Guidelines.

   * **Baseline reference**: t0106 / t0112 seed single-cell evaluation in the smoke gate returned
     DSI in `[0, 1]` and PD-rate in `[0, 200] Hz`; anchor-1 bedb_like expected ~43.6 Hz +/- 2 Hz per
     research_code.md "Smoke Gate" section (relaxed tolerance accounts for the sqrt(20/3) noise
     variance increase at `N_EVAL_SEEDS = 3` vs the t0099 `N = 20` calibration). t0113's smoke gate
     single-eval must land in the same ranges — these are sanity bounds, not the operating point.
   * Run
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0113_t0106_seed2247_replicate -- uv run python -u -m tasks.t0113_t0106_seed2247_replicate.code.smoke_gate`.
     Expected: 5 sub-checks all green within ~5 min wall-clock total. The 5 checks per
     `task_description.md` are: (1) single-eval driver run completes (DSI in `[0, 1]`, PD-rate in
     `[0, 200] Hz`, anchor-1 ~43.6 Hz +/- 2 Hz); (2) ratio DSI synthetic sanity (PD=5, ND=1 ->
     0.6667 +/- 1e-6); (3) silence-guard unit tests pass (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`
     clamps DSI to 0 on a degenerate silent case); (4) pool-restart sanity
     (`_POOL_RESTART_EVERY = 10` reads correctly from the driver module); (5) watchdog wiring
     (`make_watchdog_from_machine_log` returns a `CostWatchdog` with `hard_budget_usd = 25.00`).
   * Run
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0113_t0106_seed2247_replicate -- uv run python -u -m pytest tasks/t0113_t0106_seed2247_replicate/code/test_evaluator_dsi_guard.py -v`.
     Expected: 0 failures across the silence-guard pytest cases.
   * **Validation failure condition**: if any of the 5 smoke-gate checks fail OR the unit-test suite
     reports any failure (i.e., the smoke-gate result is at or below the t0112 baseline of 5/5
     green), halt — do NOT proceed to step 7 (Vast.ai provisioning). Create
     `intervention/smoke_gate_failed.md` with the specific failure and STOP. Do not blow $20 of
     remote compute on a known-broken pipeline.
   * **Individual-output inspection**: after the smoke gate passes, read at least 5 individual
     cell-evaluation outputs from the smoke-gate stdout (DSI, PD-rate, ND-rate, total spike count
     per anchor cell). Verify each value is in the expected range and the silence-guard zeros out
     DSI on the degenerate cases. Document this inspection in the step log.

   Inputs: step 5 output. Outputs: `logs/steps/<step_id>_implementation/smoke_gate.json` (or
   equivalent) with all five checks `passed: true`. **Satisfies REQ-6.**

### Milestone 2: Remote Provisioning + Run (steps 7-8)

7. **Provision the Vast.ai instance and compile MODs.** Run the `setup-remote-machine` skill via the
   orchestrator. Filters per `task_description.md` "Compute and Budget" section and t0106 / t0112
   precedent: EPYC class CPU (AMD EPYC 7B13 or equivalent like 7763), >= 100 GB RAM, RTX 3060 Ti or
   equivalent GPU (idle — workload is CPU-only NEURON), reliability >= 0.99, dph (dollars per hour)
   <= 0.40, post-filter for EPYC family (string match `cpu_name LIKE '%EPYC%'`, mirroring t0104's,
   t0106's, and t0112's pattern). Record `logs/steps/<step_id>_setup-machines/offer_filters.json`
   and `machine_log.json`.

   * Install NEURON 8.2.7, NetPyNE 1.1.1, pymoo, dill, numpy, scipy via `uv sync` on the instance.
   * SCP 13 `.mod` files from `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` plus
     `mod_func.c` to the instance at the same relative path. The list (per research_code.md):
     `bkt80.mod`, `calt80.mod`, `catt80.mod`, `iht80.mod`, `kdrt80.mod`, `kv3t80.mod`, `kv4t80.mod`,
     `kv7t80.mod`, `napt80.mod`, `nart80.mod`, `nav16t80.mod`, `skahpt80.mod`, `skt80.mod`. Also SCP
     the t0024 vendored MOD sources at
     `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/`.
   * Run `nrnivmodl` in the `mods/` directory to produce `x86_64/.libs/libnrnmech.so`. Verify with
     `ls -la x86_64/.libs/libnrnmech.so` (file exists, non-zero size). The t0024 compile is handled
     at runtime by `bootstrap.py:_compile_t0024_mods_linux`.

   Inputs: step 6 pass. Outputs: provisioned Vast.ai instance with NEURON, MODs, and t0113 code.
   **Satisfies REQ-7, REQ-9.**

8. **[CRITICAL] Launch the NSGA-II run (the load-bearing step).** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0113_t0106_seed2247_replicate -- uv run python -u -m tasks.t0113_t0106_seed2247_replicate.code.nsga2_driver --seed 2247 --teardown-on-watchdog`
   (the `--seed 2247` argument is redundant with `T0113_SEEDS = (2247,)` but is included explicitly
   for log traceability). The driver:

   * Initialises pop = 96 random LHS, `n_eval_seeds = 3`, `n_directions = 2`, seed 2247.

   * Runs the `TerminationCollection`: `MaximumGenerationTermination(n_max_gen=60)`,
     `HVPlateauTermination(...)` (HV-plateau stop, primary trigger; constants identical to t0106 /
     t0112), `CostWatchdogTermination(watchdog=$25)`, `OperatorStopTermination(stop_signal_md())`.

   * `_GenerationCallback` writes one JSON line per gen to
     `logs/steps/<step_id>_implementation/hv_trace.jsonl` (fields `gen`, `wall_clock_s`, `hv`,
     `n_cells_evaluated`) and dill-checkpoints the algorithm to `checkpoint_gen<NNNN>.pkl`.

   * `PerGenerationPoolRestart` (instantiated with `restart_every = _POOL_RESTART_EVERY = 10`)
     closes and recreates the `multiprocessing.Pool` every 10 gens, swapping
     `problem.elementwise_runner = StarmapParallelization(pool.starmap)`. At `N_GEN = 60`, this
     yields up to 6 restarts (vs 2 in t0106's 40 completed gens at `_POOL_RESTART_EVERY = 25`).

   * `_save_algorithm_config` writes `results/data/algorithm_config.json` with
     `pool_restart_every: 10`, `hard_budget_usd: 25.00`, `task_seed: 2247`.

   * **Validation gate (after gen 1)**: pull `hv_trace.jsonl` from the remote instance and verify
     exactly 1 well-formed JSON line with the 4 required fields. **Trivial baseline**: the gen-1 LHS
     init population (96 cells) for a healthy substrate produces HV > 0 (t0106 started at HV =
     0.2015; t0112 started at HV = 0.1156). **Failure condition**: if the `hv_trace.jsonl` file is
     empty, contains no parseable JSON, or the gen-1 HV is exactly 0 (indicating all 96 LHS cells
     were silenced — pipeline broken), halt and read 5 individual cell outputs (DSI, PD-rate,
     ND-rate, total spike count, parameter vector) before letting the run proceed to gen 5.

   * **Per-cell baseline check (after gen 1)**: pull 5 random cells from the predictions log on the
     instance and verify `dsi_ratio in [0, 1]`, `pd_rate >= 0`, `nd_rate >= 0`. **Failure
     condition**: if any cell is out of these ranges, OR if the gen-1 best DSI is above 0.99
     (suspiciously close to the silence-guard ceiling — likely a degenerate-cell artefact), halt and
     read 5 individual cell outputs before letting the run continue.

   * The orchestrator pulls `hv_trace.jsonl` periodically and watches for HV-plateau or operator
     stop. The operator can write `intervention/stop.md` to halt at the next gen boundary.

   Inputs: step 7 provisioning + step 6 smoke-gate pass. Outputs: `hv_trace.jsonl`,
   `checkpoint_gen<NNNN>.pkl` files, per-cell predictions log on the Vast.ai instance. Expected
   runtime: 2-4 h wall-clock at HV-plateau stop (most likely gen 21-50 based on the t0106 / t0112
   range); cost $2-11 actual against $25 cap. **Satisfies REQ-2, REQ-4 (driver reads renamed
   constant), REQ-8, REQ-10.**

### Milestone 3: Asset Assembly + Teardown (steps 9-11)

9. **Download artefacts and build the predictions asset.** SCP from the Vast.ai instance to the
   worktree:

   * `logs/steps/<step_id>_implementation/hv_trace.jsonl` (the per-gen HV trace).
   * All `checkpoint_gen<NNNN>.pkl` files to `logs/steps/<step_id>_implementation/checkpoints/`.
   * `results/data/algorithm_config.json` (records `pool_restart_every`, `hard_budget_usd`,
     `task_seed`).
   * The per-cell predictions log (every evaluated cell across all completed gens).

   Build the **predictions asset** at
   `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/`:

   * **`details.json`**: `spec_version: "2"`, `predictions_id: "t0113-bedb-morph-nsga2-seed2247"`,
     `name: "NSGA-II seed 2247 on 68-d Bed B + 14-d morphology, 2 directions, 60-gen replicate of t0106/t0112"`,
     `model_id: null`,
     `model_description: "Identical to t0112 except GA seed 77 -> 2247 (drawn via secrets.randbelow(10000) to avoid round-ish-low-number selection bias). Pool restart cadence 10 (same as t0112). N_GEN=60 with HV-plateau auto-stop. 68-d Bed B + 14-d morphology substrate, ratio DSI metric, silence guard active, N_EVAL_SEEDS=3."`,
     `dataset_ids: []`, `prediction_format: "json.gz"`,
     `prediction_schema: <copy t0112's schema verbatim, swapping "seed77" -> "seed2247">`,
     `instance_count = 96 x (1 + n_gen_completed)`,
     `categories: ["direction-selectivity", "compartmental-modeling", "retinal-ganglion-cell"]`,
     `created_by_task: "t0113_t0106_seed2247_replicate"`, `date_created` = ISO 8601 date.
   * **`description.md`** per `meta/asset_types/predictions/specification.md`, documenting the
     seed/budget rename vs t0112 (no other algorithm changes), the back-compat naming of
     `dsi_vector_sum` (stores ratio DSI; field name kept for t0102/t0104/t0106/t0112 downstream
     compatibility), and the random-seed provenance ("GA seed 2247 was drawn via
     `secrets.randbelow(10000)` immediately before task creation to avoid the 'round-ish-low-number'
     selection bias of seeds 44 and 77").
   * **`files/all_evaluations_seed2247.json.gz`** — gzipped JSON with top-level key `evaluations` ->
     list of per-cell records. Each record: `generation` (int, 1 = LHS init, 2+ = offspring),
     `vector_68d` (list of 68 floats = 54-d electrophys + 14-d morphology), `objective_F_minimised`
     (list of 2 floats = sign-flipped `[-ratio_dsi, -pd_rate_hz]`), `dsi_vector_sum` (float in
     [0, 1], guard-cleaned ratio DSI; field name preserved for back-compat), `pd_rate_hz` (float,
     mean PD firing rate in Hz across the 3 noise replicates). Format identical to t0106's
     `all_evaluations_seed44.json.gz` and t0112's `all_evaluations_seed77.json.gz`. The 5 MB
     pre-commit limit is respected via gzip.
   * Required `metrics_at_creation` keys: `n_generations_completed`, `n_cells_total`,
     `best_dsi_ratio`, `best_pd_rate_hz`, `n_joint_pass_unique`, `n_joint_pass_evaluations`,
     `final_hypervolume`, `final_cost_usd`.

   Validation: total record count in the unzipped JSON matches `96 x (1 + n_gen_completed)`.
   **Satisfies REQ-11, REQ-16.**

10. **Compute metrics and produce charts.** Port the t0112 analysis modules
    (`build_t0112_results.py`, `cross_seed_analysis.py`, `build_morphology_charts.py`,
    `build_predictions_assets.py` writer portion, `make_charts.py`, `metrics_builder.py`,
    `per_seed_analysis.py`, `run_local_analysis.py`) into
    `tasks/t0113_t0106_seed2247_replicate/code/` on demand, adapting them to read THREE seed sources
    (t0106 seed 44, t0112 seed 77, t0113 seed 2247) instead of two. Rename `build_t0112_results.py`
    to `build_t0113_results.py` (or equivalent) and update its read paths to include the t0113
    predictions asset alongside the t0106 and t0112 assets. Write
    `tasks/t0113_t0106_seed2247_replicate/results/metrics.json` using the explicit multi-variant
    format (per `arf/specifications/metrics_specification.md` and the `experiment-run` task type
    guidance). One variant with `variant_id: "random-init-seed2247-2dir-60gen"`, dimensions matching
    t0106 / t0112 variant shape (`task_seed: 2247`, `init_method: "lhs_random"`, `n_obj: 2`,
    `n_directions: 2`, `dsi_metric: "ratio"`, `dsi_silence_guard_active: true`, `n_eval_seeds: 3`,
    `n_generations_target: 60`, `n_generations_completed`, `n_cells`).

    * Registered metric: `direction_selectivity_index` — best ratio DSI across all evaluated cells
      (`max(dsi_ratio)`). Sub-variant `best_legit` = highest non-DSI=1.0 cell; sub-variant
      `dsi_eq_one_count` = number of cells at exactly DSI = 1.0 (these are silence-guard or
      single-spike artefacts per t0106 / t0112 reporting).
    * Operational metrics (not registered): `joint_pass_count` (cells with
      `dsi_ratio >= 0.5 AND pd_rate_hz >= 30.0`); `best_pd_rate_hz` (mirrors t0106's reported 122.62
      Hz and t0112's 114.76 Hz); `n_cells_evaluated_total`; `hv_plateau_gen` (gen at which the
      HV-plateau detector fires; `null` if not reached); `n_gen_completed`;
      `efficiency_inference_time_per_item_seconds = total_wall_clock_s / n_cells_evaluated_total`;
      `efficiency_inference_cost_per_item_usd = total_cost_usd / n_cells_evaluated_total`.
      Training-time efficiency is explicitly omitted because NSGA-II is not conventional model
      training. `pd_rate_hz` is NOT a registered project metric (only `direction_selectivity_index`,
      `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse` are registered per
      the `aggregate_metrics` aggregator output); the task brief's mention of best PD-rate is
      treated as an operational metric request, not a registered metric. The omission is deliberate
      and documented here.

    Generate charts to `tasks/t0113_t0106_seed2247_replicate/results/images/` per
    `task_description.md` lines 111-130:

    * `pareto_front_3seeds.png` — overlay of t0106 (seed 44), t0112 (seed 77), and t0113 (seed 2247)
      strict Pareto fronts on DSI vs PD-rate axes; coloured by source task. Read t0106's predictions
      asset at
      `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`
      and t0112's at
      `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz`
      for the comparison data.
    * `hv_vs_gen_3seeds.png` — log-scale HV trajectory for all three seeds on the same axes, with
      pool-restart events annotated (every 10 gens for t0112 / t0113; every 25 for t0106).
    * `joint_pass_yield_per_gen_3seeds.png` — joint-pass cell count discovered per generation for
      all three seeds.
    * `top50_morphologies_seed2247.png` — 10x5 grid of best 50 cells from t0113 (by joint-pass
      ranking or by ratio DSI ranking if joint-pass count < 50), coloured by archetype, matching the
      t0106 / t0112 top50 format.
    * `asymmetry_distribution_3seeds.png` — 4-panel histogram (soma offset, elongation, branch
      density gradient, primary branch PD concentration) for top-50 cells from all three seeds.

    Generate tables to `tasks/t0113_t0106_seed2247_replicate/results/data/`:

    * `joint_pass_summary_3seeds.csv` — per-seed (44, 77, 2247): total evals, joint-pass count,
      joint-pass %, best DSI, best PD-rate, plateau generation.
    * `pareto_front_overlap_3seeds.csv` — for each t0113 Pareto cell, the parameter-space
      nearest-neighbour distance to its closest t0106 Pareto cell AND its closest t0112 Pareto cell.
      Use the z-scored L2 metric from S-0112-04 if completed before t0113's analysis stage;
      otherwise compute BOTH raw L2 AND per-dimension z-scored L2 and document the choice in the
      orchestrator-managed reporting outputs. The raw L2 in 68-d space is dominated by
      conductance-scale parameters spanning 6 orders of magnitude (per t0112's results summary), so
      the z-scored variant is essential for substantive overlap claims.

    Inputs: step 9 outputs + t0106 predictions asset + t0112 predictions asset. Outputs:
    `results/metrics.json`, 5 PNG charts, 2 CSV tables. **Satisfies REQ-12, REQ-13, REQ-14.**

11. **Teardown the Vast.ai instance.** Run the `setup-remote-machine` skill in teardown mode (or
    call the orchestrator's teardown procedure). Verify destruction within 5 min of the last
    completed gen or operator-stop detection. Update
    `logs/steps/<step_id>_teardown/machine_log.json` with `destroyed: true` and a `destroyed_at`
    timestamp. Inputs: step 10 confirms all artefacts pulled. Outputs: `machine_log.json` with
    `destroyed: true`; Vast.ai dashboard confirms instance gone. **Satisfies REQ-15.**

* * *

## Remote Machines

Single Vast.ai CPU instance required. Filters: EPYC class CPU (AMD EPYC 7B13 or equivalent like
7763), >= 100 GB RAM, RTX 3060 Ti or equivalent GPU (idle — workload is CPU-only NEURON),
reliability >= 0.99, dph (dollars per hour) <= 0.40, post-filter for EPYC family (string match
`cpu_name LIKE '%EPYC%'`, mirroring t0104's, t0106's, and t0112's pattern). Expected hourly rate
~$0.24-0.36/h. Estimated wall-clock: 2-4 h (HV-plateau stop likely at gen 21-50 based on the t0106
gen-40 / t0112 gen-21 range; hard ceiling at gen 60). Cost cap: $25 total ($20 per-instance watchdog
enforced inside `CostWatchdogTermination`; $25 orchestrator-level ceiling via
`T0113_HARD_BUDGET_USD`). Teardown within 5 min of last completed gen or `intervention/stop.md`
detection. Reference: `arf/specifications/remote_machines_specification.md`.

* * *

## Assets Needed

* **Code substrate from t0112** (dependency `t0112_t0106_seed77_replicate`): the entire
  algorithm-critical `code/` subset copied verbatim with package-path rewrite, and one constant
  patch per the patch table in Approach (seed value `(77,)` -> `(2247,)`, three `T0112_*` ->
  `T0113_*` renames, backwards-compat alias updates, `__all__` export updates). t0112 is the
  canonical fork base (not t0106 directly) because t0112 already carries the cadence-10 protocol and
  `N_GEN = 60` ceiling that this task needs.
* **t0106 predictions asset for 3-seed comparison charts and tables** (dependency
  `t0106_long_pdnd_nsga2_300gen`):
  `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`.
  Read-only; used by step 10 to build the 3-seed charts and tables.
* **t0112 predictions asset for 3-seed comparison charts and tables** (dependency
  `t0112_t0106_seed77_replicate`):
  `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz`.
  Read-only; used by step 10 to build the 3-seed charts and tables.
* **MOD library source from t0080** (transitive dependency
  `t0080_bedb_mobo_v3_dendritic_spike_nsga2`): 13 `.mod` files plus `mod_func.c` at
  `tasks/t0080_*/code/mods/`, SCP'd to the Vast.ai instance and compiled with `nrnivmodl`. Resolved
  at runtime by `paths.resolve_t99_mod_library`.
* **t0024 Bed B port** (transitive dependency `t0024_port_de_rosenroll_2026_dsgc`): vendored MOD
  sources at `assets/library/de_rosenroll_2026_dsgc/sources/`, plus the `constants` and
  `ar2_noise.generate_ar2_batch` modules imported via full-path
  `tasks.t0024_port_de_rosenroll_2026_dsgc.code.*`.
* **Morphology generator from t0090 + t0092 patched** (transitive dependencies; canonical via
  correction C-0093-01): imported via full-path
  `tasks.t0090_morphology_generator_diversity_test.code.morphology_params`,
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix`, and
  `tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels`.
* **No external datasets, no new papers, no LLM API access required.**

* * *

## Expected Assets

Matches `task.json` `expected_assets`: `{"predictions": 1}`.

* **1 predictions asset** at
  `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/`
  containing every evaluated cell across all completed generations of the seed-2247 run. Each cell
  record carries the 68-d parameter vector (`vector_68d`), the NSGA-II minimised objective vector
  (`objective_F_minimised = [-ratio_dsi, -pd_rate_hz]`), the ratio DSI (`dsi_vector_sum`; field name
  preserved for t0102/t0104/t0106/t0112 back-compat), `pd_rate_hz`, and the generation index
  (`generation`). Format: gzipped JSON. Total record count: exactly `96 x (1 + n_gen_completed)`.
  Required `metrics_at_creation` keys per `task_description.md` lines 89-91:
  `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`. The
  `model_description` field records the random-seed provenance (drawn via
  `secrets.randbelow(10000)`).

* * *

## Time Estimation

* Research (already complete): research_code only; ~1 h logged in
  `logs/steps/<step_id>_research-code/`.
* Planning (this step): 0.5 h.
* Local code fork + import rewrite + constant patch (Milestone 1, steps 1-5): **0.5-1 h** (~5,800
  lines copied, single `sed`/PowerShell rewrite, single-file constant edits, script rename).
* Local smoke gate (Milestone 1, step 6): **0.5 h** (5 checks on Windows including NEURON
  single-cell eval at the cadence-10 protocol; ~5 min wall-clock total for the gate).
* Vast.ai provisioning + MOD compilation (Milestone 2, step 7): **0.5-1 h**.
* NSGA-II run (step 8): **2-4 h** wall-clock (HV-plateau stop likely at gen 21-50; 60-gen ceiling).
  t0112 ran 21 gens in ~3.6 h at the same cadence; t0106 ran 40 gens in ~24 h at the slower
  cadence-25.
* Asset assembly + metrics + charts (Milestone 3, steps 9-10): **1-2 h** (analysis-module port from
  t0112 is the main work; the actual chart/table compute is small).
* Teardown (step 11): **0.1 h**.
* **Total wall-clock envelope: 5-9 h** (matches expected actual cost of $2-11 at the t0112 per-hour
  rate; envelope is dominated by the NSGA-II run itself).

* * *

## Risks & Fallbacks

**Pre-mortem**: if t0113 has failed completely at completion time, the most likely failure modes
are: (a) seed 2247 yields 0 joint-pass cells (the substrate-density-is-seed-dependent reading
hardens — still publishable as a 3-point sample for S-0112-01); (b) the cadence-10 pool restart
introduces a race with seed 2247 specifically (very unlikely since t0112 already proved the protocol
robust on seed 77); (c) MOD library ABI surprise on the new Vast.ai instance (Linux MOD fails to
load despite local smoke gate passing on Windows DLL); (d) operator misses the HV-plateau window and
`N_GEN = 60` ceiling triggers later than expected, blowing wall-clock past 5-6 h; (e)
`dsi_vector_sum` schema field rename slips into the code (silently breaking back-compat with t0106 /
t0112 analysis modules); (f) HV-plateau threshold is too tight for seed 2247 and the run never
plateau-stops, requiring operator intervention; (g) the package-path rewrite accidentally edits an
upstream import (t0024/t0080/t0090/t0092), breaking the cross-task dependency chain.

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Seed 2247 produces 0 joint-pass cells (substrate density seed-dependent) | Medium | Low (still publishable as the third S-0112-01 point; widens the dispersion estimator) | Run is short ($2-11 spend); the 3-seed dispersion (44=123, 77=7, 2247=0/N) is itself the headline finding regardless of N; no re-run of this task |
| Cadence-10 pool restart introduces a seed-2247-specific race not surfaced by seed 77 | Very low | High (algorithm hangs or crashes) | Smoke-gate check 4 (pool-restart sanity) catches structural issues locally; if the remote run hangs at a restart boundary, the per-gen `dill` checkpoint allows resume from the latest gen |
| Linux MOD ABI mismatch surfaces after Vast.ai launch | Low | High (blocks the run) | Bootstrap step recompiles MODs with `nrnivmodl` on the Vast.ai instance from source; if compilation fails, halt and create intervention file; t0106 and t0112 both shipped this pattern successfully |
| HV-plateau threshold too tight; seed 2247 runs to `N_GEN = 60` ceiling without plateau | Low | Low (60 gens is well within the $25 cap; reaching the ceiling is itself informative on the plateau-vs-budget tradeoff) | `N_GEN = 60` is a hard ceiling; cost stays within $25 cap; the plateau-not-reached outcome is logged as `hv_plateau_gen: null` in metrics |
| Operator misses HV-plateau window; wall-clock past 6 h | Low | Medium ($5-10 wasted) | `T0113_HARD_BUDGET_USD = 25.00` cap inside `CostWatchdogTermination`; orchestrator pulls `hv_trace.jsonl` periodically; explicit operator-stop mechanism via `intervention/stop.md` |
| `dsi_vector_sum` field name accidentally renamed to `dsi_ratio` during the analysis-module port | Low | Medium (breaks cross-task analysis with t0106 / t0112) | Step 4 diff-check explicitly forbids any change beyond the seed/budget rename in the algorithm tree; the analysis-module port in step 10 reads from the locked `spec_version: "2"` schema, never writes a renamed field |
| Vast.ai preemption mid-run | Low | Medium (loses up to 1 gen progress) | Per-gen `dill` checkpoint enables resume from the latest gen; the JSONL HV trace is append-only |
| Package-path rewrite accidentally edits upstream imports (t0024/t0080/t0090/t0092) | Very low | High (breaks the upstream dependency chain) | Step 2's rewrite is scoped to the exact string `tasks.t0112_t0106_seed77_replicate` -> `tasks.t0113_t0106_seed2247_replicate`; step 4's diff check explicitly verifies upstream import lines are unchanged; REQ-17 has dedicated verification |
| t0106 or t0112 predictions asset comparison fails (file format change) | Very low | Low (charts incomplete) | Both assets are read-only and immutable per project rules; format locked at `spec_version: "2"`; if gzipped JSON fails to decompress, fall back to per-task analysis without the 3-seed chart and document the limitation |
| Project budget envelope insufficient before provisioning | Very low | Blocking | `task_description.md` line 105-106 mandates the envelope check before provisioning; $41.21 remaining vs $25 cap leaves $16.21 reserve at the cap, comfortably positive; if budget drops below $25 between planning and provisioning (other tasks spending), halt and create intervention file |

* * *

## Verification Criteria

Each criterion names the exact command and the expected output.

* **Plan verificator passes.** Command:
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0113_t0106_seed2247_replicate -- uv run python -u -m arf.scripts.verificators.verify_plan t0113_t0106_seed2247_replicate`.
  Expected: 0 errors. Warnings allowed only if reasoned in this plan.

* **The seed and budget renames are present and no other algorithm constants changed (REQ-2, REQ-3,
  REQ-4, REQ-5).** Command:
  `grep -n "T0113_SEEDS: tuple\[int, \.\.\.\] = (2247,)" tasks/t0113_t0106_seed2247_replicate/code/constants.py && grep -n "T0113_HARD_BUDGET_USD: float = 25.00" tasks/t0113_t0106_seed2247_replicate/code/constants.py && grep -n "_POOL_RESTART_EVERY: int = 10" tasks/t0113_t0106_seed2247_replicate/code/nsga2_driver.py && grep -n "N_GEN: int = 60" tasks/t0113_t0106_seed2247_replicate/code/constants_morphology.py`.
  Expected: four matches, one per file.

* **No `T0112_*` constant survives the rename (REQ-2, REQ-3).** Command:
  `grep -n "T0112_" tasks/t0113_t0106_seed2247_replicate/code/constants.py`. Expected: zero lines
  (all renamed to `T0113_*`).

* **No upstream task imports were accidentally edited (REQ-17).** Command:
  `grep -rn "tasks.t0024_\|tasks.t0080_\|tasks.t0090_\|tasks.t0092_\|tasks.t0093_" tasks/t0113_t0106_seed2247_replicate/code/ | wc -l`.
  Expected: the line count matches the equivalent count for t0112's tree (i.e., no upstream imports
  were dropped or added).

* **Smoke gate passed before provisioning (REQ-6).** Command:
  `cat tasks/t0113_t0106_seed2247_replicate/logs/steps/*_implementation/smoke_gate.json` (or
  equivalent log). Expected: JSON object with 5 keys all `"passed": true`. If any `false`, the
  implementation agent must NOT have provisioned the Vast.ai instance; an intervention file must
  exist.

* **HV trace well-formed (REQ-10).** Command:
  `uv run python -c "import json,sys; lines=open(sys.argv[1]).readlines(); [json.loads(l) for l in lines]; print('lines:', len(lines))" tasks/t0113_t0106_seed2247_replicate/logs/steps/*_implementation/hv_trace.jsonl`.
  Expected: prints a line count <= 60; every line parses as JSON with `gen`, `wall_clock_s`, `hv`,
  `n_cells_evaluated`.

* **Predictions asset exists and matches expected cardinality (REQ-11).** Command:
  `uv run python -u -m arf.scripts.aggregators.aggregate_predictions --ids t0113-bedb-morph-nsga2-seed2247 --format json`.
  Expected: one record with `instance_count = 96 * (1 + n_gen_completed)`,
  `predictions_id = "t0113-bedb-morph-nsga2-seed2247"`, `categories` containing
  `direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`.

* **Vast.ai instance destroyed (REQ-15).** Command:
  `uv run python -u -m arf.scripts.verificators.verify_machines_destroyed t0113_t0106_seed2247_replicate`.
  Expected: 0 errors; `destroyed: true` in `machine_log.json`.

* **Cost cap respected (REQ-8 spend half).** Command:
  `uv run python -c "import sys,json; d=json.load(open(sys.argv[1])); assert d['total_usd'] <= 25.0, f'over cap: {d[\"total_usd\"]}'; print('cost ok:', d['total_usd'])" tasks/t0113_t0106_seed2247_replicate/results/costs.json`.
  Expected: total spend <= 25.00.

* **Registered `direction_selectivity_index` metric reported (REQ-12).** Command:
  `uv run python -c "import sys,json; d=json.load(open(sys.argv[1])); vs=d['variants'][0]['metrics']; assert 'direction_selectivity_index' in vs, list(vs); print('dsi:', vs['direction_selectivity_index'])" tasks/t0113_t0106_seed2247_replicate/results/metrics.json`.
  Expected: key present with a float value in [0.0, 1.0].

* **5 charts and 2 tables produced (REQ-13, REQ-14).** Command:
  `ls tasks/t0113_t0106_seed2247_replicate/results/images/*.png | wc -l && ls tasks/t0113_t0106_seed2247_replicate/results/data/*.csv | wc -l`.
  Expected: PNG count >= 5 (including `pareto_front_3seeds.png`, `hv_vs_gen_3seeds.png`,
  `joint_pass_yield_per_gen_3seeds.png`, `top50_morphologies_seed2247.png`,
  `asymmetry_distribution_3seeds.png`); CSV count >= 2 (including `joint_pass_summary_3seeds.csv`,
  `pareto_front_overlap_3seeds.csv`).

* **Random-seed provenance documented (REQ-16).** Command:
  `grep -n "secrets.randbelow" tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/description.md`.
  Expected: at least one line mentioning the random draw via `secrets.randbelow(10000)`.

* **REQ coverage in implementation outputs.** Command:
  `grep -c "REQ-" tasks/t0113_t0106_seed2247_replicate/code/*.py tasks/t0113_t0106_seed2247_replicate/logs/steps/*_implementation/*`.
  Expected: every REQ-1 through REQ-17 referenced at least once across the implementation outputs
  (commit messages, step logs, or code comments where applicable).

* * *

## Alternative Approaches Considered

Documented inline in the Approach section above for traceability:

1. **Run multiple seeds in this single task (e.g., 3 seeds x 25 gens)** — rejected; collapses the
   per-seed cost cap and the per-seed-failure isolation that the t0106 / t0112 / t0113
   single-seed-per-task pattern provides. The S-0112-01 batch runs additional seeds in separate
   parallel tasks.
2. **Pick the seed from a curated low-number candidate set (t0112-style)** — rejected per the task
   brief's explicit motivation (avoid round-ish-low-number selection bias, widen the support beyond
   44-99). Seed 2247 was drawn via `secrets.randbelow(10000)` immediately before task creation.
3. **Disable the HV-plateau stop (S-0112-03 follow-up)** — rejected per the task brief's "out of
   scope" list; a follow-up suggestion will be generated in the reporting stage if t0113 plateaus
   before gen 30 and finds <= 10 joint-pass cells.
4. **Re-evaluate t0106 / t0112 cells at 8 directions (t0107 pattern, S-0112-05)** — rejected as out
   of scope; that is a separate downstream re-evaluation task type. A follow-up suggestion mirroring
   S-0112-05 scoped to t0113 cells will be generated in the reporting stage.
5. **Change the silence guard, DSI metric, or substrate definition** — rejected explicitly per the
   task brief's "out of scope" list. Any evaluator change breaks the like-for-like comparison with
   t0106 / t0112.
6. **Fork from t0106 directly instead of t0112** — rejected per research_code.md "The Patch Surface
   Is Exactly One Constant Rename Plus the Package-Path Rewrite"; t0112 already carries the
   cadence-10 protocol and `N_GEN = 60` ceiling that t0113 needs, so forking from t0112 minimises
   the diff surface to one constant value change plus the package-path rewrite. Forking from t0106
   would require re-applying t0112's cadence and ceiling deltas, doubling the patch surface.
