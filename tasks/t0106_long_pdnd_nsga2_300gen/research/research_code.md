---
spec_version: "1"
task_id: "t0106_long_pdnd_nsga2_300gen"
research_stage: "code"
tasks_reviewed: 12
tasks_cited: 11
libraries_found: 18
libraries_relevant: 0
date_completed: "2026-05-17"
status: "complete"
---
# Research Code — Long 2-Direction NSGA-II at 300 Generations

## Task Objective

t0106 is a tight evaluator fork of [t0104] with three substantive code changes: drop angular
sampling from 16 to 2 directions (PD = 0 deg, ND = 180 deg), redefine DSI as the antipodal ratio
`(PD - ND) / (PD + ND)`, drop `N_EVAL_SEEDS` from 4 to 3, and extend `N_GEN` from 20 to 300 on a
single GA seed (44) under an operator-gated hourly hypervolume poll with a $25 cost cap. The 68-d
Bed B + 14-d morphology substrate, all synaptic / placer / generator infrastructure, and the t0080
MOD-channel namespace remain unchanged. This research stage identifies the exact patch sites in the
[t0104] code base, lists every helper module to copy, prescribes a pymoo `Callback`-based operator
stop + dill checkpoint scaffold, and specifies a one-cell local smoke-test plan to confirm the
2-direction pipeline returns sane numbers before Vast.ai provisioning.

## Library Landscape

The library aggregator script (`aggregate_libraries.py`) is not present in this repo; libraries were
enumerated by direct file walk of `tasks/*/assets/library/*/details.json`. **18 libraries** exist
project-wide. The four that touch the t0080-t0104 lineage are:

* `modeldb_189347_dsgc` (created by [t0008]) — the upstream NEURON Hb9 DSGC model. Not imported by
  t0106; the lineage uses the de Rosenroll 2026 fork via [t0024] instead.
* `modeldb_189347_dsgc_gabamod` (created by [t0020]) — superseded library; not used.
* `modeldb_189347_dsgc_dendritic` (created by [t0022]) — superseded library; not used.
* `de_rosenroll_2026_dsgc` (created by [t0024]) — Bed B port; **transitively used** by t0106
  because `trial_helpers.py` imports `tasks.t0024_port_de_rosenroll_2026_dsgc.code.constants` and
  `ar2_noise.generate_ar2_batch`. The library asset's `sources/` directory also vendors the
  Windows-only `nrnmech.dll`; the Linux MOD library is compiled separately from the t0080 MOD source
  tree.

Other library assets (`tuning_curve_viz`, `tuning_curve_loss`, etc.) are unrelated to NSGA-II
fitting and are not relevant. **No library is imported via its registered library entry point in
t0106** — t0024 is accessed via the standard task-import pattern
`tasks.t0024_port_de_rosenroll_2026_dsgc.code.<module>` because that is how every upstream NSGA-II
task (t0078, t0080, t0091, t0099, t0102, t0104) calls into t0024 helpers.

## Key Findings

### The Vector-Sum DSI Already Reduces to Ratio DSI at Two Antipodal Directions

The `_vector_sum_dsi` function in [t0104]'s `evaluator.py` (lines 274-295) computes:

```python
total_x += mean_count * np.cos(rad)
total_y += mean_count * np.sin(rad)
total_spikes_f += mean_count
return float(np.hypot(total_x, total_y) / total_spikes_f)
```

At `angles_deg = [0.0, 180.0]` the unit vectors are `(+1, 0)` and `(-1, 0)`, so
`total_x = mean_PD - mean_ND`, `total_y = 0`, and the function returns
`abs(mean_PD - mean_ND) / (mean_PD + mean_ND)` — i.e., the absolute-valued ratio DSI. This is
mathematically the t0106 ratio DSI for `PD >= ND` and matches in all biological cases of interest. A
targeted `_ratio_dsi` is therefore **optional** (the existing function works as-is at n=2). The
implementation can be simplified by replacing the body with a `mean_pd / mean_nd` ratio expression
for clarity, but this is cosmetic.

