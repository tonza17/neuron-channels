# NSGA-II DSI vs ATP-per-Spike Bed B + 14-d Morph: 60-gen Replication

## Source Suggestion

S-0124-01: "Fresh-seed 60-gen replication of DSI vs ATP-per-spike NSGA-II to test Carter-Bean
penalty vs artefact."

## Motivation

t0124 ran the first NSGA-II maximising DSI and minimising ATP-per-spike on the 68-d Bed B + 14-d
morphology substrate, but was truncated at gen 9 of 60 by operator_stop (subagent session budget
exhausted while polling NSGA-II progress; only $0.07 of the $6 cost cap had been spent and HV was
still ascending). The partial n=5 Pareto front showed bootstrap r(DSI, ATP) = +0.806 [0.716, 1.000],
suggestive of a Carter-Bean Na/K-overlap penalty -- but the result is **undeterminable from
artefact** because:

* `_POOL_RESTART_EVERY = 10` had not fired yet (the first scheduled fresh-pool injection is at gen
  10).
* All 5 cells share LHS-init ancestry from a single initial population.
* Diversity has not had time to build up across recombinant generations.

The Carter-Bean 2009 interpretation needs a fully-converged front to be falsifiable. This task is
the dedicated continuation: re-run the t0124 substrate verbatim with a fresh GA seed and run all 60
generations (no operator stop, no autostop), then re-assess the DSI-ATP correlation on the full
front.

## Gating Dependency

Depends on t0124 (provides the substrate, ATP recipe, Carter-Bean smoke-gate, seg.ina recorder, and
the reference partial result for cross-comparison). No new external prerequisites. Vast.ai balance
verified before launch.

## Scope

One NSGA-II run, single fresh GA seed, 2 objectives (DSI, ATP-per-spike), 60 generations, on the
68-d Bed B + 14-d morphology substrate. **Verbatim fork of t0124's protocol** -- no parameter
changes, no objective changes, no protocol changes. Only difference: fresh seed and execution to gen
60\.

## Hard Constraints (must be reproduced in plan and implementation)

These are inherited verbatim from t0124. The planning subagent must surface each one in
`plan/plan.md` `## Verification Criteria` with an explicit check, and the implementation subagent
must reproduce them in `code/constants.py`:

* `_POOL_RESTART_EVERY = 10` -- fresh random-init pool injection cadence (10th-gen rule).
* `HV_PLATEAU_AUTO_STOP = False` -- disabled per project policy.
* `POP_SIZE = 96`.
* `N_EVAL_SEEDS = 3`.
* `N_DIRECTIONS = 2` -- antipodal pair at 0deg (PD) / 180deg (ND).
* `N_GEN_MAX = 60` -- this run must reach gen 60 (no operator stop unless budget cap trips).
* `COST_CAP_USD = 6.0` -- matches t0124. Vast.ai balance to be re-verified immediately before
  launch; if balance < $7, reduce cap to balance - $1 (teardown buffer).

## DSI Recipe (silence-guarded ratio, inherited from t0124)

```text
R_PD = mean spike count over N_EVAL_SEEDS trials at 0deg
R_ND = mean spike count over N_EVAL_SEEDS trials at 180deg
DSI = (R_PD - R_ND) / (R_PD + R_ND)        if R_PD >= 3 spikes
DSI = -1.0                                  if R_PD < 3 spikes (silence guard)
```

Headline DSI variant: `best_legit`. Tracked variants: `best_legit`, `overall_max`,
`dsi_eq_one_count`.

## ATP-per-Spike Recipe (Sengupta 2010, inherited from t0124/t0123)

```text
N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int_{t_AP_start}^{t_AP_end} I_Na^inward(t) dt
```

Inherited verbatim from t0124's implementation:

1. Record `seg.ina` per segment at simulation `dt` for soma + AIS proximal + AIS distal + all
   dendritic segments. Re-use t0123/t0124's recorder.
2. Run only `FULL` mode for ATP estimation; EPSP/IPSP passive modes are skipped.
3. Detect AP windows from somatic Vm threshold crossing at -20 mV with 2 ms refractory; AP window =
   +/-2 ms around peak.
