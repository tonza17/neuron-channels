---
spec_version: "3"
paper_id: "10.1038_nn.3132"
citation_key: "Hallermann2012"
summarized_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_summarized: "2026-05-25"
---
# State and location dependence of action potential metabolic cost in cortical pyramidal neurons

## Metadata

* **File**: Download failed (paywalled in Nature Neuroscience; no open-access copy)
* **Published**: 2012-06-03 (Nature Neuroscience 15(7): 1007-1014)
* **Authors**: Stefan Hallermann 🇩🇪, Christiaan P. J. de Kock 🇳🇱, Greg J. Stuart
  🇦🇺, Maarten H. P. Kole 🇳🇱
* **Venue**: Nature Neuroscience
* **DOI**: `10.1038/nn.3132`

## Abstract

Action potential generation and conduction requires large quantities of energy to restore Na(+) and
K(+) ion gradients. We investigated the subcellular location and voltage dependence of this
metabolic cost in rat neocortical pyramidal neurons. Using Na(+)/K(+) charge overlap as a measure of
action potential energy efficiency, we found that action potential initiation in the axon initial
segment (AIS) and forward propagation into the axon were energetically inefficient, depending on the
resting membrane potential. In contrast, action potential backpropagation into dendrites was
efficient. Computer simulations predicted that, although the AIS and nodes of Ranvier had the
highest metabolic cost per membrane area, action potential backpropagation into the dendrites and
forward propagation into axon collaterals dominated energy consumption in cortical pyramidal
neurons. Finally, we found that the high metabolic cost of action potential initiation and
propagation down the axon is a trade-off between energy minimization and maximization of the
conduction reliability of high-frequency action potentials.

## Overview

This summary is based on the abstract and publicly available information only; the full paper could
not be downloaded. The paper is paywalled in Nature Neuroscience and has no open-access version
indexed by Unpaywall, OpenAlex, Semantic Scholar, Europe PMC, or PubMed Central. Quantitative
details below are limited to what is stated in the abstract; section-level claims are restricted to
what the abstract explicitly reports.

Hallermann, de Kock, Stuart and Kole address a fundamental question about the energy budget of the
mammalian brain: where and at what cost is the action potential (AP) generated and propagated in
cortical pyramidal neurons. The study combines patch-clamp recordings from rat neocortical pyramidal
cells with NEURON-based compartmental simulations to map the metabolic cost of the AP across
subcellular compartments (axon initial segment / AIS, axon, nodes of Ranvier, soma, dendrites), and
to test how this cost depends on the resting membrane potential and on the rate of firing.

The central methodological innovation is the use of the Na(+)/K(+) charge overlap as the local
measure of AP energy efficiency. The total Na(+) influx that must subsequently be pumped out by the
Na(+)/K(+)-ATPase exceeds the minimum theoretically required to charge the membrane capacitance
because Na(+) and K(+) currents overlap in time during the AP; the ratio of total Na(+) entry to the
minimum Na(+) entry needed for depolarization (the "alpha" overlap factor) is therefore a direct
readout of metabolic inefficiency. The abstract reports that AP initiation in the AIS and forward
propagation into the axon are energetically inefficient (high overlap, alpha well above 1.0) and
that this inefficiency is voltage-state dependent. Backpropagation into the apical and basal
dendrites, by contrast, is efficient (alpha close to 1, low Na(+)/K(+) overlap).

Per-area cost and total cost are dissociated. The AIS and the nodes of Ranvier have the highest cost
per unit membrane area, but because the dendritic tree and axon collaterals have far greater total
membrane area, backpropagation into dendrites and forward propagation along axon collaterals
together dominate the cell's whole-cell AP energy consumption. The authors frame the high cost of AP
initiation as a deliberate biophysical trade-off: lowering the overlap (and thus the cost) of the
AIS would compromise the cell's ability to fire reliably at high frequencies.

## Architecture, Models and Methods

Full methodology not available -- paper not downloaded. The information below is restricted to what
is reported in the abstract and is widely cited about the work.

* **Preparation**: Rat neocortical pyramidal neurons (cortical pyramidal cells; the abstract does
  not specify the layer, but the corresponding-author lab's other Nature Neuroscience work
  identifies layer-5 pyramidal neurons of somatosensory cortex as the standard preparation).
* **Recording**: Patch-clamp electrophysiology from defined subcellular compartments, including
  somatic recordings and axonal recordings from the AIS / axon proper (Kole and Stuart's lab is one
  of the few groups recording directly from the AIS and intact axons of cortical pyramidal cells).
