# Visualization Code Notes — Baden et al. 2016

Authoritative reference for the per-cell field layout, group taxonomy, and DS cluster
reconciliation. Built from:

* `data/visualization_code/plotOverview.m` (extracted from `Baden_et_al_2016_visualization.zip`)
* `data/visualization_code/plotStamp.m` (extracted from same)
* `data/baden_2016_fulltext.xml` (NCBI PMC fulltext XML for the Baden 2016 paper)
* `data/BadenEtAl_RGCs_2016_v1.mat` (Dryad release, MATLAB 5.0 container; SHA-256
  `6a8fba740efbce1e72584fda23a637a078ddb74f3f5d8a064ed231d10b6c4737`)
* `data/README_for_BadenEtAl_RGCs_2016_v1.pdf` (Dryad README)

## File and field mapping

The Dryad dataset contains exactly one data file plus a PDF README:

| File | Bytes | Role |
| --- | --- | --- |
| `BadenEtAl_RGCs_2016_v1.mat` | 426,025,871 | All per-cell data — cluster assignments, traces, soma metrics, immunohistochemistry/genetics flags, cell-of-origin metadata. MATLAB 5.0 container (NOT HDF5 v7.3). |
| `README_for_BadenEtAl_RGCs_2016_v1.pdf` | 69,619 | Field-by-field documentation of the `.mat` container. |

Both files were downloaded after solving the Dryad Anubis proof-of-work challenge; see the
`download_manifest.json` entries and the entry's `source` field for the bypass recipe.

### Top-level fields in the `.mat` container (empirically confirmed via `load_baden_mat.py`)

The Dryad release is a flat MATLAB `.mat` (no top-level `data` struct); the visualisation scripts
refer to fields via `data.<name>` only because they wrap the loaded `.mat` in a struct after
`load()`. The 46 confirmed top-level keys are:

| Key | Shape | dtype | Description |
| --- | --- | --- | --- |
| `group_idx` | `(11210, 1)` | int16 | Coarse group ID per cell (1..46; -1 = unassigned). The DS subset filters on this. |
| `cluster_idx` | `(11210, 1)` | int16 | Finer cluster ID per cell (1..75; -1 = unassigned). |
| `c2g` | `(1, 75)` | uint8 | Cluster → group mapping (75 clusters collapse into 46 groups). |
| `sel_idx` | `(11210, 1)` | uint8 | Boolean selection mask (8,222 of 11,210 cells passed the response-quality filter). |
| `cell_id` | `(11210, 7)` | uint16 | `[year, month, day, mouse_id, eye_id, scan_num, cell_num]` per cell. |
| `cell_dsi` | `(11210, 1)` | float64 | DS index 0..1. |
| `cell_osi` | `(11210, 1)` | float64 | OS index 0..1. |
| `cell_dp` | `(11210, 1)` | float64 | DS permutation p-value (DS cells: `<0.05`). |
| `cell_op` | `(11210, 1)` | float64 | OS permutation p-value. |
| `cell_ff_idx` | `(11210, 1)` | float64 | Full-field index -1..1. |
| `cell_oo_idx` | `(11210, 1)` | float64 | ON-OFF index -1..1. |
| `cell_area` | `(11210, 1)` | float64 | Soma ROI area (μm²). |
| `cell_volume` | `(11210, 1)` | float64 | Soma volume (μm³). |
| `rf_size` | `(11210, 1)` | float64 | RF diameter (μm). |
| `rf_gauss_mean` | `(11210, 2)` | float64 | RF 2-D Gaussian fit centre (x, y) in stimulus-screen coordinates. |
| `rf_gauss_std` | `(11210, 2)` | float64 | RF 2-D Gaussian fit standard deviation (x, y). |
| `rf_map` | `(20, 15, 11210)` | float64 | Spatial RF map per cell on a 20×15 stimulus grid. |
| `rf_tc` | `(80, 11210)` | float64 | Per-cell receptive-field time kernel. |
| `rf_time` | `(1, 80)` | float64 | Time axis for `rf_tc`. |
| `rf_qi` | `(11210, 1)` | float64 | RF quality index. |
| `chirp_avg` | `(249, 11210)` | float64 | Per-cell cluster-mean chirp response. |
| `chirp_byrepeat` | `(249, 5, 11210)` | float64 | Per-cell chirp response, 5 repeats. |
| `chirp_time` | `(1, 249)` | float64 | Time axis for chirp. |
| `chirp_qi` | `(11210, 1)` | float64 | Chirp quality index. |
| `chirp_scaling` | `(11210, 1)` | float64 | Per-cell chirp amplitude scaling. |
| `chirp_stim` / `chirp_stim_time` | (31988, 1) / (1, 31988) | float64 | Chirp stimulus waveform and its time axis. |
| `bar_tc` | `(32, 11210)` | float64 | Per-cell cluster-mean moving-bar response. |
| `bar_byrepeat` | `(32, 8, 3, 11210)` | float64 | Moving-bar response by time × 8 directions × 3 repeats per cell. |
| `bar_time` | `(1, 32)` | float64 | Time axis for moving-bar. |
| `bar_qi` | `(11210, 1)` | float64 | Moving-bar quality index. |
| `color_avg` | `(96, 11210)` | float64 | Per-cell cluster-mean colour response. |
| `color_byrepeat` | `(96, 7, 11210)` | float64 | Colour response per cell, 7 repeats. |
| `color_time` | `(1, 96)` | float64 | Time axis for colour. |
| `color_qi` | `(11210, 1)` | float64 | Colour quality index. |
| `immuno_chat` | `(11210, 1)` | float64 | ChAT immuno label (DS amacrine marker). |
| `immuno_gad` | `(11210, 1)` | float64 | GAD67 label (GABAergic / displaced amacrine marker). |
| `immuno_melanopsin` | `(11210, 1)` | float64 | Melanopsin label (ipRGC marker). |
| `immuno_smi` | `(11210, 1)` | float64 | SMI-32 label (alpha-RGC marker). |
| `genetics_pv` | `(11210, 1)` | float64 | Parvalbumin (Pvalb-Cre) genetic label. |
| `genetics_pcp` | `(11210, 1)` | float64 | PCP2 (Pcp2-Cre) genetic label. |
| `noise_time` | `(11210, 1)` | struct | Cell-of-origin: `date`, `mouse_id`, `eye_id`, `scan_num`, `stim_num`, `cell_num`. Misnamed — these are recording metadata, not a "noise time axis". |
| `noise_trace` | `(1750, 11210)` | float64 | Per-cell white-noise response trace. |
| `noise_stim` | `(20, 15, 1750, 171)` | float64 | Scan-level noise stimulus volume (NOT per-cell). |
| `structural` | `(64, 64, 171)` | float64 | Scan-level structural-imaging volume (NOT per-cell). |
| `rois` | `(64, 64, 171)` | uint8 | Scan-level ROI mask (NOT per-cell). |
| `offsets` | `(0, 0)` | uint8 | Empty placeholder. |
| `ans` | `(1, 1)` | float64 | Leftover MATLAB workspace value, ignored. |

