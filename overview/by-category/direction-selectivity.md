# Category: Direction Selectivity

Neural responses that depend on the direction of a moving or spreading stimulus.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (38)](../papers/by-category/direction-selectivity.md) | [Answers
(13)](../answers/by-category/direction-selectivity.md) | [Suggestions
(131)](../suggestions/by-category/direction-selectivity.md) | [Datasets
(2)](../datasets/by-category/direction-selectivity.md) | [Libraries
(7)](../libraries/by-category/direction-selectivity.md) | [Predictions
(2)](../predictions/by-category/direction-selectivity.md)

---

## Papers (38)

<details>
<summary>📖 <strong>Machine learning discovers numerous new computational principles
underlying direction selectivity in the retina</strong> — Poleg-Polsky,
2026</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_s41467-026-70288-4` |
| **Authors** | Alon Poleg-Polsky |
| **Venue** | Nature Communications (journal) |
| **DOI** | `10.1038/s41467-026-70288-4` |
| **URL** | https://www.nature.com/articles/s41467-026-70288-4 |
| **Date added** | 2026-04-20 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0010_hunt_missed_dsgc_models`](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md) |

Poleg-Polsky uses a machine-learning parameter search over a 352-segment biophysical model of
a mouse ON-OFF DSGC to enumerate mechanisms that can produce direction selectivity. The search
space includes bipolar-cell input geometry, synaptic kinetics, NMDA receptor placement and
strength, dendritic voltage-gated channel densities, and the presence or absence of
SAC-derived inhibition. Thousands of candidate configurations are simulated under standardised
moving-bar stimuli and scored on DSI.

The search reveals that many qualitatively different mechanisms can produce robust direction
selectivity. Dendrite-intrinsic primitives - velocity-dependent coincidence detection,
distance-graded passive delay lines, NMDA-mediated multiplicative gating - are each sufficient
on their own. Hybrid configurations that combine these primitives with SAC-derived inhibition
match experimental DSI most closely. Targeted ablations confirm each primitive is causally
responsible for DSI within its cluster.

The paper challenges the textbook view that starburst amacrine cells are the dominant
substrate of DSGC direction selectivity. Instead, it argues the DSGC dendrite itself is a
richer computational organ capable of producing DS via multiple biophysically plausible
strategies, and that the retinal circuit likely exploits several of them in parallel.

For t0010_hunt_missed_dsgc_models, this paper is a high-priority candidate. The companion code
(`PolegPolskyLab/DS-mechanisms`) provides a NEURON + Python 352-segment DSGC model exposing
exactly the parameters our project is interested in probing - bipolar-cell input structure,
kinetics, NMDA strength, and dendritic biophysics. The ML-discovered configurations give us a
library of distinct tuning-curve shapes to include in comparative analyses. The primary
porting risk is the absent LICENSE file; a licence clarification intervention or
fork-under-MIT may be required before the code can be redistributed.

</details>

<details>
<summary>📖 <strong>Uncovering the “hidden” synaptic microarchitecture of the retinal
direction selective circuit</strong> — deRosenroll et al., 2026</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.celrep.2025.116833` |
| **Authors** | Geoff deRosenroll, Santhosh Sethuramanujam, Gautam B. Awatramani |
| **Venue** | Cell Reports (journal) |
| **DOI** | `10.1016/j.celrep.2025.116833` |
| **URL** | https://www.cell.com/cell-reports/fulltext/S2211-1247(25)01605-5 |
| **Date added** | 2026-04-20 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0010_hunt_missed_dsgc_models`](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/summary.md) |

This paper addresses how starburst amacrine cells shape direction selectivity in ON-OFF DSGCs
at the subcellular scale, focusing on the differential release of GABA and ACh. The authors
combine two-photon Ca2+ imaging of local DSGC dendritic subunits with a biophysically detailed
NEURON network model that explicitly represents the anatomical offset between SAC-GABA and
SAC-ACh synapses onto the DSGC.

Using acetylcholinesterase blockade, they perturb ACh dynamics while preserving the global
excitation/inhibition balance across the dendritic tree. Experimentally, this preserves
cell-wide firing but degrades direction selectivity at the local subunit level. The network
model reproduces the dissociation and attributes it to local uncoupling of E and I caused by
spatiotemporal perturbation of ACh relative to spatially offset GABA.

The central finding is that direction-selective computation in a DSGC is not a simple function
of whole-cell E/I balance, but depends on a *microstructured* alignment of GABA and ACh
release from SACs. Perturbing this alignment - even without disturbing the global ratio - is
sufficient to compromise the cell direction selectivity at the subunit scale. The authors call
this the "hidden" synaptic microarchitecture of the DS circuit.

For the current project (t0010_hunt_missed_dsgc_models), the paper is a top-priority
candidate: it publishes a new MIT-licensed NEURON + Python DSGC network model with
differential GABA/ACh wiring, directly addresses the project research question of how local
synaptic input patterns determine DSGC tuning, and extends the canonical Poleg-Polsky 2016
model already ported by t0008. The companion repository
(`geoffder/ds-circuit-ei-microarchitecture`, Zenodo 10.5281/zenodo.17666157) ships a driver
script, MOD files, and a HOC geometry that should be amenable to an automated port with a thin
12-direction tuning-curve wrapper. The main limitation for this summary is that the published
PDF could not be downloaded (Elsevier 403), so all quantitative values above that are not
cited from the abstract should be re-verified once a human reviewer retrieves the article
manually.

</details>

<details>
<summary>📖 <strong>Dendritic mGluR2 and perisomatic Kv3 signaling regulate dendritic
computation of mouse starburst amacrine cells</strong> — Ledesma et al.,
2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_s41467-024-46234-7` |
| **Authors** | Hector Acaron Ledesma, Jennifer Ding, Swen Oosterboer, Xiaolin Huang, Qiang Chen, Sui Wang, Michael Z. Lin, Wei Wei |
| **Venue** | Nature Communications (journal) |
| **DOI** | `10.1038/s41467-024-46234-7` |
| **URL** | https://www.nature.com/articles/s41467-024-46234-7 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_s41467-024-46234-7/summary.md) |

This Nature Communications paper from the Wei lab at the University of Chicago (with
genetic-tool collaborations from the Lin and Wang labs at Stanford) uses genetically encoded
voltage (ASAP3) and calcium (GCaMP6f) imaging together with whole-cell patch-clamp to ask how
starburst amacrine cell dendrites convert concentrically distributed synaptic inputs into
branch-specific direction-selective outputs. The study focuses on two specific membrane
conductances — metabotropic glutamate receptor 2 (mGluR2) and voltage-gated potassium channel
Kv3 — whose subcellular distributions are non-uniform: Kv3 clusters around the soma while
mGluR2 extends throughout the dendritic arbor.

Methodologically, the authors combine subcellular two-photon imaging at multiple radial
distances (0-105 µm from soma) with targeted pharmacology: LY341495 to block endogenous mGluR2
signaling and 1 mM TEA to selectively block Kv3 while leaving bipolar-cell excitatory inputs
intact. Paired SAC-DSGC recordings verify that manipulations at the SAC level propagate to
direction-selective ganglion-cell IPSCs. No biophysical compartmental model is constructed;
this is a strictly experimental paper.

The headline findings are: (1) direction-selective calcium transients emerge abruptly only in
the distal half of each SAC dendrite; (2) mGluR2 blockade releases suprathreshold calcium in
the inward direction by lowering the VGCC activation threshold (paired t-test p = 0.0002, n =
10), abolishing dendritic DS while leaving somatic responses untouched; (3) Kv3 blockade
triples somatic Vm variance (1.6 -> 4.3 mV^2, p = 0.006) and introduces fast transients >15 mV
at the soma without changing slow depolarization; (4) co-blockade of both eliminates DSGC
direction selectivity downstream, demonstrating that the two mechanisms are jointly necessary.

For this project literature survey on how morphology shapes direction selectivity via
computational modeling, Aldor2024 (Ledesma et al. 2024) is a borderline inclusion. It is SAC
rather than DSGC biology, and — critically — it does not perform morphology sweeps or build a
compartmental model. Its contribution to a morphology-focused survey is as an empirical
constraint: it identifies two anatomically localized conductances that any honest
compartmental SAC DS model must include with their correct spatial distributions (perisomatic
Kv3, dendritic mGluR2), and it quantifies the DS-relevant observables (calcium threshold
shifts, somatic Vm variance, directional calcium onset at fractional radius ~0.5) that such a
model must reproduce. Use it as a validation target when sweeping morphology or channel
distribution in a SAC model; do not cite it as a morphology-sweep example.

</details>

<details>
<summary>📖 <strong>Two mechanisms for direction selectivity in a model of the
primate starburst amacrine cell</strong> — Wu et al., 2023</summary>

| Field | Value |
|---|---|
| **ID** | `10.1017_S0952523823000019` |
| **Authors** | Jiajia Wu, Yeon Jin Kim, Dennis M. Dacey, John B. Troy, Robert G. Smith |
| **Venue** | Visual Neuroscience (journal) |
| **DOI** | `10.1017/S0952523823000019` |
| **URL** | https://www.cambridge.org/core/journals/visual-neuroscience/article/two-mechanisms-for-direction-selectivity-in-a-model-of-the-primate-starburst-amacrine-cell/6C688BA235ED1FE58BBD8BCDDB8C5B59 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1017_S0952523823000019/summary.md) |

Wu et al. (2023) build a compartmental macaque ON starburst amacrine cell (SAC) model in
NeuronC based on a connectomic reconstruction (Kim et al. 2022) and use it to resolve a
two-decade debate about the origin of direction selectivity (DS) in SAC dendrites. They
compare two mechanisms: the "morphological" mechanism (electrotonic delay along thin medial
dendrites plus a sealed-cable effect at thick distal tips), and the "space-time" mechanism
(spatially segregated sustained midget and transient DB4/5 bipolar inputs). By constructing
matched sustained-only and sustained+transient models they cleanly partition the two
contributions.

Methodologically, the model is dense enough to be realistic but simple enough to be
interpretable: 400-700 compartments, biophysically parameterised bipolar cells, a 2D stimulus
grid of bar widths (50-500 um) x velocities (100-10,000 um/s), and 30 random replicates per
cell. Voltage-gated Na and Ca channels are deliberately omitted from the SAC in the main
analysis to isolate the subthreshold origin of DS. A separate morphology sweep varies distal
(0.2-1.2 um) and medial (0.1-0.35 um) dendritic diameters, and a mouse SAC model (Ding et al.
2016 morphology) is run alongside as a cross-species morphology manipulation.

The headline result is a clean phase diagram: the morphological mechanism dominates for small,
fast objects (peak DSI ~0.32 at bar width 50 um, velocity 2000 um/s) while the space-time
mechanism dominates for large, slow objects (DSI goes from ~0.16 sustained-only to ~0.22
sustained+transient at 500 um bars, 200 um/s). DSI is maximised when medial diameter sits at
0.2-0.25 um (matching the EM anatomy) and distal diameter >=0.8 um. Dendritic N/P/Q Ca
channels regeneratively amplify the subthreshold DS signal (voltage DSI 0.28 -> 0.46, [Ca] DSI
0.78 in a single run). The mouse model reproduces the same phase structure despite different
bipolar input densities and spatial distribution.

For our t0027 literature survey on computational models linking neuronal morphology to DS,
this paper is a strong positive example of the sweep-morphology-measure-DS paradigm we are
documenting. The morphology variable is SAC dendritic geometry (not DSGC), and the outcome is
DSI at the distal varicosity. It provides a concrete anchor for (a) the expected DSI range in
SAC-only compartmental models (~0.1-0.4 in voltage, up to ~0.8 in dendritic Ca), (b) the
velocity-tuning curve of the morphological mechanism (peak near 2000 um/s in macaque), and (c)
the quantitative impact of medial vs distal diameter on DSI. Limitations to note for our
survey: the model omits GABAergic, glycinergic, and cholinergic network interactions; DSGC
morphology is absent; only one tree topology is used (diameters are swept but branching
pattern and total dendritic length are not). These gaps will need to be filled by other papers
in the survey that sweep DSGC morphology or vary branching asymmetry.

</details>

<details>
<summary>📖 <strong>Spatiotemporal properties of glutamate input support direction
selectivity in the dendrites of retinal starburst amacrine cells</strong>
— Srivastava et al., 2022</summary>

| Field | Value |
|---|---|
| **ID** | `10.7554_eLife.81533` |
| **Authors** | Prerna Srivastava, Geoff de Rosenroll, Akihiro Matsumoto, Tracy Michaels, Zachary Turple, Varsha Jain, Santhosh Sethuramanujam, Benjamin L Murphy-Baum, Keisuke Yonehara, Gautam Bhagwan Awatramani |
| **Venue** | eLife (journal) |
| **DOI** | `10.7554/eLife.81533` |
| **URL** | https://elifesciences.org/articles/81533 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.7554_eLife.81533/summary.md) |

This paper addresses a longstanding open question in retinal direction selectivity: whether
the connectomically-inspired "space-time wiring" model — in which proximal starburst amacrine
cell (SAC) dendrites receive tonic/sustained glutamate release from BC7 bipolar cells and
distal dendrites receive transient release from BC5 subtypes — is experimentally verifiable
and computationally sufficient to shape SAC dendritic direction selectivity. Prior imaging
surveys had reported uniform BC kinetics, casting doubt on the model, while prior connectomic
and voltage-clamp work had left the input-kinetic verification gap unclosed. Srivastava et al.
close this gap by combining SAC-targeted iGluSnFR imaging with compartmental modeling.

Methodologically, the authors injected Cre-dependent iGluSnFR into ChAT-Cre mouse retinas and
imaged glutamate signals at 5 µm ROI resolution along individual ON-SAC dendrites and across
population fields of view, varying stimulus spot size from 100 to 800 µm and applying a
GABA_A/GABA_C/AMPA blocker cocktail to isolate network contributions. They then deconvolved
the fluorescence with a fitted quantal iGluSnFR kernel to recover per-site vesicle release
rates, which they fed into a ball-and-stick NEURON SAC model whose synapse positions were
sampled from Ding et al. 2016 connectomic BC7/BC5 probability density functions (6 proximal +
12 distal per trial).

Empirically, they find a robust proximal-to-distal gradient in sustained/transient index (STi
≈ 0.33 proximal vs 0.16 distal on single dendrites, 0.34 vs 0.21 at population level), a 3×
higher steady-state release rate proximally (~3 vs ~1 vesicles/s), persistence of this
gradient under full inhibitory blockade, and — critically — in silico demonstrations that
swapping the proximal/distal kinetic arrangement reverses the SAC's preferred direction, that
homogenizing kinetics abolishes DS, and that DSi grows linearly with proximal-distal BC
separation distance. The effect is statistically significant up to 1 mm/s stimulus velocity
and strongest below 0.5 mm/s.

For the present project's morphology-shapes-DS literature survey, this paper is important for
three reasons. First, it is a clean example of **input-on-dendrite morphology** shaping DS:
the spatial arrangement of kinetically distinct synaptic inputs *along* the SAC dendrite,
rather than the dendritic branching structure per se, produces the DS signal — a mechanism
readily generalizable to DSGC models constrained by connectomic priors. Second, it provides a
validated pipeline (iGluSnFR → temporal deconvolution → release-rate-driven NEURON model)
reusable for DSGC studies. Third, it delineates the **scope limitation** of the
space-time-wiring mechanism (slow stimuli only), which must be respected when extrapolating to
DSGC DS where high-velocity DS is known to be robust. The paper is tagged "SAC, not DSGC" in
our survey: it operates one layer upstream of the canonical DSGC but contributes a mechanism
that any end-to-end morphology-DS model of the DSGC-afferent circuit must incorporate.

</details>

<details>
<summary>📖 <strong>Dendrite Morphology Minimally Influences the Synaptic
Distribution of Excitation and Inhibition in Retinal Direction-Selective
Ganglion Cells</strong> — El-Quessny & Feller, 2021</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_ENEURO.0261-21.2021` |
| **Authors** | Malak El-Quessny, Marla B. Feller |
| **Venue** | eNeuro (journal) |
| **DOI** | `10.1523/ENEURO.0261-21.2021` |
| **URL** | https://www.eneuro.org/content/8/5/ENEURO.0261-21.2021 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/summary.md) |

El-Quessny and Feller test whether the global shape of a DSGC’s dendritic arbor determines how
its excitatory and inhibitory synaptic inputs are spatially organized. They exploit a natural
biological contrast: Hb9::GFP vDSGCs have strongly asymmetric dendrites oriented toward the
preferred direction, while Trhr::GFP nDSGCs have symmetric dendrites but similar
direction-selective spike output. The motivation is to dissociate two classical mechanisms of
retinal direction selectivity, tuned inhibition and spatially offset inhibition, and to ask
which of them tracks dendritic morphology.

Methodologically, the authors combine two-photon targeted whole-cell voltage clamp of EPSCs
(V_hold = -70 mV) and IPSCs (V_hold = 0 mV) with per-cell morphological reconstruction in
flat-mount mouse retina. Cells are probed with both drifting bars (eight directions, 250 um/s)
and a 10 x 10 stationary flash grid over a 500 x 500 um soma-centered field (30 x 30 um
squares), which allows independent measurement of directional tuning and 2D receptive-field
geometry. Additional experiments block nAChRs with 100 uM hexamethonium to separate
cholinergic from glutamatergic excitation, and a set of vector-based COM analyses quantifies
dendritic asymmetry, E-to-I spatial offset, per-pixel E vs I correlation, and the ratio of
synaptic-field to dendritic-field area.

The headline findings are a clean dissociation. Asymmetric vDSGCs show significantly sharper
directional tuning of inhibition than symmetric nDSGCs (IPSC DSI **0.48** vs **0.34** ON;
**0.56** vs **0.31** OFF), driven by weaker preferred-side inhibition. However, E-to-I spatial
offsets are small (**<50 um**) and comparable between subtypes, E and I amplitudes are locally
correlated (R^2 ~ 0.51-0.65 per pixel), and both receptive fields exceed the dendritic field
by a factor of **~1.6-3.3** because of cholinergic (SAC) input. Pharmacological block of
nAChRs shrinks the excitatory receptive field toward the dendritic field and reveals that
nDSGC glutamatergic fields point toward the null direction, whereas vDSGC glutamatergic fields
remain biased toward the preferred direction.

For this project, which aims to match single-DSGC angle-to-AP-frequency curves in a
compartmental model, the paper is foundational. It tells us (i) dendritic asymmetry matters
for tuned inhibition but not for spatial E/I organization, so a compartmental model that
ignores global morphology can still reproduce E/I spatial structure if it gets SAC-mediated
wiring right; (ii) synapse distributions should cover **1.6-3.3x** the dendritic footprint
with a co-varying local E/I amplitude ratio; (iii) the E-to-I spatial offset along the
preferred axis is **<50 um** and inhibition is locally correlated with excitation in strength;
and (iv) reproducing the gap between stationary-map and drifting-bar offsets requires
stimulus-dependent recruitment of lateral inhibition. These quantitative constraints directly
feed into the AMPA/GABA placement, synaptic density maps, and stimulus protocols used to tune
the project’s DSGC compartmental model.

</details>

<details>
<summary>📖 <strong>Realistic retinal modeling unravels the differential role of
excitation and inhibition to starburst amacrine cells in direction
selectivity</strong> — Ezra-Tsur et al., 2021</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1009754` |
| **Authors** | Elishai Ezra-Tsur, Oren Amsalem, Lea Ankri, Pritish Patil, Idan Segev, Michal Rivlin-Etzion |
| **Venue** | PLOS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1009754` |
| **URL** | https://doi.org/10.1371/journal.pcbi.1009754 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1009754/summary.md) |

Ezra-Tsur and colleagues attack a long-standing problem in retinal computation: determining
which of several competing mechanisms (input layout, input kinetics, intrinsic ion channels,
reciprocal inhibition) produces the centrifugal preference of SAC dendrites that, in turn,
drives direction selectivity in DSGCs. Because these mechanisms are experimentally difficult
to isolate, the authors build RSME - a NEURON-encapsulating framework that ties together
detailed morphology, biophysics, retinal connectivity rules, and visual stimuli - and use it
as a counterfactual engine.

The methodological core is a genetic-algorithm sweep over an 8-dimensional parameter space
that controls the spatial density of bipolar-to-SAC synapses and the per-synapse release
kinetics, holding the passive SAC morphology (1013-compartment NeuroMorpho NMO_139062) fixed.
By varying only the input-on-dendrite layout the authors show that spatiotemporally diverse
excitation - sustained proximal, transient distal - is sufficient to reproduce experimentally
measured CSI (~0.18) and RTI (~0.33); reversing the arrangement eliminates CF preference (0/N
cells), and fixing it gives 4/2125 barely-CF cells. In a subsequent 13-SAC network, reciprocal
inhibition modulates but does not generate CF preference, peaking at ~0.1 nS.

The DSGC results are the most load-bearing for this project morphology-focused survey:
embedding a reconstructed DSGC (NMO_05318, 1013 compartments, passive, -49 mV threshold, -52
mV baseline) in the SAC network and flipping between random and asymmetric null-side
SAC-to-DSGC wiring shows that asymmetric wiring alone produces positive DSI and PD activation,
even when the SAC network has no CF preference. SAC-SAC inhibition improves DSI modestly under
noiseless stimuli and strongly under noisy stimuli - reproducing the Chen et al. short-term
depression mechanism - while asymmetric wiring remains necessary throughout. These are
specific, quantitative necessity/sufficiency claims.

For this project on computational models linking neuronal morphology to direction-selectivity,
the paper is a clear inclusion: it uses compartmental models with explicit reconstructed
morphology, it varies the input-on-dendrite layout (and separately the SAC-SAC inhibition
strength) as the causal variable, and it measures DSGC outcome via DSI and related indices. It
should be cited as the canonical RSME reference, and the specific numerical anchors
(compartment counts, conductances, Exp2Syn parameters, 0.1 nS SAC-SAC, 0.5 nS SAC-DSGC,
spiking threshold -49 mV) should be reused as starting points or baselines in any follow-up
morphology-sweep tasks that embed a DSGC in a SAC network. A limitation is that SACs are
passive-only (no ion channels), so claims about the role of SAC intrinsic properties versus
input layout are by construction bounded - this is explicitly acknowledged in the Discussion,
and the authors note RSME can implement active channels in future studies.

</details>

<details>
<summary>📖 <strong>The functional organization of excitation and inhibition in the
dendrites of mouse direction-selective ganglion cells</strong> — Jain et
al., 2020</summary>

| Field | Value |
|---|---|
| **ID** | `10.7554_eLife.52949` |
| **Authors** | Varsha Jain, Benjamin L Murphy-Baum, Geoff deRosenroll, Santhosh Sethuramanujam, Mike Delsey, Kerry R Delaney, Gautam Bhagwan Awatramani |
| **Venue** | eLife (journal) |
| **DOI** | `10.7554/eLife.52949` |
| **URL** | https://elifesciences.org/articles/52949 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/summary.md) |

This eLife paper asks a specific question about retinal direction selectivity: at what spatial
scale is the direction-selective computation actually performed inside the dendrites of an
ON-OFF DSGC? The question is motivated by decades of theoretical work (Koch, Poggio & Torre
1982; Schachter et al. 2010) proposing dendritic subunits on a 50–100 µm scale, by anatomical
evidence that starburst amacrine cells wrap varicosities around DSGC dendrites with
direction-dependent orientation (Briggman et al. 2011), and by earlier patch-clamp results
(Sivyer & Williams 2013) suggesting subthreshold local tuning. The authors set out to measure
that spatial scale directly in an intact mouse retina.

Their methodology combines two-photon Ca²⁺ imaging of small (3–4 µm) dendritic ROIs in
OGB-1-loaded DSGCs with voltage-gated Na⁺ channel blockade (intracellular QX-314 or bath TTX),
pharmacological dissection of NMDA receptors (D-AP5), genetic disruption of GABA release from
starburst amacrine cells (vGAT-KO), mechanical ablation of individual SACs via sharp-electrode
lesions, and a multi-compartmental NEURON model of a reconstructed DSGC with 177 E/I synaptic
pairs and stochastic release. The combination of imaging, targeted circuit perturbation, and
biophysical simulation is the paper's methodological core.

The headline findings are that DS information exists and is independently generated inside
5–10 µm dendritic segments — an order of magnitude smaller than classic cable-theory
estimates; that noise correlations between dendritic ROIs fall off with a 5.3 µm space
constant; that dendritic Ca²⁺ tuning matches somatic spiking tuning and is sharper than
subthreshold somatic voltage; that NMDA receptors scale responses multiplicatively without
altering PD or DSI; that ablating just 3–7 null-side SACs selectively disrupts DS at
interspersed dendritic hot spots leaving other segments intact; and that a soft dendritic
voltage threshold in the CaV activation range (−55 to −48 mV) is sufficient in the model to
convert homogeneously-tuned inputs into strongly-tuned, locally-independent compartments.

For this project the paper is central. It pins down the empirical target that an ON-OFF DSGC
compartmental model must reproduce: sharp somatic directional tuning that emerges from many
small, locally-tuned dendritic segments whose independence is enforced by dendritic threshold
nonlinearities and by spatially-precise GABAergic inhibition. It also supplies an explicit set
of channel conductances, a morphology reference (Poleg-Polsky & Diamond 2016), a ratio of 1:1
excitatory-to-inhibitory synapse count (177 each), and a concrete prediction — active
dendritic Na⁺/K⁺ channels are expected to sharpen tuning — that we will test directly as part
of our active-vs-passive dendrite experiment. The measured DSI distribution, angular SD of
~32°, and 5–10 µm compartment scale give us quantitative benchmarks to score candidate model
configurations against.

</details>

<details>
<summary>📖 <strong>Retinal direction selectivity in the absence of asymmetric
starburst amacrine cell responses</strong> — Hanson et al., 2019</summary>

| Field | Value |
|---|---|
| **ID** | `10.7554_eLife.42392` |
| **Authors** | Laura Hanson, Santhosh Sethuramanujam, Geoff deRosenroll, Varsha Jain, Gautam B Awatramani |
| **Venue** | eLife (journal) |
| **DOI** | `10.7554/eLife.42392` |
| **URL** | https://elifesciences.org/articles/42392 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/summary.md) |

Hanson et al. revisit one of the most entrenched assumptions in retinal neuroscience: that
direction selectivity in direction-selective retinal ganglion cells (DSGCs) is inherited from
the directionally tuned GABA release of starburst amacrine cells. They ask whether DSGCs can
still compute direction when starburst output itself is no longer directional, a question made
answerable for the first time by combining the Gabra2 conditional KO (which removes mutual SAC
inhibition) with optogenetic stimulation of SACs while bipolar-cell drive is pharmacologically
silenced.

Methodologically, the study integrates four approaches: cell-specific genetics to control SAC
inhibition, ChR2 optogenetics to control excitation of SACs in isolation, whole-cell and loose
cell-attached patch-clamp recordings to read out EPSCs, IPSCs, and spiking in the same DSGCs,
and a multicompartmental NEURON model (built on the Poleg-Polsky and Diamond 2016 DSGC
morphology) to test the computational sufficiency of the proposed mechanisms. Pharmacology
(hexamethonium, SR-95531, DL-AP4, UBP310, CNQX, D-AP5) isolates cholinergic, GABAergic, and
glutamatergic components. Modelling synapses and somatic Na/K/delayed-rectifier conductances
are set to densities matched to prior literature, and release probabilities are parameterised
sigmoidally with direction.

The central findings are that (i) starburst IPSC direction selectivity can be essentially
abolished (DSI about 0.07) while DSGC spiking remains robustly directional; (ii) the residual
DS is explained by a directionally tuned excitation-inhibition temporal offset of up to 50 ms
in the preferred direction, which corresponds to a relatively fixed 25-30 microm spatial
offset across velocities; (iii) this offset is cholinergic in origin, since hexamethonium
delays preferred-direction EPSCs by about 25 ms and collapses the offset; and (iv) the two DS
mechanisms (amplitude and timing) dominate different phases of the response: offsets sharpen
the early phase, amplitude differences broaden and stabilise the peak phase. The NEURON model
reproduces all of these features under both full and reduced wiring.

For this project, Hanson et al. 2019 is directly relevant on three fronts. First, it
constrains the target tuning curve: a single trial-averaged angle-to-AP-frequency curve is
unlikely to capture the dual-mechanism structure, so the target should ideally include
early-versus-peak temporal structure. Second, it provides a specific, reconstructed, publicly
available NEURON model (`geoffder/Spatial-Offset-DSGC-NEURON-Model`) with the exact
conductance recipe, passive properties, and distributed AMPA/ACh/GABA synapses needed as a
baseline for the morphology/conductance/input parametric variation planned here. Third, it
establishes that any realistic DSGC model in this project must treat excitation as two
distinct populations (bipolar AMPA and starburst ACh) with different spatial offsets, because
their differential timing is itself a DS mechanism that must be represented if the optimiser
is to fit mouse DSGC behaviour rather than a generic ON-OFF ganglion cell.

</details>

