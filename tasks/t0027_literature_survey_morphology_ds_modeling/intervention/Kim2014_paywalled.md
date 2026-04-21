---
task_id: "t0027_literature_survey_morphology_ds_modeling"
paper_id: "10.1038_nature13240"
status: "open"
date_opened: "2026-04-21"
---

# Intervention: Kim et al. (2014) PDF Paywalled

## Summary

The paper asset at `assets/paper/10.1038_nature13240/` was created with
`download_status: "failed"` because the full-text PDF is not available
through any automated open-access route. Metadata and the verbatim
abstract were obtained from CrossRef and the PMC (PMC4074887) HTML
full-text landing page. The summary document is built from the
abstract, the PMC HTML body text, and figure captions rather than the
publisher PDF.

## Automated Attempts

* Direct fetch of `https://www.nature.com/articles/nature13240.pdf`
  returned the Nature HTML paywall landing page (HTTP 200 but
  `Content-Type: text/html`).
* Seung lab `publications` directory
  (`https://seunglab.org/wp-content/uploads/.../Kim-et-al-2014...pdf`)
  returned HTML (no such public mirror at guessed path).
* PMC PDF at
  `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4074887/pdf/` and
  `https://pmc.ncbi.nlm.nih.gov/articles/PMC4074887/pdf/nihms-574498.pdf`
  redirected to a JavaScript proof-of-work challenge page
  (`Preparing to download ...`) that curl cannot solve. The PDF
  (author manuscript `NIHMS574498`) exists at PMC but is gated.
* EuropePMC render endpoint
  (`https://europepmc.org/articles/PMC4074887?pdf=render`) returned
  `{"error": "Failed to retrieve PDF for pmcid: PMC4074887"}`.

## Action Requested

A human with a standard browser session should:

1. Open `https://pmc.ncbi.nlm.nih.gov/articles/PMC4074887/` and
   download `nihms-574498.pdf` via the PMC download button (browser
   JS will solve the PoW challenge automatically). Alternatively,
   download from `https://www.nature.com/articles/nature13240` via
   institutional Nature subscription.
2. Save it as
   `assets/paper/10.1038_nature13240/files/kim_2014_space-time-wiring-ds.pdf`.
3. Delete `files/.gitkeep` and update `details.json`: set
   `download_status: "success"`, `download_failure_reason: null`, and
   `files: ["files/kim_2014_space-time-wiring-ds.pdf"]`.
4. Optionally expand the summary's quantitative bullets with any
   supplementary-equations details (e.g., direction selectivity index
   as a function of stimulus speed from Extended Data Fig. 9) that
   the HTML captures only as figure references.

This intervention is non-blocking for the literature survey: the
HTML-derived summary captures all main-text numerics (195 BCs, 79
SACs, 5881 EyeWirers, 50-100 ms BC2-BC3a lag, 32% Off-SAC IPL depth,
20-80 um dendritic-tilt range) required for cross-referencing Kim2014
as the EM substrate that downstream compartmental DSGC/SAC models
(e.g., Poleg-Polsky 2026) consume as input.
