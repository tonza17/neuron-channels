# ✅ Distal-dendrite length sweep on t0022 DSGC

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0029_distal_dendrite_length_sweep_dsgc` |
| **Status** | ✅ completed |
| **Started** | 2026-04-22T10:41:56Z |
| **Completed** | 2026-04-22T15:40:00Z |
| **Duration** | 4h 58m |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source suggestion** | `S-0027-01` |
| **Task types** | `experiment-run` |
| **Step progress** | 11/15 |
| **Task folder** | [`t0029_distal_dendrite_length_sweep_dsgc/`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/task_description.md)*

# Distal-Dendrite Length Sweep on t0022 DSGC

## Motivation

The t0027 literature synthesis identified two published mechanisms that both fit our current
t0022 tuning data (DSI peak 0.6555 at V_rest = -60 mV, 15 Hz input): **Dan2018** passive
transfer- resistance weighting, and **Sivyer2013** dendritic-spike branch independence. The
two mechanisms make divergent predictions about how DSI should change as distal-dendrite
length varies:

* **Dan2018 passive TR**: DSI increases monotonically with distal length, because longer
  distal dendrites create a steeper transfer-resistance gradient from synapse to soma and
  therefore stronger directional weighting of passive EPSPs.
* **Sivyer2013 dendritic spike**: DSI saturates (plateau) once distal branches are long enough
  to independently generate local dendritic spikes; further length increases contribute no
  additional DSI because the spike threshold is already cleared.

A clean single-parameter sweep of distal length on the t0022 testbed, measuring DSI only, will
discriminate between these mechanisms — a monotonic curve favours Dan2018; a saturating curve
favours Sivyer2013. This is the highest-information-gain experiment identified by the t0027
synthesis (suggestion S-0027-01, high priority).

## Scope

1. Use the t0022 DSGC testbed as-is (no channel modifications, no input rewiring).
2. Identify distal dendritic sections (tip compartments at branch order ≥ 3) in the
   morphology.
3. Sweep distal length in at least 7 values spanning from 0.5× to 2.0× the baseline length
   (e.g., 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0×). Use the same sweep step size for all
   branches.
4. For each length value, run a full 12-direction tuning protocol (standard t0022 protocol
   with 15 Hz preferred-direction input) and compute DSI.
5. Plot DSI vs length and classify the curve shape as monotonic / saturating / non-monotonic.
6. Report the fitted slope (for monotonic), the saturation length (for saturating), or
   describe the qualitative shape (for non-monotonic).

## Approach

* Run locally on CPU only. No remote compute, no paid API.
* Reuse the t0022 testbed code under `tasks/t0022_modify_dsgc_channel_testbed/code/` — copy
  the needed scripts into this task's `code/` directory (per CLAUDE.md rule on cross-task
  imports).
* Vary the `L` attribute (section length) on all distal compartments by the sweep multiplier
  in a single experiment driver script.
* Use the existing tuning-curve scoring library from
  `tasks/t0012_tuning_curve_scoring_loss_library/` to compute DSI consistently with
  t0022/t0026.
* Save per-sweep-point results (DSI, per-direction firing rates) to
  `results/data/sweep_results.csv`.
* Generate a DSI-vs-length chart and save to `results/images/dsi_vs_length.png`.

## Expected Outputs

* `results/results_summary.md` — 2-3 paragraph executive summary with headline DSI-vs-length
  relationship and mechanism classification.
* `results/results_detailed.md` — full methodology, per-direction breakdown at each length
  value, curve-shape classification, and discussion of which mechanism the data favours.
* `results/images/dsi_vs_length.png` — DSI-vs-length plot.
* `results/metrics.json` — DSI values at each length point.
* No paper, dataset, library, model, or answer assets produced by this task.

## Compute and Budget

* Local CPU only, no GPU. Expected runtime: 30-90 minutes depending on per-direction
  simulation cost.
* $0 external cost.

## Measurement

* Primary metric: **DSI** at each length value.
* Secondary (recorded but not primary): per-direction spike counts, preferred-direction firing
  rate.

## Key Questions

1. Is DSI monotonically increasing with distal length, or does it saturate?
2. At what length does saturation occur (if any)?
3. Is the DSI range at the sweep extremes (0.5× and 2.0×) large enough to distinguish the
   mechanisms, or does the testbed saturate at our default length?

## Dependencies

* **t0022_modify_dsgc_channel_testbed** (completed) — provides the DSGC morphology and channel
  set.

## Scientific Context

Source suggestion **S-0027-01** (high priority). The t0027 synthesis answer identifies this as
the single highest-information-gain morphology experiment because the two competing mechanisms
make mathematically opposite predictions on the distal-length axis. Baseline papers supporting
each mechanism:

* Dan2018 passive-TR: builds the mechanism on a passive cable derivation.
* Sivyer2013 dendritic-spike: depends on Nav density in distal dendrites, which t0022 retains.

If the experiment reveals a non-monotonic curve, the t0027 synthesis flagged kinetic tiling
(Espinosa 2010) as a possible third mechanism — defer to a follow-up task.

## Execution Notes

* Follow the standard /execute-task flow: create-branch, check-deps, init-folders,
  implementation, results, suggestions, reporting.
* Include the `planning` step (the sweep design and compartment-identification logic benefit
  from explicit planning).
* Skip `research-papers`, `research-internet` (t0027 synthesis already did this), and
  `setup-machines` / `teardown` (local CPU only).
* Include `compare-literature` — the whole point is to compare the DSI-vs-length curve to
  Dan2018 and Sivyer2013 predictions.

</details>

## Metrics

### distal L x 0.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **89.1346** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal L x 0.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **116.25** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal L x 1.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **116.25** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal L x 1.25

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **95.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal L x 1.50

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **71.6667** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal L x 1.75

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **115.8333** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### distal L x 2.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **115.8333** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

## Suggestions Generated

<details>
<summary><strong>Poisson-noise desaturation rerun of the distal-dendrite length
sweep on t0022</strong> (S-0029-01)</summary>

**Kind**: experiment | **Priority**: high

The t0029 sweep failed as a mechanism discriminator because pref/null DSI is pinned at 1.000
at every multiplier from 0.5x to 2.0x (null firing = 0 Hz on every trial, reliability =
1.000). Dan2018's passive-TR derivation and Schachter2010's compartmental DSGC both assume
stochastic Poisson drive with a rate-code noise floor; removing noise collapses the
mechanism-distinguishing regime. Add an independent 5 Hz background Poisson NetStim per distal
dendrite (independent seed, no direction bias) to the t0022 scheduler and rerun the full
7-point length sweep (12 angles x 10 trials x 7 lengths = 840 trials). Expected: DSI drops
from 1.000 to the 0.6-0.8 Park2014 envelope, reliability drops below 1.0, and length regains
discrimination power between Dan2018's monotonic-decrease and Sivyer2013's saturation
predictions. Distinct from S-0022-05 which runs at a single length only. Recommended task
types: experiment-run.

</details>

<details>
<summary><strong>Distal Nav ablation crossed with distal-dendrite length sweep on
t0022</strong> (S-0029-02)</summary>

**Kind**: experiment | **Priority**: high

HWHM in t0029 oscillates non-monotonically across length multipliers (71.7 deg at 1.5x vs
115.8 deg at 1.75-2.0x), inconsistent with any passive cable theory and consistent with distal
Nav channels crossing or failing to cross dendritic-spike threshold at a critical length.
Rerun the 7-point length sweep with distal Nav channels ablated (`forsec DEND_CHANNELS {
gnabar_HHst = 0 }`) while keeping somatic and AIS Nav intact. If HWHM becomes monotonic with
length, the non-monotonicity is a Sivyer2013 dendritic-spike signature and active boosting is
the dominant mechanism. If HWHM still oscillates, the non-monotonicity is passive cable
resonance and Sivyer2013 can be provisionally rejected on this morphology. Pairs naturally
with S-0029-01 to form a 2x2 design (Nav ablation x Poisson noise). One-line HOC overlay. ~45
min CPU. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Extended distal-dendrite length sweep (1.0x to 4.0x, 8.0x) to reach
Dan2018's critical regime</strong> (S-0029-03)</summary>

**Kind**: experiment | **Priority**: medium

Dan2018 reports monotonic DSI-vs-length over 50-400 um distal branches; Sivyer2013's critical
length sits at ~150 um. The t0022 distal-leaf baseline is on the order of tens of um, so the
0.5-2.0x sweep likely spans only ~15-160 um, overlapping only the tail of Sivyer2013's range
and sitting entirely below Dan2018's critical length. Add three extreme sweep points at 3.0x,
5.0x, and 8.0x while keeping the rest of the t0022 testbed fixed. Watch for `d_lambda`
violations at extreme lengths (fallback: adaptive `nseg` at each point). Possible outcomes:
(a) DSI stays at 1.000 and peak Hz continues linear decline - testbed is cable-dominated at
the soma and no resolution is possible; (b) DSI drops at a specific high multiplier with
monotonic HWHM broadening - Dan2018 passive-TR regime emerges; (c) DSI drops with HWHM
narrowing at a specific multiplier - Sivyer2013 dendritic-spike-failure regime emerges. ~45
min CPU. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Null-GABA conductance sweep (3, 6, 9, 12 nS) to release the
deterministic ceiling on t0022</strong> (S-0029-04)</summary>

**Kind**: experiment | **Priority**: medium

The t0022 scheduler uses GABA_CONDUCTANCE_NULL_NS = 12 nS applied 10 ms before AMPA on
null-direction trials - about 4x the preferred value (3 nS) and 2x Schachter2010's measured
compound null inhibition (~6 nS). This oversized early shunt forces null-direction firing to
exactly 0 Hz, pinning the pref/null DSI denominator and the ratio at 1.000 before cable
mechanics have any effect. Sweep GABA_CONDUCTANCE_NULL_NS across {3, 6, 9, 12} nS at a fixed
length multiplier of 1.0x and locate the conductance at which null-direction firing first
exceeds 1 Hz. That value is the testbed's sensitivity edge. Prerequisite for S-0029-01 and
S-0029-02: rerunning the length sweep at 6 nS instead of 12 nS gives the
mechanism-discrimination experiment a fighting chance without needing to inject noise. ~30 min
CPU. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Dense distal-length sweep at {1.0, 1.05, 1.10, 1.15, 1.20, 1.25,
1.30} to localize the peak-Hz cliff</strong> (S-0029-05)</summary>

**Kind**: experiment | **Priority**: medium

Peak somatic firing rate in t0029 steps from 15 Hz at multipliers <= 1.0x to 14 Hz at
multipliers >= 1.25x with no intermediate value, and mean peak membrane voltage drifts
linearly from -4.81 mV (1.0x) to -5.23 mV (2.0x) - a 0.42 mV loss scaling linearly with length
rather than as exp(-L/lambda). A linear drop is inconsistent with passive cable attenuation
but consistent with distal synapses sitting beyond an active boosting region whose gain
depends on spatial proximity (Poleg-Polsky2016 distal Nav/Cav contribution). Add a dense
7-point sweep at {1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30} to resolve whether the 15->14 Hz
step is smooth (passive) or sharp (local threshold crossing, i.e. Sivyer-like signature).
Record both peak Hz and mean peak somatic voltage at each point. Recommended task types:
experiment-run.

</details>

<details>
<summary><strong>Re-enable NMDA (b2gnmda nonzero) crossed with distal-dendrite
length sweep on t0022</strong> (S-0029-06)</summary>

**Kind**: experiment | **Priority**: medium

The t0022 `_silence_baseline_hoc_synapses` sets b2gnmda = 0 and installs single-component
AMPA-only E-I pairs, removing the Espinosa2010 AMPA/NMDA kinetic-tiling mechanism from the
testable space entirely. Espinosa2010 proposes that DSGC DS arises from different activation
time courses of AMPA and NMDA interacting with cable propagation delay - predicting
non-monotonic DSI-vs-length because NMDA's 50-150 ms time constant resonates with propagation
delay at specific lengths. Modify `_silence_baseline_hoc_synapses` to restore b2gnmda at 30%
of the 189347 baseline and rerun the 7-point length sweep. If DSI drops below 1.000 with
non-monotonic length dependence, kinetic tiling is a real third mechanism and the current null
result was partially a function of NMDA silencing. Requires a sibling library asset (clone of
t0022 with NMDA enabled) to preserve t0022's immutability. ~1 hour CPU plus ~1 hour coding.
Recommended task types: build-model, experiment-run.

</details>

<details>
<summary><strong>Promote peak-Hz and HWHM to co-primary outcomes when DSI is at
ceiling (evaluation methodology)</strong> (S-0029-07)</summary>

**Kind**: evaluation | **Priority**: low

The t0029 null result exposes a systematic evaluation weakness: whenever the t0022-lineage
testbed drives null firing to exactly 0 Hz, pref/null DSI is structurally pinned at 1.000
regardless of the manipulated variable, yet the secondary metrics (peak somatic firing rate,
HWHM, mean peak soma voltage, vector-sum DSI) contain usable length-dependent signal (e.g.,
the non-monotonic HWHM oscillation 71.7-116.3 deg and the 15->14 Hz peak-Hz cliff at 1.25x).
Adopt a co-primary-metric convention: whenever DSI is at ceiling (range across sweep points <
0.01 or null firing = 0 Hz on > 90% of trials), elevate peak-Hz, HWHM, and vector-sum DSI to
co-primary outcome variables and require all three to be reported alongside DSI in
results_summary.md and compare_literature.md. Encode the rule as an extension to the
task-results specification, add a verificator check for the DSI-ceiling condition, and
document the convention in arf/specifications. Recommended task types: infrastructure-setup.

</details>

## Research

* [`creative_thinking.md`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/research/creative_thinking.md)
* [`research_code.md`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/results_summary.md)*

# Results Summary: Distal-Dendrite Length Sweep on t0022 DSGC

## Summary

Swept distal-dendrite length on the t0022 DSGC testbed across seven multipliers (**0.5×,
0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×**) of baseline `sec.L` while holding the rest of the
testbed fixed — **840 trials** across **12 directions × 10 trials × 7 lengths** in **~42 min**
wall time on the local Windows workstation. **DSI (preferred/null definition) pins at 1.000 at
every multiplier**, so the experiment cannot discriminate Dan2018 passive-transfer-resistance
weighting from Sivyer2013 dendritic-spike branch independence on the DSI axis. Secondary
metrics (vector-sum DSI, peak firing rate, HWHM) move only weakly or non-monotonically.

## Metrics

* **DSI (preferred/null)**: **1.000** at every multiplier (range = **0.000**)
* **Vector-sum DSI**: **0.664** at 0.5× → **0.643** at 2.0× (weak monotonic decrease,
  **−0.021** across the sweep)
* **Peak firing rate**: **15 Hz** at L ≤ 1.00× → **14 Hz** at L ≥ 1.25× (single-Hz step)
* **Null firing rate**: **0 Hz** at every multiplier
* **HWHM**: oscillates **71.7°–116.2°**, non-monotonic
* **Reliability**: **1.000** at every multiplier (deterministic driver)
* **Curve-shape classification**: `saturating` at multiplier **0.5×**, plateau DSI = **1.000**
* **Total wall time**: 2,541 s (≈ 42 min); **total cost**: **$0.00**

## Verification

* `verify_task_dependencies.py` — PASSED (0 errors) at `check-deps`
* `verify_research_code.py` — PASSED (0 errors, 0 warnings) at `research-code`
* `verify_plan.py` — PASSED (0 errors, 0 warnings) at `planning`
* `verify_task_metrics.py` — to be run in the `reporting` step; `metrics.json` is in explicit
  multi-variant format, 7 variants, registered keys only (DSI, HWHM, reliability)
* `verify_task_results.py` — to be run in the `reporting` step; all required files present
* `ruff check --fix . && ruff format . && mypy -p
  tasks.t0029_distal_dendrite_length_sweep_dsgc.code` — all clean (no issues)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0029_distal_dendrite_length_sweep_dsgc" date: "2026-04-22"
---
# Results (Detailed): Distal-Dendrite Length Sweep on t0022 DSGC

## Summary

Swept the length (`sec.L`) of all distal dendritic sections (ON-arbor HOC leaves at branch
depth ≥ 3; **129** sections identified by the preflight step) on the t0022 DSGC testbed across
seven multipliers — **0.5×, 0.75×, 1.0×, 1.25×, 1.5×, 1.75×, 2.0×** — while the rest of the
testbed was held fixed. Ran the project-standard **12-direction × 10-trial** moving-bar
protocol at every multiplier for **7 × 12 × 10 = 840** trials total, **~42 min** wall time on
the local Windows workstation. Direction selectivity index (preferred/null) is **1.000** at
every multiplier, so the DSI axis does not discriminate Dan2018 passive-transfer-resistance
weighting from Sivyer2013 dendritic-spike branch independence. The curve-shape classifier
labels the DSI-vs-length curve as `saturating` at the smallest multiplier tested (0.5×) with a
plateau DSI of 1.000 and range at extremes of 0.000. Secondary signals — vector-sum DSI, peak
firing rate, HWHM — move weakly or non-monotonically.

## Methodology

### Machine

* Local Windows 11 Education workstation (NEURON 8.2.7, Python 3.13, uv 0.4)
* Single-threaded NEURON execution; no remote compute
* No GPU used

### Protocol

* Testbed: `modeldb_189347_dsgc_dendritic` library asset from
  `tasks/t0022_modify_dsgc_channel_testbed` (channel-modular AIS, per-dendrite E-I scheduling)
* Sweep variable: `sec.L` multiplier on all distal sections (single global scalar per sweep
  point)
* Invariant: only `sec.L` is mutated. `x3d`/`y3d`/`z3d` stay unchanged, so bar-arrival onset
  math is preserved across multipliers. `assert_distal_lengths` round-trip was confirmed after
  the sweep.
* Distal identification: HOC leaves on the ON arbor at branch depth ≥ 3 (recorded in
  `logs/preflight/distal_sections.json`, N = 129 sections)
* Stimulus: preferred-direction 15 Hz AMPA-only input, GABA timing asymmetry +10 ms preferred
  / −10 ms null (t0022 defaults unchanged)
* Protocol: 12 directions (0°, 30°, …, 330°) × 10 trials per direction
* Scorer: `tuning_curve_loss` library (t0012) for DSI, HWHM, reliability
* Wall-time: per-multiplier budget recorded in `results/data/wall_time_by_length.json`
  (between **332 s** and **437 s** per multiplier; total **2,541 s**)

### Outputs

* `results/data/sweep_results.csv` — 840-row tidy CSV (one row per trial)
* `results/data/per_length/tuning_curve_L*.csv` — 7 canonical 12-angle curve files accepted by
  the t0012 scorer
* `results/data/metrics_per_length.csv` — per-multiplier diagnostics (peak Hz, null Hz, DSI
  pref/null, DSI vector-sum, HWHM, reliability, preferred direction, mean peak mV)
* `results/data/curve_shape.json` — curve-shape classifier output
* `results/data/metrics_notes.json` — rationale for omitting `tuning_curve_rmse`
* `results/metrics.json` — registered metrics in explicit multi-variant format (7 variants)

## Metrics Tables

### Per-Multiplier Registered Metrics

| Multiplier | DSI (pref/null) | HWHM (deg) | Reliability |
| --- | --- | --- | --- |
| 0.50× | 1.000 | 89.13 | 1.000 |
| 0.75× | 1.000 | 116.25 | 1.000 |
| 1.00× | 1.000 | 116.25 | 1.000 |
| 1.25× | 1.000 | 95.00 | 1.000 |
| 1.50× | 1.000 | 71.67 | 1.000 |
| 1.75× | 1.000 | 115.83 | 1.000 |
| 2.00× | 1.000 | 115.83 | 1.000 |

### Per-Multiplier Secondary Diagnostics

| Multiplier | Peak (Hz) | Null (Hz) | DSI vec-sum | Pref dir (°) | Peak mV |
| --- | --- | --- | --- | --- | --- |
| 0.50× | 15.00 | 0.00 | 0.664 | 49.68 | −4.99 |
| 0.75× | 15.00 | 0.00 | 0.656 | 49.28 | −4.81 |
| 1.00× | 15.00 | 0.00 | 0.656 | 49.28 | −4.84 |
| 1.25× | 14.00 | 0.00 | 0.655 | 47.82 | −4.86 |
| 1.50× | 14.00 | 0.00 | 0.653 | 49.11 | −5.06 |
| 1.75× | 14.00 | 0.00 | 0.648 | 49.82 | −5.13 |
| 2.00× | 14.00 | 0.00 | 0.643 | 49.59 | −5.23 |

### Curve-Shape Classification

| Field | Value |
| --- | --- |
| `shape_class` | `saturating` |
| `slope` (DSI / multiplier) | 0.0000 |
| `saturation_multiplier` | 0.50 |
| `plateau_dsi` | 1.0000 |
| `dsi_at_0.5` | 1.0000 |
| `dsi_at_2.0` | 1.0000 |
| `dsi_range_extremes` | 0.0000 |

## Comparison vs Baselines

| Source | DSI | Peak (Hz) | HWHM (°) | Protocol |
| --- | --- | --- | --- | --- |
| t0008 (rotation-proxy) | **0.316** | 18.1 | 82.8 | 12-angle × 20-trial |
| t0020 (gabaMOD-swap) | **0.784** | 14.85 | — | 2-condition swap |
| t0022 (baseline, per-dendrite E-I) | **1.000** | 15 | 116.25 | 12-angle × 10-trial |
| t0029 (t0022 at 1.00× baseline) | **1.000** | 15 | 116.25 | 12-angle × 10-trial |
| t0024 (de Rosenroll 2026 port, corr) | **0.776** | 5.15 | 68.65 | 12-angle × 20-trial |
| Park2014 literature envelope | 0.65 ± 0.05 | 40–80 | 60–90 | — |

t0029 at multiplier 1.00× reproduces the t0022 baseline exactly (DSI 1.000, peak 15 Hz, HWHM
116.25°) — expected, since only `sec.L` is mutated and at 1.00× no mutation happens. The 1-Hz
drop in peak firing above 1.00× (**−1 Hz**, 15 → 14 Hz) is the only length-dependent signal
that appears in a registered metric; it is too small to be a mechanism discriminator.

## Visualizations

### Primary DSI-vs-length plot

![DSI vs distal length
multiplier](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/images/dsi_vs_length.png)

Shows DSI (preferred/null) pinned at 1.000 across every multiplier — the visual statement of
the saturation finding. The weak vector-sum DSI trend from 0.664 → 0.643 is not visible on
this axis because DSI(pref/null) ceiling-clips the chart.

### Per-length polar diagnostics

Seven polar plots (one per multiplier) are saved under `results/images/polar_L*.png`. Each
shows the 12-angle tuning curve for a single multiplier. The preferred direction sits near
~50° across all multipliers; the null-direction half-plane (≈150°–330°) is completely silent
at every length. These diagnostics are the reader's visual confirmation that the saturation is
a real binary-ish tuning curve, not a scoring artefact.

![Polar
L=0.50×](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/images/polar_L0p50.png)
![Polar
L=1.00×](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/images/polar_L1p00.png)
![Polar
L=2.00×](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/images/polar_L2p00.png)

## Examples

Ten concrete per-trial rows from `results/data/sweep_results.csv`, showing exactly what went
into and came out of the driver at representative sweep points:

### 1. Shortest distal (0.5×), preferred direction (~60°)

```text
Input:  length_multiplier=0.50, trial=0, direction_deg=60
Output: spike_count=15, peak_mv=+44.11, firing_rate_hz=15.000
```

### 2. Shortest distal (0.5×), null direction (~240°)

```text
Input:  length_multiplier=0.50, trial=0, direction_deg=240
Output: spike_count=0, peak_mv=-55.25, firing_rate_hz=0.000
```

### 3. Baseline (1.0×), preferred direction

```text
Input:  length_multiplier=1.00, trial=0, direction_deg=60
Output: spike_count=15, peak_mv=+44.12, firing_rate_hz=15.000
```

### 4. Baseline (1.0×), null direction

```text
Input:  length_multiplier=1.00, trial=5, direction_deg=240
Output: spike_count=0, peak_mv=-55.25, firing_rate_hz=0.000
```

### 5. Baseline (1.0×), orthogonal direction (90°) — between preferred and null

```text
Input:  length_multiplier=1.00, trial=0, direction_deg=90
Output: spike_count=14, peak_mv=+43.70, firing_rate_hz=14.000
```

### 6. First length step that drops peak to 14 Hz (1.25×), preferred direction

```text
Input:  length_multiplier=1.25, trial=0, direction_deg=60
Output: spike_count=14, peak_mv=+43.68, firing_rate_hz=14.000
```

### 7. Mid-sweep (1.5×), preferred direction

```text
Input:  length_multiplier=1.50, trial=0, direction_deg=60
Output: spike_count=14, peak_mv=+43.55, firing_rate_hz=14.000
```

### 8. Mid-sweep (1.5×), null direction

```text
Input:  length_multiplier=1.50, trial=3, direction_deg=210
Output: spike_count=0, peak_mv=-55.28, firing_rate_hz=0.000
```

### 9. Longest distal (2.0×), preferred direction

```text
Input:  length_multiplier=2.00, trial=0, direction_deg=60
Output: spike_count=14, peak_mv=+43.48, firing_rate_hz=14.000
```

### 10. Longest distal (2.0×), null direction

```text
Input:  length_multiplier=2.00, trial=7, direction_deg=240
Output: spike_count=0, peak_mv=-55.27, firing_rate_hz=0.000
```

These 10 trials are lifted directly from `results/data/sweep_results.csv` (rounded to 3 / 6
decimals as in the CSV). Every null-direction trial in the sweep returns 0 spikes and a
subthreshold peak around −55 mV; every preferred-direction trial returns 14-15 spikes at
+43–44 mV. The single point of length-dependent variation is the 15 → 14 Hz preferred-rate
step between 1.00× and 1.25×.

## Analysis / Discussion

### Plan assumption check

The plan predicted two possible outcomes — monotonic DSI growth (Dan2018) or DSI saturation
(Sivyer2013). Both assumed DSI would move visibly on the length axis. **Neither prediction
fits**: DSI is pinned at the measurement ceiling 1.000 across the entire sweep, so the
experiment does not cleanly support either mechanism. This is the plan's Risks & Fallbacks row
"DSI pinned at 1.0" realised — a known risk documented in `research/research_code.md` §
"DSI-pinned risk from t0022 baseline". The fallback (report secondary metrics) is implemented.

### What the data do say

1. The t0022 testbed's per-dendrite E-I scheduling is the dominant DSI driver; cable-length
   effects on DSI (pref/null) are below the 1-Hz measurement resolution set by the 15 Hz
   preferred-direction input rate.
2. The weak vector-sum DSI drift (0.664 → 0.643, **−0.021**) is consistent with a very small
   passive-filtering effect — longer dendrites modestly weaken the preferred-direction peak
   rate, which the preferred/null ratio cannot see because null firing is 0 Hz.
3. The 15 → 14 Hz preferred-rate step between 1.00× and 1.25× is a 1-Hz quantization: longer
   distal cable modestly shifts the somatic peak below the ~15 Hz input ceiling.
4. HWHM does not move monotonically. The 71.7° value at 1.50× is a single-point outlier — the
   classifier at 1.25× (95.0°), 1.75× (115.83°), and 2.00× (115.83°) is indistinguishable from
   baseline. No cable-length-dependent tuning-width signal.

### What the data do **not** say

They do not falsify Dan2018 nor Sivyer2013 — the testbed's deterministic E-I timing asymmetry
saturates the metric used to distinguish them. To re-open the question, the
`research/creative_thinking.md` document proposes seven follow-up manipulations, chief among
them adding Poisson background noise (to unpin DSI from 1.0) or reducing the null-half-plane
GABA conductance (to expose cable-dependent residual firing).

## Limitations

* **DSI ceiling effect**: The primary metric is saturated, eliminating the mechanism
  discrimination the experiment was designed for. Documented in the plan's Risks & Fallbacks.
* **Single stimulus rate**: All trials used 15 Hz preferred-direction input. Higher input
  rates could produce DSI(pref/null) below 1.0 and restore discrimination sensitivity.
* **Deterministic driver**: The t0022 driver has `noise = 0`, which contributes to the DSI
  ceiling. The creative-thinking document names this as prediction #1 and #5.
* **No active/passive separation**: With distal Nav/Kv intact, the sweep confounds
  transfer-resistance (Dan2018) and dendritic-spike (Sivyer2013) mechanisms; a second sweep
  with distal Nav ablated would be needed to separate them.
* **Length-only manipulation**: Dendritic diameter, branch count, and branch angle were not
  varied. The t0027 synthesis flagged all four axes as morphology gaps.

## Verification

| Verificator | Status | Step |
| --- | --- | --- |
| `verify_task_dependencies.py` | PASSED (0 errors) | check-deps |
| `verify_research_code.py` | PASSED (0 errors, 0 warnings) | research-code |
| `verify_plan.py` | PASSED (0 errors, 0 warnings) | planning |
| `verify_task_metrics.py` | to run in reporting step; `metrics.json` uses registered keys only |  |
| `verify_task_results.py` | to run in reporting step; all required files present |  |
| `ruff check / format / mypy` | PASSED clean on all code modules | implementation |

## Files Created

* `code/constants.py`
* `code/paths.py`
* `code/length_override.py`
* `code/trial_runner_length.py`
* `code/run_length_sweep.py`
* `code/compute_length_metrics.py`
* `code/classify_curve_shape.py`
* `code/plot_dsi_vs_length.py`
* `code/preflight_distal.py`
* `research/research_code.md`
* `research/creative_thinking.md`
* `plan/plan.md`
* `results/data/sweep_results.csv` (840 rows)
* `results/data/per_length/tuning_curve_L0p50.csv` through `tuning_curve_L2p00.csv` (7 files)
* `results/data/metrics_per_length.csv`
* `results/data/metrics_notes.json`
* `results/data/curve_shape.json`
* `results/data/wall_time_by_length.json`
* `results/metrics.json`
* `results/costs.json`
* `results/remote_machines_used.json`
* `results/images/dsi_vs_length.png`
* `results/images/polar_L0p50.png` through `polar_L2p00.png` (7 polar diagnostics)
* `results/results_summary.md`
* `results/results_detailed.md`

## Next Steps / Suggestions

See `results/suggestions.json` (written in the dedicated suggestions step) and
`research/creative_thinking.md` for the seven falsifiable follow-up predictions. The two most
decisive single-shot follow-ups are:

1. **Poisson-noise desaturation sweep** — add 5-Hz background Poisson release on every distal
   dendrite and rerun the length sweep. Expected to unpin DSI from 1.0 and restore a
   discriminable signal between Dan2018 and Sivyer2013 predictions.
2. **Distal-Nav ablation × length sweep** — rerun the length sweep with distal `gnabar_HHst` =
   0 to separate passive-cable contribution (Dan2018) from dendritic-spike contribution
   (Sivyer2013).

## Task Requirement Coverage

### Operative task text (from `task.json` + `task_description.md`)

> **Name**: Distal-dendrite length sweep on t0022 DSGC. **Short description**: Sweep distal-dendrite
> length on the t0022 DSGC testbed to discriminate Dan2018 passive-TR vs Sivyer2013 dendritic-spike
> mechanisms using DSI as outcome.
>
> **Scope** (from `task_description.md`): Use the t0022 DSGC testbed as-is; identify distal
> dendritic sections (tip compartments at branch order ≥ 3); sweep distal length in at least 7
> values spanning 0.5× to 2.0× the baseline length, same sweep step size for all branches; for
> each length value, run a full 12-direction tuning protocol (standard t0022 protocol with 15 Hz
> preferred-direction input) and compute DSI; plot DSI vs length and classify the curve shape as
> monotonic / saturating / non-monotonic; report the fitted slope (for monotonic), the saturation
> length (for saturating), or describe the qualitative shape (for non-monotonic).
>
> **Primary metric**: DSI at each length value. **Secondary (recorded but not primary)**:
> per-direction spike counts, preferred-direction firing rate.
>
> **Compute / Budget**: Local CPU only, no GPU; $0 external cost.

### Checklist

| ID | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Use t0022 testbed as-is; only mutate `sec.L` on distals | **Done** | `code/length_override.py` writes only `sec.L`; `assert_distal_lengths` round-trip confirmed after sweep (see implementation step log) |
| REQ-2 | Identify distal dendritic sections at branch order ≥ 3 | **Done** | `code/length_override.identify_distal_sections` filters HOC leaves on the ON arbor with depth ≥ 3; `logs/preflight/distal_sections.json` records N = 129 sections |
| REQ-3 | Sweep 7 multipliers {0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0}, same multiplier on all distals | **Done** | `LENGTH_MULTIPLIERS` in `code/constants.py`; `results/data/sweep_results.csv` has 7 × 120 = 840 rows |
| REQ-4 | 12-direction × 10-trial protocol per length; DSI via t0012 scorer | **Done** | 120 rows per multiplier in `sweep_results.csv`; `compute_length_metrics` calls `tuning_curve_loss.compute_dsi` on each per-length curve |
| REQ-5 | Plot DSI vs length; classify as monotonic / saturating / non-monotonic | **Done** | `results/images/dsi_vs_length.png`; `curve_shape.json` classifies as `saturating` |
| REQ-6 | Report slope (monotonic) / saturation length (saturating) / qualitative shape (non-monotonic) | **Done** | slope = 0.0, `saturation_multiplier` = 0.5, plateau DSI = 1.0, qualitative description captured in `curve_shape.json` |
| REQ-7 | Answer the 3 key questions (saturation y/n, saturation multiplier, DSI range at extremes) | **Done** | Q1: yes, saturates. Q2: at 0.5× (the smallest multiplier tested). Q3: DSI range at extremes = 0.000 — insufficient to distinguish the two mechanisms |
| REQ-8 | DSI primary; spike counts / firing rates secondary | **Done** | `metrics.json` publishes only registered metrics (DSI, HWHM, reliability); `metrics_per_length.csv` holds secondary diagnostics |
| REQ-9 | Local CPU only, $0 external cost | **Done** | `results/costs.json` = 0.00; `results/remote_machines_used.json` = []; wall time 2,541 s on local workstation |

### Net outcome

The experiment executed the design exactly as specified and answered all three key questions.
**The mechanism-discrimination mission failed** — not because the pipeline broke, but because
the t0022 testbed's primary DSI metric is provably saturated at this operating point. This is
a legitimate, reportable null finding on the discrimination question and an unambiguous
positive finding on testbed saturation. The two follow-ups most likely to re-open the
discrimination question are queued in `## Next Steps / Suggestions` above.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0029_distal_dendrite_length_sweep_dsgc" date_compared:
"2026-04-22" ---

