---
spec_version: "2"
task_id: "t0103_extract_baden_2016_ds_morphologies"
date_completed: "2026-05-11"
status: "complete"
---
# Plan: Extract Baden 2016 Direction-Selective Cell Data

## Objective

Download the Baden et al. 2016 *Nature* paper (DOI `10.1038/nature16468`) and the accompanying Dryad
dataset (DOI `10.5061/dryad.d9v38`) plus the lab-distributed MATLAB visualisation zip, then filter
the per-cell data to only the 8 user-specified direction-selective (DS) groups (cluster IDs **2, 17,
18, 19, 22, 35, 36, 40** in the Baden 2016 extended >32-group taxonomy) and produce one clean
per-cell dataset asset plus one paper asset. "Done" means: (a) the paper asset at
`assets/paper/10.1038_nature16468/` passes the paper verificator with 0 errors; (b) the dataset
asset at `assets/dataset/baden-2016-ds-cells/` passes the dataset verificator with 0 errors and
contains one record per cell for the 8 DS groups with every per-cell field available in the Dryad
release; (c) two diagnostic charts (per-group cell-count + IPL stratification; representative
moving-bar response trace per group) are written to `results/images/`; (d) per-group cell counts
have been cross-checked against the visualisation scripts' own summary outputs (or, if those are
unavailable, against Figure 2 of the paper) and the comparison is recorded in
`code/group_count_check.json` for the orchestrator's downstream reporting step to consume.

## Task Requirement Checklist

The operative request from `task.json` and `task_description.md`:

> Download Baden 2016 (Dryad d9v38) and extract data only for direction-selective groups 2, 17, 18,
> 19, 22, 35, 36, 40. Output: 1 dataset + 1 paper asset.
>
> Sources: Paper DOI `10.1038/nature16468`; Dataset Dryad DOI `10.5061/dryad.d9v38`; MATLAB
> visualisation zip at
> `http://retinal-functomics.net/wp-content/uploads/2015/12/ Baden_et_al_2016_visualization.zip`;
> Dryad README at `https://datadryad.org/downloads/file_stream/3407`. Extract per-cell: cluster ID +
> confidence, soma position, IPL stratification depth profile, functional response traces and
> extracted features, morphological reconstruction if available, cell-of-origin metadata. Verify
> per-group cell counts against Figure 2 / visualisation-script summaries. Produce at least one
> cell-count + IPL chart and one representative-trace chart.
> `expected_assets = {dataset: 1, paper: 1}`. Out of scope: re-classifying Baden data, re-analysing
> raw traces, expanding to non-DS groups, integrating later Baden-lab releases.

Concrete requirements extracted from the task text:

* **REQ-1** — Download the Baden 2016 paper (DOI `10.1038/nature16468`) and register it as a paper
  asset at `assets/paper/10.1038_nature16468/` following `meta/asset_types/paper/specification.md`
  v3, with `citation_key = "Baden2016"` and
  `categories = ["direction-selectivity", "retinal-ganglion-cell"]`. Satisfied by **Steps 2-3**;
  evidence:
  `verify_paper_asset --task-id t0103_extract_baden_2016_ds_morphologies 10.1038_nature16468`
  reports 0 errors.

* **REQ-2** — Download the full Dryad bundle (DOI `10.5061/dryad.d9v38`) into a task-local `data/`
  folder, recording per-file byte sizes and SHA-256 hashes in `data/download_manifest.json`.
  Satisfied by **Step 4**; evidence: `data/download_manifest.json` lists every Dryad file with
  `bytes` and `sha256` fields and every listed file exists on disk.

* **REQ-3** — Download the MATLAB visualisation zip from
  `http://retinal-functomics.net/wp-content/uploads/2015/12/Baden_et_al_2016_visualization.zip`,
  extract it into `data/visualization_code/`, and inspect its top-level scripts to identify which
  Dryad file holds cluster assignments, which field name holds the cluster ID, and where per-cell
  traces and any morphological data are stored. Satisfied by **Step 5**; evidence:
  `data/visualization_code/` contains the extracted MATLAB files and
  `code/visualization_code_notes.md` records the file/field mapping derived from the scripts.

* **REQ-4** — Download the Dryad README from `https://datadryad.org/downloads/file_stream/3407`,
  save it under `data/dryad_readme.txt`, and cross-reference its field list against what the
  visualisation scripts actually load. Satisfied by **Step 6**; evidence: `data/dryad_readme.txt`
  exists and `code/visualization_code_notes.md` contains a "README cross-check" subsection.

