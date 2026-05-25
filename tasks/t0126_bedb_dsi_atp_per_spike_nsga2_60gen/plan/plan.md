---
spec_version: "2"
task_id: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"
date_completed: "2026-05-25"
status: "complete"
---
# Plan: NSGA-II DSI vs ATP-per-Spike (Bed B + 14-d Morph) — 60-Generation Replication

## Objective

Fork the t0124 68-d Bed B + 14-d morphology NSGA-II substrate end-to-end (DSI maximised, ATP-per-
spike minimised) and re-run it verbatim with a fresh GA seed and a strict 60-generation completion
mandate. t0124 was operator-stopped at gen 9 of 60 (subagent session budget exhausted while polling
NSGA-II progress; only $0.07 of the $6 cost cap had been spent and the HV trajectory was still
ascending), and reported a partial n=5 Pareto front with bootstrap r(DSI, ATP) = +0.806
[0.716, 1.000]. That correlation is suggestive of a Carter-Bean Na/K-overlap penalty but is
**undeterminable from artefact** because (a) `_POOL_RESTART_EVERY = 10` had not fired yet (first
scheduled restart is gen 10), (b) all 5 cells share LHS-init ancestry from a single initial
population, and (c) diversity has not had time to build up across recombinant generations. This task
is the dedicated continuation that takes the t0124 substrate to gen 60 with a fresh seed and
quantitatively re-tests whether the +0.806 correlation survives — answering the S-0124-01
follow-up suggestion. **No protocol changes, no parameter changes, no objective changes** beyond the
seed and the completion mandate.

**Done** means: (1) the NSGA-II run terminates cleanly via the 60-generation ceiling OR the $6 cost
watchdog (NEVER operator-stop unless watchdog or gen-60 ceiling has fired); (2) one predictions
asset `nsga2-dsi-atp-per-spike-bedb-morph-60gen` is written with per-cell 68-d vectors, F =
`[-dsi_best_legit, +atp_per_spike_molecules]`, per-direction firing, DSI variants, per-compartment
ATP breakdown, and diagnostic PD-rate / ND-rate / cytoplasm volume / MI; (3) one answer asset
`dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact` is written delivering the Carter-Bean vs
artefact verdict per the S-0124-01 decision rule; (4) `results/metrics.json` registers the chosen
DSI variants in the explicit multi-variant format; (5) the seven required charts (including a new
t0124-vs-t0126 side-by-side Pareto chart) and the Pareto / all-evaluations JSON dumps are saved; (6)
the Carter-Bean smoke-gate passes within 30% on the canonical Bed B anchor cell before NSGA-II
launch.

* * *

## Task Requirement Checklist

Operative task text quoted verbatim from `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/task.json`
and the resolved long description at
`tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/task_description.md`:

```text
Name: NSGA-II DSI vs ATP-per-spike Bed B + 14-d morph: 60-gen replication

Short description: Fresh-seed 60-gen replication of t0124 NSGA-II (DSI vs
ATP-per-spike, Bed B + 14-d morph); tests whether +0.806 r(DSI,ATP) is a
Carter-Bean penalty or early-NSGA-II artefact.

Dependencies: t0124_bedb_dsi_atp_per_spike_nsga2.
Expected assets: 1 predictions, 1 answer.
Task types: experiment-run, data-analysis, comparative-analysis.
Source suggestion: S-0124-01.

Hard Constraints (non-negotiable, reproduced in code/constants.py):
* _POOL_RESTART_EVERY = 10  (10-gen rule)
* HV_PLATEAU_AUTO_STOP = False  (disabled per project policy)
* POP_SIZE = 96
* N_EVAL_SEEDS = 3
* N_DIRECTIONS = 2  (antipodal pair 0/180)
* N_GEN_MAX = 60  (this run MUST reach gen 60 unless $6 watchdog trips)
* COST_CAP_USD = 6.0  (Vast.ai balance >= $7, $1 teardown buffer)

DSI Recipe (silence-guarded ratio, inherited verbatim from t0124):
R_PD = mean spike count over N_EVAL_SEEDS trials at 0 deg
R_ND = mean spike count over N_EVAL_SEEDS trials at 180 deg
DSI = (R_PD - R_ND) / (R_PD + R_ND)        if R_PD >= 3 spikes
DSI = -1.0                                  if R_PD <  3 spikes (silence guard)

* Headline DSI variant: best_legit
* Tracked DSI variants: best_legit, overall_max, dsi_eq_one_count

ATP-per-Spike Recipe (Sengupta 2010, inherited verbatim from t0124):
N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int(I_Na^inward) dt
* Record seg.ina at simulation dt for soma + AIS proximal + AIS distal +
  all dendritic segments. FULL mode only.
* AP windows: somatic Vm threshold crossing at -20 mV, +/-2 ms around peak,
  2 ms refractory between detections.
* Per-AP per-compartment charge: integrate min(I_Na, 0) over AP window in
  seconds, multiply by seg.area_cm2; ATP = Q / (e * 3).
* Sum across compartments, then divide total ATP by total spikes across
  all FULL-mode trials -> ATP molecules per spike (headline, LOWER IS
  BETTER).
* If total spike count == 0: atp_per_spike = +inf (sentinel).

Carter-Bean 2009 smoke-gate (inherited verbatim from t0124):
* ATP/AP/cm at AIS on the canonical Bed B cell must be within 30% of the
  first-principles canonical band ~1e8 - 1e9 ATP/AP/cm (geometric mean
  ~3e8); the three-tier PASS/WARN/FAIL policy from t0124 is preserved.

Decision rule for the Carter-Bean vs artefact answer (from S-0124-01):
* r(DSI, ATP) > +0.5 with 95% CI excluding 0 at n >= 20 on the full
  final front -> ACCEPT Carter-Bean penalty interpretation.
* r drops below +0.3 -> ACCEPT the early-NSGA-II artefact null.
* Anything in between -> INDETERMINATE; recommend further replication.

Background launch (S-0124-02 framework concern):
* The implementation subagent must launch NSGA-II in the BACKGROUND (so
  the run is decoupled from the subagent session budget) and poll only
  progress checkpoints (hv_trace.jsonl + heartbeat) -- not the live
  training loop -- to avoid the t0124 operator-stop failure mode.

Expected outputs:
* assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph-60gen/
* assets/answer/dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact/
* results/data/pareto_front_seed*.json
* results/data/all_evaluations_seed*.json
* results/images/pareto_front_dsi_vs_atp.png
* results/images/pareto_front_t0124_vs_t0126.png   (NEW, side-by-side)
* results/images/carter_bean_atp_per_ap_check.png
* results/images/attwell_laughlin_signalling_budget.png
* results/images/top50_morphologies_seed*.png  (full dendrite trees)
* results/images/hv_trajectory_seed*.png  (gen 1 -- gen 60)

GA seed: secrets.randbelow(10000); avoid round numbers, prior lineage
seeds, AND t0124's seed 6650. This plan records the drawn seed = 8929.
```

Decomposed requirements (each step in `## Step by Step` cites the `REQ-*` items it satisfies):

