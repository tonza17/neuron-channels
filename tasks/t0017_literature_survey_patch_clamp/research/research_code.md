---
spec_version: "1"
task_id: "t0017_literature_survey_patch_clamp"
research_stage: "code"
tasks_reviewed: 8
tasks_cited: 8
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-20"
status: "complete"
---
# Research Code: Prior Task Assets for the Patch-Clamp Literature Survey

## Task Objective

Survey approximately 25 category-relevant papers on patch-clamp recordings of retinal ganglion cells
(RGCs) — especially DSGCs — that supply validation targets (somatic spike rates, EPSC/IPSC
kinetics, null/preferred ratios, space-clamp error bounds) for the DSGC compartmental model being
built in sibling tasks, and produce one answer asset linking each paper's DOI to the specific
model-validation observable it contributes.

## Library Landscape

No `assets/library/` entries exist anywhere in the project, and the repository does not provide an
`aggregate_libraries` aggregator — only aggregators for tasks, papers, answers, datasets, costs,
suggestions, metrics, machines, and categories are present. No libraries are registered and no
cross-task library imports are therefore possible. This section is intentionally short because the
library landscape is empty at this point in the project; the paper/answer asset producers are the
only cross-task reuse surfaces available.

## Key Findings

### Paper Asset Workflow in the Project

`[t0002]` established the canonical paper-asset pipeline for this project: 20 DSGC-modelling papers
were downloaded with full `details.json` v3 metadata, `summary.md` documents, and PDFs under
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/<paper_id>/files/`. The same
convention is mandated by `meta/asset_types/paper/specification.md` v3 and is what this task must
follow. `[t0002]` also demonstrated that the `/add-paper` skill is the canonical mechanism for
producing one asset at a time and that paywalled papers must be recorded with
`download_status: "failed"` plus a non-null `download_failure_reason` — the same pattern the
`intervention/paywalled_papers.md` file for this task will use.

### Answer Asset Format

`[t0002]`, `[t0003]`, and `[t0007]` each produced a single answer asset under
`assets/answer/<slug>/`. Each answer folder contains `details.json`, `short_answer.md`, and
`full_answer.md`. The slug is a short-description of the question, not a DOI. The DOI-to-validation-
target table for this task (mapping ~25 papers to AP rate, IPSC asymmetry, EPSP kinetics,
null/preferred ratios) should live in `full_answer.md` as a Markdown table, matching the precedent
set by
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/full_answer.md`.

### Target Tuning-Curve Generator Already Exists

`[t0004]` produced `code/generate_target.py` (~180 lines) that synthesizes the reference tuning
curve the DSGC model must reproduce. `GeneratorParams` defines `theta_pref_deg=90`, `r_base_hz=2.0`,
`r_peak_hz=32.0`, `n=2.0` (von Mises-like sharpness), `n_angles=12`, `n_trials=20`,
`noise_sd_hz=3.0`. Those values define the numerical targets (preferred-direction rate, baseline
rate, DSI band 0.6-0.9) that the papers surveyed here must furnish evidence for. This task is purely
literature — no code is generated — but the generator parameters give us the yardstick against
which published firing rates will be classified.

### Morphology Baseline

`[t0005]` produced a validated SWC morphology for a mouse ooDSGC that the compartmental model will
use; `code/validate_swc.py` (~120 lines) checks topology. Patch-clamp papers surveyed here should
ideally come from mouse ooDSGCs to match that morphology, or from rabbit/primate DSGCs where the
morphology is known to be similar. This informs which papers in the survey are highest-relevance.

### Simulator and Install Baseline

`[t0003]` picked NEURON+NetPyNE as the target simulator. `[t0007]` installed NEURON 8.2.7 / NetPyNE
1.0.7 under Python 3.13 and produced `sanity_netpyne.py` and `sanity_raw_neuron.py`. These confirm
that the downstream tasks using this survey's validation data can actually run compartmental
simulations — i.e. the patch-clamp measurements selected here will have a working numerical model
to validate against.

### Prior Literature Survey Mechanics (t0002)

`[t0002]` downloaded 20 DSGC-modelling papers and, in its post-task report, listed the exclusion
DOIs now reused in this task's `research/research_papers.md`. It also provides a worked example of
how many paywalled failures to expect: ~15-20% of attempted downloads required an intervention file.
That failure rate is the planning baseline for this task's paper-download step.

### Brainstorm Source Traceability

`[t0014]` produced suggestion S-0014-03 that seeded this task (patch-clamp literature survey). No
code; the `suggestions.json` from `[t0014]` records the motivation and links this task back to the
earlier brainstorm round (`[t0006]`, then `[t0001]`).

## Reusable Code and Assets

* **Paper asset specification** — `meta/asset_types/paper/specification.md` v3. Reuse method:
  **follow as authoritative spec**. No code to copy. Dictates `details.json` fields, `summary.md`
  frontmatter, `summary_path`, `files/` layout, and verificator codes `PA-E*`/`PA-W*`.

* **`/add-paper` skill** — `arf/skills/add-paper/SKILL.md` (read by subagent). Reuse method:
  **invoke via skill**, one subagent per paper. This is the canonical way to produce each of the ~25
  paper assets for this task. No code to copy.

