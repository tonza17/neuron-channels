---
spec_version: "3"
paper_id: "10.1242_jeb.017574"
citation_key: "Niven2008"
summarized_by_task: "t0097_multi_obj_optim"
date_summarized: "2026-05-08"
---

# Energy limitation as a selective pressure on the evolution of sensory systems

## Metadata

* **File**: `files/niven_2008_energy-sensory-evol.pdf`
* **Published**: 2008
* **Authors**: Jeremy E. Niven 🇬🇧, Simon B. Laughlin 🇬🇧
* **Venue**: Journal of Experimental Biology, 211(11), 1792-1804
* **DOI**: `10.1242/jeb.017574`

## Abstract

Evolution of animal morphology, physiology and behaviour is shaped by the selective pressures to
which they are subject. Some selective pressures act to increase the benefits accrued whilst others
act to reduce the costs incurred, affecting the cost/benefit ratio. Selective pressures therefore
produce a trade-off between costs and benefits that ultimately influences the fitness of the whole
organism. The nervous system has a unique position as the interface between morphology, physiology
and behaviour; the final output of the nervous system is the behaviour of the animal, which is a
product of both its morphology and physiology. The nervous system is under selective pressure to
generate adaptive behaviour, but at the same time is subject to costs related to the amount of
energy that it consumes. Characterising this trade-off between costs and benefits is essential to
understanding the evolution of nervous systems, including our own. Within the nervous system,
sensory systems are the most amenable to analysing costs and benefits, not only because their
function can be more readily defined than that of many central brain regions and their benefits
quantified in terms of their performance, but also because recent studies of sensory systems have
begun to directly assess their energetic costs. Our review focuses on the visual system in
particular, although the principles we discuss are equally applicable throughout the nervous
system. Examples are taken from a wide range of sensory modalities in both vertebrates and
invertebrates. We aim to place the studies we review into an evolutionary framework. We combine
experimentally determined measures of energy consumption from whole retinas of rabbits and flies
with intracellular measurements of energy consumption from single fly photoreceptors and recently
constructed energy budgets for neural processing in rats to assess the contributions of various
components to neuronal energy consumption. Taken together, these studies emphasize the high costs
of maintaining neurons at rest and whilst signalling. A substantial proportion of neuronal energy
consumption is related to the movements of ions across the neuronal cell membrane through ion
channels, though other processes such as vesicle loading and transmitter recycling also consume
energy. Many of the energetic costs within neurons are linked to 3Na+/2K+ ATPase activity, which
consumes energy to pump Na+ and K+ ions across the cell membrane and is essential for the
maintenance of the resting potential and its restoration following signalling. Furthermore, recent
studies in fly photoreceptors show that energetic costs can be related, via basic biophysical
relationships, to their function. These findings emphasize that neurons are subject to a law of
diminishing returns that severely penalizes excess functional capacity with increased energetic
costs. The high energetic costs associated with neural tissue favour energy efficient coding and
wiring schemes, which have been found in numerous sensory systems. We discuss the role of these
efficient schemes in reducing the costs of information processing. Assessing evidence from a wide
range of vertebrate and invertebrate examples, we show that reducing energy expenditure can account
for many of the morphological features of sensory systems and has played a key role in their
evolution.

## Overview

Niven and Laughlin synthesise a decade of empirical and theoretical work on the energetics of
neural tissue and frame it as an evolutionary argument: because the nervous system is metabolically
expensive both at rest and while signalling, natural selection should favour design choices that
maximise information processed per unit ATP, and these efficiency pressures leave detectable
signatures on sensory-system morphology and physiology. The review is structured as a chain of
arguments that descends from whole-animal energy budgets, through cellular and sub-cellular
mechanisms of ATP consumption, to specific design strategies (analogue-vs-digital coding, sparse
coding, wiring minimisation, redundancy reduction, predictive filtering) that can be read as
evolutionary responses to those energy constraints.

