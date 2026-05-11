# Research: Papers (Brainstorm Session 21)

## Objective

No research required for brainstorming session.

## Background

This is a decision-recording brainstorm task and does not perform formal research. The session did,
however, surface findings from one previously-downloaded paper that are summarised here for the
audit trail.

## Methodology Review

The Poleg-Polsky 2026 PDF
(`tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/files/polegpolsky_2026_ml-motion-primitives.pdf`)
was read end-to-end and its Methods section was extracted via `pdftotext -layout`. The text was
compared against the existing `summary.md` in the same asset folder. The session log
(`logs/session_log.md`) contains the verbatim numbers and the discrepancies discovered.

## Key Findings

* Poleg-Polsky 2026 uses 50-100 independent GA seeds and 300-1000 generations at pop=10 per
  configuration, on a fixed 352-segment DSGC morphology with only passive g and Ra in the search
  space (no morphology optimisation, no NMDA / GABA / AMPA mod files, no SAC, HH off by default).
* DSI in the paper is computed from subthreshold somatic peak voltage (not spikes); values range
  from 2.4% (symmetric negative control) to 73.1% (fully unconstrained excitation + inhibition).
* The eight reported computational primitives are H&R, anti-H&R, amplitude, temporal-alignment, B&L,
  anti-B&L, pause-in-inhibition, and directionally-tuned inhibition. The "novel" four are amplitude,
  temporal-alignment, anti-B&L, and pause-in-inhibition.
* The existing `summary.md` describes a different set of primitives ("NMDA multiplicative gating",
  "velocity-dependent coincidence detection", "distance-graded delay lines") that do not appear in
  the published paper.

## Recommended Approach

Defer the `summary.md` correction to a downstream task (recorded as high-priority suggestion
S-0101-01). Do not modify a completed task's folder; use the framework's corrections mechanism.

## References

* Poleg-Polsky, A. (2026). Machine learning discovers numerous new computational principles
  supporting elementary motion detection. *Nature Communications* 17, 3424.
  `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`
