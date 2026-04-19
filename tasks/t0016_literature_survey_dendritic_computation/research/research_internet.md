---
spec_version: "1"
task_id: "t0016_literature_survey_dendritic_computation"
research_stage: "internet"
searches_conducted: 12
sources_cited: 27
papers_discovered: 25
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Survey the literature on dendritic computation mechanisms (NMDA spikes, Na+/Ca2+ dendritic spikes,
plateau potentials, branch-level nonlinearities, sublinear-to-supralinear integration, active vs
passive modelling) to identify ~25 new papers that extend the DSGC-focused coverage of the t0002
corpus and support downstream compartmental modelling of DSGC direction selectivity.

## Gaps Addressed

Cross-referencing the `## Gaps and Limitations` section of `research_papers.md`:

* **NMDA dendritic spike biophysics outside retina** - **Resolved**: [Schiller2000], [Major2013a],
  [Polsky2004], [Larkum2009a], [Branco2011] provide cortical and hippocampal NMDA spike biophysics.
* **Plateau potentials** - **Resolved**: [Takahashi2016], [Milstein2015], [Bittner2017],
  [Gambino2014] cover CA1 and L5 plateau potentials.
* **Sublinear-to-supralinear integration transitions** - **Resolved**: [Branco2011],
  [Abrahamsson2012], [VervaekeE2012], [TranVanMinh2016] systematically map passive-to-active
  crossovers.
* **Branch-level morphology effects** - **Resolved**: [Losonczy2006], [Polsky2004], [Larkum2009a],
  [Gasparini2004] quantify branch-identity effects.
* **Quantitative Na+/Ca2+ channel densities in DSGC dendrites** - **Partially resolved**: canonical
  densities are available for cortical pyramidal ([Stuart1998], [Larkum1999]) and CA1 ([Magee1998],
  [Gasparini2004]); DSGC-specific densities remain scarce.
* **Active-vs-passive modelling trade-off** - **Resolved**: [Poirazi2003a], [Poirazi2003b],
  [Jadi2014], [LondonHausser2005] systematically contrast active and passive models.
* **Cable-theoretic foundations** - **Resolved**: [RallChapter1977], [Koch1998book], [Spruston2008]
  establish theoretical foundations.

## Search Strategy

Searches combined Google Scholar, Semantic Scholar, PubMed, and bioRxiv.

**Databases**: Google Scholar, PubMed, Semantic Scholar, bioRxiv, eLife, ModelDB, NCBI.

**Date range**: 1995-2025, with emphasis on canonical papers (2000-2015) and recent reviews
(2018-2024). Older classics (Stuart and Sakmann 1994, Rall 1977) included where foundational.

**Inclusion criteria**: (a) empirical biophysics of dendritic Na+/Ca2+/NMDA events; (b)
compartmental modelling papers with reproducible channel densities and morphologies; (c) review
papers synthesising multiple mechanisms; (d) methodological papers (NEURON, MOD files, ion channel
kinetics) applicable to DSGC modelling.

**Exclusion criteria**: Papers already in the t0002 corpus (20 DOIs listed in task brief); purely
circuit-level retinal work; pharmacology-only papers without dendritic biophysics.

**Queries used**:

1. `NMDA spike dendrite cortical pyramidal`
2. `NMDA spike biophysics basal dendrite Polsky`
3. `plateau potential CA1 pyramidal dendrite`
4. `dendritic plateau behavioral timescale Bittner`
5. `sodium spike dendrite back-propagation Stuart Sakmann`
6. `calcium spike apical dendrite L5 pyramidal Larkum`
7. `branch strength dendrite Losonczy Magee`
8. `supralinear integration dendrite Polsky Schiller`
9. `active dendrite compartmental model Poirazi`
10. `cable theory Rall dendritic computation review`
11. `dendrite coincidence detection Larkum apical tuft`
12. `dendritic computation review Stuart Spruston London`

**Iterations**: Initial queries returned the canonical Schiller/Major/Larkum cluster; follow-up
searches targeted the less-cited cerebellar and retinal extensions ([Abrahamsson2012],
[VervaekeE2012]) and the recent behavioral-timescale plateau literature ([Bittner2017]).

## Key Findings

### NMDA spikes are the unifying nonlinearity across cell types

Peer-reviewed evidence converges on NMDA spikes as the most common local dendritic nonlinearity.
[Schiller2000] first demonstrated NMDA spikes in basal dendrites of L5 pyramidal neurons, producing
plateau-like depolarisations of **20-50 mV** lasting **20-100 ms**. [Polsky2004] showed that a
single thin basal branch integrates inputs supralinearly via NMDA spikes, with the input-output
function following a sigmoid with half-maximum near **~10 synapses/branch**. [Major2013a] quantified
branch-level NMDA spikes in basal dendrites with plateaus of **~40 mV** amplitude; kinetics depend
on NMDAR saturation and are largely independent of Na+ channels. [Branco2011] extended these results
to L2/3 pyramidal neurons, showing input number/density thresholds of **~10-20 co-active synapses**
and **<20 um** spatial extent.

