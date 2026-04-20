---
spec_version: "1"
task_id: "t0015_literature_survey_cable_theory"
research_stage: "code"
tasks_reviewed: 14
tasks_cited: 3
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Survey prior neuron-channels tasks for code, datasets, morphologies, and findings relevant to a
cable-theory literature survey. The task only produces paper assets plus one answer asset — no
compartmental simulations are run — so the primary question is whether any existing task already
downloaded one of the 25 candidate cable-theory papers, or whether any existing answer already
reports electrotonic-length / d_lambda / transfer-impedance numbers for DSGCs.

## Library Landscape

The project currently has **zero registered library assets** (`tasks/*/assets/library/` is empty
across all 19 tasks as of 2026-04-19). No import candidates therefore exist. The literature-survey
task type in this project also does not produce libraries by design — it produces `paper` and
`answer` assets. Consequently this section is empty and the `libraries_found` and
`libraries_relevant` counts are both zero. Any utility code written in this task (e.g., a small
de-duplication check against the t0002 DOI exclusion list) must live inside the task's own `code/`
folder.

## Key Findings

### The t0002 Corpus Is the Only Prior Paper Survey and Is Already Indexed

Task [t0002] delivered 20 DSGC compartmental-modelling papers under
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`. Three of those papers touch
cable theory (Hines 1997, Schachter 2010, Branco 2010) and were already reviewed in
`research/research_papers.md` for this task. None of the other 17 papers treat cable theory as a
primary topic. The 20 DOIs are the exclusion list for t0015's internet search and were checked
against the discovered-paper list — no overlap remains.

### No Prior Answer Asset Reports Electrotonic-Length Numbers

Only one prior task produced an `answer` asset: [t0013]
(`tasks/t0013_resolve_morphology_provenance/assets/answer/`) documents morphology provenance for the
baseline DSGC SWC, not cable theory. No prior answer reports electrotonic length, transfer
impedance, or d_lambda discretisation values. The synthesis answer required by t0015 therefore
cannot reuse existing answer-asset content and must be written from the papers discovered during the
internet-research step.

### No Prior Cable-Theory Simulation or Calibration Has Run

Task [t0009] (calibrate dendritic diameters) is in progress and will produce diameter adjustments
for the t0005 morphology, but has not yet written any calibration result. Tasks
[t0008, t0010, t0011, t0012] are not yet started. The NEURON toolchain was installed and validated
by t0007 but no passive-cable or ZAP simulation has been run in the project. The t0015 survey
therefore cannot cross-check its numerical anchors (e.g., electrotonic-length estimates) against
simulated values from the project's own code; the numbers in the answer asset must rely on the
literature.

### t0002 Paper-Asset Spec Is the Template for t0015 Downloads

The 20 paper assets under [t0002] all use the v3 paper-asset specification (`details.json` +
canonical summary + `files/`). Folder names follow the DOI-slug produced by
`arf.scripts.utils.doi_to_slug`. Categories are drawn from `meta/categories/`. This pattern applies
directly to the 25 papers t0015 must download — no new spec work is required, and the existing
`/add-paper` skill will produce asset folders compatible with the aggregator.

## Reusable Code and Assets

**No library imports are available** (the project has zero registered libraries). All reusable items
below are either standard ARF utilities (always available) or patterns to **copy into task** where
applicable.

### ARF utility: `arf.scripts.utils.doi_to_slug`

* **Source**: `arf/scripts/utils/doi_to_slug.py`
* **What it does**: converts a DOI or DOI URL into the canonical slug used as the paper-asset folder
  name (e.g., `10.18653/v1/E17-1010` → `10.18653_v1_E17-1010`).
* **Reuse method**: **framework utility** — invoked automatically by the `/add-paper` skill; no
  copy or import required.
* **Function signatures**: `doi_to_slug(doi: str) -> str`.
* **Adaptation needed**: none.
* **Line count**: not applicable.

### t0002 paper asset pattern

* **Source**: e.g.,
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1162_neco.1997.9.6.1179/`
* **What it does**: reference layout for a paper asset conforming to spec v3 — `details.json` +
  `summary.md` + `files/` subdirectory.
