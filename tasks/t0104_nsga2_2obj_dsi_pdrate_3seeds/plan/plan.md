---
spec_version: "2"
task_id: "t0104_nsga2_2obj_dsi_pdrate_3seeds"
date_completed: "2026-05-12"
status: "complete"
---
# Plan: 68-d 2-Objective (DSI + PD-rate) NSGA-II at 3 Random-Init GA Seeds with DSI-Silence Guard

## Objective

Re-run the t0102 [t0102_seedscale_n4_gen20] 68-d Bed B + morphology NSGA-II substrate (54-d
electrophys + 14-d morphology) with three surgical changes: (1) drop the robustness objective so the
pymoo F-row becomes `[-dsi, -pd]` (`n_obj` 3 -> 2); (2) bump the GA-restart count from 2 (seeds 44,
55\) to 3 (seeds 44, 55, 66), all random-LHS init; (3) inject a silenced-cell DSI guard into
`evaluator.py` that returns DSI = 0.0 when the cell's total mean spike count across the 16
directions is below 10, eliminating the floating-point artifact that placed 27 t0102 cells at a
spurious DSI = 1.0. All other knobs match t0102 exactly: `N_EVAL_SEEDS = 4`, `n_gen = 20`,
`pop = 96`, no warm-start, single Vast.ai EPYC 7B13 64-core instance in Norway at $0.24/hr target,
seeds executed sequentially. Success criteria: produce 3 predictions assets (one per GA seed, ~2,016
cells each = 96 LHS + 20 generations x 96) and 1 answer asset answering the canonical question "Does
2-objective NSGA-II (DSI + PD-rate, with the DSI-silence guard applied) recover joint-pass cells
where t0102's 3-objective run found zero?". Both a positive (>= 1 strict joint-pass cell) and a
negative (0 cells across all 3 seeds) result are publishable. Cost cap: $15 hard (explicit per-task
override above the $8 project default), expected spend $10-12.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/task.json` and the resolved long
description at `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/task_description.md`:

```text
Name: 68-d 2-objective (DSI + PD-rate) NSGA-II at GA seeds=3, N=4, gens=20

Short description: Re-run t0102's 68-d NSGA-II with the robustness objective dropped: 3
random-init GA seeds (44/55/66), N_EVAL=4, gens=20, pop=96, DSI-silence guard applied. $15
hard cap.

Expected assets: 3 predictions, 1 answer.

Long description (excerpts):
* Fork t0102's code/ substrate verbatim.
* Objective vector: 3 -> 2 (drop robustness; keep DSI vector-sum + PD-rate). Robustness must
  remain in CellEvalResult and predictions schema for analysis, but must not enter NSGA-II
  selection.
* Patch evaluator._summarise_trials so DSI returns 0.0 when total mean spike count across 16
  directions < 10 (SILENCE_SPIKE_COUNT_THRESHOLD = 10). Add a module-level constant near
  worker globals.
* Reduce evaluator.BedBV3MorphProblem n_obj from 3 to 2; drop -result.robustness from F-row
  at evaluator.py:471 and -WORST_CASE_ROBUSTNESS at evaluator.py:477.
* nsga2_driver.py: 2-element HV ref point (line 109); drop "robustness" from saved dicts
  (lines 149, 307); drop HV_UTOPIA_ROBUSTNESS import (line 46) and config entry (line 224).
* GA seeds: 3 (44, 55, 66) random-LHS init; pop=96; n_gen=20; N_EVAL_SEEDS=4; sequential on
  one Vast.ai instance.
* Cost watchdog: per-seed $4 watchdog; wire watchdog trip directly into Vast.ai instance
  teardown via try/finally in nsga2_driver loop (S-0102-08 partial fix). Total hard cap:
  $15.
* Unit test: code/test_evaluator_dsi_guard.py with all-zero direction counts asserts DSI =
  0.0 (not 1.0). Run in smoke gate before scaling out.
* Expected assets: 3 predictions (one per seed, each ~2,016 cells) + 1 answer
  (joint-pass-recovery question).
* Out of scope: IBEA replacement (S-0102-03), Dang pop >=290 (S-0102-04), sign-averaging
  (S-0102-07), anchor lineage trace (S-0102-05), calcium-clearance sweep (S-0102-06),
  N_SEEDS default change (S-0101-02), Poleg-Polsky summary correction (S-0101-01).
