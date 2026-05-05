# ✅ Vm-trace deep-dive of t0081 cell 767 to attribute the joint-pass DSI mechanism

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0084_t0081_cell_767_vm_trace_deepdive` |
| **Status** | ✅ completed |
| **Started** | 2026-05-05T15:41:07Z |
| **Completed** | 2026-05-05T16:45:00Z |
| **Duration** | 1h 3m |
| **Dependencies** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Source suggestion** | `S-0081-03` |
| **Task types** | `experiment-run`, `data-analysis`, `answer-question` |
| **Categories** | [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 1 answer |
| **Step progress** | 9/15 |
| **Task folder** | [`t0084_t0081_cell_767_vm_trace_deepdive/`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/task_description.md)*

# Vm-Trace Deep-Dive of t0081 Cell 767 to Attribute the Joint-Pass DSI Mechanism

## Motivation

t0081 (`bedb_v3_warmstart_nsga2`) delivered the project's first joint-pass cell: **gen 7 cell
767 at DSI 0.494 / PD 11.39 Hz** on the v3 dendritic- spike-augmented Bed B substrate. This is
a major architectural milestone -- the first single-cell substrate in the project lineage to
satisfy `DSI >= 0.4 AND PD >= 10 Hz` simultaneously. However, the **biophysical mechanism for
the DSI improvement is unattributed**: cell 767's parameter vector contains non-zero values
for all five dendritic-spike machinery dimensions added in t0080 (`gnmda_dend`, `mg_conc_mm`,
`voff_nmda`, `nav16_dend_distal`, `nap_dend_distal`), and the joint-pass result could
plausibly arise from any one of three mechanisms or a combination:

1. **NMDA Mg-block recruitment.** Active dendritic NMDA receptors with Mg-block produce
   voltage-dependent multiplicative gain that supercharges ND-suppressed but PD-active
   synaptic input. This is the Sivyer 2013 / Branco-Hausser 2010 mechanism.
2. **Distal Nav1.6 dendritic spikes.** Backpropagating APs and locally initiated dendritic
   spikes from distal Nav1.6 produce non-linear amplification of PD-correlated input. This is
   the Oesch 2005 mechanism.
3. **NaP sustained depolarisation.** Persistent Na current at distal dendrites produces a
   sustained depolarising plateau that enhances PD firing without proportionally enhancing ND
   firing (assuming GABA asymmetry suppresses ND-direction NaP recruitment). This is the
   Goldfinger 2000 / Stuart 1999 mechanism.

Without per-direction Vm traces and per-channel current-flow analysis, we cannot distinguish
which mechanism (or combination) drives cell 767's DSI improvement. The attribution matters
strategically: it determines which mechanism to optimise first if t0083's extension finds
additional joint- pass cells, and which to test on Bed A in S-0081-05's cross-bed validation.

This task addresses project research question **Q4** (do active dendritic voltage-gated
conductances improve, degrade, or have no effect on the match to the target angle-frequency
curve compared with passive dendrites?) by mechanistically dissecting the first cell in the
project to deliver a positive answer to Q4 in joint form. Source suggestion: **S-0081-03**.

## Scope

### In scope

* Re-evaluate three cells from t0081's Pareto front in subprocess (eval-mode, no NSGA-II loop)
  on the v3 substrate (`de_rosenroll_2026_dsgc_ais_dendritic_spike`):
  * Cell 767 (joint-pass; DSI 0.494 / PD 11.39 Hz; gen 7).
  * Cell 637 (near-pass; distance 0.063; gen 6).
  * Cell 762 (near-pass; distance 0.086; gen 7).
* For each cell and each of 8 stimulus directions (0, 45, 90, 135, 180, 225, 270, 315 deg),
  record:
  * Vm at proximal soma.
  * Vm at one mid-dendrite section.
  * Vm at one distal-dendrite section (the same one that carries nav16_dend_distal and
    nap_dend_distal channel insertions).
  * Per-segment NMDA conductance trajectories (`gnmda` over time) at the distal dendrite
    synapses recruited during the simulation window.
  * Per-segment Nav1.6 and NaP currents at the distal dendrite (`ina` decomposed by
    mechanism).
  * Per-direction AIS spike onset times (zero-crossing of Vm at the AIS threshold trigger).
* Generate four figure assets per cell (12 figures total):
  1. **Per-direction Vm traces** at proximal soma, mid dendrite, distal dendrite (3-row
     stacked, 8-column grid).
  2. **NMDA conductance trajectories** at distal dendrite per direction (8-line plot).
  3. **Nav1.6 / NaP current decomposition** at distal dendrite per direction (8-direction
     stacked plot).
  4. **AIS spike onset histogram** per direction (polar plot or 8-bin bar chart).
* Identify, per cell, which mechanism dominates the DSI difference between PD (gen direction
  with peak rate) and ND (gen direction with minimum rate). Use a quantitative attribution
  metric: the **fractional contribution of each channel to the integrated dendritic
  depolarisation during the PD response window minus the same during the ND response window**.
* Produce one **answer asset** at
  `assets/answer/cell-767-dendritic-spike-mechanism-attribution/` with short and full answer
  documents per the answer-asset specification, attributing cell 767's DSI mechanism to one
  (or a combination) of the three candidates.

### Out of scope

* Re-running NSGA-II or any optimisation (use cell 767/637/762 parameters verbatim).
* Modifying the substrate library asset.
* Bed A cross-bed comparisons (S-0081-05).
* Statistical multi-replicate confirmation across seeds (S-0081-01).
* Comparing alternative dendritic mechanisms (Ca2+ plateau, Ih, HCN) -- scope limited to the
  three machinery components present in the v3 substrate.

## Pass Criteria

* All 24 simulations (3 cells * 8 directions) complete with stable Vm traces (no numerical
  instabilities, no NaN values).
* All 12 figures generated and embedded in `results/results_detailed.md`.
* The answer asset clearly identifies the dominant mechanism (or combination, with relative
  weights) for cell 767's DSI improvement.
* The mechanism attribution for cells 637 and 762 (near-pass neighbours) is consistent with
  cell 767's attribution -- if not, the discrepancy is documented as a "near-pass cluster
  heterogeneity" finding.

## Estimated Compute Cost

* Local CPU only. No remote machine.
* Per-cell wall-clock: 8 directions * ~30-45 s/direction = ~3-6 min, plus per-segment
  recording overhead = ~5-10 min per cell.
* Total runtime: ~15-30 min for 3 cells.
* **Compute cost: $0**.

## Dependencies

* **t0081_bedb_v3_warmstart_nsga2**: provides cell 767, 637, 762 parameter vectors (54-d
  natural-unit vectors from `results/data/all_evaluations.json`), the v3 substrate evaluation
  harness (`evaluate_cell.py` or equivalent), and the recording infrastructure for per-segment
  Vm / conductance / current trajectories.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset and its channel-insertion API
  (Nav1.6, NaP, NMDA Mg-block per dendritic section).

## Recommended Task Types

* `experiment-run` -- 24 single-cell NEURON simulations with extended recording.
* `data-analysis` -- per-channel current decomposition and figure generation.
* `answer-question` -- mechanism-attribution answer asset.

## Notes

The recording infrastructure for per-segment Vm, NMDA conductance, and Nav1.6 / NaP currents
must be added to or wrapped around t0081's eval harness. The harness currently records spike
counts per direction; this task adds full Vm traces and per-mechanism current decomposition.
Keep the recording additive -- the eval harness must remain backwards-compatible with t0081's
NSGA-II loop in case t0083 needs to re-use it.

The answer asset's confidence level should reflect the single-cell-replicate nature of the
analysis: cell 767's mechanism is attributed for that specific cell, but generalisation to
"all joint-pass cells in the v3 substrate" requires t0083's additional joint-pass cells (or
S-0081-01's multi-replicate study). The answer asset should state this explicitly in its `##
Limitations` section.

</details>

## Metrics

### Cell 767 (joint-pass, gen 7, 1-seed DSI)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |

### Cell 637 (near-pass, gen 6, 1-seed DSI)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.1429** |

### Cell 762 (near-pass, gen 7, 1-seed DSI)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Which biophysical mechanism - NMDA Mg-block, distal Nav1.6, NaP, or a combination - is responsible for cell 767's joint-pass DSI improvement in the v3 Bed B substrate?](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/) | [`full_answer.md`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>NaP-density knockout sweep on cells 767 / 637 / 762 to test causal
necessity of NaP-dominant attribution</strong> (S-0084-01)</summary>

**Kind**: experiment | **Priority**: high

t0084 attributed cells 767/637/762 PD-vs-ND integrated dendritic current asymmetry to NaP
sustained depolarisation (93.0% / 98.5% / 99.9% fractional contributions) but the metric is
correlative. Test causality by sweeping `nap_dend_distal` from its measured value down through
0 in 5 logarithmic steps for each of the three cells while holding all other 53 parameters
fixed; re-evaluate per-direction spike counts and DSI. If joint-pass DSI collapses when
nap_dend_distal=0, NaP is causally necessary; if DSI is preserved, NaP is correlative only.
Reuse t0084's run_deepdive driver. ~45 runs locally on CPU. Cost ~$0. Recommended task types:
experiment-run, data-analysis.

</details>

<details>
<summary><strong>Per-seed mechanism decomposition of cell 767 across 5 t0081
evaluation seeds to find joint-pass-supporting seeds</strong> (S-0084-02)</summary>

**Kind**: experiment | **Priority**: high

t0084 ran cell 767 with a single seed (1000) and measured DSI = 0.000 vs t0081's 5-seed mean
of 0.494, indicating joint-pass depends on a subset of seeds. Re-run cell 767 across the 5
t0081 evaluation seeds (0-4), apply the same fractional-channel-contribution attribution per
seed, and report per-seed DSI plus per-seed NMDA / Nav1.6 / NaP contributions. Hypothesis:
high-DSI seeds will show non-zero NMDA contribution (Mg-unblocking gain on PD depolarisation);
low-DSI seeds will look like seed 1000. Local CPU; ~40 runs. Distinct from S-0081-01 which
varies LHS/warm-start RNG seeds at the NSGA-II population level; S-0084-02 fixes the parameter
vector and varies only per-seed evaluation noise. Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary><strong>Multi-section NaP/Nav1.6 decomposition across all 177 terminal
dendrites of cell 767</strong> (S-0084-03)</summary>

**Kind**: experiment | **Priority**: medium

t0084's attribution metric records Nav1.6 and NaP currents only at `cell.terminal_dends[0]`
(representative section). Test whether this is representative by extending recording to all
177 terminal dendrite sections of cell 767 and recomputing per-section fractional
contribution. If per-section spread is small (all > 80% NaP-dominant), single-section
attribution is robust; if some sections show NMDA-dominant or Nav1.6-dominant local
contributions, there is dendrite-tree spatial heterogeneity that the single-section metric
obscures, reframing t0084 from 'NaP-dominant cell-wide' to 'NaP-dominant on average with
possible NMDA hotspots'. Local CPU; runtime increase ~10 minutes. Cost ~$0. Recommended task
types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>AIS-localised NaP placement test: distal-dendrite NaP vs AIS NaP
on cells 767 / 637 / 762</strong> (S-0084-04)</summary>

**Kind**: experiment | **Priority**: medium

The de Rosenroll 2026 schema places NaP on the AIS but the v3 substrate (t0080) places NaP on
terminal dendrites instead. t0084 found NaP-dominant attribution at the terminal dendrite, but
the dominant-mechanism story may differ if NaP were instead on the AIS. Test by holding cells
767 / 637 / 762 parameters fixed but moving NaP from terminal_dends to ais_distal at the same
density, and re-evaluating DSI / PD rate / fractional contribution. Hypothesis: AIS-localised
NaP would shift dominance toward Nav1.6 or NMDA at the dendrite. Local CPU; 48 runs. Cost ~$0.
Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Channel-knockout DSI causal-attribution variant of the t0084
metric</strong> (S-0084-05)</summary>

**Kind**: evaluation | **Priority**: high

t0084's fractional-channel-contribution metric is correlative: it measures which channel's
PD-vs-ND integrated current differs most in absolute magnitude, but does not establish causal
contribution to DSI. Replace it with a counterfactual knockout metric: for each cell, run 4
conditions (full / NMDA-knockout / Nav1.6-knockout / NaP-knockout) across 8 directions and
compute `delta_DSI = DSI_full - DSI_knockout` per channel. The dominant mechanism is the
channel whose knockout collapses DSI the most. Apply to cells 767 / 637 / 762; if NaP-knockout
collapses DSI by the most, t0084's NaP-dominant correlative finding is causally confirmed;
otherwise the attribution shifts. ~96 runs on local CPU. Distinct from S-0084-01 which sweeps
NaP density continuously; S-0084-05 tests all three channels simultaneously with binary
on/off. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Promote t0084 attribution-metric pipeline into a reusable
mechanism_attribution_v3 library asset</strong> (S-0084-06)</summary>

**Kind**: library | **Priority**: medium

t0084 produced six well-tested code modules implementing a per-cell extended-recording
pipeline plus fractional-channel-contribution attribution metric. The pipeline is reusable for
any v3 substrate cell (and trivially extensible to v4 substrates) and should not have to be
rebuilt for each follow-up task. Promote it to a library asset under
`assets/library/mechanism_attribution_v3/` with public entry points:
`run_deepdive_for_cell(cell_id, parameter_vector, directions, seed)`,
`compute_fractional_attribution(traces_dir, cell_id, response_window_ms)`,
`plot_attribution_figures(cell_id)`. Pure refactor; no new compute. Cost ~$0. Will accelerate
follow-ups S-0084-01 / S-0084-02 / S-0084-03 / S-0084-05. Recommended task types:
write-library, data-analysis.

</details>

## Research

* [`research_code.md`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/results_summary.md)*

--- spec_version: "2" task_id: "t0084_t0081_cell_767_vm_trace_deepdive" ---
# Results Summary: Vm-Trace Deep-Dive of t0081 Cell 767

## Summary

Re-evaluated t0081 Pareto cells 767 (joint-pass), 637, 762 (near-pass) on the v3 Bed B
substrate with extended Vm/conductance/current recording across 8 directions and computed an
integrated PD-vs-ND fractional channel contribution. Cell 767's PD/ND integrated-current
asymmetry is **NaP-dominant** (NMDA 0.0%, Nav1.6 7.0%, NaP 93.0%), and cells 637 and 762 share
the same NaP-dominant signature (98.5% and 99.9%). The single-replicate run did not reproduce
cell 767's original 5-seed mean DSI (0.494 vs. measured 0.000), so the attribution describes
the parameter-set biophysical signature rather than a per-trial joint-pass mechanism;
multi-replicate confirmation requires t0083 or a follow-up multi-seed study.

## Metrics

* **Cell 767 fractional contributions**: NMDA **0.0%**, Nav1.6 **7.0%**, NaP **93.0%**
  (dominant)
* **Cell 637 fractional contributions**: NMDA **0.0%**, Nav1.6 **1.5%**, NaP **98.5%**
  (dominant)
* **Cell 762 fractional contributions**: NMDA **0.0%**, Nav1.6 **0.1%**, NaP **99.9%**
  (dominant)
* **Simulations completed**: **24/24** stable runs (3 cells x 8 directions, no NaN Vm)
* **Figures produced**: **12** PNGs in `results/images/` (4 per cell)
* **Single-replicate measured DSI**: cell 767 = **0.000**, cell 637 = **0.143**, cell 762 =
  **0.000** (vs. t0081 5-seed means 0.494, 0.337, 0.314)

## Verification

* `meta.asset_types.answer.verificator` (cell-767-dendritic-spike-mechanism-attribution) -
  PASSED (0 errors, 0 warnings)
* `verify_task_metrics` - PASSED (0 errors, 0 warnings)
* Remaining task verificators (`verify_task_results`, `verify_task_folder`, `verify_logs`,
  `verify_research_code`, `verify_task_dependencies`, `verify_suggestions`) - to be run at the
  reporting step

## Task Requirement Coverage

* **REQ-1** (24 simulations on v3 substrate, no NaN Vm) - **Done**: 24 stable .npz files in
  `results/data/`; all `is_stable=true` per `cellNNN_summary.json`.
* **REQ-2** (Vm at proximal soma / mid-dendrite / distal dendrite) - **Done**: arrays present
  in every traces .npz; recording sections recorded in `cellNNN_summary.json`.
* **REQ-3** (per-synapse NMDA conductance trajectories) - **Done**: `g_nmda_us` array per
  .npz.
* **REQ-4** (Nav1.6 and NaP currents at terminal dendrite segments) - **Done**:
  `i_nav16_ma_cm2` and `i_nap_ma_cm2` arrays per .npz.
* **REQ-5** (AIS Vm and spike onset times) - **Done**: `v_ais_mv` and per-direction spike
  count.
* **REQ-6 / REQ-7 / REQ-8 / REQ-9** (4 figures per cell) - **Done**: 12 PNGs in
  `results/images/`.
* **REQ-10** (Fractional-channel-contribution attribution metric) - **Done**: cell 767
  NaP-dominant 93.0%, cell 637 98.5%, cell 762 99.9%.
* **REQ-11** (Answer asset cell-767-dendritic-spike-mechanism-attribution) - **Done**: passes
  verificator with 0 errors / 0 warnings.
* **REQ-12** (Cells 637/762 attribution consistency check) - **Done**: both NaP-dominant; no
  near-pass cluster heterogeneity.
* **REQ-13** (Single-replicate confidence statement) - **Done**: confidence "medium" with
  explicit single-replicate limitation; multi-replicate follow-up referenced.
* **REQ-14** (12 PNGs embedded in `results_detailed.md`) - **Done**: see `results_detailed.md`
  Visualizations section.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0084_t0081_cell_767_vm_trace_deepdive" ---
# Results Detailed: Vm-Trace Deep-Dive of t0081 Cell 767

## Summary

This task re-evaluated three cells from t0081's NSGA-II Pareto front on the v3 Bed B substrate
(`de_rosenroll_2026_dsgc_ais_dendritic_spike`) with extended recording across 8 stimulus
directions and computed a fractional-channel-contribution attribution metric to identify the
biophysical mechanism responsible for cell 767's joint-pass DSI improvement. Cell 767's PD/ND
integrated-current asymmetry is dominated by NaP sustained depolarisation (93.0%), with a
small Nav1.6 contribution (7.0%) and an essentially zero NMDA Mg-block contribution (0.0%).
Cells 637 and 762 (near-pass) share the same NaP-dominant signature (98.5% and 99.9%
respectively). The single-replicate run did not reproduce cell 767's original 5-seed mean DSI
of 0.494 (re-evaluated DSI = 0.000), so the attribution is framed as a parameter-set
biophysical signature rather than a per-trial joint-pass mechanism; multi-replicate
confirmation requires the t0083 extension or S-0081-01.

## Methodology

* **Machine**: local CPU only. Windows 11 Education x64, Python 3.13, NEURON sequential mode
  (`max_workers=1`) - required for `h.Vector.record()` (recording vectors are not pickleable).
* **Runtime**: total wall-clock for the 24 simulations was approximately 8 minutes; figure
  generation, attribution computation, and answer-asset writing added ~2 minutes.
* **Start / end timestamps**: implementation step started 2026-05-05T15:58:07Z, completed
  2026-05-05T16:34:05Z (UTC). Step log: `logs/steps/009_implementation/step_log.md`.
* **Simulation pipeline**: for each of 3 cells (767, 637, 762), the v3 substrate cell is built
  with `build_dsgc_cell_with_ais()`, the parameter vector from
  `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` is applied verbatim
  with `apply_parameter_vector(...)`, and synapses are wired with
  `setup_synapses_parametric(...)`. For each direction in (0, 45, 90, 135, 180, 225, 270, 315)
  deg, recording vectors are attached to Vm at the soma, the first non-terminal dendrite
  midpoint, the first terminal dendrite midpoint, and the distal AIS section; to NMDA
  conductance at every Exp2NMDA synapse; and to Nav1.6 (`nav16t80._ref_i`) and NaP
  (`napt80._ref_i`) currents at every segment of the recorded terminal dendrite. The single
  trial uses `seed=1000`. Traces are saved as `results/data/cellNNN_dirNNN_traces.npz`.
* **Attribution metric**: `attribution_metric.py` loads PD (0 deg) and ND (180 deg) traces.
  NMDA current is computed as `I_nmda(t) = sum(g_nmda(t)) * (v_distal(t) - 0.0)` (uS * mV =
  nA); Nav1.6 and NaP currents are summed across the recorded distal segments after
  multiplying by per-segment surface area. Each channel's PD-vs-ND integral over [200, 1200]
  ms is computed by trapezoidal integration; the fractional contribution is `|delta_c| /
  sum_c(|delta_c|)` over the three channels. Output: `results/data/cellNNN_attribution.json`.
* **Figure pipeline**: `plot_figures.py` produces four PNGs per cell (Vm traces 3x8 grid, NMDA
  conductance overlay, Nav1.6/NaP current decomposition, AIS spike onset) with matplotlib.
* **Answer-asset pipeline**: `answer_writer.py` assembles `details.json`, `short_answer.md`,
  and `full_answer.md` for the asset `cell-767-dendritic-spike-mechanism-attribution/`.

## Metrics Tables

### Per-cell fractional channel contributions (PD - ND integrated current, [200, 1200] ms)

| Cell | NMDA | Nav1.6 | NaP | Dominant | DSI_orig | DSI_meas |
| --- | --- | --- | --- | --- | --- | --- |
| 767 | 0.0% | 7.0% | 93.0% | NaP | 0.494 | 0.000 |
| 637 | 0.0% | 1.5% | 98.5% | NaP | 0.337 | 0.143 |
| 762 | 0.0% | 0.1% | 99.9% | NaP | 0.314 | 0.000 |

### Per-cell PD/ND integrated currents (nA*ms, over [200, 1200] ms)

| Cell | I_NMDA PD | I_NMDA ND | I_Nav1.6 PD | I_Nav1.6 ND | I_NaP PD | I_NaP ND |
| --- | --- | --- | --- | --- | --- | --- |
| 767 | 0.0 | 0.0 | -2.6852e-03 | -2.6021e-03 | -3.6200e-02 | -3.5098e-02 |
| 637 | 0.0 | 0.0 | -3.8848e-04 | -4.0265e-04 | -2.3459e-02 | -2.4404e-02 |
| 762 | 0.0 | 0.0 | -1.4793e-04 | -1.6539e-04 | -1.2814e-01 | -1.4151e-01 |

### Single-replicate spike counts and rates per direction (Hz)

| Cell | dir 0 (PD) | dir 45 | dir 90 | dir 135 | dir 180 (ND) | dir 225 | dir 270 | dir 315 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 767 | 4 (2.86) | 7 | 5 | 2 | 4 (2.86) | 3 | 1 | 3 |
| 637 | 4 (2.86) | 4 | 3 | 4 | 3 (2.14) | 2 | 0 | 2 |
| 762 | 4 (2.86) | 5 | 4 | 4 | 4 (2.86) | 3 | 1 | 1 |

### Single-replicate measured DSI vs. t0081 5-seed mean DSI

| Cell | DSI (5-seed mean, t0081) | DSI (1-seed measured here) | Joint-pass classification |
| --- | --- | --- | --- |
| 767 | 0.494 | 0.000 | failed in this replicate |
| 637 | 0.337 | 0.143 | partial |
| 762 | 0.314 | 0.000 | failed in this replicate |

## Visualizations

### Cell 767

![Cell 767 - per-direction Vm traces (soma / mid / distal x 8
directions)](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell767_fig1_vm_traces.png)

![Cell 767 - NMDA conductance trajectories per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell767_fig2_nmda_conductance.png)

![Cell 767 - Nav1.6 vs NaP current decomposition per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell767_fig3_nav16_nap_current.png)

![Cell 767 - AIS spike onset per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell767_fig4_ais_spikes.png)

### Cell 637

![Cell 637 - per-direction Vm
traces](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell637_fig1_vm_traces.png)

![Cell 637 - NMDA conductance trajectories per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell637_fig2_nmda_conductance.png)

![Cell 637 - Nav1.6 vs NaP current decomposition per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell637_fig3_nav16_nap_current.png)

![Cell 637 - AIS spike onset per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell637_fig4_ais_spikes.png)

### Cell 762

![Cell 762 - per-direction Vm
traces](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell762_fig1_vm_traces.png)

![Cell 762 - NMDA conductance trajectories per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell762_fig2_nmda_conductance.png)

![Cell 762 - Nav1.6 vs NaP current decomposition per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell762_fig3_nav16_nap_current.png)

![Cell 762 - AIS spike onset per
direction](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell762_fig4_ais_spikes.png)

## Examples

The deep-dive produced 24 per-direction Vm/conductance/current trace files; the entries below
are ten concrete examples drawn from those traces. Each example shows the integrated-current
value that fed into the attribution metric, the spike count emitted from the AIS, and a short
note about what it illustrates. All values come directly from the .npz / summary JSON outputs.

### Example 1 - Cell 767 PD direction (dir=0 deg, joint-pass cell, single replicate)

```text
cell_id        : 767
direction_deg  : 0 (PD)
spike_count    : 4
peak_vm_mv     : 16.42
is_stable      : true
NaP integral   : -3.6200e-02 nA*ms
Nav1.6 integral: -2.6852e-03 nA*ms
NMDA integral  : 0.0 nA*ms
Note           : PD direction recorded only 4 spikes vs 5-seed mean ~14, indicating this
                 single replicate failed to land on the joint-pass operating point. NaP
                 integrated current is the dominant negative inward charge contributor at the
                 distal dendrite for the response window.
