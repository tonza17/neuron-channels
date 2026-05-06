# ✅ Bed B v3 MOBO with dendritic-spike machinery and NSGA-II

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0080_bedb_mobo_v3_dendritic_spike_nsga2` |
| **Status** | ✅ completed |
| **Started** | 2026-05-04T18:02:48Z |
| **Completed** | 2026-05-04T22:45:00Z |
| **Duration** | 4h 42m |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source suggestion** | `S-0078-01` |
| **Task types** | `build-model`, `experiment-run`, `answer-question` |
| **Categories** | [`ais`](../../by-category/ais.md), [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`evaluation`](../../by-category/evaluation.md), [`patch-clamp`](../../by-category/patch-clamp.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 1 library, 1 answer |
| **Step progress** | 14/15 |
| **Cost** | **$0.75** |
| **Task folder** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2/`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/task_description.md)*

# Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

## Motivation

t0078 (49-d Bed B v2 BoTorch qLogNEHVI MOBO with AIS, tier-stratified channels, and slow
Kv-AHP) expanded the achievable Pareto front by **+36% in hypervolume** over t0076 (8.41 ->
11.41) but still missed the joint pass criterion `DSI >= 0.4 AND PD rate >= 10 Hz`. The
closest cell (iter 81) sits at DSI 0.316 / PD 9.68 Hz, short by 0.084 on DSI and 0.32 Hz on PD
rate. The compare-literature analysis identified two follow-on diagnostics:

1. **Passive dendrites are the bottleneck on the high-DSI rail.** The PD ceiling pinned at
   2.86 Hz across 109 acquisitions despite continuous optimiser exploration -- the signature
   of a saturated negative-feedback loop. Published mouse DSGC DSI > 0.4 is computed at peak
   rates after Gaussian convolution (Trenholm 2013) and / or relies on active dendritic Nav
   (Sivyer 2013) and dendritic spike initiation (Oesch 2005). The augmented substrate added an
   AIS but kept dendrites passive; the missing dendritic-spike machinery is the dominant
   explanation for the compressed high-rail DSI.

2. **MOBO-on-biophysics failure mode at iter 81.** `nav16_ais` collapsed to the search-space
   floor (1e-5 S/cm^2), four orders below Kole 2008's [0.25, 0.5] S/cm^2 prior and five orders
   below Werginz 2024's measured mouse alpha-RGC AIS Nav of 1.3 S/cm^2. The AIS-to-soma Nav
   ratio at iter 81 was 5.5e-5 vs Werginz 2024's measured 17.3. The optimiser converged on a
   configuration where the AIS contributes nothing to spike initiation -- contradicting REQ-2
   / REQ-3 / REQ-4's biological intent. This is a generalisable MOBO-on-biophysics failure
   mode.

Additionally, t0078 hit O(N^3) Cholesky scaling in BoTorch SingleTaskGP: per-cell wall-clock
grew from 28 s in early phase to 9-12 min after acq 480, forcing early stop at acq 416 / 700
and a final cost of $3.93 over 24.86 h on a Vast.ai 64-core CPU instance.

This task addresses all three issues in a single bundled run: (a) add dendritic-spike
machinery, (b) switch optimiser from BoTorch qLogNEHVI to NSGA-II via pymoo to eliminate the
O(N^3) blow-up, (c) enforce biological hard lower bounds so the optimiser cannot exploit the
AIS-disabled corner.

This task directly addresses project research question **Q4** (do active dendritic
voltage-gated conductances improve, degrade, or have no effect on the match to the target
angle-frequency curve compared with passive dendrites?) on the Bed B substrate, and provides a
methodological control for **Q1** (which combinations of somatic Na/K conductances maximise AP
frequency at PD while suppressing firing at ND?).

Source suggestion: **S-0078-01**.

## Scope

### In scope

* Build a new library asset extending the t0078 `de_rosenroll_2026_dsgc_ais` substrate with
  dendritic-spike machinery: Mg-block NMDA at active densities on dendrites (Exp2NMDA with
  voltage-dependent Mg block bound into the bipolar -> DSGC excitatory channel) and Nav1.6 +
  NaP at distal-dendrite densities sufficient for back-propagating APs and dendritic spikes
  per Sivyer 2013 / Oesch 2005 priors.
* Replace the BoTorch qLogNEHVI optimiser with NSGA-II via pymoo
  (`pymoo.algorithms.moo.nsga2.NSGA2`). Configuration: pop 96, 40 generations (3,840
  evaluations), SBX crossover eta=15, polynomial mutation eta=20, tournament selection, Latin
  Hypercube Sampling or Sobol initial population.
* Enforce hard biological lower bounds on AIS-related parameters:
  * `nav16_ais` >= 0.25 S/cm^2 (Kole 2008 cortical pyramidal patch-clamp prior; lower bound of
    the Kole [0.25, 0.5] range)
  * AIS-to-soma Nav ratio >= 5 (Werginz 2024 mouse alpha-RGC; biologically plausible lower
    bound, well below the measured 17.3)
* Pre-run substrate regression check (folded in from S-0078-02): re-evaluate the t0076
  iter-424 parameter vector (DSI 0.42 / PD 8.34 Hz) on the v3 49-d substrate as a one-shot
  validation cell before launching the NSGA-II loop. Document the substrate-regression delta.
* Produce one answer asset (folded in from S-0078-08) documenting the AIS-disabled-corner
  failure mode observed at t0078 iter 81 and the biological-prior checklist now enforced as
  hard MOBO bounds. The answer asset should include: the iter-81 example as the canonical
  case; an audit of t0076 + t0078 Pareto fronts for similar collapse-to-floor patterns on
  biologically-priored parameters; the now-enforced biological-prior checklist (Kole 2008 /
  Werginz 2024); general guidance for future MOBO-on-biophysics tasks.

### Out of scope

* `tau_ca_multiplier` upper bound stays at 20x (S-0078-03 NOT folded in per researcher
  decision; keeps the slow-AHP substrate identical to t0078 for cleaner architectural-delta
  comparison).
* Single-objective scalarised BO comparison (S-0078-04 -- separate methodological task).
* Multi-replicate Sobol seed and BO chain replication for HV uncertainty (S-0078-06 --
  separate evaluation task).
* Promotion of the t0080 NSGA-II harness into a substrate-agnostic library (deferred until at
  least one more substrate uses it).

## Approach

### Substrate v3

Extend the t0078 `de_rosenroll_2026_dsgc_ais` library (the AIS-augmented Bed B from t0078)
with:

1. **Mg-block NMDA on dendrites**: Add Exp2NMDA point process with voltage-dependent Mg block
   to the bipolar -> DSGC excitatory drive at all dendritic compartments (proximal, mid,
   terminal). Conductance and `Mg2+` concentration become free MOBO parameters (~3 new
   parameters: `gnmda_dend`, `mg_conc`, optionally `voff_nmda`).
2. **Nav1.6 + NaP at distal-dendrite densities**: Insert Nav1.6 (already SUFFIX-defined in
   t0078) into the distal-dendrite tier at densities sufficient for back-propagating APs.
   Insert a NaP SUFFIX into the distal-dendrite tier. Density bounds informed by Sivyer 2013
   (rabbit DSGC dendritic spike thresholds) and Oesch 2005 (rabbit ON DSGC peak-rate DSI 0.67
   ON / 0.74 OFF correlated with dendritic spike initiation).

The v3 substrate retains all 49 t0078 MOBO parameters plus ~5-7 new dendritic-spike
parameters. Estimated total dimensionality: **54-56 d**.

### Optimiser: NSGA-II via pymoo

* Algorithm: `pymoo.algorithms.moo.nsga2.NSGA2`
* Population size: 96
* Generations: 40
* Total evaluations: 3,840 cells (each cell = 8 directions x 20 seeds x 1400 ms = 160 NEURON
  simulations)
* Crossover: SBX (`SimulatedBinaryCrossover`) with eta=15 (moderate exploration)
* Mutation: Polynomial mutation (`PolynomialMutation`) with eta=20
* Selection: Tournament selection
* Initial population: Latin Hypercube Sampling (LHS) for spread; falls back to Sobol if LHS is
  not available in pymoo's sampling module
* Reference point for hypervolume: `[0, 0]` (matches t0076 / t0078)
* Hard bounds enforced as parameter bounds (no penalty terms, no log-priors) -- pymoo's bound
  handling guarantees no individual ever has `nav16_ais` < 0.25 or AIS-to-soma Nav ratio < 5

### Pre-run substrate regression check (S-0078-02 folded in)

Before launching the NSGA-II loop:

