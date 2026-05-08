---
spec_version: "1"
task_id: "t0091_morphology_extended_nsga2_v1"
research_stage: "code"
tasks_reviewed: 12
tasks_cited: 11
libraries_found: 2
libraries_relevant: 2
date_completed: "2026-05-08"
status: "complete"
---
# Research Code -- First Joint 68-d NSGA-II With Morphology In Eval Loop (t0091)

## Task Objective

t0091 is the first NSGA-II run that calls a procedural morphology generator inside the per-cell
evaluation loop, jointly optimising 14 morphology knobs and 54 v3 electrophys / synapse / dendritic
spike knobs in a 68-d parameter space. Pop 96 with up to 8 generations, adaptive HV-plateau stop,
$4.00 cost watchdog, and a 5-anchor warm-start population (Bed-B-like, symmetric, PD-asymmetric,
ND-asymmetric, alternative-topology) cloned across t0083's Pareto electrophys archive. The strategic
question is whether enabling morphology variation opens biologically-plausible joint-pass regions
that the fixed-Bed-B substrate of t0080 / t0081 / t0083 / t0086 / t0088 could not reach. The patched
generator from t0092 (`generate_fixed_morphology`, canonicalised by t0093's correction overlay
`C-0093-01`) replaces t0090's unpatched `generate_morphology` everywhere in the build path.

## Library Landscape

The library aggregator (`aggregate_libraries`) is not yet wired into this fork; the asset-type
aggregators present in `arf/scripts/aggregators/` cover only tasks, suggestions, costs, machines,
metrics, metric-results, categories, and task-types. Library assets were enumerated by reading
`tasks/*/assets/library/*/details.json` directly. Two library assets exist for procedural DSGC
morphology generation, with a `replace` correction overlay between them:

* **`procedural_dsgc_morphology_generator`** (created by t0090, library asset spec_version 2, module
  paths `code/morphology_params.py`, `code/generator.py`, `code/verification.py`,
  `code/constants.py`, `code/load_default_params.py`). Original 14-knob procedural generator;
  superseded by the fix below. **Direct use is forbidden by the t0093 correction overlay.**

* **`procedural_dsgc_morphology_generator_fix`** (created by t0092, spec_version 2, module paths
  `code/morphology_generator_fix.py`, `code/baseline_channels.py`, `code/paths.py`,
  `code/constants.py`). Drop-in replacement that patches the soma-pt3d collapse bug. Entry point
  `generate_fixed_morphology(*, params, morph_seed)` has the same signature as t0090's
  `generate_morphology` and returns the same `MorphologyResult` shape. **t0091 imports this library
  directly as
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.**
  This is the canonical morphology entry point per `C-0093-01`.

The correction overlay JSON
(`tasks/t0093_resweep_and_t0090_correction/corrections/library_procedural_dsgc_morphology_generator.json`)
is `action="replace"` with `replacement_task=t0092` and
`replacement_id=procedural_dsgc_morphology_generator_fix`. `verify_corrections.py` PASSES against
that file in t0093 [t0093]. Any cross-task code lookup for the procedural DSGC morphology generator
now resolves to t0092's patched module.

Both libraries are relevant to t0091 — t0091 imports the patched generator at the call site, and
inherits `MorphologyParams` / `MorphologyResult` / `BEDB_BASE_POINT` / `PARAM_BOUNDS` /
`StabilityKind` from t0090's `morphology_params.py` and `constants.py` (the patched library
explicitly leaves these dataclasses unchanged and re-uses them via re-export through t0090). The
t0091 implementation must **never** call t0090's `generate_morphology` directly, only through the
t0092 wrapper.

## Common Patterns

### Path management

Every prior task uses a `code/paths.py` module that exposes `TASK_ROOT`, `RESULTS_DATA_DIR`,
`IMAGES_DIR`, `INTERVENTION_DIR`, plus a per-task asset / output JSON catalogue and an
`ensure_directories()` helper that creates them idempotently
[t0080, t0081, t0083, t0086, t0088, t0093]. t0083 additionally exposes paths to its upstream task's
data files (`T0081_ALL_EVALUATIONS_JSON` etc.) so the warm-start / continuation script can consume
the prior artifact without hardcoded relative paths. t0091 must follow the same convention; in
particular, its `paths.py` must expose the t0083 Pareto archive path
(`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json`) and the t0083 full
evaluation history (`all_evaluations.json`) for the anchor electrophys-clone construction.

### Cross-platform NEURON bootstrap

t0080's `bootstrap.py` (117 lines) handles Windows-vs-Linux NEURON differences: it monkey-patches
t0024's `build_cell.py` to skip the Windows-only `NEURONHOME` check on Linux, runs `nrnivmodl` on
the t0024 vendored MOD sources to produce a Linux `.so`, and patches t0024's `load_neuron` with a
Linux-aware variant. Side-effect import (`from . import bootstrap as _bootstrap # noqa: F401`) makes
downstream importers work on both platforms without explicit calls [t0080]. t0091 inherits this
pattern by copying `bootstrap.py` (or equivalently importing it indirectly via a copied
`apply_params.py` / `build_cell_ais.py`).

### Per-cell evaluation loop

t0080's `trial_driver.py` (427 lines) is the canonical evaluator: it builds (or reuses cached) a
DSGC cell, applies the 54-d parameter vector, builds the synapse bundle, runs the 8-direction bar
sweep at N seeds via `ProcessPoolExecutor` with `cpu_count() - 1` workers, and aggregates to a DSI /
PD-rate / `is_unstable` `EvalResult`. Worker processes cache the cell in a module-level global
`_WORKER_CELL` and re-use it across trials with a parameter-vector-hash check
(`_WORKER_PARAMS_HASH`); rebuilding morphology is the most expensive step, so the cache yields a
~30% wall-clock saving for repeated parameter vectors [t0080]. t0091 must extend this pattern: the
cache key needs to include the morphology parameter hash (or the morphology vector itself), and the
cell must be **rebuilt** when the morphology vector changes — this is the structural difference
versus t0080 / t0081 / t0083, where morphology was fixed across the whole NSGA-II run.

