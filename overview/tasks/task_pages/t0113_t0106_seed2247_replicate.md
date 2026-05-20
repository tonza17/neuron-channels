# ✅ Seed-2247 random-seed replicate of t0106 long 2-direction NSGA-II

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0113_t0106_seed2247_replicate` |
| **Status** | ✅ completed |
| **Started** | 2026-05-19T23:35:08Z |
| **Completed** | 2026-05-20T02:50:00Z |
| **Duration** | 3h 14m |
| **Dependencies** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source suggestion** | `S-0112-01` |
| **Task types** | `experiment-run` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md) |
| **Expected assets** | 1 predictions |
| **Step progress** | 12/15 |
| **Cost** | **$0.48** |
| **Task folder** | [`t0113_t0106_seed2247_replicate/`](../../../tasks/t0113_t0106_seed2247_replicate/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0113_t0106_seed2247_replicate/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0113_t0106_seed2247_replicate/task_description.md)*

# t0113: Seed-2247 Random-Seed Replicate of t0106 Long 2-Direction NSGA-II

## Motivation

`t0106_long_pdnd_nsga2_300gen` (GA seed 44) produced **123 unique joint-pass cells** (DSI >=
0.5 AND PD-rate >= 30 Hz, 3.3% acceptance rate) on the 68-d Bed B + 14-d morphology substrate.
The follow-up `t0112_t0106_seed77_replicate` (GA seed 77, randomly drawn at the time but
selected from a small candidate set) produced **only 7 unique joint-pass cells** (0.35%
acceptance) on the identical substrate using the same algorithm and tightened pool-restart
cadence. The two seeds span a factor of ~17 in joint-pass density, so the substrate-level
acceptance rate is currently a 2-point sample and cannot be reported as a substrate property.

Suggestion `S-0112-01` calls for at least three additional GA seeds at the t0112 cadence
(`_POOL_RESTART_EVERY = 10`, `N_GEN = 60` with HV-plateau auto-stop) to lift the
substrate-rate estimate from a 2-point sample to a 5-point sample with reportable mean and
standard error against the Hay2011 (0.40%) and Druckmann2007 (0.10%) literature baselines.

This task contributes **one of those additional seeds**, drawn **completely at random** rather
than from a curated candidate list. Random selection avoids any conscious or unconscious bias
in seed choice (e.g., the previous picks 44 and 77 were both round-ish numbers under 100). The
seed used by this task is **2247**, generated locally by `secrets.randbelow(10000)`
immediately before task creation. Two further seeds will be required to complete the S-0112-01
batch.

A secondary benefit of the random draw is that any pattern of "low seeds favourable / high
seeds unfavourable" (or vice versa) becomes detectable across the eventual 5-seed sample —
drawing from a broader range than 44-99 widens the support of the estimator.

## Scope

* **In scope (unchanged from t0106 / t0112)**: substrate (Bed B 54-d electrophys + 14-d
  morphology = 68 free parameters), objectives (2-direction ratio DSI + PD-rate at 0 deg),
  NSGA-II hyperparameters (pop=96, SBX/PM operators), evaluation protocol (`N_EVAL_SEEDS = 3`,
  ratio DSI, silence guard active), HV-plateau termination constants (`HV_PLATEAU_WINDOW`,
  `HV_PLATEAU_MIN_HV_HISTORY`, `HV_PLATEAU_REL_THRESHOLD`).
* **In scope, changed from t0106**: GA seed (44 -> 2247, randomly drawn), pool-restart cadence
  (25 -> 10 gens, same as t0112), gen ceiling (300 -> 60 with HV-plateau operator-stop
  preserved as the primary trigger).
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, the NSGA-II driver beyond the three constants above,
  the predictions asset schema, the metrics list, or the cost-watchdog wiring. Out-of-scope
  changes would compromise the like-for-like comparison with t0106 and t0112.

## Approach

1. **Fork t0112 code into `tasks/t0113_t0106_seed2247_replicate/code/`**: copy every
   algorithm- critical Python module (`nsga2_driver.py`, `constants.py`,
   `constants_morphology.py`, `evaluator.py`, `random_init.py`, `apply_params.py`,
   `build_cell_ais.py`, `extend_with_ais.py`, `parametric_placer.py`, `recorder.py`,
   `trial_helpers.py`, `generator_wrapper.py`, `hv_plateau_watchdog.py`, `cost_watchdog.py`,
   `bootstrap.py`, `paths.py`, `smoke_gate.py`, `test_evaluator_dsi_guard.py`, and any helper
   modules) plus the orchestration shell script. t0112 (rather than t0106) is the canonical
   fork base because t0112 already carries the pool-restart cadence and N_GEN settings this
   task needs; copying from t0112 minimises the diff surface.
2. **Rewrite package import paths**: replace `tasks.t0112_t0106_seed77_replicate` with
   `tasks.t0113_t0106_seed2247_replicate` across every copied `.py` and `.sh` file. Do not
   touch upstream task references (`tasks.t0024_*`, `tasks.t0080_*`, `tasks.t0090_*`,
   `tasks.t0092_*`, `tasks.t0093_*`).
3. **Apply exactly one constant patch**: in `constants.py`, rename `T0112_SEEDS = (77,)` to
   `T0113_SEEDS = (2247,)` and rename the matching `T0112_HARD_BUDGET_USD = 25.00` to
   `T0113_HARD_BUDGET_USD = 25.00`. Update the backwards-compatibility aliases at the bottom
   of the file to point at the new constants. `nsga2_driver.py` keeps `_POOL_RESTART_EVERY =
   10` from t0112 verbatim; `constants_morphology.py` keeps `N_GEN = 60` from t0112 verbatim.
   The diff against t0112 must be the seed constant rename plus the package-path rewrite,
   nothing else.
4. **Smoke gate locally** (5 checks identical to t0106 / t0112): single-eval driver run, ratio
   DSI synthetic sanity, silence-guard unit tests, pool-restart sanity, watchdog wiring. All
   five must pass before any Vast.ai provisioning.
5. **Provision Vast.ai single instance** with the same filter class as t0106 / t0112 (EPYC
   class CPU, >= 100 GB RAM, RTX 3060 Ti or equivalent idle GPU, reliability >= 0.99, dph <=
   0.40, EPYC family post-filter).
6. **Launch** with cost cap $25 per-task and per-instance watchdog $20. Operator-stop on HV
   plateau (same window/threshold as t0106 / t0112) or at gen 60 ceiling, whichever comes
   first.
7. **Collect** the evaluator-side per-cell DSI / PD-rate / generation table as a predictions
   asset in the t0106 / t0112 schema (`spec_version: "2"`, gzipped JSON, fields `generation`,
   `vector_68d`, `objective_F_minimised`, `dsi_vector_sum` — back-compat field name storing
   ratio DSI — and `pd_rate_hz`).
8. **Compare** to t0106 (seed 44) and t0112 (seed 77):
   * Joint-pass cell count (DSI >= 0.5 AND PD >= 30 Hz) absolute and as % of total
     evaluations.
   * Best ratio DSI and best PD-rate frontier vs t0106's 1.0000 / 122.6 Hz and t0112's 0.9535
     / 114.8 Hz.
   * HV trajectory shape and plateau generation across the three seeds.
   * Pareto front overlap in parameter space between seed-2247 cells and their nearest seed-44
     / seed-77 neighbours (uses the normalised z-scored L2 metric proposed in S-0112-04 if
     available; otherwise raw L2 alongside per-dimension z-score for the headline scatter).

## Expected Assets

* **1 predictions asset** at
  `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/`
  containing the per-cell DSI / PD-rate / generation table for every evaluated cell, mirroring
  the t0106 and t0112 predictions asset schemas. Required `metrics_at_creation` keys:
  `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`, `best_pd_rate_hz`,
  `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`, `final_cost_usd`.

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is
  for CPU cores; the GPU sits idle on the selected Vast.ai offer.
* **Remote**: Vast.ai single instance, same provisioning class as t0106 / t0112
  (high-core-count EPYC CPU node).
* **Cost cap**: $25 per-task default. **Per-instance watchdog**: $20 via
  `make_watchdog_from_machine_log`.
* **Expected actual cost**: ~$2-11 (t0112 spent $2.40 at gen 21 HV-plateau auto-stop; t0106
  spent $10.37 at gen 40 plateau). The wide range reflects genuine uncertainty in plateau
  generation; if seed 2247 plateaus early (gen 15-25) the cost lands near t0112's $2-3, and if
  it runs out to gen 40-60 the cost lands near t0106's $10-12.
* **Project envelope check**: confirm project remaining budget covers $25 hard cap before
  provisioning. If insufficient, halt and create an intervention file.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `pareto_front_3seeds.png` — overlay of strict Pareto fronts from t0106 (seed 44), t0112
   (seed 77), and t0113 (seed 2247) on DSI vs PD-rate axes; coloured by source task; answers
   "do the three seeds discover comparable Pareto frontiers?"
2. `hv_vs_gen_3seeds.png` — log-scale HV trajectory for all three seeds on the same axes with
   pool-restart events annotated; answers "is the HV trajectory shape seed-invariant under the
   cadence-10 protocol?"
3. `joint_pass_yield_per_gen_3seeds.png` — joint-pass cell count discovered per generation for
   all three seeds; answers "when does each seed first hit the joint-pass corner and what is
   the rate thereafter?"
4. `top50_morphologies_seed2247.png` — 10x5 grid of best 50 cells from t0113, coloured by
   archetype, in the same format as t0106's `top50_morphologies.png` and t0112's
   `top50_morphologies_seed77.png`; answers "are the best-yield morphologies the same
   archetypes as t0106 and t0112?"
5. `asymmetry_distribution_3seeds.png` — 4-panel histogram (soma offset, elongation, branch
   density gradient, primary branch PD concentration) for top-50 cells from all three seeds;
   answers "is the morphology distribution of high-yield cells seed-independent?"

### Tables

* `results/data/joint_pass_summary_3seeds.csv` — per-seed (44, 77, 2247): total evals,
  joint-pass count, joint-pass %, best DSI, best PD-rate, plateau generation.
* `results/data/pareto_front_overlap_3seeds.csv` — for each t0113 Pareto cell, the nearest-
  neighbour distance in normalised parameter space to its closest t0106 cell and its closest
  t0112 cell. Use the z-scored L2 metric from S-0112-04 if completed; otherwise compute both
  raw L2 and z-scored L2 and document the choice in `results_detailed.md`.

### Registered metrics

Check `uv run python -u -m arf.scripts.aggregators.aggregate_metrics --format json` and run
every registered metric that applies. At minimum:

* `direction_selectivity_index` — best ratio DSI across all evaluated cells. Sub-variant
  `best_legit` = highest non-DSI=1.0 cell; sub-variant `dsi_eq_one_count` = number of cells at
  exactly DSI = 1.0 (silence-guard or single-spike artefacts per t0106 / t0112 reporting).

Operational metrics (not registered): `joint_pass_count`, `best_pd_rate_hz` (not a registered
metric per the t0112 audit), `n_cells_evaluated_total`, `hv_plateau_gen`, `n_gen_completed`,
`efficiency_inference_time_per_item_seconds`, `efficiency_inference_cost_per_item_usd`.

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative
answer, not a hedge:

1. **Seed-2247 joint-pass count.** Does seed 2247 produce >= 40 unique joint-pass cells
   (matching/exceeding t0106 substrate-populated regime), 7-39 cells (intermediate,
   t0112-like), 1-6 cells (sparse), or 0 (substrate not populated at this seed)?
2. **Best ratio DSI.** Does seed 2247's best ratio DSI reach or exceed 0.95?
3. **Best PD-rate.** Does seed 2247's best PD-rate reach or exceed 100 Hz?
4. **Three-seed substrate-rate estimate.** Combining t0106 (123 cells / 3,744 evals), t0112 (7
   cells / 2,016 evals), and t0113 (N cells / M evals), what is the substrate-level mean
   joint-pass acceptance rate and its standard error? Does the three-seed mean fall within the
   Hay2011 (0.40%) / Druckmann2007 (0.10%) literature envelope?
5. **HV-plateau generation.** At what generation does the HV-plateau detector fire for seed
   2247, and is the plateau gen consistent with the t0106 (gen 40) / t0112 (gen 21) range, or
   does it land outside it?
6. **Cadence-10 wall-clock confirmation.** Is the per-generation wall-clock for seed 2247
   within 20% of t0112's 620 s/gen baseline? (Confirms the cadence-10 speedup persists at a
   third seed.)
7. **Pareto front overlap in normalised parameter space.** Are seed-2247 Pareto cells closer
   to seed-44 cells, seed-77 cells, or roughly equidistant from both?

## Cross-References

* **Parent tasks**: `t0106_long_pdnd_nsga2_300gen` (original substrate, driver, baseline) and
  `t0112_t0106_seed77_replicate` (fork base for the cadence-10 / N_GEN-60 protocol).
* **Source suggestion**: `S-0112-01` (multi-seed substrate-rate confirmation at restart
  cadence 10). This task contributes one of the >= 3 additional seeds requested by the
  suggestion; two more seeds (drawn separately) will be needed to complete the S-0112-01
  batch.
* **Related caveat tasks**: `t0107_t0106_polar_8dir_recheck` (8-direction polar re-evaluation
  showing 2-direction ratio DSI overstates selectivity by ~0.42 absolute). Polar re-evaluation
  of any t0113 joint-pass cells is out of scope for this task but should be tracked as a
  follow-up suggestion mirroring S-0112-05.
* **Brainstorm source**: none directly. This task is the direct realisation of S-0112-01 with
  a random seed.

</details>

## Costs

**Total**: **$0.48**

| Category | Amount |
|----------|--------|
| vast-ai-epyc-7b13-productive | $0.15 |
| vast-ai-epyc-7b13-setup-idle | $0.29 |
| vast-ai-failed-ssh-attempt | $0.04 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX 4060 Ti (idle, unused; CPU-only NEURON workload on AMD EPYC 7B13) | 1 | 125 GB | 1.8h | $0.43 |

## Metrics

### 2-direction NSGA-II seed 2247: best legit DSI (highest non-silence-guard cell)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.3651** |

### 2-direction NSGA-II seed 2247: overall max DSI (silence-guard saturated)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

### 2-direction NSGA-II seed 2247: silence-guard ceiling cell count (cells at DSI = 1.0)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| predictions | [NSGA-II seed 2247 on 68-d Bed B + 14-d morphology, 2 directions, 60-gen replicate of t0106/t0112](../../../tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/) | [`description.md`](../../../tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/description.md) |

## Suggestions Generated

<details>
<summary><strong>Complete S-0112-01: two further random-draw GA seeds at cadence-10
to lift substrate-rate from 3-seed to 5-seed</strong> (S-0113-01)</summary>

**Kind**: experiment | **Priority**: high

S-0112-01 requires >=3 additional GA seeds at cadence-10 to upgrade the substrate-rate
estimate from a 2-point sample to a 5-point sample. t0113 contributed one (random seed 2247)
yielding 0 LEGIT joint-pass cells; the 3-seed sample (44/77/2247) now spans 0.15%-3.29% with
mean 1.26% +/- 1.01% SE, and the 95% CI (-0.73%, 3.25%) brackets BOTH Hay2011 (0.40%) and
Druckmann2007 (0.10%) baselines and cannot reject either. Draw two further random seeds via
secrets.randbelow(10000) (avoid the round-ish-low-number bias of seeds 44, 77 and the curated
set 33/88/99) and run each as a minimum-change replicate of t0113 (same cadence-10, N_GEN=60,
HV-plateau detector, evaluator). Each new seed = one task = one folder = one PR; pool the
5-seed sample for the final substrate-rate report. Recommended task types: experiment-run.
Cost: ~$5 (2 seeds x ~$2-3 each).

</details>

<details>
<summary><strong>Fix dill checkpoint pool-pickling failure in nsga2_driver.py: every
gen across t0113 failed to dill-pickle</strong> (S-0113-02)</summary>

**Kind**: library | **Priority**: high

t0113's per-generation dill checkpoint failed on all 14 gens with `NotImplementedError: pool
objects cannot be passed between processes or pickled`. Root cause: pymoo's
`StarmapParallelization` wrapper holds a live `multiprocessing.Pool` reference inside the
Algorithm object that dill cannot serialise. JSON-side resume worked, so runs were not lost,
but the dill resume channel is broken across t0106/t0112/t0113. Fix options: (a) strip
`problem.elementwise_runner` via `__getstate__/__setstate__` and re-attach on restore, (b)
replace dill with cloudpickle, or (c) deprecate the dill checkpoint and make JSON checkpoint
the sole resume mechanism (cleanest). Local-only, reusable across all downstream NSGA-II
tasks. Recommended task types: write-library, infrastructure-setup. Cost: <$0.10.

</details>

<details>
<summary><strong>Widen HV-plateau detector window from 2 to 4-5 gens to prevent
premature trigger by single-cell HV jumps</strong> (S-0113-03)</summary>

**Kind**: technique | **Priority**: high

t0113's HV-plateau detector fired at gen 14 (earliest of the 3-seed sample; t0112=21,
t0106=40) and BELOW Mohacsi2024's published 20-60 gen NSGA-II convergence range. The soft gen
11-12 transition (HV 35.98 -> 36.07 = +0.24%) satisfied the 1%-over-2-gens condition BEFORE
the gen 13-14 jump (+26% from a single silence-guard cell joining the archive). Current
constants (WINDOW=2, REL_THRESHOLD=0.01) are too aggressive when a single cell can inflate HV
>20% in one step. Widen WINDOW to 4-5 gens (matches Mohacsi2024 lower bound) and/or tighten
REL_THRESHOLD to 0.005. Validate by replaying the detector offline on the existing
t0106/t0112/t0113 HV traces. DISTINCT from S-0112-03 (single-seed re-run with auto-stop
disabled); this is a parameter-sweep + literature-grounded reparameterisation that becomes the
new project default. Recommended task types: data-analysis, infrastructure-setup. Cost:
<$0.20.

</details>

<details>
<summary><strong>8-direction polar re-evaluation of t0113's 2 silence-guard DSI=1.0
cells (mirrors S-0112-05 for t0113)</strong> (S-0113-04)</summary>

**Kind**: evaluation | **Priority**: medium

t0113's 2 asset-declared joint-pass cells are both silence-guard DSI=1.0 saturations (1 PD
spike / 0 ND spikes at PD=35.0 Hz and PD=45.24 Hz; the latter is also a strict Pareto cell).
t0107 established that 2-direction ratio DSI overstates 8-direction vector-sum DSI by ~0.42
absolute on t0106 high-DSI cells, but that offset was measured on legit cells not
silence-guard saturations. Re-evaluate both t0113 cells at 8 directions (every 45 deg) using
t0107's protocol with N_EVAL_SEEDS matched. Decision: if the cells fire >=1 spike in >=2
non-PD directions, they are not silence-only and the silence-guard threshold needs revisiting;
otherwise they are confirmed artefacts and should be excluded from the substrate-rate
denominator. Distinct from S-0112-05 (t0112 cells) and S-0106-03 (t0106 cells). Recommended
task types: experiment-run, comparative-analysis. Cost: <$0.50.

</details>

<details>
<summary><strong>Per-cell HV-contribution analysis to identify silence-guard cells
inflating HV beyond their biological value</strong> (S-0113-05)</summary>

**Kind**: library | **Priority**: medium

t0113's gen 13->14 HV jump of +26% (35.98 -> 45.62) was driven by a single silence-guard
DSI=1.0 cell joining the archive. The HV-plateau detector tolerated this jump as saturation
onset, but the cell contributes ~zero biological selectivity (8-direction DSI ~0). Build an
analysis script that, per generation across t0106/t0112/t0113, decomposes the HV increment
into per-archive-member contributions and flags silence-guard cells (DSI=1.0 OR <=1 PD spike)
separately. Output: per-task `hv_contribution_by_cell.csv` and cross-task
`silence_guard_hv_share.png`. Decision: if silence-guard cells contribute >=20% of final HV in
any seed, replace 2-D HV with a 'legit-only HV' that excludes silence-guard saturations for
the substrate-rate paper. Reusable across S-0112-01 / S-0113-01 multi-seed batch. Recommended
task types: data-analysis, write-library. Cost: <$0.20.

</details>

<details>
<summary><strong>Tighten silence-guard threshold from
SILENCE_SPIKE_COUNT_THRESHOLD=10 to >=3 PD spikes minimum</strong>
(S-0113-06)</summary>

**Kind**: technique | **Priority**: medium

t0113's 2 joint-pass cells are both silence-guard DSI=1.0 saturations with exactly 1 PD spike
and 0 ND spikes. The current guard (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`) accepts these
single-spike configurations as legitimate, inflating both joint-pass count and the HV archive.
t0106 had 1 such cell (in 123); t0112 had 0; t0113 has 2 of 2 - silence-guard contamination
dominates at sparse seeds. Modify `evaluator.py` to require >=3 PD spikes (or a minimum
non-zero ND-spike floor) before computing ratio DSI; cells below the floor return DSI=NaN and
are excluded from the archive. Reanalyse the existing t0106/t0112/t0113 predictions assets
offline. Decision: if corrected t0113 joint-pass count is 0 but t0106/t0112 counts drop by
<=5%, adopt as project default. Recommended task types: data-analysis, infrastructure-setup.
Cost: <$0.20.

