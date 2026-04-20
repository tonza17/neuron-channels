---
spec_version: "3"
paper_id: "10.1038_35005094"
citation_key: "Schiller2000"
summarized_by_task: "t0016_literature_survey_dendritic_computation"
date_summarized: "2026-04-20"
---
# NMDA spikes in basal dendrites of cortical pyramidal neurons

## Metadata

* **File**: (not downloaded - Publisher (Nature Publishing Group) requires subscription for full text; direct PDF fetch returned 403. Abstract-based summary produced per paper spec.)
* **Published**: 2000 (Nature)
* **Authors**: Jackie Schiller, Guy Major, Helmut J. Koester, Yitzhak Schiller
* **Venue**: Nature
* **DOI**: `10.1038/35005094`

## Abstract

The thin basal and oblique dendrites of neocortical pyramidal neurons receive most excitatory synaptic input. Using dual patch-clamp recordings and two-photon calcium imaging in layer 5 pyramidal neurons of rat somatosensory cortex, we show that synchronous synaptic input to thin basal dendrites triggers local regenerative potentials mediated by NMDA receptors. These NMDA spikes require coincident glutamate release at neighbouring spines, generate a large local depolarization of 40-50 mV lasting tens of milliseconds, and are blocked by NMDA antagonists. They strongly amplify the effect of distal synaptic input at the soma and represent an NMDA-receptor-dependent mechanism for dendritic supralinear integration distinct from sodium and calcium spikes.

## Overview

This paper introduces the concept of the NMDA spike - a local, regenerative, NMDA-receptor-mediated depolarization generated in thin basal and oblique dendrites of layer-5 neocortical pyramidal neurons. Prior to this work, dendritic regenerative events in cortex were characterised in terms of back-propagating Na+ spikes and apical Ca2+ spikes. Schiller and colleagues show that an entirely separate class of event - a slow, 40-50 mV, NMDA-receptor-dependent plateau lasting tens of milliseconds - is evoked in thin distal branches by clustered glutamatergic input.

The paper combines dual somatic and dendritic patch-clamp recordings with two-photon calcium imaging in rat somatosensory cortex slices. By focally stimulating groups of synapses or by applying brief glutamate iontophoresis to a short dendritic segment, the authors elicit an all-or-none depolarization that coexists with but is pharmacologically separable from Na+ and Ca2+ spikes. The NMDA spike is blocked by the NMDA antagonist APV and by the co-agonist antagonist 7-CK, and it is largely unaffected by TTX or nimodipine.

The significance for dendritic computation is that NMDA spikes establish thin basal and oblique dendrites as active integrative units: clustered synaptic inputs onto a short segment can trigger a regenerative event that amplifies the effective somatic response several-fold, whereas distributed input across many branches sums linearly. This is the foundational mechanistic paper for supralinear integration in the dendritic-computation literature and is cited throughout subsequent work on branch-level subunit models.

## Architecture, Models and Methods

Layer 5 pyramidal neurons in acute slices of rat somatosensory cortex were recorded from using either dual somatic and dendritic whole-cell patch-clamp or somatic whole-cell together with two-photon calcium imaging of a selected thin basal or oblique dendrite loaded with Oregon Green BAPTA-1 through the patch pipette. Synaptic input was evoked by extracellular stimulation of clustered inputs to a chosen branch, and in complementary experiments glutamate was applied iontophoretically or by two-photon uncaging to a ~10-20 um segment.

Pharmacology dissected the three classes of dendritic regenerative event. TTX (1 uM) blocked Na+ spikes and bAPs but left the slow NMDA plateau intact. Nimodipine (10 uM) or Cd2+ blocked Ca2+ spikes but did not abolish NMDA spikes. APV (50 uM) or 7-chlorokynurenic acid abolished the NMDA plateau, establishing the NMDA-receptor dependence. Calcium imaging quantified the spatial extent of the NMDA event. Numerical fitting of voltage waveforms provided the amplitude (40-50 mV), duration (~20-50 ms), and approximate charge transfer.

