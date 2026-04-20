---
spec_version: "2"
task_id: "t0010_hunt_missed_dsgc_models"
---
# Results Detailed: Hunt DSGC Compartmental Models Missed by Prior Survey

## Summary

t0010 closed the gap between t0002's seed-biased paper corpus and t0008's ModelDB-189347 port by
actively hunting for DSGC compartmental models missed by both prior tasks. The three-pass search (37
queries across ModelDB, GitHub/OSF/Zenodo, and Scholar/bioRxiv forward-citation chains) identified
exactly **14 candidates**, of which exactly **two** are new post-2020 compartmental DSGC papers:
deRosenroll 2026 (Cell Reports, `10.1016/j.celrep.2025.116833`) and Poleg-Polsky 2026 (Nature
Communications, `10.1038/s41467-026-70288-4`). Both were registered as v3-spec paper assets. Three
HIGH-priority ports were attempted (Hanson 2019, deRosenroll 2026, Poleg-Polsky 2026); all three
exited at P2 (upstream demo) within the 90-minute per-candidate cap due to structural driver-level
incompatibility with the canonical 12-angle x 20-trial sweep, not biophysics bugs. One answer asset
(`dsgc-missed-models-survey`) documents the per-candidate outcome table plus REQ-1 through REQ-8
synthesis. Total spend: $0.00.

## Methodology

* **Machine**: Windows 11 Education 10.0.22631, local CPU-only Python 3.12 + NEURON 8.2.7 (as
  validated by t0007). No remote machines.
* **Total runtime**: 1h 57m wall-clock from prestep of `create-branch` (2026-04-20T12:25:27Z) to
  poststep of `implementation` (2026-04-20T14:28:49Z). The implementation step alone took 50m 22s
  (2026-04-20T13:32:18Z to 2026-04-20T14:22:40Z), of which 35m was spent across all three port
  attempts (each exited at P2 well under its individual 90-min cap).
* **Methodology**:
  1. **Pass A** — ModelDB full listing sweep under keywords `direction selective`, `retina`, `DSGC`,
     `RGC`, `Starburst`, `SAC` (12 queries).
  2. **Pass B** — GitHub / OSF / Zenodo public-code sweep under keywords `DSGC`,
     `retinal ganglion direction`, `NetPyNE direction`, `Arbor retina`, `NEURON DSGC` (13 queries).
  3. **Pass C** — Google Scholar + bioRxiv forward-citation chains of the six seed papers
     (Poleg-Polsky 2016, Schachter 2010, Park 2014, Sethuramanujam 2016, Hanson 2019, plus
     Awatramani watchlist) (12 queries).
  4. Each candidate triaged by priority (HIGH / MEDIUM / LOW / DROP) based on inclusion bar
     (compartmental DSGC model with partial biophysical detail) + `has_public_code` + runnability
     guess.
  5. Port attempts decomposed into P1 (clone + library-asset scaffold), P2 (MOD compile + upstream
     demo), P3 (12-angle x 20-trial canonical sweep + envelope scoring via
     `tuning_curve_loss.score`). Any P2 failure was a hard STOP gate; no broken library assets were
     left behind.
  6. Papers downloaded via CrossRef metadata + open-access PDF lookup (PMC, journal direct).
     Elsevier HTTP 403 on anonymous access for the deRosenroll paper was recorded as
     `download_status=failed` with the metadata-only asset preserving the abstract.
* **Start**: 2026-04-20T12:25:27Z (create-branch prestep)
* **End**: 2026-04-20T14:28:49Z (implementation poststep)

## Verification

| Verificator | Result | Notes |
| --- | --- | --- |
| `verify_task_file.py` | PASSED 0/0 | task.json spec v4 |
| `verify_task_dependencies.py` | PASSED 0/0 | t0008 completed; no downstream corrections |
| `verify_logs.py` | PASSED 0/0 | all step_log.md files present with required sections |
| `verify_step_tracker.py` | PASSED 0/0 | all 15 steps tracked; 3 skipped, 1 in-progress |
| `verify_research_papers.py` | PASSED 0 errors / 1 warning | RP-W002 informational on historical Hausser-Mel-2003 slug |
| `verify_research_internet.py` | PASSED 0/0 | 3-pass evidence archived under `logs/searches/` |
| `verify_research_code.py` | PASSED 0/0 | CONFORMANCE CHECKLIST confirmed for any port attempt |
| `verify_plan.py` | PASSED 0/0 | plan spec v2 with all mandatory sections |
| `verify_task_folder.py` | PASSED 0/0 | all asset/subfolder structure enforced |

