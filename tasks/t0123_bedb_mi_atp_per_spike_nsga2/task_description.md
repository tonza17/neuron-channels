# NSGA-II Maximising Stimulus-Spike MI and Minimising ATP-per-Spike

## Source Suggestion

S-0097-05: "Bed B NSGA-II maximising MI and minimising ATP-per-spike (bits-per-ATP front)."

## Motivation

The t0097 multi-objective-optimisation catalogue (the
`objective-functions-for-single-neuron-multi-objective-optimisation` answer asset under
`tasks/t0097_multi_obj_optim/assets/answer/`) registered two information-and-energy objectives
derived from the canonical literature:

* `mutual_information_stimulus_spike_train` (Strong et al. 1998 direct method, Dhingra and Smith
  2004 RGC anchor): maximise the bias-corrected mutual information rate between stimulus identity
  and spike output.
* `metabolic_energy_atp_per_spike` (Sengupta et al. 2010 / Hallermann et al. 2012 / Attwell and
  Laughlin 2001): minimise the per-spike ATP cost computed as
  `(1/3) * sum_compartments int(I_Na^inward) dt / e`.

Niven et al. 2007 measured the empirical bits-per-ATP Pareto curve in four fly photoreceptor
species: information rates from **200 bits/s (D. melanogaster) to 1000 bits/s (S. carnaria)** scale
super-linearly with ATP cost, with a fixed cost of ~20% of maximum consumption. The Dhingra and
Smith 2004 brisk-transient guinea-pig RGC measurement is the only direct MI anchor in the corpus for
a retinal ganglion cell. The DSGC bits-per-ATP ratio is **unmeasured in the published literature**
-- this experiment generates a falsifiable prediction for it.

This is the explicit "MI vs ATP-per-spike" pair the catalogue ranked as one of the recommended
function-vs-cost combinations. Unlike t0122 (DSI vs cytoplasm volume), this experiment decouples
function (information) from selectivity (DSI), so the resulting Pareto front is **directly
comparable to Niven 2007's empirical curve** rather than to the project's own DSI mission. Tradeoff:
DSI is not optimised, so the Pareto front does not directly serve the project's first-question DSGC
selectivity mission -- ranked medium-priority for that reason.

## Gating Dependency

This task may start as soon as t0122 has completed and the t0120 geometry-audit verdict remains
"rendering-only / no re-runs needed" (already confirmed at t0122 launch). No new gating
prerequisites beyond the t0122 lineage.

## Hard Constraints (must be reproduced in plan and implementation)

These constraints are non-negotiable. The planning subagent must surface each one in `plan/plan.md`
`## Verification Criteria` with an explicit check, and the implementation subagent must reproduce
them in `code/constants.py`:

* **`_POOL_RESTART_EVERY = 10`** -- fresh random-init pool injection cadence. The project's standing
  10-gen rule, established by t0112 and carried through every subsequent NSGA-II task (t0113 / t0114
  / t0115 / t0122). NEVER use any other cadence.
* **`HV_PLATEAU_AUTO_STOP = False`** -- disabled per project policy (see memory:
  `feedback_disable_hv_plateau_autostop.md`). Rely on operator-stop + budget cap + gen ceiling.
* **`POP_SIZE = 96`**, **`N_EVAL_SEEDS = 3`** -- match the t0114/t0115/t0122 protocol exactly.
* **`N_GEN_MAX = 60`** -- gen ceiling per the auto-stop-disabled convention.
* **`N_DIRECTIONS = 4`** -- antipodal pairs at 0deg / 90deg / 180deg / 270deg. Reduced from the
  t0091-style 8-direction protocol to keep evaluation cost at 12 evals/cell (4 dirs * 3 noise
  seeds), within the $6 cap. See "MI Estimator Choice" below for the implications.
