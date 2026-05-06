---
spec_version: "3"
task_id: "t0086_robustness_cluster_bio_comparison"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-06T18:21:27Z"
completed_at: "2026-05-06T18:23:00Z"
---
# Step 14 -- Suggestions

## Summary

Wrote `results/suggestions.json` with 6 follow-up suggestions:

* **S-0086-01** (high priority, experiment): tighten NSGA-II priors on `gnmda_dend` to match
  Sivyer 2013 per-synapse value; re-run.
* **S-0086-02** (high priority, evaluation): resolve units mismatch between t0080 NetCon weight
  and Sivyer 2013 per-spine conductance via calibration ablation.
* **S-0086-03** (medium, experiment): per-cluster Vm trace deep-dive (extension of t0084 to all
  6 Genuine cells).
* **S-0086-04** (medium, experiment): 10-replication robustness extension on Genuine + Marginal
  cells.
* **S-0086-05** (low, evaluation): source RGC-specific NaP measurement to replace Stuart 1999.
* **S-0086-06** (medium, experiment): Bed A cross-bed validation with the same v3 substrate.

## Actions Taken

1. Reviewed Phase A robustness classification, Phase B clustering, and Phase C scorecard.
2. Identified the dominant follow-up directions: NMDA prior tightening (S-0086-01), NMDA units
   resolution (S-0086-02), per-cluster mechanism attribution (S-0086-03), 10-rep extension
   (S-0086-04), RGC-specific NaP prior (S-0086-05), and Bed A cross-bed (S-0086-06).
3. Wrote `results/suggestions.json` with 6 entries, each populated with id, title, description
   (>200 chars), kind (experiment / evaluation), priority, source_task, source_paper, and
   categories.

## Outputs

* `results/suggestions.json` (6 suggestions; spec_version=1).

## Issues

* No issues. The 6 suggestions cover both the headline biological findings (NMDA exotic
  verdict needs validation: S-0086-01, S-0086-02, S-0086-05) and the methodological
  follow-ups (per-cluster deep-dive: S-0086-03; finer robustness: S-0086-04; cross-bed:
  S-0086-06).
