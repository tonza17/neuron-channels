---
spec_version: "2"
task_id: "t0129_t0126_signed_dsi_real_rates_1seed"
date_completed: "2026-05-26"
status: "complete"
---
# Plan: Reproduce t0126 with Signed DSI and Real Per-Cell Firing Rates (1 Seed)

## Objective

Fork the t0126 Bed B + 14-d morphology NSGA-II substrate (68-d parameter vector, antipodal direction
pair `[0 deg, 180 deg]`, 60-generation production run, `_POOL_RESTART_EVERY = 10`, HV-plateau
auto-stop DISABLED) into a t0129-owned `code/` directory and re-run it on **one fresh GA seed
(3517)** with two evaluator corrections plus one diagnostic-persistence change:

1. **Signed antipodal DSI**: replace `_vector_sum_dsi` (range `[0, 1]`) with
   `_signed_antipodal_dsi(*, spike_counts_per_dir) -> float` returning the literature ratio
   `DSI = (R_PD - R_ND) / (R_PD + R_ND)` in range `[-1, 1]`. Reversed-preference cells (R_ND > R_PD)
   become detectable as negative values; vector-sum collapses them to the same magnitude as
   true-PD-preferring cells.

2. **Real per-cell firing rates**: expose `pd_rate_hz` and `nd_rate_hz` as named scalar fields on
   `CellEvalResult`, both computed as `mean(spikes_per_dir) / (TSTOP_MS / 1000.0)` from the actual
   per-direction spike counts the evaluator already records. No placeholder values, no offline
   synthesis pass, no env-var-driven sink that can silently drop in worker processes.

3. **Per-cell parameter dump**: write one JSONL row per evaluated cell (Phase A random init + every
   NSGA-II generation) to `results/cell_params.jsonl` containing
   `{gen, cell_idx, param_vector (68 floats), dsi_signed, atp_per_spike_molecules, pd_rate_hz, nd_rate_hz, silence_failed, n_errors}`.
   The sink path is passed through the `BedBV3MorphProblem` constructor so it pickles into worker
   processes — eliminating the env-var failure mode that produced t0126's synthesised
   `cell_trace_seed8929.jsonl` with `pd_rate_hz = 40` placeholders for every cell.

**Done** means: (1) NSGA-II terminates cleanly via the 60-generation ceiling or the budget cap; (2)
`results/cell_params.jsonl` has one row per evaluated cell with real (non-placeholder) `pd_rate_hz`
/ `nd_rate_hz`; (3) one predictions asset captures the final Pareto front under signed DSI with full
68-d vectors; (4) one answer asset addresses "Does the signed-DSI re-evaluation change the Pareto
structure vs t0126?"; (5) `results/metrics.json` registers `direction_selectivity_index` (the only
applicable registered metric) in the explicit multi-variant format with the new `signed_antipodal`
DSI dimension and a count of t0126-Pareto cells with `dsi_vector_sum > 0.5` but `dsi_signed < 0`
(reversed preference masked by magnitude); (6) the four required charts (Pareto front with negative
tail visible, signed-DSI distribution, PD-vs-ND scatter coloured by DSI, t0126-vs-t0129 Pareto
overlay) are saved to `results/images/`; (7) the inherited 9-check smoke gate passes on the
canonical Bed B anchor cell after the DSI helper rename. **t0127 and t0128 are out of scope**: not
read, not imported, not referenced.

* * *

## Task Requirement Checklist

Operative task text quoted verbatim from `tasks/t0129_t0126_signed_dsi_real_rates_1seed/task.json`
and the resolved long description at
`tasks/t0129_t0126_signed_dsi_real_rates_1seed/task_description.md`:

```text
Name: Reproduce t0126 with signed DSI=(PD-ND)/(PD+ND) and real per-cell firing rates

Short description: Reproduce t0126 NSGA-II on one fresh seed (3517) with
signed antipodal DSI=(PD-ND)/(PD+ND) replacing vector-sum DSI, and per-cell
pd_rate_hz/nd_rate_hz from actual spikes.

Dependencies: t0126_bedb_dsi_atp_per_spike_nsga2_60gen (only).
Expected assets: 1 predictions, 1 answer.
Task types: experiment-run, data-analysis, comparative-analysis.

Two evaluator changes:
* Change 1 (signed DSI): _signed_antipodal_dsi(*, spike_counts_per_dir) ->
  (R_PD - R_ND) / (R_PD + R_ND) in [-1, 1]. F = [-dsi_signed,
  +atp_per_spike_molecules]. WORST_CASE_DSI = -1.0 silence sentinel reused.
  Field rename dsi_vector_sum -> dsi_signed on CellEvalResult.
* Change 2 (real rates): pd_rate_hz = mean(pd_spikes) / (TSTOP_MS / 1000),
  nd_rate_hz = mean(nd_spikes) / (TSTOP_MS / 1000). Named scalar fields on
  CellEvalResult.

One diagnostic change:
* Change 3 (cell_params dump): results/cell_params.jsonl with one row per
  evaluated cell. Path captured at problem-construction time (no env var).
  Replaces the dropped cell_trace.jsonl.

Out of scope: t0127 and t0128 (do not import, read, or reference).

Hard invariants from t0126, preserved verbatim:
* _POOL_RESTART_EVERY = 10
* HV-plateau auto-stop DISABLED
* POP_SIZE = 96, N_EVAL_SEEDS = 3, N_DIRECTIONS = 2, N_GEN = 60
* Antipodal pair [0 deg, 180 deg], TSTOP_MS = 1400
* Silence guard at pd_spikes_sum < 3 returns WORST_CASE_DSI = -1.0
* Smoke gate passes on the canonical Bed B anchor cell
* Launch via run_seed3517.sh wrapper (NEVER direct driver invocation)
* GA seed = 3517 (fresh; lineage seeds 441, 6650, 8929, 2608, 8276, 9986
  excluded)

Expected outputs:
* assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/
* assets/answer/does-signed-dsi-change-t0126-pareto-structure/
* results/cell_params.jsonl
* results/images/pareto_front_dsi_signed_vs_atp.png
* results/images/dsi_signed_distribution.png
* results/images/pd_vs_nd_rate_scatter.png
* results/images/pareto_t0126_vs_t0129_overlay.png
```

Decomposed requirements (each step in `## Step by Step` cites the `REQ-*` items it satisfies). The
REQ-1..REQ-11 block satisfies the orchestrator-provided concrete acceptance criteria for this task;
REQ-12..REQ-23 cover the remaining invariants and outputs from the task description.

Mapping between the orchestrator's letter IDs (REQ-A..REQ-K from the task brief) and the numeric IDs
used below (the plan verificator regex requires numeric REQ IDs):

| Orchestrator | Plan | Topic |
| --- | --- | --- |
| REQ-A | REQ-1 | Signed antipodal DSI helper + unit tests |
| REQ-B | REQ-2 | `dsi_vector_sum -> dsi_signed` rename across consumers |
| REQ-C | REQ-3 | `pd_rate_hz` / `nd_rate_hz` as `CellEvalResult` fields |
| REQ-D | REQ-4 | `cell_params.jsonl` written per evaluated cell |
| REQ-E | REQ-5 | `run_seed3517.sh` wrapper |
| REQ-F | REQ-6 | Smoke gate passes after DSI rename |
| REQ-G | REQ-7 | 60-generation NSGA-II run completes |
| REQ-H | REQ-8 | Four required charts in `results/images/` |
| REQ-I | REQ-9 | Predictions asset with Pareto cells |
| REQ-J | REQ-10 | Answer asset on signed-DSI Pareto-structure question |
| REQ-K | REQ-11 | t0127 and t0128 NOT read or referenced |

* **REQ-1** — Implement helper
  `_signed_antipodal_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float` in
  `code/evaluator.py` returning `(R_PD - R_ND) / (R_PD + R_ND)` in range `[-1, 1]`. Returns
  `WORST_CASE_DSI = -1.0` when the denominator is zero. Implement four unit tests in
  `code/test_evaluator_dsi_signed.py`: (a) PD>ND positive case (PD=5, ND=1 -> 0.6667), (b)
  PD<ND negative case (PD=2, ND=10 -> -0.667), (c) PD=ND=0 silence sentinel returns -1.0, (d)
  PD=ND>0 zero case returns 0.0. Satisfied by Steps 4 and 6. Evidence:
  `uv run pytest tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/test_evaluator_dsi_signed.py -v`
  reports four new tests passing.

* **REQ-2** — Rename `dsi_vector_sum -> dsi_signed` on `CellEvalResult` and across every
  downstream consumer: `code/evaluator.py` (CellEvalResult field, two error-path constructors,
  `_summarise_trials`, `BedBV3MorphProblem._evaluate`), `code/smoke_gate.py` (checks 2, 7, 8),
  `code/test_evaluator_dsi_signed.py` (new file, replaces old test), `code/metrics_builder.py`
  (`row.get("dsi_vector_sum")` -> `row.get("dsi_signed")` plus
  `dimensions["dsi_metric"] = "signed_antipodal"`), `code/build_predictions_assets.py` (4 sites),
  `code/build_results.py` (3 sites), `code/post_run_analysis.py` (fallback chain at line 135-148),
  and the comparator scripts. Satisfied by Steps 3, 4, 5, 7, 11, 12. Evidence:
  `grep -rn "dsi_vector_sum" tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/` returns ZERO
  matches (or only matches inside the t0126 cross-comparison module that reads t0126's historical
  field name from the dependency).

