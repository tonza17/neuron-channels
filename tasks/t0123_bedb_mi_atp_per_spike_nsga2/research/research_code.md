---
spec_version: "1"
task_id: "t0123_bedb_mi_atp_per_spike_nsga2"
research_stage: "code"
tasks_reviewed: 16
tasks_cited: 15
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-05-24"
status: "complete"
---
# Research Code: NSGA-II Maximising MI and Minimising ATP-per-Spike

## Task Objective

This task forks the [t0122] single-seed 68-d Bed B + 14-d morphology NSGA-II substrate and swaps
both objectives: replace (DSI, cytoplasm volume) with (mutual information, ATP-per-spike). MI is
computed in two tiers: a spike-count plug-in estimator with Miller-Madow bias correction inside the
NSGA-II inner loop (2-bit ceiling on the 4-direction protocol), and the Strong-Bialek 1998
direct-method bits/s rate on the top-10 Pareto cells post-hoc with 8 directions x 20 trials. ATP per
spike follows the Sengupta 2010 recipe: integrate inward `seg.ina` over per-AP windows across soma +
AIS + every dendritic segment, divide by elementary charge, and divide by 3 (Na+/K+ ATPase
stoichiometry). Hard constraints reproduced from [t0122] verbatim are `_POOL_RESTART_EVERY=10`,
`HV_PLATEAU_AUTO_STOP=False`, `POP_SIZE=96`, `N_EVAL_SEEDS=3`, `N_GEN_MAX=60`, `COST_CAP_USD=6.0`,
plus a new constraint `N_DIRECTIONS=4` (overriding [t0122]'s 2). The headline scientific output is a
Niven 2007 comparison: does the DSGC bits-per-ATP front follow the fly photoreceptor super-linear
cost-vs-information scaling?

## Library Landscape

The project does not currently expose a library aggregator: `arf/scripts/aggregators/` ships only
`aggregate_categories`, `aggregate_costs`, `aggregate_machines`, `aggregate_metric_results`,
`aggregate_metrics`, `aggregate_suggestions`, `aggregate_task_types`, and `aggregate_tasks`. There
is therefore no registered `assets/library/` collection to enumerate. All cross-task code reuse in
this lineage follows the "copy into task" convention: each NSGA-II task forks the prior task's
`code/` directory verbatim and overrides only what changes. The procedural morphology generator and
its [t0092] patch wrapper are cited as cross-task imports in [t0122] via full repo-rooted dotted
paths (`tasks.t0090_morphology_generator_diversity_test.code.generator.generate_morphology` and
`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`).
The [t0024] de Rosenroll port (NEURON bootstrap, AR(2) noise generator, bar arrival kinematics) is
likewise imported by full path from `tasks.t0024_port_de_rosenroll_2026_dsgc.code`. The [t0080]
compiled NEURON MOD library (`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`) is the
shared `nrnmech` namespace used by all 68-d morphology-extended runs; it contains the three Na
channels `nav16t80`, `napt80`, `nart80` whose summed `seg.ina` is the substrate of the Sengupta 2010
ATP-per-spike recipe. Third-party libraries declared in `pyproject.toml` that are directly relevant:
`scikit-learn>=1.8.0` (provides `sklearn.metrics.mutual_info_score` for the discrete plug- in MI
estimator -- pattern established in [t0116] and [t0117] `cluster_seed_purity.py` line 19),
`scipy>=1.17.1` (provides `scipy.stats.entropy` for `log2`-base entropy calculations and
`linregress` for the Strong-Bialek 1/T linear fit), `numpy>=2.4.4` (numerical primitives),
`matplotlib>=3.10.8` (Niven 2007 comparison chart and the ATP/AP distribution chart), and
`pymoo>=0.6.1.6` (the NSGA-II implementation). There is no prior task code implementing the
Strong-Bialek direct method or the Sengupta ATP recipe; both modules must be written from scratch in
this task.

## Key Findings

### Fork-the-most-recent NSGA-II driver verbatim; only objectives change

[t0122] is the direct fork point. Its 776-line `nsga2_driver.py` is itself a verbatim fork of the
[t0115] driver with three deltas (new seed via `secrets.randbelow`, `N_GEN=60` ceiling, `$6` cap);
every NSGA-II convention this task needs is already in place. `_POOL_RESTART_EVERY = 10` is
hard-coded at line 105. `OperatorStopTermination` polls `intervention/stop.md` each generation.
`CostWatchdogTermination` reads `T0122_HARD_BUDGET_USD = 6.0` from `code/constants.py`. The live
`TerminationCollection` is
`{MaximumGenerationTermination, CostWatchdogTermination, OperatorStopTermination}` -- no
`HVPlateauTermination`. The per-gen dill checkpoint and JSONL trace pattern are preserved from
[t0115]. This task must adopt the [t0122] driver verbatim with only import-path rewrites
(`tasks.t0122_dsi_cytoplasm_volume_nsga2.code.*` -> `tasks.t0123_*.code.*`) and the `N_GEN=60`
default carries over from [t0122] unchanged. The [t0122] post-mortem (`$0.50` of `$6` cap, 5760
cells, 60/60 gens clean) confirms the substrate is healthy on a 4-direction protocol.

### N_DIRECTIONS = 4 needs only a single constant change

[t0122]'s `evaluator.py` line 479 computes
`angles_deg = [float(d) * (360.0 / n_directions) for d in range(n_directions)]`. For
`n_directions=4` this yields `[0.0, 90.0, 180.0, 270.0]` -- exactly the 4 antipodal-pair angles the
task description mandates. The same formula handled [t0091]'s `N_DIRECTIONS=16` and [t0122]'s
`N_DIRECTIONS=2` without modification. To get 4 directions in t0123, change `N_DIRECTIONS: int = 2`
(line 132 of [t0122]'s `constants_morphology.py`) to `N_DIRECTIONS: int = 4`. Trial cost scales
linearly: t0122 ran at 6 trials per cell (`3 eval seeds x 2 directions`) and finished at $0.50;
t0123's 12 trials per cell (`3 eval seeds x 4 directions`) extrapolates to ~$1.00 -- comfortably
inside the $6 cap. The angles 90 deg and 270 deg are NOT pre-baked into the
`_gaba_prob_for_direction` sigmoid in [t0122]'s `trial_helpers.py` line 57 (it computes
`d = abs((direction_deg - CELL_PREF_DEG + 180.0) % 360.0 - 180.0)` which generalises to any
direction). No change needed there.

### Spike-count plug-in MI is the right inner-loop estimator for 12-trial budgets

The task description and the [t0097] catalogue's `mutual_information_stimulus_spike_train` recipe
both flag that the Strong-Bialek 1998 direct method (binary spike-word entropy at multiple word
lengths T, linear regression of (H_total - H_noise)/T against 1/T to extract the bits/s intercept)
requires many trials per stimulus to estimate within-stimulus noise entropy. With only 3 trials per
direction in the inner loop, the 1/T extrapolation will be too noisy as a selection signal. The
discrete spike-count MI

```
I_count(D; N_spikes) = sum_{d, n} P(d, n) log2( P(d, n) / (P(d) P(n)) )
```

on the 4 x B contingency table (`4` directions, `B` bins of total spike count) with the Miller-Madow
bias correction `(R-1)(C-1)/(2N ln 2)` (here `R=4`, `C=B`, `N=12`) is the canonical replacement for
small N. The ceiling is `log2(4) = 2.0 bits` (saturates when each direction's spike-count
distribution is perfectly separable). `sklearn.metrics.mutual_info_score(labels_x, labels_y)`
returns the same plug-in MI in **nats** (natural log); divide by `ln(2)` to get bits. This is the
pattern established in [t0116] and [t0117] for cluster-vs-seed MI (`cluster_seed_purity.py` line 19
uses `normalized_mutual_info_score`; for raw MI use `mutual_info_score`). The Miller-Madow
correction is one line of NumPy on top of the sklearn call.

### Strong-Bialek direct-method MI is the post-hoc verification ladder, not the inner loop

The [t0097] catalogue's recipe (full_answer.md lines 287-324) is unambiguous: discretise each
trial's spike train into binary words at `dt = 5 ms`, choose `T in {25, 50, 75, 100} ms` (word
lengths `L = T/dt in {5, 10, 15, 20}` bits), pool words across all trials for `H_total(T)` and
across each direction's trials for `H_noise(T)`. Fit `[H_total(T) - <H_noise(T)>_D]/T` against `1/T`
and take the intercept. With `8 directions x 20 trials = 160 trial budget per cell`, this yields the
bits/s rate directly comparable to Dhingra and Smith 2004's 20-30 bits/s guinea-pig RGC anchor and
Niven 2007's 200-1000 bits/s fly photoreceptor range. The 1400 ms trial duration is fixed by the
project's standing measurement protocol (memory `feedback_dsgc_measurement_protocol.md`). The direct
method is implemented as a standalone post-hoc script `code/post_hoc_strong_bialek.py` that loads
the top-10 Pareto cells, re-runs each with 8 directions x 20 trials in `FULL` mode, and writes
`results/data/post_hoc_strong_bialek_mi_top10.json`. The cost overhead is 10 cells x 160 trials =
1600 sims, expected $0.20-0.50.