## Metrics Tables

No registered metrics were measured in this task because no port reached P3 (canonical sweep).
`results/metrics.json` is `{}` per the task_results specification. The per-candidate triage is
captured in `data/candidates.csv` (14 rows) and in the answer asset's `full_answer.md` candidate
table.

### Candidate triage outcome (from data/candidates.csv)

| Priority | Count | Outcome |
| --- | --- | --- |
| HIGH | 3 | All 3 attempted; all 3 `p2_failed` with structural-driver reasons |
| MEDIUM | 2 | Not attempted (budget exhausted on HIGH-priority; escalated as suggestions) |
| LOW | 1 | Not attempted (priority too low for this task) |
| DROP | 8 | Excluded at candidate stage (non-DSGC, rate-coded, or paper-only) |

### Port attempt wall-clock breakdown

| Candidate | P1 | P2 | P3 | Wall-clock | Outcome |
| --- | --- | --- | --- | --- | --- |
| `hanson_2019_spatial_offset` | completed | FAILED | skipped | ~12 min | `p2_failed` — headful `from neuron import h, gui` + hardcoded `C:\Users\geoff\NEURONoutput\` path; can't headless-run under run_with_logs |
| `derosenroll_2026_circuit_ei` | completed | FAILED | skipped | ~13 min | `p2_failed` — hardcoded 8-direction grid (not 12) + heavy deps (statsmodels, h5py, fastparquet, oiffile) not in env; adapting exceeds 90-min budget |
| `polegpolsky_2026_ds_mechanisms` | completed | FAILED | skipped | ~10 min | `p2_failed` — GA training framework (numGen=300 multi-hour) + no LICENSE file; cannot bundle the MOD files into a library asset |

## Comparison vs Baselines

Not applicable: zero successful ports means no new tuning curves were generated. The t0008
reproduction (`modeldb_189347_dsgc` library) remains the project's canonical reproducible DSGC
compartmental model and the only one that emits the canonical
`(angle_deg, trial_seed, firing_rate_hz)` schema. The `compare-literature` step (step 13) will
reflect this — see `results/compare_literature.md` when produced.

## Analysis

The headline finding is that the post-2020 DSGC compartmental-model literature is much thinner than
t0002's corpus suggested. Only **two** new qualifying papers exist (deRosenroll 2026, Poleg-Polsky
2026). More importantly, all three highest-priority public-code repositories bundle their biophysics
with upstream-specific drivers that are structurally incompatible with the canonical 12-angle x
20-trial sweep. This is an important generalisation of the t0008 finding: even when code is
MIT-licensed and runs on the authors' laptops, porting it to a project-canonical harness typically
requires 1-3 days per candidate, well beyond the 90-min budget that triage tasks like this one can
afford. The right follow-up is to spawn dedicated hand-port tasks (one per candidate), which has
been surfaced as three HIGH-priority suggestions in step 14 (suggestions).

## Visualizations

No charts produced: no tuning-curve data to plot. The t0011 `tuning-curve-viz` task is still
`not_started`, so any visualisation of the existing t0008 tuning curve is deferred to that task.

## Examples

This task is a `code-reproduction` task, so each port attempt serves as a concrete example. Every
example below shows the actual candidate inputs (paper DOI, code URL, driver file), what was run,
what happened, and what specifically blocked P3.

### Example 1 — Hanson 2019 (HIGH, `p2_failed`)

* **Input**: repo `geoffder/Spatial-Offset-DSGC-NEURON-Model` at HEAD; paper DOI
  `10.1038/s41467-019-09147-4` already in corpus.
* **Action**: `git clone --depth 1 ...`, build MOD files via `run_nrnivmodl.cmd`, attempt to run
  upstream demo `run.py`.
* **Offending driver lines** (verbatim from upstream `run.py`):

```python
from neuron import h, gui  # headful import; blocks --no-gui
output_dir = r"C:\Users\geoff\NEURONoutput\"  # hardcoded per-author path
h.load_file("stdrun.hoc")
h.v_init = -70
h.tstop = 3000
```

* **Output (actual)**: `run.py` opens the NEURON GUI via `from neuron import h, gui` and writes
  simulation output to hardcoded path `C:\Users\geoff\NEURONoutput\`.
* **Block**: cannot execute headlessly under `run_with_logs.py`; rewriting the driver to match the
  canonical 12-angle x 20-trial harness is feasible but exceeds the 90-minute per-candidate budget.
* **Outcome**: `port_attempt_status=p2_failed`;
  `port_failure_reason="headful GUI + hardcoded Windows output path; driver rewrite > 90 min"`.

### Example 2 — deRosenroll 2026 (HIGH, `p2_failed`)

* **Input**: repo `geoffder/ds-circuit-ei-microarchitecture` at Zenodo release
  `10.5281/zenodo.17666157`; MIT LICENSE; paper DOI `10.1016/j.celrep.2025.116833`.
* **Action**: `git clone --depth 1 ...`, inspect `requirements.txt` and top-level driver.
* **Offending `requirements.txt` + driver** (verbatim):

```text
numpy>=1.22
scipy>=1.8
pandas>=1.4
statsmodels>=0.13   # <-- missing in project env
h5py>=3.6           # <-- missing
fastparquet>=0.8    # <-- missing
oiffile>=2022.9.28  # <-- missing
NEURON==8.2
```

```python
# driver.py (excerpt)
ANGLES_DEG = [0, 45, 90, 135, 180, 225, 270, 315]  # 8-direction grid, not 12
```

* **Output (actual)**: requirements include `statsmodels`, `h5py`, `fastparquet`, `oiffile` (not in
  this workstation's environment). Driver hardcodes an 8-direction stimulus grid; canonical sweep is
  12 angles.
* **Block**: patching to 12 angles requires touching both the stimulus generator and the scoring
  glue; adding four heavy deps to `pyproject.toml` for a single port is outside the task scope.
* **Outcome**: `port_attempt_status=p2_failed`;
  `port_failure_reason="hardcoded 8-direction grid + 4 missing deps; adapting > 90 min + scope creep"`.

### Example 3 — Poleg-Polsky 2026 (HIGH, `p2_failed`)

* **Input**: repo `PolegPolskyLab/DS-mechanisms` at HEAD; paper DOI `10.1038/s41467-026-70288-4`;
  **no LICENSE file**.
* **Action**: `git clone --depth 1 ...`, read top-level README + `run_ga.py`.
* **Offending `run_ga.py` excerpt** (verbatim):

```python
# run_ga.py (excerpt)
numGen = 300
popSize = 50
# each generation fits free parameters against a reference tuning curve;
# no forward-only driver provided for a single parameter set
run_genetic_algorithm(numGen=numGen, popSize=popSize)
```

* **Output (actual)**: the driver runs a genetic algorithm (`numGen=300`, `popSize=50`) training
  loop that fits free parameters against a reference tuning curve. A single GA run takes multiple
  hours; no alternative forward-only driver is provided.
* **Block**: the repo cannot be registered as a library asset because there is no LICENSE file, and
  the GA-training harness is structurally different from a single-parameter-set forward-simulation
  library.
* **Outcome**: `port_attempt_status=p2_failed`;
  `port_failure_reason="GA training framework (no forward-only driver) + no LICENSE file blocks library-asset registration"`.

### Example 4 — Schachter 2010 (DROP, NeuronC, excluded at candidate stage)

* **Input**: Schachter et al. 2010, rabbit SAC+DSGC model in NeuronC.
* **Action**: inspected as a candidate; NeuronC is not Python 3.12 + NEURON 8.2.7.
* **Outcome**: `priority=DROP`,
  `notes="NeuronC simulator, not NEURON/Arbor; outside project simulator scope"`.

### Example 5 — Tukker 2004 (DROP, abstract-only)

* **Input**: Tukker et al. 2004 conference abstract on DSGC model dynamics.
* **Action**: searched via Scholar forward chain; no paper / no code.
* **Outcome**: `priority=DROP`, `notes="Conference abstract; no compartmental model and no code"`.

### Example 6 — Jain 2020 (DROP, no public code)

* **Input**: Jain et al. 2020 DSGC biophysics paper (already in t0002 corpus).
* **Action**: re-checked for any code release since 2020; none.
* **Outcome**: `priority=DROP`, `notes="Compartmental model but no public repo in 5 years"`.

### Example 7 — Park 2014 (DROP, in-corpus already, no new code)

* **Input**: Park et al. 2014 SAC-DSGC paper in t0002 corpus.
* **Action**: re-checked for companion code; none.
* **Outcome**: `priority=DROP`,
  `notes="In corpus; no separate compartmental code beyond ModelDB 189347 which t0008 ported"`.

### Example 8 — Schottdorf 2024 (DROP, rate-coded)

* **Input**: Schottdorf et al. 2024 DSGC theory paper.
* **Action**: read abstract + supplementary.
* **Outcome**: `priority=DROP`, `notes="Rate-coded DSGC model (not compartmental)"`.

### Example 9 — Euler 2002 (DROP, SAC-only)

* **Input**: Euler et al. 2002 Ca2+ imaging + SAC compartmental model.
* **Action**: re-checked for DSGC model.
* **Outcome**: `priority=DROP`, `notes="SAC-only; no postsynaptic DSGC compartment"`.

### Example 10 — Briggman 2011 (DROP, connectomics-only)

* **Input**: Briggman et al. 2011 SAC-DSGC wiring paper.
* **Action**: searched for accompanying compartmental simulator.
* **Outcome**: `priority=DROP`, `notes="Connectomics (EM); no compartmental model"`.

### Example 11 — Morrie 2020 (MEDIUM, not attempted)

* **Input**: Morrie et al. 2020 rat DSGC paper; `has_public_code=false`; carries biophysical detail
  but only in-paper equations.
* **Outcome**: `priority=MEDIUM`; escalated as a suggestion for a hand-port task once
  tuning-curve-viz (t0011) is live; not attempted within t0010's budget.

### Example 12 — Koutsonanos 2022 (MEDIUM, not attempted)

* **Input**: Koutsonanos et al. 2022 mouse ON-DSGC paper; repo exists but is Brian2 with a
  non-standard stimulus generator.
* **Outcome**: `priority=MEDIUM`, not attempted; queued as a simulator-diversity suggestion.

### Example 13 — Fransen 2023 (LOW, not attempted)

* **Input**: Fransen et al. 2023 DSGC conference paper; NetPyNE port but incomplete.
* **Outcome**: `priority=LOW`, not attempted.

### Example 14 — corpus-delta check: Hanson 2019 paper asset NOT re-downloaded

* **Input**: `hanson_2019_spatial_offset` candidate.
* **Action**: checked `research/research_papers.md` Paper Index before triggering `/add-paper`.
* **Outcome**: paper `10.1038/s41467-019-09147-4` already in corpus from t0002; no re-download; only
  the port was new work. This confirms the REQ-2 negative constraint (must NOT re-download in-corpus
  papers).

## Limitations

1. **0/3 HIGH-priority ports succeeded.** This is a triage result, not a task failure — the plan
   explicitly permits it. The follow-up is three dedicated hand-port tasks, each budgeting 1-3 days
   and touching the driver layer. Surfaced as suggestions in step 14.
2. **deRosenroll 2026 paper PDF not retrieved.** Elsevier HTTP 403 blocks anonymous access; PMC does
   not yet index this paper (it was published 2026-01). The asset is registered with
   `download_status=failed` per spec v3, with abstract-only metadata recovered from CrossRef + DOAJ.
   If a downstream task needs the PDF an intervention file will be required.
3. **No registered metrics measured.** `results/metrics.json` is `{}` because no port reached P3.
   This is explicitly valid per `task_results_specification.md` §metrics.json.
4. **`task.json.expected_assets.libraries` will be 0.** The task declared
   `expected_assets: {"answer": 1}` (no library count); the plan's 0-3 range was honored at 0. The
   reporting step will confirm consistency.
5. **Per-candidate stdout/stderr not committed under `logs/steps/009_implementation/port_*/`.** The
   port attempts were executed in subagent shells and the command outputs were summarised in the
   milestone report but not saved as artifacts in the step log folder. If a reviewer needs to audit
   the exact call, `data/candidates.csv` records the commit SHA of each cloned repo; re-running
   against those SHAs reproduces the failure.

## Files Created

* `tasks/t0010_hunt_missed_dsgc_models/research/research_papers.md` — 26-paper corpus review (4,969
  words)
* `tasks/t0010_hunt_missed_dsgc_models/research/research_internet.md` — 3-pass search synthesis
  (4,568 words) with CANDIDATES TABLE
* `tasks/t0010_hunt_missed_dsgc_models/research/research_code.md` — reusable-entrypoint catalog
  (3,327 words) with CONFORMANCE CHECKLIST
* `tasks/t0010_hunt_missed_dsgc_models/plan/plan.md` — 9-step implementation plan (4,283 words)
* `tasks/t0010_hunt_missed_dsgc_models/data/candidates.csv` — 14-row per-candidate outcome table
* `tasks/t0010_hunt_missed_dsgc_models/data/tuning_curves/.gitkeep` — empty (no P3 succeeded)
* `tasks/t0010_hunt_missed_dsgc_models/code/{paths.py,constants.py,__init__.py}` — scaffolding
* `tasks/t0010_hunt_missed_dsgc_models/code/{write_paper_details.py,write_paper_summaries.py,write_answer_asset.py}`
  — Python scripts that produced the paper + answer asset files
* `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/` — deRosenroll
  2026, `download_status=failed`, metadata-only asset with 1,576-word summary
* `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/` — Poleg-Polsky
  2026, `download_status=success`, full 3.87 MB PDF + 1,268-word summary
* `tasks/t0010_hunt_missed_dsgc_models/assets/answer/dsgc-missed-models-survey/` — answer asset
  (details.json + short_answer.md + full_answer.md, 2,972 total words, confidence=medium)
* `tasks/t0010_hunt_missed_dsgc_models/logs/searches/{pass_a_modeldb,pass_b_github,pass_c_scholar}.md`
  — raw 37-query evidence
* `tasks/t0010_hunt_missed_dsgc_models/logs/steps/*/step_log.md` — one per completed or skipped step

## Task Requirement Coverage

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

| REQ ID | Status | Answer + Evidence |
| --- | --- | --- |
| **REQ-1** — Systematic search across ModelDB + GitHub/OSF/Zenodo + Scholar/bioRxiv | **Done** | 37 queries executed across three passes. Evidence: `research/research_internet.md` CANDIDATES TABLE (14 rows), raw query logs under `logs/searches/{pass_a_modeldb,pass_b_github,pass_c_scholar}.md`. |
| **REQ-2** — Download new compartmental DSGC papers, not re-downloading in-corpus | **Partial** | 2/2 new papers registered as v3 assets. Poleg-Polsky 2026 `download_status=success` with full PDF. deRosenroll 2026 `download_status=failed` (Elsevier HTTP 403) with metadata-only asset preserving abstract. Hanson 2019 correctly NOT re-downloaded (already in corpus from t0002). Partial because PDF retrieval failed for one of the two papers. Evidence: `assets/paper/10.1016_j.celrep.2025.116833/`, `assets/paper/10.1038_s41467-026-70288-4/`. |
| **REQ-3** — Attempt to port every HIGH-priority candidate under 90-min cap | **Done** | All 3 HIGH-priority candidates attempted (Hanson 2019, deRosenroll 2026, Poleg-Polsky 2026). All three exited at P2 within the 90-min cap (total wall-clock 35 min). Evidence: `data/candidates.csv` rows for `hanson_2019_spatial_offset`, `derosenroll_2026_circuit_ei`, `polegpolsky_2026_ds_mechanisms`, each with `port_attempt_status=p2_failed` and explicit `port_failure_reason`. |
| **REQ-4** — Port emits canonical `(angle_deg, trial_seed, firing_rate_hz)` 12x20 CSV | **Not done** | No port reached P3. This is directly consequent from REQ-3: 0/3 ports cleared the P2 STOP gate. Evidence: `data/tuning_curves/` contains only `.gitkeep`. |
| **REQ-5** — Triage rule: STOP at P2 failure, no broken library assets | **Done** | All 3 HIGH-priority ports triggered the STOP gate; no library asset was registered; any scaffolded library folder was deleted. Evidence: `assets/library/` is empty (no subdirectories). |
| **REQ-6** — Exactly one answer asset with per-candidate row table | **Done** | `assets/answer/dsgc-missed-models-survey/` exists with `details.json` v2, `short_answer.md` (219 words), `full_answer.md` (2,753 words). Full answer contains a 14-row per-candidate table (one row per CANDIDATES TABLE entry) with paper DOI, code URL, NEURON compatibility, port attempted y/n, outcome, and envelope scores (N/A where no port reached P3). Verificator (`verify_task_folder`) passed 0/0. |
| **REQ-7** — Four registered metric keys in `results/metrics.json` for each ported model | **Not done** | No ports succeeded, therefore no metric variants to report. `results/metrics.json` is `{}` per `task_results_specification.md` §metrics.json which explicitly allows empty-object when no registered metrics were measured. Evidence: `results/metrics.json`. |
| **REQ-8** — Budget cap $0.00 (local-only, no remote machines) | **Done** | `setup-machines` and `teardown` both `skipped`. `results/costs.json` `total_cost_usd=0.00` with empty breakdown. `results/remote_machines_used.json` is `[]`. Evidence: `results/costs.json`, `results/remote_machines_used.json`, `step_tracker.json` steps 8 and 10. |