```

Concrete requirements decomposed (each item names the step that satisfies it and the evidence that
proves completion):

* **REQ-1** — Patch `BedBV3MorphProblem.__init__` keyword dict at `evaluator.py:455` so `"n_obj"`
  changes from `3` to `2`. Satisfied by step 3. Evidence:
  `grep -n '"n_obj": 2' tasks/t0104_*/code/evaluator.py` returns line 455 (or thereabouts) and no
  matching `"n_obj": 3` remains.
* **REQ-2** — Drop `-result.robustness` from the F-row at `evaluator.py:471` and
  `-WORST_CASE_ROBUSTNESS` from the failure-fallback F-row at `evaluator.py:477`. The CellEvalResult
  dataclass keeps the `robustness` field (computed in `_summarise_trials` lines 335-344). Satisfied
  by step 3. Evidence: in `tasks/t0104_*/code/evaluator.py`, the F-row construction at line ~471
  reads `np.array([-result.dsi_vector_sum, -result.pd_rate_hz], dtype=np.float64)` and the fallback
  at line ~477 reads `np.array([-WORST_CASE_DSI, -WORST_CASE_PD_RATE_HZ], ...)`. Neither contains
  the third entry.
* **REQ-3** — Inject the silenced-cell DSI guard into `evaluator.py._summarise_trials` between the
  spike-count-loop close (line 308 in t0102) and the first `_vector_sum_dsi` call (line 325).
  Threshold constant `SILENCE_SPIKE_COUNT_THRESHOLD: float = 10.0` declared near the worker globals
  (lines 105-108). The guard computes total mean spikes across the 16 directions and forces
  `dsi_vector_sum = 0.0` when the total is below threshold. The per-seed `_vector_sum_dsi` call at
  line 332 keeps the raw helper so per-seed robustness DSI is unaffected. Satisfied by step 3.
  Evidence: `grep -n 'SILENCE_SPIKE_COUNT_THRESHOLD' tasks/t0104_*/code/evaluator.py` returns the
  named constant and at least one usage inside `_summarise_trials`.
* **REQ-4** — Shrink the HV reference point in `nsga2_driver.py:109` from a 3-element array
  `np.array([0.0, 0.0, 0.0])` to a 2-element array `np.array([0.0, 0.0])` matching the new 2-column
  population F matrix. Satisfied by step 4. Evidence: in `tasks/t0104_*/code/nsga2_driver.py`, the
  `_compute_hv` function at line ~109 constructs a 2-element ref point.
* **REQ-5** — Drop the `"robustness": float(-f_row[2])` entry from both saved dicts in
  `nsga2_driver.py`: the per-generation evaluation record at line 149 (`_save_iteration`) and the
  Pareto-front cell dump at line 307 (`run_nsga2_for_seed`). Robustness still exists per-cell in the
  predictions assets via the unchanged `CellEvalResult.robustness`. Satisfied by step 4. Evidence:
  `grep -n '"robustness"' tasks/t0104_*/code/nsga2_driver.py` returns no matches.
* **REQ-6** — Drop the `HV_UTOPIA_ROBUSTNESS` import at `nsga2_driver.py:46` and the corresponding
  entry written to `algorithm_config.json` in `_save_algorithm_config` at line 224. Also drop
  `HV_UTOPIA_ROBUSTNESS` from `__all__` in `constants.py:25` so downstream accidental references
  fail-fast. Satisfied by steps 2 and 4. Evidence:
  `grep -n 'HV_UTOPIA_ROBUSTNESS' tasks/t0104_*/code/` returns no matches.
* **REQ-7** — Author `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/test_evaluator_dsi_guard.py`
  with at least three pytest cases: (a) all-zero direction counts across 16 dirs x 4 seeds asserts
  `_summarise_trials(...).dsi_vector_sum == 0.0` (not 1.0); (b) near-silent cell with total mean
  spikes ~ 1.25 across directions asserts guard floor returns 0.0; (c) firing positive control with
  total mean spikes >= 25 asserts the guard does NOT trigger and DSI is computed normally. Run the
  test locally before the Vast.ai smoke gate and again as part of the on-instance smoke gate.
  Satisfied by step 6. Evidence: `uv run pytest tasks/t0104_*/code/test_evaluator_dsi_guard.py -v`
  exits 0 with 3+ passing tests; the local smoke-gate log
  `logs/steps/<idx>_setup-machines/smoke_gate_local.json` records `dsi_guard_unit_test: pass`.
* **REQ-8** — Wire the cost-watchdog trip directly into Vast.ai instance teardown by wrapping the
  body of `run_nsga2_for_seed` in `try/finally`. In the `finally` block, when
  `cost_watchdog.tripped is True` OR all gens complete, invoke the Vast.ai teardown subprocess
  (`vastai destroy instance <id>`) gated behind an explicit `--teardown-on-watchdog` flag default
  `False` so smoke gate and local runs do not destroy anything. This is the S-0102-08 partial fix
  and removes the t0102 $3.51 idle leak. Satisfied by step 4. Evidence:
  `grep -n 'try:' tasks/t0104_*/code/nsga2_driver.py` shows a `try` block wrapping the body of
  `run_nsga2_for_seed`; `grep -n 'teardown_on_watchdog' tasks/t0104_*/code/nsga2_driver.py` shows
  the flag.
* **REQ-9** — Run NSGA-II at `task_seed = 44`, `task_seed = 55`, `task_seed = 66` sequentially on
  a single Vast.ai instance, each with `pop = 96`, `n_gen = 20`, `N_EVAL_SEEDS = 4`, random-LHS
  init, no warm-start. Satisfied by steps 12, 13, 14. Evidence:
  `results/data/nsga2_seed44_history.json`, `results/data/nsga2_seed55_history.json`, and
  `results/data/nsga2_seed66_history.json` all exist and record `pop_size: 96`, `n_gen: 20`,
  `n_eval_seeds: 4`, and distinct seed values.
* **REQ-10** — Build 3 predictions assets (one per GA seed) at
  `tasks/t0104_*/assets/predictions/nsga2-seed44-bedb-morph-n4-gen20-2obj/`,
  `nsga2-seed55-bedb-morph-n4-gen20-2obj/`, and `nsga2-seed66-bedb-morph-n4-gen20-2obj/`. Each asset
  contains the full per-cell history (96 LHS init + 20 generations x 96 = 2,016 cells minus any
  early-terminated generations). Per-cell JSONL retains the `robustness` field even though the axis
  was dropped from NSGA-II selection. Satisfied by step 17. Evidence:
  `uv run python -m arf.scripts.verificators.verify_predictions_asset tasks/t0104_*/assets/predictions/nsga2-seed44-bedb-morph-n4-gen20-2obj`
  exits 0 (and the same for seeds 55, 66).
* **REQ-11** — Total cost in `results/costs.json` must not exceed $15.00. Per-seed cap $4.00
  enforced by `cost_watchdog.py`; orchestrator-level $15 cap enforced as an additional check.
  Satisfied by steps 11, 12, 13, 14, 16. Evidence:
  `jq '.total_usd' tasks/t0104_*/results/costs.json` returns a numeric value <= 15.00.
* **REQ-12** — Produce 1 answer asset
  `tasks/t0104_*/assets/answer/t0104_joint_pass_recovery_2obj/` answering "Does 2-objective NSGA-II
  (DSI + PD-rate, with the DSI-silence guard applied) recover joint-pass cells where t0102's
  3-objective run found zero?" with strict joint-pass defined as DSI >= 0.5 AND PD-rate >= 30 Hz on
  the guard-cleaned DSI. Cites t0102, t0099, t0091, PolegPolsky2026, Druckmann2007, Hay2011 as
  supporting evidence. Satisfied by step 19. Evidence:
  `uv run python -m arf.scripts.verificators.verify_answer_asset tasks/t0104_*/assets/answer/t0104_joint_pass_recovery_2obj`
  exits 0.
* **REQ-13** — Smoke gate at `N_EVAL_SEEDS = 4` with the DSI guard active and `n_obj = 2` must
  pass before any long NSGA-II run on the Vast.ai instance. The gate re-evaluates 5 anchors against
  the t0093 60-cell post-fix fingerprint and asserts DSI within 0.05 and PD-rate within 1 Hz of the
  anchors. The DSI guard does not affect the 5 t0083-best anchors (they fire well above the 10-spike
  threshold). Satisfied by steps 10 and 12. Evidence:
  `logs/steps/<idx>_setup-machines/smoke_gate_local.json` and
  `logs/steps/<idx>_setup-machines/smoke_gate_remote.json` both record `pass: true` and PD-rates
  within tolerance for all 5 anchors.
* **REQ-14** — Quantify the DSI-guard impact: count cells in each seed at the guard floor (DSI =
  0.0 because total mean spikes < 10) and confirm the Pareto front no longer contains DSI = 1.0 / PD
  = 0 cells. Side-by-side reanalyse t0102's seed44 predictions with the new guard applied post-hoc
  to identify how many of the 27 t0102 DSI = 1.0 cells would have been masked. Satisfied by step 18.
  Evidence: `results/data/dsi_guard_impact.json` exists with per-seed counts at the guard floor and
  a t0102-reanalysis count.
* **REQ-15** — Compute metrics over Pareto cells and write `results/metrics.json` in the explicit
  multi-variant format with one variant per GA seed (`seed44`, `seed55`, `seed66`), each populating
  the four registered metric keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse`. Read
  `arf/specifications/metrics_specification.md` for the exact JSON schema. Satisfied by step 18.
  Evidence: `jq '.variants | keys' tasks/t0104_*/results/metrics.json` prints
  `["seed44", "seed55", "seed66"]` and each variant contains the four registered metric keys.
* **REQ-16** — Generate at least 3 charts in `results/images/`: (a) HV trajectory over generations
  comparing the 3 seeds against t0102 (3-obj) and t0099 (3-obj N=20) hypervolumes restricted to the
  (DSI, PD) plane; (b) DSI vs PD scatter colour-coded by anchor + joint-pass corner overlay; (c)
  anchor distribution heatmap across the 3 seeds. Satisfied by step 18. Evidence:
  `results/images/hv_trajectory.png`, `results/images/dsi_vs_pd_scatter.png`,
  `results/images/anchor_distribution_heatmap.png` exist.
* **REQ-17** — Destroy the Vast.ai instance within 5 minutes of last seed completion; record final
  cost in `results/costs.json` and `results/remote_machines_used.json`. Satisfied by step 16.
  Evidence:
  `uv run python -m arf.scripts.verificators.verify_machines_destroyed t0104_nsga2_2obj_dsi_pdrate_3seeds`
  exits 0.
* **REQ-18** — Do not modify any prior task folder (immutability). Only files under
  `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/` plus the allowlisted top-level tooling files
  (`pyproject.toml`, `uv.lock`, `ruff.toml`, `.gitignore`, `mypy.ini`) may change. Satisfied
  implicitly. Evidence: post-task `git diff main -- tasks/ | head` shows changes only under
  `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/`.

* * *

## Approach

### Technical approach

The task forks t0102's [t0102_seedscale_n4_gen20] `code/` substrate verbatim and applies the three
patches enumerated above. Per `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/research/research_code.md`,
the patch sites are documented at exact line numbers in t0102's source files (`evaluator.py` 480
lines, `nsga2_driver.py` 368 lines, `cost_watchdog.py` 127 lines, `constants.py` 91 lines). The 68-d
substrate splits `[54 electrophys | 14 morphology]`; per-cell evaluation reuses cached cells keyed
on the 14-d morphology hash, with `apply_parameter_vector` re-running on electrophys-only changes.
NSGA-II runs via pymoo with `StarmapParallelization` over
`multiprocessing.Pool(processes=min(60, cpu_count()-4))`. Each generation runs
`pop_size * N_EVAL_SEEDS * n_directions = 96 * 4 * 16 = 6,144` trials.

