---
spec_version: "3"
task_id: "t0099_random_init_pareto_robustness"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-09T00:34:47Z"
completed_at: "2026-05-11T01:30:00Z"
---

## Summary

Ran 3 sequential NSGA-II seeds (11, 22, 33) from totally random LHS-sampled initial populations
on Vast.ai instance 36372909, then ran the local analysis pipeline (per-seed Pareto extraction,
anchor classification, biological scorecard, cross-seed comparison) and built 3 predictions
assets + 1 answer asset + morphology charts. **Headline finding: 0 strict joint-pass cells
across all 3 seeds (55 Pareto cells total) — the warm-start used in t0091 was load-bearing for
reaching the joint-pass corner of objective space within an 8-generation budget.** Total Vast.ai
spend: $7.71 of $20 cap.

## Actions Taken

1. Ran prestep to mark step 9 as in_progress.
2. Spawned `/implementation` subagent which (a) ported t0091 NSGA-II infrastructure into
   `code/` with LHS sampling replacing the 5-anchor warm-start, (b) launched 3 sequential seed
   runs in tmux on Vast.ai instance 36372909, (c) reported back partway through seed 11.
3. Mid-run: raised per-seed cost watchdog from $1.00 to $5.00 (and task total from $3.15 to
   $20.00) per user authorisation to top up Vast.ai credit so seeds 22 and 33 could run all 8
   generations. Seed 11 had its $1.00 cap baked in memory and hit it at gen 5 (cost $1.13).
4. Monitored the run via persistent Monitor task `bd1a63os2` polling the remote log every 5
   min for milestone events. Seeds completed: seed 11 at 2026-05-09T08:32:51Z (5 gens, $1.13),
   seed 22 at 2026-05-09T21:41:43Z (8 gens, $1.96), seed 33 at 2026-05-10T20:33:48Z (8 gens,
   $3.41).
5. Synced all per-seed `pareto_front`, `all_evaluations`, `hv_trajectory`, `nsga2_checkpoint`,
   `init_pop` files from remote via `sync_results_back.sh`.
6. Ran `tasks.t0099_random_init_pareto_robustness.code.run_local_analysis` to execute Phases
   C/D/E/F: per-seed anchor classification + biological scorecard, cross-seed HV comparison,
   anchor-distribution heatmap, Pareto overlay scatter, metrics.json builder, 3 predictions
   assets, 1 answer asset.
7. Wrote `code/build_morphology_charts.py` (reuses t0098 visualisation pattern with the
   t0090/t0080 DLL-loader monkey-patch + t0092 patched generator). Produced
   `headline_best_cells.png` (4-panel comparison: t0091 joint-pass + each seed's best real
   cell) and `cross_seed_top5_morphology_grid.png` (5×3 grid: top 5 real cells per seed,
   colored by nearest t0091 anchor).
8. Ruff + mypy clean on full `code/` tree.

## Outputs

* `code/` — 25 modules (LHS sampling + NSGA-II driver + analysis pipeline + asset builder +
  morphology chart builder)
* `results/data/` — per-seed pareto_front / all_evaluations / hv_trajectory /
  nsga2_checkpoint / init_pop / anchor_tracking / biological_scorecard;
  `cross_seed_summary.json`; `anchor_distribution_table.json`
* `results/images/` — `hv_trajectory_cross_seed.png`,
  `anchor_distribution_heatmap.png`, `pareto_overlay_dsi_pdrate_robust.png`,
  `biological_heatmap_seed{11,22,33}.png`, `headline_best_cells.png`,
  `cross_seed_top5_morphology_grid.png`
* `assets/predictions/random-init-pareto-seed{11,22,33}/` — 3 predictions assets, one per seed
* `assets/answer/random_init_reproducibility_and_warmstart_dependence/` — single answer asset
  with Q1 (reproducibility) + Q2 (warm-start dependence) verdicts
* `results/metrics.json` — explicit_variants format with 4 variants (3 seeds + t0091
  reference)
* `intervention/budget_overrun_seed11.md` — documents the $1.00 cap hit at gen 5 (overshoot
  to $1.13 because watchdog checks at gen boundaries)

## Issues

1. **Seed 11 hit $1.00 watchdog at gen 5** — overshoot to $1.13 because the watchdog only
   checks at gen boundaries, not mid-gen. Documented in `intervention/budget_overrun_seed11.md`.
   The user later authorised raising the per-seed cap to $5.00, which seed 11's running
   process couldn't read (in-memory frozen value). Seed 11 still produced 19 Pareto cells,
   sufficient for the cross-seed comparison.

2. **`rall_exponent` axis sampled in [~0, ~5]**, wider than t0091 plan-stated bounds
   [0.5, 2.0]. Means the t0099 search space is genuinely wider than t0091's on this one axis,
   slightly complicating the warm-start vs no-warm-start comparison. Flagged for the
   compare-literature step.

3. **Per-gen wall-clock roughly doubled by mid-run** (e.g., seed 22 gen 1 = 52 min, gen 8 =
   167 min; seed 33 gen 6 = 222 min). Most likely cause: higher-firing-rate cells in late
   gens require finer NEURON time-stepping. Smaller contributions from fewer NaN-aborts and
   possible NEURON state accumulation. Flagged for creative-thinking step.

4. **Idle billing post-completion**: instance was destroyed ~2.6 hours after seed 33 finished
   (not the 12+ hours initially feared); $0.43 idle waste, $7.71 total task cost.
