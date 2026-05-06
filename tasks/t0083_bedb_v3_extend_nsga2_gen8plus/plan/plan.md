---
spec_version: "2"
task_id: "t0083_bedb_v3_extend_nsga2_gen8plus"
date_completed: "2026-05-05"
status: "complete"
---
# Plan: Extend t0081 NSGA-II from gen-7 with Adaptive HV-Plateau Stop

## Objective

Continue NSGA-II optimisation from t0081's gen-7 final population for at least 5 more generations on
the v3 dendritic-spike-augmented Bed B substrate, using an adaptive hypervolume-plateau stop rule
(relative HV improvement averaged over a 3-generation window < 1%, evaluated from gen 11 onwards)
and a hard cap of 10 additional generations (max gen 17). The continuation reuses t0081's gen-7
surviving population (96 individuals with pre-computed objective values, marked as already evaluated
so pymoo skips re-evaluation) on the same Vast.ai EPYC 7B13 64-core class ($0.2382/hr) under a $5.00
hard cost cap.

Success criteria: (a) **primary** — at least one **additional** Pareto cell with
`DSI >= 0.4 AND PD >= 10 Hz` beyond t0081's cell 767 (total joint-pass cells >= 2), characterising
the joint-passing neighbourhood (cells 637 / 762 from t0081 are <= 0.086 distance from cell 767);
(b) **secondary** — final HV > t0081's 16.33 with HV-plateau stop firing before the gen-17 hard
cap or the budget watchdog tripping; (c) **acceptable negative** — zero additional joint-pass
cells but final HV > 16.33 with plateau detected, documenting cell 767 as an isolated point in the
parameter space.

## Task Requirement Checklist

Operative task text (verbatim from `task_description.md`):

```text
Continue NSGA-II from t0081's gen-7 final population for at least 5 more generations with adaptive
HV-plateau stop (<1% over 3-gen window); hard cap +10 gens, $5.00 cost.

In scope:
* Reuse t0081's harness verbatim with two modifications: replace warm-start init with direct load
  of t0081's gen-7 final population (96 individuals, with objective values pre-computed and
  re-injected into pymoo's Algorithm state to skip re-evaluation); add an adaptive HV-plateau
  watchdog terminating when (HV(N) - HV(N-3))/HV(N-3) < 0.01 averaged over the last 3 generations,
  AND only after a minimum of 5 additional generations (earliest stop = gen 12; watchdog evaluates
  starting at gen 11).
* Hard cap on total additional generations: 10 (gen 8 through gen 17 maximum).
* Hard cost cap: $5.00 via budget watchdog (instance_lifetime_hr * $0.2382/hr).
* Reuse the de_rosenroll_2026_dsgc_ais_dendritic_spike library asset from t0080 unchanged.
* Same Vast.ai instance class as t0081 (AMD EPYC 7B13 64-core, 503 GB RAM, $0.2382/hr).
* Compare final Pareto front, joint-pass cell count, HV trajectory, and per-generation
  parameter-distribution diagnostics against t0081 and t0080 baselines.

Pass criteria:
* Primary: at least one additional Pareto cell with DSI >= 0.4 AND PD >= 10 Hz beyond cell 767.
* Secondary: HV trajectory continues monotonically; final HV > t0081's 16.33; HV-plateau stop fires
  before gen-17 hard cap OR budget watchdog fires.
* Acceptable negative: zero additional joint-pass cells but final HV > 16.33 with plateau detected.

Notes: watchdog logic must be additive, not destructive: each new generation appends to t0081's
saved evaluation history. Final all_evaluations.json must contain the union of t0081's 768 cells +
this task's additional cells with consistent generation numbering (gen 8 onwards).
```

Concrete requirements decomposed:

* **REQ-1**: Reuse `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset from t0080 unchanged
  (no substrate changes, no new dendritic-spike parameters, no new channels, no AIS modifications).
  Satisfied by step 5; evidence: `code/run_loop.py` imports from
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop`.
* **REQ-2**: Reuse t0081's harness (smoke gate, build_metrics, plot_results, paths, run_loop) by
  copy-into-task with import rebinding. Satisfied by step 4; evidence: corresponding files exist in
  `code/` with import rebinding to t0083 paths.
* **REQ-3**: Replace t0081's Sobol/LHS warm-start with a direct reload of t0081's gen-7 final
  population. Reload procedure: load 192 records (gen 6 + gen 7) from t0081's
  `all_evaluations.json`, build `Population.new("X", X, "F", F, "G", G)` with worst-case-sentinel
  substitution applied to F for `is_unstable=True` cells (`WORST_CASE_DSI=-1.0`,
  `WORST_CASE_RATE_HZ=0.0`), mark each individual `evaluated={"F","G"}`, run pymoo
  `RankAndCrowding().do(problem, pop192, n_survive=96)` with explicit seed (numpy
  `default_rng(seed=t80_loop.LHS_SEED)`). Satisfied by steps 6 and 7; evidence:
  `code/reload_gen7.py` produces a 96-individual `Population` and the unit test
  `code/test_reload_gen7.py` confirms the Pareto subset matches t0081's saved `pareto_front.json`.
* **REQ-4**: Add an adaptive HV-plateau watchdog as a pymoo `Termination` subclass. Returns True
  when `len(hv_history) >= 11` (i.e. earliest evaluation point is end of gen 10, after >= 5
  additional gens past gen 7) AND mean of last 3 relative deltas
  `(hv_history[g] - hv_history[g-3]) / hv_history[g-3] < 0.01`. Earliest stop = end of gen 11
  (`len(hv_history) == 12`, evaluating gens 9/10/11 against gens 6/7/8). Combined with
  `MaxGenerationTermination(10)` via `TerminationCollection`. Satisfied by step 8; evidence:
  `code/hv_plateau_watchdog.py` with unit-testable function `should_stop`.
* **REQ-5**: Hard cap of 10 additional generations (gen 8 through gen 17 maximum). Satisfied by step
  9; evidence: `MaxGenerationTermination(10)` argument in `code/run_loop.py`.
* **REQ-6**: Hard cost cap of $5.00 via budget watchdog
  (`instance_lifetime_hr * $0.2382/hr >= $5.00`). Satisfied by step 9; evidence:
  `t80_loop._HARD_BUDGET_USD = 5.00` monkey-patch in `code/run_loop.py` and final cost recorded in
  `results/costs.json`.
