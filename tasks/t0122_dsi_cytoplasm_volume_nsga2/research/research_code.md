---
spec_version: "1"
task_id: "t0122_dsi_cytoplasm_volume_nsga2"
research_stage: "code"
tasks_reviewed: 14
tasks_cited: 12
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-05-24"
status: "complete"
---
# Research Code: NSGA-II Maximising DSI and Minimising Cytoplasm Volume

## Task Objective

This task forks the t0115 single-seed 68-d Bed B + 14-d morphology NSGA-II substrate and replaces
the PD-rate objective with a cytoplasm-volume cost objective. Objectives become (maximise DSI,
minimise cytoplasm volume, the latter computed as `sum(pi * (sec.diam/2)^2 * sec.L)` over soma + all
dendrites + AIS proximal + AIS distal). Hard constraints are `_POOL_RESTART_EVERY=10`,
`HV_PLATEAU_AUTO_STOP=False`, `POP_SIZE=96`, `N_EVAL_SEEDS=3`, `N_GEN_MAX=60`, `COST_CAP_USD=6.0`
(Vast.ai balance $7). Gating dependency t0120 has been completed with verdict "rendering-only / no
re-runs needed", so this task is unblocked. The implementation must reuse t0115's 68-d substrate
end-to-end and bolt on a new cytoplasm-volume function before evaluation returns its objective
vector.

## Library Landscape

The project does not currently expose a library aggregator (`arf/scripts/aggregators/` ships only
`aggregate_categories`, `aggregate_costs`, `aggregate_machines`, `aggregate_metric_results`,
`aggregate_metrics`, `aggregate_suggestions`, `aggregate_task_types`, `aggregate_tasks`). There is
therefore no registered `assets/library/` collection to enumerate. All cross-task code reuse in this
lineage is by the "copy into task" convention: each NSGA-II task forks the prior task's `code/`
directory verbatim and overrides only what changes. The procedural morphology generator and its
t0092 patch wrapper are cited as cross-task imports in [t0091], [t0099], [t0102], [t0106], [t0112],
[t0114], and [t0115] using full repo-rooted dotted paths
(`tasks.t0090_morphology_generator_diversity_test.code.generator.generate_morphology` and
`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`).
The t0024 de Rosenroll port (NEURON bootstrap, AR(2) noise generator, bar arrival kinematics) is
likewise imported by full path from `tasks.t0024_port_de_rosenroll_2026_dsgc.code`. The t0080
compiled NEURON MOD library (`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`) is the
shared `nrnmech` namespace used by all 68-d morphology-extended runs and must be compiled with
`nrnivmodl` on the remote machine. There are no registered library assets to import; all reuse must
be by code copy + fork, with the morphology generator path being the one exception that is
canonically loaded by dotted-path import.

## Key Findings

### Fork-the-most-recent NSGA-II driver, do not redesign

[t0115] is the most recent task in the 68-d NSGA-II lineage and is the single canonical fork point
for this task. The driver `tasks/t0115_seed9354_no_autostop/code/nsga2_driver.py` (763 lines)
carries every load-bearing convention this task needs: pure LHS init via
`tasks/t0115_seed9354_no_autostop/code/random_init.py` (102 lines, uses
`pymoo.operators.sampling.lhs.LatinHypercubeSampling`), `OperatorStopTermination` polling
`intervention/stop.md`, `CostWatchdogTermination` reading `T0114_HARD_BUDGET_USD` from
`code/constants.py`, the `PerGenerationPoolRestart` callback firing every `_POOL_RESTART_EVERY = 10`
generations (line 104 of `nsga2_driver.py`), per-gen dill checkpoints to
`logs/steps/009_implementation/checkpoints/checkpoint_seed<S>_gen<NNNN>.pkl`, and per-gen JSONL
writes to `hv_trace.jsonl`. `HVPlateauTermination` is intentionally NOT in the live
`TerminationCollection` (lines 191-210); the live termination is
`{MaximumGenerationTermination, CostWatchdogTermination, OperatorStopTermination}` — exactly the
combination this task needs. [t0114] established the "no auto-stop, run until visible plateau"
convention and [t0115] confirmed it on a second random seed.

### Cytoplasm volume must be computed from the realised `h.Section` geometry

The morphology generator returns a `MorphologyResult`
(`tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` lines 131-156) whose
fields `soma`, `all_dends`, `ais_proximal`, `ais_distal` are live NEURON `h.Section` handles. Each
`h.Section` exposes `sec.L` (length in um) and `sec.diam` (diameter in um); nseg-level segments
expose `seg.diam` per sub-segment. The cytoplasm-volume formula

