# Category: Dendritic Computation

Signal processing that occurs in dendrites prior to somatic spike generation.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (44)](../papers/by-category/dendritic-computation.md) | [Answers
(9)](../answers/by-category/dendritic-computation.md) | [Suggestions
(86)](../suggestions/by-category/dendritic-computation.md) | [Datasets
(1)](../datasets/by-category/dendritic-computation.md) | [Libraries
(1)](../libraries/by-category/dendritic-computation.md) | [Predictions
(4)](../predictions/by-category/dendritic-computation.md)

---

## Papers (44)

<details>
<summary>📝 <strong>Retinal waves shape starburst amacrine cell dendrite development
through a direction-selective dendritic computation</strong> — Pitcher
et al., 2026</summary>

| Field | Value |
|---|---|
| **ID** | `10.64898_2026.02.02.701812` |
| **Authors** | Miah N. Pitcher, Aanica S. B. Gonzales, Raul Habib, Marla B. Feller |
| **Venue** | bioRxiv (preprint) |
| **DOI** | `10.64898/2026.02.02.701812` |
| **URL** | https://www.biorxiv.org/content/10.64898/2026.02.02.701812v1 |
| **Date added** | 2026-05-04 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.64898_2026.02.02.701812/summary.md) |

Pitcher et al. ask whether spontaneous retinal waves can instruct dendritic morphology through
a local dendritic computation, using developing mouse SACs as a model. The work spans calcium
imaging in P7-P13 retina, pharmacological dissection with TEA, two genetic models (b2-nAChR-KO
for activity loss, FRMD7tm for loss of wave propagation bias), and 3D dendrite reconstructions
across the same ages.

The methodology combines two-photon imaging of GCaMP-loaded single SAC dendrites with
quadrant-resolved DSI metrics for moving bars and propagating waves, plus reconstruction-based
quantification of nasal-vs-temporal dendrite length and distal complexity. The experimental
design is elegant: it shows that the dendritic computation is present (P10 imaging), that it
depends on K+-channel-based compartmentalisation (TEA experiment), that activity is required
for outgrowth (b2-nAChR-KO), and that wave *direction*, not just wave existence, is required
for the morphological asymmetry (FRMD7tm).

The headline finding is that SAC dendrites at P9-P11 exhibit centrifugal-preferred direction
selectivity to retinal waves; that dendritic tuning rises with distance from the soma; that
TEA abolishes this tuning; and that wild-type SACs have nasal dendrites longer than temporal
dendrites (a difference absent when wave propagation bias is removed). Together these results
identify SACs as the earliest known cellular decoder of retinal-wave propagation bias and link
that decoding to a structural morphological asymmetry that persists into the adult
direction-selective circuit.

For this project the paper is upstream context, not a direct input. t0080 (Bed B v3) treats
the SAC drive onto the DSGC as a fixed, idealised null-side inhibitory waveform; it does not
model SAC morphology development. Pitcher 2026 is therefore relevant only as developmental
background for *why* the SAC inhibitory drive has its asymmetric form in the mature retina,
and as a flagged source of biological asymmetry that future tasks could optionally model if
the inhibitory machinery onto the DSGC is ever brought back into the optimisation.

</details>

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
<summary>📖 <strong>Behavioral time scale synaptic plasticity underlies CA1 place
fields</strong> — Bittner et al., 2017</summary>

| Field | Value |
|---|---|
| **ID** | `10.1126_science.aan3846` |
| **Authors** | Katie C. Bittner, Aaron D. Milstein, Christine Grienberger, Sandro Romani, Jeffrey C. Magee |
| **Venue** | Science (journal) |
| **DOI** | `10.1126/science.aan3846` |
| **URL** | https://www.science.org/doi/10.1126/science.aan3846 |
| **Date added** | 2026-04-20 |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |
| **Added by** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Full summary** | [`summary.md`](../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1126_science.aan3846/summary.md) |

Bittner and colleagues (2017) discover a new form of synaptic plasticity in hippocampal area
CA1 that operates on the behavioral time scale (seconds) and is driven by dendritic plateau
potentials. Using in vivo whole-cell patch-clamp from CA1 pyramidal neurons during running on
a linear treadmill, the authors combine natural observation of spontaneous plateaus with
artificial plateau induction (via somatic current injection) paired with Schaffer-collateral
stimulation.

The methodology systematically varies the temporal offset between the plateau and the pairing
synaptic input, mapping the BTSP time window. Compartmental modelling and pharmacological
block of NMDA receptors and voltage-gated calcium channels identify the mechanistic substrate
as a calcium-activated intracellular eligibility trace that persists for seconds after a
plateau.

The central finding is that a single plateau, paired with running, is sufficient to create a
place field in one trial. The BTSP time window extends approximately plus-or-minus 1-2 seconds
on either side of the plateau, is symmetric (non-Hebbian), and does not require classical
pre-before-post spike pairing. Place-field half-width is approximately 1.5-2 seconds (about
15-20 cm at typical mouse speeds). Plateau potentials themselves are 30-60 mV in amplitude,
50-300 ms in duration, and require EC3 input to the apical tuft plus active NMDA conductances.

For the DSGC modelling programme this paper is important in two ways. First, it generalizes
plateau-driven dendritic computation beyond Larkum-style cortical BAC firing to a hippocampal
place-field mechanism, establishing plateaus as a cross-cell-type computational motif. Second,
the quantitative BTSP rule (symmetric, seconds-wide, plateau-gated) provides a candidate
mechanism that DSGC models could test: if DSGC dendrites can host brief plateau-like
depolarisations during preferred-direction motion, these could in principle gate
direction-selective plasticity on a behaviorally relevant timescale. Whether DSGC dendritic
geometry (short, non-tufted, compact) supports such plateaus is an open empirical question
that follow-up compartmental simulation can address.

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
<summary>📖 <strong>Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide
Range of Dendritic and Perisomatic Active Properties</strong> — Hay et
al., 2011</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1002107` |
| **Authors** | Etay Hay, Sean Hill, Felix Schurmann, Henry Markram, Idan Segev |
| **Venue** | PLoS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1002107` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107 |
| **Date added** | 2026-05-03 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md) |

Hay et al. (2011) address a long-standing gap in compartmental modeling of L5b cortical
pyramidal cells: no published model simultaneously reproduced the perisomatic Na+ step-current
f-I behavior and the BAP-activated dendritic Ca2+ ("BAC") firing observed in adult-rat slice
recordings. The paper's research question is whether a single conductance-based model in a
reconstructed morphology can be fit to both regimes with experimentally measured cell-to-cell
variability, and which channel densities and Ca2+-dynamics parameters are necessary or
sufficient for each regime.

Methodologically, the authors define 20 firing features (10 perisomatic, 10 BAC), each with an
experimental mean and SD computed across several cells. They use multi-objective optimization
with an elitist non-dominated sorting evolutionary algorithm — population 1000, 500
generations, 240 to 1024 CPU cores, 2-5 days runtime — to optimize 22 free parameters. The
free parameters are the maximal densities of nine ion channels (Nat, Nap, Kp, Kt, Kv3.1,
Ca_HVA, Ca_LVA, SK, Im) in soma and apical compartments, plus the Ca2+ buffer parameters gamma
and tdecay. The Ih distribution is fixed to preserve subthreshold properties. Models are
accepted when every feature falls within 2-3 SD of the experimental mean. Mechanism kinetics
use Hodgkin-Huxley formalism with Q10 = 2.3 and a -10 mV junction-potential shift where
applicable.

The headline result is a set of about 2000 acceptable L5b PC models published in ModelDB
(accession 139653). Single-target fits are easier (899 BAC-only, 52 perisomatic-only) but
typically fail the other target. Joint fits achieve every feature within 2-3 SD: e.g. BAP
amplitude **45 +/- 10 mV** at 620 um, Ca2+ spike peak **6.73 +/- 2.54 mV**, perisomatic spike
frequencies of **9 / 14.5 / 22.5 Hz**, AP half-width of **1.31 ms**, slow AHP depth around
**-60 mV**. Cross-target parameter analysis identifies apical Nat and apical Kv3.1 densities
as the dominant levers controlling BAP propagation, and shows that morphology swaps degrade
BAC features more than perisomatic features.

