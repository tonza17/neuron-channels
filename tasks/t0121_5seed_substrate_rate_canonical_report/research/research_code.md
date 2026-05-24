---
spec_version: "1"
task_id: "t0121_5seed_substrate_rate_canonical_report"
research_stage: "code"
tasks_reviewed: 12
tasks_cited: 10
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-05-24"
status: "complete"
---
# Code Research: 5-Seed Substrate-Rate Canonical Report (t0121)

## Task Objective

t0121 is a **pure write-up** task that consolidates the S-0112-01 5-seed substrate-rate batch (t0106
seed 44, t0112 seed 77, t0113 seed 2247, t0114 seed 7755, t0115 seed 9354) into one canonical
document with harmonised metric conventions, statistics (per-seed acceptance, 5-seed mean / SD / SE,
normal-approx and bootstrap 95% CIs), and side-by-side Hay 2011 / Druckmann 2007 comparisons. No new
NSGA-II runs, no remote machines, local CPU only. Three CSVs, one pooled parquet, three charts, one
answer asset, and the standard results documents are the deliverables (see
`tasks/t0121_5seed_substrate_rate_canonical_report/task_description.md`). The code work is therefore
(a) re-loading the five source-task evaluation dumps with the dedup-and-LEGIT filter conventions
inherited from [t0115], (b) re-running per-seed acceptance arithmetic against the canonical
convention so any drift across the 5 source tasks is exposed and documented, and (c) re-using the
chart and CSV builders already battle-tested in [t0115]'s `build_results.py`.

## Library Landscape

No project library asset exists yet that covers the operations needed by t0121. The
`aggregate_libraries.py` aggregator does not exist in `arf/scripts/aggregators/` in this branch
(checked directly: only `aggregate_categories`, `aggregate_costs`, `aggregate_machines`,
`aggregate_metric_results`, `aggregate_metrics`, `aggregate_suggestions`, `aggregate_task_types`,
`aggregate_tasks` are present). A filesystem walk via `Glob` over `tasks/*/assets/library/*` shows
**only `.gitkeep` markers** under every `assets/library/` directory in the repo — no library asset
has ever been registered in this project. All cross-task code reuse is therefore by-copy, per the
project's cross-task code reuse rule (libraries are the only legitimate cross-task import path;
without any registered library, every reusable piece must be **copied into the t0121 `code/`
directory** and rewritten to import from the t0121 namespace).

Two project-internal aggregators are nevertheless relevant as discovery / verification helpers even
though they are not "libraries" in the asset sense:

* `arf/scripts/aggregators/aggregate_tasks.py` — used during this code-research stage to enumerate
  dependencies and cross-check task status.
* `arf/scripts/verificators/verify_research_code.py` — required for the final verificator gate on
  this file.

Both live under `arf/` and are project infrastructure, not task-produced library assets, so they are
off-limits to the cross-task import rule.

## Key Findings

### Result-data layout is uniform across the 5 source tasks

Every one of t0106 / t0112 / t0113 / t0114 / t0115 writes its NSGA-II output dump to
`tasks/<task_id>/results/data/` with the same naming pattern: `all_evaluations_seed<N>.json[.gz]`,
`hv_trajectory_seed<N>.json`, `pareto_front_seed<N>.json`, `init_pop_seed<N>.json`, and
`nsga2_checkpoint_seed<N>.json[.gz]` (see `ls tasks/t0106_*/results/data/` ...
`ls tasks/t0115_*/results/data/`). The `all_evaluations` payload is either gzipped JSON (`t0106`,
`t0112`, `t0113`) or plain JSON (`t0114`, `t0115`), branching cleanly on the `.gz` suffix [t0106]
[t0112] [t0113] [t0114] [t0115]. The top-level object is `{"evaluations": [...]}` for some tasks and
a bare list for others; the list shape is the same in both cases — `_load_evaluations` in
`tasks/t0115_seed9354_no_autostop/code/build_results.py:222-233` handles both shapes with a single
`isinstance(data, dict)` check. The `hv_trajectory` payload is uniformly
`{"trajectory": [{"generation": int, "hypervolume": float, "cumulative_cost_usd": float, "elapsed_s": float, "n_evaluations": int}, ...]}`
(`_load_hv` at `tasks/t0115_seed9354_no_autostop/code/build_results.py:236-240`). The strict-Pareto
`pareto_front_seed<N>.json` is `{"seed": int, "n_total": int, "cells": [...]}` where each cell has
`cell_id`, `vector_68d`, `objective_F_minimised`, `dsi_vector_sum`, `pd_rate_hz`, `generation`
(verified by `head` on `pareto_front_seed9354.json`). t0121 can therefore reuse a single loader
module for all five seeds — no per-seed parsing branches needed.