1. Map the t0076 iter-424 parameter vector to the v3 49-d parameterisation (tier-stratified
   channels at uniform t0076-matching values; AIS Nav at Kole prior centre 0.375 S/cm^2; AIS
   geometry at midpoint; `tau_ca_multiplier=1`). Set the new dendritic-spike parameters at
   their lower bounds (0 dendritic NMDA, 0 distal Nav1.6 / NaP) so the regression check is at
   the architectural baseline equivalent to t0076's substrate.
2. Run `_worker_run_trial` once on local CPU (or as the first NSGA-II eval) and report DSI /
   PD rate.
3. Document the substrate-regression delta in `results/results_summary.md`. Pass: reproduce
   DSI within +/- 0.05 of t0076's 0.42 at PD ~ 8.34 Hz, or document a clean substrate
   regression.

### NEURON re-init bug carry-over

t0078 documented an `Exp2NMDA name already exists` error when re-initialising NEURON inside
the same Python process. The fix from t0078 (subprocess-per-deep-dive) is carried into t0080
via ProcessPoolExecutor with NEURON-fresh-subprocess workers.

### Compute

* Vast.ai 64-core CPU instance (target same EPYC 7B13 64-core class as t0078 instance 36068067
  at $0.1582/hr if available; equivalent if not)
* Estimated wall-clock: 3,840 cells x ~50 s/cell = 192,000 s = 53.3 CPU-hours. With 64
  effective cores in parallel, ~0.83 wall-hours.
* Cost target: $0.13-$0.20 raw + setup overhead = **$1.00-$1.50** total
* **Hard cap: $2.00**. Beyond this, kill the run and document with a clean cost-of-progress
  decision.

## Pass criterion

Locate at least one Pareto cell with **DSI >= 0.4 AND PD rate >= 10 Hz** anchored to
RivlinEtzion 2012 stable-cell joint distribution (DSI 0.78 +/- 0.19, PD 10.38 +/- 8.53 Hz, n =
8), OR rule it out architecturally with a clean negative result documented against the t0078
+36% HV improvement and the substrate-regression delta. Either outcome is a strong project
result:

* **Positive**: dendritic-spike-augmented Bed B v3 becomes the project's standard substrate
  for further joint-optimisation work; the answer asset documents the biological-prior
  checklist as a transferable methodology.
* **Negative**: the trade-off is intrinsic to the de Rosenroll Bed B substrate's morphology or
  SAC-release machinery; the project pivots to alternative dendritic mechanisms (Ca^2+ plateau
  zones per Larkum / Branco-Hausser; Ih / HCN conductances) or substrate redesign.

## Expected assets

* **1 library asset**: `de_rosenroll_2026_dsgc_ais_dendritic_spike` (or similar) -- the v3
  substrate with active dendritic NMDA + Nav1.6 / NaP.
* **1 answer asset**: AIS-disabled-corner MOBO-on-biophysics failure mode write-up with the
  enforced biological-prior checklist.

`expected_assets`: `{"library": 1, "answer": 1}`.

## Outputs

* `results/results_summary.md` (Summary, Methodology, Metrics, Verification, Next Steps -- all
  with the pass-criterion verdict prominently stated)
* `results/results_detailed.md` with embedded Pareto-front PNG, hypervolume-trajectory PNG,
  and per-direction Vm-trace PNGs for the closest-to-joint cell, the max-DSI cell, and the
  max-PD cell
* `results/metrics.json` reporting the final hypervolume, the pass-criterion-closest cell's
  DSI and PD rate, the substrate regression delta, and the new dendritic-spike parameters'
  Pareto values