```
vol_um3 = sum(pi * (sec.diam / 2.0)**2 * sec.L
              for sec in [soma, *all_dends, ais_proximal, ais_distal])
```

is computable from these handles without any NEURON simulation step. It is therefore a pure
geometric quantity that can be evaluated immediately after `_ensure_worker_cell` builds the cell
(see `tasks/t0115_seed9354_no_autostop/code/evaluator.py` lines 119-132) and before the trial loop
starts. The soma is patched by [t0092]'s `_patch_soma_geometry` (line 61 of
`morphology_generator_fix.py`) so `sec.L` for soma equals `params.soma_diameter_um` and `sec.diam`
equals `BEDB_AREA_TARGET_UM2 / (pi * soma_diameter_um)`; the volume formula is correct against the
patched geometry. AIS sections come from `tasks/t0115_seed9354_no_autostop/code/extend_with_ais.py`
(128 lines): proximal length = `AIS_PROXIMAL_FRACTION * total_length`, distal length =
`total_length - proximal_length`, both share the same `params.ais_diameter_um`. The AIS diameter is
fixed (`AIS_DEFAULT_DIAMETER_UM`) in the 68-d substrate's electrophys block, not a search-space
dimension.

### Soma-frame split is benign per [t0120]; no re-runs needed

[t0120] audited the t0092 z-axis soma patch on 20 cells stratified across asymmetry-parameter
extremes plus symmetric controls and confirmed all 60 coordinate-consistency checks pass (3 checks
per cell x 20 cells). The deliberate soma-frame split is benign; prior 68-d NSGA-II results from
[t0091], [t0099], [t0102], [t0104], [t0106], [t0112], [t0114], [t0115], and [t0118] remain valid,
and the visual disconnect in t0115's top-50 morphology grid was a rendering-only artefact. [t0120]'s
verdict explicitly says "t0122_dsi_cytoplasm_volume_nsga2 is unblocked", which satisfies the gating
dependency. This task must NOT patch `_apply_asymmetry`; the geometry the optimiser sees is correct.

### Pure-DSI optimisation hits biologically implausible Nav/NMDA densities

[t0091]'s very first 68-d run produced one strict joint-pass cell (DSI = 0.511, PD = 35.1 Hz,
robustness = 0.79) but **zero cells passed the biological-plausibility scorecard**; the optimiser
pushed channel densities into territory 85-122 sigma above the Sivyer 2013 prior. The [t0121]
canonical 5-seed report (bootstrap 95% CI +0.38% to +5.53%, point estimate **6.5x above** the Hay
2011 envelope) only sharpens the same concern: the 68-d substrate is unrealistically populated when
DSI alone (or DSI + PD-rate) is the objective. The cytoplasm-volume objective in this task is the
direct biological-cost remedy: cells with extreme channel-pumping morphologies will also have
extreme cytoplasm budgets and will be dominated on the volume axis. This is the mechanism by which
the Cuntz 2010 balancing-factor `bf in [0.2, 0.7]` band test in the task description becomes a
falsifiable prediction.

### NSGA-II at pop=96 / N_GEN=60 lands in the $1-3 cost band on the Vast.ai EPYC pipeline

[t0113] cost $0.48, [t0114] cost $1.13, and [t0115] cost $2.50 — all well below the $4 (t0113), $8
(t0114), and $25 (t0115) hard caps. This task's **$6 cap** (REDUCED from $8 because of the $7
Vast.ai balance) leaves the same $1-3 expected actual band. The per-gen wall-clock is dominated by
96 cells x 6 trials each (3 eval seeds x 2 directions) of 1400 ms simulated NEURON time on an EPYC
32/64-core Vast.ai instance. The [t0115] driver's `n_workers = min(60, max(1, cpu_count - 4))`
formula gives 28 workers on a 32-core instance and 60 workers on a 64-core instance; the remaining 4
cores stay free for the Pool restart pattern.

### Cytoplasm volume should be an evaluator-level objective, not a Problem-level constraint