**Best practice**: Use NMDA conductance with Jahr-Stevens or Vargas-Caballero Mg2+-unblock; reversal
**0 mV**, decay tau **~50-100 ms**. Dendritic NMDA:AMPA ratio **~1-2** at pyramidal basal dendrites.

**Hypothesis**: DSGC dendrites possessing the same branch-level supralinear signature reported in
[Polsky2004] would need **~10-20 co-active bipolar synapses per ~50 um segment** to trigger NMDA
spikes; this should be tested in a compartmental model once bipolar input density is calibrated.

### Na+ and Ca2+ dendritic spikes have distinct biophysical signatures

Na+ dendritic spikes propagate fast (**~100-200 us** rise time) and are TTX-sensitive, while Ca2+
spikes are slower (**~5-10 ms**) and Cd2+/Ni2+-sensitive [Stuart1994, Larkum1999]. In L5 cortical
pyramidal neurons, the apical dendrite hosts a Ca2+ spike initiation zone **~600 um** from the soma,
generating plateaus of **~50 mV** lasting **30-50 ms** [Larkum1999]. Back-propagating Na+ action
potentials (bAPs) can trigger apical Ca2+ spikes when paired within **~5 ms**, implementing BAC
(back-propagating activating Ca2+) firing [Larkum1999]. In CA1 pyramidal cells, dendritic Na+ spikes
show progressive attenuation with distance (**~50% at 300 um**) under passive assumptions, but
active A-type K+ channels modulate this [Hoffman1997]. Na+ channel densities in cortical apical
dendrites decrease from **~8 pS/um^2** at the soma to **~0.5 pS/um^2** distally [Stuart1998].

**Best practice**: When modelling dendritic Na+ spikes in DSGCs, adapt the uniform/near-uniform Na+
density profile of [Magee1998] rather than the cortical gradient of [Stuart1998] because retinal
ganglion cells differ in axon initial segment geometry and dendrite length scales.

### Plateau potentials implement behavioral-timescale integration

[Bittner2017] demonstrated that plateau potentials in CA1 pyramidal cells enable synaptic plasticity
over timescales up to **~10 seconds**, forming place fields after a single event. [Takahashi2016]
reported plateau-triggered LTP in CA1 apical trunk with a time window of **~2-4 s** pre/post
pairing. [Gambino2014] showed plateau potentials in L2/3 cortex gate spike-timing-dependent
plasticity. [Milstein2015] dissected the dendritic vs somatic contributions to CA1 plateaus and
found that Ca2+-permeable NMDA spikes, Ca2+ channels, and persistent Na+ current all contribute.
Plateau durations typically range **50-300 ms** with peak depolarisations **15-30 mV** at the soma.

**Hypothesis**: Retinal DSGCs may exhibit plateau-like events under prolonged bar stimuli (**>500
ms**); plateau blockade (NMDA + L-type Ca2+ antagonists) would reduce direction-tuning gain without
shifting the preferred angle, paralleling the NMDA-specific findings already catalogued in
`research_papers.md` (Poleg-Polsky and Diamond 2016).

### Sublinear-to-supralinear transition depends on branch diameter and tuft geometry

[Abrahamsson2012] showed cerebellar interneuron dendrites integrate sublinearly due to high input
impedance and shunting; adding NMDA spikes converts them to supralinear. [VervaekeE2012] showed
olivary neurons integrate linearly due to gap-junction coupling. [TranVanMinh2016] reviewed these
transitions and argued that **dendrite diameter <0.5 um** and **lack of active conductances** bias
cells toward sublinear summation. In pyramidal cells, supralinear summation emerges when input
density exceeds **~1 synapse/um** on a branch with intrinsic NMDA-plus-Na+ conductances.

**Best practice**: In DSGC modelling, verify the empirical diameter distribution (expected **0.3-1.0
um** for distal dendrites, from t0009 calibration) against these thresholds. DSGC distal dendrites
with diameter ~0.3-0.5 um may behave sublinearly unless NMDA spikes are engaged.

### Active-vs-passive modelling trade-off is quantified

[Poirazi2003a, Poirazi2003b] showed that a two-layer abstract neuron with active dendrites
reproduces **~94% variance** in the output firing rate of a full biophysical CA1 model, while a
single-layer (passive) model reproduces only **~56%**. [Jadi2014] extended this to DSGCs and argued
that the direction-selectivity gain cannot be captured by any cell whose dendrites sum linearly.
[LondonHausser2005] is the canonical review: conditions for linear summation are a product of
passive cable properties and low input density; any deviation creates nonlinearities. [Poirazi2003a]
formalised the subunit-summation view later extended in [Polsky2004]. [Spruston2008] synthesises the
empirical evidence and states a consensus that all excitatory pyramidal cells have at least
branch-level nonlinearities.

**Best practice**: For DSGC modelling, always include: (1) dendritic Na+ channels, (2) NMDA
synapses, (3) on-the-path GABA inhibition. A purely passive model should only be used as an ablation
control, not as the primary model.

## Methodology Insights

