---
spec_version: "1"
task_id: "t0086_robustness_cluster_bio_comparison"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 6
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-05-06"
status: "complete"
---
# Research Code: Robustness + Cluster + Biological-Plausibility Analysis of t0083 Joint-Pass Cells

## Task Objective

t0086 runs three sequential phases on top of t0083's 18-cell Pareto front: (A) re-evaluate the top
20 cells (15 joint-pass from t0081 + t0083 plus 5 closest near-pass from t0083) at 24 directions x
30 seeds x 5 outer-seed replications and classify Genuine / Marginal / Stochastic; (B) cluster
Genuine cells in the 54-d v3 parameter space using k-means
+ hierarchical + UMAP/t-SNE; (C) score each cluster centroid against published biological priors
  (Kole 2008, Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005, Goldfinger 2000, Stuart
  1999, de Rosenroll 2026) producing one answer asset attributing each cluster to known biology or
  flagging as novel/unphysical. Source suggestion: S-0083-02 (also covers S-0083-05 multi-seed gate
  and S-0081-01 multi-replicate).

## Library Landscape

A single library is relevant: **`de_rosenroll_2026_dsgc_ais_dendritic_spike`** (registered under
[t0080]). Provides the 54-d v3 substrate, the canonical per-cell evaluator
`evaluate_parameter_vector`, the parameter-vector dataclass `ParameterVector`, and the `ParamIndex`
Enum mapping parameter slot 0..53 to semantic name. t0086 imports this library unchanged for Phase A
re-evaluation.

No other libraries discovered are relevant: t0011 visualization library is matplotlib-only and Phase
B/C add their own UMAP / scorecard plots.

External dependencies needed for t0086 beyond the existing project deps: **`umap-learn`** (PyPI). To
be added to `pyproject.toml` if not present.

## Architecture Overview

### Phase A re-evaluation entry points

* **`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver.evaluate_parameter_vector`**
  -- the canonical per-cell evaluator. Signature:

  ```python
  def evaluate_parameter_vector(
      *,
      params: ParameterVector,
      angles_deg: tuple[int, ...],
      n_seeds: int,
      max_workers: int = 0,
  ) -> EvalResult: ...
  ```

  Returns `EvalResult` with `dsi`, `pd_rate_hz`, `n_trials`, `n_errors`, `elapsed_s`, `is_unstable`,
  `peak_vm_mv`. With `angles_deg = tuple(range(0, 360, 15))` (24 angles) and `n_seeds = 30`,
  evaluates 720 trials per call. Inner parallelism via `ProcessPoolExecutor` keyed on `max_workers`
  (default = `cpu_count() - 1`).

