---
spec_version: "2"
answer_id: "morphology-direction-selectivity-modeling-synthesis"
answered_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_answered: "2026-04-21"
confidence: "medium"
---
# Morphology variables and mechanisms shaping DS across computational models

## Question

What variables of neuronal morphology have been shown by computational modeling to affect direction
selectivity, by what mechanisms, and what gaps remain?

## Short Answer

Computational models have shown that direction selectivity is shaped by dendritic length,
branch-order and branching pattern, dendritic diameter, the spatial layout and kinetic tiling of
bipolar-cell inputs, asymmetric arbors and plexus density, and the electrotonic compartmentalization
of terminal branches. The load-bearing mechanisms are passive cable filtering with
transfer-resistance weighting, local-global EPSP summation along soma-to-tip dendritic gradients,
space-time input tiling, dendritic-spike branch independence via voltage-gated Na and Ca channels,
and morphology-constrained asymmetric SAC-to-DSGC inhibition. Gaps remain in systematic sweeps of
branch order and dendritic diameter on realistic reconstructions, in joint manipulation of
morphology with active conductances at DSGC terminal tips, and in morphology-aware modeling of
cortical and invertebrate direction selectivity beyond the retina.

## Research Process

Research began from five baseline papers inherited from prior project tasks
(t0002_literature_survey_dsgc_compartmental_models, t0010_hunt_missed_dsgc_models,
t0013_resolve_morphology_provenance) covering DSGC compartmental models, machine-learning-discovered
DS principles, and SAC plexus wiring. I then ran 24 structured web searches across Google Scholar,
PubMed, and bioRxiv using combinations of terms including "starburst amacrine cell compartmental
model," "DSGC morphology model," "fly VS-cell dendritic direction selectivity," "cortical dendritic
asymmetry direction selectivity," and "dendritic diameter direction selectivity." I expanded the
candidate list through citation-graph traversal from each seed paper and stopped when batches
returned zero new mechanisms against those already represented. The target was 15 new papers with a
hard floor of 12; 15 were added. Two PDFs (Kim2014 on EyeWire-reconstructed SAC wiring and
Sivyer2013 on DSGC dendritic spikes) were paywalled; I filed intervention files in
`intervention/Kim2014_paywalled.md` and `intervention/Sivyer2013_paywalled.md` and built summaries
from CrossRef, PMC open abstracts, and author preprints. Where results conflicted (for example, the
role of dendritic geometry vs input layout in T4 DS), I report both the positive and negative
findings and attribute them to specific papers.

## Evidence from Papers

### Dendritic length

[Hausselt2007][hausselt2007] swept SAC dendritic length from 50 to 200 micrometres in NEURON with
morphology otherwise preserved; DSI dropped monotonically from ~0.35 at natural 150 um to ~0.12 at
50 um because shorter cables lose the soma-to-tip voltage gradient that the Ca2+-channel
nonlinearity requires. [Tukker2004][tukker2004] similarly found that the electrotonic length
constant peaks DS at an intermediate lambda of ~400 um comparable to the dendritic spread.
[Jain2020][jain2020] reported an exponential decay of pairwise noise correlations along DSGC
dendrites with a cable space constant of 5.3 um, setting a spatial scale for independent DS
subunits.

### Branch pattern, branch order, and branching geometry

[Tukker2004][tukker2004] found SAC DSI nearly invariant to the distance of the first branch point
but increased up to twofold when branches and synapse density were concentrated in the outer 20% of
the tree. [Hausselt2007][hausselt2007] showed that placing Ca2+ conductance on higher-order (distal)
branches raises DSI by about +0.1 over uniform distribution. [Cuntz2010][cuntz2010] formalized the
link: a single scalar balancing factor bf maps monotonically onto electrotonic compartmentalization,
so low-bf trees have many electrotonically isolated subtrees while high-bf trees are
electrotonically compact. The TREES toolbox provides the canonical centripetal branch-ordering
generator used in subsequent DS models.

### Input spatial layout and synaptic clustering

