# ✅ Re-render t0099 morphology charts with correct 68-d slice

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0100_fix_t0099_morph_charts` |
| **Status** | ✅ completed |
| **Started** | 2026-05-11T01:14:24Z |
| **Completed** | 2026-05-11T01:27:00Z |
| **Duration** | 12m |
| **Dependencies** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Task types** | `correction` |
| **Step progress** | 7/15 |
| **Task folder** | [`t0100_fix_t0099_morph_charts/`](../../../tasks/t0100_fix_t0099_morph_charts/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0100_fix_t0099_morph_charts/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0100_fix_t0099_morph_charts/task_description.md)*

# Re-render t0099 Morphology Charts with Correct 68-d Slice

## Motivation

t0099 (`random_init_pareto_robustness`) produced two morphology visualisations that show only
the soma as a large filled disc, with no dendritic tree visible:

* `results/images/headline_best_cells.png`
* `results/images/cross_seed_top5_morphology_grid.png`

The root cause is a wrong slice in
`tasks/t0099_random_init_pareto_robustness/code/build_morphology_charts.py:114`:

```python
morph_vec: tuple[float, ...] = tuple(vector_68d[:14])
```

The 68-d parameter vector layout is `[54 electrophys, 14 morphology]` (per
`tasks/t0091_morphology_extended_nsga2_v1/code/biological_priors.py:31`: `MORPH_OFFSET = 54`,
and `anchor_tracking.py:160`: `vec_68d[54:]`). Slicing `[:14]` picked the first 14 electrophys
parameters (Na/K conductance densities, AIS sizes, etc.) and passed them to the procedural
morphology generator as if they were `bf`, `mean_segment_length_um`, `branch_prob_per_um`,
etc. The generator received nonsense and emitted a cell with **0 dendrite sections** — only
the soma survives, hence the giant filled circle filling each panel.

The correct slice is `vector_68d[54:]` (or equivalently `vector_68d[54:68]`).

## Scope

### In Scope

* Re-render the two affected PNGs using a corrected copy of t0099's
  `build_morphology_charts.py` with `vector_68d[:14]` -> `vector_68d[54:]`.
* Write a correction overlay (`corrections/file_replace_t0099_morph_chart_grid.json` and
  `corrections/file_replace_t0099_morph_chart_headline.json`) that points downstream consumers
  (aggregators, overview materializer) to the corrected images in this task's
  `results/images/`.
* Verify the corrected images actually show dendritic trees (visual inspection by the
  researcher; no automated visual diff).

### Out of Scope

* Modifying any file inside `tasks/t0099_random_init_pareto_robustness/` (rule 5: completed
  task folders are immutable; corrections overlay handles this).
* Re-running the NSGA-II optimisation. Optimisation code uses the correct slice everywhere;
  the bug never touched the simulation loop. t0099's DSI / PD-rate / robustness / anchor
  distribution / 0-of-55-joint-pass finding all remain valid.
* Re-rendering t0099's other 6 charts (`biological_heatmap_seed*.png`, `pareto_overlay_*.png`,
  `hv_trajectory_cross_seed.png`, `anchor_distribution_heatmap.png`) — those don't use the
  morphology generator at all.

## Approach

1. Copy the relevant rendering code from `t0099/code/build_morphology_charts.py` into
   `tasks/t0100_fix_t0099_morph_charts/code/build_morphology_charts.py` (cross-task code copy
   per CLAUDE.md rule: libraries are the only shared mechanism; non-library code must be
   copied).
2. Apply the single fix: `vector_68d[:14]` -> `vector_68d[54:]` on the only affected line.
3. Run the script locally; it reads from t0099's
   `results/data/pareto_front_seed{11,22,33}.json` + `anchor_tracking_seed{11,22,33}.json` and
   `t0091/results/data/pareto_front.json` + `anchor_tracking.json` (all already on main);
   writes the two re-rendered PNGs into this task's `results/images/`.
4. Visual confirmation: dendrite line segments now visible, soma circles correctly scaled.
5. Write two correction-overlay JSON files under `corrections/` declaring file replacement:
   t0099's `results/images/headline_best_cells.png` -> t0100's
   `results/images/headline_best_cells.png`; same for the cross-seed grid.
6. Run standard task verificators; commit; PR; merge.

## Cost Estimation

* **Total**: $0
* **Compute**: local only (matplotlib + procedural morphology generator; ~10 s wall-clock for
  19 cells across both figures)
* **Paid services**: none
* **Risk-of-going-over**: zero

## Step by Step

1. `init-folders`, `check-deps` (dependency: t0099_random_init_pareto_robustness completed).
2. Copy + fix `build_morphology_charts.py`.
3. Run the script; produce the two corrected PNGs in `results/images/`.
4. Write `corrections/file_replace_t0099_morph_chart_grid.json` and
   `corrections/file_replace_t0099_morph_chart_headline.json`.
5. Write `results/results_summary.md`, `results/results_detailed.md`, `results/metrics.json`,
   `results/costs.json`, `results/remote_machines_used.json`, `results/suggestions.json`.
6. Reporting: run verificators, push, PR, premerge, merge.

## Remote Machines

None.

## Assets Needed

None (reads existing t0099 + t0091 JSON outputs already on main).

## Expected Assets

* No assets in the asset-type sense (no paper / dataset / library / answer / model /
  predictions). The deliverables are 2 corrected PNGs and 2 correction-overlay JSON files.

## Time Estimation

~30 minutes wall-clock: ~5 min code copy + fix + render, ~25 min task scaffolding +
verificators + PR + merge.

## Risks & Fallbacks

* **Re-render fails because t0099's data files are not on main**: confirm
  `pareto_front_*.json` and `anchor_tracking_*.json` are present before starting; abort if
  missing. (Verified present at start of task.)
* **Correction-overlay JSON schema is unfamiliar**: read
  `arf/specifications/corrections_specification.md` before writing; mirror the
  file-replacement pattern from t0093's library correction overlay (`C-0093-01`).
* **The rendered dendrites still look wrong** (some other latent bug): inspect locally and, if
  the issue is deeper than the slice bug, document the residual issue in `results_detailed.md`
  and emit a follow-up suggestion rather than blocking the merge.

## Verification Criteria

* Both corrected PNGs exist in `results/images/` and show dendritic trees (visual
  confirmation).
* Both correction-overlay JSON files exist in `corrections/` and pass `verify_corrections.py
  t0100_fix_t0099_morph_charts`.
* `verify_task_file.py`, `verify_logs.py`, `verify_task_results.py`, `verify_task_metrics.py`,
  `verify_suggestions.py`, `verify_pr_premerge.py` all pass with 0 errors.

## Cross-References

* **t0099_random_init_pareto_robustness** — original task whose charts are being corrected.
* **t0091_morphology_extended_nsga2_v1** — first task using the joint 68-d vector with the
  `[54:]` morphology layout; reference for the correct slice convention.
* **t0098_visualise_pareto_morphologies** — sister visualisation task that read
  `cell["morphology_vector_14d"]` directly from JSON instead of slicing the 68-d vector and
  therefore was not affected by the bug.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0100_fix_t0099_morph_charts/results/results_summary.md)*

--- spec_version: "1" task_id: "t0100_fix_t0099_morph_charts" date_completed: "2026-05-11"
status: "complete" ---
# Results Summary: Fix t0099 Morphology Charts

## Summary

t0099's two morphology charts (`headline_best_cells.png`,
`cross_seed_top5_morphology_grid.png`) were broken because `build_morphology_charts.py:114`
used `vector_68d[:14]` (electrophys block) instead of `vector_68d[54:]` (morphology block)
when reconstructing each cell's morphology. The generator received nonsense parameters and
emitted zero dendrite sections, so the charts showed only giant filled circles. **Optimisation
results are unaffected** — every NSGA-II / evaluator / scorecard / anchor-classifier code path
uses the correct `[54:]` slice; the bug was isolated to the post-hoc visualisation script.
This task produces two corrected PNGs with proper dendritic trees in `results/images/`.

## Metrics

* **Files re-rendered**: 2 (`headline_best_cells.png` 4 panels;
  `cross_seed_top5_morphology_grid.png` 15 panels).
* **Cells visualised**: 19 total (1 t0091 reference + 3 seed-best + 15 seed-top-5).
* **Slice fix**: `vector_68d[:14]` -> `vector_68d[54:]` on a single line of
  `code/build_morphology_charts.py:114`.
* **Wall-clock**: ~5 s rendering; total task wall-clock ~20 min including framework
  scaffolding.
* **Total cost**: $0.
* **Files inside t0099 modified**: 0 (corrections via re-render in a separate task, per rule
  5).
* **Optimisation findings revised**: 0 — t0099's reported metrics, anchor distributions,
  joint-pass count, HV trajectories all remain valid.

## Verification

* `ruff check tasks/t0100_fix_t0099_morph_charts/code/` — PASSED (after line-length fix).
* `ruff format` — clean.
* `mypy -p tasks.t0100_fix_t0099_morph_charts.code` — PASSED (no issues).
* Visual inspection of both corrected PNGs by orchestrator — dendritic trees clearly visible
  in all 19 panels, soma radius correctly scaled relative to dendritic extent.
* `verify_task_file.py t0100_fix_t0099_morph_charts` — to run in reporting step.
* `verify_logs.py t0100_fix_t0099_morph_charts` — to run in reporting step.
* `verify_task_results.py t0100_fix_t0099_morph_charts` — to run in reporting step.
* `verify_task_metrics.py t0100_fix_t0099_morph_charts` — to run in reporting step.
* `verify_suggestions.py t0100_fix_t0099_morph_charts` — to run in reporting step.
* `verify_corrections.py t0100_fix_t0099_morph_charts` — to run in reporting step (empty
  folder; the corrections spec does not cover result images, so no overlay files are
  authored).
* `verify_pr_premerge.py t0100_fix_t0099_morph_charts --pr-number <N>` — to run in reporting
  step.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0100_fix_t0099_morph_charts/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0100_fix_t0099_morph_charts" date_completed: "2026-05-11"
status: "complete" ---
# Results Detailed: Fix t0099 Morphology Charts

## Summary

t0099's `code/build_morphology_charts.py` script had a single wrong slice that caused both of
its morphology visualisations to render only the soma as a giant filled circle, with no
dendritic structure visible. The cause was treating `vector_68d[:14]` as morphology when the
68-d parameter vector layout is `[54 electrophys, 14 morphology]` — the morphology block lives
at indices [54..68). This task copies the script, applies the one-character fix (`[:14]` ->
`[54:]`), re-renders the two affected PNGs into this task's own `results/images/`, and
documents the bug + fix. Optimisation results in t0099 are unaffected.

## Methodology

* **Workstation**: researcher's local Windows 11 Education box.
* **Compute**: local-only; no remote machines, no GPU, no paid services.
* **Wall-clock**: ~20 min total (~5 min actual code + render; ~15 min framework scaffolding).
* **Generator**:
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`
  (canonical via correction `C-0093-01`).
