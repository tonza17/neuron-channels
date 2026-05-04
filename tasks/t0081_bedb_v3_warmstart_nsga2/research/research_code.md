---
spec_version: "1"
task_id: "t0081_bedb_v3_warmstart_nsga2"
research_stage: "code"
tasks_reviewed: 2
tasks_cited: 2
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-05-04"
status: "complete"
---
# Research Code: Reusable Code Inventory for t0081 Warm-Start NSGA-II

## Task Objective

Identify the prior-task code, libraries, and assets that t0081 reuses, plus the minimal new code
that t0081 must add. The task is a pure re-run of t0080 on the same v3 substrate at full plan scope
(pop=96 / gen=8 = 768 cells) with a combined warm-start initial population (5 t0080 Pareto cells
verbatim, 17 t0078 Pareto cells projected to 54-d, 74 fresh LHS).

## Library Landscape

* **`de_rosenroll_2026_dsgc_ais_dendritic_spike`** (t0080): the v3 substrate library bundling
  `build_cell_ais` + `extend_with_ais` extended with dendritic NMDA + distal Nav1.6 + NaP insertion.
  24 module_paths, 7 entry points. Reused unchanged.

This is the only project library directly relevant to t0081. The upstream
`de_rosenroll_2026_dsgc_ais` (t0078) and `de_rosenroll_2026_dsgc` (t0024) are transitively loaded by
the v3 library; t0081 does not reference them directly.

## Architecture Overview

t0081 reuses the t0080 architecture verbatim:

```
tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code
├── nsga2_loop.py           # NSGA-II main loop, BedBV3Problem, cost-cap watchdog
├── parametric_placer.py    # Synapse placement (ACh + Mg-block NMDA co-located)
├── apply_params.py         # Apply 54-d normalised params to NEURON cell
├── trial_helpers.py        # Per-trial setup (synapses, recordings)
├── trial_driver.py         # ProcessPoolExecutor: 8 dirs × 20 seeds = 160 sims
├── bootstrap.py            # NEURON init + MOD-file load
├── build_cell_ais.py       # AIS-augmented Bed B cell builder
├── extend_with_ais.py      # AIS extension on top of base de Rosenroll cell
├── constants.py            # ParamIndex, LOWER_BOUNDS, UPPER_BOUNDS
├── paths.py                # File path constants
├── cost_cap.py             # Cost-cap watchdog
├── build_metrics.py        # Build metrics.json from results
├── plot_results.py         # Pareto / HV / scatter charts
└── mods/*.mod              # 13 vendored t80 MOD files
```

t0081 adds:
```
tasks.t0081_bedb_v3_warmstart_nsga2.code
├── warm_start.py           # NEW: assemble 96-cell warm-started initial pop
└── run_loop.py             # NEW: thin wrapper invoking t0080's nsga2_loop with warm-start
```

The thin-wrapper pattern keeps t0080's harness unchanged and confines the warm-start novelty to
t0081.

## Key Findings

### No new MOD files

t0080's 13 t80 MOD files (Nav1.6, NaP, NaR, Kdr, Kv3, Kv4, Kv7, Ih, CaL, CaT, BK, SK, SK_AHP) plus
the t0024 `Exp2NMDA` POINT_PROCESS provide the full v3 mechanism set. t0081 does not introduce new
ion channels, synaptic mechanisms, or calcium dynamics.

### No new substrate library

The v3 dendritic-spike-augmented Bed B substrate exists as a published library asset in t0080. t0081
reuses it via Python import, not via copy. The library's `module_paths` exposes all the entry points
t0081 needs.

### One new Python module needed

`warm_start.py` (~80–120 LOC) assembles the 96-cell warm-started initial population:

* `load_t0080_pareto() -> np.ndarray` — reads `results/data/pareto_front.json` from t0080, returns
  the (5, 54) numpy array of `params` (already in normalised pymoo space).
* `load_and_project_t0078_pareto(*, rng_seed: int = 42) -> np.ndarray` — reads `pareto_front.json`
  from t0078, extracts `params_natural` (49-d), normalises each cell to [0, 1] using t0080's
  `LOWER_BOUNDS` / `UPPER_BOUNDS`, samples 5 new dims per cell from `numpy.random.uniform(0, 1)`
  with the seed, returns the (17, 54) numpy array.
* `generate_lhs_fill(*, n_samples: int = 74, problem: BedBV3Problem, rng_seed: int = 43) -> np.ndarray`
  — uses pymoo's `LHS()` operator to produce (74, 54).
* `assemble_warm_start_population(*, problem: BedBV3Problem) -> np.ndarray` — concatenates the
  three arrays into the (96, 54) starter population.
* `main()` CLI — writes the assembled array to `results/data/warm_start_population.json` for
  reproducibility.

### One thin wrapper

`run_loop.py` (~30–50 LOC) imports t0080's `nsga2_loop` machinery and substitutes
`NSGA2(pop_size=96, sampling=Population.new("X", custom_array))` for the LHS sampling. All
constraint handling, cost-cap watchdog, results saving, and ProcessPoolExecutor parallelism remain
unchanged.

