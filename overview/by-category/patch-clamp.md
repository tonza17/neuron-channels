# Category: Patch Clamp

Electrophysiological recording technique for measuring ionic currents in cells.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (31)](../papers/by-category/patch-clamp.md) | [Answers
(3)](../answers/by-category/patch-clamp.md) | [Suggestions
(24)](../suggestions/by-category/patch-clamp.md)

---

## Papers (31)

<details>
<summary>📖 <strong>Retinal ganglion cells encode the direction of motion outside
their classical receptive field</strong> — Riccitelli et al., 2025</summary>

| Field | Value |
|---|---|
| **ID** | `10.1073_pnas.2415223122` |
| **Authors** | Serena Riccitelli, Hadar Yaakov, Alina S. Heukamp, Lea Ankri, Michal Rivlin-Etzion |
| **Venue** | Proceedings of the National Academy of Sciences (journal) |
| **DOI** | `10.1073/pnas.2415223122` |
| **URL** | https://www.pnas.org/doi/10.1073/pnas.2415223122 |
| **Date added** | 2026-05-04 |
| **Categories** | [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1073_pnas.2415223122/summary.md) |

Riccitelli et al. ask whether direction selectivity in the mouse retina is restricted to the
canonical direction-selective ganglion cells, or whether it is also computed at the population
level by RGCs through the so-called extraclassical receptive field. They tackle this with
large-scale ex vivo MEA recordings of dorsal mouse retinas plus complementary in vivo
Neuropixels recordings in the LGN, and supplement the recordings with static-bar mapping,
central-area occlusion masks, multiple bar speeds, glycinergic-amacrine pharmacology, and
gap-junction pharmacology.

Their methodology centres on a 350 um radius Central area mask that defines the classical RF
boundary and a Distancemin filter (450 um to retinal edge) that ensures every cell has a
measurable extraclassical annulus. Two motion-asymmetry metrics (mAI > 0.3, NVS > 0.15) plus
permutation shuffling identify the asymmetric PRE response. Static flashed bars locate the
asymmetric activation zone; centre masking dissociates desensitization from an inherent DS
component; strychnine and MFA reveal a wide-field-amacrine plus glycinergic plus gap-junction
circuit; multi-speed bars demonstrate speed invariance.

The headline findings are that **12.7%** of mouse RGCs (and a corresponding subset of LGN
neurons) encode motion direction outside their classical RF through an asymmetric activation
zone, that their preferred directions form a centripetal population code pointing toward the
optic disc, that direction tuning relies jointly on classical-RF desensitization and on an
inherent DS component inside the activation zone, and that glycinergic amacrine cells plus
gap-junction coupling are necessary for the full effect. The signal survives to dLGN, vLGN,
and IGL.

For this project, the paper is broader population-coding context rather than a direct model
target. The neuron-channels project simulates an explicitly direction-selective DRD4 ON-OFF
DSGC in NEURON, so Riccitelli et al. occupy a complementary niche; they describe DS
computations in non-DS RGCs that arise from circuit-level interactions outside any single
cell. The paper is relevant for framing the t0080 v3 substrate (single-DSGC model) within the
wider population-level direction-encoding literature, for noting that the 5-fold
AIS-Nav-density scaling debate concerns DRD4 DSGCs specifically rather than the broader RGC
population, and as a Zenodo data source if a later task ever needs out-of-DSGC RGC firing
benchmarks. It does not change the t0080 NSGA-II parameter bounds, the dendritic-spike
conductance ranges, or the AHP-tail metrics, but it strengthens the rationale for the project
narrow focus on the DRD4 cell type rather than generalising claims to RGC direction encoding
as a whole.

</details>

