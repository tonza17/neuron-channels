# ✅ Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0065_t0020_epsp_ipsp_vm_protocol` |
| **Status** | ✅ completed |
| **Started** | 2026-04-30T07:58:16Z |
| **Completed** | 2026-04-30T15:16:00Z |
| **Duration** | 7h 17m |
| **Dependencies** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Task types** | `data-analysis` |
| **Step progress** | 9/15 |
| **Task folder** | [`t0065_t0020_epsp_ipsp_vm_protocol/`](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/task_description.md)*

# Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol

## Motivation

The from-scratch DSGC family (t0052-t0059) is trapped in a binary regime —
single-spike-per-trial giving a trivial DSI of 1.0, or full suppression giving DSI of 0.
Diagnostic tasks t0060-t0064 characterised that trap from several angles (AMPA-only escape,
NMDA-only escape, AMPA priming, HH voltage-step and current-step tests) but the central
question remains open: how does a model that *does* show graded direction selectivity
decompose into excitatory and inhibitory drives?

Task t0020 is one of the few prior runs that produced both a non-trivial firing rate (~14.85
Hz peak) and a meaningful DSI (0.7838) — using the deposited Poleg-Polsky & Diamond 2016
ModelDB 189347 cell under the native `gabaMOD` parameter-swap protocol (PD = 0.33, ND = 0.99).
That same deposited model has not yet been measured with the new EPSP_PASSIVE / IPSP_PASSIVE /
FULL trial-mode protocol that the from-scratch family standardised in t0059.

The goal of this task is to apply that protocol to the deposited model:

* **EPSP_PASSIVE** — Hodgkin-Huxley (HH) channels off, GABA off, AMPA + NMDA active. Records
  the pure excitatory PSP at the soma.
* **IPSP_PASSIVE** — HH off, AMPA + NMDA off, GABA active. Records the pure inhibitory PSP.
* **FULL** — HH on, all synapses at canonical defaults. Records full somatic Vm (the t0020
  reference condition).

Together these three traces decompose the FULL Vm into its excitatory and inhibitory
components under exactly the same stimulus, in a model that is known to produce graded
direction selectivity. This gives us a reference Vm/EPSP/IPSP triplet to compare against the
from-scratch family's binary-regime traces — telling us whether the binary regime is (a)
excitatory under-drive, (b) inhibitory over-shunt, or (c) HH miscalibration.

## Scope

* Cell: deposited Poleg-Polsky 2016 ModelDB 189347 DSGC, exactly as built in
  `tasks/t0008_port_modeldb_189347/code/build_cell.py::build_dsgc()`.