* **`COST_CAP_USD = 6.0`** -- matches t0122's reduced cap because the Vast.ai account balance is
  still $7 (verified before launch). Watchdog stops the run if exceeded. Previous lineage came in
  well under: t0113=$0.48, t0114=$1.13, t0115=$2.50, t0122 (similar 12-eval protocol expected) under
  $3. Expected actual: $3-5.

## MI Estimator Choice

The Strong et al. 1998 direct method requires many trials per stimulus to estimate within-stimulus
noise entropy. With only 3 trials per direction in the NSGA-II inner loop, the direct method's 1/T
extrapolation is too noisy to use as an optimiser objective. Use a **two-tier MI estimator**:

* **Inner-loop objective (per-cell, per-generation)**: spike-count MI between stimulus direction and
  total spike count in the 1400 ms trial window:

  ```
  I_count(D; N_spikes) ≈ I_plugin(D; N_bin) - bias_MM
  ```

  where `D` is the direction (4 equiprobable values), `N_bin` is the spike count bucketed into
  log-spaced bins, `I_plugin` is the plug-in MI estimator on the 4 x B contingency table built from
  the 12 (direction, noise-seed) trials, and `bias_MM` is the Miller-Madow correction
  `(R-1)(C-1)/(2N ln 2)` with `R=4`, `C=B`, `N=12`. Ceiling is `log2(4) = 2.0 bits`. Report
  `I_count` in bits per stimulus.

* **Post-hoc verification (top-N cells only)**: for the top-10 cells on the joint Pareto front,
  rerun the cell with 8 directions * 20 trials per direction = 160 trials and compute the
  Strong-Bialek direct-method MI rate with 1/T extrapolation per the t0097 recipe (resolution dt=5
  ms, word lengths T in {25, 50, 75, 100} ms). Report the direct-method MI in bits/s alongside the
  spike-count MI in bits/stimulus. The cross-validation answers the catalogue's open question "is
  the 4-direction count-MI a reliable surrogate for the Strong-Bialek rate".

The catalogue (t0097) explicitly flagged that "the project's 8-direction protocol may be too
information-poor (only 3 bits of stimulus uncertainty) to give the MI estimator meaningful dynamic
range". The 4-direction protocol has a 2-bit ceiling, which is acceptable as a *relative* selection
signal for NSGA-II but compresses the bits/s scale relative to Niven 2007's 200-1000 bits/s curve.
Report this caveat in `results_detailed.md` and use the post-hoc 8-direction direct-method MI as the
quantity compared to Niven 2007.

## ATP-per-Spike Recipe

Per the t0097 catalogue's `metabolic_energy_atp_per_spike` entry, derived from Sengupta et al. 2010:

```
N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int_{t_AP_start}^{t_AP_end} I_Na^inward(t) dt
```

Implementation requirements:

1. Record `seg.ina` per segment at simulation `dt` for **soma + AIS proximal + AIS distal + all
   dendritic segments**. Increases per-trial recording footprint vs t0122 by approximately 2x.
2. Run only `FULL` mode for ATP estimation (HH on, real spikes). EPSP/IPSP-passive modes produce no
   meaningful Na+ inward current and are skipped.
3. Detect AP windows from the somatic Vm threshold crossing at -20 mV with a 2 ms refractory after
   detection. AP window = +/-2 ms around peak.
4. Convert `seg.ina` (mA/cm^2) per segment to total current via per-segment surface area
   (`seg.area() * 1e-2` for cm^2), then integrate over the AP window in seconds.
5. Charge per AP per compartment: `Q^(c, AP) = int I_Na^inward dt * seg.area_cm2`. The "inward"
   restriction means `min(I_Na, 0)` integrated (Na+ current is negative inward in NEURON convention;
   take `-min(I_Na, 0)` magnitude).
6. ATP per AP per compartment: `N_ATP^(c, AP) = (Q^(c, AP) / e) / 3` with `e = 1.602e-19 C`.
7. Sum across compartments to get per-AP per-cell ATP cost.
8. Headline objective: total ATP across all trials / total spike count across all trials. Units: ATP
   molecules per spike.

