# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0078 — <strong>Bed B v2 MOBO with AIS, tier-stratified channels, and
slow Kv-AHP</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0078_bedb_mobo_v2_ais_tiered_ahp` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0076-02` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Task folder** | [`t0078_bedb_mobo_v2_ais_tiered_ahp/`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/) |

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
