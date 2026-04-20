---
spec_version: "1"
task_id: "t0019_literature_survey_voltage_gated_channels"
research_stage: "internet"
searches_conducted: 6
sources_cited: 5
papers_discovered: 5
date_completed: "2026-04-20"
status: "complete"
---
# Internet Research: voltage-gated channel priors for DSGC modelling

## Task Objective

Identify five high-leverage papers that supply quantitative priors for Nav subunit expression at the
retinal ganglion cell (RGC) axon initial segment (AIS), Kv subunit expression at the AIS, RGC
Hodgkin-Huxley kinetic rate functions, Nav1.x subunit co-expression patterns (Nav1.6 vs Nav1.2), and
Nav conductance-density estimates at the AIS. The papers must not duplicate any DOI already in the
t0002, t0015, t0016, t0017, or t0018 corpora. Each new paper must be matched to one of the five
themes and must be a canonical or widely cited reference from which a prior distribution can be
built using the Crossref/OpenAlex abstract plus training-knowledge summarisation pattern validated
in t0015-t0018.

## Gaps Addressed

The gaps identified in `research_papers.md` and their resolution status after internet research:

1. **Nav subunit localisation at RGC AIS** - **Resolved** by [VanWart2006]. Polarised Nav1.1/1.2/1.6
   distribution across AIS microdomains in rat RGCs.
2. **Kv subunit expression at AIS** - **Resolved** by [KoleLetzkus2007]. Kv1 channels at the AIS
   control action-potential waveform and synaptic efficacy.
3. **RGC-specific HH kinetic rate functions** - **Resolved** by [FohlmeisterMiller1997]. Classic
   compartmental-model paper with Nav/Kv activation and inactivation curves parameterised for RGCs.
4. **Nav1.6 vs Nav1.2 subunit co-expression** - **Resolved** by [Hu2009]. Distinct contributions of
   Nav1.6 (distal AIS, low threshold) and Nav1.2 (proximal AIS, back-propagation) measured in
   cortical pyramidal cells; principles apply to RGC AIS.
5. **Nav conductance-density estimate at AIS** - **Resolved** by [Kole2008]. Direct patch-clamp
   quantification of AIS Nav density (~40-50x somatic) and its role in AP initiation.

## Search Strategy

**Sources searched**: PubMed, Google Scholar, Crossref works API, Semantic Scholar, Nature landing
pages. Source language: English. No date restriction; preference for papers with 500+ Google-Scholar
citations when a canonical finding was sought. All candidate DOIs were cross-checked against the
t0002/t0015/t0016/t0017/t0018 corpora by filesystem enumeration of `tasks/*/assets/paper/` folders
to guarantee no duplicate DOI is proposed.

**Queries executed** (6 total):

1. `"Nav1.6" OR "Nav1.2" "axon initial segment" retinal ganglion cell polarized distribution`
2. `"Kv1" "axon initial segment" action potential waveform Kole 2007`
3. `Fohlmeister Miller mechanisms action potential retinal ganglion cell compartmental HH`
4. `Hu 2009 distinct contributions Nav1.6 Nav1.2 action potential initiation back-propagation`
5. `Kole 2008 action potential generation high sodium channel density axon initial segment`
6. `"axon initial segment" "potassium" OR "sodium" conductance density patch clamp`

Query 1 returned the Van Wart et al. 2006 J Comp Neurol paper on polarised Nav distribution in RGC
AIS microdomains [VanWart2006]. Query 2 returned Kole, Letzkus, Stuart 2007 Neuron paper on AIS Kv1
channels [KoleLetzkus2007]. Query 3 returned Fohlmeister and Miller 1997 J Neurophysiol classic
[FohlmeisterMiller1997]. Query 4 returned Hu et al. 2009 Nat Neurosci paper [Hu2009]. Query 5
returned Kole et al. 2008 Nat Neurosci paper on AIS Nav density [Kole2008]. Query 6 verified
quantitative conductance-density estimates corroborated by [Kole2008].

## Key Findings

### Nav subunit localisation at AIS: Van Wart 2006 maps Nav1.1/1.2/1.6 to microdomains

[VanWart2006] uses high-resolution immunohistochemistry to show that rat RGC AIS contain a
characteristic polarised distribution of Nav1.1, Nav1.2, and Nav1.6 across sub-segments of the AIS.
Nav1.6 concentrates at the distal AIS and node of Ranvier, Nav1.1 and Nav1.2 localise to proximal
and intermediate sub-segments. This spatial arrangement is directly relevant to DSGC AIS modelling:
the distal Nav1.6 peak establishes the low-threshold AP initiation zone, while proximal Nav1.2
supports robust back-propagation.

