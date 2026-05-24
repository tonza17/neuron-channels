---
spec_version: "2"
task_id: "t0122_dsi_cytoplasm_volume_nsga2"
date_completed: "2026-05-24"
status: "complete"
---
# Plan: NSGA-II Maximising DSI and Minimising Cytoplasm Volume (Bed B + 14-d Morph)

## Objective

Fork the t0115 single-seed 68-d Bed B + 14-d morphology NSGA-II substrate and replace the PD-rate
objective with a **cytoplasm-volume** cost objective, computed geometrically from the
`MorphologyResult` `h.Section` handles as
`vol_um3 = sum(pi * (sec.diam / 2.0)**2 * sec.L for sec in [soma, *all_dends, ais_proximal, ais_distal])`.
The 2-objective NSGA-II now optimises `(maximise DSI, minimise cytoplasm_volume_um3)`. PD-rate is
retained as a tracked diagnostic on `CellEvalResult` and in predictions assets but does NOT enter
`out["F"]`. Run on a single Vast.ai EPYC instance with one GA seed drawn via
`secrets.randbelow(10000)`, `POP_SIZE=96`, `N_EVAL_SEEDS=3`, `_POOL_RESTART_EVERY=10`,
`HV_PLATEAU_AUTO_STOP=False`, `N_GEN_MAX=60`, and a `COST_CAP_USD=6.0` (reduced from the
project-default $8 because the Vast.ai account balance is $7 and a $1 teardown buffer is required).

**Done** means: (1) the run terminates cleanly via one of operator-stop, $6 budget watchdog, or the
60-gen ceiling; (2) one predictions asset `nsga2-cytoplasm-volume-bedb-morph` is written with
per-cell 68-d vectors, per-objective `F`, per-direction firing, and `cytoplasm_volume_um3`; (3) one
answer asset `cuntz-balancing-factor-prediction-check` is written answering "Does NSGA-II with a
cytoplasm-volume cost objective produce a high-DSI front in Cuntz 2010's predicted balancing-factor
`[0.2, 0.7]` band?"; (4) `results/metrics.json` registers `direction_selectivity_index` with
variants `best_legit`, `overall_max`, `dsi_eq_one_count` plus a new cytoplasm-volume-axis metric
set; (5) the four required charts and Pareto/all-evaluations JSON dumps are saved.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0122_dsi_cytoplasm_volume_nsga2/task.json` and the resolved long
description at `tasks/t0122_dsi_cytoplasm_volume_nsga2/task_description.md`:

```text
Name: NSGA-II maximising DSI and minimising cytoplasm volume (Bed B + 14-d morph)

Short description: 68-d NSGA-II on Bed B + 14-d morphology, 2-objective DSI vs cytoplasm
volume (Cuntz 2010 wiring cost). Gated on t0120 geometry audit passing. 1 GA seed,
pop=96, N_EVAL_SEEDS=3, $8 cap. (Cap REDUCED to $6 per task_description.md Hard
Constraints because the Vast.ai account balance is $7.)

Dependencies: t0024, t0080, t0090, t0092, t0106, t0115, t0119, t0120.
Expected assets: 1 predictions, 1 answer.
Task types: experiment-run, data-analysis, answer-question.
Source suggestion: S-0097-01.

Hard Constraints (non-negotiable, reproduced in code/constants.py):
* _POOL_RESTART_EVERY = 10  (10-gen rule; NEVER cadence 25 or any other value)
* HV_PLATEAU_AUTO_STOP = False  (disabled per project policy)
* POP_SIZE = 96
* N_EVAL_SEEDS = 3
* N_GEN_MAX = 60
* COST_CAP_USD = 6.0

Approach:
1. Copy t0115 substrate end-to-end (68-d vector, pop=96, N_EVAL_SEEDS=3,
   2 antipodal directions PD=0deg/ND=180deg, ratio DSI).
2. Replace PD-rate objective with cytoplasm volume; PD-rate stays as tracked diagnostic.
3. GA seed via secrets.randbelow(10000); avoid round-ish numbers.
4. Gen ceiling 60. Stop trigger: operator stop, $6 cost cap, or gen 60 ceiling.
5. Vast.ai EPYC 32-core or 64-core single instance.
6. Silence guard TIGHTENED from "total_mean_spikes < 10" to "pd_spikes_sum < 3".
7. Post-run: Pareto front, joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz),
   per-cell morphology gallery, Cuntz 2010 balancing-factor check on top-10 cells.
8. Answer asset: "Does NSGA-II with cytoplasm-volume cost produce a high-DSI front
   in Cuntz 2010's [0.2, 0.7] bf band?"

Expected outputs (from task_description.md):
* assets/predictions/nsga2-cytoplasm-volume-bedb-morph/
* assets/answer/cuntz-balancing-factor-prediction-check/
* results/data/pareto_front_seed*.json
* results/data/all_evaluations_seed*.json
* results/images/pareto_front_dsi_vs_volume.png
* results/images/top50_morphologies_seed*.png  (full dendrite trees, not soma-only)
* results/images/cuntz_balancing_factor_top10.png

Verification Criteria (from task_description.md):
* t0120 verdict is "rendering-only / no re-runs needed" before this task starts.
* Predictions asset passes verify_predictions_asset.
* metrics.json registers direction_selectivity_index with explicit variants
  best_legit, overall_max, dsi_eq_one_count.
* Cytoplasm volume formula is documented in results_detailed.md with
  per-section breakdown.
* Cuntz 2010 balancing-factor test result reported as
  "consistent with [0.2, 0.7] band" or "violates band".
* compare_literature.md includes a row comparing top-cell bf distribution
  to Cuntz 2010.
```

Decomposed requirements (each step in `## Step by Step` cites the `REQ-*` items it satisfies):

* **REQ-1** — Confirm `t0120_morph_generator_geometry_audit` verdict is "rendering-only / no
  re-runs needed" before any other implementation work. Satisfied by Step 1. Evidence: a
  `gating check` log entry in Step 1 captures the verdict string copied from
  `tasks/t0120_morph_generator_geometry_audit/results/results_summary.md`.

* **REQ-2** — Fork `tasks/t0115_seed9354_no_autostop/code/` verbatim into
  `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` and rewrite import paths. Satisfied by Step 2.
  Evidence: `ls tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` shows ~25 forked Python files plus the
  three new modules.

