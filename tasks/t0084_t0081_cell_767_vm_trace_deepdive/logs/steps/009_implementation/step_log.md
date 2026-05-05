---
spec_version: "3"
task_id: "t0084_t0081_cell_767_vm_trace_deepdive"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-05T15:58:07Z"
completed_at: "2026-05-05T17:30:00Z"
---
# Implementation Step Log

## Summary

Executed the 24-simulation deep-dive matrix (3 cells x 8 directions) on the v3 Bed B substrate with
extended Vm/conductance/current recording, generated 12 PNG figures (4 per cell), computed the
fractional-channel-contribution attribution metric for cells 767, 637, 762, and produced one answer
asset attributing cell 767's PD/ND integrated-current asymmetry to NaP sustained depolarisation
(0.0% NMDA, 7.0% Nav1.6, 93.0% NaP). Cells 637 and 762 also showed NaP-dominant signatures (98.5%
and 99.9%), consistent with cell 767. The single-replicate run did not reproduce cell 767's original
5-seed mean DSI of 0.494 (re-evaluated DSI = 0.000), so the attribution describes the
parameter-set's biophysical signature rather than confirming a per-trial joint-pass mechanism.

## Actions Taken

1. Created task-local code package: `paths.py` (centralised Path constants), `constants.py`
   (CELL_IDS, response window, NMDA reversal), `run_deepdive.py` (24-simulation driver wrapping
   t0080's `build_dsgc_cell_with_ais`, `apply_parameter_vector`, and `run_one_trial` and attaching
   recording vectors before each `h.run()`), `attribution_metric.py` (fractional channel
   contribution from PD/ND integrated currents over [200, 1200] ms), `plot_figures.py` (4 figures
   per cell), and `answer_writer.py` (assembles the answer asset).
2. Ran the simulation pipeline locally: 24 stable simulations completed without NaN Vm; produced 24
   `.npz` trace files plus 3 `_summary.json` and 3 `_attribution.json` files in `results/data/`, and
   12 PNGs in `results/images/`.
3. Wrote the answer asset under `assets/answer/cell-767-dendritic-spike-mechanism-attribution/` with
   `details.json`, `short_answer.md`, `full_answer.md`. Verified with the answer-asset verificator
   (passed with 0 errors / 0 warnings after extending the "Evidence from Internet Sources" section).
   Fixed the pre-existing cp1252 em-dash encoding in `details.json` and removed an internal
   contradiction in the synthesis paragraph that incorrectly named NMDA as the dominant mechanism.
4. Wrote `results/metrics.json` (per-cell variants with `direction_selectivity_index`),
   `results/costs.json` ({"total_cost_usd": 0, "breakdown": {}}), and
   `results/remote_machines_used.json` ([]).
5. Ran `uv run ruff check --fix` and `uv run ruff format` on the code package (all checks passed, no
   changes needed) and `uv run mypy -p tasks.t0084_t0081_cell_767_vm_trace_deepdive.code` (success).

## Outputs

* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/paths.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/constants.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/run_deepdive.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/attribution_metric.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/plot_figures.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/answer_writer.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell{767,637,762}_dir{0,45,90,135,180,225,270,315}_traces.npz`
  (24 files)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell{767,637,762}_summary.json` (3
  files)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell{767,637,762}_attribution.json` (3
  files)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell{767,637,762}_fig{1..4}_*.png`
  (12 PNG figures)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/metrics.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/costs.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/remote_machines_used.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/details.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/short_answer.md`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/full_answer.md`

## Issues

* The pre-existing `details.json` contained Windows-1252 (cp1252) encoded em-dashes (byte 0x97)
  which broke UTF-8 JSON parsing. Resolved by rewriting the file with ASCII hyphens in place of
  em-dashes.
* The `full_answer.md` originally produced contained an internal contradiction in the Synthesis
  paragraph (text said "the dominant mechanism is NMDA Mg-block gain modulation" while the data
  showed NaP 93%). Resolved by rewriting the Synthesis section to align with the attribution data
  (NaP-dominant) and explicitly noting the single-replicate vs t0081 5-seed discrepancy.
