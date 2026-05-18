---
spec_version: "2"
task_id: "t0106_long_pdnd_nsga2_300gen"
date_completed: "2026-05-17"
status: "complete"
---
# Plan: Long 2-Direction NSGA-II at 300 Generations on the 68-d Bed B + Morphology Substrate

## Objective

Re-run the t0102 / t0104 68-d Bed B + 14-d morphology NSGA-II lineage with four surgical changes
that trade angular sampling and replicate count for generation count on a single GA seed: (1) cut
angular sampling from 16 directions to **2** (PD = 0 deg, ND = 180 deg); (2) redefine DSI as the
antipodal ratio `(PD_rate - ND_rate) / (PD_rate + ND_rate)` (mathematically equal to the existing
vector-sum DSI when only PD and ND are sampled, so the patch is a single constant change); (3) drop
`N_EVAL_SEEDS` from 4 to 3; (4) extend `n_gen` from 20 to **300** (hard cap, extendable) on a
**single** GA seed (44) at `pop = 96` random-LHS init, with hourly hypervolume polling and an
operator-controlled stop mechanism via `intervention/stop.md`. The DSI silence guard (total spike
count across PD + ND < 10 returns DSI = 0.0) is inherited verbatim from t0104. The hard cost cap is
**$25** (per-instance watchdog $20, total task cap $25) against a project headroom of $28.72
(project budget recently raised from $50 to $75 on main commit `1d50246d`; current spend $46.28).
Success criteria: produce **1 predictions asset** (every evaluated cell across all completed
generations, with per-cell ratio DSI, PD-rate, ND-rate, total spike count, parameter vector,
generation index) and **1 answer asset** addressing whether long-running 2-direction NSGA-II
recovers strict joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz) from random init, and the gen at
which hypervolume plateaus on this landscape. Both a positive (>= 1 joint-pass cell) and a negative
(0 cells) result are publishable.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0106_long_pdnd_nsga2_300gen/task.json` and the resolved long
description at `tasks/t0106_long_pdnd_nsga2_300gen/task_description.md`:

```text
Name: Long 2-direction NSGA-II at 300 gens, 1 seed, 3 trials (ratio DSI + PD-rate)

Short description: Open-ended 68-d NSGA-II using only PD and ND bars, 1 random GA seed,
pop=96, n_eval_seeds=3, n_gen=300 (extendable). Hourly HV poll, operator-controlled stop,
$25 hard cap.

Expected assets: 1 predictions, 1 answer.

Long description (excerpts):
* Fork t0104's code/ verbatim and apply targeted patches.
* constants_morphology.py: ANGLES via N_DIRECTIONS = 2 (yields [0.0, 180.0] at the existing
  expression); N_EVAL_SEEDS = 3; N_GEN = 300.
* evaluator.py: existing _vector_sum_dsi already returns the ratio DSI at n=2; no algorithm
  change needed beyond the constants patch. Optionally rename _vector_sum_dsi -> _ratio_dsi
  for clarity.
* DSI silence guard: total spike count across PD + ND < 10 returns DSI = 0.0 (verbatim
  from t0104 evaluator.py:343-346, threshold constant SILENCE_SPIKE_COUNT_THRESHOLD = 10).
* nsga2_driver.py: single GA seed = 44, pop = 96, n_gen = 300, n_eval_seeds = 3, hourly HV
  trace at logs/steps/<step_id>/hv_trace.jsonl (one JSON line per gen with gen,
  wall_clock_s, hv, n_cells_evaluated). Add OperatorStopTermination(Termination) polling
  intervention/stop.md each gen. Add PerGenerationPoolRestart callback closing and
  recreating multiprocessing.Pool every 25 generations to mitigate NEURON memory
  accumulation. dill checkpoint each gen at logs/steps/<step_id>/checkpoint_gen<NNNN>.pkl.
* Cost watchdog: per-instance $20, total task $25 hard cap. Teardown within 5 min of last
  completed gen or stop-file detection.