* **REQ-5** — Reconcile the user-specified cluster IDs (2, 17, 18, 19, 22, 35, 36, 40) against the
  numbering scheme actually used inside the Dryad files via the visualisation scripts. If the labels
  do not match "DS"-style cell types, document the resolution; if reconciliation is ambiguous, write
  an intervention file in `intervention/` before producing the dataset asset. Satisfied by **Step
  7**; evidence: the "Cluster ID reconciliation" subsection of `code/visualization_code_notes.md`
  records the mapping; on ambiguity, an intervention file at
  `intervention/<ID>_cluster_id_ambiguity.json` exists.

* **REQ-6** — Implement a Python loader in `code/load_baden.py` that loads per-cell cluster
  assignments, filters to the 8 DS groups, pulls every available per-cell field (cluster ID +
  confidence, soma position, IPL stratification depth profile, functional response traces and
  extracted features, morphology if present, cell-of-origin metadata), and emits one clean per-cell
  record per cell. Satisfied by **Step 8**; evidence:
  `uv run python -u code/load_baden.py --dry-run` prints a per-group cell count summary and a sample
  record schema.

* **REQ-7** — Write the dataset asset at `assets/dataset/baden-2016-ds-cells/` following
  `meta/asset_types/dataset/specification.md` v2 — `details.json`, canonical `description.md`, and
  `files/` with the per-cell records in a single Parquet **or** JSONL container (whichever is the
  simpler match for the source field shapes; the loader chooses Parquet when all fields are tabular
  and JSONL when nested per-cell arrays such as traces dominate; the chosen format is recorded in
  `details.json` `files[0].format`). Satisfied by **Step 9**; evidence:
  `verify_dataset_asset --task-id t0103_extract_baden_2016_ds_morphologies baden-2016-ds-cells`
  reports 0 errors.

* **REQ-8** — If the Dryad release does not contain morphological reconstructions for these
  groups, document the absence explicitly in both `description.md` and
  `code/visualization_code_notes.md`. The loader must continue and extract whatever per-cell data IS
  present (functional traces, IPL stratification, soma position, metadata). Satisfied by **Steps
  8-9**; evidence: `description.md` "Usage Notes" subsection states the morphology status explicitly
  and `details.json` `short_description` mentions the morphology gap if present.

* **REQ-9** — Verify per-group cell counts in the produced dataset against the
  visualisation-script summaries (preferred) or, as fallback, against the counts reported in Figure
  2 of Baden 2016; write the comparison to `code/group_count_check.json` with one record per group
  containing `produced_count`, `reference_count`, `reference_source`, and `delta_pct`. Flag any
  group whose `delta_pct > 5%` as a finding. Satisfied by **Step 10**; evidence:
  `code/group_count_check.json` exists and contains 8 entries with `delta_pct` populated.

* **REQ-10** — Produce at least two diagnostic charts in `results/images/`: (a)
  `cell_counts_and_ipl.png` — per-group cell count bars plus an overlaid IPL stratification
  profile per group; (b) `representative_traces.png` — one cluster-mean response trace per group
  to the moving-bar stimulus that defines DS. Satisfied by **Step 11**; evidence: both PNG files
  exist at `tasks/.../results/images/`.

* **REQ-11** — `expected_assets = {"dataset": 1, "paper": 1}` from `task.json`. The dataset asset
  is `baden-2016-ds-cells`; the paper asset is `10.1038_nature16468`. Both must pass their
  respective verificators with 0 errors. Satisfied by **Steps 3 and 9**; evidence: the two
  verificator commands listed under Verification Criteria both report 0 errors.

* **REQ-12** — Out-of-scope constraints (no re-clustering, no re-analysis of raw traces, no non-DS
  groups, no other Baden-lab releases, no NEURON simulations, no parametric generator) must not be
  violated. Satisfied by the absence of any such steps in **Step by Step** below; evidence: the Step
  by Step contains no clustering, no trace re-fitting, no non-DS extraction, no NEURON code, and no
  generator code.

## Approach

This task is **mechanical extraction** — download three published resources, read them, write a
filtered Python load of the data, and package the result as a dataset asset plus a paper asset.
There is no statistical inference, no model fitting, and no simulation. The research stage was
deliberately skipped because every source URL, the exact 8-cluster filter, the expected output
shape, and the format spec are already enumerated in `task_description.md`; re-deriving them via
literature or internet search would only restate the brief.

**Recommended task types**: `download-paper` (for the Baden 2016 paper) and `download-dataset` (for
the Dryad bundle + visualisation zip + README, which together form a single logical dataset). The
`task.json` `task_types` field already lists both, so no orchestrator update is needed. Per the
`download-dataset` Planning Guidelines, the plan records the exact source URLs, expected file
formats, and the SHA-256 manifest commitment (REQ-2). Per the `download-paper` Planning Guidelines,
the plan commits to using `arf.scripts.utils.doi_to_slug` for the paper ID (already pre-computed:
`10.1038_nature16468`) and to running the paper verificator after asset creation.

