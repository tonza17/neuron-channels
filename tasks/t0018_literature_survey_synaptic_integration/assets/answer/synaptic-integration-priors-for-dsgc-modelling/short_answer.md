---
spec_version: "2"
answer_id: "synaptic-integration-priors-for-dsgc-modelling"
answered_by_task: "t0018_literature_survey_synaptic_integration"
date_answered: "2026-04-20"
---
## Question

What quantitative priors does the synaptic-integration literature supply for the DSGC compartmental
model on (1) AMPA/NMDA/GABA receptor kinetics, (2) shunting inhibition, (3) E-I balance temporal
co-tuning, (4) dendritic-location-dependent PSP integration, and (5) SAC-to-DSGC inhibitory
asymmetry?

## Answer

Receptor kinetics: AMPA uses a fast bi-exponential conductance (rise ~0.2 ms, decay ~1-3 ms, Erev 0
mV); NMDA uses a slow conductance (rise ~5-10 ms, decay ~50-100 ms, Erev 0 mV) with Jahr-Stevens
Mg2+ block; GABA_A uses a fast bi-exponential (rise ~0.5 ms, decay ~5-10 ms, Erev -65 to -75 mV).
Shunting inhibition vetoes excitation multiplicatively with an "on-the-path" geometry: only
inhibition sitting between the excitatory input and the soma shunts PSP amplitude, while distal
inhibition has negligible effect. Excitation and inhibition co-tune in time with inhibition lagging
excitation by ~1-3 ms in cortex and ~15-50 ms in DSGCs during null-direction motion, sharpening
spike timing. Somatic PSP amplitude decays roughly exponentially with electrotonic distance
(lambda_DC ~100-300 um for RGC dendrites) while local dendritic non-linearities (Na+, Ca2+, NMDAR)
partially compensate for distal attenuation. SAC boutons onto a DSGC dendrite are spatially
asymmetric with stronger inhibition from null-side SACs, and this cellular asymmetry (not somatic
E-I timing alone) is the primary substrate for direction selectivity at the DSGC level.

## Sources

* Paper: `10.1038_346565a0` (Lester, Clements, Westbrook, Jahr 1990)
* Paper: `10.1073_pnas.80.9.2799` (Koch, Poggio, Torre 1983)
* Paper: `10.1038_nature02116` (Wehr & Zador 2003)
* Paper: `no-doi_HausserMel2003_s0959-4388-03-00075-8` (Hausser & Mel 2003)
* Paper: `10.1038_nature00931` (Euler, Detwiler, Denk 2002)