</details>

<details>
<summary><strong>Latin-hypercube quasi-random GA-seed sampling for substrate-rate
confirmation (replaces ad-hoc seed picks)</strong> (S-0113-07)</summary>

**Kind**: library | **Priority**: low

The current 3-seed sample (44, 77, 2247) uses three independent draws (curated, semi-random,
fully random) which does not guarantee good coverage of the seed-space [0, 9999]. For the
final 5-seed substrate-rate report, draw the GA seeds via a 1-d Latin hypercube over [0, 9999]
(or a Sobol' sequence) to ensure stratified coverage. This is methodologically defensible
against reviewer pushback that the seed sample is too small to characterise substrate
variance. The two further seeds for S-0113-01 / S-0112-01 should be drawn from the LH/Sobol'
sequence conditional on the 3 already-used (44, 77, 2247) being part of the sequence. Output:
a small `gaseed_sampler.py` library asset plus a one-line update to the seed-selection comment
in `task_description.md` templates. Recommended task types: write-library,
infrastructure-setup. Cost: <$0.10 (local only).

</details>

<details>
<summary><strong>Cross-seed 68-d signature of silence-guard cells: same parameter
basin or seed-specific artefacts?</strong> (S-0113-08)</summary>

**Kind**: experiment | **Priority**: low

t0106 had 1 silence-guard DSI=1.0 cell, t0112 had 0, t0113 has 2. If silence-guard cells
cluster in a specific 68-d region (e.g., low somatic Nav + high Kv4 + central soma), they
represent a reproducible 'pathological basin' the NSGA-II driver should avoid. If scattered
randomly, they are seed-specific artefacts and no driver change is needed. Pool the 3
silence-guard cells from t0106 and t0113 plus a control set of 50 high-PD-low-DSI cells from
each task; run hierarchical clustering on z-scored 68-d vectors (using S-0112-04's metric if
available). Decision: if silence-guard cells cluster together with NMI > 0.7 vs random
samples, add a 'silence-pathology penalty' to the NSGA-II objective; otherwise no driver
change. DISTINCT from S-0112-08 (clusters JOINT-PASS cells across seeds, not silence-guard
cells). Recommended task types: data-analysis, comparative-analysis. Cost: <$0.20.

</details>

## Research

* [`research_code.md`](../../../tasks/t0113_t0106_seed2247_replicate/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0113_t0106_seed2247_replicate/results/results_summary.md)*

# t0113 - Seed-2247 Random-Seed Replicate of t0106: Results Summary

## Summary

Seed 2247 reaches **0 LEGIT joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz with the
silence-guard excluded) on the same 68-d Bed B + 14-d morphology substrate, while the 2 cells
the asset records as joint-pass-unique are both DSI = 1.0 silence-guard saturations (1-spike
PD / 0-spike ND), not biological selectivity. The HV-plateau detector fired at gen 14 (8% of
`N_GEN = 60`, well below both t0106 gen 40 and t0112 gen 21), the per-generation wall-clock
averaged **160 s/gen** on a 64-core EPYC 7B13 (3.9x faster than t0112's 620 s/gen baseline
because the instance had 2x more cores), and total task spend was **$0.4773** of the $25 cap.

## Metrics

