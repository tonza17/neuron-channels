---
spec_version: "1"
task_id: "t0129_t0126_signed_dsi_real_rates_1seed"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 5
libraries_found: 18
libraries_relevant: 0
date_completed: "2026-05-26"
status: "complete"
---
# Research Code -- t0129 Signed DSI + Real Rates Reproduction of t0126

## Task Objective

Reproduce the t0126 Bed B + 14-d morphology NSGA-II protocol on a single fresh seed (3517) with two
evaluator corrections: (1) replace vector-sum DSI with the signed antipodal ratio
`(R_PD - R_ND) / (R_PD + R_ND)` in `[-1, 1]`, and (2) persist `pd_rate_hz` / `nd_rate_hz` computed
from real per-direction spike counts instead of the placeholder rates that contaminated t0126's
hand-synthesised `cell_trace`. The forked driver also drops the per-spike `cell_trace.jsonl` and
instead writes the full 68-d parameter vector for every evaluated cell to
`results/cell_params.jsonl`. The parent task is **only** [t0126]; t0127 and t0128 are explicitly out
of scope and must not be read or imported. This file maps every t0126 module the t0129
implementation will need to fork, with the exact lines to edit, plus the do-not-touch boundaries.

## Library Landscape

The library aggregator script (`arf/scripts/aggregators/aggregate_libraries.py`) is not present in
this repository's `arf/scripts/aggregators/` directory (only `aggregate_tasks`, `aggregate_costs`,
`aggregate_machines`, `aggregate_metric_results`, `aggregate_metrics`, `aggregate_suggestions`,
`aggregate_categories`, `aggregate_task_types` are wired up). The libraries listed in
`arf/docs/reference/aggregators.md` therefore had to be enumerated directly by listing
`tasks/*/assets/library/*/details.json`. **18 distinct `library_id` values** were found across all
prior tasks:

* `de_rosenroll_2026_dsgc`, `de_rosenroll_2026_dsgc_ais`,
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` -- de Rosenroll 2026 DSGC NEURON model ports produced
  by tasks t0024, t0078, and t0080. **Indirectly used** -- t0126's `bootstrap.py` patches the t0024
  build/load functions for Linux and loads the t0024-vendored MOD `.dll` / `.so`. The t0129 fork
  inherits this unchanged. See [t0024] and [t0080] in the Task Index.
* `procedural_dsgc_morphology_generator` (task t0090) and `procedural_dsgc_morphology_generator_fix`
  (task t0092) -- produce the procedural Bed B morphologies for the 14-d morphology block of the
  68-d vector. t0126's `evaluator.py:34-37` imports `MorphologyParams` and `MorphologyResult` from
  the t0090 library; this stays unchanged for t0129. See [t0090] in the Task Index.
* `dsgc_active_channel_pack` (task t0080) -- 13-channel MOD library that supplies all electrophys
  density mechanisms; t0126 picks it up via `paths.resolve_t99_mod_library()`. Unchanged for t0129.
  See [t0080] in the Task Index.
* `tuning_curve_viz` (task t0011) and `tuning_curve_loss` (task t0012) -- not relevant. Both
  libraries target 12-angle tuning-curve fitting against the t0004 target; t0126/t0129 use the
  antipodal pair `[0 deg, 180 deg]` only, no tuning-curve fitting, no Poleg-Polsky envelope. They
  are documented here for completeness so the human reviewer can confirm the choice.
* `modeldb_189347_dsgc`, `modeldb_189347_dsgc_dendritic`, `modeldb_189347_dsgc_exact`,
  `modeldb_189347_dsgc_gabamod` (tasks t0008, t0020, t0046) -- ModelDB DSGC ports. Superseded by the
  t0024 de Rosenroll port that t0126's NEURON layer actually uses; not relevant for t0129.
* `minimal_dsgc_scalar_gaba`, `minimal_dsgc_spatial_gaba`, `minimal_dsgc_ampa_nmda_scalar_gaba`,
  `minimal_dsgc_bar_locked_gaba_ampa_sweep`, `minimal_dsgc_mg_block_nmda`,
  `minimal_dsgc_tonic_gaba_sweep` (tasks t0052 to t0062) -- minimal toy DSGC models used for
  synaptic mechanism studies. Not relevant; t0126's Bed B substrate uses the t0024 / t0080 channel
  pack.

**None of the registered libraries need new imports for t0129.** The cross-task code that t0126
relies on is either imported via the library mechanism already (t0090 morphology generator, t0080
channel pack, t0024 de Rosenroll port through the `bootstrap.py` monkey patch) or lives inside
t0126's own `code/` directory. t0129's strategy is therefore to copy the relevant t0126 modules
verbatim into `tasks/t0129_*/code/` and apply the two evaluator edits plus the cell-params dump.

## Key Findings

### Vector-sum DSI lives in one helper plus one objective line

t0126's `_vector_sum_dsi` helper sits at `tasks/t0126_*/code/evaluator.py:356-376`. It computes
`|sum_dir(mean_spikes_dir * unit_vec(dir))| / sum_dir(mean_spikes_dir)`, returning a non-negative
scalar in `[0, 1]`. It is called in exactly two places: the headline DSI of a cell at
`evaluator.py:445` (inside `_summarise_trials`), and per-seed in the robustness diagnostic loop at
`evaluator.py:453`. The objective F vector is built one place only -- inside
`BedBV3MorphProblem._evaluate` at `evaluator.py:689-700`, line 697:
`out["F"] = np.array([-result.dsi_vector_sum, +result.atp_per_spike_molecules], dtype=np.float64)`.
The negation makes DSI a maximised objective.

The signed antipodal DSI replacement is arithmetically simpler -- when the only directions are
`PD_DIRECTION_DEG = 0.0` and `PD_DIRECTION_DEG + 180.0`, the formula reduces to
`(mean(pd_spikes) - mean(nd_spikes)) / (mean(pd_spikes) + mean(nd_spikes))`. The existing silence
sentinel `WORST_CASE_DSI = -1.0` (imported from `constants_morphology` at `evaluator.py:71`) already
sits at the lower bound of the signed range, so the t0126 silence-guard branch at
`evaluator.py:439-443` can be reused without change. The negation in the F vector is still required
because the optimiser minimises F. [t0126]

### `pd_rate_hz` is already real -- it is the `cell_trace` consumer that synthesised it

`pd_rate_hz` is computed honestly inside `_summarise_trials` at `evaluator.py:446`:
`pd_rate_hz = float(np.mean(pd_spikes)) / (TSTOP_MS / 1000.0)`. The per-direction
`firing_hz_per_dir` dict at `evaluator.py:467-470` is also from real counts. The placeholder
`pd_rate_hz = 40` symptom recorded in memory `project_t0126_cell_trace_synthesised.md` was
introduced **after** the run, by a diagnostic-synthesis pass that built `cell_trace_seed8929.jsonl`
from objective-only data when the run script failed to propagate `T0126_CELL_TRACE_JSONL` to worker
processes (per memory `feedback_nsga2_launch_via_run_script`). The fix for t0129 is therefore not to
recompute `pd_rate_hz` -- the evaluator already does -- but to (a) keep `pd_rate_hz` on
`CellEvalResult` (it is already there at `evaluator.py:123`), (b) add a sibling `nd_rate_hz` field
on `CellEvalResult` computed the same way from `nd_spikes`, and (c) persist both as honest top-level
fields on every `cell_params.jsonl` row so no downstream consumer ever has to fall back to a
synthesised proxy. [t0126]

### The per-cell trace path is environment-driven and silently no-ops if unset

`evaluator._cell_trace_path()` at `evaluator.py:145-152` reads `T0126_CELL_TRACE_JSONL` (or the
back-compat alias `T0122_CELL_TRACE_JSONL`); if either is empty or unset, `_append_cell_trace` at
`evaluator.py:632-665` returns immediately without raising. This is the exact failure mode described
in memory `feedback_nsga2_launch_via_run_script` -- a direct
`python -m tasks.t0126_*.code.nsga2_driver` invocation under tmux does not inherit env vars from a
sibling shell, so the cell trace silently drops. The mitigation in the task description is twofold:
(1) launch via the `run_seed3517.sh` wrapper so the env var is set in the same shell that spawns the
driver and its multiprocessing.Pool workers, and (2) replace the trace path with a fixed
`RESULTS_DIR / "cell_params.jsonl"` location that does **not** depend on an env var, so the failure
mode cannot recur. The t0129 fork should remove `_cell_trace_path()` and the
`T0126_CELL_TRACE_JSONL` env-var dance entirely, and instead pass the cell_params output path
through the `BedBV3MorphProblem` constructor so it is captured in the pickled problem object that
the workers receive. [t0126]

### NSGA-II driver is reusable; only the objective and dump locations change

`tasks/t0126_*/code/nsga2_driver.py` (789 lines) implements the production NSGA-II loop with the
four canonical t0126 callbacks: `_GenerationCallback` (writes hv_trajectory.json,
all_evaluations.json, dill checkpoints), `PerGenerationPoolRestart` (the 10-gen rule at
`nsga2_driver.py:105` -- `_POOL_RESTART_EVERY: int = 10`), `OperatorStopTermination` (declared but
intentionally **not** added to the live `TerminationCollection` per `_build_termination` at
`nsga2_driver.py:211-224`), and `CostWatchdogTermination`. The live termination collection is only
`MaximumGenerationTermination(60)` + `CostWatchdogTermination`, matching the project policy in
memory `feedback_disable_hv_plateau_autostop.md` (HV-plateau auto-stop **disabled**). All of this is
reused verbatim by t0129. The only changes in the t0129 fork of `nsga2_driver.py` are: (a) update
all `tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.*` imports to
`tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.*`, (b) rename `T0126_HARD_BUDGET_USD` ->
`T0129_HARD_BUDGET_USD` (or alias), (c) update the `_save_iteration` comment block at
`nsga2_driver.py:314-328` so the dumped `dsi_best_legit` field is renamed to `dsi_signed` (range now
`[-1, 1]`). [t0126]

### Smoke gate, unit tests, and metrics builder all hard-code `dsi_vector_sum`

* `smoke_gate.py:210-223` (check 2 -- ratio DSI synthetic sanity) calls
  `_vector_sum_dsi(PD=5, ND=1)` and asserts the result is `0.6667`. The signed-antipodal formula on
  `(PD=5, ND=1)` also yields `(5-1)/(5+1) = 0.6667`, so the **numeric** check survives a rename;
  only the helper name and the comment string need updating.
* `smoke_gate.py:283-310` (check 6 -- no HVPlateauTermination in live collection) inspects
  `_build_termination` source. Unchanged for t0129.
* `smoke_gate.py:313-374` (check 7 -- DSI/ATP sanity range) already asserts `-1.0 <= dsi <= 1.0`, so
  it is **already compatible** with signed DSI. The field accessed is `eval_res.dsi_vector_sum` at
  line 359 -- update to `eval_res.dsi_signed`.
* `smoke_gate.py:377-403` (check 8 -- F sign) greps the source of `BedBV3MorphProblem._evaluate` for
  the substring `-result.dsi_vector_sum`. Update to `-result.dsi_signed`.
* `smoke_gate.py:264-280` (check 5 -- cost-watchdog wiring) asserts `T0126_HARD_BUDGET_USD == 6.00`;
  update symbol name if renamed.
* `test_evaluator_dsi_guard.py` (186 lines) imports `_vector_sum_dsi`, asserts
  `result.dsi_vector_sum == -1.0` for silence and `> 0.0` for firing. Eight tests in total -- must
  be ported to (a) import `_signed_antipodal_dsi`, (b) accessor renamed to `result.dsi_signed`. The
  task description requires four new tests: PD>ND positive,
  PD<ND negative, PD=ND=0 silence (= -1.0), PD=ND>0 zero. The new PD<ND negative case is genuinely
  new -- the vector-sum formula never returned a negative value, so the existing tests have no
  analogue.
* `metrics_builder.py:79-83` reads `row.get("dsi_vector_sum", 0.0)` from the cell trace rows for the
  LEGIT cohort definition. The downstream variant keys (`best_legit`, `overall_max_mi`,
  `overall_min_atp`) all flow from this. For t0129, rename to `dsi_signed` and revise the LEGIT
  threshold semantics if needed -- a `dsi_signed >= 0.5` threshold still selects strongly
  PD-preferring cells, but cells in `[-1, 0)` now also exist and need a new category
  (`reversed_preference` cells). The verification criteria in the task description explicitly
  require a count of t0126-Pareto cells with `dsi_vector_sum > 0.5` but `dsi_signed < 0` (reversed
  preference masked by magnitude); this requires loading t0126's recorded cells from
  `tasks/t0126_*/results/data/` and reprojecting them through the signed formula. [t0126]

### The `cell_params.jsonl` schema is new and supersedes the per-spike `cell_trace`

The task description (Change 3) specifies a new per-cell JSONL with the fields `gen`, `cell_idx`,
`param_vector` (full 68-d), `dsi_signed`, `atp_per_spike_molecules`, `pd_rate_hz`, `nd_rate_hz`,
`silence_failed`, `n_errors`. There is no analogue in t0126 -- its `cell_trace_seed8929.jsonl` was
produced offline and contained the synthesised `pd_rate_hz` placeholder. The new dump is small (one
row per evaluated cell -- ~96 cells/gen * 60 gen + 96 Phase-A cells = ~5856 rows) and writes the
same 68-d vector that already lives in the all_evaluations.json `vector_68d` field. The simplest
implementation is a dedicated writer in the evaluator's `_evaluate` method (after the cell result is
computed, before `out["F"]` is set), using a `multiprocessing.Lock` and a path captured at
problem-construction time. [t0126]

### Run script wrapper is the load-bearing env-var carrier

`tasks/t0126_*/code/run_seed8929.sh` (72 lines) is the canonical NSGA-II launcher. The load-bearing
lines are: line 39 `SEED=8929` (update to 3517 for t0129); line 40-46 set the `RESULTS_DATA_DIR`,
truncate the cell_trace JSONL, and export `T0126_CELL_TRACE_JSONL`. For t0129 with the env-var
dependency removed, the wrapper still needs to (a) compile mod files, (b) run Phase-A `random_init`,
(c) launch the driver with `--seed 3517 --n-gen 60 --save-algorithm-config`. The
`--teardown-on-watchdog` flag should stay because the task description still inherits t0126's budget
cap. Memory `feedback_nsga2_launch_via_run_script` mandates this wrapper path for any production
NSGA-II run. [t0126]

### Bootstrap is platform-aware and reusable verbatim

`bootstrap.py` (161 lines) patches the t0024 `build_cell` and `paths` modules for Linux, compiles
the t0024 MOD sources on Linux via `nrnivmodl`, and points `_p24.NRNMECH_DLL` at the compiled `.so`.
The module applies the bootstrap as an import side effect at line 161 (`bootstrap_neuron()`), so any
t0129 module that simply imports `tasks.t0129_*.code.bootstrap` gets the same Linux-aware behaviour.
No edits needed beyond the package rename for the new task. [t0126]

### Post-run analysis flows from the same per-cell records

`post_run_analysis.py` (231 lines) drives the comparator chart, HV trajectory chart, and Pareto
front chart. The DSI plotting at `post_run_analysis.py:135-148` already falls back between
`dsi_best_legit` and `dsi_vector_sum`; for t0129 add a `dsi_signed` fallback first and widen the
y-axis to `(-1.05, 1.05)` (was `(-0.05, 1.05)` at line 192). The `t0124_vs_t0126_comparator.py`
module looks for DSI under three names at line 113 (`"dsi_best_legit", "dsi_vector_sum", "dsi"`);
for the t0129 cross-comparator, add `dsi_signed` as the first key tried. [t0126]

### Project memories that gate the run

The following memories from `MEMORY.md` materially constrain the t0129 implementation:

* `feedback_disable_hv_plateau_autostop` -- HV-plateau auto-stop **disabled**; only triggers are
  budget cap + gen ceiling. t0126's `nsga2_driver._build_termination` already complies; preserve
  verbatim.
* `feedback_nsga2_pool_restart_every_10` -- `_POOL_RESTART_EVERY = 10` in the driver. t0126's
  nsga2_driver.py:105 complies; preserve verbatim.
* `feedback_nsga2_launch_via_run_script` -- launch via `run_seed*.sh`, never directly. The t0129
  task description Approach step 3 already mandates this; the implementation must comply.
* `project_t0126_cell_trace_synthesised` -- t0126's cell_trace was synthesised after the run, with
  `pd_rate_hz=40` placeholder. The t0129 corrections (real rates persisted from the evaluator, no
  env-var dependency) are the direct fix.
* `feedback_consolidated_task_design` -- preference for one task bundling related changes. t0129
  bundles the signed DSI swap + real-rate persistence + cell_params dump into one task; this
  complies.

[t0126]

## Reusable Code and Assets

All cross-task code reuse below is **copy into task** unless noted. None of the t0126 modules are
themselves registered as a library, so every file the t0129 implementation needs must be duplicated
into `tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/`.

### Copy-and-modify list (t0126 -> t0129)

* **`evaluator.py`** (706 lines) -- **copy into task**. Source:
  `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/evaluator.py`. Adaptations: (a) replace
  `_vector_sum_dsi` at lines 356-376 with
  `_signed_antipodal_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float` per task
  description Change 1. (b) Rename `CellEvalResult.dsi_vector_sum` (line 122) to `dsi_signed`;
  update every reference in `_summarise_trials` (lines 443, 445, 503) and the two error-path
  `CellEvalResult(...)` constructors at lines 415-433 and 540-559 and 610-629. (c) Add
  `nd_rate_hz: float` field to `CellEvalResult` (after line 123), populate at line 447 from the
  `nd_spikes` analogue (compute alongside `pd_spikes` at lines 389-407). (d) Replace
  `_append_cell_trace` at lines 632-665 with `_append_cell_params` writing the schema from task
  description Change 3; sink to a path injected via `BedBV3MorphProblem.__init__` (no env var). (e)
  Update `BedBV3MorphProblem._evaluate` at lines 689-707 to call the new `_append_cell_params`, emit
  `out["F"] = [-result.dsi_signed, +result.atp_per_spike_molecules]`, and accept
  `cell_params_path: Path` in `__init__`. (f) Update package import path at lines 38-96 from
  `tasks.t0126_*` to `tasks.t0129_*`. Signature of new helper:
  `_signed_antipodal_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float`.

* **`nsga2_driver.py`** (789 lines) -- **copy into task**. Source:
  `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/nsga2_driver.py`. Adaptations: (a)
  `tasks.t0126_*` -> `tasks.t0129_*` import rewrite throughout. (b) `_save_iteration` at lines
  289-354 -- rename the dumped field `dsi_best_legit` to `dsi_signed` at lines 325, 628 (and update
  the comment block at 314-318). (c) `BedBV3MorphProblem(...)` construction at line 568 -- pass the
  `cell_params_path = RESULTS_DIR / "cell_params.jsonl"` kwarg added in Change 3. (d)
  `T0126_HARD_BUDGET_USD` import at line 72 -- preserve cap value 6.0; either rename the symbol in
  the t0129 constants module or keep the alias. (e) Preserve `_POOL_RESTART_EVERY = 10` at line 105
  (10-gen rule). (f) `MaximumGenerationTermination(n_max_gen=60)` and removed
  `OperatorStopTermination` unchanged.

* **`run_seed8929.sh`** (72 lines) -- **copy into task** as `run_seed3517.sh`. Source:
  `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/run_seed8929.sh`. Adaptations: (a)
  `SEED=8929` (line 39) -> `SEED=3517`. (b) Remove the env-var dance at lines 42-47
  (`T0126_CELL_TRACE_JSONL` / `T0122_CELL_TRACE_JSONL`); the cell_params path is captured via the
  problem constructor in the new evaluator. (c) `tasks.t0126_*` module paths (lines 52, 57, 67) ->
  `tasks.t0129_*`. (d) The Phase-A `random_init` invocation at line 52 and the bootstrap import at
  line 57 keep the same shape, just retargeted to t0129's package.

* **`test_evaluator_dsi_guard.py`** (186 lines) -- **copy into task** as
  `test_evaluator_dsi_signed.py` (rename to advertise the new metric). Source:
  `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/test_evaluator_dsi_guard.py`. Adaptations:
  rewrite all 7 existing tests to assert on `result.dsi_signed` and to import
  `_signed_antipodal_dsi`. Add a **new**
  PD<ND test asserting the signed DSI is **negative** (e.g., PD=2, ND=10 -> dsi_signed = -0.667).
  The threshold-regression test at lines 61-65 (`test_silence_pd_threshold_value`) stays as-is. The
  `test_three_pd_spikes_does_not_trip_guard` case at lines 120-139 returns `(3-0)/(3+0) = 1.0` under
  signed-antipodal -- the existing assertion `> 0.0` survives but should be tightened to `== 1.0`.
  Verification criteria explicitly require (a) PD>ND positive case, (b)
  PD<ND negative case, (c) PD=ND=0 silence sentinel = -1.0, (d) PD=ND>0 zero case.

* **`smoke_gate.py`** (690 lines) -- **copy into task**. Source:
  `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/smoke_gate.py`. Adaptations: (a) Check 2 at
  lines 210-223: rename helper, keep the numeric assertion
  `_signed_antipodal_dsi({0.0: [5], 180.0: [1]}) == 4/6` (identical for antipodal pair). (b) Check 7
  at lines 313-374: replace `eval_res.dsi_vector_sum` (line 359) with `eval_res.dsi_signed`; the
  range check `-1.0 <= dsi <= 1.0` already matches signed range. (c) Check 8 at lines 377-403:
  update the grep target from `-result.dsi_vector_sum` to `-result.dsi_signed`. (d) All
  `tasks.t0126_*` imports retargeted to `tasks.t0129_*`. Checks 1, 3, 4, 5, 6, 9 unchanged in logic;
  only package path renames.

* **`bootstrap.py`** (161 lines) -- **copy into task** verbatim except for the docstring (still
  describes t0080). The module is platform-only; nothing DSI-related lives here.

* **`constants.py`**, **`constants_morphology.py`**, **`constants_electrophys.py`** -- **copy into
  task** verbatim, then: (a) rename `T0126_SEEDS = (8929,)` (constants.py line 72) to
  `T0129_SEEDS = (3517,)` and preserve the back-compat aliases (`T0114_SEEDS`, `T0122_SEEDS`,
  `T0126_SEEDS = T0129_SEEDS`) so the driver imports still resolve. (b) Drop the
  `T0124_SEED_EXCLUDED` assertion at line 73 -- t0129 does not enforce cross-lineage exclusion; the
  t0124/t0126 seeds (6650, 8929) are not in the t0129 lineage either. (c) Bounds, REF_POINT_HV,
  HV_UTOPIA_DSI, HV_UTOPIA_ATP_PER_SPIKE, POP_SIZE, N_GEN, N_EVAL_SEEDS, N_DIRECTIONS, SBX/PM params
  -- all imported from constants_morphology and preserved verbatim.

* **`random_init.py`** (102 lines) -- **copy into task** verbatim except for the package rename. The
  LHS sample for seed 3517 is deterministic given the seed; the
  `np.random.SeedSequence(3517).generate_state(1)[0]` will produce a distinct (96, 68) matrix from
  seed 8929's.

* **`paths.py`** (219 lines) -- **copy into task**, then add a new constant
  `CELL_PARAMS_JSONL: Path = RESULTS_DIR / "cell_params.jsonl"` near the existing `RESULTS_DIR`
  block (line 54).

* **`apply_params.py`**, **`atp_per_spike.py`**, **`anchor_classifier.py`**,
  **`anchor_definitions.py`**, **`build_cell_ais.py`**, **`cost_watchdog.py`**,
  **`cuntz_balancing_factor.py`**, **`cytoplasm_volume.py`**, **`extend_with_ais.py`**,
  **`generator_wrapper.py`**, **`hv_plateau_watchdog.py`**, **`mi_estimator.py`**,
  **`parametric_placer.py`**, **`recorder.py`**, **`trial_helpers.py`** -- **copy into task**
  verbatim with `tasks.t0126_*` -> `tasks.t0129_*` import rename. None of these touch the DSI metric
  or the cell_trace path; they are mechanical dependencies of the evaluator.

* **`metrics_builder.py`** (238 lines) -- **copy into task**. Adaptations: (a) all
  `row.get("dsi_vector_sum")` accessors (lines 79, 140) -> `row.get("dsi_signed")`. (b)
  `dimensions["dsi_metric"]` at line 118 -> `"signed_antipodal"` (was `"vector_sum"`). (c) Load
  source switched from `_load_cell_trace_jsonl` to a new `_load_cell_params_jsonl` reading
  `RESULTS_DIR / "cell_params.jsonl"`. The LEGIT threshold check `dsi >= DSI_LEGIT_THRESHOLD` (line
  82\) is preserved at `0.5`; the semantics shift slightly because reversed-preference cells
  (`dsi < 0`) are now possible and excluded. The new metrics required by the verification criteria
  (`dsi_signed_max`, `dsi_signed_pareto_median`, `atp_per_spike_pareto_min`,
  `pd_rate_hz_pareto_median`, count of t0126-Pareto cells with `dsi_vector_sum > 0.5` but
  `dsi_signed < 0`) need new variant blocks.

* **`post_run_analysis.py`** (231 lines), **`build_predictions_assets.py`** (517 lines),
  **`build_results.py`** (165 lines), **`build_pareto_plots.py`**,
  **`build_top50_morphologies.py`**, **`build_t0126_outputs.py`**, **`build_assets.py`**,
  **`dsi_atp_comparators.py`** (427 lines), **`t0124_vs_t0126_comparator.py`** (485 lines) -- **copy
  into task** for the charts and asset builders. All references to `dsi_vector_sum` in these files
  must be upgraded to prefer `dsi_signed` first, then fall back. The Pareto-plot y-axis range at
  `post_run_analysis.py:192` (`(-0.05, 1.05)`) must widen to `(-1.05, 1.05)` so the negative tail is
  visible (task description Outputs requirement). Of these, `build_t0126_outputs.py` and
  `t0124_vs_t0126_comparator.py` are task-specific orchestration that may need to be renamed (e.g.,
  `build_t0129_outputs.py`) or dropped if not needed for t0129's single-seed scope -- planning will
  decide.

* **`sync_results_back.sh`** -- **copy into task**, retarget the rsync source/destination paths.

### Library imports (no change needed)

* `from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult`
  -- registered library `procedural_dsgc_morphology_generator`. Used by the forked evaluator at
  `evaluator.py:34-37`. **Import via library** (already registered; t0126 imports through the same
  package path).

* `from tasks.t0024_port_de_rosenroll_2026_dsgc.code import build_cell, constants, paths` --
  registered library `de_rosenroll_2026_dsgc`. Used by `bootstrap.py` for Linux MOD loading.
  **Import via library**.

* `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.mods` -- the 13-channel MOD library
  `dsgc_active_channel_pack`. Loaded at runtime via NEURON's `nrn_load_dll`; no Python import. Path
  lookup is via `paths.resolve_t99_mod_library()` which the t0129 fork inherits unchanged.

### Do-not-touch (out of scope)

* `tasks/t0127_correct_t0126_cell_trace_suggestions/code/**` -- t0127 corrected t0126's cell_trace
  using a different recovery mechanism. The t0129 task description explicitly forbids reading from
  or treating t0127 as a reference. Do not import, do not copy any of t0127's helpers.
* `tasks/t0128_t0127_rerun_dsi_atp_3seeds/code/**` -- t0128 is a t0127-derived multi-seed re-run.
  Same prohibition. The t0129 task description states "the only parent task is
  t0126_bedb_dsi_atp_per_spike_nsga2_60gen."

## Lessons Learned

### Synthesising diagnostics from objective-only data is unsafe

The t0126 lineage's hard lesson, recorded in memory `project_t0126_cell_trace_synthesised`, is that
when the env-var-driven cell_trace sink silently drops (workers do not inherit the env var the
parent shell set), the temptation to backfill the missing diagnostics from the objective-only dump
produces fabricated numbers. t0126's `cell_trace_seed8929.jsonl` carried `pd_rate_hz = 40` for every
cell because the synthesis pass used a hard-coded placeholder when the real per-direction spike
counts were no longer available. The t0129 fix is twofold: (a) write the params dump on the
evaluator's own happy path so the data is always real, and (b) eliminate the env-var dependency
entirely (pass the sink path through the problem constructor). Memory
`feedback_nsga2_launch_via_run_script` is the policy correlate -- always launch via the
`run_seed*.sh` wrapper so worker env inheritance is well-defined. [t0126]

### Field rename is contagious -- enumerate consumers exhaustively

Renaming `dsi_vector_sum` -> `dsi_signed` on `CellEvalResult` touches: the evaluator (2
constructors), `BedBV3MorphProblem._evaluate`, the cell_trace writer, the smoke gate (checks 2, 7,
8), the test suite (8 tests), `metrics_builder.py` (3 fields), the predictions asset builder (4
sites in `build_predictions_assets.py`), the results builder (3 sites in `build_results.py`), the
comparator (3 fallback keys in `t0124_vs_t0126_comparator.py:113`), the Pareto plot (1 fallback
chain in `post_run_analysis.py:135-148`), and the predictions asset description.md (3 prose sites at
lines 258, 353). The grep pattern is `dsi_vector_sum` across `tasks/t0129_*/code/` after the file
copy step. [t0126]

### The 10-gen pool restart and disabled HV auto-stop are non-negotiable

Memories `feedback_nsga2_pool_restart_every_10` and `feedback_disable_hv_plateau_autostop` are
surfaced as named constants in t0126's `constants.py` (lines 85-86) so a grep finds them. The t0129
fork inherits both as project-policy invariants; any deviation must be a separate task. [t0126]

### Negative DSI is genuinely new and not handled by existing analysis code

t0126's downstream analysis (LEGIT cohort threshold, Pareto plot y-axis, comparator joint-pass
filter) assumes `dsi in [0, 1]`. When t0129 introduces `dsi in [-1, 1]`, three categories of
breakage need attention: (a) y-axis limits clip the negative tail (post_run_analysis.py:192), (b)
LEGIT threshold `dsi >= 0.5` silently rejects reversed-preference cells that may be biologically
interesting, (c) joint-pass filter at `post_run_analysis.py:155-158` requires `dsi >= 0.5` which is
fine but the prose label needs updating. [t0126]

### Smoke gate's "ratio DSI synthetic sanity" numerically coincides on antipodal pair

Check 2 at `smoke_gate.py:210-223` asserts
`_vector_sum_dsi({0.0: [5], 180.0: [1]}) == 4/6 = 0.6667`. The signed antipodal formula gives
`(5-1)/(5+1) = 0.6667` too -- the two formulae are arithmetically identical when there are exactly
two antipodal directions and both have non-negative mean counts. This means the smoke gate's numeric
assertion is **unchanged** by the metric swap; only the helper name and prose need updating. This is
a fortunate coincidence that makes the smoke gate a free positive control on the new code. [t0126]

## Recommendations for This Task

1. **Fork t0126's entire `code/` directory verbatim** into
   `tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/` first, then apply the targeted edits below.
   This minimises the risk of subtle drift from t0126's frozen reference implementation. [t0126]

2. **Apply the four evaluator edits in `evaluator.py` as a single commit** so the diff against t0126
   is reviewable: (a) add `_signed_antipodal_dsi` helper; (b) rename `CellEvalResult.dsi_vector_sum`
   -> `dsi_signed`; (c) add `nd_rate_hz` field populated from the existing per-direction counts; (d)
   replace `_append_cell_trace` with `_append_cell_params` writing the schema from task description
   Change 3 and accept the path via `BedBV3MorphProblem.__init__`. Keep `_vector_sum_dsi` deleted --
   no caller in the new code, and keeping a dead helper makes the diff confusing. [t0126]

3. **Add the new PD<ND negative test case** in `test_evaluator_dsi_signed.py` -- this is the one
   genuinely new test that the vector-sum formula could not exercise. Assert
   `_signed_antipodal_dsi({0.0: [2], 180.0: [10]}) ≈ -0.667` and `_summarise_trials` returns
   `result.dsi_signed < 0` for the trials. Run the test before the smoke gate so a sign-flip
   regression is caught early. [t0126]

4. **Remove the `T0126_CELL_TRACE_JSONL` env-var entirely** from the t0129 evaluator and run_seed
   script. Pass `cell_params_path: Path` through `BedBV3MorphProblem.__init__` so it is pickled into
   worker processes. The `multiprocessing.Lock` for serialised appends stays. After Phase A, assert
   the file exists and is non-empty before launching Phase B (per task description Risks &
   Fallbacks). [t0126]

5. **Compute the `t0126-Pareto-with-reversed-preference` count** by loading t0126's
   `tasks/t0126_*/results/data/pareto_front_seed8929.json` (read-only -- not modified) plus the
   recorded per-direction spike counts from t0126's `all_evaluations_seed8929.json` if available, or
   by re-evaluating the t0126 Pareto cells through the t0129 signed-DSI helper. This metric goes
   into `metrics.json` as required by Verification Criteria. Do **not** modify any file under
   `tasks/t0126_*/` -- read-only consumption only. [t0126]

6. **Inherit the 10-gen rule and disabled HV auto-stop verbatim**. Verify after the fork that
   `_POOL_RESTART_EVERY == 10` and that `_build_termination` returns a `TerminationCollection`
   containing only `MaximumGenerationTermination(60)` and `CostWatchdogTermination` (no
   `OperatorStopTermination`, no `HVPlateauTermination`). The t0126 smoke-gate checks 4 and 6
   already verify both; preserve and re-run on the t0129 fork.

7. **Widen the Pareto plot y-axis** in `post_run_analysis.py:192` from `(-0.05, 1.05)` to
   `(-1.05, 1.05)` and add a horizontal dashed line at `dsi_signed = 0` to make the
   reversed-preference region visually obvious. [t0126]

8. **Do not import, read, or reference t0127 or t0128 anywhere.** The task description is explicit.
   The implementation subagent must not consult their code, their plans, or their results. If the
   comparator needs a multi-seed baseline, that is a future task. [t0126]

9. **Launch via `run_seed3517.sh`** end-to-end (per memory `feedback_nsga2_launch_via_run_script`).
   The wrapper must (a) call Phase-A `random_init`, (b) trigger the bootstrap import, (c)
   `python -m tasks.t0129_*.code.nsga2_driver --seed 3517 --n-gen 60 --save-algorithm-config --teardown-on-watchdog`.
   Even on local CPU runs (no Vast.ai), keep the watchdog wiring so the budget cap stays enforced.
   [t0126]

10. **Register no new libraries.** The t0129 reproduction is a one-off experiment; the forked code
    lives entirely inside the task folder. No `tasks/t0129_*/assets/library/` entries are needed.

## Task Index

### [t0126]

* **Task ID**: `t0126_bedb_dsi_atp_per_spike_nsga2_60gen`
* **Name**: NSGA-II DSI vs ATP-per-spike Bed B + 14-d morph: 60-gen replication
* **Status**: completed
* **Relevance**: Direct parent task. Source of every module the t0129 fork copies. Source of the
  vector-sum DSI helper, the silence sentinel, the NSGA-II driver, the smoke gate, the test suite,
  the run-seed wrapper, the metrics builder, and the post-run analysis pipeline. The two t0129
  corrections (signed antipodal DSI, real per-direction firing rates persisted) are scoped against
  t0126's exact implementation; this task's `evaluator.py:356-376` (`_vector_sum_dsi`) and
  `evaluator.py:446-470` (real `pd_rate_hz`
  + `firing_hz_per_dir` already from spike counts) are the load-bearing references.

### [t0124]

* **Task ID**: `t0124_bedb_dsi_atp_per_spike_nsga2`
* **Name**: NSGA-II DSI vs ATP-per-spike Bed B + 14-d morph (predecessor of t0126)
* **Status**: completed
* **Relevance**: Direct ancestor of t0126; the smoke gate, comparator, and bound module names in
  t0126 still carry `t0124_vs_t0126_comparator` etc. Not a direct dependency of t0129 but
  understanding the t0126 -> t0124 lineage is useful context for the comparator code that t0129 will
  fork. Read-only consumption.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator (Bed B realisation)
* **Status**: completed
* **Relevance**: Owns the `procedural_dsgc_morphology_generator` registered library. The t0126 /
  t0129 evaluator imports `MorphologyParams` and `MorphologyResult` from this library; the t0129
  fork inherits the import path unchanged.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 13-channel NEURON MOD library + NSGA-II predecessor
* **Status**: completed
* **Relevance**: Owns the `dsgc_active_channel_pack` registered library -- the compiled 13-channel
  MOD library every t0126 / t0129 cell uses. Loaded via `paths.resolve_t99_mod_library()`.
  Read-only.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: De Rosenroll 2026 DSGC NEURON port
* **Status**: completed
* **Relevance**: Owns the `de_rosenroll_2026_dsgc` registered library. t0126's `bootstrap.py`
  patches t0024's `build_cell.load_neuron` for Linux; the t0129 fork inherits the bootstrap module
  verbatim. Read-only.
