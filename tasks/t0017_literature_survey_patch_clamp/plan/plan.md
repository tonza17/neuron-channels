---
spec_version: "2"
task_id: "t0017_literature_survey_patch_clamp"
date_completed: "2026-04-20"
status: "complete"
---
# Plan: Patch-Clamp Literature Survey for DSGC Model Validation

## Objective

Survey approximately 25 category-relevant peer-reviewed papers on patch-clamp recordings of retinal
ganglion cells (especially DSGCs) that supply validation targets for the DSGC compartmental model.
"Done" means: at least 20 papers exist as v3 paper assets under `assets/paper/` and pass
`verify_paper_asset`; one answer asset under `assets/answer/` maps each paper's DOI to the
model-validation observable it provides (AP rate, EPSC/IPSC kinetics, null/preferred ratios, space-
clamp error bounds); paywalled failures are recorded in `intervention/paywalled_papers.md`; no DOI
from the 20-paper t0002 corpus is duplicated.

## Task Requirement Checklist

The task is defined by `tasks/t0017_literature_survey_patch_clamp/task_description.md`:

> **Literature survey: patch-clamp recordings of RGCs and DSGCs.** Target ~25 category-relevant
> papers covering (1) Somatic whole-cell recordings of RGCs — firing-rate statistics, spike-
> threshold distributions; (2) Voltage-clamp conductance dissections — separating AMPA/NMDA/GABA
> currents during DS responses; (3) Space-clamp error analyses — how much of published conductance
> asymmetry is real vs an artefact of imperfect voltage clamp in extended dendrites; (4) Spike-train
> tuning-curve measurements — angle-resolved AP rates and their variability; (5) In-vitro stimulus
> protocols — moving bars, drifting gratings, and spots used to probe DS. Do not re-add any DOI
> already present in the t0002 corpus. Run `/research-internet` per theme, invoke `/download-paper`
> per shortlisted paper (single attempt; paywalled papers go to `intervention/paywalled_papers.md`),
> and write one answer asset mapping each paper to its model-validation observable.

**Requirements extracted:**

* **REQ-1**: Download approximately 25 new paper assets via `/add-paper` across the five themes,
  each as a v3-spec paper asset. Satisfied by Step 2. Evidence: `aggregate_papers --ids <...>`
  returns all new DOIs; `verify_paper_asset` passes for each.
* **REQ-2**: No DOI from the 20-paper t0002 corpus may be duplicated. Satisfied by Step 1 (exclusion
  list) and Step 2 (DOI check before download). Evidence: the exclusion list is enforced inline and
  no duplicate folder exists under this task's `assets/paper/`.
* **REQ-3**: Paywalled failures recorded in `intervention/paywalled_papers.md` with DOI, title, and
  failure reason; at most one download attempt per paywalled paper. Satisfied by Step 3. Evidence:
  that file exists and references every `download_status: "failed"` paper asset.
* **REQ-4**: One answer asset under `assets/answer/<slug>/` mapping each paper DOI to a model-
  validation observable (AP rate, EPSC/IPSC kinetics, null/preferred ratios, space-clamp bounds)
  with at least five numerical rows. Satisfied by Step 4. Evidence: `verify_answer_asset` passes and
  `full_answer.md` contains a validation-target table.
* **REQ-5**: All five themes must be represented in the final paper set (theme-balance). Satisfied
  by Step 1 (theme allocation) and Step 2 (per-theme download). Evidence: the answer asset table
  tags each paper with its theme.
* **REQ-6**: At least 20 paper assets pass `verify_paper_asset.py`. Satisfied by Step 2 and Step 5.
  Evidence: the verification log shows >= 20 papers passing.

## Approach

The task is pure literature work — no new code, no remote compute. The approach follows the
`[t0002]` template: call `/add-paper` as a dedicated subagent per paper, using the ~25 DOIs
identified in `research/research_internet.md` "Discovered Papers" section. The five themes in
`task_description.md` map directly to the themes already categorized in `research_papers.md`, so
allocation is: 5 papers for whole-cell RGC recordings, 5 for voltage-clamp E/I dissection, 5 for
space-clamp error analyses, 5 for spike-train tuning, 5 for stimulus protocol design.

