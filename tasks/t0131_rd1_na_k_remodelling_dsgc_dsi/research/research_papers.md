---
spec_version: "1"
task_id: "t0131_rd1_na_k_remodelling_dsgc_dsi"
research_stage: "papers"
papers_reviewed: 24
papers_cited: 12
categories_consulted:
  - "retinal-ganglion-cell"
  - "voltage-gated-channels"
  - "compartmental-modeling"
  - "direction-selectivity"
  - "patch-clamp"
  - "dendritic-computation"
date_completed: "2026-10-27"
status: "partial"
---
# Research Papers: rd1-like Na/K Remodelling of the DSGC Model

## Task Objective

Task t0131 tests whether scaling soma and axon initial segment (AIS) voltage-gated Na and K
conductances in the existing DSGC compartmental model reproduces the researcher's rd1 vs wild-type
(WT) retinal ganglion cell phenotype (`SomeResults.pdf`, panels A-D: elevated spontaneous firing,
collapsed evoked firing at +60 pA, and a +100 mV clamp showing roughly 1.7x larger sustained outward
current with a much smaller Na transient). It then measures what the remodelling does to signed
direction selectivity (DSI) and checks the researcher's toy input-output model (panel D) against the
NEURON model. This file reviews the existing paper corpus for that purpose.

The status is `partial`: the corpus contains no paper on rd1 retinal ganglion cell hyperactivity, no
paper on degeneration-driven remodelling of RGC Na/K currents, and no DSGC-specific degeneration
paper. The only degeneration data point is rd10 alpha-RGC recordings in one paper. The relevant
literature below is therefore indirect: AIS and somatic channel biophysics of healthy RGCs, RGC
spike-generator models, spontaneous-activity mechanisms, and spike-level DSI amplification in DSGCs.
The rd1/rd10 literature must be covered by the internet research stage.

Note on method: the aggregator `arf.scripts.aggregators.aggregate_papers` does not exist in this
worktree (`arf/scripts/aggregators/` has no papers aggregator), so rule 9 could not be followed
literally. The corpus was enumerated from the git-tracked `details.json` files of paper assets (102
files, some duplicates across tasks) and summaries were read directly. No corrections overlay was
applied.

## Category Selection Rationale

Consulted `retinal-ganglion-cell` (the core cell class), `voltage-gated-channels` (Na/K and AIS
biophysics are the manipulated variables), `compartmental-modeling` (the simulator is a NEURON
multi-compartment model and papers give conductance tables), `patch-clamp` (panels A-C are
current-clamp and voltage-clamp recordings), and `direction-selectivity` and `dendritic-computation`
(Part 3 asks how remodelling changes DSI, and spike generation amplifies PSP tuning).

Excluded: `synaptic-integration` and `cable-theory` as primary filters (reached only through papers
already selected). Corpus papers on starburst amacrine circuits, wiring specificity, cortical
dendritic spikes, energy budgets and NSGA-II noise were reviewed by title and excluded as not
bearing on intrinsic Na/K remodelling. No `retinal-degeneration` category exists in
`meta/categories/`; this reflects the gap.

## Key Findings

### Corpus Has Almost No rd1/rd10 Intrinsic-Remodelling Evidence

Of the 24 papers examined, only [Werginz2024] touches photoreceptor degeneration. It recorded mouse
alpha-RGCs in rd10 retina (p193-p227) with synaptic transmission blocked and found the sustained vs
transient spike-generator distinction persists: rd10 sustained-to-peak ratio **0.55 +/- 0.13**
(sustained) and **0.30 +/- 0.11** (transient) against WT **0.57** and **0.32**, with spike duration
**0.29 +/- 0.05 ms** vs **0.22 +/- 0.05 ms**. So in old rd10 alpha-RGCs the intrinsic spike
generator is largely preserved. This does not support a large intrinsic Na loss and K gain as in
panel C, and it is a tension to keep in view: the researcher's data are FVB/N rd1 (earlier, faster
degeneration, cell type not stated as alpha). The difference may be due to cell type or age, or the
hyperactivity may be network-driven rather than channel-driven.

### Where Na and K Sit: the AIS Dominates Spike Initiation

