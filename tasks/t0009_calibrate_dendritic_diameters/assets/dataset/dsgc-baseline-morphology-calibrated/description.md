---
spec_version: "2"
dataset_id: "dsgc-baseline-morphology-calibrated"
summarized_by_task: "t0009_calibrate_dendritic_diameters"
date_summarized: "2026-04-19"
---
# DSGC Baseline Morphology (141009_Pair1DSGC), Diameter-Calibrated

## Metadata

* **Name**: DSGC Baseline Morphology (141009_Pair1DSGC), Diameter-Calibrated
* **Year**: 2026
* **Authors**: t0009_calibrate_dendritic_diameters (Glite ARF project)
* **License**: CC-BY-4.0 (inherited from `dsgc-baseline-morphology`; diameter source `RGCmodel.hoc`
  MIT-licensed on the Hanson `geoffder/Spatial-Offset-DSGC-NEURON-Model` mirror of ModelDB 189347)
* **Access**: public
* **Size**: 6,736 compartments; 19 soma rows + 6,717 dendrite rows; 129 branch points; 131 leaves;
  1,536.25 µm total dendritic path length; four distinct radii (soma 4.118 µm, primary 3.694 µm, mid
  1.653 µm, terminal 0.439 µm)

## Overview

This dataset is a diameter-calibrated variant of `dsgc-baseline-morphology` (NeuroMorpho neuron
102976, `141009_Pair1DSGC`), the CNG-curated SWC reconstruction of a mouse ON-OFF
direction-selective ganglion cell recorded by Murphy-Baum and Feller at UC Berkeley. The source SWC
carries the placeholder radius **0.125 µm on every one of its 6,736 compartments** because the
upstream Simple Neurite Tracer reconstruction did not record diameters. A uniform placeholder makes
the file unusable as a biophysical input — axial resistance scales with `1/r^2` and surface area
scales with `r`, so leaving every compartment at the same thin radius silently biases every
downstream compartmental simulation.

This calibrated asset replaces the uniform placeholder with a literature-grounded per-Strahler-
order taper. Topology is **unchanged**: compartment ids, type codes, parent ids, and xyz coordinates
are copied byte-for-byte from the source SWC. Only the radius column is rewritten. The diameter
source is the Poleg-Polsky & Diamond 2016 NEURON model (ModelDB 189347), which distributes the
identical mouse ON-OFF DSGC morphology as a `.hoc` template with explicit `pt3dadd(x, y, z, diam)`
calls per section. Soma, primary dendrite, mid dendrite, and terminal dendrite radii are harvested
from the `.hoc` and applied here by compartment class — the same three-bin soma/primary/terminal
partition used by every published NEURON DSGC model (Poleg-Polsky & Diamond 2016, Hanson et al.
2019, Jain et al. 2020, Schachter et al. 2010).

## Content & Annotation

The dataset contains a single file: `files/141009_Pair1DSGC_calibrated.CNG.swc` in the SWC format
defined by the NeuroMorpho CNG standard. Each row encodes one compartment with seven
whitespace-separated fields: id, type code, x, y, z, radius, parent id. Type code 1 is soma and type
code 3 is (basal) dendrite; no axonal or apical compartments are present. Coordinates are in
micrometres and use the source file's coordinate frame unchanged.

Annotation is the per-compartment radius. The calibrated radii are assigned as follows:

| Class | Strahler order | Radius (µm) | N compartments |
| --- | --- | --- | --- |
| Soma | sentinel 0 | 4.118 | 19 |
| Primary dendrite | order == max_order (5) | 3.694 | varies |
| Mid dendrite | 1 < order < max_order | 1.653 | varies |
| Terminal dendrite | order == 1 | 0.439 | varies |

Strahler order is computed on the SWC tree by an iterative post-order DFS with the maximum-child
tie-break (if a node has children with maximum order `k` appearing in two or more children, the
node's order is `k+1`; otherwise the node's order is `max(children)`). Soma rows keep a sentinel
order of 0 to prevent them from being misclassed as "primary" by the dendrite rule. The source
header `#` comment lines are replaced with a calibration-provenance header that cites the source SWC
path, the Poleg-Polsky paper DOI, the `.hoc` SHA-256 checksum, the Strahler-order rule, and both
radius floors.

## Statistics

| Metric | Value |
| --- | --- |
| Total compartments | 6,736 |
| Soma compartments | 19 |
| Dendrite compartments | 6,717 |
| Branch points | 129 |
| Leaves | 131 |
| Total dendritic length | 1,536.25 µm |
| Max Strahler order | 5 |
| Distinct dendritic radii | 3 |
| Terminal radius (assigned) | 0.439 µm |
| Mid radius (assigned) | 1.653 µm |
| Primary radius (assigned) | 3.694 µm |
| Soma radius (assigned) | 4.118 µm |
| Terminal-radius clamps applied | 0 |
| Total surface area (calibrated) | 9,700 µm² |
| Total surface area (placeholder baseline) | 1,213 µm² |
| Surface area ratio (calibrated / placeholder) | 7.99 × |
| Total dendritic axial resistance (calibrated) | 1.50 × 10⁹ Ω |
| Total dendritic axial resistance (placeholder) | 3.13 × 10¹⁰ Ω |
| Axial resistance ratio (calibrated / placeholder) | 0.048 |

