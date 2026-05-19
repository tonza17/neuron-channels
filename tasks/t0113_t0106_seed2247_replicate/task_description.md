# t0113: Seed-2247 Random-Seed Replicate of t0106 Long 2-Direction NSGA-II

## Motivation

`t0106_long_pdnd_nsga2_300gen` (GA seed 44) produced **123 unique joint-pass cells** (DSI >= 0.5 AND
PD-rate >= 30 Hz, 3.3% acceptance rate) on the 68-d Bed B + 14-d morphology substrate. The follow-up
`t0112_t0106_seed77_replicate` (GA seed 77, randomly drawn at the time but selected from a small
candidate set) produced **only 7 unique joint-pass cells** (0.35% acceptance) on the identical
substrate using the same algorithm and tightened pool-restart cadence. The two seeds span a factor
of ~17 in joint-pass density, so the substrate-level acceptance rate is currently a 2-point sample
and cannot be reported as a substrate property.

Suggestion `S-0112-01` calls for at least three additional GA seeds at the t0112 cadence
(`_POOL_RESTART_EVERY = 10`, `N_GEN = 60` with HV-plateau auto-stop) to lift the substrate-rate
estimate from a 2-point sample to a 5-point sample with reportable mean and standard error against
the Hay2011 (0.40%) and Druckmann2007 (0.10%) literature baselines.

This task contributes **one of those additional seeds**, drawn **completely at random** rather than
from a curated candidate list. Random selection avoids any conscious or unconscious bias in seed
choice (e.g., the previous picks 44 and 77 were both round-ish numbers under 100). The seed used by
this task is **2247**, generated locally by `secrets.randbelow(10000)` immediately before task
creation. Two further seeds will be required to complete the S-0112-01 batch.

A secondary benefit of the random draw is that any pattern of "low seeds favourable / high seeds
unfavourable" (or vice versa) becomes detectable across the eventual 5-seed sample — drawing from
a broader range than 44-99 widens the support of the estimator.

## Scope

* **In scope (unchanged from t0106 / t0112)**: substrate (Bed B 54-d electrophys + 14-d morphology =
  68 free parameters), objectives (2-direction ratio DSI + PD-rate at 0 deg), NSGA-II
  hyperparameters (pop=96, SBX/PM operators), evaluation protocol (`N_EVAL_SEEDS = 3`, ratio DSI,
  silence guard active), HV-plateau termination constants (`HV_PLATEAU_WINDOW`,
  `HV_PLATEAU_MIN_HV_HISTORY`, `HV_PLATEAU_REL_THRESHOLD`).
* **In scope, changed from t0106**: GA seed (44 -> 2247, randomly drawn), pool-restart cadence (25
  -> 10 gens, same as t0112), gen ceiling (300 -> 60 with HV-plateau operator-stop preserved as the
  primary trigger).
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, the NSGA-II driver beyond the three constants above, the
  predictions asset schema, the metrics list, or the cost-watchdog wiring. Out-of-scope changes
  would compromise the like-for-like comparison with t0106 and t0112.

## Approach

1. **Fork t0112 code into `tasks/t0113_t0106_seed2247_replicate/code/`**: copy every algorithm-
   critical Python module (`nsga2_driver.py`, `constants.py`, `constants_morphology.py`,
   `evaluator.py`, `random_init.py`, `apply_params.py`, `build_cell_ais.py`, `extend_with_ais.py`,
   `parametric_placer.py`, `recorder.py`, `trial_helpers.py`, `generator_wrapper.py`,
   `hv_plateau_watchdog.py`, `cost_watchdog.py`, `bootstrap.py`, `paths.py`, `smoke_gate.py`,
   `test_evaluator_dsi_guard.py`, and any helper modules) plus the orchestration shell script. t0112
   (rather than t0106) is the canonical fork base because t0112 already carries the pool-restart
   cadence and N_GEN settings this task needs; copying from t0112 minimises the diff surface.