**Key design decisions**:

* **Single dataset asset, not three**: the Dryad bundle, MATLAB zip, and Dryad README together
  describe one logical dataset (the Baden 2016 functional RGC release). Splitting them into separate
  dataset assets would scatter related provenance and force downstream consumers to load three asset
  folders to reconstruct the picture. The MATLAB zip is treated as auxiliary source material — the
  canonical asset content is the **filtered per-cell record file** the loader writes, not the raw
  Dryad blobs. The raw Dryad files go under `data/` (task-local, not in the asset's `files/`) so the
  asset's `files/` directory contains only the clean, task-specific output that downstream modelling
  tasks actually need. *Alternative considered*: emit three sibling dataset assets
  (`baden-2016-dryad-raw`, `baden-2016-visualization-code`, `baden-2016-readme`). Rejected — the
  visualisation code is a reading aid, not data; the README is metadata about the Dryad files, not a
  dataset in its own right; and downstream modelling tasks (t0090's parameter envelopes, t0102's
  joint-pass validation) want the **filtered DS subset** in one place, not the raw 11 000-cell
  archive.

* **Loader does filtering only, no re-analysis**: per `task_description.md` "Out of scope", the
  loader pulls fields **as-is** from the Dryad files. It does not re-cluster, re-classify, or re-fit
  Ca2+ traces. The cluster IDs in the dataset asset's per-cell records are exactly the IDs that
  appear in the Dryad release after the user-vs-Dryad numbering reconciliation (REQ-5).

* **Cluster-ID reconciliation is mandatory before extraction**: the user lists 8 specific group IDs
  in the extended >32-group taxonomy. The Dryad release may use a different numbering scheme. The
  plan resolves this **before** writing the loader (Step 7) using the visualisation scripts as
  authoritative; if the resolution is ambiguous, an intervention file blocks progress. This is
  explicit in REQ-5 and is the single highest-risk decision point in the task — silently
  substituting different cluster IDs would corrupt every downstream modelling task that consumes the
  asset.

* **Container choice deferred to the loader**: Parquet is preferable for tabular per-cell features
  (cluster ID, IPL depth scalar, DSI, soma x/y, etc.). JSONL is preferable when most fields are
  variable-length per-cell arrays (e.g. full chirp response traces of different lengths). The loader
  inspects the source field shapes and picks one container; the choice is recorded in `details.json`
  so consumers know what to expect. Rejected alternative: forcing Parquet — would require either
  flattening nested traces into wide columns (loses structure) or storing them as binary blobs
  (defeats the point of Parquet).

* **No remote machines, no paid APIs**: this is a local data pull. Paper PDF is open access via
  nature.com; Dryad is public; the MATLAB zip is publicly hosted; the README is publicly hosted on
  Dryad's static file server.

**Library handling**: MATLAB `.mat` files in the Dryad release may be HDF5 v7.3 (which
`scipy.io.loadmat` cannot read). The plan adds `mat73` to `pyproject.toml` as a project-level
dependency if the Dryad files turn out to need it, falling back to `h5py` if `mat73` import fails.
`scipy.io.loadmat` is tried first since it is already in the project's environment.

**No applicable registered metrics**: the project's registered metrics
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) all measure **simulated** DSGC behaviour from compartmental modelling tasks.
This task does not run simulations — it extracts pre-recorded biological data. None of the four
metrics applies, so `results/metrics.json` will be written by the orchestrator's reporting step with
no metric entries from this task. This omission is deliberate and consistent with the task's
pure-extraction nature.

## Cost Estimation

* **Compute**: $0. Local CPU-only data download and Python parsing.
* **Remote machines**: $0. None required (see Remote Machines section).
* **Paid APIs**: $0. None used. Paper PDF is open-access from `nature.com`; Dryad and the
  visualisation zip are publicly hosted.
* **Network**: $0 marginal cost. Estimated total download: <1.2 GB (Dryad bundle ~1 GB + MATLAB
  visualisation zip ~50 MB + paper PDF ~5 MB + README ~50 KB).
* **Disk**: ~3 GB of task-local working storage during extraction; final asset payload (filtered
  per-cell records for the 8 DS groups) is expected at ~50-200 MB depending on trace length and
  morphology presence.
* **Project budget context**: `project/budget.json` reports `total_budget = $35.00 USD`,
  `per_task_default_limit = $8.00 USD`. This task consumes **$0.00** against both, leaving the
  per-task envelope fully unused.

## Step by Step

Steps are grouped into three milestones. Each milestone is independently verifiable.

### Milestone A — Download and inspect sources

