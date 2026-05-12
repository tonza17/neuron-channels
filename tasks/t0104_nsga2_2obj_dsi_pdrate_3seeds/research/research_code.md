---
spec_version: "1"
task_id: "t0104_nsga2_2obj_dsi_pdrate_3seeds"
research_stage: "code"
tasks_reviewed: 9
tasks_cited: 8
libraries_found: 2
libraries_relevant: 2
date_completed: "2026-05-12"
status: "complete"
---
# Research Code: 2-Objective NSGA-II Fork of t0102 with DSI Silence Guard

## Task Objective

t0104 forks the t0102 [t0102] 68-d Bed B + morphology NSGA-II substrate verbatim with three surgical
changes: drop the robustness objective (`n_obj` 3 -> 2, keep DSI vector-sum + PD-rate), bump GA
seeds from 2 (44, 55) to 3 (44, 55, 66), and patch `_vector_sum_dsi` / `_summarise_trials` so DSI
returns 0.0 when total spike count across the 16 directions is < 10 (suggestion S-0102-01). The
project keeps `N_EVAL_SEEDS = 4`, `n_gen = 20`, `pop = 96`, random-LHS init. This code research
audits the exact lines in `evaluator.py`, `nsga2_driver.py`, and `cost_watchdog.py` that t0104 must
modify, plus reusable analysis utilities from t0086 [t0086] and the post-patch morphology generator
from t0093 [t0093].

## Library Landscape

The repository does not currently expose `aggregate_libraries.py` under `arf/scripts/aggregators/`
(only `aggregate_categories`, `aggregate_costs`, `aggregate_machines`, `aggregate_metric_results`,
`aggregate_metrics`, `aggregate_suggestions`, `aggregate_task_types`, `aggregate_tasks` are
registered). Library asset metadata was therefore read directly from each task's
`assets/library/<id>/details.json`. The two libraries relevant to t0104 are identical to those
identified by t0102's own research_code.md and are reached transitively via the t0102 substrate
imports.

* `de_rosenroll_2026_dsgc` (v0.1.0) — Created by t0024 [t0024]. NEURON HOC template, compiled MOD
  library (`nrnmech.dll` on Windows / `libnrnmech.so` on Linux), and Python driver for the Bed B
  compartmental DSGC. Entry points: `build_dsgc_cell`, `run_tuning_curve`, `score_envelope`. Module
  paths under `tasks/t0024_port_de_rosenroll_2026_dsgc/code/`. Loaded by t0102's `bootstrap.py`
  (Linux monkey-patching) and reused unmodified by t0104.

* `procedural_dsgc_morphology_generator` (v0.1.0) — Created by t0090 [t0090]. Provides
  `MorphologyParams`, `MorphologyResult`, `generate_morphology`, `BEDB_BASE_POINT`, `PARAM_BOUNDS`,
  `INT_PARAM_NAMES`. **Replaced** by C-0093-01 with `procedural_dsgc_morphology_generator_fix`
  (t0092) which provides `generate_fixed_morphology` + `insert_baseline_channels`. The fix patches
  the soma-pt3d collapse bug that produced NaN voltages under the t0083 best-cell electrophys
  vector. t0102's `generator_wrapper.py` lines 25-30 import directly from
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix` so the corrected
  state is what the t0104 fork will see.

Both libraries are relevant. No other library asset in the project touches t0104.

## Architecture Overview

t0102's code tree is the substrate to fork. The dependency graph relevant to t0104 is:

```text
t0104/code/  ->  copies of t0102/code/{evaluator, nsga2_driver, cost_watchdog,
                                       generator_wrapper, smoke_gate, paths,
                                       constants*, anchor_classifier, ...}
                         |
                         +--> tasks.t0090_*.code.morphology_params       (library)
                         +--> tasks.t0092_*.code.morphology_generator_fix (library)
                         +--> tasks.t0092_*.code.baseline_channels       (library)
                         +--> tasks.t0024_*.code.build_cell              (library)
