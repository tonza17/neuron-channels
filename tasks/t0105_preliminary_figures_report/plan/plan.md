---
spec_version: "2"
task_id: "t0105_preliminary_figures_report"
date_completed: "2026-05-13"
status: "complete"
---
# Plan: Preliminary-Data Figure Pack and Slide Deck

## Objective

Produce a coherent preliminary-data figure pack for a written report and a presentation deck for a
direction-selective ganglion cell (DSGC) modelling project. The pack covers seven figure groups: (1)
Hodgkin-Huxley equations as a rendered PNG, (2) per-bed conductance density tables, (3) two DSGC
morphologies, (4) polar synaptic DSI panels for both model beds, (5) somatic Vm passive-and-active
three-mode overlays for both beds and both directions, (6) a unified channel-effect-on-DSI panel
across three sweeps, and (7) top-5 Pareto-cell mini-panels from the 3-objective NSGA-II run
(`t0102_seedscale_n4_gen20`). The 2-objective DSI+PD Pareto panel is deferred because its source
task `t0104_nsga2_2obj_dsi_pdrate_3seeds` is still `in_progress` — a placeholder slide is included
and a follow-up suggestion will be added. All seven PNGs land in `results/images/` and a
`python-pptx`-built deck `results/preliminary_figures_slides.pptx` embeds every PNG with a one-line
caption and a source-task citation in the slide notes. Done means: every PNG exists under
`results/images/`, the `.pptx` round-trips through `python-pptx`, every `REQ-*` item is satisfied,
and the verificator passes with zero errors.

## Task Requirement Checklist

The operative task text from `task.json` and `task_description.md` (quoted verbatim):

```text
Name: Preliminary-data figure pack and slide deck for report

Short description: Compile preliminary-data figures (HH equations PNG, conductance table,
morphologies, polar synaptic DSI, somatic Vm passive/active, channel-effect-on-DSI, 5-cell optim
panels) into PNGs + .pptx deck.

Long description (figures to produce):
1. Hodgkin-Huxley equations (PNG, not text). Render with matplotlib LaTeX/mathtext.
2. Current density table per current type, both bed models. PNG-rendered table with columns
   channel, gbar (S/cm^2), E_rev (mV), V_half_act, tau_m, V_half_inact, tau_h, source
   code/<file>:<line>. One bed per panel.
3. Morphology per bed for Bed A (t0008) and Bed B (t0024).
4. DSI as polar coordinates for synaptic currents, both beds.
5. Somatic Vm without and with action potentials, both beds, PD and ND (three-mode trio).
6. Effect of introduction of different channels on DSI (t0067, t0068, t0069 unified).
7. Optimisation: 5 cells per objective set — direction-selectivity tuning + morphology.
   7a. DSI + PD + robustness (3-obj NSGA-II) — use t0102_seedscale_n4_gen20, top 5 by joint rank.
   7b. DSI + PD (2-obj NSGA-II) — DEFERRED (t0104 in_progress). Placeholder slide + follow-up
       suggestion.

Deliverables:
* results/images/<figure_name>.png per figure.
* results/preliminary_figures_slides.pptx via python-pptx.
* results/results_detailed.md embedding every PNG with provenance.
* results/results_summary.md 2-3 paragraph abstract.
* results/metrics.json, results/costs.json (zero), results/remote_machines_used.json (empty),
  results/suggestions.json (follow-up for DSI+PD optim panel after t0104).

Out of scope: no new NEURON simulations, no new optimisation runs, no parameter re-derivation,
no changes to any other task folder.
```

Concrete requirements decomposed. Each requirement has a numeric ID (`REQ-1` ... `REQ-12`) used by
the verificator and a descriptive alias used in prose:

* **REQ-1** (alias **REQ-FIG-1**) — render a PNG with the canonical HH membrane equation plus
  per-channel current blocks for both beds. Output: `results/images/fig01_hh_equations.png`.
  Satisfied by Step 4.

* **REQ-2** (alias **REQ-FIG-2**) — render PNG tables for the conductance audit of Bed A (11 rows)
  and Bed B (12 rows) with columns Channel / `gbar` (S/cm²) / `E_rev` (mV) / `V_half_act` / `τ_m`
  / `V_half_inact` / `τ_h` / source `code/<file>:<line>`. Outputs:
  `results/images/fig02_conductance_table_bed_a.png` and
  `results/images/fig02_conductance_table_bed_b.png`. Satisfied by Step 5.

* **REQ-3** (alias **REQ-FIG-3**) — Bed A and Bed B morphology schematics. Outputs:
  `results/images/fig03_bed_a_morphology.png` and `results/images/fig03_bed_b_morphology.png`
  (copied verbatim from `tasks/t0070_writeup_two_model_beds/results/images/`). Satisfied by Step 6.

* **REQ-4** (alias **REQ-FIG-4**) — polar synaptic DSI panels for both beds, rendered as
  **two-point polar (PD at 0° + ND at 180°)** because no per-angle synaptic CSV exists in either
  dependency (confirmed in research_code.md). Labelled clearly. Outputs:
  `results/images/fig04_polar_synaptic_bed_a.png` and
  `results/images/fig04_polar_synaptic_bed_b.png`. Satisfied by Step 7.

* **REQ-5** (alias **REQ-FIG-5**) — somatic Vm three-mode overlays (EPSP_PASSIVE / IPSP_PASSIVE /
  FULL) for both beds and both directions, recomposed into a single 2×2 (bed × direction) panel.
  Output: `results/images/fig05_three_mode_overlays.png`. Satisfied by Step 8.

* **REQ-6** (alias **REQ-FIG-6**) — unified channel-effect-on-DSI figure combining t0067 (soma
  sweep), t0068 (Nav1.6+Kv3 rescue), and t0069 (AIS sweep) on shared axes by replotting from JSON.
  Output: `results/images/fig06_channel_effect_on_dsi.png`. Satisfied by Step 9.

