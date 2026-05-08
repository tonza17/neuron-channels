---
spec_version: "2"
answer_id: "t0090-procedural-cell-silence-root-cause"
answered_by_task: "t0092_diagnose_morphology_generator_silence"
date_answered: "2026-05-08"
---
# t0090 procedural cell silence root cause

## Question

Why do t0090's procedural cells produce zero spikes under the t0083 best-cell channel set, and what
is the fix?

## Answer

The t0090 generator emits the soma's two pt3d points at coincident `(x, y, 0)` coordinates, so
NEURON computes the cumulative pt3d length as zero, overrides the prior `sec.L = soma_diameter_um`
assignment, and the soma's surface area collapses to ~9.4e-14 µm² — essentially a point.
Synaptic input then drives the somatic Vm to NaN within a few simulation steps, so every procedural
cell in t0090's 60-cell sweep returns `non_finite_voltage` (51 cells) or zero spikes (the 9 STABLE
cells that happened to clear the no-stim stability check). The fix is the
`procedural_dsgc_morphology_generator_fix` library: a thin wrapper that re-emits the soma's pt3d
points along the z-axis so the cylinder length equals `soma_diameter_um` and the surface area
matches the t0024 hand-coded reference (~220 µm²). After applying the fix the BedB-equivalent
procedural cell fires 61 spikes in the PD direction (43.6 Hz, peak Vm ~11 mV).

## Sources

* Task: `t0024_port_de_rosenroll_2026_dsgc`
* Task: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* Task: `t0083_bedb_v3_extend_nsga2_gen8plus`
* Task: `t0090_morphology_generator_diversity_test`