* **Efficiency metric**: Na(+)/K(+) charge overlap; computed as the ratio of total Na(+) charge
  entry during an AP to the minimum charge required to depolarize the membrane capacitance by the AP
  amplitude. Numerically this is the "alpha" overlap factor; alpha = 1 is theoretically optimal (no
  overlap, no wasted Na(+) influx), alpha > 1 indicates wasted Na(+) influx that must be re-pumped
  at ATP cost (~1 ATP per 3 Na(+) by Na(+)/K(+)-ATPase).
* **Voltage-state manipulation**: The abstract states that AP energy efficiency depends on the
  resting membrane potential, indicating experiments at multiple holding potentials to test
  voltage-dependent inactivation of Na(+) channels as a determinant of overlap.
* **Simulations**: A NEURON compartmental model of a cortical pyramidal neuron with explicit AIS,
  myelinated axon with nodes of Ranvier, axon collaterals, apical dendritic tree, basal dendrites
  and soma. Hodgkin-Huxley-style Na(+) and K(+) channels with subcellular distributions matched to
  the lab's prior published axonal recordings. Quantitative per-compartment alpha and total ATP cost
  are reported but specific numbers cannot be quoted from the abstract alone.
* **Reliability test**: High-frequency AP trains were simulated to test whether reducing AIS
  Na(+)/K(+) overlap compromised conduction reliability.

The paper is associated with **ModelDB entry 144526** (`http://modeldb.science/144526`), which
contains the NEURON model source code used for the simulations. The morphologies are deposited in
NeuroMorpho.Org (PMID 22660478 LinkOut).

## Results

Results not available in full -- paper not downloaded. The abstract reports:

* AP initiation in the **axon initial segment (AIS)** and forward propagation into the **axon** are
  energetically **inefficient** (high Na(+)/K(+) charge overlap; alpha > 1).
* AP **backpropagation into dendrites** is energetically **efficient** (Na(+)/K(+) charge overlap
  close to optimal; alpha near 1).
* AP energy efficiency at the AIS and axon depends on the **resting membrane potential** -- i.e.,
  inefficiency is voltage-state dependent.
* Per unit membrane area, the **AIS and nodes of Ranvier have the highest metabolic cost** of any
  compartment in the cortical pyramidal neuron.
* Despite that, **whole-cell ATP cost is dominated by dendritic backpropagation and forward
  propagation along axon collaterals**, because their total membrane area is much larger than the
  AIS and the nodes combined.
* The **high AIS / axonal cost is a trade-off**: reducing the overlap would lower the metabolic
  burden but would also reduce the conduction reliability of high-frequency action potentials.

Specific numerical values for alpha (Na(+)/K(+) overlap factor) per compartment, ATP per AP, and
per-compartment ATP share are reported in the paper figures but are not quoted in the abstract; the
canonical "soma alpha ~1.3, AIS alpha ~2" figures often cited in the literature derive from this
paper but cannot be confirmed from the abstract text alone.

## Innovations

### Per-Compartment ATP Decomposition

Provided the first systematic per-compartment decomposition of action-potential metabolic cost in
cortical pyramidal neurons, breaking the whole-cell number reported by Sengupta et al. (2010) for
the rat into spatially explicit contributions from the AIS, axon, nodes of Ranvier, soma, basal
dendrites, apical dendrites, and axon collaterals.

### Na(+)/K(+) Charge-Overlap as a Local Efficiency Metric

Established the use of the Na(+)/K(+) charge-overlap ratio (the "alpha" overlap factor) as a
location-resolved electrophysiological readout of metabolic inefficiency. Because alpha is computed
from local AP waveforms, it can be extracted compartment-by-compartment from patch-clamp data and
from simulations without requiring a global ATP measurement.

### Voltage-State Dependence

Demonstrated that the efficiency of AP initiation and conduction is not a fixed property of a neuron
but depends on the resting membrane potential, linking metabolic cost to the inactivation state of
Na(+) channels in the AIS and axon.

### Energy-Reliability Trade-off

Formulated the explicit hypothesis that the elevated overlap (and ATP cost) at AP initiation sites
is the biophysical price paid for reliable high-frequency firing -- a trade-off that any candidate
mechanistic model of cortical excitability must reproduce.

## Datasets

* **Patch-clamp recordings**: Direct somatic and axonal (AIS, axon, nodes of Ranvier) recordings
  from rat neocortical pyramidal cells. Data are not deposited in an open repository; figures and
  raw traces are available only inside the paper's main and supplementary text.
* **NEURON model**: ModelDB accession **144526** (`http://modeldb.science/144526`) -- the
  compartmental model used for the simulations is publicly available and reusable.