* **REQ-3** — Expose `pd_rate_hz` and `nd_rate_hz` as named scalar fields on `CellEvalResult`,
  both computed as `mean(spikes_per_dir) / (TSTOP_MS / 1000.0)` from the actual per-direction spike
  counts. `pd_rate_hz` is already present in the t0126 fork; add `nd_rate_hz` populated
  symmetrically from `nd_spikes` (the per-direction spike list at the 180 deg direction). Satisfied
  by Step 4. Evidence: `grep -n "pd_rate_hz\|nd_rate_hz" code/evaluator.py` returns both fields on
  `CellEvalResult` and both assigned in `_summarise_trials`.

* **REQ-4** — Write `results/cell_params.jsonl` containing one row per evaluated cell across Phase
  A and every NSGA-II generation. Row schema:
  `{gen: int, cell_idx: int, param_vector: list[float] (68 floats), dsi_signed: float, atp_per_spike_molecules: float, pd_rate_hz: float, nd_rate_hz: float, silence_failed: bool, n_errors: int}`.
  The sink path must be **captured at `BedBV3MorphProblem.__init__`** (not resolved at call site,
  not from an env var) so the worker processes spawned by `multiprocessing.Pool` see it after
  pickling. Use a `multiprocessing.Lock` for serialised appends. Phase A uses `gen = -1`. Remove the
  `T0126_CELL_TRACE_JSONL` / `_cell_trace_path()` env-var dance entirely. Satisfied by Step 4.
  Evidence: after Phase A, `wc -l results/cell_params.jsonl` is `>= 96` (one row per random-init
  cell); after the full run, `wc -l` is `>= 96 + (96 * gen_completed)`.