### t0106 stores its raw evaluations as a predictions asset, not as a raw `results/data/` file

Subtle but load-bearing: t0106's `results/data/` directory contains `all_evaluations_seed44.json.gz`
(verified by `ls`), but [t0115]'s `build_results.py` actually loads t0106's evaluations from
`tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`
(see `T0106_EVALS` at `tasks/t0115_seed9354_no_autostop/code/build_results.py:54-61`). t0113
likewise — t0115's loader reads
`tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz`
(line 69-76). Both predictions assets and `results/data/` copies exist; the predictions asset is the
canonical post-build source because it is the asset that downstream tasks register against. t0121
must replicate this path-resolution convention or the file paths will silently drift.

### Per-task reporting conventions disagree about `joint_pass_pct`

The single most important finding for t0121's "harmonise conventions" step: the `joint_pass_pct`
column in `joint_pass_summary_<N>seeds.csv` is computed with a **different numerator across the
source tasks**. [t0113]'s `joint_pass_summary_3seeds.csv` and [t0114]'s
`joint_pass_summary_4seeds.csv` both report
`joint_pass_pct = n_joint_pass_unique / n_total_evals * 100` (i.e., **includes silence-guard ceiling
cells**). [t0115]'s `joint_pass_summary_5seeds.csv` and `substrate_rate_5seed.csv` instead report
`acceptance_rate_pct = n_joint_pass_legit_unique / n_total_evals * 100` (i.e., **excludes
silence-guard ceiling cells**, the LEGIT convention). Concrete drift in the published numbers:

* t0106 seed 44: t0114 reports `3.6325%` (136 / 3744), t0115 reports `3.2318%` (121 / 3744)
* t0113 seed 2247: t0114 reports `0.1488%` (2 / 1344), t0115 reports `0.0000%` (0 / 1344)
* t0114 seed 7755: t0114 reports `12.9536%` (771 / 5952), t0115 reports `8.1317%` (484 / 5952)

The **t0115 LEGIT-only convention is the canonical one** per the project memory notes (the LEGIT
filter `DSI < 0.9999` excludes silence-guard / single-spike evaluator artefacts), and is the
convention that the t0121 task description requires. t0121 must explicitly call out this drift in
the canonical report and use the LEGIT convention for every published number.

A second smaller convention difference: t0106's `joint_pass_summary_3seeds.csv` reports
`best_pd_rate_hz = 122.62` for seed 44, whereas [t0114] / [t0115] both report `125.95`. Same seed,
same data; the difference is rounding precision (t0106's CSV truncated to 5 sig figs; t0115 rounds
to 4 decimals). Trivial, but worth flagging.

### Per-seed acceptance rate inputs are the canonical 5 numbers

Per [t0115]'s `substrate_rate_5seed.csv`: seed 44 = 121 / 3744 = 3.2318%, seed 77 = 7 / 2016 =
0.3472%, seed 2247 = 0 / 1344 = 0.0000%, seed 7755 = 484 / 5952 = 8.1317%, seed 9354 = 63 / 5280 =
1.1932%. 5-seed mean = 2.5808%, sample SD = 3.3471%, sample SE = 1.4969%. 95% CI (normal approx) =
(-0.36%, +5.52%). These five values match the t0121 task description's headline numbers exactly. The
plan adds a bootstrap CI (B=10000) on top, which is a t0121-new computation ([t0115] only reports
the normal-approx CI).

### LEGIT / joint-pass thresholds are uniform across the lineage

The acceptance definition is **DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999** in every source
task (see `DSI_THRESHOLD = 0.5`, `PD_RATE_THRESHOLD_HZ = 30.0`, `LEGIT_DSI_CEILING = 0.9999` at
`tasks/t0115_seed9354_no_autostop/code/build_results.py:98-101`). The `_is_legit_joint_pass`
predicate (line 261-266) encapsulates this. [t0114]'s and earlier results files prove the threshold
has not drifted across the lineage. t0121 should copy this predicate verbatim.

### HV-plateau auto-stop convention drifts mid-batch (S-0113-03)

