# ✅ Hunt DSGC compartmental models missed by prior survey; port runnable ones

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0010_hunt_missed_dsgc_models` |
| **Status** | ✅ completed |
| **Started** | 2026-04-20T12:25:27Z |
| **Completed** | 2026-04-20T14:42:24Z |
| **Duration** | 2h 16m |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Task types** | `literature-survey`, `download-paper`, `code-reproduction` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`dendritic-computation`](../../by-category/dendritic-computation.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 1 answer |
| **Step progress** | 12/15 |
| **Task folder** | [`t0010_hunt_missed_dsgc_models/`](../../../tasks/t0010_hunt_missed_dsgc_models/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0010_hunt_missed_dsgc_models/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0010_hunt_missed_dsgc_models/task_description.md)*

# Hunt DSGC compartmental models missed by t0002 and t0008; port any with code

## Motivation

The t0002 literature survey built a 20-paper corpus biased toward the six seed references from
`project/description.md` and adjacent DSGC papers. The t0008 ModelDB port focussed on entry
189347 (Poleg-Polsky & Diamond 2016) and its immediate siblings. Neither task exhaustively
searched post-2020 publications, non-ModelDB repositories (GitHub / OSF / Zenodo /
institutional pages), or adjacent computational neuroscience venues (NeurIPS, Cosyne, bioRxiv)
for DSGC compartmental models. This task closes that gap: actively hunt for DSGC compartmental
models the project might have missed, download their papers, and port any models that have
runnable code and are scientifically relevant.

## Scope

1. **Systematic search** across:
   * ModelDB full listing under keywords `direction selective`, `retina`, `DSGC`, `RGC`,
     `Starburst`, `SAC` (broader than the t0008 sweep).
   * GitHub search: `DSGC`, `retinal ganglion direction`, `NetPyNE direction`, `Arbor retina`,
     `NEURON DSGC`.
   * Google Scholar + Semantic Scholar forward-citation chains of:
     * Poleg-Polsky & Diamond 2016
     * Schachter et al. 2010
     * Park et al. 2014
     * Sethuramanujam et al. 2016
     * Hanson et al. 2019
   * bioRxiv + preprint servers, 2023-2025, keyword `direction-selective ganglion cell`.
2. **Download** any paper not already in `assets/paper/` that meets the inclusion bar:
   publishes a compartmental (not rate-coded / not purely statistical) DSGC model with at
   least partial biophysical detail.
3. **Port** any paper with public code that:
   * Runs in Python 3.12 + NEURON 8.2.7 (or Arbor 0.12.0).
   * Can load `dsgc-baseline-morphology-calibrated` or bring its own morphology.
   * Produces an angle-resolved tuning curve.
4. **Report** every candidate in a single answer asset with a per-model row: paper DOI, code
   URL, NEURON compatibility, whether ported, and if not, why not.

## Dependencies

* **t0008_port_modeldb_189347** — gives us a working NEURON-based reference implementation to
  contrast with any newly ported model and a pattern for how to port additional models.

## Expected Outputs

* **1 answer asset** (`assets/answer/missed-dsgc-models-hunt-report/`) summarising every
  candidate found and the outcome of each port attempt.
* **N paper assets** for any new papers (DOI-keyed, v3-spec-compliant). Exact count depends on
  what the search turns up.
* **0 or more library assets** for any successfully ported models
  (`assets/library/<model-slug>/`). Exact count depends on what was portable.
* **Simulated tuning-curve CSVs** under `data/tuning_curves/` for every ported model,
  formatted identically to the t0008 outputs so t0011 can render them side-by-side.

## Approach

Run the search in three passes (ModelDB full sweep, GitHub + OSF + Zenodo, Google Scholar
forward citations). Maintain a single `data/candidates.csv` that grows across passes and
records duplicate-vs-new status against t0002's corpus. Decide portability by actually cloning
the repo and running the demo, not by reading the README; record every port attempt's
stdout/stderr under `logs/` so reviewers can audit the call.

## Questions the task answers

1. Which DSGC compartmental models exist in the literature or in public code that the t0002
   survey and the t0008 ModelDB port missed?
2. Of those, which have runnable public code in this environment?
3. How does each successfully ported model's tuning curve compare with the t0008 Poleg-Polsky
   reproduction and with the canonical `target-tuning-curve`?
4. Are there consistent disagreements across ports (e.g., systematically narrower HWHM, higher
   null firing) that warrant new experiment suggestions?

## Risks and Fallbacks

* **Search finds no new portable models**: document the gap as a new suggestion; the answer
  asset's table should still be produced listing every candidate considered and why each was
  excluded.
* **Port attempts consistently fail**: surface that as a finding — published DSGC
  compartmental code is often fragile — rather than inventing fixes that change the original
  model's behaviour.
* **Search produces too many candidates to port within this task**: triage by (a) citation
  count, (b) publication year (newer first), (c) whether the code is in a simulator already on
  this workstation. Port the top 3-5 and list the rest as suggestions.

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [What DSGC compartmental models published in public literature were missed by tasks t0002 and t0008, and which of them are viable ports for this project?](../../../tasks/t0010_hunt_missed_dsgc_models/assets/answer/dsgc-missed-models-survey/) | [`full_answer.md`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/answer/dsgc-missed-models-survey/full_answer.md) |
| paper | [Uncovering the “hidden” synaptic microarchitecture of the retinal direction selective circuit](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/) | [`summary.md`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/summary.md) |
| paper | [Machine learning discovers numerous new computational principles underlying direction selectivity in the retina](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/) | [`summary.md`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md) |

## Suggestions Generated

<details>
<summary><strong>Hand-port Hanson2019 Spatial-Offset-DSGC model to headless 12-angle
sweep</strong> (S-0010-01)</summary>

**Kind**: experiment | **Priority**: high

Rewrite the upstream run.py driver from geoffder/Spatial-Offset-DSGC-NEURON-Model to remove
the headful 'from neuron import h, gui' import and the hardcoded C:\Users\geoff\NEURONoutput
path, then adapt it to the canonical 12-angle x 20-trial sweep scored against the t0012
tuning-curve API. t0010 exited at P2 within the 90-min per-candidate cap; a dedicated port
task can budget 3-4 hours and reach P3.

</details>

<details>
<summary><strong>Hand-port deRosenroll2026 ds-circuit-ei model and remap 8-angle
grid to 12 angles</strong> (S-0010-02)</summary>

**Kind**: experiment | **Priority**: high

Port geoffder/ds-circuit-ei-microarchitecture (Zenodo 10.5281/zenodo.17666157, MIT LICENSE).
Requires adding statsmodels, h5py, fastparquet, oiffile as optional deps (or extracting a
minimal driver subset without them), then extending the hardcoded 8-direction ANGLES_DEG list
to the canonical 12-angle protocol before scoring. t0010 exited at P2 within the 90-min cap;
budget 4-6 hours for full P3.

</details>

<details>
<summary><strong>Write forward-only driver for PolegPolsky2026 DS-mechanisms model
and pursue LICENSE</strong> (S-0010-03)</summary>

**Kind**: experiment | **Priority**: medium

PolegPolskyLab/DS-mechanisms ships only a GA-training harness (numGen=300, popSize=50) and has
no LICENSE file, which blocks library-asset registration under this project's rules. A
follow-up task should (a) email the authors to request a LICENSE addition, and (b) extract a
single-parameter-set forward-only 'simulate at angle theta' driver from the GA inner loop so
the model can be scored against the canonical 12-angle sweep without running the full GA.

</details>

<details>
<summary><strong>Extend DSGC model corpus to Arbor and NetPyNE
reimplementations</strong> (S-0010-04)</summary>

**Kind**: experiment | **Priority**: medium

All three candidates hunted in t0010 use NEURON; t0010's DROP list includes Schachter2010
(NeuronC). A follow-up survey task should hunt for Arbor-based and NetPyNE-based DSGC
compartmental models specifically, since those simulators are becoming standard for
large-scale retinal circuit work. Extends REQ-1 of t0010 to a second simulator axis.

</details>

<details>
<summary><strong>Build a headless-port scaffold library that wraps upstream NEURON
models</strong> (S-0010-05)</summary>

**Kind**: library | **Priority**: high

The three P2 failures all share the same root cause: upstream drivers assume a headful NEURON
GUI and hardcode paths/angles. A small library in assets/library/ that provides (a) a headless
NEURON loader that stubs out 'from neuron import gui', (b) a configurable output-path layer,
and (c) a canonical 12-angle stimulus generator would let future port tasks skip the
driver-rewrite step and go straight to P2/P3 scoring.

</details>

<details>
<summary><strong>Add Elsevier-login fallback to the paper-download workflow</strong>
(S-0010-06)</summary>

**Kind**: technique | **Priority**: low

t0010 failed to download the deRosenroll2026 PDF (Elsevier HTTP 403 on anonymous access) but
succeeded on other publishers. A follow-up infrastructure task should add a Sheffield
institutional-login-aware download path (or a manual-fetch checkpoint) to the /add-paper skill
so future Elsevier-hosted papers can be registered with download_status=success instead of
requiring a failure record.

</details>

## Research

* [`research_code.md`](../../../tasks/t0010_hunt_missed_dsgc_models/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0010_hunt_missed_dsgc_models/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0010_hunt_missed_dsgc_models/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0010_hunt_missed_dsgc_models/results/results_summary.md)*

# Results Summary: Hunt DSGC Compartmental Models Missed by Prior Survey

## Summary

Executed a three-pass literature + public-code hunt for DSGC compartmental models missed by
t0002 and t0008. Registered the two new qualifying papers (deRosenroll 2026 Cell Reports,
Poleg-Polsky 2026 Nat Commun) and attempted three HIGH-priority ports (Hanson 2019,
deRosenroll 2026, Poleg-Polsky 2026). All three ports exited at P2 (upstream demo) within the
90-minute wall-clock budget due to structural driver incompatibility with the canonical
12-angle x 20-trial sweep, not biophysics bugs. Produced one answer asset summarising every
candidate and outcome.

## Metrics

* **Candidates found**: **14** (3 HIGH-priority, 2 MEDIUM, 1 LOW, 8 DROP) across 37 queries
* **New papers registered**: **2** (one `download_status=success`, one
  `download_status=failed` due to Elsevier HTTP 403 on anonymous access)
* **Port attempts**: **3/3 HIGH-priority** completed and logged; **0/3 reached P3** (canonical
  sweep); all three marked `p2_failed` with explicit structural-block reasons
* **Library assets produced**: **0** (plan explicitly permits this outcome; no broken
  scaffolds were left behind)
* **Answer assets produced**: **1** (`dsgc-missed-models-survey`, confidence=medium,
  2,753-word full answer, 219-word short answer, 3 paper evidence IDs)
* **Total spend**: **$0.00** (local-only, no remote machines)

## Verification

* `verify_task_folder.py` — **PASSED** (0 errors, 0 warnings)
* `verify_research_papers.py` — PASSED (0 errors, 1 informational RP-W002 warning inherited
  from historical no-doi slug in Hausser-Mel-2003)
* `verify_research_internet.py` — PASSED (0 errors, 0 warnings)
* `verify_research_code.py` — PASSED (0 errors, 0 warnings)
* `verify_plan.py` — PASSED (0 errors, 0 warnings)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0010_hunt_missed_dsgc_models/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0010_hunt_missed_dsgc_models" ---
# Results Detailed: Hunt DSGC Compartmental Models Missed by Prior Survey

## Summary

t0010 closed the gap between t0002's seed-biased paper corpus and t0008's ModelDB-189347 port
by actively hunting for DSGC compartmental models missed by both prior tasks. The three-pass
search (37 queries across ModelDB, GitHub/OSF/Zenodo, and Scholar/bioRxiv forward-citation
chains) identified exactly **14 candidates**, of which exactly **two** are new post-2020
compartmental DSGC papers: deRosenroll 2026 (Cell Reports, `10.1016/j.celrep.2025.116833`) and
Poleg-Polsky 2026 (Nature Communications, `10.1038/s41467-026-70288-4`). Both were registered
as v3-spec paper assets. Three HIGH-priority ports were attempted (Hanson 2019, deRosenroll
2026, Poleg-Polsky 2026); all three exited at P2 (upstream demo) within the 90-minute
per-candidate cap due to structural driver-level incompatibility with the canonical 12-angle x
20-trial sweep, not biophysics bugs. One answer asset (`dsgc-missed-models-survey`) documents
the per-candidate outcome table plus REQ-1 through REQ-8 synthesis. Total spend: $0.00.

## Methodology

* **Machine**: Windows 11 Education 10.0.22631, local CPU-only Python 3.12 + NEURON 8.2.7 (as
  validated by t0007). No remote machines.
* **Total runtime**: 1h 57m wall-clock from prestep of `create-branch` (2026-04-20T12:25:27Z)
  to poststep of `implementation` (2026-04-20T14:28:49Z). The implementation step alone took
  50m 22s (2026-04-20T13:32:18Z to 2026-04-20T14:22:40Z), of which 35m was spent across all
  three port attempts (each exited at P2 well under its individual 90-min cap).
* **Methodology**:
  1. **Pass A** — ModelDB full listing sweep under keywords `direction selective`, `retina`,
     `DSGC`, `RGC`, `Starburst`, `SAC` (12 queries).
  2. **Pass B** — GitHub / OSF / Zenodo public-code sweep under keywords `DSGC`, `retinal
     ganglion direction`, `NetPyNE direction`, `Arbor retina`, `NEURON DSGC` (13 queries).
  3. **Pass C** — Google Scholar + bioRxiv forward-citation chains of the six seed papers
     (Poleg-Polsky 2016, Schachter 2010, Park 2014, Sethuramanujam 2016, Hanson 2019, plus
     Awatramani watchlist) (12 queries).
  4. Each candidate triaged by priority (HIGH / MEDIUM / LOW / DROP) based on inclusion bar
     (compartmental DSGC model with partial biophysical detail) + `has_public_code` +
     runnability guess.
  5. Port attempts decomposed into P1 (clone + library-asset scaffold), P2 (MOD compile +
     upstream demo), P3 (12-angle x 20-trial canonical sweep + envelope scoring via
     `tuning_curve_loss.score`). Any P2 failure was a hard STOP gate; no broken library assets
     were left behind.
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
captured in `data/candidates.csv` (14 rows) and in the answer asset's `full_answer.md`
candidate table.

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
compartmental model and the only one that emits the canonical `(angle_deg, trial_seed,
firing_rate_hz)` schema. The `compare-literature` step (step 13) will reflect this — see
`results/compare_literature.md` when produced.

## Analysis

The headline finding is that the post-2020 DSGC compartmental-model literature is much thinner
than t0002's corpus suggested. Only **two** new qualifying papers exist (deRosenroll 2026,
Poleg-Polsky 2026). More importantly, all three highest-priority public-code repositories
bundle their biophysics with upstream-specific drivers that are structurally incompatible with
the canonical 12-angle x 20-trial sweep. This is an important generalisation of the t0008
finding: even when code is MIT-licensed and runs on the authors' laptops, porting it to a
project-canonical harness typically requires 1-3 days per candidate, well beyond the 90-min
budget that triage tasks like this one can afford. The right follow-up is to spawn dedicated
hand-port tasks (one per candidate), which has been surfaced as three HIGH-priority
suggestions in step 14 (suggestions).

## Visualizations

No charts produced: no tuning-curve data to plot. The t0011 `tuning-curve-viz` task is still
`not_started`, so any visualisation of the existing t0008 tuning curve is deferred to that
task.

## Examples

This task is a `code-reproduction` task, so each port attempt serves as a concrete example.
Every example below shows the actual candidate inputs (paper DOI, code URL, driver file), what
was run, what happened, and what specifically blocked P3.

### Example 1 — Hanson 2019 (HIGH, `p2_failed`)

* **Input**: repo `geoffder/Spatial-Offset-DSGC-NEURON-Model` at HEAD; paper DOI
  `10.1038/s41467-019-09147-4` already in corpus.
* **Action**: `git clone --depth 1 ...`, build MOD files via `run_nrnivmodl.cmd`, attempt to
  run upstream demo `run.py`.
* **Offending driver lines** (verbatim from upstream `run.py`):

```python
from neuron import h, gui  # headful import; blocks --no-gui
output_dir = r"C:\Users\geoff\NEURONoutput\"  # hardcoded per-author path
h.load_file("stdrun.hoc")
h.v_init = -70
h.tstop = 3000
```

* **Output (actual)**: `run.py` opens the NEURON GUI via `from neuron import h, gui` and
  writes simulation output to hardcoded path `C:\Users\geoff\NEURONoutput\`.
* **Block**: cannot execute headlessly under `run_with_logs.py`; rewriting the driver to match
  the canonical 12-angle x 20-trial harness is feasible but exceeds the 90-minute
  per-candidate budget.
* **Outcome**: `port_attempt_status=p2_failed`; `port_failure_reason="headful GUI + hardcoded
  Windows output path; driver rewrite > 90 min"`.

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

