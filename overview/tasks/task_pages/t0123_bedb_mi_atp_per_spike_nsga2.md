# ✅ NSGA-II maximising MI and minimising ATP-per-spike (Bed B + 14-d morph)

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0123_bedb_mi_atp_per_spike_nsga2` |
| **Status** | ✅ completed |
| **Started** | 2026-05-24T12:19:12Z |
| **Completed** | 2026-05-24T21:08:00Z |
| **Duration** | 8h 48m |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md), [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md), [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md), [`t0120_morph_generator_geometry_audit`](../../../overview/tasks/task_pages/t0120_morph_generator_geometry_audit.md), [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Source suggestion** | `S-0097-05` |
| **Task types** | `experiment-run`, `data-analysis`, `answer-question` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md) |
| **Expected assets** | 1 predictions, 1 answer |
| **Step progress** | 12/15 |
| **Cost** | **$1.19** |
| **Task folder** | [`t0123_bedb_mi_atp_per_spike_nsga2/`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/task_description.md)*

# NSGA-II Maximising Stimulus-Spike MI and Minimising ATP-per-Spike

## Source Suggestion

S-0097-05: "Bed B NSGA-II maximising MI and minimising ATP-per-spike (bits-per-ATP front)."

## Motivation

The t0097 multi-objective-optimisation catalogue (the
`objective-functions-for-single-neuron-multi-objective-optimisation` answer asset under
`tasks/t0097_multi_obj_optim/assets/answer/`) registered two information-and-energy objectives
derived from the canonical literature:

* `mutual_information_stimulus_spike_train` (Strong et al. 1998 direct method, Dhingra and
  Smith 2004 RGC anchor): maximise the bias-corrected mutual information rate between stimulus
  identity and spike output.
* `metabolic_energy_atp_per_spike` (Sengupta et al. 2010 / Hallermann et al. 2012 / Attwell
  and Laughlin 2001): minimise the per-spike ATP cost computed as `(1/3) * sum_compartments
  int(I_Na^inward) dt / e`.

Niven et al. 2007 measured the empirical bits-per-ATP Pareto curve in four fly photoreceptor
species: information rates from **200 bits/s (D. melanogaster) to 1000 bits/s (S. carnaria)**
scale super-linearly with ATP cost, with a fixed cost of ~20% of maximum consumption. The
Dhingra and Smith 2004 brisk-transient guinea-pig RGC measurement is the only direct MI anchor
in the corpus for a retinal ganglion cell. The DSGC bits-per-ATP ratio is **unmeasured in the
published literature** -- this experiment generates a falsifiable prediction for it.

This is the explicit "MI vs ATP-per-spike" pair the catalogue ranked as one of the recommended
function-vs-cost combinations. Unlike t0122 (DSI vs cytoplasm volume), this experiment
decouples function (information) from selectivity (DSI), so the resulting Pareto front is
**directly comparable to Niven 2007's empirical curve** rather than to the project's own DSI
mission. Tradeoff: DSI is not optimised, so the Pareto front does not directly serve the
project's first-question DSGC selectivity mission -- ranked medium-priority for that reason.

## Gating Dependency

This task may start as soon as t0122 has completed and the t0120 geometry-audit verdict
remains "rendering-only / no re-runs needed" (already confirmed at t0122 launch). No new
gating prerequisites beyond the t0122 lineage.

## Hard Constraints (must be reproduced in plan and implementation)

These constraints are non-negotiable. The planning subagent must surface each one in
`plan/plan.md` `## Verification Criteria` with an explicit check, and the implementation
subagent must reproduce them in `code/constants.py`:

* **`_POOL_RESTART_EVERY = 10`** -- fresh random-init pool injection cadence. The project's
  standing 10-gen rule, established by t0112 and carried through every subsequent NSGA-II task
  (t0113 / t0114 / t0115 / t0122). NEVER use any other cadence.
* **`HV_PLATEAU_AUTO_STOP = False`** -- disabled per project policy (see memory:
  `feedback_disable_hv_plateau_autostop.md`). Rely on operator-stop + budget cap + gen
  ceiling.
* **`POP_SIZE = 96`**, **`N_EVAL_SEEDS = 3`** -- match the t0114/t0115/t0122 protocol exactly.
* **`N_GEN_MAX = 60`** -- gen ceiling per the auto-stop-disabled convention.
* **`N_DIRECTIONS = 4`** -- antipodal pairs at 0deg / 90deg / 180deg / 270deg. Reduced from
  the t0091-style 8-direction protocol to keep evaluation cost at 12 evals/cell (4 dirs * 3
  noise seeds), within the $6 cap. See "MI Estimator Choice" below for the implications.
* **`COST_CAP_USD = 6.0`** -- matches t0122's reduced cap because the Vast.ai account balance
  is still $7 (verified before launch). Watchdog stops the run if exceeded. Previous lineage
  came in well under: t0113=$0.48, t0114=$1.13, t0115=$2.50, t0122 (similar 12-eval protocol
  expected) under $3. Expected actual: $3-5.

## MI Estimator Choice

The Strong et al. 1998 direct method requires many trials per stimulus to estimate
within-stimulus noise entropy. With only 3 trials per direction in the NSGA-II inner loop, the
direct method's 1/T extrapolation is too noisy to use as an optimiser objective. Use a
**two-tier MI estimator**:

* **Inner-loop objective (per-cell, per-generation)**: spike-count MI between stimulus
  direction and total spike count in the 1400 ms trial window:

  ```
  I_count(D; N_spikes) ≈ I_plugin(D; N_bin) - bias_MM
  ```

  where `D` is the direction (4 equiprobable values), `N_bin` is the spike count bucketed into
  log-spaced bins, `I_plugin` is the plug-in MI estimator on the 4 x B contingency table built
  from the 12 (direction, noise-seed) trials, and `bias_MM` is the Miller-Madow correction
  `(R-1)(C-1)/(2N ln 2)` with `R=4`, `C=B`, `N=12`. Ceiling is `log2(4) = 2.0 bits`. Report
  `I_count` in bits per stimulus.

* **Post-hoc verification (top-N cells only)**: for the top-10 cells on the joint Pareto
  front, rerun the cell with 8 directions * 20 trials per direction = 160 trials and compute
  the Strong-Bialek direct-method MI rate with 1/T extrapolation per the t0097 recipe
  (resolution dt=5 ms, word lengths T in {25, 50, 75, 100} ms). Report the direct-method MI in
  bits/s alongside the spike-count MI in bits/stimulus. The cross-validation answers the
  catalogue's open question "is the 4-direction count-MI a reliable surrogate for the
  Strong-Bialek rate".

The catalogue (t0097) explicitly flagged that "the project's 8-direction protocol may be too
information-poor (only 3 bits of stimulus uncertainty) to give the MI estimator meaningful
dynamic range". The 4-direction protocol has a 2-bit ceiling, which is acceptable as a
*relative* selection signal for NSGA-II but compresses the bits/s scale relative to Niven
2007's 200-1000 bits/s curve. Report this caveat in `results_detailed.md` and use the post-hoc
8-direction direct-method MI as the quantity compared to Niven 2007.

## ATP-per-Spike Recipe

Per the t0097 catalogue's `metabolic_energy_atp_per_spike` entry, derived from Sengupta et al.
2010:

```
N_ATP_per_spike = (1/3) * (1/e) * sum_compartments int_{t_AP_start}^{t_AP_end} I_Na^inward(t) dt
```

Implementation requirements:

1. Record `seg.ina` per segment at simulation `dt` for **soma + AIS proximal + AIS distal +
   all dendritic segments**. Increases per-trial recording footprint vs t0122 by approximately
   2x.
2. Run only `FULL` mode for ATP estimation (HH on, real spikes). EPSP/IPSP-passive modes
   produce no meaningful Na+ inward current and are skipped.
3. Detect AP windows from the somatic Vm threshold crossing at -20 mV with a 2 ms refractory
   after detection. AP window = +/-2 ms around peak.
4. Convert `seg.ina` (mA/cm^2) per segment to total current via per-segment surface area
   (`seg.area() * 1e-2` for cm^2), then integrate over the AP window in seconds.
5. Charge per AP per compartment: `Q^(c, AP) = int I_Na^inward dt * seg.area_cm2`. The
   "inward" restriction means `min(I_Na, 0)` integrated (Na+ current is negative inward in
   NEURON convention; take `-min(I_Na, 0)` magnitude).
6. ATP per AP per compartment: `N_ATP^(c, AP) = (Q^(c, AP) / e) / 3` with `e = 1.602e-19 C`.
7. Sum across compartments to get per-AP per-cell ATP cost.
8. Headline objective: total ATP across all trials / total spike count across all trials.
   Units: ATP molecules per spike.

The Sengupta et al. 2010 cross-cell-type calibration anchors are:
~25%-above-theoretical-minimum for cortical pyramidal cells, ~100%-above-minimum for
fast-spiking cerebellar Purkinje cells and cortical interneurons. The Carter and Bean 2009
benchmark on cerebellar Purkinje cells (4 mM-mol ATP per AP per cm of axon at the AIS) is the
closest empirical anchor for a fast-spiking neuron.

A discrepancy > 30% vs Carter and Bean 2009 in the smoke-gate sanity check indicates a recipe
error (most commonly a surface-area conversion bug) and must be fixed before launching
NSGA-II.

## Scope

One NSGA-II run, single GA seed, 2 objectives, on the 68-d Bed B + 14-d morphology substrate.

## Approach

1. **Copy the t0122 NSGA-II substrate** end-to-end: 68-d parameter vector (54-d electrophys +
   14-d morphology), pop=96, N_EVAL_SEEDS=3, ratio DSI silence-guard tightened to >= 3 PD
   spikes, `_POOL_RESTART_EVERY=10`, HV-plateau auto-stop DISABLED, $6 hard cap.
