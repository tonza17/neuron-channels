# ✅ Preliminary-data figure pack and slide deck for report

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0105_preliminary_figures_report` |
| **Status** | ✅ completed |
| **Started** | 2026-05-13T21:45:23Z |
| **Completed** | 2026-05-13T22:44:12Z |
| **Duration** | 58m |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md), [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md), [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md), [`t0098_visualise_pareto_morphologies`](../../../overview/tasks/task_pages/t0098_visualise_pareto_morphologies.md), [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Task types** | `data-analysis` |
| **Step progress** | 9/13 |
| **Task folder** | [`t0105_preliminary_figures_report/`](../../../tasks/t0105_preliminary_figures_report/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0105_preliminary_figures_report/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0105_preliminary_figures_report/task_description.md)*

# Preliminary-data figure pack and slide deck for report

## Motivation

The user is preparing a written report and a presentation deck and needs a curated set of
preliminary-data figures pulled from existing project results. The data is already calculated
across `t0065`-`t0102`; this task is **pure plotting and compilation** — no new NEURON
simulations, no new optimisation runs, no new biophysics decisions.

The deliverable is a coherent figure pack that walks the reader from "what the model is" (HH
equations, current densities, morphology) through "what the model does" (DSI tuning, somatic
Vm with and without action potentials, effect of adding channels) to "what optimisation found"
(5-cell panels per objective set).

## Scope

### Figures to produce

Each figure is a PNG under `results/images/` and a slide in the deck. The data source is named
for every figure; the implementation reads from the named task, does not re-run anything, and
does not re-derive any biophysical parameter.

1. **Hodgkin-Huxley equations (PNG, not text).** The canonical HH membrane equation plus the
   per-channel `Iᵢ = gᵢ · m^a · h^b · (V − Eᵢ)` blocks used by both bed models around
   `t0065`-`t0075`. Render with matplotlib LaTeX (`text.usetex` or mathtext) into a single
   PNG. Source: `tasks/t0070_writeup_two_model_beds/results/results_detailed.md` and the
   typeset `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf`.

2. **Current density table per current type, both bed models.** PNG-rendered table (matplotlib
   `Table` or `pandas.plotting.table`) with columns: channel, `gbar` (S/cm²), `E_rev` (mV),
   `V_half_act`, `τ_m`, `V_half_inact`, `τ_h`, source `code/<file>:<line>`. One bed per panel.
   Source: same as figure 1.

3. **Morphology per bed.** Cell schematic showing compartments / dendritic tree for Bed A
   (`t0008_port_modeldb_189347`) and Bed B (`t0024_port_de_rosenroll_2026_dsgc`). Use NEURON
   topology to draw a 2D projection. If a usable diagram already exists in `t0070`'s
   `results/images/`, reuse it.

4. **DSI as polar coordinates for synaptic currents, both beds.** Polar tuning of the synaptic
   drive (AMPA + NMDA + GABA peak conductance or peak post-synaptic current envelope) versus
   bar direction. Source for Bed A:
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/` `fig1_psp_vs_angle.png`
   provides the PSP-vs-angle reproduction; convert into a polar plot variant or replot from
   the underlying CSV. Source for Bed B: use whatever multi-direction synaptic-current data
   exists in `t0066_t0024_epsp_ipsp_vm_protocol/results/`; if only PD/ND are present in Bed B,
   compute a two-point polar (PD vs ND) and label it as such — do not simulate new directions.

5. **Somatic Vm without and with action potentials, both beds, PD and ND.** The three-mode
   overlay trio (EPSP_PASSIVE, IPSP_PASSIVE, FULL) is the canonical view: HH off for the EPSP
   and IPSP passive traces, HH on for the FULL trace with action potentials. Sources:
   * Bed A PD/ND: `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/`
     `three_mode_pd_overlay.png` and `three_mode_nd_overlay.png`.
   * Bed B PD/ND: `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/`
     `three_mode_pd_overlay.png` and `three_mode_nd_overlay.png`. These existing PNGs may be
     reused directly with a unified caption layout in the figure pack; if compositing is
     needed (e.g., a 2×2 panel: bed × direction), recreate from the underlying CSV in the
     source task's `results/` folder.

6. **Effect of introduction of different channels on DSI.** Sources:
   * `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/dsi_vs_density.png` —
     per-channel DSI vs `gbar` sweep at the soma.
   * `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/images/dsi_rescue_curve.png` —
     Nav1.6 + Kv3 co-expression rescue.
   * `tasks/t0069_t0067_ais_localised_channel_sweep/results/images/dsi_vs_density.png` and
     `soma_vs_ais_comparison.png` — AIS-localised version. Compose into a single multi-panel
     figure with consistent axes and a shared legend; reuse the underlying CSV in each source
     task if axis scaling needs to be unified.