* **REQ-7**: Same Vast.ai instance class as t0081 (AMD EPYC 7B13 64-core, 503 GB RAM, $0.2382/hr).
  Satisfied by step 11 (setup-machines orchestrator step); evidence:
  `logs/steps/*setup-machines*/machine_log.json` records EPYC 7B13 64-core class.
* **REQ-8**: Generation-numbering continuity — t0081 ends at gen 7; this task starts at gen 8.
  Pre-set `problem.eval_count = 768` so `gen = eval_count // POP_SIZE` produces gen-8 numbering on
  the first true offspring. Satisfied by step 9; evidence: `all_evaluations.json` records have
  `generation in {0..17}` with no gaps after merging.
* **REQ-9**: Additive evaluation history — final `all_evaluations.json` contains the union of
  t0081's 768 cells + t0083's 480-960 additional cells. Satisfied by step 9; evidence: pre-load
  `_ALL_EVALUATIONS` from t0081's `all_evaluations.json` before `minimize()`, so `_save_*` helpers
  emit the union.
* **REQ-10**: Pre-launch substrate-consistency smoke gate — re-evaluate 5 reference cells from
  t0081 (cell 767 + 4 Pareto cells across gens 4, 5, 6, 7) on the fresh Vast.ai instance and confirm
  DSI / PD reproduce within `DSI_TOLERANCE = 0.05` / `PD_TOLERANCE_HZ = 1.0`. PASS = all 5 within
  tolerance. If any cell diverges, halt and create an intervention file before launching the
  continuation. Satisfied by step 13; evidence: `logs/smoke_gate.json`.
* **REQ-11**: Hard biological lower bounds (`nav16_ais >= 0.25 S/cm^2`; AIS-to-soma Nav ratio >= 5)
  honoured. Satisfied by step 5 (inherited from `BedBV3Problem`); evidence: same as t0080 / t0081.
* **REQ-12**: 8 directions x 20 seeds x 1400 ms FULL HH per cell. Satisfied by step 5 (inherited
  from `evaluate_parameter_vector`); evidence: same as t0080 / t0081.
* **REQ-13**: Per-cell registered metrics (DSI, PD rate Hz, joint_pass dimension) in
  `results/metrics.json` for each Pareto cell + closest-to-joint cell, using the explicit
  multi-variant format with one variant per Pareto cell. Satisfied by step 16; evidence:
  `results/metrics.json` produced by `code/build_metrics.py`.
* **REQ-14**: Charts produced — Pareto front PNG, hypervolume trajectory PNG (with vertical line
  at gen 8 marking the t0081/t0083 boundary), all-cells scatter PNG. Satisfied by step 17; evidence:
  `results/images/pareto_front.png`, `results/images/hypervolume_trajectory.png`,
  `results/images/all_cells_scatter.png`.
* **REQ-15**: Vast.ai instance destroyed cleanly at the end of the run. Satisfied by orchestrator
  teardown step; evidence: `verify_machines_destroyed.py` passes.
* **REQ-16**: Compare final Pareto front, joint-pass cell count, HV trajectory, and per-generation
  parameter-distribution diagnostics against t0081 and t0080 baselines. Satisfied by step 18 (the
  charts in step 17 plus a per-generation parameter-distribution chart) and the orchestrator
  `compare-literature` step (out of plan scope); evidence: per-generation parameter distribution PNG
  \+ comparison sections in `results/results_detailed.md` (orchestrator-managed) and
  `results/compare_literature.md` (orchestrator-managed).

## Approach

t0083 is a **continuation run** that inherits t0081's architecture wholesale and adds two narrow new
modules. The chain of imports flows downward from the v3 substrate library
(`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code`, registered as
`de_rosenroll_2026_dsgc_ais_dendritic_spike`) through t0083's task-local code. No substrate changes
whatsoever — same `BedBV3Problem(n_var=54, n_obj=2, n_ieq_constr=1)`, same
`evaluate_parameter_vector` (8 directions x 20 seeds x 1400 ms FULL HH), same AIS-to-soma Nav ratio
constraint `g(x) = 5 - nav16_ais/nav16_soma`.

Key research findings driving the design:

* **Pymoo population reload semantics** (research_code findings): `Initialization.do` accepts a
  `Population` instance directly when `sampling=` is set to a `Population` object. Individuals
  carrying both `F` and `G` and having those keys in `evaluated` cause `Evaluator.eval` to skip them
  entirely (filter via
  `[i for i, ind in enumerate(pop) if not all([e in ind.evaluated for e in evaluate_values_of])]`).
  The reload pattern is:

  ```python
  pop = Population.new("X", X, "F", F, "G", G)
  for ind in pop:
      ind.evaluated.update(["F", "G"])
  algo = NSGA2(pop_size=96, sampling=pop, ...)
  ```

* **Recovering t0081's gen-7 survivors** (research_code findings): t0081 used `save_history=False`,
  so the in-process `Population` of gen-7 survivors is gone. Recovery is via
  `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` (768 `CellEvaluation`
  records, 96 per generation 0..7). Take the 192 records with `generation in {6, 7}`, build a
  192-individual `Population` with `X = params`, `F = (-dsi, -pd_rate_hz)` (sign flip for
  minimisation, with `WORST_CASE_DSI=-1.0` / `WORST_CASE_RATE_HZ=0.0` substitution for cells with
  `is_unstable=True`, matching what NSGA-II saw at end-of-gen-7), `G = constraint_violation`. Run
  pymoo `RankAndCrowding().do(problem, pop192, n_survive=96)` with explicit seed
  (`numpy.random.default_rng(seed=t80_loop.LHS_SEED)`) to deterministically recover the 96 gen-7
  survivors. Worst-case-sentinel substitution must match what NSGA-II saw: in
  `BedBV3Problem._evaluate` (t0080 line 184-187), unstable cells have their objectives overwritten
  before pymoo sees them whereas the saved `CellEvaluation` records the unmodified values.

* **HV-plateau watchdog as pymoo Termination subclass** (research_code findings): pymoo's
  `minimize(problem, algorithm, ("n_gen", N), ...)` runs to completion. Custom `Termination`
  subclasses with `_update(algorithm)` returning True at end-of-gen are the documented pattern;
  combine with `MaxGenerationTermination(10)` via `TerminationCollection`. Watchdog reads
  `algorithm.n_gen` and the saved HV trajectory at gen end. Earliest fire window: end of gen 11 with
  `len(hv_history) == 12`, evaluating gens 9/10/11 against gens 6/7/8.