* **REQ-3** — Hard constant `_POOL_RESTART_EVERY = 10` is set in `code/constants.py` (the
  project's 10-gen rule per memory `feedback_nsga2_pool_restart_every_10.md`). Satisfied by Step 3.
  Evidence: `grep -n "_POOL_RESTART_EVERY" code/constants.py` returns the line
  `_POOL_RESTART_EVERY: int = 10`.

* **REQ-4** — Hard constant `HV_PLATEAU_AUTO_STOP = False` is set in `code/constants.py` and the
  `HVPlateauTermination` is NOT added to the live `TerminationCollection` in `code/nsga2_driver.py`.
  Satisfied by Steps 3 and 4. Evidence:
  `grep -n "HV_PLATEAU_AUTO_STOP\|HVPlateauTermination" code/constants.py code/nsga2_driver.py`
  shows `HV_PLATEAU_AUTO_STOP: bool = False` and the driver's `TerminationCollection` contains only
  `{MaximumGenerationTermination, CostWatchdogTermination, OperatorStopTermination}`.

* **REQ-5** — Hard constant `POP_SIZE = 96` is set in `code/constants.py`. Satisfied by Step 3.
  Evidence: `grep -n "POP_SIZE" code/constants.py` returns `POP_SIZE: int = 96`.

* **REQ-6** — Hard constant `N_EVAL_SEEDS = 3` is set in `code/constants.py`. Satisfied by Step 3.
  Evidence: `grep -n "N_EVAL_SEEDS" code/constants.py` returns `N_EVAL_SEEDS: int = 3`.

* **REQ-7** — Hard constant `N_GEN_MAX = 60` is set in `code/constants.py` (was 300 in t0115).
  Satisfied by Step 3. Evidence: `grep -n "N_GEN_MAX\|N_GEN " code/constants.py` shows
  `N_GEN_MAX: int = 60` (or `N_GEN: int = 60`).

* **REQ-8** — Hard constant `COST_CAP_USD = 6.0` is set in `code/constants.py` and the
  `CostWatchdogTermination` is wired with that cap at the driver call site. Satisfied by Steps 3 and
  4\. Evidence: `grep -n "COST_CAP_USD\|T0122_HARD_BUDGET_USD" code/constants.py` returns
  `COST_CAP_USD: float = 6.0` (alias `T0122_HARD_BUDGET_USD = 6.0` for back-compat with the
  `CostWatchdogTermination` dataclass).

* **REQ-9** — Implement `compute_cytoplasm_volume_um3(*, cell: MorphologyResult) -> float` in a
  new `code/cytoplasm_volume.py` module summing `pi * (sec.diam / 2)**2 * sec.L` over
  `[soma, *all_dends, ais_proximal, ais_distal]`. Also implement
  `compute_per_section_volume_breakdown(*, cell) -> dict[str, float]` returning
  `{soma_um3, dendrites_um3, ais_um3}`. Satisfied by Step 5.

* **REQ-10** — Edit `code/evaluator.py` so that `CellEvalResult` gains a
  `cytoplasm_volume_um3: float` field, `BedBV3MorphProblem._evaluate` emits
  `out["F"] = [-dsi, +volume_um3]` (volume NOT negated because it is minimised), and PD-rate stays
  computed and stored on `CellEvalResult`. Satisfied by Step 6.

* **REQ-11** — Tighten the silence guard from "total_mean_spikes < 10" to "pd_spikes_sum < 3"
  inside `_summarise_trials` of `code/evaluator.py`. Update `code/test_evaluator_dsi_guard.py` to
  expect the new threshold. Satisfied by Step 6.

* **REQ-12** — In `code/constants_morphology.py`: set `N_GEN = 60`, add `HV_UTOPIA_VOLUME_UM3`
  constant, change `REF_POINT_HV` to a 2-entry `(0.0, V_max_um3)` pair to match the new F-sign
  convention. Satisfied by Step 3.

* **REQ-13** — GA seed `T0122_SEED` drawn via `secrets.randbelow(10000)` (per the t0113
  convention), avoiding round-ish numbers like 1000/5000/9000. Satisfied by Step 3. Evidence: the
  chosen seed is logged and committed into `code/constants.py` as `T0122_SEEDS = (X,)`.

* **REQ-14** — Provision a Vast.ai EPYC 32-core or 64-core single instance (whichever is cheapest
  at provisioning time) using the orchestrator's `/setup-remote-machine` skill. The orchestrator
  step `008_setup-machines` populates `logs/steps/008_setup-machines/machine_log.json` with the
  selected offer and hourly rate. Satisfied by Step 7.

* **REQ-15** — Compile the t0080 NEURON MOD library on the remote machine via `nrnivmodl` over
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`. Resolved by
  `tasks.t0115_seed9354_no_autostop.code.paths.resolve_t99_mod_library` pattern reused in
  `code/paths.py`. Satisfied by Step 8 (smoke gate).

* **REQ-16** — Smoke gate (`code/smoke_gate.py`) runs the t0115 6-check suite plus one new check
  verifying that `compute_cytoplasm_volume_um3` returns a positive float on a t0091-style anchor
  cell. Satisfied by Step 8.

* **REQ-17** — NSGA-II run executes via `code/nsga2_driver.py run_nsga2_for_seed(task_seed=...)`
  with the operator-stop / cost-watchdog / 60-gen termination triple. Per-gen dill checkpoints land
  in `logs/steps/009_implementation/checkpoints/`, per-gen JSONL writes to `hv_trace.jsonl`, and
  pool restarts fire every 10 generations. Satisfied by Step 9.

* **REQ-18** — Watchdog enforces the `$6.0` total task cap and a `$5.0` per-instance watchdog cap
  (leaves $1 below the task cap for teardown / unexpected costs). Satisfied by Step 4 (wiring) and
  Step 9 (live enforcement).

* **REQ-19** — Write `results/data/pareto_front_seed<S>.json` and
  `results/data/all_evaluations_seed<S>.json` from the per-gen JSONL trace and the final population.
  Satisfied by Step 10.

* **REQ-20** — Produce `results/images/pareto_front_dsi_vs_volume.png` (the headline Pareto chart)
  and `results/images/top50_morphologies_seed<S>.png` (full dendrite trees per memory
  `feedback_top50_morphologies_full_dendrites.md`, NOT soma-only). Satisfied by Steps 11 and 12.

* **REQ-21** — Implement `compute_balancing_factor(*, cell: MorphologyResult) -> float` in a new
  `code/cuntz_balancing_factor.py` module implementing Cuntz 2010's bf formula
  (`bf = total_wiring_length_um / (total_wiring_length_um + sum_of_path_distances_to_soma_um)`). Run
  it on the top-10 cells (ranked by DSI) and produce
  `results/images/cuntz_balancing_factor_top10.png` with the `[0.2, 0.7]` band overlay. Satisfied by
  Steps 5 and 12.

* **REQ-22** — Write `results/metrics.json` using the explicit multi-variant format. Include the
  registered metric `direction_selectivity_index` with three variants: `best_legit`, `overall_max`,
  `dsi_eq_one_count`. Add a parallel variant set for `cytoplasm_volume_um3` with sub-variants
  `min_legit`, `mean_top10`, `cuntz_bf_in_band_count`. Satisfied by Step 13.

* **REQ-23** — Build the predictions asset `assets/predictions/nsga2-cytoplasm-volume-bedb-morph/`
  with `details.json` (`spec_version: "2"`, `prediction_format: "jsonl.gz"`, per-cell 68-d vector +
  objective F + per-direction firing + cytoplasm volume), `description.md`, and
  `files/predictions.jsonl.gz`. Asset must pass `meta.asset_types.predictions.verificator`.
  Satisfied by Step 14.

* **REQ-24** — Build the answer asset `assets/answer/cuntz-balancing-factor-prediction-check/`
  with `details.json`, short answer, and full answer documents per
  `meta/asset_types/answer/specification.md`. The short answer must begin with "Yes" / "No" / "I
  don't know" and answer "Does NSGA-II with a cytoplasm-volume cost objective produce a high-DSI
  front in Cuntz 2010's predicted balancing-factor `[0.2, 0.7]` band?" using the top-10 bf
  distribution from REQ-21 as the primary evidence. Satisfied by Step 15.

* * *

## Approach

The work is a minimum-change fork of `t0115_seed9354_no_autostop` with three behavioural deltas and
one new geometric quantity:

1. **Forks the t0115 substrate end-to-end.** Per the research code review (`research_code.md`
   "Fork-the-most-recent NSGA-II driver, do not redesign"), `tasks/t0115_seed9354_no_autostop/code/`
   is the canonical fork point: `nsga2_driver.py` (763 lines), `evaluator.py` (504 lines),
   `trial_helpers.py`, `apply_params.py`, `generator_wrapper.py`, `build_top50_morphologies.py`, and
   the constants modules. Every file is copied verbatim, then import paths are rewritten
   `tasks.t0115_seed9354_no_autostop.code.* -> tasks.t0122_dsi_cytoplasm_volume_nsga2.code.*` and
   only the deltas below are applied. The 10-gen pool-restart cadence, the LHS-only init (96 rows x
   68 dims drawn via pymoo `LatinHypercubeSampling`), the `OperatorStopTermination` polling
   `intervention/stop.md`, the `CostWatchdogTermination` reading the Vast.ai
   `selected_offer.price_per_hour` from `logs/steps/008_setup-machines/machine_log.json`, the
   per-gen dill checkpoints, and the `hv_trace.jsonl` writer all transfer verbatim. This is the
   operator-endorsed "10th gen rule" lineage.

2. **Replaces the PD-rate objective with cytoplasm volume.** From research_code.md "Cytoplasm volume
   must be computed from the realised h.Section geometry": the `MorphologyResult`
   (`tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` lines 131-156)
   exposes `soma`, `all_dends`, `ais_proximal`, `ais_distal` `h.Section` handles. Each section
   exposes `sec.L` (length um) and `sec.diam` (diameter um). The formula

   ```python
   vol_um3 = sum(
       math.pi * (sec.diam / 2.0) ** 2 * sec.L
       for sec in [cell.soma, *cell.all_dends, cell.ais_proximal, cell.ais_distal]
   )
   ```

   is computable from these handles without a NEURON simulation step. The t0092 z-axis soma patch
   (`_patch_soma_geometry` line 61 of `morphology_generator_fix.py`) means
   `sec.L_soma == params.soma_diameter_um` and
   `sec.diam_soma == BEDB_AREA_TARGET_UM2 / (pi * soma_diameter_um)`, so the volume integral is
   correct against the patched geometry. The `BedBV3MorphProblem._evaluate` is edited to emit
   `out["F"] = [-dsi, +volume_um3]` (volume is positive and minimised so it is NOT negated; DSI is
   maximised so it stays negated). PD-rate is computed and stored on `CellEvalResult` (as a tracked
   diagnostic for predictions assets and joint-pass filtering) but does NOT enter the F vector.

3. **Tightens the silence guard.** From research_code.md "The silence-guard threshold = 3 PD spikes
   must be tightened from t0115's implicit ~10 mean": the t0115 evaluator at line 109 of
   `evaluator.py` uses `SILENCE_SPIKE_COUNT_THRESHOLD: int = 10` on the TOTAL mean spike count
   across 16 directions. This task uses `>= 3 PD spikes` instead — a single-line change inside
   `_summarise_trials` (line 298 of `evaluator.py`). This is critical because cytoplasm-volume
   minimisation pushes the optimiser toward tiny cells with low total spike counts, exactly the
   silence-corner regime where the original DSI = 1.0 artefact appeared.

4. **Three new modules from scratch.**

   * `code/cytoplasm_volume.py` (~30 lines): `compute_cytoplasm_volume_um3` and
     `compute_per_section_volume_breakdown`.

   * `code/cuntz_balancing_factor.py` (~50 lines): Cuntz 2010 wiring-cost `bf` formula. From
     research_code.md "Cytoplasm volume should be an evaluator-level objective, not a Problem-level
     constraint",
     `bf = total_wiring_length_um / (total_wiring_length_um + sum_of_path_distances_to_soma_um)`.
     Used only in post-processing on the top-10 cells.

   * `code/build_pareto_plots.py`: produces `pareto_front_dsi_vs_volume.png` (the headline Pareto
     chart) and `cuntz_balancing_factor_top10.png` (bf distribution with the `[0.2, 0.7]` band
     overlay). Reuses matplotlib + `LineCollection` patterns from `build_top50_morphologies.py`.

5. **Single GA seed.** From task description and research_code.md "Random-init only (no anchor
   warm-start)": draw via `secrets.randbelow(10000)` (avoid round-ish numbers like 1000, 5000, 9000)
   per the t0113 convention. NO anchor warm-start. The `n_var=68` problem uses `xl=LOWER_BOUNDS_68`
   and `xu=UPPER_BOUNDS_68` from `constants_morphology.py`.

6. **NEURON MOD library is shared with t0080.** From research_code.md "NEURON DLL is shared with
   t0080 across the lineage": `ensure_t80_dll_loaded` from
   `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params` is the process-singleton
   loader. There is NO need to recompile a t0122-specific nrnmech library. The Vast.ai bootstrap
   step compiles `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` with `nrnivmodl` into
   `x86_64/.libs/libnrnmech.so`.

**Recommended task types** (matches `task.json` `task_types`):

* **`experiment-run`** — running NSGA-II on a substrate is an experiment producing a predictions
  asset; the type's planning guidelines emphasise hypothesis definition, independent/dependent
  variables, baseline comparison, and cost cap. Hypothesis: "adding a cytoplasm-volume cost
  objective produces a Pareto front whose top-10 cells fall within the Cuntz 2010 `[0.2, 0.7]`
  band". Independent variable: the new objective. Dependent variables: DSI, cytoplasm_volume_um3,
  Cuntz bf. Baseline: t0121's 5-seed substrate-rate canonical report (2.58% +- SE 1.50% LEGIT
  yield).

* **`data-analysis`** — the post-run Pareto front, joint-pass analysis, top-10 bf computation, and
  chart generation are data analysis. Planning guidelines require per-subset breakdowns, matplotlib
  charts in `results/images/`, and structured metrics in `results/metrics.json` keyed only by
  registered metrics.

* **`answer-question`** — the task produces one answer asset answering the Cuntz prediction
  question. Planning guidelines require: define the stable question text, plan one answer asset per
  question, name evidence channels (top-10 bf distribution from the run), and define what counts as
  insufficient evidence (here: fewer than 10 LEGIT cells in the final population — in which case
  the answer says "Insufficient evidence" and reports the partial result).

**Alternatives considered (and rejected)**:

* **Alternative A — write `cytoplasm_volume_um3` as a Problem-level constraint instead of an
  objective.** Rejected because the task description and research_code.md "Cytoplasm volume should
  be an evaluator-level objective" both call for the second F-axis. A constraint would degrade to a
  hard infeasibility cliff and lose the Pareto-front trade-off information that the Cuntz prediction
  needs.

* **Alternative B — re-design the silence guard from scratch (e.g., per-direction floor on null
  rate).** Rejected because the one-line "pd_spikes_sum < 3" change is the minimum-risk patch
  consistent with the task description, and the t0102 / t0115 lineage has empirically validated the
  silence-guard pattern. A wholesale re-design would be out of scope.

* **Alternative C — run 3-5 GA seeds for cross-seed robustness (t0106 / t0121 lineage pattern).**
  Rejected because the task description explicitly mandates 1 GA seed and the $6 cap. The 5-seed
  cross-validation will be deferred to a follow-up suggestion if this single-seed run shows a
  promising Pareto front.

* **Alternative D — patch `_apply_asymmetry` in the morphology generator before this run.**
  Rejected because the gating dependency `t0120_morph_generator_geometry_audit` returned verdict
  "rendering-only / no re-runs needed" (60/60 coordinate-consistency checks pass). Patching would be
  out of scope and would invalidate the t0091-t0118 lineage.

* * *

## Cost Estimation

| Item | Estimated Cost | Notes |
| --- | --- | --- |
| Vast.ai EPYC 32-core or 64-core instance | $1.00 - $3.00 | At $0.15-0.40/hr for 6-12 hours of compute. |
| Per-instance teardown / unexpected charges | $0.10 - $0.50 | Buffer (kept under $1). |
| API calls (LLM inference) | $0.00 | None required. |
| **Estimated total actual cost** | **$1.10 - $3.50** | Within the $6 cap. |
| **Hard cap (COST_CAP_USD)** | **$6.00** | Watchdog stops the run if exceeded. |
| **Per-instance watchdog cap (T0122_PER_INSTANCE_WATCHDOG_USD)** | **$5.00** | Leaves $1 buffer below the task cap. |

Comparison with project budget (`project/budget.json`: total $100, per-task default $8, currently
$37.10 remaining): the $6 cap is below both the per-task default and the remaining project budget.
The reduced cap is dictated by the user's $7 Vast.ai account balance, not by the ARF budget. Prior
lineage spend: t0113=$0.48, t0114=$1.13, t0115=$2.50. All three came in well under their original
caps, supporting the $1-3 expected actual band.

* * *

## Step by Step

### Milestone 1 — Setup and Code Fork (Steps 1-6, local CPU)

1. **[CRITICAL] Confirm gating dependency.** Run
   `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.aggregators.aggregate_tasks --format json --detail full --ids t0120_morph_generator_geometry_audit`
   and read the `results_summary` field on the returned task object. Confirm the verdict string
   contains "rendering-only" and "t0122_dsi_cytoplasm_volume_nsga2 is unblocked". If the verdict
   says anything else (e.g., "real geometry bug"), STOP, do NOT proceed, and write an intervention
   file at `tasks/t0122_dsi_cytoplasm_volume_nsga2/intervention/gating_failed.md` listing the actual
   verdict and asking the operator how to proceed. Expected output: a log line "[gating] t0120
   verdict: rendering-only / no re-runs needed -> unblocked". Satisfies REQ-1.

2. **Fork the t0115 code directory.** Copy every file in `tasks/t0115_seed9354_no_autostop/code/` to
   `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/`. Then run a global string substitution
   `t0115_seed9354_no_autostop -> t0122_dsi_cytoplasm_volume_nsga2` across all `.py` and `.sh`
   files. Expected output: `ls code/` shows the same ~25 files as t0115. Files specifically
   preserved verbatim (only import path rewrites): `apply_params.py`, `build_cell_ais.py`,
   `constants_electrophys.py`, `extend_with_ais.py`, `generator_wrapper.py`,
   `hv_plateau_watchdog.py`, `parametric_placer.py`, `recorder.py`, `trial_helpers.py`,
   `bootstrap.py`, `cost_watchdog.py`. Satisfies REQ-2.

3. **Edit `code/constants.py` and `code/constants_morphology.py`.** Apply the following changes:

   * In `code/constants.py`:
     * Replace `T0115_SEEDS = (9354,)` with `T0122_SEEDS = (X,)` where `X` is drawn ONCE at edit
       time via `python -c "import secrets; print(secrets.randbelow(10000))"`, rejecting any draw
       that is round-ish (1000, 2000, ..., 9000, 5000) and re-drawing until the seed is not round.
     * Add `COST_CAP_USD: float = 6.0` and alias `T0122_HARD_BUDGET_USD: float = COST_CAP_USD`.
     * Add `T0122_PER_INSTANCE_WATCHDOG_USD: float = 5.0`.
     * Update the `T0104_HARD_BUDGET_PER_SEED_USD` back-compat alias to point to
       `T0122_HARD_BUDGET_USD` (so the `CostWatchdogTermination` dataclass picks up $6, not $4 or
       $25).
     * Add `_POOL_RESTART_EVERY: int = 10` (or confirm it is already there in the forked file). This
       is the project's 10-gen rule per memory `feedback_nsga2_pool_restart_every_10.md`.
     * Add `HV_PLATEAU_AUTO_STOP: bool = False` constant and add it to `__all__`. This makes the
       project-policy disable visible at import time even though the `HVPlateauTermination` is also
       removed from the live `TerminationCollection` (REQ-4).
     * Confirm `POP_SIZE` is re-exported (value 96 from `constants_morphology`).
     * Confirm `N_EVAL_SEEDS` is re-exported (value 3 from `constants_morphology`).
     * Add a `N_GEN_MAX: int = 60` constant (the task-description name) as an alias for
       `constants_morphology.N_GEN` so future grep on either name finds it.

   * In `code/constants_morphology.py`:
     * Change `N_GEN = 300` to `N_GEN: int = 60`.
     * Keep `POP_SIZE: int = 96` and `N_EVAL_SEEDS: int = 3` unchanged.
     * Change `REF_POINT_HV: tuple[float, float, float] = (0.0, 0.0, 0.0)` to a 2-entry tuple
       `REF_POINT_HV: tuple[float, float] = (0.0, V_MAX_UM3)` where `V_MAX_UM3: float = 50000.0` (a
       pessimistic per-cell volume cap; the t0091 cells topped at ~30000 um^3 so 50000 is a safe HV
       reference).
     * Add `HV_UTOPIA_VOLUME_UM3: float = 5000.0` (a Cuntz-informed minimum-volume target; small
       symmetric DSGC dendritic trees integrate to roughly this scale).
     * Keep `HV_UTOPIA_DSI: float = 0.7` unchanged.

   Expected output:
   `grep -n "_POOL_RESTART_EVERY\|HV_PLATEAU_AUTO_STOP\|POP_SIZE\|N_EVAL_SEEDS\|N_GEN_MAX\|COST_CAP_USD\|T0122_SEEDS" code/constants.py code/constants_morphology.py`
   returns exactly the values above (10, False, 96, 3, 60, 6.0, and the drawn seed). Satisfies
   REQ-3, REQ-4, REQ-5, REQ-6, REQ-7, REQ-8, REQ-12, REQ-13.

4. **Edit `code/nsga2_driver.py`.** Apply the following minimal changes:

   * Rewrite imports
     `tasks.t0115_seed9354_no_autostop.code.* -> tasks.t0122_dsi_cytoplasm_volume_nsga2.code.*`
     (already done by Step 2's global substitution; verify).
   * Default the `n_gen` argument to `60` (was `300` in t0115).
   * Confirm the live `TerminationCollection` contains only
     `{MaximumGenerationTermination(n_max_gen=n_gen), CostWatchdogTermination(...), OperatorStopTermination(...)}`
     — i.e., `HVPlateauTermination` is NOT in the list. (The t0115 driver already excludes it;
     verify after rewrite.)
   * Build the `CostWatchdogTermination` with `hard_budget_usd=T0122_HARD_BUDGET_USD` (which equals
     $6.0) and per-instance `T0122_PER_INSTANCE_WATCHDOG_USD` ($5.0).
   * Keep the `PerGenerationPoolRestart` callback firing every `_POOL_RESTART_EVERY = 10`
     generations.
   * Keep the per-gen dill checkpointing into
     `logs/steps/009_implementation/checkpoints/checkpoint_seed<S>_gen<NNNN>.pkl` and per-gen JSONL
     writes to `hv_trace.jsonl`.

   Expected output:
   `grep -n "HVPlateauTermination\|T0122_HARD_BUDGET\|n_gen.*60\|_POOL_RESTART_EVERY" code/nsga2_driver.py`
   returns the expected references and confirms `HVPlateauTermination` is not in the active
   `TerminationCollection`. Satisfies REQ-4, REQ-18.

5. **Write `code/cytoplasm_volume.py`.** Create a new ~30-line module with two functions:

   ```python
   import math
   from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
       MorphologyResult,
   )

   def compute_cytoplasm_volume_um3(*, cell: MorphologyResult) -> float:
       sections = [cell.soma, *cell.all_dends, cell.ais_proximal, cell.ais_distal]
       return sum(math.pi * (sec.diam / 2.0) ** 2 * sec.L for sec in sections)

   def compute_per_section_volume_breakdown(*, cell: MorphologyResult) -> dict[str, float]:
       soma_um3 = math.pi * (cell.soma.diam / 2.0) ** 2 * cell.soma.L
       dend_um3 = sum(math.pi * (s.diam / 2.0) ** 2 * s.L for s in cell.all_dends)
       ais_um3 = sum(
           math.pi * (s.diam / 2.0) ** 2 * s.L
           for s in [cell.ais_proximal, cell.ais_distal]
       )
       return {"soma_um3": soma_um3, "dendrites_um3": dend_um3, "ais_um3": ais_um3}
   ```

   Also write `code/cuntz_balancing_factor.py` (~50 lines) with one function:

   ```python
   def compute_balancing_factor(*, cell: MorphologyResult) -> float:
       # Cuntz 2010 bf = total_wiring_length_um /
       #                 (total_wiring_length_um + sum_of_path_distances_to_soma_um)
       total_wiring = sum(s.L for s in cell.all_dends)
       # walk parent chain from each terminal to soma, sum path distance
       path_dist_sum = ... # implement using cell.section_endpoints_xy or sec.parentseg().sec.L chain
       return total_wiring / (total_wiring + path_dist_sum)
   ```

   Expected output:
   `uv run python -c "from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.cytoplasm_volume import compute_cytoplasm_volume_um3; print('ok')"`
   prints `ok`. Satisfies REQ-9, REQ-21 (function only; chart in Step 12).

6. **Edit `code/evaluator.py`.** Apply the following changes:

   * Add `cytoplasm_volume_um3: float` field to the `CellEvalResult` dataclass at line 92.
   * Inside `evaluate_68d_vector`, immediately after `_ensure_worker_cell` builds the cell
     (currently around line 119-132), call
     `cytoplasm_volume_um3 = compute_cytoplasm_volume_um3(cell=cell.morphology_result)` and pass it
     into the `CellEvalResult` constructor.
   * Rewrite `BedBV3MorphProblem._evaluate` (line ~466) to emit
     `out["F"] = np.array([-result.dsi_vector_sum, +result.cytoplasm_volume_um3])` (DSI negated
     because maximised; volume NOT negated because minimised). Keep `n_obj = 2`.
   * Tighten the silence guard inside `_summarise_trials` (line ~298): replace
     `total_mean_spikes < SILENCE_SPIKE_COUNT_THRESHOLD` (currently `<10`) with
     `pd_spikes_sum < SILENCE_PD_SPIKES_THRESHOLD` (where `SILENCE_PD_SPIKES_THRESHOLD: int = 3`).
     Add the new constant near the top of the file.
   * Update `code/test_evaluator_dsi_guard.py` to expect the new `>= 3 PD spikes` threshold.

   Expected output:
   `grep -n "cytoplasm_volume_um3\|SILENCE_PD_SPIKES_THRESHOLD\|out\[.F.\]" code/evaluator.py`
   returns the new field, new constant, and the rewritten `out["F"]` line. Satisfies REQ-10, REQ-11.

### Milestone 2 — Smoke Gate and Remote Provisioning (Steps 7-8)

7. **Provision the Vast.ai instance.** Use the orchestrator's `/setup-remote-machine` skill to
   provision a single Vast.ai EPYC 32-core or 64-core instance (whichever is cheapest at
   provisioning time). Required filters: `>=64 GB RAM`, `reliability >= 0.99`, `dph <= 0.40`, prefer
   64-core EPYC 7B13 to inherit the t0113 / t0114 / t0115 wall-clock characteristic (~160 s/gen).
   The orchestrator writes the selected offer (including `selected_offer.price_per_hour`) to
   `logs/steps/008_setup-machines/machine_log.json`; the cost watchdog reads the hourly rate from
   this file at startup. Expected output: `cat logs/steps/008_setup-machines/machine_log.json` shows
   a `success: true` entry with a non-empty `selected_offer.id`. Satisfies REQ-14.

8. **[CRITICAL] Run the smoke gate locally on a small sample.** Execute the smoke gate via
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0122_dsi_cytoplasm_volume_nsga2 -- uv run python -m tasks.t0122_dsi_cytoplasm_volume_nsga2.code.smoke_gate`
   on a development machine BEFORE launching the Vast.ai job. The smoke gate runs the t0115 6-check
   suite plus one new check that `compute_cytoplasm_volume_um3` returns a positive float (> 100 um^3
   and < 100000 um^3) on a t0091-style anchor cell, and one new check that the live
   `TerminationCollection` introspection contains exactly
   `{MaximumGenerationTermination, CostWatchdogTermination, OperatorStopTermination}` (no
   `HVPlateauTermination`).

   **Validation gate**: the smoke gate is the trivial-baseline equivalent for this NSGA-II pipeline.
   **Baseline**: any t0091-style anchor cell must produce DSI >= 0.0 (a real, finite number, not NaN
   or +Inf) and a finite cytoplasm volume in [100, 100000] um^3. **Limit**: only the 5 anchor cells
   (not all 96 random-init cells). **Failure condition**: if ANY of the 5 anchors returns NaN F
   values, returns volume <= 100 um^3, or returns volume >= 100000 um^3, STOP and inspect individual
   outputs — do NOT launch the Vast.ai run. **Individual-output inspection**: read 5 individual
   `CellEvalResult` instances printed by the smoke gate (one per anchor) and verify each has a
   sensible DSI (in [-1, +1]), a sensible cytoplasm volume (in [100, 100000] um^3), a sensible
   PD-rate (>= 0 Hz, not negative), and a non-empty `cytoplasm_volume_um3` field. Expected output:
   the smoke gate prints `PASS` for all 8 checks (6 inherited from t0115 + 2 new). Satisfies REQ-15,
   REQ-16.