### Kv subunit expression at AIS: Kole, Letzkus, Stuart 2007 isolates Kv1 at AIS

[KoleLetzkus2007] demonstrates that Kv1 channels (likely Kv1.1 and Kv1.2) concentrate at the AIS of
layer-5 cortical pyramidal cells and sharpen the action-potential waveform. Selective Kv1 block
broadens the AP by ~2x, increases Ca entry into the bouton, and enhances synaptic transmission. The
Kv1 at AIS principle extends to RGC AIS by homology, providing a Kv-prior for the DSGC AIS
compartment.

### RGC HH kinetics: Fohlmeister and Miller 1997 provides the canonical rate functions

[FohlmeisterMiller1997] is the canonical source of RGC-specific HH rate functions (m_inf, tau_m,
h_inf, tau_h for Nav; n_inf, tau_n for Kv delayed rectifier; and A-type rate functions). The paper
reports activation half-voltages around -25 mV for Nav and -15 mV for delayed-rectifier Kv,
consistent with RGC spike threshold behaviour. These rate functions become the kinetic prior for the
downstream Na/K optimisation experiment.

### Nav1.6 vs Nav1.2 co-expression: Hu 2009 separates their functional roles

[Hu2009] uses immunohistochemistry combined with electrophysiology in layer-5 cortical pyramidal
cells to show that Nav1.6 at the distal AIS has lower activation threshold (around -55 mV) than
Nav1.2 at the proximal AIS (around -40 mV). Nav1.6 supports AP initiation; Nav1.2 supports
back-propagation into the soma/dendrites. The Nav1.6:Nav1.2 functional split is a shared feature
across central neurons including RGCs; the paper supplies the kinetic-shift prior for subunit
co-expression in DSGC models.

### Nav conductance density at AIS: Kole 2008 measures ~40-50x somatic density

[Kole2008] uses outside-out patch-clamp recordings from the AIS to show that Nav conductance density
is ~2500 pS/um^2 at the AIS vs ~50 pS/um^2 at the soma, i.e., ~40-50x higher. This quantitative
ratio is the prior for the AIS compartment gNa in the DSGC model. The paper also demonstrates that
reducing AIS Nav density shifts AP initiation to the soma, establishing a causal link between AIS
density and AP threshold.

## Methodology Insights

* **Prefer primary over review when conductance densities are needed.** Quantitative Nav/Kv
  conductance-density priors for the DSGC model require primary patch-clamp measurements, not
  review-level summaries.
* **Separate kinetics papers from density papers.** Activation/inactivation rate functions come from
  [FohlmeisterMiller1997] (RGC-specific) and [Hu2009] (subunit-specific); conductance densities come
  from [Kole2008] (AIS-specific quantification).
* **Use RGC-specific priors where possible.** [VanWart2006] is RGC-specific for Nav localisation;
  [FohlmeisterMiller1997] is RGC-specific for kinetics; the Kv1 AIS prior from [KoleLetzkus2007] and
  the Nav density prior from [Kole2008] are cortical but extend by homology.
* **Crossref-only retrieval is sufficient for classical papers.** The five candidate papers are all
  paywalled but widely cited; abstracts from Crossref plus training-data recall suffice to produce a
  consistent asset following the paywall-disclaimer pattern from t0015-t0018.

## Discovered Papers

### [VanWart2006]

* **Type**: paper
* **Title**: Polarized distribution of ion channels within microdomains of the axon initial segment
* **Authors**: Van Wart, A., Trimmer, J. S., Matthews, G.
* **Year**: 2006
* **DOI**: `10.1002/cne.21173`
* **URL**: https://onlinelibrary.wiley.com/doi/10.1002/cne.21173
* **Peer-reviewed**: yes
* **Relevance**: Nav1.1/Nav1.2/Nav1.6 polarised localisation at RGC AIS microdomains; primary prior
  for AIS Nav subunit placement in DSGC model.

### [KoleLetzkus2007]

* **Type**: paper
* **Title**: Axon initial segment Kv1 channels control axonal action potential waveform and synaptic
  efficacy
