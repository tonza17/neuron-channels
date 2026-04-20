---
spec_version: "2"
task_id: "t0013_resolve_morphology_provenance"
date_completed: "2026-04-20"
status: "complete"
---
# Plan: Resolve dsgc-baseline-morphology Source-Paper Provenance

## Objective

Close the known provenance gap on the project's baseline DSGC morphology. The dataset asset
`dsgc-baseline-morphology` (registered by `t0005_download_dsgc_morphology`) currently has
`source_paper_id: null` because two Feller-lab 2018 papers are plausible sources for the
`141009_Pair1DSGC` reconstruction. This plan downloads both candidate papers as v3-compliant paper
assets, reads their Methods sections to identify which paper introduced the reconstruction, and
files a single correction asset that updates `dsgc-baseline-morphology.source_paper_id` (or flags
the gap as requiring human intervention). "Done" means: two paper assets pass `verify_paper_asset`,
one correction asset passes the corrections verificator, and the reasoning is auditable in
`results/results_detailed.md`.

## Task Requirement Checklist

Operative task text (from `task_description.md`):

```text
Resolve dsgc-baseline-morphology source-paper provenance.

Short description: Download both plausible Feller-lab 2018 source papers, read their Methods to
identify which introduced the 141009_Pair1DSGC reconstruction, and correct
dsgc-baseline-morphology source_paper_id.

Scope:
1. Download Morrie & Feller 2018 Neuron via /add-paper.
2. Download Murphy-Baum & Feller 2018 Current Biology via /add-paper.
3. Read both papers' Methods sections, looking specifically for: recording date 141009,
   Pair1DSGC / Pair 1 DSGC / paired recording language, and any explicit citation of the
   reconstruction or its NeuroMorpho deposit.
4. If one paper is unambiguously the source, file a correction setting source_paper_id to the
   winning paper's DOI-slug. Otherwise record both DOIs under candidate_source_paper_ids and
   open an intervention file.
5. Record the full reasoning in results/results_detailed.md.
```

Requirement decomposition:

* **REQ-1** — Register `10.1016/j.neuron.2018.05.028` (Morrie & Feller 2018 *Neuron*) as a v3 paper
  asset under `assets/paper/10.1016_j.neuron.2018.05.028/`. Satisfied by Step 1. Evidence:
  `verify_paper_asset` passes.
* **REQ-2** — Register `10.1016/j.cub.2018.03.001` (Murphy-Baum & Feller 2018 *Current Biology*) as
  a v3 paper asset under `assets/paper/10.1016_j.cub.2018.03.001/`. Satisfied by Step 2. Evidence:
  `verify_paper_asset` passes.
* **REQ-3** — Read both papers' Methods sections and search for `141009`, `Pair1DSGC`,
  `Pair 1 DSGC`, `paired recording`, and neighbouring date strings. Satisfied by Step 3. Evidence:
  exact quotes copied into `results/results_detailed.md`.
* **REQ-4** — Apply the pre-specified decision procedure (one-cites-only → that paper; both-cite →
  earlier publication; neither-cites → intervention). Satisfied by Step 4. Evidence: decision-tree
  rendering in `results/results_detailed.md`.
* **REQ-5** — Write exactly one correction file at
  `corrections/dataset_dsgc-baseline-morphology.json`, either setting `source_paper_id` to the
  winner's slug or populating `candidate_source_paper_ids` and opening an intervention file.
  Satisfied by Step 5. Evidence: `verify_correction_asset` passes.
* **REQ-6** — Record the full auditable reasoning — including both papers' quoted Methods evidence,
  the NeuroMorpho REST attribution, and the decision mapping — in `results/results_detailed.md`.
  Satisfied by the results step (post-implementation). Evidence: the detailed results file contains
  a `## Provenance Decision` section that cites Methods quotes from both papers.

Ambiguity: if one or both papers are paywalled, `download_status: "failed"` metadata-only assets are
permitted per the paper spec, and the Methods-based evidence must instead come from the abstract
plus any publicly available supplement. If neither paper can be inspected beyond the abstract, the
decision must fall through to the intervention branch (REQ-5 second option).

## Approach

The task is mechanical: two DOIs are pre-identified, a decision procedure is pre-specified, and a
single scalar field on one existing asset is the only thing being changed. No code is written. The
appropriate tooling is the existing `/add-paper` skill (handles PDF fetching, Methods extraction,
summary authoring, and verificator-passing asset structure) plus a hand-written correction JSON per
`arf/specifications/corrections_specification.md`.