* **REQ-7** (alias **REQ-FIG-7-3OBJ**) — top-5 Pareto cells from t0102 (3-objective NSGA-II). Each
  cell gets a 2-panel mini-figure: polar tuning + morphology. Selection rule: filter cells by
  `pd_rate_hz >= 5.0` to exclude silenced cells whose `dsi_vector_sum` degenerates to 1.0, then take
  top 5 by joint rank on `(dsi_vector_sum, pd_rate_hz, robustness)`. Output:
  `results/images/fig07_top5_pareto_3obj.png`. Satisfied by Step 10.

* **REQ-8** (alias **REQ-DECK**) — `results/preliminary_figures_slides.pptx` built via
  `python-pptx`, one figure per slide, captioned and with the source-task citation in slide notes. A
  placeholder slide for the deferred DSI+PD 2-obj panel must be included. Satisfied by Step 11.

* **REQ-9** (alias **REQ-DEFERRED-PANEL**) — explicitly add a follow-up suggestion to render the
  DSI+PD 2-obj Pareto panel once `t0104` completes. Suggestion-writing is an orchestrator step; the
  plan only records the requirement and confirms its existence in Verification Criterion 9.

* **REQ-10** (alias **REQ-RESULTS-MD**) — full writeup embedding every PNG with `![desc](...)`
  syntax, listing data provenance per figure, noting the deferred DSI+PD panel. **Orchestrator
  step**, not in `## Step by Step`.

* **REQ-11** (alias **REQ-RESULTS-SUMMARY**) — 2-3 paragraph presentation abstract. **Orchestrator
  step**, not in `## Step by Step`.

* **REQ-12** (alias **REQ-NO-EXTERNAL-CHANGES**) — no modifications outside the task folder except
  `pyproject.toml` and `uv.lock` (to add `python-pptx`). Enforced by code review and the standard
  task-isolation checks. Satisfied by Step 1 + Verification Criterion 7.

## Approach

This task is **pure plotting and compilation**: no new NEURON simulations, no new optimisation runs,
no biophysical parameter re-derivation. The implementation reuses results already produced by 13
dependency tasks (`t0008`, `t0011`, `t0024`, `t0046`, `t0065`, `t0066`, `t0067`, `t0068`, `t0069`,
`t0070`, `t0091`, `t0098`, `t0102`).

**Task type**: `data-analysis` (matches `task.json`). The `data-analysis` Planning Guidelines
require defining specific questions, listing chart types upfront, centralised paths, and reading
intermediate data with explicit dtypes — followed throughout this plan.

Key research findings driving the approach:

* **Bed A and Bed B have no per-angle synaptic CSV**. `t0046/results/data/fig1_psp.csv` contains
  only `direction_label ∈ {PD, ND}` at `direction_deg ∈ {0, 180}`.
  `t0066/data/voltage_traces.csv` contains only PD/ND traces. Therefore figure 4 is a **two-point
  polar (PD vs ND)** for both beds, labelled as such. No interpolation or extrapolation across
  intermediate angles.

* **t0070 supplies audited equation strings and conductance tables with line-level provenance**. Bed
  A HH equations live at `tasks/t0070_writeup_two_model_beds/results/results_detailed.md` L120-L134;
  Bed B at L405-L415. Bed A conductance table at L158-L169 (11 rows); Bed B at L452-L465 (12 rows).
  Every numeric value cites a `code/<file>:line` already audited by t0070 — the implementation
  copies values verbatim from t0070's markdown into the table renderer.

* **t0070 morphology PNGs are the right reuse target for figure 3**: copy `bed_a_morphology.png` and
  `bed_b_morphology.png` from `t0070/results/images/` into `results/images/`. `task_description.md`
  explicitly names them as the canonical source.

* **t0065 / t0066 three-mode overlay PNGs already exist and could be tiled verbatim**, but the
  cleanest deck layout is a single 2×2 (bed × direction) panel recomposed from
  `voltage_traces.csv` (60,007 rows × `mode/direction/t_ms/v_mv` per bed; 10 kHz × 1400 ms × 3
  modes × 2 dirs). The recomposition is cheap and gives consistent fonts and axes — choose
  recomposition.

* **Figure 6 must be replotted from JSON, not tiled from PNGs**. The three sources (`t0067`,
  `t0068`, `t0069`) each have `data/dsi_by_condition.json`; tiling raw PNGs gives mismatched axes
  (different y-ranges, marker styles, title formatting). Replotting from JSON on shared axes is
  cleaner.

* **Figure 7 selection rule**: t0102's `pareto_front_seed44.json` (29 cells) and
  `pareto_front_seed55.json` (31 cells) total 60 cells. **27 cells have `dsi_vector_sum = 1.0`
  because `pd_rate_hz ≈ 0` silenced them** (vector-sum DSI degenerates when PD ≈ 0; flagged in
  `t0102/results/results_summary.md` lines 12-14). Filter must be `pd_rate_hz >= 5.0` before
  ranking, else the top 5 will all be silenced cells.