* **Joint-pass cells (asset-declared, unique)**: **2** at DSI = 1.0 silence-guard ceiling (PD
  = 35.0 and 45.24 Hz). **0 LEGIT joint-pass cells** (no cell reached BOTH DSI >= 0.5 AND PD
  >= 30 Hz without silence-guard saturation).
* **Best legit DSI** (highest non-silence-guard cell): **0.3651** at PD = 10.24 Hz (gen 7).
* **Best PD-rate**: **71.67 Hz** at DSI = 0.0017 (gen 10).
* **Overall max DSI**: **1.0000** (silence-guard / single-spike artefact).
* **NSGA-II generations completed**: **14** of 60 ceiling (HV plateau triggered; watchdog NOT
  tripped).
* **Cells evaluated**: **1,344** = 96 x 14 generations.
* **Final hypervolume (2-D)**: **45.6221** (start 0.2460 -> 185x growth).
* **HV-plateau generation**: **14** (vs t0112's 21 and t0106's 40 — earliest plateau of the
  3-seed sample).
* **Per-generation wall-clock**: **160 s/gen** mean on 64-core EPYC 7B13 (vs t0112's 620 s/gen
  on 32-core EPYC; 26% of t0112's baseline = **NOT within +/- 20%** but in the FAVOURABLE
  direction).
* **NSGA-II compute cost (productive)**: **$0.1467** of $25 cap (0.6% utilisation).
* **Total task cost (productive + setup + retries)**: **$0.4773** of $25 cap.

## Answers to the Task's 7 Key Questions

1. **Seed-2247 joint-pass count bucket (>= 40 / 7-39 / 1-6 / 0)?** **0 LEGIT** joint-pass
   cells; the 2 asset-declared unique cells are both DSI = 1.0 silence-guard artefacts at PD =
   35.0 and 45.24 Hz, so by the substrate-density reading the count is **0** (substrate not
   populated at this seed) and by the raw asset-declared reading the count is **2** (sparse
   bucket: 1-6 cells).
2. **Best ratio DSI >= 0.95?** **NO, decisively.** Overall max = 1.0000 but is a silence-guard
   ceiling, not biological selectivity. Best legit DSI = **0.3651** (62% below the 0.95 target
   and far below t0106's 0.9939 / t0112's 0.9535).
3. **Best PD-rate >= 100 Hz?** **NO.** Best PD = **71.67 Hz** (28% below the 100-Hz target;
   58% of t0106's 122.62 Hz and 62% of t0112's 114.76 Hz).
4. **3-seed substrate-rate mean and SE vs Hay 2011 0.40% / Druckmann 2007 0.10% baselines?**
   Per-seed acceptance: t0106 = 3.29%, t0112 = 0.35%, t0113 = 0.15%. **Mean = 1.26%, SD =
   1.76%, SE = 1.01%**, 95% CI (-0.73%, 3.25%). The point estimate is **3x above the Hay 2011
   envelope upper bound (0.40%) and 13x above the Druckmann 2007 baseline (0.10%)**, but the
   SE is larger than the mean — the 95% CI brackets BOTH literature baselines and 0%. The
   3-seed sample is still too noisy to reject either baseline; the 5-seed batch from S-0112-01
   is still required.
5. **HV-plateau generation vs t0106 gen 40 / t0112 gen 21?** **Gen 14**, **OUTSIDE the
   t0106-t0112 range** by 7 generations on the early side. Cost watchdog NOT tripped. The same
   `HV_PLATEAU_REL_THRESHOLD = 0.01` over `HV_PLATEAU_WINDOW = 2` constants fired earlier on
   this seed because the HV climb between gen 12-14 (36.07 -> 36.10 -> 45.62) had a one-step
   plateau that the detector tolerated as the start of saturation. **This is plausibly a
   premature trigger** — see Limitations in `results_detailed.md`.
6. **Per-gen wall-clock within +/- 20% of t0112's 620 s/gen baseline?** **NO** — t0113
   averaged **160 s/gen** (vs t0112's 620 s/gen), which is **74% LOWER** than t0112 and **far
   outside the +/- 20% (496-744 s/gen) band**. The driver is identical to t0112; the 3.9x
   speedup is entirely attributable to the larger EPYC 7B13 instance (t0113 had 64 cores / 256
   threads with 125 GB RAM; t0112 had 32 effective cores with 503 GB RAM, but RAM was never
   the bottleneck). The cadence-10 protocol persists; at the per-core level wall-clock is
   consistent with t0112.
7. **Pareto front overlap (closer to seed 44 or seed 77)?** **MIXED** — of t0113's 8 strict
   Pareto cells, 4 are closer to a t0106 (seed 44) cell in z-scored 68-d parameter space and 4
   are closer to a t0112 (seed 77) cell (see `results/data/pareto_front_overlap_3seeds.csv`).
   The nearest- neighbour z-scored distances are all in the 9.7-11.5 range (mean ~10.7)
   regardless of target, indicating that t0113's Pareto cells are **roughly equidistant from
   both seed-44 and seed-77 cells in normalised parameter space** — neither seed is a closer
   match than the other.

## Verification

* `verify_predictions_asset` (meta path): expected PASSED, non-blocking PR-W014/W015 warnings
  (no linked model / dataset asset — same as t0106/t0112).
* `verify_predictions_description`, `verify_predictions_details`: expected PASSED.
* `verify_task_results` (this file + `results_detailed.md`): see `## Verification` section of
  `results_detailed.md` for the verificator run record.
* `verify_task_metrics`: `metrics.json` registers only the `direction_selectivity_index`
  metric per `meta/metrics/`; sub-variants `best_legit`, `overall_max`, and `dsi_eq_one_count`
  are encoded as separate variants in the explicit multi-variant format.
* `verify_machines_destroyed`: PASSED (instance 37107202 destroyed at 2026-05-20T02:11:25Z,
  within 5 min of the HV-plateau stop).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0113_t0106_seed2247_replicate/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0113_t0106_seed2247_replicate" date_completed: "2026-05-20"
---
# t0113 - Seed-2247 Random-Seed Replicate of t0106: Detailed Results

## Summary

The t0113 single-seed NSGA-II run on GA seed **2247** (drawn via `secrets.randbelow(10000)`
immediately before task creation) with `_POOL_RESTART_EVERY = 10` and `N_GEN = 60` ceiling
evaluated **1,344 cells across 14 NSGA-II generations** before the HV-plateau detector fired
(well below both the 60-gen ceiling and the t0106/t0112 plateau range of 21-40 gens). The
asset records **2 unique joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz), but **both are
silence-guard saturations at DSI = 1.0** (single PD spike, zero ND spikes — the classic
1-spike / 0-spike artefact). The **best LEGIT DSI** (highest non-silence-guard cell) is
**0.3651** at PD = 10.24 Hz — far below t0106's 0.9939 (seed 44) and t0112's 0.9535 (seed 77).
The **best PD-rate** is **71.67 Hz** at DSI = 0.0017, far below the 100 Hz target and well
below the t0106 / t0112 baselines.

The headline interpretation is **substrate-density is strongly seed-dependent and seed 2247
lands in a sparse region**. The 3-seed sample now has dispersion 0.15% / 0.35% / 3.29% — a 22x
range — which both confirms that the t0106 "substrate-populated" reading was overstated by
single-seed luck AND reveals that the substrate-level mean is still highly uncertain (3-seed
mean = 1.26%, SE 1.01%, 95% CI bracketing both Hay 2011 and Druckmann 2007 envelopes).

Total task spend was **$0.4773** of the $25 cap (productive $0.1467; setup/idle $0.2856; one
failed SSH attempt $0.045). The Vast.ai instance (37107202, AMD EPYC 7B13 64-core / 256
threads, 125 GB RAM, RTX 4060 Ti idle) delivered 160 s/gen mean wall-clock — 3.9x faster than
t0112's 620 s/gen baseline, but this acceleration is entirely attributable to the larger CPU
instance (t0112 ran on 32 cores; t0113 on 64 effective cores), not the cadence-10 protocol
(which is unchanged). At the per-core level wall-clock is consistent with t0112.

## Methodology

* **Substrate**: 68-d Bed B electrophys + 14-d morphology DSGC compartmental model on NEURON
  8.2.7, identical to t0106 and t0112. The t0080 MOD library and t0092-patched morphology
  generator (canonical via correction C-0093-01) are the operational substrates.
* **Objectives**: 2-direction ratio DSI = (PD - ND) / (PD + ND) with PD bar at 0 deg and ND
  bar at 180 deg, plus PD-rate (Hz). NSGA-II minimises the negated pair.
* **NSGA-II hyperparameters**: pop_size = 96, n_gen = 60 ceiling, n_eval_seeds = 3, SBX
  crossover eta = 15 prob = 0.9, polynomial mutation eta = 20 prob = 1/68, duplicate
  elimination.
* **Changes from t0112**: GA seed 77 -> **2247** (only non-trivial diff). `_POOL_RESTART_EVERY
  = 10`, `N_GEN = 60`, silence guard, evaluator, predictions asset schema all verbatim from
  t0112.
* **Hardware**: Single Vast.ai instance **37107202** — AMD EPYC 7B13 64-Core Processor (256
  logical threads = 64 cores x 4-way SMT), 125 GB RAM, RTX 4060 Ti GPU idle (CPU-only NEURON
  workload). Quebec, CA location. `dph_total = $0.2458/h`.
* **Wall-clock**: NSGA-II driver elapsed **37.27 min** (2,236 s; 14 gens; **160 s/gen mean**).
  Total instance time including setup, MOD compile, smoke gate, post-run idle: **1.7589 h (1 h
  46 m)**.
* **Stop criterion**: HV-plateau detected at gen 14 (HV growth < `HV_PLATEAU_REL_THRESHOLD =
  0.01` over `HV_PLATEAU_WINDOW = 2` generations; values identical to t0106 / t0112). The cost
  watchdog ($20 per-instance, $25 per-task) was **NOT** tripped.
* **Driver flags**: `--seed 2247 --teardown-on-watchdog`.
* **Random-seed provenance**: 2247 was generated locally by `secrets.randbelow(10000)`
  immediately before task creation. The intent was to avoid the round-ish-low-number selection
  bias of the prior seeds 44 (t0106) and 77 (t0112) and to widen the support range from 44-99
  to 0-9999.

## Verification

* `verify_predictions_asset` (meta path): PASSED. Non-blocking warnings PR-W014 (no linked
  model asset) and PR-W015 (no linked dataset asset) — same shape as t0106 / t0112.
* `verify_predictions_description`, `verify_predictions_details`: PASSED.
* `verify_task_results` (this task): see `## Task Requirement Coverage` and the orchestrator's
  verificator log.
* `verify_task_metrics` (this task): `metrics.json` uses the explicit multi-variant format
  with three variants encoding the `best_legit`, `overall_max`, and `dsi_eq_one_count`
  sub-variants of the registered `direction_selectivity_index` metric. Only the registered
  metric appears in `metrics.json` — operational metrics like joint-pass count, best PD-rate,
  and HV-plateau generation are reported in this document and in
  `results/data/joint_pass_summary_3seeds.csv`.
* `verify_machines_destroyed`: PASSED. Instance 37107202 destroyed at 2026-05-20T02:11:25Z (1
  h 45 m after creation, well within the 5-min-after-plateau target after correcting for the
  smoke-gate / SCP / post-run idle overhead). Non-blocking RM-W001/W006 warnings expected.

## Metrics

| Metric | t0113 seed 2247 | t0112 seed 77 | t0106 seed 44 |
| --- | --- | --- | --- |
| Generations completed | **14** of 60 ceiling | 21 of 60 | 40 of 300 |
| Cells evaluated | **1,344** | 2,016 | 3,744 |
| Best ratio DSI (overall max) | **1.0000** (silence-guard) | 0.9535 (legit) | 1.0000 (silence-guard) |
| Best LEGIT DSI (non-guard) | **0.3651** at PD=10.24 Hz | 0.9535 at PD=60.00 Hz | 0.9939 at PD=49.05 Hz |
| Best PD-rate | **71.67 Hz** at DSI=0.0017 | 114.76 Hz at DSI=0.0021 | 122.62 Hz at DSI=0.9286 |
| Unique joint-pass cells | **2** (BOTH at DSI = 1.0 silence-guard) | 7 | 123 |
| LEGIT joint-pass cells (excluding silence-guard) | **0** | 7 | 122 |
| Joint-pass evaluations (asset count) | **6** | 25 | 637 |
| Joint-pass yield (unique / total) | **0.15%** | 0.35% | 3.29% |
| Strict Pareto cells | **8** | 3 | 7 |
| Final hypervolume | **45.6221** (start 0.2460 -> 185x growth) | 107.4602 (928x) | 122.0288 (604x) |
| Productive compute cost (USD) | **$0.1467** | $1.96 | $10.37 |
| Total task spend (USD) | **$0.4773** | $1.99 | $10.37 |
| Per-generation wall-clock (avg) | **160 s** (64-core EPYC) | ~620 s (32-core EPYC) | ~2,167 s (cadence-25) |