### Parameter projection: t0078 (49-d natural) → 54-d normalised

t0078's `pareto_front.json` stores `params_natural` (49 floats in physical units like S/cm² for Nav
densities, mM for Mg conc, etc.). t0080's `pareto_front.json` stores `params` (54 floats in [0, 1]
normalised pymoo space). To use t0078 cells in t0081's NSGA-II:

```python
for i in range(49):
    normalised[i] = (natural[i] - LOWER_BOUNDS[i]) / (UPPER_BOUNDS[i] - LOWER_BOUNDS[i])
    normalised[i] = max(0.0, min(1.0, normalised[i]))  # clamp
for i in range(49, 54):
    normalised[i] = rng.uniform(0, 1)  # random LHS within the 5 new dims
```

Bounds invariance is guaranteed by t0080's REQ-21 (preserve t0078 49-d ParamIndex 0-48).

## Reusable Code and Assets

* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop` — main NSGA-II loop
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants.LOWER_BOUNDS` and `UPPER_BOUNDS`
  — 54-d parameter bounds
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants.ParamIndex` — enum for parameter
  indices
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.assets.library.de_rosenroll_2026_dsgc_ais_dendritic_spike`
  — full substrate library
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/data/pareto_front.json` — 17 t0078 Pareto cells
  in `pareto_cells[*].params_natural` (49-d natural units) + `dsi`, `pd_rate_hz`, `iteration`
* `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/data/pareto_front.json` — 5 t0080 Pareto
  cells in `cells[*].params` (54-d normalised) + `cell_index`, `generation`, `dsi`, `pd_rate_hz`,
  `is_feasible`, `is_unstable`

## Lessons Learned

From t0080:

* **Cells run sequentially**, not in parallel, when each cell saturates 64 cores via the trial
  driver's ProcessPoolExecutor. The plan must compute wall-clock as `n_cells × per_cell_seconds`,
  NOT `n_cells / n_cores`. t0080's planning step got this wrong; t0081's planning corrects it.

* **Per-cell measured cost on EPYC 7B13 64-core at $0.2382/hr is $0.00284**. Use this empirical rate
  for budget estimation.

* **The cost-cap watchdog works as designed** — it never tripped in t0080 because the run finished
  naturally well under cap. Reuse unchanged.

* **HV trajectory logging is coarse** — t0080's `nsga2_loop.py` writes the HV trajectory at a
  granularity that produced only 2 entries (gen 0 / gen 1) for an 8-generation run. Workable but not
  ideal. Optional improvement: log per generation. Not blocking for t0081.

* **Pareto front filtering** — t0080 correctly filters `is_unstable` and infeasible cells out of
  the saved Pareto front. Reuse unchanged.

* **The substrate-regression check (REQ-9 / REQ-16) was deferred** in t0080. t0081 should validate
  the 5 t0080 Pareto cells reproduce their recorded DSI / PD when re-evaluated on a fresh Vast.ai
  instance — this acts as a substrate-consistency smoke gate.

## Recommendations for This Task

1. **Write `warm_start.py` first** with full mypy + ruff checks before launching the run.
2. **Add a smoke gate** that re-evaluates the 5 t0080 Pareto cells (NOT the t0078-projected ones,
   which may produce different results due to random new-dim sampling) and confirms DSI / PD match
   within a tolerance (e.g., ±0.05 DSI, ±1 Hz PD). This is the substrate-consistency check t0080
   deferred.
3. **Use `Population.new("X", custom_array)`** as the pymoo sampling object. Verify the API matches
   pymoo 0.6.1.6 (the installed version on the Vast.ai instance per t0080).
4. **Cost-cap at $3.00** with the same watchdog; budget envelope $2.40 (768 × $0.00284 + $0.20
   overhead).
5. **Provision a fresh Vast.ai 64-core EPYC 7B13** at the same class as t0080 instance 36137287;
   expect $0.16-$0.24/hr.

## Common Patterns

* All code in `code/` directory
* Centralised path constants in `paths.py` (reuse t0080's by import + extend with t0081 paths)
* Constants for column names + dtypes in `constants.py`
* No relative imports; absolute paths from project root via `tasks.tNNNN_*.code.*`
* Run all CLI commands via `arf.scripts.utils.run_with_logs --task-id t0081_*`

## Estimated Total New LOC

* `code/warm_start.py`: ~100 LOC
* `code/run_loop.py`: ~40 LOC
* `code/paths.py`: ~20 LOC (just the t0081-specific paths; rest imported from t0080)

**Total new LOC: ~150-180**. The 700-LOC harness from t0080 is reused without modification.

## Task Index

* **t0078_bedb_mobo_v2_ais_tiered_ahp** — provides the 17-cell Pareto front (49-d natural-unit
  parameter vectors) used as warm-start seeds projected to 54-d. Status: completed.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** — provides the v3 substrate library, the NSGA-II
  harness, the 5-cell Pareto front (54-d normalised parameter vectors) used as verbatim warm-start
  seeds, and the cost-cap watchdog reused at $3.00 cap. Status: completed.
