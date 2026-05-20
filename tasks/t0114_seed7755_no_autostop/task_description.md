# t0114: Seed-7755 NSGA-II Replicate of t0106 Substrate with HV-Plateau Auto-Stop Disabled

## Motivation

Suggestion `S-0113-03` documents that the t0106-family HV-plateau detector (`WINDOW = 2`,
`REL_THRESHOLD = 0.01`) is too aggressive: it fired at gen 14 on t0113 (seed 2247), at gen 21 on
t0112 (seed 77), and at gen 40 on t0106 (seed 44), with the t0113 trigger occurring *below* Mohacsi
2024's published 20-60 gen NSGA-II convergence range. The t0113 trigger was driven by a soft gen
11→12 transition (`HV 35.98 -> 36.07`, +0.24 %) satisfying the rule one generation before a +26 %
gen 13→14 HV jump caused by a silence-guard cell joining the archive.

S-0113-03 prescribes an offline parameter sweep over `WINDOW ∈ {3, 4, 5}` and
`REL_THRESHOLD ∈ {0.005, 0.01}` to pick new defaults. That sweep cannot tell us *what HV growth
the existing seeds would have produced past their premature trigger* — only a fresh run with
auto-stop disabled can. This task contributes that fresh run: a single long NSGA-II evolution on the
same t0106 / t0112 / t0113 substrate, with **HV-plateau auto-stop removed entirely**, allowed to run
until the gen ceiling or budget cap (the operator may also stop it manually). The resulting trace is
both (a) a fourth substrate-rate datapoint for the `S-0112-01` 5-seed batch and (b) the live
ground-truth HV trace that S-0113-03's offline detector replay can validate against.

The seed is **7755**, drawn locally by `secrets.randbelow(10000)` on 2026-05-20 by the implementing
agent. Random draw avoids any conscious or unconscious bias in seed choice and widens the support of
the existing seed sample (44, 77, 2247).

## Scope

* **In scope (unchanged from t0113)**: substrate (Bed B 54-d electrophys + 14-d morphology = 68 free
  parameters), objectives (2-direction ratio DSI + PD-rate at 0 deg), NSGA-II hyperparameters (pop =
  96, SBX/PM operators), evaluation protocol (`N_EVAL_SEEDS = 3`, ratio DSI, silence guard active),
  `_POOL_RESTART_EVERY = 10` (the "10th gen rule"), predictions asset schema, cost-watchdog wiring,
  smoke-gate suite.
* **In scope, changed from t0113**:
  1. **GA seed**: `2247 -> 7755` (randomly drawn for this task).
  2. **HV-plateau auto-stop DISABLED**: `HVPlateauTermination` is *not* added to the pymoo
     termination list. Termination is driven solely by the gen ceiling, the per-task $25 budget cap,
     the per-instance $20 watchdog, and explicit operator stop.
  3. **Gen ceiling**: `N_GEN = 60 -> 300`, matching the t0106 original ceiling. With auto-stop off
     we want the budget cap and explicit operator stop to be the binding constraints, not a tight
     ceiling.
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, the NSGA-II operator hyperparameters, the predictions
  asset schema, the metrics list, or `_POOL_RESTART_EVERY`. Out-of-scope changes would compromise
  the like-for-like comparison with t0106 / t0112 / t0113.

## Approach

1. **Fork t0113 code into `tasks/t0114_seed7755_no_autostop/code/`**: copy every algorithm-critical
   Python module (`nsga2_driver.py`, `constants.py`, `constants_morphology.py`,
   `constants_electrophys.py`, `evaluator.py`, `random_init.py`, `apply_params.py`,
   `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`, `recorder.py`,
   `trial_helpers.py`, `generator_wrapper.py`, `hv_plateau_watchdog.py` *(kept for offline replay,
   not wired into the live termination list)*, `cost_watchdog.py`, `bootstrap.py`, `paths.py`,
   `smoke_gate.py`, `test_evaluator_dsi_guard.py`, and helper modules) plus the orchestration shell
   script.