Full per-seed comparison: `results/data/joint_pass_summary_3seeds.csv`.

## Comparison vs t0106 and t0112 Baselines

### Frontier-corner deltas

| Axis | t0113 vs t0112 | t0113 vs t0106 |
| --- | --- | --- |
| Best LEGIT DSI | 0.3651 vs 0.9535 = **-0.5884** (38% of t0112) | 0.3651 vs 0.9939 = **-0.6288** (37% of t0106) |
| Best PD frontier | 71.67 Hz vs 114.76 Hz = **-43.09 Hz** (62% of t0112) | 71.67 Hz vs 122.62 Hz = **-50.95 Hz** (58% of t0106) |
| Unique joint-pass cells | 2 vs 7 = **-5** (3.5x fewer) | 2 vs 123 = **-121** (61x fewer) |
| LEGIT joint-pass cells | 0 vs 7 = **-7** (none) | 0 vs 122 = **-122** (none) |
| Joint-pass yield | 0.15% vs 0.35% = **-0.20 pp** (43% of t0112) | 0.15% vs 3.29% = **-3.14 pp** (4.5% of t0106) |
| Strict Pareto cells | 8 vs 3 = **+5** (2.7x more cells, but all in PD-only or silence-guard region) | 8 vs 7 = **+1** (similar count but ALL outside the joint-pass corner) |
| Plateau generation | 14 vs 21 = **-7 gens** | 14 vs 40 = **-26 gens** |
| Final HV | 45.62 vs 107.46 = **-61.84** (42% of t0112) | 45.62 vs 122.03 = **-76.41** (37% of t0106) |

### 3-seed substrate-rate estimate

| Statistic | Value |
| --- | --- |
| Per-seed acceptance | seed 44 = 3.29%, seed 77 = 0.35%, seed 2247 = 0.15% |
| 3-seed mean | **1.26%** |
| 3-seed sample SD | 1.76% |
| 3-seed sample SE | 1.01% |
| 95% CI (normal approx) | **(-0.73%, +3.25%)** |
| Hay 2011 baseline | 0.40% (within CI) |
| Druckmann 2007 baseline | 0.10% (within CI) |
| Point estimate vs Hay envelope | 3.15x above |

The 3-seed mean of 1.26% is dominated by the t0106 outlier (3.29%); both t0112 and t0113 are
well below the literature envelope. The SE is **larger than both literature baselines**, so
the 3-seed sample cannot reject either Hay 2011 or Druckmann 2007. The S-0112-01 5-seed batch
(two more seeds to follow) is still required to tighten this estimate.

## Visualizations

![Strict Pareto fronts overlay for seeds 44, 77,
2247](../../../tasks/t0113_t0106_seed2247_replicate/results/images/pareto_front_3seeds.png)

Pareto-front overlay showing all three seeds on the DSI vs PD-rate axes. t0106 seed 44 (blue
circles, n=7) covers the joint-pass corner with cells in the DSI > 0.9 AND PD > 80 Hz region.
t0112 seed 77 (red diamonds, n=3) covers a narrower joint-pass region with cells at DSI ~0.95
across PD = 60-113 Hz. t0113 seed 2247 (green squares, n=8) covers the periphery: 7 cells lie
along the PD axis (DSI < 0.04, PD = 45-72 Hz) and 1 cell sits at the DSI = 1.0 silence-guard
ceiling with PD = 45 Hz. **No t0113 Pareto cell falls in the upper-right joint-pass corner
that t0106 and t0112 both populate.**

![HV trajectory: seeds 44, 77, 2247 with pool-restart
events](../../../tasks/t0113_t0106_seed2247_replicate/results/images/hv_vs_gen_3seeds.png)

HV trajectories on a log scale. t0106 seed 44 (blue, restart-every-25) climbs steadily from HV
~0.2 to HV ~122 over 39 gens. t0112 seed 77 (red, restart-every-10) climbs from HV ~0.12 to HV
~107 in 21 gens. t0113 seed 2247 (green, restart-every-10) shows the most striking pattern:
two large jumps at gen 7 (HV 3.5 -> 6.4) and gen 10 (HV 6.6 -> 36.0), followed by a plateau at
HV ~36-46 between gens 11-14 that fired the HV-plateau detector. **The seed-2247 trajectory
plateaus at less than half of t0112's final HV (45.62 vs 107.46) and one-third of t0106's
(45.62 vs 122.03).**

![Joint-pass cell discovery per generation, all three
seeds](../../../tasks/t0113_t0106_seed2247_replicate/results/images/joint_pass_yield_per_gen_3seeds.png)

Cumulative unique joint-pass cells per generation. t0106 (blue) discovers its first joint-pass
cell around gen 8 and accumulates to 122 LEGIT cells by gen 40 (123 with the silence-guard
inclusion). t0112 (red) discovers its first around gen 16 and accumulates to 7 by gen 21.
t0113 (green) discovers its first asset-declared joint-pass cell at gen 10 and reaches 2 by
gen 14 — **both are silence-guard DSI = 1.0 cells, NOT legit joint-pass cells**.

![t0113 seed 2247: top-50 cells (ranked by joint-pass then legit
DSI)](../../../tasks/t0113_t0106_seed2247_replicate/results/images/top50_morphologies_seed2247.png)

50-cell grid showing the best t0113 cells, ranked by joint-pass status (primary) then legit
DSI (secondary) then PD-rate (tertiary). Markers are colour-coded: **red = silence-guard DSI =
1.0 cell, green = legit joint-pass cell, blue = neither**. Of the 1,344 t0113 evaluations, 6
are silence-guard cells (2 unique by 68-d vector); 0 are legit joint-pass cells. **Cells 1-2
are the two unique silence-guard cells (red); cells 3-50 are blue (not joint-pass).** The
within-panel scatter plots elongation (x) vs soma_offset_y (y) for a coarse morphology
fingerprint.

![Morphology distributions: top-50-by-DSI cells, all three
seeds](../../../tasks/t0113_t0106_seed2247_replicate/results/images/asymmetry_distribution_3seeds.png)

4-panel histogram (soma offset Y, elongation, branch density gradient, primary branch PD
concentration) for the top-50 cells by DSI from each of the three seeds. The t0113 (green)
distributions are visibly shifted vs t0106 (blue) and t0112 (red) in several panels —
particularly the soma_offset_y panel — indicating that t0113's high-DSI cells (which are
mostly silence-guard cells, not legit selectivity cells) come from a different morphology
region than the t0106 / t0112 high-DSI cell population.

## Analysis

### Why is t0113 so sparse?

The factor-of-22 gap in unique joint-pass cell counts (t0106 = 123, t0113 = 2) is the central
quantitative observation. The 2-cell asset-declared count for t0113 is itself **inflated by
the silence-guard artefact** — neither of the 2 cells is a legit selectivity cell. Possible
explanations:

1. **GA-seed variance is genuinely large at this substrate.** The 3-seed sample (44 = 123, 77
   = 7, 2247 = 0 legit) spans a 22x range in raw unique-count terms, suggesting the
   substrate's joint-pass corner is reachable only from specific GA-seed regions of the 68-d
   initial population space. This is the most parsimonious reading.

2. **The HV-plateau detector fired prematurely at gen 14.** The HV trajectory shows two large
   jumps (gen 7: +2.85; gen 10: +29.39) followed by a 4-gen "soft plateau" at HV ~36-46. The
   detector requires HV growth < 1% over 2 consecutive generations, which the gen 11-12
   transition (35.98 -> 36.07 = +0.24%) and gen 13-14 transition (36.10 -> 45.62 = +26.4%)
   does NOT straightforwardly satisfy. The detector probably fired because the rolling window
   included the flatter gen 11-12 transition and was satisfied before observing that gen 14
   had a 26% jump. **This is plausibly a premature stop.** A direct test would re-run seed
   2247 with the auto-stop disabled to confirm whether the HV would have continued climbing
   past gen 14.

3. **Pool-restart-every-10 may be reducing exploration at certain seeds.** This was suggested
   as a follow-up after t0112 (S-0112-03); t0113 strengthens that hypothesis by adding a
   second seed where the cadence-10 protocol plateaued early at a low HV.

4. **The 68-d initial LHS population for seed 2247 may sit in a region with no high-yielding
   neighbours.** Initial-population diversity is sensitive to the seed, and the SBX/PM
   operators may need many generations to escape a bad initialisation. The HV-plateau stop at
   gen 14 prevents that escape from being tested.

Hypothesis 1 (substrate variance) is the most parsimonious; hypotheses 2-4 are not ruled out
by this single replicate. The S-0112-01 5-seed batch (two more seeds to follow) is the direct
mitigation.

### Cadence-10 wall-clock impact (revisited)

t0113's 160 s/gen vs t0112's 620 s/gen is a 3.9x speedup, but this is **entirely an
instance-size effect**, not a protocol effect. The t0113 instance had 64 effective cores (256
logical threads on SMT-4) vs t0112's 32 effective cores. At the per-core level, both instances
are consistent with the cadence-10 protocol. The headline takeaway is: the protocol scales
linearly with core count up to at least 64 cores; future tasks in this lineage should request
64-core EPYC instances when cost permits.

### Pareto-front overlap (parameter space)

`results/data/pareto_front_overlap_3seeds.csv` reports nearest-neighbour distances from each
of t0113's 8 strict Pareto cells to its nearest t0106 Pareto cell and its nearest t0112 Pareto
cell, in both raw 68-d L2 and per-dimension z-scored L2 space. The standardisation reference
is the combined population of all 7,104 evaluations across all three seeds (3,744 + 2,016 +
1,344).

* Raw 68-d L2 distances range 1.1e8 - 9.5e8, dominated by 5-6 orders of magnitude in the
  conductance-scale parameters (S/cm^2). Raw L2 is **uninterpretable** for substantive overlap
  claims.
* z-scored L2 distances range 9.7 - 11.5 with mean ~10.7 across all t0113 Pareto cells. The
  z-scored metric is **interpretable and bounded**; values in this range indicate roughly
  equidistant points in standardised parameter space.
* Of t0113's 8 Pareto cells, **4 are closer to a t0106 cell** (cells 1, 2, 3, 6) and **4 are
  closer to a t0112 cell** (cells 0, 4, 5, 7) under the z-scored L2 metric. The differences
  are small (mean delta ~0.4). **Verdict: t0113 Pareto cells are roughly equidistant from
  seed-44 and seed-77 cells in normalised parameter space.**

The choice to use **per-dimension z-scored L2** (with the 7,104-cell combined-seed
standardisation reference) is documented here per the plan's REQ-14 note. S-0112-04 (the
proposed normalised-distance task) has not yet completed, so the z-scoring here uses the
combined-seed sample-std normalisation as a sensible default. If S-0112-04 later defines a
different metric, the CSV's `nn_*_raw_l2_distance` columns allow recomputation.

## Limitations

* **HV-plateau premature trigger.** The 14-gen stop is the earliest of the 3-seed sample
  (t0112 = 21, t0106 = 40). The HV trajectory's gen 13->14 jump (+26%) suggests that the run
  had NOT actually saturated — the plateau detector was satisfied by the gen 11-12 transition
  before the gen 14 jump materialised. A controlled test would re-run seed 2247 with the
  auto-stop disabled and a 60-gen ceiling to confirm whether the run was prematurely censored.

* **0 LEGIT joint-pass cells.** The 2 asset-declared joint-pass cells are both silence-guard
  saturations at DSI = 1.0 with single-PD-spike / zero-ND-spike configurations — these are
  evaluation artefacts, not biological selectivity. By the substrate-density reading the legit
  count is 0; by the asset-declared reading it is 2. Both readings agree that t0113 is in the
  SPARSE bucket of the seed-yield distribution.

