---
spec_version: "2"
task_id: "t0114_seed7755_no_autostop"
date_completed: "2026-05-20"
status: "complete"
---
# Plan: Seed-7755 NSGA-II Replicate of t0106 Substrate with HV-Plateau Auto-Stop Disabled

## Objective

Re-run the t0106-family long 2-direction NSGA-II on the identical 68-d Bed B electrophys + 14-d
morphology substrate using GA seed **7755** (drawn locally via `secrets.randbelow(10000)` on
2026-05-20 by the implementing agent) under the t0113 cadence-10 protocol, but with the **HV-plateau
auto-stop disabled entirely**. The run is terminated only by (in order of expected firing) explicit
operator stop, the $25 per-task hard budget cap, the $20 per-instance cost watchdog, or the
`N_GEN = 300` ceiling. This task is a minimum-change fork of `t0113_t0106_seed2247_replicate` with
exactly three deltas: (a) `T0113_SEEDS = (2247,)` becomes `T0114_SEEDS = (7755,)`; (b)
`HVPlateauTermination(seed=task_seed)` is removed from the pymoo `TerminationCollection`; (c)
`N_GEN = 60` becomes `N_GEN = 300` (matching t0106's original ceiling). Every other algorithmic knob
— `_POOL_RESTART_EVERY = 10` (the operator-endorsed "10th gen rule"), the ratio DSI metric, the
silence guard, the pop = 96 / N_EVAL_SEEDS = 3 / 2-direction evaluation protocol, the predictions
asset schema, the cost-watchdog wiring — is inherited from t0113 verbatim. The run produces a
fourth substrate-rate datapoint (alongside t0106 seed 44, t0112 seed 77, t0113 seed 2247) and the
first uncensored HV trajectory in the lineage; the offline detector replay over all four seeds ×
(WINDOW ∈ {2, 3, 4, 5}) × (REL_THRESHOLD ∈ {0.005, 0.01}) implements suggestion S-0113-03 and
recommends a new project default. **Done** means: (1) the seed-7755 NSGA-II run terminates cleanly
via one of the four legitimate triggers under the $25 hard cap; (2) one predictions asset
`t0114-bedb-morph-nsga2-seed7755` is produced under `assets/predictions/` mirroring the t0113 schema
(`spec_version: "2"`, gzipped JSON, the five per-cell fields plus `stop_trigger` in
`metrics_at_creation`); (3) `results/metrics.json` records the registered
`direction_selectivity_index` metric plus operational metrics; (4) the 5 task-specified charts and 3
CSV tables are saved to `results/images/` and `results/data/`; (5) the offline detector replay CSV
is produced and `(W*, T*)` recommendation is recorded.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0114_seed7755_no_autostop/task.json` and the resolved long
description at `tasks/t0114_seed7755_no_autostop/task_description.md`:

```text
Name: Seed-7755 NSGA-II replicate of t0106 with auto-stop disabled

Short description: Re-run t0106 NSGA-II substrate with random seed 7755,
_POOL_RESTART_EVERY=10, HV-plateau auto-stop DISABLED; runs to gen ceiling / budget cap.
Implements S-0113-03 live.

Dependencies: t0106_long_pdnd_nsga2_300gen, t0113_t0106_seed2247_replicate.
Expected assets: 1 predictions.
Task types: experiment-run.
Source suggestion: S-0113-03.

Long description (excerpts):

* In scope (unchanged from t0113): substrate (Bed B 54-d electrophys + 14-d morphology = 68
  free parameters), objectives (2-direction ratio DSI + PD-rate at 0 deg), NSGA-II
  hyperparameters (pop=96, SBX/PM operators), evaluation protocol (N_EVAL_SEEDS=3, ratio DSI,
  silence guard active), _POOL_RESTART_EVERY = 10 (the "10th gen rule"), predictions asset
  schema, cost-watchdog wiring, smoke-gate suite.
* In scope, changed from t0113: (1) GA seed 2247 -> 7755 (randomly drawn);
  (2) HV-plateau auto-stop DISABLED (HVPlateauTermination NOT added to pymoo termination
  list); (3) N_GEN = 60 -> 300 (match t0106 original ceiling). Termination triggers are
  operator stop, $25 budget cap, $20 per-instance watchdog, gen 300 ceiling.
* Out of scope: any change to substrate, objective formulation, evaluation protocol, silence
  guard, NSGA-II operator hyperparameters, predictions asset schema, metrics list, or
  _POOL_RESTART_EVERY.
* Fork t0113 code; rewrite package paths (tasks.t0113_t0106_seed2247_replicate ->
  tasks.t0114_seed7755_no_autostop); leave upstream task references (t0024, t0080, t0090,
  t0092, t0093, t0106) untouched.
* Apply three constant patches: constants.py T0113_SEEDS=(2247,) -> T0114_SEEDS=(7755,)
  with companion budget rename; constants_morphology.py N_GEN=60 -> N_GEN=300;
  nsga2_driver.py remove HVPlateauTermination(seed=...) from TerminationCollection.
* Smoke gate locally (5 t0113 checks plus one new check that termination list contains no
  HVPlateauTermination).
* Provision Vast.ai EPYC-class single instance (>=100 GB RAM, idle RTX 3060 Ti, reliability
  >= 0.99, dph <= 0.40, prefer 64-core+ EPYC 7B13 to inherit t0113's 160 s/gen wall-clock).
* Launch with $25 cap and $20 per-instance watchdog.
* Collect 1 predictions asset at
  assets/predictions/t0114-bedb-morph-nsga2-seed7755/ with spec_version "2", gzipped JSON,
  fields generation, vector_68d, objective_F_minimised, dsi_vector_sum (back-compat name
  storing ratio DSI), pd_rate_hz. Required metrics_at_creation keys:
  n_generations_completed, n_cells_total, best_dsi_ratio, best_pd_rate_hz,
  n_joint_pass_unique, n_joint_pass_evaluations, final_hypervolume, final_cost_usd,
  stop_trigger.
* Offline detector replay over WINDOW ∈ {2,3,4,5} x REL_THRESHOLD ∈ {0.005, 0.01} against
  4 seed HV traces; write results/data/detector_replay.csv; pick (W*, T*).
* 5 charts: hv_vs_gen_4seeds.png, pareto_front_4seeds.png,
  joint_pass_yield_per_gen_4seeds.png, detector_replay_heatmap.png,
  top50_morphologies_seed7755.png.
* 3 tables: joint_pass_summary_4seeds.csv, pareto_front_overlap_4seeds.csv,
  detector_replay.csv.
* Registered metrics: direction_selectivity_index (sub-variants best_legit, overall_max,
  dsi_eq_one_count).
* Operator directive 2026-05-20: "don't stop optimisation until I say so" - HVPlateauTermination
  NOT in termination list; operator stop, $25 budget cap, $20 per-instance watchdog, gen 300
  are the only valid stop mechanisms. The "10th gen rule" (_POOL_RESTART_EVERY = 10) stays.
```

Concrete requirements decomposed (each names the step that satisfies it and the proof artefact):

* **REQ-1** — **Verbatim t0113 code fork.** Copy every algorithm-critical Python module from
  `tasks/t0113_t0106_seed2247_replicate/code/` into `tasks/t0114_seed7755_no_autostop/code/`
  (algorithm-critical modules per research_code.md: `__init__.py`, `bootstrap.py`,
  `apply_params.py`, `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`,
  `recorder.py`, `trial_helpers.py`, `generator_wrapper.py`, `cost_watchdog.py`,
  `hv_plateau_watchdog.py`, `evaluator.py`, `constants_electrophys.py`, `anchor_definitions.py`,
  `anchor_classifier.py`, `biological_priors.py`, `biological_scorecard.py`, `nsga2_driver.py`,
  `test_evaluator_dsi_guard.py`, `constants.py`, `constants_morphology.py`, `paths.py`,
  `random_init.py`, `smoke_gate.py`, plus the orchestration shell scripts `run_seed2247.sh` and
  `sync_results_back.sh`). Satisfied by step 1 (copy) and step 2 (import rewrite). Evidence:
  `grep -r "t0113_t0106_seed2247_replicate" tasks/t0114_seed7755_no_autostop/code/` returns zero
  matches; `ls tasks/t0114_seed7755_no_autostop/code/*.py | wc -l` is at least 22 modules.

* **REQ-2** — **GA seed change 2247 -> 7755 (random draw).** `constants.py` declares
  `T0114_SEEDS: tuple[int, ...] = (7755,)` (renamed from `T0113_SEEDS = (2247,)`); the
  backwards-compat aliases (`T0104_SEEDS`, `T0106_SEEDS`) are updated to reference `T0114_SEEDS`;
  the `__all__` export list lists `T0114_SEEDS` (not `T0113_SEEDS`). The value `7755` is recorded in
  `task_description.md` lines 21-24 as drawn via `secrets.randbelow(10000)` on 2026-05-20. Satisfied
  by step 3. Evidence:
  `grep -n "T0114_SEEDS: tuple" tasks/t0114_seed7755_no_autostop/code/constants.py` returns one line
  containing `(7755,)`; `grep -n "T0113_SEEDS" tasks/t0114_seed7755_no_autostop/code/constants.py`
  returns zero lines.

* **REQ-3** — **Budget constant rename (value unchanged).** `T0113_HARD_BUDGET_USD = 25.00`
  becomes `T0114_HARD_BUDGET_USD = 25.00`; `T0113_PER_INSTANCE_WATCHDOG_USD = 20.00` becomes
  `T0114_PER_INSTANCE_WATCHDOG_USD = 20.00`. Values unchanged; only names change. Satisfied by step
  3\. Evidence:
  `grep -n "T0114_HARD_BUDGET_USD: float = 25.00" tasks/t0114_seed7755_no_autostop/code/constants.py`
  returns one line;
  `grep -n "T0114_PER_INSTANCE_WATCHDOG_USD: float = 20.00" tasks/t0114_seed7755_no_autostop/code/constants.py`
  returns one line; `results/data/algorithm_config.json` `"hard_budget_usd"` equals `25.00`.

* **REQ-4** — **HV-plateau auto-stop DISABLED in live termination list.** In
  `nsga2_driver.py:524-529`, remove `HVPlateauTermination(seed=task_seed)` from the
  `TerminationCollection`. Keep the other three entries (`MaximumGenerationTermination`,
  `CostWatchdogTermination`, `OperatorStopTermination`) in the same order. Prepend a comment block
  citing S-0113-03 and the 2026-05-20 user directive ("don't stop optimisation until I say so").
  Refactor the inline construction into a small
  `_build_termination(*, n_max_gen, cost_watchdog, seed, stop_path) -> TerminationCollection` helper
  so the smoke gate (REQ-7) can introspect it without launching a real run. Satisfied by step 3.
  Evidence:
  `grep -n "HVPlateauTermination(seed=" tasks/t0114_seed7755_no_autostop/code/nsga2_driver.py`
  returns zero lines INSIDE `_build_termination` (the import at lines 74-76 remains untouched).

* **REQ-5** — **`HVPlateauTermination` class remains importable.** The class and the pure
  `should_stop(hv_history: list[float]) -> bool` function in `hv_plateau_watchdog.py` are preserved
  verbatim under the new package path so the offline detector replay (REQ-13) can invoke them; the
  smoke gate (REQ-7) can also introspect the import. Satisfied by step 1 (verbatim copy) and step 2
  (package-path rewrite). Evidence:
  `uv run python -c "from tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog import HVPlateauTermination, should_stop; print('ok')"`
  exits 0 and prints `ok`.

* **REQ-6** — **`N_GEN = 60 -> 300` (match t0106 original ceiling).** `constants_morphology.py`
  line 111 is changed from `N_GEN: int = 60` to `N_GEN: int = 300`. The accompanying comment at line
  110 is rewritten to reflect the t0114 directive ("t0114: raise N_GEN to 300 matching t0106's
  original ceiling; HV-plateau auto-stop disabled; budget cap and operator stop are binding."). No
  other knob in `constants_morphology.py` changes — `HV_PLATEAU_REL_THRESHOLD`,
  `HV_PLATEAU_WINDOW`, `HV_PLATEAU_MIN_HV_HISTORY` remain readable so the offline detector replay
  can import them as the current-default reference. Satisfied by step 3. Evidence:
  `grep -n "N_GEN: int = 300" tasks/t0114_seed7755_no_autostop/code/constants_morphology.py` returns
  one line.

* **REQ-7** — **`_POOL_RESTART_EVERY = 10` PRESERVED VERBATIM (operator-endorsed "10th gen
  rule").** `nsga2_driver.py:97` keeps `_POOL_RESTART_EVERY: int = 10` from t0113 verbatim. The
  operator endorsed this constant on 2026-05-20. Satisfied by step 3 (do-not-edit constraint) and
  step 4 (diff verification). Evidence:
  `grep -n "_POOL_RESTART_EVERY: int = 10" tasks/t0114_seed7755_no_autostop/code/nsga2_driver.py`
  returns one line.

* **REQ-8** — **6-check local smoke gate passes before remote provisioning.** All 5 t0113 checks
  (single-eval driver run, ratio DSI synthetic sanity, silence-guard unit tests, pool-restart
  sanity, watchdog wiring) PLUS the new sixth check: the live `TerminationCollection` produced by
  `_build_termination(...)` contains NO `HVPlateauTermination` instance. Implementation: the smoke
  gate calls `_build_termination(...)` directly and asserts
  `not any(isinstance(t, HVPlateauTermination) for t in coll.terminations)`. Satisfied by step 6.
  Evidence: `logs/steps/<step_id>/smoke_gate.json` (or stdout) reports all 6 checks `passed: true`.
  If any check fails, step 7 (provisioning) MUST NOT proceed; an intervention file must be created.

* **REQ-9** — **Vast.ai provisioning matches t0106 / t0112 / t0113 class with EPYC 7B13
  preference.** A single Vast.ai CPU instance is provisioned with the same filter class: EPYC-class
  CPU, >= 100 GB RAM, RTX 3060 Ti or equivalent idle GPU, reliability >= 0.99, dph <= 0.40, EPYC
  family post-filter (`cpu_name LIKE '%EPYC%'`). **Prefer 64-core+ EPYC 7B13** to inherit t0113's
  160 s/gen wall-clock. Satisfied by step 7. Evidence:
  `logs/steps/<step_id>_setup-machines/machine_log.json` records the selected offer; the `cpu_name`
  field contains "EPYC".

* **REQ-10** — **MOD library compiles on the Vast.ai instance.** The 13 `.mod` files from
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` plus the t0024 vendored MODs are SCP'd
  to the instance and compiled with `nrnivmodl`, producing `x86_64/.libs/libnrnmech.so`. The compile
  is handled at runtime by `bootstrap.py:_compile_t0024_mods_linux` plus
  `paths.resolve_t99_mod_library` for the t0080 MODs. Satisfied by step 7. Evidence:
  `logs/steps/<step_id>_setup-machines/mod_compile.log` shows `nrnivmodl` exit 0 and a non-empty
  `libnrnmech.so` listing.

* **REQ-11** — **NSGA-II run terminates ONLY via legitimate triggers (no HV-plateau).** The run
  terminates via exactly one of: (a) `operator_stop` (operator drops `intervention/stop.md`); (b)
  `budget_cap` ($25 cost watchdog); (c) `gen_ceiling` (`N_GEN = 300`); (d) `instance_watchdog` ($20
  per-instance). The trigger identity is recorded in the predictions asset's
  `metrics_at_creation.stop_trigger` field and in `results/data/termination_reason.json`. The
  HVPlateauTermination is explicitly NOT a valid trigger. Satisfied by step 8. Evidence:
  `results/data/termination_reason.json` names one of the four legitimate triggers;
  `logs/steps/<step_id>_implementation/hv_trace.jsonl` line count <= 300.

* **REQ-12** — **Implementation step holds for operator stop.** The implementation subagent
  launches the NSGA-II run on the remote instance, polls `hv_trace.jsonl` periodically (every 5-10
  minutes) to surface progress to the operator, and **explicitly hands control back to the
  orchestrator/operator** before progressing to the teardown step. The operator will decide when to
  stop the run (by writing `intervention/stop.md` or by instructing the orchestrator). If the gen
  300 ceiling or the $25 cap fires before the operator stops, the run ends naturally and the
  subagent proceeds. Satisfied by step 8. Evidence:
  `logs/steps/<step_id>_implementation/monitor_pulls.jsonl` contains >= 1 monitoring entry per 10
  wall-clock minutes; the implementation step log explicitly records the operator-stop
  acknowledgment or the natural-termination event before teardown begins.

* **REQ-13** — **Offline detector replay produces 32-row CSV and `(W*, T*)` recommendation.**
  Write `tasks/t0114_seed7755_no_autostop/code/detector_replay.py` (~60 lines, NEW file) that loads
  the four HV trajectories
  (`tasks/t0106_long_pdnd_nsga2_300gen/results/data/hv_trajectory_seed44.json`,
  `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json`,
  `tasks/t0113_t0106_seed2247_replicate/results/data/hv_trajectory_seed2247.json`,
  `tasks/t0114_seed7755_no_autostop/results/data/hv_trajectory_seed7755.json`), implements a
  `should_stop_with_overrides(hv_history, *, window, rel_threshold, min_history)` helper that
  mirrors the pure function in `hv_plateau_watchdog.py` but reads its constants from arguments,
  iterates over `WINDOW ∈ {2, 3, 4, 5}` and `REL_THRESHOLD ∈ {0.005, 0.01}` for each seed at
  each generation index, and writes `results/data/detector_replay.csv` (32 rows: 4 seeds × 4
  windows × 2 thresholds). Picks `(W*, T*)` such that (a) `gen_at_fire >= 20` on every seed
  (matches Mohacsi 2024 lower bound), (b) `gen_at_fire <= 60` on t0106 (matches the longest
  available natural fire point), and (c) `|WINDOW - 2| + |REL_THRESHOLD - 0.01| / 0.005` is
  minimised among pairs satisfying (a) and (b). Records the recommendation in
  `results/data/detector_replay.csv` (e.g., as a separate "recommended" row or as a sidecar
  `detector_replay_choice.json`). Satisfied by step 9. Evidence:
  `wc -l tasks/t0114_seed7755_no_autostop/results/data/detector_replay.csv` returns at least 33
  lines (32 data + 1 header); `head -1` shows columns
  `seed, WINDOW, REL_THRESHOLD, gen_at_fire, hv_at_fire, hv_at_run_end`.

* **REQ-14** — **Predictions asset format matches t0113 plus `stop_trigger` extension.** Asset
  folder is named `assets/predictions/t0114-bedb-morph-nsga2-seed7755/`. `details.json` has
  `spec_version: "2"`, same five per-cell schema fields as t0106 / t0112 / t0113 (`generation`,
  `vector_68d`, `objective_F_minimised`, `dsi_vector_sum` (back-compat name storing ratio DSI; do
  NOT rename), `pd_rate_hz`), same categories (`direction-selectivity`, `compartmental-modeling`,
  `retinal-ganglion-cell`), same gzipped-JSON file format
  (`files/all_evaluations_seed7755.json.gz`). `instance_count = 96 x (1 + n_gen_completed)`.
  Required `metrics_at_creation` keys per `task_description.md` lines 104-107:
  `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`,
  `stop_trigger` (one of `operator_stop`, `budget_cap`, `gen_ceiling`, `instance_watchdog`). The
  `model_description` records (i) the random-seed provenance (drawn via `secrets.randbelow(10000)`)
  and (ii) the auto-stop deletion. Satisfied by step 10. Evidence:
  `uv run python -u -m arf.scripts.aggregators.aggregate_predictions --ids t0114-bedb-morph-nsga2-seed7755 --format json`
  returns one record with the correct `instance_count`; the predictions verificator passes.

* **REQ-15** — **Registered metric written to `results/metrics.json`.** The registered
  `direction_selectivity_index` metric is reported using the explicit multi-variant metrics format
  (same shape as t0106 / t0112 / t0113 for cross-task comparability) with sub-variants `best_legit`
  (highest non-DSI=1.0 cell), `overall_max` (max ratio DSI across all cells), and `dsi_eq_one_count`
  (number of cells at exactly DSI = 1.0 — these are silence-guard or single-spike artefacts per
  t0106 / t0112 / t0113 reporting). Plus operational metrics (not registered): `joint_pass_count`,
  `best_pd_rate_hz`, `n_cells_evaluated_total`, `n_gen_completed`, `stop_trigger`,
  `efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`. The other
  three registered metrics (`tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`) are NOT measured by this task — t0114 evaluates ratio DSI from 2-direction
  firing, not tuning curves; the omission is deliberate and documented. Training-time efficiency is
  omitted because NSGA-II is not conventional model training. Satisfied by step 11. Evidence:
  `uv run python -c "import json; d=json.load(open('tasks/t0114_seed7755_no_autostop/results/metrics.json')); print(list(d['variants'][0]['metrics']))"`
  lists `direction_selectivity_index` plus the operational keys.

* **REQ-16** — **5 charts produced in `results/images/`.** Per `task_description.md` lines
  131-145: (a) `hv_vs_gen_4seeds.png` (log-scale HV trajectory for all four seeds with pool-restart
  events and would-have-been-auto-stop generations annotated); (b) `pareto_front_4seeds.png` (DSI vs
  PD-rate overlay for seeds 44, 77, 2247, 7755); (c) `joint_pass_yield_per_gen_4seeds.png`
  (joint-pass cell count per generation for all four seeds); (d) `detector_replay_heatmap.png`
  (WINDOW × REL_THRESHOLD heatmap of gen-at-fire per seed); (e) `top50_morphologies_seed7755.png`
  (10x5 grid of best 50 t0114 cells coloured by archetype). All saved as PNG. Satisfied by step 11.
  Evidence: `ls tasks/t0114_seed7755_no_autostop/results/images/*.png | wc -l >= 5` and exact
  filenames match.

* **REQ-17** — **3 summary tables produced in `results/data/`.** Per `task_description.md` lines
  148-156: (a) `joint_pass_summary_4seeds.csv` (per-seed (44, 77, 2247, 7755): total evals,
  joint-pass count, joint-pass %, best DSI, best PD-rate, stop trigger, stop generation); (b)
  `pareto_front_overlap_4seeds.csv` (for each t0114 Pareto cell, nearest-neighbour z-scored L2
  distance in 68-d parameter space to its closest t0106, t0112, and t0113 cells); (c)
  `detector_replay.csv` (32 rows from REQ-13). Satisfied by steps 9 and 11. Evidence: all three CSV
  files exist and parse as pandas DataFrames with the expected columns.

* **REQ-18** — **Random-seed provenance and auto-stop deletion documented in the predictions
  asset.** The predictions asset's `model_description` field and the asset's `description.md`
  mention (i) that GA seed 7755 was drawn via `secrets.randbelow(10000)` on 2026-05-20 by the
  implementing agent and (ii) that HV-plateau auto-stop was disabled per S-0113-03 + the 2026-05-20
  user directive. Both facts are essential for downstream reproducibility. Satisfied by step 10.
  Evidence:
  `grep -n "secrets.randbelow" tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/description.md`
  returns at least one line;
  `grep -n "auto-stop disabled" tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/description.md`
  returns at least one line.

* **REQ-19** — **No edits to upstream task imports.** The imports from `tasks.t0024_*`,
  `tasks.t0080_*`, `tasks.t0090_*`, `tasks.t0092_*`, `tasks.t0093_*`, `tasks.t0106_*` (the upstream
  HV trajectories) remain unchanged (the verificator allows full-path imports of UPSTREAM tasks per
  the Cross-Task Code Reuse Rule). Satisfied by step 2 (rewrite restricted to `t0113` -> `t0114`).
  Evidence:
  `grep -rn "tasks.t0024_\|tasks.t0080_\|tasks.t0090_\|tasks.t0092_\|tasks.t0093_\|tasks.t0106_" tasks/t0114_seed7755_no_autostop/code/`
  returns the same upstream import line set as t0113's tree (no spurious adds or drops).

* * *

## Approach

**Task type recommended**: `experiment-run` (matches `task.json` `task_types: ["experiment-run"]`).
The Planning Guidelines from `meta/task_types/experiment-run/instruction.md` drive the design: fixed
and recorded random seed (GA seed 7755, drawn via `secrets.randbelow(10000)`), per-condition metrics
breakdown in explicit multi-variant `metrics.json` for cross-task comparability with t0106 / t0112 /
t0113, an explicit validation gate (6-step local smoke gate) before any Vast.ai provisioning, cost
tracking against the $25 hard cap, >= 2 charts saved to `results/images/` (this task produces 5 plus
3 CSV tables), predictions asset under `assets/predictions/`. Reproducibility: seed 7755 is the only
stochastic input; the NSGA-II run is deterministic given the seed, the Bed B substrate, the
t0092-patched morphology generator, and the t0080-vendored MOD library.

**Technical approach (grounded in `research/research_code.md` findings).** The entire delta between
t0113 and t0114 lives in three text-level changes plus a global package-path rewrite. Per
research_code.md finding "The Patch Surface Is Three Constants Plus the Package-Path Rewrite":

1. **GA seed 2247 -> 7755 (random draw).** `constants.py` line 63:
   `T0113_SEEDS: tuple[int, ...] = (2247,)` -> `T0114_SEEDS: tuple[int, ...] = (7755,)`. The value
   7755 was drawn locally by `secrets.randbelow(10000)` on 2026-05-20 by the implementing agent
   (recorded in `task_description.md` lines 21-24). Consumed by `random_init.main()` and by
   `run_seed2247.sh` (renamed to `run_seed7755.sh`). Random draw avoids selection bias and widens
   the support beyond the existing 44/77/2247 sample.

2. **HVPlateauTermination REMOVED from live termination list.** `nsga2_driver.py:524-529` currently
   constructs:

   ```python
   termination = TerminationCollection(
       MaximumGenerationTermination(n_max_gen=n_gen_effective),
       HVPlateauTermination(seed=task_seed),
       CostWatchdogTermination(watchdog=cost_watchdog, seed=task_seed),
       OperatorStopTermination(stop_path=stop_signal_md()),
   )
   ```

   becomes (the `HVPlateauTermination(...)` entry is removed entirely; the other three stay verbatim
   and in the same order):

   ```python
   # t0114: HVPlateauTermination removed from termination list per S-0113-03 +
   # user directive 2026-05-20 ("don't stop optimisation until I say so").
   # Auto-stop disabled; termination triggers are max-gen ceiling (N_GEN=300),
   # cost watchdog ($25 cap), per-instance watchdog ($20), and explicit
   # operator stop. The HVPlateauTermination class remains importable from
   # hv_plateau_watchdog.py for offline detector replay (REQ-13).
   termination = TerminationCollection(
       MaximumGenerationTermination(n_max_gen=n_gen_effective),
       CostWatchdogTermination(watchdog=cost_watchdog, seed=task_seed),
       OperatorStopTermination(stop_path=stop_signal_md()),
   )
   ```

   To make the smoke gate's new sixth check inspectable, this construction is refactored into a
   small helper:
   `_build_termination(*, n_max_gen, cost_watchdog, seed, stop_path) -> TerminationCollection`. The
   smoke gate calls the helper and iterates `coll.terminations` asserting no `HVPlateauTermination`
   instance is present. The `HVPlateauTermination` import at lines 74-76 is NOT removed — the
   class stays importable so the offline detector replay (REQ-13) can use it and the smoke gate can
   introspect it.

3. **N_GEN = 60 -> 300.** `constants_morphology.py:111` is changed from `N_GEN: int = 60` to
   `N_GEN: int = 300` (matching t0106's original ceiling). With auto-stop off we want the budget cap
   and explicit operator stop to be the binding constraints, not a tight ceiling. The comment at
   line 110 is rewritten to reflect the t0114 directive.

The cross-task import rule (per `arf/specifications/research_code_specification.md`'s
`Cross-Task Code Reuse Rule`) forbids `tasks.t0113_t0106_seed2247_replicate.code` imports. The
established lineage pattern (t0106 -> t0112 -> t0113 already used it) is verbatim copy with a global
rewrite: `tasks.t0113_t0106_seed2247_replicate` -> `tasks.t0114_seed7755_no_autostop`. Upstream task
imports (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`, `tasks.t0092_*`, `tasks.t0093_*`, plus
the t0106 HV-trajectory absolute path for the replay) stay valid unchanged — the verificator
allows full-path imports of UPSTREAM tasks.

**Predictions asset schema.** Per research_code.md finding "The Predictions Asset Schema Is Locked
at spec_version '2' and Must Be Mirrored Exactly": t0113's
`assets/predictions/t0113-bedb-morph-nsga2-seed2247/details.json` defines `spec_version: "2"` with
per-cell schema fields `generation`, `vector_68d`, `objective_F_minimised`, `dsi_vector_sum` (stores
ratio DSI; name preserved for back-compat with t0102/t0104/t0106/t0112), `pd_rate_hz`. File format
is gzipped JSON (`.json.gz`). t0114 mirrors this exactly with folder name
`t0114-bedb-morph-nsga2-seed7755` (task-brief-specified at `task_description.md` lines 102-104) and
file `files/all_evaluations_seed7755.json.gz`. The `dsi_vector_sum` field name lie (it stores a
2-direction ratio DSI, not a vector-sum DSI) is preserved verbatim: renaming it would break
`cross_seed_analysis.py` and `build_t0113_results.py` (which walk t0106 / t0112 / t0113 / t0114
predictions assets simultaneously). The t0114-specific addition is the `stop_trigger` field in
`metrics_at_creation` — one of `operator_stop`, `budget_cap`, `gen_ceiling`, `instance_watchdog`.

**Cost watchdog.** Per research_code.md finding "Cost-Watchdog and Pool-Restart Wiring Is Inherited
Verbatim": the factory `make_watchdog_from_machine_log` is called in `nsga2_driver.py:487-491` with
`hard_budget_usd=T0113_HARD_BUDGET_USD`. After the global rewrite, this reference becomes
`hard_budget_usd=T0114_HARD_BUDGET_USD` automatically. The legacy `T0104_HARD_BUDGET_USD = 4.00`
default in `cost_watchdog.py:27` MUST be overridden at the driver call site to
`T0114_HARD_BUDGET_USD = 25.00`. Per-instance watchdog: $20.

**Project budget envelope check (user context + task description "Compute and Budget").** Project
`project/budget.json` has `total_budget = $100.0`, `per_task_default_limit = $8.0`. Per the
orchestrator-aggregator output, $59.27 has been spent and **$40.73 remains**. The $25 per-task cap
fits comfortably in the $40.73 remainder ($15.73 reserve at the hard cap). The user explicitly
confirmed: "Budget cap is $25 per task hard. Project budget remaining is $40.73; this task fits
comfortably." Expected actual spend per research_code.md is $2-25 depending on operator stop time;
at t0113's per-gen rate (~$0.01/gen productive) the $25 cap supports ~2400 generations — well
above any plausible stop point. The realistic upper bound is the gen 300 ceiling, which at 160 s/gen
takes ~13 wall-clock hours and ~$5-6 in productive compute.

**Operator hold for the implementation step.** The user directive 2026-05-20 reads "don't stop
optimisation until I say so". The implementation subagent therefore launches the NSGA-II on the
remote, monitors `hv_trace.jsonl` periodically (every 5-10 minutes — pull via SCP or aggregator
query), and **explicitly hands control back to the orchestrator/operator** before progressing to
teardown. The operator will instruct the orchestrator when to stop. If the gen 300 ceiling, the $25
cap, or the $20 per-instance watchdog fires before the operator stops, the run ends naturally and
the subagent proceeds to teardown without further hold. HVPlateauTermination is explicitly NOT a
valid termination trigger and MUST NOT be added back into the termination list under any
circumstances.

**Alternatives considered**:

* **Replicate t0106 directly with auto-stop disabled (skip t0113 fork).** Rejected because
  research_code.md shows the patch surface from t0113 is exactly 3 lines plus the package-path
  rewrite; from t0106 we would also have to re-apply t0112's cadence-10 and the t0113 protocol
  refinements, doubling the surface area for bugs. Forking from t0113 keeps the diff tight.

* **Reduce N_GEN to 100-150 to bound wall-clock without disabling auto-stop.** Rejected because the
  operator directive is explicit: "don't stop optimisation until I say so". A lower ceiling would
  re-introduce a non-operator termination trigger that the directive forbids. The gen 300 ceiling is
  retained only as a final safety net for the case where the operator forgets — and even then, 300
  gens at 160 s/gen × $0.30/h = ~$4, well under the $25 cap.

* **Keep HVPlateauTermination but loosen its constants (e.g., `WINDOW = 5`,
  `REL_THRESHOLD = 0.005`).** Rejected because (a) the task brief forbids any change to the live
  termination beyond removing the HV-plateau entry; (b) S-0113-03 prescribes that the loosened
  constants be *selected* by the offline detector replay (REQ-13), not used live before that
  selection. This task contributes both halves: the uncensored live trace AND the offline replay.

* **Run additional seeds in this task (e.g., 7755 + a backup seed).** Rejected because the S-0112-01
  5-seed batch runs additional seeds in separate parallel tasks per the established lineage
  convention; collapsing multiple seeds into one task removes per-seed cost-cap isolation and
  per-seed failure isolation.

* **Apply a soft "max wall-clock hours" termination as an additional safety net.** Rejected because
  the operator-stop / budget-cap / instance-watchdog trio already covers the cost side, and the gen
  300 ceiling already covers the runaway-progress side. Adding another mechanism violates the
  directive's spirit ("only stop on my say-so or hard safety nets").

**Validation gate**: the 6-check local smoke gate (5 inherited from t0113 plus the new
no-HV-plateau-in-termination-list assertion) is the only gate between local fork and the $20-25
Vast.ai spend. All 6 checks must pass; if any fails, an intervention file is created and
provisioning halted. The single-eval driver run is the expensive operation proxy on Windows (~5 min
wall-clock) and serves as the explicit experiment-run validation gate per the task type Planning
Guidelines.

**Baseline comparisons**: t0106 seed-44 results (123 unique joint-pass cells, best ratio DSI =
1.0000, best PD-rate = 122.62 Hz, final HV = 122.0288, final cost $10.37, 40 gens completed of 300,
HV-plateau auto-stop at gen 40); t0112 seed-77 results (7 unique joint-pass cells, best ratio DSI =
0.9535, best PD-rate = 114.76 Hz, final HV = 107.4602, final cost $1.99, 21 gens completed of 60,
HV-plateau auto-stop at gen 21); t0113 seed-2247 results (0 LEGIT joint-pass cells, 2 silence-guard
DSI=1.0 cells, best legit ratio DSI = 0.3651, best PD-rate = 71.67 Hz, HV-plateau auto-stop at gen
14, cost $0.4773). t0114 results are compared against these in `joint_pass_summary_4seeds.csv` and
the 5 charts. The Hay 2011 (0.40%) and Druckmann 2007 (0.10%) literature joint-pass acceptance-rate
envelope is the substrate-level target for the eventual S-0112-01 5-seed sample; t0114 contributes
the 4th seed.

* * *

## Cost Estimation

* **Vast.ai single CPU instance (EPYC class, RTX 3060 Ti idle, prefer 64-core+ EPYC 7B13)**:
  expected hourly rate ~$0.24-0.36/h (t0113 selected at ~$0.30/h on an EPYC 7B13 64-core instance).
  Expected wall-clock 1-13 h depending on when the operator stops the run. At t0113's observed 160
  s/gen and $0.30/h, the gen 300 ceiling takes ~13.3 wall-clock hours and costs ~$4 productive
  compute; the per-gen cost is ~~$0.013. Productive compute: **~~$0.50-$4** (most likely scenario:
  operator observes HV saturation around gen 50-100 and stops, yielding $1-2 spend).
* **Setup + MOD compilation + idle**: ~30 min at $0.36/h = **$0.18**.
* **Conservative buffer for retries / post-run download**: **$1.00**.
* **No LLM API costs** — all NSGA-II logic runs locally on the Vast.ai instance with no external
  API calls. No paid third-party services beyond Vast.ai compute.
* **Estimated total**: **$2-6 expected** under the operator-stop-around-gen-50-100 scenario; **$25
  hard cap** (per-instance watchdog $20 inside `CostWatchdogTermination`; $25 orchestrator-level
  ceiling via `T0114_HARD_BUDGET_USD`).
* **Project budget context**: `project/budget.json` `total_budget = $100.0`. $59.27 already spent;
  **$40.73 remaining** (confirmed by user 2026-05-20 and by
  `arf.scripts.aggregators.aggregate_costs`). The $25 hard cap fits the remainder comfortably with
  $15.73 reserve after this task at the cap, and ~$35+ reserve at the expected $2-6 spend.
* **Per-task default limit override**: the per-task default in `project/budget.json` is $8; this
  task explicitly overrides to $25 (declared in `task_description.md` "Compute and Budget" section
  and confirmed by the user 2026-05-20). The override is honoured by passing
  `T0114_HARD_BUDGET_USD = 25.00` into `make_watchdog_from_machine_log` at the driver call site.

* * *

## Step by Step

Implementation work only. Orchestrator-managed steps (results writing, suggestions,
compare-literature, reporting) are not in this list per the plan specification.

### Milestone 1: Local Code Fork + Smoke Gate (steps 1-6)

1. **Copy t0113 `code/` verbatim into `tasks/t0114_seed7755_no_autostop/code/`.** Source:
   `tasks/t0113_t0106_seed2247_replicate/code/` (algorithm-critical subset, ~5,800 lines across the
   modules listed in research_code.md "The t0113 Code Tree Has 36 Modules Totalling 9,383 Lines").
   The required algorithm-critical files are: `__init__.py`, `bootstrap.py`, `apply_params.py`,
   `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`, `recorder.py`,
   `trial_helpers.py`, `generator_wrapper.py`, `cost_watchdog.py`, `hv_plateau_watchdog.py`,
   `evaluator.py`, `constants_electrophys.py`, `anchor_definitions.py`, `anchor_classifier.py`,
   `biological_priors.py`, `biological_scorecard.py`, `nsga2_driver.py`,
   `test_evaluator_dsi_guard.py`, `constants.py`, `constants_morphology.py`, `paths.py`,
   `random_init.py`, `smoke_gate.py`, plus the orchestration shell scripts `run_seed2247.sh` (rename
   to `run_seed7755.sh` in step 3) and `sync_results_back.sh`. Analysis modules
   (`build_t0113_results.py`, `cross_seed_analysis.py`, `build_morphology_charts.py`,
   `build_predictions_assets.py`, `make_charts.py`, `metrics_builder.py`, `per_seed_analysis.py`,
   `run_local_analysis.py`, `build_analysis_charts.py`, `build_assets.py`, `build_t0106_plots.py`,
   `build_t0112_results.py`) are deferred to the analysis stage and ported on demand in step 11.
   Inputs: t0113 code directory. Outputs: `tasks/t0114_seed7755_no_autostop/code/` mirror containing
   >= 22 algorithm-critical modules. Expected observable output:
   `ls tasks/t0114_seed7755_no_autostop/code/*.py | wc -l >= 22` and each named file present.
   **Satisfies REQ-1 (groundwork).**

2. **Rewrite package import paths.** In every copied `.py` and `.sh` file, replace
   `tasks.t0113_t0106_seed2247_replicate` with `tasks.t0114_seed7755_no_autostop`. Use a single
   PowerShell pass
   (`(Get-Content -Raw $file) -replace 'tasks\.t0113_t0106_seed2247_replicate', 'tasks.t0114_seed7755_no_autostop' | Set-Content $file -Encoding utf8`)
   across all files, or
   `sed -i 's/tasks\.t0113_t0106_seed2247_replicate/tasks.t0114_seed7755_no_autostop/g'` on the bash
   side. Do NOT touch upstream task references (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`,
   `tasks.t0092_*`, `tasks.t0093_*`, `tasks.t0106_*`, `tasks.t0112_*`) — those are valid as
   full-path imports of UPSTREAM tasks per the Cross-Task Code Reuse Rule. The `paths.py` historical
   docstring drift (mentioning t0102 per research_code.md) is inherited unchanged; only the import
   paths change. Inputs: step 1 output. Outputs: identical structure with corrected imports.
   Expected output:
   `grep -r "t0113_t0106_seed2247_replicate" tasks/t0114_seed7755_no_autostop/code/` returns zero
   matches;
   `grep -r "tasks.t0024_\|tasks.t0080_\|tasks.t0090_\|tasks.t0092_\|tasks.t0093_" tasks/t0114_seed7755_no_autostop/code/`
   still returns the expected upstream imports unchanged. **Satisfies REQ-1, REQ-19.**

3. **[CRITICAL] Apply the three constant patches plus the driver refactor.** Edit three files:

   * **`constants.py`** (118 lines): Line 63: rename `T0113_SEEDS: tuple[int, ...] = (2247,)` to
     `T0114_SEEDS: tuple[int, ...] = (7755,)`. Line 64: rename
     `T0113_HARD_BUDGET_USD: float = 25.00` to `T0114_HARD_BUDGET_USD: float = 25.00` (value
     unchanged). Line 65: rename `T0113_PER_INSTANCE_WATCHDOG_USD: float = 20.00` to
     `T0114_PER_INSTANCE_WATCHDOG_USD: float = 20.00` (value unchanged). Backwards-compat aliases at
     lines 70-75 (`T0104_SEEDS`, `T0104_HARD_BUDGET_PER_SEED_USD`, `T0104_TASK_BUDGET_TOTAL_USD`,
     `T0106_SEEDS`, `T0106_HARD_BUDGET_USD`, `T0106_PER_INSTANCE_WATCHDOG_USD`): update to reference
     the new `T0114_*` constants. Assertion comments at lines 77-79 (if present): update to
     reference `T0114_*`. `__all__` export list at lines 81-118: swap the three `T0113_*` names for
     `T0114_*`. Module docstring at lines 1-28: rewrite to reflect seed 7755, the auto-stop
     deletion, and `N_GEN = 300`.

   * **`constants_morphology.py`** (159 lines): One-line patch at line 111: `N_GEN: int = 60` ->
     `N_GEN: int = 300`. Rewrite the comment at line 110: "t0114: raise N_GEN to 300 matching
     t0106's original ceiling; HV-plateau auto-stop disabled; budget cap and operator stop are
     binding." Do NOT touch `HV_PLATEAU_REL_THRESHOLD`, `HV_PLATEAU_WINDOW`,
     `HV_PLATEAU_MIN_HV_HISTORY` — these remain readable for the offline detector replay (REQ-13).

   * **`nsga2_driver.py`** (734 lines): Refactor the inline `TerminationCollection` construction at
     lines 524-529 into a helper function
     `_build_termination(*, n_max_gen: int, cost_watchdog: CostWatchdog, seed: int, stop_path: Path) -> TerminationCollection`.
     The helper returns:

     ```python
     # t0114: HVPlateauTermination removed from termination list per S-0113-03 +
     # user directive 2026-05-20 ("don't stop optimisation until I say so").
     # Auto-stop disabled; termination triggers are max-gen ceiling (N_GEN=300),
     # cost watchdog ($25 cap), per-instance watchdog ($20), and explicit
     # operator stop. The HVPlateauTermination class remains importable from
     # hv_plateau_watchdog.py for offline detector replay (REQ-13) and the
     # smoke gate (REQ-8).
     return TerminationCollection(
         MaximumGenerationTermination(n_max_gen=n_max_gen),
         CostWatchdogTermination(watchdog=cost_watchdog, seed=seed),
         OperatorStopTermination(stop_path=stop_path),
     )
     ```

     Keep `_POOL_RESTART_EVERY: int = 10` at line 97 VERBATIM (operator-endorsed "10th gen rule"; do
     NOT edit under any circumstances per REQ-7). Keep the `HVPlateauTermination` import at lines
     74-76 VERBATIM (still importable for REQ-5 and REQ-13). Update the caller in
     `run_nsga2_for_seed` to invoke the new helper. Also update `random_init.py:21` import name from
     `T0113_SEEDS` to `T0114_SEEDS` (and any other site referencing `T0113_SEEDS`, e.g. line 96 in
     `main()`). Rename the orchestration script `run_seed2247.sh` to `run_seed7755.sh`; inside the
     script change `SEED=2247` to `SEED=7755`; optionally pass `--n-gen 300` explicitly in the
     launch line; rename `/root/t0113_workdir` -> `/root/t0114_workdir`. Rename
     `sync_results_back.sh` similarly with `t0113_workdir` -> `t0114_workdir` and `tasks.t0113_*` ->
     `tasks.t0114_*`.

   Inputs: step 2 output. Outputs: patched `constants.py`, patched `constants_morphology.py`,
   refactored `nsga2_driver.py`, patched `random_init.py`, renamed orchestration scripts. Expected
   output:
   `grep -n "T0114_SEEDS: tuple\[int, \.\.\.\] = (7755,)" tasks/t0114_seed7755_no_autostop/code/constants.py`
   returns one line;
   `grep -n "T0114_HARD_BUDGET_USD: float = 25.00" tasks/t0114_seed7755_no_autostop/code/constants.py`
   returns one line; `grep -n "T0113" tasks/t0114_seed7755_no_autostop/code/constants.py` returns
   zero lines (all renamed);
   `grep -n "N_GEN: int = 300" tasks/t0114_seed7755_no_autostop/code/constants_morphology.py`
   returns one line;
   `grep -c "HVPlateauTermination(seed=" tasks/t0114_seed7755_no_autostop/code/nsga2_driver.py`
   returns the import line count only (the construction line is gone);
   `grep -n "_POOL_RESTART_EVERY: int = 10" tasks/t0114_seed7755_no_autostop/code/nsga2_driver.py`
   returns one line. **Satisfies REQ-2, REQ-3, REQ-4, REQ-5 (class import preserved), REQ-6,
   REQ-7.**

4. **Verify the diff against t0113 is exactly the intended changes.** Run
   `diff -r tasks/t0113_t0106_seed2247_replicate/code/ tasks/t0114_seed7755_no_autostop/code/`
   (excluding `__pycache__`, `.pyc`, analysis modules not copied, and the `run_seed2247.sh` ->
   `run_seed7755.sh` rename) and confirm the non-mechanical diffs are ONLY: (a) the `T0113_*` ->
   `T0114_*` renames in `constants.py` plus the `(2247,)` -> `(7755,)` value change and the
   docstring rewrite; (b) the `T0113_SEEDS` -> `T0114_SEEDS` import-name change in `random_init.py`;
   (c) the `N_GEN = 60` -> `N_GEN = 300` change plus the comment rewrite in
   `constants_morphology.py`; (d) the HVPlateauTermination removal and `_build_termination` helper
   refactor in `nsga2_driver.py`; (e) the package-path string `t0113_t0106_seed2247_replicate` ->
   `t0114_seed7755_no_autostop` throughout; (f) the `SEED=2247` -> `SEED=7755` and `t0113_workdir`
   -> `t0114_workdir` changes in the renamed orchestration scripts; (g) the new
   `_build_termination(...)` helper invoked from the smoke gate. If unexpected diffs appear, fix
   them before proceeding. Inputs: step 3 output. Outputs: a diff log confirming a tight delta.
   Expected output: the filtered diff contains only the categories (a)-(g) above. **Satisfies
   REQ-19, REQ-4 (driver verification).**

5. **Sanity-import the code package.** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0114_seed7755_no_autostop -- uv run python -c "import tasks.t0114_seed7755_no_autostop.code.constants as c; import tasks.t0114_seed7755_no_autostop.code.constants_morphology as cm; import tasks.t0114_seed7755_no_autostop.code.nsga2_driver; import tasks.t0114_seed7755_no_autostop.code.evaluator; from tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog import HVPlateauTermination, should_stop; assert c.T0114_SEEDS == (7755,), c.T0114_SEEDS; assert c.T0114_HARD_BUDGET_USD == 25.00, c.T0114_HARD_BUDGET_USD; assert cm.N_GEN == 300, cm.N_GEN; print('imports ok')"`.
   Expected: prints `imports ok` and exits 0. If any ImportError or AssertionError, halt and fix
   package paths or constants. **Satisfies REQ-1, REQ-2, REQ-3, REQ-5 (class importable), REQ-6
   (value spot-check).**

6. **[CRITICAL] Run the 6-check local smoke gate (validation gate before remote provisioning).**
   This is the explicit validation gate per the experiment-run task type Planning Guidelines.

   * **Baseline reference**: t0106 / t0112 / t0113 single-cell evaluation in the smoke gate returned
     DSI in `[0, 1]` and PD-rate in `[0, 200] Hz`; anchor-1 bedb_like expected ~43.6 Hz +/- 2 Hz per
     research_code.md "Smoke Gate" section. t0114's smoke gate single-eval must land in the same
     ranges — these are sanity bounds, not the operating point.
   * Run
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0114_seed7755_no_autostop -- uv run python -u -m tasks.t0114_seed7755_no_autostop.code.smoke_gate`.
     Expected: 6 sub-checks all green within ~5 min wall-clock total. The 6 checks per
     `task_description.md` plus the new t0114-specific assertion: (1) single-eval driver run
     completes (DSI in `[0, 1]`, PD-rate in `[0, 200] Hz`, anchor-1 ~43.6 Hz +/- 2 Hz); (2) ratio
     DSI synthetic sanity (PD=5, ND=1 -> 0.6667 +/- 1e-6); (3) silence-guard unit tests pass
     (`SILENCE_SPIKE_COUNT_THRESHOLD = 10` clamps DSI to 0 on a degenerate silent case); (4)
     pool-restart sanity (`_POOL_RESTART_EVERY = 10` reads correctly from the driver module); (5)
     watchdog wiring (`make_watchdog_from_machine_log` returns a `CostWatchdog` with
     `hard_budget_usd = 25.00`); (6) **NEW**: the `TerminationCollection` produced by
     `_build_termination(...)` contains NO `HVPlateauTermination` instance — assert via
     `not any(isinstance(t, HVPlateauTermination) for t in coll.terminations)`.
   * Run
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0114_seed7755_no_autostop -- uv run python -u -m pytest tasks/t0114_seed7755_no_autostop/code/test_evaluator_dsi_guard.py -v`.
     Expected: 0 failures across the silence-guard pytest cases.
   * **Validation failure condition**: if any of the 6 smoke-gate checks fail OR the unit-test suite
     reports any failure (i.e., the smoke-gate result is at or below the t0113 baseline of 5/5 green
     plus the new check), halt — do NOT proceed to step 7 (Vast.ai provisioning). Create
     `intervention/smoke_gate_failed.md` with the specific failure and STOP. Do not blow $20 of
     remote compute on a known-broken pipeline.
   * **Individual-output inspection**: after the smoke gate passes, read at least 5 individual
     cell-evaluation outputs from the smoke-gate stdout (DSI, PD-rate, ND-rate, total spike count
     per anchor cell). Verify each value is in the expected range and the silence-guard zeros out
     DSI on the degenerate cases. Document this inspection in the step log.

   Inputs: step 5 output. Outputs: `logs/steps/<step_id>_implementation/smoke_gate.json` (or
   equivalent) with all six checks `passed: true`. **Satisfies REQ-8.**

### Milestone 2: Remote Provisioning + Run (steps 7-9)

7. **Provision the Vast.ai instance and compile MODs.** Run the `setup-remote-machine` skill via the
   orchestrator. Filters per `task_description.md` "Compute and Budget" section and t0106 / t0112 /
   t0113 precedent: EPYC-class CPU (PREFER AMD EPYC 7B13 64-core+ to inherit t0113's 160 s/gen
   wall-clock; AMD EPYC 7763 acceptable as fallback), >= 100 GB RAM, RTX 3060 Ti or equivalent GPU
   (idle — workload is CPU-only NEURON), reliability >= 0.99, dph (dollars per hour) <= 0.40,
   post-filter for EPYC family (string match `cpu_name LIKE '%EPYC%'`). Record
   `logs/steps/<step_id>_setup-machines/offer_filters.json` and `machine_log.json`.

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

   Inputs: step 6 pass. Outputs: provisioned Vast.ai instance with NEURON, MODs, and t0114 code.
   **Satisfies REQ-9, REQ-10.**

8. **[CRITICAL] Launch the NSGA-II run on the remote instance and HOLD FOR OPERATOR STOP.** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0114_seed7755_no_autostop -- uv run python -u -m tasks.t0114_seed7755_no_autostop.code.nsga2_driver --seed 7755 --n-gen 300 --teardown-on-watchdog`
   (the `--seed 7755` argument is redundant with `T0114_SEEDS = (7755,)` but is included explicitly
   for log traceability; `--n-gen 300` is explicit belt-and-braces for the patched `N_GEN`). The
   driver:

   * Initialises pop = 96 random LHS, `n_eval_seeds = 3`, `n_directions = 2`, seed 7755.

   * Runs the `TerminationCollection` built by `_build_termination(...)`:
     `MaximumGenerationTermination(n_max_gen=300)`, `CostWatchdogTermination(watchdog=$25)`,
     `OperatorStopTermination(stop_signal_md())`. **HVPlateauTermination is NOT in the list
     (verified by smoke check 6).**

   * `_GenerationCallback` writes one JSON line per gen to
     `logs/steps/<step_id>_implementation/hv_trace.jsonl` (fields `gen`, `wall_clock_s`, `hv`,
     `n_cells_evaluated`) and dill-checkpoints the algorithm to `checkpoint_gen<NNNN>.pkl` (note:
     dill checkpointing fails silently each gen per [t0113]'s S-0113-02; JSON-side resume via
     `hv_trajectory_seed7755.json`, `all_evaluations_seed7755.json`,
     `nsga2_checkpoint_seed7755.json` is the operative resume mechanism — non-fatal).

   * `PerGenerationPoolRestart` (instantiated with `restart_every = _POOL_RESTART_EVERY = 10`)
     closes and recreates the `multiprocessing.Pool` every 10 gens, swapping
     `problem.elementwise_runner = StarmapParallelization(pool.starmap)`. At `N_GEN = 300`, this
     yields up to 30 restarts.

   * `_save_algorithm_config` writes `results/data/algorithm_config.json` with
     `pool_restart_every: 10`, `hard_budget_usd: 25.00`, `task_seed: 7755`, `n_gen_target: 300`,
     `hv_plateau_autostop_disabled: true`.

   * **Validation gate (after gen 1)**: pull `hv_trace.jsonl` from the remote instance and verify
     exactly 1 well-formed JSON line with the 4 required fields. **Trivial baseline**: the gen-1 LHS
     init population (96 cells) for a healthy substrate produces HV > 0 (t0106 started at HV =
     0.2015; t0112 started at HV = 0.1156; t0113 started at HV ~0.24). **Failure condition**: if the
     `hv_trace.jsonl` file is empty, contains no parseable JSON, or the gen-1 HV is exactly 0
     (indicating all 96 LHS cells were silenced — pipeline broken), halt and read 5 individual
     cell outputs (DSI, PD-rate, ND-rate, total spike count, parameter vector) before letting the
     run proceed to gen 5.

   * **Per-cell baseline check (after gen 1)**: pull 5 random cells from the predictions log on the
     instance and verify `dsi_ratio in [0, 1]`, `pd_rate >= 0`, `nd_rate >= 0`. **Failure
     condition**: if any cell is out of these ranges, OR if the gen-1 best DSI is above 0.99
     (suspiciously close to the silence-guard ceiling — likely a degenerate-cell artefact), halt
     and read 5 individual cell outputs before letting the run continue.

   * **Operator-stop hold (REQ-12)**: after the gen-1 validation gate passes, the implementation
     subagent enters a monitoring loop:

     * Every 5-10 minutes, SCP `hv_trace.jsonl` from the remote instance and append the latest gen-N
       row to `logs/steps/<step_id>_implementation/monitor_pulls.jsonl`.
     * Surface the per-pull summary (current gen, current HV, HV delta vs previous pull, total cells
       evaluated, current cost from the watchdog) to the orchestrator for the operator's awareness.
     * **Hand control back to the operator/orchestrator** when (a) the operator instructs "stop now"
       via the orchestrator (the subagent writes `intervention/stop.md` on the remote at
       `/root/t0114_workdir/tasks/t0114_seed7755_no_autostop/intervention/stop.md` and waits for the
       next gen boundary), OR (b) the run terminates naturally via `budget_cap`, `gen_ceiling`, or
       `instance_watchdog`. **Do NOT proceed to step 10 (teardown) until one of these events
       occurs.**
     * **HVPlateauTermination MUST NOT be re-added to the termination list** even if HV saturates
       visually in the monitor pulls; the directive is "don't stop optimisation until I say so".

   Inputs: step 7 provisioning + step 6 smoke-gate pass. Outputs: `hv_trace.jsonl`,
   `checkpoint_gen<NNNN>.pkl` files (per-gen, possibly dill-failed but JSON resume works),
   `monitor_pulls.jsonl`, per-cell predictions log on the Vast.ai instance,
   `termination_reason.json` recording the actual `stop_trigger`. Expected runtime: 1-13 h
   wall-clock depending on operator stop time (most likely the operator stops around gen 50-100 if
   HV saturates, yielding 2-5 h wall-clock). Cost $2-25 actual against $25 cap (most likely $2-6
   under the operator-stop-around-gen-50-100 scenario). **Satisfies REQ-4 (driver reads refactored
   helper with HVPlateau removed), REQ-11, REQ-12.**

9. **Build the offline detector replay CSV (REQ-13).** Write
   `tasks/t0114_seed7755_no_autostop/code/detector_replay.py` (~60 lines, NEW file). The script:

   * Loads four HV trajectories using inline `json.loads()` plus
     `[float(t["hypervolume"]) for t in raw["trajectory"]]` projection. Source paths:
     `tasks/t0106_long_pdnd_nsga2_300gen/results/data/hv_trajectory_seed44.json` (40 gens),
     `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json` (21 gens),
     `tasks/t0113_t0106_seed2247_replicate/results/data/hv_trajectory_seed2247.json` (14 gens),
     `tasks/t0114_seed7755_no_autostop/results/data/hv_trajectory_seed7755.json` (this task,
     produced in step 8).

   * Implements
     `should_stop_with_overrides(hv_history: list[float], *, window: int, rel_threshold: float, min_history: int) -> bool`
     by mirroring the pure function in `hv_plateau_watchdog.py:29-50` but reading constants from
     arguments. The reference module-level constants (`HV_PLATEAU_WINDOW = 2`,
     `HV_PLATEAU_REL_THRESHOLD = 0.01`, `HV_PLATEAU_MIN_HV_HISTORY = 60`) are imported from
     `tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog` as the canonical reference
     baseline.

   * For each `(seed, WINDOW, REL_THRESHOLD)` triple in
     `{44, 77, 2247, 7755} x {2, 3, 4, 5} x {0.005, 0.01}` (32 cells), iterates `gen` from `4`
     (relaxed from `HV_PLATEAU_MIN_HV_HISTORY = 60` so the early-firing t0113 trace is captured
     cleanly) through `len(hv_history)`, invoking
     `should_stop_with_overrides(hv_history[:gen], window=WINDOW, rel_threshold=REL_THRESHOLD, min_history=4)`
     and recording the first `gen` at which the function returns True (or `null` if never).

   * Writes `tasks/t0114_seed7755_no_autostop/results/data/detector_replay.csv` (32+ rows: header +
     32 data rows) with columns
     `seed, WINDOW, REL_THRESHOLD, gen_at_fire, hv_at_fire, hv_at_run_end`.

   * Picks `(W*, T*)` such that (a) `gen_at_fire >= 20` on every seed (matches Mohacsi 2024 lower
     bound), (b) `gen_at_fire <= 60` on t0106 (matches the longest available natural fire point),
     (c) `|WINDOW - 2| + |REL_THRESHOLD - 0.01| / 0.005` is minimised among pairs satisfying (a) and
     (b). Records `(W*, T*, justification)` to `results/data/detector_replay_choice.json`.

   * Run:
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0114_seed7755_no_autostop -- uv run python -u -m tasks.t0114_seed7755_no_autostop.code.detector_replay`.
     Expected: prints the chosen `(W*, T*)` pair and exits 0.

   Inputs: step 8's `hv_trajectory_seed7755.json` plus three upstream HV trajectories. Outputs:
   `detector_replay.csv`, `detector_replay_choice.json`. **Satisfies REQ-13, REQ-17 partial
   (detector_replay.csv).**

### Milestone 3: Asset Assembly + Teardown (steps 10-12)

10. **Download artefacts and build the predictions asset.** SCP from the Vast.ai instance to the
    worktree:

    * `logs/steps/<step_id>_implementation/hv_trace.jsonl` (the per-gen HV trace).
    * `results/data/hv_trajectory_seed7755.json` (the per-gen HV trajectory consumed by step 9).
    * All `checkpoint_gen<NNNN>.pkl` files to `logs/steps/<step_id>_implementation/checkpoints/`
      (may be dill-failed per S-0113-02; that is non-fatal).
    * `results/data/algorithm_config.json` (records `pool_restart_every`, `hard_budget_usd`,
      `task_seed`, `n_gen_target`, `hv_plateau_autostop_disabled: true`).
    * `results/data/termination_reason.json` (records the actual `stop_trigger`).
    * The per-cell predictions log (every evaluated cell across all completed gens).

    Build the **predictions asset** at
    `tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/`:

    * **`details.json`**: `spec_version: "2"`, `predictions_id: "t0114-bedb-morph-nsga2-seed7755"`,
      `name: "NSGA-II seed 7755 on 68-d Bed B + 14-d morphology, 2 directions, up-to-300-gen replicate of t0106 with HV-plateau auto-stop disabled"`,
      `model_id: null`,
      `model_description: "Identical to t0113 except (1) GA seed 2247 -> 7755 (drawn via secrets.randbelow(10000) on 2026-05-20 by the implementing agent to widen seed support beyond 44/77/2247); (2) HVPlateauTermination REMOVED from pymoo TerminationCollection per S-0113-03 + 2026-05-20 user directive ('don't stop optimisation until I say so'); termination triggers are operator stop, $25 budget cap, $20 per-instance watchdog, N_GEN=300 ceiling; (3) N_GEN = 60 -> 300 matching t0106's original ceiling. Pool restart cadence 10 ('10th gen rule') preserved verbatim. 68-d Bed B + 14-d morphology substrate, ratio DSI metric, silence guard active, N_EVAL_SEEDS=3."`,
      `dataset_ids: []`, `prediction_format: "json.gz"`,
      `prediction_schema: <copy t0113's schema verbatim, swapping "seed2247" -> "seed7755">`,
      `instance_count = 96 x (1 + n_gen_completed)`,
      `categories: ["direction-selectivity", "compartmental-modeling", "retinal-ganglion-cell"]`,
      `created_by_task: "t0114_seed7755_no_autostop"`, `date_created` = ISO 8601 date.

    * **`description.md`** per `meta/asset_types/predictions/specification.md`, documenting (i) the
      seed/ceiling/HVPlateau changes vs t0113 (no other algorithm changes), (ii) the back-compat
      naming of `dsi_vector_sum` (stores ratio DSI; field name kept for
      t0102/t0104/t0106/t0112/t0113 downstream compatibility), and (iii) the random-seed provenance
      and the auto-stop deletion ("GA seed 7755 was drawn via `secrets.randbelow(10000)` on
      2026-05-20 to widen the support beyond seeds 44/77/2247. HV-plateau auto-stop was disabled per
      S-0113-03 + the 2026-05-20 user directive.").

    * **`files/all_evaluations_seed7755.json.gz`** — gzipped JSON with top-level key `evaluations`
      -> list of per-cell records. Each record: `generation` (int, 1 = LHS init, 2+ = offspring),
      `vector_68d` (list of 68 floats = 54-d electrophys + 14-d morphology), `objective_F_minimised`
      (list of 2 floats = sign-flipped `[-ratio_dsi, -pd_rate_hz]`), `dsi_vector_sum` (float in
      `[0, 1]`, guard-cleaned ratio DSI; field name preserved for back-compat), `pd_rate_hz` (float,
      mean PD firing rate in Hz across the 3 noise replicates). Format identical to t0106's
      `all_evaluations_seed44.json.gz`, t0112's `all_evaluations_seed77.json.gz`, t0113's
      `all_evaluations_seed2247.json.gz`. The 5 MB pre-commit limit is respected via gzip.

    * Required `metrics_at_creation` keys: `n_generations_completed`, `n_cells_total`,
      `best_dsi_ratio`, `best_pd_rate_hz`, `n_joint_pass_unique`, `n_joint_pass_evaluations`,
      `final_hypervolume`, `final_cost_usd`, **`stop_trigger`** (one of `operator_stop`,
      `budget_cap`, `gen_ceiling`, `instance_watchdog`).

    Validation: total record count in the unzipped JSON matches `96 x (1 + n_gen_completed)`.
    **Satisfies REQ-14, REQ-18.**

11. **Compute metrics and produce charts.** Port the t0113 analysis modules
    (`build_t0113_results.py`, `cross_seed_analysis.py`, `build_morphology_charts.py`,
    `build_predictions_assets.py` writer portion, `make_charts.py`, `metrics_builder.py`,
    `per_seed_analysis.py`, `run_local_analysis.py`) into `tasks/t0114_seed7755_no_autostop/code/`
    on demand, adapting them to read FOUR seed sources (t0106 seed 44, t0112 seed 77, t0113 seed
    2247, t0114 seed 7755) instead of three. Rename `build_t0113_results.py` to
    `build_t0114_results.py` and update its read paths to include the t0114 predictions asset
    alongside the t0106 / t0112 / t0113 assets. Write
    `tasks/t0114_seed7755_no_autostop/results/metrics.json` using the explicit multi-variant format
    (per `arf/specifications/metrics_specification.md` and the `experiment-run` task type guidance).
    One variant with `variant_id: "random-init-seed7755-2dir-300gen-no-autostop"`, dimensions
    matching t0113 variant shape plus the no-autostop marker (`task_seed: 7755`,
    `init_method: "lhs_random"`, `n_obj: 2`, `n_directions: 2`, `dsi_metric: "ratio"`,
    `dsi_silence_guard_active: true`, `n_eval_seeds: 3`, `n_generations_target: 300`,
    `n_generations_completed`, `n_cells`, `hv_plateau_autostop_disabled: true`,
    `stop_trigger: <actual>`).

    * Registered metric: `direction_selectivity_index` — best ratio DSI across all evaluated cells
      (`max(dsi_ratio)`). Sub-variants: `best_legit` (highest non-DSI=1.0 cell), `overall_max` (max
      ratio DSI across all cells), `dsi_eq_one_count` (number of cells at exactly DSI = 1.0 —
      silence-guard or single-spike artefacts).
    * Operational metrics (not registered): `joint_pass_count` (cells with
      `dsi_ratio >= 0.5 AND pd_rate_hz >= 30.0`); `best_pd_rate_hz` (mirrors t0106's 122.62 Hz,
      t0112's 114.76 Hz, t0113's 71.67 Hz); `n_cells_evaluated_total`; `n_gen_completed`;
      `stop_trigger`; `final_hypervolume`;
      `efficiency_inference_time_per_item_seconds = total_wall_clock_s / n_cells_evaluated_total`;
      `efficiency_inference_cost_per_item_usd = total_cost_usd / n_cells_evaluated_total`.
      Training-time efficiency is explicitly omitted because NSGA-II is not conventional model
      training. The other three registered metrics (`tuning_curve_hwhm_deg`,
      `tuning_curve_reliability`, `tuning_curve_rmse`) are NOT measured by this task — t0114
      evaluates ratio DSI from 2-direction firing, not tuning curves; the omission is deliberate and
      documented here.

    Generate charts to `tasks/t0114_seed7755_no_autostop/results/images/` per `task_description.md`
    lines 131-145:

    * `hv_vs_gen_4seeds.png` — log-scale HV trajectory for all four seeds (44, 77, 2247, 7755) on
      the same axes with pool-restart events and would-have-been-auto-stop generations annotated
      (apply the current `WINDOW = 2`, `REL_THRESHOLD = 0.01` rule retrospectively to each seed).
      Read t0106's predictions asset at
      `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`,
      t0112's at
      `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz`,
      and t0113's at
      `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz`
      for the comparison data.
    * `pareto_front_4seeds.png` — overlay of strict Pareto fronts from t0106, t0112, t0113, and
      t0114 on DSI vs PD-rate axes; coloured by source task.
    * `joint_pass_yield_per_gen_4seeds.png` — joint-pass cell count discovered per generation
      across all four seeds.
    * `detector_replay_heatmap.png` — heatmap of (WINDOW × REL_THRESHOLD) showing the generation
      at which the detector would have fired on each seed (4 panels, one per seed, with the
      recommended `(W*, T*)` cell highlighted).
    * `top50_morphologies_seed7755.png` — 10x5 grid of best 50 cells from t0114, coloured by
      archetype, matching the format of `top50_morphologies.png` (t0106),
      `top50_morphologies_seed77.png` (t0112), and `top50_morphologies_seed2247.png` (t0113).

    Generate remaining tables to `tasks/t0114_seed7755_no_autostop/results/data/`:

    * `joint_pass_summary_4seeds.csv` — per-seed (44, 77, 2247, 7755): total evals, joint-pass
      count, joint-pass %, best DSI, best PD-rate, stop trigger, stop generation.
    * `pareto_front_overlap_4seeds.csv` — for each t0114 Pareto cell, the nearest-neighbour
      z-scored L2 distance in 68-d parameter space to its closest t0106, t0112, and t0113 cells.

    Inputs: step 10 outputs + t0106 / t0112 / t0113 predictions assets + step 9's
    `detector_replay.csv`. Outputs: `results/metrics.json`, 5 PNG charts, 3 CSV tables. **Satisfies
    REQ-15, REQ-16, REQ-17.**

12. **Teardown the Vast.ai instance.** Run the `setup-remote-machine` skill in teardown mode (or
    call the orchestrator's teardown procedure). Verify destruction within 5 min of the last
    completed gen, operator-stop detection, or watchdog firing. Update
    `logs/steps/<step_id>_teardown/machine_log.json` with `destroyed: true` and a `destroyed_at`
    timestamp. Inputs: step 11 confirms all artefacts pulled. Outputs: `machine_log.json` with
    `destroyed: true`; Vast.ai dashboard confirms instance gone. **Satisfies the post-run teardown
    convention (no specific REQ-* but required by the project's machine-destruction verificator).**

* * *

## Remote Machines

Single Vast.ai CPU instance required. Filters: EPYC-class CPU (PREFER AMD EPYC 7B13 64-core+ to
inherit t0113's 160 s/gen wall-clock; AMD EPYC 7763 acceptable as fallback), >= 100 GB RAM, RTX 3060
Ti or equivalent GPU (idle — workload is CPU-only NEURON), reliability >= 0.99, dph (dollars per
hour) <= 0.40, post-filter for EPYC family (string match `cpu_name LIKE '%EPYC%'`, mirroring
t0104's, t0106's, t0112's, t0113's pattern). Expected hourly rate ~$0.24-0.36/h. Estimated
wall-clock: 1-13 h depending on operator stop time (most likely 2-5 h if the operator stops around
gen 50-100; full 300-gen ceiling at 160 s/gen = 13.3 h). Cost cap: $25 total ($20 per-instance
watchdog enforced inside `CostWatchdogTermination`; $25 orchestrator-level ceiling via
`T0114_HARD_BUDGET_USD`). Teardown within 5 min of operator stop, watchdog firing, or ceiling
completion. Reference: `arf/specifications/remote_machines_specification.md`.

* * *

## Assets Needed

* **Code substrate from t0113** (dependency `t0113_t0106_seed2247_replicate`): the entire
  algorithm-critical `code/` subset copied verbatim with package-path rewrite, and three text- level
  patches per the patch table in Approach (seed value `(2247,)` -> `(7755,)`, three `T0113_*` ->
  `T0114_*` renames, `N_GEN = 60` -> `N_GEN = 300`, HVPlateauTermination removal from
  `TerminationCollection`). t0113 is the canonical fork base (not t0106 / t0112 directly) because
  t0113 already carries the cadence-10 protocol that this task preserves verbatim.
* **t0106 predictions asset for 4-seed comparison charts and tables** (dependency
  `t0106_long_pdnd_nsga2_300gen`):
  `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`.
  Read-only; used by step 11 to build the 4-seed charts and tables.
* **t0106 HV-trajectory JSON for offline detector replay** (dependency
  `t0106_long_pdnd_nsga2_300gen`):
  `tasks/t0106_long_pdnd_nsga2_300gen/results/data/hv_trajectory_seed44.json`. Read-only; used by
  step 9.
* **t0112 predictions asset for 4-seed comparison charts and tables** (transitive dependency via
  t0113):
  `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz`.
  Read-only.
* **t0112 HV-trajectory JSON for offline detector replay**:
  `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json`. Read-only.
* **t0113 predictions asset for 4-seed comparison charts and tables** (dependency
  `t0113_t0106_seed2247_replicate`):
  `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz`.
  Read-only.
* **t0113 HV-trajectory JSON for offline detector replay**:
  `tasks/t0113_t0106_seed2247_replicate/results/data/hv_trajectory_seed2247.json`. Read-only.
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
  `tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/` containing
  every evaluated cell across all completed generations of the seed-7755 run. Each cell record
  carries the 68-d parameter vector (`vector_68d`), the NSGA-II minimised objective vector
  (`objective_F_minimised = [-ratio_dsi, -pd_rate_hz]`), the ratio DSI (`dsi_vector_sum`; field name
  preserved for t0102/t0104/t0106/t0112/t0113 back-compat), `pd_rate_hz`, and the generation index
  (`generation`). Format: gzipped JSON. Total record count: exactly `96 x (1 + n_gen_completed)`.
  Required `metrics_at_creation` keys per `task_description.md` lines 104-107:
  `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`,
  `stop_trigger` (one of `operator_stop`, `budget_cap`, `gen_ceiling`, `instance_watchdog`). The
  `model_description` field records (a) the random-seed provenance (drawn via
  `secrets.randbelow(10000)` on 2026-05-20) and (b) the auto-stop deletion (per S-0113-03 +
  2026-05-20 user directive).

* * *

## Time Estimation

* Research (already complete): research_code only; ~1 h logged in
  `logs/steps/<step_id>_research-code/`.
* Planning (this step): 0.5 h.
* Local code fork + import rewrite + constant patch + driver refactor (Milestone 1, steps 1-5):
  **0.5-1 h** (~5,800 lines copied, single `sed`/PowerShell rewrite, single-file constant edits,
  driver refactor for the smoke-gate helper, script rename).
* Local smoke gate (Milestone 1, step 6): **0.5 h** (6 checks on Windows including NEURON
  single-cell eval; ~5 min wall-clock total for the gate).
* Vast.ai provisioning + MOD compilation (Milestone 2, step 7): **0.5-1 h**.
* NSGA-II run (step 8): **1-13 h** wall-clock depending on when the operator stops the run (most
  likely 2-5 h if the operator stops around gen 50-100 after observing HV saturation; upper bound is
  the gen 300 ceiling at 160 s/gen = 13.3 h). The implementation subagent monitors every 5-10
  minutes and explicitly hands control to the operator/orchestrator before proceeding to teardown.
* Offline detector replay (step 9): **0.25 h** (~60-line script; pure-Python list manipulation; no
  NEURON or pymoo invocation).
* Asset assembly + metrics + charts (Milestone 3, steps 10-11): **1-2 h** (analysis-module port from
  t0113 to read four seed sources is the main work; the actual chart/table compute is small).
* Teardown (step 12): **0.1 h**.
* **Total wall-clock envelope: 4-18 h** (matches expected actual cost of $2-25 at the t0113 per-hour
  rate; envelope is dominated by the NSGA-II run itself which is operator-stop-bounded).

* * *

## Risks & Fallbacks

**Pre-mortem**: if t0114 has failed completely at completion time, the most likely failure modes
are: (a) the operator forgets to issue the stop signal and the gen 300 ceiling fires later than
expected, blowing wall-clock past 13 h — non-fatal because the gen 300 ceiling is the explicit
designed safety net per `task_description.md` lines 207-210; (b) seed 7755 yields 0 LEGIT joint-pass
cells (the substrate-density-is-seed-dependent reading from t0113 hardens — still publishable as
the fourth S-0112-01 point); (c) the smoke-gate "no HV-plateau in termination list" check fails
silently (e.g., the refactor accidentally leaves a stale `HVPlateauTermination` construction outside
the helper) — would let auto-stop fire on the remote, violating the user directive; (d) Vast.ai
instance is interrupted mid-run — non-fatal because the JSON-side resume channel via
`hv_trajectory_seed7755.json`, `all_evaluations_seed7755.json`, `nsga2_checkpoint_seed7755.json` is
fully functional (t0113's S-0113-02 captures the dill checkpoint failure as a known non-fatal); (e)
a silence-guard cell dominates HV growth at some late generation, distorting the offline detector
replay — mitigated by reporting both raw HV and silence-guard-stripped HV in the replay CSV; (f)
the package-path rewrite accidentally edits an upstream import
(t0024/t0080/t0090/t0092/t0093/t0106/t0112), breaking the cross-task dependency chain; (g)
`dsi_vector_sum` schema field rename slips into the code (silently breaking back-compat with t0106 /
t0112 / t0113 analysis modules); (h) cadence-10 wall-clock drifts past gen 60 (untested at run
lengths beyond t0106's 40-gen extent; per research_code.md "Cadence-10 Pool Restart Is Robust at
Long Run Lengths" the protocol is expected stable but t0114 is the first task to exercise it past 60
gens).

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Operator forgets to stop; run goes to gen 300 / $25 cap unattended | Medium | Low (acceptable per task brief — gen 300 ceiling and $25 cap are the designed safety nets for the "stop when I say so" directive) | $25 hard cap inside `CostWatchdogTermination`; gen 300 ceiling in `MaximumGenerationTermination`; the unattended-completion outcome is logged with `stop_trigger: gen_ceiling` or `stop_trigger: budget_cap` |
| Seed 7755 produces 0 LEGIT joint-pass cells (substrate density seed-dependent) | Medium | Low (still publishable as the fourth S-0112-01 point; widens the dispersion estimator) | Run cost is bounded by the operator-stop / cap mechanism; the 4-seed dispersion (44=123, 77=7, 2247=0/2 guard, 7755=N) is itself the headline finding regardless of N |
| Smoke-gate check 6 (no HV-plateau in termination list) silently regresses on a future edit | Low | High (auto-stop fires on the remote, violating the user directive) | Step 6 explicitly asserts the live `TerminationCollection` produced by `_build_termination(...)` contains no `HVPlateauTermination` instance; if the assertion fails, halt before provisioning; the refactor to a single helper function localises the construction site, eliminating the risk of stale duplicates |
| Vast.ai preemption mid-run | Low | Medium (loses up to 1 gen progress) | JSON-side resume channel (`hv_trajectory_seed7755.json`, `all_evaluations_seed7755.json`, `nsga2_checkpoint_seed7755.json`) is the operative resume mechanism per t0113's S-0113-02; the dill checkpoint failure is known non-fatal; the orchestration shell script supports resume by re-launching with the latest gen index |
| Silence-guard cell dominates HV growth at some late generation, distorting offline replay | Low | Medium (skews `(W*, T*)` selection) | Report both raw HV and silence-guard-stripped HV in the replay CSV (add a `hv_stripped_silence_guard` column); pick `(W*, T*)` using the stripped trajectory; document the dual reporting in `detector_replay_choice.json` |
| Linux MOD ABI mismatch surfaces after Vast.ai launch | Low | High (blocks the run) | Bootstrap step recompiles MODs with `nrnivmodl` on the Vast.ai instance from source; if compilation fails, halt and create intervention file; t0106 / t0112 / t0113 all shipped this pattern successfully |
| Cadence-10 wall-clock drifts past gen 60 (archive size growth slowing the evaluator) | Low | Low (extends wall-clock; cost still bounded by $25 cap) | Monitor pulls (step 8) record per-gen wall-clock; if per-gen time more than doubles compared to gen 1-20, operator is alerted and can stop the run early; `_POOL_RESTART_EVERY = 10` remains the load-bearing memory mitigation |
| Package-path rewrite accidentally edits upstream imports (t0024/t0080/t0090/t0092/t0093/t0106/t0112) | Very low | High (breaks the upstream dependency chain) | Step 2's rewrite is scoped to the exact string `tasks.t0113_t0106_seed2247_replicate` -> `tasks.t0114_seed7755_no_autostop`; step 4's diff check explicitly verifies upstream import lines are unchanged; REQ-19 has dedicated verification |
| `dsi_vector_sum` field name accidentally renamed during the analysis-module port | Low | Medium (breaks cross-task analysis with t0106 / t0112 / t0113) | Step 4 diff-check forbids any change beyond the listed patches in the algorithm tree; the analysis-module port in step 11 reads from the locked `spec_version: "2"` schema, never writes a renamed field |
| Project budget envelope insufficient before provisioning | Very low | Blocking | `task_description.md` line 123-124 mandates the envelope check before provisioning; $40.73 remaining vs $25 cap leaves $15.73 reserve at the cap, comfortably positive; if budget drops below $25 between planning and provisioning (other tasks spending), halt and create intervention file |
| t0106/t0112/t0113 predictions asset comparison fails (file format change) | Very low | Low (charts incomplete) | All three assets are read-only and immutable per project rules; format locked at `spec_version: "2"`; if gzipped JSON fails to decompress, fall back to per-task analysis and document the limitation |

* * *

## Verification Criteria

Each criterion names the exact command and the expected output.

* **Plan verificator passes.** Command:
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0114_seed7755_no_autostop -- uv run python -u -m arf.scripts.verificators.verify_plan t0114_seed7755_no_autostop`.
  Expected: 0 errors. Warnings allowed only if reasoned in this plan.

* **The seed, budget rename, ceiling change, HVPlateau removal, and pool-restart preservation are
  all present (REQ-2, REQ-3, REQ-4, REQ-6, REQ-7).** Command:
  `grep -n "T0114_SEEDS: tuple\[int, \.\.\.\] = (7755,)" tasks/t0114_seed7755_no_autostop/code/constants.py && grep -n "T0114_HARD_BUDGET_USD: float = 25.00" tasks/t0114_seed7755_no_autostop/code/constants.py && grep -n "_POOL_RESTART_EVERY: int = 10" tasks/t0114_seed7755_no_autostop/code/nsga2_driver.py && grep -n "N_GEN: int = 300" tasks/t0114_seed7755_no_autostop/code/constants_morphology.py`.
  Expected: four matches, one per file.

* **No `T0113_*` constant survives the rename (REQ-2, REQ-3).** Command:
  `grep -n "T0113_" tasks/t0114_seed7755_no_autostop/code/constants.py`. Expected: zero lines (all
  renamed to `T0114_*`).

* **HVPlateauTermination is not in the live termination collection but is still importable (REQ-4,
  REQ-5).** Command:
  `uv run python -c "from tasks.t0114_seed7755_no_autostop.code.nsga2_driver import _build_termination; from tasks.t0114_seed7755_no_autostop.code.hv_plateau_watchdog import HVPlateauTermination; from unittest.mock import MagicMock; coll = _build_termination(n_max_gen=300, cost_watchdog=MagicMock(), seed=7755, stop_path=MagicMock()); assert not any(isinstance(t, HVPlateauTermination) for t in coll.terminations), 'HVPlateauTermination present in live termination list'; print('ok')"`.
  Expected: prints `ok` and exits 0.

* **No upstream task imports were accidentally edited (REQ-19).** Command:
  `grep -rn "tasks.t0024_\|tasks.t0080_\|tasks.t0090_\|tasks.t0092_\|tasks.t0093_\|tasks.t0106_\|tasks.t0112_" tasks/t0114_seed7755_no_autostop/code/ | wc -l`.
  Expected: the line count matches the equivalent count for t0113's tree plus the new t0106 / t0112
  / t0113 HV-trajectory absolute path references in `detector_replay.py` (i.e., no upstream imports
  were dropped; new ones may be added in `detector_replay.py`).

* **Smoke gate passed before provisioning (REQ-8).** Command:
  `cat tasks/t0114_seed7755_no_autostop/logs/steps/*_implementation/smoke_gate.json` (or equivalent
  log). Expected: JSON object with 6 keys all `"passed": true`. If any `false`, the implementation
  agent must NOT have provisioned the Vast.ai instance; an intervention file must exist.

* **HV trace well-formed and termination is via a legitimate trigger (REQ-11).** Command:
  `uv run python -c "import json,sys; lines=open(sys.argv[1]).readlines(); [json.loads(l) for l in lines]; print('lines:', len(lines))" tasks/t0114_seed7755_no_autostop/logs/steps/*_implementation/hv_trace.jsonl && uv run python -c "import json; d=json.load(open('tasks/t0114_seed7755_no_autostop/results/data/termination_reason.json')); assert d['stop_trigger'] in {'operator_stop', 'budget_cap', 'gen_ceiling', 'instance_watchdog'}, d; print('trigger ok:', d['stop_trigger'])"`.
  Expected: prints a line count <= 300; every line parses as JSON; stop trigger is one of the four
  legitimate values.

* **Monitor pulls evidence the operator-stop hold (REQ-12).** Command:
  `wc -l tasks/t0114_seed7755_no_autostop/logs/steps/*_implementation/monitor_pulls.jsonl`.
  Expected: at least 1 row per ~10 minutes of run wall-clock (e.g., a 2-h run yields >= 12 rows).

* **Offline detector replay CSV exists and has 32 data rows (REQ-13).** Command:
  `uv run python -c "import csv; rows=list(csv.DictReader(open('tasks/t0114_seed7755_no_autostop/results/data/detector_replay.csv'))); assert len(rows) >= 32, len(rows); seeds={r['seed'] for r in rows}; assert seeds == {'44', '77', '2247', '7755'} or seeds == {44, 77, 2247, 7755}, seeds; print('replay ok:', len(rows), 'rows', seeds)"`.
  Expected: prints `replay ok: 32 rows {44, 77, 2247, 7755}` (or equivalent string forms).

* **Predictions asset exists and matches expected cardinality (REQ-14, REQ-18).** Command:
  `uv run python -u -m arf.scripts.aggregators.aggregate_predictions --ids t0114-bedb-morph-nsga2-seed7755 --format json`.
  Expected: one record with `instance_count = 96 * (1 + n_gen_completed)`,
  `predictions_id = "t0114-bedb-morph-nsga2-seed7755"`, `categories` containing
  `direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`. Additionally,
  `grep -n "secrets.randbelow\|auto-stop disabled" tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/description.md`
  returns at least two matching lines.

* **Cost cap respected.** Command:
  `uv run python -c "import sys,json; d=json.load(open(sys.argv[1])); assert d['total_usd'] <= 25.0, f'over cap: {d[\"total_usd\"]}'; print('cost ok:', d['total_usd'])" tasks/t0114_seed7755_no_autostop/results/costs.json`.
  Expected: total spend <= 25.00.

* **Registered `direction_selectivity_index` metric reported (REQ-15).** Command:
  `uv run python -c "import sys,json; d=json.load(open(sys.argv[1])); vs=d['variants'][0]['metrics']; assert 'direction_selectivity_index' in vs, list(vs); print('dsi:', vs['direction_selectivity_index'])" tasks/t0114_seed7755_no_autostop/results/metrics.json`.
  Expected: key present with a float value in [0.0, 1.0].

* **5 charts and 3 tables produced (REQ-16, REQ-17).** Command:
  `ls tasks/t0114_seed7755_no_autostop/results/images/*.png | wc -l && ls tasks/t0114_seed7755_no_autostop/results/data/*.csv | wc -l`.
  Expected: PNG count >= 5 (including `hv_vs_gen_4seeds.png`, `pareto_front_4seeds.png`,
  `joint_pass_yield_per_gen_4seeds.png`, `detector_replay_heatmap.png`,
  `top50_morphologies_seed7755.png`); CSV count >= 3 (including `joint_pass_summary_4seeds.csv`,
  `pareto_front_overlap_4seeds.csv`, `detector_replay.csv`).

* **Vast.ai instance destroyed.** Command:
  `uv run python -u -m arf.scripts.verificators.verify_machines_destroyed t0114_seed7755_no_autostop`.
  Expected: 0 errors; `destroyed: true` in `machine_log.json`.

* **REQ coverage in implementation outputs.** Command:
  `grep -c "REQ-" tasks/t0114_seed7755_no_autostop/code/*.py tasks/t0114_seed7755_no_autostop/logs/steps/*_implementation/*`.
  Expected: every REQ-1 through REQ-19 referenced at least once across the implementation outputs
  (commit messages, step logs, or code comments where applicable).

* * *

## Alternative Approaches Considered

Documented inline in the Approach section above for traceability:

1. **Replicate t0106 directly with auto-stop disabled (skip t0113 fork)** — rejected; forking from
   t0113 keeps the patch surface to 3 lines plus the package-path rewrite; from t0106 we would also
   have to re-apply t0112's cadence-10 and the t0113 protocol refinements.
2. **Reduce N_GEN to 100-150 to bound wall-clock without disabling auto-stop** — rejected; the
   operator directive forbids any non-operator termination trigger beyond the hard safety nets
   (budget cap, instance watchdog, gen ceiling).
3. **Keep HVPlateauTermination but loosen its constants** — rejected; S-0113-03 prescribes that
   the loosened constants be *selected* by the offline detector replay, not used live before that
   selection. This task contributes both halves.
4. **Run additional seeds in this task (e.g., 7755 + a backup seed)** — rejected; the S-0112-01
   5-seed batch runs additional seeds in separate parallel tasks per the established lineage
   convention.
5. **Apply a soft "max wall-clock hours" termination as an additional safety net** — rejected; the
   operator-stop / budget-cap / instance-watchdog trio plus the gen 300 ceiling already covers all
   safety-net cases.
