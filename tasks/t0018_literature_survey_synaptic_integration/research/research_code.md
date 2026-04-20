---
spec_version: "1"
task_id: "t0018_literature_survey_synaptic_integration"
research_stage: "code"
tasks_reviewed: 8
tasks_cited: 8
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-20"
status: "complete"
---
# Research Code: Prior Task Assets for the Synaptic-Integration Literature Survey

## Task Objective

Survey five canonical papers that supply priors for receptor kinetics (AMPA/NMDA/GABA), shunting
inhibition, balanced E-I temporal co-tuning, dendritic-location-dependent PSP integration, and
SAC-to-DSGC inhibitory asymmetry for the DSGC compartmental model being developed in sibling tasks.
Produce one answer asset that tabulates a prior distribution per DOI and theme. This research-code
step establishes which prior task assets (skills, specifications, code fragments) can be reused and
which must be re-authored inside this task.

## Library Landscape

No `assets/library/` entries exist anywhere in the project, and the repository does not provide an
`aggregate_libraries` aggregator — only aggregators for tasks, papers, answers, datasets, costs,
suggestions, metrics, machines, and categories are present. No libraries are registered and no
cross-task library imports are therefore possible. This section is intentionally short because the
library landscape is empty at this point in the project; the paper/answer asset producers are the
only cross-task reuse surfaces available.

## Key Findings

### Paper Asset Workflow Established by t0002 and Reused in t0015-t0017

`[t0002]` established the canonical paper-asset pipeline for this project: 20 DSGC-modelling papers
were downloaded with `details.json` v3 metadata, `summary.md` documents, and PDFs under
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/<paper_id>/files/`. The same
convention is mandated by `meta/asset_types/paper/specification.md` v3. `[t0015]`, `[t0016]`, and
`[t0017]` each refined the pattern for paywalled-only paper sets by using
`download_status: "failed"` with a non-null `download_failure_reason` plus
`intervention/paywalled_papers.md`; all five of this task's shortlisted DOIs are paywalled so the
same pattern applies.

### Crossref Fetcher and Paper-Asset Builder Exist in t0017

`[t0017]` wrote `code/fetch_paper_metadata.py` that reads a `SHORTLIST` constant of DOIs and queries
Crossref at `https://api.crossref.org/works/<DOI>` with a polite `mailto` User-Agent, then writes
`plan/crossref_metadata.json`. `[t0017]` also wrote `code/build_paper_asset.py` that consumes the
cached JSON and materialises `assets/paper/<slug>/` folders with v3 `details.json` and a 9-section
`summary.md`, handling the `download_status: "failed"` path. Both scripts use
`arf.scripts.utils.doi_to_slug` and are the right pattern to copy into this task's `code/` folder
with the DOI list and theme/category adjusted.

### Answer Asset Format: Spec v2

`[t0002]`, `[t0007]`, `[t0015]`, `[t0016]`, and `[t0017]` each produced a single answer asset under
`assets/answer/<slug>/`. Each answer folder contains `details.json`, `short_answer.md`, and
`full_answer.md`. The slug is a kebab-case of the question, not a DOI. The prior-distribution table
for this task (mapping 5 papers to receptor kinetics, shunting inhibition, E-I balance, dendritic
attenuation, and SAC asymmetry priors) should live in `full_answer.md` as a Markdown table, matching
the precedent set by prior answer assets.

### Target Tuning Curve, Morphology, and Simulator Already Set

`[t0004]` produced `code/generate_target.py` with `GeneratorParams` defining `theta_pref_deg=90`,
`r_base_hz=2.0`, `r_peak_hz=32.0`, `n=2.0`, `n_angles=12`, `n_trials=20`, `noise_sd_hz=3.0`. These
define the numerical targets (preferred-direction rate, baseline rate, DSI band 0.6-0.9) that
downstream model-fitting tasks will use; the synaptic-integration priors from this survey feed that
same model. `[t0005]` produced the validated mouse ooDSGC SWC morphology and `[t0007]` installed
NEURON 8.2.7 / NetPyNE 1.0.7 under Python 3.13. The pipeline that will consume this survey's priors
is thus already standing.

### Prior Literature-Survey Mechanics (t0015, t0016, t0017)

`[t0015]` (passive cable), `[t0016]` (dendritic computation), and `[t0017]` (patch-clamp) each
produced paywalled-only paper sets with `build_paper_asset.py` after a Crossref-metadata preflight.
All three wrote summaries using the Crossref abstract plus training-data recall pattern, not
PDF-level reading, and all three passed `verify_paper_asset` with that format. This task follows the
same mechanical recipe exactly.

## Reusable Code and Assets

* **Paper asset specification** — `meta/asset_types/paper/specification.md` v3. Reuse method:
  **follow as authoritative spec**. No code to copy. Dictates `details.json` fields, `summary.md`
  frontmatter, `summary_path`, `files/` layout, and verificator codes `PA-E*`/`PA-W*`.

* **Crossref fetcher** — `tasks/t0017_literature_survey_patch_clamp/code/fetch_paper_metadata.py`.
  Reuse method: **copy verbatim into `code/` and adjust the `SHORTLIST` constant** to the five new
  DOIs (`10.1038/346565a0`, `10.1073/pnas.80.9.2799`, `10.1038/nature02116`,
  `10.1016/s0959-4388(03)00075-8`, `10.1038/nature00931`). Approx. 80 lines.

