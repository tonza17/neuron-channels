---
spec_version: "1"
task_id: "t0009_calibrate_dendritic_diameters"
research_stage: "code"
tasks_reviewed: 7
tasks_cited: 5
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Replace the 0.125 µm placeholder radii in the CNG-curated
`tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc`
SWC with a literature-derived diameter taper keyed on Strahler order, preserve the 19 soma
compartments, and register the result as a new `dsgc-baseline-morphology-calibrated` dataset asset.
This research surveys the project's own codebase — libraries, prior task code, dataset assets,
answer assets, and tooling conventions — to locate reusable patterns and avoid reinventing the SWC
parsing, path-management, and plotting wheels already established in `t0004` and `t0005`.

## Library Landscape

The library aggregator is not yet implemented in this repo
(`arf/scripts/aggregators/aggregate_libraries.py` does not exist — only `aggregate_tasks`,
`aggregate_costs`, `aggregate_machines`, `aggregate_metric_results`, `aggregate_metrics`,
`aggregate_suggestions`, `aggregate_categories`, and `aggregate_task_types` are present). Directly
enumerating `tasks/*/assets/library/` confirms zero library assets have been produced by any
completed task; every completed task so far produced only `dataset` or `answer` assets. Consequently
there is nothing to "import via library" — every reusable pattern below is labelled "copy into
task". The suggestion `S-0005-04` (a reusable `load_dsgc_morphology()` library) exists as a
**pending** suggestion from `t0005` but has not been materialised. External Python packages
(`neurom`, `pyswc`, `nGauge`) recommended in the `research_internet.md` are not currently in
`pyproject.toml` — only `matplotlib>=3.10.8`, `pandas>=3.0.2`, `numpy>=2.4.4` are declared — so
the implementation plan must either add `neurom` as a dependency (allowed by CLAUDE.md rule 3 as a
`pyproject.toml` exception) or implement Strahler order from scratch.

## Key Findings

### Stdlib-only SWC parsing pattern is established and production-tested

[t0005] established a stdlib-only SWC reader in
`tasks/t0005_download_dsgc_morphology/code/validate_swc.py` (237 lines, `parse_swc_file` at lines
63-89). It produces a `list[SwcCompartment]` of `@dataclass(frozen=True, slots=True)` rows with
fields `compartment_id, type_code, x, y, z, radius, parent_id`, tolerates `#` comments and blank
lines, and asserts each row has exactly 7 whitespace-separated fields. The tree-structure invariants
it checks — exactly one root with `parent_id == -1`, all non-root `parent_id`s exist, non-negative
radii, soma present, ≥ 100 dendritic compartments — are the exact same invariants the calibrated
output must preserve. Reusing the parser keeps the diameter calibration "topology in, topology out"
with no new SWC-parsing bugs. The `_summarize` function (lines 128-176) also computes branch-point
count (129), leaf count (131), and total dendritic length (1,536.25 µm) directly from the
compartment list and these will be the pre/post equality checks for the calibrated asset [t0005].

### The 0.125 µm placeholder is literally uniform across all 6,736 compartments, soma included

The task description states "Preserve the 19 soma compartments' original (non-placeholder) radii",
but direct inspection of
`tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc`
shows all 19 soma rows (type code 1) AND all 6,717 dendrite rows (type code 3) carry the single
value `0.125` in column 6 — the file has **one** unique radius value project-wide. This is a
contradiction the implementation must resolve: the soma contour rows are also placeholders, not
original measurements, so "preserve soma radii verbatim" leaves a 19-point 0.125 µm soma that
Import3d will collapse to a ~0.25 µm soma cylinder, which is 40-60× too thin vs. the ~10-15 µm
community-standard soma diameter [PolegPolsky2016-extracted, Schachter2010]. `t0005`'s
`description.md` also lists a NeuroMorpho-reported soma surface of 6.86 µm², consistent with a
~1.5-µm-equivalent sphere — i.e. also placeholder-scaled. The implementation should either (a)
assign soma radii from Poleg-Polsky's pt3dadd soma points (0.88, 6.14, 7.74, 8.32, 8.35, 10.62, 0.88
µm diameters per the `research_internet.md` extract) or (b) flag an intervention and only calibrate
dendrite radii [t0005].