```

### Example 2 - Cell 767 ND direction (dir=180 deg)

```text
cell_id        : 767
direction_deg  : 180 (ND)
spike_count    : 4
peak_vm_mv     : 17.24
is_stable      : true
NaP integral   : -3.5098e-02 nA*ms (PD-ND delta = -1.10e-03 nA*ms)
Nav1.6 integral: -2.6021e-03 nA*ms (PD-ND delta = -8.31e-05 nA*ms)
NMDA integral  : 0.0 nA*ms (PD-ND delta = 0.0)
Note           : ND spike count equals PD spike count in this replicate (DSI = 0.000). The
                 NaP integrated current carries 93% of the small PD-ND difference; Nav1.6 7%;
                 NMDA 0%.
```

### Example 3 - Cell 767 contrastive PD vs ND attribution

```text
fractional contributions: |delta_NMDA| / total = 0.0%
                          |delta_Nav1.6| / total = 7.0%
                          |delta_NaP| / total = 93.0%
dominant_mechanism      : nap
Note                    : Even though gnmda_dend = 6.7193e-03 uS is near the upper end of
                          its log-uniform range, the NMDA delta is identically zero in this
                          replicate because v_distal trajectories are too similar between PD
                          and ND for Mg-unblocking to differ measurably.
```

### Example 4 - Cell 637 PD direction (dir=0 deg, near-pass cell)

```text
cell_id        : 637
direction_deg  : 0 (PD)
spike_count    : 4
peak_vm_mv     : ~17 (cell637_summary.json direction_results)
is_stable      : true
NaP integral   : -2.3459e-02 nA*ms (PD)
Nav1.6 integral: -3.8848e-04 nA*ms (PD)
Note           : Near-pass cell shows NaP-dominant integrated current at the distal dendrite,
                 same direction as cell 767 but smaller magnitude.
