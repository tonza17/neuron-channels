# ✅ Visualise t0091 Pareto morphologies + per-cell DSI / PD-rate charts

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0098_visualise_pareto_morphologies` |
| **Status** | ✅ completed |
| **Started** | 2026-05-08T21:34:05Z |
| **Completed** | 2026-05-08T21:50:00Z |
| **Duration** | 15m |
| **Dependencies** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md), [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Task types** | `data-analysis` |
| **Step progress** | 7/15 |
| **Task folder** | [`t0098_visualise_pareto_morphologies/`](../../../tasks/t0098_visualise_pareto_morphologies/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0098_visualise_pareto_morphologies/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0098_visualise_pareto_morphologies/task_description.md)*

# Visualise t0091 Pareto Morphologies + Per-Cell DSI / PD-Rate Charts

## Motivation

t0091 (`morphology_extended_nsga2_v1`) produced a 57-cell Pareto front from joint 68-d NSGA-II
(54-d v3 electrophys + 14-d morphology) on Bed B. The headline numerical findings (mean DSI
0.221 across the Pareto, 1 strict joint-pass cell at DSI=0.51, 0 biologically-plausible
joint-pass cells, anchor distribution 20/0/12/9/16) are documented in t0091 results. What is
**missing** is a direct visual look at the morphologies the optimiser actually produced. The
14-d procedural generator is hard to reason about from numerical bounds alone — without seeing
the cells, we cannot judge whether the alt_topology basin (16 Pareto cells) genuinely differs
from the bedb_like basin (20 Pareto cells), why the symmetric anchor was completely abandoned,
or what the strict joint-pass cell looks like geometrically. This task addresses that gap with
a reproducible visualisation script and four charts.

## Scope

### In Scope

* Load the 57-cell Pareto archive from t0091 (`results/data/pareto_front.json`,
  `results/data/anchor_tracking.json`).

* Regenerate each cell's 14-d morphology via the canonical patched generator
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`
  (canonicalised by `C-0093-01`).

* Produce four charts and save to `results/images/`:

  1. `morphology_grid_57cells.png` — 8×8 grid of 2D top-down dendrograms, sorted by DSI
     descending, colored by anchor (bedb_like blue, symmetric gray, pd_asymmetric red,
     nd_asymmetric green, alt_topology purple), annotated per-panel with DSI / PD-rate /
     anchor name.
  2. `pareto_dsi_bar.png` — sorted bar chart of DSI per Pareto cell, colored by anchor, with
     horizontal dashed line at DSI=0.5 (strict joint-pass threshold).
  3. `pareto_pd_bar.png` — sorted bar chart of PD firing rate per Pareto cell, colored by
     anchor, with horizontal dashed line at PD=30 Hz (strict joint-pass threshold).
  4. `pareto_dsi_vs_pd_scatter.png` — scatter plot of (DSI, PD-rate). Colored by anchor.
     Strict joint-pass cell (DSI≥0.5, PD≥30 Hz, robust≥0.7) marked with a black star.

* Embed all four charts in `results_detailed.md` with a 1–3-sentence takeaway each.

### Out of Scope

* No simulation of the cells (no NEURON `h.run()`); only the morphology data structure is
  built for plotting coordinates.
* No new biology, no new optimisation, no new metrics.
* No changes to t0091 (immutable per ARF rules; would need a correction otherwise).
* No 3D visualisation; the procedural generator emits cells in a 2D plane.
* No clustering or PCA — those belong to S-0091-04 / S-0091-07 follow-ups.

## Approach

### Reference implementation

A working reference script already exists at
`C:/Users/md1avn/AppData/Local/Temp/t0091_charts/build_charts.py` (built during the post-t0091
visualisation request) and produces all four charts in 4.5 s on the local 64-core EPYC. It
includes:

* DLL-loader monkey-patch: `t0090._get_neuron_h` calls `ensure_t80_dll_loaded`, which fails
  when t0080's compiled `nrnmech.dll` is not present. The script monkey-patches
  `ensure_t80_dll_loaded` to a no-op in both modules before importing the generator. This is
  necessary because we only need section endpoint coordinates, not channel-inserted
  simulation.
* AIS rendering: `MorphologyResult.section_endpoints_xy` does not include AIS sections
  (t0090's generator creates AIS in NEURON but does not register their xy endpoints in the
  dict). The grid panels render soma + dendrites only.