### Path-management and per-task constants pattern established by t0004

[t0004] `tasks/t0004_generate_target_tuning_curve/code/paths.py` is the reference pattern for
per-task path constants: a small module that defines
`TASK_ROOT = Path(__file__).resolve().parent.parent`, `DATASET_ID: str = "target-tuning-curve"`, and
a chain of `Path` objects for the asset folder, the `files/` subdir, the `details.json`,
`description.md`, CSV outputs, and `results/images/` for plots (17 lines total). `t0009` should copy
this pattern verbatim with `DATASET_ID = "dsgc-baseline-morphology-calibrated"` and add constants
for the placeholder-vs-calibrated radius histogram PNG and the per-order radius CSV that
`research_internet.md` recommends exporting alongside the SWC. All downstream modules should import
from `paths.py` rather than hard-code strings [t0004].

### Dataclass + keyword-args + explicit dtypes pattern in every prior task's code

Every code file in `t0004` and `t0005` uses `@dataclass(frozen=True, slots=True)` for result
containers, explicit keyword-only arguments for functions with ≥ 2 parameters (the `*,` separator
in `def fn(*, a: T, b: T) -> R`), and explicit type annotations on every local variable. Examples:
`validate_swc.py` `SwcCompartment` and `SwcSummary` at lines 40-61; `generate_target.py`
`GeneratorParams` at lines 24-34. The `compute_mean_curve(*, params: GeneratorParams)`,
`validate(*, swc_path: Path)` signatures show the project's strict keyword-args convention. The
calibrated SWC writer should follow suit:
`write_calibrated_swc(*, compartments: list[SwcCompartment], output_path: Path) -> None`
[t0004, t0005].

### Matplotlib plotting is Agg-backed and saves through a centralised path constant

[t0004] `generate_target.py` uses `matplotlib.use("Agg")` (line 8, before any pyplot import) to
enable headless PNG rendering, then saves through `PLOT_PATH` from `paths.py` with
`fig.savefig(PLOT_PATH, dpi=150)`. The pattern (lines 125-187) is the template for the task's
required per-order placeholder-vs-calibrated radius distribution plot, and for the
axial-resistance-per-branch plots in `plan/plan.md`. The `results/images/` directory is created at
plot time via `mkdir(parents=True, exist_ok=True)` — the task folder structure does not pre-create
`results/images/` [t0004].

### Dataset asset structure is fixed by meta/asset_types/dataset/specification.md

[t0005] `tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/` has the
canonical v2 dataset asset layout: `details.json` (with `spec_version: "2"`, `dataset_id`, `name`,
`version`, `short_description`, `description_path`, authors, institutions, `files` array, etc.),
`description.md` (with YAML frontmatter `spec_version: "2"`, `dataset_id`, `summarized_by_task`,
`date_summarized`, followed by mandatory sections: `## Metadata`, `## Overview`,
`## Content & Annotation`, `## Statistics`, `## Usage Notes`, `## Main Ideas`, `## Summary`), and
`files/` holding the data payload. The calibrated dataset must mirror this layout with its own
`description.md` documenting: the taper source paper (`PolegPolsky2016`), the Strahler-order
bucketing rule, the NeuroM tie-break convention used, the 0.15 µm terminal floor clamp count, and
the total-surface-area / axial-resistance deltas vs. the placeholder baseline [t0005].

### Topology-preserving equality checks are the validation gate

[t0005]'s `validate_swc.py` already expresses the exact three invariants the task description
demands as post-calibration checks: compartment count (6,736), branch points (129), leaves (131).
The calibrated-SWC writer must emit a file that when re-parsed with
`parse_swc_file(swc_path=calibrated_path)` and passed through `_summarize()` yields a `SwcSummary`
with `total_compartments == 6736`, `branch_points == 129`, `leaf_points == 131`, and
`total_dendritic_length_um` within 1e-3 µm of 1,536.25 (path length is a pure function of xyz
coordinates, which must be copied verbatim). This gives a deterministic binary gate on topology
preservation [t0005].

