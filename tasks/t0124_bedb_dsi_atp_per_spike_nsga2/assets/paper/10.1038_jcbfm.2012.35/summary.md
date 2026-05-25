---
spec_version: "3"
paper_id: "10.1038_jcbfm.2012.35"
citation_key: "Howarth2012"
summarized_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_summarized: "2026-05-25"
---
# Updated Energy Budgets for Neural Computation in the Neocortex and Cerebellum

## Metadata

* **File**: `files/howarth_2012_updated-energy-budgets.pdf`
* **Published**: 2012-03-21
* **Authors**: Clare Howarth (Canada), Padraig Gleeson (UK), David Attwell (UK)
* **Venue**: Journal of Cerebral Blood Flow and Metabolism, 32(7), 1222-1232
* **DOI**: `10.1038/jcbfm.2012.35`

## Abstract

The brain energy supply determines its information processing power, and generates functional
imaging signals. The energy use on the different subcellular processes underlying neural information
processing has been estimated previously for the grey matter of the cerebral and cerebellar cortex.
However, these estimates need reevaluating following recent work demonstrating that action
potentials in mammalian neurons are much more energy efficient than was previously thought. Using
this new knowledge, this paper provides revised estimates for the energy expenditure on neural
computation in a simple model for the cerebral cortex and a detailed model of the cerebellar cortex.
In cerebral cortex, most signaling energy (50%) is used on postsynaptic glutamate receptors, 21% is
used on action potentials, 20% on resting potentials, 5% on presynaptic transmitter release, and 4%
on transmitter recycling. In the cerebellar cortex, excitatory neurons use 75% and inhibitory
neurons 25% of the signaling energy, and most energy is used on information processing by
non-principal neurons: Purkinje cells use only 15% of the signaling energy. The majority of
cerebellar signaling energy use is on the maintenance of resting potentials (54%) and postsynaptic
receptors (22%), while action potentials account for only 17% of the signaling energy use.

## Overview

This paper revises the influential bottom-up energy budgets for grey matter neural computation
originally published by Attwell and Laughlin (2001) for the rat neocortex and by Howarth, Peppiatt
Wildman and Attwell (2010) for the rat cerebellum. The revision is driven by new experimental and
modelling work (Alle et al. 2009; Carter and Bean 2009; Sengupta et al. 2010) showing that mammalian
action potentials are much closer to the thermodynamic minimum than the squid-axon-based factor of 4
over-estimate used in the original budgets. Specifically, the temporal overlap between inward Na+
and outward K+ currents is much smaller than Hodgkin (1975) measured in squid, so the multiplier on
minimum charge entry needed to obtain actual Na+ entry per spike ranges from 1.04 (cerebellar
granule cells) to 2 (Purkinje cells), versus the legacy value of 4.

Replacing this single coefficient propagates through the entire budget. For neocortex the
action-potential fraction of signalling ATP drops from **47% to 21%**, the postsynaptic-receptor
fraction rises from **34% to 50%**, and total predicted signalling consumption falls from **30 to
20.4 micromol ATP/g/min** (a 32% reduction). For cerebellar cortex the action-potential fraction
drops from **36% to 17%**, resting-potential fraction rises from **42% to 54%**, and total
signalling consumption falls from **16.5 to 12.8 micromol ATP/g/min** (a 22% reduction). A central
qualitative conclusion -- that principal output neurons (Purkinje cells) are not the dominant energy
consumers in the cerebellum -- is strengthened, not weakened, by the revision: Purkinje cells now
account for only **15%** of cerebellar signalling energy, with granule cells consuming **67%**
because of their **274-fold higher density**.

The paper also ships an interactive spreadsheet so readers can substitute their own assumed overlap
factors, firing rates and synapse densities. A sensitivity analysis shows that the core conclusions
are robust: even with a conservative overlap factor of **1.6** for granule cells (instead of 1.04),
total cerebellar signalling consumption is **13.3 micromol ATP/g/min** (only +3.9%), and
resting-potential maintenance still dominates at **52%**.

## Architecture, Models and Methods

The paper uses an analytical bottom-up ATP accounting model, not a numerical compartmental
simulation. Each subcellular process is converted into an ion flux, each ion flux is converted into
ATP consumption via stoichiometry, and the per-cell totals are scaled by cell-class densities to
reach grey-matter-wide rates in micromol ATP/g/min.

Conversion stoichiometry: the Na+/K+-ATPase uses **1 ATP per 3 Na+ extruded**; Ca2+ extrusion via 3
Na+/Ca2+ exchange followed by Na+ pump-out uses **1 ATP per Ca2+ extruded**. Cl- restoration after
IPSPs is shown to be < 1% of an equivalent Na+ restoration cost and is therefore ignored.

Action potential ATP per spike is computed as: minimum charge to charge the membrane through the AP
voltage swing, multiplied by an overlap factor, divided by 3 times the elementary charge. The
overlap factor is the single coefficient that captures temporal Na+/K+ overlap. Values used in the
revised budgets:

* **Neocortex pyramidal neurons**: **1.24** (Carter and Bean 2009) -- only 24% excess over the
  theoretical minimum; legacy value was 4.