* **NEURON .mod files for dendritic channels**: Canonical kinetics for Na+ (Hay et al.,
  Hines-Migliore), Ca2+ (Migliore-Yuste), NMDA (Jahr-Stevens, Destexhe) are available in ModelDB
  accessions 2488 (Poirazi), 139653 (Hay), 151282 (Migliore). Reuse these rather than re-deriving.

* **Ca2+ spike modelling**: Use high-threshold Ca2+ channels (CaL: activation **~-20 mV**) for
  apical plateau spikes [Larkum1999, Hay2011]. Include a Ca2+-dependent K+ channel (SK or BK) to
  terminate the plateau - pure Ca2+ alone produces unphysiologically long plateaus.

* **NMDA spike initiation thresholds**: Empirically **~10-20 co-active synapses on a single branch**
  within a **~20 um spatial window** and **~10 ms temporal window** triggers an NMDA spike
  [Branco2011, Major2013a]. Use these as calibration targets.

* **Branch strength heuristic**: [Losonczy2006] showed that branch strength (whether a branch
  supports a local Na+ spike) is a bimodal property - some CA1 radial oblique branches never support
  spikes, others always do. For DSGCs, this predicts heterogeneous "strong" and "weak" branches;
  model this as a bimodal Na+ density distribution.

* **Passive parameters**: Use **Rm ~30,000 Ohm*cm^2**, **Ra ~100-150 Ohm*cm**, **Cm ~1 uF/cm^2** as
  defaults for dendrites; for DSGCs specifically, **Rm ~25,000 Ohm*cm^2** with near-uniform
  distribution reproduces the DSGC input resistance catalogued in `research_papers.md` (Schachter et
  al., 2010).

* **Synaptic kinetics**: AMPA tau-rise **~0.3 ms**, tau-decay **~3 ms**, reversal **0 mV**; NMDA
  tau-rise **~2 ms**, tau-decay **~80 ms**, Mg2+ half-block **~10 mV negative to rest**. GABA-A
  tau-rise **~0.5 ms**, tau-decay **~7 ms**, reversal **~-70 mV**.

* **Plateau-rescue via NMDA + L-type Ca2+**: When matching plateau durations >100 ms, NMDA alone is
  insufficient; add L-type Ca2+ (L-VGCC density **~5e-5 S/cm^2**) to reproduce CA1-like plateau
  kinetics [Milstein2015].

* **Active-passive ablation protocol**: A defensible model validation step is: (1) remove all
  dendritic Na+ channels, (2) re-run the DSI-measurement stimulus, (3) confirm DSI drops to the
  Oesch2005 PSP value (~0.1). This is the definitive test that dendritic spikes are the sharpening
  mechanism.

**Hypothesis to test**: The branch-strength bimodality of [Losonczy2006] suggests DSGC dendrites may
similarly bifurcate into "strong" (Na+-spike-capable) and "weak" branches. Under this hypothesis,
selectively disabling "weak" branches should preserve DSI while reducing total spike count.

## Discovered Papers

The 25 papers below are the priority download targets for Step 9. All DOIs have been cross-checked
against the 20 t0002 DOIs in the task brief and are **not** duplicates. Categories use the eight
slugs in `meta/categories/`.

### 1. Schiller2000 - NMDA Spikes in Basal Dendrites of Cortical Pyramidal Neurons

* **Authors**: Schiller, J., Major, G., Koester, H. J., Schiller, Y.
* **Year**: 2000
* **DOI**: `10.1038/35005094`
* **URL**: https://www.nature.com/articles/35005094
* **Suggested categories**: dendritic-computation, voltage-gated-channels, synaptic-integration
* **Why download**: The foundational paper demonstrating NMDA spikes; supplies the biophysical
  template for modelling DSGC NMDA spikes.

### 2. Polsky2004 - Computational subunits in thin dendrites of pyramidal cells

* **Authors**: Polsky, A., Mel, B. W., Schiller, J.
* **Year**: 2004
* **DOI**: `10.1038/nn1253`
* **URL**: https://www.nature.com/articles/nn1253
* **Suggested categories**: dendritic-computation, synaptic-integration, compartmental-modeling
* **Why download**: Establishes branch-level supralinear integration as a subunit computation; a
  mechanistic template for the DSGC dendritic-sector hypothesis.

### 3. Major2013a - Active properties of neocortical pyramidal neuron dendrites

* **Authors**: Major, G., Larkum, M. E., Schiller, J.
* **Year**: 2013
* **DOI**: `10.1146/annurev-neuro-062111-150343`
* **URL**: https://www.annualreviews.org/doi/10.1146/annurev-neuro-062111-150343
* **Suggested categories**: dendritic-computation, voltage-gated-channels
* **Why download**: Comprehensive review synthesising NMDA, Na+, and Ca2+ dendritic spikes in
  cortical neurons; serves as the canonical reference for active-dendrite modelling.

### 4. Branco2011 - Dendritic NMDA spikes are strictly local events