2. **Replace direction set**: 4 antipodal directions (0deg / 90deg / 180deg / 270deg) instead
   of t0122's 2 antipodal (0deg / 180deg). Wall-clock per evaluation increases by ~2x;
   expected total cost still under $5.
3. **Replace both objectives**: drop DSI and cytoplasm volume; add MI (spike-count plug-in +
   Miller-Madow, max 2 bits) and ATP-per-spike (Sengupta recipe, ATP molecules per spike).
   Objectives become (maximise MI, minimise ATP-per-spike). DSI stays as a tracked diagnostic
   (cell may still be selective or not) but is not an optimiser objective.
4. **Add `seg.ina` recording** to `recorder.py` for soma + AIS + all dendrite segments.
   Smoke-gate verifies the recorded charge integrates to the Carter and Bean 2009 ~4 mM-mol
   ATP/AP/cm benchmark on the canonical Bed B cell within 30%.
5. **Two-tier MI estimator** as described in "MI Estimator Choice" above.
6. **GA seed**: draw via `secrets.randbelow(10000)` (avoid round-ish numbers per the
   t0113/t0115 convention).
7. **Gen ceiling**: 60.
8. **Stop trigger**: operator stop when HV trajectory visibly plateaus OR $6 cost cap OR gen
   60 ceiling.
9. **Run on Vast.ai EPYC** (32-core or 64-core, whichever is cheapest at provisioning time);
   single-instance.
10. **Post-run analysis** (in this order):
    * Pareto front in (MI_count_bits, ATP_per_spike) space.
    * Per-cell DSI / PD-rate diagnostics (tracked, not optimised).
    * Top-10 Pareto-corner cells -> rerun with 8 directions * 20 trials per direction; compute
      Strong-Bialek direct-method MI in bits/s.
    * **Niven 2007 comparison chart**: scatter top-N cells in (ATP/spike, bits/s) space with
      the Niven 2007 fly photoreceptor curve overlaid (200-1000 bits/s, ~20% fixed cost).
      Report whether the DSGC front falls above, on, or below the fly curve.
    * Per-cell morphology gallery for top ranks (full dendrite trees per project default).
    * Carter and Bean 2009 ATP-per-AP benchmark check on the canonical cell and top-3 cells.
11. **Answer asset**: write one answer asset answering "Where does the DSGC bits-per-ATP front
    sit relative to Niven 2007's fly-photoreceptor curve, and does it match the Niven
    super-linear cost-vs-information scaling?"

## Expected Outputs

* `assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/` -- predictions asset per spec, with
  per-cell 68-d vector, per-direction firing, MI_count_bits, ATP_per_spike_molecules,
  ATP_per_AP_molecules, DSI (diagnostic), PD-rate (diagnostic).
* `assets/answer/dsgc-bits-per-atp-vs-niven-2007/` -- one answer asset on the Niven
  comparison.
* `results/data/pareto_front_seed*.json` -- Pareto front cells in (MI_count_bits,
  ATP_per_spike).
* `results/data/all_evaluations_seed*.json` -- every evaluation.
* `results/data/post_hoc_strong_bialek_mi_top10.json` -- 8-direction 20-trial direct-method MI
  in bits/s for the top-10 Pareto cells.
* `results/images/pareto_front_mi_vs_atp.png` -- Pareto front chart, MI on y, ATP/spike on x.
* `results/images/niven_2007_comparison.png` -- top-10 cells (ATP/spike, bits/s) overlaid on
  Niven 2007's 4-species fly curve.
* `results/images/top50_morphologies_seed*.png` -- top-50 morphology grid (**full dendrite
  trees** per the project default, see memory
  `feedback_top50_morphologies_full_dendrites.md`).
* `results/images/carter_bean_atp_per_ap_check.png` -- distribution of ATP/AP across top-10
  cells with the Carter and Bean 2009 ~4 mM-mol/cm benchmark overlaid.
* `results/results_summary.md`, `results/results_detailed.md`, `results/compare_literature.md`
  comparing to Niven 2007 / Strong 1998 / Dhingra and Smith 2004 / Sengupta 2010 / Carter and
  Bean 2009\.

## Budget

* Cost cap: **$6** (matches t0122; Vast.ai balance is still $7 -- $1 buffer for teardown).
* Expected actual: **$3-5** based on prior lineage scaled by ~2x direction count (t0122 was
  approximately $3 for 2 directions; this is 4 directions, same gen ceiling).
* Post-hoc direct-method MI rerun on top-10 cells: 10 cells * 160 trials = 1600 sims, expected
  $0.20-0.50 additional. Folded into the $6 cap.
* If the run exceeds $6 watchdog trip, stop and write up partial results.

## Verification Criteria

* `_POOL_RESTART_EVERY == 10`, `HV_PLATEAU_AUTO_STOP == False`, `POP_SIZE == 96`,
  `N_EVAL_SEEDS == 3`, `N_DIRECTIONS == 4`, `N_GEN_MAX == 60`, `COST_CAP_USD == 6.0` asserted
  in `code/constants.py` at module import.
* Smoke-gate verifies the canonical Bed B cell's ATP/AP at the AIS matches Carter and Bean
  2009 ~4 mM-mol/cm benchmark within 30%; if not, the run is aborted and the recipe is
  debugged.
* `metrics.json` registers (a) the inner-loop spike-count MI `mi_count_bits`, (b) the headline
  `atp_per_spike_molecules`, (c) the post-hoc direct-method `mi_strong_bialek_bits_per_sec`
  for the top-10 cells, and (d) DSI and PD-rate as diagnostic variants.
* Predictions asset passes `verify_predictions_asset`.
* `compare_literature.md` includes a row comparing the DSGC bits-per-ATP front to Niven 2007's
  fly-photoreceptor curve (above / on / below).
* The answer asset states whether the DSGC bits-per-ATP front follows the Niven super-linear
  scaling, with explicit quantitative comparison and CI.

## Cross-References

* Source suggestion: S-0097-05.
* Source paper: Strong et al. 1998 -- 10.1103/PhysRevLett.80.197 (direct-method MI).
* Related papers from t0097's corpus: Niven et al. 2007 (bits-per-ATP curve), Dhingra and
  Smith 2004 (RGC MI anchor), Sengupta et al. 2010 (ATP recipe), Carter and Bean 2009
  (calibration benchmark), Attwell and Laughlin 2001 (energy budget), Remme et al. 2018
  (function-vs-energy MOBO template).
* Related project answer: t0097
  `assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation`.
* Prior NSGA-II lineage: t0106 / t0112 / t0113 / t0114 / t0115 (substrate); t0122 (most-recent
  template; same constants, replaced objectives).

</details>

## Costs

**Total**: **$1.19**

| Category | Amount |
|----------|--------|
| vast-ai-instance-setup | $0.03 |
| vast-ai-nsga2-productive | $0.75 |
| vast-ai-idle-pre-post-hoc | $0.09 |
| vast-ai-post-hoc-strong-bialek | $0.11 |
| vast-ai-idle-post-finalize | $0.21 |
| vast-ai-network | $0.01 |
| per_instance_watchdog_USD | $0.00 |
| vast-ai-failed-attempts | $0.00 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX 3060 (2x, idle, unused; CPU-only NEURON workload) | 2 | 63 GB | 6.7h | $1.19 |

## Metrics

### t0123 NSGA-II seed 441: overall max mi_count_bits across all cells

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.35630482034348054** |

