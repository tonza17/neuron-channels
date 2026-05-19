---
spec_version: "2"
task_id: "t0112_t0106_seed77_replicate"
date_completed: "2026-05-19"
status: "complete"
---
# Plan: Seed-77 Minimum-Change Replicate of t0106 Long 2-Direction NSGA-II

## Objective

Re-run the t0106 long 2-direction NSGA-II run on the identical 68-d Bed B electrophys + 14-d
morphology substrate using a single new GA seed (77 instead of 44) with a tightened multiprocessing
pool-restart cadence (10 generations instead of 25) and a lowered generation ceiling (`N_GEN = 60`
instead of 300, HV-plateau operator-stop preserved verbatim). The goal is to test whether t0106's
joint-pass breakthrough (123 unique cells with ratio DSI >= 0.5 AND PD-rate >= 30 Hz across 3,744
evaluations) is a substrate property or a property of GA seed 44. **Done** means: (1) the seed-77
NSGA-II run completes on a single Vast.ai CPU instance under the $25 hard cost cap; (2) a single
predictions asset `t0112-bedb-morph-nsga2-seed77` is produced under `assets/predictions/`, mirroring
t0106's schema and containing all evaluated cells; (3) `results/metrics.json` records the registered
`direction_selectivity_index` metric plus operational metrics (joint-pass count,
n_cells_evaluated_total, hv_plateau_gen); (4) the 5 task-specified charts are saved to
`results/images/`. The replicate is meaningful regardless of outcome — seed 77 finding >= 40 joint-
pass cells confirms substrate populated; finding 0 confirms t0106 was seed-specific.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0112_t0106_seed77_replicate/task.json` and the resolved long
description at `tasks/t0112_t0106_seed77_replicate/task_description.md`:

```text
Name: Seed-77 minimum-change replicate of t0106 long 2-direction NSGA-II

Short description: Re-run t0106 with GA seed 77 and pool-restart-every=10 to test whether
the joint-pass breakthrough is seed-specific or substrate-general.

Dependencies: t0106_long_pdnd_nsga2_300gen.
Expected assets: 1 predictions.
Task types: experiment-run.

Long description (excerpts):
* In scope: identical substrate (Bed B 54-d electrophys + 14-d morphology = 68 free params),
  identical objectives (2-direction ratio DSI + PD-rate at 0 deg), identical NSGA-II
  hyperparameters (pop=96, SBX/PM, HV-plateau operator-stop), identical evaluation protocol
  (N_EVAL_SEEDS=3, ratio DSI, silence guard active).
* In scope, changed: GA seed (44 -> 77), pool-restart cadence (25 -> 10 gens), gen ceiling
  (300 -> 60, HV-plateau stop primary).
* Out of scope: any change to substrate, objective formulation, evaluation protocol, silence
  guard, or NSGA-II driver beyond the seed + pool-restart + N_GEN constants.
* Fork t0106 code into tasks/t0112_t0106_seed77_replicate/code/; copy nsga2_driver.py,
  constants.py, random_init.py, helper modules. Update package imports.
* Patch two constants: constants.py (T0106_SEEDS = (44,) -> T0112_SEEDS = (77,)) and
  nsga2_driver.py:97 (_POOL_RESTART_EVERY = 25 -> 10). Plus N_GEN = 60 in
  constants_morphology.py.
* Smoke gate locally (5 checks identical to t0106): single-eval driver run, ratio DSI
  synthetic sanity, silence-guard unit tests, pool-restart sanity, watchdog wiring.
* Provision remote Vast.ai single instance (same class as t0106).
* Cost cap: $25 per-task hard cap; $20 per-instance watchdog via
  make_watchdog_from_machine_log.
* Collect 1 predictions asset under assets/predictions/t0112-bedb-morph-nsga2-seed77/
  containing per-cell DSI / PD-rate / generation table for all evaluated cells, mirroring
  t0106's predictions asset schema.
* 5 charts (pareto_front_seed44_vs_seed77, hv_vs_gen_seed44_vs_seed77,
  joint_pass_yield_per_gen, top50_morphologies_seed77, asymmetry_distribution_seed44_vs_seed77).
* 2 tables (joint_pass_summary.csv, pareto_front_overlap.csv) in results/data/.
* Registered metrics: direction_selectivity_index (variant best_legit, plus DSI=1.0 count);
  pd_rate_hz (best PD-rate at_best_dsi and at_pareto_corner).
* Key questions answered in results_summary.md: (1) does seed 77 produce >= 40 unique
  joint-pass cells? (2) best ratio DSI >= 0.95? (3) best PD-rate >= 100 Hz? (4) do the two
  seeds' Pareto fronts overlap in parameter space? (5) did tighter pool-restart cadence
  materially change HV trajectory or wall-clock?
