---
spec_version: "2"
task_id: "t0015_literature_survey_cable_theory"
date_completed: "2026-04-20"
status: "complete"
---
# Plan: Literature Survey on Cable Theory and Dendritic Filtering

## Objective

Produce a cable-theory literature survey that broadens the project corpus beyond the 20 DSGC-focused
papers in `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/`. The task is
"done" when: (a) ~25 paper assets exist under this task's `assets/paper/` at spec-v3, (b) one
synthesis answer asset exists under `assets/answer/` mapping each paper to its project-relevant
cable-theory theme, (c) an `intervention/paywalled_papers.md` file lists any DOIs whose automatic
download failed, and (d) all verificators pass with no errors.

## Task Requirement Checklist

Operative task text (from `task.json` + `task_description.md`):

> **Name**: Literature survey: cable theory and dendritic filtering
>
> **Short description**: Survey ~25 category-relevant papers on cable theory and passive dendritic
> filtering to broaden the corpus beyond DSGC-specific models.
>
> **Scope**: Target ~25 category-relevant papers covering: (1) Rall-era foundations, (2) segment
> discretisation guidelines (d_lambda rule, spatial-frequency constraints on nseg), (3)
> branched-tree impedance (transfer impedance, voltage attenuation), (4) frequency-domain analyses
> (input impedance, synaptic-event filtering, chirp/ZAP), (5) transmission in thin dendrites (space
> constant, propagation failure, passive integration limits).
>
> **Exclusion**: do not re-add any DOI already present in the t0002 corpus.
>
> **Paywall policy**: papers behind institutional paywalls are recorded as
> `download_status: "failed"` and added to `intervention/paywalled_papers.md`.
>
> **Answer**: one answer asset synthesising the five themes and identifying cable-theory parameters
> most directly useful for downstream DSGC tasks.
>
> **Verification**: at least 20 paper assets pass `verify_paper_asset.py`; the answer asset passes
> `verify_answer_asset.py`; `intervention/paywalled_papers.md` exists with DOI list if any downloads
> failed; no paper in this task shares a DOI with the t0002 corpus.

Concrete requirements:

* **REQ-1** — Download ~25 paper assets covering cable theory, spec-v3 compliant, under
  `assets/paper/`. Evidence: folder count; each passes `verify_paper_asset.py`. Covered by steps
  3-7.
* **REQ-2** — Each paper must be tagged with at least one of the five themes (Rall-era
  foundations, segment discretisation, branched-tree impedance, frequency-domain analyses,
  thin-dendrite transmission) via appropriate category slugs. Evidence: `categories` field in each
  `details.json`. Covered by steps 3-7.
* **REQ-3** — No DOI in this task's corpus may appear in the t0002 corpus. Evidence: dedup check
  script output in the implementation step log. Covered by step 2 (dedup check) and step 8 (final
  audit).
* **REQ-4** — Paywalled papers: exactly one automatic download attempt per paper; on failure,
  create a paper asset with `download_status: "failed"`, non-null `download_failure_reason`, empty
  `files: []` plus `.gitkeep`, and append the DOI to `intervention/paywalled_papers.md`. No retries.
  Evidence: `intervention/paywalled_papers.md` exists; any failed asset has the three flags set.
  Covered by step 7.
* **REQ-5** — Produce one answer asset under `assets/answer/` synthesising the five themes and
  identifying the cable-theory parameters most directly useful for downstream DSGC tasks (L, tau_m,
  thin-dendrite propagation threshold, d_lambda reference frequency). Evidence: answer passes
  `verify_answer_asset.py`. Covered by step 9.
* **REQ-6** — The answer must map each of the ~25 papers to at least one theme and must state
  quantitative anchors (L ≈ 0.6-1.0, tau_m ≈ 10-30 ms, d_lambda @ 500-1000 Hz with threshold
  0.02). Evidence: full-answer content inspection in verification. Covered by step 9.
* **REQ-7** — At least 20 paper assets must pass `verify_paper_asset.py` (i.e., paywalled failures
  allowed to the extent that 20+ successes remain). Evidence: implementation step tally. Covered by
  step 10.
* **REQ-8** — All verificators for research, plan, assets, and task-level checks pass with no
  errors. Evidence: verificator exit codes in the reporting step. Covered by step 10.

There are no ambiguities requiring clarification — the task description is concrete and the five
themes are fully enumerated.

## Approach

The approach is a standard literature-survey workflow that reuses the paper-asset patterns from
t0002. The 25 candidate papers are already enumerated in `research/research_internet.md` "Discovered
Papers" section under the five themes. Each is downloaded via the `/add-paper` skill, which produces
a v3-compliant asset (`details.json` + `summary.md` + `files/`). Paywalled papers are recorded per
the policy in `task_description.md` with a single attempt, then moved on. Categories are drawn from
existing `meta/categories/` slugs (`cable-theory`, `compartmental-modeling`,
`dendritic-computation`, `retinal-ganglion-cell`, `voltage-gated-channels`, `synaptic-integration`,
`direction-selectivity`, `patch-clamp`) — no new categories are introduced.

