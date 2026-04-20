---
spec_version: "2"
task_id: "t0019_literature_survey_voltage_gated_channels"
date_completed: "2026-04-20"
status: "complete"
---
# Plan: Voltage-Gated Channel Literature Survey for DSGC Modelling

## Objective

Identify five canonical, widely-cited peer-reviewed papers that together supply quantitative priors
for the DSGC compartmental model on (1) Nav subunit localisation at the RGC axon initial segment
(AIS), (2) Kv subunit expression at the AIS, (3) RGC-specific HH-family kinetic rate functions, (4)
Nav1.6 vs Nav1.2 subunit co-expression kinetics, and (5) AIS Nav conductance density. "Done" means:
five v3 paper assets exist under `assets/paper/` (all with `download_status: "failed"` because the
papers are paywalled, built from Crossref metadata plus training-knowledge summaries), all five pass
`verify_paper_asset`; one answer asset under `assets/answer/` tabulates a Nav/Kv combination per DOI
and theme and passes `verify_answer_asset`; all five DOIs are recorded in
`intervention/paywalled_papers.md`; no DOI from the t0002/t0015/t0016/t0017/t0018 corpora is
duplicated.

## Task Requirement Checklist

The task is defined by `task.json` (category `voltage-gated-channels`, source suggestion
`S-0014-05`):

> **Literature survey: voltage-gated channels.** Survey canonical papers on Nav1.x and Kv subunit
> localisation, RGC HH kinetic models, subunit co-expression, and AIS conductance densities,
> producing a paper asset per canonical reference and one answer asset tabulating Nav/Kv
> combinations by DOI and theme. The original plan targeted ~25 papers; the brainstorm results 3
> scale-down decision common to the t0015-t0019 wave reduces the scope to 5 canonical papers per
> task.

**Requirements extracted:**

* **REQ-1**: Five new paper assets, one per theme, as v3-spec compliant folders under
  `assets/paper/`. Satisfied by Step 2. Evidence: `verify_paper_asset` passes for each and the five
  DOIs are listed in the answer asset.
* **REQ-2**: No DOI from t0002/t0015/t0016/t0017/t0018 may be duplicated. Satisfied by Step 1
  (exclusion check). Evidence: the five DOIs were verified absent from those corpora via filesystem
  enumeration of `tasks/*/assets/paper/` folders.
* **REQ-3**: All five paywalled papers recorded in `intervention/paywalled_papers.md` with DOI,
  title, and Crossref-only availability note. Satisfied by Step 3.
* **REQ-4**: One answer asset under `assets/answer/<slug>/` with a Nav/Kv combinations table keyed
  by DOI and theme, at least five rows. Satisfied by Step 4. Evidence: `verify_answer_asset` passes
  and `full_answer.md` contains a Nav/Kv combinations table.
* **REQ-5**: All five themes must be covered (theme-balance). Satisfied by Step 1.
* **REQ-6**: All five paper assets pass `verify_paper_asset`. Satisfied by Step 5.

## Approach

Pure literature work — no new code beyond copying and adjusting two existing scripts from `t0018`,
no remote compute. The approach follows the `t0015`/`t0016`/`t0017`/`t0018` template: paywalled-
only papers, built from Crossref metadata plus training-knowledge summaries with
download-status-failed, recorded in `intervention/paywalled_papers.md`.

The answer asset reuses the structure of `t0018`'s answer folder: `details.json` v2 +
`short_answer.md` (3 short sections) + `full_answer.md` (9 sections) with the Nav/Kv combinations
table in `full_answer.md`.

**Task types** (from `meta/task_types/`): `literature-survey`. The scale-down-to-5 decision is
consistent with the wave of t0015-t0019 literature tasks, all of which land at roughly 5-10 papers.

**Alternatives considered**: (a) Attempting to download paywalled PDFs via alternate sources —
rejected; the Crossref-abstract-plus-training-data pattern has been validated four times over
(t0015-t0018) and sidesteps the access problem entirely. (b) Producing fewer than five papers —
rejected because each of the five themes is load-bearing for the DSGC model's voltage-gated
channels.

## Cost Estimation

* Crossref / OpenAlex / PubMed / Semantic Scholar APIs: free, **$0**.
* No publisher access fees attempted; paywalled papers recorded as failures, **$0**.
* No LLM API calls outside standard agent orchestration (covered by subscription), **$0**.
* Remote compute: none, **$0**.
* **Total: $0**.

## Step by Step

1. **Assemble the shortlist.** Write the five DOIs from `research/research_internet.md` "Discovered
   Papers" section to `plan/shortlist.md` with their themes. Verify no DOI collides with
   t0002/t0015/t0016/t0017/t0018. Satisfies REQ-1, REQ-2, REQ-5.

2. **Fetch Crossref metadata.** Copy `fetch_paper_metadata.py` from `t0018/code/` into this task's
   `code/` folder; adjust `SHORTLIST` to the five DOIs; run it to cache Crossref metadata (title,
   authors, institutions, abstract when available, publication date) in
   `plan/crossref_metadata.json`.

