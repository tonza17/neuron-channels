---
spec_version: "2"
task_id: "t0033_plan_dsgc_morphology_channel_optimisation"
date_completed: "2026-04-22"
status: "complete"
---
# Plan: DSGC Morphology + Voltage-Gated Channel DSI Optimisation — Vast.ai Budget Envelope

## Objective

Produce a feasibility-and-cost design document for a **future** joint optimisation over DSGC
dendritic morphology and the top-10 voltage-gated channels (VGCs) that maximises the
direction-selectivity index (DSI), priced on Vast.ai GPU. This task is **planning only** — no
optimiser is launched, and no child optimiser task is created. The deliverable is one answer asset
stating the recommended (search strategy × GPU tier × total USD) combination with a defensible
sensitivity band, plus supporting parameter-count, per-simulation wall-time, and cost tables in
`results_detailed.md`. "Done" means: the answer asset exists with a populated short/full answer,
parameter counts and cost tables are reproducible from scripted enumerators in `code/`, the
sensitivity grid is populated for 3 cost multipliers × 3 sample-count multipliers, the two
verificators (`verify_plan` for this step, `verify_answer_asset` for the deliverable) run with zero
errors, and the plan's recommendation is traceable back to the t0026 empirical wall-time anchors and
the `vast_machines.py` speed-tier table without any internet search.

## Task Requirement Checklist

Operative text from `tasks/t0033_plan_dsgc_morphology_channel_optimisation/task_description.md`
(quoted verbatim):

```text
Plan a future joint DSGC morphology + top-10 VGC DSI-maximisation optimisation and estimate the
Vast.ai GPU wall-time and USD budget envelope. Planning only; no optimiser runs.

In scope:
* Synthesise existing methodology for compartmental-model parameter optimisation from the
  downloaded paper corpus ... No internet search.
* Enumerate the parameter set ... Morphology (Poleg-Polsky 2026 backbone + t0027 taxonomy);
  Voltage-gated channels (top-10 from t0019 with per-channel biophysical parameters).
* Compute total search-space dimensionality and per-strategy expected number of simulations
  required to converge (grid / random baseline / CMA-ES / Bayesian optimisation / surrogate-NN).
* Estimate per-simulation wall-time using the empirical baselines recorded by t0026
  (~3.8 s deterministic, ~12.0 s AR(2) stochastic per (angle, trial)).
* Translate wall-time into Vast.ai USD cost across 2-3 representative GPU tiers ... Tiers to
  consider: RTX 4090, A100 40 GB, H100.
* Evaluate three compute strategies: CoreNEURON on Vast.ai GPU, Surrogate NN on Vast.ai GPU,
  Vast.ai many-core CPU.
* Produce a sensitivity analysis (per-sim cost 0.5x / 1x / 2x; sample count 0.5x / 1x / 2x).
* Recommend the cheapest viable (strategy x Vast.ai GPU tier) combination, with explicit caveats.

Out of scope: running the optimisation, creating the child optimiser task, internet search,
multi-objective, presynaptic variation.

Expected assets: one answer asset
`assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/` with details.json,
short_answer.md, full_answer.md.
```

Concrete requirements extracted and keyed for traceability:

* **REQ-1** Enumerate morphology parameters — Poleg-Polsky 2026 backbone (per t0024 `build_cell.py`
  and `constants.py`) plus the 8-variable t0027 morphology-DS taxonomy (length, branch count, branch
  order, diameter, arbor asymmetry, input spatial layout, input kinetic tiling, transfer
  resistance). Deliverable: a table of morphology knobs with whether each is varied (free) or held
  fixed. **Satisfied by Steps 1, 3, and 4.** Evidence: `code/enumerate_params.py` output table in
  `results_detailed.md`.
* **REQ-2** Enumerate VGC parameters — the canonical top-10 VGC list (Nav1.6, Nav1.2 / Nav1.1, Nav
  HHst-lumped dendritic, Kdr HHst-lumped, Kv1.1, Kv1.2, Kv2.1, Kv3, Km/KCNQ, HVA Ca + cad) with
  per-channel free-parameter counts under three parameterisations (gbar-only, gbar+V_half,
  per-region gbar). **Satisfied by Steps 2 and 4.** Evidence: a VGC parameter table (channel ×
  region × free param) committed in `results_detailed.md`.
* **REQ-3** Compute search-space dimensionality across five search strategies: grid, random
  baseline, CMA-ES, Bayesian optimisation, surrogate-NN-assisted gradient-free (evolutionary).
  **Satisfied by Steps 5 and 6.** Evidence: per-strategy dimensionality + expected-simulation-count
  table.
* **REQ-4** Peg per-simulation wall-time to t0026 empirical anchors (3.8 s deterministic t0022, 12.0
  s stochastic AR(2) t0024 per (angle, trial); 7.6 min/sim and 24 min/sim respectively under the
  12-angle × 10-trial standard). **Satisfied by Steps 7 and 8.** Evidence: a wall-time table in
  `results_detailed.md`.
* **REQ-5** Translate wall-time × `vast_machines.GPU_SPEED_TIERS` ratios into Vast.ai USD cost for
  three GPU tiers: RTX 4090 (speed 1.60, ~\$0.50/h median historical), A100 40 GB (speed 1.80), H100
  (speed 3.00). Respect `DEFAULT_FILTERS` =
  `rentable=true verified=true compute_cap<1200 cuda_max_good>=12.6`. **Satisfied by Steps 8, 9, and
  10.** Evidence: cost tables in `results_detailed.md`.
