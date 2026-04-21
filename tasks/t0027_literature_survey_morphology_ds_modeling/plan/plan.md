---
spec_version: "2"
task_id: "t0027_literature_survey_morphology_ds_modeling"
date_completed: "2026-04-21"
status: "complete"
---
# Plan: Literature Survey on Morphology Effects in Direction-Selectivity Modeling

## Objective

Extend the project's morphology-and-direction-selectivity (DS) baseline corpus from 5 to 17-25
papers, write a nine-section `summary.md` for each new paper following the paper-asset spec v3, and
synthesise one answer asset that maps morphology variables to DS mechanisms and identifies gaps
worth testing on the t0022 / t0024 modeling testbeds. "Done" means: 12-20 new paper assets exist and
pass `verify_paper`, one answer asset cites all baseline + new papers by paper_id and passes
`verify_answer`, and `results_detailed.md` synthesises the corpus along the four required taxonomy
sections.

## Task Requirement Checklist

The operative task request from `tasks/t0027_.../task_description.md`:

```text
Survey the internet (Google Scholar, PubMed, bioRxiv, ModelDB, arXiv, Web of Science via Sheffield
access if needed) for papers that BUILD computational, biophysical, or theoretical models linking
neuronal morphology to direction selectivity. Primary focus is retinal DSGCs (ON, OFF, ON-OFF
subtypes) and starburst amacrine cells (SACs); secondary focus is other DS neurons (cortical V1/MT,
fly lobula plate, vestibular nuclei) where morphology is treated as a manipulated variable.

Inclusion criteria:
1. The paper builds a model — compartmental, cable-theory, or abstract NN with explicit morphology.
2. Morphology is a manipulated or causally-relevant variable.
3. The model produces or analyses direction selectivity as an outcome.

Already-covered baseline (5 papers — DO NOT re-download):
Schachter2010 (10.1371_journal.pcbi.1000899), Jain2020 (10.7554_eLife.52949),
Morrie2018 (10.1016_j.cub.2018.03.001), PolegPolsky2026 (10.1038_s41467-026-70288-4),
deRosenroll2026 (10.1016_j.celrep.2025.116833).

Budget: 12-20 new papers, push to 25 if novel mechanisms keep appearing. Stop on diminishing
returns. Per-paper cost is zero (no paid API; PDFs via open access or Sheffield SSO).

Deliverables: ~12-20 paper assets; 1 answer asset answering "What variables of neuronal morphology
have been shown by computational modeling to affect direction selectivity, by what mechanisms, and
what gaps remain?"; results_detailed.md with summary table, morphology-variable taxonomy, mechanism
taxonomy, gaps & contradictions, recommendations; results_summary.md (2-3 paragraphs).
```

Concrete requirements extracted from the task text:

* **REQ-1** — Add 12-20 new paper assets (target the upper end if novel mechanisms are still
  appearing; stop earlier on diminishing returns; max 25). Each asset must follow paper-asset spec
  v3 with `details.json` + nine-section `summary.md` + `files/` (or `.gitkeep` if download failed).
  *Satisfied by*: Step 4-7 (paper download and asset creation). *Evidence*: count of subfolders
  under `assets/paper/` ≥ 12, all pass `verify_paper`.

* **REQ-2** — Do NOT re-download the 5 baseline papers (Schachter2010, Jain2020, Morrie2018,
  PolegPolsky2026, deRosenroll2026). Cite them by paper_id from their existing locations in t0002,
  t0010, t0013. *Satisfied by*: Step 4 (dedup pass) and Step 8 (synthesis answer). *Evidence*: no
  duplicate folders for the five baseline DOIs in `assets/paper/`.

* **REQ-3** — Mark each new paper with the most specific subset of categories
  (direction-selectivity, compartmental-modeling, dendritic-computation, retinal-ganglion-cell).
  *Satisfied by*: Step 5 (per-paper details.json categories). *Evidence*: `categories` field in each
  `details.json`.