* **Reuse method**: **follow the same layout** — t0015 must produce 25 folders of the same shape
  under `tasks/t0015_literature_survey_cable_theory/assets/paper/`.
* **Function signatures**: not code; layout template.
* **Adaptation needed**: populate each paper's fields from the candidate list in
  `research/research_internet.md`.

### t0002 `details.json` + `summary.md` content template

* **Source**: any paper under [t0002]
* **What it does**: concrete example of all required paper-asset fields and summary sections.
* **Reuse method**: **copy the field structure**; individual values must be supplied per-paper.
* **Line count**: ~60 lines of JSON, ~100 lines of Markdown per paper.
* **Adaptation needed**: per-paper metadata.

### No compartmental-model code to copy

No NEURON simulation code, calibration scripts, or analysis utilities from prior tasks is relevant
to this literature survey. Code reuse in t0015 is limited to following the paper-asset layout.

## Lessons Learned

* **Literature-survey tasks have succeeded cleanly when the category list is narrow** ([t0002]
  completed in one iteration with 20 papers). t0015 should therefore keep to its five cable-theory
  themes and not drift into dendritic computation or synaptic integration (those belong to t0016 and
  t0018).
* **Paywall handling was a minor source of friction in [t0002]**: a handful of DOIs needed manual
  review. For t0015 the task description prescribes a simpler rule — try once, and on failure mark
  `download_status: "failed"` plus append the DOI to `intervention/paywalled_papers.md`. No retries,
  no iterative re-attempts.
* **Answer assets benefit from explicit quantitative anchors**: the one answer produced so far
  ([t0013]) is strong because it makes a single concrete provenance claim. The t0015 answer should
  mirror this by framing its content around three numerical targets (electrotonic length L in
  0.6-1.0, tau_m in 10-30 ms, and a thin-dendrite propagation threshold matching the Goldstein-Rall
  regime).
* **The t0002 corpus did not include Rall foundational papers**. Downstream tasks that would have
  benefited from them (e.g., t0009 calibration) had to work around the gap. t0015 plugs this
  directly and should make those papers easy to locate via clear category tagging (`cable-theory`,
  `compartmental-modeling`, `dendritic-computation`).

## Recommendations for This Task

1. **Reuse the t0002 paper-asset pattern exactly** for all 25 downloads. No custom fields or layout
   variation [t0002].
2. **Register no new library**. This task produces papers and one answer; library scaffolding is
   unnecessary and would inflate review overhead.
3. **Cross-link each paper's categories with existing categories in `meta/categories/`**:
   `cable-theory`, `compartmental-modeling`, `dendritic-computation`, `retinal-ganglion-cell`,
   `voltage-gated-channels`, `synaptic-integration`, `direction-selectivity`, `patch-clamp`. Do not
   introduce new categories in this task.
4. **Frame the answer asset around the three quantitative anchors** identified in
   `research/research_internet.md` (L ≈ 0.6-1.0, tau_m ≈ 10-30 ms, Goldstein-Rall thin-dendrite
   regime) so that downstream calibration ([t0009]) can cite them without needing to re-read every
   paper.
5. **Follow the paywall policy from `task_description.md` to the letter**: one download attempt per
   paper, then `download_status: "failed"` + `intervention/paywalled_papers.md` entry.
6. **Cite [t0002] explicitly in the answer** to make clear what this survey adds on top of the
   existing corpus and where the existing corpus papers fit (three papers touching cable theory:
   Hines 1997, Schachter 2010, Branco 2010).

## Task Index

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: compartmental models of DS retinal ganglion cells
* **Status**: completed
* **Relevance**: Supplies the 20-DOI exclusion list for t0015 and the paper-asset template that
  t0015 must follow for its 25 downloads.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: in_progress
* **Relevance**: Downstream consumer of t0015's quantitative anchors (L, tau_m, propagation
  threshold). The answer asset must be written in a form t0009 can cite directly.

### [t0013]

* **Task ID**: `t0013_resolve_morphology_provenance`
* **Name**: Resolve dsgc-baseline-morphology source-paper provenance
* **Status**: not_started
* **Relevance**: Only prior task that produced an answer asset; its structure is the reference
  layout for the t0015 synthesis answer.
