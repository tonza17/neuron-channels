---
spec_version: "2"
answer_id: "does-rd1-like-na-k-remodelling-of-the-dsgc-model-reproduce-the-rd1-phenotype-and-change-dsi"
answered_by_task: "t0131_rd1_na_k_remodelling_dsgc_dsi"
date_answered: "2026-10-27"
confidence: "medium"
---
# Does rd1-like Na/K remodelling of the DSGC model reproduce the rd1 phenotype and change DSI?

## Question

Does rd1-like remodelling of soma and AIS Na and K conductances in the Bed B DSGC model reproduce
the researcher's rd1 phenotype (panels A to C), and what does it do to signed direction selectivity
and to the panel D toy-model predictions?

## Short Answer

No, only the clamp-current ratio is reproduced: the sustained-current ratio reaches 1.63 to 1.70 on
all 8 reference cells, but only at the grid edges (s_Na 0.25, s_K 2.36 to 3.0), and the Na transient
falls to 0.40 to 0.57 of WT-like instead of 0.25. The WT-like reference cells fire spontaneously at
a median of 73.5 Hz without any input, so panels A and B cannot be tested as intended. The rd1-like
cells are silent in every current-clamp, bias and synaptic protocol (dendritic arm included), signed
DSI is therefore undefined for rd1-like cells, and all four panel D predictions are disproved in the
NEURON model, whereas the toy model matches its by-eye anchors by construction. This rests on local
NEURON experiments on 8 LEGIT cells (exploratory, with by-eye targets).

Per Key Question: Q1 partly; Q2 no (the test is uninformative about evoked firing); Q3 no; Q4 cannot
be determined for rd1-like cells (undefined), no dependence on bias could be shown; Q5 no for the
compartmental model (the toy model reproduces its own anchors).

## Research Process

Calibration targets were read by eye from `research/inputs/SomeResults.pdf` (panels A to D). Eight
reference cells were drawn with a fixed seed (131) from the t0121 pooled LEGIT table (675 cells
rebuilt from the four source evaluation dumps and checked against the t0121 parquet). Because the
LEGIT status of earlier tasks used a process-randomised synapse placement, every candidate was
re-evaluated with a deterministic placement (WT-like, 0 and 180 degrees, one seed) and accepted only
if its PD rate was within 25 percent of the recorded rate and its signed antipodal DSI exceeded 0.3:
28 candidates were screened and 6 rejected. The cells are `t0114_seed7755_0256`,
`t0114_seed7755_0114`, `t0114_seed7755_0349`, `t0106_seed44_0093`, `t0106_seed44_0074`,
`t0115_seed9354_0032`, `t0115_seed9354_0060` and `t0112_seed77_0002`.

Part 1 fitted (s_Na, s_K) from voltage-clamp data only (a structural unit test checks that the
calibration module reads no firing quantity). Part 2 ran the pre-declared +60 pA, 500 ms step (out
of sample), f-I curves and a spontaneous-activity and tonic-bias search tuned on rd1-like cells
only. Part 3 ran the signed antipodal DSI protocol (8 directions, 1400 ms, 3 seeds). Part 4 fitted a
toy model and tested the predictions in NEURON. The pre-declared trigger for the dendritic arm fired
(the bias phenotype was not obtained), so Parts 1 to 3 were rerun for the soma+AIS+dendrite arm (DSI
on 5 cells).

## Evidence from Papers

Papers were used for context and for design choices only; no number in this answer comes from them.
[Werginz2024][werginz2024] and [Goethals2020][goethals2020] motivated scaling the AIS (Na density
many times the soma value) and interpreting a somatic clamp transient as space-clamp limited.
[MargolisDetwiler2007][margolisdetwiler2007] motivated treating a tonic bias as a surrogate for
network-driven activity. [Dhingra2004][dhingra2004], [Oesch2005][oesch2005] and
[Schachter2010][schachter2010] describe the spike-generator nonlinearity and the relation between
PSP and spike DSI. No rd1 or rd10 Na/K remodelling data exist in the project paper corpus apart from
rd10 alpha RGCs where the spike generator is largely preserved.

## Evidence from Internet Sources

The `internet` method was not used.

## Evidence from Code or Experiments

All numbers come from files written by `tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/code/` and
collected in `results/data_summary.json`.

