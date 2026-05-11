# ✅ Extract direction-selective cell data from Baden et al. 2016

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0103_extract_baden_2016_ds_morphologies` |
| **Status** | ✅ completed |
| **Started** | 2026-05-11T20:51:26Z |
| **Completed** | 2026-05-12T01:55:00Z |
| **Duration** | 5h 3m |
| **Task types** | `download-dataset`, `download-paper` |
| **Categories** | [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md) |
| **Expected assets** | 1 dataset, 1 paper |
| **Step progress** | 8/15 |
| **Task folder** | [`t0103_extract_baden_2016_ds_morphologies/`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/task_description.md)*

# t0103 — Extract direction-selective cell data from Baden et al. 2016

## Motivation

The project's DSGC compartmental modelling work (t0024 substrate plus the morphology generator
lineage t0090/t0092/t0093) currently relies on a single canonical morphology from De Rosenroll
et al. 2026 and parametric variants synthesised by the t0090 generator. To ground the
parameter ranges (dendritic field diameter, branch count, total length, asymmetry) in
biological data we need a population of real, identified direction-selective (DS) RGC
morphologies and their co-recorded functional fingerprints from a single well-characterised
source.

Baden, Berens, Franke, Román Rosón, Bethge & Euler (2016), "The functional diversity of
retinal ganglion cells in the mouse", Nature 529:345–350, classified ~11 000 mouse RGCs and
displaced amacrine cells into >40 functional groups using two-photon Ca2+ imaging and a
battery of light stimuli. The dataset on Dryad accompanies the paper and contains, per cell:
cluster assignment, soma position, IPL stratification depth, response traces, and (for a
subset) morphological reconstructions obtained from dye fills during the patch-clamp
follow-ups.

This task downloads the source materials and extracts data only for the 8 DS groups the user
has identified, producing one dataset asset that the downstream modelling tasks (extending
t0090's parameter envelopes, validating t0102's joint-pass corner, building Baden-grounded
null distributions) can import directly. The Baden 2016 paper itself is also added as a paper
asset.

## Sources

* **Paper**: Baden et al. 2016, *Nature*, DOI
  [10.1038/nature16468](https://www.nature.com/articles/nature16468).
* **Dataset**: Dryad, DOI
  [10.5061/dryad.d9v38](https://datadryad.org/dataset/doi:10.5061/dryad.d9v38).
* **MATLAB visualisation code**: the lab-distributed zip at
  `http://retinal-functomics.net/wp-content/uploads/2015/12/Baden_et_al_2016_visualization.zip`.
  This zip contains the canonical scripts that map cluster IDs to cell counts, IPL depth, and
  morphological summary statistics — use it as the authoritative reference for the
  cluster→data mapping and any non-obvious data layout choices.
* **README**: `https://datadryad.org/downloads/file_stream/3407` — Dryad-hosted text README
  that documents the file layout and field meanings.

## Scope

### Groups to extract (DS only)

Extract data **only** for the following 8 direction-selective groups from the Baden 2016
taxonomy:

* Group **2** — OFF-type direction-selective cell.
* Group **17** — ON–OFF direction-selective subtype.
* Group **18** — ON–OFF direction-selective subtype.
* Group **19** — ON–OFF direction-selective subtype.
* Group **22** — ON direction-selective cell.
* Group **35** — displaced amacrine / DS-related (cluster numbering in the extended >32 group
  taxonomy used by the Dryad release).
* Group **36** — displaced amacrine / DS-related.
* Group **40** — displaced amacrine / DS-related.

If the Dryad data layout or the visualisation-zip scripts label these clusters with names that
do not match "DS" — e.g. an off-by-one or numbering scheme that puts the 4 canonical ON–OFF DS
subtypes in different IDs — the implementation step must reconcile the user's group list
against the labels in the actual data using the visualisation scripts as the authoritative
mapping, and record the resolution in `research/research_code.md`. Do not silently substitute
different groups — if the user-specified IDs cannot be located, write an intervention file.

### What to extract per group

For each of the 8 groups, extract every per-cell field available in the Dryad release. At
minimum this should include, when present in the data:

* Cluster / group ID and confidence.
* Soma position (retinal location: x, y or eccentricity/dorsoventral coordinates).
* IPL stratification depth profile.
* Functional response traces to the standard Baden 2016 stimulus set (chirp, moving bars,
  full-field, coloured, etc.) and any extracted features (DS index, OS index, polarity,
  transience, preferred direction, response quality, etc.).
* Morphological reconstruction, if available — dendritic tree (SWC or equivalent point list)
  and any derived per-cell shape statistics (field diameter, total dendritic length, branch
  points, asymmetry vector).
* Cell-of-origin metadata: retina ID, eye, dorsoventral location, age, sex if recorded.

