# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0080 — <strong>Bed B v3 MOBO with dendritic-spike machinery and
NSGA-II</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0080_bedb_mobo_v3_dendritic_spike_nsga2` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Expected assets** | 1 library, 1 answer |
| **Source suggestion** | `S-0078-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [Bed B v3 MOBO with dendritic-spike machinery and NSGA-II](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Task folder** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2/`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/) |

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

<details>
<summary>⏹ 0075 — <strong>Biologically-realistic AIS one-axis-at-a-time parameter
sweep on Bed A</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0075_bio_realistic_ais_param_sweep` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0069-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Biologically-realistic AIS one-axis-at-a-time parameter sweep on Bed A](../../../overview/tasks/task_pages/t0075_bio_realistic_ais_param_sweep.md) |
| **Task folder** | [`t0075_bio_realistic_ais_param_sweep/`](../../../tasks/t0075_bio_realistic_ais_param_sweep/) |

# Biologically-Realistic AIS Parameter Sweep on Bed A

## Motivation

t0069 attached a virtual AIS plus 1 mm axon stub to Bed A (deposited Poleg-Polsky DSGC) and
re-ran the t0067 channel-addition sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} on the AIS
instead of the soma. The sweep falsified S-0067-03's prediction (AIS-localised channels show
*larger* DSI effects than soma-localised) — it actually showed the opposite, with 11 of 15
channel conditions producing zero detectable DSI change. The cause was identified clearly: the
AIS+axon halved baseline PD firing (14.2 → 6.4 spikes) and silenced ND firing (1.6 → 0.0),
pushing baseline DSI to the trivial computational ceiling 1.0. The passive AIS+axon adds an
electrical sink that quenches the cell rather than relocating spike initiation; AIS-localised
channels at our densities cannot overcome the somatic 400 mS/cm² HHst Na drive.

The follow-up question this task answers: is there *any* DSGC + AIS configuration that
simultaneously contains all the channels biologically present in a vertebrate AIS (HHst basal
Na+K, Nav1.6, Kv3, Kv7 — the canonical RGC AIS quartet) and produces non-trivial DSI at a
biologically reasonable peak rate? "Decent DSI, not 1, and reasonable firing rate" maps to the
operational pass band {DSI in [0.3, 0.95], peak Hz in [5, 50]}. The right tool is not
optimisation — it is one axis at a time. NaP is excluded from the AIS channel set on two
grounds: (a) AIS NaP expression in RGCs is controversial; (b) the t0067 NaP-high finding (DSI
sign flip) suggests NaP destabilises the DSI mechanism rather than supporting it. BK and SK
are excluded because they localise primarily to soma and dendrites in RGCs, not to the AIS.

This task addresses RQ1 (somatic + AIS VGC combinations) and RQ4 (active vs passive
components). Source suggestions covered: S-0068-04 (move Nav1.6 + Kv3 to AIS), S-0069-01
(halve somatic gnabar before AIS), S-0069-02 (shrink AIS diameter to 0.5 micrometre),
S-0069-03 (vary axon length to probe sink), S-0069-04 (Nav1.6 + Kv3 on AIS at biological
densities).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC) plus virtual AIS + axon stub.
* AIS channel set: **{HHst basal Na + K, Nav1.6, Kv3, Kv7}**. NaP, BK, SK explicitly excluded.
* Encoding: 12-angle bar-rotation protocol (same as t0074 — cross-task comparable).
* Two-stage design: Stage 1 baseline calibration; Stage 2 per-axis sweep.

### Stage 1 — Baseline calibration

* Literature-informed AIS configuration (Wang et al. 2011, Carter et al. 2008 on mouse RGC
  AIS): AIS diameter 0.8 micrometre, AIS length 30 micrometre, axon stub 1.0 mm, AIS
  gnabar_HHst 4 0 0 mS/cm^2, AIS Nav1.6 medium density (~0.3 S/cm^2 from t0067 medium), AIS
  Kv3 medium density (~0.3 S/cm^2), AIS Kv7 low density (~0.1 S/cm^2; distal AIS, weaker than
  Nav and Kv3).
* Sweep soma `gnabar_HHst` across 6 candidates: {100, 150, 200, 250, 300, 400} mS/cm^2 (the
  t0069 baseline = 400).
* 6 candidates x 12 angles x 1 seed = 72 trials, ~5 min wall-clock.
* Pick the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]}. If multiple
  candidates qualify, pick the one closest to the centre of the band ({peak ~ 20 Hz, DSI ~
  0.6}).
* If no candidate qualifies, the task halts at Stage 1 and reports a negative result with a
  recommendation for a follow-up that loosens the AIS configuration further (e.g., reduce AIS
  Nav1.6 density first, then re-attempt).

### Stage 2 — Per-axis sweep

From the Stage-1 baseline, vary one parameter at a time with all others held at baseline:

| # | Axis | Values | Non-baseline points |
| --- | --- | --- | --- |
| 1 | Soma `gnabar_HHst` (mS / cm^2) | {100, 200, 300, 400} | 3 |
| 2 | AIS `gnabar_HHst` (mS / cm^2) | {0, 100, 200, 400, 800} | 4 |
| 3 | AIS diameter (micrometre) | {0.4, 0.6, 0.8, 1.0, 1.5} | 4 |
| 4 | AIS length (micrometre) | {15, 30, 45, 60} | 3 |
| 5 | AIS Nav1.6 density | {0, low, medium, high} | 3 |
| 6 | AIS Kv3 density | {0, low, medium, high} | 3 |
| 7 | AIS Kv7 density | {0, low, medium, high} | 3 |
| 8 | Axon length (mm) | {0.1, 0.5, 1.0, 2.0} | 3 |