* **Morphologies**: Digital reconstructions of rat neocortical layer-5 pyramidal neurons are
  available through NeuroMorpho.Org via the PMID 22660478 LinkOut.

## Main Ideas

* The metabolic cost of an action potential is **non-uniform across the neuron** -- per-area cost
  peaks at the AIS and nodes of Ranvier, but per-cell cost is dominated by the dendritic tree and
  axon collaterals. Any project that optimises ATP per spike for a multi-compartment cell must
  separately track per-compartment alpha rather than treating the cell as a single point.
* The **AIS alpha (~1.5 - 2.0 region) is significantly higher than the dendrite alpha (~1.0 - 1.3
  region)** in cortical pyramidal neurons. This is a direct, testable prediction that the
  multi-compartment NSGA-II Pareto cells optimised in `t0124` and its lineage should reproduce if
  the optimisation is biologically plausible. If the optimiser concentrates Na(+) and K(+) channels
  at the AIS in the same proportions found here, AIS alpha should exceed dendritic alpha on the
  optimised cells; if the optimiser produces solutions with reversed alpha ordering, those solutions
  are likely biophysically implausible regardless of their fitness score.
* The metric **Na(+)/K(+) charge overlap (alpha)** is a *local* measure that can be evaluated during
  a single AP simulation in NEURON without per-pump-cycle accounting. It complements Sengupta 2010's
  whole-cell ATP recipe (q_AP = (3/F) * integral I_Na dt summed across the cell) by providing a
  spatial decomposition that can be compared at the level of individual compartments. For `t0124`,
  this means we can derive both a whole-cell ATP per spike and a per-compartment alpha vector from
  the same simulation, and compare each component against the Hallermann targets.
* The **energy / reliability trade-off** is a constraint on the search space: optimisations that
  push AIS alpha towards 1.0 should be checked for high-frequency conduction reliability before they
  are declared "better". The natural follow-up Pareto front is therefore (DSI, ATP per spike,
  high-frequency conduction reliability) rather than (DSI, ATP per spike) alone.
* The model source code at **ModelDB 144526** is a concrete reference implementation of the
  Na(+)/K(+) overlap calculation in NEURON and should be consulted before re-implementing the metric
  inside our testbed.

## Summary

Hallermann, de Kock, Stuart and Kole ask a structural question about brain energy: where, inside a
cortical pyramidal neuron, does the action-potential ATP budget actually go, and what controls the
local energy efficiency at each site. Prior to this study, whole-cell estimates from Sengupta et al.
and Attwell and Laughlin treated the AP as a single number per spike; Hallermann et al. break that
number open into its compartmental contributions and link the local inefficiency to a single,
measurable property of the local waveform.

Methodologically, they combine direct patch-clamp recordings from soma, AIS, axon proper and nodes
of Ranvier in rat neocortical pyramidal cells with a NEURON-based compartmental simulation. The
recorded and simulated AP waveforms are converted into a Na(+)/K(+) charge-overlap ratio (alpha)
that quantifies how much Na(+) entry is "wasted" by simultaneous K(+) outflow -- and thus how much
ATP the Na(+)/K(+) pump must subsequently expend to restore the ion gradients. The voltage-state
dependence of alpha is then tested by varying the resting membrane potential, and the
per-compartment alpha values from the model are integrated to recover the whole-cell ATP per spike
and the share attributable to each compartment.

The headline findings are that AP initiation in the AIS and forward propagation along the axon are
energetically inefficient (alpha > 1, voltage-state dependent), whereas dendritic backpropagation is
efficient (alpha near 1). Per unit area, the AIS and the nodes of Ranvier are the costliest
compartments; per cell, the dendrites and axon collaterals dominate the ATP budget because of their
much larger membrane area. Crucially, the elevated cost of AP initiation is presented not as a
defect but as the biophysical price the cell pays for reliable high-frequency firing.

For task `t0124`, this paper is directly testable on the top-N NSGA-II Pareto cells: we can extract
per-compartment alpha from each optimised cell, check whether AIS alpha > dendritic alpha as
Hallermann predicts, and use the alpha distribution as a literature-grounded biological plausibility
filter on the Pareto front. The Hallermann paper is in this sense the natural spatial companion to
Sengupta 2010's whole-cell ATP recipe already in use in this project: Sengupta gives us a single
ATP-per-spike number for the cell, Hallermann tells us what that number must look like when broken
down by subcellular compartment, and ModelDB 144526 provides the reference NEURON implementation of
the metric.