* **Cross-task code reuse rules from the project styleguide**: `tuning_curve_viz` from
  `t0011_response_visualization_library/code/tuning_curve_viz/` is a **registered library asset**
  and can be **imported** via the absolute path
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz.polar import plot_polar_tuning_curve`.
  Conversely, `t0098/code/build_charts.py` (the canonical Pareto-cell morphology renderer) is
  **not** a library — it must be **copied** into this task's `code/` directory and adapted. Two
  fixes apply on copy: (a) change the morphology slice from `vector_68d[:14]` to `vector_68d[54:]`
  per the t0100 correction applied to t0099; (b) drop the `anchor_tracking.json` dependency and
  adapt the input schema from t0091's to t0102's `pareto_front_seed{44,55}.json`. The renderer's
  NEURON DLL-loader monkey-patch (`code/build_charts.py:43-53` in t0098: assign
  `_noop_ensure_dll_loaded` to `tasks.t0080_*.code.apply_params.ensure_t80_dll_loaded` and
  `tasks.t0090_*.code.generator.ensure_t80_dll_loaded` before importing `generate_fixed_morphology`)
  is copied verbatim — without it, NEURON `.so`/`.dll` compilation triggers on import.

* **`python-pptx` is not currently in `pyproject.toml`**. The plan adds it as a top-level dependency
  before implementation. Adding to `pyproject.toml`/`uv.lock` is the only top-level change allowed
  by Key Rule 3 in CLAUDE.md.

**Alternatives considered**:

* *Tile existing PNGs into the deck verbatim instead of recomposing.* Rejected for figures 5 and 6:
  the source PNGs have inconsistent axis ranges, fonts, and marker styles, which makes the deck look
  like a stitched collage. Recomposing from CSV/JSON gives a unified style. Figure 3 morphology PNGs
  and figure 5 raw overlays *would have been* acceptable verbatim — figure 3 PNGs are reused
  verbatim; figure 5 is recomposed to get a 2×2 layout that the source tasks did not produce.
* *Render the HH equations as a typst PDF and rasterise.* Rejected as default: keeps the pipeline
  pure-matplotlib and avoids a typst dependency. typst rendering remains the Risk #2 fallback if
  matplotlib mathtext glyphs render poorly.
* *Compute per-angle polar tuning for figures 4 and 7 by re-running NEURON.* Rejected as explicitly
  out of scope per `task_description.md` — no new NEURON simulations. Hence the two-point polar
  (PD/ND) treatment.
* *Wait for t0104 to complete and render the 2-obj panel in this task.* Rejected per user
  instruction; the deferred panel becomes a follow-up suggestion.

**Registered metrics applicable to this task**: The four registered metrics
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) all measure quantities derived from per-angle tuning curves. This task **does
not compute** any of these from scratch — it only reads aggregated values already present in
dependency tasks (e.g., `dsi_vector_sum` in t0102's Pareto JSON, which is a condensed scalar of the
same family as `direction_selectivity_index`). The implementation writes the
**`direction_selectivity_index`** values for the 5 selected Pareto cells into `results/metrics.json`
(one variant per cell, with the cell's `cell_id` as the variant key) because those values are
summary outputs of the figure pack. `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, and
`tuning_curve_rmse` are not measured here — no full angular tuning curve is computed — and are
deliberately omitted. The omission is recorded in `results/metrics.json` by simply not including
those keys; the absence is intentional and noted in this plan.

## Cost Estimation

**Total: $0.**

Itemised:

* External APIs (LLM inference, paid services): $0 — none used.
* Remote compute (GPU rental, cloud instances): $0 — no remote machines.
* Local compute: $0 — Windows workstation already paid; pure matplotlib + `python-pptx` rendering
  completes in seconds.
* Data storage / egress: $0 — all data lives inside the repository.

Budget context: project total budget is **$50** (`project/budget.json`); per-task default limit is
**$8**; alerts warn at 80% and stop at 100%. This task spends **0% of its $8 cap** and 0% of the
project total. No budget intervention required.

## Step by Step

The Step by Step covers implementation work only and ends at "compile the deck and write
`metrics.json`". Orchestrator-managed reporting steps are out of scope here per the planning
specification.

### Milestone A — Setup

1. **Add `python-pptx` to project dependencies.** Edit `pyproject.toml` and append
   `"python-pptx>=1.0"` to the `[project] dependencies` list (just below `"scikit-learn>=1.8.0"`).
   Run
   `uv run python -m arf.scripts.utils.run_with_logs --task-id t0105_preliminary_figures_report -- uv sync`
   to update `uv.lock`. Editing `pyproject.toml` and `uv.lock` is the only top-level change allowed
   by Key Rule 3. Expected: `uv.lock` updates;
   `uv run python -c "import pptx; print(pptx.__version__)"` prints a version string. Satisfies
   REQ-8 (REQ-DECK) prerequisite and REQ-12 (REQ-NO-EXTERNAL-CHANGES). Idempotent.

2. **Create `code/paths.py`** with all repository-relative path constants used downstream. Define:

   * `REPO_ROOT: Path = Path(__file__).resolve().parents[3]` (the worktree root).
   * `TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0105_preliminary_figures_report"`.
   * `RESULTS_DIR: Path = TASK_ROOT / "results"`.
   * `IMAGES_DIR: Path = RESULTS_DIR / "images"`.
   * `DATA_DIR: Path = RESULTS_DIR / "data"`.
   * `T0046_PSP_CSV: Path = REPO_ROOT / "tasks" / "t0046_reproduce_poleg_polsky_2016_exact" / "results" / "data" / "fig1_psp.csv"`.
   * `T0065_TRACES_CSV: Path = REPO_ROOT / "tasks" / "t0065_t0020_epsp_ipsp_vm_protocol" / "data" / "voltage_traces.csv"`.
   * `T0066_TRACES_CSV: Path = REPO_ROOT / "tasks" / "t0066_t0024_epsp_ipsp_vm_protocol" / "data" / "voltage_traces.csv"`.
   * `T0067_DSI_JSON: Path = REPO_ROOT / "tasks" / "t0067_t0065_soma_channel_addition_sweep" / "data" / "dsi_by_condition.json"`.
   * `T0068_DSI_JSON: Path = REPO_ROOT / "tasks" / "t0068_t0067_nav16_kv3_coexpression_rescue" / "data" / "dsi_by_condition.json"`.
   * `T0069_DSI_JSON: Path = REPO_ROOT / "tasks" / "t0069_t0067_ais_localised_channel_sweep" / "data" / "dsi_by_condition.json"`.
   * `T0070_BED_A_MORPH_PNG: Path = REPO_ROOT / "tasks" / "t0070_writeup_two_model_beds" / "results" / "images" / "bed_a_morphology.png"`.
   * `T0070_BED_B_MORPH_PNG: Path = REPO_ROOT / "tasks" / "t0070_writeup_two_model_beds" / "results" / "images" / "bed_b_morphology.png"`.
   * `T0102_PARETO_SEED44_JSON: Path = REPO_ROOT / "tasks" / "t0102_seedscale_n4_gen20" / "results" / "data" / "pareto_front_seed44.json"`.
   * `T0102_PARETO_SEED55_JSON: Path = REPO_ROOT / "tasks" / "t0102_seedscale_n4_gen20" / "results" / "data" / "pareto_front_seed55.json"`.
   * Per-figure output PNGs: `FIG01_HH_EQUATIONS_PNG`, `FIG02_TABLE_BED_A_PNG`,
     `FIG02_TABLE_BED_B_PNG`, `FIG03_BED_A_MORPH_PNG`, `FIG03_BED_B_MORPH_PNG`,
     `FIG04_BED_A_POLAR_PNG`, `FIG04_BED_B_POLAR_PNG`, `FIG05_THREE_MODE_PNG`,
     `FIG06_CHANNEL_EFFECT_PNG`, `FIG07_TOP5_PARETO_PNG`.
   * `DECK_PPTX: Path = RESULTS_DIR / "preliminary_figures_slides.pptx"`.

   Expected:
   `uv run python -c "from tasks.t0105_preliminary_figures_report.code import paths; print(paths.REPO_ROOT)"`
   prints the worktree root. Satisfies REQ-12 (REQ-NO-EXTERNAL-CHANGES) enforcement scaffolding.

