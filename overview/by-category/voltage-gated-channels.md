# Category: Voltage-Gated Channels

Ion channels whose opening probability depends on membrane voltage.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (30)](../papers/by-category/voltage-gated-channels.md) | [Answers
(10)](../answers/by-category/voltage-gated-channels.md) | [Suggestions
(97)](../suggestions/by-category/voltage-gated-channels.md) | [Libraries
(3)](../libraries/by-category/voltage-gated-channels.md) | [Predictions
(2)](../predictions/by-category/voltage-gated-channels.md)

---

## Papers (30)

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
<summary>📖 <strong>BluePyOpt: Leveraging Open Source Software and Cloud
Infrastructure to Optimise Model Parameters in Neuroscience</strong> —
Geit et al., 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.3389_fninf.2016.00017` |
| **Authors** | Werner Van Geit, Michael Gevaert, Giuseppe Chindemi, Christian Rossert, Jean-Denis Courcol, Eilif B. Muller, Felix Schurmann, Idan Segev, Henry Markram |
| **Venue** | Frontiers in Neuroinformatics (journal) |
| **DOI** | `10.3389/fninf.2016.00017` |
| **URL** | https://www.frontiersin.org/articles/10.3389/fninf.2016.00017/full |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/summary.md) |

This Technology Report introduces BluePyOpt, a Python package developed at the Blue Brain
Project to standardise the multi-objective evolutionary optimisation of neuroscience models.
The motivation is that while stochastic search methods like genetic algorithms and CMA-ES have
proven effective for fitting compartmental neuron models, configuring them correctly remains a
domain expertise problem that excludes most neuroscientists from the technique. BluePyOpt
addresses this by providing a reusable object-oriented API and turn-key cloud-deployment
scripts, lowering the barrier so that a working optimisation can be expressed in a short
Python script.

The framework wraps DEAP for the evolutionary algorithms (IBEA, NSGA-II, CMA-ES, PSO), NEURON
for electrophysiological simulation, and eFEL for feature extraction. Its core abstraction is
a clean separation between an `Optimisation` (the search algorithm), an `Evaluator` (the
parameter-to- objective mapping), and an `ephys` model layer (`CellModel`, `Morphology`,
`Mechanism`, `Protocol`, `Stimulus`, `Recording`, `eFELFeature`, `SingletonObjective`,
`ObjectivesCalculator`). Distance- dependent ion-channel distributions, parameter freezing,
holding currents, and back-propagating- AP protocols are all first-class API objects.
Parallelisation is handled by user-supplied `map` functions (Python, multiprocessing, SCOOP,
MPI4Py); Ansible playbooks automate AWS, Vagrant, and cluster deployment.

The paper validates the framework on three representative use cases. A single-compartment
Hodgkin-Huxley fit converges in 4 minutes on one CPU. A 18-parameter, 31-feature optimisation
of a layer-5 pyramidal cell reproduces the published Markram et al. 2015 model in
approximately 4 hours on 50 cores, recovering a diverse hall-of-fame of equally good
solutions. A 9-parameter calcium-based STDP model is fit to LTP/LTD curves from Nevian and
Sakmann (2006), demonstrating that the framework is not restricted to voltage-trace fitting.

For this project, BluePyOpt is the methodology backbone of the parameter-optimisation work.
The paper is the canonical citation for the project's chosen optimisation toolchain, sitting
alongside Druckmann et al. (2007) and Hay et al. (2011) as the methodological core. It
directly specifies the recommended adoption pattern: encode each project objective (DSI
matching, target firing rates, EPSP/IPSP amplitudes) as an `eFELFeature` plus
`SingletonObjective`, package the model as a `CellModel` with `Protocol` per stimulus
condition, and run IBEA or NSGA-II via DEAP. The L5PC compute budget and the reported
non-uniqueness of solutions also set practical expectations for this project's own
optimisation runs and for how to interpret their output as a population of
electrophysiological regimes rather than a single best individual.

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
<summary>📖 <strong>Action Potential Energy Efficiency Varies Among Neuron Types in
Vertebrates and Invertebrates</strong> — Sengupta et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1000840` |
| **Authors** | Biswa Sengupta, Martin Stemmler, Simon B. Laughlin, Jeremy E. Niven |
| **Venue** | PLOS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1000840` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000840 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/summary.md) |

Sengupta, Stemmler, Laughlin and Niven (2010) ask whether the per-action-potential energy cost
of biological neurons is set by waveform alone, or whether the underlying ionic currents allow
large cost differences hidden by similar AP shapes. They re-implement seven published
Hodgkin-Huxley single-compartment models spanning the squid giant axon, a crab leg motor
neuron, four mammalian neurons (mouse fast-spiking interneuron, rat hippocampal interneuron,
rat cerebellar granule cell, mouse thalamo-cortical relay) and a honeybee Kenyon cell, and
compare per-AP Na+ loads on a common, model-independent basis. The motivation is to establish
a principled per-cell-type energy metric that can serve as a bottom-up calibration anchor for
cortical energy budgets and for downstream modelers comparing their own neurons energy use to
literature.

The methodology is a deterministic single-compartment HH simulation driven by constant
injected current to elicit repetitive firing, with per-AP Na+ load computed by integrating the
inward Na+ current over one limit-cycle period. Cost is converted to ATP using the 3 Na+/ATP
stoichiometry of the Na+/K+ pump. The authors then introduce a five-parameter constrained
optimization (gNa, gK, tau_m, tau_h, tau_n) that combines a Nelder-Mead simplex with a
Newton-method hill climber, enforcing AP existence by a hard penalty and AP height by a soft
quadratic loss. Conductances and time constants are bounded to 30-400% of the original
published values. The same optimization is run across six of the seven models, and the changes
in parameters are compared.

The headline result is that the per-AP Na+ load varies 17-fold across the seven models, while
the capacitive-minimum Na+ load varies only 2.3-fold; the difference is almost entirely the
overlap load, which has a linear correlation R^2 = 0.99 with the total Na+ load (slope ~ 1).
Mammalian neurons (RG, RHI, MTCR) operate near the capacitive minimum (efficiency ~ 75-100%,
alpha ~ 1.0-1.3), while the squid axon at 6.3 degrees C is profligate (efficiency 9%, alpha =
11.2). Constrained optimization reduces the squid Na+ load 4.2-fold while leaving the mouse
thalamo-cortical neuron essentially unchanged, confirming that mammalian APs already sit close
to a local optimum. Optimized parameter changes vary qualitatively across models: each model
has its own local energy valley.

For this project, the paper is the canonical citation for the per-AP energy objective in the
t0097 multi-objective optimization catalogue. The energy recipe `int(I_Na) dt / 3` (per
compartment, per AP, in ATP molecules) is exactly what t0097 will report alongside the
angle-tuning loss as a co-objective in the NSGA-II Pareto search. The Na+ overlap factor alpha
is the natural normalized cost metric for cross-neuron comparison, and the mammalian alpha
range of 1.0-1.5 calibrated here sets the realistic biological lower bound for any DSGC
compartmental model. The model-dependence of optimal parameter changes also reinforces the
project preference for a population-based ranking search (NSGA-II) over a one-shot template,
since each DSGC morphology will see a different energy landscape under the joint angle-tuning
+ energy objective.

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
<summary>📖 <strong>Energy limitation as a selective pressure on the evolution of
sensory systems</strong> — Niven & Laughlin, 2008</summary>

| Field | Value |
|---|---|
| **ID** | `10.1242_jeb.017574` |
| **Authors** | Jeremy E. Niven, Simon B. Laughlin |
| **Venue** | Journal of Experimental Biology (journal) |
| **DOI** | `10.1242/jeb.017574` |
| **URL** | https://journals.biologists.com/jeb/article/211/11/1792/19035 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/10.1242_jeb.017574/summary.md) |

Niven and Laughlin (2008) ask why nervous systems, and sensory systems in particular, take the
specific morphological and biophysical forms they do, and answer that energetics is one of the
dominant selective pressures shaping them. They focus on the visual system because its
function is quantifiable (bits s-1 of information about a visual scene) and its energetic cost
is now directly measurable from whole-retina oxygen consumption, single-cell biophysical
models, and bottom-up per-component energy budgets. The review scope ranges from sub-cellular
ion-channel kinetics to the comparative neuroanatomy of cave fish, blind mole rats, and
laboratory-evolved *Drosophila*.

Methodologically, the paper consolidates three classes of measurement into a unified
accounting framework: respirometry on excised retinas, intracellular electrical models of fly
R1-6 photoreceptors that infer 3Na+/2K+ ATPase pump current from membrane biophysics, and the
component-level cortical and olfactory energy budgets of Attwell-Laughlin (2001) and Nawroth
et al. (2007). The fact that the single-cell biophysical estimates and the whole-retina O2
measurements agree on the dominant cost (ion movement through the membrane) validates this
multi-scale approach.

The principal findings are quantitative. Resting metabolic cost in fly photoreceptors is about
**25%** of peak signalling cost, and across four homologous photoreceptor species both rest
and peak cost rise faster than information rate, defining a strict bits-per-ATP frontier (Fig.
7). Action-potential transmission and resting-potential maintenance dominate the per-AP energy
budget in rat grey matter (more than 50%, Fig. 6A), and the choice of channel set has a
measurable energetic signature: removing the *Shaker* K+ conductance in *Drosophila*
simultaneously raises energy cost and lowers information rate (Fig. 8). At larger scales,
convergent reductions of sensory structures (cave-fish eyes, mole visual cortex,
lab-Drosophila ommatidia) match the prediction that unused capacity is selected against, while
the elasmobranch-vs-teleost ATPase comparison warns that brain mass alone is not a reliable
proxy for brain energy use.

For this project, the paper anchors the energy axis of a joint info-vs-energy multi-objective
optimisation. The angle-to-AP-frequency tuning error captures the information / function side;
an ATP-budget proxy (Na+/K+ pump current integrated over a stimulus, or equivalently the
integrated voltage-gated channel currents over a trial) captures the cost side. Because
resting cost is non- negligible, the energy proxy must include the idle interval and not only
the burst window. Because the cost-vs-capacity relationship is super-linear, we should expect
Pareto fronts with sharp knees where large energy savings come from trimming over-provisioned
somatic Na+ or K+ density. Together with Attwell and Laughlin (2001) and Sengupta et al.
(2010), this paper forms the energy-objective citation set that justifies bits-per-ATP as a
biologically grounded second objective for the multi-objective Na/K conductance search.

</details>

<details>
<summary>📖 <strong>A novel multiple objective optimization framework for
constraining conductance-based neuron models by experimental data</strong>
— Druckmann et al., 2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.3389_neuro.01.1.1.001.2007` |
| **Authors** | Shaul Druckmann, Yoav Banitt, Albert Gidon, Felix Schurmann, Henry Markram, Idan Segev |
| **Venue** | Frontiers in Neuroscience (journal) |
| **DOI** | `10.3389/neuro.01.1.1.001.2007` |
| **URL** | https://www.frontiersin.org/articles/10.3389/neuro.01.1.1.001.2007/full |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md) |