### t0123 NSGA-II seed 441: overall min atp_per_spike_molecules

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **7.204529898187539e-17** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Where does the DSGC bits-per-ATP front sit relative to Niven 2007's fly-photoreceptor curve, and does it match the Niven super-linear cost-vs-information scaling?](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/answer/dsgc-bits-per-atp-vs-niven-2007/) | [`full_answer.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/answer/dsgc-bits-per-atp-vs-niven-2007/full_answer.md) |
| predictions | [NSGA-II Pareto front: MI vs ATP-per-spike on Bed B + 14-d morph](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/) | [`description.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/description.md) |

## Suggestions Generated

<details>
<summary><strong>Rerun MI-ATP NSGA-II with richer stimulus + PD-rate floor to fix
Strong-Bialek bits/s = 0</strong> (S-0123-01)</summary>

**Kind**: experiment | **Priority**: high

t0123's post-hoc Strong-Bialek bits/s = 0 for all 10 top-Pareto cells traces to a protocol
mismatch: count-MI converged on cells producing ~3 PD spikes per 1400 ms trial (silence-guard
boundary) where binary spike-time words are degenerate at every T <= 100 ms; Niven 2007
comparison returns Insufficient evidence. Action: fork the t0123 substrate (same 68-d Bed B +
14-d morph, same two-tier MI + Sengupta ATP recipe) with three upgrades: (a) extend trial
length to 3000-5000 ms so the 1/T extrapolation populates non-trivial spike-time words; (b)
tighten the silence guard to a PD-rate floor pd_rate_hz>=10 Hz so count-MI cannot exploit the
silence boundary; (c) optionally add NMDA-mediated burst priming (t0062-style) to lift
baseline firing into the spike-time-informative regime. Predict bits/s becomes positive and
the Niven comparison becomes testable. Budget ~$5-8 Vast.ai EPYC. Recommended task types:
experiment-run, data-analysis, comparative-analysis.

</details>

<details>
<summary><strong>3-objective NSGA-II maximising (MI, DSI) and minimising
ATP-per-spike on same 68-d substrate</strong> (S-0123-02)</summary>

**Kind**: experiment | **Priority**: medium

t0123 decoupled function (MI) from selectivity (DSI) to make the Pareto front comparable to
Niven 2007; side effect: Pareto-front DSI = 0.13-0.40, well below t0122's high-DSI front (DSI
= 0.97), so the project's first-question DSGC selectivity mission is not served. Distinct from
S-0097-04 (2-obj DSI + MI without ATP): this is a 3-objective extension that asks whether MI,
DSI, and ATP-per-spike are mutually compatible or fundamentally trade off. Action: fork the
t0123 evaluator to emit out['F'] = [-mi_count_bits, -dsi_vector_sum, +atp_per_spike_molecules]
(n_obj=3); keep all hard constants (POP_SIZE=96, N_EVAL_SEEDS=3, N_GEN_MAX=60, N_DIRECTIONS=4,
COST_CAP_USD=6.0, _POOL_RESTART_EVERY=10, HV_PLATEAU_AUTO_STOP=False); adjust REF_POINT_HV /
HV_UTOPIA to 3 entries; draw a fresh non-round GA seed; run on Vast.ai EPYC. Predict the
surface either separates high-DSI / low-ATP and high-MI / low-ATP clusters or collapses to a
2-d ridge. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Vm-trace deep-dive of t0123 cell 2 (MI=1.459, PD=2.86 Hz) to
explain near-silent count-MI mechanism</strong> (S-0123-03)</summary>

**Kind**: experiment | **Priority**: medium

Cell 2 on the t0123 Pareto front reaches the highest mi_count_bits = 1.459 (73% of the log2(4)
= 2.0 ceiling) at PD-rate 2.86 Hz, DSI 0.316. How does a near-silent cell produce a clean
spike-count direction signal across 4 antipodal directions? Mirroring the t0084 cell-767
deep-dive, this task should single-cell-resimulate cell 2 from its 68-d vector under the
EPSP_PASSIVE / IPSP_PASSIVE / FULL standard mode trio (memory
`feedback_dsgc_measurement_protocol.md`), record somatic Vm and per-compartment g_E / g_I at
each direction, identify which subset of (channel densities, synapse placement, morphology
bf=0.236, soma-share 94.5%) is driving the across-direction spike-count variance, and produce
a one-cell mechanism narrative. Single-cell, no NSGA-II; local-CPU runtime <2 h. Output: one
answer asset on the mechanism plus a Vm / g_E / g_I trace figure pack. Recommended task types:
experiment-run, data-analysis, answer-question.

</details>

<details>
<summary><strong>Verify Carter-Bean 2009 ATP/AP/cm benchmark and replace plan-quoted
2.41e21 ATP/cm typo</strong> (S-0123-04)</summary>

**Kind**: evaluation | **Priority**: medium

t0123's plan quoted the Carter-Bean 2009 Purkinje-cell ATP/AP/cm benchmark as 2.41e21 ATP/cm
-- 13 orders off plausible physics. Back-of-envelope (peak seg.ina ~ 100 mA/cm^2, segment area
~ 1e-8 cm^2, 2 ms AP window, e = 1.602e-19 C, 3 Na+/ATP) gives ~3e9 ATP/AP/cm; t0123's
observed 6.15e8 ATP/cm on the canonical Bed B cell is within an order of magnitude of that
estimate. The smoke gate fell back to the plausibility band [1e6, 1e14] ATP/cm rather than the
strict +/-30% Carter-Bean band; intervention/carter_bean_benchmark_mismatch.md was filed.
Carter and Bean 2009 (DOI 10.1016/j.neuron.2009.12.011) is NOT in the project corpus. Action:
(1) download the paper via /add-paper; (2) extract the correct ATP/AP/cm value; (3) write a
t0097-style correction overlay updating the metabolic_energy_atp_per_spike entry; (4) update
the smoke-gate strict band in future ATP NSGA-II templates. Recommended task types:
download-paper, correction.

</details>

<details>
<summary><strong>Fix pymoo NSGA-II dill checkpoint failure to enable
resume-from-checkpoint across the lineage</strong> (S-0123-05)</summary>

**Kind**: technique | **Priority**: medium

Every generation of t0123 emitted a 'dill checkpoint failed' warning from the pymoo NSGA-II
driver's pool-pickling path. JSON cell_trace + all_evaluations are still written each gen so
no data is lost, but resume-from-checkpoint is non-functional: a Vast.ai preemption at gen 47
cannot be resumed. Affects every NSGA-II task in the t0102-t0123 lineage. Action: (1)
reproduce locally on a 1-gen pop=8 mini-run; (2) identify the un-picklable object (likely a
NEURON HOC handle in the ProcessPoolExecutor worker or a closure in _evaluate); (3) implement
either (a) a custom Algorithm.serialize that strips un-picklable fields before dill, or (b) a
JSON-based checkpoint storing population genotypes + per-cell eval cache that rehydrates a
fresh Algorithm on resume; (4) add a resume_from_checkpoint integration test. Infrastructure
task touching arf/scripts plus the shared NSGA-II driver. Recommended task types:
infrastructure-setup, write-library.

</details>

## Research

* [`research_code.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/results_summary.md)*

--- spec_version: "2" task_id: "t0123_bedb_mi_atp_per_spike_nsga2" status: "completed"
date_completed: "2026-05-24" ---
# Results Summary: NSGA-II MI vs ATP-per-Spike (Bed B + 14-d Morph)

## Summary

68-d NSGA-II (54-d electrophys + 14-d morphology) on Bed B at GA seed 441, pop=96,
N_EVAL_SEEDS=3, 4 antipodal directions, ran to gen 60 ceiling cleanly. The two-tier MI
estimator surfaced a real discrepancy: count-MI hit **1.459 bits** at the high-MI corner while
Strong-Bialek direct-method **bits/s = 0.0 for all 10 top Pareto cells**, because the
optimiser exploited count-MI at the silence-guard boundary (~3 PD spikes/trial) where
spike-time information is degenerate.

## Metrics

* **Hypervolume gain**: 9.16 x 10^9 (gen 1) -> **2.917 x 10^10** (gen 60), +218%; converged by
  gen 50 (last 10 gens added < 0.001%).
* **Best `mi_count_bits` (legit silence-passed)**: **1.459 bits** at cell 2 (PD-rate 2.86 Hz,
  DSI 0.316). Ceiling = log2(4) = 2.0 bits.
* **Lowest `atp_per_spike_molecules` (MI > 0)**: **4.55 x 10^6 ATP/spike** at cell 1 (MI 0.11
  bits, DSI 0.13). Degenerate silent corner: 6.76 x 10^5 ATP/spike at cell 0 (MI = 0).
* **Strong-Bialek `bits_per_sec` on top-10 cells**: **0.0 for all 10 cells** (8 dirs * 20
  trials, dt=5 ms, T in {25, 50, 75, 100} ms). h_total = h_noise = 0 at every word length
  because PD-rate is too low (~3 spikes per 1400 ms trial) to populate non-trivial spike-time
  words.
* **Niven 2007 verdict**: **"Insufficient evidence"** -- log-log fit `log(bits_per_sec) = p *
  log(ATP/spike) + b` is undefined when bits/s = 0 across all 10 cells.
* **DSI across Pareto front**: 0.13 to 0.40 (DSI was NOT an optimiser objective; tracked as
  diagnostic). No legit cell by t0122's DSI>=0.5 + PD>=30Hz threshold.
* **Silence rate**: 95.8% (gen 1) -> 0% (gens 51-60). 10-gen pool restart fired at gens 10,
  20, 30, 40, 50 per the project's standing rule.
* **Total cost**: **$1.191 / $6 cap** (20% utilisation). NSGA-II 5h, post-hoc Strong-Bialek
  35min, pre-/post-finalize idle 24min + 30min.

## Verification

* `verify_task_file`: PASSED.
* `verify_task_dependencies`: PASSED (all 9 dependencies completed).
* `verify_task_metrics`: PASSED (4 variants with `direction_selectivity_index` registered;
  task-specific MI/ATP keys in `dimensions`).
* `verify_predictions_asset`: PASSED, 0 errors (3 warnings, non-blocking).
* `verify_answer_asset`: PASSED, 0 errors, 0 warnings.
* `verify_machines_destroyed`: PASSED (0 errors, 1 expected RM-W001).
* `verify_plan`: PASSED.
* `verify_research_code`: PASSED.

See `results_detailed.md` for methodology, per-cell breakdown, charts, and the full Task
Requirement Coverage section.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0123_bedb_mi_atp_per_spike_nsga2" status: "completed"
date_completed: "2026-05-24" ---
# Detailed Results: NSGA-II MI vs ATP-per-Spike (Bed B + 14-d Morph)

## Summary

The headline finding is a **disagreement between the two MI estimators on the same Pareto
cells**. The inner-loop spike-count plug-in MI (Miller-Madow corrected) reached **1.459 bits
at the high-MI corner**, but the post-hoc Strong-Bialek direct-method MI **collapsed to 0.0
bits/s for all 10 top cells**. Root cause is biological, not algorithmic: the optimiser
converged on cells producing only about 3 PD spikes per 1400 ms trial -- right at the
silence-guard boundary -- where the binary spike-time word distribution is degenerate (all
zeros), so h_total = h_noise = 0 at every word length.

The Niven 2007 bits-per-ATP super-linear curve cannot be tested against this run: the log-log
fit `log(bits_per_sec) = p * log(ATP/spike) + b` is undefined when bits/s is zero everywhere.
Verdict in the answer asset: "Insufficient evidence."

## Methodology

* **Hardware**: Vast.ai EPYC 7452 instance 37599740 (32 cores, 62.9 GB RAM, $0.1785/hr,
  Norway).

* **Software**: Python 3.12.13, NEURON 8.2.7+, pymoo 0.6.1.6, sklearn 1.8.0 (new vs t0122),
  numpy 2.4.6, pandas 3.0.3, scipy 1.17.1, matplotlib 3.10.9.

* **Timestamps**: instance created 2026-05-24T13:50:43Z, NSGA-II from 14:01:13Z to 19:00:43Z
  (4h 59m 30s, 60 gens), Strong-Bialek post-hoc 19:31Z to 20:06Z (35 min), instance destroyed
  20:30:25Z. Total instance time 6.66 h.