<details>
<summary>📖 <strong>A new role for excitation in the retinal direction-selective
circuit</strong> — Ankri et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.1113_JP286581` |
| **Authors** | Lea Ankri, Serena Riccitelli, Michal Rivlin-Etzion |
| **Venue** | The Journal of Physiology (journal) |
| **DOI** | `10.1113/JP286581` |
| **URL** | https://physoc.onlinelibrary.wiley.com/doi/10.1113/JP286581 |
| **Date added** | 2026-05-08 |
| **Categories** | [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../meta/categories/synaptic-integration/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0091_morphology_extended_nsga2_v1`](../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Full summary** | [`summary.md`](../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1113_JP286581/summary.md) |

Ankri, Riccitelli, and Rivlin-Etzion examine how prolonged photopic illumination reshapes the
receptive field and directional code of posterior-preferring On-Off direction-selective
ganglion cells (pDSGCs) in mouse retina. The standard textbook view, including the authors'
own prior work, attributes retinal direction selectivity to asymmetric inhibition from
starburst amacrine cells, with directional excitation either absent or attributed to
space-clamp artefact. The authors set out to test whether luminance-state changes that are
known to remodel centre-surround antagonism (Ankri 2020, Farrow 2013, Nath 2023) also
reorganise the directional code itself.

Methodologically the study combines two-photon-targeted loose-patch and whole-cell
voltage-clamp recordings from genetically labelled pDSGCs (Drd4-EGFP and Trhr-EGFP mice) with
252-electrode MEA recordings from wild-type retinas. Direction tuning is probed with 1 mm bars
that traverse the centre and surround sequentially, and receptive-field structure with
concentric spot stimuli. Two adaptation protocols are used (3-5.5 min of stationary photopic
light, or repetitive visual stimulation with drifting gratings). Pharmacology with SR95531,
strychnine, and L-AP4 dissects the GABAergic, glycinergic, and On-pathway contributions to the
unmasked surround excitation.

Light adaptation expands the pDSGC receptive field asymmetrically toward the preferred side
(asymmetry index On = **0.44** vs. Off = **0.15**), more than doubles the On spike-response
duration (**305 +/- 255 ms** -> **779 +/- 149 ms**, *P* = **1.96e-4**), and adds a delayed
null-direction-tuned spiking phase to the cell's normal preferred-direction main phase.
Voltage-clamp recordings show that the centre is driven by preferred-direction-tuned
excitation while the surround is driven by null-direction-tuned excitation; inhibition becomes
essentially symmetric. The phenomenon generalises across all four cardinal On-Off DSGC
subtypes in the MEA data.

For this project the paper has two consequences. First, it confirms that the classical
inhibition-dominated DS substrate that t0091's compartmental model implements is the correct
target for a non-light-adapted photopic 16-direction protocol but is one regime among at least
two; the answer asset should explicitly scope its biological-plausibility ceiling claims to
photopic, non-light-adapted conditions and acknowledge that the surround-direction-flipping
excitation is a separate axis the v3 substrate does not score against. Second, the published
**DSI-on = 0.70 +/- 0.25** and **DSI-off = 0.65 +/- 0.30** baseline values serve as a hard
biological reference for evaluating whether any t0091 Pareto cell that achieves extremely high
DSI is super-biological rather than realistic.

</details>

<details>
<summary>📖 <strong>Persistent sodium currents in neurons: potential mechanisms and
pharmacological blockers</strong> — Müller et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.1007_s00424-024-02980-7` |
| **Authors** | Peter Müller, Andreas Draguhn, Alexei V. Egorov |
| **Venue** | Pflügers Archiv - European Journal of Physiology (journal) |
| **DOI** | `10.1007/s00424-024-02980-7` |
| **URL** | https://link.springer.com/article/10.1007/s00424-024-02980-7 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0091_morphology_extended_nsga2_v1`](../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Full summary** | [`summary.md`](../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1007_s00424-024-02980-7/summary.md) |

Mueller, Draguhn, and Egorov publish a systematic review of persistent sodium current (INaP)
in CNS neurons in Pfluegers Archiv (Springer Nature, open access). The motivation is that INaP
is a clinically important regulator of excitability - implicated in epilepsy, amyotrophic
lateral sclerosis, neuropathic pain, hemiplegic migraine, and post-injury hyperexcitability -
but the literature is fragmented across heterogeneous voltage-clamp protocols, inconsistent
definitions of persistent versus slowly inactivating, and a sprawling catalogue of putative
blocker drugs whose specificities have never been compared head-to-head.

The review proceeds in two parts. The first part formalises four candidate mechanisms
(modified Hodgkin-Huxley window current; Markov gating with closed-state inactivation or modal
gating; subtype-specific generation by Nav1.1/1.2/1.3/1.6 plus beta1/beta4 modulation;
supra-molecular coupled gating) and four canonical voltage-clamp protocols (brief step,
entry-into-slow inactivation, slow steady-state inactivation, slow ramp). It explicitly maps
which protocol isolates which kinetic component, dissolving longstanding terminological
disagreements. The second part is a 22-drug catalogue (Table 1) tabulating IC50/EC50, holding
potential, preparation, protocol, and effects on INaP versus INaT for each substance.

The headline finding is that GS967 and riluzole are the only bona fide INaP blockers - they
act on the truly non-inactivating component across both brief-step and slow-ramp protocols at
clinically achievable concentrations and with limited off-target action. Phenytoin and
lacosamide are reclassified as selective enhancers of intermediate and slow inactivation
respectively, not INaP blockers proper. All other 18 surveyed substances are disqualified by
off-target Ca, K, GABA, or mGluR effects, by poor blood-brain-barrier penetration, or by
inadequate slow-inactivation data. The review concludes with a methodological recommendation:
combine brief steps, slow-inactivation steps, and slow ramps with TTX subtraction, and require
concordant effects of two drugs or a dynamic-clamp control before claiming an INaP role for
any physiological phenomenon.

For this project, the review most important message is a negative one: there is no
DSGC-specific INaP density measurement in the surveyed literature, so the cortical-pyramidal
Stuart 1999 / Astman 2021 priors used in t0086 / t0088 / t0091 remain the best cross-cell
baseline and the morphology-extended NSGA-II distal-NaP density bounds do not need to be
revised. The methodological caution that slow ramps underestimate INaP is a prior to keep on
file for any future patch-clamp validation step but does not affect the present in-silico
NEURON-based optimisation pipeline. The drug catalogue is a useful reference if the project
ever extends into dynamic-clamp INaP-cancellation experiments, where riluzole-equivalent block
at 10 uM is the canonical reference manipulation.

</details>

<details>
<summary>📖 <strong>Differential Intrinsic Firing Properties in Sustained and
Transient Mouse αRGCs Match Their Light Response Characteristics and
Persist during Retinal Degeneration</strong> — Werginz et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.1592-24.2024` |
| **Authors** | Paul Werginz, Viktoria Király, Guenther Zeck |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.1592-24.2024` |
| **URL** | https://www.jneurosci.org/content/45/2/e1592242024 |
| **Date added** | 2026-05-03 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/summary.md) |

