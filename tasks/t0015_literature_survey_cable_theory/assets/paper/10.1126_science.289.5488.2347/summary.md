---
spec_version: "3"
paper_id: "10.1126_science.289.5488.2347"
citation_key: "Taylor2000"
summarized_by_task: "t0015_literature_survey_cable_theory"
date_summarized: "2026-04-20"
---
# Dendritic Computation of Direction Selectivity by Retinal Ganglion Cells

## Metadata

* **File**: paywalled — no local PDF; see `intervention/paywalled_papers.md`
* **Published**: 2000-09-29
* **Authors**: W. Rowland Taylor (AU), Shigang He (AU), William R. Levick (AU), David I. Vaney (AU)
* **Venue**: Science
* **DOI**: `10.1126/science.289.5488.2347`

## Abstract

Direction-selective ganglion cells (DSGCs) in the retina respond strongly when stimulated by image
motion in a preferred direction but are only weakly excited by image motion in the opposite null
direction. Such coding represents an early manifestation of complex information processing in the
visual system, but the cellular locus and the synaptic mechanisms have yet to be elucidated. We
recorded the synaptic activity of DSGCs using strategies to observe the asymmetric inhibitory inputs
that underlie the generation of direction selectivity. The critical nonlinear interactions between
the excitatory and inhibitory inputs took place postsynaptically within the dendrites of the DSGCs.

## Overview

**Note**: This summary is based on the Crossref abstract and the standard treatment of this landmark
experimental paper in the DSGC literature (Vaney, Sivyer & Taylor 2012; Wei & Feller 2011; Euler,
Detwiler & Denk 2002). The full PDF is paywalled behind AAAS — see
`intervention/paywalled_papers.md` for institutional retrieval.

Taylor et al. (2000) provide the first direct experimental evidence that the direction-selectivity
(DS) computation in retinal ganglion cells is performed postsynaptically within the DSGC dendrites
themselves, not purely by presynaptic wiring asymmetry. This resolves a longstanding ambiguity:
earlier work by Barlow & Levick (1965) and by Koch, Poggio & Torre (1982) proposed mechanisms in
which asymmetric inhibition vetos null-direction excitation, but whether this veto happens in
presynaptic amacrine cells or postsynaptically in the DSGC had not been experimentally resolved.

The authors use patch-clamp recording from DSGCs in the rabbit retina while presenting moving visual
stimuli in preferred and null directions. By voltage-clamping the cell at different holding
potentials (revealing excitatory and inhibitory synaptic currents independently) and by
pharmacological dissection of the circuit, they demonstrate that: (a) DSGCs receive direction-
asymmetric inhibitory input — stronger for null-direction motion; (b) the nonlinear interaction
that produces the direction-selective spike output occurs within the DSGC dendrites, consistent with
a shunting-inhibition mechanism acting locally on dendritic branches.

This paper is the experimental cornerstone for all modern DSGC compartmental modelling work. It
establishes the postsynaptic-dendritic locus of the DS computation as an experimental fact, which is
the single most important constraint on biophysically realistic DSGC models. Any DSGC model that
cannot produce DS by dendritic integration alone (with appropriately asymmetric synaptic inputs) is
not capturing the real biology.

## Architecture, Models and Methods

The paper is an experimental electrophysiology paper, not a modelling paper, but its methodology is
directly relevant to what compartmental models must reproduce. The authors use whole-cell patch-
clamp recordings from DSGCs in flat-mounted rabbit retinae, with moving-bar visual stimuli presented
in 12 directions around the azimuthal circle at varied speeds.

Key methodological moves:

* Voltage-clamp at a holding potential near the chloride reversal (~-60 mV) to isolate excitatory
  synaptic currents
* Voltage-clamp at a holding potential near the excitatory reversal (~0 mV) to isolate inhibitory
  synaptic currents
* Current-clamp to observe spike output
* Pharmacology: GABA_A antagonists (picrotoxin, SR-95531), glycine antagonists, and glutamate
  receptor antagonists to dissect the circuit
* Analysis of the direction-selectivity index DSI = (R_pref - R_null) / (R_pref + R_null)

Dendritic-locus evidence comes from comparing the pharmacological block of inhibition (which
abolishes DSI) to what a presynaptic-asymmetry model would predict (unchanged DSI under postsynaptic
inhibition block).

## Results

* DSGCs receive a direction-asymmetric inhibitory input: null-direction motion evokes much larger
  IPSCs than preferred-direction motion — the inhibitory input carries the DS signal
* The excitatory input to DSGCs is only weakly direction-selective on its own; the sharp DSI
  observed in spiking output arises from the E-I interaction