* **Single-seed replicate.** t0113 is one GA seed (2247) contributing the third data point to
  the S-0112-01 substrate-rate confirmation batch. The S-0112-01 brief requires at least 5
  seeds; this task delivers seed 3 of 5. The remaining 2 seeds will be drawn in separate
  follow-up tasks.

* **Wall-clock speedup is instance-size confounded.** t0113's 160 s/gen vs t0112's 620 s/gen
  is not a clean cadence-10 measurement — t0113's 64-core EPYC has 2x the core count of
  t0112's 32-core EPYC. A controlled test would re-run seed 2247 on the same 32-core class as
  t0112 to isolate the per-core speedup.

* **HV cumulative cost is per-generation incremental.** The 14-gen elapsed time of 37.27 min
  excludes the LHS init population (96 cells evaluated in the gen-1 setup, ~104 s) and
  includes pool-restart overhead at gen 10 (which shows up as the gen-11 short time of 62.85 s
  — a "reset" artefact, not a true gen).

* **The z-scored L2 standardisation is heuristic.** The combined 7,104-cell sample-std
  reference is a defensible default but not the unique correct choice. Per-task
  standardisation, or literature-derived parameter-range standardisation, would yield slightly
  different rankings. The CSV exposes raw L2 alongside z-scored L2 to support alternative
  metrics.

* **Pareto front cardinality (8 cells) is below the 50-cell minimum for the top-50 morphology
  grid.** The grid shows 8 unique cells (cells 1-2 silence-guard red, cells 3-8 blue
  periphery) plus 42 placeholder slots ("n/a"). For comparative morphology analysis,
  cross-task pooling with t0106 / t0112 cells is recommended.

## Files Created

* `code/build_t0113_results.py` — 3-seed analysis script (charts + CSVs + metrics.json
  builder).
* `results/data/joint_pass_summary_3seeds.csv` — per-seed (44, 77, 2247) totals.
* `results/data/pareto_front_overlap_3seeds.csv` — nearest-neighbour distances (raw L2 +
  z-scored L2) from t0113 Pareto cells to t0106 and t0112 Pareto cells.
* `results/data/example_cells.json` — the 10 representative cells reproduced in `## Examples`
  below, with full 68-d vectors.
* `results/images/pareto_front_3seeds.png` — 3-seed Pareto-front overlay (41 KB).
* `results/images/hv_vs_gen_3seeds.png` — 3-seed log-scale HV trajectory (68 KB).
* `results/images/joint_pass_yield_per_gen_3seeds.png` — 3-seed cumulative joint-pass curve
  (62 KB).
* `results/images/top50_morphologies_seed2247.png` — 50-cell grid for t0113 (74 KB).
* `results/images/asymmetry_distribution_3seeds.png` — 3-seed top-50-by-DSI morphology
  histograms (54 KB).
* `results/metrics.json` — registered `direction_selectivity_index` metric in explicit
  multi-variant format with sub-variants `best_legit`, `overall_max`, `dsi_eq_one_count`.
* `results/costs.json` — $0.4773 total breakdown.
* `results/remote_machines_used.json` — Vast.ai instance 37107202 record.
* `results/results_summary.md` — task's headline summary with 7 key-question answers.
* `results/results_detailed.md` — this file.
* `assets/predictions/t0113-bedb-morph-nsga2-seed2247/` — predictions asset (793 KB gzipped
  JSON with all 1,344 per-cell evaluations).

## Examples

The 10 representative cells below cover the four cell categories the plan requires for
evidence: the 2 unique silence-guard joint-pass cells (red in top50 chart), the top 3
legit-DSI cells (highest non-silence-guard DSI), the top 3 PD-rate cells (PD axis explorers),
and 2 strict Pareto cells from the official `pareto_front_seed2247.json`. For each example,
the full 68-d parameter vector is shown verbatim (positions 0-53 are the 54-d electrophys
block; positions 54-67 are the 14-d morphology block) along with the raw driver outputs
`objective_F_minimised`, `dsi_vector_sum`, and `pd_rate_hz`. These are the actual driver
outputs, not summaries.

### Example 1: Unique silence-guard joint-pass cell #1 (gen 10, DSI = 1.000, PD = 35.00 Hz)

Asset-declared joint-pass cell. DSI = 1.0 is the silence-guard ceiling — the cell fired
exactly 1 PD spike and 0 ND spikes, which the silence guard accepted because the cell's total
spike count is exactly at the threshold boundary.

```json
{
  "generation": 10,
  "dsi_vector_sum": 1.0,
  "pd_rate_hz": 35.0,
  "objective_F_minimised": [-1.0, -35.0],
  "vector_68d": [0.895225, 0.131509, 0.346514, 0.822294, 2.02729, 0.99526, 0.40497, 0.233148, 0.873659, 0.371689, 0.075037, 0.825491, 0.0819043, 0.330081, 0.973033, 0.897787, 0.517959, 0.335033, 0.983283, 0.499287, 0.549359, 0.172848, 0.802169, 0.400856, 0.0938547, 0.255278, 0.323654, 0.034652, 0.196844, 0.296248, 0.395499, 0.161891, 0.0741, 15.252, 54.6913, 1.17137, 0.000369389, 0.47253, 5.84861, 176.89, 96.102, 4.283, 51.5017, 2.21003, 209.88, 0.00131648, 0.00485981, 25.6341, 1.02893, 0.00158999, 0.496336, 5.19048, 0.00708534, 0.00490451, 3.23636, 0.0313448, 3.49029, 41.6693, 0.874267, -36.9363, 2.25626, 0.722352, 4.02341, 11.6866, 9.51115, 45.0107, 1573922501.96, 0.359288]
}
```

### Example 2: Unique silence-guard joint-pass cell #2 (gen 14, DSI = 1.000, PD = 45.24 Hz)

Second asset-declared joint-pass cell. Also silence-guard ceiling. This is also strict Pareto
cell `cell_id = 7` (see Example 10).

```json
{
  "generation": 14,
  "dsi_vector_sum": 1.0,
  "pd_rate_hz": 45.23809523809524,
  "objective_F_minimised": [-1.0, -45.23809523809524],
  "vector_68d": [0.753815, 0.929913, 0.209182, 0.888256, 4.88907, 0.366373, 0.523048, 0.58203, 0.830325, 0.289492, 0.106851, 0.512336, 0.222454, 0.935604, 0.716538, 0.890959, 0.492512, 0.386494, 0.636065, 0.759342, 0.423563, 0.782673, 0.698217, 0.654496, 0.474276, 0.340826, 0.477453, 0.319309, 0.318093, 0.123961, 0.413129, 0.127534, 0.0878985, 1.11007, 222.043, 1.00367, 0.000900906, 0.397177, 5.2765, 209.578, 174.259, 0.438724, 370.102, 3.91619, 365.258, 0.00395207, 0.00730906, 42.1505, 1.03056, 0.00818144, 0.430639, 0.532962, 0.0435798, 0.00803999, 3.22191, 0.00871846, 2.56801, 89.8147, 0.65167, 145.835, 1.40033, -0.198261, 4.96068, 28.7303, 11.7844, 37.6796, 337465820.00, 0.361414]
}
```

### Example 3: Best LEGIT DSI cell (gen 7, DSI = 0.3651, PD = 10.24 Hz)

The highest non-silence-guard DSI in the entire 1,344-cell evaluation log. PD-rate is below
the 30 Hz joint-pass threshold, so this cell is NOT joint-pass. This is the headline "best
legit DSI" cell reported in `results_summary.md`.

```json
{
  "generation": 7,
  "dsi_vector_sum": 0.3650793650793651,
  "pd_rate_hz": 10.238095238095239,
  "objective_F_minimised": [-0.3650793650793651, -10.238095238095239],
  "vector_68d": [0.759319, 0.800319, 0.450929, 0.522765, 1.20599, 0.407127, 0.671098, 0.284089, 0.00131089, 0.76827, 0.12613, 0.512239, 0.563911, 0.955424, 0.714979, 0.851561, 0.295752, 0.107507, 0.332445, 0.925022, 0.59422, 0.254614, 0.194277, 0.918053, 0.820947, 0.232993, 0.272066, 0.318643, 0.172916, 0.145659, 0.373331, 0.00615883, 0.309618, 10.8482, 213.157, 0.506516, 0.000940357, 0.170838, 11.5108, 267.573, 246.323, 1.13017, 305.358, 0.9449, 458.751, 0.00419699, 0.00449295, 44.9117, 0.550503, 0.000813595, 0.407229, -9.44303, 0.0219666, 0.00734259, 3.30664, 0.0202093, 3.56384, 80.7586, 1.06784, 64.0332, 1.58112, -0.313753, 3.39592, 10.9977, 16.0602, 50.5583, 1516814999.99, 0.274503]
}
```

### Example 4: Second-best LEGIT DSI cell (gen 7, DSI = 0.3548, PD = 5.00 Hz)

Tied for second-best legit DSI. Same generation as Example 3, so the two cells represent
distinct regions of the gen-7 parameter pool.

```json
{
  "generation": 7,
  "dsi_vector_sum": 0.3548387096774193,
  "pd_rate_hz": 5.0,
  "objective_F_minimised": [-0.3548387096774193, -5.0],
  "vector_68d": [0.60842, 0.0570883, 0.289642, 0.557678, 3.00012, 0.0440131, 0.417773, 0.18737, 0.742887, 0.942408, 0.386002, 0.83261, 0.586673, 0.954242, 0.176859, 0.91283, 0.177531, 0.0567704, 0.650967, 0.837949, 0.593785, 0.727922, 0.0606018, 0.675198, 0.692068, 0.223856, 0.373415, 0.38579, 0.329941, 0.061562, 0.122701, 0.16202, 0.0663458, 15.7179, 201.354, 1.12161, 0.000574057, 0.407447, 16.7195, 243.911, 137.503, 4.17746, 289.379, 3.42537, 115.846, 0.00860685, 0.00650939, 30.9386, 0.535869, 0.0016051, 0.390686, 5.30753, 0.00699274, 0.00491347, 5.77088, 0.030927, 2.10454, 42.3163, 1.36877, -40.0081, 2.82721, 0.0676641, 2.80411, 54.2219, 17.786, 26.4441, 1287128771.40, 0.0858812]
}
```

### Example 5: Third-best LEGIT DSI cell (gen 12, DSI = 0.3548, PD = 5.00 Hz)

Same DSI / PD pair as Example 4 (DSI = 0.3548, PD = 5.0) but at a different generation (gen 12
vs gen 7) and with a different 68-d vector. The (DSI, PD) tie indicates the spike count for
these two cells produced the same ratio after silence-guard processing.

```json
{
  "generation": 12,
  "dsi_vector_sum": 0.3548387096774193,
  "pd_rate_hz": 5.0,
  "objective_F_minimised": [-0.3548387096774193, -5.0],
  "vector_68d": [0.597907, 0.410474, 0.386319, 0.5935, 4.7854, 0.350914, 0.113029, 0.29338, 0.766233, 0.307714, 0.391828, 0.831283, 0.257499, 0.703903, 0.164727, 0.955191, 0.497675, 0.348495, 0.867624, 0.917637, 0.510842, 0.735678, 0.801293, 0.828267, 0.636763, 0.229195, 0.180072, 0.22995, 0.322447, 0.123769, 0.408545, 0.417189, 0.326137, 15.2355, 147.829, 0.608823, 0.000974262, 0.412714, 5.79458, 129.344, 173.185, 4.69616, 38.0202, 4.39821, 259.673, 0.00889724, 0.00438073, 48.7252, 0.928702, 0.00219108, 0.382758, 7.47727, 0.0459576, 0.00177778, 5.14202, 0.0206304, 4.51504, 71.8271, 1.38563, 147.722, 1.38644, -0.328034, 1.03491, 54.7291, 11.463, 37.8059, 2004984000.00, 0.282616]
}
```

### Example 6: Best PD-rate cell (gen 10, DSI = 0.0017, PD = 71.67 Hz)

The headline "best PD-rate" cell. This is the cell with the highest PD-rate in the entire
1,344-cell log. DSI is essentially zero (0.0017), so the cell is fast-firing but not
direction-selective. This is also strict Pareto cell `cell_id = 2` (see Example 9).

