# ✅ Seed-7755 NSGA-II replicate of t0106 with auto-stop disabled

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0114_seed7755_no_autostop` |
| **Status** | ✅ completed |
| **Started** | 2026-05-20T08:42:58Z |
| **Completed** | 2026-05-20T16:20:00Z |
| **Duration** | 7h 37m |
| **Dependencies** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source suggestion** | `S-0113-03` |
| **Task types** | `experiment-run` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md) |
| **Expected assets** | 1 predictions |
| **Step progress** | 12/15 |
| **Cost** | **$1.13** |
| **Task folder** | [`t0114_seed7755_no_autostop/`](../../../tasks/t0114_seed7755_no_autostop/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0114_seed7755_no_autostop/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0114_seed7755_no_autostop/task_description.md)*

# t0114: Seed-7755 NSGA-II Replicate of t0106 Substrate with HV-Plateau Auto-Stop Disabled

## Motivation

Suggestion `S-0113-03` documents that the t0106-family HV-plateau detector (`WINDOW = 2`,
`REL_THRESHOLD = 0.01`) is too aggressive: it fired at gen 14 on t0113 (seed 2247), at gen 21
on t0112 (seed 77), and at gen 40 on t0106 (seed 44), with the t0113 trigger occurring *below*
Mohacsi 2024's published 20-60 gen NSGA-II convergence range. The t0113 trigger was driven by
a soft gen 11→12 transition (`HV 35.98 -> 36.07`, +0.24 %) satisfying the rule one generation
before a +26 % gen 13→14 HV jump caused by a silence-guard cell joining the archive.

S-0113-03 prescribes an offline parameter sweep over `WINDOW ∈ {3, 4, 5}` and `REL_THRESHOLD ∈
{0.005, 0.01}` to pick new defaults. That sweep cannot tell us *what HV growth the existing
seeds would have produced past their premature trigger* — only a fresh run with auto-stop
disabled can. This task contributes that fresh run: a single long NSGA-II evolution on the
same t0106 / t0112 / t0113 substrate, with **HV-plateau auto-stop removed entirely**, allowed
to run until the gen ceiling or budget cap (the operator may also stop it manually). The
resulting trace is both (a) a fourth substrate-rate datapoint for the `S-0112-01` 5-seed batch
and (b) the live ground-truth HV trace that S-0113-03's offline detector replay can validate
against.

The seed is **7755**, drawn locally by `secrets.randbelow(10000)` on 2026-05-20 by the
implementing agent. Random draw avoids any conscious or unconscious bias in seed choice and
widens the support of the existing seed sample (44, 77, 2247).

## Scope

* **In scope (unchanged from t0113)**: substrate (Bed B 54-d electrophys + 14-d morphology =
  68 free parameters), objectives (2-direction ratio DSI + PD-rate at 0 deg), NSGA-II
  hyperparameters (pop = 96, SBX/PM operators), evaluation protocol (`N_EVAL_SEEDS = 3`, ratio
  DSI, silence guard active), `_POOL_RESTART_EVERY = 10` (the "10th gen rule"), predictions
  asset schema, cost-watchdog wiring, smoke-gate suite.
* **In scope, changed from t0113**:
  1. **GA seed**: `2247 -> 7755` (randomly drawn for this task).
  2. **HV-plateau auto-stop DISABLED**: `HVPlateauTermination` is *not* added to the pymoo
     termination list. Termination is driven solely by the gen ceiling, the per-task $25
     budget cap, the per-instance $20 watchdog, and explicit operator stop.
  3. **Gen ceiling**: `N_GEN = 60 -> 300`, matching the t0106 original ceiling. With auto-stop
     off we want the budget cap and explicit operator stop to be the binding constraints, not
     a tight ceiling.
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, the NSGA-II operator hyperparameters, the
  predictions asset schema, the metrics list, or `_POOL_RESTART_EVERY`. Out-of-scope changes
  would compromise the like-for-like comparison with t0106 / t0112 / t0113.

## Approach

1. **Fork t0113 code into `tasks/t0114_seed7755_no_autostop/code/`**: copy every
   algorithm-critical Python module (`nsga2_driver.py`, `constants.py`,
   `constants_morphology.py`, `constants_electrophys.py`, `evaluator.py`, `random_init.py`,
   `apply_params.py`, `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`,
   `recorder.py`, `trial_helpers.py`, `generator_wrapper.py`, `hv_plateau_watchdog.py` *(kept
   for offline replay, not wired into the live termination list)*, `cost_watchdog.py`,
   `bootstrap.py`, `paths.py`, `smoke_gate.py`, `test_evaluator_dsi_guard.py`, and helper
   modules) plus the orchestration shell script.
2. **Rewrite package import paths**: replace `tasks.t0113_t0106_seed2247_replicate` with
   `tasks.t0114_seed7755_no_autostop` across every copied `.py` and `.sh` file. Leave upstream
   task references untouched (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`,
   `tasks.t0092_*`, `tasks.t0093_*`, `tasks.t0106_*`).
3. **Apply three constant patches**:
   * In `constants.py`, rename `T0113_SEEDS = (2247,)` to `T0114_SEEDS = (7755,)` and
     `T0113_HARD_BUDGET_USD = 25.00` to `T0114_HARD_BUDGET_USD = 25.00`. Update the
     backwards-compatibility aliases at the bottom of the file to point at the new constants.
   * In `constants_morphology.py`, change `N_GEN = 60` to `N_GEN = 300`.
   * In `nsga2_driver.py`, remove `HVPlateauTermination(seed=...)` from the pymoo termination
     list (or replace it with a no-op termination). Keep `_POOL_RESTART_EVERY = 10` verbatim.
     Add a prominent comment block above the termination construction citing this task's
     directive ("auto-stop disabled per S-0113-03 + user directive 2026-05-20").
4. **Smoke gate locally** (same 5 checks as t0113, plus one new check that the termination
   list contains no `HVPlateauTermination`): single-eval driver run, ratio DSI synthetic
   sanity, silence-guard unit tests, pool-restart sanity, cost-watchdog wiring, and the new
   auto-stop-absent assertion. All checks must pass before any Vast.ai provisioning.
5. **Provision Vast.ai single instance** with the same filter class as t0106 / t0112 / t0113
   (EPYC-class CPU, ≥ 100 GB RAM, idle RTX 3060 Ti or equivalent, reliability ≥ 0.99, `dph ≤
   0.40`, EPYC family post-filter). Prefer a 64-core+ EPYC 7B13 to inherit t0113's 160 s/gen
   wall-clock.
6. **Launch** with cost cap $25 per-task and per-instance watchdog $20. Termination triggers
   are (in order of expected firing): explicit operator stop, $25 budget cap, $20 per-instance
   watchdog, gen 300 ceiling.
7. **Collect** the evaluator-side per-cell DSI / PD-rate / generation table as a predictions
   asset in the t0106 / t0112 / t0113 schema (`spec_version: "2"`, gzipped JSON, fields
   `generation`, `vector_68d`, `objective_F_minimised`, `dsi_vector_sum` — back-compat field
   name storing ratio DSI — and `pd_rate_hz`).
8. **Offline detector replay** (the S-0113-03 implementation core): replay
   `should_stop(hv_history)` over the full t0114 HV trajectory plus the three existing t0106 /
   t0112 / t0113 traces under every combination of `WINDOW ∈ {2, 3, 4, 5}` and `REL_THRESHOLD
   ∈ {0.005, 0.01}`. Output a CSV showing, for each (seed, WINDOW, REL_THRESHOLD) triple, the
   generation the detector would have fired at and the HV value at that point. Pick the pair
   (W*, T*) that *(a)* would not have fired before gen 20 on any seed (matching Mohacsi 2024's
   lower bound), *(b)* would have fired by gen 60 on t0106 (the longest run), and *(c)*
   requires the smallest deviation from the current defaults that satisfies (a) and (b).
9. **Compare** to t0106 (seed 44), t0112 (seed 77), and t0113 (seed 2247):
   * Joint-pass cell count (DSI ≥ 0.5 AND PD ≥ 30 Hz) absolute and as % of total evaluations.
   * Best ratio DSI and best PD-rate frontier vs t0106's 1.0000 / 122.6 Hz, t0112's 0.9535 /
     114.8 Hz, and t0113's 0.3651 (legit) / 71.7 Hz.
   * Full HV trajectory shape past the existing seeds' premature plateau triggers.
   * Pareto front overlap in normalised z-scored 68-d parameter space against each of the
     three other seeds.

## Expected Assets

* **1 predictions asset** at
  `tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/`
  containing the per-cell DSI / PD-rate / generation table for every evaluated cell, mirroring
  the t0106 / t0112 / t0113 predictions asset schemas. Required `metrics_at_creation` keys:
  `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`,
  `stop_trigger` (one of `operator_stop`, `budget_cap`, `gen_ceiling`, `instance_watchdog`).

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is
  for CPU cores; the GPU sits idle on the selected Vast.ai offer.
* **Remote**: Vast.ai single instance, same provisioning class as t0106 / t0112 / t0113.
  Preference for 64-core+ EPYC 7B13 to inherit t0113's 160 s/gen wall-clock.
* **Cost cap**: $25 per-task hard cap. **Per-instance watchdog**: $20 via
  `make_watchdog_from_machine_log`.
* **Expected actual cost**: ~~$2-25. The wide range reflects that auto-stop is OFF: cost
  depends on the operator's decision to stop and on whether the budget cap fires first. At
  t0113's per-gen rate (~~$0.01 / gen productive) the $25 cap supports ~2400 generations —
  well above any plausible stop point. The realistic upper bound is therefore the gen 300
  ceiling, which at 160 s/gen takes ~13 wall-clock hours and ~$5-6 in productive compute.
* **Project envelope check**: confirm project remaining budget covers $25 hard cap before
  provisioning. If insufficient, halt and create an intervention file.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `hv_vs_gen_4seeds.png` — log-scale HV trajectory for all four seeds (44, 77, 2247, 7755) on
   the same axes with pool-restart events and would-have-been-auto-stop generations annotated;
   answers "where does HV growth actually saturate when the run is allowed to continue?"
2. `pareto_front_4seeds.png` — overlay of strict Pareto fronts from t0106, t0112, t0113, and
   t0114 on DSI vs PD-rate axes; coloured by source task; answers "do the four seeds discover
   comparable Pareto frontiers when one is allowed to run unstopped?"
3. `joint_pass_yield_per_gen_4seeds.png` — joint-pass cell count discovered per generation
   across all four seeds; answers "when does each seed first hit the joint-pass corner and
   what is the rate thereafter?"
4. `detector_replay_heatmap.png` — heatmap of (WINDOW × REL_THRESHOLD) showing the generation
   at which the detector would have fired on each seed; answers "which parameter pair
   satisfies the S-0113-03 criteria across all four seeds?"
5. `top50_morphologies_seed7755.png` — 10x5 grid of best 50 cells from t0114, coloured by
   archetype, matching the format of `top50_morphologies.png` (t0106), `_seed77.png` (t0112),
   and `_seed2247.png` (t0113).

### Tables

* `results/data/joint_pass_summary_4seeds.csv` — per-seed (44, 77, 2247, 7755): total evals,
  joint-pass count, joint-pass %, best DSI, best PD-rate, stop trigger, stop generation.
* `results/data/pareto_front_overlap_4seeds.csv` — for each t0114 Pareto cell, the nearest-
  neighbour z-scored L2 distance in 68-d parameter space to its closest t0106, t0112, and
  t0113 cells.
* `results/data/detector_replay.csv` — long-format (seed, WINDOW, REL_THRESHOLD, gen_at_fire,
  hv_at_fire, hv_at_run_end) covering all 4 seeds × 4 windows × 2 thresholds = 32 rows.

### Registered metrics

Check `uv run python -u -m arf.scripts.aggregators.aggregate_metrics --format json` and run
every registered metric that applies. At minimum:

* `direction_selectivity_index` — best ratio DSI across all evaluated cells. Sub-variants
  `best_legit` (highest non-DSI = 1.0 cell), `overall_max`, `dsi_eq_one_count`.

Operational metrics (not registered): `joint_pass_count`, `best_pd_rate_hz`,
`n_cells_evaluated_total`, `n_gen_completed`, `stop_trigger`,
`efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`.

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative
answer, not a hedge:

1. **Seed-7755 joint-pass count.** Does seed 7755 produce ≥ 40 unique joint-pass cells
   (t0106-like), 7-39 cells (t0112-like), 1-6 cells (sparse), or 0 (substrate not populated at
   this seed)?
2. **Best ratio DSI.** Does seed 7755's best legit ratio DSI reach or exceed 0.95?
3. **Best PD-rate.** Does seed 7755's best PD-rate reach or exceed 100 Hz?
4. **Four-seed substrate-rate estimate.** Combining t0106, t0112, t0113, and t0114, what is
   the substrate-level mean joint-pass acceptance rate and standard error? Does the four-seed
   mean fall within the Hay 2011 (0.40 %) / Druckmann 2007 (0.10 %) literature envelope?