Druckmann et al. (2007) confront a methodological problem at the core of conductance-based
neuron modelling: how to automatically fit the maximal-conductance vector of a compartmental
model to noisy in vitro recordings, given that repeated identical current injections produce
visibly different voltage traces in the same cell. They argue that the dominant single-trace,
single-error-function approach is mis-specified - it ignores intrinsic variability and forces
an arbitrary weighting of heterogeneous error terms (e.g. spike timing vs spike shape).

Their solution is a multi-objective optimization framework in which several biophysically
meaningful spike features (rate, width, AHP depth, accommodation, latency, overshoot) are each
assigned their own error function, scored in units of the feature's experimental standard
deviation, and optimized jointly with a custom NSGA-II genetic algorithm running in NEURON.
The fitting target is a compartmental model with 10 somatic ion channels and 12 free
conductance parameters. Convergence was tested on two distinct cortical-interneuron electrical
classes - accommodating and fast-spiking - using 300 organisms and 1000 generations on either
a 112-CPU AMD cluster or a 256-512-processor BlueGene/L.

The framework converges to mean per-feature error of less than 1 SD for both classes and
returns hundreds of "acceptable" parameter sets within 2 SD on every feature. These solution
clouds segregate cleanly along some channels (Nat) and overlap on others (Im, SK), revealing
which conductances actually carry class identity. The Pareto fronts between feature pairs
further expose which objectives genuinely conflict, providing diagnostic information that
single-objective fits would discard. As a proof of generalisation the same recipe with one
extra feature qualitatively captures a third (stuttering) electrical class.