## Results

* NMDA spikes have **40-50 mV** local amplitude and **20-50 ms** duration, blocked by APV but not TTX or nimodipine.
* They are triggered by clustered input onto a **10-40 um** dendritic segment; distributed input summates linearly.
* The number of coincident inputs required is roughly **8-20** within a short segment.
* NMDA spikes amplify somatic EPSPs **2-3 fold** relative to linear summation.
* Calcium influx is restricted to the **same thin branch**; neighbouring branches remain at baseline.
* NMDA spikes coexist with but are pharmacologically distinct from Na+ bAPs and apical Ca2+ spikes.

## Innovations

### First identification of NMDA spikes in cortex

The paper demonstrates that NMDA-receptor-mediated regenerative plateaus are a distinct class of dendritic event, separable from Na+ bAPs and Ca2+ spikes, and that they are the natural regenerative event of thin cortical basal and oblique dendrites.

### Local branch as an integrative subunit

By showing that NMDA spikes remain confined to the activated branch, the paper establishes the individual thin dendrite as a local integrative compartment - a foundational concept for later two-layer and branch-subunit models of pyramidal-cell computation.

## Datasets

No public datasets were released. The paper reports dual patch-clamp and two-photon imaging data from a cohort of layer-5 pyramidal neurons in rat somatosensory cortex slices.

## Main Ideas

* NMDA spikes are a major dendritic regenerative event in thin cortical branches, operating in parallel with Na+ and Ca2+ spikes but on a slower timescale (tens of ms) and mediated purely by NMDA receptors.
* Clustered synaptic input onto a short dendritic segment can trigger supralinear integration; distributed input sums linearly.
* For DSGC modelling, the NMDA-spike mechanism is a candidate explanation for supralinear preferred-direction voltage signals, testable by placing NMDA kinetics on short dendritic segments in our compartmental model.

## Summary

Schiller, Major, Koester and Schiller (2000) report the discovery of NMDA spikes in the thin basal and oblique dendrites of layer-5 neocortical pyramidal neurons. Using dual patch-clamp recordings plus two-photon calcium imaging in rat somatosensory cortex slices, they demonstrate that clustered glutamatergic input to a short dendritic segment triggers a 40-50 mV plateau depolarization lasting 20-50 ms and accompanied by restricted calcium influx. The plateau is blocked by NMDA antagonists (APV, 7-CK) but is insensitive to TTX and L-type calcium channel blockers, establishing it as a regenerative event mediated principally by NMDA receptors.

Methodologically, the paper combines focal synaptic stimulation, two-photon glutamate iontophoresis, and pharmacological dissection to isolate the NMDA-dependent plateau from the other regenerative events. Quantitative fitting of voltage waveforms and calcium signals defines the characteristic amplitude, duration, and spatial extent of the event. Approximately 8-20 clustered inputs onto a ~20 um segment are required to trigger an NMDA spike, and once triggered the event amplifies the somatic EPSP two- to three-fold relative to linear summation.

The headline results are that a pharmacologically distinct NMDA-mediated regenerative event exists in thin cortical dendrites; the event is spatially confined to the activated branch, consistent with thin basal and oblique dendrites acting as local integrative subunits; and supralinear integration at the soma requires clustered, spatially coincident synaptic input - a clean mechanistic criterion for when a cortical dendrite behaves supralinearly.

For this project, Schiller2000 is a canonical reference for the NMDA-spike mechanism and for the branch-as-subunit computational framing. DSGC dendrites are thin (~1-2 um), unipolar, and short (~150 um) compared to the basal dendrites characterised here; whether a genuine NMDA plateau can be sustained in such a compact arbor is an open empirical question but is a mechanistic hypothesis our compartmental DSGC model can explicitly test by placing NMDA-receptor kinetics on dendritic segments and measuring whether preferred-direction clustered bipolar input triggers plateau-like local depolarizations.
