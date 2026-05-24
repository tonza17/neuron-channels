---
spec_version: "1"
task_id: "t0120_morph_generator_geometry_audit"
research_stage: "code"
tasks_reviewed: 14
tasks_cited: 11
libraries_found: 18
libraries_relevant: 2
date_completed: "2026-05-24"
status: "complete"
---
# Research Code: Morphology Generator Geometry Audit

## Task Objective

t0120 is a gating diagnostic task triggered by visual artefacts in t0115's
`top50_morphologies_seed9354.png` (and earlier seed-77/seed-7755 grids) where soma circles appear
disconnected from the dendrite tree. The task must sample 15-20 cells stratified across the
asymmetry-parameter extremes that drive the visual artefact (plus symmetric controls), then
empirically verify three coordinate-consistency properties on each cell: (1) every primary dendrite
section starts at `origin_xy` within float tolerance; (2) every child section's `start_xy` matches
its parent's `end_xy`; (3) NEURON `h.x3d/h.y3d` synapse-midpoint coordinates lie in the same frame
as `origin_xy` so that the moving-bar arrival-time projection `(syn_xy - origin_xy)` is computed in
a self-consistent frame. Output is one answer asset, one per-cell pass/fail CSV, one full pt3d JSON
dump per cell, and one visual diagnostic gallery. The verdict (rendering-only artefact vs real
geometry bug) gates whether every 68-d morphology-extended NSGA-II result from t0091 onward must be
re-run.

## Library Landscape

A filesystem scan of `tasks/*/assets/library/` enumerates **18** registered library assets in this
project (the library aggregator script is not present on this branch, so discovery used a direct
glob over canonical asset folders; the asset-folder layout follows
`meta/asset_types/library/specification.md`). Of these, only two are directly relevant to t0120:

* **`procedural_dsgc_morphology_generator`** v0.1.0 (created by [t0090]): pure-Python deterministic
  14-knob procedural DSGC generator. Entry points: `generate_morphology(*, params, morph_seed)`
  returning a `MorphologyResult` with `soma`, `all_dends`, `primary_dends`, `non_terminal_dends`,
  `terminal_dends`, `ais_proximal`, `ais_distal`, `terminal_locs_xy`, `origin_xy`, `connectivity`,
  and `section_endpoints_xy`. Module paths: `code/morphology_params.py`, `code/generator.py`,
  `code/verification.py`, `code/constants.py`, `code/paths.py`, `code/load_default_params.py`.
  Import via library path:
  `from tasks.t0090_morphology_generator_diversity_test.code.generator import generate_morphology`.
  This is **central** to t0120: the audit must exercise this generator and inspect both its
  Python-side `section_endpoints_xy` and the NEURON `pt3d` it emits in
  `_materialise_neuron_sections`.

* **`procedural_dsgc_morphology_generator_fix`** v0.1.0 (created by [t0092]): drop-in soma-pt3d
  patch for t0090's generator (`generate_fixed_morphology`). All NSGA-II runs from t0091 onward use
  this fixed version. Import path:
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
  **Critical for t0120**: the fix calls `h.pt3dclear()` on the soma and re-emits two pt3d points
  along the z-axis at `(0, 0, 0)` and `(0, 0, soma_diameter_um)` — which means the NEURON soma
  `pt3d` is fixed at `xy = (0, 0)` regardless of `soma_offset_pd_um`. This is the exact pattern
  t0120 must audit against, because Python `origin_xy` is set from the post-shift
  `soma_node.end_xy = (soma_offset, 0)` while the NEURON soma `pt3d` lives at the unshifted origin.

The remaining 16 libraries are NSGA-II / NEURON model ports and are not relevant to coordinate
audits: `modeldb_189347_dsgc` ([t0008]), `tuning_curve_viz` ([t0011]), `tuning_curve_loss`
([t0012]), `modeldb_189347_dsgc_gabamod` (t0020), `modeldb_189347_dsgc_dendritic` (t0022),
`de_rosenroll_2026_dsgc` (t0024), `modeldb_189347_dsgc_exact` (t0046), `minimal_dsgc_scalar_gaba`
(t0052), `minimal_dsgc_spatial_gaba` (t0053), `minimal_dsgc_ampa_nmda_scalar_gaba` (t0054),
`minimal_dsgc_mg_block_nmda` (t0055), `minimal_dsgc_tonic_gaba_sweep` (t0057),
`minimal_dsgc_bar_locked_gaba_ampa_sweep` (t0059), `dsgc_active_channel_pack` (t0074),
`de_rosenroll_2026_dsgc_ais` (t0078), `de_rosenroll_2026_dsgc_ais_dendritic_spike` (t0080). None
expose coordinate transforms, pt3d emission, or asymmetry transforms beyond what t0090/t0092 already
cover. No library has a published correction or replacement that t0120 needs.