* **REQ-6** Evaluate three compute strategies — CoreNEURON-on-Vast.ai-GPU, Surrogate-NN-on-
  Vast.ai-GPU, Vast.ai many-core CPU — with a wall-time + USD envelope for each. Surrogate-NN must
  budget training sample cost separately from inference. **Satisfied by Step 10.** Evidence:
  three-strategy cost envelope in `results_detailed.md` plus rationale text.
* **REQ-7** Produce a 3 × 3 sensitivity table for per-sim-cost multiplier (0.5×, 1×, 2×) crossed
  with sample-count multiplier (0.5×, 1×, 2×) per strategy × tier. **Satisfied by Step 11.**
  Evidence: a 3 × 3 × (strategies × tiers) sensitivity grid image + CSV in
  `results/images/sensitivity_heatmap.png` and `results_detailed.md`.
* **REQ-8** Recommend the cheapest viable (strategy × tier) combination with explicit caveats
  (unvalidated CoreNEURON speedup, unquantified surrogate economics, paywalled t0019 priors, missing
  axon sections in baseline morphology). **Satisfied by Steps 10, 12, and 13.** Evidence:
  `assets/answer/<slug>/short_answer.md` headline recommendation; `full_answer.md` caveats section.
* **REQ-9** Produce exactly one answer asset at
  `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/` with
  `details.json`, `short_answer.md`, `full_answer.md`, matching `expected_assets = {"answer": 1}`.
  **Satisfied by Steps 13 and 14.** Evidence: the three files exist and pass
  `verify_answer_asset.py`.
* **REQ-10** Constraint: no internet search anywhere in this task; no child optimiser task creation;
  no optimiser runs; no multi-objective formulation; presynaptic side held fixed; downloaded paper
  corpus only. **Enforced across all steps 1-14** by the absence of any internet-search step, any
  child-task creation, and any optimiser invocation. Evidence: orchestrator logs show no
  `research_internet` step and no `create-task` invocation.
* **REQ-11** Constraint: this task runs local CPU only, \$0 spend, no remote machines. **Stated in
  `## Cost Estimation` and `## Remote Machines`** and held by every numbered step (no step
  provisions remote compute). Evidence: `costs.json` totals \$0.00 and no `machine_log.json` entry
  exists.

## Approach

### Technical approach grounded in research findings

The plan's arithmetic sits on top of four hard empirical inputs assembled by the prior tasks:

1. **t0026 wall-time anchors**: 3.8 s per (angle, trial) on the t0022 deterministic testbed, 12.0 s
   per (angle, trial) on the t0024 stochastic AR(2) ρ=0.6 port, both single-threaded NEURON 8.2.7 on
   a Windows workstation. Under the canonical 12-angle × 10-trial protocol this is ~7.6 min/sim and
   ~24 min/sim respectively. Hyperpolarised V_rest adds a modest surcharge (1,403-1,581 s per V_rest
   level at t0024). Reported in `tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/`.
2. **t0022 + t0024 channel topology**: five `SectionList` regions (`SOMA_CHANNELS`, `DEND_CHANNELS`,
   `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON`) declared in
   `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc`. The t0024 port already
   inserts HHst + cad on soma / primary / non-terminal / terminal dendrite with four lumped gbar
   parameters per region (gNa, gKdr, gKm, gleak) = 16 free gbar parameters before any new VGC is
   introduced. AIS_PROXIMAL / AIS_DISTAL / THIN_AXON are empty in the baseline morphology because
   Poleg-Polsky 2026 has no axon.
3. **t0019 top-10 VGC set**: five canonical priors (Nav1.6 distal AIS, Nav1.2/1.1 proximal AIS, Nav
   HHst dendritic, Kdr, Kv1.1, Kv1.2, Kv2.1, Kv3 optional, Km/KCNQ, HVA Ca + cad) with per-channel
   free-parameter count 1-3 depending on parameterisation. t0019 does not publish a literal numbered
   top-10, but the synthesis in
   `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/full_answer.md`
   plus the t0022 channel-density research internet table produces the canonical 10-entry list.
4. **`vast_machines.py` cost model**: `GPU_SPEED_TIERS` table (RTX 3090=1.00, RTX 4090=1.60, A100
   40=1.80, A100 80=2.00, H100=3.00, H200=3.50), `DEFAULT_FILTERS`
   `"rentable=true verified=true compute_cap<1200 cuda_max_good>=12.6"`, and `rank_offers()` sorting
   by `(est_hours, price_per_hour)` with a ±20% speed tolerance. Provisioning constants
   `MAX_RETRY_OFFERS=3`, `POLL_INTERVAL_SECONDS=30`, `CREATION_TIMEOUT_SECONDS=600`.
   Checkpoint/heartbeat overhead kicks in at the 2-hour cliff per
   `arf/specifications/remote_machines_specification.md`.

On top of these the plan applies the methodology defaults converged across the paper corpus:

* **Default search strategy**: gradient-free evolutionary search (GA / NSGA-II) with population
  100-200, generations 20-45, crossover/mutation 0.4, multi-seed ≥3, per Ezra-Tsur 2021 and
  Poleg-Polsky 2026. Surrogate-NN acceleration is the corpus's documented speedup path (Poleg-Polsky
  2026 "tens of thousands of configurations"), with surrogate training burning O(10^3-10^4) NEURON
  evaluations — quantified only qualitatively in the Poleg-Polsky 2026 summary, so carried as an
  assumption with explicit sensitivity band.
* **Morphology reduction**: reduce morphology axis to 3-5 Cuntz scalars (spanning volume,
  carrier-point density, balancing factor `bf ∈ [0.2, 0.7]`, root location, optional per-cell taper)
  per Cuntz 2010, rather than per-branch geometry. This caps morphology at O(10^4-10^5) grid points
  even under coarse discretisation.
* **Channel reduction**: hold V_half and kinetic τ at the Fohlmeister-Miller / Van Wart / Kole / Hu
  literature values; vary only gbar per (region, channel). Top-10 VGCs × up to 5 regions, sparsified
  by the t0019 priors, yields ~15-25 region-channel gbar parameters.
* **Active-dendrite floor**: per Schachter 2010, passive-dendrite configurations cap DSI, so the
  optimiser's bounds must enforce a hard floor on dendritic gNa + gKdr. This is a planning
  constraint stated in the answer asset, not a code change in this task.
* **Discretisation floor**: `d_lambda < 0.1`, hundreds of compartments minimum (Mainen 1996,
  Schachter 2010, Ezra-Tsur 2021). The optimiser may not coarsen morphology to accelerate.

Committed plan parameters:

* **Free-parameter count for cost arithmetic**: tight parameterisation = **~25 free parameters** (5
  Cuntz morphology scalars + ~20 region-channel gbar parameters under single-region-per-channel
  top-10 assignment). Rich parameterisation sensitivity = **~45 free parameters** (5 Cuntz + ~40
  region-channel under per-region gbar) for upper-bound envelope.
* **Search strategies compared**: grid, random baseline, CMA-ES, Bayesian optimisation (BO), and
  surrogate-NN-assisted GA (the Poleg-Polsky 2026 template). Grid is included as an
  infeasibility-anchor (it is catastrophic for ~25 dimensions); random baseline is the no-assumption
  floor; CMA-ES / BO are sanity-checks against the GA default; surrogate-NN is the target strategy.
* **GPU tiers compared**: RTX 4090, A100 40 GB, H100. RTX 3090 is carried implicitly as the
  reference tier (speed 1.00).
* **Sensitivity grid**: 3 × 3 over per-sim cost multiplier {0.5, 1, 2} and sample-count multiplier
  {0.5, 1, 2}, tabulated for every (strategy × tier) cell the plan recommends.
* **Answer asset slug**: `vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation`.

### Alternatives considered

* **Collapse morphology to a fixed Poleg-Polsky backbone, sweep channels only.** Rejected because
  Mainen 1996 shows morphology alone reshapes firing with fixed channels, and
  [PolegPolsky2026]/[Schachter2010] together establish morphology-biophysics coupling. The
  researcher's explicit goal is *joint* morphology + channel DSI maximisation.
* **Sweep per-branch length/diameter as free parameters (O(100-1000) dims).** Rejected: Cuntz 2010
  shows morphology reduces cleanly to 3-5 scalars that recover real arbors within a few percent. A
  100-dim per-branch sweep is neither tractable nor scientifically informative when a 3-5-scalar
  generative model exists.
* **Gradient-based optimisation (autodiff through NEURON).** Rejected: no corpus precedent exists
  for autodiff-through-NEURON on a DSGC model, the DSI objective is non-smooth (spike counts
  thresholded), and CoreNEURON does not expose reverse-mode gradients. GA/surrogate-NN remains the
  corpus-justified default.
* **Multi-objective (DSI + information + energy + Cajal cytoplasm).** Out of scope per
  `task_description.md`. Carried as a future-task suggestion only.
* **Vary presynaptic inputs (bipolar / SAC kinetics).** Out of scope per `task_description.md`; held
  fixed per researcher constraint. Corpus precedent (Ezra-Tsur 2021) supports keeping input kinetics
  fixed while sweeping cell-intrinsic parameters.

### Task types

`task.json` declares `task_types = ["literature-survey", "answer-question"]`. Both apply:

* `literature-survey` Planning Guidelines: no new paper downloads are needed (the prior tasks supply
  the corpus). The "synthesis document in `results/results_summary.md`" guideline is handled by the
  orchestrator's `results` step, not by this plan. The corpus-only constraint maps directly to the
  REQ-10 no-internet rule.
* `answer-question` Planning Guidelines drive the concrete implementation contract: exactly one
  answer asset, question text stable enough to become canonical, explicit evidence channels (paper
  corpus, code inspection, arithmetic), stopping criterion = the 3 × 3 sensitivity grid is populated
  and the recommendation is stable under the 1× column. Uncertainty reporting = explicit caveats
  section in `full_answer.md`.

## Cost Estimation

* **Compute**: \$0.00. This task performs only code reading, arithmetic, and document assembly on
  the local Windows workstation. No simulations are run.
* **Paid APIs**: \$0.00. No LLM API calls, no Vast.ai provisioning (only a code read of
  `arf/scripts/utils/vast_machines.py`; no live `vastai search offers` calls).
* **Remote machines**: \$0.00. `task_description.md` explicitly forbids remote machines for this
  task.