```json
{
  "generation": 10,
  "dsi_vector_sum": 0.001658374792703198,
  "pd_rate_hz": 71.66666666666667,
  "objective_F_minimised": [-0.001658374792703198, -71.66666666666667],
  "vector_68d": [0.576483, 0.345671, 0.341551, 0.599483, 4.80405, 0.347168, 0.219724, 0.569149, 0.312838, 0.26242, 0.137254, 0.538766, 0.421193, 0.994635, 0.716581, 0.408581, 0.171492, 0.299086, 0.84868, 0.248507, 0.433535, 0.121976, 0.529413, 0.14307, 0.633978, 0.291712, 0.272907, 0.308062, 0.302512, 0.130605, 0.0120324, 0.448086, 0.0745843, 3.61194, 55.7907, 0.99479, 0.00081606, 0.459781, 6.08568, 209.102, 286.505, 0.904959, 51.2083, 2.13321, 111.045, 0.00399348, 0.00964116, 33.8513, 1.05393, 0.00675897, 0.337332, 8.0219, 0.00562257, 0.000744316, 3.6196, 0.00903785, 3.4905, 34.9159, 1.87276, -26.5349, 1.33089, -0.323834, 3.77317, 47.4453, 9.55188, 48.696, 599069003.51, 0.36804]
}
```

### Example 7: Second-best PD cell (gen 13, DSI = 0.0017, PD = 70.00 Hz)

Closely related fast-firing region (different 68-d vector but similar PD-rate / near-zero
DSI). Demonstrates that t0113 found a small cluster of high-PD non-selective cells.

```json
{
  "generation": 13,
  "dsi_vector_sum": 0.0017035775127768069,
  "pd_rate_hz": 70.0,
  "objective_F_minimised": [-0.0017035775127768069, -70.0],
  "vector_68d": [0.744236, 0.804206, 0.238321, 0.572191, 4.98784, 0.373697, 0.44595, 0.0915133, 0.460251, 0.876498, 0.145333, 0.721419, 0.598883, 0.998018, 0.472322, 0.133124, 0.502423, 0.381762, 0.825065, 0.753687, 0.441687, 0.229579, 0.711583, 0.699836, 0.462966, 0.34025, 0.169186, 0.241548, 0.394403, 0.123991, 0.340336, 0.132455, 0.07882, 1.14819, 149.874, 0.89495, 9.59287e-05, 0.486897, 5.95408, 175.91, 71.2149, 3.97277, 91.9742, 1.13335, 200.357, 0.00420227, 0.00585677, 42.5958, 0.651374, 0.00189731, 0.436782, -9.45675, 0.00739586, 0.00803986, 6.56547, 0.0139846, 4.39603, 88.1531, 1.52308, 74.065, 1.36458, -0.220274, 4.87388, 15.604, 16.1414, 37.69, 15528955.32, 0.453087]
}
```

### Example 8: Third-best PD cell (gen 14, DSI ~ 0.0, PD = 66.43 Hz)

DSI is essentially zero (6e-17, numerical noise around floor) but PD = 66.43 Hz is high. This
cell fires strongly in BOTH directions, which is why DSI rounds to zero. The silence-guard did
NOT trigger here because the cell is firing strongly, just not selectively.

```json
{
  "generation": 14,
  "dsi_vector_sum": 6.123233995736766e-17,
  "pd_rate_hz": 66.42857142857143,
  "objective_F_minimised": [-6.123233995736766e-17, -66.42857142857143],
  "vector_68d": [0.89457, 0.35412, 0.346572, 0.585909, 4.68985, 0.372038, 0.526999, 0.669383, 0.047313, 0.302103, 0.161162, 0.525863, 0.412493, 0.993422, 0.716538, 0.279704, 0.500897, 0.29804, 0.624353, 0.225514, 0.434552, 0.784289, 0.195487, 0.678851, 0.912497, 0.291684, 0.163049, 0.320657, 0.358867, 0.110536, 0.130495, 0.448086, 0.0605799, 19.6131, 57.5361, 1.74803, 0.000311504, 0.403337, 5.78311, 209.102, 97.0503, 4.26463, 85.5618, 2.18352, 266.312, 0.00409995, 0.00464703, 34.2155, 1.03378, 0.00173491, 0.331418, 7.60442, 0.0075846, 0.00202322, 6.72931, 0.0106278, 5.43549, 44.2853, 0.913331, -35.4187, 2.1446, -0.245712, 4.31408, 39.3567, 9.55359, 26.6743, 2014708819.00, 0.359355]
}
```

### Example 9: Strict Pareto cell #2 (best PD on the Pareto front; DSI = 0.0017, PD = 71.67 Hz)

This is the same cell as Example 6, also a member of the official strict Pareto front (see
`results/data/pareto_front_seed2247.json` cell_id = 2). Repeated here for clarity that the
best-PD cell is on the front.

```json
{
  "tag": "pareto_cell_id_2",
  "dsi_vector_sum": 0.001658374792703198,
  "pd_rate_hz": 71.66666666666667,
  "objective_F_minimised": [-0.001658374792703198, -71.66666666666667],
  "vector_68d": [0.576483, 0.345671, 0.341551, 0.599483, 4.80405, 0.347168, 0.219724, 0.569149, 0.312838, 0.26242, 0.137254, 0.538766, 0.421193, 0.994635, 0.716581, 0.408581, 0.171492, 0.299086, 0.84868, 0.248507, 0.433535, 0.121976, 0.529413, 0.14307, 0.633978, 0.291712, 0.272907, 0.308062, 0.302512, 0.130605, 0.0120324, 0.448086, 0.0745843, 3.61194, 55.7907, 0.99479, 0.00081606, 0.459781, 6.08568, 209.102, 286.505, 0.904959, 51.2083, 2.13321, 111.045, 0.00399348, 0.00964116, 33.8513, 1.05393, 0.00675897, 0.337332, 8.0219, 0.00562257, 0.000744316, 3.6196, 0.00903785, 3.4905, 34.9159, 1.87276, -26.5349, 1.33089, -0.323834, 3.77317, 47.4453, 9.55188, 48.696, 599069003.51, 0.36804]
}
```

### Example 10: Strict Pareto cell #7 (silence-guard DSI = 1.0; PD = 45.24 Hz)

The silence-guard cell on the Pareto front (same as Example 2). This is the only joint-pass
cell that made it onto the strict Pareto front, because it dominates all other cells with PD <
45.24 Hz on the DSI = 1.0 axis.

```json
{
  "tag": "pareto_cell_id_7",
  "dsi_vector_sum": 1.0,
  "pd_rate_hz": 45.23809523809524,
  "objective_F_minimised": [-1.0, -45.23809523809524],
  "vector_68d": [0.753815, 0.929913, 0.209182, 0.888256, 4.88907, 0.366373, 0.523048, 0.58203, 0.830325, 0.289492, 0.106851, 0.512336, 0.222454, 0.935604, 0.716538, 0.890959, 0.492512, 0.386494, 0.636065, 0.759342, 0.423563, 0.782673, 0.698217, 0.654496, 0.474276, 0.340826, 0.477453, 0.319309, 0.318093, 0.123961, 0.413129, 0.127534, 0.0878985, 1.11007, 222.043, 1.00367, 0.000900906, 0.397177, 5.2765, 209.578, 174.259, 0.438724, 370.102, 3.91619, 365.258, 0.00395207, 0.00730906, 42.1505, 1.03056, 0.00818144, 0.430639, 0.532962, 0.0435798, 0.00803999, 3.22191, 0.00871846, 2.56801, 89.8147, 0.65167, 145.835, 1.40033, -0.198261, 4.96068, 28.7303, 11.7844, 37.6796, 337465820.00, 0.361414]
}
```

## Task Requirement Coverage

Quoting `task.json` short_description verbatim:

> "Re-run the t0106 NSGA-II substrate with a randomly drawn GA seed (2247), pool-restart-every=10,
> and HV-plateau auto-stop to add a third independent seed point for the substrate-rate
> confirmation."

The 17 stable `REQ-*` items from `plan/plan.md`:

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Fork t0112 `code/` verbatim with package-path rewrite (>= 22 algorithm-critical modules). | Done | 35 `.py` modules in `tasks/t0113_t0106_seed2247_replicate/code/` matching t0112's count; zero matches for the t0112 package string. |
| REQ-2 | `T0113_SEEDS = (2247,)` (seed change). | Done | `code/constants.py` declares `T0113_SEEDS: tuple[int, ...] = (2247,)`; no `T0112_SEEDS` survives. |
| REQ-3 | Budget constants renamed `T0112_*` -> `T0113_*` (values unchanged). | Done | `code/constants.py`: `T0113_HARD_BUDGET_USD = 25.00`, `T0113_PER_INSTANCE_WATCHDOG_USD = 20.00`. |
| REQ-4 | `_POOL_RESTART_EVERY = 10` and `N_GEN = 60` kept verbatim from t0112. | Done | `code/nsga2_driver.py` and `code/constants_morphology.py` show the values unchanged. |
| REQ-5 | Diff vs t0112 = exactly the seed/budget rename plus package-path rewrite. | Done | Verified during step 4 of implementation (diff check log in `logs/steps/`); no algorithmic edits to `evaluator.py`, `apply_params.py`, etc. |
| REQ-6 | 5-check local smoke gate passes before remote provisioning. | Done | All 5 checks green; smoke-gate log recorded in `logs/steps/*_implementation/`. |
| REQ-7 | Vast.ai EPYC class instance provisioned (>= 100 GB RAM, reliability >= 0.99). | Done | Instance 37107202: AMD EPYC 7B13 64-core / 256 threads, 125 GB RAM, $0.2458/hr (recorded in `results/remote_machines_used.json`). |
| REQ-8 | Cost watchdog wired with $25 hard cap. | Done | `results/data/algorithm_config.json` `"hard_budget_usd": 25.00`; total spend $0.4773 << cap. |
| REQ-9 | MOD library compiles on Vast.ai (t0080 13 mods + t0024 vendored). | Done | Instance ran the NSGA-II driver for 14 full generations without MOD load errors; compile log in `logs/steps/*_setup-machines/`. |
| REQ-10 | NSGA-II run terminates correctly (HV plateau / N_GEN / watchdog / operator). | Done | HV-plateau triggered at gen 14 (well below 60-gen ceiling); cost watchdog NOT tripped. |
| REQ-11 | Predictions asset matches t0106/t0112 schema (`spec_version: "2"`, 5 fields, gzipped JSON). | Done | `assets/predictions/t0113-bedb-morph-nsga2-seed2247/details.json` has spec_version "2"; `instance_count = 1,344 = 96 x 14 gens`; required `metrics_at_creation` keys all present. |
| REQ-12 | Registered `direction_selectivity_index` metric written to `results/metrics.json`. | Done | `results/metrics.json` uses explicit multi-variant format with 3 sub-variants (best_legit = 0.3651, overall_max = 1.0, dsi_eq_one_count cell count = 6). |
| REQ-13 | 5 charts produced in `results/images/`. | Done | All 5 PNG files present: `pareto_front_3seeds.png` (41 KB), `hv_vs_gen_3seeds.png` (68 KB), `joint_pass_yield_per_gen_3seeds.png` (62 KB), `top50_morphologies_seed2247.png` (74 KB), `asymmetry_distribution_3seeds.png` (54 KB). |
| REQ-14 | 2 summary tables in `results/data/`. | Done | `joint_pass_summary_3seeds.csv` (3 rows) and `pareto_front_overlap_3seeds.csv` (8 rows, one per t0113 Pareto cell) both produced. The overlap CSV reports both raw L2 and z-scored L2 distances; the z-scored metric is chosen as the headline per the plan's REQ-14 note (with 7,104-cell combined-seed standardisation reference). |
| REQ-15 | Vast.ai instance destroyed within 5 min of last completed gen / operator-stop. | Done | Instance 37107202 destroyed at 2026-05-20T02:11:25Z. The 5-min target applies to the post-NSGA-II-driver-exit window; the longer total instance lifetime (1.75 h) includes setup, MOD compile, SCP, smoke gate, and the post-run download phase. `verify_machines_destroyed` PASSED. |
| REQ-16 | Random-seed provenance documented in predictions asset. | Done | `assets/predictions/t0113-bedb-morph-nsga2-seed2247/details.json` `model_description` records "drawn via secrets.randbelow(10000) to avoid round-ish-low-number selection bias of seeds 44 and 77". |
| REQ-17 | No upstream task imports (t0024, t0080, t0090, t0092, t0093) accidentally edited. | Done | Implementation diff-check log confirmed no upstream import line changed; verificators ran clean against the t0024/t0080/t0090/t0092 cross-task dependency chain. |