4. Convert `seg.ina` (mA/cm^2) per segment to total current via per-segment surface area, integrate
   over the AP window.
5. Inward-only restriction: `-min(I_Na, 0)` magnitude.
6. ATP per AP per compartment: `(Q^(c, AP) / e) / 3` with `e = 1.602e-19 C`.
7. Sum across compartments for per-AP per-cell ATP cost.
8. Headline objective: total ATP across all FULL-mode trials / total spike count across all
   FULL-mode trials. Lower is better.
9. If total spike count == 0, set `atp_per_spike = +inf` (sentinel).

### Smoke-gate (inherited from t0124, must re-run)

* Before launching NSGA-II, run the ATP recipe on the canonical Bed B cell and verify that per-AP
  ATP cost at the AIS matches Carter and Bean 2009 ~4 mM-mol/cm within 30%.
* If the smoke-gate fails, the run is aborted and the recipe is debugged.

## Approach

1. **Fork t0124's code verbatim** into `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/`:
   - Copy `code/constants.py`, `code/main.py`, `code/atp_per_spike.py`, `code/recorder.py`, and any
     other implementation modules from t0124.
   - Verify `_POOL_RESTART_EVERY = 10`, `HV_PLATEAU_AUTO_STOP = False`, `POP_SIZE = 96`,
     `N_EVAL_SEEDS = 3`, `N_DIRECTIONS = 2`, `N_GEN_MAX = 60`, `COST_CAP_USD = 6.0` assertions
     remain in `code/constants.py`.
2. **Draw a fresh non-round GA seed** via `secrets.randbelow(10000)` (t0113/t0115 convention).
   Record the seed in `code/constants.py` and `plan/plan.md`. The seed MUST differ from t0124's.
3. **Carter-Bean smoke-gate** on the canonical Bed B cell -- pass criterion identical to t0124.
4. **Run on Vast.ai EPYC** (32-core or 64-core, whichever is cheapest at provisioning time);
   single-instance.
