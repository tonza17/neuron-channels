# Papers: `compartmental-modelling` (2)

2 papers across 2 year(s).

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

## 1996 (1)

<details>
<summary>📖 Influence of dendritic structure on firing pattern in model neocortical
neurons — Mainen & Sejnowski, 1996</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_382363a0` |
| **Authors** | Zachary F. Mainen, Terrence J. Sejnowski |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/382363a0` |
| **URL** | https://www.nature.com/articles/382363a0 |
| **Date added** | 2026-04-20 |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modelling`](../../../meta/categories/compartmental-modelling/) |
| **Added by** | [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0015_literature_survey_cable_theory/assets/paper/10.1038_382363a0/summary.md) |

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
