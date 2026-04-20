# Modify DSGC Port with Spatially-Asymmetric Inhibition for Channel Testbed

## Motivation

The project now has two ports of the Poleg-Polsky & Diamond 2016 ModelDB 189347 DSGC model, and
neither demonstrates direction selectivity through the biologically meaningful mechanism of
postsynaptic dendritic integration of asymmetric synaptic input. Task t0008 produced
`modeldb_189347_dsgc` with DSI 0.316 and peak 18.1 Hz using a spatial-rotation proxy driver that
rotates BIP synapse coordinates per angle. Task t0020 produced `modeldb_189347_dsgc_gabamod` with
DSI 0.7838 (inside the paper's envelope [0.70, 0.85]) and peak 14.85 Hz using the paper's native
gabaMOD parameter-swap protocol, which toggles a single global GABA scalar between PD (0.33) and ND
(0.99) conditions. Both are valid scientific reproductions, but neither produces DS via the cell's
own integration of spatio-temporally asymmetric inputs — a requirement for any downstream channel
experiment that asks "does this channel combination preserve the dendritic-computation mechanism?"
Literature priors from t0015 through t0019 provide concrete blueprints for on-the-path shunting
inhibition, AIS channel split (Nav1.6/Nav1.2 at ~7x somatic density), and E-I temporal co-tuning.
This task consolidates those priors into a channel-testbed model.

## Scope

Produce a new sibling library asset (proposed slug `modeldb_189347_dsgc_dendritic`) derived from
`modeldb_189347_dsgc`. The asset shares MOD files (HHst.mod, spike.mod) and the RGCmodel.hoc
skeleton with the two prior ports but replaces the rotation and gabaMOD drivers with a
dendritic-computation driver based on spatially-asymmetric inhibition. The driver sweeps a moving
bar across the cell in 12 directions (30 degree spacing) at a fixed biological velocity; direction
selectivity arises because inhibitory synapses are positioned or timed so that bars moving in the
null direction see inhibition arriving before excitation on any given dendrite (shunting veto) while
bars moving in the preferred direction see excitation arriving first (pass-through). The AIS/soma/
dendrite compartments are organized into explicit `forsec` channel-insertion blocks so follow-up
tasks can add, remove, or replace channels without editing the driver.

## Requirements

1. **Dendritic-computation DS**: stimulus is a moving bar in 12 directions (0, 30, ..., 330); no
   per-condition gabaMOD swaps or per-angle BIP coordinate rotation. DS arises from
   spatially-asymmetric inhibition (Koch-Poggio-Torre / Barlow-Levick on-the-path shunting).
2. **12-angle coverage**: `tuning_curves.csv` with columns
   `(angle_deg, trial_seed, firing_rate_hz)`, at least 10 trials per angle, >=120 rows total.
3. **Dendritic-computation only**: a single fixed mechanism set across all 12 angles; only the
   stimulus direction changes. No parameter swaps, no driver tricks.
4. **Spike output**: somatic spikes detectable at least in the preferred direction. Peak firing rate
   >=10 Hz target; DSI >=0.5 acceptable (hitting the paper's [40, 80] Hz peak envelope is not
   required).
5. **Channel-modular AIS**: AIS, soma, and dendrite regions in separate `forsec` blocks with
   explicit channel-insertion points. `description.md` documents how to add/remove channels and how
   to swap the spike.mod channel set.
6. **Metrics**: use t0012's `tuning_curve_loss` scorer to compute DSI, HWHM, peak firing rate, and
   per-angle reliability. Produce `score_report.json`.
7. **Comparison**: `results_detailed.md` includes a comparison table vs t0008 (rotation proxy: DSI
   0.316, peak 18.1 Hz) and t0020 (gabaMOD swap: DSI 0.7838, peak 14.85 Hz) covering DSI, peak,
   HWHM, and reliability.

## Deliverables

* New library asset `modeldb_189347_dsgc_dendritic` (sibling to the two existing ports) with
  spatially-asymmetric-inhibition driver, channel-modular AIS, and documentation in
  `description.md`.
* `tuning_curves.csv` with 12 angles x >=10 trials = >=120 rows.
* `score_report.json` from the t0012 scorer with DSI, HWHM, peak, per-angle reliability.
* Comparison note in `results_detailed.md` quantifying differences vs t0008 and t0020.
* Channel-modularity documentation inside the new library asset's `description.md` explaining how to
  add, remove, or replace channels in each compartment without touching the driver.

## Dependencies

* `t0008_port_modeldb_189347` — source HOC/MOD files and library-asset skeleton to fork.
* `t0012_tuning_curve_scoring_loss_library` — DSI / HWHM / reliability scorer.
* `t0015_literature_survey_cable_theory` — cable-theory priors constraining dendritic geometry and
  space constants.
* `t0016_literature_survey_dendritic_computation` — on-the-path shunting prior that motivates the
  spatially-asymmetric inhibition mechanism.
* `t0017_literature_survey_patch_clamp` — AIS channel-density priors (Nav1.6/Nav1.2 ~7x somatic).
* `t0018_literature_survey_synaptic_integration` — E-I temporal co-tuning priors for driver
  design.
* `t0019_literature_survey_voltage_gated_channels` — Kv1/Kv3 AIS placement priors for the channel-
  modular AIS layout.

## Out of Scope

* No remote GPU compute — runs on the local Windows workstation.
* No channel-swap experiments in this task. This task delivers the testbed; follow-up tasks will use
  it to evaluate specific channel combinations (Nav1.6-only, Nav1.2-only, +Ih, Kv1 vs Kv3).
* No attempt to match the paper's peak firing envelope [40, 80] Hz — closing the peak gap is a
  separate investigation.
* No modifications to t0008 or t0020 assets; both ports remain intact for comparison.
