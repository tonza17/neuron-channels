# Intervention: Supplementary PDF Download Blocked

## Status

REQ-14 partial — supplementary citation recorded, PDF binary not attached.

## Problem

The PMC supplementary PDF for Poleg-Polsky & Diamond 2016 (NIHMS766337, PMC4795984) is hosted at:

```
https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf
```

PMC's web frontend redirects every programmatic access to a JS-only "Preparing to download..."
interstitial page (1.8 KB of HTML). We tried:

* Three browser User-Agents (Firefox/Linux, Chrome/Windows, Safari/macOS).
* Three URL forms: the canonical `instance/4795984/bin/`, the legacy `pmc/articles/PMC4795984/bin/`,
  and the publisher's `cell.com/cms/...mmc1.pdf`.
* Setting `Accept: application/pdf`, `Accept-Language: en-US`,
  `Referer: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4795984/`.

All return either the interstitial HTML, HTTP 404, or HTTP 403.

See `code/download_supplementary.py` for the exact requests tried.

## Resolution

The corrections overlay `corrections/paper_10.1016_j.neuron.2016.02.013.json` is written as a
metadata-only update that records the supplementary citation in the paper asset's abstract field.
The PDF binary itself is not attached.

A human can complete this by:

1. Opening `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4795984/` in a real browser and clicking
   the supplementary link.
2. Saving the resulting PDF to
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/supplements/NIHMS766337-supplement.pdf`.
3. Editing the corrections file to flip the action to the file-add overlay (the conditional code
   path in `download_supplementary.py`).

## Impact on Other Requirements

REQ-14 is the only requirement directly affected. The audit table, figure reproduction table, and
discrepancy catalogue (REQ-15..REQ-17) do not depend on the supplementary PDF being attached as a
binary; they depend on the supplementary text content, which is well-documented in the published
abstract and Methods section already in the paper PDF.