After all papers are in place, one synthesis answer is produced. The answer follows the v2 answer
asset spec (`details.json` + `short_answer.md` + `full_answer.md`) and is structured around the five
themes with explicit quantitative anchors drawn from the literature: electrotonic length **L ≈
0.6-1.0** (bracketed by salamander DSGC L = 0.34 ± 0.13 and cat alpha-cell L ~ 1.0), membrane time
constant **tau_m ≈ 10-30 ms**, and **d_lambda = 0.02 at 500-1000 Hz** as the recommended segment
discretisation for spike-producing dendrites. Research findings that justify these anchors are
recorded in `research/research_internet.md` (32 cited sources) and `research/research_papers.md` (3
cable-theory-adjacent papers already in t0002).

**Alternative considered**: running a deeper corpus of 40-50 papers covering secondary topics
(active conductances, plateau potentials, backpropagation). Rejected because (a) active-dendrite
papers fall under t0018 not t0015, (b) the task explicitly caps at ~25 papers, and (c) the
five-theme framing is already comprehensive for the downstream calibration consumer ([t0009]).

**Task types**: `literature-survey` (as set in `task.json`). The literature-survey task-type
planning guideline is: do one internet search, shortlist candidates, add each via `/add-paper`,
write one synthesis answer — no simulation, no remote compute, no model training.

## Cost Estimation

$0. The task uses only the local `/add-paper` skill plus (Sci-Hub/DOI-resolver) free endpoints built
into the skill. No paid LLM API calls, no remote compute, no dataset purchase. Project budget
(`project/budget.json`) is $1.00 and the task will stay at $0.00 actual spend. This is recorded in
`results/costs.json` as `{"total": 0, "items": []}`.

## Step by Step

1. **Dedup pre-check.** Read the 20 DOIs from the t0002 corpus via
   `uv run python -m arf.scripts.aggregators.aggregate_papers --ids` (list folder names). Cross
   against the 25 candidate DOIs in `research/research_internet.md` "Discovered Papers" list.
   Confirm zero overlap. Record the two lists side-by-side in the step log. Satisfies REQ-3.

2. **Materialise the candidate list.** Write a plain-text candidate list to
   `code/paper_candidates.md` with one line per candidate: DOI (or `no-doi_` fallback), citation
   key, title, primary theme. This file is the driver for steps 3-7. Satisfies REQ-1 (planning).

3. **Download Rall-era foundations papers (~7 papers).** Invoke the `/add-paper` skill once per
   Rall-theme candidate from `code/paper_candidates.md`: Rall 1959, Rall 1962a, Rall 1962b, Rall
   1967, Rall-Rinzel 1973, Rinzel-Rall 1974, Goldstein-Rall 1974. Each attempt produces a folder
   under `assets/paper/<doi_slug>/`. For papers whose download fails, record per step 7. Category:
   `cable-theory`. Satisfies REQ-1, REQ-2.

4. **Download segment-discretisation papers (~3 papers).** Run `/add-paper` for Hines-Carnevale
   NEURON textbook/reference and two d_lambda-focused papers. Category: `compartmental-modeling`.
   Satisfies REQ-1, REQ-2.

5. **Download branched-tree impedance and frequency-domain papers (~8 papers).** Run `/add-paper`
   for Koch-Poggio 1982, Koch-Poggio-Torre 1983, Koch 1984, Holmes 1986, Major 1993,
   Mainen-Sejnowski 1996, Hutcheon-Yarom 2000, Magee-Cook 2000, Narayanan-Johnston 2007 (pick 8 from
   this list). Categories: `cable-theory`, `dendritic-computation`. Satisfies REQ-1, REQ-2.

6. **Download thin-dendrite transmission papers (~7 papers).** Run `/add-paper` for Zador 1995,
   Segev-Rall 1998, Taylor 2000, Oesch 2005, Velte-Masland 1999, Coleman-Miller 1989, Velte-Miller
   1995, Fohlmeister-Miller 1997, Fohlmeister 2010 (pick 7 from this list). Categories:
   `cable-theory`, `retinal-ganglion-cell`, `dendritic-computation`. Satisfies REQ-1, REQ-2.

7. **Record paywalled failures.** For each paper whose download returned
   `download_status: "failed"`, verify the asset has `files: []` + `files/.gitkeep`, non-null
   `download_failure_reason`, and append the DOI to `intervention/paywalled_papers.md` with a
   one-line reason. One attempt only — no retries. Satisfies REQ-4.

8. **Dedup post-check and asset-level verification.** For each paper folder under this task's
   `assets/paper/`, run `uv run python -m arf.scripts.verificators.verify_paper_asset <paper_id>`
   and record the result. Confirm zero DOI overlap with t0002. Satisfies REQ-3, REQ-7.

