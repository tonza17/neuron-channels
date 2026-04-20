---
spec_version: "1"
task_id: "t0016_literature_survey_dendritic_computation"
step_id: "implementation"
step_index: 9
---
# Step 9: implementation

## Purpose

Execute `plan/plan.md`: download ~25 paper assets per the six-theme
shortlist and write one answer asset synthesising dendritic motifs that
may transfer to DSGC dendrites.

## Approach

1. Create `code/check_doi_overlap.py` for REQ-5 verification.
2. For each of the 25 target DOIs, one at a time:
   * Build `details.json` and `summary.md` per paper spec v3.
   * Flag paywalled publisher PDFs as `download_status: "failed"` with a
     concrete reason and use the abstract-based Overview path.
   * Run `meta.asset_types.paper.verificator` on that one paper and
     commit on success.
3. Run `check_doi_overlap.py`; expect exit code 0.
4. Write `intervention/paywalled_papers.md` enumerating failed DOIs.
5. Write the answer asset
   `dendritic-computation-motifs-for-dsgc-direction-selectivity`.
6. Run `meta.asset_types.answer.verificator` and commit.

## Resume Notes

This log is being (re)written after a watchdog interruption of the
original implementation run. The interrupted run left 25 empty paper
folder stubs and three batch-generation scripts in `code/` that violated
the "never generate multiple paper assets in one invocation" rule. Those
artefacts were removed as part of the pre-resume cleanup; papers are now
being added one at a time with per-paper commits.
