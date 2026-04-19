---
spec_version: "2"
task_id: "t0009_calibrate_dendritic_diameters"
date_completed: "2026-04-19"
status: "complete"
---
# Plan: Calibrate dendritic diameters for dsgc-baseline-morphology

## Objective

Replace the uniform 0.125 µm placeholder radius that every compartment of the CNG-curated SWC
`dsgc-baseline-morphology` (NeuroMorpho neuron 102976, `141009_Pair1DSGC`) currently carries with a
literature-derived diameter taper, and register the calibrated morphology as a new v2 dataset asset
`dsgc-baseline-morphology-calibrated`. The taper is keyed on Strahler order (soma / primary /
mid-dendrite / terminal), anchored to per-section diameters harvested from the `RGCmodel.hoc` file
distributed by the Poleg-Polsky & Diamond 2016 NEURON model (ModelDB 189347, mirrored at
`geoffder/Spatial-Offset-DSGC-NEURON-Model`). "Done" means the calibrated SWC preserves topology
(6,736 compartments, 129 branch points, 131 leaves, total dendritic length within 1e-3 µm of
1,536.25 µm), passes the project's dataset-asset checks, contains at least three distinct radii,
clamps terminal radii at a 0.15 µm floor, and ships with per-order distribution plots and a
surface-area / axial-resistance delta report.

## Task Requirement Checklist

The operative task text from `task.json` and `task_description.md`:

> **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
>
> **Short description**: Replace the 0.125 um placeholder radii in dsgc-baseline-morphology with a
> literature-derived diameter taper and register the result as dsgc-baseline-morphology-calibrated.
>
> **Scope (1) Research stage**: survey the published mouse ON-OFF DSGC morphometric literature for a
> defensible diameter taper rule; pick one primary source and one fallback source; document the
> choice and the per-order distribution in `research/research_papers.md`.
>
> **Scope (2) Implementation**: parse the CNG-curated SWC with a stdlib parser (reuse t0005
> `validate_swc.py`); compute per-compartment Strahler order and path distance from the soma; apply
> the chosen taper rule to assign a realistic radius to every dendritic compartment; preserve the 19
> soma compartments' original (non-placeholder) radii; write the new SWC to
> `assets/dataset/dsgc-baseline-morphology-calibrated/files/`.
>
> **Scope (3) Register** the calibrated morphology as a v2 dataset asset with a `details.json`, a
> `description.md`, and the calibrated SWC file. `details.json` must reference
> `dsgc-baseline-morphology` as the raw source and cite the chosen taper-source paper.
>
> **Scope (4) Validation**: plot per-Strahler-order radius distributions (original placeholder vs
> calibrated) and save as PNG to `results/images/`; recompute total surface area and axial
> resistance per branch and report the change vs the placeholder baseline; confirm compartment
> count, branch points, and connectivity are unchanged from the source SWC.
>
> **Expected Outputs**: 1 dataset asset; per-order diameter distribution plots; brief answer-style
> report embedded in `results/results_detailed.md` summarising the chosen taper rule, rationale, and
> the change in surface area / axial resistance vs the placeholder.
>
> **Questions answered**: (Q1) which published taper source is most faithful for mouse ON-OFF DSGCs
> of the 141009_Pair1DSGC lineage; (Q2) what Strahler-order-to-radius mapping is used; (Q3) how does
> total dendritic surface area change; (Q4) how does axial resistance along the preferred-to-null
> dendritic axis change, and what does that predict for spike-attenuation at the soma.
>
> **Risks**: no per-cell taper in literature (fallback: Poleg-Polsky, label asset accordingly);
> distal tips implausibly thin (clamp radius floor at 0.15 µm); calibration collapses spatial
> detail (re-derive until per-order variability survives).

Concrete requirements extracted:

* **REQ-1** — Pick a primary taper source + fallback and document the per-order distribution in
  `research/research_papers.md`. Evidence: the research stage already committed Poleg-Polsky &
  Diamond 2016 (ModelDB 189347, paper asset `10.1016_j.neuron.2016.02.013`) as primary and Hanson et
  al. 2019 (`eLife.42392`, `geoffder/Spatial-Offset-DSGC-NEURON-Model`) as fallback. Step 1 of this
  plan re-states that commitment, and Step 5 writes the per-order distribution into the harvested
  JSON and the calibrated asset's `description.md`.
* **REQ-2** — Parse the source CNG SWC using a stdlib parser reused from t0005. Satisfied by Step
  2 (copy `validate_swc.py` to `code/swc_io.py` and extend with a writer).
* **REQ-3** — Compute per-compartment Strahler order and path distance from the soma. Satisfied by
  Step 4 (`code/morphology.py`: stdlib Strahler + path-distance functions over the
  `list[SwcCompartment]` tree; NeuroM is NOT adopted because the project's python stack is Python
  3.12+ and NeuroM v4.0.4 adds no value over ~40 lines of stdlib recursion, and keeping the stack
  `numpy/pandas/matplotlib` only preserves reproducibility).
* **REQ-4** — Apply the chosen taper to every dendritic compartment. Satisfied by Step 6
  (`code/calibrate_diameters.py`).