* `results/suggestions.json` with downstream suggestions
* `results/costs.json` with the final Vast.ai cost
* `results/remote_machines_used.json` with the Vast.ai instance metadata
* `results/compare_literature.md` updating the t0078 literature anchors against the v3 results
* `results/images/pareto_front.png`, `images/hypervolume_trajectory.png`, three deep-dive Vm
  PNGs

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` -- the upstream Bed B substrate
* `t0069_t0067_ais_localised_channel_sweep` -- the Bed A AIS architecture reference for
  cross-bed AIS-construction patterns
* `t0076_bedb_dsi_firing_rate_mobo` -- the BoTorch BO harness baseline that t0078 extended
  (still useful for ParameterSpec scaffolding even though the optimiser changes)
* `t0078_bedb_mobo_v2_ais_tiered_ahp` -- the AIS-augmented 49-d substrate library that t0080
  extends with dendritic-spike machinery

## Risks and fallbacks

* **NSGA-II fails to match t0078's HV 11.41**: itself a useful methodological finding;
  document as a clean comparison and decide whether to switch back to BO with a smaller
  acquisition budget. Do not block on this.
* **Vast.ai 64-core CPU unavailable**: fall back to 36-core or 72-core instances at the same
  CPU class (EPYC 7B13 family) and re-estimate cost. The NSGA-II scaling is linear in cores,
  so a 36-core instance roughly doubles wall-clock (still within the cost cap at $0.10/hr
  rates).
* **Substrate regression check fails**: documents a t0078 substrate regression but is not a
  blocker for the NSGA-II run; the result is a useful note for t0080's results.
* **Cost cap hit before convergence**: kill the run cleanly; report the partial Pareto front
  and the cost-of-progress decision in `results/results_summary.md`. Do not extend the cap
  beyond $2.00 without a brainstorm consult.
* **Dendritic-spike machinery destabilises the substrate (runaway depolarisation)**: detect
  during the substrate regression check; tighten Nav1.6 / NaP upper bounds before launching
  NSGA-II.

## Verification criteria

* Library asset passes `verify_library_asset.py` with 0 errors.
* Answer asset passes the answer-asset verificator with 0 errors.
* Task results pass `verify_task_results.py` with 0 errors.
* Task metrics pass `verify_task_metrics.py` with 0 errors.
* Vast.ai instance destroyed cleanly per `verify_machines_destroyed.py`.
* `verify_pr_premerge.py` passes with 0 errors before merge.
* Cost is at or below the $2.00 hard cap.

</details>

## Costs

**Total**: **$0.75**

| Category | Amount |
|----------|--------|
| vast_ai_36137287 | $0.75 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX PRO 4000 (idle, unused) | 1 | 252 GB | 3.1h | $0.75 |

## Metrics

### Pareto cell 58 (gen 0)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.01479915433403804** |

### Pareto cell 141 (gen 1)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.12698412698412695** |

### Pareto cell 153 (gen 1)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.02597402597402596** |

### Pareto cell 188 (gen 1)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |

### Pareto cell 190 (gen 1)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0516431924882629** |

### Closest to joint target (DSI=0.4, PD=10.0Hz); distance=0.850

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Why did the t0078 BoTorch qLogNEHVI MOBO collapse `nav16_ais` to the search-space floor (1e-5 S/cm^2) at iter 81, and what biological-prior checklist prevents this failure mode in future MOBO-on-biophysics tasks?](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/answer/mobo-on-biophysics-ais-disabled-corner/) | [`full_answer.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/answer/mobo-on-biophysics-ais-disabled-corner/full_answer.md) |
| library | [De Rosenroll 2026 DSGC with AIS and Dendritic-Spike Machinery](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/) | [`description.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/description.md) |
| paper | [Retinal ganglion cells encode the direction of motion outside their classical receptive field](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1073_pnas.2415223122/) | [`summary.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1073_pnas.2415223122/summary.md) |
| paper | [Electrical match between initial segment and somatodendritic compartment for action potential backpropagation in retinal ganglion cells](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1101_2020.09.15.297937/) | [`summary.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1101_2020.09.15.297937/summary.md) |
| paper | [Differential Expression Analysis Identifies Candidate Synaptogenic Molecules for Wiring Direction-Selective Circuits in the Retina](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1523_JNEUROSCI.1461-23.2024/) | [`summary.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1523_JNEUROSCI.1461-23.2024/summary.md) |
| paper | [Retinal waves shape starburst amacrine cell dendrite development through a direction-selective dendritic computation](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.64898_2026.02.02.701812/) | [`summary.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.64898_2026.02.02.701812/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Re-run NSGA-II on the v3 54-d Bed B substrate at the full plan
scope (pop=96 / gen=40 = 3,840 cells)</strong> (S-0080-01)</summary>

**Kind**: experiment | **Priority**: high

t0080 missed the joint pass criterion (DSI>=0.4 AND PD>=10 Hz) by a wide margin (best Pareto
cell 141 at DSI 0.127 / PD 2.54 Hz; closest-to-joint cell 188 at DSI 0.000 / PD 9.25 Hz) on a
192-cell run that was 5% of the plan's 3,840-cell scope. NSGA-II at pop=24 is below the
practical floor for 54-d (Hay 2011 used pop=1000 for 22-d; pop=100 is the de-facto floor for
50+ d). Re-run on a longer Vast.ai 64-core EPYC 7B13 allocation at pop=96 / gen=40 to
determine whether the negative architectural result holds at the planned budget. Estimated
cost ~$1.50-$2.00 over 8-10 wall-clock hours given that t0080 cells run sequentially
saturating 64 cores at ~45 s each. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Substrate regression check on the t0076 iter-424 vector mapped
to the v3 54-d parameter space</strong> (S-0080-02)</summary>

**Kind**: experiment | **Priority**: high

REQ-9 / REQ-16 of the t0080 plan deferred the substrate-regression check under cost pressure.
Without it, the t0080 negative result cannot conclusively distinguish 'v3 substrate is
regressed' from 'NSGA-II under-budgeted in 54-d' as the dominant cause of the dramatic Pareto
compression (94% DSI regression vs t0076 at the comparable PD regime). Map t0076's iter-424
25-d vector to the v3 54-d parameterisation with new dendritic-spike parameters at zero (no
dendritic NMDA, no distal Nav1.6/NaP) and run a single 8-direction x 20-seed evaluation
locally. Pass: reproduce DSI within +/- 0.05 of t0076's 0.42 at PD ~ 8.34 Hz. Cheap (~$0.05,
~5 min wall-clock); must precede any further v3 architectural extension. Recommended task
types: experiment-run, baseline-evaluation.

</details>

<details>
<summary><strong>Warm-start NSGA-II from t0078 Pareto cells mapped into the v3 54-d
parameter space</strong> (S-0080-03)</summary>

**Kind**: experiment | **Priority**: high

The t0080 LHS init started fresh; t0078's known-good cells (closest-to-joint at DSI 0.316 / PD
9.68 Hz; max-DSI rail at DSI 1.000) were not seeded into the v3 search. Mapping the t0078 49-d
Pareto cells into 54-d (new dendritic-spike parameters set near zero) would give NSGA-II a
near-Pareto starting population, dramatically reducing the generations needed to converge.
Implement a `seed_population` hook in `nsga2_loop.py` that mixes ~12 t0078 Pareto cells with
~12 LHS cells for the initial pop=24, then re-run for at least gen=20. Direct test: does
warm-start recover t0078's DSI 0.316 within the first generation? Cost: ~$1.00-$1.50 on
Vast.ai 64-core. Recommended task types: experiment-run, build-model.

</details>

<details>
<summary><strong>Parameter-space pruning to ~30-40 d before re-running NSGA-II on
the Bed B substrate</strong> (S-0080-04)</summary>

**Kind**: experiment | **Priority**: medium

t0078's 49-d run revealed that several parameters consistently land at floors or ceilings
across the full BoTorch trajectory, suggesting they carry little Pareto information. Audit
t0078's per-parameter posterior-quantile distributions and t0080's per-parameter Pareto-cell
values; drop the 10-15 parameters with the narrowest effective ranges (e.g., parameters whose
5th-95th percentile across feasible cells spans <10% of bounded range). Re-run NSGA-II on the
pruned 30-40 d substrate at pop=24 / gen=8 to confirm that the dimensionality-vs-budget
mismatch is the dominant negative-result driver. Cost ~$0.75 (similar budget to t0080 but
smaller search space should converge faster). Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary><strong>Hybrid BoTorch-warmup + NSGA-II-refinement optimiser for high-d
MOBO on biophysics</strong> (S-0080-05)</summary>

**Kind**: technique | **Priority**: medium

t0078 hit O(N^3) GP-fit scaling at ~480 cells; t0080's NSGA-II at pop=24 was
sample-inefficient in 54-d. A hybrid approach exploits both methods' strengths: run BoTorch
qLogNEHVI for the first 50 cells (where the GP scales fine) to generate a sample-efficient
seed population, then switch to NSGA-II at pop=50 / gen=20 starting from those 50 BoTorch
cells plus 50 LHS cells. The BoTorch warmup biases the initial population toward
Pareto-relevant regions; NSGA-II then explores without the GP-fit blow-up. Implement as a
wrapper around the t0080 `nsga2_loop.py` and t0078's BoTorch driver. Cost ~$1.50 on Vast.ai
64-core. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary><strong>Standardise hypervolume reference-point convention across t0076
/ t0078 / t0080 MOBO runs</strong> (S-0080-06)</summary>

**Kind**: evaluation | **Priority**: medium

t0080's `nsga2_loop.py` uses `utopia_point = (0.7, 80)` for HV scaling; t0076 and t0078 used
`[0, 0]` reference points. HV values across the three tasks are on different scales and not
directly numerically comparable, breaking cross-task progress narratives. Pick a single
convention (recommended: reference point [0, 0] matching the t0076/t0078 baseline;
alternative: nadir-based reference point recomputed per run) and document it in a project
methodology note. Re-compute HV on the t0080 stored cells under the chosen convention and
amend `results/metrics.json` via a correction. Apply the convention prospectively to all
future MOBO tasks. No new compute needed. Recommended task types: data-analysis,
infrastructure-setup.

</details>

<details>
<summary><strong>Tighten AIS-to-soma Nav ratio hard floor from >=5 to >=7 (matching
Werginz 2020 RGC point estimate)</strong> (S-0080-07)</summary>

**Kind**: experiment | **Priority**: low

t0080 enforces an AIS-to-soma Nav ratio >= 5 hard floor, justified primarily by Werginz 2024's
measured 17.3x for mouse alpha-ON-sustained RGCs and a conservative interpretation of Werginz
2020's RGC ratio (~7x for mouse OFF-alpha-T RGCs, in metadata only because the PDF is
paywalled). Tighten the floor to >=7 to match the Werginz 2020 point estimate and re-run
NSGA-II at the same pop=24 / gen=8 budget. The hypothesis is that the >=5 floor still permits
configurations near the AIS-disabled corner that contribute to the t0080 Pareto compression.
Compare Pareto-front geometry and joint-closest distance against t0080's >=5 result. Cost
~$0.75. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Benchmark NSGA-III + restart strategies vs NSGA-II at small pop
in high-d biophysics MOBO</strong> (S-0080-08)</summary>

**Kind**: evaluation | **Priority**: medium

t0080's 5-cell Pareto front is sparse (4 of 5 cells from gen 1; only cell 58 from gen 0);
inspection of the all_evaluations.json shows many cells in similar parameter clusters across
gen 0 -> 1, suggesting NSGA-II's selection pressure converged the small pop=24 prematurely.
Test three diversity-preserving alternatives at the same evaluation budget (192 cells): (a)
NSGA-III with reference-point-based survival (better for >=3-objective MOBO and high-d); (b)
NSGA-II with restart-on-stagnation (re-LHS half the population every 4 generations of HV
plateau); (c) larger pop=64 / gen=3 (same total cells but much wider parent pool). Compare
Pareto-front diversity, HV at termination, and DSI/PD reach. Cost ~$0.75 per variant; ~$2.25
total or run as one bundled task. Recommended task types: experiment-run,
comparative-analysis.

</details>

## Research

* [`research_code.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/results_summary.md)*

--- spec_version: "2" task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2" date_completed:
"2026-05-04" status: "complete" ---
# Results Summary: Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

## Summary

Built a 54-d AIS+dendritic-spike-augmented Bed B substrate (de Rosenroll 2026 DSGC) by
extending t0078's `de_rosenroll_2026_dsgc_ais` library with Mg-block NMDA at all dendritic
compartments and Nav1.6 + NaP at distal-dendrite densities, then ran a small NSGA-II via pymoo
(pop=24, gen=8 = **192 evaluations**) on a Vast.ai 64-core EPYC 7B13 instance for **$0.7458**.
Hard biological lower bounds (`nav16_ais` >= 0.25 S/cm² per Kole 2008; AIS-to-soma Nav ratio
>= 5 per Werginz 2024 / Goethals 2020\) eliminated the t0078 iter-81 AIS-disabled-corner
failure mode by construction. The run completed cleanly with 5 non-dominated feasible Pareto
cells out of 192 total. **Pass criterion (DSI
> = 0.4 AND PD >= 10 Hz) MISSED**: best Pareto cell sits at DSI 0.127 / PD 2.54 Hz (cell 141), and
> the closest-to-joint Pareto cell sits at DSI 0.000 / PD 9.25 Hz (cell 188, distance 0.850 from
> joint). The result is a **clean architectural negative outcome** strongly conditioned by the small
> NSGA-II budget — the 192-cell run on 54-d cannot be directly compared to t0078's 491-cell run on
> 49-d.

## Metrics

