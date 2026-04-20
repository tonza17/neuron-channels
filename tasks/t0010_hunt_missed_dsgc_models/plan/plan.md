---
spec_version: "2"
task_id: "t0010_hunt_missed_dsgc_models"
date_completed: "2026-04-20"
status: "complete"
---
# Plan: Hunt DSGC Compartmental Models Missed by Prior Survey; Port Runnable Ones

## Objective

Close the gap between the t0002 literature survey (20-paper seeded corpus) and the t0008 ModelDB
189347 port by (a) consuming the already-completed three-pass candidate search recorded in
`research/research_internet.md`, (b) downloading the two qualifying new compartmental DSGC papers as
v3-compliant paper assets, (c) cloning each high-priority candidate repository and attempting a
NEURON 8.2.7 + Python 3.12 local port under a strict 90-minute wall-clock budget per candidate, (d)
scoring every successful port against the project's envelope via the `tuning_curve_loss` library
from t0012, and (e) summarising every candidate considered and the outcome of each port attempt in
one answer asset. "Done" looks like: two paper assets exist, 0-3 library assets exist (one per
successful port), one answer asset exists, a `data/candidates.csv` row exists for every candidate
from the CANDIDATES TABLE, and each verificator passes.

## Task Requirement Checklist

Operative task text (from `task_description.md` and `task.json`):

> **Name**: Hunt DSGC compartmental models missed by prior survey; port runnable ones
>
> **Short description**: Targeted literature + public-code search for DSGC compartmental models
> missed by the initial survey and the ModelDB 189347 port; download new papers and port any
> runnable ones to NEURON.
>
> 1. Systematic search across ModelDB full listing, GitHub/OSF/Zenodo, Google Scholar + Semantic
>    Scholar forward citations of Poleg-Polsky 2016, Schachter 2010, Park 2014, Sethuramanujam 2016,
>    Hanson 2019, and bioRxiv + preprint servers 2023-2025.
> 2. Download any paper not already in `assets/paper/` that meets the inclusion bar: publishes a
>    compartmental DSGC model with at least partial biophysical detail.
> 3. Port any paper with public code that runs in Python 3.12 + NEURON 8.2.7 (or Arbor 0.12.0), can
>    load `dsgc-baseline-morphology-calibrated` or bring its own morphology, and produces an
>    angle-resolved tuning curve.
> 4. Report every candidate in a single answer asset with a per-model row: paper DOI, code URL,
>    NEURON compatibility, whether ported, and if not, why not.
>
> **Expected outputs**: 1 answer asset, N paper assets (count determined by search), 0+ library
> assets per successful port, simulated tuning-curve CSVs in t0008 format under
> `data/tuning_curves/`.

Concrete requirement checklist:

* **REQ-1**: Execute a systematic search across ModelDB, GitHub/OSF/Zenodo, Google Scholar forward
  citations of the six seed papers, and bioRxiv preprint servers. Satisfied by steps 1-2 reusing the
  three-pass results recorded in `research/research_internet.md`. Evidence: the CANDIDATES TABLE is
  copied into `data/candidates.csv` and every row is retained or expanded.

* **REQ-2**: Download any paper that publishes a compartmental DSGC model AND is not already in the
  corpus (per `research/research_papers.md` Paper Index). Minimum set: deRosenroll 2026 (DOI
  `10.1016/j.celrep.2025.116833`), Poleg-Polsky 2026 (DOI `10.1038/s41467-026-70288-4`). Hanson 2019
  is explicitly already in corpus — must NOT be re-downloaded. Satisfied by steps 3-4. Evidence:
  two new paper-asset folders exist under `assets/paper/` with `details.json` v3 and canonical
  summaries; each passes the paper verificator.

* **REQ-3**: Attempt to port every HIGH-priority candidate from the CANDIDATES TABLE
  (`hanson_2019_spatial_offset`, `derosenroll_2026_circuit_ei`, `polegpolsky_2026_ds_mechanisms`)
  under a 90-minute wall-clock cap per candidate; each attempt decomposes into P1 (clone +
  library-asset scaffold), P2 (MOD compile + upstream demo run), P3 (12-angle x 20-trial canonical
  sweep + envelope scoring via `tuning_curve_loss`). Satisfied by steps 5-7. Evidence: logs under
  `logs/steps/009_implementation/port_*/` per candidate, and one row per candidate in
  `data/candidates.csv` with `port_outcome` populated.