* **Storage / egress**: \$0.00. Outputs are a handful of markdown, JSON, CSV, and PNG files.
* **Total**: **\$0.00**, well under the per-task \$1.00 limit and the \$1.00 project budget in
  `project/budget.json`. Reasoning: planning / literature synthesis task; no experiments.

The Vast.ai USD estimates generated *inside* the plan (~\$10-\$10,000 envelopes for different
strategy × tier combinations) refer to the **future** optimiser task's cost. They live in the answer
asset and `results_detailed.md`, not in this task's `costs.json`.

## Step by Step

### Milestone 1: Parameter enumeration (REQ-1, REQ-2)

1. **Create the scripted parameter enumerator.** Create `code/enumerate_params.py`. Import
   `SOMA_CHANNELS`, `DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON` region names as
   string constants defined inline (we do not import HOC-level objects in a CPU-only planning
   script). Read (via `Path(...).read_text()`, no code execution)
   `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` and
   `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` to enumerate the 16 baseline HHst
   gbar parameters (gNa, gKdr, gKm, gleak × 4 tiers: soma / primary / non-terminal / terminal
   dendrite). Read `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc` to
   enumerate the 5 `SectionList` regions. Output a `MorphologyParam` dataclass list (name, region,
   tier, default value, units, source tag, is_free bool) and a `ChannelParam` dataclass list with
   the same schema for lumped HHst channels. Input: those three files. Output:
   `code/parameters/morphology_params.json` and `code/parameters/channel_params_hhst.json`. Expected
   observable: two JSON files with ~16 channel entries and 4-8 morphology entries. Satisfies REQ-1.

2. **Extract the top-10 VGC list from t0019.** Extend `code/enumerate_params.py` with a function
   `load_top10_vgcs()` that reads
   `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/full_answer.md`
   as text and compiles the canonical 10-entry VGC list from the numbered channels in
   research_code.md (Nav1.6, Nav1.2/1.1, Nav-HHst-dend, Kdr-HHst, Kv1.1, Kv1.2, Kv2.1, Kv3, Km/KCNQ,
   HVA Ca + cad). The list is hard-coded as a `TOP10_VGCS: list[VGCRecord]` in the script because
   the t0019 answer is prose, not a structured list — document this synthesis rule inline with a
   comment linking to the `## Top-10 VGC Selection from t0019` section of `research_code.md`. Each
   `VGCRecord` carries channel name, primary region, secondary region (or None), free-parameter
   count under each of three parameterisations (gbar-only=1, gbar+V_half=2, per-region-gbar=2-5),
   and a paper citation key. Input: the t0019 full answer markdown. Output:
   `code/parameters/top10_vgcs.json` and a printed summary table to stdout. Expected observable: 10
   JSON objects, total VGC parameter count ranging 10 (gbar-only, single-region) → 20 (gbar-only,
   two regions) → 40+ (rich). Satisfies REQ-2.

3. **Add the Cuntz morphology axis.** Extend `code/enumerate_params.py` with a hard-coded
   `CUNTZ_PARAMS: list[MorphologyParam]` capturing the 5 Cuntz 2010 scalars (spanning volume in μm³,
   carrier-point density in pts/μm³, balancing factor `bf ∈ [0.2, 0.7]`, root location (categorical:
   soma / offset), optional taper tweak). Tag each with source="Cuntz2010,
   t0027_literature_survey_morphology_ds_modeling". Append to the morphology params JSON. Expected
   observable: morphology_params.json now has 4-8 fixed/baseline entries + 5 Cuntz entries = ~10-15
   rows, of which 5 are free. Satisfies REQ-1.

4. **Run the enumerator and commit the table.** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0033_plan_dsgc_morphology_channel_optimisation -- uv run python -u code/enumerate_params.py`.
   The script prints three summary tables to stdout and writes the three JSON files. Expected
   observable: stdout shows total free parameter counts for tight parameterisation (~25) and rich
   parameterisation (~45); a run log lands in `logs/steps/<step-id>/`. Satisfies REQ-1, REQ-2.

### Milestone 2: Search-space arithmetic (REQ-3)

5. **Compute per-strategy expected simulation counts.** Create `code/search_space.py`. Define the
   five strategies as a `SearchStrategy` enum: `GRID`, `RANDOM`, `CMA_ES`, `BAYESIAN`,
   `SURROGATE_NN_GA`. For each strategy, implement a function
   `expected_simulations(n_dims: int, strategy: SearchStrategy) -> SimulationBudget` where
   `SimulationBudget` is a frozen dataclass with fields
   `(n_samples_lower, n_samples_central, n_samples_upper, assumption_text, source_citation)`. Use
   the following corpus-grounded rules:
   * `GRID`: `10**n_dims` (infeasibility anchor; no corpus precedent for n_dims>5).
   * `RANDOM`: central = 2000 samples for n_dims≤30; lower = 500; upper = 10000 (no-assumption
     baseline; generic MC convergence).
   * `CMA_ES`: `lambda = 4 + floor(3 * log(n_dims))` per Hansen's default, generations = 100;
     central = `lambda * 100` = ~1800 for n_dims=25; lower = 0.5×; upper = 2×.
   * `BAYESIAN`: central = 500 evaluations (Gaussian-process BO scales poorly above ~30 dims); lower
     = 200; upper = 1000. Flagged as unvalidated on DSGC models in the corpus — see
     `## Gaps and Limitations` in `research_papers.md`.
   * `SURROGATE_NN_GA`: population 100-200 × generations 20-45 × multi-seed ≥3 → central ≈ 10,000
     NEURON-backed evaluations (the Ezra-Tsur 2021 × Poleg-Polsky 2026 synthesis), of which ~5000
     train the surrogate and ~5000 validate the candidates the surrogate proposes. Lower 5000, upper
     50,000. Input: `code/parameters/*.json`. Output: `code/search_space/search_space_table.csv`
     with columns `strategy`, `n_dims`, `n_samples_lower`, `n_samples_central`, `n_samples_upper`,
     `assumption_text`, `source_citation`. Expected observable: a 5-row CSV showing that grid for
     n_dims=25 is infeasible (~10^25), and surrogate-NN is the only strategy that scales to rich
     parameterisation. Satisfies REQ-3.