### Milestone 3 — NSGA-II Run on Vast.ai (Step 9, remote)

9. **[CRITICAL] Launch the NSGA-II run on Vast.ai.** SSH into the provisioned instance, sync the
   task folder, recompile the t0080 NEURON MOD library via `nrnivmodl` once, then execute:

   ```bash
   bash tasks/t0122_dsi_cytoplasm_volume_nsga2/code/run_seed<S>.sh
   ```

   The shell script calls
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0122_dsi_cytoplasm_volume_nsga2 -- uv run python -m tasks.t0122_dsi_cytoplasm_volume_nsga2.code.nsga2_driver --seed <S>`.
   The driver:

   * Initialises a `BedBV3MorphProblem(n_obj=2)` with `out["F"] = [-dsi, +volume_um3]`.
   * Runs NSGA-II with `pop_size=96`, `n_gen<=60`, `_POOL_RESTART_EVERY=10`,
     `TerminationCollection = {MaximumGenerationTermination(60), CostWatchdogTermination(hard_budget_usd=6.0), OperatorStopTermination(stop_md_path)}`.
   * Writes per-gen dill checkpoints to `logs/steps/009_implementation/checkpoints/`.
   * Writes per-gen `hv_trace.jsonl` with HV, best DSI, min volume, n_legit_cells, cumulative cost.

   **Validation gate (expensive operation)**: the NSGA-II run consumes the bulk of the $6 budget, so
   the first 3 generations must be inspected before continuing. **Baseline**: t0121's 5-seed
   substrate-rate canonical report shows **LEGIT yield of 2.58% +- SE 1.50%** on the 68-d substrate.
   **Limit**: stop and inspect after generation 3 (288 evaluations, ~5-10 minutes). **Failure
   condition**: if after 3 generations the population's best DSI is < 0.2 OR all 288 cells fail the
   silence guard (zero LEGIT cells), STOP, inspect the per-gen JSONL, and debug before continuing to
   gen 60. A best-DSI < 0.2 at gen 3 is anomalously low for this substrate (t0115 gen 3 had best DSI
   ~0.45) and indicates a bug in the new objective vector. **Individual inspection**: read 5
   individual `CellEvalResult` JSON entries from the gen-3 checkpoint and verify each has a sensible
   `cytoplasm_volume_um3` (positive, [100, 100000] um^3) and a sensible `objective_F_minimised` with
   the volume sign positive.

   **Operator-stop trigger**: the operator monitors the HV trajectory live via
   `tail -f logs/steps/009_implementation/hv_trace.jsonl` and creates `intervention/stop.md` when HV
   visibly plateaus. The `OperatorStopTermination` polls this file every 10 seconds. Expected
   output: the driver prints `[driver] terminated by stop_trigger=<X>` where `X` is one of
   `{max_gen, cost_watchdog, operator_stop}`. Satisfies REQ-17, REQ-18.

### Milestone 4 — Post-Run Analysis and Asset Building (Steps 10-15, local CPU)

10. **Sync results back and build Pareto / all-evaluations JSON.** Use the orchestrator's
    `sync_results_back.sh` (forked from t0115) to copy `logs/`, `results/data/`, and any
    intermediate checkpoints back to the local repo. Then run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0122_dsi_cytoplasm_volume_nsga2 -- uv run python -m tasks.t0122_dsi_cytoplasm_volume_nsga2.code.build_results --seed <S>`.
    The script:

    * Loads the final population from the last dill checkpoint.
    * Computes the Pareto front in (DSI, cytoplasm_volume_um3) space.
    * Writes `results/data/pareto_front_seed<S>.json` with one entry per Pareto-optimal cell,
      including `dsi_vector_sum`, `cytoplasm_volume_um3`, `pd_rate_hz`, `vector_68d`,
      `silence_failed_bool`, and a `legit_bool` (DSI >= 0.5 AND PD-rate >= 30 Hz AND NOT
      silence-failed AND cytoplasm_volume_um3 <= 50000 um^3).
    * Writes `results/data/all_evaluations_seed<S>.json` with every per-cell evaluation across all
      generations.

    Expected output: both JSON files exist with non-zero size and the Pareto front contains
    > = 5 cells. Satisfies REQ-19.