### Per-Generation Worker Pool Restart Pattern Does Not Yet Exist in the Lineage

The "per-generation worker pool restart pattern from t0102" called out in the t0106 task description
is **not implemented** in [t0102]: the driver creates one `multiprocessing.Pool` before `minimize()`
(line 259) and tears it down after `minimize()` returns (lines 322-323). The same single-pool
pattern is in [t0099] and [t0104]. The t0102 plan (Risk row in `plan.md` line 576) names worker
restart as a fallback only. For t0106 at 300 generations on a single instance, NEURON memory
accumulation is a real risk — the t0102 results acknowledge "Both seeds terminated by per-seed $4
cost watchdog before gen 20" — so t0106 needs to add a real per-generation pool restart. The
cleanest implementation is a pymoo `Callback` that closes and recreates the `Pool` every N
generations (recommend N=25, per t0106 task_description.md Risk row), updating
`problem.elementwise_runner` to a fresh `StarmapParallelization(pool.starmap)`.

### Operator-Stop and Checkpointing Are Wired via pymoo Termination, Not Callback

[t0104]'s `nsga2_driver.py` already runs a `TerminationCollection` of three terminations
(`MaximumGenerationTermination`, `HVPlateauTermination`, `CostWatchdogTermination`) at lines
339-343. The pattern for the t0106 `intervention/stop.md` operator-stop signal is to add a fourth
`Termination` subclass that polls the stop file in `_update`, returning `1.0` when the file exists.
This matches the established [t0104] pattern and avoids the `Callback`-with- `force_termination`
route from the internet research, which is harder to reason about given the existing
`TerminationCollection`. Per-generation `dill` checkpointing is straightforward to bolt on to
`_GenerationCallback.notify` (lines 217-228): `dill.dump((algorithm, state), open(...))`. The HV
trace is already written to `hv_trajectory_seed{s}.json` (line 173) — t0106 only needs to widen
that file to JSONL format with the `hv_trace.jsonl` schema from `task_description.md`.

### The Evaluator Already Parameterises n_directions

[t0104]'s `evaluate_68d_vector` already accepts `n_directions: int = N_DIRECTIONS` as a kwarg (line
383), and builds `angles_deg` from it at line 419
(`[float(d) * (360.0 / n_directions) for d in range(n_directions)]`). At `n_directions=2` this gives
`[0.0, 180.0]` exactly — no code change needed beyond switching the default constant. [t0104]'s
smoke_gate.py already calls `evaluate_68d_vector(..., n_directions=8)` (line 97), proving the
parameterisation works end-to-end. **This means the angular reduction patch is a single-line change
to a constant**, not an evaluator rewrite.

### Silence Guard Inherited Unchanged from t0102 / t0104