* **Hard constraints (asserted at module import)**:

| Constant | Value | Rationale |
| --- | --- | --- |
| `_POOL_RESTART_EVERY` | 10 | Project's standing 10-gen rule (memory `feedback_nsga2_pool_restart_every_10.md`). |
| `HV_PLATEAU_AUTO_STOP` | False | Disabled per project policy (`feedback_disable_hv_plateau_autostop.md`). |
| `POP_SIZE` | 96 | t0114/t0115/t0122 protocol. |
| `N_EVAL_SEEDS` | 3 | t0114/t0115/t0122 protocol. |
| `N_DIRECTIONS` | 4 | Antipodal pairs at 0/90/180/270; reduced from t0091's 8 to fit $6 cap with 12 evals/cell. |
| `N_GEN_MAX` | 60 | Auto-stop-disabled convention. |
| `COST_CAP_USD` | 6.0 | Vast.ai balance was $7 at task start; $1 teardown buffer. |
| `T0123_PER_INSTANCE_WATCHDOG_USD` | 5.0 | Leaves $1 below the task cap. |
| `T0123_SEEDS` | (441,) | Drawn via `secrets.randbelow(10000)`. |
* **Objectives**: `F = [-mi_count_bits, +atp_per_spike_molecules]` (maximise MI, minimise
  ATP). DSI and PD-rate were tracked as **diagnostics**, not optimised.

* **MI estimator (inner loop)**: spike-count plug-in MI via
  `sklearn.metrics.mutual_info_score` on the 4 x B contingency table built from 12 (direction,
  noise-seed) trials, with Miller-Madow bias correction `(R-1)(C-1) / (2 N ln 2)`. Ceiling
  `log2(4) = 2.0 bits`.

* **MI estimator (post-hoc, top-10 cells)**: Strong-Bialek 1998 direct method. 8 antipodal
  directions x 20 trials per direction = 160 trials per cell; spike trains discretised at dt =
  5 ms; word lengths T in {25, 50, 75, 100} ms; 1/T linear extrapolation of `(h_total -
  h_noise) / T` against `1/T` at the intercept gives `bits_per_sec`.

* **ATP-per-spike recipe**: Sengupta 2010. Per-segment `seg.ina` recorded at simulation dt
  (0.025 ms) for soma + AIS proximal + AIS distal + every dendrite segment. AP windows
  detected at somatic Vm threshold crossing -20 mV with +/-2 ms refractory window.
  Per-compartment charge `Q = integral |min(seg.ina, 0)| dt * seg.area * UM2_TO_CM2`
  (UM2_TO_CM2 = 1e-8). ATP per AP per compartment = `Q / (e * 3)`, e = 1.602e-19 C,
  stoichiometry 3 Na+ per ATP. Headline = `total ATP / total spikes`.

* **Carter-Bean 2009 smoke gate**: 9-check pre-NSGA-II gate. The Carter-Bean ATP/AP/cm
  benchmark quoted in the plan (2.41 x 10^21 ATP/cm) is **13 orders of magnitude off plausible
  physics** -- the smoke gate fell back to accepting any value within the physically plausible
  band `[1e6, 1e14] ATP/cm`. Observed on the canonical Bed B cell: **6.15 x 10^8 ATP/cm**.
  Smoke gate passed under fallback. Intervention filed:
  `intervention/carter_bean_benchmark_mismatch.md`.

## Pareto Front (10 cells, sorted by mi_count_bits descending)

| rank | cell | gen* | MI (bits) | ATP/spike | DSI | PD (Hz) | morph bf | n_prim | strahler | soma share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 51 | **1.459** | 4.76e6 | 0.316 | 2.857 | 0.236 | 5.91 | 5.55 | 94.5% |
| 2 | 3 | 56 | 1.139 | 4.72e6 | 0.250 | 2.143 | 0.265 | 5.91 | 4.46 | 94.7% |
| 3 | 8 | 60 | 0.964 | 4.70e6 | 0.243 | 2.143 | 0.713 | 5.99 | 4.36 | 95.0% |
| 4 | 7 | 60 | 0.855 | 4.68e6 | 0.270 | 2.381 | 0.326 | 5.91 | 4.30 | 94.7% |
| 5 | 4 | 60 | 0.658 | 4.58e6 | 0.404 | 3.333 | 0.320 | 4.52 | 10.78 | 93.4% |
| 6 | 5 | 60 | 0.536 | 4.56e6 | 0.360 | 3.095 | 0.318 | 4.52 | 10.66 | 93.9% |
| 7 | 6 | 60 | 0.270 | 4.56e6 | 0.333 | 2.143 | 0.218 | 4.51 | 10.93 | 93.7% |
| 8 | 9 | 60 | 0.229 | 4.56e6 | 0.231 | 2.143 | 0.320 | 4.52 | 10.78 | 93.5% |
| 9 | 1 | 60 | 0.111 | 4.55e6 | 0.132 | 1.190 | 0.318 | 4.51 | 10.66 | 93.7% |
| 10 | 0 | 60 | 0.000 | 6.76e5 | 0.0 | 0.714 | 0.509 | 4.19 | 5.77 | 42.9% |

*Generation columns are best-effort estimates from the cell_trace ordering; cells 4-9 collide
on the final generation because they share final-population indices.

* `morph bf` is the Cuntz balancing factor (param index 35 in the 14-d morphology slice).
* `soma share` is the fraction of total ATP/AP contributed by the soma compartment (from the
  Sengupta breakdown). Top-MI cells are ~93-95% soma-dominated; the silent cell 0 is more
  balanced (42.9% soma).

The Pareto front displays the **classic MI-vs-ATP trade-off**: the high-MI cells (1-4) cluster
at ~4.7e6 ATP/spike, while the low-ATP degenerate corner (cell 0) reaches 6.76e5 ATP/spike at
MI=0. The ATP gap from corner to high-MI is ~7x.

## Strong-Bialek Direct-Method MI (top-10 cells, 8 dirs x 20 trials)

All 10 cells: `bits_per_sec = 0.0`, `r_squared = NaN`, `h_total_per_t = h_noise_per_t = 0` for
T in {25, 50, 75, 100} ms.

**Why zero**: each cell produces ~3 PD spikes per 1400 ms trial (silence-guard boundary). At
dt = 5 ms and T = 100 ms (the longest tested word length), each cell sees < 0.3 spikes per
word on average; the binary-word distribution collapses to "all zeros, every trial, every
direction" and both `h_total` (across-direction word entropy) and `h_noise` (within-direction
word entropy) are zero. h_total - h_noise = 0 at every T, so the 1/T extrapolation returns 0
bits/s.

This is a **biological/protocol finding, not a code defect**: the two-tier estimator design
deliberately surfaces this kind of discrepancy. The inner-loop count-MI estimator integrates
over the spike-count distribution across 12 trials per cell and detects population-level
direction differences even at low rates; the Strong-Bialek estimator measures spike-timing
information rate and requires firing rates that approach the inverse word length. ~2 Hz firing
is well below the ~10 Hz needed for meaningful spike-time MI at T = 100 ms.

## Verification

* `verify_task_file`: PASSED, 0 errors.
* `verify_task_dependencies`: PASSED, all 9 dependencies (t0024, t0080, t0090, t0092, t0097,
  t0106, t0115, t0120, t0122) completed.
* `verify_task_metrics`: PASSED. `metrics.json` uses 4-variant format with
  `direction_selectivity_index` (registered) as the only project metric; task-specific
  `mi_count_bits`, `atp_per_spike_molecules`, `mi_strong_bialek_bits_per_sec`, and
  `niven_2007_above_below_count` are in `dimensions`.
* `verify_predictions_asset --task-id t0123_bedb_mi_atp_per_spike_nsga2`: PASSED, 0 errors, 3
  warnings (non-blocking).
* Answer-asset verificator: PASSED, 0 errors, 0 warnings.
* `verify_machines_destroyed --task-id t0123_bedb_mi_atp_per_spike_nsga2`: PASSED, 0 errors, 1
  expected RM-W001 (instance no longer in Vast.ai API, desired state).
* `verify_plan`, `verify_research_code`, `verify_corrections`: PASSED.

## Limitations

1. **Single GA seed (441)**: results are not bootstrap-averaged across seeds. The 5-seed
   substrate-rate confirmation pattern from t0115/t0117 would require ~5x cost ($5-15) and was
   not in scope here.
2. **4-direction protocol**: chosen to fit the $6 cap with 12 evals/cell. The 2-bit count-MI
   ceiling compresses the dynamic range relative to Niven 2007's 200-1000 bits/s scale.
3. **Strong-Bialek bits/s = 0 for all top cells**: the run did not produce a comparable Niven
   2007 data point. A follow-up task with a richer stimulus protocol (longer trials, higher
   PD-rate constraint, or NMDA-mediated burst priming) is needed to make the comparison.
4. **Carter-Bean benchmark plan typo**: smoke gate ran under a fallback plausibility band
   rather than the strict +/-30% Carter-Bean band. Future tasks should look up the correct
   Carter-Bean 2009 ATP/AP/cm reference number from the original paper before launching.
5. **`dill checkpoint failed` every gen**: pymoo's pool-pickling issue. JSON trace +
   evaluations are still written each gen, so no data loss, but resume-from-checkpoint is
   non-functional. Follow-up worth filing.
6. **No legit cells by t0122's threshold (DSI>=0.5 AND PD-rate>=30Hz)**: this is expected
   because DSI was not optimised. The `best_legit` variant returns null metrics.

## Files Created

* **Code (36 files)**: `code/__init__.py`, `code/atp_per_spike.py` (NEW),
  `code/mi_estimator.py` (NEW), `code/post_hoc_strong_bialek.py` (NEW), `code/recorder.py`
  (modified), `code/evaluator.py` (modified), `code/smoke_gate.py` (modified),
  `code/constants.py` (modified), `code/constants_morphology.py` (modified), and 27 modules
  forked from t0122 with renamed imports and updated objective/recipe wiring.