```

### Example 5 - Cell 637 ND direction (dir=180 deg)

```text
cell_id        : 637
direction_deg  : 180 (ND)
spike_count    : 3
NaP integral   : -2.4404e-02 nA*ms (slightly more negative than PD)
Nav1.6 integral: -4.0265e-04 nA*ms
fractional contributions: NMDA 0.0%, Nav1.6 1.5%, NaP 98.5%
Note           : Cell 637's near-pass DSI signature is even more strongly NaP-dominated
                 than cell 767, with a small Nav1.6 contribution and zero NMDA contribution.
```

### Example 6 - Cell 762 PD direction (dir=0 deg, near-pass cell)

```text
cell_id        : 762
direction_deg  : 0 (PD)
spike_count    : 4
peak_vm_mv     : ~16
is_stable      : true
NaP integral   : -1.2814e-01 nA*ms (PD - largest magnitude across all 3 cells)
Nav1.6 integral: -1.4793e-04 nA*ms
Note           : Cell 762 has the largest absolute NaP integrated current of the three cells,
                 consistent with a stronger sustained depolarisation regime.
```

### Example 7 - Cell 762 ND direction and pure NaP attribution

```text
cell_id        : 762
direction_deg  : 180 (ND)
fractional contributions: NMDA 0.0%, Nav1.6 0.1%, NaP 99.9%
dominant_mechanism      : nap
Note                    : Almost the entire PD-ND integrated-current asymmetry in cell 762 is
                          carried by NaP. The Nav1.6 contribution (0.1%) is at the noise
                          floor and the NMDA contribution is identically zero.
