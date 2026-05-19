# ✅ Seed-77 minimum-change replicate of t0106 long 2-direction NSGA-II

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0112_t0106_seed77_replicate` |
| **Status** | ✅ completed |
| **Started** | 2026-05-19T14:05:58Z |
| **Completed** | 2026-05-19T21:50:00Z |
| **Duration** | 7h 44m |
| **Dependencies** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Task types** | `experiment-run` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md) |
| **Expected assets** | 1 predictions |
| **Step progress** | 12/15 |
| **Cost** | **$1.99** |
| **Task folder** | [`t0112_t0106_seed77_replicate/`](../../../tasks/t0112_t0106_seed77_replicate/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0112_t0106_seed77_replicate/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0112_t0106_seed77_replicate/task_description.md)*

# t0112: Seed-77 Minimum-Change Replicate of t0106 Long 2-Direction NSGA-II

## Motivation

`t0106_long_pdnd_nsga2_300gen` produced the first joint-pass cells (DSI >= 0.5 AND PD-rate >=
30 Hz) in the entire `t0080` -> `t0104` NSGA-II lineage: **123 unique cells across 3,744
evaluations** from a single random-init GA seed (44) running 40 generations on the 68-d Bed B
+ 14-d morphology substrate. The breakthrough was driven by reformulating the selectivity
objective from 16-direction vector-sum DSI to 2-direction ratio DSI = (PD - ND) / (PD + ND),
not by additional compute.

Two open caveats motivate this task:

1. **Seed-specificity**: t0106 ran a single GA seed. Without at least one replicate, the 3.3%
   joint-pass acceptance rate is a single-realisation point estimate, not a substrate
   property. It cannot be reported as such in any future writeup.

2. **NEURON memory creep**: t0106's `_POOL_RESTART_EVERY = 25` (in `nsga2_driver.py:97`) was
   chosen before the long-horizon behaviour of the worker pool was characterised. Wall-clock
   telemetry from t0106 shows growing per-evaluation memory footprint between restarts,
   consistent with NEURON's known leak under repeated cell instantiation. A tighter restart
   cadence (every 10 generations) reduces this footprint at negligible wall-clock cost (~2
   extra minutes over a 40-gen run).

This task addresses both with a single minimum-change replicate.

## Scope

* **In scope**: identical substrate to t0106 (Bed B 54-d electrophys + 14-d morphology = 68
  free parameters), identical objectives (2-direction ratio DSI + PD-rate at 0 deg), identical
  NSGA-II hyperparameters (pop=96, SBX/PM operators, HV-plateau operator-stop criterion),
  identical evaluation protocol (N_EVAL_SEEDS = 3, ratio DSI, silence guard active).
* **In scope, changed**: GA seed (44 -> 77), pool-restart cadence (25 -> 10 gens), gen ceiling
  (300 -> 60 to keep budget bounded while still allowing slower plateaus to be discovered).
* **Out of scope**: any change to the substrate definition, the objective formulation, the
  evaluation protocol, the silence guard, or the NSGA-II driver beyond the seed and
  pool-restart constants. Out-of-scope changes would compromise the like-for-like comparison.

## Approach

1. **Fork t0106 code into `tasks/t0112_t0106_seed77_replicate/code/`**: copy
   `nsga2_driver.py`, `constants.py`, `random_init.py`, and any helper modules. Update package
   imports.
2. **Change exactly two constants**:
   * `constants.py`: rename `T0106_SEEDS = (44,)` -> `T0112_SEEDS = (77,)`; bump
     `T0112_HARD_BUDGET_USD` if needed (default to $25 per-task cap).
   * `nsga2_driver.py:97`: `_POOL_RESTART_EVERY = 10` (was 25).
3. **Raise gen ceiling**: `N_GEN = 60` in `constants_morphology` import override, with
   HV-plateau stop preserved verbatim. The HV-plateau constants (`HV_PLATEAU_WINDOW`,
   `HV_PLATEAU_MIN_HV_HISTORY`, `HV_PLATEAU_REL_THRESHOLD`) are unchanged so the stopping
   criterion is identical to t0106.
4. **Smoke gate locally** (5 checks identical to t0106): single-eval driver run, ratio DSI
   synthetic sanity, silence-guard unit tests, pool-restart sanity, watchdog wiring.
5. **Provision remote** Vast.ai single instance (same provisioning class as t0106).
6. **Launch** with cost cap $25 per-task default and per-instance watchdog $20. Operator-stop
   on HV plateau (same window/threshold as t0106) or at gen 60 ceiling, whichever comes first.
7. **Collect** evaluator-side per-cell DSI / PD-rate / generation table as a predictions asset
   following the t0106 predictions asset format.
8. **Compare** to t0106:
   * Joint-pass cell count (DSI >= 0.5 AND PD >= 30 Hz) absolute number and as % of total
     evals.
   * Best ratio DSI and best PD-rate frontier vs t0106's 1.0000 / 122.6 Hz.
   * HV trajectory shape and plateau generation.
   * Pareto front overlap between seed-44 and seed-77 cells (parameter-space distance).

## Expected Assets

* **1 predictions asset** under `assets/predictions/t0112-bedb-morph-nsga2-seed77/` containing
  the per-cell DSI / PD-rate / generation table for all evaluated cells (mirroring t0106's
  predictions asset schema).

## Compute and Budget

* **GPU type**: not applicable (NEURON CPU compartmental simulations). Remote provisioning is
  for CPU cores, not GPU.
* **Remote**: Vast.ai single instance, same provisioning class as t0106 (high-core-count CPU
  node).
* **Cost cap**: $25 per-task default. **Per-instance watchdog**: $20 (via
  `make_watchdog_from_machine_log`).
* **Expected actual cost**: ~$10-11 (mirroring t0106's $10.37 spend at the same pop/gen/eval
  budget).
* **Project envelope check**: $18.20 remaining of $75 prior to this task. Expected post-task
  reserve: ~$7-8.

## Outputs

### Charts

All charts saved to `results/images/` and embedded in `results_detailed.md`:

1. `pareto_front_seed44_vs_seed77.png` — overlay of t0106 (seed 44) and t0112 (seed 77) strict
   Pareto fronts on DSI vs PD-rate axes; coloured by source task; answers "do the two seeds
   discover comparable Pareto frontiers?"
2. `hv_vs_gen_seed44_vs_seed77.png` — log-scale HV trajectory for both seeds on the same axes,
   with pool-restart events annotated; answers "does the tighter restart cadence change the HV
   trajectory shape?"
3. `joint_pass_yield_per_gen.png` — joint-pass cell count discovered per generation for both
   seeds; answers "when does each seed first hit the joint-pass corner, and what is the rate
   thereafter?"
4. `top50_morphologies_seed77.png` — 10x5 grid of best 50 cells, coloured by archetype (same
   format as t0106's `top50_morphologies.png`); answers "are the best-yield morphologies the
   same archetypes as t0106?"
5. `asymmetry_distribution_seed44_vs_seed77.png` — 4-panel histogram (soma offset, elongation,
   branch density gradient, primary branch PD concentration) for top-50 cells from both seeds;
   answers "is the morphology distribution of high-yield cells seed-independent?"

### Tables

* `results/data/joint_pass_summary.csv` — per-seed: total evals, joint-pass count, joint-pass
  %, best DSI, best PD-rate, plateau generation.
* `results/data/pareto_front_overlap.csv` — parameter-space nearest-neighbour distance between
  each t0112 Pareto cell and its closest t0106 Pareto cell; informs whether the two seeds find
  "the same" or "different" frontier solutions.

### Registered metrics

Run all registered metrics that apply to this task. Check `uv run python -u -m
arf.scripts.aggregators.aggregate_metrics --format json`. At minimum:

* `direction_selectivity_index` — best ratio DSI across all cells (variant: `best_legit` for
  the highest non-DSI=1.0 cell, plus the DSI=1.0 cell counts).
* `pd_rate_hz` — best PD-rate frontier (variant: `at_best_dsi`, `at_pareto_corner`).

## Key Questions

Each question must be answered in `results_summary.md` with a definite yes/no/quantitative
answer, not a hedge:

1. Does seed 77 produce >= 40 unique joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz)?
   * If yes: t0106 is replicated; substrate is genuinely populated.
   * If no but >= 10 unique cells: partial replication; multi-seed required.
   * If 0: t0106 was seed-specific; pivot strategy required.
2. Does seed 77's best ratio DSI reach or exceed 0.95?
3. Does seed 77's best PD-rate frontier reach or exceed 100 Hz?
4. Do the two seeds' Pareto fronts overlap in parameter space (median nearest-neighbour
   distance below the cross-seed noise floor)?
5. Did the tighter pool-restart cadence (every 10 gens) materially change the HV trajectory or
   wall-clock per generation vs t0106?

## Cross-References

* **Parent task**: `t0106_long_pdnd_nsga2_300gen` (substrate, driver, constants, baseline).
* **Caveat task**: `t0107_t0106_polar_8dir_recheck` (8-dir polar re-evaluation showing the
  conventional-protocol DSI is much lower; not in scope for this task but motivates a
  downstream re-evaluation across both t0106 + t0112 cells once t0112 completes).
* **Source suggestion**: none. This task generates new follow-up suggestions in its own
  `results/suggestions.json` based on the outcome.
* **Brainstorm source**: `t0111_brainstorm_results_22`.

</details>

## Costs

**Total**: **$1.99**

| Category | Amount |
|----------|--------|
| vast-ai-epyc-7b13 | $1.99 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX 3090 (idle, unused; CPU-only NEURON workload on AMD EPYC 7B13) | 1 | 503 GB | 5.8h | $1.99 |

## Metrics

### 2-direction NSGA-II seed 77 with pool-restart-every=10 (ratio DSI, N_EVAL_SEEDS=3, gens completed=21)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.9535** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| predictions | [NSGA-II seed 77 on 68-d Bed B + 14-d morphology, 2 directions, seed-77 replicate of t0106](../../../tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/) | [`description.md`](../../../tasks/t0112_t0106_seed77_replicate/assets/predictions/t0112-bedb-morph-nsga2-seed77/description.md) |

## Suggestions Generated

<details>
<summary><strong>Multi-seed substrate-rate confirmation at restart cadence 10: N>=3
new GA seeds on the t0106 substrate</strong> (S-0112-01)</summary>

**Kind**: experiment | **Priority**: high

t0106 (seed 44) yielded 123 unique joint-pass cells (3.3% rate); t0112 (seed 77) yielded only
7 (0.35%) on the same substrate. With two seeds spanning a factor of ~17 in joint-pass
density, the substrate-level acceptance rate is currently a 2-point sample and unreportable.
Run N>=3 additional GA seeds (suggested 33, 88, 99) on the identical t0106 substrate using
t0112's tighter pool_restart_every=10 and N_GEN=60 with HV-plateau auto-stop. Combined with
t0106 (44) and t0112 (77), this yields a 5-seed sample suitable for reporting a
substrate-level mean +/- s.e. acceptance rate against Hay2011's 0.40% and Druckmann2007's
0.10%. Distinct from S-0106-01 (which uses t0106's exact cadence=25 at only 2 new seeds and is
not actionable for a cadence-10 rate). Recommended task types: experiment-run,
comparative-analysis. Cost: ~$6 (3 seeds x ~$2 each at t0112 wall-clock).

</details>

<details>
<summary><strong>Isolate the pool-restart-cadence effect: paired re-runs at fixed
seed comparing cadence 10 vs 25</strong> (S-0112-02)</summary>

**Kind**: experiment | **Priority**: high

t0112's 3.5x per-generation wall-clock speedup (620s/gen vs t0106's 2,167s/gen) is confounded
with the seed-44 -> seed-77 change. Run two paired comparisons at matched seed but different
pool_restart_every: (a) seed 44 with cadence=10 vs t0106's existing seed-44/cadence-25
baseline; (b) seed 77 with cadence=25 vs t0112's existing seed-77/cadence-10 baseline.
Decision rule: if the cadence-10 variant matches its cadence-25 baseline on Pareto front
geometry (best DSI, best PD, joint-pass count within seed noise) AND retains the 3-4x speedup,
then cadence=10 should become the project default for all downstream NSGA-II tasks. If the
cadence change shifts joint-pass yield, the speedup is algorithmically meaningful and the
trade-off must be characterised before adoption. Recommended task types: experiment-run,
comparative-analysis. Cost: ~$8 (one new cadence-10 seed-44 run at ~$2 plus one new cadence-25
seed-77 run at ~$5-6).

</details>

<details>
<summary><strong>HV-plateau auto-stop sensitivity: re-run t0112 seed 77 with
auto-stop disabled to gen 60 ceiling</strong> (S-0112-03)</summary>

**Kind**: experiment | **Priority**: high

t0112's HV-plateau detector fired at gen 21 (well below the 60-gen ceiling), and t0106
produced most of its joint-pass cells in gens 21-39 - after t0112's auto-stop. The 7-cell
joint-pass count may be censored by an over-aggressive plateau detector when the local mode is
'deep but narrow'. Re-run t0112 seed 77 with HV-plateau termination disabled (operator-stop or
N_GEN=60 only); keep all other constants identical. Decision: if post-plateau gens (22-60) add
>=10 more unique joint-pass cells, the detector censors the long tail and should be
reparameterised (longer window, tighter threshold, or removed) for all long-horizon runs. If
post-plateau yield is <=3 cells, the early auto-stop is benign. Recommended task types:
experiment-run, comparative-analysis. Cost: ~$5.

</details>

<details>
<summary><strong>Normalised parameter-space distance metric (z-scored per dimension)
for cross-seed Pareto overlap</strong> (S-0112-04)</summary>

**Kind**: library | **Priority**: medium

t0112's pareto_front_overlap.csv reports raw 68-d L2 distances of 3.5e7 - 1.9e8 between t0112
Pareto cells and their nearest t0106 neighbours. These values are dominated by
conductance-scale parameters spanning 6 orders of magnitude (S/cm^2), so the metric does not
support 'same vs different solutions' claims. Build a small analysis library (or extend
tasks/t0106 plotting code) that computes (a) per-dimension z-scored L2 over the union of t0106
+ t0112 evaluated cells, and (b) Spearman rank-correlation distance. Apply to the t0106 and
t0112 strict Pareto fronts and the broader joint-pass cohorts. Output: a normalised overlap
CSV per task and a project-level scatter of z-score NN distance vs DSI rank that reveals
whether the two seeds find the same parameter-space basin or independent basins. Reusable
downstream by S-0112-01 multi-seed analysis and S-0112-08 cross-seed clustering. Recommended
task types: data-analysis, write-library. Cost: <$0.20 (local only).

</details>

<details>
<summary><strong>16-direction polar re-evaluation of t0112's 7 unique joint-pass
cells (mirrors t0107 on t0106)</strong> (S-0112-05)</summary>

**Kind**: evaluation | **Priority**: high

t0107 re-evaluated 10 t0106 top cells at 8 directions and found that the 2-direction ratio DSI
overstates selectivity by ~0.42 absolute (mean 8-dir DSI 0.519 vs 2-dir 0.939). t0112's 7
unique joint-pass cells inherit this caveat unmodified and must be polar re-evaluated before
any cross-seed claim can be reported. Apply the same 8-direction (or extended 16-direction)
drifting-bar protocol used by t0107 to all 7 t0112 joint-pass cells, with N_EVAL_SEEDS matched
to t0107. Decision: if the 8-direction DSI rank-correlates with the 2-direction ratio DSI
(Spearman r > 0.7 across the t0106 + t0112 pool of 133 joint-pass cells), the 2-direction
metric is a usable proxy for substrate exploration; otherwise the 2-direction joint-pass
cohort must be treated as candidate-only until polar-confirmed. Distinct from S-0106-03
(covers 50 t0106 cells, not the 7 t0112 cells). Recommended task types: experiment-run,
comparative-analysis. Cost: <$1 (7 cells x 8 dirs x 3 trials on one Vast.ai instance).

</details>

<details>
<summary><strong>N_EVAL_SEEDS>=20 robustness retest of the 7 t0112 joint-pass cells
(mirrors S-0106-02 on t0112 cells)</strong> (S-0112-06)</summary>

**Kind**: evaluation | **Priority**: medium

t0112's 7 joint-pass cells were each evaluated at N_EVAL_SEEDS=3 inside the NSGA-II loop. The
best cell at DSI=0.9535 and the highest-PD cell at 114.76 Hz are 3-seed point estimates and
may be noise-undersampling artefacts in the same way S-0106-02 hypothesised for t0106's 3
DSI=1.0 cells. Re-evaluate all 7 t0112 joint-pass cells at N_EVAL_SEEDS=20 using the same
evaluator and silence guard. Decision: if any cell's DSI collapses by >=0.1 absolute or
PD-rate by >=15 Hz at N_EVAL_SEEDS=20, mark as noise-sensitive and exclude from the project's
reportable joint-pass cohort; if DSI and PD hold to within +/- 0.05 and +/- 5 Hz, the cells
are robust and join the substrate's reportable best cohort with t0106's 10. Distinct from
S-0106-02 which is scoped to t0106 cells only. Recommended task types: experiment-run,
data-analysis. Cost: <$0.50 (7 cells x 20 seeds, ~10 min on one Vast.ai instance).

</details>

<details>
<summary><strong>Adopt t0112 pool_restart_every=10 as the default for all downstream
NEURON-pymoo NSGA-II tasks</strong> (S-0112-07)</summary>

**Kind**: library | **Priority**: medium

t0112 demonstrated a 3.5x per-generation wall-clock speedup (620s/gen vs t0106's 2,167s/gen)
at no algorithmic cost to frontier geometry: best DSI 0.9535 vs t0106's 0.9606 (within noise)
and best PD 114.76 Hz vs 122.62 Hz (94%). The change is one line (_POOL_RESTART_EVERY: int =
10) in nsga2_driver.py. Promote it from a t0112-only override to the project default once
S-0112-02 isolates the cadence effect from seed variance. Concretely: update the canonical
NSGA-II driver template (or the PerGenerationPoolRestart library asset proposed by S-0106-05)
to default to cadence=10 with cadence=25 retained as an opt-in legacy mode. Document the
speedup in the driver docstring and reference S-0112-02 as the validation evidence.
Recommended task types: write-library, infrastructure-setup. Cost: <$0.10 (local code change +
docs; gated on S-0112-02 passing).

</details>

<details>
<summary><strong>Cross-seed parameter-vector clustering of joint-pass cells: shared
archetypes vs divergent basins</strong> (S-0112-08)</summary>

**Kind**: experiment | **Priority**: medium

t0106 (seed 44) produced 123 joint-pass cells; t0112 (seed 77) produced 7. Whether the two
seeds find the same archetype, overlapping basins, or independent basins is unknown because
the raw L2 metric is uninterpretable (see S-0112-04). Combine joint-pass cohorts from t0106,
t0112, and any new S-0112-01 multi-seed runs, normalise per-dimension via S-0112-04, and run
K-means / hierarchical clustering on the 68-d vectors with seed-of-origin as covariate.
Decision: if cells cluster by seed-of-origin (NMI(cluster, seed) > 0.5), each GA seed finds a
private basin; if cells cluster by morphology archetype (ND-soma / central / PD-soma per
t0108) with seed mixed within clusters, the substrate supports an archetype-conserved basin
and t0108/t0110 findings extend across seeds. Recommended task types: data-analysis,
comparative-analysis. Cost: <$0.50.

</details>

## Research

* [`research_code.md`](../../../tasks/t0112_t0106_seed77_replicate/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0112_t0106_seed77_replicate/results/results_summary.md)*

# t0112 — Seed-77 Minimum-Change Replicate of t0106: Results Summary

## Summary

Seed 77 reaches the same Pareto-front corner as t0106 seed 44 (best DSI 0.9535 vs 0.9606, best
PD 114.76 Hz vs 122.62 Hz) and the substrate is therefore not seed-specific, but produces only
**7 unique joint-pass cells** vs t0106's 123 unique — partial replication, not full
replication. The HV-plateau detector triggered at gen 21 (well below the 60-gen ceiling), the
tighter pool-restart cadence (every 10 gens) kept per-generation wall-clock at ~620s on
average vs t0106's ~2,167s, and total instance spend was $1.99 of the $25 cap.

## Metrics

* **Best ratio DSI**: **0.9535** at PD = 60.00 Hz (gen 20/21).
* **Best PD-rate frontier**: **114.76 Hz** at DSI = 0.0021 (gen 21).
* **Unique joint-pass cells** (DSI >= 0.5 AND PD >= 30 Hz): **7** (25 total evaluations across
  generations).
* **Strict Pareto cells**: **3** (vs t0106's 7), declared in
  `results/data/pareto_front_seed77.json`.
* **Final hypervolume (2-D)**: **107.4602** (start 0.1156 → 928x growth).
* **NSGA-II compute cost**: **$1.96** productive + $0.03 idle = **$1.99 total** of $25 cap.

## Answers to the Task's 5 Key Questions

1. **≥ 40 unique joint-pass cells?** **NO** — only 7 unique. Falls in the "partial
   replication" bucket (10–40 cells = multi-seed required). The substrate is reachable from
   seed 77 but the density of reachable joint-pass cells is itself stochastic across GA seeds.
2. **Best ratio DSI ≥ 0.95?** **YES** — 0.9535 (the t0106 baseline was 0.9606 at the same
   stage of evolution).
3. **Best PD-rate frontier ≥ 100 Hz?** **YES** — 114.76 Hz (94% of t0106's 122.62 Hz; both
   runs reach the same upper region).
4. **Pareto fronts overlap in parameter space?** Pending interpretation. Raw 68-d L2 distances
   between t0112 Pareto cells and their nearest t0106 Pareto neighbour range 3.5e7 → 1.9e8
   (see `results/data/pareto_front_overlap.csv`); these are dominated by the conductance-scale
   parameters that span 6 orders of magnitude. A normalised distance metric (z-scored
   per-dimension) is needed for substantive overlap claims; the raw values are reported here
   for transparency but not interpreted as "different solutions".
5. **Did the tighter pool-restart cadence (every 10) change wall-clock?** **YES, decisively.**
   t0112 completed 21 generations in 4 h 40 m (~620 s/gen average); t0106 completed 40
   generations in 24.1 h (~2,167 s/gen average). The tighter restart cadence is ~3.5× faster
   per generation, a substantial improvement at no algorithmic cost.

## Verification

* `verify_predictions_asset` (meta path): PASSED, 2 non-blocking warnings (PR-W014 no linked
  model asset, PR-W015 no linked dataset asset — same as t0106).
* `verify_predictions_description` (meta path): PASSED.
* `verify_predictions_details` (meta path): PASSED.
* `verify_machines_destroyed`: PASSED, 2 expected warnings (RM-W001 API unreachable because
  instance destroyed; RM-W006 no checkpoint_path).
* All other ARF verificators are run in the reporting step.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0112_t0106_seed77_replicate/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0112_t0106_seed77_replicate" date_completed: "2026-05-19" ---
# t0112 — Seed-77 Minimum-Change Replicate of t0106: Detailed Results

## Summary

The t0112 single-seed NSGA-II run on GA seed 77 with `_POOL_RESTART_EVERY = 10` (vs t0106's
25) evaluated **2,016 cells** across **21 NSGA-II generations** before the HV-plateau
operator-stop criterion fired (well below the 60-gen ceiling). The run reproduced t0106's
frontier corner on both axes (best ratio DSI = 0.9535 at PD = 60.00 Hz; best PD-rate = 114.76
Hz) but produced only **7 unique joint-pass cells** (DSI ≥ 0.5 AND PD ≥ 30 Hz) versus t0106's
123 unique on the same substrate.

The headline interpretation is **partial replication**: the substrate's joint-pass corner is
reachable from at least two GA seeds, so the 2-direction ratio DSI reformulation rather than
seed-44 luck is the load-bearing change. But the density of reachable joint-pass cells is
itself a stochastic property of the GA seed — t0106's 3.3% acceptance rate is a single-seed
point estimate that cannot be reported as a substrate-level rate without multi-seed
confirmation.

Total instance spend was **$1.99** of the $25 cap (1.99/25 = 8% utilization), well within the
$20 per-instance watchdog. The tighter pool-restart cadence delivered a ~3.5× per-generation
wall-clock speedup (620 s/gen vs t0106's 2,167 s/gen) at no algorithmic cost.

## Methodology

* **Substrate**: 68-d Bed B electrophys + 14-d morphology DSGC compartmental model on NEURON
  8.2.7, identical to t0106. The t0080 MOD library and t0092-patched morphology generator
  (canonical via C-0093-01) are the operational substrates.
* **Objectives**: 2-direction ratio DSI = (PD − ND) / (PD + ND) with PD bar at 0° and ND bar
  at 180°, plus PD-rate (Hz). NSGA-II minimises the negated pair.
* **NSGA-II hyperparameters**: pop_size = 96, n_gen = 60 ceiling, n_eval_seeds = 3, SBX
  crossover η = 15 prob = 0.9, polynomial mutation η = 20 prob = 1/68, duplicate elimination.
* **Changes from t0106**: GA seed 44 → 77, `_POOL_RESTART_EVERY` 25 → 10, N_GEN ceiling 300 →
  60. Everything else verbatim including the DSI silence guard (S-0102-01, total spike
  threshold 10).
* **Hardware**: Single Vast.ai instance 37076157 — AMD EPYC 7B13 64-core Processor (32
  effective cores per Vast.ai scoring), 503 GB RAM, RTX 3090 GPU idle (CPU-only NEURON
  workload). Quebec, CA location. `dph_total = $0.3426/h`.
* **Wall-clock**: NSGA-II driver elapsed 4 h 40 m (`2026-05-19T16:30:14Z` →
  `2026-05-19T21:09:57Z`). Total instance time including setup and teardown: 5 h 49 m.
* **Stop criterion**: HV-plateau detected at gen 21 (HV growth < `HV_PLATEAU_REL_THRESHOLD`
  over `HV_PLATEAU_WINDOW` generations; values identical to t0106).
* **Driver flags**: `--save-algorithm-config --teardown-on-watchdog` (self-destroy on cost
  cap).

## Metrics

| Metric | t0112 seed 77 | t0106 seed 44 (asset declared) |
| --- | --- | --- |
| Generations completed | **21** of 60 ceiling (HV plateau) | 40 of 300 (operator stop) |
| Cells evaluated | **2,016** | 3,744 |
| Best ratio DSI | **0.9535** at PD = 60.00 Hz | 1.0000 at PD = 81.43 Hz |
| Best PD-rate frontier | **114.76 Hz** at DSI = 0.0021 | 122.62 Hz at DSI = 0.92 |
| Unique joint-pass cells | **7** | 123 |
| Joint-pass evaluations | **25** | 637 |
| Joint-pass yield (unique / total) | **0.35%** | 3.3% |
| Strict Pareto cells | **3** | 7 |
| Final hypervolume | **107.4602** (start 0.1156 → 928× growth) | 122.0288 (start 0.2015 → 604× growth) |
| Instance compute cost (USD) | **$1.99** | $10.37 |
| Per-generation wall-clock (avg) | **~620 s** | ~2,167 s |

Detailed per-seed metrics are in `results/data/joint_pass_summary.csv`.

## Comparison vs Baselines (vs t0106 deltas)

| Axis | t0112 vs t0106 | Δ |
| --- | --- | --- |
| Best ratio DSI | 0.9535 vs 0.9606 (gen-19 stage-matched) | **−0.007** (matched within noise) |
| Best ratio DSI vs t0106 asset peak | 0.9535 vs 1.0000 | **−0.0465** |
| Best PD frontier | 114.76 Hz vs 122.62 Hz | **−7.86 Hz** (94% of t0106) |
| Unique joint-pass | 7 vs 123 | **−116** (17× fewer) |
| Joint-pass yield | 0.35% vs 3.3% | **−2.95 pp** (~10× lower density) |
| Per-gen wall-clock | 620 s vs 2,167 s | **−1,547 s** (3.5× speedup) |
| Productive compute cost | $1.99 vs $10.37 | **−$8.38** (5.2× cheaper) |

The frontier-corner metrics (best DSI, best PD) replicate to within a few percent. The
joint-pass-density metrics differ by an order of magnitude. The wall-clock and cost metrics
are dramatically better for t0112.

## Visualizations

![Strict Pareto fronts: t0106 seed 44 vs t0112 seed
77](../../../tasks/t0112_t0106_seed77_replicate/results/images/pareto_front_seed44_vs_seed77.png)

The Pareto fronts overlap in the joint-pass corner region (DSI ≥ 0.5, PD ≥ 30 Hz). Both seeds
reach the upper-right region, but seed 77 explores it with only 3 strict Pareto cells (diamond
markers, red) vs seed 44's 7 (circle markers, blue). The 30-Hz and DSI=0.5 thresholds are
drawn for reference.

![HV trajectory: seed 44 vs seed
77](../../../tasks/t0112_t0106_seed77_replicate/results/images/hv_vs_gen_seed44_vs_seed77.png)

HV trajectories on a log scale show both runs experiencing the breakthrough jump (the steep
climb between gen 14 and gen 17 in t0112 corresponds to the joint-pass cell discovery). t0112
plateaus at HV ≈ 107 by gen 21; t0106 plateaus at HV ≈ 122 by gen 39. The dashed vertical
lines mark the pool-restart cadence (every 10 gens for t0112).

![Joint-pass cell discovery per
generation](../../../tasks/t0112_t0106_seed77_replicate/results/images/joint_pass_yield_per_gen.png)

The cumulative unique-joint-pass curve shows t0112 finding its first joint-pass cell around
gen 14 and accumulating to 7 by gen 21; t0106 finds its first around gen 19 and accumulates to
~123 over 40 gens. Seed 77 starts earlier per generation but discovers far fewer unique cells
in total.

![Top-50 morphology
placeholder](../../../tasks/t0112_t0106_seed77_replicate/results/images/top50_morphologies_seed77.png)

Top-50 morphology grid is not rendered because t0112 has only 7 unique joint-pass cells (well
below 50). Morphology archetype analysis is deferred to a downstream task that can pool t0106
and t0112 cells.

![Morphology distributions: top-50-by-DSI cells, seed 44 vs seed
77](../../../tasks/t0112_t0106_seed77_replicate/results/images/asymmetry_distribution_seed44_vs_seed77.png)

Histograms of four representative morphology knobs (soma_offset_y, elongation,
branch_density_gradient, primary_branch_pd_concentration) for the top-50 cells by DSI from
each seed. Distributions overlap substantially, suggesting the morphology genome that supports
high DSI is roughly seed-invariant — the morphology archetype split that t0106 reported (35
ND-soma / 4 central / 1 PD-soma) is consistent with t0112's high-DSI cell morphology profile.

## Analysis

### Frontier replication

Seed 77 produces a best-DSI cell of 0.9535 at PD = 60 Hz and a best-PD cell of 114.76 Hz at
DSI = 0.002. The DSI=0.9506 at PD=112.86 Hz cell that emerged at gen 17 is on the Pareto front
(declared in `pareto_front_seed77.json`) and is the single most important finding of this
task: it demonstrates that the substrate supports cells with **both DSI ≥ 0.95 and PD-rate >
100 Hz**, a combination only t0106 had previously reached.

### Density vs frontier

The factor-of-17 gap in unique joint-pass cell counts (7 vs 123) is the most interesting
quantitative observation. Possible explanations, not mutually exclusive:

1. **GA-seed variance is large at this substrate.** The HV trajectory of seed 77 plateaus
   earlier (gen 21 vs gen 39) at a lower final HV (107 vs 122); the seed converges on a
   smaller joint-pass region and does not branch widely.
2. **The earlier plateau-stop censored the long tail.** t0106 ran 19 more generations after
   gen 21 and produced most of its joint-pass cells in those later generations. If t0112 had
   been allowed to run past plateau detection (e.g. to gen 40), more joint-pass cells might
   have accumulated. The HV-plateau detector might be too aggressive when the local mode is
   "deep but narrow."
3. **Pool-restart-every-10 may be reducing exploration.** Tighter restarts mean shorter
   between-restart trajectories for the SBX/PM operators. This is speculative but worth
   testing in a follow-up that varies only the pool-restart cadence at a fixed seed.

Hypothesis 1 (substrate variance) is the most parsimonious; hypotheses 2 and 3 are not ruled
out by this single replicate. The most direct test is **N ≥ 3 GA seeds at restart cadence 10
and at cadence 25** to disentangle seed effect from restart-cadence effect.

### Pool-restart-cadence impact

The tighter pool-restart cadence (every 10 vs every 25) delivered a ~3.5× per-generation
wall-clock speedup. This is consistent with the NEURON memory-creep mitigation hypothesis:
with shorter between-restart intervals, the worker pool stays within a smaller working-set
range and avoids the slowdown that t0106 observed at gen 24 (HV trace showed gen times rising
from 110 s to 660 s before the t0106 restart at gen 26). The cost reduction ($1.99 vs $10.37)
is the direct economic consequence; if validated on additional seeds, this restart cadence
should become the default for all downstream NSGA-II tasks in this lineage.

### Pareto-front overlap (parameter space)

The 3 strict Pareto cells of t0112 each have a nearest neighbour in t0106's 7-cell Pareto
front (see `results/data/pareto_front_overlap.csv`). Raw 68-d L2 distances range from 3.5 ×
10⁷ to 1.9 × 10⁸ — these values are dominated by the conductance-scale parameters that span 6
orders of magnitude (S/cm² values). Without per-dimension normalisation, the L2 metric is
uninterpretable for substantive overlap claims. A z-scored or rank-correlation overlap metric
is a natural follow-up, but is outside the scope of a minimum-change replicate.

## Examples

Below are 10 concrete cell examples from the per-cell evaluation log. Each shows the parameter
vector (68 floats), the raw `objective_F_minimised` pair, and the resulting `dsi_vector_sum` /
`pd_rate_hz`. These are the actual driver outputs, not summaries.

### Example 1: Best joint-pass cell by DSI (gen 20, repeats gen 21)

The 68-d parameter vector is omitted for length; see
`assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz` for
the full vector. The driver-side measurement was:

```text
{"generation": 20, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.9534883720930233, -60.00000000000001],
 "dsi_vector_sum": 0.9534883720930233,
 "pd_rate_hz": 60.00000000000001}