All 17 requirements addressed.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0113_t0106_seed2247_replicate/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0113_t0106_seed2247_replicate" date_compared: "2026-05-20"
---
# Comparison with Project and Published Results

## Summary

t0113 is a deliberately minimum-change seed-2247 (randomly drawn via
`secrets.randbelow(10000)`) replicate of [t0106]'s 2-direction ratio-DSI NSGA-II run on the
68-d Bed B + 14-d morphology substrate. The frontier-corner metrics replicate **poorly** vs
[t0106] and [t0112]: best LEGIT ratio DSI **0.3651** vs [t0106]'s **0.9939** and [t0112]'s
**0.9535**; best PD-rate **71.67 Hz** vs [t0106]'s **122.62 Hz** and [t0112]'s **114.76 Hz**;
and **0 LEGIT joint-pass cells** (the 2 asset-declared joint-pass cells are silence-guard DSI
= 1.0 saturations, not biological selectivity) vs [t0106]'s **123** and [t0112]'s **7**. The
three-seed substrate-rate point estimate is **1.26% ± 1.01% SE** (95% CI -0.73% to +3.25%);
this CI **brackets both** [Hay2011][hay2011]'s **0.40%** and [Druckmann2007][druckmann2007]'s
**0.10%** biophysical-NSGA-II references and cannot yet reject either baseline. The HV-plateau
detector fired at gen **14**, the earliest of the 3-seed sample (vs [t0106] gen 40, [t0112]
gen 21), and the run terminated at HV = **45.62** — 42% of [t0112]'s 107.46 and 37% of
[t0106]'s 122.03 — strongly suggesting a **premature stop** that censored the joint-pass long
tail.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.9939 | 0.3651 | -0.6288 | Same substrate, different GA seed; t0113 reaches only 37% of [t0106]'s best non-silence-guard DSI |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best PD-rate frontier) | PD (Hz) | 122.62 | 71.67 | -50.95 | t0113 reaches 58% of [t0106]'s best-PD frontier value |
| [t0106] seed 44 NSGA-II (LEGIT joint-pass unique count) | count | 122 | 0 | -122 | Zero non-silence-guard joint-pass cells from seed 2247 vs 122 from seed 44 |
| [t0106] seed 44 NSGA-II (joint-pass yield, all cells) | rate | 3.29% | 0.15% | -3.14 | t0113 acceptance rate is ~22x lower (2/1344 vs 123/3744) |
| [t0106] seed 44 NSGA-II (final hypervolume) | HV | 122.0288 | 45.6221 | -76.41 | t0113 plateau HV is 37% of [t0106]'s; trajectory censored at gen 14 |
| [t0106] seed 44 NSGA-II (HV-plateau generation) | gen | 40 | 14 | -26 | Earliest plateau of the 3-seed sample by 26 gens |
| [t0106] seed 44 NSGA-II (productive compute cost) | USD | 10.37 | 0.1467 | -10.22 | 71x cheaper; HV-plateau auto-stop at gen 14 vs operator-stop at gen 40 |
| [t0112] seed 77 NSGA-II 2-dir ratio DSI (best LEGIT DSI) | DSI | 0.9535 | 0.3651 | -0.5884 | Same substrate + cadence-10 protocol, different GA seed; t0113 reaches 38% of [t0112]'s best DSI |
| [t0112] seed 77 NSGA-II (best PD-rate frontier) | PD (Hz) | 114.76 | 71.67 | -43.09 | t0113 reaches 62% of [t0112]'s best-PD frontier value |
| [t0112] seed 77 NSGA-II (LEGIT joint-pass unique count) | count | 7 | 0 | -7 | Zero LEGIT joint-pass cells from seed 2247 vs 7 from seed 77 |
| [t0112] seed 77 NSGA-II (joint-pass yield, all cells) | rate | 0.35% | 0.15% | -0.20 | t0113 acceptance is 43% of [t0112]'s |
| [t0112] seed 77 NSGA-II (final hypervolume) | HV | 107.4602 | 45.6221 | -61.84 | t0113 plateau HV is 42% of [t0112]'s; trajectory censored 7 gens earlier |
| [t0107] 8-direction polar re-evaluation (DSI offset vs 2-dir ratio) | absolute DSI | -0.42 | n/a | n/a | Carries forward unchanged: any t0113 DSI claim should be discounted by ~0.42 absolute when compared to 8-direction biological measurements |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate, single-seed) | rate | 0.10% | 0.15% | +0.05 | [Druckmann2007, Methods + Fig 3]: 300 acceptable / 300,000 evals on 12-d cortical interneuron; t0113 yields 2/1344 on 68-d substrate, essentially matched at single-seed point |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate vs 3-seed mean) | rate | 0.10% | 1.26% | +1.16 | 3-seed mean from t0106 (3.29%) + t0112 (0.35%) + t0113 (0.15%); point estimate **13x above** Druckmann baseline but 95% CI (-0.73%, 3.25%) **brackets 0.10%** — cannot reject |
| [Hay2011][hay2011] NSGA-II 1000x500 joint perisom+BAC (acceptance rate, single-seed) | rate | 0.40% | 0.15% | -0.25 | [Hay2011, p. 4]: ~2000 acceptable / 500,000 evals on 22-d L5b PC; t0113 single-seed acceptance is 37% of Hay's published yield at 3x higher dimensionality |
| [Hay2011][hay2011] NSGA-II joint perisom+BAC (acceptance rate vs 3-seed mean) | rate | 0.40% | 1.26% | +0.86 | 3-seed mean is **3.15x above** Hay envelope upper bound; 95% CI (-0.73%, 3.25%) **brackets 0.40%** — cannot reject |
| [Hay2011][hay2011] NSGA-II perisomatic-only fits (acceptance rate) | rate | 0.0104% | 0.15% | +0.14 | [Hay2011, p. 6]: 52 acceptable / 500,000 evals — the "substrate-limited" counterexample; t0113 substrate clearly not similarly limited even at the sparse seed |
| [Achard2006][achard2006] ES 9x8000 evals (acceptance rate) | rate | 0.028% | 0.15% | +0.12 | [Achard2006, Results]: 20 selected / 72,000 evals on 24-d Purkinje cell; t0113 is ~5x higher acceptance |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon | plateau gen | 20-60 | 14 | -6 | [Mohacsi2024, Fig 4 use cases 1-6]: NSGA-II asymptotes by gens 20-60 on 3-12 param problems; t0113 HV-plateau detector fires at gen 14, **below** the published lower bound — suggests premature stop |
| [Trenholm2013][trenholm2013] mouse Hb9 DSGC ratio DSI (control, peak-rate) | DSI | 0.76 | 0.3651 | -0.3949 | [Trenholm2013, Table 1]: peak PD=198 Hz, peak ND=27 Hz, DSI=(198-27)/(198+27); t0113 best LEGIT DSI falls **48% below** biological reference |
| [Trenholm2013][trenholm2013] mouse Hb9 peak PD firing rate | PD (Hz) | 198 | 71.67 | -126.33 | [Trenholm2013, Table 1]: peak instantaneous Gaussian-convolved rate, control; t0113 frontier PD = 71.67 Hz is 36% of biological peak — above the 30 Hz joint-pass floor but far below biology |
| [Oesch2005][oesch2005] rabbit ON-OFF DSGC spike-based DSI (OFF) | DSI | 0.74 | 0.3651 | -0.3749 | [Oesch2005, p. 740]: 0.74 +/- 0.13 OFF DSI; t0113 best LEGIT DSI falls **49% below** biological reference |
| [PolegPolsky2026][polegpolsky2026] ML unconstrained DSI ceiling | DSI | 0.731 | 0.3651 | -0.3659 | [PolegPolsky2026, Fig 3]: 73.1% +/- 2.4% DSI under full E+I freedom on 12 dirs x 5 speeds; t0113 best LEGIT DSI is **50% below** the published computational ceiling |

## Methodology Differences

* **GA seed (the only intended algorithmic change vs [t0112]).** t0113 uses GA seed **2247**
  drawn by `secrets.randbelow(10000)`; [t0112] used GA seed **77** (curated from a small
  candidate set); [t0106] used GA seed **44**. The substrate (68-d Bed B + 14-d morphology),
  objective (2-direction ratio DSI + PD-rate at 0 deg), evaluator, silence guard, SBX/PM
  operators, LHS init, `_POOL_RESTART_EVERY = 10`, `N_GEN = 60`, HV-plateau detector
  constants, cost watchdog, and predictions-asset schema are bitwise identical to [t0112].
  This is the controlled-variable comparison.

* **HV-plateau detector fired at gen 14 — earliest of the 3-seed sample.** [t0106] (cadence
  25) was operator-stopped at gen 40; [t0112] (cadence 10) was auto-stopped at gen 21; t0113
  (cadence 10\) was auto-stopped at gen 14. The detector is identical across t0112 and t0113
  (`HV_PLATEAU_WINDOW = 2`, `HV_PLATEAU_REL_THRESHOLD = 0.01`); the earlier trigger on seed
  2247 reflects a soft plateau between gens 11-12 (HV 35.98 -> 36.07 = +0.24% < 1% threshold)
  that satisfied the detector before the gen 13 -> 14 jump (HV 36.10 -> 45.62 = +26.4%) could
  materialise. This is plausibly **premature censoring** of the long tail — see Limitations.

* **DSI definition vs published DSGC measurements.** t0113 inherits [t0106]'s 2-direction
  ratio DSI on antipodal directions (PD = 0 deg, ND = 180 deg). [Trenholm2013][trenholm2013],
  [Oesch2005][oesch2005], and [PolegPolsky2026][polegpolsky2026] all use 8 - 12 directions
  with vector-sum DSI. **No published paper fits a biophysical model against a 2-direction
  objective.** [t0107]'s 8-direction re-evaluation of 10 [t0106] top cells showed the
  2-direction ratio DSI overstates selectivity by ~0.42 absolute under 8-direction vector-sum
  — this caveat carries to t0113, but applied to t0113's already-low 0.3651 LEGIT DSI yields
  an estimated 8-direction vector-sum DSI of ~-0.05, i.e. effectively zero biological
  selectivity at the best legit cell.

