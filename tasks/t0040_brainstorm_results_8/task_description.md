# Brainstorm Results Session 8

## Motivation

Eighth strategic brainstorming session, run on 2026-04-24 after the t0037–t0039 wave merged. The
researcher requested a cross-task audit of every test run so far against published data, with the
explicit goal of identifying discrepancies and designing corrections. The session produced a master
test table, a published-data comparison table (both saved under `results/`), and a prioritised list
of four follow-up tasks that target the discrepancies.

## Scope

* Review project state after the t0037–t0039 merges: 37 tasks completed, 1 `not_started` (t0031),
  1 `intervention_blocked` (t0023), 151 uncovered suggestions, $0.00 / $1.00 budget used.
* Build a master table summarising every simulation test we have run (13 tests across t0008, t0020,
  t0022, t0024, t0026, t0029, t0030, t0034, t0035, t0036, t0037, t0039).
* Build a published-data comparison table listing every quantitative claim from the
  `compare_literature.md` files and classify each as MATCH / PARTIAL / MISMATCH.
* Group the mismatches into discrepancy themes and propose root-cause corrections.
* Approve four tasks (t0041–t0044) that address the top-leverage discrepancies.
* Apply one suggestion rejection and four reprioritisations based on recent findings.

## Researcher Decisions

* **Four new tasks, all zero-cost local runs**:
  * **t0041** — L/lambda electrotonic-length collapse analysis of t0034 and t0035 data. Data
    analysis only, no simulation. Covers S-0035-01.
  * **t0042** — Fine-grained null-GABA ladder {3.5, 3.0, 2.5} nS on t0022 baseline diameter. Tests
    whether t0022 can reach DSI >= 0.5 below 4 nS without destabilising preferred direction.
  * **t0043** — Add Nav1.6 + Kv3 to AIS\_DISTAL and distal dendrites of t0022; restore NMDA at PD
    and ND BIPs; validate peak rate against t0004 envelope (40–80 Hz). Covers S-0019-03 (partial),
    S-0018-03 (partial), S-0022-02.
  * **t0044** — 7-diameter Schachter2010 re-test on the t0043 output substrate at GABA = 4 nS.
    Pass/fail on quadratic curvature sign. Covers S-0002-02.
* **Execution order**: t0041 and t0042 can run in parallel; t0043 can run in parallel with them;
  t0044 depends on t0043 completion.
* **Suggestion corrections**:
  * Reject S-0030-06 (vector-sum DSI as t0033 objective). Superseded by S-0034-07 (primary DSI on
    t0024).
  * Reprioritise S-0029-01, S-0029-02, S-0030-02, S-0010-01 from high to medium pending t0043 and
    t0044 outcomes.
* **Sheffield paywalled-paper retrieval** (Kim2014 + Sivyer2013): deferred to a later wave.
* **t0023**: remains intervention_blocked; not revisited this session.

## New Tasks Created

Five child tasks (t0041, t0042, t0043, t0044) are authorised by this session. Task indices are
auto-assigned by `/create-task` and will be strictly greater than 40 per the ordering invariant.
Full scopes live in each child task's `task_description.md`.

## Correction Files

Five corrections written to `corrections/`:

* `suggestion_S-0030-06.json` — update status to rejected
* `suggestion_S-0029-01.json` — update priority to medium
* `suggestion_S-0029-02.json` — update priority to medium
* `suggestion_S-0030-02.json` — update priority to medium
* `suggestion_S-0010-01.json` — update priority to medium

## Published-Data Comparison Artifact

Per the researcher's explicit request, the master test table and the published-data comparison table
are stored as `results/test_vs_literature_table.md`. They are also embedded in
`results/results_detailed.md` under the Methodology section and reproduced in `logs/session_log.md`
as part of the session transcript.

## Expected Assets

This brainstorm session produces no assets beyond the brainstorm-results task folder and its
downstream child tasks. `expected_assets` is `{}`.

## Dependencies

All 37 completed tasks up through t0039. t0023 and t0031 are excluded because they are not
completed.