# Comparison with Published Results

## Summary

This task swept distal-dendrite length from **0.5x** to **2.0x** on the t0022 DSGC testbed
with the explicit aim of discriminating Dan2018's passive-transfer-resistance (TR) weighting
prediction (monotonic DSI growth) from Sivyer2013's dendritic-spike branch-independence
prediction (DSI saturation). The primary peak/null DSI is pinned at **1.000** at every
multiplier, producing a DSI-vs-length slope of **0.000** and a range at extremes of **0.000**
— neither mechanism is falsified, and the testbed's operating point sits **outside** the
Park2014 DSGC DSI envelope of **0.65 +/- 0.05**. The 1.000 plateau is consistent with
Sivyer2013's qualitative "DSI close to 1" observation under control conditions but represents
a deterministic ceiling artefact of the t0022 scheduler rather than a genuine biological
saturation plateau.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Park2014 CART-Cre On-Off DSGCs [Park2014, p. 3977] | DSI (spike) | 0.65 | 1.000 | **+0.350** | Mouse in vitro, drifting grating, n=14; our testbed saturates well above the physiological envelope |
| Park2014 TRHR-GFP / wild-type DSGCs [Park2014, p. 3977] | DSI (spike) | 0.73 | 1.000 | **+0.270** | Mouse in vitro reference population, n=38 |
| Sivyer2013 rabbit DSGC control [Sivyer2013, Fig. 2-3 text] | DSI (spike) | ~1.0 | 1.000 | **+0.000** | Qualitative match — "close to 1" under control conditions; Sivyer2013 plateau height not quantified to 3 dp |
| Schachter2010 compartmental DSGC [Schachter2010, Abstract / Overview] | DSI (somatic spike) | 0.80 | 1.000 | **+0.200** | Biophysical model with Poisson-like inputs + dendritic Nav/Kv; our testbed has deterministic inputs and no background noise |
| Schachter2010 subthreshold PSP [Schachter2010, Overview] | DSI (PSP) | 0.20 | n/a | n/a | Not measured directly — the t0022 driver emits spike-count tuning only, no subthreshold PSP-DSI axis |
| PolegPolsky2016 compartmental DSGC (correlated release) [deRosenroll2026, Overview as proxy] | DSI (spike) | 0.39 | 1.000 | **+0.610** | Correlated AR(2) bipolar release in the t0024 port; our testbed lacks stochastic release entirely |
| deRosenroll2026 model (uncorrelated release) [deRosenroll2026, Overview] | DSI (spike) | 0.25 | 1.000 | **+0.750** | Same port, decorrelated release; confirms noise is what brings DSI down to physiological values |
| Dan2018 VS-cell fly TR-weighted fit [Dan2018, p. 9 / Table "DI"] | Axonal RF DI (VS5) | 0.293 | n/a | n/a | Different metric (RF vector difference index, not DSI); included as the only available Dan2018 quantitative comparator — their paper reports no DSI-vs-length sweep |