Total Stage-2 conditions: 1 baseline + 26 non-baseline = **27 conditions x 12 angles x 5 seeds
= 1620 FULL trials**, ~100 min wall-clock at the t0067 measured ~3.75 s / trial under CVODE.

### Width metrics per axis (cross-comparable with t0074)

For each condition, compute:

* **HWHM** in degrees from the 12-angle tuning curve.
* **Vector-sum DSI** (circular concentration).
* **Peak rate (Hz)** at the angle with maximum mean rate.
* Rate at PD (axis-1 peak angle) and at the opposite angle.
* RMSE vs the t0004 cosine target.

### Outputs

* **Library asset**: `bed_a_with_bio_realistic_ais` — Bed A + AIS + axon model variant with
  the {HHst, Nav1.6, Kv3, Kv7} channel set wired in. Reusable by future tasks that need a
  working DSGC + AIS substrate.
* **Stage 1 candidate table** (`results/baseline_candidates.csv`) with 6 rows showing
  soma_gnabar_HHst, peak Hz, DSI, in-band y/n.
* **Stage 2 per-axis sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI,
  peak rate, RMSE vs cosine target, plotted against axis values.
* **Biologically-plausible AIS recommendation table**
  (`results/biological_ais_recommendation.md`): the band-constrained range for each axis (the
  values that keep the cell inside {DSI [0.3, 0.95], peak [5, 50] Hz}), plus a recommended
  canonical configuration.
* `results/metrics.json` with registered project metrics per condition.

## Approach

1. Fork t0069's AIS-attachment code into this task's `code/`. Replace the t0069
   channel-addition loop with the {HHst, Nav1.6, Kv3, Kv7} baseline channel set (with
   t0074-vendored Kv7).
2. Implement Stage 1 calibration as a 6-candidate sweep with explicit pass-band check and
   automated baseline selection.
3. Implement Stage 2 as 8 per-axis sweep functions sharing a common driver.
4. Run Stage 1, log selected baseline, run Stage 2.
5. Compute width metrics, generate per-axis plots, write the recommendation table.
6. Validate against t0069 sanity checks: trials with instability flags = 0, peak Vm bounded.

## Pass Criteria

* Stage 1 finds at least one in-band baseline (peak Hz in [5, 50] AND DSI in [0.3, 0.95]).
* All 1620 + 72 trials complete with no instability flags.
* Per-axis sensitivity plots show monotonic or unimodal sensitivity for at least 6 of the 8
  axes (the axes that don't are flagged as candidates for re-investigation; not a hard fail).
* Recommendation table produced with the band-constrained range for each axis.

## Compute Estimate

* ~2 h wall-clock on local CPU. 72 trials Stage 1 (~5 min) + 1620 trials Stage 2 (~100 min) +
  ~10 min plotting / metrics extraction.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code (Nav1.6, Kv3
  implementation patterns).
* `t0069_t0067_ais_localised_channel_sweep` — AIS attachment code; baseline characterisation
  of the passive-AIS sink effect.
* `t0074_channel_tuning_width_bed_a` — Kv7 MOD vendoring lands in t0074. This task inherits
  the vendored Kv7 mechanism and the calcium-pool unification (the latter is not actively used
  here but must remain compatible).

## Risks and Fallbacks

* **Stage 1 finds no in-band baseline**: the task halts after Stage 1 and reports a negative
  result with a follow-up recommendation. Time-cheap (~5 min). The follow-up would probably be
  a 2D Stage 1.5 sweep over {soma gnabar, AIS gnabar} or a baseline that further reduces AIS
  Nav1.6 density.
* **Stage 1 is over-fitted to soma_gnabar**: if the baseline soma_gnabar value is borderline
  (e.g., exactly at the edge of the in-band region), small parameter changes in Stage 2 may
  push the cell out of band rapidly. Mitigation: pick the Stage-1 baseline closest to the band
  centre, not the band edge.
* **Axes interact strongly**: the one-axis-at-a-time design assumes weak interactions. If a
  Stage-2 axis sweep produces non-monotonic behaviour (e.g., DSI rises then falls), report the
  non-monotonicity explicitly and flag the axis for a future joint sweep with one neighbouring
  axis.
* **AIS+axon discretisation artefacts**: if the segment count along the AIS or axon is too
  low, spike initiation and propagation may be artefactual. Mitigation: use NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) and validate that the
  chosen segment count doubles without changing peak Vm by more than 1 mV at the t0069
  baseline.

## Out of Scope

* Bed B (de Rosenroll) — explicitly out of scope per researcher decision; this task is Bed A
  only.
* Joint multi-axis optimisation — explicitly excluded; this is one-axis-at-a-time only.
* Other AIS channel candidates (Nav1.2, Kv1, Kv4 alpha-DTX-sensitive subtype) — out of scope;
  the channel set is fixed at {HHst, Nav1.6, Kv3, Kv7}. Future follow-ups may extend the
  channel set.

</details>

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
