---
spec_version: "1"
task_id: "t0105_preliminary_figures_report"
research_stage: "code"
tasks_reviewed: 16
tasks_cited: 16
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-05-13"
status: "complete"
---
# Research Code: Preliminary-Data Figure Pack and Slide Deck

## Task Objective

Compile a curated figure pack covering Hodgkin-Huxley equations, conductance density tables, two
DSGC morphologies, polar synaptic DSI, somatic Vm passive-and-active overlays, channel-effect-on-DSI
sweeps, and Pareto morphology+tuning panels into PNGs and a `python-pptx` slide deck. The task is
pure figure composition: it reads existing results from 13 completed dependency tasks, reuses PNGs
verbatim when possible, replots from saved CSV/JSON when composition or unification is needed, and
adds zero new NEURON simulations or new biophysics. The DSI+PD 2-objective Pareto panel is deferred
because `t0104` is still `in_progress`.

## Library Landscape

The library aggregator (`uv run python -u -m arf.scripts.aggregators.aggregate_libraries`) is not
shipped in this repository — only `aggregate_tasks`, `aggregate_costs`, `aggregate_metrics`,
`aggregate_metric_results`, `aggregate_suggestions`, `aggregate_categories`, `aggregate_task_types`,
and `aggregate_machines` are present in `arf/scripts/aggregators/`. Library assets were enumerated
directly: `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/` is the only
library asset in any dependency task of this task. Its `details.json` (spec_version 2, version
`0.1.0`, created by `t0011_response_visualization_library`, dated 2026-04-20) registers four entry
points relevant to this task: `plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`,
`plot_multi_model_overlay`, and `plot_angle_raster_psth`. Import path is
`tasks.t0011_response_visualization_library.code.tuning_curve_viz` ([t0011]). The aggregator output
is not available so corrections cannot be checked programmatically; spot-check of `corrections/` in
dependency tasks reveals no corrections affecting this library. Relevance: **high** for figure 7
per-cell polar tuning panels (when paired with simulated per-cell CSVs) and for figure 4 polar
synaptic DSI overlays. No other libraries discovered.

## Key Findings

### Figure 1: HH equation PNG must be rendered fresh; t0070 provides the audited text

[t0070]'s `results/results_detailed.md` lines 120-134 and 405-415 already render the canonical
Hodgkin-Huxley membrane equation `C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj` plus per-channel breakdowns
for both beds (`I_Na = g_Na · m³ · h · (V - E_Na)`, `I_Kdr = g_Kdr · n⁴ · (V - E_K)`, `I_Km`,
`I_leak`, plus `I_CaL`/`I_CaT` for Bed B only). These appear inside fenced `text` blocks, not as
PNGs. [t0071]'s `code/render_pdf.py` typeset the same equations into `results_detailed.pdf` via
`typst`, not matplotlib. **No PNG already exists** — the task must render fresh via matplotlib
mathtext. The risk noted in `task_description.md` (mathtext glyph fidelity vs typst) is real; a
fallback is to set `text.usetex=True` if a LaTeX install is available, otherwise use mathtext
strings copied verbatim from [t0070] lines 122-134 / 408-415.

### Figure 2: Conductance density tables — replot from [t0070]'s audited markdown tables

[t0070]'s conductance tables are markdown, not images. The Bed A table (`results_detailed.md` lines
158-169) has 11 rows × 9 columns (Channel, Gating, V_half_act, τ_act, V_half_inact, τ_inact, gbar,
E_rev, Source) with `code/<file>:line` provenance per row. The Bed B table (lines 452-465) follows
the same schema with 12 rows including per-tier rows (soma / primary / non-terminal / terminal) and
the `cad` calcium-decay shell. The numeric values can be extracted directly from
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc` (Bed A,
RGCsomana/RGCsomakv/RGCsomakm at L148-L150) and
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` lines 34-42 (Bed B, `GNA_SOMA_MS = 150`,
`GNA_PRIMARY_MS = 200`, etc.) ([t0008], [t0024], [t0070]). Render via `matplotlib.table.Table` or
`pandas.plotting.table` with the same column headers.

### Figure 3: Morphology PNGs already exist and can be reused verbatim