* **Cost-cap watchdog reuse** (research_code findings): t0080's `nsga2_loop.py` lines 89-123 define
  module-level globals `_LOOP_START_TIME`, `_HOURLY_RATE_USD`, `_HARD_BUDGET_USD`,
  `_BUDGET_TRIPPED`. On trip, `BedBV3Problem._evaluate` lines 158-166 set sentinel objectives so
  pymoo exits cleanly at end-of-generation. t0081 raised the cap from $3.00 to $5.00 via one-line
  monkey-patch (`t80_loop._HARD_BUDGET_USD = 5.00`); t0083 uses the same pattern with $5.00.

* **Path management** (research_code findings): t0081's `_redirect_t80_paths_to_t81` overwrites
  t0080's module-level `PARETO_FRONT_JSON`, `RESULTS_DATA_DIR`, `INTERVENTION_DIR`,
  `BUDGET_OVERRUN_MD` constants in-place after import. The `_save_*` helpers compute paths from the
  module-level constants at call time, so this works without further plumbing. t0083 replicates the
  pattern but redirects to its own `tasks/t0083_.../results/data/`.

* **Generation-numbering continuity** (research_code findings): t0080's `BedBV3Problem._evaluate`
  computes `gen = self.eval_count // POP_SIZE` (POP_SIZE=96). Pre-setting `problem.eval_count = 768`
  before `minimize()` makes the first true offspring evaluation land at `eval_count=768`, generation
  `768//96=8`. Combined with pre-loading `_ALL_EVALUATIONS` from t0081's `all_evaluations.json`, the
  saved files are the union with consistent gen numbering.

* **Substrate stability** (research_code findings): t0081's 0/768 unstable cells confirm v3
  substrate stability. No extra substrate validation beyond the 5-cell smoke gate.

**Reused t0081 code** (copy-into-task with ~3-15 LOC of import rebinding): `smoke_gate.py` (145
LOC), `build_metrics.py` (96 LOC), `plot_results.py` (123 LOC), `paths.py` (~50 LOC). Adapted from
t0081 with substantive changes: `run_loop.py` (~180 LOC).

**New modules**: `reload_gen7.py` (~120 LOC), `hv_plateau_watchdog.py` (~80 LOC),
`test_reload_gen7.py` (~80 LOC).

**Alternatives considered and rejected**:

1. **Re-launch from scratch with extended `n_gen=15`**: would re-evaluate the 768 t0081 cells,
   wasting ~$2.20 of compute on already-known evaluations and breaking the project's "evolutionary
   continuity" spirit. Rejected.
2. **Approximate continuation using only the 96 gen-7 offspring (ignoring gen-6 carryovers)**:
   simpler reload code but loses up to 96 high-quality gen-6 elite-preserved survivors that gen 7
   did not improve upon, including some Pareto cells. NSGA-II's elitist survival (RankAndCrowding
   over the combined 192) is the canonical mechanism — bypassing it would be a different
   algorithm. Rejected.
3. **Pymoo Callback that sets `algorithm.termination.force_termination = True`**: less clean than a
   custom `Termination` subclass; uses a deprecated API. Rejected.
4. **Fixed n_gen=10 additional generations with no plateau watchdog**: simpler, but the researcher
   explicitly authorised "at least 5 more generations and then check if it is still raising and
   decide when to stop" — an adaptive stop rule is the requirement, not optional. Rejected.

**Open questions resolved**:

* **Deterministic tie-break in RankAndCrowding** — pymoo's `RankAndCrowding._do` uses a numpy RNG
  for crowding-distance tie-breaking. Decision: pass an explicit
  `random_state = np.random.default_rng(seed=t80_loop.LHS_SEED)` (same seed t0081 used for LHS) and
  write `code/test_reload_gen7.py` as a unit test asserting the resulting Pareto subset of the 96
  survivors matches t0081's saved `pareto_front.json` exactly (16 cells, identical cell_index list).
  If the test fails, accept the near-equivalent survivor set since NSGA-II is robust to small
  perturbations in elite-survival ties — the failure case becomes a documented note in results,
  not a hard stop. The cell-index identity is a strong sentinel-substitution and seed correctness
  check.

* **Smoke-gate reference cells** — confirmed: 5-cell gate covering cell 767 (the joint-pass
  anchor) plus 4 Pareto cells across gens 4, 5, 6, 7 (one per generation, sampling diversity in the
  front), not the t0080 cells (which would test a different question). Tolerances unchanged from
  t0081: `DSI_TOLERANCE = 0.05`, `PD_TOLERANCE_HZ = 1.0`. The specific 4 non-anchor cell indices are
  selected at implementation time as the highest-DSI Pareto cell from each of gens 4, 5, 6, 7 in
  t0081's `pareto_front.json`.

**Recommended task type**: `experiment-run` (already set in `task.json`). Planning Guidelines
applied: explicit metrics-variant format (one variant per Pareto cell + closest-to-joint cell),
fixed seeds (LHS_SEED inherited from t0080, NSGA-II seed inherited from t0081), explicit cost cap in
plan, baseline comparisons inherited (t0080 + t0081 Pareto fronts) in compare-literature step (out
of plan scope, orchestrator-managed).

## Cost Estimation

Per-cell cost on EPYC 7B13 64-core at $0.2382/hr (measured by t0080/t0081): **$0.00284 per cell**.

* Smoke gate: 5 cells x $0.00284 = **$0.014**
* NSGA-II continuation: 480 cells (5 gens minimum) to 960 cells (10 gens max) x $0.00284 = **$1.36 -
  $2.73**