**Q1, clamp (Part 1).** WT-like sustained outward current at +35 mV (step of +100 mV from -65 mV)
has median **482.6 nA** (range 347.0 to 680.1 nA) against about 2 nA in panel C, so the absolute
scale differs by roughly two orders of magnitude. The K current activates within 0.1 ms and hides
the Na transient in the total current, so the transient was measured from the isolated soma+AIS Na
channel current (WT-like median **-14.7 nA**, range -16.7 to -11.0 nA). The sustained ratio does not
depend on s_Na and rises with s_K in steps (1.14 at 1.4, 1.28 at 1.8, 1.42 at 2.2, about 1.56 at
2.6, about 1.70 at 3.0). The fits sit on the grid boundary: s_Na is **0.25** (the lower edge) for
all 8 cells and s_K ranges from **2.36 to 3.0** (mean 2.83). Achieved sustained ratio: mean
**1.674** (1.631 to 1.698), all 8 within 0.15 of 1.7. Achieved Na transient ratio: mean **0.455**
(0.399 to 0.573), not the 0.25 target. A plausible cause is the unscaled persistent and resurgent Na
channels, but this was not tested. An absolute step to +40 mV on 2 cells gave sustained currents of
468.6 and 479.1 nA, similar to the delta step.

**Q2, current clamp (Part 2).** WT-like cells fire at rest: mean **40.75** spikes in 500 ms at 0 pA
(7 of 8 cells firing) and **40.88** at +60 pA, so +60 pA changes nothing. WT-like spike peak is
about **-4.4 mV** and FWHM **0.58 ms**, unlike the roughly 90 mV peaks in panel B. rd1-like cells
have zero spikes at -10 mV threshold at every amplitude from 0 to 10,000 pA. The pre-declared
collapse criterion gives 7 collapsed and 1 uninformative cell (`t0114_seed7755_0114` is silent in
WT-like too). This verdict does not show a collapse of evoked firing: the WT-like count is identical
at 0 and 60 pA, so what disappears is spontaneous firing. A post-hoc threshold check at -30 mV (not
pre-declared) finds 113 events for rd1-like and 327 for WT-like summed over cells at +60 pA, because
two rd1-like cells (`t0106_seed44_0093`, `t0106_seed44_0074`) show attenuated spikes peaking between
about -29 and -22 mV, so the -10 mV count understates rd1-like activity. rd1-like cells rest at a
mean of -55.5 mV versus -62.4 mV for WT-like.

**Q3, spontaneous firing.** Without bias, WT-like mean rate is **78.5 Hz** (ISI CV 0.058, very
regular) and rd1-like is **0 Hz**, the opposite of panel A. The tuning grid (312 rows over
pre-declared 0 to 50 pA DC with 0 to 10 pA noise, plus an extended exploratory grid up to 6400 pA
and 1600 pA noise) never gave a rd1-like mean rate above 0 Hz at the -10 mV threshold. The fallback
combination (6400 pA DC, no noise) gave WT-like 15.6 Hz and rd1-like 0 Hz.

**Q4, DSI (Part 3).** WT-like median signed DSI is **0.874** (mean 0.793, 8 of 8 defined), median PD
rate 86.7 Hz, ND rate 3.1 Hz. For rd1-like, PD and ND spike counts are both 0 on every cell, so DSI
is `None` (8 of 8 undefined), with and without bias. Paired PD-rate change rd1-like minus WT-like:
median **-86.7 Hz** (Wilcoxon p = 0.0078, n = 8, bootstrap 95 percent CI -108.6 to -45.5 Hz). With
the 6400 pA bias, WT-like DSI is 0.0 on 7 of 8 cells from 3 PD and 3 ND spikes (one onset spike per
seed), which is an artefact rather than tuning. The 8-direction tuning shows that WT-like cells are
pacemakers suppressed only near 180 and 225 degrees (144 to 151 spikes per trial at the other
directions on the first cell), and scaling the excitatory weights from 0 to 100 percent leaves the
WT-like PD rate flat (Part 4), so the DSI is consistent with direction-dependent inhibition cutting
an intrinsic pacemaker rather than excitation-driven tuning. The DSI-versus-scaling heatmap (36 grid
points, 5 cells, 2 directions, 2 seeds) has median PD rate of 0 to 1 Hz everywhere except (s_Na,
s_K) = (1, 1), and DSI is undefined for most cells away from (1, 1); 17 of 36 grid points have no
defined DSI. The dendritic arm gave the same outcome: rd1-like DSI undefined on 5 of 5 cells,
although some rd1-like cells fire spontaneously at rest in that arm (mean 5.4 Hz over runs, median
0, maximum 43 Hz, regular).

