# Results Summary: Minimal From-Scratch DSGC with Spatial PD/ND-Asymmetric Inhibition

## Summary

Built a from-scratch minimal DSGC on `dsgc-baseline-morphology-calibrated` (same morphology and
synapse placement seed as t0052) with 100 E + 100 I co-located synapses, position-gated AMPA-only
excitation, and **centripetal-only spatial gating** of GABA inhibition (each I synapse fires at full
2 nS amplitude only when `cos(θ_stim − θ_centrifugal_synapse) < 0`, zero otherwise). Ran the
full 12-direction × 10-trial × 3-mode sweep (360 trials in 17 min 11 s on local CPU). Headline
finding: **the FULL-mode tuning curve is identically 0 Hz across all directions** — the spatial
mechanism with full 2 nS GABA on ~50% of synapses fully suppresses spiking on this morphology /
synapse-density configuration. AMPA_ONLY fires uniformly at 0.667 Hz (excitation works at
threshold). The active-fraction soft sanity check passes (mean = 0.5000 ∈ [0.4, 0.6]).

## Metrics

* **Primary DSI (FULL)**: **0.0** — degenerate; both peak and null directions fire 0 Hz.
* **Peak Hz / Null Hz (FULL)**: **0.0 / 0.0** — full inhibitory suppression.
* **Vector-sum DSI (FULL)**: **0.0** — degenerate.
* **HWHM**: **180.0°** — degenerate (flat-zero tuning curve).
* **Tuning-curve RMSE vs t0004 target**: **17.18 Hz** — large because the t0004 target peaks near
  30 Hz while this model produces 0 Hz.
* **AMPA-only peak Hz**: **0.667 Hz** — same as t0052; confirms excitation works identically (same
  placement, same E mechanism).
* **Mean active-fraction**: **0.5000** ∈ [0.4, 0.6] soft band — **PASS**.
* **Per-direction active-fraction range**: **0.34 (θ = 30°) to 0.66 (θ = 210°)** — the
  spatial-gating mechanism does produce direction-dependent activation (more I synapses fire on
  null-side directions), but the absolute amplitude is enough to suppress spiking in every
  direction.
* **Aggregate IPSP peak (mV)**: from **6.33 mV (θ = 30°)** to **7.82 mV (θ = 210°)** — only
  ~1.24× variation, much smaller than the 3.0× active-synapse-count would suggest, due to
  driving-force saturation (same finding as t0052 IPSP voltage ratio of 1.54).
* **Placement match with t0052**: **bit-identical** placement_seed0.json — enables direct
  trial-for-trial cross-task comparison.

## Verification

* `meta.asset_types.library.verificator minimal_dsgc_spatial_gaba` — **PASSED** (0 errors / 0
  warnings).
* `verify_task_metrics.py t0053_minimal_dsgc_spatial_gaba` — **PASSED** (0 errors / 0 warnings).
* `verify_research_code.py` — **PASSED** (0/0).
* `verify_plan.py` — **PASSED** (0/0).
* `ruff check` and `ruff format` — clean across all task code modules.
* `mypy -p tasks.t0053_minimal_dsgc_spatial_gaba.code` — no issues.
* Soft active-fraction sanity check (compute_metrics.py): mean active-fraction 0.500 ∈ [0.4, 0.6]
  — **PASSED**.
* Quiescent-rest gate (`test_quiescent_rest.py`): V_rest = -65 mV ± 0.5 mV — **PASSED**.
* Spatial-gating unit test (`test_spatial_gating.py`): per-synapse
  `cos(θ_stim − θ_centrifugal) < 0` rule verified — **PASSED**.
* Placement bit-identical match with t0052 (`test_placement_seed0_match.py`) — **PASSED**.
