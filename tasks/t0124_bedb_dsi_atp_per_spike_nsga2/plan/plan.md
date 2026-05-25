---
spec_version: "2"
task_id: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_completed: "2026-05-25"
status: "complete"
---
# Plan: NSGA-II Maximising DSI and Minimising ATP-per-Spike (Bed B + 14-d Morph)

## Objective

Fork the t0123 68-d Bed B + 14-d morphology NSGA-II substrate end-to-end and swap both optimised
objectives: drop mutual information (MI) as the headline function objective and replace it with the
silence-guarded antipodal direction selectivity index (DSI = `(R_PD - R_ND) / (R_PD + R_ND)` with
`R_PD >= 3` PD-spike silence guard, t0122 convention); keep the Sengupta et al. 2010 ATP-per-spike
recipe verbatim from t0123 as the energy cost objective
(`N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int(I_Na^inward) dt`, lower is better). Halve
the direction count from t0123's 4 angles (0/90/180/270 deg) to t0122's antipodal pair (0/180 deg)
because DSI only needs one PD-ND pair and ATP-per-spike is direction-independent under per-spike
normalisation. Run one NSGA-II with one GA seed (drawn via `secrets.randbelow(10000)` at edit time,
avoiding round-ish numbers and prior-lineage seeds 77 / 441 / 1524 / 2247 / 7755 / 9354), pop=96,
N_EVAL_SEEDS=3, N_DIRECTIONS=2, `_POOL_RESTART_EVERY=10`, `HV_PLATEAU_AUTO_STOP=False`,
N_GEN_MAX=60, `COST_CAP_USD=6.0` on a single Vast.ai EPYC instance. Before launch, run the Carter
and Bean 2009 ATP/AP/cm AIS smoke-gate (within 30% of canonical reference) and re-derive the
canonical mM-mol/cm value from first principles in this plan to resolve follow-up S-0123-04.

**Done** means: (1) the run terminates cleanly via operator-stop, the $6 cost-watchdog cap, or the
60-gen ceiling; (2) one predictions asset `nsga2-dsi-atp-per-spike-bedb-morph` is written with
per-cell 68-d vectors, F = `[-dsi_best_legit, +atp_per_spike_molecules]`, per-direction firing, DSI
variants, per-compartment ATP breakdown, and diagnostic PD-rate / ND-rate / cytoplasm volume / MI;
(3) one answer asset `dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin` is written; (4)
`results/metrics.json` registers the chosen variants in the explicit multi-variant format; (5) the
seven required charts and the Pareto / all-evaluations JSON dumps are saved; (6) the Carter-Bean
smoke-gate passes within 30% on the canonical anchor cell before NSGA-II launch.

* * *

## Task Requirement Checklist

Operative task text quoted verbatim from `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/task.json` and
the resolved long description at `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/task_description.md`:

```text
Name: NSGA-II maximising DSI and minimising ATP-per-spike (Bed B + 14-d morph)

Short description: 68-d NSGA-II on Bed B + 14-d morphology, 2-objective DSI vs
ATP-per-spike (Sengupta 2010). 1 GA seed, pop=96, N_EVAL_SEEDS=3, 2-direction
protocol, $6 cap.

Dependencies: t0024, t0080, t0090, t0092, t0097, t0106, t0115, t0120, t0122,
t0123.
Expected assets: 1 predictions, 1 answer.
Task types: experiment-run, data-analysis, answer-question.
Source suggestion: S-0097-02.

Hard Constraints (non-negotiable, reproduced in code/constants.py):
* _POOL_RESTART_EVERY = 10  (10-gen rule)
* HV_PLATEAU_AUTO_STOP = False  (disabled per project policy)
* POP_SIZE = 96
* N_EVAL_SEEDS = 3
* N_DIRECTIONS = 2  (antipodal pair 0/180; halved from t0123's 4)
* N_GEN_MAX = 60
* COST_CAP_USD = 6.0  (Vast.ai balance >= $7, $1 teardown buffer)

DSI Recipe (silence-guarded ratio):
R_PD = mean spike count over N_EVAL_SEEDS trials at 0 deg
R_ND = mean spike count over N_EVAL_SEEDS trials at 180 deg
DSI = (R_PD - R_ND) / (R_PD + R_ND)        if R_PD >= 3 spikes
DSI = -1.0                                  if R_PD <  3 spikes (silence guard)

* Headline DSI variant: `best_legit` (top DSI among cells passing the guard).
* Tracked DSI variants in metrics.json: best_legit, overall_max, dsi_eq_one_count.

ATP-per-Spike Recipe (Sengupta 2010, inherited from t0123 verbatim):
N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int(I_Na^inward) dt
* Record seg.ina at simulation dt for soma + AIS proximal + AIS distal +
  all dendritic segments. FULL mode only.
* AP windows: somatic Vm threshold crossing at -20 mV, +/-2 ms around peak,
  2 ms refractory between detections.
* Per-AP per-compartment charge: integrate min(I_Na, 0) over AP window in
  seconds, multiply by seg.area_cm2; ATP = Q / (e * 3).
* Sum across compartments, then divide total ATP by total spikes across all
  FULL-mode trials -> ATP molecules per spike (headline, LOWER IS BETTER).
* If total spike count == 0: atp_per_spike = +inf (sentinel).

Carter-Bean 2009 smoke-gate (inherited from t0123, S-0123-04 follow-up):
* Re-derive the canonical ATP/AP/cm value from first principles in plan/plan.md.
* ATP/AP/cm at AIS on canonical Bed B cell must be within 30% of the re-derived
  reference; abort NSGA-II launch on failure.

Expected outputs:
* assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph/
* assets/answer/dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin/
* results/data/pareto_front_seed*.json
* results/data/all_evaluations_seed*.json
* results/images/pareto_front_dsi_vs_atp.png
* results/images/carter_bean_atp_per_ap_check.png
* results/images/attwell_laughlin_signalling_budget.png
* results/images/top50_morphologies_seed*.png (full dendrite trees)
* results/images/hv_trajectory_seed*.png

Verification Criteria (from task_description.md):
* Hard constants asserted in code/constants.py at module import.
* Carter-Bean smoke gate passes within 30% on canonical anchor cell.
* DSI silence-guard threshold == 3 PD spikes; cells below get DSI = -1.
* metrics.json registers direction_selectivity_index (variants best_legit /
  overall_max / dsi_eq_one_count), plus diagnostic dimensions
  atp_per_spike_molecules, pd_firing_rate_hz, nd_firing_rate_hz,
  cytoplasm_volume_um3, mi_count_bits.
* Predictions asset passes verify_predictions_asset.
* compare_literature.md compares the front to Carter-Bean 2009, the REVISED
  Howarth 2012 17% cortex / 21% cerebellum signalling-ATP budget (NOT the
  Attwell-Laughlin 2001 47% original), and Cuntz 2010 balancing-factor band
  [0.2, 0.7] (cross-reference to t0122).
* Answer asset states whether the DSGC front shows a Carter-Bean Na/K-overlap
  penalty with explicit quantitative comparison and bootstrap CI.

GA seed: secrets.randbelow(10000); avoid round numbers and lineage seeds
77 / 441 / 1524 / 2247 / 7755 / 9354.
```

Decomposed requirements (each step in `## Step by Step` cites the `REQ-*` items it satisfies):

