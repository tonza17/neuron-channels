# ⏹ Tasks: Not Started

1 tasks. ⏹ **1 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