7. **Optimisation: 5 cells per objective set — direction-selectivity tuning + morphology.**
   * **DSI + PD + robustness (3-objective NSGA-II).** Use the **latest** completed 3-obj run,
     which is `t0102_seedscale_n4_gen20`. Pick the top 5 Pareto cells by joint rank; for each
     cell render a 2-panel mini-figure: polar tuning curve + morphology schematic. The 57-cell
     morphology grid in `t0098_visualise_pareto_morphologies/results/images/`
     `morphology_grid_57cells.png` (from `t0091`) is a useful reference for layout style.
   * **DSI + PD (2-objective NSGA-II).** Deferred. The latest 2-obj run is `t0104` which is
     still `in_progress`. Add a placeholder slide in the deck noting the deferral, and create
     a follow-up suggestion in `results/suggestions.json` to render this panel once `t0104`
     completes. Do **not** depend on `t0104` in `task.json`.

### Deliverables

* `results/images/<figure_name>.png` — one PNG per figure (figures 1-7 above).
* `results/preliminary_figures_slides.pptx` — PowerPoint deck generated via `python-pptx`, one
  figure per slide, with concise caption and source-task citation in slide notes. Beamer is
  not used.
* `results/results_detailed.md` — full writeup embedding every PNG with
  `![desc](images/...png)` syntax, listing data provenance per figure and noting the deferred
  DSI+PD panel.
* `results/results_summary.md` — 2-3 paragraph summary suitable as a presentation abstract.
* Standard bookkeeping: `results/metrics.json`, `results/costs.json` (zero),
  `results/remote_machines_used.json` (empty), `results/suggestions.json` (must include a
  follow-up to render the DSI+PD optim panel after `t0104` completes).

### Out of scope

* No new NEURON simulations.
* No new optimisation runs.
* No re-derivation of biophysical parameters; every quoted parameter must cite a
  `code/<file>:<line>` from a dependency task (typically via `t0070`'s already-audited table).
* No changes to any other task folder.

## Approach

1. **Inventory existing PNGs and CSVs** in each dependency task's `results/` folder.
2. **Reuse PNGs verbatim** when their content already matches a figure spec (e.g., the
   t0065/t0066 three-mode overlays for figure 5).
3. **Replot from underlying CSV** when composition or unification is needed (e.g., joint
   bed-A/bed-B comparison panels, top-5 Pareto cells).
4. **Render HH equations** with matplotlib mathtext (`r"$C_m \frac{dV}{dt} = -\sum_i I_i
   ...$"`) to PNG.
5. **Generate the slide deck** with `python-pptx`, embedding each PNG and adding the
   source-task citation as a slide note.
6. Run `uv run flowmark --inplace --nobackup` on `results_detailed.md` and
   `results_summary.md` before commit.

## Expected outputs

Listed under Deliverables above. No new typed assets (`expected_assets: {}`), so a `TF-W005`
warning is expected and acceptable — this is a presentation-prep task whose outputs live
entirely in `results/`.

## Stages

* `research-code` — inventory dependency tasks' `results/` (which PNGs reusable, which CSVs
  need replotting); confirm the t0046 PSP-vs-angle CSV exists.
* `planning` — finalise the slide order and the per-figure layout (which PNGs reused, which
  recomposed, axis-unification rules).
* `implementation` — render PNGs, compose panels, build `.pptx`.
* `analysis` — verify every figure matches its spec and every source citation is correct.
* `reporting` — write `results_detailed.md` and `results_summary.md`; add the deferred-panel
  suggestion.

## Compute and budget

* Local Windows workstation. No remote machines. No paid APIs.
* Time estimate: 2-4 hours total (mostly figure composition + slide assembly).
* Budget: $0.

## Dependencies