* **REQ-5** — Implement `code/run_seed3517.sh` wrapper that (a) sets `SEED=3517`, (b) ensures
  `RESULTS_DATA_DIR` exists, (c) sources / imports `tasks.t0129_*.code.bootstrap` so the t0080 MOD
  library is compiled and loaded (handled inside the bootstrap module's import side effect), (d)
  runs Phase A `random_init` via `python -u -m tasks.t0129_*.code.random_init`, (e) launches the
  driver via
  `python -u -m tasks.t0129_*.code.nsga2_driver --seed 3517 --n-gen 60 --save-algorithm-config --teardown-on-watchdog`.
  The wrapper does NOT export `T0126_CELL_TRACE_JSONL` (removed because `cell_params.jsonl` is
  captured via the problem constructor). Satisfied by Step 5. Evidence:
  `bash tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/run_seed3517.sh` runs end-to-end (Phase A
  smoke + driver launch).

* **REQ-6** — Smoke gate passes on the fixed canonical Bed B reference cell after the DSI rename.
  Specifically: check 2 (synthetic DSI sanity) calls `_signed_antipodal_dsi({0.0: [5], 180.0: [1]})`
  and asserts the result is `4/6 = 0.6667` within `1e-6` (numerically identical to the old
  `_vector_sum_dsi({0.0: [5], 180.0: [1]})` because antipodal vector-sum reduces to the signed
  formula); check 7 (DSI/ATP sanity range) accesses `eval_res.dsi_signed` and asserts
  `-1.0 <= dsi <= 1.0`; check 8 (F sign convention) greps for `-result.dsi_signed`. Satisfied by
  Step 8. Evidence: `logs/steps/<n>_implementation/smoke_gate.json` reports all 9 checks pass; the
  canonical anchor cell's per-AP AIS ATP is within the first-principles canonical band
  `[1e8, 1e9] ATP/AP/cm` (Carter-Bean PASS).

* **REQ-7** — 60-generation NSGA-II run completes (or hits the budget cap) with seed 3517; Pareto
  front extracted from the final population to `results/data/pareto_front_seed3517.json` plus
  per-gen `all_evaluations_seed3517.json`. Live `TerminationCollection` contains EXACTLY
  `MaximumGenerationTermination(n_max_gen=60)` and `CostWatchdogTermination`; no
  `OperatorStopTermination`, no `HVPlateauTermination`. Satisfied by Steps 9 and 10. Evidence: the
  driver writes `logs/steps/<n>_implementation/hv_trace.jsonl` with 60 generation entries (or fewer
  if the watchdog tripped, with the watchdog reason logged in the final dill checkpoint).

* **REQ-8** — Produce the four required charts in `results/images/`:

  * `pareto_front_dsi_signed_vs_atp.png` — Pareto front with `dsi_signed` on y,
    `atp_per_spike_molecules` on x, **y-axis range widened to `(-1.05, 1.05)`** (was `(-0.05, 1.05)`
    in t0126's `post_run_analysis.py:192`), with a horizontal dashed line at `dsi_signed = 0`
    separating PD-preferring (above) from reversed-preference (below) cells.
  * `dsi_signed_distribution.png` — histogram of `dsi_signed` over every evaluated cell, with the
    negative tail visible on the same axis as the positive cluster.
  * `pd_vs_nd_rate_scatter.png` — scatter of `pd_rate_hz` vs `nd_rate_hz` coloured by
    `dsi_signed`, with the diagonal `pd_rate = nd_rate` line drawn (cells on this line have
    `dsi_signed ~ 0`).
  * `pareto_t0126_vs_t0129_overlay.png` — side-by-side or overlaid Pareto fronts: t0126's
    `pareto_front_seed8929.json` (read-only from the dependency task; t0126 cells reprojected
    through the t0129 signed-DSI formula using their recorded per-direction spike counts) vs the
    t0129 final front; cells whose `dsi_vector_sum > 0.5` but `dsi_signed < 0` annotated in red.

  Satisfied by Step 11.

* **REQ-9** — Build the predictions asset
  `assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/` containing: `details.json`
  (`prediction_format: "jsonl.gz"`, per-cell schema
  `{generation, cell_index, vector_68d, dsi_signed, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, pd_rate_hz, nd_rate_hz, objective_F_minimised, silence_failed_bool, legit_bool}`);
  `description.md`; `files/predictions.jsonl.gz` listing all Pareto-front cells with full 68-d
  parameter vectors. The asset MUST pass `arf/scripts/verificators/verify_predictions_asset.py` (if
  present; otherwise inherit the t0126 predictions schema). Satisfied by Step 12.

* **REQ-10** — Build the answer asset
  `assets/answer/does-signed-dsi-change-t0126-pareto-structure/` answering the question: "Does the
  signed-DSI re-evaluation of t0126's protocol change the Pareto structure, or is the vector-sum /
  signed distinction immaterial on the antipodal pair?" The short answer (2-5 sentences) opens with
  "Yes" / "No" / "I don't know" and states the supporting numbers (count of t0126-Pareto cells with
  `dsi_vector_sum > 0.5` but `dsi_signed < 0`; Pareto-front cell overlap between t0126 and t0129
  under their respective DSI definitions). The full answer cites the predictions asset, the
  `cell_params.jsonl` data, the comparator chart, and t0126's `pareto_front_seed8929.json`.
  Satisfied by Step 13.

* **REQ-11** — **t0127 and t0128 NOT read or referenced**. No file under
  `tasks/t0127_correct_t0126_cell_trace_suggestions/` or `tasks/t0128_t0127_rerun_dsi_atp_3seeds/`
  is imported, opened, or cited by t0129 code or documents. Satisfied implicitly by Steps 1-13.
  Evidence: `grep -rn "t0127\|t0128\|t0127_\|t0128_" tasks/t0129_t0126_signed_dsi_real_rates_1seed/`
  returns ZERO matches.

* **REQ-12** — Hard constant `_POOL_RESTART_EVERY = 10` preserved verbatim in `code/constants.py`
  (per project memory `feedback_nsga2_pool_restart_every_10`). Satisfied by Step 3. Evidence:
  `grep -n "_POOL_RESTART_EVERY" code/constants.py` returns `_POOL_RESTART_EVERY: int = 10`.

* **REQ-13** — Hard constant `HV_PLATEAU_AUTO_STOP = False` preserved verbatim, and the live
  `TerminationCollection` in `code/nsga2_driver.py` does NOT contain `HVPlateauTermination` (per
  memory `feedback_disable_hv_plateau_autostop`). Satisfied by Steps 3 and 9. Evidence: smoke gate
  check 6 (HV-plateau absence in live collection) passes.

* **REQ-14** — Hard constants `POP_SIZE = 96`, `N_EVAL_SEEDS = 3`, `N_DIRECTIONS = 2`,
  `N_GEN = 60`, `SILENCE_PD_SPIKES_THRESHOLD = 3`, `WORST_CASE_DSI = -1.0`, `TSTOP_MS = 1400`
  preserved verbatim from the t0126 fork. Satisfied by Step 3. Evidence:
  `grep -n "POP_SIZE\|N_EVAL_SEEDS\|N_DIRECTIONS\|N_GEN\|SILENCE_PD_SPIKES_THRESHOLD\|WORST_CASE_DSI\|TSTOP_MS" code/constants_morphology.py code/constants.py code/constants_electrophys.py`
  returns the expected values.

* **REQ-15** — GA seed `T0129_SEEDS = (3517,)` set in `code/constants.py`. The seed `3517` is
  confirmed fresh (NOT in the lineage seed set `{441, 6650, 8929, 2608, 8276, 9986}` documented in
  the orchestrator instructions). Satisfied by Step 3.

* **REQ-16** — Fork t0126's entire `code/` directory **verbatim** into
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/` first, then apply targeted edits. Drop the
  t0126-specific `build_t0126_outputs.py` orchestration (renamed to `build_t0129_outputs.py` if
  retained) and `t0124_vs_t0126_comparator.py` (rename to `t0126_vs_t0129_comparator.py` if used).
  Global string substitution
  `tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code -> tasks.t0129_t0126_signed_dsi_real_rates_1seed.code`
  and token rewrite `T0126_ -> T0129_` (keeping a back-compat alias
  `T0126_HARD_BUDGET_USD = T0129_HARD_BUDGET_USD` so any straggler imports resolve). Satisfied by
  Step 2.

* **REQ-17** — Add `CELL_PARAMS_JSONL: Path = RESULTS_DIR / "cell_params.jsonl"` to
  `code/paths.py` near the existing `RESULTS_DIR` block. The driver passes this constant to
  `BedBV3MorphProblem.__init__(cell_params_path=CELL_PARAMS_JSONL)` so worker processes see the path
  via the pickled problem object. Satisfied by Steps 3 and 9.

* **REQ-18** — Reuse `code/atp_per_spike.py` (Sengupta 2010 recipe), `code/recorder.py`
  (per-segment `seg.ina` recording for soma + AIS proximal + AIS distal + every dendritic segment),
  `code/bootstrap.py` (platform-aware NEURON / MOD compilation), and `code/cost_watchdog.py`
  verbatim (only import-path rewrite). Satisfied by Step 2. Evidence: `diff` of these files against
  t0126 shows only the package-path rewrite.

* **REQ-19** — Run the t0126-inherited 9-check smoke gate via
  `uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.smoke_gate` after the DSI
  rename. Carter-Bean check 9 (canonical anchor cell ATP/AP/cm within `[1e8, 1e9]` PASS band, or
  within the WARN band `[1e6, 1e14]`) must report PASS or WARN, not FAIL. Satisfied by Step 8.

* **REQ-20** — Compute the cross-comparison metric "count of t0126-Pareto cells with
  `dsi_vector_sum > 0.5` but `dsi_signed < 0`" by reading t0126's `pareto_front_seed8929.json`
  (read-only, from the dependency task), reprojecting each cell's recorded per-direction spike
  counts through the t0129 signed-DSI helper, and counting cells where the sign flips from
  positive-magnitude to negative. Write the count to `results/metrics.json` as a named variant
  dimension. Satisfied by Step 11.

* **REQ-21** — Write `results/metrics.json` using the explicit multi-variant format with: variant
  `t0129-seed3517-headline` (headline `direction_selectivity_index` from signed antipodal formula);
  variant `t0129-seed3517-pareto-median` (median `dsi_signed` and median `atp_per_spike_molecules`
  across the final Pareto front); variant `t0129-vs-t0126-sign-flipped` (count of t0126-Pareto cells
  with `dsi_vector_sum > 0.5` but `dsi_signed < 0`). Only registered `meta/metrics/` key
  `direction_selectivity_index` appears as a `metrics` entry; all other numeric outputs
  (`atp_per_spike_molecules`, `pd_rate_hz`, `nd_rate_hz`, `nd_rate_hz_pareto_median`, the sign-flip
  count) are reported as `dimensions` entries within each variant. Satisfied by Step 14.

* **REQ-22** — Reuse the existing t0126 DSI silence-guard regression test set (after porting to
  `dsi_signed` and adding the new PD<ND negative case). The full ported test set
  (`test_evaluator_dsi_signed.py`) must pass before NSGA-II launch. Satisfied by Step 6. Evidence:
  `uv run pytest tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/test_evaluator_dsi_signed.py -v`
  reports 0 failures.

* **REQ-23** — Persist a fixed-cell smoke-gate fixture (reference inputs and expected outputs for
  `_signed_antipodal_dsi` on the canonical Bed B anchor) inside the smoke gate JSON output at
  `logs/steps/<n>_implementation/smoke_gate.json` so any later regression test can reload it.
  Satisfied by Step 8.

* * *

## Approach

The work is a **fork-and-edit** reproduction of t0126's NSGA-II run on **one fresh seed (3517)**
with three behavioural deltas: (1) signed antipodal DSI replacing vector-sum DSI, (2) real
per-direction firing rates exposed as named `CellEvalResult` fields, (3) per-cell parameter dump
written through a constructor-captured path (no env var). t0127 and t0128 are explicitly out of
scope: their code is not read, their results are not consulted, their helpers are not imported.

**Why fork t0126's code/ verbatim first**: the t0126 module set (37 Python files) is a
production-quality NSGA-II pipeline that the project memory `feedback_consolidated_task_design`
documents as the canonical Bed B substrate. Forking verbatim minimises drift; the three deltas are
surgically applied as a single diff. The research_code.md identifies the exact lines to change
(`evaluator.py:356-376` `_vector_sum_dsi`; `evaluator.py:122` `CellEvalResult.dsi_vector_sum`;
`evaluator.py:632-665` `_append_cell_trace` env-var dance; `evaluator.py:697` `out["F"]` objective
construction; `smoke_gate.py:210, 313-374, 377-403` DSI references;
`metrics_builder.py:79, 118, 140` field accessors; `post_run_analysis.py:135-148, 192` y-axis range;
`nsga2_driver.py:325, 568, 628` `dsi_best_legit -> dsi_signed` rename and `cell_params_path`
constructor injection).

**Why signed antipodal DSI**: the standard direction-selective retinal ganglion cell (DS-RGC)
literature uses the signed ratio `DSI = (R_PD - R_ND) / (R_PD + R_ND)` in range `[-1, 1]` so
direction reversals are detectable. t0126's `_vector_sum_dsi` collapses the antipodal pair
`[0 deg, 180 deg]` to a non-negative scalar `|PD - ND| / (PD + ND)`; the magnitude is arithmetically
identical for an antipodal pair, but the sign is discarded. Reversed-preference cells (R_ND > R_PD)
look identical to true-PD-preferring cells of the same magnitude under vector-sum. The signed
formula recovers the distinction at zero algorithmic cost.

**Why real per-cell firing rates**: per project memory `project_t0126_cell_trace_synthesised`,
t0126's `cell_trace_seed8929.jsonl` was hand-synthesised after the run with `pd_rate_hz = 40` as a
hard-coded placeholder, because the env-var-driven cell_trace sink silently dropped in worker
processes (per `feedback_nsga2_launch_via_run_script`: direct driver invocation under tmux loses
`T0126_CELL_TRACE_JSONL`, the workers do not inherit it, the sink writes nothing). The evaluator
already computes real `pd_rate_hz` from spike counts at `evaluator.py:446`; t0129 just exposes the
symmetric `nd_rate_hz`, removes the env-var dependency entirely, and writes the JSONL through a path
captured at problem-construction time (pickled to workers).

**Why drop cell_trace JSONL and write cell_params.jsonl instead**: cell_trace recorded per-spike
timing detail used for downstream MI / Carter-Bean diagnostics; cell_params records only the
per-cell summary (parameter vector + four objective-related scalars + error flags). The orchestrator
brief is explicit: "skip cell_trace JSONL entirely" and "per-cell parameter dump to
results/cell_params.jsonl". The MI / Carter-Bean per-spike diagnostics are out of scope for this
task; if needed, a follow-up task can re-record per-spike timing.

**Recommended task types** (match `task.json`
`task_types = ["experiment-run", "data-analysis", "comparative-analysis"]`):

* **`experiment-run`** — the NSGA-II run is an experiment producing a predictions asset.
  Hypothesis: the signed-DSI re-evaluation reveals at least some cells in t0126's Pareto front whose
  preferred direction was reversed under the vector-sum collapse; alternatively (the null), all
  t0126 Pareto cells have genuine PD > ND so the signed re-evaluation reproduces the t0126 Pareto
  structure exactly. Independent variables: the 68-d parameter vector and the GA seed. Dependent
  variables: `dsi_signed`, `atp_per_spike_molecules`, `pd_rate_hz`, `nd_rate_hz`. Baseline: t0126's
  recorded Pareto front under vector-sum DSI (seed 8929).

* **`data-analysis`** — the post-run Pareto chart, DSI distribution histogram, PD-vs-ND scatter,
  and t0126-vs-t0129 overlay are data-analysis steps. Per the data-analysis Planning Guidelines,
  only registered `meta/metrics/` keys appear in `metrics.json`; the only applicable registered key
  is `direction_selectivity_index` (the other three — `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse` — require a full angular tuning curve, which the
  antipodal 2-direction protocol does not produce). All custom numeric outputs go in `dimensions`
  per the multi-variant format.

* **`comparative-analysis`** — explicit t0126-vs-t0129 cross-comparison via
  `pareto_t0126_vs_t0129_overlay.png` and the "count of t0126-Pareto cells with
  `dsi_vector_sum > 0.5` but `dsi_signed < 0`" metric. Per the comparative-analysis Planning
  Guidelines, the comparison reports both raw values and deltas.

**Alternatives considered (and rejected)**:

* **Alternative A — modify t0126's evaluator in place.** Rejected: violates the
  completed-task-immutability rule (CLAUDE.md Key Rule 5: "Nothing in a completed task folder may be
  changed; use the corrections mechanism in later tasks"). t0129 must fork the code and run
  independently.

* **Alternative B — run multiple fresh seeds (e.g., 3 seeds) for noise estimation.** Rejected: the
  orchestrator brief is explicit ("one fresh non-lineage seed: 3517"). A multi-seed extension is a
  legitimate follow-up if the single-seed result shows interesting sign-flip behaviour, but is not
  in scope here. The task description "Scope" section is also explicit: "Single fresh seed (3517)
  — not in the t0124 / t0126 / t0128 lineage. This is a first-pass replication; multi-seed scaling
  is left to a follow-up if results warrant."

* **Alternative C — keep cell_trace JSONL and add cell_params as an additional sink.** Rejected:
  the orchestrator brief is explicit ("skip cell_trace JSONL entirely"). The per-spike timing
  information is not needed for the signed-DSI Pareto re-evaluation; recording it would only
  re-introduce the env-var failure mode the task is designed to retire.

* **Alternative D — read t0127 / t0128 for context on what went wrong in t0126.** Rejected: the
  task description and orchestrator brief both explicitly forbid this. t0129 is a clean re-run
  scoped against t0126 only; t0127 / t0128 are separate lineages.

* **Alternative E — increase `N_GEN` beyond 60 for safety margin.** Rejected: the task description
  preserves t0126's 60-generation ceiling verbatim ("All other t0126 protocol parameters preserved
  verbatim"). Changing `N_GEN` would break the comparability with t0126.

* * *

## Cost Estimation

| Item | Estimated Cost | Notes |
| --- | --- | --- |
| NSGA-II 60-gen run (local CPU, single workstation) | $0.00 | Local CPU, no Vast.ai, no cloud. Electricity and CPU wear are not tracked under project budget. |
| API calls (LLM inference for planning / analysis) | $0.00 | None required. All analysis is deterministic Python on local artefacts. |
| Smoke-gate canonical cell evaluation | $0.00 | Local CPU; included in the wall-clock estimate, no $ cost. |
| **Estimated total actual cost** | **$0.00** | Within both the project per-task default $8 cap and the project remaining budget. |
| **Hard cap (T0129_HARD_BUDGET_USD)** | **$8.00** | Project-default per-task cap from `project/budget.json` (`per_task_default_limit: 8.0`). Cost watchdog tripped only if cumulative external cost ever exceeds this — for a local-CPU run, the watchdog will never trip. |

Comparison with project budget (`project/budget.json`: total $100, per-task default $8, no external
services in `available_services`): the $0 expected external spend is well within both the per-task
$8 cap and the $100 project budget. The watchdog wiring is preserved from t0126's fork so that any
unexpected paid service call (e.g., an inadvertent OpenAI API call) would still trip the cap.

* * *

## Step by Step

### Milestone 1 — Code Fork and Targeted Edits (Steps 1-7, local CPU)

1. **Preflight: confirm t0126 dependency health and lineage seed exclusion.** Run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m arf.scripts.aggregators.aggregate_tasks --format json --detail full --ids t0126_bedb_dsi_atp_per_spike_nsga2_60gen`
   and confirm the returned task has `status: "completed"` and that
   `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json` exists
   (read-only consumption only; needed for the t0126-vs-t0129 overlay in Step 11). Confirm seed 3517
   is NOT in the lineage seed set `{441, 6650, 8929, 2608, 8276, 9986}` (already verified by
   orchestrator). If either check fails, STOP and write an intervention file at
   `intervention/preflight_failed.md`. Expected output: log line "[preflight] t0126 status=completed
   OK; pareto_front_seed8929.json present OK; seed 3517 confirmed fresh". No REQ satisfied directly
   (preflight only).

2. **Fork the t0126 code/ directory verbatim, drop t0126-specific orchestration.** Copy every file
   in `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/` to
   `tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/`. Files to copy: `__init__.py`,
   `anchor_classifier.py`, `anchor_definitions.py`, `apply_params.py`, `atp_per_spike.py`,
   `biological_priors.py`, `biological_scorecard.py`, `bootstrap.py`, `build_assets.py`,
   `build_cell_ais.py`, `build_pareto_plots.py`, `build_predictions_assets.py`, `build_results.py`,
   `build_top50_morphologies.py`, `constants.py`, `constants_electrophys.py`,
   `constants_morphology.py`, `cost_watchdog.py`, `cuntz_balancing_factor.py`,
   `cytoplasm_volume.py`, `dsi_atp_comparators.py`, `evaluator.py`, `extend_with_ais.py`,
   `generator_wrapper.py`, `hv_plateau_watchdog.py`, `metrics_builder.py`, `mi_estimator.py`,
   `nsga2_driver.py`, `parametric_placer.py`, `paths.py`, `post_run_analysis.py`, `random_init.py`,
   `recorder.py`, `smoke_gate.py`, `sync_results_back.sh`, `trial_helpers.py`. Rename
   `run_seed8929.sh -> run_seed3517.sh` (edited in Step 5),
   `test_evaluator_dsi_guard.py -> test_evaluator_dsi_signed.py` (rewritten in Step 6),
   `build_t0126_outputs.py -> build_t0129_outputs.py` (path rewrites only),
   `t0124_vs_t0126_comparator.py -> t0126_vs_t0129_comparator.py` (path rewrites only — this
   script computes the cross-comparison chart). Then run a global string substitution
   `tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code -> tasks.t0129_t0126_signed_dsi_real_rates_1seed.code`
   and `T0126_ -> T0129_` across all `.py` and `.sh` files (use `grep -rn "t0126\|T0126" code/` and
   address any residual matches inside docstrings or cross-task overlay code that legitimately reads
   t0126's frozen artefacts). Add a back-compat alias
   `T0126_HARD_BUDGET_USD: float = T0129_HARD_BUDGET_USD` and similar for
   `T0126_PER_INSTANCE_WATCHDOG_USD` so any straggler imports resolve. Expected output: `ls code/`
   shows ~37 forked Python files plus the renamed shell wrapper and test/comparator. Satisfies
   REQ-16.

3. **Edit `code/constants.py`, `code/constants_morphology.py`, and `code/paths.py` for the t0129
   seed and the cell_params sink.** Apply the following changes:

   * In `code/constants.py`:
     * Replace `T0126_SEEDS = (8929,)` with `T0129_SEEDS: tuple[int, ...] = (3517,)`. Preserve a
       back-compat alias `T0126_SEEDS = T0129_SEEDS` so any straggler imports resolve. Document the
       rejection criteria in a docstring (lineage seeds excluded:
       `{441, 6650, 8929, 2608, 8276, 9986}`).
     * Preserve `_POOL_RESTART_EVERY: int = 10` verbatim (REQ-12; project memory
       `feedback_nsga2_pool_restart_every_10`).
     * Preserve `HV_PLATEAU_AUTO_STOP: bool = False` verbatim (REQ-13; project memory
       `feedback_disable_hv_plateau_autostop`).
     * Preserve `T0129_HARD_BUDGET_USD: float = 8.0` (renamed from t0126's `6.0`; widened to project
       per-task default for local-CPU runs where the cap is purely defensive).
     * Update the module docstring to reference t0129 and explicitly state "Signed antipodal DSI;
       real per-cell firing rates persisted; cell_params.jsonl via constructor-captured path".

   * In `code/constants_morphology.py`: keep `POP_SIZE: int = 96`, `N_EVAL_SEEDS: int = 3`,
     `N_DIRECTIONS: int = 2`, `N_GEN: int = 60`, `SILENCE_PD_SPIKES_THRESHOLD: int = 3`,
     `WORST_CASE_DSI: float = -1.0`, `TSTOP_MS = 1400` (REQ-14).

   * In `code/paths.py`: add `CELL_PARAMS_JSONL: Path = RESULTS_DIR / "cell_params.jsonl"` near the
     existing `RESULTS_DIR` block (REQ-17).

   Expected output:
   `grep -n "POP_SIZE\|N_EVAL_SEEDS\|N_DIRECTIONS\|N_GEN\|_POOL_RESTART_EVERY\|HV_PLATEAU_AUTO_STOP\|T0129_HARD_BUDGET_USD\|T0129_SEEDS\|CELL_PARAMS_JSONL" code/constants.py code/constants_morphology.py code/paths.py`
   returns the expected values. Satisfies REQ-12, REQ-13, REQ-14, REQ-15, REQ-17.

4. **Edit `code/evaluator.py` with the three behavioural changes as a single coherent diff.** Apply
   all changes in one commit so the diff against t0126 is reviewable:

   * **Change 1 (signed DSI helper)**: Replace `_vector_sum_dsi` at lines 356-376 with a new helper:

     ```python
     def _signed_antipodal_dsi(
         *,
         spike_counts_per_dir: dict[float, list[int]],
     ) -> float:
         """Signed antipodal DSI = (R_PD - R_ND) / (R_PD + R_ND), range [-1, 1].

         Assumes exactly two antipodal directions (PD at PD_DIRECTION_DEG = 0.0 and
         ND at 180.0). Returns WORST_CASE_DSI = -1.0 when the denominator is zero.
         """
         pd_dir = PD_DIRECTION_DEG  # 0.0
         nd_dir = PD_DIRECTION_DEG + 180.0  # 180.0
         pd_spikes = spike_counts_per_dir.get(pd_dir, [])
         nd_spikes = spike_counts_per_dir.get(nd_dir, [])
         r_pd = float(np.mean(pd_spikes)) if len(pd_spikes) > 0 else 0.0
         r_nd = float(np.mean(nd_spikes)) if len(nd_spikes) > 0 else 0.0
         denom = r_pd + r_nd
         if denom <= 0.0:
             return WORST_CASE_DSI
         return (r_pd - r_nd) / denom
     ```

     Delete `_vector_sum_dsi` entirely (no dead helpers).

   * **Change 2 (CellEvalResult field rename + nd_rate_hz)**: Rename `CellEvalResult.dsi_vector_sum`
     (line 122) to `dsi_signed: float`. Add a sibling field `nd_rate_hz: float` (after `pd_rate_hz`
     at line 123). In `_summarise_trials`, after computing
     `pd_rate_hz = float(np.mean(pd_spikes)) / (TSTOP_MS / 1000.0)` at line 446, add the symmetric
     `nd_rate_hz = float(np.mean(nd_spikes)) / (TSTOP_MS / 1000.0)`. Update every reference to
     `result.dsi_vector_sum` in this file: error-path `CellEvalResult(...)` constructors at lines
     415-433, 540-559, 610-629; `_summarise_trials` body at lines 443, 445, 503; and
     `BedBV3MorphProblem._evaluate` at line 697
     (`out["F"] = np.array([-result.dsi_signed, +result.atp_per_spike_molecules], dtype=np.float64)`).
     Satisfies REQ-1 (helper), REQ-2 (rename), REQ-3 (rates).

   * **Change 3 (cell_params dump via constructor-captured path)**: Remove `_cell_trace_path()` and
     `_append_cell_trace` (lines 145-152 and 632-665) and the `T0126_CELL_TRACE_JSONL` /
     `T0122_CELL_TRACE_JSONL` env-var dependency entirely. Add a new helper
     `_append_cell_params(*, sink_path: Path, lock: multiprocessing.Lock, row: dict[str, Any]) -> None`
     that serialises a dict to JSONL via
     `lock.acquire(); sink_path.open("a").write(...); lock.release()` (use a `with` block for the
     lock). Modify `BedBV3MorphProblem.__init__` to accept `cell_params_path: Path` and store it on
     the instance (also create a `multiprocessing.Manager().Lock()` so it pickles into workers
     correctly). In `BedBV3MorphProblem._evaluate` at lines 689-707, after `result` is computed and
     before `out["F"]` is set, build the row
     `{gen: <gen_from_generation_callback>, cell_idx: <idx>, param_vector: <68-d list from x.tolist()>, dsi_signed: result.dsi_signed, atp_per_spike_molecules: result.atp_per_spike_molecules, pd_rate_hz: result.pd_rate_hz, nd_rate_hz: result.nd_rate_hz, silence_failed: result.silence_failed, n_errors: result.n_errors}`
     and call
     `_append_cell_params(sink_path=self._cell_params_path, lock=self._cell_params_lock, row=row)`.
     The `gen` value defaults to `-1` for Phase A and is set to the current NSGA-II generation index
     in Phase B (the `_GenerationCallback` in `nsga2_driver.py` already maintains this counter).
     Satisfies REQ-4.

   * **Package import path rewrite** (mechanical): lines 38-96 update from `tasks.t0126_*` to
     `tasks.t0129_*` (already handled by Step 2 global substitution; verify here).

   Expected output:
   `grep -n "_vector_sum_dsi\|T0126_CELL_TRACE_JSONL\|_cell_trace_path\|_append_cell_trace" code/evaluator.py`
   returns ZERO matches;
   `grep -n "_signed_antipodal_dsi\|dsi_signed\|nd_rate_hz\|_append_cell_params" code/evaluator.py`
   shows all three new symbols. Satisfies REQ-1, REQ-2, REQ-3, REQ-4.

5. **Edit `code/run_seed3517.sh` to remove the env-var dance and update seed / paths.** Source: the
   renamed copy of `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/run_seed8929.sh`. Apply:

   * `SEED=8929` -> `SEED=3517`.
   * Remove the env-var dance at lines 42-47 (`CELL_TRACE_JSONL`, `T0126_CELL_TRACE_JSONL`,
     `T0122_CELL_TRACE_JSONL`). The cell_params path is captured via the
     `BedBV3MorphProblem.__init__(cell_params_path=...)` injection in the new evaluator (Step 4
     Change 3); no env var needed.
   * Keep the Phase-A `random_init` invocation:
     `"${PY}" -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.random_init`.
   * Keep the bootstrap import as an explicit `python -c` invocation so the t0080 MOD library is
     loaded on first call.
   * Keep the driver launch with
     `--seed "${SEED}" --n-gen 60 --save-algorithm-config --teardown-on-watchdog` (the watchdog
     wiring stays as defensive insurance even for local-CPU runs).
   * Update all `tasks.t0126_*` module paths to `tasks.t0129_*`.

   Expected output: `bash -n code/run_seed3517.sh` returns 0 (shell syntax OK);
   `grep -n "T0126_CELL_TRACE_JSONL\|T0122_CELL_TRACE_JSONL" code/run_seed3517.sh` returns ZERO
   matches. Satisfies REQ-5.

6. **Port and extend the DSI silence-guard regression tests to
   `code/test_evaluator_dsi_signed.py`.** Source: the renamed copy of
   `code/test_evaluator_dsi_guard.py` (186 lines, 7 existing tests). Adapt all existing tests to (a)
   import `_signed_antipodal_dsi` instead of `_vector_sum_dsi`, (b) access `result.dsi_signed`
   instead of `result.dsi_vector_sum`. Tighten the `test_three_pd_spikes_does_not_trip_guard`
   assertion from `> 0.0` to `== 1.0` (signed antipodal with `(PD=3, ND=0)` gives
   `(3-0)/(3+0) = 1.0`). Add **one new test** `test_signed_dsi_negative_when_nd_dominates`: assert
   `_signed_antipodal_dsi({0.0: [2], 180.0: [10]})` returns `(2-10)/(2+10) = -0.6667` within `1e-6`.
   Add **one new test** `test_signed_dsi_zero_when_pd_equals_nd`: assert
   `_signed_antipodal_dsi({0.0: [5], 180.0: [5]})` returns `0.0` within `1e-9`. Verification
   criteria require: (a) PD>ND positive case (covered by `test_three_pd_spikes_does_not_trip_guard`
   tightened to `== 1.0` AND the pre-existing test `_vector_sum_dsi(PD=5, ND=1) == 4/6` ported to
   the new helper), (b)
   PD<ND negative case (new `test_signed_dsi_negative_when_nd_dominates`), (c) PD=ND=0 silence sentinel = -1.0 (covered by existing silence-guard tests, now asserting `dsi_signed == -1.0`), (d) PD=ND>0
   zero case (new `test_signed_dsi_zero_when_pd_equals_nd`). Run the full test set:
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run pytest tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/test_evaluator_dsi_signed.py -v`.
   Expected output: all tests pass (the original 7 + 2 new = 9 tests). If any test fails, STOP and
   debug. Satisfies REQ-1, REQ-22.

7. **Edit `code/nsga2_driver.py`, `code/smoke_gate.py`, `code/metrics_builder.py`,
   `code/post_run_analysis.py`, `code/build_predictions_assets.py`, `code/build_results.py`, and
   `code/t0126_vs_t0129_comparator.py` for the `dsi_signed` rename and `cell_params_path`
   injection.** Apply:

   * `nsga2_driver.py:325, 628` — rename dumped field `dsi_best_legit` to `dsi_signed`; update the
     `_save_iteration` comment block at lines 314-318. At line 568 where `BedBV3MorphProblem(...)`
     is constructed, add `cell_params_path=CELL_PARAMS_JSONL` kwarg (import `CELL_PARAMS_JSONL` from
     `code/paths.py`). Confirm the live `TerminationCollection` in `_build_termination` (lines
     211-224) contains EXACTLY `MaximumGenerationTermination(n_max_gen=N_GEN)` (=60) and
     `CostWatchdogTermination`. **`OperatorStopTermination` and `HVPlateauTermination` MUST NOT
     appear in the live collection** (REQ-13; project memory
     `feedback_disable_hv_plateau_autostop`). Per `_POOL_RESTART_EVERY: int = 10` at line 105, the
     `PerGenerationPoolRestart` callback fires every 10 gens (REQ-12).

   * `smoke_gate.py:210-223` (check 2) — call `_signed_antipodal_dsi({0.0: [5], 180.0: [1]})` (was
     `_vector_sum_dsi`); the numeric assertion `== 4/6 = 0.6667` is unchanged because the antipodal
     vector-sum reduces to the signed formula. `smoke_gate.py:313-374` (check 7) — replace
     `eval_res.dsi_vector_sum` (line 359) with `eval_res.dsi_signed`; the range check
     `-1.0 <= dsi <= 1.0` is unchanged. `smoke_gate.py:377-403` (check 8) — update the grep target
     from `-result.dsi_vector_sum` to `-result.dsi_signed`. Checks 1, 3, 4, 5, 6, 9 unchanged in
     logic; only package-path rewrites (handled by Step 2).

   * `metrics_builder.py:79, 118, 140` — `row.get("dsi_vector_sum", 0.0)` ->
     `row.get("dsi_signed", -1.0)` (use the silence sentinel as the default; `0.0` is now a valid
     measured zero); `dimensions["dsi_metric"] = "vector_sum"` -> `"signed_antipodal"`. Switch the
     load source from `_load_cell_trace_jsonl` to a new `_load_cell_params_jsonl` reading
     `RESULTS_DIR / "cell_params.jsonl"`. Preserve the LEGIT threshold
     `dsi >= DSI_LEGIT_THRESHOLD = 0.5`; document in a comment that cells with `dsi_signed < 0` are
     now possible and excluded from the LEGIT cohort.

   * `post_run_analysis.py:135-148` — extend the DSI fallback chain to try `dsi_signed` first,
     then fall back to `dsi_best_legit`, `dsi_vector_sum`, `dsi`. `post_run_analysis.py:192` —
     widen the y-axis range from `(-0.05, 1.05)` to `(-1.05, 1.05)` and add a horizontal dashed line
     at `dsi_signed = 0` so the reversed-preference region is visually obvious. (REQ-8.)

   * `build_predictions_assets.py` and `build_results.py` — update all `dsi_vector_sum` references
     to `dsi_signed`; the predictions asset schema field becomes `dsi_signed` (Step 12).

   * `t0126_vs_t0129_comparator.py` — adapt to (a) read t0126's `pareto_front_seed8929.json`
     (read-only from the dependency task), (b) reproject each t0126 cell through the t0129
     `_signed_antipodal_dsi` helper using the cell's recorded per-direction spike counts (available
     in t0126's `all_evaluations_seed8929.json` or the predictions asset
     `files/predictions.jsonl.gz` from t0126), (c) compute the count of t0126-Pareto cells with
     `dsi_vector_sum > 0.5` but `dsi_signed < 0` (REQ-20), (d) render the
     `pareto_t0126_vs_t0129_overlay.png` chart with sign-flipped cells annotated in red (REQ-8).

   Expected output: `grep -rn "dsi_vector_sum" code/` returns matches only in
   `t0126_vs_t0129_comparator.py` (legitimately reads the historical field name from t0126's frozen
   predictions asset). Satisfies REQ-2, REQ-7 (driver wiring), REQ-20, REQ-8 (chart fallback +
   y-axis range).

### Milestone 2 — Smoke Gate and Validation (Step 8, local CPU)

8. **Run the t0126-inherited 9-check smoke gate on the local Bed B canonical anchor cell after the
   DSI rename.** Execute
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.smoke_gate`.
   The harness:
   * Runs checks 1, 7, 8 (NEURON + MOD library import + canonical anchor cell + signed DSI sanity
     range + F-axis sign convention with `dsi_signed`).
   * Runs checks 2, 3, 4, 5, 6 (synthetic DSI sanity `(5,1) -> 0.6667`, silence guard at
     `pd_spikes_sum < 3`, pool-restart cadence at every 10 gens, cost-watchdog wiring at
     `T0129_HARD_BUDGET_USD = 8.0`, HV-plateau absence in live `TerminationCollection`).
   * Runs check 9 (Carter-Bean ATP/AP/cm three-tier policy: PASS within `[1e8, 1e9]` band, WARN
     within `[1e6, 1e14]` outside the PASS band, FAIL outside `[1e6, 1e14]`).
   * Writes `logs/steps/<n>_implementation/smoke_gate.json` with all 9 check verdicts and the
     fixed-cell DSI fixture (REQ-23).

   **Validation gate (expensive operation, before NSGA-II launch)**:
   * **Trivial baseline**: the canonical Bed B anchor cell's per-AP AIS ATP cost must land within
     the first-principles canonical band `[1e8, 1e9] ATP/AP/cm` (geometric mean `~3e8 ATP/AP/cm`).
   * **`--limit` setting**: the smoke gate evaluates ONE canonical cell, so no `--limit` flag is
     needed (the cell evaluation itself is the limited validation run).
   * **Failure condition**: if check 9 reports `status: "failed"` (canonical-cell value outside
     `[1e6, 1e14]`), STOP and write an intervention file at `intervention/smoke_gate_failed.md`
     explaining the failure mode. **Do NOT proceed to NSGA-II launch on failure.** The most common
     failure for check 9 is a surface-area unit-conversion bug (would show ATP/AP at ~1e10x the
     canonical band); the second most common is missing compartments in the seg.ina record list.
   * **Individual-output inspection**: after the smoke gate runs, the implementation agent reads 5
     individual AP-window records from `smoke_gate.json` and verifies the per-compartment AIS ATP
     breakdown is non-zero with the expected ratios (AIS-distal > AIS-proximal > soma; dendrites
     varies). The agent also confirms that the signed DSI synthetic check (check 2) returns
     `0.6667 +/- 1e-6` for `(PD=5, ND=1)`.

   If any check FAILS, STOP. If check 9 WARNS but the measured value is in `[1e6, 1e14]`, proceed
   with the diagnostic logged. Satisfies REQ-6, REQ-19, REQ-23.

### Milestone 3 — Phase A Random Init and Phase B NSGA-II Run (Steps 9-10, local CPU, long-running)

9. **[CRITICAL] Launch the NSGA-II run via the `run_seed3517.sh` wrapper.** Per project memory
   `feedback_nsga2_launch_via_run_script`, NEVER invoke the driver directly — always launch via
   the shell wrapper so worker env inheritance and bootstrap initialisation are well-defined.
   Execute
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- bash tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/run_seed3517.sh`.
   The wrapper:

   * **Phase A**: builds the Latin-Hypercube random-init population of 96 cells seeded by
     `T0129_SEEDS[0] = 3517` via `python -u -m tasks.t0129_*.code.random_init`. After Phase A, the
     evaluator writes 96 rows to `results/cell_params.jsonl` (one per Phase-A cell, all with
     `gen = -1`). **Assertion gate**: after Phase A returns, confirm `cell_params.jsonl` exists, is
     non-empty, has `>= 96` lines, and each row has all required fields (REQ-4). If the file is
     missing or short, STOP and write `intervention/phase_a_cell_params_missing.md` — this is the
     env-var failure mode the task is designed to prevent and must not be silently ignored.
   * **Bootstrap**: imports `tasks.t0129_*.code.bootstrap` so the t0080 MOD library is compiled (on
     Linux) and loaded.
   * **Phase B**: launches
     `python -u -m tasks.t0129_*.code.nsga2_driver --seed 3517 --n-gen 60 --save-algorithm-config --teardown-on-watchdog`.
     The driver runs NSGA-II via pymoo with default SBX crossover (eta = 15), polynomial mutation
     (eta = 20), tournament selection of size 2. Pool-restart fires every 10 gens via
     `PerGenerationPoolRestart`. Per-gen dill checkpoints land in
     `logs/steps/<n>_implementation/checkpoints/`. Per-gen JSONL writes to
     `logs/steps/<n>_implementation/hv_trace.jsonl` with HV value plus per-cell DSI / ATP /
     silence_failed / firing rates. The `_GenerationCallback` writes
     `results/data/all_evaluations_seed3517.json` and per-gen `cell_params.jsonl` rows. Live
     `TerminationCollection` contains EXACTLY `MaximumGenerationTermination(n_max_gen=60)` +
     `CostWatchdogTermination($8 cap)`. **`OperatorStopTermination` is REMOVED** from the live
     collection (REQ-13); the run continues until gen 60 or the watchdog trips.

   **Validation gate (expensive operation, NSGA-II run)**:
   * **Trivial baseline**: t0126's Pareto front size at gen 60 (read from
     `tasks/t0126_*/results/data/pareto_front_seed8929.json`) sets the order-of-magnitude
     expectation. The t0129 final front should have `n >= 5` cells (a sanity floor; t0126 had
     `n >= 20` per its task description).
   * **Early-progress check (after gen 1)**: confirm the first generation completed without errors
     by inspecting `hv_trace.jsonl` — if all 96 cells trip the silence guard (`dsi_signed = -1.0`
     for every cell at gen 1), STOP and write `intervention/all_phase_a_silenced.md`. This is the
     same risk that the t0126 task description documents: "All Phase A cells trip the silence guard.
     Same risk as t0126 — fall back to wider random init bounds is not permitted (would break
     parameter-vector comparability with t0126). Document and stop."
   * **Failure condition**: if at gen 1 the median `dsi_signed` across the 96 cells is exactly
     `-1.0`, STOP. If `cell_params.jsonl` line count plateaus (no growth between consecutive gens),
     STOP — the per-cell sink has broken.
   * **Individual-output inspection**: after gen 5, the implementation agent reads 5 random rows
     from `cell_params.jsonl` and confirms (a) each row has all required fields, (b)
     `pd_rate_hz != 40.0` for every row (the t0126 placeholder symptom), (c)
     `dsi_signed in [-1.0, 1.0]`, (d) at least one row has `dsi_signed > 0` (the run is not stuck at
     silence).

   Expected output: the run terminates at gen 60 (or via watchdog) and writes
   `results/data/pareto_front_seed3517.json` plus `results/data/all_evaluations_seed3517.json`.
   `results/cell_params.jsonl` line count = `96 + 96 * gen_completed` (~5856 rows if 60 gens
   complete). Satisfies REQ-7, REQ-12, REQ-13, REQ-14, REQ-4 (Phase A + B sink writes).

10. **Extract and persist the final Pareto front.** After the driver returns (or after the watchdog
    trips), confirm `results/data/pareto_front_seed3517.json` exists with one entry per Pareto cell
    containing the 68-d vector, `dsi_signed`, `atp_per_spike_molecules`, `pd_rate_hz`, `nd_rate_hz`,
    per-compartment ATP breakdown, and diagnostic flags. Confirm
    `results/data/all_evaluations_seed3517.json` exists with every evaluated cell across all
    generations. Run
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.nsga2_driver --extract-final-pareto-only --seed 3517`
    (idempotent re-extraction from the last dill checkpoint if the run was watchdog-stopped).
    Expected output: the Pareto front JSON file exists and contains `n >= 5` cells (sanity floor).
    Satisfies REQ-7.

### Milestone 4 — Post-Run Analysis, Charts, Predictions and Answer Assets (Steps 11-14, local CPU)

11. **Run post-run analysis and produce the four required charts.** Execute the four chart-builder
    scripts via
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.post_run_analysis --seed 3517`
    plus
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.t0126_vs_t0129_comparator --seed 3517 --t0126-pareto tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json`.
    Outputs written to `results/images/`:

    * `pareto_front_dsi_signed_vs_atp.png` — Pareto front scatter, `dsi_signed` on y in range
      `(-1.05, 1.05)` with horizontal dashed line at `dsi_signed = 0`, `atp_per_spike_molecules` on
      x (log scale). Joint-pass region (`dsi_signed >= 0.5` AND `pd_rate_hz >= 30 Hz`) highlighted.
    * `dsi_signed_distribution.png` — histogram over every evaluated cell from
      `cell_params.jsonl`, x-axis `dsi_signed` in range `[-1, 1]`, y-axis count. Annotate the
      negative-DSI count and zero-crossing fraction.
    * `pd_vs_nd_rate_scatter.png` — scatter of `pd_rate_hz` vs `nd_rate_hz` coloured by
      `dsi_signed` (diverging colormap centred at 0), diagonal `pd_rate = nd_rate` line drawn.
    * `pareto_t0126_vs_t0129_overlay.png` — overlay of t0126's recorded Pareto front (reprojected
      through `_signed_antipodal_dsi` using each t0126 cell's recorded per-direction spike counts
      from `tasks/t0126_*/results/data/all_evaluations_seed8929.json`) and the t0129 final Pareto
      front. Cells whose t0126 `dsi_vector_sum > 0.5` but reprojected `dsi_signed < 0` are annotated
      in red. The comparator also computes the count of such sign-flipped cells (REQ-20) and writes
      it to a JSON sidecar `results/data/t0126_vs_t0129_sign_flip_count.json` for the metrics
      builder to pick up in Step 14.

    Expected output: four PNG files in `results/images/`, each `>= 50 KB` (sanity floor); the
    sidecar JSON exists with
    `{"t0126_pareto_cells_with_dsi_vector_sum_gt_0p5_and_dsi_signed_lt_0": <int>, "t0126_pareto_size": <int>}`.
    Satisfies REQ-8, REQ-20.

12. **Build the predictions asset.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.build_predictions_assets --seed 3517`.
    The script reads `results/data/pareto_front_seed3517.json` plus `cell_params.jsonl` and writes
    `assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/`:

    * `details.json`: `predictions_id = "nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129"`;
      `name = "NSGA-II Signed DSI vs ATP-per-Spike, Bed B + 14-d Morph, Seed 3517"`;
      `prediction_format = "jsonl.gz"`; `description_path = "description.md"`; per-cell schema
      `{generation, cell_index, vector_68d, dsi_signed, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, pd_rate_hz, nd_rate_hz, objective_F_minimised, silence_failed_bool, legit_bool}`;
      `created_by_task = "t0129_t0126_signed_dsi_real_rates_1seed"`;
      `metrics_at_creation = {best_dsi_signed, min_atp_per_spike, n_pareto_cells, n_generations_completed, n_cells_total, final_hypervolume, sign_flip_count_vs_t0126, stop_trigger}`.
    * `description.md`: explains the signed-DSI definition, the antipodal pair, the silence
      sentinel, the per-cell JSONL provenance, and the relationship to t0126's predictions asset.
    * `files/predictions.jsonl.gz`: gzipped JSONL with one row per Pareto cell.

    Expected output: the asset folder exists with all three components; the asset passes the
    predictions asset verificator (if present). Satisfies REQ-9.

13. **Build the answer asset.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.build_assets --kind answer --question "Does the signed-DSI re-evaluation of t0126's protocol change the Pareto structure, or is the vector-sum / signed distinction immaterial on the antipodal pair?"`
    (or write the asset manually following the answer asset specification). The script (or the
    manual write) creates `assets/answer/does-signed-dsi-change-t0126-pareto-structure/`:

    * `details.json`: `answer_id = "does-signed-dsi-change-t0126-pareto-structure"`; `question` =
      the exact question text; `short_answer_path = "short_answer.md"`;
      `full_answer_path = "full_answer.md"`; `answer_methods = ["code_experiment"]`;
      `created_by_task = "t0129_t0126_signed_dsi_real_rates_1seed"`.
    * `short_answer.md`: 2-5 sentences opening with "Yes" / "No" / "I don't know", citing the
      sign-flip count from Step 11 and the front-overlap fraction. NO inline citations in the
      `## Answer` section.
    * `full_answer.md`: explains the research process, summarises the evidence (predictions asset,
      `cell_params.jsonl` data, comparator chart, t0126's `pareto_front_seed8929.json`), states the
      conclusion, and lists limitations (single seed, antipodal protocol only). All inline citations
      in body sections; `## Sources` includes markdown reference link definitions for the cited
      paper IDs (none required for this task — the answer is grounded in own + t0126 data) and
      task IDs (`t0126`).

    Expected output: the asset folder exists with all required files; the asset passes the answer
    asset verificator. Satisfies REQ-10.

14. **Compute and write `results/metrics.json`.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.metrics_builder --seed 3517`.
    The script reads `results/data/pareto_front_seed3517.json`, `cell_params.jsonl`, and
    `results/data/t0126_vs_t0129_sign_flip_count.json`, and writes `results/metrics.json` using the
    explicit multi-variant format (per `arf/specifications/metrics_specification.md`). Three
    variants:

    * `t0129-seed3517-headline`:
      * `metrics`: `{"direction_selectivity_index": <max dsi_signed across Pareto front>}` (the only
        registered metric; reported with `dsi_metric: "signed_antipodal"` dimension).
      * `dimensions`:
        `{"dsi_metric": "signed_antipodal", "seed": 3517, "atp_per_spike_molecules_min": <min ATP across Pareto>, "pd_rate_hz_headline": <pd_rate_hz of the headline cell>, "nd_rate_hz_headline": <nd_rate_hz of the headline cell>}`.

    * `t0129-seed3517-pareto-median`:
      * `metrics`: `{"direction_selectivity_index": <median dsi_signed across Pareto>}`.
      * `dimensions`:
        `{"dsi_metric": "signed_antipodal", "seed": 3517, "atp_per_spike_molecules_pareto_median": <median ATP>, "pd_rate_hz_pareto_median": <median pd_rate_hz across Pareto>, "nd_rate_hz_pareto_median": <median nd_rate_hz>, "n_pareto_cells": <int>}`.

    * `t0129-vs-t0126-sign-flipped`:
      * `metrics`: `{"direction_selectivity_index": null}` (no headline scalar for this variant; the
        dimension is the count).
      * `dimensions`:
        `{"comparison": "t0126_vs_t0129", "sign_flip_count": <count of t0126-Pareto cells with dsi_vector_sum > 0.5 but dsi_signed < 0>, "t0126_pareto_size": <int>, "t0126_pareto_seed": 8929}`.

    Expected output: `results/metrics.json` exists; `jq '.variants | keys' results/metrics.json`
    returns the three variant names; each variant references only the registered key
    `direction_selectivity_index` in `metrics` (custom outputs in `dimensions`). Satisfies REQ-21,
    REQ-20.

* * *

## Remote Machines

**None required.** The NSGA-II run is local CPU only on the researcher's workstation. NEURON and
pymoo are CPU-bound; no GPU is needed. The orchestrator brief is explicit: "Local CPU only, no
remote machines, no setup-machines step (already marked skipped)." The Vast.ai cost-watchdog wiring
inherited from t0126 stays as defensive insurance (the `T0129_HARD_BUDGET_USD = 8.0` cap will never
trip on a local-CPU run because no paid services are called).

* * *

## Assets Needed

* **Input from t0126 (read-only)**:
  * `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json` —
    t0126's final Pareto front under vector-sum DSI; needed by `t0126_vs_t0129_comparator.py` (Step
    11\) for the overlay chart and the sign-flip count.
  * `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/all_evaluations_seed8929.json` (or
    the predictions asset `files/predictions.jsonl.gz`) — needed for the per-cell per-direction
    spike counts that the comparator reprojects through `_signed_antipodal_dsi`.
  * `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/*` — the source of every Python module
    the t0129 fork copies verbatim (Step 2).

* **Registered libraries (imported unchanged, via the t0126 fork's import paths)**:
  * `procedural_dsgc_morphology_generator` (task t0090) — provides `MorphologyParams` and
    `MorphologyResult` for the 14-d morphology block of the 68-d vector.
  * `dsgc_active_channel_pack` (task t0080) — 13-channel MOD library compiled at bootstrap.
  * `de_rosenroll_2026_dsgc` (task t0024) — DSGC NEURON port; `bootstrap.py` patches it for Linux.

* **External resources**: none. No external API calls, no dataset downloads, no remote files.

* * *

## Expected Assets

Matches `task.json` `expected_assets`:

* **1 predictions asset**:
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/`
  — Pareto front of cells under (`dsi_signed`, `atp_per_spike_molecules`) with full 68-d parameter
  vectors plus per-direction firing rates. Mirrors t0126's predictions asset format with the
  `dsi_vector_sum -> dsi_signed` rename and the added `nd_rate_hz` field.

* **1 answer asset**:
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/answer/does-signed-dsi-change-t0126-pareto-structure/`
  — one-pager answering "Does the signed-DSI re-evaluation of t0126's protocol change the Pareto
  structure, or is the vector-sum / signed distinction immaterial on the antipodal pair?" with
  supporting numbers (sign-flip count, Pareto-front overlap fraction, signed-DSI Pareto-median).

* * *

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already complete: research_code.md only) | 0h (done) |
| Planning (this document) | 0h (done) |
| Milestone 1: code fork + targeted edits (Steps 1-7) | 1-2h |
| Milestone 2: smoke gate (Step 8) | 5-15 min (one canonical cell on local CPU) |
| Milestone 3: Phase A random init + Phase B 60-gen NSGA-II (Steps 9-10) | 8-12h (matches t0126's single-seed envelope; per orchestrator brief: "t0126 ran 1 seed × 60 gen in ~9h on local CPU") |
| Milestone 4: post-run analysis, charts, predictions + answer assets, metrics.json (Steps 11-14) | 1-2h |
| **Total wall-clock (implementation only)** | **10-16h** (single-seed run dominates) |
| **Hard ceiling** | **24h** (defensive cap; if exceeded, intervention file) |

* * *

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Smoke gate fails after DSI helper rename | Low | Blocking | Diff `evaluator.py` against t0126 line-by-line; only the three behavioural changes (signed DSI helper, `dsi_signed` rename + `nd_rate_hz` field, `_append_cell_params` replacement) should differ. Re-run the unit test set (Step 6) to localise the regression. If a numerical mismatch in check 2 appears, recompute by hand: `(5-1)/(5+1) = 0.6667` is the expected value. |
| All Phase A cells trip the silence guard (`dsi_signed = -1.0` for all 96 cells) | Low (inherited from t0126; t0126 did not see this) | Blocking | Same risk as t0126 — fall back to wider random init bounds is NOT permitted (would break parameter-vector comparability with t0126). Document and stop via `intervention/all_phase_a_silenced.md`. |
| `cell_params.jsonl` not written or written with placeholder rates (`pd_rate_hz = 40` symptom) | Medium (this is the exact t0126 failure mode the task is designed to fix) | Blocking (defeats task purpose) | Two-layer mitigation: (a) the cell_params path is captured via `BedBV3MorphProblem.__init__(cell_params_path=...)` so it pickles into workers — no env-var dependency that can drop silently; (b) Step 9's assertion gate checks after Phase A that the file exists, is non-empty, has `>= 96` rows, and no row has `pd_rate_hz == 40.0` exactly. If the gate fires, STOP via `intervention/phase_a_cell_params_missing.md` — do not synthesise rates after the run. |
| Direct driver invocation drops the bootstrap or worker env | Low (task description forbids it) | Loss of cell_params, run silently broken | The implementation agent MUST launch via `bash code/run_seed3517.sh`. Per memory `feedback_nsga2_launch_via_run_script`, direct invocation under tmux loses bootstrap and worker env propagation. The wrapper sources bootstrap and sets up the worker pool before launching the driver. |
| NSGA-II run exceeds the 24h wall-clock ceiling | Low (t0126 ran in ~9h) | Delay | The `--teardown-on-watchdog` flag plus `CostWatchdogTermination($8 cap)` provide a defensive stop. For wall-clock overrun specifically, the operator may signal a manual stop after gen 60 reaches a sane convergence (HV trajectory plateau visible in `hv_trace.jsonl`); per memory `feedback_disable_hv_plateau_autostop`, automatic HV-plateau stopping is DISABLED. |
| Reading t0127 or t0128 by mistake (e.g., aggregator returns them in a generic query) | Low | Scope creep, may pollute analysis with synthesised data | The task description forbids it explicitly. All cross-task lookups use `--ids t0126_bedb_dsi_atp_per_spike_nsga2_60gen` filter. A final grep `grep -rn "t0127\|t0128\|t0127_\|t0128_" tasks/t0129_t0126_signed_dsi_real_rates_1seed/` must return ZERO matches before task completion. |
| The t0126-Pareto reprojection in the comparator needs per-direction spike counts that t0126 did not persist | Medium (t0126's predictions asset schema may not include raw spike counts) | Comparator chart degraded to magnitude-only overlay; sign-flip metric unavailable | Fallback: if t0126's `all_evaluations_seed8929.json` and predictions asset do not contain per-cell per-direction spike counts, compute the reprojection from `dsi_vector_sum` and `pd_rate_hz` + `nd_rate_hz` (the t0126 task description claims these are recorded). If even `nd_rate_hz` is missing or known-synthetic (per memory `project_t0126_cell_trace_synthesised`, `pd_rate_hz = 40` was placeholder — so `nd_rate_hz` is likely also unreliable), document the limitation in the answer asset and report only the count of t0126-Pareto cells with `dsi_vector_sum > 0.5` AND `pd_rate_hz` not equal to the placeholder `40.0`. Worst case: omit the cross-comparison metric and note the limitation in `full_answer.md`. |

* * *

## Verification Criteria

Each criterion includes the exact command to run and the expected observable output:

* **Unit tests pass (REQ-1, REQ-22)**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run pytest tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/test_evaluator_dsi_signed.py -v`.
  Expected: 9 tests pass, 0 failures. The four new acceptance-criteria tests
  (`test_signed_dsi_negative_when_nd_dominates`, `test_signed_dsi_zero_when_pd_equals_nd`, the
  silence sentinel test asserting `dsi_signed == -1.0`, and the positive-case test asserting
  `(5,1) -> 0.6667`) are all in the passing set.

* **Smoke gate passes (REQ-6, REQ-19, REQ-23)**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.smoke_gate`.
  Expected: `logs/steps/<n>_implementation/smoke_gate.json` exists with all 9 checks reporting
  `status: "passed"` (or check 9 reporting `"warning"` with the canonical-cell value in
  `[1e6, 1e14]`); the signed DSI synthetic check (check 2) returns `0.6667 +/- 1e-6` for
  `(PD=5, ND=1)`.

* **cell_params.jsonl populated with real rates (REQ-4)**: After Phase A, run
  `wc -l tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/cell_params.jsonl` and confirm
  `>= 96` lines. Run
  `python -c "import json; rows = [json.loads(l) for l in open('tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/cell_params.jsonl')]; assert all( abs(r['pd_rate_hz'] - 40.0) > 1e-9 or r['silence_failed'] for r in rows[:5] ), 'placeholder rate detected'"`
  — exits 0 if the t0126 placeholder symptom is absent (rates are real, not all 40.0).

* **NSGA-II run completes with expected outputs (REQ-7)**: After the run, confirm
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/data/pareto_front_seed3517.json` exists and
  has `>= 5` Pareto cells via
  `python -c "import json; d = json.load(open('tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/data/pareto_front_seed3517.json')); assert len(d['pareto']) >= 5"`.
  Confirm `logs/steps/<n>_implementation/hv_trace.jsonl` exists with at least one HV value per
  completed generation.

* **All four required charts exist (REQ-8)**: Run
  `ls -la tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/images/` and confirm all four files
  exist with file size `>= 50 KB`: `pareto_front_dsi_signed_vs_atp.png`,
  `dsi_signed_distribution.png`, `pd_vs_nd_rate_scatter.png`, `pareto_t0126_vs_t0129_overlay.png`.

* **Predictions and answer assets pass their verificators (REQ-9, REQ-10)**: Run
  `uv run python -u -m arf.scripts.verificators.verify_predictions_asset tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/`
  (if the verificator exists; otherwise spot-check the asset against
  `meta/asset_types/predictions/specification.md`). Run
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/answer/does-signed-dsi-change-t0126-pareto-structure/`.
  Expected: both verificators report zero errors.

* **metrics.json registers only `direction_selectivity_index` and uses multi-variant format
  (REQ-21)**: Run
  `python -c "import json; m = json.load(open('tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/metrics.json')); v = m['variants']; keys = set(); [keys.update(var['metrics'].keys()) for var in v.values()]; assert keys == {'direction_selectivity_index'}; assert set(v.keys()) == {'t0129-seed3517-headline', 't0129-seed3517-pareto-median', 't0129-vs-t0126-sign-flipped'}"`
  — exits 0 if both conditions hold.

* **No t0127 or t0128 references (REQ-11)**: Run
  `grep -rn "t0127\|t0128\|t0127_\|t0128_" tasks/t0129_t0126_signed_dsi_real_rates_1seed/` and
  confirm ZERO matches. (Permissible exception: this plan document mentions them only to declare
  them out of scope; the grep can be restricted to `code/`, `assets/`, and `results/` to focus on
  production artefacts.)

* **Hard invariants preserved (REQ-12, REQ-13, REQ-14)**: Run
  `grep -n "_POOL_RESTART_EVERY\|HV_PLATEAU_AUTO_STOP\|POP_SIZE\|N_EVAL_SEEDS\|N_DIRECTIONS\|N_GEN\|SILENCE_PD_SPIKES_THRESHOLD\|WORST_CASE_DSI\|TSTOP_MS" tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/constants.py tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/constants_morphology.py tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/constants_electrophys.py`
  and confirm: `_POOL_RESTART_EVERY: int = 10`, `HV_PLATEAU_AUTO_STOP: bool = False`,
  `POP_SIZE: int = 96`, `N_EVAL_SEEDS: int = 3`, `N_DIRECTIONS: int = 2`, `N_GEN: int = 60`,
  `SILENCE_PD_SPIKES_THRESHOLD: int = 3`, `WORST_CASE_DSI: float = -1.0`, `TSTOP_MS = 1400`.

* **Plan verificator passes (overall)**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0129_t0126_signed_dsi_real_rates_1seed -- uv run python -u -m arf.scripts.verificators.verify_plan t0129_t0126_signed_dsi_real_rates_1seed`.
  Expected: zero errors, warnings (if any) noted in the implementation log.

* * *

## Notes on Out-of-Scope Items

* **MI / Carter-Bean per-spike diagnostics**: Out of scope. The orchestrator brief explicitly drops
  `cell_trace.jsonl`. The per-spike timing information needed to compute MI and per-AP Carter-Bean
  breakdown is therefore not recorded in this task. The smoke gate's check 9 (Carter-Bean canonical
  cell ATP/AP/cm) still runs as a sanity check; it does NOT require per-spike recording for every
  NSGA-II cell.

* **Multi-seed extension**: Out of scope. One fresh seed (3517) per orchestrator brief and task
  description. A follow-up task can extend to multiple seeds if the single-seed result shows
  interesting sign-flip behaviour.

* **Reading t0127 / t0128**: Out of scope per task description and orchestrator brief. The only
  parent task is t0126.

* **Full angular tuning curve (12-direction sweep)**: Out of scope. The protocol is the antipodal
  pair `[0 deg, 180 deg]` only, inherited verbatim from t0126.