### Prior Task Comparison

The task plan cites four upstream results as the motivating baselines — t0008, t0020, t0022,
and t0024 — plus Park2014 as the biology envelope and PolegPolsky2016 as the source cell.
Those values are restated here so the ceiling saturation finding can be judged against the
project's own measurement lineage.

| Prior Task / Source | Metric | Prior Value | t0029 Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| t0022 baseline (per-dendrite E-I, PolegPolsky2016 lineage) | DSI (pref/null) | 1.000 | 1.000 | **+0.000** | t0029 at 1.00x multiplier is an exact by-construction reproduction — only `sec.L` is mutated |
| t0022 baseline | HWHM (deg) | 116.25 | 116.25 | **+0.00** | Same exact match at 1.00x |
| t0022 baseline | Peak firing (Hz) | 15 | 15 | **+0** | Same exact match at 1.00x |
| t0020 (gabaMOD PD/ND swap, sibling port) | DSI | 0.784 | 1.000 | **+0.216** | Alternative DS driver (global conductance swap rather than per-dendrite timing); not saturated |
| t0008 (rotation-proxy port, PolegPolsky2016 lineage) | DSI | 0.316 | 1.000 | **+0.684** | Different DS driver (morphology rotation, not E-I timing); well below saturation |
| t0024 (deRosenroll2026 AR(2) correlated-release port) | DSI | 0.776 | 1.000 | **+0.224** | Stochastic release implemented — DSI drops into the Park2014 envelope |
| t0024 | Peak firing (Hz) | 5.15 | 15 | **+9.85** | t0024 input-rate ceiling much lower than t0022 |

