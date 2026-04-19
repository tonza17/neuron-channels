# Papers: `synaptic-integration` (15)

15 papers across 11 year(s).

[Back to all papers](../README.md)

---

## 2021 (1)

<details>
<summary>📖 Dendrite Morphology Minimally Influences the Synaptic Distribution of
Excitation and Inhibition in Retinal Direction-Selective Ganglion Cells
— El-Quessny & Feller, 2021</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_ENEURO.0261-21.2021` |
| **Authors** | Malak El-Quessny, Marla B. Feller |
| **Venue** | eNeuro (journal) |
| **DOI** | `10.1523/ENEURO.0261-21.2021` |
| **URL** | https://www.eneuro.org/content/8/5/ENEURO.0261-21.2021 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/summary.md) |

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

## 2020 (1)

<details>
<summary>📖 The functional organization of excitation and inhibition in the dendrites
of mouse direction-selective ganglion cells — Jain et al., 2020</summary>

| Field | Value |
|---|---|
| **ID** | `10.7554_eLife.52949` |
| **Authors** | Varsha Jain, Benjamin L Murphy-Baum, Geoff deRosenroll, Santhosh Sethuramanujam, Mike Delsey, Kerry R Delaney, Gautam Bhagwan Awatramani |
| **Venue** | eLife (journal) |
| **DOI** | `10.7554/eLife.52949` |
| **URL** | https://elifesciences.org/articles/52949 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/summary.md) |

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

## 2019 (1)

<details>
<summary>📖 Retinal direction selectivity in the absence of asymmetric starburst
amacrine cell responses — Hanson et al., 2019</summary>

| Field | Value |
|---|---|
| **ID** | `10.7554_eLife.42392` |
| **Authors** | Laura Hanson, Santhosh Sethuramanujam, Geoff deRosenroll, Varsha Jain, Gautam B Awatramani |
| **Venue** | eLife (journal) |
| **DOI** | `10.7554/eLife.42392` |
| **URL** | https://elifesciences.org/articles/42392 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/summary.md) |

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

## 2017 (1)

<details>
<summary>📖 Cross-compartmental Modulation of Dendritic Signals for Retinal Direction
Selectivity — Koren et al., 2017</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2017.07.020` |
| **Authors** | David Koren, James C. R. Grove, Wei Wei |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2017.07.020` |
| **URL** | https://doi.org/10.1016/j.neuron.2017.07.020 |
| **Date added** | 2026-04-19 |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2017.07.020/summary.md) |

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

## 2016 (3)

<details>
<summary>📖 A Central Role for Mixed Acetylcholine/GABA Transmission in Direction
Coding in the Retina — Sethuramanujam et al., 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2016.04.041` |
| **Authors** | Santhosh Sethuramanujam, Amanda J. McLaughlin, Geoffery deRosenroll, Alex Hoggarth, David J. Schwab, Gautam B. Awatramani |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2016.04.041` |
| **URL** | https://www.cell.com/neuron/fulltext/S0896-6273(16)30155-6 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.04.041/summary.md) |

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
<summary>📖 NMDA Receptors Multiplicatively Scale Visual Signals and Enhance
Directional Motion Discrimination in Retinal Ganglion Cells — Poleg-Polsky
& Diamond, 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2016.02.013` |
| **Authors** | Alon Poleg-Polsky, Jeffrey S. Diamond |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2016.02.013` |
| **URL** | https://www.sciencedirect.com/science/article/pii/S0896627316001069 |
| **Date added** | 2026-04-19 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/summary.md) |

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
<summary>📖 Species-specific wiring for direction selectivity in the mammalian retina
— Ding et al., 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nature18609` |
| **Authors** | Huayu Ding, Robert G. Smith, Alon Poleg-Polsky, Jeffrey S. Diamond, Kevin L. Briggman |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/nature18609` |
| **URL** | https://www.nature.com/articles/nature18609 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature18609/summary.md) |

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

## 2014 (1)

<details>
<summary>📖 Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal
Ganglion Cells Lack Direction Tuning — Park et al., 2014</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.5017-13.2014` |
| **Authors** | Silvia J.H. Park, In-Jung Kim, Loren L. Looger, Jonathan B. Demb, Bart G. Borghuis |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.5017-13.2014` |
| **URL** | https://www.jneurosci.org/content/34/11/3976 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/summary.md) |

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

## 2012 (1)

<details>
<summary>📖 Direction selectivity in the retina: symmetry and asymmetry in structure
and function — Vaney et al., 2012</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nrn3165` |
| **Authors** | David I. Vaney, Benjamin Sivyer, W. Rowland Taylor |
| **Venue** | Nature Reviews Neuroscience (journal) |
| **DOI** | `10.1038/nrn3165` |
| **URL** | https://www.nature.com/articles/nrn3165 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/summary.md) |

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

