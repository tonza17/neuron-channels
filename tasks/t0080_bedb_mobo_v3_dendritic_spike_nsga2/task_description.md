# Bed B v3 MOBO with Dendritic-Spike Machinery and NSGA-II

## Motivation

t0078 (49-d Bed B v2 BoTorch qLogNEHVI MOBO with AIS, tier-stratified channels, and slow Kv-AHP)
expanded the achievable Pareto front by **+36% in hypervolume** over t0076 (8.41 -> 11.41) but still
missed the joint pass criterion `DSI >= 0.4 AND PD rate >= 10 Hz`. The closest cell (iter 81) sits
at DSI 0.316 / PD 9.68 Hz, short by 0.084 on DSI and 0.32 Hz on PD rate. The compare-literature
analysis identified two follow-on diagnostics:

1. **Passive dendrites are the bottleneck on the high-DSI rail.** The PD ceiling pinned at 2.86 Hz
   across 109 acquisitions despite continuous optimiser exploration -- the signature of a saturated
   negative-feedback loop. Published mouse DSGC DSI > 0.4 is computed at peak rates after Gaussian
   convolution (Trenholm 2013) and / or relies on active dendritic Nav (Sivyer 2013) and dendritic
   spike initiation (Oesch 2005). The augmented substrate added an AIS but kept dendrites passive;
   the missing dendritic-spike machinery is the dominant explanation for the compressed high-rail
   DSI.

2. **MOBO-on-biophysics failure mode at iter 81.** `nav16_ais` collapsed to the search-space floor
   (1e-5 S/cm^2), four orders below Kole 2008's [0.25, 0.5] S/cm^2 prior and five orders below
   Werginz 2024's measured mouse alpha-RGC AIS Nav of 1.3 S/cm^2. The AIS-to-soma Nav ratio at iter
   81 was 5.5e-5 vs Werginz 2024's measured 17.3. The optimiser converged on a configuration where
   the AIS contributes nothing to spike initiation -- contradicting REQ-2 / REQ-3 / REQ-4's
   biological intent. This is a generalisable MOBO-on-biophysics failure mode.

Additionally, t0078 hit O(N^3) Cholesky scaling in BoTorch SingleTaskGP: per-cell wall-clock grew
from 28 s in early phase to 9-12 min after acq 480, forcing early stop at acq 416 / 700 and a final
cost of $3.93 over 24.86 h on a Vast.ai 64-core CPU instance.

This task addresses all three issues in a single bundled run: (a) add dendritic-spike machinery, (b)
switch optimiser from BoTorch qLogNEHVI to NSGA-II via pymoo to eliminate the O(N^3) blow-up, (c)
enforce biological hard lower bounds so the optimiser cannot exploit the AIS-disabled corner.

This task directly addresses project research question **Q4** (do active dendritic voltage-gated
conductances improve, degrade, or have no effect on the match to the target angle-frequency curve
compared with passive dendrites?) on the Bed B substrate, and provides a methodological control for
**Q1** (which combinations of somatic Na/K conductances maximise AP frequency at PD while
suppressing firing at ND?).

Source suggestion: **S-0078-01**.

## Scope

### In scope

* Build a new library asset extending the t0078 `de_rosenroll_2026_dsgc_ais` substrate with
  dendritic-spike machinery: Mg-block NMDA at active densities on dendrites (Exp2NMDA with
  voltage-dependent Mg block bound into the bipolar -> DSGC excitatory channel) and Nav1.6 + NaP at
  distal-dendrite densities sufficient for back-propagating APs and dendritic spikes per Sivyer 2013
  / Oesch 2005 priors.
* Replace the BoTorch qLogNEHVI optimiser with NSGA-II via pymoo
  (`pymoo.algorithms.moo.nsga2.NSGA2`). Configuration: pop 96, 40 generations (3,840 evaluations),
  SBX crossover eta=15, polynomial mutation eta=20, tournament selection, Latin Hypercube Sampling
  or Sobol initial population.
* Enforce hard biological lower bounds on AIS-related parameters:
  * `nav16_ais` >= 0.25 S/cm^2 (Kole 2008 cortical pyramidal patch-clamp prior; lower bound of the
    Kole [0.25, 0.5] range)
  * AIS-to-soma Nav ratio >= 5 (Werginz 2024 mouse alpha-RGC; biologically plausible lower bound,
    well below the measured 17.3)
* Pre-run substrate regression check (folded in from S-0078-02): re-evaluate the t0076 iter-424
  parameter vector (DSI 0.42 / PD 8.34 Hz) on the v3 49-d substrate as a one-shot validation cell
  before launching the NSGA-II loop. Document the substrate-regression delta.
