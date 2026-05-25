# Papers: `voltage-gated-channels` (35)

35 papers across 20 year(s).

[Back to all papers](../README.md)

---

## 2024 (3)

<details>
<summary>📖 Dendritic mGluR2 and perisomatic Kv3 signaling regulate dendritic
computation of mouse starburst amacrine cells — Ledesma et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_s41467-024-46234-7` |
| **Authors** | Hector Acaron Ledesma, Jennifer Ding, Swen Oosterboer, Xiaolin Huang, Qiang Chen, Sui Wang, Michael Z. Lin, Wei Wei |
| **Venue** | Nature Communications (journal) |
| **DOI** | `10.1038/s41467-024-46234-7` |
| **URL** | https://www.nature.com/articles/s41467-024-46234-7 |
| **Date added** | 2026-04-21 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_s41467-024-46234-7/summary.md) |

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
<summary>📖 Differential Intrinsic Firing Properties in Sustained and Transient Mouse
αRGCs Match Their Light Response Characteristics and Persist during Retinal
Degeneration — Werginz et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.1592-24.2024` |
| **Authors** | Paul Werginz, Viktoria Király, Guenther Zeck |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.1592-24.2024` |
| **URL** | https://www.jneurosci.org/content/45/2/e1592242024 |
| **Date added** | 2026-05-03 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/summary.md) |

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
<summary>📖 Persistent sodium currents in neurons: potential mechanisms and
pharmacological blockers — Müller et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.1007_s00424-024-02980-7` |
| **Authors** | Peter Müller, Andreas Draguhn, Alexei V. Egorov |
| **Venue** | Pflügers Archiv - European Journal of Physiology (journal) |
| **DOI** | `10.1007/s00424-024-02980-7` |
| **URL** | https://link.springer.com/article/10.1007/s00424-024-02980-7 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1007_s00424-024-02980-7/summary.md) |

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

## 2022 (2)

<details>
<summary>📖 Differences in spike generation instead of synaptic inputs determine the
feature selectivity of two retinal cell types — Wienbar & Schwartz, 2022</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2022.04.012` |
| **Authors** | Sophia Wienbar, Gregory William Schwartz |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2022.04.012` |
| **URL** | https://www.cell.com/neuron/fulltext/S0896-6273(22)00357-9 |
| **Date added** | 2026-05-03 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1016_j.neuron.2022.04.012/summary.md) |

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
<summary>📖 Pareto optimality, economy-effectiveness trade-offs and ion channel
degeneracy: improving population modelling for single neurons — Jedlicka
et al., 2022</summary>

| Field | Value |
|---|---|
| **ID** | `10.1098_rsob.220073` |
| **Authors** | Peter Jedlicka, Alexander D. Bird, Hermann Cuntz |
| **Venue** | Open Biology (journal) |
| **DOI** | `10.1098/rsob.220073` |
| **URL** | https://royalsocietypublishing.org/doi/10.1098/rsob.220073 |
| **Date added** | 2026-05-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0124_bedb_dsi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0124_bedb_dsi_atp_per_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/paper/10.1098_rsob.220073/summary.md) |

The paper, by Jedlicka, Bird and Cuntz (Open Biology 2022), is a methodological review that
argues for adopting **Pareto optimality** as a unifying framework for constraining the
high-dimensional parameter space of conductance-based neuron population models. The motivation
is the well-known problem of **ion channel degeneracy**: many disparate combinations of ionic
conductances yield indistinguishable voltage traces, leaving population-modelling pipelines
with a vast space of valid but biologically implausible candidates. The research question is
whether evolution selects, among the degenerate solutions, the subset that is Pareto optimal
for a trade-off between functional effectiveness and energy economy.

