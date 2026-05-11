# t0103 — Extract direction-selective cell data from Baden et al. 2016

## Motivation

The project's DSGC compartmental modelling work (t0024 substrate plus the morphology generator
lineage t0090/t0092/t0093) currently relies on a single canonical morphology from De Rosenroll et
al. 2026 and parametric variants synthesised by the t0090 generator. To ground the parameter ranges
(dendritic field diameter, branch count, total length, asymmetry) in biological data we need a
population of real, identified direction-selective (DS) RGC morphologies and their co-recorded
functional fingerprints from a single well-characterised source.

Baden, Berens, Franke, Román Rosón, Bethge & Euler (2016), "The functional diversity of retinal
ganglion cells in the mouse", Nature 529:345–350, classified ~11 000 mouse RGCs and displaced
amacrine cells into >40 functional groups using two-photon Ca2+ imaging and a battery of light
stimuli. The dataset on Dryad accompanies the paper and contains, per cell: cluster assignment, soma
position, IPL stratification depth, response traces, and (for a subset) morphological
reconstructions obtained from dye fills during the patch-clamp follow-ups.

This task downloads the source materials and extracts data only for the 8 DS groups the user has
identified, producing one dataset asset that the downstream modelling tasks (extending t0090's
parameter envelopes, validating t0102's joint-pass corner, building Baden-grounded null
distributions) can import directly. The Baden 2016 paper itself is also added as a paper asset.

## Sources