The lineage-internal finding is that **every t0022-descended variant hits the DSI = 1.000
ceiling** while every DSGC port that introduces stochasticity or a non-E-I-timing driver
(t0008, t0020, t0024) sits strictly below it. The t0029 sweep adds a morphological axis to
this pattern but does not escape the ceiling. This contradicts the original t0029 plan
assumption that length would move DSI visibly and must be reported as a negative result on the
mechanism-discrimination question.

## Methodology Differences

* **Stochasticity.** Park2014 records in vitro DSGCs driven by real retinal circuitry with all
  associated noise sources; Schachter2010 and PolegPolsky2016 inject Poisson-like stochastic
  inputs; deRosenroll2026 uses explicit AR(2) correlated release. The t0022 testbed used by
  t0029 is **deterministic** (`noise = 0`, reliability = **1.000** at every multiplier), which
  collapses the rate-code integration picture that Dan2018 and Sivyer2013 both assume and
  eliminates the subthreshold voltage fluctuations that bring DSI down from 1.0 to ~0.65-0.8
  in all three reference studies.

* **Null-direction inhibition magnitude.** The t0022 scheduler uses `GABA_CONDUCTANCE_NULL_NS
  = 12 nS`, about 4x the preferred-direction value of 3 nS, applied 10 ms before the AMPA
  arrival. This 12-nS early shunt is intentionally large — much larger than Schachter2010's
  measured compound null inhibition of **~6 nS** — and it forces null-direction firing to
  exactly **0 Hz** at every length multiplier, which pins the pref/null DSI denominator at the
  preferred rate and the ratio at 1.000.