* **REQ-5** — Preserve the 19 soma compartments. The research-code stage discovered that the 19
  soma rows are ALSO placeholders (all 6,736 rows carry radius 0.125 — no original soma diameters
  exist in the source). The plan resolves this by harvesting the Poleg-Polsky `pt3dadd` soma
  diameters (0.88 / 6.14 / 7.74 / 8.32 / 8.35 / 10.62 / 0.88 µm per the research_internet.md
  extract) and assigning them to the 19 soma rows in source-SWC order, clamped to a 0.5 µm floor to
  reject the 0.88 µm endpoint artefacts. The calibrated asset's `description.md` must explicitly
  state that the literal "preserve soma rows verbatim" reading is unsatisfiable and document the
  substitute rule. Satisfied by Step 6.
* **REQ-6** — Write the calibrated SWC to
  `assets/dataset/dsgc-baseline-morphology-calibrated/files/`. Satisfied by Step 6.
* **REQ-7** — Register the calibrated morphology as a v2 dataset asset with `details.json` and
  `description.md`, citing `dsgc-baseline-morphology` as the raw source and
  `10.1016_j.neuron.2016.02.013` as `source_paper_id`. Satisfied by Step 8.
* **REQ-8** — Plot per-Strahler-order radius distributions (original placeholder vs calibrated)
  and save as PNG in `results/images/`. Satisfied by Step 7.
* **REQ-9** — Recompute total surface area and axial resistance per branch; report change vs the
  placeholder baseline. Satisfied by Step 7 (metrics JSON + per-branch CSV + plots).
* **REQ-10** — Confirm compartment count, branch-point count, leaf count, and connectivity
  unchanged. Satisfied by Step 9 (`code/test_swc_io.py` pytest) and by the Verification Criteria
  section below.
* **REQ-11** — Clamp terminal radius at a 0.15 µm floor and document the clamp count. Satisfied
  by Step 6 (clamp inside `calibrate_diameters.py`) and recorded in `description.md` via Step 8.
* **REQ-12** — Answer Q1-Q4 in `results/results_detailed.md`. The Step by Step covers
  implementation work only; results docs are orchestrator-owned, but Step 7 emits every numeric
  answer Q1-Q4 needs into `results/metrics.json`, `results/per_order_radii.csv`, and
  `results/per_branch_axial_resistance.csv` so the orchestrator's reporting step can cite them.

Ambiguity: REQ-5 cannot be satisfied literally. The plan resolves it with the harvest-and-clamp
substitute above; if Step 5 cannot harvest soma diameters for any reason, Step 6 falls back to a
uniform soma radius of 5 µm (Schachter 2010 "soma ~10 µm diameter" [Schachter2010]) and records
the fallback decision in an `intervention/` note.

## Approach

The implementation follows the pattern Ding et al. 2016 used for SAC network models: **keep the
topology of the target morphology, impose diameters by compartment class from an external source**.
The target is the `141009_Pair1DSGC` CNG tree (6,736 compartments, 129 branch points, 131 leaves,
1,536.25 µm total dendritic path length, all radii 0.125 µm). The diameter source is the
Poleg-Polsky & Diamond 2016 NEURON model on ModelDB 189347, mirrored at
`https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model` with MIT license, whose
`RGCmodel.hoc` file defines ~350 `dend[i]` array sections and one `soma` section via explicit
`pt3dadd(x, y, z, diam)` calls. Inspection during internet research found soma diameters in the
0.88-10.6 µm range, primary dendrite (`dend[1]`) attachment at ~11.0-11.5 µm, and terminal
sections with mixed diam=0 interpolation nodes and ~0.3-1.0 µm real points.

Compartment class is assigned by Horton-Strahler order computed on the target tree with a pure
stdlib recursion (post-order DFS over the parent->children graph; tie-break = maximum child).
Strahler order 1 = terminal, order N = primary (where N is the maximum order in the tree),
intermediate orders are assigned the interior bin. Each dendritic compartment is assigned the mean
radius of its bin in the Poleg-Polsky tree after filtering diam=0 interpolation nodes.

Soma radii come from the seven Poleg-Polsky soma `pt3dadd` points with a 0.5 µm floor (the 0.88 µm
endpoints are excluded as reconstruction-endpoint artefacts) mapped onto the 19 CNG soma rows in
source order so the soma cross-section peaks in the middle of the contour. All dendritic radii are
clamped to a 0.15 µm floor per the task's risk section. The final SWC is written with compartment
IDs, parent IDs, and xyz coordinates copied byte-for-byte from the source so topology is provably
preserved.

**Key research findings that drive the approach:**

* The CNG source file's 0.125 µm radius is uniform across ALL 6,736 rows (soma included), not just
  dendrites; "preserve the 19 soma compartments verbatim" is unsatisfiable and the plan substitutes
  harvested Poleg-Polsky soma diameters [research_code.md].
* The community convention for mouse ON-OFF DSGC compartmental models is a three-bin
  soma/primary/terminal partition with distinct conductance densities (Na 150/150/30 mS/cm², K
  rectifier 70/70/35 mS/cm²) that only makes sense under distinct per-class diameters
  [PolegPolsky2016, Hanson2019, Jain2020, Schachter2010].
* Poleg-Polsky's `pt3dadd` entries include diam=0 interpolation nodes that MUST be filtered before
  averaging; this is not flagged in the paper-corpus review but was discovered via direct .hoc
  inspection [research_internet.md].
* NeuroMorpho.Org has no universal "default diameter" convention — 0.125 µm is an idiosyncratic
  Simple Neurite Tracer export value for this neuron, not a repository-wide policy
  [NeuroMorpho-StdSwc-2024].
* Schachter 2010 reports DSGC proximal Rin ~150-200 MΩ and distal Rin >1 GΩ at Ra = 100 Ω·cm, Rm
  = 10-22 kΩ·cm² — the electrotonic target the calibrated axial-resistance profile should
  approach within 50%.