## Key Findings

### Two coordinate frames coexist after `_apply_asymmetry`, with the soma pt3d pinned at the origin

The procedural generator in [t0090] (`generator.py` lines 333-355) applies post-hoc asymmetry
transforms that shift the soma node to `(soma_offset_pd_um, 0)` and stretch dendrite endpoints along
the PD axis. The Python-side `section_endpoints_xy` dict therefore lives in the **post-asymmetry
frame**; `MorphologyResult.origin_xy` is set from `soma_node.end_xy` after this shift
(`generator.py` line 634). The dendritic `pt3dadd` calls in `_materialise_neuron_sections` ([t0090]
`generator.py` lines 432-443) faithfully copy these shifted xy coordinates into NEURON, so
`h.x3d/h.y3d` for any dendrite section also lives in the post-asymmetry frame. **However**, the
t0092 fix (`morphology_generator_fix.py` lines 61-75) immediately calls `h.pt3dclear()` on the soma
and re-emits two pt3d points at `(0, 0, 0)` and `(0, 0, soma_diameter_um)` — fixing the
degenerate-zero-area bug but pinning the soma's NEURON xy at `(0, 0)` regardless of
`soma_offset_pd_um`. The two frames disagree on the soma alone; downstream code that reads
`h.x3d/h.y3d` for the **soma** section will see `(0, 0)`, while everything that reads
`result.origin_xy` will see `(soma_offset, 0)`. This frame split is the most plausible explanation
for both (a) the visual artefact (renderers using `origin_xy` for the soma circle but cumulative
pt3d for dendrites — though [t0115]'s actual renderer uses `section_endpoints_xy`, not pt3d) and
(b) any downstream code that mistakenly reads soma pt3d for synapse placement on the soma.

### Synapse arrival time projection uses `(syn_xy, origin_xy)` from the same coordinate convention

[t0091]'s `trial_helpers.py` lines 64-75 compute bar arrival time as the dot product of
`(syn_xy - origin_xy)` with the unit-vector bar direction. Synapse xy comes from
`_section_midpoint_xy` (lines 160-178) which reads `h.x3d(mid)` and `h.y3d(mid)`. Because all SAC
synapses are placed on **dendrites** (never on the soma in the t0091 / t0118 SAC-driven NSGA-II
protocol), `syn_xy` is in the post-asymmetry frame and `origin_xy` is also in the post-asymmetry
frame. The subtraction therefore cancels the `soma_offset` correctly. This is the analytical
justification for the brainstorm-23 preliminary verdict that NSGA-II results are likely safe even if
a soma-frame mismatch exists — but the empirical verification on extreme-asymmetry cells is what
t0120 must perform. The same `_section_midpoint_xy` is reused verbatim in [t0099], [t0112], [t0114],
[t0115], [t0118] trial helpers, so any frame bug here propagates uniformly across every
morphology-extended NSGA-II task.

### Electrical topology is `sec.connect`-based and independent of xy coordinates

In `_materialise_neuron_sections` ([t0090] `generator.py` lines 455-462), every dendrite is wired to
its parent via `child_sec.connect(parent_sec, PARENT_TIP_LOC, CHILD_BASE_LOC)`. NEURON's
`sec.connect()` is a topology operation that ignores `pt3d` coordinates; it only joins the
electrical compartments at the named fractional locations. This is why the t0092 fix can safely
re-emit the soma pt3d on the z-axis without breaking the AIS-to-soma electrical connection. For
t0120 the implication is: even if check 3 (synapse pt3d frame) fails, **check 1 and check 2 failures
cannot break electrical simulation** — they would only affect (a) any code that uses `pt3d` to
compute distances or (b) any code that visualises the cell. The synapse arrival timing is the only
electrically-relevant consumer of pt3d xy, and that lives in `trial_helpers.py` as described above.

### The visual artefact at the heart of the diversion is a rendering convention choice, not a generator bug

[t0115]'s `build_top50_morphologies.py` `_render_panel` (lines 200-234) draws each cell using
`result.origin_xy` for the soma `Circle(radius=6.0)` and `result.section_endpoints_xy` (the
Python-tree coords, **not** NEURON pt3d) for the dendrite `LineCollection(linewidths=0.4)`. Both
inputs live in the post-asymmetry frame, so the rendering is internally consistent. The visual "gap"
between soma and dendrites arises because (a) the soma circle is fixed at radius 6 um, much smaller
than typical primary stems (the brainstorm-23 logs cite `soma_diameter_um` defaults around 12-15 um,
so the circle should be radius ~6-7.5 um, but at extreme `soma_offset_pd_um` near +/-30 um the soma
and dendrite-tree centroid can be ~50 um apart in the auto-zoomed bounding box); (b) the primary
stem is drawn at linewidth 0.4 px, visually lost at 50-cell grid panel scale; (c) the auto-zoom in
lines 226-232 uses `max(x_max-x_min, y_max-y_min)*0.55 + 10.0` for the half-width, which amplifies
the perceived gap on asymmetric cells. This is consistent with what t0090's own `visualization.py`
does (lines 86-87: `ax.scatter([soma_x], [soma_y], s=20, c="black", ...)`). The t0120 gallery must
render at 2x panel size with `linewidth=2.0` for primary stems and a soma circle scaled to
`soma_diameter_um/2` to discriminate visual artefact from real disconnection.

### `section_endpoints_xy` is the canonical structural dump key, and downstream renderers strip the `_t90` suffix

The Python-tree `section_endpoints_xy` dict is keyed by the bare node name (e.g., `dend_p0_d1_n0`),
while NEURON `sec.name()` appends `_t90` ([t0090] `generator.py` lines 423-453). Three downstream
renderers ([t0090] `visualization.py` line 60-62, [t0099] `build_morphology_charts.py`, and [t0115]
`build_top50_morphologies.py` line 173-183) all strip `_t90` to match. [t0092]'s
`structural_dump.py` (lines 170-186) uses a slightly different convention: it dumps NEURON sections
directly and converts back via `str(sec.name()).replace("_t90", "")`. t0120 should reuse t0092's
pattern since it already iterates per section, collects NEURON `pt3d`, and serializes to JSON via
the `Pt3dPoint`/`SectionDump`/`CellDump` dataclass hierarchy.

### t0092 already proved that the soma pt3d is **structurally different** from the dendrite pt3d

[t0092]'s root-cause analysis is the most directly relevant prior finding: the t0090 generator was
emitting two coincident soma pt3d points at `(start_xy[0], start_xy[1], 0.0, d)` and
`(end_xy[0], end_xy[1], 0.0, d)`. For the BedB-equivalent base point both coincide at `(0, 0)`, so
the cumulative pt3d distance was ~0 and NEURON overrode `sec.L` from `soma_diameter_um` down to
~1e-9 um, collapsing the soma area to ~9.4e-14 um^2 and driving Vm to NaN within a few simulation
steps. The fix is the z-axis cylinder re-emission. **For t0120, the implication is** that t0092
established the methodology for forensically dumping per-section pt3d via `_collect_pt3d` ([t0092]
`structural_dump.py` lines 79-91) and comparing intended-vs-actual lengths via
`_pt3d_euclidean_length` (lines 94-103). t0120 should reuse these helpers verbatim (copied, not
imported across tasks per the cross-task code reuse rule).

### Pooled cells parquet from t0117 is the canonical sampling pool for stratification

[t0117] produced
`tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet` containing
4431 cells pooled across seeds 44 / 77 / 7755 / 9354 (after 6-decimal dedup) with full 68-d vectors
and DSI / PD-rate columns. The 14 morphology parameter names live in `MORPHOLOGY_PARAM_NAMES`
(constants.py lines 131-146); the asymmetry parameters relevant to t0120's stratification are
`soma_offset_pd_um` (index 5), `field_elongation_pd` (6), `branch_density_gradient_pd` (7), and
`primary_branch_pd_concentration` (8). [t0118] already demonstrated a stratified DSI x PD quintile
sampler over this exact parquet (`stratified_sample.py` `_assign_quintile` using `pd.qcut` with
`duplicates="drop"`); t0120 should adapt this pattern to stratify by per-cell asymmetry-parameter
deciles instead of (DSI, PD) quintiles.

### t0099 / t0112 / t0114 / t0115 all share an identical NEURON-DLL bypass pattern for geometry-only rendering

When the goal is geometry inspection rather than simulation, every downstream task disables the
NEURON DLL loader to avoid recompiling `nrnmech.dll`. The pattern, copied verbatim across [t0099]
`build_morphology_charts.py` (lines 38-58), [t0112], [t0114], and [t0115]
`build_top50_morphologies.py` (lines 44-59), is:

```python
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import (
    apply_params as _t80_apply_params,
)

def _noop_ensure_dll_loaded(*, h):
    return None

_t80_apply_params.ensure_t80_dll_loaded = _noop_ensure_dll_loaded
from tasks.t0090_morphology_generator_diversity_test.code import (
    generator as _t90_generator,
)
_t90_generator.ensure_t80_dll_loaded = _noop_ensure_dll_loaded
```

t0120 will need this same bypass because it only reads pt3d and `section_endpoints_xy` — no
electrical simulation is required. The bypass eliminates the t0024 + t0080 mod compilation cost,
which is significant per call on Windows.

## Reusable Code and Assets

### `generate_fixed_morphology` from `procedural_dsgc_morphology_generator_fix`

* **Source**: `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py`
  (98 lines total).
* **What it does**: builds one procedural DSGC cell from `MorphologyParams + morph_seed`, returning
  a `MorphologyResult` with the soma-area bug patched. This is the canonical entry point every
  t0091+ NSGA-II run uses.
* **Reuse method**: **import via library** (registered as
  `procedural_dsgc_morphology_generator_fix`).
* **Function signature**:
  `generate_fixed_morphology(*, params: MorphologyParams, morph_seed: int | None = None) -> MorphologyResult`.
* **Adaptation needed**: none for the API itself. t0120 must call it once per sampled cell after
  applying the NEURON DLL bypass pattern (see Common Patterns).

### `_collect_pt3d`, `_pt3d_euclidean_length`, `Pt3dPoint`, `SectionDump`, `CellDump`

* **Source**: `tasks/t0092_diagnose_morphology_generator_silence/code/structural_dump.py` (403 lines
  total; the relevant helpers and dataclasses cover ~120 lines).
* **What it does**: iterates each NEURON section, reads `h.n3d()` then walks `h.x3d(i)`, `h.y3d(i)`,
  `h.z3d(i)`, `h.diam3d(i)` for every pt3d point, then computes cumulative euclidean length and
  packs everything into frozen dataclasses with `asdict`-friendly JSON serialisation.
* **Reuse method**: **copy into task** (this is not registered as a library; t0092 keeps it as
  task-internal code per the cross-task reuse rule).
* **Function signatures**: `_collect_pt3d(*, h: Any, sec: Any) -> list[Pt3dPoint]`,
  `_pt3d_euclidean_length(*, pt3d: list[Pt3dPoint]) -> float`,
  `_section_area(*, sec: Any) -> float`,
  `_dump_one_section(*, h: Any, sec: Any, parent_name: str | None, intended_length_um: float | None) -> SectionDump`,
  `_parent_name(*, h: Any, sec: Any) -> str | None`.
* **Adaptation needed**: extend `CellDump` (or write a t0120-local variant) to also record
  `section_endpoints_xy` per section (already on the `MorphologyResult` side), the cell's
  `params.soma_offset_pd_um / field_elongation_pd / branch_density_gradient_pd / primary_branch_pd_concentration`,
  and the three boolean check results. Roughly 80-120 lines of copied + adapted code.
* **Line count to copy**: ~140 lines (the four helpers and three dataclasses plus the section-walk
  loop).

### `_section_midpoint_xy` from t0091 trial_helpers

* **Source**: `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` lines 160-178 (~19
  lines).
* **What it does**: reads `h.n3d()`, then returns the midpoint pt3d xy of a section (averaging the
  two middle points for even pt3d counts, taking the middle point for odd counts).
* **Reuse method**: **copy into task** (this is task-internal trial helper code, not a registered
  library).
* **Function signature**: `_section_midpoint_xy(*, h: Any, section: Any) -> tuple[float, float]`.
* **Adaptation needed**: none; this is exactly what t0120 needs for check 3 (synapse pt3d frame
  consistency). The function returns `(0.0, 0.0)` on degenerate `n3d() == 0` sections — t0120
  should flag this case as a check failure rather than silently using the fallback.
* **Line count to copy**: ~19 lines.

### Stratified quintile sampler pattern from t0118

* **Source**: `tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/code/stratified_sample.py`
  (~150 lines, of which `_assign_quintile` and the raster walk over `(dsi, pd)` bins are reusable).
* **What it does**: uses `pd.qcut(x=series, q=n_quintiles, labels=False, duplicates="drop")` to
  assign per-row quintile indices, then walks the cross-product bins in raster order taking one cell
  per occupied bin.
* **Reuse method**: **copy into task** (task-internal; no library).
* **Function signature**: `_assign_quintile(*, values: np.ndarray, n_quintiles: int) -> np.ndarray`.
* **Adaptation needed**: t0120 needs **decile**-based stratification on the four asymmetry
  parameters and selection of top-decile cells rather than per-bin raster walk. Roughly 30-50 lines
  of adapted code on top of the copied pattern.
* **Line count to copy**: ~50 lines.

### NEURON DLL bypass pattern

* **Source**: `tasks/t0115_seed9354_no_autostop/code/build_top50_morphologies.py` lines 42-59 (also
  in t0099 / t0112 / t0114; identical implementation).
* **What it does**: monkey-patches `ensure_t80_dll_loaded` to a no-op so morphology generation skips
  loading the t0024 + t0080 mod libraries when only geometry is needed.
* **Reuse method**: **copy into task** (the pattern is small and repeated across tasks; no library
  wraps it).
* **Line count to copy**: ~10 lines (4 lines of imports, 2 lines of `_noop_ensure_dll_loaded`
  function, 4 lines of monkey-patch assignment).

### Pooled cells parquet (sampling pool)

* **Source**:
  `tasks/t0117_pooled_pca_cluster_factor_all_cells_4_seeds/data/pooled_all_cells.parquet` (4431
  rows, 68 morphology + electrophys columns + DSI + PD + source_task + seed + generation +
  individual_idx).
* **What it does**: pooled all-cells unfiltered NSGA-II evaluations across seeds 44 / 77 / 7755 /
  9354 from t0106, t0112, t0114, t0115 after 6-decimal dedup.
* **Reuse method**: **copy into task** (data, not code; t0120 reads it via
  `pd.read_parquet(POOLED_ALL_CELLS_PARQUET)`).
* **Adaptation needed**: t0120 needs the **14-d morphology subvector** for each cell. The 14
  morphology parameter names are exposed as
  `tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants.MORPHOLOGY_PARAM_NAMES`
  — these are valid as direct column slices of the parquet.

### `_params_from_14d` constructor

* **Source**: `tasks/t0115_seed9354_no_autostop/code/build_top50_morphologies.py` lines 100-116.
* **What it does**: converts a 14-tuple of floats (the morphology slice of the 68-d vector) into a
  `MorphologyParams` dataclass, casting ints for `num_primary_branches`, `max_strahler_depth`, and
  `morph_seed`.
* **Reuse method**: **copy into task** (task-internal helper).
* **Function signature**: `_params_from_14d(*, vec: tuple[float, ...]) -> MorphologyParams`.
* **Line count to copy**: ~17 lines.

## Lessons Learned

* **Always inspect both sides of the frame split**: t0092's diagnosis succeeded because it dumped
  pt3d **and** the `section_endpoints_xy` dict, comparing intended vs actual lengths per section. An
  audit that only inspects one side cannot detect a frame mismatch. The t0092 results summary
  explicitly notes that the soma area collapsed from 287 um^2 down to 9.4e-14 um^2 — three orders
  of magnitude — which would have been invisible without the per-section dump ([t0092]).
* **The cross-task NEURON DLL bypass pattern is fragile**: t0115's renderer needed to monkey-patch
  **two** modules (`_t80_apply_params.ensure_t80_dll_loaded` AND
  `_t90_generator.ensure_t80_dll_loaded`) because the import-time side effect inside the t0090
  generator binds the original function reference. Forgetting either one re-introduces the
  compilation cost ([t0115] `build_top50_morphologies.py` lines 42-59).
* **Visual artefacts can masquerade as data bugs**: the brainstorm-23 preliminary code trace
  concluded the soma-vs-dendrite-gap is most likely a rendering choice (small soma radius, thin
  primary stem, auto-zoomed bounding box) rather than a geometry generator bug. t0120 must
  empirically confirm this rather than relying on the code trace alone — the cost is a few CPU
  hours, the cost of being wrong is re-running every t0091-t0115 NSGA-II run.
* **Determinism contract**: `generate_fixed_morphology` produces byte-identical cells for the same
  `(params, morph_seed)` pair ([t0092] `morphology_generator_fix.py` docstring lines 36-42). t0120
  can therefore re-instantiate the exact same cells that NSGA-II evaluated by passing
  `morph_seed = int(params.morph_seed)` from the parquet row.
* **`_section_midpoint_xy` silently returns `(0.0, 0.0)` for degenerate sections**: this fallback
  was added for safety but masks the very bug t0120 is auditing. The audit must explicitly check
  `n3d() > 0` before reading midpoint and flag `n3d() == 0` as a check failure ([t0091]
  `trial_helpers.py` lines 164-167).
* **`_apply_asymmetry` semantics for primary stems**: per the brainstorm-23 code trace, a primary
  stem with pre-asymmetry `start_xy = (0, 0)` ends up at
  `sx = soma_offset + elong * 0 = soma_offset` after the transform — so the primary stem **does**
  start at the shifted soma, satisfying check 1 by construction. The audit must still empirically
  confirm this rather than trusting the trace, because float-precision issues at extreme elongations
  or off-by-one iteration bugs could produce small but non-zero mismatches that compound across the
  tree.
* **The cross-task code reuse rule is strict**: tasks like [t0099], [t0112], [t0114], [t0115] all
  copied `trial_helpers.py` verbatim from [t0091] rather than importing across task code. t0120 must
  do the same for `_section_midpoint_xy`, `_collect_pt3d`, and the stratified sampler.
* **t0118 found an evaluator-disagreement bug at cell 77_15_1356**: t0117 reported DSI=0.93 but
  re-simulation under the canonical 1400 ms / -10 mV protocol returned 0 spikes (brainstorm-23
  session log). This is **orthogonal** to t0120's geometry audit, but it underlines that the same
  generator can produce subtly different results across protocol variants — t0120's audit applies
  to geometry only, not to electrical correctness, and the verdict must explicitly state that scope
  limit.

## Recommendations for This Task

### Implementation recommendations

1. **Import the generator via library**: use
   `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
   Do not call t0090's `generate_morphology` directly — every NSGA-II run from t0091 onward uses
   the patched version, so the audit must too.

2. **Apply the NEURON DLL bypass** (copy ~10 lines from [t0115]). The audit reads only `pt3d` and
   `section_endpoints_xy`; no electrical simulation is needed.

3. **Adopt t0092's `_collect_pt3d` + `Pt3dPoint`/`SectionDump`/`CellDump` dataclass hierarchy**
   (copy ~140 lines from `structural_dump.py`). Extend `SectionDump` with `start_xy_python`,
   `end_xy_python` (from `section_endpoints_xy`) and add a top-level `check_results` field with
   booleans for the three checks. Serialize the full dump per cell as
   `results/data/section_endpoints_dump.json`.

4. **Copy `_section_midpoint_xy`** from [t0091] `trial_helpers.py` and **modify** it to raise (or
   return `None`) on `n3d() == 0` instead of returning `(0.0, 0.0)`. The t0120 audit must
   distinguish "actually at the origin" from "degenerate / no pt3d".

5. **Stratification**: use [t0117]'s `pooled_all_cells.parquet` as the source. Adapt [t0118]'s
   `_assign_quintile` pattern to compute deciles on the four asymmetry parameters. Sample:
   * 3 cells with `|soma_offset_pd_um|` in top decile
   * 3 cells with `field_elongation_pd` in top + bottom deciles (1-2 each)
   * 3 cells with `|branch_density_gradient_pd|` in top decile
   * 3 cells with `primary_branch_pd_concentration` in top decile
   * 3 worst-looking cells from inspection of `top50_morphologies_seed9354.png`
   * 3-5 symmetric controls (all four asymmetry params near BEDB_BASE_POINT defaults).

6. **Per-cell check definitions** (use `math.isclose` with `abs_tol=1e-6, rel_tol=1e-9`):
   * **Check 1** (primary stem origin): for every section in `cell.primary_dends`, look up the
     `section_endpoints_xy` entry (after stripping `_t90`) and assert
     `(start_x, start_y) ≈ cell.origin_xy`.
   * **Check 2** (parent/child match): iterate every section in `cell.all_dends` with a non-None
     `connectivity[node.name]`, look up parent's `section_endpoints_xy` end and child's start,
     assert they match.
   * **Check 3** (synapse pt3d frame): for every section in `cell.all_dends`, call the modified
     `_section_midpoint_xy(h=cell.h, section=sec)`, then assert the midpoint xy lies on the line
     from the Python `start_xy` to `end_xy` of that section (use cross-product = 0 within
     tolerance), and assert the midpoint is in the same frame as `cell.origin_xy` (i.e., for a
     dendrite section, the midpoint xy should differ from `(origin_xy[0], origin_xy[1])` by no more
     than the cumulative dendrite path length from the soma — this is a coarse sanity check that
     catches a frame shift of `soma_offset` or larger).

7. **Visual gallery**: render each cell at 2x the [t0115] panel size (~5 in x 5 in per cell), with
   primary-stem linewidth 2.0, contrasting color (e.g., `tab:red`), and a soma `Circle` with
   `radius = params.soma_diameter_um / 2` rather than fixed `radius=6.0`. Add a thin debug line from
   `origin_xy` to each primary stem's `end_xy` to visually verify the connection. Save as
   `results/images/geometry_audit_gallery.png`.

8. **Per-cell pass/fail CSV** at `results/data/coordinate_consistency_checks.csv` with columns:
   `cell_id, source_task, seed, generation, individual_idx, stratum_tag, soma_offset_pd_um, field_elongation_pd, branch_density_gradient_pd, primary_branch_pd_concentration, check1_primary_start, check2_parent_child, check3_synapse_frame, max_error_um`.

9. **Sampled-cell manifest CSV** at `results/data/sampled_cell_manifest.csv` with columns:
   `cell_id, source_task, seed, generation, individual_idx, stratum_tag` + all 14 morphology
   parameter columns + DSI + PD-rate.

10. **Answer asset**: write one answer asset under
    `assets/answer/morphology-generator-geometry-consistency/` answering "Is the procedural
    morphology generator's asymmetry transform geometrically consistent across the 15-20 sampled
    cells?". Use `details.json` v2 format (matching [t0117], [t0118] precedents) with
    `answer_methods: ["code-experiment"]` and
    `source_task_ids: ["t0090_..", "t0092_..", "t0115_..", "t0117_..", "t0119_.."]`. Confidence
    should be **high** if all 60 checks pass (20 cells x 3 checks), **medium** if 1-3 isolated
    failures, **low** otherwise.

### Approaches to avoid

* **Do not import across task code directories**. [t0099], [t0112], [t0114], [t0115] all copied
  `_section_midpoint_xy` verbatim rather than importing across task code, per the cross-task reuse
  rule. t0120 must follow the same pattern.
* **Do not rely on the silent `(0.0, 0.0)` fallback** in `_section_midpoint_xy`. Modify the copy to
  raise or return `None` so degenerate sections are caught as check failures.
* **Do not skip the symmetric controls**. Even if all asymmetric cells pass, a symmetric-control
  failure would indicate a generator-level bug independent of asymmetry — the controls are the
  null hypothesis.
* **Do not test electrical correctness**. The audit's scope is geometry only. The brainstorm-23 log
  mentions cell 77_15_1356's evaluator-disagreement bug; that is a separate orthogonal issue
  ([t0118]) and t0120 must not conflate it with frame consistency.

## Common Patterns

### Path centralisation

Every prior task in this project (e.g., [t0117] `paths.py`, [t0115] `build_top50_morphologies.py`
lines 33-37) defines all paths as `pathlib.Path` constants at the top of a `paths.py` module or
file-level constants. t0120 should follow the same convention with a `tasks/t0120_*/code/paths.py`
containing `REPO_ROOT`, `TASK_ROOT`, `CODE_DIR`, `DATA_DIR`, `RESULTS_DIR`, `RESULTS_DATA_DIR`,
`RESULTS_IMAGES_DIR`, `ASSETS_DIR`, `ANSWERS_DIR`, plus per-output constants like
`SAMPLED_CELL_MANIFEST_CSV`, `COORDINATE_CONSISTENCY_CHECKS_CSV`, `SECTION_ENDPOINTS_DUMP_JSON`,
`GEOMETRY_AUDIT_GALLERY_PNG`.

### Frozen dataclasses for all structured outputs

[t0092] `structural_dump.py` (lines 39-71), [t0117] `load_pooled_cells.py` lines 53-58, and [t0118]
all use `@dataclass(frozen=True, slots=True)` for result containers. t0120 should follow the same
convention for `Pt3dPoint`, `SectionDump`, `CellDump`, `CellCheckResult`, and
`SampledCellManifestRow`.

### Headless matplotlib with `Agg` backend

[t0090] `visualization.py` lines 15-17 explicitly sets `matplotlib.use("Agg")` for Windows headless
rendering. t0120's gallery script should do the same to avoid any GUI dependency.

### Explicit pandas dtypes

[t0117] `load_pooled_cells.py` lines 149-161 (`_typed_dataframe`) applies explicit dtypes to every
column. t0120's CSV writers should do the same for the manifest and check CSVs.

## Task Index

### [t0008]

* **Task ID**: t0008_port_modeldb_189347
* **Name**: Port ModelDB 189347 DSGC to NEURON+NetPyNE
* **Status**: completed
* **Relevance**: produced the `modeldb_189347_dsgc` library, one of the 18 enumerated libraries. Not
  directly relevant to coordinate audits.

### [t0011]

* **Task ID**: t0011_response_visualization_library
* **Name**: Response visualization library
* **Status**: completed
* **Relevance**: produced the `tuning_curve_viz` library. Not directly relevant; t0120 needs
  morphology rendering, not tuning-curve rendering.

### [t0012]

* **Task ID**: t0012_tuning_curve_scoring_loss_library
* **Name**: Tuning curve scoring loss library
* **Status**: completed
* **Relevance**: produced the `tuning_curve_loss` library. Not relevant; t0120 outputs pass/fail
  checks, not loss values.

### [t0090]

* **Task ID**: t0090_morphology_generator_diversity_test
* **Name**: Procedural DSGC morphology generator + diversity test
* **Status**: completed
* **Relevance**: created the `procedural_dsgc_morphology_generator` library that t0120 audits.
  Defines `_apply_asymmetry`, `_materialise_neuron_sections`, `section_endpoints_xy`, and
  `origin_xy` — the exact functions and data structures t0120 must verify.

### [t0091]

* **Task ID**: t0091_morphology_extended_nsga2_v1
* **Name**: First 68-d morphology-extended NSGA-II run
* **Status**: completed
* **Relevance**: defines `_section_midpoint_xy` and `_bar_arrival_times` in `trial_helpers.py`.
  These are the only electrically-relevant consumers of pt3d xy. t0120 must verify that the frame
  assumption these functions rely on is empirically correct.

### [t0092]

* **Task ID**: t0092_diagnose_morphology_generator_silence
* **Name**: Diagnose t0090 procedural cell silence + soma patch
* **Status**: completed
* **Relevance**: created the `procedural_dsgc_morphology_generator_fix` library that t0120 uses as
  the canonical generator entry point. The structural_dump.py module provides the `_collect_pt3d`
  helper and dataclass hierarchy that t0120 should copy and extend. The fix itself is the root cause
  of the soma-frame split that motivated t0120.

### [t0099]

* **Task ID**: t0099_random_init_pareto_robustness
* **Name**: Random-init Pareto robustness across seeds 11/22/33
* **Status**: completed
* **Relevance**: first downstream user of `generate_fixed_morphology` for morphology rendering;
  established the NEURON DLL bypass pattern that t0120 must reuse.

### [t0112]

* **Task ID**: t0112_t0106_seed77_replicate
* **Name**: seed-77 NSGA-II replicate
* **Status**: completed
* **Relevance**: one of the four seeds in the t0117 pooled parquet; its morphology grid PNG was one
  of the cells with the visual artefact that prompted the audit.

### [t0114]

* **Task ID**: t0114_seed7755_no_autostop
* **Name**: seed-7755 NSGA-II with autostop disabled
* **Status**: completed
* **Relevance**: another of the four seeds in the t0117 pooled parquet; its
  `top50_morphologies_seed7755.png` was the first grid where the soma-disconnection visual appeared.

### [t0115]

* **Task ID**: t0115_seed9354_no_autostop
* **Name**: seed-9354 NSGA-II with autostop disabled
* **Status**: completed
* **Relevance**: explicit dependency in `task.json`. Its `top50_morphologies_seed9354.png` is the
  PNG that the researcher flagged in brainstorm-23. Its `build_top50_morphologies.py` is the
  canonical reference for the rendering convention that t0120 must improve on.

### [t0117]

* **Task ID**: t0117_pooled_pca_cluster_factor_all_cells_4_seeds
* **Name**: Pooled PCA + cluster + factor analysis across 4 seeds, unfiltered
* **Relevance**: produced the `pooled_all_cells.parquet` (4431 cells) that t0120 uses as the
  sampling pool. Defines `MORPHOLOGY_PARAM_NAMES` and `ALL_PARAM_NAMES` constants. Its
  `_assign_quintile` pattern is reused for decile-based stratification.
* **Status**: completed

### [t0118]

* **Task ID**: t0118_resimulate_t0117_cluster_samples_ge_gi_vm
* **Name**: Re-simulate t0117 cluster samples for g_E / g_I / Vm
* **Status**: completed
* **Relevance**: most recent task to instantiate cells from the t0117 parquet for further
  inspection. Demonstrates the stratified sampling pattern (DSI x PD quintiles) and the SAC synapse
  placement protocol that t0120's check 3 must validate the frame assumption for.