* **Inputs read** (unchanged from t0099):
  * `tasks/t0099_random_init_pareto_robustness/results/data/pareto_front_seed{11,22,33}.json`
  * `tasks/t0099_random_init_pareto_robustness/results/data/anchor_tracking_seed{11,22,33}.json`
  * `tasks/t0091_morphology_extended_nsga2_v1/results/data/pareto_front.json`
* **Diagnosis source**:
  * `tasks/t0091_morphology_extended_nsga2_v1/code/biological_priors.py:31`: `MORPH_OFFSET:
    int = 54`
  * `tasks/t0091_morphology_extended_nsga2_v1/code/anchor_tracking.py:160`: reads
    `vec_68d[54:]`
  * `tasks/t0091_morphology_extended_nsga2_v1/code/build_assets.py:68`:
    `cell.get("morphology_vector_14d") or list(cell.get("vector_68d", [])[54:])`
  * `tasks/t0099_random_init_pareto_robustness/code/generator_wrapper.py:55`:
    `vector_68d[:N_PARAMS_54], vector_68d[N_PARAMS_54:]` — optimisation code is CORRECT.
  * `tasks/t0099_random_init_pareto_robustness/code/nsga2_driver.py:303`:
    `"morphology_vector_14d": [float(v) for v in x_row[54:]]` — saved JSON is CORRECT.
  * `tasks/t0099_random_init_pareto_robustness/code/build_morphology_charts.py:114`:
    `tuple(vector_68d[:14])` — chart code was WRONG.