Methodologically the paper has no new simulations -- it synthesizes (1) the Shoval-Alon
theorems from systems biology, which predict that Pareto fronts in n-d parameter space
collapse to (m-1)-dimensional polytopes with m vertices when m tasks are jointly optimized,
(2) the standard **current-counting ATP-accounting** approach for conductance-based models due
to Attwell-Laughlin and refined by Remme et al., and (3) the **Pareto Task Inference (ParTI)**
algorithm of Shoval-Hart for inferring tasks from data. The authors then walk through three
case studies from the literature (MSO coincidence detection, L5 PC dendritic computation,
stomatogastric ganglion) where Pareto-style analysis has either been done explicitly or could
be done.

The headline findings are conceptual rather than quantitative: the geometric theorems imply
that Pareto-optimal subsets of n-d conductance spaces should be **(m-1)-d manifolds**,
naturally explaining experimentally observed ion channel correlations. The MSO example shows
that an experimentally constrained model sits on the Pareto front for the
coincidence-detection vs ATP-cost trade-off; the L5 PC example links low Kv3.1 and Ca-HVA
expression in the dendritic hot zone to joint efficiency in energy and computation. Pareto
Task Inference applied to Patch-seq data is proposed as a way to deduce functional archetypes
without specifying tasks a priori.

For this project, and specifically for task t0124 (DSI vs ATP per spike NSGA-II on a 68-d
DSGC), the paper provides direct theoretical grounding. It justifies reporting the NSGA-II
Pareto front as a biologically meaningful low-d manifold (predicted to be a 1-d curve through
68-d space for two objectives), motivates testing whether parameter sets on the front exhibit
predictable conductance correlations, and supports the project use of degeneracy as an
explanatory hypothesis (multiple 68-d parameter sets yield equivalent DSI but vary in ATP
cost). The framework also suggests follow-up tasks: PCA of the Pareto front to test the
1-d-manifold prediction, and ParTI on the population of valid DSGC models to infer whether DSI
and ATP cost are the only relevant tasks or whether additional latent objectives (e.g.
robustness) are needed.

</details>

## 2020 (2)

<details>
<summary>📝 Electrical match between initial segment and somatodendritic compartment
for action potential backpropagation in retinal ganglion cells — Goethals
et al., 2020</summary>

| Field | Value |
|---|---|
| **ID** | `10.1101_2020.09.15.297937` |
| **Authors** | Sarah Goethals, Martijn C. Sierksma, Xavier Nicol, Annabelle Réaux-Le Goazigo, Romain Brette |
| **Venue** | bioRxiv (preprint) |
| **DOI** | `10.1101/2020.09.15.297937` |
| **URL** | https://www.biorxiv.org/content/10.1101/2020.09.15.297937v2 |
| **Date added** | 2026-05-04 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Added by** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1101_2020.09.15.297937/summary.md) |

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
<summary>📖 Tailoring of the axon initial segment shapes the conversion of synaptic
inputs into spiking output in OFF-alpha T retinal ganglion cells — Werginz
et al., 2020</summary>

| Field | Value |
|---|---|
| **ID** | `10.1126_sciadv.abb6642` |
| **Authors** | Paul Werginz, Vineeth Raghuram, Shelley I. Fried |
| **Venue** | Science Advances (journal) |
| **DOI** | `10.1126/sciadv.abb6642` |
| **URL** | https://www.science.org/doi/10.1126/sciadv.abb6642 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1126_sciadv.abb6642/summary.md) |

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

## 2018 (1)