11. **Build the top-50 morphology grid.** Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0122_dsi_cytoplasm_volume_nsga2 -- uv run python -m tasks.t0122_dsi_cytoplasm_volume_nsga2.code.build_top50_morphologies --seed <S>`.
    This script is a verbatim copy of
    `tasks/t0115_seed9354_no_autostop/code/build_top50_morphologies.py` (308 lines) with only the
    input/output filename edits (`all_evaluations_seed<S>.json` and
    `top50_morphologies_seed<S>.png`). The script uses `LineCollection` over
    `section_endpoints_xy.items()` excluding soma and AIS, with the soma drawn as a separate
    `Circle` patch. **CRITICAL** — per memory `feedback_top50_morphologies_full_dendrites.md` and
    the t0114 failure, this chart MUST draw the full dendrite trees, NOT just soma dots.

    Expected output: `results/images/top50_morphologies_seed<S>.png` exists, is > 200 KB, and
    visually shows 50 dendrite trees in a 10x5 (or 7x8) grid. Satisfies REQ-20.

12. **Build the Pareto chart and Cuntz bf chart.** Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0122_dsi_cytoplasm_volume_nsga2 -- uv run python -m tasks.t0122_dsi_cytoplasm_volume_nsga2.code.build_pareto_plots --seed <S>`.
    This NEW script produces:

    * `results/images/pareto_front_dsi_vs_volume.png` — a scatter plot with cytoplasm volume
      (um^3) on the x-axis, DSI on the y-axis, Pareto-front cells highlighted in red, all evaluated
      cells shown in grey, the joint-pass region (DSI >= 0.5 AND volume <= 50000) shaded, and the
      joint-pass cells marked.

    * `results/images/cuntz_balancing_factor_top10.png` — a histogram of `bf` for the top-10 cells
      (ranked by DSI), with the Cuntz 2010 `[0.2, 0.7]` band overlaid as a shaded green span, and
      the count of in-band cells annotated.

    The script calls `compute_balancing_factor` on each top-10 cell, rebuilding the morphology via
    the canonical `generate_fixed_morphology` entry point from t0092.

    Expected output: both PNG files exist, are > 100 KB each, and contain the required axes, legend,
    and annotations. Satisfies REQ-20, REQ-21.

