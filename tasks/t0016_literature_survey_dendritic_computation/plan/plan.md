---
spec_version: "2"
task_id: "t0016_literature_survey_dendritic_computation"
date_completed: "2026-04-20"
status: "complete"
---
# Plan: Literature survey: dendritic computation beyond DSGCs

## Objective

Deliver a category-targeted literature survey of ~25 papers on dendritic computation beyond the
DSGC-specific t0002 corpus, covering NMDA spikes, Na+/Ca2+ dendritic spikes, plateau potentials,
branch-level nonlinearities, sublinear-to-supralinear integration regimes, and active-vs-passive
compartmental modelling, and to synthesise one answer asset indicating which mechanisms plausibly
transfer to DSGC dendrites. "Done" means: at least 20 paper assets pass `verify_paper_asset.py`, one
answer asset passes `verify_answer_asset.py` and addresses DSGC transferability, and no DOI collides
with the t0002 corpus.

## Task Requirement Checklist

The operative task request from `task.json` and `task_description.md`:

```text
Task name: Literature survey: dendritic computation beyond DSGCs
Short description: Survey ~25 papers on dendritic spikes, NMDA nonlinearities, and
active-vs-passive integration outside DSGC-specific work.

Scope (from task_description.md):
1. NMDA spikes - thresholds, amplitudes, distance-dependence, supralinear integration.
2. Na+ and Ca2+ dendritic spikes - backpropagation, forward propagation, local spikes.
3. Plateau potentials - in-vivo evidence, role in coincidence detection, duration scaling.
4. Branch-level nonlinearities - independent subunits, clustered-vs-distributed input summation.
5. Sublinear-to-supralinear integration regimes - what controls the transition, which conditions
   make dendrites behave passively in practice.
6. Active-vs-passive modelling comparisons - cortical, cerebellar, hippocampal studies that built
   matched active and passive compartmental models and quantified the difference.

Exclusion: do not re-add any DOI already present in the t0002 corpus. Duplicates discovered mid
task must be dropped and the exclusion recorded in the task log.

Expected Outputs:
* ~25 paper assets under assets/paper/ (v3 spec compliant), some possibly with
  download_status: "failed".
* One answer asset under assets/answer/ synthesising the six themes and flagging mechanisms most
  plausible for DSGC dendrites.
* intervention/paywalled_papers.md listing DOIs requiring manual retrieval.

Verification Criteria:
* At least 20 paper assets pass verify_paper_asset.py.
* The answer asset passes verify_answer_asset.py and explicitly addresses transferability to DSGC
  dendrites.
* No paper in this task's assets/paper/ shares a DOI with the t0002 corpus.
```

Decomposed requirements:

* **REQ-1**: Download ~25 paper assets targeting the six themes. Evidence: 25 folders under
  `assets/paper/` each with `details.json` + `summary.md` + `files/*`. Covered by Step 2 and Step 3.
* **REQ-2**: Paper assets must be spec_version 3 compliant and pass `verify_paper_asset.py`.
  Evidence: batch verificator report shows zero errors. Covered by Step 4.
* **REQ-3**: At least 20 of those paper assets must have `download_status: "success"` so the
  verifier can validate full structure. Evidence: `download_status` counts in
  `results/metrics.json`. Covered by Step 3.
* **REQ-4**: Paywalled papers must be recorded as `download_status: "failed"` with a reason, and
  DOIs listed in `intervention/paywalled_papers.md`. Evidence: intervention file exists and matches
  the failed-status set. Covered by Step 3 and Step 5.
* **REQ-5**: No DOI in this task's `assets/paper/` may appear in the 20 excluded t0002 DOIs.
  Evidence: `code/check_doi_overlap.py` exits cleanly. Covered by Step 6.
* **REQ-6**: Write one answer asset `dendritic-computation-motifs-for-dsgc-direction-selectivity`
  that synthesises the six themes and flags which mechanisms plausibly transfer to DSGC dendrites,
  with caveats. Evidence: answer folder with `details.json`, `short_answer.md`, `full_answer.md`.
  Covered by Step 7.