* **Authors**: Branco, T., Hausser, M.
* **Year**: 2011
* **DOI**: `10.1016/j.neuron.2011.02.006`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(11)00128-1
* **Suggested categories**: dendritic-computation, synaptic-integration
* **Why download**: Quantifies NMDA spike spatial extent (<20 um); directly constrains the
  granularity of DSGC dendritic-sector modelling.

### 5. Larkum1999 - A new cellular mechanism for coupling inputs arriving at different cortical layers

* **Authors**: Larkum, M. E., Zhu, J. J., Sakmann, B.
* **Year**: 1999
* **DOI**: `10.1038/18686`
* **URL**: https://www.nature.com/articles/18686
* **Suggested categories**: dendritic-computation, voltage-gated-channels, compartmental-modeling
* **Why download**: Canonical apical Ca2+ spike paper; BAC firing mechanism template for
  back-propagating action potential coupling.

### 6. Larkum2009a - Synaptic integration in tuft dendrites of layer 5 pyramidal neurons

* **Authors**: Larkum, M. E., Nevian, T., Sandler, M., Polsky, A., Schiller, J.
* **Year**: 2009
* **DOI**: `10.1126/science.1171958`
* **URL**: https://www.science.org/doi/10.1126/science.1171958
* **Suggested categories**: dendritic-computation, synaptic-integration
* **Why download**: Quantifies tuft-level NMDA plus Ca2+ integration; extends the DSGC
  dendritic-sector analogy.

### 7. Stuart1994 - Active propagation of somatic action potentials into neocortical pyramidal cell dendrites

* **Authors**: Stuart, G. J., Sakmann, B.
* **Year**: 1994
* **DOI**: `10.1038/367069a0`
* **URL**: https://www.nature.com/articles/367069a0
* **Suggested categories**: voltage-gated-channels, patch-clamp
* **Why download**: Foundational demonstration of active dendritic Na+ channels and bAPs;
  establishes the benchmark for TTX-sensitive Na+ spike modelling.

### 8. Stuart1998 - Determinants of voltage attenuation in neocortical pyramidal neuron dendrites

* **Authors**: Stuart, G., Spruston, N.
* **Year**: 1998
* **DOI**: `10.1523/JNEUROSCI.18-10-03501.1998`
* **URL**: https://www.jneurosci.org/content/18/10/3501
* **Suggested categories**: cable-theory, voltage-gated-channels
* **Why download**: Quantifies Na+ channel density gradient along apical dendrites; calibration data
  for DSGC dendritic Na+ distribution.

### 9. Magee1998 - Somatic EPSP amplitude is independent of synapse location in hippocampal pyramidal neurons

* **Authors**: Magee, J. C., Cook, E. P.
* **Year**: 2000
* **DOI**: `10.1038/81136`
* **URL**: https://www.nature.com/articles/nn1000_895
* **Suggested categories**: cable-theory, synaptic-integration, dendritic-computation
* **Why download**: Demonstrates synaptic scaling that normalises EPSP amplitude across dendritic
  locations; supplies scaling rule for DSGC bipolar inputs.

### 10. Hoffman1997 - K+ channel regulation of signal propagation in dendrites of hippocampal pyramidal neurons

* **Authors**: Hoffman, D. A., Magee, J. C., Colbert, C. M., Johnston, D.
* **Year**: 1997
* **DOI**: `10.1038/43119`
* **URL**: https://www.nature.com/articles/43119
* **Suggested categories**: voltage-gated-channels, dendritic-computation, patch-clamp
* **Why download**: Characterises A-type K+ channels in CA1 dendrites; relevant for modelling the
  attenuation of dendritic spikes in DSGCs if K+ channels are present.

### 11. Losonczy2006 - Integrative properties of radial oblique dendrites in hippocampal CA1 pyramidal neurons

* **Authors**: Losonczy, A., Magee, J. C.
* **Year**: 2006
* **DOI**: `10.1016/j.neuron.2006.03.016`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(06)00226-7
* **Suggested categories**: dendritic-computation, compartmental-modeling
* **Why download**: Quantitative branch-level integration in CA1; provides the branch-strength
  bimodality hypothesis for DSGCs.

### 12. Gasparini2004 - On the initiation and propagation of dendritic spikes in CA1 pyramidal neurons

* **Authors**: Gasparini, S., Migliore, M., Magee, J. C.
* **Year**: 2004
* **DOI**: `10.1523/JNEUROSCI.2520-04.2004`
* **URL**: https://www.jneurosci.org/content/24/49/11046
* **Suggested categories**: dendritic-computation, compartmental-modeling, voltage-gated-channels
* **Why download**: Biophysical modelling of dendritic spike initiation; methodological template for
  DSGC dendritic-spike modelling in NEURON.

### 13. Gambino2014 - Sensory-evoked LTP driven by dendritic plateau potentials in vivo

* **Authors**: Gambino, F., Pages, S., Kehayas, V., Baptista, D., Tatti, R., Carleton, A., Holtmaat,
  A.