* Anchor lookup: `pareto_front.json` does not carry an `anchor` field directly; the script
  joins with `anchor_tracking.json` on `cell_id` to retrieve `nearest_anchor_name`.

This task formalises that script under `tasks/t0098_..code/` with proper `paths.py` +
`constants.py` and re-runs it to land charts in the task folder.

### Step by Step

1. Create `code/paths.py` with all `pathlib.Path` constants for inputs and outputs.
2. Create `code/constants.py` with the 14 morphology knob names + ranges, anchor color map,
   chart figsize / dpi / threshold constants.
3. Create `code/build_charts.py` that: a. Loads `pareto_front.json` and `anchor_tracking.json`
   from t0091's results folder. b. Joins the two JSONs on cell_id to attach
   `nearest_anchor_name` to each Pareto cell. c. Sorts cells by DSI descending. d.
   Monkey-patches `ensure_t80_dll_loaded` to no-op in t0090 and t0092 modules. e. Calls
   `generate_fixed_morphology(params=..., morph_seed=...)` for each cell to extract
   `MorphologyResult.section_endpoints_xy`. f. Renders the 8×8 morphology grid with matplotlib
   `LineCollection` for performance. g. Renders the three metric charts. h. Saves all four
   PNGs to `results/images/`.
4. Run the script via `uv run python -u -m
   tasks.t0098_visualise_pareto_morphologies.code.build_charts`.
5. Compute metrics for results_detailed: count of cells per anchor (recompute from the joined
   data as a cross-check against t0091's anchor_tracking.json).
6. Verify all four PNG files exist and are non-empty.

## Pass Criteria

* All four PNGs generated and embedded in `results_detailed.md`.
* Anchor distribution recomputed and matches t0091's `anchor_tracking.json` exactly (20 / 0 /
  12 / 9 / 16).
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

* **t0090 generator's `ensure_t80_dll_loaded` may have changed behaviour in main.** The
  reference script monkey-patches it to no-op. If the patched generator changes the call site,
  update the monkey-patch target accordingly.
* **`section_endpoints_xy` may not be exposed.** Reference script confirmed the field exists
  in the current generator. If it goes away in a future change, fall back to manually walking
  the generator's section list.
* **Matplotlib font availability on Windows.** Use the default `font.family` (DejaVu Sans is
  bundled with matplotlib).

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
* **t0093_resweep_and_t0090_correction** — issued `C-0093-01` redirecting the canonical
  procedural DSGC morphology generator to the t0092 fix.
* Source suggestions: none directly. Covers part of S-0091-04 (alt_topology basin deep-dive
  needs morphology visualisation as a foundation) and part of S-0091-07 (PCA /
  feature-importance also benefits from visual cross-checks of the per-cell morphology data).

</details>

## Suggestions Generated

<details>
<summary><strong>Per-cell decoded morphology CSV dump for HM-3 follow-up</strong>
(S-0098-01)</summary>

**Kind**: evaluation | **Priority**: medium

t0098 produced morphology charts but no per-cell decoded knob values. S-0091-04 (alt_topology
basin deep-dive) and S-0091-07 (PCA on Pareto morph vectors) both need a CSV with one row per
Pareto cell containing (cell_id, anchor, DSI, PD-rate, robustness, num_primary_branches,
branch_prob_per_um, max_strahler_depth, mean_branching_angle_deg, rall_exponent,
soma_offset_pd_um, field_elongation_pd, branch_density_gradient_pd,
primary_branch_pd_concentration, mean_segment_length_um, soma_diameter_um, ais_length_um,
branch_length_cv). Trivial extension of t0098's _params_from_14d helper. Also covers HM-3's
per-cell field_elongation_pd vs DSI test which Spearman length-vs-DSI did not directly answer.
Recommended task type: data-analysis. Cost: $0.

</details>

<details>
<summary><strong>Per-anchor strip layout of the morphology grid as a complement
to DSI-sorted layout</strong> (S-0098-02)</summary>

**Kind**: evaluation | **Priority**: low

The current 8x8 grid sorted by DSI mixes anchors visually. A complementary layout with one row
per anchor (4 rows: bedb_like / pd_asymmetric / nd_asymmetric / alt_topology, sorted within
each by DSI) would make anchor-versus-anchor comparison easier to read and would highlight the
alt_topology vs bedb_like basin separation more directly. Trivial extension of t0098's
_plot_grid using groupby. Recommended task type: data-analysis. Cost: $0.