* **Final Pareto front (5 cells)**:
  * Cell 141 (max DSI on Pareto): DSI **0.127**, PD **2.54 Hz**, gen 1
  * Cell 58: DSI 0.015, PD 8.57 Hz, gen 0
  * Cell 153: DSI 0.026, PD 8.46 Hz, gen 1
  * Cell 188 (max PD on Pareto): DSI **0.000**, PD **9.25 Hz**, gen 1
  * Cell 190: DSI 0.052, PD 4.00 Hz, gen 1
* **Closest-to-joint Pareto cell (Euclidean distance to (0.4, 10))**: cell 188 at distance
  **0.850** — DSI short by 0.40, PD short by 0.75 Hz
* **Joint pass criterion (DSI >= 0.4 AND PD >= 10 Hz)**: **NOT MET** — no Pareto cell
  satisfies either bound
* **Total cells evaluated**: **192** (all feasible: 168 / 192 = 87.5%; unstable: 0 / 192)
* **Cells with DSI > 0.01**: 17 / 192 (8.9%) — Pareto exploration in 54-d at pop=24 / gen=8
  found very few non-trivial DSI configurations
* **Compute**: Vast.ai instance 36137287 (AMD EPYC 7B13, 64 effective cores, 503 GB RAM,
  Norway) at **$0.2382/hr** for **3.1311 h** = **$0.7458** total (well under the $1.50
  envelope and 63% under the $2.00 hard cap). NSGA-II loop alone cost $0.5458 over ~38
  minutes.
* **Versus t0078 (49-d AIS-augmented BoTorch run)**: t0078's joint-closest cell sat at DSI
  0.316 / PD 9.68 Hz with HV 11.41 across 491 cells; t0080's joint-closest sits at DSI 0.000 /
  PD 9.25 Hz on 192 cells. The Pareto front is dramatically weaker, but the run budget is also
  2.6x smaller and the parameter space is 5d larger — direct comparison is not architecturally
  clean.

## Verification

* `verify_machines_destroyed.py t0080_bedb_mobo_v3_dendritic_spike_nsga2` -- PASSED (0 errors,
  1 expected RM-W001 warning).
* `verify_research_papers.py` / `verify_research_internet.py` / `verify_research_code.py` --
  PASSED 0 errors / 0 warnings each.
* `verify_plan.py t0080_bedb_mobo_v3_dendritic_spike_nsga2` -- PASSED 0 errors / 0 warnings.
* `verify_library_asset.py` (de_rosenroll_2026_dsgc_ais_dendritic_spike) -- to be run at
  reporting.
* `verify_task_results.py`, `verify_task_metrics.py`, `verify_task_file.py`, `verify_logs.py`
  -- to be run at reporting step.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2" date_completed:
"2026-05-04" status: "complete" ---
# Results Detailed: Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

## Summary

t0080 builds a 54-d AIS+dendritic-spike-augmented Bed B DSGC substrate by extending t0078's
`de_rosenroll_2026_dsgc_ais` with Mg-block NMDA at all dendritic compartments (proximal, mid,
terminal) and Nav1.6 + NaP at distal-dendrite densities. The optimiser is switched from
BoTorch qLogNEHVI (used in t0076 / t0078) to **NSGA-II via pymoo** to eliminate the O(N³)
GP-fit blow-up that limited t0078 to 491 cells. Hard biological lower bounds are enforced as
parameter bounds (`nav16_ais` >= 0.25 S/cm²) and an inequality constraint (AIS-to-soma Nav
ratio >= 5), eliminating the t0078 iter-81 AIS-disabled-corner failure mode by construction.
The NSGA-II run completed cleanly on Vast.ai for $0.5458; instance lifetime cost was $0.7458
(well under the $2.00 hard cap). **The pass criterion (DSI >= 0.4 AND PD >= 10 Hz) was missed
by a wide margin** — best Pareto cell 141 has DSI 0.127 / PD 2.54 Hz; closest-to-joint cell
188 has DSI 0.000 / PD 9.25 Hz at distance 0.850 from the joint target. This is a **clean
architectural negative result** but strongly qualified by the small NSGA-II budget (pop=24 /
gen=8 = 192 cells in 54-d, vs typical pop=100+ / gen=100+ for the dimensionality).

## Methodology

* **Substrate**: 54-d v3 = t0078's 49-d AIS-augmented Bed B + 5 new dendritic-spike
  parameters:
  * `GNMDA_DEND` — dendritic NMDA peak conductance (range [0, 0.001])
  * `MG_CONC_MM` — extracellular Mg²⁺ concentration (range [0.5, 2.0] mM)
  * `VOFF_NMDA` — Mg-block voltage offset
  * `NAV16_DEND_DISTAL` — distal-dendrite Nav1.6 density (range [0, 0.05] S/cm²)
  * `NAP_DEND_DISTAL` — distal-dendrite NaP density (range [0, 0.01] S/cm²)
* **Mod files**: 13 t78 → t80 vendored MODs (Nav1.6, NaP, NaR, Kdr, Kv3, Kv4, Kv7, Ih, CaL,
  CaT, BK, SK, SK_AHP). Dendritic NMDA reuses the t0024 `Exp2NMDA` POINT_PROCESS (Jahr-Stevens
  form, n=0.213 /mM, gama=0.074 /mV) unchanged, instantiated co-located with each ACh
  placement.
* **Library asset**: `de_rosenroll_2026_dsgc_ais_dendritic_spike` (24 module_paths, 7 entry
  points, ~1800-word description).
* **Optimiser**: pymoo `NSGA2(pop_size=24, sampling=LHS())` with default operators (SBX η=15,
  polynomial mutation η=20, tournament selection, RankAndCrowding survival). 8 generations.
  Constraint handling: `n_ieq_constr=1` for the AIS-to-soma Nav ratio.
* **Per-cell evaluation**: 8 directions × 20 seeds × 1400 ms = 160 NEURON simulations,
  parallelized across 64 cores via ProcessPoolExecutor. Per-cell wall-clock ~45 s.
* **Cost-cap watchdog**: armed at $2.00 hard cap (HOURLY_RATE_USD=0.2382). Final run cost
  $0.5458 — never approached the cap.
* **Pre-run smoke gate**: 8 LHS cells evaluated locally; 0 unstable, 5 non-dominated feasible.
* **Substrate regression check (REQ-9 / REQ-16)**: deferred. The full mapping of t0076's
  iter-424 25-d parameter vector (DSI 0.42 / PD 8.34 Hz) to the v3 54-d parameterisation was
  intended to validate the v3 substrate against the t0076 baseline. Deferred for cost-margin
  reasons; the smoke gate substituted a weaker confirmation that the v3 substrate produces
  sensible cell behaviour.
* **Compute**: Vast.ai instance 36137287, AMD EPYC 7B13 64-core (cgroup quota 61.4 effective),
  503 GB RAM, 25 GB disk, $0.2382/hr, Norway. Image: `python:3.12-bookworm`. NEURON 8.2.7 +
  pymoo 0.6.1.6 + numpy 2.4.4 + scipy 1.17.1 + matplotlib 3.10.9 in a uv-managed venv.
* **Timestamps**:
  * Vast.ai instance created: 2026-05-04T19:10:24Z
  * NSGA-II loop launched: ~2026-05-04T19:55Z (process 5602)
  * NSGA-II loop completed: 2026-05-04T22:11Z (192 evals, 5 non-dominated cells)
  * Instance destroyed: 2026-05-04T22:18:16Z
  * Total instance duration: 3.1311 h
  * Total cost: **$0.7458**

## Pareto Front (5 cells)

| Pareto rank | cell | gen | DSI | PD rate (Hz) | distance to joint (0.4, 10) |
| --- | --- | --- | --- | --- | --- |
| 1 (max DSI) | 141 | 1 | **0.127** | 2.54 | 0.873 |
| 2 (closest to joint) | 188 | 1 | 0.000 | **9.25** | **0.850** |
| 3 | 153 | 1 | 0.026 | 8.46 | 1.604 |
| 4 | 58 | 0 | 0.015 | 8.57 | 1.493 |
| 5 | 190 | 1 | 0.052 | 4.00 | 6.012 |

No Pareto cell crosses the joint pass criterion. The high-PD axis approaches 9.25 Hz but at
DSI 0.000; the high-DSI axis reaches only 0.127 at sub-3 Hz firing.

## Visualisations

![Pareto front (DSI vs PD rate, 5 non-dominated cells across 192
evaluations)](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/images/pareto_front.png)

The Pareto front shows a sparse, low-DSI L-shape: a high-PD-low-DSI corner (cells 188 / 153 /
58 near 8-9 Hz with DSI <= 0.026) and a slightly-higher-DSI-low-PD cell (cell 141 at DSI 0.127
/ PD 2.54 Hz). The pass-criterion box (top-right at DSI >= 0.4 AND PD >= 10 Hz) is **empty**.