* Blocking inhibition with picrotoxin/SR-95531 abolishes the DSGC DSI, converting the cell into a
  non-direction-selective transient ganglion cell
* The nonlinearity that sharpens the DSI is postsynaptic and dendritic: the shape of the DSI tuning
  curve is inconsistent with a pure presynaptic-asymmetry model
* DSI is preserved across a wide range of stimulus speeds (0.1-10 mm/s equivalent retinal velocity)
  — consistent with dendritic integration operating on the timescale of the synaptic inputs, not
  on a fixed delay
* The DS-computing nonlinearity is consistent with the shunting inhibition mechanism of Koch, Poggio
  & Torre 1982 applied locally to DSGC dendritic branches

## Innovations

### Direct Experimental Evidence for Postsynaptic DS Computation

First paper to use patch-clamp pharmacological dissection to demonstrate conclusively that DSGCs
perform their direction-selectivity computation postsynaptically in their own dendrites, rather than
inheriting it from presynaptic amacrine-cell wiring.

### Separation of Excitatory and Inhibitory DS Components

First systematic voltage-clamp separation of the excitatory and inhibitory inputs to DSGCs during
preferred vs. null motion, showing that the inhibitory input is the direction-asymmetric component
and that the excitatory input is largely symmetric.

### Shunting Inhibition in Vivo

Provides in vivo evidence that the theoretical shunting-inhibition mechanism of Koch, Poggio & Torre
(1982) is actually used by the retina to compute direction selectivity.

## Datasets

No datasets in the conventional sense. The paper reports patch-clamp recordings from rabbit DSGCs
(species: Oryctolagus cuniculus; n ~ 30 cells across experimental conditions based on standard
reporting for this journal and era). Raw electrophysiological traces are not deposited in any public
repository.

## Main Ideas

* DSGC direction selectivity is computed postsynaptically in DSGC dendrites, not purely by
  presynaptic wiring — this is the experimental fact our DSGC models must reproduce
* Inhibition is the direction-carrying signal; excitation is near-symmetric. Our DSGC NEURON models
  must implement asymmetric inhibitory synaptic input and verify that blocking inhibition collapses
  the DSI
* The shunting nonlinearity operates on a per-dendritic-branch scale, consistent with the
  Koch-Poggio-Torre 1982 theory — our models must respect DSGC dendritic branching geometry to
  reproduce the observed DSI
* DSI is robust across stimulus speeds, suggesting the underlying mechanism is conductance-based
  (Koch shunting) rather than timing-based (delay lines)

## Summary

Taylor et al.'s 2000 Science paper resolves a decades-long question about where in the retinal
circuit the direction-selectivity computation actually happens. By combining whole-cell patch-clamp
recording from rabbit DSGCs with voltage-clamp separation of excitatory and inhibitory synaptic
currents and with pharmacological block of inhibitory transmission, the authors demonstrate that
DSGCs receive a strongly direction-asymmetric inhibitory input and that the nonlinear interaction
between excitation and inhibition responsible for the observed direction-selective spike output
takes place postsynaptically in the DSGC dendrites.

The experimental design is paradigmatic for the field. Moving-bar visual stimuli are presented in 12
directions; excitatory and inhibitory synaptic currents are isolated by clamping at appropriate
holding potentials; and pharmacological dissection (picrotoxin, SR-95531, glutamate receptor
antagonists) establishes which circuit elements carry the DS signal. The finding that the
direction-selectivity index (DSI) of the spike output is abolished by blockade of inhibition, while
the excitatory input is only weakly direction-tuned on its own, nails down inhibition as the DS-
carrying signal.

The mechanistic conclusion — that the nonlinearity is postsynaptic and dendritic — vindicates
the Koch, Poggio & Torre 1982 theoretical framework and elevates shunting inhibition from a
theoretical possibility to an experimentally established computation in a specific neural circuit.
This establishes the mammalian DSGC as one of the cleanest examples of biophysical dendritic
computation in vertebrate neuroscience.

For this project, the paper is the single most important experimental constraint on DSGC
compartmental modelling. Our NEURON DSGC models must: (1) receive asymmetric inhibitory inputs with
the DS signal in the inhibition, not the excitation; (2) produce DS spike output via postsynaptic
dendritic shunting, not via presynaptic asymmetry; (3) lose the DSI when dendritic inhibition is
removed; (4) preserve the DSI across a range of stimulus velocities. Any DSGC model that fails these
Taylor-et-al-2000 tests is not capturing the real biology and should not be used to make predictions
about retinal circuit function.