The pymoo `BedBV3MorphProblem` in `tasks/t0115_seed9354_no_autostop/code/evaluator.py` (line 466)
has `n_obj=2` and writes `out["F"] = np.array([-result.dsi_vector_sum, -result.pd_rate_hz])`. The
cleanest fork in this task is to keep `n_obj=2` but redefine the second column:
`out["F"] = [-dsi, +volume_um3]`. The volume is positive and minimised, so it is NOT negated. The
first column stays negated because DSI is maximised. The `CellEvalResult` dataclass at line 92 must
grow a `cytoplasm_volume_um3: float` field so the predictions-asset writer can surface it. PD-rate
remains computed and stored on `CellEvalResult` (as the task description requires) but does not
enter `out["F"]`. The HV reference point and utopia constants must change: HV's two-entry
`REF_POINT_HV = (0.0, 0.0)` works for any two-axis F as long as both objectives are minimised with
the right sign, so `(-DSI, +volume)` -> `REF_POINT_HV` becomes something like `(0.0, V_max_um3)` for
some pessimistic volume cap. The `HV_UTOPIA_DSI` constant
(`tasks/t0115_seed9354_no_autostop/code/constants_morphology.py` line 138) carries over verbatim
(`0.7`); a new `HV_UTOPIA_VOLUME_UM3` constant must be added with a Cuntz-informed target value.

### The silence-guard threshold = 3 PD spikes must be tightened from [t0115]'s implicit ~10 mean

[t0115]'s evaluator uses `SILENCE_SPIKE_COUNT_THRESHOLD: int = 10` (line 109 of `evaluator.py`) on
the **total mean spike count across 16 directions** — not on PD-spikes alone. This task's
description requires the silence-guard be tightened to ">=3 PD spikes". This is a single- line
behavioural change: replace the `total_mean_spikes < 10` gate with a `pd_spikes_sum < 3` gate inside
`_summarise_trials` (line 298). The change shrinks the DSI = 1.0 silence-corner artefact further
than [t0115] did, which is necessary because cytoplasm-volume optimisation prefers tiny cells, and
tiny cells have the highest silence-corner risk.

### NEURON DLL is shared with t0080 across the lineage

Every 68-d morphology task in this lineage imports `ensure_t80_dll_loaded` from
`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params` (see line 47-58 of
`tasks/t0115_seed9354_no_autostop/code/apply_params.py`). This task must do the same — there is NO
need to recompile a t0122-specific nrnmech library. The 12 channel SUFFIXes `nav16t80`, `napt80`,
`nart80`, `kdrt80`, `kv3t80`, `kv4t80`, `kv7t80`, `iht80`, `calt80`, `catt80`, `bkt80`, `skahpt80`
plus the t0024 `HHst`, `cad`, `Exp2NMDA` are all loaded by the t0080 loader. The Vast.ai bootstrap
step compiles `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` with `nrnivmodl` into
`x86_64/.libs/libnrnmech.so`; the path is resolved by
`tasks/t0115_seed9354_no_autostop/code/paths.py` lines 36-49 (`resolve_t99_mod_library`).

### Top-N morphology grids must draw full dendrite trees (memory feedback rule)

Per [t0115]'s `build_top50_morphologies.py` (308 lines) and the explicit operator-feedback memory
`feedback_top50_morphologies_full_dendrites.md`, the `top50_morphologies_seed*.png` chart in this
task must use `LineCollection` over `section_endpoints_xy.items()` excluding soma and AIS, with the
soma drawn as a separate `Circle` patch. [t0114] failed this rule and was rejected; [t0115] complied
and the visual sanity check passed. This task must replicate [t0115]'s `build_top50_morphologies.py`
verbatim with the only diff being the input filename (`all_evaluations_seed<new_seed>.json`) and the
seed embedded in the output filename.

### The 5-seed canonical report [t0121] is the headline comparison baseline

[t0121] consolidated the t0106/t0112/t0113/t0114/t0115 5-seed batch (single-objective ratio-DSI
substrate-rate) with harmonised LEGIT-only conventions, normal-approx + bootstrap 95% CIs, and a Hay
2011 / Druckmann 2007 / Mohacsi 2024 literature comparison table. This task's analysis must
reference [t0121]'s **5-seed mean 2.58% +/- SE 1.50%** as the baseline yield to beat (or fall under,
if the cytoplasm-volume objective is restrictive enough to push the Pareto front into a more
selective regime). [t0121]'s `compare_literature.md` template should be followed verbatim for this
task's comparison row against Cuntz 2010 / Hay 2011 / Mohacsi 2024.

### Random-init only (no anchor warm-start)

The [t0115] lineage uses LHS init (96 rows x 68 dims) drawn from `np.random.SeedSequence(seed)` via
pymoo's `LatinHypercubeSampling`. NO anchor warm-start. The `n_var=68` problem in `evaluator.py` has
`xl=LOWER_BOUNDS_68`, `xu=UPPER_BOUNDS_68` from `constants_morphology.py`, which concatenates
t0080's 54-d electrophys bounds with t0090's 14-d morphology bounds. This task inherits this
verbatim. The GA seed must be drawn via `secrets.randbelow(10000)` per the [t0113] convention
(task-description constraint).