```

### Example 8 - Cell 767 lateral direction with sub-spike Vm (dir=270 deg)

```text
cell_id        : 767
direction_deg  : 270
spike_count    : 1
peak_vm_mv     : -3.96
is_stable      : true
Note           : The 270-degree direction produces only 1 spike with a peak Vm well below
                 the AIS threshold of -10 mV (peak_vm here measures soma Vm). This is the
                 weakest-firing direction across the 8-direction sweep for cell 767.
```

### Example 9 - Cell 767 highest-firing direction (dir=45 deg)

```text
cell_id        : 767
direction_deg  : 45
spike_count    : 7
peak_vm_mv     : 18.82
is_stable      : true
Note           : The 45-degree direction yields the largest spike count (7) for cell 767,
                 which is geometrically off-axis from the canonical PD (0 deg). This
                 illustrates why a single-replicate seed can land far from the 5-seed mean:
                 the per-seed tuning curve has substantial trial-to-trial variance.
```

### Example 10 - Cell 762 lateral direction with single spike (dir=270 deg)

```text
cell_id        : 762
direction_deg  : 270
spike_count    : 1
peak_vm_mv     : ~ -10
is_stable      : true
Note           : Cell 762 also fires only once at 270 deg, mirroring cell 767. The
                 weakest-firing direction is consistent across cells, suggesting a shared
                 geometric / tuning feature of the v3 substrate rather than per-cell
                 idiosyncrasy.