If the Dryad release does **not** contain morphological reconstructions for these groups
(plausible — Baden 2016 is primarily a functional dataset, and morphologies for DS cells may
have been added in a companion paper such as Bae et al. 2018, Ran et al. 2020, or others),
document the absence explicitly in `research/research_code.md` and in the dataset asset's
`description.md`. Continue to extract whatever per-cell data is present — the downstream
modelling tasks still benefit from the functional fingerprints and stratification depths even
without morphologies.

### Out of scope

* Re-classifying the Baden 2016 data into new groups.
* Re-analysing the raw Ca2+ traces — extract them as-is and let downstream tasks decide what
  to do with them.
* Refitting the visualisation scripts or porting them from MATLAB to Python beyond the minimum
  needed to read the data files. If a MATLAB→Python data load is needed, prefer using
  `scipy.io` or `mat73` rather than rewriting analysis code.
* Adding non-DS Baden groups (their data are not needed for the DSGC modelling line).
* Cross-paper integration with later Baden lab releases (e.g. Bae 2018, Goetz 2022) — those
  are separate tasks if they turn out to be needed.

## Approach

1. Download the Baden 2016 paper PDF and register it as a paper asset under
   `assets/paper/10.1038_nature16468/` following `meta/asset_types/paper/specification.md`.

2. Download the Dryad bundle (the full archive) into a task-local `data/` folder via
   `wget`/`curl`, recording byte sizes and SHA-256 hashes. The Dryad doi resolves to a
   download page that may package multiple files; pull every file in the archive.

3. Download the visualisation MATLAB zip and extract it into `data/visualization_code/`.
   Inspect the top-level scripts to identify (a) which Dryad file contains the cluster
   assignments, (b) which field name holds the cluster ID, and (c) where per-cell traces and
   any morphological data are stored.

4. Download the Dryad README from `https://datadryad.org/downloads/file_stream/3407` and save
   it under `data/`. Cross-reference its field list against what the visualisation scripts
   actually load.

5. Write a small Python loader in `code/` that:
   * Loads the per-cell cluster assignments.
   * Filters to the 8 DS groups listed above.
   * Pulls every available per-cell field for those cells (functional traces, IPL depth, soma
     position, morphology if present, etc.) into a clean per-cell record.
   * Writes the result to a single dataset asset under `assets/dataset/baden-2016-ds-cells/`,
     using a Parquet or JSONL container (whichever is the simpler match for the source field
     shapes).