* **REQ-4** — Flag borderline cases: SAC papers (flag "SAC, not DSGC"), passive-cable papers (flag
  "passive cable, geometry-only"), invertebrate papers (flag organism). *Satisfied by*: Step 5 (mark
  in `summary.md` Overview section) and Step 8 (taxonomy table column). *Evidence*: flag column in
  the synthesis summary table.

* **REQ-5** — Write one answer asset at
  `assets/answer/morphology-direction-selectivity-modeling-synthesis/` answering "What variables of
  neuronal morphology have been shown by computational modeling to affect direction selectivity, by
  what mechanisms, and what gaps remain?" with citations to every paper used as evidence (baseline +
  new) by paper_id. *Satisfied by*: Step 8. *Evidence*: `verify_answer` passes; cited paper_id list
  ≥ 17.

* **REQ-6** — Produce `results_detailed.md` with five sections: (a) summary table of every included
  paper (paper_id, first-author year, morphology variable, DS outcome, model type, organism, cell
  type), (b) morphology-variable taxonomy, (c) mechanism taxonomy, (d) gaps and contradictions, (e)
  3-5 prioritised morphology-sweep recommendations for the t0022 / t0024 testbeds. *Satisfied by*:
  orchestrator Phase 5 (results step). *Evidence*: file exists with all five subsections, embedded
  in `results_detailed.md`.

* **REQ-7** — Produce `results_summary.md` (2-3 paragraphs): how many papers found, which morphology
  variables have strongest evidence, what the field disagrees on, what to sweep first. *Satisfied
  by*: orchestrator Phase 5. *Evidence*: file exists, ≤ 3 paragraphs, headline metrics match
  `results_detailed.md`.

* **REQ-8** — Flag PDF-retrieval blockers as intervention files (Cell Press, Elsevier,
  Springer-Nature, Wiley paywalls). *Satisfied by*: Step 6 (intervention handling). *Evidence*: any
  blocked PDFs trigger `intervention/<slug>.md`; `details.json` `download_status: "failed"` with
  non-null `download_failure_reason`.

* **REQ-9** — No remote compute, no paid API, runs entirely on local Windows workstation. *Satisfied
  by*: Cost Estimation, Remote Machines sections (both = $0 / none). *Evidence*: empty
  `remote_machines_used.json`, `costs.json` total = 0.

## Approach

This is a literature-survey + answer-question task. The implementation follows three phases: **(1)
candidate selection** from the 20 internet-discovered papers documented in
`research/research_internet.md`, **(2) paper-asset construction** for ≥ 12 of those candidates
(highest-priority five flagged: Ezra-Tsur2021, Stincic2023, Gruntman2018, Haag2018, Anderson1999),
and **(3) synthesis answer + results** that integrate the new papers with the 10 corpus papers
already cited in `research/research_papers.md`.

The research stage already did the hard discovery work. `research_papers.md` cites 10 corpus papers
across five mechanism topics (electrotonic compartmentalisation, asymmetric SAC inhibition, active
dendritic conductances, cable theory, dense SAC tiling). `research_internet.md` adds 20 new
candidates (11 retinal, 5 invertebrate, 3 cortical, 1 cable-theory tool) covering all five
research-stage gaps. The implementation phase therefore reduces to applying the inclusion criteria
to those 20 candidates, downloading PDFs, and writing structured `summary.md` files.