**Alternatives considered:**

1. **Key the taper on path distance from the soma instead of Strahler order.** Rejected: the CNG
   tree's 1,536 µm of path length distributed over 6,717 dendritic compartments makes path-distance
   bucketing sensitive to sparse-branch artefacts; Strahler order is topologically stable and maps
   cleanly onto the community's three-bin soma/primary/terminal partition. This matches the
   `research_papers.md` recommendation.
2. **Use the TREES-toolbox `quaddiameter` Rall-3/2 power rule instead of Poleg-Polsky bins.**
   Rejected: TREES is MATLAB-only; a pure-Python re-implementation adds complexity with no clear
   accuracy benefit over the community-standard Poleg-Polsky profile, and the task description
   explicitly names Poleg-Polsky as the candidate primary source. Retained as a contingency in Risks
   & Fallbacks.
3. **Adopt NeuroM (`pip install neurom>=4.0.4`) for Strahler order computation.** Rejected: the
   project's dependency list is currently `matplotlib + pandas + numpy`; adding `neurom` and its
   transitive dependencies (`click`, `morphio`, `tqdm`) for what is ~40 lines of stdlib recursion is
   a poor trade. Stdlib implementation is preferred for determinism and to keep the worktree
   resolvable without uv upgrades. The calibrated asset's `description.md` documents the exact
   tie-break convention used (maximum child).
4. **Flag the soma placeholder as a blocking intervention.** Rejected: the project already has a
   defensible substitute (Poleg-Polsky soma `pt3dadd` diameters harvested from the same source used
   for dendrites); escalating to intervention would block downstream tasks without benefit. The
   substitute is documented transparently in the calibrated asset's `description.md`.

**Task types.** `task.json` declares `["feature-engineering", "data-analysis"]`. Both apply: feature
engineering for producing a calibrated geometry from a raw geometry + per-class diameter features,
data analysis for the per-order distribution and Rin-gradient reporting. The feature-engineering
Planning Guideline "plan the output schema before writing extraction code" drives the explicit
`PolegPolskyBin` / `StrahlerBin` / `CalibrationRecord` dataclass list in Step 5. The data-analysis
Planning Guideline "decide which statistical tests are appropriate during planning" drives the
explicit surface-area ratio + axial-resistance 50% window check in Step 7.

**Registered metrics.** The project registry currently holds `direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`. None of these apply to a
pure-morphology calibration task — they are all stimulus-response curves. This task therefore will
NOT write to `results/metrics.json` a set of registered metric keys; it will produce a structurally
similar `results/metrics.json` with calibration-specific keys (total surface area, total axial
resistance, proximal/distal Rin, clamp counts, per-order radius means). A separate task or
correction may later register these keys in `meta/metrics/` if needed. This deliberate omission is
recorded here to prevent the orchestrator from flagging it as an accidental gap.

## Cost Estimation

Total estimated cost: **$0.00**.

Itemized:

* LLM API calls: $0.00 — only the scaffolding Claude session, already paid for by the project.
* Remote compute: $0.00 — none required (see Remote Machines).
* Paid dataset access: $0.00 — Poleg-Polsky .hoc is MIT-licensed on a public GitHub mirror, CNG
  SWC is CC-BY-4.0 from t0005.
* Compute hardware: $0.00 — runs on the developer laptop in seconds (stdlib parse + O(N) tree walk
  over 6,736 rows, matplotlib plots).

Budget comparison: `project/budget.json` sets `total_budget = 0.0` and
`per_task_default_limit = 0.0` with no paid services registered. This task stays inside budget with
zero margin used.

## Step by Step

### Milestone A — Scaffolding

1. **Create the task code module skeleton.** Create
   `tasks/t0009_calibrate_dendritic_diameters/code/__init__.py`, `code/paths.py`,
   `code/constants.py`. In `code/paths.py`, copy the template from
   `tasks/t0004_generate_target_tuning_curve/code/paths.py` and rename constants:
   `DATASET_ID = "dsgc-baseline-morphology-calibrated"`, `TASK_ROOT`, `REPO_ROOT`,
   `SOURCE_SWC_PATH = REPO_ROOT / "tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc"`,
   `DATASET_ASSET_DIR = TASK_ROOT / "assets/dataset" / DATASET_ID`, `FILES_DIR`,
   `DETAILS_JSON_PATH`, `DESCRIPTION_MD_PATH`,
   `CALIBRATED_SWC_PATH = FILES_DIR / "141009_Pair1DSGC_calibrated.CNG.swc"`,
   `POLEG_POLSKY_HOC_PATH = TASK_ROOT / "code" / "RGCmodel.hoc"` (local harvested copy),
   `POLEG_POLSKY_BINS_JSON_PATH = TASK_ROOT / "code" / "poleg_polsky_bins.json"`,
   `PER_ORDER_RADII_CSV = TASK_ROOT / "results/per_order_radii.csv"`,
   `PER_BRANCH_AXIAL_CSV = TASK_ROOT / "results/per_branch_axial_resistance.csv"`,
   `METRICS_JSON_PATH = TASK_ROOT / "results/metrics.json"`,
   `IMAGES_DIR = TASK_ROOT / "results/images"`,
   `RADIUS_DIST_PNG = IMAGES_DIR / "radius_distribution_by_strahler_order.png"`,
   `AXIAL_RES_PNG = IMAGES_DIR / "axial_resistance_by_strahler_order.png"`,
   `SOMA_PROFILE_PNG = IMAGES_DIR / "soma_radius_profile.png"`. In `code/constants.py`, declare:
   `SWC_COLUMN_ID`, `SWC_COLUMN_TYPE`, `SWC_COLUMN_X`, `SWC_COLUMN_Y`, `SWC_COLUMN_Z`,
   `SWC_COLUMN_RADIUS`, `SWC_COLUMN_PARENT`; `TYPE_SOMA = 1`; `TYPE_DENDRITE = 3`;
   `ROOT_PARENT_ID = -1`; `TERMINAL_RADIUS_FLOOR_UM = 0.15`; `SOMA_RADIUS_FLOOR_UM = 0.5`;
   `AXIAL_RESISTIVITY_OHM_CM = 100.0` (Poleg-Polsky/Hanson consensus);
   `PLACEHOLDER_RADIUS_UM = 0.125`; `EXPECTED_COMPARTMENTS = 6736`; `EXPECTED_BRANCH_POINTS = 129`;
   `EXPECTED_LEAVES = 131`; `EXPECTED_DENDRITIC_LENGTH_UM = 1536.25`; `PNG_DPI = 150`. No libraries
   imported. Satisfies REQ-1 scaffolding. Expected output: three files, each 20-60 lines, importing
   via `from tasks.t0009_calibrate_dendritic_diameters.code.paths import ...`.