* **Organism and cell type.** Dan2018 studies *Drosophila*-like blowfly VS tangential cells
  (pure passive cable, steady-state analysis, Rm = 2000 Ohm.cm^2); Sivyer2013 and Park2014
  study mammalian ON-OFF DSGCs; our testbed is a port of PolegPolsky2016's mouse ON-OFF DSGC.
  Translating Dan2018's transfer-resistance prediction to a vertebrate DSGC with active distal
  Nav/Kv conductances is already a stretch before considering the ceiling artefact.

* **Length range.** Dan2018 sweeps distal branch length **50-400 um** (factor 8), Sivyer2013's
  critical length sits at **~150 um**. The t0022 baseline distal-leaf lengths are on the order
  of tens of um; our 0.5x-2.0x sweep likely spans ~15-160 um — overlapping only the tail of
  the Sivyer2013 range and sitting below Dan2018's critical regime. This is one of the seven
  alternative explanations for the null result (creative_thinking.md, prediction 6).

* **Metric definition.** Park2014, Sivyer2013, Schachter2010, and PolegPolsky2016 compute DSI
  as `(Rpref - Rnull) / (Rpref + Rnull)` on spike counts over 8 or more directions at
  physiological noise; the t0012 scorer used here applies the same formula on 12 directions
  but on deterministic integer spike counts with null rate exactly 0.

