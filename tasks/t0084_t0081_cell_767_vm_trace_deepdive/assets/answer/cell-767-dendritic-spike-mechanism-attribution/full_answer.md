---
spec_version: "2"
answer_id: "cell-767-dendritic-spike-mechanism-attribution"
answered_by_task: "t0084_t0081_cell_767_vm_trace_deepdive"
date_answered: "2026-05-05"
confidence: "medium"
---
# Cell 767 DSI Mechanism Attribution

## Question

Which biophysical mechanism - NMDA Mg-block, distal Nav1.6, NaP, or a combination - is responsible
for cell 767's joint-pass DSI improvement in the v3 Bed B substrate?

## Short Answer

Cell 767's PD/ND difference in integrated dendritic current is attributed primarily to **NaP
sustained depolarisation** (0.0% NMDA, 7.0% Nav1.6, 93.0% NaP) over the response window [200, 1200]
ms. Cells 637 and 762 share the same NaP-dominant signature (98.5% and 99.9%), suggesting NaP is a
systematic feature of the v3 Pareto near-pass cluster. The single-replicate deep-dive did not
reproduce cell 767's original 5-seed joint-pass DSI of 0.494 (re-evaluated DSI = 0.000), so the
attribution describes the parameter-set's biophysical signature rather than confirming a per-trial
joint-pass mechanism.

## Research Process

This answer was produced by t0084 through direct NEURON simulation with extended recording on the v3
Bed B substrate. Three cells from t0081's Pareto front (767: joint-pass; 637, 762: near-pass) were
re-evaluated across 8 stimulus directions (0deg-315deg, 45deg steps) with 1 replicate per direction
(seed = 1000). For each simulation, the following quantities were recorded and saved as .npz files:
Vm at proximal soma, mid-dendrite, and distal dendrite; total NMDA conductance (g, in uS) at all
Exp2NMDA synapses; Nav1.6 (nav16t80._ref_i, mA/cm2) and NaP (napt80._ref_i, mA/cm2) currents at the
representative terminal dendrite section; AIS Vm for spike onset counting.

The attribution metric integrates each channel's current (in nA) over the response window
[200, 1200] ms for the PD direction (0deg) and ND direction (180deg). The fractional contribution of
each channel is its |PD integral - ND integral| divided by the sum of all three |deltas|. The
dominant mechanism is the channel with the highest fractional contribution.

When the per-direction spike counts of this single-replicate run were aggregated, the measured DSI
for cell 767 was 0.000 (PD = ND = 2.86 Hz). This is in tension with t0081's 5-seed mean DSI of 0.494
for the same parameter vector, indicating that cell 767's joint-pass classification at t0081 was
supported by a subset of the seeds rather than every replicate. The attribution metric is therefore
reported as a parameter-set biophysical signature rather than as a per-replicate mechanism
explanation for joint-pass behaviour.

## Evidence from Papers

No new literature was reviewed for this task. The three candidate mechanisms are grounded in papers
already reviewed during t0081's research stage: NMDA Mg-block (Sivyer 2013, Branco-Hausser 2010),
distal Nav1.6 dendritic spikes (Oesch 2005), and NaP sustained depolarisation (Goldfinger 2000,
Stuart 1999).

## Evidence from Internet Sources

No internet sources were consulted for this answer. The mechanism-attribution question is fully
answerable from NEURON simulations of the v3 Bed B substrate re-evaluated locally for this task,
combined with the parameter vectors saved in t0081's `all_evaluations.json`. External documentation
or web sources would not provide additional decisive evidence about the specific PD/ND
integrated-current decomposition reported here.

## Evidence from Code or Experiments

**Cell 767 parameter values** (from t0081 all_evaluations.json, cell_index=767, gen 7):

* gnmda_dend = 6.7193e-03 uS (Exp2NMDA NetCon weight; near upper bound of log-uniform [1e-5, 1e-2])
* mg_conc_mm = 0.2607 mM (Mg block concentration)
* voff_nmda = 6.2804 mV (Mg block voltage offset)
* nav16_dend_distal = 1.4922e-02 S/cm2 (terminal dendrite Nav1.6; upper-mid range [1e-5, 0.05])
* nap_dend_distal = 9.2141e-05 S/cm2 (terminal dendrite NaP; near lower bound [1e-5, 0.01])

**Cell 767 attribution results** (integrated over [200, 1200] ms, PD=0deg vs ND=180deg):