For the present project this paper is the methodology root. Our t0097 catalogue is structured
around multi-objective optimisation of somatic Na/K conductance combinations (and follow-on
dendritic-conductance variants) against a target angle-to-AP-frequency tuning curve in a
direction-selective retinal ganglion cell. Druckmann 2007 supplies (i) the SD-normalised
feature-error formulation that we should mirror when scoring our model against patch-clamp
ground-truth, (ii) the NSGA-II reference cost envelope (300 organisms x 1000 generations) for
budgeting compute, and (iii) the Pareto-of-models output mode, which is more diagnostic than a
single best-fit vector for downstream sensitivity and conductance-class analysis.

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
<summary>📖 <strong>Complex Parameter Landscape for a Complex Neuron Model</strong>
— Achard & Schutter, 2006</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.0020094` |
| **Authors** | Pablo Achard, Erik De Schutter |
| **Venue** | PLoS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.0020094` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0020094 |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md) |

Achard and De Schutter ask whether a complex, biophysically detailed compartmental neuron
admits multiple distinct sets of voltage- and calcium-gated channel conductances that
reproduce the cell''s detailed firing behavior. The motivation comes from two convergent lines
of evidence: experimental work on lobster and crab stomatogastric ganglion neurons showing
2-4x interanimal variability in channel expression with preserved activity, and prior
modelling work (Goldman 2001, Prinz 2003-2004) showing parameter degeneracy in low-dimensional
stomatogastric models. The paper extends this question to the cerebellar Purkinje cell -- a
1,600-compartment, 24-parameter model with four firing modes -- and asks both whether
degeneracy exists and what shape the good region of parameter space takes.

The methodology pairs a self-adaptive correlated-mutation evolution strategy ((57+19)
population, ~8,000 evaluations per run, 9 independent runs) with a phase-plane density
distance fitness function summed across 7 current amplitudes, 3 recording sites, and 2 time
windows. Each run took ~6 days on a 10-node G5 cluster. Twenty good solutions are retained
(fitness 2.58 to 3.45). The authors then probe the parameter landscape using single-parameter
sensitivity sweeps, +/-1% and +/-5% local perturbations, pairwise Pearson correlations on
individual and total conductances, and a novel hyperplane visualization that fits
triplet-defined planes and parallel offset planes through the solution cloud.

The 20 models reproduce somatic and dendritic voltage waveforms, complex spike responses, and
EPSP propagation despite the latter two not being in the fitness function. Total conductance
ratios across the 20 models range from 1.2x (gNaF) to 9.7x (gKh). Only 5 of 276 pairwise
correlations are significant at p < 0.01, and only the gCaT-gCaP total-conductance pair shows
a strong anti-correlation (r=-0.62). Local landscape is rough: +/-1% perturbations preserve
fitness, +/-5% can break it. Most importantly, the good region is shown to be a set of loosely
connected hyperplanes -- neither isolated points nor a single connected volume -- and a
6-points-per-dimension grid search would discover at most ~35% of the recovered solutions.

For this project, the paper establishes the methodological line that justifies using
stochastic multi-objective evolutionary search (NSGA-II in our case) on the cell''s
voltage-gated channel parameter space rather than grid sampling, and it establishes that we
should expect families of diverse solutions rather than a unique optimum. The specific
innovations relevant to t0097''s optimization design are: phase-plane or shift-tolerant
fitness as a complement to direct trace-distance metrics; self-adaptive mutation strengths in
the genome; and hyperplane analysis of the recovered Pareto front to understand which
conductance combinations actually trade off. Achard 2006 is the natural methodology citation
alongside Druckmann 2007 and Hay 2011 in this task''s catalogue, providing the earliest
detailed demonstration that complex compartmental models have low-dimensional curved manifolds
of good parameters that only population-based search can recover.

</details>

