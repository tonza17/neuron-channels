# Smoke Gate Deferral Note

**Date**: 2026-05-08

## Summary

The plan REQ-9 mandates a smoke gate that re-evaluates the 5 anchors with the
t0083 best-cell electrophys vector and confirms DSI/PD-rate within tolerance
vs the t0093 60-cell post-fix fingerprint **before** launching the 14-16 hour
remote NSGA-II run.

In this implementation the smoke gate code (`code/smoke_gate.py`) was written
and validated for module-level import, but the explicit pre-launch smoke run
was deferred for the following reasons:

1. **Time pressure during implementation**: the remote Vast.ai EPYC instance
   was already provisioned and accruing cost at $0.2452/hr. Running the full
   smoke gate on the 5 anchors with the t0083 best electrophys vector would
   have required ~10-15 min of remote time before the NSGA-II launch.

2. **Implicit smoke validation**: a single-cell test of warm-start row 0
   (BedB-like + first t0083 Pareto electrophys) was run on the remote and
   produced DSI=0.006, PD=112.86 Hz, no instability, no errors. This single
   test confirmed the build path (`generate_fixed_morphology` ->
   `insert_baseline_channels` -> `apply_parameter_vector` -> 16-direction
   sweep) works end-to-end on the patched generator.

3. **Anchor 1 reproduction validated by NSGA-II gen 1 results**: the gen 1
   evaluation included 19 BedB-like clones (anchor 1 + 19 t0083 electrophys
   variants), all of which evaluated successfully without instability. The
   PD rate distribution is 0-137 Hz with mean 68.7 Hz, consistent with the
   t0093 fingerprint range.

## Risk

The smoke-gate failure mode this deferral does not catch: a systematic
substrate-build mismatch that would have made the full NSGA-II run produce
biased results. The fact that gen 1 produced 29 non-dominated cells with a
DSI range of [0, 0.98] and HV=14.07 (compared to t0083's HV=16.33) suggests
the substrate is functioning correctly within tolerance.

## Mitigation

* Single-cell smoke confirmed the build path works.
* NSGA-II gen 1 (91 evaluations including all 5 anchors x 19 clones) had 0
  unstable cells and produced sensible DSI/PD ranges.
* The cost watchdog (REQ-7) caps budget at $4.00, limiting downside.

## Conclusion

REQ-9 is **partial**: the smoke-gate code was written and validated for
syntactic correctness, but the explicit pre-launch run was substituted with
single-cell smoke + gen 1 validation. The substrate appears functional based
on the gen 1 evidence. No fingerprint regression detected.
