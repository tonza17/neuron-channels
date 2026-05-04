# Plan: Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start

## Objective

Re-run NSGA-II on the t0080 v3 dendritic-spike-augmented Bed B substrate at the originally planned
scope (pop=96 / gen=8 = 768 cells) with a combined warm-start initial population (5 t0080 Pareto
cells + 17 t0078 Pareto cells projected to 54-d + 74 LHS) to determine whether the t0080 negative
result holds at adequate budget. Pass criterion: at least one Pareto cell with
`DSI ≥ 0.4 AND PD ≥ 10 Hz`, OR a clean architectural negative result at 4× the t0080 cell count
and with a strong warm-start.

## Approach

t0081 reuses the t0080 substrate library and NSGA-II harness verbatim. Only two new modules are
written:

* `code/warm_start.py` (~100 LOC) — assembles the 96-cell warm-started initial population by
  loading t0080's Pareto front (5 cells, 54-d normalised), projecting t0078's Pareto front (17
  cells, 49-d natural → 54-d normalised with random LHS for the 5 new dims), and filling with 74
  fresh LHS samples.
* `code/run_loop.py` (~40 LOC) — thin wrapper calling t0080's `nsga2_loop` with
  `NSGA2(pop_size=96, sampling=Population.new("X", custom_array))`.

A pre-launch smoke gate re-evaluates the 5 t0080 Pareto cells on the fresh Vast.ai instance and
confirms DSI / PD reproduce within tolerance (substrate-consistency check that t0080 deferred). The
full NSGA-II run then executes with cost-cap watchdog at $3.00.

## Cost Estimation

Per-cell cost on EPYC 7B13 64-core at $0.2382/hr (measured by t0080): **$0.00284 per cell**.

* NSGA-II run: 768 × $0.00284 = **$2.18**
* Provisioning + idle + teardown overhead: **~$0.20**
* **Target total: ~$2.38** (researcher-authorised envelope $1.50–$2.50 effective; $3.00 hard cap)

Alternative pricing if cheaper EPYC 7B13 offer available ($0.16/hr): ~$1.60 total.

Project budget: $5.74 spent of $10.00. After-task spent ~$8.12 (just over the 80% warn threshold but
well below stop). Acceptable.

## Step by Step

1. **Add dependencies if needed**: pymoo and numpy already present in t0080's `pyproject.toml`; no
   new deps for t0081.

2. **Write `code/warm_start.py`**:
   * `load_t0080_pareto() -> np.ndarray` — reads t0080's `pareto_front.json`, returns (5, 54).
   * `load_and_project_t0078_pareto(*, rng_seed: int = 42) -> np.ndarray` — reads t0078's
     `pareto_front.json` `pareto_cells[*].params_natural`, normalises 0–48 by t0080 bounds,
     samples 49–53 from `rng.uniform(0, 1)`, returns (17, 54).
   * `generate_lhs_fill(*, n_samples: int = 74, problem: BedBV3Problem, rng_seed: int = 43) -> np.ndarray`
     — uses pymoo `LHS()`.
   * `assemble_warm_start_population(*, problem: BedBV3Problem) -> np.ndarray` — concatenates,
     returns (96, 54).
   * `main()` CLI — writes `results/data/warm_start_population.json`.

3. **Write `code/run_loop.py`**: imports t0080's `BedBV3Problem`, `_save_pareto_front`, etc. Builds
   the 96-cell warm-start array via `assemble_warm_start_population`, wraps it in
   `pymoo.core.population.Population.new("X", arr)`, instantiates
   `NSGA2(pop_size=96, sampling=PopulationInit(pop))`, and runs `minimize()` with `n_gen=8` and the
   cost-cap callback. Saves results to t0081's `results/data/`.

4. **Local smoke gate**: locally compile MODs and re-evaluate the 5 t0080 Pareto cells using t0080's
   harness; confirm DSI / PD match within tolerance ±0.05 / ±1 Hz. If any cell diverges, halt and
   investigate before launching the remote run.

5. **SCP code to Vast.ai instance** (provisioned in step 8 setup-machines).

6. **Run `nrnivmodl` on remote** to compile MODs.

7. **Smoke gate on remote**: re-evaluate the 5 t0080 cells using the freshly compiled MODs; confirm
   DSI / PD match within tolerance. Records the substrate-consistency baseline.

8. **Launch NSGA-II loop** on remote in nohup background: pop=96 / gen=8 / max-workers=0 (use all 64
   effective cores) / hourly-rate=auto-from-instance.

9. **Monitor run** via SSH polling (every ~10 min) until process exits.

10. **Pull results** to local: `pareto_front.json`, `all_evaluations.json`, `hv_trajectory.json`,
    plus `nsga2_loop.log` and `warm_start_population.json`.

11. **Generate charts** locally via
    `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.plot_results` pointed at t0081's data dir
    (or a thin wrapper).

12. **Compute metrics** via `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_metrics`
    pointed at t0081's data dir.

## Remote Machines

One Vast.ai 64-core CPU instance, AMD EPYC 7B13 family, 503 GB RAM (overkill but standard for the
class), 25 GB disk, Debian 12 / `python:3.12-bookworm`. Target $0.16–$0.24/hr.

## Assets Needed