* **Paper**: Baden et al. 2016, *Nature*, DOI
  [10.1038/nature16468](https://www.nature.com/articles/nature16468).
* **Dataset**: Dryad, DOI
  [10.5061/dryad.d9v38](https://datadryad.org/dataset/doi:10.5061/dryad.d9v38).
* **MATLAB visualisation code**: the lab-distributed zip at
  `http://retinal-functomics.net/wp-content/uploads/2015/12/Baden_et_al_2016_visualization.zip`.
  This zip contains the canonical scripts that map cluster IDs to cell counts, IPL depth, and
  morphological summary statistics — use it as the authoritative reference for the cluster→data
  mapping and any non-obvious data layout choices.
* **README**: `https://datadryad.org/downloads/file_stream/3407` — Dryad-hosted text README that
  documents the file layout and field meanings.

## Scope

### Groups to extract (DS only)

Extract data **only** for the following 8 direction-selective groups from the Baden 2016 taxonomy:

* Group **2** — OFF-type direction-selective cell.
* Group **17** — ON–OFF direction-selective subtype.
* Group **18** — ON–OFF direction-selective subtype.
* Group **19** — ON–OFF direction-selective subtype.
* Group **22** — ON direction-selective cell.
* Group **35** — displaced amacrine / DS-related (cluster numbering in the extended >32 group
  taxonomy used by the Dryad release).
* Group **36** — displaced amacrine / DS-related.
* Group **40** — displaced amacrine / DS-related.

If the Dryad data layout or the visualisation-zip scripts label these clusters with names that do
not match "DS" — e.g. an off-by-one or numbering scheme that puts the 4 canonical ON–OFF DS
subtypes in different IDs — the implementation step must reconcile the user's group list against
the labels in the actual data using the visualisation scripts as the authoritative mapping, and
record the resolution in `research/research_code.md`. Do not silently substitute different groups
— if the user-specified IDs cannot be located, write an intervention file.

### What to extract per group

For each of the 8 groups, extract every per-cell field available in the Dryad release. At minimum
this should include, when present in the data:

* Cluster / group ID and confidence.
* Soma position (retinal location: x, y or eccentricity/dorsoventral coordinates).
* IPL stratification depth profile.
* Functional response traces to the standard Baden 2016 stimulus set (chirp, moving bars,
  full-field, coloured, etc.) and any extracted features (DS index, OS index, polarity, transience,
  preferred direction, response quality, etc.).
* Morphological reconstruction, if available — dendritic tree (SWC or equivalent point list) and
  any derived per-cell shape statistics (field diameter, total dendritic length, branch points,
  asymmetry vector).
* Cell-of-origin metadata: retina ID, eye, dorsoventral location, age, sex if recorded.

If the Dryad release does **not** contain morphological reconstructions for these groups (plausible
— Baden 2016 is primarily a functional dataset, and morphologies for DS cells may have been added
in a companion paper such as Bae et al. 2018, Ran et al. 2020, or others), document the absence
explicitly in `research/research_code.md` and in the dataset asset's `description.md`. Continue to
extract whatever per-cell data is present — the downstream modelling tasks still benefit from the
functional fingerprints and stratification depths even without morphologies.

### Out of scope

* Re-classifying the Baden 2016 data into new groups.
* Re-analysing the raw Ca2+ traces — extract them as-is and let downstream tasks decide what to do
  with them.
* Refitting the visualisation scripts or porting them from MATLAB to Python beyond the minimum
  needed to read the data files. If a MATLAB→Python data load is needed, prefer using `scipy.io`
  or `mat73` rather than rewriting analysis code.
* Adding non-DS Baden groups (their data are not needed for the DSGC modelling line).
* Cross-paper integration with later Baden lab releases (e.g. Bae 2018, Goetz 2022) — those are
  separate tasks if they turn out to be needed.

## Approach

1. Download the Baden 2016 paper PDF and register it as a paper asset under
   `assets/paper/10.1038_nature16468/` following `meta/asset_types/paper/specification.md`.

2. Download the Dryad bundle (the full archive) into a task-local `data/` folder via `wget`/`curl`,
   recording byte sizes and SHA-256 hashes. The Dryad doi resolves to a download page that may
   package multiple files; pull every file in the archive.

3. Download the visualisation MATLAB zip and extract it into `data/visualization_code/`. Inspect the
   top-level scripts to identify (a) which Dryad file contains the cluster assignments, (b) which
   field name holds the cluster ID, and (c) where per-cell traces and any morphological data are
   stored.

4. Download the Dryad README from `https://datadryad.org/downloads/file_stream/3407` and save it
   under `data/`. Cross-reference its field list against what the visualisation scripts actually
   load.

5. Write a small Python loader in `code/` that:
   * Loads the per-cell cluster assignments.
   * Filters to the 8 DS groups listed above.
   * Pulls every available per-cell field for those cells (functional traces, IPL depth, soma
     position, morphology if present, etc.) into a clean per-cell record.
   * Writes the result to a single dataset asset under `assets/dataset/baden-2016-ds-cells/`, using
     a Parquet or JSONL container (whichever is the simpler match for the source field shapes).

6. Verify the per-group cell counts against the counts reported in Figure 2 of Baden 2016 (or in the
   visualisation scripts' summary outputs) and record the comparison in
   `results/results_detailed.md`. A material discrepancy (>5%) is a finding worth flagging; an exact
   match validates the filter logic.

7. Produce at least two diagnostic charts in `results/images/`:
   * One chart showing cell counts and IPL stratification per extracted group.
   * One chart showing one representative response trace per group (e.g. the cluster mean to the
     moving-bar stimulus that defines DS).

## Expected Assets

* **1 dataset asset** under `assets/dataset/baden-2016-ds-cells/` containing the extracted per-cell
  records for groups 2, 17, 18, 19, 22, 35, 36, and 40.

* **1 paper asset** under `assets/paper/10.1038_nature16468/` for the Baden 2016 paper itself (full
  v3 spec compliance — abstract, full-text summary, citation_key `Baden2016`, categories
  `direction-selectivity` and `retinal-ganglion-cell`).

## Cost Estimation

* Compute: $0. Local data download and extraction only. No remote machine, no paid API.
* Network: downloading the Dryad archive (estimated <1 GB) and one PDF — well within bandwidth
  budget.

## Time Estimation

* Download and decompress: 30-60 minutes.
* MATLAB-zip inspection and loader prototyping: 1-3 hours.
* Dataset asset assembly and diagnostic charts: 1-2 hours.
* **Total wall-clock**: 3-6 hours, all local.

## Risks & Fallbacks

* **Risk**: Dryad URL or visualisation zip have rotted. **Fallback**: fetch the dataset from the
  paper's GitHub mirror or contact the corresponding author. If unrecoverable, mark the dataset
  asset's download_status as failed and record the failure with full evidence in `intervention/`.

* **Risk**: User-specified group IDs do not match the Dryad cluster numbering. **Fallback**: use the
  visualisation scripts to map cluster IDs to functional cell-type labels and reconcile. If
  reconciliation is ambiguous, write an intervention file before producing the dataset asset.

* **Risk**: Morphological reconstructions are not in this Dryad release (Baden 2016 is primarily a
  functional dataset). **Fallback**: extract whatever IS available (functional traces, IPL
  stratification, soma position) and clearly state the morphology gap in the dataset asset's
  `description.md`; recommend a follow-up task to source DS-cell morphologies from a complementary
  paper such as Bae et al. 2018 or Ran et al. 2020 — but defer that as a separate task, do NOT
  expand scope here.

* **Risk**: MATLAB `.mat` files use the HDF5 v7.3 format that `scipy.io.loadmat` cannot read.
  **Fallback**: use `mat73` (or `h5py` directly) — add as a project-level dependency in
  `pyproject.toml` if not present.

## Verification Criteria

* `verify_task_file t0103_extract_baden_2016_ds_morphologies` passes with 0 errors.
* The dataset asset passes its verificator (paths to be filled in during planning).
* The paper asset passes its verificator.
* Per-group cell counts in the produced dataset asset are reported in `results_detailed.md` and
  cross-checked against either Baden 2016 Figure 2 or the visualisation scripts' own summaries.
* At least one diagnostic chart per the Approach is embedded in `results_detailed.md`.

## Out of Scope (explicit)

* Running NEURON simulations on the extracted morphologies — that is a downstream task.
* Building a parametric generator that mimics the Baden DS-cell morphologies — also downstream.
* Re-classifying or re-clustering Baden's data.
* Extending to non-DS groups.
* Integrating other Baden-lab data releases beyond the 2016 Nature paper.