```

The 68-d vector is split `[54 electrophys | 14 morphology]`. Per-cell evaluation: a worker process
caches one cell keyed on the 14-d morphology hash; on electrophys-only change the cell is reused and
only `apply_parameter_vector` re-runs. NSGA-II uses `pymoo` with `StarmapParallelization` fanning
out to `multiprocessing.Pool(processes=min(60, cpu_count()-4))`. Each generation runs
`pop_size * N_EVAL_SEEDS * n_directions = 96 * 4 * 16 = 6144` trials.

## Key Findings

### Exact patch sites in `evaluator.py` (480 lines)

`tasks/t0102_seedscale_n4_gen20/code/evaluator.py` requires three structurally distinct edits to
implement the S-0102-01 silence guard, drop the robustness component from the F-row returned to
pymoo, and update `n_obj`. The function-level layout was confirmed by reading the file end-to-end
[t0102].

* **Silence guard — `_vector_sum_dsi` (lines 266-287)**: This is the canonical DSI calculator.
  Today it returns 0.0 only when `total_spikes_f <= 1e-12` (line 285). The S-0102-01 fix must add a
  second early-return when total spike count is below the silence threshold. Two viable
  implementation sites:
  * Inside `_vector_sum_dsi` itself: after the `total_spikes_f += mean_count` accumulator loop (line
    284), insert `if total_spikes_f < SILENCE_SPIKE_COUNT_THRESHOLD: return 0.0` (threshold = 10.0
    per S-0102-01 description). This is the lowest-touch site because every caller of
    `_vector_sum_dsi` (the cell-level call at line 325 and the per-seed call at line 332) inherits
    the guard automatically.
  * Inside `_summarise_trials` (lines 290-355): after `spike_counts_per_dir` is fully built (line
    308 in the loop body) and before line 325 (`dsi_vector_sum = _vector_sum_dsi(...)`), compute the
    total spike count across directions and either skip the DSI call or short-circuit
    `dsi_vector_sum = 0.0`. This is the safer site if the same `_vector_sum_dsi` helper is reused by
    analysis code that should NOT see the guard (e.g., post-hoc raw-DSI scatter plots).
    Recommendation: implement at the **`_summarise_trials` site** so the per-seed robustness DSI
    computation at line 332 continues to use raw `_vector_sum_dsi` (the per-seed counts are by
    construction < 16 per direction so always tiny, and adding a guard there would silently force
    most per-seed DSIs to 0). Add a `SILENCE_SPIKE_COUNT_THRESHOLD = 10` constant near the top of
    `evaluator.py` (next to the `_WORKER_*` globals at lines 105-108) and document it in
    `code/test_evaluator_dsi_guard.py` (REQ planned in task_description.md).

* **F-row drop in `BedBV3MorphProblem._evaluate` (lines 466-480)**: The 3-element F-row is
  constructed at **line 471**:
  `out["F"] = np.array([-result.dsi_vector_sum, -result.pd_rate_hz, -result.robustness], dtype=np.float64)`
  and the failure fallback at **line 477**:
  `out["F"] = np.array([-WORST_CASE_DSI, -WORST_CASE_PD_RATE_HZ, -WORST_CASE_ROBUSTNESS], ...)`.
  Both must drop the third entry. `CellEvalResult.robustness` (declared in the dataclass at line 95)
  must remain populated by `_summarise_trials` (lines 335-344) so the predictions assets still log
  it for analysis as required by the task brief; only the pymoo F-row changes.

* **`n_obj` declaration in `BedBV3MorphProblem.__init__` (lines 448-463)**: The keyword dict at
  **line 455** sets `"n_obj": 3`. Change to `"n_obj": 2`. `n_var`, `n_ieq_constr`, `xl`, `xu` are
  unchanged.

### Exact patch site in `nsga2_driver.py` (368 lines)

`tasks/t0102_seedscale_n4_gen20/code/nsga2_driver.py` does **not** construct the pymoo `Problem`
itself — the only `Problem` construction is in `evaluator.py`'s `BedBV3MorphProblem.__init__` (see
above) [t0102]. The driver imports `BedBV3MorphProblem` at line 60 and instantiates it at **line
261**: `problem = BedBV3MorphProblem(eval_seeds=eval_seeds, elementwise_runner=runner)`. The
constructor call itself does not pass `n_obj`, so the t0104 driver does not need to change anything
at line 261. However, there are **two co-located surface-level edits** the driver does need:

* **HV reference point in `_compute_hv` (lines 108-113)**: line 109 hard-codes the 3-element ref
  point `np.array([0.0, 0.0, 0.0], dtype=np.float64)`. With `n_obj = 2`, this must become a
  2-element array `np.array([0.0, 0.0])` or the `HV(...)` call at line 113 will raise on shape
  mismatch against the 2-column population `F` matrix. Use the shared `REF_POINT_HV` constant from
  `constants.py` only if it is reduced to 2 entries; otherwise hard-code a 2-element ref point.

* **`_save_iteration` evaluation record (lines 141-151)**: line 149 stores
  `"robustness": float(-f_row[2])` — with `n_obj = 2` there is no `f_row[2]`. Drop this entry from
  the dict OR rebuild robustness from the per-cell `CellEvalResult` (which still contains it; see
  evaluator patch above). The cleanest fix is to drop `robustness` from the `all_evaluations` dump
  and let the analysis stage re-derive it from the predictions assets if needed.

* **Pareto-front cell dump in `run_nsga2_for_seed` (lines 297-309)**: line 307 stores
  `"robustness": float(-f_row[2])` in the per-cell record. Same fix as above — drop the entry from
  this dict or compute robustness via a separate pass over the per-cell summaries.

Additionally **lines 39 / 46 / 224** import / write `HV_UTOPIA_ROBUSTNESS`. Drop the import (line
46\) and the `hv_utopia` entry (line 224) in `_save_algorithm_config` to remove a stale 3-entry
artifact from `algorithm_config.json`.

### Cost watchdog wiring (`cost_watchdog.py`, 127 lines) and S-0102-08 idle-teardown

`tasks/t0102_seedscale_n4_gen20/code/cost_watchdog.py` is **dependent on `nsga2_driver.py` via a
pymoo `Termination` subclass**, not on the Vast.ai instance lifecycle directly [t0102]. The wiring
chain is:

1. `nsga2_driver.run_nsga2_for_seed` instantiates `CostWatchdog` via
   `make_watchdog_from_machine_log` (driver line 238-242), reading `selected_offer.price_per_hour`
   from `machine_log.json`.
2. `CostWatchdogTermination(watchdog=cost_watchdog, seed=task_seed)` (driver lines 93-105) wraps the
   watchdog. Its `_update` method (lines 101-105) calls `watchdog.trip_if_over_cap(...)` once per
   generation and returns `1.0` (terminated) or `0.0` (continue) to pymoo's `TerminationCollection`
   at lines 271-275.
3. `CostWatchdog.trip_if_over_cap` (`cost_watchdog.py` lines 75-97) writes
   `intervention/budget_overrun.md` when the cap is breached but **does NOT trigger Vast.ai
   teardown** — it only flips the `tripped` flag, which makes the pymoo loop terminate at its next
   generation boundary. After NSGA-II exits, `nsga2_driver` falls through to the cleanup block
   (lines 322-336) which prints the final cost and returns, but **the Vast.ai instance keeps
   billing** until an external orchestrator runs `vastai destroy instance ...`.

This is the root cause of the t0102 $3.51 idle overrun documented in suggestion S-0102-08 [t0102].
For t0104 to apply the S-0102-08 partial fix ("Bind the watchdog directly to instance teardown so
post-NSGA-II idle billing cannot accumulate") the patch must add a teardown hook into either
`CostWatchdog.trip_if_over_cap` or into the `nsga2_driver.run_nsga2_for_seed` cleanup block. Two
viable shapes:

* **Driver-level hook (lower risk)**: wrap the body of `run_nsga2_for_seed` in `try/finally`. In the
  `finally`, when `cost_watchdog.tripped is True` OR all gens completed, run the Vast.ai teardown
  command via subprocess. The driver already has access to the `selected_offer` instance ID via the
  same `machine_log.json` it read the rate from. Place the subprocess shell-out behind an explicit
  `--teardown-on-watchdog` flag default `False` so the smoke gate / local runs do not destroy
  anything.

* **Watchdog-level hook (more invasive)**: extend `CostWatchdog` with a
  `teardown_callback: Callable[[], None] | None = None` field, call it from `trip_if_over_cap` after
  writing the intervention md. The factory `make_watchdog_from_machine_log` (lines 100-116) gains a
  parallel `teardown_callback` kwarg.

The task_description.md REQ on idle-teardown wiring is satisfied by either; the driver-level hook is
preferred because it co-locates the teardown with the `pool.close()/pool.terminate()` calls at
driver lines 322-323 that already finalize compute resources.

### Predictions schema must retain `robustness` per cell

The task brief mandates that `robustness` survives in the per-cell predictions assets even though it
is dropped from the NSGA-II selection F-row. The relevant write site is
`build_predictions_assets.py` in t0102's code dir (the t0102 fork already exposes a per-cell summary
including DSI, PD, robustness, n_trials, n_errors, peak_vm_mv, is_unstable). t0104 needs to keep
that schema unchanged so analysis can later inspect the dropped axis. Inside `evaluator.py`,
`CellEvalResult` (lines 92-101) must retain its `robustness` field; the field is computed by
`_summarise_trials` lines 335-344 and returned unchanged. The only deletion is the
`-result.robustness` entry in the F-row.

### Anchor / clustering utilities from t0086 and t0102 are reusable verbatim

The analysis step (step 7 in task_description.md) requires anchor-distribution histograms across the
3 seeds. Two reusable code paths:

* `tasks/t0086_robustness_cluster_bio_comparison/code/cluster_analysis.py` [t0086] provides k-means
  (k=2..6, random_state=42) with silhouette + heuristic BIC, hierarchical clustering with cosine
  + euclidean metrics + average linkage, 50-sample bootstrap ARI stability, and per-cluster centroid
    extraction in normalised / unnormalised space. The constants `K_MIN=2`, `K_MAX=6`,
    `RANDOM_STATE=42`, `N_BOOTSTRAP=50`, `BOOTSTRAP_SUBSAMPLE_FRAC=0.8` are at lines 35-39. The
    module imports `LOWER_BOUNDS`, `N_PARAMS`, `UPPER_BOUNDS` from t0080 [t0080] — those constants
    refer to the 54-d electrophys subspace, so adapting to 68-d requires switching to t0102's
    `LOWER_BOUNDS_68` / `UPPER_BOUNDS_68` from `constants_morphology.py`.

* `tasks/t0102_seedscale_n4_gen20/code/anchor_classifier.py` [t0102] (~60-line module, exact lines
  read) provides post-hoc nearest-anchor assignment in 14-d morphology space, masking out the
  seed-index dimension at idx 12 (constant `SEED_INDEX_IN_14D = 12` at line 34). Uses
  `T0091_ANCHOR_DEFINITIONS_JSON` from t0102's paths.py and the 5 anchor names from
  `constants.ANCHOR_NAMES`. This is the entry point for the per-seed anchor histogram requested in
  step 7 of the task plan; copies straight into `tasks/t0104_*/code/` with the import paths
  rewritten from `tasks.t0102_*` to `tasks.t0104_*`.

### Morphology generator entry point (t0093)

The post-patch morphology generator is referenced indirectly through `generator_wrapper.py` [t0102]
which imports `generate_fixed_morphology` from t0092 (the canonical replacement per C-0093-01) and
`insert_baseline_channels` from t0092's `baseline_channels` module [t0093]. t0093 itself [t0093]
provides the re-sweep driver `resweep_driver.py` (240+ lines, head read) that wraps t0090's Phase D
verification under the patched generator — t0104 does NOT need to invoke `resweep_driver.py`
directly because the per-cell smoke-gate (`tasks/t0102_seedscale_n4_gen20/code/smoke_gate.py` lines
1-80) re-evaluates 5 anchors against the t0093 60-cell fingerprint at every run start and asserts
DSI within 0.05 and PD-rate within 1 Hz. Copy `smoke_gate.py` verbatim from t0102 to t0104; it is
already wired to the post-patch generator transitively via `generator_wrapper.py`.

### Constants module surface (`constants.py`, 91 lines) must drop one assertion

`tasks/t0102_seedscale_n4_gen20/code/constants.py` [t0102] re-exports the 68-d substrate constants
plus the 2-seed schedule at **lines 49-56**:

```python
T0102_SEEDS: tuple[int, ...] = (44, 55)
T0102_HARD_BUDGET_PER_SEED_USD: float = 4.00
T0102_TASK_BUDGET_TOTAL_USD: float = 8.00