2. **Rewrite package import paths**: replace `tasks.t0112_t0106_seed77_replicate` with
   `tasks.t0113_t0106_seed2247_replicate` across every copied `.py` and `.sh` file. Do not touch
   upstream task references (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`, `tasks.t0092_*`,
   `tasks.t0093_*`).
3. **Apply exactly one constant patch**: in `constants.py`, rename `T0112_SEEDS = (77,)` to
   `T0113_SEEDS = (2247,)` and rename the matching `T0112_HARD_BUDGET_USD = 25.00` to
   `T0113_HARD_BUDGET_USD = 25.00`. Update the backwards-compatibility aliases at the bottom of the
   file to point at the new constants. `nsga2_driver.py` keeps `_POOL_RESTART_EVERY = 10` from t0112
   verbatim; `constants_morphology.py` keeps `N_GEN = 60` from t0112 verbatim. The diff against
   t0112 must be the seed constant rename plus the package-path rewrite, nothing else.
4. **Smoke gate locally** (5 checks identical to t0106 / t0112): single-eval driver run, ratio DSI
   synthetic sanity, silence-guard unit tests, pool-restart sanity, watchdog wiring. All five must
   pass before any Vast.ai provisioning.
5. **Provision Vast.ai single instance** with the same filter class as t0106 / t0112 (EPYC class
   CPU, >= 100 GB RAM, RTX 3060 Ti or equivalent idle GPU, reliability >= 0.99, dph <= 0.40, EPYC
   family post-filter).
6. **Launch** with cost cap $25 per-task and per-instance watchdog $20. Operator-stop on HV plateau
   (same window/threshold as t0106 / t0112) or at gen 60 ceiling, whichever comes first.
7. **Collect** the evaluator-side per-cell DSI / PD-rate / generation table as a predictions asset
   in the t0106 / t0112 schema (`spec_version: "2"`, gzipped JSON, fields `generation`,
   `vector_68d`, `objective_F_minimised`, `dsi_vector_sum` — back-compat field name storing ratio
   DSI — and `pd_rate_hz`).
8. **Compare** to t0106 (seed 44) and t0112 (seed 77):
   * Joint-pass cell count (DSI >= 0.5 AND PD >= 30 Hz) absolute and as % of total evaluations.
   * Best ratio DSI and best PD-rate frontier vs t0106's 1.0000 / 122.6 Hz and t0112's 0.9535 /
     114.8 Hz.
   * HV trajectory shape and plateau generation across the three seeds.
   * Pareto front overlap in parameter space between seed-2247 cells and their nearest seed-44 /
     seed-77 neighbours (uses the normalised z-scored L2 metric proposed in S-0112-04 if available;
     otherwise raw L2 alongside per-dimension z-score for the headline scatter).

## Expected Assets

* **1 predictions asset** at
  `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/`
  containing the per-cell DSI / PD-rate / generation table for every evaluated cell, mirroring the
  t0106 and t0112 predictions asset schemas. Required `metrics_at_creation` keys:
  `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`.

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is for
  CPU cores; the GPU sits idle on the selected Vast.ai offer.
* **Remote**: Vast.ai single instance, same provisioning class as t0106 / t0112 (high-core-count
  EPYC CPU node).
* **Cost cap**: $25 per-task default. **Per-instance watchdog**: $20 via
  `make_watchdog_from_machine_log`.
* **Expected actual cost**: ~$2-11 (t0112 spent $2.40 at gen 21 HV-plateau auto-stop; t0106 spent
  $10.37 at gen 40 plateau). The wide range reflects genuine uncertainty in plateau generation; if
  seed 2247 plateaus early (gen 15-25) the cost lands near t0112's $2-3, and if it runs out to gen
  40-60 the cost lands near t0106's $10-12.
* **Project envelope check**: confirm project remaining budget covers $25 hard cap before
  provisioning. If insufficient, halt and create an intervention file.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `pareto_front_3seeds.png` — overlay of strict Pareto fronts from t0106 (seed 44), t0112 (seed
   77), and t0113 (seed 2247) on DSI vs PD-rate axes; coloured by source task; answers "do the three
   seeds discover comparable Pareto frontiers?"
2. `hv_vs_gen_3seeds.png` — log-scale HV trajectory for all three seeds on the same axes with
   pool-restart events annotated; answers "is the HV trajectory shape seed-invariant under the
   cadence-10 protocol?"
3. `joint_pass_yield_per_gen_3seeds.png` — joint-pass cell count discovered per generation for all
   three seeds; answers "when does each seed first hit the joint-pass corner and what is the rate
   thereafter?"
4. `top50_morphologies_seed2247.png` — 10x5 grid of best 50 cells from t0113, coloured by
   archetype, in the same format as t0106's `top50_morphologies.png` and t0112's
   `top50_morphologies_seed77.png`; answers "are the best-yield morphologies the same archetypes as
   t0106 and t0112?"
5. `asymmetry_distribution_3seeds.png` — 4-panel histogram (soma offset, elongation, branch
   density gradient, primary branch PD concentration) for top-50 cells from all three seeds; answers
   "is the morphology distribution of high-yield cells seed-independent?"

### Tables

* `results/data/joint_pass_summary_3seeds.csv` — per-seed (44, 77, 2247): total evals, joint-pass
  count, joint-pass %, best DSI, best PD-rate, plateau generation.
* `results/data/pareto_front_overlap_3seeds.csv` — for each t0113 Pareto cell, the nearest-
  neighbour distance in normalised parameter space to its closest t0106 cell and its closest t0112
  cell. Use the z-scored L2 metric from S-0112-04 if completed; otherwise compute both raw L2 and
  z-scored L2 and document the choice in `results_detailed.md`.

### Registered metrics

Check `uv run python -u -m arf.scripts.aggregators.aggregate_metrics --format json` and run every
registered metric that applies. At minimum:

* `direction_selectivity_index` — best ratio DSI across all evaluated cells. Sub-variant
  `best_legit` = highest non-DSI=1.0 cell; sub-variant `dsi_eq_one_count` = number of cells at
  exactly DSI = 1.0 (silence-guard or single-spike artefacts per t0106 / t0112 reporting).

Operational metrics (not registered): `joint_pass_count`, `best_pd_rate_hz` (not a registered metric
per the t0112 audit), `n_cells_evaluated_total`, `hv_plateau_gen`, `n_gen_completed`,
`efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`.

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative answer,
not a hedge:

1. **Seed-2247 joint-pass count.** Does seed 2247 produce >= 40 unique joint-pass cells
   (matching/exceeding t0106 substrate-populated regime), 7-39 cells (intermediate, t0112-like), 1-6
   cells (sparse), or 0 (substrate not populated at this seed)?
2. **Best ratio DSI.** Does seed 2247's best ratio DSI reach or exceed 0.95?
3. **Best PD-rate.** Does seed 2247's best PD-rate reach or exceed 100 Hz?
4. **Three-seed substrate-rate estimate.** Combining t0106 (123 cells / 3,744 evals), t0112 (7 cells
   / 2,016 evals), and t0113 (N cells / M evals), what is the substrate-level mean joint-pass
   acceptance rate and its standard error? Does the three-seed mean fall within the Hay2011 (0.40%)
   / Druckmann2007 (0.10%) literature envelope?
5. **HV-plateau generation.** At what generation does the HV-plateau detector fire for seed 2247,
   and is the plateau gen consistent with the t0106 (gen 40) / t0112 (gen 21) range, or does it land
   outside it?
6. **Cadence-10 wall-clock confirmation.** Is the per-generation wall-clock for seed 2247 within 20%
   of t0112's 620 s/gen baseline? (Confirms the cadence-10 speedup persists at a third seed.)
7. **Pareto front overlap in normalised parameter space.** Are seed-2247 Pareto cells closer to
   seed-44 cells, seed-77 cells, or roughly equidistant from both?

## Cross-References

* **Parent tasks**: `t0106_long_pdnd_nsga2_300gen` (original substrate, driver, baseline) and
  `t0112_t0106_seed77_replicate` (fork base for the cadence-10 / N_GEN-60 protocol).
* **Source suggestion**: `S-0112-01` (multi-seed substrate-rate confirmation at restart cadence 10).
  This task contributes one of the >= 3 additional seeds requested by the suggestion; two more seeds
  (drawn separately) will be needed to complete the S-0112-01 batch.
* **Related caveat tasks**: `t0107_t0106_polar_8dir_recheck` (8-direction polar re-evaluation
  showing 2-direction ratio DSI overstates selectivity by ~0.42 absolute). Polar re-evaluation of
  any t0113 joint-pass cells is out of scope for this task but should be tracked as a follow-up
  suggestion mirroring S-0112-05.
* **Brainstorm source**: none directly. This task is the direct realisation of S-0112-01 with a
  random seed.
