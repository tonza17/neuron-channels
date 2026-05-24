# NSGA-II Maximising DSI and Minimising ATP-per-Spike

## Source Suggestion

S-0097-02: "Bed B NSGA-II maximising DSI and minimising ATP-per-spike."

## Motivation

The t0097 multi-objective optimisation catalogue
(`assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation`) ranked DSI vs
ATP-per-spike as the **highest-priority biologically-anchored function-vs-energy pair** for the
project. It directly serves the project's first-question DSGC selectivity mission while trading
function against a falsifiable metabolic cost objective:

* **Function objective**: direction selectivity index (DSI = (R_PD - R_ND) / (R_PD + R_ND)) -- the
  project's headline first-question metric.
* **Energy objective**: ATP molecules consumed per spike, derived from Sengupta et al. 2010's recipe
  `(1/3) * sum_compartments int(I_Na^inward) dt / e`. Anchored to the canonical Attwell-Laughlin
  2001 energy budget (~47% of cortical signalling ATP is per-spike Na+ pumping).
* **Empirical anchors**: Carter and Bean 2009 measured ~4 mM-mol ATP per AP per cm at the AIS of
  cerebellar Purkinje cells (the closest fast-spiking comparator). Sengupta et al. 2010's cross-
  cell-type calibration places cortical pyramidal cells at ~25%-above-theoretical-minimum Na/K
  overlap, while fast-spiking cells (Purkinje, cortical interneurons) sit at ~100%-above-minimum.
  Remme et al. 2018's MSO function-vs-energy MOBO (Pareto-coding -- ITD discrimination vs Na+ ATP)
  is the direct methodological template.

Recurring biological-plausibility concerns about pure-DSI-maximisation runs (the optimiser hits NMDA
/ Nav densities 85-122 sigma above Sivyer 2013 priors -- see t0080 / t0115 follow-ups) motivate
adding a hard biological cost objective. Unlike t0122 (DSI + cytoplasm volume), the cost here is a
**dynamic per-spike metabolic cost** rather than a geometric cost. The two costs are complementary:
t0122 tests Cajal / Cuntz wiring-cost predictions; t0124 tests Attwell-Laughlin / Carter-Bean
per-spike Na/K-overlap predictions on the same substrate.

The DSGC's DSI-vs-ATP-per-spike Pareto front is **unmeasured in the published literature** -- this
experiment generates a falsifiable prediction for it and locates the DSGC relative to the
Carter-Bean Purkinje benchmark and the Attwell-Laughlin signalling-budget anchor.

## Gating Dependency

This task may start immediately. The t0122 / t0123 lineage validated the substrate (68-d Bed B +
14-d morphology, $6 cap regime), and the t0120 geometry-audit verdict "rendering-only / no re-runs
needed" remains in force. t0123 supplies the seg.ina recording infrastructure and the Carter-Bean
smoke-gate -- both inherited verbatim. No new gating prerequisites.

## Scope

One NSGA-II run, single GA seed, 2 objectives, on the 68-d Bed B + 14-d morphology substrate
validated by the t0106-t0115 lineage and exercised by t0122 / t0123.

## Hard Constraints (must be reproduced in plan and implementation)

These constraints are non-negotiable. The planning subagent must surface each one in `plan/plan.md`
`## Verification Criteria` with an explicit check, and the implementation subagent must reproduce
them in `code/constants.py`:

* **`_POOL_RESTART_EVERY = 10`** -- fresh random-init pool injection cadence. The project's standing
  10-gen rule (established by t0112, carried through every subsequent NSGA-II task t0113 / t0114 /
  t0115 / t0122 / t0123). NEVER use any other cadence.
* **`HV_PLATEAU_AUTO_STOP = False`** -- disabled per project policy (see memory:
  `feedback_disable_hv_plateau_autostop.md`). Rely on operator-stop + budget cap + gen ceiling.
* **`POP_SIZE = 96`**, **`N_EVAL_SEEDS = 3`** -- match the t0114 / t0115 / t0122 / t0123 protocol
  exactly.