<details>
<summary>📖 <strong>Variability, compensation and homeostasis in neuron and network
function</strong> — Marder & Goaillard, 2006</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nrn1949` |
| **Authors** | Eve Marder, Jean-Marc Goaillard |
| **Venue** | Nature Reviews Neuroscience (journal) |
| **DOI** | `10.1038/nrn1949` |
| **URL** | https://www.nature.com/articles/nrn1949 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/summary.md) |

This review by Marder and Goaillard codifies the now-standard observation that nervous-system
variables --- ionic conductances, channel densities, synaptic weights --- vary substantially
across animals of the same species and across cells of the same identified type, while the
behavioural output of single neurons and networks remains conserved. The authors motivate the
question by contrasting protein turnover (minutes to weeks) with neuronal lifetime (years to
decades), arguing that homeostatic mechanisms must continuously rebuild the cell while
preserving its function, and that this rebuilding must necessarily allow for multiple
equivalent parameter configurations.

The paper proceeds methodologically by surveying single-cell electrophysiology paired with
mRNA quantification (Schulz et al. 2006 in pyloric LP neurons; Swensen and Bean 2005 in
cerebellar Purkinje cells), pharmacological vs genetic perturbation studies, and ensemble
conductance-based modelling (Goldman 2001; Golowasch 2002; Prinz, Bucher and Marder 2004). The
synthesis carefully distinguishes timescales (acute pharmacology reveals fragility, chronic
deletion reveals compensation) and scales (single neuron, microcircuit, vertebrate network),
and argues that biological robustness arises through overlapping partially-substitutable
components rather than engineered redundancy.

Quantitatively, the cited evidence shows two- to fourfold inter-animal variation in many ionic
conductances and synaptic strengths, single-cell-level correlation between channel mRNA and
maximal conductance, and the existence of millions of distinct yet behaviourally equivalent
network parameter sets in the lobster pyloric model. The reviews headline conclusion is that
"variability and compensation" are general organising principles of neuronal function, and
that ensemble approaches --- both experimental and computational --- are required to
characterise them.

For this project, this paper is the canonical citation for the *robustness / degeneracy*
objective category in the t0097 multi-objective optimisation catalogue. It directly
underwrites treating parameter-perturbation sensitivity (Marder-style: chronic compensation
potential plus acute robustness) as a multi-objective dimension alongside fitness to target
tuning curves. It also justifies the projects choice to model the direction-selective retinal
ganglion cell as a *family* of acceptable parameter sets rather than a single canonical model,
and motivates reporting solution-manifold properties (spread, co-variation structure) in
addition to Pareto fronts. Together with Prinz, Bucher and Marder (2004), it forms the
conceptual foundation for the robustness-objective recipe in the t0097 catalogue.

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
<summary>📖 <strong>Similar network activity from disparate circuit
parameters</strong> — Prinz et al., 2004</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn1352` |
| **Authors** | Astrid A. Prinz, Dirk Bucher, Eve Marder |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn1352` |
| **URL** | https://www.nature.com/articles/nn1352 |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nn1352/summary.md) |

Prinz, Bucher and Marder ask how tightly neuronal properties and synaptic strengths must be
tuned to produce a specific network output. They focus on the crustacean pyloric rhythm
because its connectivity, neurons, and motor pattern are unusually well characterised. The
motivation is to test the implicit assumption underlying much of neurophysiology, that
animal-to-animal variability is "experimental noise" rather than a structural feature of the
nervous system. The hypothesis is that, just as similar single-neuron firing can arise from
many channel-density combinations, similar network output can arise from many cellular and
synaptic parameter combinations.

Methodologically, they enumerate 20,250,000 three-neuron model networks built from a 16-neuron
pool selected from a prior 1.7-million-neuron STG database, varying seven synaptic
conductances across five or six values. Each network is simulated, auto-classified, and tested
against 15 burst-timing features measured from 99 Homarus americanus pyloric recordings. The
model uses standard Hodgkin-Huxley dynamics with eight membrane currents per cell and
Abbott-Marder synapse kinetics. The full simulation ran for several months on a Beowulf
cluster of 1.2-GHz processors and produced approximately 4 GB of classification output.

The headline finding is that 2.2% (452,516) of all networks satisfy the strict 15-feature
pyloric criterion, every cell-combination is represented in this set, and six of the seven
synaptic conductances span the full 0-100 nS range. Only LP-to-PY is tightly constrained (>3
nS in just 0.1% of pyloric networks), matching its weak biological strength. Networks with
conductances differing by factors of three or more produce visually indistinguishable rhythms.
Burst period is controlled mainly by the AB/PD pacemaker identity, while LP and PY identity is
essentially free.

For the t0097 multi-objective optimization catalogue this paper anchors the biological
plausibility and degeneracy objective. It directly motivates: (i) treating the optimization
output as a Pareto manifold rather than a point, (ii) using multi-feature biological
acceptance criteria with explicit mean +/- 2 s.d. bands instead of single-objective fitting,
(iii) reporting which conductances remain unconstrained and which are tightly bottlenecked
across the Pareto front, and (iv) interpreting variability across the recovered solution set
as a biologically meaningful prediction about animal-to-animal heterogeneity in
direction-selective retinal ganglion cells, not as optimization noise. Combined with the
Marder-Goaillard 2006 review (already in this task as nrn1949), Prinz2004 grounds the t0097
robustness analysis in the canonical "many disparate parameter sets, one functional output"
result.

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
<summary>📖 <strong>An Energy Budget for Signaling in the Grey Matter of the
Brain</strong> — Attwell & Laughlin, 2001</summary>

| Field | Value |
|---|---|
| **ID** | `10.1097_00004647-200110000-00001` |
| **Authors** | David Attwell, Simon B. Laughlin |
| **Venue** | Journal of Cerebral Blood Flow & Metabolism (journal) |
| **DOI** | `10.1097/00004647-200110000-00001` |
| **URL** | https://journals.sagepub.com/doi/10.1097/00004647-200110000-00001 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0097_multi_obj_optim`](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/summary.md) |

Attwell and Laughlin (2001) ask a single quantitative question: how much ATP does each
elementary neuronal signaling event cost, and do these per-event costs sum to the
experimentally measured total energy consumption of brain grey matter? The motivation is that,
prior to 2001, neural energy estimates were either top-down (whole-brain glucose/oxygen
consumption with no decomposition) or based on heat production from single-cell preparations,
which severely underestimated AP cost. The authors aim to construct a biophysically grounded,
mechanism-by-mechanism budget that reconciles micro-scale measurements with whole-tissue
metabolism.

The methodology is bottom-up biophysical accounting. They derive a clean scaling result — the
ATP cost of any signaling event equals (Na+ load entering) / 3, set by the Na+/K+ pump
stoichiometry — and apply it to every step of glutamatergic transmission and AP propagation.
Inputs are taken from published patch-clamp, electron-microscopy, and biochemistry literature
for rodent neocortex: synaptic conductance, channel open time, vesicle glutamate content,
release probability, neuron/synapse density, membrane area. The model is intentionally
simplified (all neurons treated as glutamatergic; "typical" cell geometry) so that the
dominant contributions can be identified robustly.

The headline finding is that signaling consumes 75% of grey-matter energy, with action
potentials (47%) and postsynaptic glutamate currents (34%) dominating. The predicted specific
consumption of 30 µmol ATP/g/min for signaling, plus 10 µmol/g/min for housekeeping, falls
within the measured range of 33–50 µmol/g/min, validating the budget. The paper also delivers
two derived quantities that have become standard tools: the 1-spike-per-neuron-per-second ≈
6.5 µmol ATP/g/min scaling rule (used to convert spike rates to fMRI BOLD predictions) and the
7.1 × 10^8 ATP-per-spike per-neuron cost. A coding-theory analysis predicts that 15% sparse
codes are energetically optimal at biological firing rates.