```

Concrete requirements decomposed (each item names the step that satisfies it and the evidence that
proves completion):

* **REQ-1** — **Verbatim t0106 code fork.** Copy every algorithm-critical Python module from
  `tasks/t0106_long_pdnd_nsga2_300gen/code/` into `tasks/t0112_t0106_seed77_replicate/code/` with a
  global package-path rewrite (`tasks.t0106_long_pdnd_nsga2_300gen` ->
  `tasks.t0112_t0106_seed77_replicate`). Satisfied by step 1 (copy) and step 2 (import rewrite).
  Evidence: `grep -r "t0106_long_pdnd_nsga2_300gen" tasks/t0112_t0106_seed77_replicate/code/`
  returns zero matches; `ls tasks/t0112_t0106_seed77_replicate/code/*.py | wc -l` matches the t0106
  algorithm-critical file count (>= 22 modules).

* **REQ-2** — **GA seed change 44 -> 77.** `constants.py` declares
  `T0112_SEEDS: tuple[int, ...] = (77,)` (renamed from `T0106_SEEDS = (44,)`); the backwards-compat
  aliases (`T0104_SEEDS`, etc.) are updated to reference `T0112_SEEDS`. Satisfied by step 3.
  Evidence: `grep -n "T0112_SEEDS: tuple" tasks/t0112_t0106_seed77_replicate/code/constants.py`
  returns one line containing `(77,)`.

* **REQ-3** — **Pool-restart cadence 25 -> 10.** `nsga2_driver.py:97` declares
  `_POOL_RESTART_EVERY: int = 10` (was 25). Satisfied by step 3. Evidence:
  `grep -n "_POOL_RESTART_EVERY: int = 10" tasks/t0112_t0106_seed77_replicate/code/nsga2_driver.py`
  returns one line; `results/data/algorithm_config.json` (written by `_save_algorithm_config`)
  contains `"pool_restart_every": 10`.

* **REQ-4** — **Generation ceiling 300 -> 60.** `constants_morphology.py` declares `N_GEN: int = 60`
  (was 300). The HV-plateau constants (`HV_PLATEAU_WINDOW`, `HV_PLATEAU_MIN_HV_HISTORY`,
  `HV_PLATEAU_REL_THRESHOLD`) are NOT changed — HV-plateau stop remains primary. Satisfied by step
  3\. Evidence:
  `grep -n "N_GEN: int = 60" tasks/t0112_t0106_seed77_replicate/code/constants_morphology.py`
  returns one line; HV-plateau constants match t0106 verbatim
  (`diff tasks/t0106_long_pdnd_nsga2_300gen/code/constants_morphology.py tasks/t0112_t0106_seed77_replicate/code/constants_morphology.py`
  shows only the `N_GEN` line differs).

* **REQ-5** — **No other algorithm changes.** No edits to `evaluator.py`, `apply_params.py`,
  `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`, `recorder.py`,
  `trial_helpers.py`, `generator_wrapper.py`, `hv_plateau_watchdog.py`, `cost_watchdog.py`,
  `bootstrap.py`, the silence guard, the SBX/PM operators, the LHS init sampler, the dill checkpoint
  cadence, the operator-stop polling, or the predictions asset writer beyond the package-path
  rewrite. Satisfied by step 1 (verbatim copy) and step 2 (rewrite only). Evidence: after the
  package-path rewrite, every line outside the three patched files matches t0106 byte-for-byte
  (`diff -r tasks/t0106_long_pdnd_nsga2_300gen/code/ tasks/t0112_t0106_seed77_replicate/code/ | grep -v "t0106_long_pdnd_nsga2_300gen\|t0112_t0106 _seed77_replicate"`
  returns only the 3 expected constant lines).

* **REQ-6** — **5-check local smoke gate passes before remote provisioning.** Run `smoke_gate.py`
  and the silence-guard pytest before provisioning. All 5 checks must pass: (1) single-eval driver
  run completes with DSI in `[0, 1]` and PD-rate in `[0, 200] Hz`; (2) ratio DSI synthetic sanity
  (PD=5, ND=1 -> 0.6667 +/- 1e-6); (3) silence-guard unit tests pass; (4) pool-restart sanity
  (driver imports, `_POOL_RESTART_EVERY = 10` reads correctly); (5) watchdog wiring
  (`make_watchdog_from_machine_log` returns a `CostWatchdog` with `hard_budget_usd = 25.00`).
  Satisfied by step 6. Evidence: `logs/steps/<step_id>/smoke_gate.json` (or stdout) reports all 5
  checks `passed: true`. If any check fails, step 7 (provisioning) MUST NOT proceed; an intervention
  file must be created.

* **REQ-7** — **Vast.ai provisioning matches t0106 class.** A single Vast.ai CPU instance is
  provisioned with the same filter class as t0106 (EPYC class CPU, e.g. 7B13/7763; >= 100 GB RAM;
  RTX 3060 Ti or equivalent idle GPU; reliability >= 0.99; dph <= 0.40; EPYC family post-filter).
  Satisfied by step 7. Evidence: `logs/steps/<step_id>_setup-machines/machine_log.json` records the
  selected offer; the `cpu_name` field contains "EPYC".

* **REQ-8** — **Cost watchdog wired correctly with $25 hard cap.** The driver's call site for
  `make_watchdog_from_machine_log` passes `T0112_HARD_BUDGET_USD = 25.00`, NOT the legacy
  `T0104_HARD_BUDGET_USD = 4.00` default that lives in `cost_watchdog.py`. Per-instance watchdog is
  $20. Satisfied by step 3 (constant declaration) and step 8 (driver invocation). Evidence:
  `grep -n "T0112_HARD_BUDGET_USD" tasks/t0112_t0106_seed77_replicate/code/constants.py` shows the
  value `25.00`; `results/data/algorithm_config.json` `"hard_budget_usd"` equals `25.00`;
  `results/costs.json` `total_usd <= 25.00`.

* **REQ-9** — **MOD library compiles on the Vast.ai instance.** 13 `.mod` files from
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` plus the t0024 vendored MODs are SCP'd
  to the instance and compiled with `nrnivmodl`, producing `x86_64/.libs/libnrnmech.so`. Satisfied
  by step 7. Evidence: `logs/steps/<step_id>_setup-machines/mod_compile.log` shows `nrnivmodl` exit
  0 and a non-empty `libnrnmech.so` listing.

* **REQ-10** — **NSGA-II run terminates correctly.** The run terminates either at the HV-plateau
  stop (primary), at `N_GEN = 60` (hard ceiling), at the $25 cost watchdog, or via the operator-stop
  file `intervention/stop.md`. Satisfied by step 8. Evidence: `results/data/termination_reason.json`
  (or equivalent log) names the trigger; `logs/steps/<step_id>_implementation/hv_trace.jsonl` line
  count <= 60.

* **REQ-11** — **Predictions asset format matches t0106 exactly.** Asset folder is named
  `assets/predictions/t0112-bedb-morph-nsga2-seed77/`. `details.json` has `spec_version: "2"`, same
  five per-cell schema fields as t0106 (`generation`, `vector_68d`, `objective_F_minimised`,
  `dsi_vector_sum` (note: stores ratio DSI; field name kept for back-compat with t0102/t0104
  downstream tooling), `pd_rate_hz`), same categories (`direction-selectivity`,
  `compartmental-modeling`, `retinal-ganglion-cell`), same gzipped-JSON file format
  (`files/all_evaluations_seed77.json.gz`). `instance_count = 96 x (1 + n_gen_completed)`. Required
  `metrics_at_creation` keys: `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`,
  `best_pd_rate_hz`, `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`,
  `final_cost_usd`. Satisfied by step 9. Evidence:
  `uv run python -u -m arf.scripts.aggregators.aggregate_predictions --ids t0112-bedb-morph-nsga2-seed77 --format json`
  returns one record with the correct `instance_count`; the verificator passes.

* **REQ-12** — **Registered metrics written to `results/metrics.json`.** The registered
  `direction_selectivity_index` metric is reported using the explicit multi-variant metrics format
  (this task compares one condition but follows the same shape as t0106 for cross-task
  comparability) with variants `best_legit` (highest non-DSI=1.0 cell) and a count of DSI=1.0 cells.
  Plus operational metrics: `joint_pass_count`, `best_pd_rate_hz`, `n_cells_evaluated`,
  `hv_plateau_gen`, `n_gen_completed`, `efficiency_inference_time_per_item_seconds`,
  `efficiency_inference_cost_per_item_usd`. `pd_rate_hz` is NOT a registered project metric (only
  `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse` exist in `meta/metrics/`); it is reported as an operational metric only.
  Satisfied by step 9. Evidence:
  `cat results/metrics.json | python -c "import sys,json; d=json.load(sys.stdin); print(list(d['variants'][0]['metrics']))"`
  lists `direction_selectivity_index` and the operational keys.

* **REQ-13** — **5 charts produced in `results/images/`.** Per `task_description.md`: (a)
  `pareto_front_seed44_vs_seed77.png`, (b) `hv_vs_gen_seed44_vs_seed77.png`, (c)
  `joint_pass_yield_per_gen.png`, (d) `top50_morphologies_seed77.png`, (e)
  `asymmetry_distribution_seed44_vs_seed77.png`. All saved as PNG. Satisfied by step 10. Evidence:
  `ls tasks/t0112_t0106_seed77_replicate/results/images/*.png | wc -l >= 5`.

* **REQ-14** — **2 summary tables produced in `results/data/`.** Per `task_description.md`: (a)
  `joint_pass_summary.csv` (per-seed totals: evals, joint-pass count, joint-pass %, best DSI, best
  PD-rate, plateau gen); (b) `pareto_front_overlap.csv` (parameter-space nearest- neighbour distance
  between each t0112 Pareto cell and its closest t0106 Pareto cell). Satisfied by step 10. Evidence:
  both CSV files exist and parse as DataFrames with the expected columns.

* **REQ-15** — **Vast.ai instance destroyed within 5 min of last completed gen or operator-stop.**
  Satisfied by step 11. Evidence: `verify_machines_destroyed t0112_t0106_seed77_replicate` returns 0
  errors; `machine_log.json` `destroyed: true` and `destroyed_at` timestamp <= 5 min after the last
  `hv_trace.jsonl` line.

* * *

## Approach

**Task type recommended**: `experiment-run` (matches `task.json` `task_types: ["experiment-run"]`).
The Planning Guidelines from `meta/task_types/experiment-run/instruction.md` drive the design: fixed
seeds (77), per-condition metrics breakdown in explicit multi-variant `metrics.json`, explicit
validation gate (5-step local smoke gate before any Vast.ai provisioning), cost tracking against the
$25 hard cap (per-task default $8 explicitly overridden by the task brief), charts saved to
`results/images/`, predictions asset under `assets/predictions/`. Reproducibility: seed 77 is the
only stochastic input; the NSGA-II run is deterministic given the seed.

**Technical approach (grounded in `research_code.md` findings).** The entire delta between t0106 and
t0112 lives in three lines across three files. Per `research_code.md` finding "The Patch Surface Is
Exactly Two Constants, Plus One Generation Ceiling":

1. **GA seed 44 -> 77.** `constants.py` line 58: `T0106_SEEDS: tuple[int, ...] = (44,)` ->
   `T0112_SEEDS: tuple[int, ...] = (77,)`. Consumed by `random_init.main()` and by
   `run_three_seeds.sh` (renamed to `run_seed77.sh`).
2. **Pool restart cadence 25 -> 10.** `nsga2_driver.py:97`: `_POOL_RESTART_EVERY: int = 25` ->
   `_POOL_RESTART_EVERY: int = 10`. The constant threads through
   `PerGenerationPoolRestart.__init__(restart_every=_POOL_RESTART_EVERY)` (line 357) and is
   serialised by `_save_algorithm_config` (line 442) into `algorithm_config.json` as
   `"pool_restart_every"` — the new value propagates end-to-end automatically.
3. **Gen ceiling 300 -> 60.** `constants_morphology.py`: `N_GEN: int = 300` -> `N_GEN: int = 60`.
   HV-plateau constants (`HV_PLATEAU_WINDOW`, `HV_PLATEAU_MIN_HV_HISTORY`,
   `HV_PLATEAU_REL_THRESHOLD`) stay at t0106 values so the stopping criterion is identical;
   `N_GEN = 60` is a hard ceiling only.

The cross-task import rule (per `arf/specifications/research_code_specification.md`'s
`Cross-Task Code Reuse Rule`) forbids `tasks.t0106_long_pdnd_nsga2_300gen.code` imports. Per
`research_code.md` finding "The Cross-Task Import Rule Forces a Copy of t0106's Code", the
established pattern is verbatim copy with a global `sed` rewrite:
`tasks.t0106_long_pdnd_nsga2_300gen` -> `tasks.t0112_t0106_seed77_replicate`. Upstream task imports
(`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`, `tasks.t0092_*`) stay valid unchanged — the
verificator allows full-path imports of UPSTREAM tasks.

**Predictions asset schema.** Per `research_code.md` finding "The Predictions Asset Schema Is
Already Defined and Must Be Mirrored Exactly": t0106's
`assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/details.json` defines `spec_version: "2"`
with per-cell schema fields `generation`, `vector_68d`, `objective_F_minimised`, `dsi_vector_sum`
(stores ratio DSI; name preserved for back-compat with t0102/t0104), `pd_rate_hz`. File format is
gzipped JSON (`.json.gz`). t0112 mirrors this exactly with folder name
`t0112-bedb-morph-nsga2-seed77` (task-brief-specified) and file
`files/all_evaluations_seed77.json.gz`.

**Cost watchdog.** Per `research_code.md` finding "The Cost Watchdog Library Is
`make_watchdog_from_machine_log`, Not a Registered Library": the factory is a module-level function
in `tasks/t0106_*/code/cost_watchdog.py:102`. The legacy `T0104_HARD_BUDGET_USD = 4.00` default in
`cost_watchdog.py:27` MUST be overridden at the driver call site to `T0112_HARD_BUDGET_USD = 25.00`.
Per-instance watchdog: $20.

**Alternatives considered**:

* **Run two or three new seeds at fewer gens (e.g., 3 seeds x 25 gens).** Rejected because (a) the
  task brief explicitly says "single-seed replicate" and (b) the H1 hypothesis (joint-pass recovery
  is substrate-general) is tested most cleanly by reproducing t0106's full pop x gens budget on one
  seed; multi-seed at fewer gens would confound the test. Queued as a follow-up if seed 77 yields a
  partial replication (10-39 joint-pass cells).
* **Run seed 77 with t0106's exact `_POOL_RESTART_EVERY = 25`.** Rejected per `research_code.md`
  finding "NEURON Memory Creep Motivates the Pool-Restart Tightening" — t0106 wall-clock telemetry
  shows growing per-eval memory footprint between restarts. The proposed cadence of 10 gens (6
  restarts in a 60-gen run instead of 2) costs ~2 minutes wall-clock for a ~3-hour run, well under
  1%. The change is operationally direct, not a confound.
* **Run seed 77 at `N_GEN = 300` like t0106.** Rejected because the project budget envelope ($18.20
  remaining of $75) is tight; t0106 plateaued at gen 40 of 300 so 300-gen is empirically not needed.
  `N_GEN = 60` is a 50% safety margin above t0106's empirical plateau gen with HV-plateau stop as
  the primary trigger.
* **Change the silence guard or DSI metric.** Rejected explicitly — the task brief calls it "out of
  scope" because any evaluator change would break the like-for-like comparison.
* **Re-evaluate t0106 cells at 8 directions instead of running a new seed.** Rejected — out of scope
  per the brief. The 8-direction re-evaluation is what t0107 already did on 10 random t0106 cells;
  this t0112 task is the replicate, not the polar re-check.

**Validation gate**: the 5-check local smoke gate (single-eval driver, ratio DSI synthetic sanity,
silence-guard unit tests, pool-restart sanity, watchdog wiring) is the only gate between local fork
and the $20-25 Vast.ai spend. All 5 checks must pass; if any fails, an intervention file is created
and provisioning halted.

**Baseline comparison**: t0106 seed-44 results (123 unique joint-pass cells, best ratio DSI =
1.0000, best PD-rate = 122.62 Hz, final HV = 122.0288, final cost $10.37, 40 gens completed of 300).
t0112 results are compared against these in `joint_pass_summary.csv` and the 5 charts.

* * *

## Cost Estimation

* **Vast.ai single CPU instance (EPYC class, RTX 3060 Ti idle)**: expected hourly rate ~$0.24-0.36/h
  (t0106 selected at $0.24/h on an EPYC 7B13 64-core Norway instance). Expected wall-clock 3-4 h for
  60-gen run (t0106 ran 40 gens in ~3 h at the same pop/n_eval_seeds). Productive compute:
  ~$0.96-1.44.
* **Setup + MOD compilation + idle**: ~30 min at $0.36/h = **$0.18**.
* **Conservative buffer for retries / post-run download**: **$2.00**.
* **No LLM API costs** — all NSGA-II logic runs locally on the Vast.ai instance with no external API
  calls.
* **Estimated total**: **$3-12 expected**, **$25 hard cap** (per-instance watchdog $20 inside
  `CostWatchdogTermination`; $25 orchestrator-level ceiling).
* **t0106 precedent**: actual spend $10.37 at the same pop/n_eval_seeds budget for 40 gens; t0112 is
  designed for 60 gens with HV-plateau stop primary, so most-likely spend is ~$10-11.
* **Project budget context**: $75 total budget; $56.80 already spent; $18.20 remaining. Expected
  post-task reserve: ~$7-8. If the run plateaus early (gen 20-30), spend drops to ~$5 and post-task
  reserve is ~$13.
* **Per-task default limit override**: the per-task default in `project/budget.json` is $8; this
  task explicitly overrides to $25 (declared in `task_description.md`'s "Compute and Budget"
  section). The override is honoured by passing `T0112_HARD_BUDGET_USD = 25.00` into
  `make_watchdog_from_machine_log` at the driver call site.

* * *

## Step by Step

Implementation work only. Orchestrator-managed steps (results writing, suggestions,
compare-literature, reporting) are not in this list per the plan specification.

### Milestone 1: Local Code Fork + Smoke Gate (steps 1-6)

1. **Copy t0106 `code/` verbatim into `tasks/t0112_t0106_seed77_replicate/code/`.** Source:
   `tasks/t0106_long_pdnd_nsga2_300gen/code/` (entire directory, 34 `.py` files plus
   `run_three_seeds.sh`, ~8,117 lines). Copy every `.py` file plus the orchestration shell script.
   Inputs: t0106 code directory. Outputs: `tasks/t0112_t0106_seed77_replicate/code/` mirror with
   identical structure. Expected observable output: file count matches t0106
   (`ls tasks/t0112_*/code/*.py | wc -l == ls tasks/t0106_*/code/*.py | wc -l`). **Satisfies REQ-1
   (groundwork), REQ-5.**

2. **Rewrite package import paths.** In every copied `.py` and `.sh` file, replace
   `tasks.t0106_long_pdnd_nsga2_300gen` with `tasks.t0112_t0106_seed77_replicate`. Use a single
   `sed -i 's/t0106_long_pdnd_nsga2_300gen/t0112_t0106_seed77_replicate/g'` across all files (or
   PowerShell `-replace`). Do NOT touch upstream task references (`t0024`, `t0080`, `t0090`,
   `t0092`, `t0093`) — those are valid as full-path imports of UPSTREAM tasks. Inputs: step 1
   output. Outputs: identical structure with corrected imports. Expected output:
   `grep -r "t0106_long_pdnd_nsga2_300gen" tasks/t0112_t0106_seed77_replicate/code/` returns zero
   matches;
   `grep -r "tasks.t0024_\|tasks.t0080_\|tasks.t0090_\|tasks.t0092_" tasks/t0112_t0106_seed77_replicate/code/`
   still returns the expected upstream imports unchanged. **Satisfies REQ-1, REQ-5.**

3. **Apply the three constant patches (the entire algorithmic delta).** Edit per the
   `research_code.md` patch table:

   * **`code/constants.py`**: rename `T0106_SEEDS: tuple[int, ...] = (44,)` to
     `T0112_SEEDS: tuple[int, ...] = (77,)`. Rename `T0106_HARD_BUDGET_USD` to
     `T0112_HARD_BUDGET_USD` and keep the value `= 25.00`. Update the backwards-compat aliases
     (`T0104_SEEDS`, `T0104_HARD_BUDGET_PER_SEED_USD`, `T0104_TASK_BUDGET_TOTAL_USD` on lines 65-67
     of `constants.py`) to reference the new `T0112_*` names. Add or confirm
     `T0112_PER_INSTANCE_WATCHDOG_USD = 20.00`.
   * **`code/nsga2_driver.py`** line 97: change `_POOL_RESTART_EVERY: int = 25` to
     `_POOL_RESTART_EVERY: int = 10`. Update the module docstring (lines 13-17) to reflect the new
     cadence. Confirm all `T0106_HARD_BUDGET_USD` references are renamed to `T0112_HARD_BUDGET_USD`.
   * **`code/constants_morphology.py`**: change `N_GEN: int = 300` to `N_GEN: int = 60`. Do NOT
     touch any other constant — in particular `HV_PLATEAU_WINDOW`, `HV_PLATEAU_MIN_HV_HISTORY`,
     `HV_PLATEAU_REL_THRESHOLD`, `N_EVAL_SEEDS`, `N_DIRECTIONS`, `POP_SIZE` all stay at t0106
     values.
   * **`code/random_init.py`**: update the `T0106_SEEDS` import on line 96 (and any other site) to
     `T0112_SEEDS`.
   * **`code/run_three_seeds.sh`**: rename to `run_seed77.sh` and trim to a single seed invocation.
     Remove the post-seed-44 budget gate block (it has no meaning at one seed).

   Inputs: step 2 output. Outputs: patched constants and orchestrator script. Expected output:
   `grep -n "T0112_SEEDS: tuple\[int, ...\] = (77,)" tasks/t0112_t0106_seed77_replicate/code/constants.py`
   returns one line;
   `grep -n "_POOL_RESTART_EVERY: int = 10" tasks/t0112_t0106_seed77_replicate/code/nsga2_driver.py`
   returns one line;
   `grep -n "N_GEN: int = 60" tasks/t0112_t0106_seed77_replicate/code/constants_morphology.py`
   returns one line. **Satisfies REQ-2, REQ-3, REQ-4, REQ-8 (constant declaration half).**

4. **Verify the diff is exactly the three intended changes.** Run
   `diff -r tasks/t0106_long_pdnd_nsga2_300gen/code/ tasks/t0112_t0106_seed77_replicate/code/ | grep -v "t0106_long_pdnd_nsga2_300gen\|t0112_t0106 _seed77_replicate"`
   and confirm the output contains ONLY the three patched lines plus any incidental whitespace from
   the constant renames. If unexpected diffs appear, fix them before proceeding. Inputs: step 3
   output. Outputs: a diff log confirming a tight delta. Expected output: the diff contains the 3
   expected algorithm lines (plus the `T0106_*` -> `T0112_*` variable renames in `constants.py` and
   references to them). **Satisfies REQ-5 (verification).**

5. **Sanity-import the code package.** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0112_t0106_seed77_replicate -- uv run python -c "import tasks.t0112_t0106_seed77_replicate.code.constants; import tasks.t0112_t0106_seed77_replicate.code.constants_morphology; import tasks.t0112_t0106_seed77_replicate.code.nsga2_driver; import tasks.t0112_t0106_seed77_replicate.code.evaluator; print('imports ok')"`.
   Expected: prints `imports ok` and exits 0. If any ImportError, halt and fix package paths.
   **Satisfies REQ-1, REQ-5 (importability gate).**

6. **[CRITICAL] Run the 5-check local smoke gate (validation gate before remote provisioning).**
   This is the explicit validation gate per the experiment-run task type Planning Guidelines.

   * **Baseline reference**: t0106 seed-44 single-cell evaluation in the smoke gate returned DSI in
     `[0, 1]` and PD-rate in `[0, 200] Hz`. t0112's smoke gate single-eval must land in the same
     ranges — these are sanity bounds, not the operating point.
   * Run
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0112_t0106_seed77_replicate -- uv run python -u -m tasks.t0112_t0106_seed77_replicate.code.smoke_gate`.
     Expected: 5 sub- checks all green within 5 min wall-clock total. The 5 checks per
     `task_description.md` are: (1) single-eval driver run completes (DSI in `[0, 1]`, PD-rate in
     `[0, 200] Hz`); (2) ratio DSI synthetic sanity (PD=5, ND=1 -> 0.6667 +/- 1e-6); (3)
     silence-guard unit tests pass (`SILENCE_SPIKE_COUNT_THRESHOLD = 10` clamps DSI to 0 on a
     degenerate silent case); (4) pool-restart sanity (`_POOL_RESTART_EVERY = 10` reads correctly
     from the driver module); (5) watchdog wiring (`make_watchdog_from_machine_log` returns
     `CostWatchdog` with `hard_budget_usd = 25.00`).
   * Run
     `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0112_t0106_seed77_replicate -- uv run python -u -m pytest tasks/t0112_t0106_seed77_replicate/code/test_evaluator_dsi_guard.py -v`.
     Expected: 0 failures.
   * **Validation failure condition**: if any of the 5 smoke-gate checks fail OR the unit-test suite
     reports any failure, halt — do NOT proceed to step 7 (Vast.ai provisioning). Create
     `intervention/smoke_gate_failed.md` with the specific failure and STOP.
   * **Individual-output inspection**: after the smoke gate passes, read at least 5 individual
     cell-evaluation outputs from the smoke-gate stdout (DSI, PD-rate, ND-rate, total spike count
     per anchor cell). Verify each value is in the expected range and the silence-guard zeros out
     DSI on the degenerate cases. Document this inspection in the step log.

   Inputs: step 5 output. Outputs: `logs/steps/<step_id>_implementation/smoke_gate.json` (or
   equivalent) with all five checks `passed: true`. **Satisfies REQ-6.**

### Milestone 2: Remote Provisioning + Run (steps 7-8)

7. **Provision the Vast.ai instance and compile MODs.** Run the `setup-remote-machine` skill via the
   orchestrator. Filters per `task_description.md` "Compute and Budget" section and t0106 precedent:
   EPYC class CPU (AMD EPYC 7B13 or equivalent), >= 100 GB RAM, RTX 3060 Ti or equivalent GPU (idle
   — workload is CPU-only NEURON), reliability >= 0.99, dph <= 0.40, post-filter for EPYC family
   (string match `cpu_name LIKE '%EPYC%'`). Record
   `logs/steps/<step_id>_setup-machines/offer_filters.json` and `machine_log.json`.

   * Install NEURON 8.2.7, NetPyNE 1.1.1, pymoo, dill, numpy, scipy via `uv sync` on the instance.
   * SCP 13 `.mod` files from `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` plus
     `mod_func.c` to the instance at the same relative path. The list (per `research_code.md`):
     `bkt80.mod`, `calt80.mod`, `catt80.mod`, `iht80.mod`, `kdrt80.mod`, `kv3t80.mod`, `kv4t80.mod`,
     `kv7t80.mod`, `napt80.mod`, `nart80.mod`, `nav16t80.mod`, `skahpt80.mod`, `skt80.mod`. Also SCP
     the t0024 vendored MOD sources at
     `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/`.
   * Run `nrnivmodl` in the `mods/` directory to produce `x86_64/.libs/libnrnmech.so`. Verify with
     `ls -la x86_64/.libs/libnrnmech.so` (file exists, non-zero size). The t0024 compile is handled
     at runtime by `bootstrap.py:_compile_t0024_mods_linux`.

   Inputs: step 6 pass. Outputs: provisioned Vast.ai instance with NEURON, MODs, and t0112 code.
   **Satisfies REQ-7, REQ-9.**

8. **[CRITICAL] Launch the NSGA-II run (the load-bearing step).** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0112_t0106_seed77_replicate -- uv run python -u -m tasks.t0112_t0106_seed77_replicate.code.nsga2_driver --seed 77 --teardown-on-watchdog`.
   The driver:

   * Initialises pop = 96 random LHS, `n_eval_seeds = 3`, `n_directions = 2`, seed 77.

   * Runs the `TerminationCollection`: `MaximumGenerationTermination(n_max_gen=60)`,
     `HVPlateauTermination(...)` (HV-plateau stop, primary trigger; constants identical to t0106),
     `CostWatchdogTermination(watchdog=$25)`, `OperatorStopTermination(stop_signal_md())`.

   * `_GenerationCallback` writes one JSON line per gen to
     `logs/steps/<step_id>_implementation/hv_trace.jsonl` (fields `gen`, `wall_clock_s`, `hv`,
     `n_cells_evaluated`) and dill-checkpoints the algorithm to `checkpoint_gen<NNNN>.pkl`.

   * `PerGenerationPoolRestart` (instantiated with `restart_every = _POOL_RESTART_EVERY = 10`)
     closes and recreates the `multiprocessing.Pool` every 10 gens, swapping
     `problem.elementwise_runner = StarmapParallelization(pool.starmap)`. At `N_GEN = 60`, this
     yields up to 6 restarts (vs 2 in t0106's 40 completed gens at `_POOL_RESTART_EVERY = 25`).

   * `_save_algorithm_config` writes `results/data/algorithm_config.json` with
     `pool_restart_every: 10`, `hard_budget_usd: 25.00`, `task_seed: 77`.

   * **Validation gate (after gen 1)**: pull `hv_trace.jsonl` from the remote instance and verify
     exactly 1 well-formed JSON line with the 4 required fields. If the file is empty or malformed,
     halt and debug — do not let the run proceed past gen 5.

   * **Per-cell baseline check (after gen 1)**: pull 5 random cells from the predictions log on the
     instance and verify `dsi_ratio in [0, 1]`, `pd_rate >= 0`, `nd_rate >= 0`. **Failure
     condition**: if any cell is out of these ranges, OR if the gen-1 best DSI is above 0.99
     (suspiciously close to the silence-guard ceiling — likely a degenerate-cell artefact), halt and
     read 5 individual cell outputs (DSI, PD-rate, ND-rate, total spike count, parameter vector)
     before letting the run continue.

   * The orchestrator pulls `hv_trace.jsonl` periodically and watches for HV-plateau or operator
     stop. The operator can write `intervention/stop.md` to halt at the next gen boundary.

   Inputs: step 7 provisioning + step 6 smoke-gate pass. Outputs: `hv_trace.jsonl`,
   `checkpoint_gen<NNNN>.pkl` files, per-cell predictions log on the Vast.ai instance. Expected
   runtime: 2-4 h wall-clock at HV-plateau stop (most likely gen 30-50); cost $3-12 actual against
   $25 cap. **Satisfies REQ-2, REQ-3, REQ-4, REQ-8, REQ-10.**

### Milestone 3: Asset Assembly + Teardown (steps 9-11)

9. **Download artefacts and build the predictions asset.** SCP from the Vast.ai instance to the
   worktree:

   * `logs/steps/<step_id>_implementation/hv_trace.jsonl` (the per-gen HV trace).
   * All `checkpoint_gen<NNNN>.pkl` files to `logs/steps/<step_id>_implementation/checkpoints/`.
   * `results/data/algorithm_config.json` (records `pool_restart_every`, `hard_budget_usd`,
     `task_seed`).
   * The per-cell predictions log (every evaluated cell across all completed gens).

   Build the **predictions asset** at
   `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/`:

   * **`details.json`** (`spec_version: "2"`, `predictions_id: "t0112-bedb-morph-nsga2-seed77"`,
     `name: "NSGA-II seed 77 on 68-d Bed B + 14-d morphology, 2 directions, 60-gen replicate of t0106"`,
     `model_id: null`,
     `model_description: "... identical to t0106 except GA seed 44 -> 77, pool_restart_every 25 -> 10, N_GEN 300 -> 60 ..."`,
     `dataset_ids: []`, `prediction_format: "json.gz"`, `prediction_schema: "..."` (copy t0106's
     schema verbatim, swapping `seed44` -> `seed77`), `instance_count = 96 x (1 + n_gen_completed)`,
     `categories: ["direction-selectivity", "compartmental-modeling", "retinal-ganglion-cell"]`,
     `created_by_task: "t0112_t0106_seed77_replicate"`, `date_created` = ISO 8601 date).
   * **`description.md`** per `meta/asset_types/predictions/specification.md`, documenting the three
     constant deltas vs t0106 and the back-compat naming of `dsi_vector_sum` (stores ratio DSI;
     field name kept for t0102/t0104 downstream compatibility).
   * **`files/all_evaluations_seed77.json.gz`** — gzipped JSON with top-level key `evaluations` ->
     list of per-cell records. Each record: `generation`, `vector_68d`, `objective_F_minimised`,
     `dsi_vector_sum`, `pd_rate_hz`. Format identical to t0106's `all_evaluations_seed44.json.gz`.
   * Required `metrics_at_creation` keys: `n_generations_completed`, `n_cells_total`,
     `best_dsi_ratio`, `best_pd_rate_hz`, `n_joint_pass_unique`, `n_joint_pass_evaluations`,
     `final_hypervolume`, `final_cost_usd`.

   Validation: `wc -l` on the unzipped JSONL or equivalent count of records matches
   `96 x (1 + n_gen_completed)`. **Satisfies REQ-11.**

10. **Compute metrics and produce charts.** Write
    `tasks/t0112_t0106_seed77_replicate/results/metrics.json` using the explicit multi-variant
    format (per `arf/specifications/metrics_specification.md` and `experiment-run` task type
    guidance). One variant with `variant_id: "random-init-seed77-2dir-60gen"`, dimensions matching
    t0106's variant shape (`task_seed: 77`, `init_method: "lhs_random"`, `n_obj: 2`,
    `n_directions: 2`, `dsi_metric: "ratio"`, `dsi_silence_guard_active: true`, `n_eval_seeds: 3`,
    `n_generations_target: 60`, `n_generations_completed`, `n_cells`).

    * Registered metric: `direction_selectivity_index` — best ratio DSI across all evaluated cells
      (`max(dsi_ratio)`). Sub-variant `best_legit` = highest non-DSI=1.0 cell; sub-variant
      `dsi_eq_one_count` = number of cells at exactly DSI = 1.0 (these are silence-guard or
      single-spike artefacts per t0106's reporting).
    * Operational metrics (not registered): `joint_pass_count` (cells with
      `dsi_ratio >= 0.5 AND pd_rate_hz >= 30.0`); `best_pd_rate_hz` (mirrors t0106's reported 122.62
      Hz); `n_cells_evaluated_total`; `hv_plateau_gen` (gen at which the 60-min moving-window HV
      improvement first falls below 1%; `null` if not reached); `n_gen_completed`;
      `efficiency_inference_time_per_item_seconds = total_wall_clock_s / n_cells_evaluated_total`;
      `efficiency_inference_cost_per_item_usd = total_cost_usd / n_cells_evaluated_total`.
      Training-time efficiency is explicitly omitted per the style guide because NSGA-II is not
      conventional model training. `pd_rate_hz` is NOT a registered project metric (only
      `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
      `tuning_curve_rmse` are registered); the task brief's "Registered metrics: pd_rate_hz" note is
      treated as an operational metric request, not a registered metric. The omission is deliberate
      and documented here.

    Generate charts to `tasks/t0112_t0106_seed77_replicate/results/images/` per
    `task_description.md`:

    * `pareto_front_seed44_vs_seed77.png` — overlay of t0106 (seed 44) and t0112 (seed 77) strict
      Pareto fronts on DSI vs PD-rate axes; coloured by source task. Read t0106's predictions asset
      at
      `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/ files/all_evaluations_seed44.json.gz`
      for the comparison data.
    * `hv_vs_gen_seed44_vs_seed77.png` — log-scale HV trajectory for both seeds on the same axes,
      with pool-restart events annotated.
    * `joint_pass_yield_per_gen.png` — joint-pass cell count discovered per generation for both
      seeds.
    * `top50_morphologies_seed77.png` — 10x5 grid of best 50 cells (by joint-pass ranking), coloured
      by archetype, matching t0106's `top50_morphologies.png` format.
    * `asymmetry_distribution_seed44_vs_seed77.png` — 4-panel histogram (soma offset, elongation,
      branch density gradient, primary branch PD concentration) for top-50 cells from both seeds.

    Generate tables to `tasks/t0112_t0106_seed77_replicate/results/data/`:

    * `joint_pass_summary.csv` — per-seed (44, 77): total evals, joint-pass count, joint-pass %,
      best DSI, best PD-rate, plateau generation.
    * `pareto_front_overlap.csv` — for each t0112 Pareto cell, the L2 parameter-space distance to
      its closest t0106 Pareto cell; informs whether the two seeds find "the same" or "different"
      frontier solutions.

    Inputs: step 9 outputs + t0106 predictions asset. Outputs: `results/metrics.json`, 5 PNG charts,
    2 CSV tables. **Satisfies REQ-12, REQ-13, REQ-14.**

11. **Teardown the Vast.ai instance.** Run the `setup-remote-machine` skill in teardown mode (or
    call the orchestrator's teardown procedure). Verify destruction within 5 min of the last
    completed gen or operator-stop detection. Update
    `logs/steps/<step_id>_teardown/machine_log.json` with `destroyed: true` and a `destroyed_at`
    timestamp. Inputs: step 10 confirms all artefacts pulled. Outputs: `machine_log.json` with
    `destroyed: true`; Vast.ai dashboard confirms instance gone. **Satisfies REQ-15.**

* * *

## Remote Machines

Single Vast.ai CPU instance required. Filters: EPYC class CPU (AMD EPYC 7B13 or equivalent like
7763), >= 100 GB RAM, RTX 3060 Ti or equivalent GPU (idle — workload is CPU-only NEURON),
reliability >= 0.99, dph (dollars per hour) <= 0.40, post-filter for EPYC family (string match
`cpu_name LIKE '%EPYC%'`, mirroring t0104's and t0106's pattern). Expected hourly rate
~$0.24-0.36/h. Estimated wall-clock: 2-4 h (HV-plateau stop likely at gen 30-50; hard ceiling at gen
60). Cost cap: $25 total ($20 per-instance watchdog enforced inside `CostWatchdogTermination`; $25
orchestrator-level ceiling via `T0112_HARD_BUDGET_USD`). Teardown within 5 min of last completed gen
or `intervention/stop.md` detection. Reference:
`arf/specifications/remote_machines_specification.md`.

* * *

## Assets Needed

* **Code substrate from t0106** (dependency `t0106_long_pdnd_nsga2_300gen`): the entire `code/`
  directory copied verbatim with package-path rewrite, and 3 constant patches per the patch table in
  Approach.
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
* **t0106 predictions asset for comparison charts**:
  `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/ files/all_evaluations_seed44.json.gz`.
  Read-only; used by step 10 to build the side-by-side charts and tables.
* **No external datasets, no new papers, no LLM API access required.**

* * *

## Expected Assets

Matches `task.json` `expected_assets`: `{"predictions": 1}`.

* **1 predictions asset** at
  `tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/` containing
  every evaluated cell across all completed generations of the seed-77 run. Each cell record carries
  the 68-d parameter vector (`vector_68d`), the NSGA-II minimised objective vector
  (`objective_F_minimised = [-ratio_dsi, -pd_rate_hz]`), the ratio DSI (`dsi_vector_sum`; field name
  preserved for t0102/t0104 back-compat), `pd_rate_hz`, and the generation index (`generation`).
  Format: gzipped JSON. Total record count: exactly `96 x (1 + n_gen_completed)`. Required
  `metrics_at_creation` keys per `research_code.md`: `n_generations_completed`, `n_cells_total`,
  `best_dsi_ratio`, `best_pd_rate_hz`, `n_joint_pass_unique`, `n_joint_pass_evaluations`,
  `final_hypervolume`, `final_cost_usd`.

* * *

## Time Estimation

* Research (already complete): research_code only; ~1 h logged in `logs/steps/006_research-code/`.
* Planning (this step): 0.5 h.
* Local code fork + import rewrite + 3 patches (Milestone 1, steps 1-5): **0.5-1 h** (~8,117 lines
  copied, single `sed` rewrite, 3 line-level edits).
* Local smoke gate (Milestone 1, step 6): **0.5 h** (5 checks on Windows including NEURON
  single-cell eval, ~5 min each).
* Vast.ai provisioning + MOD compilation (Milestone 2, step 7): **0.5-1 h**.
* NSGA-II run (step 8): **2-4 h** wall-clock (HV-plateau stop likely at gen 30-50; 60-gen ceiling).
* Asset assembly + metrics + charts (Milestone 3, step 9-10): **1-2 h**.
* Teardown (step 11): **0.1 h**.
* **Total wall-clock envelope: 5-9 h** (matches expected actual cost of $10-11 at the t0106 per-
  hour rate).

* * *

## Risks & Fallbacks

**Pre-mortem**: if t0112 has failed completely at completion time, the most likely failure modes
are: (a) seed 77 yields 0 joint-pass cells (the substrate-is-seed-specific outcome — still
publishable but reframes the headline claim); (b) the pool-restart-every-10 cadence introduces a
race in `PerGenerationPoolRestart` that t0106's restart-every-25 didn't surface (algorithmic
sensitivity to restart cadence); (c) MOD library ABI surprise on the Vast.ai instance (Linux MOD
fails to load despite local smoke gate passing on Windows DLL); (d) operator misses the HV-plateau
window and `N_GEN = 60` ceiling triggers later than expected, blowing wall-clock past 6 h; (e)
`dsi_vector_sum` schema field rename slips into the code (silently breaking back-compat with t0106
analysis modules); (f) HV-plateau threshold is too tight for a 60-gen run and the run never
plateau-stops, requiring operator intervention.

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Seed 77 produces 0 joint-pass cells (substrate is seed-specific) | Medium | Medium (reframes headline but still publishable as negative replication) | Run is short ($3-12 spend); pivot strategy is multi-seed follow-up (suggestion) rather than re-running this task |
| `_POOL_RESTART_EVERY = 10` introduces a race in `PerGenerationPoolRestart` not surfaced at 25 | Low | High (algorithm hangs or crashes) | Smoke-gate check 4 (pool-restart sanity) catches structural issues locally; if the remote run hangs at a restart boundary, the per-gen `dill` checkpoint allows resume from the latest gen with `_POOL_RESTART_EVERY` raised back to 25 |
| Linux MOD ABI mismatch surfaces after Vast.ai launch | Low | High (blocks the run) | Bootstrap step recompiles MODs with `nrnivmodl` on the Vast.ai instance from source; if compilation fails, halt and create intervention file; t0106 already shipped this pattern successfully |
| HV-plateau threshold too tight; run hits `N_GEN = 60` ceiling without plateau | Medium | Low (60 gens is a 50% margin above t0106's empirical plateau at gen 40, so reaching the ceiling without plateau is itself informative) | `N_GEN = 60` is a hard ceiling; cost stays within $25 cap; the plateau-not-reached outcome is logged as `hv_plateau_gen: null` in metrics |
| Operator misses HV-plateau window; wall-clock past 6 h | Low | Medium ($5-10 wasted) | `T0112_HARD_BUDGET_USD = 25.00` cap inside `CostWatchdogTermination`; orchestrator pulls `hv_trace.jsonl` periodically; explicit operator-stop mechanism via `intervention/stop.md` |
| `dsi_vector_sum` field name accidentally renamed to `dsi_ratio` | Low | Medium (breaks cross-task analysis) | Step 4 diff-check explicitly forbids any change beyond the 3 patched lines; `research_code.md` lesson learned documents this field-name preservation |
| Vast.ai preemption mid-run | Low | Medium (loses up to 1 gen progress) | Per-gen `dill` checkpoint enables resume from the latest gen; the JSONL HV trace is append-only |
| t0106 predictions asset comparison fails (file format change) | Low | Low (comparison charts incomplete) | t0106 asset is read-only and immutable per project rules; format is locked at `spec_version: "2"`; if the gzipped JSON fails to decompress, fall back to per-task analysis without the side-by-side chart and document the limitation |

* * *

## Verification Criteria

Each criterion names the exact command and the expected output.

* **Plan verificator passes.** Command:
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0112_t0106_seed77_replicate -- uv run python -u -m arf.scripts.verificators.verify_plan t0112_t0106_seed77_replicate`.
  Expected: 0 errors. Warnings allowed only if reasoned in this plan.

* **The three intended algorithmic changes are present and ONLY those changes (REQ-2, REQ-3, REQ-4,
  REQ-5).** Command:
  `grep -n "T0112_SEEDS: tuple\[int, ...\] = (77,)" tasks/t0112_t0106_seed77_replicate/code/constants.py && grep -n "_POOL_RESTART_EVERY: int = 10" tasks/t0112_t0106_seed77_replicate/code/nsga2_driver.py && grep -n "N_GEN: int = 60" tasks/t0112_t0106_seed77_replicate/code/constants_morphology.py`.
  Expected: three matches, one per file.

* **Smoke gate passed before provisioning (REQ-6).** Command:
  `cat tasks/t0112_t0106_seed77_replicate/logs/steps/*_implementation/smoke_gate.json` (or
  equivalent log). Expected: JSON object with 5 keys all `"passed": true`. If any `false`, the
  implementation agent must NOT have provisioned the Vast.ai instance; an intervention file must
  exist.

* **HV trace well-formed (REQ-10).** Command:
  `uv run python -c "import json,sys; lines=open(sys.argv[1]).readlines(); [json.loads(l) for l in lines]; print('lines:', len(lines))" tasks/t0112_t0106_seed77_replicate/logs/steps/*_implementation/hv_trace.jsonl`.
  Expected: prints a line count <= 60; every line parses as JSON with `gen`, `wall_clock_s`, `hv`,
  `n_cells_evaluated`.

* **Predictions asset exists and matches expected cardinality (REQ-11).** Command:
  `uv run python -u -m arf.scripts.aggregators.aggregate_predictions --ids t0112-bedb-morph-nsga2-seed77 --format json`.
  Expected: one record with `instance_count = 96 * (1 + n_gen_completed)`,
  `predictions_id = "t0112-bedb-morph-nsga2-seed77"`, `categories` containing
  `direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`.

* **Vast.ai instance destroyed (REQ-15).** Command:
  `uv run python -u -m arf.scripts.verificators.verify_machines_destroyed t0112_t0106_seed77_replicate`.
  Expected: 0 errors; `destroyed: true` in `machine_log.json`.

* **Cost cap respected (REQ-8 spend half).** Command:
  `uv run python -c "import sys,json; d=json.load(open(sys.argv[1])); assert d['total_usd'] <= 25.0, f'over cap: {d[\"total_usd\"]}'; print('cost ok:', d['total_usd'])" tasks/t0112_t0106_seed77_replicate/results/costs.json`.
  Expected: total spend <= 25.00.

* **Registered `direction_selectivity_index` metric reported (REQ-12).** Command:
  `uv run python -c "import sys,json; d=json.load(open(sys.argv[1])); vs=d['variants'][0]['metrics']; assert 'direction_selectivity_index' in vs, list(vs); print('dsi:', vs['direction_selectivity_index'])" tasks/t0112_t0106_seed77_replicate/results/metrics.json`.
  Expected: key present with a float value in [0.0, 1.0].

* **5 charts and 2 tables produced (REQ-13, REQ-14).** Command:
  `ls tasks/t0112_t0106_seed77_replicate/results/images/*.png | wc -l && ls tasks/t0112_t0106_seed77_replicate/results/data/*.csv | wc -l`.
  Expected: PNG count >= 5, CSV count >= 2.

* **REQ coverage in implementation outputs.** Command:
  `grep -c "REQ-" tasks/t0112_t0106_seed77_replicate/code/*.py tasks/t0112_t0106_seed77_replicate/logs/steps/*_implementation/*`.
  Expected: every REQ-1 through REQ-15 referenced at least once across the implementation outputs
  (commit messages, step logs, or code comments where applicable).

* * *

## Alternative Approaches Considered

Documented inline in the Approach section above for traceability:

1. **Multi-seed at fewer gens (3 seeds x 25 gens)** — rejected; confounds the single-seed test of
   substrate populated-ness vs seed-specificity. Queued as follow-up suggestion if seed 77 yields a
   partial replication (10-39 joint-pass cells).
2. **Run seed 77 at `_POOL_RESTART_EVERY = 25` (t0106's value)** — rejected per the NEURON memory
   creep finding in `research_code.md`; the cadence change costs ~2 minutes wall-clock for
   substantial memory mitigation.
3. **Run seed 77 at `N_GEN = 300` like t0106** — rejected because t0106 plateaued at gen 40 and the
   project envelope is tight; 60 gens is a 50% safety margin above t0106's empirical plateau.
4. **Re-evaluate t0106 cells at 8 directions instead of new seed (t0107 pattern)** — rejected as out
   of scope; that is a separate downstream re-evaluation task, not a substrate replicate.
5. **Change the silence guard or DSI metric** — rejected explicitly per the task brief's "out of
   scope" list. Any evaluator change breaks the like-for-like comparison.
