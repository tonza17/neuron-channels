---
spec_version: "3"
task_id: "t0090_morphology_generator_diversity_test"
step_number: 9
step_name: "results"
status: "completed"
started_at: "2026-05-07T18:05:34Z"
completed_at: "2026-05-07T18:25:00Z"
---
# Step 9 -- Results

## Summary

Wrote `results_summary.md`, `results_detailed.md`, `costs.json`, `remote_machines_used.json`, and
trimmed `metrics.json` to the explicit-variant format containing only the registered metric
`direction_selectivity_index`. The detailed results document includes the mandatory `## Examples`
section (11 examples covering STABLE cells, NAN_VOLTAGE failures, edge-case parameter combinations,
and the G.1 / G.2 phase outputs) because the task type `data-analysis` is in the experiment-task
set. Both `verify_task_metrics.py` and `verify_task_results.py` PASS. The 13/16 done
+ 3/16 partial outcome from the implementation step is fully reflected in the
  `## Task Requirement Coverage` final section.

## Actions Taken

1. Ran prestep for `results`, creating `logs/steps/009_results/`.
2. Inspected `data/verification_summary.json`, `data/morphometric_summary.json`,
   `data/g1_nav_ratio_audit.json`, `data/g2_nmda_calibration.json`,
   `data/bedb_reproducibility.json`, `data/g3_nap_knockout.json` to gather quantitative material.
3. Trimmed `metrics.json` to the registered metric `direction_selectivity_index` only across 3
   variants (`different_set`, `similar_set`, `bedb_repro_5`); removed unregistered keys
   (`n_stable_morphologies`, `n_total_morphologies`, etc.) per spec rule. Also dropped the non-spec
   `task_id` and `format` top-level fields that triggered TM-E003.
4. Wrote `results_summary.md` (Summary, Metrics, Verification — at least 5 metrics with specific
   numbers, 80+ words).
5. Wrote `results_detailed.md` (Summary, Methodology, Metrics Tables, Visualizations, Analysis,
   Verification, Examples [11 entries], Limitations, Files Created, Task Requirement Coverage). All
   5 PNG charts from `results/images/` embedded with markdown image syntax + 1-3 sentence
   descriptions. The Task Requirement Coverage section maps every REQ-1..REQ-16 from the plan to a
   Done / Partial status with evidence path.
6. Wrote `costs.json` (`total_cost_usd: 0.0`, `breakdown: {}`, note explaining local-CPU-only
   execution and deferred Phase F / G.3 sweeps).
7. Wrote `remote_machines_used.json` (`[]`).
8. Ran `uv run flowmark --inplace --nobackup` on the two markdown files.
9. Ran `verify_task_metrics.py` -- initial run failed with TM-E003 ("Explicit variant format only
   allows the top-level 'variants' field"). Removed `task_id` and `format` top-level fields; re-ran
   -- PASSED.
10. Ran `verify_task_results.py` -- PASSED with 0 errors and 0 warnings.

## Outputs

* `tasks/t0090_morphology_generator_diversity_test/results/results_summary.md`
* `tasks/t0090_morphology_generator_diversity_test/results/results_detailed.md`
* `tasks/t0090_morphology_generator_diversity_test/results/metrics.json`
* `tasks/t0090_morphology_generator_diversity_test/results/costs.json`
* `tasks/t0090_morphology_generator_diversity_test/results/remote_machines_used.json`

## Issues

No issues encountered. The Examples section is exhaustive (11 entries vs the spec minimum of 10);
the Task Requirement Coverage section quotes the operative task text and provides a Done/Partial
status with evidence path for every REQ.