* **REQ-4**: The port must run in Python 3.12 + NEURON 8.2.7 (as validated by t0007) and must emit
  the canonical tuning-curve CSV schema `(angle_deg, trial_seed, firing_rate_hz)` with exactly 240
  rows (12 angles x 20 trials) under `data/tuning_curves/curve_<slug>.csv`. Satisfied by step 7
  (P3). Evidence: each port's CSV passes the t0012 `load_tuning_curve` validator (hard-fails on
  non-12-angle, non-uniform grids).

* **REQ-5**: Triage rule: if a port's P2 step fails, STOP that candidate, record the failure in
  `data/candidates.csv` with `port_outcome = "failed-<reason>"`, and do NOT force a broken library
  asset. If all three HIGH-priority candidates fail P2, document the failures in the answer asset
  and exit implementation cleanly (no library asset created). Satisfied by step 5 gate logic.
  Evidence: conditional on outcome; at minimum, candidates.csv reflects the triage.

* **REQ-6**: Produce exactly one answer asset `assets/answer/dsgc-missed-models-survey/` (or
  semantically equivalent slug) per `meta/asset_types/answer/specification.md` v2 with
  `details.json`, `short_answer.md`, and `full_answer.md`. The full answer must contain one row per
  candidate from `data/candidates.csv` summarising paper DOI, code URL, NEURON compatibility, port
  attempted y/n, outcome, and envelope scores where ported. Satisfied by step 8. Evidence:
  answer-asset verificator passes; table has >= 14 rows (one per CANDIDATES TABLE entry).

* **REQ-7**: For every successfully ported model, write the four registered metric keys
  (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
  `tuning_curve_rmse`) into `results/metrics.json` using the explicit multi-variant metrics format
  (one variant per ported model). Satisfied by step 7 (P3) and step 9. Evidence:
  `results/metrics.json` exists and each variant matches the registered metric keys in
  `meta/metrics/`.

* **REQ-8**: Cap budget at $0.00 (local-only; no remote machines). Satisfied by the Remote Machines
  section below and by step_tracker.json steps 8 and 10 both in `skipped` state.

## Approach

**Task types** (already set in `task.json`): `literature-survey`, `download-paper`,
`code-reproduction`. The three types' Planning Guidelines converge on this approach:

* literature-survey mandates systematic multi-query search + synthesis; already executed in the
  three-pass research phase. This plan consumes the synthesis rather than re-running searches.
* download-paper mandates strict use of the paper-asset v3 spec, DOI-to-slug conversion via
  `arf.scripts.utils.doi_to_slug`, and full-text reading before writing the canonical summary.
* code-reproduction mandates the port attempts as `[CRITICAL]` steps — this plan treats the P2
  (demo run) step of each port as the critical gate; if it fails the task does not silently
  substitute a different model.

**Key research findings driving the approach** (repeated here so the implementation agent does not
need to read the research files):

* The three-pass search already ran (37 queries logged in `logs/steps/005_research-internet/`). Pass
  A (ModelDB, 12 queries): only ModelDB 189347 meets the DSGC compartmental bar and is already
  ported by t0008. Pass B (GitHub/Zenodo/OSF, 15 queries): three NEURON-capable candidates plus
  several SAC-only repos. Pass C (Scholar/bioRxiv, 12 queries): confirmed no third post-2020 DSGC
  compartmental model exists.
* **Exactly two** new compartmental DSGC papers exist that the project missed: deRosenroll 2026 Cell
  Reports (code at `geoffder/ds-circuit-ei-microarchitecture`, MIT licensed, Zenodo archive
  `10.5281/zenodo.17666157`) and Poleg-Polsky 2026 Nat Commun (code at
  `PolegPolskyLab/DS-mechanisms`, no LICENSE file, no Zenodo archive). Both use NEURON 8.2 + Python.
* Hanson 2019 (`geoffder/Spatial-Offset-DSGC-NEURON-Model`) was flagged by t0008 as a Phase B
  carry-over port target but not completed. It is the lowest-risk port because it sits on the exact
  t0008 boilerplate. The paper is already in the corpus; only the port is new.
* Every successful port MUST emit the canonical tuning-curve CSV schema
  `(angle_deg, trial_seed, firing_rate_hz)` at 12 angles x 20 trials and must be scored via
  `tuning_curve_loss.score` from t0012. The scorer hard-fails on non-12-angle, non-uniform grids, so
  this is a non-negotiable format constraint.
* t0008 established seven critical Windows-NEURON gotchas the implementation agent must carry
  forward: (1) HOC path literals need forward slashes (use `str(path).replace("\\", "/")`); (2)
  explicit `h.load_file("stdrun.hoc")` required when skipping `nrngui.hoc`; (3) `NEURONHOME` env var
  must default to `C:\Users\md1avn\nrn-8.2.7`; (4) MOD files compile via `run_nrnivmodl.cmd`
  wrapping `nrnivmodl.bat`; (5) produced DLL must be at `build/<slug>/nrnmech.dll`; (6)
  `h.nrn_load_dll` must return exactly 1.0; (7) bundled-morphology upstreams that use
  `placeBIP`-style synapse placement cannot accept an external SWC without rewriting the placement
  proc.