[Werginz2024] gives a NEURON alpha-RGC table (mS/cm^2): gNa 75 in dendrites, soma and soma-AIS,
**1300** in the AIS and 65 in the axon; gK 48 in dendrites and soma, **800** in the AIS and 40 in
the axon. [Fohlmeister2010] gives cell-type-specific densities at 35 C, e.g. rat Type I Na 79.5
(dendrite) / 72.0 (soma) / 141.1 (initial segment) / 231.1 (thin segment) and K 23.4 / 50.4 / 67.8 /
74.6, with cat alpha Na reaching **448.5** on the thin segment. [Goethals2020] measured a mean AIS
axial current of **6.7 nA** in P10-12 mouse RGCs and estimated AIS Na density of at least about
**1000 S/m^2** (conservative) and about **5000-5500 S/m^2** best fit. [Werginz2020] reports an
AIS-to-soma Na ratio of about **7x** and shows AIS length and Nav1.6 density set the maximum firing
rate. All sources agree the AIS carries several-fold to over ten-fold the somatic Na density, so a
"soma plus AIS" gNa scale in Part 1 is dominated by the AIS term.

A soma voltage-clamp step does not isolate the soma. [Goethals2020] stepped the soma from -60 mV in
0.5-1 mV increments and read the AIS action potential current as a large abrupt inward current
flowing resistively to the clamped soma; **98 +/- 0.4%** of it was removed by 1 uM TTX. The panel C
"smaller inward transient" in rd1 could therefore reflect AIS Na loss, AIS shortening or
displacement, or inactivation, and clamp data at the soma cannot separate these.

### Na Subunit Identity and Depolarisation Block

[Wienbar2022] shows the same synaptic input yields opposite feature selectivity in two mouse RGC
types because of spike-generator differences: the OFF sustained alpha cell has an AIS of **22 +/-
1.7 um** with about **40%** Nav1.6, while the bursty suppressed-by-contrast cell has **16 +/- 1.5
um** and a Nav1.2-only AIS that is driven into depolarisation block more easily. [Werginz2020] found
ventral OFF-alphaT cells enter depolarisation block at lower current than dorsal cells. In
[Werginz2024] break currents were **792 +/- 132 pA** (alpha-ON), **369 +/- 63 pA** (alpha-OFF
sustained) and **560 +/- 154 pA** (alpha-OFF transient), at break voltages of about **-38 to -45
mV**. A +60 pA step is far below these, so a collapse of rd1 spiking at +60 pA is not ordinary
overdrive block; it is more consistent with Na loss or strong inactivation. A depolarised plateau
caused by a larger K load cannot be excluded without sweeping the current amplitude.

### Mechanisms of Spontaneous Firing in RGCs

[MargolisDetwiler2007] show ON RGCs lose maintained firing when ionotropic glutamate receptors are
blocked, whereas OFF RGCs keep firing and show subthreshold oscillations, burst firing and rebound
excitation, attributed to different complements of voltage-gated conductances rather than passive
properties. Elevated rd1 spontaneous activity in the literature is thus plausibly a mix of
network-driven and intrinsic pacemaker mechanisms. A single-cell model without synaptic input can
represent only the second; Part 2's tonic bias or noise is a stand-in for the first. The present
model has no T-type Ca or HCN conductance on which an OFF-like pacemaker could build. [Muller2024]
reviews persistent Na current (INaP): Nav1.6 carries a major share, and Nav1.6 knockout in cortical
layer 5 leaves about **50%** of INaP, so INaP is a candidate contributor to rest-level excitability
that a transient-Na-focused clamp may miss.

### Firing Patterns, Geometry and Irregularity

[FohlmeisterMiller1997] conclude from multi-compartment RGC models (up to 800 compartments) that
cell geometry is the primary determinant of firing pattern and F/I response, with channel density
distribution at most secondary, and that near-threshold stimuli give irregular firing from multiple
impulse initiation sites. This supports Part 2's expectation of irregular firing under weak drive,
warns that Na/K scaling alone may change gain more than pattern, and supports keeping the dendritic
scaling arm as the planned fallback. The summary of this paper is abstract-based (the PDF was not
available), so quantitative claims are unverified.

