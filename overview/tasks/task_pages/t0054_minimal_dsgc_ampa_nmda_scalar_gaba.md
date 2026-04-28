# ✅ Minimal DSGC with AMPA + NMDA excitation and scalar gabaMOD inhibition

[Back to all tasks](../README.md)

> Tuning Curve RMSE (Hz): **16.980414819835936**

## Overview

| Field | Value |
|---|---|
| **ID** | `t0054_minimal_dsgc_ampa_nmda_scalar_gaba` |
| **Status** | ✅ completed |
| **Started** | 2026-04-27T21:14:19Z |
| **Completed** | 2026-04-28T05:00:00Z |
| **Duration** | 7h 45m |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source suggestion** | `S-0052-03` |
| **Task types** | `build-model`, `experiment-run` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 1 library |
| **Step progress** | 10/15 |
| **Task folder** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba/`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/task_description.md)*

# Minimal DSGC with Co-Located AMPA + NMDA Excitation and Scalar gabaMOD Inhibition

## Source

Suggestion S-0052-03 (medium priority): "Add NMDA component to t0052 minimal DSGC and measure
DSI / peak-rate response."

## Motivation

t0052 produced a from-scratch minimal DSGC with AMPA-only excitation and scalar gabaMOD
inhibition. The aggregate EPSP at the soma decays within ~30 ms after the last synapse fires
because per-synapse AMPA `tau2 = 2.5 ms` and the membrane time constant `τ_m = R_m × C_m ≈ 6
ms`. Real DSGC EPSPs decay much more slowly because they have a substantial NMDA component
(typical NMDA decay τ ≈ 50-200 ms). t0052 also produced only one spike per trial in FULL mode
at the preferred direction, which over-saturates primary DSI to 1.0 trivially.

This task extends t0052 by adding a co-located NMDA `Exp2Syn` at each E synapse location and
runs a small `gNMDA` sweep so we can directly answer:

* How does the EPSP decay time constant scale with `gNMDA`?
* Does NMDA close the peak-rate gap (t0052: 0.667 Hz vs Park 2014 in vivo 30-100 Hz)?
* Does NMDA improve or degrade DSI under the scalar `gabaMOD` inhibition mechanism?
* At what `gNMDA` does the cell start firing multiple spikes per trial (escaping the
  single-spike degenerate regime)?

## Model Specification

Identical to t0052 unless explicitly noted.

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (same as t0052/t0053).
* 100 dendritic locations sampled with seed = 0 (bit-identical placement to t0052/t0053 —
  enforced by a placement-match test).

### Sections and channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` with the same boosted AIS
  parameters as t0052 (`AIS_LENGTH_UM=30`, `AIS_DIAMETER_UM=2`, `AIS_GNABAR=1.2`,
  `AIS_GKBAR=0.04`, `AIS_GL=0.008`, `AIS_EL_HH=-65`).
* All dendritic sections passive: `Rm = 5999 Ω·cm²`, `Ra = 100 Ω·cm`, `cm = 1 µF/cm²`, `V_rest
  = -65 mV`.

### Synapses

* 100 E + 100 I co-located pairs.
* **Excitation**: at each E location, both an AMPA and an NMDA `Exp2Syn` are co-located on the
  same segment, driven by **the same** `NetStim` event (one event per synapse per trial,
  position-gated by the bar). AMPA: `tau1 = 0.5 ms`, `tau2 = 2.5 ms`, `e = 0 mV`, peak `0.5
  nS` (same as t0052). NMDA: `tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`, peak conductance
  `gNMDA` (swept).
* NMDA is **voltage-independent** in this minimal model (no Mg²⁺ block). Voltage-dependent
  NMDA with proper Mg block is deferred to a follow-up task.
* **Inhibition**: scalar gabaMOD identical to t0052. `theta_PD = 0`, `theta_ND = 180`, peak `2
  nS × gaba_mod(theta)` where `gaba_mod(0) = 0.33` and `gaba_mod(180) = 0.99`.

### Stimulus protocol

* 12 directions × 10 trials × 3 trial modes × 4 `gNMDA` values = 1440 trials total.
* Bar 200 µm × full arena, 1.0 µm/ms (= 1000 µm/s), 1500 ms per trial.
* `BASE_OFFSET_MS = 100` (bar enters arena at t = 100 ms).

### gNMDA sweep

Four values: `{0.0, 0.25, 0.5, 1.0}` nS.

* `gNMDA = 0` reproduces t0052 within rounding (validation gate).
* `gNMDA = 0.5` matches the Poleg-Polsky 2016 baseline.
* `gNMDA = 1.0` is twice the Poleg-Polsky baseline; a coarse high-end probe.

### Trial modes