3. **Create `code/constants.py`** with all named constants:

   * `DPI: int = 150`, `FACECOLOR: str = "white"`.
   * Column names for t0067/t0068/t0069 JSON: `COL_CHANNEL: str = "channel"`,
     `COL_DENSITY: str = "density_mS_cm2"`, `COL_DSI: str = "dsi"`, etc.
   * Filter constant for figure 7: `PD_RATE_MIN_HZ: float = 5.0`.
   * Figure 7 cell count: `TOP_K_PARETO_CELLS: int = 5`.
   * Polar layout constants: `PD_ANGLE_DEG: float = 0.0`, `ND_ANGLE_DEG: float = 180.0`.
   * Modes: `MODE_FULL: str = "FULL"`, `MODE_EPSP_PASSIVE: str = "EPSP_PASSIVE"`,
     `MODE_IPSP_PASSIVE: str = "IPSP_PASSIVE"`.
   * Bed labels: `BED_A_LABEL: str = "Bed A (t0008)"`, `BED_B_LABEL: str = "Bed B (t0024)"`.
   * Slide aspect: `SLIDE_WIDTH_IN: float = 13.333`, `SLIDE_HEIGHT_IN: float = 7.5` (16:9).

   No expected output beyond a successful import. Supports REQ-1 through REQ-7 by centralising
   constants used in their renderers. Satisfies styleguide "no magic strings" rule.

### Milestone B — Figure renderers

4. **Create `code/render_hh_equations.py`.** Build a single matplotlib figure with mathtext strings
   copied verbatim from t0070's audited detailed writeup at
   `tasks/t0070_writeup_two_model_beds/results/` (lines L122-L134 for Bed A and L408-L415 for Bed
   B). Lay out as a single column: Bed A block at top, Bed B block at bottom. Use
   `rcParams["text.usetex"] = False`; rely on mathtext. Save to `FIG01_HH_EQUATIONS_PNG` at 150 DPI,
   white facecolor, tight bbox. Inputs: hardcoded mathtext strings + `code/paths.py`. Outputs:
   `fig01_hh_equations.png`. Expected: PNG ~80-150 KB, no missing-glyph "tofu" boxes on visual
   inspection. Satisfies REQ-1 (REQ-FIG-1).

5. **Create `code/render_conductance_table.py`.** Embed two dataclasses
   `@dataclass(frozen=True, slots=True) class ConductanceRow` with fields `channel: str`,
   `gbar: str`, `e_rev: str`, `v_half_act: str`, `tau_m: str`, `v_half_inact: str`, `tau_h: str`,
   `source: str`. Hardcode the 11 Bed A rows (values copied verbatim from t0070's audited writeup
   under `tasks/t0070_writeup_two_model_beds/results/`, lines L158-L169) and the 12 Bed B rows
   (L452-L465). Use `matplotlib.table.Table` to render two PNGs at 150 DPI, white facecolor. Inputs:
   hardcoded rows + `code/paths.py`. Outputs: `fig02_conductance_table_bed_a.png` and
   `fig02_conductance_table_bed_b.png`. Expected: every cell visible at standard slide size; source
   column shows `code/<file>:line` for every row. Satisfies REQ-2 (REQ-FIG-2).

6. **Create `code/render_morphology.py`.** Copy the two PNGs from t0070 verbatim into
   `results/images/`. Use `shutil.copy2(src=T0070_BED_A_MORPH_PNG, dst=FIG03_BED_A_MORPH_PNG)` and
   the same for Bed B. Inputs: `T0070_BED_A_MORPH_PNG`, `T0070_BED_B_MORPH_PNG`. Outputs:
   `fig03_bed_a_morphology.png`, `fig03_bed_b_morphology.png`. Expected: byte-identical to the t0070
   source PNGs; `Path.stat().st_size` matches. Satisfies REQ-3 (REQ-FIG-3).