## Verification

| Verificator | Status | Notes |
| --- | --- | --- |
| `ruff check tasks/t0100_fix_t0099_morph_charts/code/` | PASSED | After one E501 line-length fix. |
| `ruff format` | clean |  |
| `mypy -p tasks.t0100_fix_t0099_morph_charts.code` | PASSED | No issues. |
| Visual inspection of `headline_best_cells.png` | PASSED | 4 panels: t0091 ref (black tree), seeds 11/22/33 (cyan/orange/olive). |
| Visual inspection of `cross_seed_top5_morphology_grid.png` | PASSED | 15 panels showing top-5 cells per seed; dendritic trees clearly visible. |
| `verify_task_file.py` | to run | reporting step. |
| `verify_logs.py` | to run | reporting step. |
| `verify_task_results.py` | to run | reporting step. |
| `verify_task_metrics.py` | to run | reporting step. |
| `verify_suggestions.py` | to run | reporting step. |
| `verify_corrections.py` | to run | reporting step (empty folder; no overlay authored). |
| `verify_pr_premerge.py` | to run | reporting step. |

## Limitations

* **Corrections spec does not cover result images**: the corrections specification v3 supports
  `suggestion`, `paper`, `answer`, `dataset`, `library`, `model`, `predictions` target kinds —
  not result PNGs. Therefore there is no formal aggregator-level redirect from t0099's broken
  PNGs to this task's corrected ones. Aggregators do not consume result images at all; the
  only consumer is the overview materializer for human review on GitHub. The original
  `task_description.md` proposed writing `corrections/file_replace_*.json` overlays; that
  approach turned out not to match the spec.