For this project, Hay 2011 is a direct upstream dependency of t0074 and t0078: the SK_E2 and
CaDynamics_E2 MOD files vendored under t0074 originate here, and t0078's `tau_ca_multiplier`
extension to CaDynamics_E2 is an additional knob on the same gamma + tdecay sub-membrane shell
formalism defined in this paper. The cited parameter ranges (gamma in 0.0005-0.05; soma tdecay
20-1000 ms; apical tdecay 20-200 ms) provide the prior box that t0078's MOBO should explore.
The multi-objective + per-feature-SD scoring + Pareto-acceptable-ensemble methodology is also
the template t0078 inherits for reporting and analyzing its own MOBO results. Citing Hay 2011
in the t0078 substrate documentation is therefore mandatory.

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
<summary>📖 <strong>Dendritic Discrimination of Temporal Input Sequences in Cortical
Neurons</strong> — Branco et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1126_science.1189664` |
| **Authors** | Tiago Branco, Beverley A. Clark, Michael Häusser |
| **Venue** | Science (journal) |
| **DOI** | `10.1126/science.1189664` |
| **URL** | https://www.science.org/doi/10.1126/science.1189664 |
| **Date added** | 2026-04-19 |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/summary.md) |

Branco, Clark, and Häusser ask whether individual cortical dendrites can detect the temporal
order of their synaptic inputs — a computation previously assumed to require networks of
neurons. Using multi-site two-photon glutamate uncaging in layer 2/3 pyramidal neurons of rat
somatosensory and visual cortex, they show that single dendrites produce systematically larger
somatic EPSPs and higher spike probabilities when synapses are activated from the branch tip
toward the soma ("IN") than from soma to tip ("OUT"), and that local dendritic Ca2+ signals
carry the same directionality. The finding scales up: neurons can also discriminate arbitrary
random temporal sequences delivered to a single dendrite or distributed across multiple
dendrites.

The mechanism is revealed by pharmacology and a compartmental model. Blocking NMDA receptors
with D-AP5 abolishes supralinear summation (response drops from **223 ± 9%** to **103 ± 3%**
of linear sum) and the directional asymmetry (IN-OUT difference shrinks from **2.8 mV** to
**0.4 mV**). The compartmental model with passive dendrites and AMPA+NMDA synapses fully
reproduces direction sensitivity, identifying the mechanism as the interaction between the
dendritic impedance gradient (high distally, low proximally) and the voltage-dependent Mg2+
block of NMDA receptors. Sequences initiated distally depolarise more locally, progressively
relieving Mg2+ block and generating a regenerative NMDAR cascade that is absent in the
distal-to-proximal direction.

The paper's headline results are: IN responses **31 ± 4%** larger than OUT (n = 20); spike
probability **38 ± 9%** higher; Ca2+ signals **48 ± 13%** larger; random pattern
discrimination probability **40%** (> 1 mV, n = 7); multi-dendrite sequence discrimination
**4.0 ± 1.3 mV** (n = 5). All effects are abolished by D-AP5 or hyperpolarisation. The
mechanism is confirmed in layer 5 pyramidal neurons and hippocampal dentate gyrus granule
cells.

For this project, Branco et al. (2010) provides the mechanistic logic for dendritic direction
selectivity in the compartmental model: the impedance gradient combined with NMDA receptor
non-linearity converts a spatiotemporal sweep of synaptic activation into a directionally
tuned output. Although the paper uses cortical pyramidal neurons, the mechanism explicitly
generalises to any neuron with an impedance gradient and NMDAR-containing synapses, including
DSGCs. The ModelDB 140828 NEURON implementation offers directly reusable AMPA+NMDA synapse
code, the ~2–3 µm/ms optimal velocity sets a wave-sweep parameter target, and the D-AP5
results provide a clear internal control for validating the synaptic component of the DSGC
model.

</details>

<details>
<summary>📖 <strong>One Rule to Grow Them All: A General Theory of Neuronal Branching
and Its Practical Application</strong> — Cuntz et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1000877` |
| **Authors** | Hermann Cuntz, Friedrich Forstner, Alexander Borst, Michael Häusser |
| **Venue** | PLoS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1000877` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000877 |
| **Date added** | 2026-04-21 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`cable-theory`](../../meta/categories/cable-theory/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/summary.md) |

Cuntz, Forstner, Borst and Häusser propose that the apparent diversity of dendritic
morphologies across cell classes is the solution of a single optimisation problem: given a
target spanning field populated with carrier points, grow a tree that simultaneously minimises
total wiring length (Cajal's cytoplasm conservation) and path length from the root (Cajal's
conduction-time conservation). A single scalar balancing factor `bf` weighs the two costs, and
an extended minimum-spanning-tree algorithm converts the problem into a tractable greedy
construction.

The method is validated on three cell classes that sit in very different corners of morphology
space — fly LPTCs, mammalian CA1 pyramidal neurons, and cerebellar Purkinje cells — by
matching Sholl profiles, branch-order distributions, total dendritic length, and
segment-length statistics between synthetic and reconstructed arbors. The balancing factor
additionally maps onto electrotonic compartmentalisation, linking a single geometric parameter
to cable-theoretic behaviour. The authors release the method as the open-source MATLAB "TREES
toolbox", which also contains morphometric analyses and a semi-automated reconstruction
pipeline from confocal image stacks.

The headline results are quantitative: synthetic trees match total wiring length within a few
percent, reproduce Sholl and branch-order distributions across all three cell classes, and do
so with biologically realistic `bf` clustering at intermediate values (~**0.2-0.7**). The
theory thereby elevates Cajal's qualitative laws into a predictive generator and provides the
first genuinely low-dimensional parametric family of realistic dendritic morphologies.

For this project's literature survey on how morphology shapes direction selectivity, Cuntz2010
is flagged as borderline: it contains no DS experiments or simulations. However, it is the
enabling tool for the sweep-based approach we plan. Its 3-5 Cuntz parameters define a
tractable morphology embedding in which DSI can be evaluated compartmentally, and the mapping
between `bf` and electrotonic compartmentalisation is directly mechanistically relevant to DS
computations that rely on dendritic independence (e.g. starburst amacrine sectors, DSGC
subunit models). It will be cited as the morphology-generation backbone for any
synthetic-arbor DS sweep in the project.

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
<summary>📖 <strong>Axon Initial Segment Kv1 Channels Control Axonal Action Potential
Waveform and Synaptic Efficacy</strong> — Kole et al., 2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2007.07.031` |
| **Authors** | Maarten H.P. Kole, Johannes J. Letzkus, Greg J. Stuart |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2007.07.031` |
| **URL** | https://doi.org/10.1016/j.neuron.2007.07.031 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0019_literature_survey_voltage_gated_channels`](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Full summary** | [`summary.md`](../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1016_j.neuron.2007.07.031/summary.md) |

Maarten H.P. Kole and colleagues (2007) published "Axon Initial Segment Kv1 Channels Control
Axonal Action Potential Waveform and Synaptic Efficacy" in Neuron. The paper is included in
this task's survey because it contributes to the "Kv1 subunit expression at AIS" theme of
voltage-gated-channel priors relevant to the direction-selective retinal ganglion cell (DSGC)
compartmental model.

CrossRef did not return a machine-readable abstract for this paper. The paper's claims must
therefore be read directly from the publisher PDF before being used in the DSGC model-fitting
pipeline.

The paper's primary significance for this project is its contribution to the "Kv1 subunit
expression at AIS" evidence pool. The answer asset
`assets/answer/nav-kv-combinations-for-dsgc-modelling/` records which DSGC model Nav/Kv
channel combination (subunit identity, compartment, conductance density, activation
half-voltage, or kinetic time constant) this paper supplies, together with the numerical value
when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

</details>

<details>
<summary>📖 <strong>Dendritic Computation</strong> — London & Hausser, 2005</summary>

| Field | Value |
|---|---|
| **ID** | `10.1146_annurev.neuro.28.061604.135703` |
| **Authors** | Michael London, Michael Hausser |
| **Venue** | Annual Review of Neuroscience (journal) |
| **DOI** | `10.1146/annurev.neuro.28.061604.135703` |
| **URL** | https://www.annualreviews.org/doi/10.1146/annurev.neuro.28.061604.135703 |
| **Date added** | 2026-04-20 |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`cable-theory`](../../meta/categories/cable-theory/) |
| **Added by** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Full summary** | [`summary.md`](../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1146_annurev.neuro.28.061604.135703/summary.md) |

London and Hausser (2005) wrote the canonical review of dendritic computation: a structured
synthesis of roughly four decades of theoretical and experimental work on how single neurons
use their dendritic structure, voltage-gated ion channels, and nonlinear synaptic conductances
to perform elementary computations. The review organises the literature around three
biophysical axes (passive cable properties, active ion-channel-mediated nonlinearities, and
synaptic-placement-dependent summation) and links each to specific computational primitives
such as coincidence detection, multiplicative gain, branch-level AND-gates, and direction
selectivity.

The central synthesis is that dendritic integration is never purely linear: the same synaptic
input pattern produces linear, sublinear, or supralinear summation depending on three factors:
(1) spatial clustering of inputs (same vs different dendritic branches), (2) temporal
coincidence (within a few to tens of milliseconds), and (3) membrane state (resting,
depolarized, or post-spike). Nonlinearities are produced by NMDA spikes (approximately 4-8
clustered spines threshold, 150-300% supralinear boost), dendritic sodium spikes
(Stuart-Sakmann 1994), and calcium plateaus (Larkum 1999, approximately 30-50 ms duration),
and can be gated off by strategically placed shunting inhibition (Koch, Poggio and Torre
1982).

The review explicitly treats retinal direction selectivity as a paradigmatic example of
dendritic computation in action: the Koch-Poggio-Torre shunting mechanism, validated
experimentally in rabbit DSGCs by Taylor 2000, demonstrates that a classical dendritic
nonlinearity (asymmetric shunting inhibition) is sufficient to implement a behaviorally
relevant computation (motion direction selectivity). The review argues that comparable
computational primitives exist in pyramidal and cerebellar neurons, unified by the three-axis
framework.

For the DSGC modelling programme this review is indispensable. It provides (a) the taxonomy
within which DSGC-specific mechanisms should be placed, (b) the quantitative cross-cell-type
reference numbers (electrotonic length ranges, NMDA-spike thresholds, shunting-inhibition
effect sizes) that calibrate DSGC models against the broader literature, and (c) the
experimental-design template (ablate one nonlinearity at a time, measure change in behavior)
that DSGC simulations should follow. Specifically, any DSGC model should be analysed under
systematic ablation of each of the five dendritic primitives (cable filtering, NMDA
supralinearity, Na+ spikes, Ca2+ plateaus, shunting asymmetry) to report which are necessary
and which are sufficient for DS.

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
<summary>📖 <strong>Computational subunits in thin dendrites of pyramidal
cells</strong> — Polsky et al., 2004</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn1253` |
| **Authors** | Alon Polsky, Bartlett W. Mel, Jackie Schiller |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn1253` |
| **URL** | https://www.nature.com/articles/nn1253 |
| **Date added** | 2026-04-20 |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |
| **Added by** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Full summary** | [`summary.md`](../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_nn1253/summary.md) |

Polsky, Mel and Schiller (2004) test a core prediction of the two-layer model of
pyramidal-cell computation: that thin basal and apical oblique dendrites function as
independent sigmoidal integrative subunits whose outputs sum at the soma. Using two-photon
glutamate uncaging at pairs of spatially precise sites, they compare measured paired EPSPs to
the linear sum of individual-site responses.

The experimental design varies the spatial configuration of the two uncaged sites: either on
the same thin dendrite (same-branch) or on two different thin dendrites (different-branch).
NMDA-spike involvement is tested with APV. Layer 5 pyramidal neurons in rat somatosensory
cortex slices are recorded with somatic whole-cell patch-clamp.

Same-branch paired inputs produce somatic EPSPs 150-300% of the linear prediction, reflecting
supralinear dendritic integration. Different-branch pairs sum within ~5% of the linear
prediction. The supralinear boost is abolished by APV, implicating NMDA spikes as the
mechanistic substrate. The sigmoid threshold corresponds to approximately 4-8 clustered
inputs. The effect generalises across distal and proximal thin dendrites.

For DSGC modelling this paper is the mechanistic template for a dendritic-sector
supralinear-integration hypothesis: if starburst-amacrine-cell (SAC) inhibition selectively
gates dendritic sectors during null-direction motion while allowing preferred-direction
bipolar inputs to cluster onto individual DSGC dendrites, the resulting supralinear boost
could contribute to direction selectivity. Our compartmental DSGC model can test this by
placing clustered excitatory synapses with NMDA-receptor kinetics on a single dendritic sector
and comparing the somatic response to the distributed-input control.

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
<summary>📖 <strong>Dendrites: bug or feature?</strong> — Häusser & Mel, 2003</summary>

| Field | Value |
|---|---|
| **ID** | `no-doi_HausserMel2003_s0959-4388-03-00075-8` |
| **Authors** | Michael Häusser, Bartlett Mel |
| **Venue** | Current Opinion in Neurobiology (journal) |
| **DOI** | `10.1016/s0959-4388(03)00075-8` |
| **URL** | https://doi.org/10.1016/s0959-4388(03)00075-8 |
| **Date added** | 2026-04-20 |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Full summary** | [`summary.md`](../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/no-doi_HausserMel2003_s0959-4388-03-00075-8/summary.md) |

Michael Häusser and colleagues (2003) published "Dendrites: bug or feature?" in Current
Opinion in Neurobiology. The paper is included in this task's survey because it contributes to
the "Dendritic-location dependence of PSP integration" theme of synaptic-integration priors
relevant to the direction-selective retinal ganglion cell (DSGC) compartmental model.

CrossRef did not return a machine-readable abstract for this paper. The paper's claims must
therefore be read directly from the publisher PDF before being used in the DSGC model-fitting
pipeline.

The paper's primary significance for this project is its contribution to the
"Dendritic-location dependence of PSP integration" evidence pool. The answer asset
`assets/answer/synaptic-integration-priors-for-dsgc-modelling/` records which DSGC model prior
(rise/decay time constant, attenuation factor, E-I lag, asymmetry ratio, or
shunting-inhibition location dependence) this paper supplies, together with the numerical
value when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

</details>

<details>
<summary>📖 <strong>Wiring Optimization in Cortical Circuits</strong> — Chklovskii
et al., 2002</summary>