### ATP-per-spike recipe needs new per-segment seg.ina recording absent from [t0122]

[t0122]'s `evaluator.py` records only `cell.soma(0.5)._ref_v` (line 282) -- a single Vm trace at the
soma. The Sengupta 2010 ATP recipe in [t0097]'s catalogue (full_answer.md lines 326-372) needs
`seg.ina` per segment for soma + AIS proximal + AIS distal + every dendritic segment. The
established NEURON `Vector.record` idiom is the same as [t0122]'s `recorder.py` line 59
(`v_v.record(seg._ref_v, RECORD_DT_MS)`), but with `seg._ref_ina` instead of `seg._ref_v`. The
recording footprint roughly doubles: per cell per direction we go from 1 trace (soma Vm) to
`1 + 2 + n_dend_segments` traces (soma Vm + AIS + dendrites). Dendrite segment counts vary across
morphologies but typically range 20-200 per cell in the 14-d substrate (see [t0090] `_compute_nseg`
line 117 of [t0122] `extend_with_ais.py`). Memory cost: at `dt=25 us`, 1400 ms is 56000 floats; at
200 segments + 2 AIS + 1 soma Vm, that is ~11 MB per direction in float64, ~14 MB with overhead.
Acceptable at 12 trials per cell. The recording handles must be re-created on every `h.finitialize`
because NEURON wipes them on reset; the per-cell setup helper
`_attach_ina_recorders(*, h, cell) -> InaRecorders` runs once per `_run_one_trial` invocation in
`evaluator.py`.

### NEURON's seg.ina is the inward Na+ current summed across all Na channels per segment

The [t0080] mods folder ships three Na channels (`nav16t80`, `napt80`, `nart80`) plus 9 K-family
channels (`bkt80`, `calt80`, `catt80`, `iht80`, `kdrt80`, `kv3t80`, `kv4t80`, `kv7t80`, `skahpt80`)
plus `skt80`. Each Na channel writes to NEURON's accumulator `seg.ina` (the global Na+ ion-channel
current variable). When all three Na channels are inserted into the same segment (as in [t0122]
`apply_params.py` line 220's distal-tier overlay), `seg.ina` reports the sum of all three -- exactly
the per-segment total Na+ current the Sengupta recipe needs. The recipe takes the **inward**
component, so the per-AP charge is `Q^(c, AP) = -integral over AP window of min(I_Na, 0) dt * area`
(Na+ current in NEURON convention is negative inward; `min(I_Na, 0)` keeps only inward, the leading
sign converts to positive magnitude). The conversion from `mA/cm^2` to total current is
`I_total_mA = seg.ina * seg.area()` where `seg.area()` is in `um^2`; multiply by `1e-2` to get
`cm^2` -> `I_total_A = seg.ina * 1e-3 * seg.area() * 1e-2 / 1.0 = seg.ina * seg.area() * 1e-5 A`,
then integrate over seconds. Final ATP per AP per compartment is
`N_ATP^(c, AP) = (Q^(c, AP) / e) / 3` where `e = 1.602e-19 C` and the factor `1/3` is the Na+/K+
ATPase stoichiometry.

### AP-window detection is a soma-Vm threshold crossing with refractory enforcement

Per [t0097]'s recipe step 2 and the [t0122] / [t0091] convention, the AP-window detector uses a
soma-Vm threshold crossing at `-20 mV` with a refractory period of 2 ms between detections to avoid
double-counting mid-AP fluctuations. AP-start = upward crossing; AP-end = next downward crossing
back through -20 mV (typically 1.5-3 ms later). The task description tightens this to "+/-2 ms
around peak" which means the integration window is `[t_peak - 2 ms, t_peak + 2 ms]`. The spike
counter [t0122] `trial_helpers._count_spikes` already detects threshold crossings at
`AP_THRESHOLD_MV = -20 mV` (line 256 of [t0122] `constants_electrophys.py`); we reuse its threshold
constant but build a separate AP-peak detector for ATP windowing (the existing `_count_spikes`
returns only the count, not the times).

### Carter-Bean 2009 smoke gate is the load-bearing pre-launch sanity check

The [t0097] catalogue's `metabolic_energy_atp_per_spike` recipe step 6 sets the validation
threshold: discrepancies > 30% vs Carter and Bean 2009's
`~4 mM-mol ATP per AP per cm of axon at the AIS` benchmark indicate a recipe error (most commonly a
surface-area conversion bug) and must be fixed before launching NSGA-II. The smoke gate must compute
ATP/AP/cm at the AIS on the canonical [t0083] Bed B best-cell electrophys vector, compare it to
`~4 mM-mol/cm = 4 * 6.022e20 ATP/cm = 2.41e21 ATP/cm`, and FAIL if it deviates by more than 30%.
This is a NEW smoke check on top of [t0122]'s 8 checks; the t0123 smoke gate has 9 (or 10 if a
separate MI smoke check is added). The check is deferred to the Vast.ai remote machine (no compiled
MOD library on Windows local; the precedent is [t0122] smoke check 1 -- the anchor-cell PD-rate
sanity).