* **The broken PNGs remain in t0099/results/images/**: per rule 5 (completed task folders are
  immutable), they are not deleted. Anyone reviewing t0099 should be directed to t0100's
  `results/images/` for the corrected versions. This task's `task_description.md` and
  `results_summary.md` both make that pointer explicit.
* **The fix-up does not touch t0099's other 6 charts**: `biological_heatmap_seed*.png`,
  `pareto_overlay_*.png`, `hv_trajectory_cross_seed.png`, `anchor_distribution_heatmap.png`.
  Those charts do not invoke the morphology generator and are unaffected by the slice bug.
* **The bug exists only in t0099, not t0091/t0098**: t0091's chart code is unaffected (it uses
  `morphology_vector_14d` key directly from the saved JSON); t0098 likewise reads
  `morphology_vector_14d` directly. The bug was specific to t0099's chart script.

## Files Created

* `tasks/t0100_fix_t0099_morph_charts/code/__init__.py`
* `tasks/t0100_fix_t0099_morph_charts/code/build_morphology_charts.py` (one-character slice
  fix vs t0099 original)
* `tasks/t0100_fix_t0099_morph_charts/results/images/headline_best_cells.png` (corrected)
* `tasks/t0100_fix_t0099_morph_charts/results/images/cross_seed_top5_morphology_grid.png`
  (corrected)
* `tasks/t0100_fix_t0099_morph_charts/results/results_summary.md`
* `tasks/t0100_fix_t0099_morph_charts/results/results_detailed.md`
* `tasks/t0100_fix_t0099_morph_charts/results/metrics.json` (empty `{}`)
* `tasks/t0100_fix_t0099_morph_charts/results/costs.json` (zero)
* `tasks/t0100_fix_t0099_morph_charts/results/remote_machines_used.json` (empty array)
* `tasks/t0100_fix_t0099_morph_charts/results/suggestions.json` (empty array)
* `tasks/t0100_fix_t0099_morph_charts/logs/steps/00{1..15}_*/step_log.md` (per-step logs)
* `tasks/t0100_fix_t0099_morph_charts/logs/sessions/capture_report.json` (reporting step)

## Visualizations

### Corrected headline figure

![Corrected headline: t0091 warm-start joint-pass cell (black tree) vs t0099 random-init seeds
11/22/33; dendrite lines now
visible](../../../tasks/t0100_fix_t0099_morph_charts/results/images/headline_best_cells.png)

t0091's warm-start joint-pass cell (left panel, black) shows a roughly symmetric
Christmas-tree-like dendritic arbor. The 3 random-init seeds show sparse, asymmetric, often
degenerate morphologies — seed 11 has only a single short branch, seed 22 has a one-sided
field elongated to the right, seed 33 has a one-sided field elongated to the left. This
visually reinforces t0099's finding that the 5-anchor warm-start was load-bearing for reaching
the joint-pass corner of objective space: random initialisation collapses the morphology
generator to one-sided / sparse cells that cannot deliver the firing rate needed for
joint-pass.

### Corrected top-5 grid

![Corrected top-5 grid: 3 rows (seeds 11/22/33) x 5 cols (top-5 real cells); colors = nearest
t0091 anchor; full dendritic trees
visible](../../../tasks/t0100_fix_t0099_morph_charts/results/images/cross_seed_top5_morphology_grid.png)

15 cells across 3 seeds show genuine morphological diversity. Most cells are pd_asymmetric
(red) or alt_topology (purple); a few bedb_like (blue) and nd_asymmetric (green) cells appear.
The symmetric anchor (gray) is absent from all panels, consistent with t0099's finding that
the symmetric warm-start anchor was dominated and removed during gen 1+2 selection across
every seed.

## Task Requirement Coverage

The task's operative text (from `tasks/t0100_fix_t0099_morph_charts/task.json`):

> **Name**: "Re-render t0099 morphology charts with correct 68-d slice"
> 
> **short_description**: "Fix t0099 morphology-chart rendering: `vector_68d[:14]` was wrong
> (electrophys); replace with `vector_68d[54:]` (morphology). Re-render 2 PNGs. Optimisation
> unaffected."

The task_description.md plan items and how each was met:

| Plan item | Status | Evidence |
| --- | --- | --- |
| Copy + fix `build_morphology_charts.py` (1-char slice fix) | Done | `code/build_morphology_charts.py:128` uses `vector_68d[MORPH_OFFSET:]` with `MORPH_OFFSET = 54`; ruff + mypy clean. |
| Re-render 2 corrected PNGs in `results/images/` | Done | Both PNGs present and visually verified to show dendritic trees. |
| Confirm dendrite line segments visible, soma circles correctly scaled | Done | See Visualizations section above. |
| Write 2 correction-overlay JSON files | Not done (out-of-scope reclassification) | The corrections spec v3 does not cover result images. Documented as a Limitation. |
| Write results files (summary, detailed, metrics, costs, machines, suggestions) | Done | All 6 files present in `results/`. |
| Verificators pass | In progress | Pre-reporting verificators (ruff, mypy, visual) PASSED. Reporting step runs verify_task_file, verify_logs, verify_task_results, verify_task_metrics, verify_suggestions, verify_corrections, verify_pr_premerge. |
| Confirm optimisation results in t0099 are unaffected | Done | All NSGA-II / evaluator / scorecard / anchor-classifier code paths verified to use `[54:]`; only the post-hoc chart script was buggy. t0099's reported metrics, anchor distributions, and 0-of-55 joint-pass finding all remain valid. |

</details>