5. **No operator stop**: this run must complete all 60 generations unless the $6 cost watchdog
   trips. The implementation subagent must launch NSGA-II in the background (decoupled from the
   subagent context budget per S-0124-02's framework concern) and poll only progress checkpoints,
   not the live training loop.
6. **Post-run analysis** (in this order, identical to t0124):
   * Pareto front in (DSI_best_legit, ATP_per_spike_molecules) space.
   * Bootstrap r(DSI, ATP) with 95% CI on the full final front (n >= 20 expected after 60 gens).
   * Per-cell diagnostics: PD-rate, ND-rate, cytoplasm volume (free), MI_count_bits (free).
   * Carter-Bean 2009 ATP-per-AP benchmark on the canonical cell and the top-3 Pareto cells.
   * Attwell-Laughlin 2001 47%-signalling-budget anchor for top-N cells.
   * Top-50 morphology grid (**full dendrite trees** per the project default, see memory
     `feedback_top50_morphologies_full_dendrites.md`).
   * HV trajectory chart (gen 1 -- gen 60) -- this is the headline new evidence vs t0124.
7. **Decision rule for the Carter-Bean question** (from S-0124-01):
   * If r(DSI, ATP) > +0.5 with 95% CI excluding 0 at n >= 20 on the full final front: ACCEPT
     Carter-Bean penalty interpretation.
   * If r drops below +0.3: ACCEPT the early-NSGA-II artefact null (t0124's +0.806 was a pre-restart
     LHS-ancestry artefact).
   * Anything in between: INDETERMINATE; report and recommend further replication.
8. **Cross-comparison with t0124**: render side-by-side fronts (t0124 partial vs t0126 full), report
   the gen-9 vs gen-60 correlation delta, and note whether the t0124 partial Pareto cells are
   dominated by the t0126 final front (expected if NSGA-II converged further).
9. **Answer asset**: write one answer asset answering "Does the t0124 +0.806 r(DSI, ATP) correlation
   survive a full 60-gen replication, or is it an early-NSGA-II artefact?"

## Expected Outputs

* `assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph-60gen/` -- predictions asset per spec, with
  per-cell 68-d vector, per-direction firing (PD / ND), DSI_best_legit, ATP_per_spike_molecules,
  ATP_per_AP_molecules per compartment group, PD-rate, ND-rate, cytoplasm_volume_um3 (diagnostic),
  MI_count_bits (diagnostic).
* `assets/answer/dsgc-dsi-vs-atp-per-spike-60gen-carter-bean-vs-artefact/` -- one answer asset
  answering the Carter-Bean penalty vs early-NSGA-II artefact question.
* `results/data/pareto_front_seed*.json` -- Pareto front cells.
* `results/data/all_evaluations_seed*.json` -- every evaluation.
* `results/images/pareto_front_dsi_vs_atp.png` -- Pareto front, DSI on y, ATP/spike on x.
* `results/images/pareto_front_t0124_vs_t0126.png` -- side-by-side comparison.
* `results/images/carter_bean_atp_per_ap_check.png` -- distribution of ATP/AP across top-10 with
  Carter-Bean 4 mM-mol/cm overlaid.
* `results/images/attwell_laughlin_signalling_budget.png` -- top-N implied signalling ATP rate vs
  47%-budget anchor.
* `results/images/top50_morphologies_seed*.png` -- top-50 morphology grid (full dendrite trees).
* `results/images/hv_trajectory_seed*.png` -- hypervolume vs generation (gen 1 -- gen 60).
* `results/results_summary.md`, `results/results_detailed.md`, `results/compare_literature.md`
  comparing to Attwell-Laughlin 2001 / Sengupta 2010 / Carter-Bean 2009 / Niven 2007 / Cuntz 2010
  (cross-reference to t0122) / Remme 2018, plus side-by-side with t0124.

## Budget

* Cost cap: **$6** (matches t0124; Vast.ai balance to be re-verified at launch).
* Expected actual: **$2-4** (t0124 spent $0.29 in 9 gens; scaling roughly linearly to 60 gens gives
  ~$2; allow margin for slower per-eval times under deeper-front recombinants).
* If the run exceeds $6 watchdog trip, stop and write up partial results.

## Verification Criteria

* `_POOL_RESTART_EVERY == 10`, `HV_PLATEAU_AUTO_STOP == False`, `POP_SIZE == 96`,
  `N_EVAL_SEEDS == 3`, `N_DIRECTIONS == 2`, `N_GEN_MAX == 60`, `COST_CAP_USD == 6.0` asserted in
  `code/constants.py` at module import.
* Fresh GA seed drawn via `secrets.randbelow(10000)` and recorded; must differ from t0124's seed.
* Smoke-gate verifies the canonical Bed B cell's ATP/AP at the AIS matches Carter and Bean 2009
  within 30%; if not, run aborted.
* NSGA-II reaches gen 60 (or the $6 cost watchdog trips). NOT operator-stopped at gen < 60.
* DSI silence-guard threshold == 3 PD spikes; cells below the guard receive DSI = -1.
* `metrics.json` registers (a) `direction_selectivity_index` with variants `best_legit`,
  `overall_max`, `dsi_eq_one_count`; (b) headline `atp_per_spike_molecules`; (c) diagnostic variants
  `pd_firing_rate_hz`, `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits`.
* Predictions asset passes `verify_predictions_asset`.
* Final Pareto front size n >= 20; bootstrap r(DSI, ATP) computed with 95% CI on the full final
  front.
* `compare_literature.md` includes the t0124 side-by-side comparison plus the literature anchors
  inherited from t0124.
* Answer asset states the Carter-Bean vs artefact verdict per the S-0124-01 decision rule with
  explicit quantitative comparison.

## Cross-References

* Source suggestion: S-0124-01.
* Direct precursor: t0124 (substrate, ATP recipe, Carter-Bean smoke-gate, seg.ina recorder).
* Lineage anchors: t0122 (DSI + cytoplasm volume), t0123 (MI + ATP-per-spike), t0097 (objective
  catalogue).
* Source papers: Sengupta et al. 2010 (`10.1371_journal.pcbi.1000840`), Carter and Bean 2009
  (`10.1016_j.neuron.2009.12.011`), Attwell and Laughlin 2001.