**Port pattern (from research_code.md)**: each port follows the t0008 archetype.

1. Bundle upstream HOC/MOD verbatim under `assets/library/<slug>/sources/`.
2. Add GUI-free derivative HOC if upstream has `xpanel`/`xbutton` lines.
3. Copy the eight reusable modules from t0008 (`run_nrnivmodl.cmd`, `build_cell.py`,
   `run_tuning_curve.py`, `score_envelope.py`, `test_smoke_single_angle.py`,
   `test_scoring_pipeline.py`, `swc_io.py` if SWC-based, `constants.py`) into `code/`.
4. Import `score`, `TUNING_CURVE_CSV_COLUMNS`, and the four `METRIC_KEY_*` constants from
   `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss` (the only cross-task
   imports allowed per CLAUDE.md rule 3 — library imports only).

**Port-attempt triage decomposition** (each HIGH-priority candidate runs three substeps P1 -> P2 ->
P3 sequentially; failure at any substep ends that candidate's attempt):

* **P1 (clone + scaffold)**: `git clone <url>` into a temporary area, copy the upstream code
  verbatim into `assets/library/<slug>/sources/`, pin the commit SHA (or Zenodo version if
  available) in `details.json`, note LICENSE presence/absence. Expected wall-clock: 5-10 min.
* **P2 (MOD compile + demo)**: run `run_nrnivmodl.cmd` to produce `build/<slug>/nrnmech.dll`; load
  via `h.nrn_load_dll`; execute the model's own demo / minimal single-trial script to confirm the
  cell builds, MODs load, and a non-zero simulation runs. Expected wall-clock: 10-30 min. **This is
  the critical gate**: if P2 fails, STOP and move on.
* **P3 (canonical sweep + score)**: copy the t0008 sweep driver, adapt `build_dsgc` and
  `run_one_trial` signatures to the upstream's API, run the 12-angle x 20-trial sweep, emit the
  canonical CSV, run the identity gate (`score(TARGET_MEAN_CSV, TARGET_MEAN_CSV) == 0.0`), then
  score the port's CSV and write a candidates.csv row. Expected wall-clock: 30-50 min (10-15 of
  which is the sweep itself). Per-candidate cap: **90 minutes total**.

**Port-attempt priority order** (updated from research_internet.md recommendation 2): P1 = **Hanson
2019** (carry-over, highest completion probability given t0008 boilerplate reuse); P2 =
**deRosenroll 2026** (high scientific relevance, MIT licensed, Zenodo archive — worth the risk);
P3 = **Poleg-Polsky 2026** (same senior author as 189347, missing LICENSE and no Zenodo archive —
attempted only if Hanson + deRosenroll complete under the combined budget).

**Alternatives considered**:

1. **Port all candidates simultaneously in parallel worktrees**: rejected — CLAUDE.md rule 2
   mandates one task = one folder = one branch; parallelising within the task would require
   sub-worktrees the framework does not currently support.
2. **Hand-port Schachter 2010 from NeuronC to NEURON**: rejected — NeuronC is a separate simulator
   language and a rewrite would require unit-testing against paper Figure panels, which is out of
   this task's automatic-port envelope. Deferred to a new suggestion per research_papers.md
   recommendation 7.
3. **Use the calibrated t0009 SWC for every port**: rejected for Poleg-Polsky-lineage ports — the
   bundled morphology is topologically coupled to synapse placement (research_code.md lesson 2).
   Only applied if the upstream uses `h.Import3d_SWC_read` or equivalent geometric loader.
4. **Skip the port attempts and deliver only the paper-asset downloads + answer asset**: rejected
   — REQ-3 explicitly mandates port attempts. The 90-minute per-candidate cap is already a
   fallback; zero attempts would not satisfy the task.

## Cost Estimation

| Item | Cost (USD) | Reasoning |
| --- | --- | --- |
| LLM API (agents, local Claude Code) | $0.00 | Running inside an already-subscribed harness; no metered API spend attributed to this task. |
| Remote compute (GPU, cloud) | $0.00 | None required; all port attempts run on the local Windows workstation where NEURON 8.2.7 is validated (t0007). |
| Paper downloads | $0.00 | Both target papers are open-access: Cell Reports (deRosenroll 2026, open-access per Cell Press policy) and Nature Communications (Poleg-Polsky 2026, open-access by journal policy). |
| Code repositories | $0.00 | Both GitHub repos and the Zenodo archive are public under MIT or no-license-posted (which imposes no cost). |
| **Total** | **$0.00** |  |