3. **Build paper assets.** Copy `build_paper_asset.py` from `t0018/code/` into `code/`; adjust
   `TASK_ID`, `THEME_CATEGORIES`, and `THEME_NAMES` so each DOI gets `voltage-gated-channels` as
   primary plus one secondary theme tag; run it to materialise five `assets/paper/<slug>/` folders
   with v3 `details.json`, 9-section `summary.md`, and `files/.gitkeep` (paywalled path). Satisfies
   REQ-1.

4. **Record paywalled papers.** Write `intervention/paywalled_papers.md` listing all five DOIs with
   title, venue, and Crossref abstract availability note. Satisfies REQ-3.

5. **Produce the answer asset.** Create `assets/answer/nav-kv-combinations-for-dsgc-modelling/` with
   `details.json` v2 (spec), `short_answer.md` (3 sections), and `full_answer.md` (9 sections)
   containing the Nav/Kv combinations table with columns
   `DOI | First author & year | Theme | Prior quantity | Numerical value (range + units) | Source nature`.
   Run `verify_answer_asset` and fix errors. Satisfies REQ-4.

6. **Verify all paper assets.** Run
   `uv run python -m arf.scripts.verificators.verify_paper_asset t0019_literature_survey_voltage_gated_channels --all`
   and confirm five passing with zero `PA-E*` errors. Satisfies REQ-6.

7. **Metrics and results.** Compute `papers_built` (5), `papers_paywalled` (5), `themes_covered` (5)
   for `results/metrics.json`. No charts needed.

## Remote Machines

None required. Work is local: Crossref API queries plus local file writes.

## Assets Needed

* `research/research_internet.md` (this task) — source of the five candidate DOIs.
* `research/research_papers.md` (this task) — exclusion context.
* `tasks/t0018_literature_survey_synaptic_integration/code/fetch_paper_metadata.py` — template to
  copy.
* `tasks/t0018_literature_survey_synaptic_integration/code/build_paper_asset.py` — template to
  copy.
* `meta/asset_types/paper/specification.md` v3 — paper asset format.
* `meta/asset_types/answer/specification.md` v2 — answer asset format.

## Expected Assets

* **paper** (x 5): One `assets/paper/<doi_slug>/` folder per shortlisted DOI, v3-spec compliant, all
  with `download_status: "failed"`. Matches the scale-down-to-5 decision (`task.json` still lists
  `expected_assets.paper: 25` but this is a planned TC-W002 warning, not an error).
* **answer** (x 1): `assets/answer/nav-kv-combinations-for-dsgc-modelling/` tabulating a Nav/Kv
  combination per DOI and theme. Matches `expected_assets.answer: 1`.

## Time Estimation

* Research (done): ~3 hours (steps 4-6 completed).
* Implementation Step 1 (shortlist + crossref_metadata preflight): 20 minutes.
* Implementation Step 2 (copy fetch script + run): 15 minutes.
* Implementation Step 3 (copy build script + run): 15 minutes.
* Implementation Step 4 (paywalled_papers.md): 10 minutes.
* Implementation Step 5 (answer asset): 1 hour.
* Implementation Step 6 (verification sweep): 10 minutes.
* Implementation Step 7 (metrics): 10 minutes.
* **Total implementation wall-clock**: ~2.3 hours.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| A candidate DOI turns out to duplicate an existing corpus DOI | Low | Need to source a replacement | Cross-check every DOI against the filesystem-enumerated exclusion set before `build_paper_asset.py` runs |
| Crossref returns no abstract for a classical paper | Medium | Summary section must rely solely on training-data recall | Proceed; mark the summary as "abstract unavailable from Crossref" and cite training-knowledge nature explicitly |
| `verify_paper_asset` flags `PA-W001` word-count warnings on short abstracts | Medium | Warnings only, not errors | Accept; warnings do not block task completion |
| `verify_answer_asset` flags missing-section errors | Low | Answer fails verification | Reuse the t0018 answer asset structure verbatim; only adjust content |
| Pre-commit hooks modify log files after commit | Medium | Poststep "tree not clean" failure | Commit hook-modified logs immediately and rerun poststep, per the pattern validated in t0018 |

## Verification Criteria

* Run `verify_paper_asset t0019_literature_survey_voltage_gated_channels --all` with zero `PA-E*`
  errors on all five papers. Covers REQ-1, REQ-6.
* Confirm no DOI collision with t0002/t0015/t0016/t0017/t0018 by filesystem enumeration. Covers
  REQ-2.
* Confirm `intervention/paywalled_papers.md` exists and lists all five DOIs. Covers REQ-3.
* Run `verify_answer_asset t0019_literature_survey_voltage_gated_channels` with zero errors and
  confirm `full_answer.md` contains a Nav/Kv combinations table with at least 5 rows. Covers REQ-4.
* Confirm `results/metrics.json` has `papers_built == 5`, `papers_paywalled == 5`,
  `themes_covered == 5`. Covers REQ-5.
* Run `verify_task_complete t0019_literature_survey_voltage_gated_channels` with zero errors
  (TC-W002 and TC-W005 warnings acceptable). Required before opening the PR.