The methodological contribution is the integration of three empirical sources into a single
energy-vs-information accounting: (i) whole-retina oxygen consumption measurements from rabbit and
fly, (ii) intracellular electrical-circuit models of single fly R1-6 photoreceptors that compute
3Na+/2K+ ATPase usage from input resistance and membrane potential, and (iii) the Attwell-Laughlin
2001 cortical-grey-matter energy budget plus the Nawroth et al. 2007 olfactory glomerulus budget.
The convergence between the two independent estimates of fly photoreceptor cost (single-cell
biophysical model and bulk retinal O2) shows that ion movement through channels is the dominant
neural energy cost, validating the use of biophysical models for energy-aware design.

The headline conceptual claim is the *Law of Diminishing Returns* for neural function: the cost of
encoding one extra bit of information rises super-linearly with information rate, so excess
bandwidth and excess SNR are aggressively penalised by selection. The review marshals broad
comparative evidence (cave fish eye loss, subterranean mole somatosensory expansion at the expense
of vision, lab Drosophila eye shrinkage, island bovid endocast reduction) to argue that this
single-cell energetic logic propagates up to the morphological scale and explains repeated,
convergent reductions of unused sensory structures.

## Architecture, Models and Methods

The paper is a quantitative review rather than a primary experimental study, but it depends on
three classes of method that it summarises and integrates:

**Whole-tissue oxygen consumption.** Excised retinas from rabbit (Ames et al., 1992) and blowfly
*Calliphora vicina* (Howard et al., 1987; Pangrsic et al., 2005) are placed in respirometry
chambers and O2 consumption is measured at rest and during light stimulation. ATP turnover is
computed assuming 6 ATP per O2 molecule (oxidative phosphorylation). The blowfly retina alone
consumes about **8%** of whole-animal RMR; the human brain consumes about **20%** of BMR while
representing about **2%** of body mass.

**Single-cell biophysical models.** Niven et al. (2003a, 2007) and Laughlin et al. (1998) build
electrical-circuit models of individual fly R1-6 photoreceptors using intracellular measurements of
input resistance, membrane potential, and light-induced conductance changes. The 3Na+/2K+ ATPase
consumption is inferred from the steady-state inward current divided by the 3:2 stoichiometry of
the pump. Information rate (bits s-1) is measured by the standard de Ruyter van Steveninck noise-
substitution method on responses to repeated naturalistic light stimuli. This permits direct
calculation of bit-cost in **ATP molecules per bit**.

**Bottom-up neural energy budgets.** Attwell and Laughlin (2001) tabulate the per-action-potential
ATP cost in rat cortical grey matter, decomposing it into resting potential maintenance,
voltage-gated Na+/K+ currents during the AP, presynaptic Ca2+ entry, glutamate vesicle
endo/exocytosis, glutamate recycling, and post-synaptic NMDA / non-NMDA / mGluR currents. The
budget is then multiplied by neuron and synapse counts. Nawroth et al. (2007) extend this to a rat
olfactory glomerulus, adding dendritic back-propagating APs and dendro-dendritic synapses.

The integration combines all three so that whole-retina O2 figures, single-photoreceptor
biophysical models, and the rat-cortex per-component breakdown can be cross-checked. No new wet-lab
measurements or simulations are reported.

## Results

* In photoreceptors, **resting metabolic cost is approximately 25%** of the cost at the highest
  light levels (Fig. 5), so excess membrane and channel content imposes a large idle-time penalty.
* Action potential transmission and the maintenance of the resting potential together dominate the
  per-AP energy budget in rat grey matter; Attwell and Laughlin (2001) attribute **more than 50%**
  of the per-AP cost to the AP itself plus resting-potential restoration (Fig. 6A).
* The blowfly retina consumes about **8% of resting metabolic rate**, despite being a single
  peripheral structure; the human brain consumes about **20% of BMR** at only **2% body mass**.
* In the homologous R1-6 photoreceptors of *Drosophila melanogaster*, *D. virilis*, *Calliphora
  vicina* and *Sarcophaga carnaria*, both resting and maximum ATP cost scale with information rate
  (bits s-1) (Fig. 5); larger photoreceptors transmit more bits per second but at strictly lower
  energy efficiency (more **ATP per bit**, Fig. 7).