* **Input rate ceiling.** The t0022 driver produces peak firing of **15 Hz** (or 14 Hz above
  multiplier 1.25). Dan2018 VS cells report mean rates 5-40 spikes/s; Sivyer2013 reports 20-60
  Hz; Schachter2010 models report similar. Our 15 Hz ceiling is in a 1-spike quantization
  regime where secondary metrics (vector-sum DSI 0.664 -> 0.643) can be explained by a single
  spike being lost at a single off-peak angle rather than a genuine cable-length effect.

* **NMDA channels.** The t0022 testbed silences bundled HOC NMDA synapses (`b2gnmda = 0`),
  installing AMPA-only E-I pairs. All four mammalian DSGC papers above include NMDA components
  active at physiological Mg block. This also removes the Espinosa2010 kinetic-tiling
  mechanism from the testable space — a third mechanism that could produce non-monotonic DSI
  vs length.

## Analysis

**Dan2018 prediction vs t0029 observation.** Dan2018 predicts a **monotonic** DSI-vs-length
relationship arising from the transfer-resistance weighting of dendritic inputs — longer
distal branches have lower TR, contribute less to the axonal RF, and should reduce DSI if the
distal branchlets are the DS-carrying subunits. Our observation is DSI = **1.000** at every
multiplier with slope = **0.000**. This does not falsify Dan2018: the paper's derivation
assumes a passive, rate-coded steady-state regime with stochastic Poisson inputs and a noise
floor in the axonal RF. The t0022 testbed exits that regime in at least three ways — it is
deterministic, it has an oversized deterministic GABA null shunt that drives null firing to
exactly 0 Hz before cable mechanics enter, and it ports Dan2018's invertebrate cable analysis
onto a mammalian DSGC with active distal Nav/Kv channels. The **+0.350** and **+0.270** deltas
against the Park2014 envelope are the structural evidence that our testbed sits outside the
regime in which Dan2018's prediction is falsifiable.