13. **Build `results/metrics.json`.** Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0122_dsi_cytoplasm_volume_nsga2 -- uv run python -m tasks.t0122_dsi_cytoplasm_volume_nsga2.code.metrics_builder`.
    The script uses the explicit multi-variant format and includes the registered metric
    `direction_selectivity_index` with three variants (`best_legit`, `overall_max`,
    `dsi_eq_one_count`) plus a parallel set for the cytoplasm-volume axis using a generic
    "cytoplasm_volume_um3" key (note: this key is NOT in `meta/metrics/`; if the verificator rejects
    it, the implementing agent should drop the cytoplasm-volume variant from `metrics.json` and
    surface the values only in the predictions asset and through the orchestrator-managed detailed
    results write-up).

    **Registered metrics applicability check** (per planning skill Phase 1 step 7): the aggregator
    returned 4 registered metrics: `direction_selectivity_index` (applies, primary objective),
    `tuning_curve_hwhm_deg` (does NOT apply — this task uses 2-direction PD-vs-ND-only, not a full
    angular sweep), `tuning_curve_reliability` (does NOT apply — same reason), `tuning_curve_rmse`
    (does NOT apply — no target tuning curve fit).

    Expected output: `results/metrics.json` exists, parses as JSON, contains a `variants` list with
    one variant per sub-condition, and `direction_selectivity_index` appears in every variant's
    `metrics` block. Satisfies REQ-22.

14. **Build the predictions asset.** Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0122_dsi_cytoplasm_volume_nsga2 -- uv run python -m tasks.t0122_dsi_cytoplasm_volume_nsga2.code.build_predictions_assets --seed <S>`.
    The script creates `assets/predictions/nsga2-cytoplasm-volume-bedb-morph/` with:

    * `details.json` — `spec_version: "2"`, `predictions_id: "nsga2-cytoplasm-volume-bedb-morph"`,
      `prediction_format: "jsonl.gz"`, `prediction_schema`: per-cell
      `{generation, cell_index, vector_68d, dsi_vector_sum, cytoplasm_volume_um3, pd_rate_hz, objective_F_minimised, silence_failed_bool, legit_bool}`,
      `created_by_task: "t0122_dsi_cytoplasm_volume_nsga2"`, `metrics_at_creation`: keys
      `{n_generations_completed, n_cells_total, best_dsi_ratio, min_cytoplasm_volume_um3, n_joint_pass_unique, final_hypervolume, final_cost_usd, stop_trigger}`.

    * `description.md` — the canonical documentation document per
      `meta/asset_types/predictions/specification.md`.

    * `files/predictions.jsonl.gz` — every per-cell row from `all_evaluations_seed<S>.json` as
      gzipped JSONL.

    Expected output: the asset folder exists with all three files and passes
    `meta.asset_types.predictions.verificator`. Satisfies REQ-23.