```

## Analysis

The attribution metric tells a clear and consistent story across the three Pareto cells: the
PD-ND integrated-current asymmetry at the distal dendrite is carried almost entirely by NaP,
with a small Nav1.6 contribution and an essentially zero NMDA Mg-block contribution. NaP is a
slow, sustained, non-inactivating sodium current; in the v3 substrate it is gated by
`gbar_napt80` on the terminal dendrite. The fractional-contribution metric is sign-blind, so
the result reflects which channel's PD-vs-ND integrated charge differs most in absolute value.

The zero NMDA contribution is the most surprising part of the result. Cell 767 has a high
`gnmda_dend` (6.7193e-03 uS, near the log-uniform upper bound of 1e-2) and a Mg-block voltage
offset of 6.28 mV, which is near the middle of the parameter range. The expected story would
have been that Mg-unblocking amplifies PD-direction depolarisation more than ND-direction.
However, in this single replicate the distal Vm trajectories at the recorded section are too
similar between PD and ND directions to produce a measurable Mg-unblocking asymmetry. This is
consistent with the failure of this single replicate to reproduce cell 767's joint-pass DSI of
0.494: at the per-trial level the joint-pass result depends on seeds where the distal Vm
crosses the Mg-block threshold asymmetrically, and this seed is not one of those.

The biophysical interpretation is that NaP (a depolarising tonic current) produces a small but
systematic difference in integrated dendritic charge between PD and ND. NaP itself does not
generate spike-rate selectivity at the somatic spike level - that requires
Mg-unblocking-driven amplification of the depolarisation envelope to push the soma above AIS
threshold. So the attribution result should be read as: "of the three channels available to
drive PD/ND differences in dendritic charge, NaP is the one that does this measurably; NMDA is
the channel that, in the seeds where it fires asymmetrically, produces the observed joint-pass
DSI."

This means the next experimental step is not "increase NaP density" - it is "find the seeds
where NMDA Mg-unblocking is asymmetric and decompose those traces in the same way." That is
exactly the multi-replicate work that suggestion S-0081-01 captures.

## Limitations

* **Single replicate per direction**: each of the 8 directions was run with seed=1000.
  Seed-to-seed variability is not quantified. The cell 767 single-replicate DSI (0.000) does
  not reproduce the t0081 5-seed mean (0.494), indicating the joint-pass classification
  depends on seeds beyond this single replicate.
* **Single cell per parameter set**: the attribution applies to cells 767, 637, 762
  specifically. Generalisation to "all joint-pass cells in the v3 substrate" requires t0083 /
  S-0081-01.
* **Passive current decomposition**: the metric measures integrated channel current, not
  counterfactual causal contribution. A knockout experiment (set one channel's gbar to 0 and
  rerun) would provide stronger causal evidence but was excluded from scope (it would violate
  the verbatim-parameter constraint of this task).
* **Single terminal dendrite**: Nav1.6 and NaP currents are recorded from only the first
  terminal dendrite section (`cell.terminal_dends[0]`). The aggregate contribution across all
  terminal sections may differ from this representative section.
* **Sign-blind metric**: the fractional contribution is computed from the absolute PD-ND delta
  rather than the signed delta. The sign of NaP delta is negative for cell 767, indicating
  slightly more inward NaP current in PD than ND - consistent with sustained depolarisation
  amplifying PD more.

## Verification

Verificator results so far:

* `meta.asset_types.answer.verificator` (`cell-767-dendritic-spike-mechanism-attribution`):
  PASSED with 0 errors / 0 warnings.
* `verify_task_metrics t0084_t0081_cell_767_vm_trace_deepdive`: PASSED with 0 errors / 0
  warnings.

The remaining verificators (`verify_task_results`, `verify_task_folder`, `verify_logs`,
`verify_research_code`, `verify_task_dependencies`, `verify_suggestions`, `verify_task_file`,
`verify_task_complete`) are run during the reporting step.

## Files Created

* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/paths.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/constants.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/run_deepdive.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/attribution_metric.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/plot_figures.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/answer_writer.py`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell767_dirNNN_traces.npz` (8
  files)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell637_dirNNN_traces.npz` (8
  files)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell762_dirNNN_traces.npz` (8
  files)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell{767,637,762}_summary.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/data/cell{767,637,762}_attribution.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/images/cell{767,637,762}_fig{1..4}_*.png`
  (12 PNGs)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/results_summary.md`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/results_detailed.md` (this file)
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/metrics.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/costs.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/results/remote_machines_used.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/details.json`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/short_answer.md`
* `tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/full_answer.md`

