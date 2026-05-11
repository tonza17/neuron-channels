# t0103 Results Summary

## Summary

Extracted **1,238 per-cell records** from Baden et al. 2016 across the eight paper-authoritative
direction-selective groups `{2, 6, 12, 13, 16, 25, 26, 29}` into a 4.864 MiB Parquet dataset asset,
and registered the Baden 2016 paper itself as a paper asset. Both assets pass their verificators
with zero errors and zero warnings.

## Metrics

* **1,238** per-cell records extracted across **8 DS groups**: G2:162, G6:104, G12:397, G13:129,
  G16:99, G25:76, G26:141, G29:130.
* **40 columns per cell**: 35 scalar features (cluster, selectivity, quality, RF, soma, immuno,
  genetics, cell-of-origin) + 5 nested `list<float32>` trace columns (chirp 249 samples, moving-bar
  32, moving-bar direction-major 256, colour 96, RF kernel 80).
* **Cross-check delta vs source `.mat` `group_idx`**: **0.00% for all 8 groups**. G2 also matches
  the paper's explicit Extended-Data-Fig.-4 cell count of n=162 exactly.
* **No registered project metrics** apply to this extraction task; `metrics.json` is `{}`.

## Verification

* `meta.asset_types.paper.verificator --task-id t0103_extract_baden_2016_ds_morphologies` →
  **PASSED** (0 errors, 0 warnings).
* `meta.asset_types.dataset.verificator --task-id t0103_extract_baden_2016_ds_morphologies` →
  **PASSED** (0 errors, 0 warnings).
* `ruff check`, `ruff format`, `mypy -p tasks.t0103_extract_baden_2016_ds_morphologies.code` → all
  green.
* `verify_plan` → PASSED (0 errors, 0 warnings).
