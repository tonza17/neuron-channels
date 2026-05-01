# Add virtual AIS to deposited DSGC and re-run t0067 channel sweep on AIS

## Motivation

t0067 inserted 5 voltage-gated channels (Nav1.6, NaP, NaR, Kv3, Kv4) on the deposited Poleg-Polsky
DSGC soma. Three of the five (NaR, Kv3, Kv4) had essentially no effect on firing rate or DSI at any
density. The strongest plausible explanation: these channels are normally AIS-localised in real RGCs
(per t0019 priors), and putting them on the soma puts them in a compartment where the existing
massive HHst Na (~400 mS/cm²) drowns out their contribution plus the soma's electrotonic geometry
doesn't favour AP-shape modulation. t0019 documents distal-AIS Nav densities of 2500-5000 pS/μm²
(~25-50 mS/cm²) — the AIS is a much smaller compartment with much higher input resistance per
area.

This task tests S-0067-03: append a virtual AIS + axon cable to the deposited cell, then re-run the
t0067 channel-density sweep with the 5 channels inserted on the **AIS** instead of the soma.
Hypothesis: the AIS-localised channels show substantially larger effects on firing rate and DSI than
the soma-localised versions, because the AIS is a high-input-resistance spike-initiation zone.

## Scope

* Cell: deposited Poleg-Polsky 2016 DSGC (t0008) PLUS a new virtual AIS section (30 μm × 1 μm, 5
  segments) PLUS a passive axon cable (1000 μm × 1 μm, 50 segments). AIS connects to soma(1);
  axon connects to AIS(1).
* AIS active conductances: HHst at biologically-realistic AIS density — `gnabar = 30 mS/cm²`,
  `gkbar = 20 mS/cm²`, `gkmbar = 3 mS/cm²` (per t0019 priors).
* Axon active conductances: HHst at low density — `gnabar = 5 mS/cm²`, `gkbar = 3 mS/cm²` —
  sufficient for AP propagation, low enough to not affect somatic firing significantly.
* Mode: only `FULL` (HH on, all synapses at canonical defaults).
* Direction: PD (`gabaMOD = 0.33`) and ND (`gabaMOD = 0.99`).
* Seeds per condition: 5.
* Channels on AIS (one per experiment, 3 densities each): same as t0067.

## Conditions

16 conditions × 2 directions × 5 seeds = **160 FULL trials**.

| condition_id | channel | density (mS/cm²) | Notes |
| --- | --- | --- | --- |
| baseline_ais | (none) | — | AIS+axon attached, no extra channels — t0069 reference |
| nav16_low_ais | Nav1.6 | 10 | t0067-equivalent on AIS |
| nav16_med_ais | Nav1.6 | 30 |  |
| nav16_high_ais | Nav1.6 | 90 |  |
| nap_low_ais | NaP | 0.3 |  |
| nap_med_ais | NaP | 0.8 |  |
| nap_high_ais | NaP | 2.4 |  |
| nar_low_ais | NaR | 3 |  |
| nar_med_ais | NaR | 8 |  |
| nar_high_ais | NaR | 24 |  |
| kv3_low_ais | Kv3 | 7 |  |
| kv3_med_ais | Kv3 | 20 |  |
| kv3_high_ais | Kv3 | 60 |  |
| kv4_low_ais | Kv4 | 4 |  |
| kv4_med_ais | Kv4 | 12 |  |
| kv4_high_ais | Kv4 | 36 |  |

Densities match t0067's exactly so we can directly compare effect sizes between soma and AIS
insertion.

## Approach

1. Build the cell via t0008's `build_dsgc()` unchanged.
2. After build, add 2 new sections from Python:
   * `ais` section, 30 μm × 1 μm, 5 segments, HHst inserted with realistic AIS densities.
   * `axon` section, 1000 μm × 1 μm, 50 segments, HHst inserted at lower density.