assert len(T0102_SEEDS) == 2, f"expected 2 seeds, got {len(T0102_SEEDS)}"
```

t0104 must rename to `T0104_SEEDS = (44, 55, 66)`, update the length assertion to `== 3`, raise
`T0104_TASK_BUDGET_TOTAL_USD` to `12.00` (3 * $4 with a small idle margin under the $15 cap), and
re-export the new names. The `HV_UTOPIA_ROBUSTNESS` export at line 25 should be dropped from
`__all__` so that downstream nsga2_driver imports fail-fast if accidentally referenced.

## Reusable Code and Assets

All code copies are into `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/` with imports rewritten
from `tasks.t0102_seedscale_n4_gen20.code.*` to `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.*`.
Cross-task import is forbidden for non-library code per the cross-task code reuse rule.

* **`evaluator.py` — copy into task** (source: `tasks/t0102_seedscale_n4_gen20/code/evaluator.py`,
  480 lines). Function signatures retained: `_run_one_trial`,
  `_vector_sum_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float`,
  `_summarise_trials(*, results: list[TrialResult], n_seeds: int) -> CellEvalResult`,
  `evaluate_68d_vector(*, vector_68d: NDArray[np.float64], eval_seeds: list[int] | None = None, n_directions: int = N_DIRECTIONS) -> CellEvalResult`,
  `_worker_evaluate_vector`, class `BedBV3MorphProblem(ElementwiseProblem)`. **Adaptation**: (a) add
  `SILENCE_SPIKE_COUNT_THRESHOLD = 10` module constant; (b) inject silence guard in
  `_summarise_trials` (between lines 308 and 325); (c) drop `-result.robustness` from F-row at line
  471 and `-WORST_CASE_ROBUSTNESS` from fallback at line 477; (d) change `"n_obj": 3` to
  `"n_obj": 2` at line 455.

* **`nsga2_driver.py` — copy into task** (source:
  `tasks/t0102_seedscale_n4_gen20/code/nsga2_driver.py`, 368 lines). Function signatures retained:
  `run_nsga2_for_seed(*, task_seed: int) -> dict[str, object]`, class
  `CostWatchdogTermination(Termination)`, class `_GenerationCallback(Callback)`, `_save_iteration`,
  `_compute_hv`, `_load_init_matrix`, `_eval_seeds`, `_save_algorithm_config`, `main`.
  **Adaptation**: (a) shrink HV ref point to 2 entries (line 109); (b) drop
  `"robustness": float(-f_row[2])` from `_save_iteration`'s evaluation dict (line 149) and from
  `run_nsga2_for_seed`'s Pareto cell dict (line 307); (c) drop `HV_UTOPIA_ROBUSTNESS` import at line
  46 and the corresponding entry in `_save_algorithm_config` at line 224; (d) wrap the body of
  `run_nsga2_for_seed` in `try/finally` to invoke the Vast.ai teardown subprocess (S-0102-08).

* **`cost_watchdog.py` — copy into task** (source:
  `tasks/t0102_seedscale_n4_gen20/code/cost_watchdog.py`, 127 lines). Public surface:
  `load_hourly_rate_from_machine_log(*, path: Path) -> float`, class `CostWatchdog`,
  `make_watchdog_from_machine_log(*, machine_log_path: Path, instance_started_at: datetime, hard_budget_usd: float = T0102_HARD_BUDGET_USD) -> CostWatchdog`,
  `patch_t99_loop_rate`. **Adaptation**: rename `T0102_HARD_BUDGET_USD` to `T0104_HARD_BUDGET_USD`
  (or keep numeric value $4.00 unchanged but rename the symbol); update intervention md text to
  reference t0104; optionally extend `CostWatchdog` with a `teardown_callback` field (S-0102-08,
  watchdog-level option).

* **`generator_wrapper.py` — copy into task** (source:
  `tasks/t0102_seedscale_n4_gen20/code/generator_wrapper.py`, read 60 lines). Public: `_LIVE_CELLS`,
  `hash_morphology_vector(*, vector: NDArray[np.float64]) -> int`,
  `split_68d_vector(*, vector_68d: NDArray[np.float64]) -> tuple[NDArray, NDArray]`,
  `morphology_params_from_vector(*, morph_vector_14d: NDArray[np.float64]) -> MorphologyParams`,
  `build_cell(h, morph_params)`. **Adaptation**: rewrite the `tasks.t0102_*` self-import on line 31
  to `tasks.t0104_*`. Library imports from t0090 [t0090] and t0092 stay unchanged.

* **`constants.py`, `constants_electrophys.py`, `constants_morphology.py` — copy into task**
  (source: `tasks/t0102_seedscale_n4_gen20/code/constants*.py`, 91 lines for `constants.py`).
  **Adaptation in `constants.py`**: rename `T0102_SEEDS` to `T0104_SEEDS = (44, 55, 66)`, update
  length assertion to `== 3`, raise `T0104_TASK_BUDGET_TOTAL_USD` to `12.00`, drop
  `HV_UTOPIA_ROBUSTNESS` from `__all__`. `constants_morphology.py` keeps `N_EVAL_SEEDS = 4` and
  `N_GEN = 20` per parity with t0102.

* **`smoke_gate.py` — copy into task** (source:
  `tasks/t0102_seedscale_n4_gen20/code/smoke_gate.py`, ~150 lines, head read). Public:
  `run_smoke_gate(*, output_path: Path) -> dict[str, object]`. **Adaptation**: imports only; the
  gate already exercises the patched generator via `evaluator.evaluate_68d_vector`. After the DSI
  guard patch is in place, all 5 anchors must still produce PD-rate within 1 Hz of the t0093
  fingerprint and DSI within 0.05 — the silence guard only affects cells with < 10 total spikes,
  which the 5 anchors empirically do not hit.

* **`anchor_classifier.py`, `anchor_definitions.py`, `paths.py` — copy into task** (source:
  `tasks/t0102_seedscale_n4_gen20/code/`). **Adaptation**: rewrite `tasks.t0102_*` imports. The
  `T0091_ANCHOR_DEFINITIONS_JSON` constant in `paths.py` continues to point at the t0091 anchors
  JSON across the repo root, unchanged.

* **`cluster_analysis.py` — copy into task and adapt for 68-d** (source:
  `tasks/t0086_robustness_cluster_bio_comparison/code/cluster_analysis.py` [t0086], ~250 lines
  total, head read). Public: `KMeansEval`, `ClusterCentroidEntry` dataclasses, `_normalise` /
  `_unnormalise_vector` helpers, `_bic`. **Adaptation**: replace t0080 [t0080] `LOWER_BOUNDS` /
  `UPPER_BOUNDS` / `N_PARAMS` imports with t0104's 68-d analogs (`LOWER_BOUNDS_68`,
  `UPPER_BOUNDS_68`, `N_PARAMS_68 = 68`). Used only in the analysis step.

* **t0024 [t0024] de Rosenroll Bed B compartmental model — import via library** (registered as
  `de_rosenroll_2026_dsgc`). Path: `tasks.t0024_port_de_rosenroll_2026_dsgc.code.*`. No adaptation;
  t0102's `bootstrap.py` already loads the compiled MOD library and t0104 inherits this verbatim.

* **t0090 [t0090] / t0092 procedural DSGC morphology generator — import via library** (registered
  as `procedural_dsgc_morphology_generator`, effectively replaced by `*_fix` from t0092). Module
  paths: `tasks.t0090_morphology_generator_diversity_test.code.morphology_params`,
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix`,
  `tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels`. No adaptation; the
  t0104 fork of `generator_wrapper.py` references these unchanged.