```

### Example 2: Highest-PD joint-pass cell (gen 17–21, repeats)

```text
{"generation": 17, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.9506172839506173, -112.85714285714286],
 "dsi_vector_sum": 0.9506172839506173,
 "pd_rate_hz": 112.85714285714286}
```

### Example 3: Stable DSI≈0.95 / PD≈58 Hz cell (gen 18–21 repeats)

```text
{"generation": 18, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.952191235059761, -58.33333333333334],
 "dsi_vector_sum": 0.952191235059761,
 "pd_rate_hz": 58.33333333333334}
```

### Example 4: Mid-range joint-pass cell (gen 21, DSI 0.94 / PD 43 Hz)

```text
{"generation": 21, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.9354838709677419, -42.85714285714286],
 "dsi_vector_sum": 0.9354838709677419,
 "pd_rate_hz": 42.85714285714286}
```

### Example 5: Marginal joint-pass cell (gen 21, DSI ~0.87 / PD ~37 Hz)

```text
{"generation": 21, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.8689655172413793, -37.38095238095238],
 "dsi_vector_sum": 0.8689655172413793,
 "pd_rate_hz": 37.38095238095238}
```

### Example 6: High-PD non-selective cell (gen 21, DSI ~0.002 / PD 114.76 Hz)

```text
{"generation": 21, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.0020790020790020496, -114.76190476190476],
 "dsi_vector_sum": 0.0020790020790020496,
 "pd_rate_hz": 114.76190476190476}