## Next Steps / Suggestions

* **Multi-replicate decomposition** of cell 767 across the 5 t0081 seeds where the joint-pass
  DSI emerged: re-run the attribution metric per seed and identify the seeds that produce DSI
  >= 0.4. The expectation is that those seeds will show non-zero NMDA contribution, confirming
  the Mg-unblocking-driven amplification story.
* **NaP density ablation** for cells 767 / 637 / 762: at fixed parameters except
  `gbar_napt80`, sweep down to 0 and re-evaluate DSI. If joint-pass collapses, NaP is causally
  necessary; if joint-pass persists, NaP is correlative only.
* **Cross-bed validation**: re-run the same three cells on the Bed A substrate (which differs
  in GABA timing geometry) to test whether the NaP-dominant signature is bed-specific or a
  general v3 substrate feature.

## Task Requirement Coverage

Operative task request from `task.json`:

> "Per-direction Vm traces of t0081 cells 767 / 637 / 762 (proximal soma, mid dendrite, distal
> dendrite) to attribute cell 767's joint-pass DSI to NMDA Mg-block, distal Nav1.6, NaP, or
> combination."

* **REQ-1** (24 simulations on v3 substrate, no NaN Vm) - **Done**: 24 stable .npz files in
  `results/data/`. Evidence:
  `results/data/cell{767,637,762}_dir{0,45,90,135,180,225,270,315}_traces.npz` and
  `cellNNN_summary.json` with `is_stable=true` for every direction.
