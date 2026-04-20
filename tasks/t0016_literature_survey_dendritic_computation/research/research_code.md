---
spec_version: "1"
task_id: "t0016_literature_survey_dendritic_computation"
research_stage: "code"
tasks_reviewed: 10
tasks_cited: 7
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Review prior tasks in the project for reusable code, libraries, datasets, and lessons learned that
can support the literature survey on dendritic computation (t0016). Because this task produces
literature papers plus one answer asset, the focus is on the answer-asset precedent, the paper asset
layout, and the existing DSGC morphology and tuning-curve datasets that the answer must reference.

## Library Landscape

No registered libraries were discovered under `assets/library/` across any completed task at the
time of this survey. The project's library aggregator module is not implemented in this fork, so
library discovery was performed by direct filesystem enumeration
(`find tasks -type d -name library`), which returned zero results. Consequently, **0 libraries are
available for import**, and all reusable code from prior tasks must be copied into the current
task's `code/` directory per the cross-task import rule. This task is primarily literature work and
will not require computational code beyond the canonical asset-layout scripts already used by the
execute-task skill, so the absence of libraries is not blocking.

## Key Findings

### Paper-asset conventions are well established from t0002

The closest precedent is [t0002], which produced the 20 DSGC-related paper assets that this task
excludes from its own download target. Each paper lives at
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/<doi_slug>/` and contains
`details.json`, `summary.md`, and a `files/` subfolder with the paper PDF or markdown conversion.
All 20 t0002 paper assets follow spec_version 3. The summary documents average ~200 lines with the
seven canonical sections; the Oesch2005 summary used as the reference template in this task's
`research_papers.md` is ~215 lines long. This layout is the direct template for the ~25 paper assets
this task will produce in step 9.

### Answer-asset precedent from t0002 and t0003

Two prior tasks have produced answer assets. [t0002] wrote
`how-does-dsgc-literature-structure-the-five-research-questions`, a literature-survey answer
mirroring the structure this task needs. [t0003] wrote `dsgc-compartmental-simulator-choice`, an
answer synthesising findings across multiple references into a single recommendation. Both answers
use the canonical spec_version 2 layout with `details.json`, `short_answer.md`, and
`full_answer.md`. The t0002 answer is the direct stylistic template for the DSGC-motifs answer this
task will write in step 9, because it mirrors our task's structure: synthesise literature-derived
mechanisms into DSGC-specific modelling predictions.

### Dataset assets establish quantitative anchors

[t0005] produced `dsgc-baseline-morphology` (raw morphology from NeuroMorpho) and [t0004] produced
`target-tuning-curve` (the empirical DSI/DSR target curve). Both anchor the downstream modelling
work that this task's answer must connect to. The [t0009] task (in progress) is calibrating the raw
morphology diameters to published values, so the morphology dataset will evolve; the
dendritic-computation answer should therefore cite morphology in generic terms (e.g., "distal branch
diameters of 0.3-1.0 um per t0009 calibration") rather than pinning specific values that may change.

### Task-type structure confirms literature-survey template

[t0002], [t0003], [t0015] (in progress, cable-theory survey), and [t0017] (in progress, patch-clamp
survey) all share the `literature-survey` task type. The step structure across these sibling
literature-survey tasks is identical (create-branch, check-deps, init-folders, research-papers,
research-internet, research-code, planning, implementation, results, suggestions, reporting), and
the execute-task skill applies the same canonical set of skipped steps (setup-machines, teardown,
creative-thinking, compare-literature). [t0015]'s completed research-papers stage (commit e0a354e)
is a direct template for how to integrate prior-corpus findings with new internet-discovered papers.

### Infrastructure conventions

Every completed task includes a `logs/` directory with `commands/`, `sessions/`, `searches/`, and
`steps/` subfolders; all CLI calls are wrapped by `arf/scripts/utils/run_with_logs.py` when run on a
task branch. The step lifecycle (prestep, do work, commit, poststep) is enforced by
`arf/scripts/utils/prestep.py` and `arf/scripts/utils/poststep.py`. This task is following the same
pattern and has so far produced steps 1-5 with that infrastructure.

## Reusable Code and Assets

All items below are paths inside the project. Because no libraries exist, every reusable item is
labelled **copy into task** when applicable; most items are read-only templates that do not require
copying.

* **Source**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md`
  * **What it does**: Reference 215-line paper summary following spec_version 3 canonical structure
    (Metadata, Abstract, Overview, Architecture/Models/Methods, Results, Innovations, Datasets, Main
    Ideas, Summary).
  * **Reuse method**: read-only template; no copy needed (the summary tool or download workflow can
    mimic the layout directly).
  * **Adaptation needed**: None - used as stylistic reference only.