* **`test_evaluator_dsi_guard.py` — NEW (no copy source)**: the unit test mandated by
  task_description.md item 3 in the Approach section. Build a synthetic `TrialResult` list with all
  16 directions x 4 seeds at `spike_count = 0`, call `_summarise_trials(results=trials, n_seeds=4)`,
  assert the returned `CellEvalResult.dsi_vector_sum == 0.0` (not 1.0). A second test case builds
  one direction with 5 PD spikes and 0 ND across 15 other directions (total = 5 across one seed =
  1.25 mean) and asserts the guard floor returns 0.0 (because mean total spikes = 1.25 across
  directions, well below 10). A third positive control with total mean spikes = 25 asserts the guard
  does NOT trigger and DSI is computed normally. Approx. 80 lines.

## Lessons Learned

* **Silence-corner artifact dominated the t0102 Pareto front.** Results_summary.md from t0102
  [t0102] documents that 27 cells reached DSI = 1.0 because the vector-sum formula divides by
  near-zero `total_spikes_f` (line 285 fallback never trips when `total_spikes_f` is small but
  non-zero). NSGA-II crowding distance then preserves the silence corner across generations because
  it appears Pareto-optimal in the (DSI, PD) plane. Dropping robustness alone is not expected to fix
  this — the guard patch is independently load-bearing.