[Vlasits2016][vlasits2016] showed by morphology-matched symmetric-input control that restricting
excitation to the proximal two-thirds of the SAC dendrite (as measured anatomically) raises
distal-varicosity DSI to 0.34 +/- 0.23 versus 0.11 +/- 0.18 when inputs are spread uniformly; the
dendrite alone cannot produce strong DS without proximal-restricted input placement.
[Kim2014][kim2014] used EyeWire-reconstructed SAC and bipolar-cell arbors to show BC2 contacts
proximal SAC dendrites and BC3a contacts distal dendrites, with a 50-100 ms temporal lag that yields
a space-time-tilted kernel and outward DS. [Srivastava2022][srivastava2022] directly measured
sustained-transient input kinetics on single SAC dendrites and showed in a NEURON ball-and-stick SAC
that swapping proximal-distal kinetics reverses the preferred direction, and homogenizing kinetics
strongly reduces DSi. [Ezra-Tsur2021][ezra-tsur2021] used a genetic algorithm over an 8D
input-layout parameter space on a 1013-compartment SAC and found that only the combined
sustained-proximal with transient-distal arrangement reproduces centrifugal preference; reversed
arrangements produce zero CF-preferring SACs.

### Asymmetric arbors, plexus density, and tiling

[Morrie2018][morrie2018] showed in Sema6A-/- mice that when SAC plexus density is halved, DSGC
ON-direction vector sum magnitude collapses from 0.40 to 0.10, and 30-40% of SAC varicosities lose
their centrifugal tuning and instead follow the local distal-dendrite orientation; simulation
confirms both plexus density and per-synapse orientation matter. [Sivyer2013][sivyer2013] (via its
summary) demonstrated that DSGC terminal dendrites behave as near-independent DS subunits driven by
asymmetric SAC-mediated inhibition.

### Electrotonic compartmentalization and transfer resistance

[Dan2018][dan2018] formalized transfer-resistance (TR) weighting as the canonical dendrite-to-axon
integration rule for fly VS cells, with branchlets electrotonically decoupled (inter-branchlet TR
much smaller than local input resistance) and TR-weighted summation reducing the difference index
from 0.411 (uniform) to 0.293, exceeding 2 SD of the shuffled-weight null. [Single1997][single1997]
showed in the same fly VS-cell preparation that direction selectivity is not inherited from upstream
EMDs but is generated postsynaptically by opponent excitation and shunting inhibition on the passive
dendrite; the dendritic morphology carries the computation. [Anderson1999][anderson1999] provides
the cortical counterpoint: a detailed NEURON compartmental model of cat V1 Meynert cells with
extreme dendritic asymmetry supports single-cell DS only at unphysiologically fast stimulus
velocities, showing cortical DS cannot be explained by dendritic asymmetry alone.

### Dendritic diameter

[Wu2023][wu2023] performed the most explicit dendritic-diameter sweep to date in a primate SAC
connectomics-based model: medial dendritic diameter around 0.2-0.25 um maximizes DSI (matching
measured 0.15-0.2 um), while distal diameter saturates DSI once it exceeds ~0.8 um. The diameter
ranges are morphology variables no other DS paper systematically swept.

### Active dendritic conductances interacting with morphology

[Schachter2010][schachter2010] showed that local input resistance scales from 150-200 MOhm
proximally to >1 GOhm distally, producing a spatial gradient of dendritic-spike threshold: ~1 nS
suffices distally while 3-4 nS is needed proximally, yielding a ~4x amplification of DSI via
dendritic Na/Ca-channel threshold nonlinearity. [Sivyer2013][sivyer2013] provided dual-patch
evidence that DSGC terminal dendrites initiate fast spikes locally, with passive-only (gNa = gCa =
0\) models failing to reproduce the observed DS gain. [Aldor2024][aldor2024] added perisomatic Kv3
channels and dendritic mGluR2 as morphologically compartmentalized conductances that together
control SAC functional compartmentalization, with co-blockade abolishing DSGC direction selectivity.
[PolegPolsky2026][polegpolsky2026] used machine-learning exploration of a 352-segment DSGC model to
show that distance-graded passive delay lines, velocity-dependent coincidence detection, and
NMDA-mediated multiplicative gating can each independently drive DSI > 0.5 when morphology and
conductance distributions are tuned.