The answer asset reuses the structure of
`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/`:
`details.json` (v2) + `short_answer.md` (3-paragraph summary) + `full_answer.md` (the DOI ->
observable table plus per-theme synthesis). Numerical targets come from `[t0004]`'s GeneratorParams
(2 Hz baseline, 32 Hz peak, DSI 0.6-0.9) and from the papers themselves.

**Task types** (from `meta/task_types/`): `literature-survey`. This type's planning guideline is
"target 20-25 papers, allocate across sub-themes, expect 15-20% paywall failures, produce at least
one synthesis answer". The approach above follows this guideline directly.

**Alternatives considered**: (a) Manual download without the `/add-paper` skill — rejected because
`details.json` v3 and `summary.md` frontmatter are too error-prone to hand-produce reliably; the
skill wraps the `doi_to_slug` utility and enforces verificator compliance. (b) Skipping the answer
asset and only delivering papers — rejected because `task.json` `expected_assets.answer: 1` makes
the answer a hard requirement, and the DOI->observable mapping is the actionable output for
downstream model-fitting tasks.

## Cost Estimation

* OpenAlex / Semantic Scholar / Crossref / arXiv / PubMed Central: free APIs, **$0**.
* Publisher-hosted PDFs: free for open-access papers; paywalled papers generate
  `download_status: "failed"` entries rather than paid bypass, **$0**.
* No LLM API calls outside the standard agent orchestration (covered by the Anthropic subscription,
  not task-attributable), **$0**.
* Remote compute: none, **$0**.
* **Total: $0**. This is well within the project's remaining budget (see `project/budget.json`).

## Step by Step

1. **Assemble the shortlist.** Collate the ~25 DOIs from the "Discovered Papers" section of
   `research/research_internet.md`, tag each with its theme (1-5), and write the list to
   `plan/shortlist.md` as a numbered list `<index>. <DOI> [<theme>] — <citation>`. Cross-check
   against the exclusion list in `research/research_papers.md` and drop any t0002 duplicate. Aim for
   5 papers per theme; if a theme has fewer candidates, record the gap and accept it. Satisfies
   REQ-1, REQ-2, REQ-5.

2. **Download each paper via the `/add-paper` skill.** For each DOI in `plan/shortlist.md`, spawn
   one Agent subagent invoking `/add-paper` with that DOI and this task's ID. The skill creates
   `assets/paper/<doi_slug>/details.json`, `summary.md`, and `files/` per the v3 paper spec. Single
   download attempt; on failure the skill sets `download_status: "failed"` and leaves `files/` with
   only `.gitkeep`. Each paper is its own commit. Expected output: ~25 subfolders under
   `assets/paper/`, of which >= 20 have `download_status: "success"`. Satisfies REQ-1.

3. **Record paywalled failures.** After Step 2 completes, enumerate papers with
   `download_status: "failed"` and write `intervention/paywalled_papers.md` with one entry per
   failure: DOI, title, venue, failure reason, and whether a manual retrieval is requested. Format
   follows `tasks/t0002_literature_survey_dsgc_compartmental_models/intervention/` precedent.
   Satisfies REQ-3.

4. **Produce the answer asset.** Create `assets/answer/rgc-patch-clamp-validation-targets/` with
   `details.json` (v2), `short_answer.md` (3 paragraphs summarising the survey), and
   `full_answer.md` containing (a) a Markdown table with columns
   `DOI | First author & year | Species | Protocol | Observable | Numerical target (with units) | Theme`,
   one row per downloaded paper, and (b) a per-theme synthesis paragraph. Use the numerical targets
   `[t0004]` defines (2 Hz baseline, 32 Hz peak, DSI 0.6-0.9) to cross-check. Run
   `uv run python -m arf.scripts.verificators.verify_answer_asset t0017_literature_survey_patch_clamp`
   and fix errors. Expected output: answer asset passes verification, table has >= 5 rows with
   numerical values. Satisfies REQ-4.

5. **Verify all paper assets.** Run
   `uv run python -m arf.scripts.verificators.verify_paper_asset t0017_literature_survey_patch_clamp --all`
   and confirm >= 20 passing; fix any `PA-E*` errors by re-invoking `/add-paper` or editing
   metadata. Warnings `PA-W*` are logged in the step log but do not block. Satisfies REQ-6.

6. **Metrics and charts.** Compute three metrics for `results/metrics.json`: `papers_downloaded`
   (int), `papers_paywalled` (int), `themes_covered` (int, out of 5). No charts are needed —
   literature surveys produce counts, not curves. Write a short `papers_by_theme.svg` bar chart to
   `results/images/` if time permits (purely optional).

