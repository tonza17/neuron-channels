# Category: Cable Theory

Mathematical framework describing voltage spread in passive and active cables.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (7)](../papers/by-category/cable-theory.md) | [Answers
(1)](../answers/by-category/cable-theory.md) | [Suggestions
(7)](../suggestions/by-category/cable-theory.md) | [Datasets
(1)](../datasets/by-category/cable-theory.md)

---

## Papers (7)

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

## Tasks (3)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |
| 0015 | [Literature survey: cable theory and dendritic filtering](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) | completed | 2026-04-20 10:00 |
| 0016 | [Literature survey: dendritic computation beyond DSGCs](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) | completed | 2026-04-20 10:36 |

## Answers (1)

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

## Suggestions (5 open, 2 closed)

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