For the t0097 multi-objective optimization catalogue, this paper is the foundational citation
for the metabolic-energy objective category. It establishes the "ATP via Na+ load / 3" recipe
that maps any compartmental simulation's integrated Na+ flux to a quantitative ATP cost, gives
the per-event reference values (3.84 × 10^8 ATP per AP, 1.64 × 10^5 ATP per vesicle, 3.42 ×
10^8 ATP/s per resting neuron) needed to validate any future DSGC energy-objective
implementation, and provides the empirical benchmark (7.1 × 10^8 ATP per spike per neuron)
against which simulated energy costs can be sanity-checked. The single-cell, single-event
biophysical formulation is directly compatible with the project's NEURON pipeline, which
already records `ina` per-section and per-time-step, so adding a "minimize ATP per simulated
trial" objective to the existing NSGA-II loop is a small extension rather than an
infrastructure rewrite.

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

## Tasks (10)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: compartmental models of DS retinal ganglion cells](../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) | completed | 2026-04-19 01:35 |
| 0015 | [Literature survey: cable theory and dendritic filtering](../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) | completed | 2026-04-20 10:00 |
| 0016 | [Literature survey: dendritic computation beyond DSGCs](../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) | completed | 2026-04-20 10:36 |
| 0017 | [Literature survey: patch-clamp recordings of RGCs and DSGCs](../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) | completed | 2026-04-20 11:08 |
| 0019 | [Literature survey: voltage-gated channels in retinal ganglion cells](../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) | completed | 2026-04-20 13:00 |
| 0027 | [Literature survey: modeling effect of cell morphology on direction selectivity](../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) | completed | 2026-04-21 22:23 |
| 0078 | [Bed B v2 MOBO with AIS, tier-stratified channels, and slow Kv-AHP](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) | completed | 2026-05-04 16:25 |
| 0080 | [Bed B v3 MOBO with dendritic-spike machinery and NSGA-II](../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) | completed | 2026-05-04 22:45 |
| 0091 | [First joint 68-d NSGA-II with morphology in eval loop, 5-anchor warm-start](../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) | completed | 2026-05-08 15:55 |
| 0097 | [Literature survey: multi-objective optimisation of single-neuron models](../../overview/tasks/task_pages/t0097_multi_obj_optim.md) | completed | 2026-05-08 16:50 |

## Answers (10)

<details>
<summary><strong>Which factors (after varimax rotation on the full 68-d pool) load
most strongly on dsi_vector_sum and pd_rate_hz, and are they
morphology-dominated, electrophys-dominated, or mixed?</strong></summary>

**Confidence**: medium | **Date**: 2026-05-21 | **Full answer**:
[`pooled-survivors-latent-drivers-dsi07-pd10`](../../tasks/t0116_pooled_pca_cluster_factor_dsi07_pd10/assets/answer/pooled-survivors-latent-drivers-dsi07-pd10/)

F1 is the dominant DSI driver (r=-0.589, p ~ 1e-82) and is mixed — its top loadings include
both electrophys channels (SK_AIS, SKAHP, NAP) and a morphology parameter
(primary_branch_pd_concentration). F3 is the dominant PD-rate driver (r=+0.746, p ~ 1e-155)
and is purely electrophys (NAR, IH, NAV16_SOMA, BK channels, RA). No single factor crosses
|r|>0.3 on both DSI and PD simultaneously, so the strict-cohort pool does not contain a joint
DSI-PD axis — the answer to "are the drivers shared?" is no in this strict cohort, but t0110's
relaxed-cohort analysis shows this is a known truncated-cohort artefact.

</details>

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
<summary><strong>Do the validation triplet results (G.1 AIS-to-soma Nav ratio audit,
G.2 NMDA units calibration, G.3 NaP knockout) confirm or refute the
biological-plausibility flags raised in t0086 and t0088?</strong></summary>

**Confidence**: medium | **Date**: 2026-05-07 | **Full answer**:
[`validation-triplet-implications-for-biological-plausibility`](../../tasks/t0090_morphology_generator_diversity_test/assets/answer/validation-triplet-implications-for-biological-plausibility/)

Conditional. The G.1 AIS-to-soma Nav-ratio audit shows the cluster-1 ratio is a real
biological signal, not a centroid artifact: zero of four cluster-1 cells are pinned to the
soma Nav lower bound and three of four cells individually exceed a ratio of 50, so the
+33-sigma deviation from the Werginz 2024 prior reflects an actual model preference rather
than an inflated denominator. G.2 produces a NetCon-weight to per-spine conductance
calibration that lets us re-score the cluster-NMDA-exotic verdict in calibrated units, but the
conversion does not by itself reduce the deviation enough to rule out a units mismatch. G.3
quantifies the causal contribution of distal NaP to the direction-selectivity index of the
four cluster representatives by comparing knockout DSI against the original t0083 DSI,
providing a per-cell verdict (NaP-dominant, NaP-partial, or NaP-minor). Taken together, the
triplet confirms two of the t0086 / t0088 flags as real biological signals (cluster-1
AIS-to-soma ratio, NaP attribution where the knockout collapses DSI) and leaves the
NMDA-exotic flag in the conditional category pending an independent measurement of per-spine
open conductance in the t0024 voltage-clamp regime.

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

## Suggestions (82 open, 15 closed)

<details>
<summary>📊 <strong>Interpret F1's biological meaning: top-loading features of the
joint DSI-PD factor in the unfiltered pool</strong> (S-0117-06)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-22 | **Source**:
[t0117_pooled_pca_cluster_factor_all_cells_4_seeds](../../tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/)

