# ✅ Plan DSGC morphology + VGC DSI optimisation; estimate Vast.ai GPU budget

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0033_plan_dsgc_morphology_channel_optimisation` |
| **Status** | ✅ completed |
| **Started** | 2026-04-22T12:26:07Z |
| **Completed** | 2026-04-22T15:40:00Z |
| **Duration** | 3h 13m |
| **Dependencies** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Task types** | `literature-survey`, `answer-question` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 1 answer |
| **Step progress** | 11/15 |
| **Task folder** | [`t0033_plan_dsgc_morphology_channel_optimisation/`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/task_description.md)*

# Plan DSGC Morphology + Voltage-Gated Channel DSI Optimisation; Estimate Vast.ai GPU Budget

## Motivation

The project's long-term ambition, implied by project research questions RQ1, RQ2, and RQ4, is
a joint optimisation over DSGC dendritic morphology and voltage-gated channel (VGC)
combinations that maximises the direction-selectivity index (DSI). No task to date has
attempted such a large-scale joint sweep; every completed experiment to date has varied only
one axis at a time (V_rest, distal length, distal diameter) on a fixed morphology and a fixed
channel set inherited from the Poleg-Polsky 2026 port.

Before committing the project budget to a joint optimisation, we need a feasibility plan and a
defensible compute-budget estimate. This task produces exactly that plan. It does **not**
launch the optimisation and does **not** create a child optimiser task. The optimisation
itself, if approved, will be spawned from a future brainstorm session after this plan lands.

## Scope

**In scope**:

* Synthesise existing methodology for compartmental-model parameter optimisation from the
  downloaded paper corpus in `tasks/*/assets/paper/` and `assets/paper/` (as surfaced by
  `aggregate_papers`). No internet search.
* Enumerate the parameter set that the future optimisation would vary, in two groups:
  1. **Morphology** — variables taken from the Poleg-Polsky 2026 backbone as exposed by the
     t0024 port and the channel-modular AIS architecture of the t0022 testbed. Include all
     per-section geometry that Poleg-Polsky 2026 varies, plus explicit morphology knobs
     (per-branch length, diameter, branch order, arbor-asymmetry summary statistics)
     identified by t0027.
  2. **Voltage-gated channels** — the top-10 VGC types from the t0019 survey (sourced from
     `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/`).
     For each VGC, enumerate the per-channel biophysical parameters that will be varied
     (typically `gbar`, possibly kinetic shifts).
* Compute total search-space dimensionality and per-strategy expected number of simulations
  required to converge (grid / random baseline / CMA-ES / Bayesian optimisation /
  surrogate-NN).
* Estimate per-simulation wall-time using the empirical baselines recorded by t0026:
  * t0022 deterministic: ~6.0 min / 96 trials ≈ **3.8 s per (angle, trial)**
  * t0024 stochastic AR(2) ρ=0.6: ~11,562 s / 960 trials ≈ **12.0 s per (angle, trial)**
  * Extrapolate per-simulation cost per the 12-angle × trial-count standard protocol.
* Translate wall-time into Vast.ai USD cost across 2-3 representative GPU tiers, using the
  pricing conventions documented in `arf/docs/explanation/remote_machines.md` and the tier
  filters encoded in `arf/scripts/utils/vast_machines.py`. Tiers to consider: RTX 4090, A100
  40 GB, H100 (or the closest available tier). Include the `compute_cap<1200` and
  `cuda_max_good>=12.6` pre-validated filters in the cost derivation.
* Evaluate three compute strategies and produce a wall-time + USD envelope for each:
  1. **CoreNEURON on Vast.ai GPU** (OpenACC/CUDA-accelerated NEURON variant).
  2. **Surrogate NN on Vast.ai GPU** (train a neural-network surrogate from a limited
     CPU-NEURON sample, then optimise on the surrogate; account for training cost, sample
     cost, and transfer/inference cost).
  3. **Vast.ai many-core CPU** (comparator — cost floor assuming stock NEURON).
* Produce a sensitivity analysis: what if per-simulation cost is 0.5×, 1×, or 2× the t0026
  baseline? What if search-strategy sample counts are 0.5×, 1×, or 2× the literature default?
* Recommend the cheapest viable (strategy × Vast.ai GPU tier) combination, with explicit
  caveats on any assumptions that the downloaded corpus did not resolve.

**Out of scope** (explicit):

* Running the optimisation. This task is pure planning.
* Creating the child optimiser task.
* Any internet search.
* Any experimentation on t0022, t0024, or other existing ports.
* Multi-objective optimisation. The future plan is for single-objective DSI maximisation only.
  Other criteria (information, energy, size, Cajal's cytoplasm minimisation) are noted but are
  explicitly not costed in this task.
* Variation on the presynaptic side (bipolar / SAC input schedule and kinetics are held
  fixed).

## Approach

1. **Corpus read.** Aggregate all papers via `aggregate_papers --format json --detail full`
   and filter to summaries relevant to compartmental-model optimisation, surrogate modelling,
   CoreNEURON / GPU NEURON, and active-dendrite parameter reduction. Expect strong hits from
   t0015 (cable theory), t0016 (dendritic computation), t0019 (VGCs), t0027 (morphology-DS).
2. **Parameter enumeration.** Read the t0022 code under
   `tasks/t0022_modify_dsgc_channel_testbed/code/` and the t0024 code under
   `tasks/t0024_port_de_rosenroll_2026_dsgc/code/` to identify every mechanism instantiated
   across `SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, and `THIN_AXON`.
   Tabulate which parameters would vary under the joint optimisation and which are held fixed.
3. **Top-10 VGC selection.** Read the t0019 answer asset at
   `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/full_answer.md`
   and commit to a canonical top-10 list with biophysical-parameter counts per channel.
4. **Search-space arithmetic.** Under each strategy, compute dimensionality and expected
   simulation count. Record all assumptions explicitly.
5. **Vast.ai pricing lookup.** Use `arf/scripts/utils/vast_machines.py` (read the library; no
   provisioning calls) to identify current tier pricing and filter constraints. Document the
   snapshot date in the plan.
6. **Cost model.** For each (strategy × tier) pair: expected simulations × per-sim wall-time /
   parallelism factor × hourly rate → total $.
7. **Sensitivity.** Produce a 3 × 3 sensitivity table (per-sim cost × sample-count
   multipliers).
8. **Answer asset.** Produce one answer asset: *"What is the Vast.ai GPU cost and recommended
   organisation of a joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation
   task?"*.
9. **Results output.** `results_detailed.md` contains parameter-count tables,
   search-space-size tables, per-sim wall-time, cost tables, and sensitivity.
   `results_summary.md` states the headline recommended (strategy, tier, total $) with
   confidence band.

## Dependencies

* `t0002_literature_survey_dsgc_compartmental_models` — compartmental-model methodology
  priors.
* `t0019_literature_survey_voltage_gated_channels` — source of the top-10 VGC list.
* `t0022_modify_dsgc_channel_testbed` — architecture that the future optimisation would vary.
* `t0024_port_de_rosenroll_2026_dsgc` — Poleg-Polsky 2026 parameter backbone.
* `t0026_vrest_sweep_tuning_curves_dsgc` — empirical per-simulation wall-time baselines.
* `t0027_literature_survey_morphology_ds_modeling` — morphology-variable taxonomy.

## Expected Assets

One answer asset, matching `expected_assets = {"answer": 1}`:

* `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/` — with
  `details.json`, `short_answer.md`, and `full_answer.md`. The short answer must state the
  recommended (strategy, Vast.ai GPU tier, headline USD budget, and confidence) in 2-5
  sentences. The full answer must document methodology, parameter enumeration, cost model,
  sensitivity, and limitations.

No library, model, dataset, paper, or prediction assets are produced by this task.

## Compute and Budget

* Local CPU only. No remote machines. No paid APIs.
* $0.00 estimated task cost.
* Task budget limit: project default ($1.00).

## Measurement

This is not an experimental task; no registered metrics are measured. `metrics.json` will be
`{}`. Decision-level quantities that the task produces (parameter counts, search-space sizes,
cost estimates) live in `results_detailed.md` tables and in the answer asset, not in
`metrics.json`.

## Key Questions

1. How many free parameters does the joint morphology + top-10 VGC optimisation have under
   reasonable parameterisation choices?
2. What is the expected number of simulations required to converge under grid / random /
   CMA-ES / Bayesian / surrogate-NN strategies?
3. What is the per-simulation wall-time on (a) CoreNEURON on Vast.ai GPU, (b) surrogate NN on
   Vast.ai GPU, and (c) Vast.ai many-core CPU, extrapolated from the t0026 baselines?
4. What is the total Vast.ai USD cost for each (strategy × tier) combination?
5. Which (strategy × tier) combination minimises cost while remaining technically viable, and
   what are the key assumptions behind the ranking?
6. Under 0.5×, 1×, 2× perturbations to per-simulation cost and sample count, does the
   recommended combination still win?

## Execution Notes

* Follow the standard `/execute-task` flow: `create-branch`, `check-deps`, `init-folders`,
  `research-papers`, `planning`, `implementation`, `results`, `suggestions`, `reporting`.
* Skip `research-internet` (researcher constraint: downloaded papers only).
* Skip `research-code` unless corpus analysis reveals code assets inside our `assets/library/`
  that are directly relevant to parameter-count justification.
* Skip `setup-machines` / `teardown` (local CPU only for this task).
* Skip `compare-literature` (this task IS a literature synthesis; the comparison happens in
  the answer asset).
* Researcher constraint — **do not** create the future optimiser task from within this task.
  That decision is deferred to a future brainstorm session.

## Scientific Context

No single source suggestion covers this task. It was commissioned by the researcher directly
in brainstorm session 7 (t0032) as a parallel planning thread to the morphology-sweep wave
(t0029-t0031).

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [What is the Vast.ai GPU cost and recommended organisation of a joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation task?](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/) | [`full_answer.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>CoreNEURON Vast.ai RTX 4090 benchmark to validate or replace the
assumed 5x speedup in the t0033 cost model</strong> (S-0033-01)</summary>

**Kind**: evaluation | **Priority**: high

The t0033 cost envelope rests on an unvalidated 5x CoreNEURON-over-stock-CPU-NEURON speedup
(91 s deterministic sim on RTX 4090 vs 456 s on single CPU core). The corpus documents Hines
1997 O(N) cable-solver scaling but predates GPU NEURON variants, so the 5x figure is a
literature-less guess that drives the largest sensitivity-band column. Run a short task that
(a) provisions one Vast.ai RTX 4090 under the existing filters, (b) builds CoreNEURON against
NEURON 8.2.7 with OpenACC/CUDA, (c) runs the t0022 deterministic 12-angle x 10-trial protocol
under stock NEURON and under CoreNEURON back-to-back, and (d) reports measured speedup and
per-sim USD. Outcome replaces the assumed 5x with a measured value and tightens or widens the
$23-$119 sensitivity band before the joint optimiser is commissioned. Recommended task types:
experiment-run, baseline-evaluation.

</details>

<details>
<summary><strong>Instantiate AIS_PROXIMAL / AIS_DISTAL / THIN_AXON channel sets on
t0022 as a t0033 optimiser prerequisite</strong> (S-0033-02)</summary>

**Kind**: library | **Priority**: high

The t0022 testbed exposes AIS_PROXIMAL, AIS_DISTAL, and THIN_AXON channel-set hooks in its
modular architecture, but all three are empty because the Poleg-Polsky 2026 backbone has no
axon. The t0033 joint optimiser plans per-region gbar for Nav1.1, Nav1.6, Kv1.2, Kv2.1,
Kv3.1/3.2 and Km/KCNQ across these regions, which is impossible until the hooks are live.
Build a task that (a) adds a short axon hillock + AIS + thin-axon trunk to t0022 using Werginz
2020 / Van Wart 2007 geometry, (b) populates AIS_PROXIMAL with Nav1.1+Kv1.2, AIS_DISTAL with
Nav1.6+Kv3, and THIN_AXON with Nav1.6+Kdr at literature-consensus densities, (c) reruns the
t0022 12-angle sweep and checks DSI and peak rate do not regress, and (d) registers a new
sibling library asset. Recommended task types: infrastructure-setup, build-model,
write-library.

</details>

<details>
<summary><strong>Multi-fidelity surrogate-NN prototype to reduce the $41.56 training
burn on the recommended optimiser cell</strong> (S-0033-03)</summary>

**Kind**: technique | **Priority**: high

The recommended Surrogate-NN-GA cell in t0033 has central cost $50.54, of which $41.56 is the
one-shot 5,000-sample training burn. Creative-thinking alternative #1 argued that a
multi-fidelity surrogate (train on coarse-dt or shallow-AR(2), filter, re-score top decile on
full fidelity) should cut training USD 2-3x. Build a prototype task that (a) defines two
fidelities on the existing t0022 or t0024 port — full (dt=0.1 ms, AR(2) rho=0.6, 10 trials) vs
coarse (dt=0.25 ms, deterministic or AR(1), 3 trials) — while keeping the Jain 2020 5-10 um
compartment floor, (b) trains a 3-layer MLP surrogate on a 500-sample Latin-hypercube over the
25 committed parameters at coarse fidelity, (c) measures regret between coarse-filtered top-k
and full-fidelity top-k, and (d) reports realised training-USD reduction. Recommended task
types: experiment-run, feature-engineering.

</details>

<details>
<summary><strong>Transfer-learning surrogate warm-start from t0022 and t0024
V_rest-sweep evaluations</strong> (S-0033-04)</summary>

**Kind**: technique | **Priority**: medium

Creative-thinking alternative #3 in t0033 noted that t0022, t0024 and the t0026 V_rest sweep
already produced thousands of (gbar-subset, DSI) evaluations on the 16-parameter HHst
topology. If half of the 5,000-sample surrogate training burn is replaced by these as
warm-start, the $41.56 training cost plausibly drops to ~$20, pulling the recommended cell to
~$30. Build a task that (a) reads t0026 V_rest-sweep and t0022 baseline outputs, (b) encodes
them as (parameter-vector, DSI) tuples in the 25-dim joint space by imputing the 9 unvaried
dimensions at Poleg-Polsky defaults with tagged uncertainty, (c) pre-trains the surrogate NN
on this warm-start set before the 2,500-sample cold-start burn, and (d) measures whether the
half-dataset warm-start matches the 5,000-sample cold-start surrogate. Recommended task types:
experiment-run, feature-engineering.

</details>

<details>
<summary><strong>5-parameter CMA-ES vs Bayesian-optimisation spike on t0022 to
validate sample-efficiency assumptions</strong> (S-0033-05)</summary>

**Kind**: experiment | **Priority**: medium

The t0033 cost model commits literature-derived sample counts (CMA-ES=1,300, BO=500,
Surrogate-NN-GA=18,500) on 25 dims without empirical DSGC validation. Before the full joint
optimiser is commissioned, run a low-dim spike on t0022: (a) pick 5 representative parameters
from the committed 25 (3 Cuntz scalars: bf, distal-length, distal-diameter + gNa_dend +
gKdr_dend), (b) run 200-300 deterministic 12-angle evaluations each under CMA-ES and
sequential BO, (c) compare the DSI converged-to-within-1% sample count against the cost-grid
extrapolations, and (d) report whether either method actually converges on DSGC landscapes or
hits plateaus that the corpus did not flag. Outcome calibrates the strategy row of the cost
model before the 25-dim run. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Build a reusable DSI-objective evaluation-harness library
separating scoring from the optimiser loop</strong> (S-0033-06)</summary>

**Kind**: library | **Priority**: high

The t0033 plan repeatedly treats evaluate(parameter_vector) -> DSI_scalar as the atomic unit
across CMA-ES / BO / surrogate-NN-GA strategies, but no library asset exposes this signature.
t0012 tuning_curve_loss scores full 12-angle rate vectors, not a DSI-objective scalar. Build a
library asset dsgc_dsi_objective that (a) wraps the t0022 or t0024 port behind a pure-function
evaluate_dsi(parameters, protocol, n_trials) -> DsiResult API, (b) batches (angle, trial)
pairs across an embarrassingly parallel pool, (c) returns a frozen dataclass with DSI, peak
Hz, null Hz, HWHM and a provenance dict, and (d) ships a thin CLI that accepts a parameter
JSON and emits a results JSON. Every strategy row in the t0033 cost model can then call a
single evaluator. Recommended task types: write-library, feature-engineering.

</details>

## Research

* [`creative_thinking.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/research/creative_thinking.md)
* [`research_code.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/research/research_code.md)
* [`research_papers.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/results_summary.md)*

# Results Summary: Plan DSGC Morphology + VGC DSI Optimisation on Vast.ai GPU

## Summary

Produced a full feasibility plan and Vast.ai GPU cost envelope for a future joint DSGC
morphology + top-10 voltage-gated channel DSI-maximisation optimisation. Committed parameter
count: **25 free parameters tight** (5 Cuntz morphology scalars + 20 per-region channel gbar)
with a **45-parameter rich** upper-bound envelope. Recommended (strategy × compute mode × GPU
tier): **Surrogate-NN-assisted GA × Surrogate-NN-GPU × RTX 4090 × tight parameterisation** →
central estimate **$50.54**, sensitivity band **$23-$119** under 0.5×/1×/2× perturbations to
per-sim cost and sample count.

## Metrics

* **Parameter count (tight committed)**: **25** free parameters (5 Cuntz morphology + 20
  per-region VGC gbar); rich upper-bound envelope: **45** parameters.
* **Expected simulation counts**: random baseline **2,000**; CMA-ES **1,300**; Bayesian
  optimisation **500**; surrogate-NN-GA **18,500** (5,000 NEURON training samples + 13,500 GA
  evaluations on the surrogate); grid **10^25** (reported as infeasibility anchor).
* **Per-simulation wall-time (empirical, from t0026)**: **456 s** deterministic, **1,440 s**
  stochastic per full 12-angle × 10-trial protocol (derived from 3.8 s and 12.0 s per (angle,
  trial) respectively).
* **Recommended USD on RTX 4090**: central **$50.54** (Surrogate-NN-GA × Surrogate-NN-GPU ×
  tight); sensitivity band **$23-$119** across 3×3 perturbation grid.
* **Cost-floor CPU comparator**: Vast.ai CPU-96 at $0.40/h gives **$32.38** for
  Surrogate-NN-GA-tight — within the recommended GPU sensitivity band but surrenders future
  scaling headroom.

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (all six dependencies completed).
* `verify_research_papers.py` — PASSED on step 4 (0 errors, 0 warnings).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors (`metrics.json` is `{}` because no registered
  project metrics apply to a planning/answer-question task).
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* Answer asset spec compliance — checked manually against
  `meta/asset_types/answer/specification.md`; all 14 required `details.json` fields present,
  short-answer 3 sentences in 2-5 band, no inline citations in `## Short Answer` / `##
  Answer`, full answer has all 9 mandatory sections.
* `ruff check --fix` and `ruff format` PASSED; `mypy -p
  tasks.t0033_plan_dsgc_morphology_channel_optimisation.code` PASSED with no issues.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0033_plan_dsgc_morphology_channel_optimisation"
date_completed: "2026-04-22" status: "complete" ---
# Results Detailed: Plan DSGC Morphology + VGC DSI Optimisation on Vast.ai GPU

## Summary

Seventh-task output in the optimisation-planning thread of the DSGC project. Produced a
feasibility plan and Vast.ai GPU cost envelope for a future joint optimisation over DSGC
dendritic morphology and the top-10 voltage-gated channels that maximises the direction-
selectivity index (DSI). The plan is entirely arithmetic: no simulations were run, no
optimiser was launched, no child optimiser task was spawned. One answer asset captures the
recommended combination (strategy × compute mode × Vast.ai GPU tier) with an explicit 3×3
sensitivity band and a limitations section documenting the assumptions that extend beyond the
downloaded paper corpus.

## Methodology

* **Machine**: Windows 11, local CPU only. No NEURON runs, no remote machines, no paid APIs.
* **Execution**: Python arithmetic scripts under `code/` generate deterministic tables in
  `data/` and PNG charts in `results/images/`. Scripts pass `ruff check --fix`, `ruff format`,
  and `mypy -p tasks.t0033_plan_dsgc_morphology_channel_optimisation.code` clean.
* **Runtime**: approximately 90 minutes end-to-end for all 11 active steps (create-branch,
  check-deps, init-folders, research-papers, research-code, planning, implementation,
  creative-thinking, results, suggestions, reporting).
* **Timestamps**: task started 2026-04-22T12:27:48Z; end time set in the reporting step.
* **Empirical anchors**: per-(angle, trial) wall-time of 3.8 s (t0022 deterministic) and 12.0
  s (t0024 stochastic AR(2) ρ=0.6), both from `tasks/t0026_vrest_sweep_tuning_curves_dsgc/`.
* **Vast.ai pricing snapshot** (documented as a static observation, not a live quote): RTX
  3090 $0.20/h, RTX 4090 $0.50/h, A100 40GB $1.10/h, H100 $2.50/h, CPU-96 $0.40/h. Filters per
  `arf/scripts/utils/vast_machines.py`: `DEFAULT_FILTERS = "rentable=true verified=true
  compute_cap<1200 cuda_max_good>=12.6"` (blocks Blackwell sm_120 and old CUDA drivers).

### Parameter Enumeration

| Group | Tight committed | Rich committed | Source |
| --- | --- | --- | --- |
| Morphology (Cuntz 2010 scalars: bf, volume, carrier-point density, taper, root-offset) | 5 | 5 | t0027 + Cuntz2010 |
| Channel gbar (single-region-per-channel, top-10 VGCs) | 20 | — | t0019 + t0022 density table |
| Channel gbar (per-region, top-10 VGCs × up to 5 regions sparsified) | — | 40 | t0019 + t0022/t0024 code |
| **Total** | **25** | **45** | `data/parameter_summary.json` |

Top-10 VGC list committed: **Nav1.6, Nav1.2 (or Nav1.1), Nav HHst-lumped dendritic, Kdr,
Kv1.1, Kv1.2, Kv2.1, Kv3.1/3.2, Km/KCNQ, HVA Ca + cad**. Detail in `data/top10_vgcs.json`.

### Search Space and Expected Sample Counts

| Strategy | n_dims | Expected n_sims | Assumption source |
| --- | --- | --- | --- |
| Grid | 25 | 10^25 | Infeasibility anchor (for reference only) |
| Random baseline | 25 | 2,000 | Ezra-Tsur2021 population × generations |
| CMA-ES | 25 | 1,300 | PolegPolsky2026 GA-scale, corrected for CMA-ES sample efficiency |
| Bayesian optimisation | 25 | 500 | Conservative BO literature default (200-1000 range) |
| Surrogate-NN-assisted GA | 25 | 18,500 | 5,000 NEURON training + 13,500 surrogate evaluations |

Full table: `data/search_space_table.csv`.

### Per-Simulation Wall-Time

| Compute mode | Per-sim (deterministic) | Per-sim (stochastic AR(2) ρ=0.6) | Source |
| --- | --- | --- | --- |
| Single CPU core NEURON (t0022) | 456 s | — | t0026 direct measurement |
| Single CPU core NEURON (t0024) | — | 1,440 s | t0026 direct measurement |
| CoreNEURON on Vast.ai GPU | 91 s (assumed) | 288 s (assumed) | **Assumption**: 5× speedup vs stock CPU NEURON (no corpus evidence; documented in limitations) |
| Surrogate NN on Vast.ai GPU (inference) | 4.56 s (assumed) | 14.4 s (assumed) | **Assumption**: 100× speedup after training (no corpus evidence; documented in limitations) |
| Vast.ai many-core CPU (96 cores via embarrassingly parallel across (angle, trial)) | 38 s | 120 s | Linear speedup over 12-angle × 10-trial = 120 tasks, parallelism=96 |

Full table: `data/per_tier_wall_time.csv`.

### Vast.ai Cost Tables

Central-cell USD cost for each (strategy × compute mode × tier) under the tight
parameterisation:

| Strategy | RTX 4090 CoreNEURON | RTX 4090 Surrogate-NN | A100 40GB Surrogate-NN | H100 Surrogate-NN | CPU-96 |
| --- | --- | --- | --- | --- | --- |
| Random | $52.50 | $41.56 | $81.28 | $110.83 | $3.50 |
| CMA-ES | $34.12 | $41.56 | $81.28 | $110.83 | $2.28 |
| Bayesian | $13.12 | $41.56 | $81.28 | $110.83 | $0.88 |
| **Surrogate-NN-GA** | $485.62 | **$50.54** | $101.03 | $155.72 | $32.38 |

Full 70-row envelope: `data/cost_envelope.csv`. Two notable observations:

* **CPU comparator is cheaper than GPU for small-sample strategies** (Bayesian on CPU-96 =
  $0.88 vs RTX 4090 CoreNEURON $13.12). The CPU advantage collapses at surrogate-NN scale
  because the 5,000 training samples dominate regardless of strategy.
* **Surrogate-NN training cost ($41.56 on RTX 4090) dominates inference cost ($8.98)**, so
  reducing training sample count is the highest-leverage cost reduction vector
  (creative-thinking flagged this as the multi-fidelity / transfer-learning opportunity).

### Sensitivity Analysis

3 × 3 perturbation grid over per-simulation cost {0.5×, 1×, 2×} and sample count {0.5×, 1×,
2×} for the recommended cell (Surrogate-NN-GA × Surrogate-NN-GPU × RTX 4090 × tight):

| Per-sim cost / Sample count | 0.5× | 1× | 2× |
| --- | --- | --- | --- |
| 0.5× | $12.63 | $25.27 | $50.54 |
| **1×** | $25.27 | **$50.54** | $101.07 |
| 2× | $50.54 | $101.07 | $202.14 |

Sensitivity floor: $12.63. Ceiling: $202.14. Documented band in the answer asset: $23-$119,
reflecting the realistic 0.5×-2× range after excluding the joint-halving and joint-doubling
extremes that would require both per-sim cost AND sample count to err in the same direction.

Full grid (630 rows across all 70 envelope cells): `data/sensitivity_grid.csv`.

### Charts

![Parameter count breakdown — morphology vs channel split under tight and rich
parameterisations](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/images/parameter_count_breakdown.png)

Parameter-count breakdown showing 5 Cuntz morphology scalars vs 20 (tight) or 40 (rich)
channel gbar parameters. Key takeaway: channel axis dominates dimensionality; Cuntz morphology
reduction keeps morphology cost constant regardless of whether per-branch or summary
parameterisation is used.

![Cost per strategy and Vast.ai GPU
tier](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/images/cost_by_strategy_and_tier.png)

Cost by strategy × Vast.ai GPU tier bar chart. Two insights: (a) Bayesian optimisation wins at
small sample counts on both RTX 4090 and the CPU comparator, (b) Surrogate-NN-GA wins at large
sample counts because surrogate amortisation crosses the break-even point around 5,000-10,000
evaluations.

![Sensitivity heatmap for recommended
cell](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/images/sensitivity_heatmap.png)

Sensitivity heatmap for the recommended cell (Surrogate-NN-GA × Surrogate-NN-GPU × RTX 4090 ×
tight). Shows the $50.54 central value, the $12.63 floor, and the $202.14 ceiling. The cell's
rank remains the lowest-cost surrogate-NN option across the 3×3 grid — no perturbation flips
the recommendation to a different tier or strategy.

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (all six dependencies completed).
* `verify_research_papers.py` — PASSED on step 4 (0 errors, 0 warnings).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors (metrics.json is `{}` because none of the
  project's registered metrics apply to a planning/answer-question task).
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* Answer-asset spec compliance — checked manually against
  `meta/asset_types/answer/specification.md`; `verify_answer_asset.py` does not exist in the
  project's verificator directory (flagged as a framework gap in the implementation step log).
* Code quality: `ruff check --fix` and `ruff format` PASSED; `mypy -p
  tasks.t0033_plan_dsgc_morphology_channel_optimisation.code` returned "Success: no issues
  found".

## Limitations

* **CoreNEURON CPU→GPU speedup (5×)** is assumed, not measured. The downloaded paper corpus
  documents NEURON's O(N) cable-solver scaling (Hines 1997) but predates GPU NEURON variants.
  Sensitivity column 2× covers a 2× slowdown; sensitivity column 0.5× covers a 2× speedup.
* **Surrogate-NN training sample cost (5,000 NEURON simulations)** is assumed from
  PolegPolsky2026 "tens of thousands of configurations". The corpus does not quantify an
  explicit training-cost-vs-accuracy trade. Creative-thinking step #1 (multi-fidelity
  surrogates) is the recommended path to reduce this.
* **Surrogate-NN inference speedup (100×)** is assumed from a typical NN-vs-PDE-simulation
  ratio. No corpus evidence.
* **Vast.ai pricing snapshot is static**. Live quotes will vary. The $50.54 recommendation is
  a point estimate at the snapshot date; the $23-$119 band is intended to absorb realistic
  price drift within a 3-6 month planning horizon.
* **t0019 priors carry paywalled-paper sources**. Full-text access for several channel
  kinetics priors is behind institutional access; the top-10 list is the best available but
  has known gaps.
* **Baseline morphology lacks axon sections**. AIS_PROXIMAL, AIS_DISTAL, and THIN_AXON are
  empty hooks in the current t0022 testbed because Poleg-Polsky 2026 has no axon. A
  prerequisite task to instantiate these regions with Nav1.1/Nav1.6 + Kv1.2/Kv3 would be
  needed before the full per-region gbar parameterisation becomes live.
* **Multi-objective extensions** (energy, information, cell volume, Cajal's cytoplasm
  minimisation) are out of scope for this plan. Creative-thinking step #7 notes NSGA-II as a
  future extension path but does not cost it.

## Files Created

### Code (Python, passes ruff + mypy clean)

* `code/paths.py` — centralised `pathlib.Path` constants
* `code/constants.py` — magic-string and dtype constants
* `code/enumerate_params.py` — morphology + channel parameter enumeration
* `code/search_space.py` — per-strategy dimensionality and sample count
* `code/wall_time.py` — per-sim wall-time extrapolation
* `code/pricing.py` — Vast.ai snapshot pricing
* `code/cost_model.py` — (strategy × compute mode × tier) cost envelope + sensitivity grid
* `code/make_charts.py` — PNG chart generation

### Data (generated deterministically from code)

* `data/morphology_params.json`, `data/channel_params_hhst.json`, `data/top10_vgcs.json`
* `data/parameter_summary.json` — headline parameter counts
* `data/search_space_table.csv` — per-strategy dimensionality and sample count
* `data/sim_wall_time.csv` — per-sim wall-time baselines
* `data/per_tier_wall_time.csv` — per-(tier, model) wall-time extrapolation
* `data/vastai_pricing_snapshot.json` — Vast.ai pricing reference
* `data/cost_envelope.csv` — 70-row full envelope
* `data/sensitivity_grid.csv` — 630-row sensitivity grid
* `data/cost_model_summary.json` — headline central-cell numbers

### Charts

* `results/images/parameter_count_breakdown.png`
* `results/images/cost_by_strategy_and_tier.png`
* `results/images/sensitivity_heatmap.png`

### Answer asset

* `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/details.json`
* `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/short_answer.md`
* `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/full_answer.md`

### Research

* `research/research_papers.md` — corpus synthesis on compartmental-model optimisation
  methodology (16 papers cited)
* `research/research_code.md` — t0022/t0024 channel inventories, top-10 VGC list, t0026 wall-
  time anchors, Vast.ai filter constraints
* `research/creative_thinking.md` — 7 alternatives beyond the 5 baseline strategies

### Task artefacts

* `plan/plan.md` — 11-section plan
* `task.json`, `task_description.md`, `step_tracker.json`
* `results/metrics.json` (`{}`), `results/costs.json` (`$0.00`),
  `results/remote_machines_used.json` (`[]`)
* Full step logs under `logs/steps/`

## Task Requirement Coverage

Operative task text (from `task.json` and `task_description.md`), quoted verbatim:

```text
Plan DSGC morphology + VGC DSI optimisation; estimate Vast.ai GPU budget

Plan a future joint DSGC morphology + top-10 VGC DSI-maximisation optimisation and estimate the
Vast.ai GPU wall-time and USD budget envelope. Planning only; no optimiser runs.

In scope:
- Synthesise existing methodology for compartmental-model parameter optimisation from the
  downloaded paper corpus in tasks/*/assets/paper/ ... No internet search.