* Vast.ai search: EPYC class CPU (7B13 or equivalent), >= 100 GB RAM, RTX 3060 Ti /
  equivalent idle, reliability >= 0.99, dph <= 0.40, post-filter for EPYC family
  (mirroring t0104's pattern).
* MOD compilation: 13 .mod files from tasks/t0080_*/code/mods/ + t0024 vendored MODs
  compiled on the Vast.ai instance with nrnivmodl.
* Smoke gate (5 steps, local, pre-Vast.ai): one-cell evaluator returns DSI in [0,1] and
  PD-rate in sane range; silence-guard sensitivity sweep across thresholds {5, 10, 20};
  unit-test test_evaluator_dsi_guard passes; ratio-DSI cross-check (PD=5, ND=1 -> 0.667).
  Must pass before any Vast.ai provisioning.
* Expected assets: 1 predictions (nsga2-seed44-bedb-morph-2dir-300gen) + 1 answer
  (joint-pass-recovery + HV-plateau question).
* Verification: hv_trace.jsonl well-formed; predictions asset cardinality
  96 x (1 + n_gen_completed); cost <= $25.00; Vast.ai instance destroyed.
```

Concrete requirements decomposed (each item names the step that satisfies it and the evidence that
proves completion):

* **REQ-1** — **Ratio DSI metric correctness.** The evaluator returns
  `(PD_rate - ND_rate) / (PD_rate + ND_rate)` for every evaluated cell at `n_directions = 2`.
  Satisfied by step 3 (constants patch) plus step 6 (smoke gate cross-check). Evidence:
  `code/test_evaluator_dsi_guard.py` includes a synthetic case PD = 5, ND = 1 that asserts the
  returned DSI is within 1e-6 of 0.6667.
  `grep -n "N_DIRECTIONS: int = 2" tasks/t0106_*/code/constants_morphology.py` matches one line.
* **REQ-2** — **Silence-guard activation at threshold 10.** Cells with total spike count across PD
  \+ ND below 10 must return DSI = 0.0 (not 1.0). Satisfied by step 3 (inherit guard verbatim) and
  step 6 (smoke gate). Evidence: `tasks/t0106_*/code/evaluator.py` contains the guard line and the
  unit test `test_evaluator_dsi_guard.py` exercises it across thresholds {5, 10, 20} on a synthetic
  silent-corner case.
* **REQ-3** — **Single-seed compliance.** Exactly one GA seed (44) is executed at pop = 96,
  n_eval_seeds = 3, n_gen = 300 (hard cap). Satisfied by step 3 (constants patch) and step 8 (driver
  invocation). Evidence: `grep -n "T0106_SEEDS" tasks/t0106_*/code/constants.py` shows `(44,)` and
  the predictions asset filename includes `seed44`.
* **REQ-4** — **Hourly HV trace presence.** `logs/steps/<step_id>/hv_trace.jsonl` exists and
  contains one well-formed JSON line per completed generation with fields `gen`, `wall_clock_s`,
  `hv`, `n_cells_evaluated`. Satisfied by step 4 (callback implementation) and step 8 (run).
  Evidence: line count of `hv_trace.jsonl` equals `n_gen_completed`; every line parses as JSON with
  the four required keys.
* **REQ-5** — **Operator-stop mechanism.** Driver checks `intervention/stop.md` each generation;
  if present, completes the in-flight generation, writes the final dill checkpoint, and signals
  halt. Satisfied by step 4 (OperatorStopTermination subclass) and step 8 (run). Evidence:
  `grep -n "OperatorStopTermination" tasks/t0106_*/code/nsga2_driver.py` returns the subclass body
  and its membership in the `TerminationCollection`.
* **REQ-6** — **Per-25-gen Pool restart.** The driver closes and recreates the
  `multiprocessing.Pool` every 25 generations to mitigate NEURON memory accumulation (a NEW pattern
  not present in t0102 / t0104; cited from `research_code.md` finding "Per-Generation Worker Pool
  Restart Pattern Does Not Yet Exist in the Lineage"). Satisfied by step 4 (callback implementation)
  and step 8 (run). Evidence: `grep -n "PerGenerationPoolRestart"` and
  `grep -n "_POOL_RESTART_EVERY = 25"` both return matches in `nsga2_driver.py`.
* **REQ-7** — **Smoke-gate gate before provisioning.** The 5-step local smoke gate per
  `research_code.md` must pass before any Vast.ai provisioning. Satisfied by step 6. Evidence:
  `logs/steps/008_implementation/smoke_gate.json` exists with all five checks `passed: true`. If any
  check fails, step 7 (provisioning) MUST NOT be entered; an intervention file is created instead.
* **REQ-8** — **Vast.ai instance under $25.** Total cost across the run does not exceed $25.00.
  Per-instance $20 watchdog enforces a lower stop. Satisfied by steps 7-10. Evidence: the
  implementation step writes `results/costs.json` with total <= 25.00 and
  `verify_machines_destroyed` confirms the instance was destroyed within 5 min of the last completed
  gen.
* **REQ-9** — **Vast.ai search criteria.** Provisioning filters: EPYC class CPU (7B13 or
  equivalent), >= 100 GB RAM, RTX 3060 Ti / equivalent (idle, CPU-only NEURON workload), reliability
  > = 0.99, dph <= 0.40, post-filter for EPYC family. Satisfied by step 7. Evidence:
  > `logs/steps/007_setup-machines/offer_filters.json` records the exact filter set and the chosen
  > offer's CPU model contains "EPYC".
* **REQ-10** — **MOD compilation succeeds on the instance.** 13 .mod files from
  `tasks/t0080_*/code/mods/` and the t0024 vendored MODs are SCP'd and compiled with `nrnivmodl`,
  producing `x86_64/.libs/libnrnmech.so`. Satisfied by step 7. Evidence:
  `logs/steps/007_setup-machines/mod_compile.log` shows `nrnivmodl` exit 0 and a file listing of the
  produced shared library.
* **REQ-11** — **Predictions asset format.**
  `assets/predictions/nsga2-seed44-bedb-morph- 2dir-300gen/` exists with `details.json`
  (spec_version "2"), `description.md`, and at least one file under `files/`. The asset contains
  exactly `96 x (1 + n_gen_completed)` cells. Satisfied by step 9. Evidence:
  `verify_predictions_asset` returns 0 errors; `wc -l files/cells.jsonl` matches the expected count.
* **REQ-12** — **Answer asset format.** `assets/answer/<answer_id>/` exists with `details.json`
  and a canonical answer document. The answer names the converged HV gen, the best ratio-DSI in the
  run, the count of strict joint-pass cells (which may be zero), and explicitly addresses both H1
  (joint-pass recovery) and H2 (HV plateau location). Satisfied by step 9 (asset write during
  implementation; final answer text is written in the orchestrator-managed reporting step).
  Evidence: `verify_answer_asset` returns 0 errors on the asset structure created during
  implementation.
* **REQ-13** — **HV plateau characterisation.** The implementation step produces a chart showing
  HV vs generation across all completed gens, with a marker at the gen at which the 60-min
  moving-window HV improvement first falls below 1%. Satisfied by step 9. Evidence:
  `results/images/hv_trajectory.png` exists; `results/images/pareto_front_evolution.png` exists.
* **REQ-14** — **Joint-pass tally.** The implementation step computes the count of strict
  joint-pass cells (ratio DSI >= 0.5 AND PD-rate >= 30 Hz, post-silence-guard) across all completed
  generations and writes it to `results/metrics.json` as the key `joint_pass_count`. Satisfied by
  step 9. Evidence: `results/metrics.json` contains a `joint_pass_count` integer value (>= 0).
* **REQ-15** — **Registered direction_selectivity_index metric reported.** Best ratio DSI across
  all evaluated cells is written to `results/metrics.json` under the registered key
  `direction_selectivity_index`. Satisfied by step 9. Evidence:
  `cat results/metrics.json | python -c "import sys,json;print(json.load(sys.stdin))"` shows the key
  present with a float value in [0.0, 1.0].

* * *

## Approach

**Task types recommended**: this task is tagged in `task.json` as `experiment-run`, `data-analysis`,
`answer-question`. The Planning Guidelines from `meta/task_types/experiment-run/instruction.md`
drive the design: fixed seeds, per-subset metric breakdowns (here per-generation), explicit
validation gates (the 5-step smoke gate before Vast.ai provisioning), cost tracking against the $25
hard cap, charts saved to `results/images/`, predictions asset under `assets/predictions/`.

**Technical approach (grounded in `research_papers.md`, `research_internet.md`, and
`research_code.md`).** Fork t0104's `code/` directory verbatim (~2400 lines across 14 files) and
apply targeted patches to seven files (~120 total patch lines) per the diff sketch in
`research_code.md`. The four substantive evaluator-side changes are:

1. **2-direction angular sampling.** `constants_morphology.py:N_DIRECTIONS: int = 2`. The existing
   `evaluator.py:419` expression `[float(d) * (360.0 / n_directions) for d in range(n_directions)]`
   yields `[0.0, 180.0]` exactly at `n_directions = 2`, so no evaluator algorithm change is
   required. The t0104 `_vector_sum_dsi` function already returns the ratio DSI identically at
   `n = 2` (proven in `research_code.md`: `total_x = mean_PD - mean_ND`, `total_y = 0` so the
   function returns `|mean_PD - mean_ND| / (mean_PD + mean_ND)`). A unit test in
   `test_evaluator_dsi_guard.py` asserts numeric equivalence on a synthetic PD = 5, ND = 1 case.
2. **N_EVAL_SEEDS reduced 4 -> 3.** `constants_morphology.py:N_EVAL_SEEDS: int = 3`. The literature
   converges (`research_papers.md` finding "Sample Averaging With 3 - 5 Replicates Is the
   Literature-Converged Trade-off") on spending budget on parameter diversity rather than within-
   cell noise averaging. Budszuhn 2025's static-N = 1 result for chi-squared noise validates this;
   our noise is light-tailed (per t0102 / t0104 empirical logs) so the polynomial-time noise-
   robustness guarantee from Dang 2023 still applies (per-trial noise `p ~ 0`, well below the
   `p = 0.5` phase transition).
3. **n_gen 20 -> 300, single GA seed 44.** `constants_morphology.py:N_GEN: int = 300`,
   `constants.py:T0106_SEEDS: tuple[int, ...] = (44,)`. Literature priors place the NSGA-II plateau
   on biophysical problems between gens 50-150 (Mohacsi 2024 controlled benchmark at 12-d, ~20-60
   gens; Druckmann 2007 at 12-d, ~300 gens; Poleg-Polsky 2026 at variable d, 300 gen default with
   1000 reserved for low-performers). t0106's 28 896 evaluations on 68 d (425 eval/param) sits at
   ~5% of Chen 2024's per-parameter density (50 000 eval/param) but >14x larger than t0102's
   per-seed budget.
4. **Hourly HV trace + operator-stop + dill checkpoint + per-25-gen Pool restart.** The driver is
   patched in `nsga2_driver.py`. Per `research_code.md` patch table:
   * `OperatorStopTermination(Termination)` subclass polling `intervention/stop.md` in `_update`,
     returning 1.0 when the file exists (matches t0104's pattern of using a `Termination` subclass
     in `TerminationCollection`, not a `Callback` with `force_termination`, which would race with
     the existing collection).
   * `_GenerationCallback` (the existing t0104 callback) is extended to write one JSON line per gen
     to `hv_trace.jsonl` with `gen`, `wall_clock_s`, `hv`, `n_cells_evaluated` (the schema from
     `task_description.md`), and to dill-dump the `Algorithm` object to `checkpoint_gen<NNNN>.pkl`.
   * `PerGenerationPoolRestart` callback closes and recreates the `multiprocessing.Pool` every 25
     generations; swaps `problem.elementwise_runner` to the fresh `StarmapParallelization`. This is
     the load-bearing NEW pattern (not present in t0102 / t0104 — they all run a single `Pool` for
     the entire `minimize()` call). At 300 gens on a single instance, NEURON memory accumulation is
     a real risk per the t0102 plan risk row.

**Alternatives considered**:

* **Callback-with-`force_termination` pattern for operator stop** (per `research_internet.md`
  pymoo-callback pattern 1). Rejected because t0104 already uses a `TerminationCollection` and two
  stop mechanisms racing on the same algorithm is a known footgun. A `Termination` subclass fits
  cleanly into the existing collection.
* **Manual ask-tell loop with stop polling in the outer Python loop** (`research_internet.md`
  pattern 2). Rejected because it would require reimplementing the evaluator binding from scratch
  and lose the t0104 `_DriverState`/`_GenerationCallback` infrastructure.
* **Two or three GA seeds at fewer generations** (e.g., 3 seeds x 100 gens). Rejected because the
  research priors place the plateau between gens 50-150 on this dimensionality, so 100 gens may not
  reach plateau on a single seed; the single-seed-300-gen design is the cleanest test of the H2
  (continued HV improvement past gen 20) hypothesis. If t0106 finds joint-pass cells, a follow-up
  (S-0106-XX) will confirm with seeds 55 and 66 at the converged gen count.
* **CMAES instead of NSGA-II.** Rejected because Mohacsi 2024 shows CMAES wins on harder benchmarks
  but NSGA-II is the established lineage method, and changing both the algorithm and the search
  budget in the same task would confound the result. CMAES is logged as a candidate follow-up.

**Smoke-gate gating (validation gate for the expensive Vast.ai run).** Per `research_code.md`, the
5-step local smoke test runs one cell on Windows using the t0024 vendored `nrnmech.dll` before any
Vast.ai provisioning. The smoke gate checks: (1) single-cell evaluation returns within 30 s with DSI
in [0, 1] and PD-rate in [0, 200 Hz]; (2) `nd_rate <= pd_rate` for the bedb_like anchor; (3)
silence-guard sensitivity sweep across thresholds {5, 10, 20} all zero-out DSI on a degenerate PD =
0 case; (4) `test_evaluator_dsi_guard.py` passes; (5) ratio-DSI cross-check PD = 5, ND = 1 returns
0.6667 +/- 1e-6. Failure of any check halts provisioning and creates an intervention file.
**Baseline comparison**: the t0104 seed-55 gen-11 best cell (DSI = 0.5417, PD = 3.57 Hz on
vector-sum) is the relevant within-project baseline; t0106's best ratio DSI must not be worse than
that in expectation (per H3 in `task_description.md`).

* * *

## Cost Estimation

* **Vast.ai RTX 3060 Ti instance (idle GPU, CPU-only NEURON workload)**: $0.36/hr * 20 h = **$7.20**
  productive compute. Setup / idle overhead between MOD compilation and driver start: ~30 min at
  $0.36/hr = **$0.18**. Conservative buffer for retries and post-run download: **$2.00**.
* **No LLM API costs** — all NSGA-II logic runs locally on the Vast.ai instance with no external
  API calls.
* **Estimated total**: **$10-18 expected**, **$25 hard cap** (per-instance watchdog $20 +
  orchestrator-level $25 ceiling).
* **Project budget context**: project total recently raised from $50 to $75 on main commit
  `1d50246d` (current spend $46.28, headroom $28.72). The t0106 $25 hard cap fits within the
  headroom with $3.72 buffer. If the run exits early via operator stop at the empirical plateau
  (most likely gens 100-200 per research priors), actual spend will be **$5-12**.
* **Per-task default limit override**: $25 hard cap, explicit override above the $8 project default
  (declared in `task_description.md`).

* * *

## Step by Step

Implementation work only — orchestrator-managed steps (results writing, suggestions, compare-
literature, reporting) are not in this list per the plan specification.

### Milestone 1: Local Code Fork + Smoke Gate (steps 1-6)

1. **Copy t0104 `code/` verbatim into `tasks/t0106_long_pdnd_nsga2_300gen/code/`.** Source:
   `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/` (entire directory, ~14 files, ~2400 lines).
   Inputs: t0104 code directory. Outputs: `tasks/t0106_long_pdnd_nsga2_300gen/code/` mirror.
   Expected observable output: file count and `wc -l` total match t0104. **Satisfies REQ-1, REQ-2
   (groundwork).**

2. **Rewrite package import paths.** In every copied `.py` file, replace
   `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds` with `tasks.t0106_long_pdnd_nsga2_300gen`. Inputs:
   step 1 output. Outputs: identical structure with corrected imports. Expected output:
   `grep -r "t0104_nsga2_2obj_dsi_pdrate_3seeds" tasks/t0106_*/code/` returns zero matches.
   **Satisfies REQ-1, REQ-2 (groundwork).**

3. **Patch constants and paths.** Edit per the `research_code.md` patch table:
   * `code/constants_morphology.py`: line 111 `N_GEN: int = 20 -> 300`; line 127
     `N_EVAL_SEEDS: int = 4 -> 3`; line 128 `N_DIRECTIONS: int = 16 -> 2`.
   * `code/constants.py`: replace `T0104_SEEDS = (44, 55, 66) -> T0106_SEEDS = (44,)` and
     `T0104_HARD_BUDGET_PER_SEED_USD = 4.00 -> T0106_HARD_BUDGET_USD = 25.00`; add
     `T0106_PER_INSTANCE_WATCHDOG_USD = 20.00`. Update downstream import names.
   * `code/paths.py`: replace `t0104_nsga2_2obj_dsi_pdrate_3seeds -> t0106_long_pdnd_nsga2_300gen`
     in every path constant. Add `hv_trace_jsonl(step_id: str) -> Path`, `stop_signal_md() -> Path`,
     `checkpoint_dill(seed: int, gen: int) -> Path`.
   * `code/smoke_gate.py`: change `seeds_eval` to length-3 tuple matching `N_EVAL_SEEDS = 3`; change
     `n_directions=8 -> n_directions=2` in the `evaluate_68d_vector` call; add per-cell sanity check
     `dsi_vector_sum in [0, 1]`.
   * `code/random_init.py`: update `T0104_SEEDS` import to `T0106_SEEDS`. Inputs: step 2 output.
     Outputs: patched constants and paths. Expected output:
     `grep -n "N_DIRECTIONS: int = 2" tasks/t0106_*/code/constants_morphology.py` matches one line.
     **Satisfies REQ-1, REQ-2, REQ-3.**

4. **Patch `nsga2_driver.py` to add operator stop, hourly HV trace, dill checkpoint, and per-25-gen
   Pool restart.** Per the unified-diff sketch in `research_code.md`:
   * Add `class OperatorStopTermination(Termination)` polling `intervention/stop.md` in `_update`;
     returns 1.0 when the file exists. Splice into the existing `TerminationCollection` alongside
     `MaximumGenerationTermination`, `HVPlateauTermination`, `CostWatchdogTermination`.
   * Extend `_GenerationCallback.notify` to write one JSON line per gen to
     `paths.hv_trace_jsonl(step_id)` with `gen`, `wall_clock_s`, `hv` (via
     `pymoo.indicators.hv.HV(ref_point=[0.0, 0.0]).do(F)`), `n_cells_evaluated`. Also
     `dill.dump(algorithm, ...)` to `paths.checkpoint_dill(seed, gen)`.
   * Add `class PerGenerationPoolRestart(Callback)` that wraps `_GenerationCallback`; every 25
     generations, close the current `multiprocessing.Pool`, recreate it, and swap
     `problem.elementwise_runner = StarmapParallelization(pool.starmap)`. Module constant
     `_POOL_RESTART_EVERY: int = 25`.
   * Relax or disable `HVPlateauTermination` per the t0102 plateau-watchdog finding (its
     `window=2, min_history=4` will spuriously trigger on 300-gen runs). Either remove it from the
     collection or set `MIN_HV_HISTORY=60` (1-hour sliding window at 60s/gen).
   * Default the budget to `T0106_HARD_BUDGET_USD = 25.00`; the `CostWatchdogTermination` reads this
     constant. Inputs: step 3 output. Outputs: patched `nsga2_driver.py`. Expected output:
     `grep -n "OperatorStopTermination\|PerGenerationPoolRestart\|_POOL_RESTART_EVERY" tasks/t0106_*/code/nsga2_driver.py`
     returns three matches. **Satisfies REQ-4, REQ-5, REQ-6.**

5. **Patch `evaluator.py` cosmetically (optional).** Leave the existing `_vector_sum_dsi` function
   in place (it returns the ratio DSI identically at `n = 2`); optionally rename to `_ratio_dsi` for
   clarity. Update package import paths. Verify `evaluator.py:419` still reads
   `[float(d) * (360.0 / n_directions) for d in range(n_directions)]` (this yields `[0.0, 180.0]` at
   `n_directions = 2`). Update `evaluator.py:455`'s `BedBV3MorphProblem` keyword dict to keep
   `"n_obj": 2`. Inputs: step 4 output. Outputs: patched `evaluator.py`. Expected output:
   `grep -n '"n_obj": 2' tasks/t0106_*/code/evaluator.py` matches one line. **Satisfies REQ-1.**

6. **Run the 5-step local smoke gate (gating gate before Vast.ai).** This is the explicit validation
   gate for the expensive Vast.ai operation.
   * **Baseline comparison**: t0104 seed-55 gen-11 best cell at DSI = 0.5417, PD = 3.57 Hz. The
     smoke gate's bedb_like anchor cell should produce DSI in `[0.1, 0.9]` and PD-rate in
     `[5, 100] Hz` — a sanity range, not the operating point.
   * Run
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0106_long_pdnd_nsga2_300gen -- python -u -m tasks.t0106_long_pdnd_nsga2_300gen.code.smoke_gate`.
     Expected: 5 sub-checks all green within 5 min wall-clock total.
   * Run
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0106_long_pdnd_nsga2_300gen -- python -u -m pytest tasks/t0106_long_pdnd_nsga2_300gen/code/test_evaluator_dsi_guard.py -v`.
     Expected: 0 failures.
   * **Validation failure condition**: if any of the 5 smoke-gate checks fail OR the unit-test suite
     reports any failure, halt — do not proceed to Vast.ai provisioning. Create
     `intervention/smoke_gate_failed.md` with the specific failure and STOP. **Inspect 5 individual
     cell evaluations from the smoke gate by reading the per-cell log output** (DSI, PD-rate,
     ND-rate, total spike count) and verify each is in the expected range before declaring the gate
     passed. Inputs: step 5 output. Outputs: `logs/steps/008_implementation/smoke_gate.json` (or
     equivalent) with all five checks passed. **Satisfies REQ-7.**

### Milestone 2: Remote Provisioning (steps 7-8)

7. **Provision the Vast.ai instance.** Run `setup-remote-machine` skill via the orchestrator.
   Filters per `task_description.md`: EPYC class CPU (7B13 or equivalent), >= 100 GB RAM, RTX 3060
   Ti / equivalent (idle, CPU-only NEURON workload), reliability >= 0.99, dph <= 0.40, post-filter
   for EPYC family (mirroring t0104's pattern: t0104 selected an EPYC 7B13 64-core Norway instance
   at $0.24/hr). Record `logs/steps/007_setup-machines/offer_filters.json`.
   * Install NEURON 8.2.7, NetPyNE 1.1.1, pymoo, dill, numpy, scipy via `uv sync` on the instance.
   * SCP 13 .mod files from `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` plus
     `mod_func.c` to the instance at the same relative path. The list (per `research_code.md`):
     `bkt80.mod`, `calt80.mod`, `catt80.mod`, `iht80.mod`, `kdrt80.mod`, `kv3t80.mod`, `kv4t80.mod`,
     `kv7t80.mod`, `napt80.mod`, `nart80.mod`, `nav16t80.mod`, `skahpt80.mod`, `skt80.mod`. Also SCP
     the t0024 vendored MOD sources at
     `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/`.
   * Run `nrnivmodl` in the `mods/` directory to produce `x86_64/.libs/libnrnmech.so`. Verify by
     `ls -la x86_64/.libs/libnrnmech.so` (file exists and is non-zero size). The t0024 compile is
     handled by `bootstrap.py:_compile_t0024_mods_linux` at evaluator startup. Inputs: step 6 pass.
     Outputs: provisioned Vast.ai instance with NEURON, MODs, and t0106 code. **Satisfies REQ-9,
     REQ-10.**

8. **Launch NSGA-II run (the load-bearing step).** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0106_long_pdnd_nsga2_300gen -- python -u -m tasks.t0106_long_pdnd_nsga2_300gen.code.nsga2_driver --seed 44 --teardown-on-watchdog`.
   The driver:
   * Initialises pop = 96 random LHS, `n_eval_seeds = 3`, `n_directions = 2`.
   * Runs the `TerminationCollection` (`MaximumGenerationTermination(n_max_gen=300)`,
     `CostWatchdogTermination(watchdog=$25)`, `OperatorStopTermination(stop_signal_md())`). The
     `HVPlateauTermination` is relaxed or disabled per step 4.
   * `_GenerationCallback` writes one JSON line per gen to `hv_trace.jsonl` and dill-checkpoints the
     algorithm to `checkpoint_gen<NNNN>.pkl`.
   * `PerGenerationPoolRestart` recreates `multiprocessing.Pool` every 25 gens.
   * Every 60 min, the orchestrator pulls `hv_trace.jsonl` from the remote instance, summarises the
     last hour's delta-HV, and posts a one-line status. The operator decides "continue" (default) or
     writes `intervention/stop.md` to halt at the next gen boundary.
   * **Validation gate (after first completed generation)**: pull `hv_trace.jsonl` after gen 1 and
     verify it has one well-formed JSON line. If the file is empty or malformed, halt and debug —
     do not let the run proceed past gen 5 before the trace file is verified.
   * **Per-cell baseline check**: after gen 1, pull 5 cells at random from the predictions log and
     verify `dsi_ratio in [0, 1]`, `pd_rate >= 0`, `nd_rate >= 0`. If any is out of range, halt and
     debug.
   * Inputs: step 7 provisioning. Outputs: `hv_trace.jsonl`, `checkpoint_gen<NNNN>.pkl` files,
     per-cell predictions log on the instance. Expected runtime: 12-20 h wall-clock; cost $5-18
     actual against $25 cap. **Satisfies REQ-3, REQ-4, REQ-5, REQ-6.**

### Milestone 3: Teardown and Asset Assembly (steps 9-10)

9. **Download artifacts, build assets, and produce charts.** Pull from the Vast.ai instance to the
   worktree:
   * `logs/steps/008_implementation/hv_trace.jsonl` (the per-gen HV trace).
   * All `checkpoint_gen<NNNN>.pkl` files to `logs/steps/008_implementation/checkpoints/`.
   * The per-cell predictions log (every evaluated cell across all completed gens). Then build the
     **predictions asset** at `assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/`:
   * `details.json` (spec_version "2", asset_id "nsga2-seed44-bedb-morph-2dir-300gen", model
     identifier "nsga2-seed44-2dir", dataset "synthetic", n_predictions =
     `96 x (1 + n_gen_completed)`, description_path "description.md", added_by_task =
     "t0106_long_pdnd_nsga2_300gen", date_added = "2026-05-17").
   * `description.md` per `meta/asset_types/predictions/specification.md`.
   * `files/cells.jsonl` with one line per evaluated cell (gen, cell_idx, parameter_vector [68-d],
     dsi_ratio, pd_rate_hz, nd_rate_hz, total_spike_count, robustness, n_errors, is_unstable).
   * **Validation**: `wc -l files/cells.jsonl` matches `96 x (1 + n_gen_completed)`.

   Then build the **answer asset** stub at `assets/answer/long-300gen-pdnd-recovery/`:
   * `details.json` (spec_version per spec) and `answer.md` with the question text from
     `task_description.md`'s Expected Assets section; final answer prose is filled by the reporting
     step (orchestrator-managed). The stub here must satisfy the asset structure verificator.

   Compute metrics and write `results/metrics.json` (legacy flat format because t0106 reports one
   configuration, not multiple variants):
   * `direction_selectivity_index` (registered metric): best ratio DSI across all evaluated cells
     (`max(dsi_ratio) over the predictions asset`).
   * `joint_pass_count` (operational, not registered): count of cells with
     `dsi_ratio >= 0.5 AND pd_rate_hz >= 30.0`.
   * `hv_plateau_gen` (operational): the gen at which the 60-min moving-window HV improvement first
     falls below 1%. If the run did not reach plateau, write `null` (the orchestrator-managed
     reporting step then documents the omission).
   * `n_gen_completed` (operational): the number of completed generations.
   * `n_cells_evaluated_total` (operational): total cells across all gens.
   * Per `meta/task_types/experiment-run/instruction.md`: efficiency metrics
     `efficiency_inference_time_per_item_seconds = total_wall_clock_s / n_cells_evaluated_total` and
     `efficiency_inference_cost_per_item_usd = total_cost_usd / n_cells_evaluated_total`. Note:
     training-time efficiency does not apply (NSGA-II is not conventional training); explicitly
     omitted per the style guide.

   Generate charts to `results/images/`:
   * `hv_trajectory.png` — HV vs gen with the plateau gen marked.
   * `pareto_front_evolution.png` — Pareto fronts at gens {10, 25, 50, 100, 200, final}.
   * `joint_pass_scatter.png` — scatter of (dsi_ratio, pd_rate_hz) across all cells with the
     joint-pass region shaded; comparison line to t0104 seed-55 best cell (DSI = 0.5417, PD = 3.57
     Hz on vector-sum).
   * `silence_guard_histogram.png` — histogram of total spike counts across all cells, with the
     threshold-10 cutoff marked.

   Inputs: step 8 outputs. Outputs: predictions asset, answer-asset stub, `metrics.json`, four
   charts. **Satisfies REQ-11, REQ-12, REQ-13, REQ-14, REQ-15.**

10. **Teardown Vast.ai instance.** Run `setup-remote-machine` skill in teardown mode (or call the
    orchestrator's teardown procedure). Verify destruction within 5 min of last completed gen or
    stop-file detection. Update `logs/steps/010_teardown/machine_log.json` with `destroyed_at`
    timestamp. Inputs: step 9 confirms all artefacts pulled. Outputs: `machine_log.json` with
    `destroyed: true` and Vast.ai dashboard confirms instance gone. **Satisfies REQ-8 (teardown
    half).**

* * *

## Remote Machines

**Single Vast.ai instance required.** Filters: EPYC class CPU (AMD EPYC 7B13 or equivalent like
7763), >= 100 GB RAM, RTX 3060 Ti or equivalent (idle — workload is CPU-only NEURON), reliability
> = 0.99, dph (dollars per hour) <= 0.40, post-filter for EPYC family (string match on
> `cpu_name LIKE '%EPYC%'`, mirroring the t0104 pattern). Expected hourly rate ~$0.24-0.36/h.
> Estimated wall-clock: 12-20 h. Cost cap: $25 total ($20 per-instance watchdog enforced inside
> `CostWatchdogTermination`; $25 orchestrator-level ceiling). Teardown within 5 min of last
> completed gen or `intervention/stop.md` detection. Reference:
> `arf/specifications/remote_machines_specification.md`.

* * *

## Assets Needed

* **Code substrate from t0104** (dependency `t0104_nsga2_2obj_dsi_pdrate_3seeds`): the entire
  `code/` directory copied verbatim and patched in 7 files per `research_code.md`.
* **MOD library source from t0080** (dependency `t0080_bedb_mobo_v3_dendritic_spike_nsga2`): 13
  `.mod` files plus `mod_func.c` at `tasks/t0080_*/code/mods/`, SCP'd to the Vast.ai instance and
  compiled with `nrnivmodl`.
* **t0024 Bed B port** (dependency `t0024_port_de_rosenroll_2026_dsgc`): vendored MOD sources at
  `assets/library/de_rosenroll_2026_dsgc/sources/`, plus the `constants` and
  `ar2_noise.generate_ar2_batch` modules imported via the standard task-import path.
* **Morphology generator from t0090 + t0092 patched** (dependencies
  `t0093_resweep_and_t0090_correction` + transitive): imported via full-path
  `tasks.t0090_*.code.morphology_params`, `tasks.t0092_*.code.morphology_generator_fix`,
  `tasks.t0092_*.code.baseline_channels`.
* **No external datasets or papers downloaded**; all reference numbers (literature priors) live in
  `research_papers.md` and `research_internet.md`.

* * *

## Expected Assets

Matches `task.json` `expected_assets`: 1 predictions, 1 answer.

* **1 predictions asset** at `assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/` containing
  every evaluated cell across all completed generations. Each cell record carries the 68-d parameter
  vector, ratio DSI, PD-rate, ND-rate, total spike count, robustness (computed but not selected on),
  n_errors, is_unstable, and the generation index. Total record count: exactly
  `96 x (1 + n_gen_completed)` cells.
* **1 answer asset** at `assets/answer/long-300gen-pdnd-recovery/` addressing the canonical
  question: *"Does long-running 2-direction NSGA-II on the 68-d Bed B + 14-d morphology substrate
  recover strict joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz) from random init, and where does
  hypervolume actually plateau on this landscape?"* The answer must name the converged HV gen, the
  best ratio DSI in the run, and the count of strict joint-pass cells. The final answer prose is
  written by the orchestrator-managed reporting step; this plan establishes only the asset stub.

* * *

## Time Estimation

* Research (already complete): ~2 h total across papers + internet + code (logged in
  `logs/steps/004-006_*`).
* Planning (this step): 0.5 h.
* Local code fork + patch + smoke gate (Milestone 1 / steps 1-6): **1-2 h** (~120 patch lines across
  7 files plus the 5-step smoke gate).
* Vast.ai provisioning + MOD compilation (Milestone 2 / step 7): **0.5-1 h**.
* NSGA-II run (step 8): **12-20 h** wall-clock (operator-gated; most-likely-plateau gen is 100-200
  per research priors, giving 7-14 h productive compute; the 20 h envelope assumes the 300-gen hard
  cap is reached without operator stop).
* Teardown + asset assembly + charts (Milestone 3 / steps 9-10): **2-3 h**.
* **Total wall-clock envelope: 18-26 h** (matches `task_description.md`).

* * *

## Risks & Fallbacks

Pre-mortem: if t0106 has failed completely at completion time, the most likely failure modes are:
(a) HV plateaus before gen 50 and the result reads as the substrate-limitation hardening with no new
information; (b) NEURON memory accumulation degrades wall-clock past gen 100 even with the Pool
restart; (c) operator forgets to check `hv_trace.jsonl` for 6+ hours and the cost watchdog triggers;
(d) the smoke gate passes but the Vast.ai run hits a structural difference (Linux MOD ABI, file-path
case sensitivity) that breaks the evaluator after launch; (e) ratio DSI behaves pathologically at
low spike counts despite the silence guard.

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| HV plateaus before gen 50, providing no new info | Medium | Low (negative result still publishable) | Hourly poll catches this; operator stops early; cost < $5; result reads as substrate-limitation control |
| NEURON memory accumulation degrades wall-clock past gen 100 | Medium | Medium (run blows wall-clock envelope) | Per-25-gen Pool restart (REQ-6); fallback restart every 10 gens if still slow past gen 150 |
| Operator misses hourly poll and cost watchdog triggers | Low | Medium ($5-10 wasted) | $20 per-instance watchdog inside `CostWatchdogTermination`; $25 orchestrator-level ceiling; idle-teardown within 5 min of last gen |
| Linux vs Windows MOD ABI mismatch surfaces after launch | Low | High (blocks the run after Vast.ai launch) | Smoke gate on Linux against the SCP'd MOD library *before* the production launch; abort and reprovision if mismatch detected |
| Ratio DSI pathological at low spike counts despite guard | Low | Medium (Pareto front concentrates at silent corner) | Smoke gate silence-guard sensitivity sweep at thresholds {5, 10, 20}; post-hoc analysis if guard threshold needs adjustment |
| 16-direction vector-sum DSI of t0106 top cells disagrees with the 2-direction ratio DSI (narrow-tuning artefact) | Medium | Medium (joint-pass claim weakens) | Post-hoc 16-direction re-evaluation of the top-10 Pareto cells at 4 trials per direction (logged as future work in `suggestions.json`, not in scope here) |
| Vast.ai preemption mid-run | Low | Medium (loses up to 1 gen progress) | Per-gen `dill` checkpoint enables resume from the latest gen; the JSONL trace is append-only |
| Single GA seed produces a sample-of-1 result | Acknowledged | Medium | Explicitly noted in `task_description.md` as a deliberate budget trade-off; multi-seed confirmation queued as a follow-up suggestion if t0106 finds joint-pass cells |

* * *

## Verification Criteria

Each criterion names the exact command and the expected output.

* **Plan verificator passes.** Command:
  `uv run python -u -m arf.scripts.verificators.verify_plan t0106_long_pdnd_nsga2_300gen`. Expected:
  0 errors. Warnings allowed only if reasoned in this plan.
* **Smoke gate passed before provisioning (REQ-7).** Command:
  `cat tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/008_implementation/smoke_gate.json`. Expected:
  JSON object with 5 keys all `"passed": true`. If any `false`, the implementation agent must NOT
  have provisioned the Vast.ai instance; an intervention file must exist.
* **HV trace well-formed (REQ-4).** Command:
  `python -c "import json,sys; [json.loads(l) for l in open(sys.argv[1])]" tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/008_implementation/hv_trace.jsonl`.
  Expected: exits 0; line count equals `n_gen_completed`; every line contains `gen`, `wall_clock_s`,
  `hv`, `n_cells_evaluated`.
* **Predictions asset exists and matches expected cardinality (REQ-11).** Command:
  `uv run python -u -m arf.scripts.aggregators.aggregate_predictions --ids nsga2-seed44-bedb-morph-2dir-300gen --format json`.
  Expected: one record with `n_predictions = 96 * (1 + n_gen_completed)`.
* **Answer asset stub exists (REQ-12).** Command:
  `ls tasks/t0106_long_pdnd_nsga2_300gen/assets/answer/long-300gen-pdnd-recovery/`. Expected:
  `details.json` and an answer markdown file present.
* **Vast.ai instance destroyed (REQ-8 teardown half).** Command:
  `uv run python -u -m arf.scripts.verificators.verify_machines_destroyed t0106_long_pdnd_nsga2_300gen`.
  Expected: 0 errors; `destroyed: true` in `machine_log.json`.
* **Cost cap respected (REQ-8 spend half).** Command:
  `cat tasks/t0106_long_pdnd_nsga2_300gen/results/costs.json | python -c "import sys,json; d=json.load(sys.stdin); assert d['total_usd'] <= 25.0; print('cost ok:', d['total_usd'])"`.
  Expected: total spend <= 25.00.
* **Metrics include the registered direction_selectivity_index (REQ-15).** Command:
  `cat tasks/t0106_long_pdnd_nsga2_300gen/results/metrics.json | python -c "import sys,json; d=json.load(sys.stdin); assert 'direction_selectivity_index' in d"`.
  Expected: key present with a float value in [0.0, 1.0].
* **All operator-stop and pool-restart hooks present (REQ-5, REQ-6).** Command:
  `grep -c "OperatorStopTermination\|PerGenerationPoolRestart\|_POOL_RESTART_EVERY" tasks/t0106_long_pdnd_nsga2_300gen/code/nsga2_driver.py`.
  Expected: >= 3.
* **REQ coverage in implementation outputs.** Command:
  `grep -c "REQ-" tasks/t0106_long_pdnd_nsga2_300gen/code/*.py tasks/t0106_long_pdnd_nsga2_300gen/logs/steps/008_implementation/*`.
  Expected: every REQ-1 through REQ-15 referenced at least once across the implementation outputs.

* * *

## Alternative Approaches Considered

Documented inline in the Approach section above for traceability:

1. `Callback` with `force_termination` for operator stop — rejected; competes with the existing
   `TerminationCollection`.
2. Manual ask-tell loop — rejected; loses t0104's `_DriverState` infrastructure.
3. Multi-seed at fewer gens — rejected as confounding the H2 test; queued as follow-up if t0106
   finds joint-pass cells.
4. CMAES instead of NSGA-II — rejected as a confounded change; queued as a follow-up suggestion.