**Code reuse.** Copy `tasks/t0018_.../code/fetch_paper_metadata.py` and
`tasks/t0018_.../code/build_paper_asset.py` into `tasks/t0027/code/` (flagged in
`research/research_code.md` as the project's canonical paper-asset builder). Adapt only the
input-list (CSV/JSON of candidate DOIs) and the output directory.

**Alternatives considered.** Manually writing every `details.json` would skip the t0018 utilities
and is rejected because it produces inconsistent metadata (missing ORCID, ISO country codes, etc.)
and bypasses the verificator-aligned schema the t0018 builder enforces. Skipping the answer-asset
synthesis and only producing `results_detailed.md` is rejected because the task explicitly lists the
answer asset as REQ-5 with `expected_assets.answer = 1`.

**Task types.** `literature-survey` + `answer-question`. Planning Guidelines for these types
emphasise (a) clear inclusion criteria captured in `details.json` per paper, (b) explicit citation
graph in the answer asset, (c) gaps section in `results_detailed.md`. The plan satisfies all three.

## Cost Estimation

* **API calls**: $0 — paper metadata fetched via free OpenAlex / CrossRef / Semantic Scholar APIs;
  no paid LLM calls (summaries written by the implementation agent in-context).
* **Remote compute**: $0 — runs entirely on local Windows workstation.
* **PDF retrieval**: $0 — open-access PDFs via DOI resolution; paywalled PDFs (Cell Press, Elsevier,
  Springer-Nature, Wiley) via Sheffield institutional SSO at no marginal cost.
* **Total**: **$0**. Project budget remaining (per `aggregate_costs` at task start): well above the
  per-task default; this task does not move the needle.

## Step by Step

### Milestone 1: Candidate selection and code setup

1. **Copy paper-asset utilities.** Copy
   `tasks/t0018_paper_asset_quality_audit/code/fetch_paper_metadata.py` (~78 lines) and
   `tasks/t0018_paper_asset_quality_audit/code/build_paper_asset.py` (~829 lines) into
   `tasks/t0027/code/`. Adjust `INPUT_DOIS_PATH` and `OUTPUT_PAPERS_DIR` constants in `paths.py` to
   point at the t0027 input list and `tasks/t0027/assets/paper/`. *Expected*: two files compile
   under `uv run mypy -p tasks.t0027_literature_survey_morphology_ds_modeling.code`. Satisfies
   REQ-1, REQ-2 infrastructure.

2. **Build the candidate DOI list.** Create `code/candidate_dois.json` listing the 20 papers from
   `research/research_internet.md` Discovered Papers section, each entry with
   `{"doi": ..., "citation_key": ..., "category_hint": ..., "priority": int}`. Mark the 5
   highest-priority entries (Ezra-Tsur2021, Stincic2023, Gruntman2018, Haag2018, Anderson1999) as
   `priority: 1`; the remaining 15 as `priority: 2`. *Expected*: file exists, parseable JSON, 20
   entries. Satisfies REQ-1 source list.

3. **Dedup against the 5 baseline papers.** Run a one-line check that none of the 20 candidate DOIs
   match `10.1371/journal.pcbi.1000899`, `10.7554/eLife.52949`, `10.1016/j.cub.2018.03.001`,
   `10.1038/s41467-026-70288-4`, `10.1016/j.celrep.2025.116833`. *Expected*: zero matches. Satisfies
   REQ-2.

### Milestone 2: Paper-asset creation (priority-1 batch)

4. **[CRITICAL] Build priority-1 paper assets.** Run
   `uv run python -m tasks.t0027_literature_survey_morphology_ds_modeling.code.build_paper_asset --priority 1`.
   This calls the t0018 builder for each of the 5 priority-1 entries. For each: fetch metadata from
   OpenAlex/CrossRef → resolve PDF URL → download PDF (or mark `download_status: "failed"` with
   reason) → emit `details.json` → emit `summary.md` skeleton with all nine mandatory sections.
   *Expected*: 5 new subfolders under `assets/paper/`, each passing `verify_paper` (errors only —
   Summary section will warn until Step 5 fills it). Satisfies REQ-1, REQ-3, REQ-8.

5. **Write priority-1 summaries.** For each of the 5 priority-1 papers, the implementation agent
   reads the downloaded PDF and writes the `summary.md` Overview, Architecture/Methods, Results,
   Innovations, Datasets, Main Ideas, Summary sections per paper-asset spec v3. Each section meets
   the minimum word count (Overview ≥ 100, Methods ≥ 150, Results ≥ 5 quantitative bullets, Main
   Ideas ≥ 3 bullets, Summary 4 paragraphs ≥ 200 words). Mark borderline cases per REQ-4 in the
   Overview opening sentence ("This is a SAC paper, not a DSGC paper..."). *Expected*:
   `verify_paper` PASSES with 0 errors and 0 warnings on all 5 papers. Satisfies REQ-1, REQ-3,
   REQ-4.

### Milestone 3: Paper-asset creation (priority-2 batch with stop criterion)

6. **Build and summarise priority-2 papers in batches of 5.** Repeat steps 4-5 for the priority-2
   entries in batches of 5. After each batch, the implementation agent reviews the new papers
   against the 5 mechanism topics already covered (electrotonic compartmentalisation, asymmetric SAC
   inhibition, active dendritic conductances, cable theory, dense SAC tiling). **Stop condition**:
   if a full batch of 5 papers adds zero new mechanism categories AND zero new morphology variables
   to the taxonomy, stop adding papers. **Continue condition**: if any paper in the batch flags a
   novel mechanism or variable, queue another batch up to a hard ceiling of 25 total new papers.
   *Expected*: 7-15 additional paper assets, all passing `verify_paper`. Satisfies REQ-1, REQ-3,
   REQ-4, REQ-8. **Validation gate**: after the first batch of 5, before queueing more, the
   implementation agent inspects two random `summary.md` files end-to-end and confirms they are not
   skeletal. If either is, halt and re-write before continuing.

7. **Handle PDF-retrieval blockers.** For any paper where Step 4 set `download_status: "failed"`,
   create `intervention/paper_<paper_id>_blocked.md` with: paper title, DOI, attempted URL, failure
   reason (Cell Press SSO required / Elsevier 403 / etc.), and the suggested fix (Sheffield VPN,
   manual download, etc.). The summary still gets written from the paper's public abstract per
   paper-asset spec v3. *Expected*: one intervention file per blocked PDF (likely 0-3 given the
   publisher mix). Satisfies REQ-8.

### Milestone 4: Synthesis answer asset

8. **[CRITICAL] Write the synthesis answer asset.** Create
   `assets/answer/morphology-direction-selectivity-modeling-synthesis/details.json` and `answer.md`
   per `meta/asset_types/answer/specification.md`. The answer.md must:
   * State the question verbatim as the document title.
   * Have the `## Answer` section organise findings by **morphology variable** (dendritic length,
     branch order, diameter, asymmetry, isotropic-vs-anisotropic, input-on-dendrite layout, dense
     tiling), each subsection citing supporting papers by `[paper_id]`.
   * Have the `## Mechanism` section group by **causal mechanism** (electrotonic
     compartmentalisation, dendritic spike thresholding, NMDA-Mg gating, delay lines, coincidence
     detection, asymmetric SAC inhibition).
   * Have the `## Gaps` section identify under-explored variables and contradictions.
   * Cite every baseline paper (Schachter2010, Jain2020, Morrie2018, PolegPolsky2026,
     deRosenroll2026) plus every new paper by `paper_id`. *Expected*: `verify_answer` passes;
     `details.json` `cited_paper_ids` field lists 17-30 unique paper_ids. Satisfies REQ-5.

## Remote Machines

None required. The task runs entirely on the local Windows workstation. Paper PDF downloads use
local HTTP requests (no GPU). Summary writing happens in the implementation agent's context (no paid
API).