Project budget (`project/budget.json`): `total_budget = $1.00`, `per_task_default_limit = $1.00`.
This task consumes $0.00, well within the per-task cap.

## Step by Step

### Milestone A: Candidate capture

1. **Seed `data/candidates.csv` from the CANDIDATES TABLE.** Create `data/candidates.csv` with the
   columns
   `candidate_id,paper_doi,code_url,first_author,year,venue,simulator,has_public_code,neuron_compatible,port_attempted,port_outcome,dsi,peak_hz,null_hz,hwhm_deg,passes_envelope,exclusion_reason,triage_priority`.
   Copy each of the 14 rows from the CANDIDATES TABLE in `research/research_internet.md` verbatim,
   mapping `priority_for_t0010_implementation` -> `triage_priority` and leaving `port_attempted`,
   `port_outcome`, `dsi`, `peak_hz`, `null_hz`, `hwhm_deg`, `passes_envelope` blank. File to create:
   `tasks/t0010_hunt_missed_dsgc_models/data/candidates.csv`. Expected output: 14-row CSV. Satisfies
   REQ-1.

2. **Verify the candidates table against the existing paper corpus.** Read the Paper Index in
   `tasks/t0010_hunt_missed_dsgc_models/research/research_papers.md` and confirm that (a) Hanson
   2019 (DOI `10.7554/eLife.42392`) is already in the corpus at
   `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/` —
   if present, do NOT re-download; (b) deRosenroll 2026 (DOI `10.1016/j.celrep.2025.116833`) is NOT
   in the corpus; (c) Poleg-Polsky 2026 (DOI `10.1038/s41467-026-70288-4`) is NOT in the corpus.
   Emit a one-line log to `logs/steps/009_implementation/candidates_corpus_check.md` stating the
   verified state. Satisfies REQ-2 (precondition).

### Milestone B: Paper asset creation

3. **Download deRosenroll 2026 as a paper asset.** Invoke the `/add-paper` skill with DOI
   `10.1016/j.celrep.2025.116833`. Expected paper_id (generate via
   `uv run python -u -m arf.scripts.utils.doi_to_slug "10.1016/j.celrep.2025.116833"`):
   `10.1016_j.celrep.2025.116833`. Folder:
   `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/` with
   `details.json` v3, `summary.md`, and `files/`. Categories must include `compartmental-modeling`,
   `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`. The Overview,
   Architecture/Models/Methods, Results, Innovations, Datasets, Main Ideas, and Summary sections
   must be written from full-text reading (not abstract-only). Verify with
   `uv run python -u -m arf.scripts.verificators.verify_paper_asset --task-id t0010_hunt_missed_dsgc_models 10.1016_j.celrep.2025.116833`.
   Expected output: zero errors. Satisfies REQ-2.

4. **Download Poleg-Polsky 2026 as a paper asset.** Invoke the `/add-paper` skill with DOI
   `10.1038/s41467-026-70288-4`. Expected paper_id: `10.1038_s41467-026-70288-4`. Folder:
   `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/`. Categories must
   include `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`. Verify with
   the same command substituting the paper id. Expected output: zero errors. Satisfies REQ-2.

### Milestone C: Port attempts (strict priority order with per-candidate budget caps)