15. **Build the answer asset.** Run
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0122_dsi_cytoplasm_volume_nsga2 -- uv run python -m tasks.t0122_dsi_cytoplasm_volume_nsga2.code.build_assets --answer cuntz-balancing-factor-prediction-check`.
    The script creates `assets/answer/cuntz-balancing-factor-prediction-check/` with:

    * `details.json` per `meta/asset_types/answer/specification.md` (`spec_version` per current
      answer spec, `answer_id`, `short_answer_path`, `full_answer_path`, `question`,
      `answer_methods`).

    * Canonical short answer document — opens with "Yes" / "No" / "I don't know" depending on the
      top-10 bf distribution: "Yes" if >= 5 of 10 cells fall in `[0.2, 0.7]`, "No" if 0 of 10 fall
      in band, "Partially" if 1-4 of 10 fall in band. 2-5 sentences total. No inline citations in
      the `## Answer` section.

    * Canonical full answer document — explains the Cuntz 2010 bf computation, lists the top-10 bf
      values, names the in-band count, cross-references the Pareto-front chart and Cuntz bf chart,
      includes a `## Sources` section with reference link definitions for the cited paper IDs
      (`10.1371_journal.pcbi.1002107` for Cuntz 2010) and task IDs (`t0091`, `t0115`, `t0121`).

    **Stopping criterion for evidence** (per answer-question task type guideline): the evidence is
    sufficient when the top-10 bf distribution is computed and the in-band count is non-ambiguous
    (>= 5 or = 0). If 1-4 of 10 fall in band, the answer text says "Partially" and lists the
    per-cell bf values explicitly so the operator can decide. If FEWER than 10 LEGIT cells exist in
    the final population, the answer says "Insufficient evidence" and reports the partial result
    with the n LEGIT cells available.

    Expected output: the answer asset folder exists with all three files and passes
    `meta.asset_types.answer.verificator`. Satisfies REQ-24.