| Field | Value |
|---|---|
| **ID** | `no-doi_Chklovskii2002_wiring-optimization-cortical` |
| **Authors** | Dmitri B. Chklovskii, Thomas Schikorski, Charles F. Stevens |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/s0896-6273(02)00679-7` |
| **URL** | https://doi.org/10.1016/s0896-6273(02)00679-7 |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`cable-theory`](../../meta/categories/cable-theory/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/no-doi_Chklovskii2002_wiring-optimization-cortical/summary.md) |

Chklovskii, Schikorski, and Stevens (2002) ask why cortical gray matter has the cellular
composition that it does. Earlier work in the wiring-economy tradition (Cajal; Cherniak;
Mitchison; Chklovskii and Stevens 2000) had argued qualitatively that wire length is minimised
under selection pressure, but these arguments did not predict any quantitative property of
cortical anatomy that could be falsified by direct measurement. The paper closes this gap by
recasting the problem as a constrained optimisation: maximise synapse density subject to
bounded axonal conduction delay and bounded passive dendritic attenuation, with axon and
dendrite radii as the free variables.

The methodological contribution is a parameter-free derivation. After applying the standard
cable scalings (delay proportional to length over root radius; space constant proportional to
root radius), the species-specific membrane and axial constants cancel in the optimum, leaving
a pure geometric prediction: axons plus dendrites should fill exactly 3/5 of the gray-matter
volume at the optimum. The authors then test this with serial-section electron microscopy of
mouse hippocampal CA1 neuropil, measuring the volume fraction occupied by each cellular
component, and report agreement with the 3/5 prediction.

The headline finding is therefore a quantitative confirmation of the wiring-economy principle
as a real biological selection pressure operating on cortical morphology, not merely a
qualitative heuristic. This is one of the most cited results in computational neuroanatomy
because it demonstrates that an optimisation principle, applied with explicit biophysical
constraints, can predict an a-priori property of a real cortical tissue volume to within
experimental error. Later work has extended the framework to dendritic branching morphology
(Cuntz et al. 2010), to cortical GABAergic interneurons (Budd and Kisvarday 2012), and to
whole-brain connectomes.

For the t0097 multi-objective DSGC optimisation catalogue, this paper provides the
foundational biological justification for adding a cytoplasm-volume / wiring-cost objective
alongside functional DSGC objectives (direction-selectivity index, EPSP fidelity, robustness).
The 3/5 result tells us that real cortical neurons sit close to a wiring optimum, so a DSGC
morphology that drifts very far from the natural cytoplasm volume in our optimisation is
biologically suspect even if it yields a high DSI. Together with Cuntz et al. (2010), this
paper anchors the "minimise total cytoplasm volume" recipe that the catalogue should adopt;
deviations from the optimal volume can be reported as a quantitative biological-plausibility
metric. The main caveat for our use is that the original Chklovskii et al. analysis is for
cortical gray matter, not retinal inner plexiform layer, so the exact 3/5 fraction may not
transfer numerically to DSGC dendritic arbours - but the underlying recipe (wire cost + delay
+ attenuation) is general and is what we should adopt.

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
<summary>📖 <strong>NMDA spikes in basal dendrites of cortical pyramidal
neurons</strong> — Schiller et al., 2000</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_35005094` |
| **Authors** | Jackie Schiller, Guy Major, Helmut J. Koester, Yitzhak Schiller |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/35005094` |
| **URL** | https://www.nature.com/articles/35005094 |
| **Date added** | 2026-04-20 |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Full summary** | [`summary.md`](../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_35005094/summary.md) |

Schiller, Major, Koester and Schiller (2000) report the discovery of NMDA spikes in the thin
basal and oblique dendrites of layer-5 neocortical pyramidal neurons. Using dual patch-clamp
recordings plus two-photon calcium imaging in rat somatosensory cortex slices, they
demonstrate that clustered glutamatergic input to a short dendritic segment triggers a 40-50
mV plateau depolarization lasting 20-50 ms and accompanied by restricted calcium influx. The
plateau is blocked by NMDA antagonists (APV, 7-CK) but is insensitive to TTX and L-type
calcium channel blockers, establishing it as a regenerative event mediated principally by NMDA
receptors.

Methodologically, the paper combines focal synaptic stimulation, two-photon glutamate
iontophoresis, and pharmacological dissection to isolate the NMDA-dependent plateau from the
other regenerative events. Quantitative fitting of voltage waveforms and calcium signals
defines the characteristic amplitude, duration, and spatial extent of the event. Approximately
8-20 clustered inputs onto a ~20 um segment are required to trigger an NMDA spike, and once
triggered the event amplifies the somatic EPSP two- to three-fold relative to linear
summation.

The headline results are that a pharmacologically distinct NMDA-mediated regenerative event
exists in thin cortical dendrites; the event is spatially confined to the activated branch,
consistent with thin basal and oblique dendrites acting as local integrative subunits; and
supralinear integration at the soma requires clustered, spatially coincident synaptic input -
a clean mechanistic criterion for when a cortical dendrite behaves supralinearly.

For this project, Schiller2000 is a canonical reference for the NMDA-spike mechanism and for
the branch-as-subunit computational framing. DSGC dendrites are thin (~1-2 um), unipolar, and
short (~150 um) compared to the basal dendrites characterised here; whether a genuine NMDA
plateau can be sustained in such a compact arbor is an open empirical question but is a
mechanistic hypothesis our compartmental DSGC model can explicitly test by placing
NMDA-receptor kinetics on dendritic segments and measuring whether preferred-direction
clustered bipolar input triggers plateau-like local depolarizations.

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
<summary>📖 <strong>A new cellular mechanism for coupling inputs arriving at
different cortical layers</strong> — Larkum et al., 1999</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_18686` |
| **Authors** | Matthew E. Larkum, J. Julius Zhu, Bert Sakmann |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/18686` |
| **URL** | https://www.nature.com/articles/18686 |
| **Date added** | 2026-04-20 |
| **Categories** | [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0016_literature_survey_dendritic_computation`](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Full summary** | [`summary.md`](../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_18686/summary.md) |

Larkum, Zhu and Sakmann (1999) resolve a longstanding question in cellular cortical
neuroscience: how can inputs arriving at anatomically distant dendritic sites (layer 1 tuft vs
perisomatic basal) be coupled into a single coherent output signal? Using simultaneous dual
whole-cell patch-clamp at the soma and distal apical dendrite of layer 5 pyramidal neurons,
the authors demonstrate that the apical dendrite contains a **calcium spike initiation zone**
near the main bifurcation whose high threshold is dramatically lowered when a backpropagating
action potential from the soma arrives within a brief coincidence window.

The methodology combines dual-patch recording with focal synaptic or glutamate stimulation of
the distal apical dendrite, and with pharmacological block of voltage-gated Ca2+ channels.
Coincidence paradigms vary the interval between somatic action potential and distal
depolarization systematically. The central finding is that a small (5-10 mV) distal
depolarization that is subthreshold when delivered alone becomes suprathreshold for the apical
Ca2+ spike when paired with a somatic AP within approximately 5-10 ms: **BAC firing**.

BAC firing produces a stereotyped 3-4 spike burst at the soma at approximately 100-200 Hz
instantaneous frequency, driven by the dendritic Ca2+ plateau (duration 30-50 ms) reinjecting
current into the soma. The calcium spike is abolished by Ni2+/Cd2+, confirming voltage-gated
Ca2+ channels as the substrate. The specific localization of the initiation zone near the
apical bifurcation, rather than along the entire trunk, establishes that distinct dendritic
compartments can host qualitatively distinct regenerative processes.

For the DSGC modelling programme this paper is important as the archetype of
**active-dendritic coincidence detection**. Any compartmental DSGC model that wants to test
whether dendritic Ca2+ spikes contribute to direction selectivity will use the Larkum
architecture as its template: a discrete high-threshold Ca2+-spike zone whose activation is
gated by coincident depolarization. If preferred-direction motion drives coincident EPSPs
along a DSGC dendritic sector while asymmetric null-direction inhibition disrupts the
coincidence, the Larkum mechanism predicts a DS-correlated burst output. The model should also
be validated against the Larkum burst-frequency and plateau-duration numbers reported here as
the canonical biophysical targets for Ca2+-plateau-mediated dendritic computation.

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
<summary>📖 <strong>Influence of dendritic structure on firing pattern in model
neocortical neurons</strong> — Mainen & Sejnowski, 1996</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_382363a0` |
| **Authors** | Zachary F. Mainen, Terrence J. Sejnowski |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/382363a0` |
| **URL** | https://www.nature.com/articles/382363a0 |
| **Date added** | 2026-04-20 |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`compartmental-modelling`](../../meta/categories/compartmental-modelling/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/summary.md) |

Mainen & Sejnowski's 1996 Nature paper is a landmark in compartmental neuroscience modelling
because it cleanly separates the roles of ion-channel density and dendritic morphology in
shaping neuronal firing patterns. By applying the same fixed set of sodium, potassium, and
calcium conductances to four reconstructed neuronal morphologies — layer-5 pyramidal, layer-3
pyramidal, stellate, and low-threshold-spiking interneuron — the authors reproduce the four
characteristic firing patterns observed in neocortical recordings without changing any
biophysical parameter except the dendritic tree.

Methodologically, the paper is a textbook example of the NEURON-based compartmental-modelling
workflow: reconstructed morphology, `d_lambda` spatial discretization, axonal spike initiation
with biophysically motivated channel distributions, and quantitative comparison of simulated
somatic firing patterns to experimental intracellular data. The calcium-driven slow
depolarizing current in large apical dendrites, coupled to axonal re-excitation through the
soma, emerges as the mechanism for intrinsic bursting.

The main finding is that morphology-driven differences in the dendritic load on the soma are
sufficient to explain observed firing-pattern diversity. Truncating the apical dendrite of the
layer-5 pyramidal morphology abolishes bursting; removing dendritic calcium conductance has
the same effect, showing the two factors are jointly necessary. This is a strong and
counterintuitive result that reshaped how compartmental modellers interpret cell-type-specific
firing.

For this project, the paper is directly relevant in three ways. First, it confirms that our
DSGC compartmental models must use accurate dendritic reconstructions, not simplified
"ball-and-stick" approximations, before attributing behavioural differences to channel-density
variation between DSGC subtypes. Second, the axon-dendrite coupling framework it establishes
is essential context for understanding how spikes initiate and propagate in DSGCs given their
distinctive bistratified dendritic arbors. Third, the paper codifies the `d_lambda`
discretization practice that our NEURON models must follow to produce trustworthy
active-dendrite simulations.

</details>

<details>
<summary>📖 <strong>Channel kinetics determine the time course of NMDA
receptor-mediated synaptic currents</strong> — Lester et al., 1990</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_346565a0` |
| **Authors** | Robin A. J. Lester, John D. Clements, Gary L. Westbrook, Craig E. Jahr |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/346565a0` |
| **URL** | https://doi.org/10.1038/346565a0 |
| **Date added** | 2026-04-20 |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Full summary** | [`summary.md`](../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_346565a0/summary.md) |

Robin A. J. Lester and colleagues (1990) published "Channel kinetics determine the time course
of NMDA receptor-mediated synaptic currents" in Nature. The paper is included in this task's
survey because it contributes to the "AMPA/NMDA/GABA receptor kinetics" theme of
synaptic-integration priors relevant to the direction-selective retinal ganglion cell (DSGC)
compartmental model.

CrossRef did not return a machine-readable abstract for this paper. The paper's claims must
therefore be read directly from the publisher PDF before being used in the DSGC model-fitting
pipeline.

The paper's primary significance for this project is its contribution to the "AMPA/NMDA/GABA
receptor kinetics" evidence pool. The answer asset
`assets/answer/synaptic-integration-priors-for-dsgc-modelling/` records which DSGC model prior
(rise/decay time constant, attenuation factor, E-I lag, asymmetry ratio, or
shunting-inhibition location dependence) this paper supplies, together with the numerical
value when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

</details>

<details>
<summary>📖 <strong>Nonlinear interactions in a dendritic tree: localization, timing,
and role in information processing.</strong> — Koch et al., 1983</summary>