5. **[CRITICAL] Port attempt P1 Hanson 2019 `hanson_2019_spatial_offset`.** Candidate priority 1
   (highest completion probability — carry-over from t0008 Phase B). Wall-clock cap: **90 minutes
   total** across substeps P1-P3.

   * **Substep 5.P1 (clone + scaffold, 5-10 min)**:
     `git clone https://github.com/geoffder/ Spatial-Offset-DSGC-NEURON-Model.git` into a scratch
     folder outside the task (e.g. `%TEMP%/spatial-offset-clone`), then copy its contents into
     `assets/library/hanson_2019_spatial_offset/sources/`. Record the resolved commit SHA in
     `assets/library/hanson_2019_spatial_offset/details.json` `version`. Record LICENSE presence.
     Scaffold `details.json` v2 and `description.md` per
     `meta/asset_types/library/specification.md`.
   * **Substep 5.P2 (MOD compile + demo, 10-30 min)**: copy
     `tasks/t0008_port_modeldb_189347/code/run_nrnivmodl.cmd` and
     `tasks/t0008_port_modeldb_189347/code/build_cell.py` into `code/`, adapt the MOD source dir and
     DLL path to `assets/library/hanson_2019_spatial_offset/sources/<mods>/` and
     `build/hanson_2019_spatial_offset/nrnmech.dll`. Run the compile wrapper; then execute the
     upstream repo's own minimal demo (identify it from the README) with the DLL loaded. Expected
     output: upstream script runs to completion (may produce figures or console output) and does not
     raise. **Validation gate**: baseline for this step is "upstream demo runs headless without
     Python exceptions and with non-empty simulation output." If the demo fails (exception, Python 2
     syntax, missing dependency the t0008 boilerplate fixes cannot address), STOP the candidate, set
     `port_outcome = "failed-<reason>"` in `data/candidates.csv`, do NOT create the library asset,
     and advance to step 6.
   * **Substep 5.P3 (canonical sweep + score, 30-50 min)**: copy
     `tasks/t0008_port_modeldb_189347/code/run_tuning_curve.py`,
     `tasks/t0008_port_modeldb_189347/code/score_envelope.py`,
     `tasks/t0008_port_modeldb_189347/code/test_smoke_single_angle.py`, and
     `tasks/t0008_port_modeldb_189347/code/test_scoring_pipeline.py` into `code/`. Repoint
     `build_dsgc` and `run_one_trial` to the Hanson 2019 API. First run
     `code/test_scoring_pipeline.py` to confirm the identity gate: baseline
     `score(simulated_curve_csv=TARGET_MEAN_CSV, target_curve_csv=TARGET_MEAN_CSV).loss_scalar == 0.0`
     and `passes_envelope is True`. If the identity gate fails, STOP — the scoring wiring is
     broken. If it passes, run the smoke test with `--limit 1` (single angle=0, seed=1); baseline is
     `SMOKE_TEST_MIN_FIRING_HZ = 0.0`; if firing rate is below this, STOP and inspect individual
     outputs (inspect per-trial NEURON state dumps and verify synapse coords, stim timing, DLL
     load). Then run the full 12-angle x 20-trial sweep producing
     `data/tuning_curves/curve_hanson_2019_spatial_offset.csv` (exactly 240 rows, canonical schema).
     Finally run `code/score_envelope.py` producing
     `data/score_report_hanson_2019_spatial_offset.json` and populate the Hanson 2019 row in
     `data/candidates.csv` with `port_attempted=yes, port_outcome=ported`, DSI, peak_hz, null_hz,
     hwhm_deg, and `passes_envelope` from the score report.

   Import `score`, `TUNING_CURVE_CSV_COLUMNS`, `METRIC_KEY_DSI`, `METRIC_KEY_HWHM`,
   `METRIC_KEY_RELIABILITY`, `METRIC_KEY_RMSE` from
   `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss`. Satisfies REQ-3, REQ-4,
   REQ-5.

6. **[CRITICAL] Port attempt P2 deRosenroll 2026 `derosenroll_2026_circuit_ei`.** Candidate priority
   2\. Wall-clock cap: **90 minutes total**. Only run this step if step 5 finished (either with
   `ported` or `failed-<reason>`) AND the cumulative implementation wall-clock has not exceeded 4
   hours.

   * **Substep 6.P1**: clone `https://github.com/geoffder/ds-circuit-ei-microarchitecture.git` AND
     also fetch the Zenodo archive `10.5281/zenodo.17666157` as the version-of-record (port against
     the Zenodo tarball, not the GitHub HEAD — per research_internet.md best practice). Copy
     contents into `assets/library/derosenroll_2026_circuit_ei/sources/`. Pin the Zenodo DOI in
     `details.json` `version`. Record MIT LICENSE presence.
   * **Substep 6.P2**: identical structure to 5.P2. If P2 fails, STOP, record
     `port_outcome=failed-<reason>`, do not create library asset, advance to step 7.
   * **Substep 6.P3**: identical structure to 5.P3 emitting
     `data/tuning_curves/curve_derosenroll_2026_circuit_ei.csv` and
     `data/score_report_derosenroll_2026_circuit_ei.json`.

   Satisfies REQ-3, REQ-4, REQ-5.