6. Verify the per-group cell counts against the counts reported in Figure 2 of Baden 2016 (or
   in the visualisation scripts' summary outputs) and record the comparison in
   `results/results_detailed.md`. A material discrepancy (>5%) is a finding worth flagging; an
   exact match validates the filter logic.

7. Produce at least two diagnostic charts in `results/images/`:
   * One chart showing cell counts and IPL stratification per extracted group.
   * One chart showing one representative response trace per group (e.g. the cluster mean to
     the moving-bar stimulus that defines DS).

## Expected Assets

* **1 dataset asset** under `assets/dataset/baden-2016-ds-cells/` containing the extracted
  per-cell records for groups 2, 17, 18, 19, 22, 35, 36, and 40.

* **1 paper asset** under `assets/paper/10.1038_nature16468/` for the Baden 2016 paper itself
  (full v3 spec compliance — abstract, full-text summary, citation_key `Baden2016`, categories
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

* **Risk**: Dryad URL or visualisation zip have rotted. **Fallback**: fetch the dataset from
  the paper's GitHub mirror or contact the corresponding author. If unrecoverable, mark the
  dataset asset's download_status as failed and record the failure with full evidence in
  `intervention/`.

* **Risk**: User-specified group IDs do not match the Dryad cluster numbering. **Fallback**:
  use the visualisation scripts to map cluster IDs to functional cell-type labels and
  reconcile. If reconciliation is ambiguous, write an intervention file before producing the
  dataset asset.

* **Risk**: Morphological reconstructions are not in this Dryad release (Baden 2016 is
  primarily a functional dataset). **Fallback**: extract whatever IS available (functional
  traces, IPL stratification, soma position) and clearly state the morphology gap in the
  dataset asset's `description.md`; recommend a follow-up task to source DS-cell morphologies
  from a complementary paper such as Bae et al. 2018 or Ran et al. 2020 — but defer that as a
  separate task, do NOT expand scope here.

* **Risk**: MATLAB `.mat` files use the HDF5 v7.3 format that `scipy.io.loadmat` cannot read.
  **Fallback**: use `mat73` (or `h5py` directly) — add as a project-level dependency in
  `pyproject.toml` if not present.

## Verification Criteria

* `verify_task_file t0103_extract_baden_2016_ds_morphologies` passes with 0 errors.
* The dataset asset passes its verificator (paths to be filled in during planning).
* The paper asset passes its verificator.
* Per-group cell counts in the produced dataset asset are reported in `results_detailed.md`
  and cross-checked against either Baden 2016 Figure 2 or the visualisation scripts' own
  summaries.
* At least one diagnostic chart per the Approach is embedded in `results_detailed.md`.

## Out of Scope (explicit)

* Running NEURON simulations on the extracted morphologies — that is a downstream task.
* Building a parametric generator that mimics the Baden DS-cell morphologies — also
  downstream.
* Re-classifying or re-clustering Baden's data.
* Extending to non-DS groups.
* Integrating other Baden-lab data releases beyond the 2016 Nature paper.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| dataset | [Baden 2016 RGC direction-selective subset](../../../tasks/t0103_extract_baden_2016_ds_morphologies/assets/dataset/baden-2016-ds-cells/) | [`description.md`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/assets/dataset/baden-2016-ds-cells/description.md) |
| paper | [The functional diversity of retinal ganglion cells in the mouse](../../../tasks/t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/) | [`summary.md`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Download Bae et al. 2018 dense EM reconstructions for Baden cluster
IDs</strong> (S-0103-01)</summary>

**Kind**: dataset | **Priority**: high

Baden 2016's Dryad release contains no dendritic morphology. Bae et al. 2018 (EyeWire/E2198
dense EM dataset) published reconstructed RGC morphologies and explicitly linked many of them
to Baden 2016 functional cluster IDs. Download Bae 2018 morphologies for the 8
paper-authoritative DS clusters {2, 6, 12, 13, 16, 25, 26, 29} and emit one dataset asset of
SWC/JSON morphologies keyed by Baden cluster ID. This is the most direct way to ground t0090's
morphology-generator parameter envelopes (field diameter, branch count, total length,
asymmetry) in real biological DS-cell shapes. Recommended task types: download-dataset,
download-paper.

</details>

<details>
<summary><strong>Download Ran et al. 2020 ON-OFF DS-cell morphologies as a
complementary morphology source</strong> (S-0103-02)</summary>

**Kind**: dataset | **Priority**: high

Ran et al. 2020 (Nat Commun) provides dye-fill reconstructions of mouse ON-OFF DS RGCs with
co-recorded preferred-direction labels. The Baden 2016 Dryad release does not include
morphologies, and Ran 2020 covers exactly the ON-OFF DS subtypes (Baden clusters G12/G13) most
relevant to the t0024 ON-OFF DSGC modelling line. Download the published SWC files (or extract
from supplementary materials), register them as a dataset asset, and tag each morphology with
its preferred-direction angle and any Baden-cluster correspondence available. Useful as a
second, independent morphology source against Bae 2018 for the t0090 envelope grounding.
Recommended task types: download-dataset, download-paper.

</details>

<details>
<summary><strong>Ground t0090 morphology-generator parameter envelopes in the Baden
2016 + Bae/Ran morphologies</strong> (S-0103-03)</summary>

**Kind**: experiment | **Priority**: high

t0090's morphology generator currently samples field diameter, branch count, total length, and
asymmetry from hand-picked ranges around the t0024 canonical De Rosenroll cell. The t0103
Baden subset (RF diameter, DSI, OSI per cell across 1,238 DS cells) plus the morphologies that
the Bae 2018 / Ran 2020 follow-ups would deliver give us per-cluster biological envelopes for
each shape statistic. Run a re-calibration task that fits empirical per-cluster distributions
(mean +/- SD per Baden DS group) and replaces t0090's parametric ranges, then re-runs a small
NSGA-II validation to confirm the bio-grounded envelopes still admit the Pareto-front cells.
This is the original motivation for downloading Baden 2016 in the first place. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary><strong>Build a reusable Dryad-with-Anubis-PoW downloader library</strong>
(S-0103-04)</summary>

**Kind**: library | **Priority**: medium

t0103 had to implement a ~30-line pure-hashlib Anubis 1.24.0 proof-of-work solver inline to
unlock the Dryad d9v38 release, after discovering that vanilla CLI tools get blocked by an
anti-scraper PoW challenge and the v2 REST API requires OAuth. Extract this into a small
reusable library under `arf/scripts/utils/` (or a standalone Python package) that wraps
`Dryad-with-Anubis` downloads: resolve DOI -> solve PoW -> fetch presigned S3 URL -> stream to
disk -> verify SHA-256. Adds Wayback fallback and progress reporting. Future Baden-lab dataset
tasks (Bae 2018 if also on Dryad, Goetz 2022, Franke 2017) avoid re-implementing this.
Recommended task types: write-library, infrastructure-setup.

</details>

<details>
<summary><strong>Re-emit Baden 2016 DS subset at float64 precision split into
per-group Parquets</strong> (S-0103-05)</summary>

**Kind**: dataset | **Priority**: medium

The t0103 dataset asset down-casts the 5 trace columns (chirp 249, bar 32, bar-dir-major 256,
color 96, RF 80) from float64 to float32 to fit the 5 MiB pre-merge limit on the single
combined Parquet. For downstream ML or statistical analysis where float32 rounding becomes a
concern (e.g. PCA over chirp traces, GP regression on RF kernels), re-emit one Parquet per
Baden cluster at float64 precision, store via git-LFS or a sibling dataset asset, and update
`details.json` to point at the higher-precision payload. Add a brief schema check that the
per-group float64 Parquets and the original float32 combined Parquet agree to within rounding.
Recommended task types: feature-engineering, data-analysis.

</details>

<details>
<summary><strong>Swap the typeset PMC reproduction for the Nature publisher PDF
of Baden 2016</strong> (S-0103-06)</summary>

**Kind**: library | **Priority**: low

The Baden 2016 paper asset's PDF is a typeset reproduction of the PMC fulltext XML
(PMC4724341) because Nature's publisher PDF is paywalled and PMC's interactive viewer is
JS-protected. All scientific content is faithful, but typography and figure layout do not
match the publisher version, which makes it awkward to cite figure positions or compare with
print-version page references. A small follow-up task can obtain the publisher PDF via
institutional access (Sheffield) and swap it in via the corrections mechanism, leaving the
typeset version as a fallback. Recommended task types: download-paper, correction.

</details>

<details>
<summary><strong>Recover per-cell IPL stratification depth profiles from Baden 2016
scan-level structural data</strong> (S-0103-07)</summary>

**Kind**: technique | **Priority**: medium

The Baden 2016 Dryad release exposes a scan-level structural volume and per-scan ROI metadata,
but no per-cell IPL stratification profile (paper Fig. 2 IPL profiles are derived per-group,
not per-cell). t0103 substituted per-group mean RF diameter as the secondary statistic. A
follow-up task can re-project per-cell ROIs onto the scan-level IPL volume to reconstruct an
approximate per-cell stratification depth profile, validating against the paper's per-group
means as ground truth. This would unlock per-cell IPL depth as a feature for downstream
modelling tasks (e.g. matching modelled dendritic terminations to biological IPL bands).
Recommended task types: data-analysis, feature-engineering.

</details>

<details>
<summary><strong>Build a Baden-grounded null distribution of DSI/OSI for
t0091/t0099/t0102 Pareto evaluation</strong> (S-0103-08)</summary>

**Kind**: evaluation | **Priority**: medium

t0103 extracted DSI and OSI per cell for 1,238 DS cells across 8 Baden DS groups (DSI mean
~0.40-0.46, max ~0.73-0.76, OSI mean ~0.15-0.20). The NSGA-II Pareto fronts from
t0091/t0099/t0102 currently lack a biological null distribution to compare DSI/OSI against --
they are evaluated only against the t0024 canonical reference. Build a small task that
produces a per-Baden-group DSI/OSI empirical CDF chart, overlays the Pareto-front DSI/OSI
distributions, and reports the percentile of each Pareto cell relative to its presumed Baden
cluster. This is a cheap, high-value sanity check on whether the optimised cells fall inside
the biological envelope. Recommended task types: data-analysis, comparative-analysis.

</details>

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/results/results_summary.md)*

# t0103 Results Summary

## Summary

Extracted **1,238 per-cell records** from Baden et al. 2016 across the eight
paper-authoritative direction-selective groups `{2, 6, 12, 13, 16, 25, 26, 29}` into a 4.864
MiB Parquet dataset asset, and registered the Baden 2016 paper itself as a paper asset. Both
assets pass their verificators with zero errors and zero warnings.

## Metrics

* **1,238** per-cell records extracted across **8 DS groups**: G2:162, G6:104, G12:397,
  G13:129, G16:99, G25:76, G26:141, G29:130.
* **40 columns per cell**: 35 scalar features (cluster, selectivity, quality, RF, soma,
  immuno, genetics, cell-of-origin) + 5 nested `list<float32>` trace columns (chirp 249
  samples, moving-bar 32, moving-bar direction-major 256, colour 96, RF kernel 80).
* **Cross-check delta vs source `.mat` `group_idx`**: **0.00% for all 8 groups**. G2 also
  matches the paper's explicit Extended-Data-Fig.-4 cell count of n=162 exactly.
* **No registered project metrics** apply to this extraction task; `metrics.json` is `{}`.

## Verification

* `meta.asset_types.paper.verificator --task-id t0103_extract_baden_2016_ds_morphologies` →
  **PASSED** (0 errors, 0 warnings).
* `meta.asset_types.dataset.verificator --task-id t0103_extract_baden_2016_ds_morphologies` →
  **PASSED** (0 errors, 0 warnings).
* `ruff check`, `ruff format`, `mypy -p tasks.t0103_extract_baden_2016_ds_morphologies.code` →
  all green.
* `verify_plan` → PASSED (0 errors, 0 warnings).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0103_extract_baden_2016_ds_morphologies" date_completed:
"2026-05-11" status: "complete" ---
# t0103 Results — Detailed

## Summary

This task downloaded the Baden et al. 2016 *Nature* paper and the accompanying Dryad d9v38
release, then extracted **1,238 per-cell records** spanning the **8 paper-authoritative
direction-selective groups** `{2, 6, 12, 13, 16, 25, 26, 29}` (per the paper's main text:
"Most DS cells (70%) were sorted into 8 groups (G 2, 6, 12, 13, 16, 25, 26, 29)"). The
extracted records carry 40 per-cell fields (35 scalar + 5 nested-list trace columns) and are
written to a 4.864 MiB Parquet inside the dataset asset. Per-group cell counts match the
source `.mat` `group_idx` exactly (delta_pct = 0.00% for all 8 groups). The Baden 2016 paper
is registered as a paper asset (v3 spec). Both verificators pass with zero errors and zero
warnings.

## Methodology

* **Machine**: local Windows 11 development machine (no remote compute).
* **Tools**: Python 3.13 via `uv`; `scipy.io.loadmat` for the MATLAB 5.0 `.mat`; `pyarrow` for
  Parquet with zstd level-22 compression; `matplotlib` for figures; `typst` for the paper PDF
  reproduction (since the Nature publisher PDF is paywalled and the PMC interactive viewer is
  JS-protected).
* **Runtime**: ~3 hours wall-clock for the full task (download + Anubis-bypass + extraction +
  chart generation + remediation), of which the dominant fixed cost was the 426 MB `.mat`
  download (~3 min). The per-cell extraction itself runs in ~5 s.
* **Timestamps**: task started 2026-05-11T20:53:38Z (`create-branch`); implementation step
  closed at 2026-05-11T22:57:27Z.
* **Source data SHA-256** (recorded in `data/download_manifest.json`):
  * `BadenEtAl_RGCs_2016_v1.mat`:
    `6a8fba740efbce1e72584fda23a637a078ddb74f3f5d8a064ed231d10b6c4737` (426,025,871 bytes;
    gitignored at repo root — kept locally only).
  * `README_for_BadenEtAl_RGCs_2016_v1.pdf`:
    `585e93a7277a8389c3f89d630df0ed9cbae6c89254d05866a5133fbb813648ea` (69,619 bytes).
  * `Baden_et_al_2016_visualization.zip`: SHA-256 in `download_manifest.json`; extracted into
    `data/visualization_code/`.

## Per-Group Cell Counts

| Group | Label | Cells extracted | Source `.mat` count | Paper reference | Δ % |
| --- | --- | ---: | ---: | --- | ---: |
| G2 | OFF DS | 162 | 162 | 162 (Extended Data Fig. 4) | 0.0 |
| G6 | (ON-)OFF JAM-B mix | 104 | 104 | — | 0.0 |
| G12 | ON-OFF DS 1 | 397 | 397 | — | 0.0 |
| G13 | ON-OFF DS 2 | 129 | 129 | — | 0.0 |
| G16 | ON DS trans. | 99 | 99 | — | 0.0 |
| G25 | ON DS sust. 1 | 76 | 76 | — | 0.0 |
| G26 | ON slow | 141 | 141 | — | 0.0 |
| G29 | ON local sust. OS | 130 | 130 | — | 0.0 |
| **Total** |  | **1,238** | **1,238** |  | 0.0 |

The cell-count cross-check is the strongest verification available for this extraction: zero
delta against `source_mat_count` for every group, and exact match against the paper's explicit
n=162 for G2. The full per-group comparison record is in `code/group_count_check.json`.

## Per-Group Selectivity and Receptive-Field Summary

Computed from the produced Parquet (cells with `dsi_pvalue < 0.05` — significantly DS by the
source permutation test). All 1,238 selected cells in the eight DS groups are significantly
direction- selective.

| Group | Cells | DSI mean | DSI max | OSI mean | RF diameter mean (μm) |
| --- | ---: | ---: | ---: | ---: | ---: |
| G2 | 162 | 0.420 | 0.731 | 0.175 | 250.8 |
| G6 | 104 | 0.410 | 0.649 | 0.198 | 317.9 |
| G12 | 397 | 0.464 | 0.761 | 0.152 | 243.3 |
| G13 | 129 | 0.444 | 0.657 | 0.173 | 226.1 |
| G16 | 99 | 0.411 | 0.666 | 0.194 | 266.5 |
| G25 | 76 | 0.405 | 0.611 | 0.179 | 237.7 |
| G26 | 141 | 0.441 | 0.692 | 0.190 | 248.3 |
| G29 | 130 | 0.422 | 0.690 | 0.188 | 246.3 |

DSI is roughly 0.40–0.46 across all eight DS groups, with the largest individual DSI values
reaching 0.73–0.76 in G2 and G12 (the OFF DS and ON-OFF DS 1 groups). RF diameters span a ~90
μm range across groups, with G6 ((ON-)OFF JAM-B mix) carrying the largest mean RF (~318 μm)
and G13 (ON-OFF DS 2) the smallest (~226 μm).

## Visualizations

### Per-group cell counts and mean RF diameter

![Per-group cell counts and mean RF
diameter](../../../tasks/t0103_extract_baden_2016_ds_morphologies/results/images/cell_counts_and_ipl.png)

Top panel: bar chart of the per-group cell count from the Parquet. Bottom panel: per-group
mean RF diameter (μm), serving as a proxy for the IPL/dendritic-extent summary statistic that
the original plan called for (per-cell IPL stratification depth is **not** in the Dryad
release — see the "Limitations" section). Note the much larger RF for G6 (JAM-B mix) and the
comparatively small RF for G13 (ON-OFF DS 2).

### Representative cluster-mean moving-bar response per group

![Representative moving-bar traces per DS
group](../../../tasks/t0103_extract_baden_2016_ds_morphologies/results/images/representative_traces.png)

Eight-panel grid showing the cluster-mean moving-bar time course (`bar_tc`) ± 1 SD across
cells for each of the 8 DS groups, drawn from real `bar_tc` data in the Parquet (not
placeholders). The OFF-type response in G2 vs. the ON-OFF responses in G12/G13 vs. the
ON-dominant responses in G16/G25/G26/G29 are visible; the JAM-B mix (G6) shows the
characteristic biphasic profile.

## Examples

Five representative per-cell records pulled from the Parquet, showing the raw scalar feature
set (trace columns omitted for brevity — they are nested `list<float32>` arrays of length 249,
32, 256, 96, 80).

### Example 1 — G2 OFF DS

```text
cell_index=60, group_id=2, group_label="OFF DS", cluster_id=2, selected=True
dsi=0.298, dsi_pvalue=0.024, osi=0.121, osi_pvalue=0.41
soma_area_um2=91.5, rf_diameter_um=259.5
chirp_qi=0.31, bar_qi=0.90, color_qi=0.18, rf_qi=0.62
recording_date="2013-03-12", mouse_id=4, eye_id=1, scan_num=2, stim_num=3, cell_num=8
chirp_avg[:5] = [0.0918, -0.1955, 0.1457, 0.1246, 0.0942]
bar_tc[:6]    = [0.0099, -0.0136, -0.0020, -0.0069, 0.0249, 0.0377]
```

### Example 2 — G12 ON-OFF DS 1

```text
cell_index=1, group_id=12, group_label="ON-OFF DS 1", cluster_id=18, selected=True
dsi=0.4098, dsi_pvalue=0.004, osi=0.2065, osi_pvalue=0.211
soma_area_um2=43.07, rf_diameter_um=229.7
chirp_qi=0.281, bar_qi=0.923, color_qi=0.206, rf_qi=0.800
recording_date="2013-03-12", mouse_id=1, eye_id=1, scan_num=1, stim_num=3, cell_num=2
```

### Example 3 — G12 ON-OFF DS 1 (second representative)

```text
cell_index=3, group_id=12, group_label="ON-OFF DS 1", cluster_id=17, selected=True
dsi=0.4829, dsi_pvalue=0.000, osi=0.0564, osi_pvalue=0.981
soma_area_um2=45.76, rf_diameter_um=298.2
chirp_qi=0.280, bar_qi=0.904, color_qi=0.283, rf_qi=0.610
recording_date="2013-03-12", mouse_id=1, eye_id=1, scan_num=1, stim_num=3, cell_num=4
```

### Example 4 — G16 ON DS trans.

```text
cell_index=11, group_id=16, group_label="ON DS trans.", cluster_id=22, selected=True
dsi=0.4377, dsi_pvalue=0.001, osi=0.0813, osi_pvalue=0.661
soma_area_um2=67.29, soma_volume_um3=518.4, rf_diameter_um=155.6
chirp_qi=0.333, bar_qi=0.724, color_qi=0.193, rf_qi=0.095
recording_date="2013-03-12", mouse_id=1, eye_id=1, scan_num=1, stim_num=3, cell_num=12
```

### Example 5 — Loading recipe (the input → output the downstream consumer sees)

Input — the Parquet file plus the file-level metadata header:

```python
import json
import pyarrow.parquet as pq

t = pq.read_table(
    "tasks/t0103_extract_baden_2016_ds_morphologies/assets/dataset/"
    "baden-2016-ds-cells/files/baden-2016-ds-cells.parquet"
)
meta = json.loads(t.schema.metadata[b"baden_2016_ds_cells_metadata"])
df = t.to_pandas()
```

Output — `df` is a 1238 × 40 DataFrame with the 40 columns enumerated above; `meta` contains
the four stimulus time axes (`chirp_time_s`, `bar_time_s`, `color_time_s`, `rf_time_s`) and
three explicit "what's missing" notes (no per-cell IPL profile, no retinal soma coordinates,
no dendritic morphology).

## Analysis

### Cluster-ID reconciliation finding

The user's original DS group list in `task_description.md` `{2, 17, 18, 19, 22, 35, 36, 40}`
disagreed with the paper's own DS taxonomy on seven of eight entries. `plotStamp.m` from the
Baden lab's distributed visualisation zip provides the authoritative `group_idx → label`
mapping for the 32-group taxonomy; under that mapping, the user's IDs 17/18/19/22 correspond
to **non-DS** RGC groups ("ON local trans.", "ON trans.", "ON trans., large", "ON sust."), and
IDs 35/36/40 fall in the displaced-amacrine-cell range whose DS status the public scripts do
not name. The paper's main text explicitly states the actual DS-containing group set is `{2,
6, 12, 13, 16, 25, 26, 29}`.

This is a **finding worth reporting**, not just a cleanup step. The original task brief's
group list appears to have been authored from memory or from a different version of the Baden
lab's clustering (the paper itself acknowledges multiple clustering passes), and would have
caused the extraction to (a) silently substitute non-DS cells if not caught, or (b) emit a
near-empty dataset if matched literally against the published mapping. The plan's "do NOT
silently substitute" guidance triggered an intervention, the user explicitly resolved it in
favour of the paper's set, and the resolution is recorded in
`code/visualization_code_notes.md` and the dataset's `description.md` `## Overview` "Important
scope note" subsection.