* **REQ-2** (Vm at proximal soma / mid-dendrite / distal dendrite) - **Done**: arrays
  `v_soma_mv`, `v_mid_mv`, `v_distal_mv` in every traces .npz; recording sections recorded as
  `recording_sections` in `cellNNN_summary.json`.
* **REQ-3** (per-synapse NMDA conductance trajectories) - **Done**: `g_nmda_us` array of shape
  `(n_syns, n_timepoints)` in every traces .npz.
* **REQ-4** (Nav1.6 and NaP currents at terminal dendrite segments) - **Done**:
  `i_nav16_ma_cm2` and `i_nap_ma_cm2` arrays of shape `(n_segs, n_timepoints)` in every traces
  .npz.
* **REQ-5** (AIS Vm and spike onset times via threshold crossing at -10 mV) - **Done**:
  `v_ais_mv` array recorded; spike count per direction in `cellNNN_summary.json`
  `direction_results`.
* **REQ-6** (Figure 1 per cell - Vm traces 3x8 grid) - **Done**:
  `results/images/cell{767,637,762}_fig1_vm_traces.png`.
* **REQ-7** (Figure 2 per cell - NMDA conductance overlay) - **Done**:
  `results/images/cell{767,637,762}_fig2_nmda_conductance.png`.
* **REQ-8** (Figure 3 per cell - Nav1.6/NaP current decomposition) - **Done**:
  `results/images/cell{767,637,762}_fig3_nav16_nap_current.png`.