The Sengupta et al. 2010 cross-cell-type calibration anchors are: ~25%-above-theoretical-minimum for
cortical pyramidal cells, ~100%-above-minimum for fast-spiking cerebellar Purkinje cells and
cortical interneurons. The Carter and Bean 2009 benchmark on cerebellar Purkinje cells (4 mM-mol ATP
per AP per cm of axon at the AIS) is the closest empirical anchor for a fast-spiking neuron.

A discrepancy > 30% vs Carter and Bean 2009 in the smoke-gate sanity check indicates a recipe error
(most commonly a surface-area conversion bug) and must be fixed before launching NSGA-II.

## Scope

One NSGA-II run, single GA seed, 2 objectives, on the 68-d Bed B + 14-d morphology substrate.

## Approach

1. **Copy the t0122 NSGA-II substrate** end-to-end: 68-d parameter vector (54-d electrophys + 14-d
   morphology), pop=96, N_EVAL_SEEDS=3, ratio DSI silence-guard tightened to >= 3 PD spikes,
   `_POOL_RESTART_EVERY=10`, HV-plateau auto-stop DISABLED, $6 hard cap.
2. **Replace direction set**: 4 antipodal directions (0deg / 90deg / 180deg / 270deg) instead of
   t0122's 2 antipodal (0deg / 180deg). Wall-clock per evaluation increases by ~2x; expected total
   cost still under $5.
3. **Replace both objectives**: drop DSI and cytoplasm volume; add MI (spike-count plug-in +
   Miller-Madow, max 2 bits) and ATP-per-spike (Sengupta recipe, ATP molecules per spike).
   Objectives become (maximise MI, minimise ATP-per-spike). DSI stays as a tracked diagnostic (cell
   may still be selective or not) but is not an optimiser objective.
4. **Add `seg.ina` recording** to `recorder.py` for soma + AIS + all dendrite segments. Smoke-gate
   verifies the recorded charge integrates to the Carter and Bean 2009 ~4 mM-mol ATP/AP/cm benchmark
   on the canonical Bed B cell within 30%.
5. **Two-tier MI estimator** as described in "MI Estimator Choice" above.
6. **GA seed**: draw via `secrets.randbelow(10000)` (avoid round-ish numbers per the t0113/t0115
   convention).
7. **Gen ceiling**: 60.
8. **Stop trigger**: operator stop when HV trajectory visibly plateaus OR $6 cost cap OR gen 60
   ceiling.
9. **Run on Vast.ai EPYC** (32-core or 64-core, whichever is cheapest at provisioning time);
   single-instance.
10. **Post-run analysis** (in this order):
    * Pareto front in (MI_count_bits, ATP_per_spike) space.
    * Per-cell DSI / PD-rate diagnostics (tracked, not optimised).
    * Top-10 Pareto-corner cells -> rerun with 8 directions * 20 trials per direction; compute
      Strong-Bialek direct-method MI in bits/s.
    * **Niven 2007 comparison chart**: scatter top-N cells in (ATP/spike, bits/s) space with the
      Niven 2007 fly photoreceptor curve overlaid (200-1000 bits/s, ~20% fixed cost). Report whether
      the DSGC front falls above, on, or below the fly curve.
    * Per-cell morphology gallery for top ranks (full dendrite trees per project default).
    * Carter and Bean 2009 ATP-per-AP benchmark check on the canonical cell and top-3 cells.
11. **Answer asset**: write one answer asset answering "Where does the DSGC bits-per-ATP front sit
    relative to Niven 2007's fly-photoreceptor curve, and does it match the Niven super-linear
    cost-vs-information scaling?"

## Expected Outputs

* `assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/` -- predictions asset per spec, with
  per-cell 68-d vector, per-direction firing, MI_count_bits, ATP_per_spike_molecules,
  ATP_per_AP_molecules, DSI (diagnostic), PD-rate (diagnostic).