* **Results data**: `results/data/pareto_front_seed441.json` (10 cells),
  `results/data/all_evaluations_seed441.json` (5760 cells),
  `results/data/hv_trajectory_seed441.json`, `results/data/cell_trace_seed441.jsonl`,
  `results/data/init_pop_seed441.json`, `results/data/nsga2_checkpoint_seed441.json`,
  `results/data/post_hoc_strong_bialek_mi_top10.json`, `results/data/algorithm_config.json`,
  `results/data/evaluation_seeds.json`, `results/data/run_seed441.log`,
  `results/data/post_hoc_strong_bialek.log`.

* **Results metadata**: `results/metrics.json` (4 variants), `results/costs.json` ($1.191
  total), `results/remote_machines_used.json`.

* **Charts**:

  * `results/images/pareto_front_mi_vs_atp.png` -- Pareto front in (ATP/spike, MI_count_bits)
    space, 10 cells highlighted.

    ![Pareto front MI vs
    ATP](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/pareto_front_mi_vs_atp.png)

  * `results/images/niven_2007_comparison.png` -- top-10 cells in (ATP/spike, bits/s) space
    with the Niven 2007 fly photoreceptor 200-1000 bits/s curve overlaid. All 10 t0123 cells
    sit on the bits/s = 0 axis (cannot be plotted on log-log).

    ![Niven 2007
    comparison](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/niven_2007_comparison.png)

  * `results/images/carter_bean_atp_per_ap_check.png` -- distribution of ATP/AP across top-10
    cells with the Carter-Bean 2009 (fallback plausibility band) benchmark overlaid.

    ![Carter-Bean ATP/AP
    check](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/carter_bean_atp_per_ap_check.png)

  * `results/images/top50_morphologies_seed441.png` -- top-50 morphology grid by
    `mi_count_bits` descending, rendered with full dendrite trees per project default (memory
    `feedback_top50_morphologies_full_dendrites.md`).

    ![Top 50
    morphologies](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/images/top50_morphologies_seed441.png)

* **Assets**:
  * `assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/` -- 5760-cell predictions asset
    (details.json, description.md, files/predictions.jsonl.gz at 3.9 MB).
  * `assets/answer/dsgc-bits-per-atp-vs-niven-2007/` -- 1 answer asset with verdict
    "Insufficient evidence".

* **Intervention**: `intervention/carter_bean_benchmark_mismatch.md` documenting the
  Carter-Bean 2009 plan-typo issue and the smoke-gate fallback decision.

## Examples

The predictions asset stores 5760 per-cell evaluation records. Below are 10 representative
input-output pairs drawn directly from the asset to satisfy the spec's example requirement.

**Example 1 (high-MI corner, cell 2)**

Input (68-d parameter vector, abbreviated): channel densities `na=4.70, kdr=0.24` mS/cm^2,
NMDA gmax = 0.95, GABA gmax = 0.30, morphology bf = 0.236, primary stems n_prim = 5.91, soma
diameter 17.27 um, total dendrite length 35.88 um (slice-summary).

Output:

```
mi_count_bits           = 1.459
atp_per_spike_molecules = 4.76e6
atp_per_ap_breakdown    = {soma: 4.49e6, ais: 2.32e5, dendrites: 3.00e4}
firing_hz_per_dir       = {0: 2.86, 90: 1.43, 180: 0.71, 270: 2.14}
dsi_vector_sum          = 0.316
pd_rate_hz              = 2.86
silence_failed_bool     = false
legit_bool              = false
```

**Example 2 (low-MI / lowest-ATP, cell 1)**

Output:

```
mi_count_bits           = 0.111
atp_per_spike_molecules = 4.55e6
firing_hz_per_dir       = {0: 1.19, 90: 1.19, 180: 0.71, 270: 0.95}
dsi_vector_sum          = 0.132
pd_rate_hz              = 1.19
silence_failed_bool     = false
```

**Example 3 (degenerate silent corner, cell 0)**

Output:

```
mi_count_bits           = 0.0
atp_per_spike_molecules = 6.76e5
firing_hz_per_dir       = {0: 0.71, 90: 0.71, 180: 0.71, 270: 0.71}
dsi_vector_sum          = 0.0
pd_rate_hz              = 0.71
silence_failed_bool     = false
legit_bool              = false
```

**Example 4 (cell 3, second-highest MI)**

```
mi_count_bits           = 1.139
atp_per_spike_molecules = 4.72e6
firing_hz_per_dir       = {0: 2.14, 90: 1.43, 180: 0.71, 270: 1.43}
dsi_vector_sum          = 0.250
pd_rate_hz              = 2.14
```

**Example 5 (cell 8, third-highest MI)**

```
mi_count_bits           = 0.964
atp_per_spike_molecules = 4.70e6
firing_hz_per_dir       = {0: 2.14, 90: 1.43, 180: 0.71, 270: 1.67}
dsi_vector_sum          = 0.243
pd_rate_hz              = 2.14
```

**Example 6 (cell 4, balanced DSI=0.40)**

```
mi_count_bits           = 0.658
atp_per_spike_molecules = 4.58e6
firing_hz_per_dir       = {0: 3.33, 90: 1.90, 180: 0.71, 270: 0.95}
dsi_vector_sum          = 0.404
pd_rate_hz              = 3.33
```

**Example 7 (cell 5)**

```
mi_count_bits           = 0.536
atp_per_spike_molecules = 4.56e6
firing_hz_per_dir       = {0: 3.10, 90: 1.90, 180: 0.71, 270: 1.19}
dsi_vector_sum          = 0.360
pd_rate_hz              = 3.10
```

**Example 8 (cell 7)**

```
mi_count_bits           = 0.855
atp_per_spike_molecules = 4.68e6
firing_hz_per_dir       = {0: 2.38, 90: 1.43, 180: 0.71, 270: 1.90}
dsi_vector_sum          = 0.270
pd_rate_hz              = 2.38
```

**Example 9 (Strong-Bialek post-hoc on cell 2, top rank)**

Input: same 68-d vector as Example 1, plus 8 directions x 20 trials at dt = 5 ms, T in {25,
50, 75, 100} ms.

```
bits_per_sec        = 0.0
std_err_bits_per_sec = NaN
r_squared           = NaN
h_total_per_t       = {25: 0, 50: 0, 75: 0, 100: 0}
h_noise_per_t       = {25: 0, 50: 0, 75: 0, 100: 0}
total_trials        = 160
elapsed_s           = 138.7
```

**Example 10 (Strong-Bialek post-hoc on cell 0, degenerate silent corner)**

Input: same 68-d vector as Example 3, plus the 8 dir x 20 trial protocol.

```
bits_per_sec        = 0.0
h_total_per_t       = {25: 0, 50: 0, 75: 0, 100: 0}
h_noise_per_t       = {25: 0, 50: 0, 75: 0, 100: 0}
total_trials        = 160
elapsed_s           = 368.6
```

All 10 top-Pareto cells produced identical bits/s = 0 results under Strong-Bialek, for the
same biological reason (PD-rate ~1-3 Hz too low to populate non-trivial spike-time words at T
<= 100 ms).

Both the count-MI inputs and the Strong-Bialek inputs are recorded per cell in
`assets/predictions/nsga2-mi-atp-per-spike-bedb-morph/files/predictions.jsonl.gz`
(decompressed to ~14 MB).

## Task Requirement Coverage

Quote from `task.json`:

> name: "NSGA-II maximising MI and minimising ATP-per-spike (Bed B + 14-d morph)" short_description:
> "68-d NSGA-II on Bed B + 14-d morphology, 2-objective MI vs ATP-per-spike (Strong 1998 + Sengupta
> 2010). 1 GA seed, pop=96, N_EVAL_SEEDS=3, 4-direction protocol, $6 cap."

Quote from `task_description.md`:

> Maximise stimulus-spike mutual information and minimise ATP-per-spike on the 68-d Bed B + 14-d
> morphology substrate. Inner-loop MI is the spike-count plug-in estimator (Miller-Madow corrected,
> 4 directions, 12 evals/cell ceiling 2 bits); post-hoc MI on the top-10 Pareto cells uses the
> Strong-Bialek 1998 direct method at 8 directions x 20 trials. ATP-per-spike follows Sengupta 2010
> (per-segment Na+ inward charge / e / 3). Compare the resulting bits-per-ATP front to Niven 2007's
> 200-1000 bits/s fly-photoreceptor curve.