<details>
<summary>📖 Function and energy consumption constrain neuronal biophysics in a
canonical computation: Coincidence detection — Remme et al., 2018</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1006612` |
| **Authors** | Michiel W. H. Remme, John Rinzel, Susanne Schreiber |
| **Venue** | PLOS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1006612` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006612 |
| **Date added** | 2026-05-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`cable-theory`](../../../meta/categories/cable-theory/) |
| **Added by** | [`t0124_bedb_dsi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0124_bedb_dsi_atp_per_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/paper/10.1371_journal.pcbi.1006612/summary.md) |

Remme, Rinzel, and Schreiber address whether the morphology and membrane parameters of a real
mammalian neuron reflect a joint optimisation between functional performance and metabolic
energy consumption, or whether one of those two constraints dominates. They choose the
principal MSO cell of the auditory brainstem as their test case because (i) the functional
computation -- interaural time difference coincidence detection -- is unambiguous and
quantifiable, and (ii) prior immunohistochemistry has flagged MSO neurons as exceptionally
energy-intense, making any function-energy compromise easy to detect.

They build a minimal compartmental model -- soma plus two passive dendrites carrying a uniform
voltage-gated low-threshold potassium current IKLT -- fit it to published gerbil patch-clamp
data on EPSP attenuation, EPSP halfwidth, and input resistance with and without DTX block, and
exhaustively sweep six biophysical parameters (three morphological, three membrane) one at a
time and in selected two-parameter combinations. Performance is the firing-rate modulation
between ITD = 0 ms and ITD = 0.5 ms under a 500 Hz phase-locked pure-tone input; energy cost
is total Na+ influx across the cell converted to ATP/s via the Attwell-Laughlin 3-Na+-per-ATP
ion-counting scheme. Each parameter sweep is plotted as a curve in (energy cost,
1/performance) space, and the lower-left envelope across all sweeps is identified as the local
Pareto-optimal front.

The empirically fitted MSO model produces **~320 spikes/s** rate modulation at **6.2 x 10^9
ATP/s** and sits essentially on the Pareto front: no single-parameter perturbation can improve
performance without raising cost or vice versa. The KLT current is essential -- passive
variants halve performance and double cost. Most morphological and membrane parameters show a
clear performance peak near the measured default, while energy cost rises monotonically with
cell size; the cell appears to spend energy only where function demands it. A dendrite-less
point-neuron control matches most of the performance at far lower cost, so the measured
dendritic morphology must reflect non-function-non-energy constraints (e.g. surface area for
synapses, circuit wiring).

This paper is the direct methodological template for t0124. The task's "DSI vs ATP per spike"
NSGA-II optimisation is the natural extension of Remme et al.'s exhaustive sweep into many
more dimensions, on a direction-selective retinal ganglion cell instead of an MSO cell. The
ion-counting cost calculation, the choice to use a scalar performance metric in opposition to
a scalar metabolic metric, the practice of locating empirical defaults on the computed Pareto
front, and the search for a small set of mechanistic factors that explain the front shape are
all strategies t0124 should reuse. This will be the primary literature anchor for t0124's
compare-literature stage.

</details>

## 2017 (2)

<details>
<summary>📖 "Silent" NMDA Synapses Enhance Motion Sensitivity in a Mature Retinal
Circuit — Sethuramanujam et al., 2017</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2017.09.058` |
| **Authors** | Santhosh Sethuramanujam, Xiaoyang Yao, Geoff deRosenroll, Kevin L. Briggman, Greg D. Field, Gautam B. Awatramani |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2017.09.058` |
| **URL** | https://www.cell.com/neuron/fulltext/S0896-6273(17)30927-3 |
| **Date added** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuron.2017.09.058/summary.md) |

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

## 2016 (1)

<details>
<summary>📖 BluePyOpt: Leveraging Open Source Software and Cloud Infrastructure to
Optimise Model Parameters in Neuroscience — Geit et al., 2016</summary>

| Field | Value |
|---|---|
| **ID** | `10.3389_fninf.2016.00017` |
| **Authors** | Werner Van Geit, Michael Gevaert, Giuseppe Chindemi, Christian Rossert, Jean-Denis Courcol, Eilif B. Muller, Felix Schurmann, Idan Segev, Henry Markram |
| **Venue** | Frontiers in Neuroinformatics (journal) |
| **DOI** | `10.3389/fninf.2016.00017` |
| **URL** | https://www.frontiersin.org/articles/10.3389/fninf.2016.00017/full |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_fninf.2016.00017/summary.md) |

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

## 2012 (2)

<details>
<summary>📖 State and location dependence of action potential metabolic cost in
cortical pyramidal neurons — Hallermann et al., 2012</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn.3132` |
| **Authors** | Stefan Hallermann, Christiaan P. J. de Kock, Greg J. Stuart, Maarten H. P. Kole |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn.3132` |
| **URL** | https://doi.org/10.1038/nn.3132 |
| **Date added** | 2026-05-25 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0124_bedb_dsi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0124_bedb_dsi_atp_per_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/paper/10.1038_nn.3132/summary.md) |

Hallermann, de Kock, Stuart and Kole ask a structural question about brain energy: where,
inside a cortical pyramidal neuron, does the action-potential ATP budget actually go, and what
controls the local energy efficiency at each site. Prior to this study, whole-cell estimates
from Sengupta et al. and Attwell and Laughlin treated the AP as a single number per spike;
Hallermann et al. break that number open into its compartmental contributions and link the
local inefficiency to a single, measurable property of the local waveform.

Methodologically, they combine direct patch-clamp recordings from soma, AIS, axon proper and
nodes of Ranvier in rat neocortical pyramidal cells with a NEURON-based compartmental
simulation. The recorded and simulated AP waveforms are converted into a Na(+)/K(+)
charge-overlap ratio (alpha) that quantifies how much Na(+) entry is "wasted" by simultaneous
K(+) outflow -- and thus how much ATP the Na(+)/K(+) pump must subsequently expend to restore
the ion gradients. The voltage-state dependence of alpha is then tested by varying the resting
membrane potential, and the per-compartment alpha values from the model are integrated to
recover the whole-cell ATP per spike and the share attributable to each compartment.

The headline findings are that AP initiation in the AIS and forward propagation along the axon
are energetically inefficient (alpha > 1, voltage-state dependent), whereas dendritic
backpropagation is efficient (alpha near 1). Per unit area, the AIS and the nodes of Ranvier
are the costliest compartments; per cell, the dendrites and axon collaterals dominate the ATP
budget because of their much larger membrane area. Crucially, the elevated cost of AP
initiation is presented not as a defect but as the biophysical price the cell pays for
reliable high-frequency firing.

For task `t0124`, this paper is directly testable on the top-N NSGA-II Pareto cells: we can
extract per-compartment alpha from each optimised cell, check whether AIS alpha > dendritic
alpha as Hallermann predicts, and use the alpha distribution as a literature-grounded
biological plausibility filter on the Pareto front. The Hallermann paper is in this sense the
natural spatial companion to Sengupta 2010's whole-cell ATP recipe already in use in this
project: Sengupta gives us a single ATP-per-spike number for the cell, Hallermann tells us
what that number must look like when broken down by subcellular compartment, and ModelDB
144526 provides the reference NEURON implementation of the metric.

</details>

<details>
<summary>📖 Updated Energy Budgets for Neural Computation in the Neocortex and
Cerebellum — Howarth et al., 2012</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_jcbfm.2012.35` |
| **Authors** | Clare Howarth, Padraig Gleeson, David Attwell |
| **Venue** | Journal of Cerebral Blood Flow & Metabolism (journal) |
| **DOI** | `10.1038/jcbfm.2012.35` |
| **URL** | https://journals.sagepub.com/doi/10.1038/jcbfm.2012.35 |
| **Date added** | 2026-05-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0124_bedb_dsi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0124_bedb_dsi_atp_per_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/paper/10.1038_jcbfm.2012.35/summary.md) |