* **Outer seed mechanism**: per-trial RNG seed is computed inside `evaluate_parameter_vector` as
  `seed = SEED_BASE + s * 10_007 + int(angle) * 13` where `SEED_BASE` is a module-level constant in
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants` (default value `1000`). To produce
  5 pseudo-independent replications per cell, t0086 monkey-patches `constants.SEED_BASE` and the
  imported `trial_driver.SEED_BASE` global per replication.

* **Parameter-vector source**: 54-d parameter vectors live in
  `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` (1728 records;
  filter by `dsi >= 0.4 AND pd_rate_hz >= 10 AND is_feasible == True` to recover 14 t0083 joint-pass
  cells). Cell 767 from `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json`.
  18-cell Pareto front in `pareto_front.json` (filter to non-joint-pass; rank by Euclidean distance
  to (0.4, 10) joint corner; keep top 5 near-pass).

### Phase B cluster analysis stack

* **scikit-learn** (existing dep): `KMeans`, `silhouette_score`, `AgglomerativeClustering`,
  `adjusted_rand_score`, `TSNE(n_components=2, perplexity=5, random_state=42)`.
* **UMAP-learn** (NEW dep):
  `umap.UMAP(n_components=2, n_neighbors=5, min_dist=0.3, random_state=42)`.
* **BIC for KMeans**: manual computation via `BIC = -2 * log_likelihood + k * ln(n)` (sklearn does
  not expose this directly).

### Phase C biological scorecard

* **Published priors hard-coded** in `code/biological_priors.py`, citing the primary papers (Kole
  2008 cortical AIS Nav 0.25-0.5 S/cm^2; Werginz 2024 mouse alpha-RGC AIS Nav 1.3 S/cm^2 with 17.3x
  soma ratio; Sivyer 2013 dendritic NMDA; Branco-Hausser 2010 Mg-block voff; Oesch 2005, Goldfinger
  2000, Stuart 1999 distal Nav1.6 / NaP densities; de Rosenroll 2026 GABA/AMPA spatial
  distribution).

* **t0080 ParamIndex**: `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants.ParamIndex`
  is the canonical Enum mapping parameter slot (0..53) to semantic name. t0086 references these
  names in the biological priors file and the per-cluster scorecard.

### REQ-X cost-watchdog rate-fix

* **t0083's bug**: `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants.HOURLY_RATE_USD`
  is hard-coded `0.2382`. t0083's actual offer billed $0.3209/hr (1.347x) [t0083].
  `_elapsed_cost_usd()` in `nsga2_loop.py` uses this constant directly. Fix for t0086: monkey-patch
  the t0080 `HOURLY_RATE_USD` global at startup with the rate resolved from
  `logs/steps/<NNN>_setup-machines/machine_log.json` `selected_offer.price_per_hour`.

## Key Findings

### Reusable per-cell evaluator is stable across tasks [t0080] [t0081] [t0083]

`evaluate_parameter_vector` was authored in [t0080] and reused unchanged by [t0081] (warm-start) and
[t0083] (continuation). It produces deterministic results given a parameter vector + angles + seeds
\+ SEED_BASE; this is the contract t0086 relies on for the 5 outer-seed replications. Implementation
at line 332 of `trial_driver.py`. No known bugs; [t0083] reused it for 1728 evaluations with no
per-cell errors.

### NSGA-II saved data formats are standardised across substrate generations [t0080] [t0081] [t0083]

`results/data/all_evaluations.json` and `results/data/pareto_front.json` use the same record schema
in [t0080] (192 cells) [t0081] (768 cells) [t0083] (1728 cells): `cell_index`, `generation`,
`params` (54-element list), `dsi`, `pd_rate_hz`, `is_unstable`, `peak_vm_mv`, `elapsed_s`,
`constraint_violation`, `is_feasible`. t0086's Phase A loader uses one shared schema reader for all
three sources.

### Parameter-vector hashing is deterministic [t0080]

The `placer_seed` for a parameter vector is computed as
`SEED_BASE + (_hash_param_vector(params.values) & 0xFFFF)` -- it depends on `SEED_BASE`. When t0086
monkey-patches `SEED_BASE` per replication, the placer_seed also varies, which means synaptic
placement varies between replications. This is desired behaviour: a "Genuine" cell must be robust to
both per-trial RNG variation AND placer variation.

### Cost-watchdog rate-bug pattern [t0083]

[t0083]'s `costs.json` `note` field documents the bug: in-loop watchdog reported $4.115 spent at
completion (17.3 h x $0.2382/hr) while true Vast.ai charge was $5.55 at run-end and $5.83 at
instance-destroy. Cell-cost accounting still intact: 960 evaluations / 17.3 h = 55.5 cells/h ->
$0.00578/cell, comparable to [t0081]'s $0.00567/cell. The fix is to read the rate from the
machine_log.json at startup, not hard-code it.

### Pareto front + joint-pass criterion alignment [t0083]

[t0083]'s 18-cell final Pareto front contains 3 joint-pass cells (1304, 1559, 1677); the other 15
are non-joint-pass. The full 15 joint-pass cells across the 1728 evaluations are NOT all on the
Pareto front -- 12 are dominated by other cells in the front but still satisfy
`DSI >= 0.4 AND PD >= 10`. t0086 must filter on `all_evaluations.json` (not just the Pareto front)
to recover all 14 t0083 joint-pass cells.

### Clustering on small samples needs cross-validation [t0086 design]

With only 15 Genuine cells (best case), silhouette + BIC scores will be noisy. The
hierarchical-clustering cross-validation with cosine and euclidean metrics is the primary safeguard
against k-means artifacts. Adding a 50-sample bootstrap stability check (ARI vs full-sample labels)
further degrades cluster confidence when needed.

## Reusable Code and Assets

### `evaluate_parameter_vector` -- import via library

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_driver.py` line 332.
* **What it does**: Evaluates a 54-d parameter vector at the specified angles x seeds, returns DSI /
  PD / peak Vm / instability flag. Inner parallelism via `ProcessPoolExecutor`.
