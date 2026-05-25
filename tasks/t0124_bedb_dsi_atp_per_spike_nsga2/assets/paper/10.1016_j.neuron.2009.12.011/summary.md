---
spec_version: "3"
paper_id: "10.1016_j.neuron.2009.12.011"
citation_key: "Carter2009"
summarized_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_summarized: "2026-05-25"
---

# Sodium Entry during Action Potentials of Mammalian Neurons

## Metadata

* **File**: `files/carter_2009_sodium-entry-fast-spiking.html`
* **Published**: 2009
* **Authors**: Brett C. Carter 🇺🇸, Bruce P. Bean 🇺🇸
* **Venue**: Neuron (Cell Press) 2009, vol. 64, issue 6, pages 898-909
* **DOI**: `10.1016/j.neuron.2009.12.011`

## Abstract

We measured the time course of sodium entry during action potentials of mouse central neurons at
37 °C to examine how efficiently sodium entry is coupled to depolarization. In cortical
pyramidal neurons, sodium entry was nearly completely confined to the rising phase of the spike:
only ~25% more sodium enters than the theoretical minimum necessary for spike depolarization.
However, in fast-spiking GABAergic neurons (cerebellar Purkinje cells and cortical interneurons),
twice as much sodium enters as the theoretical minimum. The extra entry occurs because sodium
channel inactivation is incomplete during the falling phase of the spike. The efficiency of
sodium entry in different cell types is primarily a function of action potential shape and not
cell type-specific differences in sodium channel kinetics. The narrow spikes of fast-spiking
GABAergic neurons result in incomplete inactivation of sodium channels; this reduces metabolic
efficiency but likely enhances the ability to fire spikes at high frequency.

## Overview

Carter and Bean directly measure how much sodium current flows during a single action potential
in four classes of acutely dissociated mouse central neurons at physiological temperature
(37 °C). They define a "sodium entry ratio" as total integrated Na+ influx divided by the
theoretical minimum charge needed to depolarize the membrane through the spike's voltage swing
(CΔV). A ratio of 1.0 is the perfect-efficiency limit (Na+ and K+ currents do not overlap
in time); the classical Hodgkin-Huxley squid axon hits ~4.0.

The headline finding is that mammalian cortical pyramidal cells (~90% of cortex) operate near
the efficiency limit at ratio 1.24, whereas fast-spiking GABAergic neurons -- cerebellar Purkinje
cells (2.00) and parvalbumin-positive cortical basket-cell interneurons (1.98) -- burn roughly
twice the minimum Na+ per spike. CA1 hippocampal pyramidal cells sit between these two regimes
at 1.62. This result revises the Attwell-Laughlin 2001 cortical energy budget downward by a
factor of ~3 for glutamatergic spikes, since that budget assumed the squid-axon 4-fold excess.

The paper then dissects the mechanism. By cross-applying recorded action potential waveforms
from one cell type as voltage commands in another cell type, the authors show that the sodium
entry ratio is determined almost entirely by spike shape (in particular AP width), not by
cell-type-specific Na+ channel kinetics. Narrow spikes (Purkinje, interneurons; width
~0.23-0.30 ms) cause incomplete Na+ channel inactivation during the falling phase, allowing
extra Na+ to flow when the driving force is still large; broad spikes (cortical pyramidal; width
~1.21 ms) give Na+ channels enough time to fully inactivate before the falling phase begins. The
trade-off is functional: fast Kv3-driven repolarization that produces narrow spikes enables
sustained high-frequency firing (>200 Hz in Purkinje, 220-350 Hz in interneurons) at the cost of
doubled per-spike metabolic load.

## Architecture, Models and Methods

Acutely dissociated mouse central neurons were prepared from black Swiss mice (postnatal day
14-20). Four cell types were studied: cortical pyramidal neurons (n=8), cerebellar Purkinje
neurons (n=7), CA1 hippocampal pyramidal neurons (n=8), and cortical fast-spiking parvalbumin+
basket-cell interneurons (n=5) identified by EGFP expression in a GAD67-eGFP transgenic line
(Chattopadhyaya 2004, CB6-Tg(Gad1-EGFP)G42Zjh/J).