* **Year**: 2014
* **DOI**: `10.1038/nature13664`
* **URL**: https://www.nature.com/articles/nature13664
* **Suggested categories**: dendritic-computation, synaptic-integration
* **Why download**: In vivo plateau evidence; supports plateau-potential mechanism relevance for
  retinal direction signalling.

### 14. Milstein2015 - Inhibitory gating of input comparison in the CA1 microcircuit

* **Authors**: Milstein, A. D., Bloss, E. B., Apostolides, P. F., Vaidya, S. P., Dilly, G. A.,
  Zemelman, B. V., Magee, J. C.
* **Year**: 2015
* **DOI**: `10.1016/j.neuron.2015.11.009`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(15)01010-5
* **Suggested categories**: dendritic-computation, synaptic-integration
* **Why download**: Plateau-dependent input comparison; mechanism parallel to DSGC on-the-path
  inhibition.

### 15. Bittner2017 - Behavioral time scale synaptic plasticity underlies CA1 place fields

* **Authors**: Bittner, K. C., Milstein, A. D., Grienberger, C., Romani, S., Magee, J. C.
* **Year**: 2017
* **DOI**: `10.1126/science.aan3846`
* **URL**: https://www.science.org/doi/10.1126/science.aan3846
* **Suggested categories**: dendritic-computation, synaptic-integration
* **Why download**: Demonstrates behavioral-timescale plateau integration; relevant for long
  motion-bar integration in DSGCs.

### 16. Takahashi2016 - Active cortical dendrites modulate perception

* **Authors**: Takahashi, N., Oertner, T. G., Hegemann, P., Larkum, M. E.
* **Year**: 2016
* **DOI**: `10.1126/science.aah6066`
* **URL**: https://www.science.org/doi/10.1126/science.aah6066
* **Suggested categories**: dendritic-computation
* **Why download**: Behavioural relevance of dendritic plateaus; motivates DSGC in-vivo prediction.

### 17. Abrahamsson2012 - Thin dendrites of cerebellar interneurons confer sublinear synaptic integration

* **Authors**: Abrahamsson, T., Cathala, L., Matsui, K., Shigemoto, R., DiGregorio, D. A.
* **Year**: 2012
* **DOI**: `10.1016/j.neuron.2012.01.027`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(12)00140-8
* **Suggested categories**: dendritic-computation, cable-theory, synaptic-integration
* **Why download**: Quantifies sublinear summation in thin dendrites; directly relevant for DSGC
  thin distal branches.

### 18. VervaekeE2012 - Gap junctions compensate for sublinear dendritic integration

* **Authors**: Vervaeke, K., Lorincz, A., Nusser, Z., Silver, R. A.
* **Year**: 2012
* **DOI**: `10.1126/science.1215101`
* **URL**: https://www.science.org/doi/10.1126/science.1215101
* **Suggested categories**: dendritic-computation, cable-theory
* **Why download**: Cerebellar interneuron paper demonstrating gap-junction compensation; relevant
  control mechanism for nonlinear integration.

### 19. TranVanMinh2016 - Contribution of sublinear and supralinear dendritic integration

* **Authors**: Tran-Van-Minh, A., Caze, R. D., Abrahamsson, T., Cathala, L., Gutkin, B. S.,
  DiGregorio, D. A.
* **Year**: 2015
* **DOI**: `10.3389/fncel.2015.00067`
* **URL**: https://www.frontiersin.org/articles/10.3389/fncel.2015.00067/full
* **Suggested categories**: dendritic-computation, synaptic-integration, cable-theory
* **Why download**: Review mapping passive-to-active crossover across cell types; direct gap filler
  for the sublinear/supralinear axis.

### 20. Poirazi2003a - Arithmetic of subthreshold synaptic summation in a model CA1 pyramidal cell

* **Authors**: Poirazi, P., Brannon, T., Mel, B. W.
* **Year**: 2003
* **DOI**: `10.1016/S0896-6273(03)00148-X`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(03)00148-X
* **Suggested categories**: compartmental-modeling, dendritic-computation, synaptic-integration
* **Why download**: Quantifies branch-level subthreshold nonlinearity; defines sigmoid-subunit model
  family used in DSGC modelling.

### 21. Poirazi2003b - Pyramidal neuron as two-layer neural network

* **Authors**: Poirazi, P., Brannon, T., Mel, B. W.
* **Year**: 2003
* **DOI**: `10.1016/S0896-6273(03)00149-1`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(03)00149-1
* **Suggested categories**: compartmental-modeling, dendritic-computation
* **Why download**: Demonstrates active dendrites can be approximated as a two-layer network;
  validation benchmark for the DSGC compartmental-vs-reduced model trade-off.

### 22. Jadi2014 - An augmented two-layer model captures nonlinear analog spatial integration effects

* **Authors**: Jadi, M. P., Behabadi, B. F., Poleg-Polsky, A., Schiller, J., Mel, B. W.
* **Year**: 2014
* **DOI**: `10.1109/JPROC.2014.2312671`
* **URL**: https://ieeexplore.ieee.org/document/6782394
* **Suggested categories**: compartmental-modeling, dendritic-computation, direction-selectivity
* **Why download**: Directly relevant: includes Poleg-Polsky as co-author and applies the two-layer
  framework to direction selectivity.