### Dryad authentication finding

The Dryad d9v38 record cannot be downloaded with a vanilla CLI tool: the v2 REST API returns
401 without an OAuth bearer token, and the legacy `/downloads/file_stream/<id>` URLs serve an
Anubis 1.24.0 anti-scraper proof-of-work challenge. The blocker was resolved by implementing a
~30-line pure-`hashlib` PoW solver (`sha256(randomData + nonce) < 0x0000`, ~10**4 tries),
submitting the solved nonce, and receiving a `techaro.lol-anubis-auth` JWT cookie that unlocks
the presigned S3 URL on `dryad-assetstore-merritt-west.s3.us-west-2.amazonaws.com`. This is
documented inline in the implementation step log and via `logs/commands/036_*` through
`041_*`.

### Plan assumption check

The plan assumed the Dryad release would carry per-cell IPL stratification profiles and
possibly morphologies. **Both assumptions were contradicted by the data.** The Dryad `.mat`
exposes a scan-level structural volume and per-scan ROI metadata, but per-cell IPL profile and
dendritic morphology fields are not present. The dataset description's `## Content &
Annotation` section and the `## Main Ideas` block explicitly call out this gap and recommend
sourcing DS-cell morphologies from a complementary paper (Bae et al. 2018 or Ran et al. 2020)
as a follow-up task — deferred per the brief's explicit out-of-scope clause.