Howarth, Gleeson and Attwell (2012) revise the two most-cited bottom-up energy budgets for
mammalian grey matter -- Attwell and Laughlin (2001) for neocortex and Howarth et al. (2010)
for cerebellum -- in light of new mammalian measurements showing that action potentials are
far more energy-efficient than the squid-axon work of Hodgkin (1975) suggested. The research
question is narrow but consequential: when the Na+/K+ temporal-overlap factor drops from 4 to
roughly 1-2, what fraction of grey-matter signalling ATP actually goes into spiking, and how
does the rest redistribute?

The methodology is analytical ATP accounting, not numerical simulation. Each subcellular
process is reduced to an ion flux, ion fluxes are converted to ATP via Na+/K+-ATPase
stoichiometry (1 ATP per 3 Na+), and per-cell totals are weighted by published cell-class
densities to reach grey-matter rates. Cell-type-specific overlap factors are taken from the
new mammalian measurements: **1.24** for cortical pyramidal neurons (Carter and Bean 2009),
**2** for Purkinje and other large cerebellar cells, **1.3** for mossy and climbing fibres
(Alle et al. 2009), and **1.04** for cerebellar granule cells (Sengupta et al. 2010). A
supplementary interactive spreadsheet exposes every parameter for reuse.

The headline finding is a major redistribution of the cortical budget: the action-potential
fraction drops from **47% to 21%**, postsynaptic receptors rise from **34% to 50%** and become
the dominant cost, and total predicted signalling consumption falls from **30 to 20.4 micromol
ATP/g/min**. The cerebellar budget shifts similarly: APs drop from **36% to 17%**, resting
potentials rise from **42% to 54%**, and total falls from **16.5 to 12.8 micromol ATP/g/min**.
Purkinje cells consume only **15%** of cerebellar signalling ATP despite their size, because
granule cells outnumber them 274-fold and consume **67%**.