### Smoke gate

t0081's `smoke_gate.py` (145 lines) re-evaluates t0080's 5 Pareto cells against a freshly compiled
substrate to detect substrate-version drift before launching the NSGA-II loop; tolerances
`DSI_TOLERANCE=0.05` / `PD_TOLERANCE_HZ=1.0` [t0081]. t0083's `smoke_gate.py` (229 lines) does the
same for t0081's gen-7 survivors. **t0091 needs an analogous gate: re-evaluate the 5 anchor cells
under the patched generator to catch any setup mistake before the 14-16 hour Vast.ai run.** This is
particularly important because t0091 is the first task to call the morphology generator inside the
loop — a smoke gate against the t0093 60-cell verification fingerprint protects against a silent
regression in the t0091 evaluator wrapper.

### NSGA-II loop with cost watchdog

t0080's `nsga2_loop.py` (394 lines) wraps pymoo's `NSGA2` algorithm with a `BedBV3Problem` that
declares natural-unit bounds (`xl=LOWER_BOUNDS, xu=UPPER_BOUNDS`), an inequality constraint for the
AIS-to-soma Nav ratio, and a per-cell time-based cost watchdog that writes
`intervention/budget_overrun.md` and short-circuits remaining cells when a hard cap is breached
[t0080]. The save-functions (`_save_pareto_front`, `_save_all_evaluations`, `_save_hv_trajectory`)
operate on a module-level `_ALL_EVALUATIONS` list, which t0083 cleverly **pre-populates** with the
prior task's history so saved files emit the union (additive, not destructive) [t0083].

### Adaptive HV-plateau stop

t0083's `hv_plateau_watchdog.py` (118 lines) implements `HVPlateauTermination` as a
`pymoo.core.termination.Termination` subclass. It reads `HV_TRAJECTORY_JSON` (written by t0080's
`_save_hv_trajectory` after each generation) and triggers when the mean of the last 3 relative-delta
values is below `HV_PLATEAU_REL_THRESHOLD=0.01` AND the trajectory has at least
`HV_PLATEAU_MIN_HV_HISTORY` entries (a minimum-generations guard). The watchdog is combined with
`MaximumGenerationTermination` via `TerminationCollection` so the run stops on either condition
[t0083]. t0091 reuses the same termination structure but with task-specific thresholds (8-gen cap,
2-gen plateau window per the task description).

### Warm-start population assembly

