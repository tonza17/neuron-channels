---
spec_version: "1"
task_id: "t0015_literature_survey_cable_theory"
research_stage: "papers"
papers_reviewed: 20
papers_cited: 3
categories_consulted:
  - "cable-theory"
  - "compartmental-modeling"
  - "dendritic-computation"
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Broaden the project's paper corpus beyond DSGC-specific compartmental modelling by surveying roughly
25 category-relevant papers on classical cable theory and passive dendritic filtering. The survey
targets five themes (Rall-era foundations, d_lambda segment-discretisation rule, branched-tree
impedance, frequency-domain filtering, and transmission in thin dendrites) and must avoid
re-downloading the 20 DOIs already present in the t0002 DSGC corpus. This existing-papers research
step inventories what cable-theory content the project already holds so that internet search can
focus on the gap.

## Category Selection Rationale

Consulted `cable-theory`, `compartmental-modeling`, and `dendritic-computation` because those three
categories are where any prior Rall-family theoretical content would have been filed. Also checked
`retinal-ganglion-cell`, `voltage-gated-channels`, `synaptic-integration`, `direction-selectivity`,
and `patch-clamp` for completeness, but papers tagged only with those labels are DSGC-specific
experimental or modelling papers and therefore out of scope for this survey. Excluded the downstream
task categories that do not yet carry papers. The three consulted categories map directly onto the
five thematic axes of this task: foundations and d_lambda rule -> `cable-theory`; branched-tree
impedance and frequency-domain filtering -> `dendritic-computation`; thin-dendrite transmission ->
both, with implementation practice captured under `compartmental-modeling`.

## Key Findings

### Coverage of Cable Theory in the Existing Corpus

The t0002 DSGC corpus touches cable theory in three papers but does not constitute a survey of the
theory itself. [Hines1997] documents how NEURON discretises the cable equation on branched trees
(tridiagonal system solved in O(N) operations with Hines's tree elimination) and introduces the
`section`/`segment` data model that every DSGC paper in the corpus uses downstream. [Schachter2010]
applies the cable framework to a rabbit ON-OFF DSGC reconstruction with `~thousands of compartments`
sized to **< 0.1 lambda**, `Ri = 110 Ohm cm`, `Cm = 1 uF/cm^2`, and concludes that the dendritic
tree fragments into quasi-independent electrotonic subunits that each reach a local spike threshold.
[Branco2010] is the only paper in the corpus that explicitly invokes the Rall impedance-gradient
idea: distal-tip input impedance is higher than somatic input impedance, and this gradient —
combined with NMDA Mg2+ nonlinearity — underlies sequence direction selectivity in cortical
pyramidal dendrites. Branco et al. also cite Rall's 1964 prediction that passive delay lines should
produce direction-selective summation but note that the passive mechanism is too weak in short
dendrites, motivating the active NMDA mechanism.

### Quantitative Anchors Available Locally

The corpus provides one concrete set of DSGC compartment parameters: **Ri = 110 Ohm cm**, **Cm = 1
uF/cm^2**, arbor radius ~150 um, soma ~15 um, dendritic segments discretised to < 0.1 lambda
[Schachter2010]. [Hines1997] provides the theoretical framing: the implicit backward Euler and the
staggered Crank-Nicolson schemes both converge for the cable equation once segment length is below
the lambda-based discretisation bound, and analytical integration of channel gating via
`s(t+dt) = s_inf + (s(t) - s_inf) * exp(-dt/tau)` is used instead of generic ODE stepping. The
optimal-velocity band for passive + NMDA sequence direction selectivity in pyramidal dendrites is
reported as **2.6 +/- 0.5 um/ms** for somatic EPSP [Branco2010]. No direct ganglion-cell
electrotonic length constant is reported in the corpus.

### Open Themes Not Covered Locally

The corpus does not contain Rall's own foundational papers (1959 core-conductor analysis, 1962
equivalent-cylinder, 1964 active/passive dendritic models), Koch/Poggio/Torre frequency-domain
treatments, Jack/Noble/Tsien-style textbook derivations, Stuart/Spruston/Hausser-style transfer-
impedance analyses, Carnevale/Hines's textbook treatment of the d_lambda rule, or any ZAP/chirp
analyses of dendritic resonance. These are exactly the gaps this survey must fill through internet
search.

**Hypothesis**: the DSGC-specific compartment parameters from [Schachter2010] (Ri = 110 Ohm cm, Cm =
1 uF/cm^2) should place a typical 1 um diameter dendrite near the geometric regime where passive
propagation of PSPs and dendritic spikes is near-lossy (electrotonic length ~1 from distal tip to
soma). Surveying cable-theory papers that report explicit electrotonic length estimates for
ganglion-cell-class dendrites would allow this hypothesis to be checked against independent
measurements before calibration tasks commit to specific Rm/Ri values.

