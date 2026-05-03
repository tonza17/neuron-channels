# Category: Voltage-Gated Channels

Ion channels whose opening probability depends on membrane voltage.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (16)](../papers/by-category/voltage-gated-channels.md) | [Answers
(4)](../answers/by-category/voltage-gated-channels.md) | [Suggestions
(66)](../suggestions/by-category/voltage-gated-channels.md) | [Libraries
(2)](../libraries/by-category/voltage-gated-channels.md) | [Predictions
(2)](../predictions/by-category/voltage-gated-channels.md)

---

## Papers (16)

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
<summary>📖 <strong>Tailoring of the axon initial segment shapes the conversion of
synaptic inputs into spiking output in OFF-alpha T retinal ganglion
cells</strong> — Werginz et al., 2020</summary>

| Field | Value |
|---|---|
| **ID** | `10.1126_sciadv.abb6642` |
| **Authors** | Paul Werginz, Vineeth Raghuram, Shelley I. Fried |
| **Venue** | Science Advances (journal) |
| **DOI** | `10.1126/sciadv.abb6642` |
| **URL** | https://www.science.org/doi/10.1126/sciadv.abb6642 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/summary.md) |

Werginz, Raghuram, and Fried investigate how intrinsic biophysics downstream of the dendrites
shapes the spike output of OFF-alpha transient retinal ganglion cells. Their hypothesis is
that the AIS is specialised to match the synaptic input that each cell type receives. Using a
combined experimental and computational approach (patch-clamp current-clamp recordings, Nav1.6
and ankyrin-G immunohistochemistry, and NEURON compartmental modelling) they show that AIS
morphology and sodium channel density are the primary determinants of maximum firing rate and
depolarisation-block threshold.

The methodology is carefully matched: the same OFF-alphaT cell population is characterised
electrophysiologically, anatomically, and computationally. Dorsal and ventral retinal
locations are compared because prior work showed that OFF-alphaT cells receive different
synaptic drive in these regions; the intrinsic-biophysics question is whether the output side
is also tuned. The compartmental model serves as a mechanistic bridge, varying only AIS
parameters while holding dendritic and somatic properties constant, to test whether AIS alone
can explain the observed firing-rate differences.

The headline quantitative results are a 7x AIS-to-soma Na+ density ratio, a systematic
AIS-length difference between dorsal and ventral OFF-alphaT cells, and the demonstration that
AIS length alone is sufficient to reproduce the firing-rate and depolarisation-block
differences in the compartmental model. Dorsal cells have longer AISs and sustain higher
firing rates; ventral cells have shorter AISs and enter depolarisation block at lower input
currents.

