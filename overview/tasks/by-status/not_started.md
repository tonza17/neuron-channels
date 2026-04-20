# ⏹ Tasks: Not Started

2 tasks. ⏹ **2 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0013 — <strong>Resolve dsgc-baseline-morphology source-paper
provenance</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0013_resolve_morphology_provenance` |
| **Status** | not_started |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0005-01` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/), [`correction`](../../../meta/task_types/correction/) |
| **Task page** | [Resolve dsgc-baseline-morphology source-paper provenance](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Task folder** | [`t0013_resolve_morphology_provenance/`](../../../tasks/t0013_resolve_morphology_provenance/) |

# Resolve dsgc-baseline-morphology source-paper provenance

## Motivation

The `dsgc-baseline-morphology` dataset asset (NeuroMorpho neuron 102976, 141009_Pair1DSGC)
currently has `source_paper_id = null` because two Feller-lab 2018 papers are plausibly the
source:

* Morrie & Feller 2018 Neuron (DOI `10.1016/j.neuron.2018.05.028`) — nominated in the t0005
  download plan.
* Murphy-Baum & Feller 2018 Current Biology (DOI `10.1016/j.cub.2018.03.001`) — reported as
  the source by NeuroMorpho's metadata.

Until this is resolved, every downstream paper that uses the morphology will cite it
incorrectly or omit a citation entirely. This task downloads both candidate papers, reads
their Methods sections, confirms which one introduced the 141009_Pair1DSGC reconstruction, and
files a corrections asset that updates `dsgc-baseline-morphology.source_paper_id` to the
correct slug.

Covers suggestion **S-0005-01**.

## Scope

1. Download Morrie & Feller 2018 Neuron via `/add-paper`. Register as a v3 paper asset under
   `assets/paper/10.1016_j.neuron.2018.05.028/`.
2. Download Murphy-Baum & Feller 2018 Current Biology via `/add-paper`. Register as a v3 paper
   asset under `assets/paper/10.1016_j.cub.2018.03.001/`.
3. Read both papers' Methods sections. Look specifically for:
   * The recording date `141009` (October 9, 2014) or neighbouring dates.
   * The `Pair1DSGC` / `Pair 1 DSGC` / `paired recording` language matching the NeuroMorpho
     reconstruction metadata.
   * An explicit citation of the 141009_Pair1DSGC reconstruction or its deposit to
     NeuroMorpho.
4. If one paper is unambiguously the source, file a correction asset
   (`corrections/dataset_dsgc-baseline-morphology.json`) that sets `source_paper_id` to the
   winning paper's DOI-slug. If neither is an unambiguous match, file a correction that
   records both DOIs under a new `candidate_source_paper_ids` field and opens an intervention
   file explaining that Feller-lab contact is required.
5. Record the full reasoning in `results/results_detailed.md` so the provenance decision is
   auditable.

## Dependencies

* **t0005_download_dsgc_morphology** — owns the `dsgc-baseline-morphology` asset this task
  corrects.

## Expected Outputs

* **2 paper assets** (Morrie & Feller 2018 Neuron, Murphy-Baum & Feller 2018 Current Biology),
  both v3-spec-compliant with full summaries.
* **1 correction asset** in `corrections/dataset_dsgc-baseline-morphology.json` setting
  `source_paper_id` to the resolved winner (or documenting ambiguity).
* A provenance-reasoning section in `results/results_detailed.md`.

## Approach

1. Run `/add-paper` twice, once per DOI, following the paper-asset spec v3.
2. Read both full PDFs and extract the Methods paragraphs that describe the paired
   recording(s) from which 141009_Pair1DSGC was reconstructed.
3. If both papers cite the same recording session, pick the earlier one (lower DOI publication
   date). If only one paper cites the recording session, pick that one. If neither paper cites
   it, treat as ambiguous and flag for human review.

## Questions the task answers

1. Which Feller-lab 2018 paper introduced the 141009_Pair1DSGC reconstruction?
2. Does NeuroMorpho's metadata attribution (Murphy-Baum & Feller 2018) match the paper's
   Methods section, or does it disagree?
3. If both papers plausibly cite the recording, what are the tie-breakers?

## Risks and Fallbacks

* **Neither paper explicitly cites the 141009 reconstruction**: file an intervention asking
  the researcher to email the Feller lab. Do not silently pick one.
* **Both papers cite it**: pick the earlier publication date and document the tie-break.
* **Paper downloads fail (paywall / captcha)**: fall back to metadata-only paper assets (v3
  spec `download_status: "failed"`) and raise an intervention file requesting library access.

</details>

<details>
<summary>⏹ 0011 — <strong>Response-visualisation library (firing rate vs angle
graphs)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0011_response_visualization_library` |
| **Status** | not_started |
| **Effective date** | 2026-04-19 |
| **Dependencies** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | — |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [Response-visualisation library (firing rate vs angle graphs)](../../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Task folder** | [`t0011_response_visualization_library/`](../../../tasks/t0011_response_visualization_library/) |

# Response-visualisation library (firing rate vs angle graphs)

## Motivation

Every downstream experiment in this project will produce angle-resolved firing-rate data
(tuning curves). Without a shared visualisation library, each task will re-implement its own
plotting code, the plots will drift in style, and cross-model comparisons will need manual
re-work. This task builds one library, used by every later task, that turns a standard-schema
tuning-curve CSV into a consistent set of publication-quality PNGs.

## Scope

The library `tuning_curve_viz` exposes four plotting functions:

1. `plot_cartesian_tuning_curve(curve_csv, out_png, *, show_trials=True, target_csv=None)` —
   firing rate (Hz) vs direction (deg). Shows per-trial points, mean line, and a 95% bootstrap
   confidence band. Optional overlay of a target curve (dashed line) from t0004's
   `target-tuning-curve`.
2. `plot_polar_tuning_curve(curve_csv, out_png, *, target_csv=None)` — classical polar plot
   with the preferred direction annotated.
3. `plot_multi_model_overlay(curves_dict, out_png, *, target_csv=None)` — side-by-side
   Cartesian + polar overlay of multiple models (e.g., the Poleg-Polsky port from t0008, any
   models ported in t0010, and the canonical target curve).
4. `plot_angle_raster_psth(spike_times_csv, out_png, *, angle_deg)` — per-trial spike raster
   above a PSTH (Peri-Stimulus-Time Histogram), one figure per angle.

A CLI `tuning_curve_viz.cli` consumes a tuning-curve CSV path and produces all four plot types
into an output directory.

## Dependencies

* **t0004_generate_target_tuning_curve** — source of the canonical target curve for overlays
  and the smoke-test fixture.
* **t0008_port_modeldb_189347** — provides a real simulated tuning curve to smoke-test the
  library against alongside the target.

## Expected Outputs

* **1 library asset** (`assets/library/tuning-curve-viz/`) with:
  * `description.md` covering purpose, API, and example usage.
  * `module_paths` pointing at `code/tuning_curve_viz/`.
  * `test_paths` pointing at `code/tuning_curve_viz/test_*.py`.
  * Example output PNGs under the asset's `files/` (smoke-test outputs against
    `target-tuning-curve` and the t0008 simulated curve).

## Approach

Standard matplotlib + pandas. Tuning-curve CSV schema is fixed at `(angle_deg, trial_seed,
firing_rate_hz)`. Use `bootstrap` from scipy (or a small local implementation) for the 95% CI
band. For the multi-model overlay, auto-pick a colour-blind-safe palette (Okabe-Ito). No
animated plots, no interactive plots; PNG output only.

Smoke tests:

1. Generate all four plot types against `target-tuning-curve` (the pre-existing canonical
   curve).
2. Generate all four plot types against the t0008 Poleg-Polsky port's simulated tuning curve.
3. Generate the `plot_multi_model_overlay` figure combining both with the target as a dashed
   overlay.

Each smoke-test writes its output PNG to the library asset's `files/` folder so the asset
itself demonstrates what each plot looks like.

## Questions the task answers

1. Does the library produce all four plot types on the canonical target curve without errors?
2. Does it produce all four plot types on a real simulated curve (t0008) with the same code
   path?
3. Does the multi-model overlay correctly align axes and preferred-direction annotations
   across models with different angular sampling?

## Risks and Fallbacks

* **Polar-axis convention mismatch between matplotlib and the tuning-curve convention (0° =
  east)**: document the convention in the library's `description.md` and stick to
  `theta_direction=1, theta_offset=0` (standard).
* **`scipy.stats.bootstrap` unavailable**: fall back to a 4-line NumPy bootstrap.
* **Multi-model overlay becomes illegible with > 6 models**: cap overlay at 6 and surface a
  warning; the CLI batches additional models into separate PNGs.

</details>
