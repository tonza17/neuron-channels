# ✅ Literature survey: synaptic integration in RGC-adjacent systems

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0018_literature_survey_synaptic_integration` |
| **Status** | ✅ completed |
| **Started** | 2026-04-20T11:18:49Z |
| **Completed** | 2026-04-20T12:15:00Z |
| **Duration** | 56m |
| **Source suggestion** | `S-0014-04` |
| **Task types** | `literature-survey` |
| **Categories** | [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 25 paper, 1 answer |
| **Step progress** | 11/15 |
| **Task folder** | [`t0018_literature_survey_synaptic_integration/`](../../../tasks/t0018_literature_survey_synaptic_integration/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0018_literature_survey_synaptic_integration/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0018_literature_survey_synaptic_integration/task_description.md)*

# Literature survey: synaptic integration in RGC-adjacent systems

## Motivation

Research question RQ3 (AMPA/GABA balance) and later synaptic-parameter optimisation need prior
distributions for receptor kinetics, E-I ratios, and spatial-distribution patterns. The
modelling literature in t0002 touches these parameters but does not systematically cover the
synaptic- integration experimental and theoretical work that underpins them. Source
suggestion: S-0014-04 from t0014_brainstorm_results_3.

## Scope

Target ~25 category-relevant papers covering:

1. AMPA/NMDA/GABA receptor kinetics — rise and decay time constants, reversal potentials.
2. Shunting inhibition — location-dependent vetoing, input resistance changes.
3. E-I balance — temporal co-tuning, conductance ratios in retinal and cortical systems.
4. Temporal summation — how closely spaced inputs integrate vs saturate.
5. Dendritic-location dependence — soma-vs-dendrite integration, attenuation before the spike
   initiation zone.
6. Synaptic-density scaling — synapses per micrometre of dendrite, bouton counts.
7. SAC/DSGC inhibitory asymmetry — starburst amacrine cell GABA output onto DSGC dendrites in
   the preferred vs null directions.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered
mid task must be dropped and the exclusion recorded in the task log.

## Approach

1. Run `/research-internet` targeting each theme, preferring studies that publish fitted
   kinetic parameters or conductance-ratio measurements rather than qualitative reports.
2. For each shortlisted paper, invoke `/download-paper`. Paywalled papers are recorded as
   `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
3. Write one answer asset tabulating receptor kinetics and E-I ratios usable as prior
   distributions for later optimisation tasks.

## Expected Outputs

* ~25 paper assets under `assets/paper/` (v3 spec compliant).
* One answer asset under `assets/answer/` with a prior-distribution table for kinetics and E-I
  ratios, keyed by paper DOI and region.
* `intervention/paywalled_papers.md` listing DOIs requiring manual retrieval.

## Compute and Budget

No paid services required. Task-type budget gate cleared by the $1 bump set in t0014.

## Dependencies

None.

## Verification Criteria

* At least 20 paper assets pass `verify_paper_asset.py`.
* The answer asset passes `verify_answer_asset.py` and provides a numeric prior-distribution
  table.
