# Results Summary: Hunt DSGC Compartmental Models Missed by Prior Survey

## Summary

Executed a three-pass literature + public-code hunt for DSGC compartmental models missed by t0002
and t0008. Registered the two new qualifying papers (deRosenroll 2026 Cell Reports, Poleg-Polsky
2026 Nat Commun) and attempted three HIGH-priority ports (Hanson 2019, deRosenroll 2026,
Poleg-Polsky 2026). All three ports exited at P2 (upstream demo) within the 90-minute wall-clock
budget due to structural driver incompatibility with the canonical 12-angle x 20-trial sweep, not
biophysics bugs. Produced one answer asset summarising every candidate and outcome.

## Metrics

* **Candidates found**: **14** (3 HIGH-priority, 2 MEDIUM, 1 LOW, 8 DROP) across 37 queries
* **New papers registered**: **2** (one `download_status=success`, one `download_status=failed` due
  to Elsevier HTTP 403 on anonymous access)
* **Port attempts**: **3/3 HIGH-priority** completed and logged; **0/3 reached P3** (canonical
  sweep); all three marked `p2_failed` with explicit structural-block reasons
* **Library assets produced**: **0** (plan explicitly permits this outcome; no broken scaffolds were
  left behind)
* **Answer assets produced**: **1** (`dsgc-missed-models-survey`, confidence=medium, 2,753-word full
  answer, 219-word short answer, 3 paper evidence IDs)
* **Total spend**: **$0.00** (local-only, no remote machines)

## Verification

* `verify_task_folder.py` — **PASSED** (0 errors, 0 warnings)
* `verify_research_papers.py` — PASSED (0 errors, 1 informational RP-W002 warning inherited from
  historical no-doi slug in Hausser-Mel-2003)
* `verify_research_internet.py` — PASSED (0 errors, 0 warnings)
* `verify_research_code.py` — PASSED (0 errors, 0 warnings)
* `verify_plan.py` — PASSED (0 errors, 0 warnings)