* NMDA fractional contribution: **0.0%** (Delta = +0.0000e+00 nA*ms)
* Nav1.6 fractional contribution: **7.0%** (Delta = -8.31e-05 nA*ms)
* NaP fractional contribution: **93.0%** (Delta = -1.10e-03 nA*ms)
* **Dominant mechanism: NaP sustained depolarisation**

**Cell 637 attribution results** (gen 6 near-pass, DSI_orig = 0.337):

* NMDA: 0.0%, Nav1.6: 1.5%, NaP: **98.5%** (dominant)

**Cell 762 attribution results** (gen 7 near-pass, DSI_orig = 0.314):

* NMDA: 0.0%, Nav1.6: 0.1%, NaP: **99.9%** (dominant)

The NMDA contribution is computed from the current
`I_nmda(t) = sum(g_nmda(t)) * (v_distal(t) - 0.0)` integrated over the response window. Although
`gnmda_dend` is large in cell 767, the PD-ND difference of the integrated NMDA current is
essentially zero in this single-replicate run because the dendritic Vm trajectories at the recording
site are too similar between PD and ND directions to produce a measurable Mg-unblocking asymmetry.
Both Nav1.6 and NaP currents are negative (inward); the magnitudes of the PD-ND deltas are dominated
by NaP.

**Single-replicate measured DSI** (re-evaluation):

* Cell 767: PD_rate = 2.86 Hz, ND_rate = 2.86 Hz, DSI = 0.000 (vs. t0081 5-seed mean 0.494)
* Cell 637: PD_rate = 2.86 Hz, ND_rate = 2.14 Hz, DSI = 0.143 (vs. t0081 5-seed mean 0.337)
* Cell 762: PD_rate = 2.86 Hz, ND_rate = 2.86 Hz, DSI = 0.000 (vs. t0081 5-seed mean 0.314)

All 24 simulations (3 cells x 8 directions) completed stably with no NaN Vm values. 12 PNG figures
were generated (4 per cell) and saved to `results/images/`.

## Synthesis

The integrated dendritic current decomposition shows that the PD/ND asymmetry in cell 767 is carried
almost entirely by **NaP sustained depolarisation** (93%), with a smaller Nav1.6 contribution (7%)
and an essentially zero NMDA contribution. The same pattern is even more pronounced in cells 637 and
762 (NaP 98.5% and 99.9%, respectively), indicating that NaP-driven dendritic depolarisation is a
systematic biophysical feature of the v3 Pareto near-pass cluster on this substrate. NMDA Mg-block,
despite being the largest gain knob in the parameter ranges, did not produce a measurable PD/ND
asymmetry in the integrated current at the single recorded distal section.

This finding partially answers project research question Q4 (do active dendritic conductances
improve DSI?). The dominant active dendritic mechanism in these parameter sets is NaP, not NMDA
Mg-block or Nav1.6. However, the inferred mechanism does not by itself confirm joint-pass DSI: this
single-replicate run failed to reproduce cell 767's original 5-seed joint-pass DSI of 0.494. A
multi-replicate follow-up (S-0081-01 or t0083) is needed to test whether the NaP-dominant
attribution holds across the seeds that produce the joint-pass aggregate.

## Limitations

* **Single replicate per direction**: each of the 8 directions was run with seed = 1000.
  Seed-to-seed variability is not quantified. The cell 767 single-replicate DSI (0.000) does not
  reproduce the t0081 5-seed mean (0.494), indicating the joint-pass classification depends on seeds
  beyond this single replicate.
* **Single cell**: this attribution applies to cells 767, 637, 762 specifically. Generalisation to
  "all joint-pass cells in the v3 substrate" requires t0083's extended NSGA-II run to produce
  additional joint-pass cells, or S-0081-01's multi-replicate study.
* **Passive current decomposition**: the attribution metric measures integrated channel current, not
  counterfactual causal contribution. A knockout experiment (setting one channel's gbar to 0 and
  rerunning, comparing DSI change) would provide stronger causal evidence but was excluded from
  scope (it would violate the verbatim parameter constraint of this task).
* **Single terminal dendrite**: Nav1.6 and NaP currents are recorded from only the first terminal
  dendrite section (`cell.terminal_dends[0]`). The aggregate contribution across all terminal
  sections may differ from this representative section.
* **Medium confidence**: confidence is "medium" because the analysis is single-replicate and
  passive-current based rather than counterfactual. The NaP dominance is consistent with the PD-ND
  integrated-current signature but has not been causally confirmed.

## Sources

* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0081_bedb_v3_warmstart_nsga2`