3. Connect: `ais.connect(soma, 1, 0)`, then `axon.connect(ais, 1, 0)`.
4. Insert the 5 t0067 mechanisms on the AIS at gbar=0; per-trial set the active channel's gbar to
   the target density.
5. Run 160 trials using the t0067 driver template adapted for AIS-localised insertion.
6. Compute DSI per condition; compare to t0067 anchors (soma-localised counterparts).

## Outputs

* `data/per_trial_metrics.json` — 160 trial records.
* `data/dsi_by_condition.json` — 16 conditions.
* `results/metrics.json` — registered DSI for the t0069 baseline.
* `results/images/firing_rate_vs_density.png` — 5 panels (per channel), PD/ND firing rate with
  t0069-baseline reference.
* `results/images/dsi_vs_density.png` — 5 panels (per channel), DSI vs density with t0069-baseline
  reference.
* `results/images/soma_vs_ais_comparison.png` — for each channel, side-by-side bar chart of DSI
  change at low/med/high (soma from t0067 vs AIS from t0069).
* `results/results_summary.md`, `results/results_detailed.md` (spec_version 2).

## Failure-mode policy

Same as t0067/t0068: peak Vm > +60 mV or < -80 mV → flag `is_unstable = true`. Trial data still
saved.

## Key Questions

1. Does the t0069 baseline (AIS+axon attached, no extra channels) reproduce the t0067 baseline
   firing rate and DSI? If yes: AIS topology change is benign. If no: the AIS itself reshapes the
   cell's behaviour and we need to account for that before comparing channel effects.
2. For each of the 5 channels: is the |Δ DSI| at AIS substantially larger than at soma?
   Rule-of-thumb: ≥2× larger.
3. Do the 3 channels that were inert in t0067 (NaR, Kv3, Kv4) become active when relocated to the
   AIS?
4. Does Nav1.6 still erode DSI on the AIS, or does the smaller compartment change the directionality
   of the effect?
5. Does NaP still invert DSI on the AIS, or does the more isolated compartment change the sign?

## Compute and Budget

* Local Windows workstation. ~3 s/trial × 160 = ~10 min (same as t0067).
* External costs: $0.

## Time Estimation

* Implementation (cell-extension code, AIS construction, port channel-set logic): 1 hour.
* Sweep: 10 min.
* Plotting + reporting: 1 hour (3 plots + cross-task comparison).
* Verification + PR: 30 min.
* Total: ~3 hours.

## Dependencies

* `t0008_port_modeldb_189347` — cell builder.
* `t0019_literature_survey_voltage_gated_channels` — AIS Nav/Kv density priors.
* `t0065_t0020_epsp_ipsp_vm_protocol` — gabaMOD-swap protocol.
* `t0067_t0065_soma_channel_addition_sweep` — MOD files (vendored verbatim), trial driver
  template, soma-anchor DSIs for cross-comparison.

## Risks and Fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Adding HHst-bearing AIS changes the cell's spike-initiation site, making the t0069 baseline very different from t0067 baseline. | t0069 baseline DSI < 0.5 or > 1.0; or PD spike count < 5 or > 30. | This IS expected — biologically correct cells initiate at AIS. Document the new baseline; comparisons are done relative to t0069 baseline, not t0067 baseline, for fair within-task contrast. The cross-task soma-vs-AIS comparison is then "channel effect on top of each task's own baseline." |
| 2 | Axon HHst at low density doesn't propagate APs, causing reflection at AIS-axon junction. | Axon Vm shows damped APs (<+10 mV peak). | Increase axon `gnabar` to 10 mS/cm². |
| 3 | t0067 MOD files are still incompatible after mechanism re-insertion on AIS. | nrnivmodl error or runtime AttributeError. | Reuse t0068's recipe (which worked); only the section target changes. |

## Verification Criteria

* All 160 trials complete without instability.
* `data/per_trial_metrics.json` has 160 entries.
* `data/dsi_by_condition.json` has 16 entries.
* All 3 PNG plots exist and embedded in `results_detailed.md`.
* All standard verificators pass.