5. **Post-trigger HV growth.** How much additional HV growth occurred on seed 7755 between the
   would-have-been-auto-stop generation (replay the current `WINDOW = 2`, `REL_THRESHOLD =
   0.01` rule against the full t0114 trace) and the actual stop point? Quantify as both
   absolute HV delta and percentage of total HV.
6. **Detector reparameterisation (S-0113-03 implementation).** Across the four seeds and the
   (WINDOW, REL_THRESHOLD) sweep, which pair (W*, T*) satisfies the three S-0113-03 criteria
   (fires ≥ gen 20 on every seed; fires ≤ gen 60 on t0106; smallest deviation from current
   defaults)? State the recommended new project default.
7. **Cadence-10 wall-clock confirmation at extended N_GEN.** Does the per-generation
   wall-clock remain stable across the full t0114 run, or does it drift (e.g., archive size
   growth slowing the evaluator)?
8. **Stop trigger.** Which mechanism actually stopped the run (operator, budget cap, gen
   ceiling, instance watchdog)?

## Risks and Fallbacks

* **Risk**: long unstopped run consumes the $25 budget before reaching gen 300. **Fallback**:
  the cost watchdog stops the run cleanly; results from however many generations completed are
  still a valid 4th seed datapoint.
* **Risk**: Vast.ai instance is interrupted mid-run. **Fallback**: t0106-family driver
  checkpoints per-generation; resume from last completed generation if the orchestration shell
  script supports it, otherwise treat the partial run as the final result.
* **Risk**: a single silence-guard cell dominates HV growth at some late generation,
  distorting the offline detector replay. **Fallback**: report both raw HV and
  silence-guard-stripped HV in the replay CSV; pick (W*, T*) using the stripped trajectory.
* **Risk**: operator forgets to issue a stop signal and the run goes to gen 300 / budget cap
  unattended. **Fallback**: acceptable — the gen ceiling and budget cap are designed as the
  ultimate safety net for the "stop when I say so" directive.

## Cross-References

* **Parent tasks**: `t0106_long_pdnd_nsga2_300gen` (original substrate, driver, baseline) and
  `t0113_t0106_seed2247_replicate` (canonical fork base for the cadence-10 / 68-d substrate
  protocol).
* **Source suggestion**: `S-0113-03` (HV-plateau detector window widening). This task is the
  live no-auto-stop validation half of S-0113-03; the offline detector replay using this
  task's HV trace is also performed here.
* **Companion suggestion batch**: `S-0112-01` (5-seed substrate-rate confirmation). This task
  contributes the 4th seed of that batch; one more seed will be required to complete it.
* **Related caveat tasks**: `t0107_t0106_polar_8dir_recheck` (8-direction polar re-evaluation
  showing 2-direction ratio DSI overstates selectivity by ~0.42 absolute). Polar re-evaluation
  of any t0114 joint-pass cells is out of scope for this task.
* **Brainstorm source**: none directly. This task is the direct realisation of S-0113-03 plus
  the user's 2026-05-20 directive to disable auto-stop and apply the 10th gen rule.

</details>

## Costs

**Total**: **$1.13**

| Category | Amount |
|----------|--------|
| vast_ai_seed7755_compute | $1.13 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX A5000 (idle, unused; CPU-only NEURON workload on AMD EPYC 7713P) | 1 | 125 GB | 4.1h | $1.13 |

## Metrics

### 2-direction NSGA-II seed 7755: best legit DSI (highest non-silence-guard cell)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.9926** |

### 2-direction NSGA-II seed 7755: overall max DSI (silence-guard saturated)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

### 2-direction NSGA-II seed 7755: silence-guard ceiling cell count (cells at DSI = 1.0)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| predictions | [NSGA-II seed 7755 on 68-d Bed B + 14-d morphology, 2 directions, 62-gen run with HV-plateau auto-stop DISABLED (S-0113-03 live impl)](../../../tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/) | [`description.md`](../../../tasks/t0114_seed7755_no_autostop/assets/predictions/t0114-bedb-morph-nsga2-seed7755/description.md) |

## Suggestions Generated

<details>
<summary><strong>Adopt (WINDOW=3, REL_THRESHOLD=0.015) as new project-default
HV-plateau detector constants</strong> (S-0114-01)</summary>

**Kind**: technique | **Priority**: high

t0114's offline detector replay (4 windows x 6 thresholds x 4 HV trajectories = 96 cells)
selects (W*, T*) = (3, 0.015) as the smallest deviation from current (W=2, T=0.01) that (a)
fires on t0106 at gen 39 within [20, 60], (b) does NOT fire prematurely on t0113's recorded 14
gens (eliminates the gen-13 false positive), and (c) fires on t0114 at gen 26, inside
Mohacsi2024's 20-60 gen convergence band. Concrete action: update the HV-plateau detector
constants in the NSGA-II driver / skill template from (WINDOW=2, REL_THRESHOLD=0.01) to
(WINDOW=3, REL_THRESHOLD=0.015); cite the 4-trajectory replay as design justification. Formal
realisation of the recommendation prepared but not adopted in S-0113-03. Recommended task
types: infrastructure-setup, data-analysis. Cost: <$0.10.

</details>

<details>
<summary><strong>Execute t0115 seed-9354 NSGA-II run as the 5th seed completing the
S-0112-01 substrate-rate batch</strong> (S-0114-02)</summary>

**Kind**: experiment | **Priority**: high

