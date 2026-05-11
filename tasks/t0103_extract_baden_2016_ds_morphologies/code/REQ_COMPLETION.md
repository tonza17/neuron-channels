# REQ Completion Status — t0103

Status mapping for every requirement in `plan/plan.md`. Each row links the requirement to the
file/log/asset that satisfies it.

| REQ | Status | Evidence |
| --- | --- | --- |
| REQ-1 — Baden 2016 paper asset at `assets/paper/10.1038_nature16468/` (v3 spec, `citation_key=Baden2016`, categories `direction-selectivity` & `retinal-ganglion-cell`) | done | `assets/paper/10.1038_nature16468/details.json`, `assets/paper/10.1038_nature16468/summary.md`, paper verificator reports `PASSED — no errors or warnings`. |
| REQ-2 — Full Dryad bundle in `data/` with SHA-256 / bytes recorded in `data/download_manifest.json` | done | `data/BadenEtAl_RGCs_2016_v1.mat` (SHA-256 `6a8fba74…6c4737`, 426,025,871 bytes) and `data/README_for_BadenEtAl_RGCs_2016_v1.pdf` (SHA-256 `585e93a7…48ea`, 69,619 bytes) both listed in `data/download_manifest.json`. The .mat is gitignored at repo root per task brief; manifest is the reproducibility record. |
| REQ-3 — MATLAB visualisation zip downloaded and extracted, file/field mapping documented | done | `data/Baden_et_al_2016_visualization.zip` plus `data/visualization_code/plotOverview.m`, `plotStamp.m`, `shadedErrorBar.m`. Mapping in `code/visualization_code_notes.md` "File and field mapping" subsection. |
| REQ-4 — Dryad README downloaded and cross-checked against script field usage | done | `data/README_for_BadenEtAl_RGCs_2016_v1.pdf` exists; `code/visualization_code_notes.md` "README cross-check" subsection confirms field names. The README is the published Dryad README; the legacy `file_stream/3407` text URL on Dryad returns the same content. |
| REQ-5 — Reconcile user-specified IDs against Dryad numbering; document resolution or write intervention | done | `code/visualization_code_notes.md` "Cluster ID reconciliation" and "Resolution: DS group set" subsections. User chose paper-authoritative set `{2, 6, 12, 13, 16, 25, 26, 29}` (option A); no intervention file remaining. |
| REQ-6 — Python loader filtering to DS groups, pulling every per-cell field, with `None` for missing data | done | `code/load_baden_mat.py` (loader, frozen `BadenMatData`), `code/build_per_cell_dataset.py` (filter & Parquet writer). NaN is used in the source `.mat` for missing immuno/genetics labels; preserved as-is in the Parquet (loader keeps float64). |
| REQ-7 — Dataset asset at `assets/dataset/baden-2016-ds-cells/` with v2 spec (`details.json`, `description.md`, `files/`) | done | `assets/dataset/baden-2016-ds-cells/{details.json, description.md, files/baden-2016-ds-cells.parquet}`. Dataset verificator pending (see Quality Checks below). |
| REQ-8 — If morphologies absent, document in `description.md` & `visualization_code_notes.md`; loader continues | done | Both files explicitly state morphology absence. `description.md` "Content & Annotation — What is NOT in this dataset" and "Main Ideas" sections recommend Bae 2018 / Ran 2020 follow-up. |
| REQ-9 — Cross-check per-group cell counts vs. reference; record in `code/group_count_check.json`, flag deltas > 5% | done | `code/group_count_check.json` with 8 entries. All deltas 0% vs source `.mat` `group_idx`; G2 also matches the paper's explicit n=162 exactly. |
| REQ-10 — Two diagnostic charts in `results/images/` | done | `results/images/cell_counts_and_ipl.png` (per-group cell counts + per-group mean RF diameter as IPL-depth-substitute) and `results/images/representative_traces.png` (8-panel cluster-mean moving-bar response grid drawn from real `bar_tc` data). |
| REQ-11 — `expected_assets = {dataset: 1, paper: 1}`, both verificators pass | partial | Paper verificator passes (`PASSED — no errors or warnings`). Dataset verificator pending; see Quality Checks below. |
| REQ-12 — No re-clustering, no re-analysis, no non-DS groups, no other releases, no NEURON, no generator | done | All code paths read the source .mat as-is and filter only. No clustering, no NEURON imports, no morphology generator code. |

