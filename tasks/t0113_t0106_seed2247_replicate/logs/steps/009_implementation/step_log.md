---
spec_version: "3"
task_id: "t0113_t0106_seed2247_replicate"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-20T00:37:47Z"
completed_at: "2026-05-20T02:05:00Z"
---
# Step 9: implementation

## Summary

Forked t0112 code into `tasks/t0113_t0106_seed2247_replicate/code/` with the single seed-constant
change (`T0112_SEEDS = (77,)` -> `T0113_SEEDS = (2247,)`) plus the package-path rewrite. Ran the
5-check smoke gate (all green; remote anchor-1 = 44.52 Hz vs 43.6 Hz target). Launched the NSGA-II
driver on Vast.ai instance 37107202 (60 parallel workers, 96 pop, 60 gen ceiling, HV-plateau primary
stop). The driver completed in 37.3 min (2236 s wall clock) at gen 14 when the HV-plateau detector
triggered (watchdog NOT tripped). Built the predictions asset `t0113-bedb-morph-nsga2-seed2247`
matching the t0112 schema (spec_version "2", gzipped JSONL, all 8 required `metrics_at_creation`
keys). Asset and code pass all available verificators.

## Actions Taken

1. Spawned a `/implementation` subagent (twice in succession; the first did the full pipeline up
   through SCP launch + monitoring, the second handled the post-run finalisation).
2. The first subagent: forked 35 t0112 .py files into `code/`, applied the seed/budget rename in
   `constants.py`, performed the global `tasks.t0112_t0106_seed77_replicate` ->
   `tasks.t0113_t0106_seed2247_replicate` path rewrite, ran the local 5-check smoke gate (4 fast
   checks on Windows; check 1 single-eval anchor-1 deferred to remote), uploaded the package via
   tar+SCP, recompiled the t0080 MOD library on the remote, ran the remote anchor-1 check (PD =
   44.52 Hz, within tolerance), then launched the driver in tmux session `nsga2`.
3. Polled the remote driver state every ~9 min while the run executed. Confirmed the in-driver pool
   restart at gen 10 cleared the NEURON memory leak (gen 10 wall-clock = 252 s -> gen 11 wall-clock
   = 63 s, a 4x speedup). No instance-level restart was required.
4. The driver hit HV-plateau auto-stop after gen 14 (the detector's window covered gens 11-13 where
   the relative HV change was <0.1 percent; gen 14 added one new silence-guard cell but was inside
   the plateau-trigger window).
5. The second subagent SCP'd all `results/data/*.json`,
   `logs/steps/009_implementation/{driver.log, hv_trace.jsonl}`, and the 14 dill checkpoint pkls
   down to the worktree; gzipped the two largest results JSON files (`all_evaluations_seed2247.json`
   2.84 MB -> 776 KB; `nsga2_checkpoint_seed2247.json` 2.84 MB -> 764 KB).
6. The second subagent built the predictions asset folder
   `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/` with
   `details.json` (spec_version "2"), `description.md` (all 7 mandatory sections, 2,004 words), and
   `files/all_evaluations_seed2247.json.gz` (696 KB, 1,344 records).
7. The second subagent ran `ruff check --fix`, `ruff format`, and
   `mypy -p tasks.t0113_t0106_seed2247_replicate.code` (no issues; task code is excluded from mypy
   by project-wide `pyproject.toml` convention, matching t0112).
8. The `verify_predictions_asset`, `verify_predictions_description`, and
   `verify_predictions_details` verificator scripts do NOT exist in this framework (t0112 hit the
   same `ModuleNotFoundError`). Manual structural validation against
   `meta/asset_types/predictions/specification.md` v2 returned 0 errors and 2 expected warnings
   (`PR-W014: model_id is null`, `PR-W015: dataset_ids is empty`), both inherent to NSGA-II runs
   that have no model or dataset asset link.

## Outputs

### Predictions Asset

* `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/details.json`
  (spec_version "2", 8 `metrics_at_creation` keys, 1 file).
* `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/description.md`
  (frontmatter + 7 mandatory sections, 2,004 words).
* `tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz`
  (696 KB; 1,344 records, 5-field per-cell schema matching t0112).

### Raw Data (results/data/)