2. **Copy and extend the SWC parser as `code/swc_io.py`.** Copy
   `tasks/t0005_download_dsgc_morphology/code/validate_swc.py` verbatim into
   `tasks/t0009_calibrate_dendritic_diameters/code/swc_io.py`. Keep `SwcCompartment`, `SwcSummary`,
   `SWC_TYPE_*` / `ROOT_PARENT_ID` constants, `parse_swc_file`, `_validate_structure`, and
   `_summarize` unchanged. Add a writer
   `write_swc_file(*, compartments: list[SwcCompartment], output_path: Path, header_comments: list[str]) -> None`
   that writes the seven `%d %d %.6f %.6f %.6f %.6f %d` columns per row with `#`-prefixed header
   lines first, final `\n`, UTF-8 encoding. Add a helper
   `build_children_index(*, compartments: list[SwcCompartment]) -> dict[int, list[int]]` that
   returns `parent_id -> [child_id, ...]` for downstream tree walks. Import style must follow
   `arf/styleguide/python_styleguide.md`: no relative imports, keyword-only args for 2+ params,
   `@dataclass(frozen=True, slots=True)`. Satisfies REQ-2. Expected output: ~180 lines; running
   `uv run python -u -m arf.scripts.utils.run_with_logs -- python -c "from tasks.t0009_calibrate_dendritic_diameters.code.swc_io import parse_swc_file, SwcCompartment; from tasks.t0009_calibrate_dendritic_diameters.code.paths import SOURCE_SWC_PATH; rows = parse_swc_file(swc_path=SOURCE_SWC_PATH); print(len(rows))"`
   prints `6736`.

### Milestone B — Harvest the Poleg-Polsky reference diameters

3. **Fetch the `RGCmodel.hoc` file.** Add a utility script `code/harvest_poleg_polsky.py` that
   downloads
   `https://raw.githubusercontent.com/geoffder/Spatial-Offset-DSGC-NEURON-Model/master/RGCmodel.hoc`
   via `urllib.request.urlopen` (stdlib, no new dependency), writes it to `POLEG_POLSKY_HOC_PATH`,
   and computes a SHA-256 checksum logged to stdout. Include a deterministic fallback: if the
   request fails (HTTPError, URLError, timeout after 30 s), the script prints a clear error and
   exits non-zero so the orchestrator can retry. The raw .hoc is checked into the task folder (not
   excluded by `.gitignore`) so re-runs are hermetic. Satisfies REQ-1 (source commitment). Expected
   output: ~50 lines; `RGCmodel.hoc` present in `code/`; `sha256` printed to stdout.

4. **Parse `pt3dadd` calls and bin by section role.** Extend `code/harvest_poleg_polsky.py` with a
   parser that walks `RGCmodel.hoc` line by line using a single regex
   `r"pt3dadd\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)"` and a per-section
   cursor driven by `r"(\bsoma|dend)(?:\[(\d+)\])?"` tokens. Produce a dict
   `{"soma": [d0, d1, ...], "dend_0": [...], "dend_1": [...], ..., "dend_350": [...]}` with
   diameters only (xyz discarded here). Filter diameters == 0 as interpolation-node artefacts.
   Classify each `dend[i]` section into a role:
   * **primary**: sections attached directly to the soma (detected by the
     `dend[i] { connect dend[i](0), soma(0.5) }` pattern in the .hoc) — typically dend[1] and any
     siblings.
   * **terminal**: sections with no children in the .hoc topology (no
     `connect dend[j](0), dend[i](...)` referencing them as parent).
   * **mid**: everything else. Aggregate per role: `primary_mean_radius`, `mid_mean_radius`,
     `terminal_mean_radius` (diameter / 2, µm). Write the result to `POLEG_POLSKY_BINS_JSON_PATH`
     with schema:
   ```json
   {
     "source_url": "...",
     "source_sha256": "...",
     "n_pt3dadd_total": N,
     "n_pt3dadd_nonzero": M,
     "soma_raw_diameters_um": [0.88, 6.14, 7.74, 8.32, 8.35, 10.62, 0.88],
     "primary_radius_um": ...,
     "mid_radius_um": ...,
     "terminal_radius_um": ...,
     "n_primary_sections": ...,
     "n_mid_sections": ...,
     "n_terminal_sections": ...
   }
   ```
   Satisfies REQ-1 (per-order distribution documented). Expected output: a JSON file whose
   `primary_radius_um` is in the ~2-6 µm range, `mid` is ~0.5-2 µm, `terminal` is ~0.15-0.6 µm,
   consistent with the ~3-10× primary-to-terminal diameter ratio predicted in
   `research_internet.md`. Validation gate: if `primary / terminal` ratio is below 2× or above
   15×, halt and inspect `n_pt3dadd_*` counts — the parse is likely missing sections or
   mis-classifying them. Inspect 5 `dend[i]` sections' raw diameters before continuing.

