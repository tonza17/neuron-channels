# ⏹ Tasks: Not Started

4 tasks. ⏹ **4 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

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
<summary>⏹ 0073 — <strong>Multi-objective BO of channels + synapse placement on
Bed B (max DSI + max firing rate)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0073_bedb_dsi_firing_rate_mobo` |
| **Status** | not_started |
| **Effective date** | 2026-05-02 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Multi-objective BO of channels + synapse placement on Bed B (max DSI + max firing rate)](../../../overview/tasks/task_pages/t0073_bedb_dsi_firing_rate_mobo.md) |
| **Task folder** | [`t0073_bedb_dsi_firing_rate_mobo/`](../../../tasks/t0073_bedb_dsi_firing_rate_mobo/) |

# Multi-objective Bayesian optimisation of channels + synapse placement on Bed B

## Motivation

The project has two well-characterised DSGC model beds (Bed A: t0008 deposited Poleg-Polsky;
Bed B: t0024 de Rosenroll port) and a thorough understanding of how individual channels and
synapse subsystems behave (t0019 literature survey, t0067 single-channel soma sweep, t0068
co-expression rescue test, t0069 AIS sweep, t0070/t0071 writeup, t0072 per-synapse traces).
None of this work has yet asked the headline scientific question: **what combination of
voltage-gated channels and synaptic input placement gives the best joint trade-off between
direction selectivity (DSI) and firing rate?** This task answers that for Bed B.

We fix the de Rosenroll morphology (the geometric structure has already been characterised in
the t0029/t0034 dendrite sweeps — it is not the bottleneck for direction selectivity).
Channels and synapses are the search space.

## Scope

* **Cell substrate**: Bed B (t0024 de Rosenroll port). Morphology fixed (1 soma + 350
  dendrites, 10,649 `pt3dadd` points; built once via `build_dsgc_cell()` from the registered
  `de_rosenroll_2026_dsgc` library asset).
* **Search dimensions**: 25 free parameters (see Parameters section).
* **Objectives**: 2 (DSI and PD firing rate) — both maximised.
* **Optimisation algorithm**: multi-objective Bayesian optimisation via BoTorch's qNEHVI
  acquisition function (q-noisy expected hypervolume improvement). Multi-output Gaussian
  Process surrogate.
* **Compute platform** (REQUIRED): **Vast.ai 64-core CPU node**. Local-workstation execution
  is not acceptable for this task — the optimisation needs ~64-way trial-level parallelism to
  keep per-iteration wall time at ~30 s. The task plan therefore includes the canonical
  `setup-machines` and `teardown` steps; the `/setup-remote-machine` skill provisions the
  Vast.ai instance, installs the project's NEURON + Python environment via the standard `uv
  sync` flow, runs the optimisation, downloads results, and destroys the instance. No work
  runs on the local workstation beyond orchestration of the SSH session.
* **Per-iteration cost**: 8 directions × 20 seeds = 160 trials × ~3 s wall ≈ ~30 s on the
  Vast.ai 64-core node (`ProcessPoolExecutor` over trials).
* **Total compute budget**: 300-500 iterations × ~30 s ≈ **2.5-4 h wall on the Vast.ai 64-core
  node**.

## Parameters (25 free)

| # | Category | Parameter | Range | Notes |
| --- | --- | --- | --- | --- |
| 1-12 | **Channel densities** (`gbar`, S/cm²) | One per channel, log-uniform: Nav1.6, NaP, NaR, Kdr, Kv3, Kv4, KM, HCN, CaL, CaT, BK, SK | 1e-5 - 0.5 | Single density across the cell; tier-stratification deferred. |
| 13 | **Passive** | `Ra` (Ω·cm) | 50 - 250 | Linear |
| 14 | **Passive** | `cm` (µF/cm²) | 0.5 - 2.0 | Linear |
| 15 | **Passive** | `gleak` (S/cm²) | 1e-5 - 1e-3 | Log-uniform |
| 16 | **Calcium** | `cad.depth` (µm) | 0.05 - 0.5 | Internal Ca shell depth |
| 17 | **Calcium** | `cad.taur` (ms) | 5 - 100 | Ca extrusion time constant |
| 18 | **Synapse count** | `N_ACh` (int) | 50 - 350 | Total ACh terminals; default 177 |
| 19 | **Synapse count** | `N_GABA` (int) | 50 - 350 | Total GABA terminals; default 177 |
| 20 | **Synapse spatial rule** | `rho_0_ACh` (rel.) | 0.1 - 5.0 | Density at soma for ρ(d) = ρ_0 · exp(-d/λ) |
| 21 | **Synapse spatial rule** | `lambda_ACh` (µm) | 30 - 500 | Spatial decay length for ACh |
| 22 | **Synapse spatial rule** | `rho_0_GABA` (rel.) | 0.1 - 5.0 | Density at soma for GABA |
| 23 | **Synapse spatial rule** | `lambda_GABA` (µm) | 30 - 500 | Spatial decay length for GABA |
| 24 | **Synapse weight** | `w_ACh` (µS) | 1e-4 - 1e-2 | NetCon weight for ACh; default 0.003 |
| 25 | **Synapse weight** | `w_GABA` (µS) | 1e-4 - 1e-2 | NetCon weight for GABA; default 0.003 |

Channel kinetics (V_half, τ) are NOT optimised — they are fixed at literature values per
t0019, with MOD files vendored from t0067 (5 channels: Nav1.6, NaP, NaR, Kv3, Kv4) plus 6 new
MODs to vendor in this task (Kdr, KM, HCN, CaL, CaT, BK, SK — see Risks fallback if any prove
hard to source).

Reversal potentials (E_Na, E_K, E_Ca, E_GABA) are fixed by physics and NOT optimised.

## Objectives (2)

| Objective | Direction | Definition |
| --- | --- | --- |
| **DSI** (direction selectivity index) | **maximise** | `(spike_pd - spike_nd) / (spike_pd + spike_nd)`, where `spike_pd` and `spike_nd` are mean spike counts across 20 seeds at the preferred direction (0°) and null direction (180°) respectively. Range: [-1, +1]; perfect DSGC ≈ 1. |
| **PD firing rate** | **maximise** | Mean spike count over 1000 ms at the PD direction (0°), averaged across 20 seeds. In Hz: divide by 1.0 s. |

The optimiser produces a **Pareto front** — the set of cell configurations where no other
configuration is simultaneously better on both DSI and firing rate. The user picks the
operating point afterward based on biological constraints (e.g., "I need DSI ≥ 0.7 with firing
rate ≥ 30 Hz" → the Pareto front shows whether that point is achievable and what configuration
reaches it).

Although the user is NOT optimising for cytoplasm volume (morphology is fixed → cytoplasm
volume is constant), the task records cytoplasm volume per cell for completeness; it just
doesn't enter the objective function.

## Approach

1. **Vendor 6-7 new MOD files** from canonical published sources (ModelDB, Allen Institute)
   into `code/mods/`: Kdr, KM (Kv7), HCN (Ih), CaL (CaV1.x), CaT (CaV3.x), BK (KCa1.1), SK
   (KCa2). Plus the existing 5 from t0067 (Nav1.6, NaP, NaR, Kv3, Kv4) copied verbatim.
   Compile to a t0073-local `nrnmech.dll`.
2. **Add the `cad` calcium-accumulation mechanism** if not already in the de Rosenroll port
   (needed because BK and SK depend on intracellular [Ca²⁺]).
3. **Write the parametric synapse placer**: given (`N_type`, `ρ_0`, `λ`), draw N positions
   along the dendritic tree with density proportional to `exp(-d/λ)` where `d` is the path
   distance from the soma. Use `sec.distance()` to compute path distance per section midpoint.
4. **Write the trial driver**: takes a 25-d parameter vector → builds the parametric cell →
   runs 8 directions × 20 seeds (160 trials) via `ProcessPoolExecutor` over directions × seeds
   on a 64-core CPU → returns (DSI, PD firing rate).
5. **Wire up BoTorch qNEHVI**: 25-d input space, 2-d output space, multi-task GP, qNEHVI
   acquisition with reference point at (DSI=0, rate=0). Initial design-of-experiments: 30
   Sobol-sampled cells. Optimisation loop: 300-500 acquisition steps.
6. **Plot the Pareto front** at iteration 50, 100, 200, 300, ..., final. Show how the front
   converges. Highlight 3-5 representative cells from the front in detail (parameter values,
   tuning curves, spike rasters, synaptic conductance traces — reusing the t0072 recorder).
7. **Render writeup as markdown + Typst PDF** (consistent with t0070-t0072).

The orchestrator wraps steps 1-7 between a `setup-machines` step (provisions the Vast.ai node,
installs NEURON + uv-managed deps, compiles the t0073 MOD library on the remote) and a
`teardown` step (downloads all results back to the local task folder, destroys the Vast.ai
instance, updates `results/costs.json` and `results/remote_machines_used.json` with the actual
billed amount).

## Cost estimation

* **Compute platform**: Vast.ai 64-core CPU instance (no GPU needed — see Risk #2 if 64-core
  CPU nodes are unavailable in the chosen region).
* **External costs**:
  * Vast.ai 64-core CPU node typical pricing: $0.20 - $0.60 / hr (varies by host, region, bid
    vs on-demand).
  * Run duration: 2.5-4 h compute + ~10-20 min provisioning/install + ~5 min teardown.
  * **Expected billed total: $0.75 - $3.00 for the optimisation run**, plus ~$0.10 - $0.30 for
    the provisioning overhead.
  * Budget cap: $5.00 (conservative — if the run exceeds this, the implementation step halts
    and writes an intervention file).
* Disk: ~50-200 MB for raw per-iteration trial summaries (no per-synapse traces saved per
  iteration to keep size down — only the 3-5 best Pareto cells get full traces). Output is
  rsync-pulled back to the local task folder during teardown.
* Time:
  * MOD vendoring + driver code (local human time): ~6-10 h.
  * Optimisation run on Vast.ai 64-core: ~2.5-4 h wall, billed.
  * Plotting + analysis + PDF (local human time, post-teardown): ~2-3 h.
  * Total: ~12-18 h human-time + ~$1-3 cloud spend.

## Dependencies

* `t0008_port_modeldb_189347` — Bed B reuses Poleg-Polsky's morphology.
* `t0019_literature_survey_voltage_gated_channels` — V_half / τ priors for the 12 channels.
* `t0024_port_de_rosenroll_2026_dsgc` — Bed B itself; entry point `build_dsgc_cell()`.
* `t0066_t0024_epsp_ipsp_vm_protocol` — direction-encoding mechanism on Bed B (bar angle).
* `t0067_t0065_soma_channel_addition_sweep` — provides 5 vendored MODs to copy verbatim.
* `t0070_writeup_two_model_beds` — reference writeup (cite for context).
* `t0072_synaptic_traces_pd_nd` — per-synapse recorder pattern + Typst PDF pipeline.

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | One or more of the 6 new MOD files (Kdr, KM, HCN, CaL, CaT, BK, SK) cannot be sourced from a clean published implementation. | Vendor step fails on a specific channel. | Drop to 8 channels (HHst's built-in Na/Kdr/leak + the 5 t0067 channels) and document the reduction in the writeup. The optimisation framework (BoTorch + driver) doesn't care about the channel count — only the parameter dimension changes. |
| 2 | Vast.ai has no 64-core CPU node available in the requested region/price tier at provisioning time. | `setup-machines` step's instance search returns 0 matches. | Try adjacent regions; relax the price cap (typical 64-core nodes are $0.20-$0.60/hr); or accept a 32-core node (run wall doubles to ~5-8 h, still tractable). Do NOT fall back to local-workstation execution — this task is explicitly cloud-compute. If no remote node is available within the $5 budget cap, write an `intervention/` file and stop. |
| 3 | BoTorch qNEHVI fails to converge in 500 iterations (Pareto front still expanding). | Manually inspect the front at iter 100, 200, 400; check the hypervolume metric for monotonic increase. | Switch to NSGA-II via DEAP/pymoo (more iterations needed but more robust). Cap at 5000 trials. |
| 4 | Calcium dynamics make the cell numerically unstable at extreme channel-density combinations. | Trial errors out with NaN voltage or NEURON solver complaint. | Catch the exception, return a worst-case score (DSI = -1, rate = 0) so the optimiser learns to avoid that region. |
| 5 | Stochastic per-trial noise on DSI is large enough that the GP can't learn (DSI estimates have SE > 0.1). | High GP residual variance after 50 iterations. | Increase seeds per direction from 20 to 40 (doubles per-iteration time). Or use a noise-aware GP kernel (BoTorch's HeteroscedasticGP). |
| 6 | The parametric synapse placer (exponential decay) is too restrictive; the optimal cell needs a non-monotonic spatial pattern. | Best-Pareto cells cluster at parameter-bound extremes. | Add a quadratic term to the spatial rule (`ρ(d) = ρ_0 · exp(-d/λ) · (1 + α · d²)`) — adds 2 params per type, total dim = 29. |
| 7 | Adding `botorch` + `gpytorch` + `torch` to `pyproject.toml` is a large dependency footprint (~2 GB). | uv sync slow / disk concern. | Acceptable cost for the gain; document in the writeup. Alternative: use Ax (lighter wrapper around BoTorch) or scikit-optimize (much smaller, less powerful). |

## Verification criteria

* All 25 free parameters have explicit log/linear bounds documented.
* The driver handles a NaN/error trial gracefully (worst-case-score fallback).
* The Pareto front contains at least 5 distinct cell configurations after 200 iterations.
* Hypervolume metric is monotonically increasing across iterations (modulo small noise).
* At least 3 representative Pareto cells have full diagnostic traces saved (tuning curve,
  spike raster, synaptic conductances).
* All standard verificators pass.
* The writeup PDF embeds the Pareto front figure and at least 3 representative-cell figures.

## Task Requirement Checklist

* **REQ-1** — 12 voltage-gated channel mechanisms vendored or implemented (or 8 if MOD-vendor
  fallback is invoked, with documented justification).
* **REQ-2** — Parametric synapse placer takes (N, ρ_0, λ) and produces a valid synapse
  placement with the requested density pattern.
* **REQ-3** — Trial driver runs 8 directions × 20 seeds for any 25-d parameter vector and
  returns (DSI, PD firing rate). Handles NaN errors gracefully.
* **REQ-4** — BoTorch qNEHVI optimiser wired up and runs ≥ 300 iterations.
* **REQ-5** — Pareto front + hypervolume trajectory plotted; saved to `results/images/`.
* **REQ-6** — At least 3 representative Pareto cells documented in detail (parameter values,
  tuning curves, spike traces).
* **REQ-7** — `results/results_summary.md` + `results_detailed.md` (with the mandatory
  sections per the results spec) + Typst PDF.
* **REQ-8** — All standard verificators pass.
* **REQ-9** — `pyproject.toml` updated with `botorch`, `gpytorch`, `torch` (and any related
  deps) cleanly.
* **REQ-10** — A documented "next steps" suggestion: tier-stratify the channel densities of
  the best 3 Pareto cells and re-optimise locally (extends the search to ~40 dim).
* **REQ-11** — All compute (cell builds, NEURON sims, BoTorch acquisition steps) runs on the
  Vast.ai 64-core node, NOT on the local workstation. The local workstation only orchestrates
  the SSH session, holds the task folder, and pulls results back during teardown.
* **REQ-12** — `results/costs.json` records the actual Vast.ai bill (≤ $5.00) and
  `results/remote_machines_used.json` records the instance ID, GPU/CPU specs (no GPU
  expected), hourly rate, total billed time, and provisioning + teardown timestamps.

</details>

<details>
<summary>⏹ 0045 — <strong>CoreNEURON Vast.ai RTX 4090 speedup benchmark</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0045_coreneuron_vastai_speedup_benchmark` |
| **Status** | not_started |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0033-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`baseline-evaluation`](../../../meta/task_types/baseline-evaluation/) |
| **Task page** | [CoreNEURON Vast.ai RTX 4090 speedup benchmark](../../../overview/tasks/task_pages/t0045_coreneuron_vastai_speedup_benchmark.md) |
| **Task folder** | [`t0045_coreneuron_vastai_speedup_benchmark/`](../../../tasks/t0045_coreneuron_vastai_speedup_benchmark/) |