* **`N_GEN_MAX = 60`** -- gen ceiling per the auto-stop-disabled convention.
* **`N_DIRECTIONS = 2`** -- antipodal pair at 0deg (PD) / 180deg (ND), t0122-style. DSI only needs
  one antipodal pair; ATP-per-spike is direction-independent (per-spike normalisation). Reducing
  from t0123's 4 directions halves per-evaluation cost while losing nothing for the DSI + ATP
  objective pair. The MI count-entropy ceiling that motivated t0123's 4-direction protocol does not
  apply here -- MI is only tracked as a diagnostic.
* **`COST_CAP_USD = 6.0`** -- matches t0122 / t0123. Vast.ai account balance to be re-verified
  immediately before launch; if balance < $7, reduce cap to balance - $1 (teardown buffer). Watchdog
  stops the run if exceeded. Expected actual: $1-3 based on t0122 lineage at 2-direction protocol.

## DSI Recipe (silence-guarded ratio)

Per the t0122 convention, DSI is the **silence-guarded direction selectivity ratio**:

```text
R_PD = mean spike count over N_EVAL_SEEDS trials at 0deg
R_ND = mean spike count over N_EVAL_SEEDS trials at 180deg
DSI = (R_PD - R_ND) / (R_PD + R_ND)        if R_PD >= 3 spikes
DSI = -1.0                                  if R_PD < 3 spikes (silence guard)
```

* The silence guard is non-negotiable: cells with R_PD < 3 PD spikes are assigned DSI = -1 so the
  NSGA-II non-dominated sort rejects them. This prevents the optimiser from gaming the ratio with
  near-zero spike counts (e.g., 0/0 -> NaN, or 1/0 -> DSI = 1 with one chance spike).
* PD is fixed at 0deg and ND at 180deg per the t0024 / Bed B convention. No PD-rotation search.
* Headline DSI variant: `best_legit` (top DSI among cells passing the silence guard).
* Tracked DSI variants in `metrics.json`: `best_legit`, `overall_max`, `dsi_eq_one_count`.

## ATP-per-Spike Recipe (Sengupta 2010, inherited from t0123)

Per the t0097 catalogue's `metabolic_energy_atp_per_spike` entry, derived from Sengupta et al. 2010
and implemented by t0123:

```text
N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int_{t_AP_start}^{t_AP_end} I_Na^inward(t) dt
```

Implementation requirements (mirror t0123 exactly):

1. Record `seg.ina` per segment at simulation `dt` for **soma + AIS proximal + AIS distal + all
   dendritic segments**. Re-use t0123's recorder.py extension.
2. Run only `FULL` mode for ATP estimation (HH on, real spikes). EPSP / IPSP passive modes produce
   no meaningful Na+ inward current and are skipped.
3. Detect AP windows from the somatic Vm threshold crossing at -20 mV with a 2 ms refractory after
   detection. AP window = +/-2 ms around peak.
4. Convert `seg.ina` (mA/cm^2) per segment to total current via per-segment surface area
   (`seg.area() * 1e-2` for cm^2), then integrate over the AP window in seconds.
5. Charge per AP per compartment: `Q^(c, AP) = int I_Na^inward dt * seg.area_cm2`. The "inward"
   restriction means `min(I_Na, 0)` integrated (Na+ current is negative inward in NEURON convention;
   take `-min(I_Na, 0)` magnitude).
6. ATP per AP per compartment: `N_ATP^(c, AP) = (Q^(c, AP) / e) / 3` with `e = 1.602e-19 C`.
7. Sum across compartments to get per-AP per-cell ATP cost.
8. Headline objective: total ATP across all FULL-mode trials / total spike count across all
   FULL-mode trials. Units: ATP molecules per spike. **Lower is better.**
9. If total spike count == 0, set `atp_per_spike = +inf` (sentinel) so the cell is dominated. This
   sentinel must be reconciled with the DSI silence guard -- a cell with R_PD < 3 PD spikes will
   already have DSI = -1, so the ATP sentinel is only triggered for pathologically silent cells that
   somehow passed earlier filters.

### Smoke-gate (inherited from t0123, must re-run after any seg.ina recorder change)

* Before launching NSGA-II, run the ATP recipe on the canonical Bed B cell and verify that the
  per-AP ATP cost at the AIS proximal + AIS distal compartments matches the Carter and Bean 2009 ~4
  mM-mol/cm benchmark **within 30%**.
* If the smoke-gate fails, the run is aborted and the recipe is debugged (most common cause: a
  surface-area unit-conversion bug; second most common: missing compartments in the seg.ina record
  list).