## Reusable Code and Assets

### `parse_swc_file()` and `SwcCompartment` from t0005 — copy into task

* **Source**: `tasks/t0005_download_dsgc_morphology/code/validate_swc.py` lines 40-89 (dataclasses)
  and lines 63-89 (parser).
* **What it does**: Stdlib SWC reader that returns `list[SwcCompartment]` with per-compartment id,
  type code, xyz, radius, parent id. Skips `#` comments and blank lines, raises `ValueError` on
  malformed rows.
* **Reuse method**: **copy into task** — non-library; CLAUDE.md rule 3 forbids importing from
  another task's `code/`. Copy `SwcCompartment`, `SwcSummary`, `SWC_TYPE_*` constants,
  `ROOT_PARENT_ID`, `parse_swc_file`, `_validate_structure`, and `_summarize` verbatim into
  `tasks/t0009_calibrate_dendritic_diameters/code/swc_io.py`.
* **Function signatures**: `parse_swc_file(*, swc_path: Path) -> list[SwcCompartment]`,
  `validate(*, swc_path: Path) -> SwcSummary`.
* **Adaptation needed**: None for the reader; add a sibling writer
  `write_swc_file(*, compartments: list[SwcCompartment], output_path: Path, header_comments: list[str]) -> None`
  that reproduces the CNG 7-column format with one compartment per line and `#`-prefixed header
  comments.
* **Line count**: ~130 lines of reusable stdlib code (parser + summariser + dataclasses).

### `paths.py` pattern from t0004 — copy into task

* **Source**: `tasks/t0004_generate_target_tuning_curve/code/paths.py` (17 lines total).
* **What it does**: Single module of `Path` constants rooted on
  `Path(__file__).resolve().parent.parent`, defining the dataset asset folder, its `details.json`,
  `description.md`, data files, and the `results/images/` PLOT_PATH.
* **Reuse method**: **copy into task**. Create
  `tasks/t0009_calibrate_dendritic_diameters/code/paths.py` with
  `DATASET_ID = "dsgc-baseline-morphology-calibrated"` and add `CALIBRATED_SWC_PATH`,
  `PER_ORDER_RADII_CSV`, `RADIUS_DISTRIBUTION_PLOT_PATH`, and `SOURCE_SWC_PATH` (pointing to the
  absolute path
  `tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc`
  via `REPO_ROOT` resolution). No cross-task import is required — only a literal absolute-path
  reference.
* **Adaptation needed**: rename `DATASET_ID` and add 3-4 new path constants.
* **Line count**: ~25 lines.

### Matplotlib PNG pattern from t0004 — copy into task

* **Source**: `tasks/t0004_generate_target_tuning_curve/code/generate_target.py` lines 1-21 (imports
  \+ Agg backend) and 125-187 (`plot_curve`).
* **What it does**: Headless Agg-backed matplotlib figure creation, errorbar + scatter + closed-form
  line overlay, `fig.savefig(PLOT_PATH, dpi=150)`, `plt.close(fig)` pattern.
* **Reuse method**: **copy into task**. The structure (Agg import before pyplot, figure builder,
  savefig+close) is the template; the plot content itself is task-specific (per-order radius
  histograms, placeholder baseline overlay).
* **Line count**: ~30 lines of boilerplate, plus task-specific figure drawing.

### v2 dataset asset skeleton from t0005 — copy into task

* **Source**:
  `tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/{details.json,description.md}`.
* **What it does**: Canonical v2 dataset asset: `details.json` with full author/institution list,
  `files` array, `categories`, `source_paper_id`; `description.md` with YAML frontmatter + mandatory
  sections.
* **Reuse method**: **copy into task** as a structural template. The calibrated dataset's
  `source_paper_id` must be the paper-asset slug of
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
  (Poleg-Polsky & Diamond 2016). Categories should be
  `["compartmental-modeling", "dendritic-computation", "cable-theory", "retinal-ganglion-cell"]` per
  the `S-0005-02` suggestion and task description.