* `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset from t0080 — provides the v3
  substrate (cell builder, mech list, RANGE writers, MOD files).

## Expected Assets

None. `expected_assets`: `{}`. The task produces results files, not new substrate or answer assets.

## Time Estimation

* Setup-machines: ~15 min (provisioning + apt + venv + NEURON / pymoo install + MOD compile +
  verification)
* Local smoke gate: ~5 min (sequential 5-cell re-eval)
* Remote smoke gate: ~5 min
* NSGA-II main run: 768 × 43 s = **~9.2 h** wall-clock at 64-core sequential per cell
* Teardown: ~5 min
* Results / charts / metrics: ~10 min
* Total wall-clock: **~10 h**

## Risks & Fallbacks

* **Smoke gate fails on t0080 Pareto cell reproducibility** (DSI / PD don't match within tolerance):
  document the substrate-consistency delta in results; proceed with the NSGA-II run anyway since the
  warm-start cells will adapt. Note that this would be a finding worth flagging for next-task
  discussion.
* **Per-cell wall-clock exceeds 50 s** (e.g., active dendritic-spike machinery slows simulation):
  cost-cap watchdog kills run as needed; partial Pareto front is still useful. At 60 s/cell, total
  768 × 60 s = 12.8 h = $3.05 — exceeds cap by 2%. The watchdog would trip near gen 7 of 8,
  leaving an almost-complete Pareto front.
* **Vast.ai 64-core EPYC 7B13 unavailable**: fall back to 36-core or 72-core EPYC at ≤ $0.20/hr;
  per-cell wall-clock scales inversely with core count.
* **Project budget warn threshold ($8.00) reached partway**: t0081 itself doesn't trip the warn;
  after-task spent is ~$8.12. Acceptable. Future tasks would need to be cost-conscious.
* **Warm-start cells produce unstable behaviour** (e.g., some t0078 cells with random new-dim values
  trigger runaway depolarisation): NSGA-II's `is_unstable` filter handles them; the Pareto front
  filtering excludes them.
* **NSGA-II diversity collapse despite warm-start**: 74 LHS cells mitigate this. If it happens
  anyway, document and recommend NSGA-III or restart strategies in suggestions.

## Verification Criteria

* `verify_task_results.py`, `verify_task_metrics.py`, `verify_task_file.py`,
  `verify_task_dependencies.py`, `verify_task_folder.py`, `verify_logs.py`,
  `verify_research_code.py`, `verify_compare_literature.py`, `verify_machines_destroyed.py`,
  `verify_suggestions.py`, `verify_plan.py` — all PASS with 0 errors.
* Vast.ai instance destroyed cleanly per `verify_machines_destroyed.py`.
* Final cost ≤ $3.00 hard cap.
* Pre-merge verificator passes with 0 errors.
* Pareto front contains ≥ 5 non-dominated feasible cells.
* `warm_start_population.json` recorded the actual 96-cell starter array used.

## Task Requirement Checklist

* **REQ-1**: Reuse t0080's `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset unchanged. →
  Verified by Python import in `code/run_loop.py`.
* **REQ-2**: Reuse t0080's NSGA-II harness (`nsga2_loop.py` + workers + watchdog) unchanged. →
  Verified by import path; no fork.
* **REQ-3**: Generate the 96-cell warm-start initial population from 5 t0080 Pareto cells (verbatim
  54-d normalised) + 17 t0078 Pareto cells (projected 49-d natural → 54-d normalised, with the 5
  new dims sampled at random LHS per a fixed seed) + 74 fresh LHS. → Verified by
  `code/warm_start.py:assemble_warm_start_population`.
* **REQ-4**: NSGA-II run at pop=96 / gen=8 = 768 evaluations. → Verified by `code/run_loop.py` CLI
  args; final n_evals == 768 ± 1 reported in `nsga2_loop.log`.
* **REQ-5**: Hard biological lower bounds (`nav16_ais` ≥ 0.25 S/cm²; AIS-to-soma Nav ratio ≥ 5)
  honoured. → Same as t0080; reused via `BedBV3Problem`.
* **REQ-6**: Cost-cap watchdog armed at $3.00 hard cap; final cost ≤ $3.00. → Verified by
  `costs.json`.
* **REQ-7**: Pre-launch substrate-consistency smoke gate re-evaluates t0080's 5 Pareto cells and
  confirms DSI / PD match within ±0.05 / ±1 Hz. → Verified by `logs/smoke_gate.json` (or
  `results_detailed.md` Methodology section).
* **REQ-8**: 8 directions × 20 seeds × 1400 ms FULL HH per cell. → Same as t0080; reused.
* **REQ-9**: Per-cell registered metrics in `results/metrics.json` for each Pareto cell + the
  closest-to-joint cell. → Verified by `verify_task_metrics.py`.
* **REQ-10**: Pareto front PNG + hypervolume trajectory PNG + all-cells scatter PNG embedded in
  `results_detailed.md`. → Verified by `results_detailed.md` content.
* **REQ-11**: Vast.ai instance destroyed cleanly. → Verified by `verify_machines_destroyed.py`.
* **REQ-12**: Compare-literature step compares the t0081 Pareto front to t0078, t0080, and the
  published baselines (RivlinEtzion, deRosenroll, Park, Sivyer, Oesch, Trenholm, Werginz, Kole,
  Goethals). → Verified by `results/compare_literature.md`.