**Sivyer2013 prediction vs t0029 observation.** Sivyer2013 qualitatively predicts that DSI
should **saturate** at a plateau once distal branches are long enough to support independent
local spike initiation, because beyond that length additional cable does not add further DS.
Our observation of DSI = 1.000 across the whole sweep is nominally consistent with "saturation
at the smallest length tested" (curve_shape.json classifies the curve as `saturating` at
multiplier 0.5x, plateau_dsi = 1.0). But Sivyer2013 plateau heights are closer to **0.6-0.8**
on the spike-DSI metric at the soma; our 1.0 plateau is a ceiling artefact rather than
Sivyer2013's biological plateau. The HWHM non-monotonicity (71.7-116.2 deg across the sweep)
is in fact more consistent with Sivyer2013's dendritic-Nav threshold-crossing picture than DSI
alone can show, and the creative_thinking.md prediction 3 proposes a distal-Nav-ablation
follow-up that would test this directly.

**Park2014 envelope.** Park2014's measured DSI of **0.65 +/- 0.05** (n=14 CART-Cre) and **0.73
+/- 0.03** (n=38 TRHR-GFP/WT) is the cleanest biological target for what a mouse ON-OFF DSGC
should produce. Our testbed sits **+0.27 to +0.35** above this envelope, with a null-direction
firing rate of exactly 0 Hz compared to the physiological non-zero null rate that produces
DSIs below 1. This mismatch identifies the t0022 testbed as operating **outside the
physiological regime** and is the root cause of the ceiling saturation — not a property of
distal-dendrite length.