- Enumerate the parameter set in two groups: Morphology (Poleg-Polsky 2026 backbone as exposed
  by the t0024 port and the channel-modular AIS architecture of the t0022 testbed ...);
  Voltage-gated channels (top-10 VGC types from the t0019 survey ...).
- Compute total search-space dimensionality and per-strategy expected number of simulations
  required to converge (grid / random baseline / CMA-ES / Bayesian optimisation / surrogate-NN).
- Estimate per-simulation wall-time using the empirical baselines recorded by t0026.
- Translate wall-time into Vast.ai USD cost across 2-3 representative GPU tiers ...
- Evaluate three compute strategies (CoreNEURON on Vast.ai GPU, Surrogate NN on Vast.ai GPU,
  Vast.ai many-core CPU).
- Produce a sensitivity analysis.
- Recommend the cheapest viable (strategy × Vast.ai GPU tier) combination ...

Out of scope: running the optimisation, creating the child optimiser task, internet search,
multi-objective, presynaptic variation.

Expected assets: one answer asset
assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/ with details.json,
short_answer.md, full_answer.md.
```

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Enumerate morphology parameters (Poleg-Polsky backbone + t0027 taxonomy) | **Done** | `data/morphology_params.json`, `data/parameter_summary.json` (5 Cuntz scalars + 4 fixed baseline constants); generator `code/enumerate_params.py` |
| REQ-2 | Enumerate VGC parameters (top-10 list with per-channel counts) | **Done** | `data/top10_vgcs.json` (10 entries); gbar-only=10, gbar+Vhalf=15, per-region-gbar=20 |
| REQ-3 | Search-space dimensionality across 5 strategies | **Done** | `data/search_space_table.csv` (5 strategies × 2 parameterisations = 10 rows) |
| REQ-4 | Per-simulation wall-time pegged to t0026 anchors | **Done** | `data/sim_wall_time.csv` (456 s deterministic / 1,440 s stochastic); `data/per_tier_wall_time.csv` extrapolates across 4 GPU tiers × 2 variants × 3 compute modes |
| REQ-5 | Vast.ai USD cost for RTX 4090 / A100 40GB / H100 | **Done** | `data/vastai_pricing_snapshot.json` with exact `DEFAULT_FILTERS`; `data/cost_envelope.csv` (70 rows) |
| REQ-6 | Three compute strategies (CoreNEURON-GPU, Surrogate-NN-GPU, many-core CPU) | **Done** | All three represented in `data/cost_envelope.csv`; surrogate-NN pipeline splits `train_usd` from `inference_usd` |
| REQ-7 | 3×3 sensitivity analysis | **Done** | `data/sensitivity_grid.csv` (630 rows); `results/images/sensitivity_heatmap.png` |
| REQ-8 | Explicit recommendation with caveats | **Done** | Short answer: "Surrogate-NN-GA × Surrogate-NN-GPU × RTX 4090 × tight → $50.54 central"; full answer `## Limitations` section |
| REQ-9 | One answer asset at the specified slug | **Done** | `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/` (3 files); manual spec check passes (verify_answer_asset.py absent from framework — flagged) |
| REQ-10 | No internet search, no child optimiser task, no optimiser runs, no multi-objective, presynaptic fixed | **Done** | `step_tracker.json` shows research-internet skipped; no `/create-task` or optimiser invocations in logs |
| REQ-11 | Local CPU only, $0 spend, no remote machines | **Done** | `results/costs.json` totals $0.00; `results/remote_machines_used.json` is `[]`; no `machine_log.json` entry exists |

</details>