## Assets Needed

* **5 baseline papers** — already in the project at `tasks/t0002/.../`, `tasks/t0010/.../`, and
  `tasks/t0013/.../`. Cite by paper_id only; do not copy.
* **3 directly-relevant prior answer assets** — t0002 five-RQ synthesis, t0015 cable-theory answer,
  t0016 dendritic-computation motifs (per `research/research_code.md`). Cite as evidence in the
  synthesis answer.
* **t0018 paper-asset utilities** — `fetch_paper_metadata.py`, `build_paper_asset.py`. Copy into
  `tasks/t0027/code/`.
* **External**: open-access PDFs via DOI; Sheffield institutional SSO for paywalled journals.

## Expected Assets

Matches `task.json` `expected_assets`:

* **paper × 12-20** (target 15) — new paper assets at
  `assets/paper/<paper_id>/{details.json, summary.md, files/}`, each covering a model that
  manipulates morphology and reports a DS outcome.
* **answer × 1** — `assets/answer/morphology-direction-selectivity-modeling-synthesis/` answering
  the morphology-and-DS synthesis question with citations to baseline + new papers.

## Time Estimation

* Research (already done): 4-5 hours, complete.
* Implementation Milestone 1 (code setup): 0.5 hours.
* Implementation Milestone 2 (priority-1 batch, 5 papers): 2-3 hours (PDF download + summary
  writing).