## Reusable Code and Assets

### From [t0115] — copy into task

The following files in `tasks/t0115_seed9354_no_autostop/code/` are the this task fork base. All
should be copied verbatim into `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` and then minimally
patched:

* `nsga2_driver.py` (763 lines) — **copy and edit**: change all
  `tasks.t0115_seed9354_no_autostop.code.*` imports to
  `tasks.t0122_dsi_cytoplasm_volume_nsga2.code.*`; default `N_GEN` to 60 (was 300); keep
  `_POOL_RESTART_EVERY = 10`. Function
  `run_nsga2_for_seed(*, task_seed, n_gen_override=None, step_id="009_implementation") -> dict[str, object]`.
* `evaluator.py` (504 lines) — **copy and edit**: tighten silence guard from
  `total_mean_spikes < 10` to `pd_spikes_sum < 3`; add `cytoplasm_volume_um3: float` field to
  `CellEvalResult`; rewrite `BedBV3MorphProblem._evaluate` to emit `out["F"] = [-dsi, +volume_um3]`;
  keep PD-rate tracked on the dataclass. Function
  `evaluate_68d_vector(*, vector_68d, eval_seeds=None, n_directions=N_DIRECTIONS) -> CellEvalResult`.
* `generator_wrapper.py` (105 lines) — **copy verbatim** (only changes are import path rewrites).
  Functions: `build_cell(*, h, morph_params)`, `morphology_params_from_vector`, `split_68d_vector`,
  `hash_morphology_vector`.
* `trial_helpers.py` (311 lines) — **copy verbatim** (import path rewrites only). Function
  `setup_synapses_parametric(*, cell, n_ach, n_gaba, rho_0_ach, lambda_ach_um, rho_0_gaba, lambda_gaba_um, w_ach_us, w_gaba_us, placer_seed, gnmda_dend, mg_conc_mm, voff_nmda) -> SynapseBundle`.
* `apply_params.py` (234 lines) — **copy verbatim** (import path rewrites only). Function
  `apply_parameter_vector(*, cell, params)`.
* `build_cell_ais.py` (79 lines) — **copy verbatim** (import path rewrites only). Dataclass
  `DSGCCellWithAIS`.
* `extend_with_ais.py` (127 lines) — **copy verbatim** (import path rewrites only). Functions
  `extend_with_ais`, `update_ais_geometry`, `_compute_nseg`.
* `parametric_placer.py` (105 lines) — **copy verbatim** (import path rewrites only). Function
  `place_synapses(*, h, soma, candidate_sections, n_target, rho_0, lambda_um, seed)`.
* `constants.py` (126 lines) — **copy and edit**: rename `T0115_SEEDS` -> `T0122_SEEDS = (X,)`
  where `X` is drawn via `secrets.randbelow(10000)`; set `T0122_HARD_BUDGET_USD = 6.0` and
  `T0122_PER_INSTANCE_WATCHDOG_USD = 5.0`; re-export the 68-d bounds.
* `constants_morphology.py` (160 lines) — **copy and edit**: set `N_GEN = 60` (was 300); add
  `HV_UTOPIA_VOLUME_UM3` constant; change `REF_POINT_HV` to a two-entry pessimistic
  `(0.0, V_max_um3)` pair so the HV indicator works on the new F sign convention. Keep
  `POP_SIZE = 96`, `N_EVAL_SEEDS = 3`, `N_DIRECTIONS = 2`. Keep the 14-d morphology bounds and the
  t0080 54-d bounds concatenation.
* `constants_electrophys.py` (547 lines) — **copy verbatim**.
* `cost_watchdog.py` (129 lines) — **copy verbatim** (constant `T0104_HARD_BUDGET_USD = 4.00` in
  the file is the default for the dataclass; the watchdog is built with
  `T0122_HARD_BUDGET_USD = 6.0` at the driver call site).
* `hv_plateau_watchdog.py` (89 lines) — **copy verbatim** (intentionally NOT live, but the smoke
  gate REQ-8 introspection imports it).
* `random_init.py` (101 lines) — **copy and edit**: import `T0122_SEEDS` instead of `T0114_SEEDS`.
* `paths.py` (218 lines) — **copy and edit**: change `TASK_ROOT` resolution
  (`Path(__file__) .resolve().parent.parent` carries through unchanged because the file is in the
  new task folder); update T0091/T0083/T0099 reference data paths so they point to the existing
  source tasks (no change to the path strings themselves, since they hop out of the task folder by
  name).
