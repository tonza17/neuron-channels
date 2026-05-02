# Multi-objective Bayesian optimisation of channels + synapse placement on Bed B

## Motivation

The project has two well-characterised DSGC model beds (Bed A: t0008 deposited Poleg-Polsky; Bed B:
t0024 de Rosenroll port) and a thorough understanding of how individual channels and synapse
subsystems behave (t0019 literature survey, t0067 single-channel soma sweep, t0068 co-expression
rescue test, t0069 AIS sweep, t0070/t0071 writeup, t0072 per-synapse traces). None of this work has
yet asked the headline scientific question: **what combination of voltage-gated channels and
synaptic input placement gives the best joint trade-off between direction selectivity (DSI) and
firing rate?** This task answers that for Bed B.

We fix the de Rosenroll morphology (the geometric structure has already been characterised in the
t0029/t0034 dendrite sweeps — it is not the bottleneck for direction selectivity). Channels and
synapses are the search space.

## Scope

* **Cell substrate**: Bed B (t0024 de Rosenroll port). Morphology fixed (1 soma + 350 dendrites,
  10,649 `pt3dadd` points; built once via `build_dsgc_cell()` from the registered
  `de_rosenroll_2026_dsgc` library asset).
* **Search dimensions**: 25 free parameters (see Parameters section).
* **Objectives**: 2 (DSI and PD firing rate) — both maximised.
* **Optimisation algorithm**: multi-objective Bayesian optimisation via BoTorch's qNEHVI acquisition
  function (q-noisy expected hypervolume improvement). Multi-output Gaussian Process surrogate.
* **Compute platform** (REQUIRED): **Vast.ai 64-core CPU node**. Local-workstation execution is not
  acceptable for this task — the optimisation needs ~64-way trial-level parallelism to keep
  per-iteration wall time at ~30 s. The task plan therefore includes the canonical `setup-machines`
  and `teardown` steps; the `/setup-remote-machine` skill provisions the Vast.ai instance, installs
  the project's NEURON + Python environment via the standard `uv sync` flow, runs the optimisation,
  downloads results, and destroys the instance. No work runs on the local workstation beyond
  orchestration of the SSH session.
* **Per-iteration cost**: 8 directions × 20 seeds = 160 trials × ~3 s wall ≈ ~30 s on the Vast.ai
  64-core node (`ProcessPoolExecutor` over trials).
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

Channel kinetics (V_half, τ) are NOT optimised — they are fixed at literature values per t0019, with
MOD files vendored from t0067 (5 channels: Nav1.6, NaP, NaR, Kv3, Kv4) plus 6 new MODs to vendor in
this task (Kdr, KM, HCN, CaL, CaT, BK, SK — see Risks fallback if any prove hard to source).

Reversal potentials (E_Na, E_K, E_Ca, E_GABA) are fixed by physics and NOT optimised.

## Objectives (2)

| Objective | Direction | Definition |
| --- | --- | --- |
| **DSI** (direction selectivity index) | **maximise** | `(spike_pd - spike_nd) / (spike_pd + spike_nd)`, where `spike_pd` and `spike_nd` are mean spike counts across 20 seeds at the preferred direction (0°) and null direction (180°) respectively. Range: [-1, +1]; perfect DSGC ≈ 1. |
| **PD firing rate** | **maximise** | Mean spike count over 1000 ms at the PD direction (0°), averaged across 20 seeds. In Hz: divide by 1.0 s. |

The optimiser produces a **Pareto front** — the set of cell configurations where no other
configuration is simultaneously better on both DSI and firing rate. The user picks the operating
point afterward based on biological constraints (e.g., "I need DSI ≥ 0.7 with firing rate ≥ 30 Hz" →
the Pareto front shows whether that point is achievable and what configuration reaches it).

Although the user is NOT optimising for cytoplasm volume (morphology is fixed → cytoplasm volume is
constant), the task records cytoplasm volume per cell for completeness; it just doesn't enter the
objective function.

## Approach

1. **Vendor 6-7 new MOD files** from canonical published sources (ModelDB, Allen Institute) into
   `code/mods/`: Kdr, KM (Kv7), HCN (Ih), CaL (CaV1.x), CaT (CaV3.x), BK (KCa1.1), SK (KCa2). Plus
   the existing 5 from t0067 (Nav1.6, NaP, NaR, Kv3, Kv4) copied verbatim. Compile to a t0073-local
   `nrnmech.dll`.
2. **Add the `cad` calcium-accumulation mechanism** if not already in the de Rosenroll port (needed
   because BK and SK depend on intracellular [Ca²⁺]).