6. **Record dimensionality for tight and rich parameterisations.** Extend `code/search_space.py`
   with a `main()` that computes the table once at `n_dims=25` (tight) and once at `n_dims=45`
   (rich) and writes both to `code/search_space/search_space_table.csv` with an extra column
   `parameterisation ∈ {"tight", "rich"}`. Expected observable: a 10-row CSV. Run via
   `run_with_logs`. Satisfies REQ-3.

### Milestone 3: Wall-time extrapolation (REQ-4)

7. **Extract t0026 wall-time anchors and compute per-sim extrapolations.** Create
   `code/wall_time.py`. Read (text read, no execution) the t0026 results artefacts under
   `tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/` (the detailed results markdown and the
   `metrics.json` file already published by that task). Hard-code the two empirical anchors as
   module-level constants:
   * `T0022_DETERMINISTIC_SECONDS_PER_ANGLE_TRIAL: float = 3.8`
   * `T0024_STOCHASTIC_AR2_SECONDS_PER_ANGLE_TRIAL: float = 12.0` Define
     `@dataclass(frozen=True, slots=True) class SimWallTime: model_variant: str; n_angles: int; n_trials: int; seconds_per_angle_trial: float; total_seconds: float; total_minutes: float`.
     Under the 12-angle × 10-trial canonical protocol this gives ~456 s (7.6 min) for t0022 and
     ~1440 s (24 min) for t0024 per candidate morphology-channel vector. Output
     `code/wall_time/sim_wall_time.csv`. Expected observable: a 2-row CSV. Satisfies REQ-4.

8. **Apply GPU speed-tier scaling.** Extend `code/wall_time.py` with a function
   `scale_by_gpu_tier(base_seconds: float, tier_name: str) -> float` that reads
   `arf.scripts.utils.vast_machines.GPU_SPEED_TIERS` (direct import — it is a framework constant,
   not a task asset). Assume CoreNEURON delivers a literature placeholder **5×** CPU→GPU speedup at
   the RTX 3090 reference tier (justification: stated as an external assumption; no corpus
   evidence), then scales linearly by `speed_tier_ratio`. Compute per-tier per-sim wall-time for RTX
   3090, RTX 4090, A100 40 GB, H100. Surrogate-NN inference wall-time is assumed 100× faster than
   NEURON (another external assumption, flagged). CPU many-core is modelled as
   `base_seconds / min(96, n_cores_available)` where n_cores_available = 96 (default large-CPU
   Vast.ai offer). Output: `code/wall_time/per_tier_wall_time.csv`. Expected observable: a table
   with columns (strategy, tier, per_sim_seconds, assumption). Satisfies REQ-4.

### Milestone 4: Vast.ai pricing snapshot (REQ-5)

9. **Snapshot tier pricing without live provisioning.** Create `code/pricing.py`. **Do not call any
   Vast.ai live API.** Hard-code a pricing table grounded in `vast_machines.GPU_SPEED_TIERS` and
   reasonable median historical rates (document the snapshot date `2026-04-22` inline and the source
   as "vast.ai historical market observation; not a live quote"):
   * RTX 3090 ~ \$0.20 / GPU-h median.
   * RTX 4090 ~ \$0.50 / GPU-h median.
   * A100 40 GB ~ \$1.10 / GPU-h median.
   * H100 PCIe ~ \$2.50 / GPU-h median.
   * 96-core CPU-only offer ~ \$0.40 / node-h median. Emit
     `code/pricing/vastai_pricing_snapshot.json` with fields
     `(tier, dollars_per_hour, speed_tier_ratio, snapshot_date, filters_applied, source)`.
     `filters_applied` = the `vast_machines.DEFAULT_FILTERS` string
     `"rentable=true verified=true compute_cap<1200 cuda_max_good>=12.6"`. Expected observable: a
     5-row JSON array. Satisfies REQ-5.

### Milestone 5: Cost model and strategy envelopes (REQ-5, REQ-6)