* Produce one answer asset (folded in from S-0078-08) documenting the AIS-disabled-corner failure
  mode observed at t0078 iter 81 and the biological-prior checklist now enforced as hard MOBO
  bounds. The answer asset should include: the iter-81 example as the canonical case; an audit of
  t0076 + t0078 Pareto fronts for similar collapse-to-floor patterns on biologically-priored
  parameters; the now-enforced biological-prior checklist (Kole 2008 / Werginz 2024); general
  guidance for future MOBO-on-biophysics tasks.

### Out of scope

* `tau_ca_multiplier` upper bound stays at 20x (S-0078-03 NOT folded in per researcher decision;
  keeps the slow-AHP substrate identical to t0078 for cleaner architectural-delta comparison).
* Single-objective scalarised BO comparison (S-0078-04 -- separate methodological task).
* Multi-replicate Sobol seed and BO chain replication for HV uncertainty (S-0078-06 -- separate
  evaluation task).
* Promotion of the t0080 NSGA-II harness into a substrate-agnostic library (deferred until at least
  one more substrate uses it).

## Approach

### Substrate v3

Extend the t0078 `de_rosenroll_2026_dsgc_ais` library (the AIS-augmented Bed B from t0078) with:

1. **Mg-block NMDA on dendrites**: Add Exp2NMDA point process with voltage-dependent Mg block to the
   bipolar -> DSGC excitatory drive at all dendritic compartments (proximal, mid, terminal).
   Conductance and `Mg2+` concentration become free MOBO parameters (~3 new parameters:
   `gnmda_dend`, `mg_conc`, optionally `voff_nmda`).
2. **Nav1.6 + NaP at distal-dendrite densities**: Insert Nav1.6 (already SUFFIX-defined in t0078)
   into the distal-dendrite tier at densities sufficient for back-propagating APs. Insert a NaP
   SUFFIX into the distal-dendrite tier. Density bounds informed by Sivyer 2013 (rabbit DSGC
   dendritic spike thresholds) and Oesch 2005 (rabbit ON DSGC peak-rate DSI 0.67 ON / 0.74 OFF
   correlated with dendritic spike initiation).

The v3 substrate retains all 49 t0078 MOBO parameters plus ~5-7 new dendritic-spike parameters.
Estimated total dimensionality: **54-56 d**.

### Optimiser: NSGA-II via pymoo

* Algorithm: `pymoo.algorithms.moo.nsga2.NSGA2`
* Population size: 96
* Generations: 40
* Total evaluations: 3,840 cells (each cell = 8 directions x 20 seeds x 1400 ms = 160 NEURON
  simulations)
* Crossover: SBX (`SimulatedBinaryCrossover`) with eta=15 (moderate exploration)
* Mutation: Polynomial mutation (`PolynomialMutation`) with eta=20
* Selection: Tournament selection
* Initial population: Latin Hypercube Sampling (LHS) for spread; falls back to Sobol if LHS is not
  available in pymoo's sampling module
* Reference point for hypervolume: `[0, 0]` (matches t0076 / t0078)
* Hard bounds enforced as parameter bounds (no penalty terms, no log-priors) -- pymoo's bound
  handling guarantees no individual ever has `nav16_ais` < 0.25 or AIS-to-soma Nav ratio < 5

### Pre-run substrate regression check (S-0078-02 folded in)

Before launching the NSGA-II loop:

1. Map the t0076 iter-424 parameter vector to the v3 49-d parameterisation (tier-stratified channels
   at uniform t0076-matching values; AIS Nav at Kole prior centre 0.375 S/cm^2; AIS geometry at
   midpoint; `tau_ca_multiplier=1`). Set the new dendritic-spike parameters at their lower bounds (0
   dendritic NMDA, 0 distal Nav1.6 / NaP) so the regression check is at the architectural baseline
   equivalent to t0076's substrate.
2. Run `_worker_run_trial` once on local CPU (or as the first NSGA-II eval) and report DSI / PD
   rate.
3. Document the substrate-regression delta in `results/results_summary.md`. Pass: reproduce DSI
   within +/- 0.05 of t0076's 0.42 at PD ~ 8.34 Hz, or document a clean substrate regression.

### NEURON re-init bug carry-over

t0078 documented an `Exp2NMDA name already exists` error when re-initialising NEURON inside the same
Python process. The fix from t0078 (subprocess-per-deep-dive) is carried into t0080 via
ProcessPoolExecutor with NEURON-fresh-subprocess workers.

### Compute

* Vast.ai 64-core CPU instance (target same EPYC 7B13 64-core class as t0078 instance 36068067 at
  $0.1582/hr if available; equivalent if not)