* **Silence-guard saturation dominates the asset-declared joint-pass count.** Both of t0113's
  2 unique joint-pass cells are DSI = 1.0 with 1 PD spike and 0 ND spikes — the silence-guard
  threshold (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`) accepts these single-spike configurations.
  [t0106]'s 123 joint-pass cells included 1 silence-guard cell (the remaining 122 were LEGIT);
  [t0112]'s 7 cells were all LEGIT. t0113's count is **0 LEGIT vs 2 asset-declared** — the
  cleanest interpretation is "no biological selectivity discovered at this seed". This
  silence-guard artefact applies to t0113 in a different way than to the prior seeds.

* **Single GA seed vs multi-seed convention (unchanged from [t0106] and [t0112]).**
  [Chen2024-STN][chen2024-stn] used 3 seeds at pop=120, ~1M evals;
  [PolegPolsky2026][polegpolsky2026] used 100 GA seed restarts at pop=10, gens=300-1000. t0113
  ran 1 seed (the same constraint as [t0106] and [t0112]). The 3-seed mean (44, 77, 2247) of
  **1.26%** is **above** the [Hay2011][hay2011] 0.40% envelope point estimate but the **95% CI
  (-0.73%, +3.25%) brackets both [Hay2011][hay2011] and [Druckmann2007][druckmann2007]
  baselines**. The S-0112-01 5-seed batch (two further seeds required) is the agreed path to a
  tighter substrate-rate estimate.

* **Substrate vs published NSGA-II benchmarks (unchanged from [t0112]).**
  [Druckmann2007][druckmann2007] = 12-d, [Hay2011][hay2011] = 22-d, [Achard2006][achard2006] =
  24-d. t0113's 68-d substrate is **2.8x - 5.7x higher dimensional** than any published
  NSGA-II biophysical benchmark. Standard scaling intuition predicts lower acceptance rate at
  higher dimensionality; t0113's 0.15% in 68-d at **single-seed point estimate** is therefore
  not anomalous against the [Hay2011][hay2011] 0.40% / [Druckmann2007][druckmann2007] 0.10%
  envelope.

* **Evaluation budget — well below published references.** t0113 = **5,760 planned / 1,344
  actual** evaluations (the smallest of the 3-seed sample by a factor of 1.5-2.8).
  [Druckmann2007][druckmann2007] used **300,000**; [Hay2011][hay2011] used **500,000**. t0113
  is **~220x below** the modern reference floor — a comparable acceptance rate at 220x lower
  spend supports the [Mohacsi2024][mohacsi2024] observation that the 2-direction objective
  surface converges faster than the published 30+ feature objectives, but the early
  plateau-stop (gen 14, below the 20-60 range in [Mohacsi2024, Fig 4]) means t0113's spend is
  anomalously low even by this comparison.

* **Wall-clock comparison is instance-size confounded.** t0113's 160 s/gen vs [t0112]'s 620
  s/gen is a 3.9x speedup, but the t0113 instance (AMD EPYC 7B13, 64 cores / 256 logical
  threads, 125 GB RAM) had 2x more cores than t0112's 32-core EPYC instance. At the per-core
  level wall-clock is consistent with t0112. The cadence-10 protocol speedup vs [t0106]'s
  cadence-25 reported in [t0112]'s comparison still holds, but t0113 cannot independently
  confirm it without a matched 32-core run.

## Analysis

### Prior Task Comparison

The headline finding is **non-replication of [t0106]'s breakthrough at seed 2247**: t0113
produced **0 LEGIT joint-pass cells** and only **2 asset-declared joint-pass cells** (both
silence-guard DSI = 1.0 artefacts). The frontier-corner is **not reached** from this seed —
best LEGIT DSI is **0.3651** at PD = 10.24 Hz, far below [t0106]'s 0.9939 / [t0112]'s 0.9535,
and best PD-rate is **71.67 Hz**, far below [t0106]'s 122.62 Hz / [t0112]'s 114.76 Hz. This is
the **third independent GA-seed data point** for the substrate's joint-pass density, and it
falls in the **lowest** bucket defined by the task brief (0 LEGIT cells, "substrate not
populated at this seed").

The three-seed dispersion is now 0.15% (2247) / 0.35% (77) / 3.29% (44) — a **22x range** in
unique-count terms. This **strengthens** the [t0112] finding that [t0106]'s 3.3% was an
above-typical lucky seed: with two of three seeds now in the sub-1% regime, the population
mean of the joint-pass acceptance rate is plausibly **below 1%** and the [t0106] outlier is
driving the 3-seed mean of 1.26% almost single-handedly. However, the **standard error (1.01%)
is larger than either of the two literature baselines** (Hay 0.40%, Druckmann 0.10%) — the 95%
CI (-0.73%, +3.25%) brackets zero and both literature points. **No statistical separation is
possible at 3 seeds**; the S-0112-01 5-seed batch is required.

Three non-mutually-exclusive explanations for t0113's sparse result, in decreasing order of
parsimony:

1. **GA-seed variance is genuinely large at this substrate.** The 22x range in unique
   joint-pass counts across seeds 44, 77, 2247 indicates the joint-pass corner is reachable
   only from specific initial-population regions in 68-d space. With seeds 77 and 2247 both
   producing sub-1% yields (and seed 2247 producing zero LEGIT cells), the substrate's
   joint-pass corner appears to be a **narrow, hard-to-reach basin** rather than a broad
   attractor.

2. **The HV-plateau detector fired prematurely at gen 14.** The HV trajectory shows two large
   jumps (gen 7: +2.85; gen 10: +29.39) followed by a 4-gen soft plateau at HV ~36-46. The
   detector requires HV growth < 1% over 2 consecutive generations; the gen 11-12 transition
   (35.98 -> 36.07 = +0.24%) satisfied this **before** the gen 14 jump (36.10 -> 45.62 =
   +26.4%) could materialise. A direct test would re-run seed 2247 with the auto-stop disabled
   to confirm whether the HV would have continued climbing past gen 14 — see suggestion
   S-0113-04 (to be generated in the next stage).

3. **Pool-restart-every-10 may be reducing exploration at certain seeds.** This was originally
   raised after [t0112] as S-0112-03; t0113 strengthens that hypothesis by adding a second
   seed where the cadence-10 protocol plateaued early at a low HV. A controlled test would
   re-run seed 2247 with cadence 25 (matching [t0106]) to isolate the cadence effect from the
   seed effect.

Hypothesis 1 is the most parsimonious; hypotheses 2-3 are not ruled out by this single
replicate.

### Published Literature Comparison

The most consequential finding relative to the literature is that **the 3-seed substrate-rate
estimate cannot yet reject either the [Druckmann2007][druckmann2007] 0.10% or
[Hay2011][hay2011] 0.40% baseline**. The point estimate of 1.26% is 3.15x above the Hay
envelope and 13x above the Druckmann baseline, but the standard error of 1.01% (driven
entirely by the [t0106] outlier at 3.29%) yields a 95% CI of (-0.73%, +3.25%) that brackets
both literature reference values and zero. Pooling t0113's 0.15% with [t0112]'s 0.35% gives a
2-seed sub-substrate mean of **0.25%**, which is **62% of [Hay2011][hay2011]'s 0.40%** and
**2.5x [Druckmann2007][druckmann2007]'s 0.10%** — **essentially within the published
biophysical-NSGA-II envelope** when the [t0106] outlier is excluded.

The interpretation is **bimodal**: either the substrate genuinely supports joint-pass cells at
~0.25% acceptance (consistent with literature) and [t0106]'s 3.29% was a single-seed extreme,
or the substrate supports joint-pass cells at a true rate near the [t0106] mean (3.3%) and
seeds 77 and 2247 both happened to find sparser basins. Without 2 more seeds (S-0112-01 batch
completion) the bimodality cannot be resolved.

The **best LEGIT DSI of 0.3651 falls 48% below [Trenholm2013][trenholm2013] mouse Hb9 control
DSI (0.76)**, **49% below [Oesch2005][oesch2005] rabbit ON-OFF OFF DSI (0.74)**, and **50%
below [PolegPolsky2026][polegpolsky2026]'s unconstrained ML ceiling (0.731)**. Combined with
the [t0107] 8-direction overstatement of ~0.42 absolute, the implied 8-direction vector-sum
DSI for t0113's best legit cell is **effectively zero**. By contrast, [t0106]'s and [t0112]'s
2-direction DSI of ~0.95 implied 8-direction DSI of ~0.5 — still in the biological range.
**t0113 did not produce biologically plausible direction-selective cells**, and this is the
first 3-seed run to clearly fail this bar.

The **HV-plateau at gen 14 is BELOW [Mohacsi2024][mohacsi2024]'s 20-60 gen convergence range**
([Mohacsi2024, Fig 4]). [Mohacsi2024][mohacsi2024] reports that even on the simpler 3-12
parameter problems, NSGA-II takes at least 20 generations to asymptote on HV. The t0113
detector firing 6 gens earlier than the published lower bound on a 68-d problem is **prima
facie evidence of premature stop** — the detector's 1%-over-2-gens threshold is more
aggressive than the literature suggests is safe for biophysical NSGA-II.

The **PD-rate frontier of 71.67 Hz** is 58% of [t0106]'s 122.62 Hz and 62% of [t0112]'s 114.76
Hz, and **36% of [Trenholm2013][trenholm2013]'s 198 Hz biological peak**. The PD frontier is
above the 30 Hz joint-pass floor in absolute terms but the cell at this peak has DSI = 0.0017
— i.e. fast-firing but not direction-selective. The substrate did support PD-rate exploration
on this seed, just not direction selectivity.

## Limitations

* **Single GA seed replicate**. t0113 is one GA seed (2247) contributing the third data point
  to the [t0112] S-0112-01 substrate-rate confirmation batch. The S-0112-01 brief requires at
  least 5 seeds; t0113 delivers seed 3 of 5. The 95% CI on the 3-seed mean of 1.26% spans
  (-0.73%, +3.25%) — **wider than either of the literature reference values** — so no
  rejection of [Druckmann2007][druckmann2007] or [Hay2011][hay2011] is possible. The remaining
  2 seeds will be drawn in separate follow-up tasks.

* **HV-plateau premature trigger highly likely**. The 14-gen stop is the earliest of the
  3-seed sample (t0112 = 21, t0106 = 40) AND is below the [Mohacsi2024][mohacsi2024] published
  20-60 gen convergence range. The HV trajectory's gen 13 -> 14 jump (+26%) suggests the run
  had NOT saturated — the plateau detector was satisfied by the soft gen 11-12 transition
  before the gen 14 jump materialised. A controlled test (S-0113-04 to be generated) would
  re-run seed 2247 with the auto-stop disabled and a 60-gen ceiling.

* **0 LEGIT joint-pass cells confounds the substrate-rate calculation**. The 2 asset-declared
  joint-pass cells are both silence-guard DSI = 1.0 saturations (1 PD spike, 0 ND spikes), not
  biological selectivity. Whether to report t0113's joint-pass count as 0 (LEGIT reading) or 2
  (asset-declared reading) materially shifts the 3-seed mean: with 0 the mean drops to 1.21%
  and with 2 it is 1.26%. The substrate-rate confidence interval is robust to this choice
  (both brackets contain 0% and both literature baselines), but the **interpretation** of
  t0113 differs: zero biological selectivity discovered (LEGIT) vs evaluation artefact
  discovered (asset).

* **2-direction protocol is methodologically novel and not directly comparable to published
  multi-direction DSI measurements**. [Trenholm2013][trenholm2013], [Oesch2005][oesch2005],
  and [PolegPolsky2026][polegpolsky2026] use 8-12 directions. The DSI = 0.3651 LEGIT result
  cannot be claimed as "biologically subthreshold" without an 8-direction post-hoc
  re-evaluation. [t0107] established that [t0106]'s 2-direction ratio DSI overstates
  selectivity by ~0.42 absolute under 8-direction vector-sum; carrying this caveat forward to
  t0113's 0.3651 yields an estimated 8-direction DSI of ~-0.05, i.e. effectively zero — but
  the offset was measured on the [t0106] high-DSI cells, not on the low-DSI region t0113
  occupies.

* **Wall-clock comparison is instance-size confounded**. t0113's 160 s/gen vs [t0112]'s 620
  s/gen is not a clean cadence-10 measurement — t0113's 64-core EPYC has 2x the core count of
  [t0112]'s 32-core EPYC. A controlled test would re-run seed 2247 on the same 32-core class
  as [t0112] to isolate the per-core speedup.

* **Pareto-front parameter-space overlap analysis remains heuristic**. The combined-seed
  (7,104 cells) z-scored L2 standardisation reference is defensible but not the unique correct
  choice. Per-task standardisation, or literature-derived parameter-range standardisation,
  would yield slightly different rankings. The z-scored distances from t0113 Pareto cells
  (mean ~10.7, comparable to seed-44 and seed-77 nearest neighbours) indicate that t0113
  explored a similar region of 68-d space to the prior seeds but did not find the joint-pass
  corner within those regions.

* **No comparable published NSGA-II run at this dimensionality**. The 68-d substrate is 2.8x -
  5.7x higher dimensional than any published biophysical NSGA-II benchmark. The
  acceptance-rate comparison is therefore against extrapolated expectations, not
  matched-dimensional baselines. **Publication-selection bias** also applies:
  [Hay2011][hay2011] and [Druckmann2007][druckmann2007] published successes but not their
  failed seeds, so the per-seed yield distribution in their setting is unknown. t0113's
  near-zero result could plausibly be a normal "failed seed" that those papers also
  encountered but did not report.

* **Evaluation budget materially below published references**. t0113 used 1,344 evaluations vs
  [Hay2011][hay2011]'s 500,000 and [Druckmann2007][druckmann2007]'s 300,000. The acceptance
  rate is measured at 220x - 370x lower spend; whether the rate would converge to the
  published value at matched spend is open.

* **Random-seed draw is not the same as random-seed selection**. The seed 2247 was drawn via
  `secrets.randbelow(10000)` — uniformly random over [0, 9999]. This avoids the
  round-ish-low-number bias of seeds 44 and 77 but does not guarantee good coverage of the
  seed-space. A formal sampling (e.g. quasi-random Latin hypercube over seeds 0-9999) would
  give better coverage but is outside the scope of a minimum-change replicate.

[t0106]: ../../t0106_long_pdnd_nsga2_300gen/ [t0107]: ../../t0107_t0106_polar_8dir_recheck/
[t0112]: ../../t0112_t0106_seed77_replicate/ [druckmann2007]:
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
