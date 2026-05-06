---
spec_version: "1"
task_id: "t0083_bedb_v3_extend_nsga2_gen8plus"
research_stage: "code"
tasks_reviewed: 4
tasks_cited: 4
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-05-05"
status: "complete"
---
# Research Code: Extending t0081 NSGA-II from Gen-7 with Adaptive HV-Plateau Stop

## Task Objective

Continue NSGA-II from t0081's gen-7 final population for at least 5 more generations on the same v3
dendritic-spike-augmented Bed B substrate, with an adaptive hypervolume-plateau stop rule (relative
HV improvement averaged over a 3-generation window < 1%, evaluated from gen 11 onwards) and a hard
cap of 10 additional generations (max gen 17). Reuse t0081's harness verbatim with only two surgical
modifications: replace the 96-cell warm-start sampling with t0081's gen-7 surviving population
(parameter vectors + pre-computed objective values, marked as already evaluated so pymoo skips
re-evaluation), and add an HV-plateau watchdog atop t0081's existing HV trajectory machinery. Reuse
the `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset and the
`instance_lifetime_hr * $0.2382/hr` cost-cap watchdog with the new $5.00 cap. Same Vast.ai EPYC 7B13
64-core class.

## Library Landscape

A single library is relevant: **`de_rosenroll_2026_dsgc_ais_dendritic_spike`** (registered under
[t0080], at
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/`).
It is the v3 substrate library with 24 `module_paths` (8 Python modules under `code/`, 13 t80
namespace MOD files, plus the `nsga2_loop`, `paths`, `bootstrap` glue) and 7 entry points:
`build_dsgc_cell_with_ais`, `apply_parameter_vector`, `DSGCCellWithAIS`, `ParameterVector`,
`BedBV3Problem`, `run_nsga2_loop`, `evaluate_parameter_vector`. Aggregator output reflects no
corrections on this asset. t0083 reuses it via Python imports
(`from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code...`); no copy or fork. The upstream
`de_rosenroll_2026_dsgc_ais` library [t0078] and the base `de_rosenroll_2026_dsgc` library [t0024]
are loaded transitively — t0083 does not reference them directly. No other libraries in the
project are relevant: t0083 needs neither cell models, nor scoring, nor visualisation utilities
beyond what the v3 library and t0081's task-local code already provide.

## Architecture Overview

t0083 is a **continuation run** — it inherits the t0081 architecture wholesale and adds two narrow
modules. The chain of imports flows downward:

```text
tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code     (library)
├── nsga2_loop.py            # BedBV3Problem (54-d, 2 obj, 1 ieq constraint),
│                            # cost watchdog, _save_pareto_front,
│                            # _save_all_evaluations, _save_hv_trajectory
├── trial_driver.py          # ProcessPoolExecutor: 8 dirs x 20 seeds = 160 sims
├── trial_helpers.py         # Per-trial setup
├── apply_params.py          # Write 54-d ParameterVector to NEURON cell
├── build_cell_ais.py        # AIS-augmented Bed B builder
├── extend_with_ais.py       # AIS extension on top of de Rosenroll
├── parametric_placer.py     # ACh + Mg-block NMDA co-located synapses
├── recorder.py              # Vm / spike recording
├── bootstrap.py             # NEURON init + MOD load
├── constants.py             # ParamIndex, LOWER/UPPER_BOUNDS, POP_SIZE=96, etc.
├── paths.py                 # File path constants
├── plot_results.py          # Pareto / HV / scatter charts
├── build_metrics.py         # metrics.json builder
└── mods/*.mod               # 13 t80 namespace channel mechanisms

tasks.t0081_bedb_v3_warmstart_nsga2.code                (task-local; copy into t0083)
├── warm_start.py            # 96-cell warm-start assembler (NOT used by t0083 directly;
│                            # superseded by t0083's gen-7 reload module)
├── run_loop.py              # 150 LOC thin wrapper: monkey-patches t0080 paths to t0081
│                            # results dir, builds Population.new("X", arr), runs NSGA-II
├── smoke_gate.py            # Re-evaluates t0080's 5 Pareto cells on the fresh remote
├── build_metrics.py         # 96 LOC metrics.json builder per Pareto cell
├── plot_results.py          # 123 LOC: Pareto / HV / all-cells scatter
└── paths.py                 # 43 LOC: t0081 RESULTS_DATA_DIR + dependency paths

tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code          (NEW)
├── paths.py                 # NEW: t0083 paths + dependency paths to t0081 outputs
├── reload_gen7.py           # NEW: rebuild gen-7 survivor pool from t0081 saved data
│                            # via NSGA-II RankAndCrowding survival
├── run_loop.py              # NEW: thin wrapper that injects gen-7 pop with F+G
│                            # marked as already evaluated, runs +N gens with HV-plateau watchdog
├── hv_plateau_watchdog.py   # NEW: monitors per-gen HV, flags termination on plateau
├── smoke_gate.py            # COPY from t0081: validate substrate consistency on remote
├── build_metrics.py         # COPY from t0081 (path-rebound): per-Pareto-cell metrics
└── plot_results.py          # COPY from t0081 (path-rebound): Pareto / HV / scatter
```