* Follow up on S-0123-04 ("Verify Carter-Bean 2009 ATP/AP/cm benchmark and replace plan-quoted
  2.41e21 ATP/cm typo") in this task's smoke-gate: re-derive the Carter-Bean benchmark from first
  principles and document the canonical value in `plan/plan.md`.

## Approach

1. **Copy the t0123 NSGA-II substrate** end-to-end: 68-d parameter vector (54-d electrophys + 14-d
   morphology), pop=96, N_EVAL_SEEDS=3, DSI silence-guard >= 3 PD spikes, `_POOL_RESTART_EVERY=10`,
   HV-plateau auto-stop DISABLED, $6 hard cap, seg.ina recording infrastructure.
2. **Replace direction set**: 2 antipodal directions (0deg / 180deg) instead of t0123's 4 (0deg /
   90deg / 180deg / 270deg). Per-evaluation wall-clock drops by ~2x; expected total cost $1-3.
3. **Replace both objectives**: drop MI and t0122's cytoplasm volume; **maximise DSI** (silence-
   guarded ratio, t0122 convention) and **minimise ATP-per-spike** (Sengupta recipe, ATP molecules
   per spike).
4. **Re-use t0123's seg.ina recording** in `recorder.py` for soma + AIS proximal + AIS distal + all
   dendrite segments. No new recorder code -- only verify the recorder loads correctly on the
   2-direction protocol via the smoke-gate.
5. **Carter-Bean smoke-gate**: verify the canonical Bed B cell's ATP/AP at the AIS within 30% of ~4
   mM-mol/cm. Resolve S-0123-04 by documenting the canonical value with first-principles derivation.
6. **GA seed**: draw via `secrets.randbelow(10000)` (avoid round-ish numbers; t0113 / t0115
   convention).
7. **Gen ceiling**: 60.
8. **Stop trigger**: operator stop when HV trajectory visibly plateaus OR $6 cost cap OR gen 60
   ceiling.
9. **Run on Vast.ai EPYC** (32-core or 64-core, whichever is cheapest at provisioning time);
   single-instance.
10. **Post-run analysis** (in this order):
    * Pareto front in (DSI_best_legit, ATP_per_spike_molecules) space.
    * Per-cell diagnostics tracked but NOT optimised: PD-rate (Hz), ND-rate (Hz), cytoplasm volume
      (um^3, free since t0122 added the helper), MI_count_bits (free since t0123 added the estimator
      -- record but do not optimise).
    * **Carter-Bean 2009 ATP-per-AP benchmark check** on the canonical cell and the top-3 Pareto
      cells.
    * **Attwell-Laughlin 2001 signalling-budget anchor**: compute the implied per-cell signalling
      ATP rate (ATP/spike * PD-rate) for top-N cells and report where they sit relative to the
      47%-of-cortical-budget canonical figure.
    * **Top-50 morphology grid**: full dendrite trees per the project default (see memory
      `feedback_top50_morphologies_full_dendrites.md`).
    * **Joint-pass cells**: DSI >= 0.5 AND PD-rate >= 30 Hz AND ATP_per_spike <= TBD (median of the
      front used as the threshold for downstream selection).
11. **Answer asset**: write one answer asset answering "Does the DSGC DSI-vs-ATP-per-spike Pareto
    front show a Carter-Bean-style Na/K-overlap penalty, and where does it sit relative to
    Attwell-Laughlin's 47% signalling ATP budget?"

## Expected Outputs

* `assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph/` -- predictions asset per spec, with
  per-cell 68-d vector, per-direction firing (PD / ND), DSI_best_legit, ATP_per_spike_molecules,
  ATP_per_AP_molecules per compartment group, PD-rate, ND-rate, cytoplasm_volume_um3 (diagnostic),
  MI_count_bits (diagnostic).
* `assets/answer/dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin/` -- one answer asset on
  the Carter-Bean + Attwell-Laughlin comparison.
* `results/data/pareto_front_seed*.json` -- Pareto front cells in (DSI, ATP_per_spike).
* `results/data/all_evaluations_seed*.json` -- every evaluation.
* `results/images/pareto_front_dsi_vs_atp.png` -- Pareto front chart, DSI on y, ATP/spike on x.
* `results/images/carter_bean_atp_per_ap_check.png` -- distribution of ATP/AP across top-10 cells
  with the Carter and Bean 2009 ~4 mM-mol/cm benchmark overlaid.