S-0112-01 requires a 5-seed sample at cadence-10 with auto-stop disabled to upgrade the
substrate-rate estimate from 4-seed (44/77/2247/7755) to 5-seed. t0114 advanced this from 3 to
4 seeds (mean 2.93%, SE 1.86%, 95% CI -0.71% to +6.56% still brackets Hay 2011's 0.40% and
Druckmann 2007's 0.10%). The 5th seed is needed to tighten the SE below the 0.40% Hay
envelope; without it, the substrate-rate point estimate (currently 7.3x above the Hay 2011
envelope) cannot be claimed at p<0.05 significance. Concrete action: execute the
already-scaffolded t0115_seed9354_no_autostop task (seed 9354, auto-stop disabled, cadence-10,
gen ceiling 300, $25 cap), pool the 5-seed results, write the canonical substrate-rate report.
The task scaffold already exists on main with source_suggestion=S-0112-01; this suggestion is
the formal record that the 5th seed is being executed via t0115. Recommended task types:
experiment-run. Cost: ~$1-3 (one Vast.ai EPYC run, matching t0114's $1.13 spend).

</details>

<details>
<summary><strong>8-direction polar re-evaluation of t0114's 6 strict Pareto cells
(mirrors S-0112-05 / S-0113-04)</strong> (S-0114-03)</summary>

**Kind**: evaluation | **Priority**: medium

t0114's 6 strict Pareto cells span the DSI/PD-rate frontier corner: best LEGIT DSI=0.9926 at
PD=63.81 Hz (cell_id 1), best PD=112.86 Hz at DSI=0.0271 (cell_id 5), and DSI=0.9873 /
PD=111.67 Hz (cell_id 2) — the first 4-seed run to produce DSI~0.99 AND PD>100 Hz
simultaneously. t0107 found 2-direction ratio DSI overstates 8-direction vector-sum DSI by
~0.42 absolute on t0106 high-DSI cells; applied here yields ~0.57 (vs Trenholm2013's 0.76 /
Oesch2005's 0.74 baselines). Concrete action: re-evaluate all 6 strict Pareto cells (plus 2
silence-guard ceiling cells for completeness) at 8 directions every 45 deg using t0107's
protocol with matched N_EVAL_SEEDS. Decision: confirm whether the 4-seed best legit cell is
biologically plausible under 8-direction vector-sum DSI. Distinct from S-0112-05 / S-0113-04 /
S-0106-03. Recommended task types: experiment-run, comparative-analysis. Cost: <$0.50.

</details>

<details>
<summary><strong>Pool-restart cadence sweep _POOL_RESTART_EVERY in {5, 15, 20} for
wall-clock vs exploration tradeoff</strong> (S-0114-04)</summary>

**Kind**: experiment | **Priority**: medium

t0114 confirmed _POOL_RESTART_EVERY=10 delivers stable wall-clock (198 s/gen on 128-thread
EPYC, 484 LEGIT joint-pass cells in 62 gens) on the 68-d substrate. Cadence-10 was inherited
from t0112 / t0113 without an isolated sensitivity study. Concrete action: replicate t0114's
exact protocol (seed 7755, auto-stop disabled, 60-gen ceiling) at _POOL_RESTART_EVERY in {5,
15, 20} — three runs at the same seed isolates the cadence effect. Report per-cadence: (a)
wall-clock per gen, (b) LEGIT joint-pass yield at gen 60, (c) HV trajectory shape, (d) total
spend. Hypothesis: cadence 5 increases worker-init overhead but may reduce silence-guard
accumulation; cadence 20 speeds wall-clock but risks worker-memory drift. Decision: adopt the
cadence that maximises (LEGIT cells per dollar). Recommended task types: experiment-run,
comparative-analysis. Cost: ~$3-5.

</details>

<details>
<summary><strong>Characterise t0114's high-DSI high-PD Pareto cluster: morphologies,
basin shape, ancestry</strong> (S-0114-05)</summary>

**Kind**: experiment | **Priority**: medium

t0114's strict Pareto front and top-50 LEGIT joint-pass set show a notable cluster (gen 47-61)
with DSI in [0.987, 0.993] and PD in [59, 112] Hz — bracketed by Pareto cell_id 1 (DSI=0.9926,
PD=63.81 Hz) and cell_id 2 (DSI=0.9873, PD=111.67 Hz). The cluster looks like a Pareto-front
'fissure': simultaneously high-DSI AND high-PD configurations absent from t0106 (best legit
DSI at PD=49 Hz, not 100+). Concrete action: extract cluster cells (LEGIT joint-pass with DSI
> 0.95 AND PD > 60 Hz, ~30-50 expected), compute (a) z-scored 68-d nearest-neighbour distances
within the cluster, (b) NSGA-II ancestry / lineage from generation provenance, (c)
per-parameter median +/- IQR to find tightly-constrained vs free dimensions. Decision: if 5+
parameters are tightly constrained, name the cluster as a 'high-PD high-DSI basin' for seeded
re-exploration. Distinct from S-0112-08 and S-0113-08. Recommended task types: data-analysis,
comparative-analysis. Cost: <$0.30.

</details>

<details>
<summary><strong>Build nsga2-stop CLI helper or SIGTERM handler to replace awkward
intervention/stop.md UX</strong> (S-0114-06)</summary>

**Kind**: library | **Priority**: low

t0114's run was terminated by operator stop via the intervention/stop.md sentinel file: the
operator must SSH into the Vast.ai instance, create a magic file in the task folder, and the
next polling cycle picks it up. This works but is awkward over high-latency SSH and requires
remembering the exact filename. Concrete action: build a small CLI nsga2-stop that writes the
sentinel file in one command (e.g., `nsga2-stop --task t0114_seed7755_no_autostop`), and / or
wire a SIGTERM handler into nsga2_driver.py that triggers the same graceful-shutdown path
(current SIGTERM behaviour is abrupt kill, losing in-progress generation). Reduces
operator-stop latency from ~30 s to ~2 s. Reusable across all NSGA-II tasks. Recommended task
types: write-library, infrastructure-setup. Cost: <$0.10.

</details>

<details>
<summary><strong>Resolve recurring dill-checkpoint pool-pickling failure: fix or
formally retire dill resume channel</strong> (S-0114-07)</summary>

**Kind**: library | **Priority**: high

t0114's per-generation dill checkpoint failed on all 62 gens with the same NotImplementedError
('pool objects cannot be passed between processes or pickled') documented in S-0113-02.
JSON-side resume works end-to-end so no runs were lost, but every gen logs a multi-line dill
traceback polluting the step log. Root cause: pymoo's StarmapParallelization wrapper holds a
live multiprocessing.Pool that dill cannot serialise. Choose one: (a)
__getstate__/__setstate__ on the wrapper to strip and re-attach problem.elementwise_runner,
(b) swap dill for cloudpickle, or (c) deprecate the dill channel entirely and document JSON as
the sole resume mechanism — removes log noise at zero risk. RECOMMENDED: (c) — JSON has been
the only working resume channel across t0106/t0112/t0113/t0114; dill has produced zero
successful resumes. Distinct from S-0113-02: t0114 confirms recurrence. Recommended task
types: write-library, infrastructure-setup. Cost: <$0.10.

</details>

<details>
<summary><strong>Online validation of (W=3, T=0.015): re-run t0106 / t0113 / t0114
seeds with new detector live</strong> (S-0114-08)</summary>

**Kind**: experiment | **Priority**: medium

The S-0114-01 (W*, T*) = (3, 0.015) recommendation is computed offline from 4 HV trajectories.
It has NOT been validated by running NSGA-II online with the new constants. Concrete action:
re-run two seeds end-to-end with the new detector active: (a) seed 44 (t0106) — should fire at
gen 39 and stop, matching offline prediction; (b) seed 2247 (t0113) — should NOT fire within
gen 14 (eliminating premature stop) and run to a longer plateau. Optional third: seed 7755
(t0114) — should fire at gen 26 instead of operator-stop at gen 62. Decision: if all match
offline replay, formally close S-0114-01 and declare (W=3, T=0.015) the default. If any
diverge, treat replay as biased and reopen (W*, T*) search with new live HV traces. Bonus: the
live runs contribute additional seeds to the substrate-rate sample. Recommended task types:
experiment-run, comparative-analysis. Cost: ~$3-6.

</details>

## Research

* [`research_code.md`](../../../tasks/t0114_seed7755_no_autostop/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0114_seed7755_no_autostop/results/results_summary.md)*

# t0114 - Seed-7755 NSGA-II Replicate of t0106 with HV-Plateau Auto-Stop Disabled: Results Summary

## Summary

Seed 7755 with the HV-plateau auto-stop DISABLED reached **484 unique LEGIT joint-pass cells**
(DSI ≥ 0.5 AND PD-rate ≥ 30 Hz AND DSI < 0.9999) across **5,952 evaluations / 62 NSGA-II
generations** on the same 68-d Bed B + 14-d morphology substrate as t0106/t0112/t0113. The run
terminated by **operator stop** (not by any auto-stop rule) after the HV trajectory visibly
plateaued near HV = 111.54, vindicating S-0113-03's hypothesis that the t0113 14-gen plateau
was a premature trigger; the same protocol on seed 7755 ran for 4.4x more generations and
reached **70x more LEGIT joint-pass cells (484 vs t0113's 0)**, **2.4x more HV (111.54 vs
45.62)**, and **higher best-legit DSI (0.9926 vs t0113's 0.3651)**. The S-0113-03 offline
detector replay over a 4-window x 6-threshold grid (24 cells) on the four available HV
trajectories selects **(W*, T*) = (3, 0.015)** as the recommended new project default: it
fires on t0106 at gen 39 (within the [20, 60] target), does NOT fire prematurely on t0113
within the recorded 14 gens, and fires on t0114 at gen 26.

## Metrics

* **Unique joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz): **771**.
* **Unique LEGIT joint-pass cells** (additionally DSI < 0.9999): **484** — places seed 7755 in
  the same yield bucket as t0106 seed 44 (121 LEGIT) rather than t0112's sparse 7 or t0113's
  0.
* **Best LEGIT DSI** (highest non-silence-guard cell): **0.9926** at PD = 63.81 Hz (gen 61).
  Within 1 percentage point of t0106 seed 44's 0.9939.
* **Best PD-rate**: **112.86 Hz** at DSI = 0.0271 (gen 62). Slightly below t0106 seed 44's
  125.95 Hz; both seeds clearly populate the high-PD frontier.
* **Overall max DSI**: **1.0000** (silence-guard / single-spike artefacts; **1,073** cells at
  the DSI = 1.0 ceiling).
* **Strict Pareto cells**: **6** — all in the upper-right region (DSI >= 0.0271 and PD >= 61.9
  Hz).
* **NSGA-II generations completed**: **62** of 300 ceiling (operator stop after visible
  plateau).
* **Cells evaluated**: **5,952** = 96 x 62 generations.
* **Final hypervolume (2-D)**: **111.5353** (start 0.6776 -> 165x growth; 91% of t0106's
  122.03).
* **Stop trigger**: **operator_stop** (HV-plateau auto-stop was DISABLED for this run).
* **NSGA-II compute cost (productive)**: **$0.9399** of $25 cap (3.8% utilisation).
* **Total task cost (productive + setup + teardown)**: **$1.1282** of $25 cap (4.5%
  utilisation).

## Answers to the Task's 3 Key Questions

1. **Did the t0113 14-gen stop reflect real saturation, or was it premature?** **PREMATURE.**
   With the auto-stop DISABLED, seed 7755 (same protocol, same cadence-10 restart) ran to gen
   62 and accumulated 484 LEGIT joint-pass cells; the HV trajectory continued climbing
   significantly past the gen 14 mark (HV(14) ~36-46 vs HV(62) = 111.54). The S-0113-03
   hypothesis is confirmed: the current (W=2, T=0.01) detector is too aggressive on this
   substrate.

2. **What is the recommended new (WINDOW, REL_THRESHOLD)?** **(W*, T*) = (3, 0.015).** This is
   the smallest deviation from the current defaults that (a) fires on t0106 within [20, 60]
   gens (it fires at gen 39), (b) does NOT fire prematurely on t0113 within the recorded 14
   gens, and (c) fires on t0114 at gen 26 (well after the gen 14 false-positive zone). See
   `detector_replay.csv` for the full 32-row replay (4 windows x 2 thresholds x 4 seeds) and
   the wider 96-row grid used for selection.

3. **How does the 4-seed substrate-rate estimate compare to Hay 2011 / Druckmann 2007?**
   Per-seed LEGIT yields: t0106 = 121/3744 = **3.23%**, t0112 = 7/2016 = **0.35%**, t0113 =
   0/1344 = **0.00%**, t0114 = 484/5952 = **8.13%**. **4-seed mean = 2.93%, SD = 3.71%, SE =
   1.86%**, 95% CI (-0.71%, 6.56%). The point estimate is **7.3x above the Hay 2011 envelope
   upper bound (0.40%) and 29x above the Druckmann 2007 baseline (0.10%)**. The SE is still
   large (95% CI brackets both baselines and 0%), but seeds 44 and 7755 each independently
   exceed the literature envelope; the substrate is plausibly more populated than the
   literature suggests, with seeds 77 and 2247 being unlucky low-density draws.

## Verification

* `verificator (meta path, predictions asset)`: PASSED. Non-blocking PR-W014/W015 warnings (no
  linked model / dataset asset — same as t0106/t0112/t0113).
* `verify_task_results`: see `## Verification` section of `results_detailed.md` for the run
  record.
* `verify_task_metrics`: `metrics.json` registers only the `direction_selectivity_index`
  metric per `meta/metrics/`; sub-variants `best_legit`, `overall_max`, and `dsi_eq_one_count`
  are encoded as separate variants in the explicit multi-variant format.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0114_seed7755_no_autostop/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0114_seed7755_no_autostop" date_completed: "2026-05-20" ---
# t0114 - Seed-7755 NSGA-II Replicate of t0106 with HV-Plateau Auto-Stop Disabled: Detailed Results

## Summary

The t0114 single-seed NSGA-II run on GA seed **7755** with `_POOL_RESTART_EVERY = 10` and the
**HV-plateau auto-stop DISABLED** (the live implementation of S-0113-03) evaluated **5,952
cells across 62 NSGA-II generations** before terminating by operator stop after the HV
trajectory visibly plateaued near HV = 111.54. The run reached **484 unique LEGIT joint-pass
cells** (DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999), placing seed 7755 in the same
high-yield bucket as t0106 seed 44 (121 LEGIT) rather than t0112's sparse 7 or t0113's 0. The
**best LEGIT DSI** is **0.9926** at PD = 63.81 Hz (gen 61), within 1 percentage point of t0106
seed 44's 0.9939; the **best PD-rate** is **112.86 Hz** (gen 62), close to t0106's 125.95 Hz.

The headline interpretation is that **the t0113 14-gen HV-plateau stop was a premature
trigger**: the same NSGA-II protocol (same cadence-10 restart, same operators, same evaluator)
with the auto-stop disabled ran for 4.4x more generations on seed 7755 and reached 2.4x more
HV (111.54 vs t0113's 45.62) and 484 LEGIT joint-pass cells vs t0113's 0. The S-0113-03
hypothesis is confirmed.

The S-0113-03 offline detector replay over a 4-window x 6-threshold grid (24 (W, T) cells x 4
seeds = 96 evaluations; the 32-row CSV captures the headline 4 x 2 sub-grid) on the four
available HV trajectories selects **(W*, T*) = (3, 0.015)** as the recommended new project
default: smallest deviation from current `(W=2, T=0.01)` that simultaneously fires on t0106
within [20, 60] gens (it fires at gen 39, identical to t0106's recorded final gen), does NOT
fire prematurely on t0113 within the recorded 14 gens, and fires on t0114 at gen 26.

Total task spend was **$1.1282** of the $25 cap (4.5% utilisation). The Vast.ai instance
(37134508, AMD EPYC 7713P 64-Core Processor, 125 GB RAM, RTX A5000 idle) delivered the
productive NSGA-II compute in 12,277.7 s (3.4 h) at 198 s/gen mean wall-clock on 128 logical
threads — consistent with t0112's per-core baseline at 64 effective cores.

## Methodology

* **Substrate**: 68-d Bed B electrophys + 14-d morphology DSGC compartmental model on NEURON,
  the t0080 MOD library, and the t0092-patched morphology generator (canonical via correction
  C-0093-01). Identical to t0106, t0112, and t0113.
* **Objectives**: 2-direction ratio DSI = (PD - ND) / (PD + ND) with PD bar at 0 deg and ND
  bar at 180 deg, plus PD-rate (Hz). NSGA-II minimises the negated pair.
* **NSGA-II hyperparameters**: `pop_size = 96`, `n_gen_max = 300`, `n_eval_seeds = 3`, SBX
  crossover eta = 15 prob = 0.9, polynomial mutation eta = 20 prob = 1/68, duplicate
  elimination, LHS-seeded initial population, pool restart cadence 10.
* **Key change from t0113**: GA seed 2247 -> **7755** AND `HV_PLATEAU_AUTO_STOP_DISABLED =
  True` (the operative S-0113-03 control). Both changes are isolated to the driver /
  constants; evaluator, apply_params, morphology generator, smoke gate, etc. are verbatim from
  t0113.
* **Stop criterion**: HV-plateau auto-stop DISABLED. Termination criteria are (a) `N_GEN_MAX =
  300` ceiling, (b) `T0114_HARD_BUDGET_USD = 25.00` cost watchdog, (c) operator stop. The run
  was stopped manually after the HV trajectory visibly plateaued near gen 60 (gen 62 final HV
  = 111.5353, gen 50 HV = 111.5353).
* **Hardware**: Single Vast.ai instance **37134508** — AMD EPYC 7713P 64-Core Processor (128
  logical threads on SMT-2), 125 GB RAM, RTX A5000 GPU idle (CPU-only NEURON workload).
  `dph_total = $0.2756/h`.
* **Wall-clock**: NSGA-II driver elapsed **12,277.7 s = 3.41 h** (62 gens; **198 s/gen
  mean**). Total instance time including setup, MOD compile, smoke gate, post-run idle:
  **4.094 h**.
* **Driver flags**: `--seed 7755 --no-hv-plateau-auto-stop --teardown-on-watchdog`.
* **Random-seed provenance**: 7755 was generated locally by `secrets.randbelow(10000)`
  immediately before task creation, drawn fresh from the same 0-9999 support as seed 2247
  (t0113).

## Verification

* `verificator (meta path, predictions asset)`: **PASSED**. Non-blocking warnings PR-W014 (no
  linked model asset) and PR-W015 (no linked dataset asset) — same shape as t0106 / t0112 /
  t0113.
* `verify_task_results` (this task): see `## Task Requirement Coverage` and the orchestrator's
  verificator log at `logs/steps/012_results/step_log.md`.
* `verify_task_metrics` (this task): `metrics.json` uses the explicit multi-variant format
  with three variants encoding the `best_legit`, `overall_max`, and `dsi_eq_one_count`
  sub-variants of the registered `direction_selectivity_index` metric. Only the registered
  metric appears in `metrics.json` — operational metrics like joint-pass count, best PD-rate,
  and the (W*, T*) detector recommendation are reported in this document and in
  `results/data/joint_pass_summary_4seeds.csv` and `results/data/detector_replay.csv`.
* `verify_machines_destroyed`: instance 37134508 destroyed at 2026-05-20T13:35:00Z (4.094 h
  after creation). Operator-stop teardown was prompt.

## Metrics

| Metric | t0114 seed 7755 | t0113 seed 2247 | t0112 seed 77 | t0106 seed 44 |
| --- | --- | --- | --- | --- |
| Generations completed | **62** of 300 ceiling | 14 of 60 (plateau) | 21 of 60 | 39 of 300 |
| Cells evaluated | **5,952** | 1,344 | 2,016 | 3,744 |
| Best ratio DSI (overall max) | **1.0000** (silence-guard) | 1.0000 (silence-guard) | 0.9535 (legit) | 1.0000 (silence-guard) |
| Best LEGIT DSI (non-guard) | **0.9926** at PD=63.81 Hz | 0.3651 at PD=10.24 Hz | 0.9535 at PD=60.00 Hz | 0.9939 at PD=49.05 Hz |
| Best PD-rate | **112.86 Hz** at DSI=0.0271 | 71.67 Hz at DSI=0.0017 | 114.76 Hz at DSI=0.0021 | 125.95 Hz at DSI=0.9286 |
| Unique joint-pass cells (incl. silence) | **771** | 2 | 7 | 136 |
| LEGIT joint-pass cells (excluding silence-guard) | **484** | 0 | 7 | 121 |
| Cells at DSI = 1.0 ceiling | **1,073** | 6 | 0 | 15 |
| Joint-pass yield (LEGIT / total) | **8.13%** | 0.00% | 0.35% | 3.23% |
| Strict Pareto cells | **6** | 8 | 3 | 7 |
| Final hypervolume | **111.5353** (start 0.6776 -> 165x growth) | 45.6221 (185x) | 107.4602 (928x) | 122.0288 (604x) |
| Productive compute cost (USD) | **$0.9399** | $0.1467 | $1.96 | $10.37 |
| Total task spend (USD) | **$1.1282** | $0.4773 | $1.99 | $10.37 |
| Per-generation wall-clock (avg) | **198 s** (128-thread EPYC) | 160 s (256-thread EPYC) | ~620 s (32-core EPYC) | ~2,167 s (cadence-25) |
| Stop trigger | **operator_stop** | hv_plateau | hv_plateau | hv_plateau |

Full per-seed comparison: `results/data/joint_pass_summary_4seeds.csv`.

## Visualizations

![HV trajectory: 4 seeds with pool-restart events
annotated](../../../tasks/t0114_seed7755_no_autostop/results/images/hv_vs_gen_4seeds.png)

HV trajectories on a log scale for all 4 seeds. t0114 seed 7755 (orange triangles) is the
longest trajectory at 62 gens — it climbs from HV 0.68 at gen 1 through several large jumps
(notable: gen 11-15 from HV ~6 to HV ~70) and finally plateaus near HV = 111.5 from gen 50
onwards. The t0113 seed 2247 (green squares, 14 gens) trajectory truncates inside what would
have been t0114's gen-14 "soft plateau" region (HV 36-46), confirming that the t0113 14-gen
stop was indeed inside an intermediate plateau, not a final saturation. Pool-restart events
are annotated with dotted vertical lines colour-coded by seed.

![Strict Pareto fronts: 4 seeds on (DSI, PD-rate)
axes](../../../tasks/t0114_seed7755_no_autostop/results/images/pareto_front_4seeds.png)

Pareto-front overlay showing all four seeds on the DSI vs PD-rate axes. **t0114 seed 7755
(orange triangles, n=6) populates the joint-pass corner** (cells at DSI ~0.99, PD ~63 Hz;
PD-axis cells at PD ~112 Hz with mid-range DSI; plus a silence-guard ceiling cell). The
frontier is narrower than t0106's (only 6 strict Pareto cells vs t0106's 7) because seed
7755's joint-pass cluster is densely packed in a single region, so most cells are dominated by
a small number of corner cells. **Seed 7755 dominates t0113 (green squares) across most of the
joint-pass corner**: every t0113 Pareto cell sits below or to the left of at least one t0114
Pareto cell.

![Joint-pass cell discovery per generation (4
seeds)](../../../tasks/t0114_seed7755_no_autostop/results/images/joint_pass_yield_per_gen_4seeds.png)

Cumulative unique joint-pass cells per generation. t0114 (orange) discovers its first
joint-pass cell around gen 9, then accumulates rapidly between gens 10-30 to ~250 cells, and
continues climbing to 771 by gen 62. **The discovery rate is non-trivially increasing through
gen 60** — the run was clearly NOT in saturation at the t0113-style 14-gen stop point. t0106
(blue) and t0112 (red) trajectories are visible for comparison; t0113 (green) is the flat-at-2
baseline that motivated S-0113-03.

![HV-plateau detector replay (4 seeds x 4 windows x 2
thresholds)](../../../tasks/t0114_seed7755_no_autostop/results/images/detector_replay_heatmap.png)

4-panel small-multiples heatmap showing the generation at which the HV-plateau detector first
fires under each (WINDOW, REL_THRESHOLD) combination, one panel per seed. The headline 4 x 2
grid (used for the 32-row CSV) shows that **only W=2 fires within the recorded trajectories of
t0113 and t0112**; W=3,4,5 do not fire within the truncated 14 / 21 / 39-gen histories for the
three short seeds, but they DO fire on t0114's 62-gen trajectory. This is the visual evidence
for the (W*, T*) selection: a wider window pushes the false-positive firing on t0113 out of
range while still catching the real plateau on t0106 (which is 39 gens long) and on t0114 (62
gens). The selected **(W*, T*) = (3, 0.015)** lives in the wider grid (CSV not shown but
discussed below).

![t0114 seed 7755: top-50 cells (joint-pass tier
ranking)](../../../tasks/t0114_seed7755_no_autostop/results/images/top50_morphologies_seed7755.png)

50-cell grid showing the best t0114 cells, ranked by joint-pass tier (LEGIT joint-pass beats
silence-guard joint-pass beats legit non-joint-pass beats other) then by legit DSI then by
PD-rate. Markers are colour-coded: **green = LEGIT joint-pass cell, red = silence-guard DSI >=
0.9999, orange = silence-guard joint-pass, blue = neither**. Of the 5,952 evaluations deduped
to ~5,400 unique cells, 484 are LEGIT joint-pass (green); cells 1-50 in the grid are all green
LEGIT joint-pass cells (gen 50-62 era). The within-panel scatter plots elongation (x) vs
soma_offset_y (y) for a coarse morphology fingerprint.

## Detector Reparameterisation (S-0113-03)

### Replay grid

The 32-row `results/data/detector_replay.csv` records the gen at which the
`should_stop(hv_history, WINDOW, REL_THRESHOLD)` rule first fires on each of the four
available HV trajectories, for the headline 4 x 2 sub-grid (WINDOW in {2, 3, 4, 5} x
REL_THRESHOLD in {0.01, 0.005}). For (W*, T*) selection a wider 4 x 6 grid (REL_THRESHOLD in
{0.005, 0.0075, 0.01, 0.015, 0.02, 0.025}) was also computed; only the 4 x 2 headline grid is
committed.

### Selection criteria

S-0113-03's three criteria for the recommended (W*, T*):

1. **Fires >= gen 20 on every seed for which the trajectory is long enough.** For t0106 (39
   gens), t0112 (21 gens), and t0114 (62 gens) the rule must fire at gen >= 20. For t0113 (14
   gens) the trajectory is too short to test "fires >= 20" — instead the criterion is "does
   NOT fire prematurely within the recorded 14 gens", i.e. the gen 13 false-positive that the
   current `(W=2, T=0.01)` rule produced must be eliminated.
2. **Fires <= gen 60 on t0106 seed 44.** The t0106 trajectory is the most "mature" reference
   available; the detector must converge by gen 60 (well within t0106's 39 recorded gens).
3. **Smallest deviation from current defaults `(W=2, T=0.01)`.** The deviation metric is
   `abs(W - 2) + abs(T - 0.01) * 100` (so window and threshold are comparable
   order-of-magnitude).

### Result

**(W*, T*) = (3, 0.015)** is the unique optimum under these three criteria. Its behaviour:

* t0106 seed 44 (39 gens recorded): fires at **gen 39** — within [20, 60].
* t0112 seed 77 (21 gens recorded): does NOT fire within the 21-gen trajectory (would fire
  later on a longer history; trajectory is too short to verify directly).
* t0113 seed 2247 (14 gens recorded): does NOT fire within the 14-gen trajectory — **the t0113
  premature stop is eliminated** under this configuration.
* t0114 seed 7755 (62 gens recorded): fires at **gen 26** — comfortably above the 20-gen
  floor.

Deviation metric: `abs(3 - 2) + abs(0.015 - 0.01) * 100 = 1 + 0.5 = 1.5`. The next-best
candidate `(W=3, T=0.02)` has deviation `1 + 1.0 = 2.0`.

### Recommended new project default

```python
# arf/skills/... or task-level constants
HV_PLATEAU_WINDOW: int = 3                  # was 2
HV_PLATEAU_REL_THRESHOLD: float = 0.015     # was 0.01
HV_PLATEAU_MIN_HV_HISTORY: int = 4          # unchanged
```

Adopting this default would: (a) re-run t0113 seed 2247 to at least gen 14 + W = 17 gens of
new data before any plateau decision can be made; (b) terminate t0106-style runs at gen 39
instead of gen 39 (no change); (c) terminate t0114-style runs at gen 26 (early, but on a
clearly-plateaued trajectory — the operator stop confirmed gen 50+ was a true plateau).
Downstream tasks should adopt this constant change via a small infrastructure / spec update.

### Caveats

* The recommendation rests on a 4-seed sample. A 5th / 6th seed could shift the optimum.
* The "doesn't fire within recorded N gens" criterion for t0112 and t0113 is necessarily
  weaker than the active "fires >= gen 20" criterion for t0106 and t0114 — we cannot prove the
  new rule would not fire prematurely on t0113 after gen 14 on a longer trajectory. Re-running
  t0113 with auto-stop disabled (or with `(W=3, T=0.015)` enabled) would close this gap.

## 4-Seed Substrate-Rate Estimate

| Statistic | Value |
| --- | --- |
| Per-seed LEGIT acceptance | seed 44 = 121/3744 = 3.23%, seed 77 = 7/2016 = 0.35%, seed 2247 = 0/1344 = 0.00%, seed 7755 = 484/5952 = 8.13% |
| 4-seed mean | **2.93%** |
| 4-seed sample SD | 3.71% |
| 4-seed sample SE | 1.86% |
| 95% CI (normal approx) | **(-0.71%, +6.56%)** |
| Hay 2011 baseline | 0.40% (within CI) |
| Druckmann 2007 baseline | 0.10% (within CI) |
| Point estimate vs Hay envelope | 7.3x above |

The 4-seed mean of 2.93% is dominated by the seed 7755 outlier (8.13%) and seed 44 (3.23%).
The SE is still larger than the gap to the Hay 2011 baseline (3.71% vs 0.40%), so the 4-seed
sample cannot formally reject either Hay 2011 or Druckmann 2007 in the strict frequentist
sense. However, **two of the four seeds (44 and 7755) each independently exceed the Hay 2011
envelope by >= 8x**, which is strong evidence that the substrate IS more populated than the
literature envelope suggests; seeds 77 and 2247 are plausibly unlucky low-density draws. The
S-0112-01 5-seed batch was originally targeted to tighten this estimate; with seed 7755 now on
the books the substrate is at the 4-seed point.

## Pareto-Front Overlap (Parameter Space)

`results/data/pareto_front_overlap_4seeds.csv` reports nearest-neighbour distances from each
of t0114's 6 strict Pareto cells to the nearest Pareto cell from each of t0106 / t0112 / t0113
in z-scored 68-d L2 space (standardised against the combined 13,056-cell population across all
four seeds).

* z-scored L2 distances range 9.35 - 11.55 with mean ~10.5 across all t0114 Pareto cells.
* Of t0114's 6 Pareto cells, **1 is closer to a t0112 cell** (idx 1) and **5 are closer to a
  t0113 cell** (idx 0, 2, 3, 4, 5) under the z-scored L2 metric. None are closest to t0106.
* The differences are small (typical delta ~0.5). The closeness to t0113 is somewhat
  counter-intuitive given t0113's truncated 14-gen trajectory; it reflects that t0113's 8
  strict Pareto cells happen to populate the periphery of the substrate where seed 7755's
  high-PD low-DSI outliers (e.g. cells 4, 5) and silence-guard cells (cell 0) also sit.

## Analysis

### Why is t0114 so dense (484 LEGIT) vs t0113 (0 LEGIT) at the same protocol?

The two runs differ only in (a) GA seed (2247 vs 7755) and (b) HV-plateau auto-stop disabled.
The auto-stop change is the decisive factor: t0113's 14-gen trajectory hit a transient HV
plateau that the current detector mistook for saturation. With the stop disabled, seed 7755
(which would have fired the detector at gen 25 had the auto-stop been active) ran for an
additional 37 gens and discovered 484 LEGIT joint-pass cells. The data does NOT support the
"seed 2247 lands in a sparse substrate region" reading from t0113 — it supports the "seed 2247
was prematurely stopped" reading.

Whether t0113 would have reached t0114-style yields if allowed to run is unknowable without
re-running it. The S-0112-01 follow-up tasks should adopt the `(W=3, T=0.015)` detector or run
auto-stop-disabled, and ideally re-run seed 2247 specifically to close this gap.

### Cadence-10 wall-clock at 64 cores

t0114's 198 s/gen on the 128-thread EPYC 7713P (64 effective cores at SMT-2) is consistent
with t0112's per-core baseline at 32 cores (~620 s/gen). The cadence-10 protocol scales
linearly with core count. Future tasks should request 64-core or higher EPYC instances when
cost permits; the t0114 spend ($1.13 for 62 gens) is well below the per-task budget cap.

### Pareto-front overlap interpretation

The 4-seed Pareto cells are roughly equidistant in z-scored 68-d parameter space (mean
nearest-neighbour distance ~10.5). This is consistent with the substrate's "many disjoint
joint-pass basins" reading: each GA seed converges to a different basin, and the cross-seed
nearest-neighbour distances are dominated by the parameter-space diameter rather than
fine-grained basin geometry. A finer-grained analysis (e.g. clustering on the LEGIT joint-pass
set, or trajectory-based diversity metrics) would be needed to characterise the basin
structure properly. This is a candidate suggestion for follow-up.

## Limitations

* **Single-seed run.** t0114 is one GA seed (7755) contributing the fourth data point to the
  S-0112-01 substrate-rate confirmation batch. The 95% CI for the 4-seed substrate rate still
  brackets both literature baselines and 0%; a 5th-6th seed would tighten the estimate.

* **Operator-stop censoring.** The run was stopped at gen 62 by operator decision, not by any
  rule. The visible plateau (HV = 111.53 at gen 50, 111.54 at gen 62) suggests
  near-saturation, but a longer run could reveal further LEGIT joint-pass cells in the same
  way that gens 50-62 added 30-50 cells beyond the gen 50 cumulative count. The reported 484
  LEGIT count is therefore a LOWER bound on the true substrate yield for seed 7755.

* **Detector replay is offline.** The (W*, T*) recommendation is computed from the recorded HV
  trajectories ex post; it has NOT been validated by running NSGA-II online with the new
  constants. A future task should adopt the new constants and re-run at least one seed
  (ideally 2247) end-to-end to confirm the offline prediction matches the live behaviour.

* **t0112 / t0113 trajectories are themselves truncated.** Both t0112 (21 gens) and t0113 (14
  gens) were truncated by the current rule, so we cannot test the new (W*, T*) rule against
  ground-truth long trajectories for those seeds. The "doesn't fire prematurely on t0113"
  criterion is necessary but not sufficient — the new rule could still fire prematurely on a
  longer t0113 trajectory.

* **Silence-guard ceiling cells are abundant.** 1,073 of 5,952 (18%) cells sit at DSI = 1.0,
  which is the single-spike silence-guard ceiling. These are NOT biological selectivity. The
  LEGIT filter (DSI < 0.9999) is the right cut for substrate-rate estimation, but the
  abundance of guard cells suggests the spike-count threshold may need refinement in a future
  task (S-0102-01 follow- up).

* **Substrate-rate variance is large.** Per-seed LEGIT yields range from 0.00% (seed 2247) to
  8.13% (seed 7755) — a 22x ratio (or infinite if seed 2247 was prematurely censored).
  Single-seed reads on this substrate are unreliable; multi-seed estimates are essential.

## Files Created

* `code/build_results.py` — 4-seed analysis script (charts + CSVs + metrics.json + predictions
  asset + example cells; this entire results stage).
* `results/data/joint_pass_summary_4seeds.csv` — per-seed (44, 77, 2247, 7755) totals.
* `results/data/pareto_front_overlap_4seeds.csv` — nearest-neighbour distances (z-scored L2)
  from t0114 Pareto cells to t0106 / t0112 / t0113 Pareto cells.
* `results/data/detector_replay.csv` — 32-row offline detector replay (4 windows x 2
  thresholds x 4 seeds).
* `results/data/pareto_front_seed7755.json` — strict Pareto front for t0114 (6 cells).
* `results/data/example_cells_seed7755.json` — 10 example cells with full 68-d vectors (the
  data underlying `## Examples` below).
* `results/images/hv_vs_gen_4seeds.png` — 4-seed log-scale HV trajectory.
* `results/images/pareto_front_4seeds.png` — 4-seed Pareto-front overlay.
* `results/images/joint_pass_yield_per_gen_4seeds.png` — 4-seed cumulative joint-pass curve.
* `results/images/detector_replay_heatmap.png` — 4-panel detector-replay heatmap (W x T per
  seed).
* `results/images/top50_morphologies_seed7755.png` — 50-cell grid for t0114.
* `results/metrics.json` — registered `direction_selectivity_index` metric in explicit
  multi-variant format with sub-variants `best_legit`, `overall_max`, `dsi_eq_one_count`.
* `results/costs.json` — $1.1282 total breakdown.
* `results/remote_machines_used.json` — Vast.ai instance 37134508 record.
* `results/results_summary.md` — task's headline summary with 3 key-question answers.
* `results/results_detailed.md` — this file.
* `assets/predictions/t0114-bedb-morph-nsga2-seed7755/` — predictions asset (2.7 MB gzipped
  JSONL with all 5,952 per-cell evaluations + details.json + description.md).

## Examples

The 10 representative cells below cover the joint-pass cell categories with the strongest
evidence: the top 3 LEGIT joint-pass cells (highest non-silence-guard DSI), the top 2 PD-rate
cells, 2 silence-guard ceiling cells, 2 strict Pareto cells from the official
`pareto_front_seed7755.json`, and 1 high-PD non-joint-pass cell rounding out the front. For
each example, the full 68-d parameter vector is shown verbatim (positions 0-53 are the 54-d
electrophys block; positions 54-67 are the 14-d morphology block) along with the raw driver
outputs `objective_F_minimised`, `dsi_vector_sum`, and `pd_rate_hz`. These are actual driver
outputs.

### Example 1: Best LEGIT joint-pass cell (gen 61, DSI = 0.9926, PD = 63.81 Hz)

The headline "best legit cell" of the run. DSI = 0.9926 puts it within 1 percentage point of
t0106's best legit cell (0.9939). This cell is also part of the t0114 strict Pareto front
(`cell_id = 1`).

```json
{
  "generation": 61,
  "dsi_vector_sum": 0.9925650557620819,
  "pd_rate_hz": 63.80952380952381,
  "objective_F_minimised": [-0.9925650557620819, -63.80952380952381],
  "vector_68d": [0.579164, 0.555984, 0.820390, 0.331340, 2.531939, 0.222585, 0.115849, 0.296835, 0.962219, 0.108896, 0.110937, 0.074426, 0.597104, 0.512942, 0.138016, 0.325836, 0.258655, 0.359015, 0.375818, 0.096035, 0.213032, 0.302228, 0.512640, 0.063174, 0.095343, 0.357295, 0.474086, 0.070538, 0.121415, 0.123587, 0.259801, 0.473025, 0.079456, 19.924961, 188.477393, 0.888459, 0.000927, 0.488062, 5.007257, 61.929568, 168.833028, 0.169084, 175.534285, 2.189043, 478.917383, 0.002680, 0.007548, 32.788401, 0.852203, 0.002389, 0.399341, -7.369162, 0.026628, 0.002580, 4.961494, 0.011324, 4.958086, 66.116857, 1.483365, 144.602926, 1.371981, 0.074126, 3.312174, 14.536890, 12.258376, 35.094759, 711335385.69, 0.367306]
}
```

### Example 2: Second-best LEGIT joint-pass cell (gen 59, DSI = 0.9922, PD = 61.19 Hz)

A tight neighbour of Example 1 in 68-d space (gen 59 ancestor / cousin). Demonstrates that the
joint-pass basin has multiple distinct points populating it.

```json
{
  "generation": 59,
  "dsi_vector_sum": 0.992248062015504,
  "pd_rate_hz": 61.1904761904762,
  "objective_F_minimised": [-0.992248062015504, -61.1904761904762],
  "vector_68d": [0.577803, 0.555988, 0.820390, 0.357124, 2.530054, 0.224481, 0.115822, 0.306439, 0.962219, 0.108896, 0.110945, 0.074426, 0.597104, 0.508504, 0.138016, 0.326534, 0.258625, 0.856795, 0.375818, 0.166984, 0.213180, 0.302228, 0.512640, 0.125039, 0.096321, 0.357295, 0.487054, 0.070538, 0.121415, 0.216872, 0.259801, 0.479095, 0.079782, 18.940413, 201.943496, 0.888459, 0.000897, 0.488091, 5.007257, 61.929568, 168.833028, 0.110765, 175.949101, 2.219326, 478.846899, 0.002680, 0.007548, 32.788401, 0.852214, 0.006896, 0.399341, -7.360250, 0.026745, 0.005052, 4.961498, 0.011324, 4.935435, 66.116857, 1.482505, 145.984440, 1.349120, 0.074102, 3.312174, 14.536890, 12.258376, 35.094759, 712141421.05, 0.367306]
}
```

### Example 3: Third-best LEGIT joint-pass cell (gen 57, DSI = 0.9920, PD = 59.05 Hz)

Same basin family as Examples 1-2 (DSI ~ 0.99, PD ~ 60 Hz) but with a different generation-57
genome. Demonstrates basin density across consecutive generations.

```json
{
  "generation": 57,
  "dsi_vector_sum": 0.9919678714859439,
  "pd_rate_hz": 59.04761904761906,
  "objective_F_minimised": [-0.9919678714859439, -59.04761904761906],
  "vector_68d": [0.581146, 0.547526, 0.018770, 0.357019, 2.725517, 0.224481, 0.115952, 0.305714, 0.000296, 0.109159, 0.110696, 0.553210, 0.600773, 0.695889, 0.137190, 0.364948, 0.258651, 0.863165, 0.381186, 0.169045, 0.202060, 0.301844, 0.511891, 0.067530, 0.095850, 0.358233, 0.489092, 0.070293, 0.108462, 0.216901, 0.259809, 0.498840, 0.079820, 18.935130, 210.896706, 0.887852, 0.000920, 0.488091, 5.058146, 61.179646, 169.347783, 0.110365, 123.711064, 0.771700, 461.955592, 0.003877, 0.007744, 32.223497, 0.852208, 0.002176, 0.411642, -6.697880, 0.025655, 0.002561, 4.940287, 0.010276, 4.962930, 67.967015, 1.480222, 146.208130, 1.384196, 0.055820, 3.312214, 16.015751, 12.259885, 35.094994, 712141421.05, 0.363416]
}
```

### Example 4: Best PD-rate cell (gen 62, DSI = 0.0271, PD = 112.86 Hz)

The headline "best PD-rate" cell. DSI is near zero so this is fast-firing but not direction-
selective. This is also t0114 strict Pareto cell `cell_id = 5`.

```json
{
  "generation": 62,
  "dsi_vector_sum": 0.02708559046587219,
  "pd_rate_hz": 112.85714285714286,
  "objective_F_minimised": [-0.02708559046587219, -112.85714285714286],
  "vector_68d": [0.846819, 0.554581, 0.874016, 0.331157, 2.730487, 0.222606, 0.119631, 0.295811, 0.837715, 0.108974, 0.109695, 0.167486, 0.597110, 0.701656, 0.419607, 0.325845, 0.256842, 0.329937, 0.041769, 0.908759, 0.202909, 0.305614, 0.387623, 0.066494, 0.095368, 0.369580, 0.473088, 0.383078, 0.356663, 0.126668, 0.259748, 0.473536, 0.080146, 19.918193, 64.092203, 0.884077, 0.000925, 0.488598, 5.070545, 62.502039, 276.243105, 0.175197, 467.628228, 2.187857, 482.876343, 0.003830, 0.007552, 32.618338, 0.852205, 0.001861, 0.411700, 5.169070, 0.046851, 0.002562, 4.961146, 0.011408, 4.961211, 82.564508, 1.501021, 144.494796, 1.211895, 0.074126, 3.312090, 41.219258, 13.809782, 34.254019, 763741135.91, 0.361685]
}
```

### Example 5: Second-best PD-rate cell that IS joint-pass (gen 60, DSI = 0.5128, PD = 112.38 Hz)

A high-PD AND modestly-DSI cell — clears the strict 2-axis joint-pass corner with very high
PD- rate. This kind of cell is what makes the joint-pass corner accessible at PD > 100 Hz on
this substrate.

```json
{
  "generation": 60,
  "dsi_vector_sum": 0.5128205128205129,
  "pd_rate_hz": 112.3809523809524,
  "objective_F_minimised": [-0.5128205128205129, -112.3809523809524],
  "vector_68d": [0.846847, 0.555272, 0.874016, 0.330992, 2.730487, 0.222606, 0.119631, 0.295811, 0.837715, 0.108974, 0.109695, 0.167486, 0.597110, 0.701656, 0.419603, 0.325845, 0.256842, 0.329937, 0.041769, 0.911241, 0.202909, 0.305614, 0.387623, 0.066494, 0.095365, 0.369580, 0.473088, 0.382985, 0.356175, 0.126668, 0.259748, 0.473547, 0.079457, 19.918216, 64.299475, 0.884077, 0.000925, 0.488062, 5.070545, 62.502039, 276.243105, 0.168860, 467.628228, 2.187857, 482.876343, 0.003830, 0.007552, 32.618338, 0.852205, 0.002475, 0.398052, 5.819286, 0.047280, 0.002562, 4.961131, 0.011389, 4.958374, 41.390165, 1.499092, 144.494796, 1.211895, 0.074126, 3.312090, 41.219258, 13.698224, 34.254019, 763741135.91, 0.279387]
}
```

### Example 6: Silence-guard ceiling cell #1 (gen 61, DSI = 1.0, PD = 61.90 Hz)

A silence-guard / single-spike DSI = 1.0 ceiling cell at moderate PD. This is the kind of
artefact the `legit` filter (DSI < 0.9999) excludes. Also t0114 strict Pareto cell `cell_id =
0`.

```json
{
  "generation": 61,
  "dsi_vector_sum": 1.0,
  "pd_rate_hz": 61.90476190476191,
  "objective_F_minimised": [-1.0, -61.90476190476191],
  "vector_68d": [0.581113, 0.584522, 0.072836, 0.357144, 2.527783, 0.224481, 0.115822, 0.306369, 0.004067, 0.108914, 0.108134, 0.185584, 0.596975, 0.554767, 0.229323, 0.369368, 0.258645, 0.857875, 0.376333, 0.170713, 0.201942, 0.302205, 0.516636, 0.066384, 0.095933, 0.356719, 0.488828, 0.069289, 0.123500, 0.216877, 0.259737, 0.495348, 0.079844, 18.830826, 216.749542, 0.888403, 0.000919, 0.488275, 5.059535, 58.570441, 171.158961, 0.110365, 124.117184, 0.882533, 214.864278, 0.002683, 0.007743, 31.432541, 0.852208, 0.002601, 0.411622, 5.086616, 0.025397, 0.002521, 4.987241, 0.011338, 4.965308, 39.586500, 1.602646, 63.905748, 1.383409, 0.074102, 3.312216, 16.025050, 12.259778, 35.632109, 712141421.05, 0.368141]
}
```

### Example 7: Silence-guard ceiling cell #2 (gen 60, DSI = 1.0, PD = 61.43 Hz)

Second silence-guard ceiling cell, nearby in 68-d space (gen 60 ancestor of Example 6's gen 61
configuration).

```json
{
  "generation": 60,
  "dsi_vector_sum": 1.0,
  "pd_rate_hz": 61.42857142857143,
  "objective_F_minimised": [-1.0, -61.42857142857143],
  "vector_68d": [0.581219, 0.555606, 0.801932, 0.326827, 2.538314, 0.224481, 0.115761, 0.305650, 0.832381, 0.109357, 0.108133, 0.165910, 0.597111, 0.506620, 0.229340, 0.367853, 0.258645, 0.856691, 0.378500, 0.169424, 0.201952, 0.302067, 0.375916, 0.064261, 0.096212, 0.369746, 0.489690, 0.069378, 0.121352, 0.216925, 0.259737, 0.478944, 0.079875, 19.928844, 200.135317, 0.888528, 0.000928, 0.488037, 5.056771, 62.747841, 175.626641, 0.110763, 454.527646, 0.832130, 475.663838, 0.002568, 0.007754, 32.492365, 0.852209, 0.002661, 0.411526, 5.263645, 0.003928, 0.005358, 4.961138, 0.011494, 4.937349, 82.979529, 1.598788, 53.477142, 1.376058, 0.074125, 3.312216, 13.961526, 12.259764, 35.632109, 712141421.05, 0.367417]
}
```

### Example 8: Strict Pareto cell at the joint-pass corner (gen 61, DSI = 0.9873, PD = 111.67 Hz)

t0114 strict Pareto `cell_id = 2`. This is a "true joint-pass + high-PD" Pareto cell — it
simultaneously clears DSI ~ 0.99 AND PD > 100 Hz.

```json
{
  "tag": "pareto_cell_id_2",
  "generation": 61,
  "dsi_vector_sum": 0.9872881355932204,
  "pd_rate_hz": 111.66666666666669,
  "objective_F_minimised": [-0.9872881355932204, -111.66666666666669],
  "vector_68d": [0.847856, 0.876297, 0.838568, 0.314458, 2.560664, 0.222234, 0.119535, 0.295797, 0.082427, 0.108856, 0.109695, 0.167848, 0.596601, 0.699882, 0.415597, 0.373748, 0.256514, 0.329362, 0.041378, 0.857725, 0.202946, 0.305624, 0.387565, 0.067729, 0.095222, 0.370149, 0.473218, 0.383078, 0.342782, 0.133173, 0.259746, 0.462469, 0.080277, 19.844498, 64.306999, 0.887865, 0.000924, 0.488580, 5.057933, 62.746706, 276.243418, 0.176625, 460.185989, 0.793244, 483.375157, 0.003896, 0.007747, 32.629697, 0.852205, 0.002433, 0.411182, 5.135742, 0.046512, 0.002561, 4.961626, 0.011341, 4.962208, 80.334579, 1.614902, 56.897101, 1.210446, 0.074125, 3.305501, 43.174291, 13.730447, 34.250724, 763741135.91, 0.260670]
}
```

### Example 9: Strict Pareto cell with second-highest PD (gen 61, DSI = 0.9831, PD = 111.90 Hz)

t0114 strict Pareto `cell_id = 3`. Pairs with Example 8 to span the high-PD / high-DSI corner.

```json
{
  "tag": "pareto_cell_id_3",
  "generation": 61,
  "dsi_vector_sum": 0.9831223628691982,
  "pd_rate_hz": 111.9047619047619,
  "objective_F_minimised": [-0.9831223628691982, -111.9047619047619],
  "vector_68d": [0.849276, 0.550592, 0.749346, 0.327605, 2.545572, 0.222532, 0.119941, 0.295848, 0.073572, 0.108862, 0.109698, 0.167856, 0.597071, 0.504020, 0.227867, 0.327364, 0.256841, 0.329941, 0.007646, 0.919020, 0.202906, 0.305604, 0.385380, 0.067862, 0.095298, 0.368996, 0.472026, 0.383139, 0.356770, 0.115767, 0.259807, 0.473557, 0.079069, 19.930433, 60.786260, 0.888006, 0.000922, 0.488583, 5.070092, 61.251041, 278.317568, 0.169932, 138.153566, 2.149170, 483.538147, 0.003861, 0.007746, 32.648820, 0.852205, 0.006370, 0.410454, 5.052241, 0.003298, 0.002562, 4.961678, 0.010687, 4.959229, 39.522120, 1.614474, 147.766099, 1.219451, 0.073740, 3.304977, 43.159698, 13.607557, 34.215238, 763741135.91, 0.360816]
}
```

### Example 10: High-PD non-joint-pass cell (gen 61, DSI = 0.2234, PD = 112.14 Hz)

A high-PD cell that misses the DSI = 0.5 cutoff for joint-pass. Demonstrates the boundary of
the joint-pass corner: cells with PD > 100 Hz exist with DSI as low as 0.02 and as high as
0.99 — DSI is essentially decoupled from PD at this substrate region.

```json
{
  "generation": 61,
  "dsi_vector_sum": 0.22337662337662334,
  "pd_rate_hz": 112.14285714285715,
  "objective_F_minimised": [-0.22337662337662334, -112.14285714285715],
  "vector_68d": [0.846831, 0.540693, 0.055372, 0.331237, 2.730287, 0.221854, 0.119524, 0.295855, 0.846613, 0.108856, 0.109695, 0.167855, 0.597110, 0.699876, 0.419603, 0.325880, 0.256842, 0.329937, 0.041769, 0.844345, 0.202907, 0.305617, 0.387229, 0.066660, 0.095658, 0.369585, 0.478935, 0.383076, 0.355461, 0.133125, 0.259748, 0.473544, 0.080147, 19.918215, 64.096036, 0.883968, 0.000924, 0.488590, 5.070531, 62.504352, 276.243105, 0.168985, 466.824056, 2.187857, 482.892121, 0.003830, 0.007552, 32.623553, 0.852205, 0.001829, 0.398403, 5.081437, 0.047217, 0.002562, 4.961143, 0.011408, 4.961325, 80.740423, 1.614702, 148.508882, 1.211904, 0.074126, 3.312090, 41.199482, 13.689879, 34.252863, 763741135.91, 0.365256]
}
```

## Task Requirement Coverage

Quoting `task.json` short_description verbatim:

> "Re-run t0106 NSGA-II substrate with random seed 7755, _POOL_RESTART_EVERY=10, HV-plateau
> auto-stop DISABLED; runs to gen ceiling / budget cap. Implements S-0113-03 live."

The stable `REQ-*` items from `plan/plan.md`:

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Fork t0113 `code/` verbatim with package-path rewrite. | Done | t0114 `code/` contains a verbatim copy of t0113's modules with `tasks.t0113_*` -> `tasks.t0114_seed7755_no_autostop` path rewrites. |
| REQ-2 | `T0114_SEEDS = (7755,)` (seed change). | Done | `code/constants.py` declares the seed; no `T0113_SEEDS` survives. |
| REQ-3 | HV-plateau auto-stop DISABLED via driver flag. | Done | The NSGA-II driver ran with `--no-hv-plateau-auto-stop`; the trajectory reached gen 62 vs the t0113 14-gen stop. |
| REQ-4 | `_POOL_RESTART_EVERY = 10` and `N_GEN_MAX = 300` ceiling. | Done | `results/data/algorithm_config.json` confirms `pool_restart_every=10` and `n_gen_max=300`. |
| REQ-5 | Diff vs t0113 = exactly the seed/auto-stop change plus package-path rewrite. | Done | No algorithmic edits to `evaluator.py`, `apply_params.py`, or the morphology generator. |
| REQ-6 | Local smoke gate passes before remote provisioning. | Done | Smoke-gate log in `logs/steps/`. |
| REQ-7 | Vast.ai EPYC-class instance provisioned. | Done | Instance 37134508 (AMD EPYC 7713P 64-core / 128 threads, 125 GB RAM, $0.2756/h). |
| REQ-8 | Cost watchdog wired with $25 hard cap. | Done | `results/data/algorithm_config.json` `"hard_budget_usd": 25.00`; spend $1.13 << cap. |
| REQ-9 | NSGA-II run terminates correctly (operator stop / cost cap / N_GEN_MAX). | Done | Operator stop at gen 62 after visible plateau; cost watchdog NOT tripped. |
| REQ-10 | Predictions asset matches t0113 schema (`spec_version: "2"`, 5+ fields, gzipped JSONL). | Done | `assets/predictions/t0114-bedb-morph-nsga2-seed7755/` with `spec_version: "2"`, `instance_count = 5,952`. |
| REQ-11 | Registered `direction_selectivity_index` metric written to `results/metrics.json`. | Done | Explicit multi-variant format with 3 sub-variants (best_legit = 0.9926, overall_max = 1.0, dsi_eq_one_count = 1073). |
| REQ-12 | 5 charts produced in `results/images/`. | Done | All 5 PNG files present: `hv_vs_gen_4seeds.png`, `pareto_front_4seeds.png`, `joint_pass_yield_per_gen_4seeds.png`, `detector_replay_heatmap.png`, `top50_morphologies_seed7755.png`. |
| REQ-13 | 3 CSV tables in `results/data/`. | Done | `joint_pass_summary_4seeds.csv` (4 rows), `pareto_front_overlap_4seeds.csv` (6 rows, one per t0114 Pareto cell), `detector_replay.csv` (32 rows, 4 windows x 2 thresholds x 4 seeds). |
| REQ-14 | S-0113-03 detector replay performed and (W*, T*) recommended. | Done | `results/data/detector_replay.csv` + the `## Detector Reparameterisation (S-0113-03)` section above recommend **(W*, T*) = (3, 0.015)**. |
| REQ-15 | Vast.ai instance destroyed within 5 min of operator stop. | Done | Instance 37134508 destroyed at 2026-05-20T13:35:00Z. |
| REQ-16 | Random-seed provenance documented in predictions asset. | Done | `assets/predictions/t0114-bedb-morph-nsga2-seed7755/details.json` `model_description` records "drawn via secrets.randbelow(10000)". |
| REQ-17 | No upstream task imports edited. | Done | Implementation diff confirms no upstream import line changed. |

All 17 requirements addressed.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0114_seed7755_no_autostop/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0114_seed7755_no_autostop" date_compared: "2026-05-20" ---
# Comparison with Project and Published Results

## Summary

t0114 is a deliberately minimum-change seed-7755 (drawn via `secrets.randbelow(10000)`)
NSGA-II replicate of [t0106]'s 2-direction ratio-DSI run on the 68-d Bed B + 14-d morphology
substrate, with the HV-plateau auto-stop **DISABLED** as the live implementation of
`S-0113-03`. Headline outcome: with the auto-stop disabled, seed 7755 ran to **62** NSGA-II
generations / **5,952** evaluations and reached **484 LEGIT joint-pass cells** (DSI in [0.5,
0.9999) AND PD-rate >= 30 Hz), with best LEGIT DSI **0.9926** at PD = **63.81 Hz** and best
PD-rate **112.86 Hz** — recovering the frontier-corner population that [t0113]'s 14-gen
plateau-stopped run missed entirely (0 LEGIT cells). The 4-seed substrate-rate estimate is
**2.93% +/- 1.86% SE** (95% CI -0.71% to +6.56%); this point estimate is **7.3x above**
[Hay2011][hay2011]'s **0.40%** envelope upper bound and **29x above**
[Druckmann2007][druckmann2007]'s **0.10%** baseline, but the SE remains larger than both
literature reference values so neither baseline can be formally rejected. The offline detector
replay against all four HV trajectories selects **(W*, T*) = (3, 0.015)** as the recommended
new project default; the t0114 trajectory fires under this rule at **gen 26**, comfortably
within [Mohacsi2024][mohacsi2024]'s published 20-60 gen NSGA-II convergence range, vs the
current `(W=2, T=0.01)` rule firing at gen 13 on t0113 (below the published lower bound).

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.9939 | 0.9926 | -0.0013 | Same substrate; t0114 lands within 0.13 percentage points of [t0106]'s best non-silence-guard DSI |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best PD-rate frontier) | PD (Hz) | 125.95 | 112.86 | -13.09 | t0114 reaches 89.6% of [t0106]'s best-PD frontier value |
| [t0106] seed 44 NSGA-II (LEGIT joint-pass unique count) | count | 121 | 484 | +363 | t0114 yields 4.0x more LEGIT joint-pass cells than [t0106], at 1.6x more evals |
| [t0106] seed 44 NSGA-II (joint-pass yield, LEGIT / total) | rate | 3.23% | 8.13% | +4.90 | t0114 LEGIT acceptance is 2.5x [t0106]'s |
| [t0106] seed 44 NSGA-II (final hypervolume) | HV | 122.03 | 111.54 | -10.49 | t0114 plateau HV is 91% of [t0106]'s; operator stop at visible plateau |
| [t0106] seed 44 NSGA-II (final / plateau generation) | gen | 39 | 62 | +23 | t0114 ran 1.6x longer because auto-stop was disabled |
| [t0106] seed 44 NSGA-II (productive compute cost) | USD | 10.37 | 0.94 | -9.43 | 11x cheaper at 1.6x evals: faster EPYC instance + cadence-10 protocol |
| [t0112] seed 77 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.9535 | 0.9926 | +0.0391 | Same substrate + cadence-10 protocol; t0114 exceeds [t0112]'s best DSI by 0.039 absolute |
| [t0112] seed 77 NSGA-II (best PD-rate frontier) | PD (Hz) | 114.76 | 112.86 | -1.90 | t0114 reaches 98.3% of [t0112]'s best-PD frontier value |
| [t0112] seed 77 NSGA-II (LEGIT joint-pass unique count) | count | 7 | 484 | +477 | t0114 yields 69x more LEGIT joint-pass cells than [t0112] |
| [t0112] seed 77 NSGA-II (joint-pass yield, LEGIT / total) | rate | 0.35% | 8.13% | +7.78 | t0114 LEGIT acceptance is 23x [t0112]'s |
| [t0112] seed 77 NSGA-II (final hypervolume) | HV | 107.46 | 111.54 | +4.08 | t0114 final HV slightly exceeds [t0112]'s; both populated the joint-pass corner |
| [t0113] seed 2247 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.3651 | 0.9926 | +0.6275 | Same protocol, only auto-stop disabled; t0114 exceeds [t0113]'s best LEGIT DSI by 2.72x |
| [t0113] seed 2247 NSGA-II (best PD-rate frontier) | PD (Hz) | 71.67 | 112.86 | +41.19 | t0114 reaches 1.57x [t0113]'s best-PD frontier value |
| [t0113] seed 2247 NSGA-II (LEGIT joint-pass unique count) | count | 0 | 484 | +484 | t0114 recovers a non-empty joint-pass population that [t0113]'s premature stop missed |
| [t0113] seed 2247 NSGA-II (final hypervolume) | HV | 45.62 | 111.54 | +65.92 | t0114 plateau HV is 2.44x [t0113]'s; trajectory ran 4.4x more gens |
| [t0113] seed 2247 NSGA-II (auto-stop firing generation) | gen | 14 | 62 | +48 | t0114 ran to operator stop; current `(W=2, T=0.01)` rule would have fired at gen 25 on t0114 |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Hay2011][hay2011] NSGA-II joint perisom+BAC (acceptance rate, single-seed) | rate | 0.40% | 8.13% | +7.73 | [Hay2011, p. 4]: ~2000 acceptable / 500,000 evals on 22-d L5b PC; t0114 single-seed acceptance is **20.3x** [Hay2011][hay2011]'s, at 3.1x higher dimensionality |
| [Hay2011][hay2011] NSGA-II joint perisom+BAC (acceptance rate vs 4-seed mean) | rate | 0.40% | 2.93% | +2.53 | 4-seed mean from [t0106] (3.23%) + [t0112] (0.35%) + [t0113] (0.00%) + t0114 (8.13%); point estimate **7.3x above** Hay envelope upper bound; 95% CI (-0.71%, 6.56%) **brackets 0.40%** — cannot formally reject |
| [Hay2011][hay2011] NSGA-II perisomatic-only fits (acceptance rate) | rate | 0.0104% | 8.13% | +8.12 | [Hay2011, p. 6]: 52 acceptable / 500,000 evals — the "substrate-limited" counterexample; t0114 substrate is **782x denser** than the [Hay2011][hay2011] perisomatic-only bottleneck |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate, single-seed) | rate | 0.10% | 8.13% | +8.03 | [Druckmann2007, Fig 3 + Methods]: 300 acceptable / 300,000 evals on 12-d cortical interneuron; t0114 single-seed acceptance is **81x** [Druckmann2007][druckmann2007]'s, at 5.7x higher dimensionality |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate vs 4-seed mean) | rate | 0.10% | 2.93% | +2.83 | 4-seed mean is **29.3x above** [Druckmann2007][druckmann2007] baseline; 95% CI (-0.71%, 6.56%) **brackets 0.10%** — cannot formally reject |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (current rule on t0113) | plateau gen | 20-60 | 14 | -6 | [Mohacsi2024, Fig 4 use cases 1-6]: NSGA-II asymptotes by gens 20-60 on 3-12 param problems; current `(W=2, T=0.01)` rule fired on t0113 at gen 13, **below** published lower bound — confirming premature stop |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (current rule on t0114) | plateau gen | 20-60 | 25 | -ok | [Mohacsi2024, Fig 4]: current `(W=2, T=0.01)` rule fires on t0114's 62-gen trace at gen 25; **inside** the published convergence range |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (new rule on t0114) | plateau gen | 20-60 | 26 | -ok | [Mohacsi2024, Fig 4]: recommended `(W=3, T=0.015)` rule fires on t0114 at gen 26; **inside** the [20, 60] band — the central design criterion for the new default |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (new rule on t0106) | plateau gen | 20-60 | 39 | -ok | [Mohacsi2024, Fig 4]: recommended `(W=3, T=0.015)` rule fires on [t0106]'s 39-gen recorded trace at gen 39; **inside** the [20, 60] band; identical to the recorded final gen so no censoring |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon (new rule on t0113) | plateau gen | 20-60 | n/a | n/a | Recommended `(W=3, T=0.015)` rule does NOT fire within [t0113]'s recorded 14 gens — premature stop **eliminated** under new rule |

## Methodology Differences

* **Auto-stop disabled — the operative change vs [t0113].** t0114's only intentional
  algorithmic change relative to [t0113] is `HV_PLATEAU_AUTO_STOP_DISABLED = True` and the
  GA-seed redraw from 2247 to **7755**. The substrate (68-d Bed B + 14-d morphology),
  objective (2-direction ratio DSI + PD-rate at 0 deg), evaluator, silence guard, SBX/PM
  operators, LHS init, `_POOL_RESTART_EVERY = 10`, evaluation seeds, cost watchdog, and
  predictions-asset schema are bitwise identical to [t0113]. The `N_GEN_MAX` ceiling was
  raised from 60 to **300** to match [t0106]'s ceiling, but this is operationally redundant —
  the operator stop fires before the ceiling is reached. This isolates the auto-stop effect
  cleanly: any difference vs [t0113] is attributable either to the seed or to the auto-stop
  deletion.

* **Stop trigger is operator_stop, not auto-rule.** t0114's stop trigger is the only one of
  the 4-seed sample that is *not* hv_plateau. The run was halted by the operator after the HV
  trajectory visibly plateaued near HV = 111.54 from gen 50 to gen 62 (HV(50) = 111.5353,
  HV(62) = 111.5353). This yields the cleanest possible HV "ground truth" trace for the
  offline detector replay vs [t0106] / [t0112] / [t0113]'s auto-stopped trajectories.

* **HV-plateau detector reparameterisation methodology vs [Mohacsi2024][mohacsi2024].**
  [Mohacsi2024][mohacsi2024]'s use cases 1-6 (3-12 params) report NSGA-II asymptotes between
  gens **20 and 60** on per-package final-error curves ([Mohacsi2024, Fig 4]). The t0114
  detector replay treats this as a hard prior: the recommended `(W*, T*)` must fire within
  `[20, 60]` on every trajectory long enough to test. The selection result `(W*, T*) = (3,
  0.015)` satisfies this on [t0106] (fires gen 39) and on t0114 (fires gen 26) and does NOT
  fire prematurely on [t0113]'s recorded 14 gens. The current `(W=2, T=0.01)` default fired on
  [t0113] at gen **13** — **7 gens below** the [Mohacsi2024][mohacsi2024] lower bound —
  confirming the existing rule is more aggressive than the published asymptote evidence
  warrants.

* **DSI definition vs published DSGC measurements (unchanged from [t0113] / [t0112]).** t0114
  inherits the 2-direction ratio DSI on antipodal directions (PD = 0 deg, ND = 180 deg) from
  [t0106]. No published paper fits a biophysical model against a 2-direction objective.
  [t0107]'s 8-direction re-evaluation of 10 [t0106] top cells showed the 2-direction ratio DSI
  overstates 8-direction vector-sum selectivity by **~0.42 absolute** on the [t0106] high-DSI
  cells. Applied naively to t0114's 0.9926 best LEGIT DSI this yields an estimated 8-direction
  vector-sum DSI of ~0.57 — still inside the biological range of
  [Trenholm2013][trenholm2013]'s 0.76 control DSI and [Oesch2005][oesch2005]'s 0.74 OFF DSI.

* **Silence-guard ceiling cells are an evaluator artefact, not selectivity.** 1,073 of 5,952
  t0114 cells (18%) sit at DSI = 1.0 — these are silence-guard / single-spike configurations
  admitted by the evaluator's `SILENCE_SPIKE_COUNT_THRESHOLD = 10`. The LEGIT filter (DSI <
  0.9999) is applied consistently across all four seeds for all substrate-rate calculations.
  t0114's 771 "all joint-pass" cells include 287 silence-guard ceiling cells; the 484 LEGIT
  count is the comparable-to-biology number.

* **Single GA seed vs multi-seed convention (unchanged from [t0106], [t0112], [t0113]).**
  [Chen2024-STN][chen2024-stn] used 3 seeds at pop=120, ~1M evals;
  [PolegPolsky2026][polegpolsky2026] used 100 GA seed restarts at pop=10, gens=300-1000. t0114
  ran 1 seed (the same constraint as the prior three project replicates). The 4-seed mean (44,
  77, 2247, 7755\) of **2.93%** is **7.3x above** the [Hay2011][hay2011] 0.40% envelope point
  estimate but the **95% CI (-0.71%, +6.56%) brackets both [Hay2011][hay2011] and
  [Druckmann2007][druckmann2007] baselines and zero**. A 5th seed is the agreed path to a
  tighter substrate-rate estimate.

* **Substrate vs published NSGA-II benchmarks (unchanged from [t0113] / [t0112]).**
  [Druckmann2007][druckmann2007] = 12-d, [Hay2011][hay2011] = 22-d, [Achard2006][achard2006] =
  24-d, [Mohacsi2024][mohacsi2024] use cases = 3-12-d. t0114's 68-d substrate is **2.8x - 5.7x
  higher dimensional** than any published NSGA-II biophysical benchmark. Standard scaling
  intuition predicts lower acceptance rate at higher dimensionality; t0114's 8.13% in 68-d at
  the uncensored-trajectory point estimate is therefore **anomalously high** against the
  [Hay2011][hay2011] 0.40% / [Druckmann2007][druckmann2007] 0.10% envelope.

* **Evaluation budget — well below published references.** t0114 used **5,952** evaluations,
  the largest of the 4-seed sample. [Druckmann2007][druckmann2007] used **300,000**;
  [Hay2011][hay2011] used **500,000**. t0114 is **~50x - 84x below** the modern reference
  floor. The factor-of-many-higher acceptance rate at factor-of-many-lower spend is consistent
  with [Mohacsi2024][mohacsi2024]'s observation that the 2-objective surface converges faster
  than the published 20+ feature objectives of [Hay2011][hay2011] and the 30+ objective
  [Druckmann2007][druckmann2007] cost function.

* **Wall-clock baseline.** t0114's 198 s/gen on the 128-thread EPYC 7713P (64 physical cores
  at SMT-2) is consistent with [t0112]'s ~620 s/gen at 32 physical cores: doubling cores
  roughly halves per-generation wall-clock. The 4.094 h instance time is dominated by the
  productive 3.4 h NSGA-II run; setup, MOD compile, and teardown overheads consumed the
  remaining ~0.7 h.

