---
spec_version: "1"
task_id: "t0112_t0106_seed77_replicate"
research_stage: "code"
tasks_reviewed: 11
tasks_cited: 9
libraries_found: 18
libraries_relevant: 0
date_completed: "2026-05-19"
status: "complete"
---
# Research Code — Seed-77 Minimum-Change Replicate of t0106

## Task Objective

t0112 is a deliberately minimum-change replicate of the t0106 long 2-direction NSGA-II run on the
68-d Bed B electrophys + 14-d morphology substrate. The same evaluator, the same NSGA-II
hyperparameters, the same silence guard, and the same predictions asset schema are reused verbatim.
Only three constants change: the GA seed (44 -> 77), the multiprocessing pool restart cadence
(`_POOL_RESTART_EVERY` 25 -> 10 in `nsga2_driver.py`), and the generation ceiling (`N_GEN` 300 ->
60). The goal is to test whether [t0106]'s 123-unique-joint-pass-cell breakthrough is a property of
the (substrate, objective) pair or a property of GA seed 44. This research stage identifies the
exact files to fork from [t0106], the exact patch sites, the cross-task imports kept versus copied,
and confirms the predictions asset schema this task must mirror.

## Library Landscape

The project does **not** ship a library aggregator (`arf/scripts/aggregators/` lacks
`aggregate_libraries.py`); libraries were enumerated by direct filesystem walk of
`tasks/*/assets/library/*/`. **18 library asset directories** exist; one (under t0010) is empty.
None of the 18 registered libraries is imported via its registered entry point by the t0078 -> t0106
NSGA-II lineage. The relevant cross-task code paths are all standard task-imports
(`tasks.tXXXX_*.code.<module>`), which the verificator allows but which are **not** library imports
under the project's `Cross-Task Code Reuse Rule`.

Libraries that touch the NSGA-II lineage and were considered for relevance:

* `de_rosenroll_2026_dsgc` (created by [t0024]) — the Bed B port. Transitively used by t0106 because
  `evaluator.py` imports `tasks.t0024_*.code.constants` and `ar2_noise.generate_ar2_batch`. **Not**
  imported via the registered entry point (`build_dsgc_cell`, `run_tuning_curve`); the lineage uses
  the raw `code/` modules.
* `procedural_dsgc_morphology_generator` (created by [t0090]) — original 14-d morphology generator.
  Superseded by [t0093] correction C-0093-01 in favour of [t0092]'s
  `procedural_dsgc_morphology_generator_fix`.
* `procedural_dsgc_morphology_generator_fix` (created by [t0092]) — patched 14-d generator,
  canonical via the corrections overlay. The t0106 `generator_wrapper.py` imports
  `tasks.t0092_*.code.morphology_generator_fix` and `tasks.t0092_*.code.baseline_channels`.
* `de_rosenroll_2026_dsgc_ais` (created by [t0078]), `de_rosenroll_2026_dsgc_ais_dendritic_spike`
  (created by [t0080]), `modeldb_189347_dsgc*` libraries — earlier-lineage models, not used by
  t0106.
* `dsgc_active_channel_pack` (created by t0074), `tuning_curve_viz`, `tuning_curve_loss`,
  `minimal_dsgc_*` libraries — unrelated to NSGA-II fitting.

**Net effect for t0112**: zero library imports via registered entry points. Every shared module
between t0112 and the t0024/t0080/t0090/t0092/t0106 ancestors is reached via the full-path import
pattern, identical to t0106.

## Key Findings

### The Patch Surface Is Exactly Two Constants, Plus One Generation Ceiling

The entire delta between [t0106] and t0112 lives in three lines of two files. Specifically:

* `tasks/t0106_long_pdnd_nsga2_300gen/code/nsga2_driver.py:97` — `_POOL_RESTART_EVERY: int = 25` ->
  `_POOL_RESTART_EVERY: int = 10`. The constant is named in the module docstring (lines 13-17) as
  "REQ-6: pool restart cadence (load-bearing for NEURON memory mitigation at 300 gens)" and is
  threaded through `PerGenerationPoolRestart.__init__` (line 357) as the `restart_every` kwarg
  default. The `_save_algorithm_config` function (line 442) also serialises the constant into
  `results/data/algorithm_config.json` as `"pool_restart_every"`, so the new value will be recorded
  end-to-end automatically.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/constants.py:58` — `T0106_SEEDS: tuple[int, ...] = (44,)`
  -> `T0112_SEEDS: tuple[int, ...] = (77,)`. The constant is consumed by `random_init.main()` (line
  96 of `random_init.py`) and by `run_three_seeds.sh` as the seed list to iterate. The
  backwards-compatibility aliases (`T0104_SEEDS`, `T0104_HARD_BUDGET_PER_SEED_USD`,
  `T0104_TASK_BUDGET_TOTAL_USD` on lines 65-67 of `constants.py`) must follow the rename.
* `constants_morphology.py:N_GEN` — 300 -> 60 to keep the budget bounded. The HV-plateau constants
  (`HV_PLATEAU_WINDOW`, `HV_PLATEAU_MIN_HV_HISTORY`, `HV_PLATEAU_REL_THRESHOLD`) stay at t0106
  values so the stopping criterion is identical.

There are **no other algorithm changes**. The evaluator, the silence guard, the SBX/PM operators,
the LHS init sampler, the cost watchdog, the dill checkpoint cadence, the operator-stop polling, and
the predictions asset writer all remain bitwise identical to [t0106].

### The Cross-Task Import Rule Forces a Copy of t0106's Code

Per `arf/specifications/research_code_specification.md` and the project rule
`Cross-Task Code Reuse Rule`, t0112 **MUST NOT** import from
`tasks.t0106_long_pdnd_nsga2_300gen.code`. Every non-library t0106 module must be copied into
`tasks/t0112_t0106_seed77_replicate/code/`. The same rule already governed [t0106]'s relationship to
[t0104] (see [t0106]'s `research_code.md` lines 142-205), and the established pattern is verbatim
copy with a global package-path rewrite: `tasks.t0106_long_pdnd_nsga2_300gen` ->
`tasks.t0112_t0106_seed77_replicate`.

The verificator does not flag full-path imports of UPSTREAM tasks (e.g.,
`tasks.t0024_*.code.constants`); only same-tier or downstream task imports are forbidden. So the
import edges from t0106 to t0024, t0080, t0090, t0092, t0093 stay valid in t0112 with the same
import strings — only `t0106_long_pdnd_nsga2_300gen` becomes `t0112_t0106_seed77_replicate`
everywhere it appears as a self-reference.

### The t0106 Code Tree Has 34 Python Modules Totalling 8,117 Lines

A full `wc -l` over `tasks/t0106_long_pdnd_nsga2_300gen/code/*.py` returns 8,117 lines across 34
files (including the empty `__init__.py`). Of these, the **algorithm-critical** modules that must be
copied verbatim into t0112 are:

* `nsga2_driver.py` (734 lines) — the only file that receives a real edit
  (`_POOL_RESTART_EVERY = 10`).
* `constants.py` (107 lines) — receives the seed rename and the budget constant rename.
* `constants_morphology.py` (159 lines) — receives the `N_GEN = 60` patch.
* `constants_electrophys.py` (547 lines) — verbatim.
* `evaluator.py` (504 lines) — verbatim (ratio DSI already correct at `N_DIRECTIONS=2`).
* `random_init.py` (101 lines) — verbatim except for the `T0106_SEEDS` -> `T0112_SEEDS` import name.
* `paths.py` (218 lines) — verbatim except for the package-path rewrite.
* `cost_watchdog.py` (129 lines) — verbatim (factory exported as `make_watchdog_from_machine_log`).
* `hv_plateau_watchdog.py` (89 lines) — verbatim.
* `bootstrap.py` (161 lines) — verbatim (NEURON DLL loader).
* `apply_params.py` (234 lines), `build_cell_ais.py` (79 lines), `extend_with_ais.py` (127 lines),
  `parametric_placer.py` (105 lines), `recorder.py` (122 lines), `trial_helpers.py` (311 lines) —
  evaluator support; verbatim.
* `generator_wrapper.py` (105 lines) — verbatim; the thin adapter around [t0092]'s patched
  morphology generator.
* `anchor_definitions.py` (149 lines), `anchor_classifier.py` (127 lines), `biological_priors.py`
  (252 lines), `biological_scorecard.py` (183 lines) — needed by `smoke_gate.py`.
* `smoke_gate.py` (192 lines) — verbatim; runs the 5 local pre-launch checks.
* `test_evaluator_dsi_guard.py` (164 lines) — silence-guard pytest; copy verbatim.

**Total bytes to copy**: ~5,800 lines of algorithm-critical code. The remaining ~2,300 lines
(analysis / charting / asset-build modules) can be ported on demand in the analysis stage; they are
not needed for the experiment-run step.

### The Predictions Asset Schema Is Already Defined and Must Be Mirrored Exactly

[t0106]'s predictions asset
(`tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/details.json`)
specifies `spec_version: "2"` and uses the following structure for the canonical evaluations file
(`files/all_evaluations_seed44.json.gz`):

* Top-level JSON object with one key `evaluations` -> list of per-cell records.
* Each record has fields: `generation` (int, 1 = LHS init, 2+ = offspring), `vector_68d` (list of 68
  floats = 54-d electrophys + 14-d morphology), `objective_F_minimised` (list of 2 floats =
  sign-flipped `[-ratio_dsi, -pd_rate_hz]`), `dsi_vector_sum` (float in [0, 1], guard-cleaned ratio
  DSI), `pd_rate_hz` (float, mean PD firing rate in Hz across the 3 noise replicates).
* File format is gzipped JSON (`.json.gz`), explicitly to satisfy the project's 5 MB pre-commit
  limit; decompress with `gunzip` before `json.load`.
* Required `metrics_at_creation` keys: `n_generations_completed`, `n_cells_total`, `best_dsi_ratio`,
  `best_pd_rate_hz`, `n_joint_pass_unique`, `n_joint_pass_evaluations`, `final_hypervolume`,
  `final_cost_usd`.
* Required top-level keys: `predictions_id`, `name`, `short_description`, `description_path`,
  `model_id` (nullable; [t0106] used `null`), `model_description`, `dataset_ids` (`[]`),
  `prediction_format`, `prediction_schema`, `instance_count`, `files`, `categories`,
  `created_by_task`, `date_created`.

The categories used by [t0106] are `direction-selectivity`, `compartmental-modeling`,
`retinal-ganglion-cell`; t0112 should inherit these unchanged. The `instance_count` field equals the
total number of evaluated cells (`POP_SIZE * (1 + n_gen_completed)` = 96 x (1 + 39) = 3,744 for
[t0106]; t0112 will produce a slightly different count depending on stop generation).

### The `dsi_vector_sum` Field Name Is Preserved for Schema Compatibility

[t0106]'s evaluator returns a 2-direction ratio DSI but writes it into the `dsi_vector_sum` JSON
field for back-compat with [t0102] / [t0104] downstream tooling (`build_predictions_assets.py`,
`build_analysis_charts.py`). t0112 must preserve this same field name; renaming it to `dsi_ratio`
would break any cross-task analysis script that walks both [t0106] and t0112 predictions assets. The
field name lie is documented in [t0106]'s `prediction_schema` string in `details.json` ("field name
preserved for compatibility with t0102/t0104 schema").

### NEURON Memory Creep Motivates the Pool-Restart Tightening

[t0106]'s `_POOL_RESTART_EVERY = 25` (lines 13-17 of the `nsga2_driver.py` module docstring) was
"NEW in the lineage (not present in [t0102] / [t0104])" and "load-bearing for 300-gen NEURON memory
mitigation". Per t0112's `task_description.md` (motivation point 2), wall-clock telemetry from
[t0106] showed growing per-evaluation memory footprint between restarts. The proposed cadence of 10
generations is conservative — at the t0112 N_GEN ceiling of 60, the pool restarts 6 times instead of
2\. The expected wall-clock penalty is ~2 minutes over the run (each pool restart pays one fresh
NEURON-import cost per worker, ~20 s per restart x 6 restarts x ~96 workers / 96 workers parallel).

### The Cost Watchdog Library Is `make_watchdog_from_machine_log`, Not a Registered Library

The task brief mentions `make_watchdog_from_machine_log` as if it might be a library; it is **not**.
It is a module-level factory function in `tasks/t0106_long_pdnd_nsga2_300gen/code/cost_watchdog.py`
(line 102), exported alongside the `CostWatchdog` dataclass and the
`load_hourly_rate_from_machine_log` helper. The factory reads
`logs/steps/008_setup-machines/machine_log.json`, extracts `selected_offer.price_per_hour`, and
constructs a `CostWatchdog` instance pinned to that hourly rate. The entire 129-line
`cost_watchdog.py` is copied verbatim into t0112 (with the package-path rewrite); the only knob
t0112 changes is the `hard_budget_usd` default passed into the factory at the driver call site (line
27 of `cost_watchdog.py` says `T0104_HARD_BUDGET_USD: float = 4.00`; t0112 should override at the
call site to `T0112_HARD_BUDGET_USD = 25.00` via constants.py).

### t0107's Re-Evaluation Confirms the 2-Direction DSI Is a Metric Artefact (Out of Scope but Informative)

[t0107] re-evaluated 10 randomly selected cells from the [t0106] top-50 at 8 directions and found
the t0106 ratio DSI of ~0.94 dropped to 8-direction vector-sum DSI of ~0.52. Rank order was
preserved (Spearman ρ = 0.758, p = 0.011). **This is out of scope for t0112**: the task brief
explicitly forbids any change to the substrate, objective, or evaluator. t0112 is a like-for-like
seed sweep, so it must report ratio DSI in the same metric and the same 2-direction protocol as
[t0106]. The [t0107] result is documented here only to signal that downstream comparison against
literature should use the 8-direction vector-sum re-evaluation, not the 2-direction ratio DSI raw
number.

### The `_POOL_RESTART_EVERY` Constant Threads Through Algorithm-Config Serialisation Automatically

In `nsga2_driver.py:442`, the `_save_algorithm_config` function writes
`"pool_restart_every": _POOL_RESTART_EVERY` into the `algorithm_config.json` file under
`results/data/`. Because the constant is read by reference at function call time, changing the
module-level constant from 25 to 10 will automatically propagate to the JSON output without any
additional patch. The predictions asset's `model_description` field should explicitly note the new
restart cadence to make the t0112 vs [t0106] diff visible at asset-review time.

## Reusable Code and Assets

Per the cross-task rule, **every** non-library module from [t0106] below is **copy into task**. The
library-asset imports from [t0024] and [t0090] / [t0092] are existing full-path task imports, not
library entry-point imports, but they remain valid in t0112 without any rewrite because they point
at upstream task code.

### Copy into task — algorithm-critical, verbatim except for the package-path rewrite

* `tasks/t0106_long_pdnd_nsga2_300gen/code/__init__.py` (0 lines) — package marker.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/bootstrap.py` (161 lines) — NEURON DLL loader; patches
  [t0024]'s `load_neuron` to load the [t0080] MOD library. Side-effect import; do not edit.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/apply_params.py` (234 lines) — 54-d electrophys-to-cell
  write function. Signature:
  `apply_parameter_vector(*, cell: DSGCCellWithAIS, vector: NDArray) -> None`.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/build_cell_ais.py` (79 lines) — `DSGCCellWithAIS`
  dataclass.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/extend_with_ais.py` (127 lines) — AIS extender used by
  `apply_params`.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/parametric_placer.py` (105 lines) — synapse-placer; no
  task-specific knobs.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/recorder.py` (122 lines) — Vm recording helper.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/trial_helpers.py` (311 lines) — `_bar_arrival_times`,
  `_rates_with_ar2_noise`, `_gaba_prob_for_direction`, `_rates_to_events`, `_count_spikes`,
  `setup_synapses_parametric`, plus `BASE_ACH_PROB`, `RATE_DT_MS`.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/generator_wrapper.py` (105 lines) — adapter around
  [t0092]'s `generate_fixed_morphology`. Signature:
  `build_cell(*, morph_params: MorphologyParams, morph_seed: int) -> MorphologyResult`.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/cost_watchdog.py` (129 lines) — Vast.ai cost watchdog;
  exports `CostWatchdog`, `load_hourly_rate_from_machine_log`, `make_watchdog_from_machine_log`,
  `patch_t99_loop_rate`. Verbatim. Only the budget constant changes via `constants.py`.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/hv_plateau_watchdog.py` (89 lines) — HV-plateau
  termination; signature: `HVPlateauTermination(seed=task_seed)`. Verbatim.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/evaluator.py` (504 lines) — `BedBV3MorphProblem`,
  `evaluate_68d_vector`. Verbatim.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/anchor_definitions.py` (149 lines),
  `anchor_classifier.py` (127 lines), `biological_priors.py` (252 lines), `biological_scorecard.py`
  (183 lines) — needed by `smoke_gate.py`. Verbatim.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/test_evaluator_dsi_guard.py` (164 lines) — silence-guard
  pytest. Copy verbatim and rerun under t0112 imports as part of smoke gate.
* `tasks/t0106_long_pdnd_nsga2_300gen/code/run_three_seeds.sh` — orchestration script; rename and
  trim to a single-seed `run_seed77.sh` since t0112 runs only one seed.

**Subtotal verbatim copy size**: ~3,400 lines across ~16 files (no edits beyond package-path
rewrite).

### Copy into task — receives a real patch

| File | Source | Patch |
| --- | --- | --- |
| `nsga2_driver.py` | t0106 (734 lines) | Line 97: `_POOL_RESTART_EVERY: int = 25` -> `_POOL_RESTART_EVERY: int = 10`. Update module docstring (lines 13-17) to reflect the new cadence. Update all `T0106_HARD_BUDGET_USD` references to `T0112_HARD_BUDGET_USD`. Package-path rewrite of every `tasks.t0106_*` to `tasks.t0112_*`. |
| `constants.py` | t0106 (107 lines) | Rename `T0106_SEEDS = (44,)` -> `T0112_SEEDS = (77,)`. Rename `T0106_HARD_BUDGET_USD` -> `T0112_HARD_BUDGET_USD` (keep value at $25.00 default; budget envelope check confirms ~$10-11 expected actual cost). Update backwards-compat aliases (`T0104_SEEDS`, etc.) to reference `T0112_SEEDS`. |
| `constants_morphology.py` | t0106 (159 lines) | `N_GEN: int = 300` -> `N_GEN: int = 60` (per task brief; HV-plateau stop still primary). All other constants verbatim. |
| `paths.py` | t0106 (218 lines) | Replace every occurrence of `t0106_long_pdnd_nsga2_300gen` with `t0112_t0106_seed77_replicate`. |
| `random_init.py` | t0106 (101 lines) | Rename `T0106_SEEDS` import to `T0112_SEEDS`. Package-path rewrite. |
| `smoke_gate.py` | t0106 (192 lines) | Package-path rewrite. No algorithm change. |
| `constants_electrophys.py` | t0106 (547 lines) | Verbatim (no t0106-specific references). |

### Cross-task imports kept (no copy)

These are full-path imports of UPSTREAM task code, not library imports, but the verificator allows
them and the entire t0080-t0106 lineage uses the same pattern:

* `tasks.t0024_port_de_rosenroll_2026_dsgc.code.constants` and `.ar2_noise.generate_ar2_batch` —
  upstream constants and AR(2) noise generator (Bed B port). Used by `trial_helpers.py` and
  `evaluator.py`.
* `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.mods/` — the **compiled MOD library**
  (`x86_64/.libs/libnrnmech.so`) is resolved at runtime by `paths.py:resolve_t99_mod_library`. Linux
  build is via `nrnivmodl` on the Vast.ai instance.
* `tasks.t0090_morphology_generator_diversity_test.code.morphology_params` — `MorphologyParams`,
  `MorphologyResult`, `MorphometricSummary` dataclasses (14-d morphology spec).
* `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix` and
  `baseline_channels.insert_baseline_channels` — patched generator (canonical via [t0093] correction
  C-0093-01).

### Library imports via registered entry points — **none**

No library is imported via its registered entry point. The cross-task imports above use the raw
`code/` module paths, identical to the t0078 -> t0106 lineage convention. This is intentional and
unchanged from [t0106].

## Common Patterns

### Path Management

[t0106] (and the entire NSGA-II lineage from t0091 forward) centralises all paths in `paths.py`,
including (a) the **upstream** [t0080] MOD library resolver `resolve_t99_mod_library`, (b) per-seed
result file factories (`pareto_front_json(seed=...)`, `all_evaluations_json(seed=...)`,
`hv_trajectory_json(seed=...)`), and (c) step-scoped log paths (`hv_trace_jsonl(step_id=...)`,
`checkpoint_dill(seed=..., gen=..., step_id=...)`, `stop_signal_md()`,
`budget_overrun_md(seed=...)`). t0112 inherits this convention verbatim by copying `paths.py` with
the package-path rewrite. The seed-77 per-seed file names will automatically be
`pareto_front_seed77.json`, `all_evaluations_seed77.json`, etc.

### Per-Seed Asset Naming

[t0106] used the predictions ID `nsga2-seed44-bedb-morph-2dir-300gen`. t0112's task brief specifies
`t0112-bedb-morph-nsga2-seed77` (see task_description.md line 63). The naming convention is
asset-relevant: the predictions asset folder name MUST match `predictions_id` in `details.json` (per
`meta/asset_types/predictions/specification.md`).

### Run Orchestration

[t0106]'s `run_three_seeds.sh` (re-purposed from the [t0104] 3-seed template) iterates over
`T0106_SEEDS = (44,)` — i.e., a degenerate single-element loop. For t0112, the loop will iterate
over `T0112_SEEDS = (77,)`. The script's per-seed cost-gate logic at the end can be removed (no
multi-seed gating needed), or simply renamed to `run_seed77.sh` and trimmed to a single invocation.

## Lessons Learned

### Long-Run Runs Need a Tighter Pool Restart Cadence Than 25 Generations

[t0106]'s plan acknowledged pool restart at 25 generations as a memory mitigation, but the post-task
results note "growing per-evaluation memory footprint between restarts". The proposed 10- generation
cadence in t0112 is the operationally direct response. At a NEURON-import cost of ~20 s per worker
per restart and 96 workers parallel, 6 restarts in a 60-gen run cost ~2 minutes — well under 1% of
the expected wall clock (~3 hours).

### Single GA Seed Is a Statistical Liability for Substrate Claims

[t0106]'s 3.3% joint-pass yield from a single seed (44) cannot be reported as a substrate property
without a replicate. This is the central motivation for t0112. If seed 77 produces >= 40 joint-pass
cells, the substrate is genuinely populated; if 0, [t0106] was seed-specific. The dichotomy is
strong enough that even one extra seed materially changes the headline claim.

### The Predictions Asset Is the One Mandatory Output; Analysis Modules Can Be Deferred

[t0106]'s code tree has ~2,300 lines of analysis modules (`build_analysis_charts.py`,
`build_predictions_assets.py`, `build_t0106_plots.py`, etc.). t0112's brief lists 5 charts to
produce, but the **mandatory** path is just the per-cell predictions table. Analysis modules can be
ported on demand in the analysis stage. This keeps the implementation step tight.

### Cost Cap Should Stay at $25 Even Though Expected Spend Is $10-11

[t0106]'s actual spend was $10.37 at the same pop/gen/eval budget. t0112's brief proposes a $25 hard
cap with $20 per-instance watchdog — same headroom as [t0106]. The project envelope ($18.20
remaining of $75 prior to this task) is tight; the watchdog must be wired correctly. The
`make_watchdog_from_machine_log` factory call must use `T0112_HARD_BUDGET_USD = 25.00` as the
`hard_budget_usd` kwarg, NOT the legacy `T0104_HARD_BUDGET_USD = 4.00` default in
`cost_watchdog.py:27`.

### t0107 Caveat Belongs in the Reporting Stage, Not Here

[t0107]'s 8-direction polar re-evaluation showed the 2-direction ratio DSI overstates selectivity by
~0.42 absolute. This is **out of scope** for t0112 (the task brief explicitly forbids any evaluator
change), but the reporting stage should note the caveat in the same language [t0106] used: "DSI =
0.939 in 2-direction ratio metric, expected ~0.52 in 8-direction vector-sum".

## Recommendations for This Task

1. **Fork the t0106 `code/` directory verbatim** into `tasks/t0112_t0106_seed77_replicate/code/`,
   using a single `git mv`-equivalent copy + global package-path rewrite
   (`sed -i 's/t0106_long_pdnd_nsga2_300gen/t0112_t0106_seed77_replicate/g'` across all `.py` and
   `.sh` files). Do not edit any algorithm logic.

2. **Apply exactly three patches**:
   * `nsga2_driver.py:97` — `_POOL_RESTART_EVERY: int = 25` -> `10`.
   * `constants.py:58` — `T0106_SEEDS: tuple[int, ...] = (44,)` ->
     `T0112_SEEDS: tuple[int, ...] = (77,)`. Rename `T0106_HARD_BUDGET_USD` ->
     `T0112_HARD_BUDGET_USD` and keep the value at 25.00. Update the backwards-compat `T0104_*`
     aliases.
   * `constants_morphology.py` — `N_GEN: int = 300` -> `60`.

3. **Verify the predictions asset schema matches [t0106] exactly** before launching. The asset
   folder must be named `t0112-bedb-morph-nsga2-seed77` (per task brief), the `details.json` must
   list `spec_version: "2"`, and the `prediction_schema` string must declare the same five per-cell
   fields (`generation`, `vector_68d`, `objective_F_minimised`, `dsi_vector_sum`, `pd_rate_hz`).
   Keep the `dsi_vector_sum` field name even though it stores the ratio DSI.

4. **Run the smoke gate locally before any Vast.ai provisioning** — the t0106 5-check protocol is
   already wired in `smoke_gate.py` (single-eval driver run, ratio DSI synthetic sanity,
   silence-guard unit tests, pool-restart sanity, watchdog wiring). All five must pass before
   `setup-machines`.

5. **Wire the cost watchdog explicitly with `T0112_HARD_BUDGET_USD = 25.00`** at the
   `make_watchdog_from_machine_log(...)` call site. Do not rely on the legacy
   `T0104_HARD_BUDGET_USD = 4.00` default that lives in `cost_watchdog.py:27`.

6. **Do not import any registered library entry point**. The lineage convention is full-path task
   imports of upstream `code/` modules; t0112 preserves this exactly. Keep the upstream imports of
   t0024, t0080, t0090, t0092 unchanged.

7. **Defer the analysis modules** (`build_analysis_charts.py`, `build_t0106_plots.py`,
   `cross_seed_analysis.py`, `per_seed_analysis.py`) to the analysis stage. The implementation stage
   only needs the driver, the predictions asset writer, and the smoke gate.

8. **Single-seed orchestration**: trim `run_three_seeds.sh` to `run_seed77.sh` with a single
   invocation. Remove the post-seed-44 budget gate block (it has no meaning at one seed).

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Upstream Bed B substrate definition. t0112's `evaluator.py` and `trial_helpers.py`
  import `tasks.t0024_*.code.constants` and `ar2_noise.generate_ar2_batch` directly. No change.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP
* **Status**: completed
* **Relevance**: First Bed B AIS-augmented MOBO run; established the 54-d electrophys parameter pack
  that became the basis for t0080's 54-d Bed B substrate inherited by t0106 / t0112. Showed the
  O(N^3) GP scaling failure that motivated the switch to NSGA-II.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Owns the canonical Linux MOD library (13 `.mod` files compiled under
  `mods/x86_64/`) resolved at runtime by t0106 (and therefore t0112)
  `paths.py:resolve_t99_mod_library`. The package-path rewrite does NOT change this dependency.

### [t0090]

* **Task ID**: `t0090_morphology_generator_diversity_test`
* **Name**: Morphology generator diversity test
* **Status**: completed
* **Relevance**: Defines the `MorphologyParams`, `MorphologyResult`, `MorphometricSummary`
  dataclasses imported by t0106 / t0112 `evaluator.py`. The library
  `procedural_dsgc_morphology_generator` is registered here but t0106 / t0112 use the
  [t0092]-patched generator per correction C-0093-01.

### [t0092]

* **Task ID**: `t0092_diagnose_morphology_generator_silence`
* **Name**: Diagnose morphology generator silence
* **Status**: completed
* **Relevance**: Owns the patched `morphology_generator_fix` and `baseline_channels` modules
  imported by t0106 / t0112 `generator_wrapper.py`. The patched generator is canonical via [t0093]
  correction C-0093-01.

### [t0099]

* **Task ID**: `t0099_random_init_pareto_robustness`
* **Name**: Random-init NSGA-II reproducibility test: 3 seeds vs t0091 Pareto
* **Status**: completed
* **Relevance**: Origin of the per-seed file naming convention (`pareto_front_seed{s}.json`,
  `all_evaluations_seed{s}.json`, `hv_trajectory_seed{s}.json`, `nsga2_checkpoint_seed{s}.json`)
  that t0112 inherits unchanged via `paths.py`.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, random init
* **Status**: completed
* **Relevance**: Direct ancestor of t0106; established the 2-seed pop=96 N_EVAL_SEEDS=4 gens=20
  NSGA-II template. t0106 (and t0112) inherit the silence guard
  (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`) and the `dsi_vector_sum` field name from this task.

### [t0104]

* **Task ID**: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* **Name**: 68-d 2-objective (DSI + PD-rate) NSGA-II at GA seeds=3, N=4, gens=20
* **Status**: completed
* **Relevance**: Drop-robustness-objective predecessor of t0106; established the 2-objective HV
  reference point `[0.0, 0.0]` and the `TerminationCollection` pattern (MaxGen + HVPlateau +
  CostWatchdog) inherited unchanged by t0106 / t0112.

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long 2-direction NSGA-II at 300 gens, 1 seed, 3 trials (ratio DSI + PD-rate)
* **Status**: completed
* **Relevance**: Parent task and dependency of t0112. Provides the entire code tree to copy (34
  files, 8,117 lines), the predictions asset schema to mirror, the smoke-gate harness to re-run, and
  the baseline run to compare against (123 unique joint-pass cells, best ratio DSI = 1.0000, best
  PD-rate = 122.62 Hz, final HV = 122.0288, cost $10.37).

### [t0107]

* **Task ID**: `t0107_t0106_polar_8dir_recheck`
* **Name**: 8-direction polar re-evaluation of 10 random top-50 t0106 cells
* **Status**: completed
* **Relevance**: Out-of-scope caveat task. Shows t0106's 2-direction ratio DSI overstates
  selectivity by ~0.42 absolute under conventional 8-direction vector-sum protocol. Relevant only
  for the t0112 reporting stage, not for the experiment-run step.

### [t0093]

* **Task ID**: `t0093_resweep_and_t0090_correction`
* **Name**: Patched-generator full 60-morph re-sweep + t0090 correction overlay
* **Status**: completed
* **Relevance**: Issued correction C-0093-01 marking [t0090]'s generator as superseded by [t0092]'s
  patched generator. t0112 (via t0106) imports [t0092]'s patched generator per this correction.
