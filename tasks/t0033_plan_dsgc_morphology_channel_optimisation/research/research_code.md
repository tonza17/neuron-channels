---
spec_version: "1"
task_id: "t0033_plan_dsgc_morphology_channel_optimisation"
research_stage: "code"
tasks_reviewed: 8
tasks_cited: 7
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-04-22"
status: "complete"
---
# Research Code: Plan DSGC Morphology + VGC DSI Optimisation

## Task Objective

This task scopes and costs a future joint optimisation over DSGC dendritic morphology and the top-10
voltage-gated channel (VGC) types to maximise the direction-selectivity index (DSI) on the t0022
testbed architecture, priced on Vast.ai GPU. The planning step needs hard numbers for (a) the
parameter count per forsec region already present in t0022 and t0024, (b) the per-channel
biophysical parameter counts for the top-10 VGCs from t0019, (c) per-simulation wall-time anchors
from t0026, (d) the Vast.ai tier filters and cost-ranking algorithm from `vast_machines.py`, and (e)
which scoring / loss code can be reused as the optimiser objective. No simulations are run in this
task; only code inspection and arithmetic. The findings below power the parameter-count and pricing
tables in `plan/plan.md` and the final answer asset.

## Library Landscape

The project's library aggregator script is not present in this worktree (`arf/scripts/aggregators/`
ships `aggregate_tasks`, `aggregate_costs`, `aggregate_machines`, `aggregate_metric_results`,
`aggregate_metrics`, `aggregate_suggestions`, `aggregate_categories`, `aggregate_task_types` only —
no `aggregate_libraries` or `aggregate_answers`). Libraries were therefore enumerated by direct
inspection of `tasks/*/assets/library/`.

One registered library is relevant to this task:

* **`tuning_curve_loss`** (version `0.1.0`, registered by [t0012]): canonical 4-axis (DSI, peak,
  null, HWHM) tuning-curve scorer with weighted Euclidean-in-normalised-space loss, envelope
  pass/fail, and RMSE-vs-target diagnostics. Entry points include `score()`, `score_curves()`,
  `ScoreReport`, `load_tuning_curve()`, `compute_dsi()`, `compute_peak_hz()` in
  `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/` (8 modules: `__init__.py`,
  `paths.py`, `loader.py`, `metrics.py`, `envelope.py`, `weights.py`, `scoring.py`, `cli.py`).
  Aggregator output not available; the `details.json` under `assets/library/tuning_curve_loss/` is
  the primary source of truth. Import path for the optimisation objective would be
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import score_curves, ScoreReport`.

Other libraries (e.g. `modeldb_189347_dsgc_dendritic` registered by t0022, `de_rosenroll_2026_dsgc`
registered by t0024, `dsgc-baseline-morphology-calibrated` registered by t0009, `response_plots`
registered by t0011) exist but are cell-construction / plotting assets, not optimiser-objective
libraries. They are covered under the per-region channel enumeration below.

## Architecture Overview

The future optimisation inherits the t0022 testbed architecture: a ModelDB 189347 Poleg-Polsky
morphology with 282 ON-dendrite sections, plus a five-region channel-modular HOC overlay
(`dsgc_channel_partition.hoc`) that declares named `SectionList` objects for `SOMA_CHANNELS`,
`DEND_CHANNELS`, `AIS_PROXIMAL`, `AIS_DISTAL`, and `THIN_AXON` [t0022]. Each `forsec` block is a
one-line hook that an optimiser can replace to swap channel mechanisms per region without touching
the verbatim Poleg-Polsky HOC. The t0024 port overlays the same backbone with HHst + cad on every
dendrite and adds AR(2)-correlated stochastic release [t0024]. The t0026 wall-time experiment gives
the per-trial runtime anchors [t0026].

## Key Findings

### Per-Region Channel Set Already Instantiated by t0022

`dsgc_channel_partition.hoc` at
`tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc` (109 lines) defines five
`forsec` hooks, but the baseline t0022 testbed is deliberately *empty* in `AIS_PROXIMAL`,
`AIS_DISTAL`, and `THIN_AXON` — the bundled Poleg-Polsky morphology has no axon sections. Baseline
channel inventory inherited from ModelDB 189347 [t0022]:

| Region | Baseline mechanism | gbar (S/cm^2) | Source |
| --- | --- | --- | --- |
| `SOMA_CHANNELS` | HHst (spike.mod) | 1.0 (Nav) | ModelDB 189347 |
| `DEND_CHANNELS` | pas only | 0.03 (Nav prior) | ModelDB 189347, dendrite Nav is a *prior* not an active insert in the baseline |
| `AIS_PROXIMAL` | empty hook | 1.5 (Nav1.1 target) | [ModelDB-123623-KoleStuart] |
| `AIS_DISTAL` | empty hook | 8.0 (Nav1.6), 0.1 (Kv1.2), 0.0033 (Kv3 optional) | [ModelDB-144526-Hallermann, ModelDB-Kv3-Akemann2006] |
| `THIN_AXON` | empty hook | baseline HHst | — |

The t0022 build defers the population of AIS_PROXIMAL / AIS_DISTAL / THIN_AXON to channel-swap
tasks. For the future joint optimisation, every non-empty region above contributes at least one
`gbar` free parameter.

### Per-Region Channel Set Already Instantiated by t0024

The de Rosenroll 2026 port at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` (line
numbers 192-248) inserts `HHst` + `cad` on the soma, every primary dendrite, every non-terminal
dendrite, and every terminal dendrite, with per-tier `gbar` values from
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` [t0024]:

| Region | Mechanism | gNa (S/cm^2) | gKdr (S/cm^2) | gKm (S/cm^2) | gleak (S/cm^2) |
| --- | --- | --- | --- | --- | --- |
| Soma | HHst + cad | 0.150 | 0.035 | 0.003 | 1.667e-4 |
| Primary dendrite | HHst + cad | 0.200 | 0.035 | 0.003 | 1.667e-4 |
| Non-terminal dend | HHst + cad | 0.000 (zeroed) | 0.025 | 0.003 | 1.667e-4 |
| Terminal dend | HHst + cad | 0.030 | 0.025 | 0.003 | 1.667e-4 |

t0024's HHst mechanism bundles Nav, Kdr, Km, and leak into one lumped mechanism — that is four
conductance parameters per region × four regions = **16 free gbar parameters before introducing any
new VGC species** [t0024]. Ra (100 Ω·cm), cm (1.0 μF/cm²), eleak (-60 mV), celsius (36.9 °C), and
cad (CA_DECAY_TAU_MS=10 ms) are set as constants but are natural candidates for the optimiser.

### Held-Fixed Presynaptic / Synaptic Parameters

The task scope fixes all presynaptic machinery. For t0024 the held-fixed parameters read from
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` are: ACh kinetics (tau1 0.1 / tau2 4.0
ms, E 0 mV, weight 0.001 μS); GABA kinetics (tau1 0.5 / tau2 12.0 ms, E -60 mV, weight 0.003 μS,
uncorrelated scale 1.8); NMDA kinetics (tau1 2 / tau2 7 ms, E 0 mV, weight 0.0015 μS, n 0.25, γ
0.08); AR(2) process (φ=(0.9, -0.1), ρ_corr 0.6 / ρ_uncorr 0.0, innov_scale 1.0, base_rate 50 Hz);
SAC spatial offsets (30 μm min, 27 μm amacrine decay tau); bar geometry (velocity 1 μm/ms, width 250
μm) [t0024]. For t0022 the held-fixed presynaptic parameters are: AMPA (tau1 0.2 / tau2 1.5 ms, E 0
mV); GABA (tau1 0.5 / tau2 8.0 ms, E -70 mV); GABA null/pref ratio 4; burst scheduler (N_SYN_EVENTS
6, SYN_EVENT_INTERVAL_MS 30); EI offsets (±10 ms); bar (velocity 1 μm/ms) [t0022]. The researcher
explicitly excludes variation on the presynaptic side from the planned optimisation, so these values
are inputs, not free parameters.

### Top-10 VGC Selection from t0019

The t0019 answer asset at
`tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/full_answer.md`
(214 lines) enumerates five canonical priors grounded in five source papers (Van Wart 2006, Kole
2007, Fohlmeister & Miller 1997, Hu 2009, Kole 2008) [t0019]. It does not present a literal numbered
"top-10" list, but the five priors plus the `research/research_internet.md` "Channel-Density Numbers
from Public MOD Files" table in t0022 (lines 138-144) together name an effective top-10 VGC set for
the optimisation:

| # | Channel | Region(s) of interest | Per-channel free parameters (planning default) | Biophysical rationale |
| --- | --- | --- | --- | --- |
| 1 | Nav1.6 | distal AIS, soma | gbar, V_half_activation, τ_act | Hu2009 distal initiator, ~-45 mV V_half |
| 2 | Nav1.1 | proximal AIS | gbar, V_half_activation | Van Wart 2006 RGC-AIS canonical proximal subunit |
| 3 | Nav (HHst-lumped, dend) | dendrite | gbar | Poleg-Polsky 2026 dendritic Nav [t0024] |
| 4 | Kdr (HHst-lumped K) | soma, dendrite, AIS | gbar, V_half | Fohlmeister-Miller 1997 canonical kinetics |
| 5 | Kv1.1 | distal AIS | gbar | Kole 2007 near-threshold Kv1, co-localised with Nav1.6 |
| 6 | Kv1.2 | distal AIS | gbar, V_half_activation | Kole 2007 (100-300 pS/μm² default), tunable V_half |
| 7 | Kv2.1 | soma, proximal dendrite | gbar | Van Wart 2006 somatic Kv2.1 cluster |
| 8 | Kv3.1/3.2 | distal AIS (optional) | gbar | Akemann 2006 MOD file, RGC-AIS-Review-2022 |
| 9 | Km / KCNQ | soma, dendrite | gbar | HHst mechanism exposes gkmbar, Poleg-Polsky 2026 [t0024] |
| 10 | Ca (HVA) + cad | soma, dendrite | gbar_Ca, tau_cad | Fohlmeister-Miller 1997 Ca; cad decay tau |

This is the honest synthesis from the surveyed corpus. t0019's limitations section notes that all
five source papers were paywalled and that the Kv3 / KCNQ / Ca priors come from training-knowledge
overlays rather than direct paper extraction; the planner must carry these caveats forward.
Representative **per-channel free-parameter count = 2** (gbar in each of two regions of interest)
gives ~20 VGC parameters in the tightest parameterisation; a richer parameterisation that also lets
V_half / τ_act vary for Nav1.6 / Nav1.2 / Kv1.2 adds 6-9 more, landing in a 20-30 parameter total
for VGCs alone.

### Wall-Time Anchors from t0026

Per-(angle, trial) wall-time anchors read directly from
`tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/results_detailed.md` [t0026]:

| Model | Trials | Wall time | Per-(angle, trial) |
| --- | --- | --- | --- |
| t0022 (deterministic ModelDB 189347 channel testbed) | 96 | **6.0 min** | **~3.8 s** |
| t0024 (de Rosenroll 2026, AR(2) ρ=0.6) | 960 | **11,562 s / 3.21 h** | **~12.0 s** |

Per-V_rest range for t0024 was 1,403 s (V=-30 mV) to 1,581 s (V=-90 mV); hyperpolarised runs take
longer because the initial settle needs more sub-threshold steps. Hardware: Sheffield CICS Dell
OptiPlex Windows 11 workstation, single-threaded NEURON 8.2.7. t0026 explicitly flags that NEURON
supports `mpirun` and every (angle, trial) combination is embarrassingly parallel — a parallel-CPU
variant could cut t0024's 3.21 h to under 30 min [t0026]. This is a first-order input to the
"Vast.ai many-core CPU" strategy cost model.

### DSI Loss Function from t0012

`tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/scoring.py` (line 1-80+ head)
defines `ScoreReport` (frozen dataclass with `loss_scalar`, DSI / peak / null / HWHM residuals,
normalised residuals, RMSE-vs-target, reliability, `passes_envelope`, `per_target_pass`,
`weights_used`, `candidate_metrics`, `target_metrics`) and the `score()` and `score_curves()` entry
points. The scorer computes a weighted Euclidean norm in envelope-normalised space; the planner's
answer asset can specify that the future optimiser maximises `-loss_scalar` (or maximises DSI
directly using `compute_dsi()` from `tuning_curve_loss.metrics`) [t0012]. Per-metric keys registered
in `meta/metrics/` and consumed by the scorer are `direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`. The library is already a
registered asset, so the optimiser can `import` it directly and reuse its CSV loader.

### Vast.ai Tier Filters and Ranking Algorithm

`arf/scripts/utils/vast_machines.py` (237 lines) encodes the cost model (framework module, not a
task asset). Core findings:

| Aspect | Value |
| --- | --- |
| Default search filter string | `"rentable=true verified=true compute_cap<1200 cuda_max_good>=12.6"` |
| `compute_cap<1200` | blocks Blackwell sm_120 (RTX 5090, RTX PRO 6000 S/WS) for PyTorch 2.6.0 compatibility |
| `cuda_max_good>=12.6` | blocks drivers too old for container image |
| Speed-tier table (key entries) | RTX 3090 = 1.00 (reference); RTX 4090 = 1.60; A100 40GB = 1.80; A100 80GB = 2.00; H100 = 3.00; H200 = 3.50 |
| Reliability thresholds | 0.95 for ≤1 h; 0.98 for ≤5 h; 0.995 for ≤24 h; 0.999 otherwise |
| Cost-efficiency ranking | `rank_offers()` sorts by `(est_hours, price_per_hour)` with a ±20 % similar-speed tolerance — within the tolerance band the cheaper offer wins |
| Provisioning constants | `MAX_RETRY_OFFERS=3`, `POLL_INTERVAL_SECONDS=30`, `CREATION_TIMEOUT_SECONDS=600` |

`_estimate_hours(offer, estimated_hours_reference)` scales a reference runtime by
`reference_speed / offer_speed` using the `GPU_SPEED_TIERS` table. For the planning task, this gives
the tier-pricing extrapolation rule: RTX 4090 ≈ 0.625 × reference runtime, A100 40 GB ≈ 0.556×, H100
≈ 0.333×, H200 ≈ 0.286× (vs RTX 3090 reference = 1.0).

### Remote-Machine Operational Constraints

`arf/docs/explanation/remote_machines.md` and `arf/specifications/remote_machines_specification.md`
spell out the operational envelope that every cost estimate in this plan must respect:

* **Checkpointing** required when estimated wall-time exceeds 2 h: checkpoint every 30 min to a
  known path (`checkpoint_path`) and heartbeat every 5 min to `heartbeat_path`, both recorded in
  `machine_log.json`. Verificator code is `RM-W006`.
* **Instance labelling** `"<project>/<task_id>"` via `label_instance()` in `vast_machines.py`.
* **Cost recording** in two files: `tasks/<task_id>/results/costs.json` (with `vast_ai` service
  entry) and `tasks/<task_id>/results/remote_machines_used.json` (one record per machine:
  instance_id, GPU, duration, cost). Verificator `RM-E006` cross-checks the totals.
* **Budget enforcement**: `setup-machines` reads current spend via `aggregate_costs`, adds the
  plan's estimate, and refuses to provision if the total would exceed `project/budget.json`'s stop
  threshold.
* **Teardown** is mandatory — `verify_machines_destroyed` blocks PR merge if any instance is alive.

For a joint optimisation that will almost certainly run longer than 2 h, the plan must budget
checkpointing overhead (writing a state snapshot every 30 min) and heartbeat I/O (every 5 min).

### Embarrassingly Parallel Structure and NEURON GPU Options

t0026's "Compute efficiency" note [t0026] flags `mpirun` multi-processing for NEURON and observes
that "each (V_rest, angle, trial) combination is embarrassingly parallel". Joint morphology ×
channel optimisation is similarly decomposable: every objective evaluation is one 12-angle sweep
(~96-960 trials) that can fan out across GPU / CPU cores. CoreNEURON (the OpenACC/CUDA variant of
NEURON) is the obvious GPU path but has no installation or validation in any prior task — it would
be a new tool adoption. Surrogate-NN approaches (training a small NN on a CPU-NEURON sample then
optimising on the surrogate) are also untested in this project. The planner must record both as
unvalidated, with the CPU many-core path as the conservative fallback.

## Reusable Code and Assets

The future optimisation task will reuse the following (labelled per the cross-task code reuse rule):