The DSI silence guard (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`, evaluator.py line 109) lives inside
`_summarise_trials` at lines 343-346 and is independent of `n_directions`. At 2 directions the
threshold is conservative (median real DSGC cells produce >10 PD spikes alone per [Trenholm2013]);
t0106 inherits it verbatim. The plan's risk-mitigation sweep across thresholds {5, 10, 20} can be a
post-hoc analysis on the predictions asset, not a structural change.

### t0080 MOD Library Is the Canonical Linux Compile Target

[t0104]'s `paths.py` resolves the compiled MOD library from
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/x86_64/.libs/libnrnmech.so` (lines 20-25).
The t0080 `mods/` directory contains **13 `.mod` files** (bkt80.c through skt80.mod plus
`mod_func.c`): `bkt80.mod`, `calt80.mod`, `catt80.mod`, `iht80.mod`, `kdrt80.mod`, `kv3t80.mod`,
`kv4t80.mod`, `kv7t80.mod`, `napt80.mod`, `nart80.mod`, `nav16t80.mod`, `skahpt80.mod`, `skt80.mod`.
All 13 must be SCP'd to the Vast.ai instance and compiled with `nrnivmodl` before the driver starts.
The t0104 lineage already does this; t0106 inherits the procedure unchanged.

### Worker Cache Survives Morphology and Electrophys Changes

`evaluator.py` (lines 113-163) maintains a worker-process-global
`(MorphologyResult, SynapseBundle, morph_hash, electrophys_hash)` cache that rebuilds the NEURON
cell only on morphology-vector change and the synapse bundle only on electrophys-vector change. This
is critical at 300 gens because most generations contain incremental electrophys mutations on stable
morphology vectors, so most cells hit the cell-reuse fast path. **No change needed for t0106** —
the cache is geometry-aware and shrinks per-cell cost when NSGA-II converges on a narrow morphology
subspace.

### t0103 + t0099 Per-Seed Schema Patterns Carry Over

[t0103] (Baden 2016 morphology extraction) is unrelated. [t0099] is the random-init baseline whose
per-seed file naming (`pareto_front_seed{s}.json`, `all_evaluations_seed{s}.json`,
`hv_trajectory_seed{s}.json`, `nsga2_checkpoint_seed{s}.json`) [t0104] reused verbatim. t0106 will
use the same convention at `seed=44` for trivial cross-seed comparison with [t0104]'s seed-44 file.

## Reusable Code and Assets

Per the cross-task rule, every reusable piece below from the t0080-t0104 lineage is **copy into
task**. Library imports from [t0024] and [t0090] / [t0092] go via standard task-import paths (not
the registered library asset). All file paths below are repo-root-relative.

### Copy into task (verbatim, no edits)

* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/__init__.py` (1 line) — package marker.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/bootstrap.py` (~150 lines) — Linux NEURON
  bootstrap; monkey-patches t0024's `load_neuron` to load the t0080 MOD library. Side-effect import;
  do not edit.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/apply_params.py` — 54-d electrophys-to-cell write
  function. Stable across the lineage.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/build_cell_ais.py` — `DSGCCellWithAIS` dataclass
  (referenced by `trial_helpers.py`).
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/extend_with_ais.py` — AIS extender used by
  `apply_params`.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/parametric_placer.py` — synapse-placer; no
  task-specific knobs.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/recorder.py` — Vm recording helper.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/trial_helpers.py` — 13 helpers copied verbatim
  from [t0024] including `_bar_arrival_times`, `_rates_with_ar2_noise`, `_gaba_prob_for_direction`,
  `_rates_to_events`, `_count_spikes`, `setup_synapses_parametric`, `BASE_ACH_PROB`, `RATE_DT_MS`,
  plus the t0076 synaptic-placer fork.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/generator_wrapper.py` — thin adapter around
  [t0092] `generate_fixed_morphology` (the [t0093] patched version). Calls
  `tasks.t0090_*.code.morphology_params`, `tasks.t0092_*.code.morphology_generator_fix`,
  `tasks.t0092_*.code.baseline_channels.insert_baseline_channels`. Imports stay valid via the
  full-path import pattern.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/cost_watchdog.py` — Vast.ai cost watchdog;
  reusable verbatim, only the hard cap changes.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/biological_priors.py`, `biological_scorecard.py`,
  `anchor_definitions.py`, `anchor_classifier.py` — needed by smoke_gate and downstream analysis.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/test_evaluator_dsi_guard.py` — silence-guard unit
  tests; copy verbatim and rerun under t0106 imports.

**Approx total verbatim-copy size**: ~2400 lines across 14 files (estimate from `wc -l` on the t0104
code directory).

### Copy into task, patch

| File | Patch |
| --- | --- |
| `constants_electrophys.py` (548 lines) | No changes needed (ANGLES are in `constants_morphology.py` in this lineage). Keep verbatim. |
| `constants_morphology.py` (157 lines) | Line 127: `N_EVAL_SEEDS: int = 4` -> `N_EVAL_SEEDS: int = 3`. Line 128: `N_DIRECTIONS: int = 16` -> `N_DIRECTIONS: int = 2`. Line 111: `N_GEN: int = 20` -> `N_GEN: int = 300`. |
| `constants.py` (100 lines) | Replace `T0104_SEEDS = (44, 55, 66)` -> `T0106_SEEDS = (44,)`. Replace `T0104_HARD_BUDGET_PER_SEED_USD = 4.00` -> `T0106_HARD_BUDGET_USD = 25.00`. Update import names downstream. |
| `paths.py` (192 lines) | Replace all `t0104_nsga2_2obj_dsi_pdrate_3seeds` substring with `t0106_long_pdnd_nsga2_300gen`. Add `hv_trace_jsonl(step_id: str) -> Path` returning `logs/steps/<step_id>/hv_trace.jsonl`. Add `stop_signal_md() -> Path` returning `INTERVENTION_DIR / "stop.md"`. Add `checkpoint_dill(seed, gen) -> Path`. |
| `evaluator.py` (504 lines) | Replace package import paths (`t0104_nsga2_2obj_dsi_pdrate_3seeds` -> `t0106_long_pdnd_nsga2_300gen`). At line 419 the existing `angles_deg` expression already produces `[0.0, 180.0]` at `n_directions=2`; no algorithm change needed. Optionally rename `_vector_sum_dsi` -> `_ratio_dsi` for clarity. |
| `nsga2_driver.py` (480 lines) | (1) Imports / package paths rewritten. (2) Add `OperatorStopTermination(Termination)` polling `intervention/stop.md` each generation. Splice into `TerminationCollection`. (3) Add `PerGenerationPoolRestart` callback wrapping `_GenerationCallback`; close pool every 25 gens, recreate, swap `problem.elementwise_runner`. (4) Replace `hv_trajectory_json` writes with JSONL `hv_trace.jsonl` per task_description.md schema (`gen`, `wall_clock_s`, `hv`, `n_cells_evaluated`). (5) Add `dill.dump(algorithm, ...)` in `_save_iteration` at the end. (6) `_eval_seeds()` already honours `N_EVAL_SEEDS=3` after the constants patch. (7) Default budget to `T0106_HARD_BUDGET_USD = 25.00`. |
| `hv_plateau_watchdog.py` (~80 lines) | Optional in t0106 — operator-stop is the primary stop mechanism. If kept, raise `HV_PLATEAU_MIN_HV_HISTORY` from 4 to 60 (1-hour sliding window at 60s/gen) to match the hourly-poll heuristic from `research_internet.md` insight 1. |
| `random_init.py` | Update `T0104_SEEDS` import to `T0106_SEEDS`; everything else stable. |
| `smoke_gate.py` | Change `seeds_eval = [42, 4242, 424242, 4444444]` to length-3 (`N_EVAL_SEEDS=3`). Change `n_directions=8` -> `n_directions=2` in `evaluate_68d_vector` call. Add per-cell sanity-check on `dsi_vector_sum in [0, 1]`. |

### Cross-task imports kept (no copy)

* `tasks.t0024_port_de_rosenroll_2026_dsgc.code.constants` and `.ar2_noise.generate_ar2_batch` —
  upstream constants and AR(2) noise generator (Bed B port).
* `tasks.t0090_morphology_generator_diversity_test.code.morphology_params`, `.constants` — 14-d
  morphology dataclass and bounds.
* `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix`,
  `.baseline_channels` — patched morphology generator (per [t0093] correction).

These are full-path task imports, not library imports, but they are the established cross-task
pattern across the entire t0078-t0104 lineage and the verificator allows them.

### Unified-diff sketch of the four highest-impact patches

```diff
--- a/tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants_morphology.py
+++ b/tasks/t0106_long_pdnd_nsga2_300gen/code/constants_morphology.py
@@ -108,3 +108,3 @@ POP_SIZE: int = 96
-# t0102 plan REQ-2: extend N_GEN from t0099's 8 to 20 (2.5x more generations).
-N_GEN: int = 20
+# t0106: extend N_GEN to 300 (hard cap); operator-stop is primary stop mechanism.
+N_GEN: int = 300
@@ -127,3 +127,3 @@ HV_PLATEAU_MIN_HV_HISTORY: int = 4
-N_EVAL_SEEDS: int = 4
-N_DIRECTIONS: int = 16
+N_EVAL_SEEDS: int = 3
+N_DIRECTIONS: int = 2

--- a/tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants.py
+++ b/tasks/t0106_long_pdnd_nsga2_300gen/code/constants.py
@@ -60,3 +60,3 @@
-T0104_SEEDS: tuple[int, ...] = (44, 55, 66)
-T0104_HARD_BUDGET_PER_SEED_USD: float = 4.00
-T0104_TASK_BUDGET_TOTAL_USD: float = 12.00
+T0106_SEEDS: tuple[int, ...] = (44,)
+T0106_HARD_BUDGET_USD: float = 25.00
+T0106_PER_INSTANCE_WATCHDOG_USD: float = 20.00

--- a/tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/nsga2_driver.py
+++ b/tasks/t0106_long_pdnd_nsga2_300gen/code/nsga2_driver.py
@@ -126,6 +126,18 @@ class _DriverState:
+class OperatorStopTermination(Termination):
+    """Poll intervention/stop.md each generation; trigger on file exists."""
+    def __init__(self, *, stop_path: Path) -> None:
+        super().__init__()
+        self._stop_path = stop_path
+
+    def _update(self, algorithm: object) -> float:
+        if self._stop_path.exists():
+            print(f"[operator_stop] stop signal detected at {self._stop_path}; terminating")
+            return 1.0
+        return 0.0

@@ -339,6 +351,7 @@
     termination = TerminationCollection(
         MaximumGenerationTermination(n_max_gen=N_GEN),
         HVPlateauTermination(seed=task_seed),
         CostWatchdogTermination(watchdog=cost_watchdog, seed=task_seed),
+        OperatorStopTermination(stop_path=stop_signal_md()),
     )

--- a/tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/evaluator.py
+++ b/tasks/t0106_long_pdnd_nsga2_300gen/code/evaluator.py
@@ -383,3 +383,3 @@
-    n_directions: int = N_DIRECTIONS,
+    n_directions: int = N_DIRECTIONS,  # now defaults to 2 via constants_morphology
```

## MOD Files for Vast.ai SCP

The t0080 MOD library is the compile target. All 13 source files plus `mod_func.c` go to
`<vast_instance>:~/neuron-channels/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` and
`nrnivmodl` is run there to produce `x86_64/.libs/libnrnmech.so`:

1. `bkt80.mod` — BK / KCa1.1
2. `calt80.mod` — L-type Ca
3. `catt80.mod` — T-type Ca
4. `iht80.mod` — HCN / Ih
5. `kdrt80.mod` — delayed-rectifier K
6. `kv3t80.mod` — Kv3 fast K
7. `kv4t80.mod` — Kv4 / IA transient K
8. `kv7t80.mod` — Kv7 / M-current
9. `napt80.mod` — persistent Na
10. `nart80.mod` — resurgent Na
11. `nav16t80.mod` — Nav1.6
12. `skahpt80.mod` — SK_E2 slow AHP
13. `skt80.mod` — SK / KCa2 fast

Plus the t0024 sources at
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/`, compiled
into the t0024 Linux library by `bootstrap.py:_compile_t0024_mods_linux`.

## pymoo Callback + dill Checkpointing Skeleton

The skeleton below is the minimal scaffold for the operator-stop loop and per-generation `dill`
checkpoint. It mirrors the [t0104] `_GenerationCallback` structure but adds the JSONL trace writer
and the checkpoint write:

```python
import dill, json, time
from pathlib import Path
from pymoo.core.callback import Callback
from pymoo.core.termination import Termination

class OperatorStopTermination(Termination):
    def __init__(self, *, stop_path: Path) -> None:
        super().__init__()
        self._stop_path = stop_path

    def _update(self, algorithm: object) -> float:
        return 1.0 if self._stop_path.exists() else 0.0


class HourlyHVTrace(Callback):
    """Append one JSON line per gen to hv_trace.jsonl; dill-checkpoint algorithm."""
    def __init__(self, *, trace_path: Path, checkpoint_dir: Path,
                 start_wall: float, n_workers: int) -> None:
        super().__init__()
        self._trace_path = trace_path
        self._checkpoint_dir = checkpoint_dir
        self._start_wall = start_wall

    def notify(self, algorithm: object) -> None:
        gen = int(algorithm.n_gen)
        F = np.array([ind.F for ind in algorithm.pop], dtype=np.float64)
        hv = float(HV(ref_point=np.array([0.0, 0.0])).do(F)) if F.size else 0.0
        line = {
            "gen": gen,
            "wall_clock_s": float(time.time() - self._start_wall),
            "hv": hv,
            "n_cells_evaluated": int(len(algorithm.pop)),
        }
        with self._trace_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line) + "\n")
        ckpt = self._checkpoint_dir / f"checkpoint_gen{gen:04d}.pkl"
        with ckpt.open("wb") as f:
            dill.dump(algorithm, f)