9. **Write the synthesis answer.** Create `assets/answer/cable-theory-for-dsgc/` with
   `details.json`, `short_answer.md`, `full_answer.md` following the answer v2 spec. The answer
   structure: one section per theme (1-5), each citing 3-7 of the newly downloaded papers and the
   three cable-theory-adjacent papers from t0002 (Hines 1997, Schachter 2010, Branco 2010). Include
   an explicit Quantitative Anchors subsection with L, tau_m, d_lambda, and thin-dendrite
   propagation threshold. Satisfies REQ-5, REQ-6.

10. **Final verification.** Run:
    * `uv run python -m arf.scripts.verificators.verify_paper_asset` for each paper asset.
    * `uv run python -m arf.scripts.verificators.verify_answer_asset cable-theory-for-dsgc`.
    * `uv run python -m arf.scripts.verificators.verify_task_prerequisites t0015_literature_survey_cable_theory`.
      Confirm at least 20 paper assets pass and the answer passes. Satisfies REQ-7, REQ-8.

**Validation gate**: before running step 3 (the first download batch), perform a single small-scale
validation by running `/add-paper` for just ONE candidate (Rall 1959). Inspect the resulting folder:
`details.json` parses, `summary.md` has all mandatory sections, and `files/` contains a PDF or
markdown file, OR `download_status: "failed"` is correctly recorded. If the test fails, halt and
debug before batching through the remaining 24.

## Remote Machines

None required. All work is local (internet search + DOI download via the `/add-paper` skill + local
markdown/JSON writing).

## Assets Needed

* **Input papers**: the 20 t0002 papers under
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/` are read only for the DOI
  exclusion list — no content re-use beyond citation.
* **Categories**: existing slugs under `meta/categories/` (`cable-theory`, `compartmental-modeling`,
  `dendritic-computation`, `retinal-ganglion-cell`, `voltage-gated-channels`,
  `synaptic-integration`, `direction-selectivity`, `patch-clamp`).
* **Research files**: `research/research_papers.md`, `research/research_internet.md`,
  `research/research_code.md` — already produced in earlier steps and read by the implementation
  subagent.

## Expected Assets

* **~25 paper assets** under `tasks/t0015_literature_survey_cable_theory/assets/paper/<doi_slug>/`,
  each v3-compliant (`details.json`, `summary.md`, `files/`). Some may have
  `download_status: "failed"` — target at least 20 successful downloads.
* **1 answer asset** under `assets/answer/cable-theory-for-dsgc/`, v2-compliant (`details.json`,
  `short_answer.md`, `full_answer.md`). Synthesises the five cable-theory themes and anchors the
  DSGC calibration parameters.

Matches `task.json` `expected_assets`: `{"paper": 25, "answer": 1}`.

## Time Estimation

* Research: done (~1.5 hours wall-clock across research_papers, research_internet, research_code).
* Planning: ~10 minutes (this document).
* Implementation (steps 1-10): ~3-4 hours for 25 download attempts + answer synthesis.
* Analysis + reporting: ~30 minutes.

Total remaining: ~4 hours wall-clock.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| More than 5 papers paywalled | Medium | REQ-7 threshold risk | Select additional open-access candidates from the secondary candidate pool in `research/research_internet.md`; accept up to 5 failures before triggering |
| `/add-paper` fails on a DOI (malformed metadata, journal redirect loop) | Low | Delay | Record as `download_status: "failed"` with `download_failure_reason: "add-paper skill error"`; do not retry |
| DOI overlap with t0002 discovered mid-task | Low | Drop paper | Remove the offending candidate; pull from secondary pool; log the dedup event |
| Answer asset verificator rejects structure | Low | Delay | Inspect the one prior answer asset ([t0013]) as a known-good reference; copy its field structure |
| Research anchors (L, tau_m, d_lambda) conflict across sources | Medium | Content delay | Report ranges not point estimates; cite the source of each range endpoint in the answer |

## Verification Criteria

* **File existence**: `ls tasks/t0015_literature_survey_cable_theory/assets/paper/ | wc -l` returns
  ≥ 20.
* **Paper asset verification**: for each subfolder under `assets/paper/`, run
  `uv run python -m arf.scripts.verificators.verify_paper_asset <paper_id>` — at least 20 must
  exit 0 (REQ-7).
* **Answer asset verification**:
  `uv run python -m arf.scripts.verificators.verify_answer_asset cable-theory-for-dsgc` exits 0
  (REQ-5, REQ-6).
* **Dedup audit**: run `uv run python -m arf.scripts.aggregators.aggregate_papers --format ids` —
  confirm no t0015 DOI matches a t0002 DOI (REQ-3).
* **Intervention file**:
  `test -f tasks/t0015_literature_survey_cable_theory/intervention/paywalled_papers.md` succeeds if
  any failed downloads exist (REQ-4). Empty or missing is acceptable only if zero failures.
* **Task completion**:
  `uv run python -m arf.scripts.verificators.verify_task_complete t0015_literature_survey_cable_theory`
  exits 0 (REQ-8).