* **REQ-1** — Hard constant `_POOL_RESTART_EVERY = 10` is asserted in `code/constants.py` at
  module import (project's 10-gen rule per memory `feedback_nsga2_pool_restart_every_10.md`). The
  `PerGenerationPoolRestart` callback fires every 10 gens in `code/nsga2_driver.py`. Satisfied by
  Steps 3 and 5. Evidence: `grep -n "_POOL_RESTART_EVERY" code/constants.py` returns
  `_POOL_RESTART_EVERY: int = 10`.

* **REQ-2** — Hard constant `HV_PLATEAU_AUTO_STOP = False` is asserted in `code/constants.py` and
  the live `TerminationCollection` in `code/nsga2_driver.py` does NOT contain `HVPlateauTermination`
  (`hv_plateau_watchdog.py` is importable for the smoke-gate introspection check only). Satisfied by
  Steps 3 and 5. Evidence:
  `grep -n "HV_PLATEAU_AUTO_STOP\|HVPlateauTermination" code/constants.py code/nsga2_driver.py`
  shows `HV_PLATEAU_AUTO_STOP: bool = False` and `HVPlateauTermination` absent from the active
  collection.

* **REQ-3** — Hard constant `POP_SIZE = 96` is asserted in `code/constants_morphology.py` and
  re-exported by `code/constants.py`. Satisfied by Step 3. Evidence: `grep -n "POP_SIZE"` returns
  `POP_SIZE: int = 96`.

* **REQ-4** — Hard constant `N_EVAL_SEEDS = 3` is asserted in `code/constants_morphology.py`.
  Satisfied by Step 3. Evidence: `grep -n "N_EVAL_SEEDS"` returns `N_EVAL_SEEDS: int = 3`.

* **REQ-5** — Hard constant `N_DIRECTIONS = 2` is asserted in `code/constants_morphology.py`
  (halved from t0123's 4 to t0122's 2 antipodal pair). The 2 angles are 0 deg (PD) and 180 deg (ND),
  generated by the existing
  `angles_deg = [float(d) * (360.0 / n_directions) for d in range(n_directions)]` formula in
  `evaluator.py`. Satisfied by Step 3. Evidence:
  `grep -n "N_DIRECTIONS" code/constants_morphology.py` returns `N_DIRECTIONS: int = 2`.

* **REQ-6** — Hard constant `N_GEN_MAX = 60` is asserted in `code/constants.py` and `N_GEN = 60`
  in `code/constants_morphology.py`. Satisfied by Step 3. Evidence: `grep -n "N_GEN_MAX\|N_GEN "`
  returns `N_GEN_MAX: int = 60`.

* **REQ-7** — Hard constant `COST_CAP_USD = 6.0` is asserted in `code/constants.py` and the
  `CostWatchdogTermination` is constructed with `hard_budget_usd=T0124_HARD_BUDGET_USD = 6.0`.
  Per-instance watchdog `T0124_PER_INSTANCE_WATCHDOG_USD = 5.0` ($1 buffer below the task cap).
  Satisfied by Steps 3 and 5. Evidence:
  `grep -n "COST_CAP_USD\|T0124_HARD_BUDGET_USD" code/constants.py` returns
  `COST_CAP_USD: float = 6.0`.

* **REQ-8** — Fork `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/` verbatim into
  `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/` and rewrite imports
  `tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.* -> tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.*`.
  Drop `code/post_hoc_strong_bialek.py` from the fork (MI-specific scaffolding, no value for t0124).
  Satisfied by Step 2. Evidence: `ls code/` shows ~35 forked Python files minus
  `post_hoc_strong_bialek.py`, plus one NEW module `dsi_atp_comparators.py` added in Step 12.

* **REQ-9** — GA seed `T0124_SEEDS = (<drawn_seed>,)` is set in `code/constants.py`. The seed is
  drawn at edit time via `secrets.randbelow(10000)` rejecting round-ish multiples of 500 / 1000 and
  prior-lineage seeds (77, 441, 1524, 2247, 7755, 9354). Satisfied by Step 3.

* **REQ-10** — Reuse per-segment `seg.ina` recording from `code/recorder.py`
  (`attach_ina_recorders_for_atp`) inherited from t0123 verbatim for soma + AIS proximal + AIS
  distal + every dendritic segment. Recording handles re-created on each `h.finitialize` call inside
  `_run_one_trial`. Satisfied by Step 4.

* **REQ-11** — Reuse `code/atp_per_spike.py` from t0123 verbatim (Sengupta 2010 recipe:
  `detect_ap_windows` at -20 mV threshold with 2 ms refractory and +/-2 ms window;
  `compute_atp_per_ap` integrating `min(I_Na, 0)` with `UM2_TO_CM2 = 1e-8` surface-area conversion;
  `compute_atp_per_spike` returning ATP molecules per spike; `compute_compartment_breakdown`
  returning `{"soma", "ais", "dendrites_total"}` dict). NO algorithmic changes; only the import path
  is rewritten. Satisfied by Step 4.

* **REQ-12** — Promote DSI from t0123's TRACKED DIAGNOSTIC to t0124's HEADLINE OPTIMISED
  OBJECTIVE. Modify `code/evaluator.py`: (a) `CellEvalResult` keeps `dsi_vector_sum: float` and
  `silence_failed: bool` but `dsi_vector_sum` is now the FIRST F axis; (b) rewrite
  `BedBV3MorphProblem._evaluate` to emit
  `out["F"] = np.array([-result.dsi_vector_sum, +result.atp_per_spike_molecules])` (DSI negated
  because maximised; ATP NOT negated because minimised); (c) `evaluate_68d_vector` default
  `n_directions: int = 2` (was 4); (d) keep the silence guard at `pd_spikes_sum < 3` per t0122
  convention (inherited from `SILENCE_PD_SPIKES_THRESHOLD = 3`); (e) demote `mi_count_bits` from any
  F position to a diagnostic field on `CellEvalResult`. Satisfied by Step 6.

* **REQ-13** — Edit `code/smoke_gate.py` for the F-axis update + Carter-Bean first-principles
  derivation. Specifically: (a) check 7 (sanity range on objectives) becomes `DSI in [-1, 1]` and
  `ATP in [1e6, 1e14]` (replaces the t0123 `MI in [0, 2]` sanity check); (b) check 8
  (BedBV3MorphProblem._evaluate F-axis sign convention) becomes `F[0] = -DSI`, `F[1] = +ATP`
  (replaces t0123's `F[0] = -MI`); (c) check 9 (Carter-Bean ATP/AP/cm) is rebuilt around the
  first-principles derivation from this plan (see Approach below) and the typo-corrected reference
  value replaces the t0123 `2.41e21 ATP/cm` figure. The `[1e6, 1e14]` physically-plausible fallback
  band is retained. Other 6 checks (anchor PD-rate, ratio DSI synthetic sanity, silence guard,
  pool-restart cadence, cost-watchdog wiring, HV-plateau absent from live collection) are unchanged.
  Satisfied by Step 8.

* **REQ-14** — Provision a single Vast.ai EPYC 32-core or 64-core instance (whichever is cheapest
  at provisioning time) using the orchestrator's `/setup-remote-machine` skill. The orchestrator
  step `008_setup-machines` populates `logs/steps/008_setup-machines/machine_log.json` with the
  selected offer and hourly rate; the cost watchdog reads the rate from this file at startup. The
  Vast.ai remote must run `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`
  at provisioning time to produce the shared `nrnmech` library. Satisfied by Step 9.

* **REQ-15** — Run NSGA-II via
  `code/nsga2_driver.py run_nsga2_for_seed(task_seed=<drawn>, n_gen_override=None)` with the
  operator-stop / cost-watchdog / 60-gen termination triple. Per-gen dill checkpoints land in
  `logs/steps/009_implementation/checkpoints/`, per-gen JSONL writes to `hv_trace.jsonl`, and pool
  restarts fire every 10 generations. F = `[-dsi, +atp_per_spike_molecules]`. Satisfied by Step 10.

* **REQ-16** — Write `results/data/pareto_front_seed<S>.json` and
  `results/data/all_evaluations_seed<S>.json` from the final population and the per-gen JSONL trace,
  where `<S>` is the drawn GA seed. Each row contains the 68-d vector, DSI value, ATP/spike value,
  per-compartment ATP breakdown, per-direction firing rates, diagnostic cytoplasm volume, diagnostic
  MI. Satisfied by Step 11.

* **REQ-17** — Implement NEW module `code/dsi_atp_comparators.py` (~200-300 lines) that produces:
  (a) Carter-Bean 2009 ATP/AP/cm comparison overlay on the canonical anchor cell + top-3 Pareto
  cells with bootstrap CIs (within-30% / over-by-Xx / under-by-Xx labels); (b) the REVISED Howarth
  2012 17% cortex / 21% cerebellum signalling-budget overlay on top-N cells' implied per-cell
  signalling ATP rate (ATP/spike * PD-rate), correcting for the ~5x missing axon-collateral
  truncation in the Bed B substrate; (c) the Cuntz 2010 balancing-factor band [0.2, 0.7]
  cross-reference to t0122's cytoplasm-volume Pareto front. Bootstrap CIs reuse `bootstrap.py` from
  t0123. Satisfied by Step 12.

* **REQ-18** — Produce `results/images/pareto_front_dsi_vs_atp.png` (Pareto chart with DSI on y,
  ATP/spike on x, joint-pass region highlighted: DSI >= 0.5 AND PD-rate >= 30 Hz AND ATP <= median
  of the front). Satisfied by Step 13.

* **REQ-19** — Produce `results/images/carter_bean_atp_per_ap_check.png` (distribution of ATP/AP
  across the canonical anchor cell and the top-10 Pareto cells with the Carter-Bean 2009 AIS
  ATP/AP/cm benchmark as a horizontal reference line and +/-30% band shaded). Satisfied by Step 13.

* **REQ-20** — Produce `results/images/attwell_laughlin_signalling_budget.png` (top-N cells'
  implied signalling ATP rate (ATP/spike * PD-rate, axon-collateral-corrected) overlaid on the
  Howarth 2012 17% cortex / 21% cerebellum revised signalling-budget anchor, with the historical
  Attwell-Laughlin 2001 47% figure annotated as the legacy reference). Satisfied by Step 13.

* **REQ-21** — Produce `results/images/top50_morphologies_seed<S>.png` (top-50 morphology grid
  with FULL DENDRITE TREES per memory `feedback_top50_morphologies_full_dendrites.md`, NOT soma-only
  — the t0114 failure mode). Satisfied by Step 14.

* **REQ-22** — Produce `results/images/hv_trajectory_seed<S>.png` (hypervolume vs generation trace
  from `hv_trace.jsonl`). Satisfied by Step 13.

* **REQ-23** — Write `results/metrics.json` using the explicit multi-variant format with at least
  the four DSI sub-variants and ATP / diagnostic dimensions: `t0124-seed<S>-best-legit` (headline
  DSI variant with `dsi_subvariant="best_legit"` and associated `atp_per_spike_molecules`,
  `pd_firing_rate_hz`, `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits` dimensions);
  `t0124-seed<S>-overall-max-dsi`; `t0124-seed<S>-overall-min-atp`; `t0124-seed<S>-dsi-eq-one-count`
  (count of cells with DSI == 1.0 exactly, indicating ND-silenced near-degenerate solutions). The
  only `metrics` key used is `direction_selectivity_index` (the only registered metric the task
  measures). All non-registered numeric outputs (`atp_per_spike_molecules`, `pd_firing_rate_hz`,
  `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits`) are reported as `dimensions` entries
  within each variant, NOT as top-level `metrics` keys, to satisfy the verificator rule that only
  registered `meta/metrics/` keys may appear in `metrics`. Satisfied by Step 15.

* **REQ-24** — Build the predictions asset
  `assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph/` with: `details.json`
  (`prediction_format: "jsonl.gz"`, per-cell schema
  `{generation, cell_index, vector_68d, dsi_vector_sum, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, pd_rate_hz, nd_rate_hz, cytoplasm_volume_um3, mi_count_bits, objective_F_minimised, silence_failed_bool, legit_bool}`,
  `created_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"`,
  `metrics_at_creation: {best_dsi_legit, min_atp_per_spike, joint_pass_count, n_generations_completed, n_cells_total, final_hypervolume, final_cost_usd, stop_trigger}`);
  a `description.md`; and `files/predictions.jsonl.gz`. Asset must pass
  `verify_predictions_asset.py`. Satisfied by Step 16.

* **REQ-25** — Build the answer asset
  `assets/answer/dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin/` answering: "Does the
  DSGC DSI-vs-ATP-per-spike Pareto front show a Carter-Bean Na/K-overlap penalty, and where do its
  top cells sit relative to the revised Howarth 2012 17% cortex / 21% cerebellum signalling-ATP
  budget (and historically, the original Attwell-Laughlin 2001 47% anchor)?" Primary evidence: the
  joint-correlation analysis between DSI and ATP-per-spike across the Pareto front (positive convex
  -> Carter-Bean penalty; flat / weak -> NMDA-cheap DSI mechanism; negative -> non-Na+ DSI
  mechanism). Bootstrap CIs from `dsi_atp_comparators.py`. Satisfied by Step 17.

* **REQ-26** — Run the inherited DSI silence-guard regression test
  `code/test_evaluator_dsi_guard.py` (forked verbatim from t0123 with import-path rewrites only; the
  7 pytest functions cover `pd_spikes_sum in {0, 1, 2, 3, 30}`, the threshold constant value, and
  the `_vector_sum_dsi` synthetic check at `(PD=5, ND=1) = 0.6667`). Satisfied by Step 7.

* * *

## Approach

The work is a minimum-change fork of `t0123_bedb_mi_atp_per_spike_nsga2` (which was itself a fork of
`t0122_dsi_cytoplasm_volume_nsga2`) with four behavioural deltas, one dropped module, and one new
analysis module. The t0123 code/ directory is the canonical fork point because it already contains
the Sengupta 2010 ATP-per-spike recipe (`atp_per_spike.py`), the `seg.ina` recording infrastructure
(`recorder.py` `attach_ina_recorders_for_atp`), and the Carter-Bean smoke-gate (`smoke_gate.py`
check 9). The t0123 lineage's clean termination at 60/60 gens for $1 (4-direction protocol) confirms
the substrate is healthy and the cost envelope is comfortable for a halved per-cell evaluation
budget.

**The four deltas:**

1. **N_DIRECTIONS: 4 -> 2.** Set `N_DIRECTIONS: int = 2` in `code/constants_morphology.py`. The
   existing `angles_deg = [float(d) * (360.0 / n_directions) for d in range(n_directions)]` formula
   in `evaluator.py` yields `[0.0, 180.0]` for `n_directions=2` — exactly t0122's antipodal-pair
   protocol. Per-cell trial budget drops from 12 (t0123: 3 eval seeds x 4 dirs) to 6 (t0124: 3 eval
   seeds x 2 dirs); per-cell wall-clock roughly halves. The `_gaba_prob_for_direction` sigmoid in
   `trial_helpers.py` already generalises to any direction via
   `d = abs((direction_deg - CELL_PREF_DEG + 180.0) % 360.0 - 180.0)` — no change needed. The MI
   count-entropy ceiling that motivated t0123's 4-direction protocol does NOT apply here because MI
   is only a tracked diagnostic in t0124, not the function objective.

2. **Promote DSI from diagnostic to headline objective.** The DSI silence-guarded vector-sum
   `_vector_sum_dsi` already exists in `evaluator.py` from t0122 and is computed verbatim in t0123
   as a tracked diagnostic. The change is to (a) reorder `CellEvalResult` so `dsi_vector_sum` is the
   first F axis and (b) rewrite `BedBV3MorphProblem._evaluate` to emit
   `out["F"] = np.array([-result.dsi_vector_sum, +result.atp_per_spike_molecules])`. The silence
   guard threshold `SILENCE_PD_SPIKES_THRESHOLD = 3` is unchanged. For 2 antipodal directions, the
   vector-sum DSI reduces exactly to `(R_PD - R_ND) / (R_PD + R_ND)` — confirmed by the t0123
   regression test `test_evaluator_dsi_guard.py` synthetic check `(PD=5, ND=1) -> 0.6667`.

3. **Drop MI as F-axis.** Remove `mi_count_bits` from `out["F"]` and from the headline
   `CellEvalResult` fields used by the NSGA-II problem. KEEP `mi_count_bits` as a tracked diagnostic
   via `code/mi_estimator.py` — it is computed for free per cell evaluation and written into the
   predictions asset, but does NOT enter the objective vector. Drop the entire
   `code/post_hoc_strong_bialek.py` module from the t0124 fork — it is MI-verification scaffolding
   specific to t0123 and adds no value to a DSI-vs-ATP optimisation.

4. **ATP recipe: inherit verbatim from t0123.** No algorithmic changes. The Sengupta 2010 recipe in
   `code/atp_per_spike.py` is direction-independent — it integrates inward Na+ current per AP
   window regardless of bar direction — so the 2-direction protocol works as-is. The `seg.ina`
   recorder in `code/recorder.py` is also direction-independent (one recording per trial regardless
   of bar direction). The recipe assumes a FULL mode trial (HH on, real spikes). EPSP / IPSP passive
   modes produce no meaningful Na+ inward current and are skipped for ATP estimation — inherited
   from t0123 verbatim.

**One new analysis module from scratch:**

`code/dsi_atp_comparators.py` (~200-300 lines) implements the three cross-literature comparisons
that t0123 does not perform:

* Carter-Bean 2009 ATP/AP/cm comparison on top-3 Pareto cells (bootstrap CI, within-30%
  classification).
* REVISED Howarth 2012 17% cortex / 21% cerebellum signalling-ATP budget overlay on top-N cells'
  implied per-cell signalling ATP rate. NOTE the revision: the task description's anchor text
  references Attwell-Laughlin 2001's 47% original figure, but the research_internet.md update
  (Howarth, Gleeson & Attwell 2012, `10.1038/jcbfm.2012.35`) revised the AP fraction of signalling
  ATP downward from 36-47% to 17% (cortex) / 21% (cerebellum). The compare-literature layer uses the
  REVISED 17% anchor as the primary quantitative reference and cites the 2001 47% figure as the
  historical reference. Cells exceeding the 17% anchor are exhibiting genuinely inefficient sodium
  overlap; cells matching the 2001 47% anchor would actually be physiologically unrealistic.
* Cuntz 2010 balancing-factor band [0.2, 0.7] cross-reference to t0122's cytoplasm-volume Pareto
  front (loaded from `tasks/t0122_dsi_cytoplasm_volume_nsga2/results/data/pareto_front_*.json` via
  the aggregator path, not by direct Glob walk).

**Carter-Bean canonical value re-derivation from first principles (resolves S-0123-04).**

The task description and research_papers.md cite "~4 mM-mol/cm" as the Carter-Bean 2009 smoke-gate
target. research_internet.md confirmed that the Carter and Bean 2009 paper (corrected DOI
`10.1016/j.neuron.2009.12.011`, Neuron 64(6), 898-909, December 2009) reports overlap factors
`alpha ~ 1.25` for cortical pyramidal neurons and `alpha ~ 2.0` for fast-spiking GABAergic /
Purkinje neurons, but does NOT directly report a per-cm AIS ATP/AP value. The "~4 mM-mol/cm" target
is a project-internal anchor; t0123's smoke-gate flagged the plan-quoted `2.41e21 ATP/cm` figure as
a typo (it would imply ~10^18 ATP per AP at a ~25 um AIS, physically implausible).

First-principles derivation (mouse RGC AIS, using research-corpus values for the order of
magnitude):

* Werginz 2024 mouse alpha-RGC AIS Nav density: `gNa_AIS = 1300 mS/cm^2 = 1.3 S/cm^2`. (For
  cross-reference: Kole 2008 cortical pyramidal AIS `~0.25 S/cm^2`; the alpha-RGC AIS sits
  approximately 5x higher.)
* Sengupta 2010 cross-species cell-type table: cortical pyramidal Na+ load per AP per unit area
  `~285 nC/cm^2` (Carter-Bean alpha ~ 1.25 cell); fast-spiking interneuron `~315 nC/cm^2`
  (Carter-Bean alpha ~ 2.0); a DSGC is between these, so expected mouse-RGC AIS Na+ load per AP per
  unit area is approximately `~300 nC/cm^2` order of magnitude.
* Convert to ATP/AP per unit area: `Q = 300 nC/cm^2 = 3e-7 C/cm^2`; ATP/AP/area =
  `Q / (e * 3) = 3e-7 / (1.602e-19 * 3) = 6.24e11 ATP/cm^2/AP`.
* To express as per-cm of AIS length: multiply by the AIS perimeter at typical RGC AIS diameter
  `d ~ 1.0 um = 1e-4 cm`: `perimeter = pi * d = 3.14e-4 cm`. ATP/AP/cm =
  `6.24e11 * 3.14e-4 = ~2e8 ATP/AP/cm`. So the order-of-magnitude expectation is
  `~1e8 - 1e9 ATP/AP/cm` for the RGC AIS, sitting between the cortical pyramidal (alpha 1.25) and
  fast-spiking (alpha 2.0) reference values from Sengupta 2010.
* The "~4 mM-mol/cm" project-internal phrasing translates to `4e-3 mol/cm` (millimoles per cm),
  which is `4e-3 * 6.022e23 = 2.41e21` molecules of Na+ per cm; dividing by `3 Na+/ATP` gives
  `~8e20 ATP/cm` — also physically implausible (10^12 times the first-principles estimate). The
  "~4 mM-mol/cm" phrasing carried in the task description is a units-confusion artefact from the
  S-0097-02 source; the first-principles derivation places the canonical AIS ATP/AP/cm in the
  `~1e8 - 1e9 ATP/AP/cm` band, not `~10^21`.

**The smoke-gate uses the first-principles canonical band `~1e8 - 1e9 ATP/AP/cm` as the within-30%
target, with the broader `[1e6, 1e14] ATP/AP/cm` fallback band retained from t0123 as a
physically-plausible sanity check.** If the canonical Bed B cell's per-AP AIS ATP measurement lands
in the `[3e7, 3e9]` band (within 30% of the geometric mean of `[1e8, 1e9]`), the smoke-gate PASSES;
if it lands in the broader `[1e6, 1e14]` band but outside `[3e7, 3e9]`, the smoke-gate issues a
WARNING and the run proceeds with the diagnostic logged; if it lands outside `[1e6, 1e14]`, the
smoke-gate FAILS and NSGA-II launch is aborted. This three-tier policy is the S-0123-04-resolved
replacement for the t0123 typoed `2.41e21 ATP/cm` reference.

**Recommended task types** (match `task.json` `task_types`):

* **`experiment-run`** — the NSGA-II run is an experiment producing a predictions asset.
  Hypothesis: "the DSGC DSI-vs-ATP-per-spike Pareto front exhibits a Carter-Bean-style Na/K-overlap
  penalty (positive convex correlation between DSI and ATP-per-spike across non-dominated cells)
  whose top cells sit AT OR BELOW the Howarth 2012 17% cortex revised signalling-ATP budget anchor."
  Independent variable: the 68-d parameter vector and the new (DSI, ATP) F vector. Dependent
  variables: `dsi_vector_sum`, `atp_per_spike_molecules`, diagnostic
  `pd_rate_hz / nd_rate_hz / cytoplasm_volume_um3 / mi_count_bits`. Baseline: t0122's clean
  termination at 60/60 gens for $0.50 (substrate-health proxy on a 2-direction protocol).
* **`data-analysis`** — the post-run Pareto front, Carter-Bean overlay, Attwell-Laughlin / Howarth
  2012 signalling-budget overlay, top-50 morphology grid, and HV-trajectory plots are data-analysis
  steps. Per the data-analysis Planning Guidelines, only registered `meta/metrics/` keys may appear
  in `metrics.json`. Custom numeric outputs go in `dimensions` per the multi-variant format.
* **`answer-question`** — the task produces one answer asset answering the Carter-Bean +
  Howarth/Attwell-Laughlin comparison question. Per the answer-question Planning Guidelines, the
  stable question is fixed in advance; one answer asset per question. The "Insufficient evidence"
  escape clause triggers if fewer than 10 LEGIT cells are returned in the final population
  (analogous to t0123's planned escape; t0123 actually returned 0 LEGIT cells and the answer
  reported the null result quantitatively).

**Alternatives considered (and rejected):**

* **Alternative A — keep N_DIRECTIONS = 4.** Rejected because DSI only needs one antipodal pair
  (vector-sum DSI on PD-ND axis equals 2-direction antipodal ratio DSI) and ATP-per-spike is
  direction-independent under per-spike normalisation. Doubling the per-cell trial budget would push
  the run wall-clock up by ~2x with zero gain in either objective signal.
* **Alternative B — also negate the ATP objective (compute as `-atp_per_spike`).** Rejected
  because NSGA-II is a minimiser by convention; the F-vector sign convention is "negative for
  maximised objectives, positive for minimised". DSI is maximised so `-dsi_vector_sum`; ATP is
  minimised so `+atp_per_spike_molecules`. Mixing these signs would flip the front and produce
  ATP-maximising cells — directly checked by smoke-gate check 8.
* **Alternative C — use a vector-sum DSI on all 4 t0123 directions.** Rejected because for
  off-axis side lobes the vector-sum DSI is bounded above by the antipodal ratio DSI; reducing to 2
  antipodal directions gives the optimiser the maximum DSI signal per spike count. The comparison to
  t0122 (also 2 antipodal) is also cleaner.
* **Alternative D — add a third objective: cytoplasm volume.** Rejected because the t0097
  catalogue ranks DSI vs ATP-per-spike specifically (not as a triplet) and the project's standing
  policy is "one task = one front" — t0122 already produced the (DSI, cytoplasm) front. The
  comparison is achieved via the cross-reference in `dsi_atp_comparators.py`, not by adding the
  axis. Cytoplasm volume is tracked as a diagnostic, free since t0122 added the helper
  `cytoplasm_volume.py`.
* **Alternative E — wait for a Carter-Bean 2009 paper download.** Rejected because the
  research_internet.md update established that the Carter-Bean 2009 paper does not directly report
  ATP/AP/cm. The first-principles derivation from Sengupta 2010's overlap-factor table and Werginz
  2024's RGC AIS Nav density is the canonical S-0123-04 resolution; the paper PDF would be cited in
  `compare_literature.md` for the alpha=1.25 cross-cell reference but does not change the smoke-gate
  calibration. The paper is available open-access on PMC2810867 if a downstream task needs it.

* * *

## Cost Estimation

| Item | Estimated Cost | Notes |
| --- | --- | --- |
| Vast.ai EPYC 32-core or 64-core instance (NSGA-II run) | $0.80 - $2.00 | At $0.15-0.40/hr for 3-6 hours of compute. t0122 cost $0.50 at 6 trials per cell (2 dirs); t0123 cost $1 at 12 trials per cell (4 dirs); t0124 inherits t0122's 6 trials per cell with ATP recording overhead (~30%) = ~$0.65 - $1.50 expected. |
| ATP smoke-gate canonical cell evaluation | $0.05 - $0.20 | One canonical Bed B cell, full ATP recipe, on the Vast.ai instance pre-NSGA-II. |
| Per-instance teardown / unexpected charges | $0.10 - $0.50 | Buffer (kept under $1). |
| API calls (LLM inference) | $0.00 | None required. |
| **Estimated total actual cost** | **$1.00 - $2.50** | Within the $6 cap, well within the $35.41 project remaining budget. |
| **Hard cap (COST_CAP_USD)** | **$6.00** | Watchdog stops the run if exceeded. |
| **Per-instance watchdog cap (T0124_PER_INSTANCE_WATCHDOG_USD)** | **$5.00** | Leaves $1 buffer below the task cap for teardown. |

Comparison with project budget (`project/budget.json`: total $100, per-task default $8, $35.41
remaining as of 2026-05-25, no stop threshold reached): the $6 task cap is below the per-task
default and well within the $35.41 remaining project budget. The Vast.ai account balance is to be
re-verified at provisioning time; if balance is below $7, the cap is reduced to (balance - $1) per
the task description. Prior lineage spend: t0113 = $0.48, t0114 = $1.13, t0115 = $2.50, t0122 =
$0.50, t0123 = ~$1. All five came in well under their original caps, supporting the $1.00-$2.50
expected actual band at halved per-cell evaluation cost relative to t0123.

* * *

## Step by Step

### Milestone 1 — Code Fork and Edit (Steps 1-8, local CPU)

1. **Preflight: confirm Vast.ai balance and t0123 fork-base health.** Operator confirms the Vast.ai
   account balance is `>= $7` before any provisioning. Then run
   `uv run python -u -m arf.scripts.aggregators.aggregate_tasks --format json --detail full --ids t0123_bedb_mi_atp_per_spike_nsga2`
   and confirm the returned task has `status: "completed"` and a clean termination report. If either
   check fails, STOP and write an intervention file at `intervention/preflight_failed.md` explaining
   the failure. Expected output: a log line "[preflight] vast balance >= $7 OK; t0123
   status=completed OK". No REQ satisfied directly (preflight only).

2. **Fork the t0123 code/ directory verbatim, drop `post_hoc_strong_bialek.py`.** Copy every file in
   `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/` to
   `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/` EXCEPT
   `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/post_hoc_strong_bialek.py` (MI-specific, drop).
   Files to copy: `__init__.py`, `anchor_classifier.py`, `anchor_definitions.py`, `apply_params.py`,
   `atp_per_spike.py`, `biological_priors.py`, `biological_scorecard.py`, `bootstrap.py`,
   `build_assets.py`, `build_cell_ais.py`, `build_pareto_plots.py`, `build_predictions_assets.py`,
   `build_results.py`, `build_top50_morphologies.py`, `constants.py`, `constants_electrophys.py`,
   `constants_morphology.py`, `cost_watchdog.py`, `cuntz_balancing_factor.py`,
   `cytoplasm_volume.py`, `evaluator.py`, `extend_with_ais.py`, `generator_wrapper.py`,
   `hv_plateau_watchdog.py`, `metrics_builder.py`, `mi_estimator.py`, `nsga2_driver.py`,
   `parametric_placer.py`, `paths.py`, `random_init.py`, `recorder.py`, `run_seed441.sh` (rename to
   `run_seed<S>.sh`), `smoke_gate.py`, `sync_results_back.sh`, `test_evaluator_dsi_guard.py`,
   `trial_helpers.py`. Then run a global string substitution
   `tasks.t0123_bedb_mi_atp_per_spike_nsga2.code -> tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code`
   and `T0123_ -> T0124_` across all `.py` and `.sh` files. Expected output: `ls code/` shows ~36
   forked Python files (no `post_hoc_strong_bialek.py`). Satisfies REQ-8.

3. **Edit `code/constants.py` and `code/constants_morphology.py`.** Apply the following changes:

   * In `code/constants.py`:
     * Replace `T0123_SEEDS = (441,)` with `T0124_SEEDS = (<drawn_seed>,)` where `<drawn_seed>` is
       drawn at edit time via Python `secrets.randbelow(10000)` with a rejection loop discarding
       multiples of 500 / 1000 and lineage seeds `{77, 441, 1524, 2247, 7755, 9354}`. Record the
       drawn seed value verbatim in `code/constants.py` as a module-level constant.
     * Replace `T0123_HARD_BUDGET_USD = 6.0` with `T0124_HARD_BUDGET_USD: float = 6.0`. Keep
       `COST_CAP_USD: float = T0124_HARD_BUDGET_USD` alias.
     * Replace `T0123_PER_INSTANCE_WATCHDOG_USD = 5.0` with
       `T0124_PER_INSTANCE_WATCHDOG_USD: float = 5.0`.
     * Preserve back-compat aliases (`T0104_*`, `T0106_*`, `T0114_*`, `T0115_*`, `T0122_*`,
       `T0123_*`) so the forked driver and cost watchdog pick up the new $6 cap correctly.
     * Confirm `_POOL_RESTART_EVERY: int = 10` is preserved verbatim from the fork (REQ-1).
     * Confirm `HV_PLATEAU_AUTO_STOP: bool = False` is preserved verbatim from the fork (REQ-2).
     * Confirm `N_GEN_MAX: int = 60` alias is preserved (REQ-6).
     * Update the module docstring to reference the new task ID and the (DSI, ATP) objectives.

   * In `code/constants_morphology.py`:
     * Change `N_DIRECTIONS: int = 4` to `N_DIRECTIONS: int = 2` (REQ-5).
     * Keep `POP_SIZE: int = 96` (REQ-3), `N_EVAL_SEEDS: int = 3` (REQ-4), `N_GEN: int = 60`
       (REQ-6).
     * Keep `HV_UTOPIA_DSI: float = 0.7` (already defined; replaces t0123's `HV_UTOPIA_MI_BITS`
       value for the hypervolume reference point in `nsga2_driver.py`).
     * Keep `SILENCE_PD_SPIKES_THRESHOLD: int = 3` verbatim from t0122 / t0123 lineage.
     * Keep `WORST_CASE_DSI: float = -1.0` verbatim.

   Expected output:
   `grep -n "POP_SIZE\|N_EVAL_SEEDS\|N_DIRECTIONS\|N_GEN_MAX\|_POOL_RESTART_EVERY\|HV_PLATEAU_AUTO_STOP\|COST_CAP_USD\|T0124_SEEDS" code/constants.py code/constants_morphology.py`
   returns the expected values listed above. Satisfies REQ-1, REQ-2, REQ-3, REQ-4, REQ-5, REQ-6,
   REQ-7, REQ-9.

4. **Confirm `code/recorder.py` and `code/atp_per_spike.py` are reused verbatim.** No edits beyond
   the global import-path rewrite from Step 2. Verify by running
   `uv run python -u -c "from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.atp_per_spike import compute_atp_per_spike, detect_ap_windows, compute_atp_per_ap, compute_compartment_breakdown; print('OK')"`.
   Verify the unit-conversion constant: `grep -n "UM2_TO_CM2" code/atp_per_spike.py` returns
   `UM2_TO_CM2 = 1.0e-8`. Verify the per-segment recorder signature:
   `grep -n "attach_ina_recorders_for_atp" code/recorder.py` returns the function definition.
   Expected output: imports succeed and the unit-conversion factor is `1e-8` (NOT `1e-2`). Satisfies
   REQ-10, REQ-11.

5. **Edit `code/nsga2_driver.py` for F-axis label rewrites.** Specific edits:

   * Change `state.all_evaluations.append({"mi_count_bits": float(-f_row[0]), ...})` to
     `state.all_evaluations.append({"dsi_best_legit": float(-f_row[0]), ...})`.
   * Change the `hv_utopia` value: drop any `HV_UTOPIA_MI_BITS` reference and use `HV_UTOPIA_DSI` (=
     0.7) from `constants_morphology.py`. The HV reference point becomes
     `(0.0, WORST_CASE_ATP_PER_SPIKE)` where 0.0 is the worst-case DSI after negation (DSI worst =
     0, so `-0 = 0`); ATP worst-case unchanged.
   * Print statements that reference the F[0] objective name: change "MI" to "DSI".
   * Confirm `_POOL_RESTART_EVERY = 10` reference is unchanged (REQ-1).
   * Confirm `TerminationCollection` contains `MaximumGenerationTermination(n_max_gen=n_max_gen)`,
     `CostWatchdogTermination(...)`, `OperatorStopTermination(...)` — NO `HVPlateauTermination`
     (REQ-2).
   * Confirm the per-gen JSONL trace writes both DSI and ATP per cell.

   Expected output:
   `grep -n "dsi_best_legit\|HV_UTOPIA_DSI\|HVPlateauTermination" code/nsga2_driver.py` returns the
   expected matches. Satisfies REQ-1, REQ-2, REQ-15.

6. **Edit `code/evaluator.py` to promote DSI to headline F axis.** Specific edits:

   * On `CellEvalResult`: keep `dsi_vector_sum: float` and `silence_failed: bool` from the t0123
     fork; ensure `mi_count_bits: float | None` remains as a diagnostic field (not an F field);
     ensure `atp_per_spike_molecules: float` remains as the second F field.
   * In `BedBV3MorphProblem._evaluate`: rewrite
     `out["F"] = np.array([-result.mi_count_bits, +result.atp_per_spike_molecules])` to
     `out["F"] = np.array([-result.dsi_vector_sum, +result.atp_per_spike_molecules])`. Keep
     `n_obj = 2`.
   * In `evaluate_68d_vector`: change the default `n_directions: int = 4` to
     `n_directions: int = 2`.
   * In `_summarise_trials`: keep the silence-guard logic
     `if pd_spikes_sum < SILENCE_PD_SPIKES_THRESHOLD: dsi_vector_sum = WORST_CASE_DSI` verbatim from
     t0122 / t0123 (REQ-26).
   * Confirm the per-direction firing-rate fields `firing_hz_per_dir`, `pd_rate_hz`, `nd_rate_hz`
     are still on `CellEvalResult`.
   * Confirm the diagnostic `cytoplasm_volume_um3` and `mi_count_bits` are computed and stored.

   **Validation gate**: After editing, run a SINGLE-CELL evaluation on the canonical anchor cell via
   `uv run python -u -c "from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.evaluator import evaluate_68d_vector; from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.anchor_definitions import ANCHOR_NAMES, anchor_to_68d_vector; r = evaluate_68d_vector(vector_68d=anchor_to_68d_vector(name=ANCHOR_NAMES[0]), n_directions=2); print('DSI:', r.dsi_vector_sum, 'ATP:', r.atp_per_spike_molecules, 'PD_Hz:', r.pd_rate_hz, 'silence_failed:', r.silence_failed)"`.
   Expected: a DSI in `[-1, 1]` (likely `~0.3-0.5` for the canonical "bedb_like" anchor per
   research_papers.md prior), ATP in `[1e6, 1e14]`, PD-rate `>= 10 Hz`, silence_failed=False. If DSI
   <= -0.99 (silence-guard triggered on the canonical cell) or ATP outside the plausible band, STOP
   and debug — do not proceed to the smoke-gate or NSGA-II launch. Inspect 5 individual `seg.ina`
   traces in the AIS segments and verify the AP windows are non-empty. Satisfies REQ-12.

7. **Run the inherited DSI silence-guard regression tests.** Execute
   `uv run python -u -m arf.scripts.utils.run_with_logs uv run pytest tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/test_evaluator_dsi_guard.py -v`.
   Expected output: all 7 tests pass (silence guard at `pd_spikes_sum in {0, 1, 2}` returns
   `WORST_CASE_DSI = -1.0`; at `pd_spikes_sum == 3` returns `_vector_sum_dsi(...)`; at
   `pd_spikes_sum == 30` returns `_vector_sum_dsi(...)`; threshold constant is exactly 3;
   `_vector_sum_dsi(PD=5, ND=1)` returns 0.6666... within 1e-6). If any test fails, STOP and debug
   `evaluator.py`. Satisfies REQ-26.

8. **Edit `code/smoke_gate.py` for the F-axis update + S-0123-04 Carter-Bean derivation.** Edits:

   * Check 7 (sanity range on objectives): replace `MI in [0, 2]` with `DSI in [-1, 1]`, ATP
     unchanged at `[1e6, 1e14]`.

   * Check 8 (BedBV3MorphProblem F-axis sign convention): replace `F[0] = -MI` assertion with
     `F[0] = -DSI`, F[1] unchanged.

   * Check 9 (Carter-Bean): replace the t0123 plan-quoted `2.41e21 ATP/cm` reference with the
     first-principles canonical band `~1e8 - 1e9 ATP/AP/cm` derived above in `## Approach`.
     Implement the three-tier pass/warning/fail policy:
     * PASS if the canonical Bed B cell's per-AP AIS ATP measurement lands in `[3e7, 3e9]` (within
       30% of the geometric mean of the canonical band).
     * WARNING if it lands in `[1e6, 1e14]` but outside `[3e7, 3e9]` — run proceeds with
       diagnostic logged.
     * FAIL if outside `[1e6, 1e14]` — NSGA-II launch aborted. The check writes a derivation block
       to `logs/steps/009_implementation/smoke_gate.json` with the canonical-cell measured value,
       the canonical band, and the pass/warning/fail verdict.

   * Update the smoke-gate report header to reference t0124 and the (DSI, ATP) objectives.

   Satisfies REQ-13.

### Milestone 2 — Remote Machine Provision and Smoke-Gate (Steps 9-10, Vast.ai)

9. **Provision a single Vast.ai EPYC instance.** Orchestrator's `/setup-remote-machine` skill
   provisions a cheapest available 32-core or 64-core EPYC instance with Linux + a working Python
   3.12 + uv environment. The provisioning step `008_setup-machines` populates
   `logs/steps/008_setup-machines/machine_log.json` with the selected offer (instance ID, hourly
   rate, region, CPU/RAM specs). The cost watchdog reads the rate from this file at startup. On the
   instance, run `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` to
   produce the shared `nrnmech` library (or confirm the existing one is loadable). Confirm the
   instance can import `tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.bootstrap` and load
   `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.mods.nrnmech` without errors. Expected
   output: `machine_log.json` exists with `selected_offer.price_per_hour` and `instance_id`; a
   bootstrap-import smoke-test prints "OK". Satisfies REQ-14.

10. **Run the 9-check smoke-gate on the Vast.ai instance.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.smoke_gate`.
    The harness:
    * Runs checks 1, 7, 8 (NEURON + MOD library + anchor cell + DSI sanity range + F-axis sign
      convention).
    * Runs checks 2, 3, 4, 5, 6 (silence guard, pool-restart cadence, cost-watchdog wiring,
      HV-plateau absence, hard constants).
    * Runs check 9 (Carter-Bean ATP/AP/cm three-tier policy). Writes
      `logs/steps/009_implementation/smoke_gate.json` with all 9 check verdicts and the Carter-Bean
      derivation block.

    **Validation gate**: All 9 checks must PASS or WARN. If any check FAILS, STOP and write an
    intervention file at `intervention/smoke_gate_failed.md` explaining the failure mode. The most
    common failure for check 9 is a surface-area unit-conversion bug (would show ATP/AP at ~1e10x
    the canonical band, way outside `[1e6, 1e14]`); the second most common is missing compartments
    in the seg.ina record list (would show ATP/AP ~10x below the canonical band). Do NOT proceed to
    NSGA-II launch if check 9 FAILS. If check 9 WARNS but the measured value is in `[1e6, 1e14]`,
    proceed with the diagnostic logged. Satisfies REQ-13.

### Milestone 3 — NSGA-II Run (Step 11, Vast.ai, long-running)

11. **[CRITICAL] Launch the NSGA-II run.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.nsga2_driver --task-seed <drawn_seed> --step-id 009_implementation`.
    The driver:
    * Initialises a Latin-Hypercube random-init pool of 96 cells (Phase A).
    * Runs NSGA-II via pymoo with default SBX crossover (eta = 15), polynomial mutation (eta = 20),
      tournament selection of size 2.
    * Pool-restart every 10 gens via `PerGenerationPoolRestart` callback (REQ-1).
    * Per-gen dill checkpoints land in `logs/steps/009_implementation/checkpoints/`.
    * Per-gen JSONL writes to `logs/steps/009_implementation/hv_trace.jsonl` with HV value plus
      per-cell DSI / ATP / silence_failed / legit_bool / firing rates.
    * Cost watchdog reads `machine_log.json` hourly rate and trips at $5 per-instance cap (REQ-7).
    * Operator-stop termination polls `logs/steps/009_implementation/STOP_FILE` every gen; if the
      file appears, the run gracefully halts and writes the partial pareto front.
    * Maximum-generation termination at gen 60 (REQ-6).

    **Validation gate (expensive operation)**:
    * Baseline expectation: t0122 (DSI + cytoplasm at N_DIRECTIONS = 2) terminated cleanly at 60/60
      gens for $0.50 with HV trajectory rising monotonically through gen 50 then plateauing.
    * Initial gen 0 spot-check (~3 min into the run): the operator inspects 5 individual cell
      records from `hv_trace.jsonl`. Confirm: (a) DSI values are in `[-1, 1]`; (b) ATP values are in
      `[1e6, 1e14]`; (c) silence_failed=True for some cells (expected — many random-init cells
      have R_PD < 3); (d) at least one cell per gen has silence_failed=False AND DSI > 0 (the
      optimiser has live signal). If after gen 3 all cells still have silence_failed=True, STOP and
      inspect the spike-counter logic — do not let the optimiser burn the budget on a broken
      pipeline.
    * If gen-3 spot-check passes, allow the run to continue. Monitor cost via the watchdog
      heartbeat. The run terminates on whichever fires first: operator-stop (likely at gen ~50 per
      research_papers.md HV-plateau prediction), $6 watchdog (unlikely at projected $1.00-$2.50), or
      gen 60.

    Expected output (success): the final population fitness file at
    `logs/steps/009_implementation/final_population.dill`; the HV trajectory at `hv_trace.jsonl`;
    the per-gen checkpoints. Stop trigger recorded in `final_termination_reason.json`. Satisfies
    REQ-15.

### Milestone 4 — Post-Run Analysis (Steps 12-17, local CPU)

12. **Write the new module `code/dsi_atp_comparators.py`.** Functions:
    * `compute_carter_bean_atp_per_ap_per_cm(*, atp_per_ap_molecules_ais, ais_length_cm) -> float`
      — converts a single-cell AIS ATP measurement to ATP/AP/cm.
    * `classify_carter_bean(*, measured_atp_per_ap_per_cm, canonical_band=(1e8, 1e9), tolerance_frac=0.30) -> CarterBeanVerdict`
      — returns dataclass with `{within_band: bool, fold_difference: float, label: str}`.
    * `compute_implied_signalling_atp_rate(*, atp_per_spike_molecules, pd_rate_hz) -> float` —
      multiplies ATP/spike by PD-rate to get implied per-cell signalling ATP rate.
    * `correct_for_axon_collateral_truncation(*, implied_signalling_atp_rate, correction_factor=5.0) -> float`
      — scales by the missing-axon-collateral correction (5x because Bed B has no axon
      collaterals; Attwell-Laughlin 2001 cites 82% axon-collateral share = ~5x truncation).
    * `classify_howarth_attwell_laughlin(*, corrected_signalling_atp_rate, total_atp_rate, howarth_2012_cortex_fraction=0.17, howarth_2012_cerebellum_fraction=0.21, attwell_laughlin_2001_fraction=0.47) -> HowarthAttwellLaughlinVerdict`
      — returns dataclass with the fraction of total ATP devoted to signalling ATP and the verdict
      label "below_howarth_17_cortex / on_howarth_17_cortex / above_howarth_17_cortex /
      above_howarth_21_cerebellum / above_attwell_laughlin_47_historical".
    * `compute_cuntz_balancing_factor_cross_ref(*, t0122_pareto_path) -> dict[str, Any]` — loads
      t0122's cytoplasm-vs-DSI pareto front and computes the implied Cuntz balancing factor band for
      each top-N cell via `code/cuntz_balancing_factor.py` (inherited verbatim from t0123).
    * Top-level orchestrator
      `run_dsi_atp_comparators(*, pareto_front, top_n=10, bootstrap_n=1000) -> ComparatorReport` —
      produces all three comparisons with bootstrap CIs via `code/bootstrap.py` inherited from
      t0123.

    Expected output: a self-contained module with full type annotations, frozen dataclasses for
    every return type, and explicit constants for the 5x correction factor, 17% / 21% / 47% anchors,
    and the canonical Carter-Bean band. Satisfies REQ-17.

13. **Produce the four core Pareto charts.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.build_pareto_plots --task-seed <drawn_seed>`.
    The script loads `results/data/pareto_front_seed<S>.json` (built from `final_population.dill`
    plus `hv_trace.jsonl` — REQ-16) and writes:

    * `results/images/pareto_front_dsi_vs_atp.png` (REQ-18) — DSI on y, ATP/spike on x, all Pareto
      cells plotted; joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz AND ATP <= median of front)
      highlighted in a distinct colour. Title: "Pareto Front: DSI vs ATP-per-Spike (t0124, seed
      <S>)". Axis labels: "DSI (silence-guarded, vector-sum)" on y, "ATP per Spike (molecules)" on
      x. Joint-pass count annotated in the legend.

    * `results/images/carter_bean_atp_per_ap_check.png` (REQ-19) — y-axis: per-AP AIS ATP in
      ATP/AP/cm units. Horizontal reference lines at the first-principles canonical band edges
      (`1e8` and `1e9 ATP/AP/cm`) with the geometric mean (`~3e8 ATP/AP/cm`) shown as a dashed line
      and the +/-30% band (`[3e7, 3e9]`) shaded. Scatter of the canonical anchor cell value and the
      top-10 Pareto cells' AIS ATP/AP/cm with bootstrap-CI error bars. Annotation: text indicating
      which canonical-band tier each cell hits (within, warning, or fail). Title: "Carter-Bean 2009
      AIS ATP/AP/cm Smoke-Gate (canonical + top-10 Pareto cells)".

    * `results/images/attwell_laughlin_signalling_budget.png` (REQ-20) — y-axis: implied per-cell
      signalling ATP rate (ATP/spike * PD-rate), axon-collateral-corrected. Horizontal reference
      lines at the Howarth 2012 17% cortex anchor (primary), 21% cerebellum anchor (secondary), and
      47% Attwell-Laughlin 2001 historical anchor (annotated as "legacy reference"). Per-cell bars
      or scatter for the top-N cells with bootstrap-CI error bars. Title: "Implied Per-Cell
      Signalling ATP Rate vs Howarth 2012 (revised) Budget Anchor". Legend annotates the
      Attwell-Laughlin 2001 47% as the historical reference, NOT the primary comparison anchor.

    * `results/images/hv_trajectory_seed<S>.png` (REQ-22) — hypervolume vs generation from
      `hv_trace.jsonl`. Title: "NSGA-II Hypervolume Trajectory (seed <S>)". Annotation of
      stop-trigger generation.

    Expected output: four PNG files written to `results/images/` with valid axis labels, titles, and
    bootstrap-CI error bars where applicable. Satisfies REQ-18, REQ-19, REQ-20, REQ-22.

14. **Produce the top-50 morphology grid.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.build_top50_morphologies --task-seed <drawn_seed> --render-mode full_dendrite_trees`.
    The script loads the top-50 cells by DSI from `results/data/pareto_front_seed<S>.json`, rebuilds
    each via `code/generator_wrapper.py build_cell`, and renders the full dendrite tree (NOT
    soma-only — the t0114 failure mode per memory `feedback_top50_morphologies_full_dendrites.md`)
    in a 5x10 grid with per-cell annotations showing DSI, ATP/spike, PD-rate. Title: "Top-50
    Morphologies by DSI (t0124, seed <S>) — full dendrite trees". Expected output:
    `results/images/top50_morphologies_seed<S>.png` is a single high-resolution PNG with all 50
    cells visibly rendered as dendrite trees. Satisfies REQ-21.

15. **Write `results/metrics.json` in explicit multi-variant format.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.metrics_builder --task-seed <drawn_seed>`.
    The builder produces the four variants:

    * `t0124-seed<S>-best-legit`: headline variant. `dimensions` include `task_seed`,
      `init_method: "lhs_random"`, `n_obj: 2`, `n_directions: 2`, `dsi_metric: "vector_sum"`,
      `dsi_silence_guard_active: true`, `silence_guard_threshold_pd_spikes: 3`, `n_eval_seeds: 3`,
      `n_generations_target: 60`, `n_cells: <total evaluated>`, `n_legit: <count of LEGIT cells>`,
      `pool_restart_every: 10`, `hv_plateau_auto_stop_disabled: true`,
      `dsi_subvariant: "best_legit"`, plus the headline cell's `atp_per_spike_molecules`,
      `pd_firing_rate_hz`, `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits`. `metrics`:
      `{"direction_selectivity_index": <best DSI value of the best legit cell>}`.

    * `t0124-seed<S>-overall-max-dsi`: `dsi_subvariant: "overall_max_dsi"`. Records the overall
      maximum DSI ignoring the silence guard, plus the associated cell's ATP / firing / volume / MI.

    * `t0124-seed<S>-overall-min-atp`: `dsi_subvariant: "overall_min_atp"`. Records the overall
      minimum ATP/spike, plus the associated cell's DSI / firing / volume / MI.

    * `t0124-seed<S>-dsi-eq-one-count`: `dsi_subvariant: "dsi_eq_one_count"`. Records the count of
      cells with DSI == 1.0 exactly (near-degenerate ND-silenced cells where R_ND = 0). The
      `metrics` field is `{"direction_selectivity_index": 1.0}` (the variant value).

    The only registered metric key that appears in any `metrics` field is
    `direction_selectivity_index` — the only metric in `meta/metrics/` that this task can directly
    measure. Per the planning skill Phase 1 step 7: of the 4 registered metrics
    (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
    `tuning_curve_rmse`), only `direction_selectivity_index` applies. The HWHM / reliability / RMSE
    metrics REQUIRE a full angular tuning sweep (8+ directions) and a target tuning curve; t0124
    uses 2 antipodal directions and no target curve, so these three metrics CANNOT be measured by
    this task. Their omission is deliberate, not accidental, and is explicitly documented here.

    Custom non-registered numeric outputs (`atp_per_spike_molecules`, `pd_firing_rate_hz`,
    `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits`) are reported as `dimensions`
    entries within each variant, NOT as top-level `metrics` keys, to satisfy the verificator rule
    that only registered `meta/metrics/` keys may appear in `metrics`. Format follows
    `arf/specifications/metrics_specification.md` and t0123's `results/metrics.json` exactly.
    Expected output: a valid `results/metrics.json` with 4 variants. Satisfies REQ-23.

16. **Build the predictions asset.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.build_predictions_assets --task-seed <drawn_seed>`.
    The builder produces `assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph/details.json`,
    `description.md`, and `files/predictions.jsonl.gz`. `details.json` fields: `spec_version: "2"`,
    `predictions_id: "nsga2-dsi-atp-per-spike-bedb-morph"`,
    `name: "NSGA-II DSI vs ATP-per-Spike on Bed B + 14-d Morphology"`,
    `short_description: <description>`, `description_path: "description.md"`, `model_id: null` (no
    separate model asset),
    `model_description: "68-d Bed B compartmental model (54-d electrophys + 14-d morphology), NEURON-backed, NSGA-II via pymoo, single GA seed"`,
    `dataset_ids: []` (no external dataset), `prediction_format: "jsonl.gz"`,
    `prediction_schema: <per-cell schema description spanning generation, cell_index, vector_68d, dsi_vector_sum, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, pd_rate_hz, nd_rate_hz, cytoplasm_volume_um3, mi_count_bits, objective_F_minimised, silence_failed_bool, legit_bool>`,
    `instance_count: <total cells evaluated>`,
    `metrics_at_creation: {best_dsi_legit, min_atp_per_spike, joint_pass_count, n_generations_completed, n_cells_total, final_hypervolume, final_cost_usd, stop_trigger}`,
    `files: [{path: "files/predictions.jsonl.gz", description: ..., format: "jsonl"}]`,
    `categories: ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell", "voltage-gated-channels"]`,
    `created_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"`, `date_created: <ISO date>`.

    Run the verificator:
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m arf.scripts.verificators.verify_predictions_asset tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph/`.
    Expected output: 0 errors. Satisfies REQ-24.

17. **Build the answer asset.** Execute
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.build_assets --task-seed <drawn_seed>`.
    The builder produces
    `assets/answer/dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin/details.json`,
    `short_answer.md`, and `full_answer.md`.

    The question (verbatim from REQ-25): "Does the DSGC DSI-vs-ATP-per-spike Pareto front show a
    Carter-Bean Na/K-overlap penalty, and where do its top cells sit relative to the revised Howarth
    2012 17% cortex / 21% cerebellum signalling-ATP budget (and historically, the original
    Attwell-Laughlin 2001 47% anchor)?"

    Evidence channels (`answer_methods`): `["papers", "code-experiment"]` because the answer
    integrates (a) the Carter-Bean 2009 / Howarth 2012 / Attwell-Laughlin 2001 / Sengupta 2010 /
    Cuntz 2010 / Werginz 2024 paper assets and (b) the t0124 NSGA-II Pareto front from the
    `code-experiment` channel.

    Decision rule for the answer:
    * If `joint_correlation(DSI, ATP) > 0` with bootstrap-CI excluding zero AND the front exhibits a
      positive convex shape -> "YES, the DSGC front exhibits a Carter-Bean Na/K-overlap penalty with
      positive correlation r = X.XX (CI: ..., ...)" + the implied per-cell signalling ATP rate
      fraction of total ATP turnover relative to the Howarth 17% / 21% / Attwell-Laughlin 47%
      anchors.
    * If correlation is flat (|r| < 0.2 with bootstrap-CI including zero) -> "NO, the DSGC front
      does NOT exhibit a Carter-Bean Na/K-overlap penalty; DSI varies freely at fixed ATP,
      suggesting NMDA-cheap DSI mechanism dominates (Poleg-Polsky 2016 multiplicative scaling)".
    * If correlation is negative -> "NEGATIVE, the front shows a non-Na+ DSI mechanism (Ca2+ or
      K+-modulated multiplicative gating) — a novel finding warranting follow-up".
    * If fewer than 10 LEGIT cells return (analogous to t0123's 0-LEGIT outcome) -> "INSUFFICIENT
      EVIDENCE: only <n_legit> cells passed both the silence guard and the joint-pass threshold; the
      Pareto front structure cannot be quantitatively characterised" with the partial-result
      reporting.

    `details.json` fields: `spec_version: "2"`,
    `answer_id: "dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin"`,
    `question: <verbatim above>`,
    `short_title: "DSGC DSI vs ATP-per-spike: Carter-Bean and Howarth/Attwell-Laughlin comparison"`,
    `short_answer_path: "short_answer.md"`, `full_answer_path: "full_answer.md"`,
    `categories: ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell", "voltage-gated-channels"]`,
    `answer_methods: ["papers", "code-experiment"]`,
    `source_paper_ids: [<10.1371_journal.pcbi.1000840 (Sengupta 2010), 10.1097_00004647-200110000-00001 (Attwell-Laughlin 2001), 10.1523_JNEUROSCI.1592-24.2024 (Werginz 2024), 10.1038_nn.3565 (Sivyer 2013), 10.1371_journal.pcbi.1002107 (Hay 2011)>]`,
    plus the corrected Carter-Bean 2009 DOI (`10.1016/j.neuron.2009.12.011`) cited in full_answer.md
    without requiring a local paper asset.
    `source_task_ids: ["t0080_bedb_mobo_v3_dendritic_spike_nsga2", "t0097_multi_obj_optim", "t0122_dsi_cytoplasm_volume_nsga2", "t0123_bedb_mi_atp_per_spike_nsga2"]`,
    `source_urls: ["https://pmc.ncbi.nlm.nih.gov/articles/PMC2810867/", "https://pmc.ncbi.nlm.nih.gov/articles/PMC3390818/" (Howarth 2012)]`,
    `confidence: "medium"` (or "high" if the joint correlation has a clear sign with tight CI),
    `created_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"`, `date_created: <ISO date>`.

    Run the verificator:
    `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/answer/dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin/`.
    Expected output: 0 errors. Satisfies REQ-25.

* * *

## Remote Machines

One single Vast.ai EPYC instance (32-core or 64-core, whichever is cheapest at provisioning time),
Linux + Python 3.12 + uv environment. The instance must successfully compile the shared `nrnmech`
library via `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/` and load the
resulting library through `tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.bootstrap`. Expected
provisioning time: 5-15 minutes; expected run wall-clock: 3-6 hours. Provider: Vast.ai. Cost cap: $5
per instance (T0124 per-instance watchdog), $6 task cap. The `/setup-remote-machine` orchestrator
skill manages provisioning and teardown.

* * *

## Assets Needed

| Asset | Source | Purpose |
| --- | --- | --- |
| `de_rosenroll_2026_dsgc` library | `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/` | Canonical Bed B DSGC NEURON cell + dendrite geometry + nrnmech.dll vendoring; `build_dsgc_cell` used by smoke-gate anchor cell. |
| `de_rosenroll_2026_dsgc_ais_dendritic_spike` library | `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/` | 54-d ParameterVector + `apply_parameter_vector` + tiered channel write loops + AIS extension + compiled MOD pack (`nav16t80`, `napt80`, `nart80`, etc.). |
| `procedural_dsgc_morphology_generator` library | `tasks/t0090_morphology_generator_diversity_test/assets/library/` | 14-d `MorphologyParams` dataclass + `MorphologyResult` + `PARAM_BOUNDS`. |
| `procedural_dsgc_morphology_generator_fix` library | `tasks/t0092_diagnose_morphology_generator_silence/assets/library/` | Canonical patched `generate_fixed_morphology` + `insert_baseline_channels`. |
| t0123 `code/` directory | `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/` | Fork base: ~36 Python modules including `atp_per_spike.py`, `recorder.py`, `evaluator.py`, `nsga2_driver.py`, `smoke_gate.py`, `test_evaluator_dsi_guard.py`. |
| t0122 results data | `tasks/t0122_dsi_cytoplasm_volume_nsga2/results/data/pareto_front_*.json` | Cytoplasm-vs-DSI Pareto front for the Cuntz balancing-factor cross-reference in `dsi_atp_comparators.py`. |
| Sengupta 2010 paper asset | `tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/` | Cross-cell alpha table (cortical pyramidal alpha=1.25; fast-spiking alpha=2.0) for Carter-Bean smoke-gate calibration cited in `compare_literature.md`. |
| Attwell-Laughlin 2001 paper asset | `tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/` | Historical 47% signalling-ATP-budget anchor and 18% somatodendritic / 82% axon-collateral share for the 5x truncation correction. |
| Werginz 2024 paper asset | `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/` | Mouse alpha-RGC AIS Nav density (1300 mS/cm^2) for the Carter-Bean smoke-gate first-principles derivation. |
| Sivyer 2013 paper asset | `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/` | Dendritic-spike-driven DSI mechanism reference for the answer asset's mechanism classification. |
| Howarth 2012 (NOT in corpus) | `https://pmc.ncbi.nlm.nih.gov/articles/PMC3390818/` | Cited in `compare_literature.md` for the REVISED 17% cortex / 21% cerebellum signalling-ATP budget; URL-cited only, not downloaded. |
| Carter-Bean 2009 (NOT in corpus) | `https://pmc.ncbi.nlm.nih.gov/articles/PMC2810867/` | Cited in `compare_literature.md` for the alpha=1.25 reference; URL-cited only, not downloaded. |
| Cuntz 2010 paper asset | (in corpus, balancing factor reference) | Cuntz balancing-factor band [0.2, 0.7] cross-reference to t0122's cytoplasm front. |

* * *

## Expected Assets

| Asset Type | Asset ID | Description |
| --- | --- | --- |
| `predictions` | `nsga2-dsi-atp-per-spike-bedb-morph` | One predictions asset with one row per evaluated cell containing the 68-d vector, `dsi_vector_sum`, `atp_per_spike_molecules`, `atp_per_ap_molecules`, per-compartment ATP breakdown, per-direction firing rates, diagnostic `cytoplasm_volume_um3` and `mi_count_bits`, the F vector, silence-guard flag, and joint-pass flag. Per-cell records compressed to `files/predictions.jsonl.gz`. |
| `answer` | `dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin` | One answer asset answering the Carter-Bean + Howarth/Attwell-Laughlin comparison question with a short answer (2-5 sentences) and a full answer (mini-paper format). Confidence label set by the bootstrap CI on the joint DSI / ATP correlation. |

Both counts match `task.json` `expected_assets`: `{"predictions": 1, "answer": 1}`.

* * *

## Time Estimation

| Phase | Estimated Wall-Clock |
| --- | --- |
| Research (papers + internet + code) | Complete (~5 hours, already done). |
| Planning (this document) | ~1 hour. |
| Code fork + edits (Steps 1-8, local) | ~2-3 hours including the single-cell validation gate and the smoke-gate regression suite. |
| Setup-remote-machine + provisioning (Step 9) | ~30 minutes (cheapest available EPYC offer). |
| Smoke-gate on remote (Step 10) | ~10-30 minutes (depends on canonical anchor cell evaluation time). |
| NSGA-II run (Step 11) | ~3-6 hours wall-clock on 32-core EPYC; ~2.5-5 hours on 64-core. Operator stop expected near gen ~50 per the t0123 / t0122 HV-plateau pattern. |
| Post-run analysis + assets (Steps 12-17) | ~2-3 hours local. |
| Orchestrator-managed reporting steps (results_summary.md / results_detailed.md / costs.json / suggestions.json / compare_literature.md) | ~1-2 hours local. |
| **Total task wall-clock** | **~10-16 hours**, dominated by the NSGA-II run and the analysis layer. |

* * *

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Surface-area unit-conversion bug in `atp_per_spike.py` (most common Sengupta-recipe failure mode per [t0097] catalogue) | Low (recipe inherited verbatim from t0123, but a subtle import or refactor regression is possible) | Smoke-gate check 9 fails with ATP ~10^10x outside the canonical band; NSGA-II launch aborted | Smoke-gate check 9 with the three-tier policy catches it before NSGA-II. Verify `UM2_TO_CM2 = 1e-8` (Step 4). If gate fails, debug per-segment area computation and confirm `seg.area() * 1e-8` is used as cm^2 conversion. |
| Smoke-gate check 9 WARNS (canonical cell measurement in `[1e6, 1e14]` but outside `[3e7, 3e9]`) | Medium | Diagnostic noise; the run proceeds but the Carter-Bean comparison layer reports a wider-than-expected fold-difference | Log the diagnostic in `smoke_gate.json`; the answer asset notes this in the limitations section. If the cell is 10x above the canonical band, the DSI/ATP front is likely interpretable but cells exceeding the band suggest non-physiological Na+ overlap. |
| All Pareto cells trigger the DSI silence guard (R_PD < 3 for every cell, every seed; analogous to t0123's 0-LEGIT outcome) | Medium (research_papers.md predicts the substrate ceiling at DSI ~ 0.4 with full active dendritic Nav; reaching it within 5760 evals on a single seed is plausible but not certain) | Predictions asset has 0 LEGIT cells; the answer asset reports "Insufficient evidence" | The answer asset's "Insufficient evidence" escape clause is pre-wired; the partial result is still informative (the front DOES exist in the unfiltered population). Bootstrap CI on the DSI-vs-ATP correlation is reported regardless. Inspect the gen-3 spot-check (Step 11 validation gate) to catch early; if all cells silence at gen 3, STOP and debug. |
| Vast.ai instance crashes or loses network mid-run | Low-Medium | Partial Pareto front; need to resume from last checkpoint | Per-gen dill checkpoints land in `logs/steps/009_implementation/checkpoints/`. Resume via `nsga2_driver.py --resume-from-checkpoint <path>`. If the instance is permanently lost, provision a fresh one and resume from the latest checkpoint. |
| Cost watchdog trips at $5 per-instance ($6 task) before gen 60 | Low (t0122 cost $0.50, t0123 cost $1; t0124 expected $1-$2.50) | Pareto front truncated; analysis layer runs on partial data | Cost watchdog writes intervention markdown; the analysis layer adapts to whatever generation count was reached. If the watchdog trips at gen < 20, STOP and investigate — likely a per-trial wall-clock regression. |
| The first-principles Carter-Bean canonical-band derivation is wrong by more than a factor of 10 | Medium (the derivation involves 3-4 cross-references with order-of-magnitude approximations) | Smoke-gate WARNs / FAILs on the canonical cell; downstream Carter-Bean comparison ambiguous | The three-tier policy (PASS / WARN / FAIL) catches the derivation error gracefully. The `[1e6, 1e14]` plausibility band is preserved from t0123 as the broader sanity check. If the canonical cell measures outside `[3e7, 3e9]` but inside `[1e6, 1e14]`, the answer asset's confidence is downgraded to "medium" and the limitations section notes the derivation ambiguity. The S-0123-04 follow-up is partially resolved by documenting the derivation; full resolution may require a follow-up task with a direct Carter-Bean 2009 paper download. |
| `code/test_evaluator_dsi_guard.py` fails after the import-path rewrite | Low | Step 7 STOPs; needs debug of the DSI silence-guard regression test | Inherited verbatim from t0123 with only import-path rewrites — the tests cover pure-Python logic with no NEURON dependency, so failure indicates a refactor regression. Debug by running `pytest -v` on individual tests; the silence-guard threshold constant and the `_vector_sum_dsi` synthetic check are pure-Python and should never fail unless the constant value or formula changed. |
| Howarth 2012 paper not in corpus, and the 17% / 21% revised figures are out of date | Low | The compare-literature anchor uses a stale figure | The research_internet.md catalogued Howarth 2012 with full DOI and the URL is in Assets Needed for citation in `compare_literature.md`. The 17% cortex / 21% cerebellum figures are the canonical 2012 update to Attwell-Laughlin 2001 per multiple downstream citations. If a 2024+ revision exists, it would be flagged in research_internet.md — none was found. |
| GA seed `<drawn_seed>` coincidentally hits a parameter-space dead zone | Low | A second NSGA-II re-run with a different seed becomes necessary | Single-seed convention is inherited from t0113 / t0114 / t0115 / t0122 / t0123 lineage. If the result is null and the joint-pass count is 0, a follow-up task with a different seed is the planned mitigation per the t0080 / t0115 substrate-limitation precedent. |

* * *

## Verification Criteria

* **Hard-constants verification**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -c "from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code import constants; from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code import constants_morphology; assert constants._POOL_RESTART_EVERY == 10; assert constants.HV_PLATEAU_AUTO_STOP is False; assert constants_morphology.POP_SIZE == 96; assert constants_morphology.N_EVAL_SEEDS == 3; assert constants_morphology.N_DIRECTIONS == 2; assert constants.N_GEN_MAX == 60; assert constants.COST_CAP_USD == 6.0; assert constants_morphology.SILENCE_PD_SPIKES_THRESHOLD == 3; print('OK')"`.
  Expected output: `OK`. (Covers REQ-1, REQ-2, REQ-3, REQ-4, REQ-5, REQ-6, REQ-7, REQ-12 silence
  guard.)

* **DSI silence-guard regression tests pass**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs uv run pytest tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/test_evaluator_dsi_guard.py -v`.
  Expected output: 7 tests pass, 0 failed. (Covers REQ-26.)

* **Smoke-gate check 9 PASSES or WARNS**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.smoke_gate`
  on the Vast.ai instance. Inspect `logs/steps/009_implementation/smoke_gate.json`. All 9 checks
  must report `"passed": true` OR `"status": "warning"`. The Carter-Bean derivation block must be
  present in check 9 evidence with the canonical band `[1e8, 1e9] ATP/AP/cm`, the geometric mean
  `~3e8 ATP/AP/cm`, and the measured-cell verdict (within `[3e7, 3e9]` for PASS; within
  `[1e6, 1e14]` for WARN; outside for FAIL). (Covers REQ-13.)

* **NSGA-II run terminates cleanly**: Inspect
  `logs/steps/009_implementation/final_termination_reason.json`. The trigger must be one of
  `"operator_stop"`, `"max_generations"`, or `"cost_watchdog"`. Generation count must be `>= 20`
  (else the substrate is broken and a follow-up is needed). Final hypervolume must be `> 0`. (Covers
  REQ-15.)

* **Pareto front and all-evaluations JSON dumps exist and are well-formed**: Run
  `ls tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/pareto_front_seed*.json tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/all_evaluations_seed*.json`
  and verify each file is valid JSON with `>= 1` row. Each row must contain the 68-d vector, DSI
  value, ATP value, per-compartment ATP breakdown, per-direction firing rates, diagnostic volume /
  MI. (Covers REQ-16.)

* **All five required charts exist and are non-empty**: Run
  `ls tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/pareto_front_dsi_vs_atp.png tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/carter_bean_atp_per_ap_check.png tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/attwell_laughlin_signalling_budget.png tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/top50_morphologies_seed*.png tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/hv_trajectory_seed*.png`.
  Each file must be non-empty (`stat --format=%s` returns `> 0`). The top-50 morphology grid must
  visibly render FULL DENDRITE TREES (manual inspection). (Covers REQ-18, REQ-19, REQ-20, REQ-21,
  REQ-22.)

* **`metrics.json` validates against the registered metric registry**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m arf.scripts.verificators.verify_metrics tasks/t0124_bedb_dsi_atp_per_spike_nsga2`.
  Expected output: 0 errors. The four variants must be present (best_legit, overall_max_dsi,
  overall_min_atp, dsi_eq_one_count), each with `direction_selectivity_index` as the only metric key
  and the non-registered numeric outputs in `dimensions`. (Covers REQ-23.)

* **Predictions asset passes verificator**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m arf.scripts.verificators.verify_predictions_asset tasks/t0124_bedb_dsi_atp_per_spike_nsga2`.
  Expected output: 0 errors, optional warnings tolerated. (Covers REQ-24.)

* **Answer asset passes verificator**: Run
  `uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m arf.scripts.verificators.verify_answer_asset tasks/t0124_bedb_dsi_atp_per_spike_nsga2`.
  Expected output: 0 errors, optional warnings tolerated. The `## Short Answer` section must not
  contain inline citations like `[Sengupta2010]` or `[t0123]` (citations belong in `## Sources`).
  (Covers REQ-25.)

* **Requirement coverage cross-check**: Manually verify that every `REQ-1` through `REQ-26` is
  referenced by at least one step in `## Step by Step`. The mapping is: REQ-1 / REQ-2 by Steps 3, 5;
  REQ-3 / REQ-4 / REQ-5 / REQ-6 by Step 3; REQ-7 by Steps 3, 5; REQ-8 by Step 2; REQ-9 by Step 3;
  REQ-10 / REQ-11 by Step 4; REQ-12 by Step 6; REQ-13 by Step 8; REQ-14 by Step 9; REQ-15 by Step
  11; REQ-16 by Step 11; REQ-17 by Step 12; REQ-18 / REQ-19 / REQ-20 / REQ-22 by Step 13; REQ-21 by
  Step 14; REQ-23 by Step 15; REQ-24 by Step 16; REQ-25 by Step 17; REQ-26 by Step 7. All 26
  requirements are mapped. (This criterion is the requirement-coverage check mandated by the
  planning skill `## Done When`.)

* * *

## Alternative Approaches Considered

The four rejected alternatives are documented in `## Approach`. Briefly:

* A. Keep `N_DIRECTIONS = 4` — rejected; DSI needs only one antipodal pair and ATP is
  direction-independent.
* B. Negate ATP in F — rejected; minimisation convention requires `+ATP` for the minimised axis.
* C. Vector-sum DSI over 4 directions — rejected; antipodal ratio DSI gives the maximum signal per
  spike count for the 2-direction protocol.
* D. Add cytoplasm volume as a third F axis — rejected; t0097 ranks DSI vs ATP as a pair; t0122
  already produced the (DSI, cytoplasm) front. Volume is tracked as diagnostic, not optimised.
* E. Wait for a Carter-Bean 2009 paper download — rejected; the paper does not directly report
  ATP/AP/cm. The first-principles derivation from Sengupta 2010 + Werginz 2024 is the canonical
  S-0123-04 resolution.

* * *

## Architecture (Data Flow)

```text
[Vast.ai EPYC instance]
      |
      v
+-----------------------------+
| Step 9: provision; nrnivmodl on t0080/mods/                   |
+-----------------------------+
      |
      v
+-----------------------------+
| Step 10: smoke_gate.py 9 checks (incl. Carter-Bean 1e8-1e9 band) |
+-----------------------------+
      |
      v PASS / WARN
      |
+-----------------------------+
| Step 11: nsga2_driver.py --task-seed <drawn> --step-id 009    |
|  - LHS random-init pop=96                                     |
|  - 60 gens max, pool restart every 10 gens                    |
|  - per-gen: hv_trace.jsonl + checkpoint                       |
|  - F = [-DSI, +ATP_per_spike] minimised                       |
|  - cost watchdog $5 per-instance / $6 task                    |
+-----------------------------+
      |
      v
+-----------------------------+
| Step 12-17: post-run analysis                                 |
|  - dsi_atp_comparators.py (Carter-Bean / Howarth / Cuntz)     |
|  - build_pareto_plots.py (4 charts)                           |
|  - build_top50_morphologies.py (FULL DENDRITE TREES)          |
|  - metrics_builder.py (4 variants)                            |
|  - build_predictions_assets.py + verify_predictions_asset     |
|  - build_assets.py (answer) + verify_answer_asset             |
+-----------------------------+
      |
      v
[Orchestrator handles results_summary.md / costs.json / etc.]
```