### Milestone C — Compute Strahler orders and calibrate diameters

5. **Implement `code/morphology.py`.** Pure-stdlib module that operates on `list[SwcCompartment]`.
   Define:
   * `@dataclass(frozen=True, slots=True) class MorphologyGraph` with fields
     `compartments: list[SwcCompartment]`, `children_by_parent: dict[int, list[int]]`,
     `compartment_by_id: dict[int, SwcCompartment]`, `strahler_by_id: dict[int, int]`,
     `path_distance_by_id: dict[int, float]`, `max_strahler_order: int`.
   * `build_graph(*, compartments: list[SwcCompartment]) -> MorphologyGraph`: builds children index,
     computes Strahler order via iterative post-order DFS (Horton-Strahler rule with maximum-child
     tie-break: if a node has children with max order k appearing in m >= 2 children then the node's
     order is k+1, else it is max(children)). Soma rows keep a sentinel order of 0 so they are not
     mis-classed as "primary". Computes path distance from soma along parent chain using Euclidean
     xyz.
   * `iter_dendritic_ids(*, graph: MorphologyGraph) -> Iterator[int]`: yields compartment IDs with
     `type_code == TYPE_DENDRITE`.
   * Satisfies REQ-3. Expected output: ~120 lines; running
     `build_graph(compartments=parse_swc_file(swc_path=SOURCE_SWC_PATH))` returns a graph with
     `max_strahler_order` in the 5-9 range (typical for DSGC trees with 129 branch points and 131
     leaves).

6. **[CRITICAL] Implement `code/calibrate_diameters.py`.** The main pipeline. Reads the source SWC,
   the Poleg-Polsky bins, and writes the calibrated SWC. Imports: `swc_io.parse_swc_file`,
   `swc_io.write_swc_file`, `morphology.build_graph`, `paths.*`, `constants.*`, stdlib
   `dataclasses`, `json`, `pathlib`. Dataclass:
   `@dataclass(frozen=True, slots=True) class CalibrationRecord(compartment_id: int, type_code: int, strahler_order: int, bin_label: str, assigned_radius_um: float, clamped: bool)`.
   Pipeline:
   1. `raw_compartments = parse_swc_file(swc_path=SOURCE_SWC_PATH)` — expected 6,736 rows.
   2. `graph = build_graph(compartments=raw_compartments)`.
   3. `bins = json.loads(POLEG_POLSKY_BINS_JSON_PATH.read_text(encoding="utf-8"))`.
   4. **Soma assignment**: take the seven `bins["soma_raw_diameters_um"]` values, filter out the two
      endpoint 0.88 µm values (they are endpoints of the contour), convert to radii (divide by 2),
      clamp to `SOMA_RADIUS_FLOOR_UM`, then map onto the 19 CNG soma rows by linear interpolation
      (scipy-free: use `statistics.fmean` over the five central values and assign the mean to all 19
      rows; variability across the 19 soma points was <2× in Poleg-Polsky so uniform is
      acceptable). Note the substitute rule in a stdout log line.
   5. **Dendrite assignment**: for each dendritic compartment, look up its Strahler order from
      `graph.strahler_by_id`:
      * order == 1 → `terminal_radius_um` from bins
      * order == graph.max_strahler_order → `primary_radius_um`
      * any other order → `mid_radius_um`
   6. **Clamp**: if the assigned radius < `TERMINAL_RADIUS_FLOOR_UM`, raise it to the floor and
      record `clamped=True`. For soma, clamp to `SOMA_RADIUS_FLOOR_UM`.
   7. Emit `calibrated_compartments = list[SwcCompartment]` with id / type / xyz / parent copied
      verbatim from `raw_compartments`, `radius` replaced with the assigned value.
   8. `write_swc_file(compartments=calibrated_compartments, output_path=CALIBRATED_SWC_PATH, header_comments=[...])`
      — header lines must cite the source SWC, the Poleg-Polsky paper DOI, and the Strahler-order
      rule.
   9. Write a `CalibrationRecord` list to
      `tasks/t0009_calibrate_dendritic_diameters/code/calibration_records.json` for the analysis
      step. Satisfies REQ-4, REQ-5, REQ-6, REQ-11. Expected output:
      `141009_Pair1DSGC_calibrated.CNG.swc` exists, 6,736 data rows, exactly three distinct
      dendritic radii (primary / mid / terminal) plus one soma radius; stdout logs each bin mean,
      soma radius, and clamp count. Before running at full scale, run the pipeline once on the first
      50 compartments (slice `raw_compartments[:50]`) and print the 50 `CalibrationRecord`s to
      confirm soma rows 1-19 get the soma radius and dendrite rows 20-50 get non-soma radii with
      valid Strahler orders.