For t0124, this paper provides the calibrated literature anchor needed by
`compare_literature.md`. The original t0124 plan referenced the Attwell-Laughlin 2001 "47% of
signalling ATP per spike" figure, but that number was superseded by **21%** for cortex and
**17%** for cerebellum in the present paper. Howarth per-cell value for a Purkinje cell --
**8.19 x 10^9 ATP/s** under 1.24-2-style overlap factors -- and the recipe used to derive it
are directly cross-comparable with t0124 per-spike `(1/3)(1/e) integral I_Na^inward` cost,
allowing the Pareto front location on the per-spike-ATP axis to be interpreted against a
published, peer-reviewed band. The 17-21% signalling-ATP-per-spike fraction is also robust to
a 54% change in the assumed overlap factor, so it provides a defensible anchor regardless of
how exactly the DSGC overlap factor is treated.

</details>

## 2011 (1)

<details>
<summary>📖 Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of
Dendritic and Perisomatic Active Properties — Hay et al., 2011</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1002107` |
| **Authors** | Etay Hay, Sean Hill, Felix Schurmann, Henry Markram, Idan Segev |
| **Venue** | PLoS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1002107` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002107 |
| **Date added** | 2026-05-03 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md) |

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

## 2010 (3)

<details>
<summary>📖 Action Potential Energy Efficiency Varies Among Neuron Types in
Vertebrates and Invertebrates — Sengupta et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.1000840` |
| **Authors** | Biswa Sengupta, Martin Stemmler, Simon B. Laughlin, Jeremy E. Niven |
| **Venue** | PLOS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.1000840` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000840 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |
| **Added by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/summary.md) |

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
<summary>📖 Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells:
Using Temperature as an Independent Variable — Fohlmeister et al., 2010</summary>

| Field | Value |
|---|---|
| **ID** | `10.1152_jn.00123.2009` |
| **Authors** | Jürgen F. Fohlmeister, Ethan D. Cohen, Eric A. Newman |
| **Venue** | Journal of Neurophysiology (journal) |
| **DOI** | `10.1152/jn.00123.2009` |
| **URL** | https://journals.physiology.org/doi/10.1152/jn.00123.2009 |
| **Date added** | 2026-04-19 |
| **Categories** | [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/summary.md) |

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

## 2009 (2)