| Field | Value |
|---|---|
| **ID** | `10.1073_pnas.80.9.2799` |
| **Authors** | C Koch, T Poggio, V Torre |
| **Venue** | Proceedings of the National Academy of Sciences (journal) |
| **DOI** | `10.1073/pnas.80.9.2799` |
| **URL** | https://doi.org/10.1073/pnas.80.9.2799 |
| **Date added** | 2026-04-20 |
| **Categories** | [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0018_literature_survey_synaptic_integration`](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Full summary** | [`summary.md`](../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1073_pnas.80.9.2799/summary.md) |

C Koch and colleagues (1983) published "Nonlinear interactions in a dendritic tree:
localization, timing, and role in information processing." in Proceedings of the National
Academy of Sciences. The paper is included in this task's survey because it contributes to the
"Shunting inhibition" theme of synaptic-integration priors relevant to the direction-selective
retinal ganglion cell (DSGC) compartmental model.

The methodology and key findings of the paper are stated verbatim in the `## Abstract` section
above. This summary asset deliberately does not paraphrase or extend those claims beyond what
CrossRef returns; any quantitative prior used from this paper in the DSGC model-fitting
pipeline must be read directly from the published figures and tables.

The paper's primary significance for this project is its contribution to the "Shunting
inhibition" evidence pool. The answer asset
`assets/answer/synaptic-integration-priors-for-dsgc-modelling/` records which DSGC model prior
(rise/decay time constant, attenuation factor, E-I lag, asymmetry ratio, or
shunting-inhibition location dependence) this paper supplies, together with the numerical
value when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

</details>

<details>
<summary>📖 <strong>Retinal ganglion cells: a functional interpretation of dendritic
morphology</strong> — Koch et al., 1982</summary>

| Field | Value |
|---|---|
| **ID** | `10.1098_rstb.1982.0084` |
| **Authors** | Christof Koch, Tomaso Poggio, Vincent Torre |
| **Venue** | Philosophical Transactions of the Royal Society B (journal) |
| **DOI** | `10.1098/rstb.1982.0084` |
| **URL** | https://royalsocietypublishing.org/doi/10.1098/rstb.1982.0084 |
| **Date added** | 2026-04-20 |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`retinal-ganglion-cells`](../../meta/categories/retinal-ganglion-cells/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1098_rstb.1982.0084/summary.md) |

Koch, Poggio & Torre's 1982 paper is arguably the most influential theoretical paper on
retinal ganglion cell biophysics ever published, and is the direct intellectual ancestor of
the DSGC modelling work this project undertakes. Using passive cable theory applied to
histologically reconstructed cat RGC morphologies, the authors compute electrotonic properties
of each RGC class and show that none are truly isopotential despite their small physical
sizes.

The paper's central theoretical contribution is the "on-the-path" shunting-inhibition
mechanism for direction selectivity. A shunting inhibitory synapse (reversal potential near
rest, acting as a conductance gate) placed between an excitatory synapse and the soma
implements an approximately multiplicative veto of the excitation. If the inhibitory input is
activated only by null-direction motion (via a delay or asymmetric synaptic wiring), the
asymmetric activation of preferred vs. null motion produces strongly direction-selective
somatic responses even in a purely passive neuron.

The biophysical predictions are quantitative: the paper reports direction-selectivity indices
exceeding 0.5 for physiologically reasonable synaptic conductance magnitudes, matching the
values measured in cat RGCs. The effect depends critically on the relative positions of the
excitatory and inhibitory synapses along the dendrite, which is a concrete, testable
prediction for modern morphologically detailed DSGC models.

For this project, the paper is essential context in three ways. First, it establishes the
"on-the-path" shunting paradigm that all modern DSGC circuit-level models (Vaney, Taylor,
Euler, Borg-Graham, and their successors) rely on. Second, it shows that the passive
cable-theoretic machinery of Rall is sufficient to generate nontrivial retinal computations,
which means our passive baseline compartment models should already be able to produce
meaningful DS indices before adding active conductances. Third, it defines the electrotonic
compactness question concretely: our NEURON models should measure dendritic L values and
compare them against the paper's 0.5-0.8 lambda range for alpha RGCs to validate
passive-parameter choices.

</details>

<details>
<summary>📖 <strong>Distinguishing theoretical synaptic potentials computed for
different soma-dendritic distributions of synaptic input</strong> — Rall,
1967</summary>

| Field | Value |
|---|---|
| **ID** | `10.1152_jn.1967.30.5.1138` |
| **Authors** | Wilfrid Rall |
| **Venue** | Journal of Neurophysiology (journal) |
| **DOI** | `10.1152/jn.1967.30.5.1138` |
| **URL** | https://journals.physiology.org/doi/10.1152/jn.1967.30.5.1138 |
| **Date added** | 2026-04-20 |
| **Categories** | [`cable-theory`](../../meta/categories/cable-theory/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1152_jn.1967.30.5.1138/summary.md) |

Rall's 1967 paper asks whether the shape of a somatic EPSP carries information about where
along the dendritic tree the underlying synaptic input was delivered. Using the
equivalent-cylinder formalism and closed-form solutions of the passive cable equation, Rall
computes theoretical EPSP waveforms for inputs at a range of electrotonic distances from the
soma.

The paper's methodological contribution is the shape-index plot: a two-dimensional graph of
EPSP rise time versus half-width in which different input locations trace out distinguishable
curves. Somatic inputs produce fast, narrow EPSPs; distal dendritic inputs produce slower,
broader EPSPs whose temporal profile is dominated by cable low-pass filtering.

The main result is that input location is recoverable from EPSP shape with useful accuracy,
provided the underlying neuron approximately satisfies the equivalent-cylinder assumptions.
Rall also reports the expected dramatic attenuation of distal-input amplitude at the soma, and
discusses the interplay between membrane time constant and cable filtering in shaping the
observed waveform.

For the direction-selective retinal ganglion cell (DSGC) modelling work in this project, the
paper is relevant in three ways. First, it establishes that somatically-recorded EPSPs from
DSGC patch experiments can in principle be used to estimate input location, informing how we
interpret experimental data. Second, it defines a standard validation target (shape-index
curves) that our reduced compartment models should reproduce. Third, it warns that the
equivalent-cylinder simplification depends on branching-rule assumptions that real dendritic
arbors — including the starburst amacrine and DSGC arbors we care about — do not satisfy
exactly, motivating the use of full morphological compartmental simulation in NEURON rather
than reduced analytical models.

</details>

## Tasks (11)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |
| 0010 | [Hunt DSGC compartmental models missed by prior survey; port runnable ones](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) | completed | 2026-04-20 14:42 |
| 0013 | [Resolve dsgc-baseline-morphology source-paper provenance](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) | completed | 2026-04-20 17:21 |
| 0015 | [Literature survey: cable theory and dendritic filtering](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) | completed | 2026-04-20 10:00 |
| 0016 | [Literature survey: dendritic computation beyond DSGCs](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) | completed | 2026-04-20 10:36 |
| 0018 | [Literature survey: synaptic integration in RGC-adjacent systems](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) | completed | 2026-04-20 12:15 |
| 0019 | [Literature survey: voltage-gated channels in retinal ganglion cells](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) | completed | 2026-04-20 13:00 |
| 0027 | [Literature survey: modeling effect of cell morphology on direction selectivity](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) | completed | 2026-04-21 22:23 |
| 0078 | [Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) | completed | 2026-05-04 16:25 |
| 0080 | [Bed B v3 MOBO with dendritic-spike machinery and NSGA-II](../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) | completed | 2026-05-04 22:45 |
| 0097 | [Literature survey: multi-objective optimisation of single-neuron models](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) | completed | 2026-05-08 16:50 |

## Answers (9)

<details>
<summary><strong>Which objective functions have been used in published
multi-objective optimisation of single-neuron compartmental models, and
what is each one's formula, units, and NEURON-side computational recipe
on a t0091-style 8-direction trial output?</strong></summary>

**Confidence**: high | **Date**: 2026-05-08 | **Full answer**:
[`objective-functions-for-single-neuron-multi-objective-optimisation`](../../tasks/t0097_multi_obj_optim/assets/answer/objective-functions-for-single-neuron-multi-objective-optimisation/)