### Milestone D — Analysis and plots

7. **Implement `code/analyze_calibration.py`.** Reads calibration records and both SWC files,
   computes per-order statistics + surface area / axial resistance deltas, emits CSVs, plots, and
   `results/metrics.json`. Imports: `matplotlib` with `matplotlib.use("Agg")` before `pyplot`,
   `pandas` with explicit dtypes, stdlib `json` / `statistics`. For each compartment, compute:
   * `length_um` — Euclidean distance from the compartment to its parent (0 for root).
   * `surface_area_um2 = 2 * pi * radius * length_um`.
   * `axial_resistance_ohm = AXIAL_RESISTIVITY_OHM_CM * length_um * 1e-4 / (pi * (radius * 1e-4) ** 2)`
     (units: Ω, Ra in Ω·cm, L and r in µm converted to cm). Aggregate:
   * `total_surface_area_placeholder_um2`, `total_surface_area_calibrated_um2`,
     `surface_area_ratio = calibrated / placeholder` (expected 4-8× per H2).
   * `total_dendritic_axial_resistance_calibrated_ohm` vs. placeholder.
   * Per-Strahler-order: mean/min/max radius, sum of length, sum of surface area, sum of axial
     resistance. Written to `PER_ORDER_RADII_CSV`.
   * Per-branch (each branch = path from branch point to next branch point or leaf): cumulative
     axial resistance. Written to `PER_BRANCH_AXIAL_CSV`. Plots (150 DPI, Agg backend):
   * `RADIUS_DIST_PNG` — side-by-side histograms per Strahler order, placeholder on left,
     calibrated on right; log-y-axis so the uniform placeholder peak and the three-bin calibrated
     distribution are both visible.
   * `AXIAL_RES_PNG` — cumulative axial resistance along the five longest branches (preferred-
     to-null axis proxy), placeholder vs calibrated overlaid.
   * `SOMA_PROFILE_PNG` — the 19 soma-row radius trace. Write `METRICS_JSON_PATH` with keys
     `{"total_surface_area_placeholder_um2", "total_surface_area_calibrated_um2", "surface_area_ratio", "total_dendritic_axial_resistance_placeholder_ohm", "total_dendritic_axial_resistance_calibrated_ohm", "axial_resistance_ratio", "proximal_input_resistance_calibrated_ohm", "distal_input_resistance_calibrated_ohm", "proximal_rin_matches_schachter_150_to_200_meg": bool, "distal_rin_matches_schachter_gt_1_giga": bool, "n_clamped_dendrites", "n_distinct_radii", "max_strahler_order", "terminal_radius_um", "mid_radius_um", "primary_radius_um", "soma_radius_um"}`.
     Satisfies REQ-8, REQ-9, REQ-12. Expected output: three PNGs in `results/images/`, two CSVs, one
     JSON; surface-area ratio in the ~4-8× band; if `proximal_rin_matches_*` or
     `distal_rin_matches_*` is false, the next step flags a risk note for the reporting stage but
     does NOT silently rerun with different bins — the Poleg-Polsky profile is the literature
     commitment, not an engineering dial.