Recordings used a Multiclamp 700B amplifier with pClamp 9.0 at 200 kHz sampling and 10 kHz
4-pole Bessel filtering. Borosilicate-glass electrodes (1.5-3.0 MΩ) were Parafilm-wrapped to
reduce pipette capacitance to 6.0-12.5 pF. The internal solution contained 140 mM potassium
methanesulfonate, 10 mM NaCl, 1.8 mM MgCl2, 10 mM HEPES, 1 mM EGTA, 0.2 mM CaCl2, 14 mM creatine
phosphate, 4 mM MgATP, 0.3 mM Tris-GTP, pH 7.36. A liquid-junction-potential correction of
-8 mV was applied. Temperature was held at 37 ± 1 °C using a feedback-controlled
resistive heater with quartz flow pipes (250 μm ID) attached to a heated aluminum rod.

The core protocol was a two-step, same-cell measurement. First, the action potential waveform
was recorded in current clamp (either spontaneous or evoked by 10-40 pA injection). Second, the
amplifier was switched to voltage clamp with series-resistance compensation (~90% of 2-10.5
MΩ), and the recorded waveform was replayed as a command. The TTX-sensitive component was
isolated by subtracting traces in partially-blocking TTX (30-90 nM) from traces in fully-blocking
TTX (1 μM), then scaled up by the experimentally measured TTX-block factor. The scaled
trace was integrated over the action potential to give total Na+ charge, then divided by
CΔV (cell capacitance times peak-to-threshold voltage change) to give the sodium entry
ratio.

A second method -- the ratio of total Na+ entry to rising-phase Na+ entry -- gave nearly
identical results without requiring the cell's own AP. This allowed cross-application: each of
the four cell-type AP waveforms was applied to each cell type, isolating the contribution of
channel kinetics versus AP shape. Two independent voltage-clamp-fidelity tests (a second
voltage-recording electrode and GABA_A-current-based voltage readout) confirmed that the command
waveform was imposed on the membrane with peak-voltage deviation of 1.8 ± 1.4 mV and
AP-width deviation of 5 ± 7%. A system time-lag correction of 35-110 μs was applied
per cell. Statistics used the Mann-Whitney rank-sum test and Spearman rank correlation. Funding:
NIH R01-NS36855; F31-NS064630.

## Results

* **Cortical pyramidal neurons**: sodium entry ratio = **1.24 ± 0.29** (n=8); spike width =
  1.21 ± 0.29 ms; AP peak = +19 ± 8 mV; upstroke/downstroke ratio = 6.5 ± 1.3; Na+
  influx = **0.82 ± 0.30 pmol/cm²** per spike.
* **Cerebellar Purkinje neurons**: sodium entry ratio = **2.00 ± 0.61** (n=7); spike width
  = **0.23 ± 0.06 ms**; AP peak = +13 ± 10 mV; upstroke/downstroke ratio = 1.4 ±
  0.4; Na+ influx = **1.54 ± 0.54 pmol/cm²** per spike (significantly greater than
  cortical pyramidal, p = 0.018, Mann-Whitney).
* **Cortical fast-spiking interneurons** (parvalbumin+ basket cells): sodium entry ratio =
  **1.98 ± 0.55** (n=5); spike width = 0.34 ± 0.08 ms; AP peak = 12 ± 7 mV;
  upstroke/downstroke ratio = 1.6 ± 0.5; Na+ influx = **1.36 ± 0.27 pmol/cm²**
  per spike (p = 0.011 vs cortical pyramidal).
* **CA1 hippocampal pyramidal neurons**: sodium entry ratio = **1.62 ± 0.67** (n=8); spike
  width = 0.83 ± 0.33 ms (range 0.41-1.4); AP peak = +18 ± 5 mV; Na+ influx = **1.27
  ± 0.65 pmol/cm²** per spike.
* **Spike-width vs entry-ratio correlation**: Spearman rank coefficient = **-0.48** (p = 0.012,
  n=28 across all four cell types). Narrower spikes give larger excess Na+ entry.
* **Cross-waveform test (Figure 5)**: applying a Purkinje AP to all four cell types produced
  large falling-phase Na+ entry in every cell; applying a cortical pyramidal AP produced
  rising-phase-only Na+ entry in every cell. Sodium entry ratio depends on spike shape, not on
  cell-type-specific channel kinetics.