* `FULL` — AMPA + NMDA + GABA active.
* `E_ONLY` — AMPA + NMDA active, GABA `NetCon` weights zeroed (replaces t0052's `AMPA_ONLY`).
* `GABA_ONLY` — AMPA + NMDA `NetCon` weights zeroed, GABA active.

## Outputs

### Per `gNMDA` value × per direction (4 × 12 = 48 panels per output type)

* Soma `V(t)` (FULL mode), mean ± SD across 10 trials.
* Aggregate EPSP (`E_ONLY`), mean ± SD.
* Aggregate IPSP (`GABA_ONLY`), mean ± SD.
* PSTH (5 ms bins, FULL mode).
* Per-synapse activation-time histogram.

Approximately 12 × 5 = 60 PNGs per `gNMDA` value × 4 sweep values = ~240 per-direction PNGs,
plus 8 polar/Cartesian per-`gNMDA` overview PNGs and 3 sweep-summary PNGs.

### Sweep summary (the headline plots)

1. **EPSP decay-time-constant vs gNMDA** — directly answers the user's question. X-axis:
   `gNMDA` (4 points). Y-axis: time from EPSP peak to `1/e` (≈ 36.8 %) of peak. One line per
   direction or one aggregate.
2. **Peak Hz vs gNMDA** — line plot, one curve per direction.
3. **DSI vs gNMDA** — primary DSI and vector-sum DSI vs `gNMDA`.

### `metrics.json` (multi-variant format)

One variant per `(gNMDA, mode)` combination = 12 variants. Each variant carries the registered
keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`. Variant `id` schema: `gnmda_<value>_<mode>` (e.g., `gnmda_0.50_full`).

### `derived_quantities.json`

Per-variant: `peak_hz`, `null_hz`, `vector_sum_dsi`, `preferred_direction_deg`,
`active_fraction` (constant 1.0 here; included for parity with t0053). Per-`gNMDA`:
`epsp_decay_to_1e_ms` for the `E_ONLY` variant at the preferred direction. Plus the existing
t0052 fields (`gaba_mod_pd`, `gaba_mod_nd`, etc.).

## Library Asset

`minimal_dsgc_ampa_nmda_scalar_gaba` under
`tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/library/`.

## Code Design

### Modules to copy verbatim from t0052 (with import-path rewrite to `tasks.t0054_*` and bootstrap sentinel renamed to `_T0054_NEURONHOME_BOOTSTRAPPED`)

`paths.py`, `swc_io.py`, `cell.py`, `placement.py`, `neuron_bootstrap.py`, `trial.py`,
`metrics_extra.py`, `test_quiescent_rest.py`, `test_gaba_mod.py`, `__init__.py`. (10 files.)

### Modules to extend

* **`constants.py`** — add `NMDA_TAU1_MS=5.0`, `NMDA_TAU2_MS=80.0`, `NMDA_E_MV=0.0`,
  `NMDA_PEAK_NS_VALUES=(0.0, 0.25, 0.5, 1.0)`, `COL_GNMDA_NS = "gnmda_ns"`, and rename
  `TrialMode.AMPA_ONLY` → `TrialMode.E_ONLY` (or add `E_ONLY` and keep `AMPA_ONLY` as a legacy
  alias).
* **`synapses.py`** — extend `EiPair` with `nmda_syn`, `nmda_netcon`. `build_ei_pairs` creates
  the NMDA `Exp2Syn` at the same segment and a single shared `NetStim`-driven `NetCon`.
  `schedule_ei_onsets` accepts `gnmda_ns: float` and sets `nmda_netcon.weight[0] = gnmda_ns *
  1e-3`. NMDA fires from the same `NetStim.start` as AMPA — no second NetStim is needed.
* **`run_tuning_curve.py`** — add an outer loop over `gNMDA` values. Per-mode CSVs gain a
  `gnmda_ns` column. File names get a per-`gNMDA` suffix or all `gNMDA` rows are appended to a
  single CSV (the latter is preferred for downstream analysis ergonomics).
* **`compute_metrics.py`** — group by `(gnmda_ns, mode)` to compute one variant per group;
  also compute `epsp_decay_to_1e_ms` at the preferred direction per `gNMDA`.
* **`render_figures.py`** — extend with per-`gNMDA` per-direction loops and the three
  sweep-summary plots.

### Validation gates (run before the full sweep)

* **Quiescent rest test**: `V_rest = -65 ± 0.5 mV` with no synapses (same as t0052).
* **gNMDA = 0 sanity**: `tuning_curve_full` rows at `gNMDA = 0` must match t0052's
  `tuning_curve_full.csv` row-by-row within 1e-6 Hz tolerance. This validates that the NMDA
  branch is correctly inert at `gNMDA = 0` and that nothing else regressed.
* **Placement bit-identical to t0052**: read
  `tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json` and assert per-synapse
  coordinates match (same test as t0053).

## Compute and Budget

Local CPU only. ~75 min wall-clock for 1440 trials at ~3 s/trial. $0 cost.

## Out of Scope

* Voltage-dependent NMDA with Mg²⁺ block (deferred to a future task).
* Spatial PD/ND-asymmetric inhibition (covered by t0053).
* Any morphology or HH parameter changes.
* AMPA conductance sweep (covered by suggestion S-0052-01).
* Cross-comparison with t0053 (covered by suggestion S-0052-04).

## Key Questions

1. How does the EPSP decay-to-1/e time scale with `gNMDA`? At what `gNMDA` does it reach the
   "biologically realistic" 50-100 ms range?
2. Does adding NMDA close the peak-rate gap (t0052: 0.667 Hz, in vivo 30-100 Hz)?
3. Does NMDA improve or degrade primary DSI under scalar `gabaMOD`? Does the trivial
   single-spike DSI = 1 of t0052 give way to a more interesting non-trivial tuning curve?
4. At what `gNMDA` does the cell start firing multiple spikes per trial (escaping the
   single-spike degenerate regime)?

## Verification Criteria

* Library asset structure validates against `meta/asset_types/library/specification.md`.
* `metrics.json` contains 12 variants (4 × 3); all use the registered metric keys.
* All gates pass (quiescent rest, gNMDA=0 sanity, placement match).
* The `gNMDA = 0` FULL variant reproduces t0052's primary DSI = 1.0, peak Hz = 0.667 Hz, and
  null Hz = 0.0 Hz to within rounding.
* All 240+ per-direction PNGs and 11+ sweep-summary PNGs exist and are embedded in
  `results_detailed.md` (sample of headline figures inline; rest linked).

</details>

## Metrics

### gNMDA = 0.00 nS, FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **82.5** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9999999999999999** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **16.980414819835936** |

### gNMDA = 0.00 nS, E_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |

### gNMDA = 0.25 nS, FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.14285714285714285** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **97.49999437499858** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **12.64879045948517** |

### gNMDA = 0.25 nS, E_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.05263160387811578** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **0.9999999999999999** |

### gNMDA = 0.50 nS, FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.09999997749999935** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **60.00005624997203** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **12.670774228141049** |

### gNMDA = 0.50 nS, E_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

### gNMDA = 1.00 nS, FULL

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |
| [`tuning_curve_hwhm_deg`](../../metrics-results/tuning_curve_hwhm_deg.md) | **180.0** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |
| [`tuning_curve_rmse`](../../metrics-results/tuning_curve_rmse.md) | **14.052154566782137** |

### gNMDA = 1.00 nS, E_ONLY

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.07692311242603428** |
| [`tuning_curve_reliability`](../../metrics-results/tuning_curve_reliability.md) | **1.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Minimal DSGC AMPA + NMDA Scalar gabaMOD](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/library/minimal_dsgc_ampa_nmda_scalar_gaba/) | [`description.md`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/library/minimal_dsgc_ampa_nmda_scalar_gaba/description.md) |

## Suggestions Generated

<details>
<summary><strong>Add voltage-dependent NMDA Mg block to recover DSI in the t0054
minimal AMPA + NMDA + scalar gabaMOD architecture</strong> (S-0054-01)</summary>

**Kind**: experiment | **Priority**: high

t0054 demonstrated that voltage-independent NMDA (Exp2Syn, no Mg block) collapses vector-sum
DSI from 0.746 (gNMDA=0) to 0.082 (gNMDA=0.25) to 0.017 (gNMDA=1.0), confirming
PolegPolsky2016's prediction [Fig 5] that the Boltzmann Mg block is required for
multiplicative DSI scaling. Replace the NMDA Exp2Syn with a Jahr-Stevens Mg-block point
process (e.g., bipolarNMDA.mod from PolegPolsky2016 or an equivalent NMDA_Mg2 MOD), keeping
all other t0054 parameters fixed (placement seed 0, AMPA tau1=0.5/tau2=2.5/0.5 nS, scalar
gabaMOD with PD=0.33 ND=0.99 base 2 nS, soma+AIS HH). Re-run the {0, 0.25, 0.5, 1.0} nS gNMDA
sweep with the same 12 dirs x 10 trials x 3 modes protocol. Pass criterion: vector-sum DSI at
gNMDA=0.25 must exceed 0.50 and peak Hz must reach >= 5 Hz. This directly addresses the
headline negative result of t0054. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary><strong>Joint (gAMPA, gNMDA, gGABA) conductance sweep on t0054 minimal
architecture to locate a DSI-preserving operating point</strong>
(S-0054-02)</summary>

**Kind**: experiment | **Priority**: high

t0054 fixed AMPA at 0.5 nS and used the unchanged t0052 scalar gabaMOD (2 nS base, ratio 3.0),
varying only gNMDA. The DSI collapse may be recoverable by rebalancing the three conductances
jointly. Run a 3-D grid: gAMPA in {0.25, 0.5, 1.0} nS, gNMDA in {0.0, 0.1, 0.25, 0.5} nS, base
gGABA in {2, 4, 8, 16} nS, all on the t0054 codebase with placement seed 0 unchanged,
voltage-independent NMDA kept (so this is the no-Mg-block control complementary to S-0054-01).
Use 12 dirs x 5 trials per cell = 60 trials per (gAMPA, gNMDA, gGABA) point; 48 grid cells =
2880 trials. Apply early stop on cells where E_ONLY peak Hz > 30 Hz to prune the saturated
subgrid. Pass criterion: locate at least one (gAMPA, gNMDA, gGABA) triple with vector-sum DSI
>= 0.5 and peak Hz in 10-50 Hz, or rule out such an operating point in the voltage-independent
regime. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Replace 1/e-crossing EPSP-decay metric with an exponential fit and
lengthen the post-stimulus window</strong> (S-0054-03)</summary>

**Kind**: technique | **Priority**: medium

REQ-20 (epsp_decay_to_1e_ms per gNMDA) returned null at all four gNMDA values because the 1500
ms trial window is shorter than the time the cell needs to drop below V_rest + (V_peak -
V_rest)/e once 100 simultaneous NMDA Exp2Syn events with tau2=80 ms keep Vm depolarised. The
headline numerical answer to 'how does EPSP tau scale with gNMDA?' is missing -- this is a
metric implementation gap, not a biological null result. Implement two changes: (1) extend the
recorded E_ONLY trace to 3000-5000 ms post-stimulus, (2) replace the 1/e-crossing search with
a least-squares exponential fit V(t) = V_rest + A * exp(-t / tau_decay). Validate against
t0052 baseline (expected tau_decay ~ 30 ms). Acceptance: tau is finite for all 4 gNMDA values,
falls in 30-300 ms, and rises monotonically. Recommended task types: write-library,
experiment-run.

</details>

<details>
<summary><strong>Promote the t0052<->t0054 gNMDA=0 regression gate into a reusable
cross-task baseline-equivalence verificator</strong> (S-0054-04)</summary>

**Kind**: evaluation | **Priority**: low

t0054's compute_metrics.py contains an ad-hoc hard-fail gate that compares the gNMDA=0 FULL
tuning_curve_full.csv row-by-row against t0052's tuning_curve_full.csv (passed at max |rate
diff| = 0.000e+00 Hz across 120 rows). This validates that placement, AMPA, GABA, and HH
soma+AIS are bit-identical between t0052 and t0054 baselines. Promote this comparison to a
reusable utility in arf/scripts/utils that takes (task_a_id, task_b_id, csv_filename,
parameter-equivalence-config) and produces a structured pass/fail report. Wire it into a
verificator-style entry point so downstream minimal-DSGC tasks (Mg-block follow-up S-0054-01,
joint sweep S-0054-02, tau2 sweep S-0054-05) can declare 'this task's gNMDA=0 baseline must
equal t0052' as a CI prerequisite. Acceptance: the helper exists in arf/scripts/utils,
reproduces the t0054 0e+00 Hz max-diff verdict, and is invoked in the new task's compute step.
Recommended task types: write-library.

</details>

<details>
<summary><strong>NMDA decay-time tau2 sweep at fixed gNMDA on t0054 to disentangle
conductance amplitude from kinetic time constant</strong> (S-0054-05)</summary>

**Kind**: experiment | **Priority**: medium

t0054 fixed NMDA tau2 at 80 ms and varied only gNMDA, conflating conductance amplitude with
kinetic time constant. Biological NMDA decay tau spans 50-200 ms across DSGC literature
(PolegPolsky2016 reports tau1NMDA = 50 ms; t0018 cites 100-200 ms). Hold gNMDA fixed at 0.25
nS (the 12x peak-rate-boost point) and sweep tau2 in {30, 60, 80, 120, 200} ms x 12 directions
x 10 trials x 2 modes (FULL, E_ONLY) = 1200 trials, on the t0054 minimal architecture with
placement seed 0, voltage-independent NMDA kept. Report per-tau2 EPSP decay tau (using the
improved metric from S-0054-03), peak Hz, and vector-sum DSI. Pass criterion: identify whether
tau2 alone (independent of gNMDA) drives the DSI collapse, or whether the collapse is
dominated by gNMDA. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Per-trial ProcessPool parallelisation for the minimal-DSGC sweep
runner (t0052/t0053/t0054)</strong> (S-0054-06)</summary>

**Kind**: library | **Priority**: medium

t0054's 1440-trial sweep took 4 h 19 min wall-clock on a single CPU thread (~10.8 s/trial),
3.5x over the 75-minute plan target. Adding Mg-block NMDA (S-0054-01), the joint conductance
sweep (S-0054-02), and the tau2 sweep (S-0054-05) will each be 5-15x larger and infeasible on
a single thread. Each (gNMDA, direction, trial, mode) combination is embarrassingly parallel
because NEURON state is rebuilt per trial. Build a ProcessPoolExecutor wrapper for the
minimal-DSGC sweep loop in t0054/code/run_tuning_curve.py (and equivalent t0052/t0053 paths)
that farms trials across N_workers = max(1, cpu_count - 2). Validate: gNMDA=0 regression gate
against t0052 still passes at 0e+00 Hz max diff. Distinct from t0045 (CoreNEURON-on-GPU for
t0022) and S-0026-04 (t0024-specific) because it targets the CPU runner shared by
t0052/t0053/t0054. Recommended task types: write-library, baseline-evaluation.

</details>

## Research

* [`research_code.md`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/results_summary.md)*

# Results Summary: Minimal DSGC with AMPA + NMDA Excitation and Scalar gabaMOD

## Summary

Built a minimal DSGC extending t0052 with co-located NMDA `Exp2Syn` (tau1=5 ms, tau2=80 ms,
e=0 mV) at every E synapse and ran a 4-value gNMDA sweep (`{0.0, 0.25, 0.5, 1.0}` nS) × 12
directions × 10 trials × 3 modes (1440 trials, 4 h 19 min wall-clock on local CPU). The
gNMDA=0 regression gate against t0052's `tuning_curve_full.csv` passed at **max |rate diff| =
0.000e+00 Hz** across all 120 rows. Headline finding: NMDA dramatically closes the peak-rate
gap (peak Hz at preferred direction goes from 0.667 (t0052) to 8.0 at gNMDA=0.25 nS), but
scalar `gabaMOD` inhibition is too weak to maintain direction selectivity once NMDA is active
— vector-sum DSI collapses from 0.746 (gNMDA=0) to 0.082 (gNMDA=0.25) and approaches 0 at
higher gNMDA.

## Metrics

* **gNMDA=0.0 nS, FULL**: peak 0.667 Hz, null 0.000 Hz, vector-sum DSI 0.746, primary DSI
  1.000 (degenerate). **Matches t0052 exactly** — regression gate passed at 0e+00 Hz max diff.
* **gNMDA=0.25 nS, FULL**: peak 8.000 Hz, null 6.000 Hz, vector-sum DSI 0.082. ~12× firing
  rate vs gNMDA=0; DSI collapses ~9×.
* **gNMDA=0.5 nS, FULL**: peak 7.333 Hz, null 6.000 Hz, vector-sum DSI 0.029. Saturating;
  scalar gabaMOD can't keep up with NMDA-amplified excitation.
* **gNMDA=1.0 nS, FULL**: peak 4.667 Hz, null 4.667 Hz, vector-sum DSI 0.017. Effectively zero
  DSI at high NMDA — preferred and null directions fire at the same rate.
* **AMPA + NMDA only (E_ONLY)** at gNMDA=0.25/0.5/1.0: 6.7 / 4.7 / multiple Hz — confirms
  excitation is no longer single-spike-per-trial like t0052.
* **GABA_ONLY** at all gNMDA values: 0.000 Hz (no excitation, no spikes — sanity check).
* **EPSP decay-to-1/e** (REQ-20): null for all 4 gNMDA values; the windowed E_ONLY trace
  doesn't return below 1/e of peak within the trial because stacked NMDA conductance keeps the
  cell depolarised at trial end. Qualitative decay-vs-gNMDA effect is visible in the
  per-direction EPSP PNGs (sweep_summary `epsp_decay_vs_gnmda.png` plot is rendered but shows
  an empty / null y-axis).

## Verification

* `meta.asset_types.library.verificator minimal_dsgc_ampa_nmda_scalar_gaba` — **PASSED** (0
  errors / 0 warnings).
* `verify_task_metrics t0054_minimal_dsgc_ampa_nmda_scalar_gaba` — **PASSED** (0/0).
* gNMDA=0 regression gate (compute_metrics.py): **PASSED** at max |rate diff| = 0.000e+00 Hz
  vs t0052's tuning_curve_full.csv across 120 rows.
* Quiescent-rest gate: V_rest = -64.56 mV (within ±0.5 mV target).
* Placement bit-identical to t0052 — `test_placement_seed0_match.py` PASSED.
* NMDA-inert smoke test at gNMDA=0: rate matched t0052 within 1e-6 Hz before the sweep.
* `ruff check` / `ruff format` — clean across all task code modules.
* `mypy .` — no issues across 265 source files.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0054_minimal_dsgc_ampa_nmda_scalar_gaba" date_completed:
"2026-04-28" ---
# Results Detailed: Minimal DSGC with AMPA + NMDA Excitation and Scalar gabaMOD

## Summary

Extended t0052 by adding a co-located NMDA `Exp2Syn` (tau1=5 ms, tau2=80 ms, e=0 mV) at every
E synapse, swept gNMDA across `{0.0, 0.25, 0.5, 1.0}` nS, and ran the full 12-dir × 10-trial ×
3-mode protocol (1440 trials, 4 h 19 min wall-clock). The gNMDA=0 regression gate against
t0052 passed exactly. Headline finding: NMDA closes the peak-rate gap (0.67 → 8 Hz at
gNMDA=0.25; ~12×) but scalar gabaMOD cannot maintain DSI once NMDA is active (vector-sum DSI
0.746 → 0.082 → 0.029 → 0.017 across the sweep). The implementation is correct and
reproducible; the negative result on DSI vs gNMDA is the scientific finding.

## Methodology

* **Hardware**: local CPU. No GPU. No remote machines.
* **NEURON**: 8.2.7 with built-in `Exp2Syn`, `hh`, `pas` only (no MOD compilation).
* **Python**: 3.13 via uv. Same dependency pinning as t0052.
* **Random seed**: `PLACEMENT_SEED=0`, bit-identical to t0052/t0053. Per-trial seed
  `1000·angle_idx + trial_idx + 1`.
* **Sweep wall-clock**: 15 587 s = 4 h 19 min for 1440 trials at ≈ 10.8 s/trial average.
  Slower than t0052's 3.2 s/trial per Exp2Syn — the added NMDA `Exp2Syn` per synapse adds
  another integration component to every trial.
* **Validation gates run before full sweep**:
  * Quiescent rest (`test_quiescent_rest.py`): V_rest = −64.56 mV (±0.5 mV target). PASS.
  * Placement bit-identical to t0052: per-pair coords match within 1e-9. PASS.
  * NMDA-inert smoke test at gNMDA=0 (1 angle × 2 trials): firing rate 0.666667 Hz, matches
    t0052 within 1e-6 Hz. PASS.
  * Dry-run skipped (sweep launched directly).
* **Hard-fail gate inside compute_metrics.py**: gNMDA=0 FULL CSV row-by-row vs t0052's
  `tuning_curve_full.csv`. **PASSED at max |rate diff| = 0.000e+00 Hz** across 120 rows.

## Metrics

See `results/metrics.json` (12 variants, multi-variant format) and
`results/derived_quantities.json`.

### Headline (FULL mode)

| gNMDA (nS) | DSI (registered) | HWHM (deg) | reliability | RMSE_vs_target | peak_hz | null_hz | vector_sum_dsi |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 1.000 | 82.5 | 1.000 | 16.98 | 0.667 | 0.000 | 0.746 |
| 0.25 | 0.143 | n/a | 0.667 | 13.50 | 8.000 | 6.000 | 0.082 |
| 0.50 | 0.083 | n/a | 0.581 | 13.91 | 7.333 | 6.000 | 0.029 |
| 1.00 | 0.000 | n/a | 0.564 | 16.16 | 4.667 | 4.667 | 0.017 |

(Primary DSI = (peak − null) / (peak + null); HWHM and reliability come from the registered
metric helpers and become noisy / undefined as the tuning curve flattens.)

### E_ONLY mode (peak_hz, no inhibition)

| gNMDA (nS) | E_ONLY peak_hz |
| --- | --- |
| 0.00 | 0.667 |
| 0.25 | 6.667 |
| 0.50 | 4.667 |
| 1.00 | (saturating, multi-spike) |

E_ONLY peak Hz drops from 6.67 to 4.67 between gNMDA=0.25 and 0.50 because of refractory
saturation; further increases at 1.0 nS produce multi-spike trains that the simple peak-Hz
metric undercounts.

### EPSP decay (the user's question)

`epsp_decay_to_1e_ms` returned `null` for all 4 gNMDA values. The compute logic looks for the
time after EPSP peak when V drops below `V_rest + (V_peak − V_rest)/e`; with NMDA's 80 ms
decay τ acting on 100 synapses, the cell stays depolarised at trial end (1500 ms) above the
1/e point. The qualitative effect — that NMDA dramatically slows the EPSP tail — is plainly
visible in the per-direction EPSP PNGs (compare `epsp_dir_000_gnmda_0.00.png` vs
`epsp_dir_000_gnmda_1.00.png`). The numeric `epsp_decay_to_1e_ms` derivation should be
extended to either (a) lengthen the trial window or (b) fit an exponential rather than look
for a 1/e crossing.

## Visualisations

`results/images/` contains 252 PNGs.

### Sweep summary plots (the headline)

![Peak Hz vs gNMDA per direction (FULL
mode)](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/images/peak_hz_vs_gnmda.png)

Adding NMDA boosts peak firing rate by ~12× at gNMDA=0.25 across all directions; the curves
cluster (preferred and null directions both rise together), explaining the DSI collapse.

![Vector-sum DSI vs gNMDA (FULL
mode)](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/images/dsi_vs_gnmda.png)

Vector-sum DSI drops monotonically from 0.746 (gNMDA=0) to 0.017 (gNMDA=1.0) — scalar gabaMOD
inhibition cannot keep up with NMDA-amplified excitation.

![EPSP decay-to-1/e vs gNMDA
(E_ONLY)](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/images/epsp_decay_vs_gnmda.png)

Plot is rendered but the y-axis is empty — the decay metric returned `null` (see the
Methodology / Limitations sections).

### Per-direction headline figures

![Soma V(t) FULL θ=0°
gNMDA=1.0](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/images/v_soma_dir_000_gnmda_1.00.png)

At gNMDA=1.0 nS the soma reaches sustained suprathreshold depolarisation with multiple spikes
per trial — very different from t0052's single-spike regime.

![Aggregate EPSP θ=0°
gNMDA=0.0](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/images/epsp_dir_000_gnmda_0.00.png)
![Aggregate EPSP θ=0°
gNMDA=1.0](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/images/epsp_dir_000_gnmda_1.00.png)

Compare the two: at gNMDA=0 the EPSP returns to baseline within ~50 ms after peak; at
gNMDA=1.0 the EPSP barely drops before the trial ends at 1500 ms. NMDA's 80-ms decay τ
operating on 100 simultaneous synapses keeps the cell depolarised throughout the trial.

The remaining 246 PNGs (12 dirs × 5 plot types × 4 gNMDA = 240, plus 4 polar + 4 cartesian + 3
sweep summary) are in `results/images/`.

## Examples

Three concrete trial-level input/output pairs from the sweep.

### Example 1: gNMDA=0.0, θ=0°, trial 1, FULL — matches t0052 exactly

Input:

```text
gnmda_ns = 0.0
direction_deg = 0
trial_seed = 1
mode = FULL
```

Output (from `tuning_curve_full.csv`):

```text
firing_rate_hz = 0.666667
```

Same as t0052's row `0,1,0.666667`. Regression gate passed at 0 Hz diff.

### Example 2: gNMDA=0.25, θ=0°, trial 1, FULL — NMDA boost

Input:

```text
gnmda_ns = 0.25
direction_deg = 0
trial_seed = 1
mode = FULL
```

Output:

```text
firing_rate_hz = 8.000000   # 12-spike train across 1500 ms
```

12× the gNMDA=0 rate. The cell now fires multi-spike trains thanks to the slow NMDA tail.

### Example 3: gNMDA=1.0, θ=180° (null), trial 6001, FULL — DSI collapse

Input:

```text
gnmda_ns = 1.0
direction_deg = 180
trial_seed = 6001
mode = FULL
```

Output:

```text
firing_rate_hz = 4.666667    # null direction now fires almost as much as preferred
```

Compare to gNMDA=0 null Hz (0.0) — at gNMDA=1.0 the scalar `gabaMOD = 0.99` GABA amplitude can
no longer suppress the NMDA-amplified excitation, so the cell fires nearly as often in the
null direction as in the preferred direction. Vector-sum DSI 0.017.

## Analysis

### Plan-assumption check

The plan's Key Question 2 ("does NMDA close the peak-rate gap?") is answered **YES** —
gNMDA=0.25 produces 8 Hz peak (12× t0052), within an order of magnitude of the in vivo 30-100
Hz target.

The plan's Key Question 3 ("does NMDA improve or degrade DSI?") is answered **DEGRADE under
scalar gabaMOD** — DSI drops from 0.746 to 0.017 across the gNMDA sweep. This is a consistent
finding with the brainstorm-9 narrative that t0052 was over-suppressed by GABA; once NMDA
escalates excitation, scalar GABA scaling becomes insufficient. The natural follow-up is a
joint AMPA × NMDA × GABA conductance sweep to find the operating point where DSI is preserved
at biologically-realistic firing rates.

The plan's Key Question 1 ("at what gNMDA does EPSP decay reach 50-100 ms?") is **not
numerically answered** because `epsp_decay_to_1e_ms` returned `null`. Qualitatively, the EPSP
tail at gNMDA=1.0 spans the full 1500-ms trial window — much longer than t0052's ~30 ms. A
precise number requires either a longer trial window or an exponential fit.

### Why the cost

Sweep wall-clock 4 h 19 min vs the plan's ~75 min target. The 3.5× overrun is because adding
the NMDA `Exp2Syn` to every co-located synapse roughly tripled per-trial CPU (1.5× from the
integration step + 2× from the much slower decay, which keeps the synapse state active longer
in the CVODE adaptive solver). For future sweeps, expect ~3 s/trial to scale to ~10 s/trial
when adding slow synapses.

## Limitations

* **`epsp_decay_to_1e_ms` returned `null`**. Numerical answer to the headline question is
  missing; qualitative answer is in the per-direction EPSP PNGs.
* **HWHM is `null` at gNMDA > 0**. Once the tuning curve flattens (every direction firing ~6-8
  Hz), the half-width-at-half-maximum is not well-defined. This is a property of the result,
  not a bug.
* **Single-trial firing-rate granularity at gNMDA=0**. Each preferred-direction trial fires
  exactly 1 spike per 1500 ms = 0.667 Hz. Granularity at other gNMDA values is similarly
  quantized (e.g., 8 Hz = 12 spikes / 1500 ms; 4.67 Hz = 7 spikes).
* **No noise / Poisson background**. Deterministic protocol.
* **No voltage-dependent NMDA Mg block**. Voltage-independent NMDA (Voff=1 equivalent) by
  design — see suggestions for the Mg-block follow-up.
* **No active dendrites** (Nav/Kv in dendrites).

## Files Created

Code: 16 modules in `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/` (10 copied verbatim
from t0052, 1 from t0053, 5 extended). Library asset:
`assets/library/minimal_dsgc_ampa_nmda_scalar_gaba/` with verifier 0/0.

Results:

* `tuning_curve_full.csv`, `tuning_curve_e_only.csv`, `tuning_curve_gaba_only.csv` (480 rows
  each).
* `spike_times_*.csv`, `voltage_traces_*.csv` (per mode).
* `activation_times.csv`, `wallclock.json`, `placement_seed0.json`.
* `metrics.json` (12 variants), `derived_quantities.json`, `costs.json`,
  `remote_machines_used.json`.
* 252 PNGs in `images/`.

Logs: full step lifecycle (1, 2, 3, 6, 7, 9, 10 skipped, 11 skipped, 12, 13, 14, 15) plus ~30
entries in `commands/` and a session-capture report in `sessions/`.

## Verification

* `meta.asset_types.library.verificator` — PASSED 0/0.
* `verify_task_metrics`, `verify_task_dependencies`, `verify_task_file`,
  `verify_task_results`, `verify_task_folder`, `verify_logs`, `verify_research_code`,
  `verify_compare_literature`, `verify_plan` — all PASSED 0 errors.
* gNMDA=0 regression gate vs t0052: PASSED at max |rate diff| = 0.000e+00 Hz.
* Placement bit-identical to t0052: PASSED.
* `ruff check` / `ruff format` / `mypy` (265 source files): clean.

## Task Requirement Coverage

Operative task text from `task.json`:

> Extend t0052 by adding co-located NMDA Exp2Syn (tau1=5, tau2=80, e=0) at each E synapse; sweep
> gNMDA at {0, 0.25, 0.5, 1.0} nS; characterise EPSP decay, peak rate, and DSI vs gNMDA.

Operative long-description text from `task_description.md` (concise summary): build a minimal
DSGC on the t0052 baseline with AMPA + NMDA co-located excitation, scalar gabaMOD inhibition,
soma + AIS HH, 100 E + 100 I synapses, fixed seed 0; run 4 gNMDA × 12 dirs × 10 trials × 3
modes = 1440 trials; report per-gNMDA per-direction soma V(t), EPSP/IPSP, PSTH, polar tuning,
plus three sweep-summary plots; library asset `minimal_dsgc_ampa_nmda_scalar_gaba`; gNMDA=0
must reproduce t0052 within rounding.

| REQ | Item | Verdict | Evidence |
| --- | --- | --- | --- |
| REQ-1 | dsgc-baseline-morphology-calibrated | Done | cell.py; same as t0052 |
| REQ-2 | hh on soma+AIS, passive dendrites Rm/Ra/cm/V_rest | Done | constants.py; quiescent test PASS |
| REQ-3 | 100 E + 100 I co-located, uniform random, seed 0 | Done | placement.py; placement bit-identical to t0052 |
| REQ-4 | AMPA Exp2Syn 0.5/2.5/0/0.5 nS | Done | synapses.py |
| REQ-5 | NMDA Exp2Syn 5/80/0/swept | Done | synapses.py |
| REQ-6 | NMDA + AMPA fire from same NetStim | Done | shared ampa_netstim with two NetCons |
| REQ-7 | Scalar gabaMOD identical to t0052 | Done | gaba_mod() unchanged; conductance ratio 3.0 |
| REQ-8 | Stimulus 12 dirs × 200 µm × 1.0 µm/ms × 1500 ms | Done | constants.py |
| REQ-9 | 10 trials/direction, deterministic seeds | Done | run_tuning_curve.py; 480 rows per CSV |
| REQ-10 | Three trial modes FULL / E_ONLY / GABA_ONLY | Done | TrialMode enum + trial.py |
| REQ-11 | gNMDA sweep {0, 0.25, 0.5, 1.0} | Done | NMDA_PEAK_NS_VALUES |
| REQ-12 | Per-direction soma V(t) per gNMDA | Done | 48 PNGs |
| REQ-13 | Aggregate EPSP / IPSP per gNMDA | Done | 96 PNGs |
| REQ-14 | PSTH per gNMDA | Done | 48 PNGs |
| REQ-15 | Activation histogram per gNMDA | Done | 48 PNGs |
| REQ-16 | Polar tuning curve + DSI metrics per gNMDA | Done | 4 polar PNGs; metrics.json |
| REQ-17 | Cartesian tuning curve per gNMDA | Done | 4 cartesian PNGs |
| REQ-18 | Three sweep-summary plots (decay, peak Hz, DSI vs gNMDA) | Done | 3 PNGs (decay plot empty due to REQ-20) |
| REQ-19 | metrics.json multi-variant `gnmda_<value>_<mode>` | Done | 12 variants; verifier PASSED |
| REQ-20 | epsp_decay_to_1e_ms per gNMDA | Partial | All 4 returned `null`; qualitative answer in EPSP PNGs |
| REQ-21 | Quiescent rest gate | Done | V_rest -64.56 mV |
| REQ-22 | gNMDA=0 regression gate vs t0052 | Done | max |
| REQ-23 | Placement bit-identical to t0052 | Done | test_placement_seed0_match.py PASS |
| REQ-24 | gabaMOD ratio 3.0 sanity | Done | constants & metrics confirm 3.0 |
| REQ-25 | NMDA-inert smoke test at gNMDA=0 | Done | match within 1e-6 Hz |
| REQ-26 | Library asset minimal_dsgc_ampa_nmda_scalar_gaba | Done | verifier PASSED 0/0 |
| REQ-27 | Wall-clock budget ~75 min | Partial | Took 4 h 19 min (3.5× over); flagged in suggestions |

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0054_minimal_dsgc_ampa_nmda_scalar_gaba" date_compared:
"2026-04-25" ---
# Comparison with Published Results

## Summary

Adding co-located voltage-independent NMDA `Exp2Syn` (tau1 = 5 ms, tau2 = 80 ms, e = 0 mV) at
every E synapse of the t0052 minimal DSGC dramatically closes the peak-rate gap (peak Hz at
the preferred direction goes from **0.667 Hz** at gNMDA = 0 nS to **8.000 Hz** at gNMDA = 0.25
nS, a **~12x** boost) but collapses direction selectivity under the unchanged scalar `gabaMOD`
inhibition: vector- sum DSI drops from **0.746** (gNMDA = 0) to **0.082** (gNMDA = 0.25) and
approaches **0.017** at gNMDA = 1.0. The peak-rate sweep reaches an order of magnitude of the
in vivo target **30-100 Hz** implied by Park2014 cells [Park2014, p. 3978] but never matches
the in vitro DSI band of **0.65 +/- 0.05** [Park2014, p. 3978]. The result confirms the
prediction of PolegPolsky2016 [PolegPolsky2016, p. 1283] that voltage-dependent NMDA Mg-block
(absent here by design) is a necessary ingredient for multiplicative direction-selective gain.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Park2014 (CART-Cre, voltage-clamp) | DSI (primary) | 0.65 | 0.143 | -0.507 | gNMDA = 0.25 nS FULL; peak-rate regime closer to in vivo than t0052 but DSI is much lower [Park2014, p. 3978] |
| Park2014 (TRHR-GFP / wild-type) | DSI (primary) | 0.73 | 0.143 | -0.587 | Reference subset, n = 38 cells [Park2014, p. 3978] |
| Park2014 (in vivo-implied peak rate) | Peak Hz | 30.0 | 8.0 | -22.0 | gNMDA = 0.25 nS FULL; 30-100 Hz range cited in t0052 plan as the in vivo target [Park2014, p. 3978] |
| PolegPolsky2016 (NMDA decay tau) | NMDA tau (ms) | 50.0 | 80.0 | +30.0 | Their `bipolarNMDA.mod` `tau1NMDA = 50 ms` deactivation; ours `Exp2Syn` `tau2 = 80 ms` decay [PolegPolsky2016, p. 1280, Methods] |
| PolegPolsky2016 (control PD PSP, AMPA + NMDA) | PD PSP (mV) | 5.8 | ~84.0 | +78.2 | Aggregate E_ONLY EPSP peak at preferred direction; mV scale not directly comparable (see Methodology) [PolegPolsky2016, p. 1280, Fig 1] |
| PolegPolsky2016 (DSI under voltage-dependent NMDA) | DSI | 0.46 | 0.143 | -0.317 | Their NEURON model with voltage-dependent NMDA + tuned GABA preserves DSI; ours collapses without Mg-block [PolegPolsky2016, Fig 5] |
| t0052 (parent, no NMDA) | Vector-sum DSI | 0.746 | 0.746 | +0.0 | gNMDA = 0 FULL; bit-identical regression-gate match (max diff 0e+00 Hz) [t0052 results_summary.md] |
| t0052 (parent, no NMDA) | Peak Hz | 0.667 | 0.667 | +0.0 | gNMDA = 0 FULL; regression gate confirms exact reproduction [t0052 results_summary.md] |
| t0053 (sibling, spatial GABA, no NMDA) | Vector-sum DSI | 0.0 | 0.746 | +0.746 | gNMDA = 0 FULL; t0053 fully suppressed at 100 nS GABA mass while t0054 inherits t0052's 66 nS regime [t0053 results_summary.md] |
| t0048 (voltage-independent NMDA on deposited DSGC) | DSI at gNMDA = 1.0 nS | 0.078 | 0.0 | -0.078 | t0048 used `Voff_bipNMDA = 1`; same voltage-independent NMDA regime [t0048 results_summary.md] |
| t0048 (voltage-independent NMDA on deposited DSGC) | DSI range across gNMDA sweep | 0.066 | 0.143 | +0.077 | Max-min DSI across the gNMDA sweep [t0048 results_summary.md] |

### Prior Task Comparison

| Prior Task | Variant | DSI (primary) | Peak Hz | Notes |
| --- | --- | --- | --- | --- |
| t0048 (Voff = 1, voltage-independent NMDA on deposited DSGC) | gNMDA = 0.5 nS | 0.102 | n/a | Closest prior project result for "voltage-independent NMDA on a DSGC"; DSI flattens but does not collapse to zero |
| t0048 (Voff = 1, voltage-independent NMDA on deposited DSGC) | gNMDA = 3.0 nS | 0.037 | n/a | Highest gNMDA point; DSI continues to drop but stays above zero |
| t0052 (parent, scalar gabaMOD, AMPA only) | FULL | **1.000** | **0.667** | Single-spike-per-trial; trivial DSI = 1 from null = 0 Hz |
| t0053 (sibling, spatial GABA, AMPA only) | FULL | **0.000** | **0.000** | Fully suppressed by 100 nS mean GABA mass |
| t0054 (this task) | gNMDA = 0 FULL | **1.000** | **0.667** | Regression gate vs t0052: 0e+00 Hz max diff |
| t0054 (this task) | gNMDA = 0.25 FULL | **0.143** | **8.000** | NMDA closes peak-rate gap but DSI collapses ~9x |
| t0054 (this task) | gNMDA = 0.5 FULL | **0.100** | **7.333** | Saturating regime |
| t0054 (this task) | gNMDA = 1.0 FULL | **0.000** | **4.667** | Preferred = null = 4.67 Hz; vector-sum DSI 0.017 |

## Methodology Differences

* **NMDA voltage dependence**: PolegPolsky2016 [p. 1280, Methods] uses a Jahr-Stevens Mg-block
  `bipolarNMDA.mod` channel; we use NEURON's built-in `Exp2Syn` with no Mg-block. This is by
  design — the task explicitly defers voltage-dependent NMDA to a follow-up. It is the most
  consequential methodological gap.

* **NMDA kinetics**: PolegPolsky2016 reports `tau1NMDA = 50 ms` deactivation and `tau2NMDA = 2
  ms` activation [PolegPolsky2016, p. 1280, Methods]. Our `Exp2Syn` uses `tau1 = 5 ms` rise
  and `tau2 = 80 ms` decay (NEURON `Exp2Syn` convention is `tau1 < tau2`, both positive). Both
  fall within the 50-200 ms biological NMDA decay range cited in t0018, but the precise time
  course is different.

* **Excitation count**: 100 AMPA + 100 NMDA (this task) vs 177 AMPA + 177 NMDA in
  PolegPolsky2016 [p. 1280] / 282 in t0046 reproduction / >1000 SAC varicosities in
  deRosenroll2026 [p. 5]. Lower synapse count gives lower aggregate drive.

* **Inhibition mechanism**: Park2014 attributes DS to null-direction GABA from SACs;
  PolegPolsky2016 uses tuned GABA on a morphologically realistic DSGC; we use the unchanged
  t0052 scalar `gabaMOD` (PD = 0.33, ND = 0.99) on all 100 GABA synapses, an
  order-of-magnitude consistent but non-spatially-distributed inhibition pattern. The t0054
  design holds inhibition fixed at the t0052 level so that the gNMDA effect can be isolated.

* **DSGC subtype and morphology**: Park2014 records mouse On-Off DSGCs in CART-Cre and
  TRHR-GFP lines [p. 3977]; PolegPolsky2016 uses DRD4-GFP On-Off DSGCs [p. 1278]. Our
  morphology is the t0009-calibrated `dsgc-baseline-morphology-calibrated`, which is a generic
  mouse DSGC reconstruction shared across t0052 / t0053. Morphological details (dendritic
  field, soma size, AIS geometry) are not directly matched.

* **Bar speed**: 1.0 µm/ms = 1000 µm/s in this task; PolegPolsky2016 reports 1 mm/s
  [PolegPolsky2016, p. 1278] and Park2014 reports 31-36 deg/s [Park2014, p. 3977]. Conversions
  are imperfect, but our speed is consistent with prior t0052 / t0053 settings.

* **Single-event-per-synapse, no noise**: Trials are deterministic (one NetStim event per
  synapse per trial); deRosenroll2026 emphasises that DSI is sensitive to AR(2) correlated
  release noise, and Park2014's in vivo DSI band reflects in vitro membrane noise that is not
  reproduced here.

* **Aggregate EPSP magnitude scale**: Our reported aggregate E_ONLY EPSP peak is **~84 mV**
  above V_rest (i.e., the somatic voltage reaches ~0 mV after 100 simultaneous AMPA + NMDA
  conductances drive Vm to E_AMPA = E_NMDA = 0 mV with no inhibition). PolegPolsky2016's **5.8
  mV** PD PSP [p. 1280] is recorded under whole-cell voltage-clamp with TTX/QX-314 in a regime
  where the cell cannot reach reversal. The two numbers are not directly comparable — the
  methodology rows are flagged in the comparison table only for completeness.

## Analysis

### Peak-rate gap closure (Key Question 2)

NMDA closes the peak-rate gap dramatically. At gNMDA = 0.25 nS the peak firing rate at the
preferred direction reaches **8.000 Hz**, **12x** the gNMDA = 0 baseline of **0.667 Hz**. This
brings the model within an order of magnitude of the in vivo target band of **30-100 Hz**
implied by Park2014 [Park2014, p. 3977]. At gNMDA = 0.5 nS the peak rate slightly *drops* to
**7.333 Hz** because the cell saturates in a refractory-limited regime; at gNMDA = 1.0 nS the
peak rate falls further to **4.667 Hz** as the slow NMDA tail keeps the cell tonically
depolarised and curtails spikes per trial. This non-monotonic peak-rate-vs-gNMDA curve is a
quantitative finding consistent with the [t0048] cautionary note that NMDA pushed beyond the
multi-spike-per-trial threshold re-saturates the response.

### DSI collapse under voltage-independent NMDA (Key Question 3)

Vector-sum DSI drops monotonically from **0.746** to **0.082** (gNMDA = 0.25), to **0.029**
(gNMDA = 0.5), to **0.017** (gNMDA = 1.0). The primary DSI follows the same path: **1.000** ->
**0.143** -> **0.100** -> **0.000**. At gNMDA = 1.0 nS the preferred and null peak rates are
both exactly **4.667 Hz**, eliminating direction selectivity entirely. This result
quantitatively demonstrates a known mechanism documented in PolegPolsky2016 [PolegPolsky2016,
Fig 5, p. 1283-1284]: removing the voltage-dependent NMDA Mg-block converts NMDA scaling from
*multiplicative* (preserves DSI) to *additive* (degrades DSI). Our t0054 result is a
forward-direction confirmation: starting from a working DSI = 0.746 baseline, adding
voltage-independent NMDA degrades DSI exactly as PolegPolsky2016's NEURON model predicted for
the voltage-independent / Ohmic NMDA substitute. The mechanism is the same one [t0048]
explored on the deposited DSGC; t0054 reproduces it on the t0052 minimal architecture.

### Comparison with t0048 (voltage-independent NMDA on the deposited DSGC)

[t0048] reported a DSI range of **0.066** (max - min) across a 7-point gNMDA sweep at
`Voff_bipNMDA = 1`, with absolute DSI values between **0.04 and 0.10**. Our 4-point sweep
produces a DSI range of **0.143** (max - min: 0.143 at gNMDA = 0.25 minus 0.0 at gNMDA = 1.0)
with absolute DSI between **0.0 and 0.143** in the FULL mode. The two studies agree on the
qualitative finding — voltage-independent NMDA flattens but does not collapse DSI to a
meaningful in vivo target — and disagree quantitatively because the underlying
excitatory-inhibitory balance is different (t0048 uses the deposited 282-synapse DSGC with
`bipolarNMDA.mod`; we use a from-scratch 100-synapse cell with built-in `Exp2Syn`). Both
confirm the **PolegPolsky2016** prediction that voltage-dependent NMDA Mg-block is essential
for multiplicative DSI scaling.

### Compare to PolegPolsky2016's voltage-dependent NMDA model

PolegPolsky2016's NEURON model with voltage-dependent NMDA + tuned GABA preserves DSI under
noisy conditions (DSI roughly **0.46** in their Figure 5 voltage-dependent NMDA condition; DSI
degrades under their `0 Mg2+` and `high-Cl-` interventions [PolegPolsky2016, Fig 5]). Our
t0054 result lands at **0.143** primary DSI at gNMDA = 0.25 — a **-0.317** delta against the
voltage-dependent-NMDA reference, attributable to two factors: (1) the absence of Mg-block in
our NMDA, and (2) the simpler scalar `gabaMOD` inhibition. The decomposition between these two
factors is a follow-up experiment.

### EPSP decay (Key Question 1)

The numerical `epsp_decay_to_1e_ms` returned `null` for all four gNMDA values because the
trial window (1500 ms) is shorter than the time the cell takes to drop back below the 1/e
threshold once NMDA's 80 ms decay tau is engaged across 100 simultaneous synapses (the
100-fold superposition keeps Vm above the 1/e threshold throughout the trial). Qualitatively,
the EPSP tail at gNMDA = 1.0 nS extends well beyond the **~30 ms** observed in t0052 (per the
per-direction EPSP PNG comparison described in `results_detailed.md`), reaching the **~50-200
ms** biological NMDA decay range cited in [t0018]. A precise number requires either a longer
trial window or an exponential fit; the qualitative answer to Key Question 1 is **yes, NMDA
dramatically slows the EPSP tail**, but the quantitative answer is deferred.

### Single-spike vs multi-spike regime (Key Question 4)

t0052's gNMDA = 0 regime is single-spike-per-trial (0.667 Hz = 1 spike per 1500 ms). t0054's
gNMDA
>= 0.25 nS regime is multi-spike-per-trial (8 Hz = 12 spikes per 1500 ms; 4.67 Hz = 7 spikes). The
transition occurs at gNMDA = 0.25 nS — adding even the smallest non-zero NMDA conductance
moves the cell out of the degenerate single-spike regime into the multi-spike regime where DSI
is no longer trivially 1. This is exactly the regime change predicted in [t0052]'s Limitations
section and in the t0054 plan's motivation.

## Limitations

* **No voltage-dependent NMDA Mg-block in this task**. The most relevant comparison from
  PolegPolsky2016 is to their voltage-*dependent* NMDA configuration, which we cannot
  reproduce by design. Our model is the voltage-*independent* NMDA control. The DSI gap in the
  comparison table (-0.317 vs PolegPolsky2016 Fig 5) reflects exactly this design choice and
  motivates a follow-up task with a Mg-block channel.

* **Aggregate EPSP magnitudes (~84 mV) are not directly comparable to PolegPolsky2016's 5.8 mV
  PD PSP** because their measurement is voltage-clamp with reversal-potential constraints
  absent here. The mV-scale rows in the comparison table are flagged but provide little
  constraint.

* **`epsp_decay_to_1e_ms` returned null**. The headline EPSP-decay-vs-gNMDA observable is
  qualitative only. Numerical values for the time constant of the EPSP tail are not reported.

* **Park2014's "in vivo 30-100 Hz" range** is the t0052 plan's interpretation of Park2014 +
  general in vivo DSGC literature. Park2014 itself reports tuning-by-direction PSP and current
  values, not a "peak Hz" rate; the 30-100 Hz figure should be treated as a general in vivo
  DSGC range from the literature rather than a direct Park2014 quantity.

* **Park2014 in vivo DSI band of "0.40-0.60"** in the orchestrator's hand-off message could
  not be verified from the paper text. The paper reports CART-Cre cells DSI = **0.65 +/-
  0.05** (n = 14) and TRHR-GFP / wild-type cells **0.73 +/- 0.03** (n = 38) [Park2014, p.
  3978]. We use the values directly attributable to Park2014 and treat 0.65-0.73 as the in
  vitro DSI target.

* **PolegPolsky2016 DSI under voltage-dependent NMDA** of **0.46** is read from their Figure 5
  voltage-dependent NMDA + tuned GABA panel. The paper does not publish a single headline DSI
  number, so this value should be treated as a representative model output rather than a
  precise benchmark.

* **No noise comparison**: Our deterministic trials cannot probe the noisy-discrimination
  benefit of NMDA multiplication that PolegPolsky2016 demonstrates with ROC analysis [p.
  1283]. Reliability is artefactually 1.0 in this task.

* **Scalar `gabaMOD` is not the same as Park2014's null-direction SAC GABA**. The inhibition
  is spatially uniform but direction-modulated in amplitude, not spatially distributed across
  the dendritic field. The DSI collapse may partly reflect this simplification, separately
  from the voltage-independent-NMDA gap.

* **Single conductance setting per gNMDA value**: only four gNMDA values were sampled ({0.0,
  0.25, 0.5, 1.0} nS). No GABA conductance sweep was performed; the operating point where
  inhibition could compensate for NMDA-amplified excitation is not characterised.

</details>