Werginz, Kiraly, and Zeck (2024) ask whether the spike generator of mouse alpha-RGCs is itself
tuned to each cell type downstream computational role, or whether sustained-vs-transient
firing phenotypes arise purely from upstream synaptic circuitry. They isolate the spike
generator pharmacologically, record from 73 wild-type and 48 rd10-degenerate alpha-RGCs across
three subtypes (alpha-ON sustained, alpha-OFF sustained, alpha-OFF transient), and quantify
nine spike-shape and firing-pattern features per cell.

The methodology combines whole-cell current-clamp recordings (with all major synaptic
transmission blocked) and a five-tier compartmental NEURON model. The model partitions an
alpha-RGC into dendrites, soma, soma-AIS, AIS, and axon, each with its own densities of Nav,
Kv, Cav, K(Ca), Ih, and leak - all calibrated to mouse rather than the historical rat/cat
parameter sets. AIS densities are particularly high (1300 mS/cm^2 Nav, 800 mS/cm^2 Kv),
establishing the AIS as the dominant spike-generation locus. UMAP + GMM clustering of the
spike-feature vectors achieves an adjusted Rand index of 0.8 against the morphological
cell-type labels.

The paper finds that the three alpha-RGC types differ substantially in intrinsic spike output:
alpha-OFF transient cells have the shortest spikes (**0.21 ms** vs **0.31 ms** for alpha-ON
sustained), the lowest sustained-to-peak ratio (**0.32** vs **0.57**), and the highest peak
firing rates (**346 Hz** vs **278 Hz**). The compartmental model reproduces these differences
via small modulations of AIS Nav density and somatic leak conductance. Crucially, the same
firing-type distinctions persist in rd10 photoreceptor-degenerated retina up to p227,
demonstrating that alpha-RGC intrinsic properties are circuit-independent once established.

For the t0078 multi-tier MOBO project, this paper is the most directly load-bearing source we
have seen for the 49-dimensional parameter-space tier bounds. The Werginz Table 1 densities
provide mouse-specific central tendencies for all six channels across all five compartments;
the soma-vs-AIS ratios (17.3x Nav, 16.7x Kv) and the dendritic Ih (1.30x somatic) define the
tier stratification structure that t0078 was designed around. The within-cell-type variance
also provides empirical sigma values for the prior, replacing the previously assumed values
lifted from Fohlmeister 2010. The model demonstration that +/- 20% modulation of AIS Nav and
somatic leak suffices to reproduce sustained-vs-transient differences provides a tight prior
for the most important search dimensions and justifies narrower bounds on K(Ca) and Cav,
freeing search budget for the high-leverage parameters.

</details>