1. **Initialise task-local directories**. Create `data/`, `data/visualization_code/`, `code/`,
   `results/`, `results/images/`, `assets/paper/10.1038_nature16468/files/`,
   `assets/dataset/baden-2016-ds-cells/files/`, and `intervention/` inside the task folder. Expected
   output: `ls tasks/t0103_extract_baden_2016_ds_morphologies/` shows the new directories. Satisfies
   REQ-1, REQ-2 (prep).

2. **Download the Baden 2016 paper PDF** [CRITICAL]. Run
   `curl -L -o assets/paper/10.1038_nature16468/files/baden_2016_functional_diversity_rgc.pdf https://www.nature.com/articles/nature16468.pdf`
   wrapped in `arf/scripts/utils/run_with_logs.py`. If the direct PDF URL is paywalled or returns
   HTML, fall back to the open-access PubMed Central mirror at
   `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4734159/pdf/`; if both fail, set the paper asset's
   `download_status = "failed"` and `download_failure_reason` to the exact HTTP response and create
   an intervention file at `intervention/paper_download_failed.json` describing the failure.
   Expected output: the PDF exists at the path above and `file ... | grep PDF` reports a valid PDF,
   OR the intervention file exists. Satisfies REQ-1.

3. **Create the paper asset** [CRITICAL]. Write `assets/paper/10.1038_nature16468/details.json`
   (paper asset spec v3) and the canonical `assets/paper/10.1038_nature16468/summary.md` (full v3
   spec compliance — all mandatory sections: Metadata, Abstract, Overview,
   Architecture/Models/Methods, Results, Innovations, Datasets, Main Ideas, Summary), with
   `citation_key = "Baden2016"`, `categories = ["direction-selectivity", "retinal-ganglion-cell"]`,
   `summary_path = "summary.md"`, `added_by_task = "t0103_extract_baden_2016_ds_morphologies"`, and
   `date_added = "2026-05-11"`. The summary is written from a full read of the downloaded PDF; if
   the PDF download failed, the summary uses the abstract from the Nature landing page plus the
   dataset README and the Results section explicitly states the full text was not available. Run
   `uv run python -m arf.scripts.verificators.verify_paper_asset --task-id t0103_extract_baden_2016_ds_morphologies 10.1038_nature16468`
   wrapped in `run_with_logs.py` and fix any errors. Expected output: 0 errors from the verificator.
   Satisfies REQ-1, REQ-11 (paper half).

4. **Download the Dryad bundle** [CRITICAL]. Resolve `https://doi.org/10.5061/dryad.d9v38` to the
   Dryad download page, enumerate every file in the dataset version, and `curl -L` each file into
   `data/` wrapped in `run_with_logs.py`. After each download compute the SHA-256 hash
   (`python -c "import hashlib, sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()). hexdigest())" <file>`
   is fine; `certutil` is also acceptable on Windows) and append a record
   `{"path": "data/<filename>", "url": "<source url>", "bytes": <int>, "sha256": "<hex>"}` to
   `data/download_manifest.json`. Decompress any zip/tar.gz files in place under `data/`. Expected
   output: `data/download_manifest.json` lists every Dryad file with all four fields populated and
   every listed file exists on disk. Satisfies REQ-2.

5. **Download and extract the MATLAB visualisation zip**. Run
   `curl -L -o data/Baden_et_al_2016_visualization.zip http://retinal-functomics.net/wp-content/uploads/2015/12/Baden_et_al_2016_visualization.zip`
   wrapped in `run_with_logs.py`, then
   `python -m zipfile -e data/Baden_et_al_2016_visualization.zip data/visualization_code/`. Append
   the zip to `data/download_manifest.json` with its SHA-256. Open the top-level `*.m` MATLAB
   scripts (`Tabula_VolatileXX*.m`, `Run_Baden_2016*.m`, or similar — the actual file names emerge
   from the zip contents) and identify (a) which Dryad file holds cluster assignments, (b) which
   field name holds the cluster ID, (c) where per-cell traces are stored, and (d) where per-cell
   morphological data is stored if present. Write the findings to
   `code/visualization_code_notes.md`. Expected output: `data/visualization_code/` is non-empty and
   `code/visualization_code_notes.md` contains a "File and field mapping" subsection. Satisfies
   REQ-3.

6. **Download the Dryad README and cross-check field names**. Run
   `curl -L -o data/dryad_readme.txt https://datadryad.org/downloads/file_stream/3407` wrapped in
   `run_with_logs.py`. Append it to `data/download_manifest.json` with its SHA-256. Read the README
   and add a "README cross-check" subsection to `code/visualization_code_notes.md` confirming or
   contradicting the file/field mapping inferred from the MATLAB scripts. Any mismatch is flagged in
   the notes and resolved before Step 7. Expected output: `data/dryad_readme.txt` exists and the
   cross-check subsection lists each Dryad file with its README-stated purpose and
   visualisation-script usage side-by-side. Satisfies REQ-4.