**Q5, panel D.** The toy model (Naka-Rushton plus leaky integrator) matches all 11 by-eye anchors
within 20 percent, as it was fitted to them. Its rd1-like peaks are broader (FWHM 126.7 ms versus
64.5 ms) because of saturation, while the fitted rd1-like time constant (9.1 ms) is shorter than the
WT-like one (16.6 ms). In NEURON (3 cells, 3 seeds; u = 100 reproduced the Part 3 spike counts
exactly in 9 of 9 trials) the WT-like PD rate is flat in synaptic strength (83.5 Hz at u = 0, 87.5
Hz at u = 100, saturation index 1.0) and rd1-like output is 0 Hz everywhere. All four predictions
(flat saturated rd1 output, gradual WT growth, elevated rd1 baseline, temporal smearing) are
therefore **disproved**, with and without bias. The three-pulse WT-like PSTH is dominated by the
spontaneous rate and a start-up transient (distinctness 0.15 and locking r = 0.12 on the first
cell).

## Synthesis

The clamp calibration works only partly and needs the extreme corner of the pre-declared grid. The
deeper problem is that the reference cells are intrinsic pacemakers whose excitatory synaptic input
is nearly irrelevant, so the model WT-like cell is not the researcher's near-silent WT cell and the
out-of-sample comparison cannot test evoked firing. Reducing Na by 4 times and raising K by up to 3
times silences the cell completely, which removes spontaneous firing instead of producing it, so
panels A and B (hyperactive rd1, collapsed evoked firing) are not reproduced and the direction of
the rd1 effect on spontaneous firing is opposite to the data. DSI of rd1-like cells cannot be
quantified because there are no spikes; the only defensible statement is that this remodelling
abolishes firing in all conditions tested. Panel D's model-level predictions are not supported by
the compartmental model for the same reason.

## Limitations

* Calibration targets are by-eye values; the transient ratio of 0.25 is an explicit assumption
  (sensitivity runs at 0.15 and 0.35 are in `data/fitted_scalings.json`).
* The absolute current scale of the model (hundreds of nA) differs about 100 fold from panel C;
  pA-scale steps and biases barely perturb it. Extended amplitudes (up to 10 nA) and biases (up to
  6.4 nA) were exploratory.
* The soma clamp does not control the AIS and dendrites, and the transient is a model-internal Na
  channel current, not a recorded one.
* The -10 mV spike threshold misses attenuated spikes (post-hoc check above); the collapse and bias
  criteria were pre-declared with that threshold.
* Reference cells were screened with a deterministic synapse placement that differs from the earlier
  random placement, so cell identities are those of this task only. Eight cells, 3 seeds: all
  statistics are exploratory.
* The single-cell model has no presynaptic network, so the bias is only a surrogate. The dendritic
  arm used a reduced protocol (no extended amplitudes or bias grid, 5 cells for DSI).
* No remote data (rd1 or rd10 Na/K channel measurements) exist in the corpus; the researcher's raw
  traces would replace the by-eye targets.

## Sources

* Task: `t0131_rd1_na_k_remodelling_dsgc_dsi`
* Task: `t0121_5seed_substrate_rate_canonical_report`
* Task: `t0129_t0126_signed_dsi_real_rates_1seed`
* Paper: `10.1523_JNEUROSCI.1592-24.2024`
* Paper: `10.1101_2020.09.15.297937`
* Paper: `10.1523_jneurosci.5346-03.2004`
* Paper: `10.1016_j.neuron.2005.06.036`
* Paper: `10.1371_journal.pcbi.1000899`
* Paper: `10.1523_jneurosci.0130-07.2007`

[werginz2024]: ../../../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/summary.md
[goethals2020]: ../../../../t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1101_2020.09.15.297937/summary.md
[dhingra2004]: ../../../../t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/summary.md
[oesch2005]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md
[schachter2010]: ../../../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/summary.md
[margolisdetwiler2007]: ../../../../t0017_literature_survey_patch_clamp/assets/paper/10.1523_jneurosci.0130-07.2007/summary.md