* The single-replicate re-evaluation produced DSI = 0.000 for cell 767 (vs. t0081 5-seed mean
  0.494). This is documented as a limitation of the attribution: the metric describes a
  parameter-set biophysical signature, not a per-trial joint-pass mechanism. Multi-replicate
  follow-up (S-0081-01 or t0083) is needed to confirm the NaP-dominant attribution holds across the
  seeds that produce the joint-pass aggregate.
* Plan referenced `arf.scripts.verificators.verify_answer_asset` but that script does not exist; the
  canonical verificator is `meta.asset_types.answer.verificator`. Used the latter.

## Requirement Completion Checklist

* **REQ-1** (24 simulations on v3 substrate, no NaN Vm) - **Done**: 24 stable .npz files in
  `results/data/`; all `is_stable=true` per `cellNNN_summary.json` `direction_results`.
* **REQ-2** (Vm at proximal soma, mid-dendrite, distal dendrite) - **Done**: `v_soma_mv`,
  `v_mid_mv`, `v_distal_mv` arrays present in every `cellNNN_dirNNN_traces.npz`; recording sections
  recorded in `cellNNN_summary.json` `recording_sections`.
* **REQ-3** (per-synapse NMDA conductance trajectories) - **Done**: `g_nmda_us` (n_syns,
  n_timepoints) array present in every traces .npz.
* **REQ-4** (Nav1.6 and NaP currents at terminal dendrite segments) - **Done**: `i_nav16_ma_cm2` and
  `i_nap_ma_cm2` arrays (n_segs, n_timepoints) present in every traces .npz.
* **REQ-5** (AIS Vm and spike onset times via threshold crossing at -10 mV) - **Done**: `v_ais_mv`
  array recorded; spike count per direction in `cellNNN_summary.json` `direction_results`.
* **REQ-6** (Figure 1 per cell - Vm traces 3x8 grid) - **Done**:
  `cell{767,637,762}_fig1_vm_traces.png`.
* **REQ-7** (Figure 2 per cell - NMDA conductance overlay) - **Done**:
  `cell{767,637,762}_fig2_nmda_conductance.png`.
* **REQ-8** (Figure 3 per cell - Nav1.6/NaP current decomposition) - **Done**:
  `cell{767,637,762}_fig3_nav16_nap_current.png`.
* **REQ-9** (Figure 4 per cell - AIS spike onset) - **Done**:
  `cell{767,637,762}_fig4_ais_spikes.png`.
* **REQ-10** (Fractional-channel-contribution attribution metric over [200, 1200] ms) - **Done**:
  `cell{767,637,762}_attribution.json` with `frac_nmda`, `frac_nav16`, `frac_nap`, `delta_*_nA_ms`,
  and `dominant_mechanism` fields. Cell 767: NMDA 0.0%, Nav1.6 7.0%, NaP 93.0% (NaP-dominant).
* **REQ-11** (Answer asset with v2 spec) - **Done**:
  `assets/answer/cell-767-dendritic-spike-mechanism-attribution/{details.json, short_answer.md, full_answer.md}`.
  Verificator passes with 0 errors / 0 warnings.
* **REQ-12** (Cells 637 and 762 attribution consistency check) - **Done**: cells 637 and 762 also
  NaP-dominant (98.5% and 99.9%), consistent with cell 767. Documented in `full_answer.md` Evidence
  from Code or Experiments and Synthesis sections.
* **REQ-13** (Single-replicate confidence statement) - **Done**: confidence "medium";
  `full_answer.md` Limitations section explicitly states single-replicate constraint and
  generalisation requires t0083 / S-0081-01.
* **REQ-14** (12 PNGs to be embedded in `results_detailed.md`) - **Partial** (figures written to
  `results/images/`; embedding will be performed at the results step which writes
  `results_detailed.md`).