# CoreNEURON Vast.ai RTX 4090 Speedup Benchmark

## Source Suggestion

S-0033-01 (CoreNEURON Vast.ai RTX 4090 benchmark to validate or replace the assumed 5x speedup
in the t0033 cost model).

## Motivation

The t0033 planning task estimated a $50.54 central Vast.ai budget for the future joint DSGC
morphology + top-10 VGC DSI-maximisation optimiser. That estimate rests on an unvalidated
CoreNEURON-on-GPU-over-stock-CPU-NEURON speedup factor of 5x (91 s deterministic sim on RTX
4090 vs 456 s on single CPU core). The corpus documents Hines 1997 O(N) cable-solver scaling
but predates GPU NEURON variants, so the 5x figure is a literature-less guess that drives the
largest sensitivity-band column ($23–$119 under 0.5x–2x perturbations).

Brainstorm session 8 (t0040) considered offloading t0041–t0044 to Vast.ai to cut wall-clock,
and rejected that plan because the per-task compute is small and the 5x speedup is
unvalidated. This task directly addresses the validation gap: run a short, well-scoped Vast.ai
experiment that replaces the 5x assumption with a measured value and tightens (or widens) the
$23–$119 sensitivity band before the joint optimiser is commissioned.

This also exercises the project's Vast.ai provisioning workflow for the first time (total
project spend to date: $0.00 / $1.00), surfacing any setup issues before the far more
expensive t0033 optimiser run.