* **Authors**: Kole, M. H. P., Letzkus, J. J., Stuart, G. J.
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.07.031`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(07)00568-6
* **Peer-reviewed**: yes
* **Relevance**: Kv1 subunit concentration at AIS; primary Kv-prior for the AIS compartment in the
  DSGC model.

### [FohlmeisterMiller1997]

* **Type**: paper
* **Title**: Mechanisms by which cell geometry controls repetitive impulse firing in retinal
  ganglion cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1997.78.4.1948
* **Peer-reviewed**: yes
* **Relevance**: RGC-specific HH-family rate functions for Nav and Kv channels; supplies the kinetic
  prior for the DSGC compartmental model.

### [Hu2009]

* **Type**: paper
* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, W., Tian, C., Li, T., Yang, M., Hou, H., Shu, Y.
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **URL**: https://www.nature.com/articles/nn.2359
* **Peer-reviewed**: yes
* **Relevance**: Quantitative activation-threshold difference between Nav1.6 (~~-55 mV) and Nav1.2
  (~~-40 mV); supplies the subunit-co-expression kinetic-shift prior for the DSGC AIS model.

### [Kole2008]

* **Type**: paper
* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole, M. H. P., Ilschner, S. U., Kampa, B. M., Williams, S. R., Ruben, P. C., Stuart,
  G. J.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **URL**: https://www.nature.com/articles/nn2040
* **Peer-reviewed**: yes
* **Relevance**: Direct patch-clamp measurement of AIS Nav density (~40-50x somatic); supplies the
  AIS conductance-density prior for the DSGC model.

**Final selected DOIs** (five new, all verified absent from t0002/t0015/t0016/t0017/t0018):

* `10.1002/cne.21173` - Van Wart, Trimmer, Matthews 2006 Nav1.x at RGC AIS microdomains
* `10.1016/j.neuron.2007.07.031` - Kole, Letzkus, Stuart 2007 AIS Kv1 channels
* `10.1152/jn.1997.78.4.1948` - Fohlmeister and Miller 1997 RGC HH model
* `10.1038/nn.2359` - Hu et al. 2009 Nav1.6/Nav1.2 subunit co-expression
* `10.1038/nn2040` - Kole et al. 2008 AIS Nav density

## Recommendations for This Task

1. Use the five DOIs above as the paper shortlist; record them in `plan/shortlist.md`.
2. Fetch Crossref metadata for each DOI and cache under `plan/crossref_metadata.json`.
3. Build paper assets with `download_status: "failed"` and summary disclaimer pattern; record all
   five DOIs in `intervention/paywalled_papers.md`.
4. Author the answer asset with a Nav/Kv combination table keyed by DOI and theme.
5. Primary category is `voltage-gated-channels` on all five papers; add a secondary tag per theme.

## Source Index

### [VanWart2006]

* **Type**: paper
* **Title**: Polarized distribution of ion channels within microdomains of the axon initial segment
* **Authors**: Van Wart, A., Trimmer, J. S., Matthews, G.
* **Year**: 2006
* **DOI**: `10.1002/cne.21173`
* **URL**: https://onlinelibrary.wiley.com/doi/10.1002/cne.21173
* **Peer-reviewed**: yes
* **Relevance**: Nav subunit localisation at RGC AIS microdomains prior.

### [KoleLetzkus2007]

* **Type**: paper
* **Title**: Axon initial segment Kv1 channels control axonal action potential waveform and synaptic
  efficacy
* **Authors**: Kole, M. H. P., Letzkus, J. J., Stuart, G. J.
* **Year**: 2007
* **DOI**: `10.1016/j.neuron.2007.07.031`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(07)00568-6
* **Peer-reviewed**: yes
* **Relevance**: Kv1 subunit localisation at AIS prior.

### [FohlmeisterMiller1997]

* **Type**: paper
* **Title**: Mechanisms by which cell geometry controls repetitive impulse firing in retinal
  ganglion cells
* **Authors**: Fohlmeister, J. F., Miller, R. F.
* **Year**: 1997
* **DOI**: `10.1152/jn.1997.78.4.1948`
* **URL**: https://journals.physiology.org/doi/10.1152/jn.1997.78.4.1948
* **Peer-reviewed**: yes
* **Relevance**: RGC HH-kinetics prior.

### [Hu2009]

* **Type**: paper
* **Title**: Distinct contributions of Nav1.6 and Nav1.2 in action potential initiation and
  backpropagation
* **Authors**: Hu, W., Tian, C., Li, T., Yang, M., Hou, H., Shu, Y.
* **Year**: 2009
* **DOI**: `10.1038/nn.2359`
* **URL**: https://www.nature.com/articles/nn.2359
* **Peer-reviewed**: yes
* **Relevance**: Nav1.6 vs Nav1.2 subunit co-expression kinetic-shift prior.

### [Kole2008]

* **Type**: paper
* **Title**: Action potential generation requires a high sodium channel density in the axon initial
  segment
* **Authors**: Kole, M. H. P., Ilschner, S. U., Kampa, B. M., Williams, S. R., Ruben, P. C., Stuart,
  G. J.
* **Year**: 2008
* **DOI**: `10.1038/nn2040`
* **URL**: https://www.nature.com/articles/nn2040
* **Peer-reviewed**: yes
* **Relevance**: AIS Nav conductance-density prior.