* **REQ-1** — Hard constant `_POOL_RESTART_EVERY = 10` is asserted in `code/constants.py` at
  module import (project's 10-gen rule per memory `feedback_nsga2_pool_restart_every_10.md`). The
  `PerGenerationPoolRestart` callback fires every 10 gens in `code/nsga2_driver.py`. Satisfied by
  Steps 3 and 7. Evidence: `grep -n "_POOL_RESTART_EVERY" code/constants.py` returns
  `_POOL_RESTART_EVERY: int = 10`.

* **REQ-2** — Hard constant `HV_PLATEAU_AUTO_STOP = False` is asserted in `code/constants.py` and
  the live `TerminationCollection` in `code/nsga2_driver.py` does NOT contain `HVPlateauTermination`
  (`hv_plateau_watchdog.py` is importable for the smoke-gate introspection check only). Satisfied by
  Steps 3 and 7. Evidence:
  `grep -n "HV_PLATEAU_AUTO_STOP\|HVPlateauTermination" code/constants.py code/nsga2_driver.py`
  shows `HV_PLATEAU_AUTO_STOP: bool = False` and `HVPlateauTermination` absent from the active
  collection.

* **REQ-3** — Hard constant `POP_SIZE = 96` is asserted in `code/constants_morphology.py` and
  re-exported by `code/constants.py`. Satisfied by Step 3. Evidence: `grep -n "POP_SIZE"` returns
  `POP_SIZE: int = 96`.

* **REQ-4** — Hard constant `N_EVAL_SEEDS = 3` is asserted in `code/constants_morphology.py`.
  Satisfied by Step 3. Evidence: `grep -n "N_EVAL_SEEDS"` returns `N_EVAL_SEEDS: int = 3`.

* **REQ-5** — Hard constant `N_DIRECTIONS = 2` is asserted in `code/constants_morphology.py`
  (antipodal pair 0/180 deg, inherited verbatim from t0124). Satisfied by Step 3. Evidence:
  `grep -n "N_DIRECTIONS" code/constants_morphology.py` returns `N_DIRECTIONS: int = 2`.

* **REQ-6** — Hard constant `N_GEN_MAX = 60` is asserted in `code/constants.py` and `N_GEN = 60`
  in `code/constants_morphology.py`. **This run must REACH gen 60 unless the $6 watchdog trips —
  operator-stop is NOT a legitimate termination trigger for this task.** Satisfied by Steps 3 and 9.
  Evidence: `grep -n "N_GEN_MAX\|N_GEN "` returns `N_GEN_MAX: int = 60`.

* **REQ-7** — Hard constant `COST_CAP_USD = 6.0` is asserted in `code/constants.py` and the
  `CostWatchdogTermination` is constructed with `hard_budget_usd=T0126_HARD_BUDGET_USD = 6.0`.
  Per-instance watchdog `T0126_PER_INSTANCE_WATCHDOG_USD = 5.0` ($1 buffer below the task cap).
  Satisfied by Steps 3 and 7. Evidence:
  `grep -n "COST_CAP_USD\|T0126_HARD_BUDGET_USD" code/constants.py` returns
  `COST_CAP_USD: float = 6.0`.

* **REQ-8** — Fork `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/` **verbatim** into
  `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/` and rewrite imports
  `tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.* -> tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.*`
  and the token `T0124_ -> T0126_`. Drop the t0124-specific output module
  `code/build_t0124_outputs.py` from the fork (it is t0124-task-specific glue, not protocol code).
  No algorithmic changes anywhere. Satisfied by Step 2. Evidence: `ls code/` shows ~36 forked Python
  files minus `build_t0124_outputs.py`, plus one NEW module `t0124_vs_t0126_comparator.py` added in
  Step 10.

* **REQ-9** — GA seed `T0126_SEEDS = (8929,)` is set in `code/constants.py`. The seed was drawn at
  plan-edit time via Python `secrets.randbelow(10000)` rejecting (a) multiples of 100 / 500 / 1000,
  (b) values below 100, (c) the prior-lineage seeds `{77, 441, 1524, 2247, 7755, 9354}`, and (d)
  **t0124's seed `6650` to guarantee a fresh draw**. The recorded value is `8929`. Satisfied by Step
  3\.

* **REQ-10** — Reuse per-segment `seg.ina` recording from `code/recorder.py`
  (`attach_ina_recorders_for_atp`) inherited from t0124 verbatim for soma + AIS proximal + AIS
  distal + every dendritic segment. Recording handles re-created on each `h.finitialize` call inside
  `_run_one_trial`. Satisfied by Step 4.

* **REQ-11** — Reuse `code/atp_per_spike.py` from t0124 verbatim (Sengupta 2010 recipe:
  `detect_ap_windows` at -20 mV threshold with 2 ms refractory and +/-2 ms window;
  `compute_atp_per_ap` integrating `min(I_Na, 0)` with `UM2_TO_CM2 = 1e-8` surface-area conversion;
  `compute_atp_per_spike` returning ATP molecules per spike; `compute_compartment_breakdown`
  returning `{"soma", "ais", "dendrites_total"}` dict). NO algorithmic changes; only the import path
  is rewritten. Satisfied by Step 4.

* **REQ-12** — Reuse `code/evaluator.py` from t0124 verbatim: `CellEvalResult` keeps
  `dsi_vector_sum: float` as the first F axis; `BedBV3MorphProblem._evaluate` emits
  `out["F"] = np.array([-result.dsi_vector_sum, +result.atp_per_spike_molecules])`; default
  `n_directions: int = 2`; silence guard at `pd_spikes_sum < SILENCE_PD_SPIKES_THRESHOLD = 3`
  returns `WORST_CASE_DSI = -1.0`; `mi_count_bits` is a diagnostic-only field. No algorithmic
  changes. Satisfied by Step 4.

* **REQ-13** — Reuse `code/smoke_gate.py` from t0124 verbatim: the 9-check harness with the
  Carter-Bean three-tier PASS/WARN/FAIL policy (PASS within `[3e7, 3e9] ATP/AP/cm`, WARN within
  `[1e6, 1e14]` but outside `[3e7, 3e9]`, FAIL outside `[1e6, 1e14]`). The first-principles
  canonical band `~1e8 - 1e9 ATP/AP/cm` is preserved. Only the report-header task ID is rewritten
  from t0124 to t0126. Satisfied by Steps 4 and 8.

* **REQ-14** — Provision a single Vast.ai EPYC 32-core or 64-core instance (whichever is cheapest
  at provisioning time) using the orchestrator's `/setup-remote-machine` skill. The orchestrator
  step `008_setup-machines` populates `logs/steps/008_setup-machines/machine_log.json` with the
  selected offer and hourly rate; the cost watchdog reads the rate from this file at startup. The
  Vast.ai remote must run `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`
  at provisioning time to produce the shared `nrnmech` library. The Vast.ai account balance must be
  re-verified `>= $7` immediately before launch; if balance is below `$7`, the cap is reduced to
  `balance - $1` per the task description. Satisfied by Step 6.

* **REQ-15** — Run NSGA-II via
  `code/nsga2_driver.py run_nsga2_for_seed(task_seed=8929, n_gen_override=None)` with the
  **`MaximumGenerationTermination(n_max_gen=60)` and
  `CostWatchdogTermination($5 per-instance / $6 task)` termination pair only**. Per-gen dill
  checkpoints land in `logs/steps/009_implementation/checkpoints/`, per-gen JSONL writes to
  `hv_trace.jsonl`, and pool restarts fire every 10 generations. F =
  `[-dsi, +atp_per_spike_molecules]`. **The driver is launched in the BACKGROUND** (S-0124-02
  framework concern: t0124 was operator- stopped at gen 9 because the subagent context budget ran
  out while it tailed the log). Satisfied by Step 9.

* **REQ-16** — Implementation subagent must launch NSGA-II via Claude Code's
  `run_in_background=true` bash flag (or equivalent decoupling mechanism) so that the long-running
  NEURON simulation continues even when the subagent session ends, and the subagent polls only the
  progress checkpoints (`hv_trace.jsonl`, latest dill checkpoint, heartbeat file) every 5-10 minutes
  — NOT the live training loop. **OperatorStopTermination is DISABLED for t0126**: the only
  legitimate termination triggers are `MaximumGenerationTermination` at gen 60 and
  `CostWatchdogTermination` at $5/instance or $6/task. Satisfied by Step 9.

* **REQ-17** — Write `results/data/pareto_front_seed<S>.json` and
  `results/data/all_evaluations_seed<S>.json` from the final population and the per-gen JSONL trace,
  where `<S> = 8929`. Each row contains the 68-d vector, DSI value, ATP/spike value, per-compartment
  ATP breakdown, per-direction firing rates, diagnostic cytoplasm volume, diagnostic MI. Satisfied
  by Step 9.

* **REQ-18** — Implement NEW module `code/t0124_vs_t0126_comparator.py` (~150-250 lines) that
  loads `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/pareto_front_seed6650.json` (t0124's
  partial front) and this task's full front, then produces: (a) the side-by-side Pareto chart with
  both fronts overlaid; (b) the gen-9-vs-gen-60 correlation delta (bootstrap r(DSI, ATP) from each
  front, with 95% CIs); (c) a dominance analysis indicating whether any t0124 cells are dominated by
  the t0126 front (expected if NSGA-II converged further). Satisfied by Step 10.

* **REQ-19** — Produce `results/images/pareto_front_dsi_vs_atp.png` (Pareto chart with DSI on y,
  ATP/spike on x, joint-pass region highlighted: DSI >= 0.5 AND PD-rate >= 30 Hz AND ATP <= median
  of the front). Satisfied by Step 11.

* **REQ-20** — Produce `results/images/pareto_front_t0124_vs_t0126.png` (NEW chart, side-by-side
  Pareto comparison: t0124 partial gen-9 front in one colour, t0126 full gen-60 front in another;
  axes DSI on y, ATP/spike on x; bootstrap-CI ellipses on each cell; dominated-by-t0126 cells
  annotated). Satisfied by Step 11.

* **REQ-21** — Produce `results/images/carter_bean_atp_per_ap_check.png` (distribution of ATP/AP
  across the canonical anchor cell and the top-10 Pareto cells with the first-principles canonical
  band `[1e8, 1e9] ATP/AP/cm` as horizontal reference lines and the +/-30% band shaded). Satisfied
  by Step 11.

* **REQ-22** — Produce `results/images/attwell_laughlin_signalling_budget.png` (top-N cells'
  implied signalling ATP rate (ATP/spike * PD-rate, axon-collateral-corrected) overlaid on the
  Howarth 2012 17% cortex / 21% cerebellum revised signalling-budget anchor, with the historical
  Attwell-Laughlin 2001 47% figure annotated as the legacy reference). Satisfied by Step 11.

* **REQ-23** — Produce `results/images/top50_morphologies_seed<S>.png` (top-50 morphology grid
  with FULL DENDRITE TREES per memory `feedback_top50_morphologies_full_dendrites.md`, NOT soma-only
  — the t0114 failure mode). Satisfied by Step 12.

* **REQ-24** — Produce `results/images/hv_trajectory_seed<S>.png` (hypervolume vs generation trace
  from `hv_trace.jsonl`, gen 1 through gen 60; this is the **headline new evidence vs t0124** per
  the task description). Satisfied by Step 11.

* **REQ-25** — Write `results/metrics.json` using the explicit multi-variant format with at least
  the four DSI sub-variants and ATP / diagnostic dimensions: `t0126-seed8929-best-legit` (headline
  DSI variant with `dsi_subvariant="best_legit"` and associated `atp_per_spike_molecules`,
  `pd_firing_rate_hz`, `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits` dimensions);
  `t0126-seed8929-overall-max-dsi`; `t0126-seed8929-overall-min-atp`;
  `t0126-seed8929-dsi-eq-one-count` (count of cells with DSI == 1.0 exactly). The only `metrics` key
  used is `direction_selectivity_index` (the only registered metric in `meta/metrics/` this task
  measures). All non-registered numeric outputs (`atp_per_spike_molecules`, `pd_firing_rate_hz`,
  `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits`) are reported as `dimensions` entries
  within each variant. Satisfied by Step 13.

* **REQ-26** — Build the predictions asset
  `assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph-60gen/` with: `details.json`
  (`prediction_format: "jsonl.gz"`, per-cell schema
  `{generation, cell_index, vector_68d, dsi_vector_sum, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, pd_rate_hz, nd_rate_hz, cytoplasm_volume_um3, mi_count_bits, objective_F_minimised, silence_failed_bool, legit_bool}`,
  `created_by_task: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"`,
  `metrics_at_creation: {best_dsi_legit, min_atp_per_spike, joint_pass_count, n_generations_completed, n_cells_total, final_hypervolume, final_cost_usd, stop_trigger, bootstrap_r_dsi_atp, bootstrap_r_ci_lower, bootstrap_r_ci_upper, carter_bean_verdict}`);
  a `description.md`; and `files/predictions.jsonl.gz`. Asset must pass
  `verify_predictions_asset.py`. Satisfied by Step 14.

* **REQ-27** — Build the answer asset
  `assets/answer/dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact/` answering: "Does the
  t0124 +0.806 r(DSI, ATP) correlation survive a full 60-gen replication, or is it an early-NSGA-II
  artefact?" Primary evidence: the bootstrap r(DSI, ATP) on the full t0126 final front vs the t0124
  partial gen-9 front, applied to the S-0124-01 decision rule (r > +0.5 with CI excluding zero AND
  `n >= 20` -> Carter-Bean; r < +0.3 -> artefact; in-between -> indeterminate). Satisfied by Step
  15\.

* **REQ-28** — Run the inherited DSI silence-guard regression test
  `code/test_evaluator_dsi_guard.py` (forked verbatim from t0124 with import-path rewrites only).
  Satisfied by Step 5.

* **REQ-29** — Final Pareto front size `n >= 20` on the t0126 60-gen front (per task description
  Verification Criteria); bootstrap r(DSI, ATP) computed with 95% CI on the full final front.
  Satisfied by Steps 10 and 15.

* * *

## Approach

The work is a minimum-change replication of `t0124_bedb_dsi_atp_per_spike_nsga2` with two
behavioural deltas, one dropped t0124-specific module, and one new analysis module. The t0124 code/
directory is the canonical fork point because (a) it contains the verbatim DSI silence-guarded
objective and the Sengupta 2010 ATP-per-spike recipe (b) its smoke-gate already implements the
Carter-Bean first- principles three-tier policy resolving S-0123-04 (c) its `nsga2_driver.py`
already has the background-friendly checkpoint cadence required for S-0124-02 mitigation. **The
protocol, the objectives, the substrate, the constants, the smoke-gate logic, and the evaluator are
all reused unchanged.** This is intentional: the scientific value of t0126 depends on the
experimental setup being identical to t0124 so that the only varying inputs are the GA seed and the
generation count.

**The two behavioural deltas:**

1. **Fresh GA seed.** `T0126_SEEDS = (8929,)` instead of `T0124_SEEDS = (6650,)`. The seed `8929`
   was drawn at plan-edit time via `secrets.randbelow(10000)` with a rejection loop excluding
   multiples of 100/500/1000, values below 100, and the explicit set
   `{77, 441, 1524, 2247, 7755, 9354, 6650}` (project lineage seeds plus t0124's seed). The fresh
   seed gives an independent Latin-Hypercube initial sample of the 68-d space, so the t0124
   "single-LHS-ancestry" caveat is broken by construction.

2. **60-generation completion mandate.** Operator-stop termination is REMOVED from the live
   `TerminationCollection` for t0126 (or, equivalently, the `STOP_FILE` polling is replaced with a
   no-op). The only legitimate termination triggers become
   `MaximumGenerationTermination(n_max_gen=60)` and
   `CostWatchdogTermination($5 per-instance / $6 task)`. **The implementation subagent must launch
   NSGA-II in the BACKGROUND** via Claude Code's bash `run_in_background=true` flag (or equivalent
   process-decoupling mechanism) so that the run survives the subagent session ending. The subagent
   then polls progress every 5-10 minutes via `hv_trace.jsonl` + the latest dill checkpoint, never
   tailing the live log. This is the S-0124-02 framework-level mitigation: t0124's operator-stop at
   gen 9 happened because the subagent tailed the log inside its context, the context budget ran
   out, and the operator was forced to stop the run from the orchestrator side to release the
   worktree. Decoupling the long-running NSGA-II process from any single subagent session prevents
   this failure mode.

**One dropped module:**

`code/build_t0124_outputs.py` is t0124-task-specific output glue (it writes the t0124 charts and the
t0124 predictions asset path). It is replaced by `code/build_t0126_outputs.py` derived from the same
template but pointing at t0126 paths. The dropped module is functionally substituted, not
algorithmically changed.

**One new analysis module:**

`code/t0124_vs_t0126_comparator.py` (~150-250 lines) implements the cross-comparison required by the
task description "Cross-comparison with t0124" item:

* Loads `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/pareto_front_seed6650.json` (t0124's
  partial front) and this task's full front.
* Computes bootstrap r(DSI, ATP) with 95% CIs on each front independently (reusing
  `code/bootstrap.py`).
* Renders the side-by-side Pareto chart `pareto_front_t0124_vs_t0126.png`.
* Computes the dominance set: for each t0124 cell, checks whether any t0126 cell strictly dominates
  it in (DSI, ATP) space.
* Applies the S-0124-01 decision rule to the t0126 front: `r > +0.5` with 95% CI excluding 0 AND
  `n >= 20` -> CARTER_BEAN_PENALTY; `r < +0.3` -> ARTEFACT_NULL; in-between -> INDETERMINATE.

**Recommended task types** (match `task.json`
`task_types = ["experiment-run", "data-analysis", "comparative-analysis"]`):

* **`experiment-run`** — the NSGA-II run is an experiment producing a predictions asset.
  Hypothesis (verbatim from S-0124-01): "the bootstrap r(DSI, ATP) > +0.5 with 95% CI excluding zero
  at n>=20 on the full final t0126 60-gen front (Carter-Bean penalty) OR r < +0.3 (early-NSGA-II
  artefact); indeterminate is also a legitimate scientific outcome." Independent variable: the 68-d
  parameter vector and the GA seed. Dependent variables: `dsi_vector_sum`,
  `atp_per_spike_molecules`, diagnostic
  `pd_rate_hz / nd_rate_hz / cytoplasm_volume_um3 / mi_count_bits`. Baseline: t0124's partial-front
  r(DSI, ATP) = +0.806 [0.716, 1.000] at n=5.

* **`data-analysis`** — the post-run Pareto front, the t0124-vs-t0126 side-by-side, Carter-Bean
  overlay, Howarth 2012 / Attwell-Laughlin signalling-budget overlay, top-50 morphology grid, and
  HV-trajectory plots are data-analysis steps. Per the data-analysis Planning Guidelines, only
  registered `meta/metrics/` keys may appear in `metrics.json` (custom numeric outputs go in
  `dimensions` per the multi-variant format). The four registered metrics in `meta/metrics/` are
  `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse` — only `direction_selectivity_index` applies to t0126 because the antipodal
  2-direction protocol does not produce a full angular tuning curve.

* **`comparative-analysis`** — explicit t0124-vs-t0126 cross-comparison in
  `t0124_vs_t0126_comparator.py` and the new `pareto_front_t0124_vs_t0126.png` chart. Per the
  comparative-analysis Planning Guidelines, the comparison must report both raw values and deltas;
  the comparator script does so by reporting the bootstrap r delta and the dominance count.

**Alternatives considered (and rejected):**

* **Alternative A — re-use t0124's seed `6650` and just extend the existing run.** Rejected
  because (a) the t0124 NSGA-II population state was never persisted at gen 9 in a form that
  re-instantiates cleanly on a fresh Vast.ai instance — t0124 finalised at gen 9 and the per-gen
  dill checkpoints were written but the resume path is not in the inherited `nsga2_driver.py`; (b)
  more importantly, the scientific question requires an INDEPENDENT seed to break the
  single-LHS-ancestry confound identified in the task description.

* **Alternative B — run multiple seeds in parallel and report the across-seed mean correlation.**
  Rejected because the task description explicitly mandates "one NSGA-II run, single fresh GA seed".
  The project's standing convention since t0113 is one seed per task; multi-seed averaging is itself
  a separate follow-up suggestion if the t0126 single-seed result lands in the INDETERMINATE band.

* **Alternative C — let the subagent tail the live log (t0124's pattern).** Rejected because that
  is the exact failure mode that operator-stopped t0124 at gen 9. The S-0124-02 follow-up calls out
  the subagent-session-budget issue explicitly. Background launch + periodic polling decouples the
  run from any single subagent session and is the documented mitigation.

* **Alternative D — increase `N_GEN_MAX` beyond 60 (e.g., 100) for safety margin.** Rejected
  because (a) the t0122 lineage HV-plateau pattern shows convergence around gen 50; reaching gen 60
  is sufficient to characterise the front (b) the task description's hard constraint is
  `N_GEN_MAX = 60` verbatim and changing it would violate the "verbatim replication of t0124"
  mandate.

* **Alternative E — drop the Carter-Bean smoke-gate (since it passed in t0124).** Rejected because
  the smoke-gate is a per-instance hardware sanity check, not a t0124-specific calibration. A new
  Vast.ai instance could have a subtle NEURON / MOD compilation issue that the gate catches.
  Re-running the 30-second gate is cheap insurance.

* * *

## Cost Estimation

| Item | Estimated Cost | Notes |
| --- | --- | --- |
| Vast.ai EPYC 32-core or 64-core instance (NSGA-II run, 60 gens) | $1.50 - $3.50 | At $0.15-0.40/hr for 5-9 hours of compute. t0124 spent $0.29 in 9 gens; linear scaling to 60 gens is ~$1.93, with margin for slower per-eval times under deeper-front recombinants. |
| ATP smoke-gate canonical cell evaluation | $0.05 - $0.20 | One canonical Bed B cell, full ATP recipe, on the Vast.ai instance pre-NSGA-II. |
| Per-instance teardown / unexpected charges | $0.10 - $0.50 | Buffer (kept under $1). |
| API calls (LLM inference) | $0.00 | None required. |
| **Estimated total actual cost** | **$1.65 - $4.20** | Within the $6 cap, well within the $35.12 project remaining budget. |
| **Hard cap (COST_CAP_USD)** | **$6.00** | Watchdog stops the run if exceeded. |
| **Per-instance watchdog cap (T0126_PER_INSTANCE_WATCHDOG_USD)** | **$5.00** | Leaves $1 buffer below the task cap for teardown. |

Comparison with project budget (`project/budget.json`: total $100, per-task default $8, $35.12
remaining as of 2026-05-25, no stop threshold reached): the $6 task cap is below the per-task
default and well within the $35.12 remaining project budget. The Vast.ai account balance is to be
re-verified at provisioning time; if balance is below `$7`, the cap is reduced to `(balance - $1)`
per the task description. Prior lineage spend at the same constants: t0122 = $0.50 (60 gens at 2
dirs), t0123 = ~$1 (60 gens at 4 dirs), t0124 = $0.29 (9 gens at 2 dirs). Linear scaling of t0124's
spend to 60 gens predicts $1.93 actual; with margin, $1.65 - $4.20 is the expected band.

* * *

## Step by Step

### Milestone 1 — Code Fork and Edit (Steps 1-5, local CPU)

1. **Preflight: confirm Vast.ai balance and t0124 dependency health.** Operator confirms the Vast.ai
   account balance is `>= $7` before any provisioning. Then run
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m arf.scripts.aggregators.aggregate_tasks --format json --detail full --ids t0124_bedb_dsi_atp_per_spike_nsga2`
   and confirm the returned task has `status: "completed"` and that
   `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/pareto_front_seed6650.json` exists (needed
   by `t0124_vs_t0126_comparator.py` in Step 10). If either check fails, STOP and write an
   intervention file at `intervention/preflight_failed.md` explaining the failure. Expected output:
   a log line "[preflight] vast balance >= $7 OK; t0124 status=completed OK; pareto front file
   present OK". No REQ satisfied directly (preflight only).

2. **Fork the t0124 code/ directory verbatim, drop `build_t0124_outputs.py`.** Copy every file in
   `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/` to
   `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/` EXCEPT
   `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/build_t0124_outputs.py` (t0124-specific output
   glue, replaced by `build_t0126_outputs.py` in Step 11). Files to copy: `__init__.py`,
   `anchor_classifier.py`, `anchor_definitions.py`, `apply_params.py`, `atp_per_spike.py`,
   `biological_priors.py`, `biological_scorecard.py`, `bootstrap.py`, `build_assets.py`,
   `build_cell_ais.py`, `build_pareto_plots.py`, `build_predictions_assets.py`, `build_results.py`,
   `build_top50_morphologies.py`, `constants.py`, `constants_electrophys.py`,
   `constants_morphology.py`, `cost_watchdog.py`, `cuntz_balancing_factor.py`,
   `cytoplasm_volume.py`, `dsi_atp_comparators.py`, `evaluator.py`, `extend_with_ais.py`,
   `generator_wrapper.py`, `hv_plateau_watchdog.py`, `metrics_builder.py`, `mi_estimator.py`,
   `nsga2_driver.py`, `parametric_placer.py`, `paths.py`, `random_init.py`, `recorder.py`,
   `run_seed6650.sh` (rename to `run_seed8929.sh`), `smoke_gate.py`, `sync_results_back.sh`,
   `test_evaluator_dsi_guard.py`, `trial_helpers.py`. Then run a global string substitution
   `tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code -> tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code`
   and `T0124_ -> T0126_` across all `.py` and `.sh` files (use `grep -rn "t0124\|T0124" code/` to
   confirm zero residual matches after substitution). Expected output: `ls code/` shows ~36 forked
   Python files (no `build_t0124_outputs.py`). Satisfies REQ-8.

3. **Edit `code/constants.py` and `code/constants_morphology.py` for the t0126 seed + 60-gen
   mandate.** Apply the following changes:

   * In `code/constants.py`:
     * Replace `T0124_SEEDS = (6650,)` with `T0126_SEEDS: tuple[int, ...] = (8929,)`. The seed
       `8929` is the value drawn at plan-edit time via `secrets.randbelow(10000)` rejecting (a)
       multiples of 100/500/1000, (b) values < 100, (c) lineage seeds
       `{77, 441, 1524, 2247, 7755, 9354}`, and (d) t0124's seed `6650`. Record the drawn seed value
       verbatim in `code/constants.py` as a module-level constant with a docstring noting the
       rejection criteria.
     * Replace `T0124_HARD_BUDGET_USD = 6.0` with `T0126_HARD_BUDGET_USD: float = 6.0`. Keep
       `COST_CAP_USD: float = T0126_HARD_BUDGET_USD` alias.
     * Replace `T0124_PER_INSTANCE_WATCHDOG_USD = 5.0` with
       `T0126_PER_INSTANCE_WATCHDOG_USD: float = 5.0`.
     * Preserve back-compat aliases (`T0104_*`, `T0106_*`, `T0114_*`, `T0115_*`, `T0122_*`,
       `T0124_*`) so the forked driver and cost watchdog pick up the new $6 cap correctly.
     * Confirm `_POOL_RESTART_EVERY: int = 10` is preserved verbatim from the fork (REQ-1).
     * Confirm `HV_PLATEAU_AUTO_STOP: bool = False` is preserved verbatim from the fork (REQ-2).
     * Confirm `N_GEN_MAX: int = 60` alias is preserved (REQ-6).
     * Update the module docstring to reference t0126 and explicitly state "60-generation completion
       mandate; operator-stop disabled; background-launch pattern".

   * In `code/constants_morphology.py`:
     * Keep `POP_SIZE: int = 96` (REQ-3), `N_EVAL_SEEDS: int = 3` (REQ-4), `N_DIRECTIONS: int = 2`
       (REQ-5), `N_GEN: int = 60` (REQ-6).
     * Keep `HV_UTOPIA_DSI: float = 0.7` and `HV_UTOPIA_ATP_PER_SPIKE` exactly as inherited.
     * Keep `SILENCE_PD_SPIKES_THRESHOLD: int = 3` verbatim from t0122 / t0123 / t0124 lineage.
     * Keep `WORST_CASE_DSI: float = -1.0` verbatim.

   Expected output:
   `grep -n "POP_SIZE\|N_EVAL_SEEDS\|N_DIRECTIONS\|N_GEN_MAX\|_POOL_RESTART_EVERY\|HV_PLATEAU_AUTO_STOP\|COST_CAP_USD\|T0126_SEEDS" code/constants.py code/constants_morphology.py`
   returns the expected values listed above. Satisfies REQ-1, REQ-2, REQ-3, REQ-4, REQ-5, REQ-6,
   REQ-7, REQ-9.

4. **Confirm `code/recorder.py`, `code/atp_per_spike.py`, `code/evaluator.py`, `code/smoke_gate.py`
   are reused verbatim.** No edits beyond the global import-path rewrite from Step 2. Verify by
   running
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -c "from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.atp_per_spike import compute_atp_per_spike, detect_ap_windows, compute_atp_per_ap, compute_compartment_breakdown; from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.evaluator import BedBV3MorphProblem, evaluate_68d_vector, CellEvalResult; from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.recorder import attach_ina_recorders_for_atp; from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.smoke_gate import run_smoke_gate; print('OK')"`.
   Verify the unit-conversion constant: `grep -n "UM2_TO_CM2" code/atp_per_spike.py` returns
   `UM2_TO_CM2 = 1.0e-8`. Verify the F-axis sign convention in evaluator.py:
   `grep -n 'out\["F"\]' code/evaluator.py` returns
   `out["F"] = np.array([-result.dsi_vector_sum, +result.atp_per_spike_molecules])`. Expected
   output: all imports succeed, the unit-conversion factor is `1e-8`, and the F-axis sign convention
   is preserved. Satisfies REQ-10, REQ-11, REQ-12, REQ-13.

5. **Run the inherited DSI silence-guard regression tests.** Execute
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run pytest tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/test_evaluator_dsi_guard.py -v`.
   Expected output: all 7 tests pass (silence guard at `pd_spikes_sum in {0, 1, 2}` returns
   `WORST_CASE_DSI = -1.0`; at `pd_spikes_sum == 3` returns `_vector_sum_dsi(...)`; at
   `pd_spikes_sum == 30` returns `_vector_sum_dsi(...)`; threshold constant is exactly 3;
   `_vector_sum_dsi(PD=5, ND=1)` returns 0.6666... within 1e-6). If any test fails, STOP and debug
   — failure indicates a refactor regression after the import-path rewrite. Satisfies REQ-28.

### Milestone 2 — Remote Machine Provision and Smoke-Gate (Steps 6-8, Vast.ai)

6. **Provision a single Vast.ai EPYC instance.** Orchestrator's `/setup-remote-machine` skill
   provisions a cheapest available 32-core or 64-core EPYC instance with Linux + a working Python
   3.12 + uv environment. The provisioning step `008_setup-machines` populates
   `logs/steps/008_setup-machines/machine_log.json` with the selected offer (instance ID, hourly
   rate, region, CPU/RAM specs). The cost watchdog reads the rate from this file at startup. On the
   instance, run `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` to
   produce the shared `nrnmech` library (or confirm the existing one is loadable). Confirm the
   instance can import `tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code` modules and load
   `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.mods.nrnmech` without errors. Expected
   output: `machine_log.json` exists with `selected_offer.price_per_hour` and `instance_id`; a
   bootstrap-import smoke-test prints "OK". Satisfies REQ-14.

7. **Wire the `TerminationCollection` for the 60-gen mandate.** Edit `code/nsga2_driver.py` to
   ensure the live `TerminationCollection` contains EXACTLY two terminations:
   `MaximumGenerationTermination(n_max_gen=N_GEN_MAX)` (=60) and the `CostWatchdogTermination`
   instance built from `T0126_HARD_BUDGET_USD = 6.0` and `T0126_PER_INSTANCE_WATCHDOG_USD = 5.0`.
   **`OperatorStopTermination` MUST be removed from the live collection** (or, equivalently, its
   `STOP_FILE` poll path is set to a sentinel path that never resolves). Confirm
   `HVPlateauTermination` is also absent (REQ-2). Confirm `PerGenerationPoolRestart` callback fires
   every 10 gens via `_POOL_RESTART_EVERY = 10` (REQ-1). Expected output:
   `grep -n "TerminationCollection\|OperatorStopTermination\|HVPlateauTermination\|MaximumGenerationTermination\|CostWatchdogTermination" code/nsga2_driver.py`
   shows only the two intended terminations present in the live collection. Satisfies REQ-1, REQ-2,
   REQ-7, REQ-15, REQ-16.

8. **Run the 9-check smoke-gate on the Vast.ai instance.** Execute
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.smoke_gate`.
   The harness:
   * Runs checks 1, 7, 8 (NEURON + MOD library + anchor cell + DSI sanity range + F-axis sign
     convention).
   * Runs checks 2, 3, 4, 5, 6 (silence guard, pool-restart cadence, cost-watchdog wiring,
     HV-plateau absence, hard constants).
   * Runs check 9 (Carter-Bean ATP/AP/cm three-tier policy). Writes
     `logs/steps/009_implementation/smoke_gate.json` with all 9 check verdicts and the Carter-Bean
     derivation block.

   **Validation gate (expensive operation, before NSGA-II launch)**:
   * Trivial baseline: the canonical Bed B anchor cell's per-AP AIS ATP cost must land within the
     first-principles canonical band `[1e8, 1e9] ATP/AP/cm` (geometric mean `~3e8 ATP/AP/cm`, +/-30%
     band `[3e7, 3e9]`).
   * `--limit` setting: the smoke-gate evaluates ONE canonical cell, so no `--limit` flag is needed
     (the cell evaluation itself is the limited validation run).
   * Failure condition: if check 9 reports `status: "failed"` (canonical-cell value outside
     `[1e6, 1e14]`), STOP and write an intervention file at `intervention/smoke_gate_failed.md`
     explaining the failure mode. **Do NOT proceed to NSGA-II launch on failure.** The most common
     failure for check 9 is a surface-area unit-conversion bug (would show ATP/AP at ~1e10x the
     canonical band); the second most common is missing compartments in the seg.ina record list.
   * Individual-output inspection: after the smoke-gate runs, the operator inspects 5 individual
     AP-window records from `smoke_gate.json` and verifies the per-compartment AIS ATP breakdown is
     non-zero with the expected ratios (AIS-distal > AIS-proximal > soma; dendrites varies).

   If any check FAILS, STOP. If check 9 WARNS but the measured value is in `[1e6, 1e14]`, proceed
   with the diagnostic logged. Satisfies REQ-13.

### Milestone 3 — NSGA-II Run, Background-Launched (Step 9, Vast.ai, long-running)

9. **[CRITICAL] Launch the NSGA-II run in the BACKGROUND and poll progress.** Execute the driver via
   Claude Code's bash `run_in_background=true` flag (or equivalent process-decoupling mechanism such
   as `nohup ... &`, `tmux`, or `systemd-run --scope --user`):
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.nsga2_driver --task-seed 8929 --step-id 009_implementation`.

   The driver (inherited verbatim from t0124):
   * Initialises a Latin-Hypercube random-init pool of 96 cells (Phase A) seeded by
     `T0126_SEEDS[0] = 8929`.
   * Runs NSGA-II via pymoo with default SBX crossover (eta = 15), polynomial mutation (eta = 20),
     tournament selection of size 2.
   * Pool-restart every 10 gens via `PerGenerationPoolRestart` callback (REQ-1). The first restart
     fires at gen 10 — this is the key gen-9-vs-gen-60 inflection point the task is designed to
     probe.
   * Per-gen dill checkpoints land in `logs/steps/009_implementation/checkpoints/`.
   * Per-gen JSONL writes to `logs/steps/009_implementation/hv_trace.jsonl` with HV value plus
     per-cell DSI / ATP / silence_failed / legit_bool / firing rates.
   * Cost watchdog reads `machine_log.json` hourly rate and trips at `$5` per-instance cap (REQ-7).
   * **OperatorStopTermination is DISABLED** for t0126: the `STOP_FILE` polling is bypassed
     (REQ-16).
   * Maximum-generation termination at gen 60 (REQ-6).

   **Polling pattern (S-0124-02 mitigation)**:
   * After launching the background process, the subagent records the PID + log path and then polls
     every 5-10 minutes by reading the last 50 lines of `hv_trace.jsonl` and inspecting
     `logs/steps/009_implementation/checkpoints/` modification times. **Do NOT `tail -f` the live
     log inside the subagent context** (that is the t0124 failure mode).
   * If the subagent session ends before gen 60 is reached, the background process continues
     unattended on the Vast.ai instance. The cost watchdog protects against runaway spend; the
     instance teardown step (which the orchestrator schedules separately) waits for the final
     checkpoint to land before destroying the box.

   **Validation gate (expensive operation, $1.65-$4.20 expected spend)**:

   * Baseline expectation: t0122 (DSI + cytoplasm at N_DIRECTIONS = 2) terminated cleanly at 60/60
     gens for $0.50 with HV trajectory rising monotonically through gen 50 then plateauing. t0124
     terminated prematurely at gen 9 for $0.29 with HV still ascending; linear scaling to 60 gens
     predicts $1.93 actual spend.

   * Initial gen-3 spot-check (~5-8 min into the run): the subagent inspects the last 10 records in
     `hv_trace.jsonl`. Confirm: (a) DSI values are in `[-1, 1]`; (b) ATP values are in
     `[1e6, 1e14]`; (c) silence_failed=True for SOME cells (expected — many random-init cells have
     R_PD < 3); (d) at least one cell per gen has silence_failed=False AND DSI > 0 (the optimiser
     has live signal). If after gen 3 **all** cells still have silence_failed=True, STOP the
     background process (via the cost-watchdog STOP_FILE on the Vast.ai instance OR by killing the
     PID) and inspect the spike-counter logic — do not let the optimiser burn the budget on a
     broken pipeline.

   * Failure condition: if any cell record has DSI outside `[-1, 1]` OR ATP outside `[1e6, 1e14]`,
     STOP and debug. The gen-3 spot-check is the trivial baseline gate.

   * Individual-output inspection: read 5 individual cell records from gen 3 and verify the
     `firing_hz_per_dir`, `pd_rate_hz`, `nd_rate_hz` fields are present, non-negative, and roughly
     consistent (`pd_rate_hz` corresponds to direction `0.0`, `nd_rate_hz` to direction `180.0`).

   * If the gen-3 spot-check passes, allow the run to continue. Polling cadence drops to every 15-
     30 minutes once the run is healthy. The run terminates on whichever fires first: $6 watchdog
     (unlikely at projected $1.65-$4.20) or gen 60 (expected).

   Expected output (success): the final population fitness file at
   `logs/steps/009_implementation/final_population.dill`; the HV trajectory at `hv_trace.jsonl` with
   gen 1 through gen 60 entries; the per-gen checkpoints; the
   `results/data/pareto_front_seed8929.json` and `results/data/all_evaluations_seed8929.json`
   serialised from the final population. Stop trigger recorded in `final_termination_reason.json`
   with value `"max_generations"` (preferred) or `"cost_watchdog"` (acceptable fallback). The
   trigger MUST NOT be `"operator_stop"` for t0126. Satisfies REQ-15, REQ-16, REQ-17.

### Milestone 4 — Post-Run Analysis (Steps 10-15, local CPU)

10. **Write the new module `code/t0124_vs_t0126_comparator.py`.** Functions:
    * `load_t0124_partial_front() -> ParetoFront` — loads
      `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/pareto_front_seed6650.json`. Returns a
      frozen dataclass with the 5 t0124 cells.
    * `compute_bootstrap_r_dsi_atp(*, front: ParetoFront, n_bootstrap: int = 1000) -> CorrelationCI`
      — uses `code/bootstrap.py` to compute Pearson r(DSI, ATP) with 95% percentile CI.
    * `compute_dominance_set(*, dominating_front: ParetoFront, dominated_front: ParetoFront) -> list[bool]`
      — for each cell in `dominated_front`, returns True if any cell in `dominating_front`
      Pareto-dominates it (lower or equal ATP AND higher or equal DSI, with at least one strict).
    * `classify_carter_bean_vs_artefact(*, t0126_r: CorrelationCI, t0126_n: int) -> Verdict` —
      applies the S-0124-01 decision rule. Returns one of `"CARTER_BEAN_PENALTY"` (r > +0.5 AND 95%
      CI excludes 0 AND n >= 20), `"ARTEFACT_NULL"` (r < +0.3 OR upper CI < +0.3), `"INDETERMINATE"`
      (everything else).
    * Top-level orchestrator
      `run_t0124_vs_t0126_comparison(*, t0126_pareto_path: Path, output_chart_path: Path) -> ComparisonReport`
      — produces all comparisons and saves the side-by-side chart.

    Expected output: a self-contained module with full type annotations, frozen dataclasses for
    every return type, and explicit constants for the S-0124-01 thresholds (+0.5 acceptance, +0.3
    rejection, n=20 minimum). Satisfies REQ-18, REQ-29.

11. **Produce the five core charts.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.build_pareto_plots --task-seed 8929`.
    The script loads `results/data/pareto_front_seed8929.json` (built from `final_population.dill`
    plus `hv_trace.jsonl`) and writes:

    * `results/images/pareto_front_dsi_vs_atp.png` (REQ-19) — DSI on y, ATP/spike on x, all Pareto
      cells plotted; joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz AND ATP <= median of front)
      highlighted in a distinct colour. Title: "Pareto Front: DSI vs ATP-per-Spike (t0126 60-gen,
      seed 8929)".
    * `results/images/pareto_front_t0124_vs_t0126.png` (REQ-20) — side-by-side comparison from
      `t0124_vs_t0126_comparator.run_t0124_vs_t0126_comparison`. t0124 partial gen-9 front in one
      colour, t0126 full gen-60 front in another; axes DSI on y, ATP/spike on x; bootstrap-CI
      whiskers on each cell; dominated-by-t0126 t0124 cells annotated. Title: "Pareto Front: t0124
      (gen 9 partial) vs t0126 (gen 60 full)".
    * `results/images/carter_bean_atp_per_ap_check.png` (REQ-21) — y-axis: per-AP AIS ATP in
      ATP/AP/cm units. Horizontal reference lines at the first-principles canonical band edges
      (`1e8` and `1e9 ATP/AP/cm`) with the geometric mean (`~3e8`) shown as a dashed line and the
      +/-30% band (`[3e7, 3e9]`) shaded. Scatter of the canonical anchor cell value and the top-10
      Pareto cells' AIS ATP/AP/cm with bootstrap-CI error bars.
    * `results/images/attwell_laughlin_signalling_budget.png` (REQ-22) — y-axis: implied per-cell
      signalling ATP rate (ATP/spike * PD-rate), axon-collateral-corrected. Horizontal reference
      lines at the Howarth 2012 17% cortex anchor (primary), 21% cerebellum anchor (secondary), and
      47% Attwell-Laughlin 2001 historical anchor (annotated as "legacy reference").
    * `results/images/hv_trajectory_seed8929.png` (REQ-24) — hypervolume vs generation from
      `hv_trace.jsonl`. Title: "NSGA-II Hypervolume Trajectory (seed 8929, gen 1 - gen 60)".
      Annotation of stop-trigger generation. **This is the headline new evidence vs t0124** per the
      task description.

    Expected output: five PNG files written to `results/images/` with valid axis labels, titles, and
    bootstrap-CI error bars where applicable. Satisfies REQ-19, REQ-20, REQ-21, REQ-22, REQ-24.