Listed in `task.json`. Every dependency is needed because the task **reads from its results**.
None is a "process" dependency. `t0104_nsga2_2obj_dsi_pdrate_3seeds` is **not** a dependency —
the DSI+PD panel is deferred per user instruction.

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Bed B has no multi-direction synaptic-current data; polar tuning for figure 4 is undefined. | `t0066/results/` has only PD/ND traces, no per-angle CSV. | Render a two-point polar (PD vs ND) for Bed B and label clearly; do not simulate. |
| 2 | HH equation PNG rendering with matplotlib mathtext loses Greek typesetting fidelity vs. the t0071 LaTeX PDF. | Visual inspection shows broken glyphs or fallback fonts. | Switch to `text.usetex=True` (requires LaTeX install) or vector-render via tikz and rasterise. Document the rendering choice in `results_detailed.md`. |
| 3 | The 57-cell morphology grid in `t0098` uses an older 68-d slice; top-5 selection from `t0102` may need its own renderer. | `t0102` Pareto morphology PNGs do not exist as a 5-cell subset. | Reuse the `t0098` plotting code (`code/`) on `t0102`'s Pareto JSON to render a fresh 5-cell mini-grid. |
| 4 | `t0104` completes during this task and the user wants the DSI+PD panel inline rather than as a follow-up. | User intervention. | Drop the deferred-panel placeholder, add `t0104` as a dependency in a correction or in a follow-up task — do not modify this task once started. |
| 5 | `python-pptx` is not in `pyproject.toml`. | `uv sync` doesn't bring it. | Add it to `pyproject.toml` (top-level tooling file change is allowed) before implementation. |

## Verification criteria

* `results_summary.md` and `results_detailed.md` exist and pass `verify_task_results`.
* Every PNG referenced in `results_detailed.md` exists under `results/images/`.
* Each figure's caption cites at least one `code/<file>:<line>` or
  `tasks/<dep_task_id>/results/<file>` for provenance.
* The slide deck `results/preliminary_figures_slides.pptx` exists and opens in PowerPoint
  (smoke-check by `python-pptx` round-trip).
* `results/suggestions.json` contains a follow-up suggestion to render the DSI+PD optim panel
  after `t0104` completes.
* All standard verificators pass.

</details>

## Metrics

### t0102 Pareto cell 19 (seed 55) -- DSI=0.016, PD=41.43Hz

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.01622133040053583** |

### t0102 Pareto cell 16 (seed 55) -- DSI=0.022, PD=37.14Hz

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.022295894756352633** |

### t0102 Pareto cell 14 (seed 55) -- DSI=0.024, PD=29.29Hz

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.023575364723561136** |

### t0102 Pareto cell 21 (seed 44) -- DSI=0.033, PD=45.89Hz

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.032650822491865544** |

### t0102 Pareto cell 22 (seed 55) -- DSI=0.016, PD=50.18Hz

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.015898199154530338** |

## Suggestions Generated

<details>
<summary><strong>Render figure 7b -- 5-cell DSI+PD 2-obj NSGA-II Pareto panel from
t0104 once t0104 completes</strong> (S-0105-01)</summary>

**Kind**: evaluation | **Priority**: medium

REQ-9 (REQ-DEFERRED-PANEL) of t0105 was deferred because t0104_nsga2_2obj_dsi_pdrate_3seeds
was still in_progress. Once t0104 reaches status completed, render the figure-7 counterpart
(top-5 Pareto cells under DSI+PD 2-objective NSGA-II) using the same selection rule as figure
7a: filter pd_rate_hz >= 5.0 to drop silenced spurious-Pareto-anchor cells, then pick the top
5 by joint Pareto rank, and render a 2-panel mini-figure per cell (morphology schematic +
two-point polar tuning). Append the rendered panel as a new slide in t0105's
preliminary_figures_slides.pptx via a follow-up task (do not mutate t0105 -- create a new task
or a correction overlay). Reuse the renderer in
tasks/t0105_preliminary_figures_report/code/render_pareto_top5.py and read pareto-front JSON
from tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/. Priority: medium-high because it
gates presentation/report completeness. Recommended task types: data-analysis.

</details>

<details>
<summary><strong>Multi-angle synaptic-current protocol on Bed A and Bed B for a
true polar synaptic tuning curve</strong> (S-0105-02)</summary>

**Kind**: experiment | **Priority**: medium

Figure 4 of t0105 had to fall back to a two-point polar (PD at 0 deg, ND at 180 deg) because
neither t0046 (Bed A) nor t0066 (Bed B) recorded synaptic currents at intermediate stimulus
angles. Run an EPSC + IPSC peak-amplitude protocol at the standard 12-angle grid for both beds
(re-using the bar-stimulus generator from t0046 / t0066), record AMPA + NMDA + GABA peak
conductances and peak post-synaptic currents per angle, and save a CSV per bed compatible with
the t0011 plot_polar_tuning_curve loader. Output: two new polar plots that replace t0105's
two-point fallback in any successor figure pack. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Promote the t0098 morphology renderer (with t0100 vector_68d[54:]
slice fix) into a reusable library asset</strong> (S-0105-03)</summary>