2. **Rewrite package import paths**: replace `tasks.t0113_t0106_seed2247_replicate` with
   `tasks.t0114_seed7755_no_autostop` across every copied `.py` and `.sh` file. Leave upstream task
   references untouched (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`, `tasks.t0092_*`,
   `tasks.t0093_*`, `tasks.t0106_*`).
3. **Apply three constant patches**:
   * In `constants.py`, rename `T0113_SEEDS = (2247,)` to `T0114_SEEDS = (7755,)` and
     `T0113_HARD_BUDGET_USD = 25.00` to `T0114_HARD_BUDGET_USD = 25.00`. Update the
     backwards-compatibility aliases at the bottom of the file to point at the new constants.
   * In `constants_morphology.py`, change `N_GEN = 60` to `N_GEN = 300`.
   * In `nsga2_driver.py`, remove `HVPlateauTermination(seed=...)` from the pymoo termination list
     (or replace it with a no-op termination). Keep `_POOL_RESTART_EVERY = 10` verbatim. Add a
     prominent comment block above the termination construction citing this task's directive
     ("auto-stop disabled per S-0113-03 + user directive 2026-05-20").
4. **Smoke gate locally** (same 5 checks as t0113, plus one new check that the termination list
   contains no `HVPlateauTermination`): single-eval driver run, ratio DSI synthetic sanity,
   silence-guard unit tests, pool-restart sanity, cost-watchdog wiring, and the new auto-stop-absent
   assertion. All checks must pass before any Vast.ai provisioning.
5. **Provision Vast.ai single instance** with the same filter class as t0106 / t0112 / t0113
   (EPYC-class CPU, ≥ 100 GB RAM, idle RTX 3060 Ti or equivalent, reliability ≥ 0.99,
   `dph ≤ 0.40`, EPYC family post-filter). Prefer a 64-core+ EPYC 7B13 to inherit t0113's 160
   s/gen wall-clock.
6. **Launch** with cost cap $25 per-task and per-instance watchdog $20. Termination triggers are (in
   order of expected firing): explicit operator stop, $25 budget cap, $20 per-instance watchdog, gen
   300 ceiling.
7. **Collect** the evaluator-side per-cell DSI / PD-rate / generation table as a predictions asset
   in the t0106 / t0112 / t0113 schema (`spec_version: "2"`, gzipped JSON, fields `generation`,
   `vector_68d`, `objective_F_minimised`, `dsi_vector_sum` — back-compat field name storing ratio
   DSI — and `pd_rate_hz`).
8. **Offline detector replay** (the S-0113-03 implementation core): replay `should_stop(hv_history)`
   over the full t0114 HV trajectory plus the three existing t0106 / t0112 / t0113 traces under
   every combination of `WINDOW ∈ {2, 3, 4, 5}` and `REL_THRESHOLD ∈ {0.005, 0.01}`. Output a
   CSV showing, for each (seed, WINDOW, REL_THRESHOLD) triple, the generation the detector would
   have fired at and the HV value at that point. Pick the pair (W*, T*) that *(a)* would not have
   fired before gen 20 on any seed (matching Mohacsi 2024's lower bound), *(b)* would have fired by
   gen 60 on t0106 (the longest run), and *(c)* requires the smallest deviation from the current
   defaults that satisfies (a) and (b).
9. **Compare** to t0106 (seed 44), t0112 (seed 77), and t0113 (seed 2247):
   * Joint-pass cell count (DSI ≥ 0.5 AND PD ≥ 30 Hz) absolute and as % of total evaluations.
   * Best ratio DSI and best PD-rate frontier vs t0106's 1.0000 / 122.6 Hz, t0112's 0.9535 / 114.8
     Hz, and t0113's 0.3651 (legit) / 71.7 Hz.
   * Full HV trajectory shape past the existing seeds' premature plateau triggers.
   * Pareto front overlap in normalised z-scored 68-d parameter space against each of the three
     other seeds.

## Expected Assets

* **1 predictions asset** at
  `tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/` containing
  the per-cell DSI / PD-rate / generation table for every evaluated cell, mirroring the t0106 /
  t0112 / t0113 predictions asset schemas. Required `metrics_at_creation` keys:
  `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`,
  `stop_trigger` (one of `operator_stop`, `budget_cap`, `gen_ceiling`, `instance_watchdog`).

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is for
  CPU cores; the GPU sits idle on the selected Vast.ai offer.
* **Remote**: Vast.ai single instance, same provisioning class as t0106 / t0112 / t0113. Preference
  for 64-core+ EPYC 7B13 to inherit t0113's 160 s/gen wall-clock.
* **Cost cap**: $25 per-task hard cap. **Per-instance watchdog**: $20 via
  `make_watchdog_from_machine_log`.
* **Expected actual cost**: ~~$2-25. The wide range reflects that auto-stop is OFF: cost depends on
  the operator's decision to stop and on whether the budget cap fires first. At t0113's per-gen rate
  (~~$0.01 / gen productive) the $25 cap supports ~2400 generations — well above any plausible
  stop point. The realistic upper bound is therefore the gen 300 ceiling, which at 160 s/gen takes
  ~13 wall-clock hours and ~$5-6 in productive compute.
* **Project envelope check**: confirm project remaining budget covers $25 hard cap before
  provisioning. If insufficient, halt and create an intervention file.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `hv_vs_gen_4seeds.png` — log-scale HV trajectory for all four seeds (44, 77, 2247, 7755) on the
   same axes with pool-restart events and would-have-been-auto-stop generations annotated; answers
   "where does HV growth actually saturate when the run is allowed to continue?"
2. `pareto_front_4seeds.png` — overlay of strict Pareto fronts from t0106, t0112, t0113, and t0114
   on DSI vs PD-rate axes; coloured by source task; answers "do the four seeds discover comparable
   Pareto frontiers when one is allowed to run unstopped?"
3. `joint_pass_yield_per_gen_4seeds.png` — joint-pass cell count discovered per generation across
   all four seeds; answers "when does each seed first hit the joint-pass corner and what is the rate
   thereafter?"
4. `detector_replay_heatmap.png` — heatmap of (WINDOW × REL_THRESHOLD) showing the generation at
   which the detector would have fired on each seed; answers "which parameter pair satisfies the
   S-0113-03 criteria across all four seeds?"
5. `top50_morphologies_seed7755.png` — 10x5 grid of best 50 cells from t0114, coloured by
   archetype, matching the format of `top50_morphologies.png` (t0106), `_seed77.png` (t0112), and
   `_seed2247.png` (t0113).

### Tables

* `results/data/joint_pass_summary_4seeds.csv` — per-seed (44, 77, 2247, 7755): total evals,
  joint-pass count, joint-pass %, best DSI, best PD-rate, stop trigger, stop generation.
* `results/data/pareto_front_overlap_4seeds.csv` — for each t0114 Pareto cell, the nearest-
  neighbour z-scored L2 distance in 68-d parameter space to its closest t0106, t0112, and t0113
  cells.
* `results/data/detector_replay.csv` — long-format (seed, WINDOW, REL_THRESHOLD, gen_at_fire,
  hv_at_fire, hv_at_run_end) covering all 4 seeds × 4 windows × 2 thresholds = 32 rows.

### Registered metrics

Check `uv run python -u -m arf.scripts.aggregators.aggregate_metrics --format json` and run every
registered metric that applies. At minimum:

* `direction_selectivity_index` — best ratio DSI across all evaluated cells. Sub-variants
  `best_legit` (highest non-DSI = 1.0 cell), `overall_max`, `dsi_eq_one_count`.

Operational metrics (not registered): `joint_pass_count`, `best_pd_rate_hz`,
`n_cells_evaluated_total`, `n_gen_completed`, `stop_trigger`,
`efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`.

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative answer,
not a hedge:

1. **Seed-7755 joint-pass count.** Does seed 7755 produce ≥ 40 unique joint-pass cells
   (t0106-like), 7-39 cells (t0112-like), 1-6 cells (sparse), or 0 (substrate not populated at this
   seed)?
2. **Best ratio DSI.** Does seed 7755's best legit ratio DSI reach or exceed 0.95?
3. **Best PD-rate.** Does seed 7755's best PD-rate reach or exceed 100 Hz?
4. **Four-seed substrate-rate estimate.** Combining t0106, t0112, t0113, and t0114, what is the
   substrate-level mean joint-pass acceptance rate and standard error? Does the four-seed mean fall
   within the Hay 2011 (0.40 %) / Druckmann 2007 (0.10 %) literature envelope?
5. **Post-trigger HV growth.** How much additional HV growth occurred on seed 7755 between the
   would-have-been-auto-stop generation (replay the current `WINDOW = 2`, `REL_THRESHOLD = 0.01`
   rule against the full t0114 trace) and the actual stop point? Quantify as both absolute HV delta
   and percentage of total HV.
6. **Detector reparameterisation (S-0113-03 implementation).** Across the four seeds and the
   (WINDOW, REL_THRESHOLD) sweep, which pair (W*, T*) satisfies the three S-0113-03 criteria (fires
   ≥ gen 20 on every seed; fires ≤ gen 60 on t0106; smallest deviation from current defaults)?
   State the recommended new project default.
7. **Cadence-10 wall-clock confirmation at extended N_GEN.** Does the per-generation wall-clock
   remain stable across the full t0114 run, or does it drift (e.g., archive size growth slowing the
   evaluator)?
8. **Stop trigger.** Which mechanism actually stopped the run (operator, budget cap, gen ceiling,
   instance watchdog)?

## Risks and Fallbacks

* **Risk**: long unstopped run consumes the $25 budget before reaching gen 300. **Fallback**: the
  cost watchdog stops the run cleanly; results from however many generations completed are still a
  valid 4th seed datapoint.
* **Risk**: Vast.ai instance is interrupted mid-run. **Fallback**: t0106-family driver checkpoints
  per-generation; resume from last completed generation if the orchestration shell script supports
  it, otherwise treat the partial run as the final result.
* **Risk**: a single silence-guard cell dominates HV growth at some late generation, distorting the
  offline detector replay. **Fallback**: report both raw HV and silence-guard-stripped HV in the
  replay CSV; pick (W*, T*) using the stripped trajectory.
* **Risk**: operator forgets to issue a stop signal and the run goes to gen 300 / budget cap
  unattended. **Fallback**: acceptable — the gen ceiling and budget cap are designed as the
  ultimate safety net for the "stop when I say so" directive.

## Cross-References

* **Parent tasks**: `t0106_long_pdnd_nsga2_300gen` (original substrate, driver, baseline) and
  `t0113_t0106_seed2247_replicate` (canonical fork base for the cadence-10 / 68-d substrate
  protocol).
* **Source suggestion**: `S-0113-03` (HV-plateau detector window widening). This task is the live
  no-auto-stop validation half of S-0113-03; the offline detector replay using this task's HV trace
  is also performed here.
* **Companion suggestion batch**: `S-0112-01` (5-seed substrate-rate confirmation). This task
  contributes the 4th seed of that batch; one more seed will be required to complete it.
* **Related caveat tasks**: `t0107_t0106_polar_8dir_recheck` (8-direction polar re-evaluation
  showing 2-direction ratio DSI overstates selectivity by ~0.42 absolute). Polar re-evaluation of
  any t0114 joint-pass cells is out of scope for this task.
* **Brainstorm source**: none directly. This task is the direct realisation of S-0113-03 plus the
  user's 2026-05-20 directive to disable auto-stop and apply the 10th gen rule.