* **REQ-7**: The answer asset must pass `verify_answer_asset.py`. Evidence: verificator reports no
  errors. Covered by Step 8.
* **REQ-8**: The answer must explicitly address DSGC transferability (and caveats about
  anatomical/biophysical differences). Evidence: dedicated section in `full_answer.md` titled
  "Transferability to DSGC dendrites". Covered by Step 7.

## Approach

Execute a six-theme paper acquisition pipeline driven by the 25 target DOIs already enumerated in
`research/research_internet.md`, followed by answer synthesis that integrates the 25 new papers with
the 10 dendritic-computation-relevant papers already cited from the t0002 corpus (Oesch2005,
Schachter2010, PolegPolsky2016, Branco2010, Koren2017, Jain2020, Hanson2019, ElQuessny2021,
Vaney2012, Carnevale1997 - see `research/research_papers.md`). The download phase uses the project's
paper-download workflow: DOI -> metadata lookup (Crossref/Semantic Scholar for landing page,
abstract, authors, year) -> PDF download attempt via publisher URL -> v3 `details.json` -> ~800-1200
word `summary.md` matching the Oesch2005 template from t0002. Paywalled DOIs
(Nature/Science/Neuron/Nat Neurosci titles - expected ~10-15 of 25) take the abstract-based Overview
path per paper spec and are logged in `intervention/paywalled_papers.md`.

Key research findings embedded from `research/research_papers.md`:

* The DSGC-specific dendritic quantities are anchored in Oesch2005 (DSI ~0.7 spike vs ~0.1 PSP,
  spikelet ~7 mV, threshold ~-49 mV) and PolegPolsky2016 (NMDA sublinear->supralinear transition
  depends on coincidence and distance).
* Branco2010 is the canonical extra-retinal evidence that dendritic sequences encode direction.
* Cross-cell-type evidence covers NMDA spikes (Schiller2000, Polsky2004, Branco2011, Major2013a),
  Na+/Ca2+ spikes (Larkum1999, Stuart1994, Magee1998), plateau potentials (Gambino2014, Bittner2017,
  Takahashi2016, Milstein2015), branch-level integration (Losonczy2006, Poirazi2003a/b, Jadi2014),
  sublinear/supralinear regimes (Abrahamsson2012, VervaekeE2012, TranVanMinh2016, Hoffman1997,
  Gasparini2004), and active-vs-passive modelling (Spruston2008, LondonHausser2005, Hay2011,
  Larkum2009a, Stuart1998).

Alternative considered and rejected: fully automated bibliometric harvesting (pull everything citing
Oesch2005). Rejected because the 20-DOI exclusion list would yield duplicates, the target list is
already enumerated and cross-checked against t0002, and bibliometric harvesting returns many
citation-graph papers that do not address the six themes. The targeted approach keeps the survey
focused and the answer synthesis actionable.

Task types: `literature-survey` from `meta/task_types/`. Planning Guidelines for this type (from
`aggregate_task_types`) emphasise fixed step sequence (research -> planning -> implementation ->
results), no remote compute, and paper + answer as the only expected asset kinds. This plan follows
that guidance exactly.

## Cost Estimation

Total estimated cost: **$0**. All paper downloads go to publicly indexed PDFs or open-access landing
pages - no paid API required. LLM tokens for summary writing are provided by the execute-task agent
itself. Paywalled papers do not trigger payment: they get the failed-download treatment and are
logged to `intervention/paywalled_papers.md`. The project budget gate noted in `task_description.md`
(the $1 bump set in t0014) leaves ample headroom because no external paid service is invoked.
Comparison against `project/budget.json`: project budget is preserved; zero incremental spend
expected.

## Step by Step

1. **[CRITICAL] Create paper-asset folder scaffolding.** For each of the 25 target DOIs listed in
   `research/research_internet.md` (DOI slugs are produced by
   `uv run python -m arf.scripts.utils.doi_to_slug <doi>`), create
   `assets/paper/<doi_slug>/files/.gitkeep`. Expected output: 25 folders with `.gitkeep`. Satisfies
   REQ-1.

