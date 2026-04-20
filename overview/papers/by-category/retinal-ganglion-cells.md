# Papers: `retinal-ganglion-cells` (3)

3 papers across 3 year(s).

[Back to all papers](../README.md)

---

## 2004 (1)

<details>
<summary>📖 Spike Generator Limits Efficiency of Information Transfer in a Retinal
Ganglion Cell — Dhingra & Smith, 2004</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_jneurosci.5346-03.2004` |
| **Authors** | Narender K. Dhingra, Robert G. Smith |
| **Venue** | Journal of Neuroscience (journal) |
| **DOI** | `10.1523/jneurosci.5346-03.2004` |
| **URL** | https://www.jneurosci.org/content/24/12/2914 |
| **Date added** | 2026-04-20 |
| **Categories** | [`retinal-ganglion-cells`](../../../meta/categories/retinal-ganglion-cells/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modelling`](../../../meta/categories/compartmental-modelling/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1523_jneurosci.5346-03.2004/summary.md) |

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

## 2000 (1)

<details>
<summary>📖 Dendritic Computation of Direction Selectivity by Retinal Ganglion Cells
— Taylor et al., 2000</summary>

| Field | Value |
|---|---|
| **ID** | `10.1126_science.289.5488.2347` |
| **Authors** | W. Rowland Taylor, Shigang He, William R. Levick, David I. Vaney |
| **Venue** | Science (journal) |
| **DOI** | `10.1126/science.289.5488.2347` |
| **URL** | https://www.science.org/doi/10.1126/science.289.5488.2347 |
| **Date added** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cells`](../../../meta/categories/retinal-ganglion-cells/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1126_science.289.5488.2347/summary.md) |

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

## 1982 (1)

<details>
<summary>📖 Retinal ganglion cells: a functional interpretation of dendritic
morphology — Koch et al., 1982</summary>

| Field | Value |
|---|---|
| **ID** | `10.1098_rstb.1982.0084` |
| **Authors** | Christof Koch, Tomaso Poggio, Vincent Torre |
| **Venue** | Philosophical Transactions of the Royal Society B (journal) |
| **DOI** | `10.1098/rstb.1982.0084` |
| **URL** | https://royalsocietypublishing.org/doi/10.1098/rstb.1982.0084 |
| **Date added** | 2026-04-20 |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`retinal-ganglion-cells`](../../../meta/categories/retinal-ganglion-cells/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1098_rstb.1982.0084/summary.md) |

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
