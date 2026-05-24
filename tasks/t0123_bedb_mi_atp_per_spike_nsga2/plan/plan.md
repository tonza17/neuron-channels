---
spec_version: "2"
task_id: "t0123_bedb_mi_atp_per_spike_nsga2"
date_completed: "2026-05-24"
status: "complete"
---
# Plan: NSGA-II Maximising MI and Minimising ATP-per-Spike (Bed B + 14-d Morph)

## Objective

Fork the t0122 single-seed 68-d Bed B + 14-d morphology NSGA-II substrate end-to-end and replace
both objectives: drop (DSI, cytoplasm volume) and adopt (mutual information, ATP-per-spike). MI is
computed in two tiers — a spike-count plug-in estimator with Miller-Madow bias correction inside
the NSGA-II inner loop (2-bit ceiling on a 4-direction protocol), and the Strong-Bialek 1998
direct-method bits/s rate on the top-10 Pareto cells post-hoc with 8 directions x 20 trials. ATP per
spike follows the Sengupta 2010 recipe: integrate inward `seg.ina` over per-AP windows across soma +
AIS + every dendritic segment, divide by elementary charge, and divide by 3 (Na+/K+ ATPase
stoichiometry). Run on a single Vast.ai EPYC instance with one GA seed (`441`, drawn via
`secrets.randbelow(10000)`), `POP_SIZE=96`, `N_EVAL_SEEDS=3`, `N_DIRECTIONS=4`,
`_POOL_RESTART_EVERY=10`, `HV_PLATEAU_AUTO_STOP=False`, `N_GEN_MAX=60`, `COST_CAP_USD=6.0`. DSI and
PD-rate are computed and stored as tracked diagnostics but do not enter the F vector. The headline
scientific output is a Niven 2007 comparison: does the DSGC bits-per-ATP front follow the
fly-photoreceptor super-linear cost-vs-information scaling?

**Done** means: (1) the run terminates cleanly via one of operator-stop, $6 budget watchdog, or the
60-gen ceiling; (2) one predictions asset `nsga2-mi-atp-per-spike-bedb-morph` is written with
per-cell 68-d vectors, F = `[-mi_count_bits, +atp_per_spike_molecules]`, per-direction firing,
diagnostic DSI / PD-rate, and per-compartment ATP breakdown; (3) one answer asset
`dsgc-bits-per-atp-vs-niven-2007` is written answering the Niven comparison question; (4)
`results/metrics.json` registers the chosen variants in the explicit multi-variant format; (5) the
six required charts and the Pareto / all-evaluations / Strong-Bialek JSON dumps are saved; (6) the
Carter-Bean 2009 ATP/AP/cm smoke gate passes within 30% on the canonical anchor cell before launch.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0123_bedb_mi_atp_per_spike_nsga2/task.json` and the resolved long
description at `tasks/t0123_bedb_mi_atp_per_spike_nsga2/task_description.md`:

```text
Name: NSGA-II maximising MI and minimising ATP-per-spike (Bed B + 14-d morph)

Short description: 68-d NSGA-II on Bed B + 14-d morphology, 2-objective MI vs
ATP-per-spike (Strong 1998 + Sengupta 2010). 1 GA seed, pop=96, N_EVAL_SEEDS=3,
4-direction protocol, $6 cap.

Dependencies: t0024, t0080, t0090, t0092, t0097, t0106, t0115, t0120, t0122.
Expected assets: 1 predictions, 1 answer.
Task types: experiment-run, data-analysis, answer-question.
Source suggestion: S-0097-05.