For this project, the implications are direct. DSGC compartmental models must include an
explicit AIS compartment with Nav1.6 enrichment at the reported density ratio, AIS length
should be a named tunable parameter constrained by immunohistochemistry rather than a fixed
value, and depolarisation-block behaviour must be used as a fitting constraint. Ignoring the
AIS will produce a DSGC model that cannot correctly reproduce high-firing-rate and
strong-contrast responses.

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
<summary>📖 <strong>Mechanisms and Distribution of Ion Channels in Retinal Ganglion
Cells: Using Temperature as an Independent Variable</strong> — Fohlmeister
et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1152_jn.00123.2009` |
| **Authors** | Jürgen F. Fohlmeister, Ethan D. Cohen, Eric A. Newman |
| **Venue** | Journal of Neurophysiology (journal) |
| **DOI** | `10.1152/jn.00123.2009` |
| **URL** | https://journals.physiology.org/doi/10.1152/jn.00123.2009 |
| **Date added** | 2026-04-19 |
| **Categories** | [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/summary.md) |

Fohlmeister, Cohen, and Newman ask how ion channels are distributed across the dendrites,
soma, initial segment, and axon of rat and cat retinal ganglion cells, and how that
distribution must be scaled with temperature to reproduce whole-cell action-potential trains
across 7-37 C. The question matters because single-compartment or under-constrained
multicompartment models of RGCs have historically suffered from parameter degeneracy: many
G-bar maps can fit a recording at one temperature, and the community lacked a principled,
temperature-transferable channel set.

Methodologically, the authors record repetitive spiking in anatomically reconstructed rat Type
I and Type II and cat alpha and beta RGCs at multiple temperatures, then fit phase plots
(dV/dt versus V) of each cell with NEURON multicompartment simulations of the
Fohlmeister-Miller Five-channel model (Na, K(DR), Ca, K(A), K(Ca)). The crucial design choice
is to demand that a single G-bar map fit every temperature simultaneously, so temperature
becomes an identifiability lever, and to separate gating-kinetic Q10s from ion-permeability
Q10s in a GHK-style current equation.

They find that the voltage dependence of rate constants is constant within 7-23 C and within
30-37 C with a sharp transition at 23-30 C; that gating Q10s are ~1.9-1.95 and permeability
Q10s are ~1.5-1.65 above 23 C but climb toward ~8 below 10 C; and that Na channels become
non-Arrhenius below 8 C, with spike failure below 7 C. Peak Na conductance is concentrated on
a thin axonal segment 50-130 um distal to the soma (up to 448 mS/cm^2 in cat alpha), and the
temperature dependence of the IS-SD phase-plot break confirms this localization. A single
cell-type-specific channel map fits all temperatures.

For this project, which is building DSGC compartmental models, this paper is foundational: it
provides a fully calibrated, temperature-scaled Five-channel parameter set for retinal
ganglion cells in rat and cat, including the Na hotspot location, the dendritic Na+K(A) safety
factor, and the two-plateau temperature-scaling scheme. The G-bar tables and Q10 values should
be adopted as the default channel-density prior for DSGC models, modified only where
DSGC-specific evidence demands it, and the phase-plot fitting methodology should be used to
calibrate DSGC compartmental models against future whole-cell recordings.

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
<summary>📖 <strong>Distinct contributions of Nav1.6 and Nav1.2 in action potential
initiation and backpropagation</strong> — Hu et al., 2009</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn.2359` |
| **Authors** | Wenqin Hu, Cuiping Tian, Tun Li, Mingpo Yang, Han Hou, Yousheng Shu |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn.2359` |
| **URL** | https://doi.org/10.1038/nn.2359 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0019_literature_survey_voltage_gated_channels`](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Full summary** | [`summary.md`](../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/summary.md) |

Wenqin Hu and colleagues (2009) published "Distinct contributions of Nav1.6 and Nav1.2 in
action potential initiation and backpropagation" in Nature Neuroscience. The paper is included
in this task's survey because it contributes to the "Nav1.6 vs Nav1.2 subunit co-expression
kinetics" theme of voltage-gated-channel priors relevant to the direction-selective retinal
ganglion cell (DSGC) compartmental model.

CrossRef did not return a machine-readable abstract for this paper. The paper's claims must
therefore be read directly from the publisher PDF before being used in the DSGC model-fitting
pipeline.

The paper's primary significance for this project is its contribution to the "Nav1.6 vs Nav1.2
subunit co-expression kinetics" evidence pool. The answer asset
`assets/answer/nav-kv-combinations-for-dsgc-modelling/` records which DSGC model Nav/Kv
channel combination (subunit identity, compartment, conductance density, activation
half-voltage, or kinetic time constant) this paper supplies, together with the numerical value
when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

</details>

<details>
<summary>📖 <strong>Action potential generation requires a high sodium channel
density in the axon initial segment</strong> — Kole et al., 2008</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn2040` |
| **Authors** | Maarten H P Kole, Susanne U Ilschner, Björn M Kampa, Stephen R Williams, Peter C Ruben, Greg J Stuart |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn2040` |
| **URL** | https://doi.org/10.1038/nn2040 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0019_literature_survey_voltage_gated_channels`](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Full summary** | [`summary.md`](../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn2040/summary.md) |

Maarten H P Kole and colleagues (2008) published "Action potential generation requires a high
sodium channel density in the axon initial segment" in Nature Neuroscience. The paper is
included in this task's survey because it contributes to the "Nav conductance density at AIS"
theme of voltage-gated-channel priors relevant to the direction-selective retinal ganglion
cell (DSGC) compartmental model.

CrossRef did not return a machine-readable abstract for this paper. The paper's claims must
therefore be read directly from the publisher PDF before being used in the DSGC model-fitting
pipeline.

The paper's primary significance for this project is its contribution to the "Nav conductance
density at AIS" evidence pool. The answer asset
`assets/answer/nav-kv-combinations-for-dsgc-modelling/` records which DSGC model Nav/Kv
channel combination (subunit identity, compartment, conductance density, activation
half-voltage, or kinetic time constant) this paper supplies, together with the numerical value
when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

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
<summary>📖 <strong>Different Mechanisms Generate Maintained Activity in ON and OFF
Retinal Ganglion Cells</strong> — Margolis & Detwiler, 2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_jneurosci.0130-07.2007` |
| **Authors** | David J. Margolis, Peter B. Detwiler |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/jneurosci.0130-07.2007` |
| **URL** | https://www.jneurosci.org/content/27/22/5994 |
| **Date added** | 2026-04-20 |
| **Categories** | [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1523_jneurosci.0130-07.2007/summary.md) |

Margolis and Detwiler take a direct experimental approach to the question of whether retinal
ganglion cell maintained activity is synaptically driven or intrinsically generated. Using
whole-cell and cell-attached patch-clamp recordings from morphologically identified ON and OFF
RGCs in rabbit retinal wholemount, they compare maintained firing under control conditions to
firing after pharmacological blockade of ionotropic glutamate receptors. The design cleanly
separates synaptic drive from intrinsic biophysics in the same cells.

The methodology is careful about cell identification and blockade efficacy, and the follow-up
experiments extend the comparison beyond maintained firing to other signatures of pacemaker
activity: subthreshold oscillations, burst firing, and rebound excitation. Each signature is a
distinct testable claim about the cell intrinsic biophysics, not a single measurement.

The headline finding is that ON and OFF RGCs use qualitatively different strategies. ON cells
require synaptic input to fire at rest; OFF cells fire autonomously and additionally show the
full suite of pacemaker properties. The difference is not explained by passive properties but
by different voltage-gated channel complements, a conclusion supported by the pattern of
intrinsic responses.

For this project, the implications matter even though the paper is about pure ON and OFF cells
rather than DSGCs directly. ON-OFF DSGCs integrate both input streams, and the biophysics of
the OFF input pathway may bring some of the intrinsic-pacemaker machinery into the DSGC soma
and dendrites. DSGC compartmental models should consider whether burst firing, rebound
excitation, and subthreshold oscillations are expected behaviours of the target cell and
include or exclude the relevant voltage-gated channels (T-type Ca2+, HCN) accordingly. Using
maintained-activity-under-synaptic-blockade as a model validation target cleanly separates the
intrinsic biophysics from the synaptic drive, and that separation should be part of our
modelling workflow.

</details>

<details>
<summary>📖 <strong>Polarized distribution of ion channels within microdomains of
the axon initial segment</strong> — Wart et al., 2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.1002_cne.21173` |
| **Authors** | Audra Van Wart, James S. Trimmer, Gary Matthews |
| **Venue** | Journal of Comparative Neurology (journal) |
| **DOI** | `10.1002/cne.21173` |
| **URL** | https://doi.org/10.1002/cne.21173 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0019_literature_survey_voltage_gated_channels`](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Full summary** | [`summary.md`](../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1002_cne.21173/summary.md) |

Audra Van Wart and colleagues (2007) published "Polarized distribution of ion channels within
microdomains of the axon initial segment" in Journal of Comparative Neurology. The paper is
included in this task's survey because it contributes to the "Nav subunit localisation at RGC
AIS" theme of voltage-gated-channel priors relevant to the direction-selective retinal
ganglion cell (DSGC) compartmental model.

The methodology and key findings of the paper are stated verbatim in the `## Abstract` section
above. This summary asset deliberately does not paraphrase or extend those claims beyond what
CrossRef returns; any quantitative prior used from this paper in the DSGC model-fitting
pipeline must be read directly from the published figures and tables.

The paper's primary significance for this project is its contribution to the "Nav subunit
localisation at RGC AIS" evidence pool. The answer asset
`assets/answer/nav-kv-combinations-for-dsgc-modelling/` records which DSGC model Nav/Kv
channel combination (subunit identity, compartment, conductance density, activation
half-voltage, or kinetic time constant) this paper supplies, together with the numerical value
when one is reported.

The PDF was not downloadable in this run (see `intervention/paywalled_papers.md` for the
failure reason). Downstream users should obtain the paper through their institutional
subscription before citing any specific numerical claim from it.

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
<summary>📖 <strong>Spike Generator Limits Efficiency of Information Transfer in a
Retinal Ganglion Cell</strong> — Dhingra & Smith, 2004</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_jneurosci.5346-03.2004` |
| **Authors** | Narender K. Dhingra, Robert G. Smith |
| **Venue** | Journal of Neuroscience (journal) |
| **DOI** | `10.1523/jneurosci.5346-03.2004` |
| **URL** | https://www.jneurosci.org/content/24/12/2914 |
| **Date added** | 2026-04-20 |
| **Categories** | [`retinal-ganglion-cells`](../../meta/categories/retinal-ganglion-cells/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modelling`](../../meta/categories/compartmental-modelling/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/summary.md) |

Dhingra & Smith (2004) provide the first quantitative measurement of how much information the
retinal ganglion cell spike generator loses when converting graded synaptic input into a
discrete spike train. Using intracellular recordings from brisk-transient RGCs in an intact
mammalian retina at physiological temperature, combined with ideal-observer analysis of
contrast detection and increment thresholds, they find that spikes require roughly 2.5-fold
higher contrast for detection than the graded potential does (3.8% vs. 1.5%), and carry
approximately 60% fewer distinguishable gray levels.

Mechanistically, the information loss is dominated by the threshold nonlinearity of the spike
generator rather than by stochastic noise in the spike-generation machinery. A simple
threshold- nonlinearity model of the spike generator reproduces both the detection threshold
gap between graded potential and spikes and the full shape of the increment-threshold "dipper"
function for both signals. This implicates threshold-related biophysics — resting potential,
sodium-channel activation voltage, and effective gain — as the key parameters controlling RGC
spike-generator information transfer.

A further result is the trade-off between contrast sensitivity and dynamic range: depolarizing
the cell reduces spike detection threshold (improving low-contrast sensitivity) but also
reduces the range of contrasts the spike output can represent (collapsing high-contrast
responses). No single setting of the spike generator simultaneously maximizes both,
establishing a fundamental constraint on any biophysical model of RGC output.