### Input contrast and circuit linearization on dendrites

[PolegPolsky2016][polegpolsky2016] showed via a 121-compartment stochastic DSGC model that matched
E/I contrast tuning across the dendritic tree produces the highest suprathreshold DSI, and that BC
subtype heterogeneity pre-compensates the SAC dendritic nonlinearity; morphologically distributed
synapses are required. [deRosenroll2026][derosenroll2026] showed at a finer grain that broadening
the ACh time course uncouples local E and I on the same dendritic subunit (local DSI drops while
global DSI is nearly preserved), and that removing the spatial offset between GABA and ACh release
sites in the SAC network model eliminates the local-DSI drop.

### Gruntman2018 as a null for dendritic geometry

[Gruntman2018][gruntman2018] reconstructed a Drosophila T4 cell from FIB-SEM and collapsed all 154
synapses onto the dendritic base or replaced the cell with a single compartment; both produced
essentially the same DSI-versus-speed curve as the full 344-section dendrite. The T4 arbor's role
reduces to the 1D spatial layout of E and I inputs, not cable geometry - a strong null that
morphology-modeling work should beat before claiming a dendritic contribution.

## Evidence from Internet Sources

Internet search (Google Scholar, PubMed, bioRxiv) was used to identify candidate papers for the
survey and to triangulate bibliographic metadata for the two paywalled PDFs. No web resource was
cited as primary evidence for a scientific claim; all scientific claims in this answer are grounded
in the 20 paper summaries listed above. The internet served as the discovery substrate and as a
cross-reference for author affiliations and venue identifiers; it did not contribute independent
evidence.

## Evidence from Code or Experiments

Not used for this answer.

## Synthesis

The computational-modeling literature converges on a consistent picture with five mechanistic
families. First, morphology matters for DS through passive cable filtering: transfer-resistance
weighting [Dan2018][dan2018] and local-global EPSP summation with an intermediate electrotonic
length [Tukker2004][tukker2004] define how distributed dendritic inputs combine to produce an
asymmetric somatic or axonal signal. Second, morphology interacts with input layout: the
sustained-proximal transient-distal tiling of bipolar inputs ([Kim2014][kim2014],
[Srivastava2022][srivastava2022], [Ezra-Tsur2021][ezra-tsur2021]) and the proximal-restricted
excitatory field [Vlasits2016][vlasits2016] supply the space-time asymmetry that the passive cable
converts into DS; dendritic geometry without the right input layout does not produce strong DS
([Vlasits2016][vlasits2016], [Gruntman2018][gruntman2018]). Third, active conductances rescale and
amplify the morphology-gated signal: HVA Ca channels [Hausselt2007][hausselt2007], Na-channel
dendritic spikes ([Schachter2010][schachter2010], [Sivyer2013][sivyer2013]), NMDA multiplicative
gating, and perisomatic Kv3 plus dendritic mGluR2 [Aldor2024][aldor2024] add nonlinearity that turns
a modest subthreshold DS into a saturated spiking output.

Fourth, asymmetric arbors and tiled plexus density at the network level control which parts of the
morphology connect to which presynaptic partners: [Morrie2018][morrie2018] shows plexus density
dictates whether SAC varicosities retain centrifugal tuning, and [Kim2014][kim2014] shows that
BC2/BC3a wiring specificity is not explained by shared IPL depth alone. Fifth, the retinal and fly
invertebrate literatures place morphology as a computational substrate ([Single1997][single1997],
[Dan2018][dan2018]), while the cortical literature [Anderson1999][anderson1999] explicitly rejects
single-cell dendritic asymmetry as the mechanism for V1 DS. This cross-preparation comparison is
informative: morphology contributes to DS where co-located asymmetric inputs plus compartmentalized
active conductances convert cable delays into differential depolarization, and does not contribute
meaningfully when those substrates are absent.

The recent machine-learning exploration [PolegPolsky2026][polegpolsky2026] shows that many
qualitatively distinct morphology-compatible mechanisms can each independently drive DSI > 0.5 in a
352-segment DSGC, which reframes morphology-to-DS modeling from a single-mechanism question into a
landscape question: what regions of the morphology-plus-biophysics parameter space support which DS
mechanism, and which regions match biology?