10. **Compute cost envelopes per (strategy × tier).** Create `code/cost_model.py`. Load the outputs
    of steps 5, 8, 9. For each (strategy ∈ {GRID, RANDOM, CMA_ES, BAYESIAN, SURROGATE_NN_GA} ×
    compute_mode ∈ {CORENEURON_GPU, SURROGATE_NN_GPU, MANY_CORE_CPU} × tier ∈ {RTX_4090, A100_40GB,
    H100}) cell compute:
    * `total_sim_seconds = n_samples_central * per_sim_seconds(tier, compute_mode)`
    * `wall_hours = total_sim_seconds / 3600`
    * `effective_wall_hours = wall_hours * checkpoint_overhead_multiplier` where
      `checkpoint_overhead_multiplier = 1.05` when `wall_hours > 2` (30-min checkpoint + 5-min
      heartbeat per `arf/specifications/remote_machines_specification.md`) else `1.00`.
    * `usd_total = effective_wall_hours * dollars_per_hour(tier)`. For SURROGATE_NN_GPU, split
      `usd_total` into `training_usd` (for the 5000-eval surrogate train on t0022 deterministic) and
      `inference_usd` (for the GA on the trained surrogate at the 100× speedup assumption). For
      MANY_CORE_CPU, use the CPU node price (\$0.40/h) and the 96-core parallelism divisor; ignore
      the GPU speed-tier. Output: `code/cost_model/cost_envelope.csv`. Expected observable: a
      ~30-row CSV that shows CoreNEURON- on-H100 dominates many-core-CPU in wall-time but not in
      dollars-per-simulation; surrogate-NN- on-A100 minimises USD at the central cell. Satisfies
      REQ-5, REQ-6.

### Milestone 6: Sensitivity analysis (REQ-7)

11. **Generate the 3 × 3 sensitivity grid.** Extend `code/cost_model.py` with a function
    `sensitivity_grid(base_envelope: pd.DataFrame, cost_multipliers: tuple[float, ...] = (0.5, 1.0, 2.0), sample_multipliers: tuple[float, ...] = (0.5, 1.0, 2.0)) -> pd.DataFrame`.
    For each (strategy × compute_mode × tier × cost_mult × sample_mult), compute the scaled USD
    estimate. Output: `code/cost_model/sensitivity_grid.csv` (wide format), plus
    `code/cost_model/sensitivity_heatmap.png` — a 3 × 3 heatmap per recommended (strategy ×
    compute_mode × tier) rendered with matplotlib. Expected observable: a PNG and a CSV; the heatmap
    for the recommended cell shows the USD envelope spans ~4× (top-left to bottom-right cell).
    Satisfies REQ-7.

### Milestone 7: Assemble the answer asset (REQ-8, REQ-9)

12. **Render markdown-table fragments from the CSVs and copy the heatmap image.** Create
    `code/render_tables.py`. The script reads each CSV produced by Steps 1-11 and emits one
    self-contained markdown fragment per table into `code/tables/`: `morphology_table.md`,
    `vgc_table.md`, `search_space_table.md`, `wall_time_table.md`, `cost_envelope_table.md`,
    `sensitivity_table.md`. Also copy `code/cost_model/sensitivity_heatmap.png` (produced in Step
    11\) into `results/images/sensitivity_heatmap.png` so the orchestrator's downstream results step
    can embed it. Expected observable: 6 markdown fragments in `code/tables/` and one PNG in
    `results/images/`. Do not write any orchestrator-owned files in this step — those are handled by
    the downstream orchestrator stages. Satisfies REQ-5, REQ-7.

13. **[CRITICAL] Create the answer asset.** Create
    `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/` with three files:
    * `details.json` — per `meta/asset_types/answer/specification.md` v2. `answer_id` =
      `vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation`. Question text = *"What is the
      Vast.ai GPU cost and recommended organisation of a joint DSGC morphology + top-10
      voltage-gated channel DSI-maximisation task?"*. `answer_methods` =
      `["literature", "code_inspection", "arithmetic"]`. `short_answer_path` = `short_answer.md`.
      `full_answer_path` = `full_answer.md`. Categories =
      `["compartmental-modeling", "direction-selectivity", "voltage-gated-channels"]`. Source
      citations = the 16 papers cited in `research/research_papers.md` plus task IDs for the six
      dependencies. Confidence = `medium`.
    * `short_answer.md` — 2-5-sentence direct recommendation starting with the recommended
      (strategy, tier, total USD range). No inline `[AuthorYear]` or `[tNNNN]` citations in the
      `## Answer` section.
    * `full_answer.md` — mini-paper structure: question restatement, methodology (parameter
      enumeration, search-space arithmetic, wall-time extrapolation, pricing snapshot, cost model,
      sensitivity), results (all the tables from step 12 summarised), `## Limitations` (paywalled
      t0019 priors, unvalidated CoreNEURON speedup, unquantified surrogate economics, missing axon
      sections in baseline morphology, pricing snapshot is not a live quote, corpus has zero
      GPU-NEURON references), `## Sources` with reference-link definitions for every paper and task
      ID. Inline citations allowed in body sections but forbidden in `## Short Answer`. Expected
      observable: three files in the asset folder. Satisfies REQ-8, REQ-9.