The HV-plateau auto-stop rule (`HV_PLATEAU_WINDOW = 2`, `HV_PLATEAU_REL_THRESHOLD = 0.01`) fired on
[t0106] at gen 39, [t0112] at gen 21, [t0113] at gen 14 (premature, below the [t0102]-cited Mohacsi
2024 20-60 gen convergence band). After [t0113]'s premature stop, the project switched to
**HV-plateau auto-stop DISABLED** for [t0114] and [t0115] per S-0113-03, with operator stop
substituted instead. [t0114] stopped at gen 62 with HV = 111.5353 (operator stop after visible
plateau at HV~111); [t0115] stopped at gen 55 with HV = 50.5646 (operator stop after visible plateau
~HV 50). [t0114]'s offline detector replay recommended new defaults `(W*, T*) = (3, 0.015)` but
those have not been adopted for any of the 5 batch seeds; the canonical report must document that
the auto-stop rule is **NOT uniform** across the 5 seeds, which is part of the "harmonised
conventions" deliverable.

### Pool-restart cadence drifts at t0112 (the `_POOL_RESTART_EVERY = 10` rule)

[t0106] ran with `_POOL_RESTART_EVERY = 25` (legacy cadence); [t0112] / [t0113] / [t0114] / [t0115]
all ran with `_POOL_RESTART_EVERY = 10` per the project's "10th gen rule" memory note. This is
recorded as `POOL_RESTART_CADENCE` in
`tasks/t0115_seed9354_no_autostop/code/build_results.py:169-175`. The canonical chart helper
`chart_hv_vs_gen_5seeds` (`build_results.py:702-740`) annotates these restart events as faint dotted
vertical lines — t0121 should reuse this annotation for the canonical HV trajectory overlay so the
visual makes the cadence drift legible.

### Hay 2011 and Druckmann 2007 comparison values are already pinned in `compare_literature.md`

The literature comparison numbers used by the canonical report come straight from [t0114]'s and
[t0115]'s `compare_literature.md` files
(`tasks/t0114_seed7755_no_autostop/results/compare_literature.md`,
`tasks/t0115_seed9354_no_autostop/results/compare_literature.md`):