* **Adaptation needed**: new `dataset_id`, `source_paper_id`, `size_description`, `files`,
  `categories`, fresh `description.md` content per spec v2.

### Input SWC asset from t0005 — read-only reference

* **Source**:
  `tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/files/141009_Pair1DSGC.CNG.swc`
  (6,748 lines, 232,470 bytes, 7-column CNG format, ~12 header comment lines).
* **What it does**: The input artefact to calibrate. All 6,736 data rows (19 type-1 soma + 6,717
  type-3 dendrite) have column 6 = `0.125`.
* **Reuse method**: **read-only** — never modified. The calibrated SWC is written to
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/files/141009_Pair1DSGC_calibrated.CNG.swc`
  as an independent artefact.
* **Adaptation needed**: none.

## Dataset Landscape

Two datasets have been produced by completed tasks:

* **`dsgc-baseline-morphology`** [t0005] — the CNG-curated SWC this task consumes. 6,736
  compartments, 129 branch points, 131 leaves, 1,536.25 µm total dendritic path length, uniform
  0.125 µm placeholder radius. Licensed CC-BY-4.0.
* **`target-tuning-curve`** [t0004] — closed-form angle-to-AP-rate target curve (`curve_mean.csv`,
  `curve_trials.csv`, `generator_params.json`). Irrelevant to diameter calibration but shows the
  project's canonical CSV + JSON + PNG asset layout.

No prior task has produced a `predictions`, `model`, or `library` asset.

## Lessons Learned

* **`validate_swc.py` caught one real bug during t0005's execution** — the NeuroMorpho record
  listed `attributes: "No Diameter, 3D, Angles"`, but the stdlib validator nonetheless passed
  `VALID` because 0.125 µm is non-negative. This is a silent data-quality failure that the
  validator was not designed to catch. The t0009 calibration fixes exactly this class of bug; the
  post-calibration validator should additionally assert `radius > 0.05 µm` and `radius <= 15 µm`
  as a sanity band [t0005].
* **Soma contour rows are also placeholders** (see Key Findings #2) — the task description's
  "preserve 19 soma compartments verbatim" instruction is based on a false premise and must be
  resolved in the plan stage before implementation begins [t0005].
* **`neurom` Python package is not a project dependency yet**. Adding it requires modifying
  `pyproject.toml` (an explicit CLAUDE.md rule 3 exception). The alternative is a hand-rolled
  Strahler-order recursion on the `list[SwcCompartment]` tree, which is ~40 lines of Python and has
  no external dependency [research_internet.md].
* **Matplotlib PNG dpi convention is 150 across the project** [t0004]. No task has yet deviated;
  keep this consistent.
* **t0005's verify_dataset_asset.py does not exist** — the t0005 results_summary note that "the
  framework's verify_dataset_asset.py script is not implemented, so the check was done by applying
  each rule from meta/asset_types/dataset/specification.md directly". t0009 will face the same
  manual-compliance gap and should document v2 rule-by-rule conformance in its step log [t0005].
* **Placeholder 0.125 µm radius is not a NeuroMorpho-wide convention**, per
  `research/research_internet.md`: it is an idiosyncrasy of this one Simple Neurite Tracer export.
  The calibrated-dataset description should state this explicitly to avoid implying a
  NeuroMorpho-level bug is being patched.

## Recommendations for This Task

1. **Copy `validate_swc.py` verbatim** from [t0005] into `code/swc_io.py`, extend with a
   `write_swc_file()` function, and use the existing `parse_swc_file` + `_summarize` as both the
   input reader and the post-calibration topology-equality gate.
2. **Copy the `paths.py` pattern** from [t0004] with
   `DATASET_ID = "dsgc-baseline-morphology-calibrated"`. Use it as the sole path-management module;
   no hard-coded strings anywhere in task code.
3. **Implement Strahler-order computation in pure Python** as part of `code/morphology.py` —
   ~40-line recursive function over the `list[SwcCompartment]` tree — to avoid adding `neurom` as
   a dependency. If tie-break edge cases arise, fall back to adding `neurom` to `pyproject.toml`.
   Document the tie-break convention in the calibrated dataset's `description.md`.
4. **Flag the soma-placeholder contradiction** as a plan-stage issue before implementation. Options:
   (a) extract Poleg-Polsky pt3dadd soma diameters and assign them; (b) apply a uniform
   `SOMA_RADIUS = 5.0 µm` taken from Schachter2010's ~10 µm soma diameter; (c) write an
   intervention file describing the conflict. The task description's instruction cannot be literally
   followed.
5. **Assert topology equality against t0005's reported numbers**: 6,736 compartments, 129 branch
   points, 131 leaves, 1,536.25 µm total dendritic length. Use `_summarize()` from the copied
   `swc_io.py` as the oracle; write the comparison as a pytest in
   `tasks/t0009_calibrate_dendritic_diameters/code/test_swc_io.py` per CLAUDE.md rule 7.
6. **Produce the per-order radius distribution CSV** (`results/per_order_radii.csv`) in addition to
   the PNG — `research_internet.md` recommends this for downstream task reuse (t0011
   visualization, t0008 reproduction), and CSVs are the project's canonical cross-task interchange
   format [t0004].
7. **Match the v2 dataset asset layout** from [t0005] exactly: `details.json` + `description.md` +
   `files/`, with the canonical seven `##` sections in `description.md`. Explicitly list the
   Poleg-Polsky paper asset slug (`10.1016_j.neuron.2016.02.013`) as `source_paper_id`.