<details>
<summary>📖 <strong>Non-uniform weighting of local motion inputs underlies dendritic
computation in the fly visual system</strong> — Dan et al., 2018</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_s41598-018-23998-9` |
| **Authors** | Ohad Dan, Elizabeth Hopp, Alexander Borst, Idan Segev |
| **Venue** | Scientific Reports (journal) |
| **DOI** | `10.1038/s41598-018-23998-9` |
| **URL** | https://www.nature.com/articles/s41598-018-23998-9 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`cable-theory`](../../meta/categories/cable-theory/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_s41598-018-23998-9/summary.md) |

Dan, Hopp, Borst and Segev (2018) resolve the long-standing question of how the ~400–600
motion-sensitive dendritic branchlets of a blowfly VS tangential cell are integrated into the
cell's single direction-selective axonal output. They combine two prior *in vivo* datasets —
axonal intracellular recordings and branchlet-level Ca2+ imaging — and fuse them onto six
prototypical 3D reconstructions of VS1, VS2, VS3, VS4, VS5 and VS9 cells by exploiting the
morphological stereotypy of VS cells across specimens. The fused dataset yields up to 116
local receptive fields on a single prototype, enabling the first quantitative test of the rule
by which dendritic RFs are combined into the axonal RF.

The methodology is a steady-state passive cable / compartmental model in NEURON with fixed Rm
= 2,000 Ω·cm² and Ri = 40 Ω·cm and no free parameters. For each branchlet they compute the
electrotonic distance (x/λ), the local input resistance (8–13 MΩ), and — crucially — the
branchlet-to-axon transfer resistance (2.4–3.0 MΩ range, ~20% variability within a cell). They
then compare two integration rules against the experimentally measured axonal receptive field:
uniform average (the null model from Hopp et al.) versus transfer-resistance-weighted average.
A supplementary threshold non-linearity that filters out the smallest dendritic vectors is
added on top.

The headline result is that TR-weighted summation significantly outperforms uniform summation:
for VS5 the difference index drops from 0.411 to 0.293, with the improvement exceeding 2 SD of
a shuffled-weights null distribution. Adding the non-linearity improves the fit further to DI
= 0.283 (VS3), 0.236 (VS4), 0.280 (VS5). Separately, the full inter-branchlet TR matrix (3–4
MΩ) is much smaller than the local branchlet input resistance (8–13 MΩ), establishing that
VS-cell dendritic branchlets are **electrically decoupled and function as independent local
subunits**. The effective membrane time constant (<2 ms) is much shorter than the
motion-detector input timescale, validating the steady-state approximation.

For this literature survey, the paper is included as a borderline entry: it is a single-
morphology-per-cell-type passive-cable study of an invertebrate visual neuron, not a
morphology-variant sweep (the earlier task brief mis-attributed it as "Haag2018 — 200
morphology variants", which was wrong). It is nonetheless a strong reference for (a)
transfer-resistance weighting as the correct passive rule for many-to-one dendritic
integration, (b) the independent-subunit architecture as a passively-derivable property of
dendritic trees, and (c) the methodological pattern of fusing branchlet-level imaging across
specimens onto a prototypical morphology. Translation to vertebrate retinal DSGCs requires
adjusting for active dendritic mechanisms and gap-junctional network effects (the authors flag
axo-axonal coupling between neighboring VS cells, coupling coefficients up to 50%, as one
reason their fit is not perfect), but the core TR-weighting result is a morphology-agnostic
passive-cable prediction that any compartmental DSGC model should reproduce as a baseline
before invoking active conductances.

</details>

<details>
<summary>📖 <strong>Simple integration of fast excitation and offset, delayed
inhibition computes directional selectivity in Drosophila</strong> —
Gruntman et al., 2018</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_s41593-017-0046-4` |
| **Authors** | Eyal Gruntman, Sandro Romani, Michael B. Reiser |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/s41593-017-0046-4` |
| **URL** | https://www.nature.com/articles/s41593-017-0046-4 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_s41593-017-0046-4/summary.md) |

This paper asks how direction selectivity is implemented in Drosophila T4 neurons, the first
site in the fly ON motion pathway where directionally selective signals appear. The motivation
is to resolve which of the classical algorithmic motion detectors \u2014
Hassenstein\u2013Reichardt multiplication, Barlow\u2013Levick veto, or an Adelson\u2013Bergen
motion-energy filter \u2014 the fly circuit actually implements. The authors focus on T4
because prior calcium-imaging evidence had been ambiguous: the indicator is blind to
hyperpolarization and too slow to resolve the sub- ommatidial timing differences that would
distinguish these models.

Methodologically, the study combines targeted in vivo whole-cell patch-clamp of GFP-labelled
T4 cells (n = 17) with a biophysical, compartmental model of a single T4 cell whose morphology
was reconstructed from Janelia FlyEM FIB-SEM. They map the receptive field with
single-position bar flashes and with two-step apparent-motion pairs, extract per-position
onset-time and decay-time, and then fit a passive conductance-based model (99 excitatory and
55 inhibitory synapses on a 344-section dendrite) to the stationary SPFRs. They test
generalization by predicting moving-bar responses the model never saw, and they run three
clean model ablations: remove inhibition, collapse all synapses to the dendritic base, and
replace the whole cell with a single compartment.

The headline findings are that T4's direction selectivity arises from spatially offset fast
excitatory and delayed inhibitory inputs (approximately 6\u00B0 E\u2013I offset along the
PD\u2013ND axis) with invariant excitatory onset times across the receptive field, so there is
no HR-style delay line. Two-step apparent motion produces pure null-direction suppression (DSI
approximately 0.46 on the trailing side versus DSI approximately 0.03 on the leading side),
with no preferred- direction enhancement. The conductance-based model reproduces DSI vs speed
quantitatively for moving stimuli; removing inhibition abolishes DSI at every speed; and
\u2014 critically for morphology-modelling work \u2014 collapsing all synapses to the
dendritic base or using a single- compartment variant reproduces the full-dendrite DSI almost
exactly. The T4 arbor's role is therefore input sampling, not nonlinear integration.

For this project's literature survey on morphology-to-DS modelling, this is the canonical
invertebrate reference and a strong null result: the morphology-related variable that drives
DS in T4 is not dendritic cable geometry but the 1D spatial layout of excitatory and
inhibitory inputs along the PD\u2013ND dendritic axis, combined with a dynamic passive
shunting nonlinearity. That gives our compartmental RGC model a precise contrastive
hypothesis: if dendritic morphology contributes to DS beyond input layout in vertebrate DSGCs,
it must do so via active conductances, asymmetric passive cable properties, or structured
dendritic branching that goes beyond the mechanisms sufficient for T4. We should reuse
Gruntman et al.'s SPFR-to-moving-bar generalization protocol, their DSI = (R_PD \u2212 R_ND) /
R_PD convention, and their collapse-to-base vs full-arbor ablation design as template
comparisons in our own modelling work.

</details>

<details>
<summary>📖 <strong>A Dense Starburst Plexus Is Critical for Generating Direction
Selectivity</strong> — Morrie & Feller, 2018</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.cub.2018.03.001` |
| **Authors** | Ryan D. Morrie, Marla B. Feller |
| **Venue** | Current Biology (journal) |
| **DOI** | `10.1016/j.cub.2018.03.001` |
| **URL** | https://doi.org/10.1016/j.cub.2018.03.001 |
| **Date added** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0013_resolve_morphology_provenance`](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Full summary** | [`summary.md`](../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/summary.md) |

Morrie and Feller ask which morphological feature of the starburst amacrine cell plexus is
necessary for direction-selective tuning in retinal ganglion cells. Prior work established
that asymmetric SAC-to-DSGC inhibition is central to DS, and that SAC dendrites themselves are
tuned to centrifugal motion, but it was unknown whether loss of DS in morphology-mutant mice
reflected broken wiring, broken subcellular computation, or a broken circuit geometry. The
Sema6A-/- mouse offers a clean dissection because it preserves SAC cell number and GABAergic
identity but reduces arbor size and plexus overlap.

The authors combine cell-attached DSGC spike recordings, whole-cell voltage-clamp IPSC
measurements, paired SAC-DSGC patch recordings with dye fills (AlexaFluor488 for DSGCs,
AlexaFluor594 for SACs), 2-photon OGB1 Ca2+ imaging of SAC varicosities, manual morphology
tracing in FIJI Simple Neurite Tracer exported as SWC files to the TREES toolbox, and a custom
IPSC simulation in MATLAB. Mice were p25-120 CNT (ChAT-Cre/nGFP/TrHr) reporter crosses. The
experimental design cleanly separates wiring (paired recordings), subcellular computation
(Ca2+ imaging), and geometric arrangement (reconstructed SAC arbors with varicosity positions
and distal-segment orientations).

Three findings carry the paper. First, DSGC directional tuning collapses in Sema6A-/- because
null-direction inhibition is halved (~4 nS to ~1.5 nS) while preferred-direction inhibition is
unchanged. Second, paired SAC-DSGC recordings show that asymmetric wiring and per-synapse
conductance are preserved. Third, Ca2+ imaging shows that SAC varicosity-level DS is preserved
but that ~30-40% of Sema6A-/- varicosities are not tuned to centrifugal motion; instead their
preferred direction follows the orientation of a short distal (10-40 micrometre) neurite
segment, and a TREES-toolbox-based IPSC simulation with each SAC's measured varicosity
geometry reproduces the observed DSGC IPSC tuning loss.

For this project the paper's relevance is both scientific and operational. Scientifically, it
establishes that our compartmental DSGC model must couple SAC plexus coverage and local
distal-segment orientation to the amplitude and preferred direction of each GABAergic input; a
model that only varies per-synapse weight will miss the dominant mechanism of null-direction
inhibition. Operationally, for task t0013 the paper provides decisive negative evidence: its
Methods describe only SAC reconstructions (FIJI to SWC to TREES), never DSGC reconstructions,
biocytin fills, Neurolucida tracings, a `141009` or `Pair1DSGC` identifier, or a NeuroMorpho
deposition statement. The NeuroMorpho.org linkage of neuron 102976 to this DOI is therefore
not supported by the paper itself and must be resolved by inspecting a different Feller-lab
source (lab repository, earlier paired-recording paper, or unpublished deposition metadata).

</details>

<details>
<summary>📖 <strong>Cross-compartmental Modulation of Dendritic Signals for Retinal
Direction Selectivity</strong> — Koren et al., 2017</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2017.07.020` |
| **Authors** | David Koren, James C. R. Grove, Wei Wei |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2017.07.020` |
| **URL** | https://doi.org/10.1016/j.neuron.2017.07.020 |
| **Date added** | 2026-04-19 |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/summary.md) |

Koren, Grove, and Wei address a gap in the mechanistic understanding of retinal direction
selectivity: how the starburst amacrine cell (SAC) maintains the required balance between
electrotonic isolation and cross-compartmental signal integration in its dendrites, and how
that balance is regulated and coupled to direction-selective ganglion cell (DSGC) output.
Earlier work established that SAC dendritic sectors are semi-independent computational units
with centrifugal preference, but the mechanisms controlling the "semi" part of that isolation
were unknown.

Methodologically the paper combines two-photon GCaMP6 imaging of distal SAC varicosities,
whole-cell patch-clamp of SACs and DSGCs, subregion visual stimulation to dissociate local
from global dendritic activation, a selective pharmacology (LY341495 antagonist and LY354740
agonist) for mGluR2, and mGluR2 knockout mice as an off-target control. Voltage-gated calcium
channel subtypes are identified with omega-conotoxin GVIA (N-type) and omega-agatoxin IVA
(P/Q-type).

The central findings are that (i) the strong centrifugal response of distal SAC varicosities
during full-field motion is partly produced by trans-somatic signal integration from the
opposite side of the dendritic tree; (ii) mGluR2 signaling inhibits N- and P/Q-type VGCCs on
SACs to enforce sufficient electrotonic isolation during centripetal motion; (iii) blocking
mGluR2 selectively enhances preferred-direction IPSCs onto DSGCs (delay **289 ms at 440
um/s**, **147 ms at 1100 um/s**); and (iv) this aberrant inhibition reduces DSGC spiking
specifically at high motion speeds, contributing to the broad speed tuning of the
direction-selective circuit.

For this project's goal of a compartmental DSGC model that matches a target
angle-to-AP-frequency curve, the paper has two concrete implications. First, the IPSC input
model on the DSGC must reflect speed-dependent latency and amplitude arising from SAC
trans-somatic propagation rather than a speed-invariant null-direction inhibition. Second, the
saturation of centrifugal SAC calcium signals and null-direction DSGC IPSCs, even under strong
pharmacological perturbation, suggests that the target tuning curve can be reproduced with a
degenerate set of Na/K conductance combinations (RQ1 "ridge" hypothesis), because upstream
inhibition is the first-order constraint on firing at preferred direction and any well-chosen
conductance combination that preserves somatic excitability will suffice. Active dendritic
conductances in the DSGC (RQ4) can be evaluated against this framework, but the primary
directional signal arrives pre-shaped by SAC compartmental computation, not generated locally
in the DSGC dendrites.

</details>

<details>
<summary>📖 <strong>"Silent" NMDA Synapses Enhance Motion Sensitivity in a Mature
Retinal Circuit</strong> — Sethuramanujam et al., 2017</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2017.09.058` |
| **Authors** | Santhosh Sethuramanujam, Xiaoyang Yao, Geoff deRosenroll, Kevin L. Briggman, Greg D. Field, Gautam B. Awatramani |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2017.09.058` |
| **URL** | https://www.cell.com/neuron/fulltext/S0896-6273(17)30927-3 |
| **Date added** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuron.2017.09.058/summary.md) |

Sethuramanujam and colleagues address a gap in the DSGC direction-selectivity literature: is
the AMPAR-and-inhibition picture of DS generation complete, or do NMDARs also play a
functional role in the adult circuit? Using whole-cell patch-clamp recordings from ON-OFF
DSGCs in mouse retinal wholemount, combined with drifting-grating and moving-bar motion
stimuli and pharmacological block of AMPARs and NMDARs, they answer the question by directly
measuring each receptor component during preferred and null motion.

The methodology combines voltage-clamp at multiple holding potentials to isolate excitatory
and inhibitory components, pharmacological dissection to isolate AMPA and NMDA contributions
within the excitatory component, and matched current-clamp recordings to confirm the
spike-output consequences. The design lets the authors quantify the AMPA/NMDA ratio, its
direction dependence, and the effect of NMDAR block on direction selectivity index separately
at the synaptic-current and spike levels.

The headline result is that DSGCs contain a substantial but functionally silent NMDAR
population that is recruited preferentially during preferred-direction motion and
multiplicatively enhances DS. NMDAR block reduces DSI significantly at both the current and
spike level. The paper also provides quantitative AMPA/NMDA charge ratios that can be used
directly as model-fitting targets.

For this project, the implications are central. DSGC compartmental models in NEURON must
include NMDARs with proper Mg2+ block kinetics on DSGC dendrites; the AMPA-only baseline is
inadequate. NMDAR recruitment depends on dendritic depolarisation, so space-clamp corrections
from Poleg-Polsky and To-Honnuraiah-Stuart apply. Fitting objectives should include the
AMPA/NMDA charge ratio during preferred and null motion, not just peak AMPA current. The
Sethuramanujam measurements provide the quantitative targets our model must hit.

</details>

<details>
<summary>📖 <strong>Species-specific wiring for direction selectivity in the
mammalian retina</strong> — Ding et al., 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nature18609` |
| **Authors** | Huayu Ding, Robert G. Smith, Alon Poleg-Polsky, Jeffrey S. Diamond, Kevin L. Briggman |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/nature18609` |
| **URL** | https://www.nature.com/articles/nature18609 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature18609/summary.md) |

Ding et al. use serial block-face EM to reconstruct the complete synaptic wiring of four
starburst amacrine cells in mouse retina and compare it with the previously characterised
rabbit circuit. The central finding is that mouse SACs receive inhibitory SAC-SAC inputs
exclusively on their proximal dendrites, whereas rabbit SACs receive them distally. The study
is motivated by the need to understand which circuit features -- intrinsic or network-based --
account for direction selectivity of SAC dendrites, and whether that organisation varies
across species.

To interpret the anatomy, the authors construct a 7-SAC network model in Neuron-C with
anatomically measured dendritic diameters, biophysically grounded active conductances (NaV1.8,
Kdr, L-type Ca^2+), and synapse placements derived from the EM data. Mouse-like (proximal
inhibition, 145 um inter-soma spacing) and rabbit-like (distal inhibition, 200 um spacing)
configurations are compared over stimulus velocities 30-2000 um/s. Two-photon calcium imaging
and SR95531 pharmacology confirm the model predictions in vitro.

Key quantitative results: the mouse model remains DS down to ~100 um/s linear velocity,
matching the smaller mouse eye (3 mm axial diameter, ~30 um/deg) to conserve angular velocity
tuning. Distributing BC inputs uniformly reverses direction preference in the model. SAC-SAC
inhibition is necessary for DS at high contrast (300%) and for DS to centrally restricted
stimuli in mouse. Full biophysical parameters (Rm = 10,000 Ohm-cm^2, Ri = 75 Ohm-cm,
NaV1.8/Kdr/Ca^2+ densities per dendritic zone) are tabulated and distributed with the model
code.

For this project, Ding et al. (2016) provides three concrete resources: (1) a fully described
multi-compartmental DS circuit model with biophysical parameters and DSI protocol that can
directly inform DSGC model parameterisation; (2) a design principle -- restrict excitatory
inputs to proximal zones away from the output zone -- guiding AMPA vs. GABA placement in the
DSGC dendritic model; and (3) mouse-specific synaptic geometry (inhibitory inputs at proximal
third, excitatory at proximal two-thirds) to validate against when choosing GABA input
distributions in the project compartmental DSGC model.

</details>

<details>
<summary>📖 <strong>NMDA Receptors Multiplicatively Scale Visual Signals and Enhance
Directional Motion Discrimination in Retinal Ganglion Cells</strong> —
Poleg-Polsky & Diamond, 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2016.02.013` |
| **Authors** | Alon Poleg-Polsky, Jeffrey S. Diamond |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2016.02.013` |
| **URL** | https://www.sciencedirect.com/science/article/pii/S0896627316001069 |
| **Date added** | 2026-04-19 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/summary.md) |

Poleg-Polsky and Diamond investigate how direction-selective ganglion cells (DSGCs) in the
mouse retina amplify visual signals while preserving reliable directional tuning. The central
question is why NMDA receptors are present on DSGC dendrites when direction selectivity can be
computed without them. The answer proposed is that NMDARs provide multiplicative gain --
scaling responses in both the preferred and null directions by the same factor -- which
maintains the direction-selectivity index, increases absolute signal amplitude, and improves
resistance to visual noise.

The experiments combine whole-cell patch-clamp from GFP-labeled DRD4 mouse DSGCs with a
morphologically realistic multicompartmental NEURON model containing 177 AMPAR + 177 NMDAR +
177 GABA_A synapses on reconstructed ON dendrites. Slope-angle analysis distinguishes
multiplicative from additive NMDAR scaling. Two pharmacological manipulations convert
multiplication to addition: removing voltage-dependent Mg2+ block and reversing GABAergic
inhibition to excitation with high-Cl- internal solution. The NEURON model replicates all
experimental PSP and AP responses and predicts additive NMDAR scaling under both
pharmacological conditions.

The key finding is that NMDAR multiplication requires the conjunction of voltage-dependent
NMDAR conductance and directionally tuned GABAergic inhibition. Under noiseless conditions,
NMDAR blockade preserves DSI but reduces AP firing amplitude. Under noisy conditions, ROC
analysis demonstrates significantly better signal discrimination with intact NMDARs than with
AP5 or 0 Mg2+. Dendritic spikes were absent in DRD4 DSGCs; passive propagation proved
sufficient for DS computation.

For this project, the Poleg-Polsky & Diamond NEURON model is the essential template. Its
geometry (single reconstructed DRD4 DSGC), synaptic counts (177 AMPA + 177 GABA on ON
dendrites), and circuit architecture (tuned GABAergic inhibition as stronger ND conductance)
directly match the planned implementation. Available on ModelDB (accession 189347). The paper
validates passive- dendrite sufficiency for project RQ4, constrains NMDAR conductance
Mg2+-block parameters, and establishes ROC accuracy-curve area as the appropriate metric for
comparing DS tuning fidelity across model variants.

</details>

<details>
<summary>📖 <strong>Retinal Circuitry Balances Contrast Tuning of Excitation and
Inhibition to Enable Reliable Computation of Direction Selectivity</strong>
— Poleg-Polsky & Diamond, 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.4013-15.2016` |
| **Authors** | Alon Poleg-Polsky, Jeffrey S. Diamond |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.4013-15.2016` |
| **URL** | https://www.jneurosci.org/content/36/21/5861 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1523_JNEUROSCI.4013-15.2016/summary.md) |

Poleg-Polsky and Diamond ask how the retinal direction-selective circuit, which is organized
as a feedforward inhibitory microcircuit (bipolar cell → starburst amacrine cell →
direction-selective ganglion cell), keeps its excitation / inhibition ratio stable across a
wide contrast range even though the SAC interposes a highly nonlinear dendritic release step.
Using whole-cell recordings, pharmacology, two-photon Ca2+ imaging, and iGluSnFR in mouse
retina, they show that the DSGC E/I ratio is indeed contrast-independent (r = 0.94) and that
this is not because of postsynaptic receptor differences between cholinergic, NMDAR and AMPAR
components, which all share the same contrast sensitivity.

The compensating mechanism lives in the bipolar-cell layer: BCs that drive SACs are far more
contrast-sensitive (detection threshold ~16 % contrast, half-activation ~32 %) than BCs that
drive DSGCs (threshold ~65 %). Direct imaging of SAC dendritic Ca2+ shows that the SAC I/O
transform is steeply sigmoidal (threshold ~38 %, half-activation ~66 %), so the elevated
presynaptic sensitivity of SAC-targeting BCs exactly offsets the SAC nonlinearity, leaving the
feedforward GABAergic output at the DSGC contrast-matched to the direct BC → DSGC excitation.
Single-bouton recordings show this sensitivity difference is between BC subtypes, not within
them, and correlates with distinct IPL stratification.

A stochastic compartmental DSGC model (121 ON-layer compartments; AMPA, NMDA and GABA
conductances with realistic kinetics and Jahr-Stevens NMDA voltage dependence; Hodgkin-Huxley
spike generator) is used to show that matched E/I contrast tuning maximizes suprathreshold
DSI. Shifting E or I along the contrast axis either leaks non-directional null responses
through the circuit or quenches spikes altogether, confirming that the presynaptic
BC-heterogeneity mechanism is functionally necessary, not merely present.

For this project the paper is a **borderline** but important inclusion. The morphology of the
DSGC is held fixed and the primary contribution is circuit-level, so it is not a
morphology-on-DS modeling paper in the strict sense. However, the compartmental DSGC model
with spatially distributed E and I inputs, and the explicit demonstration that the
*distribution* of E/I contrast tuning across dendritic compartments gates reliable DS
computation, make this a key reference for how E/I-on-morphology shapes DS. It should be cited
alongside PolegPolsky2026 when arguing that DSGC dendritic biophysics and synaptic spatial
statistics — not just SAC wiring — determine direction-selective reliability, and its synapse
parameterization can be reused as a validated starting point for our own DSGC simulations.

</details>

<details>
<summary>📖 <strong>A Central Role for Mixed Acetylcholine/GABA Transmission in
Direction Coding in the Retina</strong> — Sethuramanujam et al., 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2016.04.041` |
| **Authors** | Santhosh Sethuramanujam, Amanda J. McLaughlin, Geoffery deRosenroll, Alex Hoggarth, David J. Schwab, Gautam B. Awatramani |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2016.04.041` |
| **URL** | https://www.cell.com/neuron/fulltext/S0896-6273(16)30155-6 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.04.041/summary.md) |

Sethuramanujam et al. (2016) investigate the computational function of co-transmission of ACh
and GABA from SACs onto DSGCs, asking whether the excitatory/inhibitory transmitter mixture at
the same synapse has functional consequences beyond what single-transmitter models predict.
The study is conducted in rabbit retina across natural, low-contrast, and high-contrast visual
stimulation.

The authors combine whole-cell voltage-clamp recordings from DSGCs with pharmacological
isolation of GABA, ACh, and glutamate receptor currents, a linear regression decomposition of
multi-component synaptic inputs, and optogenetic ChR2 activation of SACs while bipolar cell
input is silenced. These tools measure each transmitter contribution independently across
direction and contrast.

The central result is that ACh is the obligatory excitatory initiator at low contrast and
under natural stimuli, while glutamate through NMDA receptors acts as a dependent amplifier
via a nonlinear coincidence detection gate. Optogenetic isolation of the SAC network confirms
that SACs alone encode direction without upstream bipolar cell asymmetry. Both GABA and ACh
from SACs are direction-tuned, and their kinetic differences -- transient ACh vs. sustained
GABA -- contribute to the E/I asymmetry underlying direction selectivity.

For this project, the paper directly constrains the synaptic input parameterisation of a
compartmental DSGC model: cholinergic conductances must be direction-asymmetric and fast,
GABAergic conductances sustained and direction-asymmetric, and NMDA conductances
voltage-dependent with a contrast-dependent activation threshold. These constraints govern the
choice of AMPA, NMDA, and GABA-A conductance waveforms, their spatial distributions across the
dendritic arbor, and their directional weight asymmetries in the compartmental simulation.

</details>

<details>
<summary>📖 <strong>A Role for Synaptic Input Distribution in a Dendritic Computation
of Motion Direction in the Retina</strong> — Vlasits et al., 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2016.02.020` |
| **Authors** | Anna L. Vlasits, Ryan D. Morrie, Alexandra Tran-Van-Minh, Adam Bleckert, Christian F. Gainer, David A. DiGregorio, Marla B. Feller |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2016.02.020` |
| **URL** | https://doi.org/10.1016/j.neuron.2016.02.020 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1016_j.neuron.2016.02.020/summary.md) |

Vlasits et al. (2016) address a longstanding question in retinal direction selectivity:
whether the *location* of excitatory inputs along a starburst amacrine cell dendrite matters,
separately from morphology and network inhibition. They combine four experimental techniques —
visual receptive field mapping with spots and rings, MNI-glutamate uncaging, PSD95-YFP genetic
labeling, and re-analysis of the Briggman et al. connectome — to show that excitatory bipolar
inputs are concentrated on the proximal ~70% of the SAC dendrite, while neurotransmitter
release sites (varicosities) occupy the distal third. Inputs and outputs are spatially
displaced.

Methodologically, the authors build a passive ball-and-stick NEURON model of a reconstructed
SAC dendrite and drive it with simulated moving bars under four synaptic-input distributions
matched in total synapse count and mean density but differing only in spatial placement: the
empirical skewed distribution and a symmetric full-length distribution, each in two variants.
This **morphology-matched symmetric-input control** isolates the effect of input geometry from
cable properties, producing a clean comparison that has become the reference design in the
field. Two-photon Ca2+ imaging of individual varicosities and pharmacological isolation of the
GABA-A component provide the in-tissue test of the model predictions.

The key finding is that the measured proximal-restricted input distribution produces robust
outward-motion-preferring voltage at the distal release zone (varicosity DSI = 0.34 ± 0.23, n
= 25), whereas a density-matched symmetric input distribution does not. Only ~25% of
DSGC-directed release sites overlap with the excitatory receptive field. GABA-A blockade with
gabazine reduces but does not abolish the computation, confirming that dendritic mechanisms
and circuit inhibition act synergistically. Adding voltage-gated Ca2+ channels to the
varicosities amplifies DS multiplicatively but is not required to generate it.

For this project literature survey on how morphology-driven models shape DS, Vlasits2016 is
the canonical reference for two reasons. First, it is the clearest demonstration that
synaptic-input spatial statistics are a morphology-independent degree of freedom that must be
respected by any compartmental DS model. Second, its morphology-matched symmetric-input design
is the methodological template we should import when our own tasks compare cable theory, input
placement, and active channels as DS determinants. Any compartmental SAC or DSGC model we
build that matches morphology alone but ignores input placement should be expected to
underestimate DS or distribute DS incorrectly across the dendrite, and the numerical targets
in this paper (varicosity DSI ~ 0.3, input field extending to ~70% of dendritic radius, ~25%
input-output overlap) are the benchmarks our simulations should hit.

</details>

<details>
<summary>📖 <strong>Space-time wiring specificity supports direction selectivity
in the retina</strong> — Kim et al., 2014</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nature13240` |
| **Authors** | Jinseop S. Kim, Matthew J. Greene, Aleksandar Zlateski, Kisuk Lee, Mark Richardson, Srinivas C. Turaga, Michael Purcaro, Matthew Balkam, Amy Robinson, Bardia F. Behabadi, Michael Campos, Winfried Denk, the EyeWirers, H. Sebastian Seung |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/nature13240` |
| **URL** | https://www.nature.com/articles/nature13240 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nature13240/summary.md) |

Kim et al. answer a 50-year-old question about where direction selectivity arises in the
mammalian retina by combining dense electron-microscopy reconstruction with a minimal
mathematical model. Rather than attributing DS to biophysical properties of the SAC dendrite
itself (an earlier hypothesis that predicts the wrong preferred direction at the soma), they
propose that DS is built into the wiring diagram: BC types with slow visual responses synapse
near the SAC soma, BC types with fast responses synapse far from it, so outward motion
produces synchronous arrival of excitation along the dendrite and inward motion produces
asynchronous arrival.

The test is carried out on the e2198 mouse-retina SBEM dataset using a
deep-convolutional-network AI for voxel oversegmentation and a crowdsourced game, EyeWire, for
the neurite-agglomeration step. Paid lab workers and 5881 volunteer citizen-neuroscientists
reconstructed 79 Off SACs and 195 Off BC axons. Contact area between every BC-SAC pair was
computed, sorted by BC type and by distance from the SAC soma, and compared against a
co-stratification null model based on Peters Rule. The five Off BC types (BC1, BC2, BC3a,
BC3b, BC4) were classified by IPL-stratification profile and validated by mosaic regularity
and density.

The contact analysis reveals a sharp dichotomy: among the five Off BC types, only BC2
(proximal) and BC3a (distal) contact SACs substantially, and published two-photon calcium and
glutamate imaging show BC2 lags BC3a by 50-100 ms, exactly the sign and order required for
outward preferred direction. A linear-nonlinear model with a sustained (BC2) and a transient
biphasic (BC3a) subunit produces DS that subsumes Reichardt and Barlow-Levick detectors as
limiting cases, survives the isopotential-dendrite approximation (matching somatic
intracellular recordings), and suggests mammalian Off-SAC dendrites and *Drosophila* T4/T5
cells implement the same canonical motion operator. A subtle dendritic tilt through the IPL
(20-80 micrometre distance from soma) partially supports the wiring specificity but fails to
fully account for it, demonstrating quantitative violation of Peters Rule.

For the t0027 literature survey on morphology-driven DS modelling, Kim2014 is the canonical
connectome + anatomical-wiring input that every downstream compartmental DSGC/SAC model
(including Poleg-Polsky and Diamond 2026 work) consumes as its substrate. The paper is flagged
as borderline because it is primarily an EM + behavioural-model paper, not a morphology-sweep
paper: the morphology captured is the SAC stratification-depth profile and the BC2/BC3a
proximal/distal contact pattern, not a multi-compartment cable simulation. When reviewing
compartmental DS models, Kim2014 contact-vs-distance curves (Fig. 4d) should be treated as
ground-truth boundary conditions for the excitatory input spatial weighting, and the 50-100 ms
BC2-vs-BC3a lag as the ground-truth input-timing offset. Any compartmental model that cannot
reproduce this wiring is missing the principal mechanism of SAC DS as currently understood.

</details>

<details>
<summary>📖 <strong>Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective
Retinal Ganglion Cells Lack Direction Tuning</strong> — Park et al., 2014</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.5017-13.2014` |
| **Authors** | Silvia J.H. Park, In-Jung Kim, Loren L. Looger, Jonathan B. Demb, Bart G. Borghuis |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.5017-13.2014` |
| **URL** | https://www.jneurosci.org/content/34/11/3976 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/summary.md) |

Park et al. (2014) investigate the synaptic basis of direction selectivity in mouse On-Off
DSGCs, asking whether acetylcholine and glutamate inputs are genuinely directionally tuned
alongside the well-established null-direction GABA from starburst amacrine cells. The study is
motivated by a decade of contradictory voltage-clamp data that appeared to show
preferred-direction-tuned excitatory conductances, implying DS presynaptic release from
bipolar cells and SAC cholinergic terminals.

The authors combine whole-cell patch-clamp with simultaneous two-photon imaging of iGluSnFR
conditionally expressed on DSGC dendrites via CART-Cre mice, applying pharmacological
manipulations (hexamethonium for nicotinic block, gabazine for GABA-A block). Recording the
optical glutamate signal and electrical conductance in the same cell at the same time allows
direct dissociation of presynaptic release directionality from voltage-clamp measurement
artefacts.

The central result is unambiguous: glutamate release lacks directional tuning (iGluSnFR P - N
= +0.073 +/- 0.04, p = 0.95) even while simultaneously recorded excitatory current appears
tuned (+0.35 +/- 0.07 nS, p = 0.00015). Blocking GABA-A receptors with gabazine abolishes
apparent excitatory DS in both modalities, confirming the artefact arises from imperfect space
clamp during strong null-direction inhibition (2.43 +/- 0.31 nS). The DS index of recorded
cells is 0.65 +/- 0.05, establishing a quantitative target for model optimisation.

For this project's compartmental simulation, these results provide three hard constraints: (1)
excitatory inputs (glutamate and acetylcholine) must be modelled as omnidirectional; (2) null-
direction GABA inhibition is the primary DS-generating mechanism with a P - N magnitude of
approximately 2.4 nS; and (3) the target DS index for optimisation is 0.65-0.73 under in vitro
patch-clamp conditions. The space-clamp artefact warns against using apparent excitatory
tuning in experimental voltage-clamp traces to calibrate any model excitatory tuning
parameter.

</details>

<details>
<summary>📖 <strong>Direction selectivity is computed by active dendritic integration
in retinal ganglion cells</strong> — Sivyer & Williams, 2013</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn.3565` |
| **Authors** | Benjamin Sivyer, Stephen R Williams |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn.3565` |
| **URL** | https://www.nature.com/articles/nn.3565 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/summary.md) |

Sivyer and Williams address one of the oldest and most studied computations in the mammalian
retina — the direction-selective response of ON-OFF DSGCs — and ask, at the cellular level,
*where* the selectivity is actually computed. Classical circuit models had concentrated on the
presynaptic starburst amacrine cell and on spatially offset GABAergic input to the DSGC. Prior
single-site recordings had been unable to resolve whether the DSGC itself simply passes along
its synaptic input or performs active, location-specific computation of its own. The authors
reframe the question by introducing dual simultaneous whole-cell patch-clamp recordings from
the DSGC soma and from individual terminal dendritic branches of the same cell, supplemented
by pharmacology (TTX, gabazine, QX-314) and a reconstructed-morphology compartmental
simulation.

Methodologically, the paper combines two-photon-guided patch-clamping of sub-micrometre
terminal dendrites with conventional visual stimulation of ON-OFF DSGCs, and with
voltage-clamp isolation of excitatory and inhibitory synaptic conductances. Dendritic spikes
are identified by their larger amplitude at the dendritic than at the somatic recording site
and by their temporal lead over the somatic action potential — the same criteria used in
canonical cortical dendritic-spike work. The compartmental model, fitted to passive responses
and endowed with distributed voltage-gated sodium and calcium conductances, is used to test
whether the experimental observations imply branch-level spike-initiation zones operating
quasi-independently.

The headline findings are that preferred-direction stimuli drive locally initiated dendritic
spikes in terminal branches which then propagate and boost the somatic drive, while
null-direction stimuli recruit GABAergic inhibition that acts at the same terminal branches to
veto spike initiation before it can escape to the soma. The direction-selectivity index is
close to 1 at the soma under control conditions, and this selectivity is almost entirely lost
when dendritic sodium spikes are blocked. The model reproduces these behaviours when terminal
dendrites carry physiologically plausible densities of voltage-gated sodium and calcium
channels and when inhibitory synaptic input is placed asymmetrically on the preferred-null
axis. Individual terminal branches behave as near-independent direction-selective subunits
whose outputs are pooled at the soma.

For this project literature survey on how morphology shapes DS via computational modelling,
Sivyer2013 sits at the boundary of the modelling bucket: it is primarily an experimental
dual-patch study, but its compartmental simulation supplies the mechanistic bridge between
dendritic geometry and DS computation. It is included with the explicit flag that
voltage-gated channel density is as decisive as branch geometry: morphology-only (passive)
models of DSGCs cannot reproduce the observations of this paper. Any DSGC model we build or
compare against in t0027 must jointly specify dendritic morphology *and* the densities of gNa
and gCa in terminal branches, and must treat terminal branches as quasi-independent
spike-initiation compartments with local GABAergic veto rather than as a single
electrotonically collapsed input.

</details>

<details>
<summary>📖 <strong>Direction selectivity in the retina: symmetry and asymmetry in
structure and function</strong> — Vaney et al., 2012</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nrn3165` |
| **Authors** | David I. Vaney, Benjamin Sivyer, W. Rowland Taylor |
| **Venue** | Nature Reviews Neuroscience (journal) |
| **DOI** | `10.1038/nrn3165` |
| **URL** | https://www.nature.com/articles/nrn3165 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/summary.md) |