* **`tuning_curve_loss` library** — **import via library**. Path:
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.scoring import score, score_curves, ScoreReport`
  and siblings. 8 modules, ~50-300 lines each. No adaptation needed; the scorer already returns DSI,
  peak Hz, null Hz, HWHM, and a weighted scalar loss suitable as an optimiser objective [t0012].
* **t0022 run driver** — `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` (684
  lines). **Copy into task.** Provides `run_one_trial_dendritic()`, `_run_sweep()`,
  `build_ei_pairs()`, `_compute_onset_times_ms()`, `schedule_ei_onsets()`. Adaptation needed: swap
  the `forsec SOMA_CHANNELS / DEND_CHANNELS / AIS_*` HOC blocks to insert optimiser-controlled
  channel mechanisms and `gbar` values [t0022].
* **t0022 channel partition HOC** —
  `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc` (109 lines). **Copy into
  task.** Five-region `SectionList` overlay used verbatim; only the `forsec` block bodies change per
  optimiser evaluation [t0022].
* **t0022 constants** — `tasks/t0022_modify_dsgc_channel_testbed/code/constants.py` (147 lines).
  **Copy into task.** Timing, geometry, threshold, scheduling constants. Hold every presynaptic/bar
  constant fixed per scope [t0022].
* **t0024 build_cell** — `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` (300+ lines).
  **Copy into task.** Reuses `_configure_soma`, `_configure_dends`, `_find_origin`, `_map_tree`,
  `DSGCCell`. The tier-based dendrite classification (primary / non-terminal / terminal) is directly
  the right abstraction for the optimiser to control per-tier gbar_HHst [t0024].
* **t0024 AR(2) noise generator** — `tasks/t0024_port_de_rosenroll_2026_dsgc/code/ar2_noise.py`.
  **Copy into task** if the optimisation uses the stochastic t0024 backbone; the
  `generate_ar2_process()` function is the presynaptic release-rate generator. Not needed for
  deterministic t0022-style optimisation [t0024].
* **t0024 constants** — `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` (120 lines).
  **Copy into task.** All held-fixed presynaptic / synaptic / AR(2) parameters; the four lumped HHst
  gbar defaults are the starting point the optimiser perturbs [t0024].
* **t0026 V_rest override and per-(angle, trial) wall-time recorder** —
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/vrest_override.py` and
  `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/trial_runner_t0022.py` / `trial_runner_t0024.py`.
  **Copy into task.** The wall-time recording pattern is directly reusable as the optimiser's
  telemetry [t0026].
* **Vast.ai provisioning library** — `arf/scripts/utils/vast_machines.py` (237 lines). **Import
  directly** (framework module, not a task library). Provides `build_query_string()`,
  `rank_offers()`, `reliability_threshold_for()`, `label_instance()`, `destroy_and_confirm()`, and
  the `SearchCriteria`, `VastOffer`, `FailedAttempt`, `ProvisionResult`, `DestroyResult`
  dataclasses. The plan and cost model reference `DEFAULT_FILTERS`, `GPU_SPEED_TIERS`,
  `RELIABILITY_THRESHOLDS`.

## Dataset Landscape

No dataset assets are directly reused by this planning task. t0022 and t0024 hold their tuning-curve
CSVs in `data/`; t0026 holds V_rest-sweep tidy CSVs. The future optimisation will produce many
tuning-curve CSVs that the t0012 scorer consumes via `load_tuning_curve()` — but this task itself
produces only an answer asset.

## Lessons Learned

* **Wall-time multiplier between deterministic and stochastic drivers is ~3.2×.** t0022's 3.8
  s/(angle, trial) vs t0024's 12.0 s/(angle, trial) is a hard empirical fact [t0026]. Any plan that
  assumes the same speed for both is wrong.
* **Hyperpolarised V_rest runs are slower.** t0024 per-V_rest wall-time varied 1,403-1,581 s across
  -90 to -30 mV [t0026]. Optimisers that sample far from the baseline V_rest will pay a modest
  wall-time surcharge.
* **Baseline Poleg-Polsky morphology has no axon.** The t0022 channel partition leaves
  `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON` empty. Any optimisation that wants to vary AIS channels
  must first construct axon sections — that is a new implementation task, not a one-line swap
  [t0022].
* **Lumped HHst vs multi-subunit trade-off is unresolved.** t0022 and t0024 both use the HHst
  mechanism, which lumps Na + Kdr + Km + leak. Separating into Nav1.6 / Nav1.2 / Kv1.2 distinct MOD
  files (as t0019 recommends) is a mechanism-library change outside this planning task's scope
  [t0019] [t0022].
* **t0019 answer asset carries a paywall caveat.** All five source papers were not downloaded;
  numerical priors for Kv1 gbar, Nav1.6 / Nav1.2 V_half split, AIS Nav density are
  training-knowledge overlays and should be refined in later literature-survey tasks [t0019]. The
  plan must flag this uncertainty.
* **No prior task used a GPU.** Every sim to date is single-threaded CPU NEURON 8.2.7 on a Windows
  workstation. CoreNEURON, NEURON+GPU, surrogate-NN are all unvalidated — so the cost model must
  budget a "tool adoption" task on top of any GPU-strategy recommendation [t0026].
* **Scoring library is production-ready.** `tuning_curve_loss` is already a registered library asset
  with unit tests (`test_scoring.py`, `test_metrics.py`, `test_envelope.py`, `test_loader.py`,
  `test_cli.py`) [t0012] — no objective-function work needed for the planner.

## Recommendations for This Task