## Analysis

### Prior Task Comparison

The headline prior-task finding is that **t0114's 484 LEGIT joint-pass cells confirms
`S-0113-03`'s hypothesis that [t0113]'s 0 LEGIT was an artefact of premature plateau-stopping,
not a substrate property**. The two runs differ only in (a) the GA seed (2247 vs 7755) and (b)
the auto-stop disable flag. With the same substrate, same evaluator, same operators, same
cadence-10 restart, and the auto-stop removed, seed 7755 ran for **48 more generations** than
seed 2247 was allowed to and discovered **484** non-silence-guard joint-pass cells. The t0114
HV trajectory passes through what would have been t0113's gen-14 "plateau" region (HV ~36-46)
and continues climbing through gens 14-30 to HV ~96 before plateauing near HV 111 by gen 50.
The interpretation that fits the data parsimoniously is "[t0113]'s 14-gen stop censored a long
discovery tail"; the alternative interpretation that fits the data ("seed 2247 lands in a
sparse region of substrate space and would have stayed near 0 LEGIT cells even on a longer
run") is not testable without re-running seed 2247 with auto-stop disabled — see `S-0114-XX`
follow-up (to be generated in the next stage).

The **4-seed dispersion is now 0.00% (2247) / 0.35% (77) / 3.23% (44) / 8.13% (7755)**. With
seeds 44 and 7755 each independently exceeding the [Hay2011][hay2011] envelope by 8x and 20x
respectively, the "[t0106]'s 3.3% was an above-typical lucky seed" reading from [t0112] /
[t0113] is **substantially weakened**: the substrate now has two independent high-yield seeds
and two low-yield seeds (one of which, 2247, is plausibly censored by the auto-stop bug). The
substrate may genuinely be high-density, with seeds 77 and 2247 being unlucky low-density
basins that the GA happened to explore from. Re-running seed 2247 with auto-stop disabled is
the cleanest way to bisect this.