## Objective

Provision one Vast.ai RTX 4090 instance under the existing `setup-remote-machine` filters.
Build CoreNEURON against NEURON 8.2.7 with OpenACC / CUDA. Run the t0022 deterministic
12-angle x 10-trial protocol (same sim used in t0022 baseline) under:

1. Stock NEURON on CPU (single core).
2. CoreNEURON on GPU (RTX 4090).

Report wall-clock per sim, throughput (sims/hour), measured speedup factor, cost per sim in
USD at RTX 4090 Vast.ai rate, and a recommended replacement value for t0033's 5x assumption.
Produce one answer asset capturing the measured speedup and its implications for the t0033
cost envelope.

## Scope

* One Vast.ai RTX 4090 instance. Estimated wall-clock 1–3 h; estimated cost $2–5 at $0.50/h.
* Use t0022's `trial_runner` unchanged; do not modify biophysics or protocol.
* Match stock-NEURON and CoreNEURON runs trial-for-trial for apples-to-apples comparison.
* Record provisioning time and setup friction separately so the t0033 plan can budget for it.

## Out of Scope

* Multi-GPU scaling (t0033 assumes single-GPU).
* A100 / H100 benchmarks (cost column in t0033 already recomputes from measured RTX 4090
  speedup).
* CPU-96 many-core benchmark (t0033 already recommends ignoring that column).
* Any morphology or channel modifications (pure runtime benchmark).