* `results/images/attwell_laughlin_signalling_budget.png` -- top-N cells' implied signalling ATP
  rate (ATP/spike * PD-rate) overlaid on Attwell-Laughlin 2001's 47%-budget anchor.
* `results/images/top50_morphologies_seed*.png` -- top-50 morphology grid (**full dendrite trees**
  per the project default).
* `results/images/hv_trajectory_seed*.png` -- hypervolume vs generation.
* `results/results_summary.md`, `results/results_detailed.md`, `results/compare_literature.md`
  comparing to Attwell-Laughlin 2001 / Sengupta 2010 / Carter-Bean 2009 / Niven 2007 / Cuntz 2010
  (cross-reference to t0122 cytoplasm-volume front) / Remme 2018 (MSO MOBO methodology template).

## Budget

* Cost cap: **$6** (matches t0122 / t0123; Vast.ai balance to be re-verified at launch).
* Expected actual: **$1-3** based on t0122 (DSI + 2-direction protocol, came in well under $3).
  t0123's $3-5 estimate scaled by 0.5x (halved direction count) gives ~$1.5-2.5.
* If the run exceeds $6 watchdog trip, stop and write up partial results.

## Verification Criteria

* `_POOL_RESTART_EVERY == 10`, `HV_PLATEAU_AUTO_STOP == False`, `POP_SIZE == 96`,
  `N_EVAL_SEEDS == 3`, `N_DIRECTIONS == 2`, `N_GEN_MAX == 60`, `COST_CAP_USD == 6.0` asserted in
  `code/constants.py` at module import.
* Smoke-gate verifies the canonical Bed B cell's ATP/AP at the AIS matches Carter and Bean 2009 ~4
  mM-mol/cm benchmark within 30%; if not, the run is aborted and the recipe is debugged.
* DSI silence-guard threshold == 3 PD spikes; cells below the guard receive DSI = -1.
* `metrics.json` registers (a) `direction_selectivity_index` with variants `best_legit`,
  `overall_max`, `dsi_eq_one_count`; (b) headline `atp_per_spike_molecules`; (c) diagnostic variants
  `pd_firing_rate_hz`, `nd_firing_rate_hz`, `cytoplasm_volume_um3`, `mi_count_bits`.
* Predictions asset passes `verify_predictions_asset`.
* `compare_literature.md` includes rows comparing the DSGC DSI-vs-ATP front to:
  * Carter-Bean 2009 ATP/AP/cm benchmark (within 30% / over by Xx / under by Xx).
  * Attwell-Laughlin 2001 47% signalling-budget anchor (top-N cells fall above / on / below).
  * Cuntz 2010 balancing-factor band [0.2, 0.7] (cross-reference to t0122 front).
* The answer asset states whether the DSGC DSI-vs-ATP-per-spike front shows a Carter-Bean Na/K-
  overlap penalty (high-DSI corner more energy-expensive than expected, or comparable to / cheaper
  than the AIS benchmark), with explicit quantitative comparison and bootstrap CI.

## Cross-References

* Source suggestion: S-0097-02.
* Source paper: Sengupta et al. 2010 -- 10.1371/journal.pcbi.1000840 (the S-0097-02 anchor paper).
* Related papers from t0097's corpus: Attwell and Laughlin 2001 (energy budget), Carter and Bean
  2009 (calibration benchmark), Niven et al. 2007 (bits-per-ATP curve, indirect comparator from
  t0123), Cuntz et al. 2010 (cytoplasm cross-reference to t0122 front), Remme et al. 2018
  (function-vs-energy MOBO methodology template).
* Related project answer: t0097
  `assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation`.
* Prior NSGA-II lineage: t0106 / t0112 / t0113 / t0114 / t0115 (substrate); t0122 (DSI + cytoplasm
  volume, immediate sibling on the function objective); t0123 (MI + ATP-per-spike, immediate sibling
  on the cost objective -- supplies the seg.ina recorder, Carter-Bean smoke-gate, and ATP recipe
  verbatim).
* Follow-up scope from t0123: this task partially addresses S-0123-04 by re-deriving the Carter-Bean
  canonical value in the smoke-gate. S-0123-01 / S-0123-02 / S-0123-03 / S-0123-05 remain as
  separate follow-ups.