This 2012 Nature Reviews Neuroscience article by Vaney, Sivyer and Taylor is the standard
decadal synthesis of retinal direction selectivity. Its research question is how the retina -
within two synapses of the photoreceptors - produces ganglion cells whose spike output prefers
one direction of image motion, and in particular how the three Barlow-Levick computational
ingredients (spatial asymmetry, nonlinearity, time delay) are implemented at the cellular
level. The scope covers On-Off DSGCs, On DSGCs and Off DSGCs in rabbit, rat and mouse, with
the microcircuit-level focus on starburst amacrine cells and bipolar cells as the presynaptic
substrate and on DSGC dendrites as the postsynaptic substrate.

The synthesis is built from four data streams. Morphological work (dye fills, SBF-EM,
Neurobiotin-tracer coupling) defines the bistratified DSGC dendritic geometry and the SAC
mosaic. Pharmacology (GABA_A and nicotinic antagonists) and paired cell recordings pin down
which transmitters and which sides of the SAC carry the directional signal. Calcium imaging of
SAC dendrites under apparent-motion paradigms establishes that individual SAC dendrites are
themselves DS units whose calcium transients are biased toward centrifugal motion.
Developmental experiments (intravitreal GABA and cholinergic drugs, dark-rearing, TTX) show
that the direction-selective wiring is essentially hard-wired.

The headline findings are that null-side SAC-to-DSGC GABAergic inhibition is **~9x larger** in
conductance and **~11x more numerous** in synapses than the preferred-side input, that
cholinergic SAC-to-DSGC excitation is spatially symmetric, and that DSGC dendrites carry
voltage-gated self-propagating dendritic spikes that are immune to shunting by intervening
inhibition once initiated. The authors also raise a provocative methodological caveat - that
reported directional asymmetries in DSGC excitatory currents may reflect somatic voltage-clamp
errors on electrotonically extended dendrites rather than genuine DS glutamatergic or
cholinergic inputs. This leaves the relative pre- vs post-synaptic contributions to the final
spike output partially unresolved.

For this project the review is foundational. It fixes the cell type (On-Off DSGC), the minimum
biophysical geometry (bistratified dendrites, ~150-200 micrometre dendritic field per
sublamina, ~40 micrometre subunit spacing), the dominant directional input (asymmetric
null-side GABAergic inhibition, symmetric cholinergic and glutamatergic excitation), and the
post-synaptic nonlinearity (dendritic spikes). It directly informs Research Question 1
(somatic Na/K conductance combinations must still support spiking under large null-direction
inhibitory conductances), Research Question 3 (AMPA/GABA input density should be calibrated
against the ~9:1 null/preferred IPSC amplitude and isotropic EPSC), and Research Question 4
(active vs passive dendrites should be compared against the dendritic-spike substrate the
authors endorse). Its voltage-clamp-error argument is a direct caution against over-fitting to
published excitatory-current directionality.

</details>

<details>
<summary>📖 <strong>Wiring specificity in the direction-selectivity circuit of the
retina</strong> — Briggman et al., 2011</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nature09818` |
| **Authors** | Kevin L. Briggman, Moritz Helmstaedter, Winfried Denk |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/nature09818` |
| **URL** | https://www.nature.com/articles/nature09818 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/summary.md) |

Briggman, Helmstaedter, and Denk (2011) address whether direction selectivity in mouse On-Off
DSGCs requires a structural wiring asymmetry or merely functional differences in synapse
strength within an anatomically symmetric circuit. Prior patch-clamp studies had established
that inhibitory input from SACs is asymmetric -- stronger from null-side SACs -- but could not
determine whether this reflected more contacts or stronger individual synapses, nor whether
SAC dendrite orientation rather than soma location was the relevant factor.

The authors first used two-photon calcium imaging with OGB-1 to identify preferred directions
of 25 On-Off DSGCs in a 300 x 300 um mouse retinal region, then fixed the identical tissue and
acquired a 60 x 350 x 300 um SBEM volume at 16.5 x 16.5 x 23 nm resolution. Manual skeleton
tracing in KNOSSOS yielded 6 DSGC and 24 SAC dendritic trees; 831 putative SAC-to-DSGC
synapses were annotated at varicose contact sites and confirmed by ultrastructural criteria.

The data reveal a striking structural asymmetry: SAC dendrites oriented antiparallel to a DSGC
preferred direction preferentially form synapses with that cell (mean dendrite-to-null angle
165.2 +/- 51.7 degrees; 524 vs. 41 synapses from null vs. preferred-side somata, ~12.8:1).
Critically, when soma-soma axis and dendrite orientation conflict, dendrite orientation wins:
connected dendrites run 24.3 +/- 2.8 degrees closer to the null axis, confirming individual
SAC branches as independent synaptic selectors.

For this project compartmental DSGC model, these data establish the structural baseline for
inhibitory input placement: asymmetric by dendrite orientation, concentrated from
null-direction SAC branches distributed across the full DSGC dendritic field. Any model using
spatially uniform inhibitory placement or relying solely on weight asymmetry is inconsistent
with this structural evidence. The paper also directly cites Schachter et al. (2010), a
computational DSGC model in which dendritic spikes amplify SAC-derived inhibition, connecting
this anatomy paper directly to the biophysical modelling literature this project builds upon.

</details>

<details>
<summary>📖 <strong>Two distinct types of ON directionally selective ganglion cells
in the rabbit retina</strong> — Hoshi et al., 2011</summary>

| Field | Value |
|---|---|
| **ID** | `10.1002_cne.22678` |
| **Authors** | Hideo Hoshi, Lian-Ming Tian, Stephen C. Massey, Stephen L. Mills |
| **Venue** | Journal of Comparative Neurology (journal) |
| **DOI** | `10.1002/cne.22678` |
| **URL** | https://onlinelibrary.wiley.com/doi/10.1002/cne.22678 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1002_cne.22678/summary.md) |

Hoshi et al. (2011) demonstrate that the rabbit ON DS ganglion cell population, treated as a
single type for decades, actually comprises two distinct subtypes separable on six independent
criteria: tracer-coupling pattern, IPL stratification depth, dendritic branching complexity,
response latency, temporal transience, and cholinergic pharmacology. The study uses targeted
acridine-orange-guided recording and intracellular Neurobiotin/Lucifer Yellow injection in
isolated rabbit retinas, characterising 45-52 cells of each subtype -- the largest systematic
ON DS morphology-physiology dataset at the time of publication.

The uncoupled (sustained) subtype ramifies within the ON cholinergic band (~77% IPL depth),
cofasciculates with starburst amacrine dendrites, fires with long latency (381 ms peak) and
sustained character, is never tracer-coupled, and responds strongly to nicotine -- consistent
with the starburst-GABA direction-selectivity model. The coupled (transient) subtype
stratifies distal to the ChAT band (~57% IPL depth), does not cofasciculate with starburst
processes, fires with short latency (71 ms) and transient character, is gap-junction coupled
to 60-190 GABA-positive amacrine cells, and shows minimal nicotine sensitivity -- implying a
non-starburst directional mechanism.

Key quantitative findings: retroflexive terminal processes 14.7 vs. 2.4 (t(94) = 14.52, p <
0.001), dendritic self-crossings 16.5 vs. 4.6 (t(94) = 11.71, p < 0.001), stratification 57%
vs. 77% IPL depth (~3 um separation, confirmed 100% in direct crossings), and response latency
70.7 vs. 381.0 ms (p < 0.01). The two morphological measures together produce complete
population separation across 96 cells. Despite these mechanistic differences, both subtypes
produce equivalent directional output: three cardinal preferred axes, ~100 um/s preferred
velocity, and DSI ~0.66-0.67.

For the current project modelling a single ON DSGC compartmentally and optimising against a
target angle-to-AP-frequency tuning curve, this paper provides essential morphological
constraints. The uncoupled (sustained) subtype -- with high dendritic density, stratification
within the starburst band, and starburst-GABA input geometry -- is the appropriate target cell
type. Key validation benchmarks: DSI ~0.66, preferred velocity ~100 um/s, peak response
latency ~381 ms, stratification at ~77% IPL depth, eccentricity-area slope 0.0605 mm2/mm.
These constrain the morphology, wave- stimulus parameters, and response targets for
compartmental simulation.

</details>

<details>
<summary>📖 <strong>Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection
of Motion in a Simulation of the Direction-Selective Ganglion Cell</strong>
— Schachter et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1000899` |
| **Authors** | Michael J. Schachter, Nicholas Oesch, Robert G. Smith, W. Rowland Taylor |
| **Venue** | PLoS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1000899` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000899 |
| **Date added** | 2026-04-19 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`cable-theory`](../../meta/categories/cable-theory/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/summary.md) |

Schachter, Oesch, Smith & Taylor (2010) ask how the rabbit On-Off direction-selective ganglion
cell converts weakly directionally tuned synaptic input (PSP DSI ~0.2) into strongly tuned
spike output (spike DSI ~0.8). The scope is a single-cell biophysical explanation: given the
known circuitry (starburst amacrine cells providing presynaptic DS, spatially offset
postsynaptic inhibition) and the known cell (anatomical DSGC morphology with active
dendrites), can the measured transformation be reproduced, and what is each mechanism
contribution? This is motivated by prior in vitro evidence from Oesch et al. (2005) that each
somatic spike is triggered by a dendritic spike, and by the unresolved question of whether
postsynaptic inhibition alone can account for DS.

The methodology is a NeuronC compartmental simulation of a reconstructed DSGC with
Hodgkin-Huxley Na, Kv, Kv4, and Ca channels in the dendrites and soma, driven by AMPA-like
excitatory and GABA-A-like inhibitory synapses whose conductances and timings match published
voltage-clamp data. Stimulation protocols include single-synapse threshold mapping, paired
excitation+inhibition titration, and full 12-direction drifting-bar experiments. Key design
decisions include electrically compartmentalizing the dendrites via high Rm and thin distal
branches (Rin >1 GOhm), using uniform or graded dendritic gNa (**40 mS/cm^2** or **45 to 20
mS/cm^2**), and systematically removing each DS mechanism to isolate its contribution.

The headline results are that local dendritic spike thresholds act as ~4x nonlinear amplifiers
of PSP-level DS; that physiological inhibition (**~4-10 nS**) can prevent spike initiation but
cannot block propagation (which would require ~85 nS); that presynaptic DS from SACs is the
more robust mechanism across the arbor while postsynaptic inhibition dominates only at distal
tips; and that an intrinsic dendritic geometric effect actually opposes the desired DS on the
preferred side, requiring network DS to be strong enough to overcome it. Somatic voltage-clamp
additionally underestimates distal conductances by 40-100%.

For the present project compartmental modeling of DSGCs, this paper provides a concrete
reference design (channel densities, synapse conductances, inhibition placement, morphology
source) and three load-bearing predictions to reproduce: (i) the 4x amplification of DSI from
PSPs to spikes via dendritic Na, (ii) the initiation-vs-propagation asymmetry for inhibition,
and (iii) the compartmentalized-subunit structure of the tree. It also establishes that
presynaptic DS cannot be omitted from a DSGC model intended to match physiological spike
tuning and gives quantitative guidance on how to calibrate voltage-clamp-derived conductances
for use in simulation.

</details>

<details>
<summary>📖 <strong>Synaptic inputs and timing underlying the velocity tuning of
direction-selective ganglion cells in rabbit retina</strong> — Sivyer et
al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1113_jphysiol.2010.192716` |
| **Authors** | Benjamin Sivyer, Michiel Van Wyk, David I. Vaney, W. Rowland Taylor |
| **Venue** | The Journal of Physiology (journal) |
| **DOI** | `10.1113/jphysiol.2010.192716` |
| **URL** | https://doi.org/10.1113/jphysiol.2010.192716 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/summary.md) |

The paper asks why two morphologically distinct direction-selective ganglion cells in the
rabbit retina, the bistratified ON-OFF DSGC and the monostratified ON DSGC, have different
velocity tuning despite sharing the same directional computation. Using a combined
extracellular-spiking and whole-cell voltage-clamp protocol in the isolated rabbit retina, the
authors record spiking direction-velocity tuning and then isolate the light-evoked excitatory
and inhibitory synaptic conductances under voltage clamp at the chloride and cation reversal
potentials respectively.

Methodologically, the work is an application of the now-standard two-conductance decomposition
to a velocity-tuning question: the same drifting-grating and local-flicker stimuli are
presented under current- and voltage-clamp, and conductances are computed from
holding-potential-dependent currents while sodium channels are blocked with intracellular
QX-314. Direction tuning is quantified with a DSI and von Mises kappa; temporal tuning is
quantified by measuring the peak excitatory and inhibitory conductances as a function of
temporal frequency. Cell types are confirmed post hoc by dye-fill morphology to ensure that
reported differences are not confounded by misclassification.

The central finding is that the direction-selective mechanism itself is identical in the two
cell types (preferred-side excitation, null-side inhibition, with GI,N/GI,P around 3.4 and
GE,P/GE,N around 1.6) but that the velocity bandwidth differs because the ON DSGC receives a
transient inhibitory conductance that precedes a slower sustained excitatory conductance, and
the ratio of inhibition to excitation grows with temporal frequency. In ON-OFF DSGCs, by
contrast, both conductances are approximately flat from 0.5 to 8 Hz, producing the broad
velocity response for which these cells are known.

For this project, the paper is load-bearing because it converts the qualitative statement that
ON DSGCs prefer slow motion into a quantitative recipe for the inputs of a compartmental
model: spatially asymmetric preferred/null conductance ratios, temporally mismatched rise and
decay kinetics, and a specific lead-lag offset between inhibition and excitation. These
constraints directly inform both the EPSP/IPSP amplitude-and-kinetics sweep and the
wave-stimulus protocol described in the project scope, and supply a matched ON vs ON-OFF
comparison framework against which the model velocity-tuning output can be validated.

</details>

<details>
<summary>📖 <strong>Physiological properties of direction-selective ganglion cells in
early postnatal and adult mouse retina</strong> — Chen et al., 2009</summary>

| Field | Value |
|---|---|
| **ID** | `10.1113_jphysiol.2008.161240` |
| **Authors** | Minggang Chen, Shijun Weng, Qiudong Deng, Zhen Xu, Shigang He |
| **Venue** | The Journal of Physiology (journal) |
| **DOI** | `10.1113/jphysiol.2008.161240` |
| **URL** | https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.2008.161240 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2008.161240/summary.md) |

Chen et al. (2009) investigate the electrophysiology of ON-OFF direction-selective retinal
ganglion cells across postnatal development in the C57BL/6N mouse, asking when directional
computation first appears and whether visual experience shapes its development. Using
whole-cell patch clamp in the isolated retina, they record from DSGCs at P11, P13, P18, and
adulthood, and test mice reared in complete darkness from P0-P11 and P0-P30.

The approach combines loose-patch identification (DSI > 0.3 threshold), whole-cell
voltage-clamp for EPSC kinetics at -65 mV and 0 mV, and current-clamp for excitability and
directional tuning curves (12 directions, 30-degree spacing, bar 100 um x 500 um at
approximately 750 um/s). Cells were morphologically confirmed as bistratified ON-OFF DSGCs by
intracellular dye fills.

The central result is a developmental dissociation: spike counts are roughly half adult values
at P11 (ON: **21.2 +/- 4.4** vs adult **42.9 +/- 5.1 spikes**; peak rate **95.9** vs **166.4
Hz**), EPSC kinetics are significantly slower (*p* < 0.0001), and synaptic reliability is
markedly reduced -- yet DSI and tuning-curve half-width are adult-equivalent at all ages (*p*
> 0.05). Dark rearing does not alter directional tuning, confirming the circuit is fully
light-independent.

For this project, Chen et al. (2009) supply the primary empirical validation target. The
quantitative tuning metrics (DSI, half-width) from the standardised 12-direction protocol
define the target angle-to-AP-frequency relationship the compartmental model must reproduce.
The specific stimulus parameters should be replicated verbatim in the model wave protocol. The
robustness of directional tuning to excitability variations motivates sensitivity analyses in
which somatic Na/K conductances are varied widely without expecting the tuning curve to
collapse.

</details>

<details>
<summary>📖 <strong>A Dendrite-Autonomous Mechanism for Direction Selectivity in
Retinal Starburst Amacrine Cells</strong> — Hausselt et al., 2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pbio.0050185` |
| **Authors** | Susanne E. Hausselt, Thomas Euler, Peter B. Detwiler, Winfried Denk |
| **Venue** | PLoS Biology (journal) |
| **DOI** | `10.1371/journal.pbio.0050185` |
| **URL** | https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0050185 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pbio.0050185/summary.md) |

Hausselt, Euler, Detwiler, and Denk (PLoS Biology 2007) ask whether direction selectivity in
mouse retinal starburst amacrine cells is produced by the network of amacrine-cell inhibitory
interactions or by computation intrinsic to a single SAC dendritic tree. They combine somatic
whole-cell recordings during radial circular-wave visual stimulation, two-photon Ca2+ imaging
at dendritic tips, pharmacological block of GABA and glycine receptors, and a morphologically
detailed NEURON compartmental model. The central question has clear consequences for retinal
motion processing, because the answer determines whether the DSGC inherits a pre-computed
directional signal or constructs DS itself from symmetric amacrine input.

Methodologically, the authors isolate the nonlinear component of the somatic response by
Fourier decomposition and report harmonic (F2+) amplitudes rather than raw peak voltages, a
choice that cleanly separates dendritic nonlinearity from passive cable response. The
compartmental model combines reconstructed SAC morphology, tonic AMPA input producing a
soma-to-tip voltage gradient, HVA Ca2+ channels with conventional Hodgkin-Huxley kinetics, and
slow Cl- kinetics, and it sweeps dendritic length as the key geometric parameter.

The headline findings are that the F2/F1 harmonic ratio is 2-3x larger for centrifugal than
centripetal motion, that this asymmetry survives a full GABA-A + GABA-C + glycine block, that
distal dendrites are tonically depolarized by 15-20 mV relative to the soma thanks to tonic
glutamatergic drive, and that abolishing HVA Ca2+ channels with Cd2+ eliminates the DS
harmonic. In simulation, DSI drops from roughly 0.35 at natural (~150 µm) dendrites to roughly
0.12 at shortened (~50 µm) dendrites, establishing dendritic length as a first-order
determinant of DS magnitude, and all three ingredients — gradient, HVA channels, slow Cl-/Ca2+
kinetics — must be present for the full effect.

For this project literature survey on how computational modeling of neuronal morphology shapes
direction selectivity, Hausselt2007 is a foundational anchor despite targeting SACs rather
than DSGCs. It establishes the compartmental-modeling toolkit (NEURON on reconstructed
morphology with tonic synaptic drive and HVA Ca2+ channels), the dendritic-length-versus-DSI
scaling curve that any subsequent SAC or DSGC morphology sweep should benchmark against, and
the SAC-dendrite as autonomous computational unit framing that determines how much of DSGC DS
can be attributed to pre-inherited presynaptic signals. Any DSGC morphology-DS model built
downstream of this work must decide whether to hold the SAC input fixed, re-simulate it with
Hausselt-style biophysics, or abstract it into an effective directional conductance.

</details>

<details>
<summary>📖 <strong>Direction-Selective Dendritic Action Potentials in Rabbit
Retina</strong> — Oesch et al., 2005</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2005.06.036` |
| **Authors** | Nicholas Oesch, Thomas Euler, W. Rowland Taylor |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2005.06.036` |
| **URL** | https://www.sciencedirect.com/science/article/pii/S089662730500646X |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md) |

Oesch, Euler, and Taylor address a central unresolved question in retinal direction
selectivity: why does a ganglion cell whose somatic subthreshold EPSPs are only weakly
directional produce spike output that is sharply tuned to the preferred direction of motion?
By combining whole-cell current-clamp recordings from ON-OFF DSGCs in flat-mounted rabbit
retina with focal and dendritic TTX application, intracellular QX-314, controlled somatic
hyperpolarization, and two-photon Ca2+ imaging of dendritic arbors, they dissect the spatial
origin of the spikes that drive DSGC output during visual stimulation.

The headline finding is a bimodal spike amplitude distribution - large ~55 mV somatic action
potentials and small ~7 mV dendritic spikelets - that can be separated by any of three
independent manipulations (somatic TTX, QX-314, somatic hyperpolarization). The dendritic
spikelets inherit the full directional tuning of the somatic output (DSI ~0.6-0.7),
superimpose at sub-somatic-refractory intervals, and are selectively suppressed by puffing TTX
onto the dendrites (reducing light-evoked spikes by ~42% while barely affecting
depolarization-evoked somatic spikes). Calcium imaging confirms that the dendrites host
functional TTX-sensitive Na+ channels active during light-driven responses.

Mechanistically, the authors argue that direction selectivity is computed by dendritic spike
failure: locally offset GABAergic inhibition from starburst amacrine cells, positioned between
bipolar-cell excitation and the soma along the null-direction pathway, shunts dendritic spikes
before they can reach the soma. In the preferred direction the inhibition is distal to the
excitation, so dendritic spikes propagate successfully. This model naturally explains the
nondirectional zone on the preferred side of the receptive field and the preferred-side
receptive field offset.

For a DSGC compartmental modeling project, this paper is foundational. It supplies the
quantitative targets (somatic PSP amplitudes of ~12 mV across all directions, somatic
threshold near -49 mV, dendritic spikelet amplitude ~7 mV, spike DSI ~0.7 versus PSP DSI ~0.1)
that any biophysical simulation must reproduce, and it specifies the qualitative requirements:
active dendrites with distributed Na+ channels, multiple independent initiation zones,
on-the-path starburst inhibition, and a near-unity dendritic-to-somatic spike coupling. Any
model that relies on passive dendrites and a single somatic threshold cannot reach the
observed tuning sharpness and should be rejected on quantitative grounds.

</details>

<details>
<summary>📖 <strong>Direction selectivity in a model of the starburst amacrine
cell</strong> — Tukker et al., 2004</summary>

| Field | Value |
|---|---|
| **ID** | `10.1017_S0952523804214109` |
| **Authors** | John J. Tukker, W. Rowland Taylor, Robert G. Smith |
| **Venue** | Visual Neuroscience (journal) |
| **DOI** | `10.1017/S0952523804214109` |
| **URL** | https://www.cambridge.org/core/journals/visual-neuroscience/article/abs/direction-selectivity-in-a-model-of-the-starburst-amacrine-cell/BEFF3097D9C22BE07CFA6F5AA3BE4095 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`cable-theory`](../../meta/categories/cable-theory/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1017_S0952523804214109/summary.md) |