12. **Produce the top-50 morphology grid.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.build_top50_morphologies --task-seed 8929 --render-mode full_dendrite_trees`.
    The script loads the top-50 cells by DSI from `results/data/pareto_front_seed8929.json`,
    rebuilds each via `code/generator_wrapper.py build_cell`, and renders the full dendrite tree
    (NOT soma-only — the t0114 failure mode per memory
    `feedback_top50_morphologies_full_dendrites.md`) in a 5x10 grid with per-cell annotations
    showing DSI, ATP/spike, PD-rate. Title: "Top-50 Morphologies by DSI (t0126, seed 8929, gen 60)
    — full dendrite trees". Expected output: `results/images/top50_morphologies_seed8929.png` is a
    single high-resolution PNG with all 50 cells visibly rendered as dendrite trees. Satisfies
    REQ-23.

13. **Write `results/metrics.json` in explicit multi-variant format.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.metrics_builder --task-seed 8929`.
    The builder produces the four variants:

    * `t0126-seed8929-best-legit`: headline variant. `dimensions` include `task_seed`,
      `init_method: "lhs_random"`, `n_obj: 2`, `n_directions: 2`, `dsi_metric: "vector_sum"`,
      `dsi_silence_guard_active: true`, `silence_guard_threshold_pd_spikes: 3`, `n_eval_seeds: 3`,
      `n_generations_target: 60`, `n_generations_completed: <observed>`, `n_cells: <total>`,
      `n_legit: <legit count>`, `pool_restart_every: 10`, `hv_plateau_auto_stop_disabled: true`,
      `operator_stop_disabled: true`, `dsi_subvariant: "best_legit"`, plus the headline cell's
      `atp_per_spike_molecules`, `pd_firing_rate_hz`, `nd_firing_rate_hz`, `cytoplasm_volume_um3`,
      `mi_count_bits`. `metrics`: `{"direction_selectivity_index": <best DSI of best legit cell>}`.

    * `t0126-seed8929-overall-max-dsi`: `dsi_subvariant: "overall_max_dsi"`. Records the overall
      maximum DSI ignoring the silence guard, plus the associated cell's ATP / firing / volume / MI.

    * `t0126-seed8929-overall-min-atp`: `dsi_subvariant: "overall_min_atp"`. Records the overall
      minimum ATP/spike, plus the associated cell's DSI / firing / volume / MI.

    * `t0126-seed8929-dsi-eq-one-count`: `dsi_subvariant: "dsi_eq_one_count"`. Records the count of
      cells with DSI == 1.0 exactly (near-degenerate ND-silenced cells where R_ND = 0). `metrics`:
      `{"direction_selectivity_index": 1.0}`.

    The only registered metric key that appears in any `metrics` field is
    `direction_selectivity_index` — the only metric in `meta/metrics/` that this task can directly
    measure. Of the 4 registered metrics (`direction_selectivity_index`, `tuning_curve_hwhm_deg`,
    `tuning_curve_reliability`, `tuning_curve_rmse`), only `direction_selectivity_index` applies.
    The HWHM / reliability / RMSE metrics REQUIRE a full angular tuning sweep (8+ directions) and a
    target tuning curve; t0126 uses 2 antipodal directions and no target curve, so these three
    metrics CANNOT be measured by this task. Their omission is deliberate, not accidental, and is
    explicitly documented here. Custom non-registered numeric outputs (`atp_per_spike_molecules`,
    `pd_firing_rate_hz`, `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits`, plus the new
    `bootstrap_r_dsi_atp` and `bootstrap_r_ci_lower` / `bootstrap_r_ci_upper`) are reported as
    `dimensions` entries within each variant, NOT as top-level `metrics` keys. Format follows
    `arf/specifications/metrics_specification.md` and t0124's `results/metrics.json` exactly.
    Expected output: a valid `results/metrics.json` with 4 variants. Satisfies REQ-25.

