---
spec_version: "1"
task_id: "t0019_literature_survey_voltage_gated_channels"
research_stage: "papers"
papers_reviewed: 20
papers_cited: 3
categories_consulted:
  - "voltage-gated-channels"
  - "retinal-ganglion-cell"
  - "compartmental-modeling"
  - "patch-clamp"
  - "dendritic-computation"
date_completed: "2026-04-20"
status: "complete"
---
# Research Papers: voltage-gated channel priors for DSGC modelling

## Task Objective

This task surveys 5 high-leverage papers that supply priors on voltage-gated Nav and Kv channel
expression, kinetics, and conductance densities in retinal ganglion cells, to constrain the Na/K
optimisation experiment (RQ1) of the DSGC compartmental-modelling pipeline. The original t0019 plan
called for ~25 papers; the scope was reduced to 5 papers per the brainstorm-results-3 scale-down
decision common to the t0015-t0019 literature-survey wave. This research step establishes what the
existing t0002, t0015, t0016, t0017, and t0018 corpora already cover so the shortlist-building step
can target true gaps in voltage-gated-channel priors.

## Category Selection Rationale

The `voltage-gated-channels` category is the primary axis. `retinal-ganglion-cell` was consulted
because Nav1.6 distribution at the RGC axon initial segment (AIS) and Kv subunit expression in RGCs
are core themes. `patch-clamp` was consulted because the HH-family kinetic models and
activation/inactivation curves that constrain Nav/Kv priors come from voltage-clamp recordings.
`compartmental-modeling` was consulted because RGC-specific Nav/Kv conductance-density estimates for
the soma-vs-AIS-vs-dendrite compartments are the central output. `dendritic-computation` was
consulted because dendritic Nav and Kv distributions affect back-propagation and spike integration.

Excluded `synaptic-integration` and `cable-theory` as primary axes - they are covered by t0018 and
t0015 respectively.

## Key Findings

### Nav subunit expression in RGCs is not directly tabulated in any existing asset

The t0002 corpus provides DSGC-level spike-rate traces but does not report Nav1.1, Nav1.2, or Nav1.6
subunit localisation at the RGC soma, AIS, or dendrite. The t0017 patch-clamp survey added
voltage-clamp recording methodology but did not consolidate subunit-specific Nav channel priors
dedicated to the AIS sodium current. Immunohistochemistry and electrophysiology papers that
establish the Nav1.6-concentrated AIS pattern in RGCs (Van Wart-style works) are absent.

### Kv subunit expression in RGCs is not covered

No paper in the existing corpora systematically reports Kv1, Kv2, Kv3, Kv4, BK, or SK channel
distributions in RGCs. The t0017 voltage-clamp papers document transient K+ currents at the spike
output level but do not identify the underlying subunits or their conductance densities.

### HH-family kinetic models for RGC Nav/Kv are absent

Canonical rate functions, activation and inactivation curves, and time constants for RGC Nav and Kv
channels (e.g., Fohlmeister-Miller-type RGC HH models) are not present in the corpus. This is a
load-bearing gap: the downstream NEURON model requires published rate functions as the starting
point for parameter fitting.

### Subunit co-expression patterns are not documented

Specific RGC-type-level Nav+Kv combinations (e.g., ON-OFF DSGCs having Nav1.6 AIS + Kv3 soma) are
not tabulated anywhere in the project corpus. This is needed to inform which channel combinations to
include in the DSGC model.

### Nav/Kv conductance-density estimates by compartment are missing

Published quantitative estimates of Nav peak conductance density at the AIS (often 10-100x somatic),
somatic Nav density, and dendritic Nav/Kv densities are absent. These numbers are priors for the
optimisation search ranges.

## Methodology Insights

* **Target subunit-resolved and compartment-resolved measurements.** Prior distributions for Nav/Kv
  channel-density fitting must come from papers that report Nav1.x subunit identity and AIS vs.
  somatic vs. dendritic density, not bulk sodium-current recordings.
* **Prefer RGC-specific over cortical where available.** RGC Nav/Kv kinetics differ from cortical
  pyramidal-cell kinetics; RGC-specific priors should be preferred when they exist
  (Fohlmeister-Miller for RGC HH models).
* **Separate Nav-kinetics papers from Nav-density papers.** Rate functions (activation m_inf, tau_m,
  inactivation h_inf, tau_h) and conductance densities (g_Na peak in S/cm^2) are two distinct
  priors; each should have a dedicated source paper.
* **Classical reviews anchor the subunit-expression literature.** Nav1.6 at the AIS has a canonical
  set of reviews (Kole-Stuart, Hu et al.) that are frequently cited as prior sources.

## Gaps and Limitations

* No Nav subunit localisation paper in the existing corpus (Nav1.1/Nav1.2/Nav1.6 distributions).
* No Kv subunit localisation paper in the existing corpus.
* No HH-family kinetic-model paper dedicated to RGC Nav/Kv in the existing corpus.
* No subunit-combination paper for specific RGC types.
* No conductance-density paper quantifying Nav/Kv density in S/cm^2 by compartment.

## Recommendations for This Task

1. Target 5 canonical papers, one for each gap enumerated above.
2. Prefer paywalled classics that are widely cited - the abstract plus training-knowledge summary
   pattern already validated in t0015-t0018 handles them without PDF retrieval. Paywalled DOIs are
   recorded in `intervention/paywalled_papers.md`.
3. Primary category is `voltage-gated-channels`; add a secondary tag from `retinal-ganglion-cell`,
   `patch-clamp`, or `compartmental-modeling` per theme.
4. Verify every candidate DOI is not in t0002, t0015, t0016, t0017, or t0018 before adding it.
5. The answer asset must tabulate Nav/Kv subunit combinations (activation/inactivation kinetics,
   conductance-density ranges by compartment) with source DOIs so downstream Na/K optimisation tasks
   can cite them directly.

## Paper Index

### [Taylor2014]

* **Title**: Direction-selective ganglion cell calcium imaging
* **Authors**: Taylor, W. R., et al.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Task**: t0002
* **Relevance**: DSGC output-level spike behaviour; relevant for validating that chosen Nav/Kv
  combinations reproduce measured firing patterns, but provides no channel-level priors.

### [Sivyer2013]

* **Title**: Patch-clamp recordings of DSGC spike-train tuning
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1113/jphysiol.2010.192716`
* **Task**: t0002
* **Relevance**: Preferred-direction peak AP rate around 80-150 Hz; output-level validation target
  for the Nav/Kv parameter fit, not a source of channel priors.

### [Rall1967]

* **Title**: Distinguishing theoretical synaptic potentials
* **Authors**: Rall, W.
* **Year**: 1967
* **DOI**: `10.1152/jn.1967.30.5.1138`
* **Task**: t0015
* **Relevance**: Passive cable theory; foundational but predates voltage-gated-channel densities in
  dendrites.