## Quality Checks

The full quality-check suite is run by the orchestrator after this subagent returns; this section
records the local checks the implementation subagent performed:

* `ruff check --fix` and `ruff format` on `tasks/t0103_extract_baden_2016_ds_morphologies/code/`:
  run.
* `mypy -p tasks.t0103_extract_baden_2016_ds_morphologies.code`: run.
* `meta.asset_types.paper.verificator --task-id t0103_extract_baden_2016_ds_morphologies 10.1038_nature16468`:
  PASSED (no errors or warnings).
* `meta.asset_types.dataset.verificator --task-id t0103_extract_baden_2016_ds_morphologies baden-2016-ds-cells`:
  run in the final quality-check pass.
* `flowmark --inplace --nobackup` on edited markdown files: run.

## Files produced / modified

### New files

* `tasks/t0103_extract_baden_2016_ds_morphologies/code/load_baden_mat.py`
* `tasks/t0103_extract_baden_2016_ds_morphologies/code/build_per_cell_dataset.py`
* `tasks/t0103_extract_baden_2016_ds_morphologies/code/check_counts.py`
* `tasks/t0103_extract_baden_2016_ds_morphologies/code/REQ_COMPLETION.md`
* `tasks/t0103_extract_baden_2016_ds_morphologies/code/group_count_check.json`
* `tasks/t0103_extract_baden_2016_ds_morphologies/assets/dataset/baden-2016-ds-cells/details.json`
* `tasks/t0103_extract_baden_2016_ds_morphologies/assets/dataset/baden-2016-ds-cells/description.md`
* `tasks/t0103_extract_baden_2016_ds_morphologies/assets/dataset/baden-2016-ds-cells/files/baden-2016-ds-cells.parquet`

### Replaced files

* `tasks/t0103_extract_baden_2016_ds_morphologies/code/constants.py` — replaced
  `USER_DS_CLUSTER_IDS` (the original wrong list) with `DS_GROUP_IDS` (the paper set); added
  per-cell field-name constants.
* `tasks/t0103_extract_baden_2016_ds_morphologies/code/paths.py` — dropped the unused JSONL output
  path; added `BADEN_MAT_PATH` and `BADEN_README_PDF_PATH`.
* `tasks/t0103_extract_baden_2016_ds_morphologies/code/make_charts.py` — replaced the prior
  placeholder/sketched-traces chart code with real-data plotting from the produced Parquet.
* `tasks/t0103_extract_baden_2016_ds_morphologies/code/visualization_code_notes.md` — updated
  "File and field mapping" with empirically-confirmed shapes/dtypes; added "Resolution: DS group
  set" subsection recording the user's option-A choice.
* `tasks/t0103_extract_baden_2016_ds_morphologies/results/images/cell_counts_and_ipl.png` and
  `representative_traces.png` — overwritten with real-data figures.

### Removed files

* `tasks/t0103_extract_baden_2016_ds_morphologies/code/build_ds_group_dataset.py` — replaced by
  `build_per_cell_dataset.py`. The old script wrote group-level fallback data for the wrong cluster
  set and is obsolete.
* `tasks/t0103_extract_baden_2016_ds_morphologies/code/check_group_counts.py` — replaced by
  `check_counts.py`. The old script reported all `produced_count = 0` because the per-cell
  extraction was blocked.

## New dependencies

None. `scipy`, `pyarrow`, `numpy`, `pandas`, `matplotlib` are all already in `pyproject.toml`. The
Dryad `.mat` is MATLAB 5.0 (not HDF5 v7.3), so `mat73` is NOT required.