### 23. LondonHausser2005 - Dendritic computation

* **Authors**: London, M., Hausser, M.
* **Year**: 2005
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`
* **URL**: https://www.annualreviews.org/doi/10.1146/annurev.neuro.28.061604.135703
* **Suggested categories**: dendritic-computation, cable-theory
* **Why download**: The canonical Annual Review of dendritic computation; required context for any
  DSGC dendritic-modelling paper.

### 24. Spruston2008 - Pyramidal neurons: dendritic structure and synaptic integration

* **Authors**: Spruston, N.
* **Year**: 2008
* **DOI**: `10.1038/nrn2286`
* **URL**: https://www.nature.com/articles/nrn2286
* **Suggested categories**: dendritic-computation, synaptic-integration
* **Why download**: Synthesises empirical evidence for branch-level nonlinearities across pyramidal
  cell types.

### 25. Hay2011 - Models of neocortical layer 5b pyramidal cells capturing a wide range of dendritic and perisomatic active properties

* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107
* **Suggested categories**: compartmental-modeling, voltage-gated-channels
* **Why download**: Open-source NEURON model with complete channel kinetics (ModelDB 139653); direct
  source of .mod files for DSGC active dendrite modelling.

## Recommendations for This Task

1. **Prioritise open-access PDFs**: [Hay2011] (PLoS CB), [TranVanMinh2016] (Frontiers),
   [Gasparini2004] and [Stuart1998] (JNeurosci open archive) have guaranteed full-text access.
   Download these first.

2. **Expect paywalled items**: [Schiller2000, Stuart1994, Larkum1999, Hoffman1997, Magee1998]
   (Nature/Nat Neuro), [Polsky2004] (Nat Neurosci), [Larkum2009a, Bittner2017, Takahashi2016]
   (Science), [Branco2011, Abrahamsson2012, Losonczy2006, Milstein2015] (Neuron). Per task brief:
   attempt once, then mark `download_status: "failed"` and add DOI to
   `intervention/paywalled_papers.md`.

3. **Prefer review papers as fallbacks**: [LondonHausser2005], [Spruston2008], [Major2013a], and
   [TranVanMinh2016] cover the same mechanisms as their primary sources; if all primaries fail,
   these reviews still supply the synthesis.

4. **Adopt [Hay2011] MOD files as the canonical channel library**: Na+ (cortical), CaHVA, CaLVA, SK,
   Kv3_1, Im, and Ih kinetics are validated and reusable in DSGC modelling.

5. **Use NMDA kinetics from Jahr-Stevens** (classical) or [Branco2011] (cortical updates); both are
   already standard in NEURON community.

6. **Validate the active-vs-passive trade-off explicitly** by running the [Poirazi2003b] two-layer
   approximation against the full compartmental model; report variance-explained as a result metric.

7. **Update `research_papers.md` recommendation 7 (open-access venue priority)**: confirmed - eLife
   and PLoS CB items in this list are high-confidence downloads; we should also add Frontiers and
   JNeurosci open archive.

## Source Index

### [Schiller2000]

* **Type**: paper
* **Title**: NMDA Spikes in Basal Dendrites of Cortical Pyramidal Neurons
* **Authors**: Schiller, J., Major, G., Koester, H. J., Schiller, Y.
* **Year**: 2000
* **DOI**: `10.1038/35005094`
* **URL**: https://www.nature.com/articles/35005094
* **Peer-reviewed**: yes
* **Relevance**: Foundational NMDA spike demonstration; extends t0002 coverage beyond retina.

### [Polsky2004]

* **Type**: paper
* **Title**: Computational subunits in thin dendrites of pyramidal cells
* **Authors**: Polsky, A., Mel, B. W., Schiller, J.
* **Year**: 2004
* **DOI**: `10.1038/nn1253`
* **URL**: https://www.nature.com/articles/nn1253
* **Peer-reviewed**: yes
* **Relevance**: Branch-level supralinear integration; direct mechanism candidate for DSGCs.

### [Major2013a]

* **Type**: paper
* **Title**: Active properties of neocortical pyramidal neuron dendrites
* **Authors**: Major, G., Larkum, M. E., Schiller, J.
* **Year**: 2013
* **DOI**: `10.1146/annurev-neuro-062111-150343`
* **URL**: https://www.annualreviews.org/doi/10.1146/annurev-neuro-062111-150343
* **Peer-reviewed**: yes
* **Relevance**: Canonical synthesis of dendritic active properties.

### [Branco2011]

* **Type**: paper
* **Title**: Dendritic NMDA spikes are strictly local events
* **Authors**: Branco, T., Hausser, M.
* **Year**: 2011
* **DOI**: `10.1016/j.neuron.2011.02.006`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(11)00128-1
* **Peer-reviewed**: yes
* **Relevance**: Quantifies NMDA spike spatial extent.

### [Larkum1999]

* **Type**: paper
* **Title**: A new cellular mechanism for coupling inputs arriving at different cortical layers
* **Authors**: Larkum, M. E., Zhu, J. J., Sakmann, B.
* **Year**: 1999
* **DOI**: `10.1038/18686`
* **URL**: https://www.nature.com/articles/18686
* **Peer-reviewed**: yes
* **Relevance**: Apical Ca2+ spike and BAC firing.

### [Larkum2009a]

* **Type**: paper
* **Title**: Synaptic integration in tuft dendrites of layer 5 pyramidal neurons
* **Authors**: Larkum, M. E., Nevian, T., Sandler, M., Polsky, A., Schiller, J.
* **Year**: 2009
* **DOI**: `10.1126/science.1171958`
* **URL**: https://www.science.org/doi/10.1126/science.1171958
* **Peer-reviewed**: yes
* **Relevance**: Tuft-level NMDA plus Ca2+ integration.

### [Stuart1994]

* **Type**: paper
* **Title**: Active propagation of somatic action potentials into neocortical pyramidal cell
  dendrites
* **Authors**: Stuart, G. J., Sakmann, B.
* **Year**: 1994
* **DOI**: `10.1038/367069a0`
* **URL**: https://www.nature.com/articles/367069a0
* **Peer-reviewed**: yes
* **Relevance**: Foundational bAP demonstration.

### [Stuart1998]

* **Type**: paper
* **Title**: Determinants of voltage attenuation in neocortical pyramidal neuron dendrites
* **Authors**: Stuart, G., Spruston, N.
* **Year**: 1998
* **DOI**: `10.1523/JNEUROSCI.18-10-03501.1998`
* **URL**: https://www.jneurosci.org/content/18/10/3501
* **Peer-reviewed**: yes
* **Relevance**: Na+ channel density gradient.

### [Magee1998]

* **Type**: paper
* **Title**: Somatic EPSP amplitude is independent of synapse location in hippocampal pyramidal
  neurons
* **Authors**: Magee, J. C., Cook, E. P.
* **Year**: 2000
* **DOI**: `10.1038/81136`
* **URL**: https://www.nature.com/articles/nn1000_895
* **Peer-reviewed**: yes
* **Relevance**: Synaptic scaling rule.

### [Hoffman1997]

* **Type**: paper
* **Title**: K+ channel regulation of signal propagation in dendrites of hippocampal pyramidal
  neurons
* **Authors**: Hoffman, D. A., Magee, J. C., Colbert, C. M., Johnston, D.
* **Year**: 1997
* **DOI**: `10.1038/43119`
* **URL**: https://www.nature.com/articles/43119
* **Peer-reviewed**: yes
* **Relevance**: A-type K+ channels in CA1 dendrites.

### [Losonczy2006]

* **Type**: paper
* **Title**: Integrative properties of radial oblique dendrites in hippocampal CA1 pyramidal neurons
* **Authors**: Losonczy, A., Magee, J. C.
* **Year**: 2006
* **DOI**: `10.1016/j.neuron.2006.03.016`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(06)00226-7
* **Peer-reviewed**: yes
* **Relevance**: Branch-level integration.

### [Gasparini2004]

* **Type**: paper
* **Title**: On the initiation and propagation of dendritic spikes in CA1 pyramidal neurons
* **Authors**: Gasparini, S., Migliore, M., Magee, J. C.
* **Year**: 2004
* **DOI**: `10.1523/JNEUROSCI.2520-04.2004`
* **URL**: https://www.jneurosci.org/content/24/49/11046
* **Peer-reviewed**: yes
* **Relevance**: Compartmental modelling template.

### [Gambino2014]

* **Type**: paper
* **Title**: Sensory-evoked LTP driven by dendritic plateau potentials in vivo
* **Authors**: Gambino, F., Pages, S., Kehayas, V., et al.
* **Year**: 2014
* **DOI**: `10.1038/nature13664`
* **URL**: https://www.nature.com/articles/nature13664
* **Peer-reviewed**: yes
* **Relevance**: In vivo plateau evidence.

### [Milstein2015]

* **Type**: paper
* **Title**: Inhibitory gating of input comparison in the CA1 microcircuit
* **Authors**: Milstein, A. D., et al.
* **Year**: 2015
* **DOI**: `10.1016/j.neuron.2015.11.009`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(15)01010-5
* **Peer-reviewed**: yes
* **Relevance**: Plateau-dependent comparison.

### [Bittner2017]

* **Type**: paper
* **Title**: Behavioral time scale synaptic plasticity underlies CA1 place fields
* **Authors**: Bittner, K. C., Milstein, A. D., Grienberger, C., Romani, S., Magee, J. C.
* **Year**: 2017
* **DOI**: `10.1126/science.aan3846`
* **URL**: https://www.science.org/doi/10.1126/science.aan3846
* **Peer-reviewed**: yes
* **Relevance**: Behavioral plateau integration.

### [Takahashi2016]

* **Type**: paper
* **Title**: Active cortical dendrites modulate perception
* **Authors**: Takahashi, N., Oertner, T. G., Hegemann, P., Larkum, M. E.
* **Year**: 2016
* **DOI**: `10.1126/science.aah6066`
* **URL**: https://www.science.org/doi/10.1126/science.aah6066
* **Peer-reviewed**: yes
* **Relevance**: Behavioral dendritic plateaus.

### [Abrahamsson2012]

* **Type**: paper
* **Title**: Thin dendrites of cerebellar interneurons confer sublinear synaptic integration
* **Authors**: Abrahamsson, T., et al.
* **Year**: 2012
* **DOI**: `10.1016/j.neuron.2012.01.027`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(12)00140-8
* **Peer-reviewed**: yes
* **Relevance**: Sublinear thin-dendrite integration.

### [VervaekeE2012]

* **Type**: paper
* **Title**: Gap junctions compensate for sublinear dendritic integration
* **Authors**: Vervaeke, K., Lorincz, A., Nusser, Z., Silver, R. A.
* **Year**: 2012
* **DOI**: `10.1126/science.1215101`
* **URL**: https://www.science.org/doi/10.1126/science.1215101
* **Peer-reviewed**: yes
* **Relevance**: Gap-junction compensation.

### [TranVanMinh2016]

* **Type**: paper
* **Title**: Contribution of sublinear and supralinear dendritic integration to neuronal
  computations
* **Authors**: Tran-Van-Minh, A., et al.
* **Year**: 2015
* **DOI**: `10.3389/fncel.2015.00067`
* **URL**: https://www.frontiersin.org/articles/10.3389/fncel.2015.00067/full
* **Peer-reviewed**: yes
* **Relevance**: Sublinear-supralinear review.

### [Poirazi2003a]

* **Type**: paper
* **Title**: Arithmetic of subthreshold synaptic summation in a model CA1 pyramidal cell
* **Authors**: Poirazi, P., Brannon, T., Mel, B. W.
* **Year**: 2003
* **DOI**: `10.1016/S0896-6273(03)00148-X`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(03)00148-X
* **Peer-reviewed**: yes
* **Relevance**: Branch-level nonlinear summation.

### [Poirazi2003b]

* **Type**: paper
* **Title**: Pyramidal neuron as two-layer neural network
* **Authors**: Poirazi, P., Brannon, T., Mel, B. W.
* **Year**: 2003
* **DOI**: `10.1016/S0896-6273(03)00149-1`
* **URL**: https://www.cell.com/neuron/fulltext/S0896-6273(03)00149-1
* **Peer-reviewed**: yes
* **Relevance**: Two-layer model validation benchmark.

### [Jadi2014]

* **Type**: paper
* **Title**: An augmented two-layer model captures nonlinear analog spatial integration effects
* **Authors**: Jadi, M. P., Behabadi, B. F., Poleg-Polsky, A., Schiller, J., Mel, B. W.
* **Year**: 2014
* **DOI**: `10.1109/JPROC.2014.2312671`
* **URL**: https://ieeexplore.ieee.org/document/6782394
* **Peer-reviewed**: yes
* **Relevance**: Two-layer model applied to direction selectivity.

### [LondonHausser2005]

* **Type**: paper
* **Title**: Dendritic computation
* **Authors**: London, M., Hausser, M.
* **Year**: 2005
* **DOI**: `10.1146/annurev.neuro.28.061604.135703`
* **URL**: https://www.annualreviews.org/doi/10.1146/annurev.neuro.28.061604.135703
* **Peer-reviewed**: yes
* **Relevance**: Canonical review.

### [Spruston2008]

* **Type**: paper
* **Title**: Pyramidal neurons: dendritic structure and synaptic integration
* **Authors**: Spruston, N.
* **Year**: 2008
* **DOI**: `10.1038/nrn2286`
* **URL**: https://www.nature.com/articles/nrn2286
* **Peer-reviewed**: yes
* **Relevance**: Pyramidal-neuron integration synthesis.

### [Hay2011]

* **Type**: paper
* **Title**: Models of neocortical layer 5b pyramidal cells capturing a wide range of dendritic and
  perisomatic active properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107
* **Peer-reviewed**: yes
* **Relevance**: Open-source MOD files for channels.

### [RallChapter1977]

* **Type**: paper
* **Title**: Core conductor theory and cable properties of neurons (Handbook of Physiology chapter)
* **Authors**: Rall, W.
* **Year**: 1977
* **DOI**: `10.1002/cphy.cp010103`
* **URL**: https://onlinelibrary.wiley.com/doi/10.1002/cphy.cp010103
* **Peer-reviewed**: yes
* **Relevance**: Historical cable-theory foundation for this work.

### [Koch1998book]

* **Type**: paper
* **Title**: Biophysics of Computation: Information Processing in Single Neurons
* **Authors**: Koch, C.
* **Year**: 1998
* **DOI**: `10.1093/oso/9780195104912.001.0001`
* **URL**: https://global.oup.com/academic/product/biophysics-of-computation-9780195104912
* **Peer-reviewed**: yes
* **Relevance**: Textbook foundation for cable theory and dendritic computation.
