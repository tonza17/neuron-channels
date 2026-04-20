# Category: Dendritic Computation

Signal processing that occurs in dendrites prior to somatic spike generation.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (11)](../papers/by-category/dendritic-computation.md) | [Answers
(1)](../answers/by-category/dendritic-computation.md) | [Suggestions
(7)](../suggestions/by-category/dendritic-computation.md) | [Datasets
(1)](../datasets/by-category/dendritic-computation.md)

---

## Papers (11)

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

## Tasks (1)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |

## Answers (1)

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

## Suggestions (5 open, 2 closed)

<details>
<summary>🧪 <strong>Paired active-vs-passive dendrite experiment to reproduce the
Schachter2010 DSI gain (~0.3 -> ~0.7)</strong> (S-0002-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-19 | **Source**:
[t0002_literature_survey_dsgc_compartmental_models](../../tasks/t0002_literature_survey_dsgc_compartmental_models/)

Schachter2010 reports that switching DSGC dendrites from passive to active (adding
Fohlmeister-like g_Na and g_K) raises DSI from ~0.3 to ~0.7 on the same morphology and
synaptic input, and Oesch2005 provides the TTX-sensitive dendritic Na+ spike patch-clamp data
that anchor this claim. Run two paired simulations that differ only in dendritic g_Na (0 vs
Schachter2010 density), holding morphology, synapse placement, and stimulus identical, and
report the DSI delta with 95% CI across synapse-placement seeds. This directly answers RQ4 and
isolates the dendritic-conductance contribution from morphology and synaptic effects.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Factorial morphology sweep (branch orders, segment length,
segment diameter) at fixed synapse count</strong> (S-0002-04)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-19 | **Source**:
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