* In *Drosophila* `Shaker` mutants that lack the inactivating Shaker K+ conductance, replacement
  by a non-inactivating leak conductance produces both a **drop in information rate and an
  increase in steady-state energy cost** at rest and while signalling (Fig. 8) - a twofold penalty.
* The cost-per-bit of analogue (graded-potential) signalling is at least as low as that of digital
  (action-potential) signalling for short distances, while analogue can sustain higher information
  rates per second; analogue therefore dominates the early visual periphery and digital dominates
  long-range axons (Sarpeshkar 1998 prediction matches cortical observations).
* Sparse coding is energy-optimal under high signalling cost / low resting cost; the optimal
  fraction of active neurons depends on the resting:signalling cost ratio (Fig. 9, after Attwell
  and Laughlin 2001).
* Convergent eye loss in cave-isolated *Astyanax mexicanus* populations has occurred at least
  three times within roughly **1 million years**, with corresponding reductions in central visual
  processing volume; subterranean *Spalax ehrenbergi*, *Condylura cristata*, and laboratory
  *Drosophila* (Tan et al. 2005, eye size shrinks measurably with years in culture) show similar
  reductions of unused sensory structure.
* Comparative measurements of brain Na+/K+ ATPase activity in elasmobranchs vs teleosts (Nilsson
  et al. 2000) show that elasmobranchs have larger relative brains but lower specific ATPase
  activity, so total brain ATP consumption is comparable across the two clades - relative size is
  not a direct predictor of energy use.

## Innovations

### Joint Information-vs-Energy Accounting at the Single-Cell Level

Earlier energetics work treated information rate (bits s-1) and metabolic cost (ATP s-1)
separately. This review consolidates the case that the two should be plotted against each other on
a single Pareto-style frontier (Fig. 7, **bit-cost vs information rate**), letting the bits-per-ATP
ratio function as a unified efficiency metric. This frontier is exactly the type of objective space
relevant to multi-objective optimisation of single-neuron designs.

### The Law of Diminishing Returns

The review formalises the observation, supported across the four homologous fly photoreceptor
species, that adding extra bandwidth, SNR, or channel density costs an over-proportional amount
of ATP. This converts the qualitative statement that neural tissue is expensive into a concrete
selection rule: any function the cell does not need will be evolutionarily trimmed because the
energy cost grows super-linearly with the unused capacity.

### Cross-Scale Synthesis from Channels to Cave Fish

The paper is the canonical reference that ties single-channel kinetics (Shaker K+ activation and
inactivation) to whole-animal evolutionary phenomena (cave-fish eye loss, mole somatosensory
expansion). The chain channel kinetics -> single-neuron ATP/bit -> sensory-organ size -> lifestyle
fit closes the loop between biophysics and macro-ecology in a way few earlier reviews achieved.

### Energy-Aware Coding Strategies as Evolutionary Endpoints

The review systematically catalogues the menu of mechanisms by which sensory systems can move
toward the bit-per-ATP frontier: matched filtering, sparse coding, hybrid analogue/digital
schemes, wiring minimisation, redundancy reduction via predictive filtering, and efference-copy
gating of sensory feedback. Each is presented not just as a coding trick but as a recurrent
evolutionary outcome.

## Datasets

This is a theoretical/review paper; no datasets were used. The figures re-plot data from earlier
primary studies, particularly Niven et al. (2007) for the four-fly photoreceptor comparison, the
Attwell and Laughlin (2001) and Nawroth et al. (2007) energy budgets, the Zapol et al. (1979)
Weddell seal blood-flow measurements, the McNab and Eisenberg (1989) brain-mass / BMR scaling, the
Nilsson et al. (2000) elasmobranch-vs-teleost ATPase data, and the Tan et al. (2005) lab
*Drosophila* eye-size time series.

## Main Ideas