For DSGC modelling in this project, the paper provides three key constraints. First, our
compartmental DSGC models should be evaluated not only on spike output but also on the
underlying graded-potential response, since the spike conversion systematically loses
information. Second, the threshold-nonlinearity finding means that matching DSGC firing
patterns to experimental data requires careful tuning of spike-initiation-zone sodium-channel
kinetics rather than adding noise to force a match. Third, the sensitivity-dynamic-range
trade-off means that our DSGC model cannot be validated against a single operating point — we
must test across a realistic contrast range and verify that the model reproduces the shape of
the sensitivity-vs-contrast curve, not just a single contrast sensitivity value.

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
<summary>📖 <strong>The NEURON Simulation Environment</strong> — Hines & Carnevale,
1997</summary>

| Field | Value |
|---|---|
| **ID** | `10.1162_neco.1997.9.6.1179` |
| **Authors** | Michael L. Hines, Nicholas T. Carnevale |
| **Venue** | Neural Computation (journal) |
| **DOI** | `10.1162/neco.1997.9.6.1179` |
| **URL** | https://direct.mit.edu/neco/article/9/6/1179-1209/6087 |
| **Date added** | 2026-04-19 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`cable-theory`](../../meta/categories/cable-theory/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/summary.md) |

This paper describes the NEURON simulation environment, a domain-specific software system for
building biophysically detailed compartmental models of individual neurons and small networks.
It motivates the work by the inadequacy of generic ODE solvers for problems with branched
cable geometry, multiple voltage- and ligand-gated ionic currents, and spatially nonuniform
membrane potential. The scope is deliberately broad — from single-compartment HH models
through reconstructed dendritic trees with thousands of compartments — and the paper positions
NEURON as the tool that lets modelers focus on biophysics rather than on numerics.

Methodologically, NEURON rests on four design choices: (1) a two-level data model separating
anatomical `sections` from numerical `segments`; (2) an O(N) Gaussian elimination for the
branched cable matrix; (3) a staggered-time-step second-order integration scheme that is as
cheap per step as backward Euler; and (4) NMODL, a DSL for specifying membrane mechanisms that
is translated to C and dynamically linked into the simulator. The top-level interface is the
hoc interpreter with an InterViews-based GUI for interactive debugging.

The headline results are qualitative — the paper shows that the combined system can simulate
morphologically reconstructed neurons with detailed ion-channel biophysics at usable
wall-clock speeds on 1990s hardware, and that adding new channel types requires only an NMODL
file. The O(N) solver and the staggered Crank-Nicolson integrator are each presented with
mathematical justification and are the numerical innovations that make the system performant.
No quantitative benchmark table is given, but subsequent decades of published models establish
that the framework achieves its design goals.

For this project's literature survey on compartmental DSGC (direction-selective ganglion cell)
models, this paper is foundational infrastructure rather than a direct scientific antecedent.
Virtually every compartmental DSGC model in the literature is written against the abstractions
introduced here — sections, segments, NMODL mechanisms, hoc scripts. Understanding the
section/segment distinction, the role of `nseg`, and the NMODL toolchain is a prerequisite for
reading, replicating, and critiquing those models. The paper also defines the numerical
methods whose accuracy limits (first-order backward Euler, fixed-timestep analytical gating
updates) set the floor for how faithfully any DSGC compartmental model can reproduce fast
dendritic transients.

</details>

## Tasks (6)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |
| 0015 | [Literature survey: cable theory and dendritic filtering](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) | completed | 2026-04-20 10:00 |
| 0016 | [Literature survey: dendritic computation beyond DSGCs](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) | completed | 2026-04-20 10:36 |
| 0017 | [Literature survey: patch-clamp recordings of RGCs and DSGCs](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) | completed | 2026-04-20 11:08 |
| 0019 | [Literature survey: voltage-gated channels in retinal ganglion cells](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) | completed | 2026-04-20 13:00 |
| 0027 | [Literature survey: modeling effect of cell morphology on direction selectivity](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) | completed | 2026-04-21 22:23 |

## Answers (4)

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
<summary><strong>What quantitative priors does the voltage-gated-channels literature
supply for the DSGC compartmental model on (1) Nav subunit localisation at
the RGC AIS, (2) Kv1 subunit expression at the AIS, (3) RGC HH-family
kinetic rate functions, (4) Nav1.6 vs Nav1.2 subunit co-expression
kinetics, and (5) Nav conductance density at the AIS?</strong></summary>

**Confidence**: medium | **Date**: 2026-04-20 | **Full answer**:
[`nav-kv-combinations-for-dsgc-modelling`](../../tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/)

RGC AIS Nav subunits segregate into microdomains with Nav1.6 concentrated distally and Nav1.2
enriched proximally, and Kv1.1/Kv1.2 co-localising with Nav1.6 in the distal AIS.
AIS-localised Kv1 channels activate near threshold (V_half around -40 to -50 mV) with
sub-millisecond kinetics and control AP waveform and somatic repolarisation. The
Fohlmeister-Miller RGC HH kinetics provide canonical alpha/beta rate functions for Nav and Kv
at 22 degC with Nav activation V_half near -40 mV and a Q10 near 3 for warming to 37 degC.
Nav1.6 activates about 10-15 mV more negative than Nav1.2, so distal Nav1.6 initiates the AP
while proximal Nav1.2 supports backpropagation into the soma. Peak AIS Nav conductance density
is about 2500-5000 pS/um2 (roughly 50x somatic density), an order-of-magnitude prior essential
for reproducing fast, reliable AP initiation in compartmental models.

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

## Suggestions (55 open, 11 closed)