**Kind**: library | **Priority**: medium

Figure 7 in t0105 had to copy the morphology renderer code from
tasks/t0098_visualise_pareto_morphologies/code/build_charts.py into
tasks/t0105_preliminary_figures_report/code/render_pareto_top5.py with the vector_68d[54:]
morphology-slice fix from t0100 patched in manually. The t0104 follow-up panel (S-0105-01),
and any future optimisation-result report task, will need the same renderer. Package this
renderer as a top-level library asset (e.g., dsgc_morphology_renderer) under a host task --
expose a clean Python API (render_morphology(vector_68d, ax) plus a multi-cell grid helper),
include the t0100 slice fix as the default behaviour, register a details.json under
assets/library/, and document import path tasks.<host_task>.code.dsgc_morphology_renderer.
Downstream tasks then import instead of copying. Recommended task types: write-library.

</details>

<details>
<summary><strong>Add a project-wide python-pptx slide-deck builder library so figure
packs reuse a common deck assembler</strong> (S-0105-04)</summary>

**Kind**: library | **Priority**: medium

t0105 introduced python-pptx>=1.0 and implemented
tasks/t0105_preliminary_figures_report/code/build_slides.py as a task-local
one-figure-per-slide deck assembler with caption + source-task citation in slide notes.
Multiple downstream tasks (per-report figure packs, brainstorm decks, t0104 follow-up, future
MOBO writeups) will want the same machinery. Package build_slides.py as a reusable library
asset under a host task -- expose build_deck(slides: list[SlideSpec], output_path: Path) and a
SlideSpec dataclass (image_path, caption, notes, layout), register a details.json under
assets/library/, and document the import path. Downstream tasks then call the library instead
of re-implementing python-pptx layout per task. Recommended task types: write-library.

</details>

## Research

* [`research_code.md`](../../../tasks/t0105_preliminary_figures_report/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0105_preliminary_figures_report/results/results_summary.md)*

--- spec_version: "2" task_id: "t0105_preliminary_figures_report" date_completed: "2026-05-13"
status: "complete" ---
# Results Summary: Preliminary-Data Figure Pack and Slide Deck

## Summary

Produced a coherent preliminary-data figure pack covering seven figure groups for the DSGC
modelling project: HH equations, per-bed conductance density tables, two morphologies, polar
synaptic DSI (two-point), somatic Vm three-mode overlays, channel-effect-on-DSI sweep, and the
top-5 Pareto cells from the 3-objective NSGA-II run `t0102_seedscale_n4_gen20`. All 10 PNGs
land in `results/images/` and the 11-slide `preliminary_figures_slides.pptx` deck embeds every
PNG with caption + source-task citation. The 2-objective DSI+PD Pareto panel is deferred (a
placeholder slide and a follow-up suggestion record the gap). Cost: $0; no remote machines.

## Metrics

* **Figures produced**: 10 PNGs (`fig01_hh_equations`, `fig02_conductance_table_bed_{a,b}`,
  `fig03_bed_{a,b}_morphology`, `fig04_polar_synaptic_bed_{a,b}`, `fig05_three_mode_overlays`,
  `fig06_channel_effect_on_dsi`, `fig07_top5_pareto_3obj`).
* **Slide deck**: 11 slides in `preliminary_figures_slides.pptx`, 1.75 MB, round-trips through
  `python-pptx`.
* **Top-5 Pareto cell DSI** (3-obj, `t0102`): variant DSIs are 0.0162, 0.0223, 0.0236, 0.0327,
  0.0159 (in plot-order from `metrics.json`
  `variants[*].metrics.direction_selectivity_index`). Recorded as 5 variants in `metrics.json`
  with `pd_rate_hz`, `robustness`, and source-cell dimensions.
* **Quality gates**: `ruff check --fix`, `ruff format`, `mypy -p
  tasks.t0105_preliminary_figures_report.code` — all clean. End-to-end `main.py`
  reproducibility run: ~25 s.
* **REQ coverage**: 12 of 12 REQs satisfied (`REQ-1..REQ-12`); REQ-9 satisfied via
  deferred-panel placeholder + follow-up suggestion.

## Verification

* `verify_task_file.py` — PASSED, 0 errors.
* `verify_task_dependencies.py` — PASSED, 0 errors (13 deps all completed).
* `verify_research_code.py` — PASSED, 0 errors, 0 warnings.
* `verify_plan.py` — PASSED, 0 errors, 0 warnings.
* `verify_task_metrics.py` — PASSED, 0 errors, 0 warnings.
* Full pre-merge verification will run in the `reporting` step.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0105_preliminary_figures_report/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0105_preliminary_figures_report" date_completed: "2026-05-13"
status: "complete" ---
# Preliminary-Data Figure Pack and Slide Deck — Detailed Results

