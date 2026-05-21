# t0116 Methodology Notes

Schema and methodology decisions documented up-front for the downstream reporting stage to mirror.

* **Schema variance across the four source predictions files**: t0106
  (`all_evaluations_seed44.json.gz`) and t0112 (`all_evaluations_seed77.json.gz`) use gzipped JSON
  with a top-level `{"evaluations": [...]}` wrapper. t0114 (`predictions.jsonl.gz`) and t0115
  (`predictions.jsonl.gz`) use gzipped JSONL (one record per line). The loader
  (`code/load_pooled_cells.py`) branches on `path.suffixes` to pick the right decoder; both share
  the same per-record schema (`generation`, `vector_68d`, `objective_F_minimised`, `dsi_vector_sum`,
  `pd_rate_hz`), with t0114 and t0115 additionally carrying `joint_pass` and `legit` booleans that
  this task ignores.
* **`generation == 1` is the random init in all four files**: gen 1 contains exactly 96 records per
  seed (= pop slot count). There is no `generation == 0` row. The task description's "gen-0 overlay"
  therefore corresponds to `generation == 1` records. The gen-0 loader (`code/load_pooled_gen0.py`)
  hard-asserts the 96-row count per seed.
* **`joint_pass` / `legit` booleans are ignored** in favour of the canonical fields
  `dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` applied on the raw float values. This guarantees a
  single filter convention across all four sources.
* **Union-pool standardiser, fitted once, never per seed** (`code/fit_standardiser.py`,
  `data/pooled_standardiser.npz`). Per-seed z-scoring would absorb cross-seed scale differences into
  the standardiser and erase the very signal the analysis aims to detect. Every downstream PCA /
  KMeans / FA call uses `PooledStandardiser.transform(...)` against this single fit.
* **No registered metric from `meta/metrics/` applies to this task**. The four registered metrics
  (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`) all describe per-cell DSI / tuning measurements taken during a NEURON
  simulation. t0116 runs no new simulations — DSI and PD-rate are backfilled from the frozen
  predictions assets of t0106 / t0112 / t0114 / t0115. The unsupervised summaries this task produces
  (silhouette scores, % variance explained, NMI, Euclidean displacement) do not map to any
  registered metric key. `results/metrics.json` therefore intentionally contains no registered
  metric values; this omission is deliberate, not accidental.