Tukker, Taylor, and Smith address a specific puzzle raised by Euler et al. (2002): SBAC
dendritic tips show direction-selective calcium signals even with GABAa/c blocked, so where
does the DS come from? The authors hypothesize that the answer is geometry. Their scope is a
passive, excitatory-only SBAC with realistic or parameterizable morphology; their motivation
is that the SBAC is the dominant source of directional inhibition onto DSGCs, so explaining
SBAC DS bounds the morphology-to-DSGC mapping.

The method is a full Neuron-C compartmental simulation built on two digitized rabbit SBACs and
a procedural artificial-morphology generator, driven by a semirandom bipolar array (200-300
synapses) with physiological cone and synaptic dynamics. They systematically manipulate
independent geometric variables — first-branch distance, distal branching density,
dendritic-tree radius, electrotonic length constant, compartment resolution, and per-dendrite
length variability — and read out DSI at 16 dendritic tips and the soma for bars, spots,
annuli, and gratings. An optional Q-type Ca2+ channel layer provides the voltage-to-release
amplification step.

The headline findings are that (a) morphology alone generates DSI ~ 0.2 at dendritic tips for
bars and DSI up to ~0.9 for gratings; (b) the mechanism is the direction-dependent summation
of a local tip-EPSP with a soma-mediated global EPSP, with optimal electrotonic length ~
dendritic spread; (c) DS is surprisingly robust to branching detail but sensitive to distal
synapse count and to symmetry-breaking in dendritic length; and (d) a Ca2+-channel threshold
can amplify the voltage DSI roughly threefold in intracellular calcium concentration.

For this project, Tukker 2004 is the canonical starting point for morphology as a causal
variable for DS. It fits the inclusion criteria with the caveat that the cell modeled is the
SBAC rather than the DSGC itself (borderline — flagged in Overview). Its artificial-morphology
methodology, DSI definition, and local-global summation framing should be treated as reference
points when comparing to downstream DSGC-centric modeling work, and its demonstration that
passive-only, inhibition-free morphology can yield strong DS establishes the baseline any more
complex retinal DS model must improve upon.

</details>

<details>
<summary>📖 <strong>Balanced inhibition underlies tuning and sharpens spike timing
in auditory cortex</strong> — Wehr & Zador, 2003</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nature02116` |
| **Authors** | Michael Wehr, Anthony M. Zador |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/nature02116` |
| **URL** | https://doi.org/10.1038/nature02116 |
| **Date added** | 2026-04-20 |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |
| **Added by** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Full summary** | [`summary.md`](../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature02116/summary.md) |

Michael Wehr and colleagues (2003) published "Balanced inhibition underlies tuning and
sharpens spike timing in auditory cortex" in Nature. The paper is included in this task's
survey because it contributes to the "E-I balance temporal co-tuning" theme of
synaptic-integration priors relevant to the direction-selective retinal ganglion cell (DSGC)
compartmental model.

CrossRef did not return a machine-readable abstract for this paper. The paper's claims must
therefore be read directly from the publisher PDF before being used in the DSGC model-fitting
pipeline.

The paper's primary significance for this project is its contribution to the "E-I balance
temporal co-tuning" evidence pool. The answer asset
`assets/answer/synaptic-integration-priors-for-dsgc-modelling/` records which DSGC model prior
(rise/decay time constant, attenuation factor, E-I lag, asymmetry ratio, or
shunting-inhibition location dependence) this paper supplies, together with the numerical
value when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

</details>

<details>
<summary>📖 <strong>Directionally selective calcium signals in dendrites of starburst
amacrine cells</strong> — Euler et al., 2002</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nature00931` |
| **Authors** | Thomas Euler, Peter B. Detwiler, Winfried Denk |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/nature00931` |
| **URL** | https://doi.org/10.1038/nature00931 |
| **Date added** | 2026-04-20 |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../meta/categories/direction-selectivity/) |
| **Added by** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Full summary** | [`summary.md`](../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature00931/summary.md) |

Thomas Euler and colleagues (2002) published "Directionally selective calcium signals in
dendrites of starburst amacrine cells" in Nature. The paper is included in this task's survey
because it contributes to the "SAC-to-DSGC inhibitory asymmetry" theme of synaptic-integration
priors relevant to the direction-selective retinal ganglion cell (DSGC) compartmental model.

CrossRef did not return a machine-readable abstract for this paper. The paper's claims must
therefore be read directly from the publisher PDF before being used in the DSGC model-fitting
pipeline.

The paper's primary significance for this project is its contribution to the "SAC-to-DSGC
inhibitory asymmetry" evidence pool. The answer asset
`assets/answer/synaptic-integration-priors-for-dsgc-modelling/` records which DSGC model prior
(rise/decay time constant, attenuation factor, E-I lag, asymmetry ratio, or
shunting-inhibition location dependence) this paper supplies, together with the numerical
value when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

</details>

<details>
<summary>📖 <strong>Diverse Synaptic Mechanisms Generate Direction Selectivity in
the Rabbit Retina</strong> — Taylor & Vaney, 2002</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.22-17-07712.2002` |
| **Authors** | W. Rowland Taylor, David I. Vaney |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.22-17-07712.2002` |
| **URL** | https://www.jneurosci.org/content/22/17/7712 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.22-17-07712.2002/summary.md) |

Taylor and Vaney (2002) ask whether direction selectivity in rabbit On-Off DSGCs arises from
directional upstream circuitry (presynaptic), from local postsynaptic E/I interactions in the
dendrites, or from a combination of both. The motivation is to resolve a contradiction between
their own 2000 study (postsynaptic conclusion) and a contemporaneous turtle study (presynaptic
conclusion), using a more complete conductance analysis in rabbit retina.

The approach is whole-cell voltage clamp in whole-mount retina with cesium-gluconate and
QX-314 to block intrinsic voltage-gated currents, enabling linear I-V relationships from which
synaptic conductance and reversal potential are extracted every 10 ms across 9 holding
potentials. Excita- tory and inhibitory conductances are isolated by two-component
decomposition at assigned reversal potentials (Ve ~0 mV, Vi ~-65 mV). Spatial offsets of
inhibition are computed from inter- direction timing differences of conductance peaks,
assuming centred receptive fields.

Three mechanisms are found to coexist: preferred-direction excitation (**1.66x** on, **1.36x**
off), null-direction inhibition (**3.31x** on, **1.40x** off), and a **160 um** postsynaptic
spatial offset of off-inhibition with no equivalent in the on-arbor. The on-arbor relies
chiefly on the two presynaptic asymmetries; the off-arbor additionally uses the postsynaptic
spatial offset. Total conductance is nearly balanced across directions (~118% null/preferred),
because directional excitation and inhibition partially cancel. Both subarbors achieve
identical directional tuning (D ~0.56) through distinct mechanisms, demonstrating
within-neuron functional heterogeneity.

For this project, Taylor and Vaney (2002) is the primary empirical anchor for synaptic input
parameters in the DSGC compartmental model. The null/preferred Gi ratios (**3.31x** on,
**1.40x** off) constrain the inhibitory conductance asymmetry that the model must reproduce.
The 160 um inhibitory spatial offset in the off-subarbor specifies the spatial profile of
inhibitory synapse placement. The push-pull E/I structure implies both excitatory and
inhibitory conductances must be directionally modulated. The large cell-to-cell variability
justifies treating E/I ratios as free parameters in the optimisation, bounded by the reported
means and standard deviations.

</details>

<details>
<summary>📖 <strong>Dendritic Computation of Direction Selectivity by Retinal
Ganglion Cells</strong> — Taylor et al., 2000</summary>