* **Watchdog termination is not teardown.** t0102's $12.07 spend vs $8 plan cap decomposed as $8.46
  productive + $3.51 idle [t0102]. The per-seed $4 watchdog tripped correctly and the pymoo loops
  exited correctly, but the Vast.ai instance billed for 7.3 idle hours before manual teardown. The
  S-0102-08 fix must explicitly chain into a `vastai destroy` call.

* **Smoke gate is the cheap insurance against morphology silence.** t0090/t0092 silent-cell episode
  (corrected via C-0093-01) cost a full sweep. t0102's smoke gate (5 anchors x t0083 best
  electrophys, DSI tolerance 0.05, PD tolerance 1 Hz) catches the same failure mode for free —
  preserve it verbatim in t0104.

* **`N_EVAL_SEEDS = 4` is the operative noise constant**, not `N_SEEDS`. t0080's `constants.py`
  [t0080] has a dead `N_SEEDS = 20` symbol that is never imported by t0099 or t0102. The operative
  constant is in `constants_morphology.py`; do not be misled by the task_description's shorthand
  "N=4".

* **Per-seed vs cell-level DSI use different aggregations.** `_summarise_trials` calls
  `_vector_sum_dsi` once at the cell level (line 325) with the full per-direction spike-count lists,
  AND again per seed (line 332) with single-element lists. A naive silence guard inside
  `_vector_sum_dsi` would inflate-to-zero almost all per-seed DSIs (each carries < 16 spikes by
  construction) and break the robustness signal even when the cell is firing well. Implement the
  guard at `_summarise_trials` level only [t0102].

