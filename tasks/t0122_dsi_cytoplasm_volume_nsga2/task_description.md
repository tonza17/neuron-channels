# NSGA-II Maximising DSI and Minimising Cytoplasm Volume

## Source Suggestion

S-0097-01: "Bed B NSGA-II maximising DSI and minimising cytoplasm volume."

## Motivation

The t0097 multi-objective optimisation catalogue ranked DSI vs cytoplasm volume as the most
biologically-grounded objective pair in the project:

* Cajal's cytoplasm-conservation principle and Chklovskii et al. 2002's wiring-cost rule (3/5 of
  grey-matter volume is dendrites + axons for optimal wiring) make cytoplasm a primary evolutionary
  cost objective.
* Cuntz et al. 2010 (10.1371/journal.pcbi.1002107) operationalised this as a `balancing factor`
  `bf in [0.2, 0.7]` for real dendritic trees -- a falsifiable prediction the optimiser can be
  tested against.
* Cytoplasm volume per section = pi * (diameter / 2)^2 * length, summed over soma + dendrites + AIS.
  Easy to compute from the existing `MorphologyResult` without any new generator code.

This is the natural next NSGA-II direction after the 5-seed substrate-rate confirmation batch closed
at t0115. Recurring biological-plausibility concerns about pure-DSI-maximisation runs (the optimiser
hits NMDA / Nav densities 85-122 sigma above Sivyer 2013 priors) motivate adding a biological cost
objective. Cytoplasm volume was chosen over alternatives (ATP/spike, +-10% robustness) for cost
reasons -- it adds zero per-evaluation overhead since it is a pure geometric quantity computable
from the morphology.

## Gating Dependency

**This task must not start until `t0120_morph_generator_geometry_audit` has been completed and the
geometry-audit verdict is "rendering-only / no re-runs needed".** If the audit reveals a real
geometry bug, this task should be cancelled and a framework-level decision is needed about whether
to patch `_apply_asymmetry` and re-run all 68-d morphology-extended NSGA-II lineage tasks first.

## Scope

One NSGA-II run, single GA seed, 2 objectives, on the 68-d Bed B + 14-d morphology substrate that
has been validated by the t0106-t0115 lineage.

## Approach

1. **Copy the t0115 NSGA-II substrate** end-to-end: 68-d parameter vector (54-d electrophys + 14-d
   morphology), pop=96, N_EVAL_SEEDS=3, 2 antipodal directions (PD=0deg, ND=180deg), ratio DSI,
   silence-guard tightened to >= 3 PD spikes, `_POOL_RESTART_EVERY=10`, HV-plateau auto-stop
   DISABLED, $8 hard cap.
2. **Replace one objective**: drop the PD-rate objective from t0106's 2-objective configuration and
   replace with **cytoplasm volume**, computed as:
   `vol = sum(pi * (sec.diam/2)^2 * sec.L for sec in [soma, *all_dends, ais_proximal, ais_distal])`.
   Units: um^3. Objectives become (maximise DSI, minimise cytoplasm volume). PD-rate stays as a
   tracked diagnostic but is not an optimiser objective.
3. **GA seed**: draw via `secrets.randbelow(10000)` (avoid round-ish numbers; follow the t0113
   convention).
4. **Gen ceiling**: 60 (per the t0114/t0115 convention for auto-stop-disabled runs).
5. **Stop trigger**: operator stop when HV trajectory visibly plateaus, OR $8 cost cap, OR gen 60
   ceiling.
6. **Run on Vast.ai EPYC** (32-core or 64-core, whichever is cheapest at provisioning time);
   single-instance.
7. **Post-run analysis**: Pareto front in (DSI, cytoplasm_volume) space, joint-pass cells (DSI
   > = 0.5 AND PD-rate >= 30 Hz AND cytoplasm_volume <= TBD), per-cell morphology gallery for top
   > ranks, **Cuntz 2010 balancing-factor check**: compute `bf` for top-10 cells and verify whether
   > the high-DSI corner falls in the predicted `[0.2, 0.7]` band.
8. **Answer asset**: write one answer asset answering "Does NSGA-II with a cytoplasm-volume cost
   objective produce a high-DSI front in Cuntz 2010's predicted balancing-factor `[0.2, 0.7]` band?"

## Expected Outputs

* `assets/predictions/nsga2-cytoplasm-volume-bedb-morph/` -- predictions asset per spec, with
  per-cell 68-d vector + per-objective + per-direction firing.
* `assets/answer/cuntz-balancing-factor-prediction-check/` -- 1 answer asset on the Cuntz
  prediction.
* `results/data/pareto_front_seed*.json` -- Pareto front cells in (DSI, cytoplasm_volume).
* `results/data/all_evaluations_seed*.json` -- every evaluation.
* `results/images/pareto_front_dsi_vs_volume.png` -- Pareto front chart.
* `results/images/top50_morphologies_seed*.png` -- top-50 morphology grid (full dendrite trees per
  the project default).
* `results/images/cuntz_balancing_factor_top10.png` -- bf distribution for top-10 cells with Cuntz
  [0.2, 0.7] band overlaid.
* `results/results_summary.md`, `results/results_detailed.md`, `results/compare_literature.md`
  comparing to Hay 2011 / Cuntz 2010 / Mohacsi 2024.

## Budget

* Cost cap: **$8** (per-task default).
* Expected: ~$4-8 (one Vast.ai EPYC instance for 6-12 hours).
* If the run exceeds $8 watchdog trip, stop and write up partial results.

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` -- canonical Bed B cell.
* `t0080_bedb_mobo_v3_dendritic_spike_nsga2` -- 54-d electrophys parameter scheme + apply_params.
* `t0090_morphology_generator_diversity_test` -- procedural morphology generator.
* `t0092_diagnose_morphology_generator_silence` -- `generate_fixed_morphology` wrapper.
* `t0106_long_pdnd_nsga2_300gen` -- NSGA-II driver substrate (parent of the lineage).
* `t0115_seed9354_no_autostop` -- most recent run conventions to copy from.
* `t0119_brainstorm_results_23` -- commissions this task.
* **`t0120_morph_generator_geometry_audit` -- GATING DEPENDENCY**.

## Verification Criteria

* `t0120` verdict is "rendering-only / no re-runs needed" before this task starts.
* Predictions asset passes `verify_predictions_asset`.
* `metrics.json` registers `direction_selectivity_index` with explicit variants for `best_legit`,
  `overall_max`, `dsi_eq_one_count`.
* Cytoplasm volume formula is documented in `results_detailed.md` with per-section breakdown.
* Cuntz 2010 balancing-factor test result is reported as either "consistent with [0.2, 0.7] band" or
  "violates band".
* `compare_literature.md` includes a row comparing top-cell `bf` distribution to Cuntz 2010.

## Cross-References

* Source suggestion: S-0097-01.
* Source paper: Cuntz et al. 2010 -- 10.1371/journal.pcbi.1002107.
* Related project answer: t0097
  `assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation`.
* Prior lineage: t0106, t0112, t0113, t0114, t0115.