No step requires remote compute or paid APIs; no validation gate is needed beyond the verificator
runs. Steps 1-6 are idempotent — re-running `/add-paper` on an already-downloaded DOI is a no-op
(the skill detects existing folders).

## Remote Machines

None required. All work is local: API queries against open databases plus PDF downloads. No GPU, no
cloud compute.

## Assets Needed

* `research/research_internet.md` (this task) — source of the ~25 candidate DOIs.
* `research/research_papers.md` (this task) — exclusion list (20 t0002 DOIs).
* `meta/asset_types/paper/specification.md` v3 — paper asset format.
* `meta/asset_types/answer/specification.md` — answer asset format.
* `tasks/t0004_generate_target_tuning_curve/code/generate_target.py` `GeneratorParams` — numerical
  validation targets referenced in the answer.

## Expected Assets

* **paper** (x ~25): One `assets/paper/<doi_slug>/` folder per shortlisted DOI, v3-spec compliant.
  Matches `task.json` `expected_assets.paper: 25`. At least 20 must pass verification.
* **answer** (x 1): `assets/answer/rgc-patch-clamp-validation-targets/` mapping each paper DOI to
  its model-validation observable with at least five numerical rows. Matches `task.json`
  `expected_assets.answer: 1`.

## Time Estimation

* Research (done): ~6 hours (steps 4-6 already completed).
* Implementation Step 1 (shortlist): 15 minutes.
* Implementation Step 2 (25 paper downloads via subagents, serial): ~3 hours (approx. 7 min per
  paper including search, fetch, summarise, verify).
* Implementation Step 3 (paywalled intervention file): 15 minutes.
* Implementation Step 4 (answer asset): 1 hour.
* Implementation Step 5 (verification sweep): 15 minutes.
* Implementation Step 6 (metrics): 15 minutes.
* **Total implementation wall-clock**: ~5 hours.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Paywall rate exceeds 20% (>5 of 25 fail) | Medium | Fewer than 20 papers pass verification | Source replacements from `research_internet.md` follow-up queries until 20 success papers exist |
| A shortlisted DOI turns out to duplicate t0002 | Low | Wasted download and verificator PA-E011 | Cross-check every DOI against the exclusion list before calling `/add-paper` in Step 2 |
| A paper lacks an abstract or full text (PDF is image-only) | Medium | `summary.md` cannot meet PA-W001 500-word minimum | Use the abstract from OpenAlex/CrossRef metadata and note the limitation in summary.md; warning is acceptable |
| Answer asset table missing numerical values for non-quantitative papers | Low | REQ-4 violation | Default to "No numerical value reported; qualitative finding: ..." with a source-paragraph reference |
| `/add-paper` skill subagent fails transiently (API timeout) | Medium | One paper missing | Retry once per orchestrator rule 13; fall back to inline download by the orchestrator if the retry fails |
| OpenAlex/CrossRef rate limiting | Low | Delay | Standard polite pause between calls; no paid workaround |

## Verification Criteria

* Run
  `uv run python -m arf.scripts.verificators.verify_paper_asset t0017_literature_survey_patch_clamp --all`
  and confirm at least 20 papers with zero `PA-E*` errors. Covers REQ-1, REQ-6.
* Run
  `uv run python -m arf.scripts.aggregators.aggregate_papers --ids <doi_slug1> <doi_slug2> ... --format ids`
  with every shortlist DOI; output must list all of them and none of the 20 t0002 DOIs. Covers
  REQ-2.
* Confirm `tasks/t0017_literature_survey_patch_clamp/intervention/paywalled_papers.md` exists and
  every paper with `download_status: "failed"` appears in it (`grep -c` per DOI). Covers REQ-3.
* Run
  `uv run python -m arf.scripts.verificators.verify_answer_asset t0017_literature_survey_patch_clamp`
  and confirm zero errors; `full_answer.md` must contain a markdown table with at least 5
  numerical-value rows. Covers REQ-4.
* Confirm `results/metrics.json` contains `papers_downloaded >= 20`, `papers_paywalled <= 6`,
  `themes_covered == 5`. Covers REQ-5.
* Run
  `uv run python -m arf.scripts.verificators.verify_task_complete t0017_literature_survey_patch_clamp`
  and confirm zero errors before opening the PR.
