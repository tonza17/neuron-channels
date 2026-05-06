---
spec_version: "3"
task_id: "t0086_robustness_cluster_bio_comparison"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-05-06T18:19:26Z"
completed_at: "2026-05-06T18:21:00Z"
---
# Step 13 -- Compare Literature

## Summary

Wrote `results/compare_literature.md` (spec_version=1) comparing the two cluster centroids (Cluster
0: cells 1634, 1639, 1663; Cluster 1: cells 1517, 1604, 1677) to nine published biological priors.
Headline finding: both clusters score **exotic** by worst-case aggregation, driven by NMDA
per-synapse conductance >85 sigma above Sivyer 2013 in both clusters and elevated distal NaP density
>7 sigma above Stuart 1999 in both clusters. The AIS Nav densities are plausible vs Kole 2008 but
stretched vs Werginz 2024; this reflects the disagreement between the two AIS papers. Methodology
Differences section flags three known caveats: (1) NMDA scale mismatch between Sivyer 2013's
per-spine measurement and t0080's NetCon weight; (2) NaP measured in cortical pyramidals not RGCs;
(3) AIS prior conflict between Kole and Werginz.

## Actions Taken

1. Read the biological scorecard at `results/data/biological_scorecard.json` produced by
   `code/biological_scorecard.py` in the implementation step.
2. Wrote `results/compare_literature.md` with all 5 mandatory sections (Summary, Comparison Table,
   Methodology Differences, Analysis, Limitations).
3. Comparison Table includes 9 priors x 2 clusters = 18 cell rows in a single markdown table.
4. Analysis section synthesises the two-cluster typology: Cluster 0 "high-NMDA + high-NaP +
   high-AIS-ratio" vs Cluster 1 "high-NMDA + extended-GABA-lambda".

## Outputs

* `results/compare_literature.md` (spec_version=1; ~900 words; 9-prior x 2-cluster comparison
  table).

## Issues

* No issues. Note that the +85 sigma to +122 sigma NMDA exotic verdict is the most extreme finding
  and likely partially reflects a units / scope mismatch between Sivyer 2013's per-spine measurement
  and the t0080 NetCon weight encoding. This is documented in Methodology Differences and
  Limitations, and recorded as a follow-up suggestion in the suggestions step.