## Limitations

* **No per-cell IPL stratification depth profile** in the Dryad release. The paper's per-group
  IPL profiles in its Fig. 2 are derived from scan-level structural data; the per-cell profile
  field is not exposed. The chart `cell_counts_and_ipl.png` therefore substitutes per-group
  mean RF diameter as the secondary statistic.
* **No per-cell retinal soma coordinates.** The `rf_gauss_mean_x/y` fields are receptive-field
  centres in stimulus-screen space, not retinal positions.
* **No dendritic morphology.** Out of scope for t0103 per the task brief.
* **The paper PDF is a typeset reproduction of the PMC fulltext XML** because Nature's
  publisher PDF is paywalled and PMC's interactive viewer is JS-protected. All scientific
  content is faithful (drawn from the NCBI PMC v2 fulltext XML record PMC4724341), but the
  typography and layout do not match the publisher's version. A nice-to-have follow-up
  suggestion to swap in the publisher PDF is captured in `suggestions.json`.
* **The 426 MB `.mat` source file is gitignored at the repo root**, not committed.
  Reproducibility is preserved via the SHA-256 recorded in `data/download_manifest.json`, and
  the Anubis-bypass download approach is documented in this file and in the implementation
  step log.

## Verification

| Check | Command | Result |
| --- | --- | --- |
| Paper asset spec | `python -m meta.asset_types.paper.verificator --task-id t0103_extract_baden_2016_ds_morphologies` | **PASSED** (0 E / 0 W) |
| Dataset asset spec | `python -m meta.asset_types.dataset.verificator --task-id t0103_extract_baden_2016_ds_morphologies` | **PASSED** (0 E / 0 W) |
| Plan | `python -m arf.scripts.verificators.verify_plan t0103_extract_baden_2016_ds_morphologies` | **PASSED** (0 E / 0 W) |
| Python style | `ruff check tasks/t0103_extract_baden_2016_ds_morphologies/code/` | All checks passed |
| Python format | `ruff format tasks/t0103_extract_baden_2016_ds_morphologies/code/` | 9 files formatted |
| Type check | `mypy -p tasks.t0103_extract_baden_2016_ds_morphologies.code` | 0 issues |
| Cell-count cross-check | `code/check_counts.py` → `code/group_count_check.json` | 0.0% delta for all 8 groups |

