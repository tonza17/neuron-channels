# ⏳ Tasks: In Progress

1 tasks. ⏳ **1 in_progress**.

[Back to all tasks](../README.md)

---

## ⏳ In Progress

<details>
<summary>⏳ 0055 — <strong>Add Mg-block NMDA to recover DSI in t0054 minimal
architecture</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0055_nmda_mg_block_dsi_recovery` |
| **Status** | in_progress |
| **Effective date** | 2026-04-28 |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0054-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Start time** | 2026-04-28T10:48:52Z |
| **Task page** | [Add Mg-block NMDA to recover DSI in t0054 minimal architecture](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Task folder** | [`t0055_nmda_mg_block_dsi_recovery/`](../../../tasks/t0055_nmda_mg_block_dsi_recovery/) |

# Add Voltage-Dependent NMDA Mg Block to Recover DSI in the t0054 Minimal Architecture

## Source

Suggestion S-0054-01 (high priority): "Add voltage-dependent NMDA Mg block to recover DSI in
the t0054 minimal AMPA + NMDA + scalar gabaMOD architecture."

## Motivation

t0054 demonstrated that adding a voltage-independent NMDA Exp2Syn (`tau1 = 5 ms`, `tau2 = 80
ms`, `e = 0 mV`) at every AMPA location collapses vector-sum DSI from **0.746** at `gNMDA = 0`
to **0.082** at `gNMDA = 0.25 nS` and to **0.017** at `gNMDA = 1.0 nS`. Peak rate also
degrades because the long-tail NMDA depolarisation removes the directional gating that the
scalar gabaMOD relies on (PD `gaba_mod = 0.33`, ND `gaba_mod = 0.99`). The DSI collapse is
expected from PolegPolsky 2016 (Fig 5) — without a voltage-dependent Mg block, NMDA
conductance fires regardless of postsynaptic voltage and washes out the inhibition-driven
directional asymmetry. Mg block restores multiplicative gain by suppressing NMDA conductance
at hyperpolarised voltages and unblocking it once the cell is already depolarised by AMPA.

This task replaces the t0054 voltage-independent NMDA Exp2Syn with a Jahr-Stevens Mg-block
point process at every E synapse, keeps every other parameter identical, and re-runs the same
gNMDA sweep. The headline question is: does Mg block recover the DSI that t0054 lost?

## Model Specification

Identical to t0054 unless explicitly noted. The change is **only** the NMDA point process;
AMPA, GABA, morphology, HH soma+AIS, placement seed, and stimulus protocol are bit-identical
to t0054.

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (same as t0054).
* 100 dendritic locations sampled with seed = 0 (bit-identical placement to t0054 — enforced
  by a placement-match test against
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/placement_seed0.json`).

### Sections and channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` with the same boosted AIS
  parameters as t0054 (`AIS_LENGTH_UM=30`, `AIS_DIAMETER_UM=2`, `AIS_GNABAR=1.2`,
  `AIS_GKBAR=0.04`, `AIS_GL=0.008`, `AIS_EL_HH=-65`).
* All dendritic sections passive: `Rm = 5999 Ω·cm²`, `Ra = 100 Ω·cm`, `cm = 1 µF/cm²`, `V_rest
  = -65 mV`.

### Synapses

* 100 E + 100 I co-located pairs (identical to t0054).

* **AMPA**: `Exp2Syn` with `tau1 = 0.5 ms`, `tau2 = 2.5 ms`, `e = 0 mV`, peak `0.5 nS`. Driven
  by the same `NetStim` event as the NMDA point process (one event per synapse per trial).

* **NMDA (CHANGED)**: a custom `NMDA_MgBlock` point process replacing the t0054 `Exp2Syn`.
  Same dual-exponential gating kinetics (`tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`) but
  multiplied by the Jahr-Stevens Mg-block factor:

  ```text
  g_NMDA(v, t) = gNMDA_max * s(t) * 1 / (1 + n * exp(-gamma * v))
  ```

  with `n = 0.25 / mM`, `gamma = 0.08 / mV` (the values used in `bipolarNMDA.mod` in t0046's
  ModelDB 189347 reproduction). `s(t)` is the standard Exp2Syn dual-exponential gating
  variable driven by `NetCon` events. `[Mg2+]` is folded into the `n` constant. A `Voff`
  parameter (default `0`) preserves the option to compare against the voltage-independent
  regime.

* **Inhibition**: scalar gabaMOD identical to t0054. `theta_PD = 0`, `theta_ND = 180`, peak `2
  nS × gaba_mod(theta)` where `gaba_mod(0) = 0.33` and `gaba_mod(180) = 0.99`.