Two aspects demand care. First, the decision procedure from `task_description.md` must be applied
verbatim — the temptation to privilege the NeuroMorpho REST attribution (which unambiguously names
Murphy-Baum & Feller 2018) must be resisted until the Methods sections are actually read, because
the task's purpose is to verify NeuroMorpho's claim, not inherit it. Second, both papers must be
registered even if one paper is immediately disqualified by its Methods, because the task's
`expected_assets` field requires `paper: 2`.

**Alternatives considered.** An alternative would be to treat the NeuroMorpho REST attribution
(`reference_doi: ["10.1016/j.cub.2018.03.001"]`) as decisive and skip the Methods read. Rejected
because: (a) the task description explicitly frames this as Methods-based verification; (b)
NeuroMorpho metadata occasionally points at a review or secondary reference rather than the original
experimental report; (c) independent verification is cheap once the PDFs are in hand.

**Task types.** `download-paper` (two papers to register) and `correction` (one dataset asset to
update). Both are declared in `task.json` `task_types`. The `download-paper` Planning Guideline
implies that `/add-paper` handles the heavy lifting; the `correction` guideline implies that
research-code should confirm the correction target (done — see `research/research_code.md`).

## Cost Estimation

* `/add-paper` × 2 — **$0**. `/add-paper` uses Anthropic API via the orchestrating Claude Code
  session; within-session calls do not charge additional service fees beyond the standard
  subscription and are not tracked against `project/budget.json` `available_services` (which is
  currently `[]`).
* Hand-written correction JSON, markdown, and verificator runs — **$0**.
* Remote compute — **$0**. None required.
* **Total: $0.00**, well under the project's `total_budget: $1.0` USD cap and the
  `per_task_default_limit: $1.0` per-task limit. The budget gate is bypassed automatically because
  neither declared task type has `has_external_costs: true`.

## Step by Step

1. **[CRITICAL] Register Morrie & Feller 2018 *Neuron* as a paper asset.** Spawn an `/add-paper`
   subagent with DOI `10.1016/j.neuron.2018.05.028`. Target folder
   `tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.neuron.2018.05.028/`. Expected
   output: `details.json`, `summary.md`, `files/` populated, passing `verify_paper_asset`. If
   download fails (paywall/captcha), the `/add-paper` skill falls back to a metadata-only asset with
   `download_status: "failed"` per v3 spec. Satisfies REQ-1.

2. **[CRITICAL] Register Murphy-Baum & Feller 2018 *Current Biology* as a paper asset.** Spawn a
   second `/add-paper` subagent with DOI `10.1016/j.cub.2018.03.001`. Target folder
   `tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/`. Expected
   output same as Step 1. Satisfies REQ-2.

3. **[CRITICAL] Extract Methods evidence.** For each downloaded paper, open the markdown conversion
   under `files/*.md` (or the PDF text layer if only a PDF was produced). Search for the tokens
   `141009`, `Pair1DSGC`, `Pair 1 DSGC`, `paired recording`, `paired SAC`, `Sema6`, and
   `October 9, 2014` / `Oct 9 2014`. Copy every matching paragraph into a scratch file
   `logs/steps/009_implementation/methods_evidence.md` with per-paper subheadings. Expected output:
   either at least one matching paragraph per paper, or a per-paper "no match" entry. Satisfies
   REQ-3.

4. **[CRITICAL] Apply the decision procedure.** Using the evidence from Step 3, evaluate:
   * If exactly one paper's Methods cites the reconstruction → that paper's DOI-slug is the winner.
   * If both cite it → choose the paper with the earlier publication date (`date_published` in
     `details.json`).
   * If neither cites it → write an intervention file at `intervention/provenance_ambiguity.md`
     requesting the researcher email the Feller lab. Record the decision and its justification
     (including exact-quote evidence) in `logs/steps/009_implementation/decision.md`. Satisfies
     REQ-4.

5. **[CRITICAL] Write the correction asset.** Create
   `corrections/dataset_dsgc-baseline-morphology.json` per the corrections spec. Structure:
   * If a winner was chosen — `action: "update"`, target dataset asset `dsgc-baseline-morphology`,
     `changes: {"source_paper_id": "<winner_slug>"}`, plus a `rationale` that cites the Methods
     quote used as evidence.
   * If ambiguous — `action: "update"`,
     `changes: {"candidate_source_paper_ids": ["10.1016_j.neuron.2018.05.028", "10.1016_j.cub.2018.03.001"]}`,
     plus a rationale linking to the intervention file. Run the correction verificator; expected
     output: passes with zero errors. Satisfies REQ-5.

Validation gates for Step 5: the trivial baseline to compare against is "no correction at all",
which would leave the asset permanently ambiguous. A failure condition here is "correction
verificator reports errors" — halt and debug before committing. No `--limit` flag applies because
this is not a batch operation.