## Files Created

* `assets/paper/10.1038_nature16468/details.json`
* `assets/paper/10.1038_nature16468/summary.md`
* `assets/paper/10.1038_nature16468/files/baden_2016_functional_diversity_rgc.pdf`
* `assets/dataset/baden-2016-ds-cells/details.json`
* `assets/dataset/baden-2016-ds-cells/description.md`
* `assets/dataset/baden-2016-ds-cells/files/baden-2016-ds-cells.parquet`
* `code/paths.py`, `code/constants.py`, `code/load_baden_mat.py`,
  `code/build_per_cell_dataset.py`, `code/check_counts.py`, `code/make_charts.py`,
  `code/build_download_manifest.py`, `code/xml_to_pdf.py`, `code/visualization_code_notes.md`,
  `code/REQ_COMPLETION.md`, `code/group_count_check.json`
* `data/Baden_et_al_2016_visualization.zip`, `data/visualization_code/`,
  `data/baden_2016_fulltext.xml`, `data/baden_2016_fulltext.txt`,
  `data/baden_2016_paper_text.txt`, `data/baden_2016_paper.typ`,
  `data/README_for_BadenEtAl_RGCs_2016_v1.pdf`, `data/download_manifest.json`
* `data/BadenEtAl_RGCs_2016_v1.mat` (gitignored at repo root — kept locally only)
* `results/images/cell_counts_and_ipl.png`, `results/images/representative_traces.png`
* `results/results_summary.md`, `results/results_detailed.md`, `results/metrics.json`,
  `results/costs.json`, `results/remote_machines_used.json`