### Stimulus protocol

* 12 directions × 10 trials × 3 trial modes × 4 `gNMDA` values = **1440 trials total** (same
  as t0054).
* Bar 200 µm × full arena, 1.0 µm/ms (= 1000 µm/s), 1500 ms per trial.
* `BASE_OFFSET_MS = 100` (bar enters arena at t = 100 ms).

### gNMDA sweep

Four values: `{0.0, 0.25, 0.5, 1.0}` nS — identical to t0054 to enable direct DSI deltas.

* `gNMDA = 0` reproduces t0052 / t0054 within rounding (validation gate).
* `gNMDA = 0.25` is the failure point in t0054 (DSI 0.082); the pass criterion targets this
  point.
* `gNMDA = 0.5` matches the Poleg-Polsky 2016 baseline.
* `gNMDA = 1.0` is twice the Poleg-Polsky baseline; a coarse high-end probe.

### Trial modes

* `FULL` — AMPA + NMDA + GABA active.
* `E_ONLY` — AMPA + NMDA active, GABA `NetCon` weights zeroed.
* `GABA_ONLY` — AMPA + NMDA `NetCon` weights zeroed, GABA active.

## Pass / Fail Criterion

The headline gate from S-0054-01:

* **Vector-sum DSI at `gNMDA = 0.25 nS` must exceed 0.50** (vs t0054 result 0.082).
* **Peak Hz at `gNMDA = 0.25 nS` (preferred direction, FULL) must reach >= 5 Hz**.

Reporting must explicitly state PASS or FAIL against this criterion in the headline summary.

## Outputs

### Per `gNMDA` value × per direction (4 × 12 = 48 panels per output type)

* Soma `V(t)` (FULL mode), mean ± SD across 10 trials.
* Aggregate EPSP (`E_ONLY`), mean ± SD.
* Aggregate IPSP (`GABA_ONLY`), mean ± SD.
* PSTH (5 ms bins, FULL mode).
* Per-synapse activation-time histogram.

### Sweep summary (the headline plots)

1. **Vector-sum DSI vs gNMDA** with t0054 (no-Mg) curve overlaid as a baseline — directly
   visualises the recovery (or lack thereof). X-axis: `gNMDA` (4 points). Y-axis: DSI. Two
   curves: this task vs t0054.
2. **Peak Hz vs gNMDA** with t0054 overlaid.
3. **EPSP decay-time-constant vs gNMDA** with t0054 overlaid (note: t0054 reports null for
   this metric due to the 1500 ms window; this task may inherit the same limitation).
4. **NMDA Mg-block g(v) curve** at the synapse — sanity plot showing the Boltzmann factor at
   `v ∈ [-80, +20] mV`.

### `metrics.json` (multi-variant format)

