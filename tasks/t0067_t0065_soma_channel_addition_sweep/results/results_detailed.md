---
spec_version: "2"
task_id: "t0067_t0065_soma_channel_addition_sweep"
date: "2026-05-01"
---
# Detailed Results: Add 5 voltage-gated channels to the t0065 soma; sweep densities

## Summary

Added each of {Nav1.6, NaP, NaR, Kv3, Kv4} to the deposited Poleg-Polsky DSGC soma at three
densities (low/med/high, factor of ~3 between levels), one channel per experiment. Ran 160 FULL-mode
gabaMOD-swap trials (16 conditions × 2 directions × 5 seeds) in ~10 minutes wall-clock. Headline:
NaP at high density inverts direction selectivity (DSI = -0.18); Nav1.6 monotonically erodes DSI
from 0.80 to 0.23 across the density grid; NaR / Kv3 / Kv4 produce only small DSI changes (within
±0.1 of the baseline 0.80).

## Methodology

* **Cell model**: deposited Poleg-Polsky 2016 DSGC, exactly as in t0008 / t0065. No changes to
  dendrites, synapses, or the existing HHst mechanism on the soma.
* **Channel-isolation strategy**: 5 mechanisms (`nav16t67`, `napt67`, `nart67`, `kv3t67`, `kv4t67`)
  all inserted on the soma at startup with `gbar = 0`; per trial, only the active channel's `gbar`
  is set to the target density (others stay at 0). This guarantees identical cell topology across
  all 160 trials — only one density value differs between conditions.
* **Mechanism kinetics**:
  * Nav1.6: m^3·h, V_half_act = -43 mV, V_half_inact = -65 mV, τ_m = 0.05 ms, τ_h voltage-
    dependent (Carter & Bean 2009).
  * NaP: m^1, V_half = -50 mV, τ_m = 1 ms, no inactivation (Magistretti & Alonso 1999).
  * NaR: m^3·h·s, with slow `s` gate that recovers around -50 mV (simplified Khaliq-Raman 2003).
  * Kv3: m^4, V_half = -15 mV, τ_m = 1 ms (Erisir 1999).
  * Kv4: m^4·h, V_half_act = -50 mV, V_half_inact = -78 mV, τ_h = 15 ms (Hoffman 1997).
  * All use `NONSPECIFIC_CURRENT i` (no USEION) to avoid ion-accumulation conflicts with the
    existing HHst.
* **Direction encoding**: `h.gabaMOD = 0.33` (PD) or `0.99` (ND), per t0020 / t0065.
* **Per-trial sequence**:
  `apply_params(seed) → set gabaMOD → exptype = 1 → init_active() → update() → placeBIP() → set active channel gbar → finitialize(-65) → continuerun(1000) → count spikes via NetCon @ -10 mV threshold`.
* **Failure-mode policy**: peak Vm > +60 mV or < -80 mV → `is_unstable = true`. No trial was
  flagged.
* **Compute**: local Windows workstation, single CPU core, NEURON 8.2.7. ~10 min for 160 trials.
* **Timestamps**: implementation 2026-05-01T00:22-00:35Z; results 2026-05-01T00:35-00:55Z.

## Per-condition Metrics Table

| Condition | Channel | Density (mS/cm²) | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI | Δ DSI vs baseline |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | none | 0 | **14.2 ± 1.9** | **1.6 ± 1.3** | **0.797** | (reference) |
| nav16_low | Nav1.6 | 10 | 18.2 ± 2.9 | 2.6 ± 1.5 | 0.750 | -0.05 |
| nav16_med | Nav1.6 | 30 | 26.8 ± 3.6 | 9.4 ± 2.6 | 0.481 | -0.32 |
| nav16_high | Nav1.6 | 90 | 57.4 ± 2.9 | 36.0 ± 3.1 | 0.229 | -0.57 |
| nap_low | NaP | 0.3 | 23.6 ± 1.1 | 13.0 ± 2.1 | 0.290 | -0.51 |
| nap_med | NaP | 0.8 | 36.4 ± 2.1 | 28.8 ± 1.3 | 0.117 | -0.68 |
| nap_high | NaP | 2.4 | 66.8 ± 4.1 | **95.8 ± 3.5** | **-0.179** | **-0.98 (sign flip)** |
| nar_low | NaR | 3 | 14.6 ± 2.3 | 1.8 ± 1.3 | 0.780 | -0.02 |
| nar_med | NaR | 8 | 14.8 ± 2.4 | 2.0 ± 1.2 | 0.762 | -0.03 |
| nar_high | NaR | 24 | 16.4 ± 2.4 | 2.8 ± 1.9 | 0.708 | -0.09 |
| kv3_low | Kv3 | 7 | 14.4 ± 2.2 | 1.6 ± 1.3 | 0.800 | +0.00 |
| kv3_med | Kv3 | 20 | 14.6 ± 2.3 | 1.6 ± 1.3 | 0.802 | +0.00 |
| kv3_high | Kv3 | 60 | 16.0 ± 2.7 | 1.6 ± 1.3 | 0.818 | +0.02 |
| kv4_low | Kv4 | 4 | 14.0 ± 1.9 | 1.6 ± 1.3 | 0.795 | -0.00 |
| kv4_med | Kv4 | 12 | 14.0 ± 1.9 | 1.6 ± 1.3 | 0.795 | -0.00 |
| kv4_high | Kv4 | 36 | 13.6 ± 2.3 | 1.4 ± 0.9 | 0.813 | +0.02 |