The published multi-objective single-neuron optimisation literature converges on four
canonical biological objective categories that fit directly on top of the project's existing
pymoo NSGA-II loop: stimulus-spike-train mutual information via the direct method with 1/T
extrapolation, ATP-per-spike via per-compartment integration of Na+ inward current divided by
three (the Na+/K+ ATPase stoichiometry), cytoplasm volume as the sum of pi*r^2*L over
compartments (novel as an explicit MOO target on a single neuron), and Marder-style robustness
as the standard deviation of DSI under +/-10% perturbation of all channel densities. Each
catalogued objective is implemented as one pymoo evaluator callable on the project's existing
8-direction 1400-ms trial output and is reported with a uniform 8-field record (name, LaTeX
formula, units, NEURON-side quantities, recipe, biological-plausibility note,
direction-of-optimisation, supporting paper citations). The methodology synthesis adopts
per-feature SD-normalisation, the 2-3 SD acceptance threshold and ensemble-as-experiment
reporting pattern, and the optimiser-selection rule NSGA-II for high-d 2-3-objective problems,
NSGA-III for high-d many-objective problems, and qLogNEHVI for low-d constrained problems with
population fewer than 20 evaluations. Two additional well-defined objectives surfaced by the
survey are also catalogued with the full 8-field record: coincidence-detection accuracy (the
closest published function-vs-energy MOO analogue to the project's planned DSI-vs-energy work)
and bits-per-ATP efficiency (the canonical empirical Pareto curve in the field). This answer
is grounded in 21 newly catalogued papers plus 9 corpus papers and the BluePyOpt / eFEL /
pymoo / AllenSDK documentation.

</details>

<details>
<summary><strong>When the t0086 13-cell pool of 6 Genuine + 7 Marginal cells is
re-clustered in the t0080 54-d v3 parameter space and a t0084-style
Vm-trace deep-dive is run at 16 directions on per-cluster representative
cells, are the resulting clusters mechanistically distinct (different
dominant channel mechanisms across clusters) or do they share the same
mechanism with parameter-scale variation?</strong></summary>

**Confidence**: medium | **Date**: 2026-05-06 | **Full answer**:
[`are-cluster-motifs-mechanistically-distinct`](../../tasks/t0088_recluster_marginals_and_vm_motifs/assets/answer/are-cluster-motifs-mechanistically-distinct/)

No -- the clusters are not mechanistically distinct. The 13-cell re-cluster produces 4
clusters (best_k = 4 by silhouette) and all 4 cluster representatives are NaP-dominant in
PD-minus-ND attribution at 16 directions (frac NaP 0.874-0.997, frac Nav1.6 0.003-0.126, frac
NMDA = 0.000). The verdict is `shared_mechanism_different_scale`: clusters differ in 54-d
parameter scale but not in which channel drives the PD response. This extends t0084's
NaP-dominant cell 767 finding to the wider 13-cell pool of joint-pass / near-joint-pass cells
in the v3 substrate.

Per-cluster fractional channel attribution table (PD = 0 deg, ND = 180 deg, response window
[200, 1200] ms):

| Cluster | Rep cell | NMDA frac | Nav1.6 frac | NaP frac | Dominant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1604 | 0.000 | 0.012 | 0.988 | nap |
| 1 | 1634 | 0.000 | 0.126 | 0.874 | nap |
| 2 | 767 | 0.000 | 0.125 | 0.875 | nap |
| 3 | 1639 | 0.000 | 0.003 | 0.997 | nap |

</details>

<details>
<summary><strong>Which biophysical mechanism - NMDA Mg-block, distal Nav1.6, NaP, or
a combination - is responsible for cell 767's joint-pass DSI improvement
in the v3 Bed B substrate?</strong></summary>

**Confidence**: medium | **Date**: 2026-05-05 | **Full answer**:
[`cell-767-dendritic-spike-mechanism-attribution`](../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/assets/answer/cell-767-dendritic-spike-mechanism-attribution/)

Cell 767's PD/ND difference in integrated dendritic current is attributed primarily to **NaP
sustained depolarisation** (0.0% NMDA, 7.0% Nav1.6, 93.0% NaP) over the response window [200,
1200] ms. Cells 637 and 762 show the same NaP-dominant signature (98.5% and 99.9%), suggesting
NaP is a systematic feature of the v3 Pareto near-pass cluster rather than idiosyncratic to
cell 767. This single-replicate deep-dive did not reproduce cell 767's original 5-seed
joint-pass DSI of 0.494 (re-evaluated DSI = 0.000), so the attribution describes the
underlying biophysical signature of these parameters rather than confirming a per-trial
joint-pass mechanism; multi-replicate confirmation requires t0083 or a follow-up multi-seed
study.

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

## Suggestions (69 open, 17 closed)

<details>
<summary>🧪 <strong>Targeted morphology sweep around the high-DSI region of the
seed-55 Pareto front</strong> (S-0104-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-14 | **Source**:
[t0104_nsga2_2obj_dsi_pdrate_3seeds](../../tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/)

Hold the seed-55 best-DSI cell's 54-d electrophys subvector fixed and sweep the 14-d
morphology subvector across a Latin-Hypercube sample of ~200 cells, all evaluated at
N_EVAL_SEEDS = 4 with the DSI guard active. The question: does the high-DSI cell's electrophys
signature generalise across morphologies, or is the DSI = 0.54 reading specific to one
parametric tree topology? If DSI stays above 0.4 across most morphologies, the electrophys
subvector is the lever and morphology is secondary; if DSI collapses, the seed-55 cell is a
morphology-specific lucky draw. Recommended task types: experiment-run, comparative-analysis.
Cost: ~$2-3 (200 cells x N=4, no GA overhead, single Vast.ai instance for ~6 hours).

</details>

<details>
<summary>📚 <strong>Promote the t0098 morphology renderer (with t0100 vector_68d[54:]
slice fix) into a reusable library asset</strong> (S-0105-03)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-05-13 | **Source**:
[t0105_preliminary_figures_report](../../tasks/t0105_preliminary_figures_report/)

Figure 7 in t0105 had to copy the morphology renderer code from
tasks/t0098_visualise_pareto_morphologies/code/build_charts.py into
tasks/t0105_preliminary_figures_report/code/render_pareto_top5.py with the vector_68d[54:]
morphology-slice fix from t0100 patched in manually. The t0104 follow-up panel (S-0105-01),
and any future optimisation-result report task, will need the same renderer. Package this
renderer as a top-level library asset (e.g., dsgc_morphology_renderer) under a host task --
expose a clean Python API (render_morphology(vector_68d, ax) plus a multi-cell grid helper),
include the t0100 slice fix as the default behaviour, register a details.json under
assets/library/, and document import path tasks.<host_task>.code.dsgc_morphology_renderer.
Downstream tasks then import instead of copying. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Calcium-clearance perturbation sweep on the 27 silenced-cell
DSI=1.0 vectors to test silence-as-mechanism hypothesis</strong>
(S-0102-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-12 | **Source**:
[t0102_seedscale_n4_gen20](../../tasks/t0102_seedscale_n4_gen20/)

creative_analysis.md Section 7 proposes a mechanistic reading: the 27 t0102 cells with DSI >=
0.99 / PD < 0.1 are not bugs but the GA's discovery of a lateral-inhibition silencing regime
(slow Ca clearance, strong sAHP, weak ACh drive) consistent with Poleg-Polsky 2026 SAC gating.
Take each of the 27 cells, fix the 68-d vector except CAD_TAUR_MS (Ca clearance tau, dim 38),
sweep that dim from ~65 ms down to 5 ms in 10 logarithmic steps, re-evaluate DSI/PD/rob at
N_EVAL_SEEDS=8. Question: when Ca clearance is restored, do these cells collapse to the
high-PD low-DSI corner (silence was the only DSI mechanism), or do some land in the joint
corner (Ca clearance is the active constraint and the rest of the vector is joint-viable)?
Outcome: 27 x 10 grid mapping silence-to-joint escape paths. Doubles as slice-physiology
prediction (BAPTA Ca chelation should disinhibit SAC/DSGC firing). Recommended task types:
experiment-run, data-analysis. Cost: < $0.50 (270 evaluations, no GA).

</details>

<details>
<summary>📂 <strong>Download Ran et al. 2020 ON-OFF DS-cell morphologies as a
complementary morphology source</strong> (S-0103-02)</summary>

**Kind**: dataset | **Priority**: high | **Date**: 2026-05-12 | **Source**:
[t0103_extract_baden_2016_ds_morphologies](../../tasks/t0103_extract_baden_2016_ds_morphologies/)

Ran et al. 2020 (Nat Commun) provides dye-fill reconstructions of mouse ON-OFF DS RGCs with
co-recorded preferred-direction labels. The Baden 2016 Dryad release does not include
morphologies, and Ran 2020 covers exactly the ON-OFF DS subtypes (Baden clusters G12/G13) most
relevant to the t0024 ON-OFF DSGC modelling line. Download the published SWC files (or extract
from supplementary materials), register them as a dataset asset, and tag each morphology with
its preferred-direction angle and any Baden-cluster correspondence available. Useful as a
second, independent morphology source against Bae 2018 for the t0090 envelope grounding.
Recommended task types: download-dataset, download-paper.

</details>

<details>
<summary>🧪 <strong>Ground t0090 morphology-generator parameter envelopes in the
Baden 2016 + Bae/Ran morphologies</strong> (S-0103-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-12 | **Source**:
[t0103_extract_baden_2016_ds_morphologies](../../tasks/t0103_extract_baden_2016_ds_morphologies/)

t0090's morphology generator currently samples field diameter, branch count, total length, and
asymmetry from hand-picked ranges around the t0024 canonical De Rosenroll cell. The t0103
Baden subset (RF diameter, DSI, OSI per cell across 1,238 DS cells) plus the morphologies that
the Bae 2018 / Ran 2020 follow-ups would deliver give us per-cluster biological envelopes for
each shape statistic. Run a re-calibration task that fits empirical per-cluster distributions
(mean +/- SD per Baden DS group) and replaces t0090's parametric ranges, then re-runs a small
NSGA-II validation to confirm the bio-grounded envelopes still admit the Pareto-front cells.
This is the original motivation for downloading Baden 2016 in the first place. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary>🔧 <strong>Recover per-cell IPL stratification depth profiles from Baden
2016 scan-level structural data</strong> (S-0103-07)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-05-12 | **Source**:
[t0103_extract_baden_2016_ds_morphologies](../../tasks/t0103_extract_baden_2016_ds_morphologies/)

The Baden 2016 Dryad release exposes a scan-level structural volume and per-scan ROI metadata,
but no per-cell IPL stratification profile (paper Fig. 2 IPL profiles are derived per-group,
not per-cell). t0103 substituted per-group mean RF diameter as the secondary statistic. A
follow-up task can re-project per-cell ROIs onto the scan-level IPL volume to reconstruct an
approximate per-cell stratification depth profile, validating against the paper's per-group
means as ground truth. This would unlock per-cell IPL depth as a feature for downstream
modelling tasks (e.g. matching modelled dendritic terminations to biological IPL bands).
Recommended task types: data-analysis, feature-engineering.

</details>

<details>
<summary>📊 <strong>Correct fabricated content in Poleg-Polsky 2026 summary.md via
the corrections mechanism</strong> (S-0101-01)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-11 | **Source**:
[t0101_brainstorm_results_21](../../tasks/t0101_brainstorm_results_21/)

tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md has
claims absent from the paper: (a) wrong title (published 'supporting elementary motion
detection'); (b) wrong primitives ('NMDA multiplicative gating', 'velocity-dependent
coincidence detection', 'distance-graded delay lines'); (c) wrong search axes ('A-type
potassium density'); (d) wrong scope (paper covers retina + cortex L2/3). Actual 8 primitives:
H&R, anti-H&R, amplitude, temporal-alignment, B&L, anti-B&L, pause-in-inhibition,
directionally-tuned inhibition. Real DSI 2.4-73.1% from subthreshold voltage. Downstream task
writes corrections/paper_summary_10.1038_s41467-026-70288-4.json with PDF-verified content
(quotes in t0101 session_log). Cost $0.

</details>

<details>
<summary>📊 <strong>Per-cell field_elongation_pd vs DSI test on the 57-cell t0091
Pareto to resolve HM-3 inconclusive</strong> (S-0091-01)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-08 | **Source**:
[t0091_morphology_extended_nsga2_v1](../../tasks/t0091_morphology_extended_nsga2_v1/)

t0091 reported a Spearman rho=-0.07 between total dendritic length and DSI vector-sum across
the 57-cell Pareto, leaving HM-3 (length-vs-DSI scaling, Hausselt2007) inconclusive because
total length conflates field_elongation_pd with branch_density_gradient_pd and
num_primary_branches. Pure data-analysis task on existing pareto_front.json: extract
field_elongation_pd from each Pareto cell's 14-d morph_params vector, compute Spearman +
Kendall correlations against DSI, PD-rate, robustness, and the 9 channel-side priors, plot
per-anchor scatter overlays, and stratify by anchor lineage. Goal: definitively confirm or
refute that elongation along PD is the morphology axis driving DSI in joint optimisation,
separate from branch density. Cost: $0 (local CPU analysis on existing JSONL files).
Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Continue t0091 NSGA-II for 6 more generations (gen 3-8) to test
whether HV plateau or biological-plausibility shifts</strong> (S-0091-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-08 | **Source**:
[t0091_morphology_extended_nsga2_v1](../../tasks/t0091_morphology_extended_nsga2_v1/)

t0091 stopped at gen 2 of 8 when REQ-10 (>=8-cell Pareto) was satisfied 7x over (57 cells);
cost watchdog never fired ($0.65 of $4.00 cap). The HV trajectory was still climbing at +68
percent per generation (14.07 to 23.71) and plateau detection requires >=4 generations of
history before it can fire. Run pop=96 x 6 more generations on a single Vast.ai EPYC 7B13
64-core resume from t0091's gen-2 final population (snapshot the population from
results/data/all_evaluations.json). Tests three open questions: (a) does HV plateau before gen
8? (b) does any gen 3+ cell pass biological plausibility, or is universal channel-side
violation robust to generation depth? (c) does the PD vs ND anchor count shift toward
significance with more generations? Cost estimate: ~$1.80 (6 gens x ~12 min/gen wall-clock x
60 parallel workers x $0.23/hr); fits remaining $3.80 project buffer. Recommended task types:
experiment-run, data-analysis.

</details>

<details>
<summary>📊 <strong>alt_topology basin deep-dive: identify morphology features
distinguishing alt_topology vs bedb_like Pareto cells</strong> (S-0091-04)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-08 | **Source**:
[t0091_morphology_extended_nsga2_v1](../../tasks/t0091_morphology_extended_nsga2_v1/)

16 alt_topology cells survived in the 57-cell Pareto (parity with bedb_like's 20), and the
only strict joint-pass cell (DSI 0.51, PD 35 Hz, robust 0.79) is nearest to alt_topology in
14-d morphology space. creative_thinking.md flags this as evidence for at least two distinct
morphological basins of joint-pass-adjacency, but the 14-d signature distinguishing
alt_topology from bedb_like has not been quantified. Pure data analysis on pareto_front.json +
warm_start_population.json: PCA + UMAP on the 14-d morph vectors restricted to Pareto cells
colour-coded by anchor; per-feature Mann-Whitney U tests on each of the 14 knobs; identify the
top 3-5 discriminative features (likely num_primary_branches, max_strahler_depth,
mean_branching_angle); cross-reference with biological scorecard rows. Cost: $0. Recommended
task types: data-analysis.

</details>

<details>
<summary>🔧 <strong>Reformulate NSGA-II with biological priors as additional
objectives or hard constraints</strong> (S-0091-05)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-05-08 | **Source**:
[t0091_morphology_extended_nsga2_v1](../../tasks/t0091_morphology_extended_nsga2_v1/)

t0091 used 3-objective NSGA-II minimising (-DSI, -PD-rate, -robustness) with biological priors
applied as a post-hoc filter (0/57 Pareto cells pass). The optimiser drifts to the upper rail
of NMDA / NaP / GABA bounds without paying any cost. Reformulate as either (a) 4+ objective
NSGA-II adding worst-case prior-violation sigma as a fourth objective, or (b) hard-constrained
NSGA-II using pymoo's constraint handling with each prior as a g(x) <= 0 inequality. Hay 2011
is direct precedent for (a). Run a small-scale pass (pop=64, 4 gens, ~$1.00) on the t0091
substrate and compare the reformulated Pareto's biological-plausibility distribution against
t0091's post-hoc-filter Pareto. If the reformulated Pareto includes any biologically-plausible
joint-pass cells, the 'morphology cannot rescue priors' verdict was driven by formulation, not
substrate. Cost ~$1.00 on Vast.ai EPYC 7B13. Recommended task types: experiment-run,
build-model.

</details>

<details>
<summary>📂 <strong>Real-cell DSGC morphology library from NeuroMorpho: test whether
observed morphologies escape prior-violation ceiling</strong> (S-0091-06)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-05-08 | **Source**:
[t0091_morphology_extended_nsga2_v1](../../tasks/t0091_morphology_extended_nsga2_v1/)

t0091 confirmed HM-1 (morphology asymmetry necessary; symmetric anchor count = 0) but refuted
HM-2 (PD vs ND direction blind, p=0.331). The procedural 14-knob generator covers a parametric
box that biological DSGCs may or may not occupy; t0091's 57-cell Pareto stays inside that box
but cannot escape the channel-side prior-violation ceiling. Brainstorm 18 'Option G' is the
next move: build a NeuroMorpho.org-anchored real DSGC cell library (10-20 mouse / rabbit
reconstructions from Briggman 2011, Wei 2011, Morrie & Feller 2018), implement a categorical
selector + parametric deformation knobs (diameter scaling, branch pruning, soma offset), then
re-run t0091's NSGA-II with the real-cell library replacing the procedural generator. Tests
whether observed DSGC morphologies escape the prior-violation ceiling that procedural ones
cannot. Larger task: needs planning first. Cost ~$2-3 for the optimisation pass. Recommended
task types: download-dataset, build-model, write-library.

</details>

<details>
<summary>📊 <strong>Pareto-cell PCA + feature-importance analysis on the 14-d morph
vectors to rank Pareto-inclusion drivers</strong> (S-0091-07)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-08 | **Source**:
[t0091_morphology_extended_nsga2_v1](../../tasks/t0091_morphology_extended_nsga2_v1/)

t0091 reports anchor-level Pareto counts (bedb_like 20, symmetric 0, pd_asymmetric 12,
nd_asymmetric 9, alt_topology 16) but does not report which of the 14 morphology knobs
individually drive Pareto inclusion. Pure data-analysis on results/data/pareto_front.json +
all_evaluations.json: train a logistic regression / random forest classifier with the 14-d
morph vector as input and is_in_pareto as binary label, using the 187 evaluations as the
training set; report per-feature coefficients / SHAP values; cross-validate via
leave-one-anchor-out splits; visualise via per-feature partial dependence plots. Goal: rank
the 14 knobs by their causal importance for joint Pareto inclusion, beyond the anchor-level
aggregation. This complements S-0091-01 (which is single-feature Spearman) and S-0091-04
(which is alt-topology vs bedb-like comparison) with an exhaustive feature-importance audit.
Cost: $0 (local CPU). Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Investigate the 4 PD-rate=0 cells: do morphology variants shift
direction-tuning peak away from 0 deg?</strong> (S-0093-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-08 | **Source**:
[t0093_resweep_and_t0090_correction](../../tasks/t0093_resweep_and_t0090_correction/)

4/60 post-fix cells (different/morph_18, _25, _29, similar/morph_17) fire spikes only at
non-PD directions (e.g. morph_18: 0 spikes at 0 deg, 1 each at 45/90/135/180 deg, DSI=-1.0).
t0083 channels were calibrated on the BedB hand-coded morphology, so it is unknown whether
morphology variants intrinsically shift the direction-tuning peak. Re-run those 4 morphologies
at fine angular resolution (every 15 deg) under the t0083 best-cell vector, plus 5 cells
nearest the BedB symmetric anchor as control, and fit the angular position of the firing-rate
peak per cell. Output: `peak_direction_per_morph.json` mapping morph_id -> peak_direction_deg,
plus a polar-tuning-curve panel. If peaks shift systematically with asymmetry knobs, this
resolves t0091's design question of whether per-cell PD must be re-discovered after morphology
changes. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Bed B NSGA-II maximising DSI and minimising cytoplasm
volume</strong> (S-0097-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-08 | **Source**:
[t0097_multi_obj_optim](../../tasks/t0097_multi_obj_optim/)

Highest biological-plausibility ranking in the t0097 catalogue. Cytoplasm volume is the most
evolutionarily grounded cost objective (Cajal cytoplasm-conservation; Cuntz et al. 2010's `bf`
in [0.2, 0.7] band; Chklovskii et al. 2002's 3/5-of-grey-matter wiring rule). Infrastructure
already in place via the t0093-validated procedural morphology generator. Falsifiable
prediction: high-DSI corner clusters at `bf` in [0.2, 0.7]. Budget feasibility: 12-24 h on
Vast.ai EPYC 7763 64-core at $0.30/h, total $4-8 (within the per-task $5 default; flag for $8
budget bump if needed). Same population/generation budget as t0091.

</details>

<details>
<summary>🧪 <strong>Extend NSGA-II from t0083's gen-17 to gen 25 with 1.5x larger
population (144) and parameter-clustering analysis</strong> (S-0083-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-06 | **Source**:
[t0083_bedb_v3_extend_nsga2_gen8plus](../../tasks/t0083_bedb_v3_extend_nsga2_gen8plus/)

t0083 terminated at gen 17 on the MaxGenerationTermination(10) hard cap with HV still growing
strongly (gen 16 -> 17: +3.1%, gen 15 -> 16: +49%). The HV-plateau watchdog never fired,
indicating the search had not converged. Run NSGA-II from t0083's gen-17 final population for
an additional 8 generations at population 144 (vs t0083's 96) to test (a) whether the high-PD
joint-pass region (cells 1559, 1677) continues to expand, (b) whether new high-DSI joint-pass
cells appear above 0.77 (cell 1304's headline DSI), and (c) whether the 18-cell Pareto front
grows or saturates. Expected cost: ~$8-12 USD on Vast.ai EPYC 7B13 (8 gens x 144 cells x 64 s
= 20.5 h x $0.40/hr); requires the cost watchdog parameterisation fix from S-0083-04.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Per-direction Vm-trace deep-dive of cell 1304 to identify the
headline cell's biophysical mechanism</strong> (S-0083-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-06 | **Source**:
[t0083_bedb_v3_extend_nsga2_gen8plus](../../tasks/t0083_bedb_v3_extend_nsga2_gen8plus/)

Cell 1304 (gen 13, DSI 0.7652 / PD 13.96 Hz) is the project's first cell statistically
indistinguishable from RivlinEtzion 2012's published mouse ON-OFF DSGC stable-cell
distribution (DSI z=-0.08, PD z=+0.42). Its biophysical mechanism has not been attributed to
specific dendritic-spike machinery (NMDA Mg-block vs distal Nav1.6 vs NaP_dend). t0084 found
NaP_dend dominant for cell 767 (now dominated and off-Pareto); cell 1304's parameter vector
differs structurally from cell 767's (cf. [0.006, 0.001, 0.999, 0.995, 0.876, 0.992] vs
[0.008, 0.018, 1.000, 1.000, 0.250, 0.000]). Re-run cell 1304 in subprocess with per-direction
Vm recording at soma + 4 dendritic locations + AIS, then run conductance-knockout ablations
(zero out g_NaP_dend / g_NMDA / g_Nav_dend_distal) to identify the dominant DSI driver.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Tighten NSGA-II priors on gnmda_dend to match Sivyer 2013
per-synapse value, then re-run</strong> (S-0086-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-06 | **Source**:
[t0086_robustness_cluster_bio_comparison](../../tasks/t0086_robustness_cluster_bio_comparison/)

t0086's biological scorecard found that both Genuine-cell clusters have NMDA per-synapse
conductance 85-122 sigma above Sivyer 2013's published 0.1 nS. The NSGA-II search routinely
pushes gnmda_dend to the upper boundary of its log-uniform [1e-5, 1e-2] uS range. Tighten the
parameter bounds to [1e-5, 5e-4] uS (5x Sivyer 2013's value as a soft cap) and re-run NSGA-II
from t0083's gen-17 final population for 5 additional generations at population 96. Test
whether any joint-pass cells emerge in the biologically-plausible NMDA regime. If not, this
confirms that the v3 substrate cannot satisfy the joint-pass DSI/PD criterion using
biologically-plausible NMDA -- a major finding that would motivate either (a) revisiting the
joint-pass thresholds, (b) revisiting the substrate's NMDA implementation, or (c) revisiting
Sivyer 2013's measurement scope. Expected cost: ~$1.50 USD on Vast.ai EPYC 7B13 (5 gens x 96
cells x 30 s = 4 h x $0.35/hr). Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Resolve units mismatch between t0080 gnmda_dend NetCon weight and
Sivyer 2013 per-spine conductance</strong> (S-0086-02)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-06 | **Source**:
[t0086_robustness_cluster_bio_comparison](../../tasks/t0086_robustness_cluster_bio_comparison/)

t0086's NMDA exotic verdict (>85 sigma above Sivyer 2013) is so extreme that it likely
partially reflects a units / scope mismatch rather than a genuinely outlier biological
mechanism. The t0080 ParameterVector encoding `gnmda_dend` is the NetCon weight used in the
t0080 Exp2NMDA mechanism, while Sivyer 2013's value is a per-spine synaptic conductance
measured in voltage-clamp on RGC dendritic spines. These may differ by a per-cell area
normalisation or by an effective open-channel-fraction factor. Run a calibration ablation:
take a single t0080 cell, vary `gnmda_dend` from 1e-5 to 1e-2 uS, measure the per-spine
effective open conductance (from the NEURON state during a stimulus), and produce a
calibration curve mapping NetCon weight to per-spine conductance. Then re-score the t0086
clusters against Sivyer 2013 in the corrected units. Expected cost: ~$0.30 USD (1 hour CPU).
Recommended task types: data-analysis.

</details>

<details>
<summary>📊 <strong>Source RGC-specific NaP density measurement to replace Stuart
1999 / Goldfinger 2000 cortical-pyramidal prior</strong> (S-0086-05)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-05-06 | **Source**:
[t0086_robustness_cluster_bio_comparison](../../tasks/t0086_robustness_cluster_bio_comparison/)

t0086's biological scorecard used Stuart 1999 / Goldfinger 2000 NaP density (0.0005 S/cm^2) as
the prior for distal NaP, but those measurements were made in cortical pyramidal cells, not
RGCs. Both Genuine clusters scored exotic on NaP (Cluster 0 +24 sigma, Cluster 1 +7 sigma) by
this prior. Conduct a focused literature search for RGC-specific NaP density measurements (try
Hu 2009, Bender-Trussell 2009, Lewis 2014 RGC review). If an RGC-specific NaP value exists,
replace the prior, re-run the scorecard, and re-classify the clusters. Expected cost: ~$0.10
USD (paper search + summarisation only). Recommended task types: review-papers.

</details>

<details>
<summary>🧪 <strong>Bed A cross-bed validation: re-run NSGA-II on the t0080 Bed A
morphology with the same v3 substrate</strong> (S-0086-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-06 | **Source**:
[t0086_robustness_cluster_bio_comparison](../../tasks/t0086_robustness_cluster_bio_comparison/)

t0086 identified 6 Genuine cells in t0080's Bed B morphology, but the v3 substrate has not
been tested on Bed A. Run NSGA-II for 8 generations at population 96 on Bed A with the same v3
substrate and the same constraint (AIS-to-soma Nav ratio >= 5). Compare: (a) does Bed A
produce more or fewer joint-pass cells than Bed B? (b) do the Bed A joint-pass cells cluster
into the same 2 phenotypes (high-NMDA + high-NaP vs high-NMDA + extended-GABA) or do they
discover a third? (c) does Bed A allow biologically-plausible NMDA solutions where Bed B does
not? Expected cost: ~$2.50 USD on Vast.ai EPYC 7B13 (8 gens x 96 cells x 60 s = 13 h x
$0.35/hr). Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Causal NaP-knockout ablation per cluster representative</strong>
(S-0088-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-06 | **Source**:
[t0088_recluster_marginals_and_vm_motifs](../../tasks/t0088_recluster_marginals_and_vm_motifs/)

t0088 attributed PD-minus-ND fractional contributions correlationally (NMDA 0%, Nav1.6
0.3-12.6%, NaP 87.4-99.7% across the 4 cluster representatives). The attribution is
correlation-based; to causally confirm NaP as the dominant mechanism, set nap_dend_distal = 0
in each of the 4 representative cells (1604, 1634, 767, 1639) and re-measure DSI at the 16
directions used by t0088. Expected effect: DSI collapses to <0.2 in all 4 cells if NaP is
causally responsible; DSI partially preserved if NMDA + Nav1.6 + GABA also contribute. Compare
to baseline DSI_measured (cell 1604: 0.71; cell 1634: 0.20; cell 767: 0.60; cell 1639: 0.43).
Local-CPU only: 4 cells x 16 directions x ~60 s/sim = ~64 min wall-clock, $0 cost. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>13-cell full deep-dive (extend Phase B to all 13 cells, not just
representatives)</strong> (S-0088-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-06 | **Source**:
[t0088_recluster_marginals_and_vm_motifs](../../tasks/t0088_recluster_marginals_and_vm_motifs/)

t0088 Phase B ran the Vm-trace deep-dive on 4 representative cells; the 13-cell pool's other 9
cells could have within-cluster mechanism heterogeneity invisible to the representative-only
analysis. Extend Phase B to all 13 cells: 13 x 16 directions = 208 NEURON sims. Compare
per-cell fractional NaP / Nav1.6 / NMDA across all cells within each cluster; report
within-cluster spread as a measure of mechanism homogeneity per cluster. Local-CPU only: 13 x
16 x ~60 s/sim = ~3.5 hours wall-clock, $0 cost. Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary>📊 <strong>Polar attribution decomposition: integrate fractional
contributions over the direction-tuning curve</strong> (S-0088-04)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-06 | **Source**:
[t0088_recluster_marginals_and_vm_motifs](../../tasks/t0088_recluster_marginals_and_vm_motifs/)

t0088's mechanism attribution uses only PD (0 deg) - ND (180 deg) integrated current. This
discards information from the 14 other directions recorded at 22.5-deg spacing. Compute
per-direction fractional NMDA / Nav1.6 / NaP integrals and weight by the direction-tuning
curve (the AIS spike-onset polar histogram) to get a richer cross-direction attribution. Test
whether the NaP-dominant verdict holds across all directions or only at PD-flanking
directions. Pure data analysis on existing .npz files; ~1 hour wall-clock, $0 cost.
Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Multi-replicate confirmation of the t0081 joint-pass result with
3-5 independent LHS + warm-start RNG seeds</strong> (S-0081-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-05 | **Source**:
[t0081_bedb_v3_warmstart_nsga2](../../tasks/t0081_bedb_v3_warmstart_nsga2/)

t0081's joint-pass cell 767 (DSI 0.494 / PD 11.39 Hz) is a single-replicate observation from
one NSGA-II chain with one Sobol/LHS seed (seed 43 for fresh LHS) and one warm-start RNG seed
(42 for the t0078 49-d to 54-d projection). Re-run the same pop=96 / gen=8 NSGA-II
configuration on the v3 substrate with 3-5 different seed pairs (e.g., (44,45), (46,47),
(48,49)) and report joint-pass rate, HV trajectory variance, and Pareto-front overlap across
replicates. Reuse the t0081 harness verbatim. Cost ~$5-10 across 3-5 replicates at $2.39 each.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Cross-bed validation: re-run warm-start NSGA-II on Bed A with
the v3 dendritic-spike additions</strong> (S-0081-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-05 | **Source**:
[t0081_bedb_v3_warmstart_nsga2](../../tasks/t0081_bedb_v3_warmstart_nsga2/)

t0081 confirms that v3 dendritic-spike machinery + warm-start NSGA-II yields joint-pass DSI/PD
on Bed B. Test whether the same architecture generalises to Bed A (the t0067-t0074 substrate,
modelDB 189347 lineage with bio-realistic AIS). Port the 5 v3 dendritic-spike dims
(`gnmda_dend`, `mg_conc_mm`, `voff_nmda`, `nav16_dend_distal`, `nap_dend_distal`) onto Bed A's
dendrites, warm-start from the closest-to-joint Bed A cells (e.g., t0074 / t0075 outputs), run
NSGA-II at pop=96 / gen=8 = 768 cells. Cost ~$3 (mirroring t0081). Recommended task types:
build-model, experiment-run.

</details>

<details>
<summary>🧪 <strong>NaP-density knockout sweep on cells 767 / 637 / 762 to test
causal necessity of NaP-dominant attribution</strong> (S-0084-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-05 | **Source**:
[t0084_t0081_cell_767_vm_trace_deepdive](../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/)

t0084 attributed cells 767/637/762 PD-vs-ND integrated dendritic current asymmetry to NaP
sustained depolarisation (93.0% / 98.5% / 99.9% fractional contributions) but the metric is
correlative. Test causality by sweeping `nap_dend_distal` from its measured value down through
0 in 5 logarithmic steps for each of the three cells while holding all other 53 parameters
fixed; re-evaluate per-direction spike counts and DSI. If joint-pass DSI collapses when
nap_dend_distal=0, NaP is causally necessary; if DSI is preserved, NaP is correlative only.
Reuse t0084's run_deepdive driver. ~45 runs locally on CPU. Cost ~$0. Recommended task types:
experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Per-seed mechanism decomposition of cell 767 across 5 t0081
evaluation seeds to find joint-pass-supporting seeds</strong> (S-0084-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-05 | **Source**:
[t0084_t0081_cell_767_vm_trace_deepdive](../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/)

t0084 ran cell 767 with a single seed (1000) and measured DSI = 0.000 vs t0081's 5-seed mean
of 0.494, indicating joint-pass depends on a subset of seeds. Re-run cell 767 across the 5
t0081 evaluation seeds (0-4), apply the same fractional-channel-contribution attribution per
seed, and report per-seed DSI plus per-seed NMDA / Nav1.6 / NaP contributions. Hypothesis:
high-DSI seeds will show non-zero NMDA contribution (Mg-unblocking gain on PD depolarisation);
low-DSI seeds will look like seed 1000. Local CPU; ~40 runs. Distinct from S-0081-01 which
varies LHS/warm-start RNG seeds at the NSGA-II population level; S-0084-02 fixes the parameter
vector and varies only per-seed evaluation noise. Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary>🧪 <strong>Multi-section NaP/Nav1.6 decomposition across all 177 terminal
dendrites of cell 767</strong> (S-0084-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-05 | **Source**:
[t0084_t0081_cell_767_vm_trace_deepdive](../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/)

t0084's attribution metric records Nav1.6 and NaP currents only at `cell.terminal_dends[0]`
(representative section). Test whether this is representative by extending recording to all
177 terminal dendrite sections of cell 767 and recomputing per-section fractional
contribution. If per-section spread is small (all > 80% NaP-dominant), single-section
attribution is robust; if some sections show NMDA-dominant or Nav1.6-dominant local
contributions, there is dendrite-tree spatial heterogeneity that the single-section metric
obscures, reframing t0084 from 'NaP-dominant cell-wide' to 'NaP-dominant on average with
possible NMDA hotspots'. Local CPU; runtime increase ~10 minutes. Cost ~$0. Recommended task
types: experiment-run, data-analysis.

</details>

<details>
<summary>📊 <strong>Channel-knockout DSI causal-attribution variant of the t0084
metric</strong> (S-0084-05)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-05 | **Source**:
[t0084_t0081_cell_767_vm_trace_deepdive](../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/)

t0084's fractional-channel-contribution metric is correlative: it measures which channel's
PD-vs-ND integrated current differs most in absolute magnitude, but does not establish causal
contribution to DSI. Replace it with a counterfactual knockout metric: for each cell, run 4
conditions (full / NMDA-knockout / Nav1.6-knockout / NaP-knockout) across 8 directions and
compute `delta_DSI = DSI_full - DSI_knockout` per channel. The dominant mechanism is the
channel whose knockout collapses DSI the most. Apply to cells 767 / 637 / 762; if NaP-knockout
collapses DSI by the most, t0084's NaP-dominant correlative finding is causally confirmed;
otherwise the attribution shifts. ~96 runs on local CPU. Distinct from S-0084-01 which sweeps
NaP density continuously; S-0084-05 tests all three channels simultaneously with binary
on/off. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>📚 <strong>Promote t0084 attribution-metric pipeline into a reusable
mechanism_attribution_v3 library asset</strong> (S-0084-06)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-05-05 | **Source**:
[t0084_t0081_cell_767_vm_trace_deepdive](../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/)

t0084 produced six well-tested code modules implementing a per-cell extended-recording
pipeline plus fractional-channel-contribution attribution metric. The pipeline is reusable for
any v3 substrate cell (and trivially extensible to v4 substrates) and should not have to be
rebuilt for each follow-up task. Promote it to a library asset under
`assets/library/mechanism_attribution_v3/` with public entry points:
`run_deepdive_for_cell(cell_id, parameter_vector, directions, seed)`,
`compute_fractional_attribution(traces_dir, cell_id, response_window_ms)`,
`plot_attribution_figures(cell_id)`. Pure refactor; no new compute. Cost ~$0. Will accelerate
follow-ups S-0084-01 / S-0084-02 / S-0084-03 / S-0084-05. Recommended task types:
write-library, data-analysis.

</details>

<details>
<summary>🧪 <strong>Substrate regression check on the t0076 iter-424 vector mapped
to the v3 54-d parameter space</strong> (S-0080-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-04 | **Source**:
[t0080_bedb_mobo_v3_dendritic_spike_nsga2](../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/)

REQ-9 / REQ-16 of the t0080 plan deferred the substrate-regression check under cost pressure.
Without it, the t0080 negative result cannot conclusively distinguish 'v3 substrate is
regressed' from 'NSGA-II under-budgeted in 54-d' as the dominant cause of the dramatic Pareto
compression (94% DSI regression vs t0076 at the comparable PD regime). Map t0076's iter-424
25-d vector to the v3 54-d parameterisation with new dendritic-spike parameters at zero (no
dendritic NMDA, no distal Nav1.6/NaP) and run a single 8-direction x 20-seed evaluation
locally. Pass: reproduce DSI within +/- 0.05 of t0076's 0.42 at PD ~ 8.34 Hz. Cheap (~$0.05,
~5 min wall-clock); must precede any further v3 architectural extension. Recommended task
types: experiment-run, baseline-evaluation.

</details>

<details>
<summary>🧪 <strong>Spatial hot-spot analysis of Bed B GABA Bernoulli release vs
bar-arrival projection</strong> (S-0072-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0072_synaptic_traces_pd_nd](../../tasks/t0072_synaptic_traces_pd_nd/)

t0072's Example 9 single-synapse Bed B GABA peak (10.21 nS at synapse_idx=13, ND) is over 60x
the population mean peak (0.16 nS PD; 1.25 nS ND). The Bernoulli release model means most of
177 GABA terminals fire 0-1 events per trial; a handful of high-rate terminals near the bar's
arrival window summate to large momentary conductances. Test whether these hot-spots cluster
spatially: project each terminal's centroid onto the bar-projection axis (0 deg vs 180 deg),
bin into N=10 bands. For each band compute (a) Bernoulli release probability per trial
(analytic from _gaba_prob_for_direction sigmoid + AR(2) envelope), (b) realised mean peak g
from t0072 raw .npz, (c) band-mean to population-mean ratio. Plot peak-g-band vs
projected-distance for PD and ND. Expected: ND smooth gradient (high p engages all bands); PD
sharp leading-edge peak (low p only engages early-arrival terminals). Pure post-hoc on
existing data plus t0024 morphology; ~1 hour. Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Active dendritic conductances (Nav1.6 + Kv3) layered on the t0059
bar-locked GABA + AMPA-escape substrate</strong> (S-0059-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0059_bar_locked_gaba_ampa_sweep_t0057](../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/)

The t0059 negative result (max FULL peak Hz = 2.143, max vector-sum DSI = 0.209) most
plausibly stems from passive dendrites capping local depolarisation; Park2014 [p. 3977] and
PolegPolsky2016 [p. 1278] both implicitly assume active dendritic mechanisms. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, install Nav1.6 (g_Nabar in {0.05, 0.10, 0.20} S/cm^2)
and Kv3 (g_Kv3bar in {0.05, 0.10} S/cm^2) on dendritic sections, and run a focused 3x2x3
(gNa_dend x gKv3_dend x gAMPA in {1.0, 2.0, 4.0}) sweep at GABA_BASE_NS = 0.10 nS (the t0059
vector-sum DSI optimum). Pass criterion: at least one operating point with peak Hz >= 5 Hz AND
vector-sum DSI > 0.3. Distinct from S-0009-03 (calibrates densities against PolegPolsky2016
spike-shape and Ih-sag waveforms only) and S-0002-01 (somatic g_Na/g_K only). Directly
addresses RQ4 on the bar-locked substrate. Recommended task types: build-model,
experiment-run.

</details>

<details>
<summary>🧪 <strong>SEClamp Fig 3A-E re-measurement at intermediate dendritic
locations to test cable-filtering vs spatial-distribution</strong>
(S-0049-05)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-25 | **Source**:
[t0049_seclamp_cond_remeasure](../../tasks/t0049_seclamp_cond_remeasure/)

t0049 measured SEClamp conductance only at the soma (`h.RGC.soma(0.5)`). The GABA PD/ND
symmetry collapse at the soma could be due to (a) cable-filtering averaging out local
asymmetry, or (b) symmetric spatial distribution of GABA synapses across PD/ND-side dendrites.
To discriminate, insert SEClamp at intermediate dendritic locations along the principal axis
(e.g., at 25%, 50%, 75% of the dendritic path from soma to the most distal synapse on each
side) and re-run the per-channel isolation sweep at gNMDA = 0.5 nS. A monotonic decay of the
asymmetry from distal-dendrite to soma supports the cable-filtering hypothesis (b ruled out);
persistence at all locations supports the spatial-distribution hypothesis (a ruled out).
Complementary to S-0049-01's static spatial audit. Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Refine spatial audit with dendritic-branch identity
classification (proximal-PD / proximal-ND / distal)</strong> (S-0050-04)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-25 | **Source**:
[t0050_audit_syn_distribution](../../tasks/t0050_audit_syn_distribution/)

t0050 used three midline-x conventions (soma_x, zero, BIPsyn-locx-median) to classify synapses
as side_a / side_b. A more biophysically meaningful classification partitions synapses by
dendritic branch identity: walk the section tree from soma, label each first-order branch as
proximal-PD or proximal-ND based on its dendritic-field axis, then label deeper segments as
distal. This finer partition would reveal whether the 282-synapse population has
within-PD-branch or within-ND-branch density gradients invisible to a single x-midline split,
and would provide the substrate-level data needed to design any future per-branch synaptic
modification (cf. S-0050-01 / S-0050-02). Pure post-hoc analysis on existing
extract_coordinates outputs. Recommended task types: data-analysis.

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
<summary>🧪 <strong>Rerun t0039 7-diameter sweep on t0024 for active-vs-passive
testbed comparison</strong> (S-0039-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
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
<summary>📚 <strong>Add an iMK801 analogue MOD modification (selective dendritic
NMDAR block) to enable Fig 8 AP5 reproduction</strong> (S-0046-03)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0046_reproduce_poleg_polsky_2016_exact](../../tasks/t0046_reproduce_poleg_polsky_2016_exact/)

Author a new MOD mechanism (or extend `bipolarNMDA.mod`) that selectively blocks NMDAR
conductance in dendritic compartments while leaving somatic NMDAR + AMPA intact, mirroring the
paper's intracellular MK801 (iMK801) protocol. The current AP5 analogue used in t0046
(`b2gnmda = 0`) removes ALL NMDAR contribution and silences the cell entirely (DSI = 0 under
AP5); the paper's iMK801 leaves PD spiking, allowing the qualitative 'DSI preserved under AP5'
Fig 8 claim to be reproduced. This unblocks a faithful Fig 8 AP5 reproduction and resolves the
AP5-vs-iMK801 mechanistic divergence catalogued as discrepancy 1 of 12 in t0046's audit.
Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🧪 <strong>2-D distal length x diameter sweep on t0024 to disambiguate
cable-filtering vs local-spike-failure</strong> (S-0034-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
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
<summary>🧪 <strong>Surface-density-rescaled Nav diameter sweep on t0024 to test
surface-vs-volume compensation</strong> (S-0035-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
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
<summary>🧪 <strong>Ih (HCN) conductance ablation sweep on t0024 distal dendrites to
test h-current role in distal cable behaviour</strong> (S-0035-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-23 | **Source**:
[t0035_distal_dendrite_diameter_sweep_t0024](../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/)

Sweep distal Ih (HCN) gbar from 0 to 2x baseline (five points) on the t0024 DSGC while holding
all other parameters fixed, and measure primary DSI, HWHM, and distal-compartment voltage. Ih
is a known resonance and input-impedance shaper that could partly explain why distal diameter
reads flat on both t0022 and t0024 (t0030 and t0035 both null). If ablation of Ih causes the
diameter sweep to become non-flat, h-current is masking the mechanism. Distinct from S-0009-03
which targeted Ih calibration, not ablation. Recommended task types: experiment-run.

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
<summary>🧪 <strong>Per-dendrite E-I parameter sweep to map the DSI response
surface</strong> (S-0022-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
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
<summary>🧪 <strong>Add Ih (HCN) channel to dendrites and measure its effect on E-I
integration window</strong> (S-0022-08)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-21 | **Source**:
[t0022_modify_dsgc_channel_testbed](../../tasks/t0022_modify_dsgc_channel_testbed/)

The t0022 testbed currently has no Ih (HCN) channels in DEND_CHANNELS. Literature prior from
t0019 (voltage-gated-channels survey) flags Ih as a common dendritic modulator: it lowers
input resistance and shortens the E-I temporal window over which coincidence matters. Add Ih
at a realistic dendritic density (e.g., 1e-5 S/cm^2 following hippocampal CA1 values as a
start) to the DEND_CHANNELS forsec block and rerun the canonical 12-angle x 10-trial sweep
plus an EI_OFFSET sweep in {5, 10, 15, 20, 30} ms. Expected outcome: the E-I integration
window narrows (only tight E-I offsets produce DSI, long offsets stop working), quantifying
the dendritic-integration timescale imposed by Ih. Dependencies: t0022 library asset,
S-0022-03 infrastructure for EI offset sweeps if already done. Effort ~10 hours. Recommended
task type: experiment-run.

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
<summary>🧪 <strong>Extend cable-theory survey to frequency-domain and thin-dendrite
transmission</strong> (S-0015-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0015_literature_survey_cable_theory](../../tasks/t0015_literature_survey_cable_theory/)

The scoped-down 5-paper survey covers 3 of the 5 originally-planned themes in depth (Rall
foundations, on-the-path shunting DS, morphology-driven firing) and references the other two
(frequency-domain cable analysis, thin-dendrite transmission) only indirectly. A follow-up
survey task should add ~5 papers on frequency-domain cable theory (Koch 1984, Segev & Rall
1988) and thin-dendrite active transmission (Stuart & Sakmann 1994, London & Hausser 2005
review, Stuart & Spruston 2015 review) to close the gap.

</details>

<details>
<summary>🧪 <strong>Retrieve paywalled dendritic-computation PDFs via Sheffield
access and verify numerical claims</strong> (S-0016-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0016_literature_survey_dendritic_computation](../../tasks/t0016_literature_survey_dendritic_computation/)

Five foundational dendritic-computation papers (Schiller 2000, Polsky 2004, Larkum 1999,
Bittner 2017, London & Hausser 2005) are documented in intervention/paywalled_papers.md but
were not downloaded. Retrieve their PDFs through Sheffield institutional access, update each
paper asset's download_status to 'success', replace summary Overview disclaimers with
PDF-verified content, and cross-check the numerical claims in the synthesis (NMDA-spike
threshold -50 mV, NMDA-spike duration 20-40 ms, 2-3x supralinear amplification, Ca2+ plateau
duration 30-50 ms, BAC burst 100-200 Hz, BTSP eligibility window of seconds) against the
actual papers.

</details>

<details>
<summary>🧪 <strong>Extend dendritic-computation survey to cerebellar Purkinje and
STDP papers</strong> (S-0016-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0016_literature_survey_dendritic_computation](../../tasks/t0016_literature_survey_dendritic_computation/)

The scoped-down 5-paper survey covers cortical and hippocampal dendritic-computation motifs
(NMDA spike, BAC firing, BTSP, branch-level integration, canonical review) but does not cover
cerebellar Purkinje-cell branch-specific computation or cortical / hippocampal
spike-timing-dependent plasticity. A follow-up survey task should add approximately 5 papers
on cerebellar Purkinje branch-strength (Llinas & Sugimori 1980, Rancz & Hausser 2006, Brunel
2016) and cortical / hippocampal STDP (Bi & Poo 1998, Markram 1997, Sjostrom 2008 review) to
close the gap.

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
<summary>🧪 <strong>Factorial morphology sweep (branch orders, segment length,
segment diameter) at fixed synapse count</strong> (S-0002-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0002_literature_survey_dsgc_compartmental_models](../../tasks/t0002_literature_survey_dsgc_compartmental_models/)

ElQuessny2021 concludes that global DSGC morphology has only a minor effect on the synaptic
E/I distribution, but the survey finds no paper that runs a clean factorial sweep over the
three local-electrotonic knobs separately. With synaptic count fixed at the PolegPolsky
177+177 baseline and dendrites set to active (Schachter2010 densities), vary (number of branch
orders, mean segment length, mean segment diameter) on an orthogonal grid, record DSI and HWHM
per point, and test whether segment diameter has the largest effect (as cable theory
predicts). This directly answers RQ2 and provides the morphology-sensitivity map the project
currently lacks. Recommended task types: experiment-run.

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
<summary>📊 <strong>Render and QA-check 2D/3D visualisations of
dsgc-baseline-morphology for documentation and synapse placement</strong>
(S-0005-05)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0005_download_dsgc_morphology](../../tasks/t0005_download_dsgc_morphology/)

The dsgc-baseline-morphology asset is currently described only by tabulated statistics (6,736
compartments, 129 branch points, 1,536.25 um path length). Downstream tasks that place
AMPA/GABA synapses by spatial rule (e.g., Park2014 3-5x null/preferred IPSC asymmetry,
S-0002-05 GABA/AMPA density scan) need a visual reference for the dendritic arbor,
branch-order map, and soma orientation; reviewers also need a figure for any project paper.
Render three QA visualisations (2D top-down dendrogram coloured by Strahler order, 2D xy
projection coloured by path distance from soma, 3D rotating xyz scatter) using neurom +
matplotlib (or NEURON's PlotShape) and register the figures plus the rendering script as an
answer asset describing what was checked. Flag any visible reconstruction artefacts (dangling
branches, axon stubs, soma asymmetry) for downstream tasks. Recommended task types:
data-analysis, answer-question.

</details>