7. **[CRITICAL] Port attempt P3 Poleg-Polsky 2026 `polegpolsky_2026_ds_mechanisms`.** Candidate
   priority 3 (lowest — no LICENSE file, no Zenodo archive; higher risk). Wall-clock cap: **90
   minutes total**. Only run this step if steps 5 and 6 both finished AND cumulative implementation
   wall-clock has not exceeded 6 hours; otherwise defer this candidate to a new suggestion in step
   14 (suggestions stage, orchestrator-managed).

   * **Substep 7.P1**: clone `https://github.com/PolegPolskyLab/DS-mechanisms.git`, check out the
     `June2025` branch, and record "NO LICENSE" in `details.json` `license`. Copy into
     `assets/library/polegpolsky_2026_ds_mechanisms/sources/`.
   * **Substep 7.P2**: identical structure. The Poleg-Polsky repo has an ML-driven GA driver
     (`GA_NEURON.py`); the demo is the GA's smallest training run. P2 passes if the GA can run one
     generation end-to-end. If P2 fails, STOP and record.
   * **Substep 7.P3**: identical structure emitting the 352-segment DSGC sweep CSV at
     `data/tuning_curves/curve_polegpolsky_2026_ds_mechanisms.csv` and score report.

   Satisfies REQ-3, REQ-4, REQ-5.

### Milestone D: Metrics and answer asset