<details>
<summary>📖 Distinct contributions of Nav1.6 and Nav1.2 in action potential
initiation and backpropagation — Hu et al., 2009</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn.2359` |
| **Authors** | Wenqin Hu, Cuiping Tian, Tun Li, Mingpo Yang, Han Hou, Yousheng Shu |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn.2359` |
| **URL** | https://doi.org/10.1038/nn.2359 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn.2359/summary.md) |

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
<summary>📖 Sodium Entry during Action Potentials of Mammalian Neurons: Incomplete
Inactivation and Reduced Metabolic Efficiency in Fast-Spiking Neurons —
Carter & Bean, 2009</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2009.12.011` |
| **Authors** | Brett C. Carter, Bruce P. Bean |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2009.12.011` |
| **URL** | https://www.cell.com/neuron/fulltext/S0896-6273(09)01001-0 |
| **Date added** | 2026-05-25 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0124_bedb_dsi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0124_bedb_dsi_atp_per_spike_nsga2.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/paper/10.1016_j.neuron.2009.12.011/summary.md) |

Carter and Bean address a longstanding gap between the Hodgkin-Huxley squid-axon prediction of
~4-fold-excess Na+ entry per action potential and the actual per-spike metabolic cost of
mammalian central neurons. They use a same-cell paired current-clamp + voltage-clamp protocol
with TTX subtraction at physiological temperature (37 °C) to directly measure integrated
TTX-sensitive Na+ charge during native action potentials in four cell classes: cortical
pyramidal, cerebellar Purkinje, CA1 hippocampal pyramidal, and cortical parvalbumin+
basket-cell interneurons.

The key methodological move is the "sodium entry ratio" -- total Na+ charge per spike divided
by the theoretical minimum (CΔV) needed to swing the membrane through the AP's voltage range.
A ratio of 1.0 means perfect Na+/K+ temporal segregation (no overlap during the falling
phase). A second method comparing total Na+ entry to rising-phase Na+ entry produced nearly
identical results and enabled a cross-waveform experiment in which each cell type's AP was
replayed into every other cell type, decoupling the AP-shape contribution from the
channel-kinetics contribution.

Cortical pyramidal cells achieved 1.24 ± 0.29; Purkinje cells 2.00 ± 0.61; cortical
interneurons 1.98 ± 0.55; CA1 pyramidal 1.62 ± 0.67. Across all 28 neurons, spike width and
sodium entry ratio were inversely correlated (Spearman ρ = -0.48, p = 0.012). The
cross-waveform experiment showed that this correlation is driven by AP shape, not
cell-type-specific channel kinetics: narrow spikes prevent complete Na+ channel inactivation
during the falling phase, allowing extra Na+ influx while driving force is still high. The
mechanism is mediated by Kv3 potassium channels: their fast activation produces narrow spikes
that enable sustained high-frequency firing but double the per-spike metabolic load.

For this project, Carter-Bean 2009 is the load-bearing calibration benchmark for the t0123 /
t0124 ATP-per-spike recipe. The canonical Bed B DSGC's AIS-segregated per-AP per-cm Na+ cost
must land within ±30% of one of Carter-Bean's reference cell types (Purkinje for the
fast-spiking comparator; pyramidal for the slow comparator). The Pareto front t0124 produces
over DSI vs ATP-per-spike is then interpretable in Carter-Bean coordinates: high-DSI cells
with narrow somatic APs should pay a Purkinje-style overlap penalty, while broad-AP cells
should fall on the pyramidal-style efficiency end. This anchors the project's per-spike
metabolic-cost objective to a falsifiable empirical reference rather than a free parameter,
fulfilling REQ-14 of the t0123 / t0124 plan and the project's biological-plausibility
constraint.

</details>

## 2008 (2)

<details>
<summary>📖 Action potential generation requires a high sodium channel density in
the axon initial segment — Kole et al., 2008</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn2040` |
| **Authors** | Maarten H P Kole, Susanne U Ilschner, Björn M Kampa, Stephen R Williams, Peter C Ruben, Greg J Stuart |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn2040` |
| **URL** | https://doi.org/10.1038/nn2040 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1038_nn2040/summary.md) |

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
<summary>📖 Energy limitation as a selective pressure on the evolution of sensory
systems — Niven & Laughlin, 2008</summary>