2. **[CRITICAL] Download PDFs where publicly available.** For each target DOI, attempt to fetch the
   publisher PDF. If the HTTP response is 200 and returns a PDF (or an open-access HTML page
   convertible to PDF), save to `assets/paper/<doi_slug>/files/<first_author>_<year>_<slug>.pdf`. If
   fetch fails with 403/paywall/timeout, record the DOI in a local list for Step 3. Satisfies REQ-1,
   REQ-3.

3. **[CRITICAL] Write `details.json` and `summary.md` per paper.** For every DOI: (a) write
   `assets/paper/<doi_slug>/details.json` per `meta/asset_types/paper/specification.md` with
   `spec_version: "3"`, `download_status` = `"success"` or `"failed"`, non-null
   `download_failure_reason` when failed,
   `added_by_task = "t0016_literature_survey_dendritic_computation"`, `date_added = "2026-04-20"`.
   (b) write `assets/paper/<doi_slug>/summary.md` following the Oesch2005 template at
   `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/summary.md`;
   each summary has the 9 mandatory sections and targets 800-1200 words. Abstract-based overview
   path permitted when `download_status` is `"failed"`. Satisfies REQ-1, REQ-3, REQ-4.

4. **Run per-paper verificator.** Execute
   `uv run python -m arf.scripts.verificators.verify_paper_asset t0016_literature_survey_dendritic_computation`.
   Expected: zero PA-E### errors across all 25 assets. Fix any errors reported; warnings (PA-W###)
   may be noted. Satisfies REQ-2.

5. **Write paywall intervention file.** Write `intervention/paywalled_papers.md` listing each failed
   DOI with a human-readable reason. At minimum this file needs a title, a 2-sentence intro, and a
   bullet list of the failed DOIs and the publisher that blocked them. Satisfies REQ-4.

