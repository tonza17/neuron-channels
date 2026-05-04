# Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start

## Motivation

t0080 ran NSGA-II on the v3 dendritic-spike-augmented Bed B substrate at a heavily reduced scope
(pop=24 / gen=8 = 192 cells; 5% of the planned 96 / 40 = 3,840 cells) due to a planning-stage
miscalculation about cell parallelism. The result was a clean architectural negative outcome (best
Pareto cell DSI 0.127 / PD 2.54 Hz; pass criterion `DSI ≥ 0.4 AND PD ≥ 10 Hz` missed by a wide
margin), but the small budget makes it impossible to distinguish a fundamental substrate limitation
from undersampled NSGA-II convergence.

This task re-runs NSGA-II on the **same t0080 v3 substrate** at **pop=96 / gen=8 = 768 cells** (4×
the t0080 scope) with a **combined warm-start** from t0080 and t0078 Pareto cells, designed to give
the optimiser a strong head start in the 54-d search space.

Source suggestion: **S-0080-01** (with scope and strategy modifications agreed in conversation
before launch — see Approach for the deviations from the suggestion's literal text).

## Scope

### In scope

- Re-use the t0080 library asset `de_rosenroll_2026_dsgc_ais_dendritic_spike` and its 13 vendored
  MOD files unchanged. No new substrate work.
- Re-use the t0080 NSGA-II harness (`code/nsga2_loop.py` and friends) unchanged. The only change is
  the warm-start initialisation logic and the larger pop / gen counts.
- Generate the warm-start initial population:
  - **5 t0080 Pareto cells** verbatim (cells 58, 141, 153, 188, 190 from
    `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/data/pareto_front.json`). Already 54-d.
  - **17 t0078 Pareto cells** projected from 49-d to 54-d, with the 5 new dims (`GNMDA_DEND`,
    `MG_CONC_MM`, `VOFF_NMDA`, `NAV16_DEND_DISTAL`, `NAP_DEND_DISTAL`) sampled at **random LHS
    within their full ranges** — NOT zero. Source vectors from
    `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/data/pareto_front.json`.
  - **74 LHS-sampled cells** for diversity.
  - Total initial pop: **96 cells (22 seeded + 74 LHS)**.
- Run NSGA-II via pymoo: `NSGA2(pop_size=96)` with the 96-cell custom initial population, gen=8,
  default operators (SBX η=15, polynomial mutation η=20, tournament selection). Same hard
  biological lower bounds as t0080 (`nav16_ais ≥ 0.25 S/cm²`; AIS-to-soma Nav ratio ≥ 5).
- Pull `pareto_front.json`, `all_evaluations.json`, `hv_trajectory.json` from the remote.
- Generate the same charts as t0080: Pareto front, hypervolume trajectory, all-cells scatter.
- Compute per-cell registered metrics; identify the closest-to-joint Pareto cell.

### Out of scope

- Substrate redesign (still on the v3 dendritic-spike substrate from t0080).
- New MOD files (none needed).
- Library asset (re-uses t0080's; no new asset).
- Answer asset (the failure-mode answer asset already exists from t0080).
- Substrate regression check on t0076 iter-424 (still deferred; would be a separate small task).

## Approach

### Warm-start initial population

A new module `code/warm_start.py` in this task generates the 96-cell initial population:

1. Load the 5 t0080 Pareto cells from
   `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/data/pareto_front.json`
   (`cells[*].params`, each 54-d).
2. Load the 17 t0078 Pareto cells from
   `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/data/pareto_front.json` (`cells[*].params`, each
   49-d).
3. For each t0078 cell, project to 54-d:
   - Indices 0–48: copy verbatim (preserves t0078's 49-d ParamIndex layout, which t0080
     inherited).
   - Indices 49–53: sample uniformly within the v3 lower / upper bounds for the 5 new params,
     using a fixed seed for reproducibility.
4. Generate 74 LHS samples in 54-d using pymoo's `LHS()` operator, then concatenate the 5 + 17 + 74
   = 96 cells into the initial population matrix.
5. Pass the matrix to `NSGA2(pop_size=96, sampling=Population(...))` (or equivalent pymoo API for
   custom initial populations).

### NSGA-II configuration

- pop_size: 96
- n_gen: 8
- sampling: custom 96-cell warm-started population
- crossover: SBX (default η=15)
- mutation: polynomial (default η=20)
- selection: tournament (default)
- constraint: AIS-to-soma Nav ratio ≥ 5 via `n_ieq_constr=1`
- Bounds: identical to t0080 (`nav16_ais ≥ 0.25` lower bound; `tau_ca_multiplier ≤ 20` upper
  bound)

### Pre-launch validation

Before the full NSGA-II run, validate that:
- The 5 t0080 Pareto cells still produce their recorded DSI / PD values when re-evaluated on the v3
  substrate compiled fresh on the new instance (smoke test for substrate consistency across runs).
- The 17 projected t0078 cells produce non-`NaN` results (NSGA-II handles infeasible / unstable
  cells, but truly-broken cells slow convergence).

### Compute

- Vast.ai 64-core CPU EPYC 7B13 class (target same instance class as t0080: $0.16-$0.24/hr).
- Wall-clock estimate: 768 cells × 45 s/cell sequential = ~9.6 h on a 64-core instance.
- **Cost target: ~$2.40** (768 × $0.00284 + $0.20 overhead, t0080-measured per-cell rate).
- **Hard cap: $3.00** (re-armed cost-cap watchdog in `nsga2_loop.py`; existing watchdog logic
  re-used).

## Pass criterion

Locate at least one Pareto cell with **DSI ≥ 0.4 AND PD ≥ 10 Hz**, OR rule it out
architecturally across 768 cells in the warm-started 54-d space — a much stronger negative result
than t0080's 192-cell run. A negative result here, paired with t0080's, makes a clean architectural
case that the v3 substrate cannot reach the joint operating point and the project should pivot.

## Expected assets

None. The substrate library and answer asset already exist from t0080. This task produces only
results files (Pareto front, hypervolume trajectory, metrics, compare_literature) and follow-up
suggestions. `expected_assets`: `{}`.

## Outputs

- `results/results_summary.md` (Summary, Metrics, Verification)
- `results/results_detailed.md` (Methodology, Pareto Front, Visualisations, Examples, Architectural
  Diagnostic, Limitations, Files Created, Verification, Next Steps, Task Requirement Coverage)
- `results/metrics.json` with per-Pareto-cell variants
- `results/costs.json` with the final Vast.ai cost
- `results/remote_machines_used.json`
- `results/data/pareto_front.json`, `all_evaluations.json`, `hv_trajectory.json`,
  `example_cells.json`
- `results/images/pareto_front.png`, `hypervolume_trajectory.png`, `all_cells_scatter.png`
- `results/compare_literature.md` updating the t0080 / t0078 baseline comparisons

## Dependencies

- `t0024_port_de_rosenroll_2026_dsgc` — the upstream Bed B substrate
- `t0069_t0067_ais_localised_channel_sweep` — Bed A AIS reference
- `t0076_bedb_dsi_firing_rate_mobo` — 25-d BO baseline for HV anchor
- `t0078_bedb_mobo_v2_ais_tiered_ahp` — 49-d AIS-augmented substrate; provides 17 warm-start cells
- `t0080_bedb_mobo_v3_dendritic_spike_nsga2` — v3 substrate library + 5 warm-start cells + harness

## Risks and fallbacks

- **Per-cell wall-clock higher than t0080's 45 s** (e.g., the v3 substrate may be slower for
  active-dendrite cells): cost-cap watchdog kills run if approaching $3.00; partial Pareto front is
  still useful.
- **Warm-start cells produce NaN / unstable behaviour** (e.g., t0078 cells with random new-dim
  values trigger runaway depolarisation): NSGA-II's `is_unstable` filter handles them; documented as
  `n_unstable / n_total` in results.
- **NSGA-II diversity collapse on warm-started population**: small risk that all seeded cells
  cluster too tightly, reducing exploration. The 74 LHS cells mitigate this.
- **Vast.ai 64-core unavailable**: fall back to 36-core or 72-core EPYC instances; re-estimate cost
  proportionally.

## Verification criteria

- Task results pass `verify_task_results.py` with 0 errors.
- Task metrics pass `verify_task_metrics.py` with 0 errors.
- Vast.ai instance destroyed cleanly per `verify_machines_destroyed.py`.
- Cost ≤ $3.00 hard cap.
- All 13 task verificators pass (file, deps, suggestions, metrics, results, folder, logs,
  research_*, compare_literature, machines_destroyed, plan).
- Pre-merge verificator passes with 0 errors.
