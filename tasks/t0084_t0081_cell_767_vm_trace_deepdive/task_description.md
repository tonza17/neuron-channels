# Vm-Trace Deep-Dive of t0081 Cell 767 to Attribute the Joint-Pass DSI Mechanism

## Motivation

t0081 (`bedb_v3_warmstart_nsga2`) delivered the project's first joint-pass cell: **gen 7 cell 767 at
DSI 0.494 / PD 11.39 Hz** on the v3 dendritic- spike-augmented Bed B substrate. This is a major
architectural milestone -- the first single-cell substrate in the project lineage to satisfy
`DSI >= 0.4 AND PD >= 10 Hz` simultaneously. However, the **biophysical mechanism for the DSI
improvement is unattributed**: cell 767's parameter vector contains non-zero values for all five
dendritic-spike machinery dimensions added in t0080 (`gnmda_dend`, `mg_conc_mm`, `voff_nmda`,
`nav16_dend_distal`, `nap_dend_distal`), and the joint-pass result could plausibly arise from any
one of three mechanisms or a combination:

1. **NMDA Mg-block recruitment.** Active dendritic NMDA receptors with Mg-block produce
   voltage-dependent multiplicative gain that supercharges ND-suppressed but PD-active synaptic
   input. This is the Sivyer 2013 / Branco-Hausser 2010 mechanism.
2. **Distal Nav1.6 dendritic spikes.** Backpropagating APs and locally initiated dendritic spikes
   from distal Nav1.6 produce non-linear amplification of PD-correlated input. This is the Oesch
   2005 mechanism.
3. **NaP sustained depolarisation.** Persistent Na current at distal dendrites produces a sustained
   depolarising plateau that enhances PD firing without proportionally enhancing ND firing (assuming
   GABA asymmetry suppresses ND-direction NaP recruitment). This is the Goldfinger 2000 / Stuart
   1999 mechanism.

Without per-direction Vm traces and per-channel current-flow analysis, we cannot distinguish which
mechanism (or combination) drives cell 767's DSI improvement. The attribution matters strategically:
it determines which mechanism to optimise first if t0083's extension finds additional joint- pass
cells, and which to test on Bed A in S-0081-05's cross-bed validation.

This task addresses project research question **Q4** (do active dendritic voltage-gated conductances
improve, degrade, or have no effect on the match to the target angle-frequency curve compared with
passive dendrites?) by mechanistically dissecting the first cell in the project to deliver a
positive answer to Q4 in joint form. Source suggestion: **S-0081-03**.

## Scope

### In scope

* Re-evaluate three cells from t0081's Pareto front in subprocess (eval-mode, no NSGA-II loop) on
  the v3 substrate (`de_rosenroll_2026_dsgc_ais_dendritic_spike`):
  * Cell 767 (joint-pass; DSI 0.494 / PD 11.39 Hz; gen 7).
  * Cell 637 (near-pass; distance 0.063; gen 6).
  * Cell 762 (near-pass; distance 0.086; gen 7).
* For each cell and each of 8 stimulus directions (0, 45, 90, 135, 180, 225, 270, 315 deg), record:
  * Vm at proximal soma.
  * Vm at one mid-dendrite section.
  * Vm at one distal-dendrite section (the same one that carries nav16_dend_distal and
    nap_dend_distal channel insertions).
  * Per-segment NMDA conductance trajectories (`gnmda` over time) at the distal dendrite synapses
    recruited during the simulation window.
  * Per-segment Nav1.6 and NaP currents at the distal dendrite (`ina` decomposed by mechanism).
  * Per-direction AIS spike onset times (zero-crossing of Vm at the AIS threshold trigger).
* Generate four figure assets per cell (12 figures total):
  1. **Per-direction Vm traces** at proximal soma, mid dendrite, distal dendrite (3-row stacked,
     8-column grid).
  2. **NMDA conductance trajectories** at distal dendrite per direction (8-line plot).
  3. **Nav1.6 / NaP current decomposition** at distal dendrite per direction (8-direction stacked
     plot).
  4. **AIS spike onset histogram** per direction (polar plot or 8-bin bar chart).
* Identify, per cell, which mechanism dominates the DSI difference between PD (gen direction with
  peak rate) and ND (gen direction with minimum rate). Use a quantitative attribution metric: the
  **fractional contribution of each channel to the integrated dendritic depolarisation during the PD
  response window minus the same during the ND response window**.
* Produce one **answer asset** at `assets/answer/cell-767-dendritic-spike-mechanism-attribution/`
  with short and full answer documents per the answer-asset specification, attributing cell 767's
  DSI mechanism to one (or a combination) of the three candidates.

### Out of scope

* Re-running NSGA-II or any optimisation (use cell 767/637/762 parameters verbatim).
* Modifying the substrate library asset.
* Bed A cross-bed comparisons (S-0081-05).
* Statistical multi-replicate confirmation across seeds (S-0081-01).
* Comparing alternative dendritic mechanisms (Ca2+ plateau, Ih, HCN) -- scope limited to the three
  machinery components present in the v3 substrate.

## Pass Criteria

* All 24 simulations (3 cells * 8 directions) complete with stable Vm traces (no numerical
  instabilities, no NaN values).
* All 12 figures generated and embedded in `results/results_detailed.md`.
* The answer asset clearly identifies the dominant mechanism (or combination, with relative weights)
  for cell 767's DSI improvement.
* The mechanism attribution for cells 637 and 762 (near-pass neighbours) is consistent with cell
  767's attribution -- if not, the discrepancy is documented as a "near-pass cluster heterogeneity"
  finding.

## Estimated Compute Cost

* Local CPU only. No remote machine.
* Per-cell wall-clock: 8 directions * ~30-45 s/direction = ~3-6 min, plus per-segment recording
  overhead = ~5-10 min per cell.
* Total runtime: ~15-30 min for 3 cells.
* **Compute cost: $0**.

## Dependencies

* **t0081_bedb_v3_warmstart_nsga2**: provides cell 767, 637, 762 parameter vectors (54-d
  natural-unit vectors from `results/data/all_evaluations.json`), the v3 substrate evaluation
  harness (`evaluate_cell.py` or equivalent), and the recording infrastructure for per-segment Vm /
  conductance / current trajectories.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset and its channel-insertion API (Nav1.6,
  NaP, NMDA Mg-block per dendritic section).

## Recommended Task Types

* `experiment-run` -- 24 single-cell NEURON simulations with extended recording.
* `data-analysis` -- per-channel current decomposition and figure generation.
* `answer-question` -- mechanism-attribution answer asset.

## Notes

The recording infrastructure for per-segment Vm, NMDA conductance, and Nav1.6 / NaP currents must be
added to or wrapped around t0081's eval harness. The harness currently records spike counts per
direction; this task adds full Vm traces and per-mechanism current decomposition. Keep the recording
additive -- the eval harness must remain backwards-compatible with t0081's NSGA-II loop in case
t0083 needs to re-use it.

The answer asset's confidence level should reflect the single-cell-replicate nature of the analysis:
cell 767's mechanism is attributed for that specific cell, but generalisation to "all joint-pass
cells in the v3 substrate" requires t0083's additional joint-pass cells (or S-0081-01's
multi-replicate study). The answer asset should state this explicitly in its `## Limitations`
section.