8. **Register the calibrated dataset asset.** Create
   `assets/dataset/dsgc-baseline-morphology-calibrated/details.json` and `description.md` according
   to `meta/asset_types/dataset/specification.md` v2. `details.json` fields: `spec_version="2"`;
   `dataset_id="dsgc-baseline-morphology-calibrated"`;
   `name="DSGC Baseline Morphology (141009_Pair1DSGC), Diameter-Calibrated"`; `version="1"`;
   `short_description` (~15 words stating source + taper rule); `description_path="description.md"`;
   `source_paper_id="10.1016_j.neuron.2016.02.013"` (Poleg-Polsky & Diamond 2016, from
   `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`); `url=null`;
   `download_url=null`; `year=2026`; `date_published="2026-04-19"`;
   `authors=[{name="t0009_calibrate_dendritic_diameters", country=null, institution="Glite ARF project", orcid=null}]`;
   `institutions=[{name="Glite ARF project", country="GB"}]`; `license="CC-BY-4.0"` (inherited from
   the source SWC's NeuroMorpho CC-BY-4.0, with attribution preserved in `description.md`);
   `access_kind="public"`;
   `size_description="6,736 compartments (19 soma + 6,717 dendrite), 129 branch points, 131 leaves, 1,536.25 µm total dendritic length; Strahler-order-calibrated diameters from Poleg-Polsky & Diamond 2016 ModelDB 189347"`;
   `files=[{path="files/141009_Pair1DSGC_calibrated.CNG.swc", description="Diameter-calibrated SWC; topology copied verbatim from dsgc-baseline-morphology; radii assigned from Poleg-Polsky & Diamond 2016 by Strahler order.", format="swc"}]`;
   `categories=["compartmental-modeling","dendritic-computation","cable-theory", "retinal-ganglion-cell"]`.
   `description.md` YAML frontmatter: `spec_version="2"`, `dataset_id`, `summarized_by_task`,
   `date_summarized`. Mandatory sections in order: `## Metadata`, `## Overview`,
   `## Content & Annotation`, `## Statistics`, `## Usage Notes`, `## Main Ideas`, `## Summary`.
   `## Usage Notes` must explicitly describe the soma-placeholder resolution (Poleg-Polsky pt3dadd
   harvest, 0.5 µm floor), the Strahler-order tie-break convention (maximum child), the 0.15 µm
   terminal radius floor and the clamp count, and the Rin match/miss status against Schachter 2010
   [Schachter2010]. Satisfies REQ-7.

### Milestone E — Tests and verification

9. **Write the topology-equality test.** Create
   `tasks/t0009_calibrate_dendritic_diameters/code/test_swc_io.py` with pytest tests:
   * `test_calibrated_compartment_count_matches` — parses both SWCs, asserts
     `len(calibrated) == len(source) == EXPECTED_COMPARTMENTS`.
   * `test_calibrated_topology_unchanged` — asserts parent_id and type_code columns are identical
     per row.
   * `test_calibrated_coordinates_unchanged` — asserts xyz columns identical to 1e-9 µm.
   * `test_calibrated_no_radius_below_floor` — asserts every dendritic radius >=
     `TERMINAL_RADIUS_FLOOR_UM` and every soma radius >= `SOMA_RADIUS_FLOOR_UM`.
   * `test_calibrated_has_at_least_three_distinct_radii` — asserts
     `len(set(round(r, 6) for r in radii)) >= 3` (prevents regression to uniform).
   * `test_calibrated_summary_matches_source` — builds the source SWC's `SwcSummary` and the
     calibrated one; asserts `branch_points == EXPECTED_BRANCH_POINTS`,
     `leaf_points == EXPECTED_LEAVES`, and
     `abs(total_dendritic_length_um - EXPECTED_DENDRITIC_LENGTH_UM) < 1e-3`. Run:
     `uv run python -u -m arf.scripts.utils.run_with_logs -- pytest tasks/t0009_calibrate_dendritic_diameters/code/ -v`.
     Expected output: 6 passing tests, 0 failures. Satisfies REQ-10.

10. **Run the per-task style gates.** Run
    `uv run python -u -m arf.scripts.utils.run_with_logs -- ruff check --fix tasks/t0009_calibrate_dendritic_diameters/`,
    then `ruff format`, then `mypy` on the same path. Expected output: 0 errors from each tool.
    Additionally run
    `uv run python -u -m arf.scripts.aggregators.aggregate_tasks --ids t0009_calibrate_dendritic_diameters`
    to confirm the task appears in the aggregator with the expected asset count.

## Remote Machines

None required. The entire pipeline runs on the developer laptop in under 30 seconds: stdlib SWC
parse (~6,736 rows), O(N) Strahler recursion, three-bin diameter assignment, matplotlib Agg-backed
PNGs, and pytest. No GPU, no network after the one-time Poleg-Polsky .hoc fetch in Step 3 (which is
checked into the task folder after retrieval so re-runs are offline).

## Assets Needed

* **dataset `dsgc-baseline-morphology`** from `t0005_download_dsgc_morphology` (input SWC, 6,736
  compartments, CC-BY-4.0). Read-only reference; path resolved via `paths.SOURCE_SWC_PATH`.
* **paper asset `10.1016_j.neuron.2016.02.013`** from
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/` (Poleg-Polsky & Diamond
  2016). Cited as `source_paper_id` in the calibrated dataset's `details.json`; its `description.md`
  also provides the biological justification for the soma/primary/terminal three-bin convention.
* **External resource**: `RGCmodel.hoc` from
  `https://raw.githubusercontent.com/geoffder/Spatial-Offset-DSGC-NEURON-Model/master/RGCmodel.hoc`
  (MIT-licensed mirror of the ModelDB 189347 geometry file). Fetched once in Step 3 and checked into
  the task `code/` folder as `RGCmodel.hoc` for hermetic re-runs.
* **Code pattern**: `tasks/t0005_download_dsgc_morphology/code/validate_swc.py` is copied into
  `code/swc_io.py` per CLAUDE.md rule 3 (no cross-task imports; copy-and-adapt only).
* **Code pattern**: `tasks/t0004_generate_target_tuning_curve/code/paths.py` is copied into
  `code/paths.py` as a template.

## Expected Assets

* **1 dataset asset**, matching `task.json` `expected_assets.dataset == 1`:
  `assets/dataset/dsgc-baseline-morphology-calibrated/` with `details.json` (v2), `description.md`
  (v2), and `files/141009_Pair1DSGC_calibrated.CNG.swc`. `dataset_id` slug
  `dsgc-baseline-morphology-calibrated` matches the dataset-id regex `^[a-z0-9]+([.\-][a-z0-9]+)*$`.
  `source_paper_id` points to `10.1016_j.neuron.2016.02.013`. Categories: `compartmental-modeling`,
  `dendritic-computation`, `cable-theory`, `retinal-ganglion-cell`.

In addition, the task produces (not as assets, but as outputs):

* `results/metrics.json` with calibration-specific keys (not registered in `meta/metrics/`; see the
  Approach section's Registered Metrics paragraph).
* `results/per_order_radii.csv`, `results/per_branch_axial_resistance.csv`.
* Three PNG plots in `results/images/`.

## Time Estimation

* Research (already done): 0 h — completed in prior stages (`research_papers.md`,
  `research_internet.md`, `research_code.md`).
* Implementation (Steps 1-8): 2.5 h wall time at developer pace — scaffolding 20 min, parser copy
  \+ writer 25 min, .hoc harvest + regex parse 30 min, Strahler + calibrate 45 min, analysis + plots
  30 min, asset registration 20 min.
* Validation (Steps 9-10): 30 min — pytest + style + aggregator check.
* Remote compute: 0 h.
* Total: ~3 h.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Poleg-Polsky .hoc URL unreachable at run time | Low | Blocking Step 3 | Fallback URL: `https://modeldb.science/download/189347`. If both fail, emit an `intervention/` note and halt; the task requires the external diameter source. |
| Regex `pt3dadd` parser mis-classifies primary vs mid vs terminal sections | Medium | Bins wrong; calibrated Rin off | Validation gate in Step 4: primary/terminal ratio must be 2-15×; if outside, inspect 5 sections, fix the `connect` pattern, re-run. |
| Filtered soma pt3dadd still contains 0.88 µm endpoint artefacts after the 0.5 µm floor | Medium | Soma radius too small | Apply 0.5 µm floor in Step 6; log the five central values used and the two rejected endpoints in stdout so the human reviewer can sanity-check. |
| Strahler order 1 taper too thin, every terminal clamped at the 0.15 µm floor | Low-Medium | Collapses per-order variability | Step 6 records `n_clamped_dendrites`; Step 7 surfaces it in `metrics.json`. If `n_clamped > 50% of terminals`, the calibration is treated as "Poleg-Polsky-profile, mostly clamped" and the fact is stated in the asset `description.md`. |
| Post-calibration Rin gradient off by >50% from Schachter 2010 (150-200 MΩ proximal, >1 GΩ distal) | Medium | Biophysical plausibility weak | Documented in asset `description.md` as a limitation. Does NOT trigger automatic re-run with a different taper — the plan commits to the literature source and flags the mismatch for a follow-up correction task rather than tuning diameters to a target. |
| Compartment count / branch count / leaf count changes (topology broken) | Low | Invalidates downstream tasks | Step 9 pytest checks enforce this as a hard gate; if failed, halt with exit code 1, do not register the asset. |
| Soma-row substitute rule (harvested Poleg-Polsky) is rejected by a future reviewer | Low | Asset may need revision | Documented explicitly in Approach and in the asset `description.md`'s `## Usage Notes`. Downstream tasks use the corrections mechanism if needed. |
| Two sibling children both contributing to Strahler +1 increment when only one should (tie-break convention mismatch with NeuroM) | Low | Per-order bin boundaries shift | Document tie-break (max-child) in `description.md` so re-analysis with NeuroM's convention is reproducible. |

## Verification Criteria

* **Topology equality pytest passes.** Run
  `uv run python -u -m arf.scripts.utils.run_with_logs -- pytest tasks/t0009_calibrate_dendritic_diameters/code/ -v`.
  Expected: 6 tests pass, 0 failures. Confirms REQ-10 (compartment count 6,736, branch points 129,
  leaves 131, total dendritic length within 1e-3 µm of 1,536.25 µm, parent/type/xyz columns
  identical to source).
* **Radius sanity checks pass.** Run
  `uv run python -u -c "from tasks.t0009_calibrate_dendritic_diameters.code.swc_io import parse_swc_file; from tasks.t0009_calibrate_dendritic_diameters.code.paths import CALIBRATED_SWC_PATH; c = parse_swc_file(swc_path=CALIBRATED_SWC_PATH); rs = sorted({round(x.radius,6) for x in c}); print(len(rs), min(rs), max(rs))"`.
  Expected: at least 3 distinct radii, min >= 0.15 µm, max <= 15 µm. Confirms REQ-11 and that the
  calibration did not collapse into a uniform value.
* **Plan verificator passes.** Run
  `uv run python -u -m arf.scripts.verificators.verify_plan t0009_calibrate_dendritic_diameters`.
  Expected: 0 errors. Warnings acceptable only if explicitly noted here.
* **Dataset asset structural checks pass.** Run
  `uv run python -u -c "import json, pathlib; d = json.loads(pathlib.Path('tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/details.json').read_text()); assert d['spec_version']=='2' and d['dataset_id']=='dsgc-baseline-morphology-calibrated' and d['source_paper_id']=='10.1016_j.neuron.2016.02.013' and len(d['files'])==1; print('OK')"`.
  Expected: prints `OK`. Confirms REQ-7.
* **Per-order outputs present.** Run
  `uv run python -u -c "import pathlib; paths = ['tasks/t0009_calibrate_dendritic_diameters/results/per_order_radii.csv', 'tasks/t0009_calibrate_dendritic_diameters/results/per_branch_axial_resistance.csv', 'tasks/t0009_calibrate_dendritic_diameters/results/metrics.json', 'tasks/t0009_calibrate_dendritic_diameters/results/images/radius_distribution_by_strahler_order.png', 'tasks/t0009_calibrate_dendritic_diameters/results/images/axial_resistance_by_strahler_order.png', 'tasks/t0009_calibrate_dendritic_diameters/results/images/soma_radius_profile.png']; [print(p, pathlib.Path(p).exists()) for p in paths]"`.
  Expected: all six paths print `True`. Confirms REQ-8 and REQ-9.
* **Style checks pass.** Run
  `uv run python -u -m arf.scripts.utils.run_with_logs -- ruff check tasks/t0009_calibrate_dendritic_diameters/`
  and `ruff format --check tasks/t0009_calibrate_dendritic_diameters/` and
  `mypy tasks/t0009_calibrate_dendritic_diameters/`. Expected: 0 errors from each.
* **Task-complete verificator passes at the end of implementation.** Run
  `uv run python -u -m arf.scripts.verificators.verify_task_complete t0009_calibrate_dendritic_diameters`.
  Expected: 0 errors. Confirms all mandatory artefacts (plan, research docs, step_tracker, asset,
  results files, logs) are in place.