7. **Create `code/render_polar_synaptic.py`.** For Bed A: load
   `tasks/t0046_reproduce_poleg_polsky_2016_exact/results/data/fig1_psp.csv` with explicit dtypes
   (`trial_seed: int`, `direction_label: str`, `peak_psp_mv: float`, ...). Group by
   `direction_label ∈ {PD, ND}` and take the mean `peak_psp_mv`. Build a 2-row CSV
   `(angle_deg, trial_seed=0, firing_rate_hz=peak_psp_mv_mean)` at `PD_ANGLE_DEG` and
   `ND_ANGLE_DEG`. Save the temporary CSV to `DATA_DIR / "fig04_bed_a_polar_input.csv"` and call
   `plot_polar_tuning_curve(curve_csv=...)` from
   `tasks.t0011_response_visualization_library.code.tuning_curve_viz.polar`. For Bed B: load
   `tasks/t0066_t0024_epsp_ipsp_vm_protocol/data/voltage_traces.csv` with explicit dtypes, filter to
   `mode == "FULL"`, group by `direction ∈ {PD, ND}` and extract `v_mv.max() - v_mv.min()` as a
   peak-depolarisation proxy. Same CSV shape, save to `DATA_DIR / "fig04_bed_b_polar_input.csv"`,
   then call `plot_polar_tuning_curve` again. The title for each panel must state **"two-point polar
   — full angular tuning not measured"**. Inputs: `T0046_PSP_CSV`, `T0066_TRACES_CSV`, library
   import. Outputs: `fig04_polar_synaptic_bed_a.png`, `fig04_polar_synaptic_bed_b.png`. Expected:
   two polar plots each with two radii (PD at 0°, ND at 180°), clearly labelled as two-point.
   Satisfies REQ-4 (REQ-FIG-4).

8. **Create `code/render_three_mode_overlays.py`.** Load both `voltage_traces.csv` files (Bed A:
   `T0065_TRACES_CSV`, Bed B: `T0066_TRACES_CSV`) with explicit pandas dtypes (`mode: str`,
   `direction: str`, `t_ms: float`, `v_mv: float`). Build a 2×2 matplotlib subplot grid (rows: Bed
   A / Bed B; cols: PD / ND). For each panel, overlay three lines: `mode == "FULL"`,
   `mode == "EPSP_PASSIVE"`, `mode == "IPSP_PASSIVE"`. Use a fixed colour map:
   `{FULL: black, EPSP_PASSIVE: tab:blue, IPSP_PASSIVE: tab:red}`. X-axis: `t_ms` (0-1400 ms).
   Y-axis: `v_mv` shared across all four panels. Add a single legend in the top-right panel. Save at
   150 DPI, white facecolor. Inputs: `T0065_TRACES_CSV`, `T0066_TRACES_CSV`. Output:
   `fig05_three_mode_overlays.png`. Expected: 2×2 panel; FULL trace shows action potentials (HH
   on), passive traces are smooth EPSPs / IPSPs (HH off); curves visibly differ across PD vs ND.
   Satisfies REQ-5 (REQ-FIG-5).

9. **Create `code/render_channel_effect.py`.** Load all three JSONs via Pydantic models defined
   inline:

   ```python
   class SweepCondition(BaseModel):
       model_config = ConfigDict(extra="ignore")
       condition_id: str
       channel: str | None = None
       density_mS_cm2: float | None = None
       nav16_mS_cm2: float | None = None
       kv3_mS_cm2: float | None = None
       dsi: float | None = None
   ```

   For t0067 (soma sweep) and t0069 (AIS sweep): group conditions by `channel`, plot DSI vs
   `density_mS_cm2` per channel as one line each, with shared y-axis. For t0068 (rescue): plot DSI
   vs `nav16_mS_cm2`, colouring by `kv3_mS_cm2`. Combine into a single 1×3 or 3×1 panel figure
   (final orientation chosen at implementation and recorded in the orchestrator-managed writeup
   later). Add a unified legend and consistent y-axis range `[0, 1]`. Inputs: `T0067_DSI_JSON`,
   `T0068_DSI_JSON`, `T0069_DSI_JSON`. Output: `fig06_channel_effect_on_dsi.png`. Expected: three
   sub-panels with DSI on y, channel density on x; legend identifies channel and location (soma /
   AIS / Nav1.6+Kv3 rescue). Satisfies REQ-6 (REQ-FIG-6).

10. **Create `code/render_pareto_top5.py` by copying and adapting `t0098/code/build_charts.py`.**
    Steps:

    a.
    `shutil.copy2(src=tasks/t0098_visualise_pareto_morphologies/code/build_charts.py, dst=code/render_pareto_top5.py)`.
    Also copy the supporting `constants.py` and `paths.py` from `t0098/code/` into
    `code/_t0098_constants.py` and adapt path constants to point at this task's `IMAGES_DIR`.

    b. **Apply the t0100 fix**: replace every `vector_68d[:14]` with `vector_68d[54:]` (per
    `tasks/t0102_seedscale_n4_gen20/code/generator_wrapper.py:55` `vector_68d[N_PARAMS_54:]` and the
    t0100 correction applied to t0099).

    c. **Preserve the NEURON DLL monkey-patch verbatim** (assign `_noop_ensure_dll_loaded` to
    `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params.ensure_t80_dll_loaded` and
    `tasks.t0090_morphology_generator_diversity_test.code.generator.ensure_t80_dll_loaded`
    **before** importing `generate_fixed_morphology` from
    `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix`).

    d. **Adapt the input loader** to read `T0102_PARETO_SEED44_JSON` and `T0102_PARETO_SEED55_JSON`,
    concatenate the 60 cells, **filter `pd_rate_hz >= PD_RATE_MIN_HZ` (= 5.0)**, then select top 5
    by joint rank on `(dsi_vector_sum, pd_rate_hz, robustness)`. Use the project styleguide rank:
    convert each objective to a rank (`scipy.stats.rankdata`, all maximisation), sum, then
    ascending-sort and take 5.

    e. **Drop `anchor_tracking.json` usage** — t0102 cells are random-init with no anchor
    attribution. Colour cells by `seed` instead (44 vs 55) for visual differentiation.

    f. **Reduce the grid from 8×8 (57 cells) to a 5×2 layout** (5 cells × 2 panels each: polar +
    morphology). For the polar panel, build a 2-row CSV per cell with PD at 0° and ND at 180°
    using `pd_rate_hz` for both rows scaled by `dsi_vector_sum` (PD: full rate; ND: rate × (1 -
    dsi_vector_sum)). Call `plot_polar_tuning_curve(curve_csv=..., out_png=tmp.png)` from the t0011
    library, then composite via `matplotlib` into the final 5×2 panel.

    g. Save to `fig07_top5_pareto_3obj.png`. Inputs: `T0102_PARETO_SEED44_JSON`,
    `T0102_PARETO_SEED55_JSON`. Output: `fig07_top5_pareto_3obj.png` and a sidecar JSON
    `DATA_DIR / "fig07_top5_cells.json"` recording the selected `cell_id`s and their objective
    values (used by the metrics step). Expected: a 5×2 grid; no cell has `pd_rate_hz < 5.0`; every
    cell has a distinct morphology silhouette. Satisfies REQ-7 (REQ-FIG-7-3OBJ).