* `assets/answer/dsgc-bits-per-atp-vs-niven-2007/` -- one answer asset on the Niven comparison.
* `results/data/pareto_front_seed*.json` -- Pareto front cells in (MI_count_bits, ATP_per_spike).
* `results/data/all_evaluations_seed*.json` -- every evaluation.
* `results/data/post_hoc_strong_bialek_mi_top10.json` -- 8-direction 20-trial direct-method MI in
  bits/s for the top-10 Pareto cells.
* `results/images/pareto_front_mi_vs_atp.png` -- Pareto front chart, MI on y, ATP/spike on x.
* `results/images/niven_2007_comparison.png` -- top-10 cells (ATP/spike, bits/s) overlaid on Niven
  2007's 4-species fly curve.
* `results/images/top50_morphologies_seed*.png` -- top-50 morphology grid (**full dendrite trees**
  per the project default, see memory `feedback_top50_morphologies_full_dendrites.md`).
* `results/images/carter_bean_atp_per_ap_check.png` -- distribution of ATP/AP across top-10 cells
  with the Carter and Bean 2009 ~4 mM-mol/cm benchmark overlaid.
* `results/results_summary.md`, `results/results_detailed.md`, `results/compare_literature.md`
  comparing to Niven 2007 / Strong 1998 / Dhingra and Smith 2004 / Sengupta 2010 / Carter and Bean
  2009\.

## Budget

* Cost cap: **$6** (matches t0122; Vast.ai balance is still $7 -- $1 buffer for teardown).
* Expected actual: **$3-5** based on prior lineage scaled by ~2x direction count (t0122 was
  approximately $3 for 2 directions; this is 4 directions, same gen ceiling).
* Post-hoc direct-method MI rerun on top-10 cells: 10 cells * 160 trials = 1600 sims, expected
  $0.20-0.50 additional. Folded into the $6 cap.
* If the run exceeds $6 watchdog trip, stop and write up partial results.

## Verification Criteria

* `_POOL_RESTART_EVERY == 10`, `HV_PLATEAU_AUTO_STOP == False`, `POP_SIZE == 96`,
  `N_EVAL_SEEDS == 3`, `N_DIRECTIONS == 4`, `N_GEN_MAX == 60`, `COST_CAP_USD == 6.0` asserted in
  `code/constants.py` at module import.
* Smoke-gate verifies the canonical Bed B cell's ATP/AP at the AIS matches Carter and Bean 2009 ~4
  mM-mol/cm benchmark within 30%; if not, the run is aborted and the recipe is debugged.
* `metrics.json` registers (a) the inner-loop spike-count MI `mi_count_bits`, (b) the headline
  `atp_per_spike_molecules`, (c) the post-hoc direct-method `mi_strong_bialek_bits_per_sec` for the
  top-10 cells, and (d) DSI and PD-rate as diagnostic variants.
* Predictions asset passes `verify_predictions_asset`.
* `compare_literature.md` includes a row comparing the DSGC bits-per-ATP front to Niven 2007's
  fly-photoreceptor curve (above / on / below).
* The answer asset states whether the DSGC bits-per-ATP front follows the Niven super-linear
  scaling, with explicit quantitative comparison and CI.

## Cross-References

* Source suggestion: S-0097-05.
* Source paper: Strong et al. 1998 -- 10.1103/PhysRevLett.80.197 (direct-method MI).
* Related papers from t0097's corpus: Niven et al. 2007 (bits-per-ATP curve), Dhingra and Smith 2004
  (RGC MI anchor), Sengupta et al. 2010 (ATP recipe), Carter and Bean 2009 (calibration benchmark),
  Attwell and Laughlin 2001 (energy budget), Remme et al. 2018 (function-vs-energy MOBO template).
* Related project answer: t0097
  `assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation`.
* Prior NSGA-II lineage: t0106 / t0112 / t0113 / t0114 / t0115 (substrate); t0122 (most-recent
  template; same constants, replaced objectives).