* **Reuse method**: import via library `de_rosenroll_2026_dsgc_ais_dendritic_spike`.
* **Adaptation**: none. t0086 calls it 5x per cell with monkey-patched `SEED_BASE` between calls.
* **Line count**: ~80 lines (function body); imported, not copied.

### `ParameterVector` and `ParamIndex` -- import via library

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_driver.py`
  (`ParameterVector`), `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py`
  (`ParamIndex` Enum).
* **What it does**: 54-d parameter container; ParamIndex Enum provides `.NAV16_AIS_GBAR`,
  `.NAV16_SOMA_GBAR`, `.NMDA_VOFF`, etc.
* **Reuse method**: import via library.
* **Adaptation**: none.
* **Line count**: ~50 lines combined; imported.

### Result-file loaders -- copy into task

* **Source**: ad-hoc readers of `all_evaluations.json` / `pareto_front.json` exist in [t0083] but
  they are private helpers (`reload_gen7.py`).
* **What it does**: load JSON arrays into `CellEvaluation` dataclasses.
* **Reuse method**: copy into `code/load_evaluations.py`. Replace with own thin wrapper using
  pydantic models for type safety per project style guide.
* **Adaptation**: t0086 needs per-source filtering (joint-pass; near-pass). New wrapper.
* **Line count**: ~40 lines new code.

### Cost-watchdog (REQ-X) -- copy into task with rate-fix

* **Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/nsga2_loop.py` lines 99-124
  (`_elapsed_cost_usd`, `_trip_budget_overrun_if_needed`).
* **What it does**: tracks elapsed wall-clock since process start; multiplies by hourly rate; trips
  the overrun flag when `cost > BUDGET_USD`.
* **Reuse method**: copy into `code/cost_watchdog.py`.
* **Adaptation**: replace hard-coded `HOURLY_RATE_USD = 0.2382` with rate read from
  `machine_log.json` `selected_offer.price_per_hour` at module init.
* **Line count**: ~40 lines copied + ~15 lines for rate-resolution.

### Phase A / B / C orchestration -- new code

* `code/run_phase_a.py` -- top-level CLI; loads 20 cells, runs 5 reps each, classifies. ~150 lines
  new code.
* `code/run_phase_b.py` -- loads Genuine cells, runs k-means / hierarchical / UMAP / t-SNE, selects
  k via silhouette + BIC, runs bootstrap. ~200 lines.
* `code/run_phase_c.py` -- loads cluster centroids + biological priors, computes scorecard, writes
  answer asset. ~150 lines.
* `code/replication_runner.py` -- per-cell 5-replication wrapper. ~80 lines.
* `code/cluster_analysis.py` -- k-means / hierarchical / silhouette / BIC / bootstrap helpers. ~150
  lines.
* `code/biological_priors.py` -- hard-coded priors with paper_id citations. ~100 lines.
* `code/biological_scorecard.py` -- per-cluster scoring helper. ~80 lines.
* `code/paths.py` -- centralised Path constants. ~50 lines.
* `code/constants.py` -- column names, RNG seeds. ~30 lines.

## Lessons Learned

* **Watchdog rate-resolution must be data-driven** [t0083]: hard-coded constants drift from reality
  when offers change; t0083 over-spent by 16%. t0086 reads the rate at startup.

* **Per-cell wall-clock variance is non-trivial** [t0080] [t0081] [t0083]: ~30-50 s/cell on the v3
  substrate at 8 dirs x 20 seeds. Scaling to 24 dirs x 30 seeds (4.5x) is expected to produce
  ~135-225 s per replication; 5 replications per cell -> ~11-19 min/cell; 20 cells -> ~225-380 min.
  Plan for 6-8 hours wall-clock with 1-hour buffer.

* **Joint-pass count matches expectations only when filtering on full evaluation history** [t0083]:
  filtering only on `pareto_front.json` would miss 12 of the 14 t0083 joint-pass cells. t0086's
  loader must filter on `all_evaluations.json`.