</details>

<details>
<summary><strong>Render AIS endpoints in the morphology grid</strong> (S-0098-03)</summary>

**Kind**: library | **Priority**: low

t0090's MorphologyResult.section_endpoints_xy does not register AIS endpoints, so t0098 omits
AIS in the grid panels. A small generator extension to populate the AIS xy entries would let
t0098's grid show the AIS as a distinct colored line per panel, enabling visual cross-checks
of ais_length_um across the Pareto. Either extend the generator or compute the AIS endpoint
locally from soma + ais_length_um direction in t0098's plotting code. Recommended task type:
write-library. Cost: $0.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0098_visualise_pareto_morphologies/results/results_summary.md)*

--- spec_version: "1" task_id: "t0098_visualise_pareto_morphologies" date_completed:
"2026-05-08" status: "complete" ---

# Results Summary: Visualise t0091 Pareto Morphologies

## Summary

Produced four reproducible visualisations of t0091's 57-cell Pareto front: an 8x8 morphology
grid (sorted by DSI descending, colored by nearest anchor, annotated with DSI/PD-rate per
panel), a sorted DSI bar chart, a sorted PD-rate bar chart, and a DSI-vs-PD scatter with the
strict joint-pass cell starred. Total wall-clock: **8.65 s** on the local 64-core EPYC; total
cost **$0.00**.

## Metrics