## Summary

This task compiled a coherent preliminary-data figure pack for a written report and a
presentation deck on direction-selective ganglion cell (DSGC) modelling. Pure plotting: no new
NEURON simulations, no new optimisation runs, no biophysical re-derivation. Seven figure
groups (10 PNGs) plus an 11-slide `python-pptx` deck were produced from 13 dependency tasks.
The 2-objective DSI+PD Pareto panel is deferred (placeholder slide + follow-up suggestion)
because its source task `t0104_nsga2_2obj_dsi_pdrate_3seeds` is still `in_progress`. All 12
plan REQs (`REQ-1`..`REQ-12`) are satisfied. Cost: $0; no remote machines.

## Methodology

* **Machine**: Local Windows 11 workstation (`win32`, PowerShell). No remote compute.
* **Python env**: `uv sync` with `python-pptx>=1.0` added in this task; `matplotlib`,
  `pandas`, `pydantic` pre-existing.
* **Runtime**: end-to-end `code/main.py` reproducibility run ≈ 25 s.
* **Start**: 2026-05-13T21:45:23Z. **End** (results step): 2026-05-13T22:34:21Z.
* **Reproducibility**: every figure is regenerated by re-running `uv run python -m
  tasks.t0105_preliminary_figures_report.code.main`. Source data paths are centralised in
  `code/paths.py`; constants in `code/constants.py`.

### Data sources (per figure)

| Figure | Source task(s) | Reuse strategy |
| --- | --- | --- |
| Fig 1 — HH equations | `t0070_writeup_two_model_beds/results/results_detailed.md` L120-134 (Bed A), L405-415 (Bed B) | Replot via matplotlib mathtext |
| Fig 2 — conductance tables | `t0070` L158-169 (Bed A, 11 rows), L452-465 (Bed B, 12 rows) | Render `matplotlib.Table` with source `code/<file>:line` provenance |
| Fig 3 — morphology | `t0070_writeup_two_model_beds/results/images/bed_{a,b}_morphology.png` | Copy verbatim |
| Fig 4 — polar synaptic DSI | `t0046/results/data/fig1_psp.csv` (16 rows: PD/ND only); `t0066/results/data/voltage_traces.csv` (PD/ND only) | Two-point polar (PD at 0°, ND at 180°) for both beds, labelled |
| Fig 5 — three-mode overlays | `t0065/results/data/voltage_traces.csv` (Bed A) and `t0066/results/data/voltage_traces.csv` (Bed B), 10 kHz × 1400 ms × 3 modes × 2 dirs | Recompose 2×2 (bed × direction) panel |
| Fig 6 — channel-effect-on-DSI | `t0067/results/data/dsi_by_condition.json` (16 conds), `t0068/.../dsi_by_condition.json` (9), `t0069/.../dsi_by_condition.json` (16) | Replot from JSON on shared axes |
| Fig 7 — top-5 3-obj Pareto | `t0102_seedscale_n4_gen20/results/data/pareto_front_seed{44,55}.json` (29+31 cells) | Filter `pd_rate_hz >= 5.0` to drop silenced cells; pick 5 by joint rank; render morphology + two-point polar per cell. Morphology renderer copied from `t0098/code/build_charts.py` with `vector_68d[54:]` (t0100 fix). |

## Figures

### Figure 1 — Hodgkin-Huxley membrane equations

![Hodgkin-Huxley equations for both
beds](../../../tasks/t0105_preliminary_figures_report/results/images/fig01_hh_equations.png)

Renders the canonical compartmental membrane equation `C_m · dV/dt = -Σ Iᵢ - I_syn - I_inj`
together with the per-channel current blocks (`I_Na = g_Na · m³ · h · (V − E_Na)` etc.) for
both Bed A and Bed B, drawn via matplotlib mathtext. All values are sourced verbatim from
`t0070`'s already-audited writeup with `code/<file>:line` provenance preserved in figure 2.

### Figure 2 — Per-bed conductance density tables

![Bed A conductance
table](../../../tasks/t0105_preliminary_figures_report/results/images/fig02_conductance_table_bed_a.png)

![Bed B conductance
table](../../../tasks/t0105_preliminary_figures_report/results/images/fig02_conductance_table_bed_b.png)