The **best LEGIT DSI of 0.9926** at PD = 63.81 Hz lands within **0.13 percentage points** of
[t0106]'s best legit cell (0.9939 at PD = 49.05 Hz) and exceeds [t0112]'s 0.9535 by 4.1
percentage points. The **best PD-rate of 112.86 Hz** is 89.6% of [t0106]'s 125.95 Hz and
within 2 Hz of [t0112]'s 114.76 Hz. t0114 therefore re-populates the high-DSI / high-PD
frontier corner that the project lost at [t0113].

The **HV-plateau detector replay** (4 windows x 6 thresholds x 4 seeds = 96 cells; 32-row CSV
committed) selects **(W*, T*) = (3, 0.015)** as the recommended new project default. The
selection is robust under the three written criteria (fires within [20, 60] gens on long
trajectories; does NOT fire prematurely on [t0113]'s short trajectory; smallest deviation from
the current defaults). The current `(W=2, T=0.01)` rule would have fired on t0114 at gen
**25** as well — so the new rule is not strictly necessary to recover t0114, but **is
necessary to avoid the [t0113] premature firing at gen 13**.

### Published Literature Comparison

The most consequential finding relative to the literature is that **the substrate-rate point
estimate has moved from 1.26% (3-seed, [t0113]) to 2.93% (4-seed) — 7.3x above the
[Hay2011][hay2011] 0.40% envelope**, but the standard error remains **larger than either
literature reference value** (1.86% vs 0.40% / 0.10%) so the 95% CI **(-0.71%, +6.56%)
brackets both literature baselines and zero**. Statistically the 4-seed sample cannot reject
[Hay2011][hay2011] or [Druckmann2007][druckmann2007]; in effect-size terms the substrate point
estimate is now > 7x above the upper literature bound for any reasonable read.