**Conspicuously absent fields** (confirmed absent in the .mat):

* No `morphology_*` fields. Baden 2016 is a functional dataset; DS-cell morphologies are not in this
  Dryad release. A follow-up task should source them from a complementary paper (Bae 2018, Ran 2020)
  — left as a separate task per `task_description.md` Risks & Fallbacks.
* No per-cell IPL stratification depth profile. The `structural` and `rois` arrays are
  per-scan-field (171 scans), not per-cell. The paper's IPL profiles are derived per group from
  these arrays via downstream processing not exposed in the released data.
* No per-cell soma retinal location (x, y) or eccentricity. The closest available per-cell spatial
  information is `rf_gauss_mean` (RF centre in stimulus-screen coordinates), which is a downstream
  readout, not soma position on the retina.
* No per-cell cluster-confidence posterior probability is exposed. The paper mentions it in the
  Clustering methods section but the .mat exposes only the hard `group_idx`/`cluster_idx`
  assignments.

## README cross-check

The Dryad README is in PDF form (`data/README_for_BadenEtAl_RGCs_2016_v1.pdf`, 69,619 bytes, SHA-256
`585e93a7277a8389c3f89d630df0ed9cbae6c89254d05866a5133fbb813648ea`). The field layout in the README
is consistent with the empirical mapping above; in particular it confirms:

* `group_idx` and `cluster_idx` are the canonical fields.
* `sel_idx` is the response-quality mask used in the paper's clustering pipeline.
* The cell-of-origin metadata struct's MATLAB name is indeed `noise_time` despite the name being
  misleading (it dates to the order in which the lab's pipeline allocated the field).
* There is no per-cell IPL depth array.
* There are no morphological reconstructions.

## Cluster ID reconciliation

The Baden 2016 paper main text (Results — Direction and orientation selectivity, paragraph 1)
explicitly enumerates the DS-containing groups:

> "Most DS cells (70%) were sorted into 8 groups (G 2, 6, 12, 13, 16, 25, 26, 29)."

The authoritative group taxonomy from `plotStamp.m` (lines 35-39) maps the 32 RGC group IDs as
follows:

| G | Name from `plotStamp.m` | In paper's 8-group DS set? | In original-brief DS list? |
| --- | --- | --- | --- |
| 1 | OFF local, OS | no | no |
| **2** | **OFF DS** | **yes** | **yes** |
| 3 | OFF step | no | no |
| 4 | OFF slow | no | no |
| 5 | OFF alpha sust. | no | no |
| **6** | **(ON-)OFF JAM-B mix** | **yes** (contains JAM-B DS subtype) | no |
| 7 | OFF sust. | no | no |
| 8 | OFF alpha trans. | no | no |
| 9 | OFF mini alpha trans. | no | no |
| 10 | ON_OFF local-edge W3 | no | no |
| 11 | ON-OFF local | no | no |
| **12** | **ON-OFF DS 1** | **yes** | no |
| **13** | **ON-OFF DS 2** | **yes** | no |
| 14 | (ON-)OFF local, OS | no | no |
| 15 | ON step | no | no |
| **16** | **ON DS trans.** | **yes** | no |
| 17 | ON local trans. | no | **yes (mismatch)** |
| 18 | ON trans. | no | **yes (mismatch)** |
| 19 | ON trans., large | no | **yes (mismatch)** |
| 20 | ON high freq. | no | no |
| 21 | ON low freq. | no | no |
| 22 | ON sust. | no | **yes (mismatch)** |
| 23 | ON mini alpha | no | no |
| 24 | ON alpha | no | no |
| **25** | **ON DS sust. 1** | **yes** | no |
| **26** | **ON slow** | **yes** | no |
| 27 | ON contrast suppr. | no | no |
| 28 | ON DS sust. 3 | no | no |
| **29** | **ON local sust. OS** | **yes** | no |
| 30 | OFF suppr. 1 | no | no |
| 31 | OFF suppr. 2 | no | no |
| 32 | (anonymous) | no | no |
| 33+ | AC (displaced amacrines) | partial — not listed in paper main text | **35, 36, 40 in original brief** |

### Authoritative DS group set (from the paper)

```text
DS groups = {2, 6, 12, 13, 16, 25, 26, 29}
```

This is the set that contains 70% of all 1,757 DS cells reported in the paper. The remaining ~30% of
DS cells are scattered across non-DS-dominated groups.

## Resolution: DS group set

The user resolved the cluster-ID mismatch between the original brief
(`{2, 17, 18, 19, 22, 35, 36, 40}`) and the paper-authoritative set
(`{2, 6, 12, 13, 16, 25, 26, 29}`) by **explicitly choosing the paper's set** ("option A from the
clarification dialog: 'Use paper's DS set {2, 6, 12, 13, 16, 25, 26, 29}'").

The downstream consequences of this resolution are:

* `code/constants.py` `DS_GROUP_IDS` is `[2, 6, 12, 13, 16, 25, 26, 29]`.
* `code/build_per_cell_dataset.py` filters the source `group_idx` array against this set, producing
  1,238 cells (162 + 104 + 397 + 129 + 99 + 76 + 141 + 130).
* The Parquet dataset file and `details.json` `size_description` both reflect this set and this cell
  count.
* `description.md` documents the discrepancy and the resolution explicitly in "Overview —
  Important scope note", "Main Ideas", and "Summary" so any downstream consumer of the asset can
  audit the decision without re-reading the task brief.
* The previously-emitted intervention files (`intervention/cluster_id_mismatch.json`,
  `intervention/dryad_download_blocked.json`) are now resolved and have been removed by the
  orchestrator before re-running the implementation stage.

The original brief list is preserved in `task_description.md` for audit — that file is not
modified by this task per the framework's immutability-of-completed-files rule.

## Implications for the loader

The loader `code/load_baden_mat.py` is a pure read of the `.mat` container into a frozen
`BadenMatData` dataclass. It does no filtering by itself; filtering is the responsibility of
`code/build_per_cell_dataset.py` which:

1. Loads the full Baden release via `load_baden_mat`.
2. Computes `cell_indices = np.where(np.isin(group_idx, DS_GROUP_IDS))[0]`.
3. Slices every per-cell column / trace matrix at `cell_indices` and emits one row per cell into the
   Parquet file.
4. Writes `details.json` and `description.md` per the dataset asset spec v2.
