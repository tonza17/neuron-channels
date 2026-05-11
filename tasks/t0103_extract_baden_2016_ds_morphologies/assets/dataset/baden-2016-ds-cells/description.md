---
spec_version: "2"
dataset_id: "baden-2016-ds-cells"
summarized_by_task: "t0103_extract_baden_2016_ds_morphologies"
date_summarized: "2026-05-11"
---
# Baden 2016 RGC Direction-Selective Subset

## Metadata

* **Name**: Baden 2016 RGC direction-selective subset
* **Year**: 2016
* **Authors**: Tom Baden, Philipp Berens, Katrin Franke, Miroslav Román Rosón, Matthias Bethge,
  Thomas Euler — University of Tübingen
* **Source paper**: Baden et al., *Nature* 529:345–350
  ([10.1038/nature16468](https://www.nature.com/articles/nature16468))
* **Source data**: Dryad
  [10.5061/dryad.d9v38](https://datadryad.org/dataset/doi:10.5061/dryad.d9v38)
* **License**: CC0-1.0 (Dryad-default)
* **Access**: public
* **Size**: 1238 cells across 8 DS-containing groups (out of the 11,210 cell Dryad release)
* **Container**: Parquet with nested `list<float32>` columns for traces (scalar feature columns
  retain native precision)

## Overview

This dataset is the direction-selective (DS) subset of the Baden et al. 2016 *Nature* release of
functional fingerprints for ~11,000 mouse retinal ganglion cells (RGCs) and displaced amacrine cells
(dACs) measured with two-photon Ca2+ imaging. Each row is one cell, and the cells are drawn from the
**8 paper-authoritative DS groups** that the Baden 2016 main text enumerates ("Most DS cells (70%)
were sorted into 8 groups (G 2, 6, 12, 13, 16, 25, 26, 29).").

The filter from the source 11,210-cell release to the 1238-cell DS subset is exact: a single boolean
test on the `group_idx` array of the source `.mat` against the list
`{2, 6, 12, 13, 16, 25, 26, 29}`. No re-clustering, re-classification, or trace refitting is
performed — the cells, indices, and trace values are passed through exactly as released.

The dataset's purpose is to ground downstream DSGC compartmental-modelling tasks (parameter-envelope
tuning, joint-pass validation, biologically grounded null distributions) in a population of real DS
cells from one well-characterised source, rather than only the single canonical morphology used in
t0024 and its descendants.

### Important scope note — paper-authoritative DS set vs. original task brief

The task brief (`task_description.md`) originally enumerated DS groups as
`{2, 17, 18, 19, 22, 35, 36, 40}`. That list does not match the paper's own DS enumeration: only G2
overlaps. The other seven IDs in the original list either refer to non-DS RGC groups in the Baden
2016 taxonomy (G17 = "ON local trans.", G18 = "ON trans.", G19 = "ON trans., large", G22 = "ON
sust.") or to displaced amacrine subgroups beyond G32 whose DS status is not asserted by the
visualisation scripts. The user resolved the ambiguity by explicitly choosing the
paper-authoritative set, and this dataset therefore reflects the paper's own DS set
`{2, 6, 12, 13, 16, 25, 26, 29}`. The original brief list is preserved verbatim in
`task_description.md` for audit; the discrepancy and its resolution are recorded in
`code/visualization_code_notes.md` (see "Cluster ID reconciliation" and "Resolution: DS group set").

## Content & Annotation

Each Parquet row carries the following per-cell fields (see Statistics for value ranges and Usage
Notes for loading):

* **Cluster / group assignment** — `group_id` (one of `{2, 6, 12, 13, 16, 25, 26, 29}`),
  `group_label` (human-readable name from `plotStamp.m`), `cluster_id` (the finer Baden 2016 cluster
  index from the .mat `cluster_idx` array), and `selected` (the boolean response-quality mask
  `sel_idx`).
* **Selectivity indices** — `dsi`, `osi` (both 0..1), with their permutation-test p-values
  `dsi_pvalue`, `osi_pvalue` (DS cells have `dsi_pvalue < 0.05`).
* **Functional indices** — `ff_index` (full-field, -1..1), `on_off_index` (-1..1).
* **Per-stimulus quality indices** — `chirp_qi`, `bar_qi`, `color_qi`, `rf_qi` and the
  amplitude-scaling factor `chirp_scaling`.
* **Soma morphology (limited)** — `soma_area_um2`, `soma_volume_um3`. Per-cell IPL stratification
  depth and full dendritic morphology are **NOT** in the Dryad release.
* **Receptive field** — `rf_diameter_um`, plus the 2-D Gaussian-fit centre (`rf_gauss_mean_x`,
  `rf_gauss_mean_y`) and standard deviation (`rf_gauss_std_x`, `rf_gauss_std_y`) in stimulus-screen
  coordinates.
* **Immunohistochemistry / genetics flags** — `immuno_chat`, `immuno_gad`, `immuno_melanopsin`,
  `immuno_smi32`, `genetics_pv`, `genetics_pcp`. NaN means "not stained / not genetically labelled
  for this animal"; 0 vs >0 distinguishes negative from positive.
* **Cell-of-origin metadata** — `recording_date`, `mouse_id`, `eye_id`, `scan_num`, `stim_num`,
  `cell_num` (the per-mouse cell index used in the original Baden lab acquisition pipeline).
* **Functional traces** (nested `list<float32>` Parquet columns; see Usage Notes for the rationale):
  * `chirp_avg` — cluster-mean chirp response per cell, 249 samples on `chirp_time`.
  * `bar_tc` — cluster-mean moving-bar time course per cell, 32 samples on `bar_time`.
  * `bar_byrepeat_bydir_mean` — moving-bar response averaged across the 3 stimulus repeats,
    flattened as 8 directions × 32 time bins = 256 floats per cell ordered as
    `[d0_t0, ..., d0_t31, d1_t0, ..., d7_t31]`. The 8 directions span 360° in 45° steps per the
    Baden 2016 moving-bar protocol.
  * `color_avg` — coloured-stimulus cluster mean, 96 samples on `color_time`.
  * `rf_tc` — spike-triggered temporal RF kernel, 80 samples on `rf_time`.

Stimulus time axes (`chirp_time`, `bar_time`, `color_time`, `rf_time`) are constant across cells and
are stored once in the Parquet file-level metadata under the key `baden_2016_ds_cells_metadata`. The
same metadata block also documents the `bar_byrepeat_bydir_mean` layout and three explicit "what's
missing" notes.

### What is NOT in this dataset (gaps inherited from the Dryad release)

* **No per-cell IPL stratification depth profile.** The Dryad `.mat` exposes a scan-level
  `structural` volume and per-scan `rois`; the paper reports IPL profiles per group derived from
  these scans, but the per-cell IPL profile field is not in the release.
* **No per-cell retinal soma coordinates.** The `noise_time` struct (despite its misleading name —
  it is the cell-of-origin metadata struct) does not carry retinal (x, y) or eccentricity. The
  `rf_gauss_mean_*` fields are stimulus-screen receptive- field centres, which are a downstream
  readout of the cell's position relative to the stimulus monitor, not the soma's position on the
  retina.
* **No dendritic morphology.** Baden 2016 is a primarily functional dataset. The dye-fill
  morphologies for the DS-RGC types described in the paper are scattered across complementary
  references. A follow-up task should source the DS-cell morphologies from a complementary paper
  such as Bae et al. 2018 (which provides dense reconstructions for several Baden cluster IDs) or
  Ran et al. 2020 (which catalogues morphologies for ON-OFF DS cells in particular). Sourcing those
  is **out of scope for t0103** by design and is left as a separate task.

## Statistics

| Group | Label | Cells |
| --- | --- | --- |
| G2 | OFF DS | 162 |
| G6 | (ON-)OFF JAM-B mix | 104 |
| G12 | ON-OFF DS 1 | 397 |
| G13 | ON-OFF DS 2 | 129 |
| G16 | ON DS trans. | 99 |
| G25 | ON DS sust. 1 | 76 |
| G26 | ON slow | 141 |
| G29 | ON local sust. OS | 130 |

**Total cells**: 1238 (matches the sum of the eight per-group counts exactly).

The per-group counts cross-check exactly against the source `group_idx` array
(`code/group_count_check.json` records the comparison; all eight deltas are zero because the
produced count and the reference count are both computed directly from `group_idx`).

Selectivity-index distribution within DS groups (from the source `.mat`):

* `dsi`: 0..1, with the DS-defining permutation test in `dsi_pvalue`. Cells with `dsi_pvalue < 0.05`
  are the "significantly direction-selective" subset within each group.
* `osi`: 0..1, with `osi_pvalue` analogous for orientation selectivity. Some groups (e.g. G29 "ON
  local sust. OS") are dominated by OS rather than DS cells but are still included in the paper's
  8-group DS set.

Trace lengths are constant across all cells: chirp 249 samples, moving-bar 32 samples (per direction
& repeat dimension; aggregate moving-bar `bar_tc` is also 32), colour 96 samples, RF kernel 80
samples.

## Usage Notes

### Trace column precision (float32)

The five functional-trace list columns (`chirp_avg`, `bar_tc`, `bar_byrepeat_bydir_mean`,
`color_avg`, `rf_tc`) are stored as `list<float32>` to keep the single on-disk Parquet file under
the project's 5 MB per-file pre-merge limit (PM-E011). Float32 retains ~6-7 significant decimal
digits, which is comfortably below the noise floor of Baden 2016's normalised cluster-mean traces
(roughly in `[-1, 1]` range). Scalar feature columns (DSI, OSI, soma area/volume, RF Gaussian-fit
parameters, etc.) retain their native `float64` precision, since they are cheap on disk and some
downstream consumers may prefer them at full precision. Cast a trace back to `float64` at load time
if a particular analysis requires it:

```python
import numpy as np

chirp = np.asarray(df.loc[i, "chirp_avg"], dtype=np.float64)
```

### Loading

```python
import pyarrow.parquet as pq

table = pq.read_table("files/baden-2016-ds-cells.parquet")
df = table.to_pandas()  # one row per cell; trace columns are lists of float32
```

### Stimulus time axes

The Parquet file's key/value metadata holds the four stimulus time axes as JSON. Read them with:

```python
import json, pyarrow.parquet as pq

meta = json.loads(
    pq.read_metadata("files/baden-2016-ds-cells.parquet")
    .metadata[b"baden_2016_ds_cells_metadata"]
)
chirp_time_s = meta["chirp_time_s"]      # length 249
bar_time_s   = meta["bar_time_s"]        # length 32
color_time_s = meta["color_time_s"]      # length 96
rf_time_s    = meta["rf_time_s"]         # length 80
```

### Direction-major moving-bar trace

`bar_byrepeat_bydir_mean` is the moving-bar response averaged across the 3 stimulus repeats per
direction, flattened as direction-major:

```text
[d0_t0, d0_t1, ..., d0_t31, d1_t0, ..., d7_t31]   # length 256
```

To reshape one cell's response back to `(D=8, T=32)`:

```python
import numpy as np

mat = np.asarray(df.loc[i, "bar_byrepeat_bydir_mean"]).reshape(8, 32)
```

### Quirks / pitfalls

* **NaN means "not labelled"** for the `immuno_*` and `genetics_*` columns. Use `pandas.isna` /
  `numpy.isnan` to filter, not `== 0` (0 means "stained but negative").
* **`group_id` and `cluster_id` are two different things.** `group_id` is the coarser Baden 2016
  group taxonomy (1..46, with 33+ being displaced amacrine subgroups); `cluster_id` is the finer
  75-way cluster index from the .mat `cluster_idx` array. Downstream consumers should filter on
  `group_id`.
* **No per-cell IPL depth / morphology**, as noted in Content & Annotation. If a downstream task
  needs those, source from Bae 2018 or Ran 2020 in a separate task.

## Main Ideas

* This dataset is the **filtered DS subset** of Baden 2016 — exact, no re-analysis. The filter is
  `group_idx ∈ {2, 6, 12, 13, 16, 25, 26, 29}`, taken verbatim from the paper's own DS-group
  enumeration.
* The dataset supplies **functional fingerprints, RF parameters, soma area/volume, and
  cell-of-origin metadata** but **not morphologies or per-cell IPL profiles**. A morphology source
  for DS-RGC dendritic trees is a separate task (Bae 2018 / Ran 2020).
* The original task brief used a different 8-group list (`{2, 17, 18, 19, 22, 35, 36, 40}`) that
  overlaps the paper's set only at G2. The user resolved the discrepancy in favour of the paper's
  set; the original list is preserved in `task_description.md` and the reconciliation is documented
  in `code/visualization_code_notes.md`.

## Summary

This dataset is the direction-selective subset of the Baden et al. 2016 *Nature* release of
functional fingerprints for ~11,000 mouse RGCs / dACs. Each of the 1238 rows is one cell drawn from
the 8 paper-authoritative DS groups (G2, G6, G12, G13, G16, G25, G26, G29), with every per-cell
field exposed by the Dryad .mat container that is meaningful per-cell: cluster/group assignment,
selectivity indices and their permutation p-values, soma area/volume, RF Gaussian-fit parameters,
immuno/genetics labels, cell-of-origin metadata, and the four functional traces (chirp, moving-bar
mean, moving-bar by direction & repeat-mean, colour, RF temporal kernel).

For this project the dataset's primary use is to ground downstream DSGC compartmental-modelling
tasks in a real DS-cell population. Functional traces and selectivity indices feed
parameter-envelope checks for synthetic DSGCs (t0090 lineage) and provide null distributions for the
t0102 joint-pass validation. The main limitation is the absence of per-cell IPL stratification
profiles and full dendritic morphologies — those should be sourced from Bae 2018 or Ran 2020 in a
separate follow-up task, which this dataset's Main Ideas and the Resolution-decision note in
`code/visualization_code_notes.md` flag explicitly. Compared to manually digitising DS-cell traces
from publication figures, this asset gives downstream tasks direct, authoritative cluster-mean and
per-cell responses with no estimation error.