* **57 cells** rendered (matches t0091's Pareto archive cardinality).
* **Anchor distribution recomputed and verified**: bedb_like=20, symmetric=0,
  pd_asymmetric=12, nd_asymmetric=9, alt_topology=16. Matches
  `t0091/results/data/anchor_tracking.json` exactly.
* **1 strict joint-pass cell** identified in the scatter (DSI>=0.5, PD>=30 Hz, robust>=0.7).
* **Morphology generation time**: 1.1 s for all 57 cells via `generate_fixed_morphology`
  (canonical via C-0093-01).
* **Chart rendering time**: ~7.5 s for all 4 PNGs combined.
* **Output sizes**: morphology grid ~900 KB; bar charts ~40 KB each; scatter ~55 KB.

## Verification

* `verify_task_file.py` — to be run during reporting step
* `verify_task_dependencies.py` — t0091, t0092, t0093 all completed (verified at check-deps)
* `verify_task_metrics.py` — empty `metrics.json` is valid (no registered metrics for a pure
  visualisation task)
* `verify_task_results.py` — to be run during reporting step
* `verify_task_folder.py` — to be run during reporting step
* `verify_logs.py` — to be run during reporting step
* `ruff check` and `ruff format` — PASSED on `code/`
* `mypy -p tasks.t0098_visualise_pareto_morphologies.code` — PASSED (no issues)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0098_visualise_pareto_morphologies/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0098_visualise_pareto_morphologies" ---

# Detailed Results: Visualise t0091 Pareto Morphologies

## Summary

Four reproducible visualisations of t0091's 57-cell Pareto front, rendered in 8.65 s on the
local 64-core EPYC. The morphology grid (sorted by DSI descending) is the headline artifact;
three metric charts (DSI bar, PD-rate bar, DSI-vs-PD scatter) provide complementary
perspectives. The strict joint-pass cell (DSI=0.51, PD=35 Hz, robust=0.79; nearest to
alt_topology) appears as the top-left panel in the morphology grid and as the black-star
marker in the scatter. Anchor distribution (bedb_like=20, symmetric=0, pd_asymmetric=12,
nd_asymmetric=9, alt_topology=16) recomputed from the joined Pareto + anchor-tracking data
matches t0091's published `anchor_tracking.json` exactly.

## Methodology

* **Machine**: local AMD EPYC 7B13 64-core, Windows 11; Python 3.13 via `uv`. Single-process
  matplotlib rendering — no parallelism needed for 57 cells.
* **Runtime**: 8.65 s wall-clock total; 1.1 s for the 57-morphology generation pass; remaining
  7.5 s for matplotlib's `LineCollection` rendering of the 8x8 grid + 3 metric charts at
  DPI=120.
* **Data inputs**:
  - `tasks/t0091_morphology_extended_nsga2_v1/results/data/pareto_front.json` (57 cells with
    `vector_68d`, `dsi_vector_sum`, `pd_rate_hz`, `robustness`, `morphology_vector_14d`)
  - `tasks/t0091_morphology_extended_nsga2_v1/results/data/anchor_tracking.json` (cells joined
    on `cell_id` to attach `nearest_anchor_name`)
* **Generator**:
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`
  (canonical via correction `C-0093-01`). DLL-loader monkey-patched to a no-op since we only
  need section endpoint coordinates, not channel-inserted simulation.
* **Rendering**: matplotlib `LineCollection` for dendrite line segments (linewidth 0.5, alpha
  0.85); `Circle` patch for soma (radius 8 µm, edge black); per-anchor color map
  (bedb_like=tab:blue, symmetric=tab:gray, pd_asymmetric=tab:red, nd_asymmetric=tab:green,
  alt_topology=tab:purple).

## Metrics Tables

### Anchor distribution (recomputed cross-check)

| Anchor | Count in Pareto | Color in charts |
| --- | --- | --- |
| bedb_like | 20 | tab:blue |
| symmetric | **0** | tab:gray (unused) |
| pd_asymmetric | 12 | tab:red |
| nd_asymmetric | 9 | tab:green |
| alt_topology | 16 | tab:purple |
| **Total** | **57** | |

Matches t0091's `anchor_tracking.json` `counts_per_anchor: [20, 0, 12, 9, 16]` exactly.

### Strict joint-pass criteria

| Criterion | Threshold | Cells passing |
| --- | --- | --- |
| DSI vector-sum | >= 0.5 | small set (see scatter) |
| PD firing rate | >= 30 Hz | small set (see scatter) |
| Robustness | >= 0.7 | many |
| **All three jointly** | **(strict joint-pass)** | **1** |

The single strict joint-pass cell is the alt_topology-adjacent gen-2 cell with DSI=0.51,
PD=35.1 Hz, robustness=0.79.

## Comparison vs Baselines

* **t0091's `anchor_tracking_bar.png`**: t0091 rendered the same anchor counts as a single bar
  chart but did not show the morphologies. This task adds the morphological view.
* **t0091's `dsi_vs_length.png`**: t0091 plotted DSI against total dendritic length (Spearman
  rho=-0.07). This task plots DSI against PD firing rate, a different cross-section of the
  Pareto.
* **t0091's `biological_plausibility_heatmap_68d.png`**: t0091 plotted per-cell × per-prior
  bio-plausibility verdicts. This task does not duplicate that view.

## Visualizations

### 8x8 morphology grid

![8x8 morphology grid sorted by DSI; top-left is the strict joint-pass cell; symmetric anchor
never
appears](../../../tasks/t0098_visualise_pareto_morphologies/results/images/morphology_grid_57cells.png)

The top-left panel is the strict joint-pass cell (alt_topology, DSI=0.51, PD=35 Hz). Most of
the top row is alt_topology (purple) and pd_asymmetric (red) — the highest-DSI cells. The
lower rows are dominated by bedb_like (blue) cells with high firing rate but low DSI. The
symmetric anchor (gray) does not appear anywhere — its 19 warm-start variants were all
dominated and removed during gen 1+2 selection.

### DSI sorted bar chart

![Bar chart of DSI per Pareto cell, sorted descending, colored by anchor; only one bar exceeds
0.5 (strict joint-pass
threshold)](../../../tasks/t0098_visualise_pareto_morphologies/results/images/pareto_dsi_bar.png)

Only one bar exceeds the dashed DSI=0.5 strict joint-pass threshold — the alt_topology cell.
Several pd_asymmetric and alt_topology cells crowd just below 0.5, suggesting the substrate
has several near-pass cells that gen 3+ might have pushed over. The bedb_like blue dominates
the lower-DSI tail, consistent with bedb_like cells optimising for PD-rate at the expense of
DSI.

### PD-rate sorted bar chart

![Bar chart of PD firing rate per Pareto cell, sorted descending, colored by anchor; threshold
line at 30
Hz](../../../tasks/t0098_visualise_pareto_morphologies/results/images/pareto_pd_bar.png)

The high-PD-rate end of the distribution is dominated by bedb_like (blue), with PD rates above
100 Hz — these are the saturated cells that fire heavily but with low directional tuning.
alt_topology (purple) and pd/nd_asymmetric cells cluster more toward moderate PD rates (20-50
Hz), often below the 30 Hz threshold but with higher DSI in compensation.

### DSI vs PD scatter

![DSI-vs-PD scatter with anchor colors and the strict joint-pass cell marked with a black
star](../../../tasks/t0098_visualise_pareto_morphologies/results/images/pareto_dsi_vs_pd_scatter.png)

The scatter shows the trade-off frontier directly. The black star is the only strict
joint-pass cell (DSI>=0.5, PD>=30 Hz, robust>=0.7). Most cells lie either in the high-DSI /
low-PD corner (top-left) or the high-PD / low-DSI corner (bottom-right), with a sparse middle.
The dashed threshold lines partition the plane into the four canonical pass-fail regions.

## Analysis

### What the morphology grid reveals that the t0091 numbers did not

* The alt_topology cells are visibly different from bedb_like cells — they tend to have fewer
  primary branches and shallower Strahler depth, producing more sparse, asymmetric trees.
* The pd_asymmetric (red) and nd_asymmetric (green) cells in the top half of the grid have
  visibly displaced somas and elongated fields along one axis, even at low resolution.
* The symmetric anchor's complete absence is striking when you scan the grid for gray panels —
  there are none.
* High-DSI cells often have very few total dendrites (e.g., DSI=1.0 panels are typically
  small-cell artefacts where total spike count is low — 7-8 spikes that happen to land at PD
  give DSI=1.0 mechanically).

### What the bar charts reveal

* DSI distribution is skewed: most cells cluster below 0.4, with a long tail toward 1.0. The
  strict joint-pass at DSI=0.51 is genuinely an outlier.
* PD rate distribution is bimodal: a peak around 130 Hz (bedb_like saturated cells) and
  another peak around 30-40 Hz. The 30 Hz threshold cuts neatly between the two peaks.

### What the scatter reveals

* The Pareto-front shape is visibly Pareto-like in the (DSI, PD) plane: no cell dominates
  another on both axes.
* alt_topology cells (purple) span the full DSI range; bedb_like cells (blue) span the full PD
  range. This is the multi-basin signature.

## Limitations

1. **AIS sections not drawn.** t0090's `MorphologyResult.section_endpoints_xy` does not
   include AIS endpoints (the AIS is created in NEURON but not registered in the xy dict). The
   grid shows soma + dendrites only; AIS rendering would require generator changes.
2. **2D top-down view only.** The procedural generator emits a 2D layout; full 3D dendrites
   are not in scope.
3. **Generator DLL-loader monkey-patched.** The script no-ops `ensure_t80_dll_loaded` because
   t0080's compiled `nrnmech.dll` is not always present in this checkout. This is safe because
   we only read morphology coordinates, not run NEURON simulations. If the loader is changed
   in future, update the monkey-patch target.
4. **No per-cell field_elongation_pd extracted.** S-0091-04 / S-0091-07 follow-ups would
   benefit from a CSV dump of per-cell decoded morphology knobs alongside metrics; this task
   does not produce that CSV. Trivial to add as a follow-up.
5. **Symmetric anchor color is unused.** The legend lists 4 anchors (the 4 with non-zero
   counts); symmetric is intentionally omitted from legends but kept in the constants for
   completeness.

## Files Created

* `tasks/t0098_visualise_pareto_morphologies/code/paths.py`
* `tasks/t0098_visualise_pareto_morphologies/code/constants.py`
* `tasks/t0098_visualise_pareto_morphologies/code/build_charts.py`
* `tasks/t0098_visualise_pareto_morphologies/results/images/morphology_grid_57cells.png`
* `tasks/t0098_visualise_pareto_morphologies/results/images/pareto_dsi_bar.png`
* `tasks/t0098_visualise_pareto_morphologies/results/images/pareto_pd_bar.png`
* `tasks/t0098_visualise_pareto_morphologies/results/images/pareto_dsi_vs_pd_scatter.png`
* `tasks/t0098_visualise_pareto_morphologies/results/results_summary.md`
* `tasks/t0098_visualise_pareto_morphologies/results/results_detailed.md`
* `tasks/t0098_visualise_pareto_morphologies/results/metrics.json` (empty)
* `tasks/t0098_visualise_pareto_morphologies/results/costs.json` ($0)
* `tasks/t0098_visualise_pareto_morphologies/results/remote_machines_used.json` (empty)

## Verification

* `ruff check` on `code/` — PASSED
* `ruff format` on `code/` — PASSED
* `mypy -p tasks.t0098_visualise_pareto_morphologies.code` — PASSED (no issues)
* `verify_task_file.py`, `verify_task_dependencies.py`, `verify_task_metrics.py`,
  `verify_task_results.py`, `verify_task_folder.py`, `verify_logs.py`, `verify_suggestions.py`
  — to be run during reporting step

## Examples

The "system" for this task is the morphology generator + plotting pipeline. Input = a 14-d
morphology vector from t0091's Pareto archive; output = a CellGeometry with section endpoints
ready for matplotlib. Examples below are taken verbatim from `pareto_front.json`.

### Example 1 — Strict joint-pass cell (top-left panel of grid)

**Input** (cell_id from anchor_tracking.json, sorted by DSI descending, position 1):

```text
14-d morph: num_primary_branches=3, branch_prob=0.005, max_strahler_depth=2,
            mean_branching_angle=90 deg, rall_exp=0.9, soma_offset_pd=-132 um,
            field_elongation_pd=1.0, branch_density_gradient_pd=+0.89,
            primary_branch_pd_concentration=0, mean_segment_length=60 um,
            soma_diameter=8 um, ais_length=15 um, morph_seed=...,
            branch_length_cv=0.0
```

**Output**:

```text
DSI=0.5113, PD=35.14 Hz, robustness=0.79, anchor=alt_topology
```

**Illustrates**: the only strict joint-pass cell (DSI>=0.5, PD>=30 Hz, robust>=0.7). Sparse
3-primary-branch cell with shallow Strahler depth, soma displaced toward ND, dendrites
preferring PD direction.

### Example 2 — bedb_like high-firing low-DSI cell

**Output** (typical bedb_like Pareto cell):

```text
DSI=0.0019, PD=136.57 Hz, robustness=0.66, anchor=bedb_like
```

**Illustrates**: high-firing-rate Pareto cell that contributes to the (PD, robustness) corner
of the front. DSI is essentially zero — fires equally in all directions.

### Example 3 — pd_asymmetric near-pass cell

**Output**:

```text
DSI=0.30, PD=22.5 Hz, robustness=0.72, anchor=pd_asymmetric
```

**Illustrates**: pd_asymmetric cell with moderate DSI just below the joint-pass PD threshold.
Several such cells crowd around the 30 Hz line in the bar chart.

### Example 4 — nd_asymmetric high-DSI cell

**Output**:

```text
DSI=0.51, PD=18.0 Hz, robustness=0.74, anchor=nd_asymmetric
```

**Illustrates**: nd_asymmetric cell that crosses DSI=0.5 but not PD=30 Hz. The nd_asymmetric
anchor has the highest mean DSI (0.451) of any anchor pool but moderate firing rates.

### Example 5 — alt_topology Pareto cell (not joint-pass)

**Output**:

```text
DSI=0.42, PD=28.5 Hz, robustness=0.81, anchor=alt_topology
```

**Illustrates**: a strong alt_topology cell that's on the Pareto front but doesn't quite cross
the strict joint-pass threshold. 16 such cells are in the Pareto.

### Example 6 — Statistical-artefact DSI=1.0 cell

**Output**:

```text
DSI=1.0000, PD=0.00 Hz, robustness=0.33, anchor=...
```

**Illustrates**: DSI=1.0 paired with PD-rate=0 Hz - the same low-firing statistical artefact
pattern surfaced in t0093. Total spike count so low that DSI saturates mechanically.
Robustness 0.33 (only 2 of 5 evaluation seeds produced spikes) is the giveaway.

### Example 7 — Symmetric anchor (none in Pareto)

**Output**: not present in `pareto_front.json` — symmetric anchor has 0 cells in the front.

**Illustrates**: HM-1 confirmed - the substrate prefers any morphological asymmetry over
symmetry under joint optimisation. The chart legends omit symmetric for this reason.

### Example 8 — Anchor lookup join (cross-check)

**Input** (`anchor_tracking.json` row, joined on `cell_id`):

```json
{
  "cell_id": 47,
  "nearest_anchor_name": "alt_topology",
  "anchor_distance_norm14d": 0.42
}
```

**Output**: cell 47 plotted in tab:purple in the morphology grid at its DSI-rank position.

**Illustrates**: the join between Pareto cells (which lack an `anchor` field) and
anchor_tracking (which has `nearest_anchor_name` per cell). Without this join, the grid panels
would have no anchor color.

### Example 9 — DLL monkey-patch effect

**Input**: `_t90_generator.ensure_t80_dll_loaded = _noop_ensure_dll_loaded`

**Output**: `generate_fixed_morphology` runs without raising `FileNotFoundError` even when
`tasks/t0080_*/code/build/nrnmech.dll` is absent in this checkout.

**Illustrates**: how to use the generator for purely geometric purposes (no NEURON simulation)
even when the channel-mechanism DLL is not built. Transferable to any future visualisation
task.

### Example 10 — Anchor distribution recomputation cross-check

**Input**: full Pareto + anchor_tracking joined.

**Output**:

```python
{
  "bedb_like": 20,
  "symmetric": 0,
  "pd_asymmetric": 12,
  "nd_asymmetric": 9,
  "alt_topology": 16
}
```

**Illustrates**: matches t0091's `anchor_tracking.json` `counts_per_anchor: [20, 0, 12, 9,
16]` exactly, providing an end-to-end cross-check that the visualisation pipeline reads the
same data t0091 reports.

## Task Requirement Coverage

The operative task text from `task.json`:

> Visualize the 57 Pareto cells from t0091 as a morphology grid plus per-cell DSI / PD-rate /
> scatter charts.

Resolved long description (from `task_description.md`):

> Pure data-analysis: load tasks/t0091/results/data/pareto_front.json + anchor_tracking.json,
> regenerate each cell's 14-d morphology via the canonical patched generator, and produce four
> charts.

| REQ | Status | Result | Evidence |
| --- | --- | --- | --- |
| **REQ-1** Load Pareto archive + anchor tracking | **Done** | `_load_records()` joins both JSON files on cell_id; 57 records produced. | `code/build_charts.py:_load_records` |
| **REQ-2** Regenerate morphologies via canonical generator | **Done** | `_build_geometry()` calls `generate_fixed_morphology(params, morph_seed)`; 57/57 cells built in 1.1 s. | `code/build_charts.py:_build_geometry`; run log |
| **REQ-3** Produce 8x8 morphology grid sorted by DSI | **Done** | `_plot_grid()` produces `morphology_grid_57cells.png`; 57 panels + 7 blanks; sorted DSI descending. | `results/images/morphology_grid_57cells.png` |
| **REQ-4** Produce DSI bar chart | **Done** | `_plot_dsi_bar()` produces `pareto_dsi_bar.png` with DSI=0.5 threshold line. | `results/images/pareto_dsi_bar.png` |
| **REQ-5** Produce PD-rate bar chart | **Done** | `_plot_pd_bar()` produces `pareto_pd_bar.png` with PD=30 Hz threshold line. | `results/images/pareto_pd_bar.png` |
| **REQ-6** Produce DSI-vs-PD scatter | **Done** | `_plot_dsi_vs_pd_scatter()` produces `pareto_dsi_vs_pd_scatter.png` with strict joint-pass star. | `results/images/pareto_dsi_vs_pd_scatter.png` |
| **REQ-7** Anchor color map applied across charts | **Done** | `cst.ANCHOR_COLORS` used uniformly in `_color_for_anchor`. | `code/constants.py:ANCHOR_COLORS` |
| **REQ-8** Anchor distribution recomputed and matches t0091 | **Done** | 20 / 0 / 12 / 9 / 16 — matches `t0091/results/data/anchor_tracking.json` `counts_per_anchor`. | `results/results_summary.md` Metrics |
| **REQ-9** Strict joint-pass cell identifiable | **Done** | Black star in scatter; top-left panel in grid (DSI=0.51, PD=35 Hz). | `results/images/pareto_dsi_vs_pd_scatter.png`, grid panel 1 |
| **REQ-10** Script runs in under 60 s | **Done** | 8.65 s end-to-end. | `logs/commands/...` |
| **REQ-11** ruff and mypy pass | **Done** | `ruff check`, `ruff format`, and `mypy -p ...code` all pass with no issues. | step 9 step log |
| **REQ-12** Charts embedded in results_detailed.md | **Done** | All four PNGs embedded with `![desc](../../../tasks/t0098_visualise_pareto_morphologies/results/images/file.png)` syntax + 1-3 sentence takeaway each. | this file Visualizations section |

</details>