1. **Use the enumerated region parameter counts (5 forsec regions × ~3 channel parameters each ≈ 15
   region-level parameters) plus the top-10 VGC × 2 parameters ≈ 20-30 VGC parameters as the
   baseline search-space dimensionality** in the plan's search-space arithmetic. Add ~6-10
   morphology parameters from the t0027 taxonomy (length, branch count, diameter, arbor asymmetry)
   to reach a total joint dimensionality of roughly 40-50 parameters in the tight parameterisation,
   60-80 in the rich parameterisation.
2. **Peg per-simulation wall-time to the t0026 anchors** (3.8 s/trial for t0022-deterministic, 12.0
   s/trial for t0024-stochastic). Apply the `vast_machines.GPU_SPEED_TIERS` speed ratio to
   extrapolate to each GPU tier. Note that CoreNEURON's actual speedup is unvalidated in this
   project — use a literature placeholder (e.g. 5-10× for a single-cell NEURON model on a midrange
   GPU) with wide sensitivity bands.
3. **Use `tuning_curve_loss.score_curves()` as the stated optimiser objective** in the answer asset,
   with DSI weighting dominant. No need to reinvent the scorer [t0012].
4. **Pick three GPU tiers as the headline comparisons**: RTX 4090, A100 40 GB, H100. They span the
   speed-tier table (1.60, 1.80, 3.00 vs RTX 3090 = 1.00) and appear in
   `vast_machines.GPU_SPEED_TIERS`. Include RTX 3090 as the reference tier.
5. **Budget for the 2-hour checkpointing cliff.** Any headline strategy that runs more than 2 h must
   budget 30-min checkpoint I/O + 5-min heartbeat overhead per the remote machines spec.
6. **Report honestly on the top-10 VGC list**: the literal "top-10" numbered list is *synthesised*
   from t0019's 5 canonical priors plus t0022's research_internet.md channel-density table, not a
   pre-existing asset. State this in the answer asset's methodology section with the exact synthesis
   rule.
7. **Recommend the CPU many-core Vast.ai strategy as the conservative fallback** — this is the only
   compute path with validated t0026 wall-times. Surrogate-NN and CoreNEURON should be listed as
   high-upside / high-risk strategies.

## Task Index

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Source of the `tuning_curve_loss` registered library that the future joint
  optimisation will import as its objective function. Provides DSI / peak / null / HWHM residuals
  and a weighted scalar loss already validated against the t0004 target.

### [t0019]

* **Task ID**: `t0019_literature_survey_voltage_gated_channels`
* **Name**: Literature survey: voltage-gated channels in retinal ganglion cells
* **Status**: completed
* **Relevance**: Source of the 5 canonical VGC priors that this task expands into a top-10 channel
  list, with per-channel biophysical parameter counts for the optimisation search-space arithmetic.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially-asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: Provides the 5-region channel-modular HOC partition (`dsgc_channel_partition.hoc`)
  and the 12-angle × 10-trial deterministic driver that the future optimiser will drive. Its
  `constants.py` enumerates the held-fixed presynaptic / bar / scheduler parameters.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Provides the Poleg-Polsky 2026-derived parameter backbone, per-tier HHst gbar
  values (16 free parameters before new VGCs), AR(2)-correlated stochastic release, and the primary
  / non-terminal / terminal dendrite tier abstraction the optimiser will control.

### [t0026]

* **Task ID**: `t0026_vrest_sweep_tuning_curves_dsgc`
* **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
* **Status**: completed
* **Relevance**: Empirical per-(angle, trial) wall-time anchors (3.8 s for t0022 deterministic, 12.0
  s for t0024 stochastic at ρ=0.6) that every cost model in this plan must extrapolate from. Also
  documents the embarrassingly parallel structure and the mpirun opportunity.

### [t0027]

* **Task ID**: `t0027_literature_survey_morphology_ds_modeling`
* **Name**: Literature survey: modeling effect of cell morphology on direction selectivity
* **Status**: completed
* **Relevance**: Taxonomises 8 morphology variables (length, branch count / order, diameter, arbor
  asymmetry, input spatial layout, input kinetic tiling, transfer resistance, collapse-to-point)
  that feed the morphology side of the joint optimisation's search-space arithmetic.

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: compartmental models of DS retinal ganglion cells
* **Status**: completed
* **Relevance**: Declared dependency; provides compartmental-model methodology priors the planner
  must cross-reference when costing surrogate-NN and CoreNEURON strategies.