* `bootstrap.py` (161 lines) — **copy verbatim** (import path rewrites only).
* `build_top50_morphologies.py` (308 lines) — **copy and edit**: rename hard-coded
  `t0115_seed9354_no_autostop` to `t0122_dsi_cytoplasm_volume_nsga2`; change input
  `all_evaluations_seed9354.json` -> `all_evaluations_seed<NEW_SEED>.json`; change output
  `top50_morphologies_seed9354.png` -> `top50_morphologies_seed<NEW_SEED>.png`. Full dendrite tree
  rendering preserved verbatim per the memory rule.
* `smoke_gate.py` (398 lines) — **copy and edit**: REQ-8 introspection of the live
  `TerminationCollection` already excludes `HVPlateauTermination` in the [t0115] version.
* `test_evaluator_dsi_guard.py` (164 lines) — **copy and edit**: update the silence-guard
  threshold the test expects (from `>= 10` to `>= 3 PD spikes`).
* `metrics_builder.py` (81 lines) — **copy and edit**: replace the PD-rate variant with a
  cytoplasm-volume variant; keep `best_legit`, `overall_max`, `dsi_eq_one_count` variants of
  `direction_selectivity_index`; ADD `cytoplasm_volume_um3` metric with variants `min_legit`,
  `mean_top10`, `cuntz_bf_in_band_count`.

### From [t0090] — already imported by full dotted path (do not copy)

The [t0115] generator_wrapper imports
`tasks.t0090_morphology_generator_diversity_test.code.morphology_params.MorphologyParams` and
`MorphologyResult` and the
`tasks.t0090_morphology_generator_diversity_test.code.constants.PARAM_NAMES`, `PARAM_BOUNDS`,
`INT_PARAM_NAMES`, and 14 individual `PARAM_*` string constants. This task should NOT copy these;
the project precedent (codified in C-0093-01 per the comment at line 20 of [t0115]
`generator_wrapper.py`) is to import them by full path.

### From [t0092] — already imported by full dotted path (do not copy)

`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`
and
`tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels.insert_baseline_channels`
are imported by [t0115] `generator_wrapper.py` and must continue to be imported by full path from
this task. This is the canonical morphology entry point per C-0093-01.

### From [t0024] — already imported by full dotted path (do not copy)

`tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell._ensure_neuron_on_path`,
`tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise.generate_ar2_batch`, and the constants
module are imported by [t0115] code. This task inherits these imports through the verbatim copy of
`trial_helpers.py`.

### From [t0080] — already imported by full dotted path (do not copy)