* **Paper asset builder** — `tasks/t0017_literature_survey_patch_clamp/code/build_paper_asset.py`.
  Reuse method: **copy verbatim into `code/` and adjust `TASK_ID` plus `THEME_CATEGORIES`** so each
  DOI gets `synaptic-integration` primary plus one secondary theme tag. Approx. 250 lines.

* **`doi_to_slug` utility** — `arf/scripts/utils/doi_to_slug.py`. Reuse method: **import as
  module**. Canonical DOI-to-folder-name conversion. Required by paper-asset spec v3 (`PA-E011`).

* **Answer asset precedent** — any answer folder from `[t0015]`, `[t0016]`, or `[t0017]` (e.g.
  `tasks/t0017_literature_survey_patch_clamp/assets/answer/what-patch-clamp-observables-constrain-the-dsgc-model/`).
  Reuse method: **use as structural template** for `details.json` v2, `short_answer.md` (3
  sections), and `full_answer.md` (9 sections).

* **Paywalled intervention pattern** — `[t0015]`, `[t0016]`, `[t0017]` each wrote
  `intervention/paywalled_papers.md`. Reuse method: **follow the pattern** — create
  `intervention/paywalled_papers.md` listing DOI, title, Crossref abstract availability, and
  manual-retrieval recommendation.

## Lessons Learned

* Paywalled-only surveys are tractable in this project so long as the Crossref-abstract-plus-
  training-data summary pattern is followed. `[t0015]`, `[t0016]`, and `[t0017]` all succeeded with
  this recipe; no alternative-source retrieval beyond Crossref is needed for the t0018 shortlist.
* `doi_to_slug` must be used as the canonical module. Hand-conversion of DOIs to folder names causes
  `PA-E011` verificator errors (`[t0002]` and `[t0017]` both reinforced this).
* `[t0007]` confirmed NEURON 8.2.7 pins Python 3.13 at the project level. No impact on this
  literature task, but the downstream DSGC model that will consume these priors runs under that pin.
* `[t0017]` showed that `build_paper_asset.py` must explicitly handle the
  `download_status: "failed"` path (populate `files: []`, write a `files/.gitkeep` so git preserves
  the directory, write `download_failure_reason`). Reuse this logic as-is.
* Committing logs after every flowmark-triggered edit avoids the recurring
  `POSTSTEP ERROR: Working tree is not clean` pattern observed across t0015-t0017.

## Recommendations for This Task

1. **Copy `[t0017]`'s `fetch_paper_metadata.py` and `build_paper_asset.py` into `code/`** and adjust
   the DOI list to the five shortlisted DOIs plus `THEME_CATEGORIES` per theme.
2. **Follow `[t0017]`'s answer-asset structure**. The DOI-to-theme-and-prior table goes in
   `full_answer.md`; `short_answer.md` is 3 paragraphs; `details.json` follows spec v2.
3. **Record all 5 DOIs in `intervention/paywalled_papers.md`** up front — no PDF retrieval is
   attempted; the Crossref-abstract-plus-training-data pattern is the planned path.
4. **Use `synaptic-integration` as the primary category on all 5 papers**; add one secondary
   category per theme (e.g. `direction-selectivity`, `dendritic-computation`, `cable-theory`).
5. **Skip `assets/library/`** — no library is needed or appropriate for a literature survey.

## Task Index

### [t0001]

* **Task ID**: `t0001_brainstorm_results_1`
* **Name**: Brainstorm: results 1
* **Status**: completed
* **Relevance**: Upstream brainstorm round that seeded the project's literature strategy.

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: DSGC compartmental models
* **Status**: completed
* **Relevance**: Established canonical paper-asset pipeline and answer-asset structure; defines the
  20-DOI exclusion list this survey must avoid.

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate target tuning curve
* **Status**: completed
* **Relevance**: Defines numerical tuning-curve targets that downstream model fitting consumes
  alongside the synaptic-integration priors from this survey.

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download DSGC morphology
* **Status**: completed
* **Relevance**: Mouse ooDSGC morphology used by the compartmental model that will apply the
  receptor-kinetics and shunting-inhibition priors assembled here.

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install NEURON + NetPyNE
* **Status**: completed
* **Relevance**: Confirms the simulator that will consume this survey's priors is installed.

### [t0015]

* **Task ID**: `t0015_literature_survey_cable_theory`
* **Name**: Literature survey: cable theory
* **Status**: completed
* **Relevance**: First paywalled-only survey in this project; established the Crossref-abstract-
  plus-training-data summary pattern that this task reuses.

### [t0016]

* **Task ID**: `t0016_literature_survey_dendritic_computation`
* **Name**: Literature survey: dendritic computation
* **Status**: completed
* **Relevance**: Second paywalled-only survey; reinforced the download-status-failed pattern and the
  one-secondary-category-per-theme tagging approach.

### [t0017]

* **Task ID**: `t0017_literature_survey_patch_clamp`
* **Name**: Literature survey: patch-clamp methodology
* **Status**: completed
* **Relevance**: Third paywalled-only survey; its `fetch_paper_metadata.py` and
  `build_paper_asset.py` scripts are the templates this task copies and adjusts.