* * *

## Remote Machines

**Required.** One Vast.ai EPYC instance (32-core or 64-core, whichever is cheapest at provisioning
time), single-instance run, ~6-12 hours of compute. Selection filters: `>=64 GB RAM`,
`reliability >= 0.99`, `dph <= 0.40`. Idle GPU acceptable; the workload is CPU-bound NEURON. The
compiled t0080 NEURON MOD library (`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`)
ships in the repo with pre-compiled `.c` files; the remote machine runs `nrnivmodl` once at
bootstrap to produce `x86_64/.libs/libnrnmech.so`. The cost watchdog reads
`selected_offer.price_per_hour` from `logs/steps/008_setup-machines/machine_log.json` and tears down
the instance on the $5 per-instance cap. Reference:
`arf/specifications/remote_machines_specification.md`.

* * *

## Assets Needed

* **From `t0024_port_de_rosenroll_2026_dsgc`** — canonical Bed B cell builder, NEURON bootstrap
  helpers (`_ensure_neuron_on_path`), AR(2) noise generator (`generate_ar2_batch`), bar-arrival
  kinematic helpers. Imported by full dotted path through the verbatim copy of `trial_helpers.py`.
* **From `t0080_bedb_mobo_v3_dendritic_spike_nsga2`** — 54-d electrophys parameter scheme,
  `apply_parameter_vector`, `ensure_t80_dll_loaded` (process-singleton MOD library loader), 12
  compiled NEURON channels (`nav16t80`, `napt80`, ..., `skahpt80`). Imported by full dotted path
  through the verbatim copy of `apply_params.py`.
* **From `t0090_morphology_generator_diversity_test`** — 14-d morphology parameter space,
  `MorphologyParams`, `MorphologyResult`, `PARAM_BOUNDS`, `INT_PARAM_NAMES`, `PARAM_*` string
  constants. Imported by full dotted path per C-0093-01.
* **From `t0092_diagnose_morphology_generator_silence`** — `generate_fixed_morphology` (the
  canonical morphology entry point with the z-axis soma area patch), `insert_baseline_channels`.
  Imported by full dotted path through the verbatim copy of `generator_wrapper.py`.
* **From `t0106_long_pdnd_nsga2_300gen`** — NSGA-II driver substrate (parent of the lineage),
  `PerGenerationPoolRestart` callback, `OperatorStopTermination`. Inherited through the t0115 fork.
* **From `t0115_seed9354_no_autostop`** — fork point for `code/` (~25 Python files copied verbatim
  and minimally patched).
* **From `t0120_morph_generator_geometry_audit`** — gating dependency; verdict consumed at Step 1.
* **From `t0121_5seed_substrate_rate_canonical_report`** — headline literature-comparison baseline
  (5-seed LEGIT yield 2.58% +- SE 1.50%); `compare_literature.md` template.

* * *

## Expected Assets

Matches `task.json` `expected_assets: {"predictions": 1, "answer": 1}`:

* **predictions / `nsga2-cytoplasm-volume-bedb-morph`** — per-cell 68-d vectors, objective F,
  per-direction firing, cytoplasm volume, and Cuntz bf for the top-10 cells. Format: gzipped JSONL.
  Built by Step 14. Satisfies the `predictions: 1` count.
* **answer / `cuntz-balancing-factor-prediction-check`** — answer to "Does NSGA-II with a
  cytoplasm-volume cost objective produce a high-DSI front in Cuntz 2010's predicted
  balancing-factor `[0.2, 0.7]` band?" with the top-10 bf distribution as primary evidence. Built by
  Step 15. Satisfies the `answer: 1` count.

* * *

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already done) | done |
| Planning (already done) | done |
| Implementation Milestone 1 (steps 1-6, fork + edit, local) | 2-3 hours |
| Implementation Milestone 2 (steps 7-8, smoke gate + provisioning) | 1-2 hours |
| Implementation Milestone 3 (step 9, NSGA-II remote run) | 6-12 hours (operator-stop or 60-gen ceiling) |
| Implementation Milestone 4 (steps 10-15, analysis + asset building, local) | 2-4 hours |
| **Total** | **11-21 hours** |