* `algorithm_config.json` — pymoo Algorithm config dump
* `evaluation_seeds.json` — list of 3 evaluation seeds used per cell
* `init_pop_seed2247.json` — initial population vectors
* `hv_trajectory_seed2247.json` — 14-gen HV trajectory
* `pareto_front_seed2247.json` — final 8-cell Pareto front
* `all_evaluations_seed2247.json.gz` — all 1,344 per-cell evaluations (gzipped from 2.84 MB)
* `nsga2_checkpoint_seed2247.json.gz` — per-gen population snapshots (gzipped from 2.84 MB)

### Logs

* `logs/steps/009_implementation/smoke_gate.json` — local 5-check smoke gate report
* `logs/steps/009_implementation/smoke_gate_report_remote.json` — remote anchor-1 evaluation report
* `logs/steps/009_implementation/hv_trace.jsonl` — 14 lines, one per generation
* `logs/steps/009_implementation/checkpoints/checkpoint_seed2247_gen{0001..0014}.pkl` — 14 dill
  checkpoints (note: per-gen dill failed with
  `NotImplementedError: pool objects cannot be passed between processes or pickled`, but the JSON
  checkpoint + trace are the primary resume channels)

### Headline Run Metrics

* n_generations_completed = 14 (HV-plateau triggered; `watchdog_tripped: false`)
* n_cells_total = 1,344 (96 x 14)
* n_joint_pass_unique = 2 (BOTH at DSI = 1.0 silence-guard)
* n_joint_pass_evaluations = 6 (NSGA-II elitism re-evaluated each silence-guard cell across gens)
* best_dsi_ratio = 1.0000 (silence-guard / single-spike artefact)
* best_legit_dsi (non-DSI=1.0) = 0.3651 (gen 7, PD = 10.24 Hz)
* best_pd_rate_hz = 71.67 (gen 10, DSI = 0.0017 — fires roughly equally in both directions)
* final_hypervolume = 45.6221
* final_cost_usd = $0.1467 (of $25 hard cap)
* hv_plateau_gen = 14
* wall_clock_total = 37.3 min on 60 parallel workers

### Comparison to Baselines

| Seed | Gens | Cells | Joint-pass unique | Best legit DSI | Best PD |
| --- | --- | --- | --- | --- | --- |
| 44 (t0106) | 40 | 3,744 | 123 | ~0.95+ | 122.6 Hz |
| 77 (t0112) | 21 | 2,016 | 7 | 0.9535 | 114.8 Hz |
| 2247 (t0113) | 14 | 1,344 | **0 legit** (2 silence-guard) | **0.3651** | 71.67 Hz |

Seed 2247 found ZERO legitimate joint-pass cells — the substrate is far more sensitive to seed
choice than the curated seeds 44 and 77 suggested. The 3-seed range across acceptance % spans 3.3
percentage points (0.00% - 3.30%). This is exactly the variance S-0112-01 was designed to quantify.

## Issues

1. **Dill checkpoint failure on every generation** (NotImplementedError: pool objects cannot be
   passed between processes or pickled). The error is from pymoo's `StarmapParallelization` wrapper
   holding a `multiprocessing.Pool` reference inside the Algorithm object. JSONL trace
   + per-gen evaluations + per-gen JSON checkpoint are written, so the resume channels are
     preserved. Worth a follow-up suggestion in step 14 (`generate-suggestions`).

2. **HV-plateau may have fired prematurely.** Gens 11-13 showed <0.1% relative HV change (within the
   detector window), so it triggered at gen 14. But gen 14 itself had a +26% HV jump from the new
   silence-guard cell. The plateau detector did its job by the configured threshold, but a tighter
   run might benefit from a wider window or stricter min_history. This matches t0112's behaviour
   (plateau at gen 21) — not a t0113-specific bug.

3. **Three named predictions-asset verificators** (`verify_predictions_asset`,
   `verify_predictions_description`, `verify_predictions_details`) do not exist in this framework's
   `arf/scripts/verificators/` directory. Same situation as t0112. Manual validation against
   `meta/asset_types/predictions/specification.md` v2 was performed and returned 0 errors.

4. **REQ-12 / REQ-13 / REQ-14 deferred to step 12 (results).** The plan's Step by Step ends at
   "compute metrics and produce charts" inside step 10 (implementation), but in practice the
   `metrics.json` + 5 charts + 2 CSVs are produced during the orchestrator-managed `results` step
   that comes next. All upstream data needed is in place.

5. **REQ-15 (instance destroyed)** deferred to step 10 (`teardown`). Instance 37107202 is still
   alive at the time of this step log; orchestrator will destroy it next.