[t0070] produced `results/images/bed_a_morphology.png` and `results/images/bed_b_morphology.png` via
`code/plot_morphology.py` (388 lines) using the helpers in `code/schematic_helpers.py` and counts in
`code/constants.py` (`BED_A_N_ON_DEND = 282`, `BED_B_N_TERMINAL_DEND_APPROX = 177`, etc.). These are
illustrative radial-fan schematics, not 3D NEURON renders, but the `task_description.md` lists
[t0070]'s diagrams as the canonical source for figure 3. **Verbatim reuse is the right choice** —
copy the two PNGs into `results/images/` and cite them in the caption. No need to re-render unless
the figure pack wants a unified style with figure 7's top-down dendrogram (in which case use
[t0098]'s morphology generator approach with `vector_68d[54:]` morphology slice).

### Figure 4: Polar synaptic DSI — both beds have only PD/ND, no multi-angle synaptic CSV

[t0046]'s `fig1_psp.csv` contains only `direction_label ∈ {PD, ND}` at `direction_deg ∈ {0, 180}`
across 16 rows (4 trials × 2 dirs × 2 gNMDA conditions); the existing
`results/images/fig1_psp_vs_angle.png` is a Cartesian bar chart, not a tuning curve. [t0066]'s
`data/voltage_traces.csv` likewise contains only `direction ∈ {PD, ND}` and
`mode ∈ {FULL, EPSP_PASSIVE, IPSP_PASSIVE}` (1400 ms × 3 modes × 2 dirs). **No per-angle
synaptic-current data exists for either bed**, confirming Risk #1 in `task_description.md`: figure 4
must be a two-point polar (PD vs ND) for both beds, labelled as such. The PSP-vs-angle from [t0046]
still appears in the deck as supplementary evidence ([t0046], [t0066]).

### Figure 5: Three-mode overlays already exist — reuse PNGs or recompose from CSV

Both [t0065] (Bed A) and [t0066] (Bed B) produced exactly the right artefacts: PNG
`three_mode_pd_overlay.png` and `three_mode_nd_overlay.png` in `results/images/`, and the underlying
`data/voltage_traces.csv` (60,007 rows × `mode/direction/t_ms/v_mv` for Bed A; same schema for Bed
B). The CSV is dense enough (10 kHz × 1400 ms × 3 modes × 2 dirs) to recompose any panel layout: a
2×2 bed × direction matrix is the cleanest, but the existing PNGs may also be tiled directly. PD/ND
convention is verified in `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/constants.py` L19-L20
(`DIRECTION_PD_DEG = 0.0`, `DIRECTION_ND_DEG = 180.0`). HH is OFF for EPSP_PASSIVE/IPSP_PASSIVE and
ON for FULL — this matches the user's memory `feedback_dsgc_measurement_protocol.md` ([t0065],
[t0066]).

### Figure 6: Channel-effect-on-DSI — three sources, unify axes by replotting from JSON

Three sweeps contribute to figure 6, each with a usable PNG **and** a structured JSON:

* [t0067] `results/images/dsi_vs_density.png` plus `data/dsi_by_condition.json` (16 conditions each
  with `condition_id`, `channel`, `density_mS_cm2`, `dsi`, `firing_rate_pd_hz`, etc.). Soma
  channel-addition sweep.
* [t0068] `results/images/dsi_rescue_curve.png` plus `data/dsi_by_condition.json` (9 conditions with
  `nav16_mS_cm2`, `kv3_mS_cm2`, `dsi`). Nav1.6+Kv3 co-expression rescue.
* [t0069] `results/images/dsi_vs_density.png` and `soma_vs_ais_comparison.png` plus
  `data/dsi_by_condition.json` (16 conditions with `condition_id`, `channel`, `density_mS_cm2`,
  `dsi`). AIS-localised version of t0067.

To unify axes (DSI on y; channel density on x; one panel per channel × location), **replot all three
from JSON** rather than tiling raw PNGs. The PNGs differ in axis ranges, marker styles, and title
formatting, so a multi-panel composite reading the three JSONs gives a consistent figure ([t0067],
[t0068], [t0069]).

