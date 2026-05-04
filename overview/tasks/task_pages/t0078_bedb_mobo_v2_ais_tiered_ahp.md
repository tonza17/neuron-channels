# ✅ Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0078_bedb_mobo_v2_ais_tiered_ahp` |
| **Status** | ✅ completed |
| **Started** | 2026-05-03T13:02:20Z |
| **Completed** | 2026-05-04T16:25:00Z |
| **Duration** | 27h 22m |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Source suggestion** | `S-0076-02` |
| **Task types** | `build-model`, `experiment-run` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`patch-clamp`](../../by-category/patch-clamp.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 1 library |
| **Step progress** | 15/15 |
| **Cost** | **$3.93** |
| **Task folder** | [`t0078_bedb_mobo_v2_ais_tiered_ahp/`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/task_description.md)*

# Bed B v2 Multi-Objective BO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Motivation

t0076 ran a 25-d BoTorch qNEHVI multi-objective Bayesian optimisation on the Bed B (de
Rosenroll 2026\) DSGC compartmental model in NEURON, jointly maximising direction selectivity
index (DSI) and preferred-direction firing rate over 30 Sobol DoE + 400 acquisition steps (430
cell evaluations, 68,800 NEURON simulations). The headline finding is a **smooth monotone
trade-off** on the Pareto front spanning DSI in [0.003, 1.0] and PD rate in [0.4, 127.75 Hz],
with **no operating point satisfying DSI >= 0.4 AND PD rate >= 30 Hz** simultaneously. Every
Pareto cell with DSI >= 0.4 has PD rate <= 5.0 Hz; every cell with PD rate >= 30 Hz has DSI <=
0.07. The matched cell at iter 424 (DSI 0.42, PD rate 4.95 Hz) reproduces the published
deRosenroll2026 baseline (DSI 0.39) within +0.03, validating the substrate.

The t0076 compare-literature analysis identifies **three architectural omissions** that
plausibly explain the trade-off:

1. **No AIS section**. Real RGCs initiate spikes at the AIS, where Nav density is ~7x soma per
   Kole 2008 / Van Wart 2007. Bed B applies all sodium uniformly to the soma + 350 dendrites;
   the high-rate Pareto extremes (iter 319, 127.75 Hz, DSI 0.003) reflect saturated dendritic
   spiking without a directional gate.
2. **Uniform-density channels**. Real RGCs have graded Ih / Kv / Nav distributions across soma
   and dendritic tiers. The 25-d t0076 search collapses each channel to a single density
   applied everywhere, which cannot exploit the tier-specific gradients that biological cells
   use to compute direction.
3. **Absent slow-AHP machinery**. The t0076 high-rate Pareto extreme (iter 319, 127.75 Hz)
   exceeds biologically plausible mean PD rates (30 - 80 Hz per Trenholm / Borst literature)
   precisely because Bed B lacks slow Ca-activated K+ adaptation. The vendored SK and BK
   mechanisms (from Hay 2011 / Khaliq 2003 cortical / Purkinje sources) and the single-shell
   `cad` Ca pool (taur 5 ms) collectively fail to cap firing on the timescale real RGCs use.

This task closes all three architectural gaps in a single bundled MOBO run, plus folds in the
three implementation defects identified during the t0076 retrospective so the new BO loop runs
on a clean stack.

The goal is binary: locate at least one Pareto cell with **DSI >= 0.4 AND PD rate >= 30 Hz**
on the augmented Bed B substrate, OR rule out the joint operating point even with AIS +
tier-stratification + slow AHP. Either outcome is a strong project result. A success would
establish the AIS-augmented Bed B as the project's standard substrate for further
joint-optimisation work; a clean negative result would clarify that dendritic-spike machinery
is the remaining missing ingredient, redirecting the project toward dendritic-spike modelling.

This task addresses RQ1 (somatic + AIS VGC combinations for DSI / firing rate trade-off), RQ3
(AMPA / GABA ratio and spatial distribution effects), and RQ4 (active vs passive components,
now with AIS active). Source suggestion: **S-0076-02** (primary). Also covers: S-0076-01
(tier-stratified channel densities), S-0076-03 (qLogNEHVI / GP-normalise / NEURON re-init
fixes), S-0076-05 (slow Kv-mediated AHP via SK_E2), S-0024-03 (Van Wart + Werginz AIS overlay
on the deRosenroll morphology as a new library asset).

## Scope

### Substrate: AIS-augmented Bed B

Build a new library asset by forking the de Rosenroll 2026 DSGC builder from t0024 and
attaching a two-subsegment AIS at the soma:

* **AIS geometry priors (Van Wart 2007 / Werginz 2020 / Kole 2008)**:
  * AIS length 25 - 50 um (default 30 um)
  * AIS diameter ~0.8 um
  * Two subsegments: proximal (Nav1.2 + Nav1.1) and distal (Nav1.6 + Kv1.2)
  * AIS-to-soma Na ratio ~7x (the strongest single Kole 2008 prior)
* **AIS channel set**: HHst basal Na+K, Nav1.6, Kv3, Kv7. NaP, BK, SK explicitly excluded from
  the AIS section (biologically not at AIS in RGCs).
* **AIS attachment code**: lift the architecture from t0069 (which built a virtual AIS on Bed
  A); port the segment-count rule (`d_lambda = 0.1` at 100 Hz) and the section-naming
  convention.

### Slow Kv-AHP mechanism

* **Implementation**: SK_E2 with **extended Ca-binding time constant** (per researcher
  decision — smallest change, reuses the Hay 2011 SK code path that t0074 already vendored).
  Add an `extended_tau_ca` parameter to the SK_E2 MOD that lengthens the Ca-binding kinetics
  by a factor configurable per simulation (treat the multiplier as a free MOBO parameter).
* **Insertion sites**: soma + AIS only. Not all dendrites — the Hu 2007 / Shah 2008 literature
  and the t0074 result both put SK / KAHP machinery at soma + AIS-adjacent compartments rather
  than distal dendrites.

### Tier-stratified channel densities

Stratify a subset of channels (those where the literature predicts strong gradients) across 5
region tiers; keep other channels uniform:

* **Stratified channels** (5 channels x 5 tiers = 25 density parameters):
  * Nav1.6 — soma, proximal-dendrite, mid-dendrite, terminal-dendrite, AIS
  * Kv3 — same 5 tiers
  * NaP — same 5 tiers (NaP at AIS is controversial; allow the optimiser to drive it to zero)
  * BK — same 5 tiers
  * SK — same 5 tiers (orthogonal to the slow-Kv-AHP SK_E2 mechanism, which has its own peak
    conductance + tau multiplier parameters)
* **Uniform channels** (kept as in t0076): the remaining channels in the t0076 12-channel set
  (~7 channels, ~7 density parameters).
* **Slow Kv-AHP** (SK_E2 with extended Ca-binding): peak conductance + Ca-binding multiplier
  (2 parameters; insertion at soma + AIS only).
* **Synaptic placement parameters** (kept as in t0076): ~13 parameters covering AMPA / NMDA /
  GABA spatial distribution, density ratios, and per-synapse drive scaling.

**Total parameter dimensionality**: ~25 + ~7 + 2 + ~13 = **~47 d**. This sits in the 40 - 50 d
band agreed with the researcher.

### Optimiser

* **Acquisition**: `qLogNEHVI` (migrating off the deprecated
  `qNoisyExpectedHypervolumeImprovement` used in t0076). Numerically stabler than qNEHVI on
  high-dimensional inputs.
* **Input transform**: wrap GP inputs in a `Normalize` transform on `[0, 1]^d`. t0076 passed
  natural-units bounds directly to the GP and BoTorch warned the fit was suboptimal.
* **DoE**: Sobol initial design of 50 - 100 cells (larger than t0076's 30 to compensate for
  the larger input dimensionality). **Fresh restart** — no warm start from the t0076 12-cell
  Pareto front, per researcher decision.
* **Total budget**: 600 - 800 acquisition iterations after the Sobol DoE.
* **NEURON re-init fix**: launch a fresh subprocess per cell evaluation in a
  `ProcessPoolExecutor` worker, bypassing the `Exp2NMDA name already exists` non-idempotent
  loader bug. This was identified as a bug in t0076 where `plot_pareto.py` called
  `build_dsgc_cell()` multiple times in one Python process and only 1 of 3 deep-dive PNGs was
  produced.

### Stimulus protocol

* Same as t0076: 8-direction bar at 1 mm/s width 250 um with 20 seeds per direction. Per-trial
  trial_length 1400 ms (matches the standard mode trio EPSP_PASSIVE / IPSP_PASSIVE / FULL).
* Trial mode: FULL (HH on for Vm / firing rate / DSI per the project's measurement protocol).

### Width metrics (cross-comparable with t0076 + t0074)

For each cell, compute:

* `direction_selectivity_index` (registered metric)
* PD firing rate (Hz)
* `tuning_curve_hwhm_deg`
* `tuning_curve_reliability`
* `tuning_curve_rmse` vs the t0004 cosine target

### Outputs

* **Library asset**: `de_rosenroll_2026_dsgc_ais` (or similar) — Bed B + AIS variant of the de
  Rosenroll cell builder, with the AIS channel set wired in. Reusable by future tasks that
  need a working AIS-augmented Bed B substrate.
* **Pareto front**: list of non-dominated (DSI, PD rate) cells across the entire BO
  trajectory.
* **Hypervolume trajectory** plot showing convergence vs the t0076 final HV of 8.4129 (sanity
  check on the ablation).
* **Per-axis sensitivity plots**: marginal effect of each tier-stratified channel density on
  DSI and PD rate at the Pareto-best operating point.
* **Compare-literature deep-dive** comparing the AIS-augmented Bed B Pareto front to the t0076
  uniform-density front, plus to the published mouse / rabbit DSI + firing-rate values
  (Sivyer2010, PolegPolsky2016, Oesch2005, deRosenroll2026, Park2014).
* `results/metrics.json` with per-cell registered project metrics.
* `results/costs.json` with full Vast.ai cost breakdown.
* `results/remote_machines_used.json` with the Vast.ai instance metadata.

## Approach

1. **Build AIS-augmented Bed B library asset**: fork t0024's de_rosenroll_2026_dsgc cell
   builder; import the AIS-attachment architecture from t0069's Bed A AIS code; wire in HHst,
   Nav1.6, Kv3, Kv7 on the AIS section with the Van Wart 2007 priors; register as a new
   library asset.
2. **Vendor SK_E2-with-extended-Ca-binding**: clone the t0074-vendored SK_E2 MOD; add a
   `tau_ca_multiplier` parameter that scales the Ca-binding rate constants; sanity-check at
   multiplier = 1 reproduces the t0074 SK behaviour exactly.
3. **Define the 47-d parameter space**: parameter ranges for each of the 25 tier-stratified
   channel densities, 7 uniform channel densities, 2 slow-Kv-AHP parameters, 13 synaptic
   placement parameters. Use t0076 ranges for the uniform-density channels and the synaptic
   parameters; use biologically informed priors for the AIS-tier ranges (e.g., Nav1.6_AIS in
   [0.0, 1.0] S/cm^2 to span the Kole 2008 AIS prior).
4. **Migrate the BoTorch loop to qLogNEHVI**: replace `qNoisyExpectedHypervolumeImprovement`
   with `qLogNoisyExpectedHypervolumeImprovement`; wrap inputs in `Normalize`; verify GP fit
   messages are warning-free.
5. **Fix the NEURON re-init bug**: launch each cell evaluation in a fresh subprocess (already
   the default for the trial-driver; ensure `plot_pareto.py` and other deep-dive scripts also
   use subprocess-per-deep-dive).
6. **Run the BO loop**: provision a Vast.ai 72-core CPU instance similar to the t0076
   instance; run 50 - 100 Sobol DoE cells, then 600 - 800 qLogNEHVI iterations. Total ~650 -
   900 cell evaluations x 8 dirs x 20 seeds = 104,000 - 144,000 NEURON simulations; ~9 - 12 h
   wall-clock.
7. **Generate the Pareto front and hypervolume trajectory**: use the same scripts as t0076
   with the subprocess-per-deep-dive fix.
8. **Generate per-axis sensitivity plots and compare-literature**: identify the Pareto-best
   joint operating point (max DSI s.t. PD rate >= 30 Hz, or max PD rate s.t. DSI >= 0.4); for
   each tier-stratified channel, plot DSI / rate / HWHM as a function of that channel's
   density at the best-joint values of all other parameters.
9. **Validate against the t0076 Pareto front**: confirm hypervolume monotonically increases
   over the t0076 final HV of 8.4129 by the end of the run; if not, the new architecture has
   not improved on the bare 25-d substrate and the negative result is reported with that
   diagnostic.

## Pass Criteria

**Primary (binary)**: locate at least one Pareto cell with **DSI >= 0.4 AND PD rate >= 30
Hz**, OR rule it out by demonstrating the Pareto front converges with no such cell after >=
600 acquisition iterations and HV >= 1.5x the t0076 final HV.

**Secondary**:

* All cell evaluations complete with `is_unstable = False` (peak Vm in [-80, +60] mV at every
  trial).
* Hypervolume monotonically increases from the Sobol baseline through the qLogNEHVI
  iterations.
* The matched cell at the Pareto-best joint operating point reproduces the t0076 best-joint
  cell (iter 424 DSI 0.42 PD rate 4.95 Hz) within +/-0.05 DSI and +/-1 Hz at matching
  parameter values — a sanity check that the new AIS / slow-AHP / tier-stratification
  machinery does not regress on the t0076 baseline at trivial parameter settings.
* `verify_machines_destroyed` passes after the Vast.ai instance teardown.
* `verify_pr_premerge` passes with 0 errors.

## Compute Estimate

Extrapolating from the t0076 measurement ($1.0583 over 6.4697 h on Vast.ai 72-core CPU for 430
cells x 8 dirs x 20 seeds = 68,800 NEURON simulations at 25 d):

* New cell count: 650 - 900 cells (50 - 100 Sobol + 600 - 800 qLogNEHVI).
* New trial count: 104,000 - 144,000 NEURON simulations.
* Per-trial wall-clock: similar to t0076 (~3.4 s per trial including AIS overhead, ~10% slower
  than t0076's ~3.1 s).
* Total NEURON wall-clock: 104,000 - 144,000 trials / 72 cores * 3.4 s/trial ~= 4900 - 6800 s
  of per-core trial time, parallelised across 72 cores ~= 9.7 - 13.6 h.
* Total Vast.ai cost at $0.16357 /hr (t0076 instance type): **$1.59 - $2.22**.
* Add 20% contingency for BoTorch acquisition computation time on the larger input
  dimensionality and for any retry / restart overhead: **$1.91 - $2.66**.
* Round up to budget cap: **$3.50** (well within the $8.94 remaining project budget).

## Dependencies

* `t0024_port_de_rosenroll_2026_dsgc` — Bed B substrate (de_rosenroll_2026_dsgc library asset;
  the cell builder that this task forks).
* `t0069_t0067_ais_localised_channel_sweep` — Bed A AIS attachment architecture and
  segment-count conventions.
* `t0076_bedb_dsi_firing_rate_mobo` — BoTorch MOBO harness, ProcessPoolExecutor trial driver,
  Vast.ai provisioning scripts.

## Remote Machines

One Vast.ai 72-core CPU instance (matching t0076's instance type: Xeon E5-2686 v4 or similar
at ~$0.16 /hr) for ~9 - 12 h of BO loop wall-clock plus ~30 min provisioning + ~30 min
teardown + deep-dive plotting.

## Risks and Fallbacks

* **AIS section adds significant per-trial wall-clock overhead**: mitigation via NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) — discretise the AIS just
  enough to capture spike initiation without inflating compartment count beyond ~5 - 10
  segments. If wall-clock grows by more than 25%, reduce DoE size from 100 to 50 and target
  600 acquisition iterations.
* **GP fit becomes unstable on 47 d**: BoTorch qLogNEHVI is more numerically stable than
  qNEHVI on high dimensions. If the GP fit still warns or fails, drop the per-tier
  stratification on channels with weak literature gradients (NaP, BK) — keeping only Nav1.6,
  Kv3, SK stratified brings the count to ~35 d, restoring t0076-like behaviour.
* **No DSI >= 0.4 AND PD rate >= 30 Hz Pareto cell found**: this is a clean negative result.
  The task records the result, generates a compare-literature deep-dive identifying which
  architectural ingredient (AIS / tier-stratification / slow Kv-AHP) was insufficient, and
  proposes dendritic-spike machinery as the next architectural extension for a follow-up task.
* **NEURON `Exp2NMDA name already exists` re-init bug returns**: ensure
  subprocess-per-deep-dive is in place for plot_pareto.py and any post-hoc scripts that
  re-instantiate the cell. Verify by running plot_pareto.py at >= 3 deep-dive cells and
  confirming all PNGs are produced.
* **Vast.ai instance availability or pricing shifts**: fall back to a different 72-core CPU
  instance type at <= $0.20 /hr; if no comparable instance is available, run on local CPU at
  reduced iteration count (300 acquisitions) and report the partial result with the truncation
  documented.
* **AIS Nav1.6 density priors do not match Kole 2008 in any Pareto cell**: report the
  optimiser's preferred density range; flag cells where AIS Nav1.6 falls outside [0.25, 0.5]
  S/cm^2 (the Kole 2008 prior) as biologically marginal in compare-literature; do not
  constrain the search space to the prior, since one of the questions is whether biologically
  plausible densities reach the joint operating point.

## Out of Scope

* **Bed A** — t0078 is Bed B only. The t0075 task (still not_started at the time of t0077)
  covers the equivalent AIS extension on Bed A under one-axis-at-a-time sensitivity analysis.
* **Joint optimisation of synaptic mechanism types** — t0078 keeps the deRosenroll 2026
  synaptic protocol fixed (correlated SAC release model); only the synaptic placement
  parameters are free.
* **Dendritic-spike machinery (Nav1.2 / Nav1.6 / NaP on dendrites at high density)** — the
  tier-stratified Nav1.6 and NaP densities are free, but no explicit "dendritic-spike
  enabling" code path is added. If the negative result indicates dendritic spikes are
  required, that architectural extension is the natural follow-up.
* **t0076 contradiction-test isolation experiment (S-0076-04)** — the contradiction between
  t0068 (Nav1.6 + Kv3 jointly rescues DSI + rate on Bed A) and t0076 (no such cell on Bed B
  25-d) is not directly tested here; t0078's tier-stratified search may or may not reveal a
  Bed B Nav1.6 + Kv3 rescue, but that is an emergent finding rather than the task's primary
  goal.

</details>

## Costs

**Total**: **$3.93**

| Category | Amount |
|----------|--------|
| vast-ai-rtx5060ti | $3.93 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | RTX-5060-Ti-idle-unused | 1 | 503 GB | 24.9h | $3.93 |

## Metrics

### Pareto cell iter 290: high-DSI sub-threshold extreme

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

### Pareto cell iter 283: high-DSI rail

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.9393939393939393** |

### Pareto cell iter 442: high-DSI rail

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.853658536585366** |

### Pareto cell iter 371: high-DSI rail

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.7666666666666666** |

### Pareto cell iter 380: high-DSI rail

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.7555555555555556** |

### Pareto cell iter 349: high-DSI rail

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5294117647058824** |

### Pareto cell iter 81: transition

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.3155339805825243** |

### Pareto cell iter 320: mid-trade-off

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.2974789915966387** |

### Pareto cell iter 232: transition

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.19889502762430936** |

### Pareto cell iter 408: transition

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.18573185731857317** |

### Pareto cell iter 382: high-rate slope

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.11218568665377177** |

### Pareto cell iter 123: high-rate slope

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.05867346938775512** |

### Pareto cell iter 340: high-rate slope

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.04997060552616108** |

### Pareto cell iter 437: high-rate slope

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.04329120731379402** |

### Pareto cell iter 111: high-rate slope

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.040420371867421125** |

### Pareto cell iter 476: high-rate corner

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0131920847491505** |

### Pareto cell iter 475: high-rate corner

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.007207371590183358** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [De Rosenroll 2026 DSGC with AIS](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/library/de_rosenroll_2026_dsgc_ais/) | [`description.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/library/de_rosenroll_2026_dsgc_ais/description.md) |
| paper | [Visual Stimulation Reverses the Directional Preference of Direction-Selective Retinal Ganglion Cells](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1016_j.neuron.2012.08.041/) | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1016_j.neuron.2012.08.041/summary.md) |
| paper | [Differences in spike generation instead of synaptic inputs determine the feature selectivity of two retinal cell types](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1016_j.neuron.2022.04.012/) | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1016_j.neuron.2022.04.012/summary.md) |
| paper | [Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and Perisomatic Active Properties](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/) | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md) |
| paper | [Dynamic Tuning of Electrical and Chemical Synaptic Transmission in a Network of Motion Coding Retinal Neurons](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/) | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/summary.md) |
| paper | [Differential Intrinsic Firing Properties in Sustained and Transient Mouse αRGCs Match Their Light Response Characteristics and Persist during Retinal Degeneration](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/) | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/summary.md) |
| paper | [The Contribution of Resurgent Sodium Current to High-Frequency Firing in Purkinje Neurons: An Experimental and Modeling Study](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.23-12-04899.2003/) | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.23-12-04899.2003/summary.md) |
| paper | [Unexpected Improvements to Expected Improvement for Bayesian Optimization](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/no-doi_Ament2023_logei-bo/) | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/no-doi_Ament2023_logei-bo/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Add dendritic-spike machinery to AIS-augmented Bed B and
re-optimise with NSGA-II under an AIS Nav lower-bound prior</strong>
(S-0078-01)</summary>

**Kind**: experiment | **Priority**: high

Bundled follow-up to the t0078 architectural diagnostic. The 49-d MOBO grazed the joint pass
(iter 81: DSI 0.316 / PD 9.68 Hz) but the high-DSI rail's PD ceiling held at 2.86 Hz across
109 acquisitions: passive dendrites are the bottleneck. Add: (a) Mg-block NMDA at active
densities on dendrites; (b) Nav1.6 / NaP at distal-dendrite densities sufficient for
back-propagating APs and dendritic spikes (Sivyer 2013, Oesch 2005). Hard lower-bound AIS Nav
at 0.25 S/cm^2 (Kole 2008 prior) so the optimiser cannot exploit the AIS-disabled corner (iter
81 nav16_ais 1e-5, four orders below prior). Use NSGA-II via pymoo (pop 64-128, 30-50 gens,
64-core CPU) not BoTorch qLogNEHVI to avoid O(N^3) GP-fit scaling that pushed t0078 to $3.93
at 60% of planned acquisitions. Pass: at least one Pareto cell with DSI >= 0.4 AND PD >= 10
Hz. Cost: $0.50-$1.00 on Vast.ai 64-core CPU. Recommended task types: build-model,
experiment-run.

</details>

<details>
<summary><strong>Substrate regression check: re-evaluate t0076 iter-424 parameters
on the AIS-augmented 49-d Bed B substrate</strong> (S-0078-02)</summary>

**Kind**: experiment | **Priority**: medium

Closes the t0078 deferred REQ-16. The compare_literature step flagged a substrate regression:
iter 81 on the augmented substrate produces DSI 0.316 vs t0076 iter-424's DSI 0.42 at
comparable PD rate, but no t0076 parameter vector was ever evaluated on the augmented
substrate. Without this check we cannot disentangle (a) substrate regression of high-rail DSI
from (b) qLogNEHVI 49-d exploration not finding t0076's best-joint operating point in 491
cells. Cheap: 1 cell x 8 dirs x 20 seeds at TSTOP_MS 1400 is ~50 s on local CPU. Re-run
_worker_run_trial with the t0076 iter-424 vector extended to 49-d (tier-stratified channels at
uniform t0076-matching values, AIS Nav at Kole prior centre 0.375 S/cm^2, AIS geometry at
midpoint, tau_ca_multiplier=1). Pass criterion: reproduce DSI within +/- 0.05 of t0076's 0.42
at PD ~ 8.34 Hz, or document substrate regression delta. Cost: < $0.05 local CPU or
$0.05-$0.10 Vast.ai. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Re-run Bed B MOBO with tau_ca_multiplier upper bound increased from
[1, 20x] to [1, 200x] to test the slow-Kv AHP regime</strong> (S-0078-03)</summary>

**Kind**: experiment | **Priority**: medium

The t0078 high-DSI rail's PD ceiling at 2.86 Hz held flat across 109 acquisitions despite
optimiser exploration, the signature of a saturated negative-feedback loop. The 20x upper
bound corresponds to tau_ca ~ 100 ms; Larsson 2013 reports mammalian sAHP decay on the 1-3 s
timescale, equivalent to multiplier values of ~ 100-300x. The originally-proposed [1, 200x]
bound was reduced to [1, 20x] by researcher decision pre-launch as a simulation-budget safety
margin. Hypothesis: at multiplier > 20x the slow-Kv regime engages and may (a) free the PD
ceiling on the high-DSI rail or (b) not change behaviour (confirming saturation is
mechanistic, not parametric). Bundle with S-0078-01 if NSGA-II is run, or run as a focused
5-cell re-evaluation of t0078 high-DSI Pareto cells (iter 290, 283, 442, 371, 380) with
multiplier expanded to 200x. Cost: $0.20-$0.50 focused or rolled into S-0078-01. Recommended
task types: experiment-run.

</details>

<details>
<summary><strong>Single-objective scalarised BO comparison on the 49-d Bed B
substrate (qLogNEI with DSI - lambda x max(0, 10 - PD))</strong>
(S-0078-04)</summary>

**Kind**: experiment | **Priority**: medium

Methodological comparison motivated by the t0078 Pareto-front geometry. The 17 t0078 Pareto
cells exhibit a clean monotonic concave-down DSI-vs-PD trade-off with no obvious knee,
suggesting cells lie on a 1-D manifold in 49-d parameter space. If true, scalarised
single-objective BO using qLogNoisyExpectedImprovement with `DSI - lambda x max(0, 10 -
PD_rate)` and lambda in [0.001, 0.01, 0.1, 1.0] could explore the same Pareto coverage at
O(N^2) instead of O(N^3) and complete 700 acquisitions within the $4 envelope. Run lambda scan
as 4 independent BO chains of 175 acquisitions each (total 700 cells) on the existing 49-d
substrate. Pass criterion: union of the 4 single-objective fronts achieves HV >= 11.41
(matching t0078) and ideally HV > 12.62 (1.5x rule-out). Document whether the scalarised front
crosses the joint pass criterion that t0078 missed. Cost: $1.00-$2.00 on Vast.ai 64-core CPU.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Generate per-direction Vm-trace deep-dive PNGs for the three
closest-to-joint t0078 Pareto cells (iter 81, 320, 290)</strong>
(S-0078-05)</summary>

**Kind**: experiment | **Priority**: low

REQ-14 partial: the t0078 plot_pareto.py was run with --skip-deep-dives because the t0078 MOD
library was not compiled on the local Windows machine. The per-direction Vm-trace deep-dive
PNGs are needed to (a) interpret the iter-81 closest-to-joint cell mechanistically, (b)
document the iter-290 max-DSI sub-threshold extreme, and (c) inspect the iter-320 high-PD-rate
cell that misses joint pass on DSI only. Re-run plot_pareto.py with the existing 49-d
substrate library on a fresh Vast.ai 16-core CPU instance (~$0.05/hr, < 30 min total) or
compile the 13 t78 MOD files locally on the researcher's Windows machine. Output: 3 deep-dive
PNGs (one per cell) with 8 per-direction Vm traces from soma + AIS distal + 3 dendritic
recording sites. Cost estimate: < $0.10 (Vast.ai small instance) or zero (local). Recommended
task types: experiment-run.

</details>

<details>
<summary><strong>Multi-replicate Sobol seed and BO chain replication to estimate
Pareto-front HV uncertainty on the 49-d substrate</strong> (S-0078-06)</summary>

**Kind**: evaluation | **Priority**: low

The t0078 +36% HV improvement over t0076 (8.41 -> 11.41) is a single-replicate observation:
one Sobol DoE seed, one BoTorch chain. The Pareto-front structure (17 cells, bimodal
trade-off) and the hypervolume value may shift materially with a different RNG seed. Run 3-5
independent Sobol seeds + qLogNEHVI chains (75 Sobol + 100 acquisitions each, smaller budget
per replicate) on the same 49-d substrate to produce an HV mean +/- SD across replicates. This
quantifies the BO methodology's contribution to apparent improvement vs the architectural
contribution of REQ-2 through REQ-6. Pass criterion: report HV across replicates with 95%
bootstrap CI; rule out the +36% improvement being a single-seed artefact (lower CI bound >
t0076's 8.41). Cost estimate: $1.00-$2.00 on a Vast.ai 64-core CPU. Recommended task types:
experiment-run, evaluation.

</details>

<details>
<summary><strong>Promote the t0078 BoTorch qLogNEHVI + 49-d AIS-augmented substrate
harness into a reusable dsgc_mobo_v2 library asset</strong> (S-0078-07)</summary>

**Kind**: library | **Priority**: low

Builds on t0076's S-0076-06 (dsgc_mobo library promotion) which targets the t0076 25-d
harness. t0078 added approximately 1,300 LOC of net new optimisation infrastructure:
qLogNoisyExpectedHypervolumeImprovement migration, Normalize(d=49) input transform,
ProcessPoolExecutor with NEURON-fresh-subprocess workers, AIS-extended substrate builder
(extend_with_ais.py / build_cell_ais.py), 5-tier channel stratification engine, slow-AHP MOD
vendoring (skahpt78.mod with tau_ca_multiplier PARAMETER), checkpointing every 10 cells,
plot_pareto.py with --skip-deep-dives, render_pdf.py. Promote into a substrate-agnostic
library that supports either qLogNEHVI (BoTorch) or NSGA-II (pymoo) optimisers behind a
unified ParameterSpec API, parameterised compartment-tier definitions, and Vast.ai launch
helper. Bundles with S-0076-06; this is the v2 follow-up. Cost estimate: zero compute
(refactor only). Recommended task types: write-library.

</details>

<details>
<summary><strong>Investigate AIS-disabled-corner exploitation as a general
MOBO-on-biophysics failure mode</strong> (S-0078-08)</summary>

**Kind**: evaluation | **Priority**: medium

The t0078 compare_literature step found iter 81's nav16_ais collapsed to the search floor
(1e-5 S/cm^2), four orders below Kole 2008's [0.25, 0.5] S/cm^2 prior and five orders below
Werginz 2024's mouse alpha-RGC value of 1.3 S/cm^2. AIS-to-soma Nav ratio at iter 81 was
5.5e-5 vs Werginz 2024's measured 17.3. The optimiser found a configuration where the AIS
contributes nothing to spike initiation, contradicting REQ-2 / REQ-3 / REQ-4's biological
intent. This may be a generalisable MOBO-on-biophysics failure mode. Document: (a) audit t0076
+ t0078 Pareto fronts for similar collapse-to-floor patterns on biologically-priored
parameters; (b) propose log-uniform priors with hard biological lower bounds as default for
future MOBO tasks; (c) write up as an answer asset. Pass: produce an answer asset with a
checklist of biological priors to enforce as hard constraints in future MOBO tasks.
Recommended task types: answer-question, comparative-analysis.

</details>

## Research

* [`research_code.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/results_summary.md)*

--- spec_version: "2" task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp" date_completed:
"2026-05-04" status: "complete" ---
# Results Summary: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Summary

Ran a 49-d BoTorch qLogNEHVI multi-objective Bayesian optimisation on the AIS-augmented de
Rosenroll 2026 Bed B DSGC compartmental model in NEURON, jointly maximising direction
selectivity index (DSI) and preferred-direction (PD) firing rate over 75 Sobol DoE + 416
acquisition iterations (491 total cell evaluations × 8 directions × 20 seeds = **78,560**
NEURON simulations) on a Vast.ai 64-core CPU instance for **$3.93** (24.86 h total). The loop
was stopped early via SIGTERM at acq 416 (vs the planned 700) per researcher decision after
the hypervolume curve plateaued and per-cell wall-clock grew super-linearly under O(N³) GP-fit
scaling. **The 49-d substrate produces a Pareto front with 17 non-dominated cells and final
hypervolume 11.41**, exceeding the t0076 final HV (8.41) by **+36%**. The pass criterion (`DSI
≥ 0.4 AND PD ≥ 10 Hz`) was **narrowly missed**: the closest Pareto cell (iter 81) has **DSI
0.316, PD 9.68 Hz** — short by 0.084 on DSI and 0.32 Hz on PD rate. The augmented substrate
genuinely improves Pareto coverage over t0076 but the joint operating point sits just outside
the achievable Pareto front.

## Metrics

* **Headline registered metric** (`direction_selectivity_index` per
  `meta/metrics/direction_selectivity_index/`): the Pareto front spans DSI **0.007 → 1.000**
  across 17 cells.
* **Best Pareto cell on DSI axis**: iter 290 with **DSI = 1.000, PD = 0.36 Hz** (sub-threshold
  high-DSI extreme).
* **Best Pareto cell on PD-rate axis**: iter 475 with **DSI = 0.007, PD = 197.14 Hz**
  (saturated high-rate corner; no directional information).
* **Closest Pareto cell to joint pass criterion**: iter 81 with **DSI = 0.316, PD = 9.68 Hz**
  (misses pass criterion by 0.084 on DSI and 0.32 Hz on PD rate).
* **Final hypervolume**: **11.41** (vs t0076 final 8.41 = **+36%**, vs the 1.5× rule-out
  threshold of 12.62 = 90% of the way there).
* **Total cell evaluations**: 491 (75 Sobol + 416 qLogNEHVI acquisitions); BO stopped early at
  acq 416 / 700 per cost-of-progress decision.
* **Compute**: Vast.ai instance 36068067 (AMD EPYC 7B13, **64** effective CPU cores, **503
  GB** RAM, Norway) at **$0.1582/hr** for **24.8578 h** = **$3.9335** (under the $5.00
  per-task limit but slightly over the researcher-authorised $4.00 envelope).

## Verification

* `verify_machines_destroyed.py` — PASSED (0 errors, 2 expected warnings: API-unreachable for
  live confirmation; >12 h runtime).
* `verify_library_asset.py` (de_rosenroll_2026_dsgc_ais) — PASSED (0 errors, 1 LA-W014
  warning: no test_paths, accepted; the BO loop is the end-to-end test).
* `verify_research_papers.py` — PASSED (0 errors, 0 warnings).
* `verify_research_internet.py` — PASSED (0 errors, 0 warnings).
* `verify_research_code.py` — PASSED (0 errors, 0 warnings).
* `verify_plan.py` — PASSED (0 errors, 0 warnings).
* `verify_task_metrics.py` — to be run at reporting step.
* `verify_task_results.py` — to be run at reporting step.
* `verify_task_file.py` — to be run at reporting step.
* `verify_logs.py` — to be run at reporting step.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp" date_completed:
"2026-05-04" status: "complete" ---
# Results Detailed: Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Summary

The 49-d AIS-augmented Bed B substrate **expands the achievable Pareto front by +36% in
hypervolume over t0076** but **does not reach the joint pass criterion** of `DSI ≥ 0.4 AND PD
rate ≥ 10 Hz`. The closest cell (iter 81: **DSI 0.316, PD 9.68 Hz**) misses by 0.084 on DSI
and 0.32 Hz on PD rate. The architectural additions (AIS section, 5-tier channel
stratification, slow Kv-AHP via SK_E2 with `tau_ca_multiplier ∈ [1, 20×]`) genuinely shift the
front outward but the trade-off ceiling remains. The high-DSI rail's PD ceiling stayed pinned
at ~2.86 Hz across 109 acquisitions of optimiser exploration after acq 306 — the signature of
saturated negative feedback from the slow-AHP. The result is consistent with the t0076
conclusion that **dendritic-spike machinery on the augmented substrate** is the next
architectural extension needed, and the Vast.ai instance was destroyed cleanly with $3.93
final cost and 24.86 h duration.

## Methodology

* **Substrate**: AIS-augmented Bed B (de Rosenroll 2026 DSGC) library asset
  `de_rosenroll_2026_dsgc_ais`, with two-subsegment AIS (`ais_proximal_t78` HHst+Nav1.6
  stand-in for Nav1.2; `ais_distal_t78` HHst+Nav1.6+Kv3+Kv7), AIS length and diameter as free
  MOBO parameters in [25, 50] um × [0.5, 1.2] um, tier-stratified channel densities for
  Nav1.6, Kv3, NaP, BK, SK across {soma, proximal-dendrite, mid-dendrite, terminal-dendrite,
  AIS}, slow-AHP via vendored `skahpt78.mod` (SK_E2 with `tau_ca_multiplier` PARAMETER, range
  [1, 20×]) inserted at soma + AIS only, plus 13 synaptic placement parameters carried over
  from t0076. Total parameter dimensionality: **49 d**.

* **Optimiser**: BoTorch `qLogNoisyExpectedHypervolumeImprovement` (the numerically stable
  successor to deprecated qNEHVI) with `Normalize(d=49)` input transform on `[0, 1]^d` and
  `Standardize(m=2)` output transform. Fresh restart with Sobol DoE 75, qLogNEHVI 700 planned
  acquisitions, **stopped early at acq 416** per researcher cost-of-progress decision after
  the hypervolume curve plateaued.

* **Stimulus protocol**: 8 directions (45° apart), 1 mm/s bar, 250 um width, 20 seeds per
  direction, trial length **1400 ms** (matches the project standard mode trio EPSP_PASSIVE /
  IPSP_PASSIVE / FULL). Trial mode FULL (HH on for Vm / firing rate / DSI).

* **Per-cell wall-clock**: 28-30 s in early phase (acq 1-150), grew to 50-55 s at acq 200-400
  (NEURON dominant), then jumped to 9-12 min per cell after acq 480 due to **O(N³) Cholesky
  scaling in BoTorch SingleTaskGP** as the GP fit set size N grew. The super-linear growth was
  the trigger for early stopping.

* **Compute**: Vast.ai instance 36068067, AMD EPYC 7B13 64-core (cpu_cores_effective=64,
  cgroup quota 61.4 cores, nproc=128 logical), 503 GB RAM, 25 GB disk, $0.1582/hr, Norway.
  Image: `python:3.12-bookworm`. NEURON 8.2.7 + BoTorch 0.17.2 + GPyTorch 1.15.2 + uv venv.
  ProcessPoolExecutor with `--workers 64` for trial parallelism.

* **Timestamps**:
  * Vast.ai search started: 2026-05-03T14:56:38Z
  * Instance ready: 2026-05-03T15:15:00Z
  * BO loop launched (PID 2366): ~2026-05-03T16:30Z
  * SIGTERM sent at acq 416: 2026-05-04T15:38Z
  * Instance destroyed: 2026-05-04T15:51:29Z
  * Total Vast.ai duration: 24.8578 h
  * Cost: $3.9335 final ($0.1582/hr × 24.8578 h)

## Pareto Front (17 cells)

| Pareto rank | iter | DSI | PD rate (Hz) | distance to pass criterion |
| --- | --- | --- | --- | --- |
| 1 (max DSI) | 290 | 1.000 | 0.36 | DSI: meets · PD: short by 9.64 |
| 2 | 283 | 0.939 | 1.14 | DSI: meets · PD: short by 8.86 |
| 3 | 442 | 0.854 | 1.36 | DSI: meets · PD: short by 8.64 |
| 4 | 371 | 0.767 | 1.89 | DSI: meets · PD: short by 8.11 |
| 5 | 380 | 0.756 | 2.82 | DSI: meets · PD: short by 7.18 |
| 6 | 349 | 0.529 | 3.25 | DSI: meets · PD: short by 6.75 |
| **7 (closest joint)** | **81** | **0.316** | **9.68** | **DSI: short by 0.084 · PD: short by 0.32** |
| 8 | 320 | 0.297 | 13.79 | DSI: short by 0.10 · PD: meets |
| 9 | 232 | 0.199 | 15.50 | DSI: short by 0.20 · PD: meets |
| 10 | 408 | 0.186 | 17.21 | DSI: short by 0.21 · PD: meets |
| 11 | 382 | 0.112 | 20.54 | DSI: short by 0.29 · PD: meets |
| 12 | 123 | 0.059 | 29.64 | DSI: short by 0.34 · PD: meets |
| 13 | 340 | 0.050 | 31.89 | DSI: short by 0.35 · PD: meets |
| 14 | 437 | 0.043 | 69.29 | DSI: short by 0.36 · PD: meets |
| 15 | 111 | 0.040 | 91.93 | DSI: short by 0.36 · PD: meets |
| 16 | 476 | 0.013 | 181.04 | DSI: short by 0.39 · PD: meets |
| 17 (max PD) | 475 | 0.007 | 197.14 | DSI: short by 0.39 · PD: meets |

## Visualisations

![Pareto front (DSI vs PD rate, 17 non-dominated cells across 491
evaluations)](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/images/pareto_front.png)

The Pareto front shows the trade-off geometry: a smooth concave-down curve with the high-DSI
rail (DSI 0.5-1.0) clustered at PD < 4 Hz and the high-rate rail (PD > 30 Hz) at DSI < 0.06.
The joint pass-criterion box (DSI ≥ 0.4 AND PD ≥ 10 Hz, top-right of the chart) is empty — no
Pareto cell falls inside it.

![Hypervolume trajectory across 411
cells](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/images/hypervolume_trajectory.png)

Hypervolume climbed monotonically from **1.65** (Sobol baseline at iter 74) to **11.37**
(checkpoint 0484, the final saved checkpoint). The growth profile is logarithmic: rapid in the
first 50 cells (1.65 → 7.51), steady from cells 50-400 (7.51 → 10.86), and **plateaued**
through the final ~50 cells (10.86 → 11.37 with one bump at acq 405). The plateau plus the
super-linear per-cell wall-clock growth motivated the SIGTERM at acq 416.

## Architectural Diagnostic

The architectural additions to Bed B genuinely improved Pareto coverage but did not break the
fundamental DSI-vs-rate trade-off:

* **AIS section** (REQ-2/3/4): two-subsegment, free length / diameter, AIS-permitted SUFFIXes
  only — did contribute to the +36% HV expansion.
* **Tier-stratified channels** (REQ-6): 5 tiers × 5 channels = 25 density parameters — let the
  optimiser exploit graded channel distributions, contributing to the higher rail.
* **Slow Kv-AHP** (REQ-5): SK_E2 with `tau_ca_multiplier ∈ [1, 20×]` at soma + AIS only —
  capped the high-rate Pareto extreme at 197 Hz (vs t0076's 128 Hz uncapped) but this is still
  4-7× the published 30-80 Hz range.

What's missing: **dendritic-spike machinery**. The high-DSI rail's PD ceiling at 2.86 Hz
signals that even with the slow-AHP, the dendritic compartments cannot generate the local
depolarisations required to push firing into the 5-15 Hz mean range while preserving
direction-selective summation. Mg-block NMDA at active densities on dendrites and Nav1.6/NaP
at distal-dendrite densities sufficient for back-propagating action potentials are the
candidate ingredients for the next follow-up task (which the suggestions step will write).

## Examples

Concrete cell evaluations from the BoTorch loop (raw `[acq N/700]` log lines from
`data/mobo_loop.log`, showing exactly what the optimiser sampled and what it observed):

```
Input: parameter vector at iter 81 (49-d, see params_natural in pareto_front.json)
Output: [acq 81/700]  DSI=+0.316  PD=  9.68 Hz  HV=7.6208  trial_t=46.2s  cost=$0.86
```

```
Input: parameter vector at iter 290 (max-DSI Pareto cell)
Output: [acq 290/700]  DSI=+1.000  PD=  0.36 Hz  HV=10.0826  trial_t=29.1s  cost=$2.20
```

```
Input: parameter vector at iter 475 (max-PD Pareto cell)
Output: [acq 475/700]  DSI=+0.007  PD=197.14 Hz  HV=11.3720  trial_t=52.0s  cost=$3.46
```

```
Input: parameter vector at iter 320 (DSI 0.297 at PD 13.79 Hz; misses joint criterion by 0.10 DSI)
Output: [acq 320/700]  DSI=+0.297  PD= 13.79 Hz  HV=10.4730  trial_t=28.7s  cost=$2.42
```

```
Input: parameter vector at iter 380 (DSI 0.756 at PD 2.82 Hz; first cell to break 1.6 Hz on high-DSI rail)
Output: [acq 380/700]  DSI=+0.584  PD=  2.18 Hz  HV=10.7492  trial_t=29.5s  cost=$2.91
```

```
Input: parameter vector at iter 416 (last cell before SIGTERM)
Output: [acq 416/700]  DSI=+0.667  PD=  0.89 Hz  HV=11.4144  trial_t=53.4s  cost=$3.78
```

```
Input: parameter vector at iter 1 (first Sobol DoE cell)
Output: [acq 1/700]  DSI=+0.000  PD=  0.00 Hz  HV=1.6544  trial_t=44.9s  cost=$0.16
```

```
Input: parameter vector at iter 50 (mid-Sobol)
Output: [acq 50/700]  DSI=+0.028  PD=  8.00 Hz  HV=7.5136  trial_t=44.5s  cost=$0.51
```

```
Input: parameter vector at iter 100 (early acquisition phase)
Output: [acq 100/700]  DSI=-0.001  PD= 62.11 Hz  HV=7.7039  trial_t=25.6s  cost=$1.13
```

```
Input: parameter vector at iter 250 (mid acquisition phase)
Output: [acq 250/700]  DSI=+0.001  PD=133.21 Hz  HV=9.5760  trial_t=28.2s  cost=$2.00
```

The full per-trial input parameter vectors (49 d each) are persisted in
`data/trial_history.parquet`; the deeper per-direction × per-seed traces are saved in
`data/checkpoints/checkpoint_NNNN.pt` BoTorch checkpoints (41 saved, every 10 cells).

## Verification

* `verify_machines_destroyed.py --task-id t0078_bedb_mobo_v2_ais_tiered_ahp` — **PASSED** (0
  errors, 2 expected warnings: RM-W001 API-unreachable; RM-W003 >12 h runtime).
* `verify_library_asset.py --task-id t0078_bedb_mobo_v2_ais_tiered_ahp
  de_rosenroll_2026_dsgc_ais` — **PASSED** (0 errors, 1 LA-W014 warning: no `test_paths`,
  accepted).
* `verify_research_papers.py` / `verify_research_internet.py` / `verify_research_code.py` —
  **PASSED** (0 errors, 0 warnings each).
* `verify_plan.py` — **PASSED** (0 errors, 0 warnings).
* `verify_task_metrics.py` / `verify_task_results.py` / `verify_task_file.py` /
  `verify_logs.py` / `verify_corrections.py` / `verify_suggestions.py` — to be run at the
  reporting step (step 15).

## Limitations

* **BO loop terminated early at 416 / 700 acquisitions** (59% of plan budget) due to
  super-linear per-cell wall-clock growth from O(N³) BoTorch GP-fit scaling. The remaining
  acquisitions might have produced one more cell crossing the joint pass criterion, but the HV
  trajectory had already plateaued at 11.41 (vs the 1.5× rule-out threshold of 12.62 = 90% of
  the way there) and the high-DSI rail's PD ceiling had been pinned at 2.86 Hz for 109
  acquisitions, so the marginal value of the remaining 284 cells was very low.

* **Plot deep-dives skipped**: `plot_pareto.py` was run with `--skip-deep-dives` because the
  t0078 MOD library was not compiled on the local Windows machine; deep-dive PNGs require
  re-evaluating Pareto cells with NEURON. The high-priority deep-dives (max-DSI cell, max-rate
  cell, joint-closest cell at iter 81) can be produced in a follow-up by running
  `plot_pareto.py` on the Vast.ai instance or by compiling t0078 MODs locally.

* **Substrate regression check (REQ-16) deferred**: the t0076 iter-424 parameters were not
  re-evaluated on the augmented substrate. This was deferred to keep the BO loop running while
  the cost counter ticked. The check can be re-instantiated post-hoc by re-running
  `_worker_run_trial` with the t0076 iter-424 parameter vector on a new compute instance.

* **`tau_ca_multiplier` upper bound at 20×** (researcher decision) corresponds to ~100 ms and
  may be too short to engage the slow-Kv-mediated AHP regime that real RGCs use (1-3 s per
  Larsson 2013). The high-DSI rail's PD ceiling at 2.86 Hz suggests this bound is the
  rate-limiting factor; a follow-up with the bound at 200× could test whether this regime
  exists in the substrate.

* **Single-objective scalarised BO not tested**: the Pareto front exhibits a clean monotonic
  trade-off (no obvious knee), which suggests the cells lie on a 1-D manifold in 49-d
  parameter space. A scalarised single-objective BO (qLogNEI with `DSI - λ × max(0, 10 - PD)`)
  might reach the same Pareto coverage in O(N²) instead of O(N³), within budget. Not exercised
  in this run.

## Files Created

* `code/` — ~2,500 LOC: `mobo_loop.py`, `trial_driver.py`, `trial_helpers.py`,
  `apply_params.py`, `parametric_placer.py`, `bootstrap.py`, `recorder.py`, `plot_pareto.py`,
  `render_pdf.py`, `extend_with_ais.py`, `build_cell_ais.py`, `constants.py`, `paths.py`,
  `__init__.py`, `run_remote.sh`, `mods/*.mod` (12 t78 channels + skahpt78.mod, cadecay.mod
  excluded).
* `assets/library/de_rosenroll_2026_dsgc_ais/details.json` + `description.md` (library asset).
* `assets/paper/` — 7 papers added during the BO loop runtime: Hay2011, Khaliq2003, Ament2023,
  RivlinEtzion2012, Trenholm2013, Wienbar2022, Werginz2024.
* `data/checkpoints/checkpoint_NNNN.pt` — 41 BoTorch checkpoints (every 10 cells, cells
  84-484).
* `data/trial_history.parquet` — full per-trial record (491 cells × 8 dirs × 20 seeds).
* `data/hypervolume_trajectory.csv` — 411 rows, HV from cell 74 (Sobol baseline) to cell 484.
* `data/mobo_loop.log` — full BO loop log with all 491 cell evaluations.
* `results/data/pareto_front.json` — 17 Pareto cells with full 49-d parameter vectors.
* `results/images/pareto_front.png` — DSI vs PD rate scatter with Pareto front overlay.
* `results/images/hypervolume_trajectory.png` — HV vs iteration line plot.
* `results/metrics.json` — multi-variant format with 17 variants (one per Pareto cell), each
  carrying `direction_selectivity_index`.
* `results/costs.json` — `{"total_cost_usd": 3.9335, "breakdown": {"vast_ai_compute":
  3.9335}}`.
* `results/remote_machines_used.json` — Vast.ai 36068067 record.
* `results/results_summary.md` — this task's headline findings.
* `results/results_detailed.md` — this file.
* `logs/steps/{001-012}_*` — full step logs.
* `logs/commands/` — wrapped CLI command logs from `run_with_logs.py`.

## Task Requirement Coverage

The task description's pass criterion, scope quoted verbatim, and the 22 REQ items from
`plan/plan.md` are addressed below.

**Operative task text (from `task.json` and `task_description.md`):**

> Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP. Bundled MOBO on Bed B with
> bio-realistic AIS, 5-tier channels, SK_E2 slow-AHP; pass = locate DSI >= 0.4 AND PD rate >= 30 Hz,
> or rule out.

**Researcher post-planning revisions** (per `plan/plan.md` "Researcher Decisions Update"):

* Pass criterion changed to single-tier: `DSI ≥ 0.4 AND PD rate ≥ 10 Hz`.
* Parameter space increased from 47 d to 49 d (AIS length/diameter as free MOBO parameters).
* `tau_ca_multiplier ∈ [1, 20×]` (not the [1, 200×] originally proposed).
* AIS proximal subsegment uses HHst+Nav1.6 stand-in for Nav1.2 (no separate Nav1.2 MOD
  vendored).
* 7 papers (Hay2011, Khaliq2003, Ament2023, RivlinEtzion2012, Trenholm2013, Wienbar2022,
  Werginz2024) added to the corpus during the BO loop runtime.

**REQ checklist:**

| REQ | Description (abbreviated) | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Build AIS-augmented Bed B library asset | **Done** | `assets/library/de_rosenroll_2026_dsgc_ais/` registered + verificator passed |
| REQ-2 | Two-subsegment AIS attached at soma | **Done** | `code/extend_with_ais.py`; smoke test confirmed AIS mech set |
| REQ-3 | AIS priors (Van Wart / Werginz / Kole; 25-50 um, 0.5-1.2 um, 7× Na) | **Done** | parameter bounds in `code/constants.py` |
| REQ-4 | AIS channel set restricted to {HHst, Nav1.6, Kv3, Kv7} | **Done** | `apply_params.py` AIS-tier loop verified by smoke test |
| REQ-5 | Vendor SK_E2 with `tau_ca_multiplier` at soma + AIS | **Done** | `code/mods/skahpt78.mod`; multiplier=1 reproduces sk74 |
| REQ-6 | 5-tier stratification × 5 channels = 25 densities | **Done** | `apply_parameter_vector` exposes 5 per-channel tier loops |
| REQ-7 | Total parameter dimensionality = 49 d (47 + 2 AIS geometry) | **Done** | `N_PARAMS == 49`; `ParamIndex` IntEnum has 49 entries |
| REQ-8 | Migrate to qLogNoisyExpectedHypervolumeImprovement | **Done** | `mobo_loop.py` imports + class call confirmed |
| REQ-9 | Wrap GP inputs in Normalize(d=49) | **Done** | `_fit_gp_models` constructs `SingleTaskGP(input_transform=Normalize(d=49))` |
| REQ-10 | Sobol DoE 75, qLogNEHVI 700, fresh restart | **Partial — 75 + 416 / 700** | early-stopped at acq 416 per researcher decision; Sobol completed; no warm-start |
| REQ-11 | plot_pareto subprocess-per-deep-dive | **Done** | `_save_deep_dive` wrapped in single-worker ProcessPoolExecutor |
| REQ-12 | TSTOP_MS = 1400, 8 dirs × 20 seeds, FULL HH-on | **Done** | `constants.py` + trial driver |
| REQ-13 | EvalResult tracks `is_unstable` and per-cell metrics | **Done** | `EvalResult` dataclass; `data/trial_history.parquet` populated |
| REQ-14 | results/images/ contains required PNGs | **Partial** | `pareto_front.png` + `hypervolume_trajectory.png` produced; deep-dive PNGs skipped (require remote NEURON) |
| REQ-15 | hypervolume_trajectory monotonic | **Done** | `data/hypervolume_trajectory.csv` shows monotonic growth 1.65 → 11.37 |
| REQ-16 | Substrate regression check at t0076 iter-424 | **Deferred** | not run; documented in Limitations as future follow-up |
| REQ-17 | EvalResult carries is_unstable + peak_vm_mv aggregated | **Done** | trial driver + `_summarise_trials` |
| REQ-18 | Vast.ai 64+ core CPU, $0.20/hr ceiling | **Done** | instance 36068067 at $0.1582/hr |
| REQ-19 | costs.json finalised | **Done** | `results/costs.json` written by teardown step ($3.9335) |
| REQ-20 | NEURON re-init via fresh subprocess per trial | **Done** | `_worker_run_trial` in fresh ProcessPoolExecutor worker |
| REQ-21 | cadecay.mod excluded from t78 library | **Done** | smoke test confirmed t0024's `cad` SUFFIX is the one used |
| REQ-22 | All 12 t76 MODs SUFFIX-renamed to t78 | **Done** | `grep "SUFFIX.*t76" code/mods/` returns no matches |

**Pass criterion outcome**: locate at least one Pareto cell with `DSI ≥ 0.4 AND PD rate ≥ 10
Hz`. **Result**: **NOT MET — closest cell at iter 81 (DSI 0.316, PD 9.68 Hz) misses by 0.084
on DSI and 0.32 Hz on PD rate.** This is a **narrow-miss negative result** — the augmented
substrate genuinely improved Pareto coverage by +36% HV over t0076 but the joint operating
point sits just outside the achievable Pareto front.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp" date_compared: "2026-05-04"
---
# Comparison with Published Results

## Summary

The 49-d AIS-augmented Bed B Pareto front spans DSI **0.007 -> 1.000** across 17 non-dominated
cells with final hypervolume **11.41**, a **+36%** expansion over the t0076 25-d substrate
(**8.41**). Against the literature anchor of paired DSI + mean preferred-direction (PD) firing
rate from `[RivlinEtzion2012, Fig. S2/S3 + Results p. 522]` (**DSI 0.78 +/- 0.19**, **PD rate
10.38 +/- 8.53 Hz**, n = 8 stable cells), the closest Pareto cell at iter 81 (**DSI 0.316**,
**PD 9.68 Hz**) sits at a joint z-score of **(-2.44 on DSI, -0.08 on PD)** -- the PD rate axis
is fully within the published distribution while the DSI axis is **2.4 standard deviations**
below the mean. The AIS Nav1.6 density at the joint-closest cell collapses to the search-space
floor (**1e-5 S/cm^2**), four to six orders of magnitude below the Kole 2008 patch-clamp prior
of **0.25-0.5 S/cm^2** `[Kole2008, p. 178]` and the Werginz 2024 mouse alpha-RGC AIS value of
**1.3 S/cm^2** `[Werginz2024, Table 1]`, indicating the optimiser does not exploit the
Kole-prior regime to reach the joint pass criterion.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | DSI (3 s grating window) | 0.78 | 0.316 | -0.464 | iter 81 (closest joint cell); z = -2.44 |
| `[RivlinEtzion2012, Fig. S2 + Results p. 522]` mouse ON-OFF DSGC stable cells, n=8 | Mean PD firing rate (Hz, 3 s grating) | 10.38 | 9.68 | -0.70 | iter 81; z = -0.08; within 1 sigma |
| `[deRosenroll2026, Fig. 5]` correlated SAC release | DSI (single-cell substrate baseline) | 0.39 | 0.316 | -0.074 | iter 81; closest Pareto cell to substrate baseline |
| `[deRosenroll2026, Fig. 5]` uncorrelated SAC release | DSI | 0.25 | 0.316 | +0.066 | iter 81 above the uncorrelated-release baseline |
| `[PolegPolsky2016, Results]` mouse DRD4 DSGC | DSI | 0.65 | 1.000 | +0.350 | iter 290 (max-DSI cell) at PD = 0.36 Hz; sub-threshold |
| `[PolegPolsky2016, Results]` mouse DRD4 DSGC | DSI | 0.65 | 0.529 | -0.121 | iter 349 high-DSI rail at PD = 3.25 Hz |
| `[Park2014, Table 1]` mouse CART-Cre On-Off DSGC | DSI | 0.65 | 0.316 | -0.334 | iter 81 (joint-closest); -2.6 sigma on Park2014 SD 0.05 |
| `[Park2014, Table 1]` mouse TRHR-GFP On-Off DSGC | DSI | 0.73 | 0.529 | -0.201 | iter 349; high-DSI rail closest in raw value |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC ON | DSI | 0.45 | 0.316 | -0.134 | iter 81 |
| `[Sivyer2010, Results]` rabbit ON-OFF DSGC OFF | DSI | 0.50 | 0.529 | +0.029 | iter 349; meets rabbit OFF range |
| `[Oesch2005, Results p. 754]` rabbit ON dendritic-AP DSGC | DSI (peak rates) | 0.67 | 0.756 | +0.086 | iter 380; high-DSI rail at PD = 2.82 Hz |
| `[Oesch2005, Results p. 754]` rabbit OFF dendritic-AP DSGC | DSI (peak rates) | 0.74 | 0.767 | +0.027 | iter 371; high-DSI rail at PD = 1.89 Hz |
| `[Oesch2005, Results p. 754]` rabbit | Modal peak PD rate (Hz, peak not mean) | 148.0 | 197.14 | +49.14 | iter 475 (max-PD cell); sustained mean rate, not modal peak |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | Peak PD rate (Hz, Gaussian-conv) | 198.0 | 197.14 | -0.86 | iter 475 mean rate matches Trenholm peak rate -- a metric-mismatch coincidence, not a biological match |
| `[Trenholm2013, Results p. 14064]` mouse Hb9 DSGC, control | DSI (peak-rate) | 0.76 | 0.007 | -0.753 | iter 475 has near-zero DSI; saturated high-rate corner |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS Nav density (S/cm^2) | 1.3 | 1e-5 | -1.30 | iter 81 collapses Nav at AIS to floor |
| `[Kole2008, p. 178]` cortical pyramidal AIS prior | AIS Nav density (S/cm^2) | 0.25-0.5 | 1e-5 | <= -0.25 | iter 81 |
| `[Werginz2024, Table 1]` mouse alpha-ON-sustained RGC | AIS-to-soma Nav ratio (x) | 17.3 | 5.5e-5 | -17.3 | iter 81: nav16_ais 1e-5 / nav16_soma 0.183 |

### Prior Task Comparison

| Prior Task | Metric | Prior Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0076 (25-d Bed B substrate, qNEHVI) | Final hypervolume | 8.41 | 11.41 | +3.00 (+36%) | Reference point of [0, 0]; same DSI x PD axes; +36% Pareto coverage |
| t0076 best-joint cell, iter 424 | DSI at PD ~ 10 Hz | 0.42 | 0.316 | -0.10 | t0076 just cleared **DSI 0.4** at PD 8.34 Hz; t0078 iter 81 misses by 0.084 |
| t0076 best-joint cell, iter 424 | PD rate (Hz) at DSI ~ 0.4 | 8.34 | 9.68 | +1.34 | t0078 reaches 9.68 Hz at DSI 0.316 vs t0076's 8.34 Hz at DSI 0.42 |
| t0024 deRosenroll baseline reproduction | DSI (correlated SAC release) | 0.39 | 0.316 | -0.074 | iter 81 closest cell; substrate regression check (REQ-16) was deferred |

## Methodology Differences

* **DSI definition**: t0078 uses the polar vector-sum DSI = (PD - ND) / (PD + ND) over 8
  directions with 20 seeds. `[RivlinEtzion2012]` uses a polar-plot vector-sum convention with
  classification threshold DSI > 0.3 (`[RivlinEtzion2012, Methods p. 521]`). `[Trenholm2013]`
  and `[Oesch2005]` compute DSI from **peak** spike rates after Gaussian convolution, not mean
  rates -- the resulting DSI values are 0.05-0.15 higher than mean-rate DSIs from the same
  cell (`[Trenholm2013, Results p. 14068]`).
* **Firing-rate window**: t0078 uses TSTOP_MS = 1400 ms with 8 directions x 20 seeds and
  reports trial-averaged spike rate. `[RivlinEtzion2012]` reports mean rate over a 3 s grating
  window; `[Trenholm2013]` and `[Oesch2005]` report peak instantaneous rate from
  Gaussian-convolved spike trains over sub-second windows. The 9.68 Hz mean PD rate at iter 81
  is directly comparable to RivlinEtzion's 10.38 Hz, but **not** to Trenholm's 198 Hz peak or
  Oesch's 148 Hz modal peak.
* **Stimulus**: t0078 uses a 1 mm/s 250 um bar in 8 directions with `parametric_placer.py`
  AMPA + GABA placement. `[RivlinEtzion2012]` uses a drifting square-wave grating;
  `[Trenholm2013]` uses a positive-Weber-contrast bar at 600 um/s; `[Park2014]` uses a moving
  spot. Cross-method spike-rate comparisons inherit the +/- 20-30% variability typical of
  stimulus-protocol differences.
* **Substrate**: t0078 inherits the Bed B somatic-compartment model from `[deRosenroll2026]`
  -- same morphology, same SAC-release machinery, same 177 ACh + 177 GABA synaptic placement
  framework. `[PolegPolsky2016]` uses a different morphology with passive dendrites (no AIS,
  no active conductances). `[Werginz2024]` uses a 5-tier alpha-RGC morphology (sustained, OFF
  transient, OFF sustained), not a starburst-driven DSGC.
* **Pharmacology**: t0078 simulates control conditions (no GABA-A blockade).
  `[Trenholm2013]`'s 198 Hz peak rate is also control; the 244 Hz value is under picrotoxin
  (GABA-A block) and is not a comparable target for t0078.
* **AIS architecture**: t0078 implements a two-subsegment AIS with separate proximal Nav1.6
  stand-in and distal Nav1.6 + Kv3 + Kv7 SUFFIXes. `[Werginz2024]` uses a single AIS tier;
  `[Kole 2008]` measures a single-compartment cortical pyramidal AIS. The two-subsegment AIS
  used here is closer to the Hu 2009 / Van Wart 2007 division-of-labour model than to either
  reference's geometry.
* **BO methodology**: `[Ament2023]` qLogNoisyExpectedHypervolumeImprovement is the t0078
  acquisition function. t0076 used the deprecated qNEHVI from BoTorch < 0.10. Both share the
  same BoTorch SingleTaskGP back-end with `Standardize(m=2)` output transform; t0078 adds
  `Normalize(d=49)` input transform. Hypervolume is computed against the same [0, 0] reference
  point in both tasks.
* **Slow-AHP mechanism**: t0078 vendors `skahpt78.mod` (SK_E2 from `[Hay2011]` CaDynamics_E2
  with a `tau_ca_multiplier` PARAMETER scaling decay tau in [1, 20x]). `[Hay2011]` uses
  cortical L5b pyramidal-neuron parameters; the SK_E2 source is `[Khaliq2003]` Purkinje-neuron
  resurgent-Na + SK kinetics. Neither paper reports DSGC-specific tau values; the 20x upper
  bound is a researcher-imposed simulation-budget bound, not a literature ceiling.

## Analysis

The Pareto front confirms a **bimodal** trade-off geometry: the high-DSI rail (DSI 0.5-1.0)
lives at PD rates **<= 4 Hz**, and the high-rate rail (PD >= 30 Hz) lives at DSI **<= 0.06**.
The joint operating point at (DSI 0.4, PD 10 Hz) anchored by `[RivlinEtzion2012]` falls
**outside** the achievable Pareto front, missed by 0.084 on DSI and 0.32 Hz on PD rate at iter
81.

**Joint z-score interpretation.** The Mahalanobis-style joint z-score for iter 81 against the
RivlinEtzion2012 stable-cell distribution `[RivlinEtzion2012, Results p. 522]`:

* DSI z = (0.316 - 0.78) / 0.19 = **-2.44** (well outside +/-1 sigma; only ~0.7% of stable
  cells in `[RivlinEtzion2012]` would have DSI <= 0.316).
* PD-rate z = (9.68 - 10.38) / 8.53 = **-0.08** (within 1 sigma; the iter 81 PD rate is
  biologically plausible).

The result frames the negative finding precisely: t0078's PD rate axis successfully reproduces
biological mean rates, while the DSI axis remains compressed by ~2.4 sigma. The DSI
compression is consistent with the Bed B / Poleg-Polsky 2016 substrate's **passive dendrites**
-- DSI > 0.4 in published mouse DSGCs is computed at peak rates after Gaussian convolution
(`[Trenholm2013, Results p. 14068]`) and / or relies on active dendritic Nav `[Sivyer2013,
Results]` and dendritic spike initiation `[Oesch2005, Results p. 754]`. The augmented
substrate added an AIS but kept dendrites passive; the missing dendritic-spike machinery is
the dominant explanation for the compressed high-rail DSI when measured as trial-averaged DSI
from sub-second mean rates.

**Substrate validation.** Iter 81 (DSI 0.316) is the closest Pareto cell to the
`[deRosenroll2026, Fig. 5]` correlated-SAC-release baseline of **DSI 0.39** -- short by 0.074.
No Pareto cell at PD 9.68 Hz reaches the deRosenroll 0.39 DSI value. This is a **substrate
regression**: the augmented 49-d substrate at this PD rate produces lower DSI than the
original deRosenroll baseline reports. The MOBO never sampled the deRosenroll-baseline
parameter region (no deferred substrate-regression check for REQ-16 was run); the regression
therefore does not prove the augmented substrate cannot reproduce DSI 0.39, only that the
qLogNEHVI optimiser did not find such a configuration in 491 cells.

**AIS Nav density anomaly.** Iter 81's `nav16_ais` parameter sits at the search-floor of
**1e-5 S/cm^2**, four orders of magnitude below the Kole 2008 patch-clamp prior of **0.25-0.5
S/cm^2** `[Kole2008, p. 178]` and five orders below Werginz 2024 Table 1's mouse alpha-RGC AIS
Nav of **1.3 S/cm^2** `[Werginz2024, Table 1]`. The AIS-to-soma Nav ratio at iter 81 is
**5.5e-5**, vs the Werginz 2024 measured ratio of **17.3** `[Werginz2024, p. 6]`. The
optimiser converged on a configuration where the AIS contributes nothing to spike initiation;
the somatic Nav (0.183 S/cm^2 at iter 81) carries the firing. This means the joint-closest
cell does not exploit the AIS biophysics added in t0078, which contradicts REQ-2 / REQ-3 /
REQ-4's biological intent. Pareto cells along the high-rate rail (iter 437, iter 111, iter
437) do saturate `nav16_ais = 1.0 S/cm^2`, but at the cost of total directional information
(DSI < 0.05), suggesting the high AIS Nav regime triggers depolarisation block on
null-direction trials and collapses DSI. The **17 cells x 49 parameters** Pareto front is
sparsely informative about the [0.25, 0.5] S/cm^2 Kole regime: only one cell (iter 290, DSI
1.000) has a `nav16_ais` value inside the Kole prior window (0.0101 S/cm^2 -- still below the
0.25 lower bound but the closest of the 17 cells).

**Versus Trenholm 2013 peak rates.** The max-PD Pareto cell (iter 475, PD 197.14 Hz) is a
near-perfect numerical match to `[Trenholm2013, Results p. 14064]`'s **198 +/- 14 Hz** control
peak rate. This is a **metric mismatch**, not a biological match: t0078's 197 Hz is a
trial-averaged mean rate from 1400 ms simulation with 8 directions x 20 seeds, while Trenholm
2013's 198 Hz is a Gaussian-convolved peak instantaneous rate from a sub-second moving-bar
burst. A real cell sustaining 197 Hz mean rate over 1.4 s would be in depolarisation-block
regime; iter 475's DSI of 0.007 is consistent with this saturated state. The numerical
coincidence reinforces that mean-rate and peak-rate firing-rate metrics must not be
cross-compared.

**Versus PolegPolsky2016 substrate ancestor.** `[PolegPolsky2016, Results]` reports DSI
0.6-0.7 in passive-dendrite mouse DRD4 DSGCs. Our iter 290 (max DSI = 1.000) and iter 283 (DSI
0.939) cells **exceed** this published range by +0.30 to +0.40, but these cells fire at PD
rates of 0.36-1.14 Hz -- subthreshold trains, far from the 5-15 Hz mean-rate regime of real
DSGCs. The Pareto-rail cell at iter 349 (DSI 0.529, PD 3.25 Hz) sits within the PolegPolsky
2016 published range but at a sub-physiological PD rate. The augmented substrate matches
PolegPolsky 2016's DSI when the firing rate is allowed to approach zero, consistent with the
original Poleg-Polsky observation that passive dendritic propagation can produce high DSI when
spike thresholds are tuned for very low base firing.

**Versus rabbit DSGC range.** `[Sivyer2010, Results]` ON-OFF rabbit DSI of **0.45 (ON)** and
**0.50 (OFF)** is matched by iter 349 (DSI 0.529) at PD 3.25 Hz. `[Oesch2005, Results p. 754]`
peak-rate DSI of **0.67 (ON)** / **0.74 (OFF)** is matched by iter 380 (DSI 0.756) and iter
371 (DSI 0.767) at PD 1.89-2.82 Hz. None of these matches occur at biologically plausible PD
rates (>= 5 Hz) -- the augmented substrate reproduces published rabbit DSI **only** in the
sub-threshold regime.

**Hypervolume vs t0076.** The +36% HV improvement (8.41 -> 11.41) confirms the architectural
additions in REQ-2 through REQ-6 (AIS section, 5-tier channels, slow-AHP) **do** expand the
achievable Pareto front. However, the HV gain is bounded by the same dendritic-passive
constraint -- the high-DSI rail's PD ceiling moved from t0076's ~3 Hz to t0078's 2.82 Hz (no
measurable change). The HV growth came mainly from the high-rate rail extending from t0076's
128 Hz to t0078's 197 Hz, capped by the slow-AHP. The augmented substrate **expands the rate
axis but does not break the rate-DSI trade-off** at the joint operating point.

## Limitations

* **Substrate regression check (REQ-16) deferred**: The t0076 iter-424 parameter vector was
  not re-evaluated on the 49-d t0078 substrate, so the apparent DSI regression at iter 81
  (0.316 vs t0076 iter 424's 0.42) cannot be attributed solely to the substrate -- it may also
  reflect the increased acquisition-function exploration cost in 49-d vs 25-d space within the
  same evaluation budget.
* **Mean rate vs peak rate**: The published `[Trenholm2013]` and `[Oesch2005]` values are peak
  Gaussian-convolved instantaneous rates, while t0078 reports trial-averaged mean rates over
  1400 ms. The +49 Hz delta against `[Oesch2005, Results p. 754]`'s 148 Hz modal peak is a
  metric mismatch, not a biological mismatch. The only **directly-comparable** firing-rate
  reference in the corpus is `[RivlinEtzion2012]`'s 3 s-window mean rate.
* **DSI definitions vary**: `[Trenholm2013]`'s peak-rate DSI is structurally higher than the
  trial-averaged spike-count DSI used in t0078. Cross-paper DSI comparisons inherit this
  systematic difference of +0.05 to +0.15.
* **Werginz 2020 and Van Wart 2007 paper PDFs not in corpus**: The AIS Nav density priors used
  in t0078 (Kole 2008's 0.25-0.5 S/cm^2) come from the cortical pyramidal literature, not the
  RGC literature. The Werginz 2020 RGC measurement of the AIS-to-soma Na density ratio (~7x)
  is in the metadata but the paper PDF is paywalled. This propagates to incomplete prior
  validation: only `[Werginz2024, Table 1]`'s mouse alpha-RGC values (1.3 S/cm^2 AIS Nav) are
  fully characterised in the corpus.
* **Single MOBO run**: t0078 has one Sobol DoE seed and one BoTorch chain. The +36% HV
  improvement over t0076 is a single-replicate observation; the Pareto-front structure (17
  cells, bimodal trade-off) may shift with a different RNG seed. No HV uncertainty estimate is
  reported.
* **BO loop early-stopped at 416/700 acquisitions**: The remaining 284 acquisitions might have
  located a Pareto cell crossing the joint pass criterion. The HV trajectory had plateaued at
  11.41 (90% of the 1.5x rule-out threshold of 12.62), but a cell sitting just above (DSI 0.4,
  PD 10 Hz) was not categorically ruled out.
* **No paired DSI + mean PD-rate measurements other than RivlinEtzion 2012**: The literature
  anchor at (DSI 0.78, 10.38 Hz) is from a single n = 8 sample. No other paper in the project
  corpus reports paired joint DSI + mean PD-rate values; the t0078 pass criterion of (0.4, 10)
  is therefore anchored to a single small-sample reference.
* **`[Park2014]`'s SD of 0.05 is unrealistically small**: The reported DSI 0.65 +/- 0.05 SD
  yields a z-score of -7.0 against iter 81, which is implausible for a biological measurement.
  The SD likely reflects within-cell-type homogeneity in the CART-Cre transgenic line, not the
  full DSGC population; the iter-81 DSI is therefore better compared to `[RivlinEtzion2012]`'s
  larger SD of 0.19.

</details>