6. **Verify no DOI collisions with t0002.** Create `code/check_doi_overlap.py` (a simple script that
   loads the 20 t0002 DOIs from
   `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/*/details.json` and
   compares against the new task's DOIs; exits non-zero on overlap). Run it and confirm exit code 0.
   Satisfies REQ-5.

7. **[CRITICAL] Write the answer asset.** Create
   `assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/` with:
   * `details.json` (`spec_version: "2"`, answer_id matching folder, question text: "Which
     dendritic-computation motifs observed in cortical, hippocampal, and cerebellar neurons
     plausibly transfer to DSGC dendrites, and what are the biophysical caveats?")
   * `short_answer.md` (<=200 words, with YAML frontmatter)
   * `full_answer.md` synthesising the 25 new papers plus the 10 cited t0002 papers. Must contain a
     dedicated section "Transferability to DSGC dendrites" that discusses each of the six themes
     with anatomical/biophysical caveats (e.g., DSGC dendrites are ~150 um and unipolar, unlike L5
     pyramidal apical trunks). Use the t0002 answer asset at
     `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/answer/how-does-dsgc-literature-structure-the-five-research-questions/`
     as the layout template. Satisfies REQ-6, REQ-8.

8. **Run answer verificator.** Execute
   `uv run python -m arf.scripts.verificators.verify_answer_asset t0016_literature_survey_dendritic_computation`.
   Expected: zero errors. Satisfies REQ-7.

## Remote Machines

None required. All work is text synthesis and PDF download from publicly addressable URLs. No GPU,
no paid API.

## Assets Needed

Input assets consumed (read-only):

* The 10 dendritic-relevant paper assets in
  `t0002_literature_survey_dsgc_compartmental_models/assets/paper/` (Oesch2005, Schachter2010,
  PolegPolsky2016, Branco2010, Koren2017, Jain2020, Hanson2019, ElQuessny2021, Vaney2012,
  Carnevale1997).
* The two answer-asset precedents (t0002 and t0003) as layout templates.
* `tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/` - cited by name
  only.
* `tasks/t0004_generate_target_tuning_curve/assets/dataset/target-tuning-curve/` - cited by name
  only.
* `meta/asset_types/paper/specification.md` and `meta/asset_types/answer/specification.md`.

## Expected Assets

Output assets produced (must match `task.json` `expected_assets`):

* **25 paper assets** under `assets/paper/<doi_slug>/` (`spec_version: "3"`), covering the 25 DOIs
  enumerated in `research/research_internet.md`. Some (estimated 10-15) will have
  `download_status: "failed"` because of Nature/Science/Neuron paywalls; they still carry
  `details.json` and an abstract-based `summary.md`.
* **1 answer asset** under
  `assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/`
  (`spec_version: "2"`), comprising `details.json`, `short_answer.md` (<=200 words), and
  `full_answer.md`.
* **1 intervention file** `intervention/paywalled_papers.md` listing paywalled DOIs.

## Time Estimation

* Research: complete (steps 4-6 already done).
* Implementation (step 9): ~3-4 hours wall-clock for 25 papers * ~8 minutes each (metadata lookup,
  PDF fetch, `details.json`, `summary.md`) plus ~45 minutes for the answer asset.
* Validation (verificators): ~5 minutes.
* Results and reporting: ~30 minutes.
* Total new wall-clock: ~4-5 hours.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Paywall block rate exceeds 60% | Medium | Blocks REQ-3 (min 20 full-success assets) | Substitute failing Nature/Science DOIs with open-access alternatives from eLife, PLOS, PNAS, Frontiers already shortlisted in `research/research_internet.md` follow-ups. |
| DOI slug collision with t0002 discovered mid-task | Low | Duplicate asset violates REQ-5 | Re-run `code/check_doi_overlap.py` after each paper download; on hit, drop the DOI and record in the step log. |
| Crossref/publisher rate limits | Medium | Delays | Sequential downloads with 2 s sleep between fetches; retry once on 429/5xx before marking failed. |
| Summary writing drifts from the 9 mandatory sections | Medium | PA-E009 errors | Use the Oesch2005 template literally; run verificator per-paper before batching, not only at the end. |
| Answer asset misses DSGC-transferability caveats | Low | Fails REQ-8 | Template the answer with a named section "Transferability to DSGC dendrites" that enumerates each of the six themes with a caveat bullet. |
| Network outage during download phase | Low | Delays | The asset scaffolding (step 1) is independent of download; retry downloads idempotently. |

## Verification Criteria

* **File existence**: Running
  `ls -d tasks/t0016_literature_survey_dendritic_computation/assets/paper/*/` returns 25
  directories. Running
  `ls tasks/t0016_literature_survey_dendritic_computation/assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/`
  lists `details.json`, `short_answer.md`, `full_answer.md`.
* **Per-paper verificator**:
  `uv run python -m arf.scripts.verificators.verify_paper_asset t0016_literature_survey_dendritic_computation`
  returns exit code 0 with zero PA-E### errors (REQ-2).
* **Answer verificator**:
  `uv run python -m arf.scripts.verificators.verify_answer_asset t0016_literature_survey_dendritic_computation`
  returns exit code 0 (REQ-7).
* **DOI overlap check**:
  `uv run python tasks/t0016_literature_survey_dendritic_computation/code/check_doi_overlap.py`
  returns exit code 0 (REQ-5).
* **At least 20 full-success assets**: `jq '.download_status' details.json` across all 25 folders
  yields at least 20 "success" values, confirming REQ-3.
* **DSGC transferability section**:
  `grep -E "^## +Transferability to DSGC dendrites" assets/answer/dendritic-computation-motifs-for-dsgc-direction-selectivity/full_answer.md`
  returns exactly one line (REQ-8).
* **Intervention file**:
  `test -f intervention/paywalled_papers.md && test -s intervention/paywalled_papers.md` succeeds
  when at least one paywalled DOI is recorded (REQ-4).