* For our DSGC project, an objective on **bits per ATP** (or its proxy: spikes per ATP, AP-rate
  per Na+/K+ pump current) is biologically motivated and provides the second axis for a joint
  information-vs-energy Pareto frontier alongside the angle-to-AP-frequency tuning error.
* Resting ATP cost is set by leak and tonically active voltage-gated channels and is roughly
  **25% of peak**; over-provisioned somatic Na+ or K+ density therefore costs the cell
  continuously, not only during the preferred-direction wave. This argues for including idle-state
  cost as part of any energy objective in the multi-objective optimisation.
* Voltage-gated channels with high activation thresholds (only opening near AP threshold) are
  intrinsically cheaper than low-threshold or persistently active channels - useful prior for
  searching the somatic Na/K design space efficiently.
* Excess functional capacity is super-linearly penalised (Law of Diminishing Returns); the
  optimisation should expect to find solutions on a sharp knee where trimming Na+ or K+ density
  beyond the minimum needed for the target AP rate quickly buys back large energy savings.
* Loss-of-conductance mutations (e.g. Drosophila *Shaker*) can pay a **twofold penalty** - both
  reduced information rate and increased energy cost - providing a cautionary example for
  parameter pruning during model simplification.

## Summary

Niven and Laughlin (2008) ask why nervous systems, and sensory systems in particular, take the
specific morphological and biophysical forms they do, and answer that energetics is one of the
dominant selective pressures shaping them. They focus on the visual system because its function is
quantifiable (bits s-1 of information about a visual scene) and its energetic cost is now directly
measurable from whole-retina oxygen consumption, single-cell biophysical models, and bottom-up
per-component energy budgets. The review scope ranges from sub-cellular ion-channel kinetics to
the comparative neuroanatomy of cave fish, blind mole rats, and laboratory-evolved *Drosophila*.

Methodologically, the paper consolidates three classes of measurement into a unified accounting
framework: respirometry on excised retinas, intracellular electrical models of fly R1-6
photoreceptors that infer 3Na+/2K+ ATPase pump current from membrane biophysics, and the
component-level cortical and olfactory energy budgets of Attwell-Laughlin (2001) and Nawroth et
al. (2007). The fact that the single-cell biophysical estimates and the whole-retina O2
measurements agree on the dominant cost (ion movement through the membrane) validates this
multi-scale approach.

The principal findings are quantitative. Resting metabolic cost in fly photoreceptors is about
**25%** of peak signalling cost, and across four homologous photoreceptor species both rest and
peak cost rise faster than information rate, defining a strict bits-per-ATP frontier (Fig. 7).
Action-potential transmission and resting-potential maintenance dominate the per-AP energy budget
in rat grey matter (more than 50%, Fig. 6A), and the choice of channel set has a measurable
energetic signature: removing the *Shaker* K+ conductance in *Drosophila* simultaneously raises
energy cost and lowers information rate (Fig. 8). At larger scales, convergent reductions of
sensory structures (cave-fish eyes, mole visual cortex, lab-Drosophila ommatidia) match the
prediction that unused capacity is selected against, while the elasmobranch-vs-teleost ATPase
comparison warns that brain mass alone is not a reliable proxy for brain energy use.

For this project, the paper anchors the energy axis of a joint info-vs-energy multi-objective
optimisation. The angle-to-AP-frequency tuning error captures the information / function side; an
ATP-budget proxy (Na+/K+ pump current integrated over a stimulus, or equivalently the integrated
voltage-gated channel currents over a trial) captures the cost side. Because resting cost is non-
negligible, the energy proxy must include the idle interval and not only the burst window.
Because the cost-vs-capacity relationship is super-linear, we should expect Pareto fronts with
sharp knees where large energy savings come from trimming over-provisioned somatic Na+ or K+
density. Together with Attwell and Laughlin (2001) and Sengupta et al. (2010), this paper forms
the energy-objective citation set that justifies bits-per-ATP as a biologically grounded second
objective for the multi-objective Na/K conductance search.
