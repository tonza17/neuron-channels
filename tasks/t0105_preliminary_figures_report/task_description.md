# Preliminary-data figure pack and slide deck for report

## Motivation

The user is preparing a written report and a presentation deck and needs a curated set of
preliminary-data figures pulled from existing project results. The data is already calculated across
`t0065`-`t0102`; this task is **pure plotting and compilation** — no new NEURON simulations, no
new optimisation runs, no new biophysics decisions.

The deliverable is a coherent figure pack that walks the reader from "what the model is" (HH
equations, current densities, morphology) through "what the model does" (DSI tuning, somatic Vm with
and without action potentials, effect of adding channels) to "what optimisation found" (5-cell
panels per objective set).

## Scope

### Figures to produce

Each figure is a PNG under `results/images/` and a slide in the deck. The data source is named for
every figure; the implementation reads from the named task, does not re-run anything, and does not
re-derive any biophysical parameter.

1. **Hodgkin-Huxley equations (PNG, not text).** The canonical HH membrane equation plus the
   per-channel `Iᵢ = gᵢ · m^a · h^b · (V − Eᵢ)` blocks used by both bed models around
   `t0065`-`t0075`. Render with matplotlib LaTeX (`text.usetex` or mathtext) into a single PNG.
   Source: `tasks/t0070_writeup_two_model_beds/results/results_detailed.md` and the typeset
   `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf`.

2. **Current density table per current type, both bed models.** PNG-rendered table (matplotlib
   `Table` or `pandas.plotting.table`) with columns: channel, `gbar` (S/cm²), `E_rev` (mV),
   `V_half_act`, `τ_m`, `V_half_inact`, `τ_h`, source `code/<file>:<line>`. One bed per panel.
   Source: same as figure 1.

3. **Morphology per bed.** Cell schematic showing compartments / dendritic tree for Bed A
   (`t0008_port_modeldb_189347`) and Bed B (`t0024_port_de_rosenroll_2026_dsgc`). Use NEURON
   topology to draw a 2D projection. If a usable diagram already exists in `t0070`'s
   `results/images/`, reuse it.

4. **DSI as polar coordinates for synaptic currents, both beds.** Polar tuning of the synaptic drive
   (AMPA + NMDA + GABA peak conductance or peak post-synaptic current envelope) versus bar
   direction. Source for Bed A: `tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/`
   `fig1_psp_vs_angle.png` provides the PSP-vs-angle reproduction; convert into a polar plot variant
   or replot from the underlying CSV. Source for Bed B: use whatever multi-direction
   synaptic-current data exists in `t0066_t0024_epsp_ipsp_vm_protocol/results/`; if only PD/ND are
   present in Bed B, compute a two-point polar (PD vs ND) and label it as such — do not simulate
   new directions.

5. **Somatic Vm without and with action potentials, both beds, PD and ND.** The three-mode overlay
   trio (EPSP_PASSIVE, IPSP_PASSIVE, FULL) is the canonical view: HH off for the EPSP and IPSP
   passive traces, HH on for the FULL trace with action potentials. Sources:
   * Bed A PD/ND: `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/`
     `three_mode_pd_overlay.png` and `three_mode_nd_overlay.png`.
   * Bed B PD/ND: `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/`
     `three_mode_pd_overlay.png` and `three_mode_nd_overlay.png`. These existing PNGs may be reused
     directly with a unified caption layout in the figure pack; if compositing is needed (e.g., a
     2×2 panel: bed × direction), recreate from the underlying CSV in the source task's `results/`
     folder.

6. **Effect of introduction of different channels on DSI.** Sources:
   * `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/dsi_vs_density.png` —
     per-channel DSI vs `gbar` sweep at the soma.
   * `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/images/dsi_rescue_curve.png` —
     Nav1.6 + Kv3 co-expression rescue.
   * `tasks/t0069_t0067_ais_localised_channel_sweep/results/images/dsi_vs_density.png` and
     `soma_vs_ais_comparison.png` — AIS-localised version. Compose into a single multi-panel
     figure with consistent axes and a shared legend; reuse the underlying CSV in each source task
     if axis scaling needs to be unified.

7. **Optimisation: 5 cells per objective set — direction-selectivity tuning + morphology.**
   * **DSI + PD + robustness (3-objective NSGA-II).** Use the **latest** completed 3-obj run, which
     is `t0102_seedscale_n4_gen20`. Pick the top 5 Pareto cells by joint rank; for each cell render
     a 2-panel mini-figure: polar tuning curve + morphology schematic. The 57-cell morphology grid
     in `t0098_visualise_pareto_morphologies/results/images/` `morphology_grid_57cells.png` (from
     `t0091`) is a useful reference for layout style.
   * **DSI + PD (2-objective NSGA-II).** Deferred. The latest 2-obj run is `t0104` which is still
     `in_progress`. Add a placeholder slide in the deck noting the deferral, and create a follow-up
     suggestion in `results/suggestions.json` to render this panel once `t0104` completes. Do
     **not** depend on `t0104` in `task.json`.

### Deliverables

* `results/images/<figure_name>.png` — one PNG per figure (figures 1-7 above).
* `results/preliminary_figures_slides.pptx` — PowerPoint deck generated via `python-pptx`, one
  figure per slide, with concise caption and source-task citation in slide notes. Beamer is not
  used.
* `results/results_detailed.md` — full writeup embedding every PNG with `![desc](images/...png)`
  syntax, listing data provenance per figure and noting the deferred DSI+PD panel.
* `results/results_summary.md` — 2-3 paragraph summary suitable as a presentation abstract.
* Standard bookkeeping: `results/metrics.json`, `results/costs.json` (zero),
  `results/remote_machines_used.json` (empty), `results/suggestions.json` (must include a follow-up
  to render the DSI+PD optim panel after `t0104` completes).

### Out of scope

* No new NEURON simulations.
* No new optimisation runs.
* No re-derivation of biophysical parameters; every quoted parameter must cite a
  `code/<file>:<line>` from a dependency task (typically via `t0070`'s already-audited table).
* No changes to any other task folder.

## Approach

1. **Inventory existing PNGs and CSVs** in each dependency task's `results/` folder.
2. **Reuse PNGs verbatim** when their content already matches a figure spec (e.g., the t0065/t0066
   three-mode overlays for figure 5).
3. **Replot from underlying CSV** when composition or unification is needed (e.g., joint bed-A/bed-B
   comparison panels, top-5 Pareto cells).
4. **Render HH equations** with matplotlib mathtext (`r"$C_m \frac{dV}{dt} = -\sum_i I_i ...$"`) to
   PNG.
5. **Generate the slide deck** with `python-pptx`, embedding each PNG and adding the source-task
   citation as a slide note.
6. Run `uv run flowmark --inplace --nobackup` on `results_detailed.md` and `results_summary.md`
   before commit.

## Expected outputs

Listed under Deliverables above. No new typed assets (`expected_assets: {}`), so a `TF-W005` warning
is expected and acceptable — this is a presentation-prep task whose outputs live entirely in
`results/`.

## Stages

* `research-code` — inventory dependency tasks' `results/` (which PNGs reusable, which CSVs need
  replotting); confirm the t0046 PSP-vs-angle CSV exists.
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

Listed in `task.json`. Every dependency is needed because the task **reads from its results**. None
is a "process" dependency. `t0104_nsga2_2obj_dsi_pdrate_3seeds` is **not** a dependency — the
DSI+PD panel is deferred per user instruction.

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
* `results/suggestions.json` contains a follow-up suggestion to render the DSI+PD optim panel after
  `t0104` completes.
* All standard verificators pass.