[Dhingra2004] show the RGC spike generator has a threshold nonlinearity: contrast detection
threshold **1.5%** from the graded potential vs **3.8%** from spikes, spikes carrying **~60% fewer**
gray levels, and tonic depolarisation lowering the spike threshold at the cost of dynamic range.
That is a direct precedent for panel D's prediction that a depolarised, high-baseline cell has a
compressed input-output range and saturates.

### Spike Generation Amplifies DSGC Directional Tuning

[Oesch2005] report spike DSI of **0.67 +/- 0.13** (ON) and **0.74 +/- 0.13** (OFF) against PSP DSI
of only **0.09** and **0.14**, a roughly 6-fold sharpening, with light-evoked spike threshold near
**-56 mV** vs **-49 mV** for somatic current injection; bath TTX collapsed PSP DSI to **0.04** (ON)
and **0.21** (OFF). In the model of [Schachter2010], PSP DSI of about **0.2** becomes spike DSI of
about **0.8** (about 4x) through the dendritic spike threshold; one dendritic spike drives a 1:1
somatic spike, and a distal synapse needs about **1 nS** to initiate a spike vs **3-4 nS** near the
soma. DSI in DSGCs therefore depends on spike thresholds and dendritic Na channels. Reduced Na
should raise effective thresholds and cut PD rate more than ND rate, which tends to lower DSI if ND
is not already at floor, though the direction depends on the baseline. A tonic bias raises both PD
and ND rates and should compress signed DSI = (PD - ND)/(PD + ND) via the reduced dynamic range
described by [Dhingra2004]. These are hypotheses, not literature results.

### Sodium Entry and Metabolic Interpretation

[Carter2009] found sodium entry per spike depends on spike waveform, not cell-type-specific channel
kinetics: ratio of actual to minimum Na entry of **2.00 +/- 0.61** in Purkinje, **1.98 +/- 0.55** in
fast-spiking interneurons, **1.62 +/- 0.67** in CA1 and **1.24 +/- 0.29** in cortical pyramidal
cells, with spike width vs ratio Spearman **-0.48**. If rd1 Na and K remodelling alters spike width,
Na entry efficiency changes; this is peripheral but connects to the project's ATP-cost diagnostics.

## Methodology Insights

* **Define compartment scaling from published tiers**: scale gNa and gK jointly in soma and AIS,
  using the tiered table of [Werginz2024] (AIS gNa 1300 and soma 75; AIS gK 800 and soma 48) as the
  reference structure, and cross-check against [Fohlmeister2010]. Report both the multiplicative
  scale and the resulting whole-cell conductance, since the AIS term dominates.
* **Respect clamp limits**: simulate the +100 mV step at the soma and record somatic and AIS
  currents separately, following the resistive-coupling analysis of [Goethals2020]. Estimate the Na
  component as the TTX-like difference (gNa = 0 run) and the sustained component at the step end.
* **Report the Part 1 grid as two output maps**: sustained-current ratio (target about 1.7) and
  transient amplitude on at least a 6 x 6 gNa 0.25-1.0x by gK 1-3x grid; the two observables
  constrain different directions in the plane.
* **Sweep current beyond +60 pA** (to several hundred pA, where break currents of 369-792 pA occur
  per [Werginz2024]) to distinguish Na-loss collapse from depolarisation block [Werginz2020].
* **Measure f-I and adaptation in published units**: sustained-to-peak ratio (last 200 ms over peak
  in first 100 ms), spike FWHM (**0.21-0.31 ms** for alpha-RGCs [Werginz2024]), peak rate and break
  current, so model outputs compare to measured quantities.
* **Treat the tonic bias as a network surrogate**: fix Part 1 first, then tune bias and noise
  amplitude separately against the ~7 Hz target, and report DSI with and without it. State that the
  ON-cell component of maintained firing is synaptic [MargolisDetwiler2007], so a bias is a
  legitimate stand-in for that part only.
* **Compute DSI from spikes**: PSP DSI is a poor proxy (0.09-0.2 vs 0.7-0.8 for spikes
  [Oesch2005, Schachter2010]); keep PD and ND rates visible next to signed DSI.