For each bed: one `matplotlib.Table` per channel with columns Channel | `gbar` (S/cm²) |
`E_rev` (mV) | `V_half_act` | `τ_m` | `V_half_inact` | `τ_h` | source `code/<file>:line`. Bed
A has 11 channels and Bed B has 12; values come verbatim from t0070's audited tables.

### Figure 3 — Cell morphologies

![Bed A morphology
schematic](../../../tasks/t0105_preliminary_figures_report/results/images/fig03_bed_a_morphology.png)

![Bed B morphology
schematic](../../../tasks/t0105_preliminary_figures_report/results/images/fig03_bed_b_morphology.png)

Reused verbatim from `t0070_writeup_two_model_beds/results/images/`. Bed A is the t0008
deposited Poleg-Polsky 2016 cell (NEURON section schematic); Bed B is the t0024 de Rosenroll
2026 port (sparser arbor).

### Figure 4 — Polar synaptic DSI (two-point)

![Bed A polar synaptic
DSI](../../../tasks/t0105_preliminary_figures_report/results/images/fig04_polar_synaptic_bed_a.png)

![Bed B polar synaptic
DSI](../../../tasks/t0105_preliminary_figures_report/results/images/fig04_polar_synaptic_bed_b.png)

Two-point polar plots: PD at 0° and ND at 180°, with a red preferred-direction arrow. Neither
`t0046` nor `t0066` measured intermediate angles for synaptic currents, so a full polar tuning
curve is not derivable from existing data — this figure is explicitly labelled "two-point
polar" in its title and caption (Risk #1 from the plan; the fallback is documented).

### Figure 5 — Somatic Vm three-mode overlays

![Three-mode Vm overlays: bed ×
direction](../../../tasks/t0105_preliminary_figures_report/results/images/fig05_three_mode_overlays.png)

A 2×2 grid (`{Bed A, Bed B} × {PD, ND}`) of the EPSP_PASSIVE (HH off, EPSC isolated),
IPSP_PASSIVE (HH off, IPSC isolated), and FULL (HH on, action potentials) traces. Recomposed
from each bed's `voltage_traces.csv` for uniform axis treatment. The "without action
potentials" vs "with action potentials" contrast is the EPSP/IPSP passive traces vs the FULL
active trace.

### Figure 6 — Effect of channel addition on DSI

![Channel-effect on DSI: soma sweep, Nav1.6+Kv3 rescue, AIS
sweep](../../../tasks/t0105_preliminary_figures_report/results/images/fig06_channel_effect_on_dsi.png)

Unified multi-panel: t0067 soma channel sweep (16 conditions), t0068 Nav1.6+Kv3 co-expression
rescue (9 conditions), and t0069 AIS-localised sweep (16 conditions). Replotted from each
task's `dsi_by_condition.json` on shared DSI y-axis so the three sweeps compare directly.

### Figure 7 — Top-5 Pareto cells (3-objective NSGA-II, DSI + PD + robustness)

![Top-5 Pareto cells from t0102: morphology + two-point polar per
cell](../../../tasks/t0105_preliminary_figures_report/results/images/fig07_top5_pareto_3obj.png)

Five cells from `t0102_seedscale_n4_gen20` after filtering `pd_rate_hz >= 5.0` to drop
silenced cells (whose `dsi_vector_sum = 1.0` is a spurious-Pareto-anchor artifact flagged in
`t0102/results_summary.md`). Each cell gets two panels: 2D morphology schematic (renderer
copied from `t0098/code/build_charts.py` with the `vector_68d[54:]` slice fix from `t0100`)
and a two-point polar (PD vs ND) tuning. Cells are colour-coded by Pareto seed (44 vs 55)
because `t0102` cells carry no warm-start anchor attribution.

DSI values for the five selected cells (from `metrics.json`):

| Variant | Cell / seed | DSI | PD rate (Hz) | Robustness |
| --- | --- | --- | --- | --- |
| `pareto-cell-19-seed55` | 19 / 55 | 0.0162 | 41.43 | 0.985 |
| `pareto-cell-16-seed55` | 16 / 55 | 0.0223 | 37.14 | 0.966 |
| `pareto-cell-14-seed55` | 14 / 55 | 0.0236 | 29.29 | 0.977 |
| `pareto-cell-21-seed44` | 21 / 44 | 0.0327 | 45.89 | 0.912 |
| `pareto-cell-22-seed55` | 22 / 55 | 0.0159 | 50.18 | 0.964 |