**Best practice (from local evidence)**: discretise dendrites to segment lengths < 0.1 lambda to
avoid numerical artefacts [Schachter2010]; use NMODL for new channel definitions and let NEURON's
solver handle the cable matrix [Hines1997]; treat the dendritic tree as a set of electrotonic
subunits rather than as a uniform cable when directional computations matter
[Schachter2010, Branco2010].

## Methodology Insights

* **Discretisation target**: use segment length < **0.1 * lambda** along every dendrite before
  trusting the simulated waveform [Schachter2010]; this is the operational form of the d_lambda rule
  in the corpus.

* **Default passive parameters for DSGC dendrites**: **Ri = 110 Ohm cm** and **Cm = 1 uF/cm^2** are
  the values the t0002 Schachter reconstruction uses; Rm is fitted to match input resistance rather
  than asserted a priori [Schachter2010]. Any cable-theory paper selected for download should report
  comparable quantities so the values can be triangulated.

* **Electrotonic subunit framing**: treat each branch of the arbor as a local summation unit that
  reaches a local spike threshold; inhibition gates initiation, not propagation, at physiological
  conductance levels (~6 nS for DSGCs; would require ~85 nS to block propagation) [Schachter2010].
  This framing constrains which cable-theory regimes (electrotonically compact vs extended) are most
  relevant.

* **Impedance gradient mechanism**: distal input impedance higher than proximal input impedance is
  the qualitative driver of both passive direction selectivity (Rall 1964) and active NMDA-based
  direction selectivity [Branco2010]. Any survey paper that reports input-impedance vs position
  along a ganglion-cell-class dendrite is high-value.

* **Simulator alignment**: the survey answer must be readable by someone working in NEURON;
  [Hines1997] fixes the vocabulary (section, segment, nseg, lambda) and the numerical schemes
  (backward Euler, staggered Crank-Nicolson) that the rest of the project will use.

* **Hypothesis to carry into internet search**: for highly branched thin (< 1 um) dendrites, the
  classical equivalent-cylinder assumption (Rall 1962) breaks down because the 3/2-power rule on
  daughter diameters is rarely satisfied. This hypothesis should be validated against papers found
  during the internet-research step.

## Gaps and Limitations

The corpus contains zero foundational Rall papers, no textbook-level cable-theory derivations, no
Koch-style dendritic-filtering analyses, no explicit treatment of the d_lambda / nseg rule beyond
the one-line Schachter et al. statement, and no frequency-domain (ZAP/chirp) studies. It also
contains no cable-theory paper that reports an electrotonic length estimate for a retinal ganglion
cell (the few numbers available are for cortical pyramidal cells or rabbit DSGCs only). Papers on
propagation failure in thin dendrites, sealed-end vs killed-end boundary conditions, and branched-
tree transfer impedance are absent entirely. The internet-research step must supply all five
thematic buckets identified in the task description.

## Recommendations for This Task

1. **Internet search must cover all five themes** — the corpus supplies none of them in standalone
   form. Prioritise Rall foundational papers (1959/1962/1964/1967), d_lambda-rule references
   (Hines/Carnevale textbook, 2006; Mainen/Carnevale discretisation studies), and branched-tree
   impedance papers (Koch, Holmes, Zador) [Hines1997, Schachter2010, Branco2010].

2. **Include at least three ganglion-cell-specific electrotonic-length papers** so the answer asset
   can report a numerical range rather than a theoretical template.

3. **Carry the Schachter passive parameters forward** as the anchor against which any cable-theory
   paper's parameters are compared [Schachter2010].

4. **Treat Branco 2010 as the template** for how active nonlinearity interacts with a passive
   impedance gradient [Branco2010]; downstream papers on directional dendritic integration should be
   cross-referenced against it.

5. **De-duplicate aggressively** — only three corpus DOIs touch cable theory, so the
   de-duplication risk during internet search is confined to those three plus the other 17 DSGC
   papers already in t0002.

## Paper Index

### [Hines1997]

* **Title**: The NEURON Simulation Environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **Asset**:
  `../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`
* **Categories**: `compartmental-modeling`, `cable-theory`, `voltage-gated-channels`
* **Relevance**: Defines the NEURON discretisation of the branched cable equation and the
  section/segment/nseg abstractions that every DSGC paper in the corpus relies on. Primary local
  source for cable-equation numerical schemes.

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`, `synaptic-integration`, `cable-theory`
* **Relevance**: Supplies the only concrete DSGC cable-parameter set in the corpus (Ri = 110 Ohm cm,
  Cm = 1 uF/cm^2, segments < 0.1 lambda) and the electrotonic-subunit framing that downstream
  cable-theory selections must be compatible with.

### [Branco2010]

* **Title**: Dendritic Discrimination of Temporal Input Sequences in Cortical Neurons
* **Authors**: Branco, T., Clark, B. A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1126/science.1189664`
* **Asset**:
  `../../t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/`
* **Categories**: `cable-theory`, `compartmental-modeling`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Only corpus paper that explicitly invokes Rall's impedance-gradient argument and
  links it to an experimentally characterised direction-sensitive dendritic mechanism. Provides the
  impedance-gradient vocabulary the answer asset will need.