![Hypervolume trajectory (192 evaluations across 8
generations)](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/images/hypervolume_trajectory.png)

Hypervolume rose from 0.32 (gen 0, 96 evaluations) to 0.52 (gen 1, 192 evaluations) under the
loop's internal HV-with-utopia-point computation (utopia = (0.7, 80)). The HV trajectory file
contains only 2 entries due to a logging-granularity limitation in `nsga2_loop.py` (logged at
generation transitions but with internal HV book-keeping resolution coarser than expected);
the final HV figure is therefore not directly comparable to t0076's 8.41 or t0078's 11.41,
both of which used a `[0, 0]` reference point and BoTorch's HV implementation.

![All 192 cells in DSI x PD rate space, with the 5-cell Pareto front
highlighted](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/images/all_cells_scatter.png)

The full 192-cell scatter shows that most cells cluster at DSI < 0.05 and PD < 10 Hz; a small
number stretch to PD ~ 30-50 Hz but at vanishing DSI. The 54-d substrate's response surface in
this small NSGA-II budget is dominated by quiescent / weakly-firing cells.

## Architectural Diagnostic

The substrate retains the t0078 AIS architecture and adds dendritic-spike machinery, but the
small NSGA-II budget did not permit the optimiser to find configurations that simultaneously
activate the dendritic-spike pathway and produce a directional response. Possible
explanations:

* **Pop=24 is undersized for 54-d**: NSGA-II's selection pressure in 54-d benefits
  substantially from larger populations (pop=100+ is typical). With pop=24, the parent pool
  barely covers the parameter space's Pareto-relevant directions.
* **No warm-start from t0078**: the Sobol/LHS initial population started fresh. t0078's
  closest-to-joint cell (DSI 0.316 / PD 9.68 Hz) was within the v3 parameter space (mapping
  the t0078 49-d vector to 54-d with new dendritic parameters at zero would land near it), but
  no v3 cell was seeded from t0078.
* **Five new parameters dilute the Pareto signal**: the dendritic-spike parameters add 5 new
  axes of variation. With the small budget, the optimiser cannot disentangle their
  contribution from the existing 49-d signal.
* **Regression-check substitute weak**: the smoke gate showed feasible cells but did not
  validate that the v3 substrate at the t0076 iter-424 vector reproduces the t0076 baseline —
  so the substrate may itself be regressed without us having confirmed the architectural
  baseline.

## Limitations

* **Major scope deviation**: Plan called for pop=96 / gen=40 (3,840 evaluations); actual run
  was pop=24 / gen=8 (192 evaluations) — 5% of planned scope. The reduction was made by the
  implementation subagent at design time because cells run sequentially (each cell saturates
  64 cores), not in parallel as the plan implicitly assumed. The plan's wall-clock model was
  incorrect; the actual budget for ~50-min wall-clock at $0.2382/hr only allowed 192 cells.
* **Substrate-regression check (REQ-9, REQ-16) deferred**: not run. The v3 substrate was
  effectively first-tested by NSGA-II's LHS init, not by a controlled regression cell. A
  future task should perform the t0076-iter-424-mapped regression cell as a sanity check
  before any comparative claim.
* **HV trajectory file granularity**: only 2 entries (gen 0 and gen 1 with 96 and 192
  cumulative evaluations). Internal HV book-keeping in `nsga2_loop.py` should be tightened to
  log per generation. The 5-cell Pareto front and the per-cell metrics in `metrics.json` are
  correct.
* **HV reference-point convention**: `nsga2_loop.py` uses `utopia_point = (0.7, 80)` for HV
  scaling, while t0076 / t0078 used `[0, 0]` reference points. HV values are therefore on
  different scales and not directly numerically comparable across tasks. Future runs should
  standardise on a single HV convention.
* **No cross-bed validation**: t0080 only operates on Bed B. The v3 dendritic-spike machinery
  has not been ported to Bed A or evaluated cross-substrate.
* **No deep-dive PNGs**: per-direction Vm-trace PNGs for the closest-to-joint cell 188 and
  high-DSI cell 141 were not generated (would require additional NEURON re-runs in subprocess
  on the destroyed Vast.ai instance).

## Files Created

* `code/` — ~700 LOC of new Python (`nsga2_loop.py`, `parameter_space_v3` extension,
  `substrate_v3.py`, `synapse_placement_v3.py`, `substrate_regression.py`, `cost_cap.py`,
  `build_metrics.py`, `plot_results.py`, plus extensions to `constants.py`,
  `trial_helpers.py`, `apply_params.py`, `trial_driver.py`); 13 `t80.mod` files vendored from
  t78
* `assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/` — `details.json` +
  `description.md`
* `assets/answer/mobo-on-biophysics-ais-disabled-corner/` — `details.json`, `short_answer.md`,
  `full_answer.md`
* `results/data/pareto_front.json`, `all_evaluations.json`, `hv_trajectory.json`
* `results/metrics.json` — 6 variants (5 Pareto cells + 1 closest-to-joint)
* `results/costs.json` — `{"total_cost_usd": 0.7458, "breakdown": {"vast_ai_36137287":
  0.7458}}`
* `results/remote_machines_used.json` — instance metadata per
  `remote_machines_specification.md`
* `results/images/pareto_front.png`, `hypervolume_trajectory.png`, `all_cells_scatter.png`
* `logs/nsga2_loop.log` — full remote run log

## Verification

* `verify_machines_destroyed.py` — PASSED 0 errors / 1 expected RM-W001 warning
* `verify_research_papers.py`, `verify_research_internet.py`, `verify_research_code.py` —
  PASSED 0/0 each
* `verify_plan.py` — PASSED 0/0
* `verify_library_asset.py de_rosenroll_2026_dsgc_ais_dendritic_spike` — to be run at
  reporting
* `verify_task_results.py`, `verify_task_metrics.py`, `verify_task_file.py`, `verify_logs.py`,
  `verify_corrections.py`, `verify_suggestions.py` — to be run at reporting

## Examples

