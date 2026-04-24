# Category: Synaptic Integration

Summation and interaction of excitatory and inhibitory synaptic inputs.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (39)](../papers/by-category/synaptic-integration.md) | [Answers
(5)](../answers/by-category/synaptic-integration.md) | [Suggestions
(32)](../suggestions/by-category/synaptic-integration.md) | [Predictions
(2)](../predictions/by-category/synaptic-integration.md)

---

## Papers (39)

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
<summary>📖 <strong>Imperfect Space Clamp Permits Electrotonic Interactions between
Inhibitory and Excitatory Synaptic Conductances, Distorting Voltage Clamp
Recordings</strong> — Poleg-Polsky & Diamond, 2011</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pone.0019463` |
| **Authors** | Alon Poleg-Polsky, Jeffrey S. Diamond |
| **Venue** | PLoS ONE (journal) |
| **DOI** | `10.1371/journal.pone.0019463` |
| **URL** | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0019463 |
| **Date added** | 2026-04-20 |
| **Categories** | [`patch-clamp`](../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1371_journal.pone.0019463/summary.md) |

Poleg-Polsky and Diamond ask a methodological question that matters for every modelling paper
built on experimental E/I decomposition: how accurate is the standard protocol of
reconstructing excitatory and inhibitory conductances from multi-holding-potential
voltage-clamp recordings when the cell has thin, extended dendrites? They answer it with
NEURON compartmental simulations of realistic retinal ganglion cell morphologies, where the
ground-truth synaptic input is known and the somatic pipette recording can be directly
compared against it.

The methodology is careful: the authors systematically vary dendritic diameter, synaptic
distance, E/I relative timing, and holding-potential range, and compare each reconstruction
against the known inputs. They also test what happens when voltage-gated dendritic channels
are added. The design isolates space-clamp error from other confounds (series resistance,
filtering, ionic non-stationarity) and lets the reader see exactly which experimental choices
drive the largest distortions.

The headline result is that imperfect space clamp is not a second-order concern: on thin
distal dendrites up to 80% of the synaptic signal is lost, inhibitory estimates are
systematically worse than excitatory ones, and co-active E and I interact electrotonically so
that reconstructing one requires correctly modelling the other. Active dendritic channels make
everything worse. The paper practical guidance (proximal-only reconstruction,
compartmental-model validation of each experiment) is now standard.

For this project, the implication is direct. DSGC models will be calibrated against published
Ge and Gi traces from somatic voltage-clamp recordings, and those traces are lower bounds on
the true dendritic conductances, not ground truth. Our NEURON pipeline must include a somatic
voltage-clamp block so that simulated recordings can be compared to experimental recordings on
the same footing, and we must plan parameter-fitting procedures to absorb a several-fold
calibration uncertainty on distal synaptic conductance amplitudes.

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

## Tasks (8)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |
| 0010 | [Hunt DSGC compartmental models missed by prior survey; port runnable ones](../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) | completed | 2026-04-20 14:42 |
| 0013 | [Resolve dsgc-baseline-morphology source-paper provenance](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) | completed | 2026-04-20 17:21 |
| 0015 | [Literature survey: cable theory and dendritic filtering](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) | completed | 2026-04-20 10:00 |
| 0016 | [Literature survey: dendritic computation beyond DSGCs](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) | completed | 2026-04-20 10:36 |
| 0017 | [Literature survey: patch-clamp recordings of RGCs and DSGCs](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) | completed | 2026-04-20 11:08 |
| 0018 | [Literature survey: synaptic integration in RGC-adjacent systems](../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) | completed | 2026-04-20 12:15 |
| 0027 | [Literature survey: modeling effect of cell morphology on direction selectivity](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) | completed | 2026-04-21 22:23 |

## Answers (5)

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

## Suggestions (28 open, 4 closed)

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
<summary>🧪 <strong>Diagnose and fix the low peak firing rate in t0022 (15 Hz vs
40-80 Hz Schachter2010)</strong> (S-0037-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0037_null_gaba_reduction_ladder_t0022](../../tasks/t0037_null_gaba_reduction_ladder_t0022/)

At the 4 nS sweet spot the preferred-direction peak firing is 15 Hz, an order of magnitude
below Schachter2010's 40-80 Hz baseline. The same low rate was observed in t0030 at 12 nS
GABA, so this is a pre-existing t0022 drive issue (likely the AMPA-only schedule lacking NMDA
or compensatory excitation), not a GABA ladder artefact. A task should add NMDA back into the
t0022 E-I schedule (or increase AMPA gain) and verify peak firing reaches 40+ Hz without
re-pinning DSI. Until this is fixed, any cross-testbed peak-rate comparison is invalid.

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
<summary>🧪 <strong>Diagnose and fix t0022's 15 Hz peak-firing cap (inherited
AMPA-only drive issue)</strong> (S-0039-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-24 | **Source**:
[t0039_distal_dendrite_diameter_sweep_t0022_gaba4](../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/)

Peak firing at the preferred direction is 15 Hz across the diameter sweep, well below
Schachter2010's 40-80 Hz baseline. The same 15 Hz ceiling appeared in t0030 at 12 nS GABA, so
it is a pre-existing t0022 drive issue, not a diameter or GABA artefact. Duplicate of
S-0037-04 but now blocking quantitative literature comparisons for the discriminator task too.
Likely fix: add NMDA back into the E-I schedule, or boost AMPA conductance, or both. Run a
diagnostic trace of soma voltage at preferred direction and compare to Schachter2010's
published traces.

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

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-22 | **Source**:
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
<summary>🧪 <strong>Retrieve paywalled synaptic-integration PDFs via Sheffield access
and verify numerical priors</strong> (S-0018-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0018_literature_survey_synaptic_integration](../../tasks/t0018_literature_survey_synaptic_integration/)

Five synaptic-integration papers (Lester et al. 1990, Koch-Poggio-Torre 1983, Wehr & Zador
2003, Hausser & Mel 2003, Euler-Detwiler-Denk 2002) are documented in
intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs through
Sheffield institutional access, update each paper asset's download_status to 'success',
replace summary Overview disclaimers with PDF-verified content, and cross-check the numerical
priors tabulated in the Prior Distribution Table of the answer asset (NMDAR tau_decay 100-200
ms at 22-32 degC, AMPA tau_rise 0.2-0.4 ms / tau_decay 1-3 ms, GABA_A tau_decay 5-20 ms,
lambda_DC 100-300 um for RGC dendrites, DSGC E-I lag 15-50 ms, SAC dendritic Ca2+ DS index
0.3-0.5) against the actual papers before adopting them as tight compartmental-model fitting
targets.

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