* **Reproducibility requires recording all RNG seeds and the parameter-vector hash basis** [t0080]
  [t0083]: SEED_BASE + parameter vector are sufficient to reproduce; t0086 records
  `replication_seeds.json` and `cell_param_hashes.json`.

* **Inner parallelism should never exceed cell budget** [t0080]: at 64 cores, the 720-sim
  per-replication budget runs in ~150-180 s. Higher parallelism wastes spin-up overhead.

## Recommendations for This Task

1. **Reuse the t0080 library unchanged** for Phase A. Import `evaluate_parameter_vector`,
   `ParameterVector`, and `ParamIndex` directly from the t0080 package. Do not copy the per-cell
   evaluator into t0086.

2. **Monkey-patch `SEED_BASE` per replication** rather than refactoring the t0080 constants module
   to accept a `seed_base` parameter. This is the smallest-diff path that respects the cross-task
   immutability rule.

3. **Implement the REQ-X rate-fix as a copy-into-task `code/cost_watchdog.py`** that reads
   `machine_log.json` `selected_offer.price_per_hour` at module init and patches t0080's
   `HOURLY_RATE_USD` global. Log the resolved rate at startup. This is non-negotiable; the plan must
   explicitly track REQ-X.

4. **Add `umap-learn` to `pyproject.toml`** during the planning step. Verify with
   `uv run python -c "import umap"` after `uv sync`.

5. **Filter joint-pass cells on `all_evaluations.json` not `pareto_front.json`** to recover all 14
   t0083 joint-pass cells. The 5 near-pass cells come from `pareto_front.json` filtered to
   non-joint-pass.

6. **Hard-code biological priors in a per-task module with explicit `paper_id` references**. Each
   prior carries `parameter_name`, `param_index`, `published_mean`, `published_sigma`, `paper_id`,
   `units`. This makes the scorecard reproducible and auditable.

7. **Run a 50-sample bootstrap on Phase B clusters** (sub-sample Genuine cells; recompute k-means;
   report ARI vs full-sample labels). With ~15 cells (best case), bootstrap stability is the primary
   safeguard against k-means artifacts.

## Task Index

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC compartmental model to NEURON
* **Status**: completed
* **Relevance**: Provides the de Rosenroll 2026 base substrate; informs the GABA/AMPA spatial
  distribution biological prior used in Phase C.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B v2 MOBO with AIS tiered AHP (49-d substrate)
* **Status**: completed
* **Relevance**: Parent substrate of t0080 v3; informs the AIS-Nav biological prior; provides the
  warm-start Pareto cells projected into the 54-d space.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery (54-d, NSGA-II)
* **Status**: completed
* **Relevance**: PRIMARY library source. Provides `evaluate_parameter_vector`, `ParameterVector`,
  `ParamIndex`, the v3 substrate library `de_rosenroll_2026_dsgc_ais_dendritic_spike`, and the
  watchdog code pattern that t0086 copies + fixes for REQ-X.

### [t0081]

* **Task ID**: `t0081_bedb_v3_warmstart_nsga2`
* **Name**: Bed B v3 NSGA-II with combined warm-start (project's first joint-pass cell)
* **Status**: completed
* **Relevance**: provides cell 767 (first joint-pass cell) and the warm-start NSGA-II harness; cell
  767 is one of the 20 cells in t0086's Phase A re-evaluation set.

### [t0083]

* **Task ID**: `t0083_bedb_v3_extend_nsga2_gen8plus`
* **Name**: Extend t0081 NSGA-II from gen-7 with adaptive HV-plateau stop
* **Status**: completed
* **Relevance**: provides 14 additional joint-pass cells, the 18-cell final Pareto front (source for
  the 5 near-pass cells), the all_evaluations.json (1728 records), and the cost-watchdog rate-bug
  that motivates REQ-X.

### [t0084]

* **Task ID**: `t0084_t0081_cell_767_vm_trace_deepdive`
* **Name**: Vm-trace deep-dive of cell 767 to attribute the joint-pass DSI mechanism
* **Status**: completed
* **Relevance**: provides the cell-767 mechanism-attribution answer asset; informs the Phase C
  biological priors for the cell-767 cluster (which dendritic-spike machinery dominated).
