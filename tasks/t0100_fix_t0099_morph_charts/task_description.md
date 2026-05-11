# Re-render t0099 Morphology Charts with Correct 68-d Slice

## Motivation

t0099 (`random_init_pareto_robustness`) produced two morphology visualisations that show only the
soma as a large filled disc, with no dendritic tree visible:

* `results/images/headline_best_cells.png`
* `results/images/cross_seed_top5_morphology_grid.png`

The root cause is a wrong slice in
`tasks/t0099_random_init_pareto_robustness/code/build_morphology_charts.py:114`:

```python
morph_vec: tuple[float, ...] = tuple(vector_68d[:14])
```

The 68-d parameter vector layout is `[54 electrophys, 14 morphology]` (per
`tasks/t0091_morphology_extended_nsga2_v1/code/biological_priors.py:31`: `MORPH_OFFSET = 54`, and
`anchor_tracking.py:160`: `vec_68d[54:]`). Slicing `[:14]` picked the first 14 electrophys
parameters (Na/K conductance densities, AIS sizes, etc.) and passed them to the procedural
morphology generator as if they were `bf`, `mean_segment_length_um`, `branch_prob_per_um`, etc. The
generator received nonsense and emitted a cell with **0 dendrite sections** — only the soma
survives, hence the giant filled circle filling each panel.

The correct slice is `vector_68d[54:]` (or equivalently `vector_68d[54:68]`).

## Scope

### In Scope

* Re-render the two affected PNGs using a corrected copy of t0099's `build_morphology_charts.py`
  with `vector_68d[:14]` -> `vector_68d[54:]`.
* Write a correction overlay (`corrections/file_replace_t0099_morph_chart_grid.json` and
  `corrections/file_replace_t0099_morph_chart_headline.json`) that points downstream consumers
  (aggregators, overview materializer) to the corrected images in this task's `results/images/`.
* Verify the corrected images actually show dendritic trees (visual inspection by the researcher; no
  automated visual diff).

### Out of Scope

* Modifying any file inside `tasks/t0099_random_init_pareto_robustness/` (rule 5: completed task
  folders are immutable; corrections overlay handles this).
* Re-running the NSGA-II optimisation. Optimisation code uses the correct slice everywhere; the bug
  never touched the simulation loop. t0099's DSI / PD-rate / robustness / anchor distribution /
  0-of-55-joint-pass finding all remain valid.
* Re-rendering t0099's other 6 charts (`biological_heatmap_seed*.png`, `pareto_overlay_*.png`,
  `hv_trajectory_cross_seed.png`, `anchor_distribution_heatmap.png`) — those don't use the
  morphology generator at all.

## Approach

1. Copy the relevant rendering code from `t0099/code/build_morphology_charts.py` into
   `tasks/t0100_fix_t0099_morph_charts/code/build_morphology_charts.py` (cross-task code copy per
   CLAUDE.md rule: libraries are the only shared mechanism; non-library code must be copied).
2. Apply the single fix: `vector_68d[:14]` -> `vector_68d[54:]` on the only affected line.
3. Run the script locally; it reads from t0099's `results/data/pareto_front_seed{11,22,33}.json`
   + `anchor_tracking_seed{11,22,33}.json` and `t0091/results/data/pareto_front.json` +
     `anchor_tracking.json` (all already on main); writes the two re-rendered PNGs into this task's
     `results/images/`.
4. Visual confirmation: dendrite line segments now visible, soma circles correctly scaled.
5. Write two correction-overlay JSON files under `corrections/` declaring file replacement: t0099's
   `results/images/headline_best_cells.png` -> t0100's `results/images/headline_best_cells.png`;
   same for the cross-seed grid.
6. Run standard task verificators; commit; PR; merge.

## Cost Estimation

* **Total**: $0
* **Compute**: local only (matplotlib + procedural morphology generator; ~10 s wall-clock for 19
  cells across both figures)
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

* No assets in the asset-type sense (no paper / dataset / library / answer / model / predictions).
  The deliverables are 2 corrected PNGs and 2 correction-overlay JSON files.

## Time Estimation

~30 minutes wall-clock: ~5 min code copy + fix + render, ~25 min task scaffolding + verificators +
PR + merge.

## Risks & Fallbacks

* **Re-render fails because t0099's data files are not on main**: confirm `pareto_front_*.json` and
  `anchor_tracking_*.json` are present before starting; abort if missing. (Verified present at start
  of task.)
* **Correction-overlay JSON schema is unfamiliar**: read
  `arf/specifications/corrections_specification.md` before writing; mirror the file-replacement
  pattern from t0093's library correction overlay (`C-0093-01`).
* **The rendered dendrites still look wrong** (some other latent bug): inspect locally and, if the
  issue is deeper than the slice bug, document the residual issue in `results_detailed.md` and emit
  a follow-up suggestion rather than blocking the merge.

## Verification Criteria

* Both corrected PNGs exist in `results/images/` and show dendritic trees (visual confirmation).
* Both correction-overlay JSON files exist in `corrections/` and pass
  `verify_corrections.py t0100_fix_t0099_morph_charts`.
* `verify_task_file.py`, `verify_logs.py`, `verify_task_results.py`, `verify_task_metrics.py`,
  `verify_suggestions.py`, `verify_pr_premerge.py` all pass with 0 errors.

## Cross-References

* **t0099_random_init_pareto_robustness** — original task whose charts are being corrected.
* **t0091_morphology_extended_nsga2_v1** — first task using the joint 68-d vector with the `[54:]`
  morphology layout; reference for the correct slice convention.
* **t0098_visualise_pareto_morphologies** — sister visualisation task that read
  `cell["morphology_vector_14d"]` directly from JSON instead of slicing the 68-d vector and
  therefore was not affected by the bug.