14. **Verify the answer asset.** Run
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0033_plan_dsgc_morphology_channel_optimisation -- uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation`.
    Expected observable: stdout reports 0 errors. Address warnings or document why they are
    accepted. Satisfies REQ-9.

### Notes on validation gates

This task runs **no** paid APIs and **no** large-scale data processing — every step operates on JSON
/ CSV files with at most ~30 rows and a handful of PNG charts. The Step by Step above therefore does
not trigger the "expensive operation" validation-gate clause of the plan specification. The
preflight checks instead focus on:

* After step 4, inspect `code/parameters/*.json` by eye and confirm the free-parameter counts match
  the expected ~25 (tight) / ~45 (rich) bands before running step 5.
* After step 7, confirm `sim_wall_time.csv` matches the hand-arithmetic 3.8 × 12 × 10 = 456 s (~7.6
  min) and 12.0 × 12 × 10 = 1440 s (24 min) exactly, to ~0.1 s tolerance.
* After step 9, inspect `vastai_pricing_snapshot.json` and confirm the snapshot date, the filters
  string verbatim, and the five tier rows.
* After step 11, open `sensitivity_heatmap.png` and confirm that the central (1×, 1×) cell matches
  the cost value printed for the recommended (strategy, tier) cell in step 10's stdout.

### Metric coverage

No registered metric in `meta/metrics/` applies to this task. The four registered metrics
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) all measure the outcome of a NEURON simulation; this task runs no NEURON
simulations, and `task_description.md` § Measurement explicitly states `metrics.json` will be `{}`.
Parameter counts, simulation counts, and USD estimates live in the downstream results artefacts and
the answer asset, not in `metrics.json`. This is a deliberate omission, not an oversight.

## Remote Machines

None required. The task runs entirely on the local Windows workstation (Sheffield CICS Dell
OptiPlex, NEURON 8.2.7 installed but **not invoked**). Every step is a file read / parse /
arithmetic / write, bounded by a few seconds of CPU time per script. `task_description.md`
explicitly forbids remote machines for this task and forbids any Vast.ai provisioning call (step 9
only reads `arf/scripts/utils/vast_machines.py` as a library; it does not call `rank_offers()`
against a live API).

## Assets Needed

Input assets (all already present in the repository — no downloads required):

* **Paper corpus** — the 16 papers cited in `research/research_papers.md`, hosted under
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`,
  `tasks/t0015_literature_survey_cable_theory/assets/paper/`,
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/`,
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/`,
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/`,
  `tasks/t0010_hunt_missed_dsgc_models/assets/paper/`.
* **t0019 answer asset** —
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/full_answer.md`.
  Source of the top-10 VGC list.
* **t0022 code** — `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc`,
  `tasks/t0022_modify_dsgc_channel_testbed/code/constants.py`.
* **t0024 code** — `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py`,
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py`.
* **t0026 wall-time results** —
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_detailed.md`,
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/metrics.json`.
* **Framework module** — `arf/scripts/utils/vast_machines.py`. Provides `DEFAULT_FILTERS`,
  `GPU_SPEED_TIERS`, `RELIABILITY_THRESHOLDS`, `rank_offers()`, `_estimate_hours()`. Imported
  directly as a library.
* **Remote-machines spec** — `arf/specifications/remote_machines_specification.md` and
  `arf/docs/explanation/remote_machines.md`. Reference for the 2-hour checkpointing cliff and
  instance-label convention.

No external downloads, no dataset assets, no model assets needed.

## Expected Assets

The task produces exactly **one** answer asset, matching `task.json`
`expected_assets = {"answer": 1}`:

* **Answer asset** `vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation` —
  `tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/`
  with `details.json`, `short_answer.md`, `full_answer.md`. The short answer states the recommended
  (strategy, Vast.ai GPU tier, headline USD budget, confidence) in 2-5 sentences. The full answer
  documents methodology, parameter enumeration, search-space arithmetic, cost model, sensitivity
  grid, and limitations. Question text: *"What is the Vast.ai GPU cost and recommended organisation
  of a joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation task?"*.

No library, dataset, paper, model, predictions, or additional answer assets are produced.

## Time Estimation

* Milestone 1 (parameter enumeration, steps 1-4): ~45 min wall-clock — 3 scripts totalling ~300
  lines, driven by text-read of t0022, t0024, t0019 artefacts.
* Milestone 2 (search-space arithmetic, steps 5-6): ~30 min — one script, 5 strategies × 2
  parameterisations = 10 cells.
* Milestone 3 (wall-time extrapolation, steps 7-8): ~30 min — one script importing
  `vast_machines.GPU_SPEED_TIERS`, 2 anchors × 4 tiers.
* Milestone 4 (pricing snapshot, step 9): ~20 min — hard-coded table plus JSON emission.
* Milestone 5 (cost model, step 10): ~45 min — one script, ~30 rows.
* Milestone 6 (sensitivity grid, step 11): ~30 min — pandas broadcasting + matplotlib heatmap.
* Milestone 7 (answer asset + verification, steps 12-14): ~90 min — results_detailed table
  fragments, three asset files, two verificator runs.

Total implementation wall-clock: **~5 hours** on the local Windows workstation, plus ~1 hour for
orchestrator steps (results summary, suggestions, reporting) handled outside this plan. Research
phase is already complete (24 papers reviewed, 16 cited in `research_papers.md`; 8 prior tasks
reviewed in `research_code.md`).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| CoreNEURON speedup assumption (5× over CPU at RTX 3090) is wrong by >2× and flips the tier ranking | High | Recommendation in answer asset becomes misleading; future optimiser over-spends | Flag the assumption explicitly in `## Limitations`; report cost envelope at 0.5×, 1×, 2× of that speedup; recommend conservative fallback (many-core CPU) if sensitivity inverts the ranking |
| Surrogate-NN training cost (5000 NEURON evals) is wrong by an order of magnitude | Medium | Surrogate strategy USD estimate off by >4× | Report both 1000-eval and 50000-eval surrogate training bands per Poleg-Polsky 2026 qualitative statement; document as a medium-priority follow-up to re-read the Poleg-Polsky 2026 PDF for specific surrogate economics |
| Vast.ai median tier prices (snapshot 2026-04-22) drift >30% before the optimiser runs | Medium | Absolute USD numbers go stale even if rankings hold | Label prices clearly as "snapshot; not a live quote"; recommend re-snapshotting via `vast_machines.search_offers` before the optimiser provisions |
| Baseline Poleg-Polsky morphology has no axon, yet the plan's channel axis includes AIS_PROXIMAL / AIS_DISTAL / THIN_AXON gbar parameters | High | The planned optimiser cannot set AIS gbar values because those sections don't exist in the backbone | Flag explicitly in `## Limitations`; state that adding axon sections is a prerequisite implementation task ("axon construction") that must land before the optimiser, not inside it |
| t0019 top-10 VGC priors come from paywalled papers plus training-knowledge overlays (Kv3 / KCNQ / Ca) | Medium | Channel-axis parameter count and default bounds are under-evidenced | Carry t0019's caveat into `## Limitations`; recommend a paper-download follow-up task for the five paywalled sources before the optimiser commits gbar bounds |
| `vast_machines.py` provisioning constants (MAX_RETRY_OFFERS=3, CREATION_TIMEOUT_SECONDS=600) are insufficient for long optimiser runs | Low | Individual sim runs fail to provision, optimiser stalls | Plan recommends budgeting ≥3 retry attempts per expected-failure provisioning and committing heartbeat + checkpoint per the 2-hour cliff |
| Grid / Bayesian / CMA-ES sample-count formulae lack DSGC-specific validation | Medium | Per-strategy simulation counts off by a factor of 2-3 | Sensitivity grid explicitly probes 0.5× / 2× sample-count perturbations; if the ranking is sensitive, recommendation highlights this in `## Limitations` |
| Plan accidentally spawns an optimiser task via misread of the orchestrator intent | Low | Researcher constraint violation; budget overrun | REQ-10 explicitly forbids child task creation. Verification step checks that no `create-task` invocation is logged |

## Verification Criteria

* **Plan verificator passes with zero errors.** Command:
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0033_plan_dsgc_morphology_channel_optimisation -- uv run python -u -m arf.scripts.verificators.verify_plan t0033_plan_dsgc_morphology_channel_optimisation`.
  Expected output: `PL-E*` errors = 0; any warnings logged and acknowledged.
* **Answer asset verificator passes with zero errors.** Command:
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0033_plan_dsgc_morphology_channel_optimisation -- uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation`.
  Expected output: 0 errors; short_answer.md has 2-5 sentences; full_answer.md has a `## Sources`
  section with reference link definitions.
* **Requirement coverage is satisfied.** All 11 REQ-IDs in `## Task Requirement Checklist` are
  referenced by at least one numbered step in `## Step by Step`; verify by
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0033_plan_dsgc_morphology_channel_optimisation -- uv run python -c "import re; p = open('tasks/t0033_plan_dsgc_morphology_channel_optimisation/plan/plan.md').read(); reqs = sorted(set(re.findall(r'REQ-\d+', p))); print(reqs); assert len(reqs) == 11, reqs"`.
  Expected output: `['REQ-1', 'REQ-10', 'REQ-11', 'REQ-2', ..., 'REQ-9']`, no AssertionError.
* **Parameter enumerator outputs exist and are non-empty.** Command:
  `ls tasks/t0033_plan_dsgc_morphology_channel_optimisation/code/parameters/`. Expected output: at
  least three files (`morphology_params.json`, `channel_params_hhst.json`, `top10_vgcs.json`).
* **Cost envelope CSV has all three strategies and all three GPU tiers.** Command:
  `uv run python -c "import pandas as pd; df = pd.read_csv('tasks/t0033_plan_dsgc_morphology_channel_optimisation/code/cost_model/cost_envelope.csv'); assert set(df['compute_mode'].unique()) >= {'CORENEURON_GPU', 'SURROGATE_NN_GPU', 'MANY_CORE_CPU'}; assert set(df['tier'].unique()) >= {'RTX_4090', 'A100_40GB', 'H100'}; print(df.shape)"`.
  Expected output: `(N, M)` tuple with at least 9 compute_mode×tier rows per strategy.
* **Sensitivity grid covers 3 × 3 multipliers.** Command:
  `uv run python -c "import pandas as pd; df = pd.read_csv('tasks/t0033_plan_dsgc_morphology_channel_optimisation/code/cost_model/sensitivity_grid.csv'); assert set(df['cost_mult'].unique()) == {0.5, 1.0, 2.0}; assert set(df['sample_mult'].unique()) == {0.5, 1.0, 2.0}"`.
  Expected output: no AssertionError.
* **Sensitivity heatmap PNG exists.** Command:
  `ls tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/images/sensitivity_heatmap.png`.
  Expected output: the file is listed with non-zero size.
* **No internet-search step ran, no child task was created, no remote machine was provisioned.**
  Command:
  `ls tasks/t0033_plan_dsgc_morphology_channel_optimisation/logs/steps/ | grep -iE "research.internet|create.task|setup.machines" || echo "none"`.
  Expected output: `none`. This enforces REQ-10 and REQ-11.