| Field | Value |
|---|---|
| **ID** | `10.1242_jeb.017574` |
| **Authors** | Jeremy E. Niven, Simon B. Laughlin |
| **Venue** | Journal of Experimental Biology (journal) |
| **DOI** | `10.1242/jeb.017574` |
| **URL** | https://journals.biologists.com/jeb/article/211/11/1792/19035 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1242_jeb.017574/summary.md) |

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

## 2007 (4)

<details>
<summary>📖 A novel multiple objective optimization framework for constraining
conductance-based neuron models by experimental data — Druckmann et al.,
2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.3389_neuro.01.1.1.001.2007` |
| **Authors** | Shaul Druckmann, Yoav Banitt, Albert Gidon, Felix Schurmann, Henry Markram, Idan Segev |
| **Venue** | Frontiers in Neuroscience (journal) |
| **DOI** | `10.3389/neuro.01.1.1.001.2007` |
| **URL** | https://www.frontiersin.org/articles/10.3389/neuro.01.1.1.001.2007/full |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md) |

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
<summary>📖 Axon Initial Segment Kv1 Channels Control Axonal Action Potential
Waveform and Synaptic Efficacy — Kole et al., 2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2007.07.031` |
| **Authors** | Maarten H.P. Kole, Johannes J. Letzkus, Greg J. Stuart |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2007.07.031` |
| **URL** | https://doi.org/10.1016/j.neuron.2007.07.031 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Added by** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1016_j.neuron.2007.07.031/summary.md) |

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
<summary>📖 Different Mechanisms Generate Maintained Activity in ON and OFF Retinal
Ganglion Cells — Margolis & Detwiler, 2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_jneurosci.0130-07.2007` |
| **Authors** | David J. Margolis, Peter B. Detwiler |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/jneurosci.0130-07.2007` |
| **URL** | https://www.jneurosci.org/content/27/22/5994 |
| **Date added** | 2026-04-20 |
| **Categories** | [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1523_jneurosci.0130-07.2007/summary.md) |

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
<summary>📖 Polarized distribution of ion channels within microdomains of the axon
initial segment — Wart et al., 2007</summary>

| Field | Value |
|---|---|
| **ID** | `10.1002_cne.21173` |
| **Authors** | Audra Van Wart, James S. Trimmer, Gary Matthews |
| **Venue** | Journal of Comparative Neurology (journal) |
| **DOI** | `10.1002/cne.21173` |
| **URL** | https://doi.org/10.1002/cne.21173 |
| **Date added** | 2026-04-20 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/10.1002_cne.21173/summary.md) |

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

## 2006 (2)

<details>
<summary>📖 Complex Parameter Landscape for a Complex Neuron Model — Achard &
Schutter, 2006</summary>

| Field | Value |
|---|---|
| **ID** | `10.1371_journal.pcbi.0020094` |
| **Authors** | Pablo Achard, Erik De Schutter |
| **Venue** | PLoS Computational Biology (journal) |
| **DOI** | `10.1371/journal.pcbi.0020094` |
| **URL** | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.0020094 |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.0020094/summary.md) |

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
<summary>📖 Variability, compensation and homeostasis in neuron and network function
— Marder & Goaillard, 2006</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nrn1949` |
| **Authors** | Eve Marder, Jean-Marc Goaillard |
| **Venue** | Nature Reviews Neuroscience (journal) |
| **DOI** | `10.1038/nrn1949` |
| **URL** | https://www.nature.com/articles/nrn1949 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/summary.md) |

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

## 2005 (1)

<details>
<summary>📖 Direction-Selective Dendritic Action Potentials in Rabbit Retina — Oesch
et al., 2005</summary>