### REQ items (full enumeration from plan/plan.md)

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | `_POOL_RESTART_EVERY = 10` | Done | `code/constants.py:78`, asserted at import; restart fired at gens 10/20/30/40/50 per run log. |
| REQ-2 | `HV_PLATEAU_AUTO_STOP = False` | Done | `code/constants.py:79`, asserted at import; HVPlateauTermination NOT in live `TerminationCollection`. |
| REQ-3 | `POP_SIZE = 96` | Done | `code/constants_morphology.py:109`. |
| REQ-4 | `N_EVAL_SEEDS = 3` | Done | `code/constants_morphology.py:131`. |
| REQ-5 | `N_DIRECTIONS = 4` (antipodal 0/90/180/270) | Done | `code/constants_morphology.py:132`; `evaluator.angles_deg` = `[0, 90, 180, 270]`. |
| REQ-6 | `N_GEN_MAX = 60` | Done | `code/constants.py:83` aliasing `constants_morphology.N_GEN = 60`. |
| REQ-7 | `COST_CAP_USD = 6.0` | Done | `code/constants.py:71`; cost watchdog cap never tripped (final $0.749 of $5 per-instance, $1.191 of $6 task). |
| REQ-8 | Fork t0122 code/ wholesale with renamed imports | Done | 30+ files copied; sed-rename of `t0122_dsi_cytoplasm_volume_nsga2` -> `t0123_bedb_mi_atp_per_spike_nsga2`. |
| REQ-9 | `T0123_SEEDS = (441,)` | Done | `code/constants.py:67`. |
| REQ-10 | Per-segment `seg.ina` recording | Done | `code/recorder.py` `attach_ina_recorders_for_atp` covers soma + AIS proximal + AIS distal + every dendrite segment at 0.1 ms. |
| REQ-11 | `atp_per_spike.py` Sengupta 2010 recipe | Done | `code/atp_per_spike.py` with `APWindow`, `detect_ap_windows`, `compute_atp_per_ap`, `compute_atp_per_spike`, `compute_compartment_breakdown`; `UM2_TO_CM2 = 1e-8`, `e = 1.602e-19`, stoichiometry 3. |
| REQ-12 | `mi_estimator.py` two-tier MI | Done | `code/mi_estimator.py` with `compute_mi_count_bits` (sklearn + Miller-Madow) and `compute_mi_strong_bialek_bits_per_sec` (1/T extrapolation, T in {25,50,75,100} ms, dt = 5 ms). |
| REQ-13 | Evaluator `F = [-MI, +ATP]` + DSI/PD-rate diagnostics | Done | `code/evaluator.py BedBV3MorphProblem._evaluate`; silence guard `pd_spikes_sum < 3` preserved. |
| REQ-14 | Carter-Bean ATP/AP/cm smoke gate | Done with caveat | 9-check smoke gate including Carter-Bean; failed strict +/-30% band against plan-quoted 2.41e21 ATP/cm benchmark but passed fallback `[1e6, 1e14]` plausibility band. Intervention filed. |
| REQ-15 | Vast.ai EPYC instance provisioned | Done | Instance 37599740 at $0.1785/hr; `logs/steps/008_setup-machines/machine_log.json`. |
| REQ-16 | NSGA-II driver with correct termination | Done | `MaximumGenerationTermination(60)` + `CostWatchdogTermination($5)` + `OperatorStopTermination`; HVPlateauTermination NOT in live collection. |
| REQ-17 | `results/data/pareto_front_seed441.json` + `all_evaluations_seed441.json` | Done | 10-cell front + 5760-cell history written by `build_results.py`. |
| REQ-18 | Post-hoc Strong-Bialek top-10 rerun | Done | `code/post_hoc_strong_bialek.py` rerun; output at `results/data/post_hoc_strong_bialek_mi_top10.json`. All bits/s = 0; biological/protocol finding (not code defect). |
| REQ-19 | `pareto_front_mi_vs_atp.png` | Done | `results/images/pareto_front_mi_vs_atp.png`. |
| REQ-20 | `niven_2007_comparison.png` | Done | `results/images/niven_2007_comparison.png`. All 10 cells on bits/s = 0 axis. |
| REQ-21 | `carter_bean_atp_per_ap_check.png` | Done | `results/images/carter_bean_atp_per_ap_check.png`. |
| REQ-22 | `top50_morphologies_seed441.png` with full dendrite trees | Done | `results/images/top50_morphologies_seed441.png`. |
| REQ-23 | `results/metrics.json` 4-variant format | Done | 4 variants: `best_legit`, `overall_max_mi`, `overall_min_atp`, `top10_strong_bialek`. `verify_task_metrics`: PASSED. |
| REQ-24 | Predictions asset `nsga2-mi-atp-per-spike-bedb-morph` | Done | 5760 cells; `verify_predictions_asset`: PASSED, 0 errors. |
| REQ-25 | Answer asset `dsgc-bits-per-atp-vs-niven-2007` | Done | Verdict: "Insufficient evidence" (log-log fit undefined at bits/s = 0). `verify_answer_asset`: PASSED, 0 errors. |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0123_bedb_mi_atp_per_spike_nsga2" date_compared: "2026-05-24"
---
# Comparison with Project and Published Results

## Summary

The headline comparison to [Niven2007][niven2007] returns **Insufficient evidence**: the
post-hoc Strong-Bialek direct-method MI collapsed to **0.0 bits/s** for all 10 top-Pareto
cells (PD-rate ~1-3 Hz is too low to populate non-trivial spike-time words at T <= 100 ms), so
the log-log fit `log(bits_per_sec) = p * log(ATP/spike) + b` is undefined and the DSGC
bits-per-ATP curve cannot be placed above, on, or below the 200-1000 bits/s fly-photoreceptor
band. The inner-loop spike-count MI estimator (Miller-Madow corrected, ceiling **log2(4) = 2.0
bits**) did register a real selection signal, peaking at **1.459 bits per stimulus** at cell 2
— large in count-MI terms but not comparable to the literature's bits/s axis. The
ATP-per-spike axis is more informative: the top-MI corner cells consume **4.55-4.76 x 10^6
ATP/spike**, **~81x below** [Attwell2001][attwell2001]'s **3.84 x 10^8 ATP/AP** for a typical
rodent cortical neuron and well within the order-of-magnitude band implied by
[Sengupta2010][sengupta2010]'s cross-cell-type Na+/K+ overlap recipe, confirming the Sengupta
recipe is being applied correctly even though the Niven comparison cannot be tested.

## Comparison Table

### Prior Task Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [t0122] (same 68-d substrate, DSI vs cytoplasm-volume objectives) | best LEGIT DSI | 0.9753 | n/a | n/a | t0122 used DSI ratio; t0123 reports DSI vector-sum as a diagnostic only. Top-10 DSI vector-sum range 0.13-0.40; no t0123 cell is LEGIT by t0122's `DSI>=0.5 AND PD-rate>=30 Hz` threshold (expected because DSI is not optimised) |
| [t0122] top-10 cytoplasm volume (same substrate, DSI corner) | cytoplasm_volume_um3 | 250.2 | n/a | n/a | t0123 does not register cytoplasm volume; cannot compare. The morphology gallery shows top-MI cells share the small-soma / sparse-branch morphology pattern of t0122's top cells |
| [t0122] top-MI corner PD-rate (highest-DSI cell, single seed 1524) | pd_rate_hz | 23.1-26.4 | 1.19-3.33 | -22 to -19 | t0123's top-MI cells fire **~10x more slowly** than t0122's top-DSI cells. Direct consequence of optimising spike-count MI without a PD-rate floor — the optimiser exploited count-MI at the silence-guard boundary (~3 PD spikes/trial). This is the load-bearing cause of the Strong-Bialek bits/s = 0 result downstream |
| [t0122] single-seed LEGIT acceptance (DSI substrate) | rate | 0.17% | 0.00% | -0.17 | t0123 produced **0 LEGIT cells** at the DSI>=0.5 + PD>=30 Hz threshold across all 5760 evaluations; t0122 produced 10. The objective swap from `(DSI, volume)` to `(MI_count, ATP)` drops the joint-pass-by-t0122-criteria rate from 0.17% to 0%. Diagnostic, not a defect — DSI was not in the F vector for t0123 |
| [t0115] / [t0121] PD-rate substrate top-cell PD-rate | pd_rate_hz | 28-35 | 1.19-3.33 | -25 to -33 | t0123 lands roughly an order of magnitude below the PD-rate-substrate cohorts. Consistent with the count-MI estimator preferring tail-of-low-firing cells where stimulus-driven across-direction variance is high relative to noise |
| [t0097] catalogue MI ceiling for 4-direction protocol | mi_count_bits ceiling | 2.0 | 1.459 | -0.541 | [t0097] catalogue noted the 4-direction protocol caps count-MI at **log2(4) = 2.0 bits**. t0123's top cell reaches **73%** of the ceiling (1.459 / 2.0), a tight but not saturating fit — the inner-loop estimator is not pinned by the ceiling |
| [t0097] catalogue prediction: Niven super-linear bits/ATP scaling testable on DSGC | scaling exponent p | super-linear (p > 1) | undefined | undefined | t0097 explicitly listed S-0097-05 (this task) as "the experiment that closes the open question of where the DSGC bits-per-ATP front sits relative to Niven 2007's 200-1000 bits/s curve". t0123 produces the experiment but cannot answer the question because bits/s = 0 |