<details>
<summary>🧪 <strong>Tier-stratify channel densities in a follow-up Bed B MOBO (per
soma / proximal / distal / terminal)</strong> (S-0076-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-03 | **Source**:
[t0076_bedb_dsi_firing_rate_mobo](../../tasks/t0076_bedb_dsi_firing_rate_mobo/)

REQ-10 follow-up. The t0076 25-d search applied each of 12 channel densities uniformly across
soma + 350 dendrites. Real RGCs have ~50x higher Nav at AIS than soma (Kole 2008) and graded
Ih/Kv distributions per dendritic tier. Re-run the BoTorch MOBO with channels stratified into
4 region tiers (soma, proximal-dendrite, mid-dendrite, terminal), expanding the input to
~40-50 d. Seed the new GP with the 12-cell t0076 Pareto front (uniform-density solutions).
Test whether tier-stratification breaks the inherent DSI-vs-rate trade-off observed in the
25-d search. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Direct test of the t0076-vs-t0068 contradiction: isolate Nav1.6 +
Kv3 effect at the t0076 best-joint operating point</strong> (S-0076-04)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-03 | **Source**:
[t0076_bedb_dsi_firing_rate_mobo](../../tasks/t0076_bedb_dsi_firing_rate_mobo/)

t0068 reported that Nav1.6 + Kv3 co-expression jointly rescues DSI and rate, but the t0076
25-d Pareto front contains no cell with DSI>=0.6 AND rate>=40 Hz at any (Nav1.6, Kv3)
combination. The contradiction is either (a) substrate-specific (t0068 used Bed A; t0076 used
Bed B); (b) a t0068 local-minimum that wider search escaped; or (c) the other 23 t0076
parameters destructively interfere with the rescue. Resolve by fixing the t0076 iter-424
best-joint cell (DSI=0.42, rate=4.95 Hz) and sweeping ONLY (Nav1.6, Kv3) over the t0068 grid
(5x5 densities, both substrates). Compare: does the rescue appear on Bed B at this fixed
background? Does it disappear on Bed A when the other 23 t0076-style parameters are perturbed
away from t0068 defaults? Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Add a slow Kv-mediated AHP mechanism to Bed B and quantify its
effect on the firing-rate ceiling and DSI</strong> (S-0076-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-03 | **Source**:
[t0076_bedb_dsi_firing_rate_mobo](../../tasks/t0076_bedb_dsi_firing_rate_mobo/)

The t0076 high-rate Pareto extreme (iter 319, 127.75 Hz) exceeds biological mean PD rates
(30-80 Hz) precisely because Bed B lacks a slow-adaptation mechanism. The vendored SK and BK
mechanisms (from cortical/Purkinje sources) and the single-shell `cad` Ca pool (taur=5 ms)
collectively fail to cap firing on the timescale real RGCs use. Vendor a slow-AHP (e.g., SK_E2
with longer Ca-binding time, or a dedicated KAHP mechanism) and re-evaluate a 5-cell subsample
of the t0076 Pareto front: does the high-rate end of the Pareto front contract toward
physiological rates? Does a slow AHP open a new DSI>=0.4 + rate>=30 Hz region? This is a
focussed mechanism-addition test, not a full MOBO re-run. Recommended task types:
experiment-run.

</details>

<details>
<summary>📊 <strong>Plot polar tuning curves to distinguish SK_high narrowing from
flat-top clipping</strong> (S-0074-01)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

SK_high produced HWHM = 41 deg (delta -42 deg, the largest narrowing in the sweep).
Creative-thinking flagged that this could be a flat-top clipping artefact rather than true
narrowing: if SK acts as a firing-rate ceiling, the curve becomes flat-topped near the peak
and HWHM becomes ill-defined. Resolution requires a per-condition polar curve plot for SK_high
(and as a control, SK_med, SK_low, baseline). Cost: ~30 min coding using the existing t0011
plot_polar_tuning_curve. If polar plot shows flat-top with sharp shoulders, the narrowing is a
clipping artefact; if it shows a true narrow bell, the effect is real and SK_high is
biologically interesting. This is purely an analysis task on the existing per_trial_full.csv —
no new sim runs.

</details>

<details>
<summary>📊 <strong>Verify NaR broadening hypothesis: ND-lobe firing rescue at
sub-threshold angles</strong> (S-0074-02)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

NaR_med and NaR_high broadened HWHM by +34 / +36 deg without changing peak rate or vector-sum
DSI. Creative-thinking hypothesised NaR's slow `s` reactivation gate creates a sub-threshold
floor that pushes ND-direction firing above zero, broadening the curve symmetrically. Test:
load per_trial_full.csv, filter rows where condition_id in (nar_high, nar_med, baseline) and
angle in (90, 120, 150, 180, 210, 240) deg, count trials with n_spikes > 0. Hypothesis
confirmed if NaR_high has > 30% of trials firing at angle 90-180 deg vs baseline ~5%. Cost:
pure-data analysis, no new sims (~15 min coding). If confirmed, NaR is a natural candidate for
AIS-localised follow-up since AIS-localised NaR could selectively boost ND firing without
affecting PD.

</details>

<details>
<summary>🧪 <strong>AIS-localised Kv7 follow-up (t0075 candidate)</strong>
(S-0074-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

Kv7 was inert at all 3 somatic densities tested in t0074 (vector-sum DSI delta < 0.003 at
every density). Compare-literature confirmed this matches Hu 2007 / Shah 2008's prediction
that Kv7's canonical site is the AIS, not the soma. Build a virtual AIS section on Bed A (30
µm, between soma and virtual axon, with HHst at 5x somatic density), and re-run the 3-density
Kv7 sweep with insertion on the AIS rather than the soma. This was already proposed as the
t0075 candidate in earlier brainstorming (S-0067-03). Hypothesis: Kv7_AIS at 0.001-0.005
mS/cm² produces a measurable change in either HWHM or vector-sum DSI; M-current's slow
accumulation is well-suited to the AIS firing regime.

</details>

<details>
<summary>🧪 <strong>BK + SK co-expression sweep: linear-add vs saturation</strong>
(S-0074-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

BK and SK produced very similar narrowing patterns at low / med densities (delta_HWHM ~ -0.2
to -7 deg, delta_vec_DSI ~ -0.02 to -0.05 — within 1 SD of each other). Creative-thinking
proposed they may share a Ca-pool-driven mechanism. Test: 4-condition co-expression sweep —
{BK_med, SK_med, BK_med + SK_med, baseline} × 12 angles × 5 seeds = 240 trials, ~10 min
compute. If BK + SK co-expression delta equals the linear sum of single-channel deltas, the
channels are non-interacting (different downstream effects); if the combined delta saturates
near the larger single-channel delta, they share a Ca-pool-driven mechanism. Either outcome
teaches us about BK / SK co-expression in DSGCs and informs the t0075 dendritic-active
follow-up.

</details>

<details>
<summary>🧪 <strong>Kv4 retest with hyperpolarising prepulse to remove
inactivation</strong> (S-0074-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

Kv4 / IA was inert at all 3 densities. Compare-literature: Kv4's V_half_h is -50 mV; the
DSGC's resting potential is -60 mV, which is below V_half_h, so Kv4 sits inactivated at rest.
To engage Kv4, a brief hyperpolarising prepulse (~50 ms at -80 mV) before the bar-rotation
stimulus would remove inactivation. Modify the run_sweep.py protocol to include a 50 ms
pre-pulse window; re-run the 3-density Kv4 sweep (3 conditions × 12 angles × 5 seeds = 180
trials, ~6 min compute). Hypothesis: with the prepulse, Kv4 produces measurable HWHM narrowing
and peak-rate suppression at high density. If confirmed, Kv4 is biologically active in DSGCs
but only after recent hyperpolarisation — relevant for understanding ON-OFF DSGCs that
experience hyperpolarising rebounds between stimulus presentations.

</details>

<details>
<summary>🧪 <strong>Kv3 + NaP co-expression: high-rate firing regime</strong>
(S-0074-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

Kv3 was inert at all 3 densities at our peak rates (~20 Hz baseline). Literature (Rudy &
McBain 2001) says Kv3 engages strongly above 100 Hz. NaP_high produced a 74 Hz peak rate — the
highest in the sweep. Co-expression of Kv3 with NaP should put us in Kv3's effective regime.
Test: 4 conditions {NaP_high, NaP_high + Kv3_low, NaP_high + Kv3_med, NaP_high + Kv3_high} ×
12 angles × 5 seeds = 240 trials, ~10 min compute. Hypothesis: Kv3 co-expression with NaP_high
partially rescues DSI by providing fast repolarisation, allowing the cell to recover between
PD spikes and reducing the depolarisation block we hypothesised in creative-thinking.

</details>

<details>
<summary>🧪 <strong>Find the NaP density at which vector-sum DSI crosses 0.1</strong>
(S-0074-07)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

NaP_low gives vector-sum DSI = 0.227 (delta +0.034). NaP_med gives 0.226 (delta +0.033).
NaP_high gives 0.050 (delta -0.143). The DSI-loss transition between NaP_med (0.01 mS/cm²) and
NaP_high (0.05 mS/cm²) is sharp; the exact threshold density is between 0.01 and 0.05. Run a
5-density sweep (e.g., 0.01, 0.015, 0.02, 0.03, 0.05 mS/cm²) × 12 angles × 5 seeds × 5
conditions = 300 trials, ~12 min compute. Hypothesis: there's a critical density d* in (0.01,
0.03) above which vector-sum DSI drops sharply; characterising d* exactly is needed for any
future NaP-modulation experiments. Updated version of S-0067-01 using vector-sum DSI rather
than legacy DSI as the metric.

</details>

<details>
<summary>🧪 <strong>Repeat t0074 sweep on Bed B (de-Rosenroll DSGC)</strong>
(S-0074-08)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

t0074 covered Bed A only. Bed B (de-Rosenroll 2026, t0024 library) has different morphology,
different synapse placement, and a built-in Ca pool — meaning the channel-level findings here
may not generalise to Bed B. Repeat the same 25-condition × 12-angle × 5-seed sweep on Bed B.
Cost: same ~70 min compute as t0074. Comparison points: which channels remain inert; whether
NaP-induced DSI loss reproduces; whether SK_high HWHM narrowing reproduces (or is a
Bed-A-specific artefact); whether the with-cad baseline DSI shift seen in Bed A is also seen
in Bed B (where cad is native). This is a cross-substrate validation that strengthens any
conclusions drawn from t0074.

</details>

<details>
<summary>📊 <strong>Validate vendored BK/SK MOD kinetics against published RGC
patch-clamp data</strong> (S-0074-09)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

The vendored BK MOD comes from Mainen-Sejnowski 1996 (cortical pyramidal); SK from Hay 2011
(L5 pyramidal). Their kinetics may not match RGC patch-clamp recordings. Run voltage-clamp
simulations on a single soma in NEURON for each MOD (step protocol from -90 to +40 mV in 10 mV
steps, 100 ms duration) and compare resulting current traces against Pfeiffer-Friedrich 2012
(mouse RGC BK) and Wang 2014 (mouse RGC SK). If the activation V_half or time constants
deviate by > 20%, retune the MOD parameters or vendor an RGC-specific MOD instead. Cost: ~1
hour coding + 10 min sim + 30 min comparison plotting. Outcome: either a validation note in
the library description, or a v0.2.0 of the channel pack with retuned RGC-specific kinetics.

</details>

<details>
<summary>🧪 <strong>Test cad insertion on dendrites only (not soma)</strong>
(S-0074-10)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-02 | **Source**:
[t0074_channel_tuning_width_bed_a](../../tasks/t0074_channel_tuning_width_bed_a/)

Inserting cad on the soma shifted Bed A's baseline DSI from 0.7975 (no-cad regression) to
0.308 legacy / 0.193 vector-sum (with-cad). This shift is a structural artefact of soma-only
Ca-pool insertion. Real DSGCs have distributed Ca channels and Ca pools throughout the
dendrites. Test: insert cad on the dendritic compartments (not the soma), then re-run a small
validation sweep (baseline + 3 BK densities × 12 angles × 5 seeds = 240 trials). Hypothesis:
dendritic cad insertion preserves the no-cad baseline DSI more closely while still providing
functional Ca for BK / SK channels in the dendrites. If confirmed, this is the right substrate
design for t0075 active-dendrite work and improves t0074's biological plausibility post-hoc.

</details>

<details>
<summary>🧪 <strong>Find the NaP density at which DSI crosses zero</strong>
(S-0067-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-01 | **Source**:
[t0067_t0065_soma_channel_addition_sweep](../../tasks/t0067_t0065_soma_channel_addition_sweep/)

t0067 showed NaP at 0.8 mS/cm² gives DSI = 0.117 (positive but low) and at 2.4 mS/cm² gives
DSI = -0.179 (inverted). The exact crossing density is between 0.8 and 2.4 mS/cm². Run a finer
5-point density sweep on NaP only (e.g., 0.8, 1.0, 1.3, 1.7, 2.4 mS/cm²) with 10 seeds each
(~25 min compute) to characterise the DSI-vs-NaP-density transition curve and identify the
threshold density at which directional inversion becomes statistically robust. This is the
most surprising finding from t0067 and warrants quantitative refinement.

</details>

<details>
<summary>🧪 <strong>Replace simplified MOD kinetics with ModelDB-sourced canonical
implementations</strong> (S-0067-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0067_t0065_soma_channel_addition_sweep](../../tasks/t0067_t0065_soma_channel_addition_sweep/)

t0067's 5 MOD files use simplified HH-style m/h gates with V_half and time constants from
published values, but lose features specific to each channel: NaR's blocking-particle
mechanism (Khaliq-Raman 2003 uses a 5-state Markov scheme), Kv3 inactivation kinetics
(Wang-Buzsaki 1996 has a two-component decay), Kv4 voltage-dependent recovery (Hoffman 1997
has a recovery time constant tau_h(v) that varies 5-fold across V). NaR/Kv3/Kv4 in particular
showed almost no effect in t0067, possibly because the simplified kinetics miss their
distinctive features. Vendor the canonical ModelDB MOD files for these 3 channels (matching
the deposited cell's USEION conventions or wrapping in NONSPECIFIC_CURRENT shells) and re-run
the sweep. Expected: NaR/Kv3/Kv4 show real DSI effects, especially at high firing rates (>40
Hz).

</details>

<details>
<summary>📊 <strong>Investigate biological NaP overexpression as a
directional-selectivity disorder model</strong> (S-0067-05)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0067_t0065_soma_channel_addition_sweep](../../tasks/t0067_t0065_soma_channel_addition_sweep/)

t0067 showed that NaP at 2.4 mS/cm² INVERTS direction selectivity in the deposited DSGC.
Persistent sodium currents are dysregulated in several pathologies: epilepsy (SCN1A
gain-of-function increases NaP), motor neuron disease (NaP downregulation in ALS), and chronic
pain (NaP upregulation in DRG neurons). Survey the literature for clinical/preclinical reports
of altered NaP in retinal pathologies or DSGCs specifically. If found, this t0067 finding
becomes a candidate computational model for a real disease state. Output: an answer asset
summarising the literature on NaP dysregulation in DSGCs / retinal disease.

</details>

<details>
<summary>🧪 <strong>Test M-current (KCNQ / Kv7) co-expression with Nav1.6</strong>
(S-0068-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0068_t0067_nav16_kv3_coexpression_rescue](../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/)

Another rescue candidate: M-current is a slowly-activating, non-inactivating K+ current with
V_half around -40 to -45 mV. Unlike Kv3 it doesn't repolarise fast APs; it provides a tonic
outward current that opposes sustained depolarisation. In a Nav1.6-driven high-firing regime,
M-current would provide steady hyperpolarisation that reduces the cell's mean depolarisation,
possibly restoring the regime where the GABA shunt has more leverage. Implementation: write a
simple m^1 MOD with V_half = -45 mV, tau ~50 ms, sweep at Nav1.6_med + Nav1.6_high.

</details>

<details>
<summary>🧪 <strong>Move Nav1.6 + Kv3 to a virtual AIS instead of soma</strong>
(S-0068-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0068_t0067_nav16_kv3_coexpression_rescue](../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/)

Real RGCs concentrate Nav1.6 and Kv3 at the AIS at ~50x somatic densities. The Nav1.6 + Kv3
co-localisation we modelled here is somatic, which the t0067 / t0068 limitations document as
understating the joint effect. Add a 30-um AIS section to the deposited cell, place Nav1.6 +
Kv3 there at 30 / 90 mS/cm^2 (and a wider Kv3 density grid up to ~200 mS/cm^2), re-run the
rescue sweep. Expected: AIS-localised Kv3 at very high density may finally show DSI rescue
because the AIS's smaller diameter makes per-segment conductance changes leverage the AP shape
more strongly. If still no rescue, the channel-pharmacology approach to DSI rescue is null
across substrates.

</details>

<details>
<summary>🧪 <strong>Sweep Kv3 alone (no Nav1.6) to validate the kinetic-model
effect</strong> (S-0068-05)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0068_t0067_nav16_kv3_coexpression_rescue](../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/)

t0067 sweep showed Kv3 alone (without Nav1.6) had essentially no effect on firing rate or DSI
(DSI = 0.80 → 0.82 across low/med/high). t0068 shows Kv3 also has no rescue effect on top of
Nav1.6. To confirm that this isn't a model artefact (e.g., Kv3 not engaging because of an MOD
bug), run a finer Kv3-only sweep with very high densities (60, 200, 500 mS/cm^2) and check
whether SOME density level produces a measurable firing-rate effect. If Kv3 at 500 mS/cm^2
still does nothing, our simplified Kv3 MOD likely needs revision to a richer kinetic scheme
(e.g., Wang-Buzsaki with two-component decay).

</details>

<details>
<summary>🧪 <strong>Shrink AIS diameter to 0.5 μm and re-test channel
insertions</strong> (S-0069-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-01 | **Source**:
[t0069_t0067_ais_localised_channel_sweep](../../tasks/t0069_t0067_ais_localised_channel_sweep/)

Real RGC AIS diameters cluster around 0.4-0.8 μm; t0069 used 1 μm. A narrower AIS has higher
input resistance per unit area, so the same gbar of an AIS-localised Nav or Kv channel
produces a much larger local depolarisation. Test: rebuild the AIS at diam=0.5 μm (keep L=30
μm), keep all other parameters identical to t0069, re-run the 16-condition × 2-direction ×
5-seed sweep. Combined with S-0069-01 (halved somatic Na), this should be the configuration
that finally exposes AIS-localised Kv3 / Kv4 effects. Compute: ~10 min.

</details>

<details>
<summary>🧪 <strong>Co-insert Nav1.6 + Kv3 on the AIS at biological
densities</strong> (S-0069-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0069_t0067_ais_localised_channel_sweep](../../tasks/t0069_t0067_ais_localised_channel_sweep/)

S-0068-04 already proposed AIS Nav1.6 + Kv3 co-insertion. t0069's baseline-quenching means a
naive co-insertion sweep on the unweakened soma will likely also be inert. So this should run
AFTER S-0069-01 (somatic Na halved). Test 4 conditions on the t0069 substrate with halved
somatic Na: {Nav1.6_med + Kv3_med, Nav1.6_med + Kv3_high, Nav1.6_high + Kv3_med, Nav1.6_high +
Kv3_high} on AIS × PD/ND × 5 seeds = 40 trials. Hypothesis: with a weakened soma and the
natural fast-spiking AIS recipe (Nav1.6 + Kv3), the cell becomes more like a real fast-firing
RGC and DSI becomes higher (or more controllable) than the t0067 single-channel sweep showed.

</details>

<details>
<summary>🧪 <strong>Investigate whether the t0069 NaP_high AIS effect (DSI = 0.22)
is robust to AIS geometry</strong> (S-0069-05)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0069_t0067_ais_localised_channel_sweep](../../tasks/t0069_t0067_ais_localised_channel_sweep/)

NaP at high density on the AIS gave the largest signal (-0.78 ΔDSI), 80% of the soma version's
effect. Persistent Na is interesting because it survives the AIS+axon's electrical sink — its
non-inactivating depolarisation accumulates over the trial duration, so even a small AIS can
pump enough current. Question: does the AIS NaP effect scale predictably with AIS geometry, or
does it saturate? Test NaP at {1.0, 1.5, 2.4, 3.5, 5.0} mS/cm² on AIS at fixed (L=30 μm,
diam=1 μm); also test 2.4 mS/cm² at diam ∈ {0.5, 0.7, 1.0, 1.5} μm. Hypothesis: NaP gnabar ×
AIS surface area ≈ constant for a fixed DSI effect (i.e., the cell sees the integrated NaP
current). 9 conditions × 2 directions × 5 seeds = 90 trials, ~5 min.

</details>

<details>
<summary>🧪 <strong>Re-enable Bed A L-type and T-type Ca currents and quantify the
effect on tuning curves and DSI</strong> (S-0070-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0070_writeup_two_model_beds](../../tasks/t0070_writeup_two_model_beds/)

The t0070 writeup documents that Bed A's `init_active` zeros `RGCcaL` and `RGCcaT`
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc:L155-L156`),
removing the L-type and T-type Ca currents that are present in the original Poleg-Polsky 2016
paper. Bed B inherits the same `glbar_HHst = 3e-4` and `gtbar_HHst = 3e-4 S/cm^2` PARAMETER
defaults (`HHst_noiseless.mod:L57-L58`) on every section because its Python builder never
overrides them. This is the single most visible biophysical divergence between the two beds.
Run a controlled experiment: re-enable Bed A's Ca currents at the `HHst.mod` defaults (and at
the Bed B densities), re-run the t0065 EPSP/IPSP/FULL protocol, and report changes in DSI,
peak firing rate, and EPSP/IPSP envelopes. The result either justifies harmonising the two
beds on the same Ca configuration or documents a biophysically motivated reason to keep them
divergent. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>📚 <strong>Disambiguate the silently-overloaded HHst mechanism name across
the two libraries via SUFFIX rename</strong> (S-0070-05)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0070_writeup_two_model_beds](../../tasks/t0070_writeup_two_model_beds/)

The t0070 research_code.md and writeup both flag a cross-library namespace collision: both
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/HHst.mod`
(Linaro-Storace-Giugliano stochastic) and
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/HHst_noiseless.mod`
(deterministic) declare `SUFFIX HHst`. Any code that says `seg.HHst.gnabar` references
different mechanisms depending on which `nrnivmodl` directory was loaded last, with no
warning. The kinetics happen to be identical so the bug is currently latent, but mid-flight
library swaps in cross-bed runners (S-0070-02) will silently change noise behaviour. Rename
Bed B's SUFFIX (e.g., to `HHst_det`) via corrections on the t0024 library, recompile, update
`build_cell.py` and downstream protocol code, and add a verificator scanning
`tasks/*/assets/library/*/sources/*.mod` for duplicate SUFFIX. Recommended task types:
write-library, infrastructure-setup, correction.

</details>

<details>
<summary>🧪 <strong>Quantify Bed A vs Bed B `celsius` and `v_init` divergence
revealed by the side-by-side equation table</strong> (S-0071-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0071_t0070_synaptic_eqs_pdf](../../tasks/t0071_t0070_synaptic_eqs_pdf/)

Authoring all equations side-by-side in one document made four numeric divergences between Bed
A and Bed B unambiguous (rows 7, 9, 16, 17 of the comparison table in
`results_detailed.md:L778-L799`): `celsius` 32 vs 36.9 deg C (HHst gating tau differs ~2x via
Q10), `v_init` -65 vs -60 mV (shifts Mg-block operating point and Na inactivation), NMDA
on/off (S-0070-04 wires it on but does NOT pick a target value), CaL+CaT zeroed/default
(S-0070-03 turns Bed A's Ca on but does NOT pick a target). Run a 4-condition factorial sweep
on Bed A's t0065 protocol toggling `celsius in {32, 36.9}` x `v_init in {-65, -60}` to
quantify how much of the observed Bed A vs Bed B DSI / peak-Hz / EPSP-envelope difference is
attributable to these two non-Ca, non-NMDA conventions alone — the result decides whether
project-wide convention harmonisation is needed before S-0070-01..04 can be interpreted.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Quantify Bed A NMDA ND-suppression as a function of joint
(gabaMOD, Mg2+) on the t0072 substrate</strong> (S-0072-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0072_synaptic_traces_pd_nd](../../tasks/t0072_synaptic_traces_pd_nd/)

t0072's per-synapse recordings surfaced a counter-intuitive Bed A finding: mean peak g_NMDA is
0.30 nS at PD vs 0.19 nS at ND (~37% drop) despite identical BIPsyn release envelopes between
directions. The mechanism is the Jahr-Stevens Mg block: stronger ND inhibition keeps dendritic
v more hyperpolarised, deepening the voltage-dependent block and lowering realised gNMDA. Run
a focused 2-D sweep on the Bed A substrate (t0008/t0020 builder) varying (gabaMOD, [Mg2+]_o)
over a 5x5 grid at fixed PD/ND bar geometry, recording per-synapse g_NMDA and v_local with the
same recorder pattern as t0072, and producing the surface (g_NMDA_ND - g_NMDA_PD) vs (gabaMOD
ratio, [Mg2+]_o). Cross-check against a Voff_bipNMDA = 1 control (voltage-independent NMDA
from t0048) which should flatten the surface to ~0. Distinct from S-0026-06 (V_rest
TTX/NMDA-block sweep on t0022/t0024) and S-0048-* (DSI-vs-gNMDA at fixed Mg2+). Recommended
task types: experiment-run.

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
<summary>🧪 <strong>Mg-block NMDA + bar-locked tonic GABA + AMPA-escape combination
sweep on the t0059 substrate</strong> (S-0059-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0059_bar_locked_gaba_ampa_sweep_t0057](../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/)

S-0057-06 covers Mg-block NMDA + tonic GABA but uses t0057's global (100, 1400) ms tonic
window and fixed gAMPA = 0.5 nS. t0059 demonstrates the bar-locked window mechanism delivers
an 8.5 ms direction-dependent IPSP centre-of-mass shift (REQ-13 PASS) the global window
cannot. Layering Mg-block NMDA on the bar-locked substrate combines all three plausible
gap-closers identified in compare-literature: voltage-dependent NMDA gain (PolegPolsky2016),
per-synapse bar-arrival timing (deRosenroll2026), and AMPA escape. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, install the Jahr-Stevens NMDA_MgBlock mechanism from
t0055 at each E synapse, sweep gNMDA in {0.0, 0.25, 0.5, 1.0} nS x gAMPA in {1.0, 2.0, 4.0} nS
at GABA_BASE_NS = 0.10 nS (12 cells, 4320 trials at 10 trials x 12 directions x 3 modes). Pass
criterion: vector-sum DSI > 0.3 AND peak Hz >= 5 Hz. Distinct from S-0057-06 (global tonic
window, gAMPA=0.5 fixed). Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>📚 <strong>Project-wide DSGC measurement-protocol fix: EPSP_PASSIVE /
IPSP_PASSIVE / FULL trial modes with HH save-and-zero</strong> (S-0055-01)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-28 | **Source**:
[t0055_nmda_mg_block_dsi_recovery](../../tasks/t0055_nmda_mg_block_dsi_recovery/)

Refactor the minimal-DSGC trial code (forked across t0052/t0053/t0054/t0055) to replace the
legacy FULL/E_ONLY/GABA_ONLY trio with a FULL/EPSP_PASSIVE/IPSP_PASSIVE trio. EPSP_PASSIVE and
IPSP_PASSIVE must save-and-zero soma+AIS gnabar_hh and gkbar_hh so the recorded EPSP and IPSP
traces are clean synaptic envelopes, not spike-contaminated traces (the user-flagged bug that
made t0054 REQ-20 and t0055 REQ-20 return null at every gNMDA). Drop the per-synapse
activation-time histogram. Confirm and standardize the trial length with the user (1400 vs
1500 ms vs longer window for EPSP-decay metrics; 3000-5000 ms recommended by S-0054-03). Pass
criterion: EPSP/IPSP traces from a representative gNMDA value show no Na+ spikes; HH-on FULL
trace is unchanged within 1e-6 mV vs current code. Recommended task types: write-library,
infrastructure-setup. This is a project-wide infrastructure fix that benefits every future
DSGC task.

</details>

<details>
<summary>📚 <strong>Add NMDA_MgBlock voltage-clamp sanity test as a reusable
verificator across all NMDA-bearing DSGC tasks</strong> (S-0055-07)</summary>

**Kind**: library | **Priority**: low | **Date**: 2026-04-28 | **Source**:
[t0055_nmda_mg_block_dsi_recovery](../../tasks/t0055_nmda_mg_block_dsi_recovery/)

t0055 introduced a single-synapse SEClamp sanity test (`test_nmda_mg_block_voltage_dep.py`)
that validated the Jahr-Stevens Boltzmann at v in {-80, -60, -40, -20, 0, +20} mV (peak g
monotonic; peak g(-80)/peak g(-20) = 0.0167). Promote this into a reusable
arf/scripts/verificators/ check that any DSGC task using NMDA_MgBlock can invoke as a
precondition. The check loads the task's compiled NMDA mechanism, runs the 6-voltage clamp,
and asserts the monotonicity + threshold pattern within tolerance. Companion to S-0054-04
(gNMDA = 0 baseline-equivalence verificator). Pass criterion: verificator script exists, runs
against t0055 and passes; documentation describes when downstream tasks should invoke it.
Recommended task type: write-library, infrastructure-setup.

</details>

<details>
<summary>🧪 <strong>Tonic GABA + Mg-block NMDA combination on t0054-style
architecture to test multiplicative gain rescue</strong> (S-0057-06)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-28 | **Source**:
[t0057_tonic_gaba_sweep_t0053](../../tasks/t0057_tonic_gaba_sweep_t0053/)

Cumulative project evidence (t0054, t0055, t0057) converges on PolegPolsky2016's argument that
voltage-dependent NMDA Mg-block is necessary for non-trivial DSI. t0055 added Mg-block NMDA
but kept scalar gabaMOD inhibition; t0057 swapped inhibition to tonic but kept AMPA-only
excitation. Neither tested the combination. Build a minimal architecture combining (a) AMPA +
Jahr-Stevens Mg-block NMDA (t0055 NMDA_MgBlock.mod) on each E synapse and (b) tonic GABA via
gaba_tonic.mod (t0057) with the t0053 spatial centripetal gating predicate on each I synapse.
Sweep gNMDA in {0.0, 0.25, 0.5, 1.0} nS x GABA_BASE_NS in {0.1, 0.25, 0.5, 1.0} nS at fixed
gAMPA = 0.5 nS, seed 0 (16 grid cells, 5760 trials). Pass criterion: locate at least one
(gNMDA, GABA_BASE_NS) point with vector-sum DSI > 0.3 AND peak Hz >= 5 Hz, or rule it out.
Distinct from S-0054-02 (voltage-independent NMDA + scalar GABA) and S-0055-03 (Mg-block NMDA
+ scalar GABA ladder). Recommended task types: build-model, experiment-run.

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
<summary>📚 <strong>Instantiate AIS_PROXIMAL / AIS_DISTAL / THIN_AXON channel sets on
t0022 as a t0033 optimiser prerequisite</strong> (S-0033-02)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-22 | **Source**:
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
<summary>🧪 <strong>Nav1.1 proximal-AIS knockout channel-swap on the t0022
testbed</strong> (S-0022-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
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

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
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
<summary>🧪 <strong>Kv3 vs Kv1 AIS placement swap to test the Kole-Letzkus 2007
repolarisation prior</strong> (S-0022-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0022_modify_dsgc_channel_testbed](../../tasks/t0022_modify_dsgc_channel_testbed/)

Kole & Letzkus 2007 report that Kv1 in the proximal AIS sets spike threshold while Kv3 in the
distal AIS sets repolarisation speed and thus maximum sustained firing rate. Use the t0022
AIS_PROXIMAL and AIS_DISTAL forsec blocks to implement four conditions: (a) Kv1 proximal + Kv3
distal (canonical), (b) Kv1 distal + Kv3 proximal (swap), (c) Kv1 both (no Kv3), (d) Kv3 both
(no Kv1), each with Nav1.6 held at 8 S/cm^2 in the distal AIS. Rerun the 12-angle x 10-trial
sweep for each condition. Expected outcome: condition (a) peaks near 30-40 Hz; condition (b)
drops peak because distal Kv1 fails to fast-repolarise; conditions (c) and (d) test whether
either K-channel alone suffices. Dependencies: t0022 library asset. Effort ~16 hours.
Recommended task type: experiment-run, comparative-analysis.

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
<summary>🧪 <strong>Sweep paper-text biophysics (Ra 200, eleak -65, Na 200/70/35) to
test peak firing-rate shortfall</strong> (S-0024-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0024_port_de_rosenroll_2026_dsgc](../../tasks/t0024_port_de_rosenroll_2026_dsgc/)

Peak firing rate is 5.15 Hz in t0024 versus the paper's qualitative ~30-40 Hz and the t0004
envelope of 40-80 Hz. The paper text and the companion repository disagree on Ra, eleak, and
Na/K densities; the repository values were used as authoritative. Run a 2x2x3 sensitivity
sweep varying Ra (100/200), eleak (-60/-65), and Na density regime (code/paper/intermediate)
with 10 trials per condition at PD/ND to isolate which single parameter change recovers peak
rate without destroying DS. Scorer: t0012 tuning_curve_loss against the t0004 envelope.

</details>

<details>
<summary>🧪 <strong>Overlay a Van Wart + Werginz AIS on the deRosenroll morphology
to test peak-rate recovery</strong> (S-0024-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0024_port_de_rosenroll_2026_dsgc](../../tasks/t0024_port_de_rosenroll_2026_dsgc/)

Research-internet gap 2 showed that the upstream repository has no explicit AIS section, but
research-papers (Werginz 2020, Van Wart 2007) pins the AIS-to-soma Na ratio at ~7x and names
AIS length as the dominant predictor of maximum sustained firing rate. Fork t0024 into a new
library asset, add a two-subsegment AIS (proximal Nav1.2/Nav1.1, distal Nav1.6 + Kv1.2) with
Na ratio 7x and AIS length 25-50 um, rerun the 8-direction correlated/uncorrelated protocol,
and compare peak firing rate and HWHM to the t0024 baseline. Does not require rebuilding the
SAC network.

</details>

<details>
<summary>🧪 <strong>Add NMDA-block and TTX-sensitivity sweeps at each V_rest to
isolate biophysical mechanism</strong> (S-0026-06)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-21 | **Source**:
[t0026_vrest_sweep_tuning_curves_dsgc](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/)

Our V_rest sweep shows t0022 loses tuning at depolarised V_rest (DSI 0.046 at V=-30 mV) while
t0024 stays flat (DSI>=0.36). Two candidate mechanisms are Na channel inactivation and NMDA
Mg-block relief. Run the sweep once with TTX-like Na-block (g_Na=0) and once with NMDA-block
(g_NMDA=0) to isolate which channel class drives each model's V_rest sensitivity.

</details>

<details>
<summary>🧪 <strong>Extend sweep upward to V_rest in {-15, -10, -5} mV to capture the
post-collapse regime in t0024</strong> (S-0026-07)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-21 | **Source**:
[t0026_vrest_sweep_tuning_curves_dsgc](../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/)

Model t0022 peak firing collapses from 129 Hz at V=-30 to 26 Hz at V=-20 due to Na
inactivation, but t0024 still rises monotonically to 7.6 Hz at V=-20 with no collapse.
Extending the t0024 sweep to V_rest >= -20 mV would reveal whether t0024 also exhibits a
Na-inactivation collapse (suggesting shared mechanism at higher depolarisations) or remains
depolarisation-insensitive (suggesting NMDA-dominated signalling).

</details>

<details>
<summary>🔧 <strong>Calibrate active Nav / Kv / Ih densities to match Poleg-Polsky
2016 spike shape and distal Ih sag</strong> (S-0009-03)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0009_calibrate_dendritic_diameters](../../tasks/t0009_calibrate_dendritic_diameters/)

Geometry alone does not recover the Schachter Rin targets; the residual gap needs active and
passive membrane parameters. On dsgc-baseline-morphology-calibrated, install Fohlmeister-like
Nav, delayed-rectifier Kv, and Ih channels and fit their densities (somatic vs dendritic) so
that (1) the somatic action-potential shape (halfwidth, peak, afterhyperpolarisation) matches
Poleg-Polsky 2016 Figure 2, and (2) the voltage-sag response to hyperpolarising current at
distal tips matches the Ih-driven sag amplitude reported in Schachter 2010. This is distinct
from S-0002-01 (DSI-maximising g_Na/g_K grid) and S-0002-02 (passive-vs-active DSI ablation):
it tunes channel densities against single-cell electrophysiological waveforms, not tuning
curves. Output: a library asset exposing the fitted mechanism list for reuse in the DSI
experiments. Recommended task types: experiment-run, feature-engineering.

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
<summary>🧪 <strong>Retrieve paywalled voltage-gated-channel PDFs via Sheffield
access and verify numerical priors</strong> (S-0019-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0019_literature_survey_voltage_gated_channels](../../tasks/t0019_literature_survey_voltage_gated_channels/)

Five voltage-gated-channel papers (Van Wart-Trimmer-Matthews 2006, Kole-Letzkus-Stuart 2007,
Fohlmeister & Miller 1997, Hu et al. 2009, Kole et al. 2008) are documented in
intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs through
Sheffield institutional access, update each paper asset's download_status to 'success',
replace summary Overview disclaimers with PDF-verified content, and cross-check the numerical
priors tabulated in the Nav/Kv Combinations Table of the answer asset (Nav1.6 V_half around
-45 mV, Nav1.2 V_half around -32 mV, AIS Nav gbar 2500-5000 pS/um2, Kv1 V_half -40 to -50 mV,
Fohlmeister-Miller alpha/beta coefficients at 22 degC, Q10 near 3) against the actual papers
before adopting them as tight compartmental-model fitting targets.

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
<summary>🧪 <strong>Factorial (g_Na, g_K) grid search on a DSGC compartmental model
to locate the DSI-maximising conductance ridge</strong> (S-0002-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
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
<summary>🧪 <strong>Validate custom khhchan.mod biophysics with a dedicated sanity
simulation</strong> (S-0007-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-19 | **Source**:
[t0007_install_neuron_netpyne](../../tasks/t0007_install_neuron_netpyne/)

The t0007 sanity sims only exercise NEURON's built-in hh mechanism. khhchan.mod is compiled as
a smoke test but its biophysics are never run. Add a short task that inserts khhchan on a
1-compartment soma, drives it with the same IClamp protocol, and compares the resulting trace
against the built-in hh to confirm the custom mechanism produces physiologically plausible
spikes before downstream retinal tasks depend on it.

</details>