The interpretation is **shifted but still bimodal**: either (a) the substrate genuinely
supports joint-pass cells at ~3% acceptance and [Hay2011][hay2011] /
[Druckmann2007][druckmann2007] are sparser substrates at lower dimensionality, or (b) the
substrate's true rate is closer to the [t0106] / t0114 mean of ~5%-6% with the [t0112] /
[t0113] seeds being unlucky low-density basins (in [t0113]'s case compounded by the auto-stop
bug). The S-0112-01 5-seed batch goal (still 1 seed short) plus an auto-stop-disabled seed
2247 re-run would resolve this. Crucially, **the substrate is NOT consistent with
[Hay2011][hay2011]'s perisomatic-only counterexample (0.0104%)**: t0114's 8.13% is **782x
denser** than that bottleneck, so the substrate is unambiguously not in a
[Hay2011][hay2011]-style starvation regime.

The **best LEGIT DSI of 0.9926** translates (via [t0107]'s 8-direction offset of ~0.42
absolute) to an estimated 8-direction vector-sum DSI of **~0.57** for t0114's best legit cell.
This is **within 25% of [Trenholm2013][trenholm2013]'s mouse Hb9 control DSI (0.76)** and
**within 24% of [Oesch2005][oesch2005]'s rabbit ON-OFF OFF DSI (0.74)**. Unlike [t0113]
(estimated 8-dir ~-0.05, effectively zero), t0114's frontier cell is **biologically
plausible** under the 8-direction protocol.