### Recording footprint doubling has knock-on costs but stays within disk + memory budget

[t0122]'s `all_evaluations_seed1524.json` is ~2 MB at 5760 cells. With t0123's added per-cell
ATP-per-spike, MI count, per-direction firing for 4 directions, and per-segment ATP breakdowns, the
per-cell row grows ~3x. Estimated `all_evaluations_seed<S>.json` size: ~5-10 MB at 5760 cells. The
per-trial `seg.ina` traces themselves are NOT persisted (they are reduced to per-AP charge integrals
inside the trial loop and then discarded) -- this is critical to keep wall-clock acceptable. The
reduction is: in each trial, after `h.run()`, iterate the recorded `ina` Vector objects, compute the
per-AP integrated inward charge per segment, sum across segments to get per-AP ATP, sum across APs
in the trial, and emit only the scalar `atp_per_trial`. The full traces never hit disk.

### Top-N morphology grids must draw full dendrite trees ([t0122] inherits the rule from [t0115])

[t0122]'s `build_top50_morphologies.py` (323 lines) implements the full-dendrite-tree rendering
operator-feedback memory `feedback_top50_morphologies_full_dendrites.md` mandates: iterate
`result.section_endpoints_xy.items()` excluding soma and AIS, render every non-soma non-AIS section
as a `LineCollection` segment, render soma as a `Circle` patch. [t0114] failed this rule and was
rejected; [t0115] and [t0122] both complied. This task must replicate [t0122]'s
`build_top50_morphologies.py` verbatim with only the seed and input filename changing.

### Niven 2007 comparison chart is a brand-new visualisation; no prior task pattern

No prior task has rendered a bits-per-ATP scatter plot. The Niven 2007 4-species fly photoreceptor
curve (D. melanogaster 200 bits/s, D. virilis ~400, M. domestica ~700, S. carnaria ~1000 bits/s,
with fixed cost ~20% of maximum and super-linear scaling) must be hard-coded as a reference curve on
the chart. Render top-10 DSGC Pareto cells as scatter points in `(ATP/spike, bits/s)` space with the
fly curve overlaid. Use [t0122]'s matplotlib idioms (`build_pareto_plots.py` lines 26-100 for
scatter + Pareto-front highlighting) as the structural template. Output path:
`results/images/niven_2007_comparison.png`. A second chart
`results/images/pareto_front_mi_vs_atp.png` mirrors [t0122]'s `pareto_front_dsi_vs_volume.png` for
the inner-loop MI_count vs ATP/spike axes.

### Tightened DSI silence guard from [t0122] carries over even though DSI is not optimised

[t0122] tightened the silence guard from "total_mean_spikes < 10" to "pd_spikes_sum < 3" at line 157
of its `evaluator.py` because cytoplasm-volume minimisation pushes the optimiser toward tiny cells
with low total spike counts. The same risk applies to ATP-per-spike minimisation: the cheapest cell
is one that never spikes (`ATP/spike` is undefined, but the optimiser sees the worst-case penalty
which is large). The silence guard remains essential as a defensive check on the diagnostic DSI that
gets reported alongside MI; it does NOT affect the F vector but does affect the LEGIT filter in
`metrics_builder.py` and the predictions asset's `legit_bool`. Keep the guard threshold at
`SILENCE_PD_SPIKES_THRESHOLD = 3` verbatim from [t0122].

### Predictions asset schema must grow several new fields

[t0122]'s predictions asset `nsga2-cytoplasm-volume-bedb-morph` has per-cell rows with
`vector_68d, dsi_vector_sum, pd_rate_hz, robustness, cytoplasm_volume_um3, objective_F_minimised, silence_failed_bool, legit_bool`
(full_answer.md description.md at line 282 of `build_predictions_assets.py`). For t0123 the row must
drop `cytoplasm_volume_um3` and add: `mi_count_bits`, `atp_per_spike_molecules`,
`atp_per_ap_molecules` (the per-AP mean before dividing by spikes),
`atp_per_ap_compartment_breakdown` (dict with `soma`, `ais`, `dendrites_total` keys for the
per-section breakdown), and per-direction firing rates `firing_hz_per_dir` (4 entries: `dir_0`,
`dir_90`, `dir_180`, `dir_270`). DSI stays as a tracked diagnostic (`dsi_vector_sum`). For the
top-10 Pareto cells, the post-hoc rerun adds `mi_strong_bialek_bits_per_sec` (a single bits/s
estimate per cell, with its standard error from the linear-regression fit).

## Reusable Code and Assets

### From [t0122] -- copy into task

The following files in `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` are the fork base. Copy each
verbatim into `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/` and run a global search-and-replace
from `t0122_dsi_cytoplasm_volume_nsga2` to `t0123_bedb_mi_atp_per_spike_nsga2`:

* `nsga2_driver.py` (776 lines) -- **copy and edit**: rewrite imports; default `N_GEN` stays at 60.
  Function signature
  `run_nsga2_for_seed(*, task_seed, n_gen_override=None, step_id="009_implementation") -> dict[str, object]`.