Topology invariants are identical to `dsgc-baseline-morphology`: same compartment count, same
branch/leaf counts, same total dendritic length to within 1e-2 µm (numerical round-trip through
six-decimal-place SWC I/O). See
`tasks/t0009_calibrate_dendritic_diameters/results/morphology_metrics.json` for full numeric outputs
and `results/per_order_radii.csv` for per-Strahler-order breakdowns.

## Usage Notes

Load the SWC with any CNG-compatible reader. The project's stdlib reader is
`tasks.t0009_calibrate_dendritic_diameters.code.swc_io.parse_swc_file`.

**Soma placeholder substitution.** The task description asks to "preserve the 19 soma compartments'
original (non-placeholder) radii." This is literally unsatisfiable because the source SWC's soma
rows also carry the uniform 0.125 µm placeholder — there are no original soma diameters to preserve.
The substitute rule, documented here explicitly, takes the seven `pt3dadd` soma diameters from the
Poleg-Polsky `RGCmodel.hoc` (0.879, 6.141, 7.736, 8.320, 8.355, 10.623, 0.879 µm), rejects the two
0.879 µm endpoints as reconstruction-endpoint artefacts, averages the five central values, and
assigns the resulting radius (4.118 µm) to all 19 soma rows. The floor
`SOMA_RADIUS_FLOOR_UM = 0.5 µm` did not trigger for any soma row.

**Strahler tie-break.** The Horton-Strahler order is computed with a **maximum-child tie-break**:
when two or more children share the maximum order `k`, the parent's order is `k+1`. This matches the
convention used by NeuroM's `section_strahler_orders` so the calibration is reproducible against the
community-standard implementation.

**Terminal radius clamp.** Dendritic compartments assigned a raw radius below
`TERMINAL_RADIUS_FLOOR_UM = 0.15 µm` are clamped to the floor. In this calibration no terminals
required clamping — the Poleg-Polsky terminal mean (0.439 µm) sits above the floor — and the
`n_clamped_dendrites` metric is therefore 0.

**Input-resistance proxy.** The `results/morphology_metrics.json` entries
`proximal_input_resistance_calibrated_ohm` and `distal_input_resistance_calibrated_ohm` are
cumulative axial-resistance proxies, not true input resistances (no membrane term). They are useful
for cross-task regression against the placeholder baseline but should not be compared directly to
Schachter et al. 2010's 150-200 MΩ (proximal) and >1 GΩ (distal) numbers, which are steady-state Rin
including membrane conductances. A follow-up task fitting passive properties with NEURON will
produce the Rin gradient needed for that comparison.

**Recommended downstream use.** Downstream compartmental-modelling tasks should load this asset
rather than the raw `dsgc-baseline-morphology`. The placeholder SWC remains available for
topology-only analyses where diameters do not matter.

## Main Ideas

* The calibrated SWC is the morphology every downstream biophysical-simulation task should consume.
  The raw `dsgc-baseline-morphology` carries a uniform 0.125 µm placeholder and is unusable as a
  cable-theory input without calibration.
* The calibration is literature-grounded but simplifies the per-compartment diameter to a three-bin
  soma/primary/terminal partition — the same simplification Poleg-Polsky & Diamond 2016, Hanson et
  al. 2019, and Jain et al. 2020 use. A per-branch or per-path-distance taper would require a
  per-cell diameter source that is not published for this neuron.
* Surface area increases ~8× and total dendritic axial resistance drops to ~5% of the placeholder
  baseline. Downstream experiments comparing to the placeholder must rescale or refit all
  electrotonic results.

## Summary

`dsgc-baseline-morphology-calibrated` is a literature-grounded diameter calibration of the t0005
mouse ON-OFF DSGC SWC. It preserves the full 6,736-compartment topology of the CNG source while
replacing the uniform 0.125 µm placeholder radius with a per-Strahler-order taper harvested from the
Poleg-Polsky & Diamond 2016 NEURON model. The resulting morphology has four distinct radii — soma
4.118 µm, primary dendrite 3.694 µm, mid dendrite 1.653 µm, terminal dendrite 0.439 µm — clamped to
a 0.15 µm dendritic floor and a 0.5 µm soma floor.

For this project the calibrated asset is the required input for every biophysical-simulation task
that uses DSGC geometry: passive-property fits, spike-initiation studies, SAC-RGC
synaptic-integration tests, and the direction-selectivity experiments downstream of t0008. The main
limitation is that the three-bin partition smooths over real per-branch diameter variability — the
Poleg-Polsky source itself defines ~350 `dend[i]` sections with distinct `pt3dadd` points, and a
higher-fidelity calibration would require a per-cell diameter source that is not published for this
specific Feller-lab reconstruction. The per-Strahler-order plots in `results/images/` and the
metrics in `results/morphology_metrics.json` document the calibration's quantitative effects
relative to the placeholder baseline.
