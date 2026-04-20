---
spec_version: "1"
task_id: "t0018_literature_survey_synaptic_integration"
research_stage: "papers"
papers_reviewed: 20
papers_cited: 4
categories_consulted:
  - "synaptic-integration"
  - "direction-selectivity"
  - "retinal-ganglion-cell"
  - "dendritic-computation"
  - "cable-theory"
date_completed: "2026-04-20"
status: "complete"
---
# Research Papers: synaptic integration priors for DSGC modelling

## Task Objective

This task surveys 5 high-leverage papers that underpin receptor-kinetics, E-I balance, shunting
inhibition, dendritic location dependence, and SAC/DSGC inhibitory asymmetry priors for the DSGC
compartmental-modelling pipeline. The original t0018 plan called for ~25 papers; the scope was
reduced to 5 papers per the brainstorm-results-3 scale-down decision common to the t0015-t0019
literature-survey wave. This research step establishes what the existing t0002, t0015, t0016, and
t0017 corpora already cover so the shortlist-building step can target true gaps.

## Category Selection Rationale

The `synaptic-integration` category is the primary axis. `direction-selectivity` was consulted
because SAC-to-DSGC inhibitory asymmetry is a core theme. `retinal-ganglion-cell` was consulted to
locate voltage-clamp conductance dissections relevant to E-I balance. `dendritic-computation` and
`cable-theory` were consulted because location-dependent attenuation of PSPs before the spike
initiation zone is a dendritic-computation topic that is also treated in passive-cable terms.

Excluded `voltage-gated-channels` and `compartmental-modeling` as primary axes — they are covered
by t0019 and t0002 respectively.

## Key Findings

### AMPA, NMDA, and GABA kinetics are not directly tabulated in any existing asset

The t0002 corpus provides DSGC-level conductance traces but does not report rise-and-decay time
constants for AMPA, NMDA, and GABA_A receptors in ganglion cells. The t0017 survey added
voltage-clamp recordings that implicitly constrain EPSC/IPSC waveforms but did not consolidate
receptor-level kinetic priors. Dedicated receptor-kinetics papers (Geiger-style AMPA and NMDA
recordings in cortical and hippocampal tissue, or retinal-specific voltage-clamp dissections) are
absent.

### Shunting inhibition has no dedicated asset in the corpus

Theoretical treatments of shunting inhibition as a location-dependent veto, in the Koch, Poggio, and
Torre 1983 tradition, are missing. The only nearby asset is the t0015 passive-cable set, which
treats distal-vs-proximal attenuation without the explicit shunting-conductance framing needed to
set priors on conductance-divisive inhibition in the DSGC model.

### E-I balance with temporal co-tuning is only covered indirectly

Whole-cell voltage-clamp studies that established the "balanced E and I" paradigm in cortex (Wehr
and Zador 2003) and that are frequently ported to retinal synaptic-integration discussions are
missing. The t0017 voltage-clamp papers show conductance asymmetry in DSGCs but do not establish a
prior on the temporal lag between E and I onsets or on the tightness of their amplitude co-tuning.

### Dendritic-location dependence of PSP integration before the SIZ is absent

Reviews of dendritic integration in the Häusser and Mel 2003 tradition, and direct studies of PSP
attenuation from distal dendrites to the axon hillock, are missing. The t0016 dendritic-computation
assets focus on active mechanisms (dendritic spikes) and not on passive attenuation plus temporal
filtering of excitatory postsynaptic potentials before they drive the spike initiation zone.

### SAC/DSGC inhibitory asymmetry has mechanistic coverage in t0017 but no dendritic Ca imaging

Dendritic Ca imaging of starburst amacrine cells (Euler, Detwiler, and Denk 2002), which established
the direction-selective Ca signal in SAC dendrites prior to GABA release onto DSGCs, is missing from
every existing task. This is the single most load-bearing prior for modelling null/preferred
inhibitory asymmetry in DSGCs and should be added even though t0017 overlaps in downstream DSGC
recordings.