* `evaluator.py` (608 lines) -- **copy and edit**: replace `cytoplasm_volume_um3` field on
  `CellEvalResult` with `mi_count_bits: float`, `atp_per_spike_molecules: float`,
  `atp_per_ap_molecules: float`; add per-direction firing dict; rewrite
  `BedBV3MorphProblem._evaluate` to emit `out["F"] = [-mi_count_bits, +atp_per_spike_molecules]` (MI
  maximised so negated; ATP minimised directly). Replace `compute_cytoplasm_volume_um3` import with
  `compute_atp_per_spike` and `compute_mi_count_bits`. Wire the per-segment `seg.ina` recording
  inside `_run_one_trial`. Keep the silence guard at `pd_spikes_sum < 3`.
* `generator_wrapper.py` (105 lines) -- **copy verbatim**, only import-path rewrites. Functions:
  `build_cell(*, h, morph_params)`, `morphology_params_from_vector`, `split_68d_vector`,
  `hash_morphology_vector`.
* `trial_helpers.py` (311 lines) -- **copy verbatim**, import-path rewrites only. Function
  `setup_synapses_parametric(*, cell, n_ach, n_gaba, rho_0_ach, lambda_ach_um, rho_0_gaba, lambda_gaba_um, w_ach_us, w_gaba_us, placer_seed, gnmda_dend, mg_conc_mm, voff_nmda) -> SynapseBundle`.
* `apply_params.py` (234 lines) -- **copy verbatim**, import-path rewrites only. Function
  `apply_parameter_vector(*, cell, params)`.
* `build_cell_ais.py` (79 lines) -- **copy verbatim**. Dataclass `DSGCCellWithAIS`.
* `extend_with_ais.py` (127 lines) -- **copy verbatim**. Functions `extend_with_ais`,
  `update_ais_geometry`, `_compute_nseg`.
* `parametric_placer.py` (105 lines) -- **copy verbatim**. Function
  `place_synapses(*, h, soma, candidate_sections, n_target, rho_0, lambda_um, seed)`.
* `constants.py` (160 lines) -- **copy and edit**: rename `T0122_SEEDS` -> `T0123_SEEDS = (X,)`
  where `X` is drawn via `secrets.randbelow(10000)`; set `T0123_HARD_BUDGET_USD = 6.0` and
  `T0123_PER_INSTANCE_WATCHDOG_USD = 5.0`; preserve all back-compat aliases (`T0104_*`, `T0106_*`,
  `T0114_*`, `T0115_*`, `T0122_*`) so the forked driver and cost watchdog pick up the cap. Replace
  cytoplasm-volume constants with ATP/MI equivalents (see `constants_morphology.py`).
* `constants_morphology.py` (172 lines) -- **copy and edit**: `N_DIRECTIONS: int = 2` -> `4`; add
  `HV_UTOPIA_MI_BITS = 1.5` (target, below the 2-bit ceiling); add `HV_UTOPIA_ATP_PER_SPIKE = 1e9`
  (placeholder; will be tuned to match the Sengupta/Carter-Bean benchmark order of magnitude);
  replace `HV_UTOPIA_VOLUME_UM3` with the ATP/MI utopia; change `REF_POINT_HV` to a pessimistic
  `(0.0, ATP_PER_SPIKE_MAX_REF)` (negated-MI axis = 0 because MI is non-negative, ATP axis upper
  bound = 1e10 say); replace `WORST_CASE_CYTOPLASM_VOLUME_UM3` with `WORST_CASE_MI_BITS = 0.0` and
  `WORST_CASE_ATP_PER_SPIKE = ATP_PER_SPIKE_MAX_REF * 2.0`. Keep `POP_SIZE = 96`,
  `N_EVAL_SEEDS = 3`, `N_GEN = 60`.
* `constants_electrophys.py` (547 lines) -- **copy verbatim**.
* `cost_watchdog.py` (129 lines) -- **copy verbatim**.
* `hv_plateau_watchdog.py` (89 lines) -- **copy verbatim** (intentionally NOT in live
  TerminationCollection).
* `random_init.py` (101 lines) -- **copy and edit**: import `T0123_SEEDS` instead of `T0122_SEEDS`.
* `paths.py` (218 lines) -- **copy and edit**: rewrite `TASK_ROOT` resolution; add new path
  constants for `POST_HOC_STRONG_BIALEK_JSON` and `NIVEN_2007_PNG`.
* `bootstrap.py` (161 lines) -- **copy verbatim**.
* `build_top50_morphologies.py` (323 lines) -- **copy and edit**: rename hard-coded task id; change
  input filename to `all_evaluations_seed<NEW_SEED>.json`; change output filename to
  `top50_morphologies_seed<NEW_SEED>.png`. Full dendrite tree rendering preserved verbatim per the
  memory rule.
* `smoke_gate.py` (543 lines) -- **copy and edit**: keep [t0122]'s 8 checks (with the silence-guard
  threshold staying at `3 PD spikes`, the cost cap at `6.00`, the cytoplasm-volume check replaced
  with an MI-count + ATP-per-spike sanity check); ADD a 9th check: Carter-Bean ATP/AP/cm at the AIS
  on the canonical anchor cell within 30% of 4 mM-mol/cm.
* `test_evaluator_dsi_guard.py` (185 lines) -- **copy and edit**: rename, keep the DSI silence-
  guard assertion (`>= 3 PD spikes`).
* `metrics_builder.py` (181 lines) -- **copy and edit**: replace cytoplasm-volume variants with
  MI-count and ATP-per-spike variants; keep DSI variants as diagnostic; add Strong-Bialek bits/s
  variant for the top-10 cells.
* `build_predictions_assets.py` (371 lines) -- **copy and edit**: change
  `PREDICTIONS_ID = "nsga2-mi-atp-per-spike-bedb-morph"`; rewrite the per-cell row schema (see
  "Predictions asset schema must grow several new fields" above); add `metrics_at_creation` keys
  `best_mi_count_bits`, `min_atp_per_spike`, `niven_curve_above_below_count`.
* `build_pareto_plots.py` (344 lines) -- **copy and edit**: change axis labels and constants for MI
  vs ATP/spike; ADD the Niven 2007 reference curve overlay.
* `build_assets.py` (416 lines) -- **copy and edit**: change the answer asset short name to
  `dsgc-bits-per-atp-vs-niven-2007`; rewrite the question and the answer paragraph.