## Deliverables

* `assets/answer/coreneuron-rtx4090-speedup-vs-stock-neuron/` — full answer asset with
  measured speedup, per-sim cost, and recommended t0033 budget update.
* `results/results_summary.md` and `results/results_detailed.md` with Methodology, Metrics,
  Comparison vs Baselines (5x assumption), and Next Steps.
* `results/metrics.json` with: `stock_neuron_s_per_sim`, `coreneuron_s_per_sim`,
  `speedup_factor`, `coreneuron_usd_per_sim`, `provisioning_minutes`, `setup_minutes`.
* `results/compare_literature.md` comparing the measured speedup to Hines 1997 cable-solver
  scaling expectations and any CoreNEURON GPU benchmarks found in the corpus.
* `results/suggestions.json` with at minimum a follow-up proposing a correction to t0033's
  answer asset if the measured speedup differs from 5x by more than 20%.
* `results/costs.json` and `results/remote_machines_used.json` with the full Vast.ai
  provisioning record.

## Anticipated Risks

* **Vast.ai provisioning may fail or block on verification**: the project has never
  provisioned a Vast.ai instance; the `setup-remote-machine` skill may hit unexpected
  friction. Budget extra time for first-run troubleshooting and record every setup step for
  future tasks.
* **CoreNEURON build may require NEURON 8.2.7 patch or a newer version**: if CoreNEURON does
  not build cleanly against the project's NEURON version, document the workaround or flag the
  task as intervention_blocked rather than silently bumping the NEURON version.
* **Deterministic-reproducibility caveat**: stock NEURON on CPU and CoreNEURON on GPU may not
  produce bit-identical spike trains due to floating-point ordering differences; report the
  max-spike-time-deviation and any DSI delta explicitly so the t0033 optimiser knows whether
  GPU and CPU runs are substitutable.
* **Cost overrun**: hard-cap the instance runtime at 3 hours. If the benchmark cannot finish
  within the cap, post-mortem the provisioning and setup overhead and re-scope before a second
  attempt.

## Verification Criteria

* `measured_speedup_factor` is reported with both mean and 95% CI.
* `coreneuron_usd_per_sim` is reported at the actual Vast.ai instance rate at runtime (not the
  snapshot rate from t0033).
* At least one answer asset is produced per the answer specification.
* If the measured speedup differs from 5x by more than 20%, a correction-proposal suggestion
  is filed in `results/suggestions.json` against t0033's answer asset.

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