* **Purkinje cells, Golgi cells, molecular-layer interneurons**: **2** (Carter and Bean 2009 on
  Purkinje).
* **Cerebellar granule cells**: **1.04** (Sengupta et al. 2010, modelling) -- a near-perfect spike.
  A more conservative **1.6** (Carter and Bean 2009 on CA1) is also presented as a sensitivity test.
* **Mossy and climbing fibres**: **1.3** (Alle et al. 2009, hippocampal mossy fibre).

Five subcellular ATP categories are tallied for each cell type: resting potential, action potential,
postsynaptic receptors (NMDA + non-NMDA Na+ and Ca2+ fluxes plus G-protein signalling),
neurotransmitter recycling, and presynaptic Ca2+ entry plus vesicle cycling. Cerebellar calculations
include nine cell classes (Purkinje, granule, Golgi, basket, stellate, climbing fibre, mossy fibre,
astrocyte, Bergmann glia), each with its own membrane area, synapse count, firing rate and overlap
factor. The neocortex calculation lumps all neurons as glutamatergic firing at **4 Hz** (because 90%
of cells and synapses are glutamatergic), as in Attwell and Laughlin 2001.

Housekeeping (non-signalling) energy is treated separately and tuned so total predicted consumption
matches the measured rate of **33-50 micromol ATP/g/min** (rat cortex) or **20.5 micromol
ATP/g/min** (rat cerebellum) from Sokoloff et al. (1977).

## Results

* **Neocortex action-potential signalling fraction drops from 47% (Attwell-Laughlin 2001) to 21%**
  -- the headline revision.
* **Neocortex postsynaptic-receptor fraction rises from 34% to 50%** and becomes the dominant cost;
  resting potentials account for **20%**, presynaptic Ca2+/vesicle cycling for **5%**, transmitter
  recycling for **4%**.
* **Cerebellar action-potential signalling fraction drops from 36% (Howarth et al. 2010) to 17%**;
  resting potentials rise from **42% to 54%** and become dominant; postsynaptic receptors rise from
  **17% to 22%**.
* **Total neocortex signalling consumption falls from 30 to 20.4 micromol ATP/g/min** (-32%);
  **total cerebellar signalling consumption falls from 16.5 to 12.8 micromol ATP/g/min** (-22%).
* **Per-cell ATP usage**: a Purkinje cell uses **8.19 x 10^9 ATP/s** (down 34% from 1.24 x 10^10); a
  granule cell uses **1.32 x 10^8 ATP/s** (down 23% from 1.72 x 10^8).
* **Density wins over size**: Purkinje cells consume only **15%** of cerebellar signalling ATP
  despite being **62x larger** per cell than granule cells, because granule cells outnumber them
  **274-fold** and therefore consume **67%**.
* **Inhibitory vs excitatory split in cerebellum**: excitatory cells **75%**, inhibitory cells
  **25%** of signalling ATP.
* **Three-stage cerebellar pipeline split**: input remapping **53%**, sparse-code propagation
  **32%**, Purkinje output computation **15%** -- most energy is on pre-output processing.
* **Laminar reversal**: granular layer **57%** vs molecular layer **43%** of cerebellar ATP, a
  reversal of the 46:54 ratio in the old budget; the new ratio matches measured blood-vessel surface
  area (42% molecular : 58% granular) far better than membrane area (8.6-fold larger in molecular
  layer).
* **Sensitivity check**: using a granule-cell overlap factor of **1.6** instead of **1.04** changes
  total cerebellar signalling consumption from **12.8 to 13.3 micromol ATP/g/min** (+3.9%) and total
  AP fraction from **17% to 20%** -- main conclusions unaffected.

## Innovations

### Revised AP-Overlap Factor Anchored to Mammalian Measurements

The paper replaces a single legacy coefficient -- Hodgkin squid-axon overlap factor of 4 -- with
cell-type-specific mammalian values (1.04 to 2). Although the underlying experimental and modelling
work is from Alle, Carter-Bean and Sengupta, this paper is the first to propagate the correction
through full grey-matter ATP budgets for neocortex and cerebellum, providing the "updated" reference
numbers that downstream literature now cites.

### Layer-Level Energy and Supply Match in Cerebellum

The revision flips the predicted laminar distribution of cerebellar ATP from molecular-dominant
(54:46) to granular-dominant (57:43). The new prediction aligns with measured blood-vessel surface
area (58% in molecular layer vs 42% in granular) far better than with raw membrane area (8.6x larger
in molecular layer than granular layer). This argues that vascularization tracks energy demand, not
crude membrane area -- a falsifiable prediction about brain microvascular adaptation.

### Public Interactive Spreadsheet

The supplementary spreadsheet exposes every parameter (overlap factor, firing rate, synapse density,
channel kinetics) and recomputes the full budget when readers change them. This makes the model an
explicit calibration target rather than a black-box headline number, which is the form in which
t0124 needs it.

## Datasets