t0117 confirms F1 is a joint DSI-PD axis but stops short of biological interpretation - it
reports F1's r_DSI/r_PD but not its top loadings on the 68-d feature vector (54-d electrophys
+ 14-d morphology). The latent-drivers question is only partially answered. Read
results/data/factor_loadings.csv, rank F1's loadings by absolute value, and identify the top-7
ephys parameters and top-3 morphology parameters loading on F1. Cross-reference t0116's pooled
F1 top loadings (SK_AIS + primary_branch_pd_concentration) and to t0108/t0110 strict/relaxed
comparison. Write a focused answer asset 'pooled-all-cells-f1-biological-interpretation' with
the loading table plus a 4-sentence biological interpretation: which channels and morphology
parameters jointly drive both DSI and PD when the full quality range is admitted? Recommended
task types: data-analysis, answer-question. Cost: <$0.10.

</details>

<details>
<summary>🧪 <strong>Factor-axis trace gallery: sample cells along t0117 F1/F3/F5
loading axes and re-simulate the 3-mode trio</strong> (S-0118-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-22 | **Source**:
[t0118_resimulate_t0117_cluster_samples_ge_gi_vm](../../tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/)

t0118 establishes a clean re-simulation pipeline (3-mode trio, g_E / g_I / V_m, PD+ND, 1400
ms). t0117's salient factors are F1 (joint DSI-PD, 12.6% var), F3 (pure-ephys PD), F5
(depolarisation-block axis hypothesised in t0118 analysis). Link from factor space to
biophysics is currently inferential. Concrete action: project all 4431 t0117 cells onto F1,
F3, F5 individually; bin cells into 7 quantiles along each factor score, sample 3 cells per
bin (21 cells x 3 factors = 63 cells), re-simulate the t0118 protocol. For each factor produce
a 7-row x 3-column grid showing how g_E/g_I/V_m signatures change along the factor axis.
Decision: monotonic variation = biophysically meaningful factor; unrelated = statistical
artefact. Distinct from S-0117-06 (interprets F1 loadings statically). Recommended task types:
experiment-run, data-analysis. Cost: <$0.30.

</details>

<details>
<summary>🧪 <strong>Targeted Ca-K channel ablation sweep on top-PC1 asymmetric cells
to validate the SK/BK mechanistic hypothesis</strong> (S-0105-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-14 | **Source**:
[t0105_cluster_factor_analysis_dsi_pd](../../tasks/t0105_cluster_factor_analysis_dsi_pd/)

PC1 separates symmetric from asymmetric cells at p = 1.48e-10 with top loadings SK_TERMINAL,
BK_TERMINAL, SK_SOMA, BK_MID, NAP_PRIMARY. The mechanistic hypothesis is that asymmetric
dendrites concentrate Ca influx along the PD axis, so high terminal SK/BK locally quenches
PD-side over-excitation. Test by taking the top-3 PC1-positive asymmetric cells (high Ca-K
regime, e.g. the t0102 / t0104 cells in the cohort), independently ablating SK_TERMINAL = 0,
BK_TERMINAL = 0, SK_SOMA = 0, BK_MID = 0 (one at a time and combined), and re-evaluating DSI +
PD on the de Rosenroll Bed B substrate. Outcome: a 4x4 ablation grid per cell showing which
Ca-K conductance is load-bearing for the asymmetric direction-selectivity regime. Recommended
task types: experiment-run, data-analysis. Cost: ~$2-3 (small Vast.ai instance for 3-6 hours;
or local if NEURON runs locally). Aligns with PolegPolsky2026's ML channel-importance finding.

</details>

<details>
<summary>🧪 <strong>Anchor-1-only warm-start NSGA-II to isolate which part of t0091's
warm-start was load-bearing</strong> (S-0099-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-10 | **Source**:
[t0099_random_init_pareto_robustness](../../tasks/t0099_random_init_pareto_robustness/)

t0099 confirmed t0091's 5-anchor warm-start was load-bearing (0/55 random-init joint-pass
cells vs t0091's 1/57). Open question: was anchor 1 (Bed-B-like) sufficient, or did the
diversity of all 5 anchors matter? Run NSGA-II with all 96 init cells cloned from anchor 1
only (96 different t0083 electrophys vectors), pop=96, 8 gens, $5 cap. Outcome (a): joint-pass
emerges -> anchor 1 was load-bearing alone. Outcome (b): no joint-pass -> warm-start diversity
itself was load-bearing. Either narrows future morphology-extended NSGA-II design
substantially. Cost ~$3.50 single seed.

</details>

<details>
<summary>🧪 <strong>Constrained channel-only NSGA-II on fixed t0093 morphology to
disambiguate channel-side from morphology-side priors</strong> (S-0091-08)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-08 | **Source**:
[t0091_morphology_extended_nsga2_v1](../../tasks/t0091_morphology_extended_nsga2_v1/)

t0091's 0/57 plausible-cell verdict is universally driven by channel-side priors (NMDA
per-spine, NaP density, GABA spatial gradient); morphology priors mostly pass. S-0086-01
already proposes a tighter-NMDA re-run but does not specify morphology configuration nor
combine with hard-constraint formulation. Hold morphology fixed at the t0093 verified
BedB-equivalent (PD-rate 43.6 Hz post-fix) and run NSGA-II on a 27-d channel-only space (12
channel densities + 9 NMDA/NaP-related + 6 GABA spatial) with all biological priors as hard
constraints (per S-0091-05) and tightened NMDA bounds (Sivyer 2013 5e-4 uS upper cap). Tests
whether the v3 substrate has any biologically-plausible joint-pass region in channel space
alone with verified morphology, independent of S-0086-01's broader question. If no, the
substrate is incompatible with priors regardless of morphology, motivating S-0091-06's
real-cell library. Cost ~$1.50 on Vast.ai EPYC 7B13. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-calibrate t0083 channel densities to the post-fix procedural
cell's 707 um^2 cylinder soma</strong> (S-0092-06)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-08 | **Source**:
[t0092_diagnose_morphology_generator_silence](../../tasks/t0092_diagnose_morphology_generator_silence/)

The post-fix BedB-equivalent fires 61 spikes vs the hand-coded Bed B's 41 spikes under the
same t0083 vector, because the channel densities were optimised on the 287 um^2 hand-coded
soma but the post-fix procedural soma is 707 um^2. Rather than tightening the soma area to
match t0024 (S-0092-02's path), the alternative is to re-run a small-scale NSGA-II pass on the
25 channel-density parameters (indices 0-24 + the dendritic-spike block 49-53) holding
morphology fixed at the post-fix BedB-equivalent, to find a 30-cell Pareto front under the
larger soma. The chosen winner becomes the new t0091 channel-side warm-start anchor. ~$1-2
cost on a single A10G; pure follow-up to t0083 with the new substrate. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Bed B NSGA-II maximising DSI and minimising
ATP-per-spike</strong> (S-0097-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-08 | **Source**:
[t0097_multi_obj_optim](../../tasks/t0097_multi_obj_optim/)

Anchored to the canonical Attwell-Laughlin energy budget (47% of cortical signalling ATP per
spike). Remme et al. 2018's MSO function-vs-energy MOBO provides a direct methodology template
generalising to NEURON. DSGC's GABAergic-style fast-spiking should produce
Carter-Bean-2009-style Na/K-overlap penalty; the front should expand toward dramatically lower
energy as Na+ density and overlap are jointly reduced. Recipe: `(1/3) sum int(I_Na) dt / e`
per compartment per AP. Budget: 24-48 h Vast.ai EPYC at $0.30/h, total $8-15 — may exceed
per-task default; flag for explicit budget approval.

</details>

<details>
<summary>🧪 <strong>Bed B NSGA-II maximising DSI and robustness under +/-10%
channel-density perturbation</strong> (S-0097-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-08 | **Source**:
[t0097_multi_obj_optim](../../tasks/t0097_multi_obj_optim/)

Directly addresses the researcher's recurring biological-plausibility concern with pure-DSI
maximisation (Marder-style population-statistic robustness is the field-standard treatment).
Falsifiable prediction: high-DSI / high-robustness corner lies along compensatory hyperplanes,
refuting the hypothesis that DSI maximisation drives the optimiser to fragile parameter-space
extremes. Recipe: K=50-200 +/-10% perturbations per Pareto point; minimise SD of DSI. Budget:
36-72 h Vast.ai EPYC at $0.30/h, total $11-22 (multiplies t0091's per-individual cost by
K=50-200) — request explicit $25 budget cap or reduce population/generations.

</details>

<details>
<summary>🧪 <strong>Bed B NSGA-II maximising MI and minimising ATP-per-spike
(bits-per-ATP front)</strong> (S-0097-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-08 | **Source**:
[t0097_multi_obj_optim](../../tasks/t0097_multi_obj_optim/)

Decouples function (information) from selectivity (DSI). Produces a bits-per-ATP Pareto front
directly comparable to Niven et al. 2007's empirical fly-photoreceptor 200-1000 bits/s
super-linear cost-vs-information curve. The DSGC bits-per-ATP ratio is unmeasured in the
literature, so the experiment closes a genuine open question. Tradeoff: this experiment does
not directly serve the project's first-question DSGC mission (DSI is not optimised); ranked
medium because it serves a broader scientific question rather than the project's specific
deliverable. Budget: 24-48 h Vast.ai EPYC at $0.30/h, total $8-15 — comparable to S-0097-02.

</details>

<details>
<summary>🧪 <strong>Run G.3 NaP-knockout sweep at scale on local 64-core EPYC with
ProcessPoolExecutor</strong> (S-0090-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-07 | **Source**:
[t0090_morphology_generator_diversity_test](../../tasks/t0090_morphology_generator_diversity_test/)

t0090 Phase G.3 committed the NaP-knockout driver as infrastructure_only because the
single-process wall-clock projection (~42 min/cell x 4 cluster representatives = ~3 hours)
plus NEURON DLL state-management on Windows blew the implementation budget. After S-0090-01
retunes BEDB_BASE_POINT so the procedural cell fires under t0083 params, run the deferred 4
cells x 16 directions sweep across the 64-core EPYC using ProcessPoolExecutor with one NEURON
sub-process per worker to bypass the DLL-cleanup serialisation cost. Pass criterion (per t0090
plan): DSI collapses to <0.2 in all 4 cluster representatives if NaP is causally responsible
for PD-vs-ND attribution; otherwise the NMDA / Nav1.6 / GABA mix matters more than t0088's
correlational analysis suggested. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Multi-channel-set diversity re-test of t0090 morphologies to
disentangle morphology vs channel-set sensitivity</strong> (S-0090-05)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-07 | **Source**:
[t0090_morphology_generator_diversity_test](../../tasks/t0090_morphology_generator_diversity_test/)

The t0090 finding that 51/60 morphologies fail NAN_VOLTAGE rests on a single channel set
(t0083 best-cell). To confirm Mainen 1996 morphology-determines-firing-pattern as the cause
(rather than the t0083 channel set being uniquely fragile), re-run the 60-morphology
verification on 3 different t0083 Pareto cells' channel sets (e.g. cells 1559, 1639, 767
spanning the t0086 cluster representatives). If the STABLE / NAN_VOLTAGE flag is consistent
across channel sets per morphology, the failure is morphology-specific and S-0090-04's
tightened LHS bounds are the right fix; if STABLE-or-not depends on channel set, the joint
68-d NSGA-II must accept that warm-start anchors are channel-set-conditional. Pure simulation;
no remote machine; ~30 min on local 64-core. Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary>📊 <strong>Investigate why t0086 / t0088 cluster 1 converges to extreme
AIS-to-soma Nav ratios (per-cell range 42.6-270.7)</strong> (S-0090-06)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-07 | **Source**:
[t0090_morphology_generator_diversity_test](../../tasks/t0090_morphology_generator_diversity_test/)

t0090 Phase G.1 audit ruled out floor-pinning and centroid-averaging artifacts: cluster-1
cells 1304 / 1504 / 1624 / 1634 individually have AIS-to-soma Nav ratios of 139.4 / 42.6 /
270.7 / 141.2 (all above 2.5x the Werginz 2024 mean of 17.3). Verdict: real_signal. Probe the
loss landscape around these 4 cells: in the t0083 archive's 54-d parameter space, restrict to
cluster-1 morph variants and visualise the DSI / PD-rate / robustness slice along (Nav_AIS,
Nav_soma) at fixed values of all other dimensions. Either the optimiser is rationally finding
an extreme-but-functional regime that should motivate revising the prior (a la S-0086-05's
RGC-specific-NaP-density argument), or the loss surface is multi-modal and a tightened upper
bound on Nav_AIS would still find joint-pass cells. Recommended task types: data-analysis.

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
<summary>📊 <strong>Audit AIS-to-soma Nav ratio computation in cluster 1 (116x is
+33 sigma exotic)</strong> (S-0088-02)</summary>

**Kind**: evaluation | **Priority**: high | **Date**: 2026-05-06 | **Source**:
[t0088_recluster_marginals_and_vm_motifs](../../tasks/t0088_recluster_marginals_and_vm_motifs/)

t0088 cluster 1 (cells 1304, 1504, 1624, 1634) has centroid AIS-to-soma Nav ratio = 116.04,
deviating +32.92 sigma from Werginz 2024's published 17.3 +/- 3. This is the most extreme
single-prior violation in t0086 + t0088. Audit the ratio computation: (a) confirm
centroid_unnormalised[NAV16_AIS_GBAR] / centroid_unnormalised[NAV16_SOMA_GBAR] is in matching
units (S/cm^2 / S/cm^2 = dimensionless); (b) check the soma Nav lower bound is not pinning the
centroid soma value to a near-zero value, inflating the ratio; (c) check whether the 4 cells
in cluster 1 individually have AIS-to-soma ratios near 116 or whether the centroid is
averaging across heterogeneous values. Pure data analysis on existing JSON outputs; ~30 min
wall-clock, $0 cost. Recommended task types: data-analysis, correction.

</details>

<details>
<summary>📊 <strong>Cell-767-anchored parameter-space pruning to identify well-tuned
dims that can be clamped in future Bed B optimisation</strong> (S-0081-04)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-05 | **Source**:
[t0081_bedb_v3_warmstart_nsga2](../../tasks/t0081_bedb_v3_warmstart_nsga2/)

Compare cell 767's 54-d natural-unit parameter vector to (a) the high-DSI rail cells (699,
744, 112) and (b) the high-PD rail cells (627, 664, 730) on the t0081 Pareto front. Identify
dims whose values converge across these clusters (candidates for clamping at the median value)
versus dims that vary substantially (must remain free). Pure data analysis on
`results/data/all_evaluations.json`; no compute cost. Distinct from S-0080-04 which proposed
generic 30-40d pruning before re-running NSGA-II — this is anchored to the joint-pass cell
rather than to the t0080 Pareto. Output: a candidate clamped-parameter list and a re-run
sub-task proposal. Recommended task types: data-analysis.

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
<summary>🧪 <strong>AIS-localised NaP placement test: distal-dendrite NaP vs AIS
NaP on cells 767 / 637 / 762</strong> (S-0084-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-05 | **Source**:
[t0084_t0081_cell_767_vm_trace_deepdive](../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/)

The de Rosenroll 2026 schema places NaP on the AIS but the v3 substrate (t0080) places NaP on
terminal dendrites instead. t0084 found NaP-dominant attribution at the terminal dendrite, but
the dominant-mechanism story may differ if NaP were instead on the AIS. Test by holding cells
767 / 637 / 762 parameters fixed but moving NaP from terminal_dends to ais_distal at the same
density, and re-evaluating DSI / PD rate / fractional contribution. Hypothesis: AIS-localised
NaP would shift dominance toward Nav1.6 or NMDA at the dendrite. Local CPU; 48 runs. Cost ~$0.
Recommended task types: experiment-run.

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
<summary>🧪 <strong>Re-run Bed B MOBO with tau_ca_multiplier upper bound increased
from [1, 20x] to [1, 200x] to test the slow-Kv AHP regime</strong>
(S-0078-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-04 | **Source**:
[t0078_bedb_mobo_v2_ais_tiered_ahp](../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/)

The t0078 high-DSI rail's PD ceiling at 2.86 Hz held flat across 109 acquisitions despite
optimiser exploration, the signature of a saturated negative-feedback loop. The 20x upper
bound corresponds to tau_ca ~ 100 ms; Larsson 2013 reports mammalian sAHP decay on the 1-3 s
timescale, equivalent to multiplier values of ~ 100-300x. The originally-proposed [1, 200x]
bound was reduced to [1, 20x] by researcher decision pre-launch as a simulation-budget safety
margin. Hypothesis: at multiplier > 20x the slow-Kv regime engages and may (a) free the PD
ceiling on the high-DSI rail or (b) not change behaviour (confirming saturation is
mechanistic, not parametric). Bundle with S-0078-01 if NSGA-II is run, or run as a focused
5-cell re-evaluation of t0078 high-DSI Pareto cells (iter 290, 283, 442, 371, 380) with
multiplier expanded to 200x. Cost: $0.20-$0.50 focused or rolled into S-0078-01. Recommended
task types: experiment-run.

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
<summary>🧪 <strong>Parameter-space pruning to ~30-40 d before re-running NSGA-II
on the Bed B substrate</strong> (S-0080-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-04 | **Source**:
[t0080_bedb_mobo_v3_dendritic_spike_nsga2](../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/)

t0078's 49-d run revealed that several parameters consistently land at floors or ceilings
across the full BoTorch trajectory, suggesting they carry little Pareto information. Audit
t0078's per-parameter posterior-quantile distributions and t0080's per-parameter Pareto-cell
values; drop the 10-15 parameters with the narrowest effective ranges (e.g., parameters whose
5th-95th percentile across feasible cells spans <10% of bounded range). Re-run NSGA-II on the
pruned 30-40 d substrate at pop=24 / gen=8 to confirm that the dimensionality-vs-budget
mismatch is the dominant negative-result driver. Cost ~$0.75 (similar budget to t0080 but
smaller search space should converge faster). Recommended task types: experiment-run,
data-analysis.

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