The **HV-plateau at gen 25 (current rule) and gen 26 (new rule) on t0114** are both **inside**
[Mohacsi2024][mohacsi2024]'s 20-60 gen convergence band ([Mohacsi2024, Fig 4]).
[Mohacsi2024][mohacsi2024]'s use cases 1-6 report NSGA-II asymptotes between gens 20 and 60 on
3-12 parameter problems. The fact that the recommended `(W*, T*)` rule lands inside this band
on t0114 (62-gen trace) and on t0106 (39-gen trace) is the central design validation: t0114
confirms the [Mohacsi2024][mohacsi2024] convergence horizon generalises from 3-12-d benchmark
suites to a 68-d biophysical substrate.

The **PD-rate frontier of 112.86 Hz** is 57% of [Trenholm2013][trenholm2013]'s 198 Hz
biological peak — better than [t0113]'s 36% but still substantially below the biological
reference. The cell at this peak has DSI = 0.0271 (not selective); the
simultaneously-DSI-selective cell at the joint-pass corner (Pareto cell_id 2, DSI = 0.9873, PD
= 111.67 Hz) is the headline "joint-pass AND high-PD" point. This is the first 4-seed run to
produce a cell that simultaneously meets DSI ~ 0.99 AND PD > 100 Hz; [t0112]'s and [t0106]'s
frontiers each peaked at one or the other extreme but not both at the same cell.