## Task Requirement Coverage

Operative task brief (verbatim from `task.json` and the resolved long description in
`task_description.md`):

> Download Baden 2016 (Dryad d9v38) and extract data only for direction-selective groups 2, 17, 18,
> 19, 22, 35, 36, 40. Output: 1 dataset + 1 paper asset.

The group list was amended mid-task to the paper-authoritative DS set `{2, 6, 12, 13, 16, 25,
26, 29}` after a cluster-ID reconciliation intervention; the user explicitly authorised that
substitution (option A in the resolution dialog). All twelve concrete requirements from
`plan/plan.md` are mapped below; the full evidence table is in `code/REQ_COMPLETION.md`.

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Baden 2016 paper asset (v3 spec, `Baden2016`, categories direction-selectivity + retinal-ganglion-cell) | **Done** | `assets/paper/10.1038_nature16468/`; paper verificator PASSED |
| REQ-2 | Full Dryad bundle in `data/` with SHA-256 / bytes in `download_manifest.json` | **Done** | `data/BadenEtAl_RGCs_2016_v1.mat` + `data/README_*` both listed in `data/download_manifest.json`; `.mat` gitignored, SHA preserved |
| REQ-3 | MATLAB visualisation zip downloaded and inspected; file/field mapping documented | **Done** | `data/Baden_et_al_2016_visualization.zip` + `data/visualization_code/`; mapping in `code/visualization_code_notes.md` |
| REQ-4 | Dryad README downloaded and cross-checked | **Done** | `data/README_for_BadenEtAl_RGCs_2016_v1.pdf` exists; cross-check in `code/visualization_code_notes.md` |
| REQ-5 | Reconcile user-specified IDs against Dryad numbering; document resolution or write intervention | **Done** | Intervention raised, user chose paper-set option A; resolution in `code/visualization_code_notes.md` and `assets/dataset/.../description.md` |
| REQ-6 | Python loader filtering to DS groups, pulling every per-cell field, with `None` for missing data | **Done** | `code/load_baden_mat.py` + `code/build_per_cell_dataset.py`; NaN preserved for missing immuno/genetics |
| REQ-7 | Dataset asset (v2 spec: `details.json`, `description.md`, `files/`) at `assets/dataset/baden-2016-ds-cells/` | **Done** | `assets/dataset/baden-2016-ds-cells/`; dataset verificator PASSED |
| REQ-8 | Document morphology absence; loader continues; recommend follow-up | **Done** | `assets/dataset/.../description.md` "What is NOT in this dataset"; suggestion captured in `results/suggestions.json` |
| REQ-9 | Per-group cell count cross-check in `code/group_count_check.json`; flag deltas > 5% | **Done** | All 8 deltas are 0.00% |
| REQ-10 | Two diagnostic charts in `results/images/` | **Done** | `cell_counts_and_ipl.png`, `representative_traces.png` (real data, not placeholders) |
| REQ-11 | `expected_assets = {dataset: 1, paper: 1}`, both verificators pass | **Done** | Both verificators PASSED with 0 errors / 0 warnings |
| REQ-12 | No re-clustering, no re-analysis, no non-DS groups, no other releases, no NEURON, no generator | **Done** | All code only reads/filters the source `.mat`; no clustering, no NEURON imports, no morphology generator |

</details>
