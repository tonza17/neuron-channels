# rd1-like Na/K Remodelling of the DSGC Model and Its Effect on Direction Selectivity

## Motivation

The researcher's preliminary data (`SomeResults.pdf`, repository root, panels A-D) show that FVB/N
rd1 retinal ganglion cells differ from mature wild-type (WT) cells in four ways: elevated
spontaneous activity, weaker evoked spiking, a smaller voltage-gated Na current and a larger
sustained K current. This task tests whether remodelling the soma and AIS conductances of the
existing DSGC model reproduces that phenotype, and what the remodelling does to direction
selectivity (project Research Questions 1 and 4). It also tests the researcher's much simpler toy
model of input-output distortion (panel D) against the compartmental model.

## Calibration Targets (read by eye from the figure, approximate)

| Panel | WT | rd1 |
| --- | --- | --- |
| A: spontaneous, 2 s | Near silent | About 14 spikes in 2 s (~7 Hz), irregular or bursty, ~60 mV tall |
| B: +60 pA step, 500 ms | About 4 adapting spikes (~8 Hz), peaks ~90, 70, 65 mV | Almost no spiking, small blips at onset |
| C: +100 mV voltage step | Sustained outward ~2 nA, early inward Na transient | Sustained outward ~3.5 nA (~1.7x), much smaller inward transient |

If the researcher supplies exact traces, replace these numbers and record the change in
`results_detailed.md`.

## Scope

All runs are local NEURON simulations. No remote machines, cost $0.

* **Reference cells**: 5-10 LEGIT high-DSI cells drawn with a fixed seed from the t0121 pooled
  parquet (dependency `t0121_5seed_substrate_rate_canonical_report`). List the chosen cell IDs.
* **Evaluator**: reuse the signed antipodal DSI evaluator and `cell_params.jsonl` per-cell parameter
  dump from `t0129_t0126_signed_dsi_real_rates_1seed`.
* **Conditions**: WT-like (scale 1.0 on gNa and gK) and rd1-like (scaling from Part 1) for every
  reference cell.

## Part 1: Voltage-Clamp Calibration (panel C)

1. Replicate the +100 mV voltage step at the soma on each reference cell.
2. Sweep soma plus AIS gNa scale (0.25-1.0x) against gK scale (1-3x) on a grid of at least 6 x 6.
3. Choose the rd1-like scaling that matches the sustained-current ratio (~1.7x) and the reduced
   inward transient. Set the scaling from clamp data only; do not use any firing data.
4. Report the fitted scalings per cell and their spread across cells.

## Part 2: Current-Clamp Prediction (panels A and B)

1. With the Part 1 scalings, run the +60 pA, 500 ms step for WT-like and rd1-like cells. This is an
   out-of-sample test: report whether evoked firing collapses as in panel B.
2. For panel A, add a weak tonic bias current or noise at rest (exploratory; any form that works is
   acceptable, but state exactly what was used and how it was tuned). Check whether rd1-like cells
   fire irregularly at ~7 Hz while WT-like cells stay near silent.
3. Report f-I curves, spike amplitude, adaptation index and spontaneous rate for both conditions.
4. If soma and AIS scaling alone does not reproduce the phenotype, add a second arm that also scales
   dendritic channels and rerun Parts 1-2 for that arm.

## Part 3: Direction Selectivity

1. Run the standard protocol for WT-like and rd1-like cells: HH on, 8 directions, fixed 1400 ms
   trials. Use the EPSP_PASSIVE / IPSP_PASSIVE / FULL mode trio only where the existing protocol
   calls for it.
2. Report signed antipodal DSI = (PD - ND) / (PD + ND), PD rate and ND rate per cell and condition,
   with and without the tonic bias from Part 2.
3. Produce a DSI-versus-scaling heatmap over the Part 1 gNa x gK grid.

## Part 4: Reproduce or Refute Panel D

Panel D is a toy model by the researcher. The same input (three Gaussian pulses at about 180, 430
and 680 ms over 1000 ms) drives a WT-like and an rd1-like cell. Its predictions are:

* WT output grows gradually with input strength (0-100, reaching ~15); rd1 output is flat and
  saturated (~23) at all but the lowest strengths.
* WT output is cleaner and stimulus-locked; rd1 output has an elevated baseline (~0.35), broader and
  less distinct peaks.

Steps:

1. Build the simple toy model (a rate or threshold-type model with WT-like and rd1-like parameters)
   matching this description and check that it reproduces panel D. If it cannot be reproduced from
   the description, state that and list what is missing.
2. Test both predictions in the NEURON model: sweep PD synaptic drive strength and compare the
   WT-like and rd1-like output curves; drive both with the three-pulse input and compare baseline,
   stimulus-locking and peak distinctness.
3. State for each prediction whether it is reproduced, partly reproduced or disproved.

## Key Questions

1. Does Part 1 yield rd1-like scalings that reproduce the panel C current ratio on all reference
   cells?
2. Do those scalings, with no firing data in the fit, collapse evoked firing at +60 pA?
3. Can a tonic bias give ~7 Hz irregular spontaneous firing in rd1-like but not WT-like cells?
4. Does rd1-like remodelling raise, lower or leave unchanged signed DSI, and does the answer depend
   on the tonic bias?
5. Does the compartmental model reproduce the panel D saturation and temporal-smearing predictions?

## Expected Outputs

* Charts in `results/images/`, each embedded in `results_detailed.md`:
  * Panel C replication: voltage-clamp current traces, WT-like vs rd1-like (time vs nA).
  * gNa x gK calibration grid: sustained-current ratio and transient amplitude.
  * Current-clamp traces at +60 pA and at rest, WT-like vs rd1-like, and f-I curves.
  * Signed DSI, PD rate and ND rate by condition, plus the DSI-versus-scaling heatmap.
  * Panel D: toy-model reproduction, and NEURON input-strength sweep and three-pulse responses.
* One answer asset covering questions 1-5 with the evidence for each.
* Per-cell parameter dump and results tables in `data/`.
* Registered metric: `direction_selectivity_index` (signed), reported per condition as variants.

## Dependencies

* `t0121_5seed_substrate_rate_canonical_report`: pooled LEGIT cell parquet used as the reference
  cell source.
* `t0129_t0126_signed_dsi_real_rates_1seed`: signed DSI evaluator and per-cell parameter-dump
  protocol.

## Compute and Budget

Local CPU only, no Vast.ai, no paid APIs. Estimated cost $0. Estimated wall-clock: a few hours for
the clamp grid and DSI runs on 5-10 cells.

## Risks

* Panel values are read by eye; calibration targets are approximate.
* A single-cell model has no presynaptic network, so network-driven rd1 hyperactivity can only be
  represented by an ad hoc bias.
* Soma and AIS scaling may not be enough; the dendritic arm is the planned fallback.