* Provisioning + idle + teardown overhead: **~$0.20**
* **Most-likely range: $1.50 - $3.00**
* **Hard cost cap: $5.00** (allows up to ~21 hours of instance lifetime, enough to absorb any
  per-cell wall-clock variance from the v3 substrate's dendritic-spike machinery)

Project budget: $20.00 total, ~$8.13 spent before t0083 (per the task harness orchestrator context),
$11.87 remaining. After-t0083 most-likely spend: $9.63 - $11.13 — well below the $20.00 cap and
below the 80% warn threshold ($16.00). Acceptable.

The cost-cap watchdog is a defensive backstop, not a primary planning constraint: t0081 ran $2.39
actual against $3.00 cap (80% utilisation, 0% over) on 768 cells; t0083's projected envelope sits
comfortably within the same per-cell economics.

## Step by Step

### Milestone A: Prepare task-local code (steps 1-10)

1. **Create `code/__init__.py`** (empty file) so the task code package can be imported as
   `tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code`. No `REQ-*` mapping (infrastructure).

2. **Create `code/paths.py`** (~50 LOC). Copy from
   `tasks/t0081_bedb_v3_warmstart_nsga2/code/paths.py` then adapt: change `RESULTS_DIR`,
   `RESULTS_DATA_DIR`, `RESULTS_IMAGES_DIR`, `INTERVENTION_DIR`, `BUDGET_OVERRUN_MD`, `LOGS_DIR`,
   `SMOKE_GATE_LOG_JSON`, `PARETO_FRONT_JSON`, `ALL_EVALUATIONS_JSON`, `HV_TRAJECTORY_JSON`
   constants to point at `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/...`. Add new dependency-pointer
   constants:
   `T0081_ALL_EVALUATIONS_JSON = PROJECT_ROOT / "tasks" / "t0081_bedb_v3_warmstart_nsga2" / "results" / "data" / "all_evaluations.json"`,
   `T0081_PARETO_FRONT_JSON`, `T0081_HV_TRAJECTORY_JSON`. Keep the existing
   `T0080_PARETO_FRONT_JSON` constant for reference (not used at runtime by t0083). Expected output:
   `python -c "from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths; print(paths.RESULTS_DATA_DIR)"`
   prints the t0083 results-data path. Satisfies REQ-2.

3. **Create `code/reload_gen7.py`** (~120 LOC). New module. Public function
   `reload_t0081_gen7_survivors(*, problem: BedBV3Problem, seed: int) -> Population`:
   * Read `paths.T0081_ALL_EVALUATIONS_JSON` and parse into a list of records.
   * Filter to records with `generation in {6, 7}` (192 records).
   * For each record, build `X[i] = record.params` (54 floats, natural units already in pymoo scale
     per t0080 convention).
   * Compute `F[i, 0] = -dsi_to_record`, `F[i, 1] = -pd_rate_to_record` where
     `dsi_to_record = WORST_CASE_DSI` and `pd_rate_to_record = WORST_CASE_RATE_HZ` if
     `record.is_unstable`, else the recorded `record.dsi` and `record.pd_rate_hz`. Constants:
     `WORST_CASE_DSI = -1.0`, `WORST_CASE_RATE_HZ = 0.0` (matching t0080 line 184-187).
   * `G[i, 0] = record.constraint_violation` (already in pymoo's `<=0` feasible convention).
   * Build `pop = Population.new("X", X, "F", F, "G", G)`; for each `ind in pop`,
     `ind.evaluated.update(["F", "G"])`.
   * Run
     `survival = RankAndCrowding(); survivors = survival.do(problem=problem, pop=pop, n_survive=96, random_state=np.random.default_rng(seed=seed))`.
   * Return `survivors` (96-individual `Population`).
   * Add a `main()` CLI that reads paths, builds a fresh `BedBV3Problem(max_workers=1)`, calls the
     reload function with seed `t80_loop.LHS_SEED`, and writes the resulting X array to
     `results/data/reloaded_gen7_survivors.json` (96 records with cell_index, params, F, G,
     evaluated marker). Expected output:
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0083_bedb_v3_extend_nsga2_gen8plus -- python -m tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.reload_gen7`
     writes a 96-record JSON file. Satisfies REQ-3.

4. **Create `code/test_reload_gen7.py`** (~80 LOC). Unit test that exercises `reload_gen7`:
   * Calls `reload_t0081_gen7_survivors(problem=BedBV3Problem(max_workers=1), seed=LHS_SEED)`.
   * Reads t0081's `pareto_front.json` (16 cells; each has a `cell_index` field tying it to
     `all_evaluations.json`).
   * For each `cell_index` in t0081's Pareto front, asserts the corresponding 54-d parameter vector
     is present (within 1e-12 element-wise) among the 96 reloaded survivors.
   * Asserts `len(survivors) == 96`.
   * Asserts every survivor `ind.evaluated == {"F", "G"}`.
   * If the cell-index identity check fails (sentinel-substitution or seed mismatch):
     - Emit a clear pytest failure message naming up to 3 missing cell indices.
     - Log the failure as a known acceptable risk in `logs/test_reload_gen7_failure.md` at
       implementation time: the near-equivalent survivor set is acceptable since NSGA-II is robust
       to small perturbations in crowding-distance ties. Expected output:
       `uv run pytest tasks/t0083_bedb_v3_extend_nsga2_gen8plus/code/test_reload_gen7.py -v` reports
       0 failures when the deterministic survival reproduces; or 1 failure with a documented
       near-miss when it does not. Either outcome is acceptable for proceeding to the live run, but
       the failure case must be logged in `logs/`. Satisfies REQ-3 (verification component).

5. **Confirm import path of v3 substrate library**. Run
   `uv run python -c "from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import nsga2_loop; print(nsga2_loop.BedBV3Problem.__name__)"`.
   Expected output: `BedBV3Problem`. This confirms the library is importable and `BedBV3Problem`,
   `evaluate_parameter_vector`, `_save_pareto_front`, `_save_all_evaluations`,
   `_save_hv_trajectory`, `_HARD_BUDGET_USD` are accessible without copy. Satisfies REQ-1, REQ-11.

6. **Create `code/hv_plateau_watchdog.py`** (~80 LOC). New module. Three components:
   * Constants: `HV_PLATEAU_WINDOW = 3`, `HV_PLATEAU_REL_THRESHOLD = 0.01`,
     `HV_PLATEAU_MIN_GENS_AFTER_RESUME = 5`. The minimum-resume guard means watchdog is evaluated
     only after `len(hv_history) >= 11` (8 t0081 generations 0..7 + 3 new generations 8/9/10 = 11
     entries, so the first window evaluates gens 8/9/10 against gens 5/6/7 lookbacks — wait, the
     spec says watchdog evaluates starting at gen 11; let's clarify: the watchdog is evaluated after
     each generation starting after `>= 5` additional gens, so earliest evaluation point is end of
     gen 12 with `len(hv_history) == 13`, evaluating gens 10/11/12 against gens 7/8/9 lookbacks.
     Earliest stop = end of gen 12 (5 additional gens minimum).
   * Pure function `should_stop(hv_history: list[float]) -> bool`: returns False when
     `len(hv_history) < 13`; returns True when mean of last 3 relative deltas
     `(hv_history[g] - hv_history[g - HV_PLATEAU_WINDOW]) / hv_history[g - HV_PLATEAU_WINDOW]` for
     `g in [N-3, N-2, N-1]` is `< HV_PLATEAU_REL_THRESHOLD`.
   * Class `HVPlateauTermination(pymoo.core.termination.Termination)` with
     `_update(algorithm) -> float`: reads the saved `paths.HV_TRAJECTORY_JSON` after each generation
     (the file is written by `_save_hv_trajectory` at end-of-gen) and returns `1.0` if
     `should_stop(hv_history)` else `0.0` (pymoo Termination contract: returns [0,1] progress where
     1.0 means terminate).
   * Add unit tests in the same file under `if __name__ == "__main__":` block (not a separate pytest
     file): assert `should_stop([6.59, 8.99, 9.24, 11.08, 11.57, 13.14, 15.22, 16.33]) == False`
     (only 8 entries, below the 13-entry minimum); assert `should_stop([16.33] * 13) == True`
     (perfectly flat satisfies < 1% threshold); assert
     `should_stop([16.33 * (1.005 ** i) for i in range(13)]) == True` (0.5% per-gen growth averages
     0.5%, below 1% threshold). Expected output:
     `uv run python -m tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.hv_plateau_watchdog` prints
     "all unit tests passed". Satisfies REQ-4.

   **Important clarification on minimum-gens timing**: The task description says "minimum 5
   additional generations" and "earliest possible stop is gen 12". Interpreting this against t0081
   ending at gen 7: gens 8, 9, 10, 11, 12 are the 5 additional generations; the watchdog evaluates
   after gen 12 finishes. `len(hv_history)` after gen 12 = 13 (gens 0..12). The 3-generation
   lookback window evaluates deltas at gens 10/11/12 against gens 7/8/9. The `should_stop` minimum
   of 13 entries enforces this. If the task's wording is interpreted differently ("5 more after gen
   7" but allowing the watchdog itself to fire one earlier), the minimum becomes 12 entries
   (earliest stop = end of gen 11). The plan adopts the conservative reading (13-entry minimum,
   earliest stop = end of gen 12) to guarantee `>= 5` additional generations are run before any
   stop, satisfying both the "at least 5 more generations" and "earliest possible stop is gen 12"
   framings.

7. **Copy `code/smoke_gate.py` from t0081 with rebinding** (145 LOC + ~15 LOC rebind). Source:
   `tasks/t0081_bedb_v3_warmstart_nsga2/code/smoke_gate.py`. Changes:
   * Replace `from tasks.t0081_bedb_v3_warmstart_nsga2.code import paths` with
     `from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths`.
   * Replace the input source from `T0080_PARETO_FRONT_JSON` to `T0081_PARETO_FRONT_JSON` (defined
     in step 2).
   * Subset reference cells to 5: cell 767 (joint-pass anchor) plus the highest-DSI Pareto cell from
     each of gens 4, 5, 6, 7 in t0081's `pareto_front.json`. The selection is by `cell_index` field,
     computed at runtime in `smoke_gate.py:_select_reference_cells()`.
   * Tolerances unchanged: `DSI_TOLERANCE = 0.05`, `PD_TOLERANCE_HZ = 1.0`.
   * Output: `logs/smoke_gate.json` with per-cell pass/fail flag and the recorded vs re-evaluated
     DSI / PD values. Expected output (when run on the remote in step 13): a `logs/smoke_gate.json`
     with 5 cell entries, each with `pass=True`. Satisfies REQ-10.

8. **Copy `code/build_metrics.py` from t0081 with rebinding** (96 LOC + ~3 LOC rebind). Source:
   `tasks/t0081_bedb_v3_warmstart_nsga2/code/build_metrics.py`. Change
   `from tasks.t0081_bedb_v3_warmstart_nsga2.code import paths` to
   `from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths`. Logic unchanged: reads
   `pareto_front.json` + `all_evaluations.json`, builds `metrics.json` with one variant per Pareto
   cell + closest-to-joint cell (explicit multi-variant format per
   `arf/specifications/metrics_specification.md`). Tags `joint_pass` dimension with True/False for
   each variant when `DSI >= 0.4 AND PD >= 10 Hz`. Reports `direction_selectivity_index` (registered
   metric) and `pd_rate_hz` (recorded as a custom per-task field; not a registered metric). Expected
   output (when run in step 16): `results/metrics.json` with one variant per Pareto cell, each
   variant containing `direction_selectivity_index`, `pd_rate_hz`, `joint_pass`, `cell_index`,
   `generation`. Satisfies REQ-13.

9. **Copy `code/plot_results.py` from t0081 with rebinding** (123 LOC + ~3 LOC rebind, plus ~10 LOC
   for new gen-8 boundary marker and parameter-distribution chart). Source:
   `tasks/t0081_bedb_v3_warmstart_nsga2/code/plot_results.py`. Changes:
   * Rebind paths import (one line).
   * In the HV trajectory plot, add a vertical dashed line at `gen=8` annotated "t0081 -> t0083
     boundary".
   * Add new function `plot_per_generation_parameter_distribution()` that reads
     `all_evaluations.json`, splits by generation, computes per-generation mean and std of all 54
     parameters (or a curated subset of the most influential 10-15 dims), and emits
     `images/parameter_distribution_per_generation.png`. The 10-15 dim subset is selected by
     ParamIndex order with priority on the dendritic-spike-related and AIS-related dims.
   * Output PNGs: `pareto_front.png`, `hypervolume_trajectory.png`, `all_cells_scatter.png`,
     `parameter_distribution_per_generation.png`. Expected output (when run in step 17): four PNG
     files in `results/images/`. Satisfies REQ-14, REQ-16 (the parameter-distribution chart).

10. **Create `code/run_loop.py`** (~180 LOC). Adapted from
    `tasks/t0081_bedb_v3_warmstart_nsga2/code/run_loop.py` as the structural template. Outline:
    * Imports:
      `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import nsga2_loop as t80_loop`;
      `from tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code import paths, reload_gen7, hv_plateau_watchdog`;
      pymoo imports (`NSGA2`, `Population`, `MaxGenerationTermination`, `TerminationCollection`,
      `minimize`).
    * Path redirection: define `_redirect_t80_paths_to_t83()` that overwrites
      `t80_loop.PARETO_FRONT_JSON`, `t80_loop.RESULTS_DATA_DIR`, `t80_loop.INTERVENTION_DIR`,
      `t80_loop.BUDGET_OVERRUN_MD` with t0083 paths from `paths`.
    * Cost-cap override: `t80_loop._HARD_BUDGET_USD = 5.00`.
    * Pre-load `_ALL_EVALUATIONS`: read t0081's `all_evaluations.json` into a list, assign
      `t80_loop._ALL_EVALUATIONS = <list>` so subsequent `_save_all_evaluations` calls emit the
      union.
    * Build problem: `problem = t80_loop.BedBV3Problem(max_workers=0)`. Pre-set
      `problem.eval_count = 768` so first true offspring eval lands at gen 8.
    * Build sampling:
      `sampling = reload_gen7.reload_t0081_gen7_survivors(problem=problem, seed=t80_loop.LHS_SEED)`.
    * Build algorithm: `algo = NSGA2(pop_size=96, sampling=sampling)`.
    * Build termination:
      `term = TerminationCollection(MaxGenerationTermination(10), hv_plateau_watchdog.HVPlateauTermination())`.
    * Run: `result = minimize(problem, algo, termination=term, save_history=False, verbose=True)`.
    * Save final outputs: t80_loop._save_pareto_front, _save_all_evaluations, _save_hv_trajectory
      are called inside `BedBV3Problem._evaluate` per-generation per t0080 design — confirmed by
      reading t0080 code; no extra explicit save calls needed at end.
    * Add `main()` CLI that reads command-line args (`--max-gen` default 10, `--cost-cap` default
      5.00) for ad-hoc overrides (the budget-watchdog cap is set by `t80_loop._HARD_BUDGET_USD`;
      `--cost-cap` is a CLI override for it). Expected output: `nsga2_loop.log` showing 5-10
      additional generations completed, gen-numbering starts at gen 8, final `pareto_front.json` and
      `all_evaluations.json` written. Satisfies REQ-1, REQ-3, REQ-4, REQ-5, REQ-6, REQ-8, REQ-9,
      REQ-11.

### Milestone B: Pre-flight verification on local (steps 11-12)

11. **Pre-flight smoke compile + run unit tests on local**. Run:
    `uv run pytest tasks/t0083_bedb_v3_extend_nsga2_gen8plus/code/ -v` and
    `uv run python -m tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.hv_plateau_watchdog`. Expected
    output: `test_reload_gen7.py` passes (or fails with documented near-miss per step 4); HV-plateau
    unit tests print "all unit tests passed". If the reload test outputs a hard error (exception,
    not just failed assertion), STOP and debug — do not proceed until the reload module loads and
    runs to completion. Satisfies REQ-3 (test component), REQ-4.

### Milestone C: Provision and validate remote (steps 12-13)

12. **Setup-machines orchestrator step (out of plan scope, executed by setup-machines skill)**.
    Provisions one Vast.ai 64-core CPU instance, AMD EPYC 7B13 family, 503 GB RAM, 25 GB disk,
    Debian 12 / `python:3.12-bookworm`, target $0.16-$0.24/hr. Installs deps
    (`pip install pymoo numpy NEURON pandas`), runs `nrnivmodl` on the v3 substrate's `mods/*.mod`,
    validates NEURON loads. Satisfies REQ-7 (executed by orchestrator).

13. **[CRITICAL] Smoke gate on remote**. SCP `code/` to remote. Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0083_bedb_v3_extend_nsga2_gen8plus -- python -m tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.smoke_gate`
    on the remote. Validation gate parameters:
    * 5 reference cells (cell 767 + highest-DSI Pareto cell from each of gens 4/5/6/7).
    * Trivial baseline: t0081's recorded DSI and PD for each cell — exact reproduction within
      tolerance is the threshold.
    * Failure condition: if any cell exceeds tolerance (`|delta_dsi| > 0.05` OR `|delta_pd_hz|
      > 1.0`), STOP, do not proceed to NSGA-II launch, create `intervention/smoke_gate_drift.md`
      > describing the divergence.
    * Individual-output inspection: read each cell's per-direction firing rates from the smoke-gate
      output and verify there is no zero-everywhere or NaN result indicating MOD misload. The smoke
      gate already records these in `logs/smoke_gate.json`. Expected output: `logs/smoke_gate.json`
      shows all 5 cells `pass=True`. Cost: ~$0.014. Satisfies REQ-10. **CRITICAL** because the gen-7
      reload depends on substrate consistency — if it diverges, the reload is poisoned.

### Milestone D: NSGA-II continuation run (steps 14-15)

14. **[CRITICAL] Launch NSGA-II continuation on remote**. Run `nohup uv run python -m
    arf.scripts.utils.run_with_logs --task-id t0083_bedb_v3_extend_nsga2_gen8plus -- python -m
    tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.run_loop --max-gen 10 --cost-cap 5.00
    > nsga2_loop.log 2>&1 &` on remote. The cost-cap watchdog (`t80_loop._HARD_BUDGET_USD =
    > 5.00`) trips on `(elapsed_s/3600) * $0.2382 >=
    > $5.00`(~21 hours instance lifetime); the HV-plateau watchdog trips on flat HV growth after gen 12; the`MaxGenerationTermination(10)`
    > trips at gen 17 hard cap. Validation gate parameters:
    * Trivial baseline: t0081's gen-7 HV = 16.33. The continuation must reproduce this reference
      point at gen 7 (the reloaded population) when post-processing — failure would indicate a
      sentinel-substitution bug.
    * `--limit` setting: not applicable (NSGA-II is a sequential algorithm, not batch inference);
      validation is per-generation rather than per-cell. After gen 8 finishes, inspect the new HV
      value: it must be `>= 16.33` (NSGA-II's elitist survival means HV is non-decreasing). If
      `HV(gen 8) < 16.33`, STOP and debug — sentinel substitution or path redirection is wrong.
    * Failure condition: if `HV(gen 8) < HV(gen 7) = 16.33` OR if all 96 gen-8 offspring are
      `is_unstable=True` (substrate broken), STOP and create `intervention/run_loop_failure.md`.
    * Individual-output inspection: after gen 8 completes, read 5 individual gen-8 evaluation
      records from `all_evaluations.json` and verify (a) `params` arrays are within 54-d bounds, (b)
      `dsi` values are in [-1.0, 1.0], (c) `pd_rate_hz` values are in [0, ~80], (d) at least one
      cell has `is_unstable=False`. Expected output: `nsga2_loop.log` shows `n_gen` advancing past 7
      (recorded as gen 8 in saved JSON), `pareto_front.json` and `hv_trajectory.json` updating after
      each generation. Satisfies REQ-1, REQ-3, REQ-4, REQ-5, REQ-6, REQ-8, REQ-9. **CRITICAL**
      because this is the actual continuation run — without it the task has not been done.

15. **Monitor run** via SSH polling (every ~10-30 min) until process exits cleanly. Watch for:
    * Generation advancement in `nsga2_loop.log`.
    * `hv_trajectory.json` length growing (8 entries from t0081 + 1 per new gen).
    * `intervention/budget_overrun.md` appearing (would indicate budget watchdog tripped).
    * Process exit reason: HV-plateau termination, MaxGenerationTermination, or cost-cap trip.
      Expected output: process exits within 4-9 hours of wall-clock; final `n_gen` recorded.
      Satisfies REQ-9.

### Milestone E: Pull results and post-process locally (steps 16-18)

16. **Pull results from remote to local**. SCP `results/data/pareto_front.json`,
    `results/data/all_evaluations.json`, `results/data/hv_trajectory.json`, `nsga2_loop.log`,
    `logs/smoke_gate.json` from remote into the matching paths on local. Verify file sizes:
    `all_evaluations.json` should be > 51458 lines (t0081's size; t0083 adds 480-960 more cells =
    ~32-64 KB additional). Expected output:
    `ls -la tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/` shows three files of plausible
    size; `hv_trajectory.json` has 13-18 entries. Satisfies REQ-9.

17. **Compute metrics locally**. Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0083_bedb_v3_extend_nsga2_gen8plus -- python -m tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.build_metrics`.
    Reads `results/data/pareto_front.json` and `results/data/all_evaluations.json`; writes
    `results/metrics.json` with one variant per Pareto cell + closest-to-joint cell. Variants are
    tagged with `joint_pass` dimension (True when DSI >= 0.4 AND PD >= 10 Hz). Expected output:
    `results/metrics.json` exists; `jq '.variants | length' results/metrics.json` returns the
    Pareto-front size (16-30 expected). At least 1 variant has `joint_pass: True` (cell 767 is
    preserved through elitist survival); ideally >= 2 to satisfy REQ-pass-criterion-primary.
    Satisfies REQ-13.

18. **Generate charts locally**. Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0083_bedb_v3_extend_nsga2_gen8plus -- python -m tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.plot_results`.
    Reads `results/data/*`; writes `results/images/pareto_front.png`,
    `results/images/hypervolume_trajectory.png` (with vertical dashed line at gen 8 marking the
    t0081/t0083 boundary), `results/images/all_cells_scatter.png`, and
    `results/images/parameter_distribution_per_generation.png`. Expected output: four PNG files in
    `results/images/`, each non-empty (>10 KB). Satisfies REQ-14 and the comparison-artefact portion
    of REQ-16; the comparative narrative is produced by orchestrator-managed steps and is out of
    plan scope.

(Downstream orchestrator steps for results writing, suggestions, and compare-literature are managed
by execute-task and are not part of this plan's Step by Step.)

## Remote Machines

One Vast.ai 64-core CPU instance: AMD EPYC 7B13 family (or compatible 64-core EPYC class), 503 GB
RAM (overkill but standard for the class), 25 GB disk, Debian 12 / `python:3.12-bookworm`. Target
$0.16-$0.24/hr (max accepted: $0.2382/hr). Estimated runtime: 4-9 hours wall-clock for the NSGA-II
continuation plus ~5 minutes for the smoke gate plus ~30 min provisioning / teardown overhead.
Reference: t0081 used the same class for 10.045 hours at $2.39 total. See
`arf/specifications/remote_machines_specification.md` for lifecycle details.

## Assets Needed

* **`de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset** from
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/`.
  Provides the v3 substrate (cell builder with AIS + dendritic-spike machinery, MOD files in
  `mods/`, `BedBV3Problem` class, `evaluate_parameter_vector` function, `nsga2_loop` module with
  cost watchdog, HV trajectory, save helpers). Reused via Python import; no fork.
* **t0081 result data** (read at runtime, not formally a registered asset):
  `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` (768 records, source of
  the gen-7 survivor reload), `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/pareto_front.json`
  (16 cells, source of smoke-gate reference cells and `test_reload_gen7.py` ground truth),
  `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/hv_trajectory.json` (8 entries, prepended to
  t0083's HV trajectory).

## Expected Assets

`task.json` `expected_assets`: `{}`. The task produces no new substrate, library, dataset, model,
predictions, or answer assets — it produces only `results/` files (Pareto front data, HV
trajectory, evaluation history, metrics, charts) plus `logs/` records. This matches t0081's pattern
(also `expected_assets: {}`).

## Time Estimation

* Research: complete (research_code.md only; no research_papers or research_internet needed for a
  continuation task on an established substrate).
* Planning: this document, ~30 min.
* Implementation (local code creation, milestones A and B): ~1.5 hours wall-clock for ~600 LOC
  across 6 modules + 1 unit test file.
* Setup-machines: ~15-20 min (provisioning + apt + venv + NEURON / pymoo install + MOD compile
  + verification).
* Smoke gate on remote: ~5 min.
* NSGA-II continuation run: 5 gens (480 cells) at ~30 s/cell sequential = ~4 hours; 10 gens (960
  cells) = ~8 hours wall-clock; expected stop point: somewhere in gens 12-15 = 5-8 hours.
* Teardown: ~5 min.
* Pull results and post-process: ~15 min.
* **Total wall-clock: ~6-10 hours** (dominated by the NSGA-II continuation run).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Smoke gate fails on substrate-consistency reproduction (any of the 5 reference cells diverges beyond DSI ±0.05 / PD ±1 Hz) | Low | Blocking — gen-7 reload is poisoned | Halt; create `intervention/smoke_gate_drift.md`; investigate MOD-compile drift, NEURON version drift, instance-class drift; do NOT launch NSGA-II until resolved or human review approves proceeding. |
| `test_reload_gen7.py` fails (Pareto-cell identity check does not reproduce t0081's saved 16 cells) | Medium | Non-blocking but flag-worthy | Document the near-miss in `results/results_detailed.md`; proceed with the live run since NSGA-II is robust to small perturbations in crowding-distance ties; cell-identity divergence here is a known acceptable risk per research_code findings. |
| HV-plateau watchdog never fires (HV continues to grow > 1% per gen through gen 17) | Medium | Acceptable — `MaxGenerationTermination(10)` caps the run at gen 17 | Hard cap is the backstop; result is a still-actively-improving Pareto front, which is itself a publishable finding ("front did not converge in 17 generations"). |
| Per-cell wall-clock exceeds 50 s sustained (e.g., active dendritic-spike machinery slows simulation under denser populations) | Low | Cost cap may trip before gen 17 | Cost-cap watchdog at $5.00 ensures graceful termination; partial Pareto front is still useful. At 60 s/cell sustained, 960 cells = 16 h = $3.81 — well under $5.00. Watchdog provides the hard backstop. |
| Vast.ai 64-core EPYC 7B13 unavailable | Low | Delay but not blocking | Fall back to 36-core or 72-core EPYC at <= $0.24/hr; per-cell wall-clock scales inversely with core count. Document the instance class actually used in `logs/`. |
| t0081 result files (`all_evaluations.json`, `pareto_front.json`) are missing or malformed | Very Low | Blocking — task cannot start | Already verified during research_code phase; structure consistent with t0080. If missing at implementation time, create `intervention/missing_dependency.md` and halt. |
| NSGA-II diversity collapse: gen-8+ offspring cluster around cell 767 with no Pareto expansion | Medium | Possible but addresses the "acceptable negative" pass criterion | Result is `final_HV > 16.33` flat with cell 767 isolated — a publishable architectural finding. No fallback action; document and proceed. |
| Cost-cap watchdog trips before HV-plateau watchdog (instance lifetime exceeds 21 hours due to provisioning slowness) | Low | Run terminates early but still produces partial result | Watchdog produces sentinel objectives so pymoo exits cleanly at end-of-generation; partial Pareto front + partial HV trajectory still satisfies the "5 additional generations minimum" if at least gens 8-12 completed. Document the truncation in `results_detailed.md`. |
| Pre-load of t0081's `_ALL_EVALUATIONS` causes memory bloat or JSON write performance degradation | Low | Performance, not correctness | t0081's file is 768 records; t0083 adds up to 960 records; total ~1700 records is small (~150 KB JSON). No mitigation needed beyond standard JSON write performance. |
| Generation-numbering off-by-one (e.g., `eval_count` pre-set to 768 produces gen 8 for the survivor pool itself rather than for first true offspring) | Low | Wrong gen labels in saved JSON, breaks comparison plots | Verified by reading t0080 source: skip-already-evaluated means `_evaluate` does not run for survivors, so `eval_count` does not increment for them; first true increment is gen-8 offspring. If observed differently, post-hoc fix in `build_metrics.py` to subtract 1. |

## Verification Criteria

* **Plan format**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0083_bedb_v3_extend_nsga2_gen8plus -- python -m arf.scripts.verificators.verify_plan t0083_bedb_v3_extend_nsga2_gen8plus`.
  Expected output: exit code 0, no errors. Confirms 11 mandatory sections present, frontmatter
  parses, REQ-* IDs present in checklist, Step by Step references REQ-* IDs.
* **Code module presence**: Run `ls tasks/t0083_bedb_v3_extend_nsga2_gen8plus/code/`. Expected
  output (after Milestone A): files `__init__.py`, `paths.py`, `reload_gen7.py`,
  `test_reload_gen7.py`, `hv_plateau_watchdog.py`, `smoke_gate.py`, `build_metrics.py`,
  `plot_results.py`, `run_loop.py`.
* **Reload unit test**: Run
  `uv run pytest tasks/t0083_bedb_v3_extend_nsga2_gen8plus/code/test_reload_gen7.py -v`. Expected
  output: pytest reports the test result (0 failures = strict reproduction; 1 failure with
  documented near-miss = acceptable per Risks & Fallbacks).
* **HV plateau watchdog unit tests**: Run
  `uv run python -m tasks.t0083_bedb_v3_extend_nsga2_gen8plus.code.hv_plateau_watchdog`. Expected
  output: stdout contains "all unit tests passed".
* **Smoke gate result**: Confirm `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/logs/smoke_gate.json`
  exists; run `jq '[.cells[] | select(.pass == true)] | length' logs/smoke_gate.json`. Expected
  output: `5` (all 5 reference cells pass).
* **Final cost <= $5.00**: After teardown, run
  `jq '.machines[].cost_usd' tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/remote_machines_used.json`
  (or check the orchestrator's costs.json). Expected output: total <= $5.00.
* **Generation count**: Run
  `jq 'length' tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/hv_trajectory.json`. Expected
  output: integer in `[13, 18]` (8 from t0081 + 5-10 additional gens).
* **Pareto front size**: Run
  `jq '.pareto_cells | length' tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json`.
  Expected output: integer >= 16 (t0081's size; should grow with continuation).
* **Joint-pass cell count**: Run `jq '[.pareto_cells[] | select(.dsi >= 0.4 and .pd_rate_hz
  > = 10.0)] | length' tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json`.
  > Expected output: = 1 (cell 767 alone is preserved by elitist survival; ideally >= 2 to satisfy
  > primary pass criterion).
* **Final HV monotonicity**: Run
  `jq '.[].hypervolume' tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/hv_trajectory.json | tail -1`.
  Expected output: float >= 16.33 (t0081's final HV; secondary pass criterion).
* **Charts produced**: Run `ls tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/images/*.png`.
  Expected output: 4 files (`pareto_front.png`, `hypervolume_trajectory.png`,
  `all_cells_scatter.png`, `parameter_distribution_per_generation.png`).
* **Metrics file format**: Run
  `jq '.spec_version, (.variants | length)' tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/metrics.json`.
  Expected output: `spec_version` matches the current metrics_specification value; variant count
  equals Pareto front size + 1 (closest-to-joint cell variant).
* **Requirement coverage check**: Read `plan.md` Task Requirement Checklist and confirm every REQ-*
  item has at least one step reference in `## Step by Step`. Expected output: all 16 REQ-* IDs
  (REQ-1 through REQ-16) appear in step descriptions.
* **Vast.ai instance destroyed**: Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0083_bedb_v3_extend_nsga2_gen8plus -- python -m arf.scripts.verificators.verify_machines_destroyed t0083_bedb_v3_extend_nsga2_gen8plus`.
  Expected output: exit code 0, no errors.