This is a theoretical/modelling paper; no datasets were used. The model is parameterised from prior
published anatomical and electrophysiological literature: Attwell and Laughlin (2001) and Howarth,
Peppiatt Wildman and Attwell (2010) provide the morphology, synapse counts and firing rates; Alle et
al. (2009), Carter and Bean (2009) and Sengupta et al. (2010) provide the revised mammalian overlap
factors. Total energy-consumption rates for comparison come from Sokoloff et al. (1977) for
conscious rat (cortex: 33-50 micromol ATP/g/min; cerebellum: 20.5 micromol ATP/g/min). Blood-vessel
surface-area distributions for the cerebellar laminar comparison come from Howarth et al. (2010), n
= 3 rats. An interactive supplementary spreadsheet is released as the canonical implementation of
all calculations.

## Main Ideas

* **The headline number for t0124 comparison to literature is no longer the Attwell-Laughlin 2001
  47% figure -- it is the revised 21% for cortex (this paper, 2012)**. Any text in the task that
  anchors to "47% of cortical signalling ATP goes to action potentials" is using a superseded number
  and must be updated to 21% with this paper as the citation.
* **The mammalian Na+/K+ overlap factor relevant to a retinal ganglion cell is closer to 1.24 than
  to 4**. Carter and Bean pyramidal-neuron value of 1.24 is the appropriate prior for a generic
  non-Purkinje, non-granule cell -- it is the same value Howarth uses for cerebral cortex as a
  whole.
* **Per-spike ATP cost in this budget is computed exactly as t0124 implements it**: minimum charge
  to charge the membrane through the AP voltage swing, times an overlap factor, divided by 3e (one
  ATP per 3 Na+ pumped). t0124 `(1/3) * (1/e) * sum_compartments int(I_Na^inward) dt` recipe is the
  per-compartment integral form of the same accounting and produces the measurement counterpart of
  Howarth predicted per-cell value -- the recipes are cross-comparable.
* **Principal-cell firing is not the dominant energy consumer**: in the cerebellum, Purkinje cells
  use only **15%** of signalling ATP while granule cells use **67%**, because density beats size.
  For DSGC modelling, this reinforces that synaptic and resting-potential costs may dominate over
  spike costs at the system level even when the modelled cell is itself a principal output neuron.
* **Sensitivity to the overlap factor is bounded**: moving from 1.04 to 1.6 (a 54% change in the
  factor) only shifts the total AP fraction by 3 percentage points (17% to 20%). For t0124
  Pareto-front interpretation this means the **17-21% signalling-ATP band** is a robust anchor
  across the plausible range of overlap factors.

## Summary

Howarth, Gleeson and Attwell (2012) revise the two most-cited bottom-up energy budgets for mammalian
grey matter -- Attwell and Laughlin (2001) for neocortex and Howarth et al. (2010) for cerebellum --
in light of new mammalian measurements showing that action potentials are far more energy-efficient
than the squid-axon work of Hodgkin (1975) suggested. The research question is narrow but
consequential: when the Na+/K+ temporal-overlap factor drops from 4 to roughly 1-2, what fraction of
grey-matter signalling ATP actually goes into spiking, and how does the rest redistribute?

The methodology is analytical ATP accounting, not numerical simulation. Each subcellular process is
reduced to an ion flux, ion fluxes are converted to ATP via Na+/K+-ATPase stoichiometry (1 ATP per 3
Na+), and per-cell totals are weighted by published cell-class densities to reach grey-matter rates.
Cell-type-specific overlap factors are taken from the new mammalian measurements: **1.24** for
cortical pyramidal neurons (Carter and Bean 2009), **2** for Purkinje and other large cerebellar
cells, **1.3** for mossy and climbing fibres (Alle et al. 2009), and **1.04** for cerebellar granule
cells (Sengupta et al. 2010). A supplementary interactive spreadsheet exposes every parameter for
reuse.

The headline finding is a major redistribution of the cortical budget: the action-potential fraction
drops from **47% to 21%**, postsynaptic receptors rise from **34% to 50%** and become the dominant
cost, and total predicted signalling consumption falls from **30 to 20.4 micromol ATP/g/min**. The
cerebellar budget shifts similarly: APs drop from **36% to 17%**, resting potentials rise from **42%
to 54%**, and total falls from **16.5 to 12.8 micromol ATP/g/min**. Purkinje cells consume only
**15%** of cerebellar signalling ATP despite their size, because granule cells outnumber them
274-fold and consume **67%**.

For t0124, this paper provides the calibrated literature anchor needed by `compare_literature.md`.
The original t0124 plan referenced the Attwell-Laughlin 2001 "47% of signalling ATP per spike"
figure, but that number was superseded by **21%** for cortex and **17%** for cerebellum in the
present paper. Howarth per-cell value for a Purkinje cell -- **8.19 x 10^9 ATP/s** under
1.24-2-style overlap factors -- and the recipe used to derive it are directly cross-comparable with
t0124 per-spike `(1/3)(1/e) integral I_Na^inward` cost, allowing the Pareto front location on the
per-spike-ATP axis to be interpreted against a published, peer-reviewed band. The 17-21%
signalling-ATP-per-spike fraction is also robust to a 54% change in the assumed overlap factor, so
it provides a defensible anchor regardless of how exactly the DSGC overlap factor is treated.