```

`dill` is preferred over `pickle` because pymoo `Algorithm` objects contain numpy callables and
local closures that stdlib `pickle` cannot serialise (research_internet.md insight 2). The
checkpoint can be resumed with `algorithm = dill.load(open(ckpt, "rb"))` and passed to
`minimize(problem, algorithm, MaximumGenerationTermination(N_GEN), ...)`.

## Smoke-Test Plan (Local, Pre-Vast.ai)

The smoke test runs **one** 68-d cell evaluation locally on Windows using the t0024 vendored
`nrnmech.dll` to confirm the 2-direction + ratio-DSI + `N_EVAL_SEEDS=3` pipeline returns sane
numbers and that no import / hash-cache assumption breaks. Concrete steps:

1. Build the t0106 `code/` directory with all patches above.
2. Run `python -u -m tasks.t0106_*.code.smoke_gate` (which calls `evaluate_68d_vector` once with
   `n_directions=2`, `eval_seeds = [42, 4242, 424242]`). Expect:
   * Returns within ~30 s on the local workstation (single cell, 6 trials).
   * `dsi_vector_sum in [0.0, 1.0]` strict — fail if outside.
   * `pd_rate_hz in [0.0, 200.0]` (sanity bounds from [Trenholm2013]).
   * `nd_rate_hz <= pd_rate_hz` for the bedb_like anchor (cell is direction-selective by
     construction; if ND > PD, the angle convention is wrong).
   * `n_errors == 0` and `is_unstable == False` for the bedb_like anchor.
3. Run the silence-guard sensitivity check across thresholds {5, 10, 20} on the same anchor with PD
   = 0 enforced (degenerate case) — verify the guard zero-outs the DSI for all three thresholds.
4. Run `python -u -m pytest tasks.t0106_*.code.test_evaluator_dsi_guard` (copied from [t0104]).
5. Print a one-line ratio-DSI vs vector-sum-DSI cross-check: at PD = 5, ND = 1 the function should
   return `(5 - 1) / (5 + 1) = 0.667` to within 1e-6.

Pass criteria: all 5 steps pass on Windows local in < 5 min total wall-clock. Fail criteria: any DSI
outside [0, 1], any error in the bedb_like anchor evaluation, any unit-test failure.

## Lessons Learned

* **Silence-corner artifact is fixed but observable**. [t0102] saw 27 cells at spurious DSI = 1.0
  due to dividing by ~0 total spikes; [t0104] introduced `SILENCE_SPIKE_COUNT_THRESHOLD = 10` and
  the floor cleanly dropped to 0 spurious cells. t0106 inherits the guard verbatim. The 2-direction
  setting does not change this — the guard runs on total spike count, not per-direction.
* **Robustness axis is computed but not selected on**. [t0104] (REQ-5) dropped robustness from
  NSGA-II selection by switching `n_obj=3` -> `n_obj=2` and shrinking the HV ref point from 3-tuple
  to 2-tuple. The per-cell `CellEvalResult.robustness` field is still populated and lives in the
  predictions asset for post-hoc analysis. t0106 keeps the same 2-objective layout.
* **The cost watchdog already saves the run**. [t0102] reported "Both seeds terminated by per-seed
  $4 cost watchdog before gen 20" — the watchdog stop is the load-bearing mechanism. t0106 raises
  the cap to $25 total / $20 per-instance, but the same `make_watchdog_from_machine_log` shim and
  `CostWatchdogTermination` work unchanged.
* **HV plateau watchdog is too tight for long runs**. [t0102]'s `HV_PLATEAU_MIN_HV_HISTORY = 4` was
  fine at `N_GEN=20`; at `N_GEN=300` with operator-stop as primary, the HV-plateau watchdog should
  be widened (per research_internet.md: pymoo's `RobustTermination` default `period=30` and Blank &
  Deb 2020's window-30 recommendation) or disabled entirely in favour of the human-in-the-loop.
* **`generator_wrapper` caches survive 300 gens fine**. [t0091]'s anchor-tracking and per-seed
  diagnostics work in steady state at high gen counts; the worker-global cache on
  `(morph_hash, electrophys_hash)` is the key reuse mechanism.
* **No per-generation pool restart exists yet in the lineage**. The t0102 plan flagged this as a
  fallback risk mitigation; [t0102], [t0099], and [t0104] all run with a single pool for the entire
  `minimize()`. t0106 at 300 gens is the first task that actually needs the restart pattern; this
  must be implemented for real, not inherited.
* **Smoke gate is the cheapest insurance**. [t0104]'s `smoke_gate.py` ran 5 anchors x 4 seeds and
  caught two structural bugs in dev before Vast.ai provisioning. t0106 should keep the same gate at
  5 anchors x 3 seeds with `n_directions=2`.

## Recommendations for This Task

1. **Copy the entire [t0104] `code/` directory verbatim**, then apply the patches in the table
   above. Total copy size ~3000 lines; total patch surface ~120 lines across 7 files.
2. **Implement `OperatorStopTermination` as a 4th `Termination` in the existing
   `TerminationCollection`**, not as a `Callback` with `force_termination`. This matches the
   existing [t0104] driver shape and avoids two competing stop mechanisms.
3. **Add a `PerGenerationPoolRestart` callback** that closes and recreates `multiprocessing.Pool`
   every 25 generations. The trigger threshold mirrors the t0106 task_description.md Risk row.
4. **Replace `hv_trajectory_json` with JSONL `hv_trace.jsonl`** with exactly the schema in
   task_description.md (`gen`, `wall_clock_s`, `hv`, `n_cells_evaluated`) — this is the operator
   readout. Keep the t0104 `hv_trajectory_json` shape as a backwards-compatible mirror only if
   downstream analysis scripts depend on it.
5. **Add `dill` checkpointing in `_GenerationCallback.notify`** writing
   `logs/steps/<step_id>/checkpoint_gen<N>.pkl`. Resume path is straightforward via
   `dill.load(...)`.
6. **Drop the optional `_ratio_dsi` rewrite**. The existing `_vector_sum_dsi` returns the ratio DSI
   identically at `n_directions=2`. Add a unit test asserting numeric equivalence on a synthetic PD
   = 5, ND = 1 case.
7. **Run the local smoke test on Windows before any Vast.ai provisioning**. Specifically verify the
   silence-guard sensitivity sweep across {5, 10, 20} on the bedb_like anchor.
8. **Disable or relax `HVPlateauTermination`**. At 300 gens the operator-stop loop is primary;
   leaving the t0102 plateau watchdog at `window=2, min_history=4` will trigger spuriously inside
   the first hour.
9. **Inherit the t0104 cost-watchdog teardown path verbatim** (`TEARDOWN_ON_WATCHDOG=True` via the
   `--teardown-on-watchdog` CLI flag). Raising the cap from $4 to $25 changes only the constant.
10. **Re-use the [t0104] `test_evaluator_dsi_guard.py` test suite** with `N_DIRECTIONS_LOCAL = 2`
    and `N_EVAL_SEEDS_LOCAL = 3`. Verify the guard zero-out behaviour on synthetic 2-direction
    spike-count dictionaries.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 (Hb9 DSGC) to NetPyNE
* **Status**: completed
* **Relevance**: Upstream library origin (`modeldb_189347_dsgc`); not used directly by t0106 but is
  the source for the downstream de Rosenroll fork.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: ModelDB 189347 + GABA mod
* **Status**: completed
* **Relevance**: Superseded library; not used.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Channel testbed
* **Status**: completed
* **Relevance**: Superseded library; not used.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Bed B port. Provides the `ar2_noise.generate_ar2_batch` and `constants` modules
  used by `trial_helpers.py`. Source of vendored MOD files. Imported via standard task-import paths.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: 14-d morphology generator
* **Status**: completed
* **Relevance**: Provides `MorphologyParams`, `MorphologyResult`, `PARAM_NAMES`, `PARAM_BOUNDS`, and
  `INT_PARAM_NAMES`. Imported via `tasks.t0090_*.code.morphology_params` and
  `tasks.t0090_*.code.constants`.

### [t0091]

* **Task ID**: `t0091_morphology_extended_nsga2_v1`
* **Name**: Morphology-extended NSGA-II v1
* **Status**: completed
* **Relevance**: 14-d morphology NSGA-II ancestor. Source of the anchor-tracking idea and the
  `generator_wrapper` caching pattern that survives 300 gens cleanly.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Patched morphology generator
* **Status**: completed
* **Relevance**: Provides `generate_fixed_morphology` (canonical per C-0093-01) and
  `insert_baseline_channels`. The "patched" version referenced by t0106 task description.

### [t0093]

* **Task ID**: `t0093_resweep_and_t0090_correction`
* **Name**: t0090 correction + resweep
* **Status**: completed
* **Relevance**: Records the t0090 correction that selects t0092's patched generator. Direct
  dependency of t0106; nothing to copy but the correction overlay is implicitly applied via the
  `generator_wrapper.py` import path.

### [t0099]

* **Task ID**: `t0099_random_init_pareto_robustness`
* **Name**: Random-init Pareto baseline (3 seeds at gen 8)
* **Status**: completed
* **Relevance**: First random-init lineage member. Established the per-seed file naming, the LHS
  init, and the `n_obj=3` evaluator that [t0102] / [t0104] forked. The per-generation worker restart
  was flagged as a fallback risk here but never implemented.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: Seedscale at N_EVAL_SEEDS=4, N_GEN=20
* **Status**: completed
* **Relevance**: Direct ancestor 2 hops upstream. Introduced `N_EVAL_SEEDS=4`, `N_GEN=20`, and the
  silence-corner artifact that motivated the `SILENCE_SPIKE_COUNT_THRESHOLD=10` guard. Cost watchdog
  saved the run before gen 20.

### [t0103]

* **Task ID**: `t0103_extract_baden_2016_ds_morphologies`
* **Name**: Baden 2016 morphology extraction
* **Status**: completed
* **Relevance**: Reviewed for relevance; not used by t0106 (Baden morphologies are not the t0106
  substrate).

### [t0104]

* **Task ID**: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* **Name**: 2-objective NSGA-II, DSI silence guard, 3 GA seeds
* **Status**: completed
* **Relevance**: Direct parent of t0106. Whole code directory is the verbatim-copy base. Source of
  all evaluator, driver, and infrastructure code; t0106 is a tight evaluator fork with seven patched
  files.