* **Testable hypotheses**: (H1) a soma+AIS gNa scale of roughly 0.4-0.6x with gK of 1.5-2x gives a
  sustained-current ratio near 1.7; (H2) the same scalings collapse +60 pA firing without any firing
  data in the fit; (H3) a tonic bias gives about 7 Hz irregular firing in rd1-like cells but not
  WT-like cells only if rd1-like threshold or input resistance differs, which the clamp data do not
  guarantee and must be checked; (H4) rd1-like spike DSI is lower than WT-like, mainly with the
  tonic bias on [Dhingra2004]; (H5) panel D saturation appears in the compartmental model only with
  a tonic bias.

## Gaps and Limitations

* No corpus paper reports rd1 or rd10 RGC voltage-clamp Na transient or sustained K current, so the
  1.7x ratio and reduced transient of panel C cannot be benchmarked. The only rd10 data,
  [Werginz2024], show a largely preserved spike generator in old alpha-RGCs.
* No corpus paper treats DSGC-specific intrinsic Na/K properties; DSGC models such as
  [Schachter2010] use generic RGC channel sets of the [Fohlmeister2010] kind.
* No paper quantifies how remodelled Na/K changes signed antipodal DSI; this must come from our
  simulations.
* AIS Na density and subunit papers by Kole (2008), Hu (2009) and VanWart (2006) exist in the corpus
  only as CrossRef-metadata summaries with no extracted results, and [FohlmeisterMiller1997] and
  [Werginz2020] are abstract-based, so their numbers are unverified against the PDFs.
* Ages and species differ across sources (P10-12 mouse [Goethals2020], adult mouse [Werginz2024],
  rd10 p193-p227, rat and cat [Fohlmeister2010]); none is FVB/N rd1 at the researcher's age.
* Persistent Na, HCN and T-type Ca contributions to rd1 spontaneous firing are unquantified for RGCs
  in the corpus and absent from the model.

## Recommendations for This Task

1. Scale soma and AIS conductances together but log somatic and AIS currents separately, using
   [Werginz2024] and [Goethals2020] to interpret the clamp transient (Part 1).
2. Extend the Part 2 current sweep to several hundred pA so Na-loss collapse and depolarisation
   block are distinguishable ([Werginz2020], [Werginz2024]).
3. Report adaptation index, spike FWHM and f-I curves in the units of [Werginz2024] (Part 2.3).
4. Treat the tonic bias as an explicit network surrogate justified by [MargolisDetwiler2007], and
   evaluate DSI with and without it (Parts 2 and 3).
5. Compute DSI from spikes and show PD and ND rates, since rate compression drives DSI change
   ([Oesch2005], [Schachter2010], [Dhingra2004]).
6. Keep the dendritic-scaling arm as the fallback, given [FohlmeisterMiller1997] on geometry and
   dendritic channels governing F/I.
7. Hand the rd1/rd10 literature search (hyperactivity, oscillations, Na and K current changes) to
   the internet research stage and consider adding a `retinal-degeneration` category.

## Paper Index

### [Werginz2024]

* **Title**: Differential Intrinsic Firing Properties in Sustained and Transient Mouse alpha RGCs
  Match Their Light Response Phenotypes
* **Authors**: Werginz, P., Kiraly, J., Zeck, G.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1592-24.2024`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Only corpus paper with rd10 RGC recordings; supplies the tiered AIS/soma
  conductance table, f-I, break-current and spike-shape benchmarks.

### [Werginz2020]

* **Title**: Tailoring of the axon initial segment shapes the conversion of synaptic inputs into
  spiking output in OFF-alpha T retinal ganglion cells
* **Authors**: Werginz, P., Raghuram, V., Fried, S. I.
* **Year**: 2020
* **DOI**: `10.1126/sciadv.abb6642`
* **Asset**: `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `compartmental-modeling`,
  `patch-clamp`
* **Relevance**: AIS length and Nav1.6 density set maximum rate and depolarisation block; AIS/soma
  Na ratio about 7x. Summary is from the abstract and training knowledge, not a local PDF.

### [Wienbar2022]

* **Title**: Differences in spike generation instead of synaptic inputs determine the feature
  selectivity of two retinal cell types