* **Hay 2011 envelope upper bound** (full perisomatic + back-propagating AP fits): **0.40%** (~2000
  accepted / 500,000 evaluations on the 22-d L5b pyramidal cell; cited "[Hay2011, p. 4]" in
  [t0114]'s `compare_literature.md`).
* **Hay 2011 perisomatic-only bottleneck**: **0.0104%** (52 accepted / 500,000 evals; cited
  "[Hay2011, p. 6]"; the "substrate-limited counterexample").
* **Druckmann 2007 baseline**: **0.10%** (300 accepted / 300,000 evals on 12-d cortical interneuron;
  cited "[Druckmann2007, Fig 3 + Methods]").
* **Mohacsi 2024 convergence band**: **20-60 gens** (NSGA-II asymptotes on 3-12 param problems;
  cited "[Mohacsi2024, Fig 4]").

Paper assets to cite via relative paths, hosted under three earlier tasks:
`tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md`
([t0078] hosts Hay 2011),
`tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md` ([t0097] hosts
Druckmann 2007), and
`tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md` ([t0102] hosts
Mohacsi 2024) — all three exist in the repo as verified by direct `ls`.

### A pooled-cells parquet loader pattern already exists ([t0117])

[t0117] established a clean pattern for pooling raw NSGA-II evaluation records across multiple seeds
into a single parquet (`pooled_all_cells.parquet`, ~32 MB) with branching on file suffix (`.json.gz`
vs `.jsonl.gz`) — see
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/load_pooled_cells.py:1-58`. t0121's
required `pooled_legit_jointpass_cells.parquet` is a much simpler subset (LEGIT joint-pass cells
only, with seed-of-origin annotation), but the suffix-branching loader pattern and the
dedup-by-rounded-68d-vector convention from [t0117] are directly reusable.

### No statistical-bootstrap helper exists in the codebase

A repo-wide search for `scipy.stats`, `bootstrap`, `confidence_interval`, `percentile` matches
`tasks/t0105_cluster_factor_analysis_dsi_pd/code/factor_bootstrap.py` — but that bootstraps
**factor loadings** (PCA), not a scalar acceptance rate. The various `bootstrap.py` files across the
NSGA-II lineage (`t0102` / `t0104` / `t0106` / `t0112` / `t0114` / `t0115`) are all **NEURON
bootstrap** modules (cross-platform NEURON simulator setup), unrelated to statistical bootstrapping.
The bootstrap CI (B=10000) that the t0121 plan asks for is therefore **new code** — a few lines of
`numpy` resample-the-5-rates-with-replacement, take the 2.5 / 97.5 percentiles. No reusable helper
to copy.

### The canonical chart suite already exists in [t0115]

[t0115]'s `build_results.py` ships four 5-seed charts that overlap heavily with t0121's required
chart set:

* `chart_hv_vs_gen_5seeds` (line 702-740) → t0121's `hv_trajectory_5seed_overlay.png`.
* `chart_pareto_front_5seeds` (line 743-789) → can be repurposed for the
  `dsi_pd_scatter_5seed_pooled.png` (Pareto cells only; pooled DSI-vs-PD scatter is broader).
* `chart_substrate_rate_5seed_with_literature` (line 826-891) → directly delivers t0121's
  `per_seed_acceptance_bar.png` with Hay / Druckmann reference lines and 5-seed mean + SE error bar.
  The only delta is the new requirement to add a bootstrap-CI error bar alongside the normal-approx
  one.
* `chart_joint_pass_yield_5seeds` (line 792-823) → useful for the analysis section even though the
  task description does not list it as a required chart.

All four charts use a uniform color / marker key (`SEED_COLORS`, `SEED_MARKERS`, `SEED_LABELS` at
line 148-168) that t0121 should copy verbatim to keep the canonical report visually consistent with
the upstream per-seed reports.

## Reusable Code and Assets

### Charts and CSV builders from [t0115] `build_results.py` — **copy into task**

* **Source**: `tasks/t0115_seed9354_no_autostop/code/build_results.py` (1,514 lines total).
* **What it does**: loads all 5 seed evaluation dumps, computes `PerSeedSummary` per seed, computes
  `SubstrateStats` (mean / SD / SE), writes `joint_pass_summary_5seeds.csv` /
  `substrate_rate_5seed.csv`, builds 4 charts.
* **Reuse method**: **copy into task** — split into focused t0121 modules:
  * `paths.py` (~50 lines): paths to the 5 source task evaluation dumps, t0121 output paths.
  * `loaders.py` (~80 lines): `_load_evaluations`, `_load_hv`, `_load_pareto_cells`,
    `_compute_pareto_front`, `_is_legit_joint_pass`, `_summarize_seed`.
  * `stats.py` (~50 lines): `SubstrateStats`, `_compute_substrate_stats`, plus a **new**
    bootstrap-CI helper (`bootstrap_ci_for_rates(rates, b=10000) -> (lo_pct, hi_pct)` using
    `numpy.random.default_rng(seed=42).choice(rates, size=(b, n), replace=True).mean(axis=1)` then
    `np.percentile`).
  * `csv_writers.py` (~120 lines): `csv_per_seed_substrate_rate_5seed`, plus a new
    `csv_pooled_legit_jointpass_cells` (parquet writer).
  * `charts.py` (~300 lines): `chart_hv_trajectory_5seed_overlay`, `chart_per_seed_acceptance_bar`,
    `chart_dsi_pd_scatter_5seed_pooled`.
* **Function signatures to import** (after copy + rename to t0121 namespace):
  * `_load_evaluations(path: Path) -> list[dict[str, Any]]`
  * `_load_hv(path: Path) -> list[dict[str, Any]]`
  * `_load_pareto_cells(path: Path) -> list[dict[str, Any]]`
  * `_summarize_seed(*, key: str, ds: SeedDataset) -> PerSeedSummary`
  * `_compute_substrate_stats(*, summaries: dict[str, PerSeedSummary]) -> SubstrateStats`
  * `csv_substrate_rate_5seed(*, summaries, stats) -> Path`
  * `chart_hv_vs_gen_5seeds(*, datasets) -> Path`
  * `chart_substrate_rate_5seed_with_literature(*, summaries, stats) -> Path`
* **Adaptation needed**:
  * Change every `from tasks.t0115_seed9354_no_autostop.code.*` import path to
    `from tasks.t0121_5seed_substrate_rate_canonical_report.code.*`.
  * Extend `_compute_substrate_stats` to also return bootstrap (lo, hi) percentiles.
  * Add `chart_substrate_rate_5seed_with_literature` an extra `ci_lo_pct, ci_hi_pct` error-bar pair
    alongside the normal-approx SE bar.
  * Write a new `pooled_legit_jointpass_cells.parquet` writer (pandas DataFrame from each
    LEGIT-joint-pass cell across the 5 seeds with `seed`, `task_id`, `generation`, `dsi`, `pd`,
    `cell_id`) — ~30 lines.
* **Line count to copy**: approximately **500-600 lines** of the 1,514-line source file (the rest is
  t0115-specific predictions-asset and metrics builders that t0121 does not need).

### Threshold constants — **copy into task**

* **Source**: `tasks/t0115_seed9354_no_autostop/code/build_results.py:98-107`.
* **What it provides**: `DSI_THRESHOLD = 0.5`, `PD_RATE_THRESHOLD_HZ = 30.0`,
  `LEGIT_DSI_CEILING = 0.9999`, `SILENCE_GUARD_DSI = 1.0`, `HAY_2011_RATE_PCT = 0.40`,
  `DRUCKMANN_2007_RATE_PCT = 0.10`.
* **Reuse method**: **copy into task** — into `tasks/t0121_*/code/constants.py`. Add
  `HAY_2011_PERISOMATIC_RATE_PCT = 0.0104` (cited but not pinned as a constant in [t0115]).
* **Line count**: ~10 lines.

### Seed-display metadata — **copy into task**

* **Source**: `tasks/t0115_seed9354_no_autostop/code/build_results.py:109-182` (`ASSET_DECLARED`,
  `SEED_COLORS`, `SEED_MARKERS`, `SEED_LABELS`, `POOL_RESTART_CADENCE`, `ALL_SEED_KEYS`).
* **What it provides**: canonical per-seed metadata block — task_seed, n_generations_completed,
  n_cells_total, final_hypervolume, stop_trigger, plus color / marker / label / pool-restart cadence
  for the canonical 5-seed chart key.
* **Reuse method**: **copy into task** as `tasks/t0121_*/code/seed_metadata.py`.
* **Line count**: ~75 lines.

### Pooled-evaluations loader pattern — **copy into task** (adapt to LEGIT-only subset)

* **Source**:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/code/load_pooled_cells.py:1-100`.
* **What it does**: branches on file suffix (`.json.gz` vs `.jsonl.gz`), pools NSGA-II evaluation
  records across multiple seeds into a single parquet with per-seed counts CSV.
* **Reuse method**: **copy into task** — only the suffix-branching loader skeleton; the
  dedup-by-rounded-68d-vector logic is overkill for the LEGIT-only subset (which is already small)
  so the t0121 version can be substantially simpler.
* **Line count**: ~50 lines of useful structure (full file is 200+ lines).

### Source-task result data files — **read in place** (no copy; reads only)

These five evaluation dumps and HV trajectories are the canonical inputs. They are **read** from
their original task folders; nothing is copied or modified:

* `tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz`
* `tasks/t0106_long_pdnd_nsga2_300gen/results/data/hv_trajectory_seed44.json`
* `tasks/t0106_long_pdnd_nsga2_300gen/results/data/pareto_front_seed44.json`
* `tasks/t0112_t0106_seed77_replicate/results/data/all_evaluations_seed77.json.gz`
* `tasks/t0112_t0106_seed77_replicate/results/data/hv_trajectory_seed77.json`
* `tasks/t0112_t0106_seed77_replicate/results/data/pareto_front_seed77.json`
* `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz`
* `tasks/t0113_t0106_seed2247_replicate/results/data/hv_trajectory_seed2247.json`
* `tasks/t0113_t0106_seed2247_replicate/results/data/pareto_front_seed2247.json`
* `tasks/t0114_seed7755_no_autostop/results/data/all_evaluations_seed7755.json`
* `tasks/t0114_seed7755_no_autostop/results/data/hv_trajectory_seed7755.json`
* `tasks/t0114_seed7755_no_autostop/results/data/pareto_front_seed7755.json`
* `tasks/t0115_seed9354_no_autostop/results/data/all_evaluations_seed9354.json`
* `tasks/t0115_seed9354_no_autostop/results/data/hv_trajectory_seed9354.json`
* `tasks/t0115_seed9354_no_autostop/results/data/pareto_front_seed9354.json`

### Existing answer asset to cite (not reuse) — `t0106-joint-pass-recovery-2dir`

* **Source**: `tasks/t0106_long_pdnd_nsga2_300gen/assets/answer/t0106-joint-pass-recovery-2dir/`.
* **Purpose**: original 1-seed answer to the substrate-yield question; predates the 5-seed batch.
  t0121's answer asset is the 5-seed canonical follow-up, so this earlier answer should be **cited
  as a source_task_id** in t0121's `details.json` but not reused as content.

### Existing `compare_literature.md` files to cite — `t0114` and `t0115`

* **Source**: `tasks/t0114_seed7755_no_autostop/results/compare_literature.md` and
  `tasks/t0115_seed9354_no_autostop/results/compare_literature.md`.
* **Purpose**: source of the Hay 2011 / Druckmann 2007 / Mohacsi 2024 citation phrasing, baseline
  numbers, and methodology-differences boilerplate. t0121's `compare_literature.md` can be a
  tightened, harmonised re-write that supersedes both — citing them as the prior project
  comparisons that this canonical report consolidates.

## Lessons Learned

* **`joint_pass_pct` drift across the lineage** — the most consequential lesson: a metric column
  with the same name and the same units has a different definition in [t0113] / [t0114] vs [t0115]
  (silence-guard included vs LEGIT-only). t0121 must (a) explicitly call this out in the results
  summary, (b) recompute every reported number under the canonical LEGIT convention, and (c) include
  a "convention drift table" so downstream consumers see at a glance that [t0114]'s 12.95% headline
  becomes 8.13% under the canonical convention.
* **t0113's premature HV-plateau auto-stop was a real protocol bug** — [t0114]'s 484-LEGIT-cell
  recovery against [t0113]'s 0-LEGIT outcome on a 4.4x-longer run proves the auto-stop detector at
  `(W=2, T=0.01)` is too aggressive for this 68-d substrate. The S-0113-03 detector
  reparameterisation to `(W=3, T=0.015)` has been computed offline but **not adopted in
  production**; t0121 should note this as a caveat on the 5-seed estimate ([t0113]'s zero
  contribution is plausibly a censoring artefact, not a substrate property).
* **The 5-seed sample SE (1.50%) is larger than both literature baselines** — formal frequentist
  inference cannot reject Hay 2011 (0.40%) or Druckmann 2007 (0.10%) even though the point estimate
  is 6.5x / 25.8x above. The bootstrap CI will likely also bracket both baselines and zero. The
  honest framing is "point-estimate plausibly denser; CI cannot rule out literature" — see
  [t0114]'s and [t0115]'s `compare_literature.md` for the precedent wording.
* **Three of five seeds (44, 7755, 9354) independently exceed the Hay 2011 envelope** — even
  though the CI brackets it. This is the right effect-size framing for the answer asset.
* **Single-file `build_results.py` becomes a 1,500-line monolith** — [t0114] (1,674 lines) and
  [t0115] (1,514 lines) both contain a mix of CSV writers, chart builders, predictions-asset
  builders, and metrics builders in one file. t0121 should split into the focused modules listed
  above (`paths.py` / `loaders.py` / `stats.py` / `csv_writers.py` / `charts.py`) to avoid
  recreating the monolith. The result will be ~600 lines split across 5 small modules rather than
  one giant file.
* **Top-N morphology charts must render full dendrite trees, not just somas** — project memory
  note (operator feedback on [t0114]). [t0115] resolved this with `build_top50_morphologies.py`
  rendering the full apical / basal sections. t0121 doesn't require top-N morphology charts in the
  task plan, but if any morphology figure is added it must follow this convention.
* **Pool-restart cadence of 10 (the "10th gen rule")** — every NSGA-II run after [t0106] uses
  `_POOL_RESTART_EVERY = 10` (project memory note). The canonical HV-trajectory chart should
  annotate restart events for all 5 seeds so the visual makes the cadence drift between [t0106] (25)
  and the others (10) legible.

## Recommendations for This Task

1. **Adopt the t0115 LEGIT convention as the canonical definition.** Recompute every per-seed
   acceptance rate using `n_legit_joint_pass_unique / n_total_evals * 100`. Explicitly include a
   "convention-drift table" in the canonical report showing the old and new numbers per source task
   so reviewers can audit the harmonisation step.

2. **Split [t0115] `build_results.py` into focused t0121 modules.** Copy the relevant functions
   (loaders, summariser, stats, CSV / chart writers) into
   `tasks/t0121_5seed_substrate_rate_canonical_report/code/` split as `paths.py`, `loaders.py`,
   `stats.py`, `csv_writers.py`, `charts.py`, and a thin `main.py` orchestrator. Total estimated
   ~600 lines vs the upstream 1,514-line monolith. Use the per-task `paths.py` / `constants.py`
   convention required by `.claude/rules/task-documents.md`.

3. **Add a bootstrap-CI helper.**
   `numpy.random.default_rng(seed=42).choice(rates, size=(b, n), replace=True).mean(axis=1)` then
   `np.percentile(samples, [2.5, 97.5])` — 5-10 lines, fixed seed for determinism, `b=10000` per
   the plan. Report both normal-approx CI (existing) and bootstrap CI (new) side by side in the
   canonical summary. Expectation: both CIs will bracket Hay 2011 (0.40%) and Druckmann 2007
   (0.10%).

4. **Reuse the [t0115] chart visual key verbatim** — same `SEED_COLORS` / `SEED_MARKERS` /
   `SEED_LABELS` so the canonical report's charts are visually consistent with the upstream per-seed
   results files. Add a bootstrap-CI error bar alongside the existing SE error bar on the per-seed
   acceptance bar chart.

5. **Build the `pooled_legit_jointpass_cells.parquet` from scratch.** ~30 lines: load each seed's
   `all_evaluations_*.json[.gz]`, filter to LEGIT joint-pass cells, annotate with `seed`,
   `source_task`, `generation`, and write to parquet. The dedup-by-rounded-68d-vector pattern from
   [t0117] is overkill for this LEGIT-only subset (already small) and can be skipped.

6. **Cite the existing literature comparison work.** [t0114]'s and [t0115]'s `compare_literature.md`
   files already contain the canonical Hay 2011 (0.40% envelope, 0.0104% perisomatic bottleneck) /
   Druckmann 2007 (0.10%) / Mohacsi 2024 (20-60 gen) phrasing with paper-asset relative paths.
   t0121's `compare_literature.md` should consolidate these into one comparison table that
   supersedes both, citing [t0114] and [t0115] as the prior project comparisons.

7. **Cite [t0106]'s `t0106-joint-pass-recovery-2dir` answer asset.** Reference it via
   `source_task_ids` in t0121's answer asset `details.json` and call it out in the canonical report
   as the 1-seed predecessor that this 5-seed batch supersedes.

8. **Document the t0113 censoring caveat and the S-0113-03 detector reparameterisation
   non-adoption.** The 5-seed sample includes one zero contribution ([t0113]) that is plausibly an
   auto-stop censoring artefact, not a true substrate-yield zero. The canonical report should flag
   this as the dominant uncertainty in the lower tail of the 5-seed mean.

9. **No new library asset** — t0121 is a one-shot write-up; the code is not expected to be reused.
   Do not register any of the copied modules as a library asset.

## Common Patterns Across the 5-Seed Batch

* **`paths.py` + `constants.py` split** — every NSGA-II task in the lineage (`t0106` / `t0112` /
  `t0113` / `t0114` / `t0115`) has a dedicated `paths.py` (centralised `pathlib.Path` constants) and
  `constants.py` (numerical / string constants). t0121 should follow the same split per
  `.claude/rules/task-documents.md`.

* **Top-of-file path resolver** — every task's `paths.py` resolves
  `_THIS_FILE = Path(__file__).resolve()`, `TASK_ROOT = _THIS_FILE.parent.parent`,
  `REPO_ROOT = TASK_ROOT.parent.parent` (see e.g.
  `tasks/t0115_seed9354_no_autostop/code/paths.py:14-16`). This idiom is robust to invocation from
  any CWD; t0121 should copy it.

* **`@dataclass(frozen=True, slots=True)` for all per-seed structures** — `SeedDataset`,
  `PerSeedSummary`, `SubstrateStats`, `SeedSummary` etc. all follow this convention. Required by the
  project Python style guide.

* **Keyword-only function arguments with `*`** — every public function in [t0115]'s
  `build_results.py` uses `def fn(*, kwarg1, kwarg2)`. Required by the project Python style guide
  for functions with 2+ heterogeneous parameters.

* **`matplotlib.use("Agg")` before any pyplot import** — required for headless plotting on the CI
  machine. See `tasks/t0115_seed9354_no_autostop/code/cross_seed_analysis.py:21-23`.

## Task Index

### [t0106]

* **Task ID**: `t0106_long_pdnd_nsga2_300gen`
* **Name**: Long 2-direction NSGA-II at 300 gens, 1 seed, 3 trials (ratio DSI + PD-rate)
* **Status**: completed
* **Relevance**: Source of seed 44 (3744 evals, 121 LEGIT, 3.23%). First seed in the 5-seed batch.
  Provides `all_evaluations_seed44.json.gz` (under `assets/predictions/`),
  `hv_trajectory_seed44.json`, `pareto_front_seed44.json`, plus the project's existing
  `t0106-joint-pass-recovery-2dir` answer asset that t0121's answer cites as prior work.

### [t0112]

* **Task ID**: `t0112_t0106_seed77_replicate`
* **Name**: Seed-77 minimum-change replicate of t0106
* **Status**: completed
* **Relevance**: Source of seed 77 (2016 evals, 7 LEGIT, 0.35%). Second seed; introduces the
  `_POOL_RESTART_EVERY = 10` cadence change that all subsequent seeds inherit.

### [t0113]

* **Task ID**: `t0113_t0106_seed2247_replicate`
* **Name**: Seed-2247 random-seed replicate of t0106
* **Status**: completed
* **Relevance**: Source of seed 2247 (1344 evals, 0 LEGIT, 0.00%). Third seed; HV-plateau auto-stop
  fired prematurely at gen 14 (below the Mohacsi 2024 20-60 band) — produces the zero contribution
  that dominates the lower tail of the 5-seed mean and the dominant uncertainty caveat for the
  canonical report.

### [t0114]

* **Task ID**: `t0114_seed7755_no_autostop`
* **Name**: Seed-7755 NSGA-II replicate of t0106 with HV-plateau auto-stop disabled
* **Status**: completed
* **Relevance**: Source of seed 7755 (5952 evals, 484 LEGIT, 8.13%). Fourth seed; first to run with
  HV-plateau auto-stop DISABLED. Provides the offline detector replay recommending
  `(W*, T*) = (3, 0.015)` and the headline `compare_literature.md` with Hay 2011 / Druckmann 2007
  baseline phrasing that t0121's `compare_literature.md` consolidates. Also provides the
  `joint_pass_summary_4seeds.csv` with the **pre-LEGIT-correction** convention that t0121 must
  surface as a convention-drift example.

### [t0115]

* **Task ID**: `t0115_seed9354_no_autostop`
* **Name**: Seed-9354 NSGA-II replicate of t0106 with HV-plateau auto-stop disabled
* **Status**: completed
* **Relevance**: Source of seed 9354 (5280 evals, 63 LEGIT, 1.19%). Fifth and final seed.
  `build_results.py` provides the **canonical LEGIT convention** for `joint_pass_pct` /
  `acceptance_rate_pct` plus the entire chart and CSV suite that t0121 copies and adapts
  (`csv_substrate_rate_5seed`, `chart_hv_vs_gen_5seeds`, `chart_pareto_front_5seeds`,
  `chart_joint_pass_yield_5seeds`, `chart_substrate_rate_5seed_with_literature`). Already contains
  `results/data/substrate_rate_5seed.csv` with the headline numbers that t0121's task description
  quotes verbatim.

### [t0117]

* **Task ID**: `t0117_pooled_pca_cluster_factor_all_cells_4_seeds`
* **Status**: completed
* **Relevance**: Provides the pooled-evaluations parquet loader pattern (suffix-branching on
  `.json.gz` vs `.jsonl.gz`) in `code/load_pooled_cells.py` that t0121's
  `pooled_legit_jointpass_cells.parquet` builder reuses (simplified, since the LEGIT-only subset is
  small enough to skip the dedup-by-rounded-68d-vector convention).

### [t0119]

* **Task ID**: `t0119_brainstorm_results_23`
* **Status**: completed
* **Relevance**: Commissioning brainstorm session; emitted suggestion `S-0115-02` that gave rise to
  this t0121 task. Confirms the 5-seed mean / SE values (2.58% +/- 1.50%) and literature baseline
  numbers (Hay 0.40%, Druckmann 0.10%) that t0121 must reproduce.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Status**: completed
* **Relevance**: Hosts the Hay 2011 paper asset (`assets/paper/10.1371_journal.pcbi.1002107/`) —
  `summary.md` and `details.json` for the Hay 2011 NSGA-II reference (0.40% full envelope, 0.0104%
  perisomatic-only bottleneck). Cited via relative path from t0121's `compare_literature.md`.

### [t0097]

* **Task ID**: `t0097_multi_obj_optim`
* **Status**: completed
* **Relevance**: Hosts the Druckmann 2007 paper asset
  (`assets/paper/10.3389_neuro.01.1.1.001.2007/`) — `summary.md` and `details.json` for the
  Druckmann 2007 NSGA-II reference (0.10% baseline). Cited via relative path from t0121's
  `compare_literature.md`.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Status**: completed
* **Relevance**: Hosts the Mohacsi 2024 paper asset (`assets/paper/10.1371_journal.pcbi.1012039/`)
  — `summary.md` and `details.json` for the Mohacsi 2024 NSGA-II convergence-horizon reference
  (20-60 gen band). Used in t0121's methodology-differences section to frame the [t0113] premature
  auto-stop caveat.