8. **Treat `S-0005-04` (SWC loader library) as future work**, not as a t0009 deliverable — the
   task description scopes t0009 to *writing* a calibrated SWC, not building a simulator-loader
   library. Leave that to a dedicated later task.

## Task Index

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: compartmental models of DS retinal ganglion cells
* **Status**: `completed`
* **Relevance**: Holds every downloaded paper the taper-source decision depends on, including the
  primary source paper asset
  (`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
  for Poleg-Polsky & Diamond 2016) that the calibrated dataset's `details.json` must cite as
  `source_paper_id`. Also the only task with `assets/paper/` subfolders project-wide.

### [t0003]

* **Task ID**: `t0003_simulator_library_survey`
* **Name**: Simulator library survey for DSGC compartmental modelling
* **Status**: `completed`
* **Relevance**: Its `dsgc-compartmental-simulator-choice` answer asset lists ModelDB 189347 and the
  `geoffder/Spatial-Offset-DSGC-NEURON-Model` GitHub repo among the surveyed sources — the same
  two artefacts `research_papers.md` and `research_internet.md` name as primary/fallback taper
  sources. Confirms these are the community-accepted DSGC references, not task-internal choices.

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate canonical target angle-to-AP-rate tuning curve
* **Status**: `completed`
* **Relevance**: Provides the reference pattern for per-task path constants (`code/paths.py`),
  headless matplotlib PNG saving (`code/generate_target.py` lines 1-21, 125-187), dataclass +
  keyword-args + explicit-dtype conventions, and CSV-plus-JSON dataset asset layout. t0009 copies
  its `paths.py` pattern and plot boilerplate verbatim.

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download candidate DSGC morphology
* **Status**: `completed`
* **Relevance**: Direct dependency. Produces the input SWC (`dsgc-baseline-morphology`), its
  canonical validator/parser (`code/validate_swc.py`), and the v2 dataset asset structural template.
  Every reusable piece of code in this research review is sourced from t0005.

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install NEURON 8.2.7 + NetPyNE 1.1.1, compile bundled HH MOD files, run a 1-compartment
  sanity simulation, and record versions
* **Status**: `in_progress`
* **Relevance**: Would have supplied NEURON Python bindings for loading Poleg-Polsky's
  `RGCmodel.hoc` and harvesting pt3dadd diameters via `sec.diam3d(i)`. Because t0007 is not yet
  completed, t0009 must use the regex/text-parse route on the raw `.hoc` file rather than the
  NEURON-Python loader route. This is a binding constraint on the implementation strategy.