* **Squid axon comparison**: cortical pyramidal Na+ influx is **~4-fold less** than squid giant
  axon (~4 pmol/spike, Hodgkin-Huxley 1952). Even the least-efficient mammalian case (Purkinje
  at 1.54 pmol/cm²) is well below the squid axon value.
* **Mossy fiber boutons** (Alle et al. 2009): sodium entry ratio of 1.3 despite spike widths
  (0.25-0.38 ms) comparable to fast-spiking neurons. Mossy fiber Na+ channels inactivate ~2-fold
  faster than granule-cell-body channels, so kinetics can override the AP-width effect in
  special axonal compartments.
* **Frequency dependence**: in Purkinje neurons stimulated to fire up to 300 Hz, the sodium
  entry ratio changed very little despite AP broadening with frequency -- broadening (which
  lowers ratio) is counteracted by reduced peak voltage (which lowers inactivation).

## Innovations

### Direct Measurement of Per-Spike Na+ Entry at Physiological Temperature

Prior to this paper, quantitative estimates of cortical Na+ entry per AP rested on the
Hodgkin-Huxley 4-fold-excess number derived from the squid axon at room temperature. Carter and
Bean produced the first systematic same-cell measurements of integrated TTX-sensitive Na+
current during native action potentials in four mammalian cell classes at 37 °C, anchoring
the metabolic-budget literature to mammalian-specific values.

### Sodium Entry Ratio as a Metabolic-Efficiency Benchmark

The paper formalises the sodium entry ratio -- total integrated Na+ charge divided by the
theoretical minimum charge (capacitance times voltage swing) -- as a single-number metric for
how much extra metabolic load each spike costs above the thermodynamic minimum. The ratio of
1.24 for cortical pyramidal cells and 2.00 for fast-spiking GABAergic cells became the canonical
reference values for subsequent biophysical models that need to validate per-spike Na+ pumping
cost (Sengupta 2010, Hallermann 2012, Howarth 2012).

### Cross-Waveform Decoupling of AP Shape from Channel Kinetics

By replaying each cell type's recorded AP into each other cell type as a voltage command, the
authors showed that the sodium entry ratio is set almost entirely by action potential width, not
by cell-type-specific Na+ channel kinetics. This is a mechanistic claim with predictive power:
narrowing the spike of any neuron (e.g. by upregulating Kv3) will increase its per-spike
metabolic cost.

### Mechanistic Link Between Kv3, Fast Spiking, and Metabolic Inefficiency

The paper proposes the now-standard functional trade-off: fast-activating Kv3 channels enable
the rapid repolarization that produces narrow spikes and sustained high-frequency firing, but
the same rapid repolarization prevents Na+ channels from completing inactivation, doubling
per-spike Na+ load. This trade-off explains why nature tolerates 2x metabolic inefficiency in
Purkinje and interneurons -- the cost buys firing-rate bandwidth.

## Datasets

This is a primary electrophysiology paper; no public datasets are released. The raw data
consist of patch-clamp recordings from 28 dissociated mouse neurons (8 cortical pyramidal + 7
cerebellar Purkinje + 5 cortical fast-spiking interneurons + 8 CA1 pyramidal) acquired with a
Multiclamp 700B amplifier and pClamp 9.0 software. Analysis used IGOR Pro (WaveMetrics) with
DataAccess (Bruxton) for file import. Mouse genotype was Black Swiss for three cell types and
CB6-Tg(Gad1-EGFP)G42Zjh/J (Jackson Labs) for the parvalbumin+ basket-cell interneurons.
Postnatal age 14-20 days. The summary statistics (means ± SD, n per cell type) reported in
the paper are the only quantitative data available for downstream reuse.

## Main Ideas

* **The Carter-Bean canonical numbers anchor every per-spike-Na+ benchmark in this project**:
  sodium entry ratio 1.24 for cortical pyramidal, 2.00 for Purkinje, 1.98 for cortical
  fast-spiking interneurons. The t0123 / t0124 smoke gate requires the canonical Bed B DSGC's
  AIS-segregated per-AP per-cm cost to land within 30% of these values (Purkinje for the
  fast-spiking comparator; pyramidal for the non-fast-spiking comparator).