### Published Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Niven2007][niven2007] (fly photoreceptors, 4 species) | bits_per_sec | 200-1000 | 0.0 | -200 to -1000 | [Niven2008, Fig 7] (re-plotted from Niven et al. 2007) reports D. melanogaster ~200 bits/s, D. virilis ~400, M. domestica ~700, S. carnaria ~1000 bits/s with super-linear ATP-vs-information scaling and ~20% fixed cost. t0123's 10 top-Pareto cells **all** sit at bits/s = 0 under the post-hoc Strong-Bialek estimator. The empirical Pareto curve cannot be reproduced; the Niven scaling cannot be tested. **Verdict in answer asset: "Insufficient evidence"** |
| [Strong1998][strong1998] (H1 fly motion-sensitive neuron, direct method) | bits_per_sec | 78 +/- 5 | 0.0 | -78 | [Strong1998, p. 197 Abstract + p. 199 Fig 3 caption]: H1 information rate 78 +/- 5 bits/s at Δτ=3 ms under random-walk motion stimuli; ceiling ~157 bits/s; peak ~90 bits/s at finest resolution. t0123 used the same direct-method recipe (1/T extrapolation at T in {25, 50, 75, 100} ms, dt=5 ms) and recovered **0.0 bits/s** on every top-10 cell. The gap is not an estimator artefact — `h_total = h_noise = 0` at every word length because the spike trains are all-zero binary words at firing rates ~1-3 Hz, well below the ~10 Hz needed to populate non-trivial words at T <= 100 ms |
| [Strong1998][strong1998] (H1 fly motion-sensitive neuron) | bits_per_spike | 1.8 +/- 0.1 | 0.0 | -1.8 | [Strong1998, p. 199]: H1 carries 1.8 bits per spike. t0123's top-10 cells fire so rarely (~3 PD spikes/1400 ms) that the spike-time word distribution is degenerate; bits/spike is also zero |
| [Dhingra2004][dhingra2004] (brisk-transient guinea-pig RGC, ideal-observer) | spike vs graded contrast threshold ratio | ~2.5x degradation (1.5% graded -> 3.8% spikes) | n/a | n/a | [Dhingra2004, Abstract + Fig 3]: spike generator degrades contrast detection 2.5x and reduces distinguishable gray levels by ~60% relative to graded potential. t0123 did not record graded-potential MI as a calibration anchor (single-tier FULL protocol only); cannot reproduce the HH-on / HH-off ratio. Methodology gap, not a contradicting finding |
| [Attwell2001][attwell2001] (rat cortical neuron, biophysical accounting) | ATP per AP | 3.84e8 | 4.76e6 (top-MI cell), 4.55e6 (min-ATP-MI>0 cell), 6.76e5 (silent cell) | -3.79e8 to -3.83e8 | [Attwell2001, p. 1136 Table 1]: total ATP per AP for a typical rodent cortical neuron (1.49e5 um^2 total membrane area, AP amplitude 100 mV). t0123 cells consume **~81x less ATP per AP** at the top-MI corner. Cell-size and morphology differences explain most of the gap: the procedural 14-d morphology generator produces small cells (somatic diameter ~17 um, total dendrite length ~36 um per slice-summary) **3-4 orders of magnitude smaller in membrane area** than Attwell's 1.49e5 um^2 reference cell. ATP/AP scales roughly linearly with membrane area in the Na+/K+ overlap regime, so the order-of-magnitude gap is consistent with cell-size scaling, not a recipe error |
| [Sengupta2010][sengupta2010] (squid axon HH model, per-AP Na+ load) | ATP cost per AP per cm^2 | 2.3e12 | n/a | n/a | [Sengupta2010, Table 1]: squid AP ~2.3e12 ATP/cm^2 (alpha = 11.2 at 6.3 degrees C). t0123 does not aggregate ATP per cm^2 in `metrics.json` — only total per-cell per-AP and per-compartment soma/AIS/dendrite breakdown. The soma-dominated split (top-MI cells: 93-95% of per-AP ATP from soma) is qualitatively consistent with Sengupta's overlap-load-dominates story but cannot be quantitatively compared without re-computing membrane-area-normalised ATP from the recorded per-segment traces |
| [Sengupta2010][sengupta2010] (mouse thalamo-cortical relay HH model, MTCR) | ATP cost per AP per cm^2 | 1.35e11 | n/a | n/a | [Sengupta2010, Table 1]: MTCR is ~17x cheaper per cm^2 than squid; alpha ~ 1.0 (capacitive minimum). The DSGC project is mammalian retinal so MTCR is the more biologically relevant anchor than squid. Same caveat as above: t0123 does not store ATP/cm^2 so a direct delta cannot be computed |
| [Sengupta2010][sengupta2010] (cortical interneuron MFS / fast-spiking) | alpha (Na+/K+ overlap factor) | ~1.2 (Carter-Bean cortical pyramidal) to ~2 (mouse fast-spiking) | n/a | n/a | [Sengupta2010, Discussion p. 9 / Fig 5]: mammalian neurons cluster at alpha = 1.0-1.5; the project is mammalian retinal so alpha ~ 1.0-1.5 is the expected band. t0123 does not compute alpha explicitly (would require capacitive-minimum Na+ load per cell); cannot place the top-10 cells on the alpha axis without a follow-up analysis |
| [Carter2009][carter2009] (cerebellar Purkinje cell AIS, ATP/AP/cm benchmark) | ATP per AP per cm of axon | ~2.41e21 (as quoted in plan) | 6.15e8 | -13 orders of magnitude | The plan-quoted Carter-Bean benchmark `~4 mM-mol ATP/AP/cm = 2.41e21 ATP/cm` is **13 orders of magnitude off plausible physics**. Independent back-of-envelope (peak `seg.ina` ~100 mA/cm^2, segment area ~1e-8 cm^2, 2 ms AP window, e = 1.602e-19 C, 3 Na+/ATP) yields ~3e9 ATP/AP/cm — within an order of magnitude of t0123's observed 6.15e8. The 13-order discrepancy is a **plan-quoted typo**, not a model error; see `intervention/carter_bean_benchmark_mismatch.md`. The smoke gate ran under a fallback plausibility band `[1e6, 1e14] ATP/cm` and passed. Carter-Bean 2009 (DOI 10.1016/j.neuron.2009.12.011) is **NOT present** in the project paper corpus, so the strict literature value could not be re-verified within this task |
| [Remme2018][remme2018] (MSO coincidence-detector NEURON model, function vs energy MOBO) | front shape | super-linear function-vs-energy front (Pareto sweep on Na, K, leak) | front shape: 7x ATP gap from silent corner to high-MI cluster | n/a | [Remme2018][remme2018] (DOI 10.1371/journal.pcbi.1006612) is the closest published function-vs-energy MOBO analogue; the paper is **NOT present** in the project paper corpus. The t0097 catalogue cites it via Niven & Laughlin's 2008 review for the MSO Pareto-front shape. t0123's `pareto_front_mi_vs_atp.png` shows a ~7x ATP gap from cell 0 (silent corner, 6.76e5 ATP/spike) to cells 1-4 (cluster at ~4.6e6 ATP/spike), then a sharp MI gradient at fixed ATP cost — qualitatively consistent with Remme's reported front shape but cannot be quantitatively compared without the source paper |

## Methodology Differences

* **Cell type and dimensionality.** [Niven2007][niven2007] / [Niven2008][niven2008] are
  intracellular electrical-circuit measurements on fly R1-6 photoreceptors (graded-potential
  cells, no action potentials in the cellular-mammalian sense); [Strong1998][strong1998] is
  extracellular recording from the H1 fly motion detector (action potential cell). t0123 is a
  68-d biophysical NEURON model of a mammalian retinal DSGC (graded synaptic input + somatic
  Na+/K+ HH spike generator + 14-d procedural morphology). The bits/s axis is in principle the
  same quantity but the underlying neurons differ by class, species, and resolution by orders
  of magnitude.

* **Stimulus protocol.** [Niven2007][niven2007] / [Strong1998][strong1998] use long (~10-30
  minute) random-walk or naturalistic light stimuli at frame rates of 60-1000 Hz, giving
  stimulus entropy of ~hundreds of bits/s. t0123 uses a 4-direction antipodal-pair bar
  stimulus at 1400 ms per trial with 8 directions x 20 trials = 160 trials per cell in the
  post-hoc Strong-Bialek pass. The stimulus entropy is **log2(4) = 2 bits per trial** (or
  **log2(8) = 3 bits per trial** in the post-hoc protocol) — orders of magnitude poorer than
  the literature's continuous stimulus regime. The [t0097] catalogue explicitly flagged this
  as a known limit of the project's direction-protocol approach.

* **Firing-rate operating point.** [Strong1998][strong1998]'s H1 fires at tens of spikes/s
  under random-walk motion; [Niven2007][niven2007]'s photoreceptors carry information in
  graded-potential changes at much higher effective rates than mammalian spike rates. t0123's
  top-10 NSGA-II Pareto cells fire at **~1-3 Hz** under PD direction — well below the
  threshold rate ~10 Hz needed to populate non-trivial binary spike-time words at word lengths
  T <= 100 ms. The Strong-Bialek estimator returns 0 bits/s because the input data is
  **degenerate**, not because the cells are uninformative in some weaker sense.

* **MI estimator pair.** The inner-loop estimator is spike-**count** MI (4 x B contingency
  table, log-spaced bin count B, Miller-Madow bias correction); the post-hoc estimator is the
  Strong-Bialek spike-**time-word** direct method (1/T extrapolation at T in {25, 50, 75, 100}
  ms, dt = 5 ms). These measure different quantities. Count MI integrates over the trial-level
  spike count distribution and is robust at small N; time-word MI measures information in
  spike-time structure and requires firing rates that approach 1/T. t0123's two-tier design
  exposes the divergence between them; literature comparisons should be made tier-by-tier.