14. **Build the predictions asset.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.build_predictions_assets --task-seed 8929`.
    The builder produces `assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph-60gen/details.json`,
    `description.md`, and `files/predictions.jsonl.gz`. `details.json` fields: `spec_version: "2"`,
    `predictions_id: "nsga2-dsi-atp-per-spike-bedb-morph-60gen"`,
    `name: "NSGA-II DSI vs ATP-per-Spike on Bed B + 14-d Morphology (60-gen replication)"`,
    `short_description: <description>`, `description_path: "description.md"`, `model_id: null`,
    `model_description: "68-d Bed B compartmental model (54-d electrophys + 14-d morphology), NEURON-backed, NSGA-II via pymoo, single GA seed=8929, 60 generations, OperatorStopTermination disabled"`,
    `dataset_ids: []`, `prediction_format: "jsonl.gz"`,
    `prediction_schema: <per-cell schema spanning generation, cell_index, vector_68d, dsi_vector_sum, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, pd_rate_hz, nd_rate_hz, cytoplasm_volume_um3, mi_count_bits, objective_F_minimised, silence_failed_bool, legit_bool>`,
    `instance_count: <total cells evaluated>`,
    `metrics_at_creation: {best_dsi_legit, min_atp_per_spike, joint_pass_count, n_generations_completed, n_cells_total, final_hypervolume, final_cost_usd, stop_trigger, bootstrap_r_dsi_atp, bootstrap_r_ci_lower, bootstrap_r_ci_upper, carter_bean_verdict}`,
    `files: [{path: "files/predictions.jsonl.gz", description: ..., format: "jsonl"}]`,
    `categories: ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell", "voltage-gated-channels"]`,
    `created_by_task: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"`, `date_created: <ISO date>`.

    Run the verificator:
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m arf.scripts.verificators.verify_predictions_asset tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen`.
    Expected output: 0 errors. Satisfies REQ-26.

15. **Build the answer asset.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.build_assets --task-seed 8929`.
    The builder produces
    `assets/answer/dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact/details.json`,
    `short_answer.md`, and `full_answer.md`.

    The question (verbatim from REQ-27): "Does the t0124 +0.806 r(DSI, ATP) correlation survive a
    full 60-gen replication, or is it an early-NSGA-II artefact?"

    Evidence channels (`answer_methods`): `["code-experiment", "papers"]` — primary evidence is
    the t0126 NSGA-II Pareto front and the t0124-vs-t0126 comparator output; secondary evidence is
    the Carter-Bean 2009 / Sengupta 2010 / Howarth 2012 / Attwell-Laughlin 2001 paper assets cited
    for context.

    Decision rule for the answer (from S-0124-01, applied by
    `t0124_vs_t0126_comparator.classify_carter_bean_vs_artefact`):
    * If `r(DSI, ATP) > +0.5` with 95% CI excluding zero AND `n >= 20` LEGIT Pareto cells -> "YES,
      the +0.806 t0124 correlation is reproduced by the full 60-gen replication; the DSGC front
      exhibits a Carter-Bean Na/K-overlap penalty (r = X.XX [CI: ..., ...] at n = N)".
    * If `r(DSI, ATP) < +0.3` (upper CI < +0.3 also acceptable) -> "NO, the t0124 +0.806 correlation
      does NOT survive a full 60-gen replication; the partial-front result was an early-NSGA-II /
      single-LHS-ancestry artefact (r = X.XX [CI: ..., ...] at n = N)".
    * If `0.3 <= r <= 0.5` OR the CI straddles +0.5 -> "INDETERMINATE: the t0126 correlation lands
      in the ambiguous band r = X.XX [CI: ..., ...] at n = N; further replication with independent
      seeds is recommended".
    * If `n_legit < 20` (analogous to t0124's 0-LEGIT outcome AND the task-description-mandated
      minimum) -> "INSUFFICIENT EVIDENCE: only <n_legit> cells passed the silence guard; the Pareto
      front structure cannot be quantitatively characterised at this sample size".

    `details.json` fields: `spec_version: "2"`,
    `answer_id: "dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact"`,
    `question: <verbatim above>`,
    `short_title: "Does t0124's +0.806 r(DSI, ATP) survive full 60-gen NSGA-II replication?"`,
    `short_answer_path: "short_answer.md"`, `full_answer_path: "full_answer.md"`,
    `categories: ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell", "voltage-gated-channels"]`,
    `answer_methods: ["code-experiment", "papers"]`,
    `source_paper_ids: [<10.1371_journal.pcbi.1000840 (Sengupta 2010), 10.1097_00004647-200110000-00001 (Attwell-Laughlin 2001), 10.1523_JNEUROSCI.1592-24.2024 (Werginz 2024), 10.1038_nn.3565 (Sivyer 2013)>]`,
    `source_task_ids: ["t0080_bedb_mobo_v3_dendritic_spike_nsga2", "t0097_multi_obj_optim", "t0122_dsi_cytoplasm_volume_nsga2", "t0123_bedb_mi_atp_per_spike_nsga2", "t0124_bedb_dsi_atp_per_spike_nsga2"]`,
    `source_urls: ["https://pmc.ncbi.nlm.nih.gov/articles/PMC2810867/", "https://pmc.ncbi.nlm.nih.gov/articles/PMC3390818/"]`,
    `confidence: "medium"` (or "high" if the t0126 correlation lands clearly inside the +0.5 / +0.3
    bands with tight CI; "low" if INDETERMINATE),
    `created_by_task: "t0126_bedb_dsi_atp_per_spike_nsga2_60gen"`, `date_created: <ISO date>`.

    Run the verificator:
    `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen`.
    Expected output: 0 errors. The `## Short Answer` section must not contain inline citations like
    `[Sengupta2010]` or `[t0124]` (citations belong in `## Sources`). Satisfies REQ-27.