* `build_results.py` (173 lines) -- **copy and edit**: rewrite the `results_summary.md` template to
  reference MI / ATP / Niven 2007 instead of DSI / cytoplasm volume / Cuntz 2010.
* `anchor_definitions.py` (149 lines) -- **copy verbatim**.
* `anchor_classifier.py` (127 lines) -- **copy verbatim**.
* `biological_priors.py` (252 lines) -- **copy verbatim** (used by the scorecard for tracked DSI
  diagnostic only).
* `biological_scorecard.py` (183 lines) -- **copy verbatim**.

### From [t0090] -- already imported by full dotted path (do not copy)

The [t0122] `generator_wrapper` imports
`tasks.t0090_morphology_generator_diversity_test.code.morphology_params.MorphologyParams` and
`MorphologyResult` and the
`tasks.t0090_morphology_generator_diversity_test.code.constants.PARAM_NAMES`, `PARAM_BOUNDS`,
`INT_PARAM_NAMES`, and 14 individual `PARAM_*` string constants. This task should NOT copy these;
the project precedent (codified in C-0093-01 per the comment at line 20 of [t0122]
`generator_wrapper.py`) is to import them by full path.

### From [t0092] -- already imported by full dotted path (do not copy)

`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`
and
`tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels.insert_baseline_channels`
are imported by [t0122] `generator_wrapper.py` and must continue to be imported by full path. This
is the canonical morphology entry point per C-0093-01.

### From [t0024] -- already imported by full dotted path (do not copy)

`tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell._ensure_neuron_on_path`,
`tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise.generate_ar2_batch`, and the constants
module are imported by [t0122] code. This task inherits these imports through the verbatim copy of
`trial_helpers.py`.

### From [t0080] -- already imported by full dotted path (do not copy)

