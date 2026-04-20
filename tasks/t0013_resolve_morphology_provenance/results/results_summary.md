# Results Summary: Resolve DSGC Morphology Provenance

## Summary

Closed the provenance gap on `dsgc-baseline-morphology.source_paper_id`. Registered both candidate
Feller-lab 2018 papers as v3 paper assets, read their Methods sections, applied the pre-specified
decision procedure, and filed a single correction that sets `source_paper_id` to
`10.1016_j.cub.2018.03.001` (Morrie & Feller 2018 *Current Biology*, "A Dense Starburst Plexus Is
Critical for Generating Direction Selectivity"). Discovered along the way that the t0005 plan's
"Morrie & Feller 2018 *Neuron*" DOI nomination was an error: `10.1016/j.neuron.2018.05.028` resolves
to Li, Vaughan, Sturgill & Kepecs (2018), an unrelated CSHL viral-tracing paper.

## Metrics

* **Paper assets registered**: **2** (expected: 2)
* **Correction assets produced**: **1** (`C-0013-01`)
* **Winning source paper**: `10.1016_j.cub.2018.03.001` (Morrie & Feller 2018, *Current Biology*)
* **Decision branch taken**: criterion 1 ("exactly one paper's Methods cites the reconstruction")
* **PDFs successfully downloaded**: **1/2** (CB open-access on eScholarship; Neuron DOI paywalled
  and metadata-only per v3 spec)
* **Verificator pass rate**: **3/3** (`verify_paper_asset` × 2 + `verify_correction_asset`)

## Verification

* `verify_paper_asset 10.1016_j.neuron.2018.05.028` — **PASSED** (0 errors, 0 warnings)
* `verify_paper_asset 10.1016_j.cub.2018.03.001` — **PASSED** (0 errors, 0 warnings)
* `verify_correction_asset dataset_dsgc-baseline-morphology` — **PASSED** (0 errors, 0 warnings)
* Asset-count check: `assets/paper/` contains exactly the two expected folders.
* Correction-count check: `corrections/` contains exactly `dataset_dsgc-baseline-morphology.json`.
