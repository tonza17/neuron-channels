# Minimal DSGC with Co-Located AMPA + NMDA Excitation and Scalar gabaMOD Inhibition

## Source

Suggestion S-0052-03 (medium priority): "Add NMDA component to t0052 minimal DSGC and measure
DSI / peak-rate response."

## Motivation

t0052 produced a from-scratch minimal DSGC with AMPA-only excitation and scalar gabaMOD
inhibition. The aggregate EPSP at the soma decays within ~30 ms after the last synapse fires
because per-synapse AMPA `tau2 = 2.5 ms` and the membrane time constant
`τ_m = R_m × C_m ≈ 6 ms`. Real DSGC EPSPs decay much more slowly because they have a
substantial NMDA component (typical NMDA decay τ ≈ 50-200 ms). t0052 also produced only one
spike per trial in FULL mode at the preferred direction, which over-saturates primary DSI to
1.0 trivially.

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
* All dendritic sections passive: `Rm = 5999 Ω·cm²`, `Ra = 100 Ω·cm`, `cm = 1 µF/cm²`,
  `V_rest = -65 mV`.

### Synapses

* 100 E + 100 I co-located pairs.
* **Excitation**: at each E location, both an AMPA and an NMDA `Exp2Syn` are co-located on
  the same segment, driven by **the same** `NetStim` event (one event per synapse per trial,
  position-gated by the bar). AMPA: `tau1 = 0.5 ms`, `tau2 = 2.5 ms`, `e = 0 mV`,
  peak `0.5 nS` (same as t0052). NMDA: `tau1 = 5 ms`, `tau2 = 80 ms`, `e = 0 mV`, peak
  conductance `gNMDA` (swept).
* NMDA is **voltage-independent** in this minimal model (no Mg²⁺ block). Voltage-dependent
  NMDA with proper Mg block is deferred to a follow-up task.
* **Inhibition**: scalar gabaMOD identical to t0052. `theta_PD = 0`, `theta_ND = 180`,
  peak `2 nS × gaba_mod(theta)` where `gaba_mod(0) = 0.33` and `gaba_mod(180) = 0.99`.

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
* `E_ONLY` — AMPA + NMDA active, GABA `NetCon` weights zeroed (replaces t0052's
  `AMPA_ONLY`).
* `GABA_ONLY` — AMPA + NMDA `NetCon` weights zeroed, GABA active.

## Outputs

### Per `gNMDA` value × per direction (4 × 12 = 48 panels per output type)

* Soma `V(t)` (FULL mode), mean ± SD across 10 trials.
* Aggregate EPSP (`E_ONLY`), mean ± SD.
* Aggregate IPSP (`GABA_ONLY`), mean ± SD.
* PSTH (5 ms bins, FULL mode).
* Per-synapse activation-time histogram.

Approximately 12 × 5 = 60 PNGs per `gNMDA` value × 4 sweep values = ~240 per-direction
PNGs, plus 8 polar/Cartesian per-`gNMDA` overview PNGs and 3 sweep-summary PNGs.

### Sweep summary (the headline plots)

1. **EPSP decay-time-constant vs gNMDA** — directly answers the user's question. X-axis:
   `gNMDA` (4 points). Y-axis: time from EPSP peak to `1/e` (≈ 36.8 %) of peak. One line per
   direction or one aggregate.
2. **Peak Hz vs gNMDA** — line plot, one curve per direction.
3. **DSI vs gNMDA** — primary DSI and vector-sum DSI vs `gNMDA`.

### `metrics.json` (multi-variant format)

One variant per `(gNMDA, mode)` combination = 12 variants. Each variant carries the
registered keys `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
`tuning_curve_reliability`, `tuning_curve_rmse`. Variant `id` schema:
`gnmda_<value>_<mode>` (e.g., `gnmda_0.50_full`).

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
  `TrialMode.AMPA_ONLY` → `TrialMode.E_ONLY` (or add `E_ONLY` and keep `AMPA_ONLY` as a
  legacy alias).
* **`synapses.py`** — extend `EiPair` with `nmda_syn`, `nmda_netcon`. `build_ei_pairs`
  creates the NMDA `Exp2Syn` at the same segment and a single shared `NetStim`-driven
  `NetCon`. `schedule_ei_onsets` accepts `gnmda_ns: float` and sets
  `nmda_netcon.weight[0] = gnmda_ns * 1e-3`. NMDA fires from the same `NetStim.start`
  as AMPA — no second NetStim is needed.
* **`run_tuning_curve.py`** — add an outer loop over `gNMDA` values. Per-mode CSVs gain a
  `gnmda_ns` column. File names get a per-`gNMDA` suffix or all `gNMDA` rows are appended to
  a single CSV (the latter is preferred for downstream analysis ergonomics).
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