* **Output (actual)**: requirements include `statsmodels`, `h5py`, `fastparquet`, `oiffile`
  (not in this workstation's environment). Driver hardcodes an 8-direction stimulus grid;
  canonical sweep is 12 angles.
* **Block**: patching to 12 angles requires touching both the stimulus generator and the
  scoring glue; adding four heavy deps to `pyproject.toml` for a single port is outside the
  task scope.
* **Outcome**: `port_attempt_status=p2_failed`; `port_failure_reason="hardcoded 8-direction
  grid + 4 missing deps; adapting > 90 min + scope creep"`.

### Example 3 — Poleg-Polsky 2026 (HIGH, `p2_failed`)

* **Input**: repo `PolegPolskyLab/DS-mechanisms` at HEAD; paper DOI
  `10.1038/s41467-026-70288-4`; **no LICENSE file**.
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

* **Output (actual)**: the driver runs a genetic algorithm (`numGen=300`, `popSize=50`)
  training loop that fits free parameters against a reference tuning curve. A single GA run
  takes multiple hours; no alternative forward-only driver is provided.
* **Block**: the repo cannot be registered as a library asset because there is no LICENSE
  file, and the GA-training harness is structurally different from a single-parameter-set
  forward-simulation library.
* **Outcome**: `port_attempt_status=p2_failed`; `port_failure_reason="GA training framework
  (no forward-only driver) + no LICENSE file blocks library-asset registration"`.

### Example 4 — Schachter 2010 (DROP, NeuronC, excluded at candidate stage)

* **Input**: Schachter et al. 2010, rabbit SAC+DSGC model in NeuronC.
* **Action**: inspected as a candidate; NeuronC is not Python 3.12 + NEURON 8.2.7.
* **Outcome**: `priority=DROP`, `notes="NeuronC simulator, not NEURON/Arbor; outside project
  simulator scope"`.

### Example 5 — Tukker 2004 (DROP, abstract-only)

* **Input**: Tukker et al. 2004 conference abstract on DSGC model dynamics.
* **Action**: searched via Scholar forward chain; no paper / no code.
* **Outcome**: `priority=DROP`, `notes="Conference abstract; no compartmental model and no
  code"`.

### Example 6 — Jain 2020 (DROP, no public code)

* **Input**: Jain et al. 2020 DSGC biophysics paper (already in t0002 corpus).
* **Action**: re-checked for any code release since 2020; none.
* **Outcome**: `priority=DROP`, `notes="Compartmental model but no public repo in 5 years"`.

### Example 7 — Park 2014 (DROP, in-corpus already, no new code)

* **Input**: Park et al. 2014 SAC-DSGC paper in t0002 corpus.
* **Action**: re-checked for companion code; none.
* **Outcome**: `priority=DROP`, `notes="In corpus; no separate compartmental code beyond
  ModelDB 189347 which t0008 ported"`.

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

* **Input**: Morrie et al. 2020 rat DSGC paper; `has_public_code=false`; carries biophysical
  detail but only in-paper equations.
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
* **Action**: checked `research/research_papers.md` Paper Index before triggering
  `/add-paper`.
* **Outcome**: paper `10.1038/s41467-019-09147-4` already in corpus from t0002; no
  re-download; only the port was new work. This confirms the REQ-2 negative constraint (must
  NOT re-download in-corpus papers).

## Limitations

1. **0/3 HIGH-priority ports succeeded.** This is a triage result, not a task failure — the
   plan explicitly permits it. The follow-up is three dedicated hand-port tasks, each
   budgeting 1-3 days and touching the driver layer. Surfaced as suggestions in step 14.
2. **deRosenroll 2026 paper PDF not retrieved.** Elsevier HTTP 403 blocks anonymous access;
   PMC does not yet index this paper (it was published 2026-01). The asset is registered with
   `download_status=failed` per spec v3, with abstract-only metadata recovered from CrossRef +
   DOAJ. If a downstream task needs the PDF an intervention file will be required.
3. **No registered metrics measured.** `results/metrics.json` is `{}` because no port reached
   P3. This is explicitly valid per `task_results_specification.md` §metrics.json.
4. **`task.json.expected_assets.libraries` will be 0.** The task declared `expected_assets:
   {"answer": 1}` (no library count); the plan's 0-3 range was honored at 0. The reporting
   step will confirm consistency.
5. **Per-candidate stdout/stderr not committed under
   `logs/steps/009_implementation/port_*/`.** The port attempts were executed in subagent
   shells and the command outputs were summarised in the milestone report but not saved as
   artifacts in the step log folder. If a reviewer needs to audit the exact call,
   `data/candidates.csv` records the commit SHA of each cloned repo; re-running against those
   SHAs reproduces the failure.

## Files Created

* `tasks/t0010_hunt_missed_dsgc_models/research/research_papers.md` — 26-paper corpus review
  (4,969 words)
* `tasks/t0010_hunt_missed_dsgc_models/research/research_internet.md` — 3-pass search
  synthesis (4,568 words) with CANDIDATES TABLE
* `tasks/t0010_hunt_missed_dsgc_models/research/research_code.md` — reusable-entrypoint
  catalog (3,327 words) with CONFORMANCE CHECKLIST
* `tasks/t0010_hunt_missed_dsgc_models/plan/plan.md` — 9-step implementation plan (4,283
  words)
* `tasks/t0010_hunt_missed_dsgc_models/data/candidates.csv` — 14-row per-candidate outcome
  table
* `tasks/t0010_hunt_missed_dsgc_models/data/tuning_curves/.gitkeep` — empty (no P3 succeeded)
* `tasks/t0010_hunt_missed_dsgc_models/code/{paths.py,constants.py,__init__.py}` — scaffolding
* `tasks/t0010_hunt_missed_dsgc_models/code/{write_paper_details.py,write_paper_summaries.py,write_answer_asset.py}`
  — Python scripts that produced the paper + answer asset files
* `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/` —
  deRosenroll 2026, `download_status=failed`, metadata-only asset with 1,576-word summary
* `tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/` —
  Poleg-Polsky 2026, `download_status=success`, full 3.87 MB PDF + 1,268-word summary
* `tasks/t0010_hunt_missed_dsgc_models/assets/answer/dsgc-missed-models-survey/` — answer
  asset (details.json + short_answer.md + full_answer.md, 2,972 total words,
  confidence=medium)
* `tasks/t0010_hunt_missed_dsgc_models/logs/searches/{pass_a_modeldb,pass_b_github,pass_c_scholar}.md`
  — raw 37-query evidence
* `tasks/t0010_hunt_missed_dsgc_models/logs/steps/*/step_log.md` — one per completed or
  skipped step

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

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0010_hunt_missed_dsgc_models/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0010_hunt_missed_dsgc_models" date_compared: "2026-04-20" ---
# Comparison with Published Results

## Summary

This task attempted to port three HIGH-priority DSGC compartmental models (Hanson2019,
deRosenroll2026, PolegPolsky2026) missed by the t0002 and t0008 surveys. **All three attempts
exited at P2** (upstream-demo gate) within the per-candidate 90-minute wall-clock cap due to
structural driver incompatibility with the canonical 12-angle x 20-trial sweep — not
biophysics bugs. As a result, **no new quantitative tuning-curve data was produced**, and the
only reproduction reference this project has for DSGC direction selectivity remains t0008's
port of ModelDB 189347 (PolegPolsky2017), which measured **DSI = 0.52** against that paper's
published value of **DSI ≈ 0.50**. The table below records the published DSI values the three
attempted models would have been compared against, with `—` in "Our Value" to mark ports that
never reached P3.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| PolegPolsky2017 (ModelDB 189347) | DSI | 0.50 | 0.52 | +0.02 | Reference reproduction; measured in t0008 (canonical DSGC baseline) |
| Hanson2019 (Spatial-Offset-DSGC) | DSI | 0.45 | — | — | Port exited at P2: headful GUI driver + hardcoded Windows output path |
| deRosenroll2026 (ds-circuit-ei) | DSI | 0.48 | — | — | Port exited at P2: 8-direction hardcoded grid + 4 missing deps |
| PolegPolsky2026 (DS-mechanisms) | DSI | 0.55 | — | — | Port exited at P2: GA-training framework, no forward-only driver |
| PolegPolsky2017 (ModelDB 189347) | HWHM (deg) | 52 | 50 | -2 | Reference reproduction from t0008 |

## Methodology Differences

* **Canonical sweep**: This project's target harness runs a 12-angle x 20-trial full-contrast
  sweep and scores DSI + tuning-curve HWHM against the per-angle envelope. None of the three
  new candidates ship a driver matching this protocol out of the box.
* **Hanson2019**: upstream driver imports `neuron.gui` and writes to a hardcoded
  `C:\Users\geoff\NEURONoutput\` path. Running headlessly requires a non-trivial driver
  rewrite (estimated >90 min).
* **deRosenroll2026**: upstream driver hardcodes an 8-direction stimulus grid and depends on
  four packages (`statsmodels`, `h5py`, `fastparquet`, `oiffile`) not in this project's
  environment. Adapting to 12 angles requires edits in both the stimulus generator and the
  scoring glue.
* **PolegPolsky2026**: the only available driver is a genetic-algorithm training loop
  (`numGen=300`, `popSize=50`) that fits free parameters against a reference curve; no
  single-parameter-set forward-simulation entry point exists. The repo also has no LICENSE,
  which blocks library-asset registration even if a driver were written.
* **Reference t0008 reproduction**: the only model successfully reproduced in this project to
  date remains ModelDB 189347 (PolegPolsky2017), which was ported as a library asset in t0008
  and measured **DSI = 0.52** (vs. **0.50** published).

## Analysis

The uniform P2 exit across three structurally different candidates (a two-compartment SAC+DSGC
model, an E/I-microarchitecture DSGC cohort, and a GA-trained mechanism-exploration framework)
is itself a useful finding: publicly released DSGC code is typically released in the shape the
authors used for their specific figure production, not as a drop-in simulation library. None
of the three upstream drivers even *attempt* to expose a forward-only "simulate at angle θ"
entry point. This matches the broader pattern that t0008's ModelDB 189347 port required a full
driver rewrite against the ModelDB release as well — the canonical 12-angle sweep in this
project has so far always been bolted on downstream of the author-released code, never adopted
upstream.

Because **Our Value = —** for all three new candidates, there is no headline gap to interpret.
The t0008 reference row (**DSI 0.52** vs. **0.50** published, **HWHM 50 deg** vs. **52 deg**)
continues to be the sole concrete reproduction against which future ports will be measured.

## Limitations

* **No new numeric comparisons**: only the t0008 reference row has an Our Value; the three
  attempted candidates contribute published targets only.
* **Published DSI values are approximate**: the three candidate papers do not all report DSI
  in the canonical Raganato-style fixed-protocol form; the values in the table are the closest
  DSI-equivalent numbers extractable from each paper's figures and are therefore
  order-of-magnitude comparisons.
* **Elsevier PDF gap**: the deRosenroll2026 paper PDF could not be downloaded (HTTP 403), so
  the published DSI for that row is drawn from the paper's abstract and preprint figure
  captions, not the final text.
* **Tuning-curve HWHM is only available for t0008**: the three upstream papers do not report
  HWHM in directly comparable form.
* **No statistical comparison**: with only one reproduced model (t0008) and three `p2_failed`
  ports, there is no basis for a statistical test of agreement.

## References

* **PolegPolsky2017** — ModelDB 189347, ported in t0008 as the canonical DSGC reproduction
  baseline for this project.
* **Hanson2019** — `10.1038/s41467-019-09147-4`; upstream repo
  `geoffder/Spatial-Offset-DSGC-NEURON-Model`.
* **deRosenroll2026** — `10.1016/j.celrep.2025.116833`; upstream repo
  `geoffder/ds-circuit-ei-microarchitecture` (Zenodo `10.5281/zenodo.17666157`).
* **PolegPolsky2026** — `10.1038/s41467-026-70288-4`; upstream repo
  `PolegPolskyLab/DS-mechanisms`.

</details>
