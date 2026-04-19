# Brainstorm Results Session 2

## Objective

Second brainstorming session for the neuron-channels project, held after the first wave of tasks
(t0002-t0005) completed. The goal is to translate the literature survey's quantitative targets, the
simulator recommendation, the canonical target tuning curve, and the baseline morphology asset into
a concrete tooling round that lets every downstream compartmental-modelling experiment run without
per-task re-implementation of shared machinery.

## Context

Going into this session:

* **t0002** produced a 20-paper corpus and an answer asset fixing quantitative targets: DSI
  **0.7-0.85**, preferred peak **40-80 Hz**, null residual **< 10 Hz**, HWHM **60-90°**, **177 AMPA
  + 177 GABA** synapses, g_Na **0.04-0.10 S/cm²**.
* **t0003** recommended **NEURON 8.2.7 + NetPyNE 1.1.1** as the primary simulator and **Arbor
  0.12.0** as backup; Brian2 and MOOSE were rejected.
* **t0004** generated the canonical `target-tuning-curve` dataset (cos²-half-rectified, DSI 0.8824,
  HWHM 68.5°, 240-row CSV).
* **t0005** downloaded `dsgc-baseline-morphology` (NeuroMorpho 102976, Feller lab 141009_Pair1DSGC;
  6,736 compartments; 1,536.25 µm dendritic path). Two known caveats: placeholder uniform radius
  0.125 µm, ambiguous source-paper attribution.
* 23 active uncovered suggestions, most concentrated on experiments that cannot run until the
  tooling exists.

No compartmental simulation has run yet.

## Session Outcome

Seven new tasks agreed with the researcher, all `status = not_started`:

* **t0007** — Install and validate NEURON 8.2.7 + NetPyNE 1.1.1. No dependencies.
* **t0008** — Port ModelDB 189347 and similar DSGC compartmental models to NEURON as library assets.
  Depends on t0007, t0005, t0009, t0012.
* **t0009** — Calibrate dendritic diameters on `dsgc-baseline-morphology`. Depends on t0005.
* **t0010** — Literature + code hunt for DSGC compartmental models missed by t0002 and t0008; port
  any found. Depends on t0008.
* **t0011** — Response-visualisation library (firing rate vs angle graphs). Depends on t0004 and
  t0008.
* **t0012** — Tuning-curve scoring loss library. Depends on t0004.
* **t0013** — Resolve `dsgc-baseline-morphology` source-paper provenance and file a corrections
  asset. Depends on t0005.

t0007, t0009, t0012, and t0013 can run in parallel. t0008 gates t0010 and (partially) t0011.

## Corrections Filed

* **S-0004-03** → rejected (redundant with S-0002-09, now covered by t0012).
* **S-0005-04** → reprioritised HIGH → MEDIUM (NEURON loader absorbed into t0008; multi-simulator
  translator only needed once Arbor benchmarking starts).

## Researcher Preferences Captured

* Block t0008 on t0009 — use the calibrated morphology, not the placeholder-radius version.
* t0011 smoke-tests visualisation against both the canonical `target-tuning-curve` and whatever
  t0008 produces.
* Leave `project/budget.json` untouched at `$0.00 / no paid services`; everything runs locally.
* Defer the dendritic-diameter calibration source choice (Vaney/Sivyer/Taylor 2012 vs Poleg-Polsky
  2016 vs other) to t0009's research stage rather than pinning it up front.
* Build a proper scoring library (S-0002-09 covered by t0012), not an ad-hoc inline check inside
  t0008.