### Figure 7: Pareto 5-cell panels — replot from `pareto_front_seed{44,55}.json`

[t0102] saves the 3-obj Pareto fronts as `results/data/pareto_front_seed44.json` (29 cells) and
`pareto_front_seed55.json` (31 cells) — **60 cells total**. Each cell record carries `vector_68d`
(the full 68-d genome), `morphology_vector_14d` (the 14-d morphology slice, same 14-d schema as
[t0091]/[t0098]), `dsi_vector_sum`, `pd_rate_hz`, and `robustness`. The 5-cell selection rule from
`task_description.md` is "top 5 by joint rank" on the three objectives. Note the floating-point
artifact called out in [t0102]'s `results_summary.md`: 27 cells have `dsi_vector_sum = 1.0` because
PD ≈ 0 silenced them (vector-sum DSI degenerates to 1 when PD = 0); the real DSI corner sits near
0.35 at PD ≥ 5 Hz. **Selection must filter `pd_rate_hz >= 5.0` to avoid silenced cells** when
ranking by DSI, else the top 5 will all be silent. ([t0102]).

For each selected cell, the deliverable is a 2-panel mini-figure: polar tuning + morphology. The
polar tuning is **not** in the saved JSON — `pareto_front_seedXX.json` stores only the
already-aggregated `dsi_vector_sum` scalar plus `pd_rate_hz`. There is no per-angle tuning curve in
[t0102]'s data folder. **Per-cell polar tuning requires either re-running the evaluator (out of
scope per `task_description.md`) or using DSI/PD as a two-point polar with PD at 0° and ND at
180°.** The latter is the safe choice and matches figure 4's two-point treatment.

For morphology: [t0098]'s `code/build_charts.py` (430 lines) is the canonical 2D top-down dendrogram
renderer using `generate_fixed_morphology` from
`tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix`. It monkey-patches
`ensure_t80_dll_loaded` from `t0080` and `t0090` to skip NEURON DLL loading
(`code/build_charts.py:43-53`). [t0102] already has a `code/build_morphology_charts.py` (328 lines)
that does the same monkey-patch dance — **but it slices the morphology vector as `vector_68d[:14]`
(L114), which is the wrong slice**. [t0100] corrected this bug for [t0099] by using
`vector_68d[54:]` (the morphology slice per `t0102/code/generator_wrapper.py:55`'s
`vector_68d[N_PARAMS_54:]`). The same correction must be applied here ([t0091], [t0098], [t0100],
[t0102]).

### Common pattern: monkey-patch NEURON DLL loaders when reusing `generate_fixed_morphology`

[t0098] and [t0102] both call `generate_fixed_morphology` which transitively touches
`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params.ensure_t80_dll_loaded` and
`tasks.t0090_morphology_generator_diversity_test.code.generator.ensure_t80_dll_loaded`. Both loaders
trigger NEURON `.so` / `.dll` compilation if the env has NEURON installed; for pure morphology
rendering this is unnecessary. The canonical workaround (`code/build_charts.py:43-53` in [t0098],
`code/build_morphology_charts.py:41-51` in [t0102]) is to assign `_noop_ensure_dll_loaded` to both
attributes before importing `generate_fixed_morphology`. This pattern must be replicated in this
task's figure-7 renderer ([t0098], [t0102]).

### Cross-task code reuse: morphology renderer must be copied, viz library can be imported

The Pareto-cell morphology renderer in [t0098]'s `code/build_charts.py` is **not** a registered
library — it lives in a task's `code/` directory. Per the ARF cross-task code-reuse rule, the
renderer must be **copied** into `tasks/t0105_preliminary_figures_report/code/`, not imported. The
same goes for [t0070]'s `plot_morphology.py` and `schematic_helpers.py`. Conversely,
`tuning_curve_viz` is a registered library asset ([t0011]) and **can be imported** as
`tasks.t0011_response_visualization_library.code.tuning_curve_viz.polar.plot_polar_tuning_curve`.

## Reusable Code and Assets

### `tuning_curve_viz.polar.plot_polar_tuning_curve` — import via library