`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params.ensure_t80_dll_loaded` is the
process-singleton NEURON MOD library loader; the compiled
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` directory must exist on the remote
machine (it ships in the repo with pre-compiled `.c` and `.o` files; `nrnivmodl` rebuilds the `.so`
once per machine).

### New code to write from scratch in this task

* `code/cytoplasm_volume.py` — a NEW ~30-line module with one function
  `compute_cytoplasm_volume_um3(*, cell: MorphologyResult) -> float` that iterates
  `[cell.soma, *cell.all_dends, cell.ais_proximal, cell.ais_distal]` and returns
  `sum(math.pi * (sec.diam / 2.0) ** 2 * sec.L for sec in sections)`. Add a sister function
  `compute_per_section_volume_breakdown(*, cell) -> dict[str, float]` returning
  `{soma_um3, dendrites_um3, ais_um3}` for the `results_detailed.md` per-section breakdown required
  by the task description's Verification Criteria.
* `code/cuntz_balancing_factor.py` — a NEW ~50-line module with one function
  `compute_balancing_factor(*, cell: MorphologyResult) -> float` implementing the Cuntz 2010 `bf`
  formula (the ratio of total wiring cost to total signal-conduction cost across the dendritic
  tree). The Cuntz 2010 paper defines `bf` as a parameter swept in `[0, 1]` whose optimum for real
  DSGC dendrites is `[0.2, 0.7]`. Implementation follows the paper's algorithm: bf =
  (total_wiring_length_um) / (total_wiring_length_um + sum_of_path_distances_to_soma_um). Used only
  in post-processing for the top-10 cells, not in the optimiser loop.
* `code/build_pareto_plots.py` — a NEW post-run script producing
  `results/images/pareto_front_dsi_vs_volume.png` (the headline Pareto chart) and
  `results/images/cuntz_balancing_factor_top10.png` (bf distribution for top-10 cells with the Cuntz
  [0.2, 0.7] band overlaid). Reuse matplotlib + `LineCollection` patterns from
  `build_top50_morphologies.py`.

## Lessons Learned

### Operator-stop is the canonical termination trigger for ratio-DSI runs ([t0114], [t0115])

[t0114] established and [t0115] confirmed that disabling HV-plateau auto-stop in favour of
operator-stop + cost watchdog + N_GEN ceiling is the right termination policy for these runs. The
user-feedback memory `feedback_disable_hv_plateau_autostop.md` records the standing project policy.
this task's 60-gen ceiling is consistent with this: the operator will stop the run when the HV
trajectory visibly plateaus, and the cost cap will catch any runaway case.

### The 10-gen pool restart is load-bearing for run-length > ~25 gens ([t0112], [t0113], [t0114])

NEURON accumulates memory in multiprocessing.Pool workers across generations. [t0102] hit OOM at ~25
gens with a single-pool design; [t0112] introduced the `_POOL_RESTART_EVERY = 10` cadence and it has
been preserved verbatim through [t0113], [t0114], and [t0115]. This task must not change this
constant.

### Pure-DSI optimisation is biologically implausible ([t0091], [t0078] background)

The whole rationale for the cytoplasm-volume objective in this task is that the 68-d substrate
without a biological cost objective lands the Pareto front in channel-density regions that are
85-122 sigma above the Sivyer 2013 NMDA / Nav priors. [t0091]'s scorecard found zero
biologically-plausible cells in its 57-cell Pareto front. Adding a cytoplasm cost is the remedy this
task is designed to test.

### Silence-corner artefact is the dominant DSI = 1.0 inflation ([t0102], [t0115])

[t0102] discovered the original DSI = 1.0 silence-corner artefact: when a cell fires almost no
spikes anywhere, division by a near-zero `total_spikes_f` in `_vector_sum_dsi` yields spurious DSI =
1.0. [t0115]'s evaluator inherits the [t0102] fix at line 109 (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`
on total mean spikes). This task must tighten this further because cytoplasm-minimisation pushes the
optimiser toward tiny cells with low total spike counts, which is exactly the silence-corner regime.

### Top-N morphology grids must show dendrite trees, not just somas ([t0114] failure)

[t0114]'s `top50_morphologies_seed7755.png` drew only soma dots and was rejected by the operator
(memory `feedback_top50_morphologies_full_dendrites.md`). [t0115] fixed this by iterating
`result.section_endpoints_xy.items()` and drawing every non-soma, non-AIS section as a
`LineCollection` segment. This task must follow the [t0115] pattern verbatim.

### Vast.ai EPYC instances at $0.15-0.40/hr are the right tier for this workload ([t0113], [t0114], [t0115])

[t0113] $0.48, [t0114] $1.13, [t0115] $2.50 total spend confirms the EPYC 32/64-core tier is
correctly priced for 60-300 gen NSGA-II runs. The Vast.ai `selected_offer.price_per_hour` in
`logs/steps/008_setup-machines/machine_log.json` is the source of truth for the cost watchdog; the
runtime hourly rate must be read from the file at startup, not hard-coded.

## Recommendations for This Task

1. **Fork [t0115] verbatim**. Copy every file in `tasks/t0115_seed9354_no_autostop/code/` into
   `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/`, then run a global search-and-replace from
   `t0115_seed9354_no_autostop` to `t0122_dsi_cytoplasm_volume_nsga2`. Do NOT redesign.

2. **Edit only what changes**: the cytoplasm-volume objective, the tightened silence guard, the
   N_GEN=60 ceiling, the $6 hard cap, the new seed drawn via `secrets.randbelow(10000)`, and the new
   constants `HV_UTOPIA_VOLUME_UM3` + `REF_POINT_HV` second entry. Plus the metrics_builder change.

3. **Add `cytoplasm_volume.py` and `cuntz_balancing_factor.py` as NEW modules.** The volume
   computation runs once per cell at evaluation time inside `evaluate_68d_vector`, immediately after
   `_ensure_worker_cell` succeeds. The bf computation runs only in post-processing on the top-10
   cells.

4. **Tighten the silence guard to PD spikes >= 3**, not total spikes >= 10. This is a one-line
   change inside `_summarise_trials` (line 298 of [t0115] `evaluator.py`).