## Limitations

* Coverage is incomplete. Only 15 new papers were added in this task. The field includes additional
  cortical, fly lobula-plate, and zebrafish DS modeling work that was not systematically reviewed.
* Only English-language, peer-reviewed, and major-preprint sources were considered. Non-English
  primary literature and gray literature are not represented.
* Two key PDFs (Kim2014, Sivyer2013) were paywalled; summaries were built from open abstracts and
  citation-graph context rather than from the full text. Quantitative claims from those two papers
  were limited to what the abstracts and corroborating citations supported.
* No in silico replication was performed. Quantitative claims in the Evidence section are
  paraphrased from published summaries and have not been re-verified by running the original models.
* No quantitative meta-analysis was conducted. The DSI numbers reported here are indicative rather
  than a pooled effect size across papers; methods, metrics, and model assumptions vary between
  studies.
* Dendritic diameter, despite being a first-order morphology variable, was systematically swept in
  only one paper in this corpus [Wu2023][wu2023]. This is both a finding and a limitation of the
  survey.

## Sources

* Paper: `10.1038_s41598-018-23998-9`
* Paper: `10.1017_S0952523804214109`
* Paper: `10.1371_journal.pbio.0050185`
* Paper: `10.1016_j.neuron.2016.02.020`
* Paper: `10.1038_nature13240`
* Paper: `10.1038_nn.3565`
* Paper: `10.7554_eLife.81533`
* Paper: `10.1371_journal.pcbi.1000877`
* Paper: `10.1523_JNEUROSCI.17-16-06023.1997`
* Paper: `10.1038_s41467-024-46234-7`
* Paper: `10.1523_JNEUROSCI.4013-15.2016`
* Paper: `10.1038_s41593-017-0046-4`
* Paper: `10.1371_journal.pcbi.1009754`
* Paper: `10.1038_12194`
* Paper: `10.1017_S0952523823000019`
* Paper: `10.1371_journal.pcbi.1000899`
* Paper: `10.7554_eLife.52949`
* Paper: `10.1016_j.cub.2018.03.001`
* Paper: `10.1038_s41467-026-70288-4`
* Paper: `10.1016_j.celrep.2025.116833`
* Task: `t0002_literature_survey_dsgc_compartmental_models`
* Task: `t0010_hunt_missed_dsgc_models`
* Task: `t0013_resolve_morphology_provenance`

[dan2018]: https://doi.org/10.1038/s41598-018-23998-9
[tukker2004]: https://doi.org/10.1017/S0952523804214109
[hausselt2007]: https://doi.org/10.1371/journal.pbio.0050185
[vlasits2016]: https://doi.org/10.1016/j.neuron.2016.02.020
[kim2014]: https://doi.org/10.1038/nature13240
[sivyer2013]: https://doi.org/10.1038/nn.3565
[srivastava2022]: https://doi.org/10.7554/eLife.81533
[cuntz2010]: https://doi.org/10.1371/journal.pcbi.1000877
[single1997]: https://doi.org/10.1523/JNEUROSCI.17-16-06023.1997
[aldor2024]: https://doi.org/10.1038/s41467-024-46234-7
[polegpolsky2016]: https://doi.org/10.1523/JNEUROSCI.4013-15.2016
[gruntman2018]: https://doi.org/10.1038/s41593-017-0046-4
[ezra-tsur2021]: https://doi.org/10.1371/journal.pcbi.1009754
[anderson1999]: https://doi.org/10.1038/12194
[wu2023]: https://doi.org/10.1017/S0952523823000019
[schachter2010]: https://doi.org/10.1371/journal.pcbi.1000899
[jain2020]: https://doi.org/10.7554/eLife.52949
[morrie2018]: https://doi.org/10.1016/j.cub.2018.03.001
[polegpolsky2026]: https://doi.org/10.1038/s41467-026-70288-4
[derosenroll2026]: https://doi.org/10.1016/j.celrep.2025.116833