* **Exclusion DOI list** — `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`
  (20 folders). Reuse method: **copy the folder-name list as an exclusion set**. Any DOI already
  present there must not be re-added by this task. The 20 DOIs are already enumerated in this task's
  `research/research_papers.md` gaps section.

* **Target tuning-curve parameters** —
  `tasks/t0004_generate_target_tuning_curve/code/generate_target.py` `GeneratorParams` (approx.
  lines 36-45). Reuse method: **copy into task** if needed for the answer asset's validation-target
  table. ~10 lines. Likely not needed — the values (2 Hz baseline, 32 Hz peak, DSI 0.6-0.9) can
  simply be cited as `[t0004]` in the answer.

* **Answer asset precedent** —
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/`
  (details.json, short_answer.md, full_answer.md). Reuse method: **use as structural template**. The
  answer produced by this task should mirror the table layout and citation style.

* **Paywalled intervention pattern** — `[t0002]` recorded a handful of paywalled DOIs in its
  `intervention/` folder. Reuse method: **follow the pattern** — create
  `intervention/paywalled_papers.md` listing DOI, title, access-failure reason, and whether a manual
  retrieval attempt is requested.

## Lessons Learned

* Paywalled papers account for a non-trivial fraction of attempts in `[t0002]` and `[t0003]` —
  expect 3-6 failures out of 25 attempted here. Budget time to record each cleanly in the
  intervention file rather than trying alternate sources beyond a single attempt.
* `[t0002]` found that setting DOIs in folder names with slashes converted to underscores via the
  `doi_to_slug` utility is essential — hand-conversion causes `PA-E011` verificator errors.
* `[t0007]` confirmed NEURON 8.2.7 pins Python 3.13 at the project level. No impact on this
  literature task, but any follow-up implementation that codes up patch-clamp protocol simulators
  must respect that pin.
* `[t0004]` showed that mean tuning-curve parameters (2 Hz baseline, 32 Hz peak, DSI 0.6-0.9) are
  the concrete numerical targets downstream tasks consume; the survey must therefore prioritize
  papers that publish absolute firing rates in Hz, not only normalized curves.

## Recommendations for This Task

1. **Use the `/add-paper` skill, one subagent per paper**, for all ~25 new DOIs identified in
   `research/research_internet.md`. Do not batch.
2. **Apply the exclusion list from `research/research_papers.md`** — 20 `[t0002]` DOIs must be
   skipped even if they surface again in search results.
3. **Follow `[t0002]`'s answer-asset structure**. The DOI -> validation-target table goes in
   `full_answer.md`; `short_answer.md` summarizes in <=3 paragraphs; `details.json` follows v2 spec.
4. **Cite `[t0004]`'s tuning-curve parameters** (2 Hz baseline, 32 Hz peak, DSI 0.6-0.9) as the
   numerical targets the paper set must match; do not re-copy the generator.
5. **Budget 3-6 paywalled failures** and write them into `intervention/paywalled_papers.md` as they
   occur rather than at the end. No alternate-source attempts beyond one.
6. **Match mouse/rabbit/primate DSGC preparations** preferentially (aligns with `[t0005]`'s
   morphology choice). Cortical recordings are out of scope.
7. **No new library is needed or appropriate**. Do not create an `assets/library/` entry.

## Task Index

### [t0001]

* **Task ID**: `t0001_brainstorm_results_1`
* **Name**: Brainstorm: results 1
* **Status**: completed
* **Relevance**: Upstream brainstorm round that seeded the project's literature strategy; informs
  the framing that motivates this patch-clamp survey.

### [t0002]

* **Task ID**: `t0002_literature_survey_dsgc_compartmental_models`
* **Name**: Literature survey: DSGC compartmental models
* **Status**: completed
* **Relevance**: Produced the 20-paper DSGC-modelling corpus that defines this task's exclusion list
  and the canonical paper-asset and answer-asset precedents.

### [t0003]

* **Task ID**: `t0003_simulator_library_survey`
* **Name**: Simulator library survey
* **Status**: completed
* **Relevance**: Picked NEURON+NetPyNE as the simulator the validation data from this survey will
  eventually be compared against; also an example of single-answer-asset formatting.

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate target tuning curve
* **Status**: completed
* **Relevance**: Defines the numerical tuning-curve targets (2 Hz baseline, 32 Hz peak, DSI 0.6-0.9)
  that patch-clamp papers in this survey must supply evidence for.

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download DSGC morphology
* **Status**: completed
* **Relevance**: Provides the mouse ooDSGC morphology that downstream model-fitting will use; guides
  species-matching when prioritizing patch-clamp papers.

### [t0006]

* **Task ID**: `t0006_brainstorm_results_2`
* **Name**: Brainstorm: results 2
* **Status**: completed
* **Relevance**: Second brainstorm round referenced by `[t0014]` in the traceability chain that led
  to this task's source suggestion S-0014-03.

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install NEURON + NetPyNE
* **Status**: completed
* **Relevance**: Demonstrates the single-answer-asset reporting pattern; confirms the simulator
  stack that will consume this survey's validation targets is installed and working.

### [t0014]

* **Task ID**: `t0014_brainstorm_results_3`
* **Name**: Brainstorm: results 3
* **Status**: completed
* **Relevance**: Produced suggestion S-0014-03 that seeded this patch-clamp literature survey.