## Comparison vs t0065 Baseline

* t0065 single-seed baseline: PD = 15 spikes, ND = 1 spike, DSI = 0.875.
* t0067 5-seed baseline: PD = 14.2 ± 1.9, ND = 1.6 ± 1.3, DSI = 0.797.
* The 5-seed mean is lower than the t0065 single-seed point estimate (DSI 0.797 vs 0.875),
  consistent with stochastic spike-count fluctuations across seeds and the slight ND-spike
  background (1.6 vs 1).

## Visualisations

### Firing rate vs density

![Firing rate vs added-channel density](images/firing_rate_vs_density.png)

5 panels (one per channel). Solid lines = mean ± SD across 5 seeds; dashed lines = baseline PD/ND
for reference. Nav1.6 and NaP show monotonic firing-rate increases in BOTH directions across
density. NaR, Kv3, Kv4 hover near the baseline.

### DSI vs density

![DSI vs added-channel density](images/dsi_vs_density.png)

5 panels (one per channel). Green line + markers = DSI per density level; black dashed = the t0067
baseline DSI = 0.80. Nav1.6 and NaP show steep monotonic DSI decreases (NaP crosses 0 between med
and high); NaR shows a small monotonic decrease; Kv3/Kv4 are essentially flat.

### Spike count heatmap

![Spike count heatmap, channel × density grid](images/spike_count_heatmap.png)

Two side-by-side heatmaps: PD spike count (red) and ND spike count (blue). Cell labels show the mean
spike count. The PD panel grows monotonically with density for Nav1.6 and NaP. The ND panel grows
even more steeply for NaP (95.8 spikes at high density vs 1.6 baseline), which is why the DSI
inverts.

## Analysis & Discussion

### Why does NaP invert DSI at high density?

NaP is non-inactivating: once threshold is crossed, the channel stays open and provides a sustained
inward current. In FULL/PD trials, the cell already fires ~14 APs riding on a ~25 mV depolarising
EPSP envelope, and the inhibitory shunt is weak (gabaMOD = 0.33). Adding NaP at 2.4 mS/cm² lifts
the resting depolarisation enough that the cell fires 67 spikes — a ~5× increase.

In FULL/ND trials, the strong inhibitory shunt (gabaMOD = 0.99) was previously suppressing firing to
~1.6 spikes. But NaP's persistent depolarisation now overcomes the shunt: every time excitation
arrives, NaP keeps the cell above threshold for the entire EPSP duration, and the ND direction's
*longer* effective EPSP window (because of the slower inhibitory release pattern) actually produces
MORE spikes than PD. The result: ND fires 95.8, PD fires 66.8, DSI = -0.18.

This is biologically meaningful: persistent Na+ in DSGCs is known to be tightly regulated, and
elevated NaP from disease (e.g., in some channelopathies) could indeed scramble direction
selectivity. Worth flagging as a follow-up topic.

### Why does Nav1.6 erode DSI without flipping it?

