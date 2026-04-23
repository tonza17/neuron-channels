# Category: Cable Theory

Mathematical framework describing voltage spread in passive and active cables.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (10)](../papers/by-category/cable-theory.md) | [Answers
(2)](../answers/by-category/cable-theory.md) | [Suggestions
(15)](../suggestions/by-category/cable-theory.md) | [Datasets
(1)](../datasets/by-category/cable-theory.md)

---

## Papers (10)

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

## Tasks (4)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |
| 0015 | [Literature survey: cable theory and dendritic filtering](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) | completed | 2026-04-20 10:00 |
| 0016 | [Literature survey: dendritic computation beyond DSGCs](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) | completed | 2026-04-20 10:36 |
| 0027 | [Literature survey: modeling effect of cell morphology on direction selectivity](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) | completed | 2026-04-21 22:23 |

## Answers (2)

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

## Suggestions (13 open, 2 closed)

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
<summary>🔧 <strong>Inverse-fit three-bin dendritic radii against the Schachter 2010
proximal/distal input-resistance gradient</strong> (S-0009-01)</summary>

**Kind**: technique | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0009_calibrate_dendritic_diameters](../../tasks/t0009_calibrate_dendritic_diameters/)

The calibrated proximal Rin (0.52 MOhm) and distal Rin (54 MOhm) are far below Schachter
2010's 150-200 MOhm proximal and >1 GOhm distal targets because the pure-literature
Poleg-Polsky three-bin radii are not tuned to our cell. Keep the three-bin (primary / mid /
terminal) structure but treat the three radii as free parameters; fit them in a NEURON
passive-properties simulation (Ra=100 Ohm-cm, Rm fit jointly) so that soma Rin lands in
150-200 MOhm and distal-tip Rin >= 1 GOhm. Seed the optimiser with the Poleg-Polsky means
(3.694/1.653/0.439 um) and emit a corrections file that overrides
dsgc-baseline-morphology-calibrated with the fitted radii. Blocks downstream DSI reproductions
against Schachter's tree. Recommended task types: feature-engineering, experiment-run.

</details>

<details>
<summary>📊 <strong>Sensitivity analysis: re-run DSGC simulations under alternative
Strahler tie-break rules and bin boundaries</strong> (S-0009-05)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0009_calibrate_dendritic_diameters](../../tasks/t0009_calibrate_dendritic_diameters/)

The primary bin (33 compartments) is set by max_strahler_order = 5 under a max-child
tie-break; a min-child or NeuroM section-based convention can push max_order to 6 and
reclassify the current 33 primary compartments as mid, jumping proximal Rin by ~15%
(creative_thinking.md section F3, E1). Produce 3-4 sibling calibrated SWCs under alternative
tie-break rules (max-child, min-child, NeuroM section_strahler_orders, two-bin collapse) and
run the downstream DSGC passive simulation from S-0009-01 on each. Report DSI, preferred peak,
HWHM, and proximal/distal Rin per variant; quantify the sensitivity of downstream metrics to
the heuristic choice. This makes the tie-break choice reviewable rather than arbitrary.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>📚 <strong>Port the TREES-toolbox Rall 3/2 quaddiameter rule to a
pure-Python calibrator and compare against the Strahler bins</strong>
(S-0009-08)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0009_calibrate_dendritic_diameters](../../tasks/t0009_calibrate_dendritic_diameters/)

Rall's 3/2 power rule (r_parent^(3/2) = sum r_child^(3/2)) is the only biophysically
principled way to match impedance across a binary tree; our max-child Strahler bins have no
such guarantee. Implement TREES-toolbox's quaddiameter algorithm as ~80 lines of pure Python,
solve the system bottom-up from the 131 terminals with the Poleg-Polsky terminal mean fixed,
and produce a sibling asset dsgc-baseline-morphology-rall. Compare against the
Strahler-calibrated asset by per-branch axial resistance, total surface area, and
per-compartment radius deltas. Expected primary-radius shift ~15% (3.69 to ~3.1 um) at the
measured 2-way branching ratio. Creative_thinking.md section A2. Recommended task types:
write-library, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Retrieve paywalled cable-theory PDFs via Sheffield access and
verify numerical claims</strong> (S-0015-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-20 | **Source**:
[t0015_literature_survey_cable_theory](../../tasks/t0015_literature_survey_cable_theory/)

Five foundational cable-theory papers (Rall 1967, Koch-Poggio-Torre 1982, Mainen-Sejnowski
1996, Taylor 2000, Dhingra-Smith 2004) are documented in intervention/paywalled_papers.md but
were not downloaded. Retrieve their PDFs through Sheffield institutional access, update each
paper asset's download_status to 'success', replace summary Overview disclaimers with
PDF-verified content, and cross-check the numerical claims in the synthesis (electrotonic
length L ≈ 0.5-0.8, contrast thresholds 1.5% / 3.8%, ~60% gray-level loss) against the actual
papers.

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