* **Spike width is the dominant predictor of per-spike Na+ cost**, not channel-density choices.
  When the t0124 NSGA-II Pareto front trades DSI vs ATP-per-spike, the optimiser is implicitly
  trading AP-width and Kv3-Na+ overlap. Pareto cells with high ATP-per-spike should have
  narrower / earlier-repolarizing somatic AP waveforms; this is the prediction to verify.
* **The Attwell-Laughlin 2001 cortical signalling-ATP budget overestimates per-spike Na+
  pumping cost by ~3x for glutamatergic neurons** (ratio 1.24, not 4.0). The DSGC is
  glutamatergic-output but with mixed receptor architecture; if its ratio comes in near
  1.2-1.6, it sits in the pyramidal/CA1 regime, not the Purkinje/interneuron regime. This is a
  falsifiable prediction the t0124 Pareto front can resolve.
* **Cell bodies vs axons matter**: Carter-Bean measured somatic action potentials only. Mossy
  fiber boutons (Alle 2009) have narrow spikes (0.25-0.38 ms) but still ratio ~1.3 because
  bouton Na+ channels inactivate twice as fast as cell-body channels. The DSGC AIS has its own
  Nav1.6 population with distinct kinetics; the project's AIS-segregated Carter-Bean smoke-gate
  must allow this caveat in its ±30% tolerance.
* **Higher-frequency firing does not strongly change per-spike sodium entry ratio in Purkinje
  cells up to 300 Hz**, so the smoke-gate evaluation can use single-spike or low-frequency
  measurements without correcting for the firing rate the DSGC operates at (~20-60 Hz under
  preferred-direction wave stimulation).

## Summary

Carter and Bean address a longstanding gap between the Hodgkin-Huxley squid-axon prediction of
~4-fold-excess Na+ entry per action potential and the actual per-spike metabolic cost of
mammalian central neurons. They use a same-cell paired current-clamp + voltage-clamp protocol
with TTX subtraction at physiological temperature (37 °C) to directly measure integrated
TTX-sensitive Na+ charge during native action potentials in four cell classes: cortical
pyramidal, cerebellar Purkinje, CA1 hippocampal pyramidal, and cortical parvalbumin+ basket-cell
interneurons.

The key methodological move is the "sodium entry ratio" -- total Na+ charge per spike divided
by the theoretical minimum (CΔV) needed to swing the membrane through the AP's voltage
range. A ratio of 1.0 means perfect Na+/K+ temporal segregation (no overlap during the falling
phase). A second method comparing total Na+ entry to rising-phase Na+ entry produced nearly
identical results and enabled a cross-waveform experiment in which each cell type's AP was
replayed into every other cell type, decoupling the AP-shape contribution from the
channel-kinetics contribution.

Cortical pyramidal cells achieved 1.24 ± 0.29; Purkinje cells 2.00 ± 0.61; cortical
interneurons 1.98 ± 0.55; CA1 pyramidal 1.62 ± 0.67. Across all 28 neurons, spike
width and sodium entry ratio were inversely correlated (Spearman ρ = -0.48, p = 0.012). The
cross-waveform experiment showed that this correlation is driven by AP shape, not
cell-type-specific channel kinetics: narrow spikes prevent complete Na+ channel inactivation
during the falling phase, allowing extra Na+ influx while driving force is still high. The
mechanism is mediated by Kv3 potassium channels: their fast activation produces narrow spikes
that enable sustained high-frequency firing but double the per-spike metabolic load.

For this project, Carter-Bean 2009 is the load-bearing calibration benchmark for the t0123 /
t0124 ATP-per-spike recipe. The canonical Bed B DSGC's AIS-segregated per-AP per-cm Na+ cost
must land within ±30% of one of Carter-Bean's reference cell types (Purkinje for the
fast-spiking comparator; pyramidal for the slow comparator). The Pareto front t0124 produces
over DSI vs ATP-per-spike is then interpretable in Carter-Bean coordinates: high-DSI cells with
narrow somatic APs should pay a Purkinje-style overlap penalty, while broad-AP cells should
fall on the pyramidal-style efficiency end. This anchors the project's per-spike metabolic-cost
objective to a falsifiable empirical reference rather than a free parameter, fulfilling REQ-14
of the t0123 / t0124 plan and the project's biological-plausibility constraint.