<details>
<summary>📖 <strong>Voltage Clamp Errors During Estimation of Concurrent Excitatory
and Inhibitory Synaptic Input to Neurons with Dendrites</strong> — To et
al., 2022</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuroscience.2021.08.024` |
| **Authors** | Minh-Son To, Suraj Honnuraiah, Greg J. Stuart |
| **Venue** | Neuroscience (journal) |
| **DOI** | `10.1016/j.neuroscience.2021.08.024` |
| **URL** | https://www.sciencedirect.com/science/article/abs/pii/S0306452221004322 |
| **Date added** | 2026-04-20 |
| **Categories** | [`patch-clamp`](../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |
| **Added by** | [`t0017_literature_survey_patch_clamp`](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuroscience.2021.08.024/summary.md) |

To, Honnuraiah, and Stuart address a direct extension of the Poleg-Polsky and Diamond 2011
analysis: how much additional voltage-clamp error is introduced by active dendritic
voltage-gated channels, which are present in every real neuron and absent from the
passive-dendrite 2011 simulations? Using detailed NEURON compartmental models with realistic
reconstructed morphologies and distributed voltage-gated Na+ and K+ channels, they run the
standard multi-holding-potential E/I decomposition protocol and compare the recovered
conductance waveforms against ground truth.

The design systematically isolates the contribution of active channels by comparing matched
models with and without the voltage-gated conductances. Synaptic placement, timing, and
holding-potential range are varied to map which experimental conditions drive the largest
errors. The paper quantifies what prior work had identified as a qualitative caveat.

The results are unambiguous: active dendritic channels substantially worsen the decomposition
error beyond the passive case, and under some conditions produce physically impossible
negative inhibitory conductance estimates. There is no holding-potential choice that is
globally accurate; the experimenter is forced to trade Ge accuracy against Gi accuracy. The
recommended mitigation (blocking active channels with TTX and K+ blockers) has its own cost
because it removes the circuit dynamics being studied.

For this project, the implication is cumulative with the Poleg-Polsky result. Every published
DSGC voltage-clamp E/I trace we will use to calibrate our NEURON model has been distorted by
both passive cable attenuation and active dendritic processing. Our modelling pipeline must
model both: the simulated voltage-clamp block must include dendritic active channels, and we
must expect substantially larger calibration uncertainty on distal synaptic conductance
amplitudes than the Poleg-Polsky bounds alone would suggest.

</details>

<details>
<summary>📖 <strong>Differences in spike generation instead of synaptic inputs
determine the feature selectivity of two retinal cell types</strong> —
Wienbar & Schwartz, 2022</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2022.04.012` |
| **Authors** | Sophia Wienbar, Gregory William Schwartz |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2022.04.012` |
| **URL** | https://www.cell.com/neuron/fulltext/S0896-6273(22)00357-9 |
| **Date added** | 2026-05-03 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1016_j.neuron.2022.04.012/summary.md) |

Wienbar and Schwartz introduce the Bursty Suppressed-by-Contrast (bSbC) RGC of the mouse
retina and ask why it transmits a contrast-suppression signal while the OFF sustained Alpha
(OFFsA) RGC, which receives nearly identical synaptic input, transmits a high-rate
sustained-contrast signal. The paper's research question is therefore explicitly about the
contribution of cell-intrinsic spike generation machinery, rather than upstream circuitry, to
RGC feature selectivity.

The methodology combines voltage-clamp measurement of excitatory and inhibitory conductance
traces, current-clamp recordings of spike shape, confocal imaging of the AIS labelled with
ankyrin-G, sodium-channel pharmacology with the Nav1.6-selective blocker 49TTX, and a NEURON
7.7 compartmental model in which the AIS is split into a proximal Nav1.2 subsegment and a
distal Nav1.6 subsegment. The two cell types share the same dendritic and somatic architecture
in the model, and the only systematic differences are AIS length (22 +/- 1.7 um in OFFsA vs 16
+/- 1.5 um in bSbC) and Nav1.6 fraction (~40 percent in OFFsA vs ~0 percent in bSbC).

The headline finding is that the divergent contrast response functions of the two cells emerge
from the spike generator alone. The bSbC cell's short, Nav1.2-dominated AIS is driven into
depolarisation block by strong contrast inputs, silencing the cell, while OFFsA's longer
Nav1.6-rich AIS sustains high firing rates under the same drive. 49TTX selectively reduces
OFFsA spike amplitude with no effect on bSbC, confirming the Nav1.6 contribution. AIS length
differs significantly (p = 0.018) while diameter does not (p = 0.83), localising the
anatomical signature.

For task t0078 (and the broader project) the paper matters in three ways. First, it provides a
public, openly licensed NEURON model of a two-subsegment AIS with realistic Nav1.2/Nav1.6
parameterisation, length 16-22 um, and diameter ~1.3 um, archived at Zenodo DOI
10.5281/zenodo.6423531. This is the substrate that t0078 is going to port in place of the
paywalled Werginz 2020 model. Second, it establishes that AIS heterogeneity is an empirically
documented driver of RGC feature selectivity, not just a modelling convenience, which
strengthens the biological-plausibility case for tiered AHP plus tiered AIS in the DSGC v2
model. Third, it demonstrates depolarisation block as a meaningful coding mechanism, which
means t0078's firing-rate metrics need to remain well-defined when the AIS enters block under
strong drive.

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
<summary>📝 <strong>Electrical match between initial segment and somatodendritic
compartment for action potential backpropagation in retinal ganglion
cells</strong> — Goethals et al., 2020</summary>

| Field | Value |
|---|---|
| **ID** | `10.1101_2020.09.15.297937` |
| **Authors** | Sarah Goethals, Martijn C. Sierksma, Xavier Nicol, Annabelle Réaux-Le Goazigo, Romain Brette |
| **Venue** | bioRxiv (preprint) |
| **DOI** | `10.1101/2020.09.15.297937` |
| **URL** | https://www.biorxiv.org/content/10.1101/2020.09.15.297937v2 |
| **Date added** | 2026-05-04 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |
| **Added by** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1101_2020.09.15.297937/summary.md) |

Goethals et al. study the biophysical organization of the axon initial segment in mouse
retinal ganglion cells, addressing how a narrow (~1 um diameter) structure reliably transmits
the action potential to the much larger soma. The AIS must produce an axial current strong
enough to depolarize the soma by ~30 mV to reach somatic spike regeneration threshold, a
demanding requirement given the geometric impedance mismatch at the axosomatic junction. Prior
estimates of AIS Nav conductance density in RGCs came only from computational model fitting to
AP shape; this paper provides the first direct functional measurement via the axial current
itself.

The approach combines whole-cell voltage-clamp measurement of the axial current with post-hoc
ankyrin-G immunolabeling to measure AIS geometry in each recorded cell (P10-12 mouse retina, n
= 14-17 cells). Resistive coupling theory is applied to these paired measurements to estimate
AIS Nav conductance density. Additionally, the adaptation of the axial current with membrane
potential is characterized, revealing that temporal broadening by Kv1 channel inactivation
reduces effective charge attenuation from 12-fold (peak current) to only 3-fold (total charge)
over a 20 mV depolarization.

Key quantitative results: mean axial current **-6.7 +/- 1.8 nA**; minimum Nav conductance
density from cable theory **~1200 S/m2 (d = 1 um)** or **~2467 S/m2 (d = 0.8 um)**; best-fit
from resistive coupling theory **~5000-5500 S/m2 (50-55 mS/cm2)**; charge-capacitance slope
**31 mV** matching the spike-to-regeneration gap; **12-fold peak current** versus **3-fold
charge attenuation** over 20 mV depolarization. These converge with Guo et al. 2013 model
estimates (5000 S/m2) and Werginz 2020 Sci. Adv. values (~1300 mS/cm2).

For t0080, this paper provides an independent empirical lower bound on AIS Nav density in
mouse RGCs supporting the hard biological floor nav16_ais >= 0.25 S/cm2. The conservative
minimum (~10-12.6 mS/cm2) exceeds this floor by ~40-50x; the best-fit (~50-55 mS/cm2) by
~200x, confirming the floor is conservative. The paper establishes that AIS diameter is a
critical free parameter (0.7-1.2 um proximal range from measurements) and that the charge-
capacitance coupling principle should inform how AIS geometry bounds are set relative to soma
size in t0080 MOBO optimization.

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
<summary>📖 <strong>Dynamic Tuning of Electrical and Chemical Synaptic Transmission
in a Network of Motion Coding Retinal Neurons</strong> — Trenholm et al.,
2013</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.0808-13.2013` |
| **Authors** | Stuart Trenholm, Amanda J. McLaughlin, David J. Schwab, Gautam B. Awatramani |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.0808-13.2013` |
| **URL** | https://www.jneurosci.org/content/33/37/14927 |
| **Date added** | 2026-05-03 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/summary.md) |

This paper asks how a network of mouse retinal direction-selective ganglion cells (DSGCs)
combines weak electrical coupling, chemical synapses, and intrinsic membrane properties to
produce direction-tuned, anticipatory responses without runaway excitation. The motivation is
that earlier work (Trenholm et al. 2013, Nat. Neurosci.) had shown that the same
Hb9::eGFP-labelled superior- coding DSGCs perform "lag normalisation" - they detect a moving
edge at the same retinal location regardless of speed - but the mechanistic basis for the
asymmetric, leading-edge-skewed response underlying that computation was unknown.

The methodology pairs Neurobiotin tracer-coupling, two-photon-targeted whole-cell and
cell-attached patch-clamp from single and paired DSGCs, voltage- and current-clamp
characterisation of gap junctions (TTX, 18-beta-glycyrrhetinic acid), receptive-field mapping
with stationary spots and moving bars, and pharmacological dissection of GABAergic inhibition
with picrotoxin and intrinsic gain control with preconditioning current pulses. The key design
choice is to distinguish three mutually exclusive explanations for response skew -
gap-junction rectification, GABAergic inhibition, intrinsic gain control - and test each
independently.

The headline findings are: (i) only Hb9+ (superior-coding) DSGCs are strongly coupled, with ~1
nS symmetric reciprocal gap junctions and ~10 Hz low-pass filtering; (ii) gap junctions
provide a ~50-100 um subthreshold excitatory surround that primes coincident chemical synaptic
input, extending the effective receptive field and producing leading-edge-skewed motion
responses (SI **1.6 +/- 0.1** vs **1.1 +/- 0.1** in uncoupled cells); (iii) the leading-edge
skew survives picrotoxin in both preferred and null directions, ruling out GABA as the sole
cause; (iv) preconditioning spike trains attenuate initial-response spikes by **70 +/- 6%**
and abolish skew, with **tau ~604 ms** recovery, implicating activity-dependent intrinsic gain
control as the dominant rectifying mechanism. Reported peak rates are **198 +/- 14 Hz**
(preferred, control), **27 +/- 12 Hz** (null, control), and **244 +/- 18 Hz** / **202 +/- 14
Hz** under picrotoxin.

For this project, the paper is a primary literature anchor for the firing-rate target of
Hb9::eGFP mouse DSGCs and clarifies a critical interpretation issue: the project
domain-knowledge "30-80 Hz" preferred-direction figure most likely originates from mean /
trial-averaged rates (consistent with Rivlin-Etzion et al. 2012's ~10 Hz), whereas this
paper's 198 Hz preferred and 27 Hz null are peak rates from Gaussian-convolved spike trains,
and the corresponding peak-rate DSI is 0.76. The MOBO objective for the AIS-tiered AHP task
should explicitly state which metric (peak vs mean) it targets to avoid mixing scales. The
paper also constrains AIS / soma model choices: a realistic Hb9 DSGC model needs slow (~600
ms) intrinsic gain control (Na slow inactivation or Ca-activated K), spatially offset GABA
inhibition (~52 um null-side, E_GABA near -60 mV), and weak symmetric reciprocal gap-junction
coupling - all properties that bias which ion-channel parameter sets and AHP regimes can
simultaneously hit the peak-rate target and the DSI target.

</details>

<details>
<summary>📖 <strong>Visual Stimulation Reverses the Directional Preference of
Direction-Selective Retinal Ganglion Cells</strong> — Rivlin-Etzion et
al., 2012</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2012.08.041` |
| **Authors** | Michal Rivlin-Etzion, Wei Wei, Marla B. Feller |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2012.08.041` |
| **URL** | https://www.cell.com/neuron/fulltext/S0896-6273(12)00807-0 |
| **Date added** | 2026-05-03 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../meta/categories/patch-clamp/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1016_j.neuron.2012.08.041/summary.md) |

Rivlin-Etzion, Wei, and Feller (2012, Neuron) ask whether the direction-selective response of
mouse ON-OFF retinal ganglion cells is rigidly determined by the asymmetric SAC-DSGC wiring
revealed by EM reconstruction, or whether it can be reshaped by recent visual experience.
Their work targets the dominant "hardwired retina" view of direction selectivity and tests it
directly by applying brief drifting-grating adaptation protocols and measuring whether DSGC
preferred direction remains stable.

The methodology combines two-photon-targeted loose-patch recordings from genetically labelled
posterior-preferring ON-OFF DSGCs (DRD4-GFP and TRHR-GFP lines, P14-P88, both sexes) with
whole-cell voltage clamp to dissect synaptic mechanisms, plus pharmacology with gabazine to
test GABA-A involvement and L-AP4 to test ON-pathway involvement. Directional tuning is
quantified with DSI and vector-sum metrics computed from 3 s grating responses in 12
directions, using a pre/adaptation/post design with four adaptation protocols (P-N, Null, P-O,
counter-phase) plus a no-stimulus control.

The authors find that drifting-grating adaptation can fully reverse the PD of a substantial
fraction of ON-OFF DSGCs (41% of 74 cells across protocols) and that this reversal is robust,
long-lasting (persisting up to 23 min), GABA-A dependent, and mediated by a redistribution of
asymmetric inhibition rather than by new wiring. ON-pathway crossover circuits are necessary
for the reversal: L-AP4 blockade reduces reversal probability and reveals a delayed OFF
response normally masked by the ON pathway. Critically, the paper reports paired DSI plus mean
preferred-direction firing rate from the same cells: **DSI 0.78 +/- 0.19 with mean PD rate
10.38 +/- 8.53 Hz** for stable cells (n = 8\) and **DSI 0.63 +/- 0.23 with 9.95 +/- 5.42 Hz**
for reversed cells (n = 8), measured over the 3 s grating window.

For task t0078, this paper is the primary literature anchor for revising the project's pass
criterion from "PD rate >= 30 Hz" to "PD rate >= 10 Hz". The previously assumed 30-80 Hz mean
PD firing rate range conflated peak rates over sub-second windows with mean rates over
multi-second windows; this paper establishes that the mean PD firing rate of mouse ON-OFF
DSGCs is approximately 10 Hz when measured over a 3 s window, with paired DSI of 0.78. The
result also informs the Bayesian-optimisation utopia point used to compute hypervolume in
t0078 and downstream model selection. A secondary implication for downstream tasks is that
DSGC tuning is plastic on a minutes timescale, so model-fitting tasks should treat
pre-adaptation values as the canonical target and not aggregate them with post-adaptation
states.

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
<summary>📖 <strong>The Contribution of Resurgent Sodium Current to High-Frequency
Firing in Purkinje Neurons: An Experimental and Modeling Study</strong>
— Khaliq et al., 2003</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.23-12-04899.2003` |
| **Authors** | Zayd M. Khaliq, Nathan W. Gouwens, Indira M. Raman |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.23-12-04899.2003` |
| **URL** | https://www.jneurosci.org/content/23/12/4899 |
| **Date added** | 2026-05-03 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../meta/categories/patch-clamp/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.23-12-04899.2003/summary.md) |

Khaliq, Gouwens, and Raman (2003) ask whether and how the resurgent component of NaV1.6 sodium
current promotes high-frequency action-potential firing in cerebellar Purkinje neurons. The
question matters because resurgent current - sodium current that flows when the channel exits
an open-channel-block state during repolarisation - is a peculiar, structurally distinctive
feature of NaV1.6 that had been correlated with rapid firing but never causally attributed to
it. The authors scope is somatic firing in dissociated Purkinje cells from wild-type and
Scn8a-med mice; they hold dendrites and synaptic input out of the analysis to focus on
intrinsic excitability.

Methodologically, the paper combines whole-cell current-clamp action-potential recordings from
acutely dissociated Purkinje somata with voltage-clamped pharmacological isolation of seven
non-sodium currents (Kfast, Kmid, Kslow, BK, Pca, Ih, leak) and a NEURON-based
single-compartment model that integrates these seven currents with an explicit Raman-Bean
state-machine model of NaV1.6 sodium current. The med phenotype - which lacks NaV1.6 and
therefore has 90 percent reduced resurgent current - is used as a natural knockout. The model
is validated by reproducing wild-type spontaneous firing at 27 spikes/sec (matching the 29 Hz
experimental mean) and is then used to ask which of the changes seen in med cells (lost
resurgent current, modified Kfast V1/2, reduced leak) actually drive the slower firing.

The headline finding is that resurgent kinetics specifically and consistently accelerate
firing. Med cells fired at 9 +/- 2 Hz spontaneously vs 35 +/- 4 Hz wild-type, and at 13 +/- 5
vs 65 +/- 7 spikes/sec under 50 pA injection, a deficit that survived even strong current
injection (maximum sustained rate 65 +/- 10 spikes/sec med vs 107 +/- 6 wild-type). Crucially,
the model showed that the small Kfast V1/2 shift and reduced leak found in med cells would, if
anything, **speed** firing \- so the observed slowdown must come from the sodium-channel
kinetics. Replacing wild-type with med-like Na kinetics in the model slowed simulated firing
by 19-31 percent, reproducing the experimental phenotype.

For the present project this paper is the kinetic foundation of the BedB substrate
voltage-gated channel library. The bkpkj.mod calcium-activated K channel and the NaR resurgent
sodium mod-file vendored in t0074 trace directly to this paper Equation-1 state model and
Table 1 parameter set. For t0078 specifically, the AIS-tiered NaR optimization treats this
paper kinetic schemes as the fixed scaffold and varies only channel density per tier - so any
biological plausibility argument about NaR density gradients ultimately rests on the parameter
ranges established here. The paper 19 pF single-compartment geometry also provides a minimal
regression-test target: vendored mod-files should reproduce ~27 Hz spontaneous firing in that
geometry before being deployed on the multi-compartment DSGC substrate.

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

## Tasks (8)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |
| 0013 | [Resolve dsgc-baseline-morphology source-paper provenance](../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) | completed | 2026-04-20 17:21 |
| 0017 | [Literature survey: patch-clamp recordings of RGCs and DSGCs](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) | completed | 2026-04-20 11:08 |
| 0019 | [Literature survey: voltage-gated channels in retinal ganglion cells](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) | completed | 2026-04-20 13:00 |
| 0027 | [Literature survey: modeling effect of cell morphology on direction selectivity](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) | completed | 2026-04-21 22:23 |
| 0078 | [Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) | completed | 2026-05-04 16:25 |
| 0080 | [Bed B v3 MOBO with dendritic-spike machinery and NSGA-II](../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) | completed | 2026-05-04 22:45 |
| 0091 | [First joint 68-d NSGA-II with morphology in eval loop, 5-anchor warm-start](../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) | completed | 2026-05-08 15:55 |

## Answers (3)

<details>
<summary><strong>Why did the t0078 BoTorch qLogNEHVI MOBO collapse `nav16_ais` to
the search-space floor (1e-5 S/cm^2) at iter 81, and what biological-prior
checklist prevents this failure mode in future MOBO-on-biophysics
tasks?</strong></summary>

**Confidence**: high | **Date**: 2026-05-04 | **Full answer**:
[`mobo-on-biophysics-ais-disabled-corner`](../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/answer/mobo-on-biophysics-ais-disabled-corner/)

The optimiser exploited a soft-prior loophole. t0078's per-tier search bounds let `nav16_ais`
go as low as 1e-5 S/cm^2, four orders of magnitude below Kole 2008's measured cortical AIS Nav
range [0.25, 0.5] S/cm^2 and five orders below Werginz 2024's mouse alpha-RGC measurement of
1.3 S/cm^2. Multi-objective acquisition discovered that an AIS-disabled cell could match a
fragment of the Pareto front (DSI 0.316, PD 9.68 Hz at iter 81) at a lower implicit cost than
a Kole-compliant cell, because the prior was advisory rather than enforced. The fix is hard
parameter bounds, not soft penalties: pre-register `nav16_ais >= 0.25` S/cm^2 (Kole 2008) and
AIS-to-soma Nav ratio `>= 5` (Werginz 2024) as inviolable constraints, plus equivalent priors
on every biophysical parameter where measurement-grounded ranges exist.

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

## Suggestions (20 open, 4 closed)

<details>
<summary>📊 <strong>Peak-rate re-analysis of cells 1559 / 1677 for direct comparison
with Trenholm 2013 / Oesch 2005</strong> (S-0083-06)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-06 | **Source**:
[t0083_bedb_v3_extend_nsga2_gen8plus](../../tasks/t0083_bedb_v3_extend_nsga2_gen8plus/)

Cells 1559 (DSI 0.706 / PD 39.18 Hz) and 1677 (DSI 0.657 / PD 40.71 Hz) are the project's
first cells to combine biologically-plausible DSI with PD firing rates above 30 Hz mean.
Published `[Trenholm2013, Results p. 14064]` and `[Oesch2005, Results p. 754]` report peak
rather than mean PD rates: 198 Hz Gaussian-convolved peak (Trenholm) and 148 Hz modal peak
(Oesch). The current PD-rate metric is mean rate over 1400 ms; converting cells 1559 / 1677 to
peak rate would resolve the mean-vs-peak metric mismatch and enable direct numerical
comparison with Trenholm / Oesch. Re-run cells 1559 and 1677 in subprocess with
full-resolution voltage / spike traces preserved, compute Gaussian-convolved instantaneous
rates with sigma = 25 ms over a 1400 ms window, report peak rate over the PD direction.
Recommended task types: data-analysis (no new simulator runs needed if traces from t0083 are
preserved; otherwise experiment-run with 2-cell budget < $0.20).

</details>

<details>
<summary>📊 <strong>Investigate AIS-disabled-corner exploitation as a general
MOBO-on-biophysics failure mode</strong> (S-0078-08)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-04 | **Source**:
[t0078_bedb_mobo_v2_ais_tiered_ahp](../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/)

The t0078 compare_literature step found iter 81's nav16_ais collapsed to the search floor
(1e-5 S/cm^2), four orders below Kole 2008's [0.25, 0.5] S/cm^2 prior and five orders below
Werginz 2024's mouse alpha-RGC value of 1.3 S/cm^2. AIS-to-soma Nav ratio at iter 81 was
5.5e-5 vs Werginz 2024's measured 17.3. The optimiser found a configuration where the AIS
contributes nothing to spike initiation, contradicting REQ-2 / REQ-3 / REQ-4's biological
intent. This may be a generalisable MOBO-on-biophysics failure mode. Document: (a) audit t0076
+ t0078 Pareto fronts for similar collapse-to-floor patterns on biologically-priored
parameters; (b) propose log-uniform priors with hard biological lower bounds as default for
future MOBO tasks; (c) write up as an answer asset. Pass: produce an answer asset with a
checklist of biological priors to enforce as hard constraints in future MOBO tasks.
Recommended task types: answer-question, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Tighten AIS-to-soma Nav ratio hard floor from >=5 to >=7
(matching Werginz 2020 RGC point estimate)</strong> (S-0080-07)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-04 | **Source**:
[t0080_bedb_mobo_v3_dendritic_spike_nsga2](../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/)

t0080 enforces an AIS-to-soma Nav ratio >= 5 hard floor, justified primarily by Werginz 2024's
measured 17.3x for mouse alpha-ON-sustained RGCs and a conservative interpretation of Werginz
2020's RGC ratio (~7x for mouse OFF-alpha-T RGCs, in metadata only because the PDF is
paywalled). Tighten the floor to >=7 to match the Werginz 2020 point estimate and re-run
NSGA-II at the same pop=24 / gen=8 budget. The hypothesis is that the >=5 floor still permits
configurations near the AIS-disabled corner that contribute to the t0080 Pareto compression.
Compare Pareto-front geometry and joint-closest distance against t0080's >=5 result. Cost
~$0.75. Recommended task types: experiment-run.

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
<summary>🧪 <strong>Resolve inhibitory conductance time-course via SEClamp on the
deposited cell</strong> (S-0065-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0065_t0020_epsp_ipsp_vm_protocol](../../tasks/t0065_t0020_epsp_ipsp_vm_protocol/)

t0065 IPSP_PASSIVE traces are flat at e_SACinhib = -60 mV because the cell sits at the
inhibitory reversal under no excitation. The voltage trace cannot reveal the inhibitory
conductance time-course; only a voltage clamp can resolve g_inh(t). t0049 already has SEClamp
infrastructure for this cell. Combining the t0065 channel-isolation pattern (zero excitatory
drives via b2gampa = b2gnmda = s2gach = achMOD = 0) with a SEClamp at -65 mV (or any
non-equilibrium voltage offset from e_SACinhib) would resolve the inhibitory conductance in nS
as a function of time, separately for PD (gabaMOD = 0.33) and ND (gabaMOD = 0.99). This is
essential for quantifying the differential shunting magnitude that drives FULL-mode DSI: the
integral of g_inh(t) should be ~3x larger in ND than in PD. Expected output: two conductance
time-courses showing g_inhibitory(t) over the 1000 ms trial in PD vs ND, with peak g_inh and
integrated charge per direction.

</details>

<details>
<summary>🧪 <strong>SEClamp inhibitory conductance measurement on de Rosenroll
cell</strong> (S-0066-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0066_t0024_epsp_ipsp_vm_protocol](../../tasks/t0066_t0024_epsp_ipsp_vm_protocol/)

Voltage trace cannot resolve g_inh(t) when e_GABA = v_rest (zero current at rest regardless of
g). For the de Rosenroll cell specifically, combine the t0066 channel-isolation pattern (set
ach NetCon weights = 0; HHst zeroed) with a SEClamp at -65 mV (or any non-equilibrium offset
from e_GABA = -60). This will read inhibitory current in pA across the trial separately for PD
(gaba_release_prob = 0.05) and ND (gaba_release_prob = 0.80). Expected: the time-integrated
charge in ND should be ~3-16x larger than in PD depending on how synapse-level release prob
translates to mean conductance. Reuses t0049's SEClamp infrastructure (which was developed for
the deposited cell — would need a small port for the de Rosenroll synapse model). Parallel to
S-0065-03 for the deposited cell; together they give cross-model conductance benchmarks.

</details>

<details>
<summary>🧪 <strong>GABA conductance scan under SEClamp toward paper PD 12.5 / ND
30 nS at fixed gNMDA = 0.5 nS</strong> (S-0049-02)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-25 | **Source**:
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
<summary>🧪 <strong>SEClamp Fig 3A-E re-measurement across multiple V_clamp levels
(-85, -65, -45 mV) to vary GABA driving force</strong> (S-0049-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-25 | **Source**:
[t0049_seclamp_cond_remeasure](../../tasks/t0049_seclamp_cond_remeasure/)

t0049 ran SEClamp at the single V_clamp = -65 mV which yields a small GABA driving force (-5
mV vs E_GABA = -60 mV) and amplifies noise on the GABA conductance estimate (SD +/- 1.98 nS at
PD). Repeat the per-channel isolation sweep at V_clamp in {-85, -65, -45} mV. The -85 mV
condition gives a 25 mV GABA driving force (5x improvement in GABA SNR) and inverts the
AMPA/NMDA driving force; the -45 mV condition reverses the GABA driving force sign and
increases NMDA Mg-block relief. Tests (a) whether the GABA PD/ND symmetry persists across
V_clamp (ruling out driving-force noise), (b) whether NMDA over-amplification depends on
holding voltage. Recommended task types: experiment-run.

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
<summary>🧪 <strong>Retrieve paywalled patch-clamp PDFs via Sheffield access and
verify numerical claims</strong> (S-0017-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
[t0017_literature_survey_patch_clamp](../../tasks/t0017_literature_survey_patch_clamp/)

Five patch-clamp / voltage-clamp / space-clamp papers (Poleg-Polsky & Diamond 2011, To et al.
2022, Werginz et al. 2020, Sethuramanujam et al. 2017, Margolis & Detwiler 2007) are
documented in intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs
through Sheffield institutional access, update each paper asset's download_status to
'success', replace summary Overview disclaimers with PDF-verified content, and cross-check the
numerical claims in the synthesis (~80% signal loss on thin distal dendrites, 7x AIS-to-soma
Na+ density ratio, AMPA/NMDA charge ratios during preferred and null motion, proportion of
OFF-cell maintained activity that survives synaptic blockade) against the actual papers.

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
<summary>📊 <strong>Reproduce Poleg-Polsky 2016 Fig 1D/H subthreshold validation
targets (PSP amplitude, NMDAR slope angle)</strong> (S-0020-02)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-20 | **Source**:
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