| Field | Value |
|---|---|
| **ID** | `10.1016_j.neuron.2005.06.036` |
| **Authors** | Nicholas Oesch, Thomas Euler, W. Rowland Taylor |
| **Venue** | Neuron (journal) |
| **DOI** | `10.1016/j.neuron.2005.06.036` |
| **URL** | https://www.sciencedirect.com/science/article/pii/S089662730500646X |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md) |

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

## 2004 (2)

<details>
<summary>📖 Similar network activity from disparate circuit parameters — Prinz et
al., 2004</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_nn1352` |
| **Authors** | Astrid A. Prinz, Dirk Bucher, Eve Marder |
| **Venue** | Nature Neuroscience (journal) |
| **DOI** | `10.1038/nn1352` |
| **URL** | https://www.nature.com/articles/nn1352 |
| **Date added** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nn1352/summary.md) |

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

## 2003 (1)

<details>
<summary>📖 The Contribution of Resurgent Sodium Current to High-Frequency Firing in
Purkinje Neurons: An Experimental and Modeling Study — Khaliq et al., 2003</summary>

| Field | Value |
|---|---|
| **ID** | `10.1523_JNEUROSCI.23-12-04899.2003` |
| **Authors** | Zayd M. Khaliq, Nathan W. Gouwens, Indira M. Raman |
| **Venue** | The Journal of Neuroscience (journal) |
| **DOI** | `10.1523/JNEUROSCI.23-12-04899.2003` |
| **URL** | https://www.jneurosci.org/content/23/12/4899 |
| **Date added** | 2026-05-03 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |
| **Added by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.23-12-04899.2003/summary.md) |

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

## 2001 (1)

<details>
<summary>📖 An Energy Budget for Signaling in the Grey Matter of the Brain — Attwell
& Laughlin, 2001</summary>

| Field | Value |
|---|---|
| **ID** | `10.1097_00004647-200110000-00001` |
| **Authors** | David Attwell, Simon B. Laughlin |
| **Venue** | Journal of Cerebral Blood Flow & Metabolism (journal) |
| **DOI** | `10.1097/00004647-200110000-00001` |
| **URL** | https://journals.sagepub.com/doi/10.1097/00004647-200110000-00001 |
| **Date added** | 2026-05-08 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1097_00004647-200110000-00001/summary.md) |

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

## 2000 (1)

<details>
<summary>📖 NMDA spikes in basal dendrites of cortical pyramidal neurons — Schiller
et al., 2000</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_35005094` |
| **Authors** | Jackie Schiller, Guy Major, Helmut J. Koester, Yitzhak Schiller |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/35005094` |
| **URL** | https://www.nature.com/articles/35005094 |
| **Date added** | 2026-04-20 |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_35005094/summary.md) |

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

## 1999 (1)

<details>
<summary>📖 A new cellular mechanism for coupling inputs arriving at different
cortical layers — Larkum et al., 1999</summary>

| Field | Value |
|---|---|
| **ID** | `10.1038_18686` |
| **Authors** | Matthew E. Larkum, J. Julius Zhu, Bert Sakmann |
| **Venue** | Nature (journal) |
| **DOI** | `10.1038/18686` |
| **URL** | https://www.nature.com/articles/18686 |
| **Date added** | 2026-04-20 |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Added by** | [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_18686/summary.md) |

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

## 1997 (1)

<details>
<summary>📖 The NEURON Simulation Environment — Hines & Carnevale, 1997</summary>

| Field | Value |
|---|---|
| **ID** | `10.1162_neco.1997.9.6.1179` |
| **Authors** | Michael L. Hines, Nicholas T. Carnevale |
| **Venue** | Neural Computation (journal) |
| **DOI** | `10.1162/neco.1997.9.6.1179` |
| **URL** | https://direct.mit.edu/neco/article/9/6/1179-1209/6087 |
| **Date added** | 2026-04-19 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Added by** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/summary.md) |

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