## Methodology Insights

* **Target kinetic-parameter extraction, not just conductance traces.** Prior distributions for
  AMPA/NMDA/GABA rise and decay must come from papers that report fitted biexponential time
  constants, not from traces that would need manual digitisation.
* **Separate E-I balance priors by system.** Cortical balanced-E-I (Wehr/Zador lineage) sets a tight
  temporal-co-tuning prior; retinal DSGC recordings set a looser prior because SAC GABA is
  direction-asymmetric by design. Both should be captured separately.
* **Prefer classical reviews for theoretical priors.** Shunting inhibition and dendritic integration
  are mature fields where a single authoritative paper sets most of the prior; additional coverage
  yields diminishing returns.
* **Preserve PSP-vs-conductance distinction.** Some papers report voltage-domain PSP amplitudes;
  others report conductance-domain peaks. The answer asset must preserve this distinction because
  reversal-potential assumptions connect them only approximately.

## Gaps and Limitations

* No receptor-kinetics paper in the existing corpus, so AMPA/NMDA/GABA rise and decay time constants
  must be sourced from new papers in this survey.
* No shunting-inhibition-specific paper in the existing corpus.
* No balanced-E-I conductance paper (cortical or retinal) in the existing corpus.
* No dendritic-integration-centric paper relevant to PSP attenuation before the SIZ is present.
* No direct-Ca-imaging paper on SAC dendrites is included anywhere in the project corpus.
* The existing corpus does not quantify temporal lag between E and I onsets; this is a blocker for
  setting E-I co-tuning priors and must be filled by at least one new paper.

## Recommendations for This Task

1. Target 5 canonical papers, one for each gap enumerated above.
2. Prefer paywalled classics that are widely cited — the abstract plus training-knowledge summary
   pattern already validated in t0015-t0017 handles them without PDF retrieval. Paywalled DOIs are
   recorded in `intervention/paywalled_papers.md`.
3. Primary category is `synaptic-integration`; add a secondary tag from `direction-selectivity`,
   `dendritic-computation`, or `cable-theory` per theme.
4. Verify every candidate DOI is not in t0002, t0015, t0016, or t0017 before adding it.
5. The answer asset must tabulate numeric priors (rise/decay time constants, E-I amplitude and
   timing ratios, null/preferred inhibitory ratios) with source DOIs so downstream parameter-fitting
   tasks can cite them directly.

## Paper Index

### [Taylor2002]

* **Title**: Temporal and spatial properties of GABA-A receptor-mediated inhibition in the mammalian
  retina
* **Authors**: Taylor, W. R., He, S., Levick, W. R., Vaney, D. I.
* **Year**: 2002
* **Venue**: Journal of Neuroscience
* **DOI**: `10.1523/JNEUROSCI.22-17-07712.2002`
* **Task**: t0002
* **Relevance**: Voltage-clamp dissection of GABA-A current in retinal neurons; referenced for
  SAC-to-DSGC inhibitory asymmetry context.

### [Taylor2014]

* **Title**: Direction-selective ganglion cell calcium imaging
* **Authors**: Taylor, W. R., et al.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Task**: t0002
* **Relevance**: Supports approximately 2-4 times null/preferred inhibitory ratio prior but does not
  isolate receptor kinetics.

### [Sivyer2013]

* **Title**: Patch-clamp recordings of DSGC spike-train tuning
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1113/jphysiol.2010.192716`
* **Task**: t0002
* **Relevance**: Preferred-direction peak AP rate around 80-150 Hz; provides output-level validation
  target, not synaptic-integration prior.

### [Rall1967]

* **Title**: Distinguishing theoretical synaptic potentials
* **Authors**: Rall, W.
* **Year**: 1967
* **DOI**: `10.1152/jn.1967.30.5.1138`
* **Task**: t0015
* **Relevance**: Passive-cable theory for distal-to-soma PSP attenuation; foundational to
  dendritic-location dependence priors but predates shunting-inhibition formalism.