Hard Constraints (non-negotiable, reproduced in code/constants.py):
* _POOL_RESTART_EVERY = 10  (10-gen rule)
* HV_PLATEAU_AUTO_STOP = False  (disabled per project policy)
* POP_SIZE = 96
* N_EVAL_SEEDS = 3
* N_DIRECTIONS = 4  (antipodal pairs 0/90/180/270; reduced from t0091's 8)
* N_GEN_MAX = 60
* COST_CAP_USD = 6.0  (Vast.ai balance $7, $1 teardown buffer)

MI Estimator (two-tier):
* Inner-loop objective: spike-count plug-in MI with Miller-Madow bias correction
  on the 4xB contingency table (12 trials per cell). Ceiling log2(4) = 2.0 bits.
* Post-hoc verification on top-10: 8 directions x 20 trials = 160 trials;
  Strong-Bialek 1998 direct method with 1/T extrapolation,
  dt=5 ms, T in {25, 50, 75, 100} ms. Report bits/s.

ATP-per-Spike Recipe (Sengupta 2010):
N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int(I_Na^inward) dt
* Record seg.ina at simulation dt for soma + AIS proximal + AIS distal +
  all dendritic segments. FULL mode only.
* AP windows: somatic Vm threshold crossing at -20 mV, +/-2 ms around peak,
  2 ms refractory between detections.
* Per-AP per-compartment charge: integrate min(I_Na, 0) over AP window in
  seconds, multiply by seg.area_cm2; ATP = Q / (e * 3).
* Sum across compartments, then divide total ATP by total spikes across all
  trials -> ATP molecules per spike (headline).

Carter-Bean 2009 smoke gate:
* ATP/AP/cm at AIS on canonical Bed B cell must be within 30% of
  ~4 mM-mol/cm = 2.41e21 ATP/cm; abort NSGA-II launch on failure.

Expected outputs:
* assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/
* assets/answer/dsgc-bits-per-atp-vs-niven-2007/
* results/data/pareto_front_seed*.json
* results/data/all_evaluations_seed*.json
* results/data/post_hoc_strong_bialek_mi_top10.json
* results/images/pareto_front_mi_vs_atp.png
* results/images/niven_2007_comparison.png
* results/images/top50_morphologies_seed*.png (full dendrite trees)
* results/images/carter_bean_atp_per_ap_check.png

Verification Criteria (from task_description.md):
* Hard constants asserted in code/constants.py at module import.
* Carter-Bean smoke gate passes within 30% on canonical anchor cell.
* metrics.json registers mi_count_bits, atp_per_spike_molecules,
  mi_strong_bialek_bits_per_sec (top-10), and DSI / PD-rate as diagnostic
  variants.
* Predictions asset passes verify_predictions_asset.
* compare_literature.md includes a row vs Niven 2007 (above / on / below).
* Answer asset states whether the DSGC bits-per-ATP front follows the Niven
  super-linear scaling with explicit quantitative comparison.
```

Decomposed requirements (each step in `## Step by Step` cites the `REQ-*` items it satisfies):

* **REQ-1** — Hard constant `_POOL_RESTART_EVERY = 10` is asserted in `code/constants.py` at
  module import (the project's 10-gen rule per memory `feedback_nsga2_pool_restart_every_10.md`).
  The `PerGenerationPoolRestart` callback fires every 10 gens in `code/nsga2_driver.py`. Satisfied
  by Steps 3 and 4. Evidence: `grep -n "_POOL_RESTART_EVERY" code/constants.py` returns
  `_POOL_RESTART_EVERY: int = 10`.

* **REQ-2** — Hard constant `HV_PLATEAU_AUTO_STOP = False` is asserted in `code/constants.py` and
  the live `TerminationCollection` in `code/nsga2_driver.py` does NOT contain
  `HVPlateauTermination`. Satisfied by Steps 3 and 4. Evidence:
  `grep -n "HV_PLATEAU_AUTO_STOP\|HVPlateauTermination" code/constants.py code/nsga2_driver.py`
  shows `HV_PLATEAU_AUTO_STOP: bool = False` and `HVPlateauTermination` absent from the active
  collection.

* **REQ-3** — Hard constant `POP_SIZE = 96` is asserted in `code/constants_morphology.py` (and
  re-exported by `code/constants.py`). Satisfied by Step 3. Evidence: `grep -n "POP_SIZE"` returns
  `POP_SIZE: int = 96`.

* **REQ-4** — Hard constant `N_EVAL_SEEDS = 3` is asserted in `code/constants_morphology.py`.
  Satisfied by Step 3. Evidence: `grep -n "N_EVAL_SEEDS"` returns `N_EVAL_SEEDS: int = 3`.

* **REQ-5** — Hard constant `N_DIRECTIONS = 4` is asserted in `code/constants_morphology.py`
  (reduced from t0091's 8, increased from t0122's 2). The 4 angles are 0 deg, 90 deg, 180 deg, 270
  deg, generated by the existing
  `angles_deg = [float(d) * (360.0 / n_directions) for d in range(n_directions)]` formula in
  `evaluator.py`. Satisfied by Step 3. Evidence:
  `grep -n "N_DIRECTIONS" code/constants_morphology.py` returns `N_DIRECTIONS: int = 4`.

* **REQ-6** — Hard constant `N_GEN_MAX = 60` is asserted in `code/constants.py` (and `N_GEN = 60`
  in `code/constants_morphology.py`). Satisfied by Step 3. Evidence: `grep -n "N_GEN_MAX\|N_GEN "`
  returns `N_GEN_MAX: int = 60`.

* **REQ-7** — Hard constant `COST_CAP_USD = 6.0` is asserted in `code/constants.py` and the
  `CostWatchdogTermination` is constructed with `hard_budget_usd=T0123_HARD_BUDGET_USD = 6.0`.
  Per-instance watchdog `T0123_PER_INSTANCE_WATCHDOG_USD = 5.0` ($1 buffer below the task cap).
  Satisfied by Steps 3 and 4. Evidence:
  `grep -n "COST_CAP_USD\|T0123_HARD_BUDGET_USD" code/constants.py` returns
  `COST_CAP_USD: float = 6.0`.

* **REQ-8** — Fork `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` verbatim into
  `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/` and rewrite imports
  `tasks.t0122_dsi_cytoplasm_volume_nsga2.code.* -> tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.*`.
  Satisfied by Step 2. Evidence: `ls code/` shows ~30 forked Python files plus the three new
  modules.

* **REQ-9** — GA seed `T0123_SEEDS = (441,)` is set in `code/constants.py`. The seed was drawn at
  edit time via `secrets.randbelow(10000)` rejecting round-ish values (multiples of 500/1000) and
  prior-lineage seeds (77, 2247, 7755, 9354, 1524). Satisfied by Step 3.

* **REQ-10** — Add per-segment `seg.ina` recording in `code/recorder.py` for soma + AIS proximal +
  AIS distal + every dendritic segment. Recording handles re-created on each `h.finitialize` call
  inside `_run_one_trial`. Satisfied by Step 5.

* **REQ-11** — Write a NEW `code/atp_per_spike.py` module (~120 lines) implementing the Sengupta
  2010 recipe: `InaRecorders` dataclass, `attach_ina_recorders`, `detect_ap_windows` (somatic Vm
  threshold crossing at -20 mV, +/-2 ms window, 2 ms refractory),
  `compute_atp_per_ap(*, recorders, ap_windows, cell) -> AtpPerApResult`, and
  `compute_atp_per_spike(*, atp_per_ap_results: list[AtpPerApResult]) -> float`. Satisfied by Step
  6\.

* **REQ-12** — Write a NEW `code/mi_estimator.py` module (~80 lines) with two functions:
  `compute_mi_count_bits(*, direction_labels, spike_counts, n_bins=4) -> float` (sklearn plug-in MI
  plus Miller-Madow correction `(R-1)(C-1)/(2N ln 2)`, returned in bits), and
  `compute_mi_strong_bialek_bits_per_sec(*, spike_trains_by_direction, word_lengths_ms=(25,50,75,100), dt_ms=5.0) -> StrongBialekResult`.
  Satisfied by Step 7.

* **REQ-13** — Modify `code/evaluator.py`: replace `cytoplasm_volume_um3` field on
  `CellEvalResult` with `mi_count_bits: float`, `atp_per_spike_molecules: float`,
  `atp_per_ap_molecules: float`, `atp_per_ap_compartment_breakdown: dict[str, float]`, and
  `firing_hz_per_dir: dict[str, float]`. Rewrite `BedBV3MorphProblem._evaluate` to emit
  `out["F"] = np.array([-result.mi_count_bits, +result.atp_per_spike_molecules])` (MI negated
  because maximised; ATP NOT negated because minimised). Keep `n_obj = 2`. Wire per-segment
  `seg.ina` recording inside `_run_one_trial` (FULL mode only; EPSP / IPSP passive modes skipped for
  ATP). Keep the silence guard at `pd_spikes_sum < 3` (inherited from t0122). Satisfied by Step 8.

* **REQ-14** — Modify `code/smoke_gate.py`: keep t0122's 8 checks (with the cytoplasm-volume check
  replaced by an MI / ATP sanity range check) and ADD a 9th check, the Carter-Bean 2009 ATP/AP/cm
  benchmark. The check computes ATP at the AIS on the canonical t0083 Bed B best-cell electrophys
  vector, compares to `~4 mM-mol/cm = 2.41e21 ATP/cm`, and FAILS if deviation > 30%. Satisfied by
  Step 9.

* **REQ-15** — Provision a single Vast.ai EPYC 32-core or 64-core instance (whichever is cheapest
  at provisioning time) using the orchestrator's `/setup-remote-machine` skill. The orchestrator
  step `008_setup-machines` populates `logs/steps/008_setup-machines/machine_log.json` with the
  selected offer and hourly rate; the cost watchdog reads the rate from this file at startup.
  Satisfied by Step 10.

* **REQ-16** — Run NSGA-II via
  `code/nsga2_driver.py run_nsga2_for_seed(task_seed=441, n_gen_override=None)` with the
  operator-stop / cost-watchdog / 60-gen termination triple. Per-gen dill checkpoints land in
  `logs/steps/009_implementation/checkpoints/`, per-gen JSONL writes to `hv_trace.jsonl`, and pool
  restarts fire every 10 generations. Satisfied by Step 11.

* **REQ-17** — Write `results/data/pareto_front_seed441.json` and
  `results/data/all_evaluations_seed441.json` from the final population and the per-gen JSONL trace.
  Satisfied by Step 12.

* **REQ-18** — Write a NEW standalone `code/post_hoc_strong_bialek.py` script (~250 lines) that
  loads the top-10 Pareto cells from `pareto_front_seed441.json`, builds each cell via the same
  generator-wrapper + apply-params pipeline, runs each with 8 directions x 20 trials per direction
  in FULL mode, calls `compute_mi_strong_bialek_bits_per_sec` from `mi_estimator.py`, and writes
  `results/data/post_hoc_strong_bialek_mi_top10.json` with per-cell `bits_per_sec`, `std_err`,
  `r_squared`, `mi_count_bits` (cross-validation against the inner-loop value), and `atp_per_spike`.
  Satisfied by Step 13.

* **REQ-19** — Produce `results/images/pareto_front_mi_vs_atp.png` (the inner-loop Pareto chart
  with MI on y, ATP/spike on x, joint-pass region highlighted). Satisfied by Step 14.

* **REQ-20** — Produce `results/images/niven_2007_comparison.png` (top-10 cells scattered in
  (ATP/spike, bits/s) space with the Niven 2007 4-species fly-photoreceptor curve overlaid: D.
  melanogaster 200 bits/s, D. virilis ~400, M. domestica ~700, S. carnaria ~1000 bits/s, with the
  fixed ~20% cost baseline annotated; super-linear scaling reference line). Satisfied by Step 14.

* **REQ-21** — Produce `results/images/carter_bean_atp_per_ap_check.png` (distribution of ATP/AP
  across the canonical anchor cell and the top-10 Pareto cells with the Carter-Bean 2009
  `~4 mM-mol/cm = 2.41e21 ATP/cm` benchmark overlaid as a horizontal reference line, +/-30% band
  shaded). Satisfied by Step 14.

* **REQ-22** — Produce `results/images/top50_morphologies_seed441.png` (full dendrite trees per
  memory `feedback_top50_morphologies_full_dendrites.md`, NOT soma-only — the t0114 failure mode).
  Satisfied by Step 15.

* **REQ-23** — Write `results/metrics.json` using the explicit multi-variant format with the
  primary objectives (`mi_count_bits`, `atp_per_spike_molecules`), the post-hoc Strong-Bialek
  variant (`mi_strong_bialek_bits_per_sec` for the top-10), and the diagnostics
  (`direction_selectivity_index` variants plus PD-rate sub-variant). Satisfied by Step 16. Note on
  registered-metric applicability per planning skill Phase 1 step 7: of the 4 registered metrics,
  `direction_selectivity_index` applies (tracked diagnostic — DSI is computed per cell);
  `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse` do NOT apply (this task
  uses 4 antipodal directions only, not a full angular sweep / target tuning curve). Project-wide
  ad-hoc keys `mi_count_bits`, `atp_per_spike_molecules`, `mi_strong_bialek_bits_per_sec` are
  reported alongside DSI even though they are not in `meta/metrics/`; if the verificator rejects
  them, the implementing agent drops the non-registered keys from `metrics.json` and surfaces the
  values only in the predictions asset and through the orchestrator-managed detailed-results
  write-up.

* **REQ-24** — Build the predictions asset `assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/`
  with `details.json` (`prediction_format: "jsonl.gz"`, per-cell schema
  `{generation, cell_index, vector_68d, mi_count_bits, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, dsi_vector_sum, pd_rate_hz, objective_F_minimised, silence_failed_bool, legit_bool}`,
  `created_by_task: "t0123_bedb_mi_atp_per_spike_nsga2"`,
  `metrics_at_creation: {best_mi_count_bits, min_atp_per_spike, niven_curve_above_below_count, n_generations_completed, n_cells_total, final_hypervolume, final_cost_usd, stop_trigger}`),
  `description.md`, and `files/predictions.jsonl.gz`. Asset must pass
  `meta.asset_types.predictions.verificator`. Satisfied by Step 17.

* **REQ-25** — Build the answer asset `assets/answer/dsgc-bits-per-atp-vs-niven-2007/` answering
  "Where does the DSGC bits-per-ATP front sit relative to Niven 2007's fly-photoreceptor curve, and
  does it match the Niven super-linear cost-vs-information scaling?". Primary evidence: the top-10
  cells' Strong-Bialek bits/s vs ATP/spike scatter from Step 13 overlaid on the Niven curve.
  Satisfied by Step 18.

* * *

## Approach

The work is a minimum-change fork of `t0122_dsi_cytoplasm_volume_nsga2` with four behavioural deltas
and three new code modules. Per the research code review (`research/research_code.md`
"Fork-the-most-recent NSGA-II driver verbatim; only objectives change"), t0122 is the direct fork
point: its 776-line `nsga2_driver.py`, 608-line `evaluator.py`, 543-line `smoke_gate.py`, and
323-line `build_top50_morphologies.py` are the load-bearing source files. t0122's clean termination
at 60/60 gens for $0.50 confirms the substrate is healthy and the cost envelope is comfortable for a
doubled per-cell evaluation budget.

The four deltas:

1. **N_DIRECTIONS: 2 -> 4.** Per research_code.md "N_DIRECTIONS = 4 needs only a single constant
   change", t0122's `evaluator.py` line 479 computes
   `angles_deg = [float(d) * (360.0 / n_directions) for d in range(n_directions)]`. For
   `n_directions=4` this yields `[0.0, 90.0, 180.0, 270.0]` — exactly the 4 antipodal-pair angles
   the task description mandates. The same formula handled t0091's 16-direction protocol and t0122's
   2-direction protocol without modification. Per-cell trial budget grows from 6 (t0122: 3 eval
   seeds x 2 dirs) to 12 (t0123: 3 eval seeds x 4 dirs); per-cell wall-clock roughly doubles. The
   `_gaba_prob_for_direction` sigmoid in `trial_helpers.py` already generalises to any direction via
   `d = abs((direction_deg - CELL_PREF_DEG + 180.0) % 360.0 - 180.0)` — no change needed.

2. **Replace both objectives.** Per the t0097 catalogue (full_answer.md lines 287-372) and the task
   description, the new F vector is `out["F"] = [-mi_count_bits, +atp_per_spike_molecules]`. DSI and
   PD-rate are computed and stored on `CellEvalResult` for downstream predictions-asset rows and
   `compare_literature.md` but do NOT enter `out["F"]`. This keeps the optimiser focused on the 2
   declared objectives and avoids confounding the Pareto front with auxiliary axes — the same
   convention t0122 used to keep PD-rate as a diagnostic while optimising (DSI, volume).

3. **Two-tier MI estimator.** Per the t0097 catalogue and research_code.md "Spike-count plug-in MI
   is the right inner-loop estimator for 12-trial budgets":
   * Inner-loop (per cell, per gen): spike-count MI on the 4xB contingency table with Miller-Madow
     bias correction `(R-1)(C-1)/(2N ln 2)`, R=4, C=B, N=12. Ceiling `log2(4) = 2.0 bits`. Uses
     `sklearn.metrics.mutual_info_score` (returns nats; divide by `ln(2)` for bits) — pattern
     established in t0116 / t0117 `cluster_seed_purity.py` line 19.
   * Post-hoc (top-10 cells only): Strong-Bialek 1998 direct method with 1/T extrapolation.
     Discretise each trial's spike train into binary words at `dt=5 ms`, choose
     `T in {25, 50, 75, 100} ms`, pool words across trials for `H_total(T)` and across each
     direction's trials for `H_noise(T)`, fit `[H_total - <H_noise>]/T` against `1/T` via
     `scipy.stats.linregress`, take the intercept as `bits_per_sec`. Trial budget per cell:
     `8 directions x 20 trials = 160`. The two-tier architecture's purpose: inner-loop MI_count is a
     selector; post-hoc Strong-Bialek MI is the literature-comparable quantity that goes on the
     Niven 2007 axis.

4. **ATP-per-spike recipe.** Per the t0097 catalogue and research_code.md "ATP-per-spike recipe
   needs new per-segment seg.ina recording absent from t0122":
   * Record `seg.ina` per segment at simulation `dt` for soma + AIS proximal + AIS distal + every
     dendritic segment via `Vector.record(seg._ref_ina, RECORD_DT_MS)`. Recording handles are
     re-created on every `h.finitialize` because NEURON wipes them on reset.
   * AP windows detected via somatic Vm threshold crossing at `-20 mV` with 2 ms refractory.
     Integration window = `[t_peak - 2 ms, t_peak + 2 ms]`.
   * Per-AP per-compartment charge:
     `Q^(c, AP) = -integral over AP window of min(I_Na, 0) dt * seg.area_cm2`. NEURON's `seg.ina` is
     the automatic sum of all 3 Na channels (`nav16t80`, `napt80`, `nart80`) in `mA/cm^2`;
     `seg.area()` returns `um^2` so convert to `cm^2` via factor `1e-8`. `min(I_Na, 0)` keeps only
     inward (Na+ is negative inward in NEURON convention); leading minus converts to positive
     magnitude.
   * ATP per AP per compartment: `N_ATP^(c, AP) = (Q / e) / 3` with `e = 1.602e-19 C` and the factor
     `1/3` is the Na+/K+ ATPase stoichiometry.
   * Sum across compartments, then total ATP across all APs across all trials divided by total spike
     count = ATP molecules per spike (headline objective).
   * Per-trial `seg.ina` traces themselves are NOT persisted — reduced to per-AP charge integrals
     inside the trial loop and discarded — to keep wall-clock acceptable. Estimated per-trial
     recording footprint at `dt=25 us`, 1400 ms duration, ~200 dendritic segments + 2 AIS + soma:
     ~14 MB float64 per trial. Acceptable at 12 trials per cell.

**Three new code modules from scratch** (research_code.md "New code to write from scratch in this
task"):

* `code/atp_per_spike.py` (~120 lines): `InaRecorders` dataclass, `attach_ina_recorders`,
  `detect_ap_windows`, `compute_atp_per_ap`, `compute_atp_per_spike`.
* `code/mi_estimator.py` (~80 lines): `compute_mi_count_bits` (inner loop) and
  `compute_mi_strong_bialek_bits_per_sec` (post-hoc only).
* `code/post_hoc_strong_bialek.py` (~250 lines): standalone post-NSGA-II script that re-runs the
  top-10 Pareto cells at 8 dirs x 20 trials and writes
  `results/data/post_hoc_strong_bialek_mi_top10.json`.

**Recommended task types** (match `task.json` `task_types`):

* **`experiment-run`** — the NSGA-II run is an experiment producing a predictions asset.
  Hypothesis: "the DSGC bits-per-ATP Pareto front follows Niven 2007's super-linear
  cost-vs-information scaling within a fixed ~20% baseline cost". Independent variable: the 68-d
  parameter vector and the new (MI, ATP) F vector. Dependent variables: `mi_count_bits`,
  `atp_per_spike_molecules`, `mi_strong_bialek_bits_per_sec` (post-hoc), DSI / PD-rate (diagnostic).
  Baseline: t0122's clean termination at 60/60 gens for $0.50 (substrate-health proxy).
* **`data-analysis`** — the post-run Pareto front, Niven 2007 overlay, Carter-Bean ATP/AP check,
  top-50 morphology grid, and the top-10 Strong-Bialek rerun are data-analysis steps. Planning
  guidelines require per-subset breakdowns, matplotlib charts in `results/images/`, and structured
  metrics in `results/metrics.json`.
* **`answer-question`** — the task produces one answer asset answering the Niven comparison
  question. Planning guidelines: define the stable question text, plan one answer per question, name
  evidence channels (the top-10 Strong-Bialek bits/s distribution and Niven 2007 reference curve),
  define what counts as insufficient evidence (here: fewer than 10 LEGIT cells in the final
  population, in which case the answer says "Insufficient evidence" and reports the partial result).

**Alternatives considered (and rejected)**:

* **Alternative A — use Strong-Bialek direct method as the inner-loop objective.** Rejected
  because at 3 trials per direction the 1/T extrapolation is too noisy as a selection signal. Per
  the t0097 catalogue, "the project's 8-direction protocol may be too information-poor to give the
  MI estimator meaningful dynamic range" — using direct method with only 12 trials per cell would
  amplify this. The two-tier architecture cleanly separates the cheap selector from the expensive
  verifier.
* **Alternative B — 8 directions in the NSGA-II inner loop.** Rejected because 24 trials per cell
  doubles wall-clock vs the 12-trial design, pushing the run beyond the $6 cap. The Niven 2007
  comparison only needs bits/s on the top-10 cells, not on every population member; the post-hoc
  8-direction x 20-trial rerun adds only $0.20-0.50.
* **Alternative C — also negate the ATP objective (compute as `-atp_per_spike`).** Rejected
  because NSGA-II is a minimiser by convention; the F-vector sign convention is "negative for
  maximised objectives, positive for minimised". MI is maximised so `-mi_count_bits`; ATP is
  minimised so `+atp_per_spike_molecules`. Mixing this up would flip the front and produce
  ATP-maximising cells.
* **Alternative D — patch `_apply_asymmetry` in the morphology generator before this run.**
  Rejected because the gating dependency `t0120_morph_generator_geometry_audit` returned verdict
  "rendering-only / no re-runs needed". The realised geometry that `seg.area()` returns on each
  morphology is correct.
* **Alternative E — write `atp_per_spike` as a Problem-level constraint instead of an F axis.**
  Rejected because the Pareto trade-off between information and energy is the whole point of the
  Niven 2007 comparison. A constraint would lose the trade-off curve and reduce the answer to a
  binary feasible / infeasible call.

* * *

## Cost Estimation

| Item | Estimated Cost | Notes |
| --- | --- | --- |
| Vast.ai EPYC 32-core or 64-core instance (NSGA-II) | $1.00 - $3.00 | At $0.15-0.40/hr for 4-8 hours of compute. t0122 cost $0.50 at 6 trials per cell; t0123 at 12 trials per cell doubles per-cell wall-clock; ATP recording adds ~30% overhead. |
| Vast.ai cost for post-hoc Strong-Bialek rerun (top-10 cells x 160 trials = 1600 sims) | $0.20 - $0.50 | Same instance, ~30-60 minutes additional. |
| Per-instance teardown / unexpected charges | $0.10 - $0.50 | Buffer (kept under $1). |
| API calls (LLM inference) | $0.00 | None required. |
| **Estimated total actual cost** | **$1.30 - $4.00** | Within the $6 cap. |
| **Hard cap (COST_CAP_USD)** | **$6.00** | Watchdog stops the run if exceeded. |
| **Per-instance watchdog cap (T0123_PER_INSTANCE_WATCHDOG_USD)** | **$5.00** | Leaves $1 buffer below the task cap. |

Comparison with project budget (`project/budget.json`: total $100, per-task default $8, spent
$63.40, remaining $36.60, no stop threshold reached): the $6 cap is below both the per-task default
and the remaining project budget. The reduced cap is dictated by the user's $7 Vast.ai account
balance (verified before launch — operator must re-confirm at the setup-machines step), not by the
ARF budget. Prior lineage spend: t0113 = $0.48, t0114 = $1.13, t0115 = $2.50, t0122 = $0.50. All
four came in well under their original caps, supporting the $1.30-4.00 expected actual band even at
doubled per-cell evaluation cost.

* * *

## Step by Step

### Milestone 1 — Code Fork and Edit (Steps 1-9, local CPU)

1. **Confirm Vast.ai account balance and the t0122 fork-base health.** Operator confirms the Vast.ai
   account balance is `>= $7` before any provisioning. Then run
   `PYTHONIOENCODING=utf-8 uv run python -u -m arf.scripts.aggregators.aggregate_tasks --format json --detail full --ids t0122_dsi_cytoplasm_volume_nsga2`
   and confirm the returned task has `status: "completed"` and the results summary mentions a clean
   termination at 60/60 gens. If either check fails, STOP and write an intervention file at
   `intervention/preflight_failed.md` explaining the failure. Expected output: a log line
   "[preflight] vast balance >= $7 OK; t0122 status=completed OK". No REQ satisfied directly
   (preflight only).

2. **Fork the t0122 code directory verbatim.** Copy every file in
   `tasks/t0122_dsi_cytoplasm_volume_nsga2/code/` to `tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/`
   (~30 files including `nsga2_driver.py`, `evaluator.py`, `generator_wrapper.py`,
   `trial_helpers.py`, `apply_params.py`, `build_cell_ais.py`, `extend_with_ais.py`,
   `parametric_placer.py`, `recorder.py`, `constants.py`, `constants_morphology.py`,
   `constants_electrophys.py`, `cost_watchdog.py`, `hv_plateau_watchdog.py`, `random_init.py`,
   `paths.py`, `bootstrap.py`, `build_top50_morphologies.py`, `smoke_gate.py`,
   `test_evaluator_dsi_guard.py`, `metrics_builder.py`, `build_predictions_assets.py`,
   `build_pareto_plots.py`, `build_assets.py`, `build_results.py`, `anchor_definitions.py`,
   `anchor_classifier.py`, `biological_priors.py`, `biological_scorecard.py`). Then run a global
   string substitution `t0122_dsi_cytoplasm_volume_nsga2 -> t0123_bedb_mi_atp_per_spike_nsga2`
   across all `.py` and `.sh` files. Expected output: `ls code/` shows the same ~30 files as t0122
   plus the empty slots for the three new modules to be added in Steps 6, 7, 13. Satisfies REQ-8.

3. **Edit `code/constants.py` and `code/constants_morphology.py`.** Apply the following changes:

   * In `code/constants.py`:
     * Replace `T0122_SEEDS = (1524,)` with `T0123_SEEDS = (441,)` (the seed was drawn at edit time
       via `secrets.randbelow(10000)` rejecting round-ish values and prior-lineage seeds).
     * Replace `T0122_HARD_BUDGET_USD = 6.0` with `T0123_HARD_BUDGET_USD: float = 6.0`. Keep
       `COST_CAP_USD: float = T0123_HARD_BUDGET_USD` alias.
     * Replace `T0122_PER_INSTANCE_WATCHDOG_USD = 5.0` with
       `T0123_PER_INSTANCE_WATCHDOG_USD: float = 5.0`.
     * Preserve all back-compat aliases (`T0104_*`, `T0106_*`, `T0114_*`, `T0115_*`, `T0122_*`) so
       the forked driver and cost watchdog pick up the new $6 cap correctly.
     * Confirm `_POOL_RESTART_EVERY: int = 10` is preserved verbatim from the fork.
     * Confirm `HV_PLATEAU_AUTO_STOP: bool = False` is preserved verbatim from the fork.
     * Confirm `N_GEN_MAX: int = 60` alias is preserved.
     * Update the module docstring to reference the new task ID and the (MI, ATP) objectives.

   * In `code/constants_morphology.py`:
     * Change `N_DIRECTIONS: int = 2` to `N_DIRECTIONS: int = 4`.
     * Keep `POP_SIZE: int = 96`, `N_EVAL_SEEDS: int = 3`, `N_GEN: int = 60` unchanged.
     * Replace `HV_UTOPIA_VOLUME_UM3 = 5000.0` and the cytoplasm-volume `WORST_CASE_*` constants
       with: `HV_UTOPIA_MI_BITS: float = 1.5` (target below the 2-bit ceiling),
       `HV_UTOPIA_ATP_PER_SPIKE: float = 1e9` (placeholder order-of-magnitude target, to be tuned in
       the post-run analysis against the Carter-Bean / Sengupta benchmark),
       `WORST_CASE_MI_BITS: float = 0.0` (zero-information baseline),
       `WORST_CASE_ATP_PER_SPIKE: float = ATP_PER_SPIKE_MAX_REF * 2.0` where
       `ATP_PER_SPIKE_MAX_REF: float = 1e10` (a pessimistic upper bound; will be cross-checked in
       the smoke gate).
     * Change `REF_POINT_HV` from `(0.0, V_MAX_UM3)` to `(0.0, WORST_CASE_ATP_PER_SPIKE)`
       (negated-MI axis = 0 because MI is non-negative; ATP axis upper bound = pessimistic worst
       case).
     * Keep `HV_UTOPIA_DSI: float = 0.7` and other DSI constants unchanged (still used by the
       biological-scorecard for the tracked diagnostic).

   Expected output:
   `grep -n "_POOL_RESTART_EVERY\|HV_PLATEAU_AUTO_STOP\|POP_SIZE\|N_EVAL_SEEDS\|N_DIRECTIONS\|N_GEN_MAX\|N_GEN \|COST_CAP_USD\|T0123_HARD_BUDGET_USD\|T0123_SEEDS" code/constants.py code/constants_morphology.py`
   returns exactly the values above (10, False, 96, 3, 4, 60, 6.0, and seed 441). Satisfies REQ-1,
   REQ-2, REQ-3, REQ-4, REQ-5, REQ-6, REQ-7, REQ-9.

4. **Edit `code/nsga2_driver.py`.** Apply the following minimal changes:

   * Rewrite imports
     `tasks.t0122_dsi_cytoplasm_volume_nsga2.code.* -> tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.*`
     (already done by Step 2's global substitution; verify).
   * Default `n_gen` to 60 (inherited from t0122; verify).
   * Confirm the live `TerminationCollection` contains only
     `{MaximumGenerationTermination(n_max_gen=n_gen), CostWatchdogTermination(hard_budget_usd=T0123_HARD_BUDGET_USD), OperatorStopTermination(stop_md_path=...)}`
     — `HVPlateauTermination` is NOT in the active collection (already absent from t0122; verify).
   * Confirm `PerGenerationPoolRestart(_POOL_RESTART_EVERY=10)` callback is wired into the live
     algorithm.
   * Keep per-gen dill checkpointing to
     `logs/steps/009_implementation/checkpoints/checkpoint_seed441_gen<NNNN>.pkl` and the
     `hv_trace.jsonl` writer.

   Expected output:
   `grep -n "HVPlateauTermination\|T0123_HARD_BUDGET_USD\|n_gen.*60\|_POOL_RESTART_EVERY" code/nsga2_driver.py`
   returns the expected references and confirms `HVPlateauTermination` is not in the active
   `TerminationCollection`. Satisfies REQ-1, REQ-2, REQ-7.

5. **Edit `code/recorder.py` to add per-segment `seg.ina` recording.** The existing recorder
   attaches a single `Vector.record(soma(0.5)._ref_v, RECORD_DT_MS)` for somatic Vm. Add a new
   helper `attach_ina_recorders_for_atp(*, h, cell: MorphologyResult) -> InaRecorders` that iterates
   `[cell.soma, cell.ais_proximal, cell.ais_distal, *cell.all_dends]` and for each segment
   (`for seg in sec`) attaches `h.Vector().record(seg._ref_ina, RECORD_DT_MS)`. Returns the
   `InaRecorders` dataclass containing the per-segment vector handles plus the soma Vm vector and
   time vector for AP detection. Per research_code.md "Recording footprint doubling has knock-on
   costs but stays within disk + memory budget", the per-trial footprint approximately doubles vs
   t0122 but stays at ~14 MB float64 per trial which is acceptable at 12 trials per cell. Per-trial
   `seg.ina` traces are NOT persisted to disk — they are reduced to per-AP charge integrals inside
   the trial loop in `evaluator.py` Step 8. Expected output:
   `grep -n "attach_ina_recorders_for_atp\|InaRecorders" code/recorder.py` returns the new function
   and dataclass. Satisfies REQ-10.

6. **Write the NEW `code/atp_per_spike.py` module** (~120 lines). Implement the Sengupta 2010 recipe
   with these functions and dataclasses:

   ```python
   @dataclass(frozen=True, slots=True)
   class APWindow:
       t_start_ms: float
       t_peak_ms: float
       t_end_ms: float
       peak_mv: float

   @dataclass(frozen=True, slots=True)
   class AtpPerApResult:
       atp_per_ap_total: float
       atp_per_ap_soma: float
       atp_per_ap_ais: float
       atp_per_ap_dends: float

   def detect_ap_windows(
       *,
       t_ms: NDArray[float],
       v_soma_mv: NDArray[float],
       threshold_mv: float = -20.0,
       refractory_ms: float = 2.0,
       window_half_ms: float = 2.0,
   ) -> list[APWindow]:
       # Upward threshold crossings at -20 mV with 2 ms refractory.
       # AP window = [t_peak - 2 ms, t_peak + 2 ms].
       ...

   def compute_atp_per_ap(
       *,
       recorders: InaRecorders,
       ap_windows: list[APWindow],
       cell: MorphologyResult,
   ) -> list[AtpPerApResult]:
       # Per AP window: per segment, take min(I_Na, 0) pointwise (inward only),
       # integrate via np.trapezoid in seconds, multiply by seg.area_cm2 (seg.area()
       # is um^2, so * 1e-8). Get charge in coulombs. Divide by e=1.602e-19 C and
       # by 3 (Na+/K+ stoichiometry). Sum across segments grouped by
       # {soma, ais, dendrites}. Returns one AtpPerApResult per AP.
       ...

   def compute_atp_per_spike(
       *,
       atp_per_ap_results: list[AtpPerApResult],
   ) -> float:
       # Sum total ATP across all APs across all trials; divide by total spike
       # count. Returns ATP molecules per spike (the headline objective).
       if len(atp_per_ap_results) == 0:
           return float("nan")  # no spikes -> undefined
       return sum(r.atp_per_ap_total for r in atp_per_ap_results) / len(
           atp_per_ap_results
       )
   ```

   The `seg.area()` returns `um^2`. Conversion to `cm^2` is `seg.area() * 1e-8` (NOT `* 1e-2` —
   per research_code.md "the most likely failure mode is a `seg.area()` unit-conversion bug").
   Elementary charge `e = 1.602e-19 C`. ATPase stoichiometry factor `1/3`. Unit-test on a synthetic
   AP trace with known integrated current to verify the conversion before wiring into
   `evaluator.py`. Expected output:
   `uv run python -c "from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.atp_per_spike import compute_atp_per_spike, compute_atp_per_ap, detect_ap_windows; print('ok')"`
   prints `ok`. Satisfies REQ-11.

7. **Write the NEW `code/mi_estimator.py` module** (~80 lines). Implement two functions:

   ```python
   import math
   from sklearn.metrics import mutual_info_score
   from scipy.stats import linregress
   import numpy as np
   from numpy.typing import NDArray

   def compute_mi_count_bits(
       *,
       direction_labels: NDArray[np.int_],
       spike_counts: NDArray[np.int_],
       n_bins: int = 4,
   ) -> float:
       # Bin spike_counts into n_bins log-spaced or quantile bins.
       # Compute plug-in MI via sklearn (returns nats).
       # Apply Miller-Madow bias correction: (R-1)(C-1)/(2N ln 2).
       # Return bits.
       ...

   @dataclass(frozen=True, slots=True)
   class StrongBialekResult:
       bits_per_sec: float
       std_err_bits_per_sec: float
       r_squared: float
       h_total_per_t: dict[int, float]
       h_noise_per_t: dict[int, float]

   def compute_mi_strong_bialek_bits_per_sec(
       *,
       spike_trains_by_direction: dict[float, list[NDArray[np.float64]]],
       word_lengths_ms: tuple[int, ...] = (25, 50, 75, 100),
       dt_ms: float = 5.0,
       trial_duration_ms: float = 1400.0,
   ) -> StrongBialekResult:
       # For each T in word_lengths_ms:
       #   Discretise each trial's spike train into binary words at dt_ms = 5 ms,
       #   pool words across all directions for H_total(T), and across each
       #   direction's trials for H_noise(T). MI_at_T = H_total - <H_noise>_D.
       # Fit MI_at_T / T against 1/T via scipy.stats.linregress.
       # Intercept = bits_per_sec.
       ...
   ```

   The Miller-Madow correction term is `(R-1)*(C-1) / (2.0 * N * math.log(2))` where R = 4
   (directions), C = `n_bins` (spike-count bins), N = 12 (total trials per cell). Convert sklearn's
   nat output to bits via `/ math.log(2)`. The Strong-Bialek estimator pools words across all 8
   directions x 20 trials = 160 trials per cell; at T=100 ms with `dt=5 ms` each trial yields
   `1400 / 100 = 14` words, total ~2200 words per cell at largest T (per research_code.md "T=100 is
   the noisiest at 2200 observed words vs 2^20 possible"). Expected output:
   `uv run python -c "from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.mi_estimator import compute_mi_count_bits, compute_mi_strong_bialek_bits_per_sec; print('ok')"`
   prints `ok`. Satisfies REQ-12.

8. **Edit `code/evaluator.py` to wire the new objectives.** Apply the following changes:

   * Drop the `cytoplasm_volume_um3: float` field from the `CellEvalResult` dataclass and add:
     `mi_count_bits: float`, `atp_per_spike_molecules: float`, `atp_per_ap_molecules: float` (mean
     per-AP ATP, the per-AP scalar before dividing by spike count),
     `atp_per_ap_compartment_breakdown: dict[str, float]` (with `soma`, `ais`, `dendrites_total`
     keys), `firing_hz_per_dir: dict[str, float]` (with `dir_0`, `dir_90`, `dir_180`, `dir_270`
     keys).
   * Drop the `compute_cytoplasm_volume_um3` import and add
     `from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.atp_per_spike import ( compute_atp_per_spike, compute_atp_per_ap, detect_ap_windows, InaRecorders)`
     and `from ... .code.mi_estimator import compute_mi_count_bits`.
   * Inside `_run_one_trial`, after building the cell but before `h.run()`, call
     `recorders = attach_ina_recorders_for_atp(h=h, cell=cell.morphology_result)` (from
     `code/recorder.py`) when `mode == FULL` (skip for EPSP / IPSP passive modes per the task
     description). After `h.run()`, call
     `ap_windows = detect_ap_windows(t_ms=t_vec, v_soma_mv=v_soma_vec)` then
     `atp_per_ap = compute_atp_per_ap(recorders=recorders, ap_windows=ap_windows, cell=cell.morphology_result)`.
     Store the per-trial spike count, AP timings, and per-AP ATP results on the per-trial dataclass.
   * Inside `evaluate_68d_vector`, after the trial loop completes, aggregate:
     * Concatenate per-trial spike counts and direction labels (12 entries each) into arrays, call
       `mi_count_bits = compute_mi_count_bits(direction_labels=..., spike_counts=..., n_bins=4)`.
     * Concatenate all per-AP ATP results across trials, call
       `atp_per_spike = compute_atp_per_spike(atp_per_ap_results=...)` (returns NaN if zero spikes,
       which is then filtered by the silence guard).
     * Compute per-direction firing rates (mean spikes / 1.4 s) and assemble the `firing_hz_per_dir`
       dict.
     * Compute per-compartment ATP breakdown and assemble the `atp_per_ap_compartment_breakdown`
       dict (`soma`, `ais`, `dendrites_total`).
   * Rewrite `BedBV3MorphProblem._evaluate` to emit:
     `out["F"] = np.array([-result.mi_count_bits, +result.atp_per_spike_molecules])` (MI negated
     because maximised; ATP NOT negated because minimised). Keep `n_obj = 2`. If `atp_per_spike` is
     NaN (zero spikes) AND silence guard fires (`pd_spikes_sum < 3`), replace with worst-case
     sentinel value `(0.0, WORST_CASE_ATP_PER_SPIKE)` and mark `silence_failed_bool=True`.
   * KEEP the silence guard at `pd_spikes_sum < 3` (constant `SILENCE_PD_SPIKES_THRESHOLD: int = 3`
     from t0122 stays verbatim). Per research_code.md "Tightened DSI silence guard from t0122
     carries over even though DSI is not optimised", the silence guard is still essential
     defensively even though DSI is no longer the optimised objective; the optimiser will push
     toward cells that never spike (ATP / spike is undefined; sentinel-value substitution leads to
     LEGIT-filter exclusion downstream).
   * Update `code/test_evaluator_dsi_guard.py` import paths and dataclass field references to match
     the new schema; keep the `>= 3 PD spikes` threshold assertion.

   Expected output:
   `grep -n "mi_count_bits\|atp_per_spike_molecules\|out\[.F.\]\|SILENCE_PD_SPIKES_THRESHOLD" code/evaluator.py`
   returns the new fields, the rewritten `out["F"]` line, and the preserved silence-guard constant.
   Satisfies REQ-13.

9. **Edit `code/smoke_gate.py` to add the Carter-Bean 2009 check.** Keep the 8 inherited t0122
   checks (with the cytoplasm-volume sanity check replaced by an MI / ATP sanity range check that
   asserts `mi_count_bits` is in `[0.0, 2.0]` and `atp_per_spike_molecules` is in `[1e7, 1e11]` on
   the canonical anchor cell). ADD a 9th check:

   ```python
   def check_carter_bean_atp_per_ap_at_ais(*, h, anchor_cell) -> CheckResult:
       # Build canonical Bed B anchor cell.
       # Run 1400 ms FULL trial with PD bar.
       # Compute total ATP at the AIS (sum of ais_proximal + ais_distal compartments)
       # over all detected APs.
       # Divide by AIS axial length in cm (sum of sec.L * 1e-4 for ais_proximal + ais_distal)
       # to get ATP/AP/cm.
       # Compare to Carter-Bean 2009 benchmark ~4 mM-mol/cm = 2.41e21 ATP/cm.
       # PASS if within 30%; FAIL otherwise.
       benchmark_atp_per_ap_per_cm = 2.41e21
       observed = atp_per_ap_at_ais / ais_length_cm
       deviation = abs(observed - benchmark_atp_per_ap_per_cm) / benchmark_atp_per_ap_per_cm
       return CheckResult(name="carter_bean_atp_per_ap_at_ais", passed=deviation <= 0.30,
                          observed=observed, expected=benchmark_atp_per_ap_per_cm,
                          deviation_fraction=deviation)
   ```

   The check uses the canonical t0083 Bed B best-cell electrophys vector loaded via
   `_load_t0083_best_cell_electrophys()` (inherited from t0122). Defer this check to the remote
   machine (no NEURON locally on Windows); it runs as part of the smoke-gate sweep executed on the
   Vast.ai instance after `nrnivmodl` builds the t0080 mods. Per research_code.md "Carter-Bean 2009
   smoke gate is the load-bearing pre-launch sanity check", discrepancies > 30% indicate a recipe
   error (most commonly a `seg.area()` unit-conversion bug) and must be fixed before launching
   NSGA-II. Expected output: the smoke gate prints `PASS` for all 9 checks (8 inherited + 1 new
   Carter-Bean). Satisfies REQ-14.

### Milestone 2 — Remote Provisioning and Smoke Gate (Steps 10-11)

10. **Provision the Vast.ai instance.** Use the orchestrator's `/setup-remote-machine` skill to
    provision a single Vast.ai EPYC 32-core or 64-core instance (whichever is cheapest at
    provisioning time). Required filters: `>= 64 GB RAM`, `reliability >= 0.99`, `dph <= 0.40`,
    prefer 64-core EPYC 7B13 to inherit the t0113 / t0114 / t0115 / t0122 wall-clock characteristic.
    The orchestrator writes the selected offer (including `selected_offer.price_per_hour`) to
    `logs/steps/008_setup-machines/machine_log.json`; the cost watchdog reads the hourly rate from
    this file at startup. Expected output: `cat logs/steps/008_setup-machines/machine_log.json`
    shows a `success: true` entry with a non-empty `selected_offer.id`. Satisfies REQ-15.

11. **[CRITICAL] Run the smoke gate on the remote machine.** SSH into the provisioned instance, sync
    the task folder, compile the t0080 NEURON MOD library via `nrnivmodl` once. Then execute:

    ```bash
    PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
        --task-id t0123_bedb_mi_atp_per_spike_nsga2 -- \
        uv run python -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.smoke_gate
    ```

    The smoke gate runs all 9 checks (8 inherited from t0122 + the new Carter-Bean ATP/AP/cm check).

    **Validation gate**: the smoke gate is the trivial-baseline equivalent for this pipeline.
    **Baseline**: Carter-Bean 2009 benchmark `~4 mM-mol/cm = 2.41e21 ATP/cm` at the AIS on the
    canonical Bed B anchor cell. **Limit**: only the 1 anchor cell (not all 96 random-init cells).
    **Failure condition**: if the Carter-Bean ATP/AP/cm deviation > 30%, STOP and inspect the
    `seg.area()` unit-conversion path (most likely failure mode per research_code.md) — do NOT
    launch the NSGA-II run. Also FAIL if `mi_count_bits` is outside `[0.0, 2.0]` or
    `atp_per_spike_molecules` is outside `[1e7, 1e11]` on the anchor cell. **Individual
    inspection**: read the per-segment `seg.ina` integration output for 5 randomly selected dendrite
    segments and verify the integrated charge is positive and finite. Expected output: smoke gate
    prints `PASS` for all 9 checks AND prints
    `[carter_bean] observed=<X> ATP/cm, expected=2.41e21 ATP/cm, deviation=<Y>%`. Satisfies REQ-14.

### Milestone 3 — NSGA-II Run (Step 12, remote)

12. **[CRITICAL] Launch the NSGA-II run on Vast.ai.** Execute:

    ```bash
    bash tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/run_seed441.sh
    ```

    The shell script calls
    `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0123_bedb_mi_atp_per_spike_nsga2 -- uv run python -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.nsga2_driver --seed 441`.
    The driver:

    * Initialises `BedBV3MorphProblem(n_obj=2)` with
      `out["F"] = [-mi_count_bits, +atp_per_spike_molecules]`.
    * Runs NSGA-II with `pop_size=96`, `n_gen<=60`, `_POOL_RESTART_EVERY=10`,
      `TerminationCollection = {MaximumGenerationTermination(60), CostWatchdogTermination(hard_budget_usd=6.0, per_instance_watchdog_usd=5.0), OperatorStopTermination(stop_md_path)}`.
    * Writes per-gen dill checkpoints to
      `logs/steps/009_implementation/checkpoints/checkpoint_seed441_gen<NNNN>.pkl`.
    * Writes per-gen `hv_trace.jsonl` with HV, best `mi_count_bits`, min `atp_per_spike`,
      `n_legit_cells`, cumulative cost.

    **Validation gate (expensive operation)**: the NSGA-II run consumes the bulk of the $6 budget,
    so the first 3 generations must be inspected before continuing. **Baseline**: t0122's clean
    60/60-gen run at $0.50 (substrate health proxy); inner-loop `mi_count_bits` should reach ~0.5
    bits by gen 3 on a 4-direction 12-trial protocol on this substrate (lower bound from spike-count
    plug-in MI). **Limit**: stop and inspect after generation 3 (288 evaluations, ~10-20 minutes
    given doubled per-cell evaluation cost). **Failure condition**: if after 3 gens the population's
    best `mi_count_bits` is < 0.1 bits (essentially random) OR more than 95% of cells fail the
    silence guard (zero LEGIT cells), STOP, inspect the per-gen JSONL, and debug before continuing
    to gen 60. A best-MI < 0.1 at gen 3 is anomalously low and indicates a bug in the new objective
    vector. **Individual inspection**: read 5 individual `CellEvalResult` JSON entries from the
    gen-3 checkpoint and verify each has a sensible `mi_count_bits` (in `[0.0, 2.0]`), a sensible
    `atp_per_spike_molecules` (in `[1e7, 1e11]` for non-silent cells), and a sensible
    `objective_F_minimised` (first axis negative, second axis positive).

    **Operator-stop trigger**: the operator monitors the HV trajectory live via
    `tail -f logs/steps/009_implementation/hv_trace.jsonl` and creates `intervention/stop.md` when
    HV visibly plateaus. The `OperatorStopTermination` polls this file every 10 seconds. Expected
    output: the driver prints `[driver] terminated by stop_trigger=<X>` where `X` is one of
    `{max_gen, cost_watchdog, operator_stop}`. Satisfies REQ-16.

### Milestone 4 — Post-Run Analysis and Asset Building (Steps 13-18, local CPU + remote for Step 13)

13. **[CRITICAL] Post-hoc Strong-Bialek rerun on the top-10 Pareto cells.** Still on the Vast.ai
    instance (to avoid re-bootstrap cost), execute the NEW `code/post_hoc_strong_bialek.py` script:

    ```bash
    PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
        --task-id t0123_bedb_mi_atp_per_spike_nsga2 -- \
        uv run python -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.post_hoc_strong_bialek \
        --seed 441 --top-n 10 --n-directions 8 --n-trials 20
    ```

    The script:

    * Loads `results/data/pareto_front_seed441.json` (written by the driver at termination).
    * Ranks the Pareto cells by `mi_count_bits` (descending) and takes the top 10.
    * For each cell: rebuilds the morphology via the canonical `generate_fixed_morphology` from
      t0092, applies the 54-d electrophys params via `apply_parameter_vector`, runs 8 directions x
      20 trials per direction in FULL mode (160 trials total per cell, 1400 ms each).
    * Collects per-trial spike times (not just counts; the Strong-Bialek estimator needs the full
      binary word at `dt=5 ms` resolution).
    * Calls
      `compute_mi_strong_bialek_bits_per_sec(spike_trains_by_direction=..., word_lengths_ms=(25, 50, 75, 100), dt_ms=5.0)`
      from `code/mi_estimator.py`.
    * Writes `results/data/post_hoc_strong_bialek_mi_top10.json` with per-cell:
      `{cell_index, mi_strong_bialek_bits_per_sec, std_err_bits_per_sec, r_squared, h_total_per_t, h_noise_per_t, mi_count_bits (cross-validation against inner-loop value), atp_per_spike_molecules}`.

    **Validation gate**: this is an additional ~$0.20-0.50 of compute on the same instance.
    **Baseline**: Dhingra and Smith 2004 reports 20-30 bits/s on guinea-pig RGCs; Niven 2007 reports
    200-1000 bits/s on fly photoreceptors. The DSGC bits/s is unmeasured but expected in `[10, 500]`
    bits/s (RGC-scale, well below fly-photoreceptor scale). **Failure condition**: if any top-10
    cell returns `bits_per_sec > 5000` (impossibly high — would indicate an entropy calculation
    bug) or `r_squared < 0.5` (poor 1/T linear fit on the 4 T values), flag in the output and
    inspect individually before downstream Step 14 uses them. **Individual inspection**: read the
    per-T `(H_total - <H_noise>) / T` values for the top-3 cells; verify they decrease monotonically
    with `1/T` (Strong-Bialek's required behaviour). Expected output:
    `results/data/post_hoc_strong_bialek_mi_top10.json` exists with 10 entries, all with finite
    `bits_per_sec` and `r_squared >= 0.5`. Satisfies REQ-18.

14. **Sync results back and build all Pareto / Niven / Carter-Bean charts.** Use the orchestrator's
    `sync_results_back.sh` (forked from t0122) to copy `logs/`, `results/data/`, and intermediate
    checkpoints back to the local repo. Then run:

    ```bash
    PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
        --task-id t0123_bedb_mi_atp_per_spike_nsga2 -- \
        uv run python -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.build_pareto_plots \
        --seed 441
    ```

    The script produces three charts:

    * `results/images/pareto_front_mi_vs_atp.png` — scatter with `atp_per_spike_molecules` on the
      x-axis, `mi_count_bits` on the y-axis, Pareto-front cells highlighted in red, all evaluated
      cells in grey. Mirror of t0122's `pareto_front_dsi_vs_volume.png` with axis relabelling.
    * `results/images/niven_2007_comparison.png` — top-10 cells from
      `post_hoc_strong_bialek_mi_top10.json` plotted as scatter in
      `(atp_per_spike_molecules, mi_strong_bialek_bits_per_sec)` space with the Niven 2007 4-species
      fly-photoreceptor curve overlaid (D. melanogaster 200 bits/s, D. virilis 400, M. domestica
      700, S. carnaria 1000 bits/s, fixed ~20% baseline cost annotated, super-linear scaling
      reference line via `bits_per_sec ~ atp_per_spike^1.5` fitted to the 4 fly points). Each cell
      annotated as "above curve" / "on curve" / "below curve".
    * `results/images/carter_bean_atp_per_ap_check.png` — histogram (or strip plot) of
      `atp_per_ap_at_ais` for the canonical Bed B anchor cell + top-10 Pareto cells, with the
      Carter-Bean 2009 `~4 mM-mol/cm = 2.41e21 ATP/cm` benchmark overlaid as a horizontal reference
      line and a +/-30% acceptance band shaded.

    Reuses t0122's matplotlib idioms (`build_pareto_plots.py` lines 26-100 for scatter and
    Pareto-front highlighting) and `build_top50_morphologies.py`'s `LineCollection` pattern.
    Expected output: all three PNG files exist, each > 100 KB, with the required axes / legend /
    annotations. Satisfies REQ-19, REQ-20, REQ-21.

15. **Build the top-50 morphology grid (full dendrite trees).** Run:

    ```bash
    PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
        --task-id t0123_bedb_mi_atp_per_spike_nsga2 -- \
        uv run python -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.build_top50_morphologies \
        --seed 441
    ```

    This script is a verbatim copy of t0122's `build_top50_morphologies.py` (323 lines) with only
    the input / output filename edits (`all_evaluations_seed441.json` and
    `top50_morphologies_seed441.png`) and the ranking objective (now by `mi_count_bits` descending).
    The script uses `LineCollection` over `section_endpoints_xy.items()` excluding soma and AIS,
    with the soma drawn as a separate `Circle` patch. **CRITICAL** — per memory
    `feedback_top50_morphologies_full_dendrites.md` and the t0114 failure mode, this chart MUST draw
    the full dendrite trees, NOT just soma dots. Expected output:
    `results/images/top50_morphologies_seed441.png` exists, is > 200 KB, and visually shows 50
    dendrite trees in a 10x5 (or 7x8) grid. Satisfies REQ-22.

16. **Build `results/metrics.json`.** Run:

    ```bash
    PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
        --task-id t0123_bedb_mi_atp_per_spike_nsga2 -- \
        uv run python -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.metrics_builder
    ```

    The script uses the explicit multi-variant format per
    `arf/specifications/metrics_specification.md`. Variant set:

    * Variant `best_legit` — best Pareto-cell stats in the LEGIT cohort (DSI >= 0.5 AND PD-rate
      > = 30 Hz AND NOT silence-failed): `direction_selectivity_index`, `mi_count_bits`,
      > `atp_per_spike_molecules`.
    * Variant `overall_max_mi` — population-wide max `mi_count_bits`:
      `direction_selectivity_index`, `mi_count_bits`, `atp_per_spike_molecules`.
    * Variant `overall_min_atp` — population-wide min `atp_per_spike_molecules`:
      `direction_selectivity_index`, `mi_count_bits`, `atp_per_spike_molecules`.
    * Variant `top10_strong_bialek` — aggregate over the top-10 Pareto cells from Step 13:
      `mi_strong_bialek_bits_per_sec`, `atp_per_spike_molecules`, `niven_2007_above_below_count`
      (count of cells above the fly curve).

    **Registered metrics applicability check** (per planning skill Phase 1 step 7): of the 4
    registered metrics, `direction_selectivity_index` applies as a tracked diagnostic (DSI is
    computed per cell, included in the LEGIT filter, and reported in 3 of the 4 variants).
    `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse` do NOT apply: this task
    uses 4 antipodal directions only, not a full angular sweep with a target tuning curve. The
    ad-hoc keys `mi_count_bits`, `atp_per_spike_molecules`, `mi_strong_bialek_bits_per_sec`,
    `niven_2007_above_below_count` are reported alongside DSI even though they are not in
    `meta/metrics/`; if the verificator rejects them, the implementing agent drops the
    non-registered keys from `metrics.json` and surfaces the values only in the predictions asset
    and via the orchestrator-managed detailed-results write-up.

    Expected output: `results/metrics.json` exists, parses as JSON, has a `variants` list with 4
    entries, and `direction_selectivity_index` appears in 3 variants' metrics blocks. Satisfies
    REQ-23.

17. **Build the predictions asset.** Run:

    ```bash
    PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
        --task-id t0123_bedb_mi_atp_per_spike_nsga2 -- \
        uv run python -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.build_predictions_assets \
        --seed 441
    ```

    The script creates `assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/` with:

    * `details.json` — `spec_version: "2"`, `predictions_id: "nsga2-mi-atp-per-spike-bedb-morph"`,
      `prediction_format: "jsonl.gz"`, per-cell schema
      `{generation, cell_index, vector_68d, mi_count_bits, atp_per_spike_molecules, atp_per_ap_molecules, atp_per_ap_compartment_breakdown, firing_hz_per_dir, dsi_vector_sum, pd_rate_hz, objective_F_minimised, silence_failed_bool, legit_bool}`.
      For the 10 cells that participated in the Strong-Bialek rerun, the row additionally contains
      `mi_strong_bialek_bits_per_sec`, `std_err_bits_per_sec`, `r_squared`.
      `created_by_task: "t0123_bedb_mi_atp_per_spike_nsga2"`,
      `metrics_at_creation: {best_mi_count_bits, min_atp_per_spike, niven_2007_above_below_count, n_generations_completed, n_cells_total, final_hypervolume, final_cost_usd, stop_trigger}`.
    * `description.md` — the canonical documentation document per
      `meta/asset_types/predictions/specification.md`.
    * `files/predictions.jsonl.gz` — every per-cell row from `all_evaluations_seed441.json` as
      gzipped JSONL.

    Expected output: asset folder exists with all three files and passes
    `meta.asset_types.predictions.verificator`. Satisfies REQ-24.

18. **Build the answer asset.** Run:

    ```bash
    PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs \
        --task-id t0123_bedb_mi_atp_per_spike_nsga2 -- \
        uv run python -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.build_assets \
        --answer dsgc-bits-per-atp-vs-niven-2007
    ```

    The script creates `assets/answer/dsgc-bits-per-atp-vs-niven-2007/` with:

    * `details.json` per `meta/asset_types/answer/specification.md` (`spec_version` per the current
      answer spec, `answer_id`, `short_answer_path`, `full_answer_path`, `question`,
      `answer_methods`).
    * Canonical short answer document — opens with "Yes" / "No" / "Partially" / "Insufficient
      evidence" depending on the top-10 Strong-Bialek bits/s vs ATP/spike distribution: "Yes" if the
      top-10 cells trace a super-linear curve consistent with Niven 2007 (above the fixed ~20%
      baseline cost line AND with a `bits_per_sec ~ atp_per_spike^p` exponent `p > 1.0` from a
      log-log linear fit); "No" if the cells are sub-linear (`p < 1.0`) or below the fixed-cost
      line. 2-5 sentences total.
    * Canonical full answer document — explains the Niven 2007 4-species curve (D. melanogaster
      200 bits/s up to S. carnaria 1000 bits/s; fixed ~20% baseline cost), the Strong-Bialek 1998
      direct-method MI calculation, the Carter-Bean 2009 ATP/AP/cm calibration, the Sengupta 2010
      ATP recipe; lists the top-10 cells' `(atp_per_spike_molecules, mi_strong_bialek_bits_per_sec)`
      pairs; reports the log-log fit `p` exponent; cross-references
      `results/images/niven_2007_comparison.png` and
      `results/images/carter_bean_atp_per_ap_check.png`. Includes a `## Sources` section with
      reference link definitions for Niven 2007 (`10.1242_jeb.005249`), Strong 1998
      (`10.1103_PhysRevLett.80.197`), Dhingra and Smith 2004, Sengupta 2010, Carter and Bean 2009,
      and the cited task IDs (`t0097`, `t0122`, `t0123`).

    **Stopping criterion for evidence** (per answer-question task type guideline): evidence is
    sufficient when the top-10 Strong-Bialek bits/s values are all finite and the log-log fit
    `r_squared >= 0.5`. If fewer than 10 LEGIT cells exist in the final population, the answer says
    "Insufficient evidence" and reports the partial result with the n LEGIT cells available.

    Expected output: answer asset folder exists with all three files and passes
    `meta.asset_types.answer.verificator`. Satisfies REQ-25.

* * *

## Remote Machines

**Required.** One Vast.ai EPYC instance (32-core or 64-core, whichever is cheapest at provisioning
time), single-instance run, ~4-8 hours of compute for NSGA-II plus 30-60 minutes for the post-hoc
Strong-Bialek rerun. Selection filters: `>= 64 GB RAM`, `reliability >= 0.99`, `dph <= 0.40`. Idle
GPU acceptable; the workload is CPU-bound NEURON. The compiled t0080 NEURON MOD library
(`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`) ships in the repo with pre-compiled
`.c` files; the remote machine runs `nrnivmodl` once at bootstrap to produce
`x86_64/.libs/libnrnmech.so`. The cost watchdog reads `selected_offer.price_per_hour` from
`logs/steps/008_setup-machines/machine_log.json` and tears down the instance on the $5 per-instance
cap. Reference: `arf/specifications/remote_machines_specification.md`.

* * *

## Assets Needed

* **From `t0024_port_de_rosenroll_2026_dsgc`** — canonical Bed B cell builder, NEURON bootstrap
  helpers (`_ensure_neuron_on_path`), AR(2) noise generator (`generate_ar2_batch`), bar-arrival
  kinematic helpers. Imported by full dotted path through the verbatim copy of `trial_helpers.py`.
* **From `t0080_bedb_mobo_v3_dendritic_spike_nsga2`** — 54-d electrophys parameter scheme,
  `apply_parameter_vector`, `ensure_t80_dll_loaded` (process-singleton MOD library loader), 13
  compiled NEURON channels including the three Na channels (`nav16t80`, `napt80`, `nart80`) whose
  summed `seg.ina` is the substrate variable of the Sengupta 2010 ATP recipe. Imported by full
  dotted path through the verbatim copy of `apply_params.py`.
* **From `t0083_bedb_v3_extend_nsga2_gen8plus`** — canonical Bed B best-cell electrophys vector
  used as the smoke-gate anchor (`tasks/t0083_*/results/data/pareto_front.json`); loaded via the
  inherited `_load_t0083_best_cell_electrophys()` helper. Inherited through the t0122 fork.
* **From `t0090_morphology_generator_diversity_test`** — 14-d morphology parameter space,
  `MorphologyParams`, `MorphologyResult` (whose `soma`, `all_dends`, `ais_proximal`, `ais_distal`
  `h.Section` handles are the substrate for `seg.ina` recording), `PARAM_BOUNDS`, `INT_PARAM_NAMES`,
  `PARAM_*` string constants. Imported by full dotted path per C-0093-01.
* **From `t0092_diagnose_morphology_generator_silence`** — `generate_fixed_morphology` (the
  canonical morphology entry point with the z-axis soma area patch ensuring `seg.area()` returns the
  intended `~220 um^2`), `insert_baseline_channels`. Imported by full dotted path through the
  verbatim copy of `generator_wrapper.py`.
* **From `t0097_multi_obj_optim`** — the
  `objective-functions-for-single-neuron-multi-objective-optimisation` answer asset providing the
  explicit Strong-Bialek 1998 direct-method MI recipe (full_answer.md lines 287-324) and the
  Sengupta 2010 ATP-per-spike recipe (lines 326-372). Read once during planning; not imported by
  code.
* **From `t0106_long_pdnd_nsga2_300gen`** — NSGA-II driver substrate (parent of the lineage),
  `PerGenerationPoolRestart` callback, `OperatorStopTermination`. Inherited through the t0115 /
  t0122 fork chain.
* **From `t0115_seed9354_no_autostop`** — source of the 763-line `nsga2_driver.py` design.
  Inherited through the t0122 fork.
* **From `t0120_morph_generator_geometry_audit`** — gating dependency (transitive from t0122);
  verdict "rendering-only / no re-runs needed" already confirmed at t0122 launch.
* **From `t0122_dsi_cytoplasm_volume_nsga2`** — fork point for `code/` (~30 Python files copied
  verbatim and minimally patched). t0122's clean termination at 60/60 gens for $0.50 confirms the
  substrate is healthy.

* * *

## Expected Assets

Matches `task.json` `expected_assets: {"predictions": 1, "answer": 1}`:

* **predictions / `nsga2-mi-atp-per-spike-bedb-morph`** — per-cell 68-d vectors, F vector
  `[-mi_count_bits, +atp_per_spike_molecules]`, per-direction firing rates,
  `atp_per_spike_molecules`, `atp_per_ap_molecules`, per-compartment ATP breakdown, DSI / PD-rate
  diagnostics. The 10 cells that participated in the Strong-Bialek rerun additionally carry
  `mi_strong_bialek_bits_per_sec`, `std_err_bits_per_sec`, `r_squared`. Format: gzipped JSONL. Built
  by Step 17. Satisfies the `predictions: 1` count.
* **answer / `dsgc-bits-per-atp-vs-niven-2007`** — answer to "Where does the DSGC bits-per-ATP
  front sit relative to Niven 2007's fly-photoreceptor curve, and does it match the Niven
  super-linear cost-vs-information scaling?" with the top-10 Strong-Bialek `(bits/s, ATP/spike)`
  distribution as primary evidence, the log-log fit exponent `p` quantifying the curvature, and the
  count of cells above / on / below the Niven curve. Built by Step 18. Satisfies the `answer: 1`
  count.

* * *

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already done) | done |
| Planning (already done) | done |
| Implementation Milestone 1 (steps 1-9, fork + edit + 3 new modules, local) | 3-5 hours |
| Implementation Milestone 2 (steps 10-11, provisioning + smoke gate) | 1-2 hours |
| Implementation Milestone 3 (step 12, NSGA-II remote run) | 4-8 hours (operator-stop or 60-gen ceiling) |
| Implementation Milestone 4 (steps 13-18, Strong-Bialek rerun + charts + metrics + assets) | 2-4 hours |
| **Total** | **10-19 hours** |

* * *

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `seg.area()` unit-conversion bug (factor `1e-2` vs `1e-8` confusion) yields a 6-order-of-magnitude error in ATP estimates and an unusable Pareto front. | Medium | High (entire run produces wrong ATP axis; Niven 2007 comparison meaningless) | Step 11 Carter-Bean 2009 smoke gate explicitly checks the AIS ATP/AP/cm is within 30% of the `2.41e21 ATP/cm` benchmark; if it deviates by orders of magnitude, the unit-conversion bug is caught BEFORE launching the $1-4 NSGA-II run. Unit-test `compute_atp_per_ap` on a synthetic AP trace with known integrated current (Step 6) as a second sanity check before wiring into `evaluator.py`. |
| Spike-count MI sign flip in `out["F"]` (forgetting to negate the maximised MI) drives the optimiser to MINIMISE MI instead of maximising. | Low | High (entire run produces inverted Pareto front) | Step 11 smoke gate inspects an anchor cell's `objective_F_minimised[0]` and asserts it is negative (`-mi_count_bits`). Step 12 validation gate at gen 3 confirms best MI value increases (not decreases) over the first 3 generations. If MI decreases gen-to-gen, STOP and check the sign convention. |
| Strong-Bialek 1/T extrapolation gives nonsense `bits_per_sec` (negative intercept, or `r_squared < 0.3`) on the top-10 cells, breaking the Niven 2007 comparison. | Medium | Medium (answer asset reports "Insufficient evidence" instead of a comparison verdict) | Step 13 validation gate flags any top-10 cell with `r_squared < 0.5` for individual inspection. If the issue is systematic (e.g., word-length sweep too coarse), expand to `T in {15, 25, 50, 75, 100, 150} ms` and re-fit. The 4 fly photoreceptors in Niven 2007 give a known bits/s range (200-1000); DSGC values below 10 or above 5000 bits/s are flagged as anomalous. |
| Silence-guard regression: per-cell silence rate is much higher under the new ATP objective (the optimiser prefers cheap-because-silent cells), shrinking the LEGIT cohort to < 10 cells and triggering "Insufficient evidence" for the answer asset. | Medium | Medium (answer asset is "Insufficient evidence"; predictions asset still produced but less informative) | The silence guard `pd_spikes_sum < 3` is preserved from t0122 verbatim and replaces the F vector with `(0.0, WORST_CASE_ATP_PER_SPIKE)` for silent cells, marking them `silence_failed_bool=True` so they are excluded from the LEGIT cohort by the downstream filter. If fewer than 10 LEGIT cells survive at gen 60, the answer asset reports "Insufficient evidence" with the partial result. |
| Vast.ai instance fails to provision (no offers under $0.40/hr at provisioning time, or account balance below $7). | Low | Medium (delays run; orchestrator must retry or wait for account top-up) | Setup-machines step retries up to 5 offers automatically. If all fail, the operator can manually relax `dph <= 0.40` to `dph <= 0.50` in the offer filter. The Vast.ai balance check in Step 1 catches the "balance below $7" case before any provisioning is attempted, allowing the operator to top up. |
| Cost watchdog races with operator-stop and exceeds the $6 cap by a few cents. | Low | Low (Vast.ai charges only consumed seconds; per-instance $5 cap leaves $1 buffer) | The $5 per-instance watchdog cap is intentionally $1 below the $6 task cap to absorb any race. Worst case is $0.10-0.50 over the per-instance cap; well within the buffer. |
| Top-50 morphology chart drawn as soma-only (the t0114 failure mode). | Low | High (operator rejects the asset; chart must be redone) | Step 15 reuses t0122's `build_top50_morphologies.py` verbatim with only filename and ranking-objective edits; the `LineCollection` over `section_endpoints_xy.items()` excluding soma / AIS is preserved. After Step 15, the operator visually verifies the chart shows dendrite trees before Step 16 proceeds. |
| HV-plateau auto-stop accidentally re-enabled (e.g., by a copy-paste error in `nsga2_driver.py`). | Low | Medium (run terminates early before reaching the meaningful Pareto front) | Step 11 smoke gate introspects the live `TerminationCollection` and asserts `HVPlateauTermination` is NOT in it. If it is, STOP and remove it. `HV_PLATEAU_AUTO_STOP = False` constant in `code/constants.py` also serves as a documentation trail. |
| `seg.ina` recording footprint blows the worker memory budget on cells with > 300 dendritic segments (very long trees). | Low | Medium (workers OOM; pool restart cadence absorbs some but not all losses) | Per research_code.md, expected per-trial recording footprint is ~14 MB float64 at 200 segments. Long-tree outlier cells could reach ~30 MB. The `_POOL_RESTART_EVERY = 10` cadence already mitigates OOM accumulation; if individual workers OOM mid-generation, NSGA-II treats those evaluations as `(0.0, WORST_CASE_ATP_PER_SPIKE)` worst-case sentinels (same as silence-fail handling). |

* * *

## Verification Criteria

Each criterion is a concrete, testable check. The verificator commands use the full
`PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs ...` pattern enforced by
project rule 1.

* **C1 — `_POOL_RESTART_EVERY = 10` is enforced in code (REQ-1).** Run
  `grep -n "_POOL_RESTART_EVERY" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants.py` and
  confirm output contains `_POOL_RESTART_EVERY: int = 10`. Then run
  `grep -n "_POOL_RESTART_EVERY" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/nsga2_driver.py` and
  confirm the `PerGenerationPoolRestart` callback fires every `_POOL_RESTART_EVERY` generations.
  Expected: both greps succeed.

* **C2 — `HV_PLATEAU_AUTO_STOP = False` is enforced in code and the live termination collection
  excludes `HVPlateauTermination` (REQ-2).** Run
  `grep -n "HV_PLATEAU_AUTO_STOP" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants.py` and
  confirm output contains `HV_PLATEAU_AUTO_STOP: bool = False`. Then run
  `grep -A 5 "TerminationCollection" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/nsga2_driver.py`
  and confirm the active `TerminationCollection` contains exactly
  `{MaximumGenerationTermination, CostWatchdogTermination, OperatorStopTermination}` and does NOT
  contain `HVPlateauTermination`. Expected: both checks pass.

* **C3 — `POP_SIZE = 96` is enforced in code (REQ-3).** Run
  `grep -n "POP_SIZE" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants.py tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants_morphology.py`
  and confirm output contains `POP_SIZE: int = 96`. Expected: grep succeeds and value is exactly 96.

* **C4 — `N_EVAL_SEEDS = 3` is enforced in code (REQ-4).** Run
  `grep -n "N_EVAL_SEEDS" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants.py tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants_morphology.py`
  and confirm output contains `N_EVAL_SEEDS: int = 3`. Expected: grep succeeds and value is exactly
  3\.

* **C5 — `N_DIRECTIONS = 4` is enforced in code (REQ-5).** Run
  `grep -n "N_DIRECTIONS" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants_morphology.py` and
  confirm output contains `N_DIRECTIONS: int = 4`. Expected: grep succeeds and value is exactly 4.

* **C6 — `N_GEN_MAX = 60` is enforced in code (REQ-6).** Run
  `grep -n "N_GEN_MAX\|N_GEN " tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants.py tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants_morphology.py`
  and confirm output contains `N_GEN_MAX: int = 60` (or `N_GEN: int = 60`). Expected: grep succeeds
  and value is exactly 60.

* **C7 — `COST_CAP_USD = 6.0` is enforced in code and wired into the cost watchdog (REQ-7).** Run
  `grep -n "COST_CAP_USD\|T0123_HARD_BUDGET_USD" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants.py`
  and confirm output contains `COST_CAP_USD: float = 6.0` (or alias
  `T0123_HARD_BUDGET_USD: float = 6.0`). Then run
  `grep -n "hard_budget_usd" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/nsga2_driver.py` and
  confirm the `CostWatchdogTermination` is constructed with the $6 cap. Expected: both checks pass.

* **C8 — GA seed `T0123_SEEDS = (441,)` is set in code (REQ-9).** Run
  `grep -n "T0123_SEEDS" tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/constants.py` and confirm
  output contains `T0123_SEEDS = (441,)`. Expected: grep succeeds.

* **C9 — Carter-Bean 2009 smoke gate passes within 30% on the canonical anchor cell (REQ-14).**
  After Step 11 completes on the Vast.ai instance, check the smoke-gate log:
  `grep "carter_bean_atp_per_ap_at_ais.*PASS" tasks/t0123_bedb_mi_atp_per_spike_nsga2/logs/steps/008b_smoke_gate/run.log`
  returns at least one matching line. Expected: smoke gate prints
  `[carter_bean_atp_per_ap_at_ais] PASS observed=<X> ATP/cm, expected=2.41e21 ATP/cm, deviation=<Y>% (<= 30%)`.

* **C10 — Predictions asset passes its verificator (REQ-24).** Run
  `PYTHONIOENCODING=utf-8 uv run python -m meta.asset_types.predictions.verificator tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph`
  and confirm 0 errors. Expected: verificator prints "PASSED" (or returns exit code 0).

* **C11 — Answer asset passes its verificator (REQ-25).** Run
  `PYTHONIOENCODING=utf-8 uv run python -m meta.asset_types.answer.verificator tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/answer/dsgc-bits-per-atp-vs-niven-2007`
  and confirm 0 errors. Expected: verificator prints "PASSED" (or returns exit code 0).

* **C12 — `metrics.json` registers `direction_selectivity_index` as a tracked diagnostic in at
  least 3 of the 4 variants (REQ-23).** Run
  `PYTHONIOENCODING=utf-8 uv run python -c "import json; data = json.loads(open('tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/metrics.json').read()); variants = data['variants']; dsi_count = sum(1 for v in variants if 'direction_selectivity_index' in v['metrics']); assert dsi_count >= 3, f'DSI in only {dsi_count} variants'; print('OK')"`
  and confirm output is `OK`.

* **C13 — All required result files and charts exist (REQ-17, REQ-18, REQ-19, REQ-20, REQ-21,
  REQ-22).** Run
  `ls tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/data/pareto_front_seed441.json tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/data/all_evaluations_seed441.json tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/data/post_hoc_strong_bialek_mi_top10.json tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/pareto_front_mi_vs_atp.png tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/niven_2007_comparison.png tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/carter_bean_atp_per_ap_check.png tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/top50_morphologies_seed441.png`
  and confirm all 7 paths return a file. Expected: `ls` returns 7 paths with no "No such file"
  errors.

* **C14 — Plan verificator passes (REQ-coverage sanity check).** Run
  `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.verificators.verify_plan t0123_bedb_mi_atp_per_spike_nsga2`
  and confirm 0 errors. Expected: verificator prints "PASSED" (or returns exit code 0). This
  criterion also serves as the requirement-coverage check: PL-W006 fires if no `REQ-*` items are
  present, and PL-W007 fires if `## Step by Step` does not reference any `REQ-*`.