* **t0091 single joint-pass was warm-start dependent.** Reframed in t0102's answer asset [t0102]:
  the joint-pass cell was a one-mutation descendant of the `alt_topology` anchor. Removing the
  warm-start removes the joint-pass signal; t0102 confirmed at N=4. t0104 is the cheaper of the two
  remaining algorithmic levers (objective count vs algorithm replacement); IBEA / large-pop NSGA-II
  are deferred (S-0102-03 / S-0102-04).

## Recommendations for This Task

1. **Patch `evaluator.py` in three places** (see "Exact patch sites in evaluator.py" above): silence
   guard in `_summarise_trials` lines 308-325, F-row drop in `BedBV3MorphProblem._evaluate` lines
   471 / 477, `"n_obj": 2` in `BedBV3MorphProblem.__init__` line 455. Add
   `SILENCE_SPIKE_COUNT_THRESHOLD = 10` as a named module constant near the worker globals (lines
   105-108) — explicit constant > magic number.

2. **Patch `nsga2_driver.py` in four places**: 2-element HV ref point at line 109; drop
   `"robustness"` from `_save_iteration` dict at line 149; drop `"robustness"` from Pareto cell dict
   at line 307; drop `HV_UTOPIA_ROBUSTNESS` import (line 46) and config entry (line 224). Wrap
   `run_nsga2_for_seed` in `try/finally` and invoke Vast.ai teardown subprocess in `finally`
   (S-0102-08 partial fix).