### Milestone B — Reconcile cluster IDs and extract DS data

7. **Reconcile user-specified cluster IDs against the Dryad numbering** [CRITICAL]. Using the
   visualisation scripts as authoritative, build a mapping table for the 8 user-specified IDs
   `[2, 17, 18, 19, 22, 35, 36, 40]` to (a) the integer ID the Dryad data file actually stores, (b)
   the functional cell-type label the visualisation scripts assign to that ID (e.g. "OFF-DS",
   "ON-OFF-DS", "ON-DS", "displaced amacrine DS"), and (c) the count of cells the visualisation
   scripts report for that ID. Write the resolved mapping to a "Cluster ID reconciliation"
   subsection of `code/visualization_code_notes.md`. If any user-specified ID maps to a label that
   is **not** plausibly DS-related and the mapping is ambiguous, write
   `intervention/<timestamp>_cluster_id_ambiguity.json` describing the ambiguity with the full
   evidence trail and stop work here — do **not** silently substitute different clusters. Expected
   output: the reconciliation table is present in `code/visualization_code_notes.md`, OR an
   intervention file exists. Satisfies REQ-5.

8. **Implement the loader and run dry-run** [CRITICAL]. Write `code/load_baden.py` containing:
   * Constants: `DS_CLUSTER_IDS: list[int] = [2, 17, 18, 19, 22, 35, 36, 40]` (or the reconciled set
     from Step 7 if the user IDs map to different Dryad-internal IDs — in which case
     `DS_CLUSTER_IDS_USER` and `DS_CLUSTER_IDS_DRYAD` are both defined and the comment explicitly
     cites the reconciliation table line).
   * Paths constants pointing at the Dryad files identified in Step 5/6.
   * Loader function `load_dryad(*, dryad_dir: Path) -> RawBadenData` returning a frozen dataclass
     exposing the raw cluster assignments, traces, IPL depths, soma positions, metadata, and (if
     present) morphology arrays.
   * Filter function
     `filter_to_ds(*, raw: RawBadenData, cluster_ids: list[int]) -> list[CellRecord]` returning one
     `@dataclass(frozen=True, slots=True) CellRecord` per cell with **every per-cell field present
     in the Dryad release**. Use `None` for missing fields (per project python style — never
     zero/empty for "no measurement").
   * `.mat` reading: try `scipy.io.loadmat` first; on `NotImplementedError` (HDF5 v7.3) fall back to
     `mat73.loadmat`; on `mat73` import failure fall back to `h5py`. If `mat73` is needed, add it to
     `pyproject.toml` `[project] dependencies` and re-run `uv sync` (this is one of the four files
     outside the task folder that the framework permits to change).
   * A `--dry-run` CLI flag that prints, for each of the 8 reconciled clusters, the count of cells
     found and the list of per-cell field names present (so the human can sanity-check before the
     full write).
   * Morphology handling: when no morphology field is present for a cluster, set
     `cell.morphology = None` and record the absence in the per-cluster summary the dry-run prints.
     Run `uv run python -u code/load_baden.py --dry-run` wrapped in `run_with_logs.py`. Expected
     output: dry-run prints 8 cluster summaries (count + field list) and exits 0 with no errors.
     Satisfies REQ-6, REQ-8.

9. **Write the dataset asset** [CRITICAL]. Extend `code/load_baden.py` with a
   `write_asset(*, cells: list[CellRecord], asset_dir: Path) -> None` function that:
   * Chooses container format: Parquet if all `CellRecord` fields are tabular scalars, JSONL
     otherwise (e.g. when per-cell traces are variable-length arrays). Record the choice in
     `details.json` `files[0].format`.
   * Writes the per-cell records to
     `assets/dataset/baden-2016-ds-cells/files/baden-2016-ds-cells.<parquet|jsonl>`.
   * Writes `assets/dataset/baden-2016-ds-cells/details.json` (dataset asset spec v2) with
     `dataset_id = "baden-2016-ds-cells"`, `name = "Baden 2016 RGC DS subset"`, `version = null`,
     `source_paper_id = "10.1038_nature16468"`,
     `url = "https://datadryad.org/dataset/ doi:10.5061/dryad.d9v38"`, `download_url = null`,
     `year = 2016`, `date_published = "2016-01-21"`, `license = "CC0-1.0"` (Dryad default —
     confirm from the README; fall back to `null` if not stated), `access_kind = "public"`,
     `size_description = "<N> cells across 8 direction-selective groups from the Baden 2016 release, one record per cell with functional traces and IPL depth; morphologies <present|absent>"`,
     `categories = ["direction-selectivity", "retinal-ganglion-cell"]`,
     `description_path = "description.md"`. Author/institution lists come from the Baden 2016 paper
     metadata (Tom Baden, Philipp Berens, Katrin Franke, Miroslav Román Rosón, Matthias Bethge,
     Thomas Euler — Tübingen / Bernstein Centre).
   * Writes the canonical `assets/dataset/baden-2016-ds-cells/description.md` with all mandatory
     sections (Metadata, Overview, Content & Annotation, Statistics, Usage Notes, Main Ideas,
     Summary) and YAML frontmatter (`spec_version: "2"`, `dataset_id`, `summarized_by_task`,
     `date_summarized`). The Usage Notes section explicitly states the morphology status
     (present/absent) and how to load the chosen container format. Run
     `uv run python -u code/load_baden.py --write-asset` wrapped in `run_with_logs.py`. Run
     `uv run python -m arf.scripts.verificators.verify_dataset_asset --task-id t0103_extract_baden_2016_ds_morphologies baden-2016-ds-cells`
     wrapped in `run_with_logs.py` and fix any errors. Expected output: 0 verificator errors.
     Satisfies REQ-6, REQ-7, REQ-8, REQ-11 (dataset half).