* Estimated wall-clock: 3,840 cells x ~50 s/cell = 192,000 s = 53.3 CPU-hours. With 64 effective
  cores in parallel, ~0.83 wall-hours.
* Cost target: $0.13-$0.20 raw + setup overhead = **$1.00-$1.50** total
* **Hard cap: $2.00**. Beyond this, kill the run and document with a clean cost-of-progress
  decision.

## Pass criterion

Locate at least one Pareto cell with **DSI >= 0.4 AND PD rate >= 10 Hz** anchored to RivlinEtzion
2012 stable-cell joint distribution (DSI 0.78 +/- 0.19, PD 10.38 +/- 8.53 Hz, n = 8), OR rule it out
architecturally with a clean negative result documented against the t0078 +36% HV improvement and
the substrate-regression delta. Either outcome is a strong project result:

* **Positive**: dendritic-spike-augmented Bed B v3 becomes the project's standard substrate for
  further joint-optimisation work; the answer asset documents the biological-prior checklist as a
  transferable methodology.
* **Negative**: the trade-off is intrinsic to the de Rosenroll Bed B substrate's morphology or
  SAC-release machinery; the project pivots to alternative dendritic mechanisms (Ca^2+ plateau zones
  per Larkum / Branco-Hausser; Ih / HCN conductances) or substrate redesign.

## Expected assets

* **1 library asset**: `de_rosenroll_2026_dsgc_ais_dendritic_spike` (or similar) -- the v3 substrate
  with active dendritic NMDA + Nav1.6 / NaP.
* **1 answer asset**: AIS-disabled-corner MOBO-on-biophysics failure mode write-up with the enforced
  biological-prior checklist.

`expected_assets`: `{"library": 1, "answer": 1}`.

## Outputs

* `results/results_summary.md` (Summary, Methodology, Metrics, Verification, Next Steps -- all with
  the pass-criterion verdict prominently stated)
* `results/results_detailed.md` with embedded Pareto-front PNG, hypervolume-trajectory PNG, and
  per-direction Vm-trace PNGs for the closest-to-joint cell, the max-DSI cell, and the max-PD cell
* `results/metrics.json` reporting the final hypervolume, the pass-criterion-closest cell's DSI and
  PD rate, the substrate regression delta, and the new dendritic-spike parameters' Pareto values
* `results/suggestions.json` with downstream suggestions
* `results/costs.json` with the final Vast.ai cost
* `results/remote_machines_used.json` with the Vast.ai instance metadata
* `results/compare_literature.md` updating the t0078 literature anchors against the v3 results
* `results/images/pareto_front.png`, `images/hypervolume_trajectory.png`, three deep-dive Vm PNGs

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` -- the upstream Bed B substrate
* `t0069_t0067_ais_localised_channel_sweep` -- the Bed A AIS architecture reference for cross-bed
  AIS-construction patterns
* `t0076_bedb_dsi_firing_rate_mobo` -- the BoTorch BO harness baseline that t0078 extended (still
  useful for ParameterSpec scaffolding even though the optimiser changes)
* `t0078_bedb_mobo_v2_ais_tiered_ahp` -- the AIS-augmented 49-d substrate library that t0080 extends
  with dendritic-spike machinery

## Risks and fallbacks

* **NSGA-II fails to match t0078's HV 11.41**: itself a useful methodological finding; document as a
  clean comparison and decide whether to switch back to BO with a smaller acquisition budget. Do not
  block on this.
* **Vast.ai 64-core CPU unavailable**: fall back to 36-core or 72-core instances at the same CPU
  class (EPYC 7B13 family) and re-estimate cost. The NSGA-II scaling is linear in cores, so a
  36-core instance roughly doubles wall-clock (still within the cost cap at $0.10/hr rates).
* **Substrate regression check fails**: documents a t0078 substrate regression but is not a blocker
  for the NSGA-II run; the result is a useful note for t0080's results.
* **Cost cap hit before convergence**: kill the run cleanly; report the partial Pareto front and the
  cost-of-progress decision in `results/results_summary.md`. Do not extend the cap beyond $2.00
  without a brainstorm consult.
* **Dendritic-spike machinery destabilises the substrate (runaway depolarisation)**: detect during
  the substrate regression check; tighten Nav1.6 / NaP upper bounds before launching NSGA-II.

## Verification criteria

* Library asset passes `verify_library_asset.py` with 0 errors.
* Answer asset passes the answer-asset verificator with 0 errors.
* Task results pass `verify_task_results.py` with 0 errors.
* Task metrics pass `verify_task_metrics.py` with 0 errors.
* Vast.ai instance destroyed cleanly per `verify_machines_destroyed.py`.
* `verify_pr_premerge.py` passes with 0 errors before merge.
* Cost is at or below the $2.00 hard cap.