* * *

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Cytoplasm-volume sign flip in `out["F"]` (negated by mistake) drives optimiser to inflate volumes instead of minimising. | Low | High (entire run produces wrong Pareto front) | Step 8 smoke gate explicitly checks an anchor cell's `objective_F_minimised[1]` is positive (`+volume_um3`). If negative, STOP and fix before launching the Vast.ai run. |
| Silence-guard regression: the tightened guard accidentally removes LEGIT cells, shrinking the Pareto front to < 5 cells. | Medium | Medium (answer-asset stopping criterion triggers "Insufficient evidence") | Step 8 smoke gate checks the anchor-cell PD-spike count. Step 9 validation gate at gen 3 checks `n_legit_cells > 0`. If 0, STOP and inspect individual cells before continuing. |
| Vast.ai instance fails to provision (no offers under $0.40/hr at provisioning time). | Low | Medium (delays run; orchestrator must retry) | Setup-machines step retries up to 5 offers automatically. If all fail, the operator can manually relax `dph <= 0.40` to `dph <= 0.50` in the offer filter. |
| Cost watchdog races condition with operator-stop and exceeds $6 cap by a few cents. | Low | Low (Vast.ai charges only the consumed seconds; per-instance $5 cap leaves $1 buffer). | The $5 per-instance watchdog cap is intentionally $1 below the $6 task cap to absorb any race. Worst case is $0.10-0.50 over the per-instance cap; well within the buffer. |
| Cuntz bf formula misimplementation (e.g., wrong path-distance walk) reports the wrong band. | Medium | Medium (answer-asset verdict is wrong) | Unit-test `compute_balancing_factor` on a synthetic symmetric tree (expected `bf` near 0.5 per Cuntz 2010 Fig. 1) before running on top-10 cells. If the synthetic tree returns `bf` outside `[0.4, 0.6]`, STOP and debug. |
| Top-50 morphology chart drawn as soma-only (the t0114 failure). | Low | High (operator rejects the asset; chart must be redone) | Step 11 reuses t0115's `build_top50_morphologies.py` verbatim with only filename edits; the `LineCollection` over `section_endpoints_xy.items()` excluding soma/AIS is preserved. After Step 11, the operator visually verifies the chart shows dendrite trees before Step 12 proceeds. |
| HV-plateau auto-stop accidentally re-enabled (e.g., by a copy-paste error in `nsga2_driver.py`). | Low | Medium (run terminates early before reaching the meaningful Pareto front) | Step 8 smoke gate introspects the live `TerminationCollection` and asserts `HVPlateauTermination` is NOT in it. If it is, STOP and remove it. `HV_PLATEAU_AUTO_STOP = False` constant in `code/constants.py` also serves as a documentation trail. |

* * *

## Verification Criteria

Each criterion is a concrete, testable check. The verificator commands use the full
`PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs ...` pattern enforced by
project rule 1.

* **C1 — `_POOL_RESTART_EVERY = 10` is enforced in code (REQ-3).** Run
  `grep -n "_POOL_RESTART_EVERY" tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants.py` and
  confirm output contains `_POOL_RESTART_EVERY: int = 10`. Then run
  `grep -n "_POOL_RESTART_EVERY" tasks/t0122_dsi_cytoplasm_volume_nsga2/code/nsga2_driver.py` and
  confirm the `PerGenerationPoolRestart` callback fires every `_POOL_RESTART_EVERY` generations.
  Expected: both greps succeed.

* **C2 — `HV_PLATEAU_AUTO_STOP = False` is enforced in code and the live termination collection
  excludes `HVPlateauTermination` (REQ-4).** Run
  `grep -n "HV_PLATEAU_AUTO_STOP" tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants.py` and
  confirm output contains `HV_PLATEAU_AUTO_STOP: bool = False`. Then run
  `grep -A 5 "TerminationCollection" tasks/t0122_dsi_cytoplasm_volume_nsga2/code/nsga2_driver.py`
  and confirm the active `TerminationCollection` contains exactly
  `{MaximumGenerationTermination, CostWatchdogTermination, OperatorStopTermination}` and does NOT
  contain `HVPlateauTermination`. Expected: both checks pass.

* **C3 — `POP_SIZE = 96` is enforced in code (REQ-5).** Run
  `grep -n "POP_SIZE" tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants.py tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants_morphology.py`
  and confirm output contains `POP_SIZE: int = 96`. Expected: grep succeeds and value is exactly 96.

* **C4 — `N_EVAL_SEEDS = 3` is enforced in code (REQ-6).** Run
  `grep -n "N_EVAL_SEEDS" tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants.py tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants_morphology.py`
  and confirm output contains `N_EVAL_SEEDS: int = 3`. Expected: grep succeeds and value is exactly
  3\.

* **C5 — `N_GEN_MAX = 60` is enforced in code (REQ-7).** Run
  `grep -n "N_GEN_MAX\|N_GEN " tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants.py tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants_morphology.py`
  and confirm output contains `N_GEN_MAX: int = 60` (or `N_GEN: int = 60`). Expected: grep succeeds
  and value is exactly 60.

* **C6 — `COST_CAP_USD = 6.0` is enforced in code and wired into the cost watchdog (REQ-8).** Run
  `grep -n "COST_CAP_USD\|T0122_HARD_BUDGET_USD" tasks/t0122_dsi_cytoplasm_volume_nsga2/code/constants.py`
  and confirm output contains `COST_CAP_USD: float = 6.0`. Then run
  `grep -n "hard_budget_usd" tasks/t0122_dsi_cytoplasm_volume_nsga2/code/nsga2_driver.py` and
  confirm the `CostWatchdogTermination` is constructed with the $6 cap. Expected: both checks pass.

* **C7 — Gating check passed (REQ-1).** Confirm
  `tasks/t0120_morph_generator_geometry_audit/results/results_summary.md` contains the verdict
  "rendering-only" and "t0122_dsi_cytoplasm_volume_nsga2 is unblocked". Expected:
  `grep "rendering-only\|unblocked" tasks/t0120_morph_generator_geometry_audit/results/results_summary.md`
  returns both strings.

* **C8 — Predictions asset passes its verificator (REQ-23).** Run
  `PYTHONIOENCODING=utf-8 uv run python -m meta.asset_types.predictions.verificator tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/predictions/nsga2-cytoplasm-volume-bedb-morph`
  and confirm 0 errors. Expected: verificator prints "PASSED" (or returns exit code 0).

* **C9 — Answer asset passes its verificator (REQ-24).** Run
  `PYTHONIOENCODING=utf-8 uv run python -m meta.asset_types.answer.verificator tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/answer/cuntz-balancing-factor-prediction-check`
  and confirm 0 errors. Expected: verificator prints "PASSED" (or returns exit code 0).

* **C10 — `metrics.json` registers `direction_selectivity_index` with the required variants
  (REQ-22).** Run
  `PYTHONIOENCODING=utf-8 uv run python -c "import json; data = json.loads(open('tasks/t0122_dsi_cytoplasm_volume_nsga2/results/metrics.json').read()); variant_ids = [v['variant_id'] for v in data['variants']]; assert any('best_legit' in v for v in variant_ids); assert any('overall_max' in v for v in variant_ids); assert any('dsi_eq_one_count' in v for v in variant_ids); print('OK')"`
  and confirm output is `OK`.

* **C11 — All required result files and charts exist (REQ-19, REQ-20, REQ-21).** Run
  `ls tasks/t0122_dsi_cytoplasm_volume_nsga2/results/data/pareto_front_seed*.json tasks/t0122_dsi_cytoplasm_volume_nsga2/results/data/all_evaluations_seed*.json tasks/t0122_dsi_cytoplasm_volume_nsga2/results/images/pareto_front_dsi_vs_volume.png tasks/t0122_dsi_cytoplasm_volume_nsga2/results/images/top50_morphologies_seed*.png tasks/t0122_dsi_cytoplasm_volume_nsga2/results/images/cuntz_balancing_factor_top10.png`
  and confirm all 5 patterns return at least one file. Expected: `ls` returns 5 paths with no "No
  such file" errors.

* **C12 — Plan verificator passes (REQ-coverage sanity check).** Run
  `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.verificators.verify_plan t0122_dsi_cytoplasm_volume_nsga2`
  and confirm 0 errors. Expected: verificator prints "PASSED" (or returns exit code 0). This
  criterion also serves as the requirement-coverage check: PL-W006 fires if no `REQ-*` items are
  present, and PL-W007 fires if `## Step by Step` does not reference any `REQ-*`.