* * *

## Remote Machines

One single Vast.ai EPYC instance (32-core or 64-core, whichever is cheapest at provisioning time),
Linux + Python 3.12 + uv environment. The instance must successfully compile the shared `nrnmech`
library via `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` and load the
resulting library through the t0126 bootstrap import chain. Expected provisioning time: 5-15
minutes; expected run wall-clock: 5-9 hours (60 gens at ~5-9 min per gen with the 2-direction
protocol; t0124 spent ~5.4 min per gen). Provider: Vast.ai. Cost cap: `$5` per instance (T0126
per-instance watchdog), `$6` task cap. The `/setup-remote-machine` orchestrator skill manages
provisioning; teardown is the orchestrator-managed step `010_teardown` after the run finalises.

* * *

## Assets Needed

| Asset | Source | Purpose |
| --- | --- | --- |
| `de_rosenroll_2026_dsgc` library | `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/` | Canonical Bed B DSGC NEURON cell + dendrite geometry + nrnmech.dll vendoring; `build_dsgc_cell` used by smoke-gate anchor cell. |
| `de_rosenroll_2026_dsgc_ais_dendritic_spike` library | `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/` | 54-d ParameterVector + `apply_parameter_vector` + tiered channel write loops + AIS extension + compiled MOD pack (`nav16t80`, `napt80`, `nart80`, etc.). |
| `procedural_dsgc_morphology_generator` library | `tasks/t0090_morphology_generator_diversity_test/assets/library/` | 14-d `MorphologyParams` dataclass + `MorphologyResult` + `PARAM_BOUNDS`. |
| `procedural_dsgc_morphology_generator_fix` library | `tasks/t0092_diagnose_morphology_generator_silence/assets/library/` | Canonical patched `generate_fixed_morphology` + `insert_baseline_channels`. |
| t0124 `code/` directory | `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/` | Fork base: ~36 Python modules including `atp_per_spike.py`, `recorder.py`, `evaluator.py`, `nsga2_driver.py`, `smoke_gate.py`, `test_evaluator_dsi_guard.py`, `dsi_atp_comparators.py`. |
| t0124 partial Pareto front | `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/pareto_front_seed6650.json` | Side-by-side comparison input for `t0124_vs_t0126_comparator.py`. |
| t0122 results data | `tasks/t0122_dsi_cytoplasm_volume_nsga2/results/data/pareto_front_*.json` | Cytoplasm-vs-DSI Pareto front for the Cuntz balancing-factor cross-reference in `dsi_atp_comparators.py` (inherited from t0124). |
| Sengupta 2010 paper asset | `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/` | Cross-cell alpha table for Carter-Bean smoke-gate calibration cited in compare_literature.md. |
| Attwell-Laughlin 2001 paper asset | `tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/` | Historical 47% signalling-ATP-budget anchor and the 18% somatodendritic / 82% axon-collateral share for the 5x truncation correction. |
| Werginz 2024 paper asset | `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/` | Mouse alpha-RGC AIS Nav density (1300 mS/cm^2) for the Carter-Bean smoke-gate first-principles derivation. |
| Sivyer 2013 paper asset | `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/` | Dendritic-spike-driven DSI mechanism reference for the answer asset's mechanism classification. |
| Howarth 2012 (NOT in corpus) | `https://pmc.ncbi.nlm.nih.gov/articles/PMC3390818/` | Cited in compare_literature.md for the REVISED 17% cortex / 21% cerebellum signalling-ATP budget; URL-cited only. |
| Carter-Bean 2009 (NOT in corpus) | `https://pmc.ncbi.nlm.nih.gov/articles/PMC2810867/` | Cited in compare_literature.md for the alpha=1.25 reference; URL-cited only. |