### Milestone C — Cross-check counts and produce diagnostics

10. **Cross-check per-group cell counts**. Write `code/check_group_counts.py` that loads the
    produced dataset, computes the count of cells per cluster ID, and compares against the reference
    counts from the visualisation scripts (preferred; recorded in Step 7's reconciliation table) or
    from Figure 2 of Baden 2016 (fallback). Write the result to `code/group_count_check.json` as a
    list of 8 records
    `{"cluster_id": <int>, "produced_count": <int>, "reference_count": <int>, "reference_source": "visualization_scripts" | "figure_2", "delta_pct": <float>}`.
    Run `uv run python -u code/check_group_counts.py` wrapped in `run_with_logs.py`. Any group with
    `abs(delta_pct) > 5.0` is flagged in the script's stdout but does **not** halt the task (the
    discrepancy is a finding for the orchestrator's reporting step). Expected output:
    `code/group_count_check.json` exists with 8 entries. Satisfies REQ-9.

11. **Produce diagnostic charts**. Write `code/make_charts.py` that loads the dataset and produces:
    * `results/images/cell_counts_and_ipl.png` — a figure with two subplots: (top) bar chart of
      per-group cell count; (bottom) overlaid IPL stratification profile (mean +/- s.d. per group)
      on a shared depth axis.
    * `results/images/representative_traces.png` — a grid of 8 panels, one per group, each showing
      the cluster-mean response trace to the moving-bar stimulus (the standard Baden-2016
      DS-defining stimulus) with the time axis shared across panels. Use `matplotlib` only (already
      in the project environment). Run `uv run python -u code/make_charts.py` wrapped in
      `run_with_logs.py`. Expected output: both PNG files exist and are non-empty. Satisfies REQ-10.

The Step by Step ends at chart generation. Subsequent results-writing and reporting work is
orchestrator-owned and explicitly excluded from this plan per the planning skill spec.

## Remote Machines

None required. All work is local: HTTP downloads (Dryad, Nature, retinal-functomics.net), local
Python parsing of MATLAB and JSON/CSV files, and local matplotlib chart rendering. No GPU, no
training, no inference, no paid compute. Sufficient local resource: a few GB of disk and a modern
CPU.

## Assets Needed

Input materials this task consumes (all external, none from prior tasks since `task.json`
`dependencies = []`):

* The Baden 2016 paper PDF from `https://www.nature.com/articles/nature16468.pdf` (fallback: PubMed
  Central mirror under `PMC4734159`).
* The Dryad bundle at `https://doi.org/10.5061/dryad.d9v38`.
* The MATLAB visualisation zip at
  `http://retinal-functomics.net/wp-content/uploads/2015/12/Baden_et_al_2016_visualization.zip`.
* The Dryad README at `https://datadryad.org/downloads/file_stream/3407`.

No prior-task asset dependencies — this task seeds the Baden 2016 paper and dataset for downstream
consumers (t0090's parameter envelopes, t0102's joint-pass validation, future Baden-grounded
null-distribution tasks).

## Expected Assets

Matches `task.json` `expected_assets = {"dataset": 1, "paper": 1}`:

* **1 paper asset** at
  `tasks/t0103_extract_baden_2016_ds_morphologies/assets/paper/ 10.1038_nature16468/` — full v3
  spec compliance (PDF in `files/`, `details.json` with `citation_key = "Baden2016"` and
  `categories = ["direction-selectivity", "retinal-ganglion-cell"]`, canonical `summary.md` with all
  9 mandatory sections).

* **1 dataset asset** at
  `tasks/t0103_extract_baden_2016_ds_morphologies/assets/dataset/ baden-2016-ds-cells/` — v2 spec
  compliance (per-cell records in `files/baden-2016-ds-cells.parquet` or `.jsonl`, `details.json`
  linking to the Baden 2016 paper asset via `source_paper_id`, canonical `description.md` with all 7
  mandatory sections). Contains one record per cell for the 8 DS clusters with every per-cell field
  available in the Dryad release.

No library, model, prediction, answer, or suggestion assets — those are out of scope per
`task.json`.

## Time Estimation

* **Research**: 0 hours (deliberately skipped; brief is fully enumerated in `task_description.md`).
* **Milestone A — Download and inspect** (Steps 1-6): 1.0-2.0 hours. Dominated by Dryad download
  bandwidth (~1 GB) and MATLAB script reading.
* **Milestone B — Reconcile and extract** (Steps 7-9): 2.0-3.5 hours. The
  cluster-ID-reconciliation step (7) is the bottleneck if the user-vs-Dryad numbering schemes
  diverge; the loader implementation (8-9) is straightforward once the schema is known.
* **Milestone C — Cross-check and diagnostics** (Steps 10-11): 0.5-1.0 hours. Two short scripts.
* **Total wall-clock**: 3.5-6.5 hours of agent time, all local.

## Risks & Fallbacks

Risks identified by pre-mortem (imagining the task failed and working backwards):

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Dryad URL has rotted or returns an unexpected redirect | Low | Blocking download | Try alternate Dryad mirrors via the DOI; fall back to the paper's GitHub mirror if listed in the Nature article; if all fail, set the dataset asset's `download_status` analog (record in `details.json` `short_description`) and write `intervention/dryad_download_failed.json` with the full HTTP response trail |
| MATLAB visualisation zip URL (`retinal-functomics.net`) has rotted | Medium | Blocks REQ-3 and REQ-5 | Search the Wayback Machine (`web.archive.org`) for `Baden_et_al_2016_visualization.zip`; if found, use the archived copy; if not, infer the cluster-ID mapping directly from the Dryad README and the paper's Figure 2 caption and document the inference path in `code/visualization_code_notes.md` |
| User-specified cluster IDs (2, 17, 18, 19, 22, 35, 36, 40) do not align with the Dryad cluster numbering | Medium | Blocking — risks silently extracting wrong cells | Step 7 (REQ-5) reconciles via the visualisation scripts and writes the resolved mapping. If reconciliation is ambiguous (e.g. ID 35 maps to a non-DS label), write `intervention/cluster_id_ambiguity.json` and stop — do **not** substitute different cluster IDs |
| Dryad `.mat` files use HDF5 v7.3 which `scipy.io.loadmat` cannot read | Medium | Blocks loader | Step 8 falls back to `mat73.loadmat`, then to `h5py` direct read. `mat73` added to `pyproject.toml` if needed |
| Dryad release contains no morphological reconstructions for the 8 DS groups | High | Reduces dataset value but does NOT block the task | Per REQ-8, the loader continues and extracts every other per-cell field. The morphology absence is documented explicitly in `description.md` "Usage Notes" and in `code/visualization_code_notes.md`. The downstream tasks still benefit from functional traces and IPL depth. A follow-up task to source DS-cell morphologies from Bae 2018 or Ran 2020 is left for the orchestrator's suggestions step |
| Per-cell trace lengths are heterogeneous across cells/stimuli forcing JSONL over Parquet | Medium | Affects container format | The loader detects this in Step 9 and picks JSONL; the choice is recorded in `details.json` `files[0].format` so consumers know what to expect |
| Baden 2016 PDF behind paywall blocking the direct PDF URL | Low | Blocks REQ-1 | Step 2 falls back to the PubMed Central mirror (`PMC4734159`, open access); if both fail, mark `download_status = "failed"` per the paper asset spec v3 and provide a metadata-only summary built from the abstract and the Dryad README |
| Per-group cell counts deviate >5% from the reference (visualisation scripts or Figure 2) | Low | Quality flag, not blocking | Step 10's `code/group_count_check.json` records the deltas; the orchestrator's reporting step picks the finding up. If the delta is >50% on any single group, treat it as a loader bug and re-inspect Step 8's filter logic before proceeding to Step 11 |

## Verification Criteria

Each criterion has an exact command and an expected observable outcome. Run all commands wrapped in
`arf/scripts/utils/run_with_logs.py`.

* **Paper asset passes its verificator (covers REQ-1, REQ-11 paper half)**: run
  `uv run python -m arf.scripts.verificators.verify_paper_asset --task-id t0103_extract_baden_2016_ds_morphologies 10.1038_nature16468`.
  Expected: 0 errors. Warnings are acceptable but each must be either fixed or noted in
  `code/visualization_code_notes.md` with reasoning.

* **Dataset asset passes its verificator (covers REQ-6, REQ-7, REQ-11 dataset half)**: run
  `uv run python -m arf.scripts.verificators.verify_dataset_asset --task-id t0103_extract_baden_2016_ds_morphologies baden-2016-ds-cells`.
  Expected: 0 errors.

* **Download manifest exists and lists every Dryad file with SHA-256 (covers REQ-2)**: run
  `uv run python -c "import json, pathlib; d=json.loads(pathlib.Path('data/download_manifest.json').read_text()); assert all('sha256' in e and 'bytes' in e and 'path' in e for e in d); print(len(d), 'files')"`.
  Expected: prints a count >= 5 (Dryad files + MATLAB zip + README) and exits 0.

* **Visualisation code notes contain file/field mapping and README cross-check (covers REQ-3,
  REQ-4)**: run
  `uv run python -c "import pathlib; t=pathlib.Path('code/visualization_code_notes.md').read_text(); assert 'File and field mapping' in t and 'README cross-check' in t and 'Cluster ID reconciliation' in t; print('ok')"`.
  Expected: prints `ok` and exits 0.

* **Cluster-ID reconciliation completed without intervention (covers REQ-5)**: run
  `uv run python -c "import pathlib; ivs=list(pathlib.Path('intervention').glob('*cluster_id*.json')); print('intervention_files=', len(ivs))"`.
  Expected: prints `intervention_files= 0`. (If any cluster-ID intervention file exists, the
  orchestrator must resolve it before the task can be considered complete.)

* **Per-cell record count is positive (covers REQ-6, REQ-9)**: run
  `uv run python -u code/load_baden.py --report-counts`. Expected: prints 8 lines, one per cluster
  ID, each with a non-zero count, and the cluster IDs listed are exactly
  `[2, 17, 18, 19, 22, 35, 36, 40]` (or the reconciled Dryad-internal IDs corresponding to the
  user-specified IDs per Step 7).

* **Group count cross-check artefact exists (covers REQ-9)**: run
  `uv run python -c "import json, pathlib; d=json.loads(pathlib.Path('code/group_count_check.json').read_text()); assert len(d)==8 and all('delta_pct' in r for r in d); print('ok')"`.
  Expected: prints `ok` and exits 0.

* **Both diagnostic charts exist (covers REQ-10)**: run
  `uv run python -c "import pathlib; p1=pathlib.Path('results/images/cell_counts_and_ipl.png'); p2=pathlib.Path('results/images/representative_traces.png'); assert p1.exists() and p1.stat().st_size>0; assert p2.exists() and p2.stat().st_size>0; print('ok')"`.
  Expected: prints `ok` and exits 0.

* **No NEURON simulation, clustering, or generator code present (covers REQ-12 out-of-scope
  invariants)**: run
  `uv run python -c "import pathlib, re; py=' '.join(p.read_text() for p in pathlib.Path('code').rglob('*.py')); forbidden=['from neuron', 'import neuron', 'sklearn.cluster', 'KMeans', 'apply_parameter_vector', 'generate_morphology']; hits=[k for k in forbidden if k in py]; assert not hits, hits; print('ok')"`.
  Expected: prints `ok` and exits 0.

* **Plan verificator passes**: run
  `uv run python -m arf.scripts.verificators.verify_plan t0103_extract_baden_2016_ds_morphologies`.
  Expected: 0 errors.

## Alternative Approaches Considered

* **Three separate dataset assets (raw Dryad, MATLAB scripts, README) instead of one filtered
  asset.** Rejected: scatters provenance across three folders, fails the project's "no-duplication"
  principle, and the MATLAB code is a reading aid not a dataset. Single filtered asset is far more
  useful to downstream modelling tasks.

* **Include the full 11 000-cell Dryad release in the asset, not just the 8 DS groups.** Rejected:
  the task brief restricts scope to DS groups; pulling 32+ irrelevant clusters inflates the asset by
  an order of magnitude and forces every downstream consumer to filter again. If non-DS clusters are
  ever needed, that is a separate, explicitly-scoped task.

* **Skip the MATLAB visualisation zip and infer the cluster-ID mapping from the Dryad README
  alone.** Rejected: the README documents the file layout but the visualisation scripts are the only
  authoritative source for the cluster ID → cell-type-label mapping, and silently extracting wrong
  cells would corrupt every downstream task.

* **Re-write the MATLAB visualisation scripts in Python end-to-end.** Rejected explicitly in
  `task_description.md` "Out of scope" — would expand scope to a full port with no benefit to the
  downstream modelling tasks that only need the filtered per-cell data.

* **Defer the cluster-ID reconciliation to downstream consumers (just dump all 8 IDs as-is and let
  later tasks figure out which are DS).** Rejected: violates the one-task-one-purpose principle and
  would silently propagate a numbering bug across every consumer of the asset.