## 2011 (1)

<details>
<summary>📖 Wiring specificity in the direction-selectivity circuit of the retina
— Briggman et al., 2011</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nature09818` |
| **Authors** | Kevin L. Briggman, Moritz Helmstaedter, Winfried Denk |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/nature09818` |
| **URL** | https://www.nature.com/articles/nature09818 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/summary.md) |

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

## 2010 (3)

<details>
<summary>📖 Dendritic Discrimination of Temporal Input Sequences in Cortical Neurons
— Branco et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1126_science.1189664` |
| **Authors** | Tiago Branco, Beverley A. Clark, Michael Häusser |
| **Venue** | Science (journal) |
| **DOI** | `10.1126/science.1189664` |
| **URL** | https://www.science.org/doi/10.1126/science.1189664 |
| **Date added** | 2026-04-19 |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1126_science.1189664/summary.md) |

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
<summary>📖 Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of
Motion in a Simulation of the Direction-Selective Ganglion Cell — Schachter
et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1000899` |
| **Authors** | Michael J. Schachter, Nicholas Oesch, Robert G. Smith, W. Rowland Taylor |
| **Venue** | PLoS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1000899` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000899 |
| **Date added** | 2026-04-19 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`cable-theory`](../../../meta/categories/cable-theory/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/summary.md) |

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
<summary>📖 Synaptic inputs and timing underlying the velocity tuning of
direction-selective ganglion cells in rabbit retina — Sivyer et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1113_jphysiol.2010.192716` |
| **Authors** | Benjamin Sivyer, Michiel Van Wyk, David I. Vaney, W. Rowland Taylor |
| **Venue** | The Journal of Physiology (journal) |
| **DOI** | `10.1113/jphysiol.2010.192716` |
| **URL** | https://doi.org/10.1113/jphysiol.2010.192716 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2010.192716/summary.md) |

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

## 2002 (1)

<details>
<summary>📖 Diverse Synaptic Mechanisms Generate Direction Selectivity in the Rabbit
Retina — Taylor & Vaney, 2002</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.22-17-07712.2002` |
| **Authors** | W. Rowland Taylor, David I. Vaney |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.22-17-07712.2002` |
| **URL** | https://www.jneurosci.org/content/22/17/7712 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.22-17-07712.2002/summary.md) |

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

## 1965 (1)

<details>
<summary>📖 The mechanism of directionally selective units in rabbit's retina. —
Barlow & Levick, 1965</summary>

| Field | Value |
|---|---|
| **ID** | `10.1113_jphysiol.1965.sp007638` |
| **Authors** | H. B. Barlow, W. R. Levick |
| **Venue** | The Journal of Physiology (journal) |
| **DOI** | `10.1113/jphysiol.1965.sp007638` |
| **URL** | https://physoc.onlinelibrary.wiley.com/doi/10.1113/jphysiol.1965.sp007638 |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.1965.sp007638/summary.md) |

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
