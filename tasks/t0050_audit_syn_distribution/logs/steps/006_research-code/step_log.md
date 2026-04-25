---
spec_version: "3"
task_id: "t0050_audit_syn_distribution"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-25T11:19:58Z"
completed_at: "2026-04-25T11:31:00Z"
---
## Summary

Reviewed `placeBIP()` and `simplerun()` semantics in detail and uncovered a critical structural
finding: the deposited code's PD vs ND condition swap is implemented as a pure scalar
`gabaMOD = 0.33 + 0.66*direction` applied uniformly to ALL SAC inhibitory synapses, with NO spatial
threshold. Synapses do have spatial positions (`locx`, `locy`) stored at construction in
`RGCmodel.hoc:11839-11857` (locx = midpoint of the section's first two `x3d` points), and the wave
stimulus uses `locx` relative to `lightXstart=-100, lightXend=200` for stimulus timing — but the
PD/ND distinction itself is non-spatial. This pre-determines the t0050 spatial-distribution
hypothesis verdict as SUPPORTED at the structural level: the deposited GABA distribution cannot
produce a somatic PD/ND asymmetry under SEClamp because the deposited code does not encode any
spatial PD/ND distinction in the GABA placement. The audit will still extract coordinates to
quantify the (non-)asymmetry numerically.

## Actions Taken

1. Read `main.hoc:191-282` (`placeBIP()`) and `dsgc_model_exact.hoc:175-260` to identify the
   wave-stimulus + condition-swap semantics.
2. Read `RGCmodel.hoc:11839-11857` to identify how synapse `locx`/`locy` are computed (midpoint of
   first two `x3d` points; no z, no section, no path distance).
3. Read `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/build_cell.py` to identify the
   `read_synapse_coords()` helper API and the gap (only locx/locy returned, not full 3D or path
   distance).
4. Identified the recommended midline for our spatial audit: `x_soma` (the soma center
   x-coordinate). This gives an arbitrary but consistent PD-side vs ND-side classification for the
   spatial-distribution measurement, while explicitly flagging that the deposited code does NOT use
   this classification internally.
5. Wrote `research/research_code.md` covering all 8 questions; verified `verify_research_code.py`
   PASSED with 0 errors and 0 warnings.

## Outputs

* tasks/t0050_audit_syn_distribution/research/research_code.md

## Issues

The structural finding (no spatial PD/ND threshold in deposited code) means the H1 verdict is
essentially predetermined as SUPPORTED at the protocol level. The implementation step should still
extract synapse coordinates to:

* Confirm the spatial distribution numerically (count_pd ≈ count_nd at our chosen midline, per
  channel).
* Render the histograms to make the symmetry visible.
* Distinguish "deposited code has no spatial PD/ND distinction in protocol" (a structural fact) from
  "deposited code's spatial distribution is symmetric across the soma midline" (a measurable
  property that may or may not be true at every synapse class).