Nav1.6 inactivates fast (V_half_inact = -65 mV, τ_h ~1-8 ms). It boosts the cell's spike-generation
capacity by lowering threshold (V_half_act = -43 mV, vs HHst's ~-30 mV) and by adding peak
conductance for AP upstrokes. But it cannot sustain depolarisation between spikes the way NaP does,
so:

* PD firing scales monotonically (14 → 18 → 27 → 57) — more APs per train at higher density.
* ND firing scales even faster proportionally (1.6 → 2.6 → 9.4 → 36) — ND was previously
  near the threshold cutoff, so adding Nav1.6 brings it past threshold for spike generation.
* Net DSI drops 0.80 → 0.75 → 0.48 → 0.23 monotonically.

DSI doesn't invert because both directions still feel the gabaMOD differential — the ND inhibition
is still 3× stronger and produces fewer spikes than PD at every density. But Nav1.6 narrows the
absolute gap.

### Why are NaR / Kv3 / Kv4 nearly inert?

Three plausible reasons:

1. **Density mismatch with the existing HHst**: the deposited cell already has 400 mS/cm² somatic
   gnabar_HHst and ~120 mS/cm² gkbar_HHst (RGCsomak). Our added 3-90 mS/cm² of "extra" channel is
   a small fraction of the existing total.
2. **Kinetic regime**: NaR's resurgent re-opening only matters in high-frequency spike trains (>100
   Hz), but the cell tops out at ~14-67 Hz here. Kv3 and Kv4 act on AP shape and recovery, but the
   t0065 stimulus isn't pushing the cell hard enough to expose AP-shape limits.
3. **NONSPECIFIC_CURRENT simplification**: our MODs use simple HH-style kinetics from published
   V_half / time constants, but don't capture every subtlety of the original models. A more faithful
   re-implementation (especially for NaR's blocking-particle mechanism) might show stronger effects.

### Limitations of this analysis

* **Somatic insertion only**: real RGCs localise Nav1.6 / Kv3 to the AIS, not the soma. The
  deposited cell has no AIS. Putting these channels on the soma is a simplification that likely
  understates their effect on AP initiation timing.
* **One-channel-at-a-time**: real DSGCs co-express multiple Na and K subtypes. The interactions
  (e.g., Nav1.6 + Kv3 jointly enabling fast-spiking) cannot be captured by testing each channel
  alone.
* **Single density grid (3 points)**: we sampled 3 densities per channel; finer grids may reveal
  threshold-crossing behaviours not visible here (e.g., where DSI inversion occurs for NaP).
* **gabaMOD-swap protocol**: direction selectivity is encoded as a per-trial scalar, not spatially.
  Channels that affect spike timing (NaR, Kv3) may matter more in protocols where direction is
  encoded in spike-time differences.

## Examples

Each of the 160 trials is a complete input-output pair. 6 representative single-trial examples
below: 1 baseline + 5 maximum-effect (one per channel at high density).

### Example 1 — baseline FULL/PD seed=1

Input parameters:

```text
gabaMOD = 0.33               # PD
exptype = 1                  # HH on (FULL)
gbar_nav16t67 = 0
gbar_napt67   = 0
gbar_nart67   = 0
gbar_kv3t67   = 0
gbar_kv4t67   = 0
seed = 1, tstop = 1000 ms
```

Output: peak_v_mv = +43.18 mV, baseline_v_mv = -60.02 mV, **spike_count = 15** (matches t0065
exactly).

### Example 2 — nav16_high FULL/PD seed=1

Input: same as Example 1 but `gbar_nav16t67 = 0.090 S/cm² (90 mS/cm²)`. Output: peak_v_mv = +44.0
mV, **spike_count = 57** — adding 90 mS/cm² of Nav1.6 nearly quadruples the PD spike count.

### Example 3 — nap_high FULL/PD seed=1

Input: baseline + `gbar_napt67 = 0.0024 S/cm² (2.4 mS/cm²)`. Output: peak_v_mv ~+44 mV,
**spike_count = 67** — persistent Na drives sustained depolarisation, sustained firing.

### Example 4 — nap_high FULL/ND seed=1

Input: same as Example 3 but `gabaMOD = 0.99`. Output: **spike_count = 96** — the cell now fires
MORE in ND than PD because NaP's persistent depolarisation dominates over the GABA shunt (which is
shunting-only because e_GABA = v_rest = -60 mV from t0065 finding).

### Example 5 — nar_high FULL/PD seed=1

Input: baseline + `gbar_nart67 = 0.024 S/cm² (24 mS/cm²)`. Output: spike_count = 16 — only +1
over baseline. The resurgent kinetics don't trigger at 14 Hz.

### Example 6 — kv3_high FULL/PD seed=1

Input: baseline + `gbar_kv3t67 = 0.060 S/cm² (60 mS/cm²)`. Output: spike_count = 16 — Kv3 allows
~1 extra spike per train via faster repolarisation, but not transformative at this density.

## Verification