3. **Implement the DSI-guard unit test** `tasks/t0104_*/code/test_evaluator_dsi_guard.py` with at
   least three cases (all-silent, near-silent at total mean spikes = 1.25, firing positive control).
   Run before SCP to instance per task_description.md step 5b.

4. **Reuse the smoke gate verbatim** at the start of every Vast.ai run. Do not relax the 1 Hz / 0.05
   DSI tolerances for t0104 — the silence guard does not affect the 5 t0083-best anchors which
   fire well above the 10-spike threshold.

5. **Keep `robustness` in `CellEvalResult` and in the predictions assets schema** even though it is
   dropped from the F-row. Analysis (step 7) needs it to compute the post-hoc "what would robustness
   have been on the new Pareto front" comparison vs t0102.

6. **Set `T0104_TASK_BUDGET_TOTAL_USD = 12.00`** in `constants.py` (3 seeds * $4 + ~$0 idle margin
   via S-0102-08 teardown). The plan's $15 hard cap stays as an orchestrator-level guard on top of
   the per-seed watchdog.

7. **Adapt `cluster_analysis.py` from t0086 [t0086] for 68-d** when starting the analysis step.
   Replace 54-d `LOWER_BOUNDS` imports with 68-d. The k=2..6 + silhouette + BIC + bootstrap ARI
   pipeline is the canonical anchor-cluster diagnostic; no need to reinvent.

