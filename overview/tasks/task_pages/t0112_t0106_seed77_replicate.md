# ⏹ Seed-77 minimum-change replicate of t0106 long 2-direction NSGA-II

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0112_t0106_seed77_replicate` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Task types** | `experiment-run` |
| **Expected assets** | 1 predictions |
| **Task folder** | [`t0112_t0106_seed77_replicate/`](../../../tasks/t0112_t0106_seed77_replicate/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0112_t0106_seed77_replicate/task_description.md)*

# t0112: Seed-77 Minimum-Change Replicate of t0106 Long 2-Direction NSGA-II

## Motivation

`t0106_long_pdnd_nsga2_300gen` produced the first joint-pass cells (DSI >= 0.5 AND PD-rate >=
30 Hz) in the entire `t0080` -> `t0104` NSGA-II lineage: **123 unique cells across 3,744
evaluations** from a single random-init GA seed (44) running 40 generations on the 68-d Bed B
+ 14-d morphology substrate. The breakthrough was driven by reformulating the selectivity
objective from 16-direction vector-sum DSI to 2-direction ratio DSI = (PD - ND) / (PD + ND),
not by additional compute.

Two open caveats motivate this task:

1. **Seed-specificity**: t0106 ran a single GA seed. Without at least one replicate, the 3.3%
   joint-pass acceptance rate is a single-realisation point estimate, not a substrate
   property. It cannot be reported as such in any future writeup.

2. **NEURON memory creep**: t0106's `_POOL_RESTART_EVERY = 25` (in `nsga2_driver.py:97`) was
   chosen before the long-horizon behaviour of the worker pool was characterised. Wall-clock
   telemetry from t0106 shows growing per-evaluation memory footprint between restarts,
   consistent with NEURON's known leak under repeated cell instantiation. A tighter restart
   cadence (every 10 generations) reduces this footprint at negligible wall-clock cost (~2
   extra minutes over a 40-gen run).

This task addresses both with a single minimum-change replicate.

## Scope

* **In scope**: identical substrate to t0106 (Bed B 54-d electrophys + 14-d morphology = 68
  free parameters), identical objectives (2-direction ratio DSI + PD-rate at 0 deg), identical
  NSGA-II hyperparameters (pop=96, SBX/PM operators, HV-plateau operator-stop criterion),
  identical evaluation protocol (N_EVAL_SEEDS = 3, ratio DSI, silence guard active).
* **In scope, changed**: GA seed (44 -> 77), pool-restart cadence (25 -> 10 gens), gen ceiling
  (300 -> 60 to keep budget bounded while still allowing slower plateaus to be discovered).
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, or the NSGA-II driver beyond the seed and
  pool-restart constants. Out-of-scope changes would compromise the like-for-like comparison.

## Approach

1. **Fork t0106 code into `tasks/t0112_t0106_seed77_replicate/code/`**: copy
   `nsga2_driver.py`, `constants.py`, `random_init.py`, and any helper modules. Update package
   imports.
2. **Change exactly two constants**:
   * `constants.py`: rename `T0106_SEEDS = (44,)` -> `T0112_SEEDS = (77,)`; bump
     `T0112_HARD_BUDGET_USD` if needed (default to $25 per-task cap).
   * `nsga2_driver.py:97`: `_POOL_RESTART_EVERY = 10` (was 25).
3. **Raise gen ceiling**: `N_GEN = 60` in `constants_morphology` import override, with
   HV-plateau stop preserved verbatim. The HV-plateau constants (`HV_PLATEAU_WINDOW`,
   `HV_PLATEAU_MIN_HV_HISTORY`, `HV_PLATEAU_REL_THRESHOLD`) are unchanged so the stopping
   criterion is identical to t0106.
4. **Smoke gate locally** (5 checks identical to t0106): single-eval driver run, ratio DSI
   synthetic sanity, silence-guard unit tests, pool-restart sanity, watchdog wiring.
5. **Provision remote** Vast.ai single instance (same provisioning class as t0106).
6. **Launch** with cost cap $25 per-task default and per-instance watchdog $20. Operator-stop
   on HV plateau (same window/threshold as t0106) or at gen 60 ceiling, whichever comes first.
7. **Collect** evaluator-side per-cell DSI / PD-rate / generation table as a predictions asset
   following the t0106 predictions asset format.
8. **Compare** to t0106:
   * Joint-pass cell count (DSI >= 0.5 AND PD >= 30 Hz) absolute number and as % of total
     evals.
   * Best ratio DSI and best PD-rate frontier vs t0106's 1.0000 / 122.6 Hz.
   * HV trajectory shape and plateau generation.
   * Pareto front overlap between seed-44 and seed-77 cells (parameter-space distance).

## Expected Assets

* **1 predictions asset** under `assets/predictions/t0112-bedb-morph-nsga2-seed77/` containing
  the per-cell DSI / PD-rate / generation table for all evaluated cells (mirroring t0106's
  predictions asset schema).

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is
  for CPU cores, not GPU.
* **Remote**: Vast.ai single instance, same provisioning class as t0106 (high-core-count CPU
  node).
* **Cost cap**: $25 per-task default. **Per-instance watchdog**: $20 (via
  `make_watchdog_from_machine_log`).
* **Expected actual cost**: ~$10-11 (mirroring t0106's $10.37 spend at the same pop/gen/eval
  budget).
* **Project envelope check**: $18.20 remaining of $75 prior to this task. Expected post-task
  reserve: ~$7-8.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `pareto_front_seed44_vs_seed77.png` — overlay of t0106 (seed 44) and t0112 (seed 77) strict
   Pareto fronts on DSI vs PD-rate axes; coloured by source task; answers "do the two seeds
   discover comparable Pareto frontiers?"
2. `hv_vs_gen_seed44_vs_seed77.png` — log-scale HV trajectory for both seeds on the same axes,
   with pool-restart events annotated; answers "does the tighter restart cadence change the HV
   trajectory shape?"
3. `joint_pass_yield_per_gen.png` — joint-pass cell count discovered per generation for both
   seeds; answers "when does each seed first hit the joint-pass corner, and what is the rate
   thereafter?"
4. `top50_morphologies_seed77.png` — 10x5 grid of best 50 cells, coloured by archetype (same
   format as t0106's `top50_morphologies.png`); answers "are the best-yield morphologies the
   same archetypes as t0106?"
5. `asymmetry_distribution_seed44_vs_seed77.png` — 4-panel histogram (soma offset, elongation,
   branch density gradient, primary branch PD concentration) for top-50 cells from both seeds;
   answers "is the morphology distribution of high-yield cells seed-independent?"

### Tables

* `results/data/joint_pass_summary.csv` — per-seed: total evals, joint-pass count, joint-pass
  %, best DSI, best PD-rate, plateau generation.
* `results/data/pareto_front_overlap.csv` — parameter-space nearest-neighbour distance between
  each t0112 Pareto cell and its closest t0106 Pareto cell; informs whether the two seeds find
  "the same" or "different" frontier solutions.

### Registered metrics

Run all registered metrics that apply to this task. Check `uv run python -u -m
arf.scripts.aggregators.aggregate_metrics --format json`. At minimum:

* `direction_selectivity_index` — best ratio DSI across all cells (variant: `best_legit` for
  the highest non-DSI=1.0 cell, plus the DSI=1.0 cell counts).
* `pd_rate_hz` — best PD-rate frontier (variant: `at_best_dsi`, `at_pareto_corner`).

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative
answer, not a hedge:

1. Does seed 77 produce >= 40 unique joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz)?
   * If yes: t0106 is replicated; substrate is genuinely populated.
   * If no but >= 10 unique cells: partial replication; multi-seed required.
   * If 0: t0106 was seed-specific; pivot strategy required.
2. Does seed 77's best ratio DSI reach or exceed 0.95?
3. Does seed 77's best PD-rate frontier reach or exceed 100 Hz?
4. Do the two seeds' Pareto fronts overlap in parameter space (median nearest-neighbour
   distance below the cross-seed noise floor)?
5. Did the tighter pool-restart cadence (every 10 gens) materially change the HV trajectory or
   wall-clock per generation vs t0106?

## Cross-References

* **Parent task**: `t0106_long_pdnd_nsga2_300gen` (substrate, driver, constants, baseline).
* **Caveat task**: `t0107_t0106_polar_8dir_recheck` (8-dir polar re-evaluation showing the
  conventional-protocol DSI is much lower; not in scope for this task but motivates a
  downstream re-evaluation across both t0106 + t0112 cells once t0112 completes).
* **Source suggestion**: none. This task generates new follow-up suggestions in its own
  `results/suggestions.json` based on the outcome.
* **Brainstorm source**: `t0111_brainstorm_results_22`.

</details>