* * *

## Expected Assets

| Asset Type | Asset ID | Description |
| --- | --- | --- |
| `predictions` | `nsga2-dsi-atp-per-spike-bedb-morph-60gen` | One predictions asset with one row per evaluated cell containing the 68-d vector, `dsi_vector_sum`, `atp_per_spike_molecules`, `atp_per_ap_molecules`, per-compartment ATP breakdown, per-direction firing rates, diagnostic `cytoplasm_volume_um3` and `mi_count_bits`, the F vector, silence-guard flag, and joint-pass flag. Per-cell records compressed to `files/predictions.jsonl.gz`. |
| `answer` | `dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact` | One answer asset answering "Does the t0124 +0.806 r(DSI, ATP) correlation survive a full 60-gen replication, or is it an early-NSGA-II artefact?" Confidence label set by the bootstrap CI on the joint DSI / ATP correlation per the S-0124-01 decision rule. |

Both counts match `task.json` `expected_assets`: `{"predictions": 1, "answer": 1}`.

* * *

## Time Estimation

| Phase | Estimated Wall-Clock |
| --- | --- |
| Research (papers + internet + code) | Skipped — verbatim replication of t0124, inherits t0124 research. |
| Planning (this document) | ~1 hour. |
| Code fork + edits (Steps 1-5, local) | ~1-2 hours including the regression test suite. |
| Setup-remote-machine + provisioning (Step 6) | ~30 minutes (cheapest available EPYC offer). |
| Termination-collection edit + smoke-gate (Steps 7-8) | ~30 minutes. |
| NSGA-II run, background-launched (Step 9) | ~5-9 hours wall-clock on 32-core EPYC; ~4-7 hours on 64-core. Background launch decouples from subagent session; polling cadence 5-30 min. Expected stop trigger: `max_generations` at gen 60. |
| Post-run analysis + assets (Steps 10-15) | ~2-3 hours local. |
| Orchestrator-managed reporting steps (results_summary.md / results_detailed.md / costs.json / suggestions.json / compare_literature.md) | ~1-2 hours local. |
| **Total task wall-clock** | **~12-18 hours**, dominated by the NSGA-II run. The subagent-session wall-clock is much shorter because the NSGA-II run is decoupled to the background. |