8. **Reuse `anchor_classifier.py` from t0102 [t0102] verbatim** (only rewrite the self-import). The
   14-d morphology anchor histogram per seed is the primary "did the front shift" comparison against
   t0102.

9. **Do NOT modify `generator_wrapper.py` semantics** — it transitively depends on the t0092 fix
   library and any change risks reintroducing the silent-cell regression that t0090/t0093 already
   characterised [t0090] [t0093].

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC compartmental model
* **Status**: completed
* **Relevance**: Provides the Bed B NEURON HOC template and compiled MOD library that t0104 inherits
  transitively through t0102's `bootstrap.py`. Registered as the `de_rosenroll_2026_dsgc` library.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B MOBO v3 with dendritic spike NSGA-II (49/54-d origin)
* **Status**: completed
* **Relevance**: Origin of the 54-d electrophys substrate and the dead `N_SEEDS = 20` constant whose
  presence in `constants_electrophys.py` is documented to disambiguate it from the operative
  `N_EVAL_SEEDS = 4`. Also the source of compiled MOD files reused by t0102 / t0104.

### [t0086]

* **Task ID**: `t0086_robustness_cluster_bio_comparison`
* **Name**: Robustness + cluster + bio-comparison of t0081 / t0083 joint-pass cells
* **Status**: completed
* **Relevance**: Provides the canonical clustering pipeline (`cluster_analysis.py`) — k-means
  k=2..6, hierarchical clustering, 50-sample bootstrap ARI, per-cluster centroids — for the
  analysis step of t0104. Adaptation: rebind the 54-d bounds imports to 68-d.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator + diversity test + validation bundle
* **Status**: completed
* **Relevance**: Original 14-knob morphology generator (registered as
  `procedural_dsgc_morphology_generator`); replaced by t0092's fix under C-0093-01. Provides
  `MorphologyParams` and `MorphologyResult` dataclasses imported by t0102 / t0104.

### [t0093]

* **Task ID**: `t0093_resweep_and_t0090_correction`
* **Name**: Re-sweep t0090 verification under the t0092 patched generator
* **Status**: completed
* **Relevance**: Post-patch morphology generator validator. Source of the 60-cell post-fix
  verification fingerprint used by t0102's `smoke_gate.py` and reused unchanged by t0104. Confirms
  the generator is safe to use under the t0083 best-cell electrophys vector.

### [t0099]

* **Task ID**: `t0099_random_init_pareto_robustness`
* **Name**: Random-init Pareto + robustness on 68-d (3 seeds, pop=96, gens=5-8, N=20)
* **Status**: completed
* **Relevance**: First random-init 68-d NSGA-II run; established the null result that t0102
  replicated. Code substrate (nsga2_driver, evaluator, generator_wrapper) is the direct ancestor of
  t0102's code, so t0104 inherits the same architectural choices.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init
* **Status**: completed
* **Relevance**: Direct parent. t0104 forks t0102's `code/` verbatim with three patches (DSI guard,
  `n_obj` 3 -> 2, 2 seeds -> 3 seeds + teardown wiring). All exact line-number patch sites
  documented in Key Findings refer to t0102's source files.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose and patch t0090 morphology generator silence
* **Status**: completed
* **Relevance**: Source of `generate_fixed_morphology` and `insert_baseline_channels` (corrected
  morphology generator). Library-level dependency reached via t0102's `generator_wrapper.py`
  imports; no direct edits required in t0104.