t0081's `warm_start.py` (182 lines) shows the canonical pattern for assembling warm-start matrices
in pymoo's natural-unit space: load prior Pareto cells from JSON, project / clamp them per-dim
against the current task's `[LOWER_BOUNDS, UPPER_BOUNDS]`, and fill remaining slots with `LHS()`
samples drawn against the problem instance [t0081]. t0091 needs an extended variant that builds **5
anchors x ~19 electrophys clones + 1 random sample = 96 cells**, where each anchor specifies a fixed
14-d morphology vector (Bed-B-like / symmetric / PD-asymmetric / ND-asymmetric / alt-topology) and
the 54-d electrophys part is sampled from the t0083 Pareto archive (preferring Genuine + Marginal
cells per t0086's classification). The construction is morphology-aware, which t0081 was not.

### Biological scorecard

t0086's `biological_priors.py` (179 lines) defines 9 `BiologicalPrior` records covering AIS Nav,
distal Nav1.6, distal NaP, NMDA per-synapse, NMDA voff, GABA rho0 / lambda, and AIS-to-soma Nav
ratio with published mean / sigma + DOI citations; `biological_scorecard.py` (201 lines) computes
per-prior `(centroid - mean) / sigma`, classifies as plausible / stretched / exotic against
thresholds 2 / 5 sigma, aggregates per cluster as worst-case, and renders a heatmap [t0086]. t0088's
`biological_scorecard.py` (198 lines) is a near-identical extension scoring 4 cluster reps under the
corrected NMDA prior (Sivyer 2013 corrected-units from t0090 Phase G.2). Both versions read centroid
coordinates from a `cluster_centroids.json` schema with field `centroid_unnormalised: list[float]`
of length 54. **For t0091, the priors and scorecard logic extend cleanly to 68-d: param_index lookup
remains in [0, 54) for all electrophys priors; new priors on morphology dimensions (e.g.
`soma_offset_pd_um`, `field_elongation_pd`, `branch_density_gradient_pd`) need to be added via new
`BiologicalPrior` records targeting indices 54-67.** Aggregator logic, heatmap, plausibility
verdicts all transfer unchanged.

### Cost watchdog (rate from machine_log.json)

t0086's `cost_watchdog.py` (132 lines) is the canonical fix for t0083's $0.83 budget overrun caused
by a hard-coded $0.2382/hr rate when the actual offer billed at $0.3209/hr. The watchdog reads the
per-instance hourly rate from `logs/steps/<setup-machines-step>/machine_log.json`
`selected_offer.price_per_hour` at module init, exposes `CostWatchdog` with `current_cost_usd()` /
`would_exceed_at_next_step()` / `trip_if_over_cap()`, and patches t0080's module-level
`_HOURLY_RATE_USD` so any nested call into t0080's evaluator inherits the resolved rate [t0086].
**t0091 must use this resolved-rate watchdog**, configured with `hard_budget_usd=4.00` per the task
description.

## Key Findings

### Cross-task code reuse rule for t0091

The t0091 build path imports from exactly **two task code/ trees**: t0090 (for `MorphologyParams` /
`MorphologyResult` / `constants.py` reflective re-exports through the t0092 wrapper) and t0092 (for
`generate_fixed_morphology` and `insert_baseline_channels`). Both are registered library assets, so
those imports comply with the cross-task code-reuse rule. Per the rule (specification + ARF README),
all other reusable code from t0080 / t0081 / t0083 / t0086 / t0088 / t0093 must be **copied into
t0091/code/** rather than imported. This is the critical structural decision for t0091's code
layout. The t0093 resweep_driver demonstrates this pattern: it imports t0090's `MorphologyParams`
and t0092's `generate_fixed_morphology` / `insert_baseline_channels` from library assets, but also
imports `apply_parameter_vector`, `setup_synapses_parametric`, `run_one_trial`, `ParameterVector`,
etc. from t0080 / t0086 — those non-library imports are incidental to a re-sweep that does not
change interfaces. **t0091 cannot rely on the same shortcut**: its evaluator wraps the morphology
generator inside the per-cell loop, so it owns the build path and must own its supporting code.

### Soma-area collapse bug and the patched generator

t0090 originally shipped `generate_morphology` whose `_materialise_neuron_sections` emitted two
coincident `pt3dadd` points for the soma when `start_xy == end_xy == (0, 0)` for the BedB-equivalent
base point. NEURON computed the cumulative pt3d distance as ~0, overriding `sec.L = soma_diameter`
to ~1e-9 um, producing a soma surface area of ~9.4e-14 um^2 and driving every cell to NaN voltage
within a few ms of synaptic input [t0092]. The fix in t0092's `morphology_generator_fix.py` (98
lines) calls `generate_morphology` unchanged, then patches the soma in place: clear pt3d, re-emit
two points along the z-axis at `(0, 0, 0, d_target)` and `(0, 0, soma_diameter_um, d_target)` with
`d_target = BEDB_AREA_TARGET_UM2 / (pi * soma_diameter_um)` so `pi * d * L = ~220 um^2`, matching
the t0024 hand-coded reference. The fix preserves all other fields (dendrite sections, AIS, terminal
locations, morphometric summary, connectivity) and is purely a post-hoc patch — no new randomness,
deterministic [t0092]. t0093 then ran the full 60-morphology Phase D verification under the patched
generator with the t0083 best-cell electrophys vector: **60 / 60 STABLE**, **56 / 60 with PD-rate
> 0**, **0 regressions** (vs t0090 pre-fix: 9 / 60 STABLE, 0 firing) [t0093]. The correction overlay
> `C-0093-01` (action `replace`, target_kind `library`) makes the t0092 wrapper the canonical
> generator for all downstream consumers.

### NSGA-II with mixed integer / real parameters

t0080 / t0081 / t0083 use pymoo's `NSGA2` with `LHS()` sampling and `SBX(eta=15, prob=0.9)` /
`PM(eta=20)` operators, declaring `BedBV3Problem(n_var=N_PARAMS, n_obj=2, n_ieq_constr=1)` in
natural-unit space [t0080]. Two of t0080's 54 dims are integer (N_ACH and N_GABA at indices 39 and
40); pymoo treats them as real and the `ParameterVector` accessors round to int in
`apply_parameter_vector`. **t0091 has 3 integer morphology dims**: `num_primary_branches` (3-7),
`max_strahler_depth` (2-6), and `morph_seed` (0 to 2^31-1). The same real-then-round-at-application
pattern works, with two caveats: (a) `morph_seed` should NOT be optimised — it must be held fixed
within an anchor and varied only for diversity (the t0091 task description treats it as part of the
14-d vector but the optimisation cost of mutating it is high and the diversity gain is dubious), and
(b) `num_primary_branches` and `max_strahler_depth` are causal topology dims whose discrete
boundaries can produce step-function changes in the fitness landscape, so SBX / PM with eta in the
moderate range (15 / 20) is appropriate.

### Morphology-aware worker cache

t0080's worker cache key is the parameter-vector hash; the cell is built once per process. **For
t0091 the cache must be morphology-aware**: rebuild the cell when the morphology vector changes, and
reuse it when only the electrophys part changes. The simplest implementation hashes the 14
morphology values separately (or the entire 68-d vector but with a hot-cold split). With pop 96 and
~5 seeds * 16 directions = 80 trials per cell evaluation, the per-cell wall-clock dominates over
worker-pool overhead, so an extra rebuild per cell on morphology change is acceptable. The t0093
`resweep_driver.py` already demonstrates this: it builds a fresh cell per morphology and applies a
fixed 54-d electrophys vector, achieving stable execution across 60 morphologies in ~50 minutes on
local 64-core EPYC [t0093].

### Anchor-tracking analysis pattern

t0086's `cluster_analysis.py` (359 lines) computes k-means + silhouette + bootstrap-stability ARI
across k=2..6 in 54-d normalised parameter space, with `_normalise(*, params_matrix)` using
`(params - LOWER_BOUNDS) / (UPPER_BOUNDS - LOWER_BOUNDS)` and `_unnormalise_vector` reversing it
[t0086]. **For t0091's anchor-tracking analysis**, the reverse problem applies: instead of finding
clusters, classify each Pareto cell to its **nearest of 5 known anchor centroids** in the 14-d
morphology subspace using the same min-max normalisation but restricted to indices 54-67. Bootstrap
significance (similar to t0086 / t0088's framework, ARI = 0.583 +/- 0.226 on small pools) is the
right idiom for the over- / under-representation test. This is a new piece of code in t0091 but
shares the normalisation primitives.

### Cluster framework extension to 68-d

t0086 / t0088 cluster cells in 54-d normalised parameter space using `LOWER_BOUNDS, UPPER_BOUNDS`
imported from t0080. **For t0091 the 68-d parameter vector concatenates the t0080 54-d bounds with
the t0090 14-d morphology bounds**:
`LOWER_BOUNDS_68 = np.concatenate([LOWER_BOUNDS_54, [3.0, 0.005, 2.0, 30.0, 0.5, -150.0, 1.0, -1.0, 0.0, 10.0, 8.0, 15.0, 0.0, 0.0]])`
matching the field order of `MorphologyParams`. Note the dimension that pymoo treats as integer
(`morph_seed`) has a huge nominal range that should be excluded from clustering — keep clustering
in 67-d (or 13-d morphology) skipping `morph_seed`. t0091 owns this concatenation and must validate
it via an assertion check.

### Vast.ai EPYC 7B13 64-core baseline performance

t0083 reported **~$0.40/hr at $0.3209/hr** EPYC 7B13 64-core throughput: **96 cells x 8 gens =
~$5.83 / 18.16 hours wall-clock** on the v3 substrate without morphology rebuilds [t0083]. t0091
will be slightly slower per cell because morphology rebuild adds ~1-2 seconds per cell (the t0093
resweep showed ~50 minutes for 60 cells under the patched generator, locally) — at remote EPYC
speed expect ~30-50 second additional per cell, so **~96 * 5 seeds * 16 dirs / 64 parallel ~12 min
per gen + ~30s overhead per cell rebuild on every morphology change ~= 14-15 minutes per gen, 8 gens
= ~2 hours per gen with overhead ~= 14-16 hours wall-clock and ~$5.60-6.40 ungated**. The t0091 cost
watchdog at $4.00 will trigger before completion of 8 gens unless the HV plateau watchdog fires
earlier — the task description's adaptive stop is the realistic path to budget compliance.

### Windows pre-commit and charmap codec quirks

The aggregator JSON output contains `>=` (Unicode `≥`) which breaks Python's default `cp1252`
codec on Windows when stdout is captured by hooks. **All script invocations from t0091 must set
`PYTHONIOENCODING=utf-8`**, in particular when running `flowmark` or any aggregator from PowerShell.
The current t0091 environment exhibits this: the bare
`uv run python -m arf.scripts.aggregators.aggregate_tasks --detail full` traceback fingerprint is
`UnicodeEncodeError: 'charmap' codec can't encode character '≥' in position ...`. With
`PYTHONIOENCODING=utf-8` set in the call environment the same command runs cleanly. The same fix
applies to flowmark when normalising files containing non-ASCII (degree signs, em-dashes, sigma
symbols).

## Reusable Code and Assets

### Library imports (cross-task allowed)

* **`generate_fixed_morphology`** -- **import via library**. Source:
  `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py` (line 78).
  Signature:
  `generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`.
  Builds the procedural DSGC cell with the soma-area patch applied; canonical entry point per
  `C-0093-01`. Used inside the per-cell evaluation loop. **No adaptation required.**

* **`insert_baseline_channels`** -- **import via library**. Source:
  `tasks/t0092_diagnose_morphology_generator_silence/code/baseline_channels.py`. Inserts HHst + cad
  on soma + dendrites + AIS of one cell. Idempotent. Use after `generate_fixed_morphology` and
  before `apply_parameter_vector`. **No adaptation required.**

* **`MorphologyParams`** -- **import via library** (transitively part of t0090's library asset,
  surfaced through t0092's wrapper). Source:
  `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` (line 39). 14-field
  frozen dataclass with `to_dict` / `from_dict` / `from_bedb_base_point`. **No adaptation
  required.**

* **`MorphologyResult`** -- **import via library**. Source:
  `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` (line 131). Frozen
  dataclass duck-typed as `DSGCCellWithAIS` (soma, all_dends, primary_dends, non_terminal_dends,
  terminal_dends, terminal_locs_xy, origin_xy, ais_proximal, ais_distal). **No adaptation
  required.**

* **`BEDB_BASE_POINT`, `PARAM_BOUNDS`, `PARAM_NAMES`, `INT_PARAM_NAMES`, `StabilityKind`** --
  **import via library**. Source:
  `tasks/t0090_morphology_generator_diversity_test/code/constants.py`. Use for the 14-d bounds
  vectors and the integer-parameter index list. **No adaptation required.**

### Files to copy from prior tasks into `t0091/code/`

* **`apply_params.py`** -- **copy into task** (228 lines). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/apply_params.py`. Applies a 54-d
  ParameterVector to a `DSGCCellWithAIS`-shaped target (which the patched `MorphologyResult` is
  duck-typed to satisfy). 5 tier-stratified write loops + 1 uniform-density loop + slow-AHP + AIS
  geometry. The function `apply_parameter_vector(*, cell, params)` is unchanged-shape; replace the
  import path of `DSGCCellWithAIS` with the local `MorphologyResult` protocol or import t0090
  `MorphologyResult` directly (recommended — simpler). Also copy `_T80_DLL_LOADED`,
  `ensure_t80_dll_loaded`, `_INSERTED_CELLS`, `_insert_channels_once`, `_INSERTED_BASELINE_CELLS`
  machinery. Adapt: change module-level imports from `tasks.t0080_..._dendritic_spike_nsga2.code...`
  to `tasks.t0091_..._nsga2_v1.code...` for `constants`, `paths`, `bootstrap`, `extend_with_ais`,
  `build_cell_ais`. Adapt `resolve_t80_mod_library()` -> `resolve_t91_mod_library()` and update the
  `mods/` path in t0091's `paths.py`.

* **`bootstrap.py`** -- **copy into task** (117 lines). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/bootstrap.py`. Cross-platform NEURON setup
  (Windows NEURONHOME / Linux nrnivmodl monkey-patch of t0024's `build_cell.load_neuron`). **No
  adaptation required** — the t0024 import path is stable.

* **`build_cell_ais.py`** -- **copy into task** (79 lines). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build_cell_ais.py`. `DSGCCellWithAIS`
  dataclass (slots=True) and `build_dsgc_cell_with_ais()` builder for the hand-coded baseline.
  **t0091 will not call `build_dsgc_cell_with_ais()` in the loop** (the morphology generator
  replaces it), but the dataclass type is needed by `apply_params.py` / `extend_with_ais.py` /
  `trial_driver.py` and is a useful smoke-gate target. Adapt: update imports.

* **`extend_with_ais.py`** -- **copy into task** (127 lines). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/extend_with_ais.py`. Two-subsegment AIS
  extension. Used by `apply_params.py` `update_ais_geometry`. **No adaptation required.**

* **`parametric_placer.py`** -- **copy into task** (105 lines). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/parametric_placer.py`. Distance-decay synapse
  placement on terminal dendrites, used by `setup_synapses_parametric`.

* **`recorder.py`** -- **copy into task** (122 lines). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/recorder.py`. Vm + spike recording helpers.

* **`trial_helpers.py`** -- **copy into task** (311 lines). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_helpers.py`. AR(2)-noise rates,
  bar-arrival times, GABA direction probability, ACh release probability,
  `setup_synapses_parametric(*, cell, n_ach, n_gaba, ...)` which builds the ACh + GABA + NMDA
  synapse bundle on the dendrites. Critical: this consumes a `DSGCCellWithAIS`-shaped cell, and
  `MorphologyResult` is intentionally duck-typed to that shape (per t0090's documentation), so the
  same function works without modification on the patched generator's output.

* **`trial_driver.py`** -- **copy into task** (427 lines, **adapt**). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_driver.py`. Per-cell evaluation loop
  with `ProcessPoolExecutor` and worker-cell cache. **Adapt: rebuild the worker cell when the
  morphology vector changes**, not only when the parameter vector changes. The current
  `_worker_prepare(*, params, placer_seed)` keys on `_hash_param_vector(params.values)` alone; t0091
  needs `_worker_prepare(*, params_68d, morph_params, placer_seed)` where the cell is rebuilt via
  `generate_fixed_morphology(params=morph_params, morph_seed=...)` whenever the morph hash changes.

* **`build_metrics.py`** -- **copy into task** (96-133 lines depending on source variant). Source:
  any of t0080 / t0081 / t0083 / t0086 (`build_metrics.py`). Aggregates per-cell results into the
  `metrics.json` format. Adapt to include 68-d cells and morphology-aware metrics.

* **`smoke_gate.py`** -- **copy into task** (145-229 lines depending on source). Source:
  `tasks/t0081_bedb_v3_warmstart_nsga2/code/smoke_gate.py` is the simpler of the two. Adapt to
  re-evaluate the **5 anchor cells** (Bed-B-like + symmetric + PD-asymmetric + ND-asymmetric +
  alt-topology) under the patched generator with a fixed t0083 best-cell electrophys vector,
  comparing DSI / PD against the t0093 60-cell verification fingerprint (Bed-B-equivalent: PD-rate
  ~43.6 Hz post-fix per the task description Phase A anchor 1 description).

* **`hv_plateau_watchdog.py`** -- **copy into task** (118 lines). Source:
  `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/code/hv_plateau_watchdog.py`. Adapt: change
  `HV_PLATEAU_MIN_HV_HISTORY` to t0091's gen-2 plateau window after a 4-gen warm-up minimum (8-gen
  cap + adaptive stop with growth threshold 1% over 2 gens, per task description).

* **`cost_watchdog.py`** -- **copy into task** (132 lines). Source:
  `tasks/t0086_robustness_cluster_bio_comparison/code/cost_watchdog.py`. Adapt:
  `T0091_HARD_BUDGET_USD = 4.00`. Use `make_watchdog_from_machine_log` factory and
  `patch_t0080_loop_rate` (rename to `patch_t91_loop_rate`).

* **`biological_priors.py`** -- **copy into task** (179 lines from t0086 + 14 morphology priors).
  Source: `tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py`. The 9
  electrophys priors copy verbatim. **Add new priors for morphology dims**: e.g. `soma_offset_pd_um`
  (mean 0, sigma 50 from Schachter 2010 / Trenholm 2013 displacement bounds), `field_elongation_pd`
  (mean 1.0, sigma 0.3 from Briggman 2011 dendritic field aspect ratios),
  `branch_density_gradient_pd` (mean 0, sigma 0.3 from anatomical symmetry priors), 4-7 priors
  total. New `param_index` values are 54-67. Adaptation: extend the `BIOLOGICAL_PRIORS` list and
  ensure `_centroid_value` handles the longer vector.

* **`biological_scorecard.py`** -- **copy into task** (201 lines from t0086 or 198 lines from t0088;
  the t0088 version has the corrected NMDA prior). Source:
  `tasks/t0088_recluster_marginals_and_vm_motifs/code/biological_scorecard.py`. **No structural
  adaptation required**: the per-prior scoring + worst-case aggregation handles arbitrary param
  index sets. The function signature `score_clusters() -> dict` consumes `cluster_centroids.json`
  and `biological_priors.json`. For t0091 the input is **per-Pareto-cell** rather than per-cluster;
  rename to `score_pareto_cells()` and feed the 68-d Pareto vectors as pseudo-centroids (one per
  cell, n_cells=1).

### New code that must be written for t0091

* **`anchor_definitions.py`** -- 14-d morphology vectors for the 5 anchors as `MorphologyParams`
  instances or as concrete dicts. Anchor 1 = `BEDB_BASE_POINT`. Anchors 2-5 deviate from base in
  specific dims per the task description Phase A table.

* **`generator_wrapper.py`** -- thin adapter that calls `generate_fixed_morphology` and adds the
  t0091-specific `keep_alive` GC defense (mirroring t0093's `_LIVE_CELLS` list and t0092's
  `keep_alive` helper).

* **`warmstart.py`** -- the 5-anchor x ~19-electrophys-clone construction, reading t0083's
  `pareto_front.json` + `all_evaluations.json` and t0086's `cell_classification.json` to filter
  Genuine + Marginal cells.

* **`evaluator.py`** -- 68-d `BedBV3Problem` analogue: declares `n_var=68, n_obj=2, n_ieq_constr=1`,
  splits the input into 14-d morphology + 54-d electrophys, calls `generator_wrapper.build_cell`
  then `apply_parameter_vector`, scores at 16 directions x 5 seeds.

* **`nsga2_driver.py`** -- pymoo `NSGA2` runner with `sampling=ndarray` (the warmstart pop matrix),
  `SBX(eta=15)` / `PM(eta=20, prob=1/68)`, `TerminationCollection(MaxGen(8), HVPlateauTermination)`,
  integrated cost watchdog. Mirrors t0080's `nsga2_loop.run_nsga2_loop`.

* **`pareto_analysis.py`** -- extract Pareto front, run the biological scorecard on each cell, emit
  summary tables.

* **`anchor_tracking.py`** -- compute each Pareto cell's nearest-anchor index in 14-d normalised
  morphology space; tabulate counts; bootstrap p-values for over- / under-representation.

* **`paths.py`** -- canonical t0091 path module: `RESULTS_DATA_DIR`, `IMAGES_DIR`, predicted
  artefacts (`pareto_front.json`, `all_evaluations.json`, `hv_trajectory.json`,
  `warm_start_population.json`, `anchor_tracking.json`, `biological_scorecard_68d.json`), upstream
  paths (`T0083_PARETO_FRONT_JSON`, `T0083_ALL_EVALUATIONS_JSON`, `T0086_CELL_CLASSIFICATION_JSON`,
  `MACHINE_LOG_JSON`), `INTERVENTION_DIR / BUDGET_OVERRUN_MD`, `ensure_directories()`.

* **`constants.py`** -- 68-d concatenated bounds (LOWER_BOUNDS_68, UPPER_BOUNDS_68), integer index
  list (3 morphology + 2 electrophys = 5 indices), pop / generation / SBX / PM constants,
  `T0091_HARD_BUDGET_USD = 4.00`, anchor names, plateau thresholds.

### Data assets to consume (no copy needed)

* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json` -- 18 t0083 Pareto
  cells with 54-d natural-unit `params` and `dsi` / `pd_rate_hz` / `is_feasible` / `is_unstable`.
  Used for warmstart electrophys clones.

* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` -- full 1728-cell
  history (768 from t0081 + 960 from t0083). Used for fallback if 18 Pareto cells x 5 anchors is
  insufficient (95 needed).

* `tasks/t0086_robustness_cluster_bio_comparison/results/data/cell_classification.json` -- 20 cells
  classified Genuine / Marginal / Stochastic. Used to prefer Genuine + Marginal cells for
  electrophys clones.

* `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/hv_trajectory.json` schema (the t0091
  watchdog will write its own `hv_trajectory.json` in the same format).

* `tasks/t0093_resweep_and_t0090_correction/results/data/post_fix_verification_summary.json` --
  60-cell post-fix DSI / PD / stability fingerprint. Used by the t0091 smoke gate to confirm the
  patched generator + electrophys application reproduces the t0093 fingerprint within tolerance.

## Lessons Learned

### Worked well

* **t0080's worker-cache pattern** saved ~30% wall-clock by amortising cell construction across
  trials. Persists in t0081 / t0083 / t0086 / t0093 unchanged. The same pattern with a
  morphology-aware key works for t0091 [t0080, t0081, t0083, t0086, t0093].
* **t0081's smoke gate** caught a substrate-build mismatch before launching the 14-hour run, saving
  cost. Pattern: re-evaluate prior task's Pareto under freshly compiled MOD library, fail if DSI /
  PD drift > tolerance [t0081, t0083].
* **t0083's HV-plateau watchdog** with `TerminationCollection(MaxGen, HVPlateauTermination)` cleanly
  combines the plateau test with a hard generation cap; the file-driven trajectory read decouples
  the watchdog from algorithm-internal state [t0083].
* **t0086's cost-watchdog rate-fix** read the per-instance hourly rate from `machine_log.json`
  rather than hardcoding it, eliminating the t0083 $0.83 budget overrun [t0086].
* **t0092's drop-in patch** was the minimal-surface-area fix for the t0090 bug: 98 lines wrapping
  `generate_morphology` and post-patching the soma. Verified by t0093's full 60-cell re-sweep with
  zero regressions [t0092, t0093].
* **t0093's correction overlay** redirects all downstream library lookups for the procedural
  generator without modifying any prior-task file, exactly per the corrections-mechanism design
  [t0093].

### Did not work / pitfalls to avoid

* **t0078's BoTorch qLogNEHVI MOBO** stalled at 49-d / pop ~80 due to O(N^3) GP scaling — pymoo
  NSGA-II replaced it for t0080 onwards. **For 68-d, NSGA-II is the only viable choice in this
  budget; do not revisit BoTorch** (matches the prior preference recorded for high-d MOBO follow-
  ups: NSGA-II via pymoo, not BoTorch qLogNEHVI) [t0078, t0080].
* **t0080's hard-coded $0.2382/hr rate** caused t0083's $0.83 overrun when the actual offer billed
  at $0.3209/hr. **Always resolve the rate from `machine_log.json`** [t0083, t0086].
* **t0090's coincident soma `pt3dadd` points** silently produced a degenerate cylinder for the
  Bed-B-equivalent base point; the bug was invisible from the structural-dump and only surfaced
  under synaptic input. **Always include a no-stim stability check + a synaptic-input firing check
  at the smoke-gate stage** [t0090, t0092].
* **Cell-id reuse after garbage collection** can cause t0080's `_INSERTED_CELLS` and
  `_INSERTED_BASELINE_CELLS` caches to skip channel insertion on a fresh cell that happened to be
  allocated at a previously-GCd cell's address. t0093 documented this with a module-level
  `_LIVE_CELLS` list that retains references to every built cell for the duration of the process
  [t0093]. **t0091 must use the same defense.**
* **Default Windows codec is `cp1252`** and breaks on Unicode `≥` (`>=`) which appears in several
  aggregator outputs and JSON fragments. Pre-commit hooks have been observed to fail on this. **Set
  `$env:PYTHONIOENCODING="utf-8"` in PowerShell before running aggregators or flowmark.**
* **t0093's resweep_driver imports from t0080 / t0086** in addition to library assets; this works
  because t0093 is the immediate downstream of those tasks and not a "first-of-kind" task. **t0091
  cannot do that** — t0091 is a structural break (morphology-in-loop) and must own its evaluator,
  so non-library code from t0080 / t0081 / t0083 / t0086 must be **copied** into t0091/code/.

### Performance observations

* t0083 EPYC 7B13 64-core: **96 cells x 8 gens, 18.16 hours, $5.83 at $0.3209/hr**, no morphology
  rebuild [t0083].
* t0086 EPYC 7B13 64-core: **20 cells x 5 reps x 24 dirs x 30 seeds = 72,000 trials, 4.59 hours,
  $1.595 at $0.3474/hr** [t0086].
* t0093 local 64-core EPYC, 16 workers, no remote: **60 morphologies x 8 dirs = ~50 minutes**
  [t0093]. Patched generator overhead is small but non-zero.

## Recommendations for This Task

* **Import `generate_fixed_morphology`, `insert_baseline_channels`, `MorphologyParams`,
  `MorphologyResult`, `BEDB_BASE_POINT`, `PARAM_BOUNDS`, `StabilityKind` directly from t0090 /
  t0092** (registered library assets). Wrap the build call in a `generator_wrapper.py` that attaches
  a `_LIVE_CELLS` GC-defense list per t0093.

* **Copy 9 t0080 / t0081 / t0083 / t0086 source files into t0091/code/** per the cross-task code
  reuse rule: `apply_params.py` (228), `bootstrap.py` (117), `build_cell_ais.py` (79),
  `extend_with_ais.py` (127), `parametric_placer.py` (105), `recorder.py` (122), `trial_helpers.py`
  (311), `trial_driver.py` (427, **adapt for morphology-aware cache**), `hv_plateau_watchdog.py`
  (118), `cost_watchdog.py` (132), `biological_priors.py` (179, **add morphology priors**),
  `biological_scorecard.py` (201, **rename score_clusters -> score_pareto_cells**), `smoke_gate.py`
  (145, **adapt to 5 anchors**). Total ~2491 lines copied; expect ~200-400 lines of t0091-specific
  adaptation on top.

* **Write 8 new modules** (target ~150-300 lines each): `paths.py`, `constants.py`,
  `generator_wrapper.py`, `anchor_definitions.py`, `warmstart.py`, `evaluator.py`,
  `nsga2_driver.py`, `pareto_analysis.py`, `anchor_tracking.py`.

* **Use NSGA-II via pymoo, not BoTorch qLogNEHVI**, with `pop_size=96`, `n_gen=8`,
  `SBX(eta=15, prob=0.9)`, `PM(eta=20, prob=1/68)`, `eliminate_duplicates=True`. Combine
  `MaximumGenerationTermination(8)` and `HVPlateauTermination` (2-gen window, 1% threshold) via
  `TerminationCollection`. The 14-d morphology dims share the same SBX / PM treatment as the
  electrophys dims; integer dims (`num_primary_branches`, `max_strahler_depth`, `morph_seed`,
  `n_ach`, `n_gaba`) round at apply time. **`morph_seed` should be held fixed per anchor** and not
  optimised — but if it must be in the parameter space (per the task description's 14-d count),
  set its mutation eta high (`eta=80`) so PM rarely changes it across generations.

* **Use t0086's `cost_watchdog` with `hard_budget_usd=4.00`**, factory
  `make_watchdog_from_machine_log` reading the t0091 `setup-machines` log; patch the t0091
  `nsga2_driver` module-level `_HOURLY_RATE_USD` at watchdog init. **Skip the budget watchdog only
  when running entirely locally** (Phases A, C, D, E).

* **Run the smoke gate against the t0093 60-cell post-fix verification fingerprint** before
  launching the Vast.ai NSGA-II run. The smoke gate should re-evaluate the 5 anchors with the t0083
  best-cell electrophys vector and confirm DSI within 0.05 and PD-rate within 1 Hz of t0093's
  recorded values for the BedB-equivalent point (anchor 1) and reasonable values for anchors 2-5.

* **Add at least 4 new biological priors targeting morphology dims** to the t0086 scorecard:
  `soma_offset_pd_um` (Schachter 2010 / Trenholm 2013), `field_elongation_pd` (Briggman 2011),
  `branch_density_gradient_pd` (anatomical symmetry, mean 0), `primary_branch_pd_concentration`
  (Vaney 2012). Cite the same papers used in `research_papers.md`. Then run the extended scorecard
  on every Pareto cell and emit a per-cell plausibility table.

* **Tabulate anchor membership in 14-d normalised morphology space** using min-max normalisation
  against `PARAM_BOUNDS`. Report counts per anchor (out of ~18 expected Pareto cells) and bootstrap
  p-values for the over- / under-representation hypothesis (anchor 3 vs anchor 4 being the strategic
  test).

* **Set `$env:PYTHONIOENCODING="utf-8"` for every aggregator / flowmark / verificator invocation on
  Windows.** Add this to the t0091 step scripts (PowerShell) — every `uv run` call in the
  pipeline. Also be aware the Windows pre-commit hook may fail on non-ASCII content unless this is
  set.

* **Restrict `generator_wrapper.py` to call `generate_fixed_morphology` only**. Never import or call
  `generate_morphology` from t0090 directly — the correction overlay `C-0093-01` mandates this and
  the smoke gate would catch a regression but only after the cell builds, not at static analysis
  time.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port the de Rosenroll 2026 DSGC compartmental model
* **Status**: completed
* **Relevance**: Provides the hand-coded DSGC cell that t0080-t0088 used as the substrate. The
  patched generator's soma-area target (~220 um^2) is calibrated to match this reference cell.
  t0080's `bootstrap.py` monkey-patches t0024's `load_neuron` for Linux; t0091 inherits that
  bootstrap.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP
* **Status**: completed
* **Relevance**: 49-d BoTorch qLogNEHVI predecessor that hit O(N^3) GP scaling and motivated the
  switch to NSGA-II. Provides the 17 Pareto cells used as warmstart seed in t0081. Confirms the
  recommendation against BoTorch for high-d MOBO at this scale.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Canonical NSGA-II driver, evaluation loop, parameter vector, AIS extension, synapse
  bundle, MOD library, cross-platform NEURON bootstrap. The single largest source of code to copy
  into t0091.

### [t0081]

* **Task ID**: `t0081_bedb_v3_warmstart_nsga2`
* **Name**: Bed B v3 NSGA-II warm-started with t0080 + t0078 Pareto cells
* **Status**: completed
* **Relevance**: Warm-start population assembly pattern (load JSON, project / clamp, LHS fill);
  smoke-gate pattern; 8-generation runtime fingerprint. t0091 extends this pattern from 22 prior
  cells + 74 LHS to 5 anchors x ~19 electrophys clones + 1 random.

### [t0083]

* **Task ID**: `t0083_bedb_v3_extend_nsga2_gen8plus`
* **Name**: NSGA-II continuation of t0081 from gen 8 to gen 17
* **Status**: completed
* **Relevance**: HV-plateau watchdog (combined with `MaximumGenerationTermination` via
  `TerminationCollection`); module-level `_ALL_EVALUATIONS` pre-population pattern; cost overrun
  case study that motivated t0086's rate-fix; canonical 18-cell Pareto archive used as the t0091
  warmstart electrophys source.

### [t0084]

* **Task ID**: `t0084_t0081_cell_767_vm_trace_deepdive`
* **Name**: Vm-trace deep-dive on t0081 cell 767
* **Status**: completed
* **Relevance**: Background context — established the NaP-dominant attribution for cell 767 that
  t0088 later extended to 4 cluster reps. Cited transitively for the mechanism-distinctness
  framework.

### [t0086]

* **Task ID**: `t0086_robustness_cluster_bio_comparison`
* **Name**: Robustness clustering + biological-scorecard comparison
* **Status**: completed
* **Relevance**: 9-prior biological scorecard with plausible / stretched / exotic verdict logic;
  cluster framework with k-means + bootstrap-stability ARI; cost watchdog reading hourly rate from
  `machine_log.json`. Critical scaffolding for t0091 Phase C.

### [t0088]

* **Task ID**: `t0088_recluster_marginals_and_vm_motifs`
* **Name**: Recluster t0086 cell pool with marginals + Vm-trace motifs
* **Status**: completed
* **Relevance**: Updated biological-scorecard variant with corrected NMDA prior;
  mechanism-distinctness metric; representative-cell selection; confirms NaP-dominant mechanism is
  universal across v3-substrate joint-pass cells. Establishes the prior-known
  biological-plausibility ceiling that t0091 is testing.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Procedural DSGC morphology generator diversity test
* **Status**: completed
* **Relevance**: Original procedural generator (14 knobs, soma-pt3d collapse bug); registered
  library asset `procedural_dsgc_morphology_generator` (superseded by C-0093-01). t0091 imports
  `MorphologyParams`, `MorphologyResult`, `BEDB_BASE_POINT`, `PARAM_BOUNDS`, `StabilityKind` from
  t0090's `morphology_params.py` and `constants.py`.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose t0090 morphology generator silence and ship soma-pt3d fix
* **Status**: completed
* **Relevance**: Patched generator `generate_fixed_morphology` (canonical entry point per
  C-0093-01); registered library asset `procedural_dsgc_morphology_generator_fix`. t0091 imports
  this as the ONLY morphology build path.

### [t0093]

* **Task ID**: `t0093_resweep_and_t0090_correction`
* **Name**: Patched-generator 60-cell re-sweep + correction overlay against t0090
* **Status**: completed
* **Relevance**: 60-morphology Phase D verification under the patched generator (60/60 STABLE, 56/60
  with PD-rate>0); correction overlay JSON `library_procedural_dsgc_morphology_generator.json`
  redirecting `procedural_dsgc_morphology_generator` to `procedural_dsgc_morphology_generator_fix`.
  Provides the smoke-gate fingerprint for t0091.