The DSI+PD 2-objective panel (`REQ-DEFERRED-PANEL`) is **deferred**.
`t0104_nsga2_2obj_dsi_pdrate_3seeds` was still `in_progress` at this task's start time, so the
deck includes a placeholder slide ("Figure 7b — DSI + PD 2-obj Pareto (DEFERRED)") and a
follow-up suggestion will be added in the suggestions step.

## Slide deck

`results/preliminary_figures_slides.pptx` (1.75 MB, 11 slides):

| Slide | Content | Source citation (in notes) |
| --- | --- | --- |
| 1 | Title + scope | This task |
| 2 | Fig 1 HH equations | `t0070` |
| 3 | Fig 2a Bed A conductance table | `t0070`, `t0008/main.hoc:L148-150` |
| 4 | Fig 2b Bed B conductance table | `t0070`, `t0024/code/constants.py:L34-42` |
| 5 | Fig 3a Bed A morphology | `t0008`, `t0070` |
| 6 | Fig 3b Bed B morphology | `t0024`, `t0070` |
| 7 | Fig 4a Bed A polar synaptic | `t0046`, `t0066` |
| 8 | Fig 5 three-mode overlays | `t0065`, `t0066` |
| 9 | Fig 6 channel-effect-on-DSI | `t0067`, `t0068`, `t0069` |
| 10 | Fig 7 top-5 3-obj Pareto | `t0102`, `t0098` |
| 11 | Fig 7b DSI+PD 2-obj (DEFERRED) | `t0104` (pending) |

Deck round-trips through `python-pptx.Presentation(...)` — verified during the implementation
step.

## Verification

* `verify_task_file.py` — PASSED, 0 errors. (1 warning `TF-W005` — empty `expected_assets` —
  expected for a presentation-prep task.)
* `verify_task_dependencies.py` — PASSED, 0 errors, 0 warnings (13/13 deps `completed`).
* `verify_research_code.py` — PASSED, 0 errors, 0 warnings.
* `verify_plan.py` — PASSED, 0 errors, 0 warnings.
* `verify_task_metrics.py` — PASSED, 0 errors, 0 warnings (5-variant explicit format).
* `ruff check --fix .` — 0 issues across 11 `.py` files in `code/`.
* `ruff format .` — 13 files already formatted.
* `mypy -p tasks.t0105_preliminary_figures_report.code` — 0 errors.
* `code/main.py` end-to-end smoke run — succeeds; every PNG and the `.pptx` exist with
  non-zero size.

Full pre-merge verification (file isolation, branch naming, PR format, no-large-files) runs in
the `reporting` step.

## Limitations

1. **Figure 4 is a two-point polar, not a continuous tuning curve.** Neither `t0046` nor
   `t0066` measured intermediate stimulus angles for synaptic currents. The figure is labelled
   accordingly; a future task could run a multi-angle synaptic-current protocol to produce a
   genuine polar tuning.

2. **Figure 7 covers only the 3-objective Pareto (DSI + PD + robustness).** The 2-objective
   DSI+PD panel is deferred until `t0104_nsga2_2obj_dsi_pdrate_3seeds` completes. The slide
   deck has a placeholder; a follow-up suggestion will be added in the suggestions step.

3. **Figure 7 cells are colour-coded by Pareto GA seed (44 vs 55), not by warm-start anchor.**
   `t0102` cells were random-init (no warm-start anchors); the plan anticipated this.

4. **Figure 4 reuses a plain matplotlib polar instead of the t0011
   `plot_polar_tuning_curve`.** The t0011 loader strictly enforces a 12-angle CSV schema,
   which is incompatible with the two-point (PD/ND) data. Same conceptual content is
   preserved.

5. **DSI values come from `t0102` evaluation at the original `N_SEEDS=4` noise budget.** No
   re-evaluation was done here; trends would change under different `N_SEEDS`. Documented in
   `metrics.json` `variants[*].dimensions`.

## Files Created

* `code/paths.py`, `code/constants.py` (centralised paths and magic-string constants per
  styleguide).
* `code/render_hh_equations.py`, `code/render_conductance_table.py`,
  `code/render_morphology.py`, `code/render_polar_synaptic.py`,
  `code/render_three_mode_overlays.py`, `code/render_channel_effect.py`,
  `code/render_pareto_top5.py` (per-figure renderers).
* `code/build_slides.py` (python-pptx deck assembly).
* `code/main.py` (end-to-end driver — runs every renderer and the deck builder).
* `results/images/fig01_hh_equations.png`, `fig02_conductance_table_bed_a.png`,
  `fig02_conductance_table_bed_b.png`, `fig03_bed_a_morphology.png`,
  `fig03_bed_b_morphology.png`, `fig04_polar_synaptic_bed_a.png`,
  `fig04_polar_synaptic_bed_b.png`, `fig05_three_mode_overlays.png`,
  `fig06_channel_effect_on_dsi.png`, `fig07_top5_pareto_3obj.png` (10 PNGs).