* **Authors**: Wienbar, S., Schwartz, G. W.
* **Year**: 2022
* **DOI**: `10.1016/j.neuron.2022.04.012`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1016_j.neuron.2022.04.012/`
* **Categories**: `compartmental-modeling`, `retinal-ganglion-cell`, `voltage-gated-channels`,
  `patch-clamp`
* **Relevance**: Shows AIS Nav1.2/Nav1.6 composition alone changes RGC output under identical input;
  precedent that Na remodelling changes tuning.

### [Goethals2020]

* **Title**: Electrical match between initial segment and somatodendritic compartment for action
  potential backpropagation in retinal ganglion cells
* **Authors**: Goethals, S., Sierksma, M. C. et al.
* **Year**: 2020
* **DOI**: `10.1101/2020.09.15.297937`
* **Asset**:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1101_2020.09.15.297937/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `patch-clamp`,
  `compartmental-modeling`
* **Relevance**: Soma voltage clamp of RGCs reveals AIS axial current (6.7 nA) and an AIS Na density
  estimate; a template for interpreting panel C.

### [Fohlmeister2010]

* **Title**: Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells: Using
  Temperature as an Independent Variable
* **Authors**: Fohlmeister, J. F., Cohen, E. D., Newman, E. A.
* **Year**: 2010
* **DOI**: `10.1152/jn.00123.2009`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/`
* **Categories**: `retinal-ganglion-cell`, `compartmental-modeling`, `voltage-gated-channels`,
  `patch-clamp`
* **Relevance**: Per-compartment Na, K and Ca densities for several RGC types, for calibrating
  baseline and scaled values.

### [FohlmeisterMiller1997]

* **Title**: Mechanisms by Which Cell Geometry Controls Repetitive Impulse Firing in Retinal
  Ganglion Cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **Asset**:
  `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1152_jn.1997.78.4.1948/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Geometry vs channel density in F/I and irregular near-threshold firing; motivates
  the dendritic arm. Abstract-based summary only.

### [Dhingra2004]

* **Title**: Spike Generator Limits Efficiency of Information Transfer in a Retinal Ganglion Cell
* **Authors**: Dhingra, N. K., Smith, R. G.
* **Year**: 2004
* **DOI**: `10.1523/jneurosci.5346-03.2004`
* **Asset**:
  `tasks/t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/`
* **Categories**: `retinal-ganglion-cell`, `voltage-gated-channels`, `compartmental-modeling`
* **Relevance**: Threshold nonlinearity and the sensitivity vs dynamic range trade-off under
  depolarisation; precedent for panel D saturation.

### [MargolisDetwiler2007]

* **Title**: Different Mechanisms Generate Maintained Activity in ON and OFF Retinal Ganglion Cells
* **Authors**: Margolis, D. J., Detwiler, P. B.
* **Year**: 2007
* **DOI**: `10.1523/jneurosci.0130-07.2007`
* **Asset**:
  `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1523_jneurosci.0130-07.2007/`
* **Categories**: `retinal-ganglion-cell`, `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Separates synaptic-driven from intrinsic pacemaker spontaneous firing; frames the
  tonic bias of Part 2.

### [Muller2024]

* **Title**: Persistent sodium currents in neurons: potential mechanisms and pharmacological
  blockers
* **Authors**: Muller, P., Draguhn, A. et al.
* **Year**: 2024
* **DOI**: `10.1007/s00424-024-02980-7`
* **Asset**: `tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1007_s00424-024-02980-7/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`, `patch-clamp`
* **Relevance**: INaP as an unmodelled candidate contributor to rest-level excitability, and the
  Nav1.6 share of it.

### [Oesch2005]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `voltage-gated-channels`,
  `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Spike generation amplifies DSI about 6-fold and TTX collapses it; baseline for how
  Na reduction could change DSI.

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`
* **Relevance**: Compartmental DSGC reference; PSP DSI about 0.2 to spike DSI about 0.8 and
  spike-threshold dependence, relevant to Part 3.

### [Carter2009]

* **Title**: Sodium Entry during Action Potentials of Mammalian Neurons: Incomplete Inactivation and
  Reduced Metabolic Efficiency in Fast-Spiking Neurons
* **Authors**: Carter, B. C., Bean, B. P.
* **Year**: 2009
* **DOI**: `10.1016/j.neuron.2009.12.011`
* **Asset**: `tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/paper/10.1016_j.neuron.2009.12.011/`
* **Categories**: `voltage-gated-channels`, `patch-clamp`
* **Relevance**: Spike width controls Na entry per spike; links rd1 spike-shape changes to the
  project's ATP-cost diagnostics.