* **Source**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/`
  * **What it does**: Reference literature-survey answer asset (spec_version 2) with `details.json`,
    `short_answer.md`, `full_answer.md`.
  * **Reuse method**: read-only template for the DSGC-motifs answer.
  * **Adaptation needed**: Restate the scope for this task's dendritic-computation focus.

* **Source**:
  `tasks/t0003_simulator_library_survey/assets/answer/dsgc-compartmental-simulator-choice/`
  * **What it does**: Second answer-asset example confirming the spec_version 2 layout.
  * **Reuse method**: read-only template.
  * **Adaptation needed**: None.

* **Source**: `arf/scripts/verificators/verify_paper_asset.py`
  * **What it does**: Validates the paper asset structure per spec_version 3. Catches errors like
    PA-E013 (missing spec_version), PA-E014 (failed download without reason), PA-E015 (invalid
    download_status).
  * **Reuse method**: Invoke directly; no copy required.
  * **Function signatures**: Called as
    `uv run python -m arf.scripts.verificators.verify_paper_asset <task_id> [<paper_id>]`.
  * **Adaptation needed**: None.

* **Source**: `arf/scripts/verificators/verify_answer_asset.py`
  * **What it does**: Validates answer asset structure per spec_version 2.
  * **Reuse method**: Invoke directly before committing the answer.
  * **Adaptation needed**: None.

* **Source**: `meta/asset_types/paper/specification.md` and
  `meta/asset_types/answer/specification.md`
  * **What it does**: Authoritative asset-format specifications.
  * **Reuse method**: Read before creating assets.
  * **Adaptation needed**: None.

## Lessons Learned

From reviewing [t0002]'s and [t0003]'s completed execution logs and the t0015 research-papers commit
(e0a354e):

* Paper downloads against Nature/Science/Neuron commonly fail with HTTP 403; [t0002] reports several
  paywalled DOIs that required `download_status: "failed"` handling. Plan accordingly.
* Summary documents have minimum word counts (500 words total; 4 paragraphs in `## Summary`). Short
  summaries trigger PA-W001 warnings. Aim for 800-1200 words per summary to be safe.
* Verificators occasionally mismatch on DOI metadata when the PDF provides a different DOI than the
  download URL; always copy the DOI verbatim from the publisher landing page into `details.json`.
* Paywalled papers can still yield valuable `details.json` metadata from the abstract; do not skip
  the `summary.md` - use the abstract-based Overview path documented in the paper spec.
* Running `uv run flowmark --inplace --nobackup` on all created/edited `.md` files is mandatory; the
  pre-commit hook fails otherwise (this task already fixed one such issue in the research_internet
  step).
* The `--step-log-dir` flag in `init_task_folders` rejects absolute paths from run_with_logs; the
  orchestrator falls back to manual artefact writing (documented in step 3 of this task).

## Recommendations for This Task

1. **Adopt the t0002 paper-summary layout wholesale** for every paper this task downloads. The
   Oesch2005 summary in
   `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md`
   is the reference template.

2. **Mirror the t0002 answer-asset layout** for the dendritic-motifs-for-DSGC answer this task will
   produce. Use `details.json` (spec_version 2), `short_answer.md` (<=200 words), and
   `full_answer.md` (synthesising the 25 new papers plus the t0002 10 cited papers).

3. **Plan for a high paywall-failure rate**: ~10-15 of the 25 candidate DOIs are in paywalled venues
   (Nature, Science, Neuron, Nat Neurosci). Have the paywalled-paper intervention file ready; this
   task's brief already instructs the agent to attempt once, then record
   `download_status: "failed"`.

4. **Do not build new Python libraries** for this task. The output is literature and one answer
   asset; computational code is out of scope. If any helper script is needed (e.g., batch DOI
   validation), keep it inside `tasks/t0016_.../code/` and do not register as a library.

5. **Reference morphology and tuning-curve datasets generically**: because [t0005] and [t0004]
   datasets are still being calibrated (via [t0009]), cite them by asset name rather than by
   specific numbers the answer might hard-code.

6. **Run both asset verificators** (`verify_paper_asset.py`, `verify_answer_asset.py`) before
   committing step 9 implementation outputs.

## Task Index

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: DSGC compartmental models
* **Status**: completed
* **Relevance**: Produced the 20 DSGC paper assets excluded from this task's download target, the
  canonical answer-asset layout, and the reference summary template.

### [t0003]

* **Task ID**: `t0003_simulator_library_survey`
* **Name**: Simulator library survey
* **Status**: completed
* **Relevance**: Second completed literature-survey task; provides a second answer-asset precedent.

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate target DSGC tuning curve
* **Status**: completed
* **Relevance**: Supplies the target-tuning-curve dataset the dendritic-motifs answer will reference
  as the quantitative target for DSGC direction-selectivity modelling.

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download DSGC baseline morphology
* **Status**: completed
* **Relevance**: Supplies the dsgc-baseline-morphology dataset; the answer will reference its
  diameter taper (via the in-progress [t0009] calibration) when discussing sublinear vs supralinear
  integration.

### [t0015]

* **Task ID**: `t0015_literature_survey_cable_theory`
* **Name**: Literature survey: cable theory
* **Status**: in_progress
* **Relevance**: Sibling literature-survey task covering the adjacent cable-theory category; cited
  as a structural template and as a coordination point to avoid overlap.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters
* **Status**: in_progress
* **Relevance**: Calibrating the raw DSGC morphology diameters to published values. The answer asset
  should cite morphology diameters generically because t0009 will update the values.

### [t0017]

* **Task ID**: `t0017_literature_survey_patch_clamp`
* **Name**: Literature survey: patch-clamp
* **Status**: in_progress
* **Relevance**: Sibling literature-survey task covering the adjacent patch-clamp category; cited as
  a coordination point to avoid overlap on experimental-methods papers.