| Verificator | Status |
| --- | --- |
| `verify_research_code.py` | PASSED (0 errors, 0 warnings) |
| `verify_plan.py` | PASSED (0 errors, 4 non-blocking warnings) |
| `verify_task_dependencies.py` | PASSED (t0008, t0019, t0065 all completed) |
| `verify_task_metrics.py` | PASSED (registered DSI metric only) |
| `verify_task_results.py` | PASSED (mandatory sections present) |
| `verify_suggestions.py` | PASSED (5 suggestions, all required fields) |
| `verify_task_file.py` | PASSED |
| `verify_task_folder.py` | PASSED |
| `verify_logs.py` | PASSED |
| Mypy + ruff | PASSED on all task code |
| Per-trial instability flag | 0/160 trials flagged (no depolarisation runaway, no silence) |

## Limitations

1. **Somatic insertion only**: real RGCs localise Nav1.6 / Kv3 at the AIS. The deposited cell has no
   AIS. Channels' effects on AP initiation timing are therefore understated.
2. **One channel at a time**: doesn't capture co-expression interactions (e.g., Nav1.6 + Kv3 jointly
   enabling fast-spiking).
3. **Coarse density grid**: 3 points per channel; finer grids may reveal threshold-crossing
   transitions (e.g., the DSI sign-flip point for NaP).
4. **Simplified MOD kinetics**: NONSPECIFIC_CURRENT pattern with HH-style m/h gates; published
   models for NaR (Khaliq-Raman blocking-particle scheme) and Kv3 (Wang-Buzsaki kinetics) are
   richer.
5. **5 seeds per condition**: gives mean ± SD but not tight confidence intervals; the SD on ND
   spike counts (~1-3 spikes) is comparable to the baseline mean (~1.6), so small DSI changes (Δ <
   0.1) are within sampling noise.

## Files Created

* `tasks/t0067_t0065_soma_channel_addition_sweep/code/{paths,constants,run_sweep,plot_results}.py`
* `tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/{nav16t67,napt67,nart67,kv3t67,kv4t67}.mod`
* `tasks/t0067_t0065_soma_channel_addition_sweep/code/build/nrnmech.dll` (~140 KB)
* `tasks/t0067_t0065_soma_channel_addition_sweep/data/per_trial_metrics.json` (160 trials)
* `tasks/t0067_t0065_soma_channel_addition_sweep/data/dsi_by_condition.json` (16 conditions)
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/metrics.json`
  (`direction_selectivity_index = 0.7975` for baseline)
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/costs.json`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/remote_machines_used.json`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/suggestions.json`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/results_summary.md`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/results_detailed.md`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/firing_rate_vs_density.png`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/dsi_vs_density.png`
* `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/spike_count_heatmap.png`

## Task Requirement Coverage

The task as commissioned: "Create a task where you can add some more channels to the soma to change
the action potential generation. Select 3 more sodium and 2 potassium channels with different
dynamics and add them (1 per experiment) and test how firing rate and DSI changes. Use only
Poleg-Polsky model (t0065) and use some reasonable current densities."

REQs from `plan/plan.md`:

* **REQ-1 (5 channels added: Nav1.6, NaP, NaR, Kv3, Kv4)**: Done — 5 MOD files vendored +
  compiled. See `code/mods/`.
* **REQ-2 (3 densities per channel: low/med/high; ~3× between)**: Done — see Per-condition
  Metrics Table.
* **REQ-3 (one channel per experiment, isolation)**: Done — `_set_active_channel(soma, key)` zeros
  all other channels' gbar before setting the active one. Verified via baseline reproducibility
  (Example 1 matches t0065's 15 spikes).
* **REQ-4 (FULL mode only)**: Done — only `exptype = 1` used; passive trials skipped.
* **REQ-5 (PD and ND directions, gabaMOD-swap)**: Done — `GABA_MOD_PD = 0.33`,
  `GABA_MOD_ND = 0.99`.
* **REQ-6 (5 seeds per condition)**: Done — `N_SEEDS_PER_CONDITION = 5`, 80 PD trials + 80 ND
  trials.
* **REQ-7 (firing rate + DSI per condition)**: Done — see Per-condition Metrics Table.
* **REQ-8 (failure-mode flagging)**: Done — `is_unstable` field in `per_trial_metrics.json`.
  **0/160** trials flagged.
* **REQ-9 (3 plots: firing-rate-vs-density, DSI-vs-density, spike-count heatmap)**: Done —
  embedded in Visualisations section above.
* **REQ-10 (results_summary.md + results_detailed.md spec_version 2)**: Done — both files present
  with all mandatory sections.