* * *

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Subagent session ends before gen 60 reached (operator-stop equivalent failure mode from t0124) | Medium | Without background launch, would force premature termination | **The background-launch pattern in Step 9 is the primary mitigation.** NSGA-II runs as a detached process on the Vast.ai instance; the subagent polls progress checkpoints rather than tailing the live log. If the subagent session does end, the NSGA-II process continues; a subsequent subagent (or the orchestrator's teardown step) picks up the final population from the latest dill checkpoint. |
| Surface-area unit-conversion bug after import-path rewrite (Sengupta-recipe regression) | Very Low | Smoke-gate check 9 fails; NSGA-II launch aborted | Smoke-gate check 9 with the three-tier policy catches it before NSGA-II. Verify `UM2_TO_CM2 = 1e-8` (Step 4). If gate fails, debug per-segment area computation and confirm `seg.area() * 1e-8` is used as cm^2 conversion. The recipe is inherited verbatim from t0124 (already verified there). |
| Smoke-gate check 9 WARNS (canonical cell measurement outside `[3e7, 3e9]` but inside `[1e6, 1e14]`) | Low | Diagnostic noise; the run proceeds but the Carter-Bean comparison layer reports a wider-than-expected fold-difference | Log the diagnostic in `smoke_gate.json`; the answer asset notes this in the limitations section. |
| All Pareto cells trigger the DSI silence guard (R_PD < 3 for every cell, every seed; analogous to t0124's outcome at gen 9) | Low-Medium | n_legit < 20; the answer asset reports "Insufficient evidence" | The answer asset's "Insufficient evidence" escape clause is pre-wired. Bootstrap CI on the unfiltered front is reported regardless. Gen-3 spot-check in Step 9 catches early; if all cells silence at gen 3, STOP the background process and debug. The 60-gen run gives the optimiser 6x more chances to find legit cells than t0124 had. |
| Vast.ai instance crashes or loses network mid-run | Low-Medium | Partial Pareto front; need to resume from last checkpoint | Per-gen dill checkpoints land in `logs/steps/009_implementation/checkpoints/`. The background process writes a heartbeat every 60s; if no heartbeat for >5 min, the subagent's polling logic flags the failure and the orchestrator's teardown step provisions a fresh instance from the latest checkpoint via `nsga2_driver.py --resume-from-checkpoint <path>`. |
| Cost watchdog trips at `$5` per-instance ($6 task) before gen 60 | Low (t0122 = $0.50, t0123 = $1, t0124 (9 gens) = $0.29; linear-scaling 60-gen prediction = $1.93) | Pareto front truncated; analysis layer runs on partial data | Cost watchdog writes intervention markdown; the analysis layer adapts to whatever generation count was reached. If the watchdog trips at gen < 20, STOP and investigate — likely a per-trial wall-clock regression. The answer asset's "Insufficient evidence" escape clause covers n_legit < 20. |
| The t0126 60-gen front lands in the INDETERMINATE band (0.3 <= r <= 0.5 OR CI straddles +0.5) | Medium (intrinsic to single-seed Bernoulli-like outcomes) | Cannot conclusively answer Carter-Bean vs artefact | The answer asset's INDETERMINATE branch is pre-wired with the recommendation to run a multi-seed follow-up. This is a legitimate scientific outcome, not a failure — the task description treats INDETERMINATE as a valid verdict ("Anything in between: INDETERMINATE; report and recommend further replication"). |
| Background-launch mechanism not available in the subagent's runtime (Claude Code session) | Low | Subagent must fall back to foreground launch and the t0124 failure mode re-emerges | Three documented fallback mechanisms: (a) `nohup ... &` on the Vast.ai instance (POSIX standard, always available); (b) `tmux` detached session (standard on Vast.ai images); (c) `systemd-run --scope --user` (modern Linux). Step 9 explicitly lists these as alternatives to Claude Code's `run_in_background=true` so the subagent has options. |
| `code/test_evaluator_dsi_guard.py` fails after the import-path rewrite | Low | Step 5 STOPs; needs debug of the DSI silence-guard regression test | Inherited verbatim from t0124 with only import-path rewrites — the tests cover pure-Python logic with no NEURON dependency. Debug by running `pytest -v` on individual tests. |
| GA seed `8929` coincidentally hits a parameter-space dead zone | Low | A second NSGA-II re-run with a different seed becomes necessary | Single-seed convention is inherited from t0113 / t0114 / t0115 / t0122 / t0123 / t0124 lineage. If the result is INDETERMINATE due to a seed-specific basin, the answer asset's recommendation triggers a multi-seed follow-up task. |

* * *

## Verification Criteria

* **Hard-constants verification**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -c "from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code import constants; from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code import constants_morphology; assert constants._POOL_RESTART_EVERY == 10; assert constants.HV_PLATEAU_AUTO_STOP is False; assert constants_morphology.POP_SIZE == 96; assert constants_morphology.N_EVAL_SEEDS == 3; assert constants_morphology.N_DIRECTIONS == 2; assert constants.N_GEN_MAX == 60; assert constants.COST_CAP_USD == 6.0; assert constants_morphology.SILENCE_PD_SPIKES_THRESHOLD == 3; assert constants.T0126_SEEDS == (8929,); assert constants.T0126_SEEDS[0] != 6650, 'must differ from t0124 seed'; print('OK')"`.
  Expected output: `OK`. Covers REQ-1, REQ-2, REQ-3, REQ-4, REQ-5, REQ-6, REQ-7, REQ-9.

* **DSI silence-guard regression tests pass**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run pytest tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/test_evaluator_dsi_guard.py -v`.
  Expected output: 7 tests pass, 0 failed. Covers REQ-28.

* **OperatorStopTermination is NOT in the live TerminationCollection**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -c "import inspect; from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code import nsga2_driver; src = inspect.getsource(nsga2_driver); assert 'OperatorStopTermination(' not in src or 'STOP_FILE = pathlib.Path(\"/dev/null/never\")' in src, 'OperatorStopTermination must be removed or sentinel-pathed'; assert 'MaximumGenerationTermination(' in src; assert 'CostWatchdogTermination(' in src; print('OK')"`.
  Expected output: `OK`. Covers REQ-15, REQ-16.

* **Smoke-gate check 9 PASSES or WARNS**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.smoke_gate`
  on the Vast.ai instance. Inspect `logs/steps/009_implementation/smoke_gate.json`. All 9 checks
  must report `"passed": true` OR `"status": "warning"`. The Carter-Bean derivation block must
  contain the canonical band `[1e8, 1e9] ATP/AP/cm`, the geometric mean `~3e8`, and the +/-30% band
  `[3e7, 3e9]`. Covers REQ-13.

* **NSGA-II run terminates at gen 60 (or cost watchdog)**: Inspect
  `logs/steps/009_implementation/final_termination_reason.json`. The trigger MUST be
  `"max_generations"` or `"cost_watchdog"` — **NOT `"operator_stop"`**. Generation count must be
  `>= 20` (else the substrate is broken). Final hypervolume must be `> 0`. Covers REQ-6, REQ-15,
  REQ-16.

* **Background-launch evidence in logs**: Run
  `grep -nE "run_in_background|nohup|tmux|systemd-run" logs/steps/009_implementation/`. Expected: at
  least one match documenting the background-launch mechanism used. Covers REQ-16.

* **Pareto front size n >= 20**: Run
  `uv run python -u -c "import json; rows = [json.loads(l) for l in open('tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json').readlines() if l.strip()] if open('tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json').read().lstrip().startswith('{') else json.load(open('tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json')); print('n=', len(rows))"`
  (or equivalent JSON-format-aware loader). Expected: `n >= 20` for a healthy 60-gen run. If n < 20,
  the answer asset's "Insufficient evidence" branch triggers. Covers REQ-17, REQ-29.

* **Pareto front and all-evaluations JSON dumps exist and are well-formed**: Run
  `ls tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/all_evaluations_seed8929.json`
  and verify each file is valid JSON with `>= 1` row. Each row must contain the 68-d vector, DSI
  value, ATP value, per-compartment ATP breakdown, per-direction firing rates, diagnostic volume /
  MI. Covers REQ-17.

* **All six required charts exist and are non-empty**: Run
  `ls tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/images/pareto_front_dsi_vs_atp.png tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/images/pareto_front_t0124_vs_t0126.png tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/images/carter_bean_atp_per_ap_check.png tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/images/attwell_laughlin_signalling_budget.png tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/images/top50_morphologies_seed8929.png tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/images/hv_trajectory_seed8929.png`.
  Each file must be non-empty. The top-50 morphology grid must visibly render FULL DENDRITE TREES
  (manual inspection). Covers REQ-19, REQ-20, REQ-21, REQ-22, REQ-23, REQ-24.

* **`metrics.json` validates against the registered metric registry**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m arf.scripts.verificators.verify_metrics tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen`.
  Expected output: 0 errors. The four variants must be present (best_legit, overall_max_dsi,
  overall_min_atp, dsi_eq_one_count), each with `direction_selectivity_index` as the only metric key
  and the non-registered numeric outputs in `dimensions`. Covers REQ-25.

* **Predictions asset passes verificator**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m arf.scripts.verificators.verify_predictions_asset tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen`.
  Expected output: 0 errors, optional warnings tolerated. Covers REQ-26.

* **Answer asset passes verificator**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0126_bedb_dsi_atp_per_spike_nsga2_60gen -- uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen`.
  Expected output: 0 errors, optional warnings tolerated. The `## Short Answer` section must contain
  the verdict word (`YES`, `NO`, `INDETERMINATE`, or `INSUFFICIENT EVIDENCE`) per the decision rule.
  Covers REQ-27.

* **t0124-vs-t0126 cross-comparison output exists**: Run
  `ls tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/images/pareto_front_t0124_vs_t0126.png`
  and confirm the side-by-side chart was rendered. The chart must show both t0124's gen-9 partial
  front and t0126's gen-60 full front on the same axes. Covers REQ-18, REQ-20.

* **Requirement coverage cross-check**: Manually verify that every `REQ-1` through `REQ-29` is
  referenced by at least one step in `## Step by Step`. The mapping is: REQ-1 / REQ-2 by Steps 3, 7;
  REQ-3 / REQ-4 / REQ-5 / REQ-6 by Step 3; REQ-7 by Steps 3, 7; REQ-8 by Step 2; REQ-9 by Step 3;
  REQ-10 / REQ-11 / REQ-12 / REQ-13 by Step 4; REQ-14 by Step 6; REQ-15 / REQ-16 by Steps 7, 9;
  REQ-17 by Step 9; REQ-18 by Step 10; REQ-19 / REQ-20 / REQ-21 / REQ-22 / REQ-24 by Step 11; REQ-23
  by Step 12; REQ-25 by Step 13; REQ-26 by Step 14; REQ-27 by Step 15; REQ-28 by Step 5; REQ-29 by
  Steps 10, 15. All 29 requirements are mapped. This criterion is the requirement- coverage check
  mandated by the planning skill `## Done When`.

* * *

## Alternative Approaches Considered

The five rejected alternatives are documented in `## Approach`. Briefly:

* A. Re-use t0124's seed `6650` and extend the existing run — rejected; resume path not in
  inherited driver, and the scientific question requires an independent seed to break the single-
  LHS-ancestry confound.
* B. Run multiple seeds in parallel — rejected; task description mandates "one NSGA-II run, single
  fresh GA seed".
* C. Let the subagent tail the live log (t0124's pattern) — rejected; this is the exact failure
  mode that operator-stopped t0124 at gen 9.
* D. Increase `N_GEN_MAX` beyond 60 — rejected; violates the "verbatim replication of t0124"
  mandate, and t0122 lineage shows HV convergence around gen 50.
* E. Drop the Carter-Bean smoke-gate — rejected; the gate is a per-instance hardware sanity check,
  not t0124-specific calibration.

* * *

## Architecture (Data Flow)

```text
[Vast.ai EPYC instance]
      |
      v
+-----------------------------+
| Step 6: provision; nrnivmodl on t0080/mods/                       |
+-----------------------------+
      |
      v
+-----------------------------+
| Step 7: wire TerminationCollection (no OperatorStop)              |
+-----------------------------+
      |
      v
+-----------------------------+
| Step 8: smoke_gate.py 9 checks (Carter-Bean 1e8-1e9 band)         |
+-----------------------------+
      |
      v PASS / WARN
      |
+-----------------------------+
| Step 9: nsga2_driver.py --task-seed 8929 --step-id 009            |
|         LAUNCHED IN BACKGROUND (S-0124-02 mitigation)             |
|  - LHS random-init pop=96 seeded by 8929                          |
|  - 60 gens max, pool restart every 10 gens                        |
|  - per-gen: hv_trace.jsonl + dill checkpoint + heartbeat          |
|  - F = [-DSI, +ATP_per_spike] minimised                           |
|  - cost watchdog $5 per-instance / $6 task                        |
|  - NO operator-stop; max-gen OR watchdog only                     |
|  - Subagent polls every 5-30 min (no tail -f)                     |
+-----------------------------+
      |
      v gen 60 reached OR watchdog trip
      |
+-----------------------------+
| Steps 10-15: post-run analysis (local CPU)                        |
|  - t0124_vs_t0126_comparator.py (NEW, side-by-side + dominance)   |
|  - build_pareto_plots.py (5 charts incl. pareto_t0124_vs_t0126)   |
|  - build_top50_morphologies.py (FULL DENDRITE TREES)              |
|  - metrics_builder.py (4 variants)                                |
|  - build_predictions_assets.py + verify_predictions_asset         |
|  - build_assets.py (answer) + verify_answer_asset                 |
+-----------------------------+
      |
      v
[Orchestrator handles teardown / results_summary.md / costs.json / etc.]
```
