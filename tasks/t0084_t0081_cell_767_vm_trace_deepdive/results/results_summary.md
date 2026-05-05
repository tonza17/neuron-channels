---
spec_version: "2"
task_id: "t0084_t0081_cell_767_vm_trace_deepdive"
---
# Results Summary: Vm-Trace Deep-Dive of t0081 Cell 767

## Summary

Re-evaluated t0081 Pareto cells 767 (joint-pass), 637, 762 (near-pass) on the v3 Bed B substrate
with extended Vm/conductance/current recording across 8 directions and computed an integrated
PD-vs-ND fractional channel contribution. Cell 767's PD/ND integrated-current asymmetry is
**NaP-dominant** (NMDA 0.0%, Nav1.6 7.0%, NaP 93.0%), and cells 637 and 762 share the same
NaP-dominant signature (98.5% and 99.9%). The single-replicate run did not reproduce cell 767's
original 5-seed mean DSI (0.494 vs. measured 0.000), so the attribution describes the parameter-set
biophysical signature rather than a per-trial joint-pass mechanism; multi-replicate confirmation
requires t0083 or a follow-up multi-seed study.

## Metrics

* **Cell 767 fractional contributions**: NMDA **0.0%**, Nav1.6 **7.0%**, NaP **93.0%** (dominant)
* **Cell 637 fractional contributions**: NMDA **0.0%**, Nav1.6 **1.5%**, NaP **98.5%** (dominant)
* **Cell 762 fractional contributions**: NMDA **0.0%**, Nav1.6 **0.1%**, NaP **99.9%** (dominant)
* **Simulations completed**: **24/24** stable runs (3 cells x 8 directions, no NaN Vm)
* **Figures produced**: **12** PNGs in `results/images/` (4 per cell)
* **Single-replicate measured DSI**: cell 767 = **0.000**, cell 637 = **0.143**, cell 762 =
  **0.000** (vs. t0081 5-seed means 0.494, 0.337, 0.314)

## Verification

* `meta.asset_types.answer.verificator` (cell-767-dendritic-spike-mechanism-attribution) - PASSED (0
  errors, 0 warnings)
* `verify_task_metrics` - PASSED (0 errors, 0 warnings)
* Remaining task verificators (`verify_task_results`, `verify_task_folder`, `verify_logs`,
  `verify_research_code`, `verify_task_dependencies`, `verify_suggestions`) - to be run at the
  reporting step

## Task Requirement Coverage

* **REQ-1** (24 simulations on v3 substrate, no NaN Vm) - **Done**: 24 stable .npz files in
  `results/data/`; all `is_stable=true` per `cellNNN_summary.json`.
* **REQ-2** (Vm at proximal soma / mid-dendrite / distal dendrite) - **Done**: arrays present in
  every traces .npz; recording sections recorded in `cellNNN_summary.json`.
* **REQ-3** (per-synapse NMDA conductance trajectories) - **Done**: `g_nmda_us` array per .npz.
* **REQ-4** (Nav1.6 and NaP currents at terminal dendrite segments) - **Done**: `i_nav16_ma_cm2` and
  `i_nap_ma_cm2` arrays per .npz.
* **REQ-5** (AIS Vm and spike onset times) - **Done**: `v_ais_mv` and per-direction spike count.
* **REQ-6 / REQ-7 / REQ-8 / REQ-9** (4 figures per cell) - **Done**: 12 PNGs in `results/images/`.
* **REQ-10** (Fractional-channel-contribution attribution metric) - **Done**: cell 767 NaP-dominant
  93.0%, cell 637 98.5%, cell 762 99.9%.
* **REQ-11** (Answer asset cell-767-dendritic-spike-mechanism-attribution) - **Done**: passes
  verificator with 0 errors / 0 warnings.
* **REQ-12** (Cells 637/762 attribution consistency check) - **Done**: both NaP-dominant; no
  near-pass cluster heterogeneity.
* **REQ-13** (Single-replicate confidence statement) - **Done**: confidence "medium" with explicit
  single-replicate limitation; multi-replicate follow-up referenced.
* **REQ-14** (12 PNGs embedded in `results_detailed.md`) - **Done**: see `results_detailed.md`
  Visualizations section.