One variant per `(gNMDA, mode)` combination = 12 variants. Each variant carries the registered
keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`. Variant `id` schema: `gnmda_<value>_<mode>` (e.g., `gnmda_0.50_full`).

### `derived_quantities.json`

Per-variant: `peak_hz`, `null_hz`, `vector_sum_dsi`, `preferred_direction_deg`,
`active_fraction`. Per-`gNMDA`: `epsp_decay_to_1e_ms` for the `E_ONLY` variant at the
preferred direction. Plus `pass_criterion_dsi_at_gnmda_025`,
`pass_criterion_peak_hz_at_gnmda_025`, `pass_criterion_overall` (boolean).

## Library Asset

`minimal_dsgc_mg_block_nmda` under `tasks/t0055_nmda_mg_block_dsi_recovery/assets/library/`.
Includes:

* The new `NMDA_MgBlock.mod` MOD file.
* The full Python codebase (forked from t0054 with NMDA-only changes).
* A README documenting the Mg-block formula, parameter choices, and provenance (derived from
  bipolarNMDA.mod in t0046 / ModelDB 189347).

## Code Design

### Modules to copy verbatim from t0054 (with import-path rewrite to `tasks.t0055_*` and bootstrap sentinel renamed to `_T0055_NEURONHOME_BOOTSTRAPPED`)

`paths.py`, `swc_io.py`, `cell.py`, `placement.py`, `neuron_bootstrap.py`, `trial.py`,
`metrics_extra.py`, `test_quiescent_rest.py`, `test_gaba_mod.py`, `__init__.py`,
`run_tuning_curve.py`, `compute_metrics.py`, `render_figures.py`. (13 files.)

### New files

* **`code/mod/NMDA_MgBlock.mod`** — the new NMDA point process with Mg-block. Provenance noted
  in the file header (derived from bipolarNMDA.mod, ModelDB 189347).

### Modules to extend

* **`constants.py`** — copy from t0054, then rename references such that NMDA point process is
  `NMDA_MgBlock` rather than `Exp2Syn`. Add `MG_BLOCK_N = 0.25` (per-mM coefficient),
  `MG_BLOCK_GAMMA = 0.08` (per-mV coefficient), `MG_BLOCK_VOFF = 0` (0 = voltage-dependent).
* **`synapses.py`** — replace `h.Exp2Syn` for NMDA with `h.NMDA_MgBlock`. Set `tau1`, `tau2`,
  `e`, `n`, `gamma`, `Voff` from constants. The `NetCon.weight[0] = gnmda_ns * 1e-3` mechanism
  is unchanged. Keep AMPA `Exp2Syn` exactly as in t0054.
* **`neuron_bootstrap.py`** — extend the `nrnivmodl` step to compile `mod/NMDA_MgBlock.mod`
  alongside the existing MODs (this task is the first to introduce a custom MOD into the
  minimal architecture).

### Validation gates (run before the full sweep)

* **Quiescent rest test**: `V_rest = -65 ± 0.5 mV` with no synapses (same as t0054).
* **`gNMDA = 0` cross-task regression gate**: `tuning_curve_full` rows at `gNMDA = 0` must
  match t0054's `tuning_curve_full.csv` row-by-row at `gNMDA = 0` within 1e-6 Hz tolerance.
  With `gNMDA = 0` the Mg-block factor evaluates to a finite number but multiplies a zero
  conductance, so the result must be bit-identical to t0054 at gNMDA = 0 (which itself was
  bit-identical to t0052).
* **Placement bit-identical to t0054**: read
  `tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/results/placement_seed0.json` and assert
  per-synapse coordinates match.
* **NMDA voltage-dependence sanity test**: with a single NMDA_MgBlock point process
  voltage-clamped at v ∈ {-80, -60, -40, -20, 0, +20} mV, drive a single NetCon event and
  record peak gNMDA. Expected pattern: peak gNMDA at -80 mV is ~5x smaller than at -20 mV;
  peak gNMDA monotonically increases with depolarisation up to the asymptote.

## Compute and Budget

Local CPU only. Estimated wall-clock ≈ 75 minutes for 1440 trials at ~3 s/trial (matching
t0054). $0 cost. No remote machines.

If wall-clock exceeds 4 hours (as t0054's actual run did), abort and create a separate
parallelisation task (S-0054-06 covers exactly this).

## Out of Scope

* Joint (gAMPA, gNMDA, gGABA) conductance sweep (covered by S-0054-02).
* NMDA tau2 sweep at fixed gNMDA (covered by S-0054-05).
* Switching back to voltage-independent NMDA (`Voff = 1`) — kept available as a parameter for
  future ablation, not exercised in this task's sweep.
* Spatial PD/ND-asymmetric inhibition (covered by t0053).
* Any morphology, AMPA, GABA, or HH parameter changes.
* Improved EPSP-decay metric (covered by S-0054-03).

## Key Questions

1. Does the Mg-block NMDA recover vector-sum DSI at `gNMDA = 0.25 nS` to >= 0.50 (PASS) or
   does the collapse persist (FAIL)?
2. Does peak rate at `gNMDA = 0.25 nS` reach the >= 5 Hz threshold?
3. How does the DSI vs gNMDA curve compare to t0054's voltage-independent curve at every
   `gNMDA` value?
4. Does the Boltzmann gating work as expected in single-synapse voltage-clamp tests (sanity
   gate above)?

## Verification Criteria

* Library asset structure validates against `meta/asset_types/library/specification.md`.
* `metrics.json` contains 12 variants (4 × 3); all use the registered metric keys.
* All gates pass (quiescent rest, gNMDA=0 cross-task regression vs t0054, placement match,
  NMDA voltage-dependence sanity).
* The `gNMDA = 0` FULL variant reproduces t0054's gNMDA=0 row at 0e+00 Hz max diff across 120
  rows.
* Headline summary in `results_summary.md` explicitly states PASS or FAIL on the S-0054-01
  pass criterion (`vector-sum DSI > 0.50` and `peak Hz >= 5 Hz` at `gNMDA = 0.25 nS`, FULL).
* All 240+ per-direction PNGs and 11+ sweep-summary PNGs exist and are embedded in
  `results_detailed.md` (sample of headline figures inline; rest linked).

</details>