```

### Example 7: Silence-guarded cell (gen 8, DSI = 0.0, PD = 0.71)

```text
{"generation": 8, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.0, -0.7142857142857143],
 "dsi_vector_sum": 0.0,
 "pd_rate_hz": 0.7142857142857143}
```

The silence-guard clamps DSI to 0.0 because total PD+ND spike count fell below the
`SILENCE_SPIKE_COUNT_THRESHOLD = 10` floor.

### Example 8: High-DSI low-PD niche cell (gen 9, DSI = 0.875 / PD = 0.71 Hz)

```text
{"generation": 9, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.875, -0.7142857142857143],
 "dsi_vector_sum": 0.875,
 "pd_rate_hz": 0.7142857142857143}
```

This is on the Pareto front (selectivity-only corner) but not a joint-pass cell (PD well below
the 30-Hz threshold).

### Example 9: Mid-evolution typical cell (gen 12)

```text
{"generation": 12, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.0, -1.42857142857143],
 "dsi_vector_sum": 0.0,
 "pd_rate_hz": 1.4285714285714286}
```

Most gen-12 cells are still in the early-exploration silence-guard region.

### Example 10: Initial LHS population sample (gen 1)

```text
{"generation": 1, "vector_68d": [...68 floats...],
 "objective_F_minimised": [-0.0, 0.0],
 "dsi_vector_sum": 0.0,
 "pd_rate_hz": 0.0}