### Milestone C — Deck and metrics

11. **Create `code/build_slides.py`.** Build the deck via `python-pptx`:

    ```python
    from pptx import Presentation
    from pptx.util import Inches
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_WIDTH_IN)
    prs.slide_height = Inches(SLIDE_HEIGHT_IN)
    ```

    Add one slide per figure with the order: (1) `fig01_hh_equations.png`, (2a)
    `fig02_conductance_table_bed_a.png`, (2b) `fig02_conductance_table_bed_b.png`, (3a)
    `fig03_bed_a_morphology.png`, (3b) `fig03_bed_b_morphology.png`, (4a)
    `fig04_polar_synaptic_bed_a.png`, (4b) `fig04_polar_synaptic_bed_b.png`, (5)
    `fig05_three_mode_overlays.png`, (6) `fig06_channel_effect_on_dsi.png`, (7a)
    `fig07_top5_pareto_3obj.png`, (7b) **placeholder slide** for the deferred DSI+PD 2-obj panel
    with title "DSI+PD 2-obj Pareto (deferred — t0104 in_progress)" and body text noting the
    follow-up.

    For every slide: set a one-line caption as the slide title, embed the PNG as a centered picture,
    and add the source-task citation to `slide.notes_slide.notes_text_frame.text` (e.g., "Source:
    t0070 detailed writeup, lines L120-L134"). Save to `DECK_PPTX`. Inputs: all 10 PNGs from Steps
    4-10 + `code/paths.py`. Output: `results/preliminary_figures_slides.pptx`. Expected: 11 slides
    total; round-trip `Presentation(str(DECK_PPTX))` succeeds without exception. Satisfies REQ-8
    (REQ-DECK).

12. **Create `code/main.py` to orchestrate Steps 4-11 and compute metrics.** `main.py` calls each
    renderer's `main()` function in order, then writes the metrics file under `results/` using the
    explicit multi-variant format with one variant per selected Pareto cell from Step 10:

    ```json
    {
      "spec_version": "2",
      "variants": [
        {
          "variant_id": "<cell_id_1>",
          "metrics": {"direction_selectivity_index": <dsi_vector_sum>}
        },
        ...
      ]
    }
    ```

    Read the exact metrics schema from `arf/specifications/metrics_specification.md` before writing.
    Inputs: results of Steps 4-11 + `DATA_DIR / "fig07_top5_cells.json"`. Outputs: all 10 PNGs, the
    `.pptx`, and the metrics file. Expected: `main.py` exits 0; every PNG referenced in Step 11
    exists; the metrics file parses with Pydantic and contains exactly 5 variants. Collectively
    satisfies REQ-1 through REQ-8 by orchestrating their renderers end-to-end.

**Note on validation gates**: this task performs **no expensive operations** — no model training,
no paid API calls, no large-scale inference. Total runtime is dominated by matplotlib rendering
(estimated <5 minutes wall clock). The validation-gate requirement from the planning specification
does not apply. The closest analog is a defensive check inside `code/main.py` that aborts if any
output PNG is < 5 KB (indicating a render failure), and a sanity print of the top-5 selected
`cell_id`s to stdout so the user can confirm they look reasonable before the deck is built.

## Remote Machines

**None required.** Local Windows workstation only. The task is pure matplotlib + `python-pptx`
rendering on data already present in dependency tasks' `results/` and `data/` folders. No GPU, no
remote VM, no cloud storage.

## Assets Needed

This task consumes existing assets and data from 13 dependency tasks; it produces no new expected
typed assets (`expected_assets: {}` in `task.json`). Input dependencies:

* **Library asset (imported)**:
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`
  (`plot_polar_tuning_curve`, optionally `plot_multi_model_overlay`).

* **Result PNGs (copied verbatim)**: `t0070/results/images/bed_a_morphology.png`,
  `t0070/results/images/bed_b_morphology.png`.

* **Data CSVs / JSONs (read with explicit dtypes; not modified)**:
  `t0046/results/data/fig1_psp.csv`, `t0065/data/voltage_traces.csv`,
  `t0066/data/voltage_traces.csv`, `t0067/data/dsi_by_condition.json`,
  `t0068/data/dsi_by_condition.json`, `t0069/data/dsi_by_condition.json`,
  `t0102/results/data/pareto_front_seed44.json`, `t0102/results/data/pareto_front_seed55.json`.

* **Markdown sources (transcribed into hardcoded mathtext / table rows)**:
  `t0070/results/results_detailed.md` L120-L134, L158-L169, L405-L415, L452-L465.

* **Code (copied with adaptation)**: `t0098/code/build_charts.py` plus its `constants.py` and
  `paths.py`. Imports of `generate_fixed_morphology` from
  `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix` and the
  monkey-patched `ensure_t80_dll_loaded` attributes from `t0080` and `t0090`.

* **New top-level dependency**: `python-pptx` added to `pyproject.toml`.

## Expected Assets

`task.json` declares `expected_assets: {}` — **no new typed assets** are produced. This is a
presentation-prep task whose outputs live entirely in `results/`. The verificator will emit
`TF-W005` for "no expected assets" — this warning is expected and documented here as acceptable.

Concrete outputs produced (none are typed assets):

* `results/images/fig01_hh_equations.png` (REQ-FIG-1)
* `results/images/fig02_conductance_table_bed_a.png`,
  `results/images/fig02_conductance_table_bed_b.png` (REQ-FIG-2)
* `results/images/fig03_bed_a_morphology.png`, `results/images/fig03_bed_b_morphology.png`
  (REQ-FIG-3)
* `results/images/fig04_polar_synaptic_bed_a.png`, `results/images/fig04_polar_synaptic_bed_b.png`
  (REQ-FIG-4)
* `results/images/fig05_three_mode_overlays.png` (REQ-FIG-5)
* `results/images/fig06_channel_effect_on_dsi.png` (REQ-FIG-6)
* `results/images/fig07_top5_pareto_3obj.png` (REQ-FIG-7-3OBJ)
* `results/preliminary_figures_slides.pptx` (REQ-DECK)
* `results/data/fig07_top5_cells.json` (sidecar for top-5 selection)
* `results/metrics.json` (5 variants, one per selected Pareto cell, key
  `direction_selectivity_index`)

The orchestrator separately produces `results/results_detailed.md` (REQ-RESULTS-MD),
`results/results_summary.md` (REQ-RESULTS-SUMMARY), `results/costs.json`,
`results/remote_machines_used.json`, and `results/suggestions.json` (including the
REQ-DEFERRED-PANEL follow-up).

## Time Estimation

* Research stages (already done by upstream skills): 0 h remaining.
* Setup (Milestone A: dependency add, `paths.py`, `constants.py`): 20-30 min.
* Figure renderers (Milestone B, Steps 4-10): 1.5-2.5 h.
* Deck + metrics (Milestone C, Steps 11-12): 30-45 min.
* Verification: 10-15 min.

**Total**: 2.5-4 h wall clock, matching `task_description.md`'s 2-4 h estimate.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Bed B has no per-angle synaptic CSV; figure 4 polar would be undefined. | Confirmed (research_code.md) | Medium — would block REQ-FIG-4 if not handled | Render two-point polar (PD vs ND only) for both beds; label clearly as two-point. No simulation. |
| Matplotlib mathtext glyphs render poorly for HH equations (Greek letters, subscripts). | Medium | Low — visual quality only | Set `text.usetex=True` if a LaTeX install is available; otherwise rasterise the typst PDF from `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf` and embed as image. Document the choice in `results_detailed.md`. |
| `t0098/code/build_charts.py` uses `vector_68d[:14]` morphology slice (bug t0100 fixed for t0099). | Confirmed | High — silently wrong morphologies | Apply the t0100 fix on copy: replace every `vector_68d[:14]` with `vector_68d[54:]`. Verify by spot-checking that selected cells have visually distinct trees (Step 10). |
| Top-5 Pareto cells degenerate to silenced cells with `dsi_vector_sum = 1.0`. | Confirmed (27/60 cells affected) | High — figure 7 would be meaningless | Filter `pd_rate_hz >= 5.0` before ranking. Assert post-filter that at least 5 cells remain; if fewer, lower the threshold to 1.0 and document the change in `results_detailed.md`. |
| `python-pptx` is not in `pyproject.toml`. | Confirmed | Blocking for REQ-DECK | Add to `pyproject.toml` in Step 1 and run `uv sync`. Smoke-check via `import pptx`. |
| NEURON `.dll`/`.so` compilation triggers on import of `generate_fixed_morphology`. | Confirmed (research_code.md) | Medium — could crash on systems without NEURON | Apply the monkey-patch from `t0098/code/build_charts.py:43-53` verbatim before the import. Smoke-test the import in a one-line script before running the full renderer. |
| `t0104` completes during this task and the user wants the 2-obj DSI+PD panel inline. | Low (user already deferred) | Medium — would require re-planning | The deferred panel becomes a follow-up suggestion. If the user reverses the decision mid-task, create an intervention file under `intervention/` and pause; do not silently add `t0104` as a dependency. |
| One or more dependency tasks have a correction overlay affecting consumed PNGs / JSONs. | Low (research_code.md found none) | Medium — wrong source data | The library aggregator is not shipped; do a `Grep` for `corrections/` files in each dependency before reading its data. If any correction targets a consumed artifact, halt and create an intervention. |

## Verification Criteria

Each criterion specifies the exact command and expected output. The implementation is complete when
all eight criteria pass.

* **Plan verificator passes with zero errors.** Run:
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0105_preliminary_figures_report -- uv run python -m arf.scripts.verificators.verify_plan t0105_preliminary_figures_report`.
  Expected output: exit code 0; no `PL-E*` errors. `PL-W*` warnings are tolerable but should be
  minimal.

* **All ten PNGs exist with non-trivial size.** Run:
  `uv run python -c "from pathlib import Path; [print(p, p.stat().st_size) for p in sorted(Path('tasks/t0105_preliminary_figures_report/results/images').glob('fig*.png'))]"`.
  Expected: 10 lines (fig01, fig02_a, fig02_b, fig03_a, fig03_b, fig04_a, fig04_b, fig05, fig06,
  fig07), every file size `> 5000` bytes.

* **Deck round-trips through python-pptx.** Run:
  `uv run python -c "from pptx import Presentation; p = Presentation('tasks/t0105_preliminary_figures_report/results/preliminary_figures_slides.pptx'); print(len(p.slides))"`.
  Expected: prints `11` (one slide per figure plus the deferred-panel placeholder).

* **REQ coverage check (numeric IDs).** Run:
  `uv run python -c "import re, pathlib; p = pathlib.Path('tasks/t0105_preliminary_figures_report/plan/plan.md').read_text(encoding='utf-8'); print(sorted(set(re.findall(r'\bREQ-\d+\b', p))))"`.
  Expected: prints a list containing `REQ-1` through `REQ-12`. This satisfies the plan verificator's
  `REQ-N` coverage check.

* **REQ coverage check (named aliases).** Run:
  `uv run python -c "import re, pathlib; p = pathlib.Path('tasks/t0105_preliminary_figures_report/plan/plan.md').read_text(encoding='utf-8'); print(sorted(set(re.findall(r'REQ-[A-Z]+(?:-[A-Z0-9]+)*', p))))"`.
  Expected: includes `REQ-FIG-1`, `REQ-FIG-2`, `REQ-FIG-3`, `REQ-FIG-4`, `REQ-FIG-5`, `REQ-FIG-6`,
  `REQ-FIG-7-3OBJ`, `REQ-DECK`, `REQ-DEFERRED-PANEL`, `REQ-RESULTS-MD`, `REQ-RESULTS-SUMMARY`,
  `REQ-NO-EXTERNAL-CHANGES`.

* **Figure 7 selection respects the silenced-cell filter.** Run:
  `uv run python -c "import json; d = json.loads(open('tasks/t0105_preliminary_figures_report/results/data/fig07_top5_cells.json').read()); print(all(c['pd_rate_hz'] >= 5.0 for c in d['cells']))"`.
  Expected: prints `True` (no silenced cell selected). Confirms REQ-7 selection rule.

* **Metrics file uses only registered keys and the multi-variant format.** Run:
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0105_preliminary_figures_report -- uv run python -m arf.scripts.verificators.verify_metrics t0105_preliminary_figures_report`.
  Expected: exit code 0; the metrics file contains 5 variants, each with the key
  `direction_selectivity_index`.

* **No files outside the task folder are modified except `pyproject.toml` / `uv.lock`.** Run
  `git diff --name-only` from the worktree root. Expected output: every changed file lives under
  `tasks/t0105_preliminary_figures_report/` except `pyproject.toml` and `uv.lock`. Confirms REQ-12.

* **Markdown and Python style pass.** Run:
  `uv run flowmark --inplace --nobackup tasks/t0105_preliminary_figures_report/plan/plan.md` and
  `uv run ruff check --fix tasks/t0105_preliminary_figures_report/ && uv run ruff format tasks/t0105_preliminary_figures_report/ && uv run mypy tasks/t0105_preliminary_figures_report/`.
  Expected: zero ruff errors, zero mypy errors.

## Done-When Summary

The implementation is complete when every requirement below has a Done-when criterion satisfied:

| ID | Alias | Requirement | Step(s) | Done when |
| --- | --- | --- | --- | --- |
| REQ-1 | REQ-FIG-1 | HH equations rendered as PNG. | 4 | `fig01_hh_equations.png` exists, > 5 KB, no missing glyphs. |
| REQ-2 | REQ-FIG-2 | Bed A (11 rows) and Bed B (12 rows) conductance tables as PNGs with `code/<file>:line` source column. | 5 | Both `fig02_conductance_table_bed_*.png` files exist; every row's source column is non-empty. |
| REQ-3 | REQ-FIG-3 | Bed A and Bed B morphology PNGs (verbatim from t0070). | 6 | Both `fig03_bed_*_morphology.png` files exist; byte sizes match t0070 sources. |
| REQ-4 | REQ-FIG-4 | Two-point polar synaptic DSI for both beds, labelled as two-point. | 7 | Both `fig04_polar_synaptic_bed_*.png` files exist; titles contain the substring "two-point". |
| REQ-5 | REQ-FIG-5 | 2×2 (bed × direction) three-mode overlay with HH off for passive modes and HH on for FULL. | 8 | `fig05_three_mode_overlays.png` exists; four sub-panels each show three traces. |
| REQ-6 | REQ-FIG-6 | Unified channel-effect-on-DSI panel combining t0067, t0068, t0069 with shared y-axis. | 9 | `fig06_channel_effect_on_dsi.png` exists; three sub-panels all on `[0, 1]` y-range. |
| REQ-7 | REQ-FIG-7-3OBJ | Top-5 Pareto cells from t0102 (3-obj) as 5×2 grid; `pd_rate_hz >= 5.0` filter applied; morphology slice is `vector_68d[54:]`. | 10 | `fig07_top5_pareto_3obj.png` exists; sidecar JSON lists 5 cells, all with `pd_rate_hz >= 5.0`. |
| REQ-8 | REQ-DECK | `python-pptx` deck with 11 slides (one per figure + deferred placeholder); each slide has a caption and source citation in notes. | 1, 11 | `results/preliminary_figures_slides.pptx` opens via `Presentation(...)` and reports 11 slides. |
| REQ-9 | REQ-DEFERRED-PANEL | Follow-up suggestion to render DSI+PD 2-obj panel after t0104 completes. | Orchestrator (post-impl) | The orchestrator-written suggestions file contains a `kind: experiment` entry referencing t0104 and the DSI+PD panel. |
| REQ-10 | REQ-RESULTS-MD | Detailed writeup embedding every PNG with provenance and noting the deferred panel. | Orchestrator | The orchestrator-written detailed writeup exists and references all 10 PNGs and the deferred panel. |
| REQ-11 | REQ-RESULTS-SUMMARY | 2-3 paragraph presentation abstract. | Orchestrator | The orchestrator-written summary exists with 2-3 paragraphs. |
| REQ-12 | REQ-NO-EXTERNAL-CHANGES | No files outside the task folder are modified except `pyproject.toml` / `uv.lock`. | 1, plus Verification Criterion on `git diff` | `git diff --name-only` shows only allowed paths. |
