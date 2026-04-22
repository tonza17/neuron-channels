# ⏹ Plan DSGC morphology + VGC DSI optimisation; estimate Vast.ai GPU budget

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0033_plan_dsgc_morphology_channel_optimisation` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md), [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Task types** | `literature-survey`, `answer-question` |
| **Expected assets** | 1 answer |
| **Task folder** | [`t0033_plan_dsgc_morphology_channel_optimisation/`](../../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/) |

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