* **Source**: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/polar.py` (142
  lines), entry point `plot_polar_tuning_curve` from [t0011]'s registered library asset.

* **What it does**: reads an `(angle_deg, trial_seed, firing_rate_hz)` CSV and renders a polar
  firing-rate-vs-angle plot with a red preferred-direction arrow, with an optional dashed black
  target overlay. 150 DPI, white facecolor, tight bbox.

* **Reuse method**: **import via library**.

* **Signature**:

  ```python
  def plot_polar_tuning_curve(
      curve_csv: Path,
      out_png: Path,
      *,
      target_csv: Path | None = None,
  ) -> None
  ```

* **Adaptation needed**: input data must be reshaped into the canonical CSV schema (currently the
  PD/ND-only data needs to be cast as a 2-angle CSV or supplemented with 0-fill at intermediate
  angles for visual continuity). For figure 4 a 2-angle "polar" with PD at 0° and ND at 180° is
  fine.

* **Line count**: 0 to copy (imported).

### `tuning_curve_viz.overlay.plot_multi_model_overlay` — import via library

* **Source**: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/overlay.py` (158
  lines).
* **What it does**: side-by-side Cartesian + polar overlay of up to six models with Okabe-Ito
  palette and optional dashed-black target.
* **Reuse method**: **import via library**.
* **Signature**:
  `plot_multi_model_overlay(curves_dict: dict[str, Path], out_png: Path, *, target_csv: Path | None = None) -> None`
* **Adaptation needed**: optional — useful only if figure 4 ends up overlaying Bed A and Bed B polar
  plots on one set of axes. Otherwise plain matplotlib polar suffices.
* **Line count**: 0 to copy (imported).

### `t0070/code/plot_morphology.py` — copy into task (optional)

* **Source**: `tasks/t0070_writeup_two_model_beds/code/plot_morphology.py` (388 lines) plus
  `schematic_helpers.py` (161 lines) and `constants.py` (79 lines).
* **What it does**: renders the radial-fan Bed A / Bed B morphology schematics with synapse markers.
  Outputs `bed_a_morphology.png` and `bed_b_morphology.png` to `results/images/`.