`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params.ensure_t80_dll_loaded` is the
process-singleton NEURON MOD library loader; the compiled
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` directory must exist on the remote
machine (`nrnivmodl` rebuilds the `.so` once per machine). The 13 channel SUFFIXes including the
three Na channels `nav16t80`, `napt80`, `nart80` whose summed `seg.ina` enters the Sengupta recipe
are all loaded by this DLL.

### From [t0117] / [t0116] -- pattern for sklearn MI usage (copy idiom, not file)

`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/cluster_seed_purity.py` (line 19)
imports `from sklearn.metrics import normalized_mutual_info_score` and uses
`nmi: float = float( normalized_mutual_info_score(seeds, clusters))` on integer-label arrays. The
pattern is identical for `mutual_info_score(direction_labels, spike_count_bins)` returning raw
plug-in MI in **nats**. Convert to bits by dividing by `math.log(2)`. The Miller-Madow correction is
added as one line of NumPy on top.

### New code to write from scratch in this task

* `code/mi_estimator.py` -- a NEW ~80-line module with two functions:
  * `compute_mi_count_bits(*, direction_labels: NDArray[int], spike_counts: NDArray[int], n_bins: int = 4) -> float`.
    Bins `spike_counts` into `n_bins` log-spaced bins, computes the plug-in MI via
    `sklearn.metrics.mutual_info_score`, subtracts the Miller-Madow bias correction
    `(R-1)(C-1)/(2N ln 2)` (returns the bias-corrected value in bits, divided by `log(2)`).
    Inner-loop estimator -- called once per cell per generation.
  * `compute_mi_strong_bialek_bits_per_sec(*, spike_trains_by_direction: dict[float, list[NDArray[float]]], word_lengths_ms: tuple[int, ...] = (25, 50, 75, 100), dt_ms: float = 5.0) -> StrongBialekResult`.
    Discretises each trial's spike train into binary words at `dt_ms = 5 ms` resolution, computes
    `H_total(T)` (entropy of pooled-across-directions word distribution) and `H_noise(T)` (entropy
    averaged across each direction's pooled word distribution) for each word length T, fits
    `(H_total - <H_noise>)/T` against `1/T` via `scipy.stats.linregress`, returns the intercept as
    `bits_per_sec` with the regression standard error. Post-hoc only -- called on the top-10 Pareto
    cells with 8-direction x 20-trial reruns. Returns
    `StrongBialekResult(bits_per_sec, std_err_bits_per_sec, r_squared, h_total_per_t, h_noise_per_t)`
    dataclass.
* `code/atp_per_spike.py` -- a NEW ~120-line module with:
  * `InaRecorders` dataclass (per-segment list of `h.Vector` handles for `seg.ina`, plus the soma Vm
    vector and time vector for AP detection).
  * `attach_ina_recorders(*, h, cell: MorphologyResult) -> InaRecorders`. Iterates
    `[cell.soma, cell.ais_proximal, cell.ais_distal, *cell.all_dends]` and for each segment
    (`for seg in sec`) attaches `h.Vector().record(seg._ref_ina, RECORD_DT_MS)`. Returns the
    `InaRecorders` aggregate.
  * `detect_ap_windows(*, t_ms: NDArray, v_soma_mv: NDArray, threshold_mv: float = -20.0, refractory_ms: float = 2.0, window_half_ms: float = 2.0) -> list[APWindow]`.
    Returns list of `APWindow(t_start_ms, t_peak_ms, t_end_ms, peak_mv)` for each AP detected via
    threshold crossing.
  * `compute_atp_per_ap(*, recorders: InaRecorders, ap_windows: list[APWindow], cell: MorphologyResult) -> AtpPerApResult`.
    Per AP window: per segment, take `min(I_Na, 0)` pointwise (inward only), integrate via
    trapezoidal rule (`np.trapezoid`) in seconds, multiply by segment surface area
    `seg.area() * 1e-2 / 1e8 = seg.area() * 1e-10 cm^2` (since `seg.area()` is in `um^2`), get
    charge in coulombs. Divide by elementary charge `e = 1.602e-19 C` and by 3 (Na+/K+
    stoichiometry). Sum across segments to get per-AP per-cell ATP. Returns
    `AtpPerApResult(atp_per_ap_total, atp_per_ap_soma, atp_per_ap_ais, atp_per_ap_dends)`.
  * `compute_atp_per_spike(*, atp_per_ap_results: list[AtpPerApResult]) -> float`. Sum total ATP
    across all APs across all trials, divide by total spike count. Returns ATP molecules per spike.
    The headline objective.
* `code/post_hoc_strong_bialek.py` -- a NEW ~250-line standalone post-run script that loads the
  top-10 Pareto cells from `pareto_front_seed<S>.json`, builds each cell via the same
  generator_wrapper + apply_params pipeline used by the NSGA-II inner loop, runs each with 8
  directions x 20 trials in `FULL` mode, calls `compute_mi_strong_bialek_bits_per_sec` from
  `mi_estimator.py`, writes `results/data/post_hoc_strong_bialek_mi_top10.json` with per-cell
  `bits_per_sec`, `std_err`, `mi_count_bits` (the inner-loop value for cross-validation), and
  `atp_per_spike`. Uses the same `_run_one_trial` helper from `evaluator.py` (parameterised by
  `n_directions` and `n_trials_per_direction`).

### Reference data inherited from prior tasks (read-only via [t0122] paths)

* `tasks/t0083_*/results/data/pareto_front.json` -- canonical Bed B best-cell electrophys vector for
  the smoke gate anchor. Loaded via [t0122] `smoke_gate._load_t0083_best_cell_electrophys()`.
* `tasks/t0091_morphology_extended_nsga2_v1/results/data/...` -- joint-pass cell ground truth for
  cross-checks. Not needed for the smoke gate but useful for the post-hoc analysis.
* `tasks/t0093_resweep_and_t0090_correction/results/data/post_fix_verification_summary.json` -- the
  PD-rate ~43.6 Hz fingerprint that the [t0122] smoke gate check 1 reproduces. Inherited verbatim.

## Lessons Learned

### Operator-stop + cost watchdog + N_GEN ceiling is the canonical termination ([t0114], [t0115], [t0122])

[t0114] established and [t0122] confirmed (its run terminated cleanly via the 60/60 gen ceiling)
that disabling HV-plateau auto-stop in favour of
`{MaximumGenerationTermination, CostWatchdogTermination, OperatorStopTermination}` is the right
policy for these runs. The user feedback memory `feedback_disable_hv_plateau_autostop.md` codifies
this. This task's 60-gen ceiling is consistent: the operator will stop the run when HV trajectory
visibly plateaus, and the cost cap will catch any runaway case.

### The 10-gen pool restart is load-bearing for any NSGA-II run > ~25 gens ([t0112], [t0113], [t0114], [t0122])

NEURON accumulates memory in multiprocessing.Pool workers across generations. [t0102] hit OOM at ~25
gens with a single-pool design; [t0112] introduced the `_POOL_RESTART_EVERY = 10` cadence and it has
been preserved verbatim through [t0113], [t0114], [t0115], and [t0122]. This task must not change
this constant. Memory feedback rule: `feedback_nsga2_pool_restart_every_10.md`.

### NSGA-II at pop=96 / N_GEN=60 / N_EVAL_SEEDS=3 lands well under $3 ([t0113], [t0114], [t0115], [t0122])

[t0113] cost $0.48, [t0114] $1.13, [t0115] $2.50 (all 300-gen ceilings), [t0122] $0.50 (60-gen
ceiling). At 4-direction x 3-eval-seed = 12 trials per cell (vs [t0122]'s 6 trials), expect ~$1-2 on
a 60-gen run with the same Vast.ai EPYC tier. The `$6` cap leaves a wide margin. Post-hoc
Strong-Bialek rerun on top-10 cells adds 10 cells x 160 trials = 1600 sims, an additional
$0.20-0.50.

### Carter-Bean 2009 ~4 mM-mol ATP/AP/cm benchmark is the right calibration anchor ([t0097])

Per [t0097]'s ATP recipe (full_answer.md line 360), the cell-aggregate ATP/AP must be compared to
Carter and Bean 2009's ~4 mM-mol ATP per AP per cm of axon at the AIS (~2.41e21 molecules/cm).
Discrepancies > 30% indicate a recipe error (most commonly surface-area conversion: `seg.area()`
returns `um^2`, and converting to cm^2 requires a factor of `1e-8`, not `1e-2`; getting this wrong
yields a 6-order-of-magnitude error). The smoke gate must include this check. The benchmark is for
the AIS specifically because that is where the densest Na channels live in real biology; the rest of
the cell contributes less per unit length but more in aggregate because the dendritic tree length
dwarfs the AIS.

### NEURON's seg.ina is the right substrate variable, not gnabar or ena ([t0080], [t0097])

`seg.ina` is NEURON's automatic sum of all Na-channel currents in a segment. The [t0080] mods folder
ships three Na channels (`nav16t80`, `napt80`, `nart80`) all of which write to the same `ina`
accumulator via the `USEION na READ ena WRITE ina` block in each MOD file. Using `seg.gbar_*` would
give per-channel conductance (not current); using `seg.ena` would give the Na reversal potential
(not current); only `seg.ina` gives the per-segment total Na+ current the Sengupta recipe needs.

### Spike-count MI saturates at log2(N_directions) and is information-poor at low N ([t0097])

The [t0097] catalogue explicitly flagged that "the project's 8-direction protocol may be too
information-poor (only 3 bits of stimulus uncertainty) to give the MI estimator meaningful dynamic
range". With `N_DIRECTIONS = 4` the ceiling is `log2(4) = 2.0 bits`, which is acceptable as a
*relative* selection signal for NSGA-II but compresses the bits/s scale relative to Niven 2007's
200-1000 bits/s curve. This is the two-tier MI architecture's whole point: inner-loop MI_count is a
selector; post-hoc Strong-Bialek MI is the literature-comparable quantity. The post-hoc step is not
optional -- it is the only way to put numbers on the Niven 2007 axis.

### Tracked diagnostics (DSI, PD-rate) must NOT enter F vector even when computed ([t0122])

[t0122] computed PD-rate alongside the F vector and stored it on `CellEvalResult` for downstream
predictions assets, but `out["F"]` only had 2 entries: `[-dsi, +volume]`. This task does the same:
DSI, PD-rate, per-direction firing rates are all computed and stored on `CellEvalResult` and in the
per-cell JSONL row, but `out["F"]` only has 2 entries: `[-mi_count_bits, +atp_per_spike]`. This
keeps the optimiser focused on the 2 declared objectives and avoids confounding the Pareto front
with auxiliary axes.

### Direct method requires careful word-length sweep selection ([t0097])

The [t0097] recipe specifies `T in {25, 50, 75, 100} ms` with `dt = 5 ms` giving word lengths
`L in {5, 10, 15, 20} bits`. The pooled word distribution must be estimated with enough samples per
word to avoid bias. At 8 directions x 20 trials = 160 trials, and each trial of 1400 ms duration
produces `1400/T` non-overlapping words at length T: 56 words at T=25 ms, 28 at T=50, 18 at T=75, 14
at T=100. Total per-T sample sizes: ~9000, ~4500, ~3000, ~2200 words. The Strong-Bialek estimator's
bias grows as `2^L / N_words`, so the largest word length (T=100, L=20 -> 2^20 ~ 1e6 possible words,
only 2200 observed) is the noisiest. Per [t0097] step 5, the optional Panzeri- Treves NSB correction
can be used as a second estimator; for this task, scipy.stats.linregress on the 4 (T, MI_at_T/T)
points with R^2 reporting is the minimum-viable validation.

## Recommendations for This Task

1. **Fork [t0122] verbatim** as the base. Copy every file in
   `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` into
   `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/`, then run a global search-and-replace from
   `t0122_dsi_cytoplasm_volume_nsga2` to `t0123_bedb_mi_atp_per_spike_nsga2`. Do NOT redesign.

2. **Edit only what changes**: the objective vector becomes `(-mi_count_bits, +atp_per_spike)`;
   `N_DIRECTIONS` becomes 4; a per-segment `seg.ina` recording is bolted onto `_run_one_trial`;
   AP-window detection and ATP integration happen inline after `h.run()` returns; the new GA seed is
   drawn via `secrets.randbelow(10000)` (avoid round numbers per [t0113] convention); HV reference
   point and utopia constants are tuned for the new objectives.

3. **Add `mi_estimator.py` and `atp_per_spike.py` as NEW modules** following the [t0122]
   `cytoplasm_volume.py` + `cuntz_balancing_factor.py` pattern (clean, dependency-light, per-cell
   computation called from `evaluator.evaluate_68d_vector`). Both are NumPy-only plus
   `scipy.stats.linregress` for the post-hoc Strong-Bialek fit and
   `sklearn.metrics.mutual_info_score` for the inner-loop plug-in MI.

4. **Add `post_hoc_strong_bialek.py` as a NEW standalone script** that re-runs the top-10 Pareto
   cells at 8 directions x 20 trials per direction and computes the bits/s direct-method MI. The
   script is invoked AFTER the NSGA-II run completes and consumes ~$0.20-0.50 of the budget.

5. **Reuse [t0122]'s `build_top50_morphologies.py` verbatim** (only seed-string edits) for the
   full-dendrite-tree top-50 chart. ADD two NEW post-run plots:
   `results/images/pareto_front_mi_vs_atp.png` (mirror of [t0122]'s pareto chart) and
   `results/images/niven_2007_comparison.png` (top-10 cells in (ATP/spike, bits/s) space with the
   Niven 2007 4-species fly curve overlaid).

6. **Carter-Bean 2009 smoke gate is non-negotiable.** Before launching NSGA-II, compute ATP/AP/cm at
   the AIS on the canonical [t0083] Bed B best-cell electrophys vector, compare to `~4 mM-mol/cm` =
   `2.41e21 ATP/cm`, abort if deviation > 30%. The most likely failure mode is a `seg.area()`
   unit-conversion bug. Defer this check to the remote machine (no NEURON locally).

7. **Reuse [t0122]'s setup-remote-machine pattern**: Vast.ai EPYC 32-core or 64-core single instance
   at whichever is cheapest at provisioning time, `nrnivmodl` build of the [t0080] mods folder,
   `bash tasks/t0123_*/code/run_seed<S>.sh` driving the single seed. Plan must include a
   per-instance watchdog of $5 (leaves $1 buffer below the $6 task cap) and a
   `--teardown-on-watchdog` flag invocation. Cost expectation is $1-3 actual.

8. **Tracked diagnostics policy**: DSI, PD-rate, and per-direction firing rates are computed and
   stored on `CellEvalResult` for downstream predictions-asset rows and `compare_literature.md`, but
   do NOT enter `out["F"]`. The silence guard `pd_spikes_sum < 3` remains as defensive filtering for
   the LEGIT cohort, even though DSI is not optimised.

9. **One GA seed only**. Per the task description ("1 GA seed, pop=96, N_EVAL_SEEDS=3") and per
   [t0113]'s precedent (`secrets.randbelow(10000)`). Avoid round-ish numbers like 1000, 5000, 9000.

10. **Do NOT touch the morphology generator or its [t0092] patch.** [t0120]'s audit confirmed the
    geometry is correct; the gating dependency is satisfied. ATP per spike is computed from the
    `seg.area()` returned by NEURON on the patched morphology, which is the correct surface area for
    the realised geometry.

11. **Headline answer asset**: write `assets/answer/dsgc-bits-per-atp-vs-niven-2007/` with the
    answer to "Where does the DSGC bits-per-ATP front sit relative to Niven 2007's fly-photoreceptor
    curve, and does it match the Niven super-linear cost-vs-information scaling?". Use [t0122]'s
    `build_assets.py` as the structural template.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port the de Rosenroll 2026 DSGC compartmental model
* **Status**: completed
* **Relevance**: Provides the canonical Bed B cell, NEURON bootstrap, AR(2) noise generator, and
  bar-arrival kinematic helpers that the [t0122] fork imports by full dotted path.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Source of the 54-d electrophys parameter scheme, `apply_parameter_vector`, the
  13-channel SUFFIX MOD library compiled into `code/mods/`, and `ensure_t80_dll_loaded`. The three
  Na channels `nav16t80`, `napt80`, `nart80` all write to `seg.ina` which is the substrate variable
  of the Sengupta 2010 ATP-per-spike recipe.

### [t0083]

* **Task ID**: `t0083_bedb_v3_extend_nsga2_gen8plus`
* **Name**: Bed B v3 extended NSGA-II run (continued from gen 8+)
* **Status**: completed
* **Relevance**: Source of the canonical Bed B best-cell electrophys vector used as the smoke-gate
  anchor (`tasks/t0083_*/results/data/pareto_front.json`). The [t0122] smoke-gate check 1 loads this
  file via `_load_t0083_best_cell_electrophys()` and asserts PD-rate ~43.6 Hz within +/- 2 Hz. This
  task inherits the same anchor for both the existing checks and the NEW Carter-Bean ATP/AP/cm smoke
  check.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator diversity test
* **Status**: completed
* **Relevance**: Defines the 14-d morphology parameter space, `MorphologyParams`,
  `MorphologyResult`, `PARAM_BOUNDS`, `INT_PARAM_NAMES`. `MorphologyResult.soma`, `.all_dends`,
  `.ais_proximal`, `.ais_distal` are the `h.Section` handles whose segments (`for seg in sec`) the
  t0123 task attaches `seg._ref_ina` recorders to.

### [t0091]

* **Task ID**: `t0091_morphology_extended_nsga2_v1`
* **Name**: First joint 68-d NSGA-II with morphology generator in-loop
* **Status**: completed
* **Relevance**: Original 68-d NSGA-II run. Established the
  `angles_deg = [float(d) * (360.0 / n_directions) for d in range(n_directions)]` formula for
  arbitrary `N_DIRECTIONS` at line 398 of `evaluator.py`. The t0123 task uses the same formula to
  get 4 directions [0, 90, 180, 270]. Pre-NSGA-II scorecard showed pure-DSI optimisation lands in
  biologically implausible channel- density regions, motivating the move to function-vs-cost
  objectives like MI-vs-ATP.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology generator silence (soma area bug)
* **Status**: completed
* **Relevance**: Provides `generate_fixed_morphology` (the canonical morphology entry point per
  C-0093-01) and `insert_baseline_channels`. The z-axis soma patch ensures `seg.area()` returns the
  intended `~220 um^2` surface area; getting `seg.area()` wrong would break the ATP unit conversion
  catastrophically.

### [t0097]

* **Task ID**: `t0097_multi_obj_optim`
* **Name**: Multi-objective single-neuron optimisation literature catalogue
* **Status**: completed
* **Relevance**: **The defining catalogue task.** Provides the
  `mutual_information_stimulus_spike_train` recipe (Strong et al. 1998 direct method with 1/T
  extrapolation) and the `metabolic_energy_atp_per_spike` recipe (Sengupta et al. 2010 with the
  Na+/K+ stoichiometry factor of 1/3 and Carter and Bean 2009 calibration anchor). Provides the
  source paper 10.1103/PhysRevLett.80.197 (Strong 1998) and the Niven 2007 fly-photoreceptor
  reference curve that t0123's headline chart compares against. Suggestion S-0097-05 is the direct
  source of this task.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: 68-d random-init NSGA-II seed-scale at N_EVAL_SEEDS=4 / N_GEN=20
* **Status**: completed
* **Relevance**: Discovered the DSI = 1.0 silence-corner artefact and introduced the silence guard
  whose tightened threshold (3 PD spikes) the t0123 task inherits through the [t0122] fork.

### [t0112]

* **Task ID**: `t0112_t0106_seed77_replicate`
* **Name**: Seed-77 NSGA-II replicate of t0106 (substrate-rate confirmation)
* **Status**: completed
* **Relevance**: Introduced and operator-endorsed the `_POOL_RESTART_EVERY = 10` cadence (the "10th
  gen rule" per memory `feedback_nsga2_pool_restart_every_10.md`). This task preserves the constant
  verbatim through the [t0122] fork.

### [t0113]

* **Task ID**: `t0113_t0106_seed2247_replicate`
* **Name**: Seed-2247 NSGA-II replicate of t0106
* **Status**: completed
* **Relevance**: Established the `secrets.randbelow(10000)` GA seed convention (avoid round
  numbers). Confirmed the $0.48 lower bound on the expected cost envelope on 60-gen runs.

### [t0114]

* **Task ID**: `t0114_seed7755_no_autostop`
* **Name**: t0113 replica with HV-plateau auto-stop disabled (seed 7755)
* **Status**: completed
* **Relevance**: Established the "no auto-stop, operator-driven stop" termination convention.
  Demonstrated the $1.13 cost envelope at 300-gen ceiling. Failure mode (`top50_morphologies_*` drew
  only soma dots) is the cautionary tale that drives the t0123 task's full-dendrite-tree rendering
  requirement.

### [t0115]

* **Task ID**: `t0115_seed9354_no_autostop`
* **Name**: Seed-9354 NSGA-II replicate with HV-plateau auto-stop disabled
* **Status**: completed
* **Relevance**: Second-seed confirmation of [t0114]'s "no auto-stop" convention. Source of the
  763-line `nsga2_driver.py` design (forked into [t0122] and then this task). The [t0122] fork
  changed the cost cap and seed; this task inherits the entire driver pattern through [t0122].

### [t0116]

* **Task ID**: `t0116_pooled_pca_cluster_factor_dsi07_pd10`
* **Name**: Pooled-PCA cluster + factor analysis on DSI>=0.7 / PD>=10 cohort
* **Status**: completed
* **Relevance**: Established the `sklearn.metrics.normalized_mutual_info_score` usage pattern at
  `cluster_seed_purity.py` line 18. The t0123 inner-loop MI estimator follows the same import + call
  structure with `mutual_info_score` (returns nats; convert to bits via division by ln(2)).

### [t0117]

* **Task ID**: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
* **Name**: Pooled-PCA cluster + factor analysis (all 4 seeds, no DSI/PD filter)
* **Status**: completed
* **Relevance**: Second-time use of the sklearn MI pattern; confirms the import path and call
  signature are stable. `cluster_seed_purity.py` line 19 is the canonical usage.

### [t0122]

* **Task ID**: `t0122_dsi_cytoplasm_volume_nsga2`
* **Name**: NSGA-II maximising DSI and minimising cytoplasm volume (Bed B + 14-d morph)
* **Status**: completed
* **Relevance**: **THE direct fork point**. Every code file in t0123's `code/` is copied verbatim
  from `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` and minimally patched. The 776-line
  `nsga2_driver.py`, 608-line `evaluator.py`, 543-line `smoke_gate.py`, and 323-line
  `build_top50_morphologies.py` are the load-bearing source files. [t0122]'s clean termination at
  60/60 gens for $0.50 confirms the substrate is healthy and the cost envelope is comfortable.

### [t0120]

* **Task ID**: `t0120_morph_generator_geometry_audit`
* **Name**: Morphology generator geometry audit
* **Status**: completed
* **Relevance**: **GATING DEPENDENCY** (transitive from [t0122]). Verdict: "rendering-only artefact,
  no NSGA-II re-runs needed." 60/60 coordinate-consistency checks pass means the realised dendrite
  geometry that the ATP recipe iterates over is correct. No need to patch `_apply_asymmetry`.