3. **Write the parametric synapse placer**: given (`N_type`, `ρ_0`, `λ`), draw N positions along the
   dendritic tree with density proportional to `exp(-d/λ)` where `d` is the path distance from the
   soma. Use `sec.distance()` to compute path distance per section midpoint.
4. **Write the trial driver**: takes a 25-d parameter vector → builds the parametric cell → runs 8
   directions × 20 seeds (160 trials) via `ProcessPoolExecutor` over directions × seeds on a 64-core
   CPU → returns (DSI, PD firing rate).
5. **Wire up BoTorch qNEHVI**: 25-d input space, 2-d output space, multi-task GP, qNEHVI acquisition
   with reference point at (DSI=0, rate=0). Initial design-of-experiments: 30 Sobol-sampled cells.
   Optimisation loop: 300-500 acquisition steps.
6. **Plot the Pareto front** at iteration 50, 100, 200, 300, ..., final. Show how the front
   converges. Highlight 3-5 representative cells from the front in detail (parameter values, tuning
   curves, spike rasters, synaptic conductance traces — reusing the t0072 recorder).
7. **Render writeup as markdown + Typst PDF** (consistent with t0070-t0072).

The orchestrator wraps steps 1-7 between a `setup-machines` step (provisions the Vast.ai node,
installs NEURON + uv-managed deps, compiles the t0073 MOD library on the remote) and a `teardown`
step (downloads all results back to the local task folder, destroys the Vast.ai instance, updates
`results/costs.json` and `results/remote_machines_used.json` with the actual billed amount).

## Cost estimation

* **Compute platform**: Vast.ai 64-core CPU instance (no GPU needed — see Risk #2 if 64-core CPU
  nodes are unavailable in the chosen region).
* **External costs**:
  * Vast.ai 64-core CPU node typical pricing: $0.20 - $0.60 / hr (varies by host, region, bid vs
    on-demand).
  * Run duration: 2.5-4 h compute + ~10-20 min provisioning/install + ~5 min teardown.
  * **Expected billed total: $0.75 - $3.00 for the optimisation run**, plus ~$0.10 - $0.30 for the
    provisioning overhead.
  * Budget cap: $5.00 (conservative — if the run exceeds this, the implementation step halts and
    writes an intervention file).
* Disk: ~50-200 MB for raw per-iteration trial summaries (no per-synapse traces saved per iteration
  to keep size down — only the 3-5 best Pareto cells get full traces). Output is rsync-pulled back
  to the local task folder during teardown.
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
* At least 3 representative Pareto cells have full diagnostic traces saved (tuning curve, spike
  raster, synaptic conductances).
* All standard verificators pass.
* The writeup PDF embeds the Pareto front figure and at least 3 representative-cell figures.

## Task Requirement Checklist

* **REQ-1** — 12 voltage-gated channel mechanisms vendored or implemented (or 8 if MOD-vendor
  fallback is invoked, with documented justification).
* **REQ-2** — Parametric synapse placer takes (N, ρ_0, λ) and produces a valid synapse placement
  with the requested density pattern.
* **REQ-3** — Trial driver runs 8 directions × 20 seeds for any 25-d parameter vector and returns
  (DSI, PD firing rate). Handles NaN errors gracefully.
* **REQ-4** — BoTorch qNEHVI optimiser wired up and runs ≥ 300 iterations.
* **REQ-5** — Pareto front + hypervolume trajectory plotted; saved to `results/images/`.
* **REQ-6** — At least 3 representative Pareto cells documented in detail (parameter values, tuning
  curves, spike traces).
* **REQ-7** — `results/results_summary.md` + `results_detailed.md` (with the mandatory sections per
  the results spec) + Typst PDF.
* **REQ-8** — All standard verificators pass.
* **REQ-9** — `pyproject.toml` updated with `botorch`, `gpytorch`, `torch` (and any related deps)
  cleanly.
* **REQ-10** — A documented "next steps" suggestion: tier-stratify the channel densities of the best
  3 Pareto cells and re-optimise locally (extends the search to ~40 dim).
* **REQ-11** — All compute (cell builds, NEURON sims, BoTorch acquisition steps) runs on the Vast.ai
  64-core node, NOT on the local workstation. The local workstation only orchestrates the SSH
  session, holds the task folder, and pulls results back during teardown.
* **REQ-12** — `results/costs.json` records the actual Vast.ai bill (≤ $5.00) and
  `results/remote_machines_used.json` records the instance ID, GPU/CPU specs (no GPU expected),
  hourly rate, total billed time, and provisioning + teardown timestamps.