5. **Reuse [t0115]'s setup-remote-machine pattern**: Vast.ai EPYC 32-core or 64-core instance at
   whichever is cheapest at provisioning time, `nrnivmodl` build of the t0080 mods folder,
   `bash tasks/t0122_dsi_cytoplasm_volume_nsga2/code/run_seed<S>.sh` driving the single seed. Plan
   must include a per-instance watchdog of $5 (leaves $1 buffer below the $6 task cap) and a
   `--teardown-on-watchdog` flag invocation. Cost expectation is $1-3 actual.

6. **Reuse [t0115]'s `build_top50_morphologies.py` verbatim** (with seed-string edits) for the
   top-50 chart. ADD a NEW post-run plot `pareto_front_dsi_vs_volume.png` and a NEW
   `cuntz_balancing_factor_top10.png` with the [0.2, 0.7] band overlay.

7. **Use [t0121] as the headline literature baseline**: the `compare_literature.md` template should
   be forked from [t0121]'s `compare_literature.md` and a new row added for Cuntz 2010 alongside the
   existing Hay 2011 / Druckmann 2007 / Mohacsi 2024 rows.

8. **Do NOT patch `_apply_asymmetry`**. [t0120]'s audit confirmed the geometry is correct;
   re-running prior lineage tasks is not needed and is out of scope.

9. **Single GA seed only**. Per the task description ("1 GA seed, pop=96, N_EVAL_SEEDS=3") and per
   [t0113]'s precedent (`secrets.randbelow(10000)`). Avoid round-ish numbers like 1000, 5000, 9000.

10. **Document the cytoplasm-volume formula in `results_detailed.md`** with a per-section breakdown
    table (soma_um3, dendrites_um3, ais_um3) per the task description's Verification Criteria.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port the de Rosenroll 2026 DSGC compartmental model
* **Status**: completed
* **Relevance**: Provides the canonical Bed B cell, the NEURON bootstrap, the AR(2) noise generator,
  and the bar-arrival kinematic helpers that the t0115 fork imports by full dotted path.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP
* **Status**: completed
* **Relevance**: Pre-NSGA-II BoTorch qLogNEHVI run on the 49-d Bed B v2 substrate; documented the
  O(N^3) GP scaling failure that motivated the project-wide switch to NSGA-II via pymoo (see memory
  `feedback_genetic_algorithm_for_high_d_mobo.md`). Also the source of the dendritic-spike-machinery
  motivation that grew into the 54-d v3 substrate.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Source of the 54-d electrophys parameter scheme, the `apply_parameter_vector`
  function, the 12-channel SUFFIX MOD library compiled into `code/mods/`, and the
  `ensure_t80_dll_loaded` idempotent process-singleton loader. The new task inherits all of these
  through the t0115 fork.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator diversity test
* **Status**: completed
* **Relevance**: Defines the 14-d morphology parameter space, `MorphologyParams`,
  `MorphologyResult`, `PARAM_BOUNDS`, `INT_PARAM_NAMES`. The `MorphologyResult` exposes `soma`,
  `all_dends`, `ais_proximal`, `ais_distal` `h.Section` handles that the new task reads `sec.L` and
  `sec.diam` from to compute cytoplasm volume.

### [t0091]

* **Task ID**: `t0091_morphology_extended_nsga2_v1`
* **Name**: First joint 68-d NSGA-II with morphology generator in-loop
* **Status**: completed
* **Relevance**: Original 68-d NSGA-II run; demonstrated that pure-DSI optimisation produces zero
  biologically-plausible cells. Direct motivation for the new task's cytoplasm-volume cost
  objective.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology generator silence (soma area bug)
* **Status**: completed
* **Relevance**: Provides `generate_fixed_morphology` (the canonical morphology entry point per
  C-0093-01) and `insert_baseline_channels`. The z-axis soma patch is the reason cytoplasm volume
  computed from `sec.L * pi * (sec.diam/2)**2` for the soma matches the intended
  `BEDB_AREA_TARGET_UM2 = ~220 um^2` reference surface area.

### [t0099]

* **Task ID**: `t0099_random_init_pareto_robustness`
* **Name**: 68-d random-init Pareto + robustness across 3 GA seeds
* **Status**: completed
* **Relevance**: Established the LHS-only initialisation pattern and the 3-objective HV reference
  point (later reduced to 2 in the t0106 lineage). Source of `T0099_PARETO_FRONT_JSON` and
  `T0099_ANCHOR_TRACKING_JSON` cross-seed reference data still referenced by t0115's `paths.py`.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: 68-d random-init NSGA-II seed-scale at N_EVAL_SEEDS=4 / N_GEN=20