The DSI-silence guard goes into `_summarise_trials` (between t0102's lines 308 and 325), not into
`_vector_sum_dsi` itself. This placement is load-bearing: the per-seed call at line 332 reuses
`_vector_sum_dsi` with single-element spike-count lists (by construction < 16 spikes per direction),
and adding the guard there would silently force most per-seed DSIs to 0 and break the robustness
signal even when the cell is firing well. The constant `SILENCE_SPIKE_COUNT_THRESHOLD: float = 10.0`
lives near the worker globals at the top of `evaluator.py`.

The robustness field stays inside `CellEvalResult` (declared at line 95 of t0102's evaluator) and is
populated unchanged by `_summarise_trials` lines 335-344, so the predictions assets retain it for
post-hoc analysis. Only the pymoo F-row drops the `-result.robustness` entry. The driver-level
cost-watchdog teardown wires into the `finally` block of `run_nsga2_for_seed`; this is preferred
over the watchdog-level callback variant because it co-locates with the existing
`pool.close()/pool.terminate()` calls at driver lines 322-323.

GA seeds are 44, 55, 66 — seeds 44 and 55 are reused from t0102 so the 2-obj vs 3-obj comparison
is an apples-to-apples lift at the same LHS init, with 66 as the genuinely fresh sample. All three
seeds run sequentially on one Vast.ai EPYC 7B13 64-core instance in Norway at $0.24/hr.

Concrete file-level strategy: copy every code file from `tasks/t0102_seedscale_n4_gen20/code/` into
`tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/` (cross-task import is forbidden for non-library
code), rewrite the self-imports from `tasks.t0102_*` to `tasks.t0104_*`, then edit:

1. `evaluator.py` — add `SILENCE_SPIKE_COUNT_THRESHOLD = 10.0` constant; inject the guard in
   `_summarise_trials` between lines 308 and 325; drop `-result.robustness` from F-row line 471 and
   `-WORST_CASE_ROBUSTNESS` from fallback line 477; change `"n_obj": 3` to `"n_obj": 2` at line 455.

2. `nsga2_driver.py` — shrink HV ref point to 2 entries (line 109); drop `"robustness"` from
   `_save_iteration` line 149 and from Pareto-cell dump line 307; drop `HV_UTOPIA_ROBUSTNESS` import
   (line 46) and `_save_algorithm_config` entry (line 224); wrap the body of `run_nsga2_for_seed` in
   `try/finally` for the teardown hook.

3. `constants.py` — rename `T0102_SEEDS` to `T0104_SEEDS = (44, 55, 66)`, update the length
   assertion to `== 3`, raise `T0104_TASK_BUDGET_TOTAL_USD` to `12.00` (3 x $4 + small idle margin
   under the $15 cap), drop `HV_UTOPIA_ROBUSTNESS` from `__all__`.

4. `cost_watchdog.py` — rename the symbol `T0102_HARD_BUDGET_USD` to `T0104_HARD_BUDGET_USD`
   (value $4.00 unchanged); update intervention md text to reference t0104.

5. `generator_wrapper.py`, `paths.py`, `smoke_gate.py`, `anchor_classifier.py`,
   `anchor_definitions.py`, `build_assets.py`, `cross_seed_analysis.py`, `metrics_builder.py`,
   `per_seed_analysis.py`, `bootstrap.py`, `random_init.py`, `hv_plateau_watchdog.py`,
   `recorder.py`, `trial_helpers.py`, `apply_params.py`, `parametric_placer.py`,
   `build_cell_ais.py`, `extend_with_ais.py`, `biological_priors.py`, `biological_scorecard.py`,
   `build_morphology_charts.py`, `run_local_analysis.py`, `sync_results_back.sh` — copy verbatim;
   rewrite the `tasks.t0102_seedscale_n4_gen20.code.*` self-imports to
   `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.*`.

6. `run_three_seeds.sh` — adapt t0102's `run_two_seeds.sh` loop from `(44, 55)` to `(44, 55, 66)`;
   re-anchor module paths to t0104.

7. `test_evaluator_dsi_guard.py` — NEW pytest module (~80 lines) with the three test cases
   described in REQ-7.

### Alternative approaches considered

* **Inject the silence guard inside `_vector_sum_dsi` instead of `_summarise_trials`**. Rejected:
  the per-seed call at evaluator.py:332 would inherit the guard and force most per-seed DSIs to 0.0,
  silently breaking the robustness signal that we still want to compute and store for post-hoc
  analysis. The research_code.md call this out explicitly as Lesson Learned 5.

* **Use a watchdog-level teardown callback instead of a driver-level `try/finally`**. Rejected: the
  watchdog-level option requires changing `CostWatchdog`'s public surface and threading the
  `teardown_callback` through `make_watchdog_from_machine_log`. The driver-level hook is lower-risk,
  co-locates teardown with the existing `pool.close()/pool.terminate()` cleanup, and preserves the
  watchdog as a pure decision component.

* **Run 4 GA seeds (44, 55, 66, 77) for tighter variance estimates at $0.24/hr Norway**. Rejected:
  the researcher's brainstorm-session-22 directive explicitly authorized 3 seeds at a $15 cap. Three
  seeds give us a 3-point variance estimate while keeping the projected spend at $10-12 with $3-5 of
  cap headroom. A 4th seed would push expected spend to ~$13-14 and leave no margin for the per-seed
  cost watchdog overshoot characteristic of NEURON memory accumulation.

* **Parallelise the three GA seeds across three Vast.ai instances** to slash wall-clock from ~32h to
  ~~12h. Rejected: 3x provisioning overhead (~~$0.75 + 30 min total setup) plus 3x sync-back cost
  would push the spend toward $13-14 and leave no margin under the $15 cap. Sequential
  single-instance is the budget-safe choice and matches t0102's proven topology.

* **Defer the DSI-silence guard to a follow-up correction task** and run 2-obj at 3 seeds first.
  Rejected: the silence-corner artifact (27 t0102 cells at DSI = 1.0) dominated t0102's Pareto front
  and NSGA-II crowding distance preserved that corner across generations. Without the guard,
  dropping robustness alone would re-produce the same artifact in the t0104 Pareto front and
  confound the joint-pass count. The guard is independently load-bearing.

### Task types

`task.json` already lists `task_types: ["experiment-run", "data-analysis", "answer-question"]`,
which matches the work this task does:

* **experiment-run** Planning Guidelines: define hypothesis (2-objective NSGA-II + DSI-silence guard
  recovers joint-pass cells where 3-objective did not), enumerate independent variables (GA seed,
  objective count, DSI guard), dependent variables (joint-pass count, DSI, PD, HV trajectory, anchor
  distribution), estimate costs and set a cap ($15), identify baselines (t0102 null at 3-obj 2
  seeds; t0099 null at 3-obj 3 seeds N=20; t0091 single warm-start joint-pass). Multi-condition: use
  the explicit multi-variant `metrics.json` format with one variant per GA seed (`seed44`, `seed55`,
  `seed66`).

* **data-analysis** Planning Guidelines: list all metrics and chart types upfront (HV trajectory in
  the (DSI, PD) plane, DSI vs PD scatter, anchor distribution heatmap, DSI-guard impact histogram),
  state statistical tests (joint-pass yield Wilson 95% upper-CI vs t0102's 0/2,592 null),
  pre-declare per-subset breakdowns (per-seed, per-anchor, per-DSI-bin).

* **answer-question** Planning Guidelines: define the canonical question text (REQ-12), name the
  evidence channels (new NSGA-II runs + post-hoc reanalysis of t0102's predictions + cross-task
  comparison to t0099/t0091 + literature framing from PolegPolsky2026/Druckmann2007/Hay2011), set
  the stopping criterion for the answer (all 3 seeds completed OR cost watchdog tripped with
  intervention recorded).

### Registered-metric coverage

The project registers 4 metrics in `meta/metrics/`: `direction_selectivity_index` (best DSI over the
Pareto front per seed), `tuning_curve_hwhm_deg` (median HWHM over strict-pass cells, or median over
the full Pareto if zero strict-pass), `tuning_curve_reliability` (median Pearson rho over the 4
noise replicates per cell, averaged over the Pareto front), `tuning_curve_rmse` (best RMSE over the
Pareto front; the primary RMSE-aligned optimisation objective). All four apply per Pareto cell in
this task — every evaluated cell produces a tuning curve and a DSI. They are reported as
per-variant (per-GA-seed) summary statistics. Concrete measurement plan in step 18. The two
efficiency metrics `efficiency_inference_time_per_item_seconds` and
`efficiency_inference_cost_per_item_usd` are not currently registered in `meta/metrics/`; if added
later, they map naturally to per-cell evaluation time and per-cell Vast.ai cost. The task does not
train a model so `efficiency_training_time_seconds` does not apply.

* * *

## Cost Estimation

| Item | Quantity | Rate | Subtotal |
| --- | --- | --- | --- |
| Vast.ai instance (EPYC 7B13 64-core, Norway preferred) productive compute | ~30 h | $0.24/hr | ~$7.20 |
| Provisioning + SCP + remote smoke gate | ~1 h | $0.24/hr | ~$0.24 |
| Per-seed buffer for NEURON memory-leak slowdown | ~6 h | $0.24/hr | ~$1.44 |
| Idle-to-teardown margin (S-0102-08 wired) | ~0.1 h | $0.24/hr | ~$0.03 |
| LLM API calls (planning, analysis, answer-asset writing) | n/a | n/a | $0.00 (in-harness) |
| **Subtotal expected** |  |  | **~$8.91** |
| Headroom for instance-price drift to $0.30/hr | ~10 h | $0.06/hr | ~$0.60 |
| **Total expected (with drift headroom)** |  |  | **~$10-12** |
| **Hard per-task cap (explicit override)** |  |  | **$15.00** |
| **Per-seed cap (cost_watchdog.py)** |  |  | **$4.00** |

Per-seed cap is set at $4.00 in `T0104_HARD_BUDGET_USD`, so even if cost watchdog triggers on each
of the 3 seeds at exactly $4.00 ($12 productive total), the orchestrator-level $15 cap leaves $3 of
margin for provisioning and idle teardown.

Project-wide budget context: total project budget $50 (raised from $35 immediately prior to this
task via commit `388e8557` on main); current remaining $14.02 before stop-threshold. The $15 hard
per-task cap is an explicit researcher override above the $8 project default
`per_task_default_limit` in `project/budget.json`; this is recorded in
`tasks/t0104_*/task_description.md`. If actual spend exceeds $14.02 the project hits its 100%
stop-threshold and the orchestrator must record an intervention.

* * *

## Step by Step

### Milestone 1: Local code preparation (no cost)

1. **Copy the t0102 substrate into the t0104 code folder.** Run `cp` of every Python file (plus
   `run_two_seeds.sh`) under `tasks/t0102_seedscale_n4_gen20/code/` into
   `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/`. Files to copy: `bootstrap.py`, `evaluator.py`,
   `nsga2_driver.py`, `cost_watchdog.py`, `generator_wrapper.py`, `random_init.py`, `smoke_gate.py`,
   `hv_plateau_watchdog.py`, `trial_helpers.py`, `apply_params.py`, `parametric_placer.py`,
   `build_cell_ais.py`, `extend_with_ais.py`, `recorder.py`, `anchor_definitions.py`,
   `anchor_classifier.py`, `per_seed_analysis.py`, `biological_priors.py`,
   `biological_scorecard.py`, `cross_seed_analysis.py`, `metrics_builder.py`, `build_assets.py`,
   `build_morphology_charts.py`, `run_local_analysis.py`, `sync_results_back.sh`, `constants.py`,
   `constants_electrophys.py`, `constants_morphology.py`, `paths.py`, `run_two_seeds.sh`. Rewrite
   every `tasks.t0102_seedscale_n4_gen20.code.*` self-import to
   `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.*` via a single `sed -i` pass and confirm with
   `grep -rn 'tasks.t0102_seedscale_n4_gen20' tasks/t0104_*/code/` returning no matches. Inputs:
   t0102 code/. Outputs: identical files under `tasks/t0104_*/code/` with rewritten imports.
   Expected observable output: `ls tasks/t0104_*/code/*.py | wc -l` >= 28. Satisfies REQ-9 prep,
   REQ-18.

2. **Edit `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/constants.py`.** Rename `T0102_SEEDS` to
   `T0104_SEEDS: tuple[int, ...] = (44, 55, 66)`. Update the length assertion at the bottom of the
   seed block to `assert len(T0104_SEEDS) == 3, f"expected 3 seeds, got {len(T0104_SEEDS)}"`. Rename
   `T0102_HARD_BUDGET_PER_SEED_USD` to `T0104_HARD_BUDGET_PER_SEED_USD: float = 4.00`. Rename
   `T0102_TASK_BUDGET_TOTAL_USD` to `T0104_TASK_BUDGET_TOTAL_USD: float = 12.00` (3 x $4 with small
   idle margin under the $15 orchestrator cap). Drop `HV_UTOPIA_ROBUSTNESS` from `__all__` at line
   25 of t0102's constants.py. Inputs: copied constants.py. Outputs: edited file. Expected
   observable output:
   `grep -n 'T0104_SEEDS\|T0104_HARD_BUDGET_PER_SEED_USD\|T0104_TASK_BUDGET_TOTAL_USD' tasks/t0104_*/code/constants.py`
   shows the three constants with values `(44, 55, 66)`, `4.00`, `12.00`.
   `grep -n 'HV_UTOPIA_ROBUSTNESS' tasks/t0104_*/code/constants.py` returns no matches in `__all__`.
   Satisfies REQ-6 (constants part), REQ-9 (seeds), REQ-11 (budget).

3. **Edit `tasks/t0104_*/code/evaluator.py` for the 3 evaluator-level patches.** Open the copied
   480-line file. (a) Near the worker globals (lines 105-108) add a new module-level constant
   `SILENCE_SPIKE_COUNT_THRESHOLD: float = 10.0` with a docstring comment citing S-0102-01. (b)
   Inside `_summarise_trials` (lines 290-355), between the `spike_counts_per_dir` build-loop close
   (line 308) and the first `_vector_sum_dsi` call (line 325), compute the per-direction mean spike
   counts via `np.mean(counts)` for each direction's count list and sum them; if the sum is below
   `SILENCE_SPIKE_COUNT_THRESHOLD`, force `dsi_vector_sum = 0.0` and skip the `_vector_sum_dsi`
   call; otherwise proceed unchanged. Do NOT add the guard to the per-seed call at line 332. (c) In
   `BedBV3MorphProblem._evaluate` (lines 466-480), change line 471 from
   `out["F"] = np.array([-result.dsi_vector_sum, -result.pd_rate_hz, -result.robustness], dtype=np.float64)`
   to `out["F"] = np.array([-result.dsi_vector_sum, -result.pd_rate_hz], dtype=np.float64)`, and
   line 477 from
   `out["F"] = np.array([-WORST_CASE_DSI, -WORST_CASE_PD_RATE_HZ, -WORST_CASE_ROBUSTNESS], ...)` to
   `out["F"] = np.array([-WORST_CASE_DSI, -WORST_CASE_PD_RATE_HZ], ...)`. Drop the
   `WORST_CASE_ROBUSTNESS` import from the top of the file. (d) In `BedBV3MorphProblem.__init__`
   keyword dict at line 455, change `"n_obj": 3` to `"n_obj": 2`. The `CellEvalResult.robustness`
   field at line 95 stays unchanged; the `_summarise_trials` robustness computation at lines 335-344
   stays unchanged. Inputs: copied evaluator.py. Outputs: edited file. Expected observable output:
   `grep -n 'SILENCE_SPIKE_COUNT_THRESHOLD' tasks/t0104_*/code/evaluator.py` shows the constant
   definition and at least one usage; `grep -n '"n_obj"' tasks/t0104_*/code/evaluator.py` shows
   `"n_obj": 2`;
   `grep -n 'WORST_CASE_ROBUSTNESS\|result.robustness' tasks/t0104_*/code/evaluator.py` returns
   matches only for the per-cell summary write, not for the F-row construction. Satisfies REQ-1,
   REQ-2, REQ-3.

4. **Edit `tasks/t0104_*/code/nsga2_driver.py` for the 4 driver-level patches.** Open the copied
   368-line file. (a) In `_compute_hv` (lines 108-113) change line 109 from
   `ref_point = np.array([0.0, 0.0, 0.0], dtype=np.float64)` to
   `ref_point = np.array([0.0, 0.0], dtype=np.float64)`. (b) In `_save_iteration` (lines 141-151)
   delete the `"robustness": float(-f_row[2]),` line at line 149. (c) In the Pareto-front cell dump
   inside `run_nsga2_for_seed` (lines 297-309) delete the `"robustness": float(-f_row[2]),` line at
   line 307. (d) Drop the `from .constants import HV_UTOPIA_ROBUSTNESS` import line at line 46 and
   delete the corresponding `"hv_utopia_robustness": HV_UTOPIA_ROBUSTNESS,` entry in
   `_save_algorithm_config` at line 224. (e) Wrap the body of `run_nsga2_for_seed` in a single
   `try/finally`; in the `finally` block, when `cost_watchdog.tripped is True` OR
   `algorithm.has_next() is False`, invoke a Vast.ai teardown subprocess gated behind a new
   module-level flag `TEARDOWN_ON_WATCHDOG: bool = False` (default False so the smoke gate and local
   runs do not destroy anything); read the instance ID from the same `machine_log.json` that
   `make_watchdog_from_machine_log` already reads at lines 238-242. Inputs: copied nsga2_driver.py.
   Outputs: edited file. Expected observable output:
   `grep -n 'np.array(\[0.0, 0.0\]' tasks/t0104_*/code/nsga2_driver.py` returns the new ref-point
   line; `grep -n '"robustness"' tasks/t0104_*/code/nsga2_driver.py` returns no matches;
   `grep -n 'HV_UTOPIA_ROBUSTNESS' tasks/t0104_*/code/nsga2_driver.py` returns no matches;
   `grep -n 'TEARDOWN_ON_WATCHDOG' tasks/t0104_*/code/nsga2_driver.py` returns the flag definition
   and at least one usage; `grep -n 'try:' tasks/t0104_*/code/nsga2_driver.py` shows the wrapping
   `try` block. Satisfies REQ-4, REQ-5, REQ-6, REQ-8.

5. **Edit `tasks/t0104_*/code/cost_watchdog.py` and `run_two_seeds.sh -> run_three_seeds.sh`.**
   Rename the symbol `T0102_HARD_BUDGET_USD` in `cost_watchdog.py` to `T0104_HARD_BUDGET_USD`
   (numeric value $4.00 unchanged). Update the intervention md text to reference t0104. Rename
   `run_two_seeds.sh` to `run_three_seeds.sh` and change the `for SEED in 44 55` loop to
   `for SEED in 44 55 66`; swap any remaining `tasks.t0102_*` module-path strings inside the script
   to `tasks.t0104_*`. Add the `--teardown-on-watchdog` flag to the `python -m` invocation of the
   driver inside the loop so the production path uses the new teardown hook. Inputs: copied
   cost_watchdog.py, run_two_seeds.sh. Outputs: edited cost_watchdog.py, new run_three_seeds.sh.
   Expected observable output: `bash -n tasks/t0104_*/code/run_three_seeds.sh` exits 0;
   `grep 'for SEED' tasks/t0104_*/code/run_three_seeds.sh` shows `for SEED in 44 55 66`. Satisfies
   REQ-8 (driver flag wiring), REQ-9 (seeds), REQ-11 (per-seed cap symbol).

6. **Author `tasks/t0104_*/code/test_evaluator_dsi_guard.py`.** Create a NEW pytest module (~80
   lines) importing the locally-edited `_summarise_trials` and `CellEvalResult` from
   `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.evaluator`. Define three test functions:
   `test_all_silent_returns_dsi_zero` — build a synthetic list of TrialResult-like objects with
   all 16 directions x 4 noise seeds at `spike_count = 0`; call
   `_summarise_trials(results=trials, n_seeds=4)`; assert `result.dsi_vector_sum == 0.0`.
   `test_near_silent_at_one_point_two_five_total_mean_returns_zero` — build trials with total mean
   spike count across directions ~ 1.25 (well below 10); assert `result.dsi_vector_sum == 0.0`.
   `test_firing_positive_control_returns_nonzero` — build trials with total mean spike count >= 25
   (above threshold) distributed asymmetrically (e.g., 20 spikes in one direction, 5 spread across
   the other 15); assert `result.dsi_vector_sum > 0.0` (the guard does NOT trigger and the raw
   `_vector_sum_dsi` returns a finite DSI in (0, 1]). Use `@dataclass(frozen=True, slots=True)` for
   any synthetic TrialResult; do not use mocks. Inputs: edited evaluator.py. Outputs:
   `test_evaluator_dsi_guard.py`. Expected observable output:
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run pytest tasks/t0104_*/code/test_evaluator_dsi_guard.py -v`
   exits 0 with 3 passing tests. Satisfies REQ-7.

7. **Lint and type-check the task code folder.** Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run ruff check --fix tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code`
   then
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run ruff format tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code`
   then
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run mypy -p tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code`.
   This catches any stale `t0102_*` import path or constant reference missed in steps 1-5. Inputs:
   t0104 code/. Outputs: zero ruff errors / zero mypy errors. Expected observable output: all three
   commands exit 0. Satisfies REQ-18 (lint trips on any cross-task import accidentally
   re-introduced).

### Milestone 2: Smoke gate and remote provisioning

8. **[CRITICAL] Run the substrate-consistency smoke gate locally on Windows with the DSI guard
   active and `n_obj = 2`.** Execute
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run python -m tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.smoke_gate`.
   The gate re-evaluates the 5 t0083-best anchors against the t0093 60-cell post-fix verification
   fingerprint at PD-rate tolerance 1 Hz and DSI tolerance 0.05. Validation gate: this is the
   trivial baseline for "the pipeline is alive". If the smoke gate reports any anchor's bedb_like
   PD-rate outside `[anchor_pd - 1.0, anchor_pd + 1.0]` Hz, STOP and debug the import chain or the
   evaluator patch; do NOT proceed to Vast.ai provisioning. After a passing smoke gate, manually
   read the printed PD-rate for each of the 5 anchors and confirm all are within tolerance
   individually (not just the mean). Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run pytest tasks/t0104_*/code/test_evaluator_dsi_guard.py -v`
   again as part of the smoke gate and confirm 3 passing tests. Inputs: t0104 code/, t0093
   fingerprint JSON, MOD library from t0080. Outputs: stdout PD-rates,
   `logs/steps/<idx>_setup-machines/smoke_gate_local.json`. Expected observable output: all 5
   anchors within tolerance, `dsi_guard_unit_test: pass` recorded in the smoke gate log. Satisfies
   REQ-13 (local half).

9. **Provision one Vast.ai instance.** Target: AMD EPYC 7B13 64 effective cores, no GPU requirement
   (NEURON is CPU-bound), >= 200 GB RAM, Norway preferred for $0.24/hr pricing consistent with t0102
   / t0099. Record `selected_offer.price_per_hour` in
   `logs/steps/<idx>_setup-machines/machine_log.json`. Reject offers above $0.40/hr — if no Norway
   offer is available, fall back to any EPYC 7B13 below $0.40/hr (still fits $15 cap at 37 h
   runtime). Inputs: Vast.ai marketplace via setup-remote-machine skill. Outputs: `machine_log.json`
   with instance ID, IP, and hourly rate. Expected observable output: SSH handshake succeeds.
   Satisfies REQ-9 (instance), REQ-11.

10. **SCP the t0104 code/ and shared MOD library to the Vast.ai instance.** Use the
    setup-remote-machine sync utility to copy the entire `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/`
    plus the shared MOD library at
    `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/x86_64/` plus the t0093 fingerprint at
    `tasks/t0093_resweep_and_t0090_correction/results/data/`. Run `bootstrap.py` once on the remote
    machine to verify Linux `.so` resolution succeeds. Inputs: local repo. Outputs: remote repo
    mirror. Expected observable output:
    `ssh remote 'cd repo && uv run python -c "from tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code import bootstrap"'`
    exits 0. Satisfies REQ-9 (transport), REQ-18.

11. **[CRITICAL] Re-run the smoke gate on the Vast.ai instance.** Same command as step 8 but
    executed remotely, plus the pytest invocation for `test_evaluator_dsi_guard.py`. Validation
    gate: if the remote smoke gate fails (any of 5 anchors outside its 1 Hz / 0.05 DSI window) OR if
    the pytest invocation reports any failure, STOP. Do NOT launch any seed — the import chain is
    broken on the remote Linux environment or the evaluator patch is incorrect. Halt and debug:
    inspect individual PD-rate values and the bootstrap log, do not proceed to seed=44. Inputs:
    remote repo. Outputs: `logs/steps/<idx>_setup-machines/smoke_gate_remote.json`. Expected
    observable output: all 5 anchors within tolerance and 3 passing pytest tests. Satisfies REQ-13
    (remote half), REQ-7 (smoke-gate inclusion).

### Milestone 3: Long NSGA-II runs

12. **[CRITICAL] Run NSGA-II seed=44 on the Vast.ai instance.** Execute
    `bash tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/run_three_seeds.sh 44` (the script's
    per-seed branch). This launches
    `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.nsga2_driver.run_nsga2_for_seed(task_seed=44)`
    with pop=96, gens=20, N_EVAL_SEEDS=4, LHS init, n_obj=2, `--teardown-on-watchdog` set.
    Validation gate: this is an expensive operation (~10-12 hours, ~$2.40-3.00 of compute). Per-cell
    trivial baseline: the t0102 seed-44 best DSI of 0.49 at PD ~ 18 Hz. After generation 1 finishes
    (~30 minutes), pull back the generation-1 cell history and read 5 individual cells: confirm DSI
    values are in [0, 1] (not NaN), PD rates are non-negative, robustness values are in [0, 1]. If
    any DSI is NaN or PD is negative, halt and debug the evaluator patch. Sanity-check: zero cells
    should report DSI = 1.0 with PD = 0 (the guard removes the silence-corner artifact). The cost
    watchdog and HV-plateau watchdog are inside the termination collection and may stop the run
    early. Inputs: remote code/, morphology generator library, Bed B cell library. Outputs:
    `results/data/nsga2_seed44_history.json`, `results/data/nsga2_seed44_cost.json`,
    `logs/steps/<idx>_implementation/seed44_stdout.log`. Expected observable output: stdout
    "Termination reached at gen N" for some N in [10, 20]; per-seed cost <= $4.00. Satisfies REQ-9,
    REQ-11.

13. **[CRITICAL] Run NSGA-II seed=55 on the same Vast.ai instance.** Same command and validation
    gates as step 12 but with `task_seed=55`. Same gen-1 cell-history inspection requirement.
    Sanity-check identical to step 12. Inputs: remote code/. Outputs:
    `results/data/nsga2_seed55_history.json`, `results/data/nsga2_seed55_cost.json`,
    `logs/steps/<idx>_implementation/seed55_stdout.log`. Expected observable output: stdout
    "Termination reached at gen N"; combined seed44+seed55 cost <= $8.00. Satisfies REQ-9, REQ-11.

14. **[CRITICAL] Run NSGA-II seed=66 on the same Vast.ai instance.** Same command and validation
    gates as step 12 but with `task_seed=66`. Same gen-1 cell-history inspection requirement.
    Sanity-check identical to step 12. Inputs: remote code/. Outputs:
    `results/data/nsga2_seed66_history.json`, `results/data/nsga2_seed66_cost.json`,
    `logs/steps/<idx>_implementation/seed66_stdout.log`. Expected observable output: stdout
    "Termination reached at gen N"; combined seed44+seed55+seed66 cost <= $12.00. Satisfies REQ-9,
    REQ-11.

15. **Pull results back from the Vast.ai instance.** Run the inherited `sync_results_back.sh` script
    to rsync `results/data/`, `logs/`, and any intermediate artefacts to the local repo. Inputs:
    remote results. Outputs: synced local `results/data/`, `logs/`. Expected observable output:
    `ls tasks/t0104_*/results/data/` shows `nsga2_seed44_history.json`, `nsga2_seed55_history.json`,
    `nsga2_seed66_history.json`, and the three per-seed cost JSONs. Satisfies REQ-9 (transport
    back).

### Milestone 4: Teardown and analysis

16. **Destroy the Vast.ai instance.** Use the setup-remote-machine teardown utility to terminate the
    instance and record the final billed amount in `results/remote_machines_used.json`. If the
    driver-level teardown hook (REQ-8) already destroyed the instance after the last seed
    completion, confirm via `vastai show instance <id>` that the instance is in "destroyed" state
    and verify the recorded final cost matches. Inputs: machine ID. Outputs:
    `results/remote_machines_used.json` (final cost), Vast.ai instance terminated. Expected
    observable output: Vast.ai dashboard shows instance in "destroyed" state;
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run python -m arf.scripts.verificators.verify_machines_destroyed t0104_nsga2_2obj_dsi_pdrate_3seeds`
    exits 0. Satisfies REQ-8 (verification of teardown wiring), REQ-17.

17. **Build the 3 predictions assets.** Run
    `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.build_assets` (adapted in step 1 to emit 3
    assets). This reads the three NSGA-II history JSONs and emits three predictions asset folders
    following `meta/asset_types/predictions/specification.md`:
    `assets/predictions/nsga2-seed44-bedb-morph-n4-gen20-2obj/`,
    `nsga2-seed55-bedb-morph-n4-gen20-2obj/`, `nsga2-seed66-bedb-morph-n4-gen20-2obj/`. Each
    contains `details.json` (predictions metadata with the GA seed, pop, gen count, N_EVAL_SEEDS=4,
    n_obj=2, dsi_guard_threshold=10.0), `description.md` (one-page run-configuration description),
    and `files/pareto_cells.jsonl` (per-cell JSONL with the 68-d parameter vector, DSI, PD rate,
    `robustness` field still present, anchor classification, generation index). Inputs: NSGA-II
    history JSONs. Outputs: 3 predictions asset folders. Expected observable output:
    `uv run python -m arf.scripts.verificators.verify_predictions_asset tasks/t0104_*/assets/predictions/nsga2-seed44-bedb-morph-n4-gen20-2obj`
    exits 0; same for the other two seeds. Satisfies REQ-10.

18. **Run per-seed and cross-seed analysis, compute metrics, generate charts.** Execute
    `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.per_seed_analysis` for each seed (classifies
    Pareto cells to nearest anchor using the t0102-inherited `anchor_classifier.py`, counts strict
    joint-pass at DSI >= 0.5 AND PD >= 30 Hz) followed by
    `tasks.t0104_nsga2_2obj_dsi_pdrate_3seeds.code.cross_seed_analysis` (5x5 anchor distribution
    table across {seed44, seed55, seed66, t0102 aggregate, t0099 aggregate}, HV overlay in the (DSI,
    PD) plane with 5 curves, DSI vs PD scatter colour-coded by anchor with joint-pass corner
    overlay). Compute the DSI-guard impact: count cells per seed at the guard floor (DSI = 0.0
    because total mean spikes < 10) and reanalyse t0102's seed44/seed55 predictions with the new
    guard applied post-hoc to identify how many of the 27 t0102 DSI = 1.0 cells would have been
    masked; write to `results/data/dsi_guard_impact.json`. Compute and write `results/metrics.json`
    in the explicit multi-variant format with variants `seed44`, `seed55`, `seed66`, each populating
    the four registered metric keys `direction_selectivity_index` (best DSI over the Pareto front),
    `tuning_curve_hwhm_deg` (median HWHM; full Pareto if zero strict-pass),
    `tuning_curve_reliability` (median Pearson rho over the 4 noise replicates per cell, averaged),
    `tuning_curve_rmse` (best RMSE). Read `arf/specifications/metrics_specification.md` for the
    exact JSON schema. Inputs: predictions asset files, t0102 result data, t0099 result data.
    Outputs: `results/data/per_seed_summary_seed44.json`, `seed55.json`, `seed66.json`,
    `results/data/cross_seed_summary.json`, `results/data/dsi_guard_impact.json`,
    `results/metrics.json`, `results/images/hv_trajectory.png`,
    `results/images/dsi_vs_pd_scatter.png`, `results/images/anchor_distribution_heatmap.png`.
    Expected observable output: 3 PNG files present;
    `jq '.variants | keys' tasks/t0104_*/results/metrics.json` prints
    `["seed44", "seed55", "seed66"]`; `cross_seed_summary.json` contains a 5x5 anchor table.
    Satisfies REQ-14, REQ-15, REQ-16.

19. **Build the answer asset.** Generate `assets/answer/t0104_joint_pass_recovery_2obj/` per
    `meta/asset_types/answer/specification.md`: `details.json` (canonical question text, evidence
    channels used, citation list), the canonical short answer document at `short_answer.md` (2-5
    sentences stating Yes / No / I don't know, citing the joint-pass count per seed without inline
    citations), the canonical full answer document at `full_answer.md` (mini-paper with sections
    Question, Short Answer, Method, Evidence from Code or Experiments, Evidence from Existing
    Papers, Synthesis, Limitations, Sources). Cite t0102, t0099, t0091, PolegPolsky2026,
    Druckmann2007, Hay2011 as supporting evidence. Reference links in `## Sources` follow the
    asset-spec format. Inputs: per-seed summaries, cross-seed summary, DSI-guard impact JSON,
    research files. Outputs: `assets/answer/t0104_joint_pass_recovery_2obj/details.json`,
    `short_answer.md`, `full_answer.md`. Expected observable output:
    `uv run python -m arf.scripts.verificators.verify_answer_asset tasks/t0104_*/assets/answer/t0104_joint_pass_recovery_2obj`
    exits 0. Satisfies REQ-12.

* * *

## Remote Machines

One Vast.ai instance is required:

* GPU: not required (NEURON is CPU-bound).
* CPU: AMD EPYC 7B13, 64 effective cores (same as t0102, t0099, t0091).
* RAM: >= 200 GB.
* Location: Norway preferred (for $0.24/hr pricing).
* Hourly cap: $0.40/hr (reject more expensive offers).
* Runtime: ~30-36 h expected, 40 h hard ceiling enforced by per-seed cost watchdog ($4 x 3 = $12
  productive total) plus the $15 orchestrator cap.
* Provider: Vast.ai (`setup-remote-machine` skill).
* Lifecycle: provisioned in step 9, destroyed in step 16. Idle-teardown wired in step 4 via the
  S-0102-08 driver-level `try/finally` hook so post-NSGA-II idle billing cannot accumulate.

* * *

## Assets Needed

* **Bed B compartmental cell substrate** (REQ-9 dependency): `de_rosenroll_2026_dsgc` library from
  t0024 [t0024_port_de_rosenroll_2026_dsgc] (HOC template, vendored MOD library, build_cell).
  Imported via
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import _ensure_neuron_on_path, load_neuron`.

* **Compiled MOD library**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/x86_64/` —
  referenced as `T0080_MODS_DIR` by `paths.py` (unchanged from t0102). NEURON SUFFIX namespace is
  shared.

* **Morphology generator (patched)**: `procedural_dsgc_morphology_generator_fix` library from t0092
  [t0092_diagnose_morphology_generator_silence] (replaces t0090 via correction C-0093-01). Imported
  via
  `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult`,
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`,
  and
  `from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import insert_baseline_channels`.

* **t0093 anchor / verification fingerprint** (REQ-13 dependency):
  `tasks/t0093_resweep_and_t0090_correction/results/data/post_fix_verification_summary.json` for the
  5-anchor smoke-gate target (PD-rate tolerance 1 Hz, DSI tolerance 0.05).

* **t0102 substrate fork base** (verbatim except 3 patches): `tasks/t0102_seedscale_n4_gen20/code/`
  — all 28+ Python files plus `run_two_seeds.sh`, copied into `tasks/t0104_*/code/` in step 1 with
  import paths rewritten.

* **t0102 reference data** (REQ-14 reanalysis): `tasks/t0102_seedscale_n4_gen20/results/data/`
  (per-seed history JSONs, anchor tracking, cross-seed summary) — for the post-hoc DSI-guard
  reanalysis and the 5x5 anchor distribution comparison column.

* **t0099 reference data** (REQ-15 cross-seed column):
  `tasks/t0099_random_init_pareto_robustness/results/data/` (anchor_tracking.json,
  hv_trajectory.json, pareto_front.json) — for the second reference column in the cross-seed
  comparison.

* **t0086 cluster utilities** (analysis adapter, REQ-16 anchor histogram):
  `tasks/t0086_robustness_cluster_bio_comparison/code/cluster_analysis.py` — k=2..6 + silhouette
  + BIC + bootstrap ARI pipeline, adapted in step 18 to 68-d bounds. Used only if the per-seed
    anchor histogram from `anchor_classifier.py` is insufficient.

* **t0086 anchor / classification utilities**: already reachable transitively through t0102's
  `anchor_classifier.py` and `anchor_definitions.py` (copied verbatim in step 1).

* * *

## Expected Assets

Matches `task.json` `expected_assets`:

* **3 predictions assets** under `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/assets/predictions/`:
  * `nsga2-seed44-bedb-morph-n4-gen20-2obj/` — full per-cell history of the seed=44 NSGA-II run
    (96 LHS init + up to 20 x 96 = 2,016 cells, minus any early-terminated generations). Contains
    DSI (guard-cleaned), PD-rate, `robustness` (still computed and stored despite being dropped from
    F-row), anchor classification, generation index, and 68-d parameter vector per cell.
  * `nsga2-seed55-bedb-morph-n4-gen20-2obj/` — same for seed=55.
  * `nsga2-seed66-bedb-morph-n4-gen20-2obj/` — same for seed=66.

* **1 answer asset** under `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/assets/answer/`:
  * `t0104_joint_pass_recovery_2obj/` — short and full answers to "Does 2-objective NSGA-II (DSI +
    PD-rate, with the DSI-silence guard applied) recover joint-pass cells where t0102's 3-objective
    run found zero?" with evidence from the new 3-seed experiment plus the t0102 post-hoc DSI-guard
    reanalysis plus the t0099 cross-task comparison.

* * *

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already done in prior steps) | 0 h |
| Local code prep + lint + unit test (milestone 1, steps 1-7) | 1.5-2 h |
| Local + remote smoke gates (steps 8, 11) | 0.5 h |
| Vast.ai provisioning + SCP (steps 9, 10) | 0.5-1 h |
| NSGA-II seed=44 (step 12) | 9-12 h |
| NSGA-II seed=55 (step 13) | 9-12 h |
| NSGA-II seed=66 (step 14) | 9-12 h |
| Pull results + teardown (steps 15, 16) | 0.5 h |
| Analysis + asset build + answer (steps 17-19) | 3-4 h |
| **Total** | **32-40 h** |

The Vast.ai compute portion (steps 9-16) is ~28-37 h continuous; the rest is local time that can be
interleaved.

* * *

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Even after dropping robustness from the objective vector and applying the DSI-silence guard, joint-pass yield remains zero across all 3 seeds, confirming the 68-d substrate is empirically empty of joint-pass cells under random init. | Medium | Negative result, but is publishable | The answer asset is written to state the result either way (REQ-12). A 0/6,048 outcome strengthens the conclusion that algorithm replacement (S-0102-03 IBEA or S-0102-04 Dang pop>=290) is the next move, not further NSGA-II tuning. Wilson 95% upper CI on yield goes below 0.0005, a stronger statement than t0102's 0/2,592 null could make. |
| Per-seed wall-clock grows super-linearly due to NEURON memory accumulation (S-0099-04 / S-0102 known pattern). | Medium | Budget overrun, potential third-seed truncation | Worker restart between generations is already inside the inherited nsga2_driver.py. Per-seed $4 cost watchdog trips early if seed exceeds its budget; the watchdog-tripped flag now also triggers Vast.ai teardown (REQ-8, S-0102-08 partial fix). If seed=44 cost > $4 forcing early termination, halt before launching seed=55 and write an intervention recording the elapsed cost. If still over budget after seed=55, cut seed=66 at gen 15 and report partial. |
| Vast.ai instance fails to provision in $0.24/hr range; only $0.40/hr offers available. | Low | Reduced runtime headroom (~37 h vs ~62 h at $0.24/hr) | The cost watchdog reads the actual `price_per_hour` from machine_log.json; at $0.40/hr the $15 cap still buys 37 h, which fits the expected 32-40 h wall-clock. If only > $0.40/hr offers exist, halt provisioning and write an intervention file. |
| t0090 / t0093 morphology generator silently produces empty trees again (pre-fix bug). | Low | All Pareto cells NaN, smoke gate fails | Smoke gate REQ-13 against the t0093 60-cell fingerprint catches this before commitment. The t0092 fix is already C-0093-01-corrected and the t0099 / t0102 lineage has confirmed stability across 60+ cells. |
| The DSI-silence guard introduces a regression where legitimate near-silent cells with real direction selectivity (e.g., 5 PD spikes, 0 ND spikes = total mean ~ 0.3 across directions) get masked. | Low | Loss of a small set of legitimate near-silent cells from the Pareto front | The 10-spike threshold is conservative (chosen at brainstorm session 22). REQ-7's unit test documents the threshold and the firing-positive control case. Step 18's `dsi_guard_impact.json` quantifies how many cells in each t0104 seed are at the guard floor and how many t0102 cells would have been masked; if the guard masks more than 10% of any seed's Pareto front, results_detailed.md flags this as a known limitation and proposes a sensitivity sweep at thresholds 5, 10, 20, 50 as a follow-up. |
| HV-plateau termination trips early (e.g., gen 5 instead of gen 20) and gives partial result. | Medium | Lower effective gen count than planned | This is desired behaviour for converged runs and is not a defect. Step 18 reports the actual termination generation per seed. If all 3 seeds plateau by gen 8, that itself is a meaningful answer about substrate convergence speed. |
| Vast.ai instance teardown subprocess (REQ-8 hook) fails silently and instance bills idle hours after run completion. | Low | $1-3 idle overrun toward the $15 cap | The `try/finally` in `run_nsga2_for_seed` is the first line of defense. Step 16 invokes a redundant teardown via the setup-remote-machine skill plus verifies destruction via `verify_machines_destroyed`. If both fail, `results/remote_machines_used.json` records the actual billed amount and any overrun is captured against the $15 cap (~$3 of headroom). |
| Implementation agent silently substitutes a different DSI-guard placement (e.g., inside `_vector_sum_dsi` directly) and breaks the per-seed robustness computation. | Low | Per-seed DSIs all collapse to 0.0; robustness signal lost | Step 3 names the exact line range (between line 308 and line 325 of `_summarise_trials`) and explicitly forbids the `_vector_sum_dsi`-internal site. Step 7's mypy/ruff pass and step 8/11's unit test (REQ-7) catch the regression because the firing positive control test case asserts DSI > 0 for a cell with mean spikes = 25. If the unit test fails, halt and re-locate the guard. |
| GA seeds 44 and 55 produce significantly different t0104 results than t0102 ran them at the same seeds, indicating an unintended algorithmic change. | Low | Apples-to-apples 2-obj vs 3-obj lift is uninterpretable | Step 18's cross-seed comparison includes a `delta_t0102_seed44.json` derived metric that diffs the t0104 seed44 Pareto front against t0102's seed44 Pareto front in the (DSI, PD) plane; any deltas not attributable to the DSI-guard or robustness drop are flagged in results_detailed.md as a regression in the analysis stage. |

* * *

## Verification Criteria

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run python -m arf.scripts.verificators.verify_plan t0104_nsga2_2obj_dsi_pdrate_3seeds`;
  expected exit code 0 with zero errors. This confirms the plan satisfies the plan_specification.md
  v2 structural requirements before implementation begins.

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run pytest tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/code/test_evaluator_dsi_guard.py -v`;
  expected exit code 0 with at least 3 passing tests. This confirms REQ-7 (DSI-silence guard unit
  test).

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run python -m arf.scripts.verificators.verify_task_metrics t0104_nsga2_2obj_dsi_pdrate_3seeds`;
  expected exit code 0. This confirms the explicit multi-variant `results/metrics.json` (REQ-15) has
  variants `seed44`, `seed55`, `seed66` each populating the four registered metric keys
  (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`).

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run python -m arf.scripts.verificators.verify_predictions_asset tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/assets/predictions/nsga2-seed44-bedb-morph-n4-gen20-2obj`
  and the same command for `nsga2-seed55-bedb-morph-n4-gen20-2obj` and
  `nsga2-seed66-bedb-morph-n4-gen20-2obj`; all three expected exit code 0. This confirms REQ-10 (3
  predictions assets each pass spec).

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run python -m arf.scripts.verificators.verify_answer_asset tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/assets/answer/t0104_joint_pass_recovery_2obj`;
  expected exit code 0. This confirms REQ-12 (the answer asset is structurally valid and addresses
  the canonical question).

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0104_nsga2_2obj_dsi_pdrate_3seeds -- uv run python -m arf.scripts.verificators.verify_machines_destroyed t0104_nsga2_2obj_dsi_pdrate_3seeds`;
  expected exit code 0. This confirms REQ-17 (the Vast.ai instance was destroyed and
  `results/remote_machines_used.json` records it).

* Inspect `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/costs.json` and confirm the `total_usd`
  field is less than or equal to 15.00. Command: `jq '.total_usd' tasks/t0104_*/results/costs.json`;
  expected output: a numeric value <= 15.00. This confirms REQ-11 (hard $15 cap).

* Inspect `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/cross_seed_summary.json` and
  confirm it contains a 5x5 anchor distribution table across {seed44, seed55, seed66, t0102, t0099}
  and a `strict_joint_pass_count` field per seed. Command:
  `jq '.anchor_distribution | keys' tasks/t0104_*/results/data/cross_seed_summary.json`; expected
  output includes `["seed44", "seed55", "seed66", "t0102", "t0099"]`. This confirms REQ-14 / REQ-16
  (anchor histogram piece).

* Inspect `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/images/` and confirm at least 3 PNG
  files exist. Command: `ls tasks/t0104_*/results/images/*.png | wc -l`; expected output: at least
  3\. This confirms REQ-16.

* Inspect `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/dsi_guard_impact.json` and confirm
  it records per-seed counts at the guard floor (DSI = 0.0 because total mean spikes < 10) plus a
  `t0102_reanalysis_masked_count` field. Command:
  `jq '.t0102_reanalysis_masked_count' tasks/t0104_*/results/data/dsi_guard_impact.json`; expected
  output: an integer in [0, 27] (t0102 reported 27 cells at DSI = 1.0; the guard will mask some
  subset of those). This confirms REQ-14.

* Confirm REQ-* coverage end-to-end by re-running `verify_plan` (above) and reading the plan itself
  — every REQ-1 through REQ-18 must map to at least one numbered step in `## Step by Step`. The
  verificator's PL-W007 warning fires if any `REQ-*` is absent from Step by Step.