8. **Write `results/metrics.json` using the explicit multi-variant format.** For every port that
   completed P3 with `port_outcome=ported`, emit a variant with the four registered metric keys
   (`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
   `tuning_curve_rmse`). Variant names: `hanson_2019_spatial_offset`, `derosenroll_2026_circuit_ei`,
   `polegpolsky_2026_ds_mechanisms` (one per successful port). Use the metrics-specification
   explicit multi-variant format (see `arf/specifications/metrics_specification.md`). If zero ports
   succeeded, write an empty explicit-format `metrics.json` (empty `variants` list). The answer
   asset (step 9) carries the narrative explanation of port failures. Satisfies REQ-7.

9. **Write the answer asset `assets/answer/dsgc-missed-models-survey/`.** Follow
   `meta/asset_types/answer/specification.md` v2:

   * `details.json` v2 with `answer_id = "dsgc-missed-models-survey"`,
     `question = "Which DSGC compartmental models did the t0002 literature survey and the t0008 ModelDB 189347 port miss, which are portable to NEURON 8.2.7 + Python 3.12, and how do they score against the project's tuning-curve envelope?"`,
     `short_title = "Missed DSGC models hunt and port outcomes"`,
     `categories = ["compartmental-modeling", "direction-selectivity", "retinal-ganglion-cell"]`,
     `answer_methods = ["papers", "internet", "code-experiment"]`, `source_paper_ids` listing the
     two new paper IDs from steps 3-4 plus `10.7554_eLife.42392` (Hanson 2019 as evidence, not a new
     download),
     `source_task_ids = ["t0002_literature_survey_dsgc_ compartmental_models", "t0008_port_modeldb_189347", "t0012_tuning_curve_scoring_loss_ library"]`,
     `source_urls` listing the three candidate GitHub repos + Zenodo archive, `confidence = "high"`
     if at least one port succeeded else `"medium"`,
     `created_by_task = "t0010_hunt_missed_dsgc_models"`, `date_created = "2026-04-20"`.
   * `short_answer.md`: Question + 2-5 sentence Answer (state how many new models were found, how
     many were portable, the top-line envelope scores) + Sources.
   * `full_answer.md`: mandatory sections from the spec (Question, Short Answer, Research Process,
     Evidence from Papers, Evidence from Internet Sources, Evidence from Code or Experiments,
     Synthesis, Limitations, Sources). The **Evidence from Code or Experiments** section MUST
     contain a markdown table with one row per candidate from `data/candidates.csv` (columns:
     candidate_id, paper_doi, code_url, neuron_compatible, port_attempted, port_outcome, dsi,
     peak_hz, null_hz, hwhm_deg, passes_envelope). If all three HIGH-priority candidates failed P2,
     the Synthesis section must state this explicitly and the Limitations section must discuss the
     community pattern (DSGC compartmental code fragility per research_papers.md).

   Verify with
   `uv run python -u -m arf.scripts.verificators.verify_answer_asset --task-id t0010_hunt_missed_dsgc_models dsgc-missed-models-survey`
   (or the equivalent in this ARF snapshot). Expected output: zero errors. Satisfies REQ-6.

## Remote Machines

None required. The entire implementation runs on the local Windows workstation where NEURON 8.2.7
+ Python 3.12 are already validated by t0007 (`C:\Users\md1avn\nrn-8.2.7`). Remote machine setup and
  teardown steps in `step_tracker.json` (steps 8 and 10) are already marked `skipped`. Budget is
  $0.00.

## Assets Needed

Input assets consumed by this task:

* **Paper asset `10.7554_eLife.42392`** (Hanson 2019) at
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/` —
  evidence source for Hanson 2019 port; already in corpus, NOT to be re-downloaded.
* **Paper asset `10.1016_j.neuron.2016.02.013`** (Poleg-Polsky & Diamond 2016) at
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
  — baseline reference for envelope targets.
* **Library asset `modeldb_189347_dsgc`** v0.1.0 at
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/` — read as port archetype
  (code copied into this task's `code/`, not imported).
* **Library asset `tuning_curve_loss`** v0.1.0 at
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/` — imported
  (`from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import score, TUNING_CURVE_CSV_COLUMNS, METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY, METRIC_KEY_RMSE`).
* **Dataset asset `dsgc-baseline-morphology-calibrated`** at
  `tasks/t0009_calibrate_dendritic_diameters/assets/dataset/dsgc-baseline-morphology-calibrated/`
  — referenced by absolute path only for ports whose upstream accepts external SWC.
* **External repositories**: `https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model` (Hanson
  2019 code), `https://github.com/geoffder/ds-circuit-ei-microarchitecture` + Zenodo
  `10.5281/zenodo.17666157` (deRosenroll 2026 code),
  `https://github.com/PolegPolskyLab/DS-mechanisms` branch `June2025` (Poleg-Polsky 2026 code).

## Expected Assets

Per `task.json` `expected_assets` and the research synthesis:

* **1 answer asset** — `assets/answer/dsgc-missed-models-survey/` containing `details.json` v2,
  `short_answer.md`, and `full_answer.md`. Summarises the three-pass hunt outcome with one table row
  per CANDIDATES TABLE entry. Required by REQ-6 and by `task.json` `expected_assets.answer = 1`.

* **2 paper assets (mandatory)** — `10.1016_j.celrep.2025.116833` (deRosenroll 2026) and
  `10.1038_s41467-026-70288-4` (Poleg-Polsky 2026). Required by REQ-2. Each asset is
  v3-spec-compliant (`details.json`, `summary.md`, `files/`).

* **0-3 library assets** — one per successful port: `hanson_2019_spatial_offset`,
  `derosenroll_2026_circuit_ei`, `polegpolsky_2026_ds_mechanisms`. Exact count depends on how many
  P2 gates pass within the per-candidate 90-minute caps and the combined wall-clock budget. If zero
  pass, no library asset is created — the answer asset documents the failures.

* **0-3 tuning-curve CSVs** — at `data/tuning_curves/curve_<slug>.csv`, one per successful port,
  each 240 rows in canonical schema.

* **1 candidates CSV** — `data/candidates.csv`, always created, always 14+ rows (one per
  CANDIDATES TABLE entry).

**Note**: `task.json` declares only `expected_assets.answer = 1` explicitly; the 2 papers and 0-3
libraries are produced opportunistically based on what the search + port found. The task-
verificator's expected-assets check will accept this because paper and library counts are not
pre-declared.

## Time Estimation

Per-phase wall-clock estimates (implementation only; orchestrator-managed steps not included):

| Phase | Wall-clock estimate |
| --- | --- |
| Research (papers + internet + code) | Already complete (~65 min logged). |
| Planning (this document) | ~30 min (current phase). |
| Milestone A (candidates.csv seed + corpus check) | 15 min. |
| Milestone B (two paper assets via `/add-paper`) | 60 min (30 min per paper, including full-text reading + summary). |
| Milestone C (three port attempts, 90 min each) | Up to 270 min (4.5 h) in the worst case; likely 90-180 min because failure short-circuits. |
| Milestone D (metrics.json + answer asset) | 60 min. |
| **Total implementation** | **~6-7 hours wall-clock.** |

## Risks & Fallbacks

Pre-mortem assumption: the task has already failed. Working backwards from failure, the most likely
root causes are:

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Hanson 2019 repo has Python 2 / NEURON 7 code that the t0008 boilerplate fixes cannot resolve (e.g., Python 2 print statements deep in many files, NEURON 7-specific HOC idioms). | Medium | Blocks port 1; reduces ported-model count. | P2 gate catches this immediately; `port_outcome=failed-py2-compat` recorded; move to deRosenroll 2026. Fallback: add to new suggestions as a hand-port task in future iteration. |
| deRosenroll 2026 upstream depends on a library outside the current Python 3.12 environment (e.g., specific NEURON plugin, NetPyNE build). | Medium | Blocks port 2. | Inspect `requirements.txt` at clone time before P2; if mismatch, document the gap and fall back to the GitHub HEAD rather than Zenodo if HEAD has updated deps. If both fail, record and move on. |
| Poleg-Polsky 2026 GA driver's single-generation demo takes >30 minutes (exceeds P2 budget). | Medium | Reduces candidate ordering. | Cap the GA at 1 generation with tiny population (`--pop-size 2`) for P2 smoke test; if upstream does not expose this, skip P2 and record `port_outcome=failed-demo-too-slow`. Defer full sweep as a new suggestion. |
| All three HIGH-priority candidates fail P2 within budget. | Low-medium | Zero library assets produced. | The task still succeeds: deliver the two paper assets + answer asset documenting the three failures. Generate new suggestions (in the suggestions stage) for hand-port tasks. |
| GitHub clone hits a rate limit or the Zenodo archive is temporarily unavailable. | Low | Delays port. | Retry with backoff (up to 3 attempts, 60s each); if still blocked, create an intervention file in `intervention/` and defer that candidate's port. |
| Tuning-curve CSV fails the t0012 `load_tuning_curve` validator (non-12-angle grid, inconsistent trials). | Medium (per port) | Blocks scoring but not the port itself. | The sweep driver from t0008 hard-codes `N_ANGLES=12, N_TRIALS=20`; if the adaptation to the upstream API accidentally emits a different grid, the identity gate in 5/6/7.P3 catches it before full-sweep wall-clock is spent. |
| A port completes P3 but the model's tuning curve is outside the project envelope (DSI < 0.7, peak outside 30-80 Hz, HWHM outside 60-90 deg). | Medium-high | The port is technically correct but doesn't pass the envelope; this IS a finding, not a failure. | Per t0012 lesson, out-of-envelope results are findings. Record `port_outcome=ported` with `passes_envelope=false`, include the result in the answer asset's Synthesis section, and generate a suggestion to investigate the discrepancy. |
| The two new papers (deRosenroll 2026, Poleg-Polsky 2026) are paywalled in ways that break `/add-paper` automation. | Low | Blocks REQ-2. | Both journals (Cell Reports, Nature Communications) are open-access; this should not occur. If it does, record `download_status=failed` with reason, write the summary from the abstract + GitHub README, and flag the paper for manual download in an intervention file. |

## Verification Criteria

Each criterion names the exact command and the expected output.

* **Paper assets verify clean.** Run (for each new paper id):
  `uv run python -u -m arf.scripts.verificators.verify_paper_asset --task-id t0010_hunt_missed_dsgc_models 10.1016_j.celrep.2025.116833`
  and
  `uv run python -u -m arf.scripts.verificators.verify_paper_asset --task-id t0010_hunt_missed_dsgc_models 10.1038_s41467-026-70288-4`.
  Expected: zero errors per paper. Confirms REQ-2.

* **Answer asset verifies clean.** Run
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset --task-id t0010_hunt_missed_dsgc_models dsgc-missed-models-survey`
  and confirm zero errors. Confirms REQ-6.

* **Every HIGH-priority candidate has a candidates.csv row.** Run
  `python -c "import csv; rows = list(csv.DictReader(open('tasks/t0010_hunt_missed_dsgc_models/data/candidates.csv'))); high = [r for r in rows if r['triage_priority']=='high']; assert len(high)==3, f'expected 3 high-priority rows, got {len(high)}'; assert all(r['port_outcome'] for r in high), 'every high-priority candidate must have a port_outcome'; print('ok')"`.
  Expected: prints `ok`. Confirms REQ-3 and REQ-5.

* **Every ported model has an envelope-valid tuning-curve CSV.** For each library asset under
  `assets/library/`, run
  `uv run python -u -c "from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import load_tuning_curve; load_tuning_curve('tasks/t0010_hunt_missed_dsgc_models/data/tuning_curves/curve_<slug>.csv')"`
  (substitute `<slug>`). Expected: load returns a `TuningCurve` dataclass without exception and
  `len(curve.angles) == 12`. Confirms REQ-4.

* **`results/metrics.json` uses only registered metric keys.** Run
  `python -c "import json; m = json.load(open('tasks/t0010_hunt_missed_dsgc_models/results/metrics.json')); allowed = {'direction_selectivity_index', 'tuning_curve_hwhm_deg', 'tuning_curve_reliability', 'tuning_curve_rmse'}; from itertools import chain; keys = set(chain.from_iterable(v.keys() for v in m.get('variants', {}).values())) if 'variants' in m else set(m.keys()); assert keys <= allowed or not m, f'unexpected keys: {keys - allowed}'; print('ok')"`.
  Expected: prints `ok`. Confirms REQ-7.

* **Plan verificator passes.** Run
  `uv run python -u -m arf.scripts.verificators.verify_plan t0010_hunt_missed_dsgc_models`.
  Expected: zero errors.

* **Requirement coverage sanity check.** The answer asset's `full_answer.md` Synthesis section must
  mention every REQ-1 through REQ-8 by outcome. Confirm via manual grep
  (`grep -c "REQ-" tasks/t0010_hunt_missed_dsgc_models/assets/answer/dsgc-missed-models-survey/full_answer.md`)
  returning at least 8 matches.