| Field | Value |
|---|---|
| **ID** | `10.1126_science.289.5488.2347` |
| **Authors** | W. Rowland Taylor, Shigang He, William R. Levick, David I. Vaney |
| **Venue** | Science (journal) |
| **DOI** | `10.1126/science.289.5488.2347` |
| **URL** | https://www.science.org/doi/10.1126/science.289.5488.2347 |
| **Date added** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cells`](../../meta/categories/retinal-ganglion-cells/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1126_science.289.5488.2347/summary.md) |

Taylor et al.'s 2000 Science paper resolves a decades-long question about where in the retinal
circuit the direction-selectivity computation actually happens. By combining whole-cell
patch-clamp recording from rabbit DSGCs with voltage-clamp separation of excitatory and
inhibitory synaptic currents and with pharmacological block of inhibitory transmission, the
authors demonstrate that DSGCs receive a strongly direction-asymmetric inhibitory input and
that the nonlinear interaction between excitation and inhibition responsible for the observed
direction-selective spike output takes place postsynaptically in the DSGC dendrites.

The experimental design is paradigmatic for the field. Moving-bar visual stimuli are presented
in 12 directions; excitatory and inhibitory synaptic currents are isolated by clamping at
appropriate holding potentials; and pharmacological dissection (picrotoxin, SR-95531,
glutamate receptor antagonists) establishes which circuit elements carry the DS signal. The
finding that the direction-selectivity index (DSI) of the spike output is abolished by
blockade of inhibition, while the excitatory input is only weakly direction-tuned on its own,
nails down inhibition as the DS- carrying signal.

The mechanistic conclusion — that the nonlinearity is postsynaptic and dendritic — vindicates
the Koch, Poggio & Torre 1982 theoretical framework and elevates shunting inhibition from a
theoretical possibility to an experimentally established computation in a specific neural
circuit. This establishes the mammalian DSGC as one of the cleanest examples of biophysical
dendritic computation in vertebrate neuroscience.

For this project, the paper is the single most important experimental constraint on DSGC
compartmental modelling. Our NEURON DSGC models must: (1) receive asymmetric inhibitory inputs
with the DS signal in the inhibition, not the excitation; (2) produce DS spike output via
postsynaptic dendritic shunting, not via presynaptic asymmetry; (3) lose the DSI when
dendritic inhibition is removed; (4) preserve the DSI across a range of stimulus velocities.
Any DSGC model that fails these Taylor-et-al-2000 tests is not capturing the real biology and
should not be used to make predictions about retinal circuit function.

</details>

<details>
<summary>📖 <strong>Dendritic asymmetry cannot account for directional responses of
neurons in visual cortex</strong> — Anderson et al., 1999</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_12194` |
| **Authors** | J. C. Anderson, T. Binzegger, O. Kahana, K. A. C. Martin, I. Segev |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/12194` |
| **URL** | https://www.nature.com/articles/nn0999_820 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_12194/summary.md) |

Anderson, Binzegger, Kahana, Martin and Segev set out to test, experimentally and
computationally, Livingstone’s 1998 hypothesis that the direction selectivity of neurons in
primary visual cortex arises from tangential asymmetries of the basal dendritic tree acting as
a delay line. The question is central to any theory that links neuronal morphology to
direction-selective computation, because it asks whether the SAC/DSGC morphology-causal story
generalizes to neocortex.

Their method has two prongs. Experimentally, they combine in-vivo extracellular and
intracellular recording of 32 cat V1 neurons with post-hoc HRP filling, osmicated resin
embedding, three-dimensional reconstruction and retinotopy-aligned tangential projection, and
they measure the angular offset between each cell’s preferred direction and its dendritic
bias. Computationally, they build a detailed NEURON compartmental model of reconstructed cat
and monkey Meynert cells — the most dendritically asymmetric cortical cells known, with basal
dendrites up to 770 micrometres — in which 2,000 AMPA synapses are swept distal-to-proximal or
proximal-to-distal along one or two dendrites, with a somatic GABA_A synapse providing
null-direction shunting inhibition 2 ms after the nearest excitatory input.

The headline finding is that the morphology-causal hypothesis fails on both prongs. The
angular difference between dendritic bias and preferred direction is uniformly distributed
(K-S p = 0.23), robust across bin sizes and across choices of distal, middle or total
dendritic length; only 2 of 32 neurons have their longest dendrite at 180 degrees to
preferred, consistent with chance. Even the Meynert best case produces a velocity-tuned
response only at an optimal sweep velocity of ~77 degrees/s — an order of magnitude faster
than measured V1 tuning of ~10-20 degrees/s — and this peak collapses as soon as inputs are
mapped onto a second, opposing dendrite. The optimum is set by the cable relation 2 lambda /
tau_m, which is almost independent of dendrite length, closing the door on the claim that
asymmetry magnitude alone rescues the model. The authors conclude that at most a small
fraction of V1 DS can be attributed to single-cell dendritic geometry, and that network
mechanisms — recurrent cortical circuits, lagged-thalamic delay lines, and synaptic timing —
must carry the bulk of the computation.

For this project’s literature survey on morphology-to-DS modelling, the paper is a
foundational negative cortical control. It defines the line between a morphology-causal system
(retinal SACs and DSGCs, where dendritic geometry is a primary substrate of DS) and a
network-causal system (V1 simple cells, where morphology is insufficient). Any compartmental
model that we fit against DS tuning curves must log its implied 2 lambda / tau_m velocity and
compare to the Anderson et al. bound; any cortical morphology-causal claim we encounter in
newer papers should be read against this 1999 null result. The tangential-projection plus
polar-sector morphometry pipeline is directly reusable for our DSGC asymmetry analyses, and
the Meynert-cell ModelDB entry (ModelDB 3812) is a concrete starting point should we later
need a cortical compartmental comparator for our retinal DS models.

</details>

<details>
<summary>📖 <strong>Dendritic Computation of Direction Selectivity and Gain Control
in Visual Interneurons</strong> — Single et al., 1997</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.17-16-06023.1997` |
| **Authors** | Sandra Single, Juergen Haag, Alexander Borst |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.17-16-06023.1997` |
| **URL** | https://www.jneurosci.org/content/17/16/6023 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1523_JNEUROSCI.17-16-06023.1997/summary.md) |

Single, Haag, and Borst (1997) address one of the oldest questions in invertebrate visual
neuroscience: where, along the chain from photoreceptor to wide-field motion-sensitive cell,
is direction selectivity generated? The prevailing assumption had been that the elementary
motion detectors (EMDs) feeding lobula plate tangential cells were themselves strongly
direction-tuned and that the large LPTC dendrite served primarily as a spatial integrator. The
authors set out to test this assumption directly by combining pharmacology with a
biophysically grounded compartmental model of a reconstructed VS-cell from the blowfly
Calliphora erythrocephala.

They use picrotoxinin to block GABAergic inhibition in vivo while recording intracellularly
from VS- and CH-cells and extracellularly from the H1 neuron. In parallel, they build a
passive compartmental model (Rm = 2 kOhm.cm^2, Ri = 40 Ohm.cm, Cm = 0.8 uF/cm^2) in which 32
opponent excitatory-inhibitory EMD synapses are distributed over four dendritic regions along
the main dendrite. An isopotential reduction yields the closed-form saturation expression Ee
(1 - c) / (1 + c), with c = gi/ge a velocity-dependent opponent ratio, clarifying how a single
synaptic machinery can underlie two ostensibly distinct phenomena.

The key findings are that (i) motion-induced input resistance drops by about 13-14 percent in
both directions under control, implying simultaneous excitatory-inhibitory activation; (ii)
PTX reduces this change to less than 50 percent (null) and about 60 percent (preferred) of
control and flips null-direction responses from hyperpolarization to depolarization, revealing
that the underlying EMDs are only weakly directionally tuned; and (iii) the passive
compartmental model, with weakly tuned EMDs, quantitatively reproduces the classical size- and
velocity-dependent saturation ("gain control"), which is abolished once inhibition is blocked.
Direction selectivity and gain control therefore share a single dendritic mechanism.

For this project's literature survey on how morphology shapes direction selectivity via
computational modeling, Single et al. (1997) is the foundational LPTC entry: it is the first
reconstructed-morphology compartmental model of a fly tangential cell, it fixes the passive-
dendrite "null model" against which morphology-manipulation experiments must be read, and it
establishes the opponent-conductance mechanism that any subsequent morphology-to-DSI
regression in the HS-VS literature inherits. The paper's main limitation for our purposes is
that dendritic morphology is held fixed — it is a same-morphology, varied-synapse study — so
it sets the stage for, rather than directly implements, explicit morphology-variation
experiments on DSI. It is invertebrate (fly, Calliphora erythrocephala), a flag to bear in
mind when generalizing to vertebrate retinal-ganglion or cortical DS models.

</details>

<details>
<summary>📖 <strong>The mechanism of directionally selective units in rabbit's
retina.</strong> — Barlow & Levick, 1965</summary>

| Field | Value |
|---|---|
| **ID** | `10.1113_jphysiol.1965.sp007638` |
| **Authors** | H. B. Barlow, W. R. Levick |
| **Venue** | The Journal of Physiology (journal) |
| **DOI** | `10.1113/jphysiol.1965.sp007638` |
| **URL** | https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.1965.sp007638 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.1965.sp007638/summary.md) |

Barlow and Levick investigate the mechanism of direction selectivity in on-off retinal
ganglion cells of the rabbit. The central question is what intraretinal circuit produces the
striking asymmetry between vigorous preferred-direction responses and near-silence for
null-direction motion, given that this asymmetry cannot be explained by the static on/off
receptive field map.

The experimental strategy combines systematic exclusion of alternative hypotheses with
two-spot temporal sequence experiments. Optical aberrations and latency gradients are ruled
out first. Single-slit experiments localise the full DS mechanism to subunits of 6-24
arc-minutes, replicated uniformly across the 3-4.5 degree receptive field. Two-spot
experiments show that these subunits discriminate the temporal order of excitation of pairs of
neighbouring regions, with the effect present only within approximately 24 arc-minutes.

The key finding is that null-direction selectivity is produced by active inhibition: null
sequences elicit fewer spikes than the sum of individual responses (Table 3), while preferred
sequences produce a small facilitation. The inhibitory mechanism is proposed to arise from
horizontal cells conducting laterally in the null direction to veto bipolar responses. The
specific cell-type assignment was later revised to starburst amacrine cells, but the logical
architecture has proven correct.

For this project, Barlow1965 provides the primary behavioural benchmark for the compartmental
model: it must fire vigorously for preferred-direction waves and be nearly silent for
null-direction waves, with asymmetry arising from spatially distributed inhibitory GABA
synaptic input across the dendritic arbor. The inhibitory interaction range constraint
(approximately 0.25-1 degree) bounds the spatial scale of GABA inputs, and the optimal wave
speed of approximately 5 degrees/sec sets the target velocity for parametric sweeps in
simulation.

</details>

## Tasks (7)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |
| 0010 | [Hunt DSGC compartmental models missed by prior survey; port runnable ones](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) | completed | 2026-04-20 14:42 |
| 0013 | [Resolve dsgc-baseline-morphology source-paper provenance](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) | completed | 2026-04-20 17:21 |
| 0015 | [Literature survey: cable theory and dendritic filtering](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) | completed | 2026-04-20 10:00 |
| 0017 | [Literature survey: patch-clamp recordings of RGCs and DSGCs](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) | completed | 2026-04-20 11:08 |
| 0018 | [Literature survey: synaptic integration in RGC-adjacent systems](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) | completed | 2026-04-20 12:15 |
| 0027 | [Literature survey: modeling effect of cell morphology on direction selectivity](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) | completed | 2026-04-21 22:23 |

## Answers (13)

<details>
<summary><strong>Does the deposited ModelDB 189347 code reproduce Poleg-Polsky
2016's Fig 3A-F per-synapse conductance balance and DSI-vs-gNMDA flatness,
and does the extended noise sweep match the paper's qualitative
shape?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-25 | **Full answer**:
[`polegpolsky-2016-fig3-conductances-validation`](../../tasks/t0047_validate_pp16_fig3_cond_noise/assets/answer/polegpolsky-2016-fig3-conductances-validation/)

No. Every per-synapse-class summed peak conductance at the code-pinned gNMDA = 0.5 nS is 6-9x
the paper's Fig 3A-E target on the summed scale and well below it on the per-synapse-mean
scale, so neither interpretation reconciles. DSI as a function of gNMDA peaks at 0.19 near
b2gnmda = 0.5 nS and decays toward zero by 3.0 nS, never crossing the paper's claimed flat
~0.30 band. The extended noise sweep shows DSI declining qualitatively as flickerVAR rises in
the control and 0Mg conditions but the trend is weaker than the paper reports, and the ROC AUC
metric saturates at 1.0 across every cell because PSP peaks dwarf baselines on this circuit.

</details>

<details>
<summary><strong>Does setting Voff_bipNMDA = 1 (voltage-independent NMDA, the
deposited 0 Mg2+ condition) reproduce Poleg-Polsky and Diamond 2016's claim
that DSI vs gNMDA is approximately constant ~0.30 across 0-3 nS?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-25 | **Full answer**:
[`dsi-flatness-test-voltage-independent-nmda`](../../tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/)

No. Voltage-independent NMDA partially flattens the DSI-vs-gNMDA curve — the 0-3 nS range
collapses from 0.174 (Voff_bipNMDA = 0 baseline) to 0.066, satisfying the H1 range threshold
of 0.10 — but the slope test still trends downward at -0.024 per nS, above the 0.02 H1 cutoff
and never within +/- 0.05 of the paper's claimed 0.30. The combined verdict is therefore H2
(flatter than the deposited control but still not flat at 0.30): the Voff = 1 curve runs at
0.04-0.10 across the entire range, not at 0.30. The Voff_bipNMDA = 1 swap by itself does not
reproduce the paper's DSI vs gNMDA claim.

</details>

<details>
<summary><strong>Do the t0034 distal-length sweep and the t0035 distal-diameter
sweep collapse onto a single DSI-vs-L/lambda curve under Rall's cable
theory, and should t0033 parameterise dendritic morphology in 1-D
(electrotonic length L/lambda) or 2-D (raw length x raw diameter)?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-24 | **Full answer**:
[`electrotonic-length-collapse-of-length-and-diameter-sweeps`](../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/assets/answer/electrotonic-length-collapse-of-length-and-diameter-sweeps/)

No. The two sweeps do not collapse onto a single DSI-vs-L/lambda curve: in the overlapping
L/lambda interval (0.058-0.116) the Pearson r between the paired sweeps is **+0.42** for
primary DSI and **-0.68** for vector-sum DSI, both well below the 0.9 confirmation threshold,
and the sign of the vector-sum r is opposite to the prediction. Pooled degree-2 polynomial
fits leave residual RMSE of **0.040** (primary) and **0.024** (vector-sum), indicating that
non-cable effects dominate the DSI-vs-L/lambda response. t0033 should retain the 2-D (raw
length x raw diameter) morphology parameterisation rather than compress to 1-D L/lambda,
because the direction of the DSI response is not determined by L/lambda alone.

</details>

<details>
<summary><strong>Does ModelDB 189347 (Poleg-Polsky and Diamond 2016) reproduce every
quantitative claim in Figures 1-8 of the Neuron paper when re-run
faithfully under NEURON 8.2.7, and where do the paper text and the ModelDB
code disagree?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-24 | **Full answer**:
[`poleg-polsky-2016-reproduction-audit`](../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/)

Partially. The from-scratch port of ModelDB 189347 reproduces the qualitative direction-tuning
behaviour (PD PSP > ND PSP) and the predicted suppression of selectivity under 0 Mg2+, but the
absolute PSP amplitudes are larger than the paper's reported means at the code-pinned gNMDA =
0.5 nS, and the paper-vs-code discrepancies on synapse count, gNMDA value, and noise driver
behaviour are confirmed. Ten or more discrepancies are catalogued in the full answer including
six MOD-default-vs-main.hoc-override mismatches and four pre-flagged paper-vs-code
disagreements; every Figure 1-8 reproduction outcome is recorded with numerical evidence.

</details>

<details>
<summary><strong>What is the Vast.ai GPU cost and recommended organisation of a
joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation
task?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-22 | **Full answer**:
[`vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation`](../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/)

Run a surrogate-NN-assisted gradient-free evolutionary search (population 150 x 30 generations
x 3 seeds after a 5,000-sample surrogate-training burn-in, 25 free parameters = 5 Cuntz
morphology scalars + 20 channel gbar parameters) on a single RTX 4090 Vast.ai instance at a
central USD cost of about 51 dollars, with a 0.5x-2x sensitivity envelope of roughly 23-119
dollars. This combination is cheapest among the corpus-justified gradient-free strategies
because the surrogate-NN cuts 18,500 evaluations to ~8 GPU-hours of surrogate inference plus a
one-off ~83 GPU-hour CoreNEURON training burn at the RTX 4090 rate of 0.50 dollars/hour.
Confidence is medium: the CoreNEURON CPU-to-GPU speedup and the surrogate-NN economics are
external assumptions not quantified in the downloaded paper corpus, and the sensitivity grid
is propagated across a 0.5x-2x band for both per-sim cost and sample count.

</details>

<details>
<summary><strong>What variables of neuronal morphology have been shown by
computational modeling to affect direction selectivity, by what mechanisms,
and what gaps remain?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-21 | **Full answer**:
[`morphology-direction-selectivity-modeling-synthesis`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/answer/morphology-direction-selectivity-modeling-synthesis/)

Computational models have shown that direction selectivity is shaped by dendritic length,
branch-order and branching pattern, dendritic diameter (especially in starburst amacrine
cells), spatial layout and kinetic tiling of bipolar-cell inputs, asymmetric arbors and plexus
density, and the electrotonic compartmentalization of terminal branches. The load-bearing
mechanisms are passive cable filtering with transfer-resistance weighting of distributed
inputs, local-global EPSP summation along soma-to-tip dendritic gradients, space-time input
tiling (sustained proximal, transient distal), dendritic-spike branch independence driven by
voltage-gated Na and Ca channels, and asymmetric SAC-to-DSGC inhibition constrained by
morphology. Gaps remain in systematic sweeps of branch order and dendritic diameter on
realistic reconstructions, in joint manipulation of morphology with active conductances at
DSGC tips, and in morphology-aware modeling of cortical and invertebrate direction selectivity
beyond the retina.

</details>

<details>
<summary><strong>Can ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC)
be reproduced locally on Windows as a headless library, does it hit the
published direction-selectivity envelope with a canonical 12-angle x
20-trial drifting-bar protocol, and which sibling DSGC compartmental models
are the next-best candidates for porting in the same pipeline?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-20 | **Full answer**:
[`dsgc-modeldb-port-reproduction-report`](../../tasks/t0008_port_modeldb_189347/assets/answer/dsgc-modeldb-port-reproduction-report/)

Yes, ModelDB 189347 was ported and runs headless on Windows 11 with NEURON 8.2.7 via a Python
driver that sources the verbatim HOC and MOD files through `h.load_file`/`h.nrn_load_dll`; a
12-angle x 20-trial sweep on the bundled morphology completed end-to-end in roughly 10 minutes
and the four registered metrics (DSI, HWHM, reliability, RMSE vs target) were written to
`results/metrics.json`. The tuning curve does not hit the published envelope at the bundled
parameters (peak well below 40 Hz, DSI well below 0.7), because the paper derives DS from a
`gabaMOD` parameter swap rather than from spatial rotation — the port's rotation-based
protocol is only a proxy for a direction- selective stimulus. The Hanson et al. 2019
Spatial-Offset-DSGC model (GitHub `geoffder/Spatial-Offset-DSGC-NEURON-Model`) is the
next-best port candidate: it shares `RGCmodel.hoc` and `HHst.mod` with 189347 and already
ships a Python driver; Jain 2020 is medium-effort; Ding 2016, Schachter 2010, Koren 2017, and
Ezra-Tsur 2022 either lack a public compartmental model or address a different modelling
class.

</details>

<details>
<summary><strong>What DSGC compartmental models published in public literature were
missed by tasks t0002 and t0008, and which of them are viable ports for
this project?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-20 | **Full answer**:
[`dsgc-missed-models-survey`](../../tasks/t0010_hunt_missed_dsgc_models/assets/answer/dsgc-missed-models-survey/)

Two brand-new DSGC compartmental-model papers were missed by the prior corpus: deRosenroll et
al. 2026 (Cell Reports, DOI `10.1016/j.celrep.2025.116833`) and Poleg-Polsky 2026 (Nature
Communications, DOI `10.1038/s41467-026-70288-4`); Hanson 2019 (`10.7554/eLife.42392`) was in
the t0002 corpus but had never been ported. None of the three HIGH-priority candidates
completed a 12-angle canonical sweep within the 90-minute-per-candidate port budget — each
failed at the P2 upstream-demo gate for a different structural reason (Hanson: headfull Python
driver with hardcoded Windows paths; deRosenroll: hardcoded 8-direction stimulus grid plus
heavy out-of-env dependencies; Poleg-Polsky: genetic-algorithm training driver with `numDir=2`
and no LICENSE). Zero library assets were registered per the "never leave a broken library
behind" rule, and all three candidates are recorded as `p2_failed` in `data/candidates.csv`.
Deeper investment (hand-rewriting each driver) would very plausibly succeed; the 90-minute cap
is the binding constraint, not a definitive portability verdict.

</details>

<details>
<summary><strong>What does the classical cable-theory and dendritic-computation
literature imply for the compartmental modelling of direction-selective
retinal ganglion cells (DSGCs) in NEURON?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-20 | **Full answer**:
[`cable-theory-implications-for-dsgc-modelling`](../../tasks/t0015_literature_survey_cable_theory/assets/answer/cable-theory-implications-for-dsgc-modelling/)

DSGC compartmental models in NEURON must use morphologically accurate reconstructions (not
ball- and-stick), discretized with the `d_lambda` rule, and must implement direction
selectivity via postsynaptic dendritic shunting inhibition rather than presynaptic wiring
asymmetry. The DS computation must arise from asymmetric inhibitory input acting locally on
dendritic branches via the Koch-Poggio-Torre on-the-path shunting mechanism, and the model
must be validated by measuring EPSP shape-indices, losing DS under simulated inhibition block,
and reproducing the graded-vs- spike contrast-sensitivity trade-off.

</details>

<details>
<summary><strong>Which dendritic-computation motifs observed in cortical,
hippocampal, and cerebellar neurons plausibly transfer to DSGC dendrites,
and what are the biophysical caveats?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-20 | **Full answer**:
[`dendritic-computation-motifs-for-dsgc-direction-selectivity`](../../tasks/t0016_literature_survey_dendritic_computation/assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/)

Three dendritic-computation motifs plausibly transfer from pyramidal, hippocampal, and
cerebellar dendrites to DSGC dendrites: NMDA-receptor-mediated on-branch supralinear
integration, asymmetric shunting inhibition placed on the path between excitation and soma,
and sublinear-to-supralinear regime switching driven by clustered input. Ca2+-plateau BAC
firing and behavioral-timescale plasticity transfer less cleanly because DSGC dendrites are
short and unipolar rather than tufted. All transferred numbers must be treated as targets to
falsify rather than to assume, pending DSGC-specific patch validation.

</details>

<details>
<summary><strong>What does the patch-clamp / voltage-clamp / space-clamp literature
imply for the compartmental modelling of direction-selective retinal
ganglion cells (DSGCs) in NEURON, in particular for (a) treatment of
published Ge/Gi traces as model-fitting targets, (b) inclusion of dendritic
voltage-gated channels and the AIS compartment, (c) synaptic receptor
complement including NMDARs, and (d) modelling of maintained activity and
intrinsic pacemaker properties?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-20 | **Full answer**:
[`patch-clamp-techniques-and-constraints-for-dsgc-modelling`](../../tasks/t0017_literature_survey_patch_clamp/assets/answer/patch-clamp-techniques-and-constraints-for-dsgc-modelling/)

DSGC compartmental models must treat published somatic voltage-clamp Ge/Gi traces as lower
bounds on distal dendritic conductances rather than ground truth, because up to ~80% of the
synaptic signal is lost on thin distal dendrites even in passive cables and active dendritic
channels add further error. The modelling pipeline therefore needs a simulated somatic
voltage-clamp block that mimics the experimental amplifier so simulation and experiment are
compared on the same footing. The model must include an explicit AIS compartment with Nav1.6
enrichment at approximately 7x the somatic Na+ density, with AIS length as a named tunable
parameter constrained by immunohistochemistry, and NMDARs with standard Mg2+ block kinetics on
DSGC dendrites, fit to AMPA/NMDA charge ratios during preferred and null motion rather than
peak-AMPA-current alone. Finally the modeller must decide explicitly whether to include
intrinsic-pacemaker biophysics (T-type Ca2+, HCN, subthreshold oscillations) based on the
target DSGC subtype, validated by maintained-activity-under-synaptic-blockade traces.

</details>

<details>
<summary><strong>What quantitative priors does the synaptic-integration literature
supply for the DSGC compartmental model on (1) AMPA/NMDA/GABA receptor
kinetics, (2) shunting inhibition, (3) E-I balance temporal co-tuning, (4)
dendritic-location-dependent PSP integration, and (5) SAC-to-DSGC
inhibitory asymmetry?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-20 | **Full answer**:
[`synaptic-integration-priors-for-dsgc-modelling`](../../tasks/t0018_literature_survey_synaptic_integration/assets/answer/synaptic-integration-priors-for-dsgc-modelling/)

Receptor kinetics: AMPA uses a fast bi-exponential conductance (rise ~0.2 ms, decay ~1-3 ms,
Erev 0 mV); NMDA uses a slow conductance (rise ~5-10 ms, decay ~50-100 ms, Erev 0 mV) with
Jahr-Stevens Mg2+ block; GABA_A uses a fast bi-exponential (rise ~0.5 ms, decay ~5-10 ms, Erev
-65 to -75 mV). Shunting inhibition vetoes excitation multiplicatively with an "on-the-path"
geometry: only inhibition sitting between the excitatory input and the soma shunts PSP
amplitude, while distal inhibition has negligible effect. Excitation and inhibition co-tune in
time with inhibition lagging excitation by ~1-3 ms in cortex and ~15-50 ms in DSGCs during
null-direction motion, sharpening spike timing. Somatic PSP amplitude decays roughly
exponentially with electrotonic distance (lambda_DC ~100-300 um for RGC dendrites) while local
dendritic non-linearities (Na+, Ca2+, NMDAR) partially compensate for distal attenuation. SAC
boutons onto a DSGC dendrite are spatially asymmetric with stronger inhibition from null-side
SACs, and this cellular asymmetry (not somatic E-I timing alone) is the primary substrate for
direction selectivity at the DSGC level.

</details>

<details>
<summary><strong>How does the existing peer-reviewed literature on compartmental
models of direction-selective retinal ganglion cells structure the five
project research questions (Na/K conductances, morphology sensitivity,
AMPA/GABA balance, active vs passive dendrites, and angle-to-AP-frequency
tuning curves), and what quantitative targets does it provide?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-18 | **Full answer**:
[`how-does-dsgc-literature-structure-the-five-research-questions`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/)

The literature structures the five questions around a small set of quantitative targets that
the project must hit. For Na/K conductances the Fohlmeister-Miller parameter set (peak somatic
g_Na around 0.04-0.10 S/cm^2, delayed-rectifier g_K around 0.012 S/cm^2) is the standard
starting point, and no published paper reports a factorial (g_Na, g_K) grid for DSGCs. For
morphology the asymmetric ON-OFF DSGC dendrite is sharply wired in the null direction through
SAC-mediated inhibition, yet global dendrite shape only minimally changes the synaptic map
while local electrotonic compartments still matter. For AMPA/GABA balance the canonical counts
on a reconstructed mouse DSGC are 177 AMPA and 177 GABA synapses, with null-direction
inhibition running three to five times larger than preferred inhibition. Active dendrites with
Fohlmeister-like channel densities roughly double the direction-selectivity index versus
passive trees, and the target mouse ON-OFF DSGC tuning curve should hit DSI 0.7-0.85,
preferred peak 40-80 Hz, null residual under 10 Hz, and a half-width of 60-90 degrees.

</details>

## Suggestions (115 open, 16 closed)

<details>
<summary>📊 <strong>Redefine the ROC AUC negative class (off-direction or
jitter-isolated trials) so the metric does not saturate at 1.000</strong>
(S-0047-03)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-25 | **Source**:
[t0047_validate_pp16_fig3_cond_noise](../../tasks/t0047_validate_pp16_fig3_cond_noise/)

t0047 reproduces the paper's qualitative DSI-declines-with-noise shape across all three
conditions but ROC AUC saturates at 1.000 in every (condition, flickerVAR) cell. Root cause:
t0046's `_roc_auc_pd_vs_baseline` uses pre-stimulus baseline mean (5-6 mV above v_init) as the
negative class while PD PSP peaks (18-25 mV) dwarf baselines. Paper's Fig 7 shows AUC
declining toward 0.7 under noise. Concrete actions: (a) re-implement AUC using off-direction
(ND) PSP peaks as the negative class (PD-vs-ND PSP overlap framing); (b) alternatively sample
jitter-isolated trials as the no-stimulus distribution; (c) add unit tests on a synthetic
two-Gaussian distribution with controllable overlap. Recorded as discrepancy entry 15 in
t0047's catalogue. Once redefined, re-evaluate the t0047 noise-extension trial CSVs (96 trials
on disk) without re-simulating. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA conductance scan at Voff_bipNMDA=1 to close the residual
DSI gap to paper's 0.30 line</strong> (S-0048-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-25 | **Source**:
[t0048_voff_nmda1_dsi_test](../../tasks/t0048_voff_nmda1_dsi_test/)

t0048 confirmed that switching to voltage-independent NMDA (exptype=2) flattens the DSI vs
gNMDA curve to 0.04-0.10 but never reaches the paper's claimed flat ~0.30. The residual gap
must come from non-NMDA mechanisms; the leading candidate is GABA, where t0047 measured
deposited PD ~106 / ND ~216 nS summed conductance vs paper's PD ~12.5 / ND ~30 nS (8x over) at
gNMDA = 0.5 nS. Run a parameter sweep at exptype=2 over a GABA scale factor in {1.0, 0.5,
0.25, 0.125, 0.06} (ratios chosen to bracket paper's 12.5x reduction toward biological values)
at the same 7 gNMDA grid points x 4 trials per direction used here. Track DSI vs (gNMDA, GABA
scale) and report whether any GABA setting produces flat DSI ~0.30 across the gNMDA range.
Pass criterion: identify a GABA scale (if any) that simultaneously satisfies the H1
range/slope thresholds and a mean-DSI > 0.20 target. Recommended task types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Adopt exptype=2 (Voff_bipNMDA=1) as the canonical DSGC control
for downstream tasks via correction overlay</strong> (S-0048-02)</summary>

**Kind**: technique | **Priority**: high | **Date**: 2026-04-25 | **Source**:
[t0048_voff_nmda1_dsi_test](../../tasks/t0048_voff_nmda1_dsi_test/)

t0048 establishes that the deposited code's exptype=1 (voltage-dependent NMDA) does not match
the paper's biological NMDA, while exptype=2 (Voff_bipNMDA=1, voltage-independent) is closer
to the paper's text statement and the deposited 0 Mg2+ condition. Per t0048's
compare_literature.md: the deposited control choice for the project's DSGC simulations should
be exptype=2, not exptype=1. Implement this as a project-wide convention change: (a) write a
corrections-overlay note attached to t0046 documenting that ExperimentType.CONTROL is
reinterpreted as ExperimentType.ZERO_MG for paper-faithful DSGC reproduction; (b) add a
project-level constant CANONICAL_DSGC_EXPTYPE = 2 in a shared module that downstream tasks
import; (c) update the project's description.md / library asset README for
modeldb_189347_dsgc_exact to record the convention. This is correction work, not an
experiment, but it gates every downstream DSGC task that compares to the paper. Recommended
task types: correction.

</details>

<details>
<summary>🧪 <strong>AMPA conductance scan at Voff_bipNMDA=1 as a secondary check
on the residual DSI gap</strong> (S-0048-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-25 | **Source**:
[t0048_voff_nmda1_dsi_test](../../tasks/t0048_voff_nmda1_dsi_test/)

Complementary to S-0048-01's GABA scan: re-run the same 7-point gNMDA sweep at exptype=2 with
the AMPA conductance scaled across {1.0, 0.5, 0.25, 0.125} of the deposited b2gampa = 0.25 nS
value. t0048's per-class conductance comparison shows AMPA summed conductance is similar
between PD/ND (~11 nS each), so AMPA changes alone cannot create direction selectivity, but
lowering AMPA at fixed GABA could shift the AMPA/GABA balance enough to amplify whatever
residual selectivity GABA provides. This is an essential negative control for S-0048-01: if
AMPA reduction matches GABA reduction in DSI effect, the gap is symmetric and not purely GABA.
4 trials per direction x 7 gNMDA x 4 AMPA scales = 224 trials, ~30 min CPU. Recommended task
types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Higher-N (12-19 trials) rerun of t0048's Voff_bipNMDA=1 gNMDA
sweep to tighten H2 verdict bands</strong> (S-0048-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-25 | **Source**:
[t0048_voff_nmda1_dsi_test](../../tasks/t0048_voff_nmda1_dsi_test/)

t0048 used 4 trials per direction per gNMDA value. SD on PSP amplitudes was 0.16-1.02 mV,
which is below the trial-to-trial PD/ND difference at most grid points, but the H2-vs-H1
boundary at the slope test (-0.024 vs |slope| < 0.020 cutoff) is close enough that more trials
might tip the verdict. Re-run this same Voff_bipNMDA=1 sweep at the paper's reported N (12-19
trials per direction per gNMDA value) using the existing code/run_voff1_sweep.py with extended
trial seed ranges. This is distinct from S-0046-01 which targets the Voff_bipNMDA=0 baseline;
S-0048-04 specifically tightens t0048's Voff=1 H2 finding. Pass criterion: report whether the
slope test verdict changes from H2 to H1 with paper-N. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-run t0047's noise (flickerVAR) sweep at Voff_bipNMDA=1 to test
noise-DSI behavior under voltage-independent NMDA</strong> (S-0048-05)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-25 | **Source**:
[t0048_voff_nmda1_dsi_test](../../tasks/t0048_voff_nmda1_dsi_test/)

t0047 ran a noise sweep at exptype=1 (Voff_bipNMDA=0). Now that t0048 establishes
Voff_bipNMDA=1 as the paper-faithful NMDA condition, the corresponding question is whether
t0047's noise vs DSI relationship (DSI declining with flickerVAR across the three gNMDA
conditions) holds under the voltage-independent setting. Re-run the same flickerVAR x gNMDA
grid t0047 used (or a reduced 3 x 3 grid to bound CPU) at exptype=2 and compare the
noise-vs-DSI shape. Useful corollary to t0048's gNMDA finding because it tells us whether the
noise sensitivity is dominated by NMDA voltage-dependence or by AMPA/GABA balance. Lower
priority because (a) t0047 already provides the qualitative noise-vs-DSI shape and (b) the H2
verdict for the Voff=1 DSI baseline is unlikely to be qualitatively different under noise.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA conductance scan under SEClamp toward paper PD 12.5 / ND
30 nS at fixed gNMDA = 0.5 nS</strong> (S-0049-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-25 | **Source**:
[t0049_seclamp_cond_remeasure](../../tasks/t0049_seclamp_cond_remeasure/)

SEClamp at -65 mV yielded GABA PD = 47.47 / ND = 48.04 nS vs paper's 12.5 / 30 nS. Run a
`gabaMOD` (or per-synapse GABA) scan under SEClamp at gNMDA = 0.5 nS, exptype = control, with
multiplier values across {1.0, 0.5, 0.25, 0.125} of the deposited base, and additionally test
introducing PD/ND spatial asymmetry (e.g., scale ND-side GABA up by 2-3x and PD-side GABA
down) to see whether the paper's ND-bias DSI -0.41 is recoverable by a spatial redistribution
at the soma. Distinct from S-0048-01 which scans GABA at exptype = 2 across a gNMDA sweep
without SEClamp; this task uses SEClamp modality at single gNMDA. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Repeat SEClamp Fig 3A-E re-measurement at exptype=2
(Voff_bipNMDA=1) for canonical-control baseline</strong> (S-0049-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-25 | **Source**:
[t0049_seclamp_cond_remeasure](../../tasks/t0049_seclamp_cond_remeasure/)

t0049 ran the SEClamp re-measurement at exptype=control (Voff_bipNMDA=0). t0048 established
that exptype=2 (Voff_bipNMDA=1, voltage-independent NMDA) is the paper-faithful canonical
control. Repeat the same 32-trial SEClamp sweep (2 directions x 4 channel-isolations x 4
trials at gNMDA = 0.5 nS, V_clamp = -65 mV) under exptype=2 to establish whether the residual
NMDA over-amplification (SEClamp PD 13.89 vs paper 7.0) and direction-asymmetry collapse
persist under voltage-independent NMDA. This locks the canonical SEClamp baseline alongside
the canonical exptype convention before downstream parameter-tuning work begins. Recommended
task types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Re-implement placeBIP() to spatially gate gabaMOD by per-synapse
locx</strong> (S-0050-01)</summary>

**Kind**: technique | **Priority**: high | **Date**: 2026-04-25 | **Source**:
[t0050_audit_syn_distribution](../../tasks/t0050_audit_syn_distribution/)

t0050 confirmed deposited PD/ND swap is a single global scalar gabaMOD = 0.33 + 0.66*direction
applied uniformly to every SAC inhibitory synapse with no spatial threshold
(dsgc_model_exact.hoc:316-334). Modify placeBIP() (or wrap it in a helper) so gabaMOD is
computed per synapse from each synapse's locx relative to the BIPsyn-locx median (88.77 um) or
soma_x (104.58 um), scaling up ND-side synapses and down PD-side synapses while preserving the
population mean. Re-run t0049's somatic SEClamp protocol to test whether somatic GABA recovers
an ND-bias toward paper Fig 3C (PD ~12.5 / ND ~30 nS, DSI ~ -0.41). This is the primary 'fix
path A' identified by t0050's mechanism analysis. Recommended task types: feature-engineering,
experiment-run.

</details>

<details>
<summary>🔧 <strong>Re-distribute SACinhib synapses asymmetrically across PD-side and
ND-side dendrites in RGCmodel.hoc</strong> (S-0050-02)</summary>

**Kind**: technique | **Priority**: high | **Date**: 2026-04-25 | **Source**:
[t0050_audit_syn_distribution](../../tasks/t0050_audit_syn_distribution/)

Alternative 'fix path B' to S-0050-01: instead of modulating gabaMOD per synapse, modify the
construction loop in RGCmodel.hoc:11839-11857 so SACinhib synapses are placed asymmetrically
across the dendritic field (more on the ND-side, fewer on the PD-side) while leaving BIPsyn
and SACexcsyn at the deposited 282-symmetric distribution. t0050 found total dendritic length
per side is essentially identical (2311 vs 2296 um) so the dendritic substrate supports an
asymmetric placement at construction. Test whether the somatic SEClamp PD/ND asymmetry reaches
paper Fig 3C targets without changing per-synapse gabaMOD. This decouples the deposited 'three
channels share parent sections per index' design and is a more invasive but mechanistically
cleaner option. Recommended task types: feature-engineering, experiment-run.

</details>

<details>
<summary>🧪 <strong>Localise the GABA unpinning threshold with a fine sweep (5.0,
4.5, 4.0, 3.5, 3.0 nS)</strong> (S-0037-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0037_null_gaba_reduction_ladder_t0022](../../tasks/t0037_null_gaba_reduction_ladder_t0022/)

The current sweep places the unpinning threshold between 6 nS (t0036 pinned) and 4 nS (t0037
unpinned). A 0.5 nS-spaced sweep over {5.0, 4.5, 4.0, 3.5, 3.0} nS at baseline diameter on
t0022 (5 levels x 12 angles x 10 trials = 600 trials, ~20 min local CPU) would localise the
threshold to within 0.5 nS and reveal whether the DSI vs GABA curve is sharp or gradual.
Important for characterising how fragile the operational window really is.

</details>

<details>
<summary>🧪 <strong>Cross-testbed DSI comparison: t0022 at 4 nS GABA vs t0024 AR(2)
noise</strong> (S-0037-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0037_null_gaba_reduction_ladder_t0022](../../tasks/t0037_null_gaba_reduction_ladder_t0022/)

t0034/t0035 already produce measurable primary DSI on t0024 via AR(2) stochastic release
(rho=0.6). t0037 now shows that t0022 at 4 nS GABA is a second valid substrate. A dedicated
comparison task should run matched 7-diameter and 5-length sweeps on both substrates with
identical stimulus schedules and report whether the two discriminators agree on
Schachter2010-vs-passive identification. If they disagree, that itself is a finding worth
investigating.

</details>

<details>
<summary>🔧 <strong>Add preferred-direction GABA asymmetry to t0022 (cartwheel SAC
offset)</strong> (S-0037-06)</summary>

**Kind**: technique | **Priority**: low | **Date**: 2026-04-24 | **Source**:
[t0037_null_gaba_reduction_ladder_t0022](../../tasks/t0037_null_gaba_reduction_ladder_t0022/)

t0022 applies only null-direction GABA. Published DSGC models (Park2014, Schachter2010)
include a directionally-offset SAC inhibition where preferred-direction trials see much lower
GABA than null. Implement the cartwheel asymmetry as a new parameter
`GABA_CONDUCTANCE_PREF_NS` (probably 0-1 nS based on t0037's over-excitation regime below 2
nS), and measure whether primary DSI improves toward the 0.5-0.6 Park2014 centre. This moves
t0022 closer to the canonical DSGC E-I motif rather than relying on a single null-only scalar.

</details>

<details>
<summary>🧪 <strong>Rerun t0039 7-diameter sweep on t0024 for active-vs-passive
testbed comparison</strong> (S-0039-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-24 | **Source**:
[t0039_distal_dendrite_diameter_sweep_t0022_gaba4](../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/)

t0039 on t0022 at GABA=4 nS produced a passive_filtering signature (slope=-0.034, p=0.008).
Rerun the same 7-diameter sweep on t0024 (de_rosenroll_2026_dsgc, richer channel inventory,
AR(2) stochastic release) at its equivalent operational GABA level to test whether the
Schachter2010 concave-down signature emerges when active dendritic machinery is available. If
t0024 shows concave-down and t0022 shows monotonic decrease, that is the cleanest
testbed-level discrimination between the two mechanisms the project has produced. If both show
passive_filtering, that rules out Schachter2010 across the substrates the project has
available.

</details>

<details>
<summary>🧪 <strong>Fine-grained thin-end diameter sweep D in {0.3, 0.4, 0.5, 0.6,
0.7} at GABA=4 nS on t0022</strong> (S-0039-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0039_distal_dendrite_diameter_sweep_t0022_gaba4](../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/)

t0039 found DSI saturates at 0.429 for D in {0.5, 0.75, 1.0}, matching the t0037 4 nS ceiling.
This is the discriminator's upper bound at this GABA level. A finer sweep thinner than 0.5x
would locate the saturation edge and bound the headroom available to any morphology optimiser
on t0022. 5 diameters x 12 angles x 10 trials = 600 trials, ~25 min local CPU, $0.00.

</details>

<details>
<summary>🧪 <strong>Joint (GABA, diameter) sweep to separate passive filtering from
GABA-suppressed active amplification</strong> (S-0039-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0039_distal_dendrite_diameter_sweep_t0022_gaba4](../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/)

t0022 shows passive_filtering at 4 nS. Two explanations: (a) t0022 lacks active machinery, or
(b) 4 nS GABA shunts regenerative events that would otherwise produce Schachter2010
concave-down. A joint sweep GABA in {5, 4, 3, 2} x D in {0.5, 1.0, 2.0} = 12 conditions x 12
angles x 10 trials = 1440 trials (~60 min) would distinguish: if lower-GABA runs produce
concave-down curves, mechanism (b) is right; if all GABA levels show passive signatures,
mechanism (a) is right.

</details>

<details>
<summary>🔧 <strong>Update t0033 optimiser headroom estimate to reflect narrow (0.06
DSI) morphology dynamic range on t0022</strong> (S-0039-05)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0039_distal_dendrite_diameter_sweep_t0022_gaba4](../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/)

t0039 shows the t0022 discriminator's total DSI spread across a 4x diameter range is only
0.061 (0.368 to 0.429). Any pure-morphology optimiser running at GABA=4 nS on t0022 has a
ceiling of 0.429 (the 4 nS saturation value). If t0033's planned optimiser is scoped to
maximise DSI via morphology alone, the maximum achievable lift from the baseline is ~0.06 -
the headroom is much smaller than originally planned. Consider adding a channel-density
dimension to the optimiser search space, since DSI has more potential room through Nav/Cav
density than through morphology alone.

</details>

<details>
<summary>🧪 <strong>Denser 2-D sweep of L x d to map DSI response surface on
t0024</strong> (S-0041-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0041_electrotonic_length_collapse_t0034_t0035](../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/)

The t0041 overlap region contained only n=3 paired points. Run a 2-D sweep varying length and
diameter independently across a 5x5 or 7x7 grid on t0024 (at GABA operational baseline) to map
the DSI response surface rather than test collapse on two 1-D slices. Outcome would feed
directly into t0033's morphology parameterisation and quantify the interaction term that the
collapse test implied exists.

</details>

<details>
<summary>🧪 <strong>Re-run t0046 figure sweeps at paper-N (12-19 trials per
condition, full 8-direction sweep)</strong> (S-0046-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-24 | **Source**:
[t0046_reproduce_poleg_polsky_2016_exact](../../tasks/t0046_reproduce_poleg_polsky_2016_exact/)

Re-execute every figure-reproduction sweep in t0046 (`code/run_all_figures.py`) at the paper's
reported N (12-19 trials per condition) and the full 8-direction sweep instead of the
wall-clock-budget-reduced 2-4 trials and PD/ND-only collapse used in t0046. This will (a)
tighten the SD bands on PSP and AP-rate distributions, (b) replace the `atan2(mean PD PSP,
mean ND PSP)` slope approximation with a fit to the 8-direction tuning curve as the paper
does, and (c) reveal the true Fig 7 0 Mg2+ ROC AUC instead of the small-N saturation at 1.00
(paper reports 0.83). Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Decide the fate of t0042/t0043/t0044: rewrite motivation or
cancel based on t0046 findings</strong> (S-0046-04)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0046_reproduce_poleg_polsky_2016_exact](../../tasks/t0046_reproduce_poleg_polsky_2016_exact/)

t0042 (fine-grained null-GABA ladder), t0043 (Nav1.6 + Kv3 + NMDA restoration), and t0044
(Schachter re-test on t0043) are currently `intervention_blocked` pending t0046's outcome.
t0046 establishes that the systematic peak-rate gap previously seen in t0008/t0020/t0022
(which motivated t0043's channel-inventory framing) is inherent to the deposited ModelDB code,
not a modification artefact. This invalidates t0043's stated motivation. Run a
brainstorm-style triage that (a) explicitly cancels or (b) rewrites motivations for each of
the three blocked tasks, replacing the discredited peak-rate-gap framing with t0046's
confirmed findings (synapse-count overcount; AP5-vs-iMK801 substitution; PSP amplitude
inflation). Apply corrections-overlay updates to record the decisions. Recommended task types:
brainstorming, correction.

</details>

<details>
<summary>🧪 <strong>2-D distal length x diameter sweep on t0024 to disambiguate
cable-filtering vs local-spike-failure</strong> (S-0034-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-23 | **Source**:
[t0034_distal_dendrite_length_sweep_t0024](../../tasks/t0034_distal_dendrite_length_sweep_t0024/)

t0034 produced a non-monotonic primary DSI (0.545-0.774, p=0.038) and a clean monotonic
vector-sum DSI decline (R^2=0.91) that falsified Dan2018's passive-TR prediction and did not
fit Sivyer2013's plateau. Creative-thinking flagged passive cable filtering past an optimal
electrotonic length (Tukker2004, Hausselt2007) as the best fit, with local-spike-failure
(Schachter2010) explaining the preferred-angle jumps at 1.5x and 2.0x. A marginal length sweep
alone cannot distinguish these two mechanisms because lambda = sqrt(d*Rm/(4*Ra)) couples
length and diameter nonlinearly. Run a 3x3 grid (length in {0.5, 1.0, 2.0} x diameter in {0.5,
1.0, 2.0}) on the t0024 port with AR(2) rho=0.6, 12-direction x 10-trial protocol per cell,
and classify each cell as cable-limited, spike-amplified, or threshold-transition. Distinct
from S-0030-04 (same approach on t0022 testbed, which was pinned at DSI=1.000 and cannot
resolve the effect). Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>AR(2) rho sweep at t0024 baseline morphology to isolate
stochastic-release smoothing from cable biophysics</strong> (S-0034-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-23 | **Source**:
[t0034_distal_dendrite_length_sweep_t0024](../../tasks/t0034_distal_dendrite_length_sweep_t0024/)

Creative-thinking (alternative 5) proposed that AR(2)-correlated release with rho=0.6
temporally smooths the null-direction noise floor, potentially contributing to the observed
primary-DSI non-monotonicity independently of cable filtering. This hypothesis must be ruled
in or out before the cable-filtering interpretation is credible. Run the 12-direction x
10-trial protocol on t0024 at baseline morphology (length=1.0x, diameter=1.0x) with rho in
{0.0, 0.3, 0.6, 0.9} (four points) and compare primary-DSI, vector-sum DSI, null Hz, and HWHM
trajectories. If DSI is flat across rho, stochastic-release smoothing is not the driver; if
DSI varies with rho, the effect is release-noise-mediated. Distinct from S-0026-02 (which
crosses rho with V_rest to disambiguate noise vs depolarisation) because this sweeps rho at
fixed V_rest and fixed morphology to isolate the release-noise-vs-cable-biophysics axis.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Extended distal-length sweep on t0024 (0.25x to 4.0x, 9 points)
to characterise the electrotonic-length optimum</strong> (S-0034-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0034_distal_dendrite_length_sweep_t0024](../../tasks/t0034_distal_dendrite_length_sweep_t0024/)

t0034 covered 0.5x-2.0x (7 points) and found the primary-DSI peak at 0.75x (0.774) with a
non-monotonic decline beyond. To fit Tukker2004's intermediate-electrotonic-length optimum
quantitatively and to test whether the curve continues falling or saturates beyond 2.0x,
extend the sweep to 0.25x, 0.375x, 0.5x, 0.75x, 1.0x, 1.5x, 2.0x, 3.0x, 4.0x (9 points). Keep
the standard 12-direction x 10-trial protocol and AR(2) rho=0.6. Expected outcomes: (a) a
clear DSI peak at intermediate length with symmetric falloff on both sides (supports
Tukker2004 optimum); (b) preferred-angle instability across 3.0x-4.0x (supports Schachter2010
local-spike-failure); (c) d_lambda violations at extreme lengths (engineering concern - apply
adaptive nseg at each point). Distinct from S-0029-03 (same approach on t0022 testbed which
was pinned at DSI=1.000). Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Per-compartment distal-spike detector on t0024 length sweep to
verify Schachter2010 local-spike-failure at 1.5x and 2.0x</strong>
(S-0034-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0034_distal_dendrite_length_sweep_t0024](../../tasks/t0034_distal_dendrite_length_sweep_t0024/)

t0034 attributed the primary-DSI non-monotonicity and preferred-angle jumps (to 330 deg at
1.5x, to 30 deg at 2.0x) to Schachter2010 local-spike-failure in distal compartments, based
only on the somatic readout and the angular-instability fingerprint. This interpretation is
currently suggestive but not confirmed. Re-run the t0034 sweep with per-compartment V
recording at every distal terminal (177 sections) and compute the distal-to-soma spike-count
ratio per trial per angle. Under Schachter2010 local-spike-failure, the ratio should be >1 at
baseline (reliable distal spikes) and drop below 1 at 1.5x and 2.0x where cable length
decouples distal tips. If the ratio stays constant, the angle jumps are not a
local-spike-failure signature and another mechanism (NMDA recruitment, Kv3 rectification)
should be explored. Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Quantitative cable-theory fit of t0034 DSI-vs-length curve
against Rall 1/d^(3/2) and Tukker2004 predictions</strong> (S-0034-05)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0034_distal_dendrite_length_sweep_t0024](../../tasks/t0034_distal_dendrite_length_sweep_t0024/)

t0034's classify_shape.py assigns a categorical label (monotonic/saturating/non-monotonic) but
does not fit a parametric cable-theory model to the observed DSI vs length curve. Vector-sum
DSI declines monotonically from 0.507 (0.5x) to 0.357 (2.0x) with R^2=0.91, and peak firing
declines 40% across the sweep - both quantitative cable-filtering signatures. Write a
dedicated analysis task that fits (a) the Rall 1/d^(3/2) impedance-matching rule to the
peak-Hz decline, (b) Tukker2004's lambda-optimum function to the DSI vs length curve (extract
the fitted lambda at peak DSI), and (c) Hausselt2007's cable-length-to-DSI scaling. Output a
fitted parameter set with 95% CIs and a residual plot. This converts t0034's categorical
'cable-filtering best fit' into a falsifiable quantitative claim and enables direct
cross-paper comparison. Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Higher-statistics re-run of t0034 at 1.5x and 2.0x (30+ trials
per angle) to confirm the preferred-angle jumps</strong> (S-0034-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0034_distal_dendrite_length_sweep_t0024](../../tasks/t0034_distal_dendrite_length_sweep_t0024/)

t0034's non-monotonicity hinges on two preferred-angle jumps: 0 deg -> 330 deg at 1.5x (DSI
dip to 0.623) and 0 deg -> 30 deg at 2.0x (DSI collapse to 0.545). These are based on only 10
trials per angle, and the compare-literature analysis notes the 95% CI on a 10-trial DSI is
~+/-0.1 - comparable to the 0.23 observed DSI spread. Re-run the protocol at 1.5x and 2.0x
with 30-50 trials per angle (3-5x the baseline count) and recompute bootstrap CIs on DSI and
preferred-angle estimates at each point. If the jumps persist, Schachter2010
local-spike-failure is strengthened; if they collapse to a single preferred direction, they
were small-N artefacts and the cable-filtering story becomes more parsimonious. Listed in
compare-literature.md as a concrete limitation. Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Specify primary DSI as t0033 optimiser objective on t0024
substrate (not vector-sum) and drop monotonic-length priors</strong>
(S-0034-07)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-04-23 | **Source**:
[t0034_distal_dendrite_length_sweep_t0024](../../tasks/t0034_distal_dendrite_length_sweep_t0024/)

t0034 establishes two facts that directly constrain the t0033 joint morphology+VGC optimiser
design: (1) primary DSI on t0024 has measurable dynamic range (0.545-0.774, spread 0.229,
p=0.038), so the optimiser CAN use primary DSI as the objective - no need to fall back to
vector-sum DSI as S-0030-06 proposed for t0022; (2) the DSI-vs-length curve is non-monotonic
with a net negative slope, opposite to Dan2018's monotonic-increase prior - the optimiser must
NOT assume longer distal dendrites yield higher DSI. Register as a t0033 planning correction:
pick t0024 as the optimisation testbed, use primary DSI as the objective, and seed the
length-axis initial distribution near 0.75x-1.0x (observed peak). Distinct from S-0030-06
(vector-sum DSI on t0022) - this clarifies that t0024 is the correct substrate. Recommended
task types: comparative-analysis, answer-question.

</details>

<details>
<summary>🧪 <strong>Surface-density-rescaled Nav diameter sweep on t0024 to test
surface-vs-volume compensation</strong> (S-0035-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-23 | **Source**:
[t0035_distal_dendrite_diameter_sweep_t0024](../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/)

Re-run a small diameter sweep (0.5x, 1.0x, 2.0x) on the t0024 DSGC with gnabar_HHst rescaled
by 1/d in the distal compartments so the total per-section Nav count is held fixed as diameter
varies. Creative_thinking hypothesis 2 proposes that the flat DSI-vs-diameter result (t0035)
arises because NEURON's surface-density gbar scales total channel current by d while axial
load scales by d^2, cancelling the net effect. If density rescaling produces a non-flat DSI
trend, the compensation confound is confirmed; if still flat, rule out this hypothesis.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Extended distal-diameter sweep on t0024 (0.25x to 4.0x, 9 points)
to probe non-linear extremes</strong> (S-0035-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0035_distal_dendrite_diameter_sweep_t0024](../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/)

Push the diameter multiplier beyond t0035's narrow 0.5x-2.0x range into a wider 0.25x-4.0x
sweep (nine multipliers) on the t0024 DSGC substrate to look for non-linear DSI effects that
the 4x range missed. Specifically targets two possibilities: (a) input-impedance saturation at
baseline may break at extreme thinning/thickening and (b) the cable-theory 1/sqrt(d)
prediction implies a detectable DSI shift over a 16x diameter range even if a 4x range is
inside the noise floor. Distinct from S-0030-03 which targets t0022. Recommended task types:
experiment-run.

</details>

<details>
<summary>📊 <strong>Zero-cost meta-analysis of primary-DSI vs vector-sum-DSI
discrepancy across t0029, t0030, t0034, t0035</strong> (S-0035-05)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0035_distal_dendrite_diameter_sweep_t0024](../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/)

Combine metrics.json outputs from all four completed morphology sweeps (t0029 length t0022,
t0030 diameter t0022, t0034 length t0024, t0035 diameter t0024) into a single cross-task table
correlating primary DSI against vector-sum DSI. Key questions: when primary DSI is flat or at
ceiling, does vector-sum DSI pick up signal? Does the rank-order of variants agree between the
two metrics? This supports the t0033 optimiser choice and a standing evaluation-methodology
recommendation (compare against S-0029-07, S-0030-06, S-0034-07). No simulations needed; pure
re-analysis of existing CSVs. Recommended task types: data-analysis.

</details>

<details>
<summary>🔧 <strong>Deprioritise distal-diameter parameters in the t0033 DSI
optimiser search space</strong> (S-0035-06)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0035_distal_dendrite_diameter_sweep_t0024](../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/)

The t0033 DSGC optimisation plan treats distal length and distal diameter as co-equal
morphology parameters. t0034 (p=0.038 on length) and t0035 (p=0.88 on diameter) together show
that distal diameter has DSI leverage below the noise floor on the t0024 substrate, while
length is a strong discriminator. Concrete action: reduce distal-diameter weight in the
optimiser search space (smaller range, coarser grid, or drop it entirely) so the GPU budget
concentrates on axes that actually move DSI. Distinct from S-0034-07 which focuses on the
primary-vs-vector-sum objective; this one concerns the parameter search space itself.
Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>GABA-to-AMPA timing offset sweep on t0022 diameter testbed to
test timing-dominates-conductance hypothesis</strong> (S-0036-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0036_rerun_t0030_halved_null_gaba](../../tasks/t0036_rerun_t0030_halved_null_gaba/)

t0036's creative_thinking cited 'timing dominates conductance' as the second-leading
explanation for why halving null-GABA from 12 nS to 6 nS did not unpin null firing: the t0022
schedule delivers GABA 10 ms BEFORE AMPA on null trials, and the integrated kinetic profile
(not the peak) may clamp the distal membrane below Nav threshold for the whole AMPA window.
Sweep the GABA-leads-AMPA offset across {10 ms (default), 5 ms, 0 ms, -5 ms (AMPA leads GABA)}
at two fixed GABA conductances (12 nS baseline and 6 nS) at diameter 1.0x only (12 angles x 10
trials x 4 offsets x 2 GABA = 960 trials, ~35 min CPU). Primary outcome: find the offset at
which null firing first exceeds 0.1 Hz, isolating timing as an independent rescue axis
orthogonal to S-0036-01's conductance axis. Distinct from S-0030-02 (Poisson) and S-0036-01
(conductance) - this targets the GABA-AMPA offset specifically. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Distal voltage-trace capture at null direction on t0022 to
confirm sub-threshold-clamp hypothesis</strong> (S-0036-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0036_rerun_t0030_halved_null_gaba](../../tasks/t0036_rerun_t0030_halved_null_gaba/)

t0036 recorded per-trial scalar distal peak_mv only (~-55 mV at null direction) but did not
export the full distal membrane time course. Creative_thinking hypothesis 4 (distal Nav
channels sub-threshold at null regardless of diameter amplification) and limitation bullet 5
both flag missing voltage traces as blocking direct mechanistic confirmation. Extend the t0022
trial driver to save a 200-sample time-course of the most-distal compartment voltage (one
trial per direction at diameter 1.0x, GABA_NULL = 6 nS and 12 nS, 24 traces total, ~5 min
CPU). Plot v_distal(t) across directions and annotate Nav activation threshold (~-55 mV) and
AMPA/GABA event onsets. Expected: at null the distal membrane never crosses Nav threshold for
the whole AMPA window on either 6 nS or 12 nS; at preferred it crosses and fires. Closes
creative_thinking hypothesis 4 and confirms the sub-threshold-clamp failure mode. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary>📚 <strong>Extract the t0022 GABA-override monkey-patch into a reusable
library asset for downstream tasks</strong> (S-0036-04)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0036_rerun_t0030_halved_null_gaba](../../tasks/t0036_rerun_t0030_halved_null_gaba/)

t0036 introduced code/gaba_override.py which monkey-patches
_t0022_constants.GABA_CONDUCTANCE_NULL_NS at import time and re-binds the local name inside
trial_runner_diameter.py so the schedule_ei_onsets ratio is computed against the overridden
value. This pattern is immediately needed for S-0036-01 (further null-GABA reductions) and
S-0036-02 (GABA-AMPA timing offset). Rather than each task reimplementing the monkey-patch,
lift it into a library asset (working name: dsgc_t0022_schedule_overrides) exposing a typed
context-manager or setup function accepting gaba_null_ns, gaba_preferred_ns,
gaba_to_ampa_lead_ms, returning a provenance dict logged at task start. Ships a smoke test
asserting the override survived a fresh import and that the null/preferred ratio matches the
requested value. Distinct from S-0033-06 (DSI objective evaluator) which wraps the scoring
side - this wraps the schedule-parameter side. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Poisson-noise desaturation rerun of the distal-dendrite length
sweep on t0022</strong> (S-0029-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0029_distal_dendrite_length_sweep_dsgc](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/)

The t0029 sweep failed as a mechanism discriminator because pref/null DSI is pinned at 1.000
at every multiplier from 0.5x to 2.0x (null firing = 0 Hz on every trial, reliability =
1.000). Dan2018's passive-TR derivation and Schachter2010's compartmental DSGC both assume
stochastic Poisson drive with a rate-code noise floor; removing noise collapses the
mechanism-distinguishing regime. Add an independent 5 Hz background Poisson NetStim per distal
dendrite (independent seed, no direction bias) to the t0022 scheduler and rerun the full
7-point length sweep (12 angles x 10 trials x 7 lengths = 840 trials). Expected: DSI drops
from 1.000 to the 0.6-0.8 Park2014 envelope, reliability drops below 1.0, and length regains
discrimination power between Dan2018's monotonic-decrease and Sivyer2013's saturation
predictions. Distinct from S-0022-05 which runs at a single length only. Recommended task
types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Distal Nav ablation crossed with distal-dendrite length sweep
on t0022</strong> (S-0029-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0029_distal_dendrite_length_sweep_dsgc](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/)

HWHM in t0029 oscillates non-monotonically across length multipliers (71.7 deg at 1.5x vs
115.8 deg at 1.75-2.0x), inconsistent with any passive cable theory and consistent with distal
Nav channels crossing or failing to cross dendritic-spike threshold at a critical length.
Rerun the 7-point length sweep with distal Nav channels ablated (`forsec DEND_CHANNELS {
gnabar_HHst = 0 }`) while keeping somatic and AIS Nav intact. If HWHM becomes monotonic with
length, the non-monotonicity is a Sivyer2013 dendritic-spike signature and active boosting is
the dominant mechanism. If HWHM still oscillates, the non-monotonicity is passive cable
resonance and Sivyer2013 can be provisionally rejected on this morphology. Pairs naturally
with S-0029-01 to form a 2x2 design (Nav ablation x Poisson noise). One-line HOC overlay. ~45
min CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Extended distal-dendrite length sweep (1.0x to 4.0x, 8.0x) to
reach Dan2018's critical regime</strong> (S-0029-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0029_distal_dendrite_length_sweep_dsgc](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/)

Dan2018 reports monotonic DSI-vs-length over 50-400 um distal branches; Sivyer2013's critical
length sits at ~150 um. The t0022 distal-leaf baseline is on the order of tens of um, so the
0.5-2.0x sweep likely spans only ~15-160 um, overlapping only the tail of Sivyer2013's range
and sitting entirely below Dan2018's critical length. Add three extreme sweep points at 3.0x,
5.0x, and 8.0x while keeping the rest of the t0022 testbed fixed. Watch for `d_lambda`
violations at extreme lengths (fallback: adaptive `nseg` at each point). Possible outcomes:
(a) DSI stays at 1.000 and peak Hz continues linear decline - testbed is cable-dominated at
the soma and no resolution is possible; (b) DSI drops at a specific high multiplier with
monotonic HWHM broadening - Dan2018 passive-TR regime emerges; (c) DSI drops with HWHM
narrowing at a specific multiplier - Sivyer2013 dendritic-spike-failure regime emerges. ~45
min CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Null-GABA conductance sweep (3, 6, 9, 12 nS) to release the
deterministic ceiling on t0022</strong> (S-0029-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0029_distal_dendrite_length_sweep_dsgc](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/)

The t0022 scheduler uses GABA_CONDUCTANCE_NULL_NS = 12 nS applied 10 ms before AMPA on
null-direction trials - about 4x the preferred value (3 nS) and 2x Schachter2010's measured
compound null inhibition (~6 nS). This oversized early shunt forces null-direction firing to
exactly 0 Hz, pinning the pref/null DSI denominator and the ratio at 1.000 before cable
mechanics have any effect. Sweep GABA_CONDUCTANCE_NULL_NS across {3, 6, 9, 12} nS at a fixed
length multiplier of 1.0x and locate the conductance at which null-direction firing first
exceeds 1 Hz. That value is the testbed's sensitivity edge. Prerequisite for S-0029-01 and
S-0029-02: rerunning the length sweep at 6 nS instead of 12 nS gives the
mechanism-discrimination experiment a fighting chance without needing to inject noise. ~30 min
CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Dense distal-length sweep at {1.0, 1.05, 1.10, 1.15, 1.20, 1.25,
1.30} to localize the peak-Hz cliff</strong> (S-0029-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0029_distal_dendrite_length_sweep_dsgc](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/)

Peak somatic firing rate in t0029 steps from 15 Hz at multipliers <= 1.0x to 14 Hz at
multipliers >= 1.25x with no intermediate value, and mean peak membrane voltage drifts
linearly from -4.81 mV (1.0x) to -5.23 mV (2.0x) - a 0.42 mV loss scaling linearly with length
rather than as exp(-L/lambda). A linear drop is inconsistent with passive cable attenuation
but consistent with distal synapses sitting beyond an active boosting region whose gain
depends on spatial proximity (Poleg-Polsky2016 distal Nav/Cav contribution). Add a dense
7-point sweep at {1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30} to resolve whether the 15->14 Hz
step is smooth (passive) or sharp (local threshold crossing, i.e. Sivyer-like signature).
Record both peak Hz and mean peak somatic voltage at each point. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-enable NMDA (b2gnmda nonzero) crossed with distal-dendrite
length sweep on t0022</strong> (S-0029-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0029_distal_dendrite_length_sweep_dsgc](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/)

The t0022 `_silence_baseline_hoc_synapses` sets b2gnmda = 0 and installs single-component
AMPA-only E-I pairs, removing the Espinosa2010 AMPA/NMDA kinetic-tiling mechanism from the
testable space entirely. Espinosa2010 proposes that DSGC DS arises from different activation
time courses of AMPA and NMDA interacting with cable propagation delay - predicting
non-monotonic DSI-vs-length because NMDA's 50-150 ms time constant resonates with propagation
delay at specific lengths. Modify `_silence_baseline_hoc_synapses` to restore b2gnmda at 30%
of the 189347 baseline and rerun the 7-point length sweep. If DSI drops below 1.000 with
non-monotonic length dependence, kinetic tiling is a real third mechanism and the current null
result was partially a function of NMDA silencing. Requires a sibling library asset (clone of
t0022 with NMDA enabled) to preserve t0022's immutability. ~1 hour CPU plus ~1 hour coding.
Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>📊 <strong>Promote peak-Hz and HWHM to co-primary outcomes when DSI is at
ceiling (evaluation methodology)</strong> (S-0029-07)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-22 | **Source**:
[t0029_distal_dendrite_length_sweep_dsgc](../../tasks/t0029_distal_dendrite_length_sweep_dsgc/)

The t0029 null result exposes a systematic evaluation weakness: whenever the t0022-lineage
testbed drives null firing to exactly 0 Hz, pref/null DSI is structurally pinned at 1.000
regardless of the manipulated variable, yet the secondary metrics (peak somatic firing rate,
HWHM, mean peak soma voltage, vector-sum DSI) contain usable length-dependent signal (e.g.,
the non-monotonic HWHM oscillation 71.7-116.3 deg and the 15->14 Hz peak-Hz cliff at 1.25x).
Adopt a co-primary-metric convention: whenever DSI is at ceiling (range across sweep points <
0.01 or null firing = 0 Hz on > 90% of trials), elevate peak-Hz, HWHM, and vector-sum DSI to
co-primary outcome variables and require all three to be reported alongside DSI in
results_summary.md and compare_literature.md. Encode the rule as an extension to the
task-results specification, add a verificator check for the DSI-ceiling condition, and
document the convention in arf/specifications. Recommended task types: infrastructure-setup.

</details>

<details>
<summary>🧪 <strong>Poisson-noise desaturation rerun of the distal-dendrite diameter
sweep on t0022</strong> (S-0030-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0030_distal_dendrite_diameter_sweep_dsgc](../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/)

Sibling of S-0029-01 (Poisson + length sweep) targeting the diameter axis. The t0030
deterministic testbed yields reliability = 1.000 and null firing 0 Hz at every diameter, which
collapses the rate-code noise floor that Schachter2010's dendritic-spike-threshold mechanism
and Dan2018's passive-TR derivation both assume. Add an independent 5 Hz background Poisson
NetStim per distal dendrite (independent seed, no direction bias) to the t0022 scheduler and
rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials).
Expected: DSI drops from 1.000 into the 0.6-0.8 Park2014 envelope, reliability drops below
1.0, and diameter regains discrimination power between Schachter2010 active amplification
(+slope) and passive filtering (-slope). Distinct from S-0022-05 (Poisson at a single
length/diameter) and S-0029-01 (length axis). Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Wider distal-diameter sweep (0.25x to 4.0x) after the schedule
fix to probe extreme impedance regimes</strong> (S-0030-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0030_distal_dendrite_diameter_sweep_dsgc](../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/)

The t0030 sweep used multipliers 0.5x-2.0x (a 4x range) and found vector-sum DSI moved by only
0.030 absolute, with Wu2023 reporting distal-diameter DSI saturation above ~0.8 um on primate
SAC - our baseline distal seg.diam straddles that threshold so our sweep likely sat in the
saturated regime throughout. Once the S-0030-01/S-0030-02 schedule fix has removed the DSI
ceiling, rerun the diameter sweep over a wider range {0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0,
4.0}x at the same 12-direction x 10-trial protocol. Provides the impedance-gradient dynamic
range Schachter2010's 5-7x proximal-to-distal input-resistance measurement implies, and tests
whether Wu2023's saturation threshold applies to mouse ON-OFF DSGC. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Joint distal length x diameter 2-D sweep on t0022 to catch
interactions the marginal sweeps miss</strong> (S-0030-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0030_distal_dendrite_diameter_sweep_dsgc](../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/)

t0029 (distal-length sweep) and t0030 (distal-diameter sweep) both produced flat vector-sum
DSI curves when run in isolation on the t0022 E-I schedule. Marginal sweeps cannot reveal
interactions: Schachter2010's active amplification depends on length (number of Nav-bearing
segments) AND diameter (Nav substrate per unit length) jointly, and the cable space constant
lambda = sqrt(d * Rm / (4 * Ra)) couples them nonlinearly. Run a focused 2-D grid (e.g., 5
length x 5 diameter = 25 configurations x 12 angles x 10 trials = 3000 trials) on the
schedule-fixed testbed (S-0030-01 prerequisite). Distinct from S-0002-04 (broad factorial
including branch orders at fixed synapse count) because it is 2-D, focused, and scheduled
after the desaturation fix. Expected local CPU wall time ~7 h. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Non-uniform proximal-to-distal diameter taper sweep on t0022 to
match Schachter2010 impedance gradient</strong> (S-0030-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0030_distal_dendrite_diameter_sweep_dsgc](../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/)

t0030 applied a single multiplier uniformly to every distal leaf, producing a 4x range that
Schachter2010's 150-200 MOhm proximal -> >1 GOhm distal (5-7x) impedance gradient indicates is
too narrow and the wrong shape. Real DSGC dendrites taper from thick primary branches to thin
terminal tips; the uniform multiplier scales all terminals together without recreating that
gradient. Implement a taper parameter k such that a segment's diameter scales by (1 + k *
path_distance / L_max), sweep k in {-0.5, -0.25, 0, 0.25, 0.5, 0.75} to produce flattened,
nominal, and exaggerated tapers, and run the standard 12-direction x 10-trial protocol at each
k (after the S-0030-01 schedule fix). Expected outcome: the exaggerated-taper cell (high k,
very thin distal) maximises distal input impedance and should exhibit the Schachter2010
amplification signature if the mechanism is active on this morphology. Recommended task types:
experiment-run, feature-engineering.

</details>

<details>
<summary>📊 <strong>Change the t0033 optimiser objective to a vector-sum-DSI-weighted
blend instead of pure primary DSI</strong> (S-0030-06)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-04-22 | **Source**:
[t0030_distal_dendrite_diameter_sweep_dsgc](../../tasks/t0030_distal_dendrite_diameter_sweep_dsgc/)

t0029 and t0030 both pinned primary DSI at 1.000 and only vector-sum DSI retained weak
sensitivity (ranges 0.021 and 0.012 respectively). The t0033 joint morphology-channel
optimisation plan currently proposes primary DSI as the objective; under the t0022 schedule
the optimiser will see a flat landscape and cannot discover morphology-channel interactions.
Change the t0033 objective to a weighted blend (e.g., 0.5 * vector_sum_DSI + 0.3 *
peak_Hz_match + 0.2 * HWHM_match) OR switch to vector-sum DSI outright. Distinct from
S-0029-07 which proposes promoting peak-Hz and HWHM to co-primary outcomes - this proposal
keeps DSI as the headline objective but replaces its pinned primary form with its unpinned
vector-sum form. Update tasks/t0012 tuning_curve_loss to expose a loss_kind='vector_sum_dsi'
option. Recommended task types: write-library, answer-question.

</details>

<details>
<summary>📚 <strong>Instantiate AIS_PROXIMAL / AIS_DISTAL / THIN_AXON channel sets on
t0022 as a t0033 optimiser prerequisite</strong> (S-0033-02)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-22 | **Source**:
[t0033_plan_dsgc_morphology_channel_optimisation](../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/)

The t0022 testbed exposes AIS_PROXIMAL, AIS_DISTAL, and THIN_AXON channel-set hooks in its
modular architecture, but all three are empty because the Poleg-Polsky 2026 backbone has no
axon. The t0033 joint optimiser plans per-region gbar for Nav1.1, Nav1.6, Kv1.2, Kv2.1,
Kv3.1/3.2 and Km/KCNQ across these regions, which is impossible until the hooks are live.
Build a task that (a) adds a short axon hillock + AIS + thin-axon trunk to t0022 using Werginz
2020 / Van Wart 2007 geometry, (b) populates AIS_PROXIMAL with Nav1.1+Kv1.2, AIS_DISTAL with
Nav1.6+Kv3, and THIN_AXON with Nav1.6+Kdr at literature-consensus densities, (c) reruns the
t0022 12-angle sweep and checks DSI and peak rate do not regress, and (d) registers a new
sibling library asset. Recommended task types: infrastructure-setup, build-model,
write-library.

</details>

<details>
<summary>🔧 <strong>Multi-fidelity surrogate-NN prototype to reduce the $41.56
training burn on the recommended optimiser cell</strong> (S-0033-03)</summary>

**Kind**: technique | **Priority**: high | **Date**: 2026-04-22 | **Source**:
[t0033_plan_dsgc_morphology_channel_optimisation](../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/)

The recommended Surrogate-NN-GA cell in t0033 has central cost $50.54, of which $41.56 is the
one-shot 5,000-sample training burn. Creative-thinking alternative #1 argued that a
multi-fidelity surrogate (train on coarse-dt or shallow-AR(2), filter, re-score top decile on
full fidelity) should cut training USD 2-3x. Build a prototype task that (a) defines two
fidelities on the existing t0022 or t0024 port — full (dt=0.1 ms, AR(2) rho=0.6, 10 trials) vs
coarse (dt=0.25 ms, deterministic or AR(1), 3 trials) — while keeping the Jain 2020 5-10 um
compartment floor, (b) trains a 3-layer MLP surrogate on a 500-sample Latin-hypercube over the
25 committed parameters at coarse fidelity, (c) measures regret between coarse-filtered top-k
and full-fidelity top-k, and (d) reports realised training-USD reduction. Recommended task
types: experiment-run, feature-engineering.

</details>

<details>
<summary>🔧 <strong>Transfer-learning surrogate warm-start from t0022 and t0024
V_rest-sweep evaluations</strong> (S-0033-04)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0033_plan_dsgc_morphology_channel_optimisation](../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/)

Creative-thinking alternative #3 in t0033 noted that t0022, t0024 and the t0026 V_rest sweep
already produced thousands of (gbar-subset, DSI) evaluations on the 16-parameter HHst
topology. If half of the 5,000-sample surrogate training burn is replaced by these as
warm-start, the $41.56 training cost plausibly drops to ~$20, pulling the recommended cell to
~$30. Build a task that (a) reads t0026 V_rest-sweep and t0022 baseline outputs, (b) encodes
them as (parameter-vector, DSI) tuples in the 25-dim joint space by imputing the 9 unvaried
dimensions at Poleg-Polsky defaults with tagged uncertainty, (c) pre-trains the surrogate NN
on this warm-start set before the 2,500-sample cold-start burn, and (d) measures whether the
half-dataset warm-start matches the 5,000-sample cold-start surrogate. Recommended task types:
experiment-run, feature-engineering.

</details>

<details>
<summary>🧪 <strong>5-parameter CMA-ES vs Bayesian-optimisation spike on t0022 to
validate sample-efficiency assumptions</strong> (S-0033-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
[t0033_plan_dsgc_morphology_channel_optimisation](../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/)

The t0033 cost model commits literature-derived sample counts (CMA-ES=1,300, BO=500,
Surrogate-NN-GA=18,500) on 25 dims without empirical DSGC validation. Before the full joint
optimiser is commissioned, run a low-dim spike on t0022: (a) pick 5 representative parameters
from the committed 25 (3 Cuntz scalars: bf, distal-length, distal-diameter + gNa_dend +
gKdr_dend), (b) run 200-300 deterministic 12-angle evaluations each under CMA-ES and
sequential BO, (c) compare the DSI converged-to-within-1% sample count against the cost-grid
extrapolations, and (d) report whether either method actually converges on DSGC landscapes or
hits plateaus that the corpus did not flag. Outcome calibrates the strategy row of the cost
model before the 25-dim run. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>📚 <strong>Build a reusable DSI-objective evaluation-harness library
separating scoring from the optimiser loop</strong> (S-0033-06)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-22 | **Source**:
[t0033_plan_dsgc_morphology_channel_optimisation](../../tasks/t0033_plan_dsgc_morphology_channel_optimisation/)

The t0033 plan repeatedly treats evaluate(parameter_vector) -> DSI_scalar as the atomic unit
across CMA-ES / BO / surrogate-NN-GA strategies, but no library asset exposes this signature.
t0012 tuning_curve_loss scores full 12-angle rate vectors, not a DSI-objective scalar. Build a
library asset dsgc_dsi_objective that (a) wraps the t0022 or t0024 port behind a pure-function
evaluate_dsi(parameters, protocol, n_trials) -> DsiResult API, (b) batches (angle, trial)
pairs across an embarrassingly parallel pool, (c) returns a frozen dataclass with DSI, peak
Hz, null Hz, HWHM and a provenance dict, and (d) ships a thin CLI that accepts a parameter
JSON and emits a results JSON. Every strategy row in the t0033 cost model can then call a
single evaluator. Recommended task types: write-library, feature-engineering.

</details>

<details>
<summary>🧪 <strong>Nav1.1 proximal-AIS knockout channel-swap on the t0022
testbed</strong> (S-0022-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-21 | **Source**:
[t0022_modify_dsgc_channel_testbed](../../tasks/t0022_modify_dsgc_channel_testbed/)

Use the t0022 modeldb_189347_dsgc_dendritic library's AIS_PROXIMAL forsec block to append a
proximal axon segment populated with Nav1.1 at ~7x somatic density, then knock it out (set
gbar to 0) and rerun the canonical 12-angle x 10-trial sweep. VanWart2006 reports Nav1.1
dominates the proximal AIS while Nav1.6 dominates the distal AIS; removing proximal Nav1.1
should drop excitability and test whether DSI survives reduced spike-initiation margin.
Expected outcome: peak rate drops below 10 Hz while DSI holds above 0.5 (inhibitory shunt
intact, spike threshold only moved). Dependencies: t0022 library asset. Effort ~6 hours.
Recommended task type: experiment-run.

</details>

<details>
<summary>🧪 <strong>Nav1.6 distal-AIS density sweep to close the 15 Hz -> 30-40 Hz
peak-rate gap</strong> (S-0022-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-21 | **Source**:
[t0022_modify_dsgc_channel_testbed](../../tasks/t0022_modify_dsgc_channel_testbed/)

Sweep Nav1.6 density in the AIS_DISTAL forsec block over {4, 6, 8, 10, 12, 14, 16} S/cm^2
(centred on the Kole-Stuart 2008 ~8 S/cm^2 published anchor) with Kv1.2 held constant, rerun
the 12-angle x 10-trial sweep at each setting, and report peak firing rate vs Nav1.6 density.
Peak-rate cap at 10-20 Hz is shared across t0008 (18.1 Hz), t0020 (14.85 Hz), and t0022 (15
Hz) and is inherited from the unchanged t0008 HHst Na/K density, so the fix lives in the
distal AIS. Expected outcome: peak rate scales monotonically with Nav1.6 density and lands
inside 30-40 Hz at ~8 S/cm^2, matching Poleg-Polsky & Diamond 2016 and Oesch2005.
Dependencies: t0022 library asset. Effort ~12 hours. Recommended task type: experiment-run,
comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Per-dendrite E-I parameter sweep to map the DSI response
surface</strong> (S-0022-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-21 | **Source**:
[t0022_modify_dsgc_channel_testbed](../../tasks/t0022_modify_dsgc_channel_testbed/)

The t0022 driver has three free per-dendrite parameters fixed at single points:
EI_OFFSET_PREFERRED_MS = 10 ms, GABA_NULL/GABA_PREF ratio = 4x (12 nS / 3 nS), AMPA
conductance = 6 nS. Run a factorial sweep over EI_OFFSET in {5, 10, 15} ms, GABA ratio in {2,
3, 4, 6}, and AMPA in {0.15, 0.3, 0.6} nS (the last anchored to Park2014's 0.31 nS somatic
measurement) to quantify mechanism robustness. Expected outcome: a (3 x 4 x 3) = 36-point DSI
response surface showing which E-I corner of the parameter space saturates DSI at 1.0 (driver
is too deterministic) vs produces a graded DSI in the Park2014 0.65 +/- 0.05 band (mechanism
tracks continuous inhibition as real DSGCs do). Dependencies: t0022 library asset. Effort ~20
hours with the existing process-pool orchestrator. Recommended task type: experiment-run,
data-analysis.

</details>

<details>
<summary>📚 <strong>Add a Starburst Amacrine Cell feedforward layer to drive
inhibition physiologically</strong> (S-0022-04)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0022_modify_dsgc_channel_testbed](../../tasks/t0022_modify_dsgc_channel_testbed/)

The t0022 driver schedules GABA directly onto each DSGC dendrite, skipping the SAC (Starburst
Amacrine Cell) layer that shapes DS inhibition in vivo (Euler-Detwiler-Denk 2002). Extend the
modeldb_189347_dsgc_dendritic library with a configurable SAC layer: an array of simplified
SAC models (single-compartment or 2-compartment) whose dendritic output drives DSGC GABA
synapses via NetCon, with SAC dendrites themselves direction-tuned per Euler2002. Expected
outcome: DSI becomes graded rather than saturated (real SAC output is not a hard half-plane
step) and peak firing rate may rise because SAC inhibition is timed to bar arrival not to a
global half-plane rule. This is a library extension not just a channel swap; produces a fourth
DSGC library asset modeldb_189347_dsgc_sac. Dependencies: t0022 library asset, Euler2002
paper. Effort ~40 hours. Recommended task type: write-library, code-reproduction.

</details>

<details>
<summary>🧪 <strong>Inject Poisson background rate on the t0022 driver to moderate
DSI from 1.0 toward the 0.5-0.8 published band</strong> (S-0022-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0022_modify_dsgc_channel_testbed](../../tasks/t0022_modify_dsgc_channel_testbed/)

The t0022 NetStim burst driver uses noise = 0 and baseline synapses are silenced, so DSI
saturates at 1.0 across all 60 null-direction trials. Park2014, Oesch2005, and Poleg-Polsky &
Diamond 2016 all report DSI in the 0.5-0.8 range because real DSGCs have 2-5 Hz per-trial
spike jitter from stochastic bipolar release. Extend the driver with a configurable background
Poisson process (1, 2, 3, 5 Hz baseline rate on all synapses) and rerun the 12-angle x
10-trial sweep at each noise level. Expected outcome: DSI curve drops from 1.0 to ~0.8 at 2 Hz
bg to ~0.6 at 5 Hz bg, bracketing the literature envelope, with per-angle std rising from 0 Hz
to ~2-4 Hz matching Schachter2010 trial-to-trial variability. Dependencies: t0022 library
asset. Effort ~8 hours. Recommended task type: experiment-run.

</details>

<details>
<summary>📊 <strong>Harmonised cross-comparison of the three ModelDB 189347 sibling
ports (t0008, t0020, t0022)</strong> (S-0022-07)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0022_modify_dsgc_channel_testbed](../../tasks/t0022_modify_dsgc_channel_testbed/)

The project now has three independent implementations of DS on the same Poleg-Polsky & Diamond
2016 skeleton: t0008 (per-angle BIP rotation, DSI 0.316), t0020 (global gabaMOD scalar swap,
DSI 0.7838), and t0022 (per-dendrite E-I scheduling, DSI 1.0). Each used slightly different
scoring paths, trial counts, and metric key sets. Produce a shared analysis module that loads
each port's tuning_curves.csv, recomputes DSI / peak / null / HWHM / reliability under one
harmonised scorer (t0012 score() where applicable plus S-0020-04's score_two_point for t0020),
and produces one side-by-side comparison chart (polar plot overlay plus bar chart of headline
metrics). Outputs a consolidated comparison_report.md plus an overview/llm-context/ snapshot.
Dependencies: t0008, t0020, t0022 library assets, t0012 scorer. Effort ~12 hours. Recommended
task type: data-analysis, write-library.

</details>

<details>
<summary>🔧 <strong>Port the full upstream SacNetwork with bp_locs/probs/deltas to
reproduce the deRosenroll correlation-drop effect</strong> (S-0024-01)</summary>

**Kind**: technique | **Priority**: high | **Date**: 2026-04-21 | **Source**:
[t0024_port_de_rosenroll_2026_dsgc](../../tasks/t0024_port_de_rosenroll_2026_dsgc/)

The t0024 port misses REQ-5 on all three sub-criteria (corr DSI 0.82 vs paper target
[0.30,0.50]; uncorr DSI 0.84 vs [0.18,0.35]; drop fraction 0.000 vs >=0.20) because the AR(2)
correlation was applied at per-terminal Exp2Syn drivers rather than across the
spatially-distributed SAC varicosity release network that the paper identifies as the causal
substrate. Port the upstream SacNetwork class (bp_locs, probs, deltas) from
geoffder/ds-circuit-ei-microarchitecture into a new sibling library asset, drive the same
cell, and rerun the 8-direction correlated/uncorrelated sweep. Target: reproduce the ~0.39 ->
~0.25 DSI drop.

</details>

<details>
<summary>🧪 <strong>Unblock t0023 Hanson 2019 port so REQ-6 cross-comparison can
include 5/5 DSGC models instead of 4/5</strong> (S-0024-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0024_port_de_rosenroll_2026_dsgc](../../tasks/t0024_port_de_rosenroll_2026_dsgc/)

t0024 step 12 records t0023_port_hanson_2019_dsgc as intervention_blocked
(intervention/deferred_pending_t0022.md). The t0022 task has since completed (DSI 1.000, HWHM
116.25, RMSE 10.48) so the original blocking dependency is resolved. Triage t0023's
intervention file, resume the port, and then retrofit a Hanson 2019 row into the cross-model
comparison table in results_detailed.md of both t0024 and any subsequent DSGC port. Closes the
REQ-6 partial-coverage caveat.

</details>

<details>
<summary>🧪 <strong>Sweep AR(2) rho x V_rest for t0024 to separate noise correlation
from depolarisation effects</strong> (S-0026-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-21 | **Source**:
[t0026_vrest_sweep_tuning_curves_dsgc](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/)

The t0024 V_rest sweep ran only at rho=0.6 and showed a 1.9x U-shaped DSI curve with HWHM
pinned at 65-83 deg. Repeat the sweep at rho in {0.0, 0.3, 0.6, 0.9} to test whether the
tuning-smoothing is dominated by AR(2) correlation or by the depolarisation itself. Expected
outcome: rho=0.0 should recover tuning sharpness closer to t0022 while preserving the
Na-inactivation-independent peak firing behaviour.

</details>

<details>
<summary>🧪 <strong>Sweep bar velocity x V_rest on both DSGC ports to test
velocity-V_rest interaction</strong> (S-0026-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0026_vrest_sweep_tuning_curves_dsgc](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/)

Sivyer2010 reports DSI varies with velocity (0.45-0.57) at natural V_rest. Our current sweep
fixed velocity at the t0022/t0024 defaults. Repeat the 8-value V_rest sweep at 3-5 bar
velocities to check whether V_rest modulates the velocity-tuning curve or only the
direction-tuning curve. Expected runtime: ~4x current (t0022) and ~4x current (t0024) if 4
velocities are tested.

</details>

<details>
<summary>🧪 <strong>Port Hanson2019 DSGC model and repeat V_rest sweep to test
starburst-independent DS hypothesis</strong> (S-0026-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0026_vrest_sweep_tuning_curves_dsgc](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/)

Hanson2019 reports DSI 0.33 in the absence of asymmetric starburst amacrine cell responses,
suggesting an alternative mechanism. If the Hanson model is ported and swept over the same
eight V_rest values, we can compare its V_rest sensitivity against our t0022 (strongly
V_rest-dependent) and t0024 (U-shaped) results. Would clarify whether V_rest-dependence of DSI
is a universal signature or specific to starburst-driven models.

</details>

<details>
<summary>🧪 <strong>Add NMDA-block and TTX-sensitivity sweeps at each V_rest to
isolate biophysical mechanism</strong> (S-0026-06)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-21 | **Source**:
[t0026_vrest_sweep_tuning_curves_dsgc](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/)

Our V_rest sweep shows t0022 loses tuning at depolarised V_rest (DSI 0.046 at V=-30 mV) while
t0024 stays flat (DSI>=0.36). Two candidate mechanisms are Na channel inactivation and NMDA
Mg-block relief. Run the sweep once with TTX-like Na-block (g_Na=0) and once with NMDA-block
(g_NMDA=0) to isolate which channel class drives each model's V_rest sensitivity.

</details>

<details>
<summary>🧪 <strong>Swap bipolar-cell sustained vs transient kinetics on t0024 to
discriminate kinetic tiling from cable delay</strong> (S-0027-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-21 | **Source**:
[t0027_literature_survey_morphology_ds_modeling](../../tasks/t0027_literature_survey_morphology_ds_modeling/)

Run t0024 (de Rosenroll 2026 port) with bipolar-cell kinetic identities swapped: assign
sustained kinetics to distal terminals and transient kinetics to proximal terminals, opposite
to the wild-type tiling. Prediction (creative_thinking.md #2): if [Srivastava2022]
kinetic-tiling is causally responsible for SAC DS, the swap reverses preferred direction; if
[Kim2014] cable delay is causal, the swap only reduces DSI magnitude without flipping
preferred direction. Critical for choosing between two competing centrifugal-DS mechanisms
before committing to a morphology sweep design.

</details>

<details>
<summary>🧪 <strong>Random terminal-branch ablation (25%) on t0022 to test branch
independence</strong> (S-0027-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0027_literature_survey_morphology_ds_modeling](../../tasks/t0027_literature_survey_morphology_ds_modeling/)

Ablate 25% of randomly-chosen terminal dendritic branches on t0022 (10 random seeds) and
measure global DSI. Prediction (creative_thinking.md #4): if [Sivyer2013, 10.1038_nn.3565]
dendritic-spike branch independence holds, global DSI drops by <15%; if global
transfer-resistance summation dominates, DSI drops by >40%. Also yields the first
DSI-vs-stochastic-pruning curve in the corpus, which would speak to in vivo robustness under
aging or disease perturbations and complement the broader factorial morphology sweep already
proposed in S-0002-04.

</details>

<details>
<summary>🧪 <strong>Single-compartment collapse of t0024 to test whether T4-style
geometry-nullity extends to DSGCs</strong> (S-0027-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0027_literature_survey_morphology_ds_modeling](../../tasks/t0027_literature_survey_morphology_ds_modeling/)

Collapse t0024 (de Rosenroll 2026 port) to a single isopotential compartment that retains full
synaptic input drive and biophysics, and re-run the DSI-vs-speed protocol. Prediction
(creative_thinking.md #5): if T4-style geometry-nullity [Gruntman2018] extends to mammalian
DSGCs, the collapsed model reproduces full-model DSI-vs-speed; if the de Rosenroll local-DSI
mechanism is load-bearing, it fails. Cheapest of the five testbed experiments and a strong
null-hypothesis test for the necessity of dendritic geometry.

</details>

<details>
<summary>🧪 <strong>Sweep dendritic spine density on t0022 distal terminals as an
unconventional morphology variable</strong> (S-0027-07)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-21 | **Source**:
[t0027_literature_survey_morphology_ds_modeling](../../tasks/t0027_literature_survey_morphology_ds_modeling/)

No paper in the t0027 corpus sweeps dendritic spines on DSGCs; all 20 papers treat distal
terminals as smooth cables. Add explicit spine compartments (varying spine density 0, 0.5,
1.0, 2.0 spines/um on distal branches) on t0022 and measure DSI. Tests whether spine-head
capacitance shifts the dendritic-spike threshold gradient in a DS-relevant way, complementing
predictions from [Schachter2010] and [Sivyer2013]. Lower priority than the five predictive
sweeps but uniquely fills a corpus-wide blindspot identified in creative_thinking.md.

</details>

<details>
<summary>📚 <strong>Port Hanson 2019 Spatial-Offset-DSGC as a second DSGC
library</strong> (S-0008-01)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0008_port_modeldb_189347](../../tasks/t0008_port_modeldb_189347/)

Port the Hanson et al. 2019 Spatial-Offset-DSGC-NEURON-Model
(github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model) using the same HOC-driver pattern
proven in t0008. Hanson 2019 shares RGCmodel.hoc and HHst.mod with ModelDB 189347 and already
ships a Python driver (offsetDSGC.py); it implements DS via an explicit spatial-offset
mechanism that matches the rotation-based protocol used in t0008 more directly than
Poleg-Polsky's gabaMOD parameter swap. Expected effort ~8 hours; outcome is a second library
asset and a sanity comparison of the envelope miss pattern across two DSGC models. Recommended
task types: code-reproduction, write-library.

</details>

<details>
<summary>🧪 <strong>Rebuild ModelDB 189347 port on the calibrated Horton-Strahler
SWC from t0009</strong> (S-0008-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0008_port_modeldb_189347](../../tasks/t0008_port_modeldb_189347/)

Replace the bundled 1-soma + 350-dend topology in RGCmodel.hoc with the calibrated SWC from
t0009 (6,736 compartments) and rewrite placeBIP()'s section-ordering-dependent synapse
placement. This was deferred in t0008 because the bundled HOC hardcodes 3D-point placement and
section indices. Outcome is a third variant of the port asset running on a morphology that
actually matches the measured dendritic diameter profile. Recommended task types:
code-reproduction.

</details>

<details>
<summary>🧪 <strong>Parameter-sweep calibration of bundled 189347 toward the envelope
targets</strong> (S-0008-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0008_port_modeldb_189347](../../tasks/t0008_port_modeldb_189347/)

Systematically vary the main free parameters of the 189347 HOC (bipolar-to-RGC synaptic
weight, SAC inhibition gain, NMDA/AMPA ratio, HHst gbar_ scaling) to find a parameter point
where the rotation-based protocol hits the envelope (DSI 0.7-0.85, peak 40-80 Hz, null <10 Hz,
HWHM 60-90 deg). Would produce a calibration_results.json and a mapping between
envelope-passing parameters and the paper's default values. Recommended task types:
code-reproduction.

</details>

<details>
<summary>📚 <strong>Port Jain 2020 DSGC (ModelDB 267001) as a sibling DSGC
asset</strong> (S-0008-05)</summary>

**Kind**: library | **Priority**: low | **Date**: 2026-04-20 | **Source**:
[t0008_port_modeldb_189347](../../tasks/t0008_port_modeldb_189347/)

Clone ModelDB 267001 (Jain et al. 2020 eLife 56404) and port under the same HOC-driver pattern
as t0008. Jain 2020 extends the Poleg-Polsky architecture with bipolar delays and likely
shares MOD mechanisms with 189347. Medium effort (~20 hours) because the morphology and
stimulus logic are separate from 189347. Recommended task types: code-reproduction,
write-library.

</details>

<details>
<summary>🧪 <strong>Hand-port Hanson2019 Spatial-Offset-DSGC model to headless
12-angle sweep</strong> (S-0010-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0010_hunt_missed_dsgc_models](../../tasks/t0010_hunt_missed_dsgc_models/)

Rewrite the upstream run.py driver from geoffder/Spatial-Offset-DSGC-NEURON-Model to remove
the headful 'from neuron import h, gui' import and the hardcoded C:\Users\geoff\NEURONoutput
path, then adapt it to the canonical 12-angle x 20-trial sweep scored against the t0012
tuning-curve API. t0010 exited at P2 within the 90-min per-candidate cap; a dedicated port
task can budget 3-4 hours and reach P3.

</details>

<details>
<summary>🧪 <strong>Hand-port deRosenroll2026 ds-circuit-ei model and remap 8-angle
grid to 12 angles</strong> (S-0010-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0010_hunt_missed_dsgc_models](../../tasks/t0010_hunt_missed_dsgc_models/)

Port geoffder/ds-circuit-ei-microarchitecture (Zenodo 10.5281/zenodo.17666157, MIT LICENSE).
Requires adding statsmodels, h5py, fastparquet, oiffile as optional deps (or extracting a
minimal driver subset without them), then extending the hardcoded 8-direction ANGLES_DEG list
to the canonical 12-angle protocol before scoring. t0010 exited at P2 within the 90-min cap;
budget 4-6 hours for full P3.

</details>

<details>
<summary>🧪 <strong>Write forward-only driver for PolegPolsky2026 DS-mechanisms model
and pursue LICENSE</strong> (S-0010-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0010_hunt_missed_dsgc_models](../../tasks/t0010_hunt_missed_dsgc_models/)

PolegPolskyLab/DS-mechanisms ships only a GA-training harness (numGen=300, popSize=50) and has
no LICENSE file, which blocks library-asset registration under this project's rules. A
follow-up task should (a) email the authors to request a LICENSE addition, and (b) extract a
single-parameter-set forward-only 'simulate at angle theta' driver from the GA inner loop so
the model can be scored against the canonical 12-angle sweep without running the full GA.

</details>

<details>
<summary>🧪 <strong>Extend DSGC model corpus to Arbor and NetPyNE
reimplementations</strong> (S-0010-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0010_hunt_missed_dsgc_models](../../tasks/t0010_hunt_missed_dsgc_models/)

All three candidates hunted in t0010 use NEURON; t0010's DROP list includes Schachter2010
(NeuronC). A follow-up survey task should hunt for Arbor-based and NetPyNE-based DSGC
compartmental models specifically, since those simulators are becoming standard for
large-scale retinal circuit work. Extends REQ-1 of t0010 to a second simulator axis.

</details>

<details>
<summary>📚 <strong>Build a headless-port scaffold library that wraps upstream NEURON
models</strong> (S-0010-05)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0010_hunt_missed_dsgc_models](../../tasks/t0010_hunt_missed_dsgc_models/)

The three P2 failures all share the same root cause: upstream drivers assume a headful NEURON
GUI and hardcode paths/angles. A small library in assets/library/ that provides (a) a headless
NEURON loader that stubs out 'from neuron import gui', (b) a configurable output-path layer,
and (c) a canonical 12-angle stimulus generator would let future port tasks skip the
driver-rewrite step and go straight to P2/P3 scoring.

</details>

<details>
<summary>📂 <strong>Record per-trial soma spike times from modeldb_189347_dsgc to
exercise plot_angle_raster_psth on real data</strong> (S-0011-01)</summary>

**Kind**: dataset | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0011_response_visualization_library](../../tasks/t0011_response_visualization_library/)

The tuning_curve_viz raster+PSTH plot is currently exercised only by a deterministic synthetic
Poisson fixture (seed 42) because neither t0004 nor t0008 emits spike times. Extend the t0008
Poleg-Polsky NEURON driver to record soma membrane voltage, threshold-detect action
potentials, and write a spike-time CSV with columns (angle_deg, trial_seed, spike_time_s)
alongside the existing tuning-curve CSV. Target: 12 angles x 8 trials of spike times for the
baseline ModelDB 189347 port. Once available, re-point tuning_curve_viz.test_smoke.raster_psth
to the real CSV and add the resulting PNGs to assets/library/tuning_curve_viz/files/ via a
correction, replacing the synthetic fixture outputs. Recommended task types:
feature-engineering, code-reproduction.

</details>

<details>
<summary>📚 <strong>Add strict angle-grid validation mode to
tuning_curve_viz.loaders.validate_angle_grid</strong> (S-0011-02)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0011_response_visualization_library](../../tasks/t0011_response_visualization_library/)

The current validate_angle_grid is permissive: it accepts 8/12/16 uniformly-spaced angle
counts and only warns on non-uniform grids. Downstream optimisation and scoring tasks (e.g.,
S-0002-01 g_Na/g_K grid search, S-0012-03 tuning_curve_loss integration) need hard guarantees
that every CSV is on the project-canonical 12-angle 30-degree grid before plots are compared.
Add a strict_mode=False parameter to validate_angle_grid that, when True, raises ValueError
unless angles exactly match np.arange(0, 360, 30.0) to within 1e-6 degree. Add a matching
--strict-angle-grid CLI flag to tuning_curve_viz.cli. Ship unit tests covering:
strict+canonical (pass), strict+8-angle (raise), strict+12-angle-shifted-by-1-degree (raise),
permissive (current behaviour preserved). Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Add combined-report function that renders all four plot types
into one multi-page PDF/HTML per model</strong> (S-0011-03)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0011_response_visualization_library](../../tasks/t0011_response_visualization_library/)

The four tuning_curve_viz functions currently produce seven standalone PNGs per model. A
combined per-model report (one PDF with matplotlib.backends.backend_pdf.PdfPages or an HTML
file embedding the PNGs plus a parameter header) would give a single shareable artefact for
reviewers, brainstorm sessions, and any future project paper draft. Add
tuning_curve_viz.report.build_model_report(curve_csv, out_path, *, target_csv=None,
spike_times_csv=None, title=None, params=None) that collects the existing four plots plus a
header block of model metadata (name, git SHA, DSI, peak, null, HWHM from tuning_curve_loss)
and emits either PDF (default) or HTML (--format html). Exercise in the smoke test by
rendering a report for the target curve and for t0008. Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Add statistical-comparison overlays (paired bootstrap, DSI/HWHM
annotations) to multi-model plots</strong> (S-0011-04)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0011_response_visualization_library](../../tasks/t0011_response_visualization_library/)

plot_multi_model_overlay currently draws every model as a coloured line with a shared legend
but provides no quantitative comparison on the figure itself. Extend the overlay to optionally
annotate each model with its DSI, peak rate, null rate, and HWHM (computed via
tuning_curve_loss.metrics) in the legend, and add a plot_model_comparison(model_a_csv,
model_b_csv, target_csv, out_png) function that computes a paired bootstrap
difference-of-means between two models at every angle, draws the difference curve with a
shaded 95 percent CI, and shades angles where the CI excludes zero. This turns qualitative
overlay comparisons into formally comparable figures suitable for the headline DSI-residual
reporting in S-0002-01 / S-0008-04 calibration sweeps. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Port additional DSGC models from t0010 hunt and exercise
plot_multi_model_overlay with >2 models</strong> (S-0011-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0011_response_visualization_library](../../tasks/t0011_response_visualization_library/)

plot_multi_model_overlay caps at 6 models and was smoke-tested with only two (t0004 target +
t0008 ModelDB 189347). The t0010 hunt identified Hanson 2019 Spatial-Offset-DSGC, deRosenroll
2026 ds-circuit-ei, and other DSGC compartmental models but none have been ported to runnable
headless form yet. Run the headless-port scaffold proposed in S-0010-05 to produce
tuning-curve CSVs for 3-5 additional DSGC models, then regenerate the multi-model overlay
smoke test. This will surface any layout bugs (legend clipping, colour collisions,
preferred-direction arrow overlap) that single- or double-model overlays never exercise and
will give the project a real cross-model comparison figure. Recommended task types:
code-reproduction, write-library.

</details>

<details>
<summary>🔧 <strong>Parametric curve fitting (von Mises / wrapped Gaussian) for
sub-degree HWHM estimates on sparse 12-angle grids</strong> (S-0012-02)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0012_tuning_curve_scoring_loss_library](../../tasks/t0012_tuning_curve_scoring_loss_library/)

The current compute_hwhm_deg interpolates linearly between the two 30 deg samples bracketing
the half-maximum on each flank, limiting HWHM resolution to about 1 deg and producing a 5.5
deg deficit versus the closed-form 65.5 deg (measured 60.0 deg on the t0004 target). Add a
fit_parametric_tuning_curve helper to tuning_curve_loss.metrics that fits a von Mises or
wrapped Gaussian to the 12 angles via scipy.optimize.curve_fit, derives an analytic HWHM from
the fitted kappa or sigma, and exposes hwhm_deg_parametric and parametric_fit_residual_rms on
ScoreReport. Compare parametric HWHM against interpolated HWHM on t0004, t0008 (ModelDB
189347), and S-0002-01 grid-search points; document when interpolation suffices and when the
parametric fit is required. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🧪 <strong>Integrate tuning_curve_loss into the t0008 Poleg-Polsky DSGC
reproduction to score the ported ModelDB 189347 curve</strong> (S-0012-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0012_tuning_curve_scoring_loss_library](../../tasks/t0012_tuning_curve_scoring_loss_library/)

t0008 (port ModelDB 189347) is the first downstream consumer that will produce a real
simulated 12-angle tuning curve. Wire tuning_curve_loss.score into t0008's verification step
so the Poleg-Polsky reproduction's simulated curve is scored against the t0004 target and the
resulting ScoreReport.to_metrics_dict() is written straight into t0008/results/metrics.json
under the four registered keys (direction_selectivity_index, tuning_curve_hwhm_deg,
tuning_curve_reliability, tuning_curve_rmse). Deliverable: a short task that runs t0008's
simulated curve through score(), records ScoreReport.loss_scalar and passes_envelope, and
produces a side-by-side overlay plot (simulated vs target). This is the first end-to-end
validation that the scorer library does what it promises on a non-trivial candidate.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🔧 <strong>Alternative loss formulations (L1, max-residual,
weighted-L-infinity) benchmarked against the Euclidean default</strong>
(S-0012-04)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0012_tuning_curve_scoring_loss_library](../../tasks/t0012_tuning_curve_scoring_loss_library/)

tuning_curve_loss currently computes loss_scalar as a weighted Euclidean (L2) norm of four
normalised residuals. Downstream optimisers may prefer L1 (more robust to a single bad metric,
sub-gradient at zero), max-residual / L-infinity (guarantees every individual target is within
a budget), or Huber (quadratic near zero, linear in the tails). Add pluggable
loss_kind='l2'|'l1'|'linf'|'huber' to score and score_curves, keep 'l2' as the default to
preserve the identity contract, and add parametrised tests that exercise each norm on the same
synthetic inputs used by test_envelope.py. Once downstream grid searches (S-0002-01,
S-0002-04, S-0002-05) have produced O(1000) points, compare how each loss norm ranks the top-k
configurations and whether ranking changes meaningfully. Recommended task types:
write-library, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Revisit envelope widening (DSI upper 0.85 to 0.9, peak lower 40
to 30 Hz) once real simulation results are in</strong> (S-0012-05)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0012_tuning_curve_scoring_loss_library](../../tasks/t0012_tuning_curve_scoring_loss_library/)

REQ-7 was satisfied by widening two envelope bounds away from the t0002 literature values: DSI
upper raised from 0.85 to 0.9 to admit t0004's DSI 0.8824, and peak lower lowered from 40 Hz
to 30 Hz to admit t0004's 32 Hz peak. This is explicit but anchored to the t0004 generator,
not to measured DSGC variability. After t0008 (ModelDB 189347) and the Na/K grid search
(S-0002-01) produce real simulated curves, re-evaluate: (a) re-parameterise t0004 so its curve
lands inside the literature envelope (reducing DSI_MAX from 0.9 to 0.83 would drop DSI to 0.8
and peak to about 37 Hz), or (b) formally widen the envelope with a citation justifying the
wider bounds. Deliverable: an answer asset recommending a resolution, with corresponding
corrections file. Recommended task types: answer-question, correction.

</details>

<details>
<summary>📊 <strong>Cross-validate compute_reliability against independent split-half
implementations (odd-even, bootstrap, Spearman-Brown)</strong> (S-0012-06)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-20 | **Source**:
[t0012_tuning_curve_scoring_loss_library](../../tasks/t0012_tuning_curve_scoring_loss_library/)

compute_reliability implements one split-half estimator: partition trials into even/odd
indices, per-angle means, Pearson r, clamped to [0, 1]. Canonical alternatives differ in
defensible ways: (a) random-draw split rather than parity, (b) Spearman-Brown prophecy
correction to project split-half r back to full-length reliability, (c) Spearman rank
correlation for ordinal robustness, (d) bootstrap resampling to produce a confidence interval.
Build compute_reliability_variants returning all four on the same TuningCurve, run it on
t0004's trials.csv and downstream simulated trials, and write an answer asset documenting
where the estimates agree or diverge. If a variant is systematically preferred for our
approximately 20 trials per angle, promote it to the default via a corrections-aware revision.
Recommended task types: comparative-analysis, answer-question.

</details>

<details>
<summary>📂 <strong>Download the Morrie & Feller 2018 SAC reconstructions from
NeuroMorpho and build a paired SAC+DSGC morphology asset</strong>
(S-0013-03)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0013_resolve_morphology_provenance](../../tasks/t0013_resolve_morphology_provenance/)

This task attributed the dsgc-baseline-morphology reconstruction (NeuroMorpho neuron 102976,
141009_Pair1DSGC) to Morrie & Feller 2018 Current Biology (PMID 29606419). That paper's
Methods describe paired SAC-DSGC patch recordings with 2-photon stacks of both cells
post-recording, and the SAC partner of the 141009_Pair1 recording is likely deposited in
NeuroMorpho alongside the DSGC. Search NeuroMorpho by reference_pmid=29606419 to list all
reconstructions linked to the paper, download the 141009_Pair1SAC companion SWC (and any
neighbouring Pair2/Pair3 SAC+DSGC pairs), validate with validate_swc.py, and register them as
dataset assets so downstream modelling tasks can drive dsgc-baseline-morphology with
anatomically paired SAC presynaptic input. Strengthens the SAC presynaptic drive asset of
S-0002-08. Recommended task types: download-dataset.

</details>

<details>
<summary>📊 <strong>Email the Feller lab to map the 141009_Pair1DSGC session to a
specific pair in Morrie & Feller 2018 CB</strong> (S-0013-05)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-20 | **Source**:
[t0013_resolve_morphology_provenance](../../tasks/t0013_resolve_morphology_provenance/)

The provenance decision in this task (source_paper_id = 10.1016_j.cub.2018.03.001) is grounded
in methodological consistency plus the NeuroMorpho.org curated attribution, not in an
exact-quote match: Morrie & Feller 2018 CB does not literally print 141009, Pair1DSGC,
biocytin, or Neurolucida in its Methods, and the paper publishes only SAC (not DSGC)
reconstructions. A downstream task should email the Feller lab (Murphy-Baum at
murphy-baum@berkeley.edu or Morrie at rmorrie@berkeley.edu) asking which specific paired
recording in the paper's Figure 2 cohort (n = 12 Control + 9 Sema6A-/- null + 6 Sema6A-/-
preferred) produced the 141009_Pair1DSGC reconstruction, and whether the companion SAC
reconstruction is deposited at NeuroMorpho. A one-sentence email-reply quote converts the
current 'methodologically consistent' attribution into a citeable exact-quote provenance, and
directly informs S-0013-03. Recommended task types: answer-question.

</details>

<details>
<summary>🧪 <strong>Build a minimal DSGC compartmental model implementing the 6-point
specification</strong> (S-0015-04)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0015_literature_survey_cable_theory](../../tasks/t0015_literature_survey_cable_theory/)

The answer asset cable-theory-implications-for-dsgc-modelling produces a concrete 6-point
specification for DSGC modelling in NEURON (morphology, d_lambda, DS mechanism, passive
parameters, validation suite, spike-generator tuning). A follow-up experiment task should
implement a minimal working DSGC model in NEURON/NetPyNE following the specification, using a
publicly-available DSGC morphology (e.g. NeuroMorpho.org) and validate it with the four-part
test battery (shape-index, graded DS, inhibition block, contrast-response).

</details>

<details>
<summary>🧪 <strong>Experimentally test NMDA-spike contribution to DSGC direction
selectivity via compartmental simulation</strong> (S-0016-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0016_literature_survey_dendritic_computation](../../tasks/t0016_literature_survey_dendritic_computation/)

The answer asset dendritic-computation-motifs-for-dsgc-direction-selectivity identifies NMDA
spikes as the highest-confidence transferable motif. Build a NEURON/NetPyNE compartmental DSGC
model with explicit NMDA synapses (dynamic Mg2+ block, NMDA:AMPA ratio swept from 0.5 to 2.0)
and test whether spatially-clustered co-directional bipolar-cell input produces supralinear
summation during preferred-direction motion and is suppressed by asymmetric inhibition during
null-direction motion. Compare the resulting DSI (direction selectivity index) against the
no-NMDA baseline to quantify the NMDA-spike contribution to DS.

</details>

<details>
<summary>🧪 <strong>Test whether a Larkum-style Ca2+ plateau zone can be localised
in DSGC dendritic trees</strong> (S-0016-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0016_literature_survey_dendritic_computation](../../tasks/t0016_literature_survey_dendritic_computation/)

The answer asset identifies the cortical-style Ca2+-plateau initiation zone (Larkum 1999) as a
plausible but uncertain motif for DSGCs (caveat: DSGC dendritic trees lack the tuft / basal
two-compartment layout of cortical pyramidals). Build a compartmental DSGC model with
spatially-varying L-type / T-type Ca2+-channel densities to identify candidate initiation-zone
compartments, then test whether asymmetric inhibition at principal-branch bifurcations can
selectively enable Ca2+ plateaus during preferred-direction motion and suppress them during
null-direction motion. Report preferred-direction burst firing rate versus null-direction
burst rate and compare with published DSGC spiking statistics.

</details>

<details>
<summary>🧪 <strong>Extend patch-clamp survey to DSGC-specific dynamic-clamp, Ih/HCN
biophysics, and AIS measurements</strong> (S-0017-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0017_literature_survey_patch_clamp](../../tasks/t0017_literature_survey_patch_clamp/)

The scaled-down 5-paper survey covers the four DSGC-modelling sub-areas identified in the plan
(space-clamp, AIS, NMDARs, maintained activity) but leaves several high-priority follow-on
topics uncovered: (a) DSGC-specific dynamic-clamp studies that use injected conductance
waveforms to test direction selectivity mechanisms, (b) DSGC Ih/HCN biophysics and resonance
properties, (c) DSGC-specific AIS measurements (the Werginz2020 paper is on OFF-alpha T cells,
not on ON-OFF DSGCs directly), and (d) large-scale compartmental-model fitting pipelines for
RGCs. A follow-up survey task should add ~5 papers across these four sub-areas to close the
gap.

</details>

<details>
<summary>🧪 <strong>Implement AIS compartment, NMDARs, and simulated voltage-clamp
block in the downstream DSGC model build task</strong> (S-0017-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0017_literature_survey_patch_clamp](../../tasks/t0017_literature_survey_patch_clamp/)

The answer asset patch-clamp-techniques-and-constraints-for-dsgc-modelling produces a 7-point
specification for DSGC modelling in NEURON extending the cable-theory and
dendritic-computation specifications from t0015 and t0016. The downstream DSGC
compartmental-model build task must implement: (1) an explicit AIS compartment with Nav1.6 at
7x the somatic Na+ density, with AIS length as a tunable parameter; (2) NMDARs with standard
Mg2+ block kinetics on DSGC dendrites alongside AMPARs; (3) a simulated somatic voltage-clamp
block (SEClamp) so experimental and simulated voltage-clamp readouts can be compared on the
same footing; (4) depolarisation-block threshold and AMPA/NMDA charge ratio during preferred
and null motion as named fitting objectives. Validation must include DSI reduction under
simulated NMDAR block to match Sethuramanujam2017 and maintained activity under simulated
synaptic blockade to resolve the MargolisDetwiler2007 intrinsic-vs-synaptic question for the
target DSGC subtype.

</details>

<details>
<summary>🧪 <strong>Extend synaptic-integration survey with DSGC-specific
receptor-kinetic, dynamic-clamp, and connectomic SAC-DSGC papers</strong>
(S-0018-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0018_literature_survey_synaptic_integration](../../tasks/t0018_literature_survey_synaptic_integration/)

The scaled-down 5-paper survey covers the five canonical themes (AMPA/NMDA/GABA kinetics,
shunting inhibition, E-I balance, dendritic-location integration, SAC-to-DSGC asymmetry) but
with one paper per theme, selected from the most-cited classical literature. A follow-up
survey task should add ~5 DSGC-targeted papers across: (a) modern DSGC-specific AMPA and NMDA
kinetic measurements at near-physiological temperature, (b) DSGC dynamic-clamp studies that
inject measured conductance waveforms, (c) connectomic reconstructions of SAC-to-DSGC wiring
(Briggman et al. 2011, Kim et al. 2014), (d) recent E-I temporal co-tuning studies in retina
(rather than auditory cortex), and (e) DSGC dendritic computation (Oesch, Euler, Taylor,
Sivyer). This closes the gap between canonical theory and DSGC-specific parameters.

</details>

<details>
<summary>🧪 <strong>Implement AMPA + NMDA + GABA_A synapses with E-I temporal
co-tuning and SAC-to-DSGC asymmetric inhibition in downstream DSGC
model</strong> (S-0018-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0018_literature_survey_synaptic_integration](../../tasks/t0018_literature_survey_synaptic_integration/)

The answer asset synaptic-integration-priors-for-dsgc-modelling produces a 6-point
specification for DSGC synaptic integration in NEURON extending the space-clamp/AIS/NMDAR
constraints from t0017. The downstream DSGC compartmental-model build task must implement: (1)
AMPA with dual-exponential kinetics (tau_rise 0.2-0.4 ms, tau_decay 1-3 ms) and NMDA with
Mg2+-block + tau_decay 100-200 ms at 32 degC on glutamatergic inputs, (2) GABA_A with shunting
(reversal near resting Vm) and tau_decay 5-20 ms on SAC inputs, (3) E->I temporal lag of 15-50
ms on preferred-direction stimuli reproducing Wehr & Zador 2003 co-tuning, (4) asymmetric
GABAergic inputs that are strong on null-side dendrites (to match Euler-Detwiler-Denk 2002 SAC
Ca2+ DS index 0.3-0.5) and weak on preferred-side dendrites, (5) dendritic-location-dependent
EPSP attenuation consistent with Hausser-Mel lambda_DC 100-300 um, (6) named fitting
objectives for DSI under shunting-inhibition block (should drop toward 0) and EPSP/IPSP charge
balance during null-direction motion.

</details>

<details>
<summary>🧪 <strong>Extend voltage-gated-channel survey with recent DSGC-specific
Nav/Kv patch-clamp and super-resolution AIS microdomain papers</strong>
(S-0019-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0019_literature_survey_voltage_gated_channels](../../tasks/t0019_literature_survey_voltage_gated_channels/)

The scaled-down 5-paper survey covers the five canonical themes (Nav subunit localisation at
AIS, Kv1 subunit expression at AIS, RGC HH-family kinetic rate functions, Nav1.6 vs Nav1.2
co-expression kinetics, AIS Nav conductance density) but with one classical paper per theme. A
follow-up survey task should add ~5 DSGC-targeted papers across: (a) DSGC-specific Nav/Kv
patch-clamp measurements at near-physiological temperature, (b) super-resolution microscopy of
AIS microdomains (panNav vs subtype-specific antibodies, STED/STORM), (c) developmental Nav/Kv
channel trajectory studies in RGC AIS, (d) M-current/Kv7/KCNQ channels at RGC AIS, (e) Kv3
fast-delayed-rectifier measurements in RGC. This closes the gap between canonical
voltage-gated-channel theory and DSGC-specific parameters.

</details>

<details>
<summary>🧪 <strong>Excitation-side sensitivity sweep under gabaMOD-swap to close
the 25 Hz peak-firing-rate gap</strong> (S-0020-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0020_port_modeldb_189347_gabamod](../../tasks/t0020_port_modeldb_189347_gabamod/)

Under the native gabaMOD-swap protocol, DSI (0.7838) sits inside the [0.70, 0.85] envelope but
PD peak (14.85 Hz) is 25.15 Hz below the 40 Hz floor. Protocol is now ruled out, so the
shortfall must live on the excitation side. Run a factorial sweep over (a) BIP synapse count
{88, 177, 354}, (b) excMOD on AMPA+NMDA in {0.5, 1.0, 1.5, 2.0, 3.0}, (c) stimulus drive
{baseline, +50%, +100%}, holding gabaMOD at the 0.33/0.99 PD/ND pair. Report the smallest
config shift that moves peak into [40, 80] Hz without dragging DSI outside [0.70, 0.85].
Distinct from S-0008-04 (sweeps all parameters including GABA side under the rotation-proxy
protocol); this is excitation-only under the native driver, addressable only now that t0020
localised the gap. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Reproduce Poleg-Polsky 2016 Fig 1D/H subthreshold validation
targets (PSP amplitude, NMDAR slope angle)</strong> (S-0020-02)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0020_port_modeldb_189347_gabamod](../../tasks/t0020_port_modeldb_189347_gabamod/)

compare_literature.md flags that the paper reports concrete subthreshold validation targets
that this task did not measure: PD NMDAR-mediated PSP component 5.8 +/- 3.1 mV and ND 3.3 +/-
2.8 mV (Fig 1D, n=19), and NMDAR multiplicative scaling slope angle 62.5 +/- 14.2 deg (Fig 1H,
additive baseline 45 deg). Extend the gabaMOD-swap driver to record somatic whole-cell voltage
traces (v_soma, not just spike count) across the 40-trial sweep, compute (1) the peak PSP
amplitude in a 0-200 ms post-stimulus window per condition and (2) the slope-angle regression
over a scan of AMPA vs NMDA drive ratios, then gate each against the paper's n=19 mean +/- SD
intervals. This turns a single spike-output check into a multi-level subthreshold validation
that exercises the cell's passive and NMDA-block biophysics independently of spike
thresholding. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Intermediate-gabaMOD sensitivity sweep to map the PD-ND
transition curve</strong> (S-0020-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0020_port_modeldb_189347_gabamod](../../tasks/t0020_port_modeldb_189347_gabamod/)

The canonical protocol uses only the two endpoints gabaMOD = 0.33 (PD) and 0.99 (ND).
Task_description Scope explicitly deferred intermediate values as follow-up work. Run 20
trials per condition at gabaMOD in {0.20, 0.33, 0.50, 0.66, 0.83, 0.99} and plot firing rate
vs gabaMOD plus DSI computed as (rate_at_0.33 - rate_at_X)/(rate_at_0.33 + rate_at_X).
Outputs: (1) a firing-rate-vs-gabaMOD curve that shows whether the 0.33 -> 0.99 transition is
sigmoidal, threshold-like, or linear; (2) the critical gabaMOD value at which DSI crosses 0.5
(useful for later calibration); (3) a CSV with schema (gabamod, trial_seed, firing_rate_hz).
Probes whether the paper's two-point choice lies on a plateau or a steep-response region of
the inhibition axis, directly informing the inhibition-strength free parameter for later
optimisation. Recommended task types: experiment-run.

</details>

<details>
<summary>📚 <strong>Extend tuning_curve_loss with a two-point (PD/ND) scoring API to
make t0012 usable under the native protocol</strong> (S-0020-04)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0020_port_modeldb_189347_gabamod](../../tasks/t0020_port_modeldb_189347_gabamod/)

research_code.md records that t0012's high-level score() entry point rejects the two-condition
CSV because its loader's _validate_angle_grid requires exactly 12 angles on a 30-degree
spacing. t0020 worked around this by re-implementing the DSI formula inline in
score_envelope.py. Every future gabaMOD-swap task (including S-0020-01 and S-0020-03 above)
will hit the same wall. Add a score_two_point(pd_rates: np.ndarray, nd_rates: np.ndarray, *,
dsi_envelope, peak_envelope) -> TwoPointScore API to tuning_curve_loss that returns DSI, mean
PD, mean ND, per-condition stderr, gate.passed, plus optional per-trial CIs via bootstrap.
Keep the 12-angle score() untouched; the new API is an additional entry point. Register it in
the tuning_curve_loss library details.json entry_points. Recommended task types:
write-library.

</details>

<details>
<summary>📊 <strong>Add a per-trial spike-count floor to the two-point envelope gate
to catch biologically implausible passes</strong> (S-0020-05)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0020_port_modeldb_189347_gabamod](../../tasks/t0020_port_modeldb_189347_gabamod/)

Plan Risks & Fallbacks explicitly anticipated this scenario: DSI can land inside the envelope
while absolute firing rates stay unrealistically low (t0020 recorded DSI 0.7838 / peak 14.85
Hz exactly here). The current gate checks (mean_PD in [40, 80] Hz, DSI in [0.70, 0.85]) but
does not enforce biological plausibility at the trial level: the gate could pass with, say,
one trial firing 80 Hz and nineteen firing 0 Hz. Extend the envelope gate (in
tuning_curve_loss or the t0020 scorer) to add a trial-level floor: require that at least
N_pd_pass PD trials fire above a biological minimum threshold (e.g., 5 Hz). Report the
per-trial floor result alongside the mean-based envelope. Rerun scoring over t0020's existing
40-trial CSV to verify the new gate flags the current run as failed on the floor (baseline
expectation). Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>📊 <strong>Trial-count power analysis for the PD/ND DSI estimator (bootstrap
CI vs N_trials)</strong> (S-0020-06)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0020_port_modeldb_189347_gabamod](../../tasks/t0020_port_modeldb_189347_gabamod/)

t0020 reports DSI 0.7838 from 20 trials per condition but quotes no confidence interval.
Before launching sensitivity sweeps (S-0020-01, S-0020-03), future tasks need to know how many
trials per condition are needed to resolve, say, a 0.05-DSI difference at 95% CI. Compute
bootstrap 95% CIs on DSI for N_trials per condition in {5, 10, 20, 40, 80} by resampling with
replacement (10,000 resamples) from a single long run (80 trials per condition, reusing
run_gabamod_sweep.py with --n-trials 80). Output: (1) a CSV
trial_count,dsi_mean,dsi_ci_low,dsi_ci_high,peak_mean,peak_ci_low,peak_ci_high; (2) a plot of
DSI CI width vs trial count; (3) a recommended N_trials for each sensitivity-analysis budget
tier. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>📚 <strong>Extend t0011 response-visualisation library with a
condition-based (PD/ND) raster+PSTH plot</strong> (S-0020-07)</summary>

**Kind**: library | **Priority**: low | **Date**: 2026-04-20 | **Source**:
[t0020_port_modeldb_189347_gabamod](../../tasks/t0020_port_modeldb_189347_gabamod/)

t0011's tuning_curve_viz library supports angle-based rasters (one column per angle) but the
two-condition CSV produced by t0020 has no angle axis; only the bar chart (plot_pd_vs_nd.py,
t0020 local code) currently visualises it. Extend t0011 with
plot_condition_raster_psth(spike_times_df, *, conditions=('PD','ND'), out_png) that draws a
two-column raster (one per condition) above a PSTH panel. Requires t0020 (or a follow-up) to
first record per-trial spike times (not just rates) from run_gabamod_sweep.py. Complements
S-0011-01 (angle-based raster on the rotation-proxy port); this is the condition-based
analogue for the native-protocol port. Once merged, back-apply to t0020's existing sweep to
produce a publication-quality raster. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🧪 <strong>Factorial (g_Na, g_K) grid search on a DSGC compartmental model
to locate the DSI-maximising conductance ridge</strong> (S-0002-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-19 | **Source**:
[t0002_literature_survey_dsgc_compartmental_models](../../tasks/t0002_literature_survey_dsgc_compartmental_models/)

No paper in the 20-paper corpus (including Fohlmeister2010, Schachter2010, PolegPolsky2016,
Vaney2012) reports a factorial grid search over somatic (g_Na, g_K) pairs for a DSGC — this is
the central gap identified for RQ1 by the survey. Run a grid with g_Na swept across 0.02-0.20
S/cm^2 and g_K (delayed rectifier) swept across 0.003-0.050 S/cm^2 on the baseline DSGC
morphology and 177+177 synaptic budget, record DSI, preferred peak, null residual, and
tuning-curve HWHM at each point, and publish the ridge of combinations that hit DSI 0.7-0.85
with peak 40-80 Hz and null < 10 Hz. This directly supplies the RQ1 answer the project needs.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA/AMPA density ratio scan at fixed 3-5x null/preferred IPSC
asymmetry</strong> (S-0002-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0002_literature_survey_dsgc_compartmental_models](../../tasks/t0002_literature_survey_dsgc_compartmental_models/)

PolegPolsky2016 sets GABA/AMPA at 1:1 (177/177), while Park2014 and Taylor2002 constrain the
null/preferred IPSC ratio to 3-5x but not the total GABA density. Scan the GABA/AMPA density
ratio from 0.5 to 4.0 (keeping the 3-5x null asymmetry fixed, the 40-80 Hz preferred peak
fixed by the Na/K ridge, and the morphology and dendritic conductances fixed) and report how
tuning-curve HWHM and preferred peak rate co-vary. The expected pattern (sharper tuning at the
cost of lower peak rate) is stated in research_internet.md as hypothesis H4 but is not yet
tested in the literature. This directly refines the RQ3 answer. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>NMDA multiplicative-gain ablation to isolate its contribution
to DSI</strong> (S-0002-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0002_literature_survey_dsgc_compartmental_models](../../tasks/t0002_literature_survey_dsgc_compartmental_models/)

PolegPolsky2016 reports that NMDA receptors multiplicatively scale excitatory drive by ~2x and
sharpen directional discrimination, but the survey did not find a published ablation that
isolates the NMDA contribution independently of the AMPA+GABA core. Run three configurations
on the reproduced DSGC baseline (AMPA+GABA only, AMPA+GABA+NMDA with PolegPolsky2016 NMDA
parameters, AMPA+GABA+NMDA with NMDA_gain swept 1-4x) and report the DSI, peak rate, and HWHM
trajectories. This answers a specific open RQ3/RQ4-adjacent question that the literature
states but does not isolate experimentally. Recommended task types: experiment-run.

</details>

<details>
<summary>📂 <strong>Download the four discovered papers not included in the 20-paper
budget (Sivyer2017, Euler2002, Enciso2010, Webvision)</strong> (S-0002-07)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0002_literature_survey_dsgc_compartmental_models](../../tasks/t0002_literature_survey_dsgc_compartmental_models/)

research_internet.md catalogues 22 peer-reviewed candidates but only 20 became paper assets.
The held-back items are Sivyer2017 (dendro-dendritic cholinergic control of dendritic spike
initiation, Nat Commun), Euler2002 (SAC dendritic Ca signals are themselves directional,
Nature), Enciso2010 (SAC-network compartmental model, J Comp Neurosci), and the Webvision-DSGC
review. Sivyer2017 and Euler2002 directly constrain RQ4 and the presynaptic drive for RQ3, and
Enciso2010 provides a compartmental SAC-network model that could seed the presynaptic GABA
input for the DSGC model. Download them via /add-paper in a dedicated task and extend the
corpus to 24 papers. Recommended task types: download-paper, literature-survey.

</details>

<details>
<summary>📚 <strong>Register SAC presynaptic drive model as an asset for downstream
DSGC input construction</strong> (S-0002-08)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0002_literature_survey_dsgc_compartmental_models](../../tasks/t0002_literature_survey_dsgc_compartmental_models/)

Briggman2011 (SBEM wiring) and Ding2016 (cross-species comparison) supply the structural E/I
bias; Park2014 and Taylor2002 supply the 3-5x null/preferred IPSC amplitudes;
Sethuramanujam2016 adds ACh/GABA co-release; Hanson2019 challenges the pure SAC-asymmetry
model. Consolidate these findings into a pre-built SAC presynaptic drive asset (a reusable
library or dataset: angle-dependent GABA conductance time courses, AMPA time courses, and
their spatial distributions on a DSGC) so downstream DSGC simulation tasks do not each
re-implement the presynaptic waveform construction. The asset should expose a pure-function
API that takes (stimulus angle, velocity, asymmetry parameter) and returns per-synapse
conductance time courses. Recommended task types: write-library, feature-engineering.

</details>

<details>
<summary>📂 <strong>Reproduce the Park2014 mouse ON-OFF DSGC tuning-curve dataset
as a validation benchmark</strong> (S-0002-10)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0002_literature_survey_dsgc_compartmental_models](../../tasks/t0002_literature_survey_dsgc_compartmental_models/)

Park2014 (paper 10.1523_JNEUROSCI.5017-13.2014) and Chen2009 (paper
10.1113_jphysiol.2008.161240) are the two papers that set the mouse ON-OFF DSGC RQ5 targets
(DSI 0.6-0.9, peak 40-80 Hz, HWHM 60-90 deg). Park2014 is available open-access. Digitise the
published tuning-curve figure(s) into a reusable dataset asset (angle in degrees, spike rate
in Hz, error bars, cell counts) so the model can be scored against measured data rather than
only against the analytic target in t0004. This gives the project a literature-grounded
validation benchmark distinct from the canonical analytic target. Recommended task types:
download-dataset, data-analysis.

</details>

<details>
<summary>📚 <strong>Port the Poleg-Polsky & Diamond 2016 DSGC ModelDB 189347 into
the project as a library asset</strong> (S-0003-02)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-19 | **Source**:
[t0003_simulator_library_survey](../../tasks/t0003_simulator_library_survey/)

Download ModelDB 189347 (the only public DSGC NEURON model), re-run its included demo, and
register the resulting Python package as a library asset under `assets/library/`. This makes
the DSGC reference implementation available to every downstream simulation task without
re-download.

</details>

<details>
<summary>📚 <strong>Scaffold a NetPyNE `Batch` sweep harness for DSGC parameter
studies</strong> (S-0003-04)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0003_simulator_library_survey](../../tasks/t0003_simulator_library_survey/)

Build a small library that wraps NetPyNE's `Batch` class with the project's preferred sweep
axes (morphology scale, channel densities, synaptic weights) and an Optuna backend. Output: an
`assets/library/` entry plus a one-page usage example. This unblocks every downstream
tuning-curve experiment that needs to run more than one parameter combination.

</details>

<details>
<summary>📂 <strong>Generate weaker-DSI variant target tuning curves</strong>
(S-0004-01)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0004_generate_target_tuning_curve](../../tasks/t0004_generate_target_tuning_curve/)

Create sibling dataset assets (e.g., target-tuning-curve-weak-dsi,
target-tuning-curve-mid-dsi) with the same generator but r_peak values chosen so DSI lands at
~0.65 and ~0.75. Lets downstream fitting tasks test whether the optimisation pipeline is
robust across the 0.6-0.9 band instead of only the upper end.

</details>

<details>
<summary>📂 <strong>Add a Poisson-noise variant of the target trials</strong>
(S-0004-02)</summary>

**Kind**: dataset | **Priority**: low | **Date**: 2026-04-19 | **Source**:
[t0004_generate_target_tuning_curve](../../tasks/t0004_generate_target_tuning_curve/)

Replace the current Gaussian-noise trial replicates with Poisson counts converted to rates
(Fano factor ~1) and register it as a separate dataset asset. This would give
tuning_curve_reliability a noise model closer to real spike statistics while keeping the
closed-form mean curve unchanged.

</details>

<details>
<summary>📚 <strong>Build a small reusable library for target-vs-simulated tuning
curve metrics</strong> (S-0004-03)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-19 | **Source**:
[t0004_generate_target_tuning_curve](../../tasks/t0004_generate_target_tuning_curve/)

Factor the closed-form DSI, HWHM, tuning_curve_rmse, and tuning_curve_reliability computations
out of individual tasks into a shared library asset. Every later fitting task will need these
four functions; centralising them avoids divergent reimplementations and makes metric values
reproducible from parameters alone.

</details>

<details>
<summary>📂 <strong>Download additional Feller-archive DSGC reconstructions to enable
cross-cell variability sensitivity analysis</strong> (S-0005-03)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0005_download_dsgc_morphology](../../tasks/t0005_download_dsgc_morphology/)

The current dsgc-baseline-morphology commits the project to a single reconstructed cell
(141009_Pair1DSGC). Cell-to-cell variability in branching pattern, total path length, and
arbor extent is a known source of variance in DSGC tuning curves (RQ2), and the Feller archive
on NeuroMorpho hosts several sibling ON-OFF DSGC reconstructions from the same lab (e.g.,
141009_Pair2DSGC and other 2014 Pair* records). Download 3-5 additional Feller-archive ON-OFF
DSGC SWCs as separate dataset assets (each with its own NeuroMorpho neuron_id and provenance),
validate each with the existing validate_swc.py parser, and tabulate per-cell compartment
count, branch points, and total dendritic path length so a downstream morphology-sweep task
can quantify cross-cell variability without committing a priori to a specific morphology.
Recommended task types: download-dataset.

</details>