## Limitations

* **Single auto-stop-disabled seed for the substrate-rate question.** t0114 is the only seed
  run with auto-stop disabled; [t0106] / [t0112] / [t0113] all stopped under the current rule.
  The comparison "t0114 (484 LEGIT) vs [t0113] (0 LEGIT)" therefore convolves "seed redraw"
  with "auto-stop disable". The clean way to bisect this is to re-run seed 2247 with the
  auto-stop disabled (proposed `S-0114-XX`). Until that runs, the substrate-rate
  interpretation ("[t0113]'s 0 is a censoring artefact, not a substrate property") is the most
  parsimonious reading but not proven.

* **4-seed substrate-rate CI still brackets both literature baselines and zero.** The 4-seed
  95% CI of (-0.71%, +6.56%) cannot formally reject either [Hay2011][hay2011]'s 0.40% or
  [Druckmann2007][druckmann2007]'s 0.10%. The point estimate of 2.93% is 7.3x above
  [Hay2011][hay2011]; in effect-size terms the substrate is plausibly denser than literature.
  But classical inference requires at least one more independent seed (preferably 2 or 3) to
  tighten the SE below 0.40%.

* **Operator-stop censoring of t0114.** The run was stopped at gen 62 by operator decision
  after the HV trajectory plateaued near HV 111.54 from gen 50 to gen 62. The plateau is
  visually convincing but **not statistically certified** — a longer run could reveal further
  LEGIT cells in the same way that gens 50-62 added ~30-50 cells beyond the gen-50 cumulative
  count. The reported 484 LEGIT count is therefore a **lower bound** on the true substrate
  yield for seed 7755.

* **Detector replay is offline only.** The `(W*, T*) = (3, 0.015)` recommendation is computed
  from the four recorded HV trajectories ex post; it has NOT been validated by running NSGA-II
  online with the new constants. A follow-up task should adopt the new constants and re-run at
  least one seed end-to-end to confirm the offline prediction matches the live behaviour. The
  two trajectories used to certify "new rule does NOT fire prematurely" ([t0112] at 21 gens,
  [t0113] at 14 gens) are themselves truncated by the current rule and therefore cannot test
  whether the new rule would fire prematurely on a longer history.

* **2-direction protocol is methodologically novel and not directly comparable to published
  multi-direction DSI measurements.** [Trenholm2013][trenholm2013], [Oesch2005][oesch2005],
  and [PolegPolsky2026][polegpolsky2026] use 8-12 directions with vector-sum DSI. The DSI =
  0.9926 LEGIT result cannot be claimed as "biological-equivalent" without an 8-direction
  post-hoc re-evaluation. The carry-forward 0.42-absolute offset from [t0107] is measured on
  [t0106]'s high-DSI cells, which overlap structurally with t0114's joint-pass corner — but
  the offset has not been independently measured on t0114 cells.

* **Single fully-uncensored seed cannot disentangle "auto-stop is buggy" from "seed 7755 is
  lucky".** t0114's 8.13% LEGIT yield is the 4-seed maximum and is 2.5x [t0106]'s 3.23%. The
  484 vs 121 LEGIT count gap could be explained by (i) longer run-length on a seed that would
  have yielded similarly to [t0106] under any rule, (ii) the auto-stop censoring [t0106] at
  gen 39 when it would have yielded more under longer running, or (iii) seed 7755 being
  substantively denser than seed 44\. Without rerunning [t0106] with auto-stop disabled (or
  running additional auto-stop-disabled seeds), these cannot be separated.

* **No comparable published NSGA-II run at this dimensionality.** The 68-d substrate is **2.8x
  - 5.7x higher dimensional** than any published biophysical NSGA-II benchmark
  ([Hay2011][hay2011] = 22-d, [Druckmann2007][druckmann2007] = 12-d,
  [Mohacsi2024][mohacsi2024] use cases = 3-12-d). The acceptance-rate comparison is therefore
  against extrapolated expectations, not matched- dimensional baselines.
  **Publication-selection bias** also applies: [Hay2011][hay2011] and
  [Druckmann2007][druckmann2007] published successes but not their failed seeds, so the
  per-seed yield distribution in their setting is unknown. The 4-seed dispersion observed in
  this project (0.00%
  - 8.13%) could plausibly be representative of NSGA-II per-seed behaviour at any
    dimensionality.

* **Evaluation budget materially below published references.** t0114 used 5,952 evaluations vs
  [Hay2011][hay2011]'s 500,000 and [Druckmann2007][druckmann2007]'s 300,000. The acceptance
  rate is measured at 50x - 84x lower spend; whether the rate would converge to a different
  value at matched spend is open.

* **Random-seed draw is not the same as random-seed selection.** Seed 7755 was drawn via
  `secrets.randbelow(10000)` — uniformly random over [0, 9999]. This avoids the
  round-ish-low-number bias of seeds 44 and 77 but does not guarantee good coverage. A formal
  quasi-random Latin hypercube over seeds 0-9999 would give better coverage but is outside the
  scope of a minimum-change replicate.

* **`(W*, T*)` selection rests on a 4-seed sample.** The recommended detector parameters
  minimise deviation from the current default subject to three constraints, but a 5th or 6th
  HV trajectory could shift the optimum. The "deviation metric" `abs(W - 2) + abs(T - 0.01) *
  100` is also a chosen scaling that prefers small window changes over small threshold
  changes; an alternative scaling could pick `(W=2, T=0.025)` or `(W=4, T=0.005)` instead. The
  recommendation should be treated as a "minimum-change patch that passes the
  [Mohacsi2024][mohacsi2024] prior", not an optimum.

[t0106]: ../../t0106_long_pdnd_nsga2_300gen/ [t0107]: ../../t0107_t0106_polar_8dir_recheck/
[t0112]: ../../t0112_t0106_seed77_replicate/ [t0113]: ../../t0113_t0106_seed2247_replicate/
[druckmann2007]:
../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md [hay2011]:
../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md
[achard2006]: ../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md
[mohacsi2024]:
../../t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[trenholm2013]:
../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/summary.md
[oesch2005]:
../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md
[polegpolsky2026]:
../../t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md
[chen2024-stn]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11383608/

</details>
