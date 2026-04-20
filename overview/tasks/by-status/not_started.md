# ⏹ Tasks: Not Started

1 tasks. ⏹ **1 not_started**.

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