The Step by Step ends here. Results, suggestions, and reporting steps are orchestrated outside this
plan.

## Remote Machines

**None required.** All work is local: two paper downloads (HTTP), one JSON file written by hand, and
verificator runs executed via `uv run`.

## Assets Needed

* **Dataset asset** `dsgc-baseline-morphology` from `t0005_download_dsgc_morphology` (read-only).
  Specifically: `details.json` to confirm the correction-target field and
  `logs/steps/009_implementation/neuromorpho_metadata.json` as corroborating evidence.
* **External web resources**: Elsevier-hosted PDFs for DOIs `10.1016/j.neuron.2018.05.028` and
  `10.1016/j.cub.2018.03.001`. Both papers are from Elsevier journals (*Neuron* and *Current
  Biology*).
* No library assets are required (none exist yet in the project).

## Expected Assets

* **Paper asset** `10.1016_j.neuron.2018.05.028` — Morrie & Feller 2018 *Neuron*; v3-compliant with
  `details.json`, `summary.md`, and `files/*.pdf` (and `.md` if markdown conversion succeeds).
* **Paper asset** `10.1016_j.cub.2018.03.001` — Murphy-Baum & Feller 2018 *Current Biology*; same
  shape.
* **Correction asset** `corrections/dataset_dsgc-baseline-morphology.json` — targets dataset
  `dsgc-baseline-morphology`, updates either `source_paper_id` (winner case) or records
  `candidate_source_paper_ids` (ambiguous case).

This matches `task.json` `expected_assets: {"paper": 2}`. The correction asset is counted separately
from paper assets and is not listed in `expected_assets`.

## Time Estimation

* Research (already done): ~15 min (completed in `research-code` step).
* Planning (this step): ~15 min.
* Implementation: ~30-60 min total — two `/add-paper` invocations (~15-20 min each including
  Methods-reading summaries) plus ~10 min for evidence extraction, decision, and correction writing.
* Results, suggestions, reporting: ~20 min combined (orchestrator phases).
* Wall-clock total for the full task: ~90-120 min.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Paper paywalled or fetch blocked (PDF not retrievable) | Medium | Methods quote unavailable; may force intervention branch | `/add-paper` v3 allows `download_status: "failed"` metadata-only assets. If both papers are inaccessible beyond the abstract, fall through to the intervention branch. If one is accessible and unambiguously cites the reconstruction, that is still sufficient. |
| Neither paper's Methods mentions `141009` / `Pair1DSGC` / paired recording | Low-Medium | Forces intervention branch (non-ideal outcome) | Accept the intervention. Draft a clear `intervention/provenance_ambiguity.md` summarising the evidence gap and proposing the researcher email the Feller lab. Do not silently pick either paper. |
| Both papers cite the recording but at different grains (one the session date, one the animal line) | Medium | Ambiguity in "cites the reconstruction" definition | Document the grain and apply the earlier-publication-date tie-breaker verbatim, as specified in `task_description.md`. Do not invent new tie-breakers. |
| DOI slug convention drift between `/add-paper` and the correction | Low | Correction points to a non-existent paper asset | After both papers are registered, check the actual folder names on disk before writing the correction's `source_paper_id` value. The canonical converter is `arf.scripts.utils.doi_to_slug`. |
| Pre-commit / verificator flags something unexpected | Low | Step delays | Fix the underlying issue rather than skipping hooks. The correction spec and paper spec are both stable; most likely cause is a typo. |

## Verification Criteria

* `uv run python -m arf.scripts.verificators.verify_paper_asset t0013_resolve_morphology_provenance --asset 10.1016_j.neuron.2018.05.028`
  — passes with 0 errors. Confirms REQ-1.
* `uv run python -m arf.scripts.verificators.verify_paper_asset t0013_resolve_morphology_provenance --asset 10.1016_j.cub.2018.03.001`
  — passes with 0 errors. Confirms REQ-2.
* `uv run python -m arf.scripts.verificators.verify_correction_asset t0013_resolve_morphology_provenance --asset dataset_dsgc-baseline-morphology`
  — passes with 0 errors. Confirms REQ-5.
* `ls tasks/t0013_resolve_morphology_provenance/assets/paper/` returns exactly the two expected
  folder names. Confirms asset-count requirement.
* `ls tasks/t0013_resolve_morphology_provenance/corrections/` returns exactly one correction file
  (`dataset_dsgc-baseline-morphology.json`). Confirms REQ-5 one-file constraint.
* `results/results_detailed.md` contains a `## Provenance Decision` section that quotes at least one
  matching paragraph from each paper's Methods (or explicitly records a no-match). Confirms REQ-3
  and REQ-6.