* Stimulus: deposited drifting-bar stimulus, default parameters from `t0008.apply_params`.
* Directions: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`) — matching t0020.
* Trial modes: `EPSP_PASSIVE`, `IPSP_PASSIVE`, `FULL` (the same enum used in t0059's
  `code/trial.py`, redefined locally because we are running on the deposited cell, not the
  from-scratch one).
* Per-trial Vm trace: full somatic voltage trace recorded at every NEURON timestep; saved to a
  per-mode CSV.
* Trials per (mode, direction) cell: 1 (single seed = 1). This is a diagnostic decomposition,
  not a tuning-curve sweep — one trace per condition is sufficient to read off EPSP/IPSP
  shape.

This gives 6 trials total: 3 modes × 2 directions × 1 trial.

## Approach

1. Reuse `t0008.apply_params` and `t0008.build_dsgc` to construct the deposited cell.
2. Reuse `t0020.run_gabamod_sweep::run_one_trial_gabamod`'s structure as a starting template.
3. Channel-isolation overrides follow the t0049 pattern:
   * Call `apply_params(h, seed=1)` and `h("update()")` and `h("placeBIP()")` first (so that
     the default conductances are written to all point processes),
   * Override the relevant globals from Python (`h.SpikesOn`, `h.gabaMOD`, `h.b2gampa`,
     `h.b2gnmda`),
   * Re-call `h("update()")` and `h("placeBIP()")` so the synaptic point processes pick up the
     overridden globals,
   * Attach Vm + t recorders, `finitialize`, `continuerun`.
4. Save raw traces to `data/voltage_traces.csv` (long-format: `mode, direction, t_ms, v_mv`)
   so a downstream plot script can re-read without re-simulating.
5. Plot per-mode 2-panel figures (PD vs ND) and a 3-mode summary panel; embed in
   `results_detailed.md`.

The `EPSP_PASSIVE` setting `gabaMOD = 0` collapses PD and ND to the same condition (no
inhibition to swap). We still run both directions for completeness — they should overlay
exactly. If they do not, the deposited model has direction-dependent state we have not yet
identified.

## Configurations

Six trials, all `seed = 1`:

| Mode | Direction | SpikesOn | gabaMOD | b2gampa | b2gnmda |
| --- | --- | --- | --- | --- | --- |
| EPSP_PASSIVE | PD | 0 | 0.0 | default | default |
| EPSP_PASSIVE | ND | 0 | 0.0 | default | default |
| IPSP_PASSIVE | PD | 0 | 0.33 | 0.0 | 0.0 |
| IPSP_PASSIVE | ND | 0 | 0.99 | 0.0 | 0.0 |
| FULL | PD | 1 | 0.33 | default | default |
| FULL | ND | 1 | 0.99 | default | default |

`default` means whatever value `apply_params(h, seed=1)` writes (canonical paper values).
`SpikesOn = 0` activates the deposited model's built-in HH disable path (the same one t0046
and t0049 already use for sub-threshold measurements).

## Outputs

* `data/voltage_traces.csv` — long-format per-sample table.
* `results/metrics.json` — per-trial scalar summaries: peak Vm, baseline-subtracted peak
  amplitude, spike count (FULL only), trial duration.
* `results/images/vm_full_pd_vs_nd.png` — FULL-mode Vm trace, PD overlaid with ND.
* `results/images/epsp_pd_vs_nd.png` — EPSP_PASSIVE trace, PD overlaid with ND (expected to
  superimpose).
* `results/images/ipsp_pd_vs_nd.png` — IPSP_PASSIVE trace, PD overlaid with ND.
* `results/images/three_mode_pd_overlay.png` — PD direction across all three modes on one
  axis.
* `results/images/three_mode_nd_overlay.png` — ND direction across all three modes on one
  axis.
* `results/results_summary.md`, `results/results_detailed.md` with per-mode peak amplitudes
  and a qualitative description of the decomposition.

## Key Questions

1. What is the peak EPSP amplitude (passive, GABA-off) in PD versus ND? Are they identical?
2. What is the peak IPSP deflection in PD versus ND, and does the PD-vs-ND difference
   quantitatively match the gabaMOD scalar ratio (0.33 vs 0.99)?
3. When EPSP and IPSP are summed by hand, does the result resemble the FULL Vm under HH-off
   conditions? Or is the cell's nonlinear summation contributing meaningfully?
4. How do the deposited model's EPSP and IPSP shapes compare to the from-scratch family's
   EPSP/IPSP traces from t0059? This contextualises whether the binary regime is a
   synaptic-balance issue or an HH-calibration issue.

## Compute and Budget

* Local Windows workstation. Six trials × ~1.5 minutes each ≈ 10 minutes wall-clock.
* No paid API or remote GPU costs.

## Time Estimation

* Implementation: 1 hour.
* Run + plotting: 30 minutes.
* Reporting: 30 minutes.

## Dependencies

* `t0020_port_modeldb_189347_gabamod` — provides `run_one_trial_gabamod` template, the
  `apply_params` import, the `_assert_bip_positions_baseline` guard, and the validated PD/ND
  scalar values.

We do not formally depend on t0059 because that task uses the from-scratch cell substrate. We
do copy its `TrialMode` enum spelling for consistency, but the implementation is independent.

## Risks and Fallbacks

* If the deposited model's `b2gampa = 0` + `b2gnmda = 0` does not actually silence excitatory
  drive (the deposited code is a HOC tangle), we will detect this by the
  EPSP_PASSIVE-vs-IPSP_PASSIVE trace shapes being non-orthogonal. Fallback: also zero `nmdaOn
  = 0` and verify excitatory drive vanishes.
* If `SpikesOn = 0` does not fully suppress HH (it should, per t0046 / t0049 usage), the
  FULL-vs- passive traces will be ambiguous. Fallback: explicitly zero the soma `gnabar_hh`
  and `gkbar_hh` via Python after `apply_params` and verify Vm cannot exceed -20 mV in passive
  trials.

## Verification Criteria

* All six trials complete without raising `_assert_bip_positions_baseline`.
* EPSP_PASSIVE PD and ND traces are bit-identical (gabaMOD = 0 in both).
* IPSP_PASSIVE peak amplitude in ND > peak amplitude in PD (more inhibition → larger
  hyperpolarisation in ND).
* FULL-mode PD trace shows higher firing rate than ND, consistent with t0020's headline
  result.
* Plots embedded in `results_detailed.md` render correctly on GitHub.

</details>

## Metrics

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.875** |

## Suggestions Generated

<details>
<summary><strong>Apply EPSP/IPSP/FULL protocol to the from-scratch DSGC family
substrate</strong> (S-0065-01)</summary>

**Kind**: experiment | **Priority**: high

t0065 isolated the deposited cell's EPSP and IPSP shapes and showed that direction selectivity
in that cell comes from differential shunting inhibition (e_SACinhib = v_rest = -60 mV, so
opening Cl- channels produces zero net Vm deflection). The from-scratch family (t0052-t0059)
is trapped in a binary regime: single-spike-per-trial trivial DSI = 1, or full suppression DSI
= 0. A direct EPSP_PASSIVE / IPSP_PASSIVE / FULL decomposition on the from-scratch substrate
(using t0057's library wiring: 100 E + 100 I synapses on t0009 morphology) would tell us
whether the binary-regime failure is excitatory under-drive, hyperpolarising rather than
shunting inhibition, or HH miscalibration. The same six-trial protocol from tasks/t0065_*/code
can be ported to the from-scratch cell builder with minimal changes. Expected output: six
traces showing whether the from-scratch IPSP is hyperpolarising (would localise the
binary-regime cause) or flat-at-reversal (would invalidate the shunting hypothesis).

</details>

<details>
<summary><strong>Match the from-scratch GABA reversal to resting potential and
re-test direction selectivity</strong> (S-0065-02)</summary>

**Kind**: experiment | **Priority**: high

The deposited cell places e_SACinhib = -60 mV which equals the cell's leak-driven quiescent
potential, making inhibition purely shunting. If the from-scratch family uses an e_GABA below
resting potential (e.g., -75 mV which is biologically plausible for Cl- with low [Cl-]_i),
inhibition becomes hyperpolarising and can collapse the DSI to 0 by pulling the cell off
threshold across all directions. Conversely, if e_GABA > v_rest, inhibition can depolarise
toward threshold and generate spurious spikes. Setting e_GABA = v_rest in the from-scratch
substrate is a single-line change (modify the gaba_tonic.mod e parameter or the synapse
mechanism's reversal). This directly tests whether the deposited cell's success is
structurally dependent on its e_GABA = v_rest design choice. Expected output: from-scratch
family with e_GABA = v_rest produces a graded tuning curve with 5-15 Hz peak in PD and DSI in
[0.5, 0.85], matching the deposited cell's behaviour.

</details>

<details>
<summary><strong>Resolve inhibitory conductance time-course via SEClamp on the
deposited cell</strong> (S-0065-03)</summary>

**Kind**: experiment | **Priority**: medium

t0065 IPSP_PASSIVE traces are flat at e_SACinhib = -60 mV because the cell sits at the
inhibitory reversal under no excitation. The voltage trace cannot reveal the inhibitory
conductance time-course; only a voltage clamp can resolve g_inh(t). t0049 already has SEClamp
infrastructure for this cell. Combining the t0065 channel-isolation pattern (zero excitatory
drives via b2gampa = b2gnmda = s2gach = achMOD = 0) with a SEClamp at -65 mV (or any
non-equilibrium voltage offset from e_SACinhib) would resolve the inhibitory conductance in nS
as a function of time, separately for PD (gabaMOD = 0.33) and ND (gabaMOD = 0.99). This is
essential for quantifying the differential shunting magnitude that drives FULL-mode DSI: the
integral of g_inh(t) should be ~3x larger in ND than in PD. Expected output: two conductance
time-courses showing g_inhibitory(t) over the 1000 ms trial in PD vs ND, with peak g_inh and
integrated charge per direction.

</details>

<details>
<summary><strong>Multi-seed average of the t0065 protocol to add error bars on FULL
spike counts</strong> (S-0065-04)</summary>

**Kind**: experiment | **Priority**: low

t0065 ran one seed per (mode, direction) cell. The FULL-mode 15-PD vs 1-ND spike count is
consistent with t0020's 20-trial mean (14.85 vs 1.80 Hz) but has no statistical band of its
own. Running 10-20 seeds per cell would give SD/SE on each metric and let us state the DSI
with a confidence interval. EPSP_PASSIVE and IPSP_PASSIVE traces are deterministic given seed
(verified bit-identicality of EPSP_PASSIVE PD vs ND in t0065), so multi-seed for those modes
is unnecessary - only FULL needs the seed sweep. Sweep cost: ~40 trials x 3 s ≈ 2 minutes
additional, no new infrastructure. Expected output: FULL-mode spike-count distribution per
direction (mean ± SD across 20 seeds) and DSI 95% confidence interval.

</details>

<details>
<summary><strong>Eight-direction EPSP/IPSP/FULL tuning curve on the deposited
cell</strong> (S-0065-05)</summary>

**Kind**: experiment | **Priority**: low

t0065 only tests gabaMOD = 0.33 (PD) and 0.99 (ND). The Poleg-Polsky 2016 paper has a smooth
tuning curve over 8 directions, which the deposited model simulates by sweeping gabaMOD across
[0.33, 0.99]. Running EPSP_PASSIVE / IPSP_PASSIVE / FULL at all 8 directions would produce an
EPSP/IPSP decomposition for the entire tuning curve, not just the two anchor points. Most
informative for understanding how shunting modulates the EPSP envelope at intermediate
directions: does the relationship between gabaMOD and FULL-mode envelope compression scale
linearly, or is there a threshold around gabaMOD ~ 0.6 where the cell transitions from spiking
to non-spiking? Sweep cost: 24 trials (3 modes x 8 directions x 1 seed) ≈ 75 s. Expected
output: 24-trial dataset with gabaMOD-modulated tuning curve in spike counts and the
corresponding (constant) EPSP_PASSIVE and (constant-flat) IPSP_PASSIVE traces.

</details>

## Research

* [`research_code.md`](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/results_summary.md)*

# Results Summary: Test t0020 deposited DSGC under EPSP/IPSP/FULL protocol

## Summary

The deposited Poleg-Polsky & Diamond 2016 DSGC was driven through the EPSP_PASSIVE /
IPSP_PASSIVE / FULL trial-mode protocol — six trials (3 modes × 2 directions × 1 seed) —
decomposing the somatic Vm into pure-excitatory and pure-inhibitory components. Headline
finding: **the model's direction selectivity is produced almost entirely by shunting
inhibition, not hyperpolarising inhibition**. The IPSP_PASSIVE traces stay flat at the
inhibitory reversal potential e_SACinhib = -60 mV in both PD and ND, while the EPSP_PASSIVE
traces are bit-identical between directions (gabaMOD = 0). The FULL trace shows a 15× spike
count difference (15 PD vs 1 ND) driven entirely by the PD-vs-ND difference in the inhibitory
*conductance* (gabaMOD 0.33 vs 0.99) shunting away the otherwise direction-invariant
excitatory drive.

## Metrics

* **FULL PD spike count**: **15** (firing rate ≈ **15.0 Hz** over 1000 ms)
* **FULL ND spike count**: **1** (firing rate ≈ **1.0 Hz** over 1000 ms)
* **DSI (single-seed point estimate, spike-count-based)**: **0.875** ((15 − 1) / (15 + 1))
* **EPSP_PASSIVE peak Vm**: **-29.8 mV** (PD = ND, bit-identical, +28.6 mV above baseline)
* **IPSP_PASSIVE peak Vm**: **-60.0 mV** (PD), **-60.0 mV** (ND) — flat at e_SACinhib
* **IPSP_PASSIVE peak − baseline**: **+0.10 mV** (PD), **+0.11 mV** (ND) — noise floor
* **FULL peak Vm**: **+43.2 mV** (PD), **+43.3 mV** (ND) — both reach Na+-spike peak
* **FULL baseline Vm**: **-58.9 mV** (PD), **-59.3 mV** (ND)
* **Trials run**: 6 (PD × ND for each of FULL / EPSP_PASSIVE / IPSP_PASSIVE)
* **Wall-clock**: **18.7 s** for the sweep, ~1 s for plotting (local Windows workstation)
* **Sample count per trial**: 10,001 (dt = 0.1 ms × tstop = 1000 ms)

## Verification

* `verify_research_code` — PASSED (0 errors, 0 warnings) on `research_code.md`.
* `verify_plan` — PASSED (0 errors, 0 warnings) on `plan/plan.md`.
* `verify_task_dependencies` — PASSED (0 errors, 0 warnings) at check-deps step (t0020
  completed).
* Per-trial `_assert_bip_positions_baseline` — PASSED in all six trials. BIP synapse positions
  remained at their canonical baseline coordinates throughout, confirming the t0008 spatial
  rotation logic was not silently re-engaged.
* Single-seed sanity gate vs t0020 reference: t0020 reported peak PD firing rate **14.85 Hz**
  averaged across 20 PD trials. The t0065 single PD trial yields **15.0 Hz** — within the
  1-trial Poisson uncertainty band of t0020's mean.
* Mypy and ruff pass on all code in `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/`.

## Conclusion

Two-line summary for follow-on tasks:

* **EPSP_PASSIVE shows direction-invariant +28.6 mV depolarising envelope** in this model;
  direction selectivity is not encoded on the excitatory side.
* **IPSP_PASSIVE shows zero membrane deflection** because the cell's resting potential
  coincides with e_SACinhib = -60 mV; the inhibitory drive's effect is therefore purely
  shunting (changing input resistance), and the FULL-mode PD/ND difference must come entirely
  from this shunt.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0065_t0020_epsp_ipsp_vm_protocol" date: "2026-04-30" ---
# Detailed Results: Test t0020 deposited DSGC under EPSP/IPSP/FULL protocol

## Summary

Drove the deposited Poleg-Polsky & Diamond 2016 DSGC through the EPSP_PASSIVE / IPSP_PASSIVE /
FULL trial-mode protocol — six trials (3 modes × 2 directions × 1 seed). Headline finding: the
model's direction selectivity is produced almost entirely by **shunting inhibition**, not
hyperpolarising inhibition. The IPSP_PASSIVE traces sit flat at e_SACinhib = -60 mV in both PD
and ND, the EPSP_PASSIVE traces are bit-identical between directions (`gabaMOD = 0` in both),
and the FULL trace shows a 15× spike-count difference (15 PD vs 1 ND, DSI = 0.875) driven
entirely by the PD-vs-ND difference in inhibitory *conductance* (`gabaMOD = 0.33` vs `0.99`)
shunting away otherwise direction-invariant excitatory drive.

## Methodology

* **Cell model**: Poleg-Polsky & Diamond 2016 ModelDB 189347 DSGC, instantiated through
  `tasks.t0008_port_modeldb_189347.code.build_cell.build_dsgc()` with the GUI-free HOC
  derivative `dsgc_model.hoc`. Cell: 1 soma + 350 dendrite sections, 282 ON dendrites, 282
  bipolar (BIP) + 282 SAC inhibitory (SACinhib) + 282 SAC excitatory (SACexc) point processes.
* **Stimulus**: deposited drifting bar (`lightspeed = 1 µm/ms`, `lightwidth = 500 µm`,
  `lightstart = -100 ms`). Direction is encoded purely via `h.gabaMOD` (PD = 0.33, ND = 0.99)
  per the t0020 gabaMOD-swap convention; BIP synapse positions stay at baseline (no rotation).
* **Trial modes**:
  * **FULL** — `h.exptype = 1` (HH on); `gabaMOD = 0.33` (PD) or `0.99` (ND); all canonical
    conductances active.
  * **EPSP_PASSIVE** — `h.exptype = 2` (HH off via TTX); `h.gabaMOD = 0`; `h.s2ggaba = 0`
    (silence inhibition).
  * **IPSP_PASSIVE** — `h.exptype = 2` (HH off); `h.b2gampa = 0`; `h.b2gnmda = 0`; `h.s2gach =
    0`; `h.achMOD = 0` (silence both bipolar AMPA/NMDA and SAC cholinergic excitation).
* **Per-trial sequence**: `apply_params(seed=1)` → set `h.gabaMOD` → set `h.exptype` → apply
  per-mode synaptic overrides → `h("init_active()")` (rebinds `RGCsomana`/`RGCdendna` per
  exptype) → `h("update()")` → `h("placeBIP()")` → attach Vm and t recorders (and a `NetCon`
  spike threshold for FULL trials only) → `h.finitialize(-65)` → `h.continuerun(1000)`.
* **Sample rate**: 10,001 samples per trial at `dt = 0.1 ms`, `tstop = 1000 ms`.
* **Spike detection**: `NetCon` rising-edge crossings of `AP_THRESHOLD_MV = -10 mV`.
* **Compute**: local Windows workstation, single CPU core. The deposited cell's `nrnmech.dll`
  was compiled fresh inside the worktree (228 KB) before the run.
* **Wall-clock**: 18.7 s for the six-trial sweep (mean **3.1 s/trial**), plus ~1 s for
  plotting.
* **Timestamps**: implementation step started 2026-04-30T08:12:18Z, completed
  2026-04-30T08:26:18Z; results step started 2026-04-30T08:26:35Z.

## Per-trial Metrics Table

| Mode | Direction | Peak Vm (mV) | Baseline Vm (mV) | Peak − Baseline (mV) | Spikes |
| --- | --- | --- | --- | --- | --- |
| FULL | PD | **+43.180** | -58.869 | +102.05 | **15** |
| FULL | ND | **+43.291** | -59.313 | +102.60 | **1** |
| EPSP_PASSIVE | PD | -29.827 | -58.466 | +28.64 | — |
| EPSP_PASSIVE | ND | -29.827 | -58.466 | +28.64 | — |
| IPSP_PASSIVE | PD | -60.019 | -60.123 | +0.10 | — |
| IPSP_PASSIVE | ND | -60.015 | -60.123 | +0.11 | — |

DSI (spike-count): **(15 − 1) / (15 + 1) = 0.875** at this seed. Full per-trial scalar dump is
also persisted as `data/per_trial_metrics.json` for downstream consumers.

## Comparison vs Baselines

* **vs t0020 reference** (deposited cell, 20 PD + 20 ND trials, `gabaMOD` swap):
  * t0020 peak PD firing rate: **14.85 Hz** (mean ± 1.59 SD across 20 trials).
  * t0065 single PD trial: **15.0 Hz** — Δ = **+0.15 Hz**, comfortably inside the t0020
    one-sigma band.
  * t0020 ND firing rate: **1.80 Hz** (mean ± 1.03 SD); t0065 single ND trial: **1.0 Hz** — Δ
    = -0.80 Hz, within one sigma.
  * t0020 DSI (spike-rate): **0.7838**; t0065 single-seed DSI: **0.875** — t0065 is high but
    within plausible single-trial fluctuation given the small ND spike counts.
* **vs t0059 from-scratch family**: t0059 trapped at peak ≤ 2.14 Hz (binary regime). The
  deposited cell's 15 Hz PD rate is **~7× higher** at peak — consistent with the deposited
  cell having a higher-fidelity excitatory drive (BIP + SAC ACh) and a more naturalistic
  inhibitory shunt.

## Visualisations

### FULL mode: somatic Vm, PD vs ND

![FULL mode somatic Vm trace, PD overlaid with
ND](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/vm_full_pd_vs_nd.png)

PD shows ~15 spikes between 130-440 ms riding on a depolarising envelope that peaks at roughly
-45 mV between spikes. ND shows just 1 spike at ~290 ms; the underlying envelope peaks at
roughly -50 mV, ~5 mV lower than PD. The 5 mV envelope difference is enough to keep ND mostly
below AP threshold while PD repeatedly crosses it.

### EPSP_PASSIVE: PD vs ND (excitation-only, HH off)

![EPSP_PASSIVE trace, PD overlaid with
ND](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/epsp_pd_vs_nd.png)

The two traces are bit-identical (numerical confirmation: peak Vm and baseline Vm match to
machine precision). With `gabaMOD = 0` and HH off, the EPSP envelope is direction-invariant in
this model. Peak depolarisation: **-29.8 mV**, ~28.6 mV above the pre-bar baseline.

### IPSP_PASSIVE: PD vs ND (inhibition-only, HH off, all excitation off)

![IPSP_PASSIVE trace, PD overlaid with
ND](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/ipsp_pd_vs_nd.png)

Both traces sit flat at e_SACinhib = -60 mV throughout. This is **not** because inhibition is
silent — it is fully active at canonical PD (gabaMOD = 0.33) and ND (gabaMOD = 0.99) levels —
but because the cell's quiescent membrane potential under no excitation already coincides with
the inhibitory reversal. Opening Cl- channels at e_Cl = -60 mV when v_m = -60 mV produces zero
net current, hence zero voltage deflection.

### Three-mode overlay: PD direction

![Three-mode overlay for PD
direction](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/three_mode_pd_overlay.png)

Stacked on a single axis: FULL (black, with spikes), EPSP_PASSIVE (green, smooth depolarising
envelope peaking at -30 mV around t = 220 ms), IPSP_PASSIVE (purple, flat at -60 mV). The ~15
mV gap between EPSP_PASSIVE and FULL's subthreshold envelope shows the magnitude of inhibitory
shunting in PD.

### Three-mode overlay: ND direction

![Three-mode overlay for ND
direction](../../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/three_mode_nd_overlay.png)

Same three modes for ND. EPSP_PASSIVE is identical to PD's EPSP_PASSIVE. IPSP_PASSIVE is also
flat at -60 mV. FULL's envelope is visibly more compressed than PD-FULL — the 3× stronger
inhibitory drive (gabaMOD = 0.99 vs 0.33) shunts away enough of the EPSP that AP threshold is
reached only once during the trial.

## Analysis & Discussion

### Direction selectivity is shunting-inhibition-driven in this model

The four critical numbers are:

* EPSP_PASSIVE peak Vm: -29.8 mV (PD = ND, identical).
* IPSP_PASSIVE peak Vm: -60.0 mV (PD ≈ ND, both at e_SACinhib).
* FULL peak underlying envelope: -45 mV (PD), -50 mV (ND).

These have one consistent interpretation: the direction-dependent variable in FULL is the
*amplitude of inhibitory shunting*, not the inhibitory voltage drive or the excitatory drive
itself. EPSP_PASSIVE isolates the excitatory contribution and shows it is direction-invariant.
IPSP_PASSIVE isolates the inhibitory contribution and shows it produces zero voltage
deflection — but it must still produce the conductance change that explains the FULL-mode 5 mV
PD-vs-ND envelope difference. That conductance is the shunt.

### Why is the cell already at e_SACinhib in IPSP_PASSIVE?

V_INIT_MV is set to -65 mV, but `init_active()` writes `RGCepas = -60 mV` (passive leak
reversal) and `RGCgpas = 5e-5*(1+active*10)` (passive leak conductance). With no excitation
and HH off, the cell relaxes from -65 to -60 within milliseconds, driven purely by the passive
leak. This is a model-level choice in Poleg-Polsky 2016 and explains the "depolarising IPSP"
phenomenology seen here.

In a real DSGC, the resting potential is typically -65 to -70 mV while e_Cl is around -65 to
-70 mV, so the inhibitory reversal sits near or below resting potential. In this model, the
choice of e_SACinhib = -60 mV combined with eleak = -60 mV places the cell exactly at the
inhibitory reversal — an unusual design choice that maximises shunting effects relative to
hyperpolarising effects.

### Implications for the from-scratch DSGC family (t0052-t0059)

The from-scratch family is trapped in a binary regime: either single-spike-per-trial (DSI = 1
trivially) or full suppression (DSI = 0). The decomposition here suggests the failure may stem
from an inhibitory pathway that hyperpolarises rather than shunts. If the from-scratch family
uses `e_GABA < v_rest` (e.g., -75 mV), inhibition will pull the cell *away* from AP threshold,
suppressing all spikes. Replicating the deposited model's `e_GABA = v_rest` design in the
from-scratch substrate is a concrete follow-on direction (see `suggestions.json` S-0065-02).

### What this protocol cannot tell us

* The IPSP_PASSIVE trace is flat by construction — it does not reveal the *time course* of the
  inhibitory conductance, only its voltage-deflection signature. To measure the conductance
  directly, a SEClamp at e_SACinhib would resolve the inhibition-only current in pA (see
  S-0065-03).
* The single-seed run gives no error bars on FULL spike counts.

## Examples

Each of the six trials is a complete input/output pair: the input is the parameter vector
written to NEURON globals before `finitialize`; the output is the recorded somatic Vm trace
and its derived scalars.

### Example 1 — FULL / PD (best case: vigorous spiking, matches t0020 mean)

Input parameters:

```text
h.exptype = 1            # HH on
h.SpikesOn = 1
h.gabaMOD = 0.33         # PD direction encoding
h.b2gampa, h.b2gnmda = canonical  # written by apply_params(h, seed=1)
h.s2gach, h.achMOD = canonical
h.s2ggaba = canonical
seed = 1, tstop = 1000 ms, dt = 0.1 ms
```

Output (CSV head + key timepoints from `data/voltage_traces.csv`):

```csv
mode,direction,t_ms,v_mv
FULL,PD,0.0000,-65.000000
FULL,PD,0.1000,-64.732241
...
FULL,PD,127.0000,43.108888     # <-- peak Vm of trial
FULL,PD,127.1000,43.180414
...
FULL,PD,140.0000,-52.420368    # spike-train interval, between APs
FULL,PD,140.1000,-52.117935
```

Derived scalars: `peak_v_mv = +43.180`, `baseline_v_mv = -58.869`, `spike_count = 15`, firing
rate ≈ **15.0 Hz**. Illustrates the canonical PD response: depolarising envelope from BIP +
NMDA + SAC ACh excitation, weak shunting from `gabaMOD = 0.33`, repeated AP firing across
130-440 ms.

### Example 2 — FULL / ND (worst case: near-complete spike suppression)

Input parameters:

```text
h.exptype = 1            # HH on
h.gabaMOD = 0.99         # ND direction encoding (3x stronger inhibition vs PD)
all other params = canonical
```

Output (single AP near 290 ms):

```csv
FULL,ND,288.0000,-46.061120
FULL,ND,288.1000,-45.621193
FULL,ND,288.2000,-45.185862
FULL,ND,288.3000,-44.695508
FULL,ND,288.4000,-44.119057
```

Derived scalars: `peak_v_mv = +43.291`, `baseline_v_mv = -59.313`, `spike_count = 1`, firing
rate ≈ **1.0 Hz**. Illustrates ND failure mode: excitatory drive is identical to PD
(EPSP_PASSIVE traces are bit-identical) but the 3× larger gabaMOD shunts the depolarising
envelope ~5 mV lower, dropping it below AP threshold for most of the trial.

### Example 3 — EPSP_PASSIVE / PD (excitation isolation)

Input parameters:

```text
h.exptype = 2            # HH off (TTX)
h.gabaMOD = 0.0          # silence GABA via reversal-encoding scalar
h.s2ggaba = 0.0          # belt-and-braces silence inhibition
all excitatory params = canonical
```

Output (peak around 218 ms):

```csv
EPSP_PASSIVE,PD,218.4000,-29.975019
```

Derived scalars: `peak_v_mv = -29.827`, `baseline_v_mv = -58.466`, `peak − baseline = +28.64
mV`. Illustrates the pure excitatory PSP at the soma: a smooth, sub-threshold depolarising
envelope ~29 mV in amplitude.

### Example 4 — EPSP_PASSIVE / ND (excitation isolation, contrastive with PD)

Input parameters: identical to Example 3 except `h.gabaMOD = 0` is set independently of the
ND-direction nominal value (0.99) — the override forces gabaMOD off in both directions for
EPSP_PASSIVE.

Output: bit-identical to PD trace (numerical confirmation: `peak_v_mv` and `baseline_v_mv`
match to machine precision). Illustrates that direction selectivity in this model is **not**
encoded on the excitatory side — when gabaMOD = 0 in both directions, the BIP/NMDA/SAC ACh
inputs produce identical envelopes regardless of nominal direction.

### Example 5 — IPSP_PASSIVE / PD (inhibition isolation, weak)

Input parameters:

```text
h.exptype = 2            # HH off (TTX)
h.gabaMOD = 0.33         # PD inhibition strength
h.b2gampa = 0.0
h.b2gnmda = 0.0          # silence bipolar excitation
h.s2gach = 0.0
h.achMOD = 0.0           # silence SAC cholinergic excitation
```

Output (mid-trial sample):

```csv
IPSP_PASSIVE,PD,500.0000,-60.012987
```

Derived scalars: `peak_v_mv = -60.019`, `baseline_v_mv = -60.123`, `peak − baseline = +0.10
mV`. Illustrates the boundary case: with all excitation silenced, the cell relaxes from -65 mV
to e_SACinhib = -60 mV via the passive leak (which itself has reversal -60 mV), and the active
inhibition produces *zero* voltage deflection — the membrane is already at the Cl- reversal
potential.

### Example 6 — IPSP_PASSIVE / ND (inhibition isolation, strong; contrastive with PD)

Input parameters: identical to Example 5 except `h.gabaMOD = 0.99` (3× stronger inhibition).

Output (mid-trial sample):

```csv
IPSP_PASSIVE,ND,500.0000,-60.021185
```

Derived scalars: `peak_v_mv = -60.015`, `baseline_v_mv = -60.123`, `peak − baseline = +0.11
mV`. Illustrates the contrastive failure of the voltage-only protocol to detect the inhibitory
drive: despite 3× more inhibitory conductance than Example 5, the voltage trace is
indistinguishable. The inhibition is detectable only via input-resistance change (shunting),
not voltage deflection — motivating the SEClamp follow-up (S-0065-03).

### Example 7 — EPSP_PASSIVE PD vs ND bit-identicality check

Contrastive table: same row from each EPSP_PASSIVE trace at t = 218.4 ms.

```csv
mode,direction,t_ms,v_mv
EPSP_PASSIVE,PD,218.4000,-29.975019
EPSP_PASSIVE,ND,218.4000,-29.975019
```

Illustrates the verification that direction encoding via gabaMOD-swap is the *only*
direction-coupled mechanism in this stimulus — when gabaMOD is forced off, PD and ND traces
match to machine precision.

## Verification

| Verificator | Status |
| --- | --- |
| `verify_research_code.py` | PASSED (run during research-code step) |
| `verify_plan.py` | PASSED (run during planning step) |
| `verify_task_dependencies.py` | PASSED (t0020 completed) |
| `verify_task_metrics.py` | PASSED (DSI metric registered) |
| `verify_task_results.py` | PASSED (mandatory sections present) |
| `verify_suggestions.py` | PASSED (5 suggestions, all required fields) |
| `verify_task_file.py` | PASSED |
| `verify_task_folder.py` | PASSED |
| `verify_logs.py` | PASSED |
| Per-trial `_assert_bip_positions_baseline` | PASSED (all 6 trials) |
| Mypy (`mypy -p tasks.t0065_t0020_epsp_ipsp_vm_protocol.code`) | PASSED |
| Ruff check + format | PASSED |

Single-seed sanity gate vs t0020 reference: t0020 reported peak PD firing rate **14.85 Hz**
averaged across 20 PD trials. The t0065 single PD trial yields **15.0 Hz** — within the
1-trial Poisson uncertainty band of t0020's mean.

## Limitations

1. **Single seed**: the FULL-mode spike count is one realisation of a noisy stochastic
   process. The DSI is consistent with t0020's 20-trial mean but has no statistical band.
2. **No conductance measurement**: this protocol records voltage only. The fact that
   IPSP_PASSIVE shows no deflection is informative but does not quantify the inhibitory
   conductance directly. A complementary SEClamp protocol (t0049-style) would close that gap.
3. **No off-axis directions**: only PD (gabaMOD = 0.33) and ND (gabaMOD = 0.99) are tested.
   The full eight-direction tuning curve is t0020's responsibility.
4. **Deposited model only**: this decomposition tells us how the deposited cell works; the
   from-scratch family's binary regime requires a parallel decomposition on its substrate
   (with t0052-t0059 conductance values) to confirm the shunting hypothesis.
5. **Examples count below ARF threshold**: only 7 trial-level examples (vs the 10 minimum
   warning threshold). The protocol has only 6 distinct trials by design; additional examples
   would have to be synthetic time-slices, not new conditions.

## Files Created

* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/paths.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/constants.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/plot_traces.py`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/data/voltage_traces.csv` (~2.0 MB, 60,006 rows)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/data/per_trial_metrics.json`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/metrics.json`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/costs.json`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/remote_machines_used.json`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/suggestions.json`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/results_summary.md`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/results_detailed.md`
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/vm_full_pd_vs_nd.png` (~92 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/epsp_pd_vs_nd.png` (~74 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/ipsp_pd_vs_nd.png` (~43 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/three_mode_pd_overlay.png` (~89 KB)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/three_mode_nd_overlay.png` (~72 KB)

## Next Steps / Suggestions

See `results/suggestions.json` for the structured follow-up list. Key items:

1. **S-0065-01**: Replicate this decomposition on the from-scratch DSGC family substrate.
2. **S-0065-02**: Match the from-scratch GABA reversal to resting potential and re-test
   direction selectivity.
3. **S-0065-03**: Resolve inhibitory conductance time-course via SEClamp on the deposited
   cell.
4. **S-0065-04**: Multi-seed average for FULL spike-count confidence intervals.
5. **S-0065-05**: Eight-direction EPSP/IPSP/FULL tuning curve.

## Task Requirement Coverage

The task as commissioned (from `task.json` short_description and `task_description.md`):
"Apply the EPSP/IPSP/FULL trial-mode protocol from the from-scratch family (t0059) to the
deposited Poleg-Polsky 2016 model used in t0020, recording somatic Vm in PD and ND."

REQs derived from the `## Outputs` and `## Verification Criteria` sections of
`task_description.md` and `plan/plan.md`:

* **REQ-1 (deposited cell substrate)**: Done — `build_dsgc()` from t0008 used; cell wired
  exactly as in t0020. Evidence: `code/run_protocol.py` import and per-trial sequence.
* **REQ-2 (six trials, 3 modes × 2 directions × 1 seed)**: Done — six trial entries in
  `data/per_trial_metrics.json`.
* **REQ-3 (per-trial Vm trace recorded at every NEURON timestep)**: Done —
  `data/voltage_traces.csv`, 60,006 rows, 10,001 samples per trial × 6 trials.
* **REQ-4 (long-format CSV `data/voltage_traces.csv` with columns mode/direction/t_ms/v_mv)**:
  Done — see CSV header in Examples section.
* **REQ-5 (per-trial scalar metrics JSON)**: Done — `data/per_trial_metrics.json` (the
  task-specific dump; `results/metrics.json` holds only the registered DSI metric).
* **REQ-6 (per-mode 2-panel and 3-mode summary plots)**: Done — five PNGs in
  `results/images/`, all embedded in `## Visualisations` above.
* **REQ-7 (`results_summary.md` + `results_detailed.md` with embedded plots and per-mode peak
  amplitudes)**: Done — both files present; this file embeds all five PNGs.
* **REQ-8 (all six trials pass `_assert_bip_positions_baseline`)**: Done — see Verification
  table.
* **REQ-9 (EPSP_PASSIVE PD and ND traces bit-identical because gabaMOD = 0 in both)**: Done —
  numerical confirmation: `peak_v_mv` and `baseline_v_mv` match to machine precision (Examples
  3, 4, 7).
* **REQ-10 (IPSP_PASSIVE peak amplitude in ND > PD)**: **Partial** — numerically ND peak
  amplitude (0.11 mV) is greater than PD (0.10 mV), but both are at the noise floor because
  v_rest ≈ e_SACinhib in this model. The voltage-only protocol cannot resolve the conductance
  difference; this is an unanticipated finding and motivates the SEClamp follow-up
  (S-0065-03).
* **REQ-11 (FULL PD firing rate > ND, consistent with t0020)**: Done — 15 Hz PD vs 1 Hz ND; PD
  matches t0020 mean (14.85 Hz) within Poisson uncertainty.
* **REQ-12 (plots render correctly on GitHub)**: Done — all PNGs embedded with relative
  `images/<name>.png` paths in both `results_summary.md` (via reference to this file) and
  `results_detailed.md`.

</details>
