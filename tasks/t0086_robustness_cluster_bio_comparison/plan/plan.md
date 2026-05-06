---
spec_version: "2"
task_id: "t0086_robustness_cluster_bio_comparison"
date_completed: "2026-05-06"
status: "complete"
---
# Plan: Robustness + Cluster + Biological-Plausibility Analysis of t0083 Joint-Pass Cells

## Objective

Run three sequential phases on top of t0083's 18-cell Pareto front: (A) re-evaluate the top 20 cells
(15 joint-pass cells from t0081 + t0083 + 5 closest near-pass cells from t0083's Pareto front) at 24
directions x 30 seeds x 5 outer-seed replications and classify each as Genuine (5/5 replications
joint-pass), Marginal (3-4/5), or Stochastic (<=2/5); (B) cluster Genuine cells in the 54-d v3
parameter space using k-means k=2..6 with silhouette
+ BIC for k selection, hierarchical clustering (cosine + euclidean), UMAP / t-SNE 2D visualisation,
  and 50-sample bootstrap stability ARI; (C) score each cluster centroid against published
  biological priors (Kole 2008, Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch 2005,
  Goldfinger 2000, Stuart 1999, de Rosenroll 2026) producing one answer asset attributing each
  cluster to known biology or flagging as novel/unphysical.

**Done** when: the per-cell robustness classification table, the cluster characterisation tables
(centroids + variance), the UMAP plot, the per-cluster biological-plausibility scorecard, and one
answer asset (`cluster-biological-plausibility-attribution`) all exist; all REQ-1..REQ-X items are
resolved; verificators pass with 0 errors; PR merged to main.

## Task Requirement Checklist

> **Task name**: Robustness + cluster + bio-comparison of t0081/t0083 joint-pass cells.
>
> **Short description**: Re-evaluate top 20 joint-pass cells at 24 dirs x 30 seeds x 5 reps; cluster
> Genuine cells in 54-d; compare to Kole/Werginz/Sivyer/Oesch priors.
>
> **Long description (excerpts from `task_description.md`)**: Phase A (robustness validation):
> select 20 cells = 15 joint-pass + 5 closest near-pass. Re-evaluate at 24 dirs x 30 seeds x 5 outer
> RNG seeds. Classify Genuine / Marginal / Stochastic. Phase B (cluster analysis on Genuine cells):
> k-means k=2..6, silhouette + BIC; hierarchical with cosine and euclidean; UMAP + t-SNE;
> per-cluster centroids + variance; bootstrap stability. Phase C (biological comparison): score
> per-cluster centroid against Kole 2008 / Werginz 2024 / Sivyer 2013 / Branco-Hausser 2010 / Oesch
> 2005 / Goldfinger 2000 / Stuart 1999 / de Rosenroll 2026 priors. Per-cluster verdict: plausible /
> stretched / exotic. Output: one answer asset. **REQ-X cost-watchdog rate-fix (HARD)**: cost
> watchdog MUST source per-instance hourly rate from `machine_log.json`
> `selected_offer.price_per_hour`, not from a hard-coded constant.

| REQ | Description | Step(s) | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Select 15 joint-pass cells (cell 767 + 14 t0083 with DSI>=0.4 AND PD>=10) | Step 4 | `code/select_cells.py` + `results/data/selected_cells.json` |
| REQ-2 | Select 5 closest near-pass cells from t0083 Pareto front by Euclidean distance to (0.4, 10) | Step 4 | Same `selected_cells.json` includes `near_pass` array |
| REQ-3 | Re-evaluate each cell at 24 dirs x 30 seeds x 5 outer-seed replications using `evaluate_parameter_vector` | Step 6-7 | `results/data/replication_results.json` + per-cell `replication_<i>.json` |
| REQ-4 | Record 5 outer RNG seeds deterministically derived from `np.random.SeedSequence(42).spawn(5)` | Step 5 | `results/data/replication_seeds.json` |
| REQ-5 | Classify each of 20 cells as Genuine / Marginal / Stochastic | Step 8 | `results/data/cell_classification.json` |
| REQ-6 | Run k-means k=2..6 on Genuine-cell 54-d parameter vectors; select k via silhouette + BIC | Step 9 | `results/data/clustering_results.json` k-means section |
| REQ-7 | Run hierarchical clustering with cosine and euclidean metrics for cross-validation | Step 9 | `clustering_results.json` hierarchical section |
| REQ-8 | UMAP + t-SNE 2D visualisation overlaid with cluster labels | Step 10 | `results/images/umap_clusters.png`, `tsne_clusters.png` |
| REQ-9 | 50-sample bootstrap stability ARI vs full-sample labels | Step 9 | `clustering_results.json` `bootstrap_ari` field |
| REQ-10 | Per-cluster centroids + within/between cluster variance | Step 9 | `results/data/cluster_centroids.json` |
| REQ-11 | Hard-code biological priors with `paper_id` references in `code/biological_priors.py` | Step 11 | `results/data/biological_priors.json` |
| REQ-12 | Score each cluster centroid against priors (sigma deviations, plausible / stretched / exotic) | Step 12 | `results/data/biological_scorecard.json` + `results/images/biological_plausibility_heatmap.png` |
| REQ-13 | Write one answer asset attributing each cluster to known biology or flagging novel/unphysical | Step 13 | `assets/answer/cluster-biological-plausibility-attribution/{details.json, short_answer.md, full_answer.md}` |
| REQ-X | **Cost watchdog uses actual instance hourly rate from `machine_log.json` `selected_offer.price_per_hour`** | Step 2-3 | `code/cost_watchdog.py`; rate logged at startup; `costs.json` `breakdown.vast_ai.actual_rate_usd_per_hour` field |
| REQ-14 | Hard cost cap $3.50 enforced; trip + graceful termination if exceeded | Step 6 | `code/cost_watchdog.py` `_trip_budget_overrun_if_needed`; `intervention/budget_overrun.md` if tripped |
| REQ-15 | Vast.ai 64-core EPYC 7B13 instance (fallback: any 36+ core EPYC at <$0.40/hr if 7B13 unavailable at <$0.35/hr) | Step 1 | `logs/steps/008_setup-machines/machine_log.json` |
| REQ-16 | All replication seeds + per-cell parameter-vector hashes recorded for reproducibility | Step 5, 8 | `replication_seeds.json` + `cell_param_hashes.json` |

## Approach

The approach reuses the t0080 v3 substrate library (`de_rosenroll_2026_dsgc_ais_dendritic_spike`)
and the canonical `evaluate_parameter_vector` per-cell evaluator unchanged. Outer-seed control is
achieved via monkey-patching the t0080 module-level `SEED_BASE` constant before each of the 5
replications per cell. The cluster analysis stack uses scikit-learn (existing project dep) plus
UMAP-learn (newly added). Biological priors are hard-coded in `code/biological_priors.py` with
explicit `paper_id` references for audit.

The cost watchdog (REQ-X) is a copy-with-fix of t0080's `_elapsed_cost_usd` /
`_trip_budget_overrun_if_needed` pattern: instead of reading the hard-coded
`HOURLY_RATE_USD = 0.2382` from `t0080.constants`, t0086's `code/cost_watchdog.py` reads the actual
rate from the machine_log.json `selected_offer.price_per_hour` field at startup and patches the
t0080 module's `HOURLY_RATE_USD` global. This prevents a recurrence of t0083's $0.83 (16%) overrun
which was caused by the in-loop watchdog using the $0.2382/hr default when the actual offer billed
at $0.3209/hr.

**Alternatives considered**:

* **Refactor t0080 to accept a `seed_base` parameter** instead of monkey-patching: rejected because
  t0080 is a completed task whose code is immutable. Monkey-patching the imported constants is the
  smallest-diff path.
* **Run 10 replications per cell** instead of 5: rejected because it doubles the cost envelope
  ($3.50 cap would not absorb it). 5 reps cleanly distinguish Genuine (5/5) from Marginal (3-4/5)
  from Stochastic (<=2/5); the 5/3/<=2 Genuine/Marginal/Stochastic boundary has a clear
  binary-cumulative-distribution interpretation.
* **Run all 18 t0083 Pareto cells** instead of 20-cell mix: rejected because 3 of the 18 are
  joint-pass and 15 are non-joint-pass; the requested 5 closest near-pass cells contains more signal
  about the joint-pass boundary than 12 cells far from the joint corner.

**Task types**: `experiment-run` (Phase A), `data-analysis` (Phase B), `answer-question` (Phase C).
All three present in `task.json`.

## Cost Estimation

Itemised:

* Vast.ai 64-core EPYC 7B13: 6-8 hours @ ~$0.32/hr (target offer rate <$0.35/hr) = **$1.93-$2.57**
  for Phase A re-evaluation.
* Phase B (local CPU clustering): $0.
* Phase C (local CPU biological scorecard + answer asset): $0.

**Total estimated cost: $1.93-$2.57.**

**Hard cost cap: $3.50** (1.5x of estimate; absorbs ~16% per-instance variance like t0083's
overrun). Project budget left is $6.04, so $3.50 leaves a $2.54 buffer for any subsequent S-0083-*
follow-ups.

## Step by Step

1. **[CRITICAL] Provision Vast.ai instance via setup-machines step.** Search for AMD EPYC 7B13
   64-core with `cpu_ram>=300 GB`, `disk_space>=40 GB`, `reliability>=0.995`, `cuda_max_good>=12.6`,
   `compute_cap<1200`. Order by `dph` ascending. Pick lowest-rate offer with rate `< $0.35/hr`.
   Fallback: any 36+ core EPYC at `< $0.40/hr`. Provision via `vastai create instance`. Record full
   machine_log.json with `selected_offer.price_per_hour`. Verify SSH connectivity and per-cell
   parallelism. Satisfies REQ-15.

2. **Implement REQ-X cost-watchdog rate-fix.** Create
   `tasks/t0086_robustness_cluster_bio_comparison/code/cost_watchdog.py` that reads
   `tasks/t0086_*/logs/steps/008_setup-machines/machine_log.json` `selected_offer.price_per_hour` at
   module init and assigns
   `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants.HOURLY_RATE_USD` to the resolved
   value. Log the resolved rate at startup with
   `print(f"[cost_watchdog] resolved rate: ${rate:.4f}/hr from machine_log.json")`. Re-implement
   `_elapsed_cost_usd()` and `_trip_budget_overrun_if_needed()` reading from t0086's own
   `_HARD_BUDGET_USD = 3.50`. Satisfies REQ-X, REQ-14.

3. **Add UMAP-learn to pyproject.toml.** Run `uv add umap-learn` from the worktree. Verify with
   `uv run python -c "import umap; print(umap.__version__)"`. Commit `pyproject.toml` and `uv.lock`
   updates. Pre-deps for Step 9-10.

4. **Select the 20 cells.** Create `code/select_cells.py` that:
   * loads cell 767 from `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json`;
   * loads `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json`, filters to
     `dsi >= 0.4 AND pd_rate_hz >= 10 AND is_feasible == True`, expects 14 records;
   * loads `tasks/t0083_*/results/data/pareto_front.json`, filters to non-joint-pass cells, ranks by
     Euclidean distance to (0.4, 10) corner using
     `sqrt((max(0, 0.4-dsi) / 0.1)**2 + (max(0, 10-pd) / 5)**2)`, keeps top 5;
   * writes `results/data/selected_cells.json` with three sections: `joint_pass_cells` (15 records),
     `near_pass_cells` (5 records), `total` (20). Verify the output: 15 joint-pass + 5 near-pass =
     20 cells. Satisfies REQ-1, REQ-2.

5. **Generate replication seeds.** Create `code/generate_seeds.py` that:
   * draws 5 seeds deterministically:
     `seeds = [int(x.entropy) % 2**31 for x in np.random.SeedSequence(42).spawn(5)]`;
   * writes `results/data/replication_seeds.json` with `{"parent_seed": 42, "seeds": [...]}`.
     Verify: 5 distinct positive integers. Satisfies REQ-4.

6. **[CRITICAL] [validation gate] Run Phase A on cell 767 only at 1 replication first.** Before
   running the full 100 cell-evaluations, run cell 767 at the first seed only as a smoke test.
   Expected: DSI between 0.40 and 0.55, PD between 10 and 14 Hz (matching t0081's reported DSI 0.494
   / PD 11.39). If the smoke test fails (DSI < 0.30 OR PD < 8), HALT and debug -- the harness or
   library import is broken. Implementation:
   `uv run python -m tasks.t0086_robustness_cluster_bio_comparison.code.run_phase_a --smoke-only --cell-id 767 --seeds-only 1 --max-workers 43`.
   Satisfies REQ-3 partial.

7. **[CRITICAL] Run Phase A full sweep.** Execute
   `uv run python -m tasks.t0086_robustness_cluster_bio_comparison.code.run_phase_a --all-cells --max-workers 43`
   on the Vast.ai instance. The script:
   * loads `selected_cells.json`;
   * for each of 20 cells, for each of 5 seeds:
     * monkey-patches `t0080.constants.SEED_BASE = seed`;
     * calls
       `evaluate_parameter_vector(params=..., angles_deg=tuple(range(0, 360, 15)), n_seeds=30, max_workers=43)`;
     * records DSI, PD, peak_vm, is_unstable, elapsed_s, parameter_hash;
   * appends each evaluation to `results/data/replication_results.json` after each call (for
     resumability);
   * checks the cost watchdog after each evaluation; trips + halts if `cost > $3.50`. Expected: 100
     cell-evals total; per-cell wall-clock ~13.5 min; full sweep ~5-7 hours. Satisfies REQ-3,
     REQ-14, REQ-16.

8. **Classify cells Genuine / Marginal / Stochastic.** Create `code/classify_cells.py`:
   * for each cell, load its 5 replication results;
   * count `n_pass = sum(1 for r in results if r.dsi >= 0.4 and r.pd_rate_hz >= 10)`;
   * classify: Genuine (`n_pass == 5`), Marginal (`3 <= n_pass <= 4`), Stochastic (`n_pass <= 2`);
   * write `results/data/cell_classification.json` with per-cell
     `{cell_id, classification, n_pass, dsi_mean, dsi_sd, pd_mean, pd_sd, parameter_hash}`.
     Satisfies REQ-5, REQ-16.

9. **Run Phase B clustering on Genuine cells.** Create `code/cluster_analysis.py` and
   `code/run_phase_b.py` that:
   * load `cell_classification.json`; filter to `classification == "Genuine"`;
   * extract their 54-d parameter vectors; min-max-normalise per parameter using LOWER_BOUNDS /
     UPPER_BOUNDS from t0080;
   * run k-means k=2..6 with `random_state=42`, `n_init="auto"`; compute silhouette + manual BIC;
     select best k as `argmax(silhouette) ` if silhouette and BIC agree, else `k=2` (conservative);
   * run hierarchical with `metric=cosine, linkage=average` and `metric=euclidean, linkage=average`
     for k=best_k; report ARI between k-means and hierarchical labels;
   * run 50-sample bootstrap stability: re-run k-means on 50 subsamples (each is 80% of Genuine
     cells); compute ARI vs full-sample labels; report mean +/- SD;
   * compute per-cluster centroids (mean of normalised params per cluster) and within/between
     cluster variance;
   * write `results/data/clustering_results.json` (k-means + hierarchical labels per cell;
     silhouette, BIC, bootstrap ARI per k) and `results/data/cluster_centroids.json` (centroids in
     both normalised and unnormalised space, per-cluster size, within/between variance). Satisfies
     REQ-6, REQ-7, REQ-9, REQ-10.

10. **Generate UMAP + t-SNE plots.** Create `code/run_phase_b_plots.py`:
    * UMAP:
      `umap.UMAP(n_components=2, n_neighbors=min(5, n_genuine_cells - 1), min_dist=0.3, random_state=42)`;
    * t-SNE:
      `sklearn.manifold.TSNE(n_components=2, perplexity=min(5, n_genuine_cells - 1), random_state=42)`;
    * scatter plot coloured by k-means labels; annotate cell_id;
    * save `results/images/umap_clusters.png` and `tsne_clusters.png` at 200 DPI. Satisfies REQ-8.

11. **Build biological priors table.** Create `code/biological_priors.py` with a `BIOLOGICAL_PRIORS`
    list containing per-prior dataclass entries:
    `{parameter_name, param_index (t0080 ParamIndex), published_mean, published_sigma, paper_id, units, description}`.
    Tabulate each prior:
    * AIS Nav density (Kole 2008: 0.25-0.5 S/cm^2; sigma 0.1; paper_id `10.1038_nn.2153`);
    * AIS Nav density (Werginz 2024: 1.3 S/cm^2; sigma 0.2; paper_id TBD);
    * AIS-to-soma Nav ratio (Werginz 2024: 17.3x; sigma 3.0);
    * Dendritic NMDA conductance (Sivyer 2013: 0.1 nS; sigma 0.05);
    * Dendritic NMDA Mg-block voff (Branco-Hausser 2010: -25 mV; sigma 5);
    * Distal Nav1.6 density (Oesch 2005: 0.05 S/cm^2; sigma 0.02);
    * Distal NaP density (Stuart 1999 / Goldfinger 2000: 0.0005 S/cm^2; sigma 0.0002);
    * GABA spatial slope (de Rosenroll 2026: linear gradient; sigma per fit). Write
      `results/data/biological_priors.json` from this list. Satisfies REQ-11.

12. **Score clusters against priors.** Create `code/biological_scorecard.py` and
    `code/run_phase_c.py`:
    * load `cluster_centroids.json` (unnormalised) + `biological_priors.json`;
    * per cluster, per prior: deviation = `(centroid_value - published_mean) / published_sigma`;
      verdict: `plausible` if `abs(deviation) <= 2`, `stretched` if `2 < abs(deviation) <= 5`,
      `exotic` if `abs(deviation) > 5`;
    * per cluster: aggregate verdict = worst-case across priors; cluster overall verdict `plausible`
      only if all priors plausible;
    * write `results/data/biological_scorecard.json` (per-cluster, per-prior, deviation+verdict);
    * generate `results/images/biological_plausibility_heatmap.png` (cluster x prior; cell colour by
      deviation in sigma units; annotate verdict). Satisfies REQ-12.

13. **Write the answer asset.** Create `assets/answer/cluster-biological-plausibility-attribution/`:
    * `details.json` per `meta/asset_types/answer/specification.md`;
    * `short_answer.md` (Question + Answer 2-5 sentences + Sources);
    * `full_answer.md` (Question + Short Answer + Research Process + Evidence sections + Synthesis +
      Limitations + Sources). The Question: "Which clusters of joint-pass cells in t0083's expanded
      population are biologically plausible vs novel/unphysical, and which dendritic-spike machinery
      do the plausible clusters represent?" The Answer cites the per-cluster scorecard verdicts. Run
      `verify_answer_asset.py --task-id t0086 cluster-biological-plausibility-attribution`.
      Satisfies REQ-13.

## Remote Machines

Vast.ai 64-core EPYC 7B13 (or 36+ core EPYC fallback). Reliability >= 0.995 (5-24 h budget).
Estimated runtime 6-8 hours wall-clock. No GPU required (CPU-only NEURON simulation). Reference:
`arf/specifications/remote_machines_specification.md`. Single instance for the entire Phase A sweep;
tear down immediately after results download.

## Assets Needed

* `de_rosenroll_2026_dsgc_ais_dendritic_spike` library (registered under t0080); imported via
  `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import evaluate_parameter_vector, ParameterVector`.
* `tasks/t0083_*/results/data/all_evaluations.json` (1728 records).
* `tasks/t0083_*/results/data/pareto_front.json` (18 cells).
* `tasks/t0081_*/results/data/all_evaluations.json` (768 records; cell 767 source).
* `tasks/t0084_*/results/results_summary.md` (cell 767 mechanism attribution; informs Phase C
  cell-767 cluster narrative).

## Expected Assets

* **answer**: `cluster-biological-plausibility-attribution` -- per-cluster biological plausibility
  verdict, sources from Kole/Werginz/Sivyer/Branco-Hausser/Oesch/Goldfinger/Stuart/de Rosenroll
  papers in the corpus, and the t0084 cell-767 mechanism-attribution answer asset. Format:
  `details.json` + `short_answer.md` + `full_answer.md`.

## Time Estimation

* Step 1 (provisioning): 15-30 min wall-clock.
* Step 2-5 (REQ-X cost-watchdog, deps, cell selection, seeds): 30 min local.
* Step 6 (smoke gate): 5 min on Vast.ai.
* Step 7 (Phase A full sweep): **5-7 hours wall-clock** on Vast.ai.
* Step 8-10 (Phase B classification + clustering + plots): 30 min local.
* Step 11-12 (Phase C priors + scorecard): 30 min local.
* Step 13 (answer asset): 30 min local.
* Step 14-15 (results + suggestions + reporting + PR): 1 hour local.

**Total: ~8-10 hours wall-clock** (most of it Phase A on Vast.ai).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Phase A cost overrun (like t0083) | Low (REQ-X mitigates) | Could blow budget | REQ-X: cost watchdog reads actual rate from machine_log.json; hard cap $3.50 trips graceful termination |
| Vast.ai 7B13 unavailable at <$0.35/hr | Medium | Higher cost | Fallback to any 36+ core EPYC at <$0.40/hr; documented in REQ-15 |
| Per-cell wall-clock exceeds 162s estimate | Medium | Wall-clock overrun | Hard cost cap $3.50 absorbs 1.5x variance; if cap trips early, partial results still useful |
| < 3 Genuine cells (Primary pass criterion fails) | Medium | Phase B clustering not meaningful | Acceptable negative result; project pivots to S-0081-01 multi-replicate at different morphologies |
| All clusters exotic (>5 sigma from priors) | Medium | Headline negative on biological plausibility | Reported as legitimate finding; project pivots to ablation experiments |
| Bootstrap ARI < 0.5 on Phase B | Medium | Low cluster confidence | Disclose in answer asset; degrade per-cluster confidence; note small Genuine sample size |
| umap-learn install conflict on Vast.ai | Low | Step 10 blocked | Step 10 falls back to t-SNE only; UMAP not on critical path |
| Instance crashes mid-sweep | Low | Lost progress | Step 7 appends after each cell-eval; resumable by checking `replication_results.json` for completed cells |
| RNG outer-seed monkey-patch leaks across replications | Low | Confounded reps | Test in smoke gate (Step 6); verify per-cell DSI variance is non-zero |
| Per-cell parameter-vector hashes don't match t0083's | Low (deterministic) | Reproducibility broken | Step 8 records `parameter_hash` per cell; spot-check vs t0083's saved values |

## Verification Criteria

* **REQ-1, REQ-2**: `cat results/data/selected_cells.json | jq '.total'` returns `20`;
  `len(joint_pass_cells)` returns `15`; `len(near_pass_cells)` returns `5`.

* **REQ-3, REQ-16**: `cat results/data/replication_results.json | jq '. | length'` returns `100`;
  each record has `cell_id`, `seed`, `dsi`, `pd_rate_hz`, `peak_vm`, `is_unstable`, `elapsed_s`,
  `parameter_hash`.

* **REQ-4**: `cat results/data/replication_seeds.json | jq '.seeds | length'` returns `5`; all five
  values are positive integers; all distinct.

* **REQ-5**: `cat results/data/cell_classification.json | jq '. | length'` returns `20`;
  classification field in each entry is one of `Genuine` / `Marginal` / `Stochastic`.

* **REQ-6, REQ-7, REQ-9, REQ-10**: `clustering_results.json` contains `kmeans` (with `silhouette`
  and `bic` per k=2..6, `best_k`), `hierarchical_cosine`, `hierarchical_euclidean`, `bootstrap_ari`
  (mean and SD), `cluster_centroids` (one per cluster).

* **REQ-8**: `results/images/umap_clusters.png` and `tsne_clusters.png` both exist; reference in
  `results_detailed.md` `## Visualizations`.

* **REQ-11**: `results/data/biological_priors.json` exists; each prior has `parameter_name`,
  `param_index`, `published_mean`, `published_sigma`, `paper_id`, `units`, `description`; at least 8
  priors.

* **REQ-12**: `results/data/biological_scorecard.json` exists; per cluster, per prior: deviation in
  sigma units + verdict; aggregate per-cluster verdict.

* **REQ-13**: `assets/answer/cluster-biological-plausibility-attribution/` folder exists; passes
  `verify_answer_asset.py`.

* **REQ-X**: `costs.json` `breakdown.vast_ai.actual_rate_usd_per_hour` field exists and matches the
  rate logged in `logs/steps/008_setup-machines/machine_log.json` `selected_offer.price_per_hour`.
  Implementation review: grep `code/cost_watchdog.py` for "selected_offer.price_per_hour" string.

* **REQ-14**: `results/costs.json` `total_cost_usd <= 3.50`; if exceeded,
  `intervention/budget_overrun.md` exists explaining cause.

* **REQ-15**: `logs/steps/008_setup-machines/machine_log.json` `gpu_name` includes "EPYC 7B13" or
  has `cpu_cores >= 36` AND `price_per_hour < 0.40`.

* **All REQs**: `results/results_detailed.md` `## Task Requirement Coverage` section lists all
  REQ-1..REQ-16 + REQ-X with status `Done` / `Partial` / `Not done`, and an evidence pointer.

* **Verificators**: `verify_task_file`, `verify_task_dependencies`, `verify_suggestions`,
  `verify_task_metrics`, `verify_task_results`, `verify_task_folder`, `verify_logs`,
  `verify_research_code`, `verify_plan`, `verify_answer_asset`, `verify_machines_destroyed`,
  `verify_compare_literature`, `verify_pr_premerge` -- ALL pass with 0 errors.