## Key Findings

### Pymoo NSGA-II population reload semantics

pymoo's `Initialization.do` ([pymoo/core/initialization.py]) accepts a `Population` instance
directly when `sampling=` is set to a `Population` object — see the conditional branch
`if isinstance(self.sampling, Population): pop = self.sampling`. Crucially, the comment in source
states "individuals might be already evaluated", and the same module then does
`not_eval_yet = [k for k in range(len(pop)) if len(pop[k].evaluated) == 0]` and only repairs those.
Downstream, `Evaluator.eval` ([pymoo/core/evaluator.py]) checks `skip_already_evaluated` (default
True) and filters with
`[i for i, ind in enumerate(pop) if not all([e in ind.evaluated for e in evaluate_values_of])]`.
This means: if individuals carry both `F` and `G` and have those keys in their `evaluated` set,
pymoo's first generation is essentially a no-op — no NEURON simulations are re-run. The recipe is:

```python
pop = Population.new("X", X_arr, "F", F_arr, "G", G_arr)
for ind in pop:
    ind.evaluated.update(["F", "G"])
algo = NSGA2(pop_size=96, sampling=pop, ...)
```

Confirmed empirically (`Population.new` accepts multiple key/value pairs by walking
`interleaving_args`; `evaluated` is a Python `set` on each `Individual` and is updateable). [t0081]
already used `sampling=Population.new("X", warm_array)` but did NOT supply F/G, so its gen 0 was
evaluated normally (96 NEURON runs); t0083 must add the F/G + evaluated marker to actually skip
re-evaluation.

### Recovering t0081's gen-7 final population from saved data

t0081's `code/run_loop.py:_run_warmstart_nsga2` (line 107) calls pymoo's
`minimize(..., n_gen=8, save_history=False)`. The full population history is therefore not persisted
as pickle objects. What IS persisted is
`tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` — a 51458-line JSON list
of 768 `CellEvaluation` records (gen 0..7, 96 each), each carrying `params` (54 floats, natural
units), `dsi`, `pd_rate_hz`, `is_unstable`, `is_feasible`, `constraint_violation`, plus the metadata
fields. To reconstruct the gen-7 survivor pool — the 96 individuals that NSGA-II's
`RankAndCrowding` selected from gen 6 + gen 7's combined 192 evaluations to be parents of gen 8 —
t0083 must:

1. Take the 192 records with `generation in {6, 7}` from `all_evaluations.json`.
2. Build a pymoo `Population` with `X = params`, `F = (-dsi, -pd_rate_hz)` (sign-flip for
   minimisation, matching `BedBV3Problem._evaluate` line 188-189 of t0080),
   `G = constraint_violation` (already in pymoo's <=0-feasible convention).
3. Replace worst-case sentinels per t0080 line 184-187: cells where `is_unstable=True` had
   `dsi_to_record = WORST_CASE_DSI = -1.0` and `pd_rate_to_record = WORST_CASE_RATE_HZ = 0.0`. The
   recorded `dsi`/`pd_rate_hz` fields hold the *unmodified* eval result, so the F injection must
   apply the same fallback logic to match what NSGA-II saw.
4. Mark each individual's `evaluated` set as `{"F", "G"}`.
5. Run pymoo's `RankAndCrowding().do(problem=BedBV3Problem(...), pop=pop192, n_survive=96)` — see
   source at `pymoo/algorithms/moo/nsga2.py` `RankAndCrowding._do`. This replicates the
   deterministic survival t0081 performed at end-of-gen-7. Note the `random_state` argument controls
   the crowding-distance tie-break randomization; for reproducibility t0083 must pass an explicit
   seed (e.g. `np.random.default_rng(seed=t80_loop.LHS_SEED)`).
6. The resulting 96-individual `Population` becomes t0083's `sampling=`.

This procedure recovers exactly the gen-7 survivors with the original deterministic NSGA-II
selection, and is the cleanest way to continue without re-evaluating any cells. Alternative
"approximate continuation" (just take all 96 gen-7 offspring, ignoring gen-6 carryovers) would
*lose* up to 96 high-quality gen-6 survivors that NSGA-II elite-preserved — including some Pareto
cells from gen 6 that gen 7 did not improve upon. The exact-survivor reload is mandatory.

### Cost-cap watchdog reuse pattern from t0081

t0081's harness (which is t0080's harness with path overrides) embeds a module-level cost watchdog
at `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/nsga2_loop.py` lines 89-123: globals
`_LOOP_START_TIME`, `_HOURLY_RATE_USD`, `_HARD_BUDGET_USD`, `_BUDGET_TRIPPED`, with helper
`_elapsed_cost_usd()` returning `(elapsed_s / 3600.0) * _HOURLY_RATE_USD` and trip-handler
`_trip_budget_overrun_if_needed()` writing `tasks/<task>/intervention/budget_overrun.md` once and
returning True thereafter. On trip, `BedBV3Problem._evaluate` (line 160-166) sets the worst-case
sentinel `f[i, 0] = -WORST_CASE_DSI; f[i, 1] = -WORST_CASE_RATE_HZ` and `g[i, 0] = 100.0` so
dominated infeasible offspring are produced for the rest of the call — pymoo's loop then exits
cleanly at end-of-generation with the partial Pareto front intact. t0081 raised the cap by setting
`t80_loop._HARD_BUDGET_USD = 3.00` after import (line 73 of t0081's `run_loop.py`); t0083 reuses
this exact pattern with `_HARD_BUDGET_USD = 5.00`. The hourly rate is the same `$0.2382/hr` (t0080
constant `HOURLY_RATE_USD`).

### Hypervolume computation and plateau-detection hook

t0081 reuses t0080's `_save_hv_trajectory` (`tasks/t0080_.../code/nsga2_loop.py` lines 288-316),
which sorts evaluations by generation, accumulates feasible non-unstable cells across generations,
and computes
`pymoo.indicators.hv.Hypervolume(ref_point=[-REF_POINT_DSI, -REF_POINT_RATE_HZ]).do( obj_v)` per
generation. The output is `results/data/hv_trajectory.json`, with utopia point `[0.7, 80.0]` (t0080
constants `HV_UTOPIA_DSI` and `HV_UTOPIA_RATE_HZ`, lines 546-547). t0081's actual trajectory: 6.59,
8.99, 9.24, 11.08, 11.57, 13.14, 15.22, 16.33 — strictly monotone, gen 7-vs-gen 6 delta = +7.4%,
no sign of plateau. The HV-plateau watchdog for t0083 plugs in at the same place: a new function
`should_stop_for_plateau(hv_history: list[float], min_gens_after_resume: int = 5, window: int = 3, rel_threshold: float = 0.01)`
returns True when `len(hv_history) >= 11` AND for the last 3 gens, mean of
`(hv_history[g] - hv_history[g-3]) / hv_history[g-3] < rel_threshold`. The trigger schedule: gen 8
finishes -> hv_history has 9 entries (0..8); gen 11 finishes -> 12 entries, the window is gens
8/9/10/11 against gens 5/6/7/8 lookbacks. Earliest stop = end of gen 11. Hard cap = end of gen 17
(i.e. n_gen=10 additional gens).

### How to inject the watchdog into pymoo's loop

pymoo's `minimize(problem, algorithm, ("n_gen", N), ...)` runs the algorithm to completion. To stop
early, two clean options exist:

1. **Use a custom pymoo `Termination` object** that subclasses `pymoo.core.termination.Termination`
   and exposes `_update(algorithm)` returning True when stop. The watchdog reads `algorithm.n_gen`
   and queries the saved HV trajectory at gen end. This is the documented pattern and fits cleanly
   with `("n_gen", 10)` as a max bound combined via `TerminationCollection`.
2. **Use a pymoo `Callback`** that runs `_save_hv_trajectory` after each generation and sets
   `algorithm.termination.force_termination = True` (deprecated but works). Less clean than option
   1\.

Recommendation: option 1, with `MaxGenerationTermination(10)` (additional gens) plus a custom
`HVPlateauTermination` combined via `TerminationCollection`. This keeps the watchdog logic local to
t0083 without touching t0080's nsga2_loop module.

### Generation-numbering continuity

t0081's `BedBV3Problem._evaluate` computes `gen = self.eval_count // POP_SIZE` (line 156 of t0080's
nsga2_loop.py), where `POP_SIZE = 96`. For t0083, the *new* `BedBV3Problem` instance starts from
`eval_count=0`, so it would record the resumed gen 0 as "gen 0" — overlapping t0081's gen 0
numbering. Two clean options:

1. **Pre-set** `problem.eval_count = 96 * 8 = 768` before calling `minimize()`. Then the resumed gen
   0 (which is t0081's gen 7 survivors and is skipped due to pre-evaluation) is recorded as "gen 8"
   if any cells WERE re-evaluated, and the first true continuation gen is "gen 8". This matches the
   task description's "starts at gen 8".
2. **Concatenate offline**: keep t0083's `_ALL_EVALUATIONS` independent (gen 0..N-1) and shift gen
   indices by +8 when merging into the unified `all_evaluations.json` per task description's "Notes"
   section.

Option 1 is preferred — it keeps the running JSON consistent during the live run and avoids a
post-hoc rewrite. Note: with skip-already-evaluated, the gen-7 survivors do not increment
`eval_count` (the `_evaluate` body never runs for them), so the first real evaluation (gen 8
offspring) lands at `eval_count=768`, generation `768//96=8`. Correct.

### Substrate consistency: skip the smoke gate

t0081's smoke gate (`code/smoke_gate.py`, 145 LOC) re-evaluated the 5 t0080 Pareto cells on a fresh
Vast.ai instance and confirmed DSI / PD reproduce within `DSI_TOLERANCE=0.05` /
`PD_TOLERANCE_HZ=1.0`. For t0083, a smoke gate has stronger value: re-evaluate a sample of t0081's
gen-7 survivors (e.g. the joint-pass cell 767 + 4 Pareto cells) on the new Vast.ai instance to
confirm the substrate reproduces t0081's recorded DSI/PD before continuing. If reproducibility
fails, the gen-7 reload is poisoned. Implementation: copy `code/smoke_gate.py` from t0081 into t0083
verbatim, swap the input source from `T0080_PARETO_FRONT_JSON` to t0081's `pareto_front.json`, keep
tolerances identical.

### Path management pattern

t0081's `code/run_loop.py:_redirect_t80_paths_to_t81` (lines 48-57) is a clean monkey-patch:
overwrite t0080's module-level `PARETO_FRONT_JSON`, `RESULTS_DATA_DIR`, `INTERVENTION_DIR`,
`BUDGET_OVERRUN_MD` constants in-place after import. The `_save_*` helpers compute path from the
module-level constant at call time, so this works without further plumbing. t0083 must replicate the
pattern but redirect to its own `tasks/t0083_.../results/data/` directory.

### Saving the union of t0081 + t0083 evaluations

Per task description's "Notes" section, the final `all_evaluations.json` must contain the union of
t0081's 768 cells + t0083's additional cells with consistent generation numbering. Two clean moments
to merge:

1. **Pre-run**: load t0081's `all_evaluations.json` into `_ALL_EVALUATIONS` before `minimize()`.
   Then t0083's `_save_all_evaluations` writes the combined list. Implies `eval_count` pre-set to
   768 (per the previous finding), so generation indexing is naturally consistent.
2. **Post-run**: keep t0083's evaluations as gen 0..N and merge offline.

Option 1 is preferred — fewer moving parts and consistent live-running JSON.

## Reusable Code and Assets

### `BedBV3Problem` class — import via library

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/nsga2_loop.py`, lines 126-220
* **Reuse method**: **import via library** (`de_rosenroll_2026_dsgc_ais_dendritic_spike` entry point
  `BedBV3Problem`)
* **Signature**: `BedBV3Problem(*, max_workers: int)`. Inherits pymoo `Problem` with
  `n_var=54, n_obj=2, n_ieq_constr=1, xl=LOWER_BOUNDS, xu=UPPER_BOUNDS`.
* **What it does**: maps a 54-d natural-unit parameter vector to (DSI, PD rate) objectives via
  NEURON simulation. Enforces AIS-to-soma Nav ratio >= 5 as `g(x) = 5 - nav16_ais/nav16_soma`.
* **Adaptation needed**: none — t0083 reuses the class verbatim.

### `evaluate_parameter_vector` function — import via library

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_driver.py`
* **Reuse method**: **import via library** (entry point of the v3 substrate library)
* **What it does**: 8 directions x 20 seeds x 1400 ms FULL HH simulation, returns
  `EvalResult(dsi, pd_rate_hz, is_unstable, peak_vm_mv)`.
* **Adaptation needed**: none.

### Cost-cap watchdog (module-level globals + helper) — copy into task

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/nsga2_loop.py`, lines 89-123 +
  the early-exit branch in `_evaluate` (lines 158-166)
* **Reuse method**: **copy into task** (already accessible via library import, but t0083 needs to
  override `_HARD_BUDGET_USD = 5.00`; t0081 demonstrates the monkey-patch pattern in `run_loop.py`
  line 73)
* **What it does**: per-cell elapsed-time check; trips on
  `(elapsed_s/3600) * _HOURLY_RATE_USD >= _HARD_BUDGET_USD`, writes
  `intervention/budget_overrun.md`, sets sentinel objectives so pymoo exits cleanly at
  end-of-generation.
* **Adaptation needed**: change cap from $3.00 (t0081 override) to $5.00 (t0083 spec). Path patch is
  the same monkey-patch t0081 uses.
* **Line count**: ~35 lines of import-and-set code in `code/run_loop.py`.

### `_save_pareto_front`, `_save_all_evaluations`, `_save_hv_trajectory` — import via library + path patch

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/nsga2_loop.py`, lines 246-316
* **Reuse method**: **import via library**, redirected via t0081's `_redirect_t80_paths_to_t81()`
  pattern (replicated for t0083)
* **What they do**: extract non-dominated feasible cells -> write `pareto_front.json`; dump full
  list -> `all_evaluations.json`; per-gen HV -> `hv_trajectory.json` with utopia point [0.7, 80].
* **Adaptation needed**: monkey-patch `RESULTS_DATA_DIR`, `PARETO_FRONT_JSON`, `INTERVENTION_DIR`,
  `BUDGET_OVERRUN_MD` to point at t0083's paths before calling.

### `code/smoke_gate.py` — copy into task

* **Source**: `tasks/t0081_bedb_v3_warmstart_nsga2/code/smoke_gate.py` (145 LOC)
* **Reuse method**: **copy into task** (per cross-task rule: not a library)
* **What it does**: re-evaluates a small list of cells on the fresh remote and confirms DSI/PD
  reproduce within tolerance. Writes `logs/smoke_gate.json`.
* **Adaptation needed**: change input source from `T0080_PARETO_FRONT_JSON` (t0081's reference) to
  t0081's `pareto_front.json` (t0083's reference). Optionally subset to 5 cells incl. cell 767 to
  contain remote-runtime cost. Tolerances `DSI_TOLERANCE=0.05` and `PD_TOLERANCE_HZ=1.0` unchanged.
* **Line count**: ~145 lines (verbatim) + ~15 lines of path/source rebinding.

### `code/build_metrics.py` — copy into task

* **Source**: `tasks/t0081_bedb_v3_warmstart_nsga2/code/build_metrics.py` (96 LOC)
* **Reuse method**: **copy into task**
* **What it does**: reads `pareto_front.json` + `all_evaluations.json`, builds metrics.json with one
  variant per Pareto cell + closest-to-joint cell. Tags `joint_pass` dimension when DSI>=0.4 AND
  PD>=10 Hz.
* **Adaptation needed**: change the `from tasks.t0081_... import paths` line to
  `from tasks.t0083_... import paths`. Logic and metric registration unchanged.
* **Line count**: ~96 lines (verbatim) + ~3 lines of import rebinding.

### `code/plot_results.py` — copy into task

* **Source**: `tasks/t0081_bedb_v3_warmstart_nsga2/code/plot_results.py` (123 LOC)
* **Reuse method**: **copy into task**
* **What it does**: emits `images/pareto_front.png`, `images/hypervolume_trajectory.png`,
  `images/all_cells_scatter.png`. Marks joint-pass cells with green annotation.
* **Adaptation needed**: same import rebinding to t0083's `paths`. May add a vertical line at
  generation 8 on the HV trajectory plot to mark the t0081/t0083 boundary.
* **Line count**: ~123 lines (verbatim) + ~3 lines of import rebinding.

### `code/paths.py` — copy into task (with rebind)

* **Source**: `tasks/t0081_bedb_v3_warmstart_nsga2/code/paths.py` (43 LOC)
* **Reuse method**: **copy into task** (paths must be task-local)
* **What it does**: defines task-local result/data/images/intervention paths plus the dependency
  pointers (`T0080_PARETO_FRONT_JSON`, `T0078_PARETO_FRONT_JSON`).
* **Adaptation needed**: t0083 needs new dependency pointers to t0081's outputs:
  `T0081_ALL_EVALUATIONS_JSON`, `T0081_PARETO_FRONT_JSON`, `T0081_HV_TRAJECTORY_JSON`.
* **Line count**: ~50 lines.

### `code/run_loop.py` — adapt from t0081

* **Source**: `tasks/t0081_bedb_v3_warmstart_nsga2/code/run_loop.py` (150 LOC) as the structural
  template
* **Reuse method**: **copy into task** then modify
* **What changes from t0081**:
  - Replace `from .warm_start import assemble_warm_start_population` with
    `from .reload_gen7 import reload_t0081_gen7_survivors`.
  - Replace `Population.new("X", warm_array)` with the F+G-equipped Population from the reload
    function.
  - Pre-set `problem.eval_count = 768` so `gen = eval_count // POP_SIZE` produces gen-8 numbering on
    the first true offspring.
  - Pre-load `_ALL_EVALUATIONS` from t0081's `all_evaluations.json` so the saved JSON is the union.
  - Wire in the HV-plateau termination via `pymoo.core.termination.Termination` subclass combined
    with `MaxGenerationTermination(10)` via `TerminationCollection`.
  - Override hard budget cap: `t80_loop._HARD_BUDGET_USD = 5.00`.
* **Line count**: ~180 lines (similar size to t0081's; +30 LOC for HV-plateau wiring and pre-load of
  `_ALL_EVALUATIONS`).

### t0081's gen-7 evaluation data — input dataset

* **Source**: `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` (768 records)
  + `pareto_front.json` (16 cells) + `hv_trajectory.json` (8 entries)
* **Reuse method**: **read at runtime** (not library; not copy — these are upstream task results)
* **What it provides**: 768 `CellEvaluation` records (cell_index, generation, params [54 floats],
  dsi, pd_rate_hz, is_unstable, peak_vm_mv, elapsed_s, constraint_violation, is_feasible). The
  generation-6 + generation-7 subset (192 records) is the input to the gen-7 survivor reload.
* **Adaptation needed**: read-only. Apply worst-case sentinel substitution for `is_unstable=True`
  cells (matching t0080's `dsi_to_record`/`pd_rate_to_record` logic at line 184-187) before
  injecting F.

## Lessons Learned

### t0081 ran cleanly under-budget — same operational envelope works

t0081's $2.39 actual vs $3.00 cap (80% of cap, 0% over) on 768 cells / 10.045 h instance lifetime
proves the EPYC 7B13 64-core class delivers the cost-per-cell that the cost-cap math assumes
($0.00284/cell). For t0083 with ~480-960 expected cells (5-10 additional gens at pop 96), the
projected envelope is $1.36-$2.73 + ~$0.20 instance overhead — well under the $5.00 hard cap, with
~85% headroom for per-cell wall-clock variance. The cost-cap watchdog is a defensive backstop, not a
primary planning constraint.

### Substrate stability: 0/768 unstable cells in t0081

t0081's `unstable=0/768` (vs t0080's 0/192 and t0078's 0/491) confirms the v3 substrate's hard
biological bounds (`nav16_ais >= 0.25` per Kole 2008 + AIS-to-soma Nav ratio >= 5 per Werginz 2024)
combined with the dendritic-spike machinery do not introduce instability. t0083 inherits this
stability — no extra substrate validation is required beyond a 5-cell smoke gate.

### Worst-case sentinel substitution must match what NSGA-II saw

In t0080's `_evaluate` (lines 184-187 of `nsga2_loop.py`), unstable cells have their objectives
*overwritten* with `WORST_CASE_DSI=-1.0` and `WORST_CASE_RATE_HZ=0.0` BEFORE pymoo sees them,
whereas the saved `CellEvaluation` records the *unmodified* `eval_res.dsi` and `eval_res.pd_rate_hz`
plus an `is_unstable` flag. When t0083 rebuilds the Population from `all_evaluations.json` for the
gen-7 survivor reload, it must apply the same substitution to F to match the values NSGA-II actually
used for ranking. Failing this would produce different survivors than what NSGA-II selected at
end-of-gen-7 (and break continuity with t0081's saved Pareto front and HV trajectory). A unit test
that re-derives t0081's saved gen-7 front from the reload + dummy-gen-0-offspring should match
exactly.

### HV monotonicity is fragile under 1% threshold

t0081's HV trajectory: `[6.59, 8.99, 9.24, 11.08, 11.57, 13.14, 15.22, 16.33]`. The smallest
delta-pct between adjacent gens is 2.7% (gen 1->2); the delta from gen 6 to gen 7 is 7.4%. A 1%
average-over-3-gen threshold is therefore tight but not unreasonable: NSGA-II in this regime
naturally settles into 1-3% per-gen improvements when the front is dense. The threshold may fire
between gen 11 and gen 14 if the trajectory's growth continues to decelerate, or never (in which
case the gen-17 hard cap activates). The "Acceptable negative" pass criterion in the task
description recognises this — a flat HV with isolated cell 767 is a publishable architectural
finding.

### Pymoo `save_history=False` is a one-way door for population state

t0081 used `save_history=False` to keep memory low; this means the in-process `Population` object of
gen-7 survivors is gone the moment `minimize()` returns. Recovery is only possible via the
`all_evaluations.json` -> 192-individual rebuild -> `RankAndCrowding` survival pipeline described
above. For future continuation tasks (t0083 + similar), it would be cleaner to add a
checkpoint-on-end mechanism that pickles the final `algorithm.pop` to disk; a follow-up suggestion
should propose this. For t0083 itself, the rebuild path is the only available option and works
deterministically given the seed.

### Smoke gate caught nothing in t0081 — but is still mandatory

t0081's smoke gate ran 5 t0080 Pareto cells on the fresh Vast.ai instance and reported all 5 PASS
(per `results_summary.md` REQ-7 verification). Although the gate detected no problem, the ~5-minute,
~$0.02 cost is justified as a regression detector against MOD-compile drift, NEURON version drift,
and instance-class drift. t0083 should run the gate against a 5-cell sample of t0081's gen-7 Pareto
cells (incl. cell 767) before launching the continuation NSGA-II run.

## Recommendations for This Task

1. **Add no new library**. Reuse `de_rosenroll_2026_dsgc_ais_dendritic_spike` from [t0080] verbatim
   via Python import. No substrate changes whatsoever.

2. **Write 4 new modules under `tasks/t0083_.../code/`**:
   - `paths.py` (~50 LOC): t0083 paths + dependency pointers to t0081 outputs.
   - `reload_gen7.py` (~120 LOC): load t0081's gen 6 + gen 7 from `all_evaluations.json`, rebuild
     192-individual `Population` with X/F/G + `evaluated={"F","G"}`, run pymoo `RankAndCrowding`
     with explicit seed, return 96-individual gen-7 survivor `Population`.
   - `hv_plateau_watchdog.py` (~80 LOC): pymoo `Termination` subclass with `_update(algorithm)`
     reading the HV trajectory at end-of-gen, returning True when `len(hv_history) >= 11` AND mean
     of last 3 relative HV improvements < 1%. Expose unit-testable function
     `should_stop(hv_history, min_gens=5, window=3, rel_threshold=0.01)`.
   - `run_loop.py` (~180 LOC): adapt from t0081's `run_loop.py` per "Reusable Code and Assets"
     section above. Combines `MaxGenerationTermination(10)` and the HV-plateau termination via
     `TerminationCollection`. Pre-sets `problem.eval_count = 768` and pre-loads `_ALL_EVALUATIONS`
     from t0081's saved JSON for unified output.

3. **Copy 3 modules from t0081 verbatim with import rebinding**: `smoke_gate.py`,
   `build_metrics.py`, `plot_results.py`. ~10 LOC of edits per file (rebind
   `from tasks.t0081_... import paths` to `from tasks.t0083_... import paths`).

4. **Do NOT copy `warm_start.py`** from t0081. It is superseded by `reload_gen7.py`.

5. **Run a 5-cell substrate-consistency smoke gate** on the fresh Vast.ai instance before launching
   the continuation. Sample t0081's cell 767 (joint-pass) + 4 other Pareto cells across gens 4-7 to
   span the front. PASS = all 5 within DSI±0.05 / PD±1 Hz.

6. **Override the cost-cap to $5.00** by monkey-patching `t80_loop._HARD_BUDGET_USD = 5.00` in
   `run_loop.py` (one line; matches t0081's pattern).

7. **Keep generation numbering continuous** by pre-setting `problem.eval_count = 768` so the first
   continuation generation is recorded as gen 8 in `all_evaluations.json` and `hv_trajectory.json`.
   Also pre-load `_ALL_EVALUATIONS` with t0081's 768 records so the saved files contain the union.

8. **Reuse the same Vast.ai instance class** (AMD EPYC 7B13 64-core, 503 GB RAM, $0.2382/hr). Same
   `code/run_remote.sh` pattern as t0080/t0081.

9. **Write a unit test** in `tasks/t0083_.../code/test_reload_gen7.py` that verifies the
   `reload_gen7` output's Pareto cells match t0081's saved `pareto_front.json` exactly (16 cells,
   identical cell_index list). This catches sentinel-substitution bugs and seed mismatches.

10. **Suggest a framework improvement** in this task's `suggestions.json`: add a checkpoint-on-end
    `pickle.dump(algorithm.pop, ...)` to the t0080 nsga2_loop, so future continuation tasks need not
    rebuild the survivor pool from `all_evaluations.json`. This is the cleanest fix for the
    `save_history=False` lesson learned.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC NEURON model
* **Status**: completed
* **Relevance**: Provides the base de Rosenroll 2026 DSGC NEURON port that all subsequent Bed B
  substrate work derives from. The base library `de_rosenroll_2026_dsgc` is loaded transitively by
  the v3 library that t0083 uses; t0083 does not import it directly.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B v2 MOBO with AIS extension and tiered AHP
* **Status**: completed
* **Relevance**: Provides the upstream `de_rosenroll_2026_dsgc_ais` library and the 49-d ParamIndex
  layout that t0080 extended to 54-d. Loaded transitively. Also provides the original cost-cap
  watchdog pattern and the hypervolume-utopia-point convention `[0.7, 80]` that t0081/t0083 inherit.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Hosts the `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset (54-d v3
  substrate) that t0083 reuses verbatim, the `BedBV3Problem` pymoo Problem subclass, and all
  reusable nsga2_loop infrastructure (cost watchdog, HV trajectory, save helpers). Source of the
  baseline Pareto front (5 cells) for substrate-consistency comparison.

### [t0081]

* **Task ID**: `t0081_bedb_v3_warmstart_nsga2`
* **Name**: Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start
* **Status**: completed
* **Relevance**: Direct parent task. Provides the gen-7 final population (96 individuals), the
  thin-wrapper pattern (`run_loop.py`, `_redirect_t80_paths_to_t81`), and the `smoke_gate`,
  `build_metrics`, `plot_results` modules t0083 copies. Provides `all_evaluations.json` (768
  records), `pareto_front.json` (16 cells), and `hv_trajectory.json` (8 entries) as t0083 inputs.
  Established the Vast.ai EPYC 7B13 cost envelope ($2.39 / 768 cells / 10.045 h).