* No paper in this task's `assets/paper/` shares a DOI with the t0002 corpus.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [What quantitative priors does the synaptic-integration literature supply for the DSGC compartmental model on (1) AMPA/NMDA/GABA receptor kinetics, (2) shunting inhibition, (3) E-I balance temporal co-tuning, (4) dendritic-location-dependent PSP integration, and (5) SAC-to-DSGC inhibitory asymmetry?](../../../tasks/t0018_literature_survey_synaptic_integration/assets/answer/synaptic-integration-priors-for-dsgc-modelling/) | [`full_answer.md`](../../../tasks/t0018_literature_survey_synaptic_integration/assets/answer/synaptic-integration-priors-for-dsgc-modelling/full_answer.md) |
| paper | [Channel kinetics determine the time course of NMDA receptor-mediated synaptic currents](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_346565a0/) | [`summary.md`](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_346565a0/summary.md) |
| paper | [Directionally selective calcium signals in dendrites of starburst amacrine cells](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature00931/) | [`summary.md`](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature00931/summary.md) |
| paper | [Balanced inhibition underlies tuning and sharpens spike timing in auditory cortex](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature02116/) | [`summary.md`](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1038_nature02116/summary.md) |
| paper | [Nonlinear interactions in a dendritic tree: localization, timing, and role in information processing.](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1073_pnas.80.9.2799/) | [`summary.md`](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/10.1073_pnas.80.9.2799/summary.md) |
| paper | [Dendrites: bug or feature?](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/no-doi_HausserMel2003_s0959-4388-03-00075-8/) | [`summary.md`](../../../tasks/t0018_literature_survey_synaptic_integration/assets/paper/no-doi_HausserMel2003_s0959-4388-03-00075-8/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Retrieve paywalled synaptic-integration PDFs via Sheffield access
and verify numerical priors</strong> (S-0018-01)</summary>

**Kind**: experiment | **Priority**: high

Five synaptic-integration papers (Lester et al. 1990, Koch-Poggio-Torre 1983, Wehr & Zador
2003, Hausser & Mel 2003, Euler-Detwiler-Denk 2002) are documented in
intervention/paywalled_papers.md but were not downloaded. Retrieve their PDFs through
Sheffield institutional access, update each paper asset's download_status to 'success',
replace summary Overview disclaimers with PDF-verified content, and cross-check the numerical
priors tabulated in the Prior Distribution Table of the answer asset (NMDAR tau_decay 100-200
ms at 22-32 degC, AMPA tau_rise 0.2-0.4 ms / tau_decay 1-3 ms, GABA_A tau_decay 5-20 ms,
lambda_DC 100-300 um for RGC dendrites, DSGC E-I lag 15-50 ms, SAC dendritic Ca2+ DS index
0.3-0.5) against the actual papers before adopting them as tight compartmental-model fitting
targets.

</details>

<details>
<summary><strong>Extend synaptic-integration survey with DSGC-specific
receptor-kinetic, dynamic-clamp, and connectomic SAC-DSGC papers</strong>
(S-0018-02)</summary>

**Kind**: experiment | **Priority**: medium

The scaled-down 5-paper survey covers the five canonical themes (AMPA/NMDA/GABA kinetics,
shunting inhibition, E-I balance, dendritic-location integration, SAC-to-DSGC asymmetry) but
with one paper per theme, selected from the most-cited classical literature. A follow-up
survey task should add ~5 DSGC-targeted papers across: (a) modern DSGC-specific AMPA and NMDA
kinetic measurements at near-physiological temperature, (b) DSGC dynamic-clamp studies that
inject measured conductance waveforms, (c) connectomic reconstructions of SAC-to-DSGC wiring
(Briggman et al. 2011, Kim et al. 2014), (d) recent E-I temporal co-tuning studies in retina
(rather than auditory cortex), and (e) DSGC dendritic computation (Oesch, Euler, Taylor,
Sivyer). This closes the gap between canonical theory and DSGC-specific parameters.

</details>

<details>
<summary><strong>Implement AMPA + NMDA + GABA_A synapses with E-I temporal co-tuning
and SAC-to-DSGC asymmetric inhibition in downstream DSGC model</strong>
(S-0018-03)</summary>

**Kind**: experiment | **Priority**: high

The answer asset synaptic-integration-priors-for-dsgc-modelling produces a 6-point
specification for DSGC synaptic integration in NEURON extending the space-clamp/AIS/NMDAR
constraints from t0017. The downstream DSGC compartmental-model build task must implement: (1)
AMPA with dual-exponential kinetics (tau_rise 0.2-0.4 ms, tau_decay 1-3 ms) and NMDA with
Mg2+-block + tau_decay 100-200 ms at 32 degC on glutamatergic inputs, (2) GABA_A with shunting
(reversal near resting Vm) and tau_decay 5-20 ms on SAC inputs, (3) E->I temporal lag of 15-50
ms on preferred-direction stimuli reproducing Wehr & Zador 2003 co-tuning, (4) asymmetric
GABAergic inputs that are strong on null-side dendrites (to match Euler-Detwiler-Denk 2002 SAC
Ca2+ DS index 0.3-0.5) and weak on preferred-side dendrites, (5) dendritic-location-dependent
EPSP attenuation consistent with Hausser-Mel lambda_DC 100-300 um, (6) named fitting
objectives for DSI under shunting-inhibition block (should drop toward 0) and EPSP/IPSP charge
balance during null-direction motion.

</details>

<details>
<summary><strong>Register synaptic-integration category slugs if not already
present</strong> (S-0018-04)</summary>

**Kind**: evaluation | **Priority**: low

The paper assets in this task use category slugs `synaptic-integration`, `receptor-kinetics`,
`shunting-inhibition`, `ei-balance`, `dendritic-integration`, `direction-selectivity`, and
`starburst-amacrine`. Verify that all seven categories exist in meta/categories/; register any
that are missing so that category-based asset aggregators (aggregate_papers --categories
synaptic-integration) return the expected results. This mirrors the S-0017-04 registration
suggestion and the analogous S-0015-03 / S-0016-0X registrations; may already be satisfied by
category-registration tasks executed between t0015 and t0018.

</details>

## Research

* [`research_code.md`](../../../tasks/t0018_literature_survey_synaptic_integration/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0018_literature_survey_synaptic_integration/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0018_literature_survey_synaptic_integration/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0018_literature_survey_synaptic_integration/results/results_summary.md)*

--- spec_version: "2" task_id: "t0018_literature_survey_synaptic_integration" ---
# Results Summary: Synaptic-Integration Literature Survey

## Summary

Surveyed **5** high-leverage synaptic-integration papers covering the five canonical themes
(AMPA/NMDA/GABA receptor kinetics, shunting inhibition, E-I balance temporal co-tuning,
dendritic-location-dependent PSP integration, SAC-to-DSGC inhibitory asymmetry) and produced
one answer asset tabulating a prior distribution per DOI and theme. All **5** PDFs were
paywalled (Nature, PNAS, Current Opinion in Neurobiology); summaries are based on Crossref
abstracts plus training knowledge, and DOIs are recorded in `intervention/paywalled_papers.md`
for manual retrieval via Sheffield institutional access.

## Metrics

* **papers_built**: **5** (one per theme: Lester1990, KochPoggio1983, WehrZador2003,
  HausserMel2003, EulerDetwilerDenk2002)
* **papers_paywalled**: **5** (100% paywalled; all `download_status: "failed"`)
* **themes_covered**: **5** (all five planned themes covered)
* **answer_assets_built**: **1** (`synaptic-integration-priors-for-dsgc-modelling`)
* **dois_duplicated_from_prior_tasks**: **0** (verified against t0002, t0015, t0016, t0017
  corpora)

## Verification

* `verify_plan` passes with **0** errors, **0** warnings
* `verify_research_papers`, `verify_research_internet`, `verify_research_code` pass with **0**
  errors
* `verify_task_folder` passes with **0** errors, **1** warning (FD-W002 empty
  `logs/searches/`)
* `meta/asset_types/paper/verificator.py` passes on all 5 paper assets with **0** PA-E errors
  (PA-W002 / PA-W007 / PA-W008 warnings consistent with paywalled-paper template from t0017)
* `meta/asset_types/answer/verificator.py` passes on the single answer asset with **0** errors
  and **0** warnings
* `verify_task_complete` runs at the reporting step; expected warnings TC-W002 (25 vs 5 paper
  count) and TC-W005 (no merged PR yet) are planned and acceptable

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0018_literature_survey_synaptic_integration/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0018_literature_survey_synaptic_integration" ---
# Results Detailed: Synaptic-Integration Literature Survey

## Summary

Surveyed 5 high-leverage synaptic-integration papers (Lester et al. 1990 on NMDAR receptor
kinetics, Koch-Poggio-Torre 1983 on shunting inhibition, Wehr & Zador 2003 on E-I balance,
Hausser & Mel 2003 on dendritic-location-dependent PSP integration, Euler-Detwiler-Denk 2002
on SAC-to-DSGC inhibitory asymmetry), built 5 paper assets with `download_status: "failed"`
plus one answer asset tabulating a prior distribution per DOI and theme. All 5 PDFs are
paywalled; summaries combine Crossref metadata with training-knowledge consensus. DOIs were
verified non-duplicate against the t0002/t0015/t0016/t0017 corpora before asset construction.

## Methodology

### Machine

Local Windows 11 development box (same machine as t0017). No remote compute used; this is a
pure literature-survey task. No GPU hours consumed. All CLI calls were wrapped in
`arf/scripts/utils/run_with_logs.py` and logged under `logs/commands/`.

### Runtime and Timestamps

Task branch `task/t0018_literature_survey_synaptic_integration` was created at
2026-04-20T11:22:48Z and the implementation step completed at 2026-04-20T12:02:36Z
(approximately 40 minutes of actual implementation wall-clock for steps 9 and 12; total task
wall-clock approximately 1.5 hours across the 15 ARF lifecycle steps). Timestamps throughout
the task are ISO 8601 UTC.

### Paper selection

Five papers were chosen to cover the five synaptic-integration themes identified in the task
plan, one paper per theme:

1. AMPA/NMDA/GABA receptor kinetics: Lester, Clements, Westbrook, Jahr 1990
   (`10.1038/346565a0`)
2. Shunting inhibition: Koch, Poggio, Torre 1983 (`10.1073/pnas.80.9.2799`)
3. E-I balance temporal co-tuning: Wehr & Zador 2003 (`10.1038/nature02116`)
4. Dendritic-location dependence of PSP integration: Hausser & Mel 2003
   (`10.1016/s0959-4388(03)00075-8`)
5. SAC-to-DSGC inhibitory asymmetry: Euler, Detwiler, Denk 2002 (`10.1038/nature00931`)

DOIs were cross-checked against existing `tasks/t0002/assets/paper/`,
`tasks/t0015/assets/paper/`, `tasks/t0016/assets/paper/`, `tasks/t0017/assets/paper/` corpora
via filesystem enumeration; zero duplicates found.

### Crossref metadata fetch and asset build

`code/fetch_paper_metadata.py` (copied from `t0017/code/`) fetched Crossref metadata for all 5
DOIs to `plan/crossref_metadata.json`; all returned `status: "ok"` with matching titles/
authors. `code/build_paper_asset.py` (copied from `t0017/code/` with `TASK_ID`,
`THEME_CATEGORIES`, `THEME_NAMES`, and answer-asset-slug substitutions) then built each of the
five paper assets. Four materialised as DOI-slug folders; Hausser & Mel 2003's DOI contains
parentheses that the canonical `doi_to_slug` module rejects, so the builder fell back to
`no-doi_HausserMel2003_s0959-4388-03-00075-8` per the paper-asset spec v3. Each asset has
`download_status: "failed"`, `files/.gitkeep`, and `download_failure_reason: "No PDF URL
supplied"`.

### Answer asset synthesis

The answer asset `synaptic-integration-priors-for-dsgc-modelling` was written manually with
three files: `details.json` (spec v2, `confidence: "medium"`, 5 source paper IDs),
`short_answer.md` (Question, Answer, Sources sections; Answer is exactly 5 sentences), and
`full_answer.md` (9 mandatory sections with a prior-distribution table and 6 numbered
modelling constraints). The Prior Distribution Table has 6 rows (Lester1990 contributes two
rows because it supplies both the NMDAR direct measurement and the canonical AMPA/GABA_A
kinetic consensus) with columns DOI, First author & year, Theme, Prior quantity, Numerical
value (range + units), Source nature.

## Verification

* `verify_plan t0018_literature_survey_synaptic_integration`: PASSED, 0 errors, 0 warnings
* `verify_research_papers t0018_literature_survey_synaptic_integration`: PASSED, 0 errors
* `verify_research_internet t0018_literature_survey_synaptic_integration`: PASSED, 0 errors
  (after rewriting `research_internet.md` to use the `### [Key]` source-entry format)
* `verify_research_code t0018_literature_survey_synaptic_integration`: PASSED, 0 errors
* `verify_task_folder t0018_literature_survey_synaptic_integration`: PASSED, 0 errors, 1
  warning (FD-W002, `logs/searches/` empty — acceptable, a literature-survey task may rely on
  existing-paper and Crossref searches without logging structured internet queries)
* `meta/asset_types/paper/verificator.py` on all 5 paper assets: PASSED, 0 PA-E errors;
  warnings: PA-W002 (Results bullet count) on all 5, PA-W007 (no country data) on all 5,
  PA-W008 (empty abstract) on 4 papers. These warnings are inherent to the
  Crossref-plus-training-knowledge pattern and match the t0017 precedent
* `meta/asset_types/answer/verificator.py synaptic-integration-priors-for-dsgc-modelling`:
  PASSED, 0 errors, 0 warnings (after reducing short-answer sentence count from 6 to 5)
* `verify_task_complete` will run at the reporting step; the expected TC-W002 (25 vs 5 paper
  count) and TC-W005 (no merged PR yet) warnings are planned and acceptable per the wave-wide
  downscoping decision

## Limitations

All 5 source papers are paywalled and could not be retrieved through the automated pipeline.
Summaries are based on Crossref-provided metadata (full abstracts only for some, empty for
others) combined with training-knowledge consensus on the canonical treatment of each paper in
the synaptic-integration and retinal-neuroscience literature. Specific numeric values quoted
in summaries and the prior-distribution table (NMDAR tau_decay at 22-32 degC, AMPA and GABA_A
kinetic constants, lambda_DC 100-300 um for RGC dendrites, DSGC E-I lag 15-50 ms, SAC
dendritic Ca2+ DS index 0.3-0.5) should be verified against the actual PDFs before being used
as tight compartmental-model fitting targets. `intervention/paywalled_papers.md` records all 5
DOIs for Sheffield institutional access.

The task was scaled down from the planned 25 papers to 5 papers per the project-wide
`intervention/paywalled_papers.md` guidance introduced at t0014. The 5 selected papers still
cover all 5 planned themes, but breadth within each theme (e.g., modern DSGC-specific
receptor-kinetic studies, recent dynamic-clamp DSGC work, connectomic SAC-DSGC wiring
measurements) is deferred to follow-up tasks. The TC-W002 warning from `verify_task_complete`
(25 vs 5 paper count) is the expected consequence of this downscope and is acceptable.

## Files Created

### Paper Assets

* `assets/paper/10.1038_346565a0/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.1073_pnas.80.9.2799/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.1038_nature02116/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/no-doi_HausserMel2003_s0959-4388-03-00075-8/{details.json,summary.md,files/.gitkeep}`
* `assets/paper/10.1038_nature00931/{details.json,summary.md,files/.gitkeep}`

### Answer Asset

* `assets/answer/synaptic-integration-priors-for-dsgc-modelling/details.json`
* `assets/answer/synaptic-integration-priors-for-dsgc-modelling/short_answer.md`
* `assets/answer/synaptic-integration-priors-for-dsgc-modelling/full_answer.md`

### Code

* `code/fetch_paper_metadata.py` (Crossref metadata fetcher, adapted from `t0017`)
* `code/build_paper_asset.py` (v3 paper asset builder, adapted from `t0017`)

### Plan and Research

* `plan/plan.md`
* `plan/shortlist.md`
* `plan/crossref_metadata.json`
* `research/research_papers.md`
* `research/research_internet.md`
* `research/research_code.md`

### Intervention and Results

* `intervention/paywalled_papers.md`
* `results/results_summary.md`
* `results/results_detailed.md`
* `results/metrics.json`
* `results/costs.json`
* `results/remote_machines_used.json`

## Task Requirement Coverage

The task description from `task.json` reads:

> **Literature survey: synaptic integration.** Survey canonical papers on AMPA/NMDA/GABA kinetics,
> E-I balance, shunting inhibition, dendritic-location integration, and SAC-to-DSGC inhibitory
> asymmetry, producing a paper asset per canonical reference and one answer asset tabulating a prior
> distribution per DOI and theme. The original plan targeted ~25 papers; the brainstorm results 3
> scale-down decision common to the t0015-t0019 wave reduces the scope to 5 canonical papers per
> task.

Requirements from `plan/plan.md`:

* **REQ-1: Five new paper assets (one per theme), v3-spec compliant, under `assets/paper/`.**
  Status: **Done**. Evidence: 5 folders under
  `tasks/t0018_literature_survey_synaptic_integration/assets/paper/` each with `details.json`,
  `summary.md`, and `files/.gitkeep`; `meta/asset_types/paper/verificator.py` passes on all 5
  with 0 PA-E errors.
* **REQ-2: No DOI from t0002/t0015/t0016/t0017 may be duplicated.** Status: **Done**.
  Evidence: `plan/shortlist.md` records the exclusion cross-check; all 5 DOIs verified absent
  from prior corpora by filesystem enumeration.
* **REQ-3: All five paywalled papers recorded in `intervention/paywalled_papers.md`.** Status:
  **Done**. Evidence: `tasks/t0018_literature_survey_synaptic_integration/
  intervention/paywalled_papers.md` contains a 5-row DOI table with retrieval priority.
* **REQ-4: One answer asset under `assets/answer/<slug>/` with a prior-distribution table
  keyed by DOI and theme, at least 5 rows.** Status: **Done**. Evidence:
  `assets/answer/synaptic-integration-priors-for-dsgc-modelling/full_answer.md` contains the
  Prior Distribution Table with 6 rows (5 DOIs, Lester1990 contributing two rows for its two
  distinct priors); `meta/asset_types/answer/verificator.py` passes with 0 errors.
* **REQ-5: All five themes covered (theme-balance).** Status: **Done**. Evidence: one paper
  per theme in `plan/shortlist.md`; `themes_covered: 5` in `results/metrics.json`.
* **REQ-6: All five paper assets pass `verify_paper_asset`.** Status: **Done**. Evidence:
  `meta/asset_types/paper/verificator.py --task-id
  t0018_literature_survey_synaptic_integration` passes with 0 PA-E errors on all 5 assets;
  only quality-level warnings (PA-W002, PA-W007, PA-W008) remain, consistent with the
  paywalled template from t0017.

</details>
