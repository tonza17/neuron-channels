# t0104 — 68-d NSGA-II 2-Objective (DSI + PD-rate) at 3 Random-Init GA Seeds, N=4, gens=20

## Context

Direct researcher commission in brainstorm session 22 (2026-05-12), immediately after t0102 closed.
t0102 ran 68-d random-init NSGA-II at GA seeds=2, N_EVAL_SEEDS=4, gens=20 on three objectives (DSI
vector-sum, PD-rate, robustness) and produced **zero strict joint-pass cells across 2,592 evaluated
cells**. The session-22 researcher hypothesis: dropping the robustness objective frees NSGA-II's
crowding-distance selection to spend its diversity budget on the DSI / PD-rate trade-off alone,
potentially recovering joint-pass cells without invoking warm-start.

Project total budget was raised from $35 to $50 immediately prior to this task (commit `388e8557` on
main) so the $15 per-task cap below does not violate the project-level ceiling.

This task also closes the load-bearing **S-0102-01 DSI vector-sum artifact** by porting a
silenced-cell guard into `evaluator.py` before the NSGA-II run. The guard returns DSI = 0.0 when the
cell's total spike count across all 16 directions is below 10, eliminating the floating-point
artifact that put 27 t0102 cells at a spurious DSI = 1.0.

## Goal

Run the exact same 68-d Bed B + morphology NSGA-II substrate as t0102, with three changes:

1. **Objective vector**: 3 → 2 (drop robustness; keep DSI vector-sum + PD-rate)
2. **GA seeds**: 2 → 3 (44, 55, 66)
3. **DSI-silence guard active**: the S-0102-01 fix lands in this task's `evaluator.py`

All other knobs match t0102 exactly: `N_EVAL_SEEDS=4`, `n_gen=20`, `pop=96`, random LHS init, Bed B
+ 14-d morphology substrate.

## Key Questions

1. **Does dropping robustness recover joint-pass cells?** Concretely: across 3 seeds × pop=96 ×
   gens=20 = 6,048 evaluated cells, find at least one with DSI ≥ 0.5 AND PD ≥ 30 Hz on the
   cleaned DSI metric. Falsifiable: the answer is yes (≥ 1 cell) or no (0 cells).
2. **Does the DSI-silence guard remove the DSI = 1.0 corner from the Pareto front?** Quantify how
   many cells in this run reach the guard floor (DSI = 0.0 because total spikes < 10) and confirm
   the Pareto front no longer contains DSI = 1.0 / PD = 0 cells.
3. **Does the 2-objective Pareto front differ qualitatively from t0102's 3-objective front when
   restricted to the (DSI, PD) plane?** Specifically: at any given DSI threshold, does this run
   reach a higher PD-rate ceiling than t0102?

## Approach

Fork t0102's `code/` substrate verbatim. The only code-level changes:

1. **`evaluator.py`**:
   * Patch `_vector_sum_dsi` (or its wrapping `evaluate_cell` flow) so that DSI returns 0.0 when
     `sum(total_spike_count_per_direction) < 10` across the 16 directions.
   * Reduce the F-row returned to pymoo from `[-dsi, -pd, -robustness]` to `[-dsi, -pd]`. Keep the
     `robustness` field in the per-cell summary `dict` so it remains in the predictions assets and
     analysis can still inspect the dropped axis, but it must not enter NSGA-II selection.
   * Update `n_obj` from 3 to 2.

2. **`nsga2_driver.py`**: set `Problem(n_obj=2, ...)` in the pymoo definition.

3. **Unit test**: add `code/test_evaluator_dsi_guard.py` that builds a synthetic cell with all-zero
   direction counts and asserts the new evaluator returns DSI = 0.0 (not 1.0). Run it as part of the
   local smoke gate before scaling out.

4. **GA seeds**: launch three NSGA-II processes with `seed=44`, `seed=55`, `seed=66` sequentially on
   one Vast.ai instance. `pop=96`, `n_gen=20`, LHS-init each. (Seeds 44 and 55 are reused from t0102
   so the 2-obj vs 3-obj comparison is an apples-to-apples lift, with 66 as the genuinely fresh
   sample.)

5. **Cost watchdog**: keep t0102's per-seed $4 watchdog. Bind the watchdog directly to instance
   teardown so post-NSGA-II idle billing cannot accumulate (S-0102-08 partial application). Total
   hard cap: $15 enforced at the orchestrator.

## Why This Matters for the Research Questions

