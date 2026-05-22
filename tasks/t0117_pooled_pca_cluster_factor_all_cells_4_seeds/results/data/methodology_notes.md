# Methodology notes — t0117 pooled PCA + cluster + factor analysis (no filter)

* **Source schema variance**: t0106 (seed 44) and t0112 (seed 77) ship predictions as gzipped JSON
  with the structure `{"evaluations": [...]}`. t0114 (seed 7755) and t0115 (seed 9354) ship
  predictions as gzipped JSONL (one record per line). The loader (`code/load_pooled_cells.py`)
  branches on `path.suffixes` to choose the right decoder for each file.

* **Generation indexing**: All four files are 1-indexed for `generation`; `generation == 1` contains
  exactly 96 records (one per pop slot) and is the random-init pool. The `code/load_pooled_gen0.py`
  loader filters on this index. There is no `generation == 0` row.

* **No cohort filter applied (deliberate divergence from t0116)**: The only methodological change vs
  t0116 is the **removal** of the `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` cohort filter from
  `code/load_pooled_cells.py`. Every record from every source is admitted. The `joint_pass` /
  `legit` booleans on t0114 / t0115 records are deliberately ignored in t0116 and remain ignored
  here. Per-seed counts are recorded as `n_raw` (every record) and `n_unique` (post-dedup); the
  t0116-style `n_passing_filter` column is omitted because no filter exists.

* **Dedup convention**: deduplication uses the 68-d vector rounded to `DEDUP_DECIMALS = 6` decimals
  (same convention as t0116 / t0108). NSGA-II's converged offspring legitimately collapse many
  duplicate rows into one — t0106 alone produces n_raw=3744 -> n_unique=1065 (28%). This is
  expected, not a bug; the same convention applied to t0116 produced 658 passing-filter rows -> 121
  unique rows (18%).

* **Union-pool standardiser**: The 68-d z-score standardiser is fitted ONCE on the full unfiltered
  union pool (n=4431) and serialised to `data/pooled_standardiser.npz`. Every downstream PCA,
  KMeans, FA, and gen-0 projection reuses this exact fit. Per-seed re-fitting would absorb
  cross-seed scale differences into the standardiser and erase the very signal the analysis is
  designed to detect.

* **No registered metric applies**: this task performs no new simulations. `dsi_vector_sum` and
  `pd_rate_hz` are backfilled from frozen predictions assets produced by the source NSGA-II tasks
  (t0106 / t0112 / t0114 / t0115). The registered metrics in `meta/metrics/` describe per-cell DSI /
  tuning measurements taken during a simulation; none correspond to the unsupervised summaries this
  task produces (silhouette score, % variance explained, NMI, Euclidean displacement). The
  implementation therefore does not write any registered metric keys into `results/metrics.json`.

* **Head-to-head comparison vs t0116**: the comparison CSV `results/data/t0116_comparison.csv` reads
  t0116's published numbers directly from its own `results/data/` directory (per-seed cohort counts,
  cluster-seed purity, factor correlations, gen-0 displacements) and produces a row per quantity
  with `t0116_value`, `t0117_value`, `delta`. No t0116 number is recomputed from raw NSGA-II outputs
  here — the comparison is wholly data-driven from the published t0116 result CSVs, so the
  comparison can be reproduced deterministically by re-running this module.
