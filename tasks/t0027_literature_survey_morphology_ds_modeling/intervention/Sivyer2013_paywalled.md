---
task_id: "t0027_literature_survey_morphology_ds_modeling"
paper_id: "10.1038_nn.3565"
status: "open"
date_opened: "2026-04-21"
---

# Intervention: Sivyer & Williams (2013) PDF Paywalled

## Summary

The paper asset at `assets/paper/10.1038_nn.3565/` was created with
`download_status: "failed"` because the full-text PDF is not available
through any automated open-access route. Metadata and the verbatim
abstract were obtained from CrossRef and PubMed. The summary document
is built from the abstract and the public record (MeSH terms, PubMed
reference list, citing literature) rather than the full text.

## Automated Attempts

* Direct fetch of `https://www.nature.com/articles/nn.3565.pdf`
  returned the Nature HTML paywall landing page (HTTP 200 but
  `Content-Type: text/html`).
* Unpaywall API (`https://api.unpaywall.org/v2/10.1038/nn.3565`)
  reports `is_oa: false`, `oa_status: "closed"`,
  `has_repository_copy: false`. No OA locations.
* Semantic Scholar Graph API reports
  `openAccessPdf.status: "CLOSED"` and the abstract field is elided
  by the publisher.
* PubMed Central: no PMC ID associated with PMID 24162650.

## Action Requested

A human with institutional access (e.g., Sheffield VPN to Nature) or
direct contact with the Williams lab at the Queensland Brain Institute
should:

1. Download the full PDF from
   `https://www.nature.com/articles/nn.3565`.
2. Save it as
   `assets/paper/10.1038_nn.3565/files/sivyer_2013_active-dendritic-integration-ds.pdf`.
3. Delete `.gitkeep` and update `details.json` by setting
   `download_status: "success"`, `download_failure_reason: null`, and
   `files: ["files/sivyer_2013_active-dendritic-integration-ds.pdf"]`.
4. Re-read the full paper and expand the quantitative bullets in
   `summary.md` (Results, Architecture sections) with specific figures
   from the paper (exact DSI values, gNa/gCa densities from the
   compartmental model, branch-independence measurements).

This intervention is non-blocking for the literature survey: the
abstract-based summary is sufficient for cross-referencing and
categorisation within task t0027.
