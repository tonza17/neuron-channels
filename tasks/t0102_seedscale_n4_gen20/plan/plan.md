---
spec_version: "2"
task_id: "t0102_seedscale_n4_gen20"
date_completed: "2026-05-11"
status: "complete"
---
# Plan: 68-d NSGA-II at GA seeds=2, N_EVAL_SEEDS=4, gens=20, random init

## Objective

Run 68-d random-init NSGA-II on the Bed B + morphology compartmental DSGC substrate (54-d
electrophys + 14-d morphology) with two independent GA restart seeds (44, 55) at pop=96 each,
reducing within-cell noise replicates from t0099's `N_EVAL_SEEDS=5` to `N_EVAL_SEEDS=4` and
extending generations from t0099's `N_GEN=8` to `N_GEN=20`, with no warm-start anchors. The goal is
to test whether a Poleg-Polsky-style seed/generation profile (fewer noise replicates, more
generations, more diverse GA restarts) recovers the strict joint-pass corner of objective space (DSI
>= 0.5, preferred-direction firing rate PD >= 30 Hz, robustness >= 0.7) that t0099 failed to find
with 3 random-init seeds at `N_EVAL_SEEDS=5, gens=5-8`. Success = the task produces 2 predictions
assets (one per GA seed, up to 96 + 20 x 96 = 2 016 Pareto candidates each) and 1 answer asset
stating whether N=4 / gens=20 / 2 seeds at random init recovers a joint-pass cell, plus charts and
metrics. Both a positive (>= 1 joint-pass cell) and a negative (0 cells in either seed, confirming
t0099's null is robust to the seed/generation rebalance) result are publishable.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0102_seedscale_n4_gen20/task.json` and the resolved long
description at `tasks/t0102_seedscale_n4_gen20/task_description.md`:

```text
Name: 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init

Short description: 68-d NSGA-II on Bed B+morph: 2 random-init GA seeds (44, 55), N_SEEDS=4,
gens=20, pop=96. Tests if 5x noise drop + 2.5x gens recovers joint-pass corner vs t0099 null.
$8 cap.

Expected assets: 2 predictions, 1 answer.

Long description (excerpts):
* GA seeds: 2 (random-init, seeds 44 and 55).
* Noise replicates N_SEEDS: 4 (reduced from 20 by factor of 5).
* Generations: 20 (up from t0099's 5-8).
* Population: 96 (default).
* Warm-start: none.
* Goal: test whether at constant Vast.ai budget, 4 noise replicates + 20 generations + 2 random-
  init seeds recovers the joint-pass corner.
* Run two NSGA-II processes with seed=44 and seed=55 (LHS-init), pop=96 each, on the same
  Vast.ai instance, sequentially.
* Output one predictions asset per seed plus one answer asset comparing t0102 vs t0099 vs t0091.
* Hard cost cap: $8 per task.
* Verification: cost <= $8, both predictions assets validate, answer asset validates, machines
  destroyed.
* Positive criterion: >= 1 strict joint-pass cell. Negative criterion: 0 cells in either seed.
* Out of scope: modifying t0080 N_SEEDS default; correcting PolegPolsky2026 summary; budget-
  matched ablation; expanding the search space beyond 68 d.
```

Concrete requirements decomposed (each requirement names the step that satisfies it and the evidence
that proves completion):

* **REQ-1** — Override the operative noise-replicate constant to `N_EVAL_SEEDS = 4`. **Note**: per
  `tasks/t0102_seedscale_n4_gen20/research/research_code.md`, the operative constant in the t0099
  substrate is `N_EVAL_SEEDS` in `tasks/t0099_*/code/constants_morphology.py:114`, NOT
  `N_SEEDS = 20` in t0080's `constants.py:43` (the latter is never imported by the substrate). The
  task text's "import-shadow N_SEEDS from t0080" is a documentation error corrected here. Satisfied
  by step 2. Evidence: `tasks/t0102_*/code/constants_morphology.py` contains
  `N_EVAL_SEEDS: int = 4`.
* **REQ-2** — Set `N_GEN = 20` in the local `constants_morphology.py`. Satisfied by step 2.
  Evidence: `tasks/t0102_*/code/constants_morphology.py` contains `N_GEN: int = 20`.
* **REQ-3** — Run two NSGA-II processes with `task_seed = 44` and `task_seed = 55`,
  LHS-initialised initial populations, pop=96 each. Satisfied by steps 7 and 9. Evidence:
  `results/data/nsga2_seed44_history.json` and `results/data/nsga2_seed55_history.json` exist with
  pop=96 and the two distinct seeds.
* **REQ-4** — No warm-start anchors (pure random LHS init). Satisfied by step 3. Evidence:
  `tasks/t0102_*/code/random_init.py` calls `LatinHypercubeSampling()` with no anchor injection.
* **REQ-5** — Both runs execute sequentially on the same Vast.ai CPU instance (single instance).
  Satisfied by steps 6, 7, 9. Evidence:
  `tasks/t0102_*/logs/steps/008_setup-machines/machine_log.json` records a single instance;
  `run_two_seeds.sh` runs the two seeds in series.
* **REQ-6** — Hard cost cap of $8 per task; cost watchdog reads `selected_offer.price_per_hour`
  from `machine_log.json`. Satisfied by steps 2, 6, 7, 9, 10. Evidence:
  `tasks/t0102_*/code/constants.py` sets `T0102_TASK_BUDGET_TOTAL_USD: float = 8.00` and
  `T0102_HARD_BUDGET_PER_SEED_USD: float = 4.00`; final `results/costs.json` total <= $8.00.
* **REQ-7** — Substrate-consistency smoke gate must pass at `N_EVAL_SEEDS=4` against the t0093
  anchor-1 fingerprint (bedb_like PD-rate 43.6 +/- 1.0 Hz) before launching the long run. Satisfied
  by step 8 (smoke gate). Evidence: `tasks/t0102_*/logs/steps/008_setup-machines/smoke_gate.json`
  records `pass: true` and PD-rate within tolerance.
* **REQ-8** — Incremental budget gate: after seed=44 finishes, check actual elapsed cost vs $8
  cap; if first seed already > $5.00, write an intervention file and halt before launching seed=55.
  Satisfied by step 9 (sub-step 9c). Evidence:
  `tasks/t0102_*/logs/steps/009_implementation/budget_gate_after_seed44.json` records the elapsed
  cost decision and either `proceed_to_seed55: true` or an intervention file at
  `tasks/t0102_*/intervention/budget_gate_blocked.md`.
* **REQ-9** — Restart Python workers between generations (S-0099-04 mitigation against NEURON
  memory accumulation). Satisfied by step 7. Evidence: `tasks/t0102_*/code/nsga2_driver.py` includes
  the inherited per-generation worker restart logic copied from t0099.
* **REQ-10** — Produce one `predictions` asset per GA seed (2 total), each containing the full
  cell history (init + 20 generations x 96 candidates per generation, minus any early-terminated
  generations). Satisfied by step 12. Evidence:
  `tasks/t0102_*/assets/predictions/t0102_seed44_pareto/` and
  `tasks/t0102_*/assets/predictions/t0102_seed55_pareto/` both pass `verify_predictions_asset.py`.
* **REQ-11** — Produce 1 `answer` asset answering "Does N_EVAL_SEEDS=4 + N_GEN=20 + 2 random-init
  GA seeds recover the strict joint-pass corner (DSI >= 0.5, PD >= 30 Hz, robustness >= 0.7) on the
  68-d Bed B + morphology substrate without warm-start?" Satisfied by step 14. Evidence:
  `tasks/t0102_*/assets/answer/t0102_joint_pass_recovery/` passes `verify_answer_asset.py`.
* **REQ-12** — Side-by-side compare t0102 vs t0099 vs t0091 on (DSI, PD, joint-pass count,
  robustness, anchor distribution). Satisfied by step 13. Evidence:
  `tasks/t0102_*/results/data/cross_seed_summary.json` includes a 5x5 anchor table (5 anchors x
  {seed 44, seed 55, t0091, t0099 aggregate, baseline}) and HV/Pareto overlay PNGs in
  `results/images/`.
* **REQ-13** — Compute metrics over Pareto cells and write `results/metrics.json` with the four
  registered metrics (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse`) using the explicit multi-variant format with
  variants for `seed44` and `seed55`. Satisfied by step 13. Evidence: `results/metrics.json` parses
  and contains two variants `seed44` and `seed55`, each populating the four registered metric keys.
* **REQ-14** — Generate at least 2 charts: (a) HV trajectory over generations comparing the two
  seeds against t0091 and t0099, (b) DSI vs PD scatter colour-coded by anchor + joint-pass corner
  overlay. Satisfied by step 13. Evidence: `tasks/t0102_*/results/images/hv_trajectory.png` and
  `tasks/t0102_*/results/images/dsi_vs_pd_scatter.png` exist.
* **REQ-15** — Destroy the Vast.ai instance after both seeds complete; record final cost in
  `results/costs.json` and `results/remote_machines_used.json`. Satisfied by step 11. Evidence:
  `verify_machines_destroyed t0102_seedscale_n4_gen20` exits with 0 errors.
* **REQ-16** — Do not modify any prior task folder (immutability). Satisfied implicitly across all
  steps. Evidence: post-task `git diff main -- tasks/` shows only files under
  `tasks/t0102_seedscale_n4_gen20/` were touched.

* * *

## Approach

### Technical approach

Re-use the t0099 substrate verbatim. Per the code research in
`tasks/t0102_*/research/research_code.md`, the t0099 NSGA-II pipeline is a 22-file stack with a
single import-time `bootstrap.py` side effect that monkey-patches the t0024 Bed B Linux loader. The
substrate already imports two registered library assets:

* `procedural_dsgc_morphology_generator` (t0090, replaced by
  `procedural_dsgc_morphology_generator_fix` from t0092 via correction C-0093-01) — used via
  `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult`,
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`,
  and
  `from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import insert_baseline_channels`.
* `de_rosenroll_2026_dsgc` (t0024) — used via
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import _ensure_neuron_on_path, load_neuron`.

The actual NSGA-II entry point is `tasks/t0099_*/code/nsga2_driver.py` (369 lines), orchestrated by
`tasks/t0099_*/code/run_three_seeds.sh`. The plan deliberately uses the corrected file names — the
task-description references to `run_loop.py` are documentation errors per the code research.

The operative noise-replicate constant is `N_EVAL_SEEDS` in t0099's `constants_morphology.py:114`,
NOT `N_SEEDS` in t0080's `constants.py:43`. t0099 ships a stale `N_SEEDS = 20` in
`constants_electrophys.py:43` that is never imported. The plan corrects this here.

Concrete strategy: copy all ~22 t0099 substrate Python files plus `run_three_seeds.sh` verbatim into
`tasks/t0102_seedscale_n4_gen20/code/`, then edit four files:

1. `constants_morphology.py` — change `N_EVAL_SEEDS: int = 5` to `4`, and `N_GEN: int = 8` to
   `20`.
2. `constants.py` — rename `T0099_*` to `T0102_*`, set `T0102_SEEDS: tuple[int, ...] = (44, 55)`,
   set `T0102_HARD_BUDGET_PER_SEED_USD: float = 4.00`, set
   `T0102_TASK_BUDGET_TOTAL_USD: float = 8.00`.
3. `paths.py` — re-anchor `TASK_ROOT` via `__file__` and add new `T0099_*_JSON` constants pointing
   at t0099's result data for cross-seed comparison.
4. `run_three_seeds.sh -> run_two_seeds.sh` — change the loop to iterate `(44, 55)`, swap `t0099`
   module paths for `t0102`.

All other substrate files (`evaluator.py`, `nsga2_driver.py`, `generator_wrapper.py`,
`bootstrap.py`, `random_init.py`, `smoke_gate.py`, `cost_watchdog.py`, `hv_plateau_watchdog.py`,
`trial_helpers.py`, `apply_params.py`, `parametric_placer.py`, `build_cell_ais.py`,
`extend_with_ais.py`, `recorder.py`, `anchor_definitions.py`, `per_seed_analysis.py`,
`anchor_classifier.py`, `biological_priors.py`, `biological_scorecard.py`, `cross_seed_analysis.py`,
`metrics_builder.py`, `build_assets.py`, `build_morphology_charts.py`, `run_local_analysis.py`,
`sync_results_back.sh`) are copied unchanged — they pick up the new values automatically via the
relative imports.

Cross-seed analysis (`cross_seed_analysis.py`) is extended from t0099's 5x4 anchor distribution to a
5x5 table (5 anchors x {seed 44, seed 55, t0091 reference, t0099 aggregate, baseline}). The HV plot
is extended to overlay 5 lines (the two t0102 seeds, t0091, t0099 average, baseline).

The HV plateau watchdog (`HVPlateauTermination`) plus the cost watchdog (`CostWatchdogTermination`)
plus `MaximumGenerationTermination(n_max_gen=20)` are combined in `TerminationCollection`. Any one
of the three stops a run early. With HV plateau threshold 1% over a trailing window of 2 (kicking in
after 4 generations), an N_EVAL_SEEDS=4 / N_GEN=20 run on a converged front may terminate before 20
gens; this is desired behaviour.

### Alternative approaches considered

* **Env-var override of `N_EVAL_SEEDS` instead of editing the constants file**. Rejected: loses
  static type checking, conflicts with the constants module's import-time asserts, adds runtime side
  channels. The code research explicitly tests this and recommends rejection (see
  `tasks/t0102_*/research/research_code.md` Recommended Approach table).
* **Parallelise the two GA seeds across two Vast.ai instances** to halve wall-clock. Rejected: a
  second instance's provisioning overhead (~$0.25 + ~10 minutes setup) plus the second sync-back
  cost would push us toward or past the $8 cap with no margin. Sequential single-instance is the
  budget-safe choice.
* **Single GA seed at gens=40** (same total compute, more depth per seed). Rejected: per-seed
  variance in t0099 (single-seed best PD-rate 18.7 Hz at seed 22 vs 9.6 Hz at seed 11) shows the
  random-init lineage is high-variance across GA seeds; two seeds give us a usable variance estimate
  for the answer asset, while one seed at gens=40 leaves us indistinguishable from a single random
  Monte Carlo draw.
* **`N_EVAL_SEEDS=8` instead of 4** to halve noise rather than quarter it. Rejected: the brainstorm
  session 21 explicitly directed N=4 / gens=20 / 2 seeds as the Poleg-Polsky-inspired configuration;
  deviating to N=8 would change the experimental question. If N=4 turns out too noisy (smoke gate
  fails or substrate consistency degrades) the documented fallback is to halt and refile as a
  follow-up task.

### Task types

`task.json` already lists `task_types: ["experiment-run", "data-analysis", "answer-question"]`,
which matches the work this task does:

* **experiment-run** Planning Guidelines: define hypothesis (joint-pass recovery without
  warm-start), enumerate independent variables (`N_EVAL_SEEDS`, `N_GEN`, GA seed), dependent
  variables (joint-pass count, DSI, PD, HV trajectory, anchor distribution), estimate costs and set
  a cap ($8), and identify baselines (t0091 warm-start = 1 cell at gen 2; t0099 random init = 0
  cells across 3 seeds). Multi-condition: use the explicit multi-variant `metrics.json` format with
  one variant per GA seed (seed44, seed55).

* **data-analysis** Planning Guidelines: list all metrics and chart types upfront (HV trajectory,
  DSI vs PD scatter, anchor distribution heatmap), state statistical tests (joint-pass yield Wilson
  confidence interval vs t0099's 0/2208 null), and pre-declare per-subset breakdowns (per-seed,
  per-anchor).

* **answer-question** Planning Guidelines: define the single canonical question text (REQ-11),
  decide evidence channels (new experimental NSGA-II runs + cross-task comparison to t0091/t0099 +
  literature framing from PolegPolsky2026/Druckmann2007/Hay2011), and set the stopping criterion for
  the answer (both seeds completed OR budget exhausted with intervention recorded).

### Registered-metric coverage

The project registers 4 metrics in `meta/metrics/`: `direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`. All four apply per Pareto
cell in this task (every evaluated cell produces a tuning curve and a DSI). They are reported as
per-variant summary statistics (best, mean over strict-pass cells when those exist, mean over the
full Pareto otherwise). Concrete measurement plan in step 13.

* * *

## Cost Estimation

| Item | Quantity | Rate | Subtotal |
| --- | --- | --- | --- |
| Vast.ai instance (RTX 4090 / EPYC 7B13 64-core, Norway preferred) | ~20 h | $0.24/hr | ~$4.80 |
| Provisioning + smoke + image pull buffer | ~2 h | $0.24/hr | ~$0.48 |
| Vast.ai instance budget headroom for memory-leak slowdown | ~5 h | $0.24/hr | ~$1.20 |
| LLM API calls (planning, analysis, answer-asset writing) | n/a | n/a | $0.00 (in-harness) |
| **Subtotal expected** |  |  | **~$6.50** |
| **Hard per-task cap** |  |  | **$8.00** |

Per-seed cap is set at $4.00 in `T0102_HARD_BUDGET_PER_SEED_USD`, so even if cost watchdog triggers
on seed 44 at exactly $4.00 and seed 55 follows for another $4.00, the task stays at $8.

Project-wide budget context: total project budget $35; spent $23.91; remaining $11.09. The $8 cap
for this task fits within the remaining $11.09 with $3.09 of project-level headroom in case of
overrun. If the implementation agent observes the cost rising above $5.00 after the first seed
finishes, the incremental budget gate (REQ-8) halts before launching seed 55 and writes an
intervention file.

* * *

## Step by Step

### Milestone 1: Local code preparation (no cost)

1. **Copy the t0099 substrate into the task code folder.** Run a `cp` of every file listed in
   `tasks/t0102_*/research/research_code.md` Reusable Code section from
   `tasks/t0099_random_init_pareto_robustness/code/` into `tasks/t0102_seedscale_n4_gen20/code/`.
   Files to copy verbatim (no edits required): `bootstrap.py`, `evaluator.py`,
   `generator_wrapper.py`, `random_init.py`, `smoke_gate.py`, `cost_watchdog.py`,
   `hv_plateau_watchdog.py`, `trial_helpers.py`, `apply_params.py`, `parametric_placer.py`,
   `build_cell_ais.py`, `extend_with_ais.py`, `recorder.py`, `anchor_definitions.py`,
   `per_seed_analysis.py`, `anchor_classifier.py`, `biological_priors.py`,
   `biological_scorecard.py`, `metrics_builder.py`, `build_morphology_charts.py`,
   `run_local_analysis.py`, `sync_results_back.sh`, `nsga2_driver.py`. Inputs: t0099 code/. Outputs:
   identical files under `tasks/t0102_*/code/`. Expected observable output:
   `ls tasks/t0102_*/code/ | wc -l` reports >= 22 Python files. Satisfies REQ-9 (worker restart
   logic already inside nsga2_driver.py and evaluator.py).

2. **Edit `tasks/t0102_seedscale_n4_gen20/code/constants_morphology.py` to override `N_EVAL_SEEDS`
   and `N_GEN`.** Open the copied file at line 114 and change `N_EVAL_SEEDS: int = 5` to
   `N_EVAL_SEEDS: int = 4`. Find the `N_GEN: int = 8` line and change to `N_GEN: int = 20`. Add a
   docstring comment at the top of the file recording the override reason and the t0099 prior
   values. Inputs: copied constants_morphology.py. Outputs: edited file. Expected observable output:
   `grep -n 'N_EVAL_SEEDS\|N_GEN' tasks/t0102_*/code/constants_morphology.py` shows
   `N_EVAL_SEEDS: int = 4` and `N_GEN: int = 20`. Satisfies REQ-1, REQ-2.

3. **Edit `tasks/t0102_seedscale_n4_gen20/code/constants.py` for seeds and budget.** Replace
   `T0099_SEEDS = (11, 22, 33)` with `T0102_SEEDS: tuple[int, ...] = (44, 55)`. Replace the per-seed
   budget constant `T0099_HARD_BUDGET_PER_SEED_USD = 5.00` with
   `T0102_HARD_BUDGET_PER_SEED_USD: float = 4.00` and `T0099_TASK_BUDGET_TOTAL_USD = 20.00` with
   `T0102_TASK_BUDGET_TOTAL_USD: float = 8.00`. Confirm the existing
   `assert sum([per_seed] * len(seeds)) <= total` still passes (4.00 * 2 = 8.00 <= 8.00). Inputs:
   copied constants.py. Outputs: edited file. Expected observable output:
   `grep -n 'T0102_SEEDS\|T0102_HARD_BUDGET_PER_SEED_USD\|T0102_TASK_BUDGET_TOTAL_USD' tasks/t0102_*/code/constants.py`
   shows the three constants with values `(44, 55)`, `4.00`, `8.00`. Satisfies REQ-3, REQ-4, REQ-6.

4. **Adapt `tasks/t0102_*/code/paths.py` for t0102 outputs and t0099 cross-seed inputs.** Edit
   `TASK_ROOT` to compute via `__file__` (already in the t0099 copy). Add path constants
   `T0099_RESULTS_DATA_DIR`, `T0099_PARETO_FRONT_JSON`, `T0099_HV_TRAJECTORY_JSON`,
   `T0099_ANCHOR_TRACKING_JSON` pointing at
   `tasks/t0099_random_init_pareto_robustness/results/data/`. Inputs: copied paths.py. Outputs:
   edited file. Expected observable output:
   `python -c "from tasks.t0102_seedscale_n4_gen20.code.paths import T0099_PARETO_FRONT_JSON; print(T0099_PARETO_FRONT_JSON.exists())"`
   prints `True`. Satisfies REQ-12.

5. **Adapt `tasks/t0102_*/code/run_two_seeds.sh` from t0099's run_three_seeds.sh.** Rename the
   copied file from `run_three_seeds.sh` to `run_two_seeds.sh`. Change the `for SEED in 11 22 33`
   loop to `for SEED in 44 55`. Swap module path strings from
   `tasks.t0099_random_init_pareto_robustness.code.nsga2_driver` to
   `tasks.t0102_seedscale_n4_gen20.code.nsga2_driver`. Insert an incremental budget gate between the
   two seed invocations that reads `results/data/nsga2_seed44_cost.json` and exits non-zero if the
   elapsed cost exceeds $5.00 (REQ-8 enforcement). Inputs: copied run_three_seeds.sh. Outputs:
   edited run_two_seeds.sh. Expected observable output:
   `bash -n tasks/t0102_*/code/run_two_seeds.sh` exits 0;
   `grep 'for SEED' tasks/t0102_*/code/run_two_seeds.sh` shows `for SEED in 44 55`. Satisfies REQ-5,
   REQ-8.

6. **Edit `tasks/t0102_*/code/cross_seed_analysis.py` to extend the comparison to t0099.** In
   `cross_seed_analysis.py`, extend the anchor-distribution table from 5x4 to 5x5 by adding a
   `t0099_aggregate` column that reads from the new `T0099_ANCHOR_TRACKING_JSON` path. Extend the
   HV-trajectory plot to overlay 5 curves: seed 44, seed 55, t0091 reference, t0099 average,
   baseline (zero). Inputs: copied cross_seed_analysis.py, t0091 result data, t0099 result data.
   Outputs: edited cross_seed_analysis.py. Expected observable output:
   `python -m py_compile tasks/t0102_*/code/cross_seed_analysis.py` exits 0. Satisfies REQ-12.

7. **Edit `tasks/t0102_*/code/build_assets.py` to emit 2 predictions assets + 1 answer asset.** In
   the copied file, change the asset emission loop from 3 predictions assets (t0099 had 3 seeds) to
   2 predictions assets (seeds 44 and 55), and from a single results-summary answer to the t0102
   answer asset `t0102_joint_pass_recovery`. Inputs: copied build_assets.py. Outputs: edited
   build_assets.py. Expected observable output:
   `python -m py_compile tasks/t0102_*/code/build_assets.py` exits 0. Satisfies REQ-10, REQ-11.

8. **Lint the task code folder.** Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run ruff check --fix tasks/t0102_seedscale_n4_gen20/code`
   and
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run mypy -p tasks.t0102_seedscale_n4_gen20.code`.
   Inputs: t0102 code/. Outputs: zero errors / zero warnings. Expected observable output: both
   commands exit 0. Catches any stale `t0099_` import paths or constant references missed in steps
   2-7. Satisfies REQ-16 (immutability — only files under tasks/t0102_*/code/ are touched).

### Milestone 2: Smoke gate and remote provisioning

9. **[CRITICAL] Run the substrate-consistency smoke gate locally on Windows at `N_EVAL_SEEDS=4`.**
   Execute
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run python -m tasks.t0102_seedscale_n4_gen20.code.smoke_gate`.
   This runs t0099's 3 hardcoded smoke seeds `[42, 4242, 424242]` against the t0093 anchor-1
   bedb_like fingerprint (PD-rate 43.6 +/- 1.0 Hz). Validation gate: this is the trivial baseline
   for "the pipeline is alive" — if the smoke gate reports the anchor-1 PD-rate outside
   `[42.6, 44.6]` Hz, STOP and debug the import chain; do NOT proceed to Vast.ai provisioning. After
   a passing smoke gate, manually read the printed PD-rate for each of the 3 smoke seeds and verify
   all three are within tolerance individually (not just the mean). Inputs: t0102 code/, t0093
   fingerprint JSON, MOD library from t0080. Outputs: stdout PD-rates,
   `logs/steps/008_setup-machines/smoke_gate_local.json`. Expected observable output: all 3 smoke
   seeds report bedb_like PD-rate within [42.6, 44.6] Hz. Satisfies REQ-7.

10. **Provision one Vast.ai instance.** Target: AMD EPYC 7B13 64 effective cores, no GPU requirement
    (NEURON is CPU-bound), 503 GB RAM default, Norway preferred for $0.24/hr pricing consistent with
    t0099. Record `selected_offer.price_per_hour` in
    `logs/steps/008_setup-machines/machine_log.json`. Reject offers above $0.40/hr — if no Norway
    offer is available, fall back to any EPYC 7B13 below $0.40/hr (still fits $8 cap at 20 h
    runtime). Inputs: Vast.ai marketplace via setup-remote-machine skill. Outputs:
    `machine_log.json` with instance ID, IP, and hourly rate. Expected observable output: SSH
    handshake succeeds; `nvidia-smi` may fail (no GPU is fine). Satisfies REQ-5.

11. **SCP the t0102 code/ and shared MOD library to the Vast.ai instance.** Use the
    setup-remote-machine sync utility to copy the entire `tasks/t0102_seedscale_n4_gen20/` plus the
    shared MOD library at `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/x86_64/` plus
    the t0093 fingerprint at `tasks/t0093_resweep_and_t0090_correction/results/data/`. Run
    `bootstrap.py` once on the remote machine to verify the Linux .so resolution succeeds. Inputs:
    local repo. Outputs: remote repo mirror. Expected observable output:
    `ssh remote 'cd repo && uv run python -c "from tasks.t0102_seedscale_n4_gen20.code import bootstrap"'`
    exits 0. Satisfies REQ-5.

12. **[CRITICAL] Re-run the smoke gate on the Vast.ai instance.** Same command as step 9 but
    executed remotely. Validation gate: if the remote smoke gate fails (any of 3 smoke seeds outside
    the 42.6-44.6 Hz window), STOP. Do NOT launch the long run — the import chain is broken on the
    remote Linux environment. Halt and debug: inspect individual PD-rate values and the bootstrap
    log, do not proceed to seed=44. Inputs: remote repo. Outputs:
    `logs/steps/008_setup-machines/smoke_gate_remote.json`. Expected observable output: all 3 smoke
    seeds within tolerance. Satisfies REQ-7.

### Milestone 3: Long NSGA-II runs

13. **[CRITICAL] Run NSGA-II seed=44 on the Vast.ai instance.** Execute
    `bash tasks/t0102_seedscale_n4_gen20/code/run_two_seeds.sh 44` (the script's per-seed branch).
    This launches
    `tasks.t0102_seedscale_n4_gen20.code.nsga2_driver.run_nsga2_for_seed(task_seed=44)` with pop=96,
    gens=20, N_EVAL_SEEDS=4, LHS init. Validation gate: this is an expensive operation (~10 hours,
    ~$2.40 worth of compute). Per-cell baseline is the t0099 seed-22 best DSI of 0.49 at PD=18.7 Hz.
    After generation 1 finishes (~30 minutes), pull back the generation-1 cell history and read 5
    individual cells: confirm DSI values are non-negative and in [0, 1], PD rates are non-negative,
    robustness values are in [0, 1]. If any DSI is NaN or PD is negative, halt and debug the
    evaluator. The cost watchdog and HV-plateau watchdog are inside the termination collection and
    may stop the run early. Inputs: remote code/, morphology generator library, Bed B cell library.
    Outputs: `results/data/nsga2_seed44_history.json` (full Pareto trajectory),
    `results/data/nsga2_seed44_cost.json` (cumulative cost watchdog readout),
    `logs/steps/009_implementation/seed44_stdout.log`. Expected observable output: stdout
    "Termination reached at gen N" for some N in [10, 20]; cost <= $4.00. Satisfies REQ-3, REQ-9.

14. **Incremental budget gate after seed=44.** Read `results/data/nsga2_seed44_cost.json`. If
    cumulative cost > $5.00, write `intervention/budget_gate_blocked.md` recording the elapsed cost,
    the cause (NEURON memory accumulation, slower-than-expected per-cell evaluation, expensive
    Vast.ai offer, etc.), and the recommendation to either halt the task and accept seed=44 alone,
    or request the orchestrator to bump the cap. Halt before launching seed=55. If cumulative cost
    <= $5.00, write `logs/steps/009_implementation/budget_gate_after_seed44.json` with
    `proceed_to_seed55: true` and continue. Inputs: seed44_cost.json. Outputs: either an
    intervention file or a budget-gate decision JSON. Expected observable output: a decision file
    exists. Satisfies REQ-8.

15. **[CRITICAL] Run NSGA-II seed=55 on the same Vast.ai instance.** Same command and validation
    gates as step 13 but with `task_seed=55`. Same cell-history inspection requirement after
    generation 1. Inputs: remote code/. Outputs: `results/data/nsga2_seed55_history.json`,
    `results/data/nsga2_seed55_cost.json`. Expected observable output: stdout "Termination reached
    at gen N"; combined seed44+seed55 cost <= $8.00. Satisfies REQ-3, REQ-9.

16. **Pull results back from the Vast.ai instance.** Run the inherited `sync_results_back.sh` script
    to rsync `results/data/`, `logs/`, and any intermediate artefacts to the local repo. Inputs:
    remote results. Outputs: synced local `results/data/`, `logs/`. Expected observable output:
    `ls tasks/t0102_*/results/data/` shows `nsga2_seed44_history.json`, `nsga2_seed55_history.json`,
    and the per-seed cost JSONs. Satisfies REQ-5.

### Milestone 4: Teardown and analysis

17. **Destroy the Vast.ai instance.** Use the setup-remote-machine teardown utility to terminate the
    instance and record the final billed amount in `results/remote_machines_used.json`. Inputs:
    machine ID. Outputs: `results/remote_machines_used.json` (final cost), Vast.ai instance
    terminated. Expected observable output: Vast.ai dashboard shows instance in "destroyed" state;
    `uv run python -m arf.scripts.verificators.verify_machines_destroyed t0102_seedscale_n4_gen20`
    exits 0. Satisfies REQ-15.

18. **Build the 2 predictions assets.** Run `tasks.t0102_seedscale_n4_gen20.code.build_assets`. This
    reads `results/data/nsga2_seed44_history.json` and `results/data/nsga2_seed55_history.json` and
    emits two predictions asset folders following `meta/asset_types/predictions/specification.md`:
    `assets/predictions/t0102_seed44_pareto/` and `assets/predictions/t0102_seed55_pareto/`. Each
    contains `details.json` (predictions metadata with the GA seed, pop, gen count, N_EVAL_SEEDS=4),
    `description.md` (one-page description of the run configuration and result counts), and
    `files/pareto_cells.jsonl` (per-cell JSONL with the 68-d parameter vector, DSI, PD rate,
    robustness, anchor classification, generation index). Inputs: NSGA-II history JSONs. Outputs: 2
    predictions asset folders. Expected observable output:
    `uv run python -m arf.scripts.verificators.verify_predictions_asset tasks/t0102_seedscale_n4_gen20/assets/predictions/t0102_seed44_pareto`
    exits 0; same for seed55. Satisfies REQ-10.

19. **Run per-seed and cross-seed analysis.** Execute
    `tasks.t0102_seedscale_n4_gen20.code.per_seed_analysis` for each seed (classifies Pareto cells
    to nearest anchor, counts strict joint-pass) followed by
    `tasks.t0102_seedscale_n4_gen20.code.cross_seed_analysis` (5x5 anchor distribution table, HV
    overlay, DSI vs PD scatter). Inputs: predictions asset files, t0091 result JSONs, t0099 result
    JSONs. Outputs: `results/data/per_seed_summary_seed44.json`,
    `results/data/per_seed_summary_seed55.json`, `results/data/cross_seed_summary.json`,
    `results/images/hv_trajectory.png`, `results/images/dsi_vs_pd_scatter.png`,
    `results/images/anchor_distribution_heatmap.png`. Expected observable output: 3 PNG files
    present; cross_seed_summary.json contains a 5x5 anchor table and a strict_joint_pass_count field
    per seed. Satisfies REQ-12, REQ-14.

20. **Compute metrics and write `results/metrics.json`.** Use
    `tasks.t0102_seedscale_n4_gen20.code.metrics_builder` to compute, per GA seed (variant), the
    four registered metric keys: `direction_selectivity_index` (best DSI over the Pareto front),
    `tuning_curve_hwhm_deg` (median HWHM over strict-pass cells, or median over the full Pareto if
    zero strict-pass), `tuning_curve_reliability` (median Pearson rho over the 4 noise replicates
    per cell, averaged over the Pareto front), `tuning_curve_rmse` (best RMSE over the Pareto front,
    the primary optimisation objective). Write to `results/metrics.json` using the explicit
    multi-variant format with variants `seed44` and `seed55`. Read
    `arf/specifications/metrics_specification.md` for the exact JSON schema. Inputs: per-seed cell
    histories. Outputs: `results/metrics.json`. Expected observable output:
    `jq '.variants | keys' tasks/t0102_*/results/metrics.json` prints `["seed44", "seed55"]`; both
    variants contain the four registered metric keys. Satisfies REQ-13.

21. **Build the answer asset.** Generate `assets/answer/t0102_joint_pass_recovery/` per
    `meta/asset_types/answer/specification.md`: `details.json` (question text, evidence channels
    used, citation list), the canonical short answer document at `short_answer.md` (2-5 sentences
    stating Yes / No / I don't know with the strict joint-pass corner count from each seed), the
    canonical full answer document at `full_answer.md` (mini-paper structure with Sections:
    Question, Short Answer, Method, Evidence from Code or Experiments, Evidence from Existing
    Papers, Synthesis, Limitations, Sources). The Short Answer section must contain no inline
    citations. Sources section uses markdown reference links. Cite t0099, t0091, PolegPolsky2026,
    Druckmann2007, Hay2011 as supporting evidence. Inputs: per-seed summaries, cross-seed summary,
    research files. Outputs: `assets/answer/t0102_joint_pass_recovery/details.json`,
    `short_answer.md`, `full_answer.md`. Expected observable output:
    `uv run python -m arf.scripts.verificators.verify_answer_asset tasks/t0102_seedscale_n4_gen20/assets/answer/t0102_joint_pass_recovery`
    exits 0. Satisfies REQ-11.

22. **Generate at least 2 charts.** Confirmed via step 19 (hv_trajectory.png, dsi_vs_pd_scatter.png,
    anchor_distribution_heatmap.png — three charts). If additional clarity is needed, run
    `tasks.t0102_seedscale_n4_gen20.code.build_morphology_charts` to add per-cell morphology
    visualisations to `results/images/morphology/`. Inputs: predictions cells. Outputs: PNG files.
    Expected observable output: at least 2 PNGs in `results/images/`. Satisfies REQ-14.

* * *

## Remote Machines

One Vast.ai instance is required:

* GPU: not required (NEURON is CPU-bound).
* CPU: AMD EPYC 7B13, 64 effective cores (same as t0099, t0091).
* RAM: 503 GB default.
* Location: Norway preferred (for $0.24/hr pricing).
* Hourly cap: $0.40/hr (reject more expensive offers).
* Runtime: ~20 hours expected, 25 hours hard ceiling enforced by the cost watchdog at $0.40 x 25 =
  $10 — which is above the $8 cap, so the cost watchdog will trip earlier in practice.
* Provider: Vast.ai (`setup-remote-machine` skill).
* Lifecycle: provisioned in step 10, destroyed in step 17.

* * *

## Assets Needed

* **Bed B compartmental cell substrate**: `de_rosenroll_2026_dsgc` library from t0024 (HOC template,
  vendored MOD library, build_cell). Imported via
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import _ensure_neuron_on_path, load_neuron`.
* **Compiled MOD library**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/x86_64/` —
  referenced as `T0080_MODS_DIR` by t0099's paths.py (unchanged). NEURON SUFFIX namespace is shared.
* **Morphology generator (patched)**: `procedural_dsgc_morphology_generator_fix` library from t0092
  (replaces t0090 via correction C-0093-01). Imported via
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`,
  `from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import insert_baseline_channels`,
  and
  `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult`.
* **t0093 anchor-1 fingerprint**:
  `tasks/t0093_resweep_and_t0090_correction/results/data/post_fix_verification_summary.json` for the
  smoke-gate target (bedb_like PD-rate 43.6 +/- 1.0 Hz).
* **t0091 reference data**:
  `tasks/t0091_morphology_extended_nsga2_v1/results/data/pareto_front.json`, `hv_trajectory.json`,
  `anchor_tracking.json`, `biological_scorecard_68d.json` — for cross-seed comparison columns and
  HV-trajectory overlay.
* **t0099 reference data**: `tasks/t0099_random_init_pareto_robustness/results/data/`
  (anchor_tracking.json, hv_trajectory.json, pareto_front.json) — for the third reference column
  in the cross-seed comparison.

* * *

## Expected Assets

Matches `task.json` `expected_assets`:

* **2 predictions assets** under `tasks/t0102_seedscale_n4_gen20/assets/predictions/`:
  * `t0102_seed44_pareto/` — full per-cell history of the seed=44 NSGA-II run (96 init + up to 20
    x 96 generation cells, minus any early-terminated generations). Contains DSI, PD-rate,
    robustness, anchor classification, and 68-d parameter vector per cell.
  * `t0102_seed55_pareto/` — same for seed=55.
* **1 answer asset** under `tasks/t0102_seedscale_n4_gen20/assets/answer/`:
  * `t0102_joint_pass_recovery/` — short and full answers to "Does N_EVAL_SEEDS=4 + N_GEN=20 + 2
    random-init GA seeds recover the strict joint-pass corner (DSI >= 0.5, PD >= 30 Hz, robustness
    >= 0.7) on the 68-d Bed B + morphology substrate without warm-start?", with evidence from the
    new experiment plus comparisons to t0091 and t0099.

* * *

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already done in prior steps) | 0 h |
| Local code prep + lint (milestone 1) | 1-2 h |
| Local + remote smoke gates (steps 9, 12) | 0.5 h |
| Vast.ai provisioning + SCP (steps 10, 11) | 0.5-1 h |
| NSGA-II seed=44 (step 13) | 9-12 h |
| Budget gate decision (step 14) | <0.1 h |
| NSGA-II seed=55 (step 15) | 9-12 h |
| Pull results + teardown (steps 16, 17) | 0.5 h |
| Analysis + asset build + answer (steps 18-22) | 3-4 h |
| **Total** | **23-32 h** |

The Vast.ai compute portion (steps 10-17) is ~20-25 h continuous; the rest is local Windows time
that can be interleaved.

* * *

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Per-cell DSI/PD variance at N_EVAL_SEEDS=4 is so high that NSGA-II selection becomes random, yielding no joint-pass cells regardless of generation count. | Medium | Negative answer becomes uninterpretable | Run substrate-consistency smoke gate (step 9, step 12); if smoke gate passes within 1 Hz of t0093 fingerprint the noise level is acceptable. Post-NSGA-II, re-evaluate top-10 Pareto cells at N_EVAL_SEEDS=20 in a follow-up analysis to quantify the variance gap. |
| NEURON memory accumulation causes per-seed wall-clock to grow super-linearly (S-0099-04 failure pattern). | Medium | Budget overrun on seed=44 | Worker restart between generations is already inside the inherited nsga2_driver.py (REQ-9). If wall-clock still degrades, the cost watchdog trips at $4 per seed and triggers HVPlateauTermination early. The incremental budget gate (REQ-8) blocks seed=55 if seed=44 already exceeded $5.00. |
| Vast.ai instance fails to provision in $0.24/hr range; only $0.40/hr offers available. | Low | Budget reduces to ~12.5 h headroom instead of ~20 h | The cost watchdog reads the actual `price_per_hour` from machine_log.json; at $0.40/hr the $8 cap still buys 20 h, which fits expected wall-clock. If only > $0.40/hr offers exist, halt provisioning and write an intervention file. |
| t0090 / t0093 morphology generator silently produces empty trees again (pre-fix bug). | Low | All Pareto cells NaN | Smoke gate REQ-7 against the t0093 anchor-1 fingerprint catches this before commitment. The t0092 fix is already C-0093-01-corrected and the t0099 lineage has confirmed 60/60 stability. |
| HV-plateau termination trips at gen 5 instead of running to gen 20, giving us a partial result. | Medium | Lower effective gen count than planned | This is desired behaviour for converged runs and is not a defect. The analysis step reports the actual termination generation; if both seeds plateau by gen 8, that itself is a meaningful answer about substrate convergence speed. |
| Random-init at gens=20 still produces zero joint-pass cells, replicating t0099's null. | Medium | The result is "negative" rather than "positive" but is still publishable per REQ-11 | The answer asset is written to state the result either way. A 0/2 outcome strengthens the conclusion that the warm-start is load-bearing; the Wilson 95% upper CI on yield rate goes below 0.0007 at 4032 evaluations, which is a stronger statement than t0099 could make. |
| Implementation agent silently substitutes a different override mechanism (env var, CLI flag) instead of editing constants_morphology.py. | Low | Plan/result mismatch | Step 2 names the exact file and line numbers to edit and step 8 lints the result with mypy. The "Alternatives considered" section explicitly rejects the env-var path. If the implementation agent cannot edit constants_morphology.py for any reason (file permissions, etc.), it must create an intervention file. |

* * *

## Verification Criteria

* Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run python -m arf.scripts.verificators.verify_plan t0102_seedscale_n4_gen20`;
  expected exit code 0 with zero errors and zero warnings. This confirms the plan satisfies the
  plan_specification.md v2 structural requirements before implementation begins.

* Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run python -m arf.scripts.verificators.verify_task_metrics t0102_seedscale_n4_gen20`;
  expected exit code 0. This confirms the explicit multi-variant `results/metrics.json` (REQ-13) has
  variants `seed44` and `seed55` each populating the four registered metric keys
  (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`).

* Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run python -m arf.scripts.verificators.verify_predictions_asset tasks/t0102_seedscale_n4_gen20/assets/predictions/t0102_seed44_pareto`
  and the same command for `t0102_seed55_pareto`; both expected exit code 0. This confirms REQ-10 (2
  predictions assets each pass spec).

* Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run python -m arf.scripts.verificators.verify_answer_asset tasks/t0102_seedscale_n4_gen20/assets/answer/t0102_joint_pass_recovery`;
  expected exit code 0. This confirms REQ-11 (the answer asset is structurally valid and addresses
  the canonical question).

* Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0102_seedscale_n4_gen20 -- uv run python -m arf.scripts.verificators.verify_machines_destroyed t0102_seedscale_n4_gen20`;
  expected exit code 0. This confirms REQ-15 (the Vast.ai instance was destroyed and
  `results/remote_machines_used.json` records it).

* Inspect `tasks/t0102_seedscale_n4_gen20/results/costs.json` and confirm the `total_usd` field is
  less than or equal to 8.00. Command: `jq '.total_usd' tasks/t0102_*/results/costs.json`; expected
  output: a numeric value <= 8.00. This confirms REQ-6 (hard $8 cap).

* Inspect `tasks/t0102_seedscale_n4_gen20/results/data/cross_seed_summary.json` and confirm it
  contains a 5x5 anchor distribution table (5 anchors x {seed44, seed55, t0091, t0099, baseline})
  and a `strict_joint_pass_count` field per seed. Command:
  `jq '.anchor_distribution | keys' tasks/t0102_*/results/data/cross_seed_summary.json`; expected
  output includes `["seed44", "seed55", "t0091", "t0099", "baseline"]`. This confirms REQ-12.

* Inspect `tasks/t0102_seedscale_n4_gen20/results/images/` and confirm at least two PNG files exist.
  Command: `ls tasks/t0102_*/results/images/*.png | wc -l`; expected output: at least 2. This
  confirms REQ-14.

* Confirm REQ-* coverage end-to-end by re-running `verify_plan` (above) and reading the plan itself
  — every REQ-1 through REQ-16 must map to at least one numbered step in `## Step by Step`. The
  verificator's PL-W007 warning fires if any `REQ-*` is absent from Step by Step.