The project's research question 1 ("Which combinations of somatic voltage-gated sodium and potassium
conductances maximise AP frequency for a preferred-direction wave while suppressing firing in the
null direction?") has been the central optimisation target of t0080-t0102. The current evidence from
t0099 + t0102 is that NSGA-II on this 68-d substrate cannot reach the joint-pass corner from random
init at any seed/generation balance tried so far. Two unexamined factors remain in the NSGA-II
configuration: the objective count (this task) and the algorithm itself (deferred to S-0102-03 /
S-0102-04). This task tests the cheaper of the two factors first. If 2-objective NSGA-II recovers
joint-pass cells, the substrate is reachable and the issue was objective dilution; if it doesn't,
the substrate-limitation reading hardens and algorithm replacement becomes the next move.

## Cost Estimation

| Item | Estimate |
| --- | --- |
| Vast.ai instance | $0.24/hr (RTX 4090 / EPYC 7B13 64-core, t0099 / t0102 baseline) |
| Per-cell eval at N=4 | ~5x faster than t0099's N=20 (same as t0102) |
| Cells per seed | 96 + 20 × 96 = 2,016 |
| Cells total | 3 × 2,016 = 6,048 |
| Wall-clock estimate | ~30-36 h (6,048 cells × ~18 s = ~30 h plus overhead) |
| Productive compute | ~$8-10 (3 seeds at ~$3-3.5 each) |
| Idle / setup overhead | ~$1-2 (with hardened teardown per S-0102-08) |
| **Predicted spend** | **~$10-12** |
| **Hard cost cap** | **$15** (explicit per-task override; project budget is $50) |

## Step by Step

Canonical step IDs from `arf/specifications/task_steps_specification.md`:

1. `preflight` — confirm all six dependencies are completed; check that `tasks/t0102_*/code/` is
   reusable; smoke-test t0102's pipeline locally on one cell with the 2-obj + DSI-guard patch.
2. `research-code` — audit t0102's `evaluator.py` and `nsga2_driver.py`, document the exact lines
   to change in `research/research_code.md`. No paper-research step is needed.
3. `planning` — produce `plan/plan.md` with the cost / time / risk table; agree REQ-1..REQ-N
   including REQ on the DSI-silence guard unit test and REQ on idle-teardown wiring.
4. `setup-machines` — provision one Vast.ai instance matching t0102's spec; record
   `machine_log.json`.
5. `implementation` —
   * 5a. SCP code (with patches) to instance.
   * 5b. Run substrate-consistency smoke gate at N_EVAL_SEEDS=4 with DSI-guard active and `n_obj=2`
     (REQ-7-equivalent).
   * 5c. Run NSGA-II seed=44, pop=96, gens=20, 2 objectives.
   * 5d. Run NSGA-II seed=55, pop=96, gens=20, 2 objectives.
   * 5e. Run NSGA-II seed=66, pop=96, gens=20, 2 objectives.
   * 5f. Pull predictions back, build per-seed predictions assets.
6. `destroy-machines` — Vast.ai instance teardown within 5 minutes of last seed completion; record
   final cost in `results/costs.json` and `results/remote_machines_used.json`.
7. `analysis` — joint-pass tally per seed, hypervolume curves, per-seed DSI/PD scatter, anchor
   distribution histogram, side-by-side comparison vs t0102 (3-obj) and t0099 (3-obj N=20). Quantify
   the DSI-guard impact: count cells at DSI = 0.0 floor, count cells with raw-DSI ≥ 0.99 that the
   guard would have kept.
8. `reporting` — write `results/results_summary.md`, `results/results_detailed.md` with all charts
   embedded via `![desc](images/file.png)`, populate `metrics.json`, `costs.json`,
   `remote_machines_used.json`, and `suggestions.json`. Write one answer asset addressing Key
   Question 1.

## Remote Machines

One Vast.ai instance matching t0099 / t0102 spec:

* GPU tier: not required (NEURON is CPU-bound; any attached GPU is incidental)
* CPU: AMD EPYC 7B13 or equivalent, ~64 effective cores
* RAM: 200+ GB
* Location: Norway preferred for $0.24/hr offer rate
* Hard runtime cap: 40 hours
* Idle-uptime safeguard: tear down within 5 minutes of last seed completion (post-watchdog idle was
  ~$2 of t0102's overrun)

## Assets Needed

* `tasks/t0024_port_de_rosenroll_2026_dsgc` — Bed B compartmental model
* `tasks/t0102_seedscale_n4_gen20/code/` — driver fork base (verbatim except the 2-obj + DSI-guard
  patches)
* `tasks/t0093_resweep_and_t0090_correction/code/` — morphology generator (post-patch)
* `tasks/t0086_robustness_cluster_bio_comparison/code/` — anchor / clustering utilities (used in
  analysis step only)

## Expected Assets

* 3 predictions assets (one per GA seed, 2,016 cells each): `nsga2-seed44-bedb-morph-n4-gen20-2obj`,
  `nsga2-seed55-bedb-morph-n4-gen20-2obj`, `nsga2-seed66-bedb-morph-n4-gen20-2obj`
* 1 answer asset addressing: "Does 2-objective NSGA-II (DSI + PD-rate, with the DSI-silence guard
  applied) recover joint-pass cells where t0102's 3-objective run found zero?"

## Time Estimation

* Local prep + smoke + provisioning: 1-2 h
* Vast.ai NSGA-II runs (3 seeds sequential): 28-34 h
* Analysis + reporting: 3-4 h
* **Total wall-clock**: 32-40 h

## Risks & Fallbacks

* **Risk**: even without robustness in the objective vector, joint-pass yield remains zero,
  confirming the 68-d substrate is empirically empty of joint-pass cells under random init.
  **Fallback**: negative result is publishable as the definitive 2-objective control for the
  substrate-limitation hypothesis; the next move becomes algorithm replacement (S-0102-03 IBEA or
  S-0102-04 Dang pop≥290).

* **Risk**: per-seed wall-clock grows super-linearly due to NEURON memory accumulation (known from
  t0099 / t0102). **Fallback**: restart Python worker between generations as in t0102. If still too
  slow, cut third seed at gen 15 and report partial result.

* **Risk**: Vast.ai instance cost exceeds $15 cap due to instance-price drift or idle overrun.
  **Fallback**: per-seed $4 watchdog terminates each run individually; total cap $15 enforced at
  orchestrator level; idle teardown within 5 min hardens against the t0102 $2 idle leak.

* **Risk**: morphology generator silently produces empty trees (known from t0090 / t0093).
  **Fallback**: REQ-7-equivalent smoke gate must pass before committing to long run.

* **Risk**: the DSI-silence guard introduces a regression where legitimate near-silent cells with
  real direction selectivity (e.g., 5 PD spikes, 0 ND spikes) get masked. **Fallback**: include in
  results_detailed.md a sensitivity sweep of the spike-count threshold (5, 10, 20, 50) on the t0102
  predictions to confirm 10 is conservative; note any cells in the (5, 10) band as a known
  limitation. Unit test in `code/test_evaluator_dsi_guard.py` documents the exact threshold.

## Verification Criteria

* `verify_task_metrics t0104_nsga2_2obj_dsi_pdrate_3seeds` passes with 0 errors.
* `verify_machines_destroyed t0104_nsga2_2obj_dsi_pdrate_3seeds` confirms Vast.ai instance is
  destroyed.
* `verify_research_code` and `verify_plan` pass with 0 errors.
* All 3 predictions assets validate against the predictions specification.
* Total cost in `results/costs.json` does not exceed $15.00.
* Unit test `tasks/t0104_*/code/test_evaluator_dsi_guard.py` passes locally and in the smoke gate.
* At least one of the following holds (both are publishable):
  * **Positive**: ≥ 1 strict joint-pass cell (DSI ≥ 0.5, PD ≥ 30 Hz, on the guard-cleaned DSI)
    found in at least one of the three seeds.
  * **Negative**: 0 strict joint-pass cells across all three seeds, confirming the t0102 null
    extends to the 2-objective formulation.

## Out of Scope

* IBEA replacement (deferred suggestion S-0102-03).
* Dang 2023 pop ≥ 290 theory-grounded NSGA-II (deferred suggestion S-0102-04).
* Sign-averaging objective formulation per Morinaga 2024 (deferred suggestion S-0102-07).
* Anchor-distance lineage trace across t0080-t0102 Pareto cells (deferred suggestion S-0102-05) —
  separate analysis task.
* Calcium-clearance perturbation sweep on the 27 silenced cells (deferred suggestion S-0102-06).
* Lowering the project-wide `N_SEEDS` default in `tasks/t0080_*/code/constants.py` (deferred
  suggestion S-0101-02).
* Correcting Poleg-Polsky 2026 `summary.md` fabrications (deferred suggestion S-0101-01).