* **Status**: completed
* **Relevance**: Discovered the DSI = 1.0 silence-corner artefact and introduced the
  `SILENCE_SPIKE_COUNT_THRESHOLD` silence guard. The new task inherits the guard (with tightened
  threshold) through the t0115 fork.

### [t0104]

* **Task ID**: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* **Name**: NSGA-II 2-objective (DSI + PD-rate) across 3 seeds
* **Status**: completed
* **Relevance**: Source of the 2-objective `n_obj=2` Problem signature reused verbatim by the t0106
  lineage; the new task keeps `n_obj=2` but swaps PD-rate for cytoplasm volume. Also the origin of
  `T0104_HARD_BUDGET_USD` and `T0104_HARD_BUDGET_PER_SEED_USD` constants still re-exported by
  t0115's `constants.py`.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long 300-gen PD/ND NSGA-II run (parent of the t0115 lineage)
* **Status**: completed
* **Relevance**: Introduced the long-run `PerGenerationPoolRestart` callback and
  `OperatorStopTermination` pattern. The new task inherits both through the t0115 fork.

### [t0112]

* **Task ID**: `t0112_t0106_seed77_replicate`
* **Name**: Seed-77 NSGA-II replicate of t0106 (substrate-rate confirmation)
* **Status**: completed
* **Relevance**: Introduced and operator-endorsed the `_POOL_RESTART_EVERY = 10` cadence (the "10th
  gen rule" per memory `feedback_nsga2_pool_restart_every_10.md`). The new task preserves this
  constant verbatim.

### [t0113]

* **Task ID**: `t0113_t0106_seed2247_replicate`
* **Name**: Seed-2247 NSGA-II replicate of t0106 (substrate-rate confirmation)
* **Status**: completed
* **Relevance**: Established the `secrets.randbelow(10000)` GA seed convention used to draw seed
  2247\. The new task draws its single GA seed the same way. Also confirmed the $0.48 lower bound on
  the expected cost envelope.

### [t0114]

* **Task ID**: `t0114_seed7755_no_autostop`
* **Name**: t0113 replica with HV-plateau auto-stop disabled (seed 7755)
* **Status**: completed
* **Relevance**: Established the "no auto-stop, operator-driven stop" convention. Demonstrated the
  $1.13 cost envelope at 300-gen ceiling. Failure mode (`top50_morphologies_seed7755.png` drew only
  soma dots) is the cautionary tale that drives the new task's full-dendrite-tree rendering
  requirement.

### [t0115]

* **Task ID**: `t0115_seed9354_no_autostop`
* **Name**: Seed-9354 NSGA-II replicate of t0106 with HV-plateau auto-stop disabled
* **Status**: completed
* **Relevance**: **THE direct fork point**. Every code file in the new task's `code/` is copied
  verbatim from `tasks/t0115_seed9354_no_autostop/code/` and minimally patched. The 763-line
  `nsga2_driver.py`, 504-line `evaluator.py`, and 308-line `build_top50_morphologies.py` are the
  load-bearing source files.

### [t0118]

* **Task ID**: `t0118_resimulate_t0117_cluster_samples_ge_gi_vm`
* **Name**: Resimulate t0117 cluster samples capturing g_e/g_i/Vm
* **Status**: completed
* **Relevance**: Confirmed the t0115 trial_helpers + synapse-placer + 1400-ms TSTOP_MS pipeline
  works without modification on a parallel resimulation task. Validates the plan to reuse
  `trial_helpers.py` verbatim.

### [t0120]

* **Task ID**: `t0120_morph_generator_geometry_audit`
* **Name**: Morphology generator geometry audit
* **Status**: completed
* **Relevance**: **GATING DEPENDENCY**. Verdict: "rendering-only artefact, no NSGA-II re-runs
  needed. t0122_dsi_cytoplasm_volume_nsga2 is unblocked." The 60/60 coordinate-consistency checks
  pass means the new task can compute cytoplasm volume from the morphology generator output with
  full confidence that `sec.L * pi * (sec.diam/2)**2` matches realised geometry.

### [t0121]

* **Task ID**: `t0121_5seed_substrate_rate_canonical_report`
* **Name**: Canonical 5-seed substrate-rate report
* **Status**: completed
* **Relevance**: Headline literature-comparison baseline. The 5-seed LEGIT acceptance mean 2.58%
  (bootstrap 95% CI +0.38% to +5.53%) is the yield the new task's cytoplasm-constrained front should
  be compared against. Provides the `compare_literature.md` template the new task forks.
