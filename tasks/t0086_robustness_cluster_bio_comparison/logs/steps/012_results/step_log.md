---
spec_version: "3"
task_id: "t0086_robustness_cluster_bio_comparison"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-06T18:13:39Z"
completed_at: "2026-05-06T18:18:00Z"
---
# Step 12 -- Results

## Summary

Wrote `results/results_summary.md` and `results/results_detailed.md` (both spec_version=2),
synthesising Phase A robustness classification (6/7/7), Phase B clustering (best_k=2, all three
methods agree, bootstrap ARI 0.597), and Phase C biological scorecard (both clusters exotic on NMDA
\+ NaP). The `results_detailed.md` includes a per-cell robustness table with all 20 cells, a Cluster
Analysis Results section with per-method labels and ARIs, two scorecard tables, the Visualizations
section linking all 5 PNGs, an Examples section with 11 concrete per-cell examples, a Limitations
section noting the small Genuine pool / NMDA-units mismatch caveat / local UMAP-PCA fallback, and a
Task Requirement Coverage table covering all 17 REQs (REQ-1 to REQ-16 plus REQ-X) with status Done /
Partial / Not done and evidence pointers. Verified results_summary.md word count > 80 and
results_detailed.md > 200 words via length checks.

## Actions Taken

1. Wrote `results/results_summary.md` with mandatory sections Summary, Metrics, Verification.
2. Wrote `results/results_detailed.md` with all mandatory sections (Summary, Methodology,
   Verification, Limitations, Files Created, Task Requirement Coverage) plus recommended sections
   (Per-Cell Robustness Table, Cluster Analysis Results, Biological Plausibility Scorecard,
   Visualizations, Examples).
3. Verified all 17 REQs in the Task Requirement Coverage section have status Done or Partial with
   evidence pointers.

## Outputs

* `results/results_summary.md` (spec_version=2; ~600 words).
* `results/results_detailed.md` (spec_version=2; ~3000 words).

## Issues

* REQ-8 marked Partial: UMAP fell back to PCA on local Phase B run because umap-learn is not
  installed in the local venv. The remote Vast.ai instance has umap-learn but Phase B was run
  locally for cost-efficiency. Documented in `## Limitations`.