* **Reuse method**: **copy into task** (only needed if regenerating the PNGs; otherwise the existing
  PNGs in [t0070]'s `results/images/` are reused verbatim — preferred).
* **Adaptation needed**: change `IMAGES_DIR` in `paths.py` to point at
  `tasks/t0105_preliminary_figures_report/results/images/`; same for the output PNG paths.
* **Line count**: ~628 lines if copied.

### `t0098/code/build_charts.py` — copy into task with `vector_68d[54:]` correction

* **Source**: `tasks/t0098_visualise_pareto_morphologies/code/build_charts.py` (430 lines) plus
  `constants.py` (31 lines) and `paths.py` (20 lines).
* **What it does**: reads `pareto_front.json` + `anchor_tracking.json`, runs
  `generate_fixed_morphology` for each cell (monkey-patching NEURON DLL loaders), extracts
  `section_endpoints_xy`, and renders a multi-panel morphology grid plus DSI/PD bars and a scatter.
  The relevant function for this task is `_build_geometry` + `_plot_grid` (or a per-cell variant).
* **Reuse method**: **copy into task** (not a library).
* **Signature** for `_build_geometry`: `_build_geometry(*, record: CellRecord) -> CellGeometry`
  where `CellRecord.morphology_vector_14d` is the 14-d morphology slice.
* **Adaptation needed**:
  1. Change input from `pareto_front.json` (t0091 format) to `pareto_front_seed44.json` and
     `pareto_front_seed55.json` (t0102 format). The t0102 cell schema stores `vector_68d`,
     `morphology_vector_14d`, `dsi_vector_sum`, `pd_rate_hz`, `robustness` — slightly different from
     [t0091]'s schema which had a separate `anchor_tracking.json`. Either reuse
     `morphology_vector_14d` directly or recompute it from `vector_68d[54:]`.
  2. Drop `anchor_tracking.json` dependency (t0102 cells are random-init and have no anchor
     attribution); color cells by `anchor_classifier` instead, or by seed (44 vs 55).
  3. Reduce grid from 8×8 (57 cells) to a small 5-panel mini-grid for the top-5 selection.
  4. Add a polar-tuning panel beside each morphology panel (figure 7's 2-panel mini-figure spec).
* **Line count**: ~481 lines if copied, plus ~50 lines of adaptation.

### Existing PNGs reused verbatim (no code copy)

| Figure | Source PNG | Status |
| --- | --- | --- |
| 3 (Bed A morphology) | `tasks/t0070_writeup_two_model_beds/results/images/bed_a_morphology.png` | reuse verbatim |
| 3 (Bed B morphology) | `tasks/t0070_writeup_two_model_beds/results/images/bed_b_morphology.png` | reuse verbatim |
| 5 (Bed A PD overlay) | `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/three_mode_pd_overlay.png` | reuse verbatim or recompose |
| 5 (Bed A ND overlay) | `tasks/t0065_t0020_epsp_ipsp_vm_protocol/results/images/three_mode_nd_overlay.png` | reuse verbatim or recompose |
| 5 (Bed B PD overlay) | `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/three_mode_pd_overlay.png` | reuse verbatim or recompose |
| 5 (Bed B ND overlay) | `tasks/t0066_t0024_epsp_ipsp_vm_protocol/results/images/three_mode_nd_overlay.png` | reuse verbatim or recompose |
| 6 (soma sweep) | `tasks/t0067_t0065_soma_channel_addition_sweep/results/images/dsi_vs_density.png` | replot from JSON |
| 6 (Nav1.6+Kv3 rescue) | `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/results/images/dsi_rescue_curve.png` | replot from JSON |
| 6 (AIS sweep + compare) | `tasks/t0069_t0067_ais_localised_channel_sweep/results/images/{dsi_vs_density,soma_vs_ais_comparison}.png` | replot from JSON |

### Underlying CSV/JSON files (data sources for replotting)

| Figure | Path | Schema |
| --- | --- | --- |
| 4 (Bed A) | `tasks/t0046_reproduce_poleg_polsky_2016_exact/results/data/fig1_psp.csv` | 16 rows: `trial_seed,direction_label,direction_deg,exptype,...,peak_psp_mv,...` |
| 4 (Bed B) | `tasks/t0066_t0024_epsp_ipsp_vm_protocol/data/voltage_traces.csv` | 60,007 rows: `mode,direction,t_ms,v_mv` (PD/ND only) |
| 5 (Bed A) | `tasks/t0065_t0020_epsp_ipsp_vm_protocol/data/voltage_traces.csv` | 60,007 rows: `mode,direction,t_ms,v_mv` (FULL/EPSP_PASSIVE/IPSP_PASSIVE × PD/ND) |
| 5 (Bed B) | `tasks/t0066_t0024_epsp_ipsp_vm_protocol/data/voltage_traces.csv` | same schema as Bed A |
| 6 (soma sweep) | `tasks/t0067_t0065_soma_channel_addition_sweep/data/dsi_by_condition.json` | 16 conditions: `condition_id,channel,density_mS_cm2,dsi,firing_rate_pd_hz,...` |
| 6 (rescue) | `tasks/t0068_t0067_nav16_kv3_coexpression_rescue/data/dsi_by_condition.json` | 9 conditions: `condition_id,nav16_mS_cm2,kv3_mS_cm2,dsi,...` |
| 6 (AIS) | `tasks/t0069_t0067_ais_localised_channel_sweep/data/dsi_by_condition.json` | 16 conditions: `condition_id,channel,density_mS_cm2,dsi,...` |
| 7 (3-obj Pareto) | `tasks/t0102_seedscale_n4_gen20/results/data/pareto_front_seed{44,55}.json` | 60 cells total: `cell_id,vector_68d,morphology_vector_14d,dsi_vector_sum,pd_rate_hz,robustness` |

## Lessons Learned

* **Two-point polar is the only honest figure 4**: neither [t0046] nor [t0066] saved per-angle
  synaptic CSVs. [t0046] only saved PD/ND at 0°/180°; [t0066] only saved PD/ND voltage traces. Risk
  #1 in `task_description.md` materialises — label both bed polar panels as two-point and do not
  interpolate.
* **t0070 PNGs are the right reuse target for figure 3**: the radial-fan schematics are
  illustrative-not-anatomical, but `task_description.md` explicitly lists them as the figure-3
  source. Re-rendering with [t0098]'s 2D dendrogram approach would change visual style for marginal
  gain.
* **Vector-sum DSI saturates to 1.0 on silenced cells** ([t0102] `results_summary.md` lines 12-14):
  when selecting top-5 Pareto cells by DSI, the filter `pd_rate_hz >= 5.0` is mandatory. Without it,
  the top-5 will be three silenced cells with `dsi = 1.0` and `pd = 0`.
* **t0102's `build_morphology_charts.py` ships with the same `[:14]` bug t0100 fixed**: the
  morphology slice in `vector_68d` is `[54:]` per `generator_wrapper.py:55`. Reusing the t0098
  pattern is fine **as long as the slice is corrected** to `vector_68d[54:]`.
* **The DLL-loader monkey-patch is required**: [t0098] and [t0102] both monkey-patch
  `ensure_t80_dll_loaded` to a no-op before importing `generate_fixed_morphology`. Skipping the
  monkey-patch triggers NEURON `.so` compilation on first import and crashes on systems without
  NEURON installed.
* **t0070 has audited numerical values + line-level provenance for every conductance**: the Bed A
  and Bed B conductance tables in `results_detailed.md` (lines 158-169 and 452-465) are the
  authoritative source for figure 2. Every gbar / E_rev / V_half / τ has a `code/<file>:line`
  citation; no other dependency task has the same audit depth ([t0070]).
* **Library aggregator is not available in this fork**: only 8 of the standard aggregators ship.
  Library/answer/paper aggregators are absent. This forces direct filesystem enumeration of
  `assets/library/` per task — the cross-task code-reuse rule still applies (library imports OK,
  task `code/` imports forbidden).

## Recommendations for This Task

1. **Reuse [t0070]'s morphology PNGs verbatim** for figure 3. Copy `bed_a_morphology.png` and
   `bed_b_morphology.png` into `results/images/` (or reference them directly in the slide deck via
   absolute path). Do not regenerate.
2. **Reuse [t0065]'s and [t0066]'s `three_mode_*_overlay.png` PNGs verbatim** for figure 5 unless
   the deck requires a 2×2 unified layout — in that case, replot from `voltage_traces.csv` (the data
   is dense and clean).
3. **Replot figure 6 from JSON** to unify axes across [t0067], [t0068], and [t0069]. Use a 3-row
   composite (soma sweep / rescue curve / AIS sweep) with shared y-axis (DSI) and channel density on
   x.
4. **Render figure 1 (HH equations)** fresh with matplotlib mathtext, copying equation strings
   verbatim from [t0070] `results_detailed.md` lines 122-134 (Bed A) and 408-415 (Bed B). If
   mathtext glyphs render poorly, fall back to `text.usetex=True` and document the choice in
   `results_detailed.md`.
5. **Render figure 2 (conductance tables)** with `matplotlib.table.Table`. Copy values verbatim from
   [t0070]'s tables (Bed A: 11 rows, Bed B: 12 rows) and embed `code/<file>:line` provenance in the
   rightmost column.
6. **Render figure 4 as two-point polar** (PD at 0°, ND at 180°) for both beds. Label clearly as "PD
   vs ND only — full angular tuning not measured" per Risk #1 fallback. Source PSP/Vm peaks from
   [t0046]'s `fig1_psp.csv` (Bed A) and from [t0066]'s `voltage_traces.csv` peak-extraction (Bed B).
   Optionally use `plot_polar_tuning_curve` from `tuning_curve_viz` if a 2-point CSV is constructed;
   otherwise plain `matplotlib` polar suffices.
7. **Copy [t0098]'s `build_charts.py` into `tasks/t0105_preliminary_figures_report/code/` and apply
   two fixes**: (a) change the morphology slice from `[:14]` to `[54:]` (matches the [t0100]
   correction applied to [t0099]); (b) read from
   `tasks/t0102_seedscale_n4_gen20/results/data/pareto_front_seed{44,55}.json` and concatenate the
   60 cells, then filter `pd_rate_hz >= 5.0` and pick top 5 by joint rank on
   `(dsi_vector_sum, pd_rate_hz, robustness)`.
8. **Use a 2-point polar (PD/ND) for each of the 5 Pareto cells in figure 7** — per-angle tuning is
   not in saved data and re-running NEURON is out of scope. Pair each polar with the morphology
   panel rendered via the adapted `_build_geometry` + `_plot_grid` from [t0098].
9. **Skip the library aggregator step** — it is not shipped here. Document this in
   `research_code.md` (done in Library Landscape).
10. **Add `python-pptx` to `pyproject.toml`** per Risk #5 — it is not currently a project
    dependency.
11. **Add the deferred DSI+PD 2-obj panel suggestion** to `results/suggestions.json` per
    `task_description.md`: rendering this panel after [t0104] completes.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 (Poleg-Polsky 2016 DSGC)
* **Status**: completed
* **Relevance**: Bed A morphology source. Provides `assets/library/modeldb_189347_dsgc/` with
  `RGCmodel.hoc`, `main.hoc`, and `.mod` files cited throughout [t0070]'s conductance audit. The
  per-channel gbar values for figure 2 Bed A come from `main.hoc` L148-L150.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response Visualization Library
* **Status**: completed
* **Relevance**: Provides the only registered library asset relevant to this task —
  `tuning_curve_viz` with `plot_polar_tuning_curve` and `plot_multi_model_overlay` entry points.
  Import target for figures 4 and 7 polar panels.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: Bed B morphology source. Provides `code/constants.py` L34-L42 with the per-tier
  gbar values for figure 2 Bed B, and `code/build_cell.py` L140-L168 (`_map_tree`) with the
  primary/non-terminal/terminal classification used in figure 3's Bed B panel.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Reproduce Poleg-Polsky 2016 (Exact)
* **Status**: completed
* **Relevance**: Provides `results/data/fig1_psp.csv` — the only PSP-vs-direction data for Bed A.
  Confirms only PD/ND directions are available (no full tuning curve), forcing figure 4 to be a
  two-point polar.

### [t0065]

* **Task ID**: `t0065_t0020_epsp_ipsp_vm_protocol`
* **Name**: EPSP/IPSP/Vm Protocol on Bed A (t0020)
* **Status**: completed
* **Relevance**: Provides the canonical three-mode overlay PNGs for Bed A
  (`three_mode_pd_overlay.png`, `three_mode_nd_overlay.png`) — direct reuse for figure 5 Bed A
  panels. The underlying CSV `voltage_traces.csv` enables recomposition into a 2×2 layout.

### [t0066]

* **Task ID**: `t0066_t0024_epsp_ipsp_vm_protocol`
* **Name**: EPSP/IPSP/Vm Protocol on Bed B (t0024)
* **Status**: completed
* **Relevance**: Provides the matching three-mode overlay PNGs for Bed B and the underlying
  `voltage_traces.csv`. Source for figure 4 Bed B (two-point polar from PD/ND voltage peaks) and
  figure 5 Bed B panels.

### [t0067]

* **Task ID**: `t0067_t0065_soma_channel_addition_sweep`
* **Name**: Soma Channel Addition Sweep on Bed A (t0065)
* **Status**: completed
* **Relevance**: Provides `data/dsi_by_condition.json` with 16 channel-addition conditions and
  per-condition DSI values. Primary data source for figure 6 panel A (soma sweep).

### [t0068]

* **Task ID**: `t0068_t0067_nav16_kv3_coexpression_rescue`
* **Name**: Nav1.6 + Kv3 Co-expression Rescue (t0067)
* **Status**: completed
* **Relevance**: Provides `data/dsi_by_condition.json` with 9 co-expression conditions. Data source
  for figure 6 panel B (rescue curve).

### [t0069]

* **Task ID**: `t0069_t0067_ais_localised_channel_sweep`
* **Name**: AIS-localised Channel Sweep (t0067)
* **Status**: completed
* **Relevance**: Provides `data/dsi_by_condition.json` with 16 AIS-localised conditions. Data source
  for figure 6 panel C (AIS sweep + soma-vs-AIS comparison).

### [t0070]

* **Task ID**: `t0070_writeup_two_model_beds`
* **Name**: Writeup of the Two DSGC Model Beds
* **Status**: completed
* **Relevance**: Single most important dependency. Provides (a) audited HH equations in
  `results_detailed.md` lines 120-134 (Bed A) and 405-415 (Bed B) — source for figure 1; (b) audited
  conductance tables lines 158-169 and 452-465 — source for figure 2; (c) the morphology PNGs
  `bed_a_morphology.png` and `bed_b_morphology.png` — direct reuse for figure 3; (d)
  `code/plot_morphology.py` and `code/schematic_helpers.py` if morphology PNGs need to be
  re-rendered.

### [t0071]

* **Task ID**: `t0071_t0070_synaptic_eqs_pdf`
* **Name**: Typeset Synaptic Equations PDF for [t0070]
* **Status**: completed
* **Relevance**: Sibling of [t0070] that typeset the equations into `results_detailed.pdf` via
  `typst`. Not a direct figure source but a reference for equation typesetting fidelity (Risk #2
  fallback: render via PDF + rasterise if matplotlib mathtext glyphs fail).

### [t0091]

* **Task ID**: `t0091_morphology_extended_nsga2_v1`
* **Name**: Morphology-Extended NSGA-II v1
* **Status**: completed
* **Relevance**: Defines the 68-d genome schema and the 14-d morphology slice
  (`generator_wrapper.py:55` `vector_68d[N_PARAMS_54:]`). The original Pareto-front renderer in
  [t0098] was built around [t0091]'s data layout, which informs the adaptation needed for [t0102]'s
  schema.

### [t0098]

* **Task ID**: `t0098_visualise_pareto_morphologies`
* **Name**: Visualise [t0091] Pareto Morphologies
* **Status**: completed
* **Relevance**: Source of `code/build_charts.py` — the canonical Pareto-cell morphology renderer
  with `generate_fixed_morphology` + DLL-loader monkey-patch. Copy into this task's `code/` and
  adapt to read from [t0102]'s `pareto_front_seed{44,55}.json` with the `vector_68d[54:]` morphology
  slice fix.

### [t0099]

* **Task ID**: `t0099_random_init_pareto_robustness`
* **Name**: Random-init NSGA-II reproducibility test (3 seeds vs [t0091] Pareto)
* **Status**: completed
* **Relevance**: Predecessor of [t0102]; established the random-init NSGA-II pattern and was the
  first task to expose the `vector_68d[:14]` vs `vector_68d[54:]` morphology-slice bug that [t0100]
  subsequently corrected. The same fix carries over to [t0102]'s renderer.

### [t0100]

* **Task ID**: `t0100_fix_t0099_morph_charts`
* **Name**: Re-render [t0099] Morphology Charts with Correct 68-d Slice
* **Status**: completed
* **Relevance**: Confirms the morphology slice in `vector_68d` is `[54:]`, not `[:14]`. The same fix
  must be applied to [t0102]'s `build_morphology_charts.py:114` when its code is referenced.

### [t0102]

* **Task ID**: `t0102_seedscale_n4_gen20`
* **Name**: 68-d NSGA-II at GA seeds=2, N_SEEDS=4, gens=20, Random Init
* **Status**: completed
* **Relevance**: Primary data source for figure 7 (3-obj Pareto). Provides
  `results/data/pareto_front_seed{44,55}.json` with 60 cells total. The `results_summary.md` flags
  the silenced-cell DSI=1.0 artifact that must be filtered out via `pd_rate_hz >= 5.0` before
  selecting the top 5 cells.

### [t0104]

* **Task ID**: `t0104_nsga2_2obj_dsi_pdrate_3seeds`
* **Name**: 2-objective NSGA-II (DSI + PD-rate) at 3 seeds
* **Status**: in_progress
* **Relevance**: The 2-obj DSI+PD Pareto run whose output would populate the second sub-panel of
  figure 7. Because it is `in_progress`, the panel is deferred per `task_description.md`; a
  follow-up suggestion will be added to `results/suggestions.json` to render this panel after
  [t0104] completes. **Not** added as a dependency of this task per user instruction.
