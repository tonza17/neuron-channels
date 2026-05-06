---
spec_version: "3"
task_id: "t0088_recluster_marginals_and_vm_motifs"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-05-06T20:59:26Z"
completed_at: "2026-05-06T21:05:00Z"
---
# Step 13 -- Compare Literature

## Summary

Wrote `results/compare_literature.md` extending t0086's biological scorecard from k = 2 (6 Genuine
cells) to k = 4 (13-cell pool of 6 Genuine + 7 Marginal cells) and incorporating the per-cluster
Vm-trace deep-dive mechanism attribution from t0088 Phase B. All 4 clusters classified exotic by the
worst-case rule; the most novel cross-cluster finding is Cluster 1's AIS-to-soma Nav ratio = 116x
(+33 sigma vs Werginz 2024). Verdict from t0084 (cell 767 NaP-dominant) generalises to all 4
representative cells with consistent NaP fractions (0.874-0.997).

## Actions Taken

1. Read t0086's `compare_literature.md` for the canonical comparison-table format and section
   structure.
2. Wrote `compare_literature.md` with all 6 mandatory sections (Summary, Comparison Table,
   Methodology Differences, Comparison to t0084 Vm-trace Mechanism Attribution, Analysis,
   Limitations) plus Recommendations and References.
3. Built the 4-cluster comparison table with rows for the 9 published priors and columns for each
   cluster's centroid value, deviation in sigma, and verdict.
4. Compared mechanism attribution at 16 directions (this task) to t0084's 8-direction cell 767
   attribution; documented consistency within angular-resolution noise.
5. Ran `flowmark` on the file. Initial run failed `verify_compare_literature` with CL-E003 missing
   sections (the spec requires exactly Summary, Comparison Table, Methodology Differences, Analysis,
   Limitations -- I had used "Discrepancies" and "Recommendations" without the required Methodology
   Differences and Limitations); fixed by renaming "Comparison to Published Biological Priors" ->
   "Comparison Table", adding Methodology Differences section, adding Analysis section, adding
   Limitations section, and re-running flowmark.
6. Verified `verify_compare_literature` passes with 0 errors (1 warning CL-W003 about citation keys
   -- the references are present in narrative form rather than canonical citation-key form; accepted
   as a stylistic warning).

## Outputs

* `tasks/t0088_recluster_marginals_and_vm_motifs/results/compare_literature.md`

## Issues

The `verify_compare_literature` mandatory section list (Summary, Comparison Table, Methodology
Differences, Analysis, Limitations) is stricter than t0086's compare_literature structure (Summary,
Comparison Table, Discrepancies, Recommendations, References). t0086 may have benefited from a more
lenient verifier version; this task uses the current strict version. Documented in this step log;
resolution is to comply with the current spec.