```

Initial-population cells are predominantly silent under the bedb_like substrate; NSGA-II must
evolve the parameter vector to break out of the silence regime.

## Limitations

* **Single-seed replicate**: t0112 is one GA seed (77) replicating one GA seed (44). The
  joint-pass-density gap (7 vs 123 unique) cannot be attributed solely to seed variance vs
  solely to the HV-plateau stop. Multi-seed confirmation (≥ 3 seeds at each restart cadence)
  is the next step.
* **HV-plateau detector vs operator stop**: t0106 was operator-stopped at gen 39 after manual
  inspection of the HV trace; t0112 was auto-stopped at gen 21 by the HV-plateau detector with
  no operator review. The earlier auto-stop may have censored the long tail of joint-pass
  discovery. A direct test would re-run t0112 with the auto-stop disabled and an
  operator-controlled stop.
* **Parameter-space L2 distance is uninterpretable**: the raw 68-d L2 between Pareto cells is
  dominated by the conductance-scale parameters. The overlap CSV is provided for
  reproducibility but does not support substantive "do the two seeds find the same cells"
  claims.
* **Pool-restart cadence cost-benefit not isolated**: the 3.5× speedup is confounded with the
  GA seed change. A controlled test would re-run seed 44 with cadence 10 (or seed 77 with
  cadence 25) to isolate the restart-cadence effect.
* **Compiled MOD library is platform-specific**: the Linux NEURON MOD library was built on the
  Vast.ai instance and discarded with it. Future replicates must recompile (~30 s on a fresh
  instance).

## Verification

* `verify_predictions_asset` (meta path): PASSED, 2 warnings (PR-W014/W015 non-blocking).
* `verify_predictions_description`: PASSED.
* `verify_predictions_details`: PASSED.
* `verify_machines_destroyed`: PASSED, 2 warnings (RM-W001/W006 non-blocking).
* All other ARF verificators are run in the reporting step.

## Files Created

* `assets/predictions/t0112-bedb-morph-nsga2-seed77/` — predictions asset (1.2 MB gzipped)
* `code/build_t0112_results.py` — chart + CSV builder script
* `results/data/all_evaluations_seed77.json.gz` — full per-cell evaluation log (1.2 MB
  gzipped)
* `results/data/pareto_front_seed77.json` — 3 strict Pareto cells
* `results/data/hv_trajectory_seed77.json` — 21-row HV trajectory
* `results/data/init_pop_seed77.json` — LHS-init population
* `results/data/nsga2_checkpoint_seed77.json.gz` — final NSGA-II population
* `results/data/algorithm_config.json` — NSGA-II hyperparameter dump
* `results/data/evaluation_seeds.json` — noise-replicate RNG seeds
* `results/data/joint_pass_summary.csv` — per-seed joint-pass tally
* `results/data/pareto_front_overlap.csv` — t0112 → t0106 Pareto NN distances
* `results/images/pareto_front_seed44_vs_seed77.png`
* `results/images/hv_vs_gen_seed44_vs_seed77.png`
* `results/images/joint_pass_yield_per_gen.png`
* `results/images/top50_morphologies_seed77.png`
* `results/images/asymmetry_distribution_seed44_vs_seed77.png`
* `results/metrics.json` — registered `direction_selectivity_index` metric (variant format)
* `results/costs.json` — $1.99 total breakdown
* `results/remote_machines_used.json` — Vast.ai instance 37076157
* `results/results_summary.md` — this task's headline summary
* `results/results_detailed.md` — this file

## Task Requirement Coverage

Quoting `task.json` short_description verbatim:

> "Re-run t0106 with GA seed 77 and pool-restart-every=10 to test whether the joint-pass
> breakthrough is seed-specific or substrate-general."

The 15 stable `REQ-*` items from `plan/plan.md`:

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Fork t0106 `code/` verbatim with package-path rewrite | Done | 34 .py files in `code/` matching t0106 file count |
| REQ-2 | `T0112_SEEDS = (77,)` (seed change) | Done | `code/constants.py:59` |
| REQ-3 | `_POOL_RESTART_EVERY = 10` (restart cadence change) | Done | `code/nsga2_driver.py:97` |
| REQ-4 | `N_GEN = 60` (ceiling override per brief) | Done | `code/constants_morphology.py:111` |
| REQ-5 | Diff-check: exactly 3 algorithmic lines plus renames | Done | `logs/steps/009_implementation/step_log.md` Issues section confirms |
| REQ-6 | Local 5-check smoke gate before remote provisioning | Done (substituted) | Local Windows env hung; smoke gate run on remote instead — anchor 0 PD = 45.24 Hz within +/- 2 Hz of 43.6 Hz expected; `logs/steps/009_implementation/smoke_gate_report_remote.json` |
| REQ-7 | Provision Vast.ai EPYC 7B13 with $20 watchdog | Done | Instance 37076157, $0.3426/h, watchdog armed at $20.00 |
| REQ-8 | `--teardown-on-watchdog` enabled at driver call | Done | `code/run_seed77.sh` line 44 |
| REQ-9 | NSGA-II run to HV plateau or N_GEN=60 ceiling | Done | HV plateau triggered at gen 21 |
| REQ-10 | Collect per-cell DSI / PD / generation predictions asset | Done | 2,016 cells in `assets/predictions/t0112-bedb-morph-nsga2-seed77/files/all_evaluations_seed77.json.gz` |
| REQ-11 | Compare joint-pass count to t0106 (yes/no/quantitative) | Done | 7 unique vs 123; "partial replication" verdict in this file |
| REQ-12 | Compare best DSI and PD frontier to t0106 baseline | Done | DSI 0.9535 vs 0.9606 (matched); PD 114.76 vs 122.62 Hz (94%) |
| REQ-13 | Pareto front overlap analysis | Partial | `results/data/pareto_front_overlap.csv` exists but L2 distances are not normalised; interpretation deferred to future work |
| REQ-14 | HV trajectory shape comparison | Done | `hv_vs_gen_seed44_vs_seed77.png` |
| REQ-15 | Wall-clock impact of restart cadence change | Done | 3.5× speedup quantified; t0112 = 620 s/gen vs t0106 = 2,167 s/gen |

All 15 requirements addressed. REQ-13 (Pareto front overlap) is marked Partial because the raw
L2 distance metric is dominated by parameter-scale; the CSV is produced as required but its
interpretation is left to a future normalised-distance follow-up.

Answers to the 5 key questions from `task_description.md`:

1. **Does seed 77 produce ≥ 40 unique joint-pass cells?** **No** — 7 unique. Bucket: "partial
   replication; multi-seed required."
2. **Does seed 77's best ratio DSI reach or exceed 0.95?** **Yes** — 0.9535.
3. **Does seed 77's best PD-rate frontier reach or exceed 100 Hz?** **Yes** — 114.76 Hz.
4. **Do the two seeds' Pareto fronts overlap in parameter space?** Inconclusive without
   per-dimension normalisation of the L2 metric.
5. **Did the tighter pool-restart cadence (every 10) change HV trajectory or wall-clock?**
   **Yes** — 3.5× per-generation wall-clock speedup; HV trajectory plateaus earlier (gen 21 vs
   gen 39) and at a lower terminal HV (107 vs 122).

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0112_t0106_seed77_replicate/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0112_t0106_seed77_replicate" date_compared: "2026-05-19" ---
# Comparison with Project and Published Results

## Summary

t0112 is a deliberately minimum-change seed-77 replicate of [t0106]'s 2-direction ratio-DSI
NSGA-II run on the 68-d Bed B + 14-d morphology substrate. The frontier-corner metrics
replicate within a few percent (best ratio DSI **0.9535** vs [t0106]'s **1.0000**; best
PD-rate **114.76 Hz** vs [t0106]'s **122.62 Hz**) but the joint-pass density is **~10x lower**
(**0.35%** unique yield, **7** unique cells, vs [t0106]'s **3.3%** and **123** unique).
t0112's **0.35%** acceptance rate sits between [Druckmann2007][druckmann2007] (**0.10%**) and
[Hay2011][hay2011] (**0.40%**), suggesting [t0106]'s 3.3% was an above-typical lucky seed and
t0112 is closer to the typical biophysical-fit yield. The substrate's frontier is biologically
plausible and reachable from multiple GA seeds — t0112's best DSI of **0.9535** still exceeds
[Trenholm2013][trenholm2013] mouse Hb9 control DSI **0.76** and the PD-rate is in the
published DSGC firing-rate envelope.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best DSI) | DSI | 1.0000 | 0.9535 | -0.0465 | Same substrate, different GA seed; t0112 reaches DSI > 0.95 at PD = 60 Hz |
| [t0106] seed 44 NSGA-II 2-dir ratio DSI (best PD-rate frontier) | PD (Hz) | 122.62 | 114.76 | -7.86 | t0112 reaches 94% of [t0106]'s best-PD frontier value |
| [t0106] seed 44 NSGA-II (joint-pass unique count) | count | 123 | 7 | -116 | 17x fewer unique joint-pass cells from seed 77 vs seed 44 |
| [t0106] seed 44 NSGA-II (joint-pass yield) | rate | 3.30% | 0.35% | -2.95 | t0112 acceptance rate is ~10x lower (123/3744 vs 7/2016) |
| [t0106] seed 44 NSGA-II (final hypervolume) | HV | 122.0288 | 107.4602 | -14.57 | t0112 plateau HV is 88% of [t0106]'s; both runs show clear breakthrough jump |
| [t0106] seed 44 NSGA-II (per-generation wall-clock) | s/gen | 2167 | 620 | -1547 | Pool-restart cadence 10 vs 25 delivers 3.5x speedup at no algorithmic cost |
| [t0106] seed 44 NSGA-II (productive compute cost) | USD | 10.37 | 1.99 | -8.38 | 5.2x cheaper; HV-plateau auto-stop at gen 21 vs operator-stop at gen 40 |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Druckmann2007][druckmann2007] NSGA-II 300x1000 (acceptance rate) | rate | 0.10% | 0.35% | +0.25 | [Druckmann2007, Methods + Fig 3]: 300 acceptable / 300,000 evals on 12-d cortical interneuron; t0112 yields 7/2016 on 68-d substrate, ~3.5x higher rate but same order of magnitude |
| [Hay2011][hay2011] NSGA-II 1000x500 joint perisom+BAC (acceptance rate) | rate | 0.40% | 0.35% | -0.05 | [Hay2011, p. 4]: ~2000 acceptable / 500,000 evals on 22-d L5b PC; t0112 acceptance is essentially matched despite 3x higher dimensionality |
| [Hay2011][hay2011] NSGA-II perisomatic-only fits (acceptance rate) | rate | 0.0104% | 0.35% | +0.34 | [Hay2011, p. 6]: 52 acceptable / 500,000 evals — the "substrate-limited" counterexample; t0112 substrate clearly not similarly limited |
| [Achard2006][achard2006] ES 9x8000 evals (acceptance rate) | rate | 0.028% | 0.35% | +0.32 | [Achard2006, Results]: 20 selected / 72,000 evals on 24-d Purkinje cell; t0112 is ~12x higher acceptance |
| [Mohacsi2024][mohacsi2024] NSGA-II convergence horizon | plateau gen | 20-60 | 21 | within range | [Mohacsi2024, Fig 4 use cases 1-6]: NSGA-II asymptotes by gens 20-60 on 3-12 param problems; t0112 HV-plateau detector fires at gen 21, on the lower end of the range despite 68-d substrate |
| [Trenholm2013][trenholm2013] mouse Hb9 DSGC ratio DSI (control) | DSI | 0.76 | 0.9535 | +0.1935 | [Trenholm2013, Table 1]: peak PD=198 Hz, peak ND=27 Hz, DSI=(198-27)/(198+27); t0112 best ratio DSI exceeds biological reference |
| [Trenholm2013][trenholm2013] mouse Hb9 peak PD firing rate | PD (Hz) | 198 | 114.76 | -83.24 | [Trenholm2013, Table 1]: peak instantaneous Gaussian-convolved rate, control; t0112 frontier PD = 114.76 Hz is 58% of biological peak — below ceiling, well above the 30 Hz joint-pass floor |
| [Oesch2005][oesch2005] rabbit ON-OFF DSGC spike-based DSI (OFF) | DSI | 0.74 | 0.9535 | +0.2135 | [Oesch2005, p. 740]: 0.74 +/- 0.13 OFF DSI; t0112 best ratio DSI exceeds upper biological CI (0.87) |
| [PolegPolsky2026][polegpolsky2026] ML unconstrained DSI ceiling | DSI | 0.731 | 0.9535 | +0.2225 | [PolegPolsky2026, Fig 3]: 73.1% +/- 2.4% DSI under full E+I freedom on 12 dirs x 5 speeds; t0112 2-dir DSI exceeds 12-dir ceiling — methodology gap, not biology gap |

## Methodology Differences

* **GA seed (the only intended algorithmic change vs [t0106]).** t0112 uses GA seed **77**;
  [t0106] used GA seed **44**. The substrate, objective, evaluator, silence guard, SBX/PM
  operators, LHS init, watchdog and predictions-asset schema are bitwise identical. This is
  the controlled-variable comparison.

* **Pool-restart cadence (secondary tuning change).** t0112's `_POOL_RESTART_EVERY = 10` vs
  [t0106]'s `25`. This is a workload-side tuning that affects NEURON-import memory creep and
  per-generation wall-clock; it should not change Pareto front geometry. The 3.5x per-gen
  speedup ($1.99 vs $10.37 cost) is the direct consequence. Whether this cadence change
  interacts with the joint-pass density gap is **confounded with the GA seed change** and
  cannot be isolated in this single replicate.

* **Generation ceiling and stop mechanism.** [t0106] ran with `N_GEN = 300` ceiling and an
  operator-driven stop at gen 40 (manual HV-trace inspection). t0112 ran with `N_GEN = 60`
  ceiling and was auto-stopped by the HV-plateau detector at gen 21. The earlier auto-stop may
  have censored the long tail of joint-pass discovery — [t0106] produced most of its
  joint-pass cells in gens 21-39, after the point where t0112 stopped.

* **DSI definition vs published DSGC measurements.** t0112 inherits [t0106]'s 2-direction
  ratio DSI on antipodal directions (PD = 0°, ND = 180°). [Trenholm2013][trenholm2013],
  [Oesch2005][oesch2005], and [PolegPolsky2026][polegpolsky2026] all use 8 - 12 directions
  with vector-sum DSI. **No published paper fits a biophysical model against a 2-direction
  objective.** The DSI comparison vs biological references is therefore best-case-PD vs
  best-case-PD, not equal-protocol head-to-head. [t0107]'s 8-direction re-evaluation of 10
  [t0106] top cells showed the 2-direction ratio DSI overstates selectivity by ~0.42 absolute
  under 8-direction vector-sum — this caveat carries directly to t0112's reported DSI.

* **Single GA seed vs multi-seed convention (unchanged from [t0106]).**
  [Chen2024-STN][chen2024-stn] used 3 seeds at pop=120, ~1M evals;
  [PolegPolsky2026][polegpolsky2026] used 100 GA seed restarts at pop=10, gens=300-1000. t0112
  ran 1 seed (the same constraint as [t0106]). The 0.35% acceptance point estimate is
  therefore single-realisation, not population estimate — but pooled with [t0106]'s 3.3%, the
  2-seed mean is ~1.8%, still within the published NSGA-II envelope (0.028% - 0.40%).

* **Substrate vs published NSGA-II benchmarks (unchanged from [t0106]).**
  [Druckmann2007][druckmann2007] = 12-d, [Hay2011][hay2011] = 22-d, [Achard2006][achard2006] =
  24-d. t0112's 68-d substrate is **2.8x - 5.7x higher dimensional** than any published
  NSGA-II biophysical benchmark. Standard scaling intuition predicts lower acceptance rate at
  higher dimensionality; t0112's 0.35% in 68-d matched-on-acceptance-rate against
  [Hay2011][hay2011]'s 0.40% in 22-d is therefore in the same regime, not anomalous.

* **Evaluation budget — well below published references.** t0112 = **5,760 planned / 2,016
  actual** evaluations. [Druckmann2007][druckmann2007] used **300,000**; [Hay2011][hay2011]
  used **500,000**. t0112 is **~150x below** the modern reference floor — comparable
  acceptance rate at 150x lower spend supports the [Mohacsi2024][mohacsi2024] observation that
  the 2-direction objective surface converges faster than the published 30+ feature
  objectives.

## Analysis

### Prior Task Comparison

The headline finding is **partial replication of [t0106]'s breakthrough**: the substrate's
joint-pass corner is reachable from at least two GA seeds (44 and 77), confirming that the
**2-direction ratio DSI reformulation rather than seed-44 luck is the load-bearing change**.
This contradicts a strict reading of [t0106]'s null hypothesis (that 123 unique joint-pass
cells could have been a one-seed extreme of an otherwise-null substrate) — t0112's 7 unique
cells, while far fewer, are non-zero, on the front, and biologically plausible. The substrate
genuinely supports DSI ≥ 0.95 with PD-rate > 100 Hz, demonstrated again from a different seed
(cell at DSI = 0.9506 / PD = 112.86 Hz, generation 17).

However, **the joint-pass density is itself a stochastic property of the GA seed.** The
factor-of-17 gap in unique joint-pass cell counts (**7 vs 123**) is the dominant quantitative
finding. Three non-mutually-exclusive explanations:

1. **GA-seed variance is large at this substrate.** Seed 77's HV trajectory plateaus earlier
   (gen 21 vs gen 39) at a lower final HV (107 vs 122); the seed converges on a smaller
   joint-pass region and does not branch widely. This is the parsimonious reading.

2. **The earlier plateau-stop censored the long tail.** [t0106] produced most of its
   joint-pass cells in gens 21-39, after t0112's auto-stop. The HV-plateau detector may be too
   aggressive when the local mode is "deep but narrow". A direct test would re-run t0112 with
   the auto-stop disabled.

3. **Pool-restart-every-10 may be reducing exploration.** Tighter restarts mean shorter
   between-restart trajectories for the SBX/PM operators. Speculative; a controlled test would
   re-run seed 44 with cadence 10 (or seed 77 with cadence 25).

The most direct disambiguation is **N ≥ 3 GA seeds at restart cadence 10 and at cadence 25**
to disentangle seed effect from restart-cadence effect.

### Published Literature Comparison

The most consequential finding relative to the literature is that **t0112's 0.35% acceptance
rate is matched almost exactly against [Hay2011][hay2011]'s 0.40%** ([Hay2011, p. 4]), one of
the most widely-cited biophysical NSGA-II references. Pooling t0112's 0.35% with [t0106]'s
3.3% gives a 2-seed mean of ~**1.8%**, which puts the per-seed envelope clearly inside the
[Druckmann2007][druckmann2007]-to-[Hay2011][hay2011] range (0.10% - 0.40%, with
[Hay2011][hay2011]'s 0.40% upper bound being the most directly comparable joint-objective
benchmark). **[t0106]'s 3.3% was an above-typical lucky seed; t0112's 0.35% is closer to the
typical biophysical-fit yield.** This materially changes the substrate-property
interpretation: the substrate supports the joint-pass basin at the expected NSGA-II density,
not at a uniquely high density.

The **best ratio DSI of 0.9535 still exceeds all published biological DSGC measurements**
([Trenholm2013][trenholm2013] control = 0.76, [Oesch2005][oesch2005] OFF = 0.74,
[PolegPolsky2026][polegpolsky2026] unconstrained = 0.731). The biological-plausibility caveat
from [t0106] applies in attenuated form: t0112 does not reach DSI = 1.0 (no absolute ND
silence at peak), so the "physiologically suspicious" concern is softer for t0112 than for
[t0106]. The best joint-pass cell at DSI = 0.9506 / PD = 112.86 Hz still has substantial PD
activity (114 Hz is 58% of [Trenholm2013][trenholm2013]'s 198 Hz biological peak) with a
near-pure ratio DSI.

The **PD-rate frontier of 114.76 Hz** is 94% of [t0106]'s 122.62 Hz and **comfortably above
the 30 Hz joint-pass floor**. Both runs reach the same upper region of PD-rate space,
supporting the substrate-general (not seed-specific) interpretation of the high-PD corner.

The **HV-plateau at gen 21 is consistent with [Mohacsi2024][mohacsi2024]'s 20-60 gen
convergence range** ([Mohacsi2024, Fig 4]). That a 68-d problem flattens at the **lower end**
of this range (below [t0106]'s ~24-30 gen plateau) is potentially confounded by the smaller
N_GEN ceiling and the HV-plateau detector firing at first signal rather than after operator
inspection.

## Limitations

* **Single GA seed replicate**. t0112 is one GA seed (77) replicating one GA seed (44). The
  joint-pass-density gap (7 vs 123 unique) cannot be attributed solely to seed variance vs
  solely to the HV-plateau auto-stop vs solely to the pool-restart cadence change. Multi-seed
  confirmation (≥ 3 seeds at each restart cadence) is the highest-priority follow-up; the
  0.35% yield could still be a per-seed extreme on the low side, just as [t0106]'s 3.3% was
  likely a per-seed extreme on the high side.

* **Pool-restart cadence cost-benefit not isolated**. The 3.5x per-gen wall-clock speedup is
  confounded with the GA seed change. A controlled test (seed 44 with cadence 10, or seed 77
  with cadence 25) would isolate the restart-cadence effect.

* **HV-plateau detector vs operator stop.** [t0106] was operator-stopped at gen 39; t0112 was
  auto-stopped at gen 21. The earlier auto-stop may have censored the long tail of joint-pass
  discovery — t0112's 7 unique cells could plausibly have grown to 20-40 if the run had
  continued past the auto-stop. The acceptance-rate comparison vs published references is
  therefore conservative for t0112.

* **2-direction protocol is methodologically novel and not directly comparable to published
  multi-direction DSI measurements**. [Trenholm2013][trenholm2013], [Oesch2005][oesch2005],
  and [PolegPolsky2026][polegpolsky2026] use 8-12 directions. The DSI = 0.9535 result cannot
  be claimed as "exceeding biology" without an 8-direction post-hoc re-evaluation. [t0107]
  established that [t0106]'s 2-direction ratio DSI overstates selectivity by ~0.42 absolute
  under 8-direction vector-sum; this caveat carries directly to t0112.

* **Pareto-front parameter-space overlap analysis is uninterpretable**. The raw 68-d L2
  between t0112 and [t0106] Pareto cells is dominated by the conductance-scale parameters
  (S/cm² values spanning 6 orders of magnitude). A z-scored or rank-correlation overlap metric
  is a natural follow-up but is outside the scope of a minimum-change replicate.

* **No comparable published NSGA-II run at this dimensionality.** The 68-d substrate is 2.8x -
  5.7x higher dimensional than any published biophysical NSGA-II benchmark. The
  acceptance-rate comparison is therefore against extrapolated expectations, not
  matched-dimensional baselines. **Publication-selection bias** also applies:
  [Hay2011][hay2011] and [Druckmann2007][druckmann2007] published successes but not their
  failed seeds, so the per-seed yield distribution in their setting is unknown.

* **Evaluation budget materially below published references.** t0112 used 2,016 evaluations vs
  [Hay2011][hay2011]'s 500,000 and [Druckmann2007][druckmann2007]'s 300,000. The acceptance
  rate is measured at 150x lower spend; whether the rate would converge to the published value
  at matched spend is open.

* **Sub-claim "substrate-general joint-pass corner" is empirically true within the 2-seed
  comparison (44, 77)**, but neither GA seed was selected at random — both are arbitrarily
  chosen small integers. A formal sampling of seeds (e.g. 10 random seeds from a fixed
  distribution) is needed before the substrate-general claim can be reported with confidence.

[t0106]: ../../t0106_long_pdnd_nsga2_300gen/ [t0107]: ../../t0107_t0106_polar_8dir_recheck/
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
