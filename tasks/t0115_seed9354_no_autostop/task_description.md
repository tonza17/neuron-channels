# t0115: Seed-9354 NSGA-II Replicate of t0106 Substrate with HV-Plateau Auto-Stop Disabled

## Motivation

This task is the **5th and final seed** of the `S-0112-01` substrate-rate confirmation batch on the
68-d Bed B + 14-d morphology substrate. The prior four seeds are:

* `t0106_long_pdnd_nsga2_300gen` (seed 44): 123 legit joint-pass cells, 3.29 % acceptance, best
  legit DSI ~0.94 / PD ~95 Hz, plateau gen 40.
* `t0112_t0106_seed77_replicate` (seed 77): 7 legit joint-pass cells, 0.35 % acceptance, best legit
  0.9535 / PD 114.8 Hz, plateau gen 21.
* `t0113_t0106_seed2247_replicate` (seed 2247): 0 legit joint-pass cells (2 silence-guard DSI=1.0
  only), best legit 0.3651 / 10.24 Hz, premature auto-stop at gen 14.
* `t0114_seed7755_no_autostop` (seed 7755, this task's direct parent): 194 legit joint-pass cells,
  4.30 % acceptance, best legit DSI 0.9868 / PD 107.86 Hz, operator-stopped at gen 62 (auto-stop
  disabled).

The four-seed estimate of substrate acceptance density is therefore **mean 1.81 %, SD 1.86 %, SE
0.93 %** with 95 % CI (-0.16 %, 3.78 %), still bracketing both literature baselines (Hay 2011 0.40
%, Druckmann 2007 0.10 %). A 5th seed is needed to bring the standard error below 0.5 % and to give
the substrate-rate estimate enough power to reject or confirm the Hay envelope. This task
contributes that 5th seed.

The seed is **9354**, drawn locally by `secrets.randbelow(10000)` on 2026-05-20 by the implementing
agent. Random draw keeps the seed sample (44, 77, 2247, 7755, 9354) well-distributed across
[0, 10 000].

## Scope

* **In scope (unchanged from t0114)**: substrate (68 free parameters), objectives (2-direction ratio
  DSI + PD-rate at 0 deg), NSGA-II hyperparameters (pop = 96, SBX/PM operators), evaluation protocol
  (`N_EVAL_SEEDS = 3`, ratio DSI, silence guard active), `_POOL_RESTART_EVERY = 10` ("10th gen
  rule"), `N_GEN = 300` ceiling, HV-plateau auto-stop **DISABLED**, $25 per-task budget cap, $20
  per-instance watchdog, predictions asset schema, cost-watchdog wiring, smoke-gate suite (including
  the new check 6 that asserts no `HVPlateauTermination` in the live termination list).
* **In scope, changed from t0114**:
  * GA seed: `7755 → 9354` (randomly drawn for this task).
  * Vast.ai instance: **fully independent** — provision a fresh node (not the t0114 instance,
    which has been destroyed).
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, the NSGA-II driver beyond the seed constant, the
  predictions asset schema, the metrics list, or the cost-watchdog wiring.

## Approach

1. **Fork t0114 code into `tasks/t0115_seed9354_no_autostop/code/`**: copy every algorithm- critical
   Python module from `tasks/t0114_seed7755_no_autostop/code/` (the canonical fork base — t0114
   already carries the auto-stop-disabled `_build_termination()` helper, `N_GEN = 300`, and
   `_POOL_RESTART_EVERY = 10`), plus the orchestration shell script.
2. **Rewrite package import paths**: replace `tasks.t0114_seed7755_no_autostop` with
   `tasks.t0115_seed9354_no_autostop` across every copied `.py` and `.sh` file. Do not touch
   upstream task references (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`, `tasks.t0092_*`,
   `tasks.t0093_*`, `tasks.t0106_*`).
3. **Apply exactly one constant patch**: in `constants.py`, rename
   `T0114_SEEDS = (7755,) → T0115_SEEDS = (9354,)` and update the backwards-compatibility aliases
   at the bottom of the file. Do NOT touch `N_GEN`, `_POOL_RESTART_EVERY`, or the termination
   construction in `nsga2_driver.py` — t0114's auto-stop-disabled wiring is the correct default
   for this task too.
4. **Smoke gate locally** (same 6 checks as t0114): single-eval driver run (deferred to remote),
   ratio DSI synthetic sanity, silence-guard unit tests, pool-restart sanity, cost-watchdog wiring,
   and the auto-stop-absent assertion.
5. **Provision Vast.ai single instance** with the same filter class as t0114 (EPYC-class CPU, ≥
   100 GB RAM, idle GPU, reliability ≥ 0.99, `dph ≤ 0.40`, EPYC family post-filter). Prefer a
   64-core+ EPYC 7B13 / 7713P to inherit t0114's 160-200 s/gen wall-clock.
6. **Launch** with cost cap $25 per-task and per-instance watchdog $20. Termination triggers are (in
   order of expected firing): explicit operator stop, $25 budget cap, $20 per-instance watchdog, gen
   300 ceiling. **Auto-stop is intentionally OFF.**
7. **Collect** the evaluator-side per-cell DSI / PD-rate / generation table as a predictions asset
   in the t0114 schema (`spec_version: "2"`, gzipped JSON, fields `generation`, `vector_68d`,
   `objective_F_minimised`, `dsi_vector_sum` — back-compat field name storing ratio DSI — and
   `pd_rate_hz`).
8. **Compare** to t0106, t0112, t0113, t0114:
   * Joint-pass cell count (DSI ≥ 0.5 AND PD ≥ 30 Hz) absolute and as % of total evaluations.
   * Best ratio DSI and best PD-rate frontier vs the four prior seeds.
   * Full HV trajectory shape vs the four prior seeds.
   * Pareto front overlap in normalised z-scored 68-d parameter space against each prior seed.
   * **5-seed substrate-rate mean and SE** with the t0114 four-seed result as the prior.

## Expected Assets

* **1 predictions asset** at
  `tasks/t0115_seed9354_no_autostop/assets/predictions/t0115-bedb-morph-nsga2-seed9354/` containing
  the per-cell DSI / PD-rate / generation table for every evaluated cell, mirroring the t0114
  predictions asset schema.

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is for
  CPU cores; the GPU sits idle on the selected Vast.ai offer.
* **Remote**: Vast.ai single instance, same provisioning class as t0114, fully independent from the
  (now destroyed) t0114 instance.
* **Cost cap**: $25 per-task hard cap. **Per-instance watchdog**: $20.
* **Expected actual cost**: ~$1-5 (t0114 spent $0.94 stopping at gen 62 of 300; expect a similar
  per-gen rate at ~180 s/gen on EPYC 64-core). If the operator runs t0115 to the gen 300 ceiling,
  the cost lands near $5-6.
* **Project envelope check**: confirm project remaining budget covers $25 hard cap before
  provisioning. Project budget at t0114 start was $40.73; after t0114's $0.94 spend it is ~$39.79.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `hv_vs_gen_5seeds.png` — log-scale HV trajectory for all five seeds (44, 77, 2247, 7755, 9354)
   on the same axes with pool-restart events annotated.
2. `pareto_front_5seeds.png` — overlay of strict Pareto fronts from all five tasks on DSI vs
   PD-rate axes, coloured by source task.
3. `joint_pass_yield_per_gen_5seeds.png` — joint-pass cell count discovered per generation across
   all five seeds.
4. `top50_morphologies_seed9354.png` — 10x5 grid of best 50 cells from t0115, coloured by
   archetype.
5. `substrate_rate_5seed_with_literature.png` — 5-seed mean ± SE bar chart vs Hay 2011 (0.40 %)
   and Druckmann 2007 (0.10 %) literature baselines.

### Tables

* `results/data/joint_pass_summary_5seeds.csv` — per-seed (44, 77, 2247, 7755, 9354): total evals,
  joint-pass count, joint-pass %, best DSI, best PD-rate, stop trigger, stop generation.
* `results/data/pareto_front_overlap_5seeds.csv` — for each t0115 Pareto cell, the nearest-
  neighbour z-scored L2 distance in 68-d parameter space to its closest cell from each prior seed.

### Registered metrics

* `direction_selectivity_index` — best ratio DSI across all evaluated cells. Sub-variants
  `best_legit` (highest non-DSI = 1.0 cell), `overall_max`, `dsi_eq_one_count`.

Operational metrics (not registered): `joint_pass_count`, `best_pd_rate_hz`,
`n_cells_evaluated_total`, `n_gen_completed`, `stop_trigger`,
`efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`.

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative answer:

1. **Seed-9354 joint-pass count.** Does seed 9354 produce ≥ 40 unique legit joint-pass cells
   (t0106-like), 7-39 cells (t0112-like), 1-6 cells (sparse), or 0 (substrate not populated)?
2. **Best ratio DSI.** Does seed 9354's best legit ratio DSI reach or exceed 0.95?
3. **Best PD-rate.** Does seed 9354's best PD-rate reach or exceed 100 Hz?
4. **5-seed substrate-rate estimate.** Combining all 5 seeds, what is the substrate-level mean
   joint-pass acceptance rate and its standard error? Does the 5-seed mean fall within the Hay 2011
   (0.40 %) / Druckmann 2007 (0.10 %) literature envelope, or above it?
5. **Stop trigger.** Which mechanism actually stopped the run (operator, budget cap, gen ceiling,
   instance watchdog)?
6. **Per-gen wall-clock at extended N_GEN.** Does the cadence-10 pool-restart cycle continue to keep
   wall-clock near t0114's 180 s/gen sustained average?

## Risks and Fallbacks

* **Risk**: seed 9354 lands in the sparse regime (t0113-like) and contributes very little to the
  5-seed substrate-rate estimate. **Fallback**: this is still a valid datapoint; document
  prominently in results.
* **Risk**: Vast.ai instance is interrupted mid-run. **Fallback**: t0114-family driver writes HV
  trace + per-cell evaluations after every generation; resume from last completed generation if the
  orchestration shell script supports it, otherwise treat the partial run as the final result.
* **Risk**: operator forgets to issue a stop signal and the run goes to gen 300 / budget cap
  unattended. **Fallback**: acceptable — the gen ceiling and budget cap are the safety net for the
  "stop when I say so" directive.

## Cross-References

* **Parent tasks**: `t0106_long_pdnd_nsga2_300gen` (original substrate),
  `t0114_seed7755_no_autostop` (canonical fork base with auto-stop-disabled wiring).
* **Source suggestion**: `S-0112-01` (5-seed substrate-rate confirmation batch). This task is the
  5th and final seed.
* **Related suggestion**: `S-0113-03` (HV-plateau detector reparameterisation). The t0115 HV trace,
  like the t0114 trace, contributes to the offline detector-replay sweep in t0114's results stage.
* **Related caveat tasks**: `t0107_t0106_polar_8dir_recheck` (8-direction polar re-evaluation
  showing 2-direction ratio DSI overstates selectivity by ~0.42 absolute). Polar re-evaluation of
  any t0115 joint-pass cells is out of scope for this task.