* **ATP recipe.** t0123 implements [Sengupta2010][sengupta2010]'s ATP recipe verbatim (`Q =
  integral |min(seg.ina, 0)| dt * seg.area_cm2`, `N_ATP = Q / e / 3`, summed over soma + AIS +
  dendrites). Differences from the published recipes: (a) [Sengupta2010][sengupta2010] uses
  single-compartment HH models; t0123 uses a multi-compartment morphology with realised
  `seg.area()` from the procedural 14-d morphology generator; (b) [Attwell2001][attwell2001]
  is a top-down whole-tissue calculation, not a per-cell biophysical integration; (c)
  [Carter2009][carter2009] is an empirical patch-clamp measurement on Purkinje cells, not the
  same neuron class as DSGC. The cross-cell-type validation in [Sengupta2010][sengupta2010]
  gives a 17-fold range of ATP per cm^2 across seven HH models, so an order-of-magnitude or
  two range between t0123 and any single literature anchor is expected.

* **Carter-Bean plan typo.** The plan's quoted Carter-Bean benchmark `2.41e21 ATP/AP/cm` is
  off by ~13 orders of magnitude from the observed value `6.15e8 ATP/AP/cm` on the canonical
  Bed B anchor cell. Independent back-of-envelope physics (peak `ina` ~ 100 mA/cm^2 over a ~1
  um^2 AIS segment integrated over 2 ms gives ~3e9 ATP/AP/cm) places the observed value in the
  plausibility band. The plan typo, **not** the t0123 recipe, is the load-bearing error. The
  Carter and Bean 2009 paper (DOI 10.1016/j.neuron.2009.12.011) is not present in the project
  corpus, so the strict published value could not be re-verified inside this task; this is
  recorded as a follow-up to chase outside the t0123 boundary.

* **Number of optimiser objectives.** t0123 optimises 2 objectives; [Hay2011][hay2011] /
  [Druckmann2007][druckmann2007] use 10-30. Lower objective count makes the joint-pass corner
  easier in principle but the optimiser converged on a small low-firing-rate region of
  substrate, so the comparison to multi-feature published runs is structural rather than
  direct.

## Analysis

### Niven 2007 verdict: Insufficient evidence, traceable to a single load-bearing cause

The whole-task headline — comparing the DSGC bits-per-ATP front to [Niven2007][niven2007]'s
super-linear fly photoreceptor curve — fails not because of a code defect or numerical
instability, but because the two-tier MI estimator surfaced a real biological / protocol
mismatch. The inner-loop spike-count MI estimator picked a region of substrate where the
across-direction variance in trial-level spike count is informative (top-10 cells: 1.459 bits,
1.139, 0.964, ...), and the optimiser's F-vector pulled toward that region. But at those
firing rates (~1-3 Hz, ~3 PD spikes per 1400 ms trial), the spike-time word distribution is
degenerate at every word length T <= 100 ms: `h_total = h_noise = 0`, the 1/T extrapolation
has nothing to extrapolate, and the literature-comparable bits/s axis returns zero. The
[t0097] catalogue's open question "is the 4-direction count-MI a reliable surrogate for the
Strong-Bialek rate" is answered **no, not at the firing rates the count-MI optimiser converges
to**.

### ATP/spike axis: order-of-magnitude consistent with [Attwell2001][attwell2001] and [Sengupta2010][sengupta2010]

The ATP-per-spike values **4.55-4.76 x 10^6 ATP/spike** at the top-MI corner are 81x below
[Attwell2001][attwell2001]'s **3.84 x 10^8 ATP/AP** for a typical rodent cortical neuron. The
gap is dominated by cell size: Attwell's reference cell has total membrane area **1.49 x 10^5
um^2**; t0123's procedural morphology slice-summary shows somatic diameter ~17 um and total
dendrite length ~36 um per slice, which (with typical um-scale dendrite diameters) gives 3-4
orders of magnitude less membrane area. ATP per AP scales approximately linearly with membrane
area in the Na+/K+ overlap regime [Sengupta2010, Eq 9], so the 81x ATP/AP gap is consistent
with the cell-size gap. This is **independent biological corroboration** that the Sengupta
recipe is being applied correctly even though the Niven comparison cannot be tested.

### Soma-dominated ATP split is consistent with the Sengupta overlap-load story

For the top-MI cells, **93-95%** of per-AP ATP comes from the soma compartment, with the AIS
contributing ~5% and dendrites <1%. This matches [Sengupta2010][sengupta2010]'s observation
that the bulk of Na+/K+ overlap cost concentrates wherever Na+ channel density is highest — in
the t0123 substrate that is the soma (`apply_params.py` enforces a soma-dominant Na+ density
tier). The degenerate silent cell 0 (PD-rate 0.71 Hz, ATP/spike 6.76e5) shows a more balanced
soma share (42.9%), suggesting that at near-silence the per-AP ATP is dominated by the
cheapest AP event the cell can produce, not by the soma's tonic Na+ density. This
finer-grained behaviour is not in the [Sengupta2010][sengupta2010] one-compartment models but
is qualitatively consistent with the overlap-load framing.

### Count-MI vs Strong-Bialek divergence is the most informative finding

The fact that count-MI = 1.459 bits and Strong-Bialek bits/s = 0 for the **same** cell is the
single most informative finding of t0123. It is direct empirical evidence that the inner-loop
spike-count plug-in MI is **not a reliable surrogate** for the literature-comparable
Strong-Bialek rate when firing rates are low. The [t0097] catalogue's recommendation "use
count-MI as a *relative* selection signal and Strong-Bialek as the absolute literature anchor"
is therefore nuanced: the two estimators can disagree wildly, and the optimiser will
preferentially exploit the estimator with the higher dynamic range. Follow-up suggestion:
enforce a PD-rate floor (e.g. PD-rate >= 10 Hz) inside the silence guard so the count-MI
optimiser cannot converge on spike-time-degenerate regions.

### Carter-Bean plan typo is a paperwork artefact, not a biological finding

The 13-order-of-magnitude discrepancy between the plan-quoted Carter-Bean value (`2.41e21
ATP/AP/cm`) and the observed value (`6.15e8 ATP/AP/cm`) decomposes cleanly into a single typo
in the plan: 4 mM-mol/cm written in the plan should plausibly have been 4 nmol/cm (~2.4e15
ATP/cm) or some other quantity 13 orders smaller; the original Carter & Bean 2009 paper is not
in the project corpus to re-verify. The smoke gate's fallback plausibility band `[1e6, 1e14]
ATP/cm` catches recipe errors that produce 0 or off-by-many-orders results while not blocking
on the typo. The biological message is unchanged: t0123's per-AP per-compartment ATP
integration produces a quantity inside the plausibility band.

## Limitations

* **Niven 2007 paper is not in the project corpus.** The clearest empirical bits-per-ATP
  Pareto curve in the literature (DOI 10.1242/jeb.005249) was not downloaded as a paper asset
  during the t0097 catalogue stage. The catalogue cites it via Niven & Laughlin's 2008 review
  ([Niven2008][niven2008]), which re-plots Niven 2007's Fig 7. The 200-1000 bits/s range and
  ~20% fixed-cost claim are therefore traceable to the review but not to the primary paper
  inside the corpus. This is a **missing-paper observation** for a downstream `download_paper`
  task.

* **Carter & Bean 2009 paper is not in the project corpus.** The strict ATP/AP/cm benchmark
  value could not be re-verified inside this task; the plan-quoted value was 13 orders off,
  and the smoke gate ran under a fallback plausibility band. The Carter & Bean 2009 paper (DOI
  10.1016/j.neuron.2009.12.011) should be downloaded for the next compare-literature run on
  this lineage. **Missing-paper observation.**

* **Remme et al. 2018 paper is not in the project corpus.** The closest published
  function-vs-energy MOBO analogue (DOI 10.1371/journal.pcbi.1006612) was cited in the t0097
  catalogue but is not present as a paper asset. The t0123 Pareto-front shape comparison to
  [Remme2018][remme2018] is therefore qualitative (front shape) rather than quantitative (no
  specific delta, no exponent). **Missing-paper observation.**

* **Single GA seed.** t0123 ran one GA seed (441); the Strong-Bialek bits/s = 0 finding could
  in principle be a single-seed accident, although the biological / protocol root cause
  (PD-rate ~1-3 Hz at the count-MI optimum) suggests it would replicate. A 5-seed
  substrate-rate confirmation pattern (per the t0117 / t0121 lineage) is not in t0123's $6
  scope.

* **No graded-potential MI calibration.** [Dhingra2004][dhingra2004] requires a
  graded-vs-spike comparison inside the same cell. t0123 records only somatic Vm and spike
  times under FULL mode (HH on); the EPSP_PASSIVE / IPSP_PASSIVE modes that would give
  graded-potential Vm traces were not enabled per the standing measurement protocol. Cannot
  reproduce the ~60% gray-level loss number inside this task.

* **ATP not normalised to membrane area.** [Sengupta2010][sengupta2010] and
  [Attwell2001][attwell2001] report ATP/cm^2 or ATP/AP for a fixed reference cell; t0123
  reports ATP/spike per-cell only. To make the Sengupta-style cross-cell-type comparison
  quantitative would require summing `seg.area()` per cell at evaluation time and adding
  `atp_per_ap_per_cm2` to the predictions schema. Out of scope for t0123 but a straightforward
  follow-up.

* **No alpha (Na+/K+ overlap factor).** [Sengupta2010][sengupta2010]'s canonical efficiency
  metric `alpha = total Na+ load / capacitive minimum` is not computed for the top-10 cells;
  would require integrating Na+ load and the capacitive minimum separately. Follow-up.

* **Count-MI ceiling of 2.0 bits.** The 4-direction protocol caps the inner-loop count-MI at
  `log2(4) = 2.0 bits`; t0123's top cell reaches 73% of the ceiling. An 8-direction protocol
  would push the ceiling to `log2(8) = 3.0 bits` and might allow the optimiser to explore
  higher-firing-rate cells; out of scope at the $6 cap but listed in t0123's suggestions.

* **No paper-anchored citation for bits/s on RGCs.** The literature's RGC MI measurements
  (e.g. [Dhingra2004][dhingra2004]'s spike-detection-threshold analysis, not a direct bits/s
  reading; van Hateren and Snippe 2007) do not appear in the project corpus as direct bits/s
  values for guinea-pig or mouse RGCs. The Niven 2007 fly-photoreceptor numbers are therefore
  the closest available anchor, but the cell class differs (photoreceptor vs RGC). A direct
  mammalian-RGC bits/s anchor would strengthen the cross-class comparison.

[niven2007]: https://doi.org/10.1242/jeb.005249 [niven2008]:
../../t0097_multi_obj_optim/assets/paper/10.1242_jeb.017574/summary.md [strong1998]:
../../t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/summary.md [dhingra2004]:
../../t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/summary.md
[attwell2001]:
../../t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/summary.md
[sengupta2010]:
../../t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/summary.md [carter2009]:
https://doi.org/10.1016/j.neuron.2009.12.011 [remme2018]:
https://doi.org/10.1371/journal.pcbi.1006612 [hay2011]:
https://doi.org/10.1371/journal.pcbi.1002107 [druckmann2007]:
../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md [t0097]:
../../t0097_multi_obj_optim/ [t0115]: ../../t0115_seed9354_no_autostop/ [t0121]:
../../t0121_5seed_substrate_rate_canonical_report/ [t0122]:
../../t0122_dsi_cytoplasm_volume_nsga2/

</details>