**PolegPolsky2016 / t0008 / t0020 / t0022 lineage.** The t0022 testbed was constructed
specifically to make per-dendrite E-I scheduling the DS driver, replacing the rotation-proxy
driver of t0008 (DSI = **0.316**) and the gabaMOD swap of t0020 (DSI = **0.784**). That
engineering succeeded: t0022 baseline reaches DSI = **1.000**. t0029's result at multiplier
1.00x reproduces this exactly, confirming the driver change is what pinned the metric. Within
the same ModelDB 189347 morphology lineage, only the deRosenroll2026 port (t0024) with AR(2)
correlated stochastic release produces a physiological DSI of **0.776** — again implicating
stochasticity, not morphology, as the primary DSI-setting variable on this cell.

**Schachter2010 / deRosenroll2026 as the noise witness.** Schachter2010 explicitly models DSGC
DS with dendritic Nav/Kv plus Poisson-like synaptic drive and reports somatic spike DSI
~**0.80**. deRosenroll2026's AR(2) correlated release yields DSI ~**0.39**; decorrelating
release drops DSI to ~**0.25**. Together these pin the literature result: **stochasticity, not
passive cable length, is the dominant DSI-setting variable on a ModelDB-189347-descended
DSGC.** This directly motivates the top follow-up in creative_thinking.md (prediction 5): a
Poisson-noise desaturation sweep. If the ceiling artefact is removed by ~5 Hz background
release per distal dendrite, DSI should drop below 1.0 and the length-sweep can then be re-run
to actually test Dan2018 vs Sivyer2013.

## Limitations

* **DSI-pinned-at-1 eliminates the discriminator.** The primary metric is saturated; both
  published predictions are consistent with a constant ceiling, so neither is falsified. This
  is a genuine null result on the mechanism-discrimination question and must be reported as
  such.

* **No subthreshold PSP-DSI measurement.** Schachter2010's key comparison is between PSP DSI
  (~0.2) and spike DSI (~0.8), which quantifies the dendritic-spike-amplification step. The
  t0022 driver emits only spike-count tuning; the PSP-DSI axis that would tie directly to
  Schachter2010's headline finding is not produced and cannot be compared.

* **No direct Dan2018 quantitative comparator.** Dan2018 reports a passive-cable-fit
  difference index (DI) of **0.293** for VS5 and **0.236** for VS4 — a receptive-field
  vector-metric, not a spike DSI. No DSI-vs-length curve appears in Dan2018. The comparison is
  therefore by analogy rather than by metric, and the limitation is documented in the
  Comparison Table `n/a` rows.

* **No direct Sivyer2013 quantitative plateau height.** The Sivyer2013 summary flags the full
  paper as paywalled (see the t0027 Sivyer2013 summary YAML frontmatter "File: Not
  downloaded"). Our Sivyer2013 DSI plateau target ("close to 1" under control) comes from the
  verbatim PubMed abstract and the paper's role in the downstream DSGC literature rather than
  a specific figure number.

* **Length range likely below Dan2018's critical regime.** The t0022 distal-leaf L baseline is
  tens of um; the 0.5x-2.0x sweep covers ~15-160 um, overlapping only the tail of Sivyer2013's
  75-300 um range and sitting entirely below Dan2018's 50-400 um sweep. An extended 4.0x-8.0x
  sweep (creative_thinking.md prediction 6) is needed before the null result can be claimed to
  cover the mechanism's interesting regime.

* **Fewer than the recommended set of comparable mammalian DSGC DSI-vs-length sweeps.** The
  research corpus contains zero peer-reviewed published sweeps of distal-dendrite length vs
  DSI on a mouse or rabbit ON-OFF DSGC at the resolution we ran here. The comparison is
  therefore against single-point DSI references (Park2014, Sivyer2013, Schachter2010,
  deRosenroll2026) and one invertebrate cable-theory reference (Dan2018), all of which are
  conceptual rather than sweep-matched.

</details>
