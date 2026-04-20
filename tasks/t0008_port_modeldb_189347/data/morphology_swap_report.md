# Morphology Swap Report: Bundled vs Calibrated DSGC

## Context

ModelDB 189347 ships `RGCmodel.hoc` with a fixed topology:
1 soma + 350 dend sections built via
inline `pt3dadd()` blocks. Synapses are placed on ON-compartments
(identified by the cut `z >= -0.16*y + 46`) with one BIP/SACinhib/
SACexc point process per ON dendrite.

t0009 produced a Horton-Strahler calibrated SWC of a different
DSGC (141009_Pair1DSGC) with full compartmentalization. Importing
this SWC into `RGCmodel.hoc` wholesale would require either:

1. Stripping the bundled `create soma, dend[350]` block and its
   inline 3D geometry (all ~11800 lines of it) and replacing it
   with a SWC loader — but the paper's synapse placement relies
   on `x3d(0..1)`/`y3d(0..1)`/`z3d(n3d()-1)` indices that assume
   the bundled section ordering.
2. Or keeping the bundled HOC topology and treating the calibrated
   SWC as data-for-comparison only.

This task chose option 2: the tuning-curve sweep runs on the
bundled morphology for fidelity to the paper, and we compare the
calibrated SWC here for future work (a deeper port that rebuilds
`RGCmodel.hoc` around a calibrated morphology is out of scope).

## Bundled Morphology (Poleg-Polsky 2016)

| Metric                         | Value              |
| ------------------------------ | ------------------ |
| Soma sections                  | 1 |
| Dend sections                  | 350 |
| Total sections                 | 351 |
| Total segments (nseg sum)      | 351 |
| Total cable length (um)        | 6484.5 |
| Soma diameter at 0.5 (um)      | 5.983027987656088 |
| ON sections (countON)          | 282 |
| Synapses per type (numsyn)     | 282 |
| Synapse locx range (um)        | [16.0, 172.7] |
| Synapse locy range (um)        | [30.5, 221.5] |

The synapse locx/locy values are used verbatim by `placeBIP()` to
compute per-synapse arrival times of the drifting bar.

## Calibrated SWC (t0009 Horton-Strahler)

| Metric                         | Value              |
| ------------------------------ | ------------------ |
| Compartments                   | 6736 |
| Soma compartments              | 19 |
| Dendritic compartments         | 6717 |
| Dendritic cable length (um)    | 1536.3 |
| Min diameter (um)              | 0.879 |
| Max diameter (um)              | 8.235 |
| Mean diameter (um)             | 1.929 |

## Decision

The tuning-curve sweep in this task runs on the bundled Poleg-
Polsky morphology because:

* the paper's ON/OFF cut and synapse-per-dendrite logic are
  tightly coupled to the bundled section ordering and 3D layout;
* the envelope targets (DSI 0.70-0.85, peak 40-80 Hz, null <10 Hz,
  HWHM 60-90 deg) were derived from the bundled morphology, so
  swapping it would need a re-derivation;
* a full rebuild of RGCmodel.hoc around a calibrated SWC is a
  separate task (suggestion in `results/suggestions.json`).

The calibrated SWC stays in t0009 and remains available for the
next iteration.