* Implementation Milestone 3 (priority-2 batches): 3-5 hours depending on stop point.
* Implementation Milestone 4 (synthesis answer): 1-1.5 hours.
* Analysis + reporting (orchestrator): 1 hour.
* **Total wall-clock from start of implementation to PR merge**: 8-11 hours.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Cell Press / Elsevier paywalled PDFs cannot be retrieved even via Sheffield SSO | Medium | One paper per blocker has only abstract-based summary | Per REQ-8: write intervention file, mark `download_status: "failed"`, write summary from abstract only. Spec v3 explicitly allows this. |
| OpenAlex/CrossRef metadata is incomplete (missing ORCID, country, journal) | Medium | `verify_paper` warnings (PA-W007, PA-W009, PA-W010) | Warnings do not block. Acceptable trade-off vs. manual entry. |
| A candidate paper turns out not to manipulate morphology (fails inclusion criterion 2) on PDF read | Medium | Wasted effort; paper must be excluded | Implementation agent rejects in Step 5 before writing summary; logs decision; queues a replacement candidate from the priority-2 list. |
| Stop criterion in Step 6 fires too early, undershooting the 12-paper floor | Low | < 12 new papers, REQ-1 not satisfied | Hard floor at 12 in Step 6 — never stop before 12 priority-1+priority-2 papers are built, regardless of mechanism diversity. |
| Synthesis answer omits citations to baseline papers (regression bug) | Low | REQ-5 not satisfied | Step 8 explicitly lists the 5 baseline paper_ids that must appear in `cited_paper_ids`. Verification criterion checks this. |
| Implementation agent writes skeletal `summary.md` files that pass verificator on word counts but lack substance | Low-Medium | Wasted assets; downstream synthesis poor | Validation gate in Step 6: agent must inspect 2 random summaries end-to-end after the first batch and re-write before continuing. |

## Verification Criteria

* **VC-1 (REQ-1)**: Run
  `ls tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/ | wc -l` and confirm count
  ≥ 12 (target 15, ceiling 25).
* **VC-2 (REQ-1, REQ-3, REQ-4, REQ-8)**: Run
  `uv run python -u -m arf.scripts.verificators.verify_paper_assets t0027_literature_survey_morphology_ds_modeling`
  and confirm 0 errors. Warnings allowed (PA-W007, PA-W009, PA-W010 are common for non-OA
  publishers).
* **VC-3 (REQ-2)**: Run
  `ls tasks/t0027_.../assets/paper/ | grep -E "10.1371_journal.pcbi.1000899|10.7554_eLife.52949|10.1016_j.cub.2018.03.001|10.1038_s41467-026-70288-4|10.1016_j.celrep.2025.116833"`
  and confirm zero matches.
* **VC-4 (REQ-5)**: Run
  `uv run python -u -m arf.scripts.verificators.verify_answer_assets t0027_literature_survey_morphology_ds_modeling`
  and confirm 0 errors. The answer asset's `details.json` `cited_paper_ids` must include all five
  baseline DOIs as paper_ids.
* **VC-5 (REQ-6)**: Confirm `tasks/t0027_.../results/results_detailed.md` exists and contains five
  `## ` sections matching: "Summary Table", "Morphology Variable Taxonomy", "Mechanism Taxonomy",
  "Gaps and Contradictions", "Recommendations".
* **VC-6 (REQ-7)**: Confirm `tasks/t0027_.../results/results_summary.md` exists and is between 150
  and 600 words (2-3 paragraphs).
* **VC-7 (REQ-9)**: Confirm `tasks/t0027_.../results/costs.json` total = 0.0 and
  `remote_machines_used.json` is `[]`.