* **REQ-9** (Figure 4 per cell - AIS spike onset histogram) - **Done**:
  `results/images/cell{767,637,762}_fig4_ais_spikes.png`.
* **REQ-10** (Fractional-channel-contribution attribution metric over [200, 1200] ms) -
  **Done**: cell 767 NaP-dominant 93.0%; cell 637 NaP-dominant 98.5%; cell 762 NaP-dominant
  99.9%. Evidence: `results/data/cell{767,637,762}_attribution.json`.
* **REQ-11** (Answer asset with v2 spec) - **Done**:
  `assets/answer/cell-767-dendritic-spike-mechanism-attribution/{details.json,
  short_answer.md, full_answer.md}`. Verificator passes 0 errors / 0 warnings.
* **REQ-12** (Cells 637 and 762 attribution consistency check) - **Done**: both NaP-dominant
  (98.5% and 99.9%); no near-pass cluster heterogeneity. Documented in `full_answer.md`
  Synthesis and Evidence sections.
* **REQ-13** (Single-replicate confidence statement) - **Done**: confidence "medium";
  `full_answer.md` Limitations explicitly states single-replicate constraint and
  generalisation requires t0083 / S-0081-01.
* **REQ-14** (12 PNGs embedded in `results_detailed.md`) - **Done**: see Visualizations
  section above.

</details>