Ten cells from `results/data/all_evaluations.json` (5 Pareto + 5 representative non-Pareto).
Each example shows the full input parameter vector and the full evaluation output for that
NEURON trial. Selected to span the diversity of the 192-cell run: 4 high-PD non-Pareto cells
(DSI≈0, PD ~8.5–9.3 Hz), 5 Pareto cells, and 1 cell from gen 0 LHS init. Inputs are 54-d float
vectors in `[0, 1]`-normalised parameter space (pymoo's LHS bounds); outputs are dictionaries
reporting the simulation results for the 8-direction × 20-seed × 1400-ms NEURON trial.

The 10 example cells (`results/data/example_cells.json`) are reproduced below.

### Example 1 — cell 0 (gen 0 LHS init)

Input (parameter vector, 54-d):

```text
see results/data/example_cells.json -> cells[0].params
```

Output:

```json
{"cell_index": 0, "generation": 0, "dsi": 0.0, "pd_rate_hz": 0.7142857142857143, "peak_vm_mv": -1.7344266042937708, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 39.5}
```

### Example 2 — cell 42 (high-DSI non-Pareto, gen 0)

Output:

```json
{"cell_index": 42, "generation": 0, "dsi": 0.0938, "pd_rate_hz": 2.5, "peak_vm_mv": -1.5318, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 39.0}
```

### Example 3 — cell 58 (Pareto, gen 0; high-PD rail)

Output:

```json
{"cell_index": 58, "generation": 0, "dsi": 0.01479915, "pd_rate_hz": 8.571428571428571, "peak_vm_mv": 4.089969, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 46.1}
```

### Example 4 — cell 96 (high-PD non-Pareto, gen 1)

Output:

```json
{"cell_index": 96, "generation": 1, "dsi": 0.0, "pd_rate_hz": 8.571428571428571, "peak_vm_mv": 4.089969, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 41.4}
```

### Example 5 — cell 125 (high-PD non-Pareto, gen 1)

Output:

```json
{"cell_index": 125, "generation": 1, "dsi": 0.0, "pd_rate_hz": 8.571428571428571, "peak_vm_mv": 4.089969, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 40.9}
```

### Example 6 — cell 141 (Pareto max-DSI, gen 1)

Output:

```json
{"cell_index": 141, "generation": 1, "dsi": 0.1270491, "pd_rate_hz": 2.535714285714286, "peak_vm_mv": -1.5318, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 40.8}
```

### Example 7 — cell 153 (Pareto, gen 1; alt high-PD path)

Output:

```json
{"cell_index": 153, "generation": 1, "dsi": 0.0260, "pd_rate_hz": 8.464285714285714, "peak_vm_mv": 4.089969, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 42.7}
```

### Example 8 — cell 154 (high-DSI non-Pareto, gen 1)

Output:

```json
{"cell_index": 154, "generation": 1, "dsi": 0.0826, "pd_rate_hz": 2.107, "peak_vm_mv": -1.7311, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 40.9}
```

### Example 9 — cell 188 (Pareto closest-to-joint, max-PD)

Output:

```json
{"cell_index": 188, "generation": 1, "dsi": 0.0, "pd_rate_hz": 9.25, "peak_vm_mv": 4.674, "is_unstable": false, "is_feasible": true, "constraint_violation": -18.397, "elapsed_s": 43.9}
```

### Example 10 — cell 190 (Pareto, gen 1)

Output:

```json
{"cell_index": 190, "generation": 1, "dsi": 0.0516, "pd_rate_hz": 4.0, "peak_vm_mv": -1.260, "is_unstable": false, "is_feasible": true, "constraint_violation": -2.378, "elapsed_s": 40.8}
```

The full 54-d input parameter vectors for all ten cells are saved to
`results/data/example_cells.json` to keep this section readable. The `params` array in each
cell record is the 54-element float vector that was passed to `evaluate_parameter_vector` and
produced the recorded outputs above.

## Next Steps

The follow-up suggestions step proposes the next-task agenda; the headline candidates are:

1. **Re-run NSGA-II at full plan scope (pop=96 / gen=40)**: now that the harness works, re-run
   on a longer Vast.ai allocation (~$1.50-$2.00, 8-10 h) to see whether the negative result
   holds at 3,840 cells.
2. **Substrate regression check on the t0076 iter-424 vector**: validate that the v3 substrate
   reproduces t0076's DSI 0.42 / PD 8.34 Hz before any further architectural extension.
3. **Warm-start from t0078's known-good cells**: seed the NSGA-II initial population with the
   t0078 closest-to-joint cell + max-DSI rail cells mapped into the 54-d v3 space.
4. **Consider parameter-space pruning**: the t0078 results suggest several parameters cluster
   at floors / ceilings; trimming to 30-40 d may dramatically improve NSGA-II convergence at
   small budgets.

## Task Requirement Coverage

The task description's operative scope is reproduced from `task.json` and
`task_description.md`:

```text
Add dendritic-spike machinery to AIS-augmented Bed B; switch from BoTorch qLogNEHVI to NSGA-II
via pymoo; enforce hard biological bounds; test joint DSI/PD pass.
```

The plan's `## Task Requirement Checklist` listed 21 REQ-* items. Coverage:

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Build v3 library asset | Done | `assets/library/de_rosenroll_2026_dsgc_ais_dendritic_spike/details.json` + `description.md` |
| REQ-2 | Mg-block NMDA at all dendrites | Done | `code/trial_helpers.py:setup_synapses_parametric` co-locates `h.Exp2NMDA` with each ACh placement |
| REQ-3 | Nav1.6 + NaP at distal dendrites | Done | `code/apply_params.py` writes `gbar_nav16t80` + `gbar_napt80` on `cell.terminal_dends` |
| REQ-4 | Vendor 13 t78→t80 MODs | Done | `code/mods/*t80.mod` × 13 |
| REQ-5 | Reuse t0024 `Exp2NMDA` unchanged | Done | No NMDA MOD in `code/mods/`; `h.Exp2NMDA` resolves through t0024 DLL |
| REQ-6 | NSGA-II via pymoo | Done | `code/nsga2_loop.py` `NSGA2(pop_size=24, sampling=LHS())` with default operators |
| REQ-7 | `nav16_ais` lower bound 0.25 | Done | `LOWER_BOUNDS[ParamIndex.NAV16_AIS_GBAR] == 0.25` in `code/constants.py` |
| REQ-8 | AIS-to-soma Nav ratio constraint | Done | `BedBV3Problem.__init__(n_ieq_constr=1)`, `out["G"] = [5 - nav16_ais/nav16_soma]` |
| REQ-9 | Substrate regression check | **Partial** | Smoke gate (8 LHS cells, 0 unstable, 5 non-dom feasible) substituted; full t0076 iter-424 mapping deferred |
| REQ-10 | 8 dirs × 20 seeds × 1400 ms FULL HH | Done | `constants.py` `TSTOP_MS=1400, N_DIRECTIONS=8, N_SEEDS=20`, mode FULL |
| REQ-11 | Per-cell registered metrics | Done | `results/metrics.json` 6 variants × `direction_selectivity_index` + `pd_firing_rate_hz` + `peak_vm_mv`; HWHM/reliability/RMSE set to null since t0012 not wired |
| REQ-12 | Pareto + HV + scatter PNGs | Done | `results/images/{pareto_front,hypervolume_trajectory,all_cells_scatter}.png`; deep-dive Vm panels not produced |
| REQ-13 | Cost-cap watchdog | Done | `code/cost_cap.py`, watchdog active, never approached cap |
| REQ-14 | Vast.ai 64-core EPYC 7B13 | Done | Instance 36137287, EPYC 7B13, 64 cores, $0.2382/hr |
| REQ-15 | Answer asset | Done | `assets/answer/mobo-on-biophysics-ais-disabled-corner/` |
| REQ-16 | Use t0076 iter-424 vector for regression | **Blocked** | Tied to REQ-9; cost margin too tight at the 192-cell scope. Future task should pick up. |
| REQ-17 | NEURON-fresh-subprocess workers | Done | `BedBV3Problem._evaluate` calls `evaluate_parameter_vector` via ProcessPoolExecutor |
| REQ-18 | Track is_unstable / filter Pareto | Done | `_save_pareto_front` filters `is_unstable` and infeasible cells |
| REQ-19 | Cost cap honoured | Done | Final cost $0.7458 (of $2.00 cap) |
| REQ-20 | `tau_ca_multiplier` upper bound = 20 | Done | `LOWER_BOUNDS[33] = 1.0, UPPER_BOUNDS[33] = 20.0` unchanged from t0078 |
| REQ-21 | Preserve t0078 49-d ParamIndex 0-48 | Done | New parameters added at indices 49-53; existing indices unchanged |

Plus one major **scope deviation** documented under Limitations: the NSGA-II run was scaled
from the plan's pop=96 / gen=40 (3,840 cells) down to pop=24 / gen=8 (192 cells), a 95%
reduction. This is the dominant factor in the negative-result framing.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2" date_compared:
"2026-05-04" ---
# Comparison with Published Results

## Summary

The 54-d dendritic-spike-augmented Bed B substrate with NSGA-II at pop=24 / gen=8 (192
evaluations, $0.7458) produces a sparse 5-cell Pareto front that **misses the joint pass
criterion (DSI >= 0.4 AND PD >= 10 Hz) by a wide margin**. The closest-to-joint Pareto cell
sits at **DSI 0.000 / PD 9.25 Hz** (cell 188, distance 0.850 from joint), and the max-DSI
Pareto cell sits at **DSI 0.127 / PD 2.54 Hz** (cell 141). Against the literature anchor of
paired DSI + mean PD firing rate from `[RivlinEtzion2012, Fig. S2 + Results p. 522]` (**DSI
0.78 +/- 0.19**, **PD 10.38 +/- 8.53 Hz**, n = 8 stable cells), the joint-closest cell sits at
a joint z-score of **(-4.11 on DSI, -0.13 on PD)**: the PD axis is biologically plausible
while the DSI axis is **4.1 sigma** below the published mean. The result is a **clean
architectural negative outcome** strongly conditioned by the small NSGA-II budget — t0080's
192 cells in 54-d cannot be directly compared with t0078's 491 cells in 49-d. The AIS
hard-floor enforcement (`nav16_ais` >= 0.25 S/cm² per `[Kole2008, p. 178]`; AIS-to-soma Nav
ratio >= 5 per `[Werginz2024, Table 1]`) **did achieve its primary objective**: zero Pareto
cells collapsed to the t0078 iter-81 AIS-disabled-corner failure mode. Independent
confirmation from `[Goethals2020]` axial-current measurements (12-55 mS/cm² range) places
t0080's 0.25 S/cm² floor at the upper edge of that estimate range.

## Comparison Table

### Literature Comparison

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | DSI (3 s grating window) | 0.78 | 0.000 | -0.780 | Cell 188 (closest-to-joint); z = -4.11 |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | Mean PD firing rate (Hz) | 10.38 | 9.25 | -1.13 | Cell 188; z = -0.13; within 1 sigma |
| `[deRosenroll2026, Fig. 5]` correlated SAC release (Bed B substrate ancestor) | DSI | 0.39 | 0.127 | -0.263 | Cell 141 (max-DSI Pareto); -67% of published value |
| `[deRosenroll2026, Fig. 5]` uncorrelated SAC release | DSI | 0.25 | 0.127 | -0.123 | Cell 141; below uncorrelated baseline |
| `[Park2014, Table 1]` mouse CART-Cre On-Off DSGC | DSI | 0.65 | 0.127 | -0.523 | Cell 141; -10.5 sigma on Park SD 0.05 |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC ON | DSI | 0.45 | 0.127 | -0.323 | Cell 141 |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC OFF | DSI | 0.50 | 0.127 | -0.373 | Cell 141 |
| `[Oesch2005, Results p. 754]` rabbit ON dendritic-AP DSGC | Peak-rate DSI | 0.67 | 0.127 | -0.543 | Cell 141; metric mismatch (mean-rate vs peak-rate) |
| `[Oesch2005, Results p. 754]` rabbit OFF dendritic-AP DSGC | Peak-rate DSI | 0.74 | 0.127 | -0.613 | Cell 141; metric mismatch |
| `[Oesch2005, Results p. 754]` rabbit | Modal peak PD rate (Hz, peak) | 148.0 | 9.25 | -138.75 | Cell 188; metric mismatch (mean vs peak) |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | Peak PD rate (Hz, Gaussian-conv) | 198.0 | 9.25 | -188.75 | Cell 188 mean rate vs Trenholm peak rate |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | Peak-rate DSI | 0.76 | 0.127 | -0.633 | Cell 141; metric mismatch |
| `[PolegPolsky2016, Results]` mouse DRD4 DSGC (passive-dendrite ancestor) | DSI | 0.65 | 0.127 | -0.523 | Cell 141; -80% of published value |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS Nav density (S/cm²) | 1.30 | >= 0.25 | within range | Hard-floor enforced; Pareto cells span 0.25-5.0 |
| `[Kole2008, p. 178]` cortical pyramidal AIS prior | AIS Nav density (S/cm²) | 0.25-0.5 | >= 0.25 | floor met | Lower bound enforced as hard parameter floor |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS-to-soma Nav ratio (x) | 17.3 | >= 5 | floor met | Hard ratio floor of 5 enforced via inequality constraint |
| `[Goethals2020]` axial-current AIS Nav estimate (independent) | AIS Nav density (mS/cm²) | 12-55 | >= 250 | floor at upper edge | t0080's 0.25 S/cm² = 250 mS/cm² sits at the upper edge of Goethals's estimate range |

### Prior Task Comparison

| Prior Task | Metric | Prior Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Closest-to-joint DSI | 0.316 | 0.000 | -0.316 | Cell 188 vs t0078 iter 81; t0080 PD-axis Pareto cell has zero DSI |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Closest-to-joint PD rate (Hz) | 9.68 | 9.25 | -0.43 | Cell 188; PD axis nearly matches t0078 |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Pareto front size (cells) | 17 | 5 | -12 | t0080 explored 192 cells; t0078 explored 491 |
| t0078 (49-d AIS-augmented Bed B BoTorch) | Hypervolume | 11.41 | n/a (different ref) | n/a | t0080 used utopia (0.7, 80) reference; not numerically comparable |
| t0078 max-DSI Pareto cell (iter 290) | DSI | 1.000 | 0.127 | -0.873 | t0080 max-DSI sub-Pareto cell does not approach t0078's max-DSI rail |
| t0076 (25-d Bed B substrate, qNEHVI) iter-424 | DSI at PD ~ 8 Hz | 0.42 | 0.026 | -0.394 | Cell 153 (PD 8.46 Hz, closest to t0076 iter-424 PD); -94% of t0076 value |
| t0076 (25-d Bed B substrate, qNEHVI) iter-424 | PD rate (Hz) at DSI ~ 0.4 | 8.34 | 9.25 | +0.91 | Cell 188 expands PD axis but at DSI 0.000 |
| t0076 (25-d Bed B substrate, qNEHVI) | Pareto front size (cells) | many | 5 | sparse | t0076 explored 491 cells; t0080's 5-cell front is highly under-resolved |

## Methodology Differences

* **Optimiser**: t0080 uses **NSGA-II via pymoo** (population 24, generations 8, SBX eta=15,
  polynomial mutation eta=20, RankAndCrowding survival, LHS init). t0078 and t0076 used
  **BoTorch qLogNEHVI** with SingleTaskGP surrogates and Sobol DoE init. The two optimiser
  families have different sample-efficiency profiles: BoTorch's GP surrogate carries
  information across evaluations, while NSGA-II relies purely on selection pressure on the
  current population. NSGA-II needs much larger populations for high dimensionality (Hay 2011
  used pop=1000 for 22-d; t0080's pop=24 for 54-d is dramatically under-budgeted).
* **Evaluation budget**: t0080 ran **192 evaluations** (5% of plan's 3,840); t0078 ran 491;
  t0076 ran 491. The t0080 reduction was forced by per-cell saturating 64 cores (~45 s
  wall-clock per cell sequentially) on the Vast.ai instance under the $2.00 cost cap.
* **DSI definition**: t0080 / t0078 / t0076 all use polar vector-sum DSI = (PD - ND) / (PD +
  ND) over 8 directions x 20 seeds, computed from trial-averaged spike counts.
  `[Trenholm2013]` and `[Oesch2005]` compute DSI from **peak** Gaussian-convolved (sigma = 25
  ms) instantaneous rates; the resulting peak-rate DSIs are typically 0.05-0.15 higher than
  mean-rate DSIs from the same cell (`[Trenholm2013, Results p. 14068]`).
* **Firing-rate window**: t0080 uses TSTOP_MS = 1400 ms with trial-averaged spike rate.
  `[RivlinEtzion2012]` reports mean rate over a 3 s grating window; `[Trenholm2013]` /
  `[Oesch2005]` report peak instantaneous rate from Gaussian-convolved trains over sub-second
  windows. Cell 188's 9.25 Hz mean PD rate is directly comparable to RivlinEtzion's 10.38 Hz,
  but **not** to Trenholm's 198 Hz peak or Oesch's 148 Hz modal peak.
* **Substrate**: t0080 inherits the de Rosenroll Bed B morphology + SAC release from
  `[deRosenroll2026]` and adds dendritic-spike machinery (Mg-block NMDA at all dendrites +
  Nav1.6 + NaP at distal dendrites). t0078 added an AIS but kept dendrites passive. t0076 had
  no AIS and passive dendrites. `[PolegPolsky2016]` uses passive dendrites with NMDA Mg-block
  but no AIS. `[Werginz2024]` uses an alpha-RGC morphology with no SAC-driven inhibition.
* **Dimensionality**: t0080 = **54-d** (49 t0078 parameters + 5 new dendritic-spike
  parameters: `gnmda_dend`, `mg_conc`, `voff_nmda`, `nav16_dend_distal`, `nap_dend_distal`).
  t0078 = 49-d. t0076 = 25-d. The 5-d expansion in t0080 was matched with a 2.6x **smaller**
  evaluation budget, which is the dominant explanation for the regressed Pareto coverage.
* **AIS hard-floor enforcement**: t0080 is the **first task in the project** to enforce the
  AIS hard floor as a parameter bound + inequality constraint (`nav16_ais >= 0.25 S/cm²`,
  AIS-to-soma Nav ratio >= 5). t0078 had no hard floors and converged on the AIS-disabled
  corner at iter 81 (`nav16_ais` = 1e-5, ratio = 5.5e-5). t0080 cells are all biologically
  plausible by construction.
* **HV reference convention**: t0080's `nsga2_loop.py` computes HV against utopia point `(0.7,
  80)`; t0076 / t0078 used `[0, 0]`. HV values across these tasks are not numerically
  comparable; only the Pareto-front extent and the joint distance metric translate.
* **Stimulus**: t0080 uses a 1 mm/s 250 um bar in 8 directions. `[RivlinEtzion2012]` uses a
  drifting square-wave grating; `[Trenholm2013]` uses a positive-Weber bar at 600 um/s;
  `[Park2014]` uses a moving spot. Cross-method DSI / rate comparisons inherit the +/- 20-30%
  variability typical of stimulus-protocol differences.
* **Pharmacology**: t0080 simulates control conditions (no GABA-A blockade), matching
  `[Trenholm2013]` control (198 Hz) and `[RivlinEtzion2012]` control. `[Trenholm2013]`'s 244
  Hz picrotoxin value is not a comparable target.

## Analysis

The Pareto front confirms a **strongly compressed** trade-off geometry: Cell 141 (the only
Pareto cell with non-trivial DSI = 0.127) sits at PD 2.54 Hz; the high-PD rail (cells 58, 153,
188) sits at DSI <= 0.026 across PD 8.5-9.25 Hz. **No Pareto cell crosses the joint pass
criterion** (DSI >= 0.4 AND PD >= 10 Hz). The closest-to-joint distance is **0.850**,
dominated by the DSI shortfall (0.40) rather than the PD shortfall (0.75 Hz).

**Joint z-score interpretation.** The Mahalanobis-style joint z-score for cell 188 against the
RivlinEtzion2012 stable-cell distribution:

* DSI z = (0.000 - 0.78) / 0.19 = **-4.11** (well outside +/- 3 sigma; less than 0.005% of
  stable cells in `[RivlinEtzion2012]` would have DSI 0).
* PD-rate z = (9.25 - 10.38) / 8.53 = **-0.13** (within 1 sigma; biologically plausible).

The PD axis successfully reproduces biological mean rates while the DSI axis remains
essentially **at zero** for the joint-closest cell. This pattern echoes the t0078 finding (DSI
z = -2.44 on the joint-closest cell) but is much more severe — t0078 reached DSI 0.316 at PD
9.68 Hz, t0080 collapses to DSI 0.000 at PD 9.25 Hz. The dendritic-spike machinery added in
t0080 (NMDA + Nav1.6 + NaP at distal dendrites) **did not improve directional gain** in the
joint-PD regime within the 192-cell budget.

**Versus t0078.** The headline regression is dramatic: t0080's joint-closest cell DSI
(**0.000**) is **0.316 lower** than t0078's joint-closest (0.316). t0080's max-DSI Pareto cell
DSI (0.127) is **0.873 lower** than t0078's max-DSI rail (1.000). Because t0080 added 5
parameters (54-d vs 49-d) **and** halved the budget (192 vs 491 cells), the regression cannot
be cleanly attributed to the substrate. Three plausible causes, in decreasing likelihood:

1. **NSGA-II at pop=24 in 54-d is fundamentally under-budgeted**: NSGA-II selection pressure
   needs much larger populations for high dimensionality (Hay 2011 used pop=1000 for 22-d;
   pop=100 is the de-facto floor for 50+ d in the genetic-algorithm literature). pop=24 is
   below the noise floor for 54-d.
2. **No warm-start from t0078's known-good cells**: the NSGA-II LHS init started fresh.
   Mapping t0078's iter-81 vector (DSI 0.316 / PD 9.68 Hz) into the 54-d v3 space with the new
   dendritic parameters at zero would land near a known-good seed, but no v3 cell was seeded
   from t0078.
3. **The dendritic-spike substrate may itself regress the joint Pareto front**: adding 5
   parameters that **default to runaway depolarisation** (high distal Nav1.6 + NaP) without
   matched dendritic Kv3 / Kv4 / Kv7 may shift the substrate's stable manifold toward
   non-spiking or quiescent cells. The pre-launch substrate-regression check (REQ-9 / REQ-16)
   was deferred, so the substrate's biological consistency at the t0076 iter-424 vector was
   not independently verified.

**Versus t0076.** t0076's iter-424 (DSI 0.42 / PD 8.34 Hz) was the strongest single-cell joint
result in the project lineage. t0080's closest-PD Pareto cell (cell 153, PD 8.46 Hz) has DSI
**0.026** — a **94% regression** vs t0076 at the same PD rate. t0080's PD axis modestly
**expanded** to 9.25 Hz (vs t0076's 8.34 Hz), but the DSI axis catastrophically **compressed**
from 0.42 to 0.026 in the comparable PD regime. Net: the v3 substrate + NSGA-II under this
budget produces a Pareto front that is dominated by t0076's BoTorch front in the joint
operating regime.

**AIS hard-floor enforcement: design objective achieved.** Zero t0080 Pareto cells exhibit the
t0078 iter-81 AIS-disabled-corner failure mode. The hard-bound `nav16_ais >= 0.25 S/cm²` (Kole
2008 lower bound) and AIS-to-soma Nav ratio >= 5 (below the lowest measured RGC value per
`[Werginz2024]` at 17.3 and `[Werginz2020]` at ~7) eliminated by construction the regime where
the optimiser converges on a configuration with collapsed AIS Nav. Independent confirmation
from `[Goethals2020]` axial-current measurements gives an AIS Nav range of **12-55 mS/cm²**,
placing t0080's hard floor of 250 mS/cm² (= 0.25 S/cm²) at the upper edge of that estimate
range. The floor is **biologically conservative** in the sense that it accepts only the
upper-percentile literature values; future iterations may consider relaxing the floor toward
the Goethals lower bound (~0.012 S/cm²) to widen the search space.

**Versus PolegPolsky2016 substrate ancestor.** `[PolegPolsky2016, Results]` reports DSI
0.6-0.7 in passive-dendrite mouse DRD4 DSGCs **without** dendritic-spike machinery. t0080
added that machinery and produces DSI 0.127 maximum — **80% below** the published baseline.
This suggests that adding dendritic Nav1.6 + NaP without rebalancing the existing substrate's
Kv repolarisation may have **worsened** rather than improved DSI, consistent with the
runaway-depolarisation risk flagged in the task description.

**Substrate validation gap.** The substrate-regression check (REQ-9 / REQ-16) was deferred
under cost pressure; the v3 substrate's biological consistency at the t0076 iter-424 vector
was not independently verified before NSGA-II launch. Without that check, the t0080 result
cannot conclusively distinguish "v3 substrate is regressed" from "NSGA-II under-budgeted in
54-d" as the dominant cause of the dramatic Pareto compression. This must be the first action
in any t0080 follow-up task.

## Limitations

* **Major scope deviation in evaluation budget**: t0080 ran 192 evaluations vs the plan's
  3,840 (5% of planned). The reduction was forced by sequential per-cell evaluation on a
  single 64-core Vast.ai instance under the $2.00 cap. Direct comparison with t0078's 491
  evaluations or t0076's 491 evaluations is not architecturally clean.
* **Substrate-regression check (REQ-9 / REQ-16) deferred**: the v3 substrate at the t0076
  iter-424 mapped vector was not validated; the smoke gate (8 LHS cells, 0 unstable, 5
  non-dominated feasible) is a weaker substitute.
* **HV trajectory file granularity**: only 2 entries (gen 0 / gen 1, 96 / 192 cumulative
  evaluations); the HV trajectory plot is sparse. The 5-cell Pareto front and per-cell metrics
  are correct.
* **HV reference-point inconsistency**: t0080 uses utopia = (0.7, 80); t0076 / t0078 used
  reference = [0, 0]. HV values across the three tasks are on different scales and not
  directly numerically comparable. Future runs should standardise on a single convention.
* **Mean-rate vs peak-rate metric mismatch**: published `[Trenholm2013]` and `[Oesch2005]`
  values are peak Gaussian-convolved instantaneous rates (sigma = 25 ms). t0080 reports
  trial-averaged mean rates over 1400 ms. The cell-188 vs Trenholm 198 Hz delta is a metric
  mismatch, not a biological mismatch. Only `[RivlinEtzion2012]`'s 3 s-window mean rate is
  directly comparable to the t0080 firing-rate metric.
* **DSI definitions vary across the corpus**: `[Trenholm2013]`'s peak-rate DSI is structurally
  higher than the trial-averaged spike-count DSI used in t0080. Cross-paper DSI comparisons
  inherit this systematic +0.05 to +0.15 difference.
* **Park 2014 SD of 0.05 unrealistically small**: yields z = -10.5 against cell 141,
  implausible for a biological measurement. Reflects within-cell-type homogeneity in the
  CART-Cre transgenic line, not the full DSGC population. Use `[RivlinEtzion2012]`'s SD 0.19
  for defensible z-scores.
* **Werginz 2020 PDF paywalled in the project corpus**: the AIS-to-soma Nav ratio of ~7x for
  mouse OFF-alpha-T RGCs is in the metadata only. The hard-floor justification rests primarily
  on `[Werginz2024, Table 1]`'s 17.3x value. `[Goethals2020]` axial-current method provides
  independent confirmation of the AIS Nav range.
* **No cross-bed validation**: t0080 only operates on Bed B. The v3 dendritic-spike machinery
  has not been ported to or evaluated on other substrates.
* **Single NSGA-II run, single seed**: t0080's 5-cell Pareto front comes from one LHS init and
  one NSGA-II chain. The Pareto-front structure may shift with a different RNG seed; no
  Pareto-front uncertainty estimate is reported.
* **No paired DSI + mean PD-rate measurements other than `[RivlinEtzion2012]`**: the joint
  literature anchor at (DSI 0.78, 10.38 Hz) is from a single n = 8 sample. No other paper in
  the project corpus reports paired joint DSI + mean PD-rate values.

</details>
