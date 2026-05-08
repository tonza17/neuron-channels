# Visualise t0091 Pareto Morphologies + Per-Cell DSI / PD-Rate Charts

## Motivation

t0091 (`morphology_extended_nsga2_v1`) produced a 57-cell Pareto front from joint 68-d NSGA-II (54-d
v3 electrophys + 14-d morphology) on Bed B. The headline numerical findings (mean DSI 0.221 across
the Pareto, 1 strict joint-pass cell at DSI=0.51, 0 biologically-plausible joint-pass cells, anchor
distribution 20/0/12/9/16) are documented in t0091 results. What is **missing** is a direct visual
look at the morphologies the optimiser actually produced. The 14-d procedural generator is hard to
reason about from numerical bounds alone — without seeing the cells, we cannot judge whether the
alt_topology basin (16 Pareto cells) genuinely differs from the bedb_like basin (20 Pareto cells),
why the symmetric anchor was completely abandoned, or what the strict joint-pass cell looks like
geometrically. This task addresses that gap with a reproducible visualisation script and four
charts.

## Scope

### In Scope

* Load the 57-cell Pareto archive from t0091 (`results/data/pareto_front.json`,
  `results/data/anchor_tracking.json`).

* Regenerate each cell's 14-d morphology via the canonical patched generator
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`
  (canonicalised by `C-0093-01`).

* Produce four charts and save to `results/images/`:

  1. `morphology_grid_57cells.png` — 8×8 grid of 2D top-down dendrograms, sorted by DSI
     descending, colored by anchor (bedb_like blue, symmetric gray, pd_asymmetric red, nd_asymmetric
     green, alt_topology purple), annotated per-panel with DSI / PD-rate / anchor name.
  2. `pareto_dsi_bar.png` — sorted bar chart of DSI per Pareto cell, colored by anchor, with
     horizontal dashed line at DSI=0.5 (strict joint-pass threshold).
  3. `pareto_pd_bar.png` — sorted bar chart of PD firing rate per Pareto cell, colored by anchor,
     with horizontal dashed line at PD=30 Hz (strict joint-pass threshold).
  4. `pareto_dsi_vs_pd_scatter.png` — scatter plot of (DSI, PD-rate). Colored by anchor. Strict
     joint-pass cell (DSI≥0.5, PD≥30 Hz, robust≥0.7) marked with a black star.

* Embed all four charts in `results_detailed.md` with a 1–3-sentence takeaway each.

### Out of Scope

* No simulation of the cells (no NEURON `h.run()`); only the morphology data structure is built for
  plotting coordinates.
* No new biology, no new optimisation, no new metrics.
* No changes to t0091 (immutable per ARF rules; would need a correction otherwise).
* No 3D visualisation; the procedural generator emits cells in a 2D plane.
* No clustering or PCA — those belong to S-0091-04 / S-0091-07 follow-ups.

## Approach

### Reference implementation

A working reference script already exists at
`C:/Users/md1avn/AppData/Local/Temp/t0091_charts/build_charts.py` (built during the post-t0091
visualisation request) and produces all four charts in 4.5 s on the local 64-core EPYC. It includes:

* DLL-loader monkey-patch: `t0090._get_neuron_h` calls `ensure_t80_dll_loaded`, which fails when
  t0080's compiled `nrnmech.dll` is not present. The script monkey-patches `ensure_t80_dll_loaded`
  to a no-op in both modules before importing the generator. This is necessary because we only need
  section endpoint coordinates, not channel-inserted simulation.
* AIS rendering: `MorphologyResult.section_endpoints_xy` does not include AIS sections (t0090's
  generator creates AIS in NEURON but does not register their xy endpoints in the dict). The grid
  panels render soma + dendrites only.
* Anchor lookup: `pareto_front.json` does not carry an `anchor` field directly; the script joins
  with `anchor_tracking.json` on `cell_id` to retrieve `nearest_anchor_name`.

This task formalises that script under `tasks/t0098_..code/` with proper `paths.py` + `constants.py`
and re-runs it to land charts in the task folder.

### Step by Step

1. Create `code/paths.py` with all `pathlib.Path` constants for inputs and outputs.
2. Create `code/constants.py` with the 14 morphology knob names + ranges, anchor color map, chart
   figsize / dpi / threshold constants.
3. Create `code/build_charts.py` that: a. Loads `pareto_front.json` and `anchor_tracking.json` from
   t0091's results folder. b. Joins the two JSONs on cell_id to attach `nearest_anchor_name` to each
   Pareto cell. c. Sorts cells by DSI descending. d. Monkey-patches `ensure_t80_dll_loaded` to no-op
   in t0090 and t0092 modules. e. Calls `generate_fixed_morphology(params=..., morph_seed=...)` for
   each cell to extract `MorphologyResult.section_endpoints_xy`. f. Renders the 8×8 morphology grid
   with matplotlib `LineCollection` for performance. g. Renders the three metric charts. h. Saves
   all four PNGs to `results/images/`.
4. Run the script via
   `uv run python -u -m tasks.t0098_visualise_pareto_morphologies.code.build_charts`.
5. Compute metrics for results_detailed: count of cells per anchor (recompute from the joined data
   as a cross-check against t0091's anchor_tracking.json).
6. Verify all four PNG files exist and are non-empty.

## Pass Criteria

* All four PNGs generated and embedded in `results_detailed.md`.
* Anchor distribution recomputed and matches t0091's `anchor_tracking.json` exactly (20 / 0 / 12 / 9
  / 16).
* Strict joint-pass cell (DSI=0.51, PD=35 Hz, robust=0.79) clearly identifiable in
  `pareto_dsi_vs_pd_scatter.png` (black star) and in the top-left panel of
  `morphology_grid_57cells.png` (since it is sorted by DSI descending).
* Script runs end-to-end on local machine in under 60 seconds.

## Compute and Budget

* Local CPU only (64-core EPYC). No remote compute.
* No paid services. No API calls.
* **Estimated cost: $0.00.**

## Time Estimation

* Code writing: ~10 minutes (reference script already exists).
* Script execution: ~5 seconds.
* Verification + write-up: ~5 minutes.
* **Total wall-clock: ~15 minutes.**

## Expected Assets

None. Charts are deliverables under `results/images/` rather than registered asset types.
`expected_assets = {}`.

## Risks and Fallbacks

* **t0090 generator's `ensure_t80_dll_loaded` may have changed behaviour in main.** The reference
  script monkey-patches it to no-op. If the patched generator changes the call site, update the
  monkey-patch target accordingly.
* **`section_endpoints_xy` may not be exposed.** Reference script confirmed the field exists in the
  current generator. If it goes away in a future change, fall back to manually walking the
  generator's section list.
* **Matplotlib font availability on Windows.** Use the default `font.family` (DejaVu Sans is bundled
  with matplotlib).

## Verification Criteria

* `verify_research_code.py`, `verify_plan.py`, `verify_logs.py`, `verify_task_file.py`,
  `verify_task_folder.py`, `verify_task_results.py`, `verify_task_metrics.py` (with empty
  metrics.json) pass with 0 errors.
* All four PNG files exist in `results/images/` and have valid PNG headers + non-zero size.
* `results_detailed.md` embeds all four charts with `![desc](images/file.png)` syntax.

## Cross-References

* **t0091_morphology_extended_nsga2_v1** — data source: 57-cell Pareto archive,
  anchor_tracking.json, all_evaluations.json.
* **t0092_diagnose_morphology_generator_silence** — canonical generator
  `generate_fixed_morphology` (via correction `C-0093-01`).
* **t0093_resweep_and_t0090_correction** — issued `C-0093-01` redirecting the canonical procedural
  DSGC morphology generator to the t0092 fix.
* Source suggestions: none directly. Covers part of S-0091-04 (alt_topology basin deep-dive needs
  morphology visualisation as a foundation) and part of S-0091-07 (PCA / feature-importance also
  benefits from visual cross-checks of the per-cell morphology data).