* `results/preliminary_figures_slides.pptx` (11-slide deck).
* `results/data/fig07_top5_cells.json` (top-5 sidecar with `pd_rate_hz >= 5.0` filter
  applied).
* `results/metrics.json` (5 variants), `results/costs.json` (zero),
  `results/remote_machines_used.json` (empty), `results/suggestions.json` (written in the next
  step).
* `results/results_summary.md`, `results/results_detailed.md` (this file).
* `pyproject.toml`, `uv.lock` (added `python-pptx>=1.0`).

## Task Requirement Coverage

Operative task text quoted verbatim from `task.json` and `task_description.md`:

> **Name**: Preliminary-data figure pack and slide deck for report
>
> **Short**: Compile preliminary-data figures (HH equations PNG, conductance table, morphologies,
> polar synaptic DSI, somatic Vm passive/active, channel-effect-on-DSI, 5-cell optim panels) into
> PNGs + .pptx deck.
>
> Figures to produce: (1) HH equations PNG, (2) per-bed conductance density tables, (3) per-bed
> morphology, (4) polar synaptic DSI both beds, (5) three-mode Vm overlays both beds and directions,
> (6) effect of channel introduction on DSI, (7) 5-cell direction-selectivity + morphology
> mini-panels for (a) 3-obj DSI+PD+robustness optimisation and (b) 2-obj DSI+PD — 7b deferred.
> Deliverables include PNGs + python-pptx slide deck + standard results bookkeeping. Out of scope:
> no new NEURON simulations, no new optimisation runs.

REQ-by-REQ disposition:

| REQ | Alias | Result | Status | Evidence |
| --- | --- | --- | --- | --- |
| REQ-1 | REQ-FIG-1 | HH equations PNG rendered via matplotlib mathtext for both beds. | Done | `results/images/fig01_hh_equations.png` |
| REQ-2 | REQ-FIG-2 | Bed A (11-row) and Bed B (12-row) conductance tables with source `code/<file>:line` provenance per row. | Done | `results/images/fig02_conductance_table_bed_{a,b}.png` |
| REQ-3 | REQ-FIG-3 | Bed A and Bed B morphology PNGs copied verbatim from `t0070`. | Done | `results/images/fig03_bed_{a,b}_morphology.png` |
| REQ-4 | REQ-FIG-4 | Two-point polar (PD vs ND) for both beds, explicitly labelled. | Done | `results/images/fig04_polar_synaptic_bed_{a,b}.png` |
| REQ-5 | REQ-FIG-5 | 2×2 (bed × direction) three-mode overlay panel recomposed from raw CSVs. | Done | `results/images/fig05_three_mode_overlays.png` |
| REQ-6 | REQ-FIG-6 | Channel-effect-on-DSI multi-panel combining `t0067`, `t0068`, `t0069` on shared y-axis. | Done | `results/images/fig06_channel_effect_on_dsi.png` |
| REQ-7 | REQ-FIG-7-3OBJ | Top-5 Pareto cells from 3-obj `t0102` after `pd_rate_hz >= 5.0` filter, with `vector_68d[54:]` t0100 fix on the morphology renderer. | Done | `results/images/fig07_top5_pareto_3obj.png`, `results/data/fig07_top5_cells.json`, `results/metrics.json` |
| REQ-8 | REQ-DECK | 11-slide `python-pptx` deck, one figure per slide, captioned, source-task citation in notes; round-trips through `Presentation(...)`. | Done | `results/preliminary_figures_slides.pptx` |
| REQ-9 | REQ-DEFERRED-PANEL | Placeholder slide added; follow-up suggestion to be written in the `suggestions` step. | Done | Slide 11 of the deck; pending `results/suggestions.json` |
| REQ-10 | REQ-RESULTS-MD | This file with embedded figures, methodology, verification, limitations, and per-figure provenance. | Done | This `results_detailed.md` |
| REQ-11 | REQ-RESULTS-SUMMARY | 2-3 paragraph presentation abstract. | Done | `results/results_summary.md` |
| REQ-12 | REQ-NO-EXTERNAL-CHANGES | Only `pyproject.toml`, `uv.lock`, and `tasks/t0105_preliminary_figures_report/` touched. | Done | `git status` on `task/t0105_preliminary_figures_report` branch limited to allow-listed paths |

</details>
